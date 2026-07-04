# Branch Diff Workflow (Hotfix → Feature Porting)

## When to Use
When a feature branch has broken UI (overlapping popups, wrong flows, missing screens) but `prod-hotfix-bat` has working code. Use this workflow to systematically analyze and port changes.

## Step 1: File-by-File Comparison

```bash
# Define key UI files
FILES=(
  "KijanActivityTrackerApp.mc"
  "ScreenManager.mc"
  "EnergyScreen.mc"
  "MorningCheckinView.mc"
  "PacingSpoonsCheckinView.mc"
  "BasePopupView.mc"
  "InstantChangePopupView.mc"
  "ExitConfirmationPopupView.mc"
  "ScreenFlowController.mc"
  "ScreenFlowConfig.mc"
)

for f in "${FILES[@]}"; do
  prod="/path/to/prod-hotfix/kpt-app-ciq/source/$f"
  feat="/path/to/feature/kpt-app-ciq/source/$f"
  if ! test -f "$prod" && ! test -f "$feat"; then
    echo "❌ $f: Missing in both"
  elif ! test -f "$prod"; then
    echo "➕ $f: Feature only (new)"
  elif ! test -f "$feat"; then
    echo "➖ $f: Missing in Feature (needs porting)"
  elif ! diff -q "$prod" "$feat" > /dev/null 2>&1; then
    echo "🔄 $f: DIFFER (needs review/porting)"
  else
    echo "✅ $f: Identical"
  fi
done
```

## Step 2: Categorize Findings

| Category | Files | Action |
|----------|-------|--------|
| Missing in Feature | MorningCheckinView, etc. | Port from prod-hotfix |
| Different | ScreenManager, EnergyScreen | Compare diffs, port fixes |
| Feature-only | ScreenFlowController, PacingSpoonsCheckinView | Integrate into flow |
| Identical | BasePopupView, YesNoPopupView, etc. | No action needed |

## Step 3: Create Tasks

- One `TASK-*.md` file per distinct fix/integration
- Each task: User Story, Problem (specific to this project), To-Do (numbered)
- Update `INDEX.md` with a "NEW" section
- Create worklog in `kpt-doc/_worklogs/WORKLOG.md`

## Pitfalls

- **Don't just copy-paste**: Adapt to feature branch's new architecture (ScreenFlowController vs old ScreenManager)
- **Check dependencies**: New screens may need new resources (PNGs, strings, layouts)
- **Validate order**: Port P0 (popup stack, view validity) before P1 (new features)
- **Test on simulator after each batch**, not just at the end