---
name: web-dashboard-migration
description: "Migrate static/template-based dashboards (Jinja2, Handlebars, Blade) to framework-based apps (React/Next.js, Vue/Nuxt, SvelteKit). Covers spec creation, repo scaffold, component decomposition, chart migration, API integration, and deploy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-dashboard, migration, framework-decision, nextjs, frontend]
---

# Web Dashboard Migration

## Triggers
- User asks about web dashboard frontend approach (template vs framework)
- User wants to migrate existing Jinja2/Handlebars/Blade dashboard to React/Next.js/Vue/Nuxt/Svelte
- User creates new web frontend repo for existing backend
- Any task involving "dashboard", "frontend framework", "template migration", "kijan-web"

## Core Decision Framework

### Template → Framework: When to migrate
| Signal | Action |
|--------|--------|
| Dashboard has >3 Canvas elements (Chart.js/D3) | ✅ Framework (charts need component integration) |
| >500 lines of inline JS in templates | ✅ Framework (state management unmanageable) |
| >50KB template file | ✅ Framework (need modularization) |
| Multiple tabs/views with shared state | ✅ Framework (needs router + store) |
| Dark mode toggle, theme switching | ✅ Framework (Tailwind + CSS vars) |
| i18n needed (3+ languages) | ✅ Framework (next-intl / vue-i18n) |
| <500 lines, single view, no charts | ⚪ Keep template (Jinja2 static render) |
| Marketing/Landing page only | ⚪ Keep static HTML (kpt-website pattern) |

### Framework Choice Matrix
| Need | Next.js 15 | Vue/Nuxt 3 | SvelteKit |
|------|-----------|-----------|-----------|
| TypeScript native | ✅ | ✅ | ✅ |
| Server Components | ✅ | ❌ (SSR only) | ❌ |
| shadcn/ui components | ✅ (native) | ✅ (via radix) | ⚠️ manual |
| Chart integration | Recharts (native) | vue-chartjs | svelte-chartjs |
| Deploy options | Vercel/Netlify/Nginx | Any Node | Any Node |
| Bundle size | 45-60KB (framework) | 35-50KB | 25-35KB |
| Ecosystem maturity | Highest | High | Growing |

**Default recommendation:** Next.js 15 + TypeScript + Tailwind CSS 4 + shadcn/ui + Zustand + TanStack Query

## Migration Workflow

### Phase 0: Spec Creation (C)
1. Analyze existing template: `wc -l`, `find <template_dir> -name '*.html' -exec wc -l {} +`
2. Count Canvas elements, inline JS blocks, sections/IDs via `grep -c 'id="' <template>`
3. Map template sections → new component list
4. Document framework decision with rationale (use criteria table above)
5. Write spec to `kpt-doc/_specs/<project>/web/001-web-dashboard-spec.md`
6. Include: tech stack, project structure, migration mapping, design tokens, pitfall list

### Phase 1: Infrastructure (B)
1. Ensure backend is running (Docker or direct uvicorn)
2. Verify API endpoints exist for dashboard data
3. Ensure CORS allows frontend origin
4. Export translations from backend (e.g., `kpt-backend/translations/*.json`)
5. Export design tokens (colors, spacing, typography)

### Phase 2: Scaffold (A)
1. Create `<project>-web/` repo
2. `npx create-next-app@latest --typescript --tailwind --app --src-dir --import-alias "@/*"`
3. `npx shadcn-ui@latest init` (dark mode, slate palette)
4. Install: `recharts zustand @tanstack/react-query next-intl clsx tailwind-merge`
5. Setup: `[device_id]/` dynamic route, `app/layout.tsx` with Providers, `globals.css` with design tokens

### Phase 3: Component Decomposition
For each template section:
1. Identify: HTML section → Component name
2. Extract: Props interface from template context variables
3. Replace: Inline JS → React hooks (useState, useEffect, useCallback, useMemo)
4. Replace: Chart.js → Recharts (or equivalent)
5. Replace: Inline CSS → Tailwind utility classes
6. Extract: Shared patterns → reusable components

### Phase 4: API Integration
1. Create `lib/api.ts` — fetch wrapper with auth header
2. Create `lib/store.ts` — Zustand stores for client state
3. Create `lib/query.ts` — React Query hooks for server state
4. Implement: error boundaries, loading skeletons, optimistic updates

### Phase 5: Polish & Deploy
1. Accessibility audit (ARIA, keyboard nav, touch targets ≥44px)
2. i18n: copy translations, verify all `t.get()` calls have keys
3. Deploy: Vercel/Netlify/Nginx
4. CORS proxy or backend CORS headers for API calls

## Pitfalls

1. **Never migrate marketing pages** — kpt-website (static HTML for impressum/privacy) stays static. Only migrate data-heavy dashboards.
2. **Cookie-Auth stays on backend** — Next.js must forward cookies to backend, not implement new auth. SameSite/Lax considerations for cross-origin.
3. **Chart.js → Recharts migration** — Spoon icon overlays, zone backgrounds, custom plugins need Recharts custom shape components. Not 1:1 drop-in.
4. **107KB+ template → ~20 components** — Each component must be independently testable. No mega-components.
5. **Inline CSS → Tailwind** — Custom animations (pulse, keyframes) go in globals.css or Tailwind config, not removed.
6. **Dynamic route `[device_id]`** — Decide ISR vs SSR. ISR with revalidate usually sufficient.
7. **Backend CORS must allow frontend origin** — Often forgotten. Add `COR.origins` to backend config.
8. **Design tokens first, code second** — Export colors/spacing/typography from existing template BEFORE component code. Don't guess.
9. **i18n key mapping** — Backend translations (de.json, en.json, etc.) → next-intl messages/. Copy ALL keys, even if not used yet.
10. **Framework decision must be documented** — Write spec with rationale BEFORE scaffolding. Don't scaffold and decide later.

## Support Files

- See `references/` for session-specific details (migration examples, component decompositions, API mappings)
- See `templates/` for starter files (next.config, tailwind config, provider boilerplate)
- See `scripts/` for analysis scripts (template analysis, component extraction)

## Related Skills
- `kijan-personal-tracker` — Project structure, backend, deployment
- `energy-pacing-dashboard` — Energy pacing domain specifics
- `kijan-holistic-tracking` — 3-platform architecture, unified dashboard concept
- `remote-vm-deploy` — Backend deployment on remote VMs
- `kijan-health-module` — Health module backend specs