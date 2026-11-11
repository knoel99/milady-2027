#!/bin/bash
# User data for a Scaleway campaign VM (passed by `infra/deploy/scaleway.py campaign`).
# No SSH and no credential on the VM: it serves its status, logs and results over plain HTTP
# under a random path, http://IP:8000/__TOKEN__/, and the session that launched it reads them.
# The VM never deletes itself (that would need an API key): the launcher deletes it.
#
# Placeholders filled by scaleway.py: __TOKEN__ (random path), __REPO__, __REF__ (commit),
# __ARGS__ (run_stage.sh options), __MAX_MIN__ (CPU guard: power off after this many minutes;
# a powered-off Scaleway instance still bills its disk and IP until it is deleted).
set -u
WWW=/srv/www; OUT=$WWW/__TOKEN__; mkdir -p "$OUT"
: > "$WWW/index.html"                      # no directory listing at the root
status() { echo "$(date -u +%FT%TZ) $*" >> "$OUT/status.txt"; }
exec >> "$OUT/setup.log" 2>&1
status "boot"
shutdown -h +__MAX_MIN__ "milady CPU guard" || true
(cd "$WWW" && nohup python3 -m http.server 8000 >/dev/null 2>&1 &)
status "http server up"

export DEBIAN_FRONTEND=noninteractive
apt-get update -q && apt-get install -y -q git python3-venv python3-pip || { status "FAILED apt"; exit 1; }
status "apt done"
cd /opt && git clone -q "__REPO__" milady && cd milady && git checkout -q "__REF__" \
  || { status "FAILED clone"; exit 1; }
status "clone done at $(git rev-parse --short HEAD)"
python3 -m venv /opt/venv && . /opt/venv/bin/activate
pip install -q -r infra/env/requirements.txt && pip install -q --no-deps -e . \
  || { status "FAILED pip"; exit 1; }
status "pip done, $(nproc) vCPU"

mkdir -p experiments/results/logs
ln -sfn /opt/milady/experiments/results/logs "$OUT/logs"
T0=$(date +%s)
status "run_stage __ARGS__ started"
if experiments/run_stage.sh __ARGS__ > "$OUT/run_stage.log" 2>&1; then rc=0; else rc=$?; fi
status "run_stage finished rc=$rc in $(( $(date +%s) - T0 )) s"
tar -czf "$OUT/results.tar.gz" -C /opt/milady experiments/results site/experiments/figures \
  && status "DONE results.tar.gz ready" || status "FAILED tar"
