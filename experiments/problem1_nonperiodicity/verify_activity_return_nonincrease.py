#!/usr/bin/env python3
"""Compare the two existing named certificates; no new scientific domain."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
PRIMARY = ROOT / "results/problem1/20260906_activity_return_nonincrease_primary.json"
INDEPENDENT = ROOT / "results/problem1/20260906_activity_return_nonincrease_independent.json"
OUT = ROOT / "results/problem1/20260906_activity_return_nonincrease_verification.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(obj):
    return sha(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def a_cells_integer(x):
    # Local cell rule, independent of packed T>>2.
    digits = [int(c) for c in reversed(bin(x)[2:])] + [0, 0]
    return sum((digits[i + 2] ^ max(digits[i + 1], digits[i])) * 2 ** i
               for i in range(len(digits) - 2))


def a_iter(x, n):
    for _ in range(n):
        x = a_cells_integer(x)
    return x


def main():
    start = time.monotonic()
    pb, ib = PRIMARY.read_bytes(), INDEPENDENT.read_bytes()
    p, independent = json.loads(pb), json.loads(ib)
    assert sha(json.dumps(p["checks"], sort_keys=True).encode()) == p["result_hashes"]["primary_payload_sha256"]
    assert canonical(independent["results"]) == independent["result_hashes"]["results_sha256"]
    assert canonical(independent["result_summary"]) == independent["result_hashes"]["summary_sha256"]
    for text, expected in ((p["self_source"]["embedded_text"], p["self_source"]["sha256"]),
                           (p["admission"]["note_text"], p["admission"]["note_sha256"]),
                           (independent["provenance"]["source"], independent["provenance"]["source_sha256"]),
                           (independent["provenance"]["admission"], independent["provenance"]["admission_sha256"])):
        assert sha(text.encode()) == expected
    for relative, expected in ((p["self_source"]["path"], p["self_source"]["sha256"]),
                               (independent["provenance"]["source_path"], independent["provenance"]["source_sha256"])):
        assert sha((ROOT / relative).read_bytes()) == expected
    reference = sha((ROOT / "src/python/rule30_research_reference.py").read_bytes())
    assert reference == p["reference"]["sha256"] == independent["provenance"]["reference_sha256"]
    assert reference == "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
    assert p["checks"]["orbit"] == [r["x_hex"] for r in independent["results"]["orbit"]]
    assert p["checks"]["final_gate_unexecuted"] == 7
    rows, direct_count, tail_count = [], 0, 0
    for r in (4, 10):
        pc = p["checks"]["x" + str(r)]["cert"]
        ic = independent["results"]["certificates"][str(r)]
        n = 17 + r
        assert pc["n"] == ic["n"] == n
        assert p["result_summary"]["x" + str(r) + "_n"] == n
        assert [row["temporal_bits"] for row in pc["direct"]] == ic["direct_temporal_vectors"]
        assert [row["V"] for row in pc["direct"]] == [sum(row) for row in ic["direct_temporal_vectors"]]
        assert pc["tail_scores"] == ic["tail_scores"]
        assert pc["tail_entry_age"] == ic["entry_age"]
        assert pc["tail_cycle_length"] == ic["cycle_length"]
        assert pc["n"] + pc["tail_transitions"] == ic["closure_age"]
        assert pc["closed_vector"] == list(reversed(ic["repeated_vector"]))
        closed = pc["closed_vector"]
        assert [a_iter(v, ic["cycle_length"]) for v in closed] == closed
        initial = list(reversed(ic["initial_vector"]))
        assert [a_iter(v, ic["entry_age"] - n) for v in initial] == closed
        vector, replay_scores = initial, []
        for _ in pc["tail_scores"]:
            replay_scores.append(sum(v % 2 for v in vector))
            vector = [a_cells_integer(v) for v in vector]
        assert replay_scores == pc["tail_scores"]
        assert vector == closed
        all_scores = [row["V"] for row in pc["direct"][:n]] + replay_scores
        assert max(all_scores) == pc["R"] == ic["R"]
        assert all_scores.index(max(all_scores)) == pc["maximizer_age"] == ic["first_maximizing_age"]
        direct_count += len(pc["direct"])
        tail_count += len(replay_scores)
        rows.append({"time": r, "x_hex": ic["x_hex"], "n": n, "entry_age": ic["entry_age"],
                     "period": ic["cycle_length"], "R": pc["R"], "first_maximizing_age": pc["maximizer_age"]})
    assert [row["R"] for row in rows] == [13, 16]
    assert p["runtime_seconds"] < 120 and independent["runtime_seconds"] < 120
    source = Path(__file__).read_bytes()
    summary = {"rows": rows, "direct_full_vectors_compared": direct_count,
               "tail_scores_compared_and_replayed": tail_count, "orbit_states_compared": 11,
               "exact_closures_checked": 2, "all_checks_passed": True}
    result = {
        "experiment_id": "20260906-activity-return-nonincrease-verification",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1", "hypothesis": "The two named complete finite recurrence certificates agree",
        "backend": "archive-comparison-and-independent-local-cell-closure-replay",
        "parameters": {"input_records": [str(PRIMARY.relative_to(ROOT)), str(INDEPENDENT.relative_to(ROOT))],
                       "new_scientific_inputs": 0, "target_times": [4, 10]},
        "hardware": {"machine": platform.machine(), "logical_cpus": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": time.monotonic() - start,
        "result_hashes": {"primary_sha256": sha(pb), "independent_sha256": sha(ib),
                          "summary_sha256": canonical(summary), "source_sha256": sha(source)},
        "result_summary": summary, "executed_source": source.decode(), "reference_sha256": reference,
        "status": "finite-exhaustive",
        "proof_scope": "Exactly the two admitted named endpoints and their complete closed recurrences.",
        "interpretation": "Named R nonincrease fails by three; all-age scope uses the proved recurrence and exact closure.",
        "limitations": ["Fresh adversarial scope review is recorded separately.", "No survivor-only claim is refuted.",
                        "No census, expanded orbit or numerical cap change was performed."]}
    with tempfile.NamedTemporaryFile("w", dir=OUT.parent, delete=False) as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
        temp = f.name
    os.replace(temp, OUT)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
