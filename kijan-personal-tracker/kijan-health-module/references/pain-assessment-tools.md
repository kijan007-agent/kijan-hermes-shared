# Schmerz-Evaluationsinstrumente (Pain Assessment Tools)

## Klinisch Validierte Standards für Kijan

### NRS (Numeric Rating Scale)
- **Typ:** 0-10 Skala ("Wie stark ist der Schmerz?")
- **Status:** Goldstandard für akute/chronische Schmerzen
- **Kijan-Integration:** **Core severity metric** — standard severity field in symptom_logs
- **UX:** Swipe/Glider für schnellen Input
- **Validierung:** NCCN Guidelines, FDA PRO guidance

### BPI (Brief Pain Inventory)
- **Typ:** Intensität (NRS) + Beeinträchtigung (Alltagsfunktionen)
- **Status:** Highly validated — Goldstandard für chronische Schmerzen
- **Kijan-Integration:** **Wöchentliches Deep-Dive-Template** — optionaler Fragebogen
- **Items:** Schmerzintensität (4x NRS), Schmerzbeeinträchtigung (7x Alltagsbereich: Stimmung, Schlaf, Arbeit, Bewegung, Interaktion, Genus, Lebensfreude)
- **Validierung:** MD Anderson Cancer Center

### McGill SF-MPQ-2 (Short-Form McGill Pain Questionnaire)
- **Typ:** Multidimensional (sensorisch, affektiv, evaluativ, Schmerzqualität)
- **Status:** Sehr detailliert, klinisch validiert
- **Kijan-Integration:** **Optional** — für klinische Berichte / Arztbesuche
- **UX:** Zu lang für täglichen Gebrauch; nur bei Bedarf verfügbar
- **Quelle:** https://www.hotspringsresearch.org/

### PainDETECT
- **Typ:** Screening für neuropathischen vs. nozizeptiven Schmerz
- **Status:** Unterscheidet Schmerztypen, diagnostisch relevant
- **Kijan-Integration:** **Optional** — als Filter für Therapie-Empfehlungen
- **UX:** Kurzes Screening-Formular, nicht tägliche Erfassung
- **Quelle:** https://www.paindetect.de/

## Empfehlung für Kijan
- **Core:** NRS 0-10 als default severity für Schmerzsymptome
- **Weekly:** BPI als optionaler wöchentlicher Fragebogen
- **Optional:** PainDETECT als Screening-Filter (neuropathisch vs. nozizeptiv)
- **Clinical:** McGill SF-MPQ-2 für PDF-Berichte (Arztbesuche)
