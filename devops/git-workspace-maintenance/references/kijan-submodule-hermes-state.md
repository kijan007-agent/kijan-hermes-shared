# KijanPersonalTracker Hermes Branch — Submodule State (2026-05-14)

## kpt-app-ciq Submodule
- **Parent ref on hermes**: `9a7fe42846bf6fb97e8b1243832d5a1d99a65a33` (commit `160000` in parent)
- **kpt-app-ciq HEAD**: `9a7fe42` (detached)
- **feature branch**: same as HEAD (`9a7fe42` = merge of feature into hermes)
- **Contains**: EnergyScreen.mc (123 lines, pre-redesign), ScreenFlowController.mc (691 lines), no DeltaInputScreen.mc
- **Key finding**: DeltaInputScreen (417 lines) was added in `5826510` then DELETED before merge to feature
- **Key finding**: EnergyScreen chart redesign (493 lines per TASKS.md) was never merged — code is 123 lines

## kpt-doc Submodule
- **Ref**: `ab16024` (merged 2026-04-19, stale — last updated 2026-05-07 in working tree only)
- **Contains**: TASKS.md (256 lines), worklogs/, FSM docs

## kpt-backend Submodule
- **Ref**: `7dea9ed` (stale)

## kpt-admin Submodule
- **Ref**: `f6f25e0` (stale)

## Key Divergence
TASKS.md documents EnergyScreen 493-line redesign and DeltaInputScreen 417-line feature as COMPLETED.
Actual kpt-app-ciq code does NOT contain either. TASKS.md = intended state, not actual state.
