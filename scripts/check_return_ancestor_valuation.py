#!/usr/bin/env python3
"""Restricted valuation gate on phase-u gap-222 ancestors through k18.

ADMISSION (bounded falsification on an already-studied box; lead owns meaning).
Box: phase-u gap-222 occurrences through k<=18 (historical box, no expansion):
observed word E=ututut, admissibility of wE+u avoiding uu, ttttt, ututtu, all
cuts, depth L=cut+1<k. Ancestor closure strips j=0..L-1 digits (L>=1 kept).
Observable on EVERY ancestor node: v2(N)!=v2(2O) with N=E+O total endpoints
(E/O even/odd-defect counts computed separately and asserted). Nodes sorted
by (k,L,x); stop at the first gate failure, N=0 included. Either outcome
bears on the genuine three-return ancestor invariant: a verified failure
refutes that all-depth conjecture; passage is finite evidence
for structural analysis, never an infinite claim and never a period-box claim.
No bound is increased. One local CPU, 120s wall, 1GiB address space.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, resource, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
PHASE = "u"
DOMAIN_MAX_K = 18
GAP_WORD = "ututut"
FORBIDDEN = ("uu", "ttttt", "ututtu")
ALLOWED_MASKS = (0, 3, 11, 12, 15)
SCHEDULE_CAP = 64
ORACLE_K = 8
TIME_BUDGET_SECONDS = 120.0
MEMORY_BUDGET_KIB = 1024 * 1024
RESULT_FILENAME = "20260905_return_ancestor_valuation.json"
ROOT = Path(__file__).resolve().parents[1]
TEST_RELATIVE = "tests/python/test_return_ancestor_valuation.py"
LIFT_MODULE_RELATIVE = "experiments/problem1_nonperiodicity/analyze_period_two_phase_frontier_lift_recursion.py"
HYPOTHESIS = ("Every ancestor (positive depth) of every admissible phase-u "
 "gap-222 three-return cylinder through k<=18 satisfies v2(N)!=v2(2O) with "
 "N=E+O total distinct dominant endpoints.")
class ValuationLimitError(RuntimeError):
    pass
class SeparationViolationError(RuntimeError):
    pass
class OracleMismatchError(RuntimeError):
    pass
def forward_generator(name, state):
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError(name)
def frontier_children_primary(state):
    return tuple(sorted({forward_generator(n, state) for n in "tup"}))
def oracle_frontier_children(state):
    if state <= 0:
        raise ValueError("oracle states are positive")
    width = state.bit_length() + 2
    bits = [(state >> j) & 1 for j in range(width)]
    tout = 0
    for j in range(width):
        lo1 = bits[j - 1] if j >= 1 else 0
        lo2 = bits[j - 2] if j >= 2 else 0
        if bits[j] ^ (lo1 | lo2):
            tout |= 1 << j
    uout = tout ^ 0b1
    pbit0 = ((tout & 1) ^ 1)
    pbit1 = ((tout >> 1) & 1) ^ (1 if (state & 1) == 0 else 0)
    pout = (tout & ~0b11) ^ pbit0 ^ (pbit1 << 1)
    return tuple(sorted({tout, uout, pout}))
def build_levels(maximum_complexity, childfn):
    levels = [set(), {1}]
    for _ in range(2, maximum_complexity + 1):
        levels.append({c for s in levels[-1] for c in childfn(s)})
    return levels
def fiber_mask(levels, complexity, quotient):
    mask = sum(1 << d for d in range(4) if 4 * quotient + d in levels[complexity + 1])
    if mask not in ALLOWED_MASKS:
        raise AssertionError("fiber escaped five-mask alphabet")
    return mask
def mask_sequence(levels, complexity, state, depth):
    out = []
    for step in range(depth):
        q = state >> 2
        out.append(fiber_mask(levels, complexity - 1 - step, q))
        state = q
    return tuple(out)
def dominates(current, shadow):
    return len(current) == len(shadow) and all(not (a & ~b) for a, b in zip(current, shadow))
def defect_count(shadow):
    return sum(m != 0b1111 for m in shadow)
def belief_direct(levels, complexity, current, depth):
    if depth >= complexity - 1:
        mod = 4 ** depth
        res = current % mod
        wit = sorted(s for s in levels[complexity - 1] if s % mod == res)
        if wit:
            raise SeparationViolationError("separation violated")
        return {}
    mod = 4 ** depth
    res = current % mod
    cur = mask_sequence(levels, complexity, current, depth)
    out = {}
    for sh in levels[complexity - 1]:
        if sh % mod != res:
            continue
        sm = mask_sequence(levels, complexity - 1, sh, depth)
        if dominates(cur, sm):
            out[sh] = defect_count(sm)
    return out
def belief_recursive(levels, complexity, current, depth):
    if not 1 <= depth <= complexity - 2:
        raise ValuationLimitError("recursive belief needs 1<=L<=k-2")
    digit = current & 3
    quotient = current >> 2
    cmask = fiber_mask(levels, complexity - 1, quotient)
    if depth == 1:
        out = {}
        for sh in levels[complexity - 1]:
            if sh & 3 != digit:
                continue
            sm = fiber_mask(levels, complexity - 2, sh >> 2)
            if not (cmask & ~sm):
                out[sh] = int(sm != 0b1111)
        return out
    lower = belief_recursive(levels, complexity - 1, quotient, depth - 1)
    tgt = levels[complexity - 1]
    out = {}
    for sq, lc in lower.items():
        sh = 4 * sq + digit
        if sh not in tgt:
            continue
        sm = fiber_mask(levels, complexity - 2, sq)
        if cmask & ~sm:
            continue
        out[sh] = lc + int(sm != 0b1111)
    return out
def forced_zero_schedule(state, cap=SCHEDULE_CAP):
    word = []
    for _ in range(cap):
        res = state & 15
        if res == 7:
            br = "u"
        elif res == 11:
            br = "t"
        else:
            return "".join(word)
        state = forward_generator(br, forward_generator("p", (state - 3) >> 2))
        word.append(br)
    raise ValuationLimitError("schedule cap reached")
def admissible(word):
    return not any(f in word for f in FORBIDDEN)
def v2(x):
    return None if x == 0 else (x & -x).bit_length() - 1
def gate(N, O):
    a, b = v2(N), v2(2 * O)
    if a is None or b is None:
        return (a is None) != (b is None)
    return a != b
def gate_arith_selftest():
    cases = [((2, 1, True)), ((1, 1, False)), ((1, 3, True)), ((3, 5, True)), ((1, 5, False)), ((1, 0, True)), ((0, 0, False))]
    for E, O, want in cases:
        if gate(E + O, O) != want:
            raise OracleMismatchError("gate arithmetic changed")
    return len(cases)
def load_lift_module():
    import importlib.util
    path = ROOT / LIFT_MODULE_RELATIVE
    spec = importlib.util.spec_from_file_location("lift_recursion_member", path)
    if spec is None or spec.loader is None:
        raise ValuationLimitError("lift module unavailable")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
def gap222_occurrences(levels, maxK, cap, t0, check_time):
    occ = []
    truncated = 0
    excluded = 0
    for k in range(2, maxK + 1):
        for cur in sorted(levels[k]):
            if cur & 3 != 3:
                continue
            try:
                sched = forced_zero_schedule(cur, cap)
            except ValuationLimitError:
                truncated += 1
                continue
            for cut in range(len(sched) + 1):
                if sched[cut:cut + 6] != GAP_WORD:
                    continue
                if not admissible(sched[:cut] + GAP_WORD + "u"):
                    continue
                L = cut + 1
                if not L < k:
                    excluded += 1
                    continue
                if check_time and time.monotonic() - t0 > TIME_BUDGET_SECONDS:
                    raise ValuationLimitError("time budget exceeded in occurrence scan")
                occ.append((k, cur, cut, L, sched))
    return occ, truncated, excluded
def ancestor_closure(occ):
    nodes = {}
    for k, x, cut, L, sched in occ:
        for j in range(L):
            key = (k - j, x >> (2 * j), L - j)
            if key not in nodes:
                nodes[key] = (k, x, cut, L, sched)
    return nodes
def node_record(levels, k, x, L):
    if x not in levels[k]:
        raise OracleMismatchError("ancestor outside its claimed frontier")
    bel = belief_direct(levels, k, x, L)
    rec = None
    if 1 <= L <= k - 2:
        rec = belief_recursive(levels, k, x, L)
        if bel != rec:
            raise OracleMismatchError("direct/recursive disagree at k=%d x=%s" % (k, hex(x)))
    E = sum(1 for c in bel.values() if c % 2 == 0)
    O = sum(1 for c in bel.values() if c % 2 == 1)
    N = E + O
    if N != len(bel):
        raise OracleMismatchError("N mismatch")
    hist = {}
    for c in bel.values():
        hist[str(c)] = hist.get(str(c), 0) + 1
    em = {m: 0 for m in ALLOWED_MASKS}
    om = {m: 0 for m in ALLOWED_MASKS}
    for y, c in bel.items():
        n = fiber_mask(levels, k - 1, y)
        if c % 2 == 0:
            em[n] += 1
        else:
            om[n] += 1
    return {"complexity": k, "state_hex": hex(x), "depth": L,
     "endpoints": N, "E": E, "O": O, "signed_mass": E - O,
     "valuations": [v2(N), v2(2 * O)], "gate_pass": gate(N, O),
     "recursive_checked": rec is not None,
     "defect_histogram": hist,
     "outgoing_E": [em[m] for m in ALLOWED_MASKS],
     "outgoing_O": [om[m] for m in ALLOWED_MASKS]}
def git_strict(args):
    import subprocess as sp
    c = sp.run(["git", "-C", str(ROOT)] + args, capture_output=True, text=True, timeout=30)
    if c.returncode != 0:
        raise ValuationLimitError("git failed: " + c.stderr.strip())
    return c.stdout.strip()
def sha256_file(path):
    import hashlib as hl
    h = hl.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(65536), b""):
            h.update(ch)
    return h.hexdigest()
def hardware_facts():
    model, total = None, None
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    model = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    total = int(line.split()[1])
                    break
    except (OSError, ValueError):
        pass
    return {"cpu_model": model, "cpu_count": os.cpu_count(), "memory_total_kib": total, "architecture": platform.machine()}
def write_record_atomic(payload, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    enc = json.dumps(payload, indent=2, sort_keys=True).encode()
    with tempfile.NamedTemporaryFile(dir=str(dest.parent), delete=False) as h:
        h.write(enc)
        h.flush()
        os.fsync(h.fileno())
        tmp = h.name
    os.replace(tmp, dest)
    return dest
def apply_address_space_limit():
    budget = MEMORY_BUDGET_KIB * 1024
    rec = {"budget_bytes": budget}
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    except (OSError, ValueError) as exc:
        rec["address_space_limit_applied"] = False
        rec["reason"] = "getrlimit failed: %s" % exc
        return rec
    target = budget
    if hard != resource.RLIM_INFINITY and hard < budget:
        target = hard
    try:
        resource.setrlimit(resource.RLIMIT_AS, (target, hard))
    except (OSError, ValueError) as exc:
        rec["address_space_limit_applied"] = False
        rec["reason"] = "setrlimit failed: %s" % exc
        return rec
    rec["address_space_limit_applied"] = True
    rec["soft_bytes"] = target
    return rec
def run_campaign(dmax=DOMAIN_MAX_K, cap=SCHEDULE_CAP, check_time=True, enforcement=None):
    t0 = time.monotonic()
    if not 2 <= dmax <= 18:
        raise ValuationLimitError("domain cap outside 2..18")
    if not 1 <= cap <= 64:
        raise ValuationLimitError("schedule cap outside 1..64")
    narith = gate_arith_selftest()
    lift_mod = load_lift_module()
    levels = build_levels(dmax, frontier_children_primary)
    oracle_checked = 0
    oc = build_levels(min(ORACLE_K, dmax), oracle_frontier_children)
    for k in range(1, min(ORACLE_K, dmax) + 1):
        if oc[k] != levels[k]:
            raise OracleMismatchError("oracle disagrees at k=%d" % k)
        oracle_checked += len(levels[k])
    halt_reason = None
    complete = True
    occ, truncated, excluded = [], 0, 0
    nodes = {}
    rows = []
    first_failure = None
    ancestry = None
    try:
        occ, truncated, excluded = gap222_occurrences(levels, dmax, cap, t0, check_time)
        if truncated:
            complete = False
            halt_reason = "%d schedule(s) hit the cap: box unresolved" % truncated
        nodes = ancestor_closure(occ)
        for key in sorted(nodes, key=lambda e: (e[0], e[2], e[1])):
            if check_time and time.monotonic() - t0 > TIME_BUDGET_SECONDS:
                raise ValuationLimitError("time budget exceeded in node scan")
            k, x, L = key
            rec = node_record(levels, k, x, L)
            rows.append(rec)
            if not rec["gate_pass"]:
                ok, ox, ocut, oL, osched = nodes[key]
                wit = lift_mod.frontier_witness(PHASE, ok, ox)
                if wit is None or lift_mod.apply_word(wit) != ox:
                    raise OracleMismatchError("lift witness failed ancestry replay")
                stripped = ok - k
                if stripped != oL - L or ox >> (2 * stripped) != x:
                    raise OracleMismatchError("ancestry depth/complexity/quotient mismatch")
                ancestry = {"occurrence_k": ok, "occurrence_hex": hex(ox),
                 "occurrence_L": oL, "cut": ocut, "gaps": [2, 2, 2],
                 "forced_word": osched, "word_E_plus_u": osched[:ocut] + GAP_WORD + "u",
                 "generator_witness": wit, "stripped_digits": stripped}
                first_failure = rec
                break
    except (ValuationLimitError, SeparationViolationError) as exc:
        complete = False
        halt_reason = str(exc) if halt_reason is None else halt_reason + "; " + str(exc)
    runtime = time.monotonic() - t0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    tested = len(rows)
    if first_failure is not None:
        status = "refuted"
    elif complete:
        status = "finite-exhaustive"
    else:
        status = "inconclusive"
    result = {"occurrences": len(occ), "ancestors": len(nodes) if complete or nodes else 0,
     "tested": tested, "truncated_schedules": truncated, "excluded_depth_ge_k": excluded,
     "oracle_states_compared": oracle_checked, "arith_selftest": narith,
     "rows": rows, "first_failure": first_failure, "ancestry": ancestry,
     "completed_through_cap": complete and first_failure is None,
     "occurrence_domain_complete": complete,
     "valuation_search_exhausted": complete and first_failure is None and tested == len(nodes),
     "halt_reason": halt_reason, "order": ["k", "L", "x"],
     "stopping": "first gate failure or cap-18 end; no cap increase"}
    canon = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    gs = git_strict(["status", "--short"])
    if enforcement is None:
        enforcement = {"address_space_limit_applied": False,
         "reason": "no CLI enforcement record passed (library call)",
         "deadline": "cooperative monotonic budget checks when check_time is true"}
    payload = {"experiment_id": "return-ancestor-valuation",
     "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
     "git_commit": git_strict(["rev-parse", "HEAD"]),
     "git_branch": git_strict(["branch", "--show-current"]),
     "git_status": gs, "git_dirty": bool(gs.strip()), "worktree": str(ROOT),
     "source_hashes": {"analyzer_sha256": sha256_file(Path(__file__).resolve()),
      "lift_module_sha256": sha256_file(ROOT / LIFT_MODULE_RELATIVE)},
     "question": "problem1", "hypothesis": HYPOTHESIS, "backend": "python-direct-and-recursive",
     "parameters": {"phase": PHASE, "domain_max_k": dmax, "gap_word": GAP_WORD,
      "schedule_cap": cap, "time_budget_seconds": TIME_BUDGET_SECONDS,
      "memory_budget_kib": MEMORY_BUDGET_KIB},
     "enforcement": enforcement, "hardware": hardware_facts(),
     "software": {"python_version": platform.python_version(),
      "python_implementation": platform.python_implementation(), "os": platform.platform()},
     "runtime_seconds": runtime, "peak_rss_kib": peak, "result": result,
     "result_hashes": {"certificate_sha256": hashlib.sha256(canon).hexdigest()},
     "result_summary": {"occurrences": len(occ), "tested": tested,
      "failure_found": first_failure is not None,
      "occurrence_domain_complete": complete},
     "interpretation": ("A verified ancestor counterexample refutes the all-depth ancestor "
      "valuation conjecture. An ancestor failure alone does not settle the "
      "occurrence-only version. Passage through the cap is "
      "finite evidence for structural analysis, never an infinite claim."),
     "status": status,
     "proof_scope": "phase-u gap-222 ancestors 2<=k<=%d; no wider claim" % dmax,
     "limitations": ["finite historical box; no all-depth nonvanishing or periodicity theorem",
      "single local process; cooperative 120s wall budget plus outer timeout; 1GiB cap in CLI runs",
      "L>=k occurrences excluded by domain definition, counted not successes",
      "cap truncations force inconclusive, never exhaustive",
      "v2(0) treated as infinite per stated convention"]}
    try:
        payload["source_hashes"]["test_sha256"] = sha256_file(ROOT / TEST_RELATIVE)
    except OSError:
        pass
    return payload
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain-max", type=int, default=DOMAIN_MAX_K)
    ap.add_argument("--schedule-cap", type=int, default=SCHEDULE_CAP)
    ap.add_argument("--output", type=str, default=None)
    a = ap.parse_args()
    enforcement = apply_address_space_limit()
    if not enforcement["address_space_limit_applied"]:
        raise ValuationLimitError("could not enforce the address-space cap")
    import signal as _sig
    def _alarm(signum, frame):
        raise ValuationLimitError("wall-clock alarm: 115s budget reached")
    _sig.signal(_sig.SIGALRM, _alarm)
    enforcement["alarm_seconds"] = 115
    enforcement["deadline"] = "SIGALRM at 115s plus cooperative checks plus outer timeout"
    _sig.alarm(115)
    try:
        payload = run_campaign(a.domain_max, a.schedule_cap, True, enforcement)
    finally:
        _sig.alarm(0)
    dest = Path(a.output) if a.output else ROOT / "results/problem1" / RESULT_FILENAME
    res = dest.resolve()
    if not res.is_relative_to(ROOT):
        raise ValuationLimitError("output outside worktree")
    write_record_atomic(payload, res)
    print(json.dumps(payload, indent=2, sort_keys=True))
if __name__ == "__main__":
    main()
