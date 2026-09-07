#!/usr/bin/env bash
# =========================================================================
# run_astra_supervisor.sh — Graceful long-running Astra research supervisor
# =========================================================================
# Replaces the fixed-deadline runner with a soft-deadline, stall-aware,
# audit-capable supervisor.
#
# Modes:
#   --hours N        Run for N hours then drain (default: 8)
#   --continuous     Continue until a stop condition
#
# States (written to STATEFILE for dashboard):
#   RUNNING          Round in progress
#   BETWEEN_ROUNDS   Supervisor alive, no active round
#   AUDIT            Audit round in progress
#   DRAINING         Deadline passed, final round finishing
#   PAUSED           Unsafe git / blocked
#   FINISHED         Normal exit
#   STOPPED          Stop file detected
#
# Stop: touch /home/ryan/rule30-lab/astra-stop
# Watch: tmux attach -t astra
# =========================================================================

set -euo pipefail

# ── Argument parsing ─────────────────────────────────────────────────────
MODE="hours"
HOURS=8

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hours)
      MODE="hours"
      HOURS="${2:?--hours requires a number}"
      shift 2
      ;;
    --continuous)
      MODE="continuous"
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: $0 [--hours N | --continuous]" >&2
      exit 1
      ;;
  esac
done

# ── Constants ────────────────────────────────────────────────────────────
SESSION="astra"
REPO="/home/ryan/rule30-lab"
LOGFILE="${REPO}/astra-supervisor.log"
STOPFILE="${REPO}/astra-stop"
TMPDIR_ASTRA="/tmp/astra-supervisor"
STATEFILE="${TMPDIR_ASTRA}/state"
METADATA="${TMPDIR_ASTRA}/metadata"
BRANCH="research/astra-next"

STALL_TIMEOUT=$(( 40 * 60 ))    # 40 min of no activity → stalled
STALL_POLL=30                    # check every 30s for stall
GRACEFUL_TIMEOUT=$(( 120 * 60 )) # 120 min max for draining round
SLEEP_BETWEEN=10
AUDIT_INTERVAL=7                 # audit after every 7 successful rounds
NO_PROGRESS_THRESHOLD=5          # strategy reset after 5 fruitless rounds
ROLLOVER_SOFT_WARN=100000        # 100k: ask Astra to begin wrapping up
ROLLOVER_MANDATORY=120000         # 120k: mandatory rollover request
ROLLOVER_HARD_INTERRUPT=135000    # 135k: SIGINT to current round
ROLLOVER_EMERGENCY_KILL=150000    # 150k: emergency kill current round
ROLLOVER_GRACE_PERIOD=120         # 2 min after mandatory SIGINT before SIGKILL
ROLLOVER_EMERGENCY_GRACE=90          # 90s after hard SIGINT before emergency kill
ROLLOVER_POLL=15                  # check context every 15 seconds
ROLLOVER_STATEFILE="${TMPDIR_ASTRA}/rollover_state"
ROLLOVER_LOG="${REPO}/astra-rollover.log"
ROLLFILE="${REPO}/astra-rollover"
ROLLOVER_TEST_MODE="${ROLLOVER_TEST_MODE:-false}"
ROLLOVER_TEST_MULTIPLIER="${ROLLOVER_TEST_MULTIPLIER:-1}"

# ── Helpers ──────────────────────────────────────────────────────────────
ts() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[$(ts)] $*" | tee -a "${LOGFILE}"; }

check_git_clean() {
  cd "${REPO}"
  [ ! -d .git/MERGE_HEAD ] && [ ! -d .git/rebase-merge ] && [ ! -d .git/rebase-apply ]
}

set_state() {
  local state="$1"
  mkdir -p "${TMPDIR_ASTRA}"
  echo "${state}" > "${STATEFILE}"
}

set_metadata() {
  mkdir -p "${TMPDIR_ASTRA}"
  # Write each argument as a separate key=value line
  printf '%s\n' "$@" > "${METADATA}"
}

# Get the last modification time of usage.jsonl (proxy for API activity)
usage_mtime() {
  stat -c %Y ~/.opencodex/usage.jsonl 2>/dev/null || echo 0
}

# Get the last modification time of the tmux round window's pane output
round_output_mtime() {
  local round_window="$1"
  [ -z "$round_window" ] && { echo 0; return; }
  # tmux pane tty is the best proxy; fall back to pane start time
  local pane_pid
  pane_pid=$(tmux display-message -t "${SESSION}:${round_window}" -p "#{pane_pid}" 2>/dev/null) || true
  if [ -n "${pane_pid}" ]; then
    # Process start time as proxy for last meaningful state
    stat -c %Y "/proc/${pane_pid}" 2>/dev/null || echo 0
  else
    echo 0
  fi
}

# Classify whether a round produced progress by comparing handoff hash
handoff_hash() {
  sha256sum "${REPO}/ASTRA_HANDOFF.md" 2>/dev/null | cut -d' ' -f1 || echo "none"
}

# -- Context-based rollover system --
# Reads the latest gpt-6-astra inputTokens from usage.jsonl.
# ONLY uses provider=openai, resolvedModel/model=gpt-6-astra entries.
get_astra_context_tokens() {
  local usage_file="${HOME}/.opencodex/usage.jsonl"
  [ -f "${usage_file}" ] || { echo 0; return; }
  grep 'gpt-6-astra' "${usage_file}" 2>/dev/null \
    | jq -r 'select(.provider=="openai" and (.model=="gpt-6-astra" or .resolvedModel=="gpt-6-astra") and .status==200) | .usage.inputTokens // 0' 2>/dev/null \
    | grep -v '^null$' | grep -v '^0$' \
    | tail -1 || echo 0
}

# Rollover state management
get_rollover_state() {
  [ -f "${ROLLOVER_STATEFILE}" ] && cat "${ROLLOVER_STATEFILE}" 2>/dev/null || echo "NORMAL"
}

set_rollover_state() {
  mkdir -p "${TMPDIR_ASTRA}"
  echo "$1" > "${ROLLOVER_STATEFILE}"
}

get_rollover_field() {
  local field="$1"
  local default="${2:-}"
  local file="${TMPDIR_ASTRA}/rollover_${field}"
  [ -f "${file}" ] && cat "${file}" 2>/dev/null || echo "${default}"
}

set_rollover_field() {
  local field="$1" value="$2"
  mkdir -p "${TMPDIR_ASTRA}"
  echo "${value}" > "${TMPDIR_ASTRA}/rollover_${field}"
}

reset_rollover_state() {
  rm -f "${ROLLOVER_STATEFILE}" 2>/dev/null || true
  rm -f "${TMPDIR_ASTRA}/rollover"_* 2>/dev/null || true
  set_rollover_state "NORMAL"
  set_rollover_field "warn_sent" "0"
  set_rollover_field "mandatory_sent" "0"
  set_rollover_field "hard_sent" "0"
  set_rollover_field "emergency_sent" "0"
  set_rollover_field "mandatory_ts" "0"
  set_rollover_field "hard_ts" "0"
  set_rollover_field "force_killed" "0"
  set_rollover_field "tokens" "0"
}

rollog() {
  echo "[$(ts)] $*" | tee -a "${ROLLOVER_LOG}"
}

# Scale thresholds for test mode
scale_threshold() {
  local raw="$1"
  if [ "${ROLLOVER_TEST_MODE}" = "true" ]; then
    echo $(( raw * ROLLOVER_TEST_MULTIPLIER / 100 ))
  else
    echo "${raw}"
  fi
}

# Send a string to the active round tmux window (non-blocking)
send_to_round() {
  local round_window="$1"
  local msg="$2"
  [ -z "${round_window}" ] && return 1
  tmux send-keys -t "${SESSION}:${round_window}" "${msg}" Enter 2>/dev/null || return 1
}

# Send Ctrl-C to the active round tmux window only
send_ctrl_c_to_round() {
  local round_window="$1"
  [ -z "${round_window}" ] && return 1
  tmux send-keys -t "${SESSION}:${round_window}" C-c 2>/dev/null || return 1
}

# Inspect git state after forced rollover -- never reset or discard
post_rollover_git_safety() {
  cd "${REPO}"
  if ! check_git_clean; then
    rollog "WARNING: Git in unsafe state after rollover. Entering PAUSED."
    set_state "PAUSED"
    return 1
  fi
  local dirty
  dirty=$(git status --porcelain 2>/dev/null | grep -v '??' | wc -l | tr -d ' ') || dirty=0
  if [ "${dirty}" -gt 0 ]; then
    rollog "Preserving ${dirty} uncommitted research files after rollover."
  fi
  return 0
}

# Find the active round tmux window name
get_round_window() {
  local w
  w=$(tmux list-windows -t astra -F "#{window_name}" 2>/dev/null | grep -E "^r[0-9]+$" | sort -t"r" -k2 -n | tail -1) || true
  echo "$w"
}

# Find the codex exec PID for the current round
get_round_codex_pid() {
  local sup_pid="$1"
  [ -z "${sup_pid}" ] && { echo ""; return; }
  # Direct children
  for cp in $(pgrep -P "${sup_pid}" 2>/dev/null); do
    local cmdline
    cmdline=$(cat /proc/${cp}/cmdline 2>/dev/null | tr "\0" " ") || true
    if echo "${cmdline}" | grep -q "codex exec"; then
      echo "${cp}"
      return
    fi
  done
  # Grandchildren
  for cp in $(pgrep -P "${sup_pid}" 2>/dev/null); do
    for gcp in $(pgrep -P "${cp}" 2>/dev/null); do
      local cmdline
      cmdline=$(cat /proc/${gcp}/cmdline 2>/dev/null | tr "\0" " ") || true
      if echo "${cmdline}" | grep -q "codex exec"; then
        echo "${gcp}"
        return
      fi
    done
  done
  echo ""
}

# Graceful round termination: SIGINT → wait → SIGKILL only if stuck
terminate_round() {
  local pid="$1"
  local label="${2:-round}"
  [ -z "${pid}" ] && return 0

  log "Sending SIGINT to ${label} (PID ${pid})"
  kill -INT "${pid}" 2>/dev/null || true

  # Wait up to 120 seconds for graceful exit
  local waited=0
  while [ "${waited}" -lt 120 ]; do
    if ! kill -0 "${pid}" 2>/dev/null; then
      log "${label} exited gracefully after ${waited}s"
      return 0
    fi
    sleep 5
    waited=$(( waited + 5 ))
  done

  # Only SIGKILL as last resort
  log "WARNING: ${label} did not exit after 120s SIGINT grace. Sending SIGKILL."
  kill -9 "${pid}" 2>/dev/null || true
  sleep 2
  return 0
}

# ── Check continuous-mode stop conditions ────────────────────────────────
check_continuous_stop() {
  # Stop file
  if [ -f "${STOPFILE}" ]; then
    log "Stop file detected."
    return 0
  fi

  # Unsafe git state
  if ! check_git_clean; then
    log "Git in unsafe/conflicted state."
    return 0
  fi

  # Check for proof candidate in handoff (heuristic: look for "complete proof" markers)
  if grep -qi "complete proof.*survives\|problem 1.*proved\|problem 1.*solved" "${REPO}/ASTRA_HANDOFF.md" 2>/dev/null; then
    log "Possible complete proof candidate detected in handoff."
    return 0
  fi

  # Check for research blocked (heuristic — must be affirmative, not negated)
  # Look for standalone "Research blocked" or "research is blocked" lines,
  # NOT lines like "not research blocked" or "NOT goal achieved, research blocked"
  if grep -qiP "^\s*research\s+blocked\b|research\s+is\s+blocked|all\s+.*\s+routes\s+exhausted|no\s+productive\s+next\s+attack" "${REPO}/ASTRA_HANDOFF.md" 2>/dev/null; then
    # Double-check: skip if the match is in a negated context
    block_line=$(grep -iP "^\s*research\s+blocked\b|research\s+is\s+blocked" "${REPO}/ASTRA_HANDOFF.md" 2>/dev/null | head -1) || true
    if echo "$block_line" | grep -qi "not.*research blocked\|NOT.*research blocked"; then
      :  # Negated — not actually blocked
    else
      log "Research appears blocked per handoff."
      return 0
    fi
  fi

  return 1
}

# ── Initialization ───────────────────────────────────────────────────────
mkdir -p "${TMPDIR_ASTRA}"

# Clean up stale state from previous runs (but preserve stop file for now)
rm -f "${STATEFILE}" 2>/dev/null || true
rm -f "${METADATA}" 2>/dev/null || true

# Stop file: only block if supervisor is currently running (orphan guard).
# If no supervisor is running, the stop file is stale from a previous run — remove it.
EXISTING_SUP=$(pgrep -f "run_astra_supervisor.sh|run_astra_8h.sh" 2>/dev/null | awk -v mypid=$$ "\$1 != mypid" | head -1) || true
if [ -f "${STOPFILE}" ]; then
  if [ -n "${EXISTING_SUP}" ]; then
    echo "Stop file exists and supervisor is running. Not starting."
    exit 0
  else
    echo "Stale stop file from previous run. Removing and starting fresh."
    rm -f "${STOPFILE}" 2>/dev/null || true
  fi
fi

cd "${REPO}"
git checkout "${BRANCH}" 2>/dev/null || true
git pull --ff-only origin "${BRANCH}" 2>/dev/null || true

# ── tmux session management ──
# If we are already inside the target session (e.g. launched by astra.sh
# or run from tmux), skip the session check — we are the supervisor.
CURRENT_SESSION=$(tmux display-message -p '#S' 2>/dev/null) || true
if [ "${CURRENT_SESSION}" = "${SESSION}" ]; then
  # Already inside the correct session — no need to create or check
  :
elif tmux has-session -t "${SESSION}" 2>/dev/null; then
  # Session exists but we are not inside it — check for orphaned supervisor
  ORPHAN_PID=$(pgrep -f "run_astra_supervisor.sh|run_astra_8h.sh" 2>/dev/null | awk -v mypid=$$ '$1 != mypid' | head -1) || true
  if [ -n "${ORPHAN_PID}" ]; then
    echo "Active supervisor found in existing session. Not starting duplicate."
    exit 1
  else
    echo "Orphaned tmux session detected. Cleaning up..."
    tmux kill-session -t "${SESSION}" 2>/dev/null || true
  fi
fi

# Create session if we are not inside one already
if [ "${CURRENT_SESSION}" != "${SESSION}" ]; then
  tmux new-session -d -s "${SESSION}" -x 200 -y 50
fi
tmux set-option -t "${SESSION}" status-left " [#S] "

if [ "${MODE}" = "hours" ]; then
  log "========================================"
  log "Astra supervisor | Mode: --hours ${HOURS} | Stall watchdog: ${STALL_TIMEOUT}s"
  log "Audit every ${AUDIT_INTERVAL} successful rounds | Strategy reset after ${NO_PROGRESS_THRESHOLD} fruitless"
  log "Watch: tmux attach -t ${SESSION}"
  log "========================================"
else
  log "========================================"
  log "Astra supervisor | Mode: --continuous | Stall watchdog: ${STALL_TIMEOUT}s"
  log "Audit every ${AUDIT_INTERVAL} successful rounds | Strategy reset after ${NO_PROGRESS_THRESHOLD} fruitless"
  log "Watch: tmux attach -t ${SESSION}"
  log "========================================"
fi

set_state "BETWEEN_ROUNDS"
set_metadata "mode=${MODE}" "hours=${HOURS}"

ROUND=0
OVERALL_START=$(date +%s)
DRAINING=false
SUCCESSFUL_ROUNDS=0
NO_PROGRESS_COUNT=0
PREV_HANDOFF_HASH=$(handoff_hash)

# -- Rollover state initialization --
reset_rollover_state
rollog "Rollover system initialized."

# ── Total seconds and deadline (soft) ──────────────────────────────────
TOTAL_SECONDS=0
if [ "${MODE}" = "hours" ]; then
  TOTAL_SECONDS=$(( HOURS * 3600 ))
fi

if [ "${MODE}" = "hours" ]; then
  DEADLINE=$(( OVERALL_START + TOTAL_SECONDS ))
else
  DEADLINE=0  # no deadline in continuous mode
fi

# ── Main loop ────────────────────────────────────────────────────────────
while true; do
  # ── Stop file check (always) ──
  [ -f "${STOPFILE}" ] && { log "Stop file detected."; break; }

  # ── Continuous-mode stop conditions ──
  if [ "${MODE}" = "continuous" ]; then
    check_continuous_stop && break
  fi

  # -- Manual rollover file (force-rollover-and-continue) --
  if [ -f "${ROLLFILE}" ]; then
    rollog "astra-rollover file detected. Requesting immediate round rollover."
    rm -f "${ROLLFILE}" 2>/dev/null || true
    set_rollover_state "EMERGENCY_KILL"
    set_rollover_field "force_killed" "0"
    set_rollover_field "mandatory_ts" "$(date +%s)"
  fi

  # ── Soft deadline check ──
  if [ "${MODE}" = "hours" ] && [ "${DRAINING}" != "true" ]; then
    NOW=$(date +%s)
    if [ "${NOW}" -ge "${DEADLINE}" ]; then
      # Deadline reached. Check if a round is running.
      SUP_PID=$(pgrep -f "run_astra_supervisor.sh" 2>/dev/null | head -1) || true
      CODEX_PID=""
      if [ -n "${SUP_PID}" ]; then
        CODEX_PID=$(get_round_codex_pid "${SUP_PID}")
      fi

      if [ -n "${CODEX_PID}" ]; then
        DRAINING=true
        set_state "DRAINING"
        log "========================================"
        log "Deadline reached during active round. DRAINING — final round finishing."
        log "========================================"
      else
        # No round running at deadline — stop cleanly
        ELAPSED=$(( NOW - OVERALL_START ))
        log "========================================"
        log "Deadline reached. No active round. Stopping normally."
        log "${ROUND} rounds in $(( ELAPSED / 3600 ))h $(( (ELAPSED % 3600) / 60 ))m"
        log "========================================"
        break
      fi
    fi
  fi

  # ── Git safety ──
  if ! check_git_clean; then
    set_state "PAUSED"
    log "Git in unsafe state. Waiting ${SLEEP_BETWEEN}s..."
    sleep "${SLEEP_BETWEEN}"
    set_state "BETWEEN_ROUNDS"
    continue
  fi

  cd "${REPO}"
  git checkout "${BRANCH}" 2>/dev/null || true
  git pull --ff-only origin "${BRANCH}" 2>/dev/null || true

  # ── Audit round scheduling ──
  IS_AUDIT=false
  if [ "${SUCCESSFUL_ROUNDS}" -gt 0 ] && [ $(( SUCCESSFUL_ROUNDS % AUDIT_INTERVAL )) -eq 0 ]; then
    IS_AUDIT=true
    log "--- Scheduling AUDIT round (after ${SUCCESSFUL_ROUNDS} successful rounds) ---"
  fi

  # ── No-progress strategy reset ──
  IS_RESET=false
  if [ "${NO_PROGRESS_COUNT}" -ge "${NO_PROGRESS_THRESHOLD}" ]; then
    IS_RESET=true
    log "--- Scheduling STRATEGY RESET (after ${NO_PROGRESS_COUNT} fruitless rounds) ---"
  fi

  # ── Round timeout ──
  if [ "${DRAINING}" = "true" ]; then
    this_timeout=${GRACEFUL_TIMEOUT}
  else
    this_timeout=$(( 70 * 60 ))  # standard 70-minute round window
    # If mode is hours and we're close to deadline, extend to let round finish
    if [ "${MODE}" = "hours" ]; then
      REMAINING=$(( DEADLINE - $(date +%s) ))
      if [ "${REMAINING}" -gt 0 ] && [ "${REMAINING}" -lt "${this_timeout}" ]; then
        this_timeout=$(( REMAINING + 30 * 60 ))  # deadline + 30 min grace for current work
      fi
    fi
  fi

  ROUND=$(( ROUND + 1 ))
  ROUND_START=$(date +%s)
  MINS=$(( this_timeout / 60 ))

  log "--- Round ${ROUND} (timeout ${this_timeout}s) ---"
  if [ "${IS_AUDIT}" = "true" ]; then
    set_state "AUDIT"
  else
    set_state "RUNNING"
  fi

  # ── Build prompt ──
  DONE_FILE="${TMPDIR_ASTRA}/r${ROUND}.done"
  EXIT_FILE="${TMPDIR_ASTRA}/r${ROUND}.exit"
  PROMPT_FILE="${TMPDIR_ASTRA}/r${ROUND}.prompt"

  if [ "${IS_AUDIT}" = "true" ]; then
    cat > "${PROMPT_FILE}" << AUDIT_PROMPT_EOF
You are Astra, the lead mathematical researcher for Rule 30 Prize Problem 1.

This is an AUDIT round. Read ASTRA_GOAL.md and ASTRA_HANDOFF.md first.

AUDIT OBJECTIVE:
Select the most proof-critical recent all-depth claims from the handoff.
Independently attack their assumptions, quantifiers, finite-to-infinite
transitions, and dependencies. Use Muse/MiMo per ASTRA_GOAL.md.

If a flaw is found:
- Correct the handoff with precise mathematical reasoning.
- Record the exact correction and why it matters.
- Do NOT claim success unless the correction survives your own adversarial check.

If no flaw is found:
- State which claims you verified and what you checked.
- Do NOT fabricate verifications.

Make no unnecessary large census. Checkpoint and push any substantive correction.

This is an audit round in an unattended supervisor. Time/Context rollover is a
maintenance checkpoint, NOT goal achieved or research blocked.
AUDIT_PROMPT_EOF
  elif [ "${IS_RESET}" = "true" ]; then
    cat > "${PROMPT_FILE}" << RESET_PROMPT_EOF
You are Astra, the lead mathematical researcher for Rule 30 Prize Problem 1.

Read ASTRA_GOAL.md and ASTRA_HANDOFF.md first. Continue from the latest
research/astra-next checkpoint.

STRATEGY RESET ROUND:
The supervisor has detected ${NO_PROGRESS_THRESHOLD} consecutive rounds with no
substantive progress (no theorem, counterexample, no-go result, meaningful
narrowing, or genuinely new route).

Your task:
1. From the current exact bottleneck in the handoff, generate and rank at
   least 3 materially different research routes.
2. For each route, state:
   - What假设 it makes
   - What it would prove if successful
   - How to falsify it cheaply
   - Estimated research cost
3. Attack the most promising route.
4. Update ASTRA_HANDOFF.md with the strategy analysis and your findings.
5. Commit all established progress and push research/astra-next.

This is round ${ROUND} of an unattended supervisor. Time/Context rollover is a
maintenance checkpoint, NOT goal achieved or research blocked.
RESET_PROMPT_EOF
  else
    cat > "${PROMPT_FILE}" << PROMPT_EOF
You are Astra, the lead mathematical researcher for Rule 30 Prize Problem 1.

Read ASTRA_GOAL.md and ASTRA_HANDOFF.md first. Continue from the latest
research/astra-next checkpoint. Do NOT repeat completed work.

Work for approximately ${MINS} minutes on the current bottleneck. When done,
finish your current logical unit, update ASTRA_HANDOFF.md, commit all
established progress, and push research/astra-next.

This is round ${ROUND} of an unattended supervisor. Time/Context rollover is a
maintenance checkpoint, NOT goal achieved or research blocked. Research
continues across sessions.
PROMPT_EOF
  fi

  # ── Launch round in tmux ──
  tmux new-window -t "${SESSION}" -n "r${ROUND}" \
    "bash -c 'cd ${REPO} && timeout --kill-after=30 --signal=SIGINT ${this_timeout} codex exec --model gpt-6-astra -C ${REPO} --dangerously-bypass-approvals-and-sandbox < ${PROMPT_FILE}; echo \$? > ${EXIT_FILE}; touch ${DONE_FILE}; sleep 86400'"

  if [ "${IS_AUDIT}" = "true" ]; then
    log "Round ${ROUND} (AUDIT) live in tmux window r${ROUND}"
  elif [ "${IS_RESET}" = "true" ]; then
    log "Round ${ROUND} (STRATEGY RESET) live in tmux window r${ROUND}"
  else
    log "Round ${ROUND} live in tmux window r${ROUND}"
  fi

  # ── Wait for round completion with stall watchdog ──
  LAST_ACTIVITY=$(usage_mtime)
  STALL_CHECK_ELAPSED=0

  while [ ! -f "${DONE_FILE}" ]; do
    sleep "${STALL_POLL}"

    # -- Context-based rollover check --
    ROLLOVER_NOW=$(date +%s)
    ROLLOVER_CTX=$(get_astra_context_tokens)
    set_rollover_field "tokens" "${ROLLOVER_CTX}"
    ROLLOVER_SOFT_SCALED=$(scale_threshold ${ROLLOVER_SOFT_WARN})
    ROLLOVER_MAND_SCALED=$(scale_threshold ${ROLLOVER_MANDATORY})
    ROLLOVER_HARD_SCALED=$(scale_threshold ${ROLLOVER_HARD_INTERRUPT})
    ROLLOVER_EMRG_SCALED=$(scale_threshold ${ROLLOVER_EMERGENCY_KILL})
    ROLLOVER_CUR_STATE=$(get_rollover_state)
    ROLLOVER_ROUND_WINDOW=$(get_round_window)

    # -- EMERGENCY KILL --
    HARD_GRACE_ELAPSED=false
    if [ "${ROLLOVER_CUR_STATE}" = "HARD_INTERRUPT" ]; then
      ROLLOVER_HARD_TS_CHECK=$(get_rollover_field hard_ts 0)
      if [ "${ROLLOVER_HARD_TS_CHECK}" -gt 0 ] 2>/dev/null; then
        EMRG_CHECK_ELAPSED=$(( ROLLOVER_NOW - ROLLOVER_HARD_TS_CHECK ))
        [ "${EMRG_CHECK_ELAPSED}" -ge "${ROLLOVER_EMERGENCY_GRACE}" ] && HARD_GRACE_ELAPSED=true
      fi
    fi
    if [ "${ROLLOVER_CTX}" -ge "${ROLLOVER_EMRG_SCALED}" ] || [ "${ROLLOVER_CUR_STATE}" = "EMERGENCY_KILL" ] || [ "${HARD_GRACE_ELAPSED}" = "true" ]; then
      if [ "$(get_rollover_field emergency_sent 0)" != "1" ]; then
        ROLLOVER_HARD_TS=$(get_rollover_field hard_ts 0)
        EMRG_GRACE_OK=true
        if [ "${ROLLOVER_HARD_TS}" -gt 0 ] 2>/dev/null; then
          EMRG_ELAPSED=$(( ROLLOVER_NOW - ROLLOVER_HARD_TS ))
          [ "${EMRG_ELAPSED}" -lt "${ROLLOVER_EMERGENCY_GRACE}" ] && EMRG_GRACE_OK=false
        fi
        if [ "$(get_rollover_field hard_sent 0)" != "1" ]; then
          EMRG_GRACE_OK=true
        fi
        if [ "${EMRG_GRACE_OK}" = "true" ]; then
          rollog "Round ${ROUND} ROLLOVER_CTX ${ROLLOVER_CTX}: EMERGENCY KILL"
          set_rollover_state "EMERGENCY_KILL"
          set_rollover_field "emergency_sent" "1"
          set_rollover_field "force_killed" "1"
          if [ -n "${ROLLOVER_ROUND_WINDOW}" ]; then
            PANE_PID=$(tmux display-message -t "${SESSION}:${ROLLOVER_ROUND_WINDOW}" -p "#{pane_pid}" 2>/dev/null) || true
            if [ -n "${PANE_PID}" ]; then
              kill -- -"${PANE_PID}" 2>/dev/null || kill -9 "${PANE_PID}" 2>/dev/null || true
            fi
          fi
          ROLLOVER_CODEX_PID=$(get_round_codex_pid "$(pgrep -f run_astra_supervisor.sh | head -1)")
          if [ -n "${ROLLOVER_CODEX_PID}" ]; then
            kill -9 "${ROLLOVER_CODEX_PID}" 2>/dev/null || true
          fi
          sleep 2
          rollog "Round ${ROUND} emergency kill sent."
        fi
      fi
    fi

    # -- HARD INTERRUPT --
    if [ "${ROLLOVER_CTX}" -ge "${ROLLOVER_HARD_SCALED}" ] || [ "${ROLLOVER_CUR_STATE}" = "HARD_INTERRUPT" ]; then
      if [ "$(get_rollover_field hard_sent 0)" != "1" ] && [ "$(get_rollover_field emergency_sent 0)" != "1" ]; then
        ROLLOVER_MAND_TS=$(get_rollover_field mandatory_ts 0)
        HARD_GRACE_OK=true
        if [ "${ROLLOVER_MAND_TS}" -gt 0 ] 2>/dev/null; then
          HARD_ELAPSED=$(( ROLLOVER_NOW - ROLLOVER_MAND_TS ))
          [ "${HARD_ELAPSED}" -lt "${ROLLOVER_GRACE_PERIOD}" ] && HARD_GRACE_OK=false
        fi
        if [ "${HARD_GRACE_OK}" = "true" ]; then
          rollog "Round ${ROUND} ROLLOVER_CTX ${ROLLOVER_CTX}: HARD INTERRUPT - SIGKILL"
          set_rollover_state "HARD_INTERRUPT"
          set_rollover_field "hard_sent" "1"
          set_rollover_field "hard_ts" "${ROLLOVER_NOW}"
          ROLLOVER_CODEX_PID=$(get_round_codex_pid "$(pgrep -f run_astra_supervisor.sh | head -1)")
          if [ -n "${ROLLOVER_CODEX_PID}" ]; then
            kill -9 "${ROLLOVER_CODEX_PID}" 2>/dev/null || true
          fi
        fi
      fi
    fi

    # -- MANDATORY ROLLOVER REQUEST --
    if [ "${ROLLOVER_CTX}" -ge "${ROLLOVER_MAND_SCALED}" ] || [ "${ROLLOVER_CUR_STATE}" = "ROLLOVER_REQUESTED" ]; then
      if [ "$(get_rollover_field mandatory_sent 0)" != "1" ]; then
        rollog "Round ${ROUND} ROLLOVER_CTX ${ROLLOVER_CTX}: rollover requested"
        set_rollover_state "ROLLOVER_REQUESTED"
        set_rollover_field "mandatory_sent" "1"
        set_rollover_field "mandatory_ts" "${ROLLOVER_NOW}"
        kill -9 "${ROLLOVER_CODEX_PID}" 2>/dev/null || true
      fi
    fi

    # -- SOFT WRAP REQUEST --
    if [ "${ROLLOVER_CTX}" -ge "${ROLLOVER_SOFT_SCALED}" ]; then
      if [ "$(get_rollover_field warn_sent 0)" != "1" ]; then
        rollog "Round ${ROUND} ROLLOVER_CTX ${ROLLOVER_CTX}: soft wrap request"
        set_rollover_state "WRAP_REQUESTED"
        set_rollover_field "warn_sent" "1"
        # NOTE: send_to_round ineffective - codex exec reads from file redirect, not terminal
      fi
    fi

    # ── Stall watchdog ──
    STALL_CHECK_ELAPSED=$(( STALL_CHECK_ELAPSED + STALL_POLL ))
    if [ "${STALL_CHECK_ELAPSED}" -ge "${STALL_TIMEOUT}" ]; then
      CURRENT_ACTIVITY=$(usage_mtime)
      if [ "${CURRENT_ACTIVITY}" -eq "${LAST_ACTIVITY}" ]; then
        # No new API activity for the full stall window
        SUP_PID=$(pgrep -f "run_astra_supervisor.sh" 2>/dev/null | head -1) || true
        CODEX_PID=""
        if [ -n "${SUP_PID}" ]; then
          CODEX_PID=$(get_round_codex_pid "${SUP_PID}")
        fi

        if [ -n "${CODEX_PID}" ]; then
          log "STALL DETECTED: No API activity for ${STALL_TIMEOUT}s. Round ${ROUND} may be stuck."
          log "Sending SIGINT to round ${ROUND} (PID ${CODEX_PID})..."

          # Try graceful termination first
          terminate_round "${CODEX_PID}" "round ${ROUND}"

          # If DONE_FILE appeared, great. If not, wait a bit more.
          sleep 10
          if [ ! -f "${DONE_FILE}" ]; then
            log "Round ${ROUND} still running after SIGINT. Continuing to wait..."
          fi
        fi
        STALL_CHECK_ELAPSED=0
      else
        LAST_ACTIVITY="${CURRENT_ACTIVITY}"
        STALL_CHECK_ELAPSED=0
      fi
    fi

    # ── Draining: check if round exceeded graceful timeout ──
    if [ "${DRAINING}" = "true" ]; then
      ROUND_ELAPSED=$(( $(date +%s) - ROUND_START ))
      if [ "${ROUND_ELAPSED}" -ge "${GRACEFUL_TIMEOUT}" ]; then
        log "Draining timeout (${GRACEFUL_TIMEOUT}s) reached for round ${ROUND}."
        SUP_PID=$(pgrep -f "run_astra_supervisor.sh" 2>/dev/null | head -1) || true
        CODEX_PID=""
        if [ -n "${SUP_PID}" ]; then
          CODEX_PID=$(get_round_codex_pid "${SUP_PID}")
        fi
        if [ -n "${CODEX_PID}" ]; then
          terminate_round "${CODEX_PID}" "round ${ROUND}"
          sleep 10
        fi
      fi
    fi

    # ── Check stop file during round ──
    if [ -f "${STOPFILE}" ]; then
      log "Stop file detected during round ${ROUND}. Waiting for current logical unit to finish..."
      # Don't kill — let the round finish naturally
    fi
  done

  # ── Round finished ──
  EXIT_CODE=$(cat "${EXIT_FILE}" 2>/dev/null || echo "unknown")
  ROUND_END=$(date +%s)
  ROUND_ELAPSED=$(( ROUND_END - ROUND_START ))
  ROLLOVER_FORCE_KILLED=$(get_rollover_field force_killed 0)
  ROLLOVER_FINAL_STATE=$(get_rollover_state)
  if [ "${ROLLOVER_FORCE_KILLED}" = "1" ]; then
    log "Round ${ROUND} FORCE KILLED by rollover (${ROUND_ELAPSED}s, state: ${ROLLOVER_FINAL_STATE})"
    if ! post_rollover_git_safety; then
      rollog "Git unsafe after forced rollover. Entering PAUSED."
    else
      rollog "Git state clean after forced rollover. Continuing."
    fi
  else
    case "${EXIT_CODE}" in
      0)   log "Round ${ROUND} OK (${ROUND_ELAPSED}s)" ;;
      124) log "Round ${ROUND} TIMEOUT (${ROUND_ELAPSED}s)" ;;
      *)   log "Round ${ROUND} exit=${EXIT_CODE} (${ROUND_ELAPSED}s)" ;;
    esac
  fi
  # Reset rollover state for next round
  reset_rollover_state

  # ── Commit and push ──
  cd "${REPO}"
  git push origin "${BRANCH}" >> "${LOGFILE}" 2>&1 || log "Push failed (non-fatal)"

  # ── Classify round outcome ──
  NEW_HASH=$(handoff_hash)
  if [ "${NEW_HASH}" != "${PREV_HANDOFF_HASH}" ] && [ "${PREV_HANDOFF_HASH}" != "none" ]; then
    if [ "${IS_AUDIT}" = "true" ]; then
      log "Audit found correction. Resetting progress counter."
      NO_PROGRESS_COUNT=0
    else
      NO_PROGRESS_COUNT=0
      SUCCESSFUL_ROUNDS=$(( SUCCESSFUL_ROUNDS + 1 ))
      log "Round ${ROUND}: progress detected (${SUCCESSFUL_ROUNDS} successful rounds)"
    fi
  else
    if [ "${IS_AUDIT}" = "true" ]; then
      log "Audit found no correction. Resuming discovery."
    elif [ "${IS_RESET}" = "true" ]; then
      log "Strategy reset round produced no handoff change."
    else
      NO_PROGRESS_COUNT=$(( NO_PROGRESS_COUNT + 1 ))
      log "Round ${ROUND}: no handoff change (${NO_PROGRESS_COUNT}/${NO_PROGRESS_THRESHOLD} toward strategy reset)"
    fi
  fi
  PREV_HANDOFF_HASH="${NEW_HASH}"

  # ── Cleanup ──
  tmux kill-window -t "${SESSION}:r${ROUND}" 2>/dev/null || true
  rm -f "${DONE_FILE}" "${EXIT_FILE}" "${PROMPT_FILE}" 2>/dev/null || true

  # ── If draining, stop after this round ──
  if [ "${DRAINING}" = "true" ]; then
    ELAPSED=$(( $(date +%s) - OVERALL_START ))
    log "========================================"
    log "DRAINING complete. Final round ${ROUND} finished."
    log "${ROUND} rounds in $(( ELAPSED / 3600 ))h $(( (ELAPSED % 3600) / 60 ))m"
    log "========================================"
    break
  fi

  # ── Elapsed update and inter-round pause ──
  ELAPSED=$(( $(date +%s) - OVERALL_START ))
  if [ "${MODE}" = "continuous" ]; then
    log "Elapsed: ${ELAPSED}s (continuous mode)"
  else
    log "Elapsed: ${ELAPSED}s / ${TOTAL_SECONDS}s ($(( ELAPSED * 100 / (TOTAL_SECONDS > 0 ? TOTAL_SECONDS : 1) ))%)"
  fi

  set_state "BETWEEN_ROUNDS"
  [ -f "${STOPFILE}" ] && { log "Stop file detected."; break; }
  sleep "${SLEEP_BETWEEN}"
done

# ── Final cleanup ──
FINAL=$(( $(date +%s) - OVERALL_START ))
set_state "FINISHED"
log "========================================"
log "Done. ${ROUND} rounds in $(( FINAL / 3600 ))h $(( (FINAL % 3600) / 60 ))m"
log "========================================"
rm -f "${DONE_FILE}" "${EXIT_FILE}" "${PROMPT_FILE}" 2>/dev/null || true
tmux kill-session -t "${SESSION}" 2>/dev/null || true
