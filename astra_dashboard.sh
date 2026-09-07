#!/usr/bin/env bash
# astra_dashboard.sh - Polished two-pane Astra monitoring dashboard
# Windows: dashboard, live, usage, git, errors
# Ctrl-b 0-4 to switch; Ctrl-b d to detach
set -euo pipefail
SESSION="astra"
REPO="/home/ryan/rule30-lab"
DASHWIN="dashboard"

if ! tmux has-session -t "${SESSION}" 2>/dev/null; then
  echo "No tmux session. Start supervisor first."
  exit 1
fi

# Kill old dashboard window
tmux kill-window -t "${SESSION}:${DASHWIN}" 2>/dev/null || true

# Create dashboard window
tmux new-window -t "${SESSION}" -n "${DASHWIN}"
tmux set-option -t "${SESSION}:${DASHWIN}" history-limit 50000 2>/dev/null || true

# Split into 2 panes: top ~72% live, bottom ~28% status
tmux split-window -t "${SESSION}:${DASHWIN}" -v -p 28

# Get pane IDs
pids=$(tmux list-panes -t "${SESSION}:${DASHWIN}" -F "#{pane_id}")
p_live=$(echo "${pids}" | sed -n "1p")
p_stat=$(echo "${pids}" | sed -n "2p")

# Launch pane scripts
tmux send-keys -t "${SESSION}:${DASHWIN}.${p_live}" "bash ${REPO}/.astra_dash_live.sh" C-m
tmux send-keys -t "${SESSION}:${DASHWIN}.${p_stat}" "bash ${REPO}/.astra_dash_status.sh" C-m

# Create extra windows
tmux new-window -t "${SESSION}" -n "live"
tmux send-keys -t "${SESSION}:live" "bash ${REPO}/.astra_dash_live_fullscreen.sh" C-m

tmux new-window -t "${SESSION}" -n "usage"
tmux send-keys -t "${SESSION}:usage" "bash ${REPO}/.astra_dash_usage.sh" C-m

tmux new-window -t "${SESSION}" -n "git"
tmux send-keys -t "${SESSION}:git" "bash ${REPO}/.astra_dash_git.sh" C-m

tmux new-window -t "${SESSION}" -n "errors"
tmux send-keys -t "${SESSION}:errors" "bash ${REPO}/.astra_dash_errors.sh" C-m

# Go to dashboard
tmux select-window -t "${SESSION}:${DASHWIN}"
tmux select-pane -t "${SESSION}:${DASHWIN}.${p_live}"

echo "Dashboard ready."
echo "  tmux attach -t astra"
echo "  Ctrl-b 0=dashboard 1=live 2=usage 3=git 4=errors"
