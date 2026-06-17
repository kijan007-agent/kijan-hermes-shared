# HAL Testkonzept — Automatisierte Teststrategie

## Test-Dateistruktur
```
tests/test_health_aggregation/
├── unit/ — Parser, Mapping, Aggregation (isolated)
├── integration/ — DB-Connect, Import-Flow, Report-Gen
├── api/ — FastAPI TestClient, alle Endpunkte
├── e2e/ — Bearable-Import→Report, Sync-Flow
├── conftest.py — Fixtures, DB-Pools
└── test_data/ — CSVs, seed files
```

## Test-Szenarien (test_data_generator.py)
| Szenario | Beschreibung | Daten |
|----------|-------------|-------|
| default | Realistisches ME/CFS-Profil, 30 Tage | ~3000 Logs |
| bearable | Vollständiger Bearable-Export | ~5000 Logs |
| minimal | Unit-Test-Minimal-Szenario | 10 Logs |
| edge_cases | Extremwerte, Lücken, Duplicates | 500 Logs |
| high_volume | Performance-Test | 100000 Logs |

## Testfälle pro Kategorie
- severity_mapping: none=0, ×2-Korrektur, clamping, garmin 10%-Korrektur
- bearable_parser: Ordinal-Dates, AM/PM-Zeiten, empty rows
- symptom_mapping: 20+ Mappings, unknown_symptom_detected
- aggregation: 5m/15m/1h/6h/1d/7d/30d Fenster, cascade
- trend_engine: OLS slope, r_squared, p_value
- correlation_engine: Pearson r, p_value, cache
- report: 3-Schritt-Pipeline (statistisch → KI → final)
- import: CSV-Validierung, rows_imported, rows_skipped
- sync: bulk write, conflict resolution, server_version
- i18n: DE/EN/FR/ES/IT severity_labels, symptom_names

## Ausführung
```bash
# Full: unit + integration + api + e2e mit test_data_generator
pytest tests/test_health_aggregation/ -v --generate-test-data --cov=app --cov-fail-under=90

# CI-only: unit + api
pytest tests/test_health_aggregation/unit/ tests/test_health_aggregation/api/ -v
```

## Performance-Ziele
- Aggregation 10k logs: <5s
- Trend-Engine 30 Tage: <1s
- Correlation 30 Tage: <1s
- Report-Generierung: <10s
- Import 10k rows: <30s
- Sync 100 writes: <2s