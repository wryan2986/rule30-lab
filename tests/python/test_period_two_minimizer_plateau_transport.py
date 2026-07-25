from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments/problem1_nonperiodicity/analyze_period_two_minimizer_plateau_transport.py"
)
spec = spec_from_file_location("plateau_transport", MODULE_PATH)
assert spec and spec.loader
m = module_from_spec(spec)
spec.loader.exec_module(m)


def setup_levels(cap=16):
    levels = {phase: m.build_levels(phase, cap) for phase in m.PHASES}
    return levels, m.make_member(levels, cap)


def test_return_extension_indexing():
    assert m.return_extension((2, 2), False) == "utut"
    assert m.return_extension((2, 2), True) == "ututu"
    assert m.return_extension((2, 2, 2), False) == "ututut"


def test_exhaustive_small_transport():
    levels, _ = setup_levels(8)
    assert m.exhaustive_transport(levels) == 4788


def test_known_counterexample_forced_schedule():
    assert m.forced_zero_schedule(m.KNOWN) == "tutututttutututt"
    assert not m.forced_zero_schedule(m.KNOWN).startswith(m.KNOWN_FINAL)


def test_known_counterexample_survives_exactly_two_returns():
    rows = []
    for old_word, new_word in (
        (m.KNOWN_BASE, m.KNOWN_MIDDLE),
        (m.KNOWN_MIDDLE, m.KNOWN_FINAL),
    ):
        rows.append(
            m.plateau_transport(
                [m.KNOWN],
                len(old_word),
                len(new_word),
                m.survivor_for_word(old_word),
                m.survivor_for_word(new_word),
            )
        )
    assert [row["survivor_count"] for row in rows] == [1, 1]


def test_actual_return_minimizers_all_die_through_depth_fourteen():
    levels, member = setup_levels(16)
    driver = m.actual_driver(20)
    depths = [
        index + 1
        for index, branch in enumerate(driver)
        if branch == "u" and index + 1 <= 14
    ]
    assert depths == [1, 5, 7, 12, 14]
    for old_depth, new_depth in zip(depths, depths[1:]):
        old_residue = m.survivor_for_word(driver[:old_depth])
        new_residue = m.survivor_for_word(driver[:new_depth])
        for phase in m.PHASES:
            states = m.cylinder_filter(
                phase,
                old_depth,
                m.EXPECTED[old_depth][phase],
                old_residue,
                levels,
                member,
            )
            row = m.plateau_transport(
                states,
                old_depth,
                new_depth,
                old_residue,
                new_residue,
            )
            assert row["survivor_count"] == 0


def test_python_frontier_census_through_sixteen():
    payload = m.frontier_plateau_census(16, 64)
    for phase in m.PHASES:
        assert payload[phase]["two_return_candidates"] == 0
        assert payload[phase]["three_return_candidates"] == 0


def test_default_campaign_certificate_and_boundary():
    payload = m.run_campaign()
    assert payload["certificate_sha256"] == (
        "5c4f5cb9aee833a4d698630643466e75fcc6806d258746baa5c4c81eaa7a26c1"
    )
    assert payload["known_counterexample"]["third_return_possible"] is False
    assert "does not prove" in payload["scientific_boundary"]
