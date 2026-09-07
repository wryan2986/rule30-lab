"""Eight fixed cone identities; admission: nonreset_return_birth_spacing.md."""

import argparse
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

from check_round307_exit_phase import RULE


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260907_round307_nonreset_return.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def truth_step(row):
    return {i: RULE[4 * row[i - 1] + 2 * row[i] + row[i + 1]]
            for i in range(min(row) + 1, max(row))}


def packed_step(word):
    return (word << 1) ^ (word | (word >> 1))


def checked_cone(initial):
    rows = [initial]
    offset = min(initial)
    word = sum(bit << (i - offset) for i, bit in initial.items())
    for _ in range(2):
        rows.append(truth_step(rows[-1]))
        word = packed_step(word)
        assert all(bit == ((word >> (i - offset)) & 1)
                   for i, bit in rows[-1].items())
    return rows


def deadline(_signal, _frame):
    raise TimeoutError("10-second nonreset-return cone cap exceeded")


def main():
    started = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    out = args.output if args.output.is_absolute() else ROOT / args.output
    cap = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(10)
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    for left in (0, 1):
        for center in (0, 1):
            for right in (0, 1):
                assert RULE[4 * left + 2 * center + right] == (left ^ (center | right))
    hand = [[0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 1, 1], [1, 1, 0]]
    hand_rows = checked_cone(dict(zip(range(-2, 5), hand[0])))
    assert [list(row.values()) for row in hand_rows] == hand

    cases = []
    for u in (0, 1):
        for a in (0, 1):
            for b in (0, 1):
                initial = {-2: u, -1: u, 0: 0, 1: u, 2: 1, 3: a, 4: b}
                rows = checked_cone(initial)
                centers = [row[0] for row in rows]
                assert centers == [0, 0, 1]
                assert [rows[1][i] for i in (1, 2, 3)] == [1, 1 ^ u, 1 ^ (a | b)]
                pair = [rows[2][i] for i in (1, 2)]
                assert pair == [1, u * (a | b)]
                cases.append({"u": u, "a": a, "b": b,
                              "initial_values_minus2_through4": list(initial.values()),
                              "centers": centers, "second_right_pair": pair,
                              "rows_on_shrinking_trusted_cones": [list(row.values()) for row in rows]})
    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < 10 and peak < cap, {
        "runtime_seconds": elapsed, "peak_rss_bytes": peak,
        "wall_cap_seconds": 10, "memory_cap_bytes": cap,
        "self_memory": [line for line in Path("/proc/self/status").read_text().splitlines()
                        if line.startswith(("VmPeak:", "VmHWM:", "VmSize:", "VmRSS:"))],
    }
    payload = {"hand_cone": hand, "cases": cases}
    sources = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
               "experiments/problem1_nonperiodicity/check_round307_exit_phase.py",
               "proofs/informal/problem1_nonreset_return_birth_spacing.md",
               "proofs/informal/problem1_nonresetting_core_returns.md",
               "proofs/informal/problem1_shadow_gate_birth_phase.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    replay = [sys.executable,
              "experiments/problem1_nonperiodicity/check_round307_nonreset_return.py",
              "--output", str(out.relative_to(ROOT))]
    record = {
        "experiment_id": "round307-fixed-nonreset-return-shadow-cone",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "For the eight declared u,a,b assignments the shadow cone has centers 0,0,1 and second right pair (1,u*(a OR b)).",
        "backend": "Python-hand-rule-cells/independent-packed-physical-Rule30",
        "parameters": {"u": [0, 1], "a": [0, 1], "b": [0, 1],
                       "initial_positions": list(range(-2, 5)),
                       "initial_values": ["u", "u", 0, "u", 1, "a", "b"],
                       "physical_steps": 2,
                       "trusted_positions_at_steps": [list(range(-2, 5)), list(range(-1, 4)), [0, 1, 2]],
                       "packed_bit_order": "increasing physical position; position -2 is bit0",
                       "cpu_workers": 1, "wall_cap_seconds": 10,
                       "memory_cap_bytes": cap, "output_cap_bytes": 128 * 1024},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable,
                     "reproduction_argv": ["python3", "-c",
                         "import subprocess; subprocess.run(%r, check=True)" % replay],
                     "launch_note": "Validated in a fresh Python child; getrusage history is preserved across execve.",
                     "launch_scope_reference": "https://man7.org/linux/man-pages/man2/getrusage.2.html"},
        "runtime_seconds": elapsed,
        "runtime_scope": "Main entry through checks, excluding provenance serialization.",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in sources},
        "result_summary": {"all_checks_passed": True, "hand_rule_values": 8,
                           "hand_cone_steps": 2, "fixed_cone_assignments": 8,
                           "caps_passed": True},
        "status": "finite-exhaustive",
        "interpretation": "The selected-source shadow transport identity passes; cyclicity, future gates, birth timing and clock spacing are separate conditional deductions.",
        "proof_scope": "Eight seven-cell inputs, each for two steps on its shrinking trusted cone, after one hand cone.",
        "limitations": ["Local inputs are not asserted to be global E shadows or FULL realizations.",
                        "No new source, driver word, gate prefix or clock tree searched.",
                        "No numerical test of an eventual strip bound or infinite induction.",
                        "No finite original-support bound on the continuing births.",
                        "Fresh review of the birth-spacing argument is recorded separately in problem1_round309_recovered_birth_review.md; its imported dependencies were not freshly reviewed end-to-end."],
        "payload": payload,
    }
    encoded = (json.dumps(record, indent=2) + "\n").encode()
    assert len(encoded) < 128 * 1024
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=out.parent, prefix=out.name + ".",
                                         suffix=".tmp", delete=False) as handle:
            temporary = handle.name
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, out)
        fd = os.open(out.parent, os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    signal.alarm(0)
    print(json.dumps({"result": str(out.relative_to(ROOT)), "fixed_cases": 8,
                      "runtime_seconds": elapsed, "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
