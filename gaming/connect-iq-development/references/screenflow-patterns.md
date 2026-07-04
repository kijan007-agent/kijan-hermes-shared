# ScreenFlow FSM — Overlay & Transition Patterns

## TASK-100: Overlay Queue Implementation (ScreenFlowController.mc)

### Fields to add
```monkeyc
var mPendingScreen as Symbol;
var mPendingScreenParams as Dictionary or Null;
```

### go() modification
```monkeyc
function go(screen as Symbol, params as Dictionary or Null) as Void {
    if (mScreenFlowState == :overlay) {
        // Defer: queue for later
        mPendingScreen = screen;
        mPendingScreenParams = params;
        return;  // DO NOT push screen now
    }
    // ... normal transition logic ...
}
```

### onOverlayTimer() flush
```monkeyc
function onOverlayTimer() as Void {
    // ... existing overlay chain logic ...
    if (mScreenFlowState == :idle && mPendingScreen != null) {
        go(mPendingScreen, mPendingScreenParams);
        mPendingScreen = null;
        mPendingScreenParams = null;
    }
}
```

### Key insight
The overlay chain (multiple auto-dismiss overlays) must fully drain before the next screen push. Without this, the second overlay's `onOverlayDismiss()` fires while the first overlay is still active, causing UI corruption.

## TASK-101: Default-Deny Transition Validation (ScreenFlowController.mc)

### _canGo() implementation
```monkeyc
private function _canGo(currentScreen as Symbol, nextScreen as Symbol) as Boolean {
    // Check direct transition
    var rule = ScreenFlowConfig.getRule(currentScreen, :nextScreen);
    if (rule != null && rule.hasKey(nextScreen)) {
        return true;
    }
    // Check conditional transitions (:yes/:no)
    rule = ScreenFlowConfig.getRule(currentScreen, :onYes);
    if (rule != null && rule.hasKey(nextScreen)) { return true; }
    rule = ScreenFlowConfig.getRule(currentScreen, :onNo);
    if (rule != null && rule.hasKey(nextScreen)) { return true; }
    return false;  // Default deny
}
```

### Key insight
Must validate against `currentScreen` (the actual active screen), NOT `fromScreen` (which may be stale). A transition from `:dashboard` to `:feedback` might be valid, but if the actual current screen is `:overlay`, it's not.

## ActivitySession State Sync (TASK-102)

### Fields to add
```monkeyc
var mCurrentSessionInfo as Dictionary or Null;
var mSessionDirty as Boolean = false;
var mSessionChangeTimerId as Number = 0;
```

### Sync pattern
```monkeyc
function onShowActivityTrackerView() as Void {
    var session = ActivitySession.get();
    if (session != null) {
        mCurrentSessionInfo = {
            :type => session.getType(),
            :label => session.getLabel(),
            :activeDuration => session.getActiveDuration(),
            :restDuration => session.getRestDuration(),
            :isActive => ActivitySession.isActive()
        };
    } else if (mService.isSessionActive()) {
        // Service has session but ActivitySession hasn't been set yet
        // Fetch from service directly
    }
}

private function onActivitySessionChange() as Void {
    if (mSessionChangeTimerId != 0) { AppTimer.cancel(mSessionChangeTimerId); }
    mSessionChangeTimerId = AppTimer.after(100, self, :_flushSessionSync);
}
```

### Pitfall
Cold start: service may create session before view calls `ActivitySession.start()`. Always check BOTH `ActivitySession.get()` AND `service.isSessionActive()` on cold start.