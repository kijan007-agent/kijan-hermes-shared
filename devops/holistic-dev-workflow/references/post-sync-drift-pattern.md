# Post-Sync Drift Detection

> Discovered 2026-05-23: After origin/dev sync, submodules drift back up within hours. Sync-Waves are temporary, not permanent fixes.

## Pattern
After a batch sync of submodules to origin/dev:
- kpt-admin: 19→1 unmerged → later 1→20 (drift of 19)
- kpt-common-barrels-ciq: 13→1 → 1→14 (drift of 13)
- kpt-datafield-ciq: 10→1 → 1→11 (drift of 10)

## Detection
- Monitor submodules 2h AFTER sync — drift will appear
- Never mark a sync task as "erledigt" until verified 2h+ later
- The drift rate varies per repo (1-20 commits/hour observed)

## Mitigation
- Sync is a temporary stabilization, not a resolution
- Track drift accumulation rate per repo
- High-drift repos need active development attention, not just sync
- When drift > warning threshold, re-mark TASKS.md as stale
- **Post-Sync Drift Confirmed 2026-05-25:** kpt-backend synced origin/dev (0 unmerged) but has 2 unmerged on hermes (69f8d96 still on hermes). Sync masks drift but doesn't eliminate it — always check BOTH origin/dev AND origin/hermes after sync.
