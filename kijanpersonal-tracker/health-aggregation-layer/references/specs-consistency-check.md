# SPECS.md Manifest Consistency Check

## Pattern (cron-safe)

When verifying HAL spec completeness:

1. **Parse SPECS.md section 4** ("DATEIEN IN DIESEM ORDNER") to extract the manifest table
2. **Walk the spec directory** recursively, collecting all `.md` files
3. **Compare** manifest entries against actual files
4. **Flag**: missing files (manifest says exist → disk doesn't), extra files (disk has → manifest doesn't)
5. **Update** SPECS.md header status accordingly

## Discovered Extra Files (2026-05-31)

The following files exist on disk but are NOT in SPECS.md manifest:

| Datei | Beschreibung |
|-------|-------------|
| `comparative/bearable-vs-visible.md` | Bearable vs Visible comparative analysis |
| `comparative/research-summary.md` | Research summary |
| `import/visible-export-spec.md` | Visible export CSV format spec |
| `references/bearable-severity.md` | Bearable severity scale reference |
| `references/nrs-tools.md` | NRS interpretation guide |

These are valid additions — either add to SPECS.md or note as out-of-scope.

## Implementation Note

Use `os.walk()` in Python for cron jobs (no shell dependency). Filter by `.md` extension. Normalize paths with `os.path.relpath()`.

## SPECS.md Header Status Values

- `✅ VOLLSTÄNDIG` — all manifest files present, no critical gaps
- `⚠️ TEILWEISE` — some missing or inconsistencies
- `❌ LÜCKENHAFT` — critical files missing
