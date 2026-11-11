#!/bin/bash
# MilaDy evaluation on Slurm (1 GPU): model sampling, physical metrics and
# distances between distributions, results recorded in the catalogue (evaluation table).
#
# Examples (from the repository root):
#   sbatch infra/slurm/eval.sbatch infra/configs/train_fm3d.yaml
#   sbatch infra/slurm/eval.sbatch infra/configs/train_fm3d.yaml --model 3f2c…   # catalogue identifier
#   Jean Zay: sbatch --account=abc@h100 -C h100 --cpus-per-task=24 infra/slurm/eval.sbatch …
#
# Arguments: YAML file (the training one), then milady.eval options.
#
#SBATCH --job-name=milady-eval
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --hint=nomultithread
#SBATCH --time=02:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.out
# --- To adapt to the compute centre ---------------------------------------------------------------
##SBATCH --account=PROJECT@h100
##SBATCH --constraint=h100
##SBATCH --qos=qos_gpu_h100-dev          # Jean Zay: "dev" queue (<= 2 h) for short evaluations
##SBATCH --partition=gpu
set -euo pipefail

CONFIG="${1:?usage: sbatch infra/slurm/eval.sbatch config.yaml [milady.eval options]}"
shift
EXTRA_ARGS=("$@")

# shellcheck source=infra/slurm/env.sh
source "${MILADY_ROOT:-${SLURM_SUBMIT_DIR:-.}}/infra/slurm/env.sh"
milady_banner

milady_run python -m milady.eval --config "${CONFIG}" "${EXTRA_ARGS[@]}"
