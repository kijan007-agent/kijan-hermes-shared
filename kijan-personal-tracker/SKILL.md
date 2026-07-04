---
name: kijan-personal-tracker
description: Kijan Personal Tracker (KPT) full-stack reference — backend, Connect IQ, symptoms app, admin, docs, and website tech stack.
---

# Kijan Personal Tracker (KPT) Tech Stack

## Triggers
- Any task involving `kpt-backend`, `kpt-app-ciq`, `kpt-symptoms-app`, `kpt-datafield-ciq`, `kpt-admin`, `kpt-doc`, `kpt-website`
- User mentions energy pacing, spoon tracking, Garmin sync, activity tracking, health metrics
- Repo paths: `/workspace/Github/KijanPersonalTracker*`, `/workspace/Github/kijan-*`
- **⚠️ 2026-06-07 WIPE**: Both `KijanPersonalTracker-feature` and `KijanPersonalTracker-hermes` repos were COMPLETELY WIPEED (zero commits, zero remotes). See `references/repo-wipe-event-20260607.md` in cron-reliability skill. Only `kpt-doc/_specs/` and `kpt-doc/_mockups/` disk files survive.
- **⚠️ 2026-06-07 WIPE EXTENDED**: `/workspace/Github/KijanPersonalTracker-feature/` and `/workspace/Github/KijanPersonalTracker-hermes/` are ALSO empty (zero commits, zero remotes). Effective surviving code locations: (1) `/tmp/kpt-extract/source/` — extracted .mc files from prior extraction (2) `/workspace/Github/KijanPersonalTracker-prod-hotfix/` — unverified legacy copy. NEVER assume `/data/Github/` or `/workspace/Github/KijanPersonalTracker-*` have working trees.
- **⚠️ 2026-06-08 CRON PATH PITFALL**: Cron jobs frequently reference dead `/data/Github/` paths (e.g., `/data/Github/KijanPersonalTracker-feature/kpt-app-ciq/source/`). These paths DO NOT EXIST. Always verify path validity first with `git -C <path> rev-parse HEAD` — outputs "HEAD" = empty repo, skip immediately. Cron jobs should use `/workspace/Github/KijanPersonalTracker-prod-hotfix/` or `/tmp/kpt-extract/source/` as fallbacks. See `references/cron-path-mismatch-pattern.md`.
- **⚠️ 2026-06-08 WIPE FINAL STATE**: ALL KijanPersonalTracker repos (`KijanPersonalTracker-feature`, `KijanPersonalTracker-hermes`, `kpt-backend` submodule) = ZERO commits, ZERO remotes. COMPLETE DATA LOSS. Only surviving artifacts: `kpt-doc/_specs/`, `kpt-doc/_mockups/` (untracked), `/tmp/kpt-extract/source/` (read-only .mc snapshot). Any TASKS.md is pre-wipe planning intent only. NEVER assume any KijanPersonalTracker path has content.
- **⚠️ 2026-06-08 SUBMODULE-HEAD-DIVERGENCE**: The kpt-app-ciq submodule's working tree HEAD (174996a) is the feature branch merge commit, but individual .mc files may be STUB versions (e.g., EnergyScreen = 122 lines, not 493). TASKS.md in kpt-doc claims features as "COMPLETED" but the actual code on disk may be pre-chart stubs. Always verify file line counts against TASKS.md claims — TASKS.md was written BEFORE the chart implementation was finalized. Check `wc -l` on every claimed file.
- **⚠️ 2026-06-08 WORKLOG PATH PITFALL**: Worklogs directory `kpt-doc/_worklogs/` may not exist on disk. When it doesn't, report "no worklogs maintained" rather than failing. See updated Cron/Session Status Audit Procedure step 6.

## Project Structure

> **⚠️ 2026-06-07 WIPE**: All repos are empty shells. Only `kpt-doc/_specs/` and `kpt-doc/_mockups/` survive on disk. No `.mc` files, no backend code, no migrations exist anywhere. Recovery requires user-provided backup or reconstruction from specs.

```
/workspace/Github/KijanPersonalTracker-prod-hotfix/   ← ONLY remaining with working tree (verify)
kpt-doc/                                              ← Only surviving directory: specs + mockups (untracked)
```

## Backend (kpt-backend)
- **Stack:** FastAPI 0.115, SQLAlchemy 2.0 async, asyncpg 0.30, PostgreSQL (4 instances: admin/activity/projects/health)
- **Migrations:** Alembic (4 separate alembic_* directories)
- **Key models:** Device, UserDefinition, DailyCheckin, Activity, Project, HealthMetric
- **Routers:** auth (auth_enhanced.py), activities, personal, projects, reports, pdf, metrics, jobs
- **Services:** PacingEngine, ActivityRankingEngine
- **Jobs:** Weekly ranking (ranking_worker.py, ranking_queue.py)
- **Deploy:** Docker (3 Dockerfiles), Railway, ghcr.io/kijan007/kijan-backend
- **Auth:** JWT (PyJWT), HTTPBasic, LemonSqueezy subscription integration
- **PDF:** WeasyPrint + Jinja2 templates (pdf_custom.html, pdf_project.html)

## Connect IQ App (kpt-app-ciq)
- **Language:** Monkey C
- **Source:** 171 `.mc` files in `source/` (current on origin/feature)
- **Architecture:** FSM-based state machine → `ActivityFsm.mc`, `StateStore.mc`
- **Sync:** `SyncNetworkManager.mc`, `BackendCommManager.mc`, `Sync/EventRouter.mc`, `Sync/JsonSerializer.mc`, `Sync/QueueManager.mc`
- **Build:** `build.sh PRIMARY_DEVICE=epix2pro51mm`, supports --dev/--staging/--prod
- **Submodule (2026-05-13):** kpt-app-ciq in hermes workspace has FULL working tree with origin remote (https://github.com/kijan007/kpt-app-ciq.git). origin/feature HEAD = 0727f60 with 171 MC files.
- **Key patterns:** AppTimer, BackgroundService, ScreenManager, NavigationController
- **Support files:** FSM_DIAGRAM.txt, FSM_README.md, FSM_TRANSITIONS_COMPLETE.md, HEARTBEAT_IMPLEMENTATION.md, BUGFIX_FIREISIGNAL_VALIDATION.md

## Datafield (kpt-datafield-ciq)
- 5 MC files: DataFieldSync, GarminActivitySync, KijanPersonalDatafieldApp/View, Version
- Multi-product manifest (Epix2, Fenix 5/6/7 series)

## Symptoms App (kpt-symptoms-app)
- React iOS/Android app — currently uninitialized submodule (only README.md)
- Needs `git submodule update` from parent or manual clone

## Admin Portal (kpt-admin)
- FastAPI app for device/plan/voucher management
- Separate PostgreSQL instance (kijan_admin)
- 17 files: main.py, index.html, devices.html, plans.html, vouchers.html

## Documentation (kpt-doc)
- 441 files: 149 memory files in MEMORY/, 31 task files in _tasks/
- TASKS.md (active tasks), _done/ (completed), _tasks_waiting_list_no_execute/
- Release procedures, automated testing, user-facing docs, whitepaper

## VM Deploy Pitfalls (2026-05-14)
- **SSH long-lived process blocking**: `terminal()` blocks ANY command that looks like a server/watch process — including `python3 -m uvicorn`, `uvicorn`, even `pip install` on slow connections. Workaround: use `background=true` for process tracking, but for starting servers, user must run commands manually.
- **Python heredocs via SSH break**: `python3 << 'EOF'` multiline strings hang or get mangled through SSH. Use `-c` for short scripts only. For complex remote Python, write a script file locally → scp → execute.
- **CR/LF mangles sed variables**: On files with CRLF line endings (Connect IQ source), `sed` through SSH strips `$1`, quotes, and special chars. Use raw byte operations (`python3` with `'rb'`/`'wb'`) for safe manipulation.
- **Submodule divergence**: `git submodule update` resets submodules to the commit recorded in the parent repo HEAD. To use a different branch (e.g., latest `dev`), manually `cd kpt-backend && git checkout dev && git pull` AFTER `git submodule update`.
- **pip PEP 668 on Ubuntu 24.04**: `pip install` fails with `externally-managed-environment`. Use `--break-system-packages` flag.
- **No sudo password via SSH**: Use `echo 'password' | sudo -S` for non-interactive sudo. After first success, sudo cache may work without password.
- **Connect IQ env pattern**: Each environment needs: (1) `Env{name}.mc` with `(:name)` annotation, (2) `monkey-{name}.jungle` with `base.excludeAnnotations = prod;dev;staging` (excluding all OTHER envs), (3) build wrapper script calling `./build.sh --{name}`.
- `kpt-app-ciq` submodule is a **bare repo** (only .git, no working tree) — code lives in prod-hotfix copy
- Submodules often need `git submodule init && git submodule update` from parent
- **No `git` binary** available in terminal — use host git for repo operations
- kpt-symptoms-app has no git working tree (empty submodule clone)
- PROD-HOTFIX branch: `origin/prod-hotfix-bat` (working), feature branch: `origin/feature`
- **New workspace**: `/workspace/Github/KijanPersonalTracker-hermes/` is the current working copy.
  This workspace has working (non-ghost) submodules — different from the original `/workspace/Github/KijanPersonalTracker/` setup.
  In this workspace, submodules may have full working trees and packed-refs with feature branch data.
- **PATH PITFALL**: Feature branch repo at `/data/Github/KijanPersonalTracker-feature/` is EMPTY — zero commits, zero files, no remote (confirmed 2026-05-17). NEVER use `/data/Github/` for KijanPersonalTracker source. The correct workspace is `/workspace/Github/KijanPersonalTracker-hermes/`.
- **MERGE-TAG ORPHAN PATTERN**: Feature work committed to `5826510` (EnergyScreen chart 493 lines, DeltaInputScreen 417 lines, ScreenFlowController fixes) lives ONLY under `merge-feature-to-hermes_20260518_*` tag chain (17 tags). NOT on any tracked branch. Working tree has older stubs. Verify file existence via `git branch -a --contains <sha>` + `git ls-tree <branch>:<path>`. See `references/merge-tag-orphan-chain.md`.
- **SUBMODULE BRANCH DIVERGENCE (2026-05-14)**: The kpt-backend submodule on `origin/feature` points to commit 3bf07dd (prod-hotfix merge base) which is STALE. The actual dev branch (abdd433) has 37+ commits ahead with new features, bug fixes, and DAL changes (e.g., ActivityMetricDAL removal). When deploying backend, ALWAYS `git fetch + git checkout dev + git pull` in the kpt-backend submodule BEFORE running migrations or starting the server. The main repo's submodule pointer on feature branch may lag behind the actual development.
- **DISABLED/REMOVED IMPLEMENTATION CHECK**: Look for `// DISABLED: ... broken implementations removed` comments in `ScreenFlowController.mc` (lines 428-430, 545-553). If found, the feature was intentionally removed. Cross-reference with `COMPLETE_SUMMARY.md` which may still claim "COMPLETED" for removed features. When reporting status, explicitly note "REMOVED — DISABLED in source at ScreenFlowController.mc:lines" for such tasks.
- **DOC/DISK DISCREPANCY PATTERN (2026-05-12)**: TASKS.md claims 38 ScreenFlowConfig transition rules, but grep found 0 matches. TASKS.md claims TASK-100/101 COMPLETED but ScreenFlowController.mc exists only in prod-hotfix (not in feature branch submodule). Always verify TASKS.md claims against actual disk state before reporting. See `references/doc-disk-discrepancy.md` and `references/cron-status-audit-2026-05-13.md` for the latest audit protocol.
- **TASKS.md TRUST BIAS**: TASKS.md marks EnergyScreen and DeltaInputScreen as COMPLETED but EnergyScreen = 123-line stub (not chart), DeltaInputScreen = deleted in c965f54. TASK-103 through TASK-109 in TASKS.md = documentation claims with ZERO code changes. TASK-105 through TASK-109 are documented-only artifacts (files 800-2500 bytes, zero git diffs in kpt-app-ciq). TASK-105/106/107/108/109 have zero corresponding commits. Always verify COMPLETED claims against `git diff HEAD~N..HEAD --name-only` in kpt-app-ciq — never trust TASKS.md for code existence.
- **KANBAN-BEFORE-EXECUTE PATTERN (2026-05-12)**: User explicitly requested Kanban-board workflow (BOARD → Tasks → Branches → Reports). Always create `TASKS-CI-KANBAN.md` before starting multi-task work. Each task gets its own branch in `feature`. After test, merge into `feature` (NOT dev/prod). Send Telegram report per task. See `references/kanban-board-pattern.md`.
- **MULTI-PERSPECTIVE EXECUTION PATTERN (2026-05-12)**: Every task MUST be executed through these specialist lenses: Patient, Arzt, UI/UX Designer, Data-Spezialist (medizinische Daten), Data Engineer, Systemarchitekt, Softwareentwickler, Produktmanager, Projektmanager, Stakeholder. Not optional — apply to every task. See `references/multi-perspective-checklist.md`.
- **NAVIGATION-KONSISTENZ PATTERN (2026-05-12)**: App-Navigation und Dashboard-Navigation müssen konsistent sein. Prüfe immer: gleiche Menü-Pfade, gleiche Terminologie, gleiche Hierarchie-Tiefe. Dashboard-Spoon-Werte müssen als Pacing-Values im Dashboard dargestellt werden.
- **LOCAL TEST ENV PATTERN (2026-05-12)**: Local test env = `docker-compose.dev.yml` + `.env` in `kpt-backend/`. DB: postgres:15-alpine, container=kijan-db-dev, user=kijan_user, pass=kijan_password, name=kijan_tracker. Prod dump: `scripts/dump_prod.sh` (on origin/feature). Load dev: `scripts/load_dev.sh`. Dumps dir: `dumps/`. ⚠️ **No docker/pg_dump on this machine** — must be run locally by user. Save env config to `.hermes-test-env.json` for future sessions. See `references/local-test-env-setup.md`.
- **BACKEND-AUDIT-PATTERN (2026-05-12)**: Critical backend patterns: (1) All `session.commit()` must be wrapped in `_safe_commit(session)` with rollback on error — never assume commit won't fail. (2) `SECRET_KEY`/`REGISTRATION_KEY` must have startup validation via `validate_config()`. (3) Onboarding ephemeral keys must validate hash format (reject empty/invalid). (4) `execute_with_retry` must include exponential backoff + `session.rollback()` before each retry. (5) Database URLs must be validated against default passwords and localhost in prod. (6) SlowAPI fallback must log ERROR not WARNING. See `references/backend-audit-checklist.md` and `scripts/backend-audit.sh`.
- **CONNECT-IQ-CRLF-FIX (2026-05-12)**: When Connect IQ files have CRLF issues (>100 files), use binary-mode replacement: `content.replace(b'\\r\\n', b'\\n')` in Python — NOT sed (fails on binary content). Also set `git config core.autocrlf input && core.eol lf && core.safecrlf false` before checkout. See `references/cifix-mass-fix.md`.

## Cron/Session Status Audit Procedure
When asked for status on KijanPersonalTracker tasks during cron or standalone sessions:
1. **Locate project**: Use `execute_code` workspace scan for KijanPersonalTracker dirs. Check in order: (a) `/workspace/Github/KijanPersonalTracker-prod-hotfix/`, (b) `/tmp/kpt-extract/source/` (extracted .mc files), (c) `/workspace/Github/KijanPersonalTracker-hermes/`. **ALWAYS verify path validity first**: `git -C <path> rev-parse HEAD` — outputs just "HEAD" = empty repo, skip immediately. NEVER use `/data/Github/KijanPersonalTracker-feature/` or `/data/Github/KijanPersonalTracker-hermes/` — confirmed empty (zero commits, zero files, unreachable remote). Cron jobs commonly reference dead `/data/Github/` paths.
2. **WIPE CHECK**: If ALL checked paths are empty (zero commits, zero remotes), surviving code is ONLY in `/tmp/kpt-extract/source/` (prior extraction) — report this as a blocker. `/workspace/Github/KijanPersonalTracker-*` paths are also wiped as of 2026-06-07.
3. **DEV BRANCH DIVERGENCE CHECK**: Before trusting TASKS.md, run `git -C kpt-app-ciq log --oneline HEAD --format="%h %ci" | head -1` and compare to TASKS.md "Updated:" date. If delta > 5 days → TASKS.md is unreliable (see `references/dev-branch-vs-task-tracker-divergence.md`). Count source commits since last TASKS.md update: `git -C kpt-app-ciq log --oneline <task-update-date>..HEAD -- source/`. If >10 commits → verify each task claim individually.
4. **MULTI-LEVEL DIVERGENCE CHECK (2026-06-01)**: Trace each file through ALL layers: working tree → feature branch → origin/hermes. A file can be "behind" at any layer. Use `git diff feature -- source/<file>`, `git diff origin/hermes -- source/<file>`, and `git diff HEAD -- source/<file>` to identify which layer each file is stale at. Never assume a single-layer check is sufficient. See `references/multi-level-branch-divergence.md`.
5. **Read TASKS.md**: This is the **single authoritative source** for task status — never rely on source file existence
   to determine completion; docs are updated before code commits in the TASKS-driven workflow
   ⚠️ **Trust threshold**: TASKS.md status is unreliable when dev branch diverges >10 commits or >5 days from TASKS.md update date. Always verify COMPLETED claims against actual code.
6. **Read worklogs**: Check `kpt-doc/_worklogs/` (WORKLOG.md + daily dated .md files) for latest session activity. If directory doesn't exist (confirmed 2026-06-08), report "no worklogs maintained" — do NOT fail.
7. **SUBMODULE DIVERGENCE CHECK (2026-05-13)**: For `kpt-app-ciq`, the local submodule working tree HEAD may show DIFFERENT file content than `origin/feature` commits. Always check BOTH:
   a. Working tree: `wc -l kpt-app-ciq/source/EnergyScreen.mc` (what you see)
   b. Remote branch: `git -C kpt-app-ciq show origin/feature:source/EnergyScreen.mc | wc -l` (what history says)
   c. Merge-base: `git -C kpt-app-ciq merge-base --is-ancestor <chart-commit> <submodule-HEAD>` to verify ancestry
   If these diverge, report both — remote branch may have features the working tree lost via intermediate replacement commits.
8. **DELIVER FORMAT**: Status per task as bullet list (status icon, one-line summary, file ref), followed by remaining items table and branch divergence table
9. **STATUS DISCREPANCY FLAG**: If TASKS.md says COMPLETED but source files are not accessible (bare submodule), note the caveat explicitly — "COMPLETED in TASKS.md but not verifiable on disk"
10. **GHOST SUBMODULE CHECK**: If submodule's remote branch has no refs/heads (empty packed-refs), the submodule is a ghost — use prod-hotfix working copy as source of truth
11. **DISABLED/REMOVED IMPLEMENTATION CHECK**: Look for `// DISABLED: ... broken implementations removed` comments in `ScreenFlowController.mc` and `UIViewFactory.mc`. If found, the feature was planned but never merged. Cross-reference with `COMPLETE_SUMMARY.md` which may claim "COMPLETED" for features that were removed. When reporting status, explicitly note "IMPLEMENTATION REMOVED — DISABLED in source" for such tasks.

## Cron Jobs
- Morning report job at 8 AM → Telegram summary
- Cron config: `~/.hermes/cron/`

## Task Management
- `_tasks/INDEX.md` — Active task index (regenerate after pruning with `references/task-audit-and-prune.md`)
- `_tasks/_done/` — Completed/obsolete tasks moved here during cleanup

**⚠️ Multi-level divergence for task claims (2026-06-01):** When auditing task status, trace each file through: (1) working tree HEAD, (2) feature branch, (3) origin/hermes, (4) TASKS.md claims. A task can be "in progress" at one layer and "missing" at another. Always report which layer each item's state is on. See `references/multi-level-branch-divergence.md`.

## Support Files
- `references/backend-audit-checklist.md` — Backend security, data integrity, and error handling audit checklist
- `references/cron-morning-report.md` — Morning report cron config
- `references/cron-status-audit.md` — Step-by-step audit procedure
- `references/cron-status-audit-2026-05-14.md` — Cron status audit with TASKS.md trust bias findings
- `references/task-audit-and-prune.md` — Procedure for auditing and pruning task files
- `references/task-completion-verification.md` — File existence status table, git verification patterns
- **`references/kijan-frontend-specs.md`** — Kijan Frontend Spezifikationen: Flutter, React/Next.js Dashboard, DESIGN.md, Pain Scale, 6 ADRs, 6 Phasen, Test-Konzept, i18n
- **`references/health-aggregation-layer-v2.md`** — HAL v2.0: 32 Tasks, 7 Phasen, 30 Tage, UUIDv7, Bearable-Import, mobile cache
- `references/cron-status-audit-2026-05-20.md` — HAL v2.0 Backend status (~85% implementiert)
- **`references/alembic-multi-stack-pattern.md`** — 4-stack Alembic pattern: idempotent migrations, partition reordering, rename table pitfalls
- **`references/task-history-verification.md`** — Known TASKS.md → reality gaps, verification protocol
- `references/task-status-audit-pattern.md` — Procedure for auditing task completion via files
- `references/workspace-analysis.md` — Workspace scan results
- `references/doc-disk-discrepancy.md` — Known TASKS.md vs actual disk discrepancies
- `references/feature-branch-submodule-status.md` — Bare submodule status and feature branch audit
- `references/energy-screen-removed.md` — EnergyScreen/DeltaInputScreen removed implementation audit
- `references/post-wipe-extraction-location.md` — `/tmp/kpt-extract/source/` as post-wipe code fallback location
- `references/local-test-env-setup.md` — Local test environment configuration
- `references/kanban-board-pattern.md` — Kanban-Board-Erzeugung und Task-Workflow
- `references/multi-perspective-checklist.md` — 10-Spezialist-Perspektiven für jede Task
- `references/cron-status-audit-2026-05-19.md` — See kijan-personal-tracker-debug skill `references/2026-05-19-status-audit.md`
- **`references/dev-branch-vs-task-tracker-divergence.md`** — Protocol for detecting stale TASKS.md (delta >10 commits)
- **`references/multi-level-branch-divergence.md`** — Three-layer divergence audit: working tree → feature → origin/hermes → TASKS.md
- `references/cron-path-mismatch-pattern.md` — Cron jobs reference dead `/data/Github/` paths; detection and fallback protocol
- `references/tag-chain-branch-divergence.md` — Feature work on merge tags but not tracked branches. Detection protocol and classification matrix.
- **`references/task-claim-code-verification.md`** — Protocol for verifying TASKS.md "COMPLETED" claims by reading actual code (not just file existence). See also `task-claim-verification` skill's `references/claimed-vs-verified-audit-protocol.md` (2026-06-08) for the full classification decision tree.
- **⚠️ See `cron-reliability` skill: `references/repo-wipe-event-20260607.md`** — Complete wipe of both KijanPersonalTracker repos (2026-06-07). Recovery options and detection patterns.

## Related Skill: kijan-holistic-tracking
For holistic tracking architecture (3-platform strategy, energy/symptom/med integration, Burndown-Chart design, cold-start spoon strategy), load `kijan-holistic-tracking` skill. Contains: full 3-platform concept, unified dashboard layout, backend health schema, phased implementation plan.

## Related Skill: kijan-personal-tracker (kijanpersonal-tracker)
For project operations (TASKS.md patterns, branch management, status audits). **NOTE**: The skill under `kijanpersonal-tracker/` directory is NOT installed — only `kijan-personal-tracker` is available. Use `kijan-personal-tracker` for both ops and stack. **Overlap note (2026-06-01)**: Both skills document `/data/Github/` dead repo pattern and `/workspace/Github/KijanPersonalTracker-hermes/` as active workspace. When in doubt about path validity, `kijan-personal-tracker` has the more comprehensive zero-commit detection protocol. **Overlap note (2026-06-03)**: Both skills now contain `references/task-claim-code-verification.md` with the same content — this is intentional redundancy for cross-referencing. No consolidation needed as each skill's audience differs (ops vs stack). **Note (2026-06-08)**: For TASKS.md claim verification, use `task-claim-verification` skill's `references/claimed-vs-verified-audit-protocol.md` instead — it has the full classification decision tree and is more actionable.

## Related: kijan-health-module Skill
For health module tasks (symptom tracking, medication, disease catalog, ICD-10-GAM, correlation engine), load `kijan-health-module` skill. It contains:
- Full health DB schema (11 tables, partitioning strategy)
- SQLAlchemy models reference (models_health.py)
- API router patterns (symptom_tracking.py)
- ICD-10-GAM source, pain assessment tools (NRS/BPI/McGill/PainDETECT)
- PROMIS measures, Bearable CSV import spec, disease catalog seed data
- Plan enforcement pattern (BUG-015 fix)
