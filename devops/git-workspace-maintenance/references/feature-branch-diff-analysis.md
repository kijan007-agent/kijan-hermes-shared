# Feature Branch Diff Analysis Pattern

## Context
When analyzing feature branch changes without remote access (GitHub auth unavailable), use local git data directly.

## Pattern: Analyze without fetch
```bash
# 1. Check what local refs exist
grep '<branch>' .git/packed-refs

# 2. Get commit range diff (stat)
git diff --stat origin/dev..origin/feature

# 3. Get file-level additions/deletions
git diff origin/dev..origin/feature --numstat

# 4. List files that changed
git diff origin/dev..origin/feature --name-status

# 5. Show individual commit details
git log --oneline origin/dev..origin/feature --reverse

# 6. Show specific commit changes
git show <sha> --stat
git show <sha> --source --dest <file>
```

## Submodule analysis
```bash
# Per-submodule feature commits
git -C <submodule> log --oneline origin/dev..feature

# Per-submodule diff stat
git -C <submodule> diff --stat origin/dev..feature

# Specific file in specific commit
git -C <submodule> show <sha>:<path>
```

## Key signals in commit messages
- `fix(TASK-XXX):` — task-specific fix
- `feat:` — new feature
- `refactor:` — code restructuring
- `chore:` — version bumps, CI changes
- `docs:` — documentation updates
- `i18n:` — localization additions
- `Merge branch` — integration commits

## Output format for reporting
1. Total additions/deletions and file count
2. Feature branch commit list (chronological)
3. Per-submodule change summary
4. Critical files requiring review
5. Risk assessment (build, runtime, performance, resources, integration)
6. Recommended next steps