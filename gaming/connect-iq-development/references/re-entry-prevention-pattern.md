# Monkey C Re-entry Prevention Pattern

> Discovered 2026-05-23 from kpt-app-ciq commit `9b2ab5f`. Universal for all Connect IQ apps with async save/commit operations.

## Problem
During async operations (e.g., saving activity, committing session), a user action or timer can trigger a duplicate call before the first one completes. This causes:
- Double-save of the same session
- Corrupted session state
- Lost energy/spoon data
- Crash on conflicting writes

## Pattern
Add a guard flag in the service/view that prevents re-entry:

```monkeyc
var mSaveInProgress as Boolean = false;

function endActivity() as Void {
    if (mSaveInProgress) {
        return;  // Guard: silently ignore re-entry
    }
    mSaveInProgress = true;
    
    // ... save logic (async callback clears flag) ...
    
    // On completion:
    mSaveInProgress = false;
}
```

## Where to apply
- Activity save/commit paths
- Spoon checkin callbacks
- Phase change confirmations
- Any async operation with user-triggerable re-entry

## Related
- See also: subclass pattern for view hierarchies (`references/subclass-pattern.md`)
