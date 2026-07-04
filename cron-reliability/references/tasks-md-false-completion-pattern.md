# TASKS.md False Completion Pattern — KijanPersonalTracker

## Problem
TASKS.md in KijanPersonalTracker claims tasks as "COMPLETED ✅" when actual `.mc` files
were never committed. Cron sessions interrupted mid-task or work done in prior session's
working tree that was not persisted.

## Detection Protocol (ALL steps, ordered by priority)
1. **Working tree**: `find /workspace/Github/KijanPersonalTracker-hermes -name 'FileName.mc'`
2. **Git history**: `git -C kpt-app-ciq log --oneline --all -- source/FileName.mc`
3. **Remote branch**: `git -C kpt-app-ciq show origin/feature:source/FileName.mc`
4. **Session history**: `session_search(query="FileName mc file work done")`

## Reality Check Priority
Working tree > git history > session history > TASKS.md claims

## Known False Completions
| File | TASKS.md | Actual | Evidence |
|------|----------|--------|----------|
| EnergyScreen chart | COMPLETED ✅, 493 lines | 123-line stub | `find` returns stub, `origin/feature` also stub |
| DeltaInputScreen.mc | COMPLETED ✅, 417 lines | Never existed | No `find` match, no git log |
| ScreenFlowController overlay | COMPLETED ✅ | 973 lines | Present, implemented |
| Transition validation | COMPLETED ✅ | Partial | `go()` path missing guard |
| ActivitySession sync | COMPLETED ✅ | 44 lines | Present, implemented |

## Prevention
- Commit per task, not per session
- After any modification: `git status` immediately
- On cron completion: `git diff --stat` to verify staged changes match expected work
- Report "claimed" vs "verified" — never "completed" without disk verification
