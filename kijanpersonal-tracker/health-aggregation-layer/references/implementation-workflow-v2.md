# HAL Implementation Workflow — Verified Pattern (2026-05-20)

## Workflow: Spec → Migration → DAL → API → Tests → CI/CD → Docs

### Phase 1: Spezifikationen
1. Create directory: `kpt-doc/_specs/<feature-name>/`
2. Write architecture doc: `architecture/system-architecture.md`
3. Write data model doc: `architecture/data-model.md`
4. Write API spec: `api-spec/rest-api.md`
5. Write sub-domain specs (time-series, reports, import, testing, etc.)
6. Commit to kpt-doc submodule: `git add <dir>`, `git commit -m "docs: ..."`, `git push origin hermes`
7. Update parent repo: `git submodule update --remote kpt-doc`, `git add kpt-doc`, `git commit`, `git push`

### Phase 2: Alembic Migration
1. Create: `kpt-backend/alembic_health/versions/NNNN_feature_name.py`
2. Define all tables, indexes, partitions, seed data
3. Test migration manually: `psql -h ... -f migration_sql`
4. Commit + push to kpt-backend

### Phase 3: DAL Layer
1. Create: `kpt-backend/app/database_health.py` (raw table definitions + session helper)
2. Create: `kpt-backend/app/dal/health_dal.py` (HealthDALRegistry + 6+ Repositories)
3. Use `BaseHealth` for ORM models, raw tables for aggregation queries
4. Commit + push to kpt-backend

### Phase 4: REST API
1. Create: `kpt-backend/app/routers/health_*.py`
2. Use Pydantic schemas for all request/response types
3. Use `tags=["health-aggregation"]` for OpenAPI grouping
4. Register in `kpt-backend/app/main.py`:
   ```python
   from app.routers import health_aggregation
   app.include_router(health_aggregation.router, prefix="/api/health", tags=["health-aggregation"])
   ```
5. Add `get_health_session` to `kpt-backend/app/database.py`
6. Commit + push to kpt-backend

### Phase 5: Tests
1. Create: `kpt-backend/tests/test_health_<feature>.py`
2. Create: `kpt-backend/tests/conftest_<feature>.py` (fixtures)
3. Create: `kpt-backend/tests/test_<feature>_data_generator.py` (CLI test data gen)
4. Register test classes: TST-HAL-XXX naming convention
5. Commit + push to kpt-backend

### Phase 6: CI/CD Pipeline
1. Create: `kpt-backend/.github/workflows/<feature>-test.yml`
2. Define PostgreSQL 16 service container
3. Run migrations, tests, data generator
4. Commit + push to kpt-backend

### Phase 7: API Documentation
1. Create: `kpt-backend/docs/<feature>-api.md`
2. Document ALL endpoints with request/response examples
3. Reference Swagger URL: `GET /api/<feature>/docs`
4. Commit + push to kpt-backend

### Phase 8: Final Parent Update
1. `git submodule update --remote <submodule>` to get new HEAD
2. `git add <submodule>` in parent
3. `git commit -m "chore: update <submodule> → <hash> (<feature>)"`
4. `git push origin hermes`
5. Verify ALL submodules with `git submodule status`
6. Verify parent with `git status --short` — must be clean

## Verification Checklist
- [ ] All files exist at correct paths
- [ ] `git status --short` clean in ALL repos
- [ ] `git submodule status` shows correct commits (no `+` prefix)
- [ ] All pushed to origin/hermes
- [ ] Swagger URL accessible: `GET /api/<feature>/docs`
- [ ] API docs exist: `docs/<feature>-api.md`
