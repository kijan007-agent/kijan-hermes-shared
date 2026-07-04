# Post-Wipe Extraction Fallback (2026-06-07)

## Context
After the 2026-06-07 complete wipe of both KijanPersonalTracker repos (`KijanPersonalTracker-feature` and `KijanPersonalTracker-hermes`) at BOTH `/data/Github/` AND `/workspace/Github/`, the only surviving Connect IQ code is in `/tmp/kpt-extract/source/`.

## Detection Pattern
When ALL KijanPersonalTracker paths are empty:
1. `/data/Github/KijanPersonalTracker-*` → empty (cron sandbox)
2. `/workspace/Github/KijanPersonalTracker-*` → empty (workspace)
3. → Check `/tmp/kpt-extract/source/*.mc` for extraction snapshot
4. → Report "CODEBASE WIPE — only extraction snapshot available"

## What /tmp/kpt-extract/source/ Contains
- Flat `.mc` files (no directory structure)
- 171+ files from prior Connect IQ extraction
- Read-only snapshot — no git history
- Does NOT contain: `DeltaInputScreen.mc`, `TASKS.md`, worklogs, backend code

## Cron Job Impact
- Any cron task referencing TASKS.md, `_worklogs/`, or `kpt-app-ciq/` paths will fail
- Status reports must note "repos wiped — extraction snapshot only"
- Work cannot proceed until repos are restored from backup or user-provided code
