# Repo Wipe Event — 2026-06-07

## Events
Two repos that previously had commits are now completely empty:

| Repo | Previous State | Current State |
|------|---------------|---------------|
| `KijanPersonalTracker-feature` | Had commits (origin/feature), 171 MC files | Zero commits, zero remotes, zero objects |
| `KijanPersonalTracker-hermes/kpt-backend` | Had commits (dev branch), 37+ commits | Zero commits, zero remotes, zero objects |

## Impact
- **All KijanPersonalTracker implementation work is lost** — no git history, no remote tracking
- Spec docs in `kpt-doc/_specs/` and `kpt-doc/_mockups/` still exist on disk (untracked, not in git)
- Test stubs in `kpt-backend/tests/` still exist on disk
- **TASKS.md, worklogs, and all source code are gone** from version control

## Detection Pattern
```
git -C <path> log --oneline -1  → "fatal: your current branch 'master' has no commits yet"
git -C <path> remote -v         → empty output (no remotes)
git -C <path> status            → "No commits yet" + untracked files only
```

## Recovery Options
1. **Remote backup**: Check if `origin` was previously set to a real GitHub remote → `git remote add origin <url>` + `git fetch` (won't work if remote was also wiped)
2. **User backup**: Ask user if local backup exists outside this machine
3. **Spec recovery**: Reconstruct from `kpt-doc/_specs/` and `kpt-doc/_mockups/` disk files
4. **Session history**: Use `session_search` to find prior code content from earlier sessions

## Root Cause Hypothesis
- `git init --force` or `rm -rf .git && git init` on both repos
- Manual re-initialization during workspace cleanup
- Not a git operation — likely manual filesystem intervention

## Prevention
- After any workspace restructure, verify all repos: `for d in /workspace/Github/*/; do echo "$d: $(git -C "$d" rev-list --count HEAD 2>/dev/null || echo 'EMPTY')"; done`
- Never run `git init` in an existing repo directory without first backing up `.git/`
- Add pre-flight check to cron reliability: verify repos have commits before status audits
