# HAL Business Logic — ⚠️ STALE: Service layer files do NOT exist

## WARNING: This file documents code that was NEVER IMPLEMENTED

The service layer `app/services/health_aggregation/` was planned but never created.
All Phase 2 business logic lives in `app/routers/health_aggregation.py`.

## What IS Actually Implemented

### OLS Regression (BL-01 equivalent)
- Location: `app/routers/health_aggregation.py` (working tree)
- `OLSRegression`: fit() → slope, intercept, r_squared, p_value
- `TrendSignificance`: compute_p_value() via Beta-Approximation
- **PITFALL:** OLS = linear only, not for cyclical patterns
- **PITFALL:** slope = 0 bei n < 3

### Pearson Correlation (BL-02 equivalent)
- Location: `app/routers/health_aggregation.py` endpoint `/api/health/correlations`
- Pearson r between all factor→outcome pairs
- p-value via Beta-Verteilung (not normal approximation)
- **PITFALL:** Spearman nur mit n ≥ 10 sinnvoll
- **PITFALL:** Factor-Reihenfolge muss deterministisch sein

### Statistical Helpers
- `_normal_cdf()`: Abramowitz & Stegun approximation
- `_t_approx_pvalue()`: incomplete beta function
- Pure Python, no external dependencies

### i18n (BL-05 equivalent)
- Location: `app/i18n.py` (1.4KB)
- 9 languages: DE/EN/FR/ES/IT ja/nl/pt/zh-CN
- SupportedLocale Enum
- JSON-Lookup pattern

## What Does NOT Exist (documented here but NEVER implemented)

| File | Status |
|------|--------|
| `app/services/health_aggregation/correlation_engine.py` | ❌ NEVER CREATED |
| `app/services/health_aggregation/trend_engine.py` | ❌ NEVER CREATED |
| `app/services/health_aggregation/import_service.py` | ❌ NEVER CREATED |
| `app/services/health_aggregation/report_service.py` | ❌ NEVER CREATED |
| `app/services/health_aggregation/i18n_layer.py` | ❌ NEVER CREATED |

## HAL Phase 3 — Next Implementation Target

1. Create `app/services/health_aggregation/` directory
2. Implement correlation_engine.py (Pearson + Spearman)
3. Implement trend_engine.py (OLS + CUSUM)
4. Implement import_service.py (Bearable CSV parser + UnknownSymptomDetector)
5. Implement report_service.py (statistical → AI → PDF pipeline)
6. Create i18n_layer.py (separate from app/i18n.py)
7. Update router to use service layer instead of inline code
