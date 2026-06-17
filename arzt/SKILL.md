# Arzt

## Triggers
- User fragt nach Arztbesuch-Vorbereitung, Befunden, Überweisungen
- Work on medical documentation, clinical reports, ICD-10 coding
- Interpretation of lab results, imaging, EKG, Holter
- Task involves clinical decision-making support

## Rolle
Ärztliches Experten-System — klinisches Denken, Differentialdiagnostik, Leitlinien-basierte Medizin und Arzt-Patienten-Kommunikation. Dient als klinische Entscheidungsunterstützung. **Ersetzt KEINE ärztliche Diagnose oder Behandlung.**

## Klinisches Denken

### Differentialdiagnostik: Algorithmus
```
Symptom → Prävalenz prüfen → Red Flags prüfen → DD-Liste → Priorisierung → Test → Diagnose
```

#### Red Flags (immer zuerst ausschließen!)
| Symptom | Mögliche lebensbedrohliche Ursache |
|---------|-----------------------------------|
| Fatigue | Herzinsuffizienz, Schilddrüsenkoma, Sepsis |
| Schwindel | TIA, Hirnblutung, Aortendissektion |
| Schmerzen | ACS, Pulmonalembolie, Aortenaneurysma |
| Kognitive Störung | Enzephalitis, Subduralhämatom, Wernicke |
| Orthostase-Probleme | Lungenembolie, schwere Dehydratation |

### Befundinterpretation

#### Labor: Fatigue-Panel
| Befund | Normal | Auffällig bei chron. Erkrankungen | Interpretation |
|--------|--------|----------------------------------|----------------|
| Hb | 12-16 g/dl (F) | <11: anämisch, >16: polyzythämisch | Anämie als Fatigue-Ursache |
| CRP | <5 mg/l | >10: Entzündung, >50: akut | Entzündungsstatus |
| TSH | 0,4-4,0 mIU/l | >4,5: Subklinisch, >10: klinisch | Schilddrüse als Fatigue-Ursache |
| fT3/fT4 | Referenz | ↓ bei Non-Thyroid Illness | Nicht automatisch substituieren! |
| Vitamin D | 30-60 ng/ml | <20: Mangel, <10: Defizit | Korrigieren → oft Besserung |
| B12 | 200-900 pg/ml | <200: Mangel | Neurologische Symptome möglich |
| Ferritin | 20-200 ng/ml | <30: Eisenmangel (auch ohne Anämie) | |
| Natrium | 136-145 mmol/l | <135: Hypo-Natriämie | Kann Fatigue/Schwindel verursachen |
| Kalium | 3,5-5,0 mmol/l | Abweichung: Muskelkrämpfe, Herzrhythmus | |
| BNP | <100 ng/l | >100: HF-Wahrscheinlichkeit | Bei Dyspnoe/Ödemen |
| Eosinophile | 0,02-0,5 ·10⁹/l | ↑ bei Mastzellsymptomatik, Parasiten | |

#### EKG: POTS-typische Befunde
- Ruhe-Tachykardie >100 bpm (bei manchen Patienten)
- Sinus-Tachykardie im Stehen (+30 bpm)
- Geringe RR-Amplitude bei Orthostase
- T-Wellen-Inversion (selten, bei Komplexität)

#### Holter-Monitoring bei POTS
- Tag/Nacht-Herzfrequenz-Verhältnis >0,9 (normal <0,85)
- Keine arrhythmischen Ursachen für Tachykardie
- Max. HR >150 bei minimaler Belastung möglich

### Arzt-Patienten-Kommunikation

#### Befundgespräch: SPIKES-Protokoll
1. **S**etting: Rahmen schaffen (privat, genug Zeit, Bezugsperson möglich)
2. **P**erception: "Was wissen Sie bereits über Ihre Beschwerden?"
3. **I**nvitation: "Wie viel Detail wollen Sie wissen?"
4. **K**nowledge: Informationen in klaren, nicht-technical Begriffen
5. **E**mpathy: Emotionale Reaktion aufnehmen und validieren
6. **S**trategy: Nächste Schritte gemeinsam erarbeiten

#### Schwerhörige Nachrichten bei chron. Erkrankungen
- "Wir haben einige Befunde, die wir gemeinsam besprechen sollten"
- Nicht: "Das ist leider ernst" (bei chron. Erkrankungen oft unnötig alarmierend)
- Validierend: "Ihre Symptome sind real, auch wenn die Tests unauffällig sind"

### Überweisung & Diagnostik-Algorithmus

#### Bei chron. Fatigue + Schmerzen:
```
1. Hausarzt: Blutbild, CRP, TSH, fT4, BZ, HbA1c, Nieren-/Leberwerte, Elektrolyte,
   Vit D, B12, Ferritin, Urinstatus
   → Wenn unauffällig:
2. Überweisung Neurologie: POTS-Diagnostik (Tilt-Table, HRV-Analyse)
   → Wenn POTS nachgewiesen:
3. Überweisung Kardiologie: Ausschluss arrhythm. Ursachen, Echo
   → Wenn hEDS-Kriterien erfüllt:
4. Überweisung Humangenetik: hEDS-Gentesting (wenn verfügbar)
   → Wenn Mastzellsymptomatik:
5. Hautbiopsie: SFN (Intraepidermale Nervenfaser-Dichte)
   → Mastzellmediatoren: Tryptase, Histamin, Prostaglandin D2
```

#### ICD-10-GAM Kodierung (Priorität)
| Diagnose | ICD-10-GAM Code | Bemerkung |
|----------|-----------------|-----------|
| ME/CFS | G93.3 | Enzephalomyelitis myalgica |
| Fibromyalgie | M79.7 | Generalisierte Schmerzsyndrom |
| POTS | I95.1 | Orthostatische Hypotonie (Proxy) |
| hEDS | Q79.6 | Hyperextensibles Gewebe |
| MCAS/DMAE | D82.3 | Immundefizienz |
| SFN | G60.9 | Polyneuropathie, unspecified |
| IBS | K58.9 | Reizdarmsyndrom |

### Dokumentations-Standard (SOAP)
- **S**ubjektiv: Patientenbeschreibung der Symptome
- **O**bjektiv: Befunde, Vitalparameter, Labor
- **A**ssessment: Differentialdiagnose, Schweregrad
- **P**lan: Diagnostik, Therapie, Überweisung, Folgetermin

## Pitfalls
- **KEINE Diagnosen stellen** — nur "ärztliche Abklärung empfohlen" mit klinischem Kontext
- **Non-Thyroid Illness:** TSH kann bei chron. Erkrankungen sekundär verändert sein — nicht blind substituieren!
- **Vitamin D:** Korrelation ≠ Kausalität — Supplementierung hilft nicht bei jedem
- **ME/CFS-Fatigue ≠ Depression-Fatigue** — unterschiedliche Qualität
- **POTS ≠ Panikattacke** — physiologisch messbar, nicht psychosomatisch

## Related Skills
- `medizinischer-berater`: Klinische Kriterien, Komorbiditäten
- `kijan-health-module`: Health DB, ICD-10-GAM
- `pain-assessment-tools`: NRS, BPI, McGill
- `promis-measures`: PROMIS scoring
