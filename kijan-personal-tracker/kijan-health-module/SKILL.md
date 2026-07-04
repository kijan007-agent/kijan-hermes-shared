---
name: kijan-health-module
description: "Kijan Health Module — symptom tracking, medication planning, disease catalog (ICD-10-GAM), correlation engine, health DB design."
---

# Kijan Health Module

## Triggers
- Task involves symptom tracking, medication logging/planning, disease catalog, ICD-10, pain assessment, health DB (kpt-backend/alembic_health)
- User mentions correlation engine, Bearable import, Body Battery correlation
- Any work on health metrics beyond existing HealthMetric model

## Core Architecture

### Database
- **Location:** `kpt-backend/alembic_health/` — separate PostgreSQL instance from admin/activity/projects
- **4 existing migrations:** 0001_health_initial, 0003_add_event_timestamp_health, others
- **Partitioning:** symptom_logs, factor_logs, medication_logs, mood_logs, sleep_sessions, health_measurements → PARTITION BY RANGE(logged_at/start_at) monthly
- **New migrations:** 0004_symptom_tracking, 0005_medication_tracking, 0006_partitioning, 0007_disease_catalog, 0008_seed

### SQLAlchemy Models
- **New module:** `kpt-backend/app/models_health.py` (separate from models.py)
- **Key models:** SymptomDefinition, SymptomLog, FactorDefinition, FactorLog, MoodLog, MedicationDefinition, MedicationSchedule, MedicationLog, SleepSession, HealthMeasurement, CorrelationCache, ImportJob, DiseaseCatalog, SymptomDiseaseMapping

### API Router
- **File:** `kpt-backend/app/routers/symptom_tracking.py`
- **Prefix:** `/d/{device_id}/api/symptoms|factors|mood|medications|diseases|correlations|import`
- **Pattern:** CRUD for definitions, POST/GET for logs, adherence tracking for medications
- **Plan Enforcement:** `PlanManager.enforce_limit()` on all definition creation. Limits: basic=0, personal=0, health=50, professional=50

### Medication Tracking
- **Planning:** MedicationSchedule table with frequency (daily/bid/tid/qid/custom) + custom_times array
- **Logging:** MedicationLog with scheduled_at, actual_at, adherence_status (on_time/late/missed/partial)
- **Adherence:** on_time = within ±30min, late = >30min after, missed = no log within 2h, partial = dose != default

### Disease Catalog
- **Source:** ICD-10-GAM (InEK) — download XML/CSV, register required
- **Priority ICD codes:** G93.3 (ME/CFS), M79.7 (Fibromyalgie), G43 (Migräne), I15.9 (POTS)
- **Search:** fuzzy match on icd10_code, name_de, name_en
- **Read-only API** (seed data, no user edits)

### Correlation Engine
- **Pearson r** between all factors and all outcomes
- **Garmin factors** auto-included: Body Battery, HRV, Sleep Score, Stress, Steps
- **Cold-start advantage:** correlations available immediately via Garmin data (vs Bearable's 30-day wall)
- **Cache:** correlation_cache table for performance, nightly recomputation
- **Implemented:** health_aggregation.py (557 Zeilen, 2026-05-20), 17 API-Endpunkte

### Pain Assessment Standards
| Tool | Type | Kijan Use |
|------|------|-----------|
| **NRS (Numeric Rating Scale)** | 0-10 | **Core severity** for pain symptoms |
| **BPI (Brief Pain Inventory)** | Intensity + interference | **Weekly deep-dive template** |
| **McGill SF-MPQ-2** | Multidimensional | Optional — clinical reports |
| **PainDETECT** | Neuropathic vs nociceptive | Optional — screening filter |

### Bearable Import
- **CSV format:** date (ordinal), time (non-zero-padded), category, detail, rating/amount, notes, weekday
- **Parser:** `kpt-backend/scripts/import_bearable.py`
- **14 Bearable categories** (not just 7!): Mood, Symptoms, Emotions, Factors, Meds/Supplements, Health Measurements, Hydration, Nutrition/Meals, Physical Activity, Bowel Movements, Menstrual Cycle, Sleep, Significant Events, Gratitude/Reflections
- **Category mapping:** Mood→mood_log, Symptoms→symptom_log, Factors→factor_log, Meds/Supplements→medication_log, Health→health_measurement, Hydration→hydration_logs, Nutrition→nutrition_logs, Activity→activity_logs, Bowel→bowel_logs, Menstrual→menstrual_logs, Sleep→sleep_logs, Events→significant_events, Gratitude→gratitude_logs
- **Bearable body_locations:** Extract from detail name — e.g., "Tingling in left hand" → body_locations=["arm"]
- **Bearable duration:** symptom_logs.duration_min/unit — captured per-symptom, not in initial model
- **Full Bearable taxonomy reference:** See `health-aggregation-layer/references/bearable-full-taxonomy.md`

### UX Patterns (from Bearable assessment)
- Start with 2-3 categories, progressive reveal
- Single scrollable daily log screen (all categories)
- Correlation as killer feature — display prominently
- Custom item names (no forced taxonomy)

## Related Skills
- **`health-aggregation-layer`** — HAL für time-series aggregation, trend detection, correlation engine, 2-stage report generation, Bearable import, testing. **Implementierungs-Workflow**: Siehe `health-aggregation-layer/references/implementation-workflow.md` (6-Phasen Muster). **Vorlage**: Siehe `health-aggregation-layer/templates/hal-module-template.py`.
- `references/icd10-gam-source.md` — ICD-10-GAM download, categories, priority codes
- `references/pain-assessment-tools.md` — NRS, BPI, McGill, PainDETECT comparison
- `references/promis-measures.md` — PROMIS Pain Severity, Pain Interference, scoring
- `references/bearable-import-spec.md` — CSV format, parser, field mapping
- `references/disease-catalog-seed.md` — Priority ICD codes + symptom mappings
- `references/medical-domain-criteria.md` — ME/CFS (ICC/IOM), Fibromyalgie (ACR), POTS criteria, Komorbiditäts-Matrix, Baseline-Panel, ICD-10 priority codes
- `templates/health-task-template.md` — Template for new health module tasks
- `scripts/seed_disease_catalog.py` — Seed script skeleton (ICD-10-GAM + priority mappings)

## Pitfalls
- **Health DB is separate** from admin/activity/projects — migrations in `alembic_health/` only
- **No plan enforcement** on symptom creation (BUG-015) — always call `PlanManager.enforce_limit()`
- **kpt-app-ciq source** is bare repo — only accessible via prod-hotfix working copy path
- **TASKS.md is authoritative** — not index files or memory; always read TASKS.md for status
- **No git binary** in terminal — use host git or execute_code for repo operations
- **Correlation cold-start** must leverage Garmin data, not wait for manual tracking accumulation
- **Bearable severity=0 (none)** → Faktor-2-Multiplikator in Berechnungen anwenden, NUR bei Bearable-Import, nicht bei manueller Eingabe!
- **UnknownSymptomDetector:** Bei Bearable-Import immer UnknownSymptomDetector pipeline ausführen (Detection → Expansion → Realization). Siehe `health-aggregation-layer/references/unknown-symptom-detector.md`.
- **models_health.py MISSING (2026-06-02):** HAL DAL uses raw `bind.tables[]` access instead of SQLAlchemy ORM models. No `models_health.py` exists. This means: (1) Alembic autogenerate won't work for HAL, (2) DAL raw SQL is fragile (column name/type errors), (3) No typed API serialization. Before adding new HAL features, create `models_health.py` with ORM models for all HAL tables. See `references/implementation-status-2026-06-02.md`.
