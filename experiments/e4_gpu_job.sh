#!/usr/bin/env bash
# E4 on a GPU pod (tools/runpod_job.py): regenerate the data on the pod's CPU cores, compute the
# reference statistics, then train and evaluate the variants on the GPU, the seeds in parallel.
# The results are an independent replication (regenerated data, other hardware): they are copied to
# experiments/results/replications/e4_gpu[_quick]/ and never overwrite the CPU results.
#
#   python3 tools/runpod_job.py run --hours 2 --outputs experiments/results/replications/e4_gpu \
#       -- bash experiments/e4_gpu_job.sh full "0 1 2 3 4"
#   ... --outputs experiments/results/replications/e4_gpu_quick -- bash experiments/e4_gpu_job.sh quick "0"
set -u
MODE=${1:-quick}; SEEDS=${2:-0}
Q=""; TAG=""; if [ "$MODE" = quick ]; then Q="--quick"; TAG="_quick"; fi
cd "$(dirname "$0")"
OUT=results/replications/e4_gpu$TAG; mkdir -p "$OUT" results/logs
NPROC=$(nproc); NSEED=$(echo $SEEDS | wc -w); THREADS=$(( NPROC / NSEED > 8 ? 8 : (NPROC / NSEED > 0 ? NPROC / NSEED : 1) ))
T0=$(date +%s); stamp() { echo "[$(( $(date +%s) - T0 )) s] $*"; }
python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '-')"
stamp "data: $NPROC cores"
python e4_data.py $Q --jobs "$(( NPROC > 11 ? 11 : NPROC ))" | tail -n 13 || exit 1
stamp "reference"
python e4_mhd3d.py --reference $Q --threads "$(( NPROC > 16 ? 16 : NPROC ))" | tail -n 3 || exit 1
cp results/e4_data$TAG.json results/e4_reference$TAG.json "$OUT"/
stamp "models: seeds $SEEDS, $THREADS threads each"
for s in $SEEDS; do
  ( python e4_mhd3d.py $Q --seed "$s" --group all --device cuda --threads "$THREADS" > "results/logs/e4_gpu_s$s.log" 2>&1
    echo "seed $s rc=$?"; grep "^==\|Traceback\|Error\|total duration" "results/logs/e4_gpu_s$s.log" | tail -n 16
    cp results/e4_mhd3d${TAG}_s${s}.json "$OUT"/ 2>/dev/null; cp "results/logs/e4_gpu_s$s.log" "$OUT"/ ) &
done
wait
stamp "done"; nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader
ls "$OUT"
