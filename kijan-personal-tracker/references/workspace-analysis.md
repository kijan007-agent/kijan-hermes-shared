# Workspace Analysis (2026-05-09)

## Analysis Summary
Comprehensive workspace scan of Kijan Personal Tracker ecosystem.

## Key Findings

### kpt-app-ciq State
- Submodule path `/workspace/Github/KijanPersonalTracker/kpt-app-ciq/` is a **bare repo**
- Contains only `.git/` with FETCH_HEAD, HEAD, config, hooks — no working tree
- Actual source code (116 .mc files) lives in `/workspace/Github/KijanPersonalTracker-prod-hotfix/kpt-app-ciq/source/`
- This is the development working copy
- `.git` contains `index.lock` — stale lock from interrupted git operation

### kpt-symptoms-app State
- Only contains README.md — no source code
- `.git` file is not a valid git reference (empty or corrupted)
- Submodule was never properly initialized/updated

### kpt-backend Structure
- 4 PostgreSQL databases: kijan_admin, kijan_activity, kijan_projects, kijan_health
- 5 Alembic migration directories: alembic_admin, alembic_activity, alembic_health, alembic_projects, alembic
- Models defined in `app/models.py` with 4 Base classes (BaseAdmin, BaseActivity, BaseProjects, BaseHealth)
- Async database pattern with session managers

### kpt-doc Structure
- MEMORY/ — 149 files: bug fixes, patterns, technical decisions, session notes
- _tasks/ — 31 active task files (TASK-063 through TASK-109+)
- _done/ — completed tasks
- TASKS.md — master task list with priorities
- PROMPTS_FOR_LOCAL_MODELS.md, PROMPT_COMPLEX_TASKS.md — AI prompt templates

### kpt-website
- Static HTML only: index.html, impressum.html, privacy.html
- Minimal structure — no framework

### kpt-website-pre-release
- Static HTML + lang.js for i18n
- index.html, impressum.html, privacy.html, terms.html

### Other Repos in /workspace/Github/
- ESP32-Catfeeder-and-Scale (IoT/cat feeder project)
- ESP32-RC-current-sensor (ESP32 current sensor)
- EdgeTxSync (EdgeTx radio settings sync)
- kijan-rc-settings (RC settings)

### Terminal Environment
- No `git` binary available in terminal (sandboxed)
- `/usr/bin/bash` is the shell
- Docker available (used for backend)
- Python 3.11 (hermes-agent venv)

### Submodule Working Tree Pitfall (2026-05-10)
- `kpt-app-ciq` is a **bare git submodule** — only `.git/` exists, no `source/` working tree
- When files like `EnergyScreen.mc`, `ScreenFlowController.mc`, `DeltaInputScreen.mc` are requested from `kpt-app-ciq/source/`, they will fail with "File not found"
- Always fall back to `/workspace/Github/KijanPersonalTracker-prod-hotfix/kpt-app-ciq/source/` for reading MC source files
- The feature branch's actual source state requires `git submodule init && git submodule update` from the parent repo (not possible in sandbox)
- TASKS.md is accessible from `kpt-doc/_tasks/` (part of kpt-doc submodule which IS checked out)
- Worklogs at `kpt-doc/_worklogs/` (same accessible submodule)
