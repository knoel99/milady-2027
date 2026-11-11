# MilaDy Makefile - single entry point to install, deploy and run the computations.
#
#   make help                     list of targets
#   make setup                    portable: .venv venv + pinned dependencies + pip install -e .
#   make env && make up           Docker stack (PostgreSQL, MinIO, MLflow) on any machine
#   make smoke                    end-to-end test (simulation → MFF → S3 → catalogue → training → evaluation)
#   make sweep CONFIG=infra/configs/palier2_abc3d.yaml
#   make train CONFIG=infra/configs/train_fm3d.yaml [NGPUS=4]
#   make eval  CONFIG=infra/configs/train_fm3d.yaml [MODEL=<uuid>]
#
# Two execution modes, chosen automatically (can be forced with RUN=docker or RUN=local):
#   docker: if infra/docker/.env exists - the Python commands run in the container
#           $(WORKER) (worker or worker-gpu, read from .env) linked to db, s3 and mlflow;
#   local : otherwise - .venv venv (make setup), SQLite catalogue and ./data storage (portable mode),
#           or Slurm cluster (see infra/slurm/README-slurm.md).

SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c
.DEFAULT_GOAL := help
MAKEFLAGS += --no-print-directory

ROOT       := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
COMPOSE_YML := $(ROOT)/infra/docker/docker-compose.yml
ENV_FILE   := $(ROOT)/infra/docker/.env
COMPOSE    := docker compose -f $(COMPOSE_YML) --env-file $(ENV_FILE)

PYTHON     ?= python3
VENV       ?= $(ROOT)/.venv
IMAGE      ?= milady
SIF        ?= $(ROOT)/milady.sif
CONFIG     ?=
SCHEDULER  ?= local
MODEL      ?=
EVAL_ARGS  ?=
TRAIN_ARGS ?=
SWEEP_ARGS ?=
BACKUP_TARGET ?= $(ROOT)/backups
GPU        ?= 0

# Value of a variable from infra/docker/.env (empty if absent).
env_get = $(shell [ -f $(ENV_FILE) ] && sed -n 's/^$(1)=//p' $(ENV_FILE) | tail -n 1 || true)
# Number of NVIDIA GPUs visible on the host (0 without a driver). The $(shell) calls must never fail.
GPU_COUNT = $(shell (nvidia-smi -L 2>/dev/null || true) | grep -c '^GPU' || true)

RUN    ?= $(if $(wildcard $(ENV_FILE)),docker,local)
WORKER ?= $(or $(call env_get,MILADY_WORKER),worker)
# UID/GID of the container user: those from .env (repository owner), otherwise the current user.
UID_   := $(or $(call env_get,MILADY_UID),$(shell id -u))
GID_   := $(or $(call env_get,MILADY_GID),$(shell id -g))
# Never root in the container: UID/GID 0 → 1000.
UID_   := $(if $(filter 0,$(UID_)),1000,$(UID_))
GID_   := $(if $(filter 0,$(GID_)),1000,$(GID_))
# Current commit (-dirty suffix if the tracked tree is modified): provenance of the MFF files.
GIT_COMMIT ?= $(shell c=$$(git -C $(ROOT) rev-parse --short=12 HEAD 2>/dev/null) && { git -C $(ROOT) diff --quiet HEAD -- 2>/dev/null && echo $$c || echo $$c-dirty; } || true)
export GIT_COMMIT
# Optional TLS proxy certificate for pip during `docker build` (corporate/HPC network).
MILADY_BUILD_CACERT ?=
export MILADY_BUILD_CACERT
comma := ,
BUILD_SECRET := $(if $(MILADY_BUILD_CACERT),--secret id=cacert$(comma)src=$(MILADY_BUILD_CACERT),)

ifeq ($(RUN),docker)
  PY := $(COMPOSE) run --rm $(WORKER) python
  # Tests: S3 and PostgreSQL of the stack (compose MinIO, temporary database created by the tests).
  TEST_PY := $(COMPOSE) run --rm -e MILADY_TEST_S3_ENDPOINT=http://s3:9000 -e MILADY_TEST_DOCKER=0 $(WORKER) python
  # Number of GPUs visible in the container (0 → CPU training, 1 process).
  NGPUS ?= $(if $(filter worker-gpu,$(WORKER)),$(GPU_COUNT),1)
else
  PY := $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,$(PYTHON))
  TEST_PY := $(PY)
  NGPUS ?= $(GPU_COUNT)
endif
NPROC := $(if $(filter 0,$(NGPUS)),1,$(NGPUS))

.PHONY: help setup env up down ps logs shell jupyter smoke sweep train eval backup image image-gpu \
        image-mlflow image-jupyter sif test lock clean check-config check-env

help: ## Show this help
	@echo "MilaDy - available targets (current mode: RUN=$(RUN), WORKER=$(WORKER)):"
	@grep -hE '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-11s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------------------------
# Installation
# ---------------------------------------------------------------------------------------------
setup: ## Portable/cluster: create .venv and install the pinned dependencies (GPU=1 for CUDA)
	@command -v $(PYTHON) >/dev/null || { echo "Python not found ($(PYTHON))"; exit 1; }
	@$(PYTHON) -c 'import sys; assert sys.version_info >= (3, 11), "Python >= 3.11 required"'
	@[ -x $(VENV)/bin/python ] || $(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -r $(ROOT)/infra/env/$(if $(filter 1,$(GPU)),requirements-gpu.txt,requirements.txt)
	$(VENV)/bin/python -m pip install --no-deps -e $(ROOT)
	@mkdir -p $(ROOT)/data/store
	@echo "OK. Activate: source .venv/bin/activate ; test: make smoke RUN=local"

env: ## Generate infra/docker/.env with random passwords (never overwritten if it exists)
	@$(ROOT)/infra/deploy/gen_env.sh $(if $(filter 1,$(GPU)),--gpu,)
	@# data/ is mounted in the containers, which run as MILADY_UID (never root): if the repository
	@# belongs to root (VM without a normal user), data/ must belong to that UID (like bootstrap_vm.sh).
	@if [ "$$(id -u)" = 0 ]; then install -d -o $(UID_) -g $(GID_) $(ROOT)/data; else mkdir -p $(ROOT)/data; fi

check-env:
	@[ -f $(ENV_FILE) ] || { echo "infra/docker/.env missing: run 'make env' (or bootstrap_vm.sh)"; exit 1; }

check-config:
	@[ -n "$(CONFIG)" ] || { echo "Specify CONFIG=path/to/campaign.yaml"; exit 1; }
	@[ -f "$(CONFIG)" ] || [ -f "$(ROOT)/$(CONFIG)" ] || { echo "File not found: $(CONFIG)"; exit 1; }

# ---------------------------------------------------------------------------------------------
# Docker stack
# ---------------------------------------------------------------------------------------------
up: check-env ## Start db, s3 (+ buckets), mlflow and wait for the healthchecks
	@docker image inspect milady-mlflow:3.17.2 >/dev/null 2>&1 || $(MAKE) image-mlflow
	$(COMPOSE) up -d --wait --wait-timeout 300 db s3 mlflow
	@$(COMPOSE) ps --all
	@echo "Services ready. MLflow: http://localhost:$(or $(call env_get,MLFLOW_PORT),5000) (SSH tunnel on a VM)."

down: check-env ## Stop all containers (data volumes are kept)
	$(COMPOSE) --profile cpu --profile gpu --profile jupyter down

ps: check-env ## Service status
	$(COMPOSE) --profile cpu --profile gpu --profile jupyter ps --all

logs: check-env ## Service logs (SERVICE=mlflow for a single one)
	$(COMPOSE) logs --tail=200 $(SERVICE)

shell: check-env ## Interactive shell in the compute container
	$(COMPOSE) run --rm $(WORKER) bash

jupyter: check-env ## Start JupyterLab (port 8888, JUPYTER_TOKEN token from .env)
	@docker image inspect $(IMAGE):cpu-jupyter >/dev/null 2>&1 || $(MAKE) image-jupyter
	$(COMPOSE) --profile jupyter up -d --wait jupyter
	@echo "JupyterLab : http://localhost:$(or $(call env_get,JUPYTER_PORT),8888)/lab?token=<JUPYTER_TOKEN>"

# ---------------------------------------------------------------------------------------------
# Computations
# ---------------------------------------------------------------------------------------------
smoke: ## Tiny end-to-end test (a few tens of seconds on CPU)
	$(PY) infra/deploy/smoke.py

sweep: check-config ## Simulation campaign: make sweep CONFIG=... [SCHEDULER=local|docker|slurm]
	@# local: in the compute container (docker mode) or the venv; docker: driven from the host
	@# (one container per simulation, python3 + PyYAML are enough); slurm: on the cluster login node.
	$(if $(filter docker,$(SCHEDULER)),$(PYTHON),$(PY)) -m milady.sweep $(CONFIG) --scheduler $(SCHEDULER) $(SWEEP_ARGS)

train: check-config ## Training (torchrun, NGPUS processes): make train CONFIG=... [NGPUS=n]
	$(PY) -m torch.distributed.run --standalone --nnodes=1 --nproc-per-node=$(NPROC) \
	  -m milady.train.fm3d --config $(CONFIG) $(TRAIN_ARGS)

eval: ## Model evaluation: make eval CONFIG=... [MODEL=<catalogue uuid>]
	$(PY) -m milady.eval $(if $(CONFIG),--config $(CONFIG),) $(if $(MODEL),--model $(MODEL),) $(EVAL_ARGS)

test: ## pytest tests (short ones)
	$(TEST_PY) -m pytest -q -rs -p no:cacheprovider -m "not slow" tests $(TEST_ARGS)

# ---------------------------------------------------------------------------------------------
# Images and containers
# ---------------------------------------------------------------------------------------------
image: ## Build the CPU image milady:cpu
	docker build -f $(ROOT)/infra/docker/Dockerfile -t $(IMAGE):cpu \
	  --build-arg MILADY_UID=$(UID_) --build-arg MILADY_GID=$(GID_) --build-arg GIT_COMMIT=$(GIT_COMMIT) $(BUILD_SECRET) $(ROOT)

image-gpu: ## Build the GPU image milady:gpu (CUDA 12.6)
	docker build -f $(ROOT)/infra/docker/Dockerfile.gpu -t $(IMAGE):gpu \
	  --build-arg MILADY_UID=$(UID_) --build-arg MILADY_GID=$(GID_) --build-arg GIT_COMMIT=$(GIT_COMMIT) $(BUILD_SECRET) $(ROOT)

image-jupyter: ## Build the CPU image with JupyterLab (milady:cpu-jupyter)
	docker build -f $(ROOT)/infra/docker/Dockerfile -t $(IMAGE):cpu-jupyter --build-arg WITH_JUPYTER=1 \
	  --build-arg MILADY_UID=$(UID_) --build-arg MILADY_GID=$(GID_) --build-arg GIT_COMMIT=$(GIT_COMMIT) $(BUILD_SECRET) $(ROOT)

image-mlflow: ## Build the MLflow server image (milady-mlflow:3.17.2)
	docker build -f $(ROOT)/infra/docker/Dockerfile.mlflow -t milady-mlflow:3.17.2 $(BUILD_SECRET) $(ROOT)/infra/docker

sif: ## Apptainer image milady.sif (from milady:gpu if present, otherwise apptainer.def)
	@command -v apptainer >/dev/null || { echo "apptainer not found (see infra/slurm/README-slurm.md)"; exit 1; }
	@if docker image inspect $(IMAGE):gpu >/dev/null 2>&1; then \
	  echo "Converting Docker image $(IMAGE):gpu → $(SIF)"; \
	  apptainer build --force $(SIF) docker-daemon://$(IMAGE):gpu; \
	else \
	  echo "Docker image missing: building from infra/slurm/apptainer.def"; \
	  cd $(ROOT) && apptainer build --force --fakeroot $(SIF) infra/slurm/apptainer.def; \
	fi
	@ls -lh $(SIF)

# ---------------------------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------------------------
backup: check-env ## Backup: pg_dump + S3 mirror to BACKUP_TARGET (folder or s3://...)
	MILADY_ENV_FILE=$(ENV_FILE) $(ROOT)/infra/deploy/backup.sh $(BACKUP_TARGET)

lock: ## Compute new locks in infra/env/*.lock.tmp, to copy by hand into requirements*.txt (requires uv)
	@command -v uv >/dev/null || { echo "install uv: pip install uv"; exit 1; }
	cd $(ROOT)/infra/env && uv pip compile requirements.in --universal --python-version 3.11 \
	  --default-index https://pypi.org/simple --index https://download.pytorch.org/whl/cpu \
	  --index-strategy unsafe-best-match --no-header --no-annotate -o requirements.lock.tmp
	@echo "Compare infra/env/requirements.lock.tmp with requirements.txt then copy the versions over (keep the header)."
	cd $(ROOT)/infra/env && uv pip compile requirements-gpu.in --python-version 3.12 \
	  --python-platform x86_64-manylinux_2_28 --default-index https://pypi.org/simple \
	  --index https://download.pytorch.org/whl/cu126 --index-strategy unsafe-best-match \
	  --no-header --no-annotate -o requirements-gpu.lock.tmp

clean: ## Remove caches and build files (never data/, nor the Docker volumes)
	find $(ROOT) -type d \( -name __pycache__ -o -name .pytest_cache -o -name .mypy_cache -o -name .ruff_cache \) \
	  -not -path '*/.venv/*' -prune -exec rm -rf {} +
	rm -rf $(ROOT)/build $(ROOT)/dist $(ROOT)/*.egg-info $(ROOT)/infra/env/*.lock.tmp
