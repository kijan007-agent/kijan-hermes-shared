# Multi-Step Maintenance Task Pattern

When a cron job runs a multi-step maintenance task (Knowledge Hub update, system health scan, skill creation):

## Standard Sequence

1. Read the target document (KNOWLEDGE-HUB.md, config, etc.)
2. Scan active systems (kanban boards, file counts, db sizes, etc.)
3. Analyze findings — compare against stored state (check for drift)
4. Identify cross-product patterns (duplicates, trends, skill opportunities)
5. Execute updates (patch files, create skills, update status)
6. Verify integrity (grep for lost sections, check file validity)
7. Report changes concisely (no fluff, just facts and action items)

## Pitfalls

- Kanban boards may be empty — don't assume active work; focus on system health
- state.db growth can accelerate (observed: +4.4 MB per run) — set thresholds and alerts
- Knowledge Hub reports become stale quickly (100% stale within a few runs) — always re-scan fresh
- After creating skills, update KNOWLEDGE-HUB.md skill_recommendations table with ✓ CREATED status
- patch tool can leak line-number prefixes on markdown files — always grep for `^[1-9]|` after patch
- Section headers can drift between runs — always read full file before patching, verify headers post-update
