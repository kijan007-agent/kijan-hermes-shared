# Connect IQ Simulator Linux Debug — Triage Patterns

## Compile Error Triage

### Symptom: 100+ "Undefined symbol: :X" errors
**Root cause**: `monkey.jungle` missing `test` in `excludeAnnotations`
- Monkeyc kompiliert `(:test)`-annotierte Dateien standardmäßig mit
- Test-Code enthält oft Methoden die nicht in produktiven SDKs existieren
- **Fix**: `base.excludeAnnotations = prod;staging;test`

### Symptom: 500-2000+ "untyped" / "Cannot determine type" errors
**Root cause**: SDK 9.1.0 ist deutlich strikter als SDK 8.x
- Typen-Checking ist aggressiver
- Implizite Konvertierungen die in älteren SDKs funktionierten → Fehler in SDK 9.x
- **Prüfung**: Mit mindestens zwei SDKs testen (z.B. 8.4.1 + 9.1.0)
- **Fix-Strategie**: Wenn nur SDK 9.x fehlschlägt → Code ist für älteres SDK geschrieben

### Symptom: "Undefined symbol" für bekannte API-Methoden
**Root cause**: Barrel source files not in `base.sourcePath`
- Connect IQ builds fail when barrel source files are not in `base.sourcePath`
- **Fix**: Verify barrel path resolution: `ls source/ ../barrel-name/source/`
- Verify jungle file: `cat monkey.jungle | grep sourcePath`

## SDK Compatibility Matrix

| SDK | Striktheit | Typen-Checking | Test-Annotation |
|-----|-----------|---------------|-----------------|
| 8.4.1 | Medium | Standard | Compiliert test-Code |
| 9.1.0 | Hoch | Aggressiv | Compiliert test-Code |
| Älter (< 8.0) | Niedrig | Locker | Compiliert test-Code |

## Simulator Library Dependencies (Linux)

### Required Libraries (Debian 13)
- `libwebkit2gtk-4.0-37` (Ubuntu Jammy .deb)
- `libjavascriptcoregtk-4.0-18` (Ubuntu Jammy .deb)
- `libjpeg8` (Ubuntu Jammy .deb)
- `libwoff1` (Ubuntu Jammy .deb)
- `libwoff2dec.so.1.0.2` (self-compiled from google/woff2)
- `libsoup-2.4` (via Jammy libwebkit)
- Java 11+ (JDK)

### Library Conflict Resolution
1. Jammy libs FIRST in `LD_LIBRARY_PATH`
2. Remove system libwebkit symlinks if they conflict
3. Self-compile `libwoff2dec.so` from source — Debian has incompatible woff2

### Xvfb Requirements
- `Xvfb :99 -screen 0 800x600x24 -ac &`
- `export DISPLAY=:99`
- Verify: `xdpyinfo | grep -A2 "screen #0"`

### Screenshot Capture
```bash
import -window root /tmp/simulator_screenshot.png
# Or specific window:
import -window "Connect IQ Simulator" /tmp/screenshot.png
```