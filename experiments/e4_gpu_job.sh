#!/usr/bin/env bash
# E4 on a GPU pod (tools/runpod_job.py): regenerate the data on the pod's CPU cores, compute the
# reference statistics, then train and evaluate the variants on the GPU, the seeds in parallel.
# The results are an independent replication (regenerated data, other hardware): they are copied to
# experiments/results/replications/e4_gpu[_quick]/ and never overwrite the CPU results.
#
#   python3 tools/runpod_job.py run --hours 2 --outputs experiments/results/replications/e4_gpu \
#       -- bash experiments/e4_gpu_job.sh full "0 1 2 3 4"
#   ... --outputs experiments/results/replications/e4_gpu_quick -- bash experiments/e4_gpu_job.sh quick "0"
# Third argument: name of the output directory under results/replications/ (default e4_gpu); fourth: groups
# of variants (default all; e.g. D,E).
set -u
MODE=${1:-quick}; SEEDS=${2:-0}
Q=""; TAG=""; if [ "$MODE" = quick ]; then Q="--quick"; TAG="_quick"; fi
cd "$(dirname "$0")"
NAME=${3:-e4_gpu}; GROUP=${4:-all}
OUT=results/replications/$NAME$TAG; mkdir -p "$OUT" results/logs
NPROC=$(nproc); NSEED=$(echo $SEEDS | wc -w); THREADS=$(( NPROC / NSEED > 8 ? 8 : (NPROC / NSEED > 0 ? NPROC / NSEED : 1) ))
T0=$(date +%s); stamp() { echo "[$(( $(date +%s) - T0 )) s] $*"; }
python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '-')"
stamp "data: $NPROC cores"
python e4_data.py $Q --jobs "$(( NPROC > 11 ? 11 : NPROC ))" | tail -n 13 || exit 1
stamp "reference"
python e4_mhd3d.py --reference $Q --threads "$(( NPROC > 16 ? 16 : NPROC ))" | tail -n 3 || exit 1
cp results/e4_data$TAG.json results/e4_reference$TAG.json "$OUT"/
if [ "${E4_REFNULLS:-0}" = 1 ] && [ "$MODE" = full ]; then      # null points of the reference on all its snapshots (jury review of 2026-11-13)
  stamp "reference null count on all the snapshots"
  python e4_refnulls.py --device cuda --threads "$(( NPROC > 16 ? 16 : NPROC ))" | tail -n 12 && cp results/e4_refnulls.json "$OUT"/
fi
if [ "$MODE" = full ]; then ( python e4_floor.py | tail -n 3; cp results/e4_floor.json "$OUT"/ ) & fi   # noise floors, in parallel
stamp "models: seeds $SEEDS, $THREADS threads each"
PIDS=""
for s in $SEEDS; do
  ( python e4_mhd3d.py $Q --seed "$s" --group "$GROUP" --device cuda --threads "$THREADS" > "results/logs/e4_gpu_s$s.log" 2>&1
    echo "seed $s rc=$?"; grep "^==\|Traceback\|Error\|total duration" "results/logs/e4_gpu_s$s.log" | tail -n 24 ) &
  PIDS="$PIDS $!"
done
# the result files are written after every variant: copy them as they come, so that a job cut by its
# time limit still brings back what was evaluated
( while true; do cp results/e4_mhd3d${TAG}_s*.json results/e4_samples${TAG}_s0_*.npz results/logs/e4_gpu_s*.log "$OUT"/ 2>/dev/null; sleep 45; done ) &
COPIER=$!
wait $PIDS
kill $COPIER 2>/dev/null
cp results/e4_mhd3d${TAG}_s*.json results/e4_samples${TAG}_s0_*.npz results/logs/e4_gpu_s*.log "$OUT"/ 2>/dev/null
wait
stamp "done"; nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader
ls "$OUT"
