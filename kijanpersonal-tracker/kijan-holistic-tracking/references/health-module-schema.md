# Health Module Schema Reference

## Tables in health PostgreSQL instance

### symptom_definitions
```
id              INTEGER PRIMARY KEY
device_id       VARCHAR(128) — FK to devices.device_id (soft ref)
name            VARCHAR(128) — internal key (e.g., "pain", "fatigue")
display_name    VARCHAR(128) — user-visible label
category        VARCHAR(64)  — grouping category
severity_max    INTEGER      — max scale (typically 10)
is_builtin      BOOLEAN DEFAULT FALSE
is_active       BOOLEAN DEFAULT TRUE
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### symptom_logs
```
id              BIGSERIAL PRIMARY KEY
device_id       VARCHAR(128)
ts              BIGINT       — unix epoch seconds
event_timestamp TIMESTAMP WITH TIME ZONE (derived from ts)
symptom_id      INTEGER      — FK to symptom_definitions.id
severity        INTEGER      — 0 to severity_max
notes           TEXT         — optional user notes
source          VARCHAR(32)  — "watch" | "web" | "mobile"
created_at      TIMESTAMP WITH TIME ZONE
```
Partitioned monthly like health_metrics (range partition on ts).

### medication_definitions
```
id              INTEGER PRIMARY KEY
device_id       VARCHAR(128)
name            VARCHAR(128)
dosage          VARCHAR(64)  — e.g., "500mg"
unit            VARCHAR(32)  — e.g., "mg", "ml", "tabs"
color           VARCHAR(16)  — hex for UI
is_active       BOOLEAN DEFAULT TRUE
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### medication_schedules
```
id              INTEGER PRIMARY KEY
medication_id   INTEGER      — FK to medication_definitions.id
device_id       VARCHAR(128)
time_hhmm       VARCHAR(8)   — e.g., "07:00"
frequency       VARCHAR(32)  — "daily", "twice_daily", "as_needed"
days_of_week    INTEGER[]    — bitmask or array [1,2,3,4,5]
notes           TEXT
is_active       BOOLEAN DEFAULT TRUE
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### medication_logs
```
id              BIGSERIAL PRIMARY KEY
device_id       VARCHAR(128)
medication_id   INTEGER      — FK to medication_definitions.id
taken_at        TIMESTAMP WITH TIME ZONE
scheduled_at    TIMESTAMP WITH TIME ZONE (when it was due)
status          VARCHAR(32)  — "on_time" | "late" | "missed" | "skipped"
late_minutes    INTEGER      — minutes late (0 if on_time)
notes           TEXT
source          VARCHAR(32)  — "watch" | "web" | "mobile" | "reminder"
created_at      TIMESTAMP WITH TIME ZONE
```

### body_map_regions
```
id              INTEGER PRIMARY KEY
device_id       VARCHAR(128)
region          VARCHAR(64)  — e.g., "head", "lower_back", "knees"
severity        INTEGER      — 0-10
notes           TEXT
source          VARCHAR(32)
logged_at       TIMESTAMP WITH TIME ZONE
created_at      TIMESTAMP WITH TIME ZONE
```

### correlation_cache
```
id              INTEGER PRIMARY KEY
device_id       VARCHAR(128)
source_type     VARCHAR(32)  — "symptom" | "medication" | "health_metric"
source_id       INTEGER
target_type     VARCHAR(32)
target_id       INTEGER
pearson_r       FLOAT        — correlation coefficient
p_value         FLOAT        — statistical significance
observation_count INTEGER    — n used for calculation
computed_at     TIMESTAMP WITH TIME ZONE
expires_at      TIMESTAMP WITH TIME ZONE
```

### import_jobs
```
id              INTEGER PRIMARY KEY
device_id       VARCHAR(128)
import_type     VARCHAR(32)  — "bearable" | "csv" | "manual"
status          VARCHAR(32)  — "pending" | "processing" | "completed" | "failed"
file_path       VARCHAR(512) — temp file location
records_total   INTEGER
records_imported INTEGER
records_failed  INTEGER
error_message   TEXT
created_at      TIMESTAMP
completed_at    TIMESTAMP
```

### disease_catalog
```
id              INTEGER PRIMARY KEY
icd_code        VARCHAR(16)  — ICD-10-GAM code
name            VARCHAR(256) — German diagnosis name
synonyms        TEXT[]       — alternative names
related_symptoms INTEGER[]  — FK references to symptom_definitions
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

## HealthMetric (existing) — for reference
Already exists in models.py at line 517. Metric enum:
stress, hrv_rmssd, heart_rate, body_battery, spo2, effort, mood, energy, avg_stress, max_stress, body_battery_start, body_battery_end, body_battery_drain

## Key Backend Patterns

1. **Use `get_db_health()`** for all health module queries — health data lives in a separate PostgreSQL database
2. **Plan enforcement**: check `UserDefinition.max_symptomtracking` before exposing features
3. **Monthly partitioning**: new partitions must be created for future months (see 0001_health_initial.py)
4. **Soft ref pattern**: FKs to activities/devices use integer/string refs WITHOUT actual FK constraints (cross-DB references)
