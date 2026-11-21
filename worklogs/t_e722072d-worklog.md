# Worklog — t_e722072d

## Kontext
Wurzel-Fix: Worker kennen nur `no_code_reason` und verwechseln es bei reinen Doku-/Worklog-Lieferungen mit vorhandenen Commits → "kein Code-Commit"-Ablehnungen und Fehlblockaden (Beleg: t_584544e0, Team-Klärung t_b99dbd1e; Review: kpt-doc docs/reviews/prozess-klaerungen/2026-11-07-done-gate-repo-pfad-integration-worklog.md). Aufgabe: `docs_only_reason` in den Profil-SOULs verankern.

## Aktionen
1. Bestand geprüft: `/workspace/.hermes/SOUL.md` hatte docs_only_reason bereits 1× (arbeitsprozess-K7-Zeile); die 5 Profil-SOULs (software-development, devops, qa, architect, scrummaster) hatten nur no_code_reason.
2. Verwalteten Generator gesucht: kein hermes-config-kpt-Repo lokal, kein Generator für die no_code_reason-Zeile gefunden (nur donegate-check.sh/gate.py, die docs_only_reason bereits unterstützen). → direkt editiert gemäß repos.json (Config = kijan-hermes-shared, kanonisch `push`, Ziel dev).
3. In jedem der 5 Profil-SOULs den Satz direkt nach der no_code_reason-Stelle (team-klaerung-Block) eingefügt:
   "Bewusst reine Doku-/Worklog-Lieferung mit vorhandenen Commits: metadata.docs_only_reason (>=30 Zeichen) — nicht no_code_reason. Preflight: bash /workspace/.hermes/scripts/donegate-check.sh <task-id> <repo> [--docs-only '<grund>']."
4. Haupt-SOUL (/workspace/.hermes/SOUL.md) enthält docs_only_reason bereits konsistent an der K7-Stelle — keine Änderung nötig.

## Geaenderte / erstellte Dateien
- /workspace/.hermes/profiles/software-development/SOUL.md (live, +1 Zeile)
- /workspace/.hermes/profiles/devops/SOUL.md (live, +1 Zeile)
- /workspace/.hermes/profiles/qa/SOUL.md (live, +1 Zeile)
- /workspace/.hermes/profiles/architect/SOUL.md (live, +1 Zeile)
- /workspace/.hermes/profiles/scrummaster/SOUL.md (live, +1 Zeile)
- worklogs/t_e722072d-worklog.md (diese Datei)
Hinweis: Die SOUL.md-Dateien liegen unter /workspace/.hermes/ und sind in keinem Git-Repo versioniert (geprüft: kein Repo trackt SOUL.md); die funktionale Änderung ist dort live, dieses Repo sichert den Worklog-Nachweis.

## Tests / Verifikation
Befehl: `grep -c docs_only_reason` über alle 6 Dateien.
Ergebnis: software-development=1, devops=1, qa=1, architect=1, scrummaster=1, /workspace/.hermes/SOUL.md=1 — alle ≥1, DoD erfüllt.

## Dev-Integration
Commit auf task/t_e722072d, gepusht nach push/dev (kijan007-agent/kijan-hermes-shared) via `git push push HEAD:dev`.
