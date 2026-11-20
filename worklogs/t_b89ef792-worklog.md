# Worklog — t_b89ef792

## Kontext

Die deployed gate.py (/etc/hermes/done-gate/gate.py) ist aelter als origin/dev und
fehlt der B1-Guard (try/except subprocess.TimeoutExpired im `git()`-Wrapper). QA-Befund
B1 t_40a8c20d ist in origin/dev dokumentiert und gefixt, aber das /etc-Root-FS ist
read-only (ocfs2-Mount des Hosts); ein Container-Rollout ist nicht moeglich.

Projekte-Hub: http://projekte.kijan.ch/ideas/726 (Haupt-Review t_40a8c20d)

Task: Kann nicht selbst rollen, dokumentiert den Befund und den Stand.

## Aktionen

1. **Workspace pruefen** — scratch dir hat `ha-clone/` mit einem Klon von
   kijan007/hermes-admin. Worktree auf kijan-hermes-shared (push/dev, Branch
   task/t_b89ef792) angelegt unter `/workspace/.worktrees/t_b89ef792`.

2. **MD5-Vergleich gate.py**:
   ```
   md5sum ha-clone/done-gate/managed/done-gate/gate.py  -> 9afeb4f3782cadc1dce8ab85d36ac3ee
   md5sum /etc/hermes/done-gate/gate.py                 -> 3a8e6ff0334370baee0f7d97727dbf6e
   ```
   Deployed != origin/dev. policy.json ist identisch (1505 B, missing final newline
   only — irrelevant).

3. **B1-Defekt reproduziert** — Fake-git gebaut (sleep 40), jedes `git`-Call haengt:
   - **deployed gate.py**: rc=1, Traceback=True, keine JSON-decision → EXTERNER EXIT,
     ausserhalb 0/2-Vertrag (genau B1)
   - **origin/dev gate.py**: rc=2, Traceback=False, decision=block mit lesbarer Meldung
   ```
   PATH=fake_git:$PATH python3 gate.py < payload
   deployed:  rc=1  traceback=True   decision=[]
   origin/dev: rc=2  traceback=False decision={"decision":"block",...}
   ```
   Defekt-Kategorie: in `git()` (Zeile 43) fehlt try/except TimeoutExpired.
   In main() (Zeile 680) wird TimeoutExpired gefangen — aber NUR wenn der Call bis
   dorthin durchkommt. Ohne den `git()`-Wrapper-Guard propagiert die Exception aus
   `check_repo()` und beendet mit rc=1/Traceback statt 2/block.

4. **Deployed --help Test**:
   ```
   python3 /etc/hermes/done-gate/gate.py --help < /dev/null
   exit=0  (keine Ausgabe ausser shim-Log, kein Traceback)
   ```

5. **B2 (has_task_commit Timeout 20s->60s, Commit 4765fcd)**: ebenfalls nur in
   origin/dev, nicht in deployed. Wurde nicht separat getestet (B1 ist der
   kritischere Befund).

6. **Rollout-Option geprueft**: /etc/hermes ist read-only (ocfs2, uid=1000),
   kein Container-Schreibzugriff. Provisioning-Quelle: hermes-admin/done-gate,
   Mechanismus: done-gate/install.py. Der Fix muss hostseitig eingespielt werden.

7. **Dokumentation in Kommentare an t_968778c2 und t_704587ea** (wird nach dem
   Commit erledigt via kanban_comment).

## Geaenderte / erstellte Dateien

- `/workspace/.worktrees/t_b89ef792/worklogs/t_b89ef792-worklog.md` — Worklog (dieses Dokument)
- `/workspace/.worktrees/t_b89ef792/tmp/fuzzy_run.py` — Testskript Fake-git
- `/workspace/.worktrees/t_b89ef792/tmp/dev_fakegit_out.txt` — Verifikation origin/dev
- `/workspace/.worktrees/t_b89ef792/tmp/deployed_fakegit_out.txt` — Verifikation deployed
- `/tmp/s1` — Test-Repo (Scratch, kein Remote)

## Tests / Verifikation

### B1-Defektnachweis

```bash
# 1. Fake-git das haengt (timeout 1s):
mkdir -p fake_git && printf '#!/bin/sh\nsleep 40\n' > fake_git/git && chmod +x fake_git/git

# 2. Testrepo mit Task-Commit:
cd /tmp/s1  # (git init, commit mit [t_smoketest])
git log --oneline -1
# 203f11f feat: test [t_smoketest]

# 3. Test payload:
cat > /tmp/payload.json <<'EOF'
{"tool_name":"kanban_complete","cwd":"/tmp/s1",
 "tool_input":{"task_id":"t_smoketest","summary":"t",
               "metadata":{"repos":["/tmp/s1"],"commits":["203f11f"]}}}
EOF

# 4. DEPLOYED (ohne B1-Guard) — erwartet: rc=1, Traceback
PATH=fake_git:$PATH timeout 400 python3 /etc/hermes/done-gate/gate.py < /tmp/payload.json
# Ergebnis: rc=1, Traceback=True, keine decision → B1 BESTAETIGT

# 5. ORIGIN/DEV (mit B1-Guard) — erwartet: rc=2, block, kein Traceback
git -C ha-clone show origin/dev:done-gate/managed/done-gate/gate.py > /tmp/gate_dev.py
PATH=fake_git:$PATH timeout 400 python3 /tmp/gate_dev.py < /tmp/payload.json
# Ergebnis: rc=2, decision=block, kein Traceback → B1-FIX FUNKTIONIERT
```

### md5sum gate.py

```bash
md5sum /workspace/.hermes/kanban/workspaces/t_b89ef792/ha-clone/done-gate/managed/done-gate/gate.py
# 9afeb4f3782cadc1dce8ab85d36ac3ee  (origin/dev)

md5sum /etc/hermes/done-gate/gate.py
# 3a8e6ff0334370baee0f7d97727dbf6e  (deployed, aelter)

# => nicht byte-identisch, Differenz: 52 Zeilen (B1-Guard + B2 + Hints-Erweiterung)
```

### python3 /etc/hermes/done-gate/gate.py --help

```bash
python3 /etc/hermes/done-gate/gate.py --help < /dev/null; echo "exit=$?"
# exit=0  (kein Traceback bei --help, gate.py laeuft ansonsten ohne Defekt)
```

### Diff deployed vs origin/dev (wesentliche Zeilen)

```bash
diff /etc/hermes/done-gate/gate.py <(git -C ha-clone show origin/dev:done-gate/managed/done-gate/gate.py)
# Zeile 43 deployed:  r = subprocess.run(["git", "-C", ...], timeout=timeout)
# Zeile 43 origin/dev: try: r=subprocess.run(...); except TimeoutExpired: return 124,...
# Zeile 147+ deployed: keine has_task_commit-Timeout-Erweiterung (B2)
# Zeile 109+ deployed: keine erweiterten Repair-Hints
```

## Dev-Integration

- Commit: `9472dd5ee4540088b5a1fb0645b1009b3ea1971c` auf `push/dev` (kijan-hermes-shared)
  — Worktree-Branch `task/t_b89ef792` = identischer Stand zu `push/dev`.
- Worklog: `worklogs/t_b89ef792-worklog.md` committed auf `push/dev`.
- Rollout der gate.py (B1-Guard + B2 + Hints): **HOST-SEITIG** erforderlich.
  Provisioning-Quelle: `kijan007/hermes-admin@dev/done-gate/managed/done-gate/gate.py`
  (md5: `9afeb4f3782cadc1dce8ab85d36ac3ee`).
  Mechanismus: `hermes-admin/done-gate/install.py` — muss auf dem Host als
  root/hermes-Admin ausgefuehrt werden (da /etc/hermes read-only im Container).
- Kein eigenes Code-Commit auf origin/dev in diesem Task (kein Code aenderbar).
