# KPT: Credential-Konvention und korrekte Worktree-Erstellung

Befund-Dokumentation zu Task `t_33e8debc` ([DevOps] Systemische Konfigurationsprobleme beheben).
Stand: 2026-11-02.

## 1. Credential-Store: read-only Mount war die Ursache

### Symptom
Jeder `git push` gegen GitHub (HTTPS) brach mit ab:

```
fatal: unable to get credential storage lock in 1000 ms: Read-only file system
```

Der Push selbst lief durch, aber Git konnte den Credential-Store nicht aktualisieren.
Ein Token-Rotation oder ein `git credential approve` schlug damit fehl.

### Ursache
`credential.helper` (global, in `/workspace/.hermes/profiles/devops/home/.gitconfig`) zeigte auf

```
store --file=/data/hermes-workspaces/kpt/.git-credentials
```

`/data/hermes-workspaces` ist ein eigener, **read-only** gemounteter Mount:

```
findmnt -T /data/hermes-workspaces/kpt
TARGET                  SOURCE                       FSTYPE OPTIONS
/data/hermes-workspaces /dev/sdb[/hermes-workspaces] ocfs2  ro,relatime,...
/workspace               /dev/sdb[/hermes-workspaces/kpt] ocfs2 rw,relatime,...
```

Beide Pfade zeigen auf denselben Volume-Subpfad — dieselbe Datei, zweimal gemountet
(nachgewiesen über identische Inode-Nummer 44800528):

```
stat -c '%i %n' /workspace/.git-credentials /data/hermes-workspaces/kpt/.git-credentials
44800528 /workspace/.git-credentials
44800528 /data/hermes-workspaces/kpt/.git-credentials
```

Über `/workspace` ist die Datei beschreibbar, über `/data/hermes-workspaces` nicht.
Der Helper griff also auf den schreibgeschützten Pfad zu und scheiterte am Lock.

### Fix
Helper auf den beschreibbaren Pfad umstellen:

```bash
git config --global credential.helper "store --file=/workspace/.git-credentials"
```

Persistenz: `HOME` des Profils ist `/workspace/.hermes/profiles/devops/home`, die `.gitconfig`
liegt als echte Datei auf dem Volume (kein Symlink, nicht im Config-Repo tracked) und
überlebt Container-Neustarts.

### Verifikation
```bash
cd /workspace/Github/KijanPersonalTracker/kpt-backend
git push --dry-run upstream HEAD:refs/heads/task/probe
# -> * [new branch] HEAD -> task/probe     (kein Lock-Fehler, exit 0)
```
Ebenso für `kpt-app-ciq` (upstream) und `kpt-doc` (origin) geprüft.

## 2. Submodul-Credential-Helper vereinheitlichen

`credential.helper` war über die Submodule hinweg uneinheitlich. Zwei Abweichungen
wurden auf den kanonischen Store umgestellt:

| Submodul | vorher | nachher |
|---|---|---|
| `kpt-app-ciq` | `store --file=/tmp/git-cred` (ephemer, `/tmp` nicht persistent) | `store --file=/workspace/.git-credentials` |
| `kpt-website-pre-release` | `store --file=/workspace/.hermes/profiles/devops/home/.git-credentials` (Profil-lokal) | `store --file=/workspace/.git-credentials` |

Die übrigen Submodule nutzen `store --file /workspace/.hermes/profiles/web-development/cache/scratch/.gh-creds`.
Diese Datei enthält dieselben zwei Credential-Varianten (`x-access-token` und `kijan007`)
für `github.com` und funktioniert. Sie liegt allerdings im Scratch-Cache eines
fremden Profils — deshalb ist `/workspace/.git-credentials` die kanonische Quelle.

Alle Stores enthalten beide Eintraege fuer `https://github.com`:
- `//x-access-token:<token>` (App-Token)
- `//kijan007:<token>` (PAT)

`/workspace/.config/gh/hosts.yml` ist korrekt (`user: kijan007`, Token vorhanden),
wird aber nicht genutzt: die `gh`-CLI ist im Container nicht installiert
(`gh: not found` — von `kpt-deliver.sh` bewusst herausgefiltert).

## 3. `repos.json` ist konsistent

Pruefung gegen die Remote-Konvention `kijan007/<repo>`:

| Repo | origin | upstream | kanonisch_remote | Ziel |
|---|---|---|---|---|
| kpt-backend | kijan007 | kijan007 | upstream | dev |
| kpt-app-ciq | kijan007 | kijan007 | upstream | dev |
| kpt-doc | kijan007 | kijan007 | origin | dev |
| kpt-website | kijan007 | kijan007 | origin | dev |
| kpt-admin | kijan007 | kijan007 | upstream | dev |
| kpt-datafield-ciq | kijan007 | kijan007 | upstream | dev |
| kpt-common-barrels-ciq | kijan007 | kijan007 | upstream | dev |
| kpt-symptoms-app | kijan007 | kijan007 | upstream | dev |
| kijan-hermes-shared | kijan (kein Schreibrecht) | — | `push` (kijan007-agent-Fork) | dev |
| kpt-lib | lokal, kein Remote | — | — | dev (nicht lieferbar) |

Alle Eintraege zeigen auf `kijan007`, `basis_branch` ist ueberall `dev`.
`kpt-lib` ist ausdruecklich als lokales Anchor-Repo ohne Remote dokumentiert.

Pruefung der Remote-Aufloesung in `kpt-deliver.sh`: es liest `kanonisch_remote` aus
`repos.json` und faellt auf `push`, dann `origin` zurueck. Bei `kpt-backend` liefert
`upstream` (kijan007) — korrekt. Bei `kpt-doc`/`kpt-website` liefert `origin`
(kijan007) — ebenfalls korrekt, weil dort beide Remotes auf kijan007 zeigen.

## 4. Gate-Scripts funktionsfaehig

- `/etc/hermes/done-gate/gate.py`: 28819 Byte, volle Gate-Logik (seit 2026-11-02 07:28 vom Host wiederhergestellt; davor 12-Byte-Stub `placeholder`).
- `donegate-check.sh`: ausfuehrbar, `--template` liefert die Vorlage, Preflight laeuft.
- `kpt-deliver.sh`: ausfuehrbar, waehlt das kanonische Remote korrekt.

Nachweis:

```bash
bash /workspace/.hermes/scripts/donegate-check.sh t_57b817ba --no-code "<Begruendung>"
# -> PREFLIGHT: OK
```

## 5. Korrekte Worktree-Erstellung

### Grundregel
Arbeit gehoert **ausschliesslich** in einen eigenen Worktree des kanonischen Repos.
Der Haupt-Checkout wird von der Staging-Pipeline per `reset --hard` zurueckgesetzt —
dort liegen gelassene Aenderungen oder Branches gehen verloren.

### Standardfall (kpt-Submodule)
```bash
git -C /workspace/Github/KijanPersonalTracker fetch upstream
git -C /workspace/Github/KijanPersonalTracker/<submodul> fetch upstream
git -C /workspace/Github/KijanPersonalTracker/<submodul> \
    worktree add .worktrees/<task-id> -b task/<task-id> upstream/dev
cd /workspace/Github/KijanPersonalTracker/<submodul>/.worktrees/<task-id>
```

Basis ist `<kanonisch_remote>/dev`, also fuer die meisten Submodule `upstream/dev`
(kijan007). `kpt-doc` und `kpt-website` nutzen laut `repos.json` `origin/dev`
(zeigt ebenfalls auf kijan007).

### kijan-hermes-shared
```bash
git -C /workspace/kijan-hermes-shared fetch push dev
git -C /workspace/kijan-hermes-shared \
    worktree add .worktrees/<task-id> -b task/<task-id> push/dev
```
`origin` zeigt auf `kijan/kijan-hermes-shared` (kein Schreibrecht), `push` auf den
Fork `kijan007-agent/kijan-hermes-shared` — geliefert wird ueber `push`.

### Regeln waehrend der Arbeit
- Im Haupt-Checkout **keinen** Branch wechseln, nichts liegen lassen.
- Fremde Aenderungen nicht anfassen, nicht committen, nicht zuruecksetzen
  (kein `reset --hard`, kein `checkout .`, kein `stash -u` auf fremde Pfade).
- Nur eigene Pfade committen: `git add <pfade>`, nie `git add -A`.
- Commit-Message mit Task-ID: `feat(x): Text [t_1234abcd]`.
- Ergebnis auf `origin/dev` (kanonisches Remote) liefern, Ergebnis-Datei
  unter `worklogs/<task-id>-worklog.md` ablegen.

### Worklog-Vorlage
```bash
bash /workspace/.hermes/scripts/donegate-check.sh --template <task-id> > <repo>/worklogs/<task-id>-worklog.md
```
Pflicht-Sektionen (Gate-Policy `kpt`):
`# Worklog — <task-id>`, `## Kontext`, `## Aktionen`,
`## Geaenderte / erstellte Dateien`, `## Tests / Verifikation`, `## Dev-Integration`.

### Lieferung
```bash
bash /workspace/.hermes/scripts/kpt-deliver.sh <task-id> <repo>
```
Rebased auf `<kanonisch_remote>/dev`, pusht nach `dev` und `task/<task-id>`,
schliesst mit `donegate-check.sh` ab.

## 6. Bekannte Restbefunde (nicht in diesem Task behoben)

1. **Config-Repo-Divergenz**: `/workspace/.hermes` (Repo `hermes-config-kpt`) hat lokal
   6 Commits vor `origin/dev` und 19 Commits dahinter (`rev-list --left-right --count`
   → `6  19`). `repos.json`, `scripts/donegate-check.sh`, `scripts/kpt-deliver.sh` und
   `scripts/worker-env.sh` sind lokal **untracked** (`??`), in `origin/dev` aber tracked.
   Ursache: der Working Tree des Config-Repos wurde zurueckgesetzt, ohne dass die
   Dateien wieder in den Index aufgenommen wurden. Wer auf `origin/dev` arbeitet,
   erhaelt diese Dateien; wer im lokalen Checkout arbeitet, nicht.
2. **`worker-env.sh` wird nicht geladen**: `shell_init_files: []` in
   `profiles/devops/config.yaml`, und es gibt keine `.bashrc` im Profil-Home.
   `GIT_CEILING_DIRECTORIES=/workspace/.hermes/kanban/workspaces` und
   `GIT_TERMINAL_PROMPT=0` sind damit in Worker-Shells **nicht** gesetzt.
3. **DEV_VERIFY-Kette (9 Tasks)**: `/workspace/.hermes/dev-status/latest.json` meldet
   `state=fail`, `sha=7cde31a3`, `note=restore_dev.sh fehlgeschlagen (Prod-Dump konnte
   nicht in die Dev-DB geladen werden)`. `restore_dev.sh` liegt nicht im Container —
   der Restore-Zyklus laeuft host-seitig. Diese Tasks bleiben bis zur Host-Reparatur
   blockiert.
4. **Team-Klaerungen `t_57b817ba` / `t_032c251f`**: beide mit `NEEDS_USER_DECISION`
   blockiert, weil das Done-Gate als 12-Byte-Stub defekt war. Die Ursache ist behoben
   (Gate-Preflight `PREFLIGHT: OK`), aber die Karten tragen weiterhin ein
   `NEEDS_USER_DECISION`-Praefix — `autounblock.py` klassifiziert sie als `human`
   und entblockt sie **nicht** automatisch. Entblocken muss ein Mensch ausloesen.
