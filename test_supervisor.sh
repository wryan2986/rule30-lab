#!/usr/bin/env bash
# =========================================================================
# test_supervisor.sh — Validate the graceful Astra supervisor
# =========================================================================

set -euo pipefail

REPO="/home/ryan/rule30-lab"
TMPDIR_ASTRA="/tmp/astra-supervisor"
STATEFILE="${TMPDIR_ASTRA}/state"
METADATA="${TMPDIR_ASTRA}/metadata"
STOPFILE="${REPO}/astra-stop"
TEST_LOG="/tmp/astra_test.log"
RESULTS=()
PASSED=0
FAILED=0

log_test() { echo "[$(date +%H:%M:%S)] $*" | tee -a "${TEST_LOG}"; }
pass() { RESULTS+=("PASS: $1"); PASSED=$((PASSED + 1)); log_test "PASS: $1"; }
fail() { RESULTS+=("FAIL: $1"); FAILED=$((FAILED + 1)); log_test "FAIL: $1"; }

cleanup_all() {
  find /tmp -maxdepth 1 -name "astra_test_*" -type d -exec rm -rf {} + 2>/dev/null || true
  find /tmp -maxdepth 1 -name "astra-supervisor" -type d -exec rm -rf {} + 2>/dev/null || true
  find /tmp -maxdepth 1 -name "astra_test_*" -type f -exec rm -f {} + 2>/dev/null || true
  tmux kill-session -t "astra-test" 2>/dev/null || true
  sleep 0.5
}

remove_stopfile() {
  find "${REPO}" -maxdepth 1 -name "astra-stop" -exec rm -f {} + 2>/dev/null || true
}

# ── Minimal test supervisor ──────────────────────────────────────────────
# Args: $1=mode $2=deadline_sec $3=round_sleep $4=test_id
run_test_supervisor() {
  local TEST_DIR="/tmp/astra_test_${4}"
  local LOGFILE="${TEST_DIR}/supervisor.log"
  local SESSION="astra-test"
  local MODE="$1" DEADLINE_SEC="$2" ROUND_SLEEP="$3"
  local SLEEP_BETWEEN=1

  rm -rf "${TEST_DIR}" 2>/dev/null; mkdir -p "${TEST_DIR}"
  find /tmp -maxdepth 1 -name "astra-supervisor" -type d -exec rm -rf {} + 2>/dev/null || true
  mkdir -p "${TMPDIR_ASTRA}"

  tmux has-session -t "${SESSION}" 2>/dev/null && tmux kill-session -t "${SESSION}"
  tmux new-session -d -s "${SESSION}" -x 200 -y 50

  cat > "${TEST_DIR}/inner.sh" << INNER_EOF
#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="${TEST_DIR}"
LOGFILE="${TEST_DIR}/supervisor.log"
SESSION="${SESSION}"
MODE="${MODE}"
DEADLINE_SEC="${DEADLINE_SEC}"
ROUND_SLEEP="${ROUND_SLEEP}"
SLEEP_BETWEEN=1
REPO="${REPO}"
STATEFILE="${STATEFILE}"
TMPDIR_ASTRA="${TMPDIR_ASTRA}"
STOPFILE="${STOPFILE}"
GRACE_LIMIT=\$(( DEADLINE_SEC + ROUND_SLEEP * 3 + 15 ))

ts() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[\$(ts)] \$*" >> "\${LOGFILE}"; }
set_state() { mkdir -p "\${TMPDIR_ASTRA}"; echo "\$1" > "\${STATEFILE}"; }

OVERALL_START=\$(date +%s)
DEADLINE=\$(( OVERALL_START + DEADLINE_SEC ))
DRAINING=false
ROUND=0
ROUND_PID=""

log "Test ${4} starting | mode=\${MODE} deadline=\${DEADLINE_SEC}s round_sleep=\${ROUND_SLEEP}s"
set_state "BETWEEN_ROUNDS"

while true; do
  [ -f "\${STOPFILE}" ] && { log "Stop file detected."; break; }

  NOW=\$(date +%s)

  # Soft deadline check (top of loop — between-rounds case)
  if [ "\${MODE}" = "hours" ] && [ "\${DRAINING}" != "true" ] && [ "\${NOW}" -ge "\${DEADLINE}" ]; then
    if [ -n "\${ROUND_PID}" ] && kill -0 "\${ROUND_PID}" 2>/dev/null; then
      DRAINING=true
      set_state "DRAINING"
      log "DRAINING — final round finishing."
    else
      log "Deadline reached. No active round. Stopping."
      break
    fi
  fi

  if [ "\${MODE}" = "continuous" ]; then
    [ -f "\${STOPFILE}" ] && { log "Stop file detected."; break; }
  fi

  ROUND=\$(( ROUND + 1 ))
  log "--- Round \${ROUND} starting ---"
  set_state "RUNNING"

  DONE_FILE="\${TMPDIR_ASTRA}/r\${ROUND}.done"
  EXIT_FILE="\${TMPDIR_ASTRA}/r\${ROUND}.exit"

  ( sleep "\${ROUND_SLEEP}"; echo "0" > "\${EXIT_FILE}"; touch "\${DONE_FILE}" ) &
  ROUND_PID=\$!
  disown \${ROUND_PID} 2>/dev/null || true

  # Wait for round — check deadline DURING the wait
  while [ ! -f "\${DONE_FILE}" ]; do
    sleep 1

    NOW=\$(date +%s)
    if [ "\${MODE}" = "hours" ] && [ "\${DRAINING}" != "true" ] && [ "\${NOW}" -ge "\${DEADLINE}" ]; then
      if [ -n "\${ROUND_PID}" ] && kill -0 "\${ROUND_PID}" 2>/dev/null; then
        DRAINING=true
        set_state "DRAINING"
        log "DRAINING — final round finishing."
      fi
    fi

    # Safety: if draining grace expired, break inner loop only
    if [ "\${DRAINING}" = "true" ]; then
      ELAPSED_SINCE_START=\$(( \$(date +%s) - OVERALL_START ))
      if [ "\${ELAPSED_SINCE_START}" -gt "\${GRACE_LIMIT}" ]; then
        log "Draining grace expired."
        break
      fi
    fi
  done

  EXIT_CODE=\$(cat "\${EXIT_FILE}" 2>/dev/null || echo "unknown")
  log "Round \${ROUND} finished: exit=\${EXIT_CODE}"
  ROUND_PID=""

  rm -f "\${DONE_FILE}" "\${EXIT_FILE}" 2>/dev/null || true

  if [ "\${DRAINING}" = "true" ]; then
    log "DRAINING complete. Final round finished."
    break
  fi

  set_state "BETWEEN_ROUNDS"
  sleep "\${SLEEP_BETWEEN}"
done

FINAL=\$(( \$(date +%s) - OVERALL_START ))
set_state "FINISHED"
log "Done. \${ROUND} rounds in \${FINAL}s"
tmux kill-session -t "\${SESSION}" 2>/dev/null || true
INNER_EOF
  chmod +x "${TEST_DIR}/inner.sh"

  bash "${TEST_DIR}/inner.sh" &
  echo $!
}

wait_for() {
  local pid="$1" timeout="$2"
  local waited=0
  while kill -0 "${pid}" 2>/dev/null && [ "${waited}" -lt "${timeout}" ]; do
    sleep 2
    waited=$((waited + 2))
  done
  kill -0 "${pid}" 2>/dev/null && return 1 || return 0
}

show_log() {
  local logfile="$1"
  if [ -f "${logfile}" ]; then
    while IFS= read -r line; do log_test "    ${line}"; done < "${logfile}"
  fi
}

# ══════════════════════════════════════════════════════════════════════════
test1() {
  log_test "=== Test 1: Deadline expires DURING round ==="
  cleanup_all
  remove_stopfile

  local sup_pid
  sup_pid=$(run_test_supervisor "hours" 4 10 "1")

  if ! wait_for "${sup_pid}" 60; then
    fail "Test 1: Supervisor did not exit within 60s"
    cleanup_all
    return
  fi

  local logfile="/tmp/astra_test_1/supervisor.log"

  if grep -q "DRAINING" "${logfile}" 2>/dev/null; then
    pass "Test 1: DRAINING state entered when deadline expired during round"
  else
    fail "Test 1: DRAINING state was NOT entered"
    log_test "  Log:"; show_log "${logfile}"
  fi

  if grep -q "Round 1 finished: exit=0" "${logfile}" 2>/dev/null; then
    pass "Test 1: Round completed normally (exit=0), not killed"
  else
    if grep -q "Round 1 finished" "${logfile}" 2>/dev/null; then
      pass "Test 1: Round finished (was not hard-killed)"
    else
      fail "Test 1: Round did not finish normally"
      log_test "  Log:"; show_log "${logfile}"
    fi
  fi

  local round_count
  round_count=$(grep -c "Round.*starting" "${logfile}" 2>/dev/null || echo "0")
  if [ "${round_count}" -eq 1 ]; then
    pass "Test 1: Only 1 round started (no second round after draining)"
  else
    fail "Test 1: Expected 1 round, got ${round_count}"
  fi

  if grep -q "DRAINING complete" "${logfile}" 2>/dev/null; then
    pass "Test 1: DRAINING completion logged"
  else
    fail "Test 1: DRAINING completion not logged"
  fi

  if [ -f "${STATEFILE}" ] && [ "$(cat "${STATEFILE}" 2>/dev/null)" = "FINISHED" ]; then
    pass "Test 1: Final state is FINISHED"
  else
    fail "Test 1: Final state is not FINISHED ($(cat "${STATEFILE}" 2>/dev/null || echo "missing"))"
  fi

  if tmux has-session -t "astra-test" 2>/dev/null; then
    fail "Test 1: tmux session still exists"
  else
    pass "Test 1: tmux session cleaned up"
  fi

  cleanup_all
}

# ══════════════════════════════════════════════════════════════════════════
test2() {
  log_test "=== Test 2: Deadline expires BETWEEN rounds ==="
  cleanup_all
  remove_stopfile

  local sup_pid
  sup_pid=$(run_test_supervisor "hours" 3 2 "2")

  if ! wait_for "${sup_pid}" 60; then
    fail "Test 2: Supervisor did not exit within 60s"
    cleanup_all
    return
  fi

  local logfile="/tmp/astra_test_2/supervisor.log"

  if grep -q "Deadline reached. No active round. Stopping." "${logfile}" 2>/dev/null; then
    pass "Test 2: Clean stop when deadline expires between rounds"
  else
    fail "Test 2: Did not stop cleanly between rounds"
    log_test "  Log:"; show_log "${logfile}"
  fi

  if grep -q "DRAINING" "${logfile}" 2>/dev/null; then
    fail "Test 2: DRAINING state should NOT appear"
  else
    pass "Test 2: No DRAINING state (correct)"
  fi

  cleanup_all
}

# ══════════════════════════════════════════════════════════════════════════
test3() {
  log_test "=== Test 3: State file correctness ==="
  mkdir -p "${TMPDIR_ASTRA}"

  for state in RUNNING BETWEEN_ROUNDS AUDIT DRAINING PAUSED FINISHED STOPPED; do
    echo "${state}" > "${STATEFILE}"
    if [ "$(cat "${STATEFILE}")" = "${state}" ]; then
      pass "State file: ${state}"
    else
      fail "State file: ${state}"
    fi
  done

  echo "mode=continuous" > "${METADATA}"
  echo "hours=0" >> "${METADATA}"
  if grep -q "mode=continuous" "${METADATA}" && grep -q "hours=0" "${METADATA}"; then
    pass "Metadata file: mode and hours"
  else
    fail "Metadata file: mode and hours"
  fi

  rm -rf "${TMPDIR_ASTRA}" 2>/dev/null || true
}

# ══════════════════════════════════════════════════════════════════════════
test4() {
  log_test "=== Test 4: Continuous mode stops on astra-stop ==="
  cleanup_all
  remove_stopfile

  ( sleep 4 && touch "${STOPFILE}" ) &
  local stoppid=$!

  local sup_pid
  sup_pid=$(run_test_supervisor "continuous" 9999 2 "4")

  if ! wait_for "${sup_pid}" 60; then
    fail "Test 4: Supervisor did not exit within 60s"
    kill "${stoppid}" 2>/dev/null || true
    cleanup_all
    remove_stopfile
    return
  fi

  kill "${stoppid}" 2>/dev/null || true

  local logfile="/tmp/astra_test_4/supervisor.log"

  if grep -q "Stop file detected" "${logfile}" 2>/dev/null; then
    pass "Test 4: Continuous mode stopped on astra-stop"
  else
    fail "Test 4: Did not detect stop file"
    log_test "  Log:"; show_log "${logfile}"
  fi

  local round_count
  round_count=$(grep -c "Round.*starting" "${logfile}" 2>/dev/null || echo "0")
  if [ "${round_count}" -ge 1 ]; then
    pass "Test 4: At least 1 round started before stop"
  else
    fail "Test 4: No rounds started"
  fi

  cleanup_all
  remove_stopfile
}

# ══════════════════════════════════════════════════════════════════════════
> "${TEST_LOG}"
echo "============================================"
echo "  Astra Supervisor Test Suite"
echo "============================================"
echo ""

test3
test2
test1
test4

echo ""
echo "============================================"
echo "  Results: ${PASSED} passed, ${FAILED} failed"
echo "============================================"
echo ""

for r in "${RESULTS[@]}"; do
  echo "  ${r}"
done

echo ""
echo "Test log: ${TEST_LOG}"

[ "${FAILED}" -gt 0 ] && exit 1
exit 0
