<<<<<<< HEAD
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
=======
# ./DSE_totalizer.sh
# ./DSE_seqcounter.sh
# ./DSE_kmtotalizer.sh
./DSE_cardnetwrk.sh
# ./POSE.sh
# ./POSEno.sh
>>>>>>> a057817 (run POSE and pairwise INC)

./POSE.sh "$@"
./POSEno.sh "$@"
./DSE.sh "$@"
./DSEno.sh "$@"
./CARD_cardnetwrk.sh "$@"
./CARD_cardnetwrk_no.sh "$@"
./CARD_seqcounter.sh "$@"
./CARD_seqcounter_no.sh "$@"
./CARD_totalizer.sh "$@"
./CARD_totalizer_no.sh "$@"
./CARD_ladder.sh "$@"
./CARD_ladder_no.sh "$@"
./CARD_kmtotalizer.sh "$@"
./CARD_kmtotalizer_no.sh "$@"
