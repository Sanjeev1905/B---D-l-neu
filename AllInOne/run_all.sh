#!/bin/bash

set -euo pipefail

# First script: submit individual ROOT reconstruction jobs
SCRIPT1="./parallel_reco.sh"

# Second script: merge ROOT files and submit Diamond Frame jobs
SCRIPT2="./reco_Diamond.sh"

# Time interval between checks (seconds)
CHECK_INTERVAL=60

echo "=========================================="
echo "Starting first-stage reconstruction"
echo "=========================================="

bash "$SCRIPT1"

echo "First-stage jobs submitted."
echo "Waiting until no pending or running batch jobs remain..."

while true; do

    # Check pending and running jobs belonging to the current user
    ACTIVE_JOBS=$(bjobs -noheader 2>/dev/null | wc -l)

    echo "Active batch jobs: $ACTIVE_JOBS"

    if [[ "$ACTIVE_JOBS" -eq 0 ]]; then
        echo "No pending or running batch jobs remain."
        break
    fi

    echo "Checking again in $CHECK_INTERVAL seconds..."
    sleep "$CHECK_INTERVAL"

done

echo "=========================================="
echo "Starting second-stage Diamond Frame processing"
echo "=========================================="

bash "$SCRIPT2"

echo "=========================================="
echo "Both stages submitted successfully."
echo "=========================================="
