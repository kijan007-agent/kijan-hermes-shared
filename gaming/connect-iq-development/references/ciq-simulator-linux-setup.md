# Connect IQ Simulator on Linux VM — Installation Guide

## Prerequisites
- Debian 12/13 (Ubuntu 24.04 compatible)
- Xvfb: `sudo apt-get install -y xvfb`
- Java 11+: `sudo apt-get install -y default-jdk-headless`

## Step 1: Install Ubuntu Jammy (22.04) Libraries on Debian 13

Debian 13 lacks `libwebkit2gtk-4.0-37` (only has `libwebkit2gtk-4.1`). Must install Jammy .deb files.

```bash
# Download and extract libwebkit2gtk-4.0-37
cd /tmp
dpkg -x libwebkit2gtk-4.0-37*.deb webkit40_extract
dpkg -x libjavascriptcoregtk-4.0-18*.deb jsc40_extract
dpkg -x libjpeg8*.deb jpeg_extract
dpkg -x libwoff1*.deb woff_extract

# Create combined lib path
mkdir -p /tmp/webkit_combined
cp webkit40_extract/usr/lib/x86_64-linux-gnu/*webkit2gtk* jsc40_extract/usr/lib/x86_64-linux-gnu/*javascriptcore* /tmp/webkit_combined/
cp jpeg_extract/usr/lib/x86_64-linux-gnu/libjpeg.so* /tmp/webkit_combined/
cp woff_extract/usr/lib/x86_64-linux-gnu/libwoff1.so* /tmp/webkit_combined/
```

## Step 2: Build libwoff2dec.so.1.0.2 (from source)

Debian 13 has newer woff2 than what Jammy's libwebkit expects. Must compile from source.

```bash
cd /tmp
git clone https://github.com/google/woff2.git
cd woff2
make clean all
cp lib/woff2_dec /tmp/webkit_combined/libwoff2dec.so.1.0.2
# Also create symlink for older naming:
ln -s libwoff2dec.so.1.0.2 libwoff2dec.so.1
```

## Step 3: Fix libsoup Conflict

Debian 13 ships `libsoup-3.0` but Jammy's libwebkit links against `libsoup-2.4`.

```bash
# Remove conflicting symlinks if they exist
sudo rm -f /usr/lib/x86_64-linux-gnu/libwebkit2gtk*  # if installed via apt

# Ensure Jammy libs FIRST in LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/tmp/webkit40_extract/usr/lib/x86_64-linux-gnu:/tmp/jsc40/usr/lib/x86_64-linux-gnu:/tmp/webkit_combined
```

## Step 4: Start Xvfb

```bash
Xvfb :99 -screen 0 800x600x24 -ac &
export DISPLAY=:99
# Verify: xdpyinfo | grep -A2 "screen #0"
```

## Step 5: Launch Simulator

```bash
export LD_LIBRARY_PATH=/tmp/webkit40_extract/usr/lib/x86_64-linux-gnu:/tmp/jsc40/usr/lib/x86_64-linux-gnu:/tmp/webkit_combined
export DISPLAY=:99

/workspace/frameworks/Garmin/ConnectIQ/Sdks/connectiq-sdk-lin-*/bin/simulator &
```

## Step 6: Capture Screenshots

```bash
# Install import (imagemagick)
sudo apt-get install -y imagemagick

# Take screenshot
import -window root /tmp/simulator_screenshot.png

# Or capture specific window
import -window "Connect IQ Simulator" /tmp/screenshot.png
```

## Step 7: Compile App

```bash
# Generate certificate (one-time)
mkdir -p /tmp/ciq_cert
openssl genrsa -out /tmp/ciq_cert/key.pem 4096
openssl pkcs8 -topk8 -inform PEM -outform DER -in /tmp/ciq_cert/key.pem -out /tmp/ciq_cert/key.der -nocrypt

# Compile
cd /workspace/Github/KijanPersonalTracker-hermes/kpt-app-ciq
/workspace/frameworks/Garmin/ConnectIQ/Sdks/connectiq-sdk-lin-*/bin/monkeyc \
  -f monkey.jungle \
  -d fenix7 \
  -o /tmp/kpt_app.prg \
  -y /tmp/ciq_cert/key.der \
  -t -l 3

# Install via monkeydo
/workspace/frameworks/Garmin/ConnectIQ/Sdks/connectiq-sdk-lin-*/bin/monkeydo /tmp/kpt_app.prg
```

## Troubleshooting

### "ERROR: Invalid device id specified"
- SDK `connectIQ/` directory is missing or empty
- Verify: `ls connectIQ/ | head -5` (must be non-empty)
- Device must appear in `devices.xml` inside `monkeybrains.jar`

### "ERROR: The private key was not specified"
- Add `-y <path_to_der_key>` to monkeyc command

### Simulator crashes on startup
- Missing libwoff2dec: `export LD_LIBRARY_PATH=/tmp/webkit_combined:$LD_LIBRARY_PATH`
- Missing libsoup-2.4: Ensure LD_LIBRARY_PATH points to Jammy libs first
- Wrong DISPLAY: `export DISPLAY=:99`

### Compile "untyped" / "Cannot determine type" errors
- **SDK 9.1.0 ist deutlich strikter** als ältere SDKs — 500-2000+ Fehler möglich
- Massive "untyped", "Cannot determine type", type mismatch errors
- **Prüfung**: Immer mit mindestens zwei SDKs testen (8.x + 9.x)
- **⚠️ Test-Code ausschließen**: `monkey.jungle` muss `test` in `excludeAnnotations` haben — `base.excludeAnnotations = prod;staging;test`. Ohne `test`: alle `(:test)`-annotierten Dateien werden kompiliert und verursachen Fehler durch nicht-existente Methoden (`:setCurrentScreen` etc.)
- **`:setCurrentScreen` ist KEINE Connect IQ Methode** — falsche Syntax in Test-Code. Korrekter Aufruf: `WatchUi.setActiveScreen()` oder `ScreenManager.setCurrentScreen()`. Die Symbol-Referenz `:kijanActivityTracker` ist ein SymbolTable-Key, KEIN Methodenname.
- **Fix-Strategie**: Wenn nur SDK 9.x fehlschlägt → Code ist für älteres SDK geschrieben. Nicht blind fixen!
- Solutions:
  1. Use older SDK (8.x) if compatible with target devices
  2. Fix all type annotations in source code
  3. Check SDK compatibility matrix for target device API level

### "symbol lookup error: libsoup-3.0"
- System libsoup-3.0 is being picked up instead of Jammy's libsoup-2.4
- Fix: Put Jammy libs FIRST in LD_LIBRARY_PATH
- Or remove system libwebkit symlinks: `sudo rm -f /usr/lib/x86_64-linux-gnu/libwebkit2gtk*`

### Xvfb display not working
- `xdpyinfo` fails → Xvfb not running or wrong display
- `Xvfb :99 -screen 0 800x600x24 &` then `export DISPLAY=:99`
