# Bare Clone Detection — KijanPersonalTracker

## Session: 2026-05-09

### Problem
`kpt-app-ciq/` is a bare clone — `.git/` exists with 4582 pack objects but zero working tree files and no index.

### Symptoms
- `find . -name "*.mc"` → empty
- `git checkout` → fails (no index)
- `.git/` has `objects/pack/pack-*.idx` and `objects/pack/pack-*.pack`
- `.git/HEAD` points to `refs/heads/dev`
- `.git/refs/heads/` has `dev` and `feature` refs
- No `git` binary available in shell (`command not found`)

### Diagnosis Steps
1. `ls .git/objects/pack/` — confirms pack files exist
2. `ls .git/index` — absent confirms no index
3. `cat .git/HEAD` — confirms active ref
4. `cat .git/refs/heads/<branch>` — get SHA of target
5. `find / -maxdepth 6 -name "*.mc"` — check if other repos have files
6. Python pack parsing (`git index reader`, `idx v2 parser`) to extract file list from pack

### Resolution
```bash
# Option 1: Reclone (simplest)
rm -rf kpt-app-ciq
git clone https://github.com/kijan007/kpt-app-ciq.git kpt-app-ciq

# Option 2: Create index from existing refs
cd kpt-app-ciq
git remote add origin https://github.com/kijan007/kpt-app-ciq.git
git fetch origin
git checkout feature

# Option 3: When no git binary available
# Parse pack idx with Python to list files, read blobs directly
# See references/kijan-personal-tracker.md for project-specific paths
```

### Key Lesson
Bare clones happen when `git clone --bare` is used or when a repo is fetched but not checked out. Always verify `ls <repo>/source/` after cloning to confirm working tree exists.
