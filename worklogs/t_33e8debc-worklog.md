# Worklog — t_33e8debc

## Kontext

Task `t_33e8debc` ([DevOps] Systemische Konfigurationsprobleme beheben) aus der
Zerlegung von `t_b316161f` (Inventar aller 13 blockierten Tasks).

Ziel: die systemischen Konfigurationsprobleme beheben, die mehrere Tasks blockieren —
Credentials, `repos.json`, Gate-Scripts. Akzeptanzkriterien: Credentials korrekt
konfiguriert, `repos.json` konsistent, Scripts funktionsfähig, Fix an mindestens einem
betroffenen Task nachweisbar.

Ausgangslage aus dem Eltern-Hand-off (t_b316161f): 13 blockierte Tasks in vier Kategorien —
A) Gate-Infrastruktur (2), B) DEV_VERIFY (9), C) leerer Workspace (1), D) Nutzer-Terminierung (1).
Kein Block durch Worker-Fehler bei Repo-Pfad/Worktree/Worklog.

## Aktionen

1. **Credentials geprüft.**
   - `/workspace/.git-cred` existiert nicht — der im Task genannte Pfad war nie belegt.
   - `git config --global credential.helper` zeigte auf
     `store --file=/data/hermes-workspaces/kpt/.git-credentials`.
   - `findmnt -T /data/hermes-workspaces/kpt` → Mount ist `ro`. `/workspace` ist `rw`.
   - `stat -c '%i %n'` auf beide Credential-Pfade → identische Inode 44800528: dieselbe
     Datei, zweimal gemountet (rw über `/workspace`, ro über `/data/hermes-workspaces`).
   - Folge: jeder HTTPS-Push brach mit
     `fatal: unable to get credential storage lock in 1000 ms: Read-only file system` ab.
     Push lief durch, aber Credential-Updates (Token-Rotation) waren unmöglich.

2. **Fix angewendet:** `git config --global credential.helper "store --file=/workspace/.git-credentials"`.
   Persistenz geprüft: `HOME` des Profils ist `/workspace/.hermes/profiles/devops/home`,
   `.gitconfig` ist eine echte Datei auf dem Volume (kein Symlink), überlebt Neustarts.

3. **Submodul-Helper vereinheitlicht.** Zwei Abweichungen auf den kanonischen Store
   umgestellt: `kpt-app-ciq` (zeigte auf ephemeres `/tmp/git-cred`) und
   `kpt-website-pre-release` (zeigte auf ein profil-lokales File).
   Alle Stores enthalten beide Credential-Varianten (`x-access-token`, `kijan007`) für github.com.

4. **`repos.json` geprüft:** alle 8 kpt-Submodule zeigen auf `kijan007`, `basis_branch`
   durchgängig `dev`, `kijan-hermes-shared` korrekt mit `kanonisch_remote=push`,
   `kpt-lib` ausdrücklich als lokales Anchor-Repo ohne Remote dokumentiert.
   Remote-Auflösung in `kpt-deliver.sh` (kanonisch_remote → push → origin) gegen die
   tatsächlichen Remotes geprüft — korrekt.

5. **Scripts geprüft:** `donegate-check.sh` und `kpt-deliver.sh` ausführbar und funktionsfähig.
   `gate.py` ist die volle Gate-Logik (28819 Byte, seit 2026-11-02 07:28 wiederhergestellt;
   davor 12-Byte-Stub `placeholder` — Ursache der 2 Gate-Klärungs-Blockaden).

6. **Doku erstellt:** `devops/git-workspace-maintenance/references/kpt-credential-und-worktree-konvention.md`
   mit Credential-Analyse, `repos.json`-Tabelle, Script-Nachweis und der korrekten
   Worktree-Erstellung (Standardfall, kijan-hermes-shared, Regeln, Worklog-Vorlage, Lieferung).

7. **Worktree angelegt:**
   `git -C /workspace/kijan-hermes-shared worktree add .worktrees/t_33e8debc -b task/t_33e8debc push/dev`
   (Basis `push/dev` = 34b8948).

## Geaenderte / erstellte Dateien

- `devops/git-workspace-maintenance/references/kpt-credential-und-worktree-konvention.md` — neu: Credential-Analyse (read-only-Mount als Ursache), `repos.json`-Konsistenztabelle, Script-Verifikation, Worktree-/Liefer-Konvention, Restbefunde.
- `worklogs/t_33e8debc-worklog.md` — neu: dieser Worklog.

Ausserhalb des Repos (Laufzeit-Konfiguration, nicht versioniert):
- `/workspace/.hermes/profiles/devops/home/.gitconfig` — `credential.helper` umgestellt (Backup: `.gitconfig.bak-t_33e8debc`).
- `/workspace/Github/KijanPersonalTracker/.git/modules/kpt-app-ciq/config` — `credential.helper` umgestellt.
- `/workspace/Github/KijanPersonalTracker/.git/modules/kpt-website-pre-release/config` — `credential.helper` umgestellt.

## Tests / Verifikation

- `git push --dry-run upstream HEAD:refs/heads/task/probe-t_33e8debc` in kpt-backend → `* [new branch] HEAD -> task/probe-t_33e8debc`, exit 0, **kein Lock-Fehler** (vorher: `unable to get credential storage lock in 1000 ms: Read-only file system`).
- `git push --dry-run upstream HEAD:refs/heads/task/probe-t_33e8debc` in kpt-app-ciq → exit 0, kein Lock-Fehler.
- `git push --dry-run upstream HEAD:refs/heads/task/probe-t_33e8debc` in kpt-doc (origin) → exit 0, kein Lock-Fehler.
- `bash /workspace/.hermes/scripts/donegate-check.sh t_57b817ba --no-code "<Begründung>"` → `PREFLIGHT: OK` — **Fix an einem betroffenen Task nachgewiesen** (die Team-Klärung t_57b817ba war durch den defekten Gate-Stub blockiert).
- `bash /workspace/.hermes/scripts/donegate-check.sh --template t_33e8debc` → Vorlage mit allen 6 Pflicht-Sektionen.
- `git -C /workspace/Github/KijanPersonalTracker status --porcelain` → nur ` M <submodul>` (Pointer auf geänderte `.git/modules/*/config`), kein Superprojekt-Diff.
- `git config --global credential.helper` → `store --file=/workspace/.git-credentials`.
- `stat -c '%i %n' /workspace/.git-credentials /data/hermes-workspaces/kpt/.git-credentials` → beide 44800528 (identische Datei, rw über `/workspace`).
- `bash /workspace/.hermes/scripts/donegate-check.sh t_33e8debc <repo> <sha>` → siehe Ergebnis der Lieferung.

## Dev-Integration

- Branch: `task/t_33e8debc` in `kijan-hermes-shared`, Basis `push/dev` (34b8948).
- Remote: `push` = `kijan007-agent/kijan-hermes-shared` (Fork); `origin` = `kijan/kijan-hermes-shared` ohne Schreibrecht.
- Commit(s): siehe `git rev-parse HEAD` im Worktree, geliefert auf `push/dev`.
