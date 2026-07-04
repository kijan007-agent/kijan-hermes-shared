# Dev Branch vs Task Tracker Divergence

## Pattern
Code on the `dev` (or `feature`) branch advances independently of TASKS.md. TASKS.md becomes stale when:
1. Dev branch has >10 commits beyond the last TASKS.md update date
2. Tasks are implemented under different names or merged into other branches
3. Documentation was updated to mark tasks "COMPLETED" before code was actually merged

## Evidence (2026-05-20)
- TASKS.md last updated: 2026-05-08
- Dev branch `fec8c9b`: 30+ commits past TASKS.md scope (phase-aware routing, feedback param fixes, layout switching, subclass refactoring)
- Task status claims in TASKS.md refer to:
  - Non-existent files (DeltaInputScreen never existed)
  - Stub files claimed as complete (EnergyScreen 80 lines vs claimed 493)
  - Tasks with zero corresponding commits (TASK-105 through TASK-109)

## Detection Protocol
1. `git log --oneline -1 --format="%h %ci" kpt-app-ciq/` — get latest dev commit date
2. Compare to TASKS.md "Updated:" date
3. If delta > 5 days: TASKS.md status is unreliable
4. `git log --oneline kpt-app-ciq/...HEAD -- kpt-doc/_tasks/TASKS.md` — check last TASKS.md update commit
5. `git log --oneline <last-task-update>..HEAD -- kpt-app-ciq/source/` — count commits touching source since TASKS.md update
6. If >10 source commits: task tracker is stale, verify each task claim against actual code

## Resolution
- When dev branch diverges >10 commits from TASKS.md: audit each task claim individually
- Never assume TASKS.md is authoritative when delta > 5 days
- Update TASKS.md only after verifying code state matches claims
- Document known divergent tasks in this file when new patterns emerge
