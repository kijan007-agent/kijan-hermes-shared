# Visible Export-Spezifikation

## Datenquellen

### Visible-CSV-Export

```
Quelle: Visible App → Profile Tab → "Export data"
Format: CSV (Single dump file)
Umfang: "All data you've ever tracked"
Zweck: Datenexport für Forscher und Nutzer
```

### Visible Health Summary (PDF)

```
Quelle: Visible App → Profile Tab → "Download Health Summary"
Format: PDF (12-Monats-Übersicht)
Anforderung: Mindestens 30 Tage Daten
Zweck: Klinische Übersicht
```

### Visible Monthly Trend Report (PDF)

```
Quelle: Visible App → Profile Tab → "Download Monthly Trend Report"
Format: PDF (30-Tage vs 3-Monats-Vergleich)
Anforderung: Mindestens 90 Tage Daten
Zweck: Detaillierte Trend-Analyse
```

## CSV-Spalten-Schema (geschätzt)

Basierend auf den Visible Check-in-Formularen:

```csv
date,check_in_type,hrv,rhr,morning_stability_score,sleep_quality,energy,pain,fatigue,cognitive_difficulty,anxiety,mood,social_exertion,emotional_exertion,period,infection_type,crash,medication,notes,activity_type,activity_impact,pacepoints_used,pacepoints_remaining
```

## Spalten-Mapping zu Kijan

| Spalte | Typ | Beschreibung | Mapping zu Kijan |
|--------|-----|-------------|-----------------|
| date | DATE | Datumsangabe | → logged_at |
| check_in_type | ENUM | morning/evening/monthly | → source |
| hrv | FLOAT | Herzfrequenzvariabilität | → health_measurements.hrv |
| rhr | FLOAT | Ruhige Herzfrequenz | → health_measurements.heart_rate |
| morning_stability_score | INT | AI Score (0-100?) | → stability_scores.score |
| sleep_quality | INT | Nachtschlaf-Qualität (0-10) | → sleep_logs.quality |
| energy | INT | Energielevel (0-10) | → symptom_logs (energy symptom) |
| pain | INT | Schmerz (0-10) | → symptom_logs (pain) |
| fatigue | INT | Müdigkeit (0-10) | → symptom_logs (fatigue) |
| cognitive_difficulty | INT | Kognitiv (0-10) | → symptom_logs (cognitive) |
| anxiety | INT | Angst (0-10) | → symptom_logs (anxiety) |
| mood | CATEGORY | Gesamtstimmung | → mood_logs.overall_score |
| social_exertion | INT | Soziale Belastung (0-10) | → symptom_logs (social_exertion) |
| emotional_exertion | INT | Emotionale Belastung (0-10) | → symptom_logs (emotional_exertion) |
| period | BOOLEAN | Period vorhanden | → menstrual_logs |
| infection_type | VARCHAR | Infektionstyp | → infection_logs |
| crash | BOOLEAN | Crash erlebt | → crash_logs |
| medication | TEXT | Medikamente (comma-sep) | → medication_logs |
| notes | TEXT | Freitext | → symptom_logs.notes |
| activity_type | TEXT | Aktivität (comma-sep) | → activity_logs |
| activity_impact | TEXT | Impact (comma-sep) | → activity_impact_logs |
| pacepoints_used | INT | Verbraucht | → pacepoint_logs.used |
| pacepoints_remaining | INT | Verbleibend | → pacepoint_logs.remaining |

## Import-Pipeline

```
Phase 1: CSV-Par ... [truncated]