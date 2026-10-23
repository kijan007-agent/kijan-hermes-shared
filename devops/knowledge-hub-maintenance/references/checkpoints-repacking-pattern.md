# Checkpoints Repacking Pattern

**First observed:** 2026-07-26 23:31 UTC
**Status:** Active pattern

## Pattern

When checkpoints change, file count and size can diverge in unexpected ways:

| Scenario | File Count | Size | Meaning |
|----------|-----------|------|---------|
| Normal growth | ▲ | ▲ | More data accumulated |
| Normal cleanup | ▼ | ▼ | Data removed |
| **Repacking** | ▲ | ▼ | More files, less total size — internal format change or fragmentation |
| **Consolidation** | ▼ | ▲ | Fewer files, more total size — files merged or format expanded |

## Example (Jul 26)

- **Before (Jul 24):** 69 MB, 4,621 files → avg 15.4 KB/file
- **After (Jul 26):** 64.8 MB, 7,191 files → avg 9.2 KB/file
- **Change:** ▲+570 files, ▼-4.2 MB, avg file size dropped 40%
- **Interpretation:** Hermes checkpoint format changed — more granular files, smaller individual size. Likely checkpoint repacking or granularity change.

## Diagnostic Steps

```bash
# 1. Measure current state
du -sh /home/jan/.hermes/checkpoints/
find /home/jan/.hermes/checkpoints/ -type f | wc -l

# 2. Per-subdirectory breakdown
for dir in /home/jan/.hermes/checkpoints/*/; do
  echo "=== $dir ==="
  du -sh "$dir"
  find "$dir" -type f | wc -l
done

# 3. File size distribution
find /home/jan/.hermes/checkpoints/ -type f -printf '%s\n' | sort -n | tail -5
find /home/jan/.hermes/checkpoints/ -type f -printf '%s\n' | sort -n | head -5
```

## Alert Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| File count change | >100 files/run | >500 files/run |
| Size change | >5 MB/run | >50 MB/run |
| Avg file size < 1KB | Check fragmentation | Check for empty/minimal files |
| Avg file size > 1MB | Check for oversized checkpoints | Consider compression |

## Related

- State.db growth often coincides with checkpoint changes — monitor both together
- Checkpoint repacking may indicate Hermes internal changes (version upgrade, config change)
- If file count grows without size growth: possible orphaned empty/minimal files
