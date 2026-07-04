# Knowledge Hub Update Workflow

> Repeatable pattern for Knowledge Hub cron updates. Discovered/validated 2026-05-21. Updated 2026-05-23 (dual-offset), 2026-05-25 (pipe-inconsistency), 2026-05-27 (duplicate-section detection), 2026-05-28 (Alembic count correction, kpt-doc file count, stale data cleanup), 2026-05-29 (HAL test infrastructure, test explosion, Energy Chart STABIL), 2026-06-03 (file count staleness protocol, new model patterns), 2026-06-08 (status-line fragility, replace_all multi-section danger, header/footer timestamp convention).

## Purpose
Systematically aggregate cross-product knowledge from cron outputs, status reports, sessions, and git state into KNOWLEDGE-HUB.md.

## Steps

### Phase 1: Gather Inputs
1. **Repo Path Discovery (CRITICAL):** Verify paths — dead: `/data/Github/`, `/workspace/Github/kijan-personal-tracker/`, `/workspace/Github/KijanPersonalTracker/`. Authoritative: `/workspace/Github/KijanPersonalTracker-hermes/` AND `/data/Github/KijanPersonalTracker-hermes/`.
2. **Branch Offset Measurement:** BOTH `git log --oneline origin/dev..HEAD | wc -l` AND `git log --oneline origin/hermes..HEAD | wc -l`. ALL products synced to hermes = unmerged=0 baseline. Only origin/dev divergence matters.
3. **Status Reports:** `ls /workspace/.hermes/workflows/holistic-dev-workflow/reports/`
4. **Cron Outputs:** Check `/workspace/.hermes/cron/` for new outputs
5. **Session Files:** `find /workspace/.hermes/ -name 'session_*' -newer <last-update>`
6. **TASKS.md:** `find /workspace/Github -name "TASKS.md" -newer KNOWLEDGE-HUB.md`
7. **Skills:** `find ~/.hermes/skills -newer KNOWLEDGE-HUB.md -name "SKILL.md"`
8. **Alembic Stack Count:** `find <repo>/ -type d -name 'alembic_*' | wc -l`
9. **File Count Verification:** `find <repo>/ -type f | wc -l` per product — never trust previous Knowledge Hub file counts.

### Phase 2: Analyze & Synthesize
1. **Process Insights:** Workflow improvements, lessons learned
2. **Domain Knowledge:** New patterns, spec completions, architecture decisions
3. **Technical Patterns:** New implementations, fixes, architectural discoveries
4. **Risk Patterns:** New bugs, TASKS.md discrepancies, branch divergence issues
5. **Cross-Product Pattern Detection:** Same pattern in ≥2 products → consolidate

### Phase 3: Cross-Product Analysis
1. **Duplicates:** Same pattern in multiple products → consolidate
2. **New Patterns:** Cross-product patterns that didn't exist before
3. **Skills to Create:** Patterns worth codifying → create SKILL.md (only if not in existing skills)
4. **Skills to Update:** Patterns that evolved → patch existing skills

### Phase 4: Update Knowledge Hub
1. Update header timestamp
2. Add new entries to appropriate sections
3. Update Cross-Product Analysis section
4. Update Skill Registry
5. Update footer with next update time

### Phase 5: Create Skills (if applicable)
For patterns worth codifying:
1. Create SKILL.md with trigger, steps, pitfalls, cross-product relevance
2. Add reference files if needed
3. Update Knowledge Hub skill registry

## Pitfalls

### Status-Line Fragility (2026-06-08)
After patching one status line in a section, the file content shifts — `old_string` for the NEXT patch no longer matches.
**Workaround:** Re-read the file between patches in the same section. Use `search_files` to find exact current content before each patch. Never batch multiple patches on status lines.

### Replace_all Danger on Multi-Section Entries (2026-06-08)
Entries like `kpt-doc SYNCED` or `kpt-backend WARNING` appear in BOTH the risk_patterns table AND the submodule status summary. `replace_all=True` removes from unintended sections.
**Workaround:** Never use `replace_all` on entries that appear in multiple sections. After any replace, verify ALL occurrences were intended. Use unique single-line patterns with enough context to be unambiguous.

### Pipe-Inconsistency (2026-05-25)
KNOWLEDGE-HUB.md uses 3 different pipe counts (`|`, `|||`, `|||||`, `||||||`) for table rows — string-replace on full blocks FAILS.
**Workaround:** Read as lines, find by keyword match, replace per-line. Never search multi-line blocks.

### Duplicate-Section Pattern (2026-05-27)
The file has multiple "Workflow-Verbesserungen" sections that get duplicated by naive updates.
**Fix:** After any update, scan for duplicate section headers and remove older duplicates. Also scan for remaining old timestamps.

### Alembic Directory Migration (2026-05-27)
alembic/ and i18n/ directories moved off-disk to alembic_activity/ and translations/. Always check actual directory structure.

### Submodule Unmerged Count Staleness (2026-06-01)
**PITFALL:** Unmerged counts in KNOWLEDGE-HUB.md can be severely stale. kpt-admin (20→1), kpt-common-barrels-ciq (14→1), kpt-datafield-ciq (11→1) — all 3 were CRITICAL/WARNING but actually SYNCED vs origin/hermes. **Always verify with fresh `git rev-list --count origin/hermes..HEAD` before trusting previous Knowledge Hub state.** Stale counts trigger false CRITICAL alerts.

### Alembic Idempotent Pattern (2026-05-27)
Check column existence before ALTER TABLE. PITFALL: running migrations twice on different env fails without existence checks.

### Alembic Partition Reordering (2026-05-27)
When reordering partitions: drop → recreate → validate. PITFALL: FK constraints must be temporarily disabled.

### Alembic Rename Table (2026-05-27)
Safe table rename with cascade handling. PITFALL: `op.rename_table()` does NOT auto-update FK constraints.

### Branch Offset Measurement
Must always measure against BOTH origin/dev AND origin/hermes.

### TASKS.md Trust Bias
Never trust TASKS.md blindly — always verify with `git diff HEAD~N..HEAD --name-only`.

### Kanban.db Empty
Board data missing, kanban-cli non-functional.

### Cron Paths
Hardcoded to `/workspace/Github/` not `/data/Github/`.

### File Count Staleness (2026-06-03)
Counts in KNOWLEDGE-HUB.md go stale because: (1) counting methodology changes (alembic env.py excluded from py count: 109→102), (2) file categorization corrections (.mc/.xml reclassified: 169→241), (3) recursive find vs manual count discrepancies (kpt-doc 504→480, MEMORY 188→187). **Always verify with fresh `find` or `tree` counts before updating Knowledge Hub — never trust previous Knowledge Hub file counts.** Mark corrections explicitly as `**CHANGED** (old→new — reason)`.

### Header/Footer Timestamp Convention (2026-06-08)
Header "Stand" and footer "Letzte Änderung" MUST match. "Nächste Aktualisierung" intentionally differs (+6h). Verify: `header_ts == footer_ts` before committing.

## Key Discoveries Log

### 2026-06-09
- **Drift Direction Reversal:** kpt-backend 13 AHEAD→13 BEHIND vs origin/dev (origin/dev gained commits). kpt-app-ciq 0→120 AHEAD vs hermes (CRITICAL DRIFT). kpt-doc 71→154 AHEAD vs origin/dev. **NEVER report just the count — always include direction + reference branch.**
- **kpt-backend SYNCED vs hermes:** 0 unmerged, health_aggregation.py committed — 115 py files (repo-wide, was 102), 185 total files, 39 migrations
- **kpt-app-ciq CRITICAL DRIFT:** 120 ahead vs origin/hermes — feature→dev merged but hermes NOT updated. Pattern: `feature → dev` merge diverges hermes
- **kpt-doc DIRTY:** untracked `_specs/kijan-frontend/` (web/001-web-dashboard-spec.md 13KB), 154 ahead vs origin/dev, 715 total files, 325 MEMORY docs
- **KNOWLEDGE-HUB Dual-Read Pattern:** When updating across multiple sections (status table → risk patterns → divergence analysis → TBD), re-read the full file between each section. Line numbers shift after every patch. Patching one section without re-reading breaks the next section's old_string.
- **File Count Corrections:** kpt-backend 102→115 py (find includes alembic env.py), kpt-doc 480→715 total (325 MEMORY + 3 SPEC + 26 _specs + 361 other)
- **No new skills needed** — all patterns already covered by existing skills

### 2026-06-03
- **File Count Staleness Pattern:** Counts in KNOWLEDGE-HUB.md go stale due to methodology drift: kpt-backend py 109→102 (alembic env.py excluded), kpt-doc total 504→480 (corrected recursive find), MEMORY 188→187. **Always verify with fresh `find` counts — never trust previous Knowledge Hub file counts.**
- **kpt-backend new models:** RankingTask/RankingResult (DB queue), DeviceSyncStats, DatafieldPairingCode, ActivityEnergyCost, HealthMetric (12,228L range-partitioned), FeedbackMetric triggers (after_activity/after_pause/after_session).
- **i18n Layer Pattern:** app/i18n.py + translations/ JSON auto-load — 9 languages.
- **kpt-app-ciq hermes branch RESOLVED:** 168→0 ahead — feature→dev merged, hermes updated.
- **kpt-doc corrected to 480 total files (187 MEMORY + 2 SPEC).**
- **No new skills needed** — all patterns documented as "evtl. später" in Knowledge Hub.
- **Knowledge Hub file count protocol created** as `references/knowledge-hub-file-counting.md`.

### 2026-05-29
- **HAL Test Infrastructure Pattern:** `conftest.py`(134L) + `conftest_health.py`(66L) — session-scoped fixtures, multi-database mock sessions. Already covered by `kijan-health-module` skill.
- **Test Explosion:** kpt-backend tests 1,353→3,205 lines (+137%). New files: test_api.py(446L), test_config_endpoint.py(176L), test_ranking_queue.py(473L), test_timestamp_migrations.py(207L).
- **Energy Progression Chart promoted to STABIL:** was ITERATIV, now stable — time-series scatter plot pattern confirmed.
- **Deprecated method() count increased:** 3→4 instances (added FeedbackDelegate to ScreenFlowController + TimeWindowMenuDelegate x3).
- **kpt-backend file count:** 56→75 app/ files (app/45, dal/6, jobs/4, routers/11, services/9).
- **kpt-app-ciq XML growth:** 20→24 .xml files (262→264 total).
- **kpt-doc file count:** 504→503 total files.
- **No new files** detected across kpt-doc, kpt-backend, kpt-app-ciq since last scan.
- **Alembic count confirmed:** alembic_activity(17), alembic_admin(12), alembic_health(7), alembic_projects(3) = **39 total** — no drift.
- **KNOWLEDGE-HUB pipe-inconsistency persists:** 3 different pipe counts (5, 6, 9) — per-line replacement required.
- **replace_all danger confirmed again:** entries in risk patterns table can match in multiple sections — always use unique single-line patterns.
- **Duplicate section header "Workflow-Verbesserungen" persists:** 2 instances in file — scan and remove older duplicates after update.
- **kpt-doc SYNCED status:** 0 unmerged vs origin/hermes (was origin/dev, corrected).

### 2026-05-26
- **CRITICAL Status Cleanup Pattern:** broad replace misses formatted variants — scan individually
- **kpt-app-ciq: 169 .mc + 20 .xml files** — massive expansion from 177
- **kpt-backend 9 translations:** de/en/es/fr/it/ja/nl/pt/zh-CN
- **kpt-backend docs/health-aggregation-api.md (8.7KB)**

### 2026-05-25
- **kpt-backend origin/dev SYNCED** (was 6 unmerged)
- **Post-Sync Drift Pattern:** drift resumes immediately after sync
- **kpt-backend origin/hermes drift:** 2 commits ahead on hermes after dev sync

### 2026-05-23
- **BRANCH OFFSET EXPLOSION:** kpt-app-ciq 168→739 commits in ~7h
- **kpt-backend dev stale:** origin/dev ahead 39 commits
- **ALL PRODUCTS SYNCED TO HERMES:** 8/10 OK, kpt-app-ciq CRITICAL, kpt-doc HIGH
- **Dual-offset measurement required** for all products

### 2026-05-21
- **Energy Progression Chart:** kpt-backend iterative commits
- **TASKS.md Complete-Gap:** TASK-020 missing features, TASK-021 file doesn't exist
- **WORKLOG 14+ days stale** since 2026-05-08
- **HAL Spec Complete:** all 8 milestones done
- **ScreenFlowController Overlay Stacking Fix:** 584 lines
- **2 skills created:** task-claim-verification, energy-screen-audit
