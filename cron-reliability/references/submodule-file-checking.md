# Submodule File Checking (2026-05-23)

## Problem
kpt-app-ciq is a git submodule in KijanPersonalTracker-hermes. Standard file paths (`/data/Github/KijanPersonalTracker-feature/kpt-app-ciq/source/EnergyScreen.mc`) fail because:
- `/data/Github/` is not mounted in cron sandbox
- Submodule working tree may not be populated
- Submodule HEAD may be detached

## Detection Flow

### 1. Find actual location
```bash
find /workspace -name 'kpt-app-ciq' -type d 2>/dev/null
# → /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq
```

### 2. Check if submodule is populated
```bash
ls /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq/source/EnergyScreen.mc
```
If found → `read_file` at that path.

### 3. If not found, check git tree
```bash
cd /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq
git ls-tree -r HEAD -- source/ | grep EnergyScreen
```

### 4. If still not found, check parent repo submodule pointer
```bash
cd /workspace/Github/KijanPersonalTracker-hermes
git ls-tree -r HEAD -- kpt-app-ciq/ | grep EnergyScreen
# Only shows commit hash, not files
```

### 5. If nothing found, check git history
```bash
cd /workspace/Github/KijanPersonalTracker-hermes
git log --all --oneline -- 'kpt-app-ciq/source/EnergyScreen.mc'
```

## Key Pattern
Files in submodules MUST be looked up via the submodule's own working tree or git tree, NOT via parent repo paths. Parent repo only stores commit hash pointers.
