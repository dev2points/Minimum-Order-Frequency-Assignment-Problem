./run_pipeline.sh
./run_pipeline_no_processing.sh



# #!/usr/bin/env bash
# set -euo pipefail

# cd "$(dirname "$0")"

# TO=${TO:-600}
# MO=${MO:-14000}

# mkdir -p results/no_preprocessing

# solve_one() {
# 	local wcnf=$1
# 	local log_file="results/no_preprocessing/${wcnf%.wcnf}.log"
# 	mkdir -p "$(dirname "$log_file")"
# 	./runlim -r "$TO" -s "$MO" ./EvalMaxSAT_bin "$wcnf" 2>&1 | tee "$log_file"
# }

# shopt -s nullglob
# for group_dir in wcnf/*; do
# 	[[ -d $group_dir ]] || continue
# 	for wcnf in "$group_dir"/*.wcnf; do
# 		solve_one "$wcnf"
# 	done
# done
