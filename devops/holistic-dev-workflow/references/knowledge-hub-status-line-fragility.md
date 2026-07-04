# Knowledge Hub Status Line Fragility

> Discovered 2026-06-08. After patching one status line in KNOWLEDGE-HUB.md, the file content shifts and subsequent patches fail because `old_string` no longer matches.

## The Problem

KNOWLEDGE-HUB.md uses per-line keyword replacement via `skill_manage(action='patch')`. When you patch one line in a section, the entire file content changes. If you then try to patch a second line with the same `old_string`, it will fail because the content has shifted.

## Symptoms

- First patch succeeds
- Second patch on a different line in the same section fails with "Found N matches" or "No matches found"
- The `old_string` was correct before the first patch but is now stale

## Workaround

**Always re-read the file between patches in the same section.**

```
1. patch line A → success
2. read_file the entire KNOWLEDGE-HUB.md
3. find the new content for line B
4. patch line B with updated old_string → success
```

## Prevention

- **Never batch multiple patches** on status lines in a single pass
- After each patch, **re-read the affected section** before crafting the next patch
- Use `search_files` to find exact current content before patching
- Status lines change after every update (timestamps, status keywords, byte counts shift)

## Known Affected Sections

- Submodule status table (line ~244-255)
- Risk patterns table (line ~191-222)
- Cross-product analysis table (line ~440+)
- kpt-backend section (line ~260+)
- kpt-app-ciq section (line ~305+)
- kpt-doc section (line ~290+)

## History

| Date | Issue | Fix |
|------|-------|-----|
| 2026-06-08 | Multiple patches on same section failed | Always re-read between patches |
| 2026-05-27 | `replace_all=True` removed entries from unintended sections | Never use `replace_all` on multi-section entries |
| 2026-05-25 | Pipe-inconsistency broke block-level replace | Per-line keyword replacement only |
