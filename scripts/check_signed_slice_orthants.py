#!/usr/bin/env python3
"""Targeted orthant-union falsification; see the matching informal note."""
from __future__ import annotations

import datetime
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src/python"))
import period_two_signed_slice_transfer_check as transfer


def main():
    start = time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
    def timeout(*_):
        raise TimeoutError("120-second cap")
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(120)
    levels = {a: transfer.build_levels(a, 16, transfer.frontier_children_primary)
              for a in transfer.PHASES}
    for a in transfer.PHASES:
        other = transfer.build_levels(a, 8, transfer.oracle_frontier_children)
        assert all(other[k] == levels[a][k] for k in range(1, 9))
    occurrences, truncated, excluded = transfer.three_return_occurrences(levels, 16, 64, start)
    assert len(occurrences) == 19 and not truncated and not excluded
    ancestors = transfer.ancestor_closure(occurrences)
    assert len(ancestors) == 25
    ordered = sorted(ancestors, key=lambda t: (t[1], t[0] == "u", t[3], t[2]))
    ordered += [("u", 18, 0x642E4D2F1, 3), ("u", 18, 0x6473D46AB, 5)]
    rows = []
    first = None
    lift = transfer.load_lift_module()
    for a, k, x, depth in ordered:
        if k >= len(levels[a]):
            levels[a] = transfer.build_levels(a, k, transfer.frontier_children_primary)
        assert x in levels[a][k]
        vec, belief = transfer.slice_vector(levels[a], k, x, depth)
        recursive = transfer.belief_recursive(levels[a], k, x, depth)
        assert belief == recursive
        bins = {n: [0, 0] for n in transfer.MASK_ORDER}
        for y, cost in belief.items():
            n = transfer.fiber_mask(levels[a], k - 1, y)
            bins[n][cost % 2] += 1
        assert tuple(bins[n][0] - bins[n][1] for n in transfer.MASK_ORDER) == vec
        row = {"phase": a, "complexity": k, "state_hex": hex(x), "depth": depth,
               "vector": list(vec), "signed_mass": sum(vec), "belief_size": len(belief),
               "component_even_odd_counts": {format(n, "04b"): bins[n] for n in bins}}
        rows.append(row)
        if not (any(v > 0 for v in vec) and any(v < 0 for v in vec)):
            continue
        if k <= 16:
            original = next(o for o in sorted(occurrences)
                            if o[0] == a and o[1] >= k and o[3] >= depth
                            and o[1] - k == o[3] - depth and o[2] >> (2*(o[1]-k)) == x)
        elif x == 0x642E4D2F1:
            original = ("u", 19, 0x190B934BC7, 4)
        else:
            original = ("u", 18, 0x6473D46AB, 5)
        phase, orig_k, orig_x, orig_depth = original
        schedule = transfer.forced_zero_schedule(orig_x)
        cut = orig_depth - 1
        gaps = next(g for g, word, complete in transfer.three_return_patterns()
                    if schedule[cut:].startswith(word) and transfer.admissible(schedule[:cut] + complete))
        witness = lift.frontier_witness(phase, orig_k, orig_x)
        assert witness is not None and lift.apply_word(witness) == orig_x
        row["admissible_descendant"] = {"phase": phase, "complexity": orig_k,
            "state_hex": hex(orig_x), "depth": orig_depth, "cut": cut,
            "gaps": list(gaps), "schedule": schedule, "generator_word": witness,
            "stripped_digits": orig_k-k}
        first = row
        break
    result = {"domain_occurrences": 19, "domain_ancestors": 25,
              "planned_nodes": len(ordered), "checked_nodes": len(rows),
              "rows": rows, "first_mixed_sign_vector": first,
              "stop_reason": "first_counterexample" if first else "exhausted"}
    paths = [Path(__file__).relative_to(ROOT), Path("src/python/period_two_signed_slice_transfer_check.py"),
             Path(transfer.LIFT_MODULE_RELATIVE), Path("src/python/rule30_research_reference.py")]
    hashes = {str(p): hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    hashes["result_sha256"] = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    cpu = next(line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
               if line.startswith("model name"))
    record = {"experiment_id": "20260905_signed_slice_orthants", "question": "problem1",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "git_dirty_paths": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines(),
        "hypothesis": "Every outgoing slice vector on the three-return ancestor domain has no two components of opposite strict sign.",
        "backend": "python-distinct-frontiers-direct-and-recursive-beliefs",
        "parameters": {"domain_max_k": 16, "phases": ["p", "u"], "all_56_gap_triples": True,
                       "named_nodes_after_domain": [["u", 18, "0x642e4d2f1", 3], ["u", 18, "0x6473d46ab", 5]],
                       "wall_limit_seconds": 120, "address_space_bytes": 1024**3, "schedule_cap": 64},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        "software": {"python": sys.version, "platform": platform.platform()},
        "runtime_seconds": time.monotonic()-start, "result_hashes": hashes, "result_summary": result,
        "status": "refuted" if first else "finite-exhaustive",
        "proof_scope": "Exact named counterexample if present; finite scope is the ordered 25 existing ancestors followed by two named nodes, stopping at first failure.",
        "interpretation": "A mixed-sign vector refutes the two-orthant restriction, not signed nonvanishing.",
        "limitations": ["No all-depth nonvanishing theorem.", "No larger nonvanishing census.",
                        "No exclusion of other disconnected regions or arithmetic restrictions.",
                        "Smallest only in the expressly ordered tested set, not all admissible ancestors."]}
    destination = ROOT / "results/problem1/20260905_signed_slice_orthants.json"
    fd, tmp = tempfile.mkstemp(dir=destination.parent, prefix=destination.name+".", suffix=".tmp")
    with os.fdopen(fd, "w") as stream:
        json.dump(record, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, destination)
    signal.alarm(0)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
