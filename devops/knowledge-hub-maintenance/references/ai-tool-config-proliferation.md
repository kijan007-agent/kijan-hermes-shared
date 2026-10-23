# AI Tool Config Proliferation Pattern

Detected 2026-06-21 in Kijan monorepo `/workspace/Github/KijanPersonalTracker-hermes/`.

## File Types Found

| Config File | Count | Location |
|-------------|-------|----------|
| `.rooignore` | 4 | monorepo root + kpt-app-ciq, kpt-common-barrels-ciq, kpt-datafield-ciq |
| `.roorules` | 3 | monorepo root + kpt-app-ciq, kpt-datafield-ciq |
| `.clineignore` | 1 | monorepo root |
| `.clinerules` | 1 | monorepo root |
| `.claudeignore` | 1 | monorepo root |
| `.continueignore` | 1 | monorepo root |

## Pattern

- Each AI tool uses its own config file format (ignore + rules)
- Config files appear at monorepo root AND per-product directories
- kpt-backend has NO per-product AI config (only monorepo-level `.rooignore` applies)
- `.continue` directory exists at kpt-backend root (0 bytes — placeholder)
- `.gitignore` at root covers monorepo-level exclusions
- Config files are additive: root-level configs apply to all submodules

## Implication for Knowledge Hub

When counting "AI tool config files" in Knowledge Hub status:
- Count per-product configs separately (not just root)
- Note that kpt-backend intentionally lacks per-product AI configs
- `.rooignore` at root (622 bytes) is the authoritative exclusion list
- New config types (`.roorules`, `.clineignore`, etc.) should be tracked as they appear
