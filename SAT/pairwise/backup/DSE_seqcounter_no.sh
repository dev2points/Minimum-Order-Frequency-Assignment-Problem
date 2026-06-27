#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh no DSE 1 1 "$@"
