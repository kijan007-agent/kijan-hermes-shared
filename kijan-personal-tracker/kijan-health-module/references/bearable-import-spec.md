# Bearable CSV Import Specification

## CSV Format
```
date | time of day | category | detail | rating/amount | notes | weekday
```

### Format-Quirks
- **date:** Ordinal format — `22nd Jan 2022` (NOT ISO 8601)
- **time of day:** Non-zero-padded — `9:05` (NOT `09:05`)
- **category:** High-level bucket — `Mood`, `Symptoms`, `Factors`, `Meds/Supplements`, `Health Measurements`, `Emotions`, `Notes`
- **detail:** Specific item — `Headache`, `Metformin 500mg`, `Anxiety`
- **rating/amount:** Numeric — scale ratings (1-10) OR absolute counts
- **Format:** One row per data point (long/tall format)

## Date Parsing
```python
import re
from datetime import datetime

ORDINAL_RE = re.compile(r"(\d+)(st|nd|rd|th)\s+(\w+)\s+(\d{4})")

def parse_bearable_date(s: str) -> datetime.date:
    m = ORDINAL_RE.match(s.strip())
    day, _, month_str, year = m.group(1), m.group(2), m.group(3), m.group(4)
    return datetime.strptime(f"{day} {month_str} {year}", "%d %b %Y").date()
```

## Time Parsing
```python
def parse_bearable_time(s: str) -> datetime.time:
    s = s.strip()
    try:
        return datetime.strptime(s, "%H:%M").time()
    except ValueError:
        return datetime.strptime(s, "%I:%M %p").time()  # AM/PM fallback
```

## Category → Kijan Entity Mapping
| Bearable Category | Kijan Target Table |
|-------------------|-------------------|
| Mood | mood_logs |
| Symptoms | symptom_logs |
| Factors | factor_logs |
| Meds/Supplements | medication_logs |
| Health Measurements | health_measurements |
| Emotions | mood_logs (emotion_tags) |
| Notes | daily notes |

## Import Flow
1. POST `/d/{device_id}/api/import/bearable` — upload CSV
2. Returns `job_id`
3. GET `/d/{device_id}/api/import/{job_id}/status` — progress
4. Response: `{status, rows_imported, rows_skipped, error_details}`
