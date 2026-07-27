from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments/problem1_nonperiodicity/analyze_period_two_dominant_shadow_transducer.py"
)
spec = spec_from_file_location("dominant_shadows", MODULE_PATH)
assert spec and spec.loader
m = module_from_spec(spec)
spec.loader.exec_module(m)


def test_three_return_pattern_count():
    assert len(m.three_return_patterns()) == 56


def test_fiber_alphabet_on_small_frontiers():
    for phase in m.PHASES:
        levels = m.build_levels(phase, 9)
        for complexity in range(1, 8):
            for quotient in levels[complexity]:
                assert m.fiber_mask(levels, complexity, quotient) in m.ALLOWED_MASKS


def test_mask_containment_is_common_digit_simulation():
    for current in m.ALLOWED_MASKS:
        for shadow in m.ALLOWED_MASKS:
            if current & ~shadow:
                continue
            for digit in range(4):
                if (current >> digit) & 1:
                    assert (shadow >> digit) & 1


def test_default_positive_cut_occurrences_have_dominant_shadows():
    payload = m.run_campaign(16)
    assert payload["combined"]["positive_cut_occurrences"] == 5
    assert payload["combined"].get("violations", 0) == 0


def test_default_campaign_certificate():
    payload = m.run_campaign()
    assert payload["certificate_sha256"] == (
        "fcfe33d05d2071f0e5971df1cdd1ac4c90dae42c7485f9ce5aaab6aaf1f04a86"
    )
    assert payload["combined"]["occurrences"] == 19


def test_full_controlled_campaign_certificate():
    payload = m.run_campaign(20)
    assert payload["certificate_sha256"] == (
        "65c431803e07785a47a1851f3cb51358ffd8566ce5af46b6f4117adb705c3889"
    )
    assert payload["combined"]["occurrences"] == 210
    assert payload["combined"].get("violations", 0) == 0


def test_default_pair_alphabet_and_boundary():
    payload = m.run_campaign()
    assert payload["observed_pair_alphabet"] == [
        "0b1011/0b1011",
        "0b1011/0b1111",
        "0b1100/0b1100",
        "0b1100/0b1111",
        "0b1111/0b1111",
    ]
    assert "does not prove" in payload["scientific_boundary"]
