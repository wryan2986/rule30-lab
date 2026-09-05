#!/usr/bin/env python3
"""Independent oracle tests: hand-derived vectors, seam cases, cross-checks."""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from check_three_return_signed_mass_independent import (  # noqa: E402
    admissible,
    all_gap_triples,
    belief_direct,
    belief_recursive,
    build_frontiers,
    build_multiplicities,
    fiber,
    forced_zero_schedule,
    gen_p,
    gen_t,
    gen_t_bitwise,
    gen_u,
    return_extension,
    signed_mass,
    status_for,
    sweep,
    validate_caps,
)


def test_generators_hand_derived():
    # t(1) = 1 ^ ((1<<1)|(1<<2)) = 1^6 = 7; u(1) = 6
    assert gen_t(1) == 7
    assert gen_u(1) == 6
    # t(3) = 3^(6|12) = 3^14 = 13; 3 odd so p(3) = u(3) = 12
    assert gen_t(3) == 13
    assert gen_u(3) == 12
    assert gen_p(3) == 12
    # 6 even: p(6) = t(6)^1^2; t(6) = 6^(12|24) = 6^28 = 26
    assert gen_t(6) == 26
    assert gen_p(6) == 26 ^ 1 ^ 2


def test_frontiers_hand_derived():
    fu = build_frontiers("u", 3)
    assert fu[1] == {1}
    assert fu[2] == {6, 7}
    assert fu[3] == {24, 25, 26, 27}
    fp = build_frontiers("p", 2)
    assert fp[1] == {3}
    assert fp[2] == {12, 13}


def test_schedule_hand_derived():
    # 7 mod 16 == 7 -> u; p((7-3)>>2)=p(1)=6; u(6)=27; 27 mod 16==11 -> t;
    # then 111 mod 16 == 15 -> stop. schedule == "ut".
    assert forced_zero_schedule(7) == "ut"


def test_fibers_hand_derived():
    fu = build_frontiers("u", 3)
    assert fiber(fu, 1, 1) == frozenset((2, 3))
    assert fiber(fu, 2, 6) == frozenset((0, 1, 2, 3))
    # Children of 7 are t(7)=25, u(7)=24, both lifts of quotient 6, so the
    # fiber above quotient 7 itself is empty (mask 0000 is in the alphabet).
    assert fiber(fu, 2, 7) == frozenset()


def test_admissible_triple_count_is_56():
    n = sum(
        1 for g in all_gap_triples() if admissible(return_extension(g, True))
    )
    assert n == 56


def test_known_depth_one_cancellation_reproduced():
    # Derivative note: phase u, 0x198, complexity 5, depth 1 has cost0:1,
    # cost1:1 hence P(-1)=0. Not a three-return occurrence; oracle check only.
    fu = build_frontiers("u", 5)
    assert 408 in fu[5]
    bh: list = []
    b1 = belief_direct(fu, 5, 408, 1, bh)
    assert Counter(b1.values()) == Counter({0: 1, 1: 1})
    assert signed_mass(b1) == 0
    assert belief_recursive(fu, 5, 408, 1, bh) == b1


def test_oracles_agree_on_small_frontiers():
    for a in ("p", "u"):
        fr = build_frontiers(a, 6)
        for k in range(2, 7):
            for x in sorted(fr[k]):
                if x & 3 != 3:
                    continue
                for depth in range(1, k):
                    bh: list = []
                    assert belief_direct(fr, k, x, depth, bh) == belief_recursive(
                        fr, k, x, depth, bh
                    )


def test_level_zero_boundary_permitted():
    # Recursive formulation permits the level-0 quotient: fiber(0) at level 0
    # is exactly the seed-digit set {3} (phase p) / {1} (phase u).
    for a, seed in (("p", 3), ("u", 1)):
        fr = build_frontiers(a, 2)
        assert fiber(fr, 0, 0) == frozenset((seed,))
    # A strict-0000-at-level-0 variant would instead reject; the direct
    # definition used here keeps the permitted seed-digit mask.


def test_dedup_matches_distinct_frontier_sets():
    # Frontier sets already hold distinct integers; multiplicities only used
    # for the sensitivity comparison.
    for a in ("p", "u"):
        fr = build_frontiers(a, 6)
        mults = build_multiplicities(a, 6)
        for k in range(1, 7):
            assert set(mults[k]) == fr[k]


def test_bitwise_oracle_agrees_with_packed_generator():
    # Independent bit-by-bit Boolean rule vs packed shift formula.
    for x in list(range(1, 3000)) + [2**40 + 1, 2**63 - 1]:
        assert gen_t_bitwise(x) == gen_t(x)


def test_cap_validation_fail_closed():
    for bad_k in (0, 1, 17, 100, -3):
        try:
            validate_caps(bad_k, 120.0)
        except ValueError:
            pass
        else:
            raise AssertionError(f"max_k={bad_k} accepted")
    for bad_w in (0, -1.0, 120.5, 1000.0):
        try:
            validate_caps(16, bad_w)
        except ValueError:
            pass
        else:
            raise AssertionError(f"wall={bad_w} accepted")
    validate_caps(2, 120.0)
    validate_caps(16, 0.5)


def test_status_mapping_incomplete_is_inconclusive():
    assert status_for("exhausted", None, 0) == "finite-exhaustive"
    assert status_for("wall-limit", None, 0) == "inconclusive"
    assert status_for("exhausted", None, 1) == "inconclusive"
    assert status_for("separation-violation", None, 0) == "inconclusive"
    assert status_for("exhausted", {"mass": 0}, 0) == "refuted"
    assert status_for("first-zero", {"mass": 0}, 0) == "refuted"


def test_forced_tiny_deadline_reports_inconclusive():
    res = sweep(max_k=16, wall_limit=1e-9)
    assert res["stop_reason"] == "wall-limit"
    assert res["status"] == "inconclusive"


def test_separation_lemma_finite_check_both_phases():
    # Direct-set attempt to refute the parent separation lemma through k=8:
    # no x in O_(a,k) shares mod-4^(k-1) residue with any y in O_(a,k-1).
    # Base k=2 pins the top digits: p {0,1} vs 3; u {2,3} vs 1.
    for a, seed_digit, cur_digits in (("p", 3, {0, 1}), ("u", 1, {2, 3})):
        fr = build_frontiers(a, 8)
        assert set(fr[1]) == ({3} if a == "p" else {1})
        x2 = sorted(fr[2])
        assert {s & 3 for s in x2} == cur_digits
        for y in fr[1]:
            assert y == seed_digit
            for x in x2:
                assert x % 4 != y % 4
        for k in range(2, 9):
            mod = 4 ** (k - 1)
            shadow_residues = {y % mod for y in fr[k - 1]}
            for x in fr[k]:
                assert x % mod not in shadow_residues, (a, k, x)


def test_projection_theorem_finite_check():
    for a in ("p", "u"):
        fr = build_frontiers(a, 8)
        for k in range(2, 9):
            for s in fr[k]:
                assert (s >> 2) in fr[k - 1], (a, k, s)


def test_empty_same_cylinder_at_boundary_depths():
    # Direct residue scans (no lemma assumed): at L=k-1 and L=k the
    # same-cylinder set {y in O_(a,k-1): y = x mod 4^L} is empty, through k=6.
    for a in ("p", "u"):
        fr = build_frontiers(a, 6)
        for k in range(2, 7):
            for x in fr[k]:
                for depth in (k - 1, k):
                    mod = 4**depth
                    residue = x & (mod - 1)
                    witnesses = [
                        y for y in fr[k - 1] if (y & (mod - 1)) == residue
                    ]
                    assert witnesses == [], (a, k, hex(x), depth)


def test_sweep_prose_consistency_full_box():
    # Instance = (k,a,x,c,g); mass list length must equal instance count;
    # regenerates the multiplicity prose from the actual array.
    res = sweep(max_k=16, wall_limit=120.0)
    assert res["stop_reason"] == "exhausted"
    assert res["truncated_schedules"] == 0
    assert len(res["mass_values_sorted"]) == res["instances"] == 19
    assert res["mass_values_sorted"] == sorted(res["mass_values_sorted"])
    from collections import Counter as _Counter

    counts = _Counter(res["mass_values_sorted"])
    assert sum(counts.values()) == 19
    assert counts[1650] == 2  # prose must say twice, not thrice
    assert counts[579] == 3
    # Every evaluated occurrence is in-domain; outside rows are L>=k only.
    for row in res["occurrences"]:
        assert row["depth"] < row["complexity"]
    for row in res["outside_domain_rows"]:
        assert row["depth"] >= row["complexity"]
    # Sign-flip control witness recorded exactly, if the claim is retained.
    if res["weighted_zero_or_signflip"]:
        assert res["sign_flip_witness"] is not None

