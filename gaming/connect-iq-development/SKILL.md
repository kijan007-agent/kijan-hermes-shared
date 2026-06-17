---
name: connect-iq-development
category: gaming
description: Garmin Connect IQ watch app development — UI patterns, branch porting, chart rendering, and systematic fix workflows.
---

# Connect IQ Development — App Design, Debugging, Porting

Skills for Garmin Connect IQ app development: UI/UX patterns, branch porting, chart rendering, and systematic fix workflows.

## Porting from Hotfix to Feature Branch (TASKS-driven)

When a feature branch's UI is broken (overlapping popups, wrong flows) but prod-hotfix-bat has working code:

1. **Analyze diff scope**: 
   - File-by-file compare via `diff` or script: list key UI files in both branches
   - Mark: Identical / DIFFER / Missing in one / New in one
   - Focus on: `ScreenManager.mc`, `EnergyScreen.mc`, `MorningCheckinView.mc`, `PacingSpoonsCheckinView.mc`, `InstantChangePopupView.mc`, `ScreenFlowController.mc`
2. **Extract key changed files** by category:
   - UI screens (EnergyScreen, CheckinView, etc.)
   - Navigation/flow (ScreenFlowController, InitScreens, etc.)
   - Data layer (StatusCheckManager, ConfigStore, etc.)
   - Resources (drawables, strings, layouts)
3. **Create TASK-*.md files** in `kpt-doc/_tasks/` — one file per distinct task
   - Naming: `TASK-{number}_{short_description}.md`
   - Each file: User Story, Problem, To-Do (numbered steps)
   - Update `INDEX.md` with a "NEW" section summarizing all new tasks
4. **Port P0 fixes first**: View validity guards, popup stack management, screen registration
6. **Create worklog** in `kpt-doc/_worklogs/WORKLOG.md` with timestamped entries
   - **RULE**: Each entry MUST include:
     - Repository name worked in (e.g., `KijanPersonalTracker-feature`)
     - Branch name (e.g., `feature`)
     - Git commit hash (if changes committed, e.g., `1c06a2fe2342`)
     - Pattern: `## HH:MM UTC — [Repository] [Branch] [Commit/Status]`
7. **Commit per task** for traceability
8. **Verify on simulator** after each batch

## Connect IQ UX Fix Patterns

### TASK-100: Overlay Stacking / Popup Queue
- **Cause**: `showOverlay()` stacks multiple overlays without waiting for auto-dismiss.
- **Fix**: Add `mPendingScreen` + `mPendingScreenParams` fields. In `go()`, defer push when overlay active. On `onOverlayTimer()`, flush deferred screens after overlay chain completes.
- **⚠️ 2026-05-12**: `mPopupStack` and `mActiveDelegate` pattern from connect-iq-ux-fixes.md NOT yet implemented in ScreenFlowController.mc. `mPendingScreen` exists but has no flush logic. See TASK-CIQ-03.

### TASK-101: Transition Validation — Default-Deny
- **Cause**: `_canGo()` validates against `fromScreen` instead of `currentScreen`, allowing invalid transitions that cause overlapping popups.
- **Fix**: Check `currentScreen` (not `fromScreen`) against `ScreenFlowConfig`. Default deny — only allow transitions explicitly defined. Add logging for rejected transitions.
- **Status (2026-05-19)**: `fireSignal()` validates against `mCurrent` via `_canGo()`. `go()` path (line 68) does NOT call transition validation — only checks `hasScreen()` and skips push if target already in stack. No `validateTransition()` method exists in ScreenFlowValidator. `validateSignal()` + `advanceState()` exist but no unified transition gate. Gap: `go()` path has no explicit transition guard — invalid transitions pass through `go()` and fail silently at `_push()` time.

### TASK-102: ScreenRenderer Not Showing
- **Cause**: EnergyScreen not registered in InitScreens.mc.
- **⚠️ 2026-05-13**: EnergyScreen.mc EXISTS (123-line stub). Chart redesign (493 lines) in kpt-app-ciq history, never merged to feature. TASK-CIQ-02: register the stub in InitScreens.mc when wired up.
- **Cause**: Callbacks fire on invalid views, delegate not cleaned up
- **Fix**: Validate `isViewValid()` before any callback execution, `clearPopupStack()` on screen exit

### Problem: ScreenRenderer Not Showing
- **Cause**: EnergyScreen (extends ScreenRenderer) not registered in InitScreens.mc.
- **Fix**: Add to `mScreens` array when condition is met
- **⚠️ 2026-05-13**: EnergyScreen EXISTS (123-line stub). Chart redesign (493 lines at 972f55f) in origin/feature history, NOT in working tree. Chart was committed then replaced by intermediate commit `9bb0b5d`. When re-implementing, decide: wire up the stub or restore chart from history.

## Spoon-Level Visualization Patterns

### ⚠️ EnergyScreen — POST-WIPE STATUS (2026-06-08)

> **ALL repos wiped.** Pre-wipe state: `EnergyScreen.mc` in kpt-app-ciq HEAD = 123-line stub, NOT chart redesign. Chart (493 lines) existed at commit `972f55f` then replaced by stub at `9bb0b5d`. `EnergyDrawable.mc` (151 lines) is the shared drawable. Spoon colors: >=20 green, >=10 yellow, <10 red. `:energyScreen` route in ScreenFlowController.mc pointed to stub, NOT chart. TASKS.md claimed COMPLETED but disk disagreed. DeltaInputScreen: documented as 417 lines, file NEVER existed.

### ⚠️ TASKS.md Commit-Hash Staleness (2026-05-25)

**Pattern**: TASKS.md references commit hashes from BEFORE major branch merges (e.g., 779-commit hermes branch). When TASKS.md date predates the latest merge date, ALL hash-tied claims are unreliable.

**Detection**: 
```bash
git log --oneline -1                       # latest commit on branch
grep -o '[0-9a-f]\{7,\}' TASKS.md | head  # stored hashes in TASKS.md
```
If latest commit predates all stored hashes → TASKS.md anchors are stale.

### Color Thresholds (spoon mode)
- >= 20: green
- >= 10: yellow  
- < 10: red

### EnergyDrawable API (actual — 151 lines)
- `getColor(energyLevel, unitMode)` — returns Graphics.COLOR_RED/ORANGE/GREEN
- `_getSpoonBitmap(energyLevel)` — loads SpoonGreen/Yellow/Red from Rez.Drawables
- `draw(dc, cx, cy, energyLevel, unitMode, maxIcons)` — spoons (2 rows circles + spoon bitmap) or energy (diamonds)
  - Spoon mode: iconSize=7, step=16, 2 rows ceil/floor split
  - Energy mode: iconSize=10 (diamond), step=13

## Status Check & Data Layer

### StatusCheckManager Integration
- Use `getLastNChecks(n)` for historical data
- Use `getCheckCount()` to check if data exists
- Correlate timestamps to hours via `(ts + tzOffset) % 86400 / 3600`

### Interpolation Pattern
- Fill hourly array with -1 (no-data sentinel)
- Place actual values at hour positions
- Forward-fill gaps with linear interpolation
- Backward-fill remaining gaps
- Final fallback to default value

### Support Files

- `references/ciq-simulator-linux-setup.md` — **COMPLETE GUIDE**: Running Connect IQ Simulator on Linux VM (Debian 13) with Xvfb, Jammy libs, self-compiled libwoff2dec. Installation steps, compilation, screenshot capture, troubleshooting.
- `references/monkey-jungle-test-exclude.md` — (:test) Annotation Exclude Pattern für monkey.jungle.
- `references/submodule-remote-sync-without-pki.md` — Content-Extraktion ohne SSH-PKI für Submodule.
- `references/phasechange-feedback-pattern.md` — PhaseChange Feedback Kommunikation: fireSignal → onPhaseChangeConfirmed() Return-Value Pattern
- `references/external-repo-locations.md` — External repo paths
- `references/connect-iq-ux-fixes.md` — Detailed UX fix patterns (popups, charts, interpolation)
- `references/screenflow-patterns.md` — ScreenFlow FSM overlay queue, transition validation, session sync patterns
- `references/kijan-repo-structure.md` — KijanPersonalTracker repo layout, submodule URLs, branch convention, TASKS.md structure, common pitfalls
- `references/status-audit-workflow.md` — 6-step cross-repo status verification workflow (disk → git → remote → findings)
- kpt-app-ciq is a **bare repo** at `/workspace/Github/KijanPersonalTracker/kpt-app-ciq/` — no working tree. Source code in prod-hotfix copy at `/workspace/Github/KijanPersonalTracker-prod-hotfix/kpt-app-ciq/source/`
- `references/branch-diff-workflow.md` — Systematic file-by-file branch diff workflow for hotfix→feature porting
- `scripts/feedback_cron.sh` — 60-minute status feedback (Telegram + terminal)
- `scripts/screenshot-mockup.py` — reusable Pillow mockup generator (labels output as MOCKUP)
- `references/feature-branch-20250509.md` — kijan-personal-tracker skill: Feature branch 2025-05-09 analysis (40 commits, 32.8k+/- lines, critical review items)
- `references/broken-features-removal-pattern.md` — EnergyScreen/DeltaInputScreen removal rationale + re-implementation checklist
- `references/cron-status-detection-pattern.md` — Cron-job status detection workflow when files missing from disk
- `references/re-entry-prevention-pattern.md` — Guard flag pattern to prevent duplicate async operations (save/commit)
- `references/subclass-pattern.md` — Monkey C UI inheritance: base class + subclasses instead of copy-paste views
- `references/ubuntu-vm-sdk-setup-2026-05-16.md` — VM provisioning, VNC setup, SDK install, build workflow, SCP workarounds
- `scripts/feedback_cron.sh` — 60-minute status feedback (Telegram + terminal)
### Pitfall
- Cold start: service may create session before view calls `ActivitySession.start()`. Always check BOTH `ActivitySession.get()` AND `service.isSessionActive()` on cold start.
- **kpt-app-ciq has NO `.mc` files** — external repo only. See `references/external-repo-locations.md` for details.
- **New workspace `/workspace/Github/KijanPersonalTracker-hermes/`**: This workspace has working (non-ghost) submodules. When analyzing feature branches here, packed-refs may contain feature branch data even without remote access. Use `git show <sha>:<path>` and `git diff origin/dev..origin/feature` directly on packed-refs data.

### ⚠️ Workspace Path Convention — Choose Correct One

**This workspace (active)**: `/workspace/Github/KijanPersonalTracker-hermes/`
- kpt-app-ciq is a **working submodule** with full .mc source tree
- All `.mc` files accessible at `/workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq/source/`
- kpt-doc accessible at `/workspace/Github/KijanPersonalTracker-hermes/kpt-doc/`

**Old workspace (deprecated)**: `/workspace/Github/KijanPersonalTracker/`
- kpt-app-ciq was a **broken bare repo** — no .mc files accessible
- DO NOT use paths from this workspace — they will return "File not found"

**⚠️ Cron-job sandbox paths**: `/data/Github/` paths are sandbox-only and NOT accessible.
Always use `/workspace/Github/KijanPersonalTracker-hermes/` as base path.

### ⚠️ Cron Fallback: Tarball Extraction (2026-06-03 confirmed)

When cron job paths (`/data/Github/`) are dead for KijanPersonalTracker AND `/workspace/` is not available:
1. Check for tarballs: `ls /tmp/kpt-app-ciq*.tar.gz 2>/dev/null`
2. Extract to temp: `tar xzf /tmp/kpt-app-ciq-full.tar.gz -C /tmp/kpt-extract`
3. Read from extracted path: `/tmp/kpt-extract/source/*.mc`
4. This is the ONLY fallback — no remote fetch possible from cron sandbox.
5. **WARNING**: Tarball content is STATIC — not git-tracked, may be stale. Always note extraction source.

### ⚠️ Cron Job: TASKS.md False Completion — Always Verify Against Disk AND Git

**See `cron-reliability` skill for full detection protocol and known false completions.**

### ⚠️ Submodule Working Tree vs Remote Branch Divergence (2026-05-13/23)
**Problem**: On cold start, `onShow()` fires with stale/null `_type`/`_label` cached in the view.
Service already has the real session state, but the view hasn't synced yet → wrong screens rendered.

**Fix**: In `onShow()`, BEFORE any UI rendering or screen selection, sync from service:
```monkeyc
var svc = KijanActivityTrackerService.getInstance() as KijanActivityTrackerService;
if (svc.isSessionActive()) {
    _type  = svc.mType;
    _label = svc.mLabel;
}
```
This must come AFTER `KijanViewBase.onShow()` (so service is initialized) but BEFORE
`_rebuildScreens()` or any screen navigation logic.

**Why**: `initialize()` may have started a session, but `onShow()` is called on a fresh or
recycled view instance. The view's cached state is from a previous session or null. The service
is the single source of truth — always read from it first.

### Submodule Remote Divergence — Content-Sync ohne SSH-PKI

Wenn Submodule lokale Commits haben die mit `origin/feature` divergieren und **keine SSH-PKI Auth** besteht:

1. **Divergenz prüfen**: `git log --oneline feature..origin/feature` und `git log --oneline origin/feature..feature`
2. **Nur neue Remote-Commits identifizieren**: `git log --oneline --ancestry-path <merge-base>..origin/feature`
3. **Content extrahieren via git show** (ohne fetch/pull): `git show <sha>:<path>` für jede geänderte Datei
4. **Content in Working Tree schreiben**: `git show <sha>:<path> > <file>` für jede Datei
5. **Diff prüfen**: `git diff <file>` — CRLF-Unterschiede ignorieren, echte inhaltliche Diffs identifizieren
6. **Lokale vs Remote-Inhalte vergleichen**: `git show :<file>` (working tree) vs `git show origin/feature:<file>` — nach CRLF-Normalisierung (`\\r\\n` → `\\n`)
7. **Commit und Submodule-Pointer im Parent-Repo updaten**: `git add <submodule> && git commit`
8. **Niemals `submodule update --init` vor dem Commit** — das setzt den Submodule-HEAD auf den recorded SHA zurück und VERLIERT alle Änderungen!

**Pitfall**: `submodule update --init` reset den Submodule-HEAD auf den recorded SHA. Immer zuerst Content anwenden, commit'en, dann Parent-Repo pointer updaten.

**Pitfall**: `git diff HEAD` zeigt oft Hunderte Zeilen Diffs wegen CRLF — immer nach Content-Diffs filtern durch CRLF-Normalisierung.

### Commit-Diff via gh api wenn SSH-PKI fehlt

Wenn `gh` CLI eingeloggt ist aber SSH-Key keine Read-Auth hat:

1. **Dateiliste**: `gh api repos/owner/repo/commits/<sha>...<base-sha> --jq '.files[] | .filename'`
2. **Diff pro File**: `gh api repos/owner/repo/commits/<sha>...<base-sha> --jq '.files[] | "\(.filename)\n---DIFF---\n\(.patch)\n---END---"'`
3. **Patches anwenden**: `gh api` Diff in Python-String-Replace konvertieren (nicht `patch` tool — das versagt bei großem Kontext und sich ändernden Zeilen)

**Pitfall**: `gh` CLI muss unter dem SAME user wie der Arbeitsprozess laufen. Auf VMs mit `/workspace/` liegt die gh-Config oft unter `/root/.config/gh/hosts.yml`, aber execute_code läuft als anderer User. Fix: `cp /root/.config/gh/hosts.yml /workspace/.config/gh/hosts.yml`.

### Patch-Strategie bei großen MonkeyC Files

Bei Files >1000 Zeilen und komplexen Commits:
1. **Niemals das `patch` tool mit `old_string`/`new_string` verwenden** — das versagt wenn sich Zeilen verschoben haben
2. **Stattdessen**: Python `str.replace()` mit dem exakten alten Textblock als Key
3. **Vorher prüfen**: `grep -n 'function onPhaseChangeConfirmed' file.mc` — muss exakt 1x existieren
4. **Nachher prüfen**: `git diff --stat` — sollte nur die erwarteten Files zeigen, nicht "deletion + insertion" für das ganze File

### ⚠️ Submodule Working Tree vs Remote Branch Divergence (2026-05-13/23)

When `kpt-app-ciq` submodule is at HEAD `9a7fe42` (or any local commit):
- Working tree EnergyScreen = 123 lines (stub)
- `origin/feature` HEAD at `972f55f` = 493 lines (chart) — IS ancestor of local HEAD
- Chart was committed at `972f55f` then REPLACED by intermediate commit `9bb0b5d` (new file, 123 lines)
- **Ancestor ≠ current content** — verify BOTH working tree AND remote branch when auditing
- **TASKS.md is planning intent, NOT reality** — a task can be "COMPLETED" in TASKS.md while the file never reached disk (cron interruption). Always `find` before `read_file`.

### ⚠️ Cron Job: TASKS.md False Completion — Always Verify Against Disk AND Git

### Connect IQ Multi-Environment Pattern (2026-05-14)

For different build targets (dev/staging/prod/local VM), use annotation-based environment selection:

1. **Create `Env{env}.mc`** in `source/` with unique annotation:
```monkeyc
(:local)
module Env {
    function getBackendUrl() as String { return "http://100.83.88.122:8011/"; }
}
```

2. **Create `monkey-{env}.jungle`**:
```
project.manifest = ./manifest.xml
base.sourcePath = ./source;../kpt-common-barrels-ciq/source
base.excludeAnnotations = prod;staging;test   # exclude ALL OTHER envs
```

**⚠️ `test` Annotation muss explizit excluded werden** — Monkeyc kompiliert `(:test)`-annotierte Dateien STANDARDMÄSSIG mit. Test-Dateien (`Test*.mc`) enthalten oft Methoden die nicht in produktiven SDKs existieren (`:setCurrentScreen`, etc.). Ohne `test` in excludeAnnotations: 100+ Compile-Fehler durch Test-Code.

3. **Add `--{env}` flag to `build.sh`**:
```bash
elif [ "$1" = "--local" ]; then
    JUNGLE="monkey-local.jungle"
    shift
```

4. **Create wrapper script** `build_ciq_{env}.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")"
./build.sh --{env} "${1:-epix2pro51mm}"
```

**Template**: `templates/ciq-env-build-script.sh` in this skill.

**Pitfall**: `(:local)` annotation MUST NOT appear in the `excludeAnnotations` list of `monkey-local.jungle`, otherwise it gets excluded too and no `Env` module is compiled.

### Pitfall
- Cold start: service may create session before view calls `ActivitySession.start()`. Always check BOTH `ActivitySession.get()` AND `service.isSessionActive()` on cold start.
- **kpt-app-ciq has NO `.mc` files** — external repo only. See `references/external-repo-locations.md` for details.
- **New workspace `/workspace/Github/KijanPersonalTracker-hermes/`**: This workspace has working (non-ghost) submodules. When analyzing feature branches here, packed-refs may contain feature branch data even without remote access. Use `git show <sha>:<path>` and `git diff origin/dev..origin/feature` directly on packed-refs data.

### Screenshot-Generierung — Fallback-Mockups (2026-05-17)

**KERN-PRINZIP**: Echte Simulator-Screenshots VOR Mockups. Mockups sind KEINE echten Screenshots — nur als Fallback akzeptabel.

**Simulator auf Linux VM — JETZT FUNKTIONIEREND (2026-05-17):**
Der Connect IQ Simulator läuft auf Linux/Debian 13 VMs mit Xvfb!
- **Voraussetzungen**: Xvfb + Ubuntu Jammy (22.04) WebKit libs + self-compiled libwoff2dec
- **Simulator starten**: `DISPLAY=:99 LD_LIBRARY_PATH=/tmp/webkit40_extract/usr/lib/x86_64-linux-gnu:/tmp/jsc40/usr/lib/x86_64-linux-gnu /workspace/frameworks/Garmin/ConnectIQ/Sdks/connectiq-sdk-lin-*/bin/simulator`
- **Xvfb**: `Xvfb :99 -screen 0 800x600x24 &`
- **Screenshots**: `xdotool` oder `import -window root /tmp/screenshot.png` via Xvfb
- **⚠️ 2026-05-17**: SDK 9.1.0 ist STRENGER als ältere SDKs — massive "untyped" und "Cannot determine type" Compile-Fehler bei älterem Code. SDK-Version prüfen!

### onUpdate() Pitfalls
- **onUpdate() must not allocate** — no new objects, no string concatenation in loops
- **Bitmap loading** — always use `WatchUi.loadResource(Rez.Drawables.X)` not raw paths
- **`has :method` checks** required before calling newer API methods (e.g., `fillPolygon`)
- **Array vs Dictionary payloads** — ActivityEventQueue uses arrays for sync payloads
- **Property access** — use `properties.hasKey()` then `properties.get()` with try-catch, never direct access

### Deprecated method() Pattern (2026-05-27)
- **Pattern:** `method(:onOverlayTimer)` instead of `Lang.Method(:onOverlayTimer)`
- **Found:** 3 instances in kpt-app-ciq — ScreenFlowController and TimeWindowMenuDelegate
- **Fix:** Replace all `method(:symbol)` with `Lang.Method(:symbol)` — this is a Connect IQ SDK compatibility issue
- **Detection:** `grep -rn 'method(' source/ --include='*.mc' | grep -v 'Lang.Method'`

### Re-entry Prevention (CRITICAL)
- Guard async save/commit paths with `mInProgress` flag — user can trigger re-entry
- See `references/re-entry-prevention-pattern.md` for full pattern

### UI Architecture: Subclass Pattern
- Never copy-paste >50 lines of view code — use inheritance instead
- Base class with shared layout + state, subclass per phase/view
- Max 2 levels deep (Monkey C memory constraints)
- See `references/subclass-pattern.md` for full pattern

### Build & Simulator — SDK Prerequisites

**Required**: Valid Garmin Connect IQ SDK with `connectIQ/` directory containing device API data.

**Pitfall**: SDK archives extracted incorrectly (empty `connectIQ/` subdirectory) → `monkeyc` cannot find device definitions → `ERROR: Invalid device id specified`. Symptoms:
- SDK root contains only HTML/README/docs/bin/resources/samples/share — no `connectIQ/` dir
- `bin/api.db` exists but device-specific APIs are missing (e.g., `epix2pro51mm` in API 6.0+ not in SDK 8.4.1 API 5.2)
- `monkeyc` is a bash wrapper calling `monkeybrains.jar` via Java

**Valid SDK structure**:
```
connectiq-sdk-lin-<version>/
  bin/
    monkeyc, monkeydo, simulator, monkeybrains.jar
    api.db, api.mir, api.debug.xml   ← API signature database
  connectIQ/                          ← CRITICAL: device API data (non-empty!)
    <device_id>/
      compiler.json, simulator.json
      epix2pro51mm.api.debug.xml
      epix2pro51mm.bin
      ...
  resources/device-reference/
  samples/
```

**Fix**: Re-download SDK from [developer.garmin.com/connect-iq/sdk/](https://developer.garmin.com/connect-iq/sdk/). Verify `connectIQ/` directory exists and is non-empty BEFORE building.

**SDK on remote VM**: If the SDK must run on a remote VM (e.g., the CIQ SDK requires local execution), install Java first (`sudo apt-get install default-jdk-headless`), then download SDK to the VM directly. Use `ssh user@host 'bash -s' << 'HEREDOC'` with `sudo` inside the heredoc body — not as a prefix — to avoid breaking apt-get's TTY requirements.

**SDK Installation — Immer direkt zip, NIE AppImage:**
- SDK direkt als zip von [developer.garmin.com/connect-iq/sdk/](https://developer.garmin.com/connect-iq/sdk/) herunterladen → entpacken → `connectIQ/` Verzeichnis prüfen.
- SDK Manager AppImage auf ALLEN Ubuntu-Versionen unzuverlässig (libsoup, libcurl, libwebkit2gtk Konflikte).
- **Priorität:** zip-Installation > Distrobox > AppImage. AppImage nur als letzter Ausweg.

**SDK auf frischer VM — Schnellweg (Ubuntu 22.04+):**
1. SDK zip auf VM kopieren ( scp oder manuell via Browser)
2. Entpacken: `unzip connectiq-sdk-linux.zip`
3. Prüfen: `ls connectIQ/ | head -5` (muss nicht-leer sein)
4. Java installieren: `sudo apt-get install -y default-jdk-headless`
5. simulator + monkeyc sofort nutzbar

### ⚠️ SDK-Strengerheits-Level — Compile-Fehler durch SDK-Version

**SDK 9.1.0** ist deutlich strikter als SDK 8.x und älter:
- Massive "untyped" und "Cannot determine type" Fehler bei älterem Code
- Typen-Checking ist viel aggressiver — Methodenparameter müssen exakt passen
- "Type mismatch (passing)" Fehler bei impliziten Konvertierungen die in älteren SDKs funktionierten
- **Symptom**: 500-2000+ Compile-Fehler obwohl Code mit älterem SDK funktioniert
- **Prüfung**: Immer mit mindestens zwei SDK-Versionen testen (z.B. 8.4.1 + 9.1.0)
- **Fix-Strategie**: Wenn nur SDK 9.x fehlschlägt → Code ist für älteres SDK geschrieben. Nicht blind fixen — SDK-Version der Zielgeräte prüfen!
- **⚠️ `:setCurrentScreen` ist KEINE gültige Connect IQ Methode** — falsche Methodenreferenz-Syntax in Test-Code. Korrekter Aufruf ist z.B. `WatchUi.setActiveScreen(screen)` oder `ScreenManager.setCurrentScreen()`. Die Symbol-Referenz `:kijanActivityTracker` ist ein SymbolTable-Key, KEIN Methodenname.

**VM-Reboot — VNC passwd leere Datei:**
- Beim ersten VNC-Start ist `~/.vnc/passwd` oft 0 Bytes → Authentication failed.
- Fix: Passwort mit Python schreiben: `python3 -c 'import hashlib; pw="hermes007"; r=b""; [r:=r+hashlib.md5(pw.encode()).digest() for _ in range(3)]; r=r[:16]; open("~/.vnc/passwd","wb").write(r)'`
- Dann: `vncserver -kill :1 && vncserver :1 -geometry 1920x1080 -depth 24 -localhost no`

**Pitfall — SDK Manager AppImage**: The Garmin Connect IQ SDK Manager AppImage requires GUI (X11 forwarding). It has NO CLI mode for installing SDKs. If `sdkmanager` complains about missing `libsecret-1.so.0` or needs DISPLAY, the SDK is NOT installed yet. Options:
1. Use SSH X11 forwarding (`ssh -X`) to launch the AppImage and install SDKs via GUI.
2. Download the SDK zip manually from [developer.garmin.com/connect-iq/sdk/](https://developer.garmin.com/connect-iq/sdk/) with a browser, then scp to the VM and extract manually.
3. Verify installation by checking for `monkeyc` binary + `api.db` + non-empty `connectIQ/` directory.

**Device compatibility**: Newer devices (epix2pro51mm, fenix8, etc.) require SDK with API level matching the device's firmware version. epix2pro51mm is in API level 5.2+ (per `devices.xml` in `monkeybrains.jar`). SDK 8.4.1+ should work. Verify with `jar tf monkeybrains.jar | grep devices.xml`. The device must appear in the extracted devices.xml.

**monkeyc device resolution failure**: If ALL device IDs are rejected (not just one), the SDK's `connectIQ/` directory is missing or corrupted. Verify the SDK root has a non-empty `connectIQ/` subdirectory with per-device API data files.

**Java requirement**: `monkeyc` is a Java wrapper — Java 11+ required (`java -version`). On fresh Ubuntu: `sudo apt-get install default-jdk-headless`. Set `JAVA_HOME=/usr/lib/jvm/default-java` before invoking `monkeyc` if needed.

**Pitfall — Barrel modules missing from build**: Connect IQ builds fail with "Undefined symbol ':' detected" when barrel source files are not in `base.sourcePath`. The `monkey.jungle` file references `../kpt-common-barrels-ciq/source` — this path MUST be resolved relative to the jungle file location. When deploying to a remote VM, copy ALL barrel modules to the expected relative path. Verify with `ls source/ ../kpt-common-barrels-ciq/source/` before building.

**Pitfall — Submodule source code not available**: External repos like `kpt-app-ciq` may have no `.mc` files in the sandbox (bare repo). Use `/workspace/Github/KijanPersonalTracker-hermes/` as active workspace where submodules have working trees. Always verify file existence with `find` before reading — if `*.mc` files are missing, check if the submodule is properly initialized with `git submodule update --init --recursive`.

**Pitfall — SCP zwischen VMs timeouted**: `scp` zwischen entfernten VMs timeoutet häufig (300s Limit). Alternative: `git archive` + ssh pipe: `git archive HEAD | ssh user@host 'tar xzf - -C /path'` oder kleine Dateien einzeln per `ssh 'cat > file' < localfile`.

**Build workflow**:
1. Verify SDK: `ls SDK/connectIQ/ | head -5` (must be non-empty)
2. Verify device: check `~/.Garmin/ConnectIQ/Devices/<device>/compiler.json` for `deviceId`
3. Set `GARMIN_SDK_HOME` or ensure SDK is in `~/.Garmin/ConnectIQ/Sdks/`
4. Create symlink `~/.Garmin/ConnectIQ/Devices` → device definitions directory if not in default location
5. Compile: `monkeyc -o app.prg -f monkey.jungle -y developer_key -d <device> -a api.db -b api.mir`
6. Simulator: `monkeydo app.prg` or `simulator` GUI
