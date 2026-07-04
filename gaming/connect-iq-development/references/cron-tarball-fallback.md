# Cron Tarball Fallback Pattern

**Discovered**: 2026-06-03

## Problem
Cron jobs run in a sandbox where `/data/Github/` paths for KijanPersonalTracker are dead repos (zero commits, unreachable remotes). The active workspace `/workspace/Github/` may also be unavailable.

## Detection
```bash
git -C /data/Github/KijanPersonalTracker-feature rev-parse HEAD  # outputs just "HEAD" = empty
git branch -a  # empty = no branches
```

## Fallback Steps
1. `ls /tmp/kpt-app-ciq*.tar.gz` — find available tarballs
2. `tar xzf /tmp/kpt-app-ciq-full.tar.gz -C /tmp/kpt-extract` — extract to temp
3. Read from `/tmp/kpt-extract/source/*.mc`
4. Note: tarball content is STATIC — not git-tracked, may be stale

## Known Tarballs
- `/tmp/kpt-app-ciq-full.tar.gz` — full source (7.8MB, 302 entries)
- `/tmp/kpt-app-ciq.tar.gz` — smaller variant (220KB)
- `/tmp/kpt-common-barrels.tar.gz` — shared barrels only (6KB)

## Key Files in Full Tarball
- `source/EnergyScreen.mc` — energy screen (123 lines stub)
- `source/ScreenFlowController.mc` — navigation controller (691 lines)
- `source/EnergyDrawable.mc` — shared drawable (151 lines)
- `source/ActivitySession.mc` — session state
- `docs/Architecture.md` — architecture docs
- No `TASKS.md` or `_worklogs/` in tarball — only in feature repo's kpt-doc submodule
- No `DeltaInputScreen.mc` — was removed/disabled in codebase

## Classification of Missing Files
When a file is missing from the tarball:
- **Never existed**: `DeltaInputScreen.mc` (disabled in ScreenFlowController line 428-429)
- **Removed**: Was implemented then deleted (check git history separately)
- **Not in tarball**: May exist in live repo but not packed
- **Always verify**: `tar tzf <tarball> | grep <file>` before assuming absence
