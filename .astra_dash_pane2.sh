#!/usr/bin/env bash
# Pane 2: Git / Research State
while true; do
  cd /home/ryan/rule30-lab
  printf "\033[1m=== GIT / RESEARCH STATE ===\033[0m\n"
  printf "Branch: %s\n" "$(git branch --show-current 2>/dev/null)"
  printf "Commit: %s\n" "$(git log --oneline -1 2>/dev/null)"
  printf "Ahead: %s  Behind: %s\n" "$(git rev-list --count @{u}..HEAD 2>/dev/null || echo ?)" "$(git rev-list --count HEAD..@{u} 2>/dev/null || echo ?)"
  printf "Dirty: %s tracked\n" "$(git status --porcelain 2>/dev/null | grep -v "^??" | wc -l)"
  printf "Handoff: %s\n" "$(stat -c %y ASTRA_HANDOFF.md 2>/dev/null | cut -d. -f1 || echo ?)"
  lp=$(grep -F "push" /home/ryan/rule30-lab/astra-supervisor.log 2>/dev/null | grep -v "failed" | tail -1 | grep -oP "^\[\K[^\]]+" || echo "none")
  printf "Last push: %s\n" "${lp}"
  sleep 8
  clear
done