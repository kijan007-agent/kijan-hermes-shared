---
name: docker-troubleshooting
description: Common Docker debugging patterns — health check failures, container networking, volume mounts, and service dependency issues.
version: 1.0.0
metadata:
  hermes:
    tags: [docker, troubleshooting, containers, devops]
---

# Docker Troubleshooting — Patterns & Pitfalls

> Load this skill when debugging Docker compose stacks, container health checks, networking issues, or service startup failures.

## Debugging workflow

1. **Check container status**: `docker compose ps` — look for unhealthy, restarting, or errored containers.
2. **Read logs**: `docker compose logs <service> 2>&1 | tail -60`
3. **Inspect health**: `docker inspect <container> --format='{{json .State.Health}}'`
4. **Test manually**: If the service seems up but marked unhealthy, try connecting to it directly from the host.

## Common pitfall: /dev/tcp health check fails in /bin/sh

When a container is stuck "unhealthy" with no obvious errors, the health check command itself may be the problem.

### The bug

The health check runs via `/bin/sh`, which on Debian/Ubuntu is `dash`. The `/dev/tcp/host/port` construct is a **bashism** — it does NOT work in dash:

```
# THIS FAILS on dash (/bin/sh):
test: ["CMD-SHELL", "exec 3<>/dev/tcp/127.0.0.1/6333 && echo ok"]
```

Error you'll see:
```
/bin/sh: 1: cannot create /dev/tcp/127.0.0.1/6333: Directory nonexistent
```

### The fix

Explicitly use `bash`:
```yaml
test: ["CMD-SHELL", "bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333 && echo ok'"]
```

Or use a POSIX-compatible alternative:
```yaml
# Using bash built-in
test: ["CMD-SHELL", "bash -c 'echo > /dev/tcp/127.0.0.1/6333'"]

# Or install curl/wget (heavier but more portable)
test: ["CMD-SHELL", "curl -sf http://localhost:6333/ || exit 1"]
```

### When to suspect this

- Service logs show it started successfully and is listening.
- `docker compose logs <service>` shows no errors.
- But `docker ps` shows `unhealthy`.
- `docker inspect --format='{{json .State.Health}}'` shows exit code 2 with a `/dev/tcp` error.

## Reference files

- `references/docker-healthcheck-pitfalls.md` — expanded examples and edge cases.