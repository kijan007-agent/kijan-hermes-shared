# 4-Datenbank-Migration-Stack Pattern

> Discovered 2026-05-23 from kpt-backend. Multi-domain repos need separate alembic stacks.

## Pattern

For repos with multiple independent domains, use **one alembic config per domain**:

```
<repo>/
  alembic_activity/       # Activity/session domain
  alembic_admin/          # Admin/tenant domain
  alembic_health/         # Health/metrics domain
  alembic_projects/       # Projects domain
```

## Why
- Different domains have different migration cadences
- Health migrations (partitioning, time-series) are completely independent from admin schemas
- Prevents migration conflicts across domains
- Each domain can have its own `env.py` tailored to its needs

## Implementation
```
alembic_activity/env.py    → --config alembic_activity/alembic.ini
alembic_admin/env.py       → --config alembic_admin/alembic.ini
alembic_health/env.py      → --config alembic_health/alembic.ini
alembic_projects/env.py    → --config alembic_projects/alembic.ini
```

Each stack has its own:
- `alembic.ini` (target DB URL, script location)
- `env.py` (domain-specific configuration)
- `versions/` (domain-specific migration history)

## Migration Counts (2026-05-27 update)
- Previous: 39 total (17+12+7+3)
- Current: 43 total (18+13+8+4)
- Delta: +4 (activity +1, admin +1, health +1, projects unchanged)
- Count with: `find <repo>/ -type d -name 'alembic_*' -exec find {} -name '*.py' \; | grep -c versions/`

## Pitfall
- Never share migrations across domains — they will conflict
- Each domain's `env.py` must set its own `target_metadata`
- Migration files in `versions/` are domain-scoped — no cross-domain references
