# Knowledge Hub File Counting Protocol

> Discovered 2026-06-03. File counts in KNOWLEDGE-HUB.md go stale rapidly due to methodology drift and categorization corrections.

## Why Counts Go Stale

1. **Counting methodology changes:** e.g., alembic env.py excluded from py count (109→102)
2. **File categorization corrections:** e.g., .mc/.xml files reclassified (169→241)
3. **Recursive find vs manual count discrepancies:** e.g., kpt-doc 504→480 (corrected), MEMORY 188→187

## Verification Protocol

**Always run fresh counts before updating KNOWLEDGE-HUB.md:**

```bash
# Python files (exclude alembic env.py, test files if tracked separately)
find <repo>/ -name '*.py' -not -path '*/alembic/env.py' | wc -l

# MC/XML files (Connect IQ)
find <repo>/ -name '*.mc' | wc -l
find <repo>/ -name '*.xml' | wc -l

# Total repo files
find <repo>/ -type f | wc -l

# Specific directory
find <repo>/app/ -type f | wc -l

# Test files
find <repo>/ -name 'test_*.py' | wc -l
```

## Update Convention

When counts change from previous Knowledge Hub state:
- Mark as `**CHANGED** (old→new — reason)`
- Document the correction reason explicitly
- Never silently update — always explain the delta

## Known Corrections (2026-06-03)

| Product | Metric | Old | New | Reason |
|---------|--------|-----|-----|--------|
| kpt-backend | py files | 109 | 102 | Excluded alembic env.py + root scripts |
| kpt-backend | test files | 12 | 11 | Test consolidation |
| kpt-backend | test lines | 3,205 | 2,512 | Test consolidation |
| kpt-app-ciq | .mc/.xml | 169 | 241 | Corrected categorization |
| kpt-doc | total files | 504 | 480 | Corrected recursive find |
| kpt-doc | MEMORY | 188 | 187 | Corrected recursive find |
