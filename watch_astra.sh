#!/usr/bin/env bash
# ============================================================================
# watch_astra.sh — Attach to the live Astra tmux session
# ============================================================================
#
# Usage:
#   ./watch_astra.sh              # attach (Ctrl-b d to detach)
#   ./watch_astra.sh list         # list all round windows
#   ./watch_astra.sh log          # tail the supervisor log
#   ./watch_astra.sh state        # show current supervisor state
#   ./watch_astra.sh round N      # attach and switch to round N window
#
# ============================================================================

set -euo pipefail

SESSION="astra"
REPO="/home/ryan/rule30-lab"
STATEFILE="/tmp/astra-supervisor/state"

case "${1:-attach}" in
  list)
    if tmux has-session -t "${SESSION}" 2>/dev/null; then
      echo "Active windows in '${SESSION}':"
      tmux list-windows -t "${SESSION}" -F "  #{window_index}: #{window_name} #{window_flags}"
    else
      echo "No tmux session '${SESSION}' running."
    fi
    ;;
  log)
    tail -f "${REPO}/astra-supervisor.log"
    ;;
  state)
    if [ -f "${STATEFILE}" ]; then
      echo "Supervisor state: $(cat "${STATEFILE}")"
    else
      echo "No state file found. Supervisor may not be running."
    fi
    echo ""
    # Show recent log lines
    tail -5 "${REPO}/astra-supervisor.log" 2>/dev/null || echo "No log found."
    ;;
  round)
    N="${2:?Usage: $0 round <number>}"
    if tmux has-session -t "${SESSION}" 2>/dev/null; then
      tmux select-window -t "${SESSION}:r${N}" 2>/dev/null && \
        tmux attach -t "${SESSION}" || \
        echo "Window r${N} not found. Available:"
      tmux list-windows -t "${SESSION}" -F "  #{window_index}: #{window_name}"
    else
      echo "No tmux session '${SESSION}' running."
    fi
    ;;
  attach|*)
    if tmux has-session -t "${SESSION}" 2>/dev/null; then
      exec tmux attach -t "${SESSION}"
    else
      echo "No tmux session '${SESSION}' running."
      echo "Start it with: ./astra.sh [--hours N | --continuous]"
      exit 1
    fi
    ;;
esac
