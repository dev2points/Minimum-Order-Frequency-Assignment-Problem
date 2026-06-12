#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

TO=${TO:-600}
MO=${MO:-14000}
PYTHON_BIN=${PYTHON_BIN:-python3}

mapfile -t DATASETS < <(find dataset -mindepth 1 -maxdepth 1 -type d | sort | xargs -n 1 basename)
DSE_ENCODINGS=(1 5 6 8)

run_case() {
	local dataset=$1
	local encoding=$2
	local card=${3:-}
	local group
	local log_file

	if [[ $encoding == "POSE" ]]; then
		group="POSE"
		log_file="results/no_preprocessing/pipeline/$group/${dataset}.log"
		mkdir -p "$(dirname "$log_file")"
		./runlim -r "$TO" -s "$MO" "$PYTHON_BIN" -u evalmaxsat_no_processing.py "$dataset" POSE 2>&1 | tee "$log_file" || true
	else
		group="DSE_${card}"
		log_file="results/no_preprocessing/pipeline/$group/${dataset}.log"
		mkdir -p "$(dirname "$log_file")"
		./runlim -r "$TO" -s "$MO" "$PYTHON_BIN" -u evalmaxsat_no_processing.py "$dataset" DSE "$card" 2>&1 | tee "$log_file" || true
	fi
}

if [[ $# -gt 0 ]]; then
	DATASETS=("$@")
fi

for dataset in "${DATASETS[@]}"; do
	run_case "$dataset" POSE
	for card in "${DSE_ENCODINGS[@]}"; do
		run_case "$dataset" DSE "$card"
	done
done
