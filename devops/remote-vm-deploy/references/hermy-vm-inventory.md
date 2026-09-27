# hermy-vm Inventory

> **TL;DR** — SSH pubkey registration for hermes user: DONE (verified 2026-09-27).
> Current ED25519 key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKXNC1/s26IP70GQNc08NOWanu6fGqpQYiji2RREpsN6 hermes-access`
> Fingerprint: `SHA256:HtzeNtIIVcA6zxbwkz05uZDCkL8RUvFewSIdlnABids`
> Registered in: `~hermes/.ssh/authorized_keys` on hermy-vm (run 841, session 20260828_060841_6ba0ab)

---

## VM Overview

| Property | Value |
|---|---|
| **Hostname** | hermy-vm |
| **Tailscale hostname** | hermy-vm.kijan.ch |
| **Tailscale IP** | 100.66.141.92 (DNS A record) |
| **Alternative IP** | 100.83.88.122 (shared skill doc — verify if VM re-provisioned) |
| **OS** | Ubuntu 24.04 LTS |
| **RAM** | 3.8 GB |
| **vCPU** | 2 |
| **Disk** | 48 GB |
| **Owner** | hermes (UID 1000) |
| **Status** | Active |
| **Docker** | Not installed (see deployment notes) |

---

## SSH Access

**Current key (verified 2026-09-27, run 22362 + run 841):**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKXNC1/s26IP70GQNc08NOWanu6fGqpQYiji2RREpsN6 hermes-access
```
**Fingerprint:** SHA256:HtzeNtIIVcA6zxbwkz05uZDCkL8RUvFewSIdlnABids
**Algorithm:** ED25519 (rotated from prior RSA key, registered in run 841)
**Verified:** `~hermes/.ssh/authorized_keys` on hermy-vm — SSH pubkey auth confirmed working. Commands `whoami`, `hostname`, `df`, `free` executed successfully via pubkey auth (run 841).

**Local key location:** `/workspace/.ssh/id_ed25519` (Hermes devops profile)
**Connection:** `ssh -i /workspace/.ssh/id_ed25519 hermes@hermy-vm.kijan.ch`

> **Note:** hermy-vm is Tailscale-only. It is NOT reachable from the public internet.
> Ensure your environment has Tailscale connectivity before connecting.

---

## Deployment Notes

- Docker is NOT installed on hermy-vm (confirmed 2026-07-13)
- To deploy Docker: see `../remote-vm-deploy/SKILL.md`
- Backend source: `/home/hermes/Github/KijanPersonalTracker/` (if cloned)

---

## Last Updated

- 2026-09-27 — Updated SSH key to current ED25519 key (run 22362). Verified key intact at `/workspace/.ssh/id_ed25519`. RSA key retired.
- 2026-07-13 — Initial inventory created. Docker not installed.
