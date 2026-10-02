#!/usr/bin/env python3
"""Bounded exhaustive check of the odd-word portal-layer monodromy claim.

The raw child recurrence and the GF(2) affine composition below are separate
implementations.  This is finite computational evidence, not an infinite
proof.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import platform
import resource
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20261002_portal_layer_monodromy.json"
REFERENCE = ROOT / "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
WALL_CAP = 30.0
MEMORY_CAP = 256 * 1024 * 1024
OUTPUT_CAP = 256 * 1024
START = time.monotonic()
TICKS = 0
RAW_LAYER_UPDATES = 0


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def check_caps(force: bool = False) -> None:
    global TICKS
    TICKS += 1
    if force or TICKS % 4096 == 0:
        if time.monotonic() - START > WALL_CAP:
            raise TimeoutError("30-second overall wall-time cap reached")
        status = Path("/proc/self/status").read_text()
        rss = int(next(x.split()[1] for x in status.splitlines() if x.startswith("VmRSS:"))) * 1024
        if rss > MEMORY_CAP:
            raise MemoryError("256-MiB resident-memory cap reached")


def peak_rss() -> int:
    status = Path("/proc/self/status").read_text()
    return int(next(x.split()[1] for x in status.splitlines() if x.startswith("VmHWM:"))) * 1024


def atomic_json(path: Path, obj: dict) -> None:
    raw = (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode()
    if len(raw) > OUTPUT_CAP:
        raise ValueError(f"result exceeds 256-KiB output cap: {len(raw)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def parity(x: int) -> int:
    return x.bit_count() & 1


def odd_words(p: int):
    return (w for w in range(1 << p) if parity(w))


def pair_array(p: int):
    return itertools.product(range(4), repeat=p)


def bits(pair: int) -> tuple[int, int]:
    return pair & 1, (pair >> 1) & 1


def raw_step(v: tuple[int, int], q: int, w: int,
             high: tuple[int, int], parent: tuple[int, int]) -> tuple[int, int]:
    """Literal two-child recurrence, using scalar Boolean operations only."""
    x, y = v
    h, k = high
    ell, m = parent
    u = ell ^ (q & m)
    vv = u ^ m
    hraw, hraw_next = h ^ (q & k), h ^ k ^ (q & k)
    z, zprime = x ^ (q & y), x ^ y ^ (q & y)
    d = k ^ m ^ (m & x) ^ ((1 ^ ell ^ m) & y)
    # D = K+M+MX+(1+L+M)Y. The preceding line includes K and M.
    f = h ^ ell ^ ((1 ^ ell) & x)
    xn = f ^ (w & d)
    yn = d
    # Check the raw-parent/raw-child realization against the affine scalar
    # formula at each phase; this catches a shared algebra/indexing mistake.
    expect_z = hraw ^ (u | z)
    expect_zn = hraw_next ^ (vv | zprime)
    # The added coordinate is precisely raw-child normalized at q_next=q+w.
    qn = q ^ w
    raw_y_next = expect_z ^ expect_zn
    raw_x_next = expect_z ^ (qn & raw_y_next)
    if (xn, yn) != (raw_x_next, raw_y_next):
        raise AssertionError(("raw-vs-polynomial one-step discrepancy", q, w,
                              high, parent, v, (xn, yn),
                              (raw_x_next, raw_y_next)))
    return xn, yn


def raw_step_direct(v: tuple[int, int], q: int, w: int,
                    high: tuple[int, int], parent: tuple[int, int]) -> tuple[int, int]:
    """Independent implementation from raw z,z' bits, then renormalization."""
    x, y = v
    h, k = high
    ell, m = parent
    u = ell ^ (q & m)
    vv = u ^ m
    z, zprime = x ^ (q & y), x ^ y ^ (q & y)
    h0, h1 = h ^ (q & k), h ^ k ^ (q & k)
    zn = h0 ^ (u | z)
    zpn = h1 ^ (vv | zprime)
    qn = q ^ w
    yn = zn ^ zpn
    return zn ^ (qn & yn), yn


def compose_affine(highs: tuple[int, ...], parents: tuple[int, ...], w: int):
    """Compose per-layer GF(2) matrices; entries are individual bits."""
    a = (1, 0, 0, 1)  # row-major identity
    b = (0, 0)
    q = 0
    for s, (hp, pp) in enumerate(zip(highs, parents)):
        h, k = bits(hp)
        ell, m = bits(pp)
        ws = (w >> s) & 1
        c = (1 ^ ell ^ (ws & m), ws & (1 ^ ell ^ m), m, 1 ^ ell ^ m)
        # From F=H+L+(1+L)X and D=K+M+MX+(1+L+M)Y.
        f0 = h ^ ell
        d0 = k ^ m
        e = (f0 ^ (ws & d0), d0)
        aa, ab, ac, ad = a
        ca, cb, cc, cd = c
        a = (ca * aa ^ cb * ac, ca * ab ^ cb * ad,
             cc * aa ^ cd * ac, cc * ab ^ cd * ad)
        eb, ed = b
        b = (ca * eb ^ cb * ed ^ e[0], cc * eb ^ cd * ed ^ e[1])
        q ^= ws  # q is deliberately tracked as an independent schedule audit.
    return a, b, q


def matrix_apply(a: tuple[int, ...], v: tuple[int, int]) -> tuple[int, int]:
    aa, ab, ac, ad = a
    x, y = v
    return (aa * x ^ ab * y, ac * x ^ ad * y)


def case_record(p: int, w: int, highs: tuple[int, ...], parents: tuple[int, ...],
                seed: tuple[int, int], blocks: int = 1):
    global RAW_LAYER_UPDATES
    v = seed
    q = 0
    for _ in range(blocks):
        for s in range(p):
            v = raw_step_direct(v, q, (w >> s) & 1, bits(highs[s]), bits(parents[s]))
            RAW_LAYER_UPDATES += 1
            q ^= (w >> s) & 1
    return v, q


def evaluate():
    counts = {"p1_to_p3_cases": 0, "p4_cases": 0,
              "matrix_compositions": 0, "raw_parent_any_one_cases": 0,
              "all_zero_parent_cases": 0, "seed_return_comparisons": 0,
              "odd_driver_words": 0,
              "matrix_kind_counts_d0d1": {"00": 0, "01": 0, "10": 0, "11": 0},
              "zero_parent_fixed_point_counts": {"no_solutions": 0, "two_solutions": 0}}
    exceptional = {"no_solution": None, "solution_family": None}
    examples = {"matrix_kinds": {}}
    failure = None
    for p in range(1, 5):
        high_arrays = list(pair_array(p)) if p <= 3 else None
        parent_arrays = list(pair_array(p))
        for w in odd_words(p):
            counts["odd_driver_words"] += 1
            if p <= 3:
                # All cyclic arrays of higher pairs and parent pairs.
                for highs in itertools.product(range(4), repeat=p):
                    for parents in parent_arrays:
                        check_caps()
                        A, b, qend = compose_affine(highs, parents, w)
                        counts["p1_to_p3_cases"] += 1
                        counts["matrix_compositions"] += 1
                        if qend != 1:
                            failure = {"type": "odd_driver_failed_to_toggle", "p": p, "w": w}
                            break
                        # q follows the driver bits, independent of pair codes.
                        q = 0
                        ds0 = ds1 = 1
                        for s, pp in enumerate(parents):
                            ell, m = bits(pp)
                            u = ell ^ (q & m)
                            vparent = u ^ m
                            ds0 &= 1 ^ u
                            ds1 &= 1 ^ vparent
                            q ^= (w >> s) & 1
                        expected = (ds1, ds1, ds0 ^ ds1, ds1)
                        kind = f"{ds0}{ds1}"
                        counts["matrix_kind_counts_d0d1"][kind] += 1
                        examples["matrix_kinds"].setdefault(kind, {
                            "p": p, "w_lsb": w, "high_pairs": list(highs),
                            "parent_pairs": list(parents), "A": list(A)})
                        if A != expected:
                            failure = {"type": "candidate_matrix_mismatch", "p": p,
                                       "w_lsb": w, "high_pairs": list(highs),
                                       "parent_pairs": list(parents), "actual_A": list(A),
                                       "claimed_A": list(expected)}
                            break
                        q = 0
                        parent_nonzero = False
                        for s, pp in enumerate(parents):
                            ell, m = bits(pp)
                            u = ell ^ (q & m)
                            parent_nonzero |= bool(u or (u ^ m))
                            q ^= (w >> s) & 1
                        counts["raw_parent_any_one_cases"] += int(parent_nonzero)
                        counts["all_zero_parent_cases"] += int(not parent_nonzero)
                        if parent_nonzero:
                            if any(matrix_apply(A, matrix_apply(A, col)) != (0, 0)
                                   for col in ((1, 0), (0, 1))):
                                failure = {"type": "nilpotence_mismatch", "p": p,
                                           "w_lsb": w, "parent_pairs": list(parents),
                                           "A": list(A)}
                                break
                            for seed in itertools.product((0, 1), repeat=2):
                                ret, _ = case_record(p, w, highs, parents, seed)
                                one_step = tuple(x ^ y for x, y in zip(matrix_apply(A, seed), b))
                                if ret != one_step:
                                    failure = {"type": "one_period_affine_return_mismatch",
                                               "p": p, "w_lsb": w, "high_pairs": list(highs),
                                               "parent_pairs": list(parents), "seed": list(seed),
                                               "raw_return": list(ret), "affine_return": list(one_step)}
                                    break
                                counts["seed_return_comparisons"] += 1
                                twice, _ = case_record(p, w, highs, parents, seed, blocks=2)
                                fixed = tuple(x ^ y for x, y in zip(b, matrix_apply(A, b)))
                                if twice != fixed:
                                    failure = {"type": "two_period_coalescence_mismatch",
                                               "p": p, "w_lsb": w, "high_pairs": list(highs),
                                               "parent_pairs": list(parents), "seed": list(seed),
                                               "raw_two_period_return": list(twice),
                                               "claimed_fixed_value": list(fixed)}
                                    break
                            if p == 1 and w == 1 and highs == (0,) and parents == (1,):
                                examples["any_raw_parent_one"] = {"w_lsb": w, "high_pairs": list(highs),
                                    "parent_pairs": list(parents), "A": list(A), "b": list(b)}
                        else:
                            # A=G; enumerate all four seeds and verify exactly
                            # the stated affine fixed-point condition and family.
                            if A != (1, 1, 0, 1):
                                failure = {"type": "all_zero_parent_not_unipotent", "p": p,
                                           "w_lsb": w, "A": list(A)}
                            solutions = [seed for seed in itertools.product((0, 1), repeat=2)
                                         if tuple(seed[i] ^ z for i, z in enumerate(matrix_apply(A, seed))) == b]
                            claimed = ([(x, b[0]) for x in (0, 1)] if b[1] == 0 else [])
                            counts["zero_parent_fixed_point_counts"][
                                "two_solutions" if b[1] == 0 else "no_solutions"] += 1
                            # All-zero raw parents force L=M=0. Check the direct
                            # offset identities in addition to the affine solver.
                            q_formula = 0
                            bx_formula = by_formula = 0
                            for s, hp in enumerate(highs):
                                h, k = bits(hp)
                                bx_formula ^= h ^ ((q_formula ^ 1) & k)
                                by_formula ^= k
                                q_formula ^= (w >> s) & 1
                            if b != (bx_formula, by_formula):
                                failure = {"type": "zero_parent_offset_formula_mismatch", "p": p,
                                           "w_lsb": w, "high_pairs": list(highs),
                                           "parent_pairs": list(parents), "b": list(b),
                                           "formula_b": [bx_formula, by_formula]}
                            if set(solutions) != set(claimed):
                                failure = {"type": "exceptional_fixed_family_mismatch", "p": p,
                                           "w_lsb": w, "high_pairs": list(highs),
                                           "parent_pairs": list(parents), "b": list(b),
                                           "solutions": [list(x) for x in solutions],
                                           "claimed": [list(x) for x in claimed]}
                            for seed in itertools.product((0, 1), repeat=2):
                                ret, _ = case_record(p, w, highs, parents, seed)
                                affine = tuple(x ^ y for x, y in zip(matrix_apply(A, seed), b))
                                if ret != affine:
                                    failure = {"type": "one_period_affine_return_mismatch",
                                               "p": p, "w_lsb": w, "high_pairs": list(highs),
                                               "parent_pairs": list(parents), "seed": list(seed),
                                               "raw_return": list(ret), "affine_return": list(affine)}
                                    break
                                counts["seed_return_comparisons"] += 1
                            if b[1] and exceptional["no_solution"] is None:
                                exceptional["no_solution"] = {"p": p, "w_lsb": w,
                                    "high_pairs": list(highs), "parent_pairs": list(parents), "b": list(b)}
                            if not b[1] and exceptional["solution_family"] is None:
                                exceptional["solution_family"] = {"p": p, "w_lsb": w,
                                    "high_pairs": list(highs), "parent_pairs": list(parents), "b": list(b),
                                    "solutions": [list(x) for x in solutions]}
                        if failure:
                            break
                    if failure:
                        break
                if failure:
                    break
            else:
                for highs in ((0,) * p, (1,) * p, (2,) * p, (3,) * p):
                    for parents in parent_arrays:
                        check_caps()
                        A, b, qend = compose_affine(highs, parents, w)
                        counts["p4_cases"] += 1
                        counts["matrix_compositions"] += 1
                        ds0 = ds1 = 1
                        q = 0
                        parent_nonzero = False
                        for s, pp in enumerate(parents):
                            ell, m = bits(pp)
                            u = ell ^ (q & m)
                            vparent = u ^ m
                            ds0 &= 1 ^ u
                            ds1 &= 1 ^ vparent
                            parent_nonzero |= bool(u or vparent)
                            q ^= (w >> s) & 1
                        expected = (ds1, ds1, ds0 ^ ds1, ds1)
                        kind = f"{ds0}{ds1}"
                        counts["matrix_kind_counts_d0d1"][kind] += 1
                        examples["matrix_kinds"].setdefault(kind, {
                            "p": p, "w_lsb": w, "high_pairs": list(highs),
                            "parent_pairs": list(parents), "A": list(A)})
                        if qend != 1 or A != expected:
                            failure = {"type": "candidate_matrix_mismatch", "p": p,
                                       "w_lsb": w, "high_pairs": list(highs),
                                       "parent_pairs": list(parents), "actual_A": list(A),
                                       "claimed_A": list(expected), "q_end": qend}
                            break
                        counts["raw_parent_any_one_cases"] += int(parent_nonzero)
                        counts["all_zero_parent_cases"] += int(not parent_nonzero)
                        if parent_nonzero and any(matrix_apply(A, matrix_apply(A, col)) != (0, 0)
                                                  for col in ((1, 0), (0, 1))):
                            failure = {"type": "nilpotence_mismatch", "p": p,
                                       "w_lsb": w, "parent_pairs": list(parents),
                                       "A": list(A)}
                            break
                        if not parent_nonzero:
                            if A != (1, 1, 0, 1):
                                failure = {"type": "all_zero_parent_not_unipotent", "p": p,
                                           "w_lsb": w, "parent_pairs": list(parents),
                                           "A": list(A)}
                            sols = [seed for seed in itertools.product((0, 1), repeat=2)
                                    if tuple(seed[i] ^ z for i, z in enumerate(matrix_apply(A, seed))) == b]
                            claim = ([(x, b[0]) for x in (0, 1)] if b[1] == 0 else [])
                            counts["zero_parent_fixed_point_counts"][
                                "two_solutions" if b[1] == 0 else "no_solutions"] += 1
                            q_formula = 0
                            bx_formula = by_formula = 0
                            for s, hp in enumerate(highs):
                                h, k = bits(hp)
                                bx_formula ^= h ^ ((q_formula ^ 1) & k)
                                by_formula ^= k
                                q_formula ^= (w >> s) & 1
                            if b != (bx_formula, by_formula):
                                failure = {"type": "zero_parent_offset_formula_mismatch", "p": p,
                                           "w_lsb": w, "high_pairs": list(highs),
                                           "parent_pairs": list(parents), "b": list(b),
                                           "formula_b": [bx_formula, by_formula]}
                            if set(sols) != set(claim):
                                failure = {"type": "exceptional_fixed_family_mismatch", "p": p,
                                           "w_lsb": w, "high_pairs": list(highs),
                                           "parent_pairs": list(parents), "b": list(b),
                                           "solutions": [list(x) for x in sols],
                                           "claimed": [list(x) for x in claim]}
                        for seed in itertools.product((0, 1), repeat=2):
                            ret, _ = case_record(p, w, highs, parents, seed)
                            if parent_nonzero:
                                fixed = tuple(x ^ y for x, y in zip(b, matrix_apply(A, b)))
                                affine = tuple(x ^ y for x, y in zip(matrix_apply(A, seed), b))
                                okay = ret == affine
                            else:
                                fixed = None
                                affine = tuple(x ^ y for x, y in zip(matrix_apply(A, seed), b))
                                okay = ret == affine
                            if not okay:
                                failure = {"type": "raw_return_mismatch", "p": p,
                                           "w_lsb": w, "high_pairs": list(highs),
                                           "parent_pairs": list(parents), "seed": list(seed),
                                           "return": list(ret), "affine_return": list(affine)}
                                break
                            counts["seed_return_comparisons"] += 1
                            if parent_nonzero:
                                twice, _ = case_record(p, w, highs, parents, seed, blocks=2)
                                if twice != fixed:
                                    failure = {"type": "two_period_coalescence_mismatch",
                                               "p": p, "w_lsb": w, "high_pairs": list(highs),
                                               "parent_pairs": list(parents), "seed": list(seed),
                                               "raw_two_period_return": list(twice),
                                               "claimed_fixed_value": list(fixed)}
                                    break
                        if failure:
                            break
                    if failure:
                        break
                if failure:
                    break
        if failure:
            break
    if failure is None:
        # Independent one-step expression audit.
        for q, wbit, hp, pp, seed in itertools.product(range(2), range(2), range(4), range(4), itertools.product(range(2), repeat=2)):
            raw_step(seed, q, wbit, bits(hp), bits(pp))
        # One explicitly named even-driver boundary control, outside the
        # theorem's odd-driver domain.
        evens = {"p": 1, "w_lsb": 0, "q_start": 0, "high_pair": 1,
                 "parent_pair": 2, "seed_domain": [[0, 0], [0, 1], [1, 0], [1, 1]]}
        evA, evb, evq = compose_affine((1,), (2,), 0)
        ev_fixed = [seed for seed in itertools.product((0, 1), repeat=2)
                    if tuple(seed[i] ^ z for i, z in enumerate(matrix_apply(evA, seed))) == evb]
        ea, eb, ec, ed = evA
        ev_square = (ea * ea ^ eb * ec, ea * eb ^ eb * ed,
                     ec * ea ^ ed * ec, ec * eb ^ ed * ed)
        if (evA, evq, ev_fixed) != ((1, 0, 1, 0), 0, []):
            failure = {"type": "named_even_driver_control_mismatch", "A": list(evA),
                       "b": list(evb), "q_end": evq,
                       "fixed_points": [list(x) for x in ev_fixed]}
        evens.update({"A": list(evA), "b": list(evb), "q_end": evq,
                      "A_squared": list(ev_square), "A_squared_equals_A": ev_square == evA,
                      "fixed_points": [list(x) for x in ev_fixed]})
        examples["even_driver_scope_control"] = evens
        counts["raw_layer_updates"] = RAW_LAYER_UPDATES
    return counts, exceptional, examples, failure


def main() -> int:
    check_caps(force=True)
    ref_bytes = REFERENCE.read_bytes()
    if sha(ref_bytes) != REFERENCE_SHA:
        raise RuntimeError("immutable reference hash differs from supplied provenance")
    counts, exceptional, examples, failure = evaluate()
    elapsed = time.monotonic() - START
    source = Path(__file__).read_bytes()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    cpu = ""
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.lower().startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
    except OSError:
        pass
    summary = {"counts": counts, "exceptional_all_zero_parent_examples": exceptional,
               "named_cases": examples, "discrepancy": failure}
    record = {
        "experiment_id": "20261002_portal_layer_monodromy",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "question": "problem1",
        "hypothesis": "For every odd p-bit driver and arbitrary cyclic higher/parent pair arrays, the p-step added-state affine return matrix is [[d1,d1],[d0+d1,d1]], with the stated nilpotent/coalescence or all-zero-parent fixed-family behavior.",
        "backend": "independent scalar raw-bit recurrence plus GF(2) 2x2 affine matrix composition",
        "parameters": {
            "periods": [1, 2, 3, 4], "odd_driver_domain": "all p-bit words of odd Hamming parity",
            "p1_to_p3_arrays": "every ordered p-array of higher pairs and every ordered p-array of parent pairs, each pair in {00,01,10,11}",
            "p4_higher_control_arrays": [[0, 0], [1, 0], [0, 1], [1, 1]],
            "p4_parent_arrays": "every ordered p-array of parent pairs in {00,01,10,11}",
            "child_seeds": [[0, 0], [0, 1], [1, 0], [1, 1]],
            "caps": {"wall_seconds": WALL_CAP, "resident_memory_bytes": MEMORY_CAP,
                     "output_bytes": OUTPUT_CAP}
        },
        "hardware": {"platform": platform.platform(), "machine": platform.machine(),
                     "processor": platform.processor(), "cpu_model": cpu,
                     "cpu_count": os.cpu_count(), "peak_rss_bytes": peak_rss()},
        "software": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                      "system": platform.system(), "release": platform.release()},
        "runtime_seconds": elapsed,
        "result_summary": summary,
        "result_hashes": {"script_sha256": sha(source), "immutable_reference_sha256": REFERENCE_SHA,
                          "canonical_summary_sha256": sha(canonical(summary)),
                          "payload_sha256_excluding_this_field": "pending"},
        "source_and_input_hashes": {
            "experiments/problem1_nonperiodicity/check_portal_layer_monodromy.py": sha(source),
            "src/python/rule30_research_reference.py": REFERENCE_SHA
        },
        "proof_dependency_policy": "The concurrently authored proof note is outside this run's inputs and hash dependencies.",
        "implementation_diagnostics": [
            {"classification": "superseded checker bug, not theorem evidence",
             "bug": "Raw children (z_n,z'_n) were returned as normalized (X_n,Y_n); the required inversion is Y_n=z_n XOR z'_n and X_n=z_n XOR(q_n AND Y_n).",
             "smallest_observed_case": {"p": 1, "w_lsb": 1, "high_pairs": [0],
                 "parent_pairs": [1], "seed": [0, 0], "incorrect_return": [0, 1],
                 "correct_affine_return": [1, 0]}},
            {"classification": "superseded checker bug, not theorem evidence",
             "bug": "A one-period return was compared directly to the claimed two-period fixed value.",
             "smallest_observed_case": {"p": 1, "w_lsb": 1, "high_pairs": [0],
                 "parent_pairs": [2], "seed": [0, 0], "one_period_return": [1, 1],
                 "affine_one_period_return": [1, 1], "two_period_fixed_value": [1, 0]}}
        ],
        "status": "inconclusive" if failure or elapsed > WALL_CAP else "finite-exhaustive",
        "interpretation": "A finite exhaustive check over exactly the declared domains; it does not establish an all-period theorem." if failure is None else "The proposed candidate has a mechanical discrepancy; see the smallest reported case.",
        "proof_scope": "Exhaustive for p=1,2,3 over all odd drivers, all upper-pair arrays, all parent-pair arrays and four seeds; for p=4 exhaustive over all odd drivers, all parent arrays, four constant higher-pair controls and four seeds. Matrix/fixed-point checks are finite computational evidence only.",
        "limitations": ["No claim is made for even drivers; even words serve only as a parity-schedule control.",
                        "The p=4 higher-pair arrays are restricted to the four listed constants.",
                        "Finite enumeration is not a proof for arbitrary p.",
                        "Hard caps are 30 seconds, 256 MiB resident memory, and 256 KiB JSON output."],
    }
    record["result_hashes"]["payload_sha256_excluding_this_field"] = sha(canonical({k: v for k, v in record.items() if k != "result_hashes"}))
    atomic_json(OUT, record)
    print(json.dumps({"output": str(OUT), "status": record["status"], "runtime_seconds": elapsed,
                      "counts": counts, "discrepancy": failure,
                      "payload_sha256": record["result_hashes"]["payload_sha256_excluding_this_field"]}, sort_keys=True))
    return 1 if failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
