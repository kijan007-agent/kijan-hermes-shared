---
name: cron-reliability
category: devops
description: Scheduled job patterns for Hermes Agent — status detection, false-completion verification, workspace path conventions, and interrupt-resilient workflows.
---

# Cron Job Reliability — Scheduled Job Patterns

Patterns for running Hermes Agent as a cron job: detecting task status reliably, verifying file existence, handling workspace paths, and preventing false completion claims.

## Core Principle: TASKS.md is Planning Intent, Not Reality
TASKS.md tracks what SHOULD be done. Working tree + git history = actual state.
**Never** use TASKS.md status alone as the source of truth for task completion.

## Workspace Path Convention

| Path | Status | Use For |
|------|--------|---------|
| `/workspace/Github/KijanPersonalTracker-hermes/` | ✅ ACTIVE | All file operations, git commands |
| `/workspace/Github/KijanPersonalTracker-feature/` | ✅ ACTIVE (feature branch) | Code inspection on feature branch |
| `/workspace/Github/KijanPersonalTracker-prod-hotfix/` | ⚠️ UNKNOWN (post-wipe) | Last known: LEGACY. Verify before use. |
| `/data/Github/` | ❌ NOT MOUNTED IN CRON | Cron sandbox — empty shells, use `/workspace/Github/` exclusively |
| `/data/Github/KijanPersonalTracker-feature/` | ❌ WIPE (2026-06-07) | Zero commits, zero remotes — COMPLETELY WIPED. See COMPLETE REPO DELETION PATTERN. |
| `/data/Github/KijanPersonalTracker-hermes/` | ❌ WIPE (2026-06-07) | Zero commits, zero remotes — COMPLETELY WIPED. See COMPLETE REPO DELETION PATTERN. |
| `/workspace/Github/KijanPersonalTracker-feature/` | ❌ WIPE (2026-06-07) | Zero commits, zero remotes — COMPLETELY WIPED. |
| `/workspace/Github/KijanPersonalTracker-hermes/` | ❌ WIPE (2026-06-07) + SUBMODULE WIPE (2026-06-08) | Zero commits. kpt-backend submodule also zero commits + no remote. |
| `/workspace/Github/KijanPersonalTracker-feature/` | ❌ WIPE (2026-06-07) | Zero commits, zero remotes — COMPLETELY WIPED. |
| `/workspace/Github/KijanPersonalTracker-prod-hotfix/` | ⚠️ UNKNOWN (post-wipe) | Last known: LEGACY. Verify before use. |
| `/tmp/kpt-extract/source/` | ⚠️ UNKNOWN (post-wipe) | Was post-wipe .mc snapshot — verify existence. |
| `/data/Github/KijanPersonalTracker-feature/` | ❌ EMPTY (2026-06-08) | Zero commits, zero remotes — wiped 2026-06-07. |
| `/data/Github/KijanPersonalTracker-hermes/` | ❌ EMPTY (2026-06-08) | Zero commits, zero remotes — wiped 2026-06-07. |
## Empty Repo Detection Pattern (2026-05-24)

When cron job paths (`/data/Github/...`) return "File not found" or "Path not found":
1. Check `/workspace/Github/` first — this is the actual mounted workspace
2. Run `git -C <path> log --oneline -1 2>&1` to verify repo has commits
3. Check `git remote -v` — empty remotes + zero objects = empty shell
4. If no commits + no remotes → empty shell, report as blocker
5. If commits exist → use that path instead
6. **Fallback**: If `/workspace/Github/` also empty, check `/home/hermes/Github/`
7. **Fallback**: If still nothing, run `find / -maxdepth 4 -name 'KijanPersonalTracker*' -type d 2>/dev/null | head -5`

**CRITICAL**: `/data/Github/KijanPersonalTracker-feature/` and `/data/Github/KijanPersonalTracker-hermes/` are empty git shells (zero commits, zero remotes, zero pack objects). `/data/Github/` is NOT mounted in this environment. The real repos are at `/workspace/Github/`.

**NEW (2026-05-24)**: When a repo has zero git objects AND zero remotes (not just no commits), it's a completely empty clone — nothing to verify, report as "repo not deployed to this environment" immediately. Don't waste cycles on `git log` or `ls` of empty dirs.

## Detection Workflow (execute ALL steps)

### Step 1: Direct file check
```bash
find /workspace/Github/KijanPersonalTracker-hermes -name 'FileName.mc'
```
If found → `read_file` at that path.
If not → Step 2.

### Step 2: Git history in working tree
```bash
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq log --oneline --all -- source/FileName.mc
```
If found → file was committed then deleted/replaced.
If not → Step 3.

### Step 3: Submodule remote branches
```bash
git -C /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq show origin/feature:source/FileName.mc
```
Packed-refs may contain feature branch data without remote access.

### Step 4: Session history
```
session_search(query="<filename> mc file work done implementation")
```

### Step 5: Cross-reference TASKS.md (context only)
TASKS.md may explain INTENDED work — but never trust it for existence.

## Status Reporting Convention

| Symbol | Meaning | Action |
|--------|---------|--------|
| ✅ | File exists AND matches documented impl | No action |
| ⚠️ | Documented as done but file mismatch | Report discrepancy, plan re-impl |
| ❌ | File never created or deleted | Report as "not started" or "deleted" |
| 📋 | TASKS.md says done, disk disagrees | Report as "claimed but not committed" |

## Post-Wipe Status (2026-06-07+)

**ALL KijanPersonalTracker repos are empty.** Zero commits, zero remotes, zero objects.
- `KijanPersonalTracker-feature` → wiped
- `KijanPersonalTracker-hermes` → wiped
- `kpt-backend` (submodule) → wiped

**Surviving artifacts (untracked only):** `kpt-doc/_specs/`, `kpt-doc/_mockups/`, `/tmp/kpt-extract/source/` (read-only .mc snapshot)

**TASKS.md is unrecoverable** from git — any local copy is pre-wipe planning intent, NOT reality.

## Pre-Wipe False Completions (historical reference only)

| Item | Claimed | Actual (pre-wipe) |
|------|---------|-------------------|
| EnergyScreen chart redesign | COMPLETED ✅, 493 lines | 81-line stub (chart committed at `972f55f`, replaced at `9bb0b5d`) |
| DeltaInputScreen | COMPLETED ✅, 417 lines | File NEVER existed |
| ScreenFlowController overlay stacking | COMPLETED ✅ | 585 lines, overlay queue + chain system |
| Transition validation (fireSignal) | COMPLETED ✅ | Config-driven with conditional routing |
| ActivitySession state sync | COMPLETED ✅ | ActivitySessionContext in use |
| TASK-105 through TASK-109 | COMPLETED ✅ | Specs only (4 files in _tasks/), zero code changes |

## False Completion Detection Notes
- Ancestor ≠ current content: chart was committed at `972f55f` then replaced at `9bb0b5d`
- When auditing, check BOTH working tree AND remote branch (packed-refs may contain feature data)
- EnergyScreen stub is CORRECT per current codebase — it's intentional, not broken

## False Completion Root Causes
1. Cron sessions interrupted before `git commit`
2. Work done in temp working tree that was discarded
3. TASKS.md written proactively (tasks planned but not yet committed)
4. Submodule HEAD not updated to match remote branch content
5. **Simplified replacement**: Full feature implemented then replaced by simplified version (EnergyScreen: 493→122 lines). Check `git merge-base --is-ancestor <full-commit> <simplified-commit>` to detect replacement chains.

## Prevention Checklist
- After file modification: `git status` immediately
- Commit per task, not per session
- On cron completion: run `git diff --stat` to verify expected changes are staged
- Report status as "claimed" vs "verified" — never "completed" without disk verification
- When auditing, check BOTH working tree AND remote branch (ancestor ≠ current content)
- **WORKLOG gap check**: `ls -la <worklog_dir>` + `git log --since=<last_worklog_date>` — if commits > last worklog date, flag stale worklog

## WORKLOG Stale Detection (2026-05-23, updated 2026-06-08)
Pattern: Worklog entries stop while commits continue.
- Find last worklog entry: `ls -lt <worklog_dir>/ | head -5`
- Find last commit: `git log --oneline -1 --since="<last_worklog_date>"`
- If gap > 3 days: report "WORKLOG GAP" — untracked commits exist
- Worklogs are manually maintained — never auto-synced with TASKS.md or git
- **If worklog directory doesn't exist**: report "no worklogs maintained" — do NOT fail
- **Combined stale check**: `git log --since="<last_worklog_date>" --oneline` + `ls -lt worklogs/ | head -1` — if commit count > 0 AND worklog gap > 3d → "WORKLOG STALE: N commits since last entry"

## Submodule HEAD vs Working Tree vs Remote Branch Divergence (2026-06-08)
Three layers can diverge independently — always check all three:
1. **Submodule working tree HEAD**: `git -C <submodule-path> log --oneline -1` — what's on disk
2. **Parent repo submodule pointer**: `git -C <parent> show <branch>:<submodule-path> --format=%H` — what parent expects
3. **Submodule remote branch**: `git -C <submodule-path> show origin/feature:source/<file>` — what remote has
4. **TASKS.md claim**: Independent document — verify against layer 1 (disk), NOT layer 3 (remote)
5. When layer 1 ≠ layer 3: the working tree is stale at the submodule level. The feature may exist on remote but not on disk.
6. **Key pattern**: TASKS.md in a parent repo can claim "COMPLETED" for a file in a submodule that was updated AFTER the submodule was last synced. The submodule pointer in the parent repo lags behind the submodule's own remote.
7. **Detection**: `git -C <submodule> log --oneline feature -5` + `git -C <submodule> log --oneline origin/feature -5` — if divergence > 0, the submodule has un-synced commits. Always check BOTH.
8. **NEVER** run `submodule update --init` before committing — it resets HEAD and loses changes
9. Commit locally first, then update parent repo's submodule pointer

## COMPLETE REPO DELETION PATTERN (2026-06-07)
When a repo that previously had commits now shows "No commits yet" with zero pack objects:
- The repo was **completely wiped** (not just branch reset)
- All work is lost unless backed up externally
- Report as CRITICAL BLOCKER — this is a data loss event, not a stale state
- Check if backup exists: `ls /workspace/Github/KijanPersonalTracker-feature/.git/refs/original/ 2>/dev/null`
- Check if origin remote is still reachable: `git -C <path> remote get-url origin 2>/dev/null`
- **Prevention**: After any git operation that changes history, verify with `git rev-list --count HEAD`
- **Root cause pattern**: `git push --force` or `git init --bare` over existing repo = complete wipe

## Submodule File Checking (2026-05-23)
When a project uses git submodules (e.g., kpt-app-ciq):
1. **DO NOT** use `read_file` on submodule paths without confirming it's checked out
2. Submodule working tree may be detached HEAD — `git status` in submodule path first
3. If submodule not checked out: use `git ls-tree -r HEAD -- <path>` in parent repo to find file references
4. File existence on disk ≠ file exists in git tree (submodule may not be populated)
5. When a file is in the submodule tree but not on disk: check if parent repo submodule pointer is stale
6. **Critical**: Tasks referencing files in submodules MUST specify the submodule path explicitly, not just the parent repo path

## Cross-Repo File Location Pattern (2026-05-24)
When a prompt references files at a path that doesn't exist:
1. Check the prompt path first (e.g., `/data/Github/...`)
2. If "File not found" → search `/workspace/Github/` recursively
3. If not in `/workspace/Github/` → check `/data/Github/` as fallback (may have different repo layout)
4. If files exist in a submodule → the path is `<parent-repo>/<submodule-path>/<file>`
5. Always verify the repo has commits before trusting it contains the files
6. **Pattern**: kpt-app-ciq source files live in `/workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq/source/` — NOT at `/data/Github/KijanPersonalTracker-feature/kpt-app-ciq/source/` (which is an empty shell)

## Status Report Format (from cron-status-reports)

### Report Types

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

### Silent Rules
- If status unchanged from last report → `[SILENT]`
- If repo not found → report with "Repo not found"
- No user questions — autonomous decisions only
- **Empty-Shell-Silence**: When spec files exist but implementation is 0% and all repos are empty shells or remotes unreachable → `[SILENT]`. A report with "0% implemented, everything blocked" provides no actionable signal. Only report when there is genuine progress or a blocker that requires user action (e.g., "Remote repo deleted — needs re-clone").

### Night Silence
- No reports between 22:00 and 07:30. The 07:30 report includes night summary.

## Linked Resources
- `references/submodule-file-checking.md` — Step-by-step submodule file detection flow
- `references/cron-path-validation-pattern.md` — 3-layer validation for cron path resolution (exists → valid → content)
- `references/post-wipe-extraction-fallback.md` — `/tmp/kpt-extract/source/` as post-wipe code fallback (2026-06-07)
- `references/commit-to-task-mapping-pattern.md` — Map git commits to TASKS.md tasks via ancestry tracing
