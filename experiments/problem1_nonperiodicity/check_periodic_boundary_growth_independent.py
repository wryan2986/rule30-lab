#!/usr/bin/env python3
"""Independent cell-vector replay of the admitted periodic boundary law."""
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import time
from datetime import datetime, timezone
from fractions import Fraction

from check_boundary_sum_periodic_tails import atomic, digest

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "results/problem1/20260905_periodic_rational_primary.json"
NOTE = ROOT / "proofs/informal/problem1_periodic_boundary_growth.md"


def run(row):
    word, a, lam = row["q"], row["spatial_onset"], row["lambda"]
    columns = row["columns"]
    p = len(word)
    d0 = (a + 1) // 2
    m = lam // math.gcd(lam, 2)
    period = math.lcm(p, m)

    def bit(phase, position):
        n = position if position < a else a + (position - a) % lam
        return (columns[n] >> (phase % p)) & 1

    def jscore(phase, d):
        cells = [bit(phase, 2 * d + i) for i in range(8)]
        av = sum((cells[i + 2] ^ (cells[i + 1] | cells[i])) << i for i in range(6))
        pv = sum(cells[i + 2] << i for i in range(6))
        return int(av in (0, 5)) + int(pv in (0, 5))

    for phase, letter in enumerate(word):
        residue = sum(bit(phase, i) << i for i in range(4))
        assert residue == {"u": 7, "t": 11}[letter]

    rows, prefixes, period_checks = [], [], 0
    for e in range(p):
        w = [jscore(e - d, d) for d in range(d0 + 3 * period)]
        for d in range(d0, d0 + 2 * period):
            assert w[d] == w[d + period]
            period_checks += 1
        pr = [0]
        for value in w:
            pr.append(pr[-1] + value)
        prefixes.append(pr)
        total = sum(w[d0:d0 + period])
        mu = Fraction(total, period)
        offsets = [Fraction(pr[d0 + r]) - mu * (d0 + r) for r in range(period)]
        rows.append({"ending_phase": e, "M": total, "mean": str(mu),
                     "initial_scores": w[:d0], "period_scores": w[d0:d0 + period],
                     "offset_min": str(min(offsets)), "offset_max": str(max(offsets))})
    for e in range(p):
        assert rows[e]["M"] == rows[(e + m) % p]["M"]

    age_checks, direct_checks = 0, 0
    for start_phase in range(p):
        for s in range(d0 + 1, d0 + period + 2):
            e = (start_phase + s - 2) % p
            assert prefixes[e][s + period - 1] - prefixes[e][s - 1] == rows[e]["M"]
            age_checks += 1
        ages = sorted({1, max(1, d0), d0 + 1, d0 + period, d0 + period + 1, d0 + 2 * period + 1})
        for s in ages:
            direct = sum(jscore(start_phase + t, s - t - 2) for t in range(s - 1))
            e = (start_phase + s - 2) % p
            assert direct == prefixes[e][s - 1]
            direct_checks += 1
    repeated = word * (2 + 6 // p)
    adm = not any(bad in repeated for bad in ("uu", "ttttt", "ututtu"))
    return {"word": word, "p": p, "spatial_onset": a, "spatial_period": lam,
            "d0": d0, "m": m, "L": period, "phase_classes": math.gcd(p, m),
            "admissible": adm, "phases": rows, "score_period_checks": period_checks,
            "age_increment_checks": age_checks, "direct_forward_checks": direct_checks,
            "admissible_countermodel": adm and any(r["M"] >= period for r in rows)}


def main():
    began = time.monotonic()
    old = json.loads(INPUT.read_text())["result_summary"]["rows"]
    inputs = [{k: r[k] for k in ("q", "spatial_onset", "lambda", "columns")} for r in old]
    inputs.append({"q": "ut", "spatial_onset": 0, "lambda": 7,
                   "columns": [((7 >> i) & 1) | (((123 >> i) & 1) << 1) for i in range(7)]})
    rows = [run(r) for r in inputs]
    assert next(r for r in rows if r["word"] == "ut")["phases"][0]["mean"] == "1/14"
    summary = {"rows": rows, "countermodels": [r["word"] for r in rows if r["admissible_countermodel"]],
               "all_checks_passed": True}
    paths = [Path(__file__), INPUT, NOTE,
             ROOT / "experiments/problem1_nonperiodicity/check_boundary_sum_periodic_tails.py",
             ROOT / "proofs/informal/problem1_periodic_schedule_rationality.md",
             ROOT / "proofs/informal/problem1_critical_cost_schedule_identity.md",
             ROOT / "src/python/rule30_research_reference.py"]
    cpu = next((x.split(":", 1)[1].strip() for x in Path("/proc/cpuinfo").read_text().splitlines() if x.startswith("model name")), "unknown")
    record = {
        "experiment_id": "20260906_periodic_boundary_growth_independent",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1", "hypothesis": "The exact eventual score-period and phase-dependent age increment hold on the five admitted stored periodic survivors; a mean>=1 would refute a schedule-only subunit bound.",
        "backend": "python-cell-vectors",
        "parameters": {"words": [r["q"] for r in inputs], "input_domain": "stored spatial vector certificates only", "age_checks": "all starting phases, s=d0+1 through d0+L+1, plus six direct forward boundary ages", "wall_seconds": 120, "memory_limit_gib": 1},
        "hardware": {"cpu": cpu, "machine": platform.machine(), "logical_cpu_count": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": time.monotonic() - began,
        "source_and_input_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        "admission_snapshot": NOTE.read_text(), "executed_source": Path(__file__).read_text(),
        "input_vector_snapshots": inputs,
        "result_summary": summary, "result_hashes": {"summary_sha256": digest(summary)},
        "status": "finite-exhaustive", "proof_scope": "Exact finite replay on five named periodic schedules, with no recurrence or cycle generation. All-period inference uses the separate proof.",
        "interpretation": "The named phase means are exact controls, not a uniform bound on arbitrary schedules.",
        "limitations": ["No ordinary endpoint or finite-seed trajectory is asserted.", "No new spatial period or schedule is searched.", "Stored vector certificates are reused without regenerating their cycles.", "The independent cell replay is lead-local; primary modular implementation and external proof review are recorded separately.", "Base Git plus exact source hashes identify the uncommitted research inputs."]}
    assert time.monotonic() - began < 120
    atomic(ROOT / "results/problem1/20260906_periodic_boundary_growth_independent.json", record)
    print(json.dumps([{k: r[k] for k in ("word", "L", "phase_classes", "admissible")} | {"M": [x["M"] for x in r["phases"]], "means": [x["mean"] for x in r["phases"]]} for r in rows]))


if __name__ == "__main__":
    main()
