# MilaDy on a Slurm cluster (Jean Zay, mesocentres, Slurm in the cloud)

This folder contains the templates for launching MilaDy campaigns on a supercomputer:

| File | Role |
|---|---|
| `env.sh` | common environment (Apptainer image, `$WORK`/`$SCRATCH`, catalog, MLflow), `milady_run` function |
| `gen_data.sbatch` | **job array**: one simulation per element, 1 GPU each |
| `train.sbatch` | **multi-GPU / multi-node** training: one `torchrun` per node, `MASTER_ADDR:MASTER_PORT` rendezvous |
| `eval.sbatch` | evaluation of a model (1 GPU) |
| `apptainer.def` | definition of the Apptainer image (base `docker://pytorch/pytorch`) |

Principle: **computations run in an Apptainer image (`.sif`) converted from the GPU Docker image of the cloud
VM**, the repository being mounted on `/opt/milady` (the commit of the mounted repository, not that of the image
build, is recorded in the files and in the catalog). On the login node, only the submission of
campaigns needs a small Python environment (§1). The code and the dependencies are the same from one target to
the other; results are bit-for-bit identical only on the same hardware, and an image built from
`apptainer.def` does not have the same system packages.

## 1. Quick start (any Slurm cluster with Apptainer)

```bash
# On the login node (connection node)
cd $WORK                       # or a working folder on a shared file system
git clone https://github.com/knoel99/milady-2027.git && cd milady-2027

# Image: see §3 (built elsewhere then copied, or pulled from a registry)
ls milady.sif

# Light Python on the login node to submit (once): milady.sweep calls `sbatch`, which is absent from
# the image, so it runs OUTSIDE the container. PyYAML, NumPy and SQLAlchemy are enough (no torch).
# Python >= 3.11 required: if `python3 --version` is older (RHEL 9: 3.9), first load a recent
# Python module of the center (`module avail python`, exact name to adapt).
python3 -m venv .venv-front && .venv-front/bin/pip install pyyaml numpy sqlalchemy "psycopg[binary]"
.venv-front/bin/pip install --no-deps -e .         # (or `make setup`, heavier: includes torch CPU)

# Simulation campaign (the YAML → job array expansion is done by milady.sweep)
.venv-front/bin/python -m milady.sweep infra/configs/palier2_abc3d.yaml --scheduler slurm

# Or by hand: the 37 simulations of palier2_abc3d (indices 0 to 36), at most 16 at once
sbatch --array=0-36%16 infra/slurm/gen_data.sbatch infra/configs/palier2_abc3d.yaml

# Training on 2 nodes of 4 GPUs, then evaluation
sbatch --nodes=2 --gres=gpu:4 infra/slurm/train.sbatch infra/configs/train_fm3d.yaml
sbatch infra/slurm/eval.sbatch infra/configs/train_fm3d.yaml

squeue --me                    # monitoring; logs: data/sweeps/<campaign>/<timestamp>/milady-sim-<campaign>-<job>_<task>.out
                                # (milady.sweep, path printed), or milady-sim-<job>_<task>.out in the submission folder (sbatch by hand)
```

The scripts are submitted **from the repository root** (Slurm runs a copy of the script: the repository
is found through `SLURM_SUBMIT_DIR` or through the `MILADY_ROOT` variable).

Do not run `milady.sweep --scheduler slurm` inside `apptainer exec`: `sbatch` does not exist in the
image, and the repository root there is `/opt/milady`, a path the jobs would not find on the host.

**End of time limit and resumption.** `gen_data.sbatch` launches the simulation in an `srun` step and
requests `--signal=TERM@120`: 120 s before the limit, the simulation receives SIGTERM, writes its
checkpoint (in `$MILADY_DATA/work/…`, on `$SCRATCH`) and stops (status `failed`, note
`interrupted` in the catalog). Resubmitting the same indices resumes from the last checkpoint:
`.venv-front/bin/python -m milady.sweep <campaign.yaml> --scheduler slurm` only resubmits the
simulations that are `queued` or `failed` (`--indices 3,7` to choose some); a simulation left `running` (node lost
without SIGTERM) is resubmitted only with `--retry-running`.

**Cores per task.** Since Slurm 22.05, `srun` no longer necessarily inherits `sbatch`'s `--cpus-per-task`:
the templates give it explicitly to `srun` (otherwise the whole step, including the
`torchrun` processes of a node, would be confined to a single core).

Settings: all the variables of `env.sh` (`MILADY_SIF`, `MILADY_DATA`, `MILADY_DB_URL`…) can be
exported before `sbatch` or written once and for all in `~/.config/milady/slurm.env`:

```bash
mkdir -p ~/.config/milady
cat > ~/.config/milady/slurm.env <<'EOF'
MILADY_SIF=$WORK/milady-2027/milady.sif
MILADY_DATA=$SCRATCH/milady
EOF
```

The `#SBATCH` options of the templates are **generic** (1 GPU, 8 cores, 4 h for a simulation;
1 node of 4 GPUs, 20 h for training): account, partition, constraint and QoS **must be adapted
to the center** — on the command line (`sbatch --account=… -C …`) rather than by modifying the files.

## 2. Jean Zay (IDRIS)

Information checked on 2026-11-07 in the IDRIS documentation (links at the end of the section). It
changes: reread the documentation before a major campaign.

### Account and hours

- Each job must indicate the project **and the type of hours**: `--account=<project>@cpu`,
  `@v100`, `@a100` or `@h100`; `<project>` is the value of `$IDRPROJ` (`idrproj` lists your projects).
- GPU hours are obtained through a DARI request (dynamic or regular access); an internship normally goes
  through the host team's project.

### GPU partitions and Slurm options

| Nodes | Option | CPU / node | GPU / node | Max. duration |
|---|---|---|---|---|
| V100 16/32 GB (4 GPUs) | default (`-C v100-16g` or `-C v100-32g` to force) | 40 | 4 | 100 h |
| V100 32 GB (8 GPUs) | `--partition=gpu_p2` (`gpu_p2s`, `gpu_p2l`) | 24 | 8 | 100 h |
| A100 80 GB (8 GPUs, 52 nodes) | `-C a100` | 64 (AMD) | 8 | 20 h |
| H100 80 GB (4 GPUs, 364 nodes) | `-C h100` | 96 | 4 | 100 h |

- Before any module on A100 / H100: `module load arch/a100` or `module load arch/h100` (unnecessary with
  the Apptainer image, which contains its own CUDA stack; useful if using IDRIS's PyTorch modules).
- Default duration: **10 minutes** — always specify `--time`.
- A job on more than one node is in **exclusive mode**: whole nodes are billed.
- `--hint=nomultithread` is used in IDRIS's examples (and in our templates).

### QoS (quality of service)

| Partition | Default QoS (≤ 20 h) | Long (≤ 100 h) | Development (≤ 2 h) |
|---|---|---|---|
| V100 | `qos_gpu-t3` | `qos_gpu-t4` (16 GPUs max. per job) | `qos_gpu-dev` |
| A100 | `qos_gpu_a100-t3` | — (no QoS > 20 h on A100) | `qos_gpu_a100-dev` |
| H100 | `qos_gpu_h100-t3` | `qos_gpu_h100-t4` (16 GPUs max. per job) | `qos_gpu_h100-dev` |

The `-dev` QoS are limited to 10 jobs (running or pending) per user and 32 GPUs.
The number of array elements running simultaneously is limited with `%`: `--array=0-199%16`.

Examples:

```bash
# Simulations: 1 H100 GPU and 1/4 of the node (24 cores) per simulation
sbatch --account=abc@h100 -C h100 --cpus-per-task=24 --time=10:00:00 \
       --array=0-36%16 infra/slurm/gen_data.sbatch infra/configs/palier2_abc3d.yaml
# Training: 2 full H100 nodes
sbatch --account=abc@h100 -C h100 --nodes=2 --gres=gpu:4 --cpus-per-task=96 --time=20:00:00 \
       infra/slurm/train.sbatch infra/configs/train_fm3d.yaml
# Quick test in the development queue
sbatch --account=abc@h100 -C h100 --qos=qos_gpu_h100-dev --time=00:30:00 \
       infra/slurm/eval.sbatch infra/configs/train_fm3d.yaml
```

### Disk spaces

| Variable | Use for MilaDy | Characteristics |
|---|---|---|
| `$HOME` | configuration (`~/.config/milady/slurm.env`) | 3 GB, backed up |
| `$WORK` | cloned repository, `.sif` image, **SQLite catalog** and MLflow database (`$WORK/milady/`) | per-project quota (5 TB by default), not backed up |
| `$SCRATCH` | **MFF files** of the campaigns (`$SCRATCH/milady/store`) | fast SSD, unused files **deleted after 30 days** |
| `$STORE` | long-term archiving of the final datasets | not accessible from the compute nodes |

After a campaign: copy the files to keep from `$SCRATCH` to `$WORK`/`$STORE`, or to the project's
S3 storage (§5).

### Containers: Singularity on Jean Zay

- The available engine is **Singularity** (`module load singularity`); Docker and Podman are not.
  `env.sh` loads this module automatically if it finds neither `apptainer` nor `singularity`.
- **Building from a `.def` file is impossible** (neither root nor `fakeroot`): build the image
  elsewhere (§3), or, once the image is published (§3; it is not yet), from a login node:
  `singularity build milady.sif docker://ghcr.io/knoel99/milady:gpu` (run from `$WORK`/`$SCRATCH`;
  memory is limited on the login nodes: prefer a `prepost` node for large images).
- An image can be used on the compute nodes only after being copied into the authorized space:
  `idrcontmgr cp milady.sif` (then `idrcontmgr ls`); `env.sh` then takes
  `$SINGULARITY_ALLOWED_DIR/milady.sif` by default. This space is limited to 20 containers.
- Jupyter and TensorBoard cannot be launched from a container on Jean Zay: use IDRIS's JupyterHub for
  interactive analysis.

### No Internet on the compute nodes

Jean Zay's compute nodes have **no Internet access** (downloads must be done from the
login nodes or the pre/post-processing nodes). Consequences for MilaDy:

- **catalog**: SQLite on `$WORK` (`MILADY_DB_URL=sqlite:///$WORK/milady/catalog.sqlite`, default value of
  `env.sh`). The catalog waits up to 120 s for a free lock: several simulations of an
  array can write to it. In case of stubborn locks on the parallel file system, keep
  only the writing of MFF files in the jobs, then register **after the fact** from the
  login node (jobs launched with `milady.sweep … --no-catalog`; h5py and fsspec required: `.venv-front/bin/pip install h5py fsspec`,
  or the `.venv` of `make setup`):
  `MILADY_DB_URL=sqlite:///$WORK/milady/catalog.sqlite .venv-front/bin/python -m milady.catalog ingest $SCRATCH/milady/store/<campagne>/*/fields.h5 --campaign <campagne>`;
- **MLflow tracking**: local SQLite database (`MLFLOW_TRACKING_URI=sqlite:///$WORK/milady/mlflow.db`), to be
  consulted with `mlflow ui --backend-store-uri sqlite:///…/mlflow.db` (from the laptop after copying,
  or IDRIS's JupyterHub);
- **synchronization to the cloud infrastructure** (PostgreSQL + S3 of the VM): see §5.

Sources (IDRIS documentation, consulted on 2026-11-07):
[GPU partitions and QoS](http://www.idris.fr/docs/jean-zay/slurm/slurm_partitions_gpu),
[multi-project accounts and `--account`](http://www.idris.fr/docs/jean-zay/gestion-compte/multi-projets),
[disk spaces](http://www.idris.fr/docs/jean-zay/environnement/espaces-disques),
[Singularity containers](http://www.idris.fr/docs/jean-zay/environnement/conteneurs),
[new user — no Internet on the compute nodes](http://www.idris.fr/docs/jean-zay/nouvel-utilisateur),
[PyTorch data parallelism](http://www.idris.fr/docs/jean-zay/intelligence_artificielle/distribution_parallelisme/data-parallelism-pytorch),
[job arrays](http://www.idris.fr/docs/jean-zay/slurm/exec_jobarray).

### Note on multi-GPU launching

IDRIS's documentation launches PyTorch DDP with `srun` (one Slurm task per GPU) and the `idr_torch`
library. Our templates launch **one `torchrun` per node** (one Slurm task per node), which works
identically in a container and on any cluster; `torchrun` sets `RANK`, `LOCAL_RANK`, `WORLD_SIZE`,
`MASTER_ADDR` and `MASTER_PORT` for each process. The two approaches are equivalent for DDP.

## 3. Building the `.sif` image

| Situation | Command |
|---|---|
| Machine with Docker and Apptainer (cloud VM, Linux laptop) | `make image-gpu && make sif` → `milady.sif` |
| Apptainer alone, with `--fakeroot` | `apptainer build --fakeroot milady.sif infra/slurm/apptainer.def` |
| Image published in a registry | `apptainer build milady.sif docker://ghcr.io/knoel99/milady:gpu` |
| Jean Zay | build elsewhere then `scp milady.sif jean-zay:$WORK/milady-2027/` and `idrcontmgr cp milady.sif` |

Publishing the image to the GitHub registry (once, from a machine with Docker):

```bash
echo "$GITHUB_TOKEN" | docker login ghcr.io -u <utilisateur> --password-stdin   # token with write:packages
docker tag milady:gpu ghcr.io/knoel99/milady:gpu && docker push ghcr.io/knoel99/milady:gpu
```

The image is several GB (CUDA stack): build it on `$WORK` or `$SCRATCH`, never in `$HOME`.

## 4. Other clusters

### Mesocentres (Slurm + Apptainer)

Same procedure; to adapt: `--partition` (name of the GPU partition, `sinfo -s`), `--account` if
requested, GPU type (`--gres=gpu:a100:1` or `--constraint`), disk variables (`$WORK`/`$SCRATCH`
do not exist everywhere: set `MILADY_DATA` and `MILADY_STATE`). If Apptainer is not installed:
`MILADY_SIF=none` and a venv (`make setup GPU=1`) or the center's Python modules. If the compute
nodes can reach a PostgreSQL server, `MILADY_DB_URL=postgresql://…` replaces SQLite.

### Slurm in the cloud

For several GPU nodes rented on demand: AWS ParallelCluster, Google Cloud HPC Toolkit (Cluster
Toolkit), Azure CycleCloud, or the "turnkey" Slurm clusters of GPU providers. The templates
work without modification (`--partition` to adapt); since the nodes have Internet, one can target
the VM stack directly (PostgreSQL catalog and S3):

```bash
export MILADY_DB_URL=postgresql://milady:<password>@<vm-private-ip>:5432/milady
export MILADY_STORAGE_URI=s3://milady-data MILADY_S3_ENDPOINT=http://<vm-private-ip>:9000
export AWS_ACCESS_KEY_ID=<S3_ACCESS_KEY de .env> AWS_SECRET_ACCESS_KEY=<S3_SECRET_KEY de .env>
export MLFLOW_TRACKING_URI=http://<vm-private-ip>:5000
```

(the VM must then publish its ports on the private network: `BIND_ADDR=<private-ip>` in `infra/docker/.env`
and `<private-ip>,<private-ip>:*` added to `MLFLOW_ALLOWED_HOSTS`, with a firewall limited to the cluster's subnet).

## 5. Bringing results back to the central infrastructure

From the login node (which has Internet access) or after copying to the laptop:

```bash
# 1. MFF files to the project's S3 storage (mc, rclone or aws s3 sync)
mc alias set milady https://<point-d-accès-s3> <clé> <secret>
mc mirror $SCRATCH/milady/store/palier2_abc3d milady/milady-data/palier2_abc3d
# 2. Registration in the central catalog (idempotent: can be rerun). The shell does not expand
#    s3:// wildcards: the objects are listed with mc find.
export MILADY_DB_URL=postgresql://milady:<password>@<host>:5432/milady
export MILADY_S3_ENDPOINT=https://<point-d-accès-s3> AWS_ACCESS_KEY_ID=<clé> AWS_SECRET_ACCESS_KEY=<secret>
python -m milady.catalog ingest --campaign palier2_abc3d \
  $(mc find milady/milady-data/palier2_abc3d --name fields.h5 | sed 's#^milady/#s3://#')
```

`ingest` reads the file's metadata (`milady_uuid`, parameters, code, commit, diagnostics): the
identifiers remain the same as in the cluster's SQLite catalog. Only the simulations, their files and
their diagnostics are registered (without compute time or resources); models, evaluations, tasks and
checkpoints (`$SCRATCH/milady/store/_models`) stay on the cluster. `ingest` requires h5py, fsspec and s3fs (`.venv` of
`make setup`), not the small submission venv.
