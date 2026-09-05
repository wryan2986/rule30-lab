#!/usr/bin/env python3
"""Replay two named slice vectors and test their three-return ancestry.

Admission and fixed limits: problem1_signed_slice_convex_obstruction.md.
No frontier census beyond the existing complexity-18 vector checks.
"""
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
MASKS = (0, 3, 11, 12, 15)
SOURCES = (
    Path(__file__).relative_to(ROOT),
    Path("scripts/check_three_return_signed_mass_independent.py"),
    Path("experiments/problem1_nonperiodicity/analyze_period_two_phase_frontier_lift_recursion.py"),
    Path("src/python/rule30_research_reference.py"),
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    started = time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
    signal.alarm(120)
    oracle = load("convex_oracle", SOURCES[1])
    lift = load("convex_lift", SOURCES[2])
    # Hand cases, then independent Boolean and packed implementations.
    assert oracle.gen_t(1) == 7 and oracle.gen_u(1) == 6
    assert oracle.gen_t(3) == 13
    for x in range(1, 256):
        assert oracle.gen_t(x) == oracle.gen_t_bitwise(x)
    small = oracle.build_frontiers("u", 6)
    assert [len(small[k]) for k in range(1, 6)] == [1, 2, 4, 9, 18]
    small_checks = 0
    for k in range(2, 7):
        for x in small[k]:
            assert lift.frontier_member("u", k, x)
            for depth in range(1, k):
                assert oracle.belief_direct(small, k, x, depth, []) == oracle.belief_recursive(small, k, x, depth, [])
                small_checks += 1
    levels = oracle.build_frontiers("u", 18)
    rows = []
    for x, depth, expected in (
        (0x642E4D2F1, 3, (262, 0, 200, 27, 117)),
        (0x6473D46AB, 5, (3, 0, 5, 0, 7)),
    ):
        k = 18
        assert x in levels[k]
        parent = oracle.belief_direct(levels, k - 1, x >> 2, depth - 1, [])
        assert parent == oracle.belief_recursive(levels, k - 1, x >> 2, depth - 1, [])
        vector = [0] * 5
        for endpoint, defects in parent.items():
            mask = sum(1 << d for d in oracle.fiber(levels, k - 2, endpoint))
            vector[MASKS.index(mask)] += (-1) ** defects
        assert tuple(vector) == expected
        m = sum(1 << d for d in oracle.fiber(levels, k - 1, x >> 2))
        assert m == 11
        child = oracle.belief_direct(levels, k, x, depth, [])
        assert child == oracle.belief_recursive(levels, k, x, depth, [])
        mass = oracle.signed_mass(child)
        assert mass == vector[4] - vector[2]
        matches = []
        tested = 0
        # All 1+4+16+64 descendants; membership by exact inversion,
        # and every accepted witness replayed independently bit by bit.
        for stripped in range(4):
            for suffix in range(4**stripped):
                tested += 1
                z = 4**stripped * x + suffix
                cut = depth + stripped - 1
                sched = oracle.forced_zero_schedule(z)
                if sched[cut:cut + 6] != "ututut":
                    continue
                if not oracle.admissible(sched[:cut] + "utututu"):
                    continue
                if not lift.frontier_member("u", k + stripped, z):
                    continue
                word = lift.frontier_witness("u", k + stripped, z)
                assert len(word) == k + stripped and word[0] == "u"
                replay = 1
                for letter in word[1:]:
                    old = replay
                    replay = oracle.gen_t_bitwise(old)
                    if letter != "t":
                        replay ^= 1
                    if letter == "p" and not old & 1:
                        replay ^= 2
                assert replay == z
                matches.append({"complexity": k + stripped, "state_hex": hex(z),
                                "depth": depth + stripped, "cut": cut,
                                "stripped_digits": stripped, "gaps": [2, 2, 2],
                                "schedule": sched, "generator_word": word})
        rows.append({"complexity": k, "state_hex": hex(x), "depth": depth,
                     "parent_vector": vector, "current_mask": m, "child_mass": mass,
                     "parent_belief_size": len(parent), "child_belief_size": len(child),
                     "descendants_tested": tested, "admissible_descendants": matches})
    combo = [2*a + 83*b for a, b in zip(rows[0]["parent_vector"], rows[1]["parent_vector"])]
    assert combo == [773, 0, 815, 54, 815]
    established = all(r["admissible_descendants"] for r in rows)
    payload = {"rows": rows, "positive_combination": combo,
               "ancestry_established_for_both": established,
               "verification": {"boolean_generator_cases": 255,
                                "direct_recursive_small_beliefs": small_checks,
                                "named_vector_checks": 2}}
    hashes = {str(p): hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}
    hashes["payload_sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    cpu = next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unknown")
    record = {
        "experiment_id": "20260905_signed_slice_convex_obstruction",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "git_dirty_paths": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines(),
        "question": "problem1", "hypothesis": "Both named opposite-sign slice vectors occur in the ancestor closure of admissible three-return cylinders.",
        "backend": "python-exact-integers-direct-and-recursive",
        "parameters": {"phase": "u", "named_complexity": 18, "maximum_added_digits": 3,
                       "schedule_cap": 64, "wall_limit_seconds": 120, "address_space_bytes": 1024**3,
                       "cases": [["0x642e4d2f1", 3], ["0x6473d46ab", 5]]},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(), "cpu_count": os.cpu_count(),
                     "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        "software": {"python": sys.version, "platform": platform.platform()},
        "runtime_seconds": time.monotonic() - started,
        "result_hashes": hashes, "result_summary": payload,
        "status": "finite-exhaustive",
        "proof_scope": "Two named exact vector evaluations and all 85 bounded descendants each; explicit witnesses establish ancestry when present.",
        "interpretation": "Validated opposite-sign ancestry implies the stated single-convex-region obstruction." if established else "Ancestry not established for both: no restricted-domain convex obstruction inferred.",
        "limitations": ["No all-depth signed-nonvanishing result.", "No claim of smallest opposite-sign pair.",
                        "No obstruction to disconnected or schedule-indexed regions.",
                        "This is targeted replay, not a larger three-return census."]}
    out = ROOT / "results/problem1/20260905_signed_slice_convex_obstruction.json"
    fd, temp = tempfile.mkstemp(dir=out.parent, prefix=out.name + ".", suffix=".tmp")
    with os.fdopen(fd, "w") as stream:
        json.dump(record, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, out)
    signal.alarm(0)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
