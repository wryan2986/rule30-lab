#!/usr/bin/env bash
# .astra_dash_git.sh - Git state and recent commits
source "$(dirname "$0")/.astra_dash_lib.sh"

while true; do
  cd "${REPO}" 2>/dev/null || true
  printf "${BOLD}${CYN}  GIT STATE${RST}\n\n"

  branch=$(git branch --show-current 2>/dev/null) || true
  [ -z "$branch" ] && branch="--"
  hash=$(git log --oneline -1 2>/dev/null | cut -d" " -f1) || true
  [ -z "$hash" ] && hash="--"
  ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null) || true
  ahead=$(safe_num "$ahead")
  behind=$(git rev-list --count HEAD..@{u} 2>/dev/null) || true
  behind=$(safe_num "$behind")
  dirty=$(git status --porcelain 2>/dev/null | grep -v "??" | wc -l | tr -d " ") || true
  dirty=$(safe_num "$dirty")

  printf "  Branch:  ${BOLD}%s${RST}\n" "$branch"
  printf "  HEAD:    %s\n" "$hash"
  printf "  Ahead:   %d   Behind: %d\n" "$ahead" "$behind"
  printf "  Dirty:   %d tracked files\n" "$dirty"

  ho_time=$(stat -c %y "${REPO}/ASTRA_HANDOFF.md" 2>/dev/null | cut -d. -f1) || true
  [ -z "$ho_time" ] && ho_time="--"
  printf "  Handoff: %s\n\n" "$ho_time"

  last_push=$(grep -F "push" "${SUPERVISOR_LOG}" 2>/dev/null | grep -v "failed" | tail -1 | sed "s/.*\[\([0-9-]* [0-9:]*\)\].*/\1/") || true
  [ -z "$last_push" ] && last_push="none"
  printf "  Last push: %s\n\n" "$last_push"

  printf "${BOLD}  Recent commits:${RST}\n"
  git log --oneline -10 2>/dev/null | while IFS= read -r ln; do
    [ -z "$ln" ] && continue
    printf "    %s\n" "$ln"
  done

  if [ "$dirty" -gt 0 ]; then
    printf "\n${BOLD}  Dirty tracked files:${RST}\n"
    git status --porcelain 2>/dev/null | grep -v "??" | head -10 | while IFS= read -r ln; do
      printf "    %s\n" "$ln"
    done
    [ "$dirty" -gt 10 ] && printf "    ${DIM}... and %d more${RST}\n" "$((dirty - 10))"
  fi

  sleep 8
  clear
done
