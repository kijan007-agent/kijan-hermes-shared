# Branch Offset Monitoring — Thresholds & Protocol

> Working tree vs hermes branch commit-count delta als Indikator für TASKS.md Validität.

## Pattern

Working tree HEAD vs hermes branch commit count delta zeigt, ob TASKS.md veraltet sein könnte.

```bash
# kpt-app-ciq: working tree vs hermes branch
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq log --oneline hermes..origin/hermes | wc -l
# → 28 commits ahead = TASKS.md veraltet

# Alternative: commit count delta
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq rev-list --count hermes..origin/hermes
```

## Thresholds

| Delta | Status | TASKS.md Validität | Aktion |
|-------|--------|-------------------|--------|
| 0 | ✓ Sync | Gültig | Normaler Workflow |
| 1-5 | ⚠️ Warning | Möglicherweise veraltet | TASKS.md mit git HEAD vergleichen |
| 6-10 | ⚠️⚠️ | Sicherlich veraltet | TASKS.md nicht als Source of Truth verwenden |
| >10 | 🔴 Kritisch | Ungültig | TASKS.md ignorieren, git log als einzige Quelle |

## Verification Protocol

1. **Delta prüfen:** `git rev-list --count <base>..<target>`
2. **Delta > 5:** TASKS.md mit git log HEAD vergleichen
3. **Delta > 10:** TASKS.md komplett ignorieren
4. **TASKS.md Claim ≠ Reality:** Line count check + content grep auf behauptete Features
5. **Branch-Offset dokumentieren:** Im Knowledge Hub unter "risk_patterns" eintragen

## Bekannte Offsets (2026-05-20)

| Submodule | Working Tree | hermes branch | Delta |
|-----------|-------------|---------------|-------|
| kpt-app-ciq | `fec8c9b` | `edb16cf` | 28 commits ahead |
| kpt-backend | — | `803d925` | ✓ synced |
| kpt-doc | — | `f8d0ec8` | ✓ synced |
