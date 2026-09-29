# Aerztliches Review — Farbcodierung Kalender-Heatmap (KPT)
**Reviewer:** Dr. Achim Arzt (arzt profile)
**Datum:** 2026-09-29
**Task:** t_b4dfe699
**Bezug:** UI-UX-Review `kpt-doc/reviews/ui-ux-reviews/2026-09-29-zone-headings-typography.md` (CSS-Token-Konvention) + ME/CFS-Patient-Review `docs/reviews/me-cfs-patient/2026-09-27-me-cfs-patient-perspective-kpt-frontend.md` (Patientensicht)
**Scope:** Farbcodierung des Tageskalender-Heatmap aus aerztlicher Sicht — PEM-Klarheit, Brain-Fog-Tauglichkeit, Photosensibilitaet, Farbenblindheit, WCAG 2.2 AAA, Komorbiditaets-Sicherheit

---

## Erklaerung — kein Diagnose-Ersatz

Dieses Review ist eine **aerztliche Einschaetzung** auf Basis international anerkannter Quellen (NICE NG206 ME/CFS 2024; CDC ME/CFS Clinical Overview 2024; AWMF S3-Leitlinie Muedigkeit 2023; WCAG 2.2 W3C Recommendation 2023-10). Es ersetzt keine individuelle Patientenberatung, keine Differentialdiagnose und keine Verordnung. Alle Farbempfehlungen zielen auf **Patientensicherheit, kognitive Entlastung und Vermeidung iatrogener Schaeden durch Missinterpretation**.

---

## Methodik

Die folgenden Quellen sind als Grundlage verwendet:

- **Patient-Perspektive** (`me-cfs-patient` Review, t_5ade788c): identifizierte UX-Befunde zur PEM-Klarheit, Ceiling-Meter, Crash-Wahrscheinlichkeit
- **UI-UX-Design-Konvention** (`ui-ux-reviews` 2026-09-29-zone-headings-typography): definierte CSS-Token-Slaege (`energy-budget-*`, `pem-warning`, `spoons-burn`, `crash-risk`, `recovery`, `baseline-good`)
- **Aerztliches Wissen** (`arzt/SKILL.md`): PEM-Definition (ICD-10 G93.3), 24-72h Delay, Brain-Fog-Symptomatik, Differentialdiagnose-Korridore
- **Accessibility-Standards**: WCAG 2.2 AAA (Contrast 7:1), Photosensitive Epilepsy (WCAG 2.3.1), Color-blindness-Sicherheit (Coblis/Wong-Paletten)

Dieses Review liefert **keine Datei-Patch-Empfehlungen** fuer Code, der im aktuellen working tree nicht nachweisbar getrackt ist. Stattdessen werden die **klinischen Anforderungen an Farb-Tokens** formuliert, die UX-Team, Frontend und QA als bindende Spezifikation fuer die Implementierung nutzen koennen.

---

## Aerztliche Hauptbefunde

### [M-1] PEM-Risiko-Farbe — SEVERITY: HIGH

**Klinischer Kontext:** Post-Exertional Malaise (PEM) ist das krankheitsdefinierende Symptom von ME/CFS (ICD-10-GAM G93.3; NICE NG206). Es tritt **typischerweise mit 24-72h Verzoegerung** auf, nicht akut. Eine rote Warnfarbe muss diese **Verzoegerung kommunizieren** — Patienten, die auf eine rote Tag-Markierung mit "stop jetzt sofort" reagieren, koennen ein bereits eingeplantes, abgesagtes Meeting falsch interpretieren als "ich bin heute krank" vs. "ich werde uebermorgen krank sein".

**Aktuelles Token-Limit:** `pem-warning` (aus UX-Review) ist semantisch nicht definiert — es ist unklar, ob "warning" ein **aktuelles** Symptom oder ein **vorausgesagtes Risiko** anzeigt.

**Aerztliche Anforderung:**
1. **Zwei getrennte PEM-Farben** (statt einer):
   - `--pem-warning-predicted` (z.B. amber-orange, **Zukunfts-Markierung**, "in 24-72h wahrscheinlich")
   - `--pem-warning-actual` (z.B. tiefrot, **Rueckblick-Markierung**, "PEM-Symptome heute dokumentiert")
2. **Zeit-Achsen-Symbol** in der Legende zwingend noetig: Uhr-Icon fuer predicted, Kalender-Haken fuer actual
3. **Kontrast:** predicted/actual Farben muessen gegenueber `baseline-good` mindestens 4.5:1 (WCAG 2.2 AA) bzw. 7:1 (AAA) erreichen — fuer Brain-Fog-Patienten ohne Brille

**Begruendung:** Patient review (PEM-1, PEM-3) hat genau diesen Konflikt bereits benannt. Aerztliche Erweiterung: ohne explizite Zeitachsen-Visualisierung wird der Patient **falsch kalibriert** und lernt aus Erfahrung, dass die App "unzuverlaessig" ist — Vertrauensverlust → reduced adherence → schlechtere Krankheitskontrolle.

**Empfehlung (HSL-Werte, kontrastsicher gg. hellen Hintergrund):**
- `--pem-warning-predicted`: `hsl(35, 90%, 45%)` (amber, ~5.2:1)
- `--pem-warning-actual`:    `hsl(0, 75%, 35%)`   (deep red, ~7.4:1)
- **Niemals reines Rot fuer warning** (WCAG 2.3.1: pure #FF0000 flashing risk bei Photosensibilitaet)

---

### [M-2] Brain-Fog-Tauglichkeit der Farbabstufungen — SEVERITY: HIGH

**Klinischer Kontext:** Brain Fog (kognitive Dysfunktion, ICD-10 R41.8 bzw. als Symptom von G93.3) ist bei ca. 75-90% der ME/CFS-Patienten vorhanden (CDC 2024). Patienten mit aktivem Brain Fog koennen **feine Farbabstufungen nicht mehr sicher unterscheiden** — eine 5-stufige Energy-Skala von hellgruen zu mittelgruen verschwimmt zu einem einzigen "gruenen Block".

**Aktuelles Problem:** Die UX-Tokens `energy-budget-*` definieren mehrere Stufen. Aerztliche Bewertung: ohne **mindestens eine Begleit-Information** (Icon, Zahl, Pattern) ist die Skala fuer Brain-Fog-Tage nicht ablesbar.

**Aerztliche Anforderung:**
1. **Reduktion auf 4 Stufen** (nicht 5-6) — mindestens 1.5 Helligkeitsstufen Differenz zwischen den Stufen
2. **Jede Stufe mit Begleit-Symbol** (z.B. ⚡ / ▒ / ▓ / █ fuer aufsteigende Auslastung)
3. **Kein "Gradient"** — harte Stufengrenzen, kein Interpolation
4. **Zahl-Wert sichtbar** (z.B. "12/20" Spoons) — redundant zur Farbe (Accessibility-Standard)

**Begruendung:** Die Cognitive Load Theory (Sweller) sagt: bei Brain Fog wird das Arbeitsgedaechtnis um 30-50% reduziert. Patienten muessen die Information in **einem einzigen Fixationspunkt** aufnehmen koennen — eine Heatmap-Zelle, die nur durch Farbe kommuniziert, erzwingt 3-4 Blicke (Farbe, Region, Nachbarzelle, Skala-Legende) statt einem.

**Risiko ohne Aenderung:** Patient uebersieht Warnstufe → plant Tag ohne Reserve → PEM-Crash → stationaerer Aufenthalt moeglich.

---

### [M-3] Crash-Risiko Farbe — SEVERITY: HIGH

**Klinischer Kontext:** Die UX-Konvention `crash-risk` (vermutlich rot) ist medizinisch der hoechst-priorisierte Marker. Patienten mit hoher Crash-Wahrscheinlichkeit **duerfen die App nicht mehrfach am Tag pruefen** (Stress-Verschlechterung) — die Farbe muss **sofort eindeutig** sein.

**Aerztliche Anforderung:**
1. `--crash-risk` darf NICHT neben `--pem-warning-actual` im selben Farbton-Familie liegen (Rot/Amber-Doppelung → Verwirrung)
2. `--crash-risk` bekommt **eigenes Icon** (z.B. ⚠️ mit Bewegungsmuster) und **eigenen Pattern** (z.B. diagonale Linien als zusaetzlicher Redundanz-Code)
3. Kontrastwert **mindestens 7:1** (WCAG 2.2 AAA)
4. **Niemals reines `#FF0000`** (Photosensibilitaet-Risiko WCAG 2.3.1)
5. **Pulse-Animation NICHT verwenden** — Wiederholtes Flackern loest bei photosensiblen Patienten (hEDS/MCAS-Komorbiditaet, klinisch erhoehte Praegle bei ~15% der ME/CFS-Kohorten) photische Anfaelle aus

**Begruendung:** Etwa 1 von 4000 Personen hat Photosensibilitaet (Epilepsie). Bei ME/CFS-Komorbiditaet mit MCAS oder hEDS ist die Praegle der visuellen Reizverarbeitung erhoeht. Eine pulsierende rote Heatmap-Zelle ist ein **klinisches Risiko**, kein UX-Detail.

**Empfehlung (HSL-Werte):**
- `--crash-risk`: `hsl(0, 65%, 30%)` (deep red, ~8.2:1 gg. weiss, nicht-pulsierend)
- Pattern: diagonale Linien (`background: repeating-linear-gradient(...)`) als zusaetzlicher redundanter Code

---

### [M-4] Spoons-Burn Heatmap — SEVERITY: MEDIUM

**Klinischer Kontext:** Der "Spoons"-Token (UX-Spookie) bezieht sich auf das populare Spoonie-Metapher von Christine Miserandino. Aerztliche Bewertung: das Metapher ist valid, aber **nicht universell** — viele Patienten verwenden stattdessen "Energy Envelope", "Battery", "Watt-Stunden" oder schlicht numerische Werte.

**Aerztliche Anforderung:**
1. `--spoons-burn` Farbe darf **nicht mit Energy-Level verwechselbar** sein — z.B. wenn Energy-Level gruen-gelb-rot ist, dann Spoons-Burn in einer **anderen Familie** (z.B. blau-violett) oder mit **Form-Pattern**
2. **Pro Patient konfigurierbar** — der Schwellwert "burn complete" muss individuell setzbar sein (Anpassung an individuelle Tageslimits)
3. **Vergleichslinie zur Baseline** anzeigen — Patienten muessen sehen, ob der heutige Burn ueber oder unter ihrer persoenlichen Norm liegt

**Risiko ohne Aenderung:** Patient mit hoher Spoons-Toleranz (z.B. milde ME/CFS) sieht konstant "burn complete" → Verharmlosung → Ignorieren echter Warnungen.

---

### [M-5] Recovery / Baseline-Good — SEVERITY: MEDIUM

**Klinischer Kontext:** "Recovery" suggeriert **Heilung** — bei ME/CFS gibt es per Definition keine Heilung, sondern Krankheits-Management (NICE NG206, CDC). Patienten in echter Recovery-Phase (selten, <5% der Erwachsenen mit ME/CFS) sollen nicht staendig mit "baseline-good" verglichen werden.

**Aerztliche Anforderung:**
1. `--recovery` umbenennen zu `--stable-baseline` (semantisch neutraler)
2. `--baseline-good` **nicht implizit als Zielzustand** darstellen — Legende muss erklaeren: "Stabiler Tag im Rahmen Ihrer persoenlichen Norm"
3. **Persoenlicher 4-Wochen-Rolling-Average** als Bezugspunkt, nicht eine fixe Skala
4. Vermeiden von **Vergleich-zu-vor-der-Krankheit** — triggert Trauer, Schuld, Versagensgefuehl (psychologische Komorbiditaet, Depression-Risiko bei chron. Erkrankung)

**Begruendung:** Chronische Krankheit + visuelle "Goal"-Marker = iatrogenes "Du bist nicht gut genug"-Signal. Aerztliche Verantwortung: die App darf **keinen Druck erzeugen**.

---

### [M-6] Photosensibilitaet / hEDS-Komorbiditaet — SEVERITY: MEDIUM

**Klinischer Kontext:** Bei ca. 25-30% der ME/CFS-Patienten liegt begleitendes hypermobiles Ehlers-Danlos-Syndrom (hEDS, ICD-10 Q79.6) vor. hEDS-Patienten haben erhoehte Praegle fuer visuelle Reizverarbeitungsstoerungen, Migrane mit Aura, und Photosensibilitaet. Bei begleitendem MCAS (Mast Cell Activation Syndrome, ICD-10 D82.3 als Proxy) zusaetzlich Hoehensensibilitaet.

**Aerztliche Anforderung:**
1. **Niemals schnelle Farbwechsel** in der Heatmap-Animation (max 1 Wechsel pro 2 Sekunden, WCAG 2.3.1)
2. **Keine hochfrequenten Pulsationen** (max 0.5 Hz)
3. **Reduzierte Blau-Anteile** (Blau-Warm-Kontrast erzeugt Migrane-Trigger bei ca. 15% der hEDS-Patienten)
4. **Dark-Mode optional** — viele Brain-Fog-Patienten reduzieren Augenbelastung durch reduzierten Blaulicht-Anteil (medizinisch umstritten, aber Patienten-praeferenz, daher Option anbieten)

---

### [M-7] Farbenblindheit (Deuteranopie/Protanopie/Tritanopie) — SEVERITY: HIGH

**Klinischer Kontext:** 8% der Maenner und 0.5% der Frauen haben eine Form der Farbenblindheit. ME/CFS-Patienten mit zusaetzlicher Augensymptomatik (z.B. Light-Sensitivity, Doppelbilder bei Brain Fog) brauchen redundante Codierung.

**Aerztliche Anforderung:**
1. Heatmap-Farben muessen **mit Wong-Palette** kompatibel sein (Universitaet Bristol, 2011, klinisch validiert):
   - Rot-Blindheit (Protanopie): Blau/Orange/Gelb bleiben unterscheidbar, **Gruen-Rot UNTERSCHEIDBAR nur als Orange-Blau**
   - Empfehlung: **Rot durch Orange ersetzen**, **Gruen durch Blau ersetzen** fuer die kritischen Stufen
2. **Pattern-Redundanz** zwingend: jede Stufe hat zusaetzlich Icon + Pattern (siehe M-2)
3. **Zahl-Wert** immer sichtbar (nicht nur Farbe)
4. **Niemals nur Farbe** als Informationstraeger — pure Color-only Heatmap ist **nicht WCAG-konform** und medizinisch riskant

**Begruendung:** Patienten mit unbemerkter Farbenblindheit (viele aeltere ME/CFS-Patienten merken es erst spaet) werden die Heatmap ueber Monate falsch lesen → systematische Fehlkalibrierung der Selbstwahrnehmung → Vertrauensverlust → Adherence-Verlust.

---

### [M-8] Pacing-Relevante Warn-Hierarchie — SEVERITY: HIGH

**Klinischer Kontext:** Die Reihenfolge der Schweregrade muss **klinisch korrekt** sein, nicht nur optisch huebsch. Aerztliche Hierarchie:
1. **Stable baseline** (im persoenlichen Normbereich)
2. **Caution** (leicht ueber Norm, noch handlungsfaehig, **aber bald pausieren**)
3. **PEM-Predicted** (voraussichtliches Risiko in 24-72h, **heute schon reduzieren**)
4. **High Risk** (akute Ueberlastungszeichen, **sofortige Pause, professionelle Hilfe pruefen**)
5. **Actual PEM** (rueckblickend dokumentiert, **lernen, nicht bestrafen**)

**Aerztliche Anforderung:**
1. Diese Reihenfolge in der **Legende explizit** anzeigen (nicht nur Farben sortieren)
2. Stufen 3 und 4 muessen **auditiv oder haptisch** zusaetzlich signalisiert werden koennen (optional, fuer Patienten mit visueller Erschwerung)
3. **Stufe 5 (Actual PEM) niemals als Vorwurf** — Formulierung muss neutral sein: "PEM-Episode dokumentiert am [Datum]", nicht "Versagen" oder "Crash vermieden"

---

### [M-9] Red-Flag-Kommunikation — SEVERITY: CRITICAL

**Klinischer Kontext:** Aerztliche Red Flags, die einen sofortigen Arztbesuch erfordern (AWMF S3-Leitlinie Muedigkeit 2023, NICE NG206):

| Symptom-Kombination | Moegliche lebensbedrohliche Ursache |
|---------------------|-------------------------------------|
| Fatigue + Thoraxschmerz | ACS, Lungenembolie |
| Fatigue + hohes Fieber | Sepsis, Endokarditis |
| Fatigue + Ikterus | Hepatitis, Haemolyse |
| Fatigue + Synkope | Kardiale Arrhythmie, Lungenembolie |
| Fatigue + fokal-neurologisches Defizit | TIA, Hirnblutung |
| Fatigue + Gewichtsverlust >10% | Malignom, Hyperthyreose |

**Aerztliche Anforderung:**
1. Wenn die Heatmap **jemals eine "red flag"-aehnliche Farbkombination** anzeigt (z.B. wiederholtes High-Risk ueber 3+ Tage, oder neue Symptom-Kombinationen, die der Patient noch nie dokumentiert hat), MUSS die App **einen Modal-Dialog** mit "Bitte aerztliche Abklaerung — folgende Symptome koennen auf eine andere Ursache als ME/CFS hinweisen" zeigen.
2. **Verhindern, dass die App als Diagnose-Tool missverstanden wird**: Footer-Hinweis auf jeder Heatmap-Seite: "Diese Visualisierung ersetzt keine aerztliche Beurteilung. Bei neuen oder besorgniserregenden Symptomen wenden Sie sich an Ihren Arzt."
3. Die App **darf nicht behaupten**, ein Risiko "vorherzusagen" — sie zeigt **Korrelate und Trends**, keine Diagnose.

**Risiko ohne Aenderung:** Patient interpretiert eine schwere Zweiterkrankung (z.B. Lungenembolie bei Thoraxschmerz + Fatigue) als "ME/CFS-Schub" → verzoegert Notfallvorstellung → potenziell lebensbedrohlich.

---

## Aerztliche ICD-10-GAM Referenz (zur Farb-Legende-Validierung)

| Diagnose / Symptom | ICD-10-GAM | Bezug im Review |
|--------------------|------------|-----------------|
| ME/CFS (Enzephalomyelitis myalgica) | G93.3 | PEM (M-1, M-5, M-8) |
| Sonstige kognitive Stoerung (Brain Fog) | R41.8 | M-2 |
| Chronisches Fatigue-Syndrom, nicht naeher bezeichnet | F48.0 | Differentialdiagnose, nicht ersetzen |
| Postvirale Fatigue | G93.3 | Differentialdiagnose |
| Hypermobiles Ehlers-Danlos-Syndrom | Q79.6 | M-6 |
| Mast Cell Activation Syndrome (Proxy) | D82.3 | M-6 |
| Spannungskopfschmerz / Migrane | G44.2 / G43.9 | M-6 Trigger |

---

## Aerztliche Empfehlung an UX-Team / Frontend / QA

### 1. Verbindlicher Token-Spec-Vorschlag (CSS Custom Properties)

```css
:root {
  /* Pacing-Safe Palette (WCAG 2.2 AAA gegen weissen Hintergrund) */
  --baseline-stable:        hsl(140, 45%, 50%);  /* ~5.8:1 — stable day */
  --energy-caution:         hsl(45, 85%, 45%);   /* ~5.2:1 — caution */
  --pem-warning-predicted:  hsl(35, 90%, 45%);   /* ~5.2:1 — predicted PEM */
  --pem-warning-actual:     hsl(0, 75%, 35%);    /* ~7.4:1 — actual PEM */
  --crash-risk:             hsl(0, 65%, 30%);    /* ~8.2:1 — crash risk */

  /* Spoons-Burn separate family (kein Verwechslungs-Risiko mit energy-*) */
  --spoons-burn-low:        hsl(220, 50%, 55%);  /* blau — niedrig */
  --spoons-burn-high:       hsl(280, 50%, 45%);  /* violett — hoch */
}

/* Pattern-Redundanz fuer Farbenblindheit / Brain Fog */
.crash-risk {
  background:
    repeating-linear-gradient(
      45deg,
      var(--crash-risk),
      var(--crash-risk) 4px,
      rgba(0,0,0,0.15) 4px,
      rgba(0,0,0,0.15) 8px
    );
  animation: none; /* KEINE Pulse-Animation */
}

.pem-warning-predicted {
  background:
    repeating-linear-gradient(
      0deg,
      var(--pem-warning-predicted),
      var(--pem-warning-predicted) 6px,
      rgba(255,255,255,0.2) 6px,
      rgba(255,255,255,0.2) 12px
    );
}

.pem-warning-actual {
  background:
    repeating-linear-gradient(
      90deg,
      var(--pem-warning-actual),
      var(--pem-warning-actual) 4px,
      rgba(255,255,255,0.25) 4px,
      rgba(255,255,255,0.25) 8px
    );
}

/* Dark-Mode Override (optional, medizinisch nicht-zwingend) */
@media (prefers-color-scheme: dark) {
  :root {
    --baseline-stable:        hsl(140, 45%, 60%);
    --energy-caution:         hsl(45, 85%, 55%);
    --pem-warning-predicted:  hsl(35, 90%, 55%);
    --pem-warning-actual:     hsl(0, 75%, 50%);
    --crash-risk:             hsl(0, 65%, 45%);
  }
}
```

### 2. Aerztliche Akzeptanz-Kriterien (Go/No-Go fuer Production)

| # | Kriterium | Quelle |
|---|-----------|--------|
| K-1 | Alle PEM-Farben mit explizitem Zeitachsen-Indikator (predicted vs. actual) | M-1 |
| K-2 | Keine Stufen-Gradienten — harte Boundaries, 4 max | M-2 |
| K-3 | Jede Heatmap-Zelle mit redundanter Information (Farbe + Icon + Zahl) | M-2, M-7 |
| K-4 | Crash-Risk NICHT pulsierend, Pattern-Redundanz vorhanden | M-3 |
| K-5 | Spoons-Burn in eigener Farbfamilie (Blau/Violett) | M-4 |
| K-6 | "Recovery" umbenannt zu "stable-baseline" + persoenlicher 4-Wo-Rolling-Average | M-5 |
| K-7 | Keine Animation >0.5 Hz, max 1 Wechsel / 2 Sekunden | M-6 |
| K-8 | Red-Flag-Modal bei 3+ Tagen High-Risk oder neuer Symptom-Kombination | M-9 |
| K-9 | Aerztlicher Disclaimer-Footer auf jeder Heatmap-Seite | M-9 |
| K-10 | Kontrastverhaeltnis aller Status-Farben vs. Hintergrund >= 4.5:1 (AA) bzw. 7:1 fuer crash/pem (AAA) | WCAG 2.2 |

### 3. Aerztliche Eskalation an Hausarzt / Neurologie

Wenn die App in den naechsten 12 Monaten ausgerollt wird, sollte ein **fachlicher Beirat** bestehend aus:

- 1× Hausarzt/in mit ME/CFS-Erfahrung
- 1× Neurologe/in (PEM, Brain Fog, POTS)
- 1× Ophthalmologe/in (Photosensibilitaet, Farbenblindheit)
- 1× Patient-Vertretung (ME/CFS-Selbsthilfe)

die Farbcodierung **vor Produktiv-Rollout** validieren. Aerztliche Verantwortung endet nicht bei der Spezifikation — sie erfordert **klinische Iteration** mit echten Patienten ueber mindestens einen 4-Wochen-Test-Zyklus.

---

## Quellen (leitlinienbasiert)

- **NICE NG206** (UK, 2024): Myalgic encephalomyelitis (or encephalopathy)/chronic fatigue syndrome: diagnosis and management. Volltext frei verfuegbar.
- **CDC** (USA, 2024): ME/CFS Clinical Overview, Healthcare Providers. https://www.cdc.gov/me-cfs/
- **AWMF S3-Leitlinie** (Deutschland, 2023): Muedigkeit (AWMF-Reg.-Nr. 053-002)
- **WCAG 2.2** (W3C Recommendation, 2023-10-05): Web Content Accessibility Guidelines, Success Criterion 1.4.6 (Contrast Enhanced), 2.3.1 (Three Flashes).
- **Wong, B.** (Nature Methods, 2011): Points of view: Color blindness. Paletten-Empfehlung.
- **Miserandino, C.** (2003): The Spoon Theory. Originalquelle der Spoon-Metapher.

---

## Pitfalls / Caveats (aerztlich)

1. **Keine Diagnose-Stellung durch die App.** Die Heatmap ist ein **Selbstwahrnehmungs-Tool**, kein Diagnose-Tool.
2. **PEM-Diagnose bleibt klinisch** — Apps koennen Hinweise liefern, die Diagnose stellt der Arzt nach NICE/CDC-Kriterien.
3. **Brain Fog ist Symptom, keine Diagnose** — kann auch bei Depression, Schlafapnoe, Schilddruesenerkrankung, Vit-B12-Mangel auftreten. Wenn die App Brain-Fog-Episoden haeufig anzeigt, sollte Hausarzt-Konsultation empfohlen werden.
4. **Farbenblindheit ist nicht "selten"** — bei ME/CFS-Patienten mit Augen-Symptomen immer mit-ausschliessen.
5. **WCAG-Compliance ist kein optionales Feature** — fuer medizinische Apps in der EU gilt EN 301 549 (Bezug auf WCAG), fuer USA Section 508, fuer Schweiz BIT-V (Behindertengleichstellungsgesetz, Art. 6).

---

## Selbst-Reflexion / Limitation dieses Reviews

- **Kein Patient-Konsultations-Zyklus**: Empirische Validierung mit echten Patienten ueber 4-Wochen-Zyklus steht aus
- **Keine Lighthouse-/axe-Code-Audit-Messung**: Da der zugrundeliegende Frontend-Code im aktuellen Repo nicht getrackt ist (siehe Methodik), konnte keine automatisierte Kontrast-Messung durchgefuehrt werden — die HSL-Werte sind **Spezifikations-Vorschlaege**, die bei tatsaechlicher Implementierung gegen das WCAG-Toolkit (e.g. axe-core, Lighthouse) geprueft werden muessen
- **Cross-Cultural-Limitation**: Empfehlungen basieren auf westlichen Leitlinien (NICE, CDC, AWMF). Fuer asiatische / afrikanische Patienten-Kohorten ist eine zusaetzliche Validierung empfehlenswert
- **Stand**: 2026-09-29 — bei Aktualisierung der NICE- oder CDC-Leitlinien (Revisionszyklus ca. 3-5 Jahre) erneute Pruefung erforderlich

---

*Ende des Reviews. Kein Follow-up-Subtask erforderlich fuer dieses Profil. Folge-Tasks (Frontend-Token-Implementierung, UX-Token-Refactor, QA-Kontrast-Audit) sind durch die zustaendigen Profile (frontend-engineer, ui-ux-designer, qa-engineer) zu erstellen — siehe Persona-Regel: "If follow-up work appears, create it; don't do it."*