from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_witness_complexity.py"
)
SPEC = spec_from_file_location("period_two_witness_complexity", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_actual_boundary_prefix_is_expected():
    driver = MODULE.actual_driver(4)
    assert driver == ("u", "t", "t", "t")
    assert MODULE.fresh_boundary_prefix(driver) == (
        "11",
        "10",
        "00",
        "11",
        "01",
    )


def test_reverse_witnesses_reach_target():
    depth = 4
    target = ("00",) * depth
    witnesses = MODULE.reverse_shortest_witnesses(depth, target)
    assert len(witnesses) == 4**depth
    for state, word in witnesses.items():
        assert MODULE.dual_image(word, state) == target


def test_phase_decomposition_gives_valid_witnesses():
    boundary = MODULE.fresh_boundary_prefix(("u", "t", "t"))
    row = MODULE.witness_row(4, boundary)
    assert row["minimum_normalized_length"] == 7
    assert row["by_phase"]["p"]["minimum_normalized_length"] == 8
    assert row["by_phase"]["u"]["minimum_normalized_length"] == 7


def test_actual_complexities_are_monotone_through_depth_five():
    result = MODULE.run_campaign(5)
    rows = result["actual_boundary_rows"]
    assert [row["minimum_normalized_length"] for row in rows] == [1, 2, 2, 7, 8]
    assert [
        row["by_phase"]["p"]["minimum_normalized_length"] for row in rows
    ] == [1, 3, 7, 8, 8]
    assert [
        row["by_phase"]["u"]["minimum_normalized_length"] for row in rows
    ] == [2, 2, 2, 7, 12]


def test_counting_bound_small_depths():
    checked = MODULE.verify_counting_bound(4)
    assert checked["all_checks_pass"] is True
    assert checked["checked_rows"][-1]["driver_prefixes"] == 8


def test_campaign_certificate_is_deterministic():
    first = MODULE.run_campaign(4)
    second = MODULE.run_campaign(4)
    assert first["certificate_sha256"] == second["certificate_sha256"]
