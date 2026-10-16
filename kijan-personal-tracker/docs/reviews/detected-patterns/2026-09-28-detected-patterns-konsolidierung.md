# UI/UX-Design: DETECTED PATTERNS Konsolidierung

**Task:** `t_detected_patterns_dup`
**Finding:** "DETECTED PATTERNS" erscheint 2× auf der Today-Seite (Zone 1 + Zone 4), mit uninterpretierbaren %-Werten (z.B. "Weekend Recovery Pattern 120%").
**Sprache der UI:** Deutsch (basierend auf den Originaltexten der Findings).
**Zielgruppe:** Patient mit ME/CFS + Brain-Fog + Feinmotorik-Einschränkungen (Envelope-Logik statt Gamification).

---

## 1. Diagnose (was an der aktuellen Darstellung kaputt ist)

| Problem | Auswirkung auf Patient |
|---------|------------------------|
| Pattern-Liste 2× auf derselben Seite | Visuelles Rauschen, Patient fragt sich "welche ist richtig?" |
| Rohe %-Werte ohne Bezugsskala | "120%" ist mathematisch korrekt, aber patient:innen-irreführend. Patient denkt "mehr als möglich", das triggert Perfektionismus. |
| Keine Erklärung was das Pattern *bedeutet* | Patient kann nicht entscheiden ob Handlung nötig. |
| Unbestimmte Anzahl von Patterns | Cognitive Load — ungeplant, keine "Ends in Sicht"-Linie. |

---

## 2. Lösung — Designvorgabe

### 2.1 EINE Pattern-Karte, fester Ort: Zone 4 (Analytics)

Die Zone-1-Erwähnung (falls dort als Mini-Liste vorhanden) **entfernen** oder auf eine
*verlinkende Zeile* reduzieren:

> "Du hast X wiederkehrende Muster erkannt → siehe Analytics"

Kein zweites Pattern-Rendering in Zone 1.

### 2.2 Maximal 3 Patterns pro Karte

- Hartes Cap auf 3 sichtbare Patterns.
- Wenn mehr Muster existieren: "+ N weitere (zum Erinnern)" als inaktiver Footer-Link.
- Begründung: Brain-Fog — drei ist noch verarbeitbar, vier+ überlastet.

### 2.3 Pattern-Zeile (das ist die zentrale UI-Einheit)

```
┌──────────────────────────────────────────────────────────┐
│  ⚑  Wochenend-Erholung                          Hinweis  │  ← Confidence-Label, KEIN %
│     Du fühlst dich Mo/Di typischerweise besser.         │  ← 1 Zeile Erklärung
│                                                          │
│     [ Skala: schwach ↓ mittel ↓ stark ]   ●○ ○ ○ ○ ○    │  ← Skalen-Dots, 0–5
└──────────────────────────────────────────────────────────┘
```

Bestandteile:
1. **Icon** (links, ⚑ als Ruhe-/Beobachtungs-Symbol — kein Trend-Pfeil nach oben, kein Trophy)
2. **Pattern-Name** (1 Zeile, max. 28 Zeichen, mit Determinanten-Ergänzung in Klammern falls nötig)
3. **Confidence-Label** (rechts oben):
   - "Hinweis"  (Konfidenz 30–60 %)
   - "Mittel"   (60–80 %)
   - "Stark"    (>80 %)
   - KEINE numerischen %-Werte.
4. **Eine Zeile Erklärung** in patient:innen-Sprache, Aktiv-Form, ohne Imperativ ("du solltest").
5. **5-Punkt-Skala als Dots** statt Prozent. Skala-Label steht davor.
   - "schwach ↓ mittel ↓ stark" — kein "0% / 50% / 100%".

### 2.4 Behandlung von Werten > 100 %

Die "120%"-Werte entstehen typischerweise durch Division mit kleinem Nenner
(Wochenend-Stunden / Normalwoche-Stunden, oder Recovery-Index über 1.0 normiert).

**Designentscheidung:** Diese Werte werden in der UI **gar nicht** angezeigt.
Stattdessen wird im Backend ein **Ordinal-Label** berechnet:

| Rohwert | Label | Dots |
|---------|-------|------|
| 0.0 – 0.3 | "kaum" | ●○○○○ |
| 0.3 – 0.7 | "spürbar" | ●●●○○ |
| 0.7 – 1.2 | "deutlich" | ●●●●○ |
| 1.2 – 2.0 | "stark" | ●●●●● |
| > 2.0 | "(ungewöhnlich)" + Tooltip "Wert über erwarteter Spanne — bitte Beobachtung fortsetzen" |

Damit ist das Problem "120 % was heißt das" semantisch gelöst: es heißt "deutlich" oder
ggf. "ungewöhnlich" mit einem Erklärungs-Tooltip. Patient sieht nie eine nackte Zahl
ohne Bezugsrahmen.

### 2.5 Acceptance-Criteria-Mapping

| Kriterium | Lösung |
|-----------|--------|
| DETECTED PATTERNS nur 1× auf der Seite | Zone-1-Vorschau entfernen, vollständige Karte nur in Zone 4. |
| Jeder Pattern hat 1 Zeile Erklärung | Pflicht-Bestandteil der Pattern-Zeile, harter Length-Check (≤ 80 Zeichen). |
| Werte niemals > 100 % ohne Skalen-Erklärung | Ordinal-Labels aus dem Backend; %-Werte kommen nicht mehr in die UI. |

---

## 3. Sprachregeln (UI-Texte)

- Aktiv und sachlich, KEIN Imperativ ("du musst", "achte darauf").
- Keine Gamification ("Streak", "Score", "Punkte", "Level").
- Beispiele (Copy-Vorlage für die Pattern-Generierung):

| Pattern-Name (Roh) | Erklärung-Text (Patient) |
|---|---|
| `sustained_low_energy` | "Deine Energie war in den letzten 7 Tagen durchgehend niedrig." |
| `weekend_recovery`    | "Am Wochenende geht es dir meistens etwas besser als unter der Woche." |
| `post_exertion_dip`   | "Nach Aktivitäten mit mittlerer Anstrengung folgt ein deutlicher Einbruch." |
| `medication_adherence`| "Du hast deine Medikamente an 5 von 7 Tagen wie geplant eingenommen." |
| `sleep_irregularity`  | "Deine Schlafenszeit schwankt deutlich von Tag zu Tag." |

Diese Texte sind deterministisch aus einer Lookup-Tabelle (Pattern-ID → Patient:innen-Text),
nicht LLM-generiert — wichtig für Klinische Verlässlichkeit / IV-Begutachtung.

---

## 4. Reduced-Motion / Accessibility

- Pattern-Karte ist `<details>` aufklappbar — default collapsed auf mobilen Viewports.
- Dot-Skala hat `aria-valuenow` + Text-Alternative für Screenreader ("3 von 5, deutlich").
- Konfidenz-Label hat Icon + Text ("Hinweis" mit ⚑), nicht nur Farbe.
- Keine Animation beim Einblenden (Brain-Fog sensibel für Bewegungs-Auslöser).

---

## 5. Offene Punkte für die Umsetzung

| Punkt | Owner |
|---|---|
| Backend: Ordinal-Label aus Roh-Metriken berechnen | backend-engineer |
| Lookup-Tabelle Pattern-ID → Patient:innen-Text | content (Klinische Validierung) |
| Zone-1-Mini entfernen / auf Link reduzieren | fullstack |
| Hartes 3-Pattern-Cap im Frontend | frontend |
| Accessibility-Check (NVDA + VoiceOver + Switch-Control) | accessibility-tester |

---

## 6. Mini-Mockup

```
┌─ Analytics (Zone 4) ─────────────────────────────────────┐
│                                                           │
│  Erkannte Muster                            [Hilfe ⓘ]    │
│  ─────────────────                                          │
│                                                           │
│  ⚑  Wochenend-Erholung                  Mittel            │
│     Am Wochenende geht es dir meistens besser.            │
│     schwach ↓ mittel ↓ stark     ● ● ○ ○ ○                │
│                                                           │
│  ⚑  Erschöpfung nach Anstrengung        Stark             │
│     Nach Belastung folgt ein deutlicher Einbruch.          │
│     schwach ↓ mittel ↓ stark     ● ● ● ● ○                │
│                                                           │
│  ⚑  Unregelmäßiger Schlaf                Hinweis           │
│     Deine Schlafenszeit schwankt von Tag zu Tag.          │
│     schwach ↓ mittel ↓ stark     ● ● ○ ○ ○                │
│                                                           │
│  + 2 weitere Muster (zur Erinnerung)                     │
└───────────────────────────────────────────────────────────┘
```

---

## 7. Done-Definition

- [ ] Zone-1 zeigt höchstens noch einen 1-Zeilen-Link zur Analytics-Karte.
- [ ] Zone-4 zeigt genau eine Pattern-Karte mit max. 3 sichtbaren Patterns.
- [ ] Keine rohen %-Werte mehr in der UI; nur Dots (0–5) + Ordinal-Label.
- [ ] Jeder Pattern-Eintrag hat genau eine Zeile Erklärung in deutscher Patient:innen-Sprache.
- [ ] Lookup-Tabelle vom Klinischen Berater abgenommen.
- [ ] Accessibility-Test grün.
