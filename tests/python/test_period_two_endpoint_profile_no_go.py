from __future__ import annotations

import importlib.util
from collections import defaultdict
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_endpoint_profile_no_go.py"
)
SPEC = importlib.util.spec_from_file_location("endpoint_profile_no_go", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


@pytest.fixture(scope="module")
def levels() -> list[set[int]]:
    return module.build_levels(module.DEFAULT_MAXIMUM_COMPLEXITY)


def test_frontier_generators_match_known_phase_u_levels() -> None:
    built = module.build_levels(3)
    assert built[1] == {1}
    assert built[2] == {6, 7}
    assert built[3] == {24, 25, 26, 27}


def test_fibers_stay_in_the_five_mask_alphabet(levels: list[set[int]]) -> None:
    observed = {
        module.fiber_mask(levels, complexity, state)
        for complexity in range(1, 10)
        for state in levels[complexity]
    }
    assert observed <= set(module.ALLOWED_MASKS)
    assert {0b0011, 0b1011, 0b1100, 0b1111} <= observed


def test_endpoint_profile_distinguishes_absence_from_present_zero(
    levels: list[set[int]],
) -> None:
    profile = module.endpoint_profile(levels, 20, 0x6F34E870DB)
    assert profile == (0b1011, (0b0000, 0b0000, None, 0b0000))


def test_paired_profile_is_exact_for_one_digit_small(
    levels: list[set[int]],
) -> None:
    for complexity in range(3, 9):
        groups: dict[object, list[tuple[int, int]]] = defaultdict(list)
        for current in levels[complexity]:
            for shadow in levels[complexity - 1]:
                if module.synchronized_or_full_pair(
                    levels, complexity, current, shadow
                ):
                    key = (
                        module.endpoint_profile(levels, complexity, current),
                        module.endpoint_profile(
                            levels, complexity - 1, shadow
                        ),
                    )
                    groups[key].append((current, shadow))
        for pairs in groups.values():
            summaries = {
                module.one_digit_type_summary(
                    levels, complexity, current, shadow
                )
                for current, shadow in pairs
            }
            assert len(summaries) == 1


def test_explicit_pairs_have_the_same_one_step_profile(
    levels: list[set[int]],
) -> None:
    good = module.endpoint_profile(
        levels, module.CURRENT_COMPLEXITY - 1, module.GOOD_SHADOW
    )
    bad = module.endpoint_profile(
        levels, module.CURRENT_COMPLEXITY - 1, module.BAD_SHADOW
    )
    assert good == bad == (0b1111, (0b1111,) * 4)
    assert module.synchronized_or_full_pair(
        levels, module.CURRENT_COMPLEXITY, module.CURRENT, module.GOOD_SHADOW
    )
    assert module.synchronized_or_full_pair(
        levels, module.CURRENT_COMPLEXITY, module.CURRENT, module.BAD_SHADOW
    )


def test_word_30_has_different_concrete_continuation_languages(
    levels: list[set[int]],
) -> None:
    good = module.follow_word(
        levels,
        module.CURRENT_COMPLEXITY,
        module.CURRENT,
        module.GOOD_SHADOW,
        module.CONTINUATION_WORD,
    )
    bad = module.follow_word(
        levels,
        module.CURRENT_COMPLEXITY,
        module.CURRENT,
        module.BAD_SHADOW,
        module.CONTINUATION_WORD,
    )
    assert good is not None
    assert good[-1] == (0x1BCD3A1C36C, 0x642E240C2C)
    assert bad is None
    bad_steps = module.pair_step_details(
        levels,
        module.CURRENT_COMPLEXITY,
        module.CURRENT,
        module.BAD_SHADOW,
        module.CONTINUATION_WORD,
    )
    assert bad_steps[-1]["current_mask"] == "0000"
    assert bad_steps[-1]["shadow_mask"] == "1011"
    assert bad_steps[-1]["dominant"]
    assert not bad_steps[-1]["synchronized_or_full"]


def test_default_campaign_certificate() -> None:
    payload = module.run_campaign()
    assert payload["outputs_built"] == 1_444_495
    assert payload["obstruction"]["profiles_equal"]
    assert payload["obstruction"]["one_digit_summaries_equal"]
    assert payload["certificate_sha256"] == (
        "4434461668a668758e7f5f4744824bd530a77aafe423d97d415e175b5beb2d67"
    )
