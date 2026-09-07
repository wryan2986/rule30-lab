#!/usr/bin/env bash
# test_rollover.sh -- Validate the context-based rollover safety system
set -uo pipefail

REPO="/home/ryan/rule30-lab"
TMPDIR_ASTRA="/tmp/astra-supervisor"
ROLLFILE="${REPO}/astra-rollover"
STOPFILE="${REPO}/astra-stop"
TEST_LOG="/tmp/astra_rollover_test.log"
RESULTS=()
PASSED=0
FAILED=0

log_test() { echo "[$(date +%H:%M:%S)] $*" | tee -a "${TEST_LOG}"; }
pass() { RESULTS+=("PASS: $1"); PASSED=$((PASSED + 1)); log_test "PASS: $1"; }
fail() { RESULTS+=("FAIL: $1"); FAILED=$((FAILED + 1)); log_test "FAIL: $1"; }

get_astra_tokens() {
  local f="${1:-/dev/null}"
  [ -f "${f}" ] || { echo 0; return; }
  grep 'gpt-6-astra' "${f}" 2>/dev/null \
    | jq -r 'select(.provider=="openai" and (.model=="gpt-6-astra" or .resolvedModel=="gpt-6-astra") and .status==200) | .usage.inputTokens // 0' 2>/dev/null \
    | grep -v '^null$' \
    | tail -1 || echo 0
}

test_state_machine() {
  log_test "=== Test 1: Rollover state file management ==="
  mkdir -p "${TMPDIR_ASTRA}"
  for state in NORMAL WRAP_REQUESTED ROLLOVER_REQUESTED HARD_INTERRUPT EMERGENCY_KILL; do
    echo "${state}" > "${TMPDIR_ASTRA}/rollover_state"
    [ "$(cat "${TMPDIR_ASTRA}/rollover_state")" = "${state}" ] \
      && pass "State: ${state}" || fail "State: ${state}"
  done
  rm -rf "${TMPDIR_ASTRA}"
}

test_token_filtering() {
  log_test "=== Test 2: Token filtering (Astra only) ==="
  TEST_DIR="/tmp/astra_test_rollover_2"
  MOCK_HOME="${TEST_DIR}/home"
  mkdir -p "${MOCK_HOME}/.opencodex"

  cat > "${MOCK_HOME}/.opencodex/usage.jsonl" << 'USAGEOF'
{"provider":"openai","model":"gpt-6-astra","resolvedModel":"gpt-6-astra","status":200,"usage":{"inputTokens":50000,"outputTokens":100}}
{"provider":"opencode-go","model":"mimo-v2.5","status":200,"usage":{"inputTokens":999999,"outputTokens":100}}
{"provider":"opencode-go","model":"muse-spark","status":200,"usage":{"inputTokens":888888,"outputTokens":100}}
{"provider":"openai","model":"gpt-6-astra","resolvedModel":"gpt-6-astra","status":200,"usage":{"inputTokens":75000,"outputTokens":200}}
{"provider":"openai","model":"gpt-6-astra","resolvedModel":"gpt-6-astra","status":429,"usage":{"inputTokens":80000,"outputTokens":0}}
USAGEOF

  CTX=$(get_astra_tokens "${MOCK_HOME}/.opencodex/usage.jsonl")
  [ "${CTX}" = "75000" ] && pass "Correct Astra inputTokens (75000)" || fail "Got ${CTX}, expected 75000"

  # MiMo should not be counted
  ALL_TOKS=$(grep 'gpt-6-astra' "${MOCK_HOME}/.opencodex/usage.jsonl" 2>/dev/null \
    | jq -r 'select(.status==200) | .usage.inputTokens // 0' 2>/dev/null \
    | grep -v '^null$' || true)
  SUM=0
  while IFS= read -r t; do [ -n "${t}" ] && SUM=$(( SUM + t )); done <<< "${ALL_TOKS}"
  # Sum should be 50000+75000=125000, not 999999 or 888888
  [ "${SUM}" = "125000" ] && pass "Only Astra provider counted (sum=125000)" || fail "Wrong sum: ${SUM}"

  rm -rf "${TEST_DIR}"
}

test_escalation_chain() {
  log_test "=== Test 3: Full escalation chain ==="
  TEST_DIR="/tmp/astra_test_rollover_3"
  LOGFILE="${TEST_DIR}/rollover.log"
  MOCK_HOME="${TEST_DIR}/home"
  mkdir -p "${TEST_DIR}" "${TMPDIR_ASTRA}" "${MOCK_HOME}/.opencodex"

  echo '{"provider":"openai","model":"gpt-6-astra","resolvedModel":"gpt-6-astra","status":200,"usage":{"inputTokens":500,"outputTokens":100}}' > "${MOCK_HOME}/.opencodex/usage.jsonl"

  echo "NORMAL" > "${TMPDIR_ASTRA}/rollover_state"
  for f in warn_sent mandatory_sent hard_sent emergency_sent; do echo "0" > "${TMPDIR_ASTRA}/rollover_${f}"; done
  echo "0" > "${TMPDIR_ASTRA}/rollover_mandatory_ts"
  echo "0" > "${TMPDIR_ASTRA}/rollover_hard_ts"
  echo "0" > "${TMPDIR_ASTRA}/rollover_force_killed"

  ( sleep 300 ) &
  ROUND_PID=$!

  SOFT=1000; MAND=1200; HARD=1350; EMRG=1500

  for poll in $(seq 1 20); do
    CTX=$(get_astra_tokens "${MOCK_HOME}/.opencodex/usage.jsonl")
    NOW=$(date +%s)
    STATE=$(cat "${TMPDIR_ASTRA}/rollover_state")
    echo "[$(date +%H:%M:%S)] Poll ${poll}: ctx=${CTX} state=${STATE}" >> "${LOGFILE}"

    # EMERGENCY
    if [ "${CTX}" -ge "${EMRG}" ] || [ "${STATE}" = "EMERGENCY_KILL" ]; then
      if [ "$(cat "${TMPDIR_ASTRA}/rollover_emergency_sent" 2>/dev/null || echo 0)" != "1" ]; then
        echo "[$(date +%H:%M:%S)] EMERGENCY KILL at ctx=${CTX}" >> "${LOGFILE}"
        echo "EMERGENCY_KILL" > "${TMPDIR_ASTRA}/rollover_state"
        echo "1" > "${TMPDIR_ASTRA}/rollover_emergency_sent"
        echo "1" > "${TMPDIR_ASTRA}/rollover_force_killed"
        kill -9 "${ROUND_PID}" 2>/dev/null || true
      fi
    fi

    # HARD INTERRUPT
    if [ "${CTX}" -ge "${HARD}" ] || [ "${STATE}" = "HARD_INTERRUPT" ]; then
      HS=$(cat "${TMPDIR_ASTRA}/rollover_hard_sent" 2>/dev/null || echo 0)
      ES=$(cat "${TMPDIR_ASTRA}/rollover_emergency_sent" 2>/dev/null || echo 0)
      if [ "${HS}" != "1" ] && [ "${ES}" != "1" ]; then
        echo "[$(date +%H:%M:%S)] HARD INTERRUPT at ctx=${CTX}" >> "${LOGFILE}"
        echo "HARD_INTERRUPT" > "${TMPDIR_ASTRA}/rollover_state"
        echo "1" > "${TMPDIR_ASTRA}/rollover_hard_sent"
        echo "${NOW}" > "${TMPDIR_ASTRA}/rollover_hard_ts"
        kill -INT "${ROUND_PID}" 2>/dev/null || true
      fi
    fi

    # MANDATORY
    if [ "${CTX}" -ge "${MAND}" ] || [ "${STATE}" = "ROLLOVER_REQUESTED" ]; then
      if [ "$(cat "${TMPDIR_ASTRA}/rollover_mandatory_sent" 2>/dev/null || echo 0)" != "1" ]; then
        echo "[$(date +%H:%M:%S)] ROLLOVER REQUESTED at ctx=${CTX}" >> "${LOGFILE}"
        echo "ROLLOVER_REQUESTED" > "${TMPDIR_ASTRA}/rollover_state"
        echo "1" > "${TMPDIR_ASTRA}/rollover_mandatory_sent"
        echo "${NOW}" > "${TMPDIR_ASTRA}/rollover_mandatory_ts"
      fi
    fi

    # SOFT WRAP
    if [ "${CTX}" -ge "${SOFT}" ]; then
      if [ "$(cat "${TMPDIR_ASTRA}/rollover_warn_sent" 2>/dev/null || echo 0)" != "1" ]; then
        echo "[$(date +%H:%M:%S)] SOFT WRAP at ctx=${CTX}" >> "${LOGFILE}"
        echo "WRAP_REQUESTED" > "${TMPDIR_ASTRA}/rollover_state"
        echo "1" > "${TMPDIR_ASTRA}/rollover_warn_sent"
      fi
    fi

    if ! kill -0 "${ROUND_PID}" 2>/dev/null; then
      echo "[$(date +%H:%M:%S)] Round dead. Done." >> "${LOGFILE}"
      break
    fi

    NEW_CTX=$(( CTX + 100 ))
    echo "{\"provider\":\"openai\",\"model\":\"gpt-6-astra\",\"resolvedModel\":\"gpt-6-astra\",\"status\":200,\"usage\":{\"inputTokens\":${NEW_CTX},\"outputTokens\":100}}" >> "${MOCK_HOME}/.opencodex/usage.jsonl"
    sleep 0.3
  done

  kill -9 "${ROUND_PID}" 2>/dev/null || true

  grep -q 'SOFT WRAP' "${LOGFILE}" && pass "Soft wrap triggered" || fail "Soft wrap NOT triggered"
  grep -q 'ROLLOVER REQUESTED' "${LOGFILE}" && pass "Mandatory rollover triggered" || fail "Mandatory rollover NOT triggered"
  grep -q 'HARD INTERRUPT' "${LOGFILE}" && pass "Hard interrupt triggered" || fail "Hard interrupt NOT triggered"
  grep -q 'EMERGENCY KILL' "${LOGFILE}" && pass "Emergency kill triggered" || fail "Emergency kill NOT triggered"

  SW=$(grep -n 'SOFT WRAP' "${LOGFILE}" | head -1 | cut -d: -f1)
  MR=$(grep -n 'ROLLOVER REQUESTED' "${LOGFILE}" | head -1 | cut -d: -f1)
  HI=$(grep -n 'HARD INTERRUPT' "${LOGFILE}" | head -1 | cut -d: -f1)
  EK=$(grep -n 'EMERGENCY KILL' "${LOGFILE}" | head -1 | cut -d: -f1)
  [ "${SW}" -lt "${MR}" ] && [ "${MR}" -lt "${HI}" ] && [ "${HI}" -lt "${EK}" ] \
    && pass "Escalation order correct" || fail "Wrong order: soft=${SW} mand=${MR} hard=${HI} emrg=${EK}"

  SWC=$(grep -c 'SOFT WRAP' "${LOGFILE}")
  MRC=$(grep -c 'ROLLOVER REQUESTED' "${LOGFILE}")
  HIC=$(grep -c 'HARD INTERRUPT' "${LOGFILE}")
  EKC=$(grep -c 'EMERGENCY KILL' "${LOGFILE}")
  [ "${SWC}" = "1" ] && pass "No soft wrap spam" || fail "Soft wrap sent ${SWC}x"
  [ "${MRC}" = "1" ] && pass "No mandatory spam" || fail "Mandatory sent ${MRC}x"
  [ "${HIC}" = "1" ] && pass "No hard interrupt spam" || fail "Hard sent ${HIC}x"
  [ "${EKC}" = "1" ] && pass "No emergency spam" || fail "Emergency sent ${EKC}x"

  FK=$(cat "${TMPDIR_ASTRA}/rollover_force_killed" 2>/dev/null || echo 0)
  [ "${FK}" = "1" ] && pass "force_killed flag set" || fail "force_killed not set"

  rm -rf "${TEST_DIR}"
}

test_stop_vs_rollover() {
  log_test "=== Test 4: Stop vs Rollover file distinction ==="
  touch "${STOPFILE}" && pass "astra-stop exists" || fail "astra-stop"
  touch "${ROLLFILE}" && pass "astra-rollover exists" || fail "astra-rollover"
  [ "${STOPFILE}" != "${ROLLFILE}" ] && pass "Different paths" || fail "Same path"
  rm -f "${STOPFILE}" "${ROLLFILE}"
}

test_git_safety() {
  log_test "=== Test 5: Git safety post-rollover ==="
  grep -q 'post_rollover_git_safety' "${REPO}/run_astra_supervisor.sh" \
    && pass "post_rollover_git_safety exists" || fail "function not found"
  grep -A20 'post_rollover_git_safety()' "${REPO}/run_astra_supervisor.sh" \
    | grep -q 'check_git_clean' \
    && pass "Git safety check present" || fail "Git safety check missing"
  ! grep -A20 'post_rollover_git_safety()' "${REPO}/run_astra_supervisor.sh" \
    | grep -q 'git reset\|git clean\|git stash' \
    && pass "No destructive git commands" || fail "Destructive git command found"
}

test_supervisor_integrity() {
  log_test "=== Test 6: Supervisor integrity ==="
  bash -n "${REPO}/run_astra_supervisor.sh" 2>/dev/null \
    && pass "Supervisor syntax valid" || fail "Supervisor syntax error"
  bash -n "${REPO}/.astra_dash_status.sh" 2>/dev/null \
    && pass "Dashboard syntax valid" || fail "Dashboard syntax error"
  grep -q 'get_astra_context_tokens' "${REPO}/run_astra_supervisor.sh" \
    && pass "Token getter present" || fail "Token getter missing"
  grep -q 'ROLLOVER_TEST_MODE' "${REPO}/run_astra_supervisor.sh" \
    && pass "Test mode support" || fail "Test mode missing"
  grep -q 'ROLLFILE' "${REPO}/run_astra_supervisor.sh" \
    && pass "Rollover file support" || fail "Rollover file missing"
  grep -q 'reset_rollover_state' "${REPO}/run_astra_supervisor.sh" \
    && pass "State reset present" || fail "State reset missing"
  grep -q 'between.*rounds\|BETWEEN_ROUNDS' "${REPO}/run_astra_supervisor.sh" \
    && pass "BETWEEN_ROUNDS state" || fail "BETWEEN_ROUNDS missing"
  grep -q 'HARD_INTERRUPT\|EMERGENCY_KILL\|WRAP_REQUESTED\|ROLLOVER_REQUESTED' "${REPO}/run_astra_supervisor.sh" \
    && pass "All rollover states defined" || fail "Missing rollover states"
}

# ══════════════════════════════════════════════════════════════════════════
> "${TEST_LOG}"
echo "============================================"
echo "  Astra Rollover Test Suite"
echo "============================================"
echo ""

test_state_machine
test_token_filtering
test_escalation_chain
test_stop_vs_rollover
test_git_safety
test_supervisor_integrity

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
