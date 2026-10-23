# Python `.replace()` `{}` Placeholder Leak

**Discovered**: 2026-07-10
**Severity**: HIGH — silent failure
**Skill**: knowledge-hub-maintenance

## Problem

When updating KNOWLEDGE-HUB.md via Python `str.replace(old, new)`, if `old` contains `{}` (from a prior cron update that used f-string interpolation like `f"### Neue Patterns ({})" `), the `replace()` call silently fails to match — **no error, no output change**, and the stale `{}` remains in the file.

## Symptoms

- File appears unchanged after `str.replace()` call
- `grep '{}' file` reveals literal `{}` in section headers
- Line count unchanged

## Prevention

1. **Never use f-string interpolation to build the `old` parameter** in `str.replace()` — always use the exact literal string from the file
2. **Read the file content first**, then use the exact substring found in the file as `old`
3. **Prefer line-by-line index replacement** (`lines[i] = new_content`) over `str.replace()` — it avoids substring matching entirely

## Detection

After any Python update to KNOWLEDGE-HUB.md:
```bash
grep -n '{}' /workspace/.hermes/workflows/holistic-dev-workflow/KNOWLEDGE-HUB.md
```
Expected result: **0 matches**. Any match = stale placeholder.

## Fix

If `{}` found in file content (not in comments):
1. Use `sed -n 'Np' file` to get the exact line at the given index
2. Manually craft the replacement with the exact literal text
3. Or use line-by-line index replacement instead

## Session Evidence

During 2026-07-10 20:52 cron run:
- `str.replace('### Neue Patterns ({}):', '### Neue Patterns (2026-07-10 20:52 UTC):')` **failed silently**
- The `old` string in the code didn't match the actual file content
- Fix: Used `lines[770] = '### Neue Patterns (2026-07-10 20:52 UTC)\n'` (index-based)
- This is a recurring pattern — ALWAYS use index-based replacement for known-line updates
