# replace_all Repair Procedure for KNOWLEDGE-HUB.md

When `replace_all` corrupts KNOWLEDGE-HUB.md (creates duplicated/corrupted lines), follow this exact procedure.

## Step 1: Detect Corruption

```bash
grep -n 'HANGED\|UNCHANGED\*\|ahead vs origin\|kpt-symptoms-app' KNOWLEDGE-HUB.md | head -20
```

Look for:
- Lines with garbled text (`UNCHANGEDHANGED**`, `UNCHANGED*UNCHANGED**`)
- Duplicate entries of the same product line
- Concatenated timestamps (`17:30 23:23`)
- Any line containing `*` in the middle of a word

## Step 2: Identify the Corruption Range

```bash
grep -n 'kpt-symptoms-app' KNOWLEDGE-HUB.md
grep -n 'HANGED\|UNCHANGED\*' KNOWLEDGE-HUB.md
```

Note the line numbers of the first clean occurrence and the start of corruption.

## Step 3: Surgical Removal via Python

```python
with open('/workspace/.hermes/workflows/holistic-dev-workflow/KNOWLEDGE-HUB.md') as f:
    lines = f.readlines()

# Delete lines 96-101 (example range — adjust per actual grep output)
# Keep lines 0-95 and 102-end
del lines[96:102]

with open('/workspace/.hermes/workflows/holistic-dev-workflow/KNOWLEDGE-HUB.md', 'w') as f:
    f.writelines(lines)
```

**Critical**: Always verify the exact line numbers with `grep -n` before deleting. Off-by-one errors in Python (0-indexed) vs grep (1-indexed) will corrupt the file further.

## Step 4: Verify Repair

```bash
grep -c 'kpt-symptoms-app' KNOWLEDGE-HUB.md  # Should be 1 (or expected count)
grep -c 'HANGED\|UNCHANGED\*' KNOWLEDGE-HUB.md  # Should be 0
```

## Prevention

**NEVER use `replace_all` on KNOWLEDGE-HUB.md.** Always use targeted `patch` with unique `old_string` context. If `patch` says "Found N matches" (N > 1), do NOT fall back to `replace_all` — instead:
1. Add more surrounding context to `old_string` to make it unique
2. Or use Python `read_file` + line-range deletion + `write_file`
