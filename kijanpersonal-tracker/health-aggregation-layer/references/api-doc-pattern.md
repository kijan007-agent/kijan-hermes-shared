# HAL API Documentation Pattern (Two-Tier Approach)

## Tier 1: Auto-Generated Swagger (FastAPI)
- URL: `GET /api/<feature>/docs`
- Generated from Pydantic schemas, `@router.*` decorators, `summary`/`description` fields
- Live testing capability
- Always available in production

## Tier 2: Manual Markdown Documentation
- Location: `kpt-backend/docs/<feature>-api.md`
- Location: `kpt-doc/_specs/<feature>/api-spec/rest-api.md`
- Content: All endpoints with request/response examples, error codes, rate limits, i18n notes
- Format: Standard markdown with tables for endpoints, params, schemas

## API Doc Structure
```
docs/<feature>-api.md
├── Schnellstart (Swagger URLs)
├── Endpunkte pro Sub-Feature
│   ├── Tabelle: Methode | Pfad | Beschreibung
│   ├── Request Body Beispiel
│   └── Response Beispiel
├── Fehlercodes
├── Rate Limits
└── i18n Support
```

## Naming Convention
- Feature: `health-aggregation-api.md` or `feature-name-api.md`
- Spec: `api-spec/rest-api.md` + `api-spec/async-jobs.md` + `api-spec/websocket-events.md`
