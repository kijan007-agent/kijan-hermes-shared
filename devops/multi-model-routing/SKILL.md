---
name: multi-model-routing
description: Multi-model LLM routing, on-demand lifecycle management, health scoring, and resource-aware model selection for local LLM orchestrators.
version: 1.0.0
metadata:
  hermes:
    tags: [llm, orchestration, multi-model, routing, llama-cpp, config]
---

# Multi-Model LLM Routing & Orchestration

> Load this skill when configuring or debugging multi-model LLM orchestration, resource-aware model routing, or auxiliary model routing through an orchestrator.

## Core Architecture

```
Request -> Intent Classification -> Candidate Scoring -> Weighted Selection -> Model Routing
  (LLM/keyword)    (RAM fit check)     (health + weight)   (load if needed)
```

- **Always-on model** starts at boot, never stopped (smallest model)
- **On-demand loading**: check RAM before loading; evict LRU if insufficient
- **Idle unloading**: background task every 60s stops models idle > IDLE_TIMEOUT
- **Direct llama-server management**: spawn/kill; no LiteLLM proxy

## Config Structure

See `references/config-schema.md` for complete field reference.

Key sections in `config.yaml`:
- `global` - RAM thresholds, idle timeout, health scoring, hardware profile
- `dispatch` - context-aware classification, keyword fallback settings
- `hardware` - CPU cores, NUMA nodes, shared RAM, GPU type
- `model_preload` - models to keep loaded at startup
- `models` - per-model config with roles, weights, health, tokenizer

## Resource-Aware Lifecycle

1. Check `available_ram < model_size + headroom` before loading
2. If insufficient, evict LRU non-always-on model
3. Start llama-server, wait for `/health` readiness
4. Background idle monitor unloads models idle > IDLE_TIMEOUT when RAM tight

## Intent Classification Pipeline

1. **LLM classifier** (phi4mini) classifies as code/smart/fast/vision + complexity 1-3
2. **Keyword fallback** (EN+DE lists, message length heuristic) on LLM error/timeout
3. **Weighted model selection** from candidates matching role + RAM fit

## Weighted Model Selection

- Each model: `weight` (higher = preferred) + `health_score` (0-1)
- Health = `success_rate * 0.6 + latency_normalized * 0.4`
- Auto-disable below threshold; re-enable after cooldown
- Already-running models preferred to avoid cold starts

## Auxiliary Routing Pattern

Route auxiliaries through the orchestrator to leverage its routing intelligence:

```yaml
auxiliary:
  <name>:
    provider: orchestrator
    model: <model_name>
    base_url: http://127.0.0.1:<port>/v1
    timeout: <seconds>
```

Model selection guideline:
- **Vision tasks** -> VL model (qwen3_vl_30b)
- **Heavy reasoning** -> qwen36_35b (best general model)
- **Compression** -> qwen36_27b (balanced speed/quality)
- **Session search** -> qwen35_9b (speed over quality)
- **Skills hub** -> qwen25_coder_7b (fast, coder-capable)
- **Approval** -> qwen36_35b (safety evals need reasoning)
- **MCP** -> qwen36_35b (tool-use needs code capability)
- **Title generation** -> phi4mini (speed over quality)
- **Curator** -> qwen36_35b (heavy reasoning for lifecycle decisions)

## Key Pitfalls

- **Unified RAM (no VRAM)**: AMD Ryzen AI shared RAM - set `ram_headroom_gb` conservatively (16GB+)
- **NPU not supported by llama.cpp**: XDNA2 NPU requires ONNX; GGUF only uses CPU+Vulkan
- **Docker GPU passthrough**: Needs `/dev/dri/renderD128`, video/render group, `mesa-vulkan-drivers`, `network_mode: host`
- **WSL Vulkan**: Mount `/usr/lib/wsl` + `LD_LIBRARY_PATH` includes WSL Vulkan libs
- **Split GGUF files**: Only register `-00001-of-NNNNN` shards
- **mmproj for VL models**: Must specify `--mmproj` in `extra_args`

## Cline Integration

```
Base URL: http://localhost:9100/v1
API Provider: openai
API Key: dummy (non-empty)
Model: auto
```

## Related Files

- `references/config-schema.md` - Complete config field reference
- `references/health-scoring-algorithm.md` - Health scoring implementation details