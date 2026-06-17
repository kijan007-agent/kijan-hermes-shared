# SDK Installation Verification

## Quick Check (after SDK install)
```bash
# Inside the machine where SDK is installed
find ~/.Garmin -name 'monkeyc' -o -name 'api.db' 2>/dev/null
# Should output paths like:
# /home/hermes/.Garmin/ConnectIQ/Sdks/connectiq-sdk-linux-8.4.1/bin/monkeyc
# /home/hermes/.Garmin/ConnectIQ/Sdks/connectiq-sdk-linux-8.4.1/bin/api.db

# Check connectIQ directory
ls ~/.Garmin/ConnectIQ/Sdks/connectiq-sdk-linux-8.4.1/connectIQ/ | head -5
# Should list device-specific dirs (epix2pro, fenix, etc.)

# Verify monkeyc works
~/.Garmin/ConnectIQ/Sdks/connectiq-sdk-linux-8.4.1/bin/monkeyc --version
```

## Distrobox-specific
SDK Manager AppImage runs inside Distrobox container `garmin-sdk` (ubuntu:22.04).
AppImage needs GUI — no CLI install mode.

## Manual SDK install via zip
1. Download from https://developer.garmin.com/connect-iq/sdk/
2. Extract: `unzip connectiq-sdk-linux-8.4.1.zip -d ~/.Garmin/ConnectIQ/Sdks/`
3. Verify: `ls ~/.Garmin/ConnectIQ/Sdks/connectiq-sdk-linux-8.4.1/connectIQ/` must be non-empty
4. Set GARMIN_SDK_HOME or symlink into ~/.Garmin/ConnectIQ/Sdks/