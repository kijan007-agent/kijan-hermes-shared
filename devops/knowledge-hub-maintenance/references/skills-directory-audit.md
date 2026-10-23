# Skills Directory Audit

When counting skills for KNOWLEDGE-HUB.md, the directory has two layouts that must both be audited.

## Layout

### Top-level categories
`.hermes/skills/` contains flat category dirs: `devops`, `gaming`, `mlops`, etc.

### Sub-directory skills
Inside each category: `<category>/<skill-name>/` (e.g., `devops/knowledge-hub-maintenance/`).

## Counting Rules

1. **Total categories:** `os.listdir(.hermes/skills/)` — count non-hidden dirs
2. **With SKILL.md:** A category counts as "with SKILL.md" if ANY `SKILL.md` exists under it (top-level or sub-dir)
3. **Hidden dirs:** `.curator_backups/`, `.hub/` — EXCLUDE from all counts
4. **Product-skill categories:** `kijan/`, `watch-app/`, `health-module/`, `website/` may be removed when no longer relevant, but kanban boards at `kanban/boards/` persist independently

## Audit Script Pattern

```python
import os
skills_dir = '/workspace/.hermes/skills'
cats = []
for entry in sorted(os.listdir(skills_dir)):
    if entry.startswith('.'):
        continue
    entry_path = os.path.join(skills_dir, entry)
    if not os.path.isdir(entry_path):
        continue
    # Check if any SKILL.md exists under this category
    has_skill = False
    for root, dirs, files in os.walk(entry_path):
        if 'SKILL.md' in files:
            has_skill = True
            break
    cats.append((entry, has_skill))
with_skill = sum(1 for _, h in cats if h)
print(f"{len(cats)} categories ({with_skill} mit SKILL.md)")
```

## Known Patterns

- Skills can be created as top-level (e.g., `state-db-cleanup/`) and later reorganized into a category (e.g., `devops/state-db-cleanup/`)
- When a skill is removed from `skills/` but its kanban board remains, note both facts separately
- Category count changes between runs are normal — consolidation and cleanup are expected
