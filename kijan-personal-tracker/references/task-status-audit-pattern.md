# Task Status Audit Pattern for Kijan Personal Tracker

## Problem
KPT uses TASKS.md as a master task list, but actual code state in feature branch
may diverge from TASKS.md documentation. The feature branch lives in a bare git
submodule with no working tree.

## Audit Procedure
1. Read TASKS.md from `kpt-doc/_tasks/` (submodule IS checked out)
2. Read individual TASK-NNN.md files if they exist
3. Read source files from `prod-hotfix/kpt-app-ciq/source/` (NOT kpt-app-ciq/source/)
4. Cross-reference TASKS.md status claims against actual file content
5. Flag any "COMPLETED" tasks where the actual file doesn't contain the described code
6. Report discrepancies — doc may be stale even when code was changed in a different repo copy

## Key Pitfall
- **Path resolution**: The feature branch path `/data/Github/KijanPersonalTracker-feature/` and
  `/workspace/Github/KijanPersonalTracker-feature/` DO NOT EXIST. Always use:
  - `kpt-doc/_tasks/` from `/workspace/Github/KijanPersonalTracker/kpt-doc/_tasks/`
  - MC source from `/workspace/Github/KijanPersonalTracker-prod-hotfix/kpt-app-ciq/source/`
- TASKS.md can claim "COMPLETED ✅" but the actual MC file in the working tree may be the
old version. Always verify by reading the file line count and key content patterns.
EnergyScreen.mc example: TASKS.md says 493 lines, actual working tree has 125 lines.

## Files to Check
- TASKS.md: master task list with priorities and status
- TASK-NNN_*.md: individual task specs (may not exist for all)
- EnergyScreen.mc: chart redesign target
- DeltaInputScreen.mc: quick-input UX target  
- ScreenFlowController.mc: overlay stacking (if exists as standalone file)
- TASK-107 through TASK-109: pending tasks
- WORKLOG.md + daily logs: last known state per date

## Cron-Friendly
This pattern is designed for unscheduled cron audits where git commands are unavailable
and the sandbox is read-only.
