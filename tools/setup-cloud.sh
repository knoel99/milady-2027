#!/bin/bash
# Setup script for the milady-2027 cloud environment (Claude Code on the web).
# Paste as is into the environment's "Setup script" field.
#
# It runs as root on Ubuntu 24.04 each time a container is built, after the repository is cloned
# and before Claude Code starts, from the directory that holds the checkout. Each block first
# checks whether the tool already works and only installs what is missing; each block has a time
# cap (timeout) so that the whole script finishes in under five minutes: every command stops at
# the latest at the shared deadline T0 + 280 s (function t). No block uses apt.
#
# Python packages come from the pinned lock infra/env/requirements.txt (CPU torch included), as
# `make setup` and the tests workflow do, then the package is installed in editable mode: the
# tests that start subprocesses (`python -m milady.…`) need it. If the checkout is not there, the
# lower bounds of pyproject.toml are used instead. Measured with uv: about 15 s for the lock.
#
# Full log: /tmp/setup-milady.log. Only the final summary goes to standard output.
set -u
LOG=/tmp/setup-milady.log
exec 3>&1 >>"$LOG" 2>&1   # fd 3 = original output, for the summary
echo "=== setup-milady $(date -u +%FT%TZ)"
T0=$(date +%s)
DEADLINE=$(( T0 + 280 ))
# t N command...: like "timeout N", but never beyond the shared deadline.
t() {
  local n=$1 left=$(( DEADLINE - $(date +%s) )); shift
  [ "$left" -lt "$n" ] && n=$left
  [ "$n" -ge 1 ] || return 124
  timeout "$n" "$@"
}
export DEBIAN_FRONTEND=noninteractive
export PATH=/opt/node22/bin:/usr/local/bin:$PATH
export NODE_PATH=/opt/node22/lib/node_modules
export PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore

# 1. Quarto 1.7.32 from the official archive (pip install quarto-cli used to hang).
(
  if [ "$(quarto --version 2>/dev/null)" != "1.7.32" ]; then
    d=$(mktemp -d) &&
      t 180 curl -fsSL -o "$d/quarto.tgz" \
        https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.32/quarto-1.7.32-linux-amd64.tar.gz &&
      tar -xzf "$d/quarto.tgz" -C /opt &&
      ln -sf /opt/quarto-1.7.32/bin/quarto /usr/local/bin/quarto
    rm -rf "$d"
  fi
  echo "Quarto block finished at +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

# 2. KaTeX 0.19.0 in /opt/katex (for tools/check_katex.mjs).
(
  if ! NODE_PATH=/opt/katex/node_modules node -e "process.exit(require('katex').version==='0.19.0'?0:1)" 2>/dev/null; then
    t 120 npm install --silent --prefix /opt/katex katex@0.19.0
  fi
  echo "KaTeX block finished at +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

# 3. Python: the pinned lock when the checkout is present, otherwise the lower bounds of
#    pyproject.toml (CPU torch first). pytest and ruff at the versions of the tests workflow.
#    uv (parallel downloads); pip remains the fallback for each step.
(
  PY=$(command -v python3)
  REPO=milady-2027
  DEV="pytest==9.2.0 ruff==0.17.4"
  UV=$(command -v uv || echo /root/.local/bin/uv)
  [ -x "$UV" ] || { t 60 python3 -m pip install -q --break-system-packages uv && UV=$(command -v uv); }
  uvpip() { t "$1" "$UV" pip install -q --system --break-system-packages --python "$PY" "${@:2}"; }
  if [ -f "$REPO/infra/env/requirements.txt" ]; then
    uvpip 200 --index-strategy unsafe-best-match -r "$REPO/infra/env/requirements.txt" \
      || t 250 python3 -m pip install -q --break-system-packages -r "$REPO/infra/env/requirements.txt"
    uvpip 60 --no-deps -e "$REPO" \
      || t 60 python3 -m pip install -q --break-system-packages --no-deps -e "$REPO"
  else
    TORCH_INDEX=https://download.pytorch.org/whl/cpu
    PKGS="numpy>=1.26 scipy>=1.11 h5py>=3.10 zarr>=3.0 numcodecs>=0.13 pyyaml>=6.0
      sqlalchemy>=2.0 psycopg[binary]>=3.1 fsspec>=2024.6 jsonschema>=4.20
      mlflow-skinny>=3.0 alembic>=1.13 matplotlib>=3.8"
    uvpip 150 "torch>=2.4" --index-url "$TORCH_INDEX" \
      || t 200 python3 -m pip install -q --break-system-packages "torch>=2.4" --index-url "$TORCH_INDEX"
    # shellcheck disable=SC2086
    uvpip 180 $PKGS || t 200 python3 -m pip install -q --break-system-packages $PKGS
  fi
  # shellcheck disable=SC2086
  uvpip 60 $DEV || t 60 python3 -m pip install -q --break-system-packages $DEV
  echo "Python block finished at +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

wait

{
  echo "--- versions"
  echo "quarto     : $(quarto --version 2>/dev/null)"
  echo "katex      : $(NODE_PATH=/opt/katex/node_modules node -e "console.log(require('katex').version)" 2>/dev/null)"
  python3 -c "import torch, numpy, scipy, h5py, zarr, sqlalchemy, mlflow, matplotlib, pytest; print('python     : deps OK, torch', torch.__version__, '| numpy', numpy.__version__)" 2>/dev/null \
    || echo "python     : import FAILED (see $LOG)"
  python3 -c "import milady; print('milady     :', milady.__version__, 'root', milady.project_root())" 2>/dev/null \
    || echo "milady     : not installed (checkout absent)"
  echo "--- total duration: $(( $(date +%s) - T0 )) s"
} 2>&1 | tee -a "$LOG" >&3 || true
exit 0
