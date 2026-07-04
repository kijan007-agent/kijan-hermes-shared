---
name: task-claim-verification
description: Universal TASKS.md completion verification — file existence, stub detection, fabricated-complete classification.
---

# task-claim-verification

> Universal TASKS.md completion verification pattern.

## Trigger
- Vor Task-Start: Ist TASKS.md Claim noch valide?
- Nach Task-Ende: Claim korrekt?
- TASKS.md markiert Tasks als "complete", die nicht implementiert sind

## Steps
1. **Line-Count Check:** `wc -l < file` — unter 200 Zeilen = möglicher Stub
2. **Keyword Integration Check:** Greps nach Integrations-Keywords (z.B. "EnergyScreen" in EnergyScreen files)
3. **Git History Check:** `git log --diff-filter=D -- <file>` — file wurde commit-then-deleted?
4. **TASKS.md Claim vs Reality:** Lese TASK-claim, vergleiche mit existierender Code-Base
5. **WORKLOG Sync Check:** Letzter WORKLOG-Eintrag vs aktuelle Commits — >3 Tage gap = stale

## Fabricated-Complete Classification (see kijanpersonal-tracker/references/task-claim-verification-protocol.md)
| Level | Description |
|-------|-------------|
| Stale | Claim war true, Doc nicht aktualisiert |
| Overstated | Core existiert, Details fehlen |
| Stub | Gerüst, Features nicht implementiert |
| Fabricated | Claim ist komplett falsch |
| Deleted | File existierte, wurde absichtlich gelöscht |
| Disabled | File exists on disk but is commented-out/disabled in controller (see kijanpersonal-tracker for details) |

## Disabled Code Detection Pattern (2026-05-24 updated)
When a file exists on disk but is NOT wired up in the controller:
1. Check controller for commented-out instantiation: `grep -n 'DISABLED\\|//.*new.*ClassName' controller.mc`
2. Check if route still exists in ScreenFlowConfig: `grep ':routeName' ScreenFlowConfig.mc` — route may exist but screen disabled
3. Check if instantiation is in disabled block: look for `// if (screen == :routeName) { return new ClassName(); }`
4. Check if ScreenPageManager still adds it conditionally: `grep 'ClassName' ScreenPageManager.mc` — may have conditional add
5. If route exists but instantiation is commented → screen is registered but unreachable, NOT "missing"
6. Report as `⚠️ Disabled` not `❌ Missing` — the code exists, just not active
7. Check for related delegates: `grep 'DISABLED\\|//.*Delegate' controller.mc` — delegates may also be disabled
8. **NEW (2026-05-24)**: EnergyScreen instantiation is disabled at SFC lines 551-553 (`// if (screen == :energyScreen) { return new EnergyScreen(...) }`) AND delegate creation at lines 763-764 (`return null;`). Route still exists in ScreenFlowConfig but screen is unreachable. Classification: `⚠️ Disabled on disk` — 122 lines, intentionally simplified production version.

## Post-Wipe Reality (2026-06-07+)

All KijanPersonalTracker repos wiped (zero commits, zero remotes). TASKS.md and all source code are gone from version control.

**Current verification reality:**
- No code to verify against — only untracked disk artifacts survive (`kpt-doc/_specs/`, `_mockups/`, `/tmp/kpt-extract/source/`)
- TASKS.md claims are now purely speculative — pre-wipe planning intent only
- Classification of any Kijan task must start with: **REPO WIPE — no code exists to verify**
- Recovery requires user-provided backup or reconstruction from `kpt-doc/_specs/` specs
- **NOTE (2026-06-09):** Repos have been re-initialized with new commits. kpt-backend has 185 files (115 py), kpt-app-ciq has 324 files, kpt-doc has 715 files. TASKS.md in kpt-doc/_tasks/ still exists. Verification is now possible again against the re-initialized repos.

## Pre-Wipe Classification (historical — code no longer exists)
| Status | Criteria | Example |
|--------|----------|---------|
| ✅ Done | File exists, wired in controller, matches spec | ScreenFlowController overlay queue (TASK-100) |
| ⏳ Simplified | File exists, wired in, intentionally stripped down | EnergyScreen 122 lines (not 493) |
| ⚠️ Disabled on disk | File exists but commented-out in controller | EnergyScreen SFC:551-553,763-764 |
| ⚠️ Partial | Core impl present, missing pieces | Task-101: fireSignal validates, go() doesn't |
| ⚠️ Replaced | Full impl exists in history, replaced by simplified version | EnergyScreen: 493→122 lines |
| ❌ Missing | File never existed or fully deleted | DeltaInputScreen |
| 📋 Claimed | TASKS.md says done, disk disagrees | Document discrepancy |

## Cross-Product Relevance
- Alle Produkte mit TASKS.md (Kijan, kpt-backend, kpt-app-ciq)
- Universal anwendbar für alle produkt-übergreifende Tasks

### See also
- **`references/cron-status-audit-pattern.md`** — TASKS.md claims vs reality verification protocol, line-count regression detection, classification rules
- **`references/energy-screen-false-completion.md`** — Specific EnergyScreen case (493 claimed → 169 peak → 80 current)
- **`references/claimed-vs-verified-audit-protocol.md`** — Full step-by-step audit protocol with classification decision tree and known false completions table

## Never-Existing File Pattern (2026-05-23)
TASKS.md kann Tasks als "COMPLETED" markieren, deren Dateien NIE existiert haben:
- DeltaInputScreen: TASKS.md dokumentiert 417 Zeilen, file NEVER existed on disk
- Check: `find <repo> -name 'DeltaInputScreen*'` — nothing found
- Check: `git log --all --oneline -S 'DeltaInputScreen' -- '**/DeltaInputScreen*'` — nothing found
- Check: `git log --all --oneline --diff-filter=A -- '**/DeltaInputScreen*'` — nothing found
- If all checks negative: mark as "NEVER_CREATED" not "Stub" or "Deleted"
- This pattern occurs when docs are written before implementation begins
- **⚠️ 2026-06-08**: DeltaInputScreen was confirmed NEVER_CREATED in a fresh cron audit — TASKS.md claimed COMPLETED but the file was never written. Always run the full 3-check protocol before classifying.

## Line-Count Regression Pattern (2026-05-27)
TASKS.md claims a large file (e.g., 493 lines) but the actual max historical line count is much smaller:
- EnergyScreen: TASKS.md claims 493 lines, max historical = 169 lines at commit `c0fc0b1`
- The chart was implemented (c0fc0b1, 169 lines) then reverted to simpler version (80 lines)
- Check: `git log --all --oneline -- <file>` to find max line count
- Check: `git show <commit>:<file> | wc -l` at peak complexity commits
- If TASKS.md claim > max historical → mark as "OVERSTATED" not "Complete"
- Key: TASKS.md may reference combined file size or never-achieved spec, not actual implementation

## Submodule-Head-Lags-Remote Pattern (2026-06-08)
TASKS.md claims features as COMPLETED but the submodule working tree is stale:
1. `git -C <submodule> log --oneline feature -5` — check submodule HEAD
2. `git -C <submodule> log --oneline origin/feature -5` — check remote
3. If working tree HEAD < origin/feature HEAD: submodule has un-synced commits
4. The parent repo's submodule pointer may also be stale — check `git -C <parent> show <branch>:<submodule>`
5. When submodule working tree ≠ remote: TASKS.md claims may reference remote code, not disk code
6. **Always verify against layer 1 (working tree disk)**, not layer 3 (remote), when auditing TASKS.md
7. This is NOT a wipe — the code exists on remote, just not on disk. Classification: "⏳ Behind remote" not "❌ Missing"

## Simplified-Replacement Chain Detection (2026-06-02)
When a file was fully implemented then replaced by a simplified version:
1. `git merge-base --is-ancestor <full-commit> <simplified-commit>` → true = replacement chain
2. `git log --ancestry-path <full-commit>..<simplified-commit>` → shows the chain
3. Working tree reflects simplified version, NOT the original full impl
4. Classification: "⚠️ Replaced" not "Stub" or "Missing"
5. Key: `git merge-base --is-ancestor` is the definitive test — if false, the commits are unrelated
