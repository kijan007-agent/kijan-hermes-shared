# Worklog — t_b7890121

## Kontext
Cross-Profile-Infrastruktur: (1) state.db-Wachstum — profiles/software-development/state.db war zum Befundzeitpunkt 4,7 GB (aktuell 6,74 GB), /workspace 78–84 % belegt; Lauf 62860 crashte mit "disk is probably full". (2) Kontext-Kompaktierungs-Deckel — Lauf 62846: 27 Kompaktierungsversuche fielen durch den 600-s-Deckel (`Context compression reached its total ceiling after 600.0s ... continuing without compression`). Eltern-Klärungen t_032c251f (/dev/null behoben, purge-Dry-Run rc=0 nachgewiesen) und t_459551b8 (Gateway-Erschöpfung, kein fachlicher Blocker) sind abgeschlossen. Die Karte war auf einen abschliessbaren ersten Schritt zugeschnitten: Rebase, Worklog in Pflicht-Form, Test ausführen, Done-Gate + kanban_complete.

Ursachen-Nachweis (dieser Lauf):
- Freelist-Check der drei groessten DBs: software-development 6.74 GB / freelist 0.00 GB; devops 2.81 GB / freelist ~0; web-development 3.04 GB / freelist 0.06 GB. Das Wachstum ist echtes Inhaltswachstum (kompaktierte Messages + Sessions ohne Aufbewahrungsregel), keine Fragmentierung — Purge ist das richtige Mittel, VACUUM nur nach grossen Loeschungen noetig.
- Deckel-Key in Hermes-Quelle verifiziert: agent/conversation_compression_deadline.py liest `compression.context_total_ceiling_seconds` (Default 600, config_defaults.py:642) und hebt den Deckel zusaendlich auf das Aux-Budget `auxiliary.compression.timeout` (Zeilen 52–56). Die Fehlermeldung stammt aus agent/compression_facade.py:57.

## Aktionen
- `git -C /workspace/.worktrees/t_b7890121 fetch push --prune && git rebase push/dev` → "Current branch task/t_b7890121 is up to date", rc=0; HEAD == push/dev == dcda74d4a55de2281679aa27676acb5bc9d9b740; Arbeitsbaum sauber.
- Deliverables aus Vorversuchen (untracked) uebernommen und gegen die Hermes-Quelle verifiziert:
  - `scripts/purge-state-db.sh`: Retention-Purge (Default 30d) ueber alle Profile; loescht nur beendete, ungepinnte, nicht-archivierte Sessions batchweise (FTS-Trigger laufen mit), prueft vorab `PRAGMA integrity_check(1)`, flock pro DB, Bestaetigungs-Pflicht (-y/--dry-run), wal_checkpoint(TRUNCATE), optional `--vacuum`, .bak-Rotation.
  - `scripts/set-compression-limits.py`: setzt pro Profil-`config.yaml` `compression.context_total_ceiling_seconds` (Default 1800), `compression.context_timeout_seconds` (300) und `auxiliary.compression.timeout` (900); erhaelt fremde Schluessel; Dry-Run-Modus.
- Test 1 (echte Profile, Dry-Run): `bash scripts/purge-state-db.sh --dry-run` — die ersten 7 Profile wurden abgearbeitet ohne Fehler (architect: wuerde 72 Sessions / 26754 Messages purgen; arzt: 45 / 49885; creative: 14 / 15994; data-science: 51 / 28190; apple u. a.: keine purgefaehigen Sessions), rc je Profil 0. Der Gesamtdurchlauf ueberschritt das Terminal-Tool-Limit (420 s), weil die SUM(LENGTH(...))-Abfrage ueber 6-GB-DBs lang laeuft — daher Live-Purge als Folgekarte geplant (siehe Dev-Integration).
- Test 2 (synthetische DB, echter Purge): 20 alte Sessions a 50 Messages (je 4x50 KB Inhalt, ~191 MB) + 1 laufende Session (ended_at NULL) in profiles-root-Kopie; `purge-state-db.sh --profiles-root <tmp> --retention-days 30 -y` → rc=0, 20 Sessions + 1000 Messages geloescht, `live`-Session und deren 10 Messages erhalten.
- Test 3 (Purge + VACUUM, Groesse vorher/nachher): frische synthetische DB, `purge-state-db.sh ... --vacuum -y` → rc=0, Dateigroesse 200.728.576 → 16.384 Bytes, `PRAGMA integrity_check` = ok, nur `live`-Session vorhanden.
- Test 4 (Kompression, temporaeres Profil): config.yaml mit `auxiliary.compression.total_ceiling_seconds: 600` + Fremdkey; Dry-Run rc=0; Live-Lauf rc=0; Readback: `compression.context_total_ceiling_seconds: 1800`, `compression.context_timeout_seconds: 300`, `auxiliary.compression.timeout: 900` gesetzt, Fremdkey `some_other: keep_me` erhalten, "1 Datei(en) geprueft, 0 Fehler".
- Worklog angelegt (Pflicht-Form via donegate-check.sh --template), Skripte + Worklog committet, auf push/dev geliefert.

## Geaenderte / erstellte Dateien
- scripts/purge-state-db.sh — Aufbewahrungsregel + Purge/VACUUM-Mechanismus fuer state.db aller Profile (Retention 30d, integrity- und flock-geschuetzt, laufende Sessions bleiben)
- scripts/set-compression-limits.py — setzt Kontext-Kompaktierungs-Deckel (1800 s) + Aux-Timeout (900 s) cross-profile, Dry-Run faehig
- worklogs/t_b7890121-worklog.md — dieser Worklog
- Aufraeumen: Test-Synthetic-DBs unterhalb cache/scratch (fällige 24h-Bereinigung, keine Repo-Artefakte)

## Tests / Verifikation
- `git fetch push --prune && git rebase push/dev` → rc=0, up to date, HEAD==push/dev==dcda74d4
- `bash scripts/purge-state-db.sh --dry-run` (echte Profile) → rc=0 pro Profil; quantifiziert Purgebares (z. B. architect 72 Sessions/26754 Messages); Abbruch des Gesamtdurchlaufs erst durch 420-s-Tool-Limit
- synthetischer Purge: `purge-state-db.sh --profiles-root <tmp> --retention-days 30 -y` → rc=0; 20 Sessions/1000 Messages geloescht; laufende Session (`ended_at IS NULL`) + deren Messages erhalten
- synthetischer Purge+VACUUM: `purge-state-db.sh ... --vacuum -y` → rc=0; **200.728.576 → 16.384 Bytes** (Vorher/Nachher-Nachweis); `PRAGMA integrity_check` = ok
- `set-compression-limits.py --profiles-root <tmp>` (Dry-Run + Live) → rc=0; Readback bestaetigt `context_total_ceiling_seconds: 1800` statt Default 600, Fremdkeys erhalten, 0 Fehler
- Key-Verifikation gegen Quelle: conversation_compression_deadline.py:44 (`context_total_ceiling_seconds`), config_defaults.py:642 (Default 600), compression_facade.py:57 (Fehlermeldung) — die vom Skript gesetzten Schluessel sind die von Hermes tatsaechlich gelesenen
- Nicht in diesem Lauf ausgefuehrt (Folgekarte): Live-Purge+VACUUM der echten Multi-GB-DBs (Ursache: 2700-s-Task-Budget + aktive Profile; Mechanismus selbst ist durch die synthetischen Tests mit echtem sqlite3-Pfad belegt).

## Dev-Integration
- Commit(s): siehe `git rev-parse HEAD` in /workspace/.worktrees/t_b7890121 — auf push/dev (kijan-hermes-shared, kanonisches Remote gemaess repos.json) geliefert
- donegate-check.sh PREFLIGHT: OK vor kanban_complete
- Folgekarte erstellt: Live-Purge (mit --vacuum) der grossen Profil-DBs + Anwendung von set-compression-limits.py auf die echten Profile + Cron-Einrichtung der Retention
