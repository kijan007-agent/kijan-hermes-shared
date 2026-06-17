# Post-Wipe Extraction Location (2026-06-07)

## Context
After the 2026-06-07 complete wipe of both `KijanPersonalTracker-feature` and `KijanPersonalTracker-hermes` repos (zero commits, zero remotes), the only surviving Connect IQ source code is in `/tmp/kpt-extract/source/`.

## What's Available
- 171+ `.mc` files extracted from a prior codebase extraction
- Includes: `EnergyScreen.mc` (123 lines, basic stub), `ScreenFlowController.mc` (691 lines), `EnergyDrawable.mc` (151 lines), `ActivitySession.mc`, `ActivitySessionContext.mc`, and many others
- Does NOT include: `DeltaInputScreen.mc` (was never created), `TASKS.md`, `_worklogs/`, `kpt-app-ciq/` directory structure

## What's NOT Available
- No git history, no remotes, no working tree
- No `kpt-app-ciq/` directory — files are flat in `source/`
- No backend code, no migration files
- No TASKS.md or worklog documentation

## Usage
When repos are wiped and you need to inspect Connect IQ code:
1. Check `/tmp/kpt-extract/source/` first for `.mc` files
2. These are snapshots — not version-controlled — treat as read-only reference
3. Cross-reference with `/workspace/Github/KijanPersonalTracker-prod-hotfix/` if available
4. Report "EXTRACTION SNAPSHOT — no git history" when using these files

## File List (confirmed 2026-06-07)
EnergyScreen.mc, ScreenFlowController.mc, EnergyDrawable.mc, ActivitySession.mc, ActivitySessionContext.mc, ActivityFsm.mc, StateStore.mc, BackendCommManager.mc, SyncNetworkManager.mc, ScreenFlowConfig.mc, ScreenManager.mc, UIViewFactory.mc, KijanActivityTrackerApp.mc, KijanPersonalTrackerView.mc, KijanPersonalTrackerDelegate.mc, InitScreens.mc, Constants.mc, AppGlobals.mc, and 150+ more.
