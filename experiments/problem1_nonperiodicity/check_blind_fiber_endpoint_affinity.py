#!/usr/bin/env python3
"""Finite p=8 endpoint check and p=2..14, r=1..6 blind-cube extension search."""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20261002_blind_fiber_endpoint_affinity.json"
REFERENCE = ROOT / "src/python/rule30_research_reference.py"
ANALYZER = ROOT / "experiments/problem1_nonperiodicity/analyze_blind_visit_rank.py"
CLASSIFIER_NOTE = ROOT / "proofs/informal/problem1_last_reset_child_and_endpoint_parity_complexity.md"
P = 8
R = 1
WALL_CAP = 60.0
LIFT_CAP = 300_000
MEMORY_CAP = 256 * 1024 * 1024
START = time.monotonic()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check_caps() -> None:
    if time.monotonic() - START > WALL_CAP:
        raise TimeoutError("overall wall-time cap reached")
    status = Path("/proc/self/status").read_text()
    rss_kib = int(next(line.split()[1] for line in status.splitlines() if line.startswith("VmRSS:")))
    if rss_kib * 1024 > MEMORY_CAP:
        raise MemoryError("256 MiB resident-memory cap reached")


def peak_rss_bytes() -> int:
    status = Path("/proc/self/status").read_text()
    hwm_kib = int(next(line.split()[1] for line in status.splitlines() if line.startswith("VmHWM:")))
    return hwm_kib * 1024


def cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unavailable"


def atomic_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode()
    if len(data) > 256 * 1024:
        raise ValueError(f"result exceeds 256 KiB output cap: {len(data)} bytes")
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def parity(x: int) -> int:
    return x.bit_count() & 1


def gf2_rank(vectors: list[int]) -> int:
    pivots = {}
    for value in vectors:
        x = value
        while x:
            bit = x.bit_length() - 1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                break
    return len(pivots)


def lsb_bits(w: int, p: int = P) -> list[int]:
    return [(w >> i) & 1 for i in range(p)]


def portal_lift(w: int, p: int = P) -> int:
    cur = x = 0
    for s in range(2 * p):
        x |= cur << s
        cur ^= (w >> (s % p)) & 1
    if cur:
        raise AssertionError("odd driver did not close doubled integration")
    return x


def broad_child(b: int, c: int, n: int) -> int:
    """Fast exact packed realization of the cyclic child recurrence."""
    if b == 0:
        raise ValueError("zero low plane has no unique recurrent child")
    mask = (1 << n) - 1
    reset = b.bit_length() - 1
    seed = 1 ^ parity(c >> reset)
    d, m, k = (c ^ b) & mask, (~b) & mask, 1
    while k < n:
        lo = (1 << k) - 1
        od, om = d, m
        d = (od ^ (om & ((od << k) & mask))) & mask
        m = ((om & lo) | (om & ((om << k) & mask) & (~lo & mask))) & mask
        k <<= 1
    y = d ^ (m if seed else 0)
    return ((y << 1) | seed) & mask


def quotient_seq(w: int, p: int = P, r: int = R) -> tuple[int, ...]:
    """Use the specified analyzer's exact aligned normalized quotient states."""
    x = portal_lift(w, p)
    n, mask = 2 * p, (1 << (2 * p)) - 1
    low, high = x, mask
    dyn = []
    for _ in range(r):
        child = broad_child(low, high, n)
        dyn.append(child)
        high, low = low, child
    states = []
    for s in range(p):
        q = (x >> s) & 1
        st = 0
        for j, z in enumerate(dyn):
            xx = (z >> s) & 1
            yy = xx ^ ((z >> (s + p)) & 1)
            if q:
                xx ^= yy
            st |= xx << (2 * j)
            st |= yy << (2 * j + 1)
        states.append(st)
    return tuple(states)


def endpoint_classifier(w: int) -> int:
    """Degree-7 cyclic orbit-sum formula (6) from the classifier note."""
    bits = lsb_bits(w)
    offsets = (
        (0, 2),
        (0, 1, 2),
        (0, 1, 6),
        (0, 1, 2, 3),
        (0, 1, 2, 6),
        (0, 1, 2, 3, 6),
        (0, 1, 2, 3, 4, 5, 6),
    )
    ans = 0
    for term in offsets:
        orbit = 0
        for i in range(P):
            product = 1
            for a in term:
                product &= bits[(i + a) % P]
            orbit ^= product
        ans ^= orbit
    return ans


def scalar_child(b: list[int], c: list[int]) -> list[int]:
    """Independent cell-array cyclic child, seeded from its last reset."""
    n = len(b)
    resets = [i for i, bit in enumerate(b) if bit]
    if not resets:
        raise ValueError("scalar cyclic recurrence requires a nonzero low plane")
    last = resets[-1]
    a = [0] * n
    a[0] = 1 ^ (sum(c[last:]) & 1)
    for s in range(n):
        a[(s + 1) % n] = c[s] ^ (b[s] | a[s])
    return a


def scalar_cyclic_child(b: int, c: int, n: int) -> int:
    """Two-seed cyclic solver, independent of the packed broad_child formula."""
    if b == 0:
        raise ValueError("zero low plane has no unique child")
    solutions = []
    for seed in (0, 1):
        a, out = seed, 0
        for s in range(n):
            out |= a << s
            a = ((c >> s) & 1) ^ (((b >> s) & 1) | a)
        if a == seed:
            solutions.append(out)
    if len(solutions) != 1:
        raise AssertionError(("cyclic child solution count", b, c, solutions))
    return solutions[0]


def original_two_row_step(state: tuple[int, ...], label: int) -> tuple[int, ...]:
    """Independent original-row normalized transition from the cone checker."""
    pairs = [(1, 0), (0, 1)] + list(zip(state[::2], state[1::2]))
    output = []
    for j in range(2, len(pairs)):
        h, l, x = pairs[j - 2:j + 1]
        first = h[0] ^ (l[0] | x[0])
        second = (h[0] ^ h[1]) ^ ((l[0] ^ l[1]) | (x[0] ^ x[1]))
        difference = first ^ second
        output.extend((first ^ (label & difference), difference))
    return tuple(output)


def blind_basis(free: list[int]) -> tuple[list[int], list[int]]:
    """Pivot at sorted free[0]; basis is e_s+e_pivot for every later s."""
    if not free:
        return [], []
    phases = free[1:]
    vectors = [(1 << s) ^ (1 << free[0]) for s in phases]
    if gf2_rank(vectors) != len(free) - 1 or any(v == 0 for v in vectors):
        raise AssertionError(("invalid parity-constrained blind basis", free, vectors))
    return phases, vectors


def basis_coordinates(anchor: int, member: int, phases: list[int], vectors: list[int]) -> tuple[int, list[int]]:
    diff = member ^ anchor
    coeffs = [(diff >> phase) & 1 for phase in phases]
    reconstructed = 0
    for coeff, vector in zip(coeffs, vectors):
        if coeff:
            reconstructed ^= vector
    return reconstructed, coeffs


def scalar_phase_states(x: int, layers: list[int], p: int) -> list[list[int]]:
    states = []
    for s in range(p):
        flat = []
        q = (x >> s) & 1
        for z in layers:
            xx = (z >> s) & 1
            yy = xx ^ ((z >> (s + p)) & 1)
            if q:
                xx ^= yy
            flat.extend((xx, yy))
        states.append(flat)
    return states


def p8_scalar_two_row_control(analyzer) -> dict:
    """Exhaust all odd p=8 drivers, scalar stacks through depth 7."""
    p, max_depth, n = 8, 7, 16
    by_depth = {d: {"drivers": 0, "quotient_state_comparisons": 0,
                    "two_row_phase_updates": 0} for d in range(1, max_depth + 1)}
    scalar_child_solves = 0
    early_zero = []
    words = [w for w in range(1 << p) if parity(w)]
    for w in words:
        check_caps()
        x = analyzer.portal_lift(w, p)
        low, high = x, (1 << n) - 1
        layers = []
        for depth in range(1, max_depth + 1):
            if low == 0:
                early_zero.append({"driver": w, "first_unconstructible_depth": depth})
                break
            child = scalar_cyclic_child(low, high, n)
            scalar_child_solves += 1
            layers.append(child)
            high, low = low, child
            flat_states = scalar_phase_states(x, layers, p)
            analyzer_states = tuple(analyzer.quotient_seq(w, p, depth))
            analyzer_flat = tuple(tuple((state >> i) & 1 for i in range(2 * depth)) for state in analyzer_states)
            if tuple(tuple(st) for st in flat_states) != analyzer_flat:
                raise AssertionError(("p8 scalar full-bit quotient comparison", w, depth, flat_states, analyzer_flat))
            by_depth[depth]["drivers"] += 1
            by_depth[depth]["quotient_state_comparisons"] += p
            by_depth[depth]["two_row_phase_updates"] += p
            for s in range(p):
                got = original_two_row_step(tuple(flat_states[s]), (w >> s) & 1)
                want = tuple(flat_states[(s + 1) % p])
                if got != want:
                    raise AssertionError(("p8 temporal two-row update", w, depth, s, got, want))
    return {"p": 8, "input_count": len(words), "odd_driver_words_lsb_first_sha256":
            sha("\n".join("".join(map(str, lsb_bits(w, 8))) for w in words).encode()),
            "scalar_two_seed_child_solves": scalar_child_solves,
            "depth_counts": {str(d): by_depth[d] for d in range(1, max_depth + 1)},
            "early_zero_cases": early_zero, "early_zero_count": len(early_zero),
            "all_inputs_accounted_for": len(early_zero) + by_depth[max_depth]["drivers"] == len(words),
            "result": "all comparisons and same-depth phase transitions passed"}


def basis_algebra_control() -> dict:
    """Mechanical parity-cube tests, including the anchor-free[0]=0 bug case."""
    cases = []
    for name, free, anchor, assignments, functions in (
        ("k2_even_blind_parity_anchor_pivot_zero", [0, 1], 4, [0, 3],
         {"identity_pair": lambda x: (x & 1, (x >> 1) & 1),
          "linear_xor": lambda x: ((x & 1) ^ ((x >> 1) & 1),),
          "nonlinear_product": lambda x: ((x & 1) & ((x >> 1) & 1),)}),
        ("k3_even_blind_parity_affine_square", [0, 1, 2], 8, [0, 3, 5, 6],
         {"identity_pair": lambda x: ((x >> 1) & 1, (x >> 2) & 1),
          "linear_xor": lambda x: ((x & 1) ^ ((x >> 2) & 1),),
          "nonlinear_product": lambda x: (((x >> 1) & 1) & ((x >> 2) & 1),)}),
    ):
        phases, vectors = blind_basis(free)
        expected_rank = len(free) - 1
        if gf2_rank(vectors) != expected_rank:
            raise AssertionError((name, "rank", vectors))
        # The prescribed assignments are explicit blind-label masks.
        members = [anchor | mask for mask in assignments]
        if any(parity(member) != 1 for member in members) or len(set(members)) != 1 << expected_rank:
            raise AssertionError((name, "cube members", members))
        function_results = {}
        for fname, function in functions.items():
            outputs = {member: function(member) for member in members}
            base_out = outputs[anchor]
            images = [tuple(a ^ b for a, b in zip(base_out, outputs[anchor ^ delta])) for delta in vectors]
            mismatch = False
            for member in members:
                reconstructed, coeffs = basis_coordinates(anchor, member, phases, vectors)
                if reconstructed != (member ^ anchor):
                    raise AssertionError((name, fname, "coordinate reconstruction", member))
                predicted = list(base_out)
                for coeff, image in zip(coeffs, images):
                    if coeff:
                        predicted = [a ^ b for a, b in zip(predicted, image)]
                mismatch |= tuple(predicted) != outputs[member]
            function_results[fname] = {"basis_prediction_mismatch": mismatch}
        if name.startswith("k2_") and any(v["basis_prediction_mismatch"] for v in function_results.values()):
            raise AssertionError((name, "one-dimensional cube must fit every function"))
        if name.startswith("k3_") and not function_results["nonlinear_product"]["basis_prediction_mismatch"]:
            raise AssertionError((name, "nonlinear control was not detected"))
        square_control = None
        if name.startswith("k3_"):
            base = anchor
            wi = base ^ vectors[0]
            wj = base ^ vectors[1]
            wij = base ^ wi ^ wj
            square = (base, wi, wj, wij)
            if (len(set(square)) != 4 or any(parity(word) != 1 for word in square)
                    or base ^ wi ^ wj ^ wij != 0 or any(word not in members for word in square)):
                raise AssertionError((name, "square parallelogram control", square))
            square_control = {"ordered_vertices": list(square), "distinct": True,
                              "all_odd": True, "xor_zero": True}
        cases.append({"name": name, "anchor": anchor, "free_phases": free,
                      "basis_vectors": vectors, "basis_rank": gf2_rank(vectors),
                      "member_masks": assignments, "functions": function_results,
                      "square_parallelogram_control": square_control})
    return {"cases": cases, "all_basis_identity_controls_passed": True}


def verify_extension_witness(w: list[int], p: int, r: int, analyzer) -> dict:
    n = 2 * p
    scalar_states = {}
    for word in w:
        x = analyzer.portal_lift(word, p)
        low, high = x, (1 << n) - 1
        layers = []
        for _ in range(r + 1):
            if low == 0:
                raise AssertionError(("witness left retained-stack domain", word))
            child = scalar_cyclic_child(low, high, n)
            layers.append(child)
            high, low = low, child
        scalar_states[word] = scalar_phase_states(x, layers, p)
        expected = tuple(analyzer.quotient_seq(word, p, r + 1))
        expected_flat = tuple(tuple((state >> j) & 1 for j in range(2 * (r + 1))) for state in expected)
        if tuple(tuple(state) for state in scalar_states[word]) != expected_flat:
            raise AssertionError(("scalar cyclic quotient mismatch", word))
    # Check the original update as a temporal phase transition at each fixed
    # depth. It preserves depth; it does not grow the stack.
    for word in w:
        labels = [((word >> s) & 1) for s in range(p)]
        for depth in range(1, r + 2):
            state_depth = [
                tuple(bit for z in scalar_states[word][s][:2 * depth]) for s in range(p)]
            for s in range(p):
                got = original_two_row_step(state_depth[s], labels[s])
                want = state_depth[(s + 1) % p]
                if got != want:
                    raise AssertionError(("two-row temporal phase transition mismatch", word, depth, s, got, want))
    return {"scalar_two_seed_cyclic_child": "passed for all four words and depths 1..r+1",
            "independent_original_two_row_normalized_update": "passed phasewise for all four words"}


def quotient_parent_and_last_low(w: int, p: int, r: int, analyzer):
    """Return exact R and its raw final low plane; None means earlier zero."""
    n = 2 * p
    x = analyzer.portal_lift(w, p)
    low, high = x, (1 << n) - 1
    for _ in range(r):
        if low == 0:
            return None, 0
        child = analyzer.broad_child(low, high, n)
        high, low = low, child
    if low == 0:
        # The depth-r quotient exists, but the full raw parent track is zero;
        # its next child is not unique.
        return tuple(analyzer.quotient_seq(w, p, r)), 0
    return tuple(analyzer.quotient_seq(w, p, r)), low


def scalar_return(w: int) -> dict:
    n, word = 2 * P, [((w >> (s % P)) & 1) for s in range(2 * P)]
    # D(x)=ww with integration constant x_0=0.
    cur, xbits = 0, []
    for bit in word:
        xbits.append(cur)
        cur ^= bit
    if cur:
        raise AssertionError("scalar portal integration failed")
    low = xbits[:]
    high = [0] * n
    for lifts in range(1, LIFT_CAP + 1):
        check_caps()
        child = scalar_child(low, high)
        high, low = low, child
        if not any(low):
            target = sum(bit << i for i, bit in enumerate(high))
            return {"first_return_depth": lifts, "returned_endpoint_word": target,
                    "returned_endpoint_bits_lsb_first": "".join(map(str, high)),
                    "returned_endpoint_parity": sum(high) & 1}
    raise RuntimeError(f"scalar return exceeded cap {LIFT_CAP} for w={w}")


def main() -> int:
    check_caps()
    start = time.monotonic()
    spec = importlib.util.spec_from_file_location("blind_visit_analyzer", ANALYZER)
    analyzer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(analyzer)
    all_odd = [w for w in range(1 << P) if parity(w)]
    p8_scalar_control = p8_scalar_two_row_control(analyzer)
    basis_control = basis_algebra_control()
    # The task fixes driver labels, so group the literal ordered aligned tuples.
    fibers: dict[tuple[int, ...], list[int]] = {}
    endpoint = {}
    for w in all_odd:
        q = tuple(analyzer.quotient_seq(w, P, R))
        fibers.setdefault(q, []).append(w)
        endpoint[w] = endpoint_classifier(w)
    counts = {"odd": sum(endpoint.values()), "even": len(endpoint) - sum(endpoint.values())}
    if counts != {"odd": 56, "even": 72}:
        raise AssertionError(f"degree-7 classifier count mismatch: {counts}")

    witness = None
    for state, words in sorted(fibers.items(), key=lambda item: item[1]):
        for quad in itertools.combinations(words, 4):
            check_caps()
            a, b, c, d = quad
            if a ^ b ^ c ^ d:
                continue
            if endpoint[a] ^ endpoint[b] ^ endpoint[c] ^ endpoint[d]:
                witness = {"drivers": list(quad), "state_sequence": list(state),
                           "classifier_endpoint_parities": [endpoint[x] for x in quad]}
                break
        if witness:
            break

    direct = None
    status = "finite-exhaustive"
    interpretation = "No counterexample found among all aligned p=8,r=1 fibers; this is finite evidence only."
    if witness:
        for w in witness["drivers"]:
            check_caps()
            direct_entry = scalar_return(w)
            if direct_entry["returned_endpoint_parity"] != endpoint[w]:
                raise AssertionError(f"independent scalar replay disagreed at w={w}")
            if direct is None:
                direct = []
            direct.append({"driver": w, **direct_entry})
        if len({tuple(quotient_seq(w)) for w in witness["drivers"]}) != 1:
            raise AssertionError("certificate drivers do not share the exact state tuple")
        if len(set(witness["drivers"])) != 4 or __import__("functools").reduce(int.__xor__, witness["drivers"], 0) != 0:
            raise AssertionError("certificate is not a distinct parallelogram")
        if __import__("functools").reduce(int.__xor__, witness["classifier_endpoint_parities"], 0) != 1:
            raise AssertionError("certificate endpoint parity is not non-affine")
        status = "refuted"
        interpretation = "A directly replayed parallelogram refutes affine endpoint parity on a fixed p=8,r=1 quotient fiber."

    extension_results = []
    overall_ext_witness = None
    completed_scopes = []
    stopped_early = None
    try:
        for period in (2, 4, 6, 8, 10, 12, 14):
            period_words = [w for w in range(1 << period) if parity(w)]
            for depth in range(1, 7):
                check_caps()
                cube_stream = hashlib.sha256()
                groups: dict[tuple[int, ...], list[int]] = {}
                parent_info = {}
                for w in period_words:
                    check_caps()
                    parent, last_low = quotient_parent_and_last_low(w, period, depth, analyzer)
                    parent_info[w] = (parent, last_low)
                    if parent is None:
                        continue
                    groups.setdefault(parent, []).append(w)

                scope = {"p": period, "depth_r": depth,
                         "odd_driver_count": len(period_words),
                         "earlier_zero_driver_count": sum(parent_info[w][0] is None for w in period_words),
                         "constructible_parent_fiber_count": len(groups)}
                scope_witness = None
                eligible_groups = []
                excluded_zero_parent_groups = 0
                excluded_earlier_zero_groups = 0
                excluded_incomplete_cube_groups = 0
                excluded_zero_parent_drivers = 0
                excluded_cube_earlier_zero_drivers = 0
                histogram = {}
                max_dimension = 0
                basis_checks = 0
                affine_member_prediction_checks = 0
                candidate_cube_cardinality_checks = 0
                completeness_checks = 0
                canonical_cube_certificate = None
                nonconstant_y_fiber_count = 0
                first_y_history_pair = None
                for parent, members in sorted(groups.items(), key=lambda item: item[1]):
                    check_caps()
                    blind = [s for s, st in enumerate(parent) if analyzer.blind_state(st, depth)]
                    anchor = min(members)
                    fixed_mask = sum(1 << s for s in range(period) if s not in blind)
                    free = blind
                    basis_phases, basis_vectors = blind_basis(free)
                    fixed_bits = anchor & fixed_mask
                    expected = sorted(sum(((fixed_bits >> s) & 1) << s for s in range(period) if s not in blind)
                                      | sum(value << phase for phase, value in zip(blind, assignment))
                                      for assignment in itertools.product((0, 1), repeat=len(blind))
                                      if parity(sum(value << phase for phase, value in zip(blind, assignment)) | fixed_bits))
                    expected_cardinality = (1 << max(0, len(blind) - 1)) if blind else int(parity(fixed_bits) == 1)
                    if len(expected) != expected_cardinality or len(set(expected)) != len(expected):
                        raise AssertionError(("blind-label cube cardinality", period, depth, blind, expected_cardinality, expected))
                    candidate_cube_cardinality_checks += 1
                    # Exclude whole parent fibers unless every odd-cube label
                    # constructs this same R and has a nonzero final raw track.
                    statuses = [parent_info.get(w, (None, 0)) for w in expected]
                    if any(pr is None for pr, _ in statuses):
                        excluded_earlier_zero_groups += 1
                        excluded_cube_earlier_zero_drivers += len(expected)
                        cube_stream.update(json.dumps({"p": period, "r": depth, "parent": list(parent),
                                                       "excluded": "earlier-zero", "members": expected},
                                                      sort_keys=True, separators=(",", ":")).encode() + b"\n")
                        continue
                    if any(low == 0 for _, low in statuses):
                        excluded_zero_parent_groups += 1
                        excluded_zero_parent_drivers += len(expected)
                        cube_stream.update(json.dumps({"p": period, "r": depth, "parent": list(parent),
                                                       "excluded": "zero-final-parent", "members": expected},
                                                      sort_keys=True, separators=(",", ":")).encode() + b"\n")
                        continue
                    if expected != members:
                        # A constructible nonzero member cannot be silently
                        # dropped: that would be an invalid truncated fiber.
                        raise AssertionError(("odd blind cube does not equal complete exact orbit", period, depth,
                                              parent, members, expected, blind))
                    if any(pr != parent for pr, _ in statuses):
                        raise AssertionError(("fixed blind cube does not retain parent orbit", period, depth, parent))
                    completeness_checks += 1

                    outputs = {w: tuple(analyzer.quotient_seq(w, period, depth + 1)) for w in expected}
                    eligible_groups.append((parent, expected, blind, anchor, basis_phases, basis_vectors, outputs))
                    y_histories = {w: tuple((state >> (2 * (depth + 1) - 1)) & 1
                                            for state in outputs[w]) for w in expected}
                    if len(set(y_histories.values())) > 1:
                        nonconstant_y_fiber_count += 1
                        if first_y_history_pair is None:
                            pair = next(( (u, v) for i, u in enumerate(expected)
                                          for v in expected[i + 1:]
                                          if y_histories[u] != y_histories[v]), None)
                            if pair:
                                first_y_history_pair = {"drivers": list(pair),
                                                         "parent_state_sequence": list(parent),
                                                         "newest_Y_histories": [list(y_histories[w]) for w in pair]}
                    dimension = len(basis_vectors)
                    max_dimension = max(max_dimension, dimension)
                    histogram[str(len(expected))] = histogram.get(str(len(expected)), 0) + 1
                    base_out = outputs[anchor]
                    basis_images = []
                    for delta in basis_vectors:
                        member = anchor ^ delta
                        if member not in outputs:
                            raise AssertionError(("odd cube basis member missing", period, depth, member))
                        basis_images.append(tuple(base_out[s] ^ outputs[member][s] for s in range(period)))
                    affine_bad = None
                    for member in expected:
                        predicted = list(base_out)
                        diff = member ^ anchor
                        reconstructed_delta, coeffs = basis_coordinates(anchor, member, basis_phases, basis_vectors)
                        for coeff, image in zip(coeffs, basis_images):
                            if coeff:
                                predicted = [a ^ b for a, b in zip(predicted, image)]
                        if reconstructed_delta != diff:
                            raise AssertionError(("blind-cube basis coordinates do not reconstruct member", period,
                                                  depth, anchor, member, diff, reconstructed_delta, basis_phases))
                        if tuple(predicted) != outputs[member]:
                            affine_bad = member
                            break
                        affine_member_prediction_checks += 1
                    basis_checks += 1
                    cube_ledger = {"p": period, "r": depth, "parent": list(parent), "blind_phases": blind,
                                   "fixed_nonblind_labels": {str(s): (anchor >> s) & 1 for s in range(period) if s not in blind},
                                   "anchor": anchor, "basis_vectors": basis_vectors, "member_count": len(expected),
                                   "basis_rank": gf2_rank(basis_vectors),
                                   "members_sha256": sha(json.dumps(expected, separators=(",", ":")).encode()),
                                   "output_sha256": sha(json.dumps([[w, list(outputs[w])] for w in expected], separators=(",", ":")).encode()),
                                   "affine_match": affine_bad is None}
                    cube_stream.update(json.dumps(cube_ledger, sort_keys=True, separators=(",", ":")).encode() + b"\n")
                    if canonical_cube_certificate is None and dimension > 0:
                        canonical_cube_certificate = {k: cube_ledger[k] for k in ("anchor", "blind_phases", "fixed_nonblind_labels", "basis_vectors", "basis_rank", "member_count", "members_sha256", "output_sha256", "affine_match")}
                    if affine_bad is not None:
                        # A nonlinear Boolean map has a nonzero second finite
                        # difference on some square in this affine cube.
                        for base in expected:
                            for i in range(len(basis_vectors)):
                                for j in range(i + 1, len(basis_vectors)):
                                    check_caps()
                                    wi = base ^ basis_vectors[i]
                                    wj = base ^ basis_vectors[j]
                                    wij = base ^ wi ^ wj
                                    if not all(x in outputs for x in (wi, wj, wij)):
                                        continue
                                    xor_out = tuple(outputs[base][s] ^ outputs[wi][s] ^
                                                    outputs[wj][s] ^ outputs[wij][s]
                                                    for s in range(period))
                                    if any(xor_out):
                                        quad = sorted((base, wi, wj, wij))
                                        candidate = {"p": period, "depth_r": depth, "drivers": quad,
                                                    "parent_state_sequence": list(parent),
                                                    "child_sequences": [list(outputs[x]) for x in quad],
                                                    "phasewise_nonzero_output_xor": [i for i, x in enumerate(xor_out) if x],
                                                    "raw_phasewise_output_xor": list(xor_out)}
                                        if scope_witness is None:
                                            scope_witness = candidate
                            if scope_witness:
                                break
                        if scope_witness is None:
                            raise AssertionError(("affine mismatch lacked coordinate-basis-square witness",
                                                  period, depth, parent, affine_bad))
                    if scope_witness:
                        break
                scope.update({"eligible_nonzero_parent_fiber_count": len(eligible_groups),
                              "eligible_driver_count": sum(len(g[1]) for g in eligible_groups),
                              "excluded_zero_parent_fiber_count": excluded_zero_parent_groups,
                              "excluded_zero_parent_driver_count": excluded_zero_parent_drivers,
                              "excluded_earlier_zero_cube_fiber_count": excluded_earlier_zero_groups,
                              "excluded_earlier_zero_driver_count": scope["earlier_zero_driver_count"] + excluded_cube_earlier_zero_drivers,
                              "excluded_incomplete_cube_fiber_count": excluded_incomplete_cube_groups,
                              "candidate_cube_cardinality_checks": candidate_cube_cardinality_checks,
                              "verified_full_odd_cube_count": completeness_checks,
                              "affine_fiber_basis_checks": basis_checks,
                              "affine_member_prediction_checks": affine_member_prediction_checks,
                              "maximum_affine_dimension": max_dimension,
                              "eligible_cube_size_histogram": histogram,
                              "all_declared_odd_parent_fibers_complete": (
                                  scope["earlier_zero_driver_count"] == 0 and
                                  excluded_zero_parent_groups == 0 and excluded_earlier_zero_groups == 0 and
                                  excluded_incomplete_cube_groups == 0),
                              "nonconstant_newest_Y_history_fiber_count": nonconstant_y_fiber_count,
                              "first_newest_Y_history_difference_pair": first_y_history_pair,
                              "canonical_nontrivial_cube_certificate": canonical_cube_certificate,
                              "cube_ledger_stream_sha256": cube_stream.hexdigest()})
                scope["first_coordinate_basis_square_witness"] = scope_witness
                scope["status"] = "counterexample" if scope_witness else "finite-exhaustive-survival"
                if scope_witness:
                    verify = verify_extension_witness(scope_witness["drivers"], period, depth, analyzer)
                    scope_witness["independent_verification"] = verify
                    extension_results.append(scope)
                    overall_ext_witness = scope_witness
                    stopped_early = {"reason": "first counterexample", "remaining_scopes": [
                        {"p": p2, "r": r2} for p2 in (2, 4, 6, 8, 10, 12, 14)
                        for r2 in range(1, 7) if (p2, r2) > (period, depth)]}
                    raise StopIteration
                extension_results.append(scope)
                completed_scopes.append({"p": period, "r": depth})
    except StopIteration:
        pass
    except (TimeoutError, MemoryError) as exc:
        stopped_early = {"reason": str(exc), "remaining_scopes": [
            {"p": p2, "r": r2} for p2 in (2, 4, 6, 8, 10, 12, 14)
            for r2 in range(1, 7) if {"p": p2, "r": r2} not in completed_scopes and
            not any(s.get("p") == p2 and s.get("depth_r") == r2 for s in extension_results)]}

    elapsed = time.monotonic() - start
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    source_bytes, analyzer_bytes, note_bytes = Path(__file__).read_bytes(), ANALYZER.read_bytes(), CLASSIFIER_NOTE.read_bytes()
    ref_bytes = REFERENCE.read_bytes()
    if sha(ref_bytes) != "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01":
        raise AssertionError("immutable reference hash differs from repository handoff")
    payload = {"fiber_count": len(fibers), "fiber_size_histogram": {
        str(k): sum(len(v) == k for v in fibers.values()) for k in sorted({len(v) for v in fibers.values()})},
        "odd_driver_count": len(all_odd), "classifier_counts": counts,
        "parallelogram_witness": witness, "direct_scalar_replays": direct,
        "independent_controls": {"p8_all_odd_scalar_and_two_row": p8_scalar_control,
                                 "blind_basis_algebra": basis_control},
        "one_layer_observation_extension": {"scope_order": "p ascending, then r ascending",
            "scopes_completed": completed_scopes, "scopes": extension_results,
            "first_witness": overall_ext_witness, "stopped_early": stopped_early}}
    result_hash = sha(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    record = {
        "experiment_id": "20261002_blind_fiber_endpoint_affinity_and_blind_cube_extension",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(), "git_commit": commit,
        "question": "problem1", "hypothesis": {"H_endpoint": "For every fixed exact aligned normalized quotient state sequence R_s at p=8,r=1, f8(w) is affine over GF(2) in the odd driver labels.", "H_ext": "For p=2,4,6,8,10,12,14 and r=1..6, on every fixed exact aligned depth-r quotient orbit in the retained-stack domain, the full aligned depth-(r+1) state sequence is affine in the odd hidden driver labels."},
        "backend": "Python analyzer quotient plus degree-7 endpoint classifier; exhaustive independent scalar two-seed and original two-row controls",
        "parameters": {"H_endpoint": {"p": 8, "r": 1, "input_count": 128}, "H_ext": {"p_values": [2,4,6,8,10,12,14], "r_values": [1,2,3,4,5,6], "driver_domain_each_scope": "all odd p-bit words", "exact_odd_affine_cube_required": True, "affine_map_check": "anchor plus explicit blind-label basis; check predicted output for every fiber member", "witness_order": "first coordinate-basis-square witness; p/r ascending, fibers by sorted member lists, then base and basis directions"}, "alignment": "literal aligned phase; no necklace canonicalization", "quotient_grouping": "exact tuple returned by analyze_blind_visit_rank.quotient_seq", "classifier_terms_offsets": [[0,2],[0,1,2],[0,1,6],[0,1,2,3],[0,1,2,6],[0,1,2,3,6],[0,1,2,3,4,5,6]], "first_return_lift_cap_per_input": LIFT_CAP},
        "admission": {"basis": "Parent-admitted bounded transport falsification. A witness refutes the tested affine fiber map in its declared domain; survival is finite evidence about driver-label transport and does not establish the parent theorem.", "whole_tail_relevance": "A counterexample rules out this affine fixed-state route as stated; no counterexample leaves a finite candidate statistic to assess, without resolving the whole-tail conjecture."},
        "hardware": {"platform": platform.platform(), "machine": platform.machine(), "cpu_model": cpu_model(), "logical_cpu_count": os.cpu_count(), "peak_rss_bytes": peak_rss_bytes()},
        "software": {"python": sys.version, "executable": sys.executable, "platform": platform.platform()}, "runtime_seconds": elapsed,
        "resource_caps": {"overall_wall_seconds": WALL_CAP, "first_return_lifts_per_input": LIFT_CAP, "resident_memory_bytes": MEMORY_CAP, "output_bytes": 256 * 1024},
        "result_hashes": {"summary_sha256": result_hash, "script_sha256": sha(source_bytes), "analyzer_sha256": sha(analyzer_bytes), "classifier_note_sha256": sha(note_bytes), "immutable_reference_sha256": sha(ref_bytes)},
        "source_and_input_hashes": {"experiments/problem1_nonperiodicity/check_blind_fiber_endpoint_affinity.py": sha(source_bytes), "experiments/problem1_nonperiodicity/analyze_blind_visit_rank.py": sha(analyzer_bytes), "proofs/informal/problem1_last_reset_child_and_endpoint_parity_complexity.md": sha(note_bytes), "src/python/rule30_research_reference.py": sha(ref_bytes), "odd_driver_words_lsb_first_sha256": sha("\n".join("".join(map(str, lsb_bits(w))) for w in all_odd).encode())},
        "result_summary": payload, "interpretation": interpretation, "status": status,
        "H_ext_status": "counterexample" if overall_ext_witness else ("partial-finite" if stopped_early else "finite-exhaustive-on-nonzero-parent-domain"),
        "H_ext_all_parent_fibers_complete": (stopped_early is None and len(completed_scopes) == 42 and
                                               all(s["all_declared_odd_parent_fibers_complete"] for s in extension_results)),
        "implementation_diagnostics": {"superseded_basis_bug": "Previous conditional pivot selection could include a zero vector and omit a valid direction when anchor[free[0]]=0. Current basis always uses the first sorted blind phase as pivot and every remaining phase as e_s XOR e_pivot; rank and per-member coordinates are checked. This was an implementation correction, not mathematical evidence."},
        "proof_scope": "H_endpoint remains the completed p=8,r=1 finite check. H_ext is finite-exhaustive only for the exact scopes listed in result_summary; every tested parent fiber was checked against its exact odd affine cube, followed by an anchor-basis affine prediction for all members. No infinite statement is proved.",
        "limitations": ["H_ext is limited to p=2,4,6,8,10,12,14 and r=1..6, subject to any reported cap or first witness stop.", "Inputs with a zero low plane before the requested stack are listed as outside the retained-stack domain; no child is assigned. Per-scope all-parent-fibers-complete flags disclose exclusions.", "The p=8 independent scalar/two-row control exhausts all odd drivers through depth seven, stopping at early zero planes.", "H_endpoint parity counts are rechecked with the historical degree-7 classifier; this run performs no new portal first-return traversal.", "The 60-second, 300000-lift, 256-MiB resident-memory, and 256-KiB output caps are recorded; no cap was enlarged.", "No conclusion is drawn about the whole-tail conjecture or untested p/r."],
        "provenance": {"analyzer_source": analyzer_bytes.decode(), "classifier_note": note_bytes.decode(), "immutable_reference_path": "src/python/rule30_research_reference.py", "immutable_reference_sha256": sha(ref_bytes)}
    }
    if time.monotonic() - START > WALL_CAP:
        raise TimeoutError("overall wall-time cap reached before result write")
    atomic_json(OUT, record)
    print(json.dumps({"status": status, "runtime_seconds": elapsed, "fiber_count": len(fibers), "histogram": payload["fiber_size_histogram"], "witness": witness, "result": str(OUT), "sha256": sha(OUT.read_bytes())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (TimeoutError, MemoryError, RuntimeError) as exc:
        print(json.dumps({"status": "inconclusive", "failure": str(exc), "elapsed_seconds": time.monotonic() - START}), file=sys.stderr)
        raise
