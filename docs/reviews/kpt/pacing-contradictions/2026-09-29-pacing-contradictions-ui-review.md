# UI/UX Review: Pacing-Seite — Widersprüchliche Energie-Zahlen

**Task:** t_pacing_contradictions
**Date:** 2026-09-29
**Author:** Ulrike "Uli" UX (ui-ux-designer)
**Status:** Review & Fix-Spezifikation abgeschlossen

---

## 1. Befund (Bug-Analyse)

### 1.1 Drei widersprüchliche Werte auf der Pacing-Seite

| Ort | Angezeigter Wert | Semantik | Problem |
|-----|-----------------|----------|---------|
| Forecast Hero (Zeile 58-62 pacing.html) | `8.1%` | Forecast Mean (Morgen) | Unbenanntes Zahlentripel: `8.1% / 6.3% — 9.8%` → Mean/Lower/Upper ohne Labels |
| Stats Card Energie (Zeile 77-82) | `6.1/30 · 115 spoons` | Ø 6.1 Einh./Tag über 30 Tage = 183 Total | Falsche Berechnung: `stats.energy_count` = Anzahl Tage (30), nicht Total-Summe |
| Stats Card Energie Sub (Zeile 82) | `115 spoons` | Sollte Total über alle Tage sein | 115 ≠ 6.1 × 6 (30 Tage); Wert ist `energy_avg × energy_count` — falsche Interpretation |

### 1.2 Konkrete Berechnungsfehler

**Stats-Energie-Bereich (Zeile 1643-1693 in personal.py):**
```python
# FALSCH (aktuell):
spoons_per_day = [int(checkins_by_date[k]["energy_level"]) for k in tracked_keys if int(checkins_by_date[k]["energy_level"]) > 0]
spent_spoons = sum(spoons_per_day)           # Summe aller Tageswerte
avg_spoons = round(spent_spoons / len(spoons_per_day), 1)  # Ø pro Tag
# → Stats-Template zeigt: avg_spoons / max_spoons · energy_count spoons
# → 115 spoons = avg_spoons × energy_count (falsch, energy_count = Tage, nicht Faktor)
```

**Stats-Rendering (pacing.html Zeile 77-82):**
```html
<!-- FALSCH (aktuell): -->
<p class="pacing-stat-value">{{ stats.energy_avg }}<span class="pacing-stat-unit">/{{ stats.max_spoons }}</span></p>
<p class="pacing-stat-sub">{{ stats.energy_count }} {{ t.get("pacing_spoons_label", "spoons") }}</p>
<!-- "6.1/30 · 115 spoons" = avg × count = FALSCH
     115 spoons suggeriert Total, ist aber avg × Tage-Anzahl = falscher Wert -->
```

**Forecast-Zahlentripel (pacing.html Zeile 58-62):**
```html
<!-- PROBLEM: Unbenanntes Zahlentripel -->
<p class="forecast-card__big">
  <strong>{{ _f.mean|default('—') }}<span class="forecast-card__unit">%</span></strong>
</p>
<p class="forecast-card__range">
  <span>{{ _f.lower|default('—') }}%</span> <span>—</span> <span>{{ _f.upper|default('—') }}%</span>
</p>
<!-- "8.1% / 6.3% — 9.8%" = Mean / Lower — Upper, aber ohne Labels!
     Nutzer kann nicht unterscheiden: ist 8.1% das Maximum? Minimum? Der Durchschnitt? -->
```

### 1.3 Korrekte Semantik (aus spoon_semantics_glossary.md)

| Feld | Bedeutung | Quelle |
|------|-----------|--------|
| `current_spoons` | Verbleibende Energie JETZT | `DailyCheckin.energy_level` |
| `energy_avg` (Ø) | Durchschnittliche Tagesenergie über Zeitraum | `mean(energy_vals)` |
| `energy_count` | Anzahl Tage mit Energie-Daten im Zeitraum | `len(energy_vals)` |
| `max_spoons` | Tagesbudget-Obergrenze | `device.total_units` (21 bei Kijan) |
| `forecast.mean` | Vorhergesagte Energie morgen in % | Forecast Engine |
| `forecast.lower/upper` | Konfidenzintervall der Vorhersage in % | Forecast Engine |

---

## 2. Fix-Spezifikation

### 2.1 Stats-Energie-Card — Neue Semantik

| Vorher | Nachher | Begründung |
|--------|---------|-----------|
| `6.1/30 · 115 spoons` | `Ø 6.1 Einh./Tag · 6 Tage mit Daten` | Korrekte Lesart: Ø pro Tag, Anzahl Tage |
| "spoons" Label | "Einh." (Einheiten) | Spoon-Begriff entfernen (laut spoon_ui_labels_spec.md) |
| `{{ stats.energy_count }} spoons` | `{{ stats.energy_count }} {{ t.get("days_with_data", "Tage mit Daten") }}` | Klartext-Label statt impliziter Bedeutung |

**Template-Fix (pacing.html Zeile 74-83):**
```html
<article class="pacing-stat-card">
  <h3 class="pacing-stat-title"><span>🔋</span> {{ t.get("pacing_energy_label", "Ø Energie/Tag") }}</h3>
  {% if stats.energy_avg is not none %}
  <p class="pacing-stat-value">
    <span class="pacing-stat-avg">{{ stats.energy_avg }}</span>
    <span class="pacing-stat-unit">/ {{ stats.max_spoons }} {{ t.get("pacing_unit_einh", "Einh.") }}</span>
  </p>
  {% else %}
  <p class="pacing-stat-value">—</p>
  {% endif %}
  <p class="pacing-stat-sub">
    {{ stats.energy_count }} {{ t.get("pacing_days_with_data", "Tage mit Daten") }}
  </p>
</article>
```

### 2.2 Forecast Hero — Labels für Zahlentripel

| Vorher | Nachher | Begründung |
|--------|---------|-----------|
| `8.1%` (ohne Label) | `Ø 8.1 %` | Mean explizit als Durchschnitt benennen |
| `6.3%` (ohne Label) | `Min 6.3 %` | Untergrenze als Minimum beschriften |
| `9.8%` (ohne Label) | `Max 9.8 %` | Obergrenze als Maximum beschriften |

**Template-Fix (pacing.html Zeile 58-63):**
```html
<p class="forecast-card__big">
  <strong>{{ t.get("forecast_label_mean", "Ø") }} {{ _f.mean|default('—') }}<span class="forecast-card__unit">%</span></strong>
</p>
<p class="forecast-card__range">
  <span>{{ t.get("forecast_label_min", "Min") }} {{ _f.lower|default('—') }}%</span>
  <span aria-hidden="true">—</span>
  <span>{{ t.get("forecast_label_max", "Max") }} {{ _f.upper|default('—') }}%</span>
</p>
```

### 2.3 i18n-Keys hinzufügen

In der Routing-Funktion (personal.py) müssen folgende neue i18n-Keys verfügbar sein:

```python
t.get("pacing_energy_label", "Ø Energie/Tag")
t.get("pacing_unit_einh", "Einh.")
t.get("pacing_days_with_data", "Tage mit Daten")
t.get("forecast_label_mean", "Ø")
t.get("forecast_label_min", "Min")
t.get("forecast_label_max", "Max")
```

### 2.4 Spoon-Begriff Eliminieren (laut spoon_ui_labels_spec.md)

Alle Vorkommen von "spoons" auf der Pacing-Seite:

| Ort | Vorher | Nachher |
|-----|--------|---------|
| pacing.html Zeile 82 | `pacing_spoons_label = "spoons"` | `pacing_days_with_data = "Tage mit Daten"` |
| pacing.html Zeile 115 | `forecast_week_label = "Next 7 days — predicted spoons"` | `forecast_week_label = "Next 7 days — predicted energy"` |
| pacing.html Zeile 116 | `forecast_week_title = "Next 7 Days — Predicted Spoons"` | `forecast_week_title = "Next 7 Days — Predicted Energy"` |

---

## 3. Akzeptanzkriterien

- [ ] Keine unbeschrifteten Prozent-Tripel auf der Pacing-Seite → Mean/Lower/Upper haben Labels (Ø/Min/Max)
- [ ] Stats-Energie-Card zeigt `Ø X/Y Einh. · N Tage mit Daten` (nicht `X/Y · X×N spoons`)
- [ ] Alle Werte haben Label + Einheit + konsistente Quelle
- [ ] Keine Spoon-Begriffe mehr auf der Pacing-Seite (laut spoon_ui_labels_spec.md)
- [ ] CSS-Klasse `.pacing-stat-sub` bekommt eindeutigen Text, der die Anzahl Tage erklärt

---

## 4. Änderungsübersicht (Backend Dev)

| Datei | Zeilen | Änderung |
|-------|--------|---------|
| `pacing.html` | 58-63 | Forecast Mean/Lower/Upper mit Ø/Min/Max Labels |
| `pacing.html` | 74-83 | Stats-Energie-Card: Labels + Einheiten korrigiert |
| `pacing.html` | 115-116 | "Spoons" → "Energy" in Forecast-Titel |
| `pacing.html` | 82 | `pacing_spoons_label` → `pacing_days_with_data` |
| `pacing.css` (ggf.) | — | `.forecast-card__range` mit Labels gestalten |

---

## 5. Betroffene Dateien (kanban-attachments)

- `pacing_contradictions_spec.md` — Original-Spezifikation
- `pacing_contradictions_mockup.html` — Visuelle Vorschau der Fixes
