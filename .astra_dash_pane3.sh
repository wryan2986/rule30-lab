#!/usr/bin/env bash
# Pane 3: Model / Provider Activity
USAGE="/home/ryan/.opencodex/usage.jsonl"
while true; do
  printf "\033[1m=== MODEL / PROVIDER ===\033[0m\n"
  if [ -f "${USAGE}" ]; then
    astra_n=$(grep -c '"model":"gpt-6-astra' "${USAGE}")
    muse_n=$(grep -c '"model":"muse-spark' "${USAGE}")
    mimo_n=$(grep -c '"model":"mimo-v2.5' "${USAGE}")
    printf "Astra=%d Muse=%d MiMo=%d\n" "${astra_n}" "${muse_n}" "${mimo_n}"
    rw=$(tmux list-windows -t astra -F "#{window_name}" 2>/dev/null | grep -E "^r[0-9]+$" | sort -t"r" -k2 -n | tail -1)
    if [ -n "${rw}" ]; then
      rn="${rw#r}"
      rt=$(grep -F "Round ${rn} starting" /home/ryan/rule30-lab/astra-supervisor.log 2>/dev/null | tail -1 | grep -oP "^\[\K[^\]]+")
      if [ -n "${rt}" ]; then
        re=$(date -d "${rt}" +%s 2>/dev/null || echo 0)
        ra=$(awk -v re=${re} '{ts=int($2/1000); if(ts>=re && $0 ~ /"model":"gpt-6-astra/) c++} END{print c+0}' "${USAGE}")
        rm=$(awk -v re=${re} '{ts=int($2/1000); if(ts>=re && $0 ~ /"model":"muse-spark/) c++} END{print c+0}' "${USAGE}")
        rmm=$(awk -v re=${re} '{ts=int($2/1000); if(ts>=re && $0 ~ /"model":"mimo-v2.5/) c++} END{print c+0}' "${USAGE}")
        printf "This rnd: Astra=%d Muse=%d MiMo=%d\n" "${ra}" "${rm}" "${rmm}"
      fi
    fi
    printf "\033[2m--- recent ---\033[0m\n"
    tail -5 "${USAGE}" 2>/dev/null | while IFS= read -r ln; do
      m=$(echo "${ln}" | jq -r '.model' 2>/dev/null)
      case "${m}" in gpt-6-astra) s=AST;; muse-spark*) s=MUS;; mimo-v2.5) s=MIMO;; *) s=${m:0:4};; esac
      printf "  %s %4dms in=%-6d cache=%-6d out=%-4d\n" "${s}" "$(echo "${ln}" | jq -r '.durationMs')" "$(echo "${ln}" | jq -r '.usage.inputTokens')" "$(echo "${ln}" | jq -r '.usage.cachedInputTokens')" "$(echo "${ln}" | jq -r '.usage.outputTokens')"
    done
  else printf "usage.jsonl not found\n"; fi
  sleep 8
  clear
done
