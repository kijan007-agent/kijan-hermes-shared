# Komparative Analyse: Bearable vs. Visible

## Quelle
- MakeVisible.com Hauptwebsite, Blog, About (2026-05-20 gescrappt)
- Bearable-App-Assessment (kpt-doc/_research/bearable-app-assessment.md)
- GitHub Bearable Exporter Projekte — CSV-Format-Spezifikationen

## Produktübersicht

| Merkmal | Bearable | Visible |
|---------|----------|---------|
| Plattform | iOS/Android App | iOS/Android App + **physisches Wearable (Band 2.0)** |
| Zielgruppe | Alle chronischen Erkrankungen | Long Covid, ME/CFS, Fibromyalgie, POTS, EDS |
| Hardware | Keine | **Polar Heart-Rate-Armband** (sponsored) |
| Preismodell | Einmalig/Abonnement | **Hardware-Kosten + monatliches Membership** |
| Forschung | Keine organisierte | **PLRC-Partnerschaft**, 4+ aktive Studien |
| User | 100k+ | ~60.000 tägliche Nutzer |
| Export | CSV-Export | CSV-Export + **PDF Health Summary (12mo)** + **PDF Monthly Trend Report** |
| API | Keine öffentliche API | Keine öffentliche API |
| HSA/FSA | Nein | **Ja** (reimbursement eligible) |

## Visible Check-in-Struktur

### Morning Check-in (täglich)
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| HRV (gemessen via Band) | Numerisch | Kontinuierliche HRV-Messung |
| Resting Heart Rate | Numerisch | Automatisch aus Band-Daten |
| Morning Stability Score | 0-10 | **AI-gestützter Score** (Crash-Suszeptibilität) |
| Sleep quality | 0-10 | Selbstberichtete Nachtschlaf-Qualität |
| Energy | 0-10 | Energielevel beim Aufwachen |
| Notes | Freitext | Optionale Morgentagebuch-Einträge |
| Medication | Multiple | Welche Medikamente eingenommen |
| Symptom severity | 0-10 | Alle aktiven Symptome bewerten |
| Period | Boolean | Period vorhanden? |
| Infection | Kategorie | Erkältung, Grippe, COVID, etc. |

### Evening Check-in (täglich)
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| Pain | 0-10 | Schmerzlevel |
| Fatigue | 0-10 | Müdigkeit |
| Cognitive difficulty | 0-10 | Kognitive Schwierigkeiten |
| Anxiety | 0-10 | Angstlevel |
| Mood | Kategorie | Gesamtstimmung |
| Social exertion | 0-10 | Soziale Anstrengung |
| Emotional exertion | 0-10 | Emotionale Anstrengung |
| Activity impact | Multi-select | Welche Aktivitäten heute (mit Impact) |
| Crash | Boolean | Crash erlebt? |
| Notes | Freitext | Optionale Abendeintragungen |

### Monthly Check-in (alle ~30 Tage)
| Feld | Typ | Beschreibung |
|------|-----|-------------|
| FUNCAP27 | 27 Fragen | **Functional Capacity** Score (0-6) |
| Symptom overview | Alle Symptome | Langzeit-Symptom-Übersicht |
| Medication review | Alle Medikamente | Wirkung/Wirkungsänderung |
| Notes | Freitext | Monatliche Reflexion |

## Gap-Analyse: Visible Unique Features

| Feature | Bearable | Visible | Unser Modell |
|---------|----------|---------|-------------|
| PacePoints | ❌ | ✅ Energy Budgeting | **NEU: pacepoint_logs** |
| Continuous HRV | ❌ | ✅ Kontinuierlich | **NEU: hrv_continuous_logs** |
| Crash-Tracking | ❌ | ✅ PEM-episodes | **NEU: crash_logs** |
| Infection tracking | Teilweise | ✅ Mit Typ-Klassifikation | **NEU: infection_logs** |
| FUNCAP27 | ❌ | ✅ 27-Fragen-Fragebogen | **NEU: funcap27_sessions** |
| Breathing exercises | ❌ | ✅ HRV-Biofeedback | **NEU: breathing_sessions** |
| Morning Stability Score | ❌ | ✅ AI-predicted | **NEU: stability_scores** |
| Activity impact | ❌ | ✅ Which activities worsened symptoms | **NEU: activity_impact_logs** |
| Health Summary PDF | ❌ | ✅ 12-Monats-Übersicht | **NEU: health_summary_reports** |
| Monthly Trend Report | ❌ | ✅ 30d vs 3mo Vergleich | **NEU: trend_report_pdf** |
| Research data sharing | ❌ | ✅ Anonymisiert an PLRC | **NEU: research_opt_in** |
| Nervous system recovery | ❌ | ✅ Tools | **NEU: recovery_sessions** |

## Wettbewerbsvorteil Kijan über Visible

| Merkmal | Visible | Kijan (HAL) |
|---------|---------|-------------|
| Datenquellen | Nur Visible Band 2.0 | **Garmin + Bearable + manuell** |
| MedGemma KI-Berichte | ❌ PDF-Reports | ✅ **KI-generierte KI-Berichte** |
| Trend-Erkennung | Visuell | ✅ **Automatische OLS Regression** |
| Korrelations-Analyse | ❌ | ✅ **Symptom ↔ Faktor Korrelation** |
| Open Source | ❌ | ✅ |
| Lokalisierung | ❌ | ✅ **i18n für alle Sprachen** |
| Custom Symptom-Definition | ✅ | ✅ |
| UnknownSymptomDetector | ❌ | ✅ **Auto-Erkennung + Erweiterung** |
| Datenhoheit | ✅ (Daten bei Visible) | ✅ **(Daten beim Nutzer)** |
| Forschungsexport | ✅ (nur an PLRC) | ✅ **(beliebiger Export)** |
| Kosten | ~$30-40/mo + Band | ✅ **Kostenlos** |

## Zusammenfassung

### Was Visible besser macht als Bearable:
1. Physiologische Daten via Wearable (HRV kontinuiierlich)
2. Crash/PEM-Tracking mit Trigger-Analyse
3. Energy Budgeting (PacePoints) — einzigartiges Feature
4. Stability Score — AI-gestützte Crash-Vorhersage
5. Funktionen für ME/CFS speziell (FUNCAP27, Infection tracking)
6. Research Integration — direkte Studien-Enrollment
7. PDF Reports für Kliniker (Health Summary, Monthly Trend)
8. Breathing exercises mit HRV-Biofeedback

### Was Kijan besser macht als Visible:
1. Multi-Source (Garmin + Bearable + manuell) — Visible nur Band
2. MedGemma KI — tiefere Analyse als PDF-Reports
3. Automatisierte Korrelation — Visible nur visuelle Trends
4. Open Source + Datenhoheit
5. i18n — Visible nur Englisch
6. Kostenlos — Visible teuer
7. UnknownSymptomDetector — automatische Model-Erweiterung
8. Flexible Datenquellen — keine Hardware-Abhängigkeit
