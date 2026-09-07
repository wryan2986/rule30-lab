"""Fixed full-driver phase-summary counterexample; not a source search.

Admission and hand derivation:
proofs/informal/problem1_full_driver_phase_memory_obstruction.md.
Caps: 16 A steps per certificate, 10 seconds, 128 MiB, one local worker.
"""

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

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260907_round305_phase_transport.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
HAND_EDGES = ((110, 100), (112, 100), (100, 111), (111, 100),
              (220, 201), (201, 223), (223, 200), (224, 200),
              (200, 222), (222, 200), (400, 444), (444, 401),
              (401, 445), (445, 400))
SOURCES = (110, 112)
CHILDREN = (220, 221, 224, 225)
GRANDCHILDREN = (440, 441, 448, 449)
CORES = (111, 222, 444, 445)
EXPECTED_MAPS = {110: (0, 0), 112: (0, 0),
                 220: (0, 0), 224: (1, 0)}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def packed(y):
    return (y >> 2) ^ ((y >> 1) | y)


def cells(y):
    word = [bool((y >> j) & 1) for j in range(max(1, y.bit_length()))]
    padded = word + [False, False]
    return sum((1 << j) for j in range(len(word))
               if padded[j + 2] != (padded[j + 1] or padded[j]))


def certificate(y):
    rows, seen, current = [], {}, y
    for _ in range(16):
        if current in seen:
            delay = seen[current]
            period = len(rows) - delay
            core = rows[delay + ((-delay) % period)]
            return {"seed": y, "rows": rows, "tau": delay,
                    "period": period, "cyc": core}
        seen[current] = len(rows)
        rows.append(current)
        following = packed(current)
        assert following == cells(current), (y, current)
        current = following
    raise AssertionError("fixed certificate exceeded its 16-step cap")


def product_phase(y, z, horizon):
    low, high, cyclic_high = [], [], []
    for _ in range(horizon):
        assert z % 2 == 0
        low.append(y & 1)
        high.append((y >> 1) & 1)
        cyclic_high.append((z >> 1) & 1)
        y, z = packed(y), packed(z)
    eta, theta = 1, 0
    for bit in low:
        eta *= 1 ^ bit
    for s in range(horizon):
        summand = high[s] ^ low[s]
        for k in range(s + 1, horizon):
            summand *= 1 ^ low[k]
        theta ^= summand ^ cyclic_high[s]
    return eta, theta


def scalar_phase(y, z, a, horizon):
    response, inverse_flip = a, 0
    for _ in range(horizon):
        response = ((y // 2) % 2) ^ int(bool(y % 2) or bool(response))
        inverse_flip ^= (z // 2) % 2
        y, z = cells(y), cells(z)
    return response ^ inverse_flip


def deadline(_signal, _frame):
    raise TimeoutError("10-second cap exceeded")


def main():
    started = time.perf_counter()
    cap = 128 * 1024 * 1024
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(10)
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    for before, after in HAND_EDGES:
        assert packed(before) == cells(before) == after
    certs = {y: certificate(y) for y in SOURCES + CHILDREN + GRANDCHILDREN + CORES}
    actual_maps = {}
    for y, expected in EXPECTED_MAPS.items():
        actual = tuple(certs[2 * y + a]["cyc"] % 2 for a in (0, 1))
        assert actual == expected
        assert all(certs[2 * y + a]["cyc"] // 2 == certs[y]["cyc"]
                   for a in (0, 1))
        actual_maps[y] = actual
    summaries = {y: (certs[y]["cyc"], certs[y]["tau"], *actual_maps[y])
                 for y in SOURCES}
    assert summaries[110] == summaries[112] == (111, 1, 0, 0)
    assert certs[110]["period"] == certs[112]["period"] == 2
    assert certs[220]["cyc"] == certs[224]["cyc"] == 222
    assert (certs[220]["tau"], certs[224]["tau"]) == (3, 1)
    assert (certs[440]["cyc"], certs[448]["cyc"]) == (444, 445)
    checks = []
    for y, expected in ((220, (0, 0)), (224, (1, 1))):
        for extra in (0, 2):
            horizon = certs[y]["tau"] + extra
            eta, theta = product_phase(y, 222, horizon)
            assert (eta, theta) == expected
            for a in (0, 1):
                response = (eta * a) ^ theta
                assert response == scalar_phase(y, 222, a, horizon)
                assert response == actual_maps[y][a]
                checks.append({"source": y, "horizon": horizon, "bit": a,
                               "eta": eta, "theta": theta, "phase": response})
    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < 10 and peak < cap
    payload = {"hand_edges": HAND_EDGES, "certificates": list(certs.values()),
               "summaries": summaries, "phase_maps": actual_maps, "checks": checks}
    source_paths = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
                    "proofs/informal/problem1_full_driver_phase_memory_obstruction.md",
                    "proofs/informal/problem1_global_cycle_shadow.md",
                    "proofs/informal/problem1_physical_time_cycle_defects.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round305-fixed-full-driver-phase-summary-obstruction",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "Rows110 and112 have identical complete cores, exact least delays and full one-bit phase maps, but zero extension exposes distinct child phase maps.",
        "backend": "Python-packed-A/independent-Boolean-cells/product-formula/scalar-OR",
        "parameters": {"sources": SOURCES, "children": CHILDREN,
                       "grandchildren": GRANDCHILDREN, "cores": CORES,
                       "formula_sources": [220, 224], "horizon_extras": [0, 2],
                       "bits": [0, 1], "cycle_step_cap": 16, "cpu_workers": 1,
                       "wall_cap_seconds": 10, "memory_cap_bytes": cap},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "Main entry through fixed mathematical checks; excludes final provenance and serialization.",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in source_paths},
        "result_summary": {"all_checks_passed": True, "hand_edges": len(HAND_EDGES),
                           "closed_certificates": len(certs), "phase_checks": len(checks),
                           "same_source_summary": [111, 1, 0, 0],
                           "child_zero_phases": [0, 1], "caps_passed": True},
        "interpretation": "The named general summary update is refuted, including on two successive zero extensions. This is not a FULL-conditioned counterexample.",
        "status": "finite-exhaustive",
        "proof_scope": "Exactly the fixed hand edges, fourteen closed cycle certificates, four full Boolean phase maps, and eight product/scalar phase comparisons.",
        "limitations": ["No source or prefix search.", "No FULL survivor or all-depth exclusion.",
                        "No refutation of every augmented or FULL-conditioned summary.",
                        "Fresh external review is missing."],
        "payload": payload,
    }
    encoded = (json.dumps(record, indent=2) + "\n").encode()
    assert len(encoded) < 128 * 1024
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=OUT.parent, prefix=OUT.name + ".",
                                         suffix=".tmp", delete=False) as handle:
            temporary = handle.name
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUT)
        fd = os.open(OUT.parent, os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    signal.alarm(0)
    print(json.dumps({"result": str(OUT.relative_to(ROOT)),
                      "closed_certificates": len(certs), "phase_checks": len(checks),
                      "runtime_seconds": elapsed, "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
