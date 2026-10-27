# Worklog — t_9d2cdb94

## Kontext

Team-Klärung (assignee: scrummaster) zum Dispatcher-Befund aus Lauf 59088 / Task
t_a6fcd671. Ausgangsfragen: (1) clientseitige Heartbeat-Rate-Limitierung, (2) Dispatcher
soll Heartbeats als Stale-Signal behandeln und/oder Default-Runtime-Caps setzen,
(3) Quota-gate-Flapping abfedern.

- Projekte-Hub: http://projekte.kijan.ch/ideas/633 (Eintrag `Review: Dispatcher-Befund Lauf 59088`).
Repository: kijan-hermes-shared (kanonisches Remote `push` = kijan007-agent/kijan-hermes-shared,
Ziel-Branch `dev`).

Zwei Vorläufe (61523, 61541) crashten mit "model hit max output tokens" — dieser Lauf
(61798) arbeitet deshalb mit kurzen Einzelschritten und DB-Auswertung statt Langtext.

## Aktionen

1. `kanban_show()` / DB-Abfrage auf `/workspace/.hermes/kanban.db` — Task-Body, Events
   und Kommentar t_26ca3e9e gelesen. Ergebnis: 30 Unblocks (1792789827→1793030204),
   0 Spawns für t_a6fcd671.
2. Prioritätsverteilung der Ready-Lane rekonstruiert (`task_events`: promoted/unblocked/
   reclaimed → ready; claimed/scheduled/blocked/completed/archived → raus).
   Ergebnis: zu jedem Unblock ≥ 12 Ready-Tasks mit `priority > 175`; Zieltask prio 175.
   → Prioritäts-Aushungerung als Hauptursache identifiziert (Ergänzung zum Ausgangsbefund).
3. Gegenprobe aktueller Bestand: `select count(*) from tasks where status='ready'` → 45,
   davon 2 mit `priority > 175` (Lane inzwischen leer).
4. Dispatcher-Pfad im Quelltext geprüft: Claim-Auswahl nach `priority DESC`
   (`hermes_cli/kanban_db_dispatch.py`, `recompute_ready` in `kanban_db.py`),
   Kapazität `max_in_progress=12` / `max_in_progress_per_profile=5`.
5. Heartbeat-Bridge im Runtime-Code lokalisiert: Commit `bc31ee5cf8`
   "fix(kanban): bridge worker runtime activity to board heartbeat".
6. `autounblock.py` geprüft (Quota-Gate-Probe): Flap-Zyklen über 3 Tage bestätigt.
7. Entscheidungen getroffen (siehe Review-Artefakt §3) und 3 Folgekarten angelegt:
   - `t_89e4977f` (software-development) Heartbeat-Rate-Limit clientseitig
   - `t_162f3992` (architect) Default-Cap 4 h + Sturm-Erkennung
   - `t_0dbdb378` (devops) Hysterese + Eskalation im autounblock-Gate
8. Entscheidungen als Kommentar (Kommentar-ID 47609) auf t_9d2cdb94 hinterlegt.
9. Worktree angelegt: `git -C /workspace/kijan-hermes-shared fetch push dev` →
   `git worktree add .worktrees/t_9d2cdb94 -b task/t_9d2cdb94 push/dev`.
10. Review-Artefakt geschrieben und committet, dann Projekte-Hub-Eintrag erstellt.

## Geaenderte / erstellte Dateien

- `docs/reviews/kpt/2026-10-27-dispatcher-befund-lauf-59088.md` — Review-Artefakt mit
  Befund-Recap, Zusatzbefund (Prioritäts-Aushungerung), Entscheidungen und Folgekarten.
- `worklogs/t_9d2cdb94-worklog.md` — dieser Worklog.

## Tests / Verifikation

- `python3` (kanban.db, Rekonstruktion Ready-Lane) → 30 Unblocks im Fenster,
  zu jedem Zeitpunkt ≥ 12 Ready-Tasks mit prio > 175, 0 Spawns.
- `sqlite3 "select count(*) from tasks where status='ready'"` → 45; davon 2 mit prio > 175.
- `git -C /workspace/kijan-hermes-shared worktree list` → neuer Worktree `.worktrees/t_9d2cdb94`
  auf Branch `task/t_9d2cdb94` von `push/dev`.
- `bash /workspace/.hermes/scripts/donegate-check.sh t_9d2cdb94 <repo> <sha>` → siehe
  Dev-Integration.
- Projekte-Hub: POST http://projekte.kijan.ch/api/ideas → HTTP 201, ID siehe Dev-Integration.

## Dev-Integration

- Commits: `a5e955d645916e7a387f0932a835c9bf1e97e687` ("docs(review): t_9d2cdb94 -- Dispatcher-Befund
  Lauf 59088 (Heartbeat-Sturm, Runtime-Caps, Quota-Gate)") auf `origin/dev` geliefert
  (Push `push HEAD:dev` erfolgreich, `git log push/dev` zeigt a5e955d).
- Push-Ziel: `push` (= kijan007-agent/kijan-hermes-shared), Branch `dev` (kanonisch laut
  repos.json: `kanonisch_remote: push`, `basis_branch: dev`).
- Projekte-Hub-Einträge (theme "Prozess-/Sprint-Reviews 2026-10-27"):
  - Ankerpunkt Review: http://projekte.kijan.ch/ideas/633
  - F-01 Heartbeat-Sturm: http://projekte.kijan.ch/ideas/634
  - F-02 Default-Runtime-Cap: http://projekte.kijan.ch/ideas/635
  - F-03 Quota-Gate-Flapping: http://projekte.kijan.ch/ideas/636
  - F-04 Ready-Lane-Aushungerung: http://projekte.kijan.ch/ideas/637
  - Datei (raw): https://raw.githubusercontent.com/kijan007-agent/kijan-hermes-shared/dev/docs/reviews/kpt/2026-10-27-dispatcher-befund-lauf-59088.md
