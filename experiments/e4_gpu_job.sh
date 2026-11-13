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
# E4_SAME_DATA=1: stop before the models if the data regenerated on this pod are not the realisation that the seed offset names
# (the solver is chaotic and some CPU types give other trajectories from the same seeds; found on 2026-11-13). The committed
# reference of the realisation is read before the reference stage overwrites it.
EXPECT=""
if [ "${E4_SAME_DATA:-0}" = 1 ] && [ "$MODE" = full ]; then
  case "${E4_DATA_SEED:-0}" in 0) REFFILE=results/e4_reference.json;; 100) REFFILE=results/replications/e4_indep/e4_reference.json;; *) REFFILE="";; esac
  [ -n "$REFFILE" ] && EXPECT=$(python -c "import json; v=json.load(open('$REFFILE'))['values']; print(' '.join(f\"{e}:{v[e]['E_B']:.10g}\" for e in v))")
fi
python e4_mhd3d.py --reference $Q --threads "$(( NPROC > 16 ? 16 : NPROC ))" | tail -n 3 || exit 1
if [ -n "$EXPECT" ]; then
  python - "$EXPECT" <<'PY' || { stamp "STOP: the data of this pod are another realisation than the one named by the seed offset"; exit 3; }
import json, sys
v = json.load(open("results/e4_reference.json"))["values"]
gap = max(abs(v[e]["E_B"] / float(x) - 1) for e, x in (t.split(":") for t in sys.argv[1].split()))
print(f"same data check: largest relative gap of E_B to the committed reference {gap:.2e}")
sys.exit(0 if gap < 1e-6 else 1)
PY
fi
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
    rc=$?; echo "$rc" > "results/logs/rc_s$s"
    echo "seed $s rc=$rc"; grep "^==\|Traceback\|Error\|total duration" "results/logs/e4_gpu_s$s.log" | tail -n 24 ) &
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
# E4_SAVE_MODELS=1: the weights of the models of groups A to E, S and L (about 50 MB each) come back with the outputs; they are
# git-ignored and meant for a release (research/release/README.md)
[ "${E4_SAVE_MODELS:-0}" = 1 ] && cp results/e4_model${TAG}_*_s*.pt "$OUT"/ 2>/dev/null
stamp "done"; nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader
ls "$OUT"
# a seed that failed must fail the job (the outputs written before the failure are kept): until 2026-11-13 the job ended with
# rc 0 whatever the seeds returned
FAILED=""; for s in $SEEDS; do [ "$(cat "results/logs/rc_s$s" 2>/dev/null)" = 0 ] || FAILED="$FAILED $s"; done
if [ -n "$FAILED" ]; then stamp "FAILED seeds:$FAILED"; exit 4; fi
