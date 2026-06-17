# HAL v2.0 — Comprehensive Architecture (2026-05-20)

## Key Architecture Decisions

### 1. Severity Scale: none = 0
Bearable severity 0 is a REAL value (no symptom), not missing data.
- 0 → none (0) — no correction
- 1-4 → bearable — factor ×2 (clamped to 10)
- 5-6 → moderate — factor ×2 (clamped to 10)
- 7-8 → severe — factor ×2 (clamped to 10)
- 9-10 → extreme — factor ×2 (clamped to 10)

### 2. Source-Specific Correction
- bearable_import: severity × 2 (scale mapping)
- garmin_sync: severity × 1.1 (10% under-reporting)
- native (mobile/dashboard): severity × 1.0 (no correction)

### 3. UUIDv7 as Primary Key (not raw timestamp)
- 48-bit Unix timestamp embedded in UUIDv7[0:6]
- Guaranteed uniqueness across distributed systems
- Multi-device offline sync without collision risk
- Timestamp stored as separate TIMESTAMPTZ column for range queries

### 4. 3-Stage Reporting Pipeline
1. Statistical evaluation (metrics, trends, correlations)
2. AI report generation (MedGemma) — takes statistical JSON as input
3. Final report assembly — combines stats + AI output + template

### 5. Mobile Cache Pattern
- SQLite WAL mode on device
- sync_queue FIFO for pending writes
- Last-write-wins with server_version for conflict resolution
- Cache invalidation via stale_threshold in aggregation_metadata

### 6. Aggregation Resolutions
5m, 15m, 6h, 1d, 7d, 30d — cascading parent windows

### 7. i18n Coverage
All user-facing strings: severity labels, symptom names, factor labels, report templates, error messages — supported in DE, EN, FR, ES, IT

### 8. Testing Strategy
- 5 test scenarios: default, bearable, minimal, edge_cases, high_volume
- Test data generator CLI: `python test_data_generator.py`
- Regression suite: pytest with >90% coverage target
- E2E: bearable import → report generation, sync flow