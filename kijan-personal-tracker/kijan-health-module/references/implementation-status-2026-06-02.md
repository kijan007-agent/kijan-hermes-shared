# HAL Implementation Status — 2026-06-02

## Current State

### ✅ Implemented (functional, deployed)
- **MILE-001 (Foundation)**: Migration 0007 (30,914 bytes) — all HAL tables created with monthly partitioning (2026-2031)
- **DAL**: `health_dal.py` (446 Zeilen) — SymptomDefinitionDAL, SymptomLogDAL, FactorDefinitionDAL, HealthAggregationDAL, ReportRunDAL + HealthDALRegistry
- **Router**: `health_aggregation.py` (515 Zeilen) — 27 Endpunkte: CRUD symptoms/factors, aggregations, trends, correlations, reports
- **Tests**: `test_health_aggregation.py` (506 Zeilen), `test_health_data_generator.py` (5,635 Zeilen)
- **Integration**: Router registered in `main.py` line 647, `engine_health` in connection pool

### ❌ Missing (blocks "live" usage)
- **models_health.py** — KEIN SQLAlchemy ORM-Modul. DAL nutzt raw `bind.tables['symptom_definitions']` access. Fragil, kein typed ORM, kein Alembic autogenerate support.
- **Mood-Log CRUD** — Tabelle existiert (Migration), aber keine DAL/Router
- **Medication CRUD** — Tabelle existiert, aber keine DAL/Router
- **HealthMeasurement CRUD** — Tabelle existiert, aber keine DAL/Router
- **Bearable Import** — TASK-I01..I06, TASK-USD01..05: CSV-Parser, Mapping-Engine, UnknownSymptomDetector
- **i18n** — Symptom-Namen i18n fehlt
- **Mobile Cache** — TASK-MC01..MC04: Sync-Endpoint, SQLite-Client-Schema
- **Frontend** — kpt-symptoms-app leer, kein Web-Dashboard

### 📊 Coverage
| Komponente | Status | Zeilen |
|------------|--------|--------|
| Migration | ✅ | 30,914 |
| DAL | ✅ (raw SQL) | 446 |
| Router | ✅ | 515 |
| Tests | ✅ | 5,635 |
| ORM Models | ❌ | 0 |
| Bearable Import | ❌ | 0 |
| Mood/Med/Measurement CRUD | ❌ | 0 |
| Frontend | ❌ | 0 |

### 🔴 Critical Gap
`models_health.py` muss erstellt werden mit SQLAlchemy-Modellen für:
- SymptomDefinition, SymptomLog, FactorDefinition, FactorLog
- MoodLog, MedicationDefinition, MedicationSchedule, MedicationLog
- HealthAggregation, CorrelationCache, ReportRun, ImportJob
- Erweiterte Tabellen: hydration_logs, nutrition_logs, activity_logs, etc.

Ohne ORM-Modelle:
- Alembic autogenerate funktioniert nicht für HAL
- DAL raw SQL ist fehleranfällig (Spaltennamen, Typen)
- Kein typed API (Pydantic kann keine ORM-Modelle serialisieren)
