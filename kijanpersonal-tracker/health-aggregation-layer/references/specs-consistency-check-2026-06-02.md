# SPECS.md Manifest Consistency Check — 2026-06-02

## Problem
SPECS.md Abschnitt 4 referenziert 26 Dateien, Disk hat 31.
5 Dateien nach Manifest-Erstellung hinzugefügt:

| Datei | Grund |
|-------|-------|
| `comparative/bearable-vs-visible.md` | Komparative Analyse (Visible vs Bearable) |
| `comparative/research-summary.md` | MakeVisible.com Research |
| `import/visible-export-spec.md` | Visible CSV Export-Spezifikation |
| `references/bearable-severity.md` | Bearable Severity-Skala Referenz |
| `references/nrs-tools.md` | NRS Tools Referenz |

## Status
- SPECS.md Abschnitt 4 ist **veraltet**
- Alle 31 Dateien sind valid und gehören zur Spezifikation
- SPECS.md selbst ist aktuell (2026-05-27)

## Empfohlene Aktion
SPECS.md Abschnitt 4 um `comparative/` und `references/` erweitern.