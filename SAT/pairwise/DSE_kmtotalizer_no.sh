#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh no DSE 8 8 "$@"
*** Add File: SourceCode/SAT/pairwise/CARD_seqcounter_pre.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh pre CARD 1 1 "$@"
*** Add File: SourceCode/SAT/pairwise/CARD_seqcounter_no.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh no CARD 1 1 "$@"
*** Add File: SourceCode/SAT/pairwise/CARD_totalizer_pre.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh pre CARD 5 5 "$@"
*** Add File: SourceCode/SAT/pairwise/CARD_totalizer_no.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh no CARD 5 5 "$@"
*** Add File: SourceCode/SAT/pairwise/CARD_ladder_pre.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh pre CARD 6 6 "$@"
*** Add File: SourceCode/SAT/pairwise/CARD_ladder_no.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh no CARD 6 6 "$@"
*** Add File: SourceCode/SAT/pairwise/CARD_kmtotalizer_pre.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh pre CARD 8 8 "$@"
*** Add File: SourceCode/SAT/pairwise/CARD_kmtotalizer_no.sh
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./_run_pairwise_batch.sh no CARD 8 8 "$@"
