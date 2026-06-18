#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./INC.sh "$@"
./INCSC_NSC.sh "$@"
./INCSC_NSC_no.sh "$@"
./INCSC_TOT.sh "$@"
./INCSC_TOT_no.sh "$@"
