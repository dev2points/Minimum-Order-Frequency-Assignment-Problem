#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh pre CARD 8 8 "$@"
