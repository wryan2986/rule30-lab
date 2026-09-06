#!/usr/bin/env python3
"""Cell/projection certificate for exactly the admitted named return block."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "proofs/informal/problem1_activity_return_nonincrease.md"
OUT = ROOT / "results/problem1/20260906_activity_return_nonincrease_independent.json"
REFERENCE_HASH = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
WORD = "ttttututut"
CAP = 65536


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def bits(value):
    return [int(c) for c in reversed(bin(value)[2:])] if value else []


def integer(row):
    return sum(b * 2 ** i for i, b in enumerate(row))


def trim(row):
    while row and row[-1] == 0:
        row.pop()
    return row


def t_cells(row):
    padded = [0, 0] + list(row) + [0, 0]
    return trim([padded[i + 2] ^ int(padded[i + 1] == 1 or padded[i] == 1)
                 for i in range(len(row) + 2)])


def a_cells(row):
    padded = list(row) + [0, 0]
    return trim([padded[i + 2] ^ int(padded[i + 1] == 1 or padded[i] == 1)
                 for i in range(len(row))])


def lowbit(row):
    return row[0] if row else 0


def gate(row):
    low = integer(row[:4])
    return {7: "u", 11: "t"}.get(low)


def forced(row):
    branch = gate(row)
    assert branch is not None
    out = t_cells(a_cells(row))
    if branch == "u":
        out[0] ^= 1
    return trim(out)


def direct(row, s):
    current = list(row)
    vector = []
    for _ in range(s):
        vector.append(current[2 * s] if len(current) > 2 * s else 0)
        current = t_cells(current)
    return vector


def certificate(row, n, started):
    assert n == (len(row) + 1) // 2 - 1
    direct_vectors = [direct(row, s) for s in range(n + 3)]
    components = []
    for d in range(1, n + 1):
        component = row[2 * d:]
        for _ in range(n - d):
            component = a_cells(component)
        components.append(component)
    initial = [integer(c) for c in components]
    seen, scores = {}, []
    state_hash = hashlib.sha256()
    for step in range(CAP + 1):
        assert time.monotonic() - started < 120
        state = tuple(bytes(c) for c in components)
        age = n + step
        if state in seen:
            entry_age = seen[state]
            cycle_length = age - entry_age
            exact = {
                "closed": True, "tail_start_age": n,
                "entry_age": entry_age, "closure_age": age,
                "cycle_length": cycle_length,
                "initial_vector": initial,
                "repeated_vector": [integer(c) for c in components],
                "tail_scores": scores,
                "distinct_state_stream_sha256": state_hash.hexdigest(),
            }
            all_scores = [sum(v) for v in direct_vectors[:n]] + scores
            exact["R"] = max(all_scores)
            exact["first_maximizing_age"] = all_scores.index(exact["R"])
            for s in range(n, n + 3):
                i = s - n
                if i >= len(scores):
                    i = entry_age - n + (s - entry_age) % cycle_length
                assert sum(direct_vectors[s]) == scores[i]
            return {"x": integer(row), "x_hex": hex(integer(row)), "n": n,
                    "direct_temporal_vectors": direct_vectors, **exact}
        if step == CAP:
            return {"x": integer(row), "n": n, "closed": False,
                    "reason": "declared transition cap reached",
                    "direct_temporal_vectors": direct_vectors,
                    "tail_scores": scores,
                    "distinct_state_stream_sha256": state_hash.hexdigest()}
        seen[state] = age
        state_hash.update(json.dumps([integer(c) for c in components], separators=(",", ":")).encode() + b"\n")
        scores.append(sum(lowbit(c) for c in components))
        components = [a_cells(c) for c in components]
    raise AssertionError("unreachable")


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as f:
        tmp = Path(f.name)
        json.dump(value, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def main():
    started = time.monotonic()
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_AS, (1024 ** 3, 1024 ** 3))
    admission_bytes, source_bytes = NOTE.read_bytes(), Path(__file__).read_bytes()
    reference = ROOT / "src/python/rule30_research_reference.py"
    assert sha(reference.read_bytes()) == REFERENCE_HASH
    row = bits(0x6473d46ab)
    orbit = [{"time": 0, "x": integer(row), "x_hex": hex(integer(row)), "gate": gate(row)}]
    targets = {}
    for r, expected in enumerate(WORD):
        assert gate(row) == expected
        previous_length = len(row)
        row = forced(row)
        assert len(row) == previous_length + 2
        orbit.append({"time": r + 1, "x": integer(row), "x_hex": hex(integer(row)), "gate": gate(row)})
        if r + 1 in (4, 10):
            targets[r + 1] = list(row)
    assert gate(row) == "u"  # observed gate only; its step is not executed
    certificates = {str(r): certificate(targets[r], 17 + r, started) for r in (4, 10)}
    closed = all(c["closed"] for c in certificates.values())
    summary = {"all_closed": closed}
    if closed:
        summary.update({"R_at_4": certificates["4"]["R"], "R_at_10": certificates["10"]["R"],
                        "difference": certificates["10"]["R"] - certificates["4"]["R"],
                        "nonincrease_refuted_on_named_block": certificates["10"]["R"] > certificates["4"]["R"]})
    result = {"orbit": orbit, "certificates": certificates}
    cpu = next((s.split(":", 1)[1].strip() for s in Path("/proc/cpuinfo").read_text().splitlines()
                if s.startswith("model name")), "unknown")
    runtime = time.monotonic() - started
    assert runtime < 120
    record = {
        "experiment_id": "20260906-activity-return-nonincrease-independent",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1", "hypothesis": "R(F^6(x4)) <= R(x4) on the one admitted prescribed gap222 return block",
        "backend": "independent-python-cell-arrays-projected-tail-vector",
        "parameters": {"initial_x": "0x6473d46ab", "observed_branches": WORD,
                       "final_gate_not_executed": "u", "target_times": [4, 10], "gaps": [2, 2, 2],
                       "tail_transition_cap_per_endpoint": CAP, "direct_ages": "0..n+2 inclusive",
                       "cpu_concurrency": 1, "wall_cap_seconds": 120, "memory_cap_bytes": 1024 ** 3},
        "hardware": {"cpu": cpu, "machine": platform.machine(), "logical_cpus": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": runtime, "result_summary": summary,
        "result_hashes": {"results_sha256": digest(result), "summary_sha256": digest(summary)},
        "status": "finite-exhaustive" if closed else "inconclusive",
        "proof_scope": "Two named endpoints; complete closed finite vectors certify all ages only via the stated diagonal recurrence.",
        "interpretation": "No inference from a finite maximum without exact closure; no infinite survivor is exhibited.",
        "limitations": ["No new endpoint search or frontier/return/activity-level census.",
                        "Primary comparison and fresh adversarial proof review remain separately required.",
                        "The final u gate is tested but not executed."],
        "provenance": {"source_path": str(Path(__file__).relative_to(ROOT)), "source_sha256": sha(source_bytes),
                       "source": source_bytes.decode(), "admission_path": str(NOTE.relative_to(ROOT)),
                       "admission_sha256": sha(admission_bytes), "admission": admission_bytes.decode(),
                       "reference_sha256": REFERENCE_HASH},
        "results": result,
    }
    atomic(OUT, record)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
