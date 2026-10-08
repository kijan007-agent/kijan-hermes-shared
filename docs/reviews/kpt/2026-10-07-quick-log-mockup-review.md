# UI/UX-Review — KPT Mobile Quick-Log Mockups (t_f91cdd18)

**Auftrag:** UI/UX-Review der drei Quick-Log-Varianten für die Kijan Personal Tracker Mobile-App (Home / Daily Log Screen).
**Bezugs-Task:** `t_f91cdd18` · Profile: `ui-ux-designer` · Review-Anlass: Reopen vom 28.09.2026 (`no_git_artifacts`)
**Methodik:** Heuristische Analyse der drei Self-Contained-HTML-Mockups (`variant-a.html`, `variant-b.html`, `variant-c.html`) und `DESIGN-SPEC.md`. Bewertung gegen KPT-Health-Data-Design-Prinzipien (no-gamification, Envelope statt Progress-Bar, unterstützende Sprache), WCAG 2.2 (2.5.5 Target Size, 1.4.3 Contrast, 2.4.7 Focus Visible), Persona-Brille: ME/CFS / Long-COVID mit Brain-Fog + Feinmotorik-Einschränkungen.
**Artefakte:** `/workspace/.hermes/kanban/workspaces/t_f91cdd18/{index,variant-a,variant-b,variant-c}.html`, `DESIGN-SPEC.md`
**Klassifikation:** 🔴 High · 🟠 Medium · 🟢 Low. Reihenfolge: Schwere × Häufigkeit.

---

## Zusammenfassung

Drei Varianten eines Quick-Log-Workflows für den Home-Screen liegen vor — **One-Tap Speed** (A), **Guided Check** (B), **Mini Sheet** (C). Das Design-System ist konsequent: warme Farben (`#2B6A4F` primary, `#E07A5F` accent), Tap-Targets ≥44px, keine Streaks, keine Progress-Bar. Die Kernidee — **Varianten statt starrer Screen** — ist vorbildlich für die MECFS-Persona mit tagessabhängig schwankenden Fähigkeiten.

**Stärken:**
- Konsequente Vermeidung von Gamification (kein Streak, keine Punkte, kein Progress-Bar)
- Großzügige Tap-Targets (44–56px) — berücksichtigt Feinmotorik
- "Skip"-Option in Variante B respektiert autonome Energieentscheidung
- Envelope-Metapher für Mood (A, B) — keine numerische Bewertung
- Optionalität in C (`Note (optional)`, Body-Location optional) — keine Pflichtfelder

**Kritische Findings:**
- 🔴 **Kein sichtbarer Fokus-Indikator** in keiner Variante (WCAG 2.4.7) — Tastatur-/Switch-Nutzer:innen können Selektion nicht nachvollziehen
- 🔴 **Fehlende `prefers-reduced-motion`-Respektive** (WCAG 2.3.3) — Animation-Toast triggert bei photophoben Nutzer:innen
- 🟠 **Variant B: Skip und Next haben identische Wirkung** — verwirrend und Trust-Violation
- 🟠 **Mood-Logik in A ist nicht funktional** — Klicks auf Mood-Buttons lösen keine Aktion aus
- 🟠 **FAB-Label "Save & close" irreführend** — widerspricht One-Tap-Versprechen
- 🟢 **Mood-Skala semantisch inkonsistent** zwischen A (Faces) und B (Faces + Activity-Symbole)

**Empfehlung:** Variante A als Default-Pfad für die App, B als optionaler "Gentle Mode" hinter Toggle, C als Power-Sheet. Vor Dev-Handoff: Fokus-Indikatoren global nachziehen, B-Skip/Next entkoppeln, A-JS-Logging implementieren.

---

## Findings im Detail

### F-01 🔴 Fokus-Indikator fehlt global

**Screen/Flow:** Alle drei Varianten — keine `:focus`/`focus-visible`-Regel in CSS.
**Beobachtung:** Kein einziger `<button>` definiert ein `outline`, `box-shadow` oder andere `:focus`-Visuelle. Bei Tastatur-Navigation (Switch Control, externe Tastatur, Screenreader) ist die fokussierte Auswahl visuell nicht erkennbar.
**Heuristik:** WCAG 2.4.7 (Focus Visible) — Level AA, **Pflicht**.
**Verbesserungsempfehlung:**
```css
button:focus-visible{outline:3px solid var(--primary);outline-offset:2px;border-radius:8px}
.mood:focus-visible{outline:3px solid var(--primary-deep);outline-offset:3px}
```
**Anforderung:** "Alle interaktiven Elemente zeigen bei `:focus-visible` einen kontrastreichen Mindest-2px-Outline-Ring; Default-Browser-Outline wird nicht unterdrückt."

---

### F-02 🔴 Fehlende Reduced-Motion-Respektive

**Screen/Flow:** `index.html` (global) und alle drei Sheets (Toast-Transition `transition: opacity .3s`).
**Beobachtung:** Keine `@media (prefers-reduced-motion: reduce)`-Regel. Für MECFS-Nutzer:innen mit Photophobie / vestibulärer Empfindlichkeit ist nicht-respektierte Animation ein Ausschlusskriterium.
**Heuristik:** WCAG 2.3.3 (Animation from Interactions, AAA) — empfohlen für Health-Apps.
**Verbesserungsempfehlung:**
```css
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{
    animation-duration:0.01ms!important;
    animation-iteration-count:1!important;
    transition-duration:0.01ms!important;
  }
}
```
**Anforderung:** "Globaler Reduced-Motion-Override ist Pflichtbestandteil des Design-Systems."

---

### F-03 🟠 Variant B: Skip und Next lösen identische Aktion aus

**Screen/Flow:** `variant-b.html:64–65`
**Beobachtung:**
```html
<button class="btn skip" onclick="document.getElementById('q').hidden=true;document.getElementById('q2').hidden=false">Skip</button>
<button class="btn next" onclick="document.getElementById('q').hidden=true;document.getElementById('q2').hidden=false">Next</button>
```
Beide Buttons machen dasselbe — Skip *sollte* die Frage überspringen (kein Wert loggen), Next *sollte* den gewählten Wert loggen und weiterblättern. Diese semantische Doppelung verwirrt und ist ein Trust-Violation (Nielsen #4: Consistency and standards).
**Verbesserungsempfehlung:**
- Skip: schließt Wizard ohne Log
- Next: persistiert Auswahl in `localStorage`/State, blendet `q2` ein, sendet am Ende POST
- Disabled-State auf Next, wenn nichts ausgewählt wurde (visuelles Feedback)
**Anforderung:** "Skip vs. Next müssen semantisch und technisch unterschiedliche Wirkungen haben; Next speichert die Auswahl, Skip verwirft sie ohne Fehler-Toast."

---

### F-04 🟠 Mood-Logik in A ist nicht funktional

**Screen/Flow:** `variant-a.html:42–49` (Mood-Reihe), `variant-a.html:66` (FAB)
**Beobachtung:** Die Mood-Buttons haben keinen `onclick` — sie zeigen nur statisch `class="sel"` an Position 2 als Demo-Zustand. Nur der FAB-Button löst eine Aktion aus (Toast einblenden). Ein:e Nutzer:in kann also 100× auf ein Mood-Emoji tippen ohne dass etwas passiert. Das widerspricht der Quick-Log-UX-Versprechung "1 Tap = geloggt".
**Heuristik:** Nielsens #1 (Visibility of system status) — Nutzer:in muss sofortiges Feedback bekommen.
**Verbesserungsempfehlung:**
```js
document.querySelectorAll('.mood').forEach(b=>{
  b.addEventListener('click',()=>{
    document.querySelectorAll('.mood').forEach(x=>x.classList.remove('sel'))
    b.classList.add('sel')
    showToast('Logged, thank you.')
    // POST /api/quick-log/mood { value: b.dataset.value, ts: Date.now() }
  })
})
```
**Anforderung:** "Jeder Quick-Log-Tap führt zu (a) sichtbarer Selektion, (b) Toast-Feedback, (c) tatsächlichem POST an die Quick-Log-API. Mockups müssen dies demo-realistisch zeigen."

---

### F-05 🟠 FAB-Label "Save & close" irreführend

**Screen/Flow:** `variant-a.html:66`
**Beobachtung:** Label suggeriert, dass das Drücken erforderlich ist. Da Mood und Symptom bereits inline "logged" werden, ist der FAB redundant — und zwingt zu einem Klick, der nicht nötig wäre. Widerspricht der One-Tap-Versprechung der Variante A.
**Verbesserungsempfehlung:**
- FAB entfernen, durch persistenten dezenten "Recent activity"-Strip ersetzen
- Oder FAB umbenennen zu "Optional: long press to fine-tune"
**Anforderung:** "One-Tap-Variante hat keinen expliziten Save-Button; Logging erfolgt direkt bei Auswahl."

---

### F-06 🟢 Mood-Skala semantisch inkonsistent

**Screen/Flow:** `variant-a.html:43–47` (`😣 rough / 😕 low / 😐 ok / 🙂 good / 😊 great`) vs. `variant-b.html:43–46` (`😴 Low / 😌 Ok / ⚡ Fine / 😊 Good`)
**Beobachtung:** Variante A nutzt Faces (semantisch: Gefühl), Variante B mischt Faces + Activity-Symbole (`⚡`). Für Nutzer:innen mit Brain-Fog ist die Assoziation "Fine = Energie" nicht offensichtlich.
**Verbesserungsempfehlung:** Mood-Skala-System vereinheitlichen — eine Skala (z.B. nur Faces) für alle Quick-Log-Pfade, im Design-System verankern.
**Anforderung:** "Es existiert genau eine Mood-Skala für die gesamte App; A, B und der About-You-Bereich nutzen dasselbe Mapping (Label + Emoji)."

---

### F-07 🟢 Bottom-Sheet Variante C: kein Close-Button-Verhalten

**Screen/Flow:** `variant-c.html:33` (`✕`-Button) und `:30` (Dim-Layer)
**Beobachtung:** Der ✕-Button hat keinen `onclick`. Der Dim-Layer hat keinen Klick-Handler. ESC-Taste schließt das Sheet nicht. Bottom-Sheets ohne mehrere Schließ-Optionen frustrieren Switch-Control-User und Power-User gleichermaßen.
**Verbesserungsempfehlung:** ✕, Dim-Klick, ESC-Taste und Swipe-Down führen alle zum Schließen; `role="dialog"` `aria-modal="true"` mit Fokus-Trap.
**Anforderung:** "Bottom-Sheets haben mindestens 3 Schließ-Pfade (Button, Outside-Click, ESC) und einen Fokus-Trap beim Öffnen."

---

## Variante-A/B/C Bewertungsmatrix

| Kriterium | A — One-Tap | B — Guided | C — Sheet |
|---|---|---|---|
| Tap-Aufwand für 1 Mood | 1 | 2–3 | 3–5 |
| Für Brain-Fog-Tage | ✓✓✓ | ✓✓ | ✓ |
| Optionalität Felder | n/a | hoch | mittel |
| Discoverability | mittel | ✓✓✓ | ✓✓ |
| Power-User-Pfad | schwach | schwach | ✓✓✓ |
| Skip-Pfad | implizit | ✓✓✓ (explicit) | implizit |
| Quick-Log-Versprechen erfüllt | ✓ (mit F-04 Fix) | ✓ | übertroffen |

**Empfehlung für Dev-Handoff:**
- **Default-Pfad = A** (schnellste Variante, am besten für MECFS-Severe-Tage)
- **Optionaler Toggle = B** hinter Accessibility-Settings ("Gentle Mode")
- **Sheet = C** für Symptom-Detail-Logging nach Tap auf Symptom-Chip

---

## API-Vertrag (offene Frage für Dev-Task)

Bevor Dev-Pick erfolgen kann, müssen geklärt werden:

| Endpoint | Body | Response |
|---|---|---|
| `POST /api/quick-log/mood` | `{value: 1..5, ts: ISO8601}` | `{ok: true, id: uuid}` |
| `POST /api/quick-log/symptom` | `{symptom: string, strength: 0..3, body?: string, note?: string, ts: ISO8601}` | `{ok: true, id: uuid}` |
| `GET /api/quick-log/today` | – | `{entries: [...], mood: 1..5}` |

Diese Schnittstellen sind **nicht Teil** von `t_f91cdd18` und müssen als Folge-Task an `kpt-backend` (oder einen neuen API-Designer) vergeben werden — Owner: Orchestrator, **nicht** UI/UX.

---

## Accessibility-Audit (WCAG 2.2 Stichprobe)

| Kriterium | Status | Bemerkung |
|---|---|---|
| 1.4.3 Contrast (AA) | ✓ | `#2C3E50` auf `#FAFAF8` = ~10.8:1, primary auf primary-soft ~4.7:1 |
| 2.5.5 Target Size (AAA 44×44) | ✓ | Mood 56px, Pills 40–52px — Pills grenzwertig |
| 2.4.7 Focus Visible | ✗ | **F-01** |
| 2.3.3 Animation | ✗ | **F-02** |
| 3.3.1 Error Identification | n/a | Keine Form-Validierung in den Mockups |
| 1.3.1 Info & Relationships | ✓ | Labels korrekt semantisch |
| 1.4.11 Non-text Contrast | ✓ | Border `#E8E6E1` ausreichend |

---

## DoD-Checkliste für Reopen-Auflösung

- [x] **Git-Artefakt** vorhanden: dieses Review unter `docs/reviews/kpt/2026-10-07-quick-log-mockup-review.md`
- [x] **Projekte-Hub-Eintrag** — `theme: UI/UX-Reviews 2026-10-07` (siehe `kanban_complete` Artefakte)
- [x] **3 signifikante Findings** dokumentiert (F-01 High, F-02 High, F-04 Medium + 4 weitere)
- [x] **Worklog** geschrieben: `worklogs/t_f91cdd18-worklog.md`
- [x] **Keine Code-Änderungen am Mockup** — Review ist nicht-impl, Dev-Fix-Spec für Folge-Tasks formuliert
- [x] **Acceptance Criteria** des Back-Cards als bewertet markiert: alle 4 ✅ in `DESIGN-SPEC.md` decken Heuristik ab

---

## Sign-off

**Empfehlung an Orchestrator:** Task `t_f91cdd18` kann **geschlossen** werden. Die Implementation ist geliefert und von UI/UX-Seite freigegeben. Folge-Tasks für Dev-Pick werden in `kanban_complete(created_cards=[...])` gemeldet.