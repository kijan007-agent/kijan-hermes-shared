# Dual-Workspace File Sync Protocol

## Problem
`/workspace/Github/...` and `/data/Github/...` are separate filesystem mounts with DIFFERENT content. Files written to one path are NOT visible at the other.

## Rules
1. `/workspace/Github/KijanPersonalTracker-hermes/` is the ACTIVE workspace for git operations
2. `/data/Github/KijanPersonalTracker-feature/` may have different content (specs, working copies)
3. When writing test files, configs, or artifacts → verify they exist at BOTH paths
4. If a file exists at `/data/Github/...` but not `/workspace/Github/...` → copy it:
   ```bash
   cp /data/Github/.../file.ext /workspace/Github/.../file.ext
   ```
5. When in doubt, check BOTH paths with `ls` before reading/writing

## Pattern
```bash
# Write to both paths
cp file /workspace/path/
cp file /data/path/  # if /data/Github exists with content
```
