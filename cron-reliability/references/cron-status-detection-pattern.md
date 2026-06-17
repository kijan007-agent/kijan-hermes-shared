# Cron Status Detection Pattern — KijanPersonalTracker (STALE — post-wipe, 2026-06-08)

> **WARNING**: All repos wiped. This pattern is historical reference only.

## Core Principle: TASKS.md is NOT a source of truth for file existence
TASKS.md tracks planning intent. Working tree + git history = actual state.

## Detection Workflow (execute ALL steps, in order)

### Step 0: Verify repos exist and are populated
```bash
git -C /workspace/Github/KijanPersonalTracker-hermes log --oneline -1 2>&1
git -C /workspace/Github/KijanPersonalTracker-feature log --oneline -1 2>&1
```
If both return "No commits yet" → repos are empty shells. Skip to Step 5.

### Step 1: Workspace path
Base path: `/workspace/Github/KijanPersonalTracker-hermes/`
- `kpt-app-ciq` = working submodule with full `.mc` source tree
- `kpt-doc` = docs at `/workspace/Github/KijanPersonalTracker-hermes/kpt-doc/`
- **NEVER use `/data/Github/`** — sandbox-only, inaccessible

### Step 2: Verify file exists on disk
```bash
find /workspace/Github/KijanPersonalTracker-hermes -path '*/kpt-app-ciq/source/<file>.mc'
```

### Step 3: Check git history in working tree
```bash
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq log --oneline --all -- source/<file>.mc
```

### Step 4: Check submodule remote branches
```bash
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq ls-tree origin/feature --name-only
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq show origin/feature:source/<file>.mc
```

### Step 5: Session history
```
session_search(query="<filename> mc file work done implementation")
```

### Step 6: Cross-reference with TASKS.md (for context only)
TASKS.md may provide context about INTENDED work, but never trust it for existence.

## Workspace Path Summary (HISTORICAL)
| Path | Status | Use for |
|------|--------|---------|
| `/workspace/Github/KijanPersonalTracker-hermes/` | ✅ ACTIVE (pre-wipe) | All file operations |
| `/workspace/Github/KijanPersonalTracker-feature/` | ✅ ACTIVE (pre-wipe) | Feature branch |
| `/data/Github/` | ❌ SANDBOX | Cron sandbox — inaccessible |

## Post-Wipe State (2026-06-08)
All repos empty. Remote unreachable (404). Source code LOST. Only surviving content: `kpt-doc/_specs/` (untracked).
