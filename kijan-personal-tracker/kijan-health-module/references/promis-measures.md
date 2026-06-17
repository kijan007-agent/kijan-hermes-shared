# PROMIS Pain Measures für Kijan

## PROMIS (Patient-Reported Outcomes Measurement Information System)
- **URL:** https://www.healthmeasures.net/explore-measurement-systems/promis
- **Status:** FDA/EMA anerkannter Goldstandard für patient-reported outcomes
- **Digital-first:** Adaptive Testing (CAT), validiert für mobile Geräte
- **Kosten:** Frei verfügbar für Forschung/Entwicklung

## PROMIS Pain Severity Short Form
- **Format:** 4-6 Items
- **Skala:** NRS 0-10 pro Item
- **Misst:** Schmerzintensität
- **Kijan-Integration:** Basis für Schmerz-Schwere-Tracking

## PROMIS Pain Interference Short Form
- **Format:** 6 Items
- **Misst:** Impact auf Alltagsfunktionen
- **Items:** Stimmung, Schlaf, Arbeit, körperliche Bewegung, soziale Interaktion, Genus des Lebens, Lebensfreude
- **Kijan-Integration:** **Core wöchentlicher Fragebogen** — direkt korrelierbar mit symptom_logs und medication_logs

## Scoring
- **Rohscores → T-Scores** via PyPROMIS oder offizielle Scoring-Manuals
- **T-Score Mean=50, SD=10** in general US population
- **Höhere Scores = mehr Beeinträchtigung**

## Python-Tools
- **PyPROMIS:** https://github.com/healthmeasures/PROMIS — Berechnung T-Scores
- **R-Pakete:** `promis` für statistische Analyse

## Kijan-Integration
1. BPI Pain Interference als wöchentlicher Template-Fragebogen
2. Promis Pain Severity als Grundlage für severity-coding
3. Korrelation von Pain Interference mit:
   - Body Battery Trends
   - Schlafqualität
   - Medication adherence
   - Symptom severity trends
