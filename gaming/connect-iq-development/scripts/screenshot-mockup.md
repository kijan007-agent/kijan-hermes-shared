# Pillow-Based Screenshot Mockups for Connect IQ Apps

When the Connect IQ SDK (monkeydo/simulator) is NOT installed, generate visual mockups using Pillow instead of live rendering.

## Technique

1. **Analyze source code** for UI structure:
   - `resources/layouts/*.xml` — layout positions, sizes, drawable IDs
   - `resources/strings/strings.xml` — labels, text values
   - `resources/drawables/drawables.xml` — color definitions (COLOR_WHITE, COLOR_GREEN, etc.)
   - `source/*Screen*.mc` — `onUpdate()` / `onPostDraw()` methods (actual rendering logic)
   - `source/*Drawable*.mc` — shared drawing helpers (e.g., EnergyDrawable.draw)

2. **Extract layout constants**:
   - Screen dimensions (390×450 = Venu 3 / Fenix 7 / Epix 2)
   - Font names (FONT_SMALL, FONT_TINY, FONT_NUMBER_MEDIUM, etc.)
   - Color constants → hex values (COLOR_WHITE=#FFFFFF, COLOR_ORANGE=#FFA500, etc.)
   - Text positioning (cx/cy coordinates, justify modes)

3. **Generate Pillow script** (`scripts/generate_screenshots.py`):
   - Map Monkey C fonts → Pillow font sizes (FONT_XTINY=10px, FONT_TINY=12px, FONT_SMALL=16px, FONT_NUMBER_MEDIUM=56px)
   - Recreate layout using PIL ImageDraw (text, circles, rectangles, ellipses)
   - Apply correct colors, positions, and text content
   - Output PNG files

## Key Mapping

| Monkey C | Pillow Font Size |
|----------|------------------|
| FONT_XTINY | 10 |
| FONT_TINY | 12 |
| FONT_SMALL | 16 |
| FONT_MEDIUM | 20-24 |
| FONT_LARGE | 28 |
| FONT_NUMBER_HOT | ~80 |
| FONT_NUMBER_MEDIUM | 56 |

| Monkey C Color | Hex |
|---------------|-----|
| COLOR_WHITE | (255, 255, 255) |
| COLOR_BLACK | (0, 0, 0) |
| COLOR_YELLOW | (255, 255, 0) |
| COLOR_ORANGE | (255, 165, 0) |
| COLOR_RED | (255, 0, 0) |
| COLOR_GREEN | (0, 200, 0) |
| COLOR_DK_GRAY | (40, 40, 40) |
| COLOR_LT_GRAY | (169, 169, 169) |
| COLOR_BLUE | (0, 0, 255) |

## Pitfalls

- **Pillow `anchor` parameter**: Older Pillow versions don't support `anchor='ml'`. Use manual offset calculation instead: `bbox = draw.textbbox((0,0), text, font=font)` then `ax = cx - tw//2`.
- **Font fallback**: Try multiple system paths; fall back to `ImageFont.load_default()` (very small).
- **Text metrics**: Always use `textbbox()` before `text()` to get accurate width/height for centering.
- **Screen dimensions**: Match target device — Venu 3/Fenix 7/Epix 2 = 390×450, Forerunner 265 = 260×220, etc.

## Delivery

Generate all mockups to `kpt-app-ciq/screenshots/` directory, then deliver via Telegram `MEDIA:` protocol.
