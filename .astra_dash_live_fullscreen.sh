#!/usr/bin/env bash
# .astra_dash_live_fullscreen.sh - Full-screen raw research stream
source "$(dirname "$0")/.astra_dash_lib.sh"

last_round=""

while true; do
  w=$(get_round_window)
  if [ -n "$w" ]; then
    rn=$(get_round_num "$w")
    if [ "$w" != "$last_round" ]; then
      if [ -n "$last_round" ]; then
        printf "\n${YEL}====== ROUND %s ENDED ======${RST}\n\n" "$(get_round_num "$last_round")"
      fi
      hash=$(git -C "${REPO}" log --oneline -1 2>/dev/null | cut -d" " -f1 || echo "--")
      printf "${CYN}====== ROUND %s \u2022 %s ======${RST}\n" "$rn" "$(date +%H:%M)"
      printf "${DIM}Base: %s${RST}\n\n" "$hash"
      last_round="$w"
    fi
    tmux capture-pane -t "astra:${w}" -p -S - 2>/dev/null || true
  else
    [ -n "$last_round" ] && printf "\n${YEL}====== ROUND ENDED ======${RST}\n\n" && last_round=""
    printf "${DIM}Waiting for next round\u2026${RST}\n"
  fi
  sleep 5
  clear
done
