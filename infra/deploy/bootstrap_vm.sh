#!/usr/bin/env bash
# Full MilaDy installation on a fresh Ubuntu 22.04 / 24.04 VM (cloud GPU or CPU).
#
# Usage (from the cloned repository):
#   git clone https://github.com/knoel99/milady-2027.git && cd milady-2027
#   sudo infra/deploy/bootstrap_vm.sh [--cpu] [--no-smoke] [--no-build]
#
# Steps (each idempotent: re-running the script breaks nothing):
#   1. base system packages;
#   2. Docker Engine + compose plugin from the official Docker repository;
#   3. if nvidia-smi sees a GPU: NVIDIA Container Toolkit (official NVIDIA repository);
#      otherwise, an explicit message (install the driver or choose a provider GPU image);
#   4. infra/docker/.env with random passwords (openssl rand), never overwritten;
#   5. build the images (milady:gpu or milady:cpu, MLflow server);
#   6. start db (PostgreSQL), s3 (MinIO), mlflow and wait for the healthchecks;
#   7. make smoke (tiny simulation → MFF → S3 → catalogue → training → evaluation).
#
# Options :
#   --cpu        ignore the GPU even if present (CPU image)
#   --no-smoke   do not run the smoke test
#   --no-build   do not (re)build the images (already built)
#   -h, --help   this help
#
# Optional variables:
#   MILADY_BUILD_CACERT=/path/ca.pem   TLS proxy certificate (image build)
set -euo pipefail

# --- Arguments --------------------------------------------------------------------------------
FORCE_CPU=0
RUN_SMOKE=1
DO_BUILD=1
while [[ $# -gt 0 ]]; do
    case "$1" in
        --cpu) FORCE_CPU=1 ;;
        --no-smoke) RUN_SMOKE=0 ;;
        --no-build) DO_BUILD=0 ;;
        -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
        *) echo "Unknown option: $1 (see --help)" >&2; exit 2 ;;
    esac
    shift
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${REPO_ROOT}/infra/docker/.env"
COMPOSE=(docker compose -f "${REPO_ROOT}/infra/docker/docker-compose.yml" --env-file "${ENV_FILE}")
OWNER="${SUDO_USER:-$(id -un)}"

log()  { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[1;33m[warning]\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m[error]\033[0m %s\n' "$*" >&2; exit 1; }

[[ "$(id -u)" -eq 0 ]] || die "run with sudo: sudo $0 $*"
[[ -f "${REPO_ROOT}/infra/docker/docker-compose.yml" ]] || die "incomplete repository: ${REPO_ROOT}"

# --- 0. System -------------------------------------------------------------------------------
# shellcheck disable=SC1091
. /etc/os-release
if [[ "${ID:-}" != "ubuntu" ]]; then
    warn "system ${PRETTY_NAME:-unknown}: script designed for Ubuntu 22.04/24.04 (continuing)."
elif [[ "${VERSION_ID:-}" != "22.04" && "${VERSION_ID:-}" != "24.04" ]]; then
    warn "Ubuntu ${VERSION_ID} untested (22.04 and 24.04 are): continuing."
fi
CODENAME="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
export DEBIAN_FRONTEND=noninteractive

# --- 1. Base packages -----------------------------------------------------------------------
log "1/7 Base system packages"
apt-get update -y
apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg git make openssl rsync jq pciutils htop tmux unzip python3 python3-yaml

# --- 2. Docker (official repository) ---------------------------------------------------------------
log "2/7 Docker Engine + compose"
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    echo "Docker already installed: $(docker --version); $(docker compose version)"
else
    # Procedure from https://docs.docker.com/engine/install/ubuntu/ (checked on 2026-11-07).
    # a) Conflicting packages (Ubuntu's docker.io, podman-docker...): they prevent the installation of
    #    docker-ce. "apt-get remove" (not purge) keeps /var/lib/docker (images, volumes).
    mapfile -t conflicts < <(dpkg-query -W -f='${binary:Package} ${db:Status-Status}\n' \
        docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc \
        2>/dev/null | awk '$2 == "installed" {print $1}')
    if [[ ${#conflicts[@]} -gt 0 ]]; then
        warn "packages incompatible with Docker CE, removed: ${conflicts[*]}"
        apt-get remove -y "${conflicts[@]}"
    fi
    # b) Official GPG key and repository, in the deb822 format of the current documentation.
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    rm -f /etc/apt/sources.list.d/docker.list   # old one-line syntax: no duplicate source
    printf '%s\n' \
        "Types: deb" \
        "URIs: https://download.docker.com/linux/ubuntu" \
        "Suites: ${CODENAME}" \
        "Components: stable" \
        "Architectures: $(dpkg --print-architecture)" \
        "Signed-By: /etc/apt/keyrings/docker.asc" \
        > /etc/apt/sources.list.d/docker.sources
    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi
# systemd absent (WSL, container): Docker is assumed to be already running.
has_systemd() { command -v systemctl >/dev/null 2>&1 && [[ -d /run/systemd/system ]]; }
if has_systemd; then
    systemctl enable --now docker
fi
docker info >/dev/null 2>&1 || die "the Docker daemon is not responding (systemctl status docker)"
if [[ "${OWNER}" != "root" ]] && ! id -nG "${OWNER}" | tr ' ' '\n' | grep -qx docker; then
    usermod -aG docker "${OWNER}"
    echo "User ${OWNER} added to the docker group (effective at the next SSH login)."
fi

# --- 3. NVIDIA GPU ----------------------------------------------------------------------------
log "3/7 NVIDIA GPU"
GPU=0
if [[ ${FORCE_CPU} -eq 1 ]]; then
    echo "--cpu: GPU ignored."
elif command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1; then
    GPU=1
    nvidia-smi -L
    nvidia-smi --query-gpu=driver_version,memory.total --format=csv,noheader | head -n 1
    if ! command -v nvidia-ctk >/dev/null 2>&1; then
        # Procedure from the NVIDIA documentation (install-guide, "stable" repository, checked on 2026-11-07).
        curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
            | gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
        curl -fsSL https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
            | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
            > /etc/apt/sources.list.d/nvidia-container-toolkit.list
        apt-get update -y
        apt-get install -y nvidia-container-toolkit
    else
        echo "NVIDIA Container Toolkit already installed: $(nvidia-ctk --version | head -n 1)"
    fi
    # Declare the nvidia runtime in /etc/docker/daemon.json (idempotent). Docker is only restarted
    # if the file changed: re-running the script does not interrupt running containers.
    daemon_before="$(sha256sum /etc/docker/daemon.json 2>/dev/null || true)"
    nvidia-ctk runtime configure --runtime=docker
    if [[ "$(sha256sum /etc/docker/daemon.json 2>/dev/null || true)" != "${daemon_before}" ]]; then
        if has_systemd; then systemctl restart docker; else warn "restart the Docker daemon by hand"; fi
    else
        echo "nvidia runtime already declared to Docker: no restart."
    fi
elif lspci 2>/dev/null | grep -qi nvidia; then
    warn "NVIDIA card present but driver missing (nvidia-smi does not respond)."
    cat >&2 <<'MSG'
  Two solutions:
    a) install the driver then reboot the VM, and re-run this script:
         sudo apt-get install -y ubuntu-drivers-common && sudo ubuntu-drivers install --gpgpu
         sudo reboot
    b) recreate the VM with a provider "GPU / Deep Learning" image (NVIDIA driver
       preinstalled), which is the simplest.
  Meanwhile we continue in CPU mode (milady:cpu image).
MSG
else
    echo "No NVIDIA GPU detected: CPU mode. (For a GPU VM, choose a provider image"
    echo "with the NVIDIA driver preinstalled, or install the driver: ubuntu-drivers install --gpgpu.)"
fi
WORKER=worker
[[ ${GPU} -eq 1 ]] && WORKER=worker-gpu

# --- 4. .env file --------------------------------------------------------------------------
log "4/7 Configuration infra/docker/.env"
if [[ ${GPU} -eq 1 ]]; then
    "${REPO_ROOT}/infra/deploy/gen_env.sh" --gpu --owner "${OWNER}"
else
    "${REPO_ROOT}/infra/deploy/gen_env.sh" --cpu --owner "${OWNER}"
fi
# The compute container chosen here takes precedence over an earlier value (e.g. switching CPU → GPU).
sed -i "s/^MILADY_WORKER=.*/MILADY_WORKER=${WORKER}/" "${ENV_FILE}"
# Provenance: repository commit (read as the owner to avoid "dubious ownership").
GIT_COMMIT="$(sudo -u "${OWNER}" git -C "${REPO_ROOT}" rev-parse --short=12 HEAD 2>/dev/null || true)"
export GIT_COMMIT

# Local data (repository mounted in the containers): data/ belongs to the container UID.
CUID="$(sed -n 's/^MILADY_UID=//p' "${ENV_FILE}" | tail -n 1)"
CGID="$(sed -n 's/^MILADY_GID=//p' "${ENV_FILE}" | tail -n 1)"
install -d -o "${CUID:-1000}" -g "${CGID:-1000}" "${REPO_ROOT}/data"

# --- 5. Images ----------------------------------------------------------------------------------
log "5/7 Building the images (${WORKER}, mlflow)"
if [[ ${DO_BUILD} -eq 1 ]]; then
    # Via the Makefile (docker build): accepts MILADY_BUILD_CACERT, same image names as compose.
    if [[ ${GPU} -eq 1 ]]; then
        make -C "${REPO_ROOT}" image-gpu image-mlflow
    else
        make -C "${REPO_ROOT}" image image-mlflow
    fi
else
    echo "--no-build: build skipped."
fi
if [[ ${GPU} -eq 1 ]]; then
    echo "Checking GPU access from a container:"
    "${COMPOSE[@]}" run --rm --no-deps "${WORKER}" nvidia-smi -L \
        || die "the container cannot see the GPU (check nvidia-ctk runtime configure, then restart Docker)"
fi

# --- 6. Services --------------------------------------------------------------------------------
log "6/7 Starting db, s3, mlflow (waiting for the healthchecks)"
"${COMPOSE[@]}" up -d --wait --wait-timeout 300 db s3 mlflow
"${COMPOSE[@]}" ps --all

# --- 7. Smoke test -------------------------------------------------------------------------
if [[ ${RUN_SMOKE} -eq 1 ]]; then
    log "7/7 Smoke test (make smoke)"
    make -C "${REPO_ROOT}" smoke RUN=docker WORKER="${WORKER}"
else
    log "7/7 Smoke test skipped (--no-smoke); later: make smoke"
fi

# --- Summary -------------------------------------------------------------------------------------
IP="$(curl -fsS -m 3 https://api.ipify.org 2>/dev/null || hostname -I | awk '{print $1}')"
cat <<EOF

MilaDy is ready on this machine (compute container: ${WORKER}).

From your laptop, open an SSH tunnel to the web interfaces (ports bound to 127.0.0.1):
  ssh -N -L 5000:localhost:5000 -L 9001:localhost:9001 -L 8888:localhost:8888 ${OWNER}@${IP}
  MLflow: http://localhost:5000      MinIO console: http://localhost:9001
  (MinIO credentials: S3_ROOT_USER / S3_ROOT_PASSWORD in ${ENV_FILE})

Useful commands (in ${REPO_ROOT}):
  make sweep CONFIG=infra/configs/palier2_abc3d.yaml     simulation campaign
  make train CONFIG=infra/configs/train_fm3d.yaml        training
  make backup BACKUP_TARGET=s3://my-bucket/backups       backup (before shutting down!)
  make down                                              stop the services

BILLING: a stopped GPU VM ("stopped") may still be billed (disk, IP, sometimes the GPU
depending on the provider). After the backup, DELETE the VM (see infra/README.md, "Stop paying").
EOF
