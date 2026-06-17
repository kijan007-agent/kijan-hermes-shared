# queueActivity / queueActivityUpdate Payload Structure

## queueActivity (EV_STOP events)

Backend payload array — each index has a specific meaning:

| Index | Field | Backend Interpretation |
|-------|-------|------------------------|
| 0 | Event type (EV_STOP=3) | Event classification |
| **1** | **End timestamp** | **Duration = end_ts - start_ts on backend** |
| 2 | Slot ID | Activity type/slot |
| 3 | Phase | Active or rest phase |
| 4 | Duration seconds | Display duration (may be redundant) |
| 5+ | Health metrics | Stress, body battery, etc. |

## queueActivityUpdate (EV_UPDATE events)

| Index | Field | Notes |
|-------|-------|-------|
| 0 | EV_UPDATE=2 | |
| 1 | Activity ID | Backend record to update |
| 2 | Start time | Session start epoch |
| 3 | Duration seconds | Elapsed duration |
| 4+ | Health metrics | avgStress, maxStress, bbStart, bbEnd, rmssd |

## Bug Pattern: Stale End Timestamp

When `queueActivity()` is called from `stopAndSave()` during an instant activity change:
- The caller passes `startTime = session_start_time` (original session start)
- The caller passes `durationSeconds = elapsed_seconds`
- If the payload's index 1 is set to `startTime` (the original start), the backend computes:
  - `duration = startTime - startTime = 0`

**Correct payload construction:**
```
var endTime = startTime + durationSeconds;
var payload = [EV_STOP, endTime, slotId, phase, durationSeconds, ...];
```

This ensures the backend can compute the actual duration regardless of what the caller passed as `startTime`.
