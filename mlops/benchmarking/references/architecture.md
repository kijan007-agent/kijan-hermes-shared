# Benchmark-Integration mit Hermes Agent — Design-Dokument

## System-Übersicht

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BENCHMARK INFRASTRUCTURE                         │
│                                                                     │
│  ┌──────────────┐   ┌──────────────┐   ┌───────────────────────┐  │
│  │ benchmark_   │   │ benchmark_   │   │ benchmark_status.py   │  │
│  │ models.py    │──▶│ cache.json   │   │ (Report Generator)    │  │
│  └──────────────┘   └──────┬───────┘   └──────────┬────────────┘  │
│  ┌──────────────┐   ┌──────▼───────┐   ┌──────────▼────────────┐  │
│  │ benchmark_   │   │ statistics/  │   │ benchmark_dashboard/  │  │
│  │ config.yaml  │   │              │   │                       │  │
│  └──────────────┘   └──────────────┘   └───────────────────────┘  │
│                     ┌──────────────┐                              │
│                     │  CRON JOBS   │                              │
│                     │              │                              │
│                     │  • benchmark │                              │
│                     │    update    │                              │
│                     │  • status    │                              │
│                     │  • dashboard │                              │
│                     │  • report    │                              │
│                     └──────────────┘                              │
│                     ┌──────────────┐                              │
│                     │ DELIVERY     │                              │
│                     │              │                              │
│                     │  • Terminal  │                              │
│                     │  • Telegram  │                              │
│                     │  • Gateway   │                              │
│                     └──────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

## Architektur-Komponenten

### benchmark_models.py (Core Engine)
- Lädt GGUF/Safetensor-Modelle via llama.cpp/pyllama.cpp
- Misst Token/s über mehrere Iterationen
- Speichert Ergebnisse in `benchmark_results.json`

### benchmark_status.py (Report Generator)
- CLI-Modi: `--by-source`, `--summary`, `--changes`, `--html`, `--diff`, `--json`
- Generiert Text, HTML und JSON-Reports
- Vergleicht mit letztem Report (`last_report.txt`)

### Cron-Jobs
- `benchmark-status-report` (30 min) — Statusreport an origin
- `benchmark-update` (täglich) — Vollbenchmark
- `dashboard-refresh` (stündlich) — HTML aktualisieren

## Kompatibilität mit Hermes Agent

### ✅ Voll kompatibel
- Python-Skripte mit Standard-Dependencies
- Cron-Job Integration via hermes cron
- JSON-Ausgabe native kompatibel
- CLI-Schnittstelle terminal-fähig
- Speicherlayout `/data/ai/`

### ⚠️ Bedingungen
- llama.cpp/pyllama.cpp muss installiert sein
- CPU-Last: belegt alle Kerne während Benchmark
- RAM: ~16-64 GB je nach Modell
- Laufzeit: 10-60 Min pro voller Lauf

## Workflow-Empfehlungen

### Täglicher Betrieb
```
00:00  → benchmark-update (full)
00:30  → status report
06:00  → status report
12:00  → status report
18:00  → status report
22:00  → dashboard refresh
```

### Manuelles Triggern
```bash
hermes cron run benchmark-update
python3 /data/ai/benchmark_models.py --quick
python3 /data/ai/benchmark_status.py --top 5
```

## Datenfluss

```
benchmark_models.py
  → benchmark_results.json (Rohergebnisse)
  → statistics/model_stats/ (aggregiert)
  → statistics/metrics/ (Zeitreihe)
  → benchmark_status.py → Terminal/HTML/JSON
  → Dashboard: metrics.json + index.html
```
