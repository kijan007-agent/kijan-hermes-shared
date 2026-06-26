---
name: health-aggregation-layer
description: "Health Aggregation Layer (HAL) — time-series aggregation, correlation engine, trend detection, 2-stage report generation (statistical → AI), Bearable import, and reporting pipeline for Kijan Personal Tracker health data."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [health-aggregation-layer, hal, time-series, correlation, trend, reporting, bearable-import]
---

# Health Aggregation Layer (HAL)

## Triggers
- Task involves health data aggregation beyond basic symptom/factor logging
- User mentions Bearable import, time-series resolution, trend detection, correlation
- Work on statistical reports, AI-generated health reports (MedGemma), or weekly/monthly aggregation
- Health DB (kpt-backend/alembic_health) migration or schema changes
- Symptom-to-factor correlation, Body Battery / HRV analysis

## Architecture

### Layered Design

```
Client Layer (watch/mobile/dashboard)
    ↓
Import Layer (Bearable CSV, Garmin Health API)
    ↓
Storage Layer (PostgreSQL, monthly partitions)
    ↓
Aggregation Engine (time-series windows)
    ↓
Correlation Engine (Pearson r)
    ↓
Trend Detection (OLS regression, CUSUM)
    ↓
Report Layer (statistical → AI → PDF)
```

## Data Model (Extended)

### Core Tables (existing)
**symptom_definitions** — User-defined symptoms with i18n names (de/en), category mapping
**symptom_logs** — Individual severity entries (0-10 scale), PARTITIONED BY RANGE(logged_at) monthly
**factor_definitions** — External factors (Kaffee, Schlaf, Sport, etc.)
**factor_logs** — Factor values (0-10 scale), linked to symptom correlation
**mood_logs** — Overall mood score + emotion_tags array
**medication_definitions** — Medication catalog with dosing schedule
**medication_schedules** — Planned medication (scheduled_at, frequency, custom_times)
**medication_logs** — Actual intake (actual_at, adherence_status: on_time/late/missed/partial)
**health_measurements** — Raw Garmin metrics (Body Battery, HRV, Stress, Steps)
**correlation_cache** — Pre-computed Pearson r between all factor→outcome pairs
**import_jobs** — Import job tracking (status: pending/processing/completed/failed, rows_imported)
### Aggregation Engine (continued)

### Aggregation Engine — Mobile Cache Support
- **health_aggregations** table stores all pre-computed aggregations
- **aggregation_metadata** table stores cache metadata: stale_threshold, last_computed_at, resolution_map
- **Change-point cache** (change_point_cache table): CUSUM detection results for rapid trend identification
- **Mobile cache pattern**: SQLite WAL mode on client, sync_queue FIFO, conflict resolution: last-write-wins with server_version

### Identifier Strategy (UUIDv7 vs Timestamp) — HAL v2.0 Analysis
- **UUIDv7 als PK ist die richtige Wahl** (nicht raw timestamp):
  - ✅ Garantiert eindeutiger PK (74-bit random)
  - ✅ Zeit-sorriert (48-bit Unix-Timestamp in UUIDv7[0:6])
  - ✅ Offline-Generierung auf mehreren Geräten ohne Kollision
  - ✅ Replikationssicherheit (kollisionsfrei auch bei Multi-Device)
- **TIMESTAMPTZ als Sekundärschlüssel** für Zeitreihen-Abfragen:
  - `WHERE logged_at >= start AND logged_at < end ORDER BY logged_at`
  - Aus UUIDv7 extrahierbare Zeitinformation (innerhalb 1ms)
  - **PITFALL:** Timestamp allein als ID scheitert bei hoher Frequenz (<1ms Precision) und Multi-Device-Schreiben

### Aggregation Engine

**Resolutions:** 5m, 15m, 1h, 6h, 1d, 7d, 30d

**Incremental Algorithm:**
1. New data point arrives → find current open window for each resolution
2. If window open: update sum, count, min, max incrementally
3. If window closed: create new window, full recomputation for that window
4. Cascade update to parent windows (e.g., 1h update → 6h update → 1d update)
5. Never recompute from raw logs unless window gap detected

**Metrics per window:** mean, median, std, min, max, sum, count, improvement_rate

**PITFALL:** Window gap detection — if new data arrives for a closed window's time range, mark window as invalid and recompute from raw logs. This happens when data is imported out-of-order or with time gaps.

## Identifier Strategy

**UUIDv7 recommended** over raw timestamp as ID:
- ✅ Time-sorted queries without additional index
- ✅ Globally unique across distributed systems
- ✅ Kollisionsschutz bei parallelem Import
- ✅ Better than UUIDv4 for range queries

**Timestamp as ID theoretically possible** but NOT recommended:
- ❌ Requires microsecond precision (race conditions)
- ❌ Fails with concurrent imports from multiple devices
- ❌ Cannot encode direction (improvement vs worsening) without metadata
- ✅ Only benefit: simpler queries, no index needed for time-sorted

## Correlation Engine

**Pearson r** between all factors and all symptom outcomes
- **Minimum sample size:** n ≥ 30 for statistical validity
- **Garmin factors auto-included:** Body Battery, HRV, Stress, Steps, Sleep Score
- **Cold-start advantage:** correlations available immediately via Garmin data
- **Cache strategy:** nightly recomputation, stored in correlation_cache table
- **Significance test:** p-value < 0.05 required for inclusion in reports

## Trend Detection

**OLS Linear Regression** on time-series data:
- Slope + r² per symptom per resolution
- p-value for significance (threshold: < 0.05)
- Trend direction: improving (slope < 0 for symptom severity) / worsening (slope > 0)

**CUSUM Change-Point Detection:**
- Cumulative sum of deviations from mean
- Threshold-based change-point detection
- Identifies sudden shifts in symptom patterns

**PITFALL:** OLS assumes linear trend — not valid for cyclical patterns (e.g., weekly fluctuations). Use seasonal decomposition for cyclical data.

## Report Generation (3-Stage Pipeline)

**Step 1 — Statistical Evaluation:**
1. Fetch aggregation windows for requested period
2. Compute metrics: mean, median, std, min, max, improvement_rate
3. Run correlation analysis: factor → symptom pairs
4. Run trend detection: OLS + CUSUM per symptom
5. Output: structured statistical JSON (NOT raw data)

**Step 2 — AI Report (MedGemma):**
1. Feed statistical JSON summary (NOT raw data) into MedGemma
2. Compare against previous period (month or week)
3. Generate natural language insights in German
4. Output: markdown report → PDF export

**Step 3 — Final Report Assembly:**
1. Combine statistical data + KI output + template
2. Format: markdown/PDF export
3. Status flow: drafting → statistical → ki_ready → ki_done → final
4. **PITFALL:** Feed statistical summary to AI, NOT raw data — raw data exceeds context window and increases cost.

**Multi-Step Report Generation:**
- Reports are created in multiple steps via `POST /api/health/reports/generate`
- Returns `report_id` + `status` for polling
- `GET /api/health/reports/{report_id}` returns current status + partial results
- `GET /api/health/reports/{report_id}/download` returns final file

## Bearable Import

**CSV Format:** date (ordinal), time (non-zero-padded), category, detail, rating/amount, notes, weekday
## Severity Mapping (Bearable 0-10 → Kijan 5-stufig + 10% Correction):
- **none = 0** is a REAL severity level (not missing value)
- 0 → none (0) — KEINE Korrektur (kein Symptom)
- 1-4 → bearable (1-4) — **faktor-2-correction**: severity × 2
- 5-6 → moderate (5-6) — faktor-2-correction: min(10, severity × 2) clamped to 10
- 7-8 → severe (7-8) — faktor-2-correction: min(10, severity × 2) clamped to 10
- 9-10 → extreme (9-10) — faktor-2-correction: min(10, severity × 2) clamped to 10

### 10% Correction for Garmin Sync
- `garmin_sync` source → severity × 1.1, clamped to 10
- Accounts for under-reporting in Garmin data
- **PITFALL:** Different correction per source: bearable_import uses ×2, garmin_sync uses ×1.1, native uses ×1.0 (no correction)

### Korrektur-Tabelle für alle Quellen
| Quelle | severity | Korrektur | Ergebnis |
|--------|----------|-----------|----------|
| bearable_import | 0 (none) | 0 | 0 |
| bearable_import | 1 (bearable) | ×2 | 2 |
| bearable_import | 3 (bearable) | ×2 | 6 |
| bearable_import | 5 (moderate) | ×2 | 10 |
| bearable_import | 7 (severe) | ×2 clamped | 10 |
| bearable_import | 10 (extreme) | ×2 clamped | 10 |
| garmin_sync | 5 | ×1.1 | 5 |
| garmin_sync | 7 | ×1.1 | 7 |
| garmin_sync | 9 | ×1.1 clamped | 10 |
| native (mobile/dashboard) | 5 | ×1.0 | 5 |
| native | 7 | ×1.0 | 7 |

**PITFALL:** Bearable severity 0 = none is NOT a missing value — it's a valid severity level meaning "no symptom present". Never apply factor-2-correction to severity=0.

**Symptom Mapping:** Bearable categories → Kijan categories (pain/fatigue/cognitive/mood/sleep/gastro/neuro)
**Unknown Symptoms:** UnknownSymptomDetector 3-phase pipeline (Detection → Expansion → Realization)

## Bearable Full-Feature Taxonomy (14 Categories)

Bearable tracks 14 distinct categories, NOT just symptoms/mood/factors:

| # | Bearable Category | Kijan Target | Notes |
|---|-------------------|-------------|-------|
| 1 | Symptoms | symptom_logs | severity 0-10, body_locations, duration |
| 2 | Mood | mood_logs | overall_score + emotion_tags |
| 3 | Emotions | mood_logs.emotion_tags[] | per-emotion intensity |
| 4 | Factors | factor_logs | rating (1-3 scale, not numeric amounts) |
| 5 | Meds/Supplements | medication_logs | name, dose, timing |
| 6 | Health Measurements | health_measurements | Steps, HR, BP, HRV, temp, glucose, weight |
| 7 | **Hydration** | hydration_logs | glasses/ml conversion |
| 8 | **Nutrition/Meals** | nutrition_logs | meal_type, food_tags[], portion_estimate |
| 9 | **Physical Activity** | activity_logs | type, duration_min, intensity |
| 10 | **Bowel Movements** | bowel_logs | Bristol Stool Scale (1-7) |
| 11 | **Menstrual Cycle** | menstrual_logs | phase, flow_intensity, symptoms |
| 12 | **Sleep** | sleep_logs | multi-session per day, quality, interruptions |
| 13 | **Significant Events** | significant_events | name, type, impact_score (-10 to +10) |
| 14 | **Gratitude/Reflections** | gratitude_logs | free-text content |

**PITFALL:** Bearable factors use 1-3 scale ONLY — not numeric amounts. Kijan adds numeric amounts as an improvement.

**PITFALL:** Bearable body_locations are separate symptom metadata — must be extracted from symptom detail name (e.g., "Tingling in left hand" → body_locations=["arm"]).

**PITFALL:** Bearable duration tracking is per-symptom — not captured in our initial model. Include duration_min/unit in symptom_logs.

## Visible (makevisible.com) — Komparative Analyse

**Produkt:** Wearable-First Health-Tracking (Visible Band 2.0 + App). Ziel: ME/CFS, Long Covid, Fibromyalgie, POTS, EDS.
**100k+ Mitglieder**, membership-basiert, HSA/FSA eligible. Kein öffentlicher Preis auf Website.

### Visible Unique Features (über Bearable hinaus)

| Feature | Kijan Target | Prio |
|---------|-------------|------|
| **PacePoints** (Energy Budgeting) | `pacepoint_logs` | **1** |
| **Crash/PEM Tracking** | `crash_logs` | **1** |
| **Infection type classification** | `infection_logs` + `infection_types` | **1** |
| **Continuous HRV** (Band) | `hrv_continuous_logs` | **1** |
| **Breathing exercises** (HRV-Biofeedback) | `breathing_sessions` | **1** |
| **FUNCAP27** (27-Fragen-Fragebogen) | `funcap27_sessions` | **1** |
| **Morning Stability Score** (AI) | `stability_scores` | **2** |
| **Activity impact tracking** | `activity_impact_logs` | **2** |
| **Sleep depth** (Band) | `sleep_depth` | **2** |
| **Research participation** | `research_participation` | **2** |
| **Health Summary PDF** (12mo) | `health_summary_reports` | **3** |
| **Clinician reports** | `clinician_reports` | **3** |

### Visible Check-in-Struktur

**Morning Check-in:** HRV (gemessen), RHR, Morning Stability Score, Sleep Quality, Energy, Pain, Fatigue, Cognitive Difficulty, Anxiety, Mood, Medication, Period, Infection Type, Symptom Severity, Notes

**Evening Check-in:** Pain, Fatigue, Cognitive Difficulty, Anxiety, Mood, Social Exertion, Emotional Exertion, Activity Impact, Crash, Notes

**Monthly Check-in:** FUNCAP27 (27 Fragen, Score 0-6), Symptom Overview, Medication Review, Reflections

### Visible Export-Format (CSV)

```
date,check_in_type,hrv,rhr,morning_stability_score,sleep_quality,energy,pain,fatigue,cognitive_difficulty,anxiety,mood,social_exertion,emotional_exertion,period,infection_type,crash,medication,notes,activity_type,activity_impact,pacepoints_used,pacepoints_remaining
```

**PITFALL:** Visible exportiert alle Daten in EINER CSV (kein API, kein Streaming). Parser muss flexible Spalten erkennen.

### Wettbewerbsvorteil Kijan über Visible

- Multi-Source (Garmin + Bearable + manuell) — Visible nur Band
- MedGemma KI — tiefere Analyse als PDF-Reports
- Automatisierte Korrelation — Visible nur visuelle Trends
- Open Source + Datenhoheit
- i18n — Visible nur Englisch
- Kostenlos — Visible teuer (~$30-40/mo + Band)
- UnknownSymptomDetector — automatische Model-Erweiterung

## Data Model — Erweiterte Tabellen (DM-009)

### pacepoint_logs (PARTITION BY RANGE(logged_at))
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| user_id | UUID | FK → users |
| activity_name | VARCHAR(256) | Aktivitätsname |
| pacepoints_used | INT | Verbrauchte PacePoints |
| pacepoints_remaining | INT | Verbleibend |
| symptom_impact | JSONB | {symptom_id: severity_change} |
| logged_at | TIMESTAMPTZ | PARTITION KEY |
| source | VARCHAR(32) | bearable_import, visible_import, mobile |

### crash_logs (PARTITION BY RANGE(logged_at))
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| user_id | UUID | FK → users |
| crash_start | TIMESTAMPTZ | Crash-Beginn |
| crash_end | TIMESTAMPTZ | Crash-Ende (NULL = ongoing) |
| severity | INT | 0-10 |
| trigger_factors | JSONB | ["exercise", "social", "unknown"] |
| duration_hours | FLOAT | Berechnet aus start/end |
| logged_at | TIMESTAMPTZ | PARTITION KEY |
| source | VARCHAR(32) | bearable_import, visible_import, mobile |

### infection_logs (PARTITION BY RANGE(logged_at))
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| user_id | UUID | FK → users |
| infection_type | VARCHAR(64) | FK → infection_types |
| onset_date | DATE | Symptombeginn |
| resolution_date | DATE | Auflösung (NULL = ongoing) |
| severity | INT | 0-10 |
| symptoms_json | JSONB | ["fever", "fatigue", "cough"] |
| source | VARCHAR(32) | bearable_import, visible_import, mobile |

### infection_types (Lookup)
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| code | VARCHAR(32) | COVID-19, INFLUENZA, URI, etc. |
| name_de | VARCHAR(128) | DE-Name |
| name_en | VARCHAR(128) | EN-Name |

### hrv_continuous_logs (PARTITION BY RANGE(logged_at))
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| user_id | UUID | FK → users |
| hrv_value | FLOAT | HRV in ms |
| timestamp | TIMESTAMPTZ | PARTITION KEY |
| source | VARCHAR(32) | visible_band, garmin |

### breathing_sessions
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| user_id | UUID | FK → users |
| session_start | TIMESTAMPTZ | |
| session_end | TIMESTAMPTZ | |
| duration_min | INT | |
| hrv_before | FLOAT | Vorher-HRV |
| hrv_after | FLOAT | Nachher-HRV |
| hrv_change_pct | FLOAT | ((after-before)/before)*100 |
| exercise_type | VARCHAR(64) | "coherent breathing", etc. |

### funcap27_sessions
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| user_id | UUID | FK → users |
| session_date | DATE | |
| total_score | FLOAT | 0-6 |
| question_scores | JSONB | [q1_score, q2_score, ..., q27_score] |
| notes | TEXT | |
| source | VARCHAR(32) | |

### stability_scores
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| user_id | UUID | FK → users |
| score | INT | 0-100 |
| score_date | DATE | |
| factors | JSONB | {hrv_trend: +2, sleep_quality: 7, ...} |
| source | VARCHAR(32) | visible_band, garmin |

### activity_impact_logs (PARTITION BY RANGE(logged_at))
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| id | UUIDv7 | PK |
| user_id | UUID | FK → users |
| activity_type | VARCHAR(64) | |
| symptom_id | UUID | FK → symptom_definitions.id |
| severity_change | INT | Vorher-Nachher |
| logged_at | TIMESTAMPTZ | PARTITION KEY |
| source | VARCHAR(32) | visible_import, mobile |

## UnknownSymptomDetector Pipeline (3 Phases)

### Phase 1: DETECTION (automatisch)
```python
# 1. Case-insensitive exact match
# 2. Levenshtein fuzzy match (threshold > 0.8 = known)
# 3. Semantic keyword categorization (pain/neuro/gastro/fatigue/etc.)
# 4. Body location extraction from symptom name
# 5. Auto-create suggestion generation
```

### Phase 2: MODEL-EXPANSION (semi-automatisch / KI)
```python
# 1. Cluster similar unknown symptoms (normalize body locations)
# 2. Semantic analysis for complex symptoms
# 3. Check against existing definitions (SQL ILIKE)
# 4. Optional: AI suggestion (Phi-4-mini classification)
```

### Phase 3: REALIZATION (User-Review → Auto-Commit)
```python
# 1. Present review interface (API/CLI/Web) with suggestions
# 2. User actions: accept_suggestion / edit / map_existing / skip / merge
# 3. Auto-create new SymptomDefinition or SymptomImportMapping
# 4. Re-import with new mappings
```

**Status Machine:** pending → analyzed → reviewed → (created | mapped | skipped)

**PITFALL:** Bearable dates are ordinal (e.g., "22nd Jan 2022") — parser must handle month abbreviations and ordinal suffixes.

## i18n Support

All user-facing strings must be localized:
- Symptom names (de/en)
- Factor labels
- Report templates (de/en)
- UI messages
- Error messages
- API validation messages

**Pattern:** Store i18n keys in JSON files, resolve at presentation layer. API returns keys, client resolves.

## Testing

**Test Categories:** Unit (parser, aggregation, correlation) / Integration (DB, API) / API (validation, auth) / E2E (full flow)
**Test Data Generator:** CLI tool generating realistic ME/CFS profiles with PEM patterns
**Regression:** All tests green before merge, coverage ≥ 90%, CI/CD pipeline with PostgreSQL service

## Support Files

- **`references/data-model.md`** — Complete table definitions with columns, types, indexes, partitions
- **`references/system-architecture.md`** — Layered architecture diagram, component responsibilities
- **`references/identifier-design.md`** — UUIDv7 vs timestamp-as-ID analysis
- **`references/rest-api.md`** — REST endpoint definitions for `/d/{device_id}/api/health`
- **`references/websocket-events.md`** — Real-time event channels
- **`references/async-jobs.md`** — Cron job definitions (weekly_report, monthly_report, aggregation_refresh)
- **`references/resolution.md`** — Time-series resolution engine (5m/15m/1h/6h/1d/7d/30d)
- **`references/aggregation.md`** — Incremental aggregation algorithm
- **`references/trend.md`** — OLS regression + CUSUM change-point detection
- **`references/correlation.md`** — Pearson correlation engine
- **`references/statistical.md`** — Statistical report metrics
- **`references/kai-report.md`** — AI report pipeline (MedGemma)
- **`references/scheduling.md`** — Report generation workflow and status machine
- **`references/templates.md`** — Weekly/monthly report templates
- **`references/bearable-spec.md`** — Bearable CSV format specification
- **`references/severity-mapping.md`** — Bearable 0-10 → Kijan 5-stufig mapping
- **`references/symptom-mapping.md`** — Bearable → Kijan symptom category mapping
- **`references/test-concept.md`** — Test strategy: 5 Szenarien (default, bearable, minimal, edge_cases, high_volume), pytest >90% coverage, CLI test_data_generator
- **`references/api-doc-pattern.md`** — Two-tier API documentation pattern: FastAPI Swagger auto-gen + manual markdown docs
- **`references/test-data-generator.md`** — Test data generator CLI and scenarios
- **`references/regression.md`** — Regression test execution and CI/CD pipeline
- **`references/unknown-symptom-detector.md`** — UnknownSymptomDetector 3-phase pipeline (Detection → Expansion → Realization) with status machine
- **`references/bearable-full-taxonomy.md`** — All 14 Bearable categories, data model mappings, body_locations extraction
- **`references/dual-workspace-sync-protocol.md`** — Dual workspace path resolution: /workspace vs /data filesystem mounts require explicit file sync.
- **`templates/hal-module-template.py`** — Starter template for new HAL modules (migration + DAL + API)
- **`scripts/hal-status-checker.py`** — Cron-safe HAL implementation status checker (milestone detection, code pattern matching, JSON output)
- **`scripts/test-data-generator.py`** — CLI test data generator with scenarios (default, bearable, edge-cases)
- **`references/implementation-plan-32-tasks.md`** — 🚫 DEPRECATED: 32-task plan predates SPECS.md which defines 44+ tasks across 8 milestones. Use SPECS.md as single source of truth.
- **`references/hal-v2-comprehensive.md`** — HAL v2.0 Architektur-Entscheidungen: none=0, UUIDv7 vs Timestamp, 3-Stufen-Reporting, Mobile-Cache
- **`references/implementation-workflow.md`** — 6-phase HAL implementation pattern (specs → migration → DAL → API → tests → CI/CD)
- **`references/implementation-workflow-v2.md`** — Verified 8-phase workflow with git submodule handling, dual-workspace path resolution, and verification checklist (2026-05-20)
- **`references/business-logic-reference.md`** — ⚠️ STALE: documents service layer files (correlation_engine.py, trend_engine.py, import_service.py, report_service.py, i18n_layer.py) that DON'T EXIST. Actual implementation: OLS + correlation in `app/routers/health_aggregation.py` working tree only. Service layer is Phase 3 (pending).
- **`references/kijan-frontend-spec-reference.md`** — Kijan Frontend Spezifikationen: Flutter Mobile, React Web, Pain Scale, i18n, API Mapping, Design-Tokens (Phase 3+ Frontend)
- **`references/health-aggregation-spec-2026-05-21.md`** — Full task inventory (44 tasks across 8 milestones) from SPECS.md, discrepancy with 32-task plan.
- **`references/missing-specs.md`** — Missing HAL specs (RESOLVED 2026-05-27). All 4 missing specs created.
- **`references/specs-consistency-check.md`** — Cron-safe SPECS.md manifest vs disk verification pattern (discovered 2026-05-31). **⚠️ STALE**: Manifest 2026-05-27 veraltet — 5 neue Dateien nicht erfasst. Siehe `references/specs-consistency-check-2026-06-02.md`.
- **`references/bearable-severity.md`** — Bearable Severity-Skala (0-6) mit NRS-Äquivalenten und medizinischen Standards (ICHD-3, WHO Pain Ladder).
- **`references/nrs-tools.md`** — NRS-Interpretationsleitfaden und NRS-Tools für Kijan (Visualisierung, Threshold-Alerts, Trend-Korrelation).
- **`references/implementation-status-2026-06-02.md`** — Cron-job Statusbericht 2026-06-02. SPEZIFIKATION ✅ VOLLSTÄNDIG (30 Dateien). Implementierung: ~25-30%. MILE-001 ⚠️75%, MILE-002 ✅100%. models_health.py ❌, Service Layer ❌. Migration 0007: 31 Tabellen, 60 Partitionen. Revision-Konflikt: 0007_add_energy_cost_metric.py vs 0007_health_aggregation_layer.py.
- **`references/hal-orm-gap.md`** — models_health.py ist NICHT vorhanden. DAL nutzt raw `bind.tables[]` access.

## Implementation Status (2026-06-03 09:34)

### Phase 1: DATA MODEL — COMPLETE ✅
- 31 tables, monthly partitioning, UUIDv7 PKs
- 7 alembic migrations in `alembic_health/`
- DAL: 7 classes (HealthRepository, SymptomDefinitionDAL, SymptomLogDAL, FactorDefinitionDAL, HealthAggregationDAL, ReportRunDAL, HealthDALRegistry)

### Phase 2: BUSINESS LAYER — PARTIAL ⚠️
- **ROUTER:** `app/routers/health_aggregation.py` (25,935B/760L committed + 248L uncommitted)
  - OLS regression implemented (was TODO)
  - Pearson correlation endpoint `/api/health/correlations` added
  - Statistical helpers `_normal_cdf()` + `_t_approx_pvalue()` added
- **SERVICES:** `app/services/health_aggregation/` — **DOES NOT EXIST** ❌
  - correlation_engine.py — NOT IMPLEMENTED
  - trend_engine.py — NOT IMPLEMENTED
  - report_service.py — NOT IMPLEMENTED
  - import_service.py — NOT IMPLEMENTED
  - i18n_layer.py — NOT IMPLEMENTED
- **i18n:** `app/i18n.py` (1.4KB) — 9-Sprachen JSON-Lookup ✅
- **Tests:** 11 files, 2,512 lines ✅

### Phase 3: SERVICE LAYER — PENDING ❌
- correlation_engine, trend_engine, report_service, import_service — all pending
- This is the gap between specs and reality

### Phase 4: AI REPORTING — PENDING ❌
- MedGemma AI-Report, PDF Export, Mobile Cache — not implemented

- **CRITICAL: NEVER run `git submodule update --remote` on submodules with custom commits** — this resets them to the remote branch HEAD, destroying unpushed local work (discovered 2026-05-20 during HAL implementation). Use `git submodule update --remote --merge` or manually reset with `git reset --hard <commit>` after submodule updates.
- **CRITICAL: `git submodule update` on parent repo undoes parent's submodule pointer changes** — when updating parent repo after submodule commits, update each submodule individually to the desired commit BEFORE committing the parent. Do NOT use `--recursive` on the parent repo.
- **Health DB is separate** from admin/activity/projects — migrations in `alembic_health/` only
- **Dual workspace paths**: test files written to `/data/Github/...` are NOT visible at `/workspace/Github/...`. Use `cp` or `shutil.copy2` to sync files between dual workspace paths. `/workspace/Github/KijanPersonalTracker-hermes/` is the active workspace; `/data/Github/KijanPersonalTracker-feature/` may have different content (specs, working copies). **PITFALL**: cron jobs reading specs from `/data/Github/...` while implementation is in `/workspace/Github/...` — always verify paths before comparing status.
- **Submodule commit flow**: Commit in submodule → push → `git submodule update --remote <name>` to get new HEAD → `git add <submodule>` in parent → commit parent → push parent. The `git submodule update` MUST happen AFTER the submodule push, never before.
- **Correlation cold-start** must leverage Garmin data, not wait for manual tracking accumulation
- **No plan enforcement** on symptom/factor definition creation — always call `PlanManager.enforce_limit()`
- **Aggregation window gaps** — out-of-order imports can create gaps requiring full recomputation
- **OLS assumption** — linear trend only, not valid for cyclical patterns
- **AI report cost** — feed statistical summary to MedGemma, NOT raw data
- **Bearable ordinal dates** — parser must handle "22nd Jan 2022" format with ordinal suffixes
- **UUIDv7 for distributed sync** — timestamp alone cannot guarantee uniqueness across devices
- **Visible CSV single-dump** — no API, no streaming. Must handle flexible column detection at parse time
- **Visible Bearable hybrid** — Bearable CSV and Visible CSV have different structures. Separate import pipelines required
- **PacePoints are Visible-unique** — energy budgeting concept doesn't exist in Bearable. Requires dedicated tracking table
- **FUNCAP27 is research-grade** — 27 questions per session, each stored as separate row in question_scores JSONB
- **Crash tracking is ME/CFS-specific** — Visible's crash definition is "lengths of time where illness is significantly worse"
- **Stability Score is AI-predicted** — Visible uses ML algorithm trained on 60k+ users. Can import as factor, not predict from scratch
- **Dual workspace path discovery** — When searching for backend code, check BOTH `/data/Github/KijanPersonalTracker-feature/` (specs/working copies) AND `/workspace/Github/KijanPersonalTracker-hermes/` (active workspace). Cron jobs often read specs from `/data/` but code lives in `/workspace/`. Always enumerate both paths when the expected path is not found.
