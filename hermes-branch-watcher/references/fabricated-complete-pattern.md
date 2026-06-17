# Fabricated Complete Pattern

> TASKS.md claims can be completely false, not just stale or overstated.

## Evidence (2026-05-21)

### TASK-020: EnergyScreen Chart
- Claim: "Chart implemented with gradient, multi-line, spoon marker, quick input"
- Reality: 80-line stub, NO chart features
- Classification: Stub vs claim

### TASK-021: DeltaInputScreen
- Claim: "DeltaInputScreen implemented"  
- Reality: File DOES NOT EXIST on any branch
- Classification: FABRICATED

## Detection Protocol
1. File exists? → No → FABRICATED
2. Line count < expected/3? → Likely stub
3. Each claimed feature present? → Missing feature → claim FALSE
4. Worklog > 3 days stale? → Treat all claims as SUSPECT
5. Branch offset > 50? → TASKS.md likely unreliable

## Classification
| Level | Description |
|-------|-------------|
| Stale | Claim was true, doc not updated |
| Overstated | Core exists, some details missing |
| Stub | Skeleton, features not added |
| Fabricated | Claim is completely false |
| Deleted | File existed then was intentionally removed |
