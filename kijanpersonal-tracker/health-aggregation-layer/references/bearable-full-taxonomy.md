# Bearable Full-Feature Taxonomy

> Source: Bearable App Assessment + CSV Export Analysis (coornail.net) + samstarling/bearable-csv

## 14 Bearable Tracking Categories

| # | Category | CSV `category` Value | Kijan Target Table | Mapping Notes |
|---|----------|---------------------|-------------------|---------------|
| 1 | Mood | `Mood` | mood_logs | score=rating, emotion_tags=detail |
| 2 | Symptoms | `Symptoms` | symptom_logs | symptom_name=detail, severity=rating |
| 3 | Emotions | `Emotions` | mood_logs.emotion_tags[] | detail→emotion_tag, rating→intensity |
| 4 | Factors | `Factors` | factor_logs | factor_name=detail, value=rating |
| 5 | Meds/Supplements | `Meds/Supplements` | medication_logs | med_name=detail, dose=rating |
| 6 | Health Measurements | `Health Measurements` | health_measurements | metric=detail, value=rating |
| 7 | Hydration | `Hydration` | hydration_logs | glasses→ml (1 glass ≈ 250ml) |
| 8 | Nutrition/Meals | `Nutrition` | nutrition_logs | meal_type, food_tags[] |
| 9 | Physical Activity | `Physical Activity` | activity_logs | type, duration, intensity |
| 10 | Bowel Movements | `Bowel Movements` | bowel_logs | Bristol Stool Scale (1-7) |
| 11 | Menstrual Cycle | `Menstrual Cycle` | menstrual_logs | phase, flow, symptoms |
| 12 | Sleep | `Sleep` | sleep_logs | multi-session, quality |
| 13 | Significant Events | `Significant Events` | significant_events | name, type, impact |
| 14 | Gratitude/Reflections | `Gratitude` | gratitude_logs | free-text |

## CSV Format (All Categories)

```
date | time of day | category | detail | rating/amount | notes | weekday
```

- **date:** Ordinal format — `22nd Jan 2022` (NOT ISO 8601)
- **time of day:** `9:05` or `2:30 PM` (non-zero-padded hours)
- **category:** One of the 14 above
- **detail:** Specific item name (symptom name, food name, activity type, etc.)
- **rating/amount:** Numeric — 0-10 for severity, absolute counts for steps/amounts
- **notes:** Free text
- **weekday:** Monday..Sunday

## Known Gaps in Bearable (Kijan Advantages)

| Gap | Bearable Limitation | Kijan Advantage |
|-----|-------------------|-----------------|
| Factors | 1-3 scale only, no numeric amounts | Numeric amounts (coffee=3 cups) |
| Sleep | Single session per day | Multi-session per day |
| Body Locations | No body tag support | body_locations JSONB field |
| Duration | No symptom duration tracking | duration_min/unit in symptom_logs |
| Web/Dashboard | No web app | Full web reporting dashboard |
| PDF Export | Not yet implemented | PDF export day 1 |
| Correlation | 30-day cold start | Immediate via Garmin data |
| CSV Import | Not yet implemented | Native support |
| Garmin | No integration | Native Garmin/Body Battery |
