# Cron Status Audit — 2026-05-20

## Summary
HAL v2.0 Backend-Phase 1-5: ~85% der Backend-Arbeit implementiert. React-Frontend noch nicht gestartet.

## Key Findings

### Health Aggregation Layer (HAL)
- **health_aggregation.py**: 557 Zeilen, 17 API-Endpunkte implementiert
  - Symptom CRUD (create, list, get, update, delete, deactivate)
  - Symptom Logs (create, bulk-create, list, get)
  - Factor CRUD + Logs
  - Aggregations + Trends (OLS) + Correlations (Pearson r)
  - Reports (create, list, get, step-update, finalize)
- **i18n-Layer**: Implementiert
- **Correlation Engine**: Pearson r, Garmin-Faktoren auto-included
- **Testing**: test_health_data_generator.py + conftest_health.py + test_health_aggregation.py
- **DB-Migrations**: 7 in alembic_health (0001-0007), 0007 = HAL-Schema (30KB)

### kpt-app-ciq (Watch App)
- **171 MC-Files** auf origin/feature
- **ScreenFlow FSM**: 584 Zeilen, overlay stacking (TASK-100) implementiert
- **TODOs:**
  - TASK-101 `_canGo()` = `return true` (hardcoded), config-basierte Validation nur in merge-tag orphan chain
  - TASK-100 deprecated `method(:onOverlayTimer)` auf Zeile 595 — einziger verbliebener deprecated Call
  - TASK-042 Test Coverage: ScreenFlowConfig transition rules fehlen
- **TASKS.md stale** — delta >10 commits, nie aktualisierte COMPLETED-Claims

### Backend (kpt-backend)
- **4 alembic-Instanzen**: admin (12), activity (17), health (7), projects (3)
- **Routers**: 14 Dateien, health_aggregation.py neu (557 Zeilen)
- **BUG-015**: Plan Enforcement für Symptom-Definitionen noch nicht fixt

### kpt-symptoms-app (React Frontend)
- Leeres Submodule — noch nicht initialisiert

### Waiting List (11 Items)
- BUG-013 bis BUG-019: Limit Enforcement (Activities, Feedback-Metrics, Symptom-Tracking, Calendar, Feature-Gates, Data-Retention, Voucher)
- 3 enforce-*-count-limit Backend-Tasks

## Workflow
1. WORKLOG.md lesen (letzte Aktualisierung: 2026-05-08)
2. TASKS.md + INDEX.md lesen für aktive Tasks
3. health_aggregation.py Zeilenzahl + API-Endpunkte zählen
4. kpt-app-ciq submodule status prüfen (bare vs working tree)
5. Waiting-List-Items auflisten
