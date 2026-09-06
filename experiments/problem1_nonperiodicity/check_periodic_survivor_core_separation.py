#!/usr/bin/env python3
"""Compare existing cores with two exact rational survivors; no frontier run."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import time
from datetime import datetime, timezone

from check_boundary_sum_periodic_tails import atomic, digest

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "results/problem1/20260905_frontier_head_primary.json"
ADMISSION = ROOT / "proofs/informal/problem1_periodic_survivor_core_separation.md"


def packed_residues(b):
    values = set()
    for a in (7, 123):
        word = sum(a << (7 * i) for i in range((b + 12) // 7 + 1))
        for shift in range(7):
            values.add((word >> shift) & ((1 << b) - 1))
    return values


def rational_residues(b):
    # Compute the 2-adic rational first at sufficient precision, then
    # project. This does not use repeated words or circular bit shifts.
    modulus = 2 ** (b + 6)
    return {((-a * pow(127, -1, modulus)) % modulus // 2 ** shift) % (2 ** b)
            for a in (7, 123) for shift in range(7)}


def compare(cores, independent):
    rows = []
    residues = rational_residues if independent else packed_residues
    for phase in ("p", "u"):
        for h in range(1, 9):
            data = cores[phase][str(h)]
            core = data["core"]
            assert data["status"] == "complete"
            entries = []
            for b in range(1, data["width"] + 1):
                tail = residues(b)
                cr = {x % (2 ** b) for x in core}
                overlap = sorted(tail & cr)
                entries.append({"bits": b, "core_residues": sorted(cr),
                                "tail_residues": sorted(tail), "overlap": overlap,
                                "disjoint": not overlap})
            separate = [e["bits"] for e in entries if e["disjoint"]]
            first = min(separate) if separate else None
            rows.append({"phase": phase, "h": h, "width": data["width"],
                         "core": core, "stabilization_age": data["first_stabilization_time"],
                         "entries": entries, "first_separating_bits": first,
                         "minimum_initial_k": h + data["first_stabilization_time"],
                         "alternating_prefix_bound_k_minus": h + 2 - (first + 1) // 2 if first else None})
    return rows


def main():
    started = time.monotonic()
    cores = json.loads(INPUT.read_text())["result_summary"]["head_data"]["cores"]
    assert packed_residues(1) == rational_residues(1) == {0, 1}
    assert (-7 * pow(127, -1, 16384)) % 16384 == 903
    assert (-7 * pow(127, -1, 65536)) % 65536 == 50055
    first_started = time.monotonic()
    primary = compare(cores, False)
    first_time = time.monotonic() - first_started
    second_started = time.monotonic()
    independent = compare(cores, True)
    second_time = time.monotonic() - second_started
    assert primary == independent
    summary = {"cores": len(primary), "entries": sum(len(r["entries"]) for r in primary),
               "rows": primary, "independent_agreement": True}
    paths = [Path(__file__), ADMISSION, INPUT,
             ROOT / "experiments/problem1_nonperiodicity/check_boundary_sum_periodic_tails.py",
             ROOT / "proofs/informal/problem1_frontier_head_dynamics.md",
             ROOT / "proofs/informal/problem1_boundary_sum_periodic_tail_probe.md",
             ROOT / "src/python/rule30_research_reference.py"]
    cpu = next((x.split(":", 1)[1].strip() for x in Path("/proc/cpuinfo").read_text().splitlines() if x.startswith("model name")), "unknown")
    record = {
        "experiment_id": "20260906_periodic_survivor_core_separation",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1", "hypothesis": "Existing ordinary leading cores separate all rotations of the two rational alternating-branch survivors at a useful residue width.",
        "backend": "python-packed-and-rational",
        "parameters": {"phases": ["p", "u"], "h": [1, 8], "b": "1 through each stored core's bit width", "survivors": ["-7/127", "-123/127"], "shifts": [0, 6], "wall_seconds": 120, "memory_limit_gib": 1},
        "hardware": {"cpu": cpu, "machine": platform.machine(), "logical_cpu_count": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": time.monotonic() - started,
        "implementation_runtimes": {"packed": first_time, "rational": second_time},
        "source_and_input_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        "admission_snapshot": ADMISSION.read_text(), "executed_source": Path(__file__).read_text(),
        "input_core_snapshot": cores,
        "result_hashes": {"primary_sha256": digest(primary), "independent_sha256": digest(independent), "summary_sha256": digest(summary)},
        "result_summary": summary, "status": "finite-exhaustive",
        "interpretation": "Exact disjointness entries combine with the existing all-depth head theorem; the proof and scope are separate from this finite comparison.",
        "proof_scope": "Only the 16 already committed cores and declared residue comparisons; no new states or schedules.",
        "limitations": ["No arbitrary-return or whole-tail exclusion.", "The source core construction is reused, not rerun.", "Both implementations are lead-local.", "Base Git and source hashes jointly identify the uncommitted research inputs."]}
    assert time.monotonic() - started < 120
    atomic(ROOT / "results/problem1/20260906_periodic_survivor_core_separation.json", record)
    print(json.dumps([{k: r[k] for k in ("phase", "h", "first_separating_bits", "minimum_initial_k", "alternating_prefix_bound_k_minus")} for r in primary]))


if __name__ == "__main__":
    main()
