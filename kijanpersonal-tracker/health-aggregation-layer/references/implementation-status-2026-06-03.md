# HAL Implementation Status — 2026-06-03 09:34 UTC

## CRITICAL: Service Layer Does NOT Exist

The skill `health-aggregation-layer` documents `app/services/health_aggregation/` files (correlation_engine.py, trend_engine.py, report_service.py, import_service.py, i18n_layer.py) that were **never implemented**. These exist only in specs (kpt-doc/_specs/health-aggregation-layer/).

**Reality:** Phase 2 = BL-only. All business logic is in the router `app/routers/health_aggregation.py`.

## What IS Implemented (as of this check)

### Data Layer ✅
- 31 tables, monthly partitioning, UUIDv7 PKs
- 7 alembic migrations (alembic_health/)
- 7 DAL classes (HealthRepository, SymptomDefinitionDAL, SymptomLogDAL, FactorDefinitionDAL, HealthAggregationDAL, ReportRunDAL, HealthDALRegistry)

### Router ✅
- `app/routers/health_aggregation.py` (25,935B / 760L committed + 248L uncommitted)
- OLS regression (was TODO → now implemented)
- Pearson correlation endpoint `/api/health/correlations`
- Statistical helpers `_normal_cdf()`, `_t_approx_pvalue()`
- 22+ API endpoints

### i18n ✅
- `app/i18n.py` (1.4KB) — 9-Sprachen JSON-Lookup

### Tests ✅
- 11 test files, 2,512 lines

## What is NOT Implemented

- correlation_engine.py
- trend_engine.py
- report_service.py
- import_service.py
- i18n_layer.py (separate from app/i18n.py)
- MedGemma AI-Report
- PDF Export
- Mobile Cache
- CUSUM Change-Point Detection
- Rolling Aggregation
- models_health.py (DAL uses raw SQL)

## kpt-backend Status
- HEAD: `3b3cb3a`
- Unmerged vs origin/dev: 12 commits
- **Unmerged vs origin/hermes: 2 commits** (CHANGED: 0→2)
  - `3b3cb3a` Merge origin/feature
  - `0a07455` Merge PR #30 from kijan007/prod

## Next Action
HAL Phase 3 — Implement service layer (correlation_engine, trend_engine, report_service, import_service) + merge kpt-backend to origin/hermes
