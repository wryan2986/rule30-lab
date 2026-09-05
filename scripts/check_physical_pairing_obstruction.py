#!/usr/bin/env python3
"""Physical realizability of the named Hamming obstruction (Problem 1).

ADMISSION (bounded exact search; lead owns theorem and integration).
Target: x=0x642fdfb in O_(u,14), bitlen 27, forced schedule tutututu.
By the membership lemma, X_n=T^n(S)>>n lies in O_(a,k) with k=ceil((s+n)/2)
and phase u iff s+n is odd. For the named target this forces s+n=27; with
n>=s this gives s<=13 and n=27-s. Search EXACTLY all 4096 odd S with s<=13
at n=27-s and record every hit with coupled trace witnesses. Either outcome
bears on physical-subfamily invariants (whether a physical-only single-bit
pairing route survives domain restriction), not on first-witness period
boxes. A hit refutes bare physical exclusion but its alternation behavior
is assessed separately in this same record. No hit is an exact named
nonrealizability claim in the n>=s regime only, never a universal no-go and
never an infinite statement. No bound is increased and no other state is
searched. One local CPU, 120s wall, 1GiB address space.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, resource, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
TARGET_X = 0x642fdfb
TARGET_PHASE = "u"
TARGET_K = 14
TARGET_SUM = 27
S_MAX_BITS = 13
TARGET_SCHEDULE = "tutututu"
TIME_BUDGET_SECONDS = 120.0
MEMORY_BUDGET_KIB = 1024 * 1024
RESULT_FILENAME = "20260905_physical_pairing_obstruction.json"
ROOT = Path(__file__).resolve().parents[1]
TEST_RELATIVE = "tests/python/test_physical_pairing_obstruction.py"
HYPOTHESIS = ("The named state 0x642fdfb is not physically realizable as "
 "X=T^n(S)>>n for any odd positive finite seed S with s=bitlen(S)<=13 at "
 "n=27-s (the n>=s regime forced by the membership lemma).")
class PhysicalLimitError(RuntimeError):
    pass
def T_packed(state):
    return state ^ ((state << 1) | (state << 2))
def T_cellarray(state, width):
    if state < 0:
        raise ValueError("state must be nonnegative")
    bits = [(state >> j) & 1 for j in range(width)]
    out = 0
    for j in range(width):
        xj = bits[j]
        lo1 = bits[j - 1] if j >= 1 else 0
        lo2 = bits[j - 2] if j >= 2 else 0
        if xj ^ (lo1 | lo2):
            out |= 1 << j
    return out
def iterate_packed(seed, steps):
    trajectory = [seed]
    for _ in range(steps):
        trajectory.append(T_packed(trajectory[-1]))
    return trajectory
def center_bits(trajectory, times):
    return [(trajectory[t] >> t) & 1 for t in times]
def U_map(x):
    return T_packed(x) ^ 1
def P_map(x):
    return T_packed(x) ^ 1 ^ (2 if x & 1 == 0 else 0)
def forced_branch(word):
    return {"t": T_packed, "u": U_map}[word]
def assess_hit(seed, s, n):
    blocks = len(TARGET_SCHEDULE)
    last_time = n + 2 * blocks + 1
    traj = iterate_packed(seed, last_time)
    if traj[n] >> n != TARGET_X:
        return None
    width = s + 2 * last_time + 2
    independent = seed
    for time_index in range(last_time + 1):
        if independent != traj[time_index]:
            raise PhysicalLimitError("cell-array disagrees on hit trajectory")
        independent = T_cellarray(independent, width)
    centers = center_bits(traj, range(n, last_time + 1))
    alternating = all(bit == 1 - j % 2 for j, bit in enumerate(centers))
    halfrows = [traj[n + 2*j] >> (n + 2*j) for j in range(blocks + 1)]
    steps = []
    for j, letter in enumerate(TARGET_SCHEDULE):
        physical_time = n + 2*j
        right1 = (traj[physical_time] >> (physical_time - 1)) & 1
        right2 = ((traj[physical_time] >> (physical_time - 2)) & 1
                  if physical_time >= 2 else 0)
        fringe_b = 1 ^ (right1 | right2)
        residue = halfrows[j] & 15
        branch_ok = letter == {7: "u", 11: "t"}.get(residue)
        predicted = forced_branch(letter)(P_map(halfrows[j] >> 2))
        steps.append({"row": j, "halfrow_hex": hex(halfrows[j]),
            "next_halfrow_hex": hex(halfrows[j+1]),
            "residue_mod16": residue, "branch": letter, "b": fringe_b,
            "branch_ok": branch_ok,
            "physical_branch_match": fringe_b == int(letter == "u"),
            "halfrow_step_match": predicted == halfrows[j+1]})
    coupled = alternating and all(row["branch_ok"] and
        row["physical_branch_match"] and row["halfrow_step_match"] for row in steps)
    return {"seed_hex": hex(seed), "s": s, "n": n,
        "cellarray_confirmed": True,
        "centers": "".join(str(bit) for bit in centers),
        "alternating_from_1": alternating, "coupled_halfrows": coupled,
        "schedule_match": all(row["branch_ok"] for row in steps), "rows": steps}
def run_campaign(check_time=True, enforcement=None):
    t0 = time.monotonic()
    assert TARGET_X.bit_length() == TARGET_SUM
    assert TARGET_X & 1 == 1
    per_width = []
    hits = []
    total = 0
    cross = 0
    for s_try in (1, 5, 13):
        for seed in (2 ** (s_try - 1) + 1, 2 ** s_try - 1):
            w = seed.bit_length() + 4
            if T_cellarray(seed, w) != T_packed(seed):
                raise PhysicalLimitError("cell-array disagrees on sample")
            cross += 1
    for s in range(1, S_MAX_BITS + 1):
        n = TARGET_SUM - s
        count = 0
        lo = 1 if s == 1 else 2 ** (s - 1) + 1
        width_count = 0
        for seed in range(lo, 2 ** s, 2):
            if check_time and time.monotonic() - t0 > TIME_BUDGET_SECONDS:
                raise PhysicalLimitError("time budget exceeded in seed scan")
            if seed & 1 == 0 or seed.bit_length() != s:
                raise PhysicalLimitError("seed outside odd width class")
            total += 1
            width_count += 1
            traj = iterate_packed(seed, n)
            if traj[n] >> n == TARGET_X:
                hit = assess_hit(seed, s, n)
                if hit is None:
                    raise PhysicalLimitError("hit lost on reassessment")
                hits.append(hit)
                count += 1
        per_width.append({"s": s, "n": n, "seeds": width_count, "hits": count})
    if total != 4096:
        raise PhysicalLimitError("seed count changed: %d" % total)
    runtime = time.monotonic() - t0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {"target_hex": hex(TARGET_X), "target_sum": TARGET_SUM,
     "s_max": S_MAX_BITS, "seeds_enumerated": total,
     "per_width": per_width, "hits": hits, "hit_count": len(hits),
     "cross_checks": cross, "order": ["s ascending", "seed ascending"],
     "stopping": "full enumeration of all 4096; no bound increase"}
    canon = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    gs = git_strict(["status", "--short"])
    if enforcement is None:
        enforcement = {"address_space_limit_applied": False,
         "reason": "no CLI enforcement record passed (library call)",
         "deadline": "cooperative monotonic budget checks when check_time is true"}
    payload = {"experiment_id": "physical-pairing-obstruction",
     "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
     "git_commit": git_strict(["rev-parse", "HEAD"]),
     "git_branch": git_strict(["branch", "--show-current"]),
     "git_status": gs, "git_dirty": bool(gs.strip()), "worktree": str(ROOT),
     "source_hashes": {"analyzer_sha256": sha256_file(Path(__file__).resolve())},
     "question": "problem1", "hypothesis": HYPOTHESIS, "backend": "python-packed-and-cellarray",
     "parameters": {"target_hex": hex(TARGET_X), "target_sum": TARGET_SUM,
      "s_max": S_MAX_BITS, "seeds": 4096, "schedule": TARGET_SCHEDULE,
      "time_budget_seconds": TIME_BUDGET_SECONDS, "memory_budget_kib": MEMORY_BUDGET_KIB},
     "sources": ["proofs/informal/problem1_three_return_boundary_sufficiency.md",
      "proofs/informal/problem1_signed_belief_pairing_obstruction.md"],
     "enforcement": enforcement, "hardware": hardware_facts(),
     "software": {"python_version": platform.python_version(),
      "python_implementation": platform.python_implementation(), "os": platform.platform()},
     "runtime_seconds": runtime, "peak_rss_kib": peak, "result": result,
     "result_hashes": {"certificate_sha256": hashlib.sha256(canon).hexdigest()},
     "result_summary": {"seeds_enumerated": total, "hit_count": len(hits)},
     "interpretation": ("No hit is exact named nonrealizability in the n>=s regime "
      "only, never a universal no-go. A hit refutes bare physical exclusion; its "
      "alternation and schedule behavior are assessed separately in the record."),
     "status": "refuted" if hits else "finite-exhaustive",
     "proof_scope": "exact enumeration of all 4096 odd seeds s<=13 at n=27-s",
     "limitations": ["n>=s regime only; other regimes and states not searched",
      "single local process; cooperative 120s wall budget plus outer timeout; 1GiB cap in CLI runs",
      "finite enumeration only; no infinite conclusion"]}
    try:
        payload["source_hashes"]["test_sha256"] = sha256_file(ROOT / TEST_RELATIVE)
    except OSError:
        pass
    return payload
def git_strict(args):
    import subprocess as sp
    c = sp.run(["git", "-C", str(ROOT)] + args, capture_output=True, text=True, timeout=30)
    if c.returncode != 0:
        raise PhysicalLimitError("git failed: " + c.stderr.strip())
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
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=str, default=None)
    a = ap.parse_args()
    enforcement = apply_address_space_limit()
    if not enforcement["address_space_limit_applied"]:
        raise PhysicalLimitError("could not enforce the address-space cap")
    import signal as _sig
    def _alarm(signum, frame):
        raise PhysicalLimitError("wall-clock alarm: 115s budget reached")
    _sig.signal(_sig.SIGALRM, _alarm)
    enforcement["alarm_seconds"] = 115
    enforcement["deadline"] = "SIGALRM at 115s plus cooperative checks plus outer timeout"
    _sig.alarm(115)
    try:
        payload = run_campaign(True, enforcement)
    finally:
        _sig.alarm(0)
    dest = Path(a.output) if a.output else ROOT / "results/problem1" / RESULT_FILENAME
    res = dest.resolve()
    if not res.is_relative_to(ROOT):
        raise PhysicalLimitError("output outside worktree")
    write_record_atomic(payload, res)
    print(json.dumps(payload, indent=2, sort_keys=True))
if __name__ == "__main__":
    main()
