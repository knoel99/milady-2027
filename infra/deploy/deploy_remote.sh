#!/usr/bin/env bash
# Deploy MilaDy to a remote VM from the laptop: copy the repository (rsync) or git clone on the
# VM, then run bootstrap_vm.sh over SSH.
#
# Usage :
#   infra/deploy/deploy_remote.sh user@host [options] [-- bootstrap_vm.sh options]
#
# Options :
#   -i KEY          private SSH key (otherwise agent / ~/.ssh/config)
#   -p PORT         SSH port (default 22)
#   --dir DIR       remote directory (default: ~/milady-2027)
#   --git URL       clone/update from this URL on the VM instead of copying the local tree
#   --branch B      branch for --git (default: main)
#   --sync-only     copy only, without running bootstrap_vm.sh
#   -h, --help      this help
#
# Examples:
#   infra/deploy/deploy_remote.sh ubuntu@51.15.0.10
#   infra/deploy/deploy_remote.sh ubuntu@51.15.0.10 -i ~/.ssh/id_ed25519 -- --no-smoke
#   infra/deploy/deploy_remote.sh ubuntu@gpu-vm --git https://github.com/knoel99/milady-2027.git
#
# The copy excludes secrets (any .env file, including infra/docker/.env: the VM generates its own),
# data (data/), virtual environments and Apptainer images. Re-running the script updates the
# VM (idempotent).
set -euo pipefail

usage() { sed -n '2,24p' "$0"; }

[[ $# -ge 1 ]] || { usage; exit 2; }
case "$1" in -h|--help) usage; exit 0 ;; esac
TARGET="$1"; shift

SSH_OPTS=(-o ServerAliveInterval=30 -o StrictHostKeyChecking=accept-new)
REMOTE_DIR="milady-2027"
GIT_URL=""
BRANCH="main"
SYNC_ONLY=0
BOOTSTRAP_ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        -i) SSH_OPTS+=(-i "$2"); shift ;;
        -p) SSH_OPTS+=(-p "$2"); shift ;;
        --dir) REMOTE_DIR="$2"; shift ;;
        --git) GIT_URL="$2"; shift ;;
        --branch) BRANCH="$2"; shift ;;
        --sync-only) SYNC_ONLY=1 ;;
        --) shift; BOOTSTRAP_ARGS=("$@"); break ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown option: $1 (see --help)" >&2; exit 2 ;;
    esac
    shift
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# shellcheck disable=SC2029  # the arguments are deliberately expanded on the laptop side
ssh_run() { ssh "${SSH_OPTS[@]}" "${TARGET}" "$@"; }

echo "==> Connecting to ${TARGET}"
# shellcheck disable=SC2016  # expanded on the VM
ssh_run 'echo "   $(hostname) : $(. /etc/os-release && echo "$PRETTY_NAME"), $(nproc) CPU, $(free -g | awk "/Mem:/{print \$2}") GB RAM"; command -v nvidia-smi >/dev/null && nvidia-smi -L || echo "   (no nvidia-smi)"'

if [[ -n "${GIT_URL}" ]]; then
    echo "==> Git clone / update on the VM (${GIT_URL}, ${BRANCH})"
    # The variables are expanded here (laptop side): single quotes in the remote command.
    ssh_run "set -euo pipefail
        command -v git >/dev/null || { sudo apt-get update -y && sudo apt-get install -y git make; }
        if [ -d '${REMOTE_DIR}/.git' ]; then
            git -C '${REMOTE_DIR}' fetch --tags origin
            git -C '${REMOTE_DIR}' checkout '${BRANCH}'
            git -C '${REMOTE_DIR}' pull --ff-only
        else
            git clone --branch '${BRANCH}' '${GIT_URL}' '${REMOTE_DIR}'
        fi"
else
    echo "==> Copying the local tree to ${TARGET}:${REMOTE_DIR} (rsync)"
    ssh_run "command -v rsync >/dev/null || { sudo apt-get update -y && sudo apt-get install -y rsync make; }; mkdir -p '${REMOTE_DIR}'"
    # Excluded files are neither copied nor deleted on the VM side (--delete does not touch excluded files).
    # Anchored patterns ("/data/"): the package src/milady/data/ must, for its part, be copied.
    rsync -az --delete --info=stats1 \
        -e "ssh ${SSH_OPTS[*]}" \
        --exclude '/.venv/' --exclude '/.venv-front/' --exclude '/data/' --exclude '/backups/' \
        --exclude '/mlruns/' --exclude '.env' --exclude '/*.sif' --exclude '*.tar' \
        --exclude '__pycache__/' --exclude '.pytest_cache/' --exclude '.quarto/' \
        --exclude 'node_modules/' \
        "${REPO_ROOT}/" "${TARGET}:${REMOTE_DIR}/"
fi

if [[ ${SYNC_ONLY} -eq 1 ]]; then
    echo "==> --sync-only: bootstrap not run. On the VM: cd ${REMOTE_DIR} && sudo infra/deploy/bootstrap_vm.sh"
    exit 0
fi

echo "==> bootstrap_vm.sh ${BOOTSTRAP_ARGS[*]:-} (sudo on the VM; password may be requested)"
# -t: pseudo-terminal for sudo and live output.
ssh -t "${SSH_OPTS[@]}" "${TARGET}" "cd '${REMOTE_DIR}' && sudo infra/deploy/bootstrap_vm.sh ${BOOTSTRAP_ARGS[*]:-}"

host="${TARGET#*@}"
cat <<EOF

==> Deployment finished. Web interfaces through an SSH tunnel:
    ssh -N -L 5000:localhost:5000 -L 9001:localhost:9001 ${TARGET}
    then http://localhost:5000 (MLflow) and http://localhost:9001 (MinIO console).
    Commands: ssh ${TARGET} 'cd ${REMOTE_DIR} && make sweep CONFIG=infra/configs/palier2_abc3d.yaml'
    Do not forget: make backup then delete the VM ${host} to stop billing.
EOF
