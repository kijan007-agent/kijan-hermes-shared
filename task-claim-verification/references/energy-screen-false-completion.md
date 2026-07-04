# EnergyScreen False Completion — Specific Case

## Background
TASKS.md claimed EnergyScreen chart as COMPLETED with 493 lines. Actual: 80-line production version.

## Evidence
- **Peak chart version**: 169 lines at commit `c0fc0b1` ("enhance dashboard energy display")
- **Reverted to**: 80 lines in later commits (edf5ab8, 9bb0b5d)
- **Current version**: 80 lines — spoon count display + icon row via EnergyDrawable
- **EnergyDrawable**: 52 lines, simple filled/empty circles with color thresholds (60%/30%)
- **No gradient bands**, no multi-line graph, no spoon marker, no legend
- **Status**: ⚠️ OVERSTATED — TASKS.md claim of 493 lines is false; max historical was 169 lines

## DeltaInputScreen — NEVER_CREATED Pattern
- TASKS.md claims DeltaInputScreen at 417 lines as COMPLETED
- File NEVER existed on disk or in git history
- `git log --all --oneline -S 'DeltaInputScreen'` → nothing
- `git log --all --oneline --diff-filter=A -- '**/DeltaInputScreen*'` → nothing
- Classification: NEVER_CREATED (doc-first pattern, spec written but never implemented)

## Why Claims Are Overstated
TASKS.md uses doc-first pattern — specs written before implementation. Claims reflect
intended spec, not actual code. When auditing: always verify via `git log` line counts
and file existence, not just TASKS.md status markers.
