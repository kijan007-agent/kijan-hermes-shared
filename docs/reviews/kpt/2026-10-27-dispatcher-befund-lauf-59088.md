# Review: Dispatcher-Befund Lauf 59088 — Heartbeat-Sturm, Runtime-Caps, Quota-gate-Flapping

- Task: t_9d2cdb94 ([Team-Klärung], scrummaster)
- Datum: 2026-10-27
- Datenbasis: /workspace/.hermes/kanban.db (task_events, task_runs, tasks), Logs /workspace/logs/
- Ausgangsbefund: Lauf 59088 (Task t_a6fcd671), Analyse in Lauf/Kommentar t_26ca3e9e

## 1. Befund-Recap

1. **Heartbeat-Sturm** — Worker pid 750488 feuerte 151 Heartbeats in ~1,2 s (~123/s) direkt
   nach dem Spawn. Die frischen Heartbeats hielten den Lauf im Dispatcher "lebendig", obwohl
   der Worker faktisch keinen Fortschritt machte (Provider down). Folge: kein Stale-Reclaim,
   der Lauf hing 151 min bis zu einem manuellen Reclaim (20:10:11).
2. **Kein Runtime-Cap** — Lauf 59088 hatte `max_runtime_seconds` leer; es gab keine
   automatische Obergrenze. Die neu geschnittenen Folge-Tasks (t_43e1ba4a → t_7d380ff0 →
   t_c7834fff) tragen jetzt 1h-Caps.
3. **Quota-gate-Flapping** — nach dem Reclaim flapperte t_a6fcd671 ~3 Tage
   (30× SCHEDULED/UNBLOCK, 1792789827 → 1793030204) zwischen "Provider-Quota erschöpft"
   (TimeoutError / Connection refused / HTTP 503: nodes faex,aimax,hx unreachable) und
   "Quota wieder verfügbar", ohne dass je ein neuer Worker gestartet wurde.

## 2. Zusatzbefund aus der DB-Analyse (korrigiert/vertieft)

Der Kern des Problems war **nicht** (nur) das Gate-Flapping. Die 30 Unblocks führten
**nie** zu einem Spawn. Ursache: strikte Priority-Reihenfolge bei begrenzter Lane-Kapazität.

- Konfiguration: `max_in_progress = 12` (global), `max_in_progress_per_profile = 5`.
- Ziel-Task t_a6fcd671: Priority 175.
- Zu **jedem** der 30 Unblock-Zeitpunkte enthielt die Ready-Lane **≥ 12 Tasks mit
  Priority > 175** (gemessen: 25–308 Tasks mit prio > 175, 12 mit prio == 175).
- Ergebnis: der Task war in der Ready-Lane, wurde aber nie ausgewählt → kein Spawn,
  30 Zyklen SCHEDULED → UNBLOCK → SCHEDULED.
- Beleg der Prioritätsordnung im Dispatcher: Auswahl nach `priority DESC` (Basis
  `kpt`/`kijan-hermes-shared`); der Claim-Pfad filtert die Lane über die
  Kapazitätsgrenze, bevor ein Task gespawnt wird.

Damit erklärt sich der Eindruck "der Dispatcher reagiert nicht": das Quota-Gate war
korrekt und hat den Task bewusst zurückgehalten (Provider down), und die
Prioritäts-Aushungerung verhinderte zusätzlich jeden Wiedereinstieg.

## 3. Entscheidungen (Team-Klärung, scrummaster)

### Frage 1 — Wer behebt die clientseitige Heartbeat-Rate-Limitierung?
**Entscheidung: software-development** (Folgekarte `t_89e4977f`).
- Mindestens 30 s Abstand zwischen zwei Heartbeat-Writes; Writes innerhalb des Fensters
  werden verworfen (Dedupe, kein Stauen).
- Referenz: Commit `bc31ee5cf8` "bridge worker runtime activity to board heartbeat" —
  dort ist der Tight-Loop entstanden.

### Frage 2 — Heartbeats als Stale-Signal + Default-Runtime-Caps?
**Entscheidung: ja, beides** (Folgekarte `t_162f3992`, assignee `architect`).
- **Default-Runtime-Cap:** Tasks ohne explizites `max_runtime_seconds` bekommen
  dispatcherseitig 14400 s (4 h). Explizite Werte (auch größer) bleiben erlaubt.
- **Sturm-Erkennung:** > 10 Heartbeats/min in einem gleitenden Fenster ⇒ die
  überschüssigen Heartbeats zählen nicht mehr als Lebenszeichen; der Task wird wie
  ohne Heartbeat behandelt, `dispatch_stale_timeout_seconds` greift wieder.
- Beide Werte werden als Konfigurationsschlüssel geführt, nicht hart verdrahtet.

### Frage 3 — Quota-gate-Flapping abfedern?
**Entscheidung: Hysterese + Eskalation** (Folgekarte `t_0dbdb378`, assignee `devops`,
  betrifft `/workspace/.hermes/scripts/autounblock.py`).
- **Nur nach stabiler Freigabe re-dispatchen:** Entblocken erst nach 3 aufeinanderfolgenden
  OK-Proben im Abstand von je ≥ 10 min.
- **Eskalation:** nach 10 Flaps (block→unblock-Zyklen) innerhalb von 24 h wird das Gate
  für den Task geschlossen und dauerhaft mit `needs_input` blockiert statt endlos zu
  flappern.
- **Fairness (neu, an architect):** die Prioritäts-Aushungerung aus §2 muss mitgedacht
  werden (z. B. altersbasierter Priority-Boost), sonst bleibt der Task trotz repariertem
  Gate liegen.

## 4. Folgekarten

| Karte | Assignee | Inhalt |
|---|---|---|
| `t_89e4977f` | software-development | Heartbeat-Rate-Limit clientseitig (30 s, Dedupe) |
| `t_162f3992` | architect | Default-Cap 4 h + Heartbeat-Sturm als Stale-Signal |
| `t_0dbdb378` | devops | autounblock: Hysterese (3 stabile OK-Proben) + Eskalation nach 10 Flaps |

Alle drei Karten übernehmen die Entscheidungen aus §3 im Karten-Body, damit sie ohne
Sibling-Kontext umsetzbar sind.

## 5. Verifikation

- `python3`-Analyse über `/workspace/.hermes/kanban.db`: Rekonstruktion der Ready-Lane
  aus `task_events` (promoted/unblocked/reclaimed → ready, claimed/scheduled/blocked/
  completed/archived → raus), Auswertung je Unblock-Zeitpunkt gegen `tasks.priority`.
- Gegenprobe: aktueller Ready-Bestand `status='ready'` → 45 Tasks, davon nur 2 mit
  `priority > 175` (Lane ist inzwischen leer; die Aushungerung warfenzyklus-bedingt).
- 30 Unblocks von t_a6fcd671 im Fenster 1792789827–1793030204, 0 Spawns.

## 6. Offen / Risiko

- Die Default-Cap-Entscheidung (4 h) ist eine Betriebsentscheidung des Teams, kein
  Produkt- oder Rechts-Thema — daher keine Eskalation an Jan nötig.
- Die Fairness-Korrektur (Prioritäts-Boost) ist bewusst als offene Architekturfrage in
  `t_162f3992` hinterlegt und nicht eigenmächtig entschieden.
