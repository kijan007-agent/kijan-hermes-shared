---
name: fitbit-watch-app-debugging
description: "Debug Fitbit/Galaxy Wear OS watch apps — activity tracking bugs, queueActivity timestamp issues, Fitbit/Galaxy compatibility, activity recording, FIT session management."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [debugging, fitbit, galaxy-wearos, watch-app, activity-tracking, timestamp-bug]
---

# Fitbit/Galaxy Watch App Debugging

## Overview

Debugging Fitbit/Galaxy Wear OS watch apps requires understanding the **backend's interpretation of queued activity events** and the Fitbit/Galaxy-specific constraints around FIT sessions and activity recording.

## When to Use

- Activity duration shows as 0 on the dashboard
- Instant activity changes don't update the current activity
- Activities don't sync to the backend
- FIT session save/discard issues
- Compatibility issues between Fitbit and Galaxy devices

## Key Concepts

### queueActivity Timestamp Bug Pattern

The `queueActivity()` function in `ActivitySync` queues events for the backend. For `EV_STOP` events:

- **Index 0:** Event type (EV_STOP = 3)
- **Index 1:** **End timestamp** — used by the backend to calculate activity duration
- **Index 2:** Activity slot ID
- **Index 3:** Phase number
- **Index 4:** Duration in seconds

**CRITICAL BUG:** If index 1 (end timestamp) is passed the original session start time instead of the computed end time (`startTime + durationSeconds`), the backend calculates `end - start = 0` → duration shows as 0 on the dashboard.

**Fix:** Always compute `endTime = startTime + durationSeconds` and use it as index 1:

```
var endTime = startTime + durationSeconds;
var payload = [EV_STOP, endTime, slotId, phase, durationSeconds, ...];
```

### queueActivityUpdate (EV_UPDATE)

The `queueActivityUpdate()` function has the same parameter layout and can exhibit the same timestamp leakage if called with stale start times. Verify all call sites pass accurate timestamps.

### Instant Activity Change Flow

When the user triggers an instant activity change ("now" button):
1. `stopAndSave()` is called on the current session
2. `stopAndSave` calls `ActivitySync.queueActivity()` with the stop event
3. The old activity's duration is calculated from the EV_STOP end timestamp
4. A new session is started via `startSession()` → `queueActivityStart()`
5. The new activity record is created on the backend

**If the EV_STOP timestamp is stale, the old activity shows 0 duration and the new activity may not link properly.**

### FIT Session Management

- FIT sessions are created via `ActivityRecording.createSession()` or `ActivitySession.start()`
- On Fitbit devices, FIT sessions require specific sport/subsport config
- `mSession.isRecording()` check before stop/save is required
- `discard()` vs `save()` depends on user's FIT upload preference

## Common Debugging Steps

1. **Check the EV_STOP payload** — verify index 1 is `startTime + durationSeconds`, not just `startTime`
2. **Trace all `queueActivity()` call sites** — ensure none pass stale timestamps
3. **Check `queueActivityUpdate()` call sites** — same timestamp issue can occur for mid-session updates
4. **Verify sync queue state** — check `Storage.getValue("syncQueue")` for stuck or malformed entries
5. **Check phone connection status** — activities only queue when `System.getDeviceSettings().phoneConnected` is true

## Known File Locations (kpt-app-ciq project)

- `source/ActivitySync.mc` — queueActivity, queueActivityUpdate, EV_STOP logic
- `source/KijanActivityTrackerService.mc` — stopAndSave, startSession, createSession
- `source/ActivitySelectionDelegate.mc` — instant change mode detection
- `source/InstantActivityChangeDelegate.mc` — new activity start with time adjustment
- `source/KijanActivityTrackerView.mc` — UI state, phase transitions
