# Missing HAL Specifications — RESOLVED (2026-05-27)

## Status

Alle 4 fehlenden Spezifikationsdateien wurden erstellt und sind jetzt vorhanden:

| Datei | SPECS.md Referenz | Status |
|-------|-------------------|--------|
| `time-series/mobile-cache.md` | TASK-TS04: Mobile-Device Cache-Protokoll | ✅ Erstellt 2026-05-27 |
| `i18n/architecture.md` | TASK-I18N01: i18n-Schlüsselkonvention + JSON-Struktur | ✅ Erstellt 2026-05-27 |
| `i18n/key-conventions.md` | TASK-I18N02: Schlüsselkonventionen | ✅ Erstellt 2026-05-27 |
| `i18n/symptom-mapping.md` | Symptom-Namen i18n-Strategie | ✅ Erstellt 2026-05-27 |

## SPECS.md Status

- **SPECS.md** Status auf `✅ VOLLSTÄNDIG` aktualisiert (2026-05-27)
- Header-Format korrigiert (Mischung `>` und `|` in metadata-Zeilen → konsistent `>`)

## SPECS.md Konsistenz-Check (cron)

SPECS.md listet 32 Dateien (inkl. i18n/ und references/). Cron-Jobs:
1. Prüfe `find`-Ergebnis gegen SPECS.md Tabelle
2. Bei Abweichung: SPECS.md korrigieren ODER fehlende Datei erstellen
3. SPECS.md Header auf `✅ VOLLSTÄNDIG` setzen wenn alle Dateien vorhanden
