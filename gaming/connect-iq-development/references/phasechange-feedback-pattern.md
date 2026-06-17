# PhaseChange Feedback — Kommunikation mit Return-Value (2026-05-17)

## Pattern: fireSignal → go + onPhaseChangeConfirmed() Return Value

**Problem**: `fireSignal(:confirmPhaseActiveToRest, {})` in `PhaseChangeToPauseDelegate` und `fireSignal(:confirmPhaseRestToActive, {})` in `PhaseChangeToActiveDelegate` ist unzuverlässig — Signal-Routing durch FSM kann fehlschlagen, besonders bei schnellen Übergängen.

**Lösung**: Return-Value Pattern statt fireSignal:

```
PhaseChangeToPauseDelegate.onSelect():
  1. popCurrent()  ← Popup wegnehmen
  2. mTrackerView.onPhaseChangeConfirmed() → Boolean
     - true:  feedback wurde gezeigt (sfc.fireSignal → spoons checkin flow)
     - false: kein feedback → confirmPhaseChange() + go(:phaseChangeToPause)
```

```
PhaseChangeToActiveDelegate.onSelect():
  1. service.confirmPhaseChange()
  2. go(:phaseChangeToActive, {:response => :yes})
```

## KijanActivityTrackerView.onPhaseChangeConfirmed()

```monkeyc
function onPhaseChangeConfirmed() as Boolean {
    // 1. feedback_mode aus ActivityTypeStore.lookup
    var feedbackMode = ActivityTypeStore.getField(dbId, "feedback_mode");
    
    // 2. needsFeedback bestimmen
    var needsFeedback = (feedbackMode == 2) || (feedbackMode == 1 && currentPhase == 0);
    
    // 3. Bei feedback: mPhaseChangeFeedbackIsActivePhase setzen + fireSignal
    if (needsFeedback && elapsedInPhase > 60) {
        mPhaseChangeFeedbackIsActivePhase = (currentPhase == 0);
        mIsPhaseChangeFeedback = true;
        var feedbackContext = (currentPhase == 0) ? :midActivity : :afterPause;
        sfc.fireSignal(:phaseChangeFeedback, {:activityTypeId, :callback, :context});
        return true;
    } else {
        mService.confirmPhaseChange();
        return false;
    }
}
```

## KijanActivityTrackerView.onMidActivityFeedback()

```monkeyc
if (mIsPhaseChangeFeedback && mPhaseChangeFeedbackIsActivePhase && pacingActive) {
    mSpoonsPacingPending = true;
    sfc.back();  // Pop feedback view
    _showMidActivitySpoonsCheckin();  // Show spoons checkin
} else {
    mService.confirmPhaseChange();
}
```

## Wichtige Regeln

1. **mPhaseChangeFeedbackIsActivePhase** muss vor fireSignal gesetzt werden — es ist ein Flag für den Callback
2. **pacingActive** wird mit `_isPacingActive()` geprüft, nicht direkt auf mService
3. **mSpoonsPacingPending** ist ein Flag für die View, dass nach Feedback ein spoons checkin folgen soll
4. **fireSignal** für `:phaseChangeFeedback` muss `{:context => :midActivity oder :afterPause}` enthalten
5. **go()** ist zuverlässiger als fireSignal für direkte Navigation
6. **popCurrent()** MUSS vor der Callback-Logik passieren, damit das Feedback-Popup weg ist

## File-Changes für dieses Pattern

| File | Änderung |
|------|----------|
| `KijanActivityTrackerView.mc` | `onPhaseChangeConfirmed()` mit Return Value, `mPhaseChangeFeedbackIsActivePhase`, `_showMidActivitySpoonsCheckin()`, `_isPacingActive()` |
| `PhaseChangeToPauseDelegate.mc` | `onSelect()`: popCurrent + onPhaseChangeConfirmed statt fireSignal |
| `PhaseChangeToActiveDelegate.mc` | `onSelect()`: confirmPhaseChange + go statt fireSignal |
