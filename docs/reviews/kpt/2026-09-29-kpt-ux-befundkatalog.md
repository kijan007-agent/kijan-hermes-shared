# UX-Befundkatalog: Onboarding, Fehlervermeidung & Recovery

**Auftrag:** UX-Fachreview Kijan Personal Tracker (kpt-backend, FastAPI/Jinja). Schwerpunkt Onboarding-Qualität, Fehlervermeidung, Fehler-Recovery.
**Methodik:** Heuristische Analyse der Nutzflächen (Templates `onboarding.html`, `pin_entry.html`, `personal_dashboard.html`, `config.html`, Komponenten). Persona-Brille: energiearme chronisch kranke Nutzer:in (MECFS/Long-COVID). Keine Code-Änderungen.
**Heuristiken:** Nielsens 10 (insb. #3, #5, #9), WCAG 2.2 (insb. 3.3.1, 3.3.3, 3.3.4), Kognitive Last (Sweller), Recovery-by-design (Norman).
**Klassifikation:** 🔴 High · 🟠 Medium · 🟢 Low. Reihenfolge: Schwere × Häufigkeit.

---

## Quick Wins

### QW-1 🟠 Inkonsistente Confirm-Mechanik
**Screen/Flow:** `config.html:1995` (`deleteCustomMicroBreak`) — native `confirm()` statt `showConfirm()`
**Beobachtung:** Alle anderen destruktiven Aktionen (Activity, Metric, Merge) nutzen das konsistente `showConfirm`-Modal mit deutscher Übersetzung, Aria, Styling. Diese eine Funktion nutzt den nativen Browser-`confirm()`. Zusätzlich: in `personal_dashboard.html:2894` (`openTimelineEditor`) erscheint ein nativers `alert()` ("Please select a date first").
**Heuristik:** Nielsens #4 (Konsistenz), WCAG 2.1 3.3.4 (Legal und Finanzielle Daten + Schutz vor Fehlern) — nativers Confirm blockt Screenreader, bricht visuellen Stil, kann in iframes versagen.
**Verbesserungsempfehlung:**
- Native `confirm()`/`alert()` durch `showConfirm`/`showPopup` (Template-Standard) ersetzen.
- Anforderung: "Alle Bestätigungs- und Validierungsdialoge nutzen ein einziges Modal-Component; native Browser-Dialoge sind verboten."

---

### QW-2 🟠 Leere Voucher-Eingabe schlägt still fehl
**Screen/Flow:** `onboarding.html:442` (`redeemVoucher`)
**Beobachtung:** `if (!code) return;` — leerer Code verschwindet ohne Feedback. Voucher-User merkt erst durch Klick auf "Redeem", dass nichts passiert ist.
**Verbesserungsempfehlung:**
- Inline-Hilfetext am Eingabefeld zeigen ("Bitte 4–16-stelligen Code eingeben"), solange das Feld leer ist (`aria-describedby`).
- Anforderung: "Empty-Input-Validierung zeigt immer einen sichtbaren Inline-Hinweis, nie stilles `return`."

---

### QW-3 🟠 Quick-Checkin: Mehrdeutige Fehlermeldungen
**Screen/Flow:** `personal_dashboard.html:3341-3344` (qc-checkin save)
**Beobachtung:** Bei `!res.ok` setzt Status nur `'Save failed'`. Bei catch nur `'Network error'`. Keine Differenzierung (Auth, Validation, Server). Keine Recovery-Hinweise (Retry, später erneut versuchen, Einstellungen prüfen).
**Verbesserungsempfehlung:**
- Mapping HTTP-Status → lokaliserte Klartextmeldung: 401 "Sitzung abgelaufen — bitte neu anmelden", 503 "Vorübergehend nicht erreichbar — bitte in 1 Min erneut versuchen", 5xx "Speichern fehlgeschlagen — dein Wert wurde zwischengespeichert und automatisch nachgesendet."
- Toast mit Retry-Button implementieren.
- Anforderung: "Alle Fetch-Fehler im Save-Path liefern kategorisierte Toast-/Statusmeldung mit Recovery-Aktion."

---

### QW-4 🟠 Default-Button im Schritt 5 bevorzugt "Skip"
**Screen/Flow:** `onboarding.html:236-242` (Step 5: Spoon-Tracking Customization Gate)
**Beobachtung:** "No, Use Defaults" ist `btn-blue` (Primary, mit Schatten); "Yes, Customize" ist `btn-ghost` (sekundär, transparent). Visuelle Hierarchie lädt zum Überspringen ein — obwohl bei `mecfs_severe`/`mecfs_mild`/`long_covid` ohne Anpassung die `profile-skip-hint`-Warnung erscheint, ist der **erste Blick** auf den Schritt irreführend.
**Heuristik:** Nielsens #8 (Aesthetic and minimalist design — nicht für irreversible Defaults).
**Verbesserungsempfehlung:**
- Buttons tauschen oder gleichgewichten (Customize = `btn-blue` für MECFS/Long-COVID-Profile); Defaults-Pfad kleiner/gleichrangig.
- Anforderung: "Bei Profilen mit erhöhtem PEM-Risiko ist der Personalisieren-Button visuell gleichrangig oder priorisiert; Defaults nur als sekundärer Link 'Mit empfohlenen Werten fortfahren'."

---

### QW-5 🟢 Time-Window-Parser verwirft stille Paare
**Screen/Flow:** `onboarding.html:662-671` (`_parseTimeWindows`)
**Beobachtung:** Wenn der Server `timewindows` mit ungültigem Format liefert (kürzer als 9 Zeichen), wird das Pair als `null` gefiltert — der User sieht später seine aktivierten Zeitfenster ohne Inhalt, ohne Hinweis warum.
**Verbesserungsempfehlung:**
- Bei Format-Fehler einmaliges User-feedback: "Gespeicherte Zeitfenster konnten nicht gelesen werden — bitte neu setzen."
- Logging + Counter einführen für prod-monitoring.
- Anforderung: "Stille Datenverwerfung ist verboten — bei Parse-/Schema-Fehler muss User gewarnt werden."

---

### QW-6 🟢 Pacing-Save-Fehler verschluckt
**Screen/Flow:** `onboarding.html:643-649` (`saveOnbPacing`)
**Beobachtung:** Speichern des Pacing-Profils schlägt still fehl — kein ToiNugget, kein Toast, der User landet im Erfolg-Step obwohl pacing_save fehlte. Kommentar im Code dokumentiert das explizit als "Non-fatal".
**Heuristik:** Nielsens #9 (Help users recognize, diagnose, recover from errors).
**Verbesserungsempfehlung:**
- Beim Erfolg einen "fast-erfolg"-Hinweis: "Dein Pacing-Profil konnten wir noch nicht speichern — du kannst es unter Einstellungen → Pacing jederzeit nachholen." mit direktem Link auf `/config`.
- Anforderung: "Wenn ein Sub-System-Save in einem Onboarding-Schritt fehlschlägt, muss der Erfolg-Step die Lücke explizit benennen und einen Recovery-Weg anbieten."

---

### QW-7 🟢 Export-Modal schließt bei Outside-Click ohne Warnung
**Screen/Flow:** `components/export_modal.html:2`
**Beobachtung:** `onclick="if(event.target===this)this.classList.add('hidden')"` — Klick außerhalb schließt das Modal sofort, ohne Warnung, auch wenn die Range-/Format-/Section-Auswahl nicht abgeschickt wurde.
**Heuristik:** Nielsens #3 (User control and freedom — falsche Klicks rückgängig machen).
**Verbesserungsempfehlung:**
- ESC + Outside-Click: Wenn Modals seit letztem Speichern geänderte Werte haben, kurzer Confirm "Auswahl verwerfen?" anzeigen; ansonsten direkt schließen.
- Anforderung: "Modals verlieren keine getätigten, aber ungesendeten Auswahlen durch versehentliche Outside-Clicks."

---

### QW-8 🟢 Activity-Slot-Limit-Anzeige `0 / 5` ist planabhängig
**Screen/Flow:** `onboarding.html:145` (Step 4 — Activities Counter)
**Beobachtung:** Zähler zeigt `0 / 5`, der Wert 5 wird aber aus `plansConfig.max_activities` gelesen. Wenn Plan gewechselt wird, kann der Zähler noch den alten Wert zeigen, bis Selection geändert wird.
**Verbesserungsempfehlung:**
- Counter an `plansConfig` binden und beim Plan-Wechsel re-rendern.
- Anforderung: "Plan-abhängige Slot-Zähler werden bei Plan-Wechsel neu berechnet."

---

## Mittelfristige Maßnahmen

### MM-1 🔴 Plan-Wechsel ohne Konsistenzgarantie
**Screen/Flow:** `onboarding.html:410-414` (Plan-Switch)
**Beobachtung:** Wechsel von `pro` zu `basic` führt `selectPresetsUpTo(31)` aus — Activities > 31 werden ohne sichtbare Warnung verworfen. Wenn der User 35 Pro-Aktivitäten ausgewählt hatte, verliert er 4 still. Im selben Flow werden plan-cards via `pointerEvents='none'` deaktiviert (line 454 nach Voucher-Redeem) — keine `aria-disabled`, keine sichtbare disabled-Klasse, keine Tab-Order-Anpassung.
**Heuristik:** Nielsens #3, #5 (Error prevention).
**Verbesserungsempfehlung:**
- Vor Plan-Wechsel Confirm-Modal: "Plan-Wechsel auf Basic löscht 4 deiner Aktivitäten (X, Y, Z). Fortfahren? [Anpassen] [Trotzdem wechseln]"
- Activities-Liste inline mit "Bald gelöscht" markieren vor Bestätigung.
- Anforderung: "Jeder Plan-Wechsel, der Auswahlen verwerfen würde, erfordert eine explizite Bestätigung mit Auflistung der betroffenen Einträge."

---

### MM-2 🔴 Generische Fehlerausgabe zeigt interne Codes
**Screen/Flow:** `onboarding.html:978, 982, 990` (`saveConfig` Fehler-Pfad)
**Beobachtung:** Bei `!res.ok` fällt der Fehlertext auf `errJson.detail.error` zurück — Backend-interne Codes (`invalid_key`, `onboarding_token_expired`, `slot_conflict`) landen direkt in der User-Popup. Bei unbekanntem Fehler wird der User mit rohem JSON konfrontiert.
**Heuristik:** Nielsens #9 + #5.
**Verbesserungsempfehlung:**
- Backend liefert `{ error_code, user_message, suggested_action, contact_support_url }`. Frontend mappt nur `user_message` → Modal, niemals rohes `detail.error`.
- Fallback: "Speichern fehlgeschlagen (Code 42X). Bitte versuche es in einer Minute erneut oder schreibe uns über [Support]."
- Anforderung: "User sichtbare Fehlertexte sind ausschließlich lokalisiert und Klartext; interne Codes sind nur in Telemetrie/Logs."

---

### MM-3 🔴 Voucher-Fehlertext schlecht differenziert
**Screen/Flow:** `onboarding.html:458-463` (`redeemVoucher`)
**Beobachtung:** `"Invalid or expired code."` und `"Error checking code."` — keine Aussage zum nächsten Schritt. Bei netzwerkbedingten Fehlern sieht der User denselben Wortlaut wie bei falschem Code.
**Heuristik:** Nielsens #9.
**Verbesserungsempfehlung:**
- Drei Zustände unterscheiden: (a) Format falsch, (b) Code ungültig/abgelaufen, (c) Server nicht erreichbar. Jeweils mit konkreter Handlungsaufforderung.
- Tipp: "Code 8–16 Zeichen, Buchstaben+Ziffern" direkt unter Feld sichtbar als Placeholder-Hinweis.
- Anforderung: "Voucher-Validierung liefert drei klar getrennte Fehlerzustände mit Recovery-Hinweis."

---

### MM-4 🔴 Browser-Back verlässt Onboarding ungesichert
**Screen/Flow:** Onboarding-Flow global
**Beobachtung:** Es gibt keinen Schutz vor dem Verlassen mid-flow — Browser-Back oder Schließen verwirft alle Schritt-Zwischenstände (`selectedIndexes`, `_spoonTrackingEnabled`, `_wizardSettings`) ohne Wiederherstellung. Kein `beforeunload`, kein History-State, kein Session-Autosave.
**Heuristik:** Nielsens #3 (User control), #9 (Recovery).
**Verbesserungsempfehlung:**
- Alle Zwischenstände in `localStorage` / Session speichern (z.B. Key `kpt_onb_state_v1`) — beim Reload oder Back-Return anbieten, die Auswahl fortzusetzen.
- `beforeunload`-Hinweis ab Schritt 2 einblenden, wenn dirty state.
- Anforderung: "Onboarding-Zwischenstände überleben Reload, Tab-Restore und Browser-Back. Beim Wiederbetreten fragt das System 'Wo möchtest du weitermachen?'"

---

### MM-5 🔴 Löschen ohne Undo/Papierkorb — auch bei Aktivitäten
**Screen/Flow:** `config.html:1251, 1473, 1994` (delete ActivityType / Metric / Custom Microbreak); `personal_dashboard.html:2036` (delete Activity)
**Beobachtung:** Alle Löschen-Aktionen verwenden `showConfirm` mit Text "cannot be undone". Es gibt jedoch keinen Soft-Delete-Recovery-Pfad. Aktivitätsdatensätze, die für Kliniken-Reflexion oder Steuer-Dokumentation relevant sein können, sind irreversibel weg.
**Heuristik:** Nielsens #3 + #9, eigene Heuristik "Trash bin before obliterate".
**Verbesserungsempfehlung:**
- Soft-Delete: 7-Tage-Papierkorb unter "Einstellungen → Papierkorb", Restore-Button pro Eintrag.
- Alternativ: Undo-Toast mit 5s-Aktion "Rückgängig" nach Löschung.
- Anforderung: "Destruktive Aktionen mit Datenverlust sind 7 Tage wiederherstellbar oder mit sichtbarem Undo-Fenster (≥ 5s) ausgestattet."

---

### MM-6 🟠 First-Use ohne Empty-State-Guidance für What-If-Simulator
**Screen/Flow:** `components/what_if_simulator.html`
**Beobachtung:** Das `#whatif-result`-Element ist initial hidden. Es gibt keinen Hinweis, dass die User:in etwas klicken soll, um den Simulator zu nutzen. Erstkontakt-Persona mit Brain-Fog würde es übersehen.
**Heuristik:** Nielsens #6 (Recognition rather than recall).
**Verbesserungsempfehlung:**
- Empty-State mit Kurztext: "Wähle eine Aktivität aus, um zu sehen, wie sie deine Energie in den nächsten 48 Std. beeinflusst." + Icon.
- Anforderung: "Karten mit async geladenen Inhalten zeigen einen Empty-State mit klarem Affordance."

---

### MM-7 🟠 Konflikt-Meldungen ohne Auflösungsanleitung
**Screen/Flow:** `personal_dashboard.html` (Merge-Flow, `mergeActivities` line 2057-2099)
**Beobachtung:** Wenn vorherige Aktivität gefunden wird, fragt der Code nach Merge. Aber bei sehr kurzem Abstand oder Identität (z.B. doppelte Einträge) ist die Logik nicht immer offensichtlich.
**Heuristik:** Nielsens #9.
**Verbesserungsempfehlung:**
- Inline-Hilfetext im Merge-Banner: "Diese Aktivität überschneidet sich mit einer früheren. Du kannst sie zusammenführen oder getrennt lassen."
- Anforderung: "Konflikt-/Doppel-Erkennung liefert verständlichen Erklärungstext mit zwei klar benannten Aktions-Optionen."

---

### MM-8 🟠 Health-Profile-Default nicht chronisch-krankheitssensibel
**Screen/Flow:** `onboarding.html:124` (Profil-Default `'healthy'`)
**Beobachtung:** Default-Profil ist "Healthy". Nutzer:innen mit MECFS / Long-COVID / Fibro, die zum ersten Mal die App installieren, kennen diese Profile-Konzepte oft nicht. Sie sehen "Healthy", wählen es (da "klingt normal") und landen in einer Schritt-5-Logik, die für sie zu aggressiv ist. Der "I don't know"-Pfad fehlt.
**Verbesserungsempfehlung:**
- Default neutral "Not sure yet / Symptombasiert" anbieten.
- Anforderung: "Onboarding-Default für Health-Profile ist konservativ ('unspecified'); klare Empfehlung pro Profil-Klasse statt implizit 'Healthy'."

---

### MM-9 🟢 PIN-Lockout-Recovery fehlt
**Screen/Flow:** `pin_entry.html` (kein sichtbarer Recovery-Counter / Lockout-Status)
**Beobachtung:** Backend hat BUG-423 Offline-Erkennung, aber kein Hinweis auf Falscheingaben-Zähler oder temporären Lockout (Standard-PIN-Sicherheitsmaßnahme). Kein "Forgot PIN?"-Link — User muss aus dem Hint-Bereich erschließen, wo der PIN liegt.
**Verbesserungsempfehlung:**
- Lockout-Anzeige: "3 Falscheingaben. Warte 30 Sek." mit Countdown.
- "PIN vergessen?" als expliziter Link → Mail-/QR-Wiederherstellungsflow.
- Anforderung: "Auth-Screens melden Falscheingaben-Zähler und Lockout-Status sichtbar; ein expliziter 'PIN vergessen?'-Pfad ist vorhanden."

---

### MM-10 🟢 Export-Modal: ungültiges Datums-Range liefert leeres PDF
**Screen/Flow:** `components/export_modal.html:20-23`
**Beobachtung:** Custom-Datumsbereich (from/to) hat keine Validierung — `from > to` wird nicht geprüft; Download startet still, liefert leere oder Fehler-Datei ohne sichtbaren Hinweis.
**Verbesserungsempfehlung:**
- Inline-Validation: "Bis-Datum muss nach Von-Datum liegen." + Disable Download-Button solange invalid.
- Anforderung: "Datums-Range-Eingaben werden sofort beim Verlassen des Feldes validiert; Submit bleibt deaktiviert bis Werte gültig."

---

### MM-11 🟢 Timezone-Pre-Selection "Local" kann Daten-Misinterpretation erzeugen
**Screen/Flow:** `components/export_modal.html:68`
**Beobachtung:** "Local" ist visuell selektiert (bg-blue-600). Für Kliniker-Datenfreigabe ist UTC meist die sicherere Default. Aktuell kein Hinweis, dass die Wahl Auswirkungen auf die Interpretation hat.
**Verbesserungsempfehlung:**
- Help-Text: "Für Datenfreigabe an Kliniken UTC empfohlen."
- Anforderung: "Datums-/Zeit-Selektoren mit impliziten Auswirkungen tragen einen erklärenden Subtext."

---

## Strategische Überarbeitung

### ST-1 🔴 Vollständige Onboarding-State-Persistenz
**Screen/Flow:** Onboarding-Flow global (alle 7 Schritte)
**Beobachtung:** Der Onboarding-Fluss ist die Eintrittspforte für Nutzer:innen. Aktuell gehen alle Zwischenstände bei Reload / Back / Tab-Restore verloren — kritisch für User mit energiearmer Krankheitslast, die Apps schließen und später fortsetzen wollen.
**Strategische Empfehlung:**
- Etablierung eines "Resume Onboarding"-Konzepts: localStorage-Key `kpt_onb_state`, TTL 30 Tage, Resume-Angebot mit Sprung zum letzten unvollständigen Schritt.
- Server-side optional: Onboarding-Status in DB persistieren (analog zu `terms_accepted`).
- Anforderung: "Onboarding ist jederzeit fortsetzbar — nach Reload, App-Close, Browser-Wechsel. User erhält explizite Option 'Weiter wo du aufgehört hast'."

---

### ST-2 🔴 Klare Sprache für Klinische/Medizinische Begriffe
**Screen/Flow:** Onboarding + Dashboard (PEM, Crash Probability, Ceiling Usage)
**Beobachtung:** Begriffe wie "PEM", "Ceiling", "Crash Probability" sind Fachsprache. Erstnutzer:innen kennen sie oft nicht. Die Texte sind z.T. englisch (TASK-163 Profile-Texte), deutsche Übersetzungen inkonsistent.
**Strategische Empfehlung:**
- Glossar-Erstauftritt: erstes Auftauchen von "PEM" o.ä. koppelt mit `?`-Icon + Popup-Erklärung ("Post-Exertional Malaise — Zustandsverschlechterung nach Anstrengung").
- Konsequente deutsche Terminologie mit englischer Klammer-Bezeichnung.
- Anforderung: "Fachbegriffe (PEM, Spoon, Ceiling, Crash Probability) erscheinen mit Inline-Glossar-Tooltip; i18n-Texte sind konsistent eindeutscht mit englischer Klammer."

---

### ST-3 🟠 Löschen mit Sicherheitsnetz: Soft-Delete + Audit
**Screen/Flow:** Alle `showConfirm`-Lösch-Pfade
**Beobachtung:** Siehe MM-5 — strategisch betrachtet fehlt ein systematisches Recovery-Konzept, nicht nur einzelne Undo-Toasts.
**Strategische Empfehlung:**
- Soft-Delete-Pattern mit `deleted_at` Timestamp auf allen relevanten Entitäten.
- UI: Papierkorb-Tab in Settings, Restore mit Audit-Log-Eintrag.
- Backfill: Bestehende Datensätze unverändert lassen (kein Daten-Migrations-Risiko).
- Anforderung: "Lösch-Aktionen sind 30 Tage wiederherstellbar mit Audit-Log-Eintrag (wer, wann, woher wiederhergestellt)."

---

### ST-4 🟠 Konsistente Fehler-Taxonomie im gesamten UI
**Screen/Flow:** Alle `fetch()`-Pfade, alle Validierungen
**Beobachtung:** Fehlermeldungen variieren stark: native `alert`, `showPopup`, Status-Texte, Toasts. Manche zeigen Roh-JSON, manche Klartext. Keine zentrale Fehler-Engine.
**Strategische Empfehlung:**
- Single error-renderer (`KPT.toast(level, title, body, actions)`), der Toast vs. Modal vs. Inline-State unterscheidet.
- Backend sendet standardisierte `{ error_code, user_message, severity, suggested_action }` — Frontend mappt nur.
- Anforderung: "Alle Fehlermeldungen stammen aus einer einzigen Render-Komponente; native Dialoge sind verboten; Backend liefert standardisierte Fehlerobjekte."

---

### ST-5 🟢 Accessibility-Audit der bestehenden Modals & Forms
**Screen/Flow:** Alle Modals in `components/*`, alle Forms (Pacing, Export, Config)
**Beobachtung:** Erste Indikatoren (Custom Confirm, `role="dialog" aria-modal`, error-boundary vorhanden), aber keine systematische A11y-Validierung: Tab-Trap im Modal, Esc-Close, Focus-Restoration, aria-describedby für Hilfetexte, Color-Contrast bei `text-slate-500` auf `bg-slate-900` (≈4.0:1 — grenzwertig).
**Strategische Empfehlung:**
- Phase-1-A11y-Sweep: Tab-Trap, Esc-Close, Focus-Restoration für alle Modals.
- Phase-2: Color-Contrast-Review (WCAG AA 4.5:1 für Text, 3:1 für UI).
- Phase-3: Screenreader-Test (NVDA + VoiceOver) für Critical Flows (Onboarding, PIN, Checkin, Export).
- Anforderung: "Alle interaktiven Komponenten erfüllen WCAG 2.2 AA. Critical Flows sind mit Screenreadern getestet; Befunde dokumentiert und behoben."

---

### ST-6 🟢 Personalisierungs-Defaults: Adaptive Heuristik
**Screen/Flow:** Onboarding + Pacing-Profile
**Beobachtung:** Aktuell ist `healthy` Default, dann benutzergewählte Profile. Eine adaptive Logik (basierend auf Symptom-Score aus Checkins) könnte nach den ersten 7 Tagen einen sanften Profil-Wechsel anbieten — statt den User im falschen Profil zu lassen.
**Strategische Empfehlung:**
- Nach 7 Tagen: "Du nutzt seit einer Woche [Profil]. Basierend auf deinen Checkins sehen wir Hinweise auf [Profil-Klasse]. Möchtest du wechseln?" mit klarem CTA + Begründung.
- Anforderung: "Profil-Anpassung wird proaktiv vorgeschlagen, wenn die Datenlage es nahelegt — User behält immer die Entscheidung."

---

## Heuristik-Index

| # | Befund | Severity | Bereich |
|---|--------|----------|---------|
| QW-1 | Inkonsistente Confirm-Mechanik (native confirm/alert) | 🟠 | `config.html:1995`, `personal_dashboard.html:2894` |
| QW-2 | Leere Voucher-Eingabe schlägt still fehl | 🟠 | `onboarding.html:442` |
| QW-3 | Quick-Checkin: vage Fehlermeldungen | 🟠 | `personal_dashboard.html:3341-3344` |
| QW-4 | Default-Button bevorzugt Skip-Customize | 🟠 | `onboarding.html:236-242` |
| QW-5 | Time-Window-Parser verwirft still | 🟢 | `onboarding.html:662-671` |
| QW-6 | Pacing-Save-Fehler verschluckt | 🟢 | `onboarding.html:643-649` |
| QW-7 | Export-Modal ohne Outside-Click-Warnung | 🟢 | `components/export_modal.html:2` |
| QW-8 | Activity-Slot-Counter planabhängig veraltet | 🟢 | `onboarding.html:145` |
| MM-1 | Plan-Wechsel ohne Konsistenzgarantie | 🔴 | `onboarding.html:410-414` |
| MM-2 | Generische Fehlerausgabe zeigt interne Codes | 🔴 | `onboarding.html:978,982,990` |
| MM-3 | Voucher-Fehlertext schlecht differenziert | 🔴 | `onboarding.html:458-463` |
| MM-4 | Browser-Back verlässt Onboarding ungesichert | 🔴 | Onboarding global |
| MM-5 | Löschen ohne Undo/Papierkorb | 🔴 | alle delete-Flows |
| MM-6 | What-If-Simulator ohne Empty-State | 🟠 | `what_if_simulator.html` |
| MM-7 | Konflikt-Meldungen ohne Auflösungsanleitung | 🟠 | `personal_dashboard.html:2057` |
| MM-8 | Health-Profile-Default nicht chronisch-krankheitssensibel | 🟠 | `onboarding.html:124` |
| MM-9 | PIN-Lockout-Recovery fehlt | 🟢 | `pin_entry.html` |
| MM-10 | Export-Modal: ungültiges Datums-Range | 🟢 | `export_modal.html:20-23` |
| MM-11 | Timezone-Pre-Selection implizit | 🟢 | `export_modal.html:68` |
| ST-1 | Vollständige Onboarding-State-Persistenz | 🔴 | Onboarding global |
| ST-2 | Klare Sprache für Fachbegriffe | 🔴 | Cross-cutting |
| ST-3 | Löschen mit Sicherheitsnetz: Soft-Delete + Audit | 🟠 | alle delete-Flows |
| ST-4 | Konsistente Fehler-Taxonomie | 🟠 | Cross-cutting |
| ST-5 | Accessibility-Audit der Modals & Forms | 🟢 | Cross-cutting |
| ST-6 | Adaptive Profil-Personalisierung | 🟢 | Onboarding + Pacing |

---

## Annahmen / ungesichtete Bereiche

- **Microbreak-Komponente, Pem-Risk, Energy-Timeline** wurden nur über Template-Code (Größe/Aufbau) beurteilt, nicht durch interaktive Tests.
- **Mobile Navigation** (Bottom-Nav / FAB-Konflikte) wurde im Code-Reading erwähnt (DASH-689, FEAT-671), aber nicht in Live-Test nachvollzogen.
- **Backend-Validierungs-Antworten** (z. B. welche Fehler-Codes tatsächlich zurückkommen) basieren auf dem Frontend-Code; eine Backend-Inspektion war out-of-scope.
- **kpt-symptoms-app (mobile)** als Schwester-Projekt wurde im Repository gefunden (`VoiceCapture.kt`/`VoiceCapture.swift` — Module für Sprachaufnahme), aber nicht im Detail analysiert, da im aktuellen Workspace-Fokus nicht klar ist, ob es End-User-Onboarding exponiert.
- **A11y-Validierung** beruht auf Code-Inspektion (aria-Attribute, focus-States). Manuelles Screenreader-Testing war nicht möglich.
- **Sprache:** Diese Analyse folgt der Persona-Sprache Deutsch (Nutzer:in ist die Zielgruppe), die deutsche Übersetzungsschicht ist nicht Wort-für-Wort geprüft.

---

## Synthese-Empfehlung

Quick Wins (8) sind alle in 0.5–2 Personentagen umsetzbar und verbessern primär die Konsistenz, Klarheit und Recovery. Priorität: QW-1, QW-3, MM-1, MM-2, MM-4 → spürbare Hebel.

Mittelfristige Maßnahmen (11) betreffen Daten-Integrität, Konfliktbehandlung, Personalisierung — typischerweise 3–8 Tage pro Maßnahme. MM-5 (Soft-Delete) ist system-weit und sollte vor allen anderen destruktiven Flows adressiert werden.

Strategische Überarbeitung (6) sind Architektur-Themen — System-State-Persistenz, Fehler-Taxonomie, A11y. Sie sind Vor-Bedingungen für nachhaltige Qualitätssteigerung und benötigen je 1–3 Sprints.

