# Double PEM Screen — Design Rationale

**Task:** t_double_pem · **Role:** ui-ux-designer · **Target:** KijanPersonalTracker mobile

## Goal
Show two PEM-relevant time periods side-by-side so the user recognises patterns without relying on memory (brain fog). Surface context automatically; never dramatise.

## Design stance: Honest Envelope, No Alarm
- PEM is a fact of ME/CFS, not a failure. UI acknowledges it calmly.
- Colours are muted (no saturated reds). Critical states use deep red `#C62828`, never alone.
- Language is supportive: "Leicht erhöht" not "Warning". "Pause einplanen" not "Crash Alert".
- All controls ≥ 44 px hit target. Period chips 40 px high.

## Variant comparison
| # | File | Strength | Trade-off |
|---|------|----------|-----------|
| 1 | variant_001_calm_side_by_side.html | Minimal cognitive load, envelope-first | Less explicit delta info |
| 2 | variant_002_stacked_diff.html | Explicit A↔B deltas, scannable | More numbers; risk of overload |
| 3 | variant_003_dashboard_card.html | Insight-led, pattern highlight | Busier, more visual weight |

## Variant 1 — Calm Side-by-Side
Energie-bar + envelope-status on top, then PEM-risk card, then symptoms row. The first card answers "bin ich im Rahmen?" — the user's primary question. No numerical deltas shown; relies on colour and copy. Best for daily check-in, low cognitive load. Insight is a single supporting line, never a verdict.

## Variant 2 — Stacked Diff
Explicit A↔B delta pills on every metric (↑87%, ↓12%). Period tabs (Tag / Woche / Aktivität) at the top let the user switch the comparison mode. Risk-bar uses a gradient stripe instead of a ring. Best when the user is investigating a pattern ("warum gestern schlechter?") — gives them the numbers without forcing them to compare in their head.

## Variant 3 — Dashboard Card
Two mini-cards (A / B) at the top so the user can see both states simultaneously without scrolling. A larger central card shows the current PEM-score with a ring visual, then a coloured insight card surfaces the pattern itself ("mehr Schritte am Vortag korrelieren mit HRV-Abfall"). Best for the periodic review moment. Highest information density — risk of overload on bad days.

## Recommendation
Use **Variant 1** as the default landing view (envelope-first, calm).
Use **Variant 2** when the user taps "mehr Details" or opens a week/activity comparison.
Use **Variant 3** as the optional "Pattern" view from a tab, never as the default — insight cards should be opt-in because surfacing patterns can feel judgemental when the user is in a crash.

## Shared decisions across all variants
- Background `#121212`, text `#E0E0E0`/`#A0A0A0`, primary `#5C9BFF`
- Risk palette: LOW `#4CAF50`, MEDIUM `#FFB74D`, HIGH `#FF6B6B`, CRITICAL `#C62828`
- PEM-risk dot is always prefixed by a plain German word ("Leicht erhöht"), never a colour-only signal
- Symptom scale 0–10 shown as `n/10` and as filled dots (dot count 0–6 for glanceable scan)
- Body 16 px min, values 20 px bold, labels 12 px uppercase with letter-spacing
- Touch targets ≥ 44 px, period chips 40 px high
- No gamification: no streaks, no scores-as-rewards, no "great job" copy
- Recovery ETA shown only when confidence ≥ 60% (avoid false precision)

## Accessibility
- All colour is paired with text or iconography (colour-blind safe)
- Critical state never conveyed by red alone — always with the word + a glyph
- Dark mode base; high contrast 7:1 for primary text on `#121212`
- Interactive elements have visible focus rings (not shown in mockup; spec note)

## Out of scope (this task)
- Production React/Native component implementation
- Data-fetching and aggregation logic (handled by health module)
- Animation transitions between A/B (recommend 200 ms cross-fade only, no parallax)

## Files in this sketch
- SPEC.md — original spec from prior task
- DESIGN.md — this rationale
- variant_001_calm_side_by_side.html
- variant_002_stacked_diff.html
- variant_003_dashboard_card.html

