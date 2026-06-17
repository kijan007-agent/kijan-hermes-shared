# HAL v2.0 — Implementation Plan (32 Tasks, 7 Phases)

## Task IDs: HAL-P{Phase}-{Number}

### Phase 1: Backend-Basis (3 Tage, 4 Tasks)
- **HAL-P1-001**: DB-Migration (symptom_logs, factor_logs, health_aggregations)
- **HAL-P1-002**: SymptomDefinition CRUD API
- **HAL-P1-003**: Symptom/Faktor Log API
- **HAL-P1-004**: i18n-Grundlagen (severity_labels, symptom_categories)

### Phase 2: Import + Mapping (3 Tage, 5 Tasks)
- **HAL-P2-001**: Bearable CSV Parser
- **HAL-P2-002**: Severity-Mapping (none=0, faktor-2-correction)
- **HAL-P2-003**: Symptom-Mapping (Bearable → Kijan)
- **HAL-P2-004**: UnknownSymptomDetector Phase 1 (Detection)
- **HAL-P2-005**: Import Job Management

### Phase 3: Aggregation + Trends (4 Tage, 5 Tasks)
- **HAL-P3-001**: Rolling-Aggregation Engine
- **HAL-P3-002**: Aggregation-Cache (health_aggregations)
- **HAL-P3-003**: Aggregation-Invalidation (cascade)
- **HAL-P3-004**: Trend-Engine (OLS Regression)
- **HAL-P3-005**: Correlation-Engine (Pearson r)

### Phase 4: Reporting (4 Tage, 4 Tasks)
- **HAL-P4-001**: Statistische Auswertung (Bericht Schritt 1)
- **HAL-P4-002**: KI-Bericht (MedGemma Integration)
- **HAL-P4-003**: Report-Store (report_runs)
- **HAL-P4-004**: Report-Download (markdown/pdf)

### Phase 5: Sync + Cache (4 Tage, 4 Tasks)
- **HAL-P5-001**: Sync-Bulk API
- **HAL-P5-002**: Server-Side Conflict Resolution
- **HAL-P5-003**: Aggregation-Metadata Table
- **HAL-P5-004**: Change-Point-Cache

### Phase 6: Testing (3 Tage, 5 Tasks)
- **HAL-P6-001**: Testdatengenerator
- **HAL-P6-002**: Unit-Tests
- **HAL-P6-003**: API-Tests
- **HAL-P6-004**: E2E-Tests
- **HAL-P6-005**: Regressionstest-Suite

### Phase 7: React Frontend (9 Tage, 5 Tasks)
- **HAL-P7-001**: Dashboard-Component
- **HAL-P7-002**: Analytics-Page
- **HAL-P7-003**: Report-Builder
- **HAL-P7-004**: i18n-Integration (React)
- **HAL-P7-005**: Mobile-Symptom-Tracking

## Parallelization
- Phase 1: 3 parallel tasks
- Phase 2: 3 parallel tasks
- Phase 3: 3 parallel tasks
- Phase 4: 2 parallel tasks
- Phase 5: 2 parallel tasks
- Phase 6: 5 parallel tasks
- Phase 7: 3 parallel tasks

## Milestones
- M1: Backend-Basis (3 Tage)
- M2: Import-Engine (3 Tage)
- M3: Aggregation (4 Tage)
- M4: Reporting (4 Tage)
- M5: Sync + Cache (4 Tage)
- M6: Testing (3 Tage)
- M7: Frontend (9 Tage)
- **Gesamt: 32 Tasks, 30 Tage**