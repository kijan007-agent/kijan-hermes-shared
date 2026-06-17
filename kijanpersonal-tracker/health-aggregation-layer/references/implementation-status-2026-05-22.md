# HAL Implementierungsstand — 2026-05-22

## Completed

### Migration
- **alembic_health/versions/0007_health_aggregation_layer.py** (797 Zeilen)
  - Komplettes HAL-Datenmodell: symptom_definitions, symptom_logs, factor_definitions, factor_logs, mood_logs, medication_definitions/schedules/logs, health_measurements
  - health_aggregations + aggregation_metadata + correlation_cache + change_point_cache
  - import_jobs table
  - pacepoint_logs, crash_logs, infection_logs + infection_types
  - hrv_continuous_logs, breathing_sessions, funcap27_sessions, stability_scores
  - activity_impact_logs
  - Partitionierung: RANGE monthly 2026-2031 (~60 partitions/table)
  - UUIDv7 als PK-Strategy dokumentiert

### DAL (app/dal/health_dal.py — 445 Zeilen)
- **SymptomDefinitionDAL** — CRUD (create, get_by_id, get_by_user_and_id, list_by_user, update, delete)
- **SymptomLogDAL** — CRUD + bulk_create
- **FactorDefinitionDAL** — CRUD
- **HealthAggregationDAL** — create_or_update (upsert), get_aggregations
- **ReportRunDAL** — CRUD, update_status, list_by_user
- **HealthDALRegistry** — Factory mit @property Accessor für alle Repos

### Router (app/routers/health_aggregation.py — 514 Zeilen)
- **Prefix:** `/api/health`
- **Symptom-Endpunkte:** POST/GET/GET:{id}/PUT/DELETE /symptoms
- **Symptom-Log-Endpunkte:** POST /symptoms/logs, POST /symptoms/logs/bulk, GET /symptoms/logs, GET /symptoms/logs/{id}
- **Faktor-Endpunkte:** POST/GET/GET:{id}/PUT/DELETE /factors
- **Aggregations:** GET /aggregations
- **Trends:** POST /trends/calculate, GET /trends (TODO-Stubs)
- **Korrelationen:** GET /correlations (TODO-Stub)
- **Reports:** POST/GET /reports, GET /reports/{id}, PATCH /reports/{id}/step, POST /reports/{id}/finalize
- Pydantic Schemas: SymptomDefinitionCreate/Out, SymptomLogCreate/Out, BulkSymptomLogCreate, FactorDefinitionCreate/Out, HealthAggregationOut, TrendResult, CorrelationResult, ReportRunOut
- Status-Flow: drafting → statistical → ki_ready → ki_done → final

### Test-Suite
- **conftest_health.py** (66 Zeilen) — Fixtures: mock_dal_session, mock_symptom_definitions_dal, mock_health_dal
- **test_health_aggregation.py** (506 Zeilen) — Test-Pläne für TST-HAL-001 bis TST-HAL-008
- **test_health_data_generator.py** (159 Zeilen) — TestDataGenerator mit default/edge_case Szenarien

### Database
- **app/database_health.py** (27 Zeilen) — Separate AsyncSession für Health-DB

## Not Implemented (TODOs)

### Service-Layer (app/services/)
- **TrendEngine** — OLS Linear Regression + CUSUM Change-Point Detection
- **CorrelationEngine** — Pearson r zwischen Faktor→Outcome-Paaren
- **ImportService** — Bearable CSV Parser (ordinal dates), Visible CSV Parser, severity mapping (faktor-2-correction)
- **ReportService** — 3-Stufen-Pipeline (statistical → MedGemma AI → PDF)
- **AggregationEngine** — Incremental window aggregation (5m/15m/1h/6h/1d/7d/30d)
- **UnknownSymptomDetector** — 3-Phase Pipeline (Detection → Expansion → Realization)

### Router TODO-Stubs
- POST /trends/calculate — OLS Implementierung fehlt
- GET /trends — Trend-Abfrage fehlt
- GET /correlations — Correlation-Abfrage fehlt
- User-ID aus JWT extrahieren (aktuell TODO)

### ORM Models
- SQLAlchemy ORM models existieren NICHT in separater Datei
- DAL nutzt raw table metadata via session.bind.tables
- Skill SKILL.md sagt: "ORM models NOT in separate file yet"

### Missing Tables (in Migration aber nicht in DAL)
- mood_logs, factor_logs, medication_definitions/schedules/logs
- health_measurements, change_point_cache, aggregation_metadata
- pacepoint_logs, crash_logs, infection_logs/types
- hrv_continuous_logs, breathing_sessions, funcap27_sessions
- stability_scores, activity_impact_logs

## Workspace-Pfad-Hinweis
- Aktiver Workspace: `/workspace/Github/KijanPersonalTracker-hermes/`
- Specs: `/data/Github/KijanPersonalTracker-feature/kpt-doc/_specs/health-aggregation-layer/`
- Dual-Workspace-Sync nötig (dual-workspace-sync-protocol.md)
