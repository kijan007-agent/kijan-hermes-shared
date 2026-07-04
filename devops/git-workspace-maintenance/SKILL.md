---
name: git-workspace-maintenance
description: "Manage local git repos: fix ownership, create bundles, resolve permission errors."
---

# Git Workspace Maintenance

## Permission Fixes
Recurring issue in `/data/Github/` repos: `.git/` directories owned by `root`.
Triggers: `index.lock`, `unpacker error`, `dubious ownership`.
Action:
```bash
sudo chown -R jan:jan /data/Github/<repo>
sudo chmod -R u+rwx /data/Github/<repo>
```

## Bundle Transfer (Migration/Backup)
Use when remotes are inaccessible or permission denied (e.g., pushing to root-owned server).
1. **Create Bundle:** `git bundle create /tmp/branch.bundle <ref>` (e.g., `origin/dev`, `HEAD`)
2. **Copy Bundle:** `scp /tmp/branch.bundle user@host:/path/`
3. **Apply Bundle:** `git bundle unbundle <file> | xargs git cherry-pick` or `git fetch <file> <ref>`

## Bare Clone — No Working Tree
Triggers: `.git/` exists with pack objects, no index, no working tree files, `git checkout` fails because there's no index.
Diagnosis: `ls .git/index` → absent, `find . -name "*.mc"` → nothing (but pack has objects).
Fix:
```bash
# If it's a bare clone:
git remote add origin <url>   # if remote not configured
git fetch origin
git checkout <branch>         # creates index + working tree from branch tip

# Or if it's a shallow/partial clone with no index:
rm -f .git/index
git reset --hard HEAD         # rebuilds index from HEAD commit

# Or if the commit is dangling (no ref points to it):
git fsck --lost-found         # find dangling commits
git branch <temp> <sha>       # create temp ref
git checkout <temp>
```

## Submodule Working Tree Recovery
Triggers: `.mc` / source files missing from submodule dir, `.git/index` absent, `.git` is directory but no working tree files.
```bash
# Remove stale shallow checkout
rm -rf <submodule>/.git/index <submodule>/.git/HEAD <submodule>/.git/packed-refs
# Re-initialize
git submodule update --init --recursive <submodule>
# Or manually: cd <submodule> && git checkout feature
```
Also check: `.gitmodules` paths, whether the submodule `.git` file points to the right gitdir, and if `gitdir:` path in `.git` file resolves.

## Local Remote Merging
Merging local feature to local prod when no shared remote is available:
1. `git remote add prod-repo <path_to_prod_repo>`
2. `git fetch prod-repo`
3. `git merge prod-repo/branch`
4. Resolve conflicts (submodules often need `git checkout feature-repo/feature -- <file>`).

### Further reading
- **`references/kijan-personal-tracker.md`** — KijanPersonalTracker project paths, branch state, TASKS.md patterns, common pitfalls. Updated 2026-05-18: active workspace = `/workspace/Github/KijanPersonalTracker-hermes/`. kpt-app-ciq HEAD = 5225456 (dirty +). kpt-doc = 5618c0e (clean, 4 worklogs). TASKS.md has stale commit hash references. DeltaInputScreen = deleted at c965f54. EnergyScreen = 123-line stub.
- **`references/kijan-empty-repo-state.md`** — Both feature and hermes repos are empty git shells (no commits, no remotes, no pack objects). `kpt-app-ciq/` source code never persisted to disk. Prior session task completions documented in TASKS.md/worklogs but source not on disk.
- **`references/empty-repo-recurring-pattern.md`** — Repeated empty-repo pattern across multiple cron sessions for KijanPersonalTracker repos, root cause (ghost submodule branch), and workaround strategy.
- **`references/bare-clone-detection.md`** — Bare clone symptoms, diagnosis steps, resolution patterns, and lesson on verifying working tree after clone.
- **`references/task-status-discrepancy.md`** — Detecting documented-vs-actual status gaps in cron status audits (when tasks are "completed" in docs but source files are missing from disk).
- **`references/kijan-feature-branch-absence.md`** — The `KijanPersonalTracker-feature` repo does NOT exist on disk. When auditing status, workspace scan must verify repo existence before attempting file reads.
- **`references/cron-status-audit-pattern.md`** — Mandatory audit workflow for cron tasks against empty repos: path prefix mismatch, ghost submodules, and distinguishing documented intent from verifiable state.

### Pitfall: TASKS.md says COMPLETED but source not on disk (bare submodule)
In KijanPersonalTracker, `kpt-app-ciq` is a bare submodule — no `.mc` files on disk.
When auditing status: TASKS.md + worklogs are the **only** source of truth for code changes.
Never claim "file not found = task not done" — verify via TASKS.md completion markers first.
Always note the caveat: "Completion documented, source not accessible (bare submodule)."

### Pitfall: Ghost Submodule (empty remote branch)
Pattern: `.gitmodules` config points to a branch, but the remote has no refs/heads for that branch.
Symptoms: `git submodule update` hangs or produces nothing, `git branch -a` shows no matching branch,
packed-refs is empty, refs/heads directory is empty.
Diagnosis:
```bash
# Check if branch exists on remote
git ls-remote origin refs/heads/<branch>
# If empty → ghost branch, submodule is non-functional
# Fix: Use alternative working copy path (e.g., prod-hotfix) instead of submodule
```
Example: KijanPersonalTracker's `kpt-app-ciq` submodule points to `dev` branch of `kijan007/kpt-app-ciq`
which has no branches. The submodule is effectively a broken reference.

### Pitfall: Workspace-local feature branch exists but remote fetch fails
Pattern: Feature branch repo (e.g., `/workspace/Github/KijanPersonalTracker-hermes/`) has
packed-refs with `origin/feature` SHA, but `git fetch` fails due to missing GitHub auth.
The feature branch commits exist locally but cannot be pulled.
Diagnosis:
```bash
# Check if packed-refs has the branch SHA
grep 'feature' .git/packed-refs
# Verify local commits exist
git log --oneline -5 origin/feature
# Check remote reachability
git remote -v
```
Fix: Use local packed-refs data directly — `git show <sha>:<path>` for file content,
`git diff origin/dev..origin/feature --stat` for file-level diffs.
No remote fetch needed to analyze what changed.

### Pitfall: Submodule ownership blocks git operations
Pattern: Submodule `.git/` dirs owned by root or different user → `git` commands silently fail.
Fix: `git config --global --add safe.directory /path/to/<submodule>` for each submodule.
Also check packed-refs in submodules for ghost branches.

### Pitfall: CRLF/linefeed blocks submodule checkout (submodule stuck on wrong commit)
Pattern: Main-Repo expects Submodule commit `X`, local Submodule is at commit `Y`.
`git submodule update` aborts because working tree has uncommitted changes (CRLF vs LF).
Symptoms: `modified: kpt-app-ciq (new commits, modified content)`, 200+ changed files listed.
Fix sequence:
```bash
# 1. Set lineending policy for the submodule
cd <submodule>
git config core.autocrlf input
git config core.eol lf
git config core.safecrlf false

# 2. Force checkout the exact commit the Main-Repo expects
git reset --hard <expected-commit-hash>

# 3. In main repo, the submodule should now show 'new commits' (hash change) — stage it
cd ../<main-repo>
git add <submodule>
```
Critical: If `git submodule update` fails with "Your local changes would be overwritten",
do NOT use `--force` or `git clean -fd` (can be slow/blocked). Use `git reset --hard` directly in the submodule.
Always verify with `git rev-parse HEAD` that the submodule is at the expected commit.

### Pitfall: Cron prompt references /data/Github/ but workspace is /workspace/Github/
Pattern: User/cron task provides file paths like `/data/Github/KijanPersonalTracker-feature/...` but the actual workspace base is `/workspace/Github/`.
Diagnosis: `/data/Github/` may exist but contain only `kpt-doc/_specs/` (untracked) — source code lives under `/workspace/Github/KijanPersonalTracker-hermes/`.
Action: When given paths start with `/data/Github/KijanPersonalTracker-feature`, first scan both `/data/Github/KijanPersonalTracker-feature/` AND `/workspace/Github/KijanPersonalTracker-hermes/` before declaring files missing. Do NOT assume "not found in /data" means "task not done."

### Pitfall: TASKS.md line-count claims are doc-first specs, not reality
Pattern: TASKS.md documents intended file size (e.g., "EnergyScreen: 493 lines") but actual max historical line count is much smaller (169 lines at peak). DeltaInputScreen claimed at 417 lines but file never existed.
Diagnosis: `git log --all --oneline -- <file> | while read sha rest; do echo "$sha $(git show ${sha}:$(basename <file>) 2>/dev/null | wc -l)"; done | sort -k2 -rn | head -5`
Action: When TASKS.md claims file size differs from reality, classify as OVERSTATED or NEVER_CREATED, not Complete. Always verify via git history, not just TASKS.md status markers. See `task-claim-verification` skill.

### Pitfall: Cron status audit — both repos empty, source only in git objects
Pattern: Both `KijanPersonalTracker-feature` and `KijanPersonalTracker-hermes` have zero commits, no remotes, no pack objects. Only `kpt-doc/_specs/` (untracked) persists.
Diagnosis: `git branch -a` (empty), `git log` (empty), `ls .git/objects/pack/` (empty), `cat .git/config` (no remotes).
Action: Scan BOTH repos, then report explicitly: "Both KijanPersonalTracker repos are empty git shells. Source code accessible only via remote fetch (requires SSH auth) or prior TASKS.md/worklog documentation." Block on codebase presence before any implementation.

### Pitfall: Submodule ref on branch doesn't match submodule HEAD
Pattern: Parent repo branch shows submodule at commit `X`, but submodule HEAD is `Y`.
`git submodule status` shows `+<hash>` (staged update, not committed) or `-<hash>` (not checked out).
Fix: `cd <submodule> && git rev-parse HEAD` to get actual checked-out commit,
then compare with `git show <parent-branch>:<submodule-path>` (returns 160000 commit <ref>).

### Pitfall: Documented Feature vs Actual Code State (merge purged files)
Pattern: TASKS.md / worklogs claim a feature was implemented, but the actual code is reverted/stale.
Caused by: files added in a commit (e.g., `5826510`) then deleted before merge to target branch.
Diagnosis sequence:
```bash
# 1. Verify the claimed commit exists in submodule
git rev-parse --verify <claimed-commit>

# 2. Check if files from that commit exist in current branch
git show <claimed-commit>:<path/to/file>   # succeeds if file exists
git show <feature-branch>:<path/to/file>   # succeeds if still present

# 3. Diff between claimed commit and current branch
git diff <claimed-commit>..<feature> --name-status | grep <filename>
# D = deleted, A = added (check both directions)

# 4. Trace file add/remove history
git log --all --oneline -- source/path/to/file
# Shows all commits that touched the file — look for add then delete

# 5. Verify merge ancestry
git merge-base --is-ancestor <claimed-commit> <feature>
```
Key: A merge commit (e.g., `9a7fe42`) may inherit changes from parents but ALSO
delete files from one parent in the resolution. Always diff forward from the feature commit.

### Pitfall: Submodule ref on branch doesn't match submodule HEAD
Pattern: Parent repo branch shows submodule at commit `X`, but submodule HEAD is `Y`.
`git submodule status` shows `+<hash>` (staged update, not committed) or `-<hash>` (not checked out).
Fix: `cd <submodule> && git rev-parse HEAD` to get actual checked-out commit,
then compare with `git show <parent-branch>:<submodule-path>` (returns 160000 commit <ref>).

### Pitfall: Container has no SSH auth for GitHub
Container runs as root with no SSH agent and no GitHub PAT in environment.
SSH keys from `/workspace/.ssh/` must be copied to `/root/.ssh/` and `~/.ssh/config` must set `IdentityFile`.
If the key is not registered in GitHub (user's personal key), SSH will be rejected with `Permission denied (publickey)`.
Fix options:
1. User adds the public key (`cat /workspace/.ssh/id_ed25519.pub`) to GitHub → Settings → SSH Keys.
2. User provides a GitHub PAT → switch remote to `https://<token>@github.com/...`.
Without one of these, all `git fetch/push` operations fail regardless of correct key files on disk.

### Pitfall: Merge script fails on private repos (HTTPS remotes)
The `update-hermes-from-feature.sh` script fetches from all configured submodules. Private repos (kpt-common-barrels-ciq, kpt-symptoms-app) use HTTPS remotes that fail in the container. Fix by converting to SSH:
```bash
for repo in kpt-common-barrels-ciq kpt-symptoms-app; do
  cd /workspace/Github/KijanPersonalTracker-hermes/$repo
  git remote set-url origin git@github.com:kijan007/$repo.git
done
```
Or run the script and manually handle the private repos after.

### Pitfall: Empty git repo (no commits, no objects, no remotes)
When a repo appears on disk but has zero content: no branches, no commits, no pack files, no remotes.
This means the repo was `git init`-ed but never cloned/fetched. Code cannot "be there" if nothing was ever fetched.
Diagnosis sequence:
```bash
git branch -a          # empty = no refs
git log --oneline -5   # empty = no commits
ls .git/objects/pack/  # empty = no fetched objects
cat .git/config        # check for [remote "origin"] sections
cat .git/FETCH_HEAD    # check if last fetch failed silently
```
If ALL are empty/missing → repo is a shell. Cannot proceed with file reads on it.
Report as blocker: "Repo initialized but empty — no remote configured, no content fetched."

### Pitfall: Repeated empty-repo pattern in KijanPersonalTracker repos
**REPEATABLE PATTERN:** Both `KijanPersonalTracker-feature` and `KijanPersonalTracker-hermes` are empty git shells across multiple cron sessions. `kpt-app-ciq/` source code never persists to disk. Only `kpt-doc/_specs/` and `kpt-backend/tests/` exist as untracked content.

When BOTH repos are empty:
1. **Do NOT** assume prior session work was committed
2. **Do NOT** search for source files — they don't exist locally
3. Report explicitly: "Both KijanPersonalTracker repos are empty git shells. No source code available locally. Prior task completions documented in TASKS.md/worklogs but source not on disk."
4. Block on codebase presence before any implementation work