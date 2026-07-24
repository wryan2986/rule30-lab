from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_phase_universality.py"
)
SPEC = importlib.util.spec_from_file_location("phase_universality", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_dual_generators_are_permutations() -> None:
    for depth in range(1, 5):
        for letter in MOD.LETTERS:
            states, permutation = MOD.generator_permutation(letter, depth)
            assert len(states) == 4**depth
            assert sorted(permutation) == list(range(4**depth))


def test_positive_monoid_reaches_zero_from_every_level_state() -> None:
    states, witnesses = MOD.positive_witnesses_to_zero(5)
    assert len(states) == len(witnesses) == 4**5
    target = ("00",) * 5
    for state, word in witnesses.items():
        assert MOD.dual_image(word, state) == target


def test_phase_padding_is_identity_at_selected_depth() -> None:
    depth = 5
    for phase in MOD.PHASES:
        states, permutation = MOD.generator_permutation(phase, depth)
        order = MOD.permutation_order(permutation)
        padding = phase * order
        for state in states:
            assert MOD.dual_image(padding, state) == state


def test_every_driver_has_both_phase_witnesses() -> None:
    result = MOD.verify_phase_padded_driver_universality(5)
    assert result["total_phase_padded_witnesses"] == 62
    for row in result["depths"]:
        expected = 2 ** row["driver_prefix_length"]
        assert row["driver_words_checked"] == expected
        assert row["witnesses_by_phase"] == {"p": expected, "u": expected}


def test_finite_depth_does_not_claim_one_infinite_witness() -> None:
    payload = MOD.run_campaign(3)
    assert "witness depends on the requested depth" in payload["scope_warning"]
    assert payload["exact_conclusions"]["finite_phase_universality"].startswith(
        "both fixed phases"
    )


def test_default_campaign_certificate() -> None:
    payload = MOD.run_campaign()
    assert payload["certificate_sha256"] == (
        "0cc889ae19213ffb06de8a1bf907761f5451b1111801ee07194ace498592193b"
    )
    assert payload["phase_padded_driver_universality"][
        "total_phase_padded_witnesses"
    ] == 254
