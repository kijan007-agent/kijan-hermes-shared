# Connect IQ UX Fix Patterns — From Hotfix to Feature Branch

## Problem #1: Overlapping Popups

### Root Cause
No popup lifecycle management, stale delegate references after screen transitions.

### Fix — View Validity Guard Pattern

Add to every manager/delegate that creates popups:
```mc
private var mViewId as Number = 0;
function setViewId(viewId as Number) { mViewId = viewId; }
function getViewId() as Number { return mViewId; }
function isViewValid() as Boolean { return mViewId != 0; }
function invalidateView() as Void { mViewId = 0; }
```

Apply in popup callbacks BEFORE any action:
```mc
function onConfirm(value as Number) as Void {
    if (mManager != null && mManager.isViewValid()) {
        mManager.onCheckinConfirmed(value);
    }
}
function onReject() as Void {
    if (mManager != null && mManager.isViewValid()) {
        mManager.onCheckinRejected();
    }
}
```

In the View's destroy():
```mc
function destroy() as Void {
    if (mStatusCheckManager != null) {
        mStatusCheckManager.invalidateView();
    }
    View.destroy();
}
```

## Problem #2: Wrong Navigation After Popup Action

### Root Cause
Callbacks fire on stale delegate, wrong screen shown after confirmation.

### Fix — Popup Stack Management

In ScreenFlowController.mc:
```mc
private var mActiveDelegate as Object? = null;
private var mPopupStack as Array = [];

function setActivePopup(delegate as Object) as Void {
    if (mActiveDelegate != null && mActiveDelegate has :invalidate) {
        mActiveDelegate.invalidate();
    }
    mPopupStack.add(delegate);
    mActiveDelegate = delegate;
}

function clearPopupStack() as Void {
    for (var i = 0; i < mPopupStack.size(); i++) {
        var del = mPopupStack[i];
        if (del != null && del has :invalidate) { del.invalidate(); }
    }
    mPopupStack = [];
    mActiveDelegate = null;
}

function popPopup() as Void {
    if (mPopupStack.size() > 0) {
        mPopupStack.remove(mPopupStack.size() - 1);
        mActiveDelegate = (mPopupStack.size() > 0) ? mPopupStack[mPopupStack.size() - 1] : null;
    }
}
```

## Problem #3: ScreenRenderer Not Displaying

### Root Cause
EnergyScreen (extends ScreenRenderer) not registered in InitScreens.mc.

### Fix
In InitScreens.mc `onAppLoaded`:
```mc
if (unitMode != null && !unitMode.equals("disabled")) {
    mScreens.add(new EnergyScreen(this));
}
```

Ensure EnergyScreen is imported at top of file.

## Problem #4: Spoon Icons Not Showing

### Root Cause
drawables.xml missing SpoonGreen/SpoonYellow/SpoonRed bitmap definitions, PNGs not in resources.

### Fix
1. Copy PNGs: `spoon-green.png`, `spoon-yellow.png`, `spoon-red.png` to `resources/drawables/`
2. Add to `resources/drawables/drawables.xml`:
```xml
<bitmap id="SpoonGreen" filename="spoon-green.png" dithering="none" />
<bitmap id="SpoonYellow" filename="spoon-yellow.png" dithering="none" />
<bitmap id="SpoonRed" filename="spoon-red.png" dithering="none" />
```

## Problem #5: Chart Interpolation Bugs

### Root Cause
prevH can go negative, causing index errors or incorrect interpolation.

### Fix — Robust Interpolation
```mc
private function _interpolateChecksTo24Hours(checks as Array) as Array {
    var hourly = [];
    for (var h = 0; h < 24; h++) { hourly.add(-1); }

    if (checks.size() == 0) { return hourly; }

    // Place actual values
    for (var i = 0; i < checks.size(); i++) {
        var hourOfDay = (((checks[i].getTimestamp() + offset) % 86400) / 3600).toNumber();
        if (hourOfDay >= 0 && hourOfDay < 24) {
            hourly[hourOfDay] = checks[i].getSpoonsValue();
        }
    }

    // Forward fill
    for (var h = 0; h < 24; h++) {
        if (hourly[h] == -1) {
            var nextH = h + 1;
            while (nextH < 24 && hourly[nextH] == -1) { nextH++; }
            if (nextH < 24) {
                var prevH = h - 1;
                while (prevH >= 0 && hourly[prevH] == -1) { prevH--; }
                if (prevH >= 0) {
                    var progress = (h - prevH).toFloat() / (nextH - prevH).toFloat();
                    hourly[h] = (hourly[prevH] + (hourly[nextH] - hourly[prevH]) * progress).toNumber();
                }
            }
        }
    }

    // Backward fill remaining
    for (var h = 0; h < 24; h++) {
        if (hourly[h] == -1) {
            var prevH = h - 1;
            while (prevH >= 0 && hourly[prevH] == -1) { prevH--; }
            if (prevH >= 0) { hourly[h] = hourly[prevH]; }
        }
    }

    // Final fallback
    for (var h = 0; h < 24; h++) {
        if (hourly[h] == -1) { hourly[h] = 15; }
    }

    return hourly;
}
```

## Problem #6: Color Zones Not Implemented

### Root Cause
Chart background drawn as single color, no zone differentiation.

### Fix — Zone Drawing
In EnergyDrawable.mc:
```mc
static function drawZoneBackground(dc, x, y, w, h, maxSpoons, zoneStart, zoneEnd, zoneColor) {
    if (zoneStart >= zoneEnd) { return; }
    var yTop = y + h - ((zoneEnd / maxSpoons) * h);
    var yBot = y + h - ((zoneStart / maxSpoons) * h);
    dc.setColor(zoneColor, Graphics.COLOR_TRANSPARENT);
    dc.fillRectangle(x + 1, yTop, w - 2, yBot - yTop);
}
```

In EnergyScreen._draw24HourGraph():
```mc
// 0-10 red zone
EnergyDrawable.drawZoneBackground(dc, graphX, graphY, graphWidth, graphHeight, maxSpoons, 0, 10, Graphics.COLOR_RED);
// 10-20 yellow zone
EnergyDrawable.drawZoneBackground(dc, graphX, graphY, graphWidth, graphHeight, maxSpoons, 10, 20, Graphics.COLOR_YELLOW);
// 20-30 green zone
EnergyDrawable.drawZoneBackground(dc, graphX, graphY, graphWidth, graphHeight, maxSpoons, 20, 30, Graphics.COLOR_GREEN);
```
