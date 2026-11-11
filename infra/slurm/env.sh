# shellcheck shell=bash
# Environment shared by the MilaDy Slurm templates (sourced by gen_data.sbatch, train.sbatch, eval.sbatch).
# Do not run directly: `source infra/slurm/env.sh` in a Slurm script.
#
# All variables can be overridden before `sbatch` (Slurm forwards the submission environment
# by default) or in ~/.config/milady/slurm.env (read if it exists):
#
#   MILADY_ROOT          cloned repository (default: submission directory SLURM_SUBMIT_DIR)
#   MILADY_SIF           Apptainer/Singularity image; default: $SINGULARITY_ALLOWED_DIR/milady.sif
#                        (Jean Zay), otherwise $MILADY_ROOT/milady.sif; "none" → no container
#                        (MILADY_VENV venv or the centre's Python module)
#   MILADY_VENV          venv to activate when MILADY_SIF=none (default: $MILADY_ROOT/.venv)
#   MILADY_MODULES       modules to load (default: "singularity" if the module command exists
#                        and no apptainer/singularity is in the PATH)
#   MILADY_DATA          data root (default: $SCRATCH/milady, otherwise $WORK/milady, otherwise
#                        $MILADY_ROOT/data)
#   MILADY_STATE         persistent catalogue and tracking (default: $WORK/milady, otherwise $MILADY_ROOT/data)
#   MILADY_DB_URL        catalogue (default: sqlite:///$MILADY_STATE/catalog.sqlite; PostgreSQL
#                        only possible if the compute nodes can reach it)
#   MILADY_STORAGE_URI   storage of the MFF files (default: file://$MILADY_DATA/store)
#   MLFLOW_TRACKING_URI  tracking (default: sqlite:///$MILADY_STATE/mlflow.db; no Internet on
#                        the Jean Zay compute nodes)

if [[ -f "${HOME}/.config/milady/slurm.env" ]]; then
    # shellcheck disable=SC1091
    source "${HOME}/.config/milady/slurm.env"
fi

export MILADY_ROOT="${MILADY_ROOT:-${SLURM_SUBMIT_DIR:-$(pwd)}}"

# --- Modules and container engine ------------------------------------------------------------
if [[ -z "${MILADY_MODULES+x}" ]]; then
    MILADY_MODULES=""
    if ! command -v apptainer >/dev/null 2>&1 && ! command -v singularity >/dev/null 2>&1 \
        && command -v module >/dev/null 2>&1; then
        MILADY_MODULES="singularity"   # Jean Zay : « module load singularity »
    fi
fi
if [[ -n "${MILADY_MODULES}" ]] && command -v module >/dev/null 2>&1; then
    module purge
    # shellcheck disable=SC2086
    module load ${MILADY_MODULES}
fi
if command -v apptainer >/dev/null 2>&1; then
    MILADY_CONTAINER_CMD="apptainer"
elif command -v singularity >/dev/null 2>&1; then
    MILADY_CONTAINER_CMD="singularity"
else
    MILADY_CONTAINER_CMD=""
fi

if [[ -z "${MILADY_SIF:-}" ]]; then
    if [[ -n "${SINGULARITY_ALLOWED_DIR:-}" && -f "${SINGULARITY_ALLOWED_DIR}/milady.sif" ]]; then
        MILADY_SIF="${SINGULARITY_ALLOWED_DIR}/milady.sif"
    else
        MILADY_SIF="${MILADY_ROOT}/milady.sif"
    fi
fi
export MILADY_SIF

# --- Data, catalogue, tracking ------------------------------------------------------------------
if [[ -z "${MILADY_DATA:-}" ]]; then
    if [[ -n "${SCRATCH:-}" ]]; then MILADY_DATA="${SCRATCH}/milady"
    elif [[ -n "${WORK:-}" ]]; then MILADY_DATA="${WORK}/milady"
    else MILADY_DATA="${MILADY_ROOT}/data"; fi
fi
if [[ -z "${MILADY_STATE:-}" ]]; then
    if [[ -n "${WORK:-}" ]]; then MILADY_STATE="${WORK}/milady"; else MILADY_STATE="${MILADY_ROOT}/data"; fi
fi
mkdir -p "${MILADY_DATA}/store" "${MILADY_STATE}"
export MILADY_DATA MILADY_STATE
export MILADY_DB_URL="${MILADY_DB_URL:-sqlite:///${MILADY_STATE}/catalog.sqlite}"
export MILADY_STORAGE_URI="${MILADY_STORAGE_URI:-file://${MILADY_DATA}/store}"
export MLFLOW_TRACKING_URI="${MLFLOW_TRACKING_URI:-sqlite:///${MILADY_STATE}/mlflow.db}"
export MILADY_HOST="${MILADY_HOST:-${SLURM_CLUSTER_NAME:-$(hostname -s)}}"
export PYTHONUNBUFFERED=1
# OpenMP/BLAS threads = cores reserved per task (avoids oversubscription).
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-${SLURM_CPUS_PER_TASK:-1}}"

# --- Execution ----------------------------------------------------------------------------------
# Provenance: commit of the mounted repository, read on the host. The image may have been built at another
# commit (MILADY_GIT_COMMIT variable baked into the Docker image): it is replaced at each run.
milady_host_commit() {
    local c
    c="$(git -C "${MILADY_ROOT}" -c safe.directory='*' rev-parse --short=12 HEAD 2>/dev/null)" || return 0
    if git -C "${MILADY_ROOT}" -c safe.directory='*' -c core.fsmonitor=false diff --quiet HEAD -- 2>/dev/null; then
        echo "${c}"
    else
        echo "${c}-dirty"
    fi
}

# milady_run CMD...: run CMD in the image (repository mounted on /opt/milady, GPU via --nv) or, failing
# that, in the venv / current environment. The working directory is the repository root.
milady_run() {
    if [[ "${MILADY_SIF}" != "none" ]]; then
        if [[ -z "${MILADY_CONTAINER_CMD}" ]]; then
            echo "apptainer/singularity not found; MILADY_SIF=none to use a venv" >&2
            return 1
        fi
        if [[ ! -f "${MILADY_SIF}" ]]; then
            echo "Image not found: ${MILADY_SIF} (see infra/slurm/README-slurm.md)" >&2
            return 1
        fi
        local binds="${MILADY_ROOT}:/opt/milady,${MILADY_DATA},${MILADY_STATE}"
        # Empty commit (git absent on the node): the Python code re-reads it from the mounted repository.
        local commit
        commit="$(milady_host_commit)"
        # --nv: host CUDA driver and libraries; without a GPU, just a warning.
        "${MILADY_CONTAINER_CMD}" exec --nv --bind "${binds}" --pwd /opt/milady \
            --env "PYTHONNOUSERSITE=1,MILADY_ROOT=/opt/milady,MILADY_GIT_COMMIT=${commit}" \
            "${MILADY_SIF}" "$@"
    else
        if [[ -f "${MILADY_VENV:-${MILADY_ROOT}/.venv}/bin/activate" ]]; then
            # shellcheck disable=SC1091
            source "${MILADY_VENV:-${MILADY_ROOT}/.venv}/bin/activate"
        fi
        (cd "${MILADY_ROOT}" && "$@")
    fi
}

milady_banner() {
    echo "== MilaDy / Slurm: job ${SLURM_JOB_ID:-?}${SLURM_ARRAY_TASK_ID:+[${SLURM_ARRAY_TASK_ID}]} on $(hostname)"
    echo "   repository: ${MILADY_ROOT}"
    echo "   image     : ${MILADY_SIF} (${MILADY_CONTAINER_CMD:-no engine})"
    echo "   data      : ${MILADY_STORAGE_URI}"
    echo "   catalogue : ${MILADY_DB_URL%%\?*}   tracking: ${MLFLOW_TRACKING_URI}"
    command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L || true
}
