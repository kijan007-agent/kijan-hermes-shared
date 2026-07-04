# Orchestrator Config Schema Reference

Complete field reference for orchestrator `config.yaml`.

## Global Section

| Field | Type | Default | Description |
|---|---|---|---|
| ram_headroom_gb | float | 16.0 | GB headroom to keep after loading |
| unload_threshold_gb | float | 80.0 | Free RAM below which idle models unload |
| idle_timeout | int | 600 | Seconds before idle models eligible for unload |
| num_workers | int | 4 | Concurrency |
| startup_wait | int | 60 | Seconds to wait for model readiness |
| self_improve_interval | int | 3600 | Self-improvement loop interval |
| always_on_model | string | phi4mini | Tiny model kept loaded at boot |
| tools_model | string | qwen36_35b | Default tool-capable model |
| ram_auto_disable | bool | true | Auto-disable large models on low RAM |
| ram_auto_disable_threshold_gb | float | 20.0 | Disable models >10B when RAM < this |
| ram_auto_enable_threshold_gb | float | 60.0 | Re-enable when RAM recovers above this |
| health_score_enabled | bool | true | Enable health scoring |
| health_disable_threshold | float | 0.5 | Auto-disable models with health < this |
| health_reenable_cooldown | int | 900 | Seconds before re-enabling disabled model |
| health_success_rate_weight | float | 0.6 | Weight for success rate in health |
| health_latency_weight | float | 0.4 | Weight for latency in health |

## Hardware Section

| Field | Type | Description |
|---|---|---|
| name | string | Hardware profile identifier |
| cpu_cores | int | CPU core count |
| numa_nodes | int | NUMA node count |
| shared_ram_gb | int | Total shared RAM |
| gpu_type | string | GPU architecture |
| dedicated_vram | bool | Whether GPU has dedicated VRAM |

## Model Preload Section

List of model names to keep loaded at startup. Reduces cold start latency.

## Model Entry Fields

| Field | Type | Default | Description |
|---|---|---|---|
| path | string | — | Relative to MODELS_DIR |
| port | int | — | llama-server port |
| ctx_size | int | 8192 | Context window (tokens) |
| gpu_layers | int | 999 | Layers to offload (999=all) |
| size_gb | float | 8.0 | Approx loaded RAM |
| memory_footprint_gb | float | 0.0 | Weights + KV cache |
| context_window_safe | int | 8192 | Max safe context |
| preferred_context_size | int | 4096 | Typical use size |
| tokenizer_type | string | "" | Tokenizer for token counting |
| roles | list | [] | fast, code, smart, always_on, vision |
| tool_capable | bool | false | Handles structured tool calls |
| thinking | bool | false | Enable preserve-thinking |
| weight | float | 5.0 | Selection weight |
| health_score | float | 1.0 | Initial health (0-1) |
| extra_args | list | [] | llama-server flags |
