#!/bin/bash
# Automated Dropbox placeholder recovery runner
# Use with launchd for scheduled recovery

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/recover_dropbox_files.py"
LOG_DIR="$HOME/.opencode/logs"
LOG_FILE="$LOG_DIR/dropbox_recovery_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$LOG_DIR"

echo "=== Dropbox Placeholder Recovery ===" | tee "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Check current status
echo "Current status:" | tee -a "$LOG_FILE"
python3 "$PYTHON_SCRIPT" 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "Proceed with automated recovery? (yes/no)" | tee -a "$LOG_FILE"

# For automation, use environment variable
if [[ "${AUTO_RECOVER:-false}" == "true" ]]; then
    echo "AUTO_RECOVER=true, proceeding..." | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
    
    # Delete placeholders and monitor
    python3 "$PYTHON_SCRIPT" --delete --monitor --report 2>&1 | tee -a "$LOG_FILE"
    
    echo "" | tee -a "$LOG_FILE"
    echo "Recovery complete. Waiting 5 seconds for iCloud sync..." | tee -a "$LOG_FILE"
    sleep 5
    
    # Final report
    python3 "$PYTHON_SCRIPT" --report 2>&1 | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "Finished: $(date)" | tee -a "$LOG_FILE"
echo "Log saved: $LOG_FILE"
