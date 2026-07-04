# Backend Fix Template

> Use this template when applying backend fixes to KijanPersonalTracker.

## Checklist

- [ ] `SECRET_KEY`/`REGISTRATION_KEY` have startup validation
- [ ] All `session.commit()` wrapped in `_safe_commit()`
- [ ] Onboarding ephemeral keys validate hash format
- [ ] `execute_with_retry` has exponential backoff + rollback
- [ ] Database URLs validated against defaults/localhost
- [ ] SlowAPI fallback logs at ERROR level
- [ ] RankingEngine uses correct DB session for each model

## Post-Fix Verification

```bash
# Start test env
docker compose -f kpt-backend/docker-compose.dev.yml up -d

# Check health
curl http://localhost:8000/health

# Verify no startup errors
docker compose -f kpt-backend/docker-compose.dev.yml logs api | grep -i error
```

## Common Pitfalls

1. **Never commit raw `session.commit()` without try/except/rollback** — 60+ instances in repositories.py
2. **Environment variables without defaults cause NoneType crashes** — always provide empty string default
3. **Database URL mismatch between dev/prod** — validate at startup, not at runtime
4. **SlowAPI silently falls back to no-rate-limit** — must log ERROR, not WARNING
