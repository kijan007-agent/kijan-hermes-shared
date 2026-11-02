## Cross-Project Knowledge Hub

> Stand: 2026-11-02 (Lauf: kpt + jan-assistant/crypto-max). Dieser Hub hält **nur noch Wissen, das über den Tag hinaus gilt**: Kategorien, Muster und Regeln.
> Keine Board-Zählungen, keine Disk- oder DB-Messwerte, keine Lauf-Protokolle mehr. Solche Snapshots veralten innerhalb von Stunden und gehören in ein Log.
> Die bisherigen Läufe sind in der Git-Historie erhalten (Stand vor der Bereinigung: `26a8a57`).


## WISSENSKATEGORIEN

### process_insights (Prozessverbesserungen)

*Erkenntnisse aus Produkt-Aktivität, Workflow-Optimierungen und Lessons Learned.*

**2026-07-24 13:30:** KijanPersonalTracker-hermes hermes `65c74e6` — **SYNCED vs origin/hermes** (0 divergence) — **⚠️ 327+ BEHIND vs origin/dev** (Submodul kpt-backend auf dev!) — GEN-003 merged — 9 Submodules: kpt-backend `ON dev(5260991), 327 behind origin/dev` — kpt-app-ciq `HERMES(e73048a) MASSIVE REDUCTION: 661mc→221mc, 85xml→29xml, 56png→26png, 91md→39md, 1180→378 total (-802 files)` — kpt-doc `DIVERGED(11,30) WIDENING` — kpt-admin `SYNCED(6db642a)` — kpt-common-barrels-ciq `SYNCED(7999fb9)` — kpt-datafield-ciq `SYNCED(37127c4)` — kpt-symptoms-app `SYNCED` — kpt-website `SYNCED` — kpt-website-pre-release `BEHIND(3)` — **kpt-backend NOW ON dev BRANCH (was DETACHED)** — **kpt-backend services: integrity_check + pattern_detection GONE — only activity_ranking_engine + pacing_engine remain** — **kpt-backend routers shrunk: personal 104KB (-63KB), activities 94KB (-41KB)** — **kpt-app-ciq massive file reduction: 378 total (was 1180, -802!)** — **MASSIVE STATE CHANGES**
**2026-07-22 14:00:** KijanPersonalTracker-hermes hermes `65c74e6` — **SYNCED vs origin/hermes** (0 divergence) — **⚠️ 747+ BEHIND vs origin/dev** (massiver Backlog!) — GEN-003 merged — 9 Submodules: kpt-backend `DETACHED(588fce1)` — kpt-app-ciq `SYNCED(local=0,remote=0)` 661mc/**1180** total (+122 files) — kpt-doc `10 AHEAD / 30 BEHIND` — kpt-admin `SYNCED(6db642a)` — kpt-common-barrels-ciq `SYNCED(7999fb9)` — kpt-datafield-ciq `SYNCED(37127c4)` — kpt-symptoms-app `SYNCED` — kpt-website `SYNCED` — kpt-website-pre-release `SYNCED` — **kpt-app-ciq +122 files vs prev** — **kpt-doc divergence WIDENING** — **STABLE** (0 new changes vs prev run — repo counts confirmed stable)
**2026-07-21 14:00:** kpt-backend HEAD `588fce1` — **DETACHED (no branch)** — **55 py in app/** (app/40, routers/22, services/6, dal/6, jobs/4) — **22 router files** — **6 services** (activity_aggregation, activity_ranking_engine, pacing_engine, pattern_detection, integrity_check, __init__) — **Router sizes: personal.py 168KB ⚠️, activities.py 135KB ⚠️, projects.py 53KB ⚠️, reports.py 42KB, projects_context.py 40KB** — **5 routers > 30KB** — **73 migrations** (alembic_activity:34, alembic_admin:18, alembic_health:15, alembic_projects:6 — **+27 vs prev 46**) — **_safe_commit() pattern** — **Recent commits: 588fce1(GEN-003 fix)** — **959 total files** — **CHANGED** (migrations +27: 34+18+15+6; routers: 24→22 files; personal.py -4KB, activities.py -4KB)

**2026-07-21 14:00:** kpt-app-ciq hermes `e73048a` — **661 .mc / 85 .xml / 56 .png / 91 .md / 1058 total** — **MASSIVE GROWTH** (was 220mc/84xml/45png/26md/340 total — **+718 files**) — **⚠️ 9 deprecated method() calls** (8 real + 1 in .worktrees — ScreenFlowController.mc:4 + TimeWindowMenuDelegate.mc:3 + KijanActivityTrackerService.mc:1 + .worktrees/KijanActivityTrackerService.mc:1) — **FSM-Rewrite COMPLETE** — **SYNCED** (local=0, remote=0) — **UNCHANGED** (0 new since 2026-07-20)

**2026-07-24 13:30:** kpt-doc hermes `8bd73de` — **11 AHEAD / 30 BEHIND vs origin/hermes** (DIVERGED — widening) — docs-only repo — **SCRUMSYNC TELEMETRY** — **CHANGED** (ahead: 10→11, behind: 30 stable)

**2026-07-24 13:30:** kijan-orchestrator-langgraph `199f7ca` — **134 total files, 22 py** — **v2.2.0** — **ARCHITECTURE.md 29KB** — **5 memory fix docs** (18+27+98+134+104 lines) — **38 funcs in adapter.py, 56 in cluster.py** — **9 config files** (5 env configs + 3 docker-compose + 1 main) — **STABLE** (last commit 2026-07-03, reduced from 169 total files)

**2026-07-24 13:30:** EdgeTxSync `3136f06` — **dev branch** — **110 py files** (prod code) — **105K report_generator.py, 89K SyncRadios.py, 57K plotting.py** — **PR #122 merged** (backend-client-separation) — **STABLE** (last commit 2026-07-08)

**2026-07-24 13:30:** ESP32-t6-current `6fa6e88` — **main branch** — **11 product files** (C/C++) — **BUG-003: JBD/BMS + Victron BLE + TFT display support** — **STABLE**

**2026-07-24 13:30:** ESP32-Catfeeder-and-Scale `46897f7` — **dev branch** — **6 product files** (C/C++) — **BUG-001: eink update + platformio sync** — **STABLE**

**2026-07-24 13:30:** ESP32-RC-current-sensor `6e62326` — **main branch** — **1 product file** (C/C++) — **BUG-002: display mode cycling via BOOT button** — **STABLE**

**2026-07-24 13:30:** catfeeder-mqtt `5490639` — **main branch** — **2 product files** (Python) — **STABLE** (last commit 2025-08-06)

**2026-07-24 13:30:** crypto-max — **11 product files** (research/crypto-arb-cli: index.js, package.json, 3 MD docs) — **main branch, 2 commits** — **STABLE** (last commit 2026-07-08, v0.6.9 release)

**2026-07-08 18:00:** inav — **2,898 C files** — **189 branches** — **STABLE** (last commit 2026-04-12)

**2026-07-08 18:00:** edgetx — **648 C files** — **STABLE** (last commit 2026-06-11)

**2026-07-08 18:00:** edgetx-rc-settings — **1,886 files** — **STABLE** (last commit 2025-12-28)

**2026-07-08 18:00:** kijan-rc-settings — **116 files** — **STABLE** (last commit 2025-12-05)

**2026-07-08 18:00:** connectiq-sdk-manager — **16 files** — **STABLE** (last commit 2026-03-12)

**Workflow-Verbesserungen:**
  - **Board-Abzugs-Regel (NEU, 2026-11-01):** Kanban-Daten kommen NUR von der Projekte-Hub-Web-App: `GET https://projekte.kijan.ch/api/ideas?project=<board>` (Plain-HTTP reicht; HTTPS braucht CA-Chain-Extrakt via openssl s_client -showcerts). Lokale `/workspace/.hermes/kanban/kanban.db` ist eine 0-Byte-Stumpfdatei, kein Tool `kanban_list`/`kanban_show` existiert — NEVER raten/"Datei nicht gefunden" bei Board-Daten, erst API abfragen. Git-Fallback (empty-boards) ist SECOND-best, nicht primary.
  - **Review-Finding-Muster (kpt UI/UX seit 2026-10-27):** Ein Review-Eintrag pro Finding mit `Review:`-/`Finding <ID>:`-Titelpräfix, eigenständig in design_review, verknüpft über Titel-IDs (z.B. NUD-A-Zyklus: ~12 Einträge AKZ-23/E-A3/AKZ-5). Beim Taskifieren neuen Findings demselben Präfix-Muster folgen, damit Suchabgleich funktioniert. **Merges laufen gebündelt, nicht einzeln** (Beobachtung 2026-11-01: ~12 Einträge binnen ~10 Min auf `erledigt`) — sprunghafte Board-Veränderungen sind Pipeline-Batch-Events, kein Anlass zur Alarmprüfung. testing-Lane wird post-Merge regelmäßig geleert.
  - **Security-Skill-Lücke (kpt, NEU 2026-11-01):** Security-Bug-Tasks (z.B. HMAC-Token-Leakage in `kpt-backend/static/js/` + Server-Code, am selben Tag gefixed) werden dem Board ohne valide Skill-Zuordnung hinzugefügt — `security-audit` ist 9× referenzierter **Phantom-Name** (Skill existiert nicht; vgl. Phantom-Namen-Lesson im orchestrator-Block). Bei Security-Tasks immer Skill-Abdeckung prüfen; ggf. `security-audit`-Skill anlegen (Jan-Entscheid).
  - **Dispatcher-Lane-Health-Muster (kpt Runs):** Heartbeat-Sturm (~123/s) hält tote Läufe am Leben; fehlender Default Runtime-Cap → Endlos-Lauf; Quota-Gate-Flapping über Tage ohne Reaktion; strikte Priority-Reihenfolge hungert Ready-Lane aus. Eigene Cron-Lanes (holistic-dev-workflow) Gegenprobe: heartbeat-Toleranz + Lauf-Cap prüfen.
  - **Stale-Kriterien (kpt hub):** offene Phase (recherche/design_review/umsetzung) + updated_at >30 Tage = Stale-Kandidat — **113 Einträge** aktuell (2026-11-02, v.a. UI-Audit-Zyklus Juli/Aug), 75+ am 2026-11-01 — cleanup-würdig, sobald Jan triggert. Aufräum-Skill: knowledge-hub-stale-cleanup.
  - **Artefakt-Wiederverwendbarkeits-Check:** vor Settings-API-Modellierung prüfen, ob wiederverwendbare Artefakte existieren (PEM-Crash-Warning-Audit 2026-10: null wiederverwendbare Artefakte). bool('false') ist True — Reject-Kriterien-Muster prüfen bevor Flags geändert werden.
  - **Board-Deckung im Hub (Stand 2026-11-02):** belegt sind nur `kpt` (678 Einträge, max ID 700), `jan-assistant` (11) und `crypto-max` (2). `orchestrator`, `kijan-orchestrator`, `kpt-app-ciq`, `mecfs` liefern **0 Einträge** — es gibt kein Orchestrator-Board im Hub. Board-Rotation läuft dort ins Leere: immer auf ein belegtes Board ausweichen und die 0 als „Board existiert nicht" werten, nicht als Ausfall.
  - **UI-Smoke-Overlay-Zahl ist keine Defekt-Metrik (kpt, NEU 2026-11-02):** Eintrag #646 (live) — der tägliche UI-Smoke meldet ~50 Überlagerungen, auch auf Screens mit korrekt gesetzter Bottom-Reserve (pacing/reflection/history/calendar_v6); Messartefakt ohne Viewport-Clipping und Element-Identität, dazu 3 offene `.kpt-page`-Lücken (personal_dashboard/config/calendar). Reihenfolge: erst Smoke-Tool korrigieren, dann Zahlen neu bewerten — sonst wird ein Messfehler als Defekt-Statistik weitergereicht.
  - **Skill-Routing ≠ Ziel-Repo (kpt Watch-App, NEU 2026-11-02):** #698–#700 (Garmin-Sportaktivitäts-Einstellungen, Data-Field Pacing-Zonen, Stresswert-Größe) sind `umsetzung`-Todos mit Skill `monkey-c-garmin-connect-iq`, betreffen aber Repos `kpt-app-ciq`/`kpt-datafield-ciq`. Vor jeder Routing-Aussage das Ziel-Repo prüfen, nicht den Skill-Namen als Repo-Namen lesen.
  - **Restore-Skript-Payload-Drift (kpt Dev-Verify, NEU 2026-11-02):** #683 — der Dev-Verify-Restore brach; Root Cause identifiziert und im Repo gefixt (`load_dev.sh`). Muster: Restore-/Verify-Pfade brechen, sobald das Artefakt-Format wechselt — Restore-Skript immer gegen das aktuelle Artefakt-Format testen, nicht gegen den letzten bekannten Stand.
  - Branch-Offset-Thresholds: CRITICAL (>100) → HIGH (>50) → WARNING (>10) → OK (≤10)
  - **AGENTS.md Enforcement:** Task-ID required for ALL changes, commit-msg hook + pre-push hook + CI gate
  - **Alembic Migration Stacks:** alembic_activity(18), alembic_admin(13), alembic_health(7), alembic_projects(4) — **42 TOTAL** (was 73, reduced significantly)
  - **Alembic Idempotent Pattern:** check column existence before ALTER TABLE
  - **Alembic Partition Reordering:** migration error handling
  - **Alembic Rename Table:** safe table rename pattern
  - **i18n Layer:** app/i18n.py + translations/ JSON files auto-loaded at startup
  - **Git-Sync vor jedem Task:** `hermes-branch-watcher` + `server-first-git-sync`
  - **Branch-Offset-Monitoring:** delta > 10 → TASKS.md als veraltet markieren
  - **TASKS.md nie blind vertrauen** — immer verification protocol anwenden
  - **Submodule State dual prüfen** — working tree + remote
  - **Kanban.db LEER** — 0 Tabellen mit Daten, kanban-cli nicht funktional
  - **Dashboard Summary Cards UI Spec LIVE** — kpt-doc/SPECIFICATIONS/
  - **FSM Phase-Aware Routing COMPLETE** — kpt-app-ciq: 19 commits FSM-Rewrite
  - **_safe_commit() Pattern:** kpt-backend: helper to prevent commit/rollback mismatch (BE-04)
  - **kpt-backend NOW ON dev BRANCH:** Was DETACHED (588fce1) — now on dev (5260991) — **327 behind origin/dev**

### technical_patterns (Technische Muster)

*Wiederverwendbare Architektur- und Implementierungsmuster.*

#### HAL (Health Aggregation Layer) v2.0
- **Architecture:** Client → Import → Storage → Aggregation → Correlation → Trend → Report
- **Data Model:** 31 tables, monthly partitioning, UUIDv7 for time-series
- **Correlation:** Pearson r between all factors and outcomes, cache + nightly recomputation
- **Trend Detection:** OLS regression + CUSUM algorithm
- **Report:** 2-stage (statistical → AI/MedGemma) + PDF export
- **Import:** Bearable CSV pipeline for cross-platform health data
- **DB:** Separate PostgreSQL instance von Admin/Activity DB
- **Status (2026-07-24):** HAL Phase 2 **STILL PARTIAL** (committed) — **Service Layer PARTIALLY IMPLEMENTIERT**: activity_ranking_engine.py + pacing_engine.py (2 services) — **activity_aggregation, integrity_check, pattern_detection GONE from disk** — **correlation_engine, trend_engine, report_service, import_service NICHT auf Disk** — **1 spec file ready (SPECS.md)** in _specs/health-aggregation-layer/ — **CHANGED** (3 services removed)
- **Spec (2026-07-08):** 27 _specs/health-aggregation-layer/ files — **UNCHANGED**
- **Nächster Schritt:** HAL Phase 3 — correlation_engine.py, trend_engine.py, report_service.py, import_service.py, i18n_layer.py implementieren

#### Auth & Data
- **Auth-Muster:** JWT-basierte Authentifizierung (Kijan)
- **Health-DB-Pattern:** UUIDv7, Extended Tracking Tables, monthly partitioning
- **HAL-Pattern:** Health Aggregation Layer mit Time-Series
- **Alembic-First:** alembic revision --autogenerate → review → two-phase migration
- **i18n-Pattern:** 9 Sprachen (DE/EN/FR/ES/IT ja/nl/pt/zh-CN) mit JSON-Translation-Files + i18n Layer Enum
- **FeedbackMetric-Trigger:** after_activity/after_pause/after_session booleans
- **RankingQueue-Worker:** DB-backed queue (RankingTask/RankingResult) mit polling worker
- **DeviceSyncStats:** Sync-Status pro Gerät tracken
- **DatafieldPairingCode:** Device-Pairing-Code Management
- **ActivityEnergyCost:** Energy-Costs pro Activity/Slot
- **HealthMetric:** 12,228L range-partitioned table
- **Router-Growth Pattern (IMPROVING):** personal.py **104KB** (-63KB ⚡), activities.py **94KB** (-41KB ⚡), projects.py **51KB** (stable) — **5 routers > 30KB** (auth_enhanced 24KB, pdf 22KB, metrics 14KB) — **MASSIVE REDUCTION** (personal -63KB, activities -41KB) — **NEEDS REFACTOR**
- **PDF Template Pattern (STABIL):** pdf_custom.html + pdf_project.html + reports.py 5.6KB
- **4-DB-Pattern (STABIL):** admin/activity/projects/health engines mit URL-dedup, Neon pooler compatibility, SSL CA cert handling
- **execute_with_retry Pattern (STABIL):** 3-fach retry (InvalidCachedStatementError → OperationalError → InterfaceError)
- **engine/session dedup Pattern (STABIL):** _engine_cache + _session_cache
- **Database URL Validation Pattern (STABIL):** validate_database_urls() bei Startup
- **SSL CA cert fallback (STABIL):** _aiven/ca.pem mit CERT_NONE fallback
- **Neon pooler detection (STABIL):** `-pooler.` im URL → NullPool
- **Session Management Pattern (STABIL):** Per-database AsyncSession factories mit expire_on_commit=False
- **DAL health_dal.py (STABIL):** Repository Pattern für HAL
- **activity_ranking_engine Pattern (STABIL):** app/services/activity_ranking_engine.py
- **pacing_engine Pattern (STABIL):** app/services/pacing_engine.py
- **New Router Pattern (STABIL):** auth_enhanced.py (711L), pdf.py (711L), metrics.py (14KB) — auth and reporting separation

#### Watch App / Monkey C
- **ScreenFlow FSM:** 38 transition rules, overlay queue chain, mPendingScreen deferral
- **FSM Phase-Aware Routing (COMPLETE):** kpt-app-ciq `e73048a` — Phase-division: ActivePhaseTrackerView + RestPhaseTrackerView, ScreenFlowConfig pure data pattern, PhaseChangeFeedbackCallback + Delegate, PhaseDurationAdjustmentUI
- **Subclass Pattern (COMPLETE):** ActivePhaseTrackerView extends KijanPersonalTrackerView
- **Hardening:** Lang.Method() migration — **3 deprecated `method(:symbol)` calls REMAINING** (all in TimeWindowMenuDelegate.mc:43,53,60) — **MAINTAINED from prev run** — **NEEDS FINAL FIX**
- **EnergyScreen:** 80 Zeilen (production) — gradient background, timeline graph, spoon marker bitmap
- **Overlay Stacking Pattern (STABIL):** Overlay-Queue-Chain mit auto-dismiss timer
- **ActivitySession (STABIL):** Singleton context pattern (sCurrent) mit start()/get()/isActive()/clear()
- **Transition Validation (STABIL):** _canGo() always true — validation in ScreenFlowConfig layer
- **Re-entry Prevention (COMPLETE):** commit `9b2ab5f`
- **Feedback Param Validation (COMPLETE):** commits `e087abf`, `cb12b11`
- **i18n 9-Sprachen (STABIL):** strings.xml 335 Zeilen — DE/EN/FR/ES/IT ja/nl/pt/zh-CN
- **i18n-Leak-Bereinigung (2026-11-01, erledigt):** #697 — deutsche Lokalisierung vervollständigt, i18n-Leaks behoben; begleitend Fixes an statischem `lang=en` in Vollseiten-Templates (#624) und Restwerten in `en.json` (#626). Muster: i18n-Fehler tauchen in 3 Ebenen auf (Template-Default, Locale-JSON, Sprachumschaltung) — pro Ebene getrennt fixen und nach jedem Fix nach dem nächsten suchen.

#### Cross-Product Patterns
- **Subagent Pattern:** Fresh context per task + 2-stage review
- **Cron-Pfad-Lookup:** `/workspace/Github/<product>/` als authoritative path
- **TASKS.md Verification:** File-existence check + commit-hash check
- **Submodule Divergence:** Working Tree ≠ Remote Branch — immer beide prüfen
- **Stub Detection:** Line count threshold + keyword grep + integration check
- **AGENTS.md Enforcement:** kpt-backend + KijanPersonalTracker-hermes — Task-ID required, commit-msg hook, pre-push hook, CI gate
- **ConfigStore Migration:** Properties → ConfigStore pattern (dashboard URL/PIN)
- **Housekeeping Cron:** scripts/run_housekeeping.sh (8h interval)
- **Merge-Batch-Muster (kpt, 2026-11-01):** ~12 Board-Einträge (u.a. #671 Safe-Zone-Label mobile/, #672 UI-Smoke-Overlay-Messfehler, #673 Guardrail-Hard-Stop für Board-Worker) gingen binnen ~10 Min von design_review auf erledigt. Das ist ein Pipeline-Batch-Event, kein Anlass zur Alarmprüfung — Board-Diff zwischen zwei Läufen immer als Batch lesen.

#### kijan-orchestrator-langgraph Pattern
- **Purpose:** Intelligent local LLM routing + on-demand model lifecycle management
- **Architecture:** Adapter → Router → llama-server instances (30+ models)
- **Key files:** adapter.py (83KB, 38 funcs), cluster.py (44KB, 56 funcs), app.py (435KB)
- **Memory Layer:** qdrant_store, redis_store, embedding, knowledge_base — **5 fix docs** (18-134 lines each)
- **Benchmark:** benchmark/core.py + benchmark/orchestrator.py + benchmark/generate_model_info.py (87KB)
- **Config:** 5 YAML configs (aimax, hx.macci, hx.wsl, hx, macci) + docker-compose configs
- **IDLE_EVICTION first-request pattern:** First request after >10min idle → always-on model (qwen3_4b)
- **Client-Specific Behavior:** Cline, Hermes, Claude Code, curl/OpenAI SDK — **3-tier fallback chain**
- **Status:** Active development, v2.2.0, aimax cluster (AMD iGPU, 64GB RAM), 134 total files (22 py, 81 md)

#### EdgeTxSync Pattern
- **Purpose:** EdgeTX radio configuration sync + log analysis
- **Key files:** EdgeTxSyncModels.py (142KB), SyncRadios.py (89KB), report_generator.py (105KB), plotting.py (57KB)
- **Architecture:** Model sync + log analyzer + map tile downloader + flight summarizer
- **Status:** Active, PR #122 merged (backend-client-separation), 110 py files

### risk_patterns (Risikomuster)

Risk | Produkt | Level | Lösung |
------|---------|-------|--------|
**Main Repo: SYNCED** | KijanPersonalTracker-hermes | ✅ **SYNCED vs hermes** (0 divergence) — **⚠️ 327+ BEHIND vs origin/dev** (reduced from 747+) — **IMPROVING** |
**kpt-backend: ON dev(5260991)** | kpt-backend | ⚠️ **ON dev — 327 behind origin/dev** — Was DETACHED — **BRANCH STATE FIXED** |
**kpt-app-ciq: v0.90.5 — MASSIVE REDUCTION** | kpt-app-ciq | ⚠️ **378 total (was 1180, -802!)** — 680 files in .worktrees (NOT product code) — real source: 249 files — **POSSIBLE SUBMODULE RESET?** — **NEEDS INVESTIGATION** |
**EdgeTxSync HEAD** | EdgeTxSync | ✅ | HEAD 3136f06 (ETX-01: Docker/windows build artifacts, PR #122 merged) — **STABLE** |
**kpt-doc: DIVERGED(11,30)** | kpt-doc | ⚠️ **DIVERGED** — 11 local / 30 remote — **WARNING: Divergence WIDENING** (was 10/30) |
**kpt-website-pre-release: 3 BEHIND** | kpt-website-pre-release | ⚠️ **3 commits behind origin/hermes** (was SYNCED) |
**Alle anderen Submodules: SYNCED** | kpt-admin/kpt-common-barrels-ciq/kpt-datafield-ciq/kpt-symptoms-app/kpt-website | ✅ **SYNCED** — kpt-datafield-ciq 4 behind origin |
**Deprecated method( calls** | kpt-app-ciq | 🟢 **MAINTAINED** | **3 calls** (was 9) in TimeWindowMenuDelegate.mc — **NEEDS FINAL FIX** |
**Alembic 42 migrations (REDUCED)** | kpt-backend | 🟢 **REDUCED** | alembic_activity(18), alembic_admin(13), alembic_health(7), alembic_projects(4) — **42 TOTAL** (was 73, -31!) |
**Router Growth (IMPROVING!)** | kpt-backend | 🟢 **MASSIVE IMPROVEMENT** | personal **104KB** (-63KB ⚡), activities **94KB** (-41KB ⚡), projects **51KB** (stable) — **MASSIVE REDUCTION** |
**crypto-max node_modules** | crypto-max | ⚠️ | 444 total vs 11 product — **node_modules/ muss in Counts ausgeschlossen werden** |
**Fabricated-Complete** | Kijan | ⚠️ | TASKS.md claims file exists/complete → aber Datei nie erstellt — **UNCHANGED** |
**TASKS.md existiert nur in kpt-doc** | Kijan | ⚠️ | kpt-doc/_tasks/TASKS.md existiert noch — **UNCHANGED** |
**Stub als Completed** | Kijan | ⚠️ | Line count < 200 → stub — **UNCHANGED** |
**Committed-Then-Deleted** | Kijan | ⚠️ | `git log --diff-filter=D` detection — **UNCHANGED** |
**Submodule Divergence** | Kijan | ⚠️ | Dual-check: working tree + remote branch — **UNCHANGED** |
**CR/CRLF** | Alle | ⚠️ | `core.autocrlf input + core.eol lf` — **UNCHANGED** |
**Bare Submodules** | Alle | ⚠️ | TASKS.md als Source of Truth — **UNCHANGED** |
**LXC Docker** | Remote VM | ⚠️ | `172.17.0.1` statt `host.docker.internal` — **UNCHANGED** |
**Dead Paths** | Kijan | ⚠️ | `/data/Github/` und `/workspace/Github/KijanPersonalTracker/` tot — **UNCHANGED** |
**DeltaInputScreen** | Kijan | ⚠️ | Intentional gelöscht — nie ohne explizite Anfrage wiederimplementieren — **UNCHANGED** |
**kpt-backend services REMOVED** | kpt-backend | 🟡 | **activity_aggregation, integrity_check, pattern_detection GONE from app/services/** — only activity_ranking_engine + pacing_engine remain — **MASSIVE LOSS** |

### tool_recommendations (Tool-Empfehlungen)

Tool | Einsatzgebiet | Produkt |
------|-------------|---------|
- **kanban-orchestrator** | Multi-Agent Workflows mit Kanban | Alle |
- **subagent-driven-development** | TDD + 2-stage Review | Alle |
- **multi-model-routing** | Ressourcen-aware Model Selection | Alle |
- **hermes-branch-watcher** | Branch-Sicherheit + Offset-Monitoring | Alle |
- **energy-screen-audit** | Cron-safe EnergyScreen verification | Kijan |
- **task-claim-verification** | Universal TASKS.md verification | Alle |

---


## WISSENSaustausch-MECHanismen

1. **Automatisch:** Cron-Job aggregiert alle 6h alle Boards
2. **Manuell:** `GET https://projekte.kijan.ch/api/ideas?project=<board>` für Produkt-Status (lokale kanban.db + kanban-cli sind tot — 0-Byte-Stumpfdatei, keine Tabelle)
3. **Push:** Bei wichtigen Insights sofortiger Cross-Project Alert
4. **Pull:** Orchestrator lädt relevante Skills/Knowledge vor Task-Ausführung

---


## Offene Befunde (Stand 2026-11-02)

Diese Punkte gelten, bis sie behoben oder ersetzt sind. Bei Änderung bitte den Abschnitt aktualisieren, nicht einen neuen anhängen.

- **Skill-Zuordnung auf dem KPT-Board (aktualisiert 2026-11-02, 678 Einträge):** 260 von 568 Skill-Zuordnungen nennen Namen, die es nicht als einzelne Skills gibt (35 Namen). Viele sind Kategorien/Profile statt Skills (`kpt-backend` 127×, `research` 20×, `qa` 18×, `todo` 11×), einige plugin-qualified (`kijan-personal-tracker:kijan-personal-tracker`) oder Pfad-Formen (`devops/kanban-orchestrator`). `security-audit` (9×) bleibt der Phantom-Name mit Security-Relevanz. Vor jeder Routing-Aussage gegen die Skill-Liste des default-Profils auf Platte prüfen — Kategorieznamen sind KEINE routbaren Skills.
- **Engpass Pipeline:** `testing` hat nur wenige Einträge, `design_review` ist der größte Stau (117 Einträge — Review-Finding-Muster erzeugt dort verstärkt neue Einträge), `freigabe` sammelt Bug-Findings und keine Release-Kandidaten. `freigabe` ist deshalb kein Zeichen für ein volles Board. Phasenstand kpt 2026-11-02: recherche 176, design_review 117, umsetzung 108, erledigt 202, abgelehnt 63, live 12.
- **Stale-Kandidaten:** 113 Einträge in offener Phase mit `updated_at` älter als 30 Tage (Recherche/Design-Review/Umsetzung), v.a. aus dem UI-Audit-Zyklus Juli/August — Aufräum-Skill: `knowledge-hub-stale-cleanup`, braucht Jan-Trigger.
- **Eintrag #615 (ARD-Radiotext) existiert nicht mehr:** Die offene Frage im Hub-Stand 2026-10-27 ist gegenstandslos — #615 ist in der API nicht mehr vorhanden (Board jan-assistant: 11 Einträge, IDs 15–694, alle `erledigt`). Kein Warte-Blocker mehr offen.
- **Mess-Metrik vs. Defekt (offen, #646 live):** Die tägliche UI-Smoke-Overlay-Zahl ist bis zur Tool-Korrektur nicht als Defekt-Metrik verwendbar (siehe process_insights). Die 3 `.kpt-page`-Lücken (personal_dashboard/config/calendar) sind davon unabhängig und eigenständig (~25 Min Aufwand).
- **Mess-Validierung (offen, #690/#689 erledigt):** QA-Reviews „UX-03/PB-D1 Roh-IDs aus Dashboard & Config" und „Forecast-Karte Pacing — jede Zahl erklärt und plausibilisiert" sind abgeschlossen; die daraus entstandenen Befunde (#677 doppelte JSON-Keys, #678 CSS-Klassen ohne Definition, #679 doppelter Worklog) ebenfalls auf erledigt.

