# Health Scoring Algorithm

Tracks per-model performance for health-aware routing.

## Score Components
- **Success Rate (60%)**: Ratio of successful requests to total requests
- **Latency (40%)**: Normalized latency comparison across models in same role

## Update Mechanism
- **Per-request EMA**: `weight[role][model] = 0.8 * old + 0.2 * new_tps`
- **Batch recalc**: Self-improve loop recomputes from full outcome history

## Auto-Disable / Re-enable
- Model disabled when `health_score < health_disable_threshold` (default 0.5)
- Disabled models excluded from routing candidates
- Re-enable cooldown: `health_reenable_cooldown` seconds (default 900)
- On re-enable, health resets to 1.0 and re-trains from fresh data

## Implementation
```python
def _update_weight(self, model, role, tps):
    if tps <= 0:
        return
    prev = self.model_weights[role].get(model, tps)
    self.model_weights[role][model] = round(0.8 * prev + 0.2 * tps, 2)

def _pick_model(self, role, running, available_gb, large=False, running_only=False):
    # ... filter candidates ...
    all_candidates = [
        n for n, m in self.models.items()
        if role in m.roles and m.full_path.exists() and fits(n)
        and n not in self.disabled
    ]
    weights = self.model_weights.get(role, {})
    # ... rank by weight * health_score ...
```
