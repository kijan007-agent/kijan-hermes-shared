# Docker Health Check Pitfalls — Session Details

## Qdrant: /dev/tcp failing on Debian-based image

### Context
- Image: `qdrant/qdrant` (Debian Trixie base)
- Original health check: `exec 3<>/dev/tcp/127.0.0.1/6333 && echo 'qdrant tcp alive'`
- Error: `/bin/sh: 1: cannot create /dev/tcp/127.0.0.1/6333: Directory nonexistent`
- Root cause: health check runs via `/bin/sh` (dash), which is NOT bash. `/dev/tcp` is a bash built-in.
- Fix: wrap in `bash -c '...'`

### Why it's subtle
The qdrant container IS running and listening on port 6333. You can verify:
```
curl http://localhost:6333/   # works fine from host
```
But the health check (inside the container, via `/bin/sh`) always fails. This creates a chicken-and-egg problem: dependent services won't start because qdrant is unhealthy, and you might think qdrant itself is broken.

### Verification
After fixing, confirm health is passing:
```
docker inspect <container> --format='{{.State.Health.Status}}'
# should print: healthy
```

## Related: Alpine-based containers

Some containers use Alpine which has `wget` but no `curl`. Others have neither. Always check what's available:
```
docker exec <container> which curl wget nc bash 2>&1
```

The most portable health check uses `bash -c` with `/dev/tcp` or `test -e` on network ports.
