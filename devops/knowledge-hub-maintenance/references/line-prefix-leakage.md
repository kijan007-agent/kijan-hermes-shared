# Patch Tool Line-Number Prefix Leakage

## Pattern
After a `patch` operation, `patch` tool can leak line-number prefixes onto output lines:
- `3|## Cross-Project Knowledge Hub` (was `## Cross-Project Knowledge Hub`)
- `4|` (was empty line)
- `5|||||||||` (was `|||||||||`)
- `6|*Nächste Aktualisierung:` (was `*Nächste Aktualisierung:`)
- `7|` (was empty line)

## Detection
```bash
grep -n '^[3-7]|' KNOWLEDGE-HUB.md
# or: grep -n '^|' file | head  # any line starting with digit+|
```

## Fix (Python)
```python
content = open(path).read()
lines = content.split('\n')
clean = []
for line in lines:
    if line[:2] in ('3|', '4|', '5|', '6|', '7|'):
        clean.append(line[2:])
    else:
        clean.append(line)
open(path, 'w').write('\n'.join(clean))
```

## Prevention
- Always run `grep -n '^[3-7]|'` IMMEDIATELY after any patch
- Never trust the patch output blindly
- The `patch` tool is modifying line content, not just the file
- This happens on single-line replacements too, not just multi-line

## Root Cause
The `patch` tool appears to inject line-number context markers into the replacement output. This is a tool bug, not a user error.

## Related
- `scripts/post-patch-dedup-check.py` — runs after every patch
- `references/replace-all-repair-procedure.md` — repair for replace_all corruption