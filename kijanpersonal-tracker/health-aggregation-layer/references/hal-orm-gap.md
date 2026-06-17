# HAL ORM Gap — models_health.py Missing

## Problem (2026-06-02 confirmed)

HAL (Health Aggregation Layer) has NO SQLAlchemy ORM models. Despite 30,914-line migration (0007) creating all tables, the DAL (`health_dal.py`, 446 Zeilen) uses raw `bind.tables['symptom_definitions']` access instead of typed ORM models.

## Impact

1. **Alembic autogenerate broken** — no models to diff against
2. **DAL fragile** — column name/type errors at runtime only
3. **No typed API** — Pydantic can't serialize ORM models that don't exist
4. **Migration drift risk** — no code-level schema validation

## Current State

| File | Status | Lines |
|------|--------|-------|
| Migration 0007 | ✅ | 30,914 |
| health_dal.py | ✅ (raw SQL) | 446 |
| health_aggregation.py router | ✅ | 515 |
| **models_health.py** | **❌ MISSING** | **0** |

## Required ORM Models

`app/models_health.py` must define:
- SymptomDefinition, SymptomLog (partitioned)
- FactorDefinition, FactorLog (partitioned)
- MoodLog, MedicationDefinition, MedicationSchedule, MedicationLog
- HealthAggregation (partitioned), CorrelationCache, ReportRun, ImportJob
- Extended: hydration_logs, nutrition_logs, activity_logs, bowel_logs, menstrual_logs
- sleep_logs, significant_events, gratitude_logs, health_measurements

## Tables Covered by Migration 0007

symptom_definitions, symptom_logs, factor_definitions, factor_logs, mood_logs,
medication_definitions, medication_schedules, medication_logs, health_metrics,
health_aggregations, correlation_cache, change_point_cache, import_jobs,
import_job_details, symptom_import_mappings, unknown_symptom_queue,
aggregation_metadata, report_runs, pacepoint_logs, crash_logs, infection_logs,
infection_types, hrv_continuous_logs, breathing_sessions, funcap27_sessions,
stability_scores, activity_impact_logs, research_participation

## Fix Priority

**P0** — models_health.py erstellen, dann:
1. DAL rewrite to use ORM
2. Alembic autogenerate validation
3. Pydantic schema integration
4. Missing CRUD (Mood, Medication, HealthMeasurement)
5. Bearable Import (TASK-I01..I06)
6. UnknownSymptomDetector (TASK-USD01..05)
