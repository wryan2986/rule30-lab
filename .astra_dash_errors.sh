#!/usr/bin/env bash
# .astra_dash_errors.sh - Recent 429/5xx/supervisor errors
source "$(dirname "$0")/.astra_dash_lib.sh"

while true; do
  printf "${BOLD}${RED}  ERRORS & PROBLEMS${RST}\n\n"

  found=0

  if [ -f "$USAGE_FILE" ]; then
    errs=$(tail -200 "$USAGE_FILE" 2>/dev/null | jq -r \
      "select(.status != 200) | \(.timestamp/1000 | todate | split(\"T\")[1] | split(\".\")[0]) + \"  \" + (.model | split(\"-\") | last | .[0:8]) + \"  \" + (.status|tostring)" \
      2>/dev/null) || true
    if [ -n "$errs" ]; then
      printf "${BOLD}  Provider errors (recent):${RST}\n"
      echo "$errs" | tail -10 | while IFS= read -r ln; do
        [ -z "$ln" ] && continue
        printf "    %s\n" "$ln"
      done
      found=1
    fi
  fi

  if [ -f "$SUPERVISOR_LOG" ]; then
    sup_errs=$(grep -iE "fail|error|timeout|exit=[^0]" "${SUPERVISOR_LOG}" 2>/dev/null | tail -10) || true
    if [ -n "$sup_errs" ]; then
      [ "$found" -eq 1 ] && echo ""
      printf "${BOLD}  Supervisor log issues:${RST}\n"
      echo "$sup_errs" | while IFS= read -r ln; do
        [ -z "$ln" ] && continue
        printf "    %s\n" "$ln"
      done
      found=1
    fi
  fi

  cd "${REPO}" 2>/dev/null || true
  g_dirty=$(git status --porcelain 2>/dev/null | grep -v "??" | wc -l | tr -d " ") || true
  g_dirty=$(safe_num "$g_dirty")
  g_ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null) || true
  g_ahead=$(safe_num "$g_ahead")
  if [ "$g_dirty" -gt 0 ] || [ "$g_ahead" -gt 0 ]; then
    [ "$found" -eq 1 ] && echo ""
    printf "${BOLD}  Git state:${RST}\n"
    [ "$g_dirty" -gt 0 ] && printf "    ${YEL}%d dirty tracked files${RST}\n" "$g_dirty"
    [ "$g_ahead" -gt 0 ] && printf "    ${YEL}%d unpushed commits${RST}\n" "$g_ahead"
    found=1
  fi

  if [ -f "$STOP_FILE" ]; then
    [ "$found" -eq 1 ] && echo ""
    printf "  ${RED}${BOLD}\u26a0 STOP FILE EXISTS: %s${RST}\n" "$STOP_FILE"
    found=1
  fi

  if [ "$found" -eq 0 ]; then
    printf "  ${DIM}No recent problems.${RST}\n"
  fi

  sleep 8
  clear
done
