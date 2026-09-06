#!/usr/bin/env python3
"""Independent cell/long-division checks of the fixed temporal-deficit admission."""
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "proofs/informal/problem1_temporal_activity_deficit.md"
OUT = ROOT / "results/problem1/20260906_temporal_activity_deficit_independent.json"
INPUTS = [("0", 0, 1), ("1", 1, 1), ("2", 2, 1), ("3", 3, 1),
          ("5", 5, 1), ("7", 7, 1), ("-1", -1, 1), ("-2", -2, 1),
          ("-3", -3, 1), ("-1/7", -1, 7), ("1/3", 1, 3), ("-1/3", -1, 3)]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def atomic(path, value):
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def digits(numerator, denominator, width):
    # Successive exact rational remainders, independently of modular inversion.
    out = []
    for _ in range(width):
        bit = numerator % 2
        out.append(bit)
        numerator = (numerator - bit * denominator) // 2
    return out


def number(cells):
    return sum(bit * (2 ** i) for i, bit in enumerate(cells))


def t_cells(cells):
    return [bit ^ ((cells[i - 1] if i >= 1 else 0)
                   | (cells[i - 2] if i >= 2 else 0))
            for i, bit in enumerate(cells)]


def a_cells(cells):
    pad = cells + [0, 0]
    return [pad[i + 2] ^ (pad[i + 1] | pad[i]) for i in range(len(cells))]


def charged(cells):
    assert len(cells) == 6
    return int(cells == [0] * 6 or cells == [1, 0, 1, 0, 0, 0])


def temporal(cells, s):
    # All causal dependencies for these six cells are within this initial row.
    assert len(cells) >= 2 * s + 4
    values = []
    row = cells[:]
    for _ in range(s):
        values.append(charged(row[2 * s - 2:2 * s + 4]))
        row = t_cells(row)
    return values


def forced(cells):
    # Independent odd-section construction Q(P(x>>2)), not 4 A^2(x)+3.
    gate = number(cells[:4])
    assert gate in (7, 11)
    z = cells[2:]
    p = t_cells([1] + z + [0, 0])[1:]
    out = t_cells(p + [0, 0])
    if gate == 7:
        out[0] ^= 1
    return out


def run():
    started = time.monotonic()
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_AS, (1024 ** 3, 1024 ** 3))
    rows, entry_checks = [], []
    for label, n, den in INPUTS:
        if den == 1 and n >= 0:
            entry = (0, n)
        elif label in ("-1", "-2", "-3"):
            entry = (1, -n)
        elif label == "-1/7":
            entry = (2, 1)
        else:
            entry = None
        for s in range(1, 17):
            cells = digits(n, den, 2 * s + 4)
            values = temporal(cells, s)
            z = s - sum(values)
            if entry is not None:
                h, finite = entry
                k = (finite.bit_length() + 1) // 2
                assert z <= min(s, max(h, k))
                entry_checks.append([label, s, h, k, z, min(s, max(h, k))])
            if label in ("-1", "-2", "-3", "1", "2", "3"):
                assert z == 1
            if label == "-1/7":
                assert z == min(s, 2)
            if label in ("1/3", "-1/3"):
                assert z == s
            if label == "0":
                assert z == 0
            rows.append({"input": label, "s": s, "temporal_scores": values,
                         "D": sum(values), "Z": z})

    local = []
    for neighborhood in range(256):
        cells = digits(neighborhood, 1, 8)
        window = number(cells[2:])
        successor = number(t_cells(cells)[2:])
        implication = window != 5 or successor in (26, 27)
        assert implication
        local.append([neighborhood, window, successor, implication])

    temporal_words = []
    for a in range(8):
        for b in range(8):
            aa, bb = digits(a, 1, 3), digits(b, 1, 3)
            cc = [0, 0, 0, 0]
            for t in reversed(range(3)):
                cc[t] = cc[t + 1] ^ (aa[t] | bb[t])
            last = lambda word: max((i for i, bit in enumerate(word) if bit), default=-1)
            assert last(cc) == max(last(aa), last(bb))
            assert all((cc[t] ^ cc[t + 1]) == (aa[t] | bb[t]) for t in range(3))
            temporal_words.append([a, b, number(cc), last(aa), last(bb), last(cc)])

    harmonics = []
    for k in (0, 1, 2):
        total, h = Fraction(0), 0
        while True:
            previous = total
            total += Fraction(1, 2 * h + 1)
            if total > 2 * k:
                break
            h += 1
        assert previous <= 2 * k < total
        harmonics.append({"K": k, "h": h,
                          "sum": [total.numerator, total.denominator],
                          "previous_sum": [previous.numerator, previous.denominator]})

    seams, forced_rows = [], []
    for x in (7, 43):
        actual = digits(x, 1, max(4, x.bit_length()))
        states, gates = [x], []
        for _ in range(2):
            gates.append("u" if number(actual[:4]) == 7 else "t")
            actual = forced(actual)
            states.append(number(actual))
        if x == 7:
            assert states == [7, 27, 111] and number(actual[:4]) == 15
        forced_rows.append({"x": x, "states": states, "gates": gates})
        for s in range(1, 17):
            initial = digits(x, 1, 2 * s + 6)
            nxt = forced(initial)
            zx = s + 1 - sum(temporal(initial, s + 1))
            zf = s - sum(temporal(nxt, s))
            aged = nxt[:]
            for _ in range(s - 1):
                aged = a_cells(aged)
            term_i = charged(aged[:6])
            projected = initial[2 * s - 2:]
            term_j = charged(a_cells(projected)[:6]) + charged(projected[2:8])
            assert zx - zf == 1 + term_i - term_j
            assert -1 <= zx - zf <= 2
            seams.append({"x": x, "s": s, "Z_next_age": zx,
                          "Z_forced": zf, "I": term_i, "J": term_j,
                          "difference": zx - zf})

    output = {"rows": rows, "entry_checks": entry_checks,
              "local_charge_rows": local, "temporal_word_rows": temporal_words,
              "harmonics": harmonics, "forced_rows": forced_rows, "seams": seams}
    runtime = time.monotonic() - started
    assert runtime < 120
    source, admission = Path(__file__).read_bytes(), NOTE.read_bytes()
    record = {
        "experiment_id": "20260906-temporal-activity-deficit-independent",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "Fixed temporal D identity, finite-entry deficit bound, charge-5 implication, last-time identity and actual one-gate seam",
        "backend": "independent-python-cell-arrays-rational-long-division",
        "parameters": {"inputs": [x[0] for x in INPUTS], "ages": [1, 16],
                       "local_neighborhoods": [0, 255], "temporal_words": [0, 7],
                       "harmonic_K": [0, 1, 2], "forced_inputs": [7, 43],
                       "forced_updates": 2, "wall_cap_seconds": 120,
                       "memory_cap_bytes": 1024 ** 3, "cpu_concurrency": 1},
        "hardware": {"machine": platform.machine(), "processor": platform.processor(),
                     "logical_cpus": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": runtime,
        "result_hashes": {key: digest(value) for key, value in output.items()},
        "result_summary": {"temporal_rows": len(rows), "entry_bounds": len(entry_checks),
                           "local_rows": len(local), "temporal_word_rows": len(temporal_words),
                           "seams": len(seams), "harmonic_thresholds": [[r["K"], r["h"]] for r in harmonics],
                           "all_checks_passed": True},
        "interpretation": "Finite controls only; the all-depth last-time and spatial-limit arguments require proof review.",
        "status": "finite-exhaustive",
        "proof_scope": "Exactly the declared rational/age and Boolean domains, with full vectors retained.",
        "limitations": ["No compactness implication follows from finite controls.",
                        "No actual-survivor growth, occurrence exclusion, or Problem 1 solution is asserted.",
                        "No optimized backend, additional comparator or larger frontier was tested."],
        "provenance": {"source_path": str(Path(__file__).relative_to(ROOT)),
                       "source_sha256": sha(source), "source": source.decode(),
                       "admission_path": str(NOTE.relative_to(ROOT)),
                       "admission_sha256": sha(admission), "admission": admission.decode(),
                       "reference_sha256": sha((ROOT / "src/python/rule30_research_reference.py").read_bytes())},
        "results": output,
    }
    atomic(OUT, record)
    print(json.dumps(record["result_summary"], sort_keys=True))


if __name__ == "__main__":
    run()
