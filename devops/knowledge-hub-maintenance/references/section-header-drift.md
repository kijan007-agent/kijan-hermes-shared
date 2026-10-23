# Section Header Drift in KNOWLEDGE-HUB.md

## Problem
Section headers in KNOWLEDGE-HUB.md drift between cron runs because updates modify them.
This makes `patch` targeting unreliable — the old_string no longer matches.

## Known Drift Patterns
| Original Header | Drifted To | Frequency |
|----------------|------------|-----------|
| `### Neue Skills` | `### Neue Skills (seit letztem Run)` | Every run |
| `### Skills-Referenz (kijan-hermes-shared, validiert YYYY-MM-DD HH:MM)` | `### Skills-Referenz (.hermes/skills, validiert YYYY-MM-DD HH:MM)` | When skills location changes |
| `### Divergenz-Analye` | `### Divergenz-Analyse` | Typos get fixed |
| `### Duplicates identifiziert und zusammengeführt` | `### Duplicates identifiziert` | Length trimmed |
| `### Neue Patterns (seit letztem Run)` | `### Neue Patterns (seit letztem Run)` | Stable |

## Detection
```bash
grep -n '^###' KNOWLEDGE-HUB.md
# Check for duplicate header text (strip trailing content)
awk -F'### ' '/^###/ {print $2}' KNOWLEDGE-HUB.md | sort | uniq -c | sort -rn | head
```

## Prevention
1. **Always read full file before patching** — never assume header format
2. **Use Python line-index targeting** — identify exact line numbers, update by index
3. **Stabilize headers** — decide on canonical header format and stick to it across runs
4. **Post-update verification** — grep all headers after any update

## Repair (if duplicates exist)
```python
content = open('KNOWLEDGE-HUB.md', 'r').read()
lines = content.split('\n')

# Find duplicate headers
from collections import Counter
headers = {}
for i, line in enumerate(lines):
    if line.startswith('### '):
        header = line.strip()
        if header in headers:
            print(f"DUPLICATE: '{header}' at lines {headers[header]+1} and {i+1}")
        headers[header] = i
```

## Structural Integrity Rules
KNOWLEDGE-HUB.md must have exactly ONE of each section:
- `### Neue Skills`
- `### Skills-Referenz`
- `### Divergenz-Analyse` (note: German spelling)
- `### Duplicates identifiziert und zusammengeführt`
- `### Neue Patterns (seit letztem Run)`

Any deviation = immediate Python rebuild required.