#!/bin/bash
# MilaDy data generation on Slurm: job array, ONE simulation (1 GPU) per element.
#
# Normal submission (from the repository root) — the array is sized by milady.sweep:
#   python -m milady.sweep infra/configs/palier2_abc3d.yaml --scheduler slurm
# Manual submission (N simulations, at most 16 in parallel):
#   sbatch --array=0-$((N-1))%16 infra/slurm/gen_data.sbatch infra/configs/palier2_abc3d.yaml
# Jean Zay (H100 example; see infra/slurm/README-slurm.md):
#   sbatch --account=abc@h100 -C h100 --cpus-per-task=24 --array=0-36%16 \
#          infra/slurm/gen_data.sbatch infra/configs/palier2_abc3d.yaml
#
# Argument: campaign YAML file. The array element SLURM_ARRAY_TASK_ID selects the parameter point
# (order of the campaign expansion by milady.sweep).
# Environment: see infra/slurm/env.sh (Apptainer image, $WORK/$SCRATCH, SQLite catalogue).
#
#SBATCH --job-name=milady-sim
#SBATCH --array=0-0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --hint=nomultithread
#SBATCH --time=04:00:00
#SBATCH --output=%x-%A_%a.out
#SBATCH --error=%x-%A_%a.out
# SIGTERM 120 s before the time limit, sent to the srun step (the simulation): it writes its checkpoint
# and stops cleanly (without this margin, Slurm only grants KillWait, often 30 s).
#SBATCH --signal=TERM@120
# --- To adapt to the compute centre (uncomment: "##SBATCH" is ignored by Slurm) ---------
##SBATCH --account=PROJECT@h100         # Jean Zay: project@cpu|v100|a100|h100 (echo $IDRPROJ)
##SBATCH --constraint=h100              # Jean Zay: h100 (gpu_p6), a100 (gpu_p5), v100-32g...
##SBATCH --qos=qos_gpu_h100-t3          # Jean Zay: -t3 <= 20 h (default), -t4 <= 100 h, -dev <= 2 h
##SBATCH --partition=gpu                # regional centre / cloud Slurm: name of the GPU partition
set -euo pipefail

CONFIG="${1:?usage: sbatch [--array=...] infra/slurm/gen_data.sbatch campaign.yaml [milady.sim.run options]}"
shift
EXTRA_ARGS=("$@")

# Slurm runs a copy of this script: the repository is found through MILADY_ROOT or the submission directory.
# shellcheck source=infra/slurm/env.sh
source "${MILADY_ROOT:-${SLURM_SUBMIT_DIR:-.}}/infra/slurm/env.sh"
milady_banner

TASK="${SLURM_ARRAY_TASK_ID:-0}"
echo "== simulation ${TASK} of ${CONFIG} ($(date -u +%FT%TZ))"
start=$(date +%s)

# The simulation writes the MFF file to MILADY_STORAGE_URI and registers itself in the catalogue
# (MILADY_DB_URL) with the Slurm job id (SLURM_ARRAY_JOB_ID_SLURM_ARRAY_TASK_ID).
# It runs in an srun step to receive the --signal signal (the shell of the batch script, for its part,
# is not signalled). --cpus-per-task is passed explicitly again: since Slurm 22.05, srun no longer
# necessarily inherits the value from sbatch. After an interruption (status "failed", note
# "interrupted" in the catalogue), resubmitting the same index resumes from the last checkpoint:
#   sbatch --array=<indices> infra/slurm/gen_data.sbatch <campaign.yaml>
# Outside Slurm (template trial: SLURM_ARRAY_TASK_ID=0 bash infra/slurm/gen_data.sbatch ...), no srun.
launch=()
if [[ -n "${SLURM_JOB_ID:-}" ]] && command -v srun >/dev/null 2>&1; then
    launch=(srun --ntasks=1 --cpus-per-task="${SLURM_CPUS_PER_TASK:-1}")
fi
# shellcheck disable=SC2016  # block evaluated in the srun step
"${launch[@]}" bash -c '
    set -euo pipefail
    source "${MILADY_ROOT}/infra/slurm/env.sh"
    milady_run python -m milady.sim.run "$0" --index "$1" "${@:2}"
' "${CONFIG}" "${TASK}" "${EXTRA_ARGS[@]}"

echo "== finished in $(( $(date +%s) - start )) s"
