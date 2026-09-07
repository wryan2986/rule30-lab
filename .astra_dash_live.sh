#!/usr/bin/env bash
# .astra_dash_live.sh - Live research output from supervisor log
source "$(dirname "$0")/.astra_dash_lib.sh"

last_round=""

show_separator() {
  local rn="$1"
  local hash=$(git -C "${REPO}" log --oneline -1 2>/dev/null | cut -d" " -f1 || echo "--")
  local bar=$(printf "%0.s" $(seq 1 50) | tr " " "=" )
  echo ""
  printf "${CYN}%s${RST}\n" "$bar"
  printf "${CYN} ROUND %s \u2022 NEW ASTRA CONTEXT${RST}\n" "$rn"
  printf "${DIM} Started: %s    Base: %s${RST}\n" "$(date +%H:%M)" "$hash"
  printf "${CYN}%s${RST}\n" "$bar"
}

show_ended() {
  local rn="$1"
  local bar=$(printf "%0.s" $(seq 1 50) | tr " " "\u2500")
  echo ""
  printf "${YEL}%s${RST}\n" "$bar"
  printf "${YEL} ROUND %s COMPLETE${RST}\n" "$rn"
  printf "${YEL}%s${RST}\n" "$bar"
}

while true; do
  sup_pid=$(get_supervisor_pid)
  codex_pid=""
  codex_round=""

  if [ -n "$sup_pid" ]; then
    codex_pid=$(get_codex_child_pid "$sup_pid")
  fi

  if [ -n "$codex_pid" ]; then
    codex_round=$(get_codex_round_num "$codex_pid")
  fi

  # Fallback: get round from supervisor log if codex PID parse failed
  if [ -z "$codex_round" ] && [ -n "$sup_pid" ]; then
    codex_round=$(grep -oP "Round \K[0-9]+" "$SUPERVISOR_LOG" 2>/dev/null | tail -1) || true
    # Only use if supervisor is still alive (not from old log entries)
    [ -z "$codex_round" ] && codex_round=""
  fi

  if [ -n "$codex_round" ]; then
    # Active round
    if [ "$codex_round" != "$last_round" ]; then
      if [ -n "$last_round" ]; then
        show_ended "$last_round"
      fi
      show_separator "$codex_round"
      last_round="$codex_round"
    fi
    # Tail supervisor log from round start
    round_line=$(grep -n "Round ${codex_round} starting" "$SUPERVISOR_LOG" 2>/dev/null | tail -1 | cut -d: -f1) || true
    if [ -n "$round_line" ]; then
      tail -n +"${round_line}" "$SUPERVISOR_LOG" 2>/dev/null | tail -50
    else
      # Fallback: just tail the log
      tail -50 "$SUPERVISOR_LOG" 2>/dev/null || true
    fi
  else
    # No active round
    if [ -n "$last_round" ]; then
      show_ended "$last_round"
      last_round=""
    fi
    if [ -n "$sup_pid" ]; then
      sup_state=$(detect_state)
      case "$sup_state" in
        BETWEEN_ROUNDS)
          printf "${DIM}  \u25c9 BETWEEN ROUNDS \u2014 supervisor preparing next round${RST}\n"
          ;;
        RUNNING)
          printf "${DIM}  \u25c9 RUNNING \u2014 waiting for round output${RST}\n"
          ;;
        BLOCKED)
          printf "${RED}  \u26a0 SUPERVISOR BLOCKED${RST}\n"
          ;;
        *)
          printf "${DIM}  \u25c9 Waiting for next round\u2026${RST}\n"
          ;;
      esac
    else
      # Supervisor not running — show last 20 lines of log
      tail -20 "$SUPERVISOR_LOG" 2>/dev/null || printf "${DIM}  No supervisor log found${RST}\n"
    fi
  fi

  sleep 5
  clear
done
