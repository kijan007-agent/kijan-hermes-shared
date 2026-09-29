# ME/CFS-Patienten-Perspektive Review — KPT Frontend
**Reviewer:** Mia ME-CFS (me-cfs-patient profile)
**Date:** 2026-09-27
**Task:** t_5ade788c
**Reviewed templates:** onboarding, pin_entry, personal_dashboard, config, export_modal, what_if_simulator, pem_risk, energy_timeline, pacing
**Base:** UX-Befundkatalog (t_a536e91e) + Architektur-Komplexitätstreiber (t_154d66d0)

---

## Zielsetzung dieses Reviews

Als ME/CFS-Patientin mit Brain Fog, Fatigue-Fluktuationen und PEM-Sensibilität prüfe ich jedes Feature darauf, ob es **tatsächlich hilft, Überlastung zu vermeiden** — oder ob es versehentlich Druck erzeugt. Mein Maßstab:

- **Pacing-by-Design:** Kann ich das System nutzen, ohne meine Energy Envelope zu überschreiten?
- **Brain-Fog-Tauglichkeit:** Kann ich es bedienen, wenn ich kognitiv eingeschränkt bin?
- **PEM-Klarheit:** Verstehe ich mein Risiko rechtzeitig, bevor ein Crash passiert?
- **Recovery-Ethik:** Werden Rückschläge nicht als Versagen, sondern als Signal dargestellt?

---

## ME/CFS-Domäne: Terminologie-Check

### [A1] Energy-Level-Vokabular — SEVERITY: HIGH
**Befund:** Die Architektur verwendet `energyLevel` (Backend), während die Templates `energy_budget`, `spoons`, `ceiling_usage`, `current_energy` wild mischen. Das führt zu Verwirrung, wenn ein Patient nach "Energy Budget" sucht und das System ihm "Spoons" zeigt.

**UX-Anforderung:** Eindeutige, patienten-verständliche Terminologie. Empfehlung: Ein konsistentes Vokabular pro Anzeige-Kontext — z.B. "Energy" als Oberbegriff, "Spoons" als Tageszähler, "Ceiling" als Tageslimit.

**Konkreter Schaden:** Wenn ein Patient mit limitierter kognitiver Kapazität nicht versteht, was "Ceiling usage 87%" bedeutet, kann er nicht richtig priorisieren.

---

### [A2] PEM/Crash/Flare — SEVERITY: HIGH
**Befund:** Architektur verwendet "PEM" (medizinisch korrekt), Templates mischen "crash", "flare-up", "overload" ohne klare Unterscheidung.

**UX-Anforderung:** Klare visuell-räumliche Unterscheidung zwischen:
- **PEM (Post-Exertional Malaise):** Die krankheitsdefinierende Reaktion — Verzögerung 24-72h nach Überschreitung
- **Crash:** Akute Energie-Erschöpfung — unmittelbar
- **Flare-up:** Symptom-Verschlimmerung (nicht identisch mit PEM)

Patienten, die diese Begriffe verwechseln, können ihre Muster nicht richtig erkennen.

---

## PEM-Risikokomponente (pem_risk.html) — Detailreview

### [PEM-1] Crash-Wahrscheinlichkeit in Prozent — SEVERITY: HIGH
**Befund:** `crash_probability` wird als Prozentzahl angezeigt (`42% Crash probability`). Dies ist für ME/CFS-Patienten **problematisch aus mehreren Gründen**:
1. **Kognitive Überlastung:** Eine einzelne Prozentzahl gibt keine Handlungsanweisung. Ist 42% "viel" oder "wenig"?
2. **Falsche Präzision:** Wahrscheinlichkeitsangaben aus einer Schätzung wirken genauer als sie sind — Patienten könnten sich darauf verlassen und riskant handeln.
3. **PEM-Delay-Problem:** PEM tritt verzögert auf (24-72h). Eine "Crash probability" suggeriert, dass der Crash unmittelbar bevorsteht — das ist für PEM falsch.

**UX-Anforderung:** Anzeige als **Risikolevel mit klarem Handlungsimpuls**, nicht als Prozentzahl. Beispiel: "⚠️ Hohes PEM-Risiko — Aktivitäten reduzieren" mit einer Farbcodierung (grün/gelb/rot) und einer konkreten Empfehlung.

**Referenz:** UX-Befundkatalog QW1 (Visibility of System Status) und Nielsen #1.

---

### [PEM-2] Ceiling-Meter: Kein Kontext für "Was bedeutet 87%?" — SEVERITY: HIGH
**Befund:** Der Ceiling-Verbrauch wird als Prozentzahl ohne Referenzpunkt gezeigt. Ein Patient sieht "87%" — aber was bedeutet das für sein heutiges Limit? Wie viele Spoons hat er noch?

**UX-Anforderung:** Ergänzend zum Prozent-Meter eine **Spoon-Anzeige im Klartext**: "12 von 20 Spoons verbraucht" — oder ein äquivalentes Konzept, das auch für Nicht-Spoon-Nutzer verständlich ist.

**Bezug:** Cognitive Load Theory — mehrere kognitive Schritte werden vermieden, wenn die Information "Wie viel habe ich noch?" direkt beantwortet wird.

---

### [PEM-3] Crash-Window: Nützlich, aber unvollständig — SEVERITY: MEDIUM
**Befund:** `predicted_crash_window` zeigt ein Zeitfenster. Das ist wertvoll, aber für PEM ungenügend, weil:
- PEM kommt typischerweise **verzögert** (24-72h), nicht als "Fenster in 4 Stunden"
- Die Anzeige suggeriert ein unmittelbar bevorstehendes Ereignis

**UX-Anforderung:** Label ändern zu "Mögliche PEM-Reaktion" mit Zeitraum + dem Hinweis, dass PEM typischerweise verzögert auftritt. Das setzt die richtige Erwartung.

---

### [PEM-4] Vorhersage-Label "Projected" — SEVERITY: MEDIUM
**Befund:** In der Energy-Timeline werden "Projected"-Werte als gestrichelte Linie angezeigt. Patienten, die sich auf Vorhersagen verlassen und dann einen Crash erleben, verlieren Vertrauen ins System.

**UX-Anforderung:** "Projected" immer als unsichere Schätzung kennzeichnen — z.B. "(Schätzung)" oder "≈" — und Vertrauensintervalle sichtbar machen.

---

## Energy Timeline — Detailreview

### [TL-1] Collapsed by Default: Hidden Critical Information — SEVERITY: HIGH
**Befund:** Die Energy-Timeline ist per Default collapsed (`class="hidden"`). PEM-Risiko-Daten sind aber **die kritischste Information** für ME/CFS-Patienten. Sie zu verstecken bedeutet, dass ein Patient diese Info nur findet, wenn er aktiv danach sucht.

**UX-Anforderung (Quick Win):** Die Energy-Timeline sollte **expanded by default** sein, zumindest beim ersten Besuch (Onboarding abgeschlossen, kein previous state). Optional ein "Collapse" für erfahrene Nutzer, die sie wegklappen wollen.

**Referenz:** Nielsen #3 (User Control), Recovery-by-Design — die kritischste Information muss IMMER sichtbar sein.

---

### [TL-2] Spoons-Anzeige: Konsistenz — SEVERITY: MEDIUM
**Befund:** Die Timeline zeigt "🥄 Spoons" im Summary-Bar, aber der Rest des Systems (pem_risk, forecast) verwendet "Energy" als Begriff. Das erzeugt kognitive Reibung.

**UX-Anforderung:** Einheitliche Terminologie oder ein konsistenter Wechsel zwischen Konzepten mit einem klaren Mapping.

---

## What-If-Simulator — Detailreview

### [WI-1] Preset-Labels "Light/Moderate/Active" — SEVERITY: HIGH
**Befund:** Die Preset-Buttons zeigen "Light / 10 min", "Moderate / 30 min", "Active / 1 hour". Für ME/CFS-Patienten ist "Moderate" eine täuschende Bezeichnung — 30 Minuten "moderate" Aktivität können PEM auslösen, je nach individuellem Zustand.

**UX-Anforderung:** Die Preset-Labels sollten **PEM-spezifisch** sein, nicht alltagssprachlich:
- "Sehr leicht (10 Min)" — kein/spart Spoons
- "Leicht (30 Min)" — einzelne Spoon
- "Anstrengend (1h)" — hohe PEM-Gefahr

Oder: Die Labels mit individuellen Spoon-Kosten versehen, die der Patient selbst kalibriert hat.

---

### [WI-2] Crash Probability im What-If: Falsche Klarheit — SEVERITY: HIGH
**Befund:** Der What-If-Simulator zeigt eine einzelne "Crash probability"-Zahl. Das ist dieselbe Problematik wie bei PEM-1, aber hier noch gefährlicher, weil der Patient aktiv plant.

**UX-Anforderung:** Anstelle einer Prozentzahl: Eine farbcodierte Risikokategorie (grün/gelb/rot) plus ein Klartext-Hinweis: "Aktivität mit erhöhtem PEM-Risiko — Consider breaking into smaller chunks".

---

### [WI-3] 48h-Impact: Mini-Balken ohne Achsenbeschriftung — SEVERITY: MEDIUM
**Befund:** Die 48h-Impact-Grafik (8 Balken, 6h-Segmente) hat nur generische Zeitmarken (0h, 6h, ... 48h). Für Brain-Fog-Patienten ist das schwer zu lesen.

**UX-Anforderung:** Reale Uhrzeiten anzeigen ("08:00", "14:00" etc.) oder Wochentage. Kognitive Barriere minimieren.

---

## Onboarding — Detailreview (Ergänzend zu UX-Befundkatalog)

### [ONB-1] Energy-Tracking erklären: "Was passiert wenn ich nichts tracke?" — SEVERITY: HIGH
**Befund:** Der UX-Befundkatalog identifiziert fehlende Erklärungen im Onboarding. Aus ME/CFS-Perspektive ist der wichtigste fehlende Punkt: **Was passiert, wenn ich einen Tag nicht tracke?**

Viele ME/CFS-Patienten haben Tage, an denen sie nicht in der Lage sind, ihr Handy zu benutzen. Wenn das System an diesen Tagen "0 Spoons" als Realität annimmt, generiert es falsche Daten.

**UX-Anforderung:** Im Onboarding klar kommunizieren:
- "Du kannst vergangene Tage nachholen"
- "Fehlende Tage werden nicht als 0 gewertet"
- Hinweis auf die "Missed day"-Policy

---

### [ONB-2] PEM-Verständnis im Onboarding — SEVERITY: HIGH
**Befund:** Es gibt keinen expliziten Abschnitt im Onboarding, der PEM erklärt — die krankheitsdefinierende Eigenschaft von ME/CFS. Das bedeutet, dass Patienten, die neu diagnostiziert wurden, nicht verstehen, warum das System ihre "Crashes" verzögert vorhersagt.

**UX-Anforderung:** Kurze, nicht-medizinische Erklärung: "PEM bedeutet, dass sich Überlastung oft erst 24-72 Stunden später bemerkbar macht. KPT zeigt dir提前 (vorher) Warnungen, damit du rechtzeitig gegensteuern kannst."

---

## Recovery-Ethik

### [REC-1] Crash-Darstellung: Nicht als Versagen — SEVERITY: HIGH
**Befund:** Wenn ein Patient einen Crash erleidet, zeigt das System das als negativen Zustand. Aus psychologischer Sicht kann das Schuldgefühle erzeugen — "Ich habe versagt".

**UX-Anforderung:** Sprache und Framing anpassen:
- ❌ "Crash detected" / "Overload"
- ✅ "PEM signal detected" / "Body signalling need for rest"
- ✅ "You respected your limits today — tomorrow may be different"

Recovery-Messages sollten informativ sein, nicht verurteilend. Dies unterstützt die psychologische Sicherheit, die für chronisch Kranke essenziell ist.

**Bezug:** Psychologischer Berater-Befund (t_dad66073) — Self-Efficacy und Attribution.

---

### [REC-2] Kein Streak/Performance-Druck — SEVERITY: MEDIUM
**Befund:** Check-in-Streaks, Consistency-Scores oder ähnliche Gamification-Elemente erzeugen für ME/CFS-Patienten gefährlichen Druck. Auf einen "Streak" hinzuarbeiten, kann Patienten dazu verleiten, sich zu überlasten, um den Streak nicht zu brechen.

**UX-Anforderung:** Keine Streak-Mechanik. Wenn Consistency angezeigt wird, immer mit dem Kontext: "Consistency helps you see patterns — not a score to maximise."

---

## Quick Wins aus ME/CFS-Perspektive

| ID | Befund | Aufwand | Nutzen | Priorität |
|---|---|---|---|---|
| QW-M1 | Energy-Timeline: Expanded by default | Niedrig | Hoch | **Quick Win** |
| QW-M2 | "Crash probability" → Farblabel + Handlungstext statt % | Niedrig | Hoch | **Quick Win** |
| QW-M3 | Ceiling-Meter: Spoon-Rest-Anzeige ergänzen | Niedrig | Hoch | **Quick Win** |
| QW-M4 | Recovery-Sprache: "PEM signal" statt "Crash/Overload" | Niedrig | Mittel | **Quick Win** |
| QW-M5 | Onboarding: PEM-Verzögerung erklären | Mittel | Hoch | **Quick Win** |

## Mittelfristige Maßnahmen aus ME/CFS-Perspektive

| ID | Befund | Aufwand | Nutzen | Priorität |
|---|---|---|---|---|
| MM-M1 | Konsistentes Energy-Vokabular (Energy/Spoons/Ceiling) | Mittel | Hoch | Mittelfristig |
| MM-M2 | What-If: PEM-spezifische Aktivitätslabels | Mittel | Hoch | Mittelfristig |
| MM-M3 | 48h-Timeline: Reale Uhrzeiten statt generische Labels | Niedrig | Mittel | Mittelfristig |
| MM-M4 | Onboarding: Fehlende Tage nicht als 0 | Mittel | Mittel | Mittelfristig |
| MM-M5 | No-Streak-Policy: Kein Gamification-Druck | Niedrig | Hoch | Mittelfristig |

## Strategische Überarbeitung aus ME/CFS-Perspektive

| ID | Befund | Aufwand | Nutzen | Priorität |
|---|---|---|---|---|
| ST-M1 | Architektur: A1/A2/A3 Terminologie-Konsolidierung | Hoch | Hoch | Strategisch |
| ST-M2 | Architektur: B1 Domain-Overlap (Activity/Symptom/Pacing) | Hoch | Mittel | Strategisch |
| ST-M3 | Full i18n: Alle PEM-Terme in allen Sprachen | Hoch | Mittel | Strategisch |

---

## Zusammenfassung

Das KPT-Frontend hat eine **solide PEM-Risikoinfrastruktur** (Ceiling-Meter, Crash-Window, What-If-Simulator). Die Kernprobleme aus ME/CFS-Patienten-Sicht sind:

1. **Kognitive Barriere durch Prozentzahlen** — Crash probability und Ceiling usage als nackte % sind nicht handlungsleitend für jemanden mit Brain Fog
2. **Begriffsverwirrung** — PEM/Crash/Flare/Overload werden inkonsistent verwendet, was Muster-Erkennung erschwert
3. **Information versteckt** — Die wichtigste Information (Energy-Timeline) ist collapsed
4. **Recovery-Ethik fehlt** — System framing kann Schuldgefühle erzeugen statt informieren

Alle identifizierten Befunde sind mit den UX-Heuristiken (Nielsen #1, #3, #4, #5) und WCAG 2.2 kongruent. Der größte Impact kommt aus den Quick Wins QW-M1 bis QW-M5 — geringer Aufwand, hoher Nutzen für genau die Patienten, die das System am meisten brauchen.
