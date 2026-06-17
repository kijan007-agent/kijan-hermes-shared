# Web Dashboard Migration — Session 2026-05-22

## Migration: personal_dashboard.html (Jinja2) → kijan-web (Next.js 15)

### Source Analysis
- **File:** `/workspace/Github/KijanPersonalTracker-hermes/kpt-backend/templates/personal_dashboard.html`
- **Size:** 109,705 bytes, 2,303 lines
- **Canvas elements:** 5 (qc-chart, qc-chart-main, timelineChart, phaseChart, energy-progression-chart)
- **Inline JS blocks:** 3 (QuickCheckin, EnergyProgression, ActivityCosts)
- **Inline CSS:** 1 block (L12-122, ~110 lines)
- **Sections (id="xxx"):** 62 unique IDs
- **i18n keys:** ~50+ via `{{ t.get("key", "default") }}`
- **Languages:** 8 (de, en, es, fr, it, ja, nl, pt, zh-CN)

### Template Sections → Component Mapping

| Section ID Range | Purpose | Lines | New Component |
|-----------------|---------|-------|---------------|
| qc-spoon-icon → qc-status | Quick Check-in | 124-179 | `QuickCheckin.tsx` |
| summary-spoon-icon → summary-mood | Energy Envelope | 204-238 | `EnergyEnvelope.tsx` |
| qc-chart-wrapper-main → qc-chart-empty-main | Energy Progression Chart | 239-245 | `EnergyProgressionChart.tsx` |
| activity-costs-sort → activity-costs-raw | Activity Costs | 247-265 | `ActivityCostsChart.tsx` |
| metric-toggles → phaseChart | Health Metrics + Phase Chart | 267-282 | `MetricToggles.tsx` + `PhaseChart.tsx` |
| tab-btn-* | Tab Navigation | 286-290 | `TabBar.tsx` |
| tab-content-list | Activity List View | 291-346 | `ActivityTimeline.tsx` |
| tab-content-day → day-view-content | Calendar Day View | 347-354 | `CalendarView.tsx` |
| tab-content-month → monthPhaseChart | Calendar Month View | 356-367 | `MonthView.tsx` |
| checkin-loaded → activity-costs-raw | Pacing Panel (all) | 369-469 | `PacingPanel.tsx` |
| pdf-modal | PDF Preview Modal | 474-479 | `PdfModal.tsx` |
| modal-overlay → confirm-status | Activity Edit Modal | 494-552 | `ActivityModal.tsx` |
| hint-popup → confirm-modal | Confirm/Help Modals | 556-569 | `ConfirmModal.tsx` |

### personal.py Routes → API Integration

| Route | Method | React Integration |
|-------|--------|-------------------|
| `/d/{id}/` | GET | Server Component → fetch → props |
| `/d/{id}/api/checkin/graph` | GET | `useQuery(['checkin-graph', id])` |
| `/d/{id}/api/checkin/today` | GET | `useQuery(['checkin-today', id])` |
| `/d/{id}/api/checkin` | POST | `useMutation` (optimistic) |
| `/d/{id}/api/checkin/today-consumption` | GET | `useQuery(['checkin-consumption', id])` |
| `/d/{id}/api/checkins` | GET | `useQuery(['checkins', id])` |
| `/d/{id}/api/pacing` | GET | `useQuery(['pacing', id])` |
| `/d/{id}/config/pacing` | PUT | `useMutation` |
| `/d/{id}/api/activity-costs` | GET/POST | `useQuery` / `useMutation` |
| `/d/{id}/calendar` | GET | Server Component |
| `/d/{id}/config` | GET | Server Component |
| `/d/{id}/live` | GET | WebSocket/SSE connection |

### Design Tokens (from inline CSS)

```css
/* Background */
--bg-primary: #0f172a (slate-900)
--bg-card: #1e293b (slate-800)
--bg-border: #334155 (slate-700)

/* Text */
--text-primary: #e2e8f0 (slate-200)
--text-muted: #cbd5e1 (slate-300)
--text-subtle: #94a3b8 (slate-400)

/* Brand */
--color-primary: #3b82f6 (blue-500)
--color-success: #22c55e (green-500)
--color-warning: #f59e0b (amber-500)
--color-danger: #ef4444 (red-500)
--color-garmin: #5eead4 (teal-400)

/* Zones */
--zone-green: rgba(34, 197, 94, 0.15)
--zone-yellow: rgba(245, 158, 11, 0.15)
--zone-red: rgba(239, 68, 68, 0.15)

/* Spacing */
--card-padding: 1.25rem (20px)
--border-radius: 12px (cards), 999px (badges)
--touch-min: 44px (WCAG)
```

### Translation Files
- `kpt-backend/translations/` — 9 language files (de, en, es, fr, it, ja, nl, pt, zh-CN)
- next-intl structure: `kijan-web/messages/{lang}.json`
- Copy all keys from backend → frontend, add any missing UI keys

### Framework Decision Rationale
1. **5 Canvas charts** — Chart.js CDN → Recharts components (type-safe, no CDN)
2. **107KB monolithic template** — 62 sections → 20 independent components
3. **State complexity** — Tab switching, metric toggles, check-in state → Zustand + React Query
4. **i18n** — 9 languages → next-intl (App Router native)
5. **Deploy separation** — Dashboard independent from backend deployment
6. **Hot reload** — Vite HMR for development speed
7. **Testability** — Unit tests per component, integration tests per page
8. **Accessibility** — shadcn/ui ARIA-ready components
9. **Dark mode** — Tailwind dark: classes, CSS vars for theming
10. **Type safety** — TypeScript everywhere, no runtime type errors