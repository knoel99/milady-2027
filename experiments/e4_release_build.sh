#!/usr/bin/env bash
# E4 release build, on CPU: one of the three stages of .github/workflows/e4-release.yml, or all of them in a row.
#
#   bash experiments/e4_release_build.sh data                 # data, MFF files, reference statistics
#   bash experiments/e4_release_build.sh mff                  # the MFF files again from the snapshots (new provenance note)
#   bash experiments/e4_release_build.sh model <seed>         # W9 (and G0, G1) trained and evaluated, map of W16
#   bash experiments/e4_release_build.sh assemble <out> <url> # the folder of the release
#   bash experiments/e4_release_build.sh all <out> <url>      # the three stages, seeds 0 to 4 one after the other
#
# The stages overwrite experiments/results/e4_data.json, e4_reference.json and e4_mhd3d_s<seed>*.json of the checkout: run
# them in a throw-away checkout (the CI runner, or a git worktree), never in a working copy whose results are to be kept.
# E4_RELEASE_BUILD=1 must be set, as a guard. E4_N_RECOLOUR: samples of W9 per η for the map of W16 (default 32768, lowered if the machine is too slow).
set -euo pipefail
[ "${E4_RELEASE_BUILD:-0}" = 1 ] || { echo "set E4_RELEASE_BUILD=1 (this overwrites result files of the checkout)"; exit 2; }
cd "$(dirname "$0")"
export PYTHONPATH="$PWD/../src${PYTHONPATH:+:$PYTHONPATH}" E4_SAVE_MODELS=1
STAGE=${1:-all}; NPROC=$(nproc); N_REC=${E4_N_RECOLOUR:-32768}
T0=$(date +%s); stamp() { echo "[$(( $(date +%s) - T0 )) s] $*"; }

mff() {   # the MFF files, with a provenance note that says whether the data are the realisation of the main run of the report
  local note; note=$(python3 e4_release.py --print-note --npz data_e4)
  stamp "MFF: $note"; python3 -m milady.data.convert e4 data_e4 data_e4_mff --overwrite --note "$note" > /dev/null
  python3 -m milady.data.convert validate --full data_e4_mff/e4_eta*.h5
}

data() {
  if [ "$(ls data_e4/eta_*.npz 2>/dev/null | wc -l)" != 11 ]; then stamp "data on $NPROC cores"; python3 e4_data.py --jobs "$NPROC" | tail -n 13; fi
  mff
  stamp "reference statistics"; python3 e4_mhd3d.py --reference --threads "$NPROC" | tail -n 3
}

model() {
  local s=$1; mkdir -p results/logs release_models
  rm -f results/e4_mhd3d_s"$s".json results/e4_mhd3d_s"$s"_*.json      # the committed files of the GPU runs: not part of this build
  stamp "seed $s: groups D and G"
  python3 e4_mhd3d.py --seed "$s" --group D,G --device cpu --threads "$NPROC" > "results/logs/release_s$s.log" 2>&1 \
    || { tail -n 30 "results/logs/release_s$s.log"; exit 1; }
  grep "^==\|total duration" "results/logs/release_s$s.log" | tail -n 8
  stamp "seed $s: parameter files and map of W16 on $N_REC samples"
  local laws="--no-laws"; [ "$s" = 0 ] && laws=""
  python3 e4_release_models.py --weights results --out release_models --seeds "$s" --n-recolour "$N_REC" --threads "$NPROC" $laws
}

assemble() {
  local out=$1 url=$2
  stamp "release folder"
  python3 e4_release.py --mff data_e4_mff --npz data_e4 --run results --models release_models --out "$out" --url "$url" \
    --host "${E4_BUILD_HOST:-the CPU of a GitHub Actions runner}" ${E4_REPO_DIR:+--repo-dir "$E4_REPO_DIR"}
}

case "$STAGE" in
  data) data ;;
  mff) mff ;;
  model) model "${2:?seed}" ;;
  assemble) assemble "${2:?output folder}" "${3:?url}" ;;
  all) data; for s in ${E4_SEEDS:-0 1 2 3 4}; do model "$s"; done; assemble "${2:?output folder}" "${3:?url}" ;;
  *) echo "unknown stage $STAGE"; exit 2 ;;
esac
stamp "done: $STAGE"
