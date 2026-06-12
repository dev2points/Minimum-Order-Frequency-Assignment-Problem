#!/usr/bin/env bash

TO=${TO:-600}
MO=${MO:-14000}
MODE=${MODE:-preprocessing}
DATASET=${1:-graph04}

if [ "$MODE" = "no_preprocessing" ] || [ "$MODE" = "no-preprocessing" ] || [ "$MODE" = "no" ]; then
    SCRIPT=main_no.py
    RESULTS_DIR=results/no_preprocessing
else
    SCRIPT=main.py
    RESULTS_DIR=results/preprocessing
fi

mkdir -p "$RESULTS_DIR"

./runlim -r "$TO" -s "$MO" python3 -u "$SCRIPT" "$DATASET" "$TO" 2>&1 | tee "$RESULTS_DIR/$DATASET.log"
