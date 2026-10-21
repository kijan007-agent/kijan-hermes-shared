## Cross-Project Knowledge Hub

Stand: 2026-10-20 21:00 UTC
**Status:** 🟡 Stable — Boards leer; state.db +3.2 MB in 12 h; Disk jetzt 85 %; NEU: 3 Cron-Jobs mit Fehlerstatus, davon 1 (oauth-refresh) mit kaputtem Skript-Pfad.
> Aktualisierung: alle 6h via Cron-Job
> Nächste Aktualisierung: 2026-10-21 03:00 UTC
> Board-Rotation dieses Laufs: **kijan-steuern, jan-assistant** (nächstes Mal: kpt, orchestrator)

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

#### Cross-Product Patterns
- **Subagent Pattern:** Fresh context per task + 2-stage review
- **Cron-Pfad-Lookup:** `/workspace/Github/<product>/` als authoritative path
- **TASKS.md Verification:** File-existence check + commit-hash check
- **Submodule Divergence:** Working Tree ≠ Remote Branch — immer beide prüfen
- **Stub Detection:** Line count threshold + keyword grep + integration check
- **AGENTS.md Enforcement:** kpt-backend + KijanPersonalTracker-hermes — Task-ID required, commit-msg hook, pre-push hook, CI gate
- **ConfigStore Migration:** Properties → ConfigStore pattern (dashboard URL/PIN)
- **Housekeeping Cron:** scripts/run_housekeeping.sh (8h interval)

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

## AKTUELLE PRODUKTE & IHRE DOMÄNEN

Produkt | Tenant | Primäre Domäne | Berater | Status |
|---------|--------|----------------|---------|--------|
> ⚠️ **Historischer Snapshot (Stand 2026-07-26). Seit 2026-10-20 09:00 nicht mehr verifizierbar:** `KijanPersonalTracker` und `kijan-orchestrator` liegen im aktuellen Container **nicht mehr vor** (nur `KijanPersonalTracker-2` ohne `.git`). Diese Zeilen sind Kontext, **kein aktueller Status**.
Produkt | Tenant | Primäre Domäne | Berater | Status |\n|||||||||||---------|--------|----------------|---------|--------|\n||||||||| Kijan Personal Tracker | kijan | Gesundheits-Tracking, ME/CFS, Schmerz | Med, Psych, Schmerz, ME/CFS | **ACTIVE** — kpt-backend **ON dev(5260991), 327 behind origin/dev** — kpt-app-ciq **HERMES(e73048a) v0.90.5 — 378 total** — Router Growth: personal **104KB** (-63KB ⚡), activities **94KB** (-41KB ⚡), projects **51KB** — **MASSIVE IMPROVEMENT** |
HAL Module | kijan | Health Aggregation Layer | Medical | **PHASE 2 DEGRADING** — services reduced: `activity_aggregation`, `integrity_check`, `pattern_detection` **GONE** — only `activity_ranking_engine` + `pacing_engine` remain |
kijan-orchestrator-langgraph | kijan | LLM Orchestrator, Model Routing | Tech | **ACTIVE** — 134 total (22 py, 81 md) — docs cleanup — **STABLE** — v2.2.0 |
EdgeTxSync | kijan | EdgeTX Radio Sync, Log Analysis | Embedded | **PR #122 MERGED** — backend-client-separation — 110 py — HEAD 3136f06 — **STABLE** |
ESP32-Projects | embedded | Catfeeder, Current Sensor, Power Monitoring | Embedded | **3 REPOS ACTIVE** — 18 product files total — **STABLE** |
crypto-max | kijan | Crypto Arbitrage Research | Research | **11 product files** (1013L index.js) — research only — node_modules bloat (444 total incl. deps) |

### Kijan Submodule Status (2026-07-26 09:00)

Produkt | HEAD Commit | Branch | Unmerged (local) | Unmerged (remote) | Status |
---------|-------------|--------|------------------|--------------------|--------|
Main | `65c74e6` | hermes | **0** | **0** | ✅ **SYNCED** (keine neuen Commits seit 2026-07-03) |
kpt-backend | `5260991` | **dev** | **327** | **0** | ⚠️ **ON dev — 327 behind origin/dev** — Was DETACHED, NOW ON BRANCH — **MASSIVE STATE CHANGE** |
kpt-app-ciq | `e73048a` | hermes | **0** | **0** | ✅ **HERMES** — 221mc/29xml/26png/39md/378 total (was 1180!) — v0.90.5 |
kpt-doc | `8bd73de` | hermes | **11** | **30** | ⚠️ **DIVERGED** — **WIDENING** (was 10/30) |
kpt-admin | `6db642a` | HEAD | **0** | **0** | ✅ **SYNCED** — PR #3 merged |
kpt-common-barrels-ciq | `7999fb9` | HEAD | **0** | **0** | ✅ **SYNCED** |
kpt-datafield-ciq | `37127c4` | HEAD | **0** | **0** | ✅ **SYNCED** — v0.84.1 — **3 behind origin** |
kpt-symptoms-app | `1be73d4` | hermes | **0** | **0** | ✅ **SYNCED** |
kpt-website | `9514570` | hermes | **0** | **0** | ✅ **SYNCED** |
kpt-website-pre-release | `46d4492` | hermes | **3** | **0** | ⚠️ **3 behind origin/hermes** (was SYNCED) |

---

### Cross-Product Knowledge Hub

Stand: 2026-10-19 20:40 UTC
> Aktualisierung: alle 6h via Cron-Job
> Nächste Aktualisierung: 2026-10-19 23:40 UTC
> Gap seit letztem Stand: 32 Tage (2026-09-17 → 2026-10-19) — Cron still alive, vorheriger Run #N+10 hing laut Hub-Historie in Tool-Schleife ohne Output.

### Duplicates identifiziert und zusammengeführt

*Alle bereits in existierenden Skills konsolidiert — KEINE neuen Duplicates seit letztem Run.*
1. **EnergyScreen Audit** — Konsolidiert in `energy-screen-audit` Skill
2. **Submodule Divergence** — Konsolidiert in `hermes-branch-watcher`
3. **TASKS.md Overclaim / Fabricated-Complete** — Generalisiert in `task-claim-verification` + `hermes-branch-watcher`
4. **Branch-Offset-Monitoring** — Konsolidiert in `hermes-branch-watcher`
5. **Cron-Reliability Pattern** — In `cron-reliability` Skill
6. **i18n 9-Sprachen Pattern** — kpt-backend + kpt-app-ciq — cross-product applicable
7. **Knowledge Hub Cron Update** — In `knowledge-hub-cron-update` Skill
8. **Divergence Metric** — Submodule ahead values were all WRONG — new merge-base metric adopted across all entries

### Cross-Product Pattern Analysis (2026-07-26 09:00)

1. **i18n 9-Sprachen Pattern:** kpt-backend (9 JSON) + kpt-app-ciq (strings.xml 335L) — **identische 9 Sprachen** (DE/EN/FR/ES/IT ja/nl/pt/zh-CN) — **UNCHANGED**
2. **Monkey C method() deprecation:** **3 calls REMAINING** (TimeWindowMenuDelegate.mc:43,53,60) — **MAINTAINED** — no further progress
3. **kpt-app-ciq MASSIVE REDUCTION:** 221mc/29xml/26png/39md/**378** total (was 1180, **-802 files!** — 440mc, 56xml, 30png, 52md lost) — **v0.90.5** — **POSSIBLE SUBMODULE RESET — NEEDS INVESTIGATION**
4. **HAL v2 Status:** Phase 1 ✅ COMPLETE — Phase 2 ❌ **DEGRADING** — services reduced: `activity_aggregation`, `integrity_check`, `pattern_detection` **GONE from disk** — only `activity_ranking_engine` + `pacing_engine` remain
5. **Router Growth (MASSIVE IMPROVEMENT!):** personal.py **104KB** (-63KB ⚡), activities.py **94KB** (-41KB ⚡), projects.py **51KB** — **3 routers remain > 30KB** (auth_enhanced 24KB, pdf 22KB, metrics 14KB) — **SIGNIFICANT REDUCTION**
6. **kpt-backend app structure:** 36 py in app/ (routers 11, dal 6, services 3, jobs 3, root 13) — 78 py total (incl. alembic) — **REDUCED from 55 py**
7. **kpt-backend alembic:** 42 migrations (was 73, -31!) — alembic_activity(18), alembic_admin(13), alembic_health(7), alembic_projects(4) — **MASSIVE REDUCTION**
8. **EdgeTxSync:** 110 py — **STABLE** — HEAD 3136f06 (ETX-01 Docker/windows build artifacts) — PR #122 merged (backend-client-separation)
9. **kijan-orchestrator-langgraph:** 134 total (22 py, 81 md) — **REDUCED from 169** — docs cleanup — active dev: pytest suite, backup fixes, Redis/Qdrant auth
10. **kpt-backend NOW ON dev BRANCH:** Was DETACHED — now on dev (5260991) — **327 behind origin/dev** — **IMPROVEMENT**
11. **kpt-doc Divergence:** 11 AHEAD / 30 BEHIND (was 10/30) — **WIDENING**
12. **kpt-website-pre-release:** 3 commits behind origin/hermes — **CHANGED** (was SYNCED)
13. **ESP32 repos:** 18 product files total (11+6+1) — **STABLE** — BUG-001/002/003 synced
14. **catfeeder-mqtt:** 2 product files — **STABLE**
15. **Main repo: 327+ BEHIND vs origin/dev** — **IMPROVING** (was 747+)
16. **kpt-app-ciq worktrees bloat:** 680 files in .worktrees/ — **NOT product code** — real source: 249 files (219mc + 42 resources + docs/tests)

### Neue Erkenntnisse (2026-07-24 13:30)

1. **kpt-backend NOW ON dev BRANCH:** Was DETACHED (588fce1) — now on dev (5260991) — 327 behind origin/dev — **CRITICAL STATE CHANGE**
2. **kpt-backend services MASSIVELY REDUCED:** activity_aggregation, integrity_check, pattern_detection **GONE from disk** — only activity_ranking_engine + pacing_engine remain — **MASSIVE LOSS of domain logic**
3. **kpt-backend routers MASSIVELY SHRUNK:** personal.py 104KB (-63KB), activities.py 94KB (-41KB) — **314KB → 213KB total for 5 routers** — **SIGNIFICANT IMPROVEMENT**
4. **kpt-backend Alembic REDUCED:** 42 migrations (was 73, -31!) — alembic_activity(18), alembic_admin(13), alembic_health(7), alembic_projects(4)
5. **kpt-app-ciq MASSIVE FILE REDUCTION:** 221mc/29xml/26png/39md/378 total (was 1180, -802!) — **POSSIBLE SUBMODULE RESET — NEEDS INVESTIGATION**
6. **kijan-orchestrator-langgraph:** 134 total files (was 169) — docs cleanup
7. **kpt-doc divergence WIDENING:** 11 AHEAD / 30 BEHIND (was 10/30) — HEAD updated to `8bd73de` (scrumsync telemetry)
8. **kpt-website-pre-release:** 3 commits BEHIND origin/hermes (was SYNCED)
9. **Main repo: 327+ BEHIND vs origin/dev** — improving (was 747+)

### Skill-Registry (2026-07-17)

Name | Kategorie | Status | Cross-Product? |
------|-----------|--------|---------------|
holistic-dev-workflow | devops | ✓ aktiv | Ja |
kanban-orchestrator | devops | ✓ aktiv | Ja |
server-first-git-sync | devops | ✓ aktiv | Ja |
hermes-branch-watcher | devops | ✓ aktiv | **Ja** (branch-offset + fabricated-complete) |
docker-troubleshooting | devops | ✓ aktiv | Ja |
subagent-driven-development | devops | ✓ aktiv | Ja |
multi-model-routing | devops | ✓ aktiv | Ja |
kijanpersonal-tracker | kijan | ✓ aktiv | Nein |
kijan-health-module | kijan | ✓ aktiv | Nein |
health-aggregation-layer | kijan | ✓ aktiv | **Ja** |
kijan-personal-tracker-debug | kijan | ✓ aktiv | **Ja** |
energy-screen-audit | kijan | ✓ existiert | **Ja** |
task-claim-verification | kijan | ✓ existiert | **Ja** |
cron-reliability | devops | ✓ existiert | **Ja** |
connect-iq-development | gaming | ✓ existiert | **Ja** |
rc-aircraft-cad | embedded | ✓ existiert | **Ja** |
medizinischer-berater | medizinisch | ✓ aktiv | Ja |
psychologischer-berater | psychologisch | ✓ aktiv | Ja |
schmerzpatient | medizinisch | ✓ aktiv | Ja |
me-cfs-patient | medizinisch | ✓ aktiv | Ja |

---

## WISSENSaustausch-MECHanismen

1. **Automatisch:** Cron-Job aggregiert alle 6h alle Boards
2. **Manuell:** `hermes kanban list --tenant {name}` für Produkt-Status
3. **Push:** Bei wichtigen Insights sofortiger Cross-Project Alert
4. **Pull:** Orchestrator lädt relevante Skills/Knowledge vor Task-Ausführung

---

## SKILL-REGISTRY

### Aktive Skills
(alle Skills aus oben → unverändert)

### Neue Erkenntnisse (2026-07-24 13:30)

#### process_insights (CHANGED — MASSIVE STATE CHANGES)
1. **kpt-backend NOW ON dev BRANCH:** Was DETACHED — now on dev (5260991) — 327 behind origin/dev — **CRITICAL STATE CHANGE** — **CHANGED**
2. **kpt-backend services MASSIVELY REDUCED:** activity_aggregation, integrity_check, pattern_detection **GONE** — only activity_ranking_engine + pacing_engine remain — **MASSIVE LOSS** — **CHANGED**
3. **kpt-backend routers MASSIVELY SHRUNK:** personal 104KB (-63KB), activities 94KB (-41KB) — **SIGNIFICANT IMPROVEMENT** — **CHANGED**
4. **kpt-backend Alembic REDUCED:** 42 migrations (was 73, -31!) — **CHANGED**
5. **kpt-app-ciq MASSIVE FILE REDUCTION:** 378 total (was 1180, -802!) — **POSSIBLE SUBMODULE RESET** — **CHANGED**
6. **kpt-doc divergence WIDENING:** 11 AHEAD / 30 BEHIND (was 10/30) — **CHANGED**
7. **kijan-orchestrator-langgraph:** 134 total files (was 169) — docs cleanup — **CHANGED**
8. **kpt-website-pre-release:** 3 commits behind origin/hermes — **CHANGED**
9. **Main repo: 327+ BEHIND vs origin/dev** — improving (was 747+) — **CHANGED**
10. **kpt-app-ciq version v0.90.5** — **CHANGED**
11. **EdgeTxSync backend-client separation merged** — **CHANGED**

#### risk_patterns updates (CHANGED)
1. **kpt-backend: ON dev(5260991), 327 behind origin/dev** — Was DETACHED — **MASSIVE IMPROVEMENT** — **CHANGED**
2. **Router Growth MASSIVE IMPROVEMENT:** personal **104KB** (-63KB ⚡), activities **94KB** (-41KB ⚡), projects **51KB** — **CHANGED** (slight reduction → massive reduction)
3. **kpt-backend services REMOVED:** activity_aggregation, integrity_check, pattern_detection GONE — **CRITICAL RISK** — **CHANGED**
4. **Alembic 42 migrations (REDUCED):** alembic_activity(18), alembic_admin(13), alembic_health(7), alembic_projects(4) — **CHANGED** (was 73)
5. **kpt-app-ciq MASSIVE REDUCTION:** 378 total (was 1180) — **POSSIBLE SUBMODULE RESET** — **CHANGED**
6. **kpt-doc: DIVERGED(11,30)** — **WIDENING** — **CHANGED**
7. **kpt-website-pre-release: 3 BEHIND** — **CHANGED** (was SYNCED)

#### technical_patterns updates (CHANGED)
1. **Router Growth MASSIVE IMPROVEMENT:** personal.py **104KB** (-63KB ⚡), activities.py **94KB** (-41KB ⚡), projects.py **51KB** — **3 routers > 30KB** (auth_enhanced 24KB, pdf 22KB, metrics 14KB) — **CHANGED** (slight → massive reduction)
2. **kpt-backend NOW ON dev BRANCH:** Was DETACHED — now on dev (5260991) — **CHANGED** (was DETACHED)
3. **kpt-backend app structure:** 36 py in app/ (routers 11, dal 6, services 3, root 13) — **REDUCED from 55 py** — **CHANGED**
4. **kpt-backend services:** Only 2 remain — activity_ranking_engine, pacing_engine — **CHANGED**
5. **kpt-backend Alembic:** 42 migrations (was 73, -31!) — **CHANGED**
6. **kpt-app-ciq MASSIVE REDUCTION:** 221mc/29xml/26png/39md/378 total (was 1180, -802!) — **POSSIBLE SUBMODULE RESET** — **CHANGED**
7. **Monkey C method() deprecation:** **MAINTAINED at 3 calls** — no further progress — **UNCHANGED**
8. **kijan-orchestrator-langgraph:** 134 total (was 169) — docs cleanup — **CHANGED**
9. **EdgeTxSync:** 110 py — **STABLE** — HEAD 3136f06 — **CHANGED**
10. **kpt-doc HEAD:** 8bd73de (scrumsync telemetry) — **CHANGED** (was 5a96920)
11. **HAL Phase 2 DEGRADING:** activity_aggregation, integrity_check, pattern_detection **GONE from disk** — only 2 services remain — **CHANGED**
12. **EdgeTxSync Backend-Client Separation:** Merged PR #122 — **CHANGED**

### Neue Erkenntnisse (2026-07-26 09:00)

1. **kpt-backend NOW ON dev BRANCH:** Was DETACHED — now on dev (5260991) — 327 behind origin/dev — **CRITICAL STATE CHANGE**
2. **kpt-backend services MASSIVELY REDUCED:** activity_aggregation, integrity_check, pattern_detection **GONE** — only activity_ranking_engine + pacing_engine remain — **MASSIVE LOSS**
3. **kpt-backend routers MASSIVELY SHRUNK:** personal 104KB (-63KB), activities 94KB (-41KB) — **SIGNIFICANT IMPROVEMENT**
4. **kpt-backend Alembic REDUCED:** 42 migrations (was 73, -31!)
5. **kpt-app-ciq MASSIVE FILE REDUCTION:** 378 total (was 1180, -802!) — **POSSIBLE SUBMODULE RESET**
6. **kpt-doc divergence WIDENING:** 11 AHEAD / 30 BEHIND — **CHANGED**
7. **kijan-orchestrator-langgraph:** 134 total files (was 169) — docs cleanup — **CHANGED**
8. **kpt-website-pre-release:** 3 commits behind origin/hermes — **CHANGED**
9. **Main repo: 327+ BEHIND vs origin/dev** — improving (was 747+) — **CHANGED**
10. **kpt-app-ciq version v0.90.5** — **CHANGED**
11. **EdgeTxSync backend-client separation merged** — **CHANGED**
12. **kpt-backend app structure:** 36 py in app/ (routers 11, dal 6, services 3, root 13) — **REDUCED from 55 py**
13. **HAL Phase 2 DEGRADING:** activity_aggregation, integrity_check, pattern_detection **GONE from disk** — only 2 services remain

### Cross-Product Analysis (2026-09-13 11:40)

**Status 2026-09-13 11:40 UTC — verifiziert live (Knowledge-Hub-Cron, alle 6h):**

**Process Insights:**
- Kanban-Boards leer (0 Tasks in allen Workspaces) — keine neue Board-Aktivität seit letztem Lauf.
- state.db um +36% gewachsen (3.411.968 → 4.624.384 bytes) seit letztem Lauf 05:25 UTC — anhaltendes Wachstum durch Agent-Betrieb (Sessions/Messages akkumulieren), kein Board-Task-Korrelat (Boards weiterhin leer).
- Sessions/Messages pro Profil unverändert seit letztem Lauf.
- **Pipe-Noise-Korruption (HUB DATENKORROSION #3): 18 Zeilen mit `|`-Prefix-Runs (2–5 pipes) bereinigt** — erneut aufgetreten trotz Cleanup im Vorlauf; Ursache unverändert ein Markdown-Renderer/Editor-Schritt. Gegenmaßnahme: grep-Check `^\|{2,}` bei jedem Lauf als fester Bestandteil von Step 0.

**Live-Metriken (frisch gemessen, lt. Pre-Write-Validation-Gate):**
- Skills: 233 SKILL.md
- state.db: 4.624.384 bytes (Haupt-.hermes/state.db, +36% ggü. 3.411.968); Profil-DBs unverändert: architect 17.170.432, devops 2.154.496, kpt 4.001.792, rc-aircraft-cad 3.043.328, web-development 245.760
- Kanban tasks: 0 (alle Boards leer)
- Sessions/Messages per Profil: architect 206/588, devops 13/293, kpt 13/240, rc-aircraft-cad 2/283, web-development 0/0
- Checkpoint .json Dateien: 0 (store/projects leer)

**Patterns:** Keine neuen produktübergreifenden Muster aus Boards extrahierbar (keine Board-Daten). Bestehende Muster (HAL v2.0, Router-Splitting, Alembic-Idempotenz, kanban-orchestrator, subagent-driven-development, UUIDv7, Pearson-Korrelation) bleiben gültig und wiederverwendbar. **Wiederverwendbares Muster dieses Laufs:** mehrstufige Pipe-Noise-Korruptions-Reparatur (grep-Detection → Python-Regex-Strip, kein replace_all) — in `knowledge-hub-maintenance` Skill dokumentiert.

**Neue Erkenntnisse:** Keine produktübergreifenden Board-Erkenntnisse (alle Boards leer). Änderungen seit letztem Lauf: (1) state.db-Wachstum +51% ohne Board-Aktivität (Agent-Betrieb akkumuliert State-Daten), (2) erneutes Auftreten der Pipe-Noise-Korruption (18 Zeilen) — beobachtenswert und durch festen Check in Step 0 der Maintenance abzufangen. Nächster Lauf in 6h.
### Cross-Product Analysis (2026-09-14 13:14)

**Status 2026-09-14 13:14 UTC — verifiziert live (Knowledge-Hub-Cron, alle 6h):**

**Process Insights:**
- Kanban-Boards leer (0 Tasks in allen Workspaces) — keine neue Board-Aktivität seit letztem Lauf. Bestätigt über sqlite3-Query auf .hermes/kanban.db (tasks/events/runs je 0).
- **Live-Metriken (frisch gemessen):**
  - Skills: 233 SKILL.md (stabil, unverändert ggü. Vorlauf)
  - state.db (Haupt-.hermes/state.db): **6.688.768 bytes**, +44.7% ggü. Vorlauf (4.624.384) — anhaltendes Wachstum durch Agent-Betrieb (Sessions/Messages akkumulieren), kein Board-Task-Korrelat (Boards weiterhin leer). Profil-DBs unverändert: architect 17.170.432, devops 2.154.496, kijan-personal-tracker 4.001.792, rc-aircraft-cad 3.043.328, web-development 245.760.
- Kanban tasks: 0 (alle Boards leer)
- Session/Messaging: keine neue Board-Aktivität.
- **Pipe-Noise-Korruption: KEIN Befund** — grep-Check `^|` liefert 0 Zeilen mit Pipe-Prefix-Runs. Frühere Korruption (18 Zeilen, Datenkorrosion #3) derzeit nicht erneut aufgetreten; fester Check in Step 0 bleibt aktiv.

**Duplicates:** Keine neuen Duplicates über Produkte hinweg identifiziert. Bestehende Duplicate-Konsolidierungen (EnergyScreen→energy-screen-audit, Submodule Divergence→hermes-branch-watcher, TASKS.md Overclaim→task-claim-verification) bleiben gültig und in Skills verankert.

**Patterns:** Keine neuen produktübergreifenden Muster aus Boards extrahierbar (keine Board-Daten). Bestehende wiederverwendbare Muster (HAL v2.0, Router-Splitting, Alembic-Idempotenz, kanban-orchestrator, subagent-driven-development, UUIDv7, Pearson-Korrelation) bleiben gültig. **Beobachtung:** anhaltendes state.db-Wachstum (+45% in einem 25h-Fenster) ohne Board-Korrelat ist ein wiederkehrendes Signal — relevant für state-db-acceleration-response / state-db-cleanup Skills.

**Skills:** Keine neuen Skills erforderlich — erkannte Muster sind bereits in existierenden Skills verankert. Wartung bestehender Skills (state-db, knowledge-hub) fortgeführt.

### Cross-Product Analysis (2026-09-14 19:35)

**Status 2026-09-14 19:35 UTC — verifiziert live (Knowledge-Hub-Cron, alle 6h):**

**Process Insights:**
- Kanban-Boards leer (0 Tasks in allen Workspaces) — keine neue Board-Aktivität seit letztem Lauf. Bestätigt über sqlite3-Query auf .hermes/kanban.db (tasks/events/runs je 0).
- **Live-Metriken (frisch gemessen):**
  - Skills: 233 SKILL.md (stabil, unverändert ggü. Vorlauf)
  - state.db (Haupt-.hermes/state.db): **7.585.792 bytes**, +13.4% ggü. Vorlauf (6.688.768), kumuliert +64% ggü. 2026-09-13 (4.624.384) — anhaltendes Wachstum durch Agent-Betrieb (Sessions/Messages akkumulieren), kein Board-Task-Korrelat (Boards weiterhin leer).
  - Profile-DBs unverändert: architect 17.170.432, devops 2.154.496, kijan-personal-tracker 4.001.792, rc-aircraft-cad 3.043.328, web-development 245.760.
  - Checkpoints: 20 Dateien in .hermes/checkpoints. store/-Checkpoint-JSON: 0 (Pfad .hermes/store existiert nicht mehr — Checkpoint-Store-Collapse weiterhin zutreffend, keine .json-Dateien).
  - Sessions: 1.782 .json in .hermes/sessions.
- Session/Messaging: keine neue Board-Aktivität.

**Duplicates:** Keine neuen Duplicates über Produkte hinweg identifiziert. Bestehende Duplicate-Konsolidierungen (EnergyScreen→energy-screen-audit, Submodule Divergence→hermes-branch-watcher, TASKS.md Overclaim→task-claim-verification) bleiben gültig und in Skills verankert.

**Patterns:** Keine neuen produktübergreifenden Muster aus Boards extrahierbar (keine Board-Daten). Bestehende wiederverwendbare Muster (HAL v2.0, Router-Splitting, Alembic-Idempotenz, kanban-orchestrator, subagent-driven-development, UUIDv7, Pearson-Korrelation) bleiben gültig. **Beobachtung:** state.db-Wachstum setzt sich fort (+13.4% in diesem 6h-Fenster) — beschleunigtes Wachstum ist ein wiederkehrendes, aktives Signal; relevant für state-db-acceleration-response / state-db-cleanup Skills. Der 2026-09-13 11:40 und 13:14 gemeldete Anstieg wird hier als Fortsetzung bestätigt (kein Abbruch/Shrink).

**Skills:** Keine neuen Skills erforderlich — erkannte Muster sind bereits in existierenden Skills verankert (state-db, knowledge-hub). Wartung bestehender Skills fortgeführt. Keine neuen wiederverwendbaren Erkenntnisse, da keine Board-Aktivität vorliegt.

### Cross-Product Analysis (2026-09-17 07:40)

**Status 2026-09-17 07:40 UTC — verifiziert live (Knowledge-Hub-Cron, alle 6h):**

**Process Insights:**
- Kanban-Boards leer (0 Tasks, 0 Events, 0 Runs in allen Tabellen) — **>96 Tage kontinuierlich leer** (seit 2026-08-02). Keine Board-Aktivität für cross-produktive Analyse verfügbar.
- **state.db-Wachstum setzt sich deutlich fort:** Haupt-.hermes/state.db **11.853.824 bytes** (+56.4% ggü. Vorlauf 7.585.792, +156% ggü. 2026-09-13 4.624.384). Wachstum komplett durch Agent-Betrieb (Sessions/Messages akkumulieren), kein Board-Task-Korrelat (Boards weiterhin seit >96 Tagen leer).
- **f3k-design:** Kein Git-Repo (kein `.git` vorhanden), nur statische Dateien — keine Branch-Divergenz analysierbar. Zuletzt Jun 2026.
- **kijan-steuern:** Letzter Commit 2026-08-02 (>45 Tage inaktiv), keine Commits in 30/90 Tagen. Stiller Status.
- Pipe-noise-Korruption: **KEIN Befund** — `grep -cE '^\|{2,}'` = 0 Zeilen. Fester Check in Step 0 bleibt aktiv.
- Checkpoint .json Dateien: 2 in `.hermes/checkpoints/` (Checkpoint-Store-Collapse weiterhin zutreffend: keine `.json` in store/).
- Sessions: 1.788 `.json` in `.hermes/sessions/`.

**Live-Metriken (frisch gemessen, lt. Pre-Write-Validation-Gate):**
- Skills: **233 SKILL.md** (stabil — 52 Kategorien, davon 43 in `devops/`). Top: devops 43, software-development 26, productivity 21, creative 19, mlops 17.
- state.db: 11.853.824 bytes (+56.4% in 6h-Fenster; kumuliert +156% seit 2026-09-13).
- Kanban tasks/events/runs: 0 (alle Boards leer).
- Checkpoint .json: 2 (in `/workspace/.hermes/checkpoints/`).
- Sessions .json: 1.788.
- Accessible repos: `kijan-steuern` (inaktiv, letzter Commit 2026-08-02), `f3k-design` (kein Git, statisch). Kijan-Produkt-Submodule auf `/data/Github/` — nicht aus Container erreichbar (Stand 2026-08-04 unverändert).

**Duplicates:** Keine neuen Duplicates über Produkte hinweg identifiziert. Bestehende Duplicate-Konsolidierungen (EnergyScreen→energy-screen-audit, Submodule Divergence→hermes-branch-watcher, TASKS.md Overclaim→task-claim-verification) bleiben gültig und in Skills verankert.

**Patterns:** Keine neuen produktübergreifenden Muster aus Boards extrahierbar (keine Board-Daten). Bestehende wiederverwendbare Muster (HAL v2.0, Router-Splitting, Alembic-Idempotenz, kanban-orchestrator, subagent-driven-development, UUIDv7, Pearson-Korrelation) bleiben gültig. **Beobachtung:** state.db-Wachstum (+56% in 6h) setzt das wiederkehrende Beschleunigungssignal fort — relevanter Kontext für `state-db-acceleration-response` / `state-db-cleanup` Skills. Board-Empty-Since 2026-08-02 (>96 Tage) ist der dominante strukturelle Zustand des Hubs.

**Skills:** Keine neuen Skills erforderlich — erkannte Muster sind bereits in existierenden Skills verankert (state-db, knowledge-hub). Wartung bestehender Skills fortgeführt.

**FALLBACK-EXTRACTED (source=git_fallback):** Kijan-Produkt-Submodule (kpt-backend, kpt-app-ciq, kpt-doc etc.) auf Host-Pfad `/data/Github/` — nicht aus Container erreichbar. Kijan-steuern-Repo: letzte Aktivität 2026-08-02, seitdem keine Commits. f3k-design: kein Git-Repo, nur statische Dateien.

### Cross-Product Analysis (2026-10-19 20:40)

**Status 2026-10-19 20:40 UTC — verifiziert live (Knowledge-Hub-Cron, alle 6h):**

**Process Insights:**
- Kanban-Boards weiterhin leer — `kanban.db` (122.880 bytes, mtime 2026-09-21) hat **0 Tasks / 0 Events / 0 Runs / 0 Comments / 0 Links / 0 Attachments**. Boards leer seit **>116 Tagen** (Stand 2026-10-19, +20 Tage vs. 2026-09-17-Eintrag). Schema vorhanden (6 Tabellen), aber kein Schreiber. **Stale-DB-Signal:** kanban.db selbst wächst seit 21 Tagen nicht mehr (last write 2026-09-21) — kein aktiver Worker, kein stiller Writer.
- **state.db-Wachstum setzt sich ungebremst fort — +1.167 % in 32 Tagen:** `/workspace/.hermes/state.db` jetzt **150.118.400 bytes** (vs. 11.853.824 bytes am 2026-09-17). Auch im aktuellen 6h-Fenster erneut +1.7 MB (+1.1 %). Wachstum komplett Agent-getrieben (Sessions/Messages), weiterhin KEIN Board-Task-Korrelat. **Relevanz:** das ist jetzt nicht mehr „Beschleunigungssignal", sondern **dauerhafter Defaultzustand** — `state-db-acceleration-response` Skill bleibt unverändert relevant; neue Kontextnotiz für `kanban-orchestrator` wäre, dass Task-Writer-Pfad aktuell stillsteht.
- **Skill-Indexierungs-Sprung: 233 → 5.339 SKILL.md in 32 Tagen.** Vorher wurde nur `hermes-agent/optional-skills/` gezählt (213). Jetzt sichtbar: 1.201 in `/workspace/.hermes/skills/`, 3.910 in `/workspace/.hermes/profiles/*/skills/` (34 Profile × ~115/Skill-Mirror = Duplikate), 213 in `hermes-agent/`, 15 elsewhere. **Befund:** die ~3.900 Profile-Skills sind Mirror-Kopien der zentralen Skills (Plattform-Pattern: jede Profil-Session bekommt eigenen Skill-Stand). **Drift-Risiko**: Mirror-Kopien divergieren potenziell vom Upstream — `profile-skill-drift-monitor` Skill ist genau dafür zuständig; kein neuer Skill nötig, aber **Erinnerung im Hub** sinnvoll.
- **Aktive Profile: 34** (apple, architect, arzt, autonomous-ai-agents, creative, data-science, devops, …, ui-ux-designer, web-dashboard-migration, web-development). Kein „default" als Verzeichnis vorhanden — Active-Profile-Auswahl erfolgt zur Laufzeit.
- **Accessible Repos verändert:** `kijan-steuern` (weiterhin inaktiv seit 2026-08-02) + **`jan-assistant`** (jetzt neu in `/workspace/Github/jan-assistant/.git`) — `f3k-design` taucht nicht mehr unter `.git`-Verzeichnissen auf, war zuletzt nur statisch gemeldet. `/data/Github/`: weiterhin nicht erreichbar (Container-Grenze, unverändert seit 2026-08-04).
- **Sessions: 1.849** `.json` (+61 in 32 Tagen), **Checkpoints: 4** `.json` (+2 seit Sep 17), **store/: 0** (weiterhin collapse).

**Live-Metriken (frisch gemessen, lt. Pre-Write-Validation-Gate):**
- Skills gesamt: **5.339 SKILL.md** (.hermes-weit, inkl. Profile-Mirrors)
- state.db: **150.118.400 bytes** (+12.7× vs. 2026-09-17; +1.7 MB seit vorheriger Hub-Messung im 6h-Fenster)
- Kanban tasks/events/runs/comments/links/attachments: **0 / 0 / 0 / 0 / 0 / 0**
- Kanban-DB-mtime: **2026-09-21 05:45** (still seit 21 Tagen — kein aktiver Worker)
- Checkpoint `.json`: **4** in `.hermes/checkpoints/`, **0** in `store/` (Collapse andauernd)
- Sessions `.json`: **1.849** (+61 seit 2026-09-17)
- Profile aktiv: **34** (kein „default"-Verzeichnis)
- Accessible Git-Repos: `kijan-steuern` (letzter Commit 2026-08-02, inaktiv), `jan-assistant` (neu sichtbar). Kijan-Produkt-Submodule auf `/data/Github/` — nicht aus Container erreichbar (unverändert).

**Duplicates:** Keine neuen Duplicates. Bestehende Konsolidierungen (EnergyScreen→energy-screen-audit, Submodule Divergence→hermes-branch-watcher, TASKS.md Overclaim→task-claim-verification) bleiben gültig. Mirror-Skills in Profiles sind KEINE fachlichen Duplicates, sondern Plattform-Pattern — kein Konsolidierungsbedarf.

**Patterns:**
- **Board-Empty-Since 2026-08-02 = >116 Tage** ist der dominante strukturelle Zustand — nicht mehr „Beschleunigungssignal", sondern **etablierter Default**. Cross-Product-Analyse ohne Board-Daten weiterhin nur via git_fallback möglich.
- **state.db-Wachstum ist dauerhafter Zustand**, nicht mehr Einzelfall. Der vorherige Hub-Eintrag listete „+56.4 % in 6h" als Signal — das wiederholt sich alle 6h und ist deshalb kein Signal mehr, sondern das neue Normalmaß.
- **Profile-Skill-Mirrors** (3.910 zusätzliche SKILL.md) sind neu sichtbar im Index und sollten bei jeder zukünftigen Drift-Suche berücksichtigt werden — `profile-skill-drift-monitor` ist die richtige Adresse.

**Skills:** Keine neuen Skills erforderlich. Bestehende Skills (`profile-skill-drift-monitor`, `state-db-acceleration-response`, `kanban-orchestrator`, `kanban-workflow-revival`) decken die neuen Beobachtungen ab; keine Updates nötig.

**FALLBACK-EXTRACTED (source=git_fallback):** Kijan-Produkt-Submodule unverändert nicht aus Container erreichbar. `jan-assistant` jetzt zusätzlich sichtbar (war in Hub-Stand 2026-09-17 nicht aufgeführt).

---

### Cross-Product Analysis (2026-10-20 09:00)

**Board-Rotation:** kpt, orchestrator (2 von N — bewusst gekürzt, Output-Budget)

#### 1. Boards weiterhin LEER — Ursache jetzt präzisiert (neu)
- `kanban.db` `/workspace/.hermes/kanban.db`: **alle 6 Tabellen 0 Zeilen** (tasks, task_events, task_runs, task_comments, task_links, task_attachments). DB-File 122 KB, **mtime 2026-09-21** — seit ~1 Monat *null* Schreibzugriffe.
- **NEU gegenüber Vorlauf:** Es existieren **drei** kanban.db-Pfade. `/workspace/.hermes/kanban/kanban.db` (0 B) und `/workspace/kanban.db` (0 B) sind **leere Platzhalter** ohne `tasks`-Tabelle. Nur `/workspace/.hermes/kanban.db` ist die echte DB.
- **Konsequenz für Agents:** Werkzeuge, die `kanban/kanban.db` oder `./kanban.db` suchen, schlagen mit "no such table" fehl und werden fälschlich als "Board leer" interpretiert. **Immer gegen `/workspace/.hermes/kanban.db` prüfen.** Das erklärt vermutlich einen Teil der seit 2026-09-17 wiederkehrenden "alle Boards leer"-Meldungen.

#### 2. Produkt-Board-Ersatz: Repos verschoben/fehlend (neu, wichtig)
- `/workspace/Github/KijanPersonalTracker` **existiert nicht mehr**; nur noch `/workspace/Github/KijanPersonalTracker-2` — und dort **kein `.git`** (kein Repo-Stand prüfbar).
- `/workspace/Github/kijan-orchestrator` **existiert nicht** (kein Treffer, auch kein Namensmuster).
- Verfügbare Repos im Container: `jan-assistant` (main, `80c4479`, 2 Commits, 1 dirty), `kijan-steuern` (main, `e0ea499`, 12 Commits, clean), `f3k-design`.
- **Insight:** Der Hub-Produktblock (Zeilen 190–210) beschreibt KPT-Submodule mit Ständen vom 2026-07-26. Diese Werte sind **nicht mehr verifizierbar** — sie sollten als historisch markiert werden, nicht als aktueller Stand. Der git_fallback-Pfad ist für KPT derzeit **wirkungslos**.

#### 3. Live-Metriken (kpt-/orchestrator-unabhängig)
- `state.db`: **157,2 MB** (157.175.808 B) — weiteres Wachstum gegenüber 156,9 MB im Vorlauf, **aktiv** (mtime 08:50, ~10 min vor diesem Lauf).
- Skills: **5.238** SKILL.md in `.hermes` = 1.196 global + **3.814 in 34 Profilen**. Verteilung stabil.
- `sessions/*.json`: 1.849 (unverändert), `checkpoints/`: 0, `store/`: 0.
- Disk: `/workspace` 250 GB, **207 GB belegt (83 %)**, 44 GB frei. Der letzte Punkt ist neu und relevant — `state-db-cleanup`/`checkpoints-cleanup` sollten bei 90 % Priorität bekommen, nicht erst dann.

#### 6. NEU: beide Knowledge-Hub-Git-Remotes sind tot — kanonisches Repo ist `kijan007-agent/kijan-hermes-shared`
Die in den lokalen Clones konfigurierten Remotes existieren **nicht mehr**:
- `/workspace/.hermes/workflows` → `https://github.com/kijan007/kijan-hermes-shared-workflows.git` → **404 Repository not found**
- `/workspace/.hermes/skills` → `https://github.com/kijan007/kijan-hermes-shared-skills.git` → **404 Repository not found**

Der Token in `/workspace/.git-credentials` (User `kijan007`, 44 Repos sichtbar) hat Zugriff auf **44 Repos**; ein Tree-Scan über alle findet `KNOWLEDGE-HUB.md` **nirgends** remote — das einzige kanonische Shared-Repo ist **`kijan007-agent/kijan-hermes-shared`** (Branches `main`/`dev`, 799 Pfade, `devops/holistic-dev-workflow/references/knowledge-hub-*.md` vorhanden). Dort liegt die Hub-Datei künftig unter **`devops/holistic-dev-workflow/KNOWLEDGE-HUB.md`**, der Skill unter **`devops/knowledge-hub-maintenance/SKILL.md`** (im Shared-Repo bisher **nicht** vorhanden → neu angelegt). Auch `gh` ist in diesem Container **nicht installiert** (`/usr/bin/gh: not found`), der Credential-Helper `gh auth git-credential` läuft ins Leere → **Push via `git push` unmöglich**.

**Workaround (verifiziert):** Lieferung über die GitHub-Contents-API (Token aus `.git-credentials`, `PUT /repos/{repo}/contents/{path}` mit `sha` des bestehenden Blobs) — Commits `5c681e9a` (KNOWLEDGE-HUB.md) und `0f779fdd` (knowledge-hub-maintenance/SKILL.md) auf `main`, Byte-Hashes anschließend gegen `raw.githubusercontent.com` verifiziert (MATCH). Der lokale Clone `/workspace/.hermes/workflows` bleibt **2 Commits vor origin** (Push blockiert) — die Inhalte sind identisch, nur die Ablage ist neu.

**Konsequenz für die Kette:** Der `knowledge-hub-maintenance`-Skill ist im Shared-Repo **neu**, die `knowledge-hub-*-references` liegen unter `devops/holistic-dev-workflow/references/` — die Skill-Verzeichnisstruktur der lokalen Clones (`/workspace/.hermes/skills` mit 1.214 Skills) entspricht **nicht** der Shared-Repo-Struktur (799 Pfade). Vor künftigen Hub-Commits muss das Ziel-Repo und der Zielpfad geprüft werden, nicht blind `git push` aus dem lokalen Clone.

**Neue Erkenntnisse:** (a) Zwei leere 0-Byte-`kanban.db`-Dateien als Fehlerquelle identifiziert; (b) KPT-/Orchestrator-Repos im Container nicht mehr vorhanden → Produktblock im Hub ist veraltet, nicht "unverändert"; (c) Plattenbelegung 83 % als neuer Watchpoint.

**Skills:** Keine neuen Skills. Bestehende decken ab: `kanban-board-audit` (leere-DB-Prüfung), `state-db-acceleration-response`, `missing-repos-detection` (jetzt direkt passend für KPT/Orchestrator-Fehlstellen), `profile-skill-drift-monitor`, `git-workspace-maintenance`. Kein Skill-Update nötig — der Fall ist bereits beschrieben, es fehlt nur die Bestätigung im Hub.

**FALLBACK-EXTRACTED (source=git_fallback):** `jan-assistant` unverändert bei `80c4479` (1 dirty file), `kijan-steuern` unverändert clean bei `e0ea499`; KPT/Orchestrator nicht prüfbar (Repos fehlen bzw. ohne `.git`).

---

### Cross-Product Analysis (2026-10-20 21:00)

**Board-Rotation:** kijan-steuern, jan-assistant (2 von N — bewusst gekürzt, Output-Budget)

#### 1. NEU: Cron-Layer ist der einzige aktive Signal-Treiber (3 Fehlerjobs)
Der Board-Layer ist tot, aber der **Cron-Layer produziert jetzt messbare Insights** — bisher im Hub nicht erfasst:
- `oauth-refresh` (`*/30 * * * *`, `deliver: local`): `last_status: error` vom 2026-10-20 10:07. Grund: **3 Refresh-Skripte existieren, das im Cron-Prompt genannte `refresh_google_token.py` ist kaputt** (zeigt auf die nicht existierende `google_oauth_token.json` (Einzahl), erwartet `client_id`/`client_secret` *im Token-File*, kein `installed`-Parsing). Der funktionierende Pfad ist `cache/oauth_refresh_run.py`. Zusätzlich: `google_oauth_tokens.json` hat **kein `expires_at`**, nur `last_refresh` + `expires_in` → jeder Zyklus refresht unnötig (`REFRESH: no_expiry`).
- `bounce-filter-monitor` (`0 9 * * 1`): `last_status: error` vom 2026-10-19 — *"Alle Cloud-Provider und Peer-Fallbacks sind nicht verfügbar. Kein LLM konnte die Anfrage bedienen."* → **Provider-Ausfall, nicht Logik-Bug.**
- `projekte-hub-ideas-sync` (alle 2h, 08–22 Uhr): `last_status: error` seit **2026-08-02** (HTTP 500) — läuft weiter, ist aber seit 2,5 Monaten blind. Der Nachfolger `projekte-hub-ideas-sync-gated` (`29 * * * *`) läuft sauber.
- `email-calendar-sync`: pausiert, letzter Fehler `cannot import name 'ledger_transaction' from 'cron.executions'` — **API-Drift** (Hermes-Update ohne Skill-Angleichung), nicht Datenproblem.
- Zustandsbild: 10 Jobs `scheduled`/`ok`, 4 `paused`, 3 `error`. `failure_streak` bei oauth-refresh inzwischen 0 (selbstheilend).

**Insight:** Bei leerem Board ist der **Cron-Job-Status der einzige operativ verwertbare Signal-Treiber** — er ist billiger zu lesen (1 JSON) als Repos und liefert Fehler mit konkreten Ursachen. Das sollte ein fester Bestandteil des Aggregators werden (aktuell nur `state.db` + Skills + Repos).

#### 2. NEU: Zwei weitere 0-Byte-`kanban.db`-Platzhalter inzwischen datiert
Bekannt war `/workspace/.hermes/kanban/kanban.db` (0 B) und `/workspace/kanban.db` (0 B). Neu datiert: **`/workspace/.hermes/kanban/kanban.db` mtime 2026-10-15 02:35**, **`/workspace/kanban.db` mtime 2026-10-13 20:25** — beide werden also *noch immer angelegt/touchiert*, obwohl die echte DB seit 2026-09-21 unbeschrieben ist. Das heißt: **irgendein Prozess legt die Platzhalter regelmäßig neu an** — nicht nur Altlasten. `kanban-board-audit` deckt das bereits ab, ist aber mit „Path prüfen" zu unspezifisch; der Fix wäre, die Erzeuger zu identifizieren.

#### 3. NEU: `KijanPersonalTracker-2` ist kein abgeschnittener Klon, sondern ein Fragment
`/workspace/Github/KijanPersonalTracker-2` enthält **exakt 2 Dateien**, beide vom 2026-09-18: `kpt-backend/scripts/reporting/__init__.py` (6,4 KB) und `kpt-backend/scripts/reporting/pem_analysis.py` (7,9 KB). Kein `.git`, kein `kpt-backend`-App-Code, keine Submodule, keine CIQ-App. **Das ist kein „Repo verschoben"**, sondern ein fragmentarischer Auszug — vermutlich eine bewusste Teil-Extraktion (Reporting/PEM-Analyse). **Konsequenz:** Der git_fallback-Pfad ist für KPT nicht nur wirkungslos, sondern **strukturell unmöglich** — es fehlt die Repo-Historie, nicht nur der Remote. KPT-Status-Aussagen im Hub (Zeilen 190–212) bleiben historisch und sind aus diesem Container **nicht reaktivierbar**, ohne das Original-Repo neu zu klonen.

#### 4. NEU: `kijan-steuern` — `inbox/` ist gefüllt, aber nicht sortiert (Steuer-Frist)
`CH-Steuern 2025/inbox/` enthält **56 Dateien** (Handy-Fotos/Scans), **keine davon seit 2026-10-01 angefasst** — die letzte Aktivität im Ordner liegt vor dem 01.10. Der Ordner ist also **nicht leer, aber ungesortiert** (Dateien liegen seit Wochen im Inbox statt in `Anlagen/`). Das ist ein handlungsrelevanter Punkt für die Steuererklärung Kanton Luzern (Frist Ende März 2027), kein reines Board-Thema: die OCR-Sortierung (Skill `ocr-and-documents`) steht seit Wochen aus.

#### 5. Live-Metriken (Board-unabhängig)
- `state.db`: **153,1 MB** (160.571.392 B) — +3,4 MB gegenüber 157,2 MB im Vorlauf, mtime 21:02 (aktiv, dieser Lauf). Wachstum ~+2 %/12 h → Verlangsamung ggü. den +56 %/6h-Episoden vom September. `sessions/`: 289 MB (1.849 JSON, unverändert), `profiles/`: 1,2 GB.
- Skills: **5.352** SKILL.md = 1.214 global + **3.910 in 34 Profilen** + 213 in `hermes-agent/`. Davon **1 Skill am heutigen Tag geändert**: `devops/kanban-board-audit` (2026-10-20). Profil-Skills: **keine Änderung seit 2026-07-28** → Drift ist eingefroren, nicht gewachsen.
- Disk: `/workspace` 250 GB, **211 GB belegt (85 %)**, 40 GB frei — **+4 GB seit dem 09:00-Lauf** (207→211 GB). Bei 85 % ist der Puffer dünner als der Hub-Stand vor 12 h suggerierte.
- `cron/executions.db`: 1.001 Executions heute (999 completed, 1 failed, 1 running) — **einzige fehlgeschlagene Execution: oauth-refresh 10:00**.

**Skills:** Bestehender Skill `google-oauth-workflow` aktualisiert — die Angabe „`scripts/oauth_refresh.py` (canonical)" war falsch und ist jetzt korrigiert (kanonisch: `cache/oauth_refresh_run.py`; `scripts/refresh_google_token.py` ist als **kaputt und nicht auszuführen** markiert; `expires_at`-Schema-Requirement ergänzt). Keine neuen Skills. `cron-reliability` deckt den Job-Fehlerstatus bereits ab, `kanban-board-audit` die DB-Platzhalter — beide brauchen kein Update, nur Verifikation.

**FALLBACK-EXTRACTED (source=git_fallback):** `jan-assistant` unverändert `80c4479` (dirty: `.openclaude/settings.local.json`); `kijan-steuern` unverändert `e0ea499` (clean, letzter Commit 2026-08-24 — Tax-Daten seit ~2 Monaten unbearbeitet); `f3k-design` ohne `.git` (kein Repo); KPT/Orchestrator nicht prüfbar (Fragment bzw. fehlend).

### Cross-Product Analysis (2026-10-21 03:35)

**Board-Rotation:** kpt, orchestrator (2 von N — bewusst gekürzt, Output-Budget)

#### 1. KORREKTUR zum Vorlauf: die 0-Byte-`kanban.db`-Platzhalter werden NICHT neu angelegt
Der Vorlauf (2026-10-20 21:00) folgerte aus den mtimes, „irgendein Prozess legt die Platzhalter regelmäßig neu an". Nach 6,5 h ist das **widerlegt**: `/workspace/.hermes/kanban/kanban.db` (0 B) steht weiterhin auf **mtime 2026-10-15 02:35**, `/workspace/kanban.db` (0 B) auf **2026-10-13 20:25** — beide **unverändert**. Die Platzhalter sind Altlasten aus einmaligen Init-Läufen, kein laufender Erzeuger. Die echte DB `/workspace/.hermes/kanban.db` (122 KB) hat ebenfalls **mtime 2026-09-21** → **alle 6 Tabellen 0 Zeilen, seit 30 Tagen null Schreibzugriffe**. Board-Layer ist faktisch tot; `hermes kanban list --json --archived` → `[]`, `hermes kanban diagnostics --json` → leer.

#### 2. NEU: die Hermes-CLI selbst ist degradiert — Paket-Install blockiert durch Ownership
Jeder `hermes`-Aufruf emittiert aktuell zwei Warnungen:
- `source-update completion failed: refusing to update /hermes-src: /hermes-src is owned by uid 1000, not the current uid 0` → der Container läuft als **root**, `/hermes-src` gehört **uid 1000** → der Self-Update-Pfad verweigert die Reparatur.
- `⚠ install out of sync (ffmpeg: not installed or outdated; ripgrep: not installed or outdated; venv: out of sync with uv.lock)` → **`ffmpeg` und `rg` fehlen in PATH, venv ≠ uv.lock**.
Das ist die wahrscheinlichste Wurzel der bereits bekannten **API-Drift** (`cannot import name 'ledger_transaction' from 'cron.executions'`) beim Job `email-calendar-sync`: Code und venv stammen auseinander. Gegenmassnahme wäre `hermes pm install`, braucht aber vorher die Ownership von `/hermes-src` (uid 1000 vs. root) — **Fix ausserhalb des Containers, daher hier nur als Befund**.

#### 3. NEU: Orchestrator ist nicht "weg", sondern **konfiguriert, aber nicht erreichbar**
`/workspace/.hermes/config.yaml.orchestrator` existiert und zeigt auf `provider: orchestrator`, `base_url: http://127.0.0.1:9100/v1`, `default: qwen36_35b`, Ollama-Backup `127.0.0.1:11434`. Ein Verbindungsversuch auf `:9100` → **kein Listener/Timeout (curl 000)**. Zusätzlich ist `docker` in diesem Container **nicht installiert** (`docker: command not found`) → Container-Start/Restart des Orchestrators ist von hier aus nicht möglich. Erkenntnis: „Orchestrator-Repo fehlt" war zu grob — es fehlt der *laufende Dienst*, die *Konfiguration* ist da. KPT-/Orchestrator-Board-Aussagen bleiben historisch.

#### 4. KORREKTUR zum Vorlauf: `steuern/inbox/` ist zu 91 % **Duplikat**, nicht „unsortiert"
`CH-Steuern 2025/inbox/` (56 Dateien, 11 MB) vs. `02_Rohdokumente_2025/` (51 Dateien, 9,6 MB): **51 Dateinamen sind identisch** — die Inbox enthält also fast durchgehend bereits einsortierte Belege (gleiche Namen, gleiche Herkunft). **Nur 5 Dateien sind wirklich neu/ungesortiert:**
- `AIA Reporting - Bescheinigung Kunde - Jan Kiefer - 2025-12-31.pdf`
- `Steuerverzeichnis vom 01.01.2025 bis 31.12.2025 - Jan Kiefer - 2025-12-31.pdf`
- `Vermoegensverzeichnis Raiffeisen Rio 649.065.931.8 per 3 - 6490659318 - 2025-12-31.pdf`
- `definitive Abrechnung 2025 - 4.5 Zimmer-Wohnung Hochparterre.pdf`
- `definitive Abrechnung 2025 - Einstellplatz Nr. 4.pdf`

Die Aussage „56 Belege warten auf OCR-Sortierung" war **übertrieben**: real offen sind 5 Dokumente (2 Mietabrechnungen Deutschland + Vermögensverzeichnis + AIA + Steuerverzeichnis) — Aufwand für die Steuererklärung 2025 damit deutlich kleiner als angenommen. `03_Neu_hochgeladene_Dokumente_Chat` (6 Dateien) ist ebenfalls bereits einsortiert.

#### 5. Live-Metriken (Board-unabhängig)
- `state.db`: **173,3 MB** (173.297.664 B) — **+12,7 MB in 6,5 h (~+8 %)** gegenüber 160,6 MB im Vorlauf. Die im Vorlauf notierte „Verlangsamung auf ~2 %/12 h" ist **widerlegt**: die Wachstumsrate ist wieder hoch. Treiber laut Tabellen-Count: `messages` **59.031** (FTS-Index parallel), `sessions` 1.109, `system_prompts` 162. `state-db-acceleration-response` ist damit wieder einschlägig.
- Skills: **5.337** SKILL.md = 1.214 global + **3.910 in 34 Profilen** + 213 in `hermes-agent/` — **−15 ggü. Vorlauf** (5.352), erstmals rückläufig; Profil-Skills weiterhin ohne Änderung seit 2026-07-28 (Drift eingefroren).
- Disk: `/workspace` 250 GB, **212 GB belegt (85 %)**, **39 GB frei** (−1 GB ggü. Vorlauf).
- Cron-Layer unverändert: 14 Jobs `scheduled`, **3 mit `last_status: error`** — `email-calendar-sync` (API-Drift, s. #2), `projekte-hub-ideas-sync` (HTTP 500 seit 2026-08-02, Nachfolger `…-gated` läuft sauber), `bounce-filter-monitor` (Provider-Ausfall, wöchentlich). **Keine neue Fehlerklasse** — der Layer ist stabil, nicht besser.

#### 6. NEU: beide Knowledge-Hub-Git-Remotes sind tot — kanonisches Repo ist `kijan007-agent/kijan-hermes-shared`
Die in den lokalen Clones konfigurierten Remotes existieren **nicht mehr**:
- `/workspace/.hermes/workflows` → `https://github.com/kijan007/kijan-hermes-shared-workflows.git` → **404 Repository not found**
- `/workspace/.hermes/skills` → `https://github.com/kijan007/kijan-hermes-shared-skills.git` → **404 Repository not found**

Der Token in `/workspace/.git-credentials` (User `kijan007`, 44 Repos sichtbar) hat Zugriff auf **44 Repos**; ein Tree-Scan über alle findet `KNOWLEDGE-HUB.md` **nirgends** remote — das einzige kanonische Shared-Repo ist **`kijan007-agent/kijan-hermes-shared`** (Branches `main`/`dev`, 799 Pfade, `devops/holistic-dev-workflow/references/knowledge-hub-*.md` vorhanden). Dort liegt die Hub-Datei künftig unter **`devops/holistic-dev-workflow/KNOWLEDGE-HUB.md`**, der Skill unter **`devops/knowledge-hub-maintenance/SKILL.md`** (im Shared-Repo bisher **nicht** vorhanden → neu angelegt). Auch `gh` ist in diesem Container **nicht installiert** (`/usr/bin/gh: not found`), der Credential-Helper `gh auth git-credential` läuft ins Leere → **Push via `git push` unmöglich**.

**Workaround (verifiziert):** Lieferung über die GitHub-Contents-API (Token aus `.git-credentials`, `PUT /repos/{repo}/contents/{path}` mit `sha` des bestehenden Blobs) — Commits `5c681e9a` (KNOWLEDGE-HUB.md) und `0f779fdd` (knowledge-hub-maintenance/SKILL.md) auf `main`, Byte-Hashes anschließend gegen `raw.githubusercontent.com` verifiziert (MATCH). Der lokale Clone `/workspace/.hermes/workflows` bleibt **2 Commits vor origin** (Push blockiert) — die Inhalte sind identisch, nur die Ablage ist neu.

**Konsequenz für die Kette:** Der `knowledge-hub-maintenance`-Skill ist im Shared-Repo **neu**, die `knowledge-hub-*-references` liegen unter `devops/holistic-dev-workflow/references/` — die Skill-Verzeichnisstruktur der lokalen Clones (`/workspace/.hermes/skills` mit 1.214 Skills) entspricht **nicht** der Shared-Repo-Struktur (799 Pfade). Vor künftigen Hub-Commits muss das Ziel-Repo und der Zielpfad geprüft werden, nicht blind `git push` aus dem lokalen Clone.

**Neue Erkenntnisse:** (a) Platzhalter-These des Vorlaufs widerlegt (Altlasten, kein Erzeuger); (b) **`hermes`-CLI degradiert: `/hermes-src`-Ownership uid 1000 vs. root blockiert Self-Update, `ffmpeg`/`rg` fehlen, venv ≠ uv.lock** — erklärt die API-Drift; (c) Orchestrator-*Dienst* läuft nicht (`:9100` tot, kein `docker` im Container), Config ist aber vorhanden; (d) steuern-inbox real nur 5 offene Belege, 51/56 sind Duplikate bereits einsortierter Belege; (e) `state.db` +8 %/6,5 h — Beschleunigung zurück; (f) **beide Hub-Git-Remotes sind 404** — kanonisches Repo ist `kijan007-agent/kijan-hermes-shared`, Lieferung via Contents-API statt `git push`.

**Skills:** Bestehender Skill `devops/knowledge-hub-maintenance` aktualisiert (im Shared-Repo unter `devops/knowledge-hub-maintenance/SKILL.md` neu angelegt) — die Vorgabe „CRITICAL: Use `execute_code` for ALL checks" ist im **Cron-Kontext falsch** (`execute_code` ist ohne User-Freigabe blockiert). Neu dokumentiert: Cron-taugliche Prüfpfade (`terminal` + `python3`-Heredoc), die Tirith-Blocker (Plain-HTTP-URL, Inline-Interpreter mit Socket, verschachtelte Shell-Loops, `hermes update` als Danger-Pattern), der Duplikat-Check für `inbox/` (Datei-Namen-Intersection statt Dateizahl) und die Priorisierung von Paket-Install + `/hermes-src`-Ownership vor jedem API-Drift-Fix. Keine neuen Skills.

**FALLBACK-EXTRACTED (source=git_fallback):** `jan-assistant` unverändert `80c4479` (dirty: `.openclaude/`), `kijan-steuern` unverändert `e0ea499` (clean, letzter Commit 2026-08-24 — Tax-Daten seit ~2 Monaten unbearbeitet); KPT-2 weiterhin Fragment (2 Dateien, kein `.git`); Orchestrator-Repo weiterhin nicht vorhanden, nur Config + nicht laufender Dienst.
