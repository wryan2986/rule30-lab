"""Fixed four-state algebra check; no seed, word, period, or orbit search.

Admission and outcome implications are in the accompanying proof, Section 0.
Run from a small Python parent if launcher RSS contaminates resource reporting.
"""

import hashlib
import itertools
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
OUT = ROOT / "results/problem1/20260907_round303_birth_algebra.json"
PROOF = "proofs/informal/problem1_cycle_birth_observation_no_go.md"
DEPS = [
    PROOF,
    "proofs/informal/problem1_activity_sparse_temporal_codes.md",
    "proofs/informal/problem1_activity_temporal_gate_bridge.md",
    "proofs/informal/problem1_full_fringe_temporal_diagonal.md",
    "proofs/informal/problem1_scan_doubling_cycle_lag.md",
    "proofs/informal/problem1_cycle_delay_renewal.md",
]
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
H_HAND = ((0, 1, 3, 3), (3, 2, 2, 2), (2, 3, 1, 1), (1, 0, 0, 0))
EXPECTED = {(1, (1, 3)): 2, (1, (1, 1)): 3,
            (2, (1, 3)): 3, (2, (1, 1)): 2}
WALL_SECONDS = 10
MEMORY_BYTES = 128 * 1024 * 1024


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deletion_bits(a, b):
    """Independent local deletion equations, with explicit Boolean bits."""
    al, ah = a % 2, a // 2
    bl, bh = b % 2, b // 2
    rl = bl ^ int(bool(al) or bool(ah))
    rh = bh ^ int(bool(ah) or bool(rl))
    return rl + 2 * rh


def solve_scan(a, target):
    """Invert deletion by trying its four possible next symbols."""
    possible = [b for b in range(4) if deletion_bits(a, b) == target]
    assert len(possible) == 1
    return possible[0]


def deadline(_signum, _frame):
    raise TimeoutError("10-second algebra cap exceeded")


def main():
    started = time.perf_counter()
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(WALL_SECONDS)
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))
    assert sha(ROOT / REFERENCE) == REFERENCE_SHA
    independent = tuple(tuple(solve_scan(a, i) for a in range(4))
                        for i in range(4))
    assert independent == H_HAND
    assert all(H_HAND[i][2] == H_HAND[i][3] for i in range(4))
    assert deletion_bits(1, 2) == 1 and deletion_bits(2, 1) == 2

    certificates = []
    case_count = 0
    # The interior is ANY function on four states, not an enumerated word.
    for interior in itertools.product(range(4), repeat=4):
        for (gate, suffix), expected in EXPECTED.items():
            table_outputs, solved_outputs = [], []
            for start in range(4):
                a = interior[start]
                b = interior[start]
                for letter in (*suffix, 3, gate):
                    a = H_HAND[letter][a]
                    b = solve_scan(b, letter)
                assert a == b == expected
                table_outputs.append(a)
                solved_outputs.append(b)
                case_count += 1
            assert table_outputs[expected] == expected
            certificates.append([list(interior), gate, list(suffix),
                                 table_outputs, solved_outputs])
    assert case_count == 4096
    payload = {
        "hand_scan_table": H_HAND,
        "independent_scan_table": independent,
        "return_cases": certificates,
        "immediate_merge_2_3": True,
        "nonnilpotent_dyadic_control": {"word": [1, 2], "Phi_word": [1, 2]},
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    source_paths = DEPS + [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE]
    elapsed = time.perf_counter() - started
    peak_rss_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < WALL_SECONDS
    assert peak_rss_bytes <= MEMORY_BYTES
    cpu_model = next((line.split(":", 1)[1].strip()
                      for line in Path("/proc/cpuinfo").read_text().splitlines()
                      if line.startswith("model name")), "unreported")
    result = {
        "experiment_id": "round303-cycle-birth-fixed-algebra",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "Suffixes 13 and 11 force the stated opposite recurrent scan starts for either permitted gate, regardless of the preceding four-state function.",
        "backend": "python-tabulated-maps-and-independent-deletion-inversion",
        "parameters": {
            "states": [0, 1, 2, 3], "gates": [1, 2],
            "suffixes": [[1, 3], [1, 1]], "interior_functions": 256,
            "start_specific_return_checks": case_count,
            "wall_cap_seconds": WALL_SECONDS, "memory_cap_bytes": MEMORY_BYTES,
            "scientific_orbit_inputs": [], "cpu_workers": 1,
        },
        "hardware": {"machine": platform.machine(), "processor": platform.processor(),
                     "cpu_model": cpu_model,
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak_rss_bytes},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "From main entry through all mathematical checks and canonical payload construction; excludes metadata collection and atomic serialization.",
        "result_hashes": {"canonical_payload_sha256": hashlib.sha256(canonical).hexdigest()},
        "source_hashes": {p: sha(ROOT / p) for p in source_paths},
        "result_summary": {"all_checks_passed": True, "return_checks": case_count,
                           "scan_entries": 16, "caps_passed": True},
        "interpretation": "The fixed algebra supports the symbolic arbitrary-prefix construction. No finite-source supply or infinite FULL survivor is tested.",
        "status": "finite-exhaustive",
        "proof_scope": "All four-state interior functions, both suffixes and gates, and all starting states; the 16 local scan entries and fixed Phi(12)=12 control.",
        "limitations": ["No finite spatial support assertion for constructed cyclic rows.",
                        "No check of an infinite FULL future or uniform future strip bound.",
                        "Not machine verification of the all-depth proof or a fresh external review."],
        "payload": payload,
    }
    encoded = (json.dumps(result, indent=2) + "\n").encode()
    assert len(encoded) < 1024 * 1024
    OUT.parent.mkdir(parents=True, exist_ok=True)
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
        if temporary is not None and os.path.exists(temporary):
            os.unlink(temporary)
    signal.alarm(0)
    print(json.dumps({"result": str(OUT.relative_to(ROOT)),
                      "checks": case_count, "runtime_seconds": elapsed,
                      "payload_sha256": result["result_hashes"]["canonical_payload_sha256"]}))


if __name__ == "__main__":
    main()
