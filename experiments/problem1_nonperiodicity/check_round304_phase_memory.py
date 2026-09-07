"""Fixed 7/166 controls for the transient phase formula; no input search.

Admission: problem1_global_cycle_shadow.md Section 6. Agreement checks the
two mechanisms in the formula; disagreement invalidates its claimed reduction.
Only 12 (source, bit, horizon) cases, with 10-second/128-MiB caps, are run.
"""

import hashlib
import json
import os
import platform
from pathlib import Path
import resource
import signal
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260907_round304_phase_memory.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
CASES = ((7, 6, 0, 1, (13, 13)), (166, 200, 1, 1, (401, 400)))
HORIZONS = (1, 2, 5)
HAND_EDGES = ((7, 6), (6, 6), (14, 12), (15, 12), (12, 13), (13, 12),
              (166, 222), (222, 200), (200, 222), (332, 445), (333, 444),
              (400, 444), (444, 401), (401, 445), (445, 400))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def a_packed(x):
    return (x >> 2) ^ ((x >> 1) | x)


def a_cells(x):
    # Independent explicit Boolean cells, high zero boundary included.
    width = max(1, x.bit_length())
    cells = [bool((x >> i) & 1) for i in range(width)] + [False, False]
    output = [cells[i + 2] != (cells[i + 1] or cells[i]) for i in range(width)]
    return sum(int(bit) * (2 ** i) for i, bit in enumerate(output))


def cycle_certificate(seed):
    # Exactly the admitted fixed seeds, at most 16 updates per seed.
    rows, where, row = [], {}, seed
    for _ in range(16):
        if row in where:
            onset = where[row]
            period = len(rows) - onset
            phase = onset + ((-onset) % period)
            return {"seed": seed, "rows": rows, "onset": onset,
                    "period": period, "cyc": rows[phase]}
        where[row] = len(rows)
        rows.append(row)
        following = a_packed(row)
        assert following == a_cells(row)
        row = following
    raise AssertionError("fixed cycle did not close within its 16-step cap")


def formula(y, z, horizon):
    u, v, w = [], [], []
    for _ in range(horizon):
        u.append(y & 1)
        v.append((y >> 1) & 1)
        assert z & 1 == 0
        w.append((z >> 1) & 1)
        y, z = a_packed(y), a_packed(z)
    eta, theta = 1, 0
    for bit in u:
        eta *= 1 ^ bit
    for s in range(horizon):
        term = v[s] ^ u[s]
        for k in range(s + 1, horizon):
            term *= 1 ^ u[k]
        theta ^= term ^ w[s]
    return eta, theta


def scalar_phase(y, z, initial, horizon):
    # Iterate the original OR recurrence, then undo the cyclic permutation.
    # This does not use the product formula, packed A, or eta/theta.
    response, undo = initial, 0
    for _ in range(horizon):
        lo, hi = y % 2, (y // 2) % 2
        response = hi ^ int(bool(lo) or bool(response))
        undo ^= (z // 2) % 2
        y, z = a_cells(y), a_cells(z)
    return response ^ undo


def deadline(_sig, _frame):
    raise TimeoutError("10-second fixed phase-memory cap exceeded")


def main():
    started = time.perf_counter()
    limit = 128 * 1024 * 1024
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(10)
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    for before, after in HAND_EDGES:
        assert a_packed(before) == a_cells(before) == after

    certificates, checks = [], []
    for y, z, hand_eta, hand_theta, expected in CASES:
        source = cycle_certificate(y)
        assert source["cyc"] == z and source["onset"] == 1
        core = cycle_certificate(z)
        assert core["onset"] == 0 and all(r % 2 == 0 for r in core["rows"])
        certificates.extend((source, core))
        for initial in (0, 1):
            lifted = cycle_certificate(2 * y + initial)
            assert lifted["cyc"] == expected[initial]
            certificates.append(lifted)
            for horizon in HORIZONS:
                eta, theta = formula(y, z, horizon)
                assert (eta, theta) == (hand_eta, hand_theta)
                phase = (eta * initial) ^ theta
                assert phase == scalar_phase(y, z, initial, horizon)
                assert 2 * z + phase == lifted["cyc"]
                checks.append({"source": y, "initial_bit": initial, "horizon": horizon,
                               "eta": eta, "theta": theta, "cyc": 2 * z + phase})
    assert len(checks) == 12
    payload = {"hand_edges": HAND_EDGES, "cycles": certificates, "checks": checks}
    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < 10 and peak <= limit
    source_paths = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
                    "proofs/informal/problem1_global_cycle_shadow.md",
                    "proofs/informal/problem1_cycle_delay_renewal.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round304-fixed-transient-phase-memory",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The transient phase formula gives the exact phase-correct zero/one extensions of the fixed finite rows 7 and166 at every tested valid horizon.",
        "backend": "Python-product-formula/independent-cell-and-scalar-OR-recurrence",
        "parameters": {"sources": [7, 166], "bits": [0, 1], "horizons": HORIZONS,
                       "cases": 12, "cycle_step_cap": 16, "cpu_workers": 1,
                       "wall_cap_seconds": 10, "memory_cap_bytes": limit},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "main entry through all fixed scientific checks; excludes provenance and atomic serialization",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in source_paths},
        "result_summary": {"all_checks_passed": True, "cases": 12, "hand_edges": 15,
                           "caps_passed": True},
        "status": "finite-exhaustive",
        "proof_scope": "Exactly the 12 fixed source/bit/horizon cases, their eight source/core/lift cycle certificates, and 15 hand transitions.",
        "interpretation": "The controls verify both loss of the original bit at a transient reset and phase reversal without any actual low-bit reset.",
        "limitations": ["Not machine verification of the all-depth formula or global shadow construction.",
                        "No proof that the two phase bits form an autonomous quotient.",
                        "No source search, FULL orbit or fresh external review."],
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
        directory_fd = os.open(OUT.parent, os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    signal.alarm(0)
    print(json.dumps({"result": str(OUT.relative_to(ROOT)), "checks": len(checks),
                      "runtime_seconds": elapsed, "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
