from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_schedule_survivor.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_schedule_survivor", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

QUOTIENT_SCRIPT = (
    ROOT
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_quotient.py"
)
QUOTIENT_SPEC = importlib.util.spec_from_file_location(
    "period_two_quotient_schedule_crosscheck", QUOTIENT_SCRIPT
)
assert QUOTIENT_SPEC is not None and QUOTIENT_SPEC.loader is not None
quotient = importlib.util.module_from_spec(QUOTIENT_SPEC)
QUOTIENT_SPEC.loader.exec_module(quotient)


def _v2(value: int) -> int:
    if value == 0:
        return 10_000
    return (value & -value).bit_length() - 1


def _forward_zero_step(q_name: str, x_value: int) -> int:
    assert x_value % 4 == 3
    return module.forward_generator(
        q_name,
        module.forward_generator("p", x_value >> 2),
    )


def test_inverse_generators_round_trip_all_small_quotients() -> None:
    for width in range(1, 11):
        mask = (1 << width) - 1
        for state in range(1 << width):
            for name in module.LETTERS:
                output = module.forward_generator(name, state) & mask
                assert module.inverse_generator_mod(name, output, width) == state


def test_backward_branch_is_exact_inverse_and_contraction() -> None:
    for width in range(6, 18, 2):
        inner_mask = (1 << (width - 2)) - 1
        for q_name in ("t", "u"):
            for successor in range(min(1 << (width - 2), 256)):
                current = module.backward_zero_branch(q_name, successor, width)
                assert current % 4 == 3
                assert _forward_zero_step(q_name, current) & inner_mask == successor

            for left in range(32):
                for right in range(32):
                    current_left = module.backward_zero_branch(q_name, left, width)
                    current_right = module.backward_zero_branch(q_name, right, width)
                    expected = min(_v2(left - right) + 2, width)
                    actual = module.valuation_mod_difference(
                        current_left, current_right, width
                    )
                    assert actual == expected


def test_schedule_survivor_cocycle_is_consistent_on_quotients() -> None:
    schedules = (
        ("t",) * 16,
        ("u",) * 16,
        tuple("tututtuutttuutut"),
    )
    for q_names in schedules:
        for width in range(8, 30, 2):
            current = module.schedule_survivor_residue(q_names, width)
            successor = module.schedule_survivor_residue(q_names[1:], width - 2)
            assert (
                _forward_zero_step(q_names[0], current)
                & ((1 << (width - 2)) - 1)
            ) == successor
            assert current % 16 == (11 if q_names[0] == "t" else 7)


def test_pair_transducer_matches_backward_contraction_for_all_short_schedules() -> None:
    from itertools import product

    for pair_count in range(2, 9):
        for q_names in product(("t", "u"), repeat=pair_count):
            pairs, _ = module.survivor_output_pairs(q_names, pair_count)
            pair_value = module.pairs_to_integer(pairs)
            direct_value = module.schedule_survivor_residue(
                q_names, 2 * pair_count
            )
            assert pair_value == direct_value


def test_word_and_fringe_implementations_match_existing_oracle() -> None:
    heads, q_names = module.fringe_schedule(256)
    quotient_heads, quotient_pairs = quotient.fringe_driver(256)
    assert heads == quotient_heads
    assert q_names == ["u" if head == "T" else "t" for head in quotient_heads]
    assert len(quotient_pairs) == 257

    word: tuple[str, ...] = ()
    for block in range(128):
        assert module.emitted_block(word) == quotient._emitted_block(word)
        assert module.inverse_word_preimage_zero(
            module.normalize_word(word)
        ) == quotient.inverse_word_preimage_zero(module.normalize_word(word))
        word = module.block_update(word, q_names[block])


def test_synthetic_mismatch_valuation_gives_exact_zero_streak() -> None:
    q_names = tuple("utttututtuutttut" * 8)
    width = 128
    survivor = module.schedule_survivor_residue(q_names, width)

    for valuation in range(0, 31):
        current = survivor ^ (1 << valuation)
        streak = 0
        for q_name in q_names:
            if current % 4 != 3:
                break
            streak += 1
            current = _forward_zero_step(q_name, current)
        assert streak == valuation // 2


def test_actual_path_mismatch_law_and_pair_stream_regression() -> None:
    result = module.run_campaign(
        actual_blocks=512,
        survivor_width=128,
        pair_count=128,
    )
    assert result["certificate_sha256"] == (
        "01a1eed537d527aedaa3ecfda58a7868ad288ea7dcad074e7524201735f25942"
    )

    mismatch = result["actual_mismatch_law"]
    assert mismatch["all_streak_valuation_checks_pass"] is True
    assert mismatch["maximum_consecutive_zero_blocks"] == 3
    assert mismatch["maximum_mismatch_valuation"] == 7
    assert mismatch["streak_counts"] == {
        "0": 406,
        "1": 86,
        "2": 19,
        "3": 2,
    }

    inverse_lift = result["alternating_inverse_lift_identity"]
    assert inverse_lift["shift_zero_equals_inverse_diagonal_lift"] is True
    assert inverse_lift["all_selected_moving_tail_identities_pass"] is True
    assert inverse_lift["inverse_lift_residue_sha256"] == (
        "df14d046ac29d7708712a77daa173bd89542e3c6fc7765530aa0dd86ee74be91"
    )

    transducer = result["schedule_survivor_pair_transducer"]
    assert transducer["direct_backward_contraction_matches"] is True
    assert transducer["nonzero_pairs_observed"] == 103
    assert transducer["longest_zero_pair_run_observed"] == 2
    assert transducer["pair_stream_sha256"] == (
        "f854d84e6227989f44dc4646793401802017194a5498ee02b05d84c3484be289"
    )


def test_campaign_limits_fail_closed() -> None:
    with pytest.raises(module.ScheduleSurvivorLimitError, match="actual blocks"):
        module.run_campaign(actual_blocks=4_097)
    with pytest.raises(module.ScheduleSurvivorLimitError, match="survivor width"):
        module.run_campaign(survivor_width=1_026)
    with pytest.raises(module.ScheduleSurvivorLimitError, match="pair count"):
        module.run_campaign(pair_count=513)
    with pytest.raises(ValueError, match="even integer"):
        module.run_campaign(survivor_width=127)


def test_script_emits_scoped_json() -> None:
    completed = subprocess.run(
        (
            sys.executable,
            str(SCRIPT),
            "--actual-blocks",
            "128",
            "--survivor-width",
            "64",
            "--pair-count",
            "64",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == "problem1-period-two-schedule-survivor-v1"
    assert payload["status"] == "finite-exhaustive"
    assert len(payload["result_summary"]["certificate_sha256"]) == 64
    assert any(
        "does not exclude eventual center period two" in limitation
        for limitation in payload["limitations"]
    )
