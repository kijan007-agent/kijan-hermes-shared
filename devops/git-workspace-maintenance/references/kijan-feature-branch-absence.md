# KijanPersonalTracker Feature Branch Absence

## Discovery (2026-05-10)
Status audit requested paths: `/data/Github/KijanPersonalTracker-feature/` or `/workspace/Github/KijanPersonalTracker-feature/`.
Neither directory exists on disk. Only these Kijan repos exist:
- `/workspace/Github/KijanPersonalTracker/` (main repo with submodules)
- `/workspace/Github/KijanPersonalTracker-prod-hotfix/` (prod-hotfix working copy)

## Pattern
When a task references `KijanPersonalTracker-feature` paths:
1. Workspace scan `/workspace/Github/` first — do NOT assume the feature branch exists
2. If absent: fall back to main repo TASKS.md as single source of truth
3. Report: "Feature branch repo not on disk — status from TASKS.md only"
4. Never attempt to read `.mc` files from feature-branch paths — they don't exist

## Related
- `kijan-personal-tracker` skill → `references/feature-branch-not-on-disk.md`
