# hermy-vm (Hermes Remote VM)

## Access
- **User**: hermes
- **IP**: 100.83.88.122 (Tailscale)
- **SSH Key**: `/workspace/.ssh/id_ed25519` (from Hermes machine)
- **Password**: hermes007 (fallback, only if PubkeyAuth disabled)

## Hardware
| Komponente | Wert |
|-----------|------|
| RAM | 3.8 GB (414 MB used, 3.4 GB free) |
| Swap | 3.8 GB |
| CPU | 2 vCPUs (AMD Ryzen AI Max Pro 395) |
| Disk | 48 GB total, 39 GB free (16% used) |
| Kernel | 6.8.0-111-generic |
| OS | Ubuntu 24.04.4 LTS |

## Current State (2026-05-14)
- SSH: ✅ Working
- Docker: ❌ Not installed (apt install attempted, blocked by timeout)
- PostgreSQL: ❌ Not installed
- Status: Awaiting full pipeline setup (Docker → DB → Backend → Onboarding → Activity flow)

## Pending Tasks
1. Docker CE + Compose Plugin installieren
2. PostgreSQL Container (Port 5433) starten
3. Kijan Backend deployen (docker-compose.dev.yml)
4. Onboarding via Web Interface
5. Aktivität starten/beenden testen
