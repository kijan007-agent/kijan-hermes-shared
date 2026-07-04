# Monkey C Subclass Pattern for UI Views

> Discovered 2026-05-23 from kpt-app-ciq commit `b12fce2`. Replace copy-paste view hierarchies with inheritance.

## Problem
Copy-paste view hierarchies in Connect IQ apps create:
- Duplicated layout code (80+ lines per copy)
- Inconsistent behavior across copied views
- Impossible to fix in one place
- Violates Monkey C's limited memory model

## Pattern
Create a base class with common layout/state, subclass for variations:

```monkeyc
class BasePhaseView extends KijanViewBase {
    function onLayout(dc) {
        // Common layout logic
        super.onLayout(dc);
        // ... shared positioning ...
    }
    
    function initialize() {
        super.initialize();
        // ... shared initialization ...
    }
}

class ActivePhaseView extends BasePhaseView {
    function onLayout(dc) {
        super.onLayout(dc);
        // Active-specific additions only
    }
}

class RestPhaseView extends BasePhaseView {
    function onLayout(dc) {
        super.onLayout(dc);
        // Rest-specific additions only
    }
}
```

## When to apply
- Multiple views with 70%+ shared layout code
- Phase-aware UI (active vs rest vs idle)
- View hierarchies with common button/label structures
- Any copy-paste exceeding 50 lines

## Pitfall
- Monkey C has limited inheritance depth — keep hierarchies shallow (max 2 levels)
- `super()` calls must be first line in overridden functions
- Resource references (Rez.Drawables.*) must exist in the subclass's .xml too if overridden
