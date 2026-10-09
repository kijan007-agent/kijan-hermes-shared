# UI/UX Follow-up — Quick-Log JS-Wiring + Mood-Skala

Task: t_11c32b47 · Profile: ui-ux-designer · Branch: dev
Bezugs-Review: `2026-10-07-quick-log-mockup-review.md` (Commit `91512e6`, Findings F-03 / F-04 / F-06)

## Scope
Umsetzung der Interaktions-/Skala-Patches aus F-03, F-04, F-06 in den drei Varianten (`variant-a/b/c.html`) und in `DESIGN-SPEC.md`. Out-of-scope laut Body: A11y-CSS und API-Backend (`t_f91cdd18-followup-api`).

## Findings — Status

### F-03 (Medium) Skip vs Next semantisch entkoppeln — DONE
- **Variante B** (`variant-b.html`): Skip-Button verwirft die aktuelle Auswahl **ohne Toast** und rückt vor; Next persistiert in `localStorage` (Key `kpt.quicklog.guided`) und blendet einen kurzen Toast ein. Next ist `disabled` solange keine Energy-Auswahl existiert (Schritt 1). Schritt 2 (Symptome) hat keine Pflichtauswahl — Done wird freigeschaltet sobald Schritt 2 erreicht ist.
- Hydration aus `localStorage` setzt die Auswahl + Schritt beim Reload wieder.
- API-Call als `// TODO(api)` no-op bis `t_f91cdd18-followup-api` landet.

### F-04 (Medium) Mood-Logik funktional machen — DONE
- **Variante A** (`variant-a.html`): `onclick`-Handler auf `.mood`-Buttons mit:
  - Single-Select-Toggle (zweiter Klick auf denselben Button löscht die Auswahl — defensive gegen Misclick)
  - `role="radiogroup"` / `role="radio"` / `aria-checked` für assistive tech
  - `aria-live="polite"` Region kündigt "Mood logged as …" an
  - Toast "Mood (label) saved."
  - `localStorage` persistiert (Key `kpt.quicklog.mood`) + Hydration beim Reload
  - `POST /api/quick-log/mood` mit Body `{ mood: <1..5>, at: <ISO8601> }` — als `// TODO(api)` no-op bis Backend verfügbar
- **Variante B** (Energy-Reihe) und **Variante C** (Mood-Reihe am Sheet-Anfang) verwenden dieselbe Logik (radio-group + `localStorage` + `// TODO(api)` POST).

### F-06 (Low) Mood-Skala vereinheitlichen — DONE
- Eine Skala: `😣 rough / 😕 low / 😐 ok / 🙂 good / 😊 great` (Codes 1..5).
- ⚡ aus Variante B entfernt; 😴 und 😌 ebenfalls raus.
- Variante C hat jetzt zusätzlich eine "How do you feel?"-Reihe oben im Mini-Sheet mit derselben Skala.
- In `DESIGN-SPEC.md` als **bindender Standard** für alle drei Varianten **und den About-You-Bereich** dokumentiert (Tabelle + deprecated-Glyphs explizit gelistet).

## Deliverables (in Workspace `t_11c32b47`)
- `variant-a.html` (10.245 B) — Home MoodOneTap + JS-Wiring
- `variant-b.html` (10.577 B) — Guided Check, Skip/Next entkoppelt, ⚡ entfernt
- `variant-c.html` (11.583 B) — Mini Sheet, Mood-Reihe oben, alle Controls verkabelt
- `DESIGN-SPEC.md` — Mood-Skala als bindender Standard + Interaction-Contract für F-03 / F-04 dokumentiert

## Geänderte Stellen im Detail

### variant-a.html
- `.mood`-Buttons: `role="radio"`, `aria-checked`, `aria-label`, `data-mood` (war `data`)
- Demo-`.sel` entfernt (war hartkodiert auf "low")
- `.row#moods` als `role="radiogroup"` mit `aria-label`
- Neues `<div id="mood-live" aria-live="polite" class="sr">` für Screenreader-Ankündigung
- Neues `<script>` mit `selectMood`, `showToast`, `persistLocal`, `postMood`, Hydration
- `.toast` CSS auf `pointer-events:none` ergänzt (war hinderlich für Klicks)

### variant-b.html
- Energy-Reihe: 5 Buttons (war 4), `role="radiogroup"`, ⚡ durch 🙂 ersetzt, 😴 / 😌 raus
- Symptom-Reihe: `data-sym`-Attribute + `id="sym-list"` ergänzt
- Skip/Next Buttons: Inline-`onclick` entfernt, sauberer `<script>`-Block mit State-Machine
- Neuer `.toast` Style + `#toast` Element
- `localStorage`-Key `kpt.quicklog.guided` für State-Persistenz + Hydration
- Next-Button disabled bei fehlender Auswahl (Schritt 1), "Done" auf Schritt 2

### variant-c.html
- Neue `Mood`-Reihe oben im Sheet (5 Buttons, unified scale, F-06)
- Symptom-/Severity-/Body-/Note-Controls bekommen `data-`-Attribute + IDs
- Cancel/Save Buttons: inline-`onclick` raus, `<script>`-Block verkabelt alle Radiogruppen + Multi-Select
- `localStorage`-Key `kpt.quicklog.sheet` + `// TODO(api)` POST-Stub
- Save-Button gating: aktiv wenn `mood ODER symptom` gewählt; severity pflicht wenn symptom gewählt

### DESIGN-SPEC.md
- Neuer Abschnitt "MoodQuickButton — unified face scale (F-06 binding standard)" mit Glyph/Code/Label/Meaning-Tabelle
- "Interaction contract (binding for engineering)" Sektion mit Skip-vs-Next-Tabelle, Mood-Selection-Bullets, About-You-Hinweis
- Acceptance-Criteria-Liste erweitert um F-03/F-04/F-06 mit [x]

## Akzeptanzkriterien (Task-Body)
- [x] Drei Varianten haben echte `onclick`-Handler (kein Demo-Static-State)
- [x] Mood-Skala dokumentiert in `DESIGN-SPEC.md` als verbindlicher Standard
- [x] JS-Snippets kommentiert mit `// TODO` wo API-Endpoint noch offen ist (`t_f91cdd18-followup-api`)

## Verifikation
- `node --check` auf jeden extrahierten `<script>`-Block → OK (Syntax valide)
- Tag-Balance `html`/`body`/`script` in allen drei Files → 1:1
- HTML-Größe plausibel (10–12 KB pro File)
- Acceptance-Criteria oben abgehakt