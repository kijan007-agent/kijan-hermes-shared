# ICD-10-GAM Datenquelle für Disease Catalog

## Download
- **URL:** https://www.inek.de/icd10-gam-download/
- **Format:** XML (primary), CSV (secondary)
- **Kosten:** Kostenlos mit Registrierung
- **Alternativ:** G-19 Krankenglossar (https://www.g-19.de/) mit ausführlichen Beschreibungen

## ICD-10 Category Mapping für Disease Catalog
| Code-Range | Category | Kijan-Relevanz |
|------------|----------|----------------|
| A00-B99 | infectious | medium |
| C00-D48 | neoplasms | low |
| E00-E90 | endocrine | medium |
| **G00-G99** | **nervous_system** | **HIGH — ME/CFS, Migräne, Fibro** |
| I00-I99 | circulatory | medium |
| J00-J99 | respiratory | low |
| K00-K93 | digestive | medium |
| **M00-M99** | **musculoskeletal** | **HIGH — Fibromyalgie** |
| N00-N99 | genitourinary | low |
| **F00-F99** | **mental** | **medium** |
| **R00-R94** | **symptoms/signs** | **HIGH — symptom-ICD codes** |

## Priority ICD Codes for Kijan (chronische Krankheiten)
| Code | DE Name | EN Name | Category |
|------|---------|---------|----------|
| G93.3 | Postvirales Fatiges-Syndrom | ME/CFS | nervous_system |
| M79.7 | Fibromyalgie | Fibromyalgia | musculoskeletal |
| G43 | Migräne | Migraine | nervous_system |
| I15.9 | Sekundäre Hypertonie | POTS | circulatory |
| M05 | Seropositive RA | Rheumatoid Arthritis | musculoskeletal |
| L40 | Psoriasis | Psoriasis | skin |
| F41.1 | Generalisierte Angst | Generalized Anxiety | mental |
| F32 | Depressive Episode | Depression | mental |

## Symptom-Krankheit-Mapping Prioritäten
- **G93.3 (ME/CFS):** Fatigue, PEM, Brain fog, Schlafstörungen, Kopfschmerz, Muskelschmerz, orthostatische Intoleranz
- **M79.7 (Fibro):** Generalisierter Schmerz, Fatigue, Brain fog, Schlafstörungen, Steifigkeit, Kribbeln
- **G43 (Migräne):** Kopfschmerz, Übelkeit, Lichtempfindlichkeit, Tonempfindlichkeit, Aura
- **Symptom-Kategorien:** pain, cognitive, sensory, energy, sleep, gastrointestinal, musculoskeletal, neurological
