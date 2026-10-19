#!/bin/bash

# Submit batch jobs for Diamond Frame reconstruction

set -euo pipefail

# Directory containing reconstructed ROOT files
INPUT_BASE="/group/belle/users/sanjeeva/recob2dst"

# Directory for merged input files
MERGED_BASE="/group/belle/users/sanjeeva/merged_recob2dst"

# Directory for Diamond Frame output files
OUTPUT_BASE="/group/belle/users/sanjeeva/recodiamondFrame"

# Reconstruction script
REC_SCRIPT="../AllInOne/recoDiamond.py"

# Batch queue
QUEUE="s"

# Delete existing output directories
rm -rf "$MERGED_BASE"
rm -rf "$OUTPUT_BASE"

# Create output directories
mkdir -p "$MERGED_BASE"
mkdir -p "$OUTPUT_BASE"

# Check input directory
if [[ ! -d "$INPUT_BASE" ]]; then
    echo "ERROR: Input directory does not exist: $INPUT_BASE"
    exit 1
fi

# Find all ROOT files
shopt -s nullglob
ROOT_FILES=("$INPUT_BASE"/*.root)

if [[ ${#ROOT_FILES[@]} -eq 0 ]]; then
    echo "ERROR: No ROOT files found in $INPUT_BASE"
    exit 1
fi

# Group files by coupling combination
declare -A COUPLING_FILES

for INPUT_FILE in "${ROOT_FILES[@]}"; do

    FILENAME=$(basename "$INPUT_FILE")

    # Expected filename:
    # recob2dst_0.001_0.251_0.212_1_seed12346.root

    if [[ "$FILENAME" =~ ^recob2dst_([-+]?[0-9]*\.?[0-9]+)_([-+]?[0-9]*\.?[0-9]+)_([-+]?[0-9]*\.?[0-9]+)_.*\.root$ ]]; then

        G_L="${BASH_REMATCH[1]}"
        G_R="${BASH_REMATCH[2]}"
        G_P="${BASH_REMATCH[3]}"

        COUPLING="${G_L}_${G_R}_${G_P}"

        COUPLING_FILES["$COUPLING"]+="$INPUT_FILE"$'\n'

    else
        echo "WARNING: Skipping unexpected filename: $FILENAME"
    fi

done

JOB_COUNT=0

# Merge files belonging to the same coupling combination
for COUPLING in "${!COUPLING_FILES[@]}"; do

    echo "=========================================="
    echo "Processing coupling: $COUPLING"
    echo "=========================================="

    MERGED_FILE="${MERGED_BASE}/${COUPLING}.root"
    LOG_FILE="${OUTPUT_BASE}/log_${COUPLING}.log"

    # Read the list of files belonging to this coupling combination
    #mapfile -t FILE_LIST <<< "${COUPLING_FILES[$COUPLING]}"
    FILE_STRING="${COUPLING_FILES[$COUPLING]%$'\n'}"
    mapfile -t FILE_LIST <<< "$FILE_STRING"

    # Merge the ROOT files
    echo "Merging ${#FILE_LIST[@]} files into $MERGED_FILE"

    hadd -f "$MERGED_FILE" "${FILE_LIST[@]}"

    # Output filename contains only coupling parameters
    OUTPUT_FILE="${OUTPUT_BASE}/${COUPLING}.root"

    echo "Submitting Diamond Frame reconstruction"
    echo "Input : $MERGED_FILE"
    echo "Output: $OUTPUT_FILE"

    bsub -q "$QUEUE" \
        "basf2 ${REC_SCRIPT} ${MERGED_FILE} ${OUTPUT_FILE} > ${LOG_FILE} 2>&1"

    JOB_COUNT=$((JOB_COUNT + 1))

done

echo "=========================================="
echo "Submission completed."
echo "Jobs submitted: $JOB_COUNT"
echo "Merged inputs : $MERGED_BASE"
echo "Output directory: $OUTPUT_BASE"