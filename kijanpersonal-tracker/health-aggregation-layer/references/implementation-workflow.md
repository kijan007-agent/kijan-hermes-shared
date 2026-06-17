# Health Aggregation Layer — Implementierungs-Workflow

**Quelle:** Implementiert 2026-05-20, HAL-Phase-0 (31 Tabellen, full CRUD, REST API, Test-Suite, CI/CD).

## 6-Phasen Implementierungsmuster

### Phase 1: Spezifikation (kpt-doc/_specs/)
- Alle Dokumente in `kpt-doc/_specs/health-aggregation-layer/`
- Format: `kpt-doc` als git submodule — commit und push separat
- Hauptdokument: `SPECS.md` mit Task-Index und Status

### Phase 2: Migration (alembic_health/versions/)
- **Dateiname:** `NNNN_<description>.py` — immer mit 4-stelliger Nummer
- **31 Tabellen:** 20 partitioned (RANGE) + 11 non-partitioned
- **Seed Data:** Symptom/Faktor-Definitionen + Infection Types
- **Partitionen:** 60 partitions (2026-01 bis 2030-12)
- **UUIDv7 IDs:** Alle Primary Keys — time-sorted, globally unique
- **Partition-Schlüssel:** `logged_at` für Zeitreihentabellen

### Phase 3: DAL Layer (app/dal/)
- **HealthDALRegistry:** Singleton mit 6 Repositories (SymptomDefs, SymptomLogs, FactorDefs, Aggregations, Reports)
- **Bulk-CRUD:** Alle Repos haben `bulk_create()` für Import-Pipeline
- **Async Session:** `get_health_session()` as context manager in `database_health.py`
- **Partition Awareness:** DAL kennt partition key, filtert auf aktuelle Partitionen

### Phase 4: REST API (app/routers/)
- **Route:** `/api/health/` — alle Endpunkte prefixed
- **CRUD:** 30+ Endpunkte für Symptome, Faktoren, Logs, Aggregationen, Trends, Korrelationen, Reports
- **Bulk-Import:** `POST /symptoms/logs/bulk` — für Bearable/Visible CSV-Import
- **Report Lifecycle:** `drafting → statistical → ki_ready → ki_done → final`
- **Router-Registrierung:** `app/main.py` → `include_router(health_aggregation_router)`

### Phase 5: Tests (tests/)
- **Test-Suite:** `test_health_aggregation.py` — 8 Test-Klassen, 25+ Tests
- **Test-Kennzeichnung:** `TST-HAL-XXX` für eindeutige Referenzierung
- **Test-Daten-Generator:** `test_health_data_generator.py` — CLI + 3 Szenarien
  - Default-Szenario: ME/CFS-Profil, 30 Tage
  - Bearable-Import-Szenario: 60 Tage, viele Symptome
  - Edge-Cases: Extreme Werte, leere Felder, Unicode
- **CI/CD:** `/.github/workflows/hal-test.yml` — PostgreSQL 16 Service + Migration + Tests

### Phase 6: Spezifikationen pushen
- `kpt-doc` als submodule — `git add`, `git commit`, `git push` separat
- Parent-repo update: `git submodule update --remote kpt-doc` → commit → push

## Arbeitsweise für parallele Teilaufgaben

- Migration + DAL: **parallel** (keine Abhängigkeiten)
- DAL + API: **parallel** (DAL ist unabhängig)
- Tests: **nach** API (benötigt Endpunkte)
- CI/CD: **nach** Tests
- Spezifikationen: **parallel** zu jeder Phase

## Commit-Convention

- `feat(hal):` — Neue HAL-Funktionalität
- `fix(hal):` — Bugfix in HAL
- `test(hal):` — Neue Tests
- `docs(hal):` — Spezifikationen
- `chore(hal):` — Infrastruktur (CI/CD, config)

## Status-Tracking

- **TASK-HAL-001** bis **TASK-HAL-XXX** — Task-Kennzeichnung
- **TST-HAL-001** bis **TST-HAL-008** — Test-Kennzeichnung
- Status: `pending` / `in_progress` / `completed` / `blocked`
- Integration-Milestones: **MILESTONE-HAL-001** (DAL ready) bis **MILESTONE-HAL-004** (CI/CD green)
