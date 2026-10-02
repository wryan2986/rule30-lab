#!/usr/bin/env python3
"""Bounded adversarial checks of the cyclic blind-cone lemma.

Admission: a counterexample kills the proposed cone/spacing proof. Passing
these exact finite domains supports auditing that proof; it proves no
infinite statement. The primary implementation evolves two original rows,
independently of the polynomial difference recurrence being checked.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
REFERENCE_HASH = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"


def step(state: tuple[int, ...], label: int) -> tuple[int, ...]:
    """Apply Rule 30 separately to the two halves, then normalize."""
    if label not in (0, 1) or not state or len(state) % 2 or any(bit not in (0, 1) for bit in state):
        raise ValueError("state must be a nonempty flat tuple (X1,Y1,...,Xr,Yr) of binary bits; label must be binary")
    pairs = [(1, 0), (0, 1)] + list(zip(state[::2], state[1::2]))
    output = []
    for j in range(2, len(pairs)):
        h, l, x = pairs[j - 2:j + 1]
        first = h[0] ^ (l[0] | x[0])
        second = (h[0] ^ h[1]) ^ ((l[0] ^ l[1]) | (x[0] ^ x[1]))
        difference = first ^ second
        output.extend((first ^ (label & difference), difference))
    return tuple(output)


def blind(state: tuple[int, ...]) -> bool:
    return step(state, 0) == step(state, 1)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
            temporary = Path(f.name)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
        temporary = None
        fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-r", type=int, default=8)
    parser.add_argument("--comparison-r", type=int, default=6)
    parser.add_argument("--max-cyclic-period", type=int, default=3)
    parser.add_argument("--max-seconds", type=float, default=60)
    parser.add_argument("--max-memory-mib", type=int, default=256)
    parser.add_argument("--max-output-kib", type=int, default=128)
    parser.add_argument("--output", type=Path, default=ROOT / "results/problem1/20261002_cyclic_blind_cone_independent.json")
    args = parser.parse_args()
    if not (1 <= args.max_r <= 8 and 1 <= args.comparison_r <= 6 and 1 <= args.max_cyclic_period <= 3):
        parser.error("This verifier admits only r<=8, comparison r<=6, cyclic p<=3.")
    if args.max_seconds <= 0 or args.max_memory_mib <= 0 or args.max_output_kib <= 0:
        parser.error("Resource caps must be positive.")
    resource.setrlimit(resource.RLIMIT_AS, (args.max_memory_mib * 2**20,) * 2)
    started = time.monotonic()

    def cap() -> None:
        if time.monotonic() - started > args.max_seconds:
            raise TimeoutError("wall-time cap reached; no final record written")

    def require(condition: bool, **witness: object) -> None:
        if not condition:
            raise AssertionError(json.dumps(witness, sort_keys=True))

    source_paths = [
        Path(__file__).resolve(),
        ROOT / "experiments/problem1_nonperiodicity/analyze_portal_multilift_phase_quotient.py",
        ROOT / "src/python/rule30_research_reference.py",
    ]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    require(hashes["src/python/rule30_research_reference.py"] == REFERENCE_HASH, stage="immutable reference hash")
    spec = importlib.util.spec_from_file_location("existing_quotient", source_paths[1])
    existing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(existing)

    # Hand controls: blind raw 11 -> 00; either next label gives Y_1=1.
    require(step((1, 1), 0) == (0, 0), stage="hand control 11")
    require(step((1, 1), 1) == (0, 0), stage="hand control half-swap")
    require(step((0, 0), 0) == (1, 1), stage="hand control 00 label0")
    require(step((0, 0), 1) == (0, 1), stage="hand control 00 label1")
    tight_paths = [((0, 0), (1, 1)), ((0, 0, 1, 0), (1, 1, 1, 1))]
    for path in tight_paths:
        require(step(path[0], 0) == path[1] and step(path[1], 1) == path[0], stage="sharp gap two", path=path)
        require(sum(blind(state) for state in path) == 1, stage="sharp blind count", path=path)
    # One named review control, not a period-12 state-space census.
    review_path = [(0, 0), (1, 1)] * 6
    odd_realizations = 0
    for labels in itertools.product((0, 1), repeat=12):
        if sum(labels) % 2 and all(step(review_path[s], labels[s]) == review_path[(s+1) % 12] for s in range(12)):
            odd_realizations += 1
    require(odd_realizations == 32, stage="dimension versus count review control", odd_realizations=odd_realizations)

    transition_cases = projection_cases = no_consecutive_cases = raw_blind_states = 0
    for r in range(1, args.comparison_r + 1):
        for state in itertools.product((0, 1), repeat=2*r):
            cap()
            is_blind = blind(state)
            raw_blind_states += is_blind
            for label in (0, 1):
                successor = step(state, label)
                require(successor == existing.transition(state, label), stage="independent transition", r=r, state=state, label=label)
                transition_cases += 1
                if r > 1:
                    require(successor[:-2] == step(state[:-2], label), stage="projectivity", r=r, state=state, label=label)
                    require(not is_blind or blind(state[:-2]), stage="blind nesting", r=r, state=state)
                    projection_cases += 1
                if is_blind:
                    require(not blind(successor), stage="consecutive blind", r=r, state=state, label=label)
                    no_consecutive_cases += 1

    cone_rows = []
    for r in range(1, args.max_r + 1):
        histories = observations = 0
        for xs in itertools.product((0, 1), repeat=r):
            for labels in itertools.product((0, 1), repeat=r//2):
                cap()
                state = tuple(bit for x in xs for bit in (x, 0))
                for t in range(r//2 + 1):
                    if t:
                        require(state[4*t-1] == 1, stage="cone front", r=r, xs=xs, labels=labels, t=t, state=state)
                    require(all(state[2*j-1] == 0 for j in range(2*t+1, r+1)), stage="cone zero tail", r=r, xs=xs, labels=labels, t=t, state=state)
                    observations += 1
                    if t < len(labels):
                        state = step(state, labels[t])
                histories += 1
        cone_rows.append({"r": r, "histories": histories, "time_observations": observations})

    cycle_rows = []
    for p in range(1, args.max_cyclic_period + 1):
        for r in range(1, 2*p+1):
            g = max(2, r//2+1)
            orbit_labels = {}
            attempted = cycle_cases = max_k = 0
            for labels in itertools.product((0, 1), repeat=p):
                for initial in itertools.product((0, 1), repeat=2*r):
                    cap()
                    attempted += 1
                    state, path = initial, []
                    for label in labels:
                        path.append(state)
                        state = step(state, label)
                    if state != initial:
                        continue
                    cycle_cases += 1
                    phases = [s for s, value in enumerate(path) if blind(value)]
                    require(len(phases) <= p//g, stage="cyclic count", p=p, r=r, labels=labels, initial=initial, phases=phases)
                    if phases:
                        gaps = [(phases[(i+1) % len(phases)]-s) % p or p for i, s in enumerate(phases)]
                        require(min(gaps) >= g, stage="cyclic wrap spacing", p=p, r=r, labels=labels, initial=initial, phases=phases, gaps=gaps)
                    max_k = max(max_k, len(phases))
                    orbit_labels.setdefault(tuple(path), []).append(labels)
            for path, labelings in orbit_labels.items():
                k = sum(blind(value) for value in path)
                require(len(labelings) == 2**k, stage="aligned ambiguity cube", p=p, r=r, path=path, labelings=labelings, k=k)
                odd = sum(sum(labels) % 2 for labels in labelings)
                require(odd == 2**(k-1) if k else odd in (0, 1), stage="odd ambiguity cube", p=p, r=r, k=k, odd=odd)
            cycle_rows.append({"p": p, "r": r, "driver_initial_pairs": attempted, "cyclic_pairs": cycle_cases, "aligned_orbits": len(orbit_labels), "max_k": max_k, "gap_bound": g})

    # Exact algebraic ledger identity only; not a census of longer-period orbits.
    charge_formula_checks = 0
    for p in range(1, 257):
        direct = sum(max(p // max(2, r//2+1)-1, 0) for r in range(1, 2*p+1))
        closed = 0 if p == 1 else 2*sum(p//q for q in range(1, p+1))-4*p+p//2+1
        require(direct == closed, stage="charge sum formula", p=p, direct=direct, closed=closed)
        charge_formula_checks += 1

    payload = {
        "transition_cases": transition_cases, "projection_cases": projection_cases,
        "raw_blind_states": raw_blind_states, "no_consecutive_cases": no_consecutive_cases,
        "cone_domains": cone_rows, "cyclic_domains": cycle_rows,
        "charge_formula_integer_checks": charge_formula_checks,
        "review_controls": {"sharp_gap_two_depths": [1, 2], "period12_single_named_orbit": {"tested_label_words": 4096, "blind_phases": 6, "odd_realizations": odd_realizations, "odd_affine_dimension": 5}},
        "counterexamples": [],
    }
    record = {
        "experiment_id": "cyclic-blind-cone-independent-20261002",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1", "hypothesis": "Zero difference cone; cyclic blind gap >= max(2,floor(r/2)+1); unrestricted aligned ambiguity cube.",
        "backend": "independent scalar two-row Rule30 Python",
        "parameters": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
        "hardware": {"machine": platform.machine(), "processor": platform.processor(), "logical_cpu_count": os.cpu_count()},
        "software": {"python": sys.version, "platform": platform.platform()},
        "runtime_seconds": time.monotonic()-started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "source_hashes": hashes,
        "result_hashes": {"canonical_payload_sha256": hashlib.sha256(canonical_bytes(payload)).hexdigest()},
        "result_summary": payload, "status": "finite-exhaustive",
        "proof_scope": "Only the finite domains explicitly listed in result_summary.",
        "interpretation": "No counterexample within exact bounds. The separate all-depth proof must be audited logically.",
        "limitations": ["No all-period claim follows from these enumerations.", "No full-period portal connectors were searched.", "No original-support charge, FULL contradiction, or Prize Problem solution is established."],
    }
    data = json.dumps(record, sort_keys=True, indent=2).encode()+b"\n"
    if len(data) > args.max_output_kib * 1024:
        raise RuntimeError("output cap reached; no record written")
    cap()
    atomic_write(args.output, data)
    print(json.dumps({"output": str(args.output), "runtime_seconds": record["runtime_seconds"], "canonical_payload_sha256": record["result_hashes"]["canonical_payload_sha256"], "transition_cases": transition_cases, "cone_histories": sum(row["histories"] for row in cone_rows), "cyclic_pairs": sum(row["cyclic_pairs"] for row in cycle_rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
