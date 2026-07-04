# Cron Status Audit Pattern

## Problem
Cron jobs receive task lists referencing files at specific paths. Those files may not exist locally due to:
1. Empty repos (no commits/fetches in container)
2. Ghost submodules (remote branch has no content)
3. Path prefix mismatch (`/data/Github/` vs `/workspace/Github/`)

## Audit Workflow (Mandatory for cron)

```
1. Scan /data/Github/KijanPersonalTracker-feature/
   → ls -la (check for kpt-app-ciq/ subdirectory)
2. Scan /workspace/Github/KijanPersonalTracker-hermes/
   → git log --oneline -5 (check for commits)
   → git submodule status (check submodule state)
3. If BOTH repos empty → scan kpt-doc/_specs/ (only persistent content)
4. Report: "Repos empty, source inaccessible. Prior status from TASKS.md only."
5. NEVER declare tasks "not done" based solely on file-not-found in empty repos.
```

## Key Rule
When auditing cron tasks against empty repos:
- **TASKS.md/worklogs** = documented intent (may or may not match actual code)
- **Empty git repos** = cannot verify; block on fetch
- **kpt-doc/_specs/** = only locally persistent content
- **Source code** = only accessible via `git show <sha>:<path>` or remote fetch

## Cron Session Evidence (recurring since ~May 9, confirmed through June 3)
- `kpt-app-ciq` submodule: ghost `dev` branch on remote, submodule broken (persistent)
- Both `KijanPersonalTracker-feature` and `KijanPersonalTracker-hermes`: empty git shells (23+ days persistent)
- Only `kpt-doc/_specs/health-aggregation-layer/` persists on disk (~20 spec files)
- Remote `origin` for feature repo: "Repository not found" (private or non-existent on GitHub)
- Remote for kpt-backend: no remote configured
- Prior session work documented in TASKS.md/worklogs but source never persisted to container
- **Pattern stability**: No change across 6+ cron sessions (May 11 – June 3). Not a transient issue — a structural gap between documented intent and container state.
