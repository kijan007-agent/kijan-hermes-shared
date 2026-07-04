# Medizinischer Berater

## Triggers
- User fragt nach medizinischen Symptomen, Diagnosen, Laborwerten
- Work on health symptoms, disease catalog, ICD-10 mappings
- User wants medical interpretation of symptoms or lab results
- Health module task involves clinical criteria or differential diagnosis

## Rolle
Fachärztliches Experten-System — synthetisiert evidenzbasierte Medizin, Leitlinien und klinische Kriterien. Dient als medizinisches Nachschlagewerk für die Kijan Health Module Implementierung. **Ersetzt KEINE ärztliche Diagnose oder Behandlung.**

## Klinisches Wissen

### Diagnostische Kriterien-Referenz
| Syndrom | Kriterium | Kernmerkmal | Ausschluss |
|---------|-----------|-------------|------------|
| ME/CFS (ICC 2011) | PEM + ≥3/4 Symptome | Post-exertional Malaise | Andere Ursachen |
| ME/CFS (IOM 2015) | SEID: Aktivitätsverlust + PEM/Orthostase/Schlafstörung | ≥6 Monate Dauer | |
| Fibromyalgie (ACR 2010) | WPI ≥7 + SSS ≥5 ODER WPI 3-6 + SSS ≥9 | WPI = Widespread Pain Index, SSS = Symptom Severity Scale | Andere rheum. Ursachen |
| POTS | HR-Anstieg ≥30bpm in 10 Min Stehen | Keine Orthostase-Hypotonie | Andere Tachykardien |
| Rheumatoide Arthritis | ACR/EULAR ≥6/10 | Symmetrische Polyarthritis ≥6 Wochen | Infekt-/virale Arthropathien |
| Hypothyreose | TSH erhöht, fT3/fT4 niedrig | — | Non-thyroidal illness |

### Schmerz-Assessment-Standards
| Tool | Typ | Anwendung |
|------|-----|-----------|
| **NRS (0-10)** | Einzelfrage | Kern-Schmerzintensität |
| **BPI** | Intensität + Beeinträchtigung | Wöchentliche Deep-Dive |
| **McGill SF-MPQ-2** | Multidimensional | Klinische Reports |
| **PainDETECT** | Neuropathisch vs.nozizeptiv | Screening-Filter |
| **FSS (Fibromyalgia Severity Scale)** | 0-10 | Kurz-Screening |

### Komorbiditäts-Matrix (Kijan-relevant)
```
ME/CFS ───┬── POTS (30-60% Überlappung)
          ├── Fibromyalgie (30-60% Überlappung)
          ├── Mastzellsymptomatik (häufig)
          ├── Histamin-Intoleranz (häufig)
          └── Small Fiber Neuropathy (häufig)

Fibromyalgie ───┬── Zentrale Sensibilisierung (gemeinsam)
               ├── POTS/Komorbidität
               └── IBS/SIBO (häufig)

POTS ───┬── hEDS (bis 80% Überlappung)
        ├── Mastzellsymptomatik
        └── ME/CFS-ähnliche Fatigue
```

### Ausschlussdiagnostik (Baseline-Panel)
1. Blutbild (Anämie, Entzündung)
2. TSH, fT3, fT4 (Schilddrüse)
3. HbA1c (Diabetes)
4. Basischemie (Niere, Leber, Elektrolyte)
5. CRP, BSG (Entzündung)
6. Vitamin D, B12, Ferritin (Mangel)
7. ANA, RF (Autoimmun-Filter)
8. EBV-Serologie (falls relevant)

### Therapie-Referenz (Leitlinien-basiert)
- **ME/CFS:** Pacing Goldstandard. GET kritisch bewertet (CDC 2021). Symptomatisch: Fludrocortison/Midodrin für POTS, Gabapentin für Schmerz.
- **Fibromyalgie:** Multimodale Schmerztherapie. Amitriptylin 10-100mg, Duloxetin, Pregabalin. Keine Heilung, Management.
- **POTS:** Kompressionsstrümpfe, Salt/Fluid (10-12g Salz, 2-3L Wasser), Beta-Blocker, Midodrin, Fludrocortison. Leveritt-Protocol (Recline-First).

## Pitfalls
- **KEINE Diagnosen stellen** — immer "ärztliche Abklärung empfohlen"
- **ME/CFS: GET ist kontrovers** — niemals als Erstempfehlung
- **POTS-Diagnose** braucht Active Standing Test oder Tilt-Table, nicht nur Garmin HR
- **Komorbiditäten** sind die Regel, nicht die Ausnahme — immer mitdenken
- **ICD-10-GAM** ist Quelle für Disease Catalog in Health DB

## Related Skills
- `kijan-health-module`: Health DB Design, ICD-10-GAM, Symptom Tracking
- `pain-assessment-tools`: NRS, BPI, McGill, PainDETECT Details
- `promis-measures`: PROMIS Pain Severity/Interference scoring
