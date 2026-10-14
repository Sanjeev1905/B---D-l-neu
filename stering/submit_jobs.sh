#!/bin/bash

# Number of jobs
N_JOBS=10

# Number of events per job
EVENTS=50000

# Decay file
DEC_FILE="hp_dec.dec"

# Output directory
OUT_DIR="../data/sm"

# Create output directory if it does not exist
mkdir -p "$OUT_DIR"

# Submit jobs
for i in $(seq 1 "$N_JOBS"); do

    # Different random seed for each job
    SEED=$((12345 + i))

    # Output ROOT and log files
    ROOT_FILE="${OUT_DIR}/np_50k_${i}.root"
    LOG_FILE="${OUT_DIR}/out_${i}.txt"

    echo "Submitting job $i with seed $SEED"

    bsub -q h "basf2 generate_data.py -- ${EVENTS} ${DEC_FILE} ${ROOT_FILE} --seed ${SEED} > ${LOG_FILE} 2>&1"

done

echo "All $N_JOBS jobs submitted."
echo "Output directory: $OUT_DIR"