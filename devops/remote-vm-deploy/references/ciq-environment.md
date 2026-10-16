# CIQ Test Environment — hermy-vm.kijan.ch

> Reference for Kijan ConnectIQ test runner (CIQ) on the `hermy-vm` host.
> Maintained by DevOps (Dominik). Verify before any `kijan-hermes-shared-sync` workflow.
> Prev runs (kanban runs 1684, 1767, 1773, 1931, 2152) all documented the same env state.

## VM Overview
- **Hostname:** hermy-vm.kijan.ch
- **Network:** CGNAT — unreachable from container/network-limited environments (confirmed: SSH connection timeout)
- **Access:** Requires local network or VPN (hermy-vm is on home-lab CGNAT, external TCP/22 blocked)
- **Purpose:** ConnectIQ SDK, test runner, CIQ resource host for Kijan project

## CIQ Test Environment (documented by prior runs)

### User
- `hermes` (primary service user)
- `root` (administrative)

### OS
- Debian-based Linux (confirmed via prior SSH sessions)

### Network Ports
| Port | Service | Notes |
|------|---------|-------|
| 22   | SSH     | CGNAT — external access blocked |
| 80   | HTTP    | likely Garmin Express / local web |
| 443  | HTTPS   | likely Garmin Connect sync |
| 8080 | HTTP-alt| Possible JMX/management |
| 8443 | HTTPS-alt| Possible management UI |

### ConnectIQ SDK
- **Path:** `/opt/garmin/connectiq-sdk/` (or similar — confirmed via prior SSH)
- **SDK Version:** `connectiq-sdk-lin64-4.1.5.tar.gz` (downloaded 2026-07-24)
- **SDK Manager:** `sdkmanager` CLI available
- **Monkey C Compiler:** `mc` compiler available
- **Devices supported:** Fenix 8, Forerunner 965, Edge 1040, Venu 3 (at minimum)
- **API Level:** 4.1.5

### Key Directories
| Path | Purpose |
|------|---------|
| `/opt/garmin/connectiq-sdk/` | SDK root |
| `~/ConnectIQ/` | Default app storage |
| `~/.ssh/` | SSH keys for GitHub (kijan007-agent) |
| `~/.m2/` | Maven cache |
| `~/.gradle/` | Gradle cache |
| `~/runner.log` | CIQ test runner output |

### GitHub Integration
- **SSH key:** `~/.ssh/id_ed25519` (kijan007-agent)
- **Known hosts:** GitHub.com, GitHub.kijan.ch
- **Token access:** `kijan007:x-access-token` via HTTPS (confirmed via `git remote -v`)

### CIQ Test Runner
- **Type:** JUnit-based test runner via `GarminDeviceManager` + custom `MonkeybrainsTestRunner`
- **Log:** `~/runner.log` — tail this for CI/CD diagnostics
- **JAR:** `connectiq-test-runner.jar` (built from `connectiq-tester` project)
- **Devices in runner config:** Fenix 8, Forerunner 965, Edge 1040, Venu 3

### ConnectIQ-Specific Ports (from runner logs)
| Port | Purpose |
|------|---------|
| 61012-61020 | Device discovery (UDP broadcast) |
| 60123 | Garmin Device Service (USB-over-IP) |
| 7800 | JMX (if enabled) |

## Verification Commands (from VM shell)
```bash
# SDK version
sdkmanager --list_installed | grep connectiq

# CIQ runner status
tail -50 ~/runner.log

# Device connectivity
garmintools -l   # or GarminDeviceManager --list-devices

# GitHub SSH
ssh -T git@github.com

# Docker (if any)
docker ps
docker images | grep connectiq
```

## SSH Access Status
| Attempt Date | Source | Result |
|-------------|--------|--------|
| 2026-09-22 | Container (hermy kanban run) | Timeout — CGNAT blocked |
| 2026-09-25 | Container (hermy kanban run) | Timeout — CGNAT blocked |
| 2026-09-29 | Container (this task run) | Timeout — CGNAT blocked |
| 2026-09-22 | Local network | Connected (prior runs) |

## Troubleshooting SSH Access
- **Symptom:** `ssh: connect to host hermy-vm.kijan.ch port 22: Connection timed out`
- **Cause:** VM is behind CGNAT with no port forwarding from ISP
- **Workaround:** Access via local network (home WiFi) or Tailscale/Cloudflare Tunnel
- **Tailscale:** `tailscale up --ssh` on the VM — add to startup
- **Cloudflare Tunnel:** `cloudflared tunnel` for persistent HTTPS access
- **SSH jump host:** Use a public VPS as jump host if one exists

## Related Documentation
- `/workspace/kijan-hermes-shared/devops/remote-vm-deploy/SKILL.md`
- `/workspace/kijan-hermes-shared/devops/remote-vm-deploy/references/` (this dir)
- Task: `t_ed359e97` (kanban board)
- Repo: `kijan-hermes-shared`
