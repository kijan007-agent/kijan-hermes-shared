# Branch Offset Monitoring

> Monitor working tree vs hermes branch commit-count delta.

## Thresholds
| Delta | Level | Action |
|-------|-------|--------|
| 0-10 | GREEN | Normal |
| 11-50 | WARNING | TASKS.md may be stale |
| 51-100 | RED | TASKS.md unreliable |
| 101+ | CRITICAL | TASKS.md completely outdated |

## Commands
```
git rev-list --count WORKING_TREE_HEAD..hermes
git log --oneline origin/dev..HEAD  # unmerged commits
```

## Real-World Examples
- kpt-app-ciq (2026-05-22): 168 → **739 commits in ~7h** → CRITICAL. TASKS.md totally unreliable. Offset explosion pattern: rapid merge activity can create 500+ commit deltas rapidly.
- kpt-backend (2026-05-22): origin/dev ahead by **39 commits** (not 3 as previously reported). Always check BOTH directions: `rev-list --count origin/dev..dev` AND `rev-list --count dev..origin/dev`.
- kpt-doc: 71 commits hermes ahead → dual-branch pattern (dev=docs, hermes=spec), no merge needed.

## Unmerged Count Staleness Warning (2026-06-01)
**PITFALL:** Previous KNOWLEDGE-HUB state can report stale unmerged counts (e.g., 20, 14, 11 unmerged) while repos are actually SYNCED vs origin/hermes. kpt-admin (20→1), kpt-common-barrels-ciq (14→1), kpt-datafield-ciq (11→1) — all 3 were falsely CRITICAL/WARNING. **Always verify with fresh `git rev-list --count origin/hermes..HEAD` — never trust cached counts from Knowledge Hub.** Stale counts trigger false CRITICAL alerts.
