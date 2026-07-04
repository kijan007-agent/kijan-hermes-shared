# Backend Audit Checklist — Critical Patterns

> Generated 2026-05-12 from KijanPersonalTracker code review.

## P0 — Must Fix

### 1. Secret/Key Default Validation
```python
SECRET_KEY = os.getenv('SECRET_KEY', '')
REGISTRATION_KEY = os.getenv('REGISTRATION_KEY', '')

def validate_config():
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is empty — app will crash at startup")
    if not REGISTRATION_KEY:
        raise RuntimeError("REGISTRATION_KEY is empty — app will crash at startup")
    logger.info("Config validation passed")
```
Call `validate_config()` at module load time or in `main.py` startup.

### 2. Repository Commit Rollback
Never use raw `self.session.commit()` without error handling. Use:
```python
def _safe_commit(session):
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
```
Every `session.commit()` in `repositories.py` must be replaced with `_safe_commit(self.session)`.

### 3. Onboarding Auth Security
Ephemeral keys must validate hash format:
```python
if not key_hash or key_hash == '0' * len(key_hash):
    return HTTPException(status_code=400, detail="Invalid onboarding key")
```
Reject empty/zero-filled hashes. Never accept arbitrary hex as valid.

### 4. execute_with_retry — Exponential Backoff + Rollback
```python
async def execute_with_retry(db, stmt, params=None):
    from sqlalchemy.exc import OperationalError, InterfaceError
    import asyncio
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await db.execute(stmt, params)
        except InvalidCachedStatementError:
            await asyncio.sleep(0.01 * (2 ** attempt))
            if attempt == 0:
                await db.rollback()
            continue
        except (OperationalError, InterfaceError) as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(0.1 * (2 ** attempt))
                await db.rollback()
                continue
            raise
```

### 5. Database URL Validation
```python
def validate_database_urls():
    errors = []
    for name, url in [(n, u) for n, u in [
        ("DATABASE_URL_ADMIN", DATABASE_URL_ADMIN),
        ("DATABASE_URL_ACTIVITY", DATABASE_URL_ACTIVITY),
        ("DATABASE_URL_PROJECTS", DATABASE_URL_PROJECTS),
        ("DATABASE_URL_HEALTH", DATABASE_URL_HEALTH),
    ]:
        if not url:
            errors.append(f"{name} is empty")
        elif not url.startswith('postgresql+asyncpg://'):
            errors.append(f"{name} missing postgresql+asyncpg:// prefix")
        elif 'kijan_password' in url:
            errors.append(f"{name} uses default password")
        elif 'localhost' in url:
            errors.append(f"{name} points to localhost")
    return errors
```

### 6. SlowAPI Fallback — ERROR Level Logging
When slowapi is not installed, log at ERROR level (not WARNING):
```python
except ImportError:
    logger.error("slowapi not installed — rate limiting DISABLED. SECURITY RISK!")
    logger.error("Ensure rate limiting is enabled in production!")
```

## P1 — Important

### 7. RankingEngine DB Sessions
When using `ProjectTaskActivity`, query against `db_projects` not `db_activity`. Different DBs = no shared tables.

### 8. Transaction Isolation
Between read and write in the same operation, use `SELECT ... FOR UPDATE` or explicit locking to prevent race conditions.

## P2 — Code Quality

### 9. Configurable Constants
`HEALTH_STATES` and `LOAD_TYPES` as module-level dicts should be moved to config/env for hot-reload capability.

### 10. Naming Conventions
- Classes: PascalCase (`SpoonsCheckinDelegate`, not `spoonsCheckinDelegate`)
- Variables: camelCase
- Constants: UPPER_SNAKE_CASE
