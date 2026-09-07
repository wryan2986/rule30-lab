"""Fixed Boolean identities supporting the K=2-to-K=1 reduction.

Admission and the exact sixteen assignments are in
proofs/informal/problem1_two_bit_strip_collapse.md, Section 6.
This does not test infinite FULL or global E-shadow membership.
"""

import hashlib
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


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260907_round306_two_bit_collapse.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
RULE = (0, 1, 1, 1, 1, 0, 0, 0)  # index = 4*left + 2*center + right


def sha(data):
    return hashlib.sha256(data).hexdigest()


def physical(row):
    return {i: RULE[4 * row.get(i - 1, 0) + 2 * row.get(i, 0)
                    + row.get(i + 1, 0)] for i in range(-5, 4)}


def packed_cut_output(row, right):
    # A acts on the input cut one cell to the right of the output cut.
    word = sum(row.get(i, 0) << (right + 1 - i)
               for i in range(-5, right + 2))
    return ((word >> 2) ^ ((word >> 1) | word)) & 1


def checked_step(row):
    answer = physical(row)
    for right in range(-4, 3):
        assert answer[right] == packed_cut_output(row, right)
    return answer


def deadline(_signal, _frame):
    raise TimeoutError("10-second fixed algebra cap exceeded")


def main():
    started = time.perf_counter()
    cap = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(10)
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA

    # Freeze the eight hand Rule30 values before using either implementation.
    for left in (0, 1):
        for center in (0, 1):
            for right in (0, 1):
                index = 4 * left + 2 * center + right
                assert RULE[index] == (left ^ (center | right))

    clock_cases = []
    for u in (0, 1):
        for shadow_center in (0, 1):
            actual = {-3: 1 ^ u, -2: u, -1: 1, 0: 1}
            proposed_shadow = {-3: 1 ^ u, -2: u, -1: 0,
                               0: shadow_center}
            a_next = checked_step(actual)
            h_next = checked_step(proposed_shadow)
            assert a_next[-2] == u
            assert h_next[-2] == 1  # Contradicts required shadow value 0.
            clock_cases.append({"u": u, "shadow_center": shadow_center,
                                "actual_next_minus2": a_next[-2],
                                "shadow_next_minus2": h_next[-2],
                                "required_shadow_next_minus2": 0})

    exit_cases = []
    for actual_pair in (1, 2, 3):
        for shadow_pair in (0, 1, 2, 3):
            actual = {-3: 1, -2: 0, -1: 1, 0: 1,
                      1: actual_pair & 1, 2: actual_pair >> 1}
            shadow = {-3: 1, -2: 0, -1: 0, 0: 1,
                      1: shadow_pair & 1, 2: shadow_pair >> 1}
            a_next, h_next = checked_step(actual), checked_step(shadow)
            assert a_next[0] == 0
            assert a_next[-2] ^ h_next[-2] == 1
            assert all(a_next[i] == h_next[i] for i in (-5, -4, -3))
            # Earlier cells have identical input cones as well.
            exit_cases.append({"actual_right_pair": actual_pair,
                               "shadow_right_pair": shadow_pair,
                               "next_minus2_discrepancy": 1,
                               "next_spatial_depth": 3})
    assert len(clock_cases) == 4 and len(exit_cases) == 12

    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < 10 and peak < cap
    payload = {"clock_cases": clock_cases, "exit_cases": exit_cases}
    source_paths = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
                    "proofs/informal/problem1_two_bit_strip_collapse.md",
                    "proofs/informal/problem1_one_bit_shadow_exit.md",
                    "proofs/informal/problem1_cycle_delay_renewal.md",
                    "proofs/informal/problem1_physical_time_cycle_defects.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round306-fixed-two-bit-strip-collapse-algebra",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The four odd-doubling assignments force shadow output 1 at position -2, and the twelve post-exit assignments have exact next spatial disagreement depth 3.",
        "backend": "Python-hand-truth-table/independent-packed-A-cut",
        "parameters": {"u": [0, 1], "shadow_centers": [0, 1],
                       "exit_actual_right_pairs": [1, 2, 3],
                       "exit_shadow_right_pairs": [0, 1, 2, 3],
                       "pair_encoding": "position1 low, position2 high",
                       "exit_actual_positions_minus3_through0": [1, 0, 1, 1],
                       "exit_shadow_positions_minus3_through0": [1, 0, 0, 1],
                       "other_initial_cells": 0,
                       "physical_steps": 1, "cpu_workers": 1,
                       "wall_cap_seconds": 10, "memory_cap_bytes": cap,
                       "output_cap_bytes": 128 * 1024},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "Main entry through fixed checks; excludes final provenance and serialization.",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in source_paths},
        "result_summary": {"all_checks_passed": True, "hand_rule_values": 8,
                           "odd_doubling_cases": 4, "exit_cases": 12,
                           "caps_passed": True},
        "status": "finite-exhaustive",
        "interpretation": "The two new local identities agree with independent cut updates. The eventual K=2-to-K=1 theorem is a separate conditional all-depth deduction.",
        "proof_scope": "Exactly sixteen declared local assignments and eight hand rule values.",
        "limitations": ["No claim that a test shadow is E of its actual row.",
                        "No infinite FULL orbit, state search, or clock computation.",
                        "No numerical verification of clock growth or the infinite induction.",
                        "No eventual bound on delay is established.",
                        "External adversarial review is missing."],
        "payload": payload,
    }
    encoded = (json.dumps(record, indent=2) + "\n").encode()
    assert len(encoded) < 128 * 1024
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=OUT.parent, prefix=OUT.name + ".",
                                         suffix=".tmp", delete=False) as handle:
            temporary = handle.name
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUT)
        fd = os.open(OUT.parent, os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    signal.alarm(0)
    print(json.dumps({"result": str(OUT.relative_to(ROOT)),
                      "odd_doubling_cases": 4, "exit_cases": 12,
                      "runtime_seconds": elapsed, "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
