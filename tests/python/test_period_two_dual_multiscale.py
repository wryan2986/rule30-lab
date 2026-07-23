from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_dual_multiscale.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_dual_multiscale", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_exact_root_permutations_and_sections() -> None:
    assert MODULE.root_permutation("u") == (3, 2, 0, 1)
    assert MODULE.generator_sections("t") == ("t", "p", "p", "u")
    assert MODULE.generator_sections("p") == ("p", "u", "p", "t")
    assert MODULE.generator_sections("u") == ("p", "u", "t", "p")


def test_self_replication_witnesses() -> None:
    result = MODULE.verify_self_replication_witnesses()
    witnesses = result["stabilizer_section_witnesses"]
    assert witnesses["t"]["word"] == "t"
    assert witnesses["p"]["word"] == "ppT"
    assert witnesses["u"]["word"] == "tPttP"
    assert result["all_checks_pass"] is True


def test_all_checked_level_orbits_are_full() -> None:
    result = MODULE.verify_level_orbits(8)
    assert result["orbit_sizes"] == {
        str(depth): 4**depth for depth in range(1, 9)
    }


def test_pair_orbit_pattern_through_depth_four() -> None:
    result = MODULE.verify_pair_orbits(4)
    assert [result["levels"][str(depth)]["ordered_pair_orbits"] for depth in range(1, 5)] == [2, 4, 6, 8]
    assert all(
        result["levels"][str(depth)]["all_orbits_root_separating"]
        for depth in range(1, 5)
    )


def test_actual_block_32_has_maximal_sections_through_depth_eight() -> None:
    result = MODULE.verify_actual_section_growth(8)
    block = result["blocks"]["32"]
    assert block["word_length"] == 64
    assert block["section_orbit_sizes"] == [4**depth for depth in range(1, 9)]
    assert block["full_through_depth"] == 8


def test_campaign_certificate_is_stable() -> None:
    result = MODULE.run_campaign(8)
    assert result["certificate_sha256"] == "0efa9c6f8d8a8252adfc4cf67e681e19f9c52449cc74ba14a8119db29e3948c4"
