#!/usr/bin/env bash
# .astra_dash_usage.sh - Recent OpenCodex model/provider usage table
source "$(dirname "$0")/.astra_dash_lib.sh"

while true; do
  W=$(term_width)
  printf "${BOLD}${CYN}  USAGE${RST}  ${DIM}~/.opencodex/usage.jsonl${RST}\n\n"

  if [ ! -f "$USAGE_FILE" ]; then
    printf "${DIM}  No usage data available.${RST}\n"
  else
    total=$(wc -l < "$USAGE_FILE" 2>/dev/null) || true
    total=$(safe_num "$total")
    astra_n=$(grep -c "astra" "$USAGE_FILE" 2>/dev/null) || true
    muse_n=$(grep -c "muse" "$USAGE_FILE" 2>/dev/null) || true
    mimo_n=$(grep -c "mimo" "$USAGE_FILE" 2>/dev/null) || true
    astra_n=$(safe_num "$astra_n")
    muse_n=$(safe_num "$muse_n")
    mimo_n=$(safe_num "$mimo_n")

    printf "${DIM}  Total: %d  Astra: %d  Muse: %d  MiMo: %d${RST}\n\n" \
      "$total" "$astra_n" "$muse_n" "$mimo_n"

    if [ "$W" -ge 90 ]; then
      printf "  %-6s  %-7s  %5s  %8s  %8s  %7s  %s\n" \
        "TIME" "MODEL" "DUR" "INPUT" "CACHE" "OUT" "STATUS"
      printf "  %-6s  %-7s  %5s  %8s  %8s  %7s  %s\n" \
        "------" "-------" "-----" "--------" "--------" "-------" "------"
    else
      printf "  %-5s  %-5s  %4s  %7s  %7s  %6s  %s\n" \
        "TIME" "MODEL" "DUR" "IN" "CACHE" "OUT" "ST"
      printf "  %-5s  %-5s  %4s  %7s  %7s  %6s  %s\n" \
        "-----" "-----" "----" "-------" "-------" "------" "--"
    fi

    tail -20 "$USAGE_FILE" 2>/dev/null | while IFS= read -r ln; do
      [ -z "$ln" ] && continue
      ts_ms=$(echo "$ln" | jq -r ".timestamp // 0" 2>/dev/null) || true
      ts_ms=$(safe_num "$ts_ms")
      if [ "$ts_ms" -gt 9999999999 ]; then
        ts_sec=$((ts_ms / 1000))
      else
        ts_sec=$ts_ms
      fi
      [ "$ts_sec" -eq 0 ] && time_str="--" || time_str=$(date -d "@$ts_sec" +%H:%M 2>/dev/null || echo "--")

      model=$(echo "$ln" | jq -r ".model // empty" 2>/dev/null) || true
      ml=$(model_label "$model")

      dur_ms=$(echo "$ln" | jq -r ".durationMs // 0" 2>/dev/null) || true
      dur_ms=$(safe_num "$dur_ms")
      dur_s=$((dur_ms / 1000))

      in_tok=$(echo "$ln" | jq -r ".usage.inputTokens // 0" 2>/dev/null) || true
      in_tok=$(safe_num "$in_tok")
      cache_tok=$(echo "$ln" | jq -r ".usage.cachedInputTokens // 0" 2>/dev/null) || true
      cache_tok=$(safe_num "$cache_tok")
      out_tok=$(echo "$ln" | jq -r ".usage.outputTokens // 0" 2>/dev/null) || true
      out_tok=$(safe_num "$out_tok")

      sts=$(echo "$ln" | jq -r ".status // 0" 2>/dev/null) || true
      sts=$(safe_num "$sts")
      if [ "$sts" -eq 200 ]; then
        sts_str="${GRN}\u2713${RST}"
      elif [ "$sts" -eq 429 ]; then
        sts_str="${YEL}429${RST}"
      elif [ "$sts" -ge 500 ]; then
        sts_str="${RED}${sts}${RST}"
      else
        sts_str="${RED}${sts}${RST}"
      fi

      if [ "$W" -ge 90 ]; then
        printf "  %-6s  %-7s  %4ds  %8s  %8s  %7s  %b\n" \
          "$time_str" "$ml" "$dur_s" "$(fmt_tokens "$in_tok")" \
          "$(fmt_tokens "$cache_tok")" "$(fmt_tokens "$out_tok")" "$sts_str"
      else
        printf "  %-5s  %-5s  %3ds  %7s  %7s  %6s  %b\n" \
          "$time_str" "$ml" "$dur_s" "$(fmt_tokens "$in_tok")" \
          "$(fmt_tokens "$cache_tok")" "$(fmt_tokens "$out_tok")" "$sts_str"
      fi
    done
  fi

  sleep 5
  clear
done
