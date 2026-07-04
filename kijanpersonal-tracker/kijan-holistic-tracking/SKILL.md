---
name: kijan-holistic-tracking
description: "Kijan Personal Tracker holistic tracking architecture — 3-platform strategy (Watch/Dashboard/Mobile), energy pacing + symptom + medication tracking integration, Burndown-Chart design, data flow, and phased implementation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kijanpersonal-tracker, architecture, holistic-tracking, energy-pacing, symptom-tracking, medication-tracking]
---

# Kijan Holistic Tracking Architecture

## Triggers
- Planning or implementing energy pacing, symptom tracking, medication management, or health metrics in Kijan
- Multi-platform design across Watch (CIQ), Web Dashboard, and Mobile App
- Burndown-Chart design or health data correlation
- Any task mentioning "ganzheitlich", "holistisch", "Plattform-übergreifend", "Synchronisation", "Tag-im-Überblick"

## Concept: 3-Platform Strategy

Each platform has a **single core responsibility** — no platform does everything:

| Platform | Kernfunktion | Unique Value |
|----------|-------------|--------------|
| **Watch (CIQ)** | Quick-Logging (<2s), Spoon-Burndown, Aktivität | Immer dabei, kein Phone nötig |
| **Dashboard (Web)** | Analysen, Korrelationen, Arztberichte | Tiefe Einblicke, Pearson r, PDF |
| **Mobile App** | Push-Reminders, erweitertes Symptom-Logging | Einziger Push-Kanal, Body-Map, Fotos |

### Synergy Principle
- **Watch = Datenerfassung** (always-on, sub-second logging)
- **Dashboard = Dateninterpretation** (correlations, trends, reports)
- **Mobile = Intervention** (push reminders, extended logging)

## Unified Dashboard Layout (from 2026-05-13 concept)

```
1. Energy Envelope (Spoon Ring + PEM-Risk + Hülle%)
2. Burndown-Chart "Tag im Überblick" (4 Datasets: today, yesterday, weekly avg, monthly band)
3. Today's Activities with spoon counts
4. Today's Symptom Summary
5. Today's Medication Status
6. Weekly Progress Bars
7. Quick Check-in bar
8. Bottom nav: Dash | Aktiv | Verh | Gesund | Einstell
```

## Burndown-Chart Design

- **4 Datasets:** Today (solid green), Yesterday (dotted gray), Weekly Avg (dashed blue), Monthly Band (shaded)
- **Zone background:** Green (20-25 spoons), Orange (10-20), Red (0-10)
- **Interactive:** Hover = symptom overlay, Click zone = filter activities, Crosshair = HRV/Steps/BB
- **Underneath:** Medication timeline as secondary axis

## Data Flow Architecture

```
Watch → HTTPS POST → Backend (FastAPI/PostgreSQL) ← iCal/QR → Dashboard
Mobile ↔ REST API (JWT) ↔ Backend
```

| Direction | Mechanism | Frequency |
|-----------|-----------|-----------|
| Watch → Backend | HTTPS POST (batched) | Per check-in + activity |
| Backend → Watch | GET /d/{id}/config + /api/health | On sync/start |
| Mobile ↔ Backend | REST API (JWT) | Real-time |
| Dashboard ↔ Backend | Cookie + JWT | Real-time |

## Backend Health Module Schema

### New Tables (in health database):

| Table | Purpose |
|-------|---------|
| symptom_definitions | User-defined symptoms |
| symptom_logs | Symptom log (partitioned monthly) |
| medication_definitions | User medications |
| medication_schedules | Med schedule per medication |
| medication_logs | Intake log |
| body_map_regions | Pain regions (enum) |
| correlation_cache | Pearson r between all pairs |
| import_jobs | Bearable/CSV import jobs |
| disease_catalog | ICD-10-GAM seed data |

### New Router Prefix: `/d/{device_id}/api/`
- `symptoms/` — CRUD + Logs
- `medications/` — CRUD + Schedules + Logs
- `body-map/` — Pain region log
- `correlations/` — Correlation data
- `health-report/` — Doctor reports
- `import/` — Bearable CSV import

## Phased Implementation Plan

### Phase 1: Dashboard Burndown-Chart (Priority 1)
1. Burndown-Chart with 4 datasets (today, yesterday, weekly avg, monthly band)
2. Symptom overlay on chart
3. Medication timeline under chart
4. Zone background (green/orange/red)

### Phase 2: Backend Health-Module
1. DB migration for symptom_logs + medication_logs
2. API routers for symptom/med CRUD + logs
3. Correlation engine extension (symptom ↔ Garmin metrics)

### Phase 3: Connect IQ Extensions
1. SymptomQuickLog.mc screen (NRS 0-10)
2. MedicationReminder.mc screen
3. Sync integration (symptom/med data → backend)

### Phase 4: Mobile App
1. Scaffold React Native app
2. Push notifications (med reminders, PEM risk)
3. Body-Map (SVG touch), photo symptom log
4. PDF doctor reports

### Phase 5: Integration
1. Symptom ↔ Activity correlation on dashboard
2. Medication adherence in health overview
3. Unified "Health" tab in dashboard

## Watch Extension: New CIQ Screens

> **⚠️ 2026-06-08 WIPE**: All KijanPersonalTracker repos wiped. No code exists to implement against. Status below is pre-wipe planning intent only.

| Screen | Purpose | Status |
|--------|---------|--------|
| SymptomQuickLog.mc | Fast symptom log (NRS 0-10) | Needs creation |
| MedicationReminder.mc | Med reminder + log | Needs creation |
| HealthSummaryScreen.mc | HRV/BB/Sleep/SpO2 compact | Needs creation |
| BurndownScreen.mc | Extended burndown chart | Exists (stub) |
| EnergyScreen.mc | Energy check-in (NRS) | ⚠️ Pre-wipe: 123-line stub (not 493-line chart) |
| DeltaInputScreen.mc | Quick delta input | ❌ Pre-wipe: NEVER COMMITTED |

## Watch → Backend Sync Extensions

Current sync data:
- Activity (start/end, metrics)
- Energy Pacing (check-in)
- Health Metrics (HRV, BB, stress, steps, sleep)
- Device config

New sync data:
- SymptomLog (symptom_id, severity, logged_at, notes)
- MedicationLog (med_id, taken_at, status)
- MedicationSchedule (synced from dashboard)
- BodyMap (pain regions as bitmask)

## Cold-Start Spoon Problem (from 2026-05-13 discussion)

**Problem:** Individual spoon consumption per activity is unknown at the start.

**Solution:** Community Median + Adaptive Learning
- Days 1-3: Community median for activity type
- Days 4-7: User-adjustable ("Mehr/weniger spoons?")
- Day 8+: Automatic learning begins
- Algorithm: `new_spoons = old_spoons + (actual_used - spent) * alpha`

## Key Pitfalls

1. **kpt-app-ciq source** is in `/workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq/source/` (working tree in hermes workspace), NOT in prod-hotfix bare clone
2. **Health DB** is separate from Activity/Admin/Project DBs — use `get_db_health()` for all health module queries
3. **Symptom tracking** is disabled on basic plan (`max_symptomtracking = 0` in UserDefinition) — check plan before exposing
4. **HealthMetric metrics** enum must be extended if adding new metric types — check `_VALID_METRICS` constant
5. **Monthly partitioning** — health_metrics uses range partitioning; new partitions must be created for future months

## Related Skills
- `kijan-personal-tracker` — Project structure, branches, TASKS.md patterns
- `kijan-health-module` — Health DB schema, SQLAlchemy models, API patterns, ICD-10-GAM
- `kijan-personal-tracker-debug` — Garmin watch app debugging patterns
- `energy-pacing-dashboard` — Energy pacing dashboard patterns for Kijan

## Reference Files
- **`references/holistic-tracking-concept.md`** — Full 3-platform tracking concept (2026-05-13)
- **`references/health-module-schema.md`** — Complete health DB table definitions and relationships
- **`references/symptom-tracking-api.md`** — Symptom/Medication API router patterns
