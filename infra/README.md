# Deploying MilaDy: GPU cloud VM, Slurm cluster, laptop

This guide explains, step by step, how to go from `git clone` to an MHD simulation campaign,
a training run and an evaluation, with data in the standard format (MFF, compatible with
The Well) and a central catalog of results. The architecture and the technical choices are
described in [`ARCHITECTURE.md`](../docs/ARCHITECTURE.md); the detailed contract (format, catalog
schema) in [`../docs/specs/infra.md`](../docs/specs/infra.md).

| Target | Used for | Main command |
|---|---|---|
| **A. GPU cloud VM** (rented by the hour) | 3D campaigns and training runs without access to a computing center | `sudo infra/deploy/bootstrap_vm.sh` |
| **B. Slurm cluster** (Jean Zay, mesocentre, cloud Slurm) | large campaigns, multi-node | `sbatch infra/slurm/…` — see [`slurm/README-slurm.md`](slurm/README-slurm.md) |
| **C. Laptop** (CPU) | development, tests, small 2D/3D grids | `make setup && make smoke` |

All commands are run **from the repository root**. `make help` lists the targets.

---

## 1. What you get

```
┌──────────────────────────── VM or laptop (docker compose) ──────────────────────────────┐
│  db        PostgreSQL 16  — "milady" catalog + "mlflow" database           127.0.0.1:5432 │
│  s3        MinIO          — buckets milady-data, milady-models, mlflow     127.0.0.1:9000 │
│                             (web console                                    127.0.0.1:9001)│
│  mlflow    MLflow 3       — training tracking                              127.0.0.1:5000 │
│  worker    image milady:cpu or milady:gpu — simulations, training, evaluation             │
│  jupyter   (optional)     — JupyterLab                                     127.0.0.1:8888 │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

The ports are open only on `127.0.0.1`: from the laptop, you reach them **through an SSH tunnel**
(§2.4). The passwords are generated at installation in `infra/docker/.env` (never committed).

## 2. Target A — cloud VM with GPU

### 2.1 Prerequisites

1. An account with a provider offering hourly GPU VMs (Scaleway, OVHcloud, AWS, Google
   Cloud, Azure, or GPU-specialized providers).
2. An **SSH key** (`ssh-keygen -t ed25519`) registered with the provider.
3. A VM with:
   - **Ubuntu 22.04 or 24.04**, preferably the provider's "GPU / Deep Learning" image
     (NVIDIA driver preinstalled: the script installs the rest);
   - a GPU suited to the grid size (§6.2);
   - a disk of **100 to 200 GB** (Docker images ≈ 15 GB, plus the data if they stay on
     the VM; with a provider S3 bucket, 100 GB is enough);
   - a firewall opening only **SSH (22)**.

### 2.2 One-command installation (on the VM)

```bash
ssh ubuntu@VM_IP
git clone https://github.com/knoel99/milady-2027.git && cd milady-2027
sudo infra/deploy/bootstrap_vm.sh            # options: --cpu, --no-smoke, --no-build
```

The script (idempotent, can be rerun):

1. installs the base packages and **Docker** from the official repository;
2. if `nvidia-smi` sees a GPU: installs the **NVIDIA Container Toolkit** and registers it with Docker;
   if an NVIDIA card is present without a driver: prints the procedure (install the driver
   with `ubuntu-drivers install --gpgpu` then reboot, or recreate the VM with a GPU image from the
   provider) and continues on CPU;
3. generates `infra/docker/.env` with random passwords (`openssl rand`);
4. builds the image (`milady:gpu`, CUDA 12.6, or `milady:cpu`) and the MLflow server image;
5. starts `db`, `s3` (bucket creation) and `mlflow`, and waits for their healthchecks to be green;
6. runs `make smoke`: tiny 3D simulation → MFF file → S3 → catalog → dataset →
   one-iteration training (logged in MLflow) → evaluation. Measured duration: 10 s.

Total duration: **3 min measured** on CPU (`--cpu`, Docker already present, cold image build;
33 s for a rerun with cached images, §11). On a fresh GPU VM, allow
5 to 20 minutes depending on network throughput (Docker installation, GPU image of several GB).

Behind a corporate or computing-center TLS proxy, give its certificate **on the same
line as `sudo`** (sudo does not pass environment variables):

```bash
sudo MILADY_BUILD_CACERT=/path/to/ca.pem infra/deploy/bootstrap_vm.sh
```

### 2.3 Other ways to install

**Without logging in (cloud-init)**: when creating the VM, paste
[`deploy/cloud-init.yaml`](deploy/cloud-init.yaml) into the "user data" / "cloud-init" field
of the console, after checking the repository URL and the user at the top of the file. Monitoring:
`ssh ubuntu@IP 'sudo tail -f /var/log/milady-bootstrap.log'`.

**From the laptop** (copy of your working tree, including unpushed changes):

```bash
infra/deploy/deploy_remote.sh ubuntu@VM_IP                 # rsync + bootstrap
infra/deploy/deploy_remote.sh ubuntu@IP -i ~/.ssh/id_ed25519 -- --no-smoke
infra/deploy/deploy_remote.sh ubuntu@IP --git https://github.com/knoel99/milady-2027.git
```

Rerunning the same command updates the VM (remote data and `.env` are preserved).

**Private repository**: on the VM, `git clone git@github.com:knoel99/milady-2027.git` with a
read-only deploy key (GitHub → Settings → Deploy keys), or `deploy_remote.sh` (rsync, no GitHub
access required on the VM).

### 2.4 Using the VM

After a new SSH connection (so that membership of the `docker` group takes effect):

```bash
cd milady-2027
make ps                                                    # service status
make sweep CONFIG=infra/configs/palier2_abc3d.yaml         # campaign (in the compute container)
make sweep CONFIG=infra/configs/palier2_abc3d.yaml SCHEDULER=docker   # one container per simulation
make train CONFIG=infra/configs/train_fm3d.yaml            # training (all GPUs, torchrun)
make eval  CONFIG=infra/configs/train_fm3d.yaml            # evaluation (MODEL=<uuid> for a specific model)
make shell                                                 # shell in the compute container
make logs SERVICE=mlflow                                   # logs of a service
```

Long campaigns are launched in `tmux` (installed) to survive a disconnection:
`tmux new -s milady`, then `Ctrl-b d` to detach and `tmux attach -t milady` to come back.

Web interfaces, from the laptop:

```bash
ssh -N -L 5000:localhost:5000 -L 9001:localhost:9001 -L 8888:localhost:8888 ubuntu@VM_IP
```

then <http://localhost:5000> (MLflow), <http://localhost:9001> (MinIO console, credentials
`S3_ROOT_USER` / `S3_ROOT_PASSWORD` from `infra/docker/.env`), <http://localhost:8888> (JupyterLab
after `make jupyter`, token `JUPYTER_TOKEN`).

Catalog on the command line (in the container):

```bash
make shell
python -m milady.catalog campaigns
python -m milady.catalog sims --campaign palier2_abc3d --param Rm__gt=8
python -m milady.catalog summary
```

### 2.5 Storing the data at the provider rather than on the VM

By default, files go into MinIO, hence **on the VM's disk**. For them to survive
the deletion of the VM, use a provider S3 bucket: create the bucket and an access key
in the console, then in `infra/docker/.env`:

```bash
MILADY_STORAGE_URI=s3://my-bucket-milady/data
MILADY_MODELS_URI=s3://my-bucket-milady/models
MILADY_S3_ENDPOINT=https://s3.fr-par.scw.cloud     # endpoint of the provider and region
MILADY_S3_ACCESS_KEY=<clé du fournisseur>
MILADY_S3_SECRET_KEY=<secret du fournisseur>
```

then `make down && make up`. Do not modify `S3_ACCESS_KEY` / `S3_SECRET_KEY`: these are the keys of the
MinIO account, still used by MLflow for its artifacts (`make backup` also copies them to the
bucket). The provider's keys are given only to the compute containers, never to MinIO.
Give this key rights limited to the MilaDy bucket alone (provider IAM policy).

## 3. Target B — Slurm cluster

See [`slurm/README-slurm.md`](slurm/README-slurm.md): Apptainer image built from the Docker
image (`make image-gpu && make sif`), job array for the simulations, multi-node `torchrun`
for training, detailed notes for Jean Zay (accounts `projet@h100`, partitions, QoS,
`$WORK`/`$SCRATCH`, no Internet on the compute nodes so SQLite catalog then
after-the-fact registration of the simulations in the central database from the MFF files
(`python -m milady.catalog ingest`), the models, evaluations and tasks remaining in the cluster's SQLite).

## 4. Target C — laptop

### 4.1 Without Docker (lightest)

Prerequisites: Python 3.11, 3.12 or 3.13 (lock checked under 3.13 here, under 3.12 in the Docker image),
the `venv` module (Debian/Ubuntu: `sudo apt install python3-venv`), `make`, 5 GB of disk space.
Ubuntu 22.04 only has Python 3.10: use the Docker stack there (§4.2) or install Python 3.12
(for example with `uv python install 3.12`, then `make setup PYTHON=…/python3.12`).

```bash
git clone https://github.com/knoel99/milady-2027.git && cd milady-2027
make setup                                # .venv + pinned dependencies (torch CPU) + pip install -e .
source .venv/bin/activate
make smoke RUN=local                      # SQLite catalog data/catalog.sqlite, files in data/store/
make test RUN=local
```

Full chain in portable mode (checked here on a campaign reduced to 4 simulations at 12³ and a
6-iteration training run, §11; real campaigns at 64³ require a GPU):

```bash
make sweep CONFIG=infra/configs/palier2_tg3d.yaml          # simulations → MFF → data/store + catalog
make train CONFIG=infra/configs/train_fm3d.yaml            # creates the dataset from the campaign, trains
make eval  CONFIG=infra/configs/train_fm3d.yaml            # latest "fm3d_tg3d" model (or MODEL=<uuid>)
python -m milady.catalog summary                           # mean/standard deviation per model, metric, parameters
```

For a quick trial, any key of the training configuration can be overridden
(`TRAIN_ARGS="--set train.iters=10 data.kmax=3 …"`). If `--set name=…` changes the model name,
`make eval` no longer finds it by name: pass `MODEL=<uuid>` (printed at the end of training).

In portable mode, `MILADY_DB_URL` and `MILADY_STORAGE_URI` are not defined: the catalog is
`data/catalog.sqlite` and the storage is `data/store/`. On a laptop with an NVIDIA GPU:
`make setup GPU=1` (CUDA 12.6).

### 4.2 With Docker (same stack as the VM, no GPU)

```bash
make env          # generates infra/docker/.env (random passwords) and data/
make image        # image milady:cpu (2 min cold; otherwise built at the first `make smoke`)
make up           # PostgreSQL + MinIO + MLflow
make smoke        # in the worker container (milady:cpu)
make down         # stop (the data stay in the Docker volumes)
```

Docker Desktop (macOS, Windows/WSL2) works; allow 8 GB of RAM for Docker.

## 5. Data and results

- **Files**: one MFF file (HDF5, compatible with The Well, `milady_*` attributes) per simulation, stored
  under `{MILADY_STORAGE_URI}/{campaign}/{simulation_uuid}/fields.h5`, with a SHA-256 checksum in the catalog.
- **Catalog**: campaigns, simulations (JSONB parameters, status, machine, compute time), files,
  diagnostics, datasets, models, evaluations, tasks; view `v_eval_summary`.
- **Training tracking**: MLflow (metrics and hyperparameters; checkpoints in `MILADY_MODELS_URI`, copied into the
  MLflow artifacts only with `mlflow.log_checkpoint: true`); `model.mlflow_run_id`
  links the catalog to MLflow.

## 6. Costs: how to estimate them

Prices vary by provider, region and mode (on demand, reserved, *spot* /
interruptible) and change often: this guide gives **no price**, but a method.

### 6.1 Formula

```
cost ≈ Σ_tasks (duration_h × n_GPU × GPU_hourly_price)        compute (a running VM is billed, even idle)
     + disk_volume_GB × price_GB_month × duration_months       VM disks and snapshots
     + object_volume_GB × price_GB_month × duration_months      S3 bucket
     + outgoing_volume_GB × price_GB_egress                     downloads out of the provider
```

The hourly price to use is that of the **whole instance** (CPU, RAM and GPU included), read from
the provider's pricing page on the day of the rental.

### 6.2 Measure before extrapolating

1. Run a single representative simulation (same resolution, same simulated duration) and read its
   compute time in the catalog (`wall_time_s`);
2. GPU hours of the campaign ≈ `wall_time_s × n_simulations / 3600` (1 GPU per simulation);
3. training ≈ duration of one epoch × number of epochs × number of GPUs;
4. afterwards, actual consumption can be read in the catalog:

```sql
-- compute hours per campaign (GPU hours only if each simulation has its own GPU, e.g. Slurm array)
SELECT c.name, round(CAST(sum(s.wall_time_s * CASE WHEN s.n_gpus > 1 THEN s.n_gpus ELSE 1 END) / 3600.0 AS NUMERIC), 1) AS heures_gpu
FROM simulation s JOIN campaign c ON c.id = s.campaign_id
WHERE s.status = 'done' GROUP BY c.name ORDER BY heures_gpu DESC;
```

Memory: a state (u, B) in float32 on an N³ grid takes 6 × N³ × 4 bytes, i.e. ≈ 0.4 GB
for N = 256 and ≈ 3.2 GB for N = 512. Measurement on processor (7 November 2026; torch 2.14.1 CPU,
Xeon 2.1 GHz, 4 threads; dynamic mode, ABC then random forcing, float32, 2 steps; resident memory
read from `/proc/self/status` and `getrusage`): the peak, minus the memory of Python and torch after
import, is 100 MB at 64³ (≈ 17 states) and 717 MB at 128³ (≈ 15 states, with both forcings).
Extrapolating to 15 states: ≈ 6 GB for 256³ (a 24 GB GPU is enough) and ≈ 48 GB for 512³ (80 GB
GPU). On GPU, the cuFFT workspace and PyTorch's allocator cache come on top:
check with `python -m milady.sim.mhd3d bench --device cuda` (maximum allocated memory) or
`nvidia-smi` during the test simulation.

### 6.3 Reducing the bill

- **Interruptible instances (*spot*)** for the simulation arrays: each simulation is
  independent and rerunnable (status `failed` if the simulation received SIGTERM, otherwise left `running`: rerun with
  `make sweep … SWEEP_ARGS=--retry-running`; `runtime.checkpoint_to_storage: true` to resume from the
  checkpoint after the loss of the VM);
- shut the VM down between two campaigns **and delete it** when it is no longer needed (§8);
- keep the data in an S3 bucket (cheaper than a VM disk per GB);
- size the GPU on the memory actually needed (§6.2) rather than on the largest model.

## 7. Backup and restoration

```bash
make backup                                     # → ./backups (PostgreSQL dumps + bucket mirror)
make backup BACKUP_TARGET=/mnt/disque-sauvegarde
BACKUP_S3_ENDPOINT=https://s3.fr-par.scw.cloud BACKUP_ACCESS_KEY=… BACKUP_SECRET_KEY=… \
  make backup BACKUP_TARGET=s3://my-bucket/milady-backups
```

`infra/deploy/backup.sh` produces compressed `pg_dump -Fc` dumps of the `milady` and `mlflow` databases
(rotation: last 14) and an incremental mirror of the buckets (`mc mirror`). To be run **before any
VM deletion**, and ideally every night via `cron` (example in the script's header).

Restoration on a new machine (after `make env && make up`):

```bash
C="docker compose -f infra/docker/docker-compose.yml --env-file infra/docker/.env"
$C exec -T db pg_restore -U milady -d milady --clean --if-exists < backups/db/milady-YYYYMMDDTHHMMSSZ.dump
$C exec -T db pg_restore -U milady -d mlflow --clean --if-exists < backups/db/mlflow-YYYYMMDDTHHMMSSZ.dump
$C run --rm --no-deps -v "$PWD/backups:/backup" --entrypoint /bin/sh s3-init -c \
  'mc alias set src http://s3:9000 "$S3_ROOT_USER" "$S3_ROOT_PASSWORD" &&
   for b in milady-data milady-models mlflow; do mc mirror --overwrite "/backup/objects/$b" "src/$b"; done'
```

## 8. Stop paying

A **stopped** VM often remains partly billed (disk, IP address, sometimes the reserved GPU,
depending on the provider). To really stop billing:

1. `make backup BACKUP_TARGET=…` to a bucket or the laptop, and check the backup;
2. `make down`;
3. in the provider's console: **delete the VM**, then check that no detached disk
   (volume), snapshot or reserved IP address remains;
4. the S3 bucket continues to be billed per GB-month: delete what is no longer useful.

Tip: set up a budget alert in the provider's console.

## 9. Troubleshooting

| Symptom | Likely cause and remedy |
|---|---|
| `permission denied … docker.sock` | log in again over SSH (`docker` group added by the script), or prefix with `sudo` |
| `bootstrap`: "NVIDIA card present but driver missing" | `sudo ubuntu-drivers install --gpgpu && sudo reboot`, then rerun the script; or use the provider's GPU image |
| the container does not see the GPU | `sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker`; test `docker run --rm --gpus all milady:gpu nvidia-smi` |
| `CUDA error: no kernel image` or driver too old | CUDA 12.6 image: driver ≥ 525; Blackwell GPU: build with `BASE_IMAGE=…cuda13.0…` (header of `Dockerfile.gpu`) |
| `make up`: a service stays `unhealthy` | `make logs SERVICE=<service>`; `make ps` |
| PostgreSQL: authentication refused after regenerating `.env` | the password is set when the volume is created: put the old `.env` back, or start from scratch (`docker compose … down -v` **erases the data**) |
| MLflow: `Invalid Host header` | add the name used to `MLFLOW_ALLOWED_HOSTS` (`.env`) |
| `pull access denied for minio/minio` | MinIO no longer publishes community images: keep `pgsty/minio` (default), or another S3 image via `MINIO_IMAGE`, or a provider bucket (§2.5) |
| `pip`: `CERTIFICATE_VERIFY_FAILED` during `docker build` (corporate proxy) | `make image MILADY_BUILD_CACERT=/path/to/ca.pem` (same for `image-gpu`, `image-mlflow`, `image-jupyter`) |
| disk full | `docker system df` then `docker image prune`; move the data to a bucket (§2.5) |
| `make smoke` fails | rerun with `MILADY_SMOKE_DEBUG=1`; the failing step is named; `make smoke RUN=local` isolates Docker; `python infra/deploy/smoke.py --allow-fallback` isolates the infrastructure (storage, catalog, MLflow) from a failure of the solver, the training or the metrics |
| `bootstrap` behind a proxy: `CERTIFICATE_VERIFY_FAILED` although `MILADY_BUILD_CACERT` is exported | `sudo` clears the environment: `sudo MILADY_BUILD_CACERT=/path/to/ca.pem infra/deploy/bootstrap_vm.sh` |
| `make sweep` (Docker): `Permission denied` on `/opt/milady/data` | repository owned by root: `make env` (or `bootstrap_vm.sh`) gives `data/` to the container's UID; otherwise `sudo install -d -o 1000 -g 1000 data` |
| `make setup`: `ensurepip is not available` | `sudo apt install python3-venv` (or `python3.12-venv`) |
| `make eval`: "specify --model" | no model with the configuration's name (`name:`): pass `MODEL=<uuid>` (`python -m milady.catalog summary`) |
| `torchrun` logs: `errno: 97 - Address family not supported` | harmless warning (no IPv6) |
| port 5432/9000/5000 already in use | change `DB_PORT`, `S3_PORT`, `MLFLOW_PORT` in `.env` |

## 10. Security

- No secret in the repository: `infra/docker/.env` (permissions 600) is ignored by git, only
  `.env.example` is versioned; backup credentials go through the environment.
- Ports bound to `127.0.0.1` (access through an SSH tunnel), including JupyterLab (8888, additionally protected by the
  `JUPYTER_TOKEN` token); do not open 5432, 9000, 9001, 5000, 8888 to the Internet.
  Docker bypasses the `ufw` firewall for published ports: never set `BIND_ADDR=0.0.0.0`
  on an exposed VM; for a Slurm cluster on the same private network, use the private address and a
  security group limited to the subnet (see `slurm/README-slurm.md` §4).
- MinIO: an application account (`S3_ACCESS_KEY`, read/write rights) distinct from the
  administrator account; the keys of a provider bucket (`MILADY_S3_ACCESS_KEY`) are given
  only to the compute containers, never to MinIO (§2.5).
- Passwords kept off the processes' command line (`ps`): the PostgreSQL URI of MLflow
  (`MLFLOW_BACKEND_STORE_URI`) and the Jupyter token (`JUPYTER_TOKEN`) go through the container
  environment (`docker inspect` still shows them: restricted to root and the `docker` group).
- Compute containers, Jupyter and MLflow run without root (host UID, or 10001 for MLflow);
  PostgreSQL drops root at startup (official image); MinIO (image `pgsty/minio`) runs as
  root in its container, with no port exposed outside `127.0.0.1`.
- Update: `git pull && make image image-mlflow && make up` (or `make image-gpu`).

## 11. What was tested, and how long it takes (CPU)

Measurements of 7 November 2026 on a **GPU-less** test machine (4 cores shared with other
workloads, Ubuntu 24.04, Docker 29.9, Compose 5.6, Internet access through a TLS proxy). Durations are
wall-clock times of the whole command; they give an order of magnitude, not a guarantee.

**Laptop, without Docker** (Python 3.13 venv, SQLite catalog, `file://` storage):

| Command | Duration | Result |
|---|---|---|
| `make setup` (fresh venv, pinned dependencies, torch CPU 196 MB) | 68 s | complete installation |
| `make smoke RUN=local` | 4 s | 10 steps OK (16³ simulation → validated MFF → Zarr → catalog → dataset → 1 `fm3d` iteration → evaluation → `eval_summary`) |
| `make test RUN=local` | 20 s | 61 passed, 6 skipped (PostgreSQL, S3 and E2 data absent) |
| `make sweep CONFIG=<TG 2×2 campaign, 12³>` | 4 s | 4 simulations `done`, MFF files + sha256 in the catalog |
| `make train CONFIG=infra/configs/train_fm3d.yaml TRAIN_ARGS="--set … train.iters=6 data.kmax=3"` | 5 s | dataset created from the campaign, model + quick evaluation in the catalog |
| `make eval CONFIG=infra/configs/train_fm3d.yaml MODEL=<uuid>` | 2 s | 4 points evaluated, `python -m milady.catalog summary` consistent; without `MODEL`, the latest model with the configuration's name is found |

**Full Docker stack** (PostgreSQL 16, MinIO, MLflow 3.17, CPU `worker` container):

| Command | Duration | Result |
|---|---|---|
| `make env` | < 1 s | `.env` (permissions 600, random passwords), `data/` owned by the container's UID |
| `make image MILADY_BUILD_CACERT=…` (cold) | 2 min | `milady:cpu` image of 2.3 GB (including 64 s of pip installation) |
| `make image` (new commit, unchanged dependencies) | 7 s | apt and pip layers reused |
| `make up` (images present) | 14 s | `db`, `s3`, `mlflow` healthy, `s3-init` finished (code 0) |
| `make smoke` (in an ephemeral `worker` container) | 10 s | 10 steps OK; objects in MinIO, MLflow run `FINISHED`, rows in the catalog |
| `docker compose … --profile cpu up -d worker` then `docker compose … exec worker make smoke RUN=local` | 6 s | same, from a permanent `worker` |
| `make sweep CONFIG=<reduced campaign>` | 10 s | 4 simulations in the container, files in `s3://milady-data/<campaign>/<uuid>/fields.h5` |
| `make sweep … SCHEDULER=docker SWEEP_ARGS="--force --indices 0,1"` | 9 s | one container per simulation, `docker` tasks in the catalog |
| `make train …` (same overrides) | 10 s | MLflow run (86 parameters, loss curves), checkpoints in `s3://milady-models` |
| `make eval … EVAL_ARGS="--out s3://milady-models/…/eval.json"` | 5 s | evaluations in the catalog, JSON report in S3 |
| `make test` (in the container, PostgreSQL and MinIO of the stack) | 32 s | 66 passed, 1 skipped (E2 data); since then, a 68th test (fine-tuning anchoring) has been added: outside the container, without PostgreSQL, 64 passed and 4 skipped |
| `make backup BACKUP_TARGET=/tmp/…` | 1 s | `milady-*.dump`, `mlflow-*.dump`, mirror of the 3 buckets |
| `docker compose … down -v` | 3 s | containers, network and volumes removed |

Manual checks after `make smoke`: `docker compose … exec db psql -U milady -d milady`
(tables `campaign`, `simulation`, `file`, `diagnostic`, `dataset`, `model`, `evaluation`, `job` and view
`v_eval_summary` populated; `mlflow` database present), `mc ls -r` on the three buckets (MFF files,
checkpoints, MLflow artifacts), MLflow REST API (`/api/2.0/mlflow/runs/get`: run `FINISHED`,
`loss` metric, `checkpoint.pt` artifact).

**New-user walkthrough** (clean copy of the repository, without `data/` or `.env`, as root):

| Command | Duration | Result |
|---|---|---|
| `MILADY_BUILD_CACERT=… infra/deploy/bootstrap_vm.sh --cpu` (1st run, cold image) | 3 min 03 s | 7 steps, smoke test passed, code 0 |
| same command, 2nd run (images cached) | 33 s | `.env` kept, smoke test passed |
| `bootstrap_vm.sh --cpu --no-build --no-smoke` | 4 s | idempotent |

**Slurm templates run without Slurm** (`MILADY_SIF=none`, venv, simulated `$WORK`/`$SCRATCH`,
`srun`/`scontrol` replaced by dummy scripts):

| Command | Duration | Result |
|---|---|---|
| `SLURM_ARRAY_TASK_ID=i bash infra/slurm/gen_data.sbatch <campaign>` (4 elements) | 2 s each | files in `$SCRATCH/milady/store`, SQLite catalog `$WORK/milady/catalog.sqlite` |
| `GPUS_PER_NODE=2 bash infra/slurm/train.sbatch infra/configs/train_fm3d.yaml --set …` | 6 s | `torchrun` with 2 CPU processes (gloo), SQLite MLflow `$WORK/milady/mlflow.db` |
| `bash infra/slurm/eval.sbatch infra/configs/train_fm3d.yaml --model <uuid>` | 2 s | evaluations in the cluster's catalog |
| `python -m milady.sweep infra/configs/palier2_abc3d.yaml --scheduler slurm --dry-run` | 1 s | `sbatch` script rendered (`--array=0-36%16`), nothing submitted |

**Review checks** (same day, after corrections):

| Check | Result |
|---|---|
| `make test` outside the container with a test PostgreSQL 16 | 66 passed, 1 skipped (E2 data); `schema.sql` ≡ `models.py`, `DEFAULT` included |
| 3D MFF file read back with `WellDataset`'s HDF5 accesses (the_well 1.2.0) | identical fields, `PERIODIC` boundary conditions |
| 18 corruptions of an MFF file (type, groups, shapes, NaN, masks, UUID…) | all reported by `validate` (NaN in the middle of a trajectory: `--full`) |
| Docker stack (`up`, `make smoke` in `worker`) | MLflow under UID 10001, no password in `ps`, ports on `127.0.0.1` |
| `make jupyter` | 403 without a token or with a wrong token, 200 with `JUPYTER_TOKEN` |
| `gen_data.sbatch` (dummy srun): SIGTERM during the simulation, then same index resubmitted | checkpoint written, resumed at t = 113 then ended `done` |
| Docker section of `bootstrap_vm.sh` in a disposable Ubuntu 24.04 with `docker.io` | `docker.io` removed, `docker.sources` (deb822) read by apt, `docker-ce` available |
| dependencies of the GPU image (without torch/CUDA) resolved for Python 3.12 manylinux | 95 packages, base-image torch kept |
| submission from a light login-node venv (PyYAML, NumPy, SQLAlchemy; dummy `sbatch`) | array submitted, tasks registered in the catalog |

## 12. What could not be tested here

- **GPU**: no card on the test machine. Not run: the `milady:gpu` image
  (`Dockerfile.gpu` built up to the pip step, fixed afterwards, without a full rebuild),
  the NVIDIA Container Toolkit and step 3 of `bootstrap_vm.sh`, the `worker-gpu` service, the solver
  and the training on CUDA (bf16, several GPUs, NCCL), `make train NGPUS=4`. No GPU compute time
  is therefore given; measure it first:
  `python -m milady.sim.mhd3d bench --n 64 128 256 --device cuda --steps 50`.
- **Real Slurm**: no scheduler here. `sbatch`, job arrays, multi-node `srun`,
  the `torchrun` rendezvous between nodes and requeueing after preemption have not been seen
  running. `gen_data.sbatch` launches the simulation in an `srun` step with `--signal=TERM@120`:
  SIGTERM 120 s before the limit, checkpoint, then resumption by resubmitting the index (chain
  SIGTERM → checkpoint → resumption verified here with a dummy `srun`; signal delivery by
  a real Slurm remains to be observed once on the cluster, with a short `--time`).
- **Apptainer / Singularity**: not installed here; `make sif`, `apptainer.def` and the
  `milady_run` function in container mode (`--nv`, mounts) are untested.
- **Jean Zay**: the options (`projet@h100`, `-C h100`, QoS, `idrcontmgr`, absence of Internet on
  the nodes) come from the IDRIS documentation, without execution.
- **Cloud providers**: no VM rented. Not tested: `cloud-init.yaml` (only parsed as
  YAML), `deploy_remote.sh` (rsync/SSH to a VM), a Docker installation on an Ubuntu without
  Docker (here Docker was already present: step 2 was skipped), Ubuntu 22.04, provider S3 buckets
  (AWS, Scaleway, OVHcloud: only MinIO was used) and `make backup` to `s3://…`.
- **Real size**: the `palier2_abc3d` campaigns (37 simulations at 64³) and `palier2_tg3d`
  (12 simulations at 64³) and a full training run (`train_fm3d.yaml`, 200 epochs) were not
  launched: only reduced versions were.
- **Jupyter**: `make jupyter` was checked during development (token required), not during this
  integration pass.
