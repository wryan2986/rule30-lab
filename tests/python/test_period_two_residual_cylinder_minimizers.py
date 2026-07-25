from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments/problem1_nonperiodicity/analyze_period_two_residual_cylinder_minimizers.py"
)
spec = spec_from_file_location("residual_cylinders", MODULE_PATH)
assert spec and spec.loader
m = module_from_spec(spec)
spec.loader.exec_module(m)


def setup_levels(cap=13):
    levels = {phase: m.build_phase_levels(phase, cap) for phase in m.PHASES}
    return levels, m.make_member(levels, cap)


def test_projection_factorization_matches_direct_small_frontiers():
    levels, member = setup_levels(8)
    assert m.exhaustive_small_check(levels, member) == 3608


def test_actual_survivor_residues_match_known_prefix():
    expected = [0x3, 0x7, 0x7, 0xC7, 0x2C7, 0x6C7]
    assert [m.survivor_for_word(m.actual_driver(d)) for d in range(1, 7)] == expected


def test_actual_depth_ten_phase_minima():
    levels, member = setup_levels(13)
    residue = m.survivor_for_word(m.actual_driver(10))
    p = m.cylinder_kappa(
        phase="p", depth=10, residue=residue, maximum_complexity=17,
        levels=levels, member=member,
    )
    u = m.cylinder_kappa(
        phase="u", depth=10, residue=residue, maximum_complexity=19,
        levels=levels, member=member,
    )
    assert p[0] == 17 and len(p[1]) == 1
    assert u[0] == 19 and len(u[1]) == 1


def test_actual_depth_twelve_funnel():
    levels, member = setup_levels(16)
    residue = m.survivor_for_word(m.actual_driver(12))
    states, funnel = m.cylinder_filter(
        phase="p", depth=12, complexity=28, residue=residue,
        levels=levels, member=member,
    )
    assert len(states) == 3
    assert funnel == [23751, 12249, 4962, 2391, 1291, 415, 157, 73, 36, 20, 9, 3, 3]


def test_counterexample_is_unique_in_all_three_cylinders():
    levels, member = setup_levels(13)
    for word in m.COUNTER_WORDS.values():
        states, _ = m.cylinder_filter(
            phase="u", depth=len(word), complexity=25,
            residue=m.survivor_for_word(word), levels=levels, member=member,
        )
        assert states == [m.KNOWN_COUNTEREXAMPLE]


def test_residual_complexity_cap_is_enforced():
    levels, member = setup_levels(4)
    try:
        m.cylinder_filter(
            phase="p", depth=2, complexity=7, residue=3,
            levels=levels, member=member,
        )
    except m.ResidualCylinderLimitError:
        pass
    else:
        raise AssertionError("expected residual cap error")


def test_default_campaign_certificate_and_boundary():
    payload = m.run_campaign()
    assert payload["certificate_sha256"] == "8fa73099c54206ed68e0e33028d9d2a4a381d7f6425544c539a887c82c23f087"
    assert len(payload["actual_rows"]) == 10
    assert "does not prove" in payload["scientific_boundary"]
