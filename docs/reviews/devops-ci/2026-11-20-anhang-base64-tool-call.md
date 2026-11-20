# Review: Anhang-Schleife — kein Inline-Base64 > ~4 kB im Tool-Call

Task: t_edbb0e12 (Follow-up zu t_1ddab3fc) · Datum: 2026-11-20 · Profil: devops

## Befund

Worker-Schritte, die eine Datei per `kanban_attach` an eine Kanban-Karte haengen,
uebergeben die Bytes als **base64 im Tool-Call-Argument**. Base64 blaesst um ~4/3
auf: ein 9-kB-Bericht sind ~11.6k Zeichen reines Tool-Output. Das liegt ueber den
Max-Output-Tokens des Modells.

Folgen (Laufprotokolle t_26ca3e9e, Analyse t_1ddab3fc):
- Lauf 61866: Crash `model hit max output tokens ... still truncated after 4
  continuation attempts` — der Tool-Call wurde **nie ausgefuehrt**.
- Lauf 62022: Schleife — Kontext 144.819 >= Kompressionsschwelle 131.072 bei
  Compression-Cooldown 890 s; der Anhang ging erst nach Stunden zufällig durch.

Der Fehler sitzt am Modell->Tool-Argument-Rand, **vor** jeder Dispatcher-Logik.
Ein Provider-Timeout/Fallback (t_26927ce8) hilft hier nicht.

## Umsetzung Regel 1 (geliefert)

Guidance in den beiden Skills, die jeder Worker/orchestrator geladen bekommt
(`kijan-hermes-shared`, Sync in die aktiven Profile via Skills-Sync-Job):

- `devops/kanban-worker/SKILL.md` — Abschnitt „Attachments: never inline base64
  above ~4 kB": <=3 kB ok; sonst commit+SHA-Referenz, `kanban_attach_url`, oder
  Repo-Pfad-Referenz. Nie dasselbe Base64 erneut generieren.
- `devops/kanban-orchestrator/SKILL.md` — Abschnitt „Card bodies must not require
  large inline attachments": Kartentexte schreiben Lieferung als commit+Referenz
  fest; echter Anhang nur per URL und in eigener Karte.

## Auftrag 2: Kann der Dispatcher grosse Anhang-Schritte vermeiden?

Untersucht in `hermes-agent` (Fork kijan007/hermes-agent):

- **Kein Flow-Guard an dieser Stelle.** Die Flow-Guard-Ausgabe im Worker-Prompt
  kommt aus der Kanban-Task-Schnittstelle, prueft Rollen/Abhaengigkeiten, aber
  nichts an Argumentgroessen. Ein grep nach `flow_guard`/`Flow guard` in den
  Python-Quellen findet keine Implementierung, die Tool-Argumente inspiziert.
- **Existierende Guardrails wirken woanders.** `agent/turn_preflight.py` und
  `agent/turn_recovery.py` regeln den *Kontext* (uncompressed-context-guardrail),
  nicht die Groesse eines einzelnen ausgehenden Tool-Arguments.
- **Wirksame Stelle waere `tools/kanban_tools.py`** (Handler von `kanban_attach`):
  ein harter Groessencheck auf `content_base64` (z. B. > 4 kB -> Fehler mit
  Hinweis auf `kanban_attach_url`/git-Referenz) wandelt die endlose Retry-Schleife
  in eine sofortige, lesbare Meldung. Schraenkt ein: weil die Truncation schon beim
  Generieren des Arguments passiert, sieht der Handler das Argument bei sehr
  grossen Dateien gar nicht mehr — der Check ist ein **Backstop**, keine
  Verhinderung.
- **Echte Verhinderung** muesste vor dem Modellschritt ansetzen (Task-Karten
  verbieten Anhang-Schritte fuer grosse Dateien). Das ist genau der
  Orchestrator-Abschnitt, der mit diesem Task geliefert wurde — wirksam, ohne
  Kern-Patch am Agent-Fork.

## Bewertung: Regel 1 reicht vorlaeufig

Begruendung:
1. Die Ursache ist ein Modell-Limit, kein Dispatcher-Bug. Verhindern kann ihn nur,
   was das Argument erst gar nicht erzeugen laesst — also Kartentext und
   Worker-Verhalten (Regel 1), nicht eine nachgelagerte Pruefung.
2. Ein Kern-Patch in `tools/kanban_tools.py` ist moeglich, aber ein Fork-Eingriff in
   die Agent-Software ausserhalb der KPT-Repos; er waere zusaetzliche Infrastruktur
   und braucht ein eigenes Gate. Als Folge-Karte sinnvoll (Backstop-Meldung), nicht
   als Voraussetzung.
3. Beide gelieferten Abschnitte sind in den Skills, die laut Skills-Sync in alle
   Worker-Profilefliessen; damit gilt die Regel prozessseitig fuer alle Profile,
   ohne dass jede SOUL einzeln angefasst wird.

## Empfohlene Folge

Optionale Karte: Groessen-Backstop in `kanban_attach` (Base64 > 4 kB -> Fehler mit
Handlungshinweis) im Fork kijan007/hermes-agent, inkl. Test in
`tests/tools/test_kanban_tools.py`.
