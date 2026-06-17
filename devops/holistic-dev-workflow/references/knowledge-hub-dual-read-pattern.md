# Knowledge Hub Dual-Read Pattern

> When updating KNOWLEDGE-HUB.md across multiple sections, re-read the full file between each section's patches.

## Why

Every `patch` operation changes line numbers in the file. After patching section A, the `old_string` for section B no longer matches because:
- Lines were added/removed/shifted
- Pipe counts in table rows may vary (5, 6, or 9 pipes)
- Timestamps in headers may shift

## Pattern

```
1. Read file → find section A → patch section A
2. Read file AGAIN → find section B → patch section B
3. Read file AGAIN → find section C → patch section C
4. Read file AGAIN → verify footer timestamp matches header
```

## Never

- Batch multiple patches on different sections without re-reading
- Assume line numbers are stable after a patch
- Use `replace_all` on entries that appear in multiple sections

## Real Failure

Session 2026-06-09: Patching kpt-backend status in risk table without re-reading caused the kpt-backend status line in the submodule status table to fail on the next patch attempt — the old_string had shifted.
