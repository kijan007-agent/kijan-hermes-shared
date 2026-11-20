# Worklog — t_edbb0e12

## Kontext
Follow-up zu t_1ddab3fc: Worker-Schritte, die einen Bericht per `kanban_attach` an
eine Karte haengen, senden die Bytes als Inline-Base64 im Tool-Call-Argument.
~9 kB Bericht = ~11.6k Zeichen Tool-Output -> Max-Output-Tokens, Call wird
abgeschnitten und nie ausgefuehrt (Lauf 61866 Crash, Lauf 62022
Compression-Cooldown-Schleife, t_26ca3e9e). Auftrag: (1) Worker-Guidance fuer alle
Profile, (2) pruefen, ob Dispatcher/Task-Schnittstelle grosse Anhang-Schritte
vermeiden kann.

Repo-Wahl (war Ursache von 50+ Fehlversuchen): Das in der Karte genannte
`hermes-config` existiert nirgends als Git-Repo — `/workspace/.hermes` hat kein
`.git` (`git rev-parse` -> fatal), und `github.com/kijan007/hermes-config-kpt`
liefert "Repository not found" (waehrend `kpt-backend` am selben Host erreichbar
ist, also kein Auth-Problem). Kanonisches Hermes-Config-Repo mit `dev`-Branch ist
`kijan-hermes-shared` (repos.json: pfad `/workspace/kijan-hermes-shared`,
kanonisch_remote `push`, ziel `dev`). Die Worker-Guidance liegt dort in
`devops/kanban-worker/SKILL.md` und `devops/kanban-orchestrator/SKILL.md` und wird
per Cron-Job "Hermes Skills Sync" in die aktiven Profile kopiert — identischer
Stand mit `/workspace/.hermes/skills/` (diff Exit 0).

## Aktionen
- `kanban_show` + Attempts gelesen; Zielrepo-Suche: `/workspace/.hermes` (kein Git),
  `git ls-remote` gegen `kijan007/hermes-config-kpt` (nicht gefunden),
  `kijan007/hermes-config` (nicht gefunden).
- `git -C /workspace/kijan-hermes-shared remote -v` -> `push` = kijan007-agent,
  Branch `dev` vorhanden; vorhandener Worktree
  `/workspace/kijan-hermes-shared/.worktrees/t_edbb0e12` (branch `task/t_edbb0e12`)
  wiederverwendet statt neu geklont.
- `git fetch push` + `git rebase push/dev` -> "Current branch task/t_edbb0e12 is up
  to date", Basis `1f43e49`, Arbeitsbaum sauber.
- `devops/kanban-worker/SKILL.md`: neuer Abschnitt "Attachments: never inline
  base64 above ~4 kB (t_edbb0e12)" — Schwellwert ~3 kB Datei, danach
  commit+SHA-Referenz / `kanban_attach_url` / Repo-Pfad; Retry-Verbot fuer
  identisches Base64; Block statt Grinding.
- `devops/kanban-orchestrator/SKILL.md`: neuer Abschnitt "Card bodies must not
  require large inline attachments (t_edbb0e12)" — Kartentexte schreiben Lieferung
  als commit+Referenz fest, echter Anhang nur per URL in eigener Karte.
- Dispatcher-Pruefung (Auftrag 2) in `docs/reviews/devops-ci/2026-11-20-anhang-base64-tool-call.md`
  dokumentiert: kein Flow-Guard inspiziert Tool-Argumente (grep `flow_guard`/
  "Flow guard" ohne Fund in den Python-Quellen), bestehende Guardrails in
  `agent/turn_preflight.py`/`turn_recovery.py` wirken auf den Kontext, wirksame
  Backstop-Stelle waere `tools/kanban_tools.py` (Handler `kanban_attach`) — nur als
  Folge-Karte, da Kern-Patch am Agent-Fork ausserhalb der KPT-Repos.

## Geaenderte / erstellte Dateien
- `devops/kanban-worker/SKILL.md` — Anhang-Regel fuer alle Worker (kein Inline-Base64 > ~4 kB).
- `devops/kanban-orchestrator/SKILL.md` — Kartentexte ohne grosse Anhang-Schritte.
- `docs/reviews/devops-ci/2026-11-20-anhang-base64-tool-call.md` — Befund, Dispatcher-Pruefung, Begruendung "Regel 1 reicht vorlaeufig".
- `worklogs/t_edbb0e12-worklog.md` — diese Datei.

## Tests / Verifikation
- `grep -c "t_edbb0e12" devops/kanban-worker/SKILL.md devops/kanban-orchestrator/SKILL.md` -> `devops/kanban-worker/SKILL.md:1`, `devops/kanban-orchestrator/SKILL.md:1` (beide Abschnitte vorhanden).
- Schwellwert-Nachweis: `python3 -c "... base64.b64encode(b'x'*kb*1024) ..."` -> `3 kB file -> 4100 chars`, `4 kB file -> 5464 chars`, `9 kB file -> 12292 chars`. Bestaetigt den Befund (~9 kB -> ~11.6k Zeichen) und die gewaehlte ~3-kB-Grenze (bleibt unter 4 kB Argument).
- `diff -q /workspace/kijan-hermes-shared/devops/kanban-worker/SKILL.md /workspace/.hermes/skills/devops/kanban-worker/SKILL.md` -> Exit 0 (shared-Repo ist Quelle der in Profile geladenen Skills).
- Cron `jobs.json`: Job "Hermes Skills Sync" vorhanden (kopiert Skills in `~/.hermes/skills`) — die Regel greift damit ab dem naechsten Sync-Lauf in jedem Worker-Run, ohne dass jede Profil-SOUL einzeln geaendert wird.
- `bash /workspace/.hermes/scripts/donegate-check.sh t_edbb0e12 <worktree> <sha>` -> PREFLIGHT: OK (Ausgabe im Abschluss-Kommentar).

## Dev-Integration
- Commit(s): auf `push/dev` via `bash /workspace/.hermes/scripts/kpt-deliver.sh t_edbb0e12 /workspace/kijan-hermes-shared/.worktrees/t_edbb0e12` (SHA wird im Abschluss-Kommentar und in metadata.commits genannt).
- Arbeitsbaum nach Push sauber (`git status --porcelain --untracked-files=no` leer).
