# Review: MCP-Server fuer Medizinische Recherche
**Datum:** 2026-09-29
**Task:** t_e92fed7b
**Profile:** medizinischer-berater, arzt

---

## 1. Ausgangslage und Ziel

KPT-Backend erhaelt einen MCP-Server, der medizinische Literaturrecherche (arxiv + PubMed) als Werkzeuge fuer LLM-Agenten bereitstellt. Review covers:
- Bestehende arxiv-Skill-Integration
- Empfehlung fuer PubMed/E-utilities-API-Einbindung
- Compliance-Grenzen (PHI/PII-Schutz, keine klinischen Diagnosen)
- Tool-Design fuer medizinische Recherche

---

## 2. Bestehende Stack-Analyse

### 2.1 arxiv-Skill (`research/arxiv`)
- **Status:** Implementiert, funktional
- **API:** REST/Atom XML, keine Auth, Rate ~1 req/3s
- **Verfuegbare Tools (Skill):**
  - `search_arxiv.py` mit Parsing (--max, --sort, --author, --category, --id)
  - Semantic Scholar API fuer Citations, References, Recommendations, Author Profiles
- **Gaps:**
  - Kein MCP-Tool-Wrapper vorhanden (Skill ist CLI-basiert)
  - Kein Caching/Mehrsprachigkeit
  - Keine DeepL-Integration fuer Abstract-Zusammenfassungen

### 2.2 PubMed/E-utilities
- **Status:** Nicht vorhanden
- **API:** NCBI E-utilities (ESearch, EFetch, ESummary)
  - ESearch: Stichwort-/Autor-/Mesh-Suche
  - EFetch: Volltexte (MEDLINE/XML)
  - ESummary: Zusammenfassungen (不爱XML)
- **Rate:** 3 req/s via API Key (default: 1 req/s)
- **Key Endpoint:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

### 2.3 MCP-Native-Integration
- **Config:** `mcp_servers: {}` (keine Server konfiguriert)
- **Tool-Discovery:** Automatic via config.yaml
- **Provider:** auto (ncp, stdio, HTTP)

---

## 3. Empfehlungen: Tool-Design

### 3.1 arxiv MCP Tool (Erweiterung bestehenden Skills)

| Tool | Input | Output | Anmerkung |
|------|-------|--------|-----------|
| `arxiv_search` | query, max_results, sortBy | JSON: [{id, title, authors, abstract, categories, published}] | Bereits im Skill vorhanden, als MCP wrappen |
| `arxiv_fetch` | arxiv_id | JSON: Vollständige Metadaten + PDF-URL | 1 Req/3s Rate Limit |
| `arxiv_citations` | arxiv_id | JSON: Citations + References via Semantic Scholar | 1 req/s, API Key empfohlen |
| `arxiv_recommendations` | arxiv_ids[] | JSON: Paper-Recommendations | POST /recommendations/v1/papers/ |

**Design-Hinweis:** arxiv ist fuer Preprints/ML-Papers geeignet. Fuer kliniknahe medizinische Literatur ist PubMed PRIMARY.

### 3.2 PubMed MCP Tool (Neuentwicklung)

```python
# Empfohlenes MCP-Tool-Interface
TOOLS = [
    {
        "name": "pubmed_search",
        "description": "Search PubMed/MEDLINE by keyword, author, MeSH terms",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search terms (supports MeSH, author:..., [pt] filt...)"},
                "max_results": {"type": "integer", "default": 10, "max": 100},
                "filter": {"type": "string", "description": "e.g. free_fulltext[ft], review[pt], clinicaltrial[pt]"},
                "datetype": {"type": "string", "description": "dp (date published), edat (Entrez date), pdat"},
                "mindate": {"type": "string", "description": "YYYY/MM/DD"},
                "maxdate": {"type": "string", "description": "YYYY/MM/DD"},
            }
        }
    },
    {
        "name": "pubmed_fetch",
        "description": "Fetch full PubMed article metadata by PMID",
        "input_schema": {
            "type": "object",
            "properties": {
                "pmid": {"type": "string"},
                "pmids": {"type": "array", "items": {"type": "string"}, "maxItems": 100},
                "format": {"type": "string", "enum": ["medline", "abstract", "summary"], "default": "abstract"},
            }
        }
    },
    {
        "name": "pubmed_mesh_tree",
        "description": "Get MeSH term tree structure for hierarchy navigation",
        "input_schema": {
            "type": "object",
            "properties": {
                "term": {"type": "string"},
            }
        }
    }
]
```

### 3.3 Compliance-Grenzen (Aus `compliance-medizin`)

| Aktivitaet | Erlaubt | Grenze |
|------------|---------|--------|
| Literatursuche nach Symptomen | JA | Keine personenbezogenen Daten in Query |
| Abstract/Fulltext abrufen | JA | Keine PHI in Anfragen |
| Studienlage synthetisieren | JA, beratend | KEINE Diagnose, KEINE Behandlungsempfehlung ohne Arzt |
| PubMed Clinical Queries | JA | z.B. `therapeutic[sb]`, `etiology[sb]` |
| Arxiv-Preprints | JA | Preprints == nicht peer-reviewed, als solches kennzeichnen |

**Verboten:**
- Patientendaten in Suchanfragen (keine "Patient mit X, Y, Z")
- Klinische Entscheidungen ohne humanaerztliche Ueberpruefung
- Direkte Diagnosen basierend auf Studienlage

### 3.4 Qualitaetssignale fuer medizinische Literatur

```
Evidence Hierarchy (absteigend):
  1. Systematic Reviews / Meta-Analysen (Cochrane)
  2. Randomisierte Kontrollierte Studien (RCT)
  3. Kohortenstudien
  4. Fall-Kontroll-Studien
  5. Case Reports
  6. Preprints (arxiv) -- KEINE peer-review

Relevanz-Filter (PubMed):
  - review[pt]           -- Reviews
  - clinicaltrial[pt]    -- Clinical Trials
  - guideline[pt]        -- Guidelines
  - meta-analysis[pt]    -- Meta-Analysen
  - free_fulltext[ft]    -- Frei zugaenglich

Klinische Query-Filter (PubMed Clinical Queries):
  - etiology[sb]          -- Aetiologie
  - prognosis[sb]        -- Prognose
  - diagnosis[sb]        -- Diagnose
  - treatment[sb]        -- Therapie
  - qualitative[sb]       -- Qualitative Studien
```

---

## 4. Architektur-Vorschlag

### 4.1 MCP-Server Struktur (kpt-backend)

```
kpt-backend/
  mcp/
    servers/
      __init__.py
      arxiv_server.py      # arxiv + Semantic Scholar MCP tools
      pubmed_server.py     # PubMed E-utilities MCP tools
      config.py            # Rate limits, API keys, caching
    pyproject.toml         # Abhaengigkeiten: mcp, httpx, lxml
```

### 4.2 Abhaengigkeiten

```toml
[project]
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
    "cachetools>=5.0.0",
]
```

### 4.3 Rate Limiting Strategy

| API | Limit | Strategie |
|-----|-------|-----------|
| arXiv API | 1 req / 3s | Client-seitig: `time.sleep(3)` zwischen Requests |
| Semantic Scholar | 1 req/s (free), 100/s (API key) | API-Key-Env-Var, Exponential Backoff |
| PubMed E-utilities | 3 req/s (mit API Key), 1 req/s (default) | NCBI-API-Key in Env, Request-Queue |

---

## 5. Verifikation / Tests

Empfohlene Testcases fuer das MCP-Server-Modul:

```
Test 1: arxiv_search
  Input:  query="ME/CFS pacing therapy", max_results=5
  Expect: JSON mit 5 Paper-IDs, Titeln, Abstracts

Test 2: pubmed_search mit MeSH
  Input:  query="Fibromyalgia[mh] AND Amitriptyline[tiab]", max_results=10
  Expect: PMID-Liste, Titel, Journal, Jahr

Test 3: pubmed_fetch mit mehreren PMIDs
  Input:  pmids=["12345678","23456789"], format="abstract"
  Expect: MEDLINE-XML/Abstract-Format

Test 4: Compliance — PHI in Query
  Input:  query="Patient Jan Kiefer Fatigue PEM"
  Expect: Review-Flag oder Rejection, KEINE Patientendaten im Request-Log

Test 5: Rate Limit Handling
  Input:  10x rapid arxiv_search
  Expect: 200er Responses, kein 429 (dank Rate-Limiter)
```

---

## 6. Follow-up Tasks

| Task | Titel | Assignee | Status |
|------|-------|---------|--------|
| t_b9a1e3c7 | PubMed MCP Toolchain: E-utilities + MeSH + Caching | arzt | todo |
| t_8f2d5a91 | arxiv + PubMed MCP Showcase: Testcode + Beispiele | software-development | todo |

---

## 7. Fazit

**arxiv-Skill:** Funktional, kein MCP-Wrapper vorhanden. Als MCP-Tools wrappen fuer Tool-Discovery.

**PubMed:** Vollstaendig fehlend. E-utilities API ist kostenlos, gut dokumentiert, fuer medizinische Literatur PRIMARY. Sollte als separater MCP-Server `pubmed_server.py` implementiert werden.

**Compliance:** Klare Grenzen definiert. Keine PHI in Queries, keine Diagnosen, keine Behandlung ohne Arzt. Review-Patterns fuer Compliance-Checks einbauen.

**Naechster Schritt:** `arzt`-Profile erstellt Child-Tasks fuer PubMed-Implementation. `software-development`-Profile fuer Tests/Showcase.
