#!/usr/bin/env bash
# Prepare one Scaleway VM (Ubuntu 24.04) for several race teams: one Linux user, one clone of the
# repository, one branch race/<team>, one Python environment, one harness and one systemd service
# per team. Run as root, from a clone of the repository on the VM; idempotent (rerun after a change).
#
#   sudo TEAMS="openai google mistral" bash infra/deploy/race-host.sh   # default: every team but claude, xai
#
# Before: /etc/race/secrets.env (root, mode 600), one KEY=value per line: the provider keys named in
# race/config.toml [teams] (OPENAI_API_KEY, GEMINI_API_KEY, ...), RUNPOD_API_KEY, GITHUB_TOKEN (a
# fine-grained token with contents read/write on the repository only), optionally <TEAM>_GPU_BUDGET_USD.
# After: log in to the harnesses that use a subscription (infra/deploy/racectl login <team>), check
# (racectl check <team>), start (racectl start <team>). Runbook: race/HOST.md.
#
# Why separate clones and users rather than git worktrees of one clone: worktrees share one .git
# directory, so every team could read, and rewrite, the branches and objects of the others, and the
# brief says a team cannot see the other teams. A clone per Linux user (home mode 700, /proc mounted
# with hidepid) keeps each team's files, harness credentials and processes to itself.
set -euo pipefail
[ "$(id -u)" -eq 0 ] || { echo "run as root"; exit 1; }
SRC="$(cd "$(dirname "$0")/../.." && pwd)"
REPO="${REPO:-https://github.com/knoel99/milady-2027.git}"
REF="${REF:-main}"
SECRETS=/etc/race/secrets.env
[ -f "$SECRETS" ] || { echo "missing $SECRETS (see the header of this script)"; exit 1; }
chmod 600 "$SECRETS"
TEAMS="${TEAMS:-$(python3 "$SRC/tools/race_host.py" teams | tr ' ' '\n' | grep -vxE 'claude|xai' | tr '\n' ' ')}"
CPU_QUOTA="${CPU_QUOTA:-400%}"     # per team: 4 cores of the host
MEM_MAX="${MEM_MAX:-12G}"           # per team

echo "== base packages, Node.js 22, uv"
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q git curl ca-certificates jq build-essential python3 python3-venv python3-pip
if ! node --version 2>/dev/null | grep -q '^v2[2-9]'; then
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y -q nodejs
fi
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
# Chromium for the figure skills (schematic-figure, archify): Playwright's, shared read-only.
if [ ! -d /opt/pw-browsers ]; then
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers npx -y playwright@1.49.1 install --with-deps chromium
  chmod -R a+rX /opt/pw-browsers
fi

echo "== Quarto 1.7.32 for the report (HTML and LaTeX PDF; TinyTeX per team below)"
if [ "$(quarto --version 2>/dev/null)" != "1.7.32" ]; then
  d=$(mktemp -d)
  curl -fsSL -o "$d/q.tgz" https://github.com/quarto-dev/quarto-cli/releases/download/v1.7.32/quarto-1.7.32-linux-amd64.tar.gz
  tar -xzf "$d/q.tgz" -C /opt && ln -sf /opt/quarto-1.7.32/bin/quarto /usr/local/bin/quarto; rm -rf "$d"
fi
apt-get install -y -q poppler-utils

echo "== the published site of the project is closed to the teams (race/BRIEF.md)"
for h in knoel99.github.io; do grep -q " $h$" /etc/hosts || echo "0.0.0.0 $h" >> /etc/hosts; done

echo "== processes of one team invisible to the others"
grep -q 'hidepid' /etc/fstab || echo 'proc /proc proc defaults,hidepid=invisible 0 0' >> /etc/fstab
mount -o remount,hidepid=invisible /proc || true

install -d -m 755 /opt/race
install -m 755 "$SRC/infra/deploy/race-team-loop.sh" /opt/race/race-team-loop.sh
install -m 755 "$SRC/infra/deploy/racectl" /usr/local/bin/racectl
cat > /etc/systemd/system/race@.service <<EOF
[Unit]
Description=MilaDy race team %i
After=network-online.target
Wants=network-online.target

[Service]
User=race-%i
EnvironmentFile=/etc/race/%i.env
Environment=PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
WorkingDirectory=/home/race-%i/milady
ExecStart=/opt/race/race-team-loop.sh %i
Restart=on-failure
RestartSec=120
CPUQuota=$CPU_QUOTA
MemoryMax=$MEM_MAX

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload

for T in $TEAMS; do
  echo "== team $T"
  U="race-$T"; H="/home/$U"
  id "$U" >/dev/null 2>&1 || useradd -m -s /bin/bash "$U"
  chmod 700 "$H"
  python3 "$SRC/tools/race_host.py" env --team "$T" --secrets "$SECRETS" > "/etc/race/$T.env" \
    || echo "  WARNING: /etc/race/$T.env lacks a key (first line of the file)"
  chown "root:$U" "/etc/race/$T.env"; chmod 640 "/etc/race/$T.env"
  SETUP="$(python3 "$SRC/tools/race_host.py" setup --team "$T")"
  sudo -iu "$U" env REPO="$REPO" REF="$REF" T="$T" SETUP="$SETUP" ENVF="/etc/race/$T.env" bash -s <<'EOS'
set -euo pipefail
set -a; . "$ENVF"; set +a
mkdir -p ~/.npm-global ~/logs && npm config set prefix ~/.npm-global
REPO="${RACE_REPO:-$REPO}"   # the team's own repository (tools/race_snapshot.py), when the secrets name one
if [ ! -d ~/milady/.git ]; then git clone -q "$REPO" ~/milady; fi
cd ~/milady
git fetch -q origin
if git rev-parse -q --verify "origin/race/$T" >/dev/null; then git checkout -q -B "race/$T" "origin/race/$T"
elif ! git rev-parse -q --verify "race/$T" >/dev/null; then git checkout -q -b "race/$T" "origin/$REF"; fi
git config user.name "race-$T"; git config user.email "race-$T@users.noreply.github.com"
git config credential.helper store
[ -n "${GITHUB_TOKEN:-}" ] && printf 'https://x-access-token:%s@github.com\n' "$GITHUB_TOKEN" > ~/.git-credentials \
  && chmod 600 ~/.git-credentials
# One prefix of pods and one objectives file per team (tools/runpod_job.py reads the prefix).
mkdir -p "race/teams/$T"
[ -d ~/venv ] || uv venv -q ~/venv
. ~/venv/bin/activate
uv pip install -q -r infra/env/requirements.txt && uv pip install -q --no-deps -e .
echo "  harness: $SETUP"
bash -c "$SETUP" || echo "  WARNING: harness setup of $T failed or needs a login (racectl login $T)"
bash tools/install_skills.sh >/dev/null 2>&1 || echo "  WARNING: figure skills not installed"
[ -x ~/.TinyTeX/bin/x86_64-linux/pdflatex ] || quarto install tinytex --no-prompt >/dev/null 2>&1 || echo "  WARNING: TinyTeX not installed (no PDF report)"
echo "  ready: $(git rev-parse --abbrev-ref HEAD) at $(git rev-parse --short HEAD)"
EOS
done
echo "== done. Next: racectl login <team> (subscriptions), racectl check <team>, racectl start <team>"
