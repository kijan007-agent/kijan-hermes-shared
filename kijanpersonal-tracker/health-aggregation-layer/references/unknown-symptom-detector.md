# UnknownSymptomDetector — Spezifikation

> 3-Phasen-Pipeline: Erkennung → Modellerweiterung → Realisierung

## Problem

Bearable CSV-Export enthält beliebige vom Benutzer definierte Symptomnamen, die in Kijan nicht vordefiniert sind. Ohne Erkennung würden diese Daten verloren gehen oder manuell angelegt werden.

## Architektur: 3-Phasen-Pipeline

```
Phase 1: DETECTION (automatisch)
    → Exact match + Fuzzy-Match + Semantik-Analyse + Body Location Extraction
    → Output: known=True/False, category_hint, suggestions, body_locations

Phase 2: MODEL-EXPANSION (KI-gestützt)
    → Clustering ähnlicher unbekannter Symptome
    → KI-Klassifizierung (Phi-4-mini für komplexe Symptome)
    → Vorschlagserzeugung für neue Definitionen

Phase 3: REALIZATION (User-Review → Auto-Commit)
    → User-Review-Interface (API/CLI/Web)
    → Auto-Commit: neue SymptomDefinitionen + SymptomImportMappings
    → Status-Machine: pending → analyzed → reviewed → (created | mapped | skipped)
```

## UnknownSymptomQueue

Temporäre Queue während Import mit Status:
- `pending` — noch nicht analysiert
- `analyzed` — Detection + Semantik abgeschlossen
- `reviewed` — User hat über Vorschlag entschieden
- `resolved` — Mapping oder neue Definition erstellt

## Test-Szenarien

| ID | Input | Expected |
|----|-------|----------|
| USD-TST-001 | "Headache" | known=True, confidence=1.0 |
| USD-TST-002 | "Heahde" (Typo) | known=True, confidence=0.85, suggestions=["headache"] |
| USD-TST-003 | "Brain zaps" | known=False, category_hint=neuro, auto_create_suggestion |
| USD-TST-004 | "Tingling in left hand" | known=False, category_hint=neuro, body_locations=[arm] |
| USD-TST-005 | Cluster: "Tingling in left hand" + "Tingling in right hand" | 1 Cluster, auto_create: "Tingling" |
| USD-TST-006 | "Rage attacks" | known=False, category_hint=mood, auto_create_suggestion |

## Import-Flow mit UnknownDetection

```
1. Zeile parsen (date, time, category, detail, rating, notes)
2. category → Kijan entity type
3. detail (Symptom-Name):
   a. UnknownSymptomDetector.detect_unknown(detail, user_id)
      → known=True: direct mapping
      → known=False: add to unknown_queue
4. Alle Zeilen verarbeitet?
   → Ja: UnknownSymptomHandler.process_queue(unknown_queue)
      a. ModelExpansionService.analyze_unknown() → ExpansionReport
      b. RealizationService.present_review() → User-Review
      c. RealizationService.auto_commit() → neue Definitions + Mappings
      d. Import mit Mappings neu starten
5. Report: {imported, skipped, unknown_created, unknown_mapped, unknown_skipped}
```
