# Kijan Personal Tracker — TASKS für Feature-Branch-Portierung

Quelle: prod-hotfix-bat (working) → Ziel: feature-Branch

---

## TASK-001: EnergyScreen — 24h Timeline-Chart mit Farbzonen

**Priority:** P0 (Blocking — Haupt-Feature)

**User Story:** Als Nutzer möchte ich eine visuelle Darstellung meines heutigen Spoon-Verlaufs über den Tag hinweg mit Farbzonen (0-10 rot, 10-20 gelb, 20-30 grün), gestrige Werte als zweite Linie und einen 7-Tage-Mittelwert mit Spannbreite.

**Status:** IN PROGRESS (Basis-Implementierung vorhanden, aber unvollständig)

### Anforderungen

#### A. Farbzonen-Hintergrund
- 0-10 = rotes Rechteck im Chart-Bereich
- 10-20 = gelbes Rechteck
- 20-30 = grünes Rechteck
- Zonen als horizontale Streifen im Diagramm-Bereich

#### B. Linien-Graph
1. **Heutige Linie:** Fett/grün — aktueller Tagesverlauf
2. **Gestrige Linie:** Hellgrau — gestriger Tagesverlauf
3. **7-Tage Mittelwert:** Blaue gestrichelte Linie horizontal
4. **7-Tage Spannbreite:** Transparentes Band (Min-Max) dahinter als Fill

#### C. Spoon-Icon Visualisierung
- spoon-green.png: Value >= 20
- spoon-yellow.png: Value >= 10
- spoon-red.png: Value < 10
- Icon auf der Chart-Linie an der aktuellen Position platzieren

#### D. Wert-Eingabeoption
- Touch/Buttons zum Erfassen eines neuen Wertes
- Zeigt aktuellen Wert + Differenz zum Vorgänger
- Eingabe-Bestätigung mit "Set" und "Skip"

### Abhängigkeiten
- TASK-002 (Spoon-Drawables)
- TASK-003 (StatusCheckManager Integration)

---

## TASK-002: Spoon-Drawables aus Hotfix portieren

**Priority:** P0 (Required for TASK-001)

**Problem:** Feature-Branch hat drawables.xml entfernt: SpoonGreen, SpoonYellow, SpoonRed sind nicht mehr definiert.

### Anforderungen
1. drawables.xml erweitern mit SpoonGreen/SpoonYellow/SpoonRed Bitmaps
2. PNG-Dateien aus Hotfix nach Feature kopieren
3. EnergyDrawable._getSpoonBitmap() reintegrieren
4. EnergyScreen: Spoon-Icon auf Chart-Linie platzieren

---

## TASK-003: StatusCheckManager — Datenquelle für Chart

**Priority:** P1

**Status:** IN PROGRESS

### Anforderungen
1. `getDailyConsumption(dayOffset)` → Spoon-Werte für gestrige Daten
2. `getLastNChecks(n)` → Status-Checks für Chart-Punkte
3. Zeitstempel-Korrelation mit Stunden-Interpolation
4. `isBadDayActive()` + `getDailyModifier()` für Bad-Day-Logik

---

## TASK-004: PacingSpoonsCheckinView — Wert-Eingabe UI

**Priority:** P1

### Anforderungen
1. Spoon-Modus: +/- 1 Spoon, 0-25 Bereich
2. Farbcodierung des aktuellen Werts (rot/gelb/grün)
3. History-Bars für gestern und Vorgestern
4. Bestätigungsdialog mit "Set" und "Skip"
5. Backend-POST zu `/d/{deviceId}/api/checkin`
6. 1h-Cooldown beim Wiederzugriff

---

## TASK-005: DashboardManager — Dashboard-Öffnung fixen

**Priority:** P2

### Problem
Feature: DashboardManager ist kürzer, fehlt openDashboard() mit PhoneConnectivity-Check

### Änderungen die portiert werden müssen
1. `fetchAndStorePin()` — PIN-Workflow
2. `openDashboard()` mit PhoneConnectivity-Check
3. `openActivityComment()` mit edit-token fetch chain
4. `onEditTokenResponse()` mit 404-Retry-Logik
5. `_showPhoneNotConnected()` Popup via ScreenFlowController

---

## TASK-006: ScreenFlowController — Popup-Flows reparieren

**Priority:** P0 (Critical — UX-Problem #1)

**Problem im Feature-Branch:**
- Überlagernde Popups (multiple screens on stack)
- Falsche Navigation nach Bestätigung/Ablehnung
- Stale View Callbacks nach Popup-Aktion

### Fixes aus Hotfix
1. View Validity Guard (mViewId + isViewValid)
2. Popup-Stack Management (setActivePopup, clearPopupStack, popPopup)
3. Callback-Validierung vor Ausführung

---

## TASK-007: InitScreens — Screen-Integration

**Priority:** P1

### Problem
EnergyScreen (ScreenRenderer) muss in InitScreens.mc korrekt registriert werden

### Anforderungen
1. `EnergyScreen` zu mScreens in InitScreens hinzufügen (wenn unit_mode != "disabled")
2. ScreenRenderer-Konfiguration prüfen
3. onUpdate() und onPostDraw() korrekt registrieren
4. EnergyScreen bei unit_mode change aktivieren/deaktivieren

---

## TASK-008 bis TASK-023

Siehe vollständige TASKS.md in `kpt-doc/_tasks/TASKS.md`

---

# UX-Probleme im Feature-Branch (aus Hotfix analysiert)

## Problem #1: Überlagernde Popups → FIX: TASK-006
## Problem #2: Falsche Flows nach Popup-Aktion → FIX: TASK-006
## Problem #3: EnergyScreen wird nicht angezeigt → FIX: TASK-007
## Problem #4: Spoon-Icons fehlen → FIX: TASK-002
## Problem #5: Chart-Interpolation defekt → FIX: TASK-001
## Problem #6: Farbzonen nicht implementiert → FIX: TASK-001
## Problem #7: Wert-Eingabe unvollständig → FIX: TASK-004
## Problem #8: ActivityEventQueue reduziert → ANALYSIS: TASK-008
