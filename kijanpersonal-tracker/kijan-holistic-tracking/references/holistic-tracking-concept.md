# Ganzheitliches Tracking-Konzept (2026-05-13)

## Unified Dashboard Layout

```
┌──────────────────────────────────────────────────────┐
│ Kijan  |  Mittwoch, 13. Mai  |  [Avatar]            │
│──────────────────────────────────────────────────────│
│  [Dashboard] [Aktivitäten] [Verlauf] [Gesundheit]   │
│──────────────────────────────────────────────────────│
│                                                      │
│  🥄 ENERGY ENVELOPE                                  │
│  ┌──────────┐  ┌─────────┐  ┌─────────┐             │
│  │ Ring 60% │  │ PEM: ⚠️│  │ Hülle:  │             │
│  │=15 Spoons│  │ MEDIUM  │  │ 40% erfüllt│           │
│  └──────────┘  └─────────┘  └─────────┘             │
│                                                      │
│  📊 TAG IM ÜBERBLICK (NEU)                          │
│  ┌─────────────────────────────────────────────┐    │
│  │ [Burndown-Chart mit Symptom-Overlays]       │    │
│  │ [Medikamenten-Zeitstrich darunter]          │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  📋 HEUTIGE AKTIVITÄTEN + SPOONS                   │
│  ┌─────────────────────────────────────────────┐    │
│  │ 🚿 Morgenroutine     │█░░░░░░░░░  2 Spoons  │    │
│  │ 🧠 Brain Fog         │█░░░░░░░░░  0.5       │    │
│  │ 🚶 Spaziergang       │░░░░░░░░░░  —         │    │
│  │ 🍳 Kochen            │░░░░░░░░░░  —         │    │
│  │ 💻 Arbeit            │░░░░░░░░░░  —         │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  🤒 SYMPTOM-ÜBERSICHT HEUTE                         │
│  ┌─────────────────────────────────────────────┐    │
│  │ Schmerz:    4/10  🔥  seit 08:30            │    │
│  │ Müdigkeit:  7/10  😴  seit Aufstehen         │    │
│  │ Brain Fog:  5/10  🧠  seit 14:00            │    │
│  │ Übelkeit:   1/10  🤢  kurz 12:15             │    │
│  │ [+ Symptom hinzufügen]                      │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  💊 MEDIKAMENTE HEUTE                               │
│  ┌─────────────────────────────────────────────┐    │
│  │ ☑️ Metformin 500mg  07:00 ✓ 2x               │    │
│  │ ☐ Vitamin D 2000IE  12:00  ⏰ fällig         │    │
│  │ ☐ Ibuprofen 400mg   14:00  🔔 alert          │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  📈 WOCHENVERLAUF                                   │
│  ┌─────────────────────────────────────────────┐    │
│  │ Energie   ████████░░░░░░░░  65%            │    │
│  │ HRV       ██████░░░░░░░░░░  55%            │    │
│  │ Schmerz   ████░░░░░░░░░░░░  35% (↑ besser) │    │
│  │ Schlaf    ██████████░░░░░░  70%            │    │
│  │ Hülle     ██████░░░░░░░░░░  50%            │    │
│  │ Symptom-  ████████░░░░░░░░  60% (weniger)  │    │
│  │ Adhärenz  ████████████░░░░  85%            │    │
│  └─────────────────────────────────────────────┘    │
│                                                      │
│  QUICK CHECK-IN                                     │
│  Energie: [▬▬▬▬▬▬▬▬▬▬░░] 15 Spoons  [Speichern]  │
│──────────────────────────────────────────────────────│
│  🏠  📊  📈  🧬  ⚙️                               │
│  Dash  Aktiv  Verh  Gesund Einstell                  │
└──────────────────────────────────────────────────────┘
```

## Tracking Categories

### A. Energy Pacing
| Feature | Watch | Dashboard | Mobile |
|---------|-------|-----------|--------|
| Gesamtspoons/Tag | ✅ | ✅ | ✅ |
| Spoon-Burndown heute | ✅ | ✅ | ✅ |
| Spoon-Verbrauch pro Aktivität | ✅ | ✅ | ✅ |
| Pacing-Warnung | ✅ Vib | ✅ Banner | ✅ Push |
| PEM-Risiko-Score | ❌ | ✅ | ✅ |

### B. Symptomtracking
| Feature | Watch | Dashboard | Mobile |
|---------|-------|-----------|--------|
| Symptom-Auswahl (NRS 0-10) | ✅ | ✅ | ✅ |
| Symptom-Kategorien | ❌ | ✅ Custom | ✅ + ICD-10 |
| Body-Map (Schmerz) | ❌ | ✅ SVG | ✅ Touch |
| Symptom-Trend | ❌ | ✅ | ✅ |
| Korrelation mit Garmin | ❌ | ✅ Pearson r | ✅ |

### C. Medikamententracking
| Feature | Watch | Dashboard | Mobile |
|---------|-------|-----------|--------|
| Medikamenten-Plan | ❌ | ✅ | ✅ Sync |
| Einnahme-Log | ❌ | ✅ Manuell | ✅ Push |
| Adhärenz (on_time/late/missed) | ❌ | ✅ % | ✅ Badge |
| Erinnerung/Alarm | ❌ | ❌ | ✅ Primär |

### D. Garmin Health Metrics (Auto)
| Feature | Watch | Dashboard | Mobile |
|---------|-------|-----------|--------|
| HRV RMSSD | ✅ | ✅ | ✅ |
| Body Battery | ✅ | ✅ | ✅ |
| Stress Score | ✅ | ✅ | ✅ |
| Schlaf | ✅ | ✅ | ✅ |
| Steps/Active | ✅ | ✅ | ✅ |
| SpO2 | ✅ | ✅ | ✅ |

## Cold-Start Spoon Strategy
- Days 1-3: Community median for activity type
- Days 4-7: User-adjustable ("Mehr/weniger spoons?")
- Day 8+: `new_spoons = old_spoons + (actual_used - spent) * alpha`
