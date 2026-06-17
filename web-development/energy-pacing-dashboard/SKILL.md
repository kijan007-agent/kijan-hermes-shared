---
name: energy-pacing-dashboard
description: Energy pacing dashboard patterns for Kijan Personal Tracker — energy_level ↔ spoon conversion, personal_dashboard.html quirks, /api/checkin/graph endpoint, slider configuration
---

# Energy Pacing Dashboard Patterns (Kijan Personal Tracker)

## Domain
Kijan Personal Tracker dashboard — energy pacing check-ins, spoons unit, energy progression graph.

## Core Conversion Logic

### energy_level (0–100) ↔ spoons (0–25)
```javascript
// energy_level → spoons
const spoons = Math.round(energy_level / 100.0 * totalSpoons);

// spoons → energy_level (for API)
const energy_level = Math.round(spoons / totalSpoons * 100);
```

`totalSpoons` comes from `_pacingConfig.total_units` (default 25) or `device.total_units` in backend.
`unit_mode` from config: `'spoons'` or `'energy'`.

**ALWAYS check `unit_mode` before displaying or sending values.** Default fallback is `'spoons'`.

## Dashboard Template (personal_dashboard.html)

### Key Functions
- `loadEnergyProgression()` — fetches `/api/checkin/graph`, renders 24h chart
- `loadTodayCheckin()` — fetches `/api/checkin/today`, displays spoons/energy
- `submitCheckin()` — submits from pacing tab slider (converts spoons → energy_level)
- `quickCheckin()` — submits from quick check-in (converts spoons → energy_level)
- `updateEnergySlider(config)` — syncs `ci-energy` and `qc-energy` sliders to unit_mode
- `loadPacingConfig()` — fetches `/d/{device_id}/config/pacing`

### Change-Value Input Pattern (NEW)
- Instead of absolute-value slider, use +/- buttons with a delta input
- Layout: `[−] [input: change value] [+]`
- Backend computes: `base_energy + change` → clamped to 0–100
- `adjustValue(delta)` helper: reads input, adds delta, updates input element
- `loadTodayCheckin()` must pre-fill `ci-energy-change` with `change_from_last` from API response

### loadTodayCheckin()
- Must update both `checkin-display` and `energy-progression-empty` visibility
- Must update spoon icon via `current-spoon-icon` element (img src with spoon-color)
- Must calculate and display `change_from_last` in `ci-energy-change` input
- Spoons mode: `min="0" max="25" value="12"` (step=1)
- Energy mode: `min="0" max="100" value="50"` (step=5)
- Label updates via `updateEnergySlider()` based on `unit_mode`
- Always add `id="qc-energy-label"` for JS updates

### Pacing Tab Slider (id="ci-energy")
- Same dual-mode pattern as qc-energy
- Pre-filled from `loadTodayCheckin()` response

### Energy Progression Chart
- Endpoint: `/d/{device_id}/api/checkin/graph`
- Returns: `unit_mode`, `total_units`, `today[]`, `yesterday[]`, `7day_avg[]`, `7day_min[]`, `7day_max[]`
- X-axis: hours 00–23, Y-axis: 0 to `total_units`
- 5 datasets: 7-day max, 7-day avg, 7-day min, yesterday, today
- All values on chart must be converted to spoons if `unit_mode === 'spoons'`

#### Zone Backgrounds
- 0–10: red band (`rgba(239, 68, 68, 0.15)`)
- 10–20: yellow band (`rgba(245, 158, 11, 0.15)`)
- 20–30: green band (`rgba(34, 197, 94, 0.15)`)
- Implemented via Chart.js `beforeDatasetsDraw` plugin — draw rects per zone on yScale pixels

#### Spoon Icon Overlay
- Use Chart.js `afterDraw` plugin to draw `spoon-green.png` / `spoon-yellow.png` / `spoon-red.png` at each point coordinate
- Threshold: >=20 green, >=10 yellow, <10 red
- Image size: 20x20px, centered at point (cx - 10, cy - 10)

## Backend (personal.py)

### `/api/checkin/graph` Endpoint
- Reads from `energy_pacing_checkins` table (DailyCheckin model)
- Converts `energy_level` → `spoons` in response using device config
- Aggregates: today's check-ins (by hour), yesterday's, 7-day avg/min/max (by hour)
- Empty state when no data exists for any period

## Task Files
- Location: `kpt-doc/_tasks/`
- Naming: `TASK-{number}_{description}.md`
- Numbering starts at **103** for this project's active tasks
- Completed tasks move to `kpt-doc/_done/`

## Pitfalls
1. **Never hardcode slider ranges** — always derive from `_pacingConfig` or device config
2. **Always convert on both sides** — display → spoons, submit → energy_level
3. **Check `unit_mode` with fallback** — never assume it's one mode
4. **Backend conversion uses device config, not user config** — ensure consistency
5. **Chart empty state** — check all datasets for null, show placeholder message

## Support Files

- `references/chart-zone-spoon-pattern.md` — Chart.js zone backgrounds + spoon icon overlay plugin
