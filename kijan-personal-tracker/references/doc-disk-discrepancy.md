# DOC/DISK Discrepancy Pattern — KijanPersonalTracker

## Problem
TASKS.md claims tasks are "COMPLETED ✅" but actual `.mc` source files in the working tree
do not reflect the described implementation. This happens when:
- Code was written in TASKS.md but never committed to a working tree
- Feature branch source was documented but the bare submodule has no working tree
- prod-hotfix working tree still has old versions of files

## Known Discrepancies (2026-05-10 audit)

| Task | TASKS.md Claims | Actual Disk State |
|------|----------------|-------------------|
| TASK-020 EnergyScreen | 493 lines, gradient chart, 24h timeline | 125 lines, basic display only |
| TASK-021 DeltaInputScreen | 417 lines, dual mode | File does not exist in any working tree |
| TASK-100 Overlay stacking | COMPLETED | ScreenFlowController.mc does not exist |
| TASK-101 Transition validation | COMPLETED | Depends on non-existent ScreenFlowController |
| TASK-102 Session sync | COMPLETED | ActivitySession model not found on disk |

## Resolution
- Tasks documented as "COMPLETED" are documented-only — code may need to be written/committed
- Always verify with: `wc -l <file>` and grep for key patterns
- Report as: "COMPLETED in TASKS.md but not verifiable on disk"
- Action: Write the actual code to prod-hotfix working tree, then commit

## Status
- First discovered: 2026-05-10
- Affected branch: feature (kpt-app-ciq bare submodule)
- Resolution path: Port documented designs to actual .mc files in prod-hotfix
