# Cron Status Audit Procedure

Use when a cron job or scheduled task needs to report status on KijanPersonalTracker work.

## Procedure

1. **Locate project**: `execute_code` workspace scan for KijanPersonalTracker dirs
2. **Read TASKS.md** (`kpt-doc/_tasks/TASKS.md`) — authoritative task status
3. **Read worklogs** (`kpt-doc/_worklogs/`) — check `WORKLOG.md` + latest dated `.md`
4. **Verify file existence**: `find /workspace/Github/KijanPersonalTracker-hermes -name 'FileName.mc'` — if not found, feature was removed/disabled
5. **Check COMPLETE_SUMMARY.md** for DISABLED implementations
6. **Check git HEAD** for latest commit

## Output Format

Per task: `✅/⏳/❌ TASK-{N}: [one-line summary] — [file ref or caveat]`

Then: Remaining items table + branch divergence table.

## Critical Caveat

TASKS.md may claim COMPLETED but files may not exist (EnergyScreen.mc, DeltaInputScreen.mc). Never assume doc = code. Cross-check every claim against disk.

## 2026-05-12 Update

- Feature branch at `/data/Github/KijanPersonalTracker-feature/` does NOT exist.
- Feature branch data is in the hermes monorepo packed-refs.
- Worklogs last written date is stale — always check git log.
