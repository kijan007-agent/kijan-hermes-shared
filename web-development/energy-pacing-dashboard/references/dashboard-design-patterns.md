# Dashboard Design Patterns — Kijan Energy Pacing

## Dashboard Layout for Chronic Patients

### Primary Layout (420px+)
```
┌─────────────────────────────────────────────┐
│  TODAY (3 primary metrics)                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │Energy    │ │HRV       │ │Pain      │   │
│  │Envelope  │ │Trend     │ │Heatmap   │   │
│  │60% ✓    │ │▼ -12     │ │4/10 😐   │   │
│  └──────────┘ └──────────┘ └──────────┘   │
│                                             │
│  PACING (Activity vs. Envelope)             │
│  ┌─────────────────────────────────────┐   │
│  │ ██████████████░░░░░░░░ 65%         │   │
│  │ ──────────────── ─────────────     │   │
│  │     Ziel              Verbleibend    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  PEM RISK (Prediction)                      │
│  ┌─────────────────────────────────────┐   │
│  │ Risiko: MEDIUM ──────────────      │   │
│  │ HRV ↓ + Steps ↑ = Warning          │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  QUICK LOG (1-tap)                          │
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

## Energy Envelope Visualization

### Pattern: Circle/Ring, NOT Progress Bar
- **❌ BAD:** "Fill the bar" — implies control/ability to push
- **✅ GOOD:** "Your available energy envelope" — implies limitation

```
Energy Envelope Design:
- Circle/ring showing "% available" (NOT "% completed")
- Warning at <20% available (crash risk)
- "Banking" indicator: show stored energy
- Color: green (enough), yellow (tight), red (critical)
- Relativ to individual envelope, NOT absolute
```

## PEM Risk Score

### Formula
```
PEM Risk = f(
  HRV drop >15% under baseline,
  Steps >100% of envelope limit,
  Sleep quality <60% of individual norm,
  Time since last crash <48h
)

Score: 0-100
  0-20:   LOW ✅ — Normal continue
  21-50:  MEDIUM ⚠️ — Reduce envelope
  51-80:  HIGH 🚨 — Drastically reduce envelope
  81-100: CRITICAL ❌ — Crash likely
```

## Pain Heatmap Pattern

### Weekly View: 7 columns (Mon-Sun) × N rows (body regions)
- **Color:** intensity (warm → cool)
- **Opacity:** duration (more time = more opaque)
- **Border:** flare vs. baseline

```
Colors:
  0:   transparent (no pain)
  1-3: #FFD93D (yellow, mild)
  4-6: #FFA07A (orange, moderate)
  7-9: #FF6B6B (red, strong)
  10:  #C62828 (dark red, extreme)
```

## Correlation Matrix Pattern

### Garmin ↔ Symptom Correlations
```
         HRV   BB   Steps  Sleep  Stress
Energy    -0.7  -0.5  +0.3    +0.4    +0.6
Pain      +0.3  -0.2  +0.1    +0.2    +0.1
Fatigue   -0.6  -0.4  -0.2    +0.5    +0.5
Brain Fog -0.8  -0.3  +0.1    +0.3    +0.7

r < -0.5: Strong negative correlation
r > +0.5: Strong positive correlation
Visual: Color-coded matrix, significance as asterisks (p<0.05, p<0.01)
```

## Design Language

### Typography
- Min 16px body text (accessibility)
- Min 14px labels
- Max 60 chars/line (readability)
- Sans-serif (Roboto, Inter) — no serif fonts on small screens

### Dark Mode Colors (for ME/CFS)
| Element | Hex | Notes |
|---------|-----|-------|
| Background | #121212 | NOT #000000 — reduces eye strain |
| Text Primary | #E0E0E0 | NOT #FFFFFF — reduces contrast strain |
| Text Secondary | #A0A0A0 | |
| Primary | #5C9BFF | Calm blue, not neon |
| Success | #4CAF50 | Natural green |
| Warning | #FFB74D | Warm orange, not aggressive red |
| Danger | #F44336 | Use sparingly |
| Pain warm | #FF6B6B→#FFA07A→#FFD93D | NOT red-green for colorblind |

### Motion & Animation
- Max 200ms transitions (no long animations for brain fog)
- No auto-play videos (cognitive overload)
- No counting animations (unnecessary wait)
- Skeleton loading over spinners

### Responsive Breakpoints
| Breakpoint | Device | Priority |
|------------|--------|----------|
| < 360px | Small phones | Energy + Quick Log |
| 360-420px | Standard phones | Energy + Pacing + Pain |
| 420-768px | Large phones/tablets | Full layout |
| > 768px | Desktop | Full layout + Weekly Trend |

## Kijan Dashboard — What Doesn't Help

| Problem | Why It Doesn't Work | Alternative |
|---------|---------------------|-------------|
| Absolute numbers (steps, calories) | ME/CFS patient can't reach these targets → frustration | Relative values (% of envelope) |
| "Good/bad day" rating | Value-laden, creates guilt | "Envelope fulfilled / partially met" |
| Daily perfection | Unrealistic for chronic illness | Weekly consistency score |
| Complex charts | Brain fog: too much info | 3 primary metrics, expandable details |
| Gamification (streaks, badges) | Streak break = frustration | Envelope-aware milestones |

## Kijan Dashboard — What Helps

| Feature | Benefit for ME/CFS/Pain Patient |
|---------|--------------------------------|
| Energy envelope visualization | Makes energy limit visible |
| PEM risk score | Prediction instead of retrospection |
| Pacing feedback | Objective (not subjective feeling) |
| HRV baseline tracking | Early PEM warning |
| Pain-Garmin correlation | Identify triggers |
| Weekly consistency | Better than daily perfection |
| Supportive language | "Envelope check-in" not "day rating" |
