#!/usr/bin/env bash
# Pane 1: Supervisor Status
while true; do
  printf "\033[1m=== SUPERVISOR STATUS ===\033[0m\n"
  st=$(grep -F "Astra supervisor starting" /home/ryan/rule30-lab/astra-supervisor.log 2>/dev/null | tail -1 | grep -oP "^\[\K[^\]]+")
  [ -n "${st}" ] && se=$(date -d "${st}" +%s 2>/dev/null || echo 0) && now=$(date +%s) && el=$((now-se)) && printf "Elapsed: %dh%02dm / ~8h (%d%%)\n" $((el/3600)) $(((el%3600)/60)) $((el*100/28800))
  rw=$(tmux list-windows -t astra -F "#{window_name}" 2>/dev/null | grep -E "^r[0-9]+$" | sort -t"r" -k2 -n | tail -1)
  if [ -n "${rw}" ]; then
    rn="${rw#r}"; printf "Round: #%s\n" "${rn}"
    rt=$(grep -F "Round ${rn} starting" /home/ryan/rule30-lab/astra-supervisor.log 2>/dev/null | tail -1 | grep -oP "^\[\K[^\]]+")
    [ -n "${rt}" ] && re=$(date -d "${rt}" +%s 2>/dev/null || echo 0) && now=$(date +%s) && printf "Round: %dh%02dm\n" $(((now-re)/3600)) $(((now-re)%3600/60))
    pp=$(tmux display-message -t astra:${rw} -p "#{pane_pid}" 2>/dev/null || true)
    [ -n "${pp}" ] && cp=$(pgrep -P "${pp}" 2>/dev/null | head -1 || true) && [ -n "${cp}" ] && printf "PID: %s\n" "${cp}"
  else printf "Round: (between)\n"; fi
  if [ -f /home/ryan/.opencodex/usage.jsonl ]; then
    le=$(tail -1 /home/ryan/.opencodex/usage.jsonl 2>/dev/null)
    printf "Model: %s (%s)\n" "$(echo "${le}" | jq -r '.model // "?"')" "$(echo "${le}" | jq -r '.provider // "?"')"
    it=$(echo "${le}" | jq -r '.usage.inputTokens // 0' 2>/dev/null)
    ct=$(echo "${le}" | jq -r '.usage.cachedInputTokens // 0' 2>/dev/null)
    printf "Tokens: %d in (%d cached)\n" "${it}" "${ct}"
    [ "${it}" -gt 120000 ] 2>/dev/null && printf "\033[1;31m!! >120k ROLLOVER\033[0m\n" || [ "${it}" -gt 100000 ] 2>/dev/null && printf "\033[1;33m! ~120k\033[0m\n"
  fi
  [ -f /home/ryan/rule30-lab/astra-stop ] && printf "\033[1;31mSTOP FILE\033[0m\n" || printf "Stop: no\n"
  sleep 8
  clear
done