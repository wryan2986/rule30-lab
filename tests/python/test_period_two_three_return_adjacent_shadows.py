from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments/problem1_nonperiodicity/analyze_period_two_three_return_adjacent_shadows.py"
)
spec = spec_from_file_location("adjacent_shadows", MODULE_PATH)
assert spec and spec.loader
m = module_from_spec(spec)
spec.loader.exec_module(m)


@lru_cache(maxsize=None)
def campaign(maximum_complexity: int):
    return m.run_campaign(maximum_complexity)


def test_admissible_three_return_pattern_count():
    patterns = m.three_return_patterns()
    assert len(patterns) == 56
    assert all(m.admissible(complete) for _, _, complete in patterns)
    assert all(
        not (gaps[0] == 2 and gaps[1] == 3)
        for gaps, _, _ in patterns
    )


def test_known_positive_cut_schedule():
    assert m.forced_zero_schedule(0x6F65C387) == "utututut"


def test_phase_p_default_shadow_counts():
    totals = campaign(16)["phases"]["p"]["totals"]
    assert totals["occurrences"] == 8
    assert totals["shadowed_occurrences"] == 8
    assert totals["violations"] == 0
    assert totals["positive_cut_occurrences"] == 1


def test_phase_u_default_shadow_counts():
    totals = campaign(16)["phases"]["u"]["totals"]
    assert totals["occurrences"] == 11
    assert totals["shadowed_occurrences"] == 11
    assert totals["violations"] == 0
    assert totals["positive_cut_occurrences"] == 4


def test_default_certificate_and_combined_counts():
    payload = campaign(16)
    assert payload["certificate_sha256"] == (
        "66675662be4c8a43ca13eb0995549c0596819c3aba9d7693fbc8df121cea36f9"
    )
    assert payload["combined"]["occurrences"] == 19
    assert payload["combined"]["positive_cut_occurrences"] == 5
    assert payload["combined"]["violations"] == 0


def test_full_controlled_certificate():
    payload = campaign(20)
    assert payload["certificate_sha256"] == (
        "05b8559842204a24e94595b39fa03dc2a5806295ad1756712d35130285056324"
    )
    assert payload["combined"]["occurrences"] == 210
    assert payload["combined"]["positive_cut_occurrences"] == 58
    assert payload["combined"]["violations"] == 0


def test_limits_and_scientific_boundary():
    try:
        m.run_campaign(21)
    except m.ShadowCampaignLimitError:
        pass
    else:
        raise AssertionError("expected controlled complexity cap")
    assert "does not yet prove" in campaign(16)["scientific_boundary"]
