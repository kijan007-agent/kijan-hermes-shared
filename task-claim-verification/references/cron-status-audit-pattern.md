# Cron Status Audit Pattern (2026-05-27)

## Pattern: TASKS.md Claims vs Reality Verification Protocol

When auditing TASKS.md completion claims for accuracy:

### Step 1: File Existence Check
```bash
# Check if file exists on disk
find <repo> -name '<FileName>' -type f
# Check git history for any creation
git log --all --oneline --diff-filter=A -- '**/<FileName>*'
# Check git log for any reference
git log --all --oneline -S '<FileName>'
```

### Step 2: Line-Count Verification
```bash
# Current line count
wc -l <file>
# Historical max line count
git log --all --oneline -- <file> | while read sha rest; do
  echo "$sha $(git show ${sha}:$(basename <file>) 2>/dev/null | wc -l)"
done | sort -k2 -rn | head -5
```

### Step 3: Chart/Feature Regression Detection
```bash
# Check commits that simplified/reverted complexity
git log --all --oneline --diff-filter=M -- <file> | head -20
# Compare peak complexity vs current
git show <peak-commit>:<file> | wc -l
git show HEAD:<file> | wc -l
```

### Step 4: Overlay/State Fix Verification
```bash
# Check overlay management is wired
grep -n 'overlay\|stack\|popup\|dismiss' <controller>.mc
# Check transition validation uses correct source
grep -n 'fromScreen\|mCurrentScreen' <controller>.mc
# Check session sync fixes
git show <commit-hash> --stat
```

### Classification Rules
| Claim | Reality | Classification |
|-------|---------|---------------|
| File exists at claimed size | ✅ matches | COMPLETED |
| File exists but smaller | OVERSTATED | core exists, details missing |
| File exists but chart removed | REGRESSED | was implemented, reverted |
| File never existed | NEVER_CREATED | doc-first pattern, no code |
| File exists but not wired | DISABLED | code present, unreachable |

### Key Findings from KijanPersonalTracker Audit
- EnergyScreen: TASKS.md claims 493 lines → max historical 169 lines (c0fc0b1) → current 80 lines
- DeltaInputScreen: TASKS.md claims 417 lines → file NEVER existed → NEVER_CREATED
- TASKS.md is doc-first (spec written before implementation), leading to overstated claims
- Always verify via git history, not just current disk state
