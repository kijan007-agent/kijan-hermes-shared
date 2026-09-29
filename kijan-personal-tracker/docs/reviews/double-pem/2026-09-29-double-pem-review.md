# UI/UX Review: Double PEM Screen — KijanPersonalTracker

**Date:** 2026-09-29
**Reviewer:** Ulrike "Uli" UX (ui-ux-designer)
**Task:** t_double_pem
**Status:** Complete

## Reviewed Files

| File | Path |
|------|------|
| Variant 1 — Calm Side-by-Side | `docs/reviews/double-pem/variant_001_calm_side_by_side.html` |
| Variant 2 — Stacked Diff | `docs/reviews/double-pem/variant_002_stacked_diff.html` |
| Variant 3 — Dashboard Card | `docs/reviews/double-pem/variant_003_dashboard_card.html` |
| Design Rationale | `docs/reviews/double-pem/DESIGN.md` |

## Review Findings

### F1 — All Variants: Colour + Text Pairing (PASS)
All three variants pair every colour-coded state with a German word label. No state is communicated by colour alone. This satisfies Brain-Fog Accessibility Rule from the health-data-design principles.

### F2 — Variant 1: Envelope-First Landing (PASS)
The top card leads with "Im Rahmen" + green envelope confirmation. This answers the user's primary question ("Am I within my limits?") before showing any risk data. Cognitive load is minimal. No numerical deltas — relies on colour and copy. Best default for daily check-in.

### F3 — Variant 2: Explicit Delta Pills (PASS with note)
A/B delta pills (↑87%, ↓12%) are legible and scannable. The risk-bar gradient stripe is a clean variation from a ring. Period tabs (Tag / Woche / Aktivität) enable flexible comparison modes. Risk: numbers can increase anxiety on bad days — mitigate with "Erholung wahrscheinlich" copy in recovery zone.

### F4 — Variant 3: Insight-Led Pattern Card (CONDITIONAL PASS)
The insight card ("mehr Schritte am Vortag korrelieren mit HRV-Abfall") surfaces a pattern proactively. This is valuable for periodic review but could feel judgemental during a crash. Recommend: insight cards should be opt-in or behind a "Muster erkennen" tap, not surfaced on load.

### F5 — All Variants: Touch Targets (PASS)
Period chips are 40 px high (meets 44 px guideline closely); primary button is 52 px. Fine-motor considerations are addressed.

### F6 — Variant 1 & 2: Language Tone (PASS)
"Leicht erhöht", "Pause einplanen", "Im Rahmen" — all supportive, non-alarmist. No "Warning", "Alert", or "Crash" copy anywhere.

### F7 — Variant 2: Period Tab Labels (MINOR ISSUE)
Period tabs use abbreviated labels that may be ambiguous: "Tag", "Woche", "Aktivität". Recommend adding a sub-label or tooltip explaining what "Aktivität" means in context (activity-triggered PEM window).

## Recommendations

1. **Use Variant 1 as the default landing view** — envelope-first, low cognitive load, calm.
2. **Use Variant 2 when user taps "mehr Details"** or opens week/activity comparison.
3. **Use Variant 3 as optional "Muster" tab** — opt-in only, never surfaced automatically.
4. **Recovery ETA threshold**: Only show when confidence ≥ 60% (per spec). Add a note in the code review checklist.
5. **Animation**: Recommend 200 ms cross-fade between A/B periods; no parallax or slide transitions.

## Shared Design Decisions (All Variants)

- Background `#121212`, text `#E0E0E0` / `#A0A0A0`, primary `#5C9BFF`
- Risk palette: LOW `#4CAF50`, MEDIUM `#FFB74D`, HIGH `#FF6B6B`, CRITICAL `#C62828`
- All colour paired with German text label
- Body min 16 px, values 20 px bold, labels 12 px uppercase with letter-spacing
- Touch targets ≥ 44 px
- No gamification (no streaks, no score-as-reward copy)

## Out of Scope

- Production React/Native implementation
- Data-fetching and aggregation logic
- Animation implementation

## Verdict

**Approved** with conditions: Variant 3 insight cards should be gated behind user opt-in or a dedicated "Muster" tab. All three variants are structurally sound and satisfy the health-data-design principles.
