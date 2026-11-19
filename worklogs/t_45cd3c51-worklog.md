# Worklog — t_45cd3c51

## Kontext

Task `t_45cd3c51` („kpt-deliver.sh: fetch --prune + docs-only Trockenlauf einbauen"),
DevOps-Profil. Zwei aufeinanderfolgende Team-Klärungen (`t_f62955c3` Hub 791,
`t_8d8a7ae5`) haben dieselbe systematische Lücke am Liefer-Skript
`/workspace/.hermes/scripts/kpt-deliver.sh` belegt:

- **K13 (Inseln):** Das Done-Gate bewertet **alle** Tracking-Refs der kanonischen Remotes.
  Stale Tracking-Refs (z. B. `origin/task/<id>`, remote nicht mehr vorhanden) erzeugen K13,
  obwohl die Arbeit korrekt auf `dev` liegt. Die Refspec-Korrektur aus `t_f62955c3` verhindert
  *neue* stale Refs, räumt aber bestehende Altlasten nicht ab — dafür fehlt ein `fetch --prune`.
- **K14 (Race):** `dev` zieht ~8 Commits/3 h. Ein Worker, der 40–90 min läuft, steht zum
  Abschlusszeitpunkt hinter dem dev-Tip. `kpt-deliver.sh` macht fetch+rebase+push, aber ohne
  `--prune` und ohne die Möglichkeit, den docs-only-Trockenlauf
  (`donegate-check.sh <task> --docs-only "<grund>"`) im selben Skript zu reproduzieren.

Ausgangslage (in diesem Lauf reproduziert):
- `bash /workspace/.hermes/scripts/kpt-deliver.sh t_093662a8 <worktree>` lieferte nach
  **erfolgreichem Push** (`OK: <sha> auf origin/dev`) trotzdem `PREFLIGHT: FAIL` mit
  „kein Code-Commit … oder bei bewusst reiner Doku-Lieferung metadata.docs_only_reason setzen".
- `donegate-check.sh` beherrschte `--docs-only` bereits positionsunabhängig (Zeile 44–68);
  `kpt-deliver.sh` reichte es nicht durch.

## Aktionen

1. **Orientierung.** `kanban_show(t_45cd3c51)`, `/workspace/.hermes/repos.json`,
   `/etc/hermes/done-gate/policy.json` (Instanz `kpt`: Ziel-Branch `dev`, `require_worklog: true`,
   `canonical_owner: kijan007`), `gate.py` (K11 `code_commit_errors`, K13/K14 `island_errors`,
   Worklog-Sektionen `worklog_sections`). Manifest-Repo `kijan-hermes-shared`:
   `kanonisch_remote = push` (`kijan007-agent/kijan-hermes-shared`), Ziel-Branch `dev`, danach PR.

2. **Skript analysiert.** `/workspace/.hermes/scripts/kpt-deliver.sh` (105 Zeilen):
   Schritt 4 war `g fetch -q "$remote" "$branch"` — **ohne** `--prune`; die abschließende
   Gate-Zeile war `donegate-check.sh "$t" "$repo"` — **ohne** `--docs-only`.

3. **Änderung 1 — `fetch --prune` (K13).** Schritt 4 des Rebase/Push-Loops wurde:
   `g fetch -q --prune "$remote" "+refs/heads/*:refs/remotes/$remote/*"`.
   Der explizite Wildcard-Refspec ist nötig, weil ein auf einen Branch eingeschränkter
   Fetch-Refspec (`+refs/heads/dev:refs/remotes/<remote>/dev`) stale Refs **nicht** prune-t —
   genau die Ursache aus `t_f62955c3` (dort 306 stale Refs). Der Wildcard-Refspec deckt alle
   Branches ab; `--prune` entfernt die, die es remote nicht mehr gibt.

4. **Änderung 2 — `--docs-only "<grund>"`.** Neuer optionaler Parameter neben `--branch` und
   `--remote`. Wird an die abschließende `donegate-check.sh`-Zeile durchgereicht:
   `donegate-check.sh "$t" --docs-only "$docs_only" "$repo" "$sha"`.
   Ohne den Parameter bleibt das bisherige Verhalten unverändert (Rückwärtskompatibilität).
   Der `$sha` wurde zusätzlich mit übergeben — vorher ging der aktuelle Commit nicht in die
   Gate-Prüfung ein.

5. **Arbeitskopie angelegt.** Konfig-Repo `kijan007/hermes-config-kpt` (Basis `origin/dev`),
   Branch `task/t_45cd3c51`, Worktree `/workspace/.worktrees/t_45cd3c51/config`.
   `kijan-hermes-shared`: Worktree `/workspace/.worktrees/t_45cd3c51/shared`, Branch
   `task/t_45cd3c51`, Basis `push/dev`.

6. **K13 verifiziert (Konfig-Repo `kijan-hermes-shared`).**
   `git fetch --prune push '+refs/heads/*:refs/remotes/push/*'` → danach
   `git for-each-ref refs/remotes/push/task | wc -l` = 3 und
   `git ls-remote --heads push 'refs/heads/task/*' | wc -l` = 3 → **keine stale Refs**.
   Gegenprobe im Projekt-Repo `kpt-backend`: nach `git fetch --prune origin` bzw. `upstream`
   (jeweils mit Wildcard-Refspec) `git for-each-ref refs/remotes/<remote>/task | wc -l` = 276 und
   `git ls-remote --heads <remote> 'refs/heads/task/*' | wc -l` = 276 → **keine stale Refs**
   (vor der Refspec-Korrektur aus `t_f62955c3` waren es 216 lokal vs. 166 remote).

7. **K14-Trockenlauf für `t_b6e78edd` (docs-only).**
   Worktree `kpt-backend/.worktrees/t_b6e78edd` (neu, auf `origin/dev`,
   `46b945cab`) angelegt; `worklogs/t_b6e78edd-worklog.md` liegt dort vor.
   `bash /workspace/.hermes/scripts/donegate-check.sh t_b6e78edd --docs-only "<Begründung>" \
   <worktree> 2e0f4ffc0cd7ebd3ae3c7a649befa8214c3005e1` → **`PREFLIGHT: OK`**.
   K13-Nebenprobe: alle acht Refs mit `t_b6e78edd` im Namen
   (`refs/heads/task/t_b6e78edd`, `…-ci`, `remotes/{origin,upstream,integration,kanban-origin,ssh-kijan007}/…`)
   haben `git rev-list --count <ref> --not origin/dev upstream/dev` = **0** → keine Insel.

8. **K13-Isolation der Task-eigenen Branches geprüft.** Die Gate-Prüfung bewertet Branches, deren
   Name die Task-ID enthält. Für den neuen Branch `task/t_45cd3c51` gilt dasselbe wie für
   `t_b6e78edd`: Der Branch wird nach dem Push auf `dev` integriert, damit `rev-list --count`
   gegen die Ziel-Branches 0 ergibt.

9. **Lieferung.** Beide Worktrees committet (Commit-Message enthält die Task-ID), Rebase auf den
   kanonischen Remote, Push auf `dev` + `task/<task-id>`, Gate-Trockenlauf.

## Geaenderte / erstellte Dateien

- `scripts/kpt-deliver.sh` — geändert: `fetch --prune` mit Wildcard-Refspec im Rebase/Push-Loop,
  neuer Parameter `--docs-only "<grund>"` mit Durchreichung an `donegate-check.sh`,
  `$sha` wird mit übergeben, Kopfkommentar mit Änderungsnachweis und Task-ID.
- `worklogs/t_45cd3c51-worklog.md` — dieser Worklog.

Nicht versioniert (Container-Laufzeitkonfiguration, kein Projektcode):
- `/workspace/.hermes/scripts/kpt-deliver.sh` — das aktive Skript (identischer Stand wie
  `scripts/kpt-deliver.sh` im Config-Repo; dort versioniert).

## Tests / Verifikation

- `bash -n /workspace/.hermes/scripts/kpt-deliver.sh` → exit 0 (Syntax ok).
- `git fetch --prune push '+refs/heads/*:refs/remotes/push/*'` (kijan-hermes-shared) → exit 0.
- `git for-each-ref refs/remotes/push/task | wc -l` → 3; `git ls-remote --heads push 'refs/heads/task/*' | wc -l` → 3 → **keine stale Refs** (K13).
- `git fetch --prune origin '+refs/heads/*:refs/remotes/origin/*'` (kpt-backend) → exit 0;
  `git for-each-ref refs/remotes/origin/task | wc -l` → 276; `git ls-remote --heads origin 'refs/heads/task/*' | wc -l` → 276 → **keine stale Refs** (K13).
- `git fetch --prune upstream '+refs/heads/*:refs/remotes/upstream/*'` (kpt-backend) → exit 0;
  `git for-each-ref refs/remotes/upstream/task | wc -l` → 276; `git ls-remote --heads upstream 'refs/heads/task/*' | wc -l` → 276 → **keine stale Refs** (K13).
- `git rev-list --count <ref> --not origin/dev upstream/dev` für alle 8 Refs mit `t_b6e78edd` im Namen → je **0** → K13 ohne Insel.
- `bash /workspace/.hermes/scripts/donegate-check.sh t_b6e78edd --docs-only "<Begründung>" \
  /workspace/Github/KijanPersonalTracker/kpt-backend/.worktrees/t_b6e78edd 2e0f4ffc0cd7ebd3ae3c7a649befa8214c3005e1`
  → **`PREFLIGHT: OK`** (K14-Trockenlauf).
- `git -C <worktree> status --porcelain --untracked-files=no` → leer (nach Commit).
- `bash /workspace/.hermes/scripts/kpt-deliver.sh t_45cd3c51 <worktree>` → `OK: <sha> auf <remote>/dev`, Abschluss `PREFLIGHT: OK`.

## Dev-Integration

- Config-Repo `kijan007/hermes-config-kpt`: Branch `task/t_45cd3c51`, Basis `origin/dev`,
  Commits mit Task-ID `t_45cd3c51` in der Message, gepusht auf `dev` + `task/t_45cd3c51`.
- `kijan-hermes-shared`: Branch `task/t_45cd3c51`, Basis `push/dev` (Fork
  `kijan007-agent/kijan-hermes-shared`), Commits mit Task-ID, auf `push/dev` integriert.
- Abschlussprüfung: `bash /workspace/.hermes/scripts/donegate-check.sh t_45cd3c51 <worktree> <sha>`.

## Abschluss-Verifikation (Lauf t_45cd3c51, 2026-11-19)

- `bash -n scripts/kpt-deliver.sh` → exit 0 (Syntax ok).
- `diff scripts/kpt-deliver.sh /workspace/.hermes/scripts/kpt-deliver.sh` → identisch
  (aktives Laufzeit-Skript = versionierter Stand).
- K13 Config-Repo: `git fetch --prune origin '+refs/heads/*:refs/remotes/origin/*'` →
  `git for-each-ref refs/remotes/origin/task | wc -l` = 35,
  `git ls-remote --heads origin 'refs/heads/task/*' | wc -l` = 35 → **keine stale Refs**.
- K13 `kijan-hermes-shared`: `git for-each-ref refs/remotes/push/task | wc -l` = 5,
  `git ls-remote --heads push 'refs/heads/task/*' | wc -l` = 5 → **keine stale Refs**.
- K14-Trockenlauf: `bash /workspace/.hermes/scripts/donegate-check.sh t_b6e78edd --docs-only \
  "<Begründung>" /workspace/Github/KijanPersonalTracker/kpt-backend/.worktrees/t_b6e78edd \
  2e0f4ffc0cd7ebd3ae3c7a649befa8214c3005e1` → **`PREFLIGHT: OK`**.
- Gate-Trockenlauf des Tasks selbst:
  `bash /workspace/.hermes/scripts/donegate-check.sh t_45cd3c51 \
  /workspace/.worktrees/t_45cd3c51/config cce82d4a092a47f990dc63435dd3bad798ad87b2`
  → **`PREFLIGHT: OK`**.
- PR-Hinweis: Das im Manifest genannte kanonische Repo `kijan/kijan-hermes-shared` ist mit
  keinem der drei im Container hinterlegten Credentials (`kijan007`, `x-access-token`,
  `kijan007-agent`) auffindbar — GitHub API antwortet durchgängig `404 Not Found`
  (auch `git ls-remote`), und `kijan007-agent/kijan-hermes-shared` ist laut API kein Fork
  (`fork: false`, kein `parent`). Die Lieferung deshalb direkt auf den laut Manifest
  kanonischen Remote `push` (`kijan007-agent/kijan-hermes-shared`, Ziel-Branch `dev`);
  ein PR gegen `kijan/kijan-hermes-shared` ist aus dem Container nicht erstellbar.

## Zusatzbefund im selben Lauf: Gate sah nur HEAD (K11-Falle)

Bei der ersten `kpt-deliver.sh`-Ausführung in diesem Lauf war der letzte Commit der
reine Worklog-Commit (`21ab74cf`), der Code-Commit lag darunter (`cce82d4`). Das Skript
meldete dem Gate nur `HEAD` → das Gate wertete „kein Code-Commit" und lehnte ab
(`PREFLIGHT: FAIL`), obwohl der Code-Commit auf `origin/dev` integriert war.

Fix in `scripts/kpt-deliver.sh`: es werden jetzt **alle** Commits mit Task-ID in der
Message auf dem Ziel-Branch (`git log --format=%H -F --grep="$t" -n 50 "$remote/$branch"`)
plus `HEAD` an `donegate-check.sh` übergeben. Danach: `OK: e595f525… auf origin/dev` →
`PREFLIGHT: OK`.
