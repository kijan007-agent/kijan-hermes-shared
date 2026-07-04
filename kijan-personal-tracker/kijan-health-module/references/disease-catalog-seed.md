# Disease Catalog Seed — Priority ICD Codes & Symptom Mappings

## Priority ICD Codes for Kijan (chronische Erkrankungen)

### G93.3 — ME/CFS (Postviral Fatigue Syndrome)
| Symptom | Kategorie | Prevalence | Core |
|---------|-----------|------------|------|
| Fatigue | energy | 0.99 | true |
| Post-exertional malaise (PEM) | energy | 0.95 | true |
| Brain fog | cognitive | 0.85 | true |
| Schlafstörungen | sleep | 0.70 | false |
| Kopfschmerz | pain | 0.55 | false |
| Muskelschmerz | musculoskeletal | 0.65 | false |
| Gelenkschmerz | musculoskeletal | 0.50 | false |
| Orthostatische Intoleranz | circulatory | 0.60 | false |

### M79.7 — Fibromyalgie
| Symptom | Kategorie | Prevalence | Core |
|---------|-----------|------------|------|
| Generalisierter Schmerz | pain | 0.99 | true |
| Fatigue | energy | 0.85 | true |
| Brain fog | cognitive | 0.70 | true |
| Schlafstörungen | sleep | 0.80 | false |
| Kopfschmerz | pain | 0.45 | false |
| Steifigkeit | musculoskeletal | 0.60 | false |
| Kribbeln | neurological | 0.30 | false |

### G43 — Migräne
| Symptom | Kategorie | Prevalence | Core |
|---------|-----------|------------|------|
| Kopfschmerz | pain | 0.99 | true |
| Übelkeit | gastrointestinal | 0.40 | false |
| Lichtempfindlichkeit | sensory | 0.75 | false |
| Tonempfindlichkeit | sensory | 0.60 | false |
| Brain fog | cognitive | 0.30 | false |
| Aura | neurological | 0.25 | false |

## JSON Seed Format (für seed_disease_catalog.py)
```json
{
  "icd10_code": "G93.3",
  "name_de": "Postvirales Fatiges-Syndrom",
  "name_en": "Myalgic Encephalomyelitis / Chronic Fatigue Syndrome",
  "category": "nervous_system",
  "description": "Chronische multisystemische Erkrankung mit schwerster Fatigue und Post-Exertional Malaise",
  "symptoms": [
    {"symptom_name": "Fatigue", "symptom_category": "energy", "prevalence": 0.99, "is_core": true},
    {"symptom_name": "Post-exertional malaise", "symptom_category": "energy", "prevalence": 0.95, "is_core": true},
    {"symptom_name": "Brain fog", "symptom_category": "cognitive", "prevalence": 0.85, "is_core": true},
    {"symptom_name": "Schlafstörungen", "symptom_category": "sleep", "prevalence": 0.70, "is_core": false},
    {"symptom_name": "Kopfschmerz", "symptom_category": "pain", "prevalence": 0.55, "is_core": false},
    {"symptom_name": "Muskelschmerz", "symptom_category": "musculoskeletal", "prevalence": 0.65, "is_core": false},
    {"symptom_name": "Gelenkschmerz", "symptom_category": "musculoskeletal", "prevalence": 0.50, "is_core": false},
    {"symptom_name": "Orthostatische Intoleranz", "symptom_category": "circulatory", "prevalence": 0.60, "is_core": false}
  ]
}
```

## Quellen für Symptom-Prevalence
- ICD-10-GAM Beschreibungen (InEK)
- PROMIS Pain Measures (NRS/BPI validation studies)
- bearable-app-assessment.md §2.1 (chronic illness symptom prevalence)
- MIMIC-IV (pain-vital correlations for research)
- NHANES (epidemiological baselines)
