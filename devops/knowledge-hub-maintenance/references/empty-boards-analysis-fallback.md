# Empty Boards Cross-Domain Analysis Fallback Pattern

**Created:** 2026-08-02  
**Trigger:** All Kanban product boards EMPTY (>0 days continuous) → no workflow data available for cross-product analysis.

## Problem
When all 4+ Kanban product boards are empty (confirmed state as of 2026-08-02, >95 days continuous), the standard cross-product analysis workflow yields zero insights. This is a chronic institutional gap that blocks Knowledge Hub updates.

## Solution: Fallback to Git Branch History
Even when Kanban boards are empty, **Git branch history** and **feature commits** provide rich source material for cross-domain pattern detection.

### Data Sources (in priority order)
1. **Active feature branches** — `git log --oneline HEAD..origin/main` or similar divergent branches show what's actively being developed
2. **Submodule states** — check if submodules (kpt-backend, kpt-app-ciq) are up-to-date relative to main
3. **Branch divergence deltas** — ahead/behind counts across products reveal parallel development patterns
4. **Commit message taxonomy** — classify recent commits by domain type (UI, backend, embedded, infra) → reveals cross-domain activity trends
5. **Repo existence/disappearance** — track whether repositories appear or vanish (prod-hotfix example from 2026-08-02)

### What This Fallback CAN Detect
- **Feature Branch Divergence Pattern:** When a feature branch diverges deeply with structural changes (e.g., KijanPersonalTracker-feature `wf-layout-final` Watchface rework), monitor for main integration requirements
- **Repo Disappearance Pattern:** Repositories vanishing over time (e.g., prod-hotfix) → flag as anomaly vs expected cleanup
- **Submodule Sync Status:** Track whether submodules are catching up or falling behind their upstreams
- **Cross-Product Activity Correlation:** If multiple product branches show similar patterns on the same day, infer coordinated effort despite empty boards

### What This Fallback CANNOT Detect
- Actual workflow bottlenecks (no handoff data)
- Process efficiency metrics (no timestamps/counts)
- Real deliverable progress (commits != accepted work)
- Team workload distribution (one committer can mask imbalance)

## Implementation Steps
1. Verify all board task counts are 0: `python3 -c "import sqlite3; ..."` per board
2. For each product's Git workspace: run `git rev-list --count` for ahead/behind vs main
3. Classify recent commits (last 30 days) by type and domain
4. Check submodule statuses with `git submodule status`
5. Report findings to Knowledge Hub under `### process_insights` as "FALLBACK-EXTRACTED" rather than standard insights
6. Always note the board-empty condition prominently so downstream readers know the data source

## Pitfalls
- **DO NOT** extract Kanban-style workflow metrics from git data (commits are not tasks, branches are not workflows)
- **DO NOT use this fallback because the local `kanban.db` is empty** — that DB is not the board's data source. The board lives in the Projekte-Hub web app; query `GET https://projekte.kijan.ch/api/ideas?project=<board>` first (see `projekte-hub-api-fetch.md`). Verified 2026-10-21: the local DB was empty while the API served 578 live kpt entries — the git fallback was used unnecessarily for weeks and the real board data was missed.
- Label all fallback findings with metadata `source=git_fallback` to distinguish from board-derived insights
- Git data only shows what was committed, not what was discussed/decided/planned
- Branch names may be misleading (`wf-layout-final` suggests completeness but status is unclear)
