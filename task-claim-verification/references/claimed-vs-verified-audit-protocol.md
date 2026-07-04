# Claimed-vs-Verified Audit Protocol (2026-06-08)

## When TASKS.md Claims Don't Match Reality

### Step-by-Step Verification

1. **Locate actual code** — Check `/tmp/kpt-extract/source/` first (post-wipe extraction), then `/workspace/Github/...`, NEVER trust `/data/Github/` in cron.

2. **Read actual file** — Use `read_file` on the actual file, don't rely on TASKS.md descriptions.

3. **Compare line count** — TASKS.md claims EnergyScreen = 493 lines, actual = 123 lines. If claim > actual * 2x → OVERSTATED.

4. **Check feature parity** — TASKS.md claimed EnergyScreen has: gradient background, 24h timeline, 7-day avg line, min/max band, spoon marker, quick input, legend. Actual code has: color zones + icon row. Missing: ALL chart features.

5. **Check if feature was disabled** — ScreenFlowController.mc lines 428-430, 545-553: `// DISABLED: DeltaInputScreen and EnergyScreen broken implementations removed`. Feature exists on disk but is NOT wired up.

6. **Check if feature was deleted** — DeltaInputScreen.mc does not exist anywhere. Check `find` and `git log -S` to confirm NEVER_CREATED.

7. **Check worklog recency** — Last worklog 2026-05-08. Current date 2026-06-08. Gap = 31 days. WORKLOG STALE.

### Classification Decision Tree

```
File exists on disk?
  └─ NO → Check git history for deleted?
          └─ NO → NEVER_CREATED (like DeltaInputScreen)
          └─ YES → DELETED
  
  └─ YES → Is it wired in controller?
          └─ NO (commented out) → DISABLED (like EnergyScreen in SFC:551)
          └─ YES → Check line count vs claim
                  └─ Claim > actual * 2x → OVERSTATED
                  └─ Claim ≈ actual → VERIFIED
                  
          └─ YES → Check feature completeness
                  └─ Missing >50% claimed features → PARTIAL
                  └─ All features present → COMPLETE
```

### Known False Completions (2026-06-08)

| Item | TASKS.md Claim | Actual | Classification |
|------|---------------|--------|---------------|
| EnergyScreen chart | COMPLETED, 493 lines, gradient+timeline+markers | 123 lines, color zones + icon row only | OVERSTATED |
| DeltaInputScreen | COMPLETED, 417 lines, dual mode | File NEVER existed | NEVER_CREATED |
| ScreenFlowController overlay | COMPLETED | 691 lines, full queue chain | VERIFIED ✅ |
| Transition validation | COMPLETED | fireSignal validates against mCurrent | VERIFIED ✅ |
| ActivitySession sync | COMPLETED | Deferred push + stack dedup | VERIFIED ✅ |
| TASK-105..109 docs | COMPLETED | Last worklog 2026-05-08, 31-day gap | STALE |

### Key Takeaway
TASKS.md is planning intent, not reality. Always verify COMPLETED claims by reading actual source files and comparing feature completeness against the claim. Never use TASKS.md status alone.
