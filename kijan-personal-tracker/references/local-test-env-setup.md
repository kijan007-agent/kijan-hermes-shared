# Local Test Environment Setup

## Docker Compose (kpt-backend)

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: kijan-db-dev
    environment:
      POSTGRES_USER: kijan_user
      POSTGRES_PASSWORD: kijan_password
      POSTGRES_DB: kijan_tracker
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U kijan_user -d kijan_tracker"]
      interval: 5s
      timeout: 3s
      retries: 5
    volumes:
      - db_data_dev:/var/lib/postgresql/data

  api:
    build:
      context: ..
      dockerfile: Dockerfile.dev
    container_name: kijan-api-dev
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL_ADMIN=postgresql+asyncpg://kijan_user:kijan_password@db:5432/kijan_tracker
      - DATABASE_URL_ACTIVITY=postgresql+asyncpg://kijan_user:kijan_password@db:5432/kijan_activity
      - DATABASE_URL_PROJECTS=postgresql+asyncpg://kijan_user:kijan_password@db:5432/kijan_projects
      - DATABASE_URL_HEALTH=postgresql+asyncpg://kijan_user:kijan_password@db:5432/kijan_health
      - SECRET_KEY=dev-secret-key-change-in-prod
      - REGISTRATION_KEY=dev-registration-key
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ..:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  db_data_dev:
```

## .env file (kpt-backend/.env)

```
DATABASE_URL_ADMIN=postgresql+asyncpg://kijan_user:kijan_password@db:5432/kijan_tracker
DATABASE_URL_ACTIVITY=postgresql+asyncpg://kijan_user:kijan_password@db:5432/kijan_activity
DATABASE_URL_PROJECTS=postgresql+asyncpg://kijan_user:kijan_password@db:5432/kijan_projects
DATABASE_URL_HEALTH=postgresql+asyncpg://kijan_user:kijan_password@db:5432/kijan_health
SECRET_KEY=dev-secret-key-change-in-prod
REGISTRATION_KEY=dev-registration-key
```

## Prod Dump Workflow

1. Run `./scripts/dump_prod.sh` on PROD server → `dumps/prod_YYYYMMDD.dump`
2. Copy dump to local `dumps/` directory
3. Run `./scripts/load_dev.sh` → loads into kijan-db-dev

## ⚠️ Environment Constraint

**No Docker or pg_dump available on the Hermes agent machine.** All docker/compose/pg_dump operations must be run locally by the user. The agent creates the config files and scripts, but cannot execute them.

## Verification

```bash
docker compose -f docker-compose.dev.yml ps
docker compose -f docker-compose.dev.yml logs db
# Health check: pg_isready -h localhost -p 5432 -U kijan_user -d kijan_tracker
# API check: curl http://localhost:8000/health
```

## Troubleshooting

- Port 5432 in use: `lsof -i :5432` → kill or change port in compose
- Container won't start: `docker compose -f docker-compose.dev.yml logs db`
- Migration errors: run `alembic upgrade head` inside the api container
