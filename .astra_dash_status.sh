#!/usr/bin/env bash
# .astra_dash_status.sh - Compact full-width status dashboard with usage tracking
source "$(dirname "$0")/.astra_dash_lib.sh"

CONTEXT_LIMIT=120000
CACHE_DIR="/tmp/astra-dash-cache"
mkdir -p "$CACHE_DIR" 2>/dev/null || true

prev_astra=0; prev_muse=0; prev_mimo=0; prev_e429=0; prev_e5xx=0
last_round_seen=""

while true; do
  W=$(term_width)
  NOW=$(date +%s)

  # -- State detection --
  sup_state=$(detect_state)

  # -- Process-based round tracking --
  sup_pid=$(get_supervisor_pid)
  codex_pid=""
  codex_round=""
  codex_start=0
  rnd_epoch=0
  rnd_el=0

  if [ -n "$sup_pid" ]; then
    codex_pid=$(get_codex_child_pid "$sup_pid")
  fi

  if [ -n "$codex_pid" ]; then
    codex_round=$(get_codex_round_num "$codex_pid")
    codex_start=$(get_codex_start_time "$codex_pid")
    [ "$codex_start" -gt 0 ] && rnd_el=$((NOW - codex_start))
    [ "$codex_start" -gt 0 ] && rnd_epoch=$codex_start
  fi

  # Fallback: check supervisor log for round number
  if [ -z "$codex_round" ]; then
    if [ "$sup_state" = "RUNNING" ] || [ "$sup_state" = "AUDIT" ] || [ "$sup_state" = "DRAINING" ] || [ "$sup_state" = "BETWEEN_ROUNDS" ]; then
      latest_log_round=$(grep -oP "Round \\K[0-9]+" "$SUPERVISOR_LOG" 2>/dev/null | tail -1) || true
      codex_round="${latest_log_round:-}"
    fi
  fi

  # For between rounds / finished / stopped, get last round info
  if [ -z "$codex_pid" ] && [ -n "$codex_round" ]; then
    rnd_start=$(get_round_start "$codex_round")
    rnd_epoch=$(ts_to_epoch "$rnd_start")
    [ "$rnd_epoch" -gt 0 ] && rnd_el=0
  fi

  # -- Read mode and totals from metadata --
  sup_mode=$(get_metadata "mode")
  sup_hours=$(get_metadata "hours")

  # -- Supervisor elapsed --
  sup_epoch=0
  sup_el=0
  if [ -n "$sup_pid" ]; then
    sup_start=$(get_supervisor_start)
    sup_epoch=$(ts_to_epoch "$sup_start")
    [ "$sup_epoch" -gt 0 ] && sup_el=$((NOW - sup_epoch))
  fi

  # -- Compute remaining / total display --
  no_supervisor=false
  if [ -z "$sup_pid" ]; then
    no_supervisor=true
  fi

  if [ "$no_supervisor" = "true" ]; then
    total_display="--"
    remaining_str="--"
  elif [ "$sup_mode" = "continuous" ]; then
    total_display="\u221e"
    remaining_str="--"
  elif [ -n "$sup_mode" ] && [ "$sup_mode" = "hours" ] && [ -n "$sup_hours" ] && [ "$sup_hours" -gt 0 ] 2>/dev/null; then
    total_display="$(( sup_hours * 3600 ))"
    if [ "$sup_epoch" -gt 0 ]; then
      deadline=$(( sup_epoch + sup_hours * 3600 ))
      remaining=$(( deadline - NOW ))
      [ "$remaining" -lt 0 ] && remaining=0
      remaining_str="$(fmt_duration "$remaining")"
    else
      remaining_str="--"
    fi
  else
    total_display="8h"
    if [ "$sup_epoch" -gt 0 ]; then
      deadline=$(( sup_epoch + 8 * 3600 ))
      remaining=$(( deadline - NOW ))
      [ "$remaining" -lt 0 ] && remaining=0
      remaining_str="$(fmt_duration "$remaining")"
    else
      remaining_str="--"
    fi
  fi

  # -- Context (Astra only) --
  ctx_tokens=0
  if [ -f "$USAGE_FILE" ]; then
    raw=$(grep "gpt-6-astra" "$USAGE_FILE" 2>/dev/null | jq -r "select(.provider==\"openai\" and (.model==\"gpt-6-astra\" or .resolvedModel==\"gpt-6-astra\") and .status==200) | .usage.inputTokens // 0" 2>/dev/null | grep -v '^null$' | grep -v '^0$' | tail -1) || true
    ctx_tokens=$(safe_num "$raw")
  fi
  ctx_pct=0
  [ "$ctx_tokens" -gt 0 ] && ctx_pct=$((ctx_tokens * 100 / CONTEXT_LIMIT))
  [ "$ctx_pct" -gt 100 ] && ctx_pct=100
  bar_w=20; [ "$W" -lt 70 ] && bar_w=12
  ctx_color="$GRN"; [ "$ctx_pct" -ge 75 ] && ctx_color="$YEL"; [ "$ctx_pct" -ge 90 ] && ctx_color="$RED"

  # -- State string --
  case "$sup_state" in
    RUNNING)
      sc="${GRN}\u25cf RUNNING \u2022 ROUND ${codex_round:-?}${RST}"
      ;;
    AUDIT)
      sc="${MAG}\u25cf AUDIT \u2022 ROUND ${codex_round:-?}${RST}"
      ;;
    DRAINING)
      sc="${YEL}\u25cf DRAINING \u2022 FINAL ROUND ${codex_round:-?}${RST}"
      ;;
    BETWEEN_ROUNDS)
      sc="${GRN}\u25c9 RUNNING \u2022 BETWEEN ROUNDS${RST}"
      ;;
    PAUSED)
      sc="${RED}\u26a0 PAUSED \u2022 UNSAFE GIT${RST}"
      ;;
    BLOCKED)
      sc="${RED}\u26a0 BLOCKED${RST}"
      ;;
    FINISHED)
      sc="${DIM}\u25a0 FINISHED${RST}"
      ;;
    STOPPED)
      sc="${DIM}\u25a0 STOPPED${RST}"
      ;;
    *)
      sc="${DIM}\u25a0 UNKNOWN${RST}"
      ;;
  esac

  # -- Header --
  printf "${BOLD}RULE 30 \u2022 ASTRA RESEARCH${RST}"
  [ -n "$codex_round" ] && printf "  ${DIM}Round %s${RST}" "$codex_round"
  if [ "$sup_mode" = "continuous" ] && [ "$no_supervisor" = "false" ]; then
    printf "  ${CYN}${DIM}CONTINUOUS${RST}"
  fi
  printf "\n"

  # -- Status line with elapsed timer --
  if [ "$no_supervisor" = "true" ]; then
    printf "%b  No supervisor running\n" "$sc"
  else
    elapsed_str="$(fmt_duration "$rnd_el")"
    printf "%b  Round %s \u2022 %s" \
      "$sc" "${codex_round:--}" "$elapsed_str"
    if [ "$sup_mode" = "continuous" ] && [ "$sup_el" -gt 0 ]; then
      printf "  ${DIM}Total: %s${RST}" "$(fmt_duration "$sup_el")"
    elif [ "$sup_mode" = "hours" ] && [ -n "$sup_hours" ] && [ "$sup_hours" -gt 0 ] 2>/dev/null; then
      printf "  ${DIM}Total: %s${RST}" "$(fmt_duration "$sup_el")"
    fi
    printf "\n"
  fi

  # -- Context --
  if [ "$ctx_tokens" -gt 0 ]; then
    printf "Astra ctx %7s / 120k  ${ctx_color}%s${RST}  %d%%\n" \
      "$(fmt_tokens "$ctx_tokens")" "$(progress_bar "$ctx_pct" "$bar_w")" "$ctx_pct"
  else
    printf "Astra ctx     -- / 120k  ${DIM}\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591${RST}  --%%\n"
  fi

  # -- Rollover status --
  rollover_state=$(cat "$ROLLOVER_STATEFILE" 2>/dev/null || echo "NORMAL")
  rollover_mandatory_ts=$(cat /tmp/astra-supervisor/rollover_mandatory_ts 2>/dev/null || echo "0")
  rollover_exists=false; [ -f "${REPO}/astra-rollover" ] && rollover_exists=true
  stop_exists=false; [ -f "${REPO}/astra-stop" ] && stop_exists=true

  case "$rollover_state" in
    NORMAL)            rollover_display="${GRN}NORMAL${RST}" ;;
    WRAP_REQUESTED)    rollover_display="${YEL}WRAP REQUESTED${RST}" ;;
    ROLLOVER_REQUESTED) rollover_display="${RED}ROLLOVER REQUESTED${RST}" ;;
    HARD_INTERRUPT)    rollover_display="${RED}${BOLD}HARD INTERRUPT${RST}" ;;
    EMERGENCY_KILL)    rollover_display="${RED}${BOLD}FORCED ROLLOVER${RST}" ;;
    *)                 rollover_display="${DIM}$rollover_state${RST}" ;;
  esac
  printf "Rollover %b" "$rollover_display"
  if [ "$rollover_mandatory_ts" -gt 0 ] 2>/dev/null; then
    roll_elapsed=$(( NOW - rollover_mandatory_ts ))
    printf "  ${DIM}(%s since request)${RST}" "$(fmt_duration "$roll_elapsed")"
  fi
  printf "\n"

  signal_str=""
  [ "$stop_exists" = "true" ] && signal_str="${RED}STOP${RST} "
  [ "$rollover_exists" = "true" ] && signal_str="${signal_str}${YEL}ROLLOVER${RST} "
  [ -n "$signal_str" ] && printf "Signals   %b\n" "$signal_str"

  # -- Git --
  cd "${REPO}" 2>/dev/null || true
  g_hash=$(git log --oneline -1 2>/dev/null | cut -d" " -f1) || true
  [ -z "$g_hash" ] && g_hash="--"
  g_dirty=$(git status --porcelain 2>/dev/null | grep -v "??" | wc -l | tr -d " ") || true
  g_dirty=$(safe_num "$g_dirty")
  g_ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null) || true
  g_ahead=$(safe_num "$g_ahead")
  g_pushed="pushed"; [ "$g_ahead" -gt 0 ] && g_pushed="unpushed"
  g_state="clean"; [ "$g_dirty" -gt 0 ] && g_state="${g_dirty} dirty"

  printf "Git      %s %s \u2022 %s \u2022 ahead %s\n" \
    "$g_hash" "$g_pushed" "$g_state" "$g_ahead"

  # -- Workers (bulk jq+awk pass) --
  r_astra=0; r_muse=0; r_mimo=0; run_astra=0; run_muse=0; run_mimo=0; err429=0; err5xx=0
  if [ -f "$USAGE_FILE" ]; then
    jq -r 'select(.status==200) | [( (.timestamp/1000|floor|tostring)), .provider, .model] | join("\t")' "$USAGE_FILE" 2>/dev/null | awk -F"\t" -v re="$rnd_epoch" -v se="$sup_epoch" '
      { t=int($1); p=$2; m=$3 }
      t >= se {
        if (p=="openai" && m~/astra/) run_astra++
        else if (p=="opencode-go" && m~/muse/) run_muse++
        else if (p=="opencode-go" && m~/mimo/) run_mimo++
      }
      t >= re && re > 0 {
        if (p=="openai" && m~/astra/) r_astra++
        else if (p=="opencode-go" && m~/muse/) r_muse++
        else if (p=="opencode-go" && m~/mimo/) r_mimo++
      }
      END { printf "%d %d %d %d %d %d\n", r_astra, r_muse, r_mimo, run_astra, run_muse, run_mimo }
    ' > /tmp/_astra_w.txt 2>/dev/null || true
    read r_astra r_muse r_mimo run_astra run_muse run_mimo < /tmp/_astra_w.txt 2>/dev/null || true

    # Errors (round only)
    jq -r 'select(.status!=200) | [( (.timestamp/1000|floor|tostring)), (.status|tostring)] | join("\t")' "$USAGE_FILE" 2>/dev/null | awk -F"\t" -v re="$rnd_epoch" '
      { t=int($1); st=int($2) }
      t >= re && re > 0 {
        if (st==429) e429++
        else if (st>=500 && st<600) e5xx++
      }
      END { printf "%d %d\n", e429, e5xx }
    ' > /tmp/_astra_e.txt 2>/dev/null || true
    read err429 err5xx < /tmp/_astra_e.txt 2>/dev/null || true
  fi

  if [ -z "$codex_pid" ]; then
    r_astra=$prev_astra; r_muse=$prev_muse; r_mimo=$prev_mimo
    err429=$prev_e429; err5xx=$prev_e5xx
  fi

  if [ -n "$codex_round" ]; then
    echo "$r_astra" > "$CACHE_DIR/r${codex_round}_astra" 2>/dev/null || true
    echo "$r_muse" > "$CACHE_DIR/r${codex_round}_muse" 2>/dev/null || true
    echo "$r_mimo" > "$CACHE_DIR/r${codex_round}_mimo" 2>/dev/null || true
    echo "$err429" > "$CACHE_DIR/r${codex_round}_e429" 2>/dev/null || true
    echo "$err5xx" > "$CACHE_DIR/r${codex_round}_e5xx" 2>/dev/null || true
  fi

  err_str=""
  [ "$err429" -gt 0 ] && err_str="  429:${err429}"
  [ "$err5xx" -gt 0 ] && err_str="${err_str}  5xx:${err5xx}"

  # -- Delegation ratio --
  total_calls=$(( run_astra + run_muse + run_mimo ))
  if [ "$total_calls" -gt 0 ]; then
    deleg_pct=$(( (run_muse + run_mimo) * 100 / total_calls ))
    printf "Workers R A%d M%d Mi%d  Run A%d M%d Mi%d%s  Deleg %d%%\n" \
      "$r_astra" "$r_muse" "$r_mimo" \
      "$run_astra" "$run_muse" "$run_mimo" "$err_str" "$deleg_pct"
  else
    printf "Workers R A%d M%d Mi%d  Run A%d M%d Mi%d%s\n" \
      "$r_astra" "$r_muse" "$r_mimo" \
      "$run_astra" "$run_muse" "$run_mimo" "$err_str"
  fi

  # -- Usage rates (5h avg/hour + weekly avg/hour) --
  if [ -f "$USAGE_FILE" ] && [ "$sup_epoch" -gt 0 ]; then
    # Last 5 hours
    five_h_ago=$(( NOW - 18000 ))
    tok_5h=$(usage_tokens_in_window "all" "all" "$five_h_ago" "$NOW")
    calls_5h=$(usage_calls_in_window "all" "all" "$five_h_ago" "$NOW")
    # Last 7 days
    week_ago=$(( NOW - 604800 ))
    tok_wk=$(usage_tokens_in_window "all" "all" "$week_ago" "$NOW")
    calls_wk=$(usage_calls_in_window "all" "all" "$week_ago" "$NOW")
    # Session totals
    tok_sess=$(usage_tokens_in_window "all" "all" "$sup_epoch" "$NOW")
    calls_sess=$(usage_calls_in_window "all" "all" "$sup_epoch" "$NOW")

    # Rates per hour (use integer hours to avoid bc overflow)
    sess_secs=$(( NOW - sup_epoch )); [ "$sess_secs" -lt 3600 ] && sess_secs=3600
    sess_hrs=$(( sess_secs / 3600 )); [ "$sess_hrs" -lt 1 ] && sess_hrs=1
    wk_secs=$(( NOW - week_ago )); wk_hrs=$(( wk_secs / 3600 )); [ "$wk_hrs" -lt 1 ] && wk_hrs=1

    rate_5h_t="$(echo "scale=0; $tok_5h / 5" | bc 2>/dev/null || echo 0)"
    rate_5h_c="$(echo "scale=1; $calls_5h / 5" | bc 2>/dev/null || echo 0)"
    rate_wk_t="$(echo "scale=0; $tok_wk / $wk_hrs" | bc 2>/dev/null || echo 0)"
    rate_wk_c="$(echo "scale=1; $calls_wk / $wk_hrs" | bc 2>/dev/null || echo 0)"
    rate_sess_t="$(echo "scale=0; $tok_sess / $sess_hrs" | bc 2>/dev/null || echo 0)"
    rate_sess_c="$(echo "scale=1; $calls_sess / $sess_hrs" | bc 2>/dev/null || echo 0)"

    printf "Usage    Sess %stok %scalls/h  5h %stok %scalls/h  Wk %stok %scalls/h\n" \
      "$(fmt_tokens "$tok_sess")" "$rate_sess_c" \
      "$(fmt_tokens "$rate_5h_t")" "$rate_5h_c" \
      "$(fmt_tokens "$rate_wk_t")" "$rate_wk_c"
  fi

  # -- Last Request --
  if [ -f "$USAGE_FILE" ]; then
    last_line=$(tail -1 "$USAGE_FILE" 2>/dev/null) || true
    if [ -n "$last_line" ]; then
      l_dur=$(echo "$last_line" | jq -r ".durationMs // 0" 2>/dev/null) || true
      l_dur=$(safe_num "$l_dur"); l_dur_s=$((l_dur / 1000))
      l_in=$(echo "$last_line" | jq -r ".usage.inputTokens // 0" 2>/dev/null) || true
      l_in=$(safe_num "$l_in")
      l_cache=$(echo "$last_line" | jq -r ".usage.cachedInputTokens // 0" 2>/dev/null) || true
      l_cache=$(safe_num "$l_cache")
      l_out=$(echo "$last_line" | jq -r ".usage.outputTokens // 0" 2>/dev/null) || true
      l_out=$(safe_num "$l_out")
      l_sts=$(echo "$last_line" | jq -r ".status // 0" 2>/dev/null) || true
      l_sts=$(safe_num "$l_sts")
      l_mdl=$(echo "$last_line" | jq -r ".model // \"\"" 2>/dev/null) || true
      l_icon="${GRN}\u2713${RST}"; [ "$l_sts" -ne 200 ] && l_icon="${RED}\u2717${RST}"

      printf "Last     %s %ds \u2022 %s in \u2022 %s cache \u2022 %s out %b\n" \
        "$(model_label "$l_mdl")" "$l_dur_s" "$(fmt_tokens "$l_in")" \
        "$(fmt_tokens "$l_cache")" "$(fmt_tokens "$l_out")" "$l_icon"
    else
      printf "Last     --\n"
    fi
  else
    printf "Last     --\n"
  fi

  if [ -f "$STOP_FILE" ] && [ -z "$sup_pid" ]; then
    printf "${RED}${BOLD}STOP FILE DETECTED${RST}\n"
  fi

  sleep 5
  clear
done
