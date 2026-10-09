# KPT Mobile · Quick-Log Workflow — Design Spec

Task: t_f91cdd18 · Profile: ui-ux-designer
Deliverable: Home (Daily Log) screen, focusing on MoodQuickButton + SymptomQuickAdd, optimized for a rapid "Quick-Log UX".

## Context & Principles
- Target user group: people with ME/CFS / chronic fatigue, often brain-fog and fine-motor strain.
- No gamification, no streaks, no progress bars. Gentle, supportive, low-effort language.
- Big tap targets (≥44pt / 44px), high contrast, minimal steps, no required typing.
- The envelope model informs mood capture (a range, not a score).

## Component specs

### MoodQuickButton — unified face scale (F-06 binding standard)
The single canonical mood scale across all variants (A, B, C) **and** the About-You area is the 5-point face band:

| Code | Glyph | Label  | Meaning                       |
|------|-------|--------|-------------------------------|
| 1    | 😣    | rough  | very low energy / worst day   |
| 2    | 😕    | low    | below baseline                |
| 3    | 😐    | ok     | baseline / nothing remarkable |
| 4    | 🙂    | good   | above baseline                |
| 5    | 😊    | great  | very good day                 |

- **No numbers shown to the user.** Codes are only the wire format (`{ mood: 1..5 }`).
- **No progress-bar / no streak / no score** — these are envelope picks, not measurements.
- ⚡ / 😴 / 😌 / ⚡ Fine are **deprecated** and must not appear in any variant.
- All mood buttons must carry `role="radio"` inside a `role="radiogroup"` parent with an accessible name.
- Selection is single-tap (auto-saves) on the Home screen (variant A). Variant B selects then gates "Next". Variant C offers mood at the top of the mini-sheet.
- Every mood selection persists locally (key: `kpt.quicklog.mood` on A, `kpt.quicklog.guided` on B, `kpt.quicklog.sheet` on C) **and** fires a `POST /api/quick-log/mood` (currently a `// TODO(api)` no-op; see t_f91cdd18-followup-api).

### MoodQuickButton (Home)
- Big, single primary button on the Home screen (~1 tap to log mood).
- Tap opens a 5-point envelope (Very low → Very well) rendered as a soft horizontal band — NOT a progress bar, no numbers.
- One tap on a point closes and writes the record; toast "Logged, thank you."
- Per variant (below) the amount of guidance differs.

### SymptomQuickAdd (Home)
- Compact "+" chip / sheet trigger next to mood on Home.
- Opens a bottom sheet: pick symptom chips, pick strength (4-step none/mild/medium/severe), optional body location, optional note.
- Save logs instantly, no confirmation screen.

## Three variants (each a self-contained HTML)

### Variant A — One-Tap Speed (variant-a.html)
- Fastest path. Envelope band directly on Home, tap = logged.
- Symptom sheet 3 controls (pick / strength / save), no optional fields forced.
- Best for high brain-fog days / low spoons.

### Variant B — Guided Check (variant-b.html)
- Step-by-step wizard: 1) energy level, 2) symptom pick. One screen per question.
- Progress dots (not bar). "Skip" + "Next" bottom nav. Supportive copy.
- Best for users who want a gentle nudge and structure, mid-energy days.

### Variant C — Mini Sheet (variant-c.html)
- Full bottom-sheet form for symptom with all controls visible at once.
- Strength via 4 symbolic levels (○◔◑●), body map as circle chips, optional note.
- Best power path for detailed logging when user has the energy.

## Color tokens (shared)
- primary #2B6A4F · primary-soft #D9EDE4 · primary-deep #1B4332
- accent #E07A5F · accent-soft #DCEBEF; bg #FAFAF8 / #F6F1E7 / #EEEBE4; ink #2C3E50; muted #5D6D7E

## Interaction contract (binding for engineering)

### Skip vs Next on guided variants (F-03)
| Button | Behaviour                                                                 | Toast |
|--------|----------------------------------------------------------------------------|-------|
| Skip   | Discard current question's selection without persisting, advance silently | none  |
| Next   | Persist current answer to `localStorage` **and** to the API (TODO), advance | yes   |

- **Next is disabled** until a required selection exists on the current step (energy level on step 1; no required selection on step 2 / symptom list).
- Skipping never produces a confirmation toast — discarded answers should feel quiet.

### Mood selection (F-04)
- Click on a `.mood` button toggles selection (`role="radio"`, single-select inside a `radiogroup`).
- A second click on the same button clears the selection (defensive against misclicks).
- Selection is announced via `aria-live="polite"` for assistive-tech users.
- The selection immediately:
  1. Marks the button `.sel` and sets `aria-checked="true"`.
  2. Updates the "Logged" status strip on Home.
  3. Writes to `localStorage` (key `kpt.quicklog.mood` on A; on B/C each variant's state key applies).
  4. Fires `POST /api/quick-log/mood` with `{ mood: <1..5>, at: <ISO8601> }`. Endpoint is `// TODO(api)` — see t_f91cdd18-followup-api. While the backend is missing the call is a no-op; the UI is fully functional against `localStorage`.

### About-You area
- Same scale, same accessibility pattern, same wire envelope. Specifically: `role="radiogroup"` with an accessible name, 5 buttons with `data-mood` and `aria-label`, no numbers, no progress bar.

## Acceptance criteria coverage
- [x] Main dashboard (Home Daily Log) designed in all 3 variants
- [x] Quick-entry interactions defined (mood one-tap, symptom sheet)
- [x] Accessibility: ≥44px targets, contrast tokens, no required typing
- [x] Spec + working HTML deliverable attached
- [x] **F-03** — Skip (discard, silent) / Next (persist + toast) semantics implemented in variant B; Next is gated on selection
- [x] **F-04** — Variant A mood buttons wired with toggle selection, `aria-live` announcement, `localStorage` persistence, and `POST /api/quick-log/mood` (currently `// TODO(api)` no-op); analogues in B (energy row) and C (sheet mood row)
- [x] **F-06** — Unified 5-point face scale (😣 rough / 😕 low / 😐 ok / 🙂 good / 😊 great) is now the **binding standard** across all three variants and the About-You area; ⚡ / 😴 / 😌 glyphs removed
