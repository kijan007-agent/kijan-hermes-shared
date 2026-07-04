---
name: benchmarking
description: "Measure local model performance (GGUF/Safetensor), generate status reports, compare runs, deliver results via cron."
version: 1.0.0
author: Jan + Hermes
license: MIT
metadata:
  hermes:
    tags: [benchmarking, performance, cron, telegram, reporting]
    related_skills: []
---

# Benchmarking — Local Model Performance Measurement

Measure local GGUF/Safetensor models, generate status reports, compare runs.

## Files

- `/data/ai/benchmark_models.py` — Core engine (llama.cpp/pyllama.cpp, measures tok/s)
  - `--full` — All models, 5 iterations, full metrics
  - `--quick` — Fast test, 1 iteration, TPS median only
  - `--compare` — Compare with last run
  - `--json` — Output raw JSON to stdout
- `/data/ai/benchmark_status.py` — Report generator from `benchmark_results.json`
  - `--by-source` — Group by backend (llama.cpp, vLLM, etc.)
  - `--summary` — One-line summary
  - `--changes` — Delta vs last report
  - `--html` — Generate HTML dashboard
  - `--diff` — Pipe-friendly `model|tps|source|timestamp` format
  - `--json` — Raw benchmark_results.json
  - `--save` — Persist report for diff comparison
- `/data/ai/benchmark_config.yaml` — Model list, hardware profile, presets
- `/data/ai/ARCHITECTURE.md` — Full system design document

## Quick Usage

```bash
# Run full benchmark
python3 /data/ai/benchmark_models.py --full

# Quick status
python3 /data/ai/benchmark_status.py --summary

# Grouped report
python3 /data/ai/benchmark_status.py --by-source --save

# HTML dashboard
python3 /data/ai/benchmark_status.py --html
```

## Cron Job Pattern

```bash
# Status report (30 min)
hermes cron create \
  --name "benchmark-status" \
  --schedule "30m" \
  --deliver "origin" \
  --prompt "python3 /data/ai/benchmark_models.py 2>/dev/null; python3 /data/ai/benchmark_status.py --by-source --save 2>/dev/null"

# Telegram delivery (add chat_id)
hermes cron create \
  --name "benchmark-telegram" \
  --schedule "30m" \
  --deliver "telegram:<chat_id>[:<thread_id>]" \
  --prompt "python3 /data/ai/benchmark_status.py --summary 2>/dev/null"

# Full daily update (off-peak)
hermes cron create \
  --name "benchmark-daily" \
  --schedule "daily" \
  --deliver "origin" \
  --prompt "python3 /data/ai/benchmark_models.py --full 2>/dev/null"
```

## Pitfalls

- Benchmarking all models takes 10-60 min, consumes 16-64 GB RAM — run during maintenance windows
- `llama.cpp` / `pyllama-cpp-python` must be installed: `pip install pyllama-cpp-python`
- Results written to `/data/ai/benchmark_results.json` — always reference this file
- Compare mode requires a previous `last_report.txt` in `/data/ai/statistics/`
- Model paths in `benchmark_config.yaml` must be absolute — relative paths fail in cron context
- Cron delivery defaults to `origin` (terminal) — use `telegram:` prefix for Telegram, `gateway:` for Hermes Gateway
- For Telegram delivery, the bot must already be connected to the target chat; chat_id starts with `-100`

## Deliver Formats

| Prefix | Target | Example |
|--------|--------|---------|
| `origin` | Terminal (this chat) | `--deliver origin` |
| `telegram:` | Telegram | `--deliver telegram:-1001234567890` |
| `gateway:` | Hermes Gateway API | `--deliver gateway:8080` |
| `file:` | Local file | `--deliver file:/tmp/report.txt` |
| `webhook:` | HTTP endpoint | `--deliver webhook:https://hook.site/...` |

## Data Flow

```
benchmark_models.py
  ├── benchmark_results.json (raw results)
  └── statistics/
      ├── model_stats/ (per-model aggregates)
      ├── metrics/ (time-series)
      └── last_report.txt (saved report for diff)
```

## Integration with Hermes Agent

- Results can feed into model health scoring (TPS threshold → health_score)
- Top-performing models should be in `config.yaml` model_preload array
- Benchmark config should stay in sync with available models in `/data/ai/models/`
- Dashboard HTML at `/data/ai/dashboard/benchmark.html` for browser access
