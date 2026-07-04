# Alembic Multi-Stack Migration Pattern for Kijan Backend

> Discovered 2026-05-23, validated 2026-05-27. kpt-backend uses 4 separate alembic stacks in one repo.

## Architecture

```
/workspace/Github/KijanPersonalTracker-hermes/kpt-backend/
  alembic_activity/       # 17 migrations — Activity/session domain
  alembic_admin/          # 12 migrations — Admin/tenant domain
  alembic_health/         # 7 migrations  — Health/metrics domain
  alembic_projects/       # 3 migrations  — Projects domain
  alembic_i18n/           # 1 migration   — i18n catalog (single table)
  ─────────────────────────────────────────────
  TOTAL: 40 migrations across 5 stacks
```

## Why 4 Stacks
- Different domains have different migration cadences
- Health migrations (partitioning, time-series) independent from admin schemas
- Prevents migration conflicts across domains
- Each domain can have its own `env.py` tailored to its needs
- Each stack targets a different database: admin (kijan_admin), activity/projects/health (kijan_tracker)

## Key Patterns

### Idempotent Migrations
- **ALWAYS** check column/table existence before ALTER TABLE
- Pattern: use `sa.Column` introspection via `metadata.reflect()` before adding columns
- `if not column_exists(conn, 'table', 'column'):` → then ALTER TABLE
- **PITFALL:** Running migrations twice on a different env (dev → prod) fails without existence checks

### Partition Reordering
- When reordering table partitions: drop → recreate in new order → validate constraint
- **PITFALL:** Foreign key constraints must be temporarily disabled during partition reordering
- **PITFALL:** Handle migration errors gracefully — verify after each step

### Rename Table Pattern
- Safe table rename: rename_table(table, new_name) with cascade handling
- Update all foreign key references, indexes, and constraints
- **PITFALL:** Alembic `op.rename_table()` does NOT auto-update FK constraints — manual updates needed

### Migration File Naming
- Use descriptive names: `alembic_health/versions/001_create_health_tables.py`
- Include domain prefix in migration messages: `[health] create symptom_logs table`

## Command Usage
```bash
# Activity stack
alembic --config alembic_activity/alembic.ini upgrade head

# Admin stack
alembic --config alembic_admin/alembic.ini upgrade head

# Health stack
alembic --config alembic_health/alembic.ini upgrade head

# Projects stack
alembic --config alembic_projects/alembic.ini upgrade head

# Generate migration
alembic --config alembic_health/alembic.ini revision --autogenerate -m "health: add new table"
```

## Cross-Product Relevance
This pattern applies to any multi-domain repo where different modules have independent migration needs:
- Separate DB URLs per domain (admin vs main)
- Different migration cadences per domain
- Prevents migration conflicts across domains