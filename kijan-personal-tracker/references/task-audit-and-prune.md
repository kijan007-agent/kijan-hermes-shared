# Task Audit & Prune Procedure

Auditing `_tasks/` directories in KijanPersonalTracker repos to identify obsolete/resolved tasks and move them to `_done/`.

## Procedure

1. **List all task files** — `ls` or Python script to enumerate all `TASK-*.md` and `*.md` in `_tasks/`
2. **Read INDEX.md** — get the full task list and structure
3. **For each task, verify against codebase:**
   - Read the task file to understand what it asks for
   - Grep/search source files for evidence of the fix/feature
   - Mark as RESOLVED (fix present) or OBSOLETE (no longer relevant)
4. **Identify remaining tasks** — those where code still lacks the fix
5. **Move obsolete/resolved tasks** — `shutil.move()` from `_tasks/` to `_tasks/_done/`
6. **Rewrite INDEX.md** — update to reflect remaining tasks only, remove stale references

## Verification Criteria

- **RESOLVED** — Code contains the fix/feature described in the task
- **OBSOLETE** — Task describes something no longer relevant (e.g., different visualization approach, acceptable trade-off)
- **STILL NEEDED** — Code still lacks the fix/feature; task remains valid

## Pitfalls

- INDEX.md often lags behind actual file state — always regenerate it after moving files
- Some tasks reference BUG-xxx files which may use different naming conventions
- Don't move tasks whose resolution is unclear — leave them for manual review
