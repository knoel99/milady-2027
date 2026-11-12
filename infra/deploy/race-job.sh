#!/bin/bash
# User data for a compute-broker job VM (passed by tools/compute_broker.py).
# Like scaleway-campaign.sh, the VM holds no credential: it downloads the team's code archive
# from the broker, runs one command, and serves its status and outputs over plain HTTP under a
# random path, http://IP:8000/__TOKEN__/, where the broker collects them before deleting the VM.
#
# Placeholders filled by the broker: __TOKEN__, __ARCHIVE_URL__, __COMMAND__ (base64),
# __OUTPUTS__ (space-separated paths to pack), __MAX_MIN__ (guard).
set -u
WWW=/srv/www; OUT=$WWW/__TOKEN__; mkdir -p "$OUT"
: > "$WWW/index.html"
status() { echo "$(date -u +%FT%TZ) $*" >> "$OUT/status.txt"; }
exec >> "$OUT/setup.log" 2>&1
status "boot"
pack() { (cd /opt/milady && tar -czf "$OUT/results.tar.gz" --ignore-failed-read __OUTPUTS__); }
( sleep $(( __MAX_MIN__ * 60 )); status "GUARD timeout after __MAX_MIN__ min: stopping the job"
  pkill -f job.sh; pack; status "FAILED guard timeout, partial results.tar.gz ready"
  sleep 1800; poweroff ) &
(cd "$WWW" && nohup python3 -m http.server 8000 >/dev/null 2>&1 &)
status "http server up"

export DEBIAN_FRONTEND=noninteractive
apt-get update -q && apt-get install -y -q python3-venv python3-pip curl || { status "FAILED apt"; exit 1; }
mkdir -p /opt/milady && cd /opt/milady
curl -fsS "__ARCHIVE_URL__" | tar -x || { status "FAILED archive download"; exit 1; }
status "archive extracted"
python3 -m venv /opt/venv && . /opt/venv/bin/activate
pip install -q -r infra/env/requirements.txt && pip install -q --no-deps -e . \
  || { status "FAILED pip"; exit 1; }
status "pip done, $(nproc) vCPU"

echo "__COMMAND__" | base64 -d > /opt/job.sh
T0=$(date +%s)
status "job started"
if bash /opt/job.sh > "$OUT/job.log" 2>&1; then rc=0; else rc=$?; fi
status "job finished rc=$rc in $(( $(date +%s) - T0 )) s"
pack && status "DONE rc=$rc results.tar.gz ready" || status "FAILED tar"
