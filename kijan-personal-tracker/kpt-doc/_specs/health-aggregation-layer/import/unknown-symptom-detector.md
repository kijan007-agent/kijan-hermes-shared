# UnknownSymptomDetector — Spec

## Purpose

Detects novel / unknown symptom patterns by clustering raw symptom descriptions
from multiple import sources (CSV, daily check-in, manual entry).

## Architecture

```
SymptomEntry (dataclass)
    ├── description: str
    ├── source: str
    └── timestamp: str | None

UnknownSymptom (dataclass)
    ├── cluster_id: int
    ├── name: str
    ├── confidence: float
    ├── member_descriptions: list[str]
    └── source_count: int

UnknownSymptomDetector (class)
    ├── cluster_symptoms(entries) -> list[UnknownSymptom]
    └── cluster_threshold, suggest_floor, min_cluster_size

UnknownSymptomRouter (class)
    └── FastAPI router at /api/unknown-symptoms
```

## Algorithm

1. **Tokenization** — lowercase, strip punctuation, filter German stop words
   and tokens shorter than 3 characters.
2. **TF-IDF** — lightweight term-frequency × inverse-document-frequency vectors
   (no external dependencies).
3. **Agglomerative clustering** — bottom-up merging by cosine similarity
   (threshold 0.35 default).
4. **Cluster naming** — top-3 frequent tokens per cluster, joined by " + ".
5. **Confidence scoring** — average pairwise cosine similarity within cluster.
6. **Suggestion floor** — only clusters with confidence >= `SUGGEST_FLOOR`
   (0.5) are returned as actionable items.

## Constants

| Name | Value | Description |
|------|-------|-------------|
| `SUGGEST_FLOOR` | `0.5` | Minimum confidence for automatic suggestion |
| `CLUSTER_MIN_SIZE` | `2` | Minimum members per cluster |
| `cluster_threshold` | `0.35` | Cosine similarity threshold for merging |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/unknown-symptoms/cluster` | Submit symptom entry, get clusters |
| GET | `/api/unknown-symptoms` | List all known clusters |

## Testing

- Unit tests for `_cluster_def_names()` helper
- Integration tests for `cluster_symptoms()` with known inputs
- Router endpoint tests
