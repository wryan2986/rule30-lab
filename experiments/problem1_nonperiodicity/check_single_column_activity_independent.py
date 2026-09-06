#!/usr/bin/env python3
"""Named single-column controls; no new input or age beyond the admission."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time

from check_temporal_activity_deficit_independent import (
    ROOT, INPUTS, digits, t_cells, a_cells, forced, atomic, sha, digest,
)

NOTE = ROOT / "proofs/informal/problem1_single_column_activity.md"
DEFICIT = ROOT / "results/problem1/20260906_temporal_activity_deficit_independent.json"
DEPENDENCY = Path(__file__).with_name("check_temporal_activity_deficit_independent.py")
OUT = ROOT / "results/problem1/20260906_single_column_activity_independent.json"


def activity(cells, s):
    if s == 0:
        return []
    assert len(cells) >= 2 * s + 1
    row, vector = cells[:], []
    for _ in range(s):
        vector.append(row[2 * s])
        row = t_cells(row)
    return vector


def run():
    started = time.monotonic()
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_AS, (1024 ** 3, 1024 ** 3))
    deficit_bytes = DEFICIT.read_bytes()
    deficit = json.loads(deficit_bytes)
    for key, expected in deficit["result_hashes"].items():
        assert digest(deficit["results"][key]) == expected
    old_z = {(r["input"], r["s"]): r["Z"] for r in deficit["results"]["rows"]}
    rows, bounds, comparisons = [], [], []
    for label, numerator, denominator in INPUTS:
        values = []
        if denominator == 1 and numerator >= 0:
            entry = (0, numerator)
        elif label in ("-1", "-2", "-3"):
            entry = (1, -numerator)
        elif label == "-1/7":
            entry = (2, 1)
        else:
            entry = None
        for s in range(17):
            vector = activity(digits(numerator, denominator, 2 * s + 1), s)
            v = sum(vector)
            values.append(v)
            rows.append({"input": label, "s": s, "temporal_bits": vector, "V": v})
            if entry is not None:
                h, finite = entry
                k = (finite.bit_length() + 1) // 2
                bound = min(s, max(h, k - 1))
                assert v <= bound
                bounds.append([label, s, h, k, v, bound])
            if label in ("0", "1", "2", "3"):
                assert v == 0
            if label in ("-1", "-2", "-3"):
                assert v == int(s > 0)
            if label == "-1/7":
                assert v == (0 if s <= 1 else 1 + int(s % 3 == 0))
            if label == "1/3":
                assert v == s // 2
            if label == "-1/3":
                assert v == (s + 1) // 2
            if s > 0:
                assert v <= 2 * old_z[label, s] + 1
        for s in range(1, 15):
            upper = values[s - 1] + 3 * values[s] + 3 * values[s + 1] + 2 * values[s + 2] + 2
            assert old_z[label, s] <= upper
            comparisons.append([label, s, values[s], old_z[label, s], upper])

    seams = []
    for x in (7, 43):
        for s in range(1, 16):
            cells = digits(x, 1, 2 * s + 4)
            next_cells = forced(cells)
            vx = sum(activity(cells, s + 1))
            vf = sum(activity(next_cells, s))
            b0, b1 = cells[2 * s + 2], t_cells(cells)[2 * s + 2]
            aged = cells[:]
            for _ in range(s + 1):
                aged = a_cells(aged)
            end = aged[0]
            assert vx - vf == b0 + b1 - end
            assert -1 <= vx - vf <= 2
            seams.append({"x": x, "s": s, "V_next_age": vx, "V_forced": vf,
                          "initial_bit": b0, "next_bit": b1, "aged_bit": end,
                          "difference": vx - vf})

    result = {"rows": rows, "entry_bounds": bounds, "comparisons": comparisons, "seams": seams}
    source, admission, dependency = Path(__file__).read_bytes(), NOTE.read_bytes(), DEPENDENCY.read_bytes()
    runtime = time.monotonic() - started
    assert runtime < 120
    record = {
        "experiment_id": "20260906-single-column-activity-independent",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "Single-column finite-entry bound, comparison with D deficit, and exact first-gate seam",
        "backend": "independent-python-cell-arrays-rational-long-division",
        "parameters": {"inputs": [r[0] for r in INPUTS], "ages": [0, 16],
                       "comparison_ages": [1, 14], "seam_inputs": [7, 43], "seam_ages": [1, 15],
                       "cpu_concurrency": 1, "memory_cap_bytes": 1024 ** 3, "wall_cap_seconds": 120},
        "hardware": {"machine": platform.machine(), "processor": platform.processor(), "logical_cpus": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": runtime,
        "result_hashes": {key: digest(value) for key, value in result.items()},
        "result_summary": {"rows": len(rows), "entry_bounds": len(bounds), "comparisons": len(comparisons),
                           "seams": len(seams), "all_checks_passed": True},
        "interpretation": "Finite identities on the named inputs only; actual record growth and all-depth transitions need proof.",
        "status": "finite-exhaustive",
        "proof_scope": "Exactly twelve rational controls, ages0..16, and the declared comparison/seam subranges.",
        "limitations": ["No new survivor, period, frontier, occurrence, or memory sweep.",
                        "This is independent of the primary modular implementation but reuses the earlier cell helpers.",
                        "No infinite claim follows from finite agreement."],
        "provenance": {"source_path": str(Path(__file__).relative_to(ROOT)), "source_sha256": sha(source), "source": source.decode(),
                       "admission_path": str(NOTE.relative_to(ROOT)), "admission_sha256": sha(admission), "admission": admission.decode(),
                       "dependency_path": str(DEPENDENCY.relative_to(ROOT)), "dependency_sha256": sha(dependency), "dependency": dependency.decode(),
                       "deficit_record_path": str(DEFICIT.relative_to(ROOT)), "deficit_record_sha256": sha(deficit_bytes),
                       "reference_sha256": sha((ROOT / "src/python/rule30_research_reference.py").read_bytes())},
        "results": result,
    }
    atomic(OUT, record)
    print(json.dumps(record["result_summary"], sort_keys=True))


if __name__ == "__main__":
    run()
