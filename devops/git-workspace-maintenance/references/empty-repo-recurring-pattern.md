# Empty Repo Recurring Pattern — KijanPersonalTracker

## Pattern
Both `KijanPersonalTracker-feature` and `KijanPersonalTracker-hermes` are empty git shells across multiple cron sessions.

## Evidence (2026-05-23)
- `KijanPersonalTracker-feature`: no commits, `kpt-doc/_specs/` only (untracked), no `kpt-app-ciq/`
- `KijanPersonalTracker-hermes/kpt-backend`: no commits, 3 test files only (untracked)
- Neither repo has remotes configured
- TASKS.md, worklogs, and `.mc` source files do not exist locally
- `kpt-doc/_specs/health-aggregation-layer/` has 20+ spec files (the only persistent content)

## Root Cause
`kpt-app-ciq` submodule (bare) — submodule ref points to `dev` branch of `kijan007/kpt-app-ciq` which has no branches (ghost branch). Submodule is broken/non-functional.

## Workaround
- Prior task completion status must come from TASKS.md/worklogs in the **hermes repo's upstream history**, not local disk
- Source code implementation requires fetching from the feature branch directly
- When both repos empty: report blocker, do not assume code exists locally

## Status Across Cron Sessions
- Sessions since ~May 9 have repeatedly encountered empty repos
- Tasks planned in TASKS.md exist as documentation only — source never persisted
- The `dev` branch on remote may have content but is inaccessible from container (no SSH auth / ghost branch)
