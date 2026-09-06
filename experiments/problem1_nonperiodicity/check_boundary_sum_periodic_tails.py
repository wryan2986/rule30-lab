#!/usr/bin/env python3
"""Exact, bounded periodic-tail falsification test; see the admission note."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[2]
MAX_PERIOD = 12
START = time.monotonic()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def ror(a, shift, p):
    shift %= p
    return ((a >> shift) | (a << (p - shift))) & ((1 << p) - 1)


def packed_a(a, p):
    return ror(a, 2, p) ^ (ror(a, 1, p) | a)


def packed_r(a, p):
    return ror(packed_a(packed_a(a, p), p), -2, p)


def cell_a(a, p):
    cells = [(a >> i) & 1 for i in range(p)]
    return sum((cells[(i + 2) % p] ^ (cells[(i + 1) % p] | cells[i])) << i for i in range(p))


def cell_r(a, p):
    # First A is computed from cells. The second stage is cyclic T,
    # independently of the rotate(A(A(a))) expression used above.
    middle = [(cell_a(a, p) >> i) & 1 for i in range(p)]
    return sum((middle[i] ^ (middle[(i - 1) % p] | middle[(i - 2) % p])) << i for i in range(p))


def low(a, p, width):
    return sum(((a >> (i % p)) & 1) << i for i in range(width))


def gate(a, p):
    return {7: "u", 11: "t"}.get(low(a, p, 4))


def canonical(cycle):
    i = cycle.index(min(cycle))
    return cycle[i:] + cycle[:i]


def primary_cycles(edges):
    degree = {v: 0 for v in edges}
    for dest in edges.values():
        if dest in degree:
            degree[dest] += 1
    queue = [v for v in degree if degree[v] == 0]
    removed = set()
    while queue:
        v = queue.pop()
        removed.add(v)
        dest = edges[v]
        if dest in degree:
            degree[dest] -= 1
            if degree[dest] == 0:
                queue.append(dest)
    cycles, visited = [], set()
    for start in sorted(set(edges) - removed):
        if start in visited:
            continue
        path, local = [], {}
        v = start
        while v in edges and v not in local and v not in visited:
            local[v] = len(path)
            path.append(v)
            v = edges[v]
        if v in local:
            cycles.append(canonical(path[local[v]:]))
        visited.update(path)
    return sorted(cycles)


def independent_cycles(edges):
    # Follow every root independently; do not use pruning or a global
    # visited set. The cap here is a mathematical finite set, not a timeout.
    found = set()
    for start in edges:
        positions, word = {}, []
        v = start
        while v in edges and v not in positions:
            positions[v] = len(word)
            word.append(v)
            v = edges[v]
        if v in positions:
            found.add(tuple(canonical(word[positions[v]:])))
    return [list(c) for c in sorted(found)]


def admissible(word):
    repeated = word * (2 + 6 // len(word))
    return all(bad not in repeated for bad in ("uu", "ttttt", "ututtu"))


def score(a, p, independent=False):
    if independent:
        cells = [(a >> i) & 1 for i in range(p)]
        first = sum((cells[(i + 2) % p] ^ (cells[(i + 1) % p] | cells[i % p])) << i for i in range(6))
        second = sum(cells[(i + 2) % p] << i for i in range(6))
        return int(first in (0, 5)) + int(second in (0, 5))
    return int(low(packed_a(a, p), p, 6) in (0, 5)) + int(low(ror(a, 2, p), p, 6) in (0, 5))


def cycle_record(cycle, p, independent):
    letters = "".join(gate(a, p) for a in cycle)
    result = {"states": cycle, "branches": letters, "admissible": admissible(letters)}
    if not result["admissible"]:
        return result
    alignment_period = p // math.gcd(p, 2)
    joint_period = math.lcm(len(cycle), alignment_period)
    totals = []
    for h in range(alignment_period):
        terms = []
        for t in range(joint_period):
            a = cycle[t % len(cycle)]
            shift = 2 * (h - t)
            if independent:
                y = sum(((a >> ((i + shift) % p)) & 1) << i for i in range(p))
            else:
                y = ror(a, shift, p)
            terms.append(score(y, p, independent))
        totals.append(sum(terms))
    result.update(alignment_period=alignment_period, joint_period=joint_period,
                  score_totals=totals, means=[str(Fraction(x, joint_period)) for x in totals],
                  refutes_uniform_subunit=any(x >= joint_period for x in totals))
    return result


def run(independent):
    rows, total_states, map_rows = [], 0, []
    amap = cell_a if independent else packed_a
    rmap = cell_r if independent else packed_r
    finder = independent_cycles if independent else primary_cycles
    assert [amap(7, 4), amap(11, 4), rmap(7, 4), rmap(11, 4)] == [2, 1, 14, 7]
    for p in range(1, MAX_PERIOD + 1):
        edges = {}
        for a in range(1 << p):
            ar, rr = amap(a, p), rmap(a, p)
            map_rows.append([p, a, ar, rr, score(a, p, independent)])
            total_states += 1
            if gate(a, p) and gate(rr, p):
                edges[a] = rr
            if time.monotonic() - START > 120:
                raise TimeoutError("Admitted total wall limit exceeded")
        cycles = finder(edges)
        records = [cycle_record(cycle, p, independent) for cycle in cycles]
        rows.append({"spatial_period": p, "states": 1 << p,
                     "edges_with_gates_at_both_ends": len(edges), "cycles": records})
        if any(c.get("refutes_uniform_subunit") for c in records):
            break
    return {"rows": rows, "states_checked": total_states, "map_hash": digest(map_rows),
            "cycles_checked": sum(len(r["cycles"]) for r in rows),
            "admissible_cycles": sum(c["admissible"] for r in rows for c in r["cycles"]),
            "countermodels": [[r["spatial_period"], c] for r in rows for c in r["cycles"] if c.get("refutes_uniform_subunit")]}


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(value, f, sort_keys=True, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    source_paths = [Path(__file__).relative_to(ROOT),
                    Path("proofs/informal/problem1_boundary_sum_periodic_tail_probe.md"),
                    Path("proofs/informal/problem1_critical_cost_schedule_identity.md"),
                    Path("src/python/rule30_research_reference.py")]
    cpu = next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines() if line.startswith("model name")), "unknown")
    common = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1", "hypothesis": "An admissible pure spatially periodic forced cycle has boundary-sum mean at least one in some alignment.",
        "parameters": {"spatial_periods": [1, MAX_PERIOD], "alphabet": ["t", "u"],
                       "forbidden_cyclic_factors": ["uu", "ttttt", "ututtu"], "stop": "first completed spatial period with countermodel, else period 12", "wall_seconds": 120, "memory_limit_gib": 1},
        "hardware": {"machine": platform.machine(), "cpu": cpu, "logical_cpu_count": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "source_hashes": {str(p): hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths},
        "admission_snapshot": (ROOT / source_paths[1]).read_text(),
        "executed_source": Path(__file__).read_text(),
        "status": "finite-exhaustive",
        "proof_scope": "Only pure spatially periodic 2-adic tails in the exact declared finite graph. Cycle arithmetic certifies all ages for a retained cycle, not general ordinary histories.",
        "limitations": ["No finite-seed or ordinary-frontier membership is asserted.", "No larger spatial period or nonperiodic tail is covered.", "Both implementations are lead-local; external review is separately recorded.", "Git names the base checkpoint; exact uncommitted source contents are identified by hashes."]}
    summaries = []
    for independent in (False, True):
        began = time.monotonic()
        summary = run(independent)
        elapsed = time.monotonic() - began
        summaries.append(summary)
        name = "independent" if independent else "primary"
        record = dict(common, experiment_id=f"20260906_boundary_periodic_tails_{name}",
                      backend="python-cell" if independent else "python-packed",
                      runtime_seconds=elapsed, result_summary=summary,
                      result_hashes={"summary_sha256": digest(summary)},
                      interpretation="Exact periodic-tail countermodel found." if summary["countermodels"] else "No countermodel in this admitted periodic-tail class; the proposed general bound remains unproved.")
        atomic(ROOT / f"results/problem1/20260906_boundary_periodic_tails_{name}.json", record)
    assert summaries[0] == summaries[1], "Independent implementations disagree"
    print(json.dumps({"states": summaries[0]["states_checked"], "cycles": summaries[0]["cycles_checked"],
                      "admissible_cycles": summaries[0]["admissible_cycles"],
                      "countermodels": summaries[0]["countermodels"],
                      "runtime_seconds": time.monotonic() - START}, sort_keys=True))


if __name__ == "__main__":
    main()
