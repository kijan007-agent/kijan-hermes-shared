# Commit-to-Task Mapping Pattern

When auditing task status, map git commits to TASKS.md tasks by tracing commit history against documented task dates.

## Pattern

### 1. Find last TASKS.md update date
```bash
git log --oneline --follow --format="%ci" -- kpt-doc/_tasks/TASKS.md | head -1
```

### 2. Count commits since that date
```bash
git log --oneline --since="<TASKS.md update date>" -- kpt-app-ciq/source/ | wc -l
```
If >10 commits → TASKS.md is stale, verify each claim individually.

### 3. Trace specific feature commits
```bash
# For each claimed feature, find the commit that implemented it
git log --oneline --all -- source/EnergyScreen.mc | head -10
git log --oneline --all -- source/DeltaInputScreen.mc | head -10
```

### 4. Check submodule divergence
```bash
# Parent repo submodule pointer
git ls-tree hermes kpt-app-ciq

# Submodule HEAD
cd kpt-app-ciq && git rev-parse HEAD

# Submodule remote branch
git show origin/feature:source/EnergyScreen.mc | wc -l
```

### 5. Classification Matrix
| Pattern | Detection | Classification |
|---------|-----------|----------------|
| Worklog gap | `ls worklogs` vs `git log --since` | "WORKLOG GAP — N days stale" |
| File never existed | `find` + `git log -S` | "NEVER_CREATED" |
| Full→Simplified | `git merge-base --is-ancestor` | "Replaced (N→M lines)" |
| Stale TASKS.md | Commits since TASKS.md > 10 | "Unreliable — verify individually" |
| Submodule stale | `git ls-tree` ≠ submodule HEAD | "Submodule pointer stale" |
| Worklog empty dir | `ls worklogs` = empty/missing | "No worklogs maintained" |

## Session Example (2026-06-08)
- TASKS.md last updated: May 8 (30+ days ago)
- Commits since May 8: 30+ on hermes branch
- EnergyScreen: 122 lines (not 493 as claimed)
- DeltaInputScreen: NEVER_CREATED
- Worklogs: last entry May 8 (30+ days stale)
- kpt-app-ciq submodule HEAD: 174996a (dev branch)
- kpt-backend: c74006f (pacing dashboard fixes)
- Result: 2 of 6 tasks verified done, 2 not implemented, 2 stale docs
