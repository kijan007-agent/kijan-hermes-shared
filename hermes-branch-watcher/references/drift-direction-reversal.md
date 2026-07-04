# Drift Direction Reversal Pattern

> When a submodule's drift direction flips (ahead ↔ behind) between audits, the offset is measured against a **different reference point** — not just a count change.

## The Pattern

A submodule can report the SAME offset number but in **opposite directions** between audits:

| Product | Previous Audit | Current Audit | Direction Change |
|---------|---------------|---------------|-----------------|
| kpt-backend | 13 AHEAD vs origin/dev | 13 BEHIND vs origin/dev | origin/dev gained 13+ commits |
| kpt-app-ciq | 0 ahead vs origin/hermes | 120 AHEAD vs origin/hermes | hermes branch diverged heavily |
| kpt-doc | 71 ahead vs origin/dev | 154 AHEAD vs origin/dev | dev branch gained 83+ commits |

## Root Causes

1. **Remote catches up:** Other contributors pushed to origin/dev while you were working on hermes → previously AHEAD becomes BEHIND
2. **Branch divergence:** Your hermes branch accumulated commits that haven't been propagated → 0 → 120 ahead
3. **Direction matters:** `AHEAD` means your local has more commits; `BEHIND` means remote has more

## Detection

```bash
# Direction check — both directions mandatory
git rev-list --count origin/dev..HEAD       # ahead count
git rev-list --count HEAD..origin/dev       # behind count
# If first > 0: you are ahead. If second > 0: you are behind.
# They are NOT symmetric — both must be checked.
```

## Key Insight

**A count of "13" with AHEAD vs BEHIND is a completely different situation:**
- AHEAD 13: your local is ahead, need to push or merge remote
- BEHIND 13: remote is ahead, need to pull or merge

**Never report just the number — always report direction + reference branch.**

## Real Case: kpt-app-ciq (2026-06-09)

- Previous: 0 ahead vs origin/hermes (RESOLVED)
- Current: 120 AHEAD vs origin/hermes (CRITICAL DRIFT)
- Cause: feature branch merged to dev, but hermes not updated post-merge
- Pattern: `feature → dev` merge → dev diverges from hermes → hermes accumulates unmerged commits
- Action: merge origin/dev to hermes, review 120 commits for conflicts

## Real Case: kpt-backend (2026-06-09)

- Previous: 13 AHEAD vs origin/dev
- Current: 13 BEHIND vs origin/dev
- Cause: origin/dev received 13+ new commits (energy pacing dashboard fix, HAL v2)
- Action: merge origin/dev to hermes
