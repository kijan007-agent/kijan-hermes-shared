# Ubuntu VM SDK Setup — Session 2026-05-16

## New VM Provisioning (100.66.141.92)

### User Setup
- SSH key copied via `sshpass -p 'hermes007' ssh-copy-id hermes@100.66.141.92`
- Passwordless SSH login verified
- sudo: password `hermes007`

### VNC Setup
```bash
# Install
sudo apt-get install -y xvfb tigervnc-standalone-server xfce4-session xfce4-terminal xfwm4 xfce4-panel xfce4-settings xdg-utils

# VNC password (non-interactive via python)
python3 -c "import base64; open('/tmp/vncpw','wb').write(base64.b64decode('aGVybWVzMDA3'))"
echo hermes007 | vncpasswd -f > ~/.vnc/passwd && chmod 600 ~/.vnc/passwd

# Start with external binding (CRITICAL: -localhost no)
vncserver :1 -geometry 1920x1080 -depth 24 -localhost no -PasswordFile ~/.vnc/passwd

# Verify external binding
ss -tlnp | grep 5901  # should show 0.0.0.0:5901, not 127.0.0.1:5901
```

**Connection:** `100.66.141.92:5901` / Password: `hermes007`

### SDK Dependencies
```bash
sudo apt-get install -y default-jdk-headless  # Java for monkeyc
```

### SDK Manager
- Run via VNC GUI: `~/bin/sdkmanager`
- Installs SDK to `~/.Garmin/ConnectIQ/Sdks/`
- SDK Manager generates developer key to `~/developer_key`

### Build Artifacts
- **monkeyc:** `~/.Garmin/ConnectIQ/Sdks/connectiq-sdk-lin-9.1.0-2026-03-09-6a872a80b/bin/monkeyc`
- **api.db:** Same bin/ directory
- **Devices:** `~/.Garmin/ConnectIQ/Devices/`
- **Developer key:** `~/developer_key`
- **Build command:**
```bash
cd /home/hermes/Github/kpt-app-ciq
JAVA_HOME=/usr/lib/jvm/default-java \
  /home/hermes/.Garmin/ConnectIQ/Sdks/connectiq-sdk-lin-9.1.0-2026-03-09-6a872a80b/bin/monkeyc \
  -o /tmp/kpt_app.prg -f monkey.jungle -y /home/hermes/developer_key -d epix2pro51mm
```

### Barrel Modules
- Located at: `kpt-common-barrels-ciq/source/`
- Files: `KijanAlerts.mc`, `KijanDeviceId.mc`, `KijanNet.mc`, `KijanPhaseTimer.mc`, `StressCalculator.mc`
- Referenced in `monkey.jungle` via `base.sourcePath`
- **Must be copied to VM** when deploying source code

### Common Build Errors
1. `java: command not found` → Install `default-jdk-headless`
2. `Undefined symbol ':' detected` → Barrel modules missing from build path
3. `Invalid device id` → SDK `connectIQ/` directory empty or missing
4. `launcher icon can't be found` → Resources directory missing drawables

### SCP Workaround
- Large SCP transfers to new VM may timeout
- Use `tar | ssh` pipe or break into smaller chunks
- Git archive → pipe → extract on remote