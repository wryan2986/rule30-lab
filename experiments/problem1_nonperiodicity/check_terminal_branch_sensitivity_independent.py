#!/usr/bin/env python3
"""Cell-only checks of the admitted highest-two-bit branch perturbation.

No survivor cycles, frontiers, or new comparator words are generated.
The periodic driver comes from already stored spatial vector certificates.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import subprocess
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "proofs/informal/problem1_terminal_branch_sensitivity.md"
INPUT = ROOT / "results/problem1/20260905_periodic_rational_primary.json"
OUT = ROOT / "results/problem1/20260906_terminal_branch_sensitivity_independent.json"
BAD = ("uu", "ttttt", "ututtu")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def atomic(path, value):
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def a_cells(cells):
    padded = cells + [0, 0]
    return [padded[i + 2] ^ (padded[i + 1] | padded[i]) for i in range(len(cells))]


def score(cells):
    def charged(word):
        return word == [0] * 6 or word == [1, 0, 1, 0, 0, 0]
    return int(charged(a_cells(cells)[:6])) + int(charged(cells[2:8]))


def as_int(cells):
    return sum(v << i for i, v in enumerate(cells))


def bits(case, phase, start, length):
    onset, period, columns = case["spatial_onset"], case["lambda"], case["columns"]
    positions = [i if i < onset else onset + (i - onset) % period for i in range(start, start + length)]
    return [(columns[i] >> (phase % len(case["q"]))) & 1 for i in positions]


def word(case, phase, length):
    return "".join(case["q"][(phase + i) % len(case["q"])] for i in range(length))


def allowed(text):
    return not any(b in text for b in BAD)


def driver(case, ending, count):
    parity = 0
    rows = []
    for d in range(count):
        cells = bits(case, ending - d, 2 * d, 8)
        toggle = cells[3] | cells[4]
        parity ^= toggle
        changed = cells[:]
        changed[6] ^= 1
        changed[7] ^= parity
        rows.append([as_int(cells), toggle, parity, score(cells), score(changed)])
    return rows


def forward(cells, length, age):
    schedule, costs, states = [], [], []
    for t in range(length):
        states.append(cells[:])
        gate = as_int(cells[:4])
        assert gate in (7, 11), (t, gate)
        schedule.append("u" if gate == 7 else "t")
        if t <= age - 2:
            shift = 2 * (age - t - 2)
            costs.append(score(cells[shift:shift + 8]))
        cells = [1, 1] + a_cells(a_cells(cells))
    return "".join(schedule), sum(costs), states


def literal(case, age):
    original = bits(case, 0, 0, 2 * age + 4)
    expected = word(case, 0, age + 1)
    observed, base, states = forward(original, age + 1, age)
    assert observed == expected
    # Solve the TWO high bits by direct cell evolution, independently of
    # the defect recurrence. Exactly one of the four lifts has the flip.
    target = expected[:-1] + ("t" if expected[-1] == "u" else "u")
    assert allowed(target)
    candidates = []
    for high in range(4):
        candidate = original[:-2] + [high & 1, high >> 1]
        try:
            got, value, orbit = forward(candidate, age + 1, age)
        except AssertionError:
            continue
        if got == target:
            candidates.append((candidate, value, orbit))
    assert len(candidates) == 1
    changed, altered, orbit = candidates[0]
    ending = (age - 2) % len(case["q"])
    rows = driver(case, ending, age - 1)
    assert base == sum(r[3] for r in rows)
    assert altered == sum(r[4] for r in rows)
    # Check every claimed moving two-bit difference using the direct orbits.
    for t in range(age):
        b = 2 * age + 2 - 2 * t
        assert states[t][:b] == orbit[t][:b]
        assert states[t][b] ^ orbit[t][b] == 1
        eps = states[t][b + 1] ^ orbit[t][b + 1]
        next_eps = states[t + 1][b - 1] ^ orbit[t + 1][b - 1]
        assert next_eps == eps ^ (states[t][b - 2] | states[t][b - 3])
    return {"age": age, "base": base, "changed": altered,
            "delta": altered - base, "base_integer_hex": hex(as_int(original)),
            "changed_integer_hex": hex(as_int(changed)), "observed": observed,
            "changed_observed": target,
            "orbit_pair_hash": digest([[as_int(x) for x in states], [as_int(x) for x in orbit]])}


def check(case):
    p, a, lam = len(case["q"]), case["spatial_onset"], case["lambda"]
    d0 = (a + 1) // 2
    length = math.lcm(p, lam // math.gcd(lam, 2))
    phases = []
    for e in range(p):
        prefix = "".join(case["q"][(e + 2 - 5 + j) % p] for j in range(6))
        flipped = prefix[:-1] + ("t" if prefix[-1] == "u" else "u")
        if not allowed(flipped):
            continue
        rows = driver(case, e, d0 + 4 * length)
        block = rows[d0:d0 + 2 * length]
        assert block == rows[d0 + 2 * length:d0 + 4 * length]
        phases.append({"ending_phase": e, "joint_period": 2 * length,
                       "driver_parity": sum(r[1] for r in rows[d0:d0 + length]) % 2,
                       "base_total": sum(r[3] for r in block),
                       "changed_total": sum(r[4] for r in block),
                       "delta_total": sum(r[4] - r[3] for r in block),
                       "period_rows": block, "period_rows_sha256": digest(block),
                       "prefix_rows": rows[:d0]})
    ages = sorted({2, *(d0 + v * 2 * length + r for v in range(3) for r in range(2, p + 2))})
    literals = [literal(case, s) for s in ages if s >= 2 and allowed(word(case, 0, s) + ("t" if case["q"][s % p] == "u" else "u"))]
    return {"word": case["q"], "d0": d0, "L": length, "phases": phases, "literal_checks": literals}


def main():
    began = time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    cases = [{"q": "ut", "spatial_onset": 0, "lambda": 7,
              "columns": [((7 >> i) & 1) | (((123 >> i) & 1) << 1) for i in range(7)]}]
    old = json.loads(INPUT.read_text())["result_summary"]["rows"]
    cases.extend({k: row[k] for k in ("q", "spatial_onset", "lambda", "columns")}
                 for q in ("ututtt", "ttututt") for row in old if row["q"] == q)
    rows, used = [], []
    for case in cases:
        used.append(case)
        rows.append(check(case))
        if any(r["delta_total"] for r in rows[-1]["phases"]):
            break
    summary = {"rows": rows, "stopped_at_first_nonzero_control": any(p["delta_total"] for r in rows for p in r["phases"])}
    paths = [Path(__file__), NOTE, INPUT, ROOT / "src/python/rule30_research_reference.py"]
    record = {"experiment_id": "20260906_terminal_branch_sensitivity_independent",
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "question": "problem1", "hypothesis": "The derived two-bit defect recurrence gives the exact change of Psi after one admissible final-branch flip; nonzero periodic mean refutes bounded cost per edit.",
              "backend": "python-independent-cell-arrays", "parameters": {"used_cases": [r["q"] for r in used], "wall_seconds": 120, "memory_bytes": 1 << 30, "literal_ages": [[v["age"] for v in r["literal_checks"]] for r in rows]},
              "hardware": {"machine": platform.machine(), "cpu": next((v.split(":", 1)[1].strip() for v in Path("/proc/cpuinfo").read_text().splitlines() if v.startswith("model name")), "unknown"), "logical_cpu_count": os.cpu_count()},
              "software": {"python": platform.python_version(), "platform": platform.platform()},
              "runtime_seconds": time.monotonic() - began,
              "source_and_input_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              "source_snapshot": Path(__file__).read_text(), "admission_snapshot": NOTE.read_text(), "input_snapshots": used,
              "result_summary": summary, "result_hashes": {"summary_sha256": digest(summary)},
              "status": "finite-exhaustive", "proof_scope": "Only the declared periodic control driver, defect-cycle closure, and finite literal cell replays; all-age inference requires the separate mathematical proof.",
              "interpretation": "This tests stability under one late interruption, without asserting ordinary-frontier membership.",
              "limitations": ["No ordinary endpoint or finite-seed realization is asserted.", "No additional rational cycle or frontier was computed.", "Both implementations remain local; this independent cell derivation is by the lead.", "Full Git plus source snapshots identify uncommitted admitted work."]}
    assert time.monotonic() - began < 120
    atomic(OUT, record)
    print(json.dumps([{ "word": r["word"], "phases": [{k: p[k] for k in ("ending_phase", "joint_period", "driver_parity", "base_total", "changed_total", "delta_total")} for p in r["phases"]], "literals": [{k: v[k] for k in ("age", "base", "changed", "delta")} for v in r["literal_checks"]]} for r in rows]))


if __name__ == "__main__":
    main()
