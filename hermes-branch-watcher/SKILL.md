---
name: hermes-branch-watcher
description: "Branch safety gate — always verify and switch to hermes branch before any workspace action."
---

# hermes-branch-watcher

## PURPOSE
Bevor ANY commit, push, pull, oder workspace-modifizierende Aktion: sicherstellen, dass alle Repos im KijanPersonalTracker-Projekt auf dem `hermes` Branch arbeiten. Verhindert versehentliche commits auf `feature` oder anderen Branches.

## WHEN TO USE
- **BEVOR** auch nur EINE Datei gelesen oder geschrieben wird (IMMER erster Schritt)
- Vor JEDER `git commit` oder `git push`
- Vor jeder workspace-modifizierenden Aktion
- Wenn der User sagt "auf hermes wechseln" oder "branch wächter"
- Vor jeder Task-Ausführung
- **IMMER als allererster Schritt in jeder Session**, bevor code_read/write/edit

## WORKSPACE PATH
- Main: `/workspace/Github/KijanPersonalTracker-hermes`
- Submodule kpt-backend: `<main>/kpt-backend`
- Submodule kpt-app-ciq: `<main>/kpt-app-ciq`
- Feature branches: `/data/Github/KijanPersonalTracker-feature/` (only read — persistent empty repo since May 11)
- **NOTE:** `/data/Github/KijanPersonalTracker-feature` has been empty (zero commits, unreachable remote) across 6+ cron sessions (May 11 – June 3). Do not rely on it for source code verification.

## EXECUTION ORDER — ZWINGEND EINHALTEN

### CRITICAL: Empty Repo Detection
- **PITFALL:** Repos können leer sein (keine commits) — prüfen mit `git log --oneline` vor `git show` oder `git branch`
- **PITFALL:** `git status` zeigt "Untracked files" aber "No commits yet" → repo ist initialisiert aber leer
- **ABHILFE:** Immer zuerst `git log --oneline -1` prüfen, erst dann `git show`/`git branch` ausführen

### Phase 1: Branch-Wächter (BEVOR IRGENDWAS)
```python
# 1. Branch-Status prüfen
for repo in ["Main", "kpt-backend", "kpt-app-ciq"]:
    branch = git symbolic-ref --short HEAD <repo>
    
    # 2. Korrigieren falls nötig
    if branch != "hermes":
        git checkout hermes <repo>
        git reset --hard origin/hermes <repo>  # WARN: uncommitted changes lost!
    
    # 3. Bestätigen
    assert branch == "hermes"

# 4. Uncommitted changes auflisten
dirty_files = git status --short
if dirty_files:
    print(f"Dirty: {len(dirty_files)} files")
    for f in dirty_files:
        print(f"  {f}")
```

### Phase 2: Task-Ausführung
- Jetzt erst Dateien lesen/schreiben
- Jetzt erst Fixes anwenden

### Phase 3: Pre-Commit-Check
- Nochmal Branch-Status prüfen
- Sicherstellen, dass alles auf `hermes` ist
- Erst dann commiten

### Phase 4: Branch-Offset-Monitoring
- Commit-count delta: `git rev-list --count WORKING_TREE_HEAD..hermes`
- **Dual-origin measurement (NEU 2026-05-27):** Measure against BOTH `origin/dev` AND `origin/hermes`. kpt-backend pattern: `origin/dev..HEAD` (8 ahead) vs `origin/hermes..HEAD` (2 ahead) — both meaningful, both must be tracked.
- Siehe `references/branch-offset-monitoring.md` für Threshold-Tabelle
- > 100 commits = CRITICAL → TASKS.md komplett unbrauchbar (05-22: kpt-app-ciq 168→739 in ~7h!)
- > 50 commits = HIGH → TASKS.md stark veraltet, nur mit verification protocol verwenden
- > 10 commits = WARNING → TASKS.md wahrscheinlich veraltet
- Auch prüfen: `git rev-list --count origin/dev..dev` für unmerged commits in origin
- **Post-Sync Drift:** After origin/dev sync, drift resumes immediately (1→20, 1→14, 1→11). Sync waves are temporary.

## RULES
- **NIEMALS** auf `feature` arbeiten — das ist Jan's Branch
- Alle Fixes müssen auf `hermes`
- Vor Task-Ausführung IMMER Branch prüfen
- Bei Diskrepanz: sofort korrigieren, NICHT weiterarbeiten

## ERROR HANDLING
- Wenn `checkout` fehlschlägt: User warnen
- Wenn Merge-Konflikte: `merge --abort` + `reset --hard origin/hermes`
- Wenn Auth fehlt: User informieren, NICHT pushen

## Drift Direction Reversal (NEU 2026-06-09)
- When a submodule reports the SAME offset number between audits, it may be in the **opposite direction** (AHEAD → BEHIND or vice versa)
- Always check BOTH directions: `git rev-list --count origin/dev..HEAD` AND `git rev-list --count HEAD..origin/dev`
- A count of "13 AHEAD" vs "13 BEHIND" is a completely different situation — never report just the number
- See `references/drift-direction-reversal.md` for the full pattern
- **PITFALL:** Reporting only the count without direction causes false status assessments

## POST-TASK
Nach Abschluss:
1. Branch-Status nochmal prüfen
2. Alle auf `hermes` bestätigen
3. Dirty-Files auflisten
