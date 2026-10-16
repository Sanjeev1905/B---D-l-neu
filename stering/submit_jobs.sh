#!/bin/bash

# Number of samples per coupling combination
N_SAMPLES=330

# Number of events per sample
EVENTS=5000

# Directory containing decay files
DEC_DIR="../evtgen_dataprod/decfiles"

# Base output directory
OUT_BASE="../data/samples2"

# Starting random seed
BASE_SEED=12345

# Create output directory
mkdir -p "$OUT_BASE"

# Find all decay files
shopt -s nullglob
DEC_FILES=("$DEC_DIR"/decay_*.dec)

if [ ${#DEC_FILES[@]} -eq 0 ]; then
    echo "ERROR: No decay_*.dec files found in $DEC_DIR"
    exit 1
fi

JOB_COUNT=0

for DEC_FILE in "${DEC_FILES[@]}"; do

    # Extract coupling values from the filename
    FILENAME=$(basename "$DEC_FILE" .dec)
    COUPLINGS=${FILENAME#decay_}

    sample_count=0

    # Create directory for this coupling combination
    OUT_DIR="${OUT_BASE}/${COUPLINGS}"
    mkdir -p "$OUT_DIR"

    echo "Processing $DEC_FILE"

    for i in $(seq 1 "$N_SAMPLES"); do

        # Unique seed for each job
        SEED=$((BASE_SEED + sample_count + 1))

        # Output filenames
        ROOT_FILE="${OUT_DIR}/mdst_${COUPLINGS}_${i}_seed${SEED}.root"
        LOG_FILE="${OUT_DIR}/mdst_${COUPLINGS}_${i}_seed${SEED}.log"

        # Skip existing ROOT files
        if [ -f "$ROOT_FILE" ]; then
            echo "Skipping existing file: $ROOT_FILE"
            continue
        fi

        echo "Submitting job $((JOB_COUNT + 1)): $ROOT_FILE (seed=$SEED)"

        bsub -q s \
            "basf2 generate_data.py -- ${EVENTS} ${DEC_FILE} ${ROOT_FILE} --seed ${SEED} > ${LOG_FILE} 2>&1"

        JOB_COUNT=$((JOB_COUNT + 1))
        sample_count=$((sample_count + 1))

    done
done

echo "Submission completed."
echo "Jobs submitted: $JOB_COUNT"
echo "Output directory: $OUT_BASE"