# Missing Repos Pattern — 2026-07-12

Pattern detected: critical repos can disappear from both /workspace/ and .hermes/ without triggering alerts.

## Affected repos (as of 2026-07-12)
- KijanPersonalTracker-feature — was /workspace/KijanPersonalTracker-feature
- KijanPersonalTracker-hermes — was /workspace/KijanPersonalTracker-hermes
- kijanpersonal-tracker — was /workspace/kijanpersonal-tracker
- kpt-doc — was /workspace/kpt-doc
- 9 ESP32 repos — were under /workspace/.hermes/ (ESP32-*, kijan-rc-*, EdgeTxSync)

## Detection
All 4 KijanPersonalTracker repos and 9 ESP32 repos returned [MISSING] from /workspace/.
No traces in backups or pastes (backups only contain pre-update zip files).
Git unavailable in sandbox environment — cannot check branch state or reflogs.

## Root cause (unknown)
Could be: workspace cleanup, migration, sandbox reset, or manual deletion.
Requires user investigation.

## Impact
- Knowledge Hub divergence tracking completely disabled
- ESP32 development capability lost
- KijanPersonalTracker merge history lost
