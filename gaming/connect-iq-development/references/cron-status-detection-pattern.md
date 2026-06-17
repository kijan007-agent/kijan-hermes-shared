# Cron Status Detection Pattern — KijanPersonalTracker

## Core Principle: TASKS.md is NOT a source of truth for file existence
TASKS.md tracks planning intent. Working tree + git history = actual state.
If `find` says file is missing, it's missing — regardless of TASKS.md claims.

## Detection Workflow (execute ALL steps, in order)

### Step 1: Workspace path (ALWAYS start here)
Base path: `/workspace/Github/KijanPersonalTracker-hermes/`
- `kpt-app-ciq` = working submodule with full `.mc` source tree
- `kpt-doc` = docs at `/workspace/Github/KijanPersonalTracker-hermes/kpt-doc/`
- **NEVER use `/data/Github/`** — sandbox-only, inaccessible

### Step 2: Verify file exists on disk
```bash
find /workspace/Github/KijanPersonalTracker-hermes -path '*/kpt-app-ciq/source/<file>.mc'
```
If found: `read_file` at that path.
If not found: go to Step 3.

### Step 3: Check git history in working tree
```bash
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq log --oneline --all -- source/<file>.mc
```
If found: file was committed but deleted or replaced.
If not found: go to Step 4.

### Step 4: Check submodule remote branches
```bash
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq ls-tree origin/feature --name-only
# or for specific file:
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq show origin/feature:source/<file>.mc
```
Packed-refs may contain feature branch data even without remote access.

### Step 5: Session history
```bash
session_search(query="<filename> mc file work done implementation")
```

### Step 6: Cross-reference with TASKS.md (for context only)
TASKS.md may provide context about INTENDED work, but never trust it for existence.

## Status Reporting Convention
| Symbol | Meaning | Action |
|--------|---------|--------|
| ✅ | File exists AND matches documented implementation | No action needed |
| ⚠️ | Documented as done but file mismatch (stub vs full impl) | Document discrepancy, plan re-implementation |
| ❌ | File doesn't exist — never created or was deleted | Report as "not started" or "deleted", do NOT report as "pending" |
| 📋 | TASKS.md says done, disk says otherwise | **This is the common case** — report as "claimed but not committed" |

## Known False Completions (2026-05-23 audit)
- **EnergyScreen chart**: TASKS.md: "COMPLETED ✅" → disk: 123-line stub. `origin/feature` also has stub (chart was committed then replaced at `9bb0b5d`)
- **DeltaInputScreen.mc**: TASKS.md: "COMPLETED ✅" → file NEVER existed on disk or git

## Workspace Path Summary
| Path | Status | Use for |
|------|--------|---------|
| `/workspace/Github/KijanPersonalTracker-hermes/` | ✅ ACTIVE | All file operations |
| `/workspace/Github/KijanPersonalTracker/` | ⚠️ OLD | kpt-app-ciq was bare repo, no .mc files |
| `/data/Github/` | ❌ SSBAND | Cron sandbox — inaccessible |
