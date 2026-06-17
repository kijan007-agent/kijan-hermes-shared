---
name: server-first-git-sync
version: 1.0
description: Before every task, always check and pull from server's feature branch. Server is source of truth.
---

## Rule
**Before every task**, always check and pull changes from the server's feature branch. Server is the absolute source of truth.

## Procedure

### 1. Main Repository
```bash
cd /workspace/Github/KijanPersonalTracker-hermes
git fetch origin
git checkout feature
git pull origin feature
```

### 2. Every Submodule
```bash
cd /workspace/Github/KijanPersonalTracker-hermes
for sub in kpt-app-ciq kpt-backend kpt-doc kpt-datafield-ciq kpt-admin kpt-symptoms-app; do
    cd "$sub"
    git fetch origin
    git checkout origin/feature
    cd ..
done
```

### 3. Sync Submodule Pointers
```bash
git submodule update
```

### 4. Handle CRLF/Linefeed Issues
If submodule shows "modified content" after sync:
```bash
cd <submodule-dir>
git config core.autocrlf input
git config core.eol lf
git config core.safecrlf false
git reset --hard <commit-hash-from-main-repo>
cd ..
```

### 4b. Mass CRLF Fix for Connect IQ (.mc files)
After resetting the submodule, if `.mc` files still have CRLF:
```python
import os
ciq_source = '/workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq/source'
for root, dirs, files in os.walk(ciq_source):
    for f in files:
        if f.endswith(('.mc', '.py')):
            full = os.path.join(root, f)
            with open(full, 'rb') as fh:
                content = fh.read()
            if b'\r\n' in content:
                with open(full, 'wb') as fh:
                    fh.write(content.replace(b'\r\n', b'\n'))
```
⚠️ Never use `sed` for this — Python binary-mode is required.

## Known Workspaces (updated 2026-05-20)

- `/workspace/Github/KijanPersonalTracker-hermes/` — hermes branch workspace (Hermes work)
- `/data/Github/KijanPersonalTracker-feature/` — feature branch workspace (feature work, specs)
- BOTH are valid git repos with real content. Use `/data/` for specs authoring, `/workspace/` for implementation.
- `origin/feature` — primary development branch
- `origin/feature-2` — legacy branch (contains EnergyScreen.mc)
- `origin/hermes` — synced to feature (via merge)
- `origin/prod-hotfix-bat` — production hotfix branch

## Update Pattern: Feature → Hermes
When `update-hermes-from-feature.sh` is not available or needs manual execution, use:
```bash
# For each repo (public ones):
git fetch origin
git merge origin/feature --no-ff -m "Merge feature → hermes"
git push origin hermes
# Tag: git tag merge-feature-to-hermes_<timestamp>
# Private repos: convert remote to SSH first
```

### Private Repo SSH Conversion
Before merging, private repos need SSH remotes:
```bash
cd <private-repo>
git remote set-url origin git@github.com:kijan007/<repo-name>.git
```
Without this, `git fetch origin` fails with SSH permission denied.

### Merge Integrity Verification
After merge, confirm feature commits are included in hermes:
```bash
git log --oneline origin/hermes..origin/feature | wc -l
# If > 0 → incomplete merge, feature commits missing from hermes
```

## Remote VM Pitfalls (Proxmox LXC / SSH)

### Patch Creates Duplicates
After patching code files, always `read_file` to verify no duplicate blocks were created (duplicate if/try/except/while blocks). This happens when the old and new strings share common prefixes.

### Patch Creates Indentation Errors
Patching Python files can break indentation if the old/new strings don't align exactly with line boundaries. Always verify the patched region looks correct.

### WeasyPrint Import — ImportError Insufficient
`except ImportError` does NOT catch WeasyPrint import failures. WeasyPrint loads its own C-extensions at import time which crash when libpango/libcairo missing → use `except Exception`.

## Remote VM Pitfalls (Proxmox LXC / SSH)
### SSH terminal tool — foreground blocks long-lived processes
**CRITICAL**: The `terminal` tool treats ANY command that looks like a server/process as "long-lived" and blocks it — even `ps aux | grep`. This includes `python3 -m uvicorn`, `docker compose up`, `nohup ... &`, and `python3 -c '...'` with multiline content.

**Workaround**:
1. **For servers**: Always use `terminal(background=true)` to start servers. Verify readiness in a SEPARATE command (e.g., `curl`, `docker logs`).
2. **For Python scripts**: Avoid heredocs (`<< 'EOF'`) in SSH — they hang the SSH channel. Use simple one-liners or `python3 -c` with escaped strings.
3. **For `apt`/`pip install`**: These can hang for minutes. Use `terminal(background=true)` or run manually on the VM.
4. **For `scp`**: Can hang on slow connections. Use `ssh` to write files directly on the VM instead.
5. **For `ps`/process checks**: Use `docker ps` instead of `ps aux | grep` — the grep pattern triggers the long-lived detector.

### write_file does NOT work on remote VM paths
`write_file` writes to the agent's local filesystem only. To write files on a remote VM, use `ssh ... "python3 -c '...'"` or `cat > file << 'EOF'` on the VM directly.

### Docker on LXC — `host.docker.internal` doesn't work
On Proxmox LXC, `host.docker.internal` is NOT available. Use the Docker bridge gateway directly: `172.17.0.1` (default) or `bridge` network mode.

## Merge feature → hermes (update-hermes-from-feature.sh)

### The Script
Located at `/workspace/.hermes/update-hermes-from-feature.sh` (or `<repo>/scripts/` in KijanPersonalTracker).
Usage: `bash update-hermes-from-feature.sh`

### Pitfall: Private Repos Break the Script
The script fetches from `origin/feature` and merges to `hermes`. Private repos (kpt-common-barrels-ciq, kpt-symptoms-app) fail on fetch because their remotes use HTTPS (not SSH). 

**Fix:** Before running the script, convert all remotes to SSH:
```bash
cd <repo>
git remote set-url origin git@github.com:kijan007/<repo>.git
```
Or set globally for all submodules:
```bash
for sub in kpt-common-barrels-ciq kpt-symptoms-app; do
  cd /workspace/Github/KijanPersonalTracker-hermes/$sub
  git remote set-url origin git@github.com:kijan007/$(basename $(pwd)).git
done
```

### Pitfall: Stale origin/* refs After Merge
After merging, `git rev-parse origin/feature` may still show an old SHA because `origin/feature` refs are cached. Use `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` to force-update all remote refs before comparing.

### Pitfall: `--no-ff` Merge — `Already up to date` with Different SHAs
After a `--no-ff` merge, `origin/feature` and `origin/hermes` point to different commits (feature is the merge-base, hermes is the merge commit). This is **normal** — do NOT interpret as "not merged". Verify with:
```bash
git merge-base --is-ancestor origin/feature origin/hermes && echo "feature is ancestor of hermes"
# or
git log --oneline origin/hermes..origin/feature  # should be EMPTY if feature is included
```

### Pitfall: User Pushes to feature Between Fetch and Merge
The script fetches, but if the user pushes new commits to feature between fetch and merge, the script merges an outdated snapshot. Run `git fetch origin` immediately before the script, and inform the user to pause pushes during the merge.

### Pitfall: CRLF Blocks Submodule Merge
Submodule with CRLF issues aborts `git submodule update`. Fix before merging:
```bash
cd <submodule>
git config core.autocrlf input
git config core.eol lf
git config core.safecrlf false
git reset --hard <expected-hash>
```

## Verification
After sync:
```bash
git submodule status  # compare with git ls-tree HEAD
git status            # no uncommitted changes expected
```

## Verify Merge Integrity
After merging feature → hermes:
```bash
# For each repo, confirm feature commits are in hermes
git log --oneline origin/hermes..origin/feature | wc -l  # should be 0 or only merge commits
```
If non-zero → feature commits NOT in hermes → incomplete merge.