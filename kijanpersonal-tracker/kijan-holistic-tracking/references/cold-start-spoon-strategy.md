# Cold-Start Spoon Strategy (2026-05-13)

## Problem
Individual spoon consumption per activity is unknown at the start. User has no baseline data.

## Solution: Community Median + Adaptive Learning

### Phase 1: Community Median (Days 1-3)
- Query backend for community median spoons for the activity type
- Backend API: `GET /api/symptoms/defaults?activity=walking` → `{"median_spoons": 25, "n_users": 142}`
- App displays: "Typisch: 25 spoons für diese Aktivität"
- User can adjust with +5/-5 buttons

### Phase 2: User Adjustment (Days 4-7)
- After 3 check-ins, prompt: "Passt der Spoon-Wert?"
- +/- buttons to adjust
- Store: `device.spoon_adjustment[activity_id]` = delta
- New effective value: `median + adjustment`

### Phase 3: Automatic Learning (Day 8+)
- Algorithm: `new_spoons = old_spoons + (actual_used - spent) * alpha`
- alpha starts at 0.3, decays to 0.1 over 30 days
- More weight on recent data (exponential decay)
- Minimum 7 data points before trusting the model

### Backend API
```
POST /d/{device_id}/api/spoon-learning/adjust
{
  "activity_id": 3,
  "delta": -5,
  "reason": "too_much_fatigue"
}

GET /d/{device_id}/api/spoon-learning/defaults
→ {
    "walking": {"median": 25, "n": 142, "my_adjustment": 0},
    "cooking": {"median": 15, "n": 98, "my_adjustment": -2},
    ...
  }
```

### Watch Flow
1. User starts activity
2. App fetches current spoon budget for this activity (median + adjustment or learned value)
3. Display: "~25 spoons für diese Aktivität"
4. After activity: compare spent vs actual → feed into learning

### Key Pitfalls
- Don't force onboarding quiz — high drop-off rate
- Don't start with 0 — demotivating
- Don't use a single global default — activity-specific medians are essential
- Community median should filter by user's self-diagnosis (ME/CFS vs healthy)
