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
    / "analyze_period_two_renewal.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_renewal", SCRIPT)
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
    "period_two_quotient_crosscheck", QUOTIENT_SCRIPT
)
assert QUOTIENT_SPEC is not None and QUOTIENT_SPEC.loader is not None
quotient = importlib.util.module_from_spec(QUOTIENT_SPEC)
QUOTIENT_SPEC.loader.exec_module(quotient)


EXPECTED_TRANSDUCER = [
    {"state": [0, 0], "input": "t", "output": "t", "next_state": [0, 0]},
    {"state": [0, 0], "input": "p", "output": "p", "next_state": [1, 1]},
    {"state": [0, 0], "input": "u", "output": "p", "next_state": [1, 1]},
    {"state": [0, 1], "input": "t", "output": "p", "next_state": [0, 1]},
    {"state": [0, 1], "input": "p", "output": "u", "next_state": [1, 0]},
    {"state": [0, 1], "input": "u", "output": "u", "next_state": [1, 0]},
    {"state": [1, 0], "input": "t", "output": "p", "next_state": [1, 1]},
    {"state": [1, 0], "input": "p", "output": "p", "next_state": [0, 1]},
    {"state": [1, 0], "input": "u", "output": "t", "next_state": [0, 0]},
    {"state": [1, 1], "input": "t", "output": "u", "next_state": [1, 0]},
    {"state": [1, 1], "input": "p", "output": "t", "next_state": [0, 0]},
    {"state": [1, 1], "input": "u", "output": "p", "next_state": [0, 1]},
]


def test_independent_word_implementation_matches_existing_oracle() -> None:
    from itertools import product

    for length in range(0, 6):
        for word in product(module.LETTERS, repeat=length):
            assert module.inverse_word_root(word, 0) == quotient._inverse_word_root(
                word, 0
            )
            assert module.inverse_word_section(
                word, 1
            ) == quotient._inverse_word_section(word, 1)
            assert module.section_along(word, (1, 1)) == quotient._section_along(
                word, (1, 1)
            )
            assert module.emitted_block(word) == quotient._emitted_block(word)
            assert module.inverse_word_preimage_zero(
                word
            ) == quotient.inverse_word_preimage_zero(word)


def test_combined_section_transducer_table_is_exact() -> None:
    assert module.combined_section_table() == EXPECTED_TRANSDUCER


def test_all_words_through_length_eight_obey_both_reductions() -> None:
    result = module.verify_word_reductions(8)
    assert result["non_all_t_words_checked"] == 9_832
    assert result["renewal_q_branches_checked"] == 19_664
    assert result["zero_emission_integer_q_branches_checked"] > 0
    assert result["all_checks_pass"] is True


def test_integer_continuation_table_has_two_unique_branches() -> None:
    assert module.continuation_table() == [
        {
            "x_mod_16": 3,
            "x_shifted_mod_4": 0,
            "successor_mod_4": {"t": 1, "u": 0},
            "zero_continuation_q": None,
        },
        {
            "x_mod_16": 7,
            "x_shifted_mod_4": 1,
            "successor_mod_4": {"t": 2, "u": 3},
            "zero_continuation_q": "u",
        },
        {
            "x_mod_16": 11,
            "x_shifted_mod_4": 2,
            "successor_mod_4": {"t": 3, "u": 2},
            "zero_continuation_q": "t",
        },
        {
            "x_mod_16": 15,
            "x_shifted_mod_4": 3,
            "successor_mod_4": {"t": 0, "u": 1},
            "zero_continuation_q": None,
        },
    ]
    assert module.forced_zero_step(7) == (
        "u",
        module.forward_generator("u", module.forward_generator("p", 1)),
    )
    assert module.forced_zero_step(11) == (
        "t",
        module.forward_generator("t", module.forward_generator("p", 2)),
    )
    assert module.forced_zero_step(3) is None
    assert module.forced_zero_step(15) is None


def test_tail_forms_of_integer_recurrence_are_exact() -> None:
    for z_value in range(1_024):
        branch_u = module.forward_generator(
            "u", module.forward_generator("p", (16 * z_value + 7) >> 2)
        )
        assert branch_u == 4 * module.forward_generator(
            "p", module.forward_generator("u", z_value)
        ) + 3
        assert branch_u.bit_length() == (16 * z_value + 7).bit_length() + 2

        branch_t = module.forward_generator(
            "t", module.forward_generator("p", (16 * z_value + 11) >> 2)
        )
        assert branch_t == 4 * module.forward_generator(
            "u", module.forward_generator("p", z_value)
        ) + 3
        assert branch_t.bit_length() == (16 * z_value + 11).bit_length() + 2


def test_actual_path_refutes_a_leading_run_bound_of_two() -> None:
    result = module.actual_renewal_path(512)
    assert result["deficit_monotonicity_checked"] is True
    assert result["first_leading_run_above_two"] == {
        "block": 283,
        "leading_t_run": 3,
        "emitted_block": 2,
        "first_non_t": "u",
        "block_minus_leading_t_run": 280,
    }
    assert result["first_record_for_each_new_maximum"][:4] == [
        {
            "block": 0,
            "leading_t_run": 0,
            "emitted_block": 3,
            "first_non_t": None,
            "block_minus_leading_t_run": 0,
        },
        {
            "block": 3,
            "leading_t_run": 1,
            "emitted_block": 3,
            "first_non_t": "u",
            "block_minus_leading_t_run": 2,
        },
        {
            "block": 11,
            "leading_t_run": 2,
            "emitted_block": 3,
            "first_non_t": "u",
            "block_minus_leading_t_run": 9,
        },
        {
            "block": 283,
            "leading_t_run": 3,
            "emitted_block": 2,
            "first_non_t": "u",
            "block_minus_leading_t_run": 280,
        },
    ]


def test_campaign_limits_fail_closed() -> None:
    with pytest.raises(module.PeriodTwoRenewalLimitError, match="word length"):
        module.run_campaign(maximum_word_length=11)
    with pytest.raises(module.PeriodTwoRenewalLimitError, match="actual blocks"):
        module.run_campaign(actual_blocks=4_097)


def test_script_emits_strictly_scoped_json() -> None:
    completed = subprocess.run(
        (
            sys.executable,
            str(SCRIPT),
            "--maximum-word-length",
            "6",
            "--actual-blocks",
            "300",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == (
        "problem1-period-two-renewal-reduction-v1"
    )
    assert payload["status"] == "finite-exhaustive"
    assert len(payload["result_summary"]["certificate_sha256"]) == 64
    assert any(
        "does not exclude eventual center period two" in limitation
        for limitation in payload["limitations"]
    )
