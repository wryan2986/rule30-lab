"""Falsify tau(y)<=bitlen(y)-1; stop at first witness, at most width12.

Admission: proofs/informal/problem1_width_delay_bound_test.md.
No shift-tower sampling, fitted intercept, or larger census is performed.
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
OUT = ROOT / "results/problem1/20260907_round305_width_delay.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
HAND_EDGES = ((0, 0), (1, 1), (2, 3), (3, 3),
              (4, 7), (5, 6), (6, 6), (7, 6))
MAX_INPUT = 4095


def sha(data):
    return hashlib.sha256(data).hexdigest()


def packed(y):
    return (y >> 2) ^ ((y >> 1) | y)


def cells(y):
    word = [bool((y // (2 ** j)) % 2) for j in range(max(1, y.bit_length()))]
    padded = word + [False, False]
    return sum(2 ** j for j in range(len(word))
               if padded[j + 2] != (padded[j + 1] or padded[j]))


def packed_orbit(y):
    rows, seen, row = [], {}, y
    for _ in range(4096):
        if row in seen:
            tau = seen[row]
            period = len(rows) - tau
            return rows, tau, period, rows[tau + ((-tau) % period)]
        seen[row] = len(rows)
        rows.append(row)
        row = packed(row)
    raise AssertionError("orbit cap exceeded")


def cell_orbit(y):
    # Independent recurrence and repeat detection by list membership.
    rows, row = [], y
    for _ in range(4096):
        if row in rows:
            tau = rows.index(row)
            period = len(rows) - tau
            multiple = ((tau + period - 1) // period) * period
            core = rows[tau + ((multiple - tau) % period)]
            return rows, tau, period, core
        rows.append(row)
        row = cells(row)
    raise AssertionError("independent orbit cap exceeded")


def deadline(_signal, _frame):
    raise TimeoutError("30-second width-bound falsification cap exceeded")


def main():
    started = time.perf_counter()
    cap = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(30)
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    for before, after in HAND_EDGES:
        assert packed(before) == cells(before) == after
    transcript = hashlib.sha256()
    witness, count, comparisons = None, 0, 0
    for y in range(1, MAX_INPUT + 1):
        first, second = packed_orbit(y), cell_orbit(y)
        assert first == second, y
        rows, tau, period, core = first
        comparisons += len(rows)
        count += 1
        transcript.update((json.dumps([y, rows, tau, period, core],
                                      separators=(",", ":")) + "\n").encode())
        if tau > y.bit_length() - 1:
            witness = {"source": y, "width": y.bit_length(), "tau": tau,
                       "period": period, "cyc": core, "rows": rows,
                       "closing_edge": [rows[-1], rows[tau]],
                       "excess_over_width_minus_one": tau - y.bit_length() + 1}
            break
    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < 30 and peak < cap
    payload = {"hand_edges": HAND_EDGES, "checked_interval": [1, count],
               "compared_orbit_edges": comparisons, "witness": witness,
               "ordered_check_transcript_sha256": transcript.hexdigest()}
    source_paths = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
                    "proofs/informal/problem1_width_delay_bound_test.md",
                    "proofs/informal/problem1_cycle_completion_defect_transport.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round305-width-minus-one-delay-bound-falsification",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "Every positive finite y has least A-preperiod at most bitlen(y)-1.",
        "backend": "Python-independent-packed-and-Boolean-cell-orbits",
        "parameters": {"first_input": 1, "maximum_input": MAX_INPUT,
                       "order": "increasing numeric", "stop": "first violation or maximum input",
                       "cpu_workers": 1, "orbit_step_cap": 4096,
                       "wall_cap_seconds": 30, "memory_cap_bytes": cap,
                       "output_cap_bytes": 256 * 1024},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "Main entry through scientific checks; excludes final provenance and atomic serialization.",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode()),
            "ordered_check_transcript_sha256": transcript.hexdigest()},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in source_paths},
        "result_summary": {"all_implementations_agree": True, "checked_inputs": count,
                           "bound_refuted": witness is not None,
                           "witness": None if witness is None else witness["source"],
                           "caps_passed": True},
        "interpretation": "A verified counterexample refutes the precise universal bound; absence within the cap would leave the all-depth claim open.",
        "status": "finite-exhaustive",
        "proof_scope": "The contiguous finite interval actually checked and the complete closed witness certificate if one is found.",
        "limitations": ["Not a test or refutation of every possible width-dependent bound.",
                        "No shift-tower rate, physical FULL orbit or general bounded-strip theorem.",
                        "No refitted constant or extension of the search cap.",
                        "External review is missing."],
        "payload": payload,
    }
    encoded = (json.dumps(record, indent=2) + "\n").encode()
    assert len(encoded) < 256 * 1024
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
    print(json.dumps({"result": str(OUT.relative_to(ROOT)), "checked_inputs": count,
                      "witness": witness, "runtime_seconds": elapsed,
                      "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
