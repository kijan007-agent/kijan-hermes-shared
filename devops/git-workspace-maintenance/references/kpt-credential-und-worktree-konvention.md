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

`credential.helper` war über die Submodule hinweg uneinheitlich. Ursprüngliche
Abweichungen (t_33e8debc, 2026-11-02): `kpt-app-ciq` auf `store --file=/tmp/git-cred`
(ephemer), `kpt-website-pre-release` auf den Profil-lokalen Store, sechs Repos auf
`store --file /workspace/.hermes/profiles/web-development/cache/scratch/.gh-creds`
(Scratch-Cache eines **fremden** Profils — beim Aufräumen dieses Caches bricht der
Push-Zugang weg).

### Ist-Zustand nach Vereinheitlichung (Nachweis t_05100867, 2026-11-19)

Verifikation je Repo mit `git -C <repo> config --get-all credential.helper`.
Sollwert: `store` + `store --file /workspace/.git-credentials` (global aus
`/workspace/.hermes/profiles/devops/home/.gitconfig`).

| Repo | credential.helper (Ist 2026-11-19) | konform |
|---|---|---|
| KijanPersonalTracker (main) | `store`, `store --file /workspace/.git-credentials` | ja |
| kpt-admin | dito | ja |
| kpt-app-ciq | dito | ja |
| kpt-backend | dito | ja |
| kpt-common-barrels-ciq | dito | ja |
| kpt-datafield-ciq | dito | ja |
| kpt-doc | dito | ja |
| kpt-symptoms-app | dito | ja |
| kpt-watchface-ciq | dito (lokaler Fremd-Eintrag `…/profiles/web-development/cache/scratch/.gh-creds` am 2026-11-19 entfernt) | ja |
| kpt-website | dito | ja |
| kpt-website-pre-release | dito | ja |

Korrektur t_05100867: `kpt-watchface-ciq` hatte als einziges Repo noch einen
**lokalen** Eintrag `store --file /workspace/.hermes/profiles/web-development/cache/scratch/.gh-creds`
in seiner `.git/config` (global war bereits korrekt). Entfernt mit
`git -C kpt-watchface-ciq config --local --unset-all credential.helper`;
danach greift wieder der globale kanonische Store. Damit zeigen **alle 11 Repos**
(main + 10 Submodule mit `.git`) auf exakt einen kanonischen Store.

Push-Probe je Repo (`git push --dry-run <kanonisch_remote> HEAD:refs/heads/task/t_05100867`):
11/11 Exit 0, kein `unable to get credential storage lock`. Hinweis: `kpt-watchface-ciq`
hat nur ein `origin`-Remote (kein `upstream`) — kanonisches Remote ist dort `origin`.

Alle Stores enthalten Eintraege fuer `https://github.com`:
- `//x-access-token:***>` (App-Token)
- `//kijan007:<token>` (PAT)

Stand 2026-11-19: `/workspace/.git-credentials` (75 B, 600, uid 1000) enthält den
github.com-Eintrag; `/workspace/.hermes/home/.git-credentials` (144 B, 666) enthält
beide Varianten. Die Dateien sind **nicht mehr byte-identisch** (frühere Annahme im
Review überholt); massgeblich ist, dass der von `credential.helper` referenzierte
kanonische Store funktioniert — nachgewiesen durch die 11/11 erfolgreichen Push-Proben.

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

**Push-Berechtigung fuer `push` (Befund t_05100867, 2026-11-19):** der kanonische
Store `/workspace/.git-credentials` enthaelt nur ein `x-access-token` fuer `kijan007`;
das liefert auf `kijan007-agent/kijan-hermes-shared` `403 Permission denied`.
Der Token fuer `kijan007-agent` liegt in `~/.git-credentials` (der globale
`store`-Helper liest sie). Loesung — einmalig pro Clone, kein Repo-Commit:

```bash
git -C /workspace/kijan-hermes-shared config credential.username kijan007-agent
```

Nach dem Setzen liefert `git push push HEAD:dev` Exit 0. **Nicht** in die kpt-Submodule
kopieren: dort bleibt es bei `store` + `store --file /workspace/.git-credentials` (AK 1).

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

## 6. Restbefunde (Stand 2026-11-19)

1. **Config-Repo-Divergenz — ERLEDIGT (t_05100867, 2026-11-19)**.
   Der Config-Repo-Checkout `/workspace/.hermes` ist selbst kein Git-Arbeitsbaum mehr
   (`git -C /workspace/.hermes rev-parse` → `fatal: not a git repository`);
   gepflegt wird er ueber den Clone `/workspace/.worktrees/t_05100867-cfg`
   (Remote `origin` = `kijan007/hermes-config-kpt`, Branch `dev`).
   Vorheriger Stand: `repos.json` war untracked lokal, `scripts/donegate-check.sh`,
   `scripts/kpt-deliver.sh` und `scripts/worker-env.sh` waren im Repo **gar nicht**
   enthalten (`git ls-files scripts` listete sie nicht auf).
   Bereinigung: die drei Gate-Skripte aus `/workspace/.hermes/scripts/` 1:1 in den
   Config-Repo-Clone uebernommen und committed
   (`chore(config): Done-Gate-Skripte ... ins Config-Repo aufnehmen [t_05100867]`),
   Push nach `origin/dev` und `origin/task/t_05100867`.
   Ergebnis: `repos.json` ist tracked (`git ls-files repos.json` → `repos.json`),
   alle drei Skripte sind tracked, Divergenz `origin/dev...HEAD` = `0  0`.
   `donegate-check.sh` und `kpt-deliver.sh` bleiben zusaetzlich am Runtime-Pfad
   `/workspace/.hermes/scripts/` ausfuehrbar (identischer Inhalt, md5 geprueft).
2. **`worker-env.sh` — Review-Befund ist in dieser Umgebung NICHT REPRODUZIERBAR
   (t_05100867, 2026-11-19)**.
   Der Review-Befund lautete: "Datei existiert lokal nicht / wird nicht geladen".
   Nachmessung: die Datei **existiert** und ist korrekt:
   `/workspace/.hermes/scripts/worker-env.sh` (5 Zeilen) mit
   `export GIT_CEILING_DIRECTORIES=/workspace/.hermes/kanban/workspaces` und
   `export GIT_TERMINAL_PROMPT=0`; sie ist seit t_05100867 zudem **tracked** im
   Config-Repo (siehe Befund 1). Damit ist der Kern des Review-Befunds widerlegt.
   Offen bleibt nur die *Ladung*: `terminal.shell_init_files: []` steht aktuell in
   **allen** 30 Profil-Configs (`grep -rn shell_init_files profiles/*/config.yaml`)
   und in der Root-`config.yaml` gibt es keinen `shell_init`-Schluessel. Die
   Datei wird also nicht ueber `shell_init_files` eingebunden; die Review-Aussage
   "Datei fehlt" bleibt dennoch unzutreffend.
   **Konsequenz fuer Worker (verbindlich):** `GIT_CEILING_DIRECTORIES` und
   `GIT_TERMINAL_PROMPT=0` nicht voraussetzen. Deshalb gilt weiterhin die Regel
   aus Abschnitt 5: Projektarbeit **immer** in einem expliziten Worktree des
   kanonischen Repos, nie im Hermes-Home, und Git-Befehle nie relativ aus dem
   Hermes-Home heraus starten.
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

## 7. Konvention: weitere Repos aufnehmen

Wenn ein neues kpt-Repo (oder ein neues Submodul) dazukommt, gilt diese Reihenfolge —
sie ist in einem Task mit Task-ID im Commit-Namen zu erledigen:

1. **Eintrag in `repos.json`** (Config-Repo `hermes-config-kpt`, Branch `dev`):
   ```json
   "<repo-name>": {
     "pfad": "<repo-name>",
     "push_remote": "upstream",
     "origin": "kijan007/<repo-name>",
     "upstream": "kijan007/<repo-name>",
     "ziel": "dev",
     "basis_branch": "dev",
     "kanonisch_remote": "upstream",
     "hinweis": "alles in kijan007 (Remote upstream)"
   }
   ```
   `kanonisch_remote` muss ein real existierender Remote des Repos sein; `ziel`
   und `basis_branch` sind `dev`.

2. **Credential-Helper auf den kanonischen Store vereinheitlichen**:
   ```bash
   git -C <repo> config --local --unset-all credential.helper   # Fremd-Eintraege raus
   git -C <repo> config --get-all credential.helper               # Ist-Anzeige
   ```
   Sollwert: `store` + `store --file /workspace/.git-credentials` (global aus
   `/workspace/.hermes/profiles/<profil>/home/.gitconfig`). **Kein** Pfad in ein
   Scratch-Verzeichnis eines fremden Profils (`…/profiles/*/cache/scratch/…`) —
   beim Aufraeumen des Scratch-Caches bricht sonst der Push-Zugang weg.

3. **Push-Probe** (kanonisches Remote, kein Lock-Fehler):
   ```bash
   git -C <repo> push --dry-run <kanonisch_remote> HEAD:refs/heads/task/probe-<task-id>
   ```
   Exit 0 und kein `unable to get credential storage lock` ist Pflicht. Fuer
   Repos ohne `upstream`-Remote (z. B. `kpt-watchface-ciq`) ist `origin` das
   kanonische Remote.

4. **Ist-Tabelle in Abschnitt 2 nachziehen**: neue Zeile mit Repo-Name,
   tatsaechlichem Helper-Wert und Datum des Nachweises; Fremd-Eintraege, die
   entfernt wurden, in der Fussnote der Tabelle benennen.

5. **Konvention aktualisieren und liefern**: Commit in
   `kijan-hermes-shared` (Remote `push`, Branch `dev`) mit Task-ID im Namen,
   dazu Worklog `worklogs/<task-id>-worklog.md` mit Befehl + Ergebnis je Schritt.
