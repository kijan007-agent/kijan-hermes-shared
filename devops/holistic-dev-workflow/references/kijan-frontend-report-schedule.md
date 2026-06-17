# Kijan Frontend Report Schedule

> Cron-configured report times and formats for Kijan Personal Tracker frontend monitoring.

## Report Times

| Report | Time | Content | Format |
|--------|------|---------|--------|
| Morgenbriefing | 07:30 | Facts, RCA, Mockups, Questions/Blockers | 🌅 + Fakten + Blocker + Mockups + Nächste Schritte |
| Task Overview | every 90m | Done / In Progress / Next | 📊 + ✅ / 🔄 / ⏭️ |
| Status Report | 12:30 + 18:00 | Overall progress, files, blockers | 📊 + Status % + files + blockers |
| Night Summary | 07:30 next day | Night summary + progress (included in morning briefing) | In morning briefing |

**Night:** No reports between 22:00 and 07:30.

## Cron Jobs

- `kijan-frontend-morning-briefing` — 07:30
- `kijan-frontend-task-overview` — every 90m
- `kijan-frontend-status-1230` — 12:30
- `kijan-frontend-status-1800` — 18:00
