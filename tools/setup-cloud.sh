#!/bin/bash
# Script d'installation de l'environnement cloud milady-2027 (Claude Code sur le web).
# À coller tel quel dans le champ « Setup script » de l'environnement.
#
# Il tourne en root sous Ubuntu 24.04, avant le démarrage de Claude Code et peut-être avant le
# clonage du dépôt : il ne lit aucun fichier du dépôt. Chaque bloc teste d'abord si l'outil
# marche déjà et n'installe que ce qui manque ; chaque bloc a un plafond de temps (timeout) pour
# que l'ensemble finisse en moins de cinq minutes. Le seul bloc qui passe par apt est le bloc
# ffmpeg + Playwright : il n'y a donc jamais deux apt en même temps.
#
# Pas de torch pour l'instant (inutile au film) : il s'installe à la demande avec
#   pip install --break-system-packages torch --index-url https://download.pytorch.org/whl/cpu
#
# Journal complet : /tmp/setup-milady.log. Seul le résumé final va sur la sortie standard.
set -u
LOG=/tmp/setup-milady.log
exec 3>&1 >>"$LOG" 2>&1   # fd 3 = sortie d'origine, pour le résumé
echo "=== setup-milady $(date -u +%FT%TZ)"
T0=$(date +%s)
export DEBIAN_FRONTEND=noninteractive
export PATH=/opt/node22/bin:/usr/local/bin:$PATH
export NODE_PATH=/opt/node22/lib/node_modules
export PLAYWRIGHT_BROWSERS_PATH=${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}
export PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore

# 1. ffmpeg (apt), puis Playwright et son Chromium. À la suite : les deux peuvent appeler apt.
#    Playwright déjà présent (cas de l'image Claude Code) : on garde sa version et on ne
#    télécharge son Chromium que s'il manque. Le réinstaller avec npm changerait de version
#    et forcerait ~330 Mo de téléchargement (cause du « exit code -1 » de l'ancien script).
(
  if ! command -v ffmpeg >/dev/null; then
    timeout 150 apt-get update -qq && timeout 150 apt-get install -y -qq ffmpeg
  fi || true
  if node -e "require('playwright')" 2>/dev/null; then
    node -e "const fs=require('fs');process.exit(fs.existsSync(require('playwright').chromium.executablePath())?0:1)" \
      || timeout 200 node "$NODE_PATH/playwright/cli.js" install chromium
  else
    timeout 100 npm install -g --silent playwright &&
      timeout 180 playwright install --with-deps chromium
  fi
  echo "bloc apt/Playwright fini à +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

# 2. Quarto 1.7.32 depuis l'archive officielle (pip install quarto-cli restait bloqué).
(
  if [ "$(quarto --version 2>/dev/null)" != "1.7.32" ]; then
    d=$(mktemp -d) &&
      timeout 180 curl -fsSL -o "$d/quarto.tgz" \
        https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.32/quarto-1.7.32-linux-amd64.tar.gz &&
      tar -xzf "$d/quarto.tgz" -C /opt &&
      ln -sf /opt/quarto-1.7.32/bin/quarto /usr/local/bin/quarto
    rm -rf "$d"
  fi
  echo "bloc Quarto fini à +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

# 3. KaTeX 0.19.0 dans /opt/katex (pour tools/check_katex.mjs).
(
  if ! NODE_PATH=/opt/katex/node_modules node -e "process.exit(require('katex').version==='0.19.0'?0:1)" 2>/dev/null; then
    timeout 120 npm install --silent --prefix /opt/katex katex@0.19.0
  fi
  echo "bloc KaTeX fini à +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

# 4. Dépendances Python de pyproject.toml (base + dev, sans torch), puis faster-whisper.
#    Liste recopiée de pyproject.toml : le dépôt n'est peut-être pas encore cloné.
#    uv (téléchargements en parallèle) : ~45 s à froid, contre ~250 s avec pip ; pip en secours.
(
  PKGS="numpy>=1.26 scipy>=1.11 h5py>=3.10 zarr>=3.0 numcodecs>=0.13 pyyaml>=6.0
    sqlalchemy>=2.0 psycopg[binary]>=3.1 fsspec>=2024.6 jsonschema>=4.20
    mlflow-skinny>=3.0 alembic>=1.13 matplotlib>=3.8 pytest>=8.0 ruff>=0.6 mypy>=1.10 faster-whisper"
  UV=$(command -v uv || echo /root/.local/bin/uv)
  [ -x "$UV" ] || { timeout 60 python3 -m pip install -q --break-system-packages uv && UV=$(command -v uv); }
  # shellcheck disable=SC2086
  timeout 180 "$UV" pip install -q --system --break-system-packages --python "$(command -v python3)" $PKGS \
    || timeout 200 python3 -m pip install -q --break-system-packages $PKGS
  echo "bloc Python fini à +$(( $(date +%s) - T0 )) s"
) </dev/null || true &

wait

{
  echo "--- versions (durée totale : $(( $(date +%s) - T0 )) s)"
  echo "ffmpeg     : $(ffmpeg -version 2>/dev/null | head -1 | cut -d' ' -f3)"
  echo "quarto     : $(quarto --version 2>/dev/null)"
  echo "playwright : $(node -e "console.log(require('playwright/package.json').version)" 2>/dev/null)"
  echo "chromium   : $(node -e "const fs=require('fs');const p=require('playwright').chromium.executablePath();console.log(fs.existsSync(p)?p:'ABSENT')" 2>/dev/null)"
  echo "katex      : $(NODE_PATH=/opt/katex/node_modules node -e "console.log(require('katex').version)" 2>/dev/null)"
  python3 -c "import numpy, scipy, h5py, zarr, sqlalchemy, mlflow, matplotlib, pytest, faster_whisper; print('python     : deps OK, faster_whisper', faster_whisper.__version__)" 2>/dev/null \
    || echo "python     : ÉCHEC d'import (voir $LOG)"
} 2>&1 | tee -a "$LOG" >&3 || true
exit 0
