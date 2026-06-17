#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$HOME/kijan-hermes-shared"
LOG_FILE="$HOME/kijan-hermes-shared/sync.log"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

echo "[$TIMESTAMP] === SYNC START ===" >> "$LOG_FILE"

cd "$REPO_DIR"

# Pull latest from GitHub
if git pull origin main 2>&1 | tee -a "$LOG_FILE"; then
    echo "[$TIMESTAMP] Pull successful" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] Pull failed (may be up-to-date)" >> "$LOG_FILE"
fi

# Add any new/modified local files (skills, etc.)
git add -A 2>/dev/null

# Check if there are changes
if git diff --cached --quiet; then
    echo "[$TIMESTAMP] No local changes to commit" >> "$LOG_FILE"
else
    # Commit with auto-generated message
    git commit -m "chore: auto-sync $(date '+%Y-%m-%d %H:%M:%S')" 2>&1 | tee -a "$LOG_FILE"
    # Push to GitHub
    if git push origin main 2>&1 | tee -a "$LOG_FILE"; then
        echo "[$TIMESTAMP] Push successful" >> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] Push failed" >> "$LOG_FILE"
    fi
fi

echo "[$TIMESTAMP] === SYNC END ===" >> "$LOG_FILE"
echo ""
