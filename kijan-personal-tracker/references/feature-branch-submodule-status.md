# Feature Branch Submodule Status

**Updated:** 2026-05-11 (audit)

## Current State

- **Feature branch repo:** `/workspace/Github/KijanPersonalTracker-feature/` — EXISTS with full working tree
- **kpt-app-ciq submodule:** Bare submodule, non-functional remote. Code lives in prod-hotfix working copy.
- **Working source:** `/workspace/Github/KijanPersonalTracker-prod-hotfix/kpt-app-ciq/source/` (170 .mc files)
- **Feature branch working tree:** `/workspace/Github/KijanPersonalTracker-feature/kpt-app-ciq/source/` (170 .mc files)

## TASKS.md vs Disk Discrepancies (Updated)

| Task | TASKS.md | Disk (prod-hotfix) | Disk (feature branch) |
|------|----------|-------------------|----------------------|
| TASK-020 EnergyScreen | 493 lines, chart redesign ✅ | EnergyDrawable.mc exists (151 lines) | EnergyScreen.mc DOES NOT EXIST |
| TASK-021 DeltaInputScreen | 417 lines, dual mode ✅ | DOES NOT EXIST | DOES NOT EXIST |
| TASK-100 Overlay stacking | COMPLETED ✅ | ScreenFlowController.mc has fix | ScreenFlowController.mc has fix |
| TASK-101 Transition validation | COMPLETED ✅ | ScreenFlowController.mc has fix | ScreenFlowController.mc has fix |
| TASK-102 Session sync | COMPLETED ✅ | ActivitySession.mc exists | ActivitySession.mc exists |

## Critical Finding: Disabled Implementations

EnergyScreen.mc and DeltaInputScreen.mc were **removed as broken** from the codebase:
- `// DISABLED: DeltaInputScreen and EnergyScreen broken implementations removed` in ScreenFlowController.mc
- `createEnergyScreen()` returns `null` in UIViewFactory.mc
- Neither file exists in git history (never committed)
- Supporting infrastructure (EnergyDrawable, spoon PNGs) remains in place

See `references/energy-screen-removed.md` for full audit details.
