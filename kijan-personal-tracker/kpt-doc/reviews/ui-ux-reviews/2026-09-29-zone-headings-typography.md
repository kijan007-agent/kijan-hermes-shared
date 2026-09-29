# KPT Zone/Section Heading Typography — Design Recommendation

**Date:** 2026-09-29
**Task:** t_zone_headings
**Author:** Ulrike "Uli" UX (ui-ux-designer profile)
**Status:** Final Recommendation

---

## Context

Kijan Personal Tracker (KPT) is a health tracking app designed for ME/CFS patients
and others with energy-limiting conditions. Cognitive accessibility is paramount:
brain fog, sensory sensitivity, and reduced processing speed are baseline user
characteristics. Section and zone headings are the primary wayfinding mechanism
in the app — they must communicate layout structure instantly, with minimal effort.

**Reference:** KPT app (energy pacing dashboard, health modules, symptom tracking,
medication, activity, sleep, journal, weekly overview, settings).

---

## Current Assessment

KPT uses a "zone" metaphor for energy bands (red/yellow/green spoon zones) in
the energy pacing dashboard. Zone background colors carry meaning (energy state).
Section headings in the current UI (based on energy-pacing-dashboard skill docs)
use a mix of ad-hoc sizing and default browser styles — no systematic hierarchy
is documented.

Key problems to solve:
- No defined heading level system (H1/H2/H3 equivalent for KPT zones)
- Font choices not verified against dyslexia / low-vision accessibility
- Contrast ratios may be insufficient for users with migraine or photosensitivity
- No explicit line-height / spacing guidance for cognitive load reduction
- Color encoding (red/yellow/green) needs text backup — not all users decode color

---

## Recommended Typography System

### Design Principles

1. **High-legibility sans-serif** — optimized for readers with low vision or dyslexia
2. **Generous spacing** — reduces cognitive processing load
3. **Short, scannable labels** — no full sentences in headings
4. **WCAG AA minimum, target AAA** — contrast ratios 4.5:1 (normal text), 3:1 (large)
5. **Color-independent** — every colored zone label also has text/icon reinforcement
6. **Envelopes not progress bars** — heading sizes grow toward maximum, not down from it
   (no gamification — no "7/10 filled"; show context, not progress)

---

### Font Stack

```
--kpt-font-primary:    'Atkinson Hyperlegible', system-ui, sans-serif;
--kpt-font-secondary:  'Lexend', 'Atkinson Hyperlegible', system-ui, sans-serif;
--kpt-font-mono:       'JetBrains Mono', 'Fira Code', monospace;
```

| Font | Why |
|------|-----|
| Atkinson Hyperlegible | Designed by Braille Institute; proven legibility for low-vision and print-disabled users. Wide letterforms, clear distinction between similar characters (l/1, O/0). |
| Lexend | Shallowslant.com research; reduces reading effort for dyslexia-spectrum users by shortening the visual word-shape. Use as secondary only. |
| JetBrains Mono | For numerical data (spoon counts, times, dosages) — prevents digit confusion. |

**Google Fonts import:**
```
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Lexend:wght@300;400;500;600&display=swap');
```

---

### Heading Level Definitions

#### Zone Heading A — Top-Level Zone Title

```
font-family:  var(--kpt-font-primary);
font-size:     1.75rem;    /* 28px at base 16px */
font-weight:   700;        /* Bold */
line-height:   1.25;
letter-spacing: 0.01em;
margin-top:    0;
margin-bottom: 0.5rem;     /* 8px */
color:         var(--kpt-text-primary);  /* #1a1a2e on light, #f0f0f5 on dark */
```

**Used for:** App-wide section names — e.g., "Energy Dashboard", "Symptom Tracker",
"Medication", "Activity Log", "Sleep", "Journal", "Settings"

**Accessibility:** 28px bold exceeds WCAG AAA for large text (3:1 contrast acceptable).
Avoid ALL CAPS — reduces reading speed for dyslexia users. Use Title Case.

**Zone indicator rule:** Zone A headings that describe an energy state MUST include
a text label AND a zone icon (spoon icon, color-coded but not color-only):

```html
<h2 class="zone-heading zone-heading--a">
  <span class="zone-icon zone-icon--green" aria-hidden="true"></span>
  Energy Dashboard
  <span class="zone-label">(High Energy)</span>
</h2>
```

---

#### Zone Heading B — Sub-Section / Module Title

```
font-family:  var(--kpt-font-primary);
font-size:     1.25rem;    /* 20px */
font-weight:   600;        /* Semi-bold */
line-height:   1.3;
letter-spacing: 0;
margin-top:    0;
margin-bottom: 0.375rem;   /* 6px */
color:         var(--kpt-text-secondary);  /* #4a4a6a on light, #c0c0d0 on dark */
```

**Used for:** Sub-sections within a zone — e.g., "Today's Check-In", "Weekly Summary",
"Medication Schedule", "Symptom Detail View", "Add Entry"

**Accessibility:** 20px semi-bold — distinguishable from Zone A without being loud.
Still readable at 200% zoom (minimum browser text zoom requirement).

**Visual differentiation from A:** Use weight contrast (700 vs 600), not size alone.
Pair with a left border accent or underline in muted tone (not color-encoded).

---

#### Zone Heading C — Card / Entry Title

```
font-family:  var(--kpt-font-primary);
font-size:     1rem;       /* 16px */
font-weight:   500;        /* Medium */
line-height:   1.4;
letter-spacing: 0;
margin-top:    0;
margin-bottom: 0.25rem;   /* 4px */
color:         var(--kpt-text-primary);
```

**Used for:** Individual entry titles, card headers, list item labels —
e.g., "Ibuprofen 400mg", "Morning Walk", "Fatigue — Level 6", "Entry: Sep 28"

**Accessibility:** 16px medium weight — comfortable body size. This prevents
"wall of bold text" where every item screams for attention (critical for
cognitive overload prevention in ME/CFS).

---

### Body / Content Text (Minimum Standard)

```
font-family:  var(--kpt-font-primary);
font-size:     1rem;       /* 16px minimum — never below */
font-weight:   400;        /* Regular */
line-height:   1.6;        /* Generous for dyslexia readability */
letter-spacing: 0.01em;
max-width:     65ch;       /* ~65 characters — reduces line-tracing effort */
```

---

### Zone Color Encoding — Text Backup Requirement

Every color-coded zone element MUST have a text or icon equivalent:

| Zone | Color | Text Equivalent | Icon |
|------|-------|-----------------|------|
| Low energy | `#dc2626` / red | "Low" | Grey/hollow spoon |
| Medium energy | `#d97706` / amber | "Medium" | Half-filled spoon |
| High energy | `#16a34a` / green | "High" | Full/filled spoon |

**CSS variable pattern:**
```css
--kpt-zone-low:    #dc2626;
--kpt-zone-medium: #d97706;
--kpt-zone-high:   #16a34a;

--kpt-text-zone-low:    #9a1a1a;   /* dark enough for #dc2626 bg */
--kpt-text-zone-medium: #92400e;  /* dark enough for #d97706 bg */
--kpt-text-zone-high:  #14532d;  /* dark enough for #16a34a bg */
```

---

### Spacing System

Based on a 4px base grid:

| Token | Value | Use |
|-------|-------|-----|
| `--kpt-space-1` | 4px | Tight inline spacing |
| `--kpt-space-2` | 8px | Card internal padding |
| `--kpt-space-3` | 12px | Between related elements |
| `--kpt-space-4` | 16px | Standard section gap |
| `--kpt-space-6` | 24px | Between zone sections |
| `--kpt-space-8` | 32px | Between major zones |

**Heading margin-bottom to next element:** 8px (--kpt-space-2) — tight, but
not cramped. Avoid large gaps above headings (creates visual "weight" imbalance).

---

### Dark Mode Considerations

```
@media (prefers-color-scheme: dark) {
  :root {
    --kpt-bg-primary:    #0f0f1a;
    --kpt-bg-secondary:  #1a1a2e;
    --kpt-text-primary:  #f0f0f5;
    --kpt-text-secondary: #a0a0b8;
    --kpt-border:        #2a2a3e;
  }
}
```

- Heading colors shift to `#f0f0f5` (primary) and `#a0a0b8` (secondary) in dark mode
- Zone background colors use the same hue with reduced opacity (0.15 instead of 0.2)
- Red/amber/green zones: reduce saturation by 10-15% in dark mode to prevent halo effect
  for users with migraine/photophobia

---

### Implementation Checklist

- [ ] Import Atkinson Hyperlegible + Lexend from Google Fonts
- [ ] Define CSS custom properties for font stack
- [ ] Define CSS custom properties for heading levels (A, B, C)
- [ ] Define spacing tokens (--kpt-space-*)
- [ ] Define zone color tokens with text equivalents
- [ ] Apply `.zone-heading--a`, `.zone-heading--b`, `.zone-heading--c` classes
- [ ] Audit all current headings: replace any below 16px body text
- [ ] Verify color zone elements have text/icon backup (no color-only indicators)
- [ ] Test contrast ratios with browser DevTools (WCAG AA minimum)
- [ ] Test at 200% browser zoom — no layout breakage
- [ ] Test with OS-level dark mode enabled
- [ ] Review with screen reader (NVDA or VoiceOver) — heading hierarchy must be logical

---

### Summary of Recommended Values

| Level | Element | Font | Size | Weight | Line-height | Color |
|-------|---------|------|------|--------|-------------|-------|
| A | Zone title | Atkinson Hyperlegible | 28px / 1.75rem | 700 bold | 1.25 | primary |
| B | Sub-section | Atkinson Hyperlegible | 20px / 1.25rem | 600 semi-bold | 1.3 | secondary |
| C | Card/entry | Atkinson Hyperlegible | 16px / 1rem | 500 medium | 1.4 | primary |
| Body | Content text | Atkinson Hyperlegible | 16px / 1rem | 400 regular | 1.6 | primary |

---

*References:*
- Atkinson Hyperlegible: https://fonts.google.com/specimen/Atkinson+Hyperlegible
- Lexend: https://www.lexend.com/
- WCAG 2.1 Success Criterion 1.4.3 (Contrast Minimum): https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum
- KPT Health-Data-Design Principles: ui-ux-designer skill (no gamification, envelope pattern, supportive language)
