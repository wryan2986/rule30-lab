#!/usr/bin/env bash
# astra_monitor.sh - Lightweight continuous monitoring for Astra supervisor
set +e  # monitoring script must tolerate errors
# Note: check_cycle returns non-zero on alert, caught by || true

REPO="/home/ryan/rule30-lab"
LOGFILE="${REPO}/astra-supervisor.log"
USAGE_FILE="$HOME/.opencodex/usage.jsonl"
MONITOR_LOG="${REPO}/astra-monitor.log"

ts() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[$(ts)] $*" >> "${MONITOR_LOG}"; }
alert() { echo "[$(ts)] ALERT: $*" >> "${MONITOR_LOG}"; echo "[$(ts)] ALERT: $*" >> /tmp/astra-monitor-alerts; }

get_astra_tokens() {
  [ -f "$USAGE_FILE" ] || { echo 0; return; }
  grep 'gpt-6-astra' "$USAGE_FILE" 2>/dev/null \
    | jq -r 'select(.provider=="openai" and (.model=="gpt-6-astra" or .resolvedModel=="gpt-6-astra") and .status==200) | .usage.inputTokens // 0' 2>/dev/null \
    | grep -v '^null$' | tail -1 || echo 0
}

check_cycle() {
  local issues=0
  local sup_pid
  sup_pid=$(pgrep -f 'run_astra_supervisor.sh' 2>/dev/null | head -1)
  if [ -z "$sup_pid" ]; then
    alert "Supervisor not running!"
    return 1
  fi
  local codex_pid
  codex_pid=$(pgrep -f 'codex exec.*gpt-6-astra' 2>/dev/null | head -1)
  local ctx
  ctx=$(get_astra_tokens)
  local ctx_k=$(( ctx / 1000 ))
  if [ "$ctx" -gt 150000 ]; then
    alert "Astra context very high: ${ctx_k}k"
    issues=$((issues + 1))
  elif [ "$ctx" -gt 120000 ]; then
    alert "Astra context past threshold: ${ctx_k}k"
    issues=$((issues + 1))
  fi
  local roll_state
  roll_state=$(cat /tmp/astra-supervisor/rollover_state 2>/dev/null || echo "NORMAL")
  if [ "$roll_state" != "NORMAL" ]; then
    alert "Rollover state: ${roll_state}"
    issues=$((issues + 1))
  fi
  cd "$REPO"
  if [ -d .git/MERGE_HEAD ] || [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
    alert "Git in unsafe state"
    issues=$((issues + 1))
  fi
  if [ -f "$LOGFILE" ]; then
    local log_age
    log_age=$(( $(date +%s) - $(stat -c %Y "$LOGFILE" 2>/dev/null || echo 0) ))
    if [ "$log_age" -gt 600 ]; then
      alert "Supervisor log stale: ${log_age}s"
      issues=$((issues + 1))
    fi
  fi
  if [ "$issues" -eq 0 ]; then
    log "OK: sup=${sup_pid} ctx=${ctx_k}k round=${codex_pid:+active} state=${roll_state}"
  else
    log "ISSUES=${issues}: sup=${sup_pid} ctx=${ctx_k}k round=${codex_pid:+active} state=${roll_state}"
  fi
}

log "=== Monitor started ==="
while true; do
  check_cycle || true
  sleep 300
done
