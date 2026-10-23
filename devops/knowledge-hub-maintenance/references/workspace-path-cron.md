# Cron Workspace Path Resolution

**VERIFIZIERT 2026-09-25 (live, Cron-Run #43):** In dieser Umgebung ist `/workspace` das korrekte
Dateisystem-Root — auch im Cron-Modus. `/home/jan/` existiert NICHT im Container.

## Regeln
- Dateizugriffe immer unter `/workspace/...` (z.B. `/workspace/.hermes/state.db`).
- Bei "nicht gefunden": zuerst mit `/workspace/...` suchen (glob/search_files), bevor der User gebeten wird, Pfade zu klären.
- Historischer Irrtum: ältere Runs/Skills empfahlen `/home/jan/` in Cron-Mode — das war ein Host-Pfad-Artefakt.
  Alle seit 2026-08 laufenden Cron-Jobs haben `/workspace/` erfolgreich genutzt (kijan-steuern, f3k-design, .hermes/*).
- Host-Pfad `/data/Github/` (Kijan-Produkt-Submodule) ist aus dem Container NICHT erreichbar
  → FALLBACK-EXTRACTED-Marker im Knowledge Hub dokumentiert das seit 2026-08-04.
