#!/usr/bin/env python3
"""Four admitted r=2/r=3 seam checks; never a suffix-width search."""
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time
from datetime import datetime, timezone

from check_terminal_branch_sensitivity_independent import atomic, digest, forward, score, as_int

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "proofs/informal/problem1_finite_suffix_defect_transfer.md"
OUT = ROOT / "results/problem1/20260906_finite_suffix_defect_seams.json"
CASES = [(2, "tt", (3, 115)), (3, "ttu", (4, 452))]


def A(x):
    return (x >> 2) ^ ((x >> 1) | x)


def J(x):
    return int(A(x) & 63 in (0, 5)) + int((x >> 2) & 63 in (0, 5))


def window(phase, position, width):
    assert position >= 0
    modulus = 1 << (position + width)
    numerator = (-7, -123)[phase % 2]
    return (numerator * pow(127, -1, modulus) % modulus) >> position


def invert_generator(target, letter, width):
    out = 0
    for i in range(width):
        if (letter == "p" and i < 2) or (letter == "u" and i == 0):
            correction = 1
        else:
            correction = ((out >> (i - 1)) & 1 if i else 0) | ((out >> (i - 2)) & 1 if i >= 2 else 0)
        out |= (((target >> i) & 1) ^ correction) << i
    return out


def cylinder(word):
    # Full inverse-branch construction, with no moving-defect formula.
    value, width = 3, 2
    for q in reversed(word):
        value = invert_generator(value, q, width)
        value = invert_generator(value, "p", width)
        value = 4 * value + 3
        width += 2
    return value


def back_defect(base_window, target, width):
    mask = (1 << width) - 1
    base_image = A(A(base_window))

    def image(delta):
        return (A(A(base_window ^ (delta << 4))) ^ base_image) & mask

    out = 0
    for i in range(width):
        out |= (((image(out) ^ target) >> i) & 1) << i
    assert image(out) == target
    assert out & 1 == target & 1
    return out


def scalar_cost(value, age):
    total = 0
    for t in range(age - 1):
        assert value & 15 in (7, 11)
        total += J(value >> (2 * (age - t - 2)))
        value = 4 * A(A(value)) + 3
    return total


def transferred(r, tau, age):
    n, width = age + 1 - r, 2 * r
    ending = (age - 2) % 2
    terminal = cylinder(tau)
    delta = (terminal ^ window(n, 0, width + 2)) >> 2
    seed = delta
    base_tail = scalar_cost(window(n, 0, width + 2), r - 1)
    changed_tail = scalar_cost(terminal, r - 1)
    rows = []
    for d in range(r - 2, age - 1):
        driver = window(ending - d, 2 * (d - r + 2), width + 4)
        delta = back_defect(driver, delta, width)
        base = window(ending - d, 2 * d, 8)
        # The two admitted seams have w<=8. No generic larger width run.
        changed = base ^ (delta << (8 - width))
        rows.append([driver, delta, J(base), J(changed)])
    period = (1 << (width - 1)) * 14
    if len(rows) >= period:
        assert rows[period - 1][1] == seed
        assert rows[period:] == rows[:len(rows) - period]
    return {"base": base_tail + sum(v[2] for v in rows),
            "changed": changed_tail + sum(v[3] for v in rows),
            "base_tail": base_tail, "changed_tail": changed_tail,
            "terminal_defect": seed, "period": period,
            "transfer_rows": rows, "transfer_sha256": digest(rows)}


def literal(r, tau, age):
    base_word = "".join("ut"[i % 2] for i in range(age + 1))
    changed_word = base_word[:age + 1 - r] + tau
    for word in (base_word, changed_word):
        assert all(b not in word for b in ("uu", "ttttt", "ututtu"))
    states, values, inputs, orbits = [], [], [], []
    for word in (base_word, changed_word):
        x = cylinder(word)
        inputs.append(hex(x))
        cells = [(x >> i) & 1 for i in range(2 * age + 4)]
        got, value, orbit = forward(cells, age + 1, age)
        assert got == word
        values.append(value)
        states.append(digest(orbit))
        orbits.append(orbit)
    assert int(inputs[0], 16) == window(0, 0, 2 * age + 4)
    # Independently recover the entire moving transfer vector from the
    # actual full cell histories, not merely their aggregate scores.
    direct_rows = []
    n, width = age + 1 - r, 2 * r
    for d in range(r - 2, age - 1):
        t = age - d - 2
        start = 2 * (n - t) + 2
        base, changed = orbits[0][t], orbits[1][t]
        assert base[:start] == changed[:start]
        actual_delta = as_int([a ^ b for a, b in zip(base[start:start + width], changed[start:start + width])])
        direct_rows.append([as_int(base[start - 4:start + width]), actual_delta,
                            score(base[2 * d:2 * d + 8]), score(changed[2 * d:2 * d + 8])])
    return {"base": values[0], "changed": values[1], "integers_hex": inputs,
            "observed_words": [base_word, changed_word], "cell_orbit_hashes": states,
            "moving_rows": direct_rows, "moving_rows_sha256": digest(direct_rows)}


def main():
    began = time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS, (1 << 30, 1 << 30))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    rows = []
    for r, tau, ages in CASES:
        checks = []
        for age in ages:
            transfer = transferred(r, tau, age)
            independent = literal(r, tau, age)
            assert (transfer["base"], transfer["changed"]) == (independent["base"], independent["changed"])
            assert transfer["transfer_rows"] == independent["moving_rows"]
            checks.append({"age": age, "transfer": transfer, "literal": independent})
        small, large = checks
        period = large["transfer"]["period"]
        assert ages[1] - ages[0] == period
        for index, name in ((2, "base"), (3, "changed")):
            expected = sum(v[index] for v in large["transfer"]["transfer_rows"][:period])
            assert large["transfer"][name] - small["transfer"][name] == expected
        rows.append({"r": r, "tau": tau, "checks": checks})
    summary = {"rows": rows, "all_checks_passed": True}
    sources = [Path(__file__), NOTE, ROOT / "experiments/problem1_nonperiodicity/check_terminal_branch_sensitivity_independent.py", ROOT / "src/python/rule30_research_reference.py"]
    record = {"experiment_id": "20260906_finite_suffix_defect_seams", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "question": "problem1", "hypothesis": "The finite defect state, initial-tail seams, and sufficient period match independent full cylinder/cell evolution at the four declared r2/r3 seam cases.",
              "backend": "packed-backward-defect-versus-inverse-cylinder-cell-forward", "parameters": {"cases": CASES, "wall_seconds": 120, "memory_bytes": 1 << 30, "survivor": "ut phases -7/127,-123/127 only"},
              "hardware": {"machine": platform.machine(), "logical_cpu_count": os.cpu_count(), "cpu": next((x.split(":", 1)[1].strip() for x in Path("/proc/cpuinfo").read_text().splitlines() if x.startswith("model name")), "unknown")},
              "software": {"python": platform.python_version(), "platform": platform.platform()},
              "runtime_seconds": time.monotonic() - began, "result_summary": summary,
              "result_hashes": {"summary_sha256": digest(summary)},
              "source_and_input_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
              "executed_source": Path(__file__).read_text(), "admission_snapshot": NOTE.read_text(),
              "dependency_source_snapshot": sources[2].read_text(), "status": "finite-exhaustive",
              "proof_scope": "Four fixed seam inputs and exact closure of their derived finite defect state; the all-r theorem is a separate argument.",
              "interpretation": "Both seam types agree; no inference from a width sweep or sampled absence is made.",
              "limitations": ["No ordinary-frontier membership is asserted.", "No new comparator or rational cycle is generated.", "Both independent formulations were implemented locally by the lead.", "The general all-r proof needs its separate review; this is finite verification only."]}
    assert time.monotonic() - began < 120
    atomic(OUT, record)
    print(json.dumps([{ "r": row["r"], "tau": row["tau"], "checks": [{"age": c["age"], "base": c["transfer"]["base"], "changed": c["transfer"]["changed"], "tail": [c["transfer"]["base_tail"], c["transfer"]["changed_tail"]]} for c in row["checks"]]} for row in rows]))


if __name__ == "__main__":
    main()
