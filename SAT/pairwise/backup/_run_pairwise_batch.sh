#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ $# -lt 4 ]]; then
	echo "Usage: $0 <pre|no> <DSE|CARD> <exact_encoding> <distance_encoding> [datasets...]" >&2
	exit 2
fi

TO=${TO:-600}
MO=${MO:-14000}
PYTHON_BIN=${PYTHON_BIN:-python3}

mode=$1
baseline=$2
exact_encoding=$3
distance_encoding=$4
shift 4

case "$mode" in
	pre)
		script_name="pairwise.py"
		result_root="results/preprocessing"
		;;
	no)
		script_name="pairwise_no_preprocessing.py"
		result_root="results/no_preprocessing"
		;;
	*)
		echo "Unknown mode: $mode" >&2
		exit 2
		;;
esac

if [[ $# -gt 0 ]]; then
	DATASETS=("$@")
else
	mapfile -t DATASETS < <(find dataset -mindepth 1 -maxdepth 1 -type d | sort | xargs -n 1 basename)
fi

run_case() {
	local dataset=$1
	local group
	local log_file
	local -a cmd

	case "$baseline" in
		DSE)
			group="DSE_${exact_encoding}"
			cmd=("$PYTHON_BIN" -u "$script_name" "$dataset" assumptions "$exact_encoding")
			;;
		CARD)
			group="CARD_${exact_encoding}_${distance_encoding}"
			cmd=("$PYTHON_BIN" -u "$script_name" "$dataset" assumptions "$exact_encoding" card "$distance_encoding")
			;;
		*)
			echo "Unknown baseline: $baseline" >&2
			exit 2
			;;
	esac

	log_file="${result_root}/${group}/${dataset}.log"
	mkdir -p "$(dirname "$log_file")"
	./runlim -r "$TO" -s "$MO" "${cmd[@]}" 2>&1 | tee "$log_file" || true
}

for dataset in "${DATASETS[@]}"; do
	run_case "$dataset"
done
