"""One fixed Phi-nilpotence certificate; not a word or seed search.

Admission: proofs/informal/problem1_finite_cycle_phase_fork.md, Section 0.
Run as a small Python child to avoid inherited launcher RSS accounting.
"""

import hashlib
import json
import os
import platform
from pathlib import Path
import resource
import signal
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260907_round304_phase_fork.json"
WORD = "0000220002020022"
HAND = (
    WORD, "0002130023230213", "0022230201032223", "0211032333111103",
)
TABLE = ("0321", "3012", "3210", "3210")
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
CAP_STEPS = 100000
WALL_SECONDS = 60
MEMORY_BYTES = 128 * 1024 * 1024
SOURCE_URL = "https://ericrowland.github.io/papers/Local_nested_structure_in_rule_30.pdf"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def g_bits(a, b):
    al, ah, bl, bh = a & 1, a >> 1, b & 1, b >> 1
    lo = bl ^ (al | ah)
    hi = bh ^ (ah | lo)
    return lo | (hi << 1)


def phi_tuple(row):
    return tuple(g_bits(row[i], row[(i + 1) % len(row)])
                 for i in range(len(row)))


def phi_string(row):
    return "".join(TABLE[int(a)][int(b)] for a, b in zip(row, row[1:] + row[:1]))


def packed_a(row):
    return (row >> 2) ^ ((row >> 1) | row)


def cell_a(cells):
    extended = cells + [0, 0]
    return [int(extended[i + 2] != (extended[i + 1] or extended[i]))
            for i in range(len(cells))]


def deadline(_sig, _frame):
    raise TimeoutError("round304 fixed certificate exceeded 60 seconds")


def check_vector(seed, expected):
    assert packed_a(seed) == expected
    width = max(1, seed.bit_length())
    cells = [bool((seed >> i) & 1) for i in range(width)]
    assert cell_a(cells) == [(expected >> i) & 1 for i in range(width)]


def main():
    started = time.perf_counter()
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(WALL_SECONDS)
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))
    assert digest((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    for a in range(4):
        for b in range(4):
            assert g_bits(a, b) == int(TABLE[a][b])
    for a, b in zip(HAND, HAND[1:]):
        assert phi_string(a) == b
        assert phi_tuple(tuple(map(int, a))) == tuple(map(int, b))
    for seed, expected in ((0, 0), (1, 1), (2, 3), (3, 3), (4, 7),
                           (6, 6), (7, 6), (55, 50), (50, 55)):
        check_vector(seed, expected)

    # Independent representations and independent complete loops. The only
    # admitted scientific input is WORD. No absent-zero conclusion is inferred.
    first = tuple(map(int, WORD))
    hash_tuple, digits_tuple, nonzero_count = hashlib.sha256(), [], 0
    tuple_started = time.perf_counter()
    for depth_tuple in range(CAP_STEPS + 1):
        hash_tuple.update(bytes(first))
        if not any(first) or depth_tuple == CAP_STEPS:
            break
        nonzero_count += 1
        digits_tuple.append(first[0])
        first = phi_tuple(first)
    else:
        raise AssertionError("unreachable loop exhaustion")
    tuple_time = time.perf_counter() - tuple_started
    tuple_zero = not any(first)

    second = WORD
    hash_string, digits_string = hashlib.sha256(), []
    string_started = time.perf_counter()
    depth_string = 0
    while True:
        hash_string.update(bytes(int(c) for c in second))
        if set(second) == {"0"} or depth_string == CAP_STEPS:
            break
        digits_string.append(int(second[0]))
        second = phi_string(second)
        depth_string += 1
    string_time = time.perf_counter() - string_started
    string_zero = set(second) == {"0"}
    assert (tuple_zero, depth_tuple) == (string_zero, depth_string)
    assert hash_tuple.hexdigest() == hash_string.hexdigest()
    assert digits_tuple == digits_string

    payload = {"word": WORD, "hand_transitions": HAND,
               "zero_reached": tuple_zero, "deletion_steps": depth_tuple,
               "trajectory_encoding": "concatenated raw symbol bytes, initial through final row",
               "trajectory_sha256": hash_tuple.hexdigest()}
    cell_time = 0.0
    if tuple_zero:
        assert nonzero_count == depth_tuple
        y = 0
        for digit in reversed(digits_tuple):
            y = 4 * y + digit
        assert y > 0 and (y & 3) == int(WORD[0])
        p = len(WORD)
        u = [int(c) // 2 for c in WORD]
        assert all(int(c) % 2 == 0 for c in WORD)
        assert sum(u) == 6 and u[1] != u[9]

        rows, current = [], y
        for t in range(p):
            rows.append(current)
            assert current % 4 == int(WORD[t])
            current = packed_a(current)
        assert current == y and len(set(rows)) == p

        # Independently evolve a Boolean cell list with a literal local rule.
        # Compare every bit at every time, not just the observed pair.
        cell_started = time.perf_counter()
        width = y.bit_length()
        expected_bits = [[(r >> i) & 1 for i in range(width)] for r in rows]
        cells = [bool(bit) for bit in expected_bits[0]]
        for phase in range(1, p + 1):
            cells = cell_a(cells)
            assert cells == expected_bits[phase % p]
        cell_time = time.perf_counter() - cell_started

        lift_orbits = []
        for e in (0, 1):
            lift, trace, orbit, v = 2 * y + e, [], [], e
            for t in range(p):
                assert (lift >> 1) == rows[t]
                assert (lift & 1) == v
                orbit.append(lift)
                trace.append(v)
                v ^= u[t]
                lift = packed_a(lift)
            assert lift == 2 * y + e and v == e and len(set(orbit)) == p
            lift_orbits.append(orbit)
            assert "".join(map(str, trace)) == (
                "0000010000110001" if e == 0 else "1111101111001110")
        assert set(lift_orbits[0]).isdisjoint(lift_orbits[1])
        payload.update({"nilpotence_index": depth_tuple, "source_width_bits": width,
                        "source_hex": hex(y), "source_little_endian_sha256":
                        digest(y.to_bytes((width + 7) // 8, "little")),
                        "source_least_period": p, "upper_bit_weight": sum(u),
                        "lift_least_periods": [p, p], "lift_low_traces":
                        ["0000010000110001", "1111101111001110"],
                        "lift_cycles_disjoint": True,
                        "cell_bits_compared": p * width})

    elapsed = time.perf_counter() - started
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < WALL_SECONDS and peak_rss <= MEMORY_BYTES
    sources = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
               "proofs/informal/problem1_activity_sparse_temporal_codes.md",
               "proofs/informal/problem1_physical_time_cycle_defects.md"]
    pdf = Path("/tmp/astra-round304/rowland.pdf")
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round304-fixed-even-parity-finite-cycle-fork",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The one fixed even-parity pure word 0000220002020022 is Phi-nilpotent and yields two disjoint finite cyclic one-bit lifts with the same least period.",
        "backend": "python-tuple-bit-formula/string-table/packed-A/Boolean-cell-A",
        "parameters": {"word": WORD, "word_count": 1, "period": 16,
                       "deletion_step_cap": CAP_STEPS, "cpu_workers": 1,
                       "wall_cap_seconds": WALL_SECONDS, "memory_cap_bytes": MEMORY_BYTES},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak_rss},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "main entry through scientific checks; excludes provenance and atomic serialization",
        "component_seconds": {"tuple_deletion": tuple_time, "string_deletion": string_time,
                              "cell_verification": cell_time},
        "result_hashes": {"canonical_payload_sha256": digest(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: digest((ROOT / p).read_bytes()) for p in sources},
        "candidate_provenance": {"url": SOURCE_URL, "printed_page": 17,
                                 "binary_word": "0000110001010011",
                                 "pdf_sha256": digest(pdf.read_bytes()) if pdf.exists() else None,
                                 "scope": "candidate selection only; no imported minimality claim"},
        "result_summary": {"zero_reached": tuple_zero, "implementations_agree": True,
                           "deletion_steps": depth_tuple, "caps_passed": True},
        "status": "finite-exhaustive" if tuple_zero else "inconclusive",
        "interpretation": ("Exact finite-source counterexample to odd-parity rigidity."
                           if tuple_zero else "Fixed cap did not establish nilpotence."),
        "proof_scope": "One fixed cyclic-word trajectory, 16 g entries, three hand transitions, nine small A vectors; on success, every bit of the reconstructed row for its complete 16-step cycle and both lifted cycles.",
        "limitations": ["No source, period or FULL-prefix search.",
                        "No first-occurrence, unbounded-supply or density claim.",
                        "Not an infinite FULL countermodel or external mathematical review."],
        "payload": payload,
    }
    encoded = (json.dumps(record, indent=2) + "\n").encode()
    assert len(encoded) < 1024 * 1024
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=OUT.parent, prefix=OUT.name + ".",
                                         suffix=".tmp", delete=False) as handle:
            temporary = handle.name
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUT)
        directory_fd = os.open(OUT.parent, os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    signal.alarm(0)
    print(json.dumps({"result": str(OUT.relative_to(ROOT)),
                      "zero_reached": tuple_zero, "deletion_steps": depth_tuple,
                      "width": payload.get("source_width_bits"),
                      "runtime_seconds": elapsed}))


if __name__ == "__main__":
    main()
