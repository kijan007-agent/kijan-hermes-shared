# Stale Data Patterns in KNOWLEDGE-HUB.md

## Pattern 1: Migration Count Drift
- Symptom: "39 migrations" when actual count is 43
- Cause: Each stack gets +1 migration, but total count not updated across all sections
- Fix: Update in ALL locations: Workflow-Verbesserungen, Cross-Product Analysis, Branch-Struktur, Sync Status table
- Detection: `grep -n 'migrations' KNOWLEDGE-HUB.md` → compare all values

## Pattern 2: Deprecated Method Count Staleness
- Symptom: "Deprecated method( 9 Instanzen" when actually 7 (4 fixed)
- Cause: Count updated in one section but not others
- Fix: Sweep ALL occurrences with grep, update each independently
- Detection: `grep -n 'Deprecated.*method' KNOWLEDGE-HUB.md`

## Pattern 3: File Existence Claims
- Symptom: "MEMORY_INDEX.md FEHLT" when file exists (35 lines)
- Cause: Previous session couldn't find file (wrong path), report persisted
- Fix: Always re-verify file existence before declaring "FEHLT"
- Detection: `find . -name 'MEMORY_INDEX.md'`

## Pattern 4: Submodule Status Staleness
- Symptom: Missing submodule entry in tables
- Cause: Submodule exists in gitmodules but not in Knowledge Hub
- Fix: Check gitmodules + working tree + Knowledge Hub tables independently
- Detection: `git submodule status` + `ls submodule_dir`

## Pattern 5: Duplicate Sections
- Symptom: Same section header appearing multiple times
- Cause: Append-based updates without checking for existing sections
- Fix: Always check for existing section before adding
- Detection: `grep -n 'Workflow-Verbesserungen' KNOWLEDGE-HUB.md`

## Pattern 6: Corrupted Lines from replace_all
- Symptom: Lines with garbled text like "UNCHANGEDHANGED**", "UNCHANGED*UNCHANGED**"
- Cause: replace_all on non-unique patterns appends to ALL matches
- Fix: Python line-range deletion (see replace-all-repair-procedure.md)
- Detection: `grep -n 'HANGED\|UNCHANGED\*' KNOWLEDGE-HUB.md`

## Pattern 7: Old Timestamp Persistence
- Symptom: 2026-07-03 timestamps remaining after update to 2026-07-08
- Cause: Only header/footer updated, not body content timestamps
- Fix: Sweep ALL `2026-07-03` (or any old date) in content with grep after update
- Detection: `grep -n '2026-07-0[3-7]' file` → should be 0 except for timestamps

## Pattern 8: File-Count Drift (Sandbox vs Reality)
- Symptom: Known file count (e.g., 23,496 py) diverges from reality (23,448 py)
- Cause: File counts change between sessions but report not updated
- Fix: Always re-count with `find . -name '*.py' | wc -l` or Python os.walk()
- Detection: Cross-reference all known counts against fresh counts

## Pattern 9: Empty Skill Category Drift
- Symptom: Skill category marked "ACTIVE" but contains no SKILL.md
- Cause: Categories created but never populated
- Fix: Run category audit: `for cat in skills/; do SKILL.md=$(find $cat -name SKILL.md); echo "$cat: $(test -f $SKILL.md && ACTIVE || EMPTY)"; done`
- Detection: 16 empty categories found in audit

## Pattern 10: Patch Tool Line-Number Prefix Leakage
- Symptom: Lines like `3|`, `4|`, `5|`, `6|`, `7|` prepended to content
- Cause: patch tool injects line-number context markers into replacement output
- Fix: After EVERY patch, run `grep -n '^[3-7]|' file` and strip first 2 chars
- Detection: Immediate post-patch grep check