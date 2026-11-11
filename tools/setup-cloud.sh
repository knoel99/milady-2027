#!/bin/bash
# Setup script for the milady-2027 cloud environment (Claude Code on the web).
# Paste as is into the environment's "Setup script" field.
#
# It runs as root on Ubuntu 24.04, before Claude Code starts and possibly before the repository
# is cloned: it reads no file from the repository. Each block first checks whether the tool
# already works and only installs what is missing; each block has a time cap (timeout) so that
# the whole script finishes in under five minutes: every command stops at the latest at the
# shared deadline T0 + 280 s (function t). The only block that uses apt is the
# ffmpeg + Playwright block, so two apt processes never run at the same time.
#
# torch in its CPU build (index https://download.pytorch.org/whl/cpu), installed before the other
# Python packages: tests/test_mhd3d.py and tests/test_train.py import it, and without it make test fails.
# Cold timings with uv: torch ~25 s, the rest ~56 s.
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
export PLAYWRIGHT_BROWSERS_PATH=${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}
export PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore

# 1. ffmpeg (apt), then Playwright and its Chromium. In sequence: both may call apt.
#    Playwright already present (the Claude Code image case): keep its version and only
#    download its Chromium if it is missing. Reinstalling it with npm would change the version
#    and force a ~330 MB download (cause of the "exit code -1" of the old script).
(
  if ! command -v ffmpeg >/dev/null; then
    t 150 apt-get update -qq && t 150 apt-get install -y -qq ffmpeg
  fi || true
  if node -e "require('playwright')" 2>/dev/null; then
    node -e "const fs=require('fs');process.exit(fs.existsSync(require('playwright').chromium.executablePath())?0:1)" \
      || t 200 node "$NODE_PATH/playwright/cli.js" install chromium
  else
    t 100 npm install -g --silent playwright &&
      t 180 playwright install --with-deps chromium
  fi
  echo "apt/Playwright block finished at +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

# 2. Quarto 1.7.32 from the official archive (pip install quarto-cli used to hang).
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

# 3. KaTeX 0.19.0 in /opt/katex (for tools/check_katex.mjs).
(
  if ! NODE_PATH=/opt/katex/node_modules node -e "process.exit(require('katex').version==='0.19.0'?0:1)" 2>/dev/null; then
    t 120 npm install --silent --prefix /opt/katex katex@0.19.0
  fi
  echo "KaTeX block finished at +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

# 4. Python: CPU torch first, then the dependencies of pyproject.toml (base + dev) and
#    faster-whisper. List copied from pyproject.toml: the repository may not be cloned yet.
#    uv (parallel downloads): ~80 s cold overall, versus ~250 s without torch using pip;
#    pip remains the fallback for each step.
(
  PY=$(command -v python3)
  TORCH_INDEX=https://download.pytorch.org/whl/cpu
  PKGS="numpy>=1.26 scipy>=1.11 h5py>=3.10 zarr>=3.0 numcodecs>=0.13 pyyaml>=6.0
    sqlalchemy>=2.0 psycopg[binary]>=3.1 fsspec>=2024.6 jsonschema>=4.20
    mlflow-skinny>=3.0 alembic>=1.13 matplotlib>=3.8 pytest>=8.0 ruff>=0.6 mypy>=1.10 faster-whisper"
  UV=$(command -v uv || echo /root/.local/bin/uv)
  [ -x "$UV" ] || { t 60 python3 -m pip install -q --break-system-packages uv && UV=$(command -v uv); }
  t 150 "$UV" pip install -q --system --break-system-packages --python "$PY" "torch>=2.4" --index-url "$TORCH_INDEX" \
    || t 200 python3 -m pip install -q --break-system-packages "torch>=2.4" --index-url "$TORCH_INDEX"
  # shellcheck disable=SC2086
  t 180 "$UV" pip install -q --system --break-system-packages --python "$PY" $PKGS \
    || t 200 python3 -m pip install -q --break-system-packages $PKGS
  echo "Python block finished at +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

wait

{
  echo "--- versions"
  echo "ffmpeg     : $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f3)"
  echo "quarto     : $(quarto --version 2>/dev/null)"
  echo "playwright : $(node -e "console.log(require('playwright/package.json').version)" 2>/dev/null)"
  echo "chromium   : $(node -e "const fs=require('fs');const p=require('playwright').chromium.executablePath();console.log(fs.existsSync(p)?p:'ABSENT')" 2>/dev/null)"
  echo "katex      : $(NODE_PATH=/opt/katex/node_modules node -e "console.log(require('katex').version)" 2>/dev/null)"
  python3 -c "import torch, numpy, scipy, h5py, zarr, sqlalchemy, mlflow, matplotlib, pytest, faster_whisper; print('python     : deps OK, torch', torch.__version__, '| faster_whisper', faster_whisper.__version__)" 2>/dev/null \
    || echo "python     : import FAILED (see $LOG)"
  echo "--- total duration: $(( $(date +%s) - T0 )) s"
} 2>&1 | tee -a "$LOG" >&3 || true
exit 0
