# Feature Branch Divergence Pattern

When the `feature` branch leads the `hermes` branch by significant margins across multiple products, this indicates active parallel development that requires attention.

## Detection Thresholds

| Delta | Signal | Action |
|-------|--------|--------|
| > 0 files | INFO | Note in status report |
| > 50 files | WARNING | Feature branch actively diverging |
| > 100 files | HIGH | Significant parallel development — consider sync |
| > 200 files | CRITICAL | Major divergence — feature branch may contain unmerged work |

## Session Evidence (2026-06-27 17:30)

| Produkt | Feature | Hermes | Delta | Signal |
|---------|---------|--------|-------|--------|
| kpt-backend | 255 (148 py) | 185 (102 py) | +70 | WARNING |
| kpt-app-ciq | 364 (230 mc) | 324 (214 mc) | +40 | INFO |
| kpt-doc | 996 (972 md) | 715 (691 md) | +281 | CRITICAL |

## New Patterns in Feature Branch (2026-06-27)

### kpt-backend NEW Services
- `activity_aggregation_service.py` (6KB) — HAL v2 Service Layer pattern
- `integrity_check.py` (4KB) — data integrity verification
- **HAL v2 Service Layer**: Raw SQLAlchemy HAL mit Service-Layer-Abstraktion

### kpt-backend NEW Routers
- `alerts.py` (5.6KB) — event-driven alerts via DB-backed queue
- `pdf.py` (29KB) — server-side PDF generation
- `activity_aggregation.py` (16KB) — HAL aggregation endpoint

### kpt-backend Growth
- `activities.py`: 92KB → 119KB (+29KB)
- `personal.py`: 102KB → 161KB (+59KB)
- `auth_enhanced.py`: 23KB → 33KB (+10KB)
- Routers: 9 → 12 files

### kpt-app-ciq Growth
- ScreenFlowController.mc: 72KB → 83KB
- KijanActivityTrackerService.mc: 54KB → 80KB
- KijanActivityTrackerView.mc: 71KB → 86KB
- i18n: 9 → 11 Sprachen (DE/EN/FR/ES/IT/JP/NL/PT/ZH)
- FSM files STILL PRESENT (5 docs in source/)

### kpt-doc Growth
- MEMORY: 309 .md files — **MEMORY_INDEX.md STILL NOT FOUND**
- user-facing/: 26 items (7+ languages)
- workflow/: 4 items (ROLES_SKILLS_MATRIX.md 37KB)
- _1_refinement/: 7 items (MSA proposal, symptom tracking spec)
- _tasks/: 332 items — _done/: 26 items
- NEW docs: RELEASE_PROCEDURE.md, AUTOMATED_TESTING_INSTRUCTIONS.md, COST_ANALYSIS.md, DATABASE_ARCHITECTURE.md, SCREEN_FLOW_ARCHITECTURE.md, TASK_PROCESSING_WORKFLOW.md (+STAGING)

## Action Items
1. **kpt-doc MEMORY_INDEX.md**: Still not found — CRITICAL
2. **kpt-backend HAL v2 Service Layer**: New pattern, document in knowledge hub
3. **kpt-app-ciq FSM files**: Still present in source/ — cleanup needed
4. **kpt-backend i18n**: NO translations/ — i18n layer NOT PRESENT (was 9 in hermes)
5. **Cross-product sync**: Feature branch leads all 3 products — evaluate merge readiness

## Related Patterns
- `references/branch-offset-monitoring.md` (hermes-branch-watcher) — commit-level divergence
- `references/drift-direction-reversal.md` (hermes-branch-watcher) — direction tracking
- `references/ai-tool-config-proliferation.md` (knowledge-hub-maintenance) — file count accuracy