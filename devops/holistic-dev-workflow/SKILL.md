---
name: holistic-dev-workflow
description: "Orchestriert den kompletten Entwicklungsprozess von Themen-Erfassung bis Deploy/Rollout über Multi-Produkt-Szenarien mit tenant-basierter Isolation und automatischer Integration wissenschaftlicher Berater."
version: 1.0.0
tags: [kanban, multi-agent, workflow, orchestration, multi-product, scientific-advisors]
---

# Holistic Dev Workflow

Orchestriert den kompletten Entwicklungsprozess von Themen-Erfassung bis Deploy/Rollout über Multi-Produkt-Szenarien mit tenant-basierter Isolation und automatischer Integration wissenschaftlicher Berater.

## Workflow-Phasen

1. Input Intake — Themen-Eingabe via Telegram, Datei, Todo, Konsole
2. Research — Automatischer Web/Domain-RAG mit wissenschaftlichen Beratern
3. Product Management — INVEST User Stories mit fachspezifischer Validierung
4. UX/UI Design — Wireframes, Accessibility (WCAG 2.1 AA)
5. Architecture — ADR-Template, Ressourcen-aware Tech-Stack
6. Implementation — Subagent-Driven Development mit 2-Stufen-Review
7. Testing — Unit, Integration, Security, Performance Tests
8. Approval + Deploy — Approval Package, Git-Workflow, Canary/Blue-Green Rollout

## Multi-Produkt Architektur

- Tenant-Isolation pro Produkt (Kanban, Git, Telegram)
- Knowledge Hub: Cross-Produkt-Wissensaustausch
- Status Reporter: 3h-Zustandsbericht
- Knowledge Aggregator: 6h cross-produktive Wissensakkumulation

## Scientific Advisor Triggers

- Medizinisch: symptom, disease, diagnosis → medizinischer-berater
- Psychologisch: mood, stress, anxiety → psychologischer-berater
- Rechtlich: legal, compliance, gdpr → expanding legal advisor
- Naturwissenschaftlich: experiment, research → expanding science advisor

## Setup-Referenzen

- references/multi-product-setup.md: Multi-Produkt Tenant-Setup
- references/scientific-advisor-trigger-matrix.md: Domain-spezifische Berater-Trigger
- **`references/kijan-frontend-report-schedule.md`** — Kijan Frontend Report-Zeiten: Morgenbriefing 07:30, Task-Übersicht alle 90min, Status 12:30 + 18:00
- **`references/scientific-advisor-trigger-matrix.md`** — Domain-spezifische Berater-Trigger
- **`references/drift-direction-reversal.md`** — When submodule offset numbers are identical between audits but direction flipped (AHEAD→BEHIND), report both direction + reference branch
- **`references/knowledge-hub-dual-read-pattern.md`** — Re-read KNOWLEDGE-HUB.md between section patches; line numbers shift
- holistic-dev-workflow-status-report: 3h-Zustandsbericht (cron: kijan-frontend-morning-briefing + kijan-frontend-task-overview + kijan-frontend-status-1230 + kijan-frontend-status-1800)

| Bericht | Zeit | Inhalt | Format |
|---------|------|--------|--------|
| Morgenbriefing | 07:30 | Facts, RCA, Mockups, Fragen/Blocker | 🌅 + Fakten + Blocker + Mockups + Nächste Schritte |
| Task-Übersicht | alle 90m | Done / In Progress / Next | 📊 + ✅ / 🔄 / ⏭️ |
| Statusbericht | 12:30 | Gesamtfortschritt, Dateien, Blocker | 📊 + Status % + Dateien + Blocker |
| Statusbericht | 18:00 | Gesamtfortschritt, Dateien, Blocker, Erfüllt | 📊 + Status % + Dateien + Blocker + Erfüllt |
| Nacht-Zusammenfassung | 07:30 (folgender Tag) | Zusammenfassung Nacht + Fortschritt | Im Morgenbriefing enthalten |

**Nacht:** Keine Berichte zwischen 22:00 und 07:30. Der 07:30 Morgenbericht enthält auch die Nacht-Zusammenfassung.

### Report-Format

**Morgenbriefing (07:30):**
```
🌅 Morgenbriefing - [Datum]

📊 Fakten:
  - Backend: [Status]
  - Mobile: [Status]
  - Web: [Status]

🔴 Blocker/Fragen:
  - [Fragen die geklärt werden müssen]

📐 Mockups:
  - [Verfügbare Mockups]

📋 Nächste Schritte:
  - [Heute zu erledigende Aufgaben]
```

**Task-Übersicht (alle 90min):**
```
📊 [Zeit] - Task-Übersicht

✅ Done:
  - [Aufgaben]

🔄 In Progress:
  - [Aufgaben]

⏭️ Next:
  - [Aufgaben]
```

**Statusbericht (12:30, 18:00):**
```
📊 Statusbericht [Zeit] - [Datum]

📊 Gesamtstatus: [Progress %]

📁 Dateien:
  - [Neue/Geänderte Dateien]

🔴 Blocker:
  - [Falls vorhanden]
```

## Pitfalls

- Always call tenant parameter with kanban_create
- Git-Sync vor jeder Aufgabe
- Bare Submodule beachten (kpt-app-ciq)
- **Branch-Offset-Monitoring:** Working tree vs hermes branch commit-count delta prüfen — delta > 10 = WARNING, delta > 50 = HIGH (TASKS.md stark veraltet), delta > 100 = CRITICAL (TASKS.md komplett unbrauchbar). Siehe `hermes-branch-watcher/references/branch-offset-monitoring.md`.
- **Knowledge Hub Self-Verification:** Knowledge Hub selbst kann Duplicates, falsche Skill-Claims, und stale Offsets enthalten. Vor jeder Nutzung: Skill-Existenz via filesystem check verifizieren, nicht Trust.
- **Post-Sync Drift Pattern:** Nach origin/dev sync werden Submodule-Offsets sofort wieder aufgebaut (beobachtet: 1→20, 1→14, 1→11). Sync-Waves sind nur temporär — nie als "erledigt" markieren.
- **4-Datenbank-Migration-Stack:** kpt-backend verwendet 4 separate alembic stacks (activity/admin/health/projects) in einem Repo. Für multi-domain projects: create `alembic_<domain>/` per domain, never share one alembic config across domains. Alembic Total: 39 migrations (17+12+7+3). alembic/ und i18n/ Verzeichnisse NICHT auf Disk — nach alembic_activity/ und translations/ verschoben.
- **Alembic Idempotent (NEU):** check column existence before ALTER TABLE — prevents migration failures on re-run. Pattern: `if not column_exists(conn, 'table', 'column'):` → ALTER TABLE. PITFALL: running migrations twice on different env fails without existence checks.
- **Alembic Partition Reordering (NEU):** when reordering partitions, handle migration errors gracefully, drop → recreate → validate. PITFALL: FK constraints must be temporarily disabled.
- **Alembic Rename Table (NEU):** safe table rename with cascade handling. PITFALL: `op.rename_table()` does NOT auto-update FK constraints — manual updates needed.
- **kanban.db often empty** — do not assume kanban board data exists; verify before relying on it
- **KNOWLEDGE-HUB.md pipe-inconsistency** — The file uses 3 different pipe counts (5, 6, sometimes 9) for table rows. Block-level string-replace WILL FAIL. Always use per-line keyword replacement (find line by content, replace that line). Verify no old timestamps remain after update.
- **Knowledge Hub status line fragility (NEU 2026-06-08):** After patching one status line in a section, the file content shifts — the `old_string` for the NEXT patch no longer matches. **Always re-read the file between patches in the same section.** Do NOT batch multiple patches on status lines.
- **replace_all danger (NEU 2026-06-08):** Entries like kpt-backend WARNING appear in BOTH risk_patterns table AND submodule status summary. `replace_all=True` removes from unintended sections. **Never use replace_all on entries that appear in multiple sections.**
- **File Count Staleness (NEU 2026-06-03):** File counts in KNOWLEDGE-HUB.md go stale because: (1) counting methodology changes (alembic env.py excluded from py count: 109→102), (2) file categorization corrections (.mc/.xml reclassified: 169→241), (3) recursive find vs manual count discrepancies (kpt-doc 504→480, MEMORY 188→187). **Always verify with fresh `find` or `tree` counts before updating Knowledge Hub — never trust previous Knowledge Hub file counts.** Mark corrections explicitly as `**CHANGED** (old→new — reason)`.
- **Header/Footer Timestamp Convention (NEU 2026-06-08):** Header "Stand" == Footer "Letzte Änderung". "Nächste Aktualisierung" = +6h. Verify: `header_ts == footer_ts` before commit.
- **Drift Direction Reversal (NEU 2026-06-09):** When reporting submodule offsets, always include direction (AHEAD/BEHIND) + reference branch. A count of "13" means opposite things as AHEAD vs BEHIND. kpt-backend: 13 AHEAD→13 BEHIND vs origin/dev. kpt-app-ciq: 0→120 AHEAD vs hermes. NEVER report just the number.
- **KNOWLEDGE-HUB Dual-Read Pattern (NEU 2026-06-09):** When updating KNOWLEDGE-HUB.md across multiple sections (status table → risk patterns → divergence analysis → TBD), re-read the full file between each section's patches. Line numbers shift after every patch. Patching one section without re-reading will break the next section's old_string.

## Knowledge Hub Integration

- KNOWLEDGE-HUB.md (6h cron update) — cross-product knowledge aggregation
- **`references/branch-offset-thresholds.md`** — delta thresholds und Verification Protocol
- **`references/knowledge-hub-update-workflow.md`** — Knowledge Hub Aktualisierungs-Workflow (cron audit → cross-product analysis → skill creation → hub update). **Updated 2026-06-08: added status-line fragility, replace_all danger on multi-section entries, header/footer timestamp convention, kpt-backend SYNCED (102 py), kpt-app-ciq 324 files, kpt-doc 715 files, 3 ARCHITECTURE DOCS.**
- **`references/knowledge-hub-verification-protocol.md`** — Knowledge Hub Self-Verification: Duplicates, false claims, stale data detection — **Updated 2026-06-08: ARCHITECTURE DOCS pattern, resolved states (kpt-backend SYNCED, kpt-app-ciq SYNCED, kpt-doc SYNCED).**
- **`references/knowledge-hub-file-counting.md`** — File counting protocol and stale count prevention
- **`references/knowledge-hub-status-line-fragility.md`** — After patching one status line, re-read before patching next. `old_string` shifts. Never batch patches on status lines.
- **`references/multi-database-migration-stack.md`** — Multi-domain repos: separate alembic config per domain
- **`references/post-sync-drift-pattern.md`** — Submodule drift after origin/dev sync (temporary, not permanent)
- **`energy-screen-audit`** und **`task-claim-verification`** existieren jetzt als Skills (2026-05-21) — vorher nur Knowledge-Einträge. Beide sind produkt-übergreifend: `task-claim-verification` gilt für alle TASKS.md-Claims, `energy-screen-audit` für alle Connect IQ UI-Verifizierung.