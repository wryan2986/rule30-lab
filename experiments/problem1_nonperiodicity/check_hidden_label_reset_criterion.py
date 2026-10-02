#!/usr/bin/env python3
"""Bounded H_reset falsification and targeted triple-presentation fiber check."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20261002_hidden_label_reset_criterion.json"
ANALYZER_PATH = ROOT / "experiments/problem1_nonperiodicity/analyze_blind_visit_rank.py"
STACK_NOTE = ROOT / "proofs/informal/problem1_portal_multilift_phase_quotient.md"
MONODROMY_NOTE = ROOT / "proofs/informal/problem1_portal_layer_monodromy.md"
SHALLOW_NOTE = ROOT / "proofs/informal/problem1_shallow_blind_label_affinity.md"
PERIODS = (2, 4, 6, 8, 10, 12, 14)
DEPTHS = range(1, 7)
WALL_CAP = 60.0
MEMORY_CAP = 256 * 1024 * 1024
OUTPUT_CAP = 256 * 1024
REFERENCE_PATH = ROOT / "src/python/rule30_research_reference.py"
REFERENCE_SHA256 = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
START = time.monotonic()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def check_caps() -> None:
    if time.monotonic() - START > WALL_CAP:
        raise TimeoutError("overall 60-second wall cap reached")
    status = Path("/proc/self/status").read_text()
    rss_kib = int(next(line.split()[1] for line in status.splitlines() if line.startswith("VmRSS:")))
    if rss_kib * 1024 > MEMORY_CAP:
        raise MemoryError("256-MiB resident-memory cap reached")


def peak_rss_bytes() -> int:
    status = Path("/proc/self/status").read_text()
    return int(next(line.split()[1] for line in status.splitlines() if line.startswith("VmHWM:"))) * 1024


def cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.lower().startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unavailable"


def atomic_json(path: Path, obj: dict) -> None:
    raw = (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode()
    if len(raw) > OUTPUT_CAP:
        raise ValueError(f"result exceeds 256-KiB output cap: {len(raw)} bytes")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def canonical_sha(obj: object) -> str:
    return sha(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def source_hash_mapping(source_bytes: bytes, analyzer_bytes: bytes, stack_bytes: bytes,
                        mono_bytes: bytes, shallow_bytes: bytes, reference_bytes: bytes) -> dict:
    if sha(reference_bytes) != REFERENCE_SHA256:
        raise AssertionError("immutable reference hash differs from recorded repository provenance")
    return {
        "experiments/problem1_nonperiodicity/check_hidden_label_reset_criterion.py": sha(source_bytes),
        "experiments/problem1_nonperiodicity/analyze_blind_visit_rank.py": sha(analyzer_bytes),
        "proofs/informal/problem1_portal_multilift_phase_quotient.md": sha(stack_bytes),
        "proofs/informal/problem1_portal_layer_monodromy.md": sha(mono_bytes),
        "proofs/informal/problem1_shallow_blind_label_affinity.md": sha(shallow_bytes),
        "src/python/rule30_research_reference.py": sha(reference_bytes),
    }


def load_analyzer():
    spec = importlib.util.spec_from_file_location("hidden_reset_existing_analyzer", ANALYZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load existing analyzer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bit(word: int, phase: int) -> int:
    return (word >> phase) & 1


def raw_layer_pair(state: int, layer: int) -> tuple[int, int]:
    """Decode normalized (X,Y) for one-indexed dynamic layer."""
    off = 2 * (layer - 1)
    return (bit(state, off), bit(state, off + 1))


def scalar_child(low: int, high: int, n: int) -> int:
    """Independent cyclic child from a_(s+1)=c_s XOR (b_s OR a_s)."""
    def run(seed: int, keep: bool) -> tuple[int, int]:
        y = seed
        word = 0
        for s in range(n):
            if keep:
                word |= y << s
            b, c = bit(low, s), bit(high, s)
            y = c ^ (b | y)
        return y, word

    end0, _ = run(0, False)
    end1, _ = run(1, False)
    if end0 != end1:
        raise AssertionError("nonzero low track did not synchronize scalar return")
    seed = end0
    end, word = run(seed, True)
    if end != seed:
        raise AssertionError("scalar cyclic seed failed closure")
    return word


def scalar_stack_ordered(w: int, p: int, depth: int) -> list[int]:
    n = 2 * p
    q = x = 0
    for s in range(n):
        x |= q << s
        q ^= bit(w, s % p)
    if q:
        raise AssertionError("odd driver integration failed to close at 2p")
    low, high = x, (1 << n) - 1
    layers = []
    for _ in range(depth):
        child = scalar_child(low, high, n)
        layers.append(child)
        high, low = low, child
    return layers


def two_row_step(state: int, w_s: int, depth: int) -> int:
    """Original paired two-row quotient recurrence, independent of analyzer."""
    prev = [(1, 0), (0, 1)]
    for j in range(depth):
        prev.append(raw_layer_pair(state, j + 1))
    nxt = []
    for j in range(depth):
        Xjm2, Yjm2 = prev[j]
        Xjm1, Yjm1 = prev[j + 1]
        X, Y = prev[j + 2]
        F = Xjm2 ^ (Xjm1 | X)
        D = Yjm2 ^ Yjm1 ^ Y ^ (Xjm1 & Y) ^ (Yjm1 & X) ^ (Yjm1 & Y)
        nxt.append((F ^ (w_s & D), D))
    out = 0
    for j, (X, Y) in enumerate(nxt):
        out |= X << (2 * j)
        out |= Y << (2 * j + 1)
    return out


def independent_witness_replay(w: int, p: int, r: int, s: int, analyzer_seq: list[int], analyzer) -> dict:
    raw_layers = scalar_stack_ordered(w, p, r + 1)
    q = 0
    raw_seq = []
    for phase in range(p):
        state = 0
        for j, raw in enumerate(raw_layers):
            X = bit(raw, phase)
            Y = X ^ bit(raw, phase + p)
            if q:
                X ^= Y
            state |= X << (2 * j)
            state |= Y << (2 * j + 1)
        raw_seq.append(state)
        q ^= bit(w, phase)
    if q != 1:
        raise AssertionError("half-period q did not flip")
    if raw_seq != analyzer_seq:
        raise AssertionError("independent scalar child disagrees with existing analyzer")
    propagated = [raw_seq[0]]
    state = raw_seq[0]
    for phase in range(p):
        state = two_row_step(state, bit(w, phase), r + 1)
        propagated.append(state)
        expected = raw_seq[(phase + 1) % p]
        if state != expected:
            raise AssertionError(("original two-row transition mismatch", phase, state, expected))
    if propagated[-1] != propagated[0]:
        raise AssertionError("two-row transition did not close cyclically")

    blind = [analyzer.blind_state(st, r) for st in raw_seq]
    target_y = bit(raw_seq[(s + 1) % p], 2 * r + 1)
    b = None
    for j in range(1, p + 1):
        if bit(raw_seq[(s + j) % p], 2 * (r - 1) + 1):
            b = j
            break
    if b is None:
        b = p + 1
    witnesses = [j for j in range(1, b) if raw_layer_pair(raw_seq[(s + j) % p], r) == (1, 0)]
    if not blind[s] or target_y != 1 or witnesses:
        raise AssertionError("recorded witness fails independent reset-criterion check")
    return {
        "scalar_child_replay": "passed",
        "original_two_row_transition_replay": "passed",
        "phasewise_stack_match": True,
        "driver_bits_lsb_first": [bit(w, i) for i in range(p)],
        "phase_s": s,
        "blind_at_depth_r": blind[s],
        "newest_Y_r_plus_1_at_s_plus_1": target_y,
        "first_parent_Y_r_one_distance_b": b if b <= p else "p+1 (none in one cycle)",
        "parent_pair_at_first_Y_one": (
            {"j": b, "phase": (s + b) % p,
             "X_r": raw_layer_pair(raw_seq[(s + b) % p], r)[0],
             "Y_r": raw_layer_pair(raw_seq[(s + b) % p], r)[1]}
            if b <= p else None),
        "X1_Y0_witness_distances_before_b": witnesses,
        "parent_pairs_forward_through_b": [
            {"j": j, "phase": (s + j) % p, "X_r": raw_layer_pair(raw_seq[(s + j) % p], r)[0],
             "Y_r": raw_layer_pair(raw_seq[(s + j) % p], r)[1]}
            for j in range(1, min(b, p + 1))
        ],
        "normalized_state_cycle": raw_seq,
        "raw_scalar_layer_words_lsb_first_2p": [
            "".join(str(bit(layer, i)) for i in range(2 * p)) for layer in raw_layers
        ],
    }


def triple_presentation_fiber(analyzer) -> dict:
    """Targeted four-word aligned p=30 fiber; no enumeration beyond four inputs."""
    p, base_period, r = 30, 10, 6
    base_w = 55 | (55 << 10) | (55 << 20)
    base_seq30 = analyzer.quotient_seq(base_w, p, r)
    base_seq10 = analyzer.quotient_seq(55, base_period, r)
    expected_repetition = all(base_seq30[s] == base_seq10[s % base_period] for s in range(p))
    blind = [s for s, st in enumerate(base_seq30) if analyzer.blind_state(st, r)]
    triple_base_blind = [s + k * base_period for k in range(3)
                         for s, st in enumerate(base_seq10) if analyzer.blind_state(st, r)]
    parent_nonzero = any(raw_layer_pair(st, r) != (0, 0) for st in base_seq30)
    base_info = {
        "p": p, "r": r, "base_period": base_period,
        "base_w_integer": base_w,
        "base_w_bits_lsb_first": "".join(str(bit(base_w, i)) for i in range(p)),
        "base_weight": base_w.bit_count(),
        "complete_depth_r_upper_orbit_is_three_aligned_copies": expected_repetition,
        "depth_r_blind_phases": blind,
        "three_copies_of_base_blind_set": triple_base_blind,
        "blind_set_matches_three_copies": blind == triple_base_blind,
        "depth_r_parent_nonzero": parent_nonzero,
        "depth_r_upper_orbit_sha256": sha(json.dumps(base_seq30, separators=(",", ":")).encode()),
    }
    if not expected_repetition or not parent_nonzero:
        return {"status": "parent-before-expansion", "base": base_info,
                "reason": "repeated aligned upper orbit or nonzero-parent premise failed"}

    cube_size = 1 if not blind else 1 << (len(blind) - 1)
    if cube_size > 4:
        return {"status": "parent-before-expansion", "base": base_info,
                "odd_fiber_size": cube_size,
                "reason": "actual three-copy blind set gives more than four odd drivers; no expansion performed"}

    nonblind_mask = ((1 << p) - 1) ^ sum(1 << s for s in blind)
    required_blind_parity = 1 ^ (base_w & nonblind_mask).bit_count() % 2
    words = []
    for assignment in range(1 << len(blind)):
        if assignment.bit_count() % 2 != required_blind_parity:
            continue
        w = base_w & nonblind_mask
        for j, phase in enumerate(blind):
            if bit(assignment, j):
                w |= 1 << phase
        words.append(w)
    if len(words) != cube_size:
        raise AssertionError("constructed parity fiber has incorrect cardinality")

    if blind == [4, 14, 24]:
        prescribed = [base_w ^ (1 << 4) ^ (1 << 14),
                      base_w ^ (1 << 4) ^ (1 << 24),
                      base_w ^ (1 << 14) ^ (1 << 24), base_w]
        if set(words) != set(prescribed):
            raise AssertionError("actual exact odd cube differs from prescribed four words")
        words = prescribed
    else:
        words.sort()

    base_upper = [st & ((1 << (2 * r)) - 1) for st in base_seq30]
    inputs = []
    sequences = []
    y_histories = []
    input_stream = bytearray()
    for w in words:
        check_caps()
        if w.bit_count() % 2 != 1 or any(bit(w ^ base_w, s) for s in range(p) if s not in blind):
            raise AssertionError("constructed word escaped the exact odd blind-label fiber")
        seq = analyzer.quotient_seq(w, p, r + 1)
        upper = [st & ((1 << (2 * r)) - 1) for st in seq]
        if upper != base_upper:
            raise AssertionError("candidate word does not share the complete depth-r upper orbit")
        if not any(raw_layer_pair(st, r) != (0, 0) for st in seq):
            raise AssertionError("candidate word has zero depth-r raw parent")
        y = [raw_layer_pair(st, r + 1)[1] for st in seq]
        driver_bits = "".join(str(bit(w, i)) for i in range(p))
        upper_raw = json.dumps(upper, separators=(",", ":")).encode()
        full_raw = json.dumps(seq, separators=(",", ":")).encode()
        y_raw = "".join(map(str, y)).encode()
        input_raw = f"p={p};w_lsb={driver_bits}".encode()
        input_stream.extend(input_raw + b"\n")
        inputs.append({"w_integer": w, "w_bits_lsb_first": driver_bits,
                       "weight": w.bit_count(), "odd": True,
                       "driver_sha256": sha(input_raw),
                       "upper_orbit_sha256": sha(upper_raw),
                       "full_depth_r_plus_1_orbit_sha256": sha(full_raw),
                       "newest_Y_history_lsb_phase_order": y_raw.decode(),
                       "newest_Y_history_sha256": sha(y_raw),
                       "upper_orbit_matches_base": True, "nonzero_depth_r_parent": True})
        sequences.append(seq)
        y_histories.append(y)

    y_xor = [0] * p
    full_xor = [0] * p
    for yh, seq in zip(y_histories, sequences):
        for s in range(p):
            y_xor[s] ^= yh[s]
            full_xor[s] ^= seq[s]
    y_equal = all(y == y_histories[0] for y in y_histories[1:])
    y_differences_by_input = {
        str(words[index]): [s for s in range(p) if y_histories[index][s] != y_histories[0][s]]
        for index in range(1, len(words))
    }
    y_difference_union = sorted({s for phases in y_differences_by_input.values() for s in phases})
    upperblind_outputs = {
        str(s): [y[(s + 1) % p] for y in y_histories] for s in blind
    }
    hb_nonconstant = [s for s, values in upperblind_outputs.items() if len(set(values)) > 1]
    y_differences_at_child_output_phases = sorted(
        {((s + 1) % p) for s in blind if ((s + 1) % p) in y_difference_union})
    full_xor_nonzero = [s for s, value in enumerate(full_xor) if value]

    scalar_controls = []
    for index, w in enumerate(words):
        check_caps()
        layers = scalar_stack_ordered(w, p, r + 1)
        q = 0
        scalar_seq = []
        for phase in range(p):
            state = 0
            for j, raw in enumerate(layers):
                X = bit(raw, phase)
                Y = X ^ bit(raw, phase + p)
                if q:
                    X ^= Y
                state |= X << (2 * j)
                state |= Y << (2 * j + 1)
            scalar_seq.append(state)
            q ^= bit(w, phase)
        if q != 1 or scalar_seq != sequences[index]:
            raise AssertionError("independent scalar cyclic child replay disagrees")
        current = scalar_seq[0]
        for phase in range(p):
            current = two_row_step(current, bit(w, phase), r + 1)
            if current != scalar_seq[(phase + 1) % p]:
                raise AssertionError(("original two-row transition replay disagrees", index, phase))
        scalar_controls.append({"w_integer": w, "scalar_child_replay": "passed",
                                "original_two_row_transition_replay": "passed",
                                "phasewise_state_match": True,
                                "raw_layer_word_sha256": sha(json.dumps(layers, separators=(",", ":")).encode())})

    return {
        "status": "four-input-counterexample-to-H_Y" if not y_equal else "H_Y-survives-this-four-input-fiber",
        "scope": "one exact aligned p=30, r=6 odd-label fiber; exactly four inputs, no p=30 enumeration",
        "hash_encoding": "Driver SHA hashes UTF-8 'p=30;w_lsb=<30-bit phase-ordered string>'; orbit hashes compact UTF-8 JSON integer arrays; Y hashes the 30 phase-ordered ASCII bits.",
        "base": base_info,
        "odd_fiber_size": len(words),
        "exact_four_input_cube_verified": len(words) == 4,
        "inputs": inputs,
        "named_H_Y_counterpair": {
            "first_w_integer": 57711655,
            "second_w_integer": 40950823,
            "both_odd_weights": [13, 13],
            "both_least_period_30": True,
            "least_period_certificate": "A repetition count t divides both 30 and the word's weight 13; gcd(30,13)=1 forces t=1.",
            "newest_Y_difference_phases": [s for s in range(p)
                                           if y_histories[0][s] != y_histories[1][s]],
            "first_driver_sha256": inputs[0]["driver_sha256"],
            "second_driver_sha256": inputs[1]["driver_sha256"],
            "first_newest_Y_sha256": inputs[0]["newest_Y_history_sha256"],
            "second_newest_Y_sha256": inputs[1]["newest_Y_history_sha256"],
        },
        "input_set_sha256": sha(bytes(input_stream)),
        "common_complete_depth_r_upper_orbit": True,
        "all_four_depth_r_parents_nonzero": True,
        "H_Y": {"status": "counterexample" if not y_equal else "not-refuted-on-this-fiber",
                "all_newest_Y_histories_equal": y_equal,
                "Y_difference_phases_by_nonbase_input": y_differences_by_input,
                "Y_difference_phase_union": y_difference_union,
                "phasewise_XOR_of_four_newest_Y_histories": "".join(map(str, y_xor)),
                "phasewise_XOR_nonzero_positions": [s for s, value in enumerate(y_xor) if value]},
        "H_B": {"definition": "At each blind phase s of the fixed depth-r upper orbit, child output D_(r+1)(s)=Y_(r+1)(s+1) is constant across this fiber.",
                "upper_blind_phases": blind,
                "child_output_values_at_each_upper_blind_phase": upperblind_outputs,
                "nonconstant_upper_blind_phases": [int(s) for s in hb_nonconstant],
                "status": "counterexample" if hb_nonconstant else "survives-this-four-input-fiber",
                "Y_difference_phases_intersecting_any_s_plus_1": y_differences_at_child_output_phases,
                "any_Y_difference_at_s_plus_1_for_upperblind_s": bool(y_differences_at_child_output_phases)},
        "H_ext": {"status": "affine-parallelogram-passes" if not full_xor_nonzero else "counterexample",
                  "phasewise_XOR_of_four_full_depth_r_plus_1_states": full_xor,
                  "phasewise_XOR_nonzero_positions": full_xor_nonzero},
        "independent_rebuild_controls": scalar_controls,
        "interpretation": "The four-point H_Y failure does not refute H_ext: on this exact 2-cube the XOR of all four full outputs is zero." if not y_equal and not full_xor_nonzero else "Finite targeted fiber result only; no general H_Y or H_ext conclusion.",
        "conditional_lemma_scope": "This finite result neither proves H_B nor proves the parent-supplied conditional H_B=>H_ext. H_B holds on this fiber while H_Y fails, so the two tests separate here.",
    }


def targeted_only() -> int:
    """Read-only replay of the four-word check; preserve the full-run record."""
    analyzer = load_analyzer()
    if sha(REFERENCE_PATH.read_bytes()) != REFERENCE_SHA256:
        raise AssertionError("immutable reference hash differs")
    targeted = triple_presentation_fiber(analyzer)
    check_caps()
    print(json.dumps({"mode": "targeted-only-read-only",
                      "status": targeted["status"],
                      "words": [q["w_integer"] for q in targeted.get("inputs", [])],
                      "H_Y": targeted.get("H_Y", {}).get("status"),
                      "H_B": targeted.get("H_B", {}).get("status"),
                      "H_ext": targeted.get("H_ext", {}).get("status"),
                      "targeted_summary_sha256": canonical_sha(targeted)}, sort_keys=True))
    return 0


def main() -> int:
    analyzer = load_analyzer()
    scopes = []
    completed_scopes = []
    witness = None
    stopped = None
    total_checked = total_parent_nonzero = total_trigger = total_excluded = 0
    odd_input_hash = hashlib.sha256()
    try:
        for p in PERIODS:
            for r in DEPTHS:
                check_caps()
                scope = {"p": p, "r": r, "odd_driver_count": 1 << (p - 1),
                         "drivers_examined": 0, "nonzero_depth_r_parent_drivers": 0,
                         "zero_or_unconstructible_parent_drivers": 0,
                         "blind_phase_count_on_domain": 0,
                         "trigger_phase_count_y_next_one": 0,
                         "tested_reset_predicates": 0,
                         "status": "in-progress"}
                for w in range(1 << p):
                    if w.bit_count() % 2 == 0:
                        continue
                    check_caps()
                    scope["drivers_examined"] += 1
                    total_checked += 1
                    word = "".join(str(bit(w, i)) for i in range(p))
                    odd_input_hash.update(f"p={p};w={word}\n".encode())
                    try:
                        seq = analyzer.quotient_seq(w, p, r + 1)
                    except ValueError:
                        scope["zero_or_unconstructible_parent_drivers"] += 1
                        total_excluded += 1
                        continue
                    parent_nonzero = any(raw_layer_pair(st, r) != (0, 0) for st in seq)
                    if not parent_nonzero:
                        scope["zero_or_unconstructible_parent_drivers"] += 1
                        total_excluded += 1
                        continue
                    scope["nonzero_depth_r_parent_drivers"] += 1
                    total_parent_nonzero += 1
                    for s, st in enumerate(seq):
                        if not analyzer.blind_state(st, r):
                            continue
                        scope["blind_phase_count_on_domain"] += 1
                        y_next = bit(seq[(s + 1) % p], 2 * r + 1)
                        if y_next != 1:
                            continue
                        scope["trigger_phase_count_y_next_one"] += 1
                        total_trigger += 1
                        first_y = None
                        for j in range(1, p + 1):
                            if raw_layer_pair(seq[(s + j) % p], r)[1] == 1:
                                first_y = j
                                break
                        b = first_y if first_y is not None else p + 1
                        scope["tested_reset_predicates"] += 1
                        exists_reset = any(
                            raw_layer_pair(seq[(s + j) % p], r) == (1, 0)
                            for j in range(1, b)
                        )
                        if not exists_reset:
                            witness = {"p": p, "r": r, "w_integer_lsb": w,
                                       "w_bits_lsb_first": [bit(w, i) for i in range(p)],
                                       "phase_s": s, "blind": True,
                                       "Y_r_plus_1_at_s_plus_1": y_next,
                                       "b": b if b <= p else "p+1 (no Y_r=1 in cycle)",
                                       "parent_pair_at_first_Y_one": (
                                           {"j": b, "phase": (s + b) % p,
                                            "X_r": raw_layer_pair(seq[(s + b) % p], r)[0],
                                            "Y_r": raw_layer_pair(seq[(s + b) % p], r)[1]}
                                           if b <= p else None),
                                       "parent_pair_forward": [
                                           {"j": j, "phase": (s + j) % p,
                                            "X_r": raw_layer_pair(seq[(s + j) % p], r)[0],
                                            "Y_r": raw_layer_pair(seq[(s + j) % p], r)[1]}
                                           for j in range(1, min(b, p + 1))
                                       ]}
                            witness["independent_rebuild"] = independent_witness_replay(
                                w, p, r, s, seq, analyzer)
                            scope["status"] = "counterexample"
                            scopes.append(scope)
                            stopped = {"reason": "first witness in requested lexicographic scope order",
                                       "remaining_scopes": [
                                           {"p": pp, "r": rr}
                                           for pp in PERIODS for rr in DEPTHS
                                           if (pp, rr) > (p, r)]}
                            raise StopIteration
                scope["status"] = "finite-exhaustive-survival"
                scopes.append(scope)
                completed_scopes.append({"p": p, "r": r})
    except StopIteration:
        pass
    except (TimeoutError, MemoryError) as exc:
        stopped = {"reason": str(exc), "remaining_scopes": [
            {"p": pp, "r": rr} for pp in PERIODS for rr in DEPTHS
            if {"p": pp, "r": rr} not in completed_scopes and
            not any(q["p"] == pp and q["r"] == rr for q in scopes)]}

    targeted = None
    if stopped is None or stopped.get("reason", "").startswith("first witness"):
        try:
            check_caps()
            targeted = triple_presentation_fiber(analyzer)
        except (TimeoutError, MemoryError) as exc:
            targeted = {"status": "partial-finite-inconclusive", "reason": str(exc)}

    elapsed = time.monotonic() - START
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    source_bytes = Path(__file__).read_bytes()
    analyzer_bytes = ANALYZER_PATH.read_bytes()
    note_bytes = STACK_NOTE.read_bytes()
    mono_bytes = MONODROMY_NOTE.read_bytes()
    shallow_bytes = SHALLOW_NOTE.read_bytes()
    reference_bytes = REFERENCE_PATH.read_bytes()
    source_mapping = source_hash_mapping(source_bytes, analyzer_bytes, note_bytes,
                                        mono_bytes, shallow_bytes, reference_bytes)
    summary = {
        "periods": list(PERIODS), "depths_r": list(DEPTHS),
        "completed_scopes": completed_scopes, "scope_records": scopes,
        "first_counterexample": witness, "stopped_early": stopped,
        "drivers_checked_across_started_scopes": total_checked,
        "nonzero_parent_driver_cases": total_parent_nonzero,
        "excluded_zero_or_unconstructible_parent_cases": total_excluded,
        "trigger_phases_tested": total_trigger,
        "triple_presentation_fiber": targeted,
        "all_42_scopes_completed": len(completed_scopes) == len(PERIODS) * len(tuple(DEPTHS)),
        "odd_driver_input_stream_sha256": odd_input_hash.hexdigest(),
    }
    record = {
        "experiment_id": "20261002_hidden_label_reset_criterion",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "question": "bounded falsification of H_reset on every odd driver for p=2,4,6,8,10,12,14 and r=1..6",
        "hypothesis": "At a depth-r blind phase s with Y_(r+1)(s+1)=1, cyclically before the first Y_r=1 (or through one full cycle if none), some parent pair (X_r,Y_r)=(1,0) occurs.",
        "admission": {
            "basis": "Parent-authorized bounded falsification; no original endpoint traversals.",
            "counterexample_consequence": "Refutes H_reset on the first reported finite scope and invalidates this proposed route to H_Y as stated.",
            "survival_consequence": "Finite evidence only; it does not prove H_reset or H_Y and does not establish a whole-tail result.",
        },
        "backend": "Existing analyze_blind_visit_rank quotient_seq plus independent direct scalar cyclic recurrence and original two-row replay for a witness",
        "reproducible_control": {"command": "python3 experiments/problem1_nonperiodicity/check_hidden_label_reset_criterion.py",
                                 "witness_replay": "The recorded first witness is rebuilt from the direct scalar cyclic child recurrence and checked phasewise against the original two-row quotient update.",
                                 "triple_presentation_fiber": "The same command evaluates exactly the four listed p=30, r=6 drivers and independently rebuilds all four scalar and two-row cyclic stacks.",
                                 "triple_presentation_fiber_targeted_only": "python3 experiments/problem1_nonperiodicity/check_hidden_label_reset_criterion.py --targeted-only"},
        "parameters": {"periods": list(PERIODS), "depths_r": list(DEPTHS),
                       "drivers": "all odd-parity p-bit integers in increasing order; bits displayed LSB-first",
                       "phases": "0..p-1 increasing; no rotation quotient",
                       "witness_order": "p, then r, then integer w, then phase"},
        "resource_caps": {"wall_seconds": WALL_CAP, "resident_memory_bytes": MEMORY_CAP,
                          "output_bytes": OUTPUT_CAP},
        "hardware": {"platform": platform.platform(), "machine": platform.machine(),
                     "cpu_model": cpu_model(), "logical_cpu_count": os.cpu_count(),
                     "peak_rss_bytes": peak_rss_bytes()},
        "software": {"python": sys.version, "executable": sys.executable},
        "runtime_seconds": elapsed,
        "source_hashes": {"checker_sha256": source_mapping["experiments/problem1_nonperiodicity/check_hidden_label_reset_criterion.py"],
                          "existing_analyzer_sha256": source_mapping["experiments/problem1_nonperiodicity/analyze_blind_visit_rank.py"],
                          "portal_stack_note_sha256": source_mapping["proofs/informal/problem1_portal_multilift_phase_quotient.md"],
                          "monodromy_note_sha256": source_mapping["proofs/informal/problem1_portal_layer_monodromy.md"],
                          "shallow_note_sha256": source_mapping["proofs/informal/problem1_shallow_blind_label_affinity.md"],
                          "immutable_reference_sha256": source_mapping["src/python/rule30_research_reference.py"]},
        "source_and_input_hashes": {**source_mapping,
                                    "triple_presentation_fiber_input_set_sha256": targeted.get("input_set_sha256") if targeted else None},
        "result_hashes": {"canonical_summary_sha256": canonical_sha(summary),
                          "immutable_reference_sha256": source_mapping["src/python/rule30_research_reference.py"],
                          "checker_sha256": source_mapping["experiments/problem1_nonperiodicity/check_hidden_label_reset_criterion.py"]},
        "result_summary": summary,
        "status": ("finite-counterexample" if witness else
                   "partial-finite-inconclusive" if stopped else "finite-exhaustive-survival"),
        "interpretation": ("A directly replayed witness falsifies H_reset in the declared finite domain."
                           if witness else
                           "Every completed declared case satisfies H_reset; this finite search is not a proof."),
        "limitations": ["The ordered H_reset search is limited to p=2,4,6,8,10,12,14 and r=1..6; the separate targeted test has exactly four p=30,r=6 inputs.",
                        "The search concerns normalized cyclic portal stacks generated by the existing analyzer.",
                        "No original endpoint traversal or exhaustive p=30 search was run.",
                        "Finite survival is not proof of H_reset or H_Y."],
    }
    if time.monotonic() - START > WALL_CAP:
        record["status"] = "partial-finite-inconclusive"
        record["result_summary"]["stopped_early"] = {"reason": "wall cap reached before atomic result write"}
    atomic_json(OUT, record)
    print(json.dumps({"status": record["status"], "runtime_seconds": elapsed,
                      "completed_scope_count": len(completed_scopes),
                      "drivers_checked": total_checked, "trigger_phases_tested": total_trigger,
                      "witness_id": ({"p": witness["p"], "r": witness["r"],
                                      "w": witness["w_integer_lsb"], "s": witness["phase_s"]}
                                     if witness else None),
                      "triple_status": targeted["status"] if targeted else None,
                      "result": str(OUT), "result_sha256": sha(OUT.read_bytes())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--targeted-only"]:
        raise SystemExit(targeted_only())
    if sys.argv[1:]:
        raise SystemExit("usage: check_hidden_label_reset_criterion.py [--targeted-only]")
    raise SystemExit(main())
