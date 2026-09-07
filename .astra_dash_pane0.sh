#!/usr/bin/env bash
# Pane 0: Live Research - follows current round
last_round=""
while true; do
  win=$(tmux list-windows -t astra -F "#{window_name}" 2>/dev/null | grep -E "^r[0-9]+$" | sort -t"r" -k2 -n | tail -1)
  if [ -n "${win}" ]; then
    if [ "${win}" != "${last_round}" ]; then
      [ -n "${last_round}" ] && printf "\n\033[1;33m====== %s FINISHED ======\033[0m\n" "$(echo "${last_round}" | tr "[:lower:]" "[:upper:]")"
      printf "\033[1;36m====== %s START ======\033[0m\n" "$(echo "${win}" | tr "[:lower:]" "[:upper:]")"
      rn="${win#r}"; grep -F "Round ${rn} starting" /home/ryan/rule30-lab/astra-supervisor.log 2>/dev/null | tail -1 | sed "s/^/  /"
      tmux capture-pane -t astra:${win} -p 2>/dev/null | grep "session id:" | tail -1 | sed "s/^/  /"
      git -C /home/ryan/rule30-lab log --oneline -1 2>/dev/null | sed "s/^/  commit: /"; printf "\n"
      last_round="${win}"
    fi
    tmux capture-pane -t astra:${win} -p -S - 2>/dev/null
  else
    [ -n "${last_round}" ] && printf "\n\033[1;33m====== %s FINISHED ======\033[0m\n" "$(echo "${last_round}" | tr "[:lower:]" "[:upper:]")" && last_round=""
    printf "\033[2mWaiting for next round...\033[0m\n"
  fi
  sleep 5
  clear
done