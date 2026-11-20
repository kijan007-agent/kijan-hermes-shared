#!/usr/bin/env bash
# purge-state-db.sh — Cross-Profile state.db-Aufbewahrung: alte, beendete Sessions
# inklusive Messages purgen (FTS-Trigger halten die Indizes konsistent), dann VACUUM,
# plus Rotation alter state.db.bak_*-Reparaturbackups.
#
# Hintergrund (Task t_b7890121): state.db wächst unbegrenzt (software-development: 4,7 GB,
# /workspace 84% belegt, Lauf 62860 crashte mit "disk is probably full"). 1,3 Mio.
# kompaktierte Messages (1,7 GB) werden nie entfernt, es existiert kein Purge/VACUUM.
#
# Sicherheit:
#   - Nur Sessions mit ended_at IS NOT NULL (kein laufender Prozess), nicht gepinnt,
#     nicht archiviert (Archivierung ist Nutzerentscheidung), aelter als RETENTION_DAYS.
#   - flock pro DB verhindert Parallellauf; integrity_check vorher.
#   - Messages werden batchweise geloescht (FTS-/Trigram-Trigger laufen mit).
#   - -wal/-shm vor VACUUM per wal_checkpoint(TRUNCATE) geleert.
#   - --dry-run zeigt nur, was passieren wuerde.
#
# Usage:
#   purge-state-db.sh [--profiles-root DIR] [--retention-days N] [--batch N]
#                     [--vacuum] [--dry-run] [--bak-keep N] [--bak-age-days N] [-y]
# Env: PURGE_STATE_DB_CONFIRM=1 entspricht -y.
set -uo pipefail

PROFILES_ROOT="${PURGE_PROFILES_ROOT:-/workspace/.hermes/profiles}"
RETENTION_DAYS="${PURGE_RETENTION_DAYS:-30}"
BATCH="${PURGE_BATCH:-5000}"
DO_VACUUM=0
DRY_RUN=0
BAK_KEEP="${PURGE_BAK_KEEP:-2}"
BAK_AGE_DAYS="${PURGE_BAK_AGE_DAYS:-7}"
ASSUME_YES=0

while [ $# -gt 0 ]; do
    case "$1" in
        --profiles-root) PROFILES_ROOT="$2"; shift 2 ;;
        --retention-days) RETENTION_DAYS="$2"; shift 2 ;;
        --batch) BATCH="$2"; shift 2 ;;
        --vacuum) DO_VACUUM=1; shift ;;
        --dry-run) DRY_RUN=1; shift ;;
        --bak-keep) BAK_KEEP="$2"; shift 2 ;;
        --bak-age-days) BAK_AGE_DAYS="$2"; shift 2 ;;
        -y|--yes) ASSUME_YES=1; shift ;;
        -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
        *) echo "unbekannte Option: $1" >&2; exit 2 ;;
    esac
done

LOG_TAG="[purge-state-db]"
log() { echo "$LOG_TAG $(date '+%Y-%m-%d %H:%M:%S') $*"; }
die() { log "FEHLER: $*"; exit 1; }

if [ ! -d "$PROFILES_ROOT" ]; then die "profiles-root fehlt: $PROFILES_ROOT"; fi
command -v sqlite3 >/dev/null || die "sqlite3 nicht gefunden"

if [ "$ASSUME_YES" -ne 1 ] && [ "${PURGE_STATE_DB_CONFIRM:-0}" != "1" ]; then
    if [ "$DRY_RUN" -ne 1 ]; then
        die "Kein Bestätigungs-Flag (-y/--yes, --dry-run oder PURGE_STATE_DB_CONFIRM=1)"
    fi
fi

if [ "$DRY_RUN" -eq 1 ]; then
    log "DRY-RUN: es wird nichts geloescht"
fi

LOG_ERR="${TMPDIR:-/tmp}/purge-state-db-stderr.log"

# sqlite3 mit langem busy-Timeout: VACUUM/DELETE blockieren sonst, wenn der
# Gateway/Worker parallel auf derselben DB schreibt (SQLITE_BUSY).
SQLITE=(sqlite3 -cmd ".timeout 60000")

total_msgs=0; total_sessions=0; total_bytes_before=0; total_bytes_after=0

purge_db() {
    local db="$1" profile="$2"
    [ -f "$db" ] || return 0

    local size_before size_after
    size_before=$(stat -c %s "$db" 2>/dev/null || echo 0)

    # flock pro DB: keine doppelten Purges, kein Mischen mit anderen Wartungslaeufen
    local lock="/tmp/purge-state-db-$(basename "$profile").lock"
    (
        flock -n 9 || { log "$profile: laeuft bereits — uebersprungen"; exit 0; }

        local integrity
        integrity=$("${SQLITE[@]}" "$db" "PRAGMA integrity_check(1);" 2>&1 | head -1)
        if [ "$integrity" != "ok" ]; then
            log "$profile: integrity_check fehlerhaft ($integrity) — übersprungen (Reparatur via check-all-hermes-state-db.sh)"
            exit 0
        fi

        local cutoff now
        now=$(date +%s)
        cutoff=$(( now - RETENTION_DAYS * 86400 ))

        local n_sessions n_msgs msg_bytes delta_file
        delta_file="${AGG_FILE:-/tmp/purge-state-db-aggregate.$$}"
        n_sessions=$("${SQLITE[@]}" "$db" "SELECT COUNT(*) FROM sessions WHERE ended_at IS NOT NULL AND pinned=0 AND archived=0 AND ended_at < $cutoff;")
        n_msgs=$("${SQLITE[@]}" "$db" "SELECT COUNT(*) FROM messages WHERE session_id IN (SELECT id FROM sessions WHERE ended_at IS NOT NULL AND pinned=0 AND archived=0 AND ended_at < $cutoff);")
        # Bytes nur aus stabilen Spalten (context/reasoning/api_content) — die
        # Codex-Spalten sind optional, Spaltenfehler duerfen den Purge nicht stoppen.
        msg_bytes=$("${SQLITE[@]}" "$db" "SELECT COALESCE(ROUND(SUM(LENGTH(COALESCE(content,''))+LENGTH(COALESCE(tool_calls,''))+LENGTH(COALESCE(reasoning,''))+LENGTH(COALESCE(api_content,'')))/1048576.0),0) FROM messages WHERE session_id IN (SELECT id FROM sessions WHERE ended_at IS NOT NULL AND pinned=0 AND archived=0 AND ended_at < $cutoff);")

        if [ "$n_sessions" -eq 0 ]; then
            log "$profile: keine purgefaehigen Sessions (Retention ${RETENTION_DAYS}d) — keine Aenderung"
            exit 0
        fi

        if [ "$DRY_RUN" -eq 1 ]; then
            log "$profile: DRY-RUN wuerde purgen: $n_sessions Sessions, $n_msgs Messages (~${msg_bytes} MB Inhalt), VACUUM=$DO_VACUUM"
            # Auch im DRY-RUN aggregieren (sonst zeigt die Zusammenfassung 0/0).
            echo "$n_msgs $n_sessions $size_before $size_before" >> "$delta_file"
            exit 0
        fi

        log "$profile: purge ${n_sessions} Sessions / ${n_msgs} Messages (~${msg_bytes} MB Inhalt, Retention ${RETENTION_DAYS}d)"

        # 1) Messages purgefaehiger Sessions batchweise loeschen (FTS-Trigger laufen mit).
        local deleted=0 batch_deleted
        while :; do
            batch_deleted=$("${SQLITE[@]}" "$db" "
                DELETE FROM messages WHERE id IN (
                    SELECT id FROM messages WHERE session_id IN (
                        SELECT id FROM sessions WHERE ended_at IS NOT NULL AND pinned=0 AND archived=0 AND ended_at < $cutoff
                    ) LIMIT $BATCH
                );
                SELECT changes();")
            [ -z "$batch_deleted" ] && batch_deleted=0
            [ "$batch_deleted" -eq 0 ] && break
            deleted=$((deleted + batch_deleted))
        done
        log "$profile: $deleted Messages geloescht"

        # 2) Aux-Tabellen der geloeschten Sessions leeren (DELETE-CASCADE deckt
        #    session_model_usage ab; übrige Tabellen sind messagebezogen).
        "${SQLITE[@]}" "$db" "DELETE FROM session_model_usage WHERE session_id IN (SELECT id FROM sessions WHERE ended_at IS NOT NULL AND pinned=0 AND archived=0 AND ended_at < $cutoff);"

        # 3) Sessions selbst loeschen
        "${SQLITE[@]}" "$db" "DELETE FROM sessions WHERE ended_at IS NOT NULL AND pinned=0 AND archived=0 AND ended_at < $cutoff;"
        log "$profile: ${n_sessions} Sessions geloescht"

        # 4) WAL leeren, damit der Platz in der Haupt-DB sichtbar wird
        "${SQLITE[@]}" "$db" "PRAGMA wal_checkpoint(TRUNCATE);" >/dev/null 2>&1

        # 5) VACUUM: Platz tatsaechlich ans Dateisystem zurueckgeben
        if [ "$DO_VACUUM" -eq 1 ]; then
            log "$profile: VACUUM läuft (kann einige Minuten dauern)..."
            if "${SQLITE[@]}" "$db" "VACUUM;" 2>>"$LOG_ERR"; then
                log "$profile: VACUUM abgeschlossen"
            else
                log "$profile: VACUUM fehlgeschlagen — Size-Check unten zeigt den realen Stand"
            fi
        fi

        size_after=$(stat -c %s "$db" 2>/dev/null || echo 0)
        log "$profile: Groesse ${size_before} -> ${size_after} Bytes ($(( size_before/1048576 )) MB -> $(( size_after/1048576 )) MB)"

        # Aggregat: EINE Zeile pro Profil (msgs sessions bytes_before bytes_after),
        # damit die Zusammenfassung nicht nur das letzte Profil zaehlt.
        echo "$deleted $n_sessions $size_before $size_after" >> "$delta_file"
    ) 9>"$lock"
}

AGG_FILE="/tmp/purge-state-db-aggregate.$$"
: > "$AGG_FILE"

# ---------- 1) Rotation alter .bak-Reparaturbackups ----------
rotate_baks() {
    local dir="$1"
    # aelter als BAK_AGE_DAYS: weg
    find "$dir" -maxdepth 1 -name 'state.db.bak_*' -type f -mtime +"$BAK_AGE_DAYS" -print0 2>/dev/null | \
        xargs -0 -r rm -f
    # mehr als BAK_KEEP behalten: die juengsten BAK_KEEP behalten, Rest weg
    local keep=0
    while IFS= read -r bak; do
        keep=$((keep + 1))
        [ "$keep" -le "$BAK_KEEP" ] && continue
        rm -f "$bak"
    done < <(ls -t "$dir"/state.db.bak_* 2>/dev/null)
}

for profile_dir in "$PROFILES_ROOT"/*/; do
    [ -d "$profile_dir" ] || continue
    profile="$(basename "$profile_dir")"
    db="$profile_dir/state.db"
    purge_db "$db" "$profile"
    [ "$DRY_RUN" -eq 1 ] || rotate_baks "$profile_dir"
done

log "=== Zusammenfassung ==="
if [ -s "$AGG_FILE" ]; then
    # Format pro Zeile: msgs sessions bytes_before bytes_after
    read -r total_msgs total_sessions bsum asum < <(awk '{m+=$1; s+=$2; b+=$3; a+=$4} END {print m+0, s+0, b+0, a+0}' "$AGG_FILE")
    log "  Bytes gesamt: ${bsum} -> ${asum} ($(( bsum/1048576 )) MB -> $(( asum/1048576 )) MB)"
fi
log "  Sessions geloescht: $total_sessions"
log "  Messages geloescht: $total_msgs"
log "  Retention: ${RETENTION_DAYS}d, VACUUM: $DO_VACUUM, DRY-RUN: $DRY_RUN"
rm -f "$AGG_FILE"
exit 0
