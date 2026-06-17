# Health Aggregation Layer — Spec Task Inventory (2026-05-21)

Source: `/data/Github/KijanPersonalTracker-feature/kpt-doc/_specs/health-aggregation-layer/SPECS.md`

## Status: SPECS.md exists (implementation NOT started)
- 25 spec files in 9 subdirectories (130 KB total)
- Feature branch at `/data/Github/KijanPersonalTracker-feature/` has ZERO commits — all work is uncommitted working tree
- Only test skeleton files exist in hermes repo (kpt-backend/tests/) — no DAL, models, or routers implemented

## Full Task Inventory (44 unique tasks across 8 milestones)

### MILE-001 Foundation (TASK-F01..F04)
- TASK-F01: DB-Migration 0007 (Partitioning + neue Tabellen)
- TASK-F02: Health-Modelle (models_health.py)
- TASK-F03: Base-Repositories (dal/health_repositories.py)
- TASK-F04: Router-Setup (routers/health_aggregation.py)

### MILE-002 Core CRUD (TASK-C01..C06)
- TASK-C01: SymptomDefinition CRUD
- TASK-C02: SymptomLog CRUD + Partitioning-Pruning
- TASK-C03: FactorDefinition + FactorLog CRUD
- TASK-C04: MoodLog CRUD
- TASK-C05: MedicationDefinition + Schedule + Log CRUD
- TASK-C06: HealthAggregation CRUD

### MILE-003 Import (TASK-I01..I06, USD01..USD05)
- TASK-I01: Bearable CSV-Parser
- TASK-I02: Category → Kijan Mapping Engine
- TASK-I03: Bearable Severity-Skala Integration (none=0)
- TASK-I04: Async-Import-Job + Status-Tracking
- TASK-I05: Fuzzy-Matching für Symptom-Namen
- TASK-I06: Dedup-Logik (timestamp ID)
- TASK-USD01: UnknownSymptomDetector (Detection Engine)
- TASK-USD02: ModelExpansionService (Cluster + Semantik + KI)
- TASK-USD03: RealizationService (User-Review + Auto-Commit)
- TASK-USD04: unknown_symptom_queue + Status-Machine
- TASK-USD05: Vollständiger Import-Flow mit UnknownDetection

### MILE-004 Time-Series (TASK-TS01..TS05)
- TASK-TS01: Resolution-Engine (5m/15m/1h/6h/1d/7d/30d)
- TASK-TS02: Rolling Aggregation (mean/median/min/max/count/std)
- TASK-TS03: Time-Zone-Korrektur + UTC-Canonicalisierung
- TASK-TS04: Mobile-Device Cache-Protokoll (sync window)
- TASK-TS05: Aggregation Cache Table

### MILE-005 Trend & Correlation (TASK-TR01..TR05)
- TASK-TR01: Pearson-Korrelation Engine
- TASK-TR02: Lineare Regression für Trendermittlung
- TASK-TR03: Change-Point-Detection (CUSUM)
- TASK-TR04: Korrelations-Cache + Nightly-Recompute
- TASK-TR05: Garmin-Faktor-Integration (Body Battery etc.)

### MILE-006 Reports (TASK-RP01..RP06)
- TASK-RP01: Statistische Auswertung (Schritt 1)
- TASK-RP02: KI-Report-Generierung MedGemma (Schritt 2)
- TASK-RP03: Mehrstufige Report-Erstellung (Stateful)
- TASK-RP04: Wochen-/Monatsbericht-Template
- TASK-RP05: PDF/Markdown-Export
- TASK-RP06: Report-Scheduling + Cron

### MILE-007 i18n & Testing (TASK-I18N01..02 + TASK-MC01..MC04)
- TASK-I18N01: i18n-Schlüsselkonvention + JSON-Struktur
- TASK-I18N02: Symptom-Namen i18n
- TASK-MC01: Sync-Endpoint-Design
- TASK-MC02: Offline-Prioritäts-Logik
- TASK-MC03: Conflict Resolution (last-write + semantic)
- TASK-MC04: SQLite-Client-Schema

## Discrepancy: implementation-plan-32-tasks.md vs SPECS.md
- The 32-task plan (HAL-P1-001..P7-005) is an older/oversimplified plan
- SPECS.md defines 44+ tasks with different naming convention (TASK-F01, TASK-C01, etc.)
- The 32-task plan includes Phase 7 (React Frontend) which is NOT in SPECS.md
- **Action needed**: Update or replace implementation-plan-32-tasks.md with SPECS.md-derived plan

## Next Step
TASK-F01: DB-Migration 0007 — first implementation task
