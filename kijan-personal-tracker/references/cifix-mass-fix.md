# Mass CRLF Fix for Connect IQ Files

## Problem

Connect IQ `.mc` files have Windows CRLF line endings (`\r\n`). This breaks Connect IQ compilation on Linux/macOS.

## Why Python binary-mode instead of sed?

`sed -i 's/\r$//'` fails silently on binary content and may corrupt non-text files. Python binary-mode replacement is reliable:

```python
import os

def fix_crlf(directory):
    fixed = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(('.mc', '.py')):
                full = os.path.join(root, f)
                with open(full, 'rb') as fh:
                    content = fh.read()
                if b'\r\n' in content:
                    content = content.replace(b'\r\n', b'\n')
                    with open(full, 'wb') as fh:
                        fh.write(content)
                    fixed += 1
    return fixed
```

## Prevention

After fixing, prevent future CRLF issues:

```bash
# In the Connect IQ submodule
cd kpt-app-ciq
git config core.autocrlf input
git config core.eol lf
git config core.safecrlf false
git reset --hard <commit-hash>
```

## Scale

In KijanPersonalTracker-hermes (2026-05-12): **140 files, 23,289 CRLF lines** affected. All `.mc` and `.py` files in `kpt-app-ciq/source/`.

## Note

The fix is idempotent — safe to run multiple times. No data loss risk since `\r\n` → `\n` only removes the carriage return byte.
