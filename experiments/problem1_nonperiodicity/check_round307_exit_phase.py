"""Fixed algebra and phase certificate; admission: full_driver_exit_phase.md."""

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
OUT = ROOT / "results/problem1/20260907_round307_exit_phase.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
# Rows 000,001,...,111: eight hand-derived physical Rule 30 values.
RULE = (0, 1, 1, 1, 1, 0, 0, 0)
SCALAR = ((0, 1), (1, 1), (1, 0), (0, 0))
H = ((0, 1, 3, 3), (3, 2, 2, 2), (2, 3, 1, 1), (1, 0, 0, 0))
HAND_EDGES = ((7, 6), (6, 6), (14, 12), (12, 13), (13, 12),
              (28, 25), (25, 27), (27, 25))
CERTIFICATES = ((7, 1, 1, 6), (6, 0, 1, 6),
                (14, 1, 2, 13), (28, 1, 2, 27))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def packed(y):
    return (y >> 2) ^ ((y >> 1) | y)


def cells(y):
    return sum(RULE[4 * ((y >> (i + 2)) & 1)
                     + 2 * ((y >> (i + 1)) & 1) + ((y >> i) & 1)] << i
               for i in range(y.bit_length()))


def scalar_cell(letter, bit):
    return RULE[4 * (letter >> 1) + 2 * (letter & 1) + bit]


def paired_cells(letter, state):
    # A updates the appended two bits using two different overlapping cones.
    low = RULE[4 * (letter & 1) + 2 * (state >> 1) + (state & 1)]
    high = RULE[4 * (letter >> 1) + 2 * (letter & 1) + (state >> 1)]
    return low + 2 * high


def certificate(seed):
    seen, rows, row = {}, [], seed
    for _ in range(8):
        if row in seen:
            tau = seen[row]
            period = len(rows) - tau
            return {"seed": seed, "rows_before_repeat": rows,
                    "tau": tau, "period": period,
                    "cyc": rows[tau + (-tau) % period]}
        seen[row] = len(rows)
        rows.append(row)
        assert packed(row) == cells(row)
        row = packed(row)
    raise AssertionError("eight-step certificate cap exceeded")


def deadline(_signal, _frame):
    raise TimeoutError("10-second exit-phase algebra cap exceeded")


def main():
    started = time.perf_counter()
    cap = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(10)
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    for left in (0, 1):
        for center in (0, 1):
            for right in (0, 1):
                assert RULE[4 * left + 2 * center + right] == (left ^ (center | right))
    for before, after in HAND_EDGES:
        assert packed(before) == cells(before) == after

    scalar_cases = []
    for letter in range(4):
        for bit in (0, 1):
            assert SCALAR[letter][bit] == scalar_cell(letter, bit)
            scalar_cases.append([letter, bit, SCALAR[letter][bit]])

    # Complete transformation monoid on one bit; no input word enumeration.
    composition_cases = []
    for old in SCALAR:
        for letter in range(4):
            direct = tuple(scalar_cell(letter, old[bit]) for bit in (0, 1))
            if letter == 0:
                expected = old
            elif letter == 2:
                expected = tuple(1 ^ value for value in old)
            else:
                expected = (int(letter == 1),) * 2
            assert direct == expected and direct in SCALAR
            composition_cases.append({"old_map": old, "letter": letter,
                                      "new_map": direct})

    pair_cases = []
    for letter in (0, 2):
        for state in (1, 3):
            actual = paired_cells(letter, state)
            assert actual == H[letter][state]
            assert actual == (state if letter == 0 else 4 - state)
            pair_cases.append([letter, state, actual])
    assert paired_cells(3, 0) == paired_cells(2, 3) == 1

    certs = []
    for seed, tau, period, cyc in CERTIFICATES:
        result = certificate(seed)
        assert (result["tau"], result["period"], result["cyc"]) == (tau, period, cyc)
        certs.append(result)
    assert certs[2]["cyc"] == 2 * certs[1]["cyc"] + 1
    assert certs[3]["cyc"] == 4 * certs[1]["cyc"] + 3

    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < 10 and peak < cap
    payload = {"scalar_cases": scalar_cases, "composition_cases": composition_cases,
               "invariant_pair_cases": pair_cases, "phase_certificates": certs,
               "paired_first_step": [[3, 0, 1], [2, 3, 1]],
               "hand_edges": HAND_EDGES}
    sources = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
               "proofs/informal/problem1_full_driver_exit_phase.md",
               "proofs/informal/problem1_global_cycle_shadow.md",
               "proofs/informal/problem1_one_bit_shadow_exit.md",
               "proofs/informal/problem1_physical_time_cycle_defects.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round307-fixed-complete-driver-exit-phase",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The one-bit reset maps, their composition updates, the nonresetting invariant pair and the fixed 7/6 phase certificate agree with independent cell updates.",
        "backend": "Python-hand-rule-cells/independent-packed-A-and-map-tables",
        "parameters": {"letters": [0, 1, 2, 3], "scalar_bits": [0, 1],
                       "old_scalar_maps": SCALAR, "pair_letters": [0, 2],
                       "pair_states": [1, 3], "certificates": CERTIFICATES,
                       "certificate_order": ["seed", "tau", "period", "cyc"],
                       "hand_edges": HAND_EDGES, "max_certificate_steps": 8,
                       "cpu_workers": 1, "wall_cap_seconds": 10,
                       "memory_cap_bytes": cap, "output_cap_bytes": 128 * 1024},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "Main entry through checks, excluding provenance serialization.",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in sources},
        "result_summary": {"all_checks_passed": True, "hand_rule_values": 8,
                           "hand_edges": 8, "scalar_cases": 8,
                           "composition_cases": 16, "invariant_pair_cases": 4,
                           "phase_certificates": 4, "caps_passed": True},
        "status": "finite-exhaustive",
        "interpretation": "Fixed algebra and the named phase certificate pass; the all-period formula and E phase selection are separate mathematical deductions.",
        "proof_scope": "Eight letter/bit values, sixteen map compositions, four pair transitions, two first-step values and four named finite A orbits.",
        "limitations": ["No periodic-driver or source-word census.",
                        "No infinite FULL realization or eventual strip bound verified.",
                        "The fixed 7/6 example is not an infinite FULL orbit.",
                        "No finite original-support bound on births or repairs.",
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
    print(json.dumps({"result": str(OUT.relative_to(ROOT)), "all_checks_passed": True,
                      "runtime_seconds": elapsed, "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
