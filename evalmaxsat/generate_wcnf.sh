#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

TO=${TO:-600}
MO=${MO:-14000}

mapfile -t DATASETS < <(find dataset -mindepth 1 -maxdepth 1 -type d | sort | xargs -n 1 basename)

DSE_ENCODINGS=(1 5 6 8)

mkdir -p wcnf/POSE wcnf/DSE_1 wcnf/DSE_5 wcnf/DSE_6 wcnf/DSE_8

run_case() {
	local dataset=$1
	local encoding=$2
	local card=${3:-}
	local generated_file
	local target_dir

	if [[ $encoding == "POSE" ]]; then
		generated_file="${dataset}_POSE.wcnf"
		target_dir="wcnf/POSE"
		rm -f "$generated_file"
		./runlim -r "$TO" -s "$MO" python3 -u main.py "$dataset" POSE
	else
		generated_file="${dataset}_DSE_${card}.wcnf"
		target_dir="wcnf/DSE_${card}"
		rm -f "$generated_file"
		./runlim -r "$TO" -s "$MO" python3 -u main.py "$dataset" DSE "$card"
	fi

	if [[ -f $generated_file ]]; then
		mv -f "$generated_file" "$target_dir/$generated_file"
	else
		echo "[SKIP] No WCNF generated for $dataset ($encoding${card:+,$card})"
	fi
}

for dataset in "${DATASETS[@]}"; do
	run_case "$dataset" POSE
	for card in "${DSE_ENCODINGS[@]}"; do
		run_case "$dataset" DSE "$card"
	done
done