"""Fixed validation of the shadow-gate birth criterion and phase quotient.

Admission: proofs/informal/problem1_shadow_gate_birth_phase.md.
Only32 Boolean identity cases and two named physical controls are tested.
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
OUT = ROOT / "results/problem1/20260907_round305_shadow_gate.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
H = ((0, 1, 3, 3), (3, 2, 2, 2), (2, 3, 1, 1), (1, 0, 0, 0))
CONTROLS = ((27, (1, 0), (27, 50, 111, 200), 0),
            (55, (0, 0), (55, 100, 223, 400), 1))
HAND_EDGES = ((27, 25), (25, 27), (55, 50), (50, 55),
              (100, 111), (111, 100), (110, 100), (220, 201),
              (201, 223), (223, 200), (200, 222), (222, 200))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def packed(y):
    return (y >> 2) ^ ((y >> 1) | y)


def a_cells(y):
    bits = [bool((y >> k) & 1) for k in range(max(1, y.bit_length()))]
    padded = bits + [False, False]
    return sum(1 << k for k in range(len(bits))
               if padded[k + 2] != (padded[k + 1] or padded[k]))


def certificate(y):
    rows, seen, row = [], {}, y
    for _ in range(16):
        if row in seen:
            tau = seen[row]
            period = len(rows) - tau
            return {"seed": y, "rows": rows, "tau": tau, "period": period,
                    "cyc": rows[tau + ((-tau) % period)]}
        seen[row] = len(rows)
        rows.append(row)
        assert packed(row) == a_cells(row)
        row = packed(row)
    raise AssertionError("fixed cycle cap exceeded")


def physical(row):
    # Explicit complete finite physical row, with both exterior boundaries0.
    out = {}
    for i in range(min(row) - 1, max(row) + 2):
        left, center, right = (bool(row.get(k, 0)) for k in (i - 1, i, i + 1))
        if left != (center or right):
            out[i] = 1
    assert out
    return out


def cut(row, j):
    return sum(1 << (j - i) for i in row if i <= j)


def deadline(_signal, _frame):
    raise TimeoutError("10-second fixed gate-check cap exceeded")


def main():
    started = time.perf_counter()
    cap = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(10)
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    for before, after in HAND_EDGES:
        assert packed(before) == a_cells(before) == after
    quotient = []
    for letter in range(4):
        for state in range(4):
            flag = int(state == 0)
            expected = flag if letter == 0 else (1 ^ flag if letter == 3 else 0)
            assert int(H[letter][state] == 0) == expected
            quotient.append([letter, state, expected])
    forward = []
    for word in range(16):
        a, b, c, d = ((word >> k) & 1 for k in range(4))
        initial = {0: 1, 1: a, 2: b, 3: c, 4: d}
        middle = {0: 0}
        for i in (1, 2, 3):
            middle[i] = int(bool(initial[i - 1]) !=
                            (bool(initial[i]) or bool(initial[i + 1])))
        pair = tuple(int(bool(middle[i - 1]) !=
                         (bool(middle[i]) or bool(middle[i + 1]))) for i in (1, 2))
        expected = a * b * int(bool(c) or bool(d))
        assert int(pair == (0, 0)) == expected
        forward.append({"right_bits": [a, b, c, d], "next_pair": pair,
                        "next_zero_flag": expected})
    controls, certificates = [], {}
    for source, right_pair, expected_rows, birth in CONTROLS:
        initial = {-k: 1 for k in range(source.bit_length()) if (source >> k) & 1}
        initial.update({i: 1 for i, bit in enumerate(right_pair, 1) if bit})
        rows = [initial]
        for _ in range(3):
            rows.append(physical(rows[-1]))
        left_rows = [cut(row, 0) for row in rows]
        assert tuple(left_rows) == expected_rows
        assert [row.get(0, 0) for row in rows] == [1, 0, 1, 0]
        for t, row in enumerate(rows):
            value = cut(initial, t)
            for _ in range(t):
                value = packed(value)
            assert value == cut(row, 0)
        for y in (*left_rows[:3], cut(initial, 2)):
            certificates[y] = certificate(y)
        src_cert = certificates[source]
        assert src_cert["tau"] == 0
        assert certificates[left_rows[1]]["tau"] == 0
        assert certificates[left_rows[2]]["tau"] == birth
        shadow_cut = certificates[cut(initial, 2)]["cyc"]
        assert shadow_cut >> 2 == source
        actual_flag = int(right_pair == (0, 0))
        shadow_flag = int(shadow_cut % 4 == 0)
        period_word = [y % 4 for y in src_cert["rows"]]
        assert period_word[0] == 3 and period_word[1] in (1, 2)
        assert actual_flag == int(period_word[1] == 2)
        parity, reset_offset = 0, None
        for distance in range(1, src_cert["period"] + 1):
            symbol = period_word[-distance]
            if symbol in (1, 2):
                reset_offset = -distance
                break
            parity ^= int(symbol == 3)
        assert reset_offset is not None
        assert shadow_flag == parity
        assert birth == actual_flag ^ shadow_flag
        controls.append({"source": source, "right_pair": right_pair,
                         "right_tail_after_position2": "identically zero",
                         "physical_rows": [sorted(row) for row in rows],
                         "center_and_left_rows": left_rows, "shadow_cut2": shadow_cut,
                         "actual_flag": actual_flag, "shadow_flag": shadow_flag,
                         "last_reset_offset": reset_offset, "suffix_parity": parity,
                         "birth": birth})
    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < 10 and peak < cap
    payload = {"quotient_checks": quotient, "forward_checks": forward,
               "controls": controls, "cycles": list(certificates.values()),
               "hand_edges": HAND_EDGES}
    source_paths = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
                    "proofs/informal/problem1_shadow_gate_birth_phase.md",
                    "proofs/informal/problem1_global_cycle_shadow.md",
                    "proofs/informal/problem1_inverse_scan_reset_language.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round305-fixed-shadow-gate-birth-and-phase-identities",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The scan zero-indicator quotient, four-bit flag update and actual/shadow gate birth formula agree with independent exact updates on the declared controls.",
        "backend": "Python-finite-Boolean-identities/full-physical-cells/packed-original-cuts",
        "parameters": {"scan_letters": [0, 1, 2, 3], "scan_states": [0, 1, 2, 3],
                       "right_words": "all16 four-bit words for the Boolean identity only",
                       "physical_controls": [{"source": x, "right_pair": p,
                                              "remaining_right_tail": "zero"}
                                             for x, p, _, _ in CONTROLS],
                       "physical_steps": 3, "cycle_step_cap": 16,
                       "cpu_workers": 1, "wall_cap_seconds": 10,
                       "memory_cap_bytes": cap, "output_cap_bytes": 128 * 1024},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "Main entry through all fixed checks; excludes final provenance and atomic serialization.",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in source_paths},
        "result_summary": {"all_checks_passed": True, "quotient_cases": len(quotient),
                           "forward_flag_cases": len(forward), "physical_controls": len(controls),
                           "closed_certificates": len(certificates), "caps_passed": True},
        "interpretation": "The fixed checks support the exact specified shadow observable. They do not close its future evolution from the two flags.",
        "status": "finite-exhaustive",
        "proof_scope": "Exactly32 Boolean identity cases, two fixed three-step physical controls and their listed closed cycle certificates.",
        "limitations": ["No infinite FULL continuation of either finite control is claimed.",
                        "No source, period, neighborhood-discovery or prefix search.",
                        "Arbitrary four-bit identity cases are not claimed to be admissible shadow states.",
                        "No autonomous phase update, finite birth budget or all-depth machine proof.",
                        "Fresh external review is missing."],
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
    print(json.dumps({"result": str(OUT.relative_to(ROOT)), "algebra_cases": 32,
                      "physical_controls": len(controls), "closed_certificates": len(certificates),
                      "runtime_seconds": elapsed, "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
