# Knowledge Hub Self-Verification Protocol

> Knowledge Hub kann falsche Claims enthalten — selbst es ist nicht die Source of Truth.

## Known Failure Modes (2026-05-22)

### Duplicate Entries
- `hermes-branch-watcher` doppelt in tool_recommendations
- `hermes-branch-watcher` doppelt in skill-registry
- **Detection:** Grep für Skill-Namen, alle Vorkommen zählen

### False Skill Claims
- `submodule-divergence-check` als Skill gelistet, existiert NICHT auf Disk
- `branch-offset-monitoring` als Skill gelistet, existiert NICHT auf Disk
- **Detection:** `ls ~/.hermes/skills/<name>/SKILL.md` für jeden gelisteten Skill
- Bekannte nicht-existente Skills: `submodule-divergence-check`, `branch-offset-monitoring`
- Bekannte existierende Skills: `energy-screen-audit`, `task-claim-verification`

### Stale Data
- **kpt-backend:** SYNCED vs hermes (0 unmerged), 12 ahead vs origin/dev — HEAD c74006f — health_aggregation.py committed — **102 py files**
- **kpt-app-ciq:** SYNCED vs hermes (0 unmerged), 9 behind origin/dev (DRIFT) — HEAD 174996a — **324 total files**
- **kpt-doc:** SYNCED vs hermes (0 unmerged), 71 behind origin/dev — HEAD 2f31d17 — **715 total files** (325 MEMORY + 3 SPEC)
- **kanban.db:** LEER — Board-Daten fehlen, kanban-cli nicht funktional
- **Alembic count:** 39 total (activity:17, admin:12, health:7, projects:3) — NOT 43
- Timestamps müssen mit Cron-Job Sync halten
- **Detection:** Compare timestamp with `date -u`

### ARCHITECTURE DOCS Pattern (2026-06-08)
3 new root-level architecture docs in KijanPersonalTracker-hermes:
- ARCHITECTURE_DOCUMENTATION_INDEX.md (8.5KB)
- ARCHITECTURE_QUICK_REFERENCE.md (8.5KB)
- ARCHITECTURE_REVIEW_COMPREHENSIVE.md (30.8KB)
- **Verification:** Check git log for non-standard .md files at repo root

## Verification Checklist
1. Alle Skill-Namen in SKILL-Registry → existiert auf Disk?
2. Alle Skill-Namen in tool_recommendations → existiert auf Disk?
3. Branch-Offsets → aktuell gemessen?
4. Duplicate-Einträge → bereinigt?
5. Timestamp → < 6h alt?
6. Referenzierte reference-files → existieren?
7. **Resolved CRITICAL state:** Nach Status-Change von CRITICAL → RESOLVED:
   - Kein "CRITICAL" in Zeilen mit dem Produkt-Namen mehr
   - Kein alter Offset-Wert als standalone Zahl
   - Emojis konsistent (🔴 → ✅)
   - Richtung korrekt (168→0, nicht 0→0)
   - **Verifikation:** `grep` für "CRITICAL" UND alte Offset-Werte separat, nicht kombiniert
8. **Status-Line Fragility (2026-06-08):** Nach jedem Patch in einem Abschnitt: Datei neu lesen. `old_string` für nächste Zeile ist stale. **Nie mehrere Patches auf Status-Zahlen im selben Abschnitt batchen.**
9. **Header/Footer Timestamp Check (2026-06-08):** Header "Stand" == Footer "Letzte Änderung". "Nächste Aktualisierung" ≠ current (+6h). Verify: `header_ts == footer_ts`.
10. **File Count Verification (2026-06-03):** Vor jeder Update: `find <repo>/ -type f | wc -l` pro Produkt — nie vorherige Counts vertrauen.
