# Kanban-Board-Pattern für Kijan Task-Workflow

## Kontext
User möchte Tasks als Kanban-Board verwaltet haben:
- Board in `kpt-doc/_tasks/TASKS-CI-KANBAN.md` als Markdown
- Jede Task → eigener Branch (z.B. `feature/task-be-01`)
- Reihenfolge: Backend P0→P1→P2 → Connect IQ P0→P1→P2
- Nach jedem Task: Telegram Report an `telegram:Jan K`
- Integration nur in `feature` (nicht dev/prod)
- Board-URL für Telegram: `MEDIA:/workspace/Github/KijanPersonalTracker-hermes/kpt-doc/_tasks/TASKS-CI-KANBAN.md`

## Erzeugung des Boards
1. Alle Tasks mit Priorität, Status, Branch-Name, Notes sammeln
2. Markdown-Tabelle je Prioritätsstufe (P0/P1/P2)
3. In `kpt-doc/_tasks/TASKS-CI-KANBAN.md` schreiben
4. Telegram Report: Board als MEDIA-Datei senden

## Board-Format
```markdown
# Kijan CI/CD Kanban Board — Feature Branch Workflow

**Reihenfolge:** Backend P0→P1→P2 → CIQ P0→P1→P2 → Dashboard (cross-cutting)
**Workflow:** Feature Branch → Test → Merge in feature
**Report:** Telegram nach jedem Task
**Multi-Perspektive:** Patient, Arzt, UI/UX, Data Specialist, Data Engineer, Systemarchitekt, Softwareentwickler, PM, Projektmanager, Stakeholder

---

## 🔴 BACKEND P0

| # | Task | Status | Branch | Notes |
|---|------|--------|--------|-------|
| BE-01 | ... | ✅ DONE | feature/task-be-01 | ... |
| BE-02 | ... | 🔄 IN PROGRESS | feature/task-be-02 | ... |

---

## 📋 TELEMETRY REPORT

### TASK-{ID} Report ✅ DONE
- **Branch:** feature/task-{id}
- **Files changed:** ...
- **Finding:** ...
- **Tests:** ...
- **Merge:** In feature gemergt
```

## Pitfall
- Kein externes Board (Trello, GitHub Projects etc.) — alles lokal in Markdown
- Board muss nach jedem Task aktualisiert werden (Status-Updates)
- Telegram Report muss immer Board-Pfad enthalten