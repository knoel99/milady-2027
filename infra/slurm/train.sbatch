#!/bin/bash
# MilaDy multi-GPU training on Slurm: torchrun (DDP) on one or several nodes.
#
# One torchrun launcher per node (srun --ntasks-per-node=1), which starts GPUS_PER_NODE processes;
# rendezvous on the first node of the allocation (MASTER_ADDR, MASTER_PORT).
#
# Examples (from the repository root):
#   sbatch infra/slurm/train.sbatch infra/configs/train_fm3d.yaml                 # 1 node, 4 GPUs
#   sbatch --nodes=2 infra/slurm/train.sbatch infra/configs/train_fm3d.yaml       # 2 nodes
#   Jean Zay H100 (4 GPUs and 96 cores per node):
#   sbatch --account=abc@h100 -C h100 --nodes=2 --gres=gpu:4 --cpus-per-task=96 \
#          infra/slurm/train.sbatch infra/configs/train_fm3d.yaml
#   Jean Zay A100 (8 GPUs and 64 cores per node): -C a100 --gres=gpu:8 --cpus-per-task=64
#
# Arguments: training YAML file, then additional options of milady.train.fm3d.
#
#SBATCH --job-name=milady-train
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=32
#SBATCH --hint=nomultithread
#SBATCH --time=20:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.out
# --- To adapt to the compute centre ---------------------------------------------------------------
##SBATCH --account=PROJECT@h100
##SBATCH --constraint=h100
##SBATCH --qos=qos_gpu_h100-t3
##SBATCH --partition=gpu
set -euo pipefail

CONFIG="${1:?usage: sbatch infra/slurm/train.sbatch config.yaml [milady.train.fm3d options]}"
shift
EXTRA_ARGS=("$@")

# shellcheck source=infra/slurm/env.sh
source "${MILADY_ROOT:-${SLURM_SUBMIT_DIR:-.}}/infra/slurm/env.sh"
milady_banner

# --- torchrun rendezvous -------------------------------------------------------------------------
NNODES="${SLURM_NNODES:-1}"
GPUS_PER_NODE="${GPUS_PER_NODE:-${SLURM_GPUS_ON_NODE:-$(nvidia-smi -L 2>/dev/null | wc -l)}}"
[[ "${GPUS_PER_NODE}" -ge 1 ]] || GPUS_PER_NODE=1   # node without GPU: 1 CPU process
MASTER_ADDR="$(scontrol show hostnames "${SLURM_JOB_NODELIST}" | head -n 1)"
MASTER_PORT="${MASTER_PORT:-$(( 20000 + ${SLURM_JOB_ID:-0} % 20000 ))}"
export MASTER_ADDR MASTER_PORT NNODES GPUS_PER_NODE
# Minimal NCCL logging; NCCL_DEBUG=INFO to diagnose an inter-node hang.
export NCCL_DEBUG="${NCCL_DEBUG:-WARN}"
# CPU cores per process (DataLoader, CPU FFT): task cores / GPUs of the node.
export OMP_NUM_THREADS=$(( ${SLURM_CPUS_PER_TASK:-${GPUS_PER_NODE}} / GPUS_PER_NODE ))
[[ "${OMP_NUM_THREADS}" -ge 1 ]] || export OMP_NUM_THREADS=1

echo "== ${NNODES} node(s) × ${GPUS_PER_NODE} GPU; master ${MASTER_ADDR}:${MASTER_PORT}"

# Each srun task (one per node) launches torchrun with its node rank (SLURM_NODEID).
# The single-quoted block is evaluated on each node (SLURM_NODEID differs there).
# --cpus-per-task is passed to srun again: since Slurm 22.05, srun no longer necessarily inherits the value from
# sbatch, and the task (hence all torchrun processes of the node) would be confined to 1 core.
# shellcheck disable=SC2016
srun --kill-on-bad-exit=1 --ntasks-per-node=1 --cpus-per-task="${SLURM_CPUS_PER_TASK:-1}" bash -c '
    set -euo pipefail
    source "${MILADY_ROOT}/infra/slurm/env.sh"
    milady_run python -m torch.distributed.run \
        --nnodes="${NNODES}" --nproc-per-node="${GPUS_PER_NODE}" --node-rank="${SLURM_NODEID}" \
        --master-addr="${MASTER_ADDR}" --master-port="${MASTER_PORT}" \
        -m milady.train.fm3d --config "$0" "${@}"
' "${CONFIG}" "${EXTRA_ARGS[@]}"
