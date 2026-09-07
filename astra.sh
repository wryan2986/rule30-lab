#!/usr/bin/env bash
# astra.sh - One command. Always works.
# Accepts optional args: --hours N or --continuous
SESSION="astra"
REPO="/home/ryan/rule30-lab"
SUPERVISOR_SCRIPT="${REPO}/run_astra_supervisor.sh"
STOPFILE="${REPO}/astra-stop"

# Pass any arguments through to supervisor
SUPERVISOR_ARGS="${@}"

# ── Orphan detection: if tmux session exists but no supervisor is running,
# kill the stale session so we can start fresh. ──
cleanup_orphaned_session() {
  if tmux has-session -t "${SESSION}" 2>/dev/null; then
    local sup_pid
    sup_pid=$(pgrep -f "run_astra_supervisor.sh|run_astra_8h.sh" 2>/dev/null | head -1) || true
    if [ -z "$sup_pid" ]; then
      echo "Orphaned tmux session (no supervisor running). Cleaning up..."
      tmux kill-session -t "${SESSION}" 2>/dev/null || true
      # Also remove stale stop file from previous run
      rm -f "${STOPFILE}" 2>/dev/null || true
      return 0  # session was killed, caller should start fresh
    fi
    return 1  # session is live with a running supervisor
  fi
  # No session exists — also clean stale stop file
  rm -f "${STOPFILE}" 2>/dev/null || true
  return 0
}

# Inside tmux: switch-client (always works, no prompts)
if [ -n "$TMUX" ]; then
  if cleanup_orphaned_session; then
    # Session was killed or didn't exist — start fresh
    cd "${REPO}"
    tmux new-session -d -s "${SESSION}" -x 200 -y 50
    tmux send-keys -t "${SESSION}" "bash ${SUPERVISOR_SCRIPT} ${SUPERVISOR_ARGS}" C-m
    sleep 2
    bash "${REPO}/astra_dashboard.sh"
    tmux switch-client -t "${SESSION}:dashboard"
  else
    # Session is live with a running supervisor — just attach
    if ! tmux list-windows -t "${SESSION}" -F "#{window_name}" 2>/dev/null | grep -q "^dashboard$"; then
      bash "${REPO}/astra_dashboard.sh"
    fi
    tmux switch-client -t "${SESSION}:dashboard" 2>/dev/null || tmux switch-client -t "${SESSION}"
  fi
  exit 0
fi

# Outside tmux
if cleanup_orphaned_session; then
  # Session was killed or didn't exist — start fresh
  cd "${REPO}"
  tmux new-session -d -s "${SESSION}" -x 200 -y 50
  tmux send-keys -t "${SESSION}" "bash ${SUPERVISOR_SCRIPT} ${SUPERVISOR_ARGS}" C-m
  sleep 2
  bash "${REPO}/astra_dashboard.sh"
fi

# Create dashboard window if missing
if ! tmux list-windows -t "${SESSION}" -F "#{window_name}" 2>/dev/null | grep -q "^dashboard$"; then
  bash "${REPO}/astra_dashboard.sh"
fi

# Try to attach. If another client has it, kill that client and retry.
if ! tmux attach -t "${SESSION}" 2>/dev/null; then
  echo "Detaching stale client..."
  for c in $(tmux list-clients -t "${SESSION}" -F "#{client_name}" 2>/dev/null); do
    tmux kill-client -t "${c}" 2>/dev/null || true
  done
  sleep 0.5
  exec tmux attach -t "${SESSION}"
fi
