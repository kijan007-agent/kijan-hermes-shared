# Broken Features Removal Pattern — Confirmed 2026-06-03

## EnergyScreen Chart
- **Status**: Replaced stub at commit `9bb0b5d` (after 493-line chart at `972f55f`)
- **Current**: 123-line stub in `/workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq/source/EnergyScreen.mc`
- **Chart exists**: Only on merge tag `merge-feature-to-hermes_20260518_064319`, NOT on any branch
- **Classification**: ⚠️ Was implemented, replaced by stub, chart exists only on merge tag

## DeltaInputScreen (Quick Input)
- **Status**: DISABLED in ScreenFlowController.mc (lines 428-429)
- **File exists**: NEVER existed on any reachable branch — code was commented out before first commit
- **ScreenFlowController line 428**: `// DISABLED: DeltaInputScreen and EnergyScreen broken implementations removed`
- **Classification**: ❌ Never deployed — planning intent only, never committed
- **Route exists**: `:deltaInput` in ScreenFlowConfig but `:createView` returns null

## Re-implementation Checklist
If re-implementing EnergyScreen chart:
1. Restore from merge tag: `git show merge-feature-to-hermes_20260518_064319:source/EnergyScreen.mc`
2. OR implement from scratch — stub is 123 lines, chart was 493
3. Wire up in ScreenFlowController `_createView()` (uncomment lines 428-430)
4. Wire up in ScreenFlowConfig for `:energyScreen` route
5. Register in InitScreens.mc when condition met (unit_mode != "disabled")

If re-implementing DeltaInputScreen:
1. File never existed — design only
2. Must implement from scratch
3. Would need: numeric input view, delegate, ScreenFlowController wiring
4. ScreenFlowController already has disabled stub code (lines 428-429, 545-549)
5. Would need to remove comments and implement the actual class

## Classification Matrix
| Pattern | Detection | Classification |
|---------|-----------|---------------|
| Implemented then stubbed | `git log --ancestry-path` shows full→stub | ⚠️ Replaced |
| Implemented then deleted | `git log --diff-filter=D` | ⚠️ Was implemented, later deleted |
| On tag only | `git branch -a --contains <sha>` | 📦 Tag-only |
| Never existed | File not in any commit/branch/tag | ❌ Never deployed |
| Disabled on disk | Commented out in controller | ⏳ Disabled |
