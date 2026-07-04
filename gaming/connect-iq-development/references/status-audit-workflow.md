# Connect IQ Status Audit Workflow

Systematic 6-step verification for cross-repo status audits (cron or manual).

## Step-by-Step

### 1. Find the actual file on disk
```bash
find /workspace/Github/KijanPersonalTracker-hermes -name 'FileName.mc' 2>/dev/null
```
If found → proceed to Step 2 (read & verify).
If not → Step 3 (check git history).

### 2. Read and verify against TASKS.md
- Read file, compare line count/features against TASKS.md claims
- Mark: ✅ matches / ⚠️ partial / ❌ missing
- For EnergyScreen: check if stub (123 lines) or chart (493 lines)

### 3. Check git history for the file
```bash
cd /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq
git log --oneline --all -- source/FileName.mc | head -10
git log --oneline --ancestry-path <merge-base>..origin/feature -- source/FileName.mc
```
If committed then replaced: find the commit where it was replaced.

### 4. Check remote branch content
```bash
git show origin/feature:source/FileName.mc | wc -l
```
Packed-refs may contain feature branch data without remote access.

### 5. Check cross-repo references
```bash
# Check parent repo for submodule pointer
cd /workspace/Github/KijanPersonalTracker-hermes
git submodule status
git log --oneline -5 -- kpt-app-ciq
```

### 6. Compile findings into status table
| Item | TASKS.md Claims | Disk | Git History | Remote | Verdict |
|------|-----------------|------|-------------|--------|---------|

## False Completion Patterns to Watch

1. **TASKS.md written before commit** — cron writes TASKS.md then gets interrupted
2. **Ancestor ≠ current** — file committed at SHA-A, replaced at SHA-B, TASKS.md references SHA-A
3. **File never existed** — TASKS.md describes planned work, not actual work
4. **Submodule not populated** — file exists in submodule tree but not on disk
5. **Branch on disk diverges from remote** — local commits exist that haven't been pushed

## Worklog Gap Detection
```bash
ls -lt /workspace/Github/KijanPersonalTracker-hermes/kpt-doc/_worklogs/ | head -5
git log --oneline --since="<last_worklog_date>" --all | head -10
```
If commits exist after last worklog date → report WORKLOG GAP.
