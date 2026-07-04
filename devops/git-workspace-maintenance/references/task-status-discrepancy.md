# Task Status Discrepancy Detection

## Problem
Documentation (TASKS.md, worklogs) claims tasks are "completed" but source files are missing from disk. Common in cron/status-audit sessions when source repos have bare clones or stale checkouts.

## Detection Pattern
1. **Read TASKS.md** — collect claimed-completed tasks with file references
2. **For each claimed file**: `test -f <path>` or `ls <path>` — verify existence
3. **If source dir missing**: Check if repo is bare clone (`.git/objects/pack/` present but no source files)
4. **Cross-reference with prod-hotfix**: Compare against known-good branch to identify what's actually present vs just documented
5. **Report with severity levels**:
   - ✅ Documented AND verified on disk
   - ⚠️ Documented but unverifiable (no source dir)
   - ❌ Not documented, not present

## KijanPersonalTracker Specifics
- `kpt-app-ciq/` is bare — no `source/` directory exists on disk
- `kpt-common-barrels-ciq/source/` and `kpt-datafield-ciq/source/` have working trees
- TASKS.md references `/data/Github/` paths (stale) — actual base is `/workspace/Github/`
- prod-hotfix branch has full working tree for comparison
- EnergyScreen.mc documented as 493 lines (feature) vs 125 lines (prod-hotfix) — feature version lost
- DeltaInputScreen.mc documented as 417 lines — never existed on disk

## When This Happens
- Cron jobs run status checks against repos that were cloned bare/partially
- Previous sessions documented implementations that were never committed to working tree
- Feature branch diverged and source was never checked out after divergence
- **Confirmed pattern (May 11 – June 3):** `KijanPersonalTracker-feature` has been empty for 23+ consecutive cron sessions. The repo exists on disk but has zero commits and an unreachable remote. Source code has never persisted to the container.

## Prevention
- After cloning a repo, always verify: `ls <repo>/source/ | head` for Monkey C projects
- Add `verify_working_tree` step to cron task checklists before reporting status
- Use prod-hotfix as ground truth for "what exists" when feature source is missing
