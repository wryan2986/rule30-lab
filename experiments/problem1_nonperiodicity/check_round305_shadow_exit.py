"""32 fixed Boolean controls for the one-bit-shadow exit table.

The second test row is NOT asserted to be E of the first. This checks
local identities only; see problem1_one_bit_shadow_exit.md for admission.
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

from check_round305_shadow_gate import physical

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260907_round305_shadow_exit.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def deadline(_signal, _frame):
    raise TimeoutError("10-second fixed exit-table cap exceeded")


def main():
    started = time.perf_counter()
    cap = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(10)
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    checks = []
    for ell in (0, 1):
        for actual_pair in range(4):
            u = int(actual_pair == 0)
            for shadow_pair in range(4):
                h = shadow_pair & 1  # position1, not the low bit of a cut at2
                hat_u = int(shadow_pair == 0)
                common = {-3: 1 ^ u, -2: u, -1: 1}
                actual = {**common, 0: 1, 1: actual_pair & 1, 2: actual_pair >> 1}
                shadow = {**common, 0: 1 ^ ell, 1: h, 2: shadow_pair >> 1}
                actual = {i: b for i, b in actual.items() if b}
                shadow = {i: b for i, b in shadow.items() if b}
                a_rows, h_rows = [actual], [shadow]
                for _ in range(3):
                    a_rows.append(physical(a_rows[-1]))
                    h_rows.append(physical(h_rows[-1]))
                assert [row.get(0, 0) for row in a_rows] == [1, 0, 1, 0]
                def difference(t, i):
                    return a_rows[t].get(i, 0) ^ h_rows[t].get(i, 0)
                assert all(difference(1, i) == 0 for i in range(-6, 0))
                assert all(difference(2, i) == 0 for i in range(-6, -1))
                if ell == 0:
                    expected = (0, 0, u ^ hat_u)
                elif u == 0:
                    expected = (1 ^ h, 0, 1)
                elif h == 1:
                    expected = (0, 0, 0)
                else:
                    expected = (1, 1, 0)
                actual_values = (difference(1, 0), difference(2, -1), difference(2, 0))
                assert actual_values == expected
                checks.append({"ell": ell, "actual_right_bits": [actual_pair & 1, actual_pair >> 1],
                               "shadow_right_bits": [h, shadow_pair >> 1], "u": u,
                               "odd_center_difference": actual_values[0],
                               "next_even_left_difference": actual_values[1],
                               "next_even_center_difference": actual_values[2]})
    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert len(checks) == 32 and elapsed < 10 and peak < cap
    payload = {"checks": checks}
    source_paths = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
                    "experiments/problem1_nonperiodicity/check_round305_shadow_gate.py",
                    "proofs/informal/problem1_one_bit_shadow_exit.md",
                    "proofs/informal/problem1_global_cycle_shadow.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round305-fixed-one-bit-shadow-exit-table",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The four-branch two-step discrepancy table agrees with direct physical Boolean updates on all32 declared local cone assignments.",
        "backend": "Python-explicit-four-branch-formula/whole-row-Boolean-cell-evolution",
        "parameters": {"ell": [0, 1], "actual_right_pairs": [0, 1, 2, 3],
                       "shadow_right_pairs": [0, 1, 2, 3],
                       "pair_encoding": "position1 is low bit, position2 is high bit",
                       "common_left_cells_minus1_minus2_minus3": ["1", "u", "1 XOR u"],
                       "all_other_initial_cells": 0, "physical_steps": 3,
                       "cpu_workers": 1, "wall_cap_seconds": 10,
                       "memory_cap_bytes": cap, "output_cap_bytes": 128 * 1024},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "Main entry through fixed checks; excludes final provenance and serialization.",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in source_paths},
        "result_summary": {"all_checks_passed": True, "local_algebra_cases": len(checks),
                           "caps_passed": True},
        "interpretation": "The local table is verified. Global shadow membership and infinite FULL are premises of the separate mathematical theorem, not outputs of these controls.",
        "status": "finite-exhaustive",
        "proof_scope": "Exactly32 local assignments and their first three physical updates.",
        "limitations": ["No claim that the second local row is the global E shadow of the first.",
                        "No infinite FULL continuation or new admissible source is constructed.",
                        "No numerical check of the all-depth least-delay implication.",
                        "No autonomous state quotient or eventual strip exclusion.",
                        "External review is missing."],
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
    print(json.dumps({"result": str(OUT.relative_to(ROOT)), "checks": len(checks),
                      "runtime_seconds": elapsed, "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
