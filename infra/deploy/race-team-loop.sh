#!/usr/bin/env bash
# The race loop of one team (started by systemd as race@<team>.service, user race-<team>).
# Invokes the team's harness headless again and again with race/TEAM-PROMPT.md, pushes the branch
# race/<team> after every invocation, and stops when the work is over: the file ~/STOP exists, the
# harness wrote ~/milady/research/GOAL-MET (it judged its goal met, see race/TEAM-PROMPT.md), or three
# short failures in a row (usually a spent cap or an expired login). There is no deadline.
set -u
T="$1"
cd "$HOME/milady" || exit 1
. "$HOME/venv/bin/activate"
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"
LOG="$HOME/logs/race.log"; STATE="$HOME/.race-iteration"
i=$(cat "$STATE" 2>/dev/null || echo 0); fails=0
log() { echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }
push() {
  git add -A && git commit -q -m "race $T: $1" >/dev/null 2>&1 || true
  for n in 1 2 3 4; do git push -q origin "race/$T" >> "$LOG" 2>&1 && return 0; sleep $((n * 10)); done
  log "push failed"
}
log "loop started (iteration $i)"
while :; do
  [ -f "$HOME/STOP" ] && { log "STOP file: stopping"; break; }
  [ -f research/GOAL-MET ] && { log "goal met (research/GOAL-MET): stopping"; break; }
  i=$((i + 1)); echo "$i" > "$STATE"; T0=$(date +%s)
  log "iteration $i started"
  python3 tools/race_launch.py run-main --team "$T" --prompt-file race/TEAM-PROMPT.md --iteration "$i" \
    >> "$LOG" 2>&1; rc=$?
  dt=$(( $(date +%s) - T0 ))
  if [ "$rc" -ne 0 ] && [ "$dt" -lt 300 ]; then fails=$((fails + 1)); else fails=0; fi
  log "iteration $i ended rc=$rc after $dt s"
  push "iteration $i"
  if [ "$fails" -ge 3 ]; then log "STOPPED: three short failures in a row (cap spent or login expired?)"; break; fi
  [ "$rc" -ne 0 ] && sleep 60
done
push "loop stopped"
python3 tools/runpod_job.py cleanup >> "$LOG" 2>&1 || true
