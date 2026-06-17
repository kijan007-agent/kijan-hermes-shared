# Multi-Product Setup

## Tenant-Isolation Pattern

Jedes Produkt bekommt einen eigenen tenant mit isolierten Ressourcen:

- **Kanban Board:** Separate Boards pro tenant
- **Git Worktree:** `/workspace/Github/{product}/` — isolierter Workspace
- **Telegram Channel:** `#team-{product}` — produkt-spezifischer Channel
- **Topics Directory:** `/workspace/topics/{product}/` — Input-Staging
- **Output Directory:** `/workspace/output/{product}/` — Task-Ausgabe

## Knowledge Hub

Location: `/workspace/.hermes/workflows/holistic-dev-workflow/knowledge-hub.md`

Speichert cross-produktive Erkenntnisse:
- Process insights und Lessons Learned
- Domain knowledge und Best Practices
- Technical patterns und wiederverwendbare Code-Snippets
- Risk patterns und bekannte Fallstricke

## Cross-Product Communication

- Knowledge Hub: geteilte insights über alle Produkte
- Status Report: produkt-agnostischer System-Health
- Skill Updates: wiederverwendbare patterns und Workflow-Improvements
