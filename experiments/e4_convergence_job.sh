#!/usr/bin/env bash
# Convergence check of the E4 data asked by the encadrant (2026-11-12): the three held-out η at 24³
# (every mode |m_i| ≤ 7) and with half the CFL number at 16³, one η at 32³, plus the 16³ baseline
# recomputed on the same hardware. Solver on the GPU, summaries only (no snapshot file is kept).
#   python3 tools/runpod_job.py run --hours 1 --outputs experiments/results/replications/e4_convergence \
#       -- bash experiments/e4_convergence_job.sh
set -u
cd "$(dirname "$0")"
OUT=results/replications/e4_convergence; mkdir -p "$OUT"
DEV=${1:-cuda}
python e4_data.py --index 1 5 9 --jobs 1 --device "$DEV" | tail -n 4 && cp results/e4_data.json "$OUT"/e4_data_n16_same_hardware.json
python e4_data.py --cfl 0.75 --index 1 5 9 --jobs 1 --device "$DEV" | tail -n 4 && cp results/e4_data_cfl0.75.json "$OUT"/
python e4_data.py --n 24 --index 1 5 9 --jobs 1 --device "$DEV" | tail -n 4 && cp results/e4_data_n24.json "$OUT"/
python e4_data.py --n 32 --index 5 --jobs 1 --device "$DEV" | tail -n 2 && cp results/e4_data_n32.json "$OUT"/
ls -la "$OUT"
