# submit jobs to the batch system for parallel reconstruction of ROOT files

#!/bin/bash

set -euo pipefail

# Directory containing input ROOT files
INPUT_BASE="/group/belle/users/sanjeeva/samples2"

# Directory for reconstructed ROOT files
OUTPUT_BASE="/group/belle/users/sanjeeva/recob2dst"


# Reconstruction script
REC_SCRIPT="../stering/dstrlnu_recoPar.py"

# Batch queue
QUEUE="s"

# delete output directory if it already exists
rm -rf "$OUTPUT_BASE"

# Create output directory
mkdir -p "$OUTPUT_BASE"

# Find coupling directories
shopt -s nullglob
COUPLING_DIRS=("$INPUT_BASE"/*/)

if [ ${#COUPLING_DIRS[@]} -eq 0 ]; then
    echo "ERROR: No coupling directories found in $INPUT_BASE"
    exit 1
fi

JOB_COUNT=0
SKIP_COUNT=0

for COUPLING_DIR in "${COUPLING_DIRS[@]}"; do

    # Extract coupling combination from directory name
    COUPLING=$(basename "$COUPLING_DIR")

    echo "=========================================="
    echo "Processing coupling: $COUPLING"
    echo "=========================================="

    # Find ROOT files in the current coupling directory
    ROOT_FILES=("$COUPLING_DIR"/*.root)

    if [ ${#ROOT_FILES[@]} -eq 0 ]; then
        echo "No ROOT files found in $COUPLING_DIR"
        continue
    fi

    for INPUT_FILE in "${ROOT_FILES[@]}"; do

        # Extract input filename
        FILENAME=$(basename "$INPUT_FILE")

        # Construct output filename
        OUTPUT_FILE="${OUTPUT_BASE}/recob2dst_${FILENAME#mdst_}"

        # Construct log filename
        LOG_FILE="${OUTPUT_BASE}/log_${FILENAME%.root#mdst_}.log"

        # Skip if output already exists
        if [ -f "$OUTPUT_FILE" ]; then
            echo "Skipping existing output: $OUTPUT_FILE"
            SKIP_COUNT=$((SKIP_COUNT + 1))
            continue
        fi

        echo "Submitting reconstruction job $((JOB_COUNT + 1))"
        echo "Input : $INPUT_FILE"
        echo "Output: $OUTPUT_FILE"

        # Submit reconstruction to the batch system
        bsub -q "$QUEUE" \
            "basf2 ${REC_SCRIPT} ${INPUT_FILE} ${OUTPUT_FILE} > ${LOG_FILE} 2>&1"

        JOB_COUNT=$((JOB_COUNT + 1))

    done

done

echo "=========================================="
echo "Submission completed."
echo "Jobs submitted: $JOB_COUNT"
echo "Jobs skipped  : $SKIP_COUNT"
echo "Output directory: $OUTPUT_BASE"