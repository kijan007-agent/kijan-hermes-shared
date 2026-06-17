#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="$HOME/kijan-hermes-shared"
LOG_FILE="$HOME/kijan-hermes-shared/sync.log"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
echo "[$TIMESTAMP] === SYNC START ===" >> "$LOG_FILE"
cd "$REPO_DIR"
git pull origin main 2>&1 | tee -a "$LOG_FILE"
git add -A 2>/dev/null
if ! git diff --cached --quiet; then
    git commit -m "chore: auto-sync $(date '+%Y-%m-%d %H:%M:%S')" 2>&1 | tee -a "$LOG_FILE"
    git push origin main 2>&1 | tee -a "$LOG_FILE"
else
    echo "[$TIMESTAMP] No local changes" >> "$LOG_FILE"
fi
echo "[$TIMESTAMP] === SYNC END ===" >> "$LOG_FILE"
