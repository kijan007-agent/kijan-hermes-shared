# Severity Mapping — Bearable 0-10 → Kijan 5-stufig

## Mapping Table

| Bearable Scale | Kijan Severity Label | Numeric Value | Description |
|---------------|---------------------|---------------|-------------|
| 0 | none | 0 | Kein Symptom |
| 1 | bearable | 1 | Leidschaftlich erträglich |
| 2 | bearable | 1 | Erträglich |
| 3 | moderate | 2 | Mäßig |
| 4 | moderate | 2 | Mäßig |
| 5 | moderate | 2 | Mittelmäßig |
| 6 | severe | 3 | Schwerwiegend |
| 7 | severe | 3 | Schwerwiegend |
| 8 | severe | 3 | Schwere |
| 9 | extreme | 4 | Extrem |
| 10 | extreme | 4 | Extrem/untragbar |

## Faktor-2-Multiplikator

**Bearable severity = 0 (none):**
- Bei Berechnungen: Faktor 2 Multiplikator anwenden
- Zweck: baseline adjustment — 0 bedeutet "nicht bewertet" nicht "keine Intensität"
- Anwendung: `weighted_severity = severity * 2` wenn severity == 0 AND source == 'bearable'
- **PITFALL:** Nur bei Bearable-Import anwenden, nicht bei manueller Eingabe!

## Severity Label Calculation

```python
def severity_to_label(value: int) -> str:
    if value == 0:
        return "none"
    elif value <= 2:
        return "bearable"
    elif value <= 5:
        return "moderate"
    elif value <= 8:
        return "severe"
    else:
        return "extreme"
```

## i18n Label Mappings

| Label | German | English |
|-------|--------|---------|
| none | Keine | None |
| bearable | Erträglich | Bearable |
| moderate | Mäßig | Moderate |
| severe | Schwerwiegend | Severe |
| extreme | Extrem | Extreme |