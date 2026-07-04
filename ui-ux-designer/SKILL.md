# UI/UX Designer

## Triggers
- User fragt nach Dashboard-Design, Visualisierung von Gesundheitsdaten
- Work on energy-pacing-dashboard, personal_dashboard.html, dashboard themes
- Task involves UI/UX, data visualization, health metrics display
- User wants to improve how health/activity data is presented

## Rolle
Senior UI/UX Designer mit Expertise in **Health Data Visualization**, **Energie-Pacing-Dashboards** und **barrierefreiem Design** für chronisch erkrankte Nutzer. Verbindet medizinisches Verständnis mit gestalterischer Exzellenz.

## Design-Prinzipien für Health Dashboards

### Chronische Erkrankung: Spezielle Anforderungen
| Faktor | Design-Konsequenz |
|--------|-------------------|
| **Brain Fog** (ME/CFS) | Klare Hierarchie, maximal 3 primäre Infos, reduzierte kognitive Last |
| **Fatigue** | Scanability, große Touch-Targets, wenig Scrollen |
| **Augenbelastung** | Hoher Kontrast, keine überladenen Charts, reduzierte Farbvielfalt |
| **Feinmotorik** | Große Targets (≥44px), generous spacing, keine kleinen Klickzonen |
| **Schlechte Tage** | Keine Panik-induzierenden Visualisierungen, supportive Sprache |
| **Wochenend-Flares** | Langfristige Trends statt täglicher Perfektion betonen |

### Gesundheitsdaten-Visualisierung: Golden Rules

#### Energy Level / Spoon Theory — Implementierung
- **Nicht als "Progress-Bar"** — das suggeriert "fülle dich auf"
- **Als "Envelope"-Visualisierung** — zeige begrenzte Kapazität ehrlich
- **Farbkodierung:** Grün (genug), Gelb (knapp), Rot (über)
- **Relativ zum Envelope**, nicht absolut

### HRV & Body Battery Trends
- **7-Tage Moving Average** für HRV (daily noise filtern)
- **Baseline-Shift erkennen:** HRV-Baseline verschiebt sich nach PEM
- **Body Battery Recovery Rate:** Wie schnell erholt sich BB über Nacht?
- **Keine Panik bei Einzelwerten** — Trends betonen

### Schmerz-Tracking Visualisierung
- **Heatmap (Tage x Körperregionen):** Flare-Muster erkennen
- **Nicht als "rote Zone"** — supportive Farben (warm → cool statt grün → rot)
- **Intensität als Opacity**, nicht als Farbe (farbblind-freundlich)
- **Wochen-Übersicht:** Weniger Detail, mehr Trend

### Dashboard-Layout für chron. Patienten
```
┌─────────────────────────────────────────────┐
│  TODAY (3 primäre Metrics)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │Energy    │ │HRV       │ │Pain      │   │
│  │Envelope  │ │Trend     │ │Heatmap   │   │
│  │60% ✓    │ │▼ -12     │ │4/10 😐   │   │
│  └──────────┘ └──────────┘ └──────────┘   │
│                                             │
│  PACING (Aktivität vs. Envelope)            │
│  ┌─────────────────────────────────────┐   │
│  │ ██████████████░░░░░░░░ 65%         │   │
│  │ ──────────────── ─────────────     │   │
│  │     Ziel              Verbleibend    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  PEM RISK (Vorhersage)                      │
│  ┌─────────────────────────────────────┐   │
│  │ Risiko: MEDIUM ──────────────      │   │
│  │ HRV ↓ + Schritte ↑ = Warnung        │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  QUICK LOG (1-Tipp)                         │
│  [Symptom + [Intensity + [Notes]    [Save] │
│                                             │
│  WEEKLY TREND (7d)                          │
│  ┌─────────────────────────────────────┐   │
│  │ Energy ████░░░░░░░░░░░░░            │   │
│  │ HRV    ████████░░░░░░░░░            │   │
│  │ Pain   ░░░████████░░░░░░░           │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Design-Sprache

### Typografie
- **Min. 16px** für Body-Text (Barrierefreiheit)
- **Min. 14px** für Labels
- **Max. 60 Zeichen/Zeile** (Lesbarkeit)
- **Sans-serif** (Roboto, Inter) — keine serifen Fonts auf kleinen Screens

### Farben (Dark Mode für ME/CFS)
- **Background:** #121212 (nicht #000000 — reduziert Eye-Strain)
- **Text Primary:** #E0E0E0 (nicht #FFFFFF — reduziert Kontrast-Strain)
- **Text Secondary:** #A0A0A0
- **Primary:** #5C9BFF (ruhiges Blau, nicht Neon)
- **Success:** #4CAF50 (natürliches Grün)
- **Warning:** #FFB74D (warmes Orange, nicht aggressives Rot)
- **Danger:** #F44336 (sparsam einsetzen)
- **Pain warm colors:** #FF6B6B → #FFA07A → #FFD93D (nicht Rot-Grün für Farbblinde)

### Motion & Animation
- **Max 200ms** Transitionen (keine langen Animationen bei Brain Fog)
- **Keine auto-play Videos** (kognitive Überlastung)
- **Keine Counting-Animationen** (unnötige Wartezeit)
- **Skeleton Loading** statt Spinner (bessere wahrgenommene Performance)

### Responsive Breakpoints
| Breakpoint | Geräte | Priorität |
|------------|--------|-----------|
| < 360px | Kleine Smartphones | Energy + Quick Log |
| 360-420px | Standard Smartphones | Energy + Pacing + Pain |
| 420-768px | Large Phones / Tablets | Voll-Layout |
| > 768px | Desktop | Voll-Layout + Weekly Trend |

## Daten-Visualisierung: Specific Patterns

### Energy Envelope Visualization
```
Das Energy Envelope ist KEIN Progress Bar!

❌ BAD: "Fülle den Balken auf" (impliziert Kontrolle)
✅ GOOD: "Dein verfügbarer Energiemantel" (impliziert Begrenzung)

Design:
- Envelope als Kreis/Ring, nicht als Rechteck
- Füllstand zeigt "% verfügbar", nicht "% abgeschlossen"
- Warnung bei <20% verfügbar (Crash-Risiko)
- "Banking"-Indikator: Zeige, wie viel du "gespeichert" hast
```

### PEM Risk Score
```
PEM-Risiko als Kombination aus:
1. HRV-Abfall (>15% unter Baseline)
2. Schritte über Envelope (>100% des Limits)
3. Schlafqualität (<60% der individuellen Norm)
4. Zeit seit letztem Crash (<48h)

Score: 0-100
  0-20: LOW ✅ - Normal weiter
  21-50: MEDIUM ⚠️ - Envelope reduzieren
  51-80: HIGH 🚨 - Envelope stark reduzieren
  81-100: CRITICAL ❌ - Crash wahrscheinlich
```

### Pain Heatmap Pattern
```
Wochenansicht: 7 Spalten (Mo-So) × N Reihen (Körperregionen)

Jede Zelle:
  Farbe = Intensität (warm → cool)
  Opacity = Dauer (mehr Zeit = deckender)
  Border = Flare vs. baseline

Farben:
  0: transparent (kein Schmerz)
  1-3: #FFD93D (gelb, mild)
  4-6: #FFA07A (orange, moderat)
  7-9: #FF6B6B (rot, stark)
  10: #C62828 (dunkelrot, extrem)
```

### Correlation Matrix
```
Garmin ↔ Symptom Korrelationen:

         HRV   BB   Schritte  Schlaf  Stress
Energy    -0.7  -0.5  +0.3    +0.4    +0.6
Pain      +0.3  -0.2  +0.1    +0.2    +0.1
Fatigue   -0.6  -0.4  -0.2    +0.5    +0.5
Brain Fog -0.8  -0.3  +0.1    +0.3    +0.7

r < -0.5: Starke negative Korrelation
r > +0.5: Starke positive Korrelation

Visual: Farbige Matrix, Signifikanz als Sterne (p<0.05, p<0.01)
```

## Kijan Dashboard: Aktuelle Probleme & Lösungsansätze

### Was NICHT hilft (aktuelle Probleme)
| Problem | Warum es nicht hilft | Alternative |
|---------|---------------------|-------------|
| Absolute Zahlen (Schritte, Kalorien) | ME/CFS-Patient kann diese Ziele nicht erreichen → Frustration | Relative Werte (% vom Envelope) |
| "Gute/Schlechte Tage" Bewertung | Wertend, erzeugt Schuldgefühle | "Erfüllter/partially met Envelope" |
| Tägliche Perfektion | Unrealistisch für chron. Erkrankung | Weekly Consistency Score |
| Komplexe Charts | Brain Fog: zu viel Information | 3 primäre Metrics, Expandable Details |
| Gamification (Streaks, Badges) | Streak-Bruch = Frustration | Envelope-Aware Milestones |

### Was HILFT (empfohlen)
| Feature | Nutzen für ME/CFS/Pain-Patient |
|---------|-------------------------------|
| **Envelope-Visualisierung** | Macht Energie-Grenze sichtbar |
| **PEM-Risiko-Score** | Vorhersage statt Nachschau |
| **Pacing-Feedback** | Objektive Rückmeldung (nicht subjektives Gefühl) |
| **HRV-Baseline-Tracking** | Early Warning für PEM |
| **Pain-Garmin Correlation** | Trigger identifizieren |
| **Weekly Consistency** | Besser als tägliche Perfektion |
| **Supportive Language** | "Envelope-Check-in" statt "Day Rating" |

## Pitfalls
- **NIEMALS** Gamification für chron. Erkrankung (Streaks bei ME/CFS = Frustration)
- **Keine absoluten Fitness-Ziele** — relative Werte (% Envelope)
- **Keine "Schlechte Tage" Bewertung** — supportive Sprache
- **Keine überladenen Charts** — Brain Fog beachten
- **Keine roto-grüne Farbkodierung** — Farbblindheit + Schmerz-Skala
- **Keine Panik-Indikatoren** — supportive statt alarmierend

## Related Skills
- `energy-pacing-dashboard`: Energy pacing patterns, dashboard implementation
- `kijanpersonal-tracker`: Project structure, TASKS patterns
- `popular-web-designs`: Design systems, Stripe/Linear/Vercel patterns
- `sketch`: Throwaway HTML mockups