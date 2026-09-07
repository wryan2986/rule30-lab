#!/usr/bin/env bash
# .astra_dash_lib.sh - Shared functions for Astra dashboard panes
# NO set -euo pipefail -- monitoring dashboards must tolerate missing data

REPO="/home/ryan/rule30-lab"
SUPERVISOR_LOG="$REPO/astra-supervisor.log"
USAGE_FILE="$HOME/.opencodex/usage.jsonl"
STOP_FILE="$REPO/astra-stop"
STATEFILE="/tmp/astra-supervisor/state"
METADATA="/tmp/astra-supervisor/metadata"
ROLLOVER_STATEFILE="/tmp/astra-supervisor/rollover_state"

RST=$'\033[0m'; BOLD=$'\033[1m'; DIM=$'\033[2m'
GRN=$'\033[1;32m'; YEL=$'\033[1;33m'; RED=$'\033[1;31m'
CYN=$'\033[1;36m'; BLU=$'\033[1;34m'; MAG=$'\033[1;35m'
WHT=$'\033[1;37m'; GRY=$'\033[0;37m'

trap 'exit 0' INT TERM

term_width() { tput cols 2>/dev/null || echo 80; }

fmt_duration() {
  local s="${1:-0}"
  s="${s//[^0-9]/}"
  [ -z "$s" ] && s=0
  if [ "$s" -ge 3600 ]; then printf "%dh%02dm" $((s/3600)) $(((s%3600)/60))
  elif [ "$s" -ge 60 ]; then printf "%dm%02ds" $((s/60)) $((s%60))
  else printf "%ds" "$s"; fi
}

fmt_tokens() {
  local t="${1:-0}"
  t="${t//[^0-9]/}"
  [ -z "$t" ] && t=0
  if [ "$t" -ge 1000000 ]; then printf "%.1fM" "$(echo "scale=1;$t/1000000"|bc 2>/dev/null)"
  elif [ "$t" -ge 1000 ]; then printf "%.1fk" "$(echo "scale=1;$t/1000"|bc 2>/dev/null)"
  else printf "%d" "$t"; fi
}

safe_num() { local v="${1:-}"; v="${v//[^0-9]/}"; [ -z "$v" ] && v=0; echo "$v"; }

model_label() {
  local m="${1:-}"
  case "$m" in
    *astra*) echo "ASTRA";;
    *muse*)  echo "MUSE";;
    *mimo*)  echo "MIMO";;
    *luna*)  echo "LUNA";;
    *omen*)  echo "OMEN";;
    *) [ -n "$m" ] && echo "${m:0:6}" || echo "\u2014";;
  esac
}

# Returns round window name or empty string. Never fails.
get_round_window() {
  local w
  w=$(tmux list-windows -t astra -F "#{window_name}" 2>/dev/null | grep -E "^r[0-9]+$" | sort -t"r" -k2 -n | tail -1) || true
  echo "$w"
}

get_round_num() { echo "${1:-}" | sed 's/^r//'; }

get_supervisor_start() {
  local line
  line=$(grep -F "Astra supervisor starting\|Astra supervisor |" "$SUPERVISOR_LOG" 2>/dev/null | tail -1) || true
  [ -z "$line" ] && echo "" && return
  echo "$line" | sed "s/.*\[\([0-9-]* [0-9:]*\)\].*/\1/"
}

get_round_start() {
  local rn="${1:-}"
  [ -z "$rn" ] && echo "" && return
  local line
  line=$(grep -F "Round $rn " "$SUPERVISOR_LOG" 2>/dev/null | tail -1) || true
  [ -z "$line" ] && echo "" && return
  echo "$line" | sed "s/.*\[\([0-9-]* [0-9:]*\)\].*/\1/"
}

ts_to_epoch() {
  local ts="${1:-}"
  [ -z "$ts" ] && { echo 0; return; }
  date -d "$ts" +%s 2>/dev/null || echo 0
}

progress_bar() {
  local pct="${1:-0}" w="${2:-20}"
  pct="${pct//[^0-9]/}"
  [ -z "$pct" ] && pct=0
  [ "$pct" -gt 100 ] && pct=100
  local filled=$(( pct * w / 100 )) empty=$(( w - filled ))
  local i bar=""
  for ((i=0; i<filled; i++)); do bar+="\u2588"; done
  for ((i=0; i<empty; i++)); do bar+="\u2591"; done
  printf "%s" "$bar"
}

trim_str() {
  local s="$1" mx="$2"
  [ "${#s}" -gt "$mx" ] && { printf "%.*s\u2026" "$((mx - 1))" "$s"; return; }
  printf "%s" "$s"
}

# ── Process-based state detection ──

get_supervisor_pid() {
  pgrep -f "run_astra_supervisor.sh|run_astra_8h.sh" 2>/dev/null | head -1 || echo ""
}

get_codex_child_pid() {
  local sup_pid="${1:-}"
  [ -z "$sup_pid" ] && echo "" && return
  local child
  child=$(pgrep -P "$sup_pid" 2>/dev/null | while read cp; do
    cmdline=$(cat /proc/$cp/cmdline 2>/dev/null | tr "\0" " ")
    echo "$cmdline" | grep -q "codex exec" && echo "$cp" && break
  done) || true
  if [ -z "$child" ]; then
    for cp in $(pgrep -P "$sup_pid" 2>/dev/null); do
      for gcp in $(pgrep -P "$cp" 2>/dev/null); do
        cmdline=$(cat /proc/$gcp/cmdline 2>/dev/null | tr "\0" " ")
        if echo "$cmdline" | grep -q "codex exec"; then
          echo "$gcp"
          return
        fi
      done
    done
  fi
  echo "$child"
}

get_codex_round_num() {
  local pid="${1:-}"
  [ -z "$pid" ] && echo "" && return
  local cmdline
  cmdline=$(cat /proc/$pid/cmdline 2>/dev/null | tr "\0" " ") || true
  echo "$cmdline" | grep -oP "round \\K[0-9]+" || echo ""
}

get_codex_start_time() {
  local pid="${1:-}"
  [ -z "$pid" ] && echo 0 && return
  local start
  start=$(stat -c %Y /proc/$pid 2>/dev/null) || echo 0
  echo "$start"
}

detect_state() {
  if [ -f "$STATEFILE" ]; then
    local file_state
    file_state=$(cat "$STATEFILE" 2>/dev/null | tr -d '\n')
    case "$file_state" in
      RUNNING|BETWEEN_ROUNDS|AUDIT|DRAINING|PAUSED|FINISHED|STOPPED)
        echo "$file_state"
        return
        ;;
    esac
  fi
  local sup_pid
  sup_pid=$(get_supervisor_pid)
  if [ -z "$sup_pid" ]; then
    if [ -f "$SUPERVISOR_LOG" ]; then
      if grep -q "DRAINING complete\|^Done\.\|DRAINING complete" "$SUPERVISOR_LOG" 2>/dev/null; then
        echo "FINISHED"
        return
      fi
      if grep -q "Stop file detected" "$SUPERVISOR_LOG" 2>/dev/null; then
        local last_action
        last_action=$(tail -5 "$SUPERVISOR_LOG" 2>/dev/null) || true
        if echo "$last_action" | grep -q "Stop file detected"; then
          echo "STOPPED"
          return
        fi
      fi
    fi
    echo "FINISHED"
    return
  fi
  local codex_pid
  codex_pid=$(get_codex_child_pid "$sup_pid")
  if [ -n "$codex_pid" ]; then
    echo "RUNNING"
  else
    if [ -f "$STOP_FILE" ]; then
      echo "BLOCKED"
    else
      echo "BETWEEN_ROUNDS"
    fi
  fi
}

get_metadata() {
  local key="${1:-}"
  [ -z "$key" ] && echo "" && return
  [ -f "$METADATA" ] || { echo ""; return; }
  grep "^${key}=" "$METADATA" 2>/dev/null | head -1 | cut -d= -f2- || echo ""
}

# ── Usage rate computation ──
# Computes total tokens (input+output) from usage.jsonl in a time window.
# $1 = provider filter (e.g. "openai" or "all")
# $2 = model filter (e.g. "gpt-6-astra" or "all")
# $3 = epoch start (seconds)
# $4 = epoch end (seconds)
usage_tokens_in_window() {
  local prov="${1:-all}" mdl="${2:-all}" t_start="${3:-0}" t_end="${4:-9999999999}"
  [ ! -f "$USAGE_FILE" ] && { echo 0; return; }
  jq -r --arg prov "$prov" --arg mdl "$mdl" --argjson ts "$t_start" --argjson te "$t_end" '
    select(.status==200)
    | select(if $prov=="all" then true else .provider==$prov end)
    | select(if $mdl=="all" then true else .model==$mdl end)
    | (.timestamp/1000|floor) as $t
    | select($t >= $ts and $t < $te)
    | ((.usage.inputTokens // 0) + (.usage.outputTokens // 0))
  ' "$USAGE_FILE" 2>/dev/null | awk '{s+=$1} END {print s+0}'
}

# Count API calls in a time window
usage_calls_in_window() {
  local prov="${1:-all}" mdl="${2:-all}" t_start="${3:-0}" t_end="${4:-9999999999}"
  [ ! -f "$USAGE_FILE" ] && { echo 0; return; }
  jq -r --arg prov "$prov" --arg mdl "$mdl" --argjson ts "$t_start" --argjson te "$t_end" '
    select(.status==200)
    | select(if $prov=="all" then true else .provider==$prov end)
    | select(if $mdl=="all" then true else .model==$mdl end)
    | (.timestamp/1000|floor) as $t
    | select($t >= $ts and $t < $te)
    | 1
  ' "$USAGE_FILE" 2>/dev/null | awk '{s+=$1} END {print s+0}'
}
