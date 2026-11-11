# syntax=docker/dockerfile:1.7
# CPU image of the MilaDy project (portable, VM without GPU, continuous integration).
#
# Build (from the repository root):
#   docker build -f infra/docker/Dockerfile -t milady:cpu .
#   or: make image
#
# Options:
#   --build-arg MILADY_UID=$(id -u) --build-arg MILADY_GID=$(id -g)
#       aligns the container user with the host user (files written
#       in the repository mounted as a volume);
#   --build-arg WITH_JUPYTER=1      adds JupyterLab ("jupyter" service of the compose);
#   --build-arg GIT_COMMIT=$(git rev-parse --short=12 HEAD)
#       bakes the commit into the image (provenance of the MFF files, no .git in the image);
#   --secret id=cacert,src=/path/ca.pem
#       certificate of a corporate/HPC TLS proxy for pip (optional).

FROM python:3.12.15-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    MILADY_ROOT=/opt/milady \
    MPLBACKEND=Agg

# Minimal system tools: git (provenance), make (Makefile targets), curl (checks),
# PostgreSQL client (psql/pg_dump to administer the catalogue from the worker).
RUN apt-get update \
 && apt-get install -y --no-install-recommends git make curl ca-certificates postgresql-client tini \
 && rm -rf /var/lib/apt/lists/*

# ARGs are declared as close as possible to where they are used: a different value only invalidates
# the build cache from this line onwards (apt and pip stay cached).
ARG MILADY_UID=1000
ARG MILADY_GID=1000

# Non-root user, aligned with the host UID/GID. Robust to IDs already taken in
# the base image (e.g. GID 20 on Macs, UID 1000 "ubuntu"): the group is reused, the
# existing user is renamed.
RUN set -eu; \
    [ "${MILADY_UID}" != "0" ] || { echo "MILADY_UID=0 refused: the container runs without root" >&2; exit 1; }; \
    getent group "${MILADY_GID}" >/dev/null || groupadd --gid "${MILADY_GID}" milady; \
    if getent passwd "${MILADY_UID}" >/dev/null; then \
        usermod -l milady -d /home/milady -m -g "${MILADY_GID}" "$(getent passwd "${MILADY_UID}" | cut -d: -f1)"; \
    else \
        useradd --uid "${MILADY_UID}" --gid "${MILADY_GID}" --create-home --shell /bin/bash milady; \
    fi

WORKDIR /opt/milady

# 1) Pinned dependencies first (layer cached as long as the lock does not change).
COPY infra/env/requirements.txt /tmp/requirements.txt
ARG WITH_JUPYTER=0
RUN --mount=type=secret,id=cacert,required=false \
    if [ -s /run/secrets/cacert ]; then export PIP_CERT=/run/secrets/cacert; fi \
 && pip install -r /tmp/requirements.txt \
 && if [ "${WITH_JUPYTER}" = "1" ]; then pip install "jupyterlab==4.6.4"; fi

# 2) Project code, installed in editable mode: a repository mounted on /opt/milady
#    (docker-compose) replaces the code without rebuilding the image.
# Provenance: declared AFTER the dependencies, otherwise every new commit would reinstall torch.
ARG GIT_COMMIT=""
ENV MILADY_GIT_COMMIT=${GIT_COMMIT}
COPY --chown=${MILADY_UID}:${MILADY_GID} . /opt/milady
RUN --mount=type=secret,id=cacert,required=false \
    if [ -s /run/secrets/cacert ]; then export PIP_CERT=/run/secrets/cacert; fi \
 && pip install --no-deps -e . \
 && mkdir -p /opt/milady/data \
 && chown -R "${MILADY_UID}:${MILADY_GID}" /opt/milady \
 && python -c "import milady, numpy, h5py, torch; print('milady', milady.__version__, 'torch', torch.__version__)"

USER milady

# tini: forwards signals (clean shutdown of the simulations) and reaps zombies.
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "-c", "import milady; print('MilaDy image ready (CPU). Example: make smoke')"]
