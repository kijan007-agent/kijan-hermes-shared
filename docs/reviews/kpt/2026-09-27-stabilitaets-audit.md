# Stabilitaets-Audit: KijanPersonalTracker Backend
**Task:** t_b94da104 | **Audit-Datum:** 2026-09-27 | **Scope:** kpt-backend
**Repo:** Kijan-Company/kpt-backend | **Branch:** dev

---

## 1. Abhaengigkeits-Matrix

| Abhaengigkeit | Art |Timeouts |Retries |Backoff |Idempotenz |Circuit-Brk |Rate-Limit |Health-Check |Shutdown |Bulkhead |
|---|---|---|---|---|---|---|---|---|---|---|
| PostgreSQL (4 DBs) | DB |TEILW |JA |NEIN |NEIN |NEIN |NEIN |JA |NEIN |TEILW |
| Redis (Cache) | Cache |FEHLT |FEHLT |FEHLT |N/A |FEHLT |FEHLT |FEHLT |N/A |FEHLT |
| FastAPI/Uvicorn | HTTP |TEILW |N/A |N/A |N/A |N/A |N/A |JA |TEILW |N/A |
| Alembic Migrations | Infra |NEIN |NEIN |FEHLT |N/A |FEHLT |FEHLT |NEIN |N/A |N/A |
| External APIs (Garmin, Oura, Wetter) | Drittsystem |FEHLT |FEHLT |FEHLT |UNBEKANNT |FEHLT |FEHLT |N/A |N/A |FEHLT |
| Lemon.markets | Zahlung |FEHLT |FEHLT |FEHLT |UNBEKANNT |FEHLT |FEHLT |N/A |N/A |FEHLT |
| Uvicorn Gunicorn | HTTP-Server |N/A |N/A |N/A |N/A |N/A |N/A |N/A |JA |N/A |

---

## 2. Timeouts

### 2.1 Datenbank (PostgreSQL)

**Befund:** MITTEL

- **Connection Pool:** `app/database.py:56` -- `pool_size=20, max_overflow=10, pool_timeout=30`. Connection-Timeout: 30s, vorhanden.
- **execute_with_retry:** `app/database.py:97-130` -- Retry-Loop mit `wait_exponential_jitter` aus `tenacity`, min=1s, max=10s, jitter +/-1s. **Backoff vorhanden, aber nicht exponentiell (kein multiplier).**
- **Health Check:** `app/models_health.py` -- `/health`, `/healthz`, `/ready` Endpoints. DB-Ping via `SELECT 1` in `app/routers/metrics.py`. Checking all 4 DBs separately.
- **FEHLT:** Idle-Timeout fuer DB-Connections (SQLAlchemy `pool_recycle` NICHT gesetzt). Connections koennen von der DB-Seite getrennt werden, ohne dass der Pool es bemerkt.

**Datei:Zeile:** `app/database.py:56` (pool_size, max_overflow, pool_timeout)

### 2.2 HTTP-Client (FastAPI)

**Befund:** KRITISCH

- **httpx.AsyncClient:** Wird in mehreren Routern als Module-Pattern (`app/routers/*/client.py` Pattern) erzeugt. Kein globaler Timeout-Config-State gefunden. **Default-Timeout von httpx ist 5s, aber keiner explizit gesetzt.**
- **Kein globaler HTTP-Timeout-Middleware** fuer ausgehende Requests.
- **Externe APIs:** Garmin-Connect, Oura-API, OpenWeather haben **keine expliziten Read/Connect Timeouts**.

**Datei:Zeile:** Suche nach `httpx.AsyncClient()` -- kein `timeout=` Argument gefunden.

### 2.3 Alembic Migrations

**Befund:** KRITISCH

- `_apply_migrations()` in `app/main.py:137-214` fuehrt Alembic bei jedem Startup aus.
- Kein Timeout fuer `alembic_command.upgrade` -- bei einer langsamen/lockenden Migration haengt der gesamte App-Start.
- `asyncio.to_thread(alembic_command.upgrade, ...)` -- kein Timeout-Wrapper.

**Datei:Zeile:** `app/main.py:172` -- `await asyncio.to_thread(alembic_command.upgrade, cfg, "head")`

---

## 3. Retry-Strategien

### 3.1 Datenbank-Retries

**Befund:** MITTEL (vorhanden, aber verbesserungswuerdig)

- `execute_with_retry()` in `app/database.py:97-130` mit `tenacity`:
  - `stop_after_attempt(5)` -- max 5 Versuche
  - `wait_exponential_jitter(initial=1, max=10, exp_base=2, jitter=1)` -- effektiv 1-11s Wartezeit
  - `retry_if_exception_type(sa.OperationalError)`
- **Problem:** Kein `retry_on_status_code` fuer HTTP-Fehler (503 Service Unavailable).
- **Problem:** Kein `retry_if_result` um idempotente Read-Operationen zu wiederholen.

**Datei:Zeile:** `app/database.py:97-130`

### 3.2 Telemetry Flush

**Befund:** MITTEL

- `_telemetry_flush_loop()` in `app/main.py:252-300` looft alle 30s.
- Fehlgeschlagene Flushes werden in `telemetry_buffer.requeue_failed()` zurueckgestellt.
- **Problem:** Kein Maximum fuer Requeue-Versuche. Bei DB-Ausfall werden fehlgeschlagene Telemetry-Daten unbegrenzt im Memory gehalten (`telemetry_buffer`).
- **Problem:** Keine Exponential-Backoff zwischen Flush-Versuchen.

**Datei:Zeile:** `app/main.py:252-300`

### 3.3 Alembic Migrations

**Befund:** KRITISCH

- Keine Retry-Logik fuer Migrationen. `alembic_command.upgrade` wird genau einmal aufgerufen.
- `BUG-577` Workaround fuehrt einen Self-Check nach dem Upgrade durch, aber keine Retry-Logik.

**Datei:Zeile:** `app/main.py:170-186`

### 3.4 Idempotency Keys

**Befund:** FEHLT (niedrig fuer Lese-Operationen, kritisch fuer Schreib-Operationen)

- Kein Idempotency-Key-Mechanismus fuer ausgehende API-Calls (Garmin, Oura, Weather).
- `telemetry_buffer.requeue_failed()` nutzt `(device_id, start_time)` als natuerlichen Idempotency-Key fuer DB-Updates (ausreichend fuer Telemetry).
- `execute_with_retry()` fuer DB-Zugriffe ist idempotent (Read-Operationen).

---

## 4. Circuit-Breaker

**Befund:** KRITISCH -- Kein Circuit-Breaker anywhere in der Codebase.

- Kein `circuitbreaker`-PyPI-Paket, kein `pybreaker`, kein `resilience4j`.
- Bei Garmin-API-Ausfall: jede Request retryt bis Timeout, dann 503 an Client.
- Kein FastAPI-Middleware fuer Circuit-Breaking.
- **Operativer Impact:** Single External-API-Ausfall kann den gesamten Request-Thread-Pool erchöpfen.

---

## 5. Rate-Limits

### 5.1 Eingehend (API-Gateway)

**Befund:** UNBEKANNT

- Kein explizites Rate-Limiting-Middleware in `app/main.py`.
- Starlette's `SlowAPIMiddleware` (default 1 request/sec/proc) laeuft nicht konfiguriert.
- Keine `RateLimiter` von `slowapi` oder aehnlichem.

### 5.2 Ausgehend (Externe APIs)

**Befund:** FEHLT

- Garmin-Connect: keine Rate-Limit-Handling-Logik.
- Oura-API: keine explizite Rate-Limit-Konfiguration.
- Weather-API: keine explizite Rate-Limit-Konfiguration.

---

## 6. Health-Checks

**Befund:** GUT (MIT Luecken)

- `/health` (`app/models_health.py`) -- Basic Ping
- `/healthz` -- Kubernetes Liveness (nur HTTP 200 wenn App laeuft)
- `/ready` -- Readiness mit DB-Ping (prueft alle 4 DBs mit `execute_with_retry`)
- **Separierung Deep/Shallow:** JA -- `/healthz` = shallow, `/ready` = deep
- **Kubernetes-Konformitaet:** TEILW -- `/healthz` fuer Liveness, `/ready` fuer Readiness
- **Luecke:** Redis/Externe-APIs nicht im Health-Check enthalten
- **Luecke:** Migrations-Status nicht im Health-Check (nur bei Startup geprueft)

**Datei:Zeile:** `app/models_health.py:1+` (Gesamtfile), `app/routers/metrics.py` (DB-Ping)

---

## 7. Graceful Shutdown

**Befund:** MITTEL

- `uvicorn` via `main.py` nutzt ` lifespan='on'` (AsyncExitStack mit `@asynccontextmanager`).
- **Vorhanden:** Uvicorn-default SIGTERM-Handling mit `timeout_graceful_shutdown=10`.
- **Luecke:** Kein explizites `max_requests` oder `max_requests_jitter` in Uvicorn-Config (Memory-Leak-Schutz fehlt).
- **Luecke:** Connection-Draining-Timeouts nicht explizit konfiguriert (nur Default 10s).
- **Telemetry:** `_telemetry_flush_loop` wird nicht gestoppt/awaited beim Shutdown (Graceful-Exit nicht implementiert).
- **Luecke:** `retention_cleanup_loop` Background-Task (in `app/middleware/request_logger.py`) -- kein explizites Shutdown-Signal.

**Datei:Zeile:** `app/main.py` (kein `on_event("shutdown")`), Uvicorn-Config in `docker-compose*.yml`

---

## 8. Bulkhead / Isolation

**Befund:** MITTEL (verbesserungswuerdig)

- **4 separate Datenbanken:** Admin, Activity, Projects, Health -- gute logische Trennung.
- **4 separate AsyncSession:** Jede DB hat eigenen Session-Pool.
- **Connection Pooling:** `pool_size=20, max_overflow=10` pro Engine (aus `app/database.py:56`).
- **Luecke:** Alle 4 Engines werden im gleichen AsyncIO-Event-Loop betrieben. Keine Thread-Pool-Trennung.
- **Luecke:** Kein `pool_recycle` (TCP-Keepalive fuer DB-Connections).
- **Luecke:** HTTP-Client-Instanzen (Garmin, Oura) teilen sich keinen Connection-Pool-Limiter.

**Datei:Zeile:** `app/database.py:40-56` (Engines), `app/database.py:56` (pool_config)

---

## 9. Priorisierte Findings

### KRITISCH

| # | Finding | Datei:Zeile | Operativer Impact |
|---|---|---|---|
| K1 | **Kein Circuit-Breaker** -- ext. API-Ausfall erchuellt Request-Threads | Gesamte Codebase | Service degradirt bei Drittanbieter-Ausfall |
| K2 | **Alembic-Migration ohne Timeout** -- Startup haengt bei langsamer/lockender DB | `main.py:172` | Totaler Ausfall bei Migration haengt |
| K3 | **Keine HTTP-Client-Timeouts** -- httpx verwendet Default (5s) ohne Konfiguration | Suche `httpx.AsyncClient` | Unvorhersehbare Timeout-Zeiten |
| K4 | **Unbegrenzte Telemetry-Requeue** -- Memory wächst bei DB-Ausfall | `main.py:271` | Memory-Leak bei DB-Ausfall |

### MITTEL

| # | Finding | Datei:Zeile | Operativer Impact |
|---|---|---|---|
| M1 | DB Connection Pool: `pool_recycle` nicht gesetzt | `database.py:56` | Stale Connections bei DB-Timeout |
| M2 | Kein `retry_on_status_code` fuer HTTP-503 in DB-Retry | `database.py:97-130` | Transit. DB-Fehler werden nicht optimal behandelt |
| M3 | Graceful Shutdown: Telemetry-Flush-Loop nicht gestoppt | `main.py:252` | Datenverlust beim Shutdown moeglich |
| M4 | Health-Checks decken Redis nicht ab | `models_health.py` | Health-Endpoint meldet OK trotz Redis-Ausfall |
| M5 | `uvicorn` kein `max_requests` konfiguriert | `docker-compose*.yml` | Memory-Leak-Risiko bei Worker-Langlebigkeit |
| M6 | Kein Rate-Limiting-Middleware (eingehend) | `main.py` | DoS-Risiko auf API |

### NIEDRIG

| # | Finding | Datei:Zeile | Operativer Impact |
|---|---|---|---|
| N1 | Backoff nicht exponentiell (kein multiplier in tenacity) | `database.py:97-130` | suboptimale Backoff-Kurve |
| N2 | Alembic-Migration kein Retry | `main.py:170-186` | Einzelne Migration kann startup brechen |
| N3 | Keine Idempotency-Keys fuer externe API-Calls | Router `*/client.py` | Doppelt-Calls moeglich bei Retry |
| N4 | Kein `pool_pre_ping` konfiguriert | `database.py:40-56` | Connection-validierung nur bei Checkout |

---

## 10. Referenz auf Vorherige Inventur

Die vorherige Inventur (`kanban task backlog`) inventarisierte folgende Funktionalitaeten, die im Stability-Audit referenziert werden:

- **Activity Tracking:** DB-Retry `execute_with_retry` vorhanden (mittel) -- `app/database.py:97-130`
- **Health-Modul:** Health-Checks vorhanden, aber Redis fehlt (mittel)
- **Projects-Modul:** Separater DB-Pool vorhanden (gut)
- **Lemon.markets:** Keine Resilience-Mechanismen gefunden (kritisch)

---

## 11. Empfehlungen (nicht implementiert -- nur Audit)

1. **Circuit-Breaker einfuehren:** `pip install circuitbreaker`, Middleware fuer Garmin/Oura/Weather-APIs.
2. **Alembic-Timeout:** `asyncio.wait_for()` um `alembic_command.upgrade` wrappen mit `timeout=60`.
3. **HTTP-Timeout-Middleware:** Globales `httpx.AsyncClient` mit `timeout=httpx.Timeout(10.0, connect=5.0)`.
4. **Telemetry Requeue-Limit:** `max_requeue_size=1000` in `telemetry_buffer`.
5. **Redis-Health-Check:** `/ready`-Endpoint um Redis-Ping erweitern.
6. **Graceful Shutdown:** `@asynccontextmanager`-Shutdown-Handler implementieren, der `_telemetry_flush_loop.cancel()` und `retention_cleanup_loop.cancel()` awaited.
7. **Rate-Limiting:** `slowapi` integrieren: `SlowAPIMiddleware(limit="100/minute")`.
8. **DB `pool_recycle`:** `pool_recycle=3600` in allen Engine-Configs setzen.
