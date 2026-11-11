#!/usr/bin/env bash
# Run the internship experiments E1-E3 with several seeds, then the figures and the digest.
#
# Usage: experiments/run_stage.sh [--quick] [--seeds "0 1 2 3 4"] [--jobs N]
#   --quick   small sizes (minutes); outputs *_quick.* are git-ignored and never cited
#   --seeds   model seeds of E1 and E2 (default: 0 1 2 3 4, rule 4 of CLAUDE.md)
#   --jobs    parallel processes (default: number of cores / 2; every process uses 2 threads)
#
# Steps (each step waits for the previous one):
#   1. E3 (no seed), E2 data, E1 simulations;
#   2. one process per seed: E1 training (cache in results/cache_e1/) and E2 models;
#   3. E1 evaluation over all the seeds, from the cache;
#   4. figures.py and digest.py (full runs only: results/digest.md).
# Logs: results/logs/. A full run takes about 3 h on 16 cores (estimate, to be measured); every
# process stays under the 2 h of rule 3. Interrupted runs resume: E1 and E2 data are cached.
set -euo pipefail
cd "$(dirname "$0")"

QUICK=""; SEEDS="0 1 2 3 4"; JOBS=$(( $(nproc) / 2 > 0 ? $(nproc) / 2 : 1 ))
while [ $# -gt 0 ]; do
  case "$1" in
    --quick) QUICK="--quick" ;;
    --seeds) SEEDS="$2"; shift ;;
    --jobs) JOBS="$2"; shift ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
  shift
done
TAG=${QUICK:+_quick}
LOGS=results/logs; mkdir -p "$LOGS"
step() { echo "[$(date +%H:%M:%S)] $*"; }

step "1/4 E3, E2 data and E1 simulations (logs in $LOGS)"
python3 e3_abc.py $QUICK > "$LOGS/e3$TAG.log" 2>&1 &
python3 e2_data.py $QUICK > "$LOGS/e2_data$TAG.log" 2>&1 &
python3 e1_gissinger.py $QUICK --simulate-only > "$LOGS/e1_sim$TAG.log" 2>&1 &
wait

step "2/4 one process per seed ($SEEDS), $JOBS at a time"
{
  for s in $SEEDS; do echo "python3 e1_gissinger.py $QUICK --train-only --seeds $s > $LOGS/e1_s$s$TAG.log 2>&1"; done
  for s in $SEEDS; do echo "python3 e2_mhd2d.py $QUICK --seed $s > $LOGS/e2_s$s$TAG.log 2>&1"; done
} | xargs -P "$JOBS" -I{} bash -c "{}"

step "3/4 E1 evaluation over the seeds $SEEDS"
python3 e1_gissinger.py $QUICK --seeds $SEEDS > "$LOGS/e1_eval$TAG.log" 2>&1

step "4/4 figures and digest"
python3 figures.py e1 e2 e3 $QUICK > "$LOGS/figures$TAG.log" 2>&1
if [ -z "$QUICK" ]; then
  python3 digest.py > results/digest.md
  step "done: results/digest.md updated; check it, then commit results/ and site/experiments/figures/"
else
  python3 digest.py > /dev/null
  step "done (quick): outputs results/*_quick.*, not versioned"
fi
