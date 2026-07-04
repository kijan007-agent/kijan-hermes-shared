# Cron Path Validation Pattern (2026-05-24)

When cron jobs reference files that don't exist at expected paths:

## 3-Layer Validation

### Layer 1: Path Existence
```bash
# Check if path exists and has content
ls <path> 2>/dev/null | head -5
# Empty output → check Layer 2
```

### Layer 2: Git Repo Validity
```bash
# A real repo must have: commits, remotes, or at least pack objects
git -C <path> rev-parse HEAD  # must output a hash, not just "HEAD"
git -C <path> log --oneline -1  # must output a commit
git -C <path> remote -v  # must show at least one remote
git -C <path> rev-list --objects HEAD 2>/dev/null | wc -l  # must be > 0
```
If ALL four commands show empty/zero → **empty shell, skip immediately.**

### Layer 3: Content Resolution
```bash
# If path repo is valid but file missing:
find <repo-root> -name '*.mc' -maxdepth 5 | grep -i <filename>
git -C <repo-root> log --all --oneline -- source/<filename>  # check if committed then deleted
```

## KijanPersonalTracker Path Map

| Path | Status | Content |
|------|--------|---------|
| `/workspace/Github/KijanPersonalTracker-hermes/` | ✅ ACTIVE | Full repo + submodules |
| `/workspace/Github/KijanPersonalTracker-feature/` | ✅ ACTIVE | Empty repo, zero commits |
| `/data/Github/KijanPersonalTracker-feature/` | ❌ EMPTY | Zero commits, no remotes |
| `/data/Github/KijanPersonalTracker-hermes/` | ❌ EMPTY | Zero commits, no remotes |
| `/home/hermes/Github/` | ⏳ FALLBACK | Check if mounted |

## Key Insight (2026-05-24)
Empty git repos (zero commits, zero remotes, zero objects) are indistinguishable from "repo not yet cloned" using only `ls` or `find`. You MUST run `git rev-parse HEAD` to detect them. A bare `ls` of an empty git repo looks like a valid directory.
