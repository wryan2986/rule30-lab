"""Verify one hand-derived period-six mortality witness; no search."""
import hashlib
import json
import os
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTE = "proofs/informal/problem1_anchored_activity_vertical_spine_obstruction.md"
OUT = ROOT / "results/problem1/20260906_anchored_spine_primary.json"
REFERENCE = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def snapshot(path):
    raw = (ROOT / path).read_bytes()
    return {"path": path, "sha256": digest(raw), "text": raw.decode()}


def main():
    started = time.perf_counter()
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
    signal.alarm(120)
    assert digest((ROOT / "src/python/rule30_research_reference.py").read_bytes()) == REFERENCE
    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    assert len(git_commit) == 40
    expected = [50, 23, 10, 45, 36, 63, 0]
    words = [50]
    for _ in range(6):
        value = words[-1]
        rotate_one = (value >> 1) | ((value & 1) << 5)
        rotate_two = (value >> 2) | ((value & 3) << 4)
        words.append(rotate_two ^ (rotate_one | value))
    assert words == expected
    rows = [[(word >> i) & 1 for i in range(6)] for word in words]
    pairs = [[(word >> (2*j)) & 3 for word in words] for j in range(3)]
    expected_pairs = [[2, 3, 2, 1, 0, 3, 0], [0, 1, 2, 3, 1, 3, 0],
                      [3, 1, 0, 2, 2, 3, 0]]
    assert pairs == expected_pairs
    # Verify exactly the 18 nontrivial temporal-deletion seams in the note.
    for j in range(3):
        for t in range(6):
            a, b = pairs[j][t:t+2]
            low = (b & 1) ^ ((a & 1) | ((a >> 1) & 1))
            high = ((b >> 1) & 1) ^ (((a >> 1) & 1) | low)
            assert low + 2*high == pairs[(j+1) % 3][t]
    payload = {"period_bits": 6, "initial_word": 50, "a_rows": rows,
               "temporal_pairs": pairs,
               "pair_activity_counts": [sum(v != 0 for v in p) for p in pairs],
               "first_zero_time": words.index(0)}
    assert payload["pair_activity_counts"] == [5, 5, 5]
    source = snapshot(str(Path(__file__).relative_to(ROOT)))
    admission = snapshot(NOTE)
    record = {
        "experiment_id": "20260906_anchored_spine_primary",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit, "question": "problem1",
        "hypothesis": "The single stated period-six row dies first at time six, with exactly five active times at each aligned pair.",
        "backend": "python-packed-cyclic-A-and-local-g",
        "parameters": {"initial_word": 50, "period_bits": 6, "updates": 6,
                       "initial_inputs": 1, "local_g_seams": 18,
                       "cpu_seconds_limit": 120, "wall_seconds_limit": 120,
                       "ram_bytes_limit": 1024**3, "concurrency": 1},
        "hardware": {"uname": list(platform.uname()), "logical_cpus": os.cpu_count()},
        "software": {"python": sys.version, "executable": sys.executable},
        "runtime_seconds": time.perf_counter()-started,
        "result_hashes": {"payload_sha256": digest(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()),
                          "source_sha256": source["sha256"], "admission_sha256": admission["sha256"],
                          "immutable_reference_sha256": REFERENCE},
        "result_summary": {"full_hand_rows_match": True, "local_g_seams_match": 18,
                           "first_zero_time": 6, "pair_activity_counts": [5, 5, 5]},
        "interpretation": "Exact verification of the one hand-derived witness, not a period or mortality search.",
        "status": "finite-exhaustive",
        "proof_scope": "Singleton initial row 50 on a six-cell ring, exactly six updates and 18 declared g seams.",
        "limitations": ["No actual survivor is constructed or excluded.",
                        "Infinite spatial and temporal conclusions require the separate periodicity/zero-row proof.",
                        "Only coefficient-one lifetime bound is refuted; no conclusion about cK for larger c.",
                        "Immutable supplied reference is hashed, not modified or extended to a new backend."],
        "payload": payload, "source_snapshot": source, "admission_snapshot": admission}
    fd, name = tempfile.mkstemp(prefix=OUT.name+".", suffix=".tmp", dir=OUT.parent)
    with os.fdopen(fd, "w") as stream:
        json.dump(record, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(name, OUT)
    signal.alarm(0)
    print(json.dumps({"path": str(OUT.relative_to(ROOT)), **record["result_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
