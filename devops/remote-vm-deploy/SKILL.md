---
name: remote-vm-deploy
description: Deploy Docker, PostgreSQL, and Kijan stack on remote VMs (SSH + Tailscale). Covers VM provisioning, Docker install, service setup, and full pipeline verification.
version: 1.0
---

# Remote VM Deploy Skill

## Triggers
- User mentions deploying Docker, VMs, or remote infrastructure
- Remote VM setup with SSH key authentication
- Tailscale-based machine access
- "VM aufsetzen", "Docker remote", "Server einrichten"

## Prerequisites

### SSH Key Location
SSH keys are stored at `/workspace/.ssh/` (NOT `/data/hermes-workspace/.ssh/` — that path is on the host machine only).

### Connection Pattern
```bash
ssh -i /workspace/.ssh/id_ed25519 hermes@<IP> "command"
```

## Remote VM Setup Procedure

### 1. Test SSH Connectivity
```bash
ssh -i /workspace/.ssh/id_ed25519 <user>@<host> "whoami && hostname && uname -r && df -h / | tail -1"
```

### 2. Install Docker on Remote VM
**Never use `curl | sh`** — it times out. Use apt directly:

```bash
ssh -i /workspace/.ssh/id_ed25519 <user>@<host> \
  "sudo apt update -qq && sudo apt install -y ca-certificates curl gnupg lsb-release && \
   sudo install -m 0755 -d /etc/apt/keyrings && \
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.gpg > /dev/null && \
   chmod a+r /etc/apt/keyrings/docker.gpg && \
   echo \"deb [arch=\$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
   sudo apt update -qq && \
   sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
```

⚠️ **sudo ohne Password**: Falls der User sudo ohne PW braucht, nutze `echo "password" | sudo -S` statt interaktivem Prompt.
⚠️ **lsb_release missing**: Falls `lsb_release` nicht installiert, nutze `cat /etc/os-release | grep VERSION_CODENAME | cut -d= -f2`.

### 3. PostgreSQL on Non-Default Port (No Conflict with localhost:5432)
```bash
ssh -i /workspace/.ssh/id_ed25519 <user>@<host> \
  "docker run -d --name postgres-dev --restart unless-stopped \
   -p 5433:5432 \
   -e POSTGRES_USER=kijan_user \
   -e POSTGRES_PASSWORD=kijan_password \
   -e POSTGRES_DB=kijan_tracker \
   -v postgres-dev-data:/var/lib/postgresql/data \
   postgres:15-alpine"
```

Port-Mapping: Externer Port **5433** → Interner Port **5432**.
DB-URL für Backend: `postgresql+asyncpg://kijan_user:kijan_password@<vm-ip>:5433/kijan_tracker`

### 4. Adminer (Optional Web-UI)
```bash
ssh -i /workspace/.ssh/id_ed25519 <user>@<host> \
  "docker run -d --name adminer --restart unless-stopped -p 8080:8080 adminer:latest"
```

## Pitfalls

### SSH Key Path
- **Local machine** (Hermes): `/workspace/.ssh/id_ed25519`
- **Host machine** (jan@aimax): `/data/hermes-workspace/.ssh/id_ed25519`
- These are DIFFERENT machines. Use the correct path for where you execute.

### sudo Requires Password on Remote
SSH commands execute as the remote user. `sudo` in SSH commands fails silently if password prompt can't be displayed. Fix:
- Add user to sudoers NOPASSWD, OR
- Use `echo "password" | sudo -S bash -c "commands"`

### Docker Install Timeout
`curl https://get.docker.com | sh` WILL timeout on slow connections. Always use direct apt packages.

### Port Conflicts
Check `ss -tlnp` or `netstat -tlnp` before binding ports. Host localhost:5432 may conflict with Docker container port 5432.

### write_file Does NOT Work on Remote Paths
`write_file` writes to the local file system (agent's machine), NOT to the remote VM. On a remote VM, always use `ssh -i ... user@host 'command'` or `ssh ... user@host "cat > file << 'EOF'\n...\nEOF"` to write remote files. There is NO tool to write arbitrary remote files — only SSH.

### Docker-in-LXC: `host.docker.internal` Does NOT Exist
In a Proxmox LXC container, Docker has no `host.docker.internal` (that's Docker Desktop only). Use `172.17.0.1` (Docker bridge gateway) to reach the host.

### SSH Multiline Strings Block the Channel
SSH commands with multiline Python strings or heredocs (`<< "EOF"`) can block the SSH channel indefinitely. Keep SSH commands to single-line Python `-c` calls or use `bash -c "single-line"`. If it hangs, the channel is dead — retry.

### Docker Compose Reads docker-compose.yml by Default
`docker compose up` reads `docker-compose.yml`, not `docker-compose.dev.yml`. Always specify `-f docker-compose.dev.yml` when you want the dev config.

### pip PEP 668 on Ubuntu 24.04
`pip install` fails with `externally-managed-environment`. Must use `pip3 install --break-system-packages`.

### Python Heredocs via SSH Break
`python3 << 'EOF'` multiline strings hang or get mangled through SSH. Use `-c` for short scripts only. For complex remote Python, write a script file locally → scp → execute.

### CR/LF Mangles sed Variables
On files with CRLF line endings (Connect IQ source files), `sed` through SSH strips `$1`, quotes, and special chars. Use raw byte operations (`python3` with `'rb'`/``'wb'`) for safe manipulation.

### Submodule Divergence
`git submodule update` resets submodules to the commit recorded in the parent repo HEAD. To use a different branch (e.g., latest `dev`), manually `cd kpt-backend && git checkout dev && git pull` AFTER `git submodule update`.

## VM Specs Reference
| VM | RAM | CPU | Disk | OS | Docker |
|----|-----|-----|------|----|--------|
| hermy-vm (hermes@100.83.88.122) | 3.8 GB | 2 vCPU | 48 GB | Ubuntu 24.04 | Not installed |

## Backend on Remote VM (Without Docker Compose)
When docker-compose fails (missing sudo, no pip, etc.), run the backend directly:

```bash
ssh -i /workspace/.ssh/id_ed25519 hermes@100.83.88.122 \
  "sudo apt-get install -y python3-pip && cd /home/hermes/Github/KijanPersonalTracker/kpt-backend && \
   pip3 install -r requirements.txt"
```

Then start with env-vars pointing to the external DB:
```bash
export DATABASE_URL_ADMIN=postgresql+asyncpg://kijan_user:kijan_password@172.17.0.1:5433/kijan_tracker
export DATABASE_URL_ACTIVITY=postgresql+asyncpg://kijan_user:kijan_password@172.17.0.1:5433/kijan_tracker
export DATABASE_URL_PROJECTS=postgresql+asyncpg://kijan_user:kijan_password@172.17.0.1:5433/kijan_tracker
export DATABASE_URL_HEALTH=postgresql+asyncpg://kijan_user:kijan_password@172.17.0.1:5433/kijan_tracker
export SECRET_KEY=local-dev-secret-key
export REGISTRATION_KEY=8yLDQH0ZW4gjdISkzNvX
cd /home/hermes/Github/KijanPersonalTracker/kpt-backend
python3 migrate.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

All 4 DB URLs point to the **same** DB (we have only one PostgreSQL instance).

## Verification Steps
1. `docker ps` — container running
2. `docker exec <container> psql -U <user> -c '\l'` — DB accessible
3. Backend `.env` points to correct port
4. `docker compose -f docker-compose.dev.yml up -d` — backend starts
5. Onboarding via web interface
6. Activity start/stop flow

## Related Skills
- `kijan-personal-tracker` — Backend config, DB schema, docker-compose.dev.yml
- `server-first-git-sync` — Git sync before tasks
- `docker-troubleshooting` — Common Docker debugging patterns