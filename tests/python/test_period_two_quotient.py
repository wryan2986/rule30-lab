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
    / "analyze_period_two_quotient.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_quotient", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_pair_transition_graph_is_exact_and_strongly_connected() -> None:
    graph = module.fringe_pair_graph()
    assert graph["assignments_exhausted"] == 16
    assert graph["adjacency"] == {
        "00": ["01", "11"],
        "01": ["10", "11"],
        "10": ["11"],
        "11": ["00", "10"],
    }
    assert graph["strongly_connected"] is True
    assert [
        (entry["source_pair"], entry["target_pair"])
        for entry in graph["explicit_directed_cycle"]
    ] == [
        ([0, 0], [0, 1]),
        ([0, 1], [1, 0]),
        ([1, 0], [1, 1]),
        ([1, 1], [0, 0]),
    ]


def test_fringe_formula_matches_two_direct_rule30_steps() -> None:
    for r1 in (0, 1):
        for r2 in (0, 1):
            for r3 in (0, 1):
                for r4 in (0, 1):
                    # Spatial indices 0..5 stand for d-4..d+1.  The
                    # alternating boundary forces x_d=x_(d+1)=1.
                    row = [r4, r3, r2, r1, 1, 1]
                    first = [
                        row[index]
                        ^ (
                            (row[index - 1] if index >= 1 else 0)
                            | (row[index - 2] if index >= 2 else 0)
                        )
                        for index in range(len(row))
                    ]
                    second = [
                        first[index]
                        ^ (
                            (first[index - 1] if index >= 1 else 0)
                            | (first[index - 2] if index >= 2 else 0)
                        )
                        for index in range(len(first))
                    ]
                    expected = (second[4], second[5])
                    assert module.fringe_pair_transition(
                        (r2, r1), (r3, r4)
                    ) == expected


def test_three_schedule_head_oracles_agree_before_schedule_cap() -> None:
    maximum_block = 12
    fringe_heads, fringe_pairs = module.fringe_driver(maximum_block)
    schedule_heads, periods = module.exact_schedule_heads(
        maximum_block, maximum_period=8_192
    )

    width = 64
    trace = module.minus_one_third_mod(width)
    seed = module.inverse_diagonal_map_mod(trace, width)
    row_heads, row_pairs = module.spacetime_driver(seed, width, maximum_block)

    assert fringe_heads == schedule_heads == row_heads
    assert fringe_pairs == row_pairs
    assert "".join(fringe_heads) == "TPUPTPTPPUPTP"
    assert periods == [1, 2, 4, 8, 32, 64, 64, 256, 256, 256, 512, 1_024, 2_048]


def test_default_campaign_refutes_both_named_candidates() -> None:
    result = module.run_campaign()

    assert result["all_finite_oracles_agree"] is True
    assert result["seven_block_schedule_head_candidate"]["first_mismatch"] == {
        "block": 153,
        "expected_head": "T",
        "actual_head": "P",
        "matched_blocks_before_mismatch": 151,
    }
    assert result["seven_block_schedule_head_candidate"][
        "pair_at_first_mismatch"
    ] == [1, 1]
    endpoint = result["dyadic_endpoint_parity_candidate"]
    assert endpoint["first_mismatch"] == {
        "exponent": 11,
        "position": 2_047,
        "bit": 0,
        "expected_exponent_parity": 1,
        "matches_candidate": False,
    }
    assert all(sample["matches_candidate"] for sample in endpoint["samples"][:10])
    assert result["fringe_schedule_identity"][
        "depth_two_portrait_transition_conflict"
    ] == {
        "portrait_word_order": [
            "epsilon",
            "0",
            "1",
            "00",
            "01",
            "10",
            "11",
        ],
        "head": "T",
        "portrait": [0, 1, 0, 0, 1, 0, 1],
        "first_block": 11,
        "first_current_emitted_block": 3,
        "first_next_emitted_block": 0,
        "conflicting_block": 55,
        "conflicting_current_emitted_block": 3,
        "conflicting_next_emitted_block": 2,
        "next_zero_status_differs": True,
    }
    assert result["alternating_lift"] == {
        "trace_residue": module.minus_one_third_mod(2_048),
        "inverse_seed_ones": 1_076,
        "inverse_seed_last_one_position": 2_046,
        "inverse_seed_sha256_little_endian_packed": (
            "279385743213d9b8b175fd080dbe07762652f5b3e3cf3a25386cd60e6a00da7c"
        ),
    }
    criterion = result["arithmetic_finite_support_criterion"]
    assert criterion["verified_blocks"] == 160
    assert criterion["maximum_leading_t_run_observed"] == 2
    assert criterion["all_leading_run_identities_pass"] is True
    assert len(result["certificate_sha256"]) == 64


def test_depth_two_portrait_conflict_is_reproduced_directly() -> None:
    heads, _ = module.fringe_driver(56)
    conflict = module.depth_two_portrait_conflict(heads)
    assert conflict is not None
    assert conflict["first_block"] == 11
    assert conflict["conflicting_block"] == 55
    assert conflict["first_next_emitted_block"] == 0
    assert conflict["conflicting_next_emitted_block"] == 2
    assert conflict["next_zero_status_differs"] is True


def test_arithmetic_support_criterion_matches_direct_word_actions() -> None:
    heads, _ = module.fringe_driver(32)
    seed = module.inverse_diagonal_map_mod(module.minus_one_third_mod(64), 64)
    criterion = module.arithmetic_support_criterion(seed, heads, 32)
    assert criterion["all_residual_word_preimage_identities_pass"] is True
    assert criterion["all_excess_degree_identities_pass"] is True
    assert criterion["all_leading_run_identities_pass"] is True
    assert criterion["maximum_leading_t_run_observed"] == 2
    assert criterion["selected_checkpoints"][-1] == {
        "block": 32,
        "highest_seed_one": 62,
        "preimage_zero_degree": 126,
        "excess_degree": 62,
        "leading_t_run": 0,
        "first_non_t": "u",
        "block_minus_leading_t_run": 32,
    }

    for name in ("t", "p", "u"):
        for state in range(16):
            width = max(8, state.bit_length() + 4)
            image = module.forward_generator(name, state)
            current_word = (name,)
            recovered = 0
            for position in range(width):
                bit = (image >> position) & 1
                recovered |= module._inverse_word_root(current_word, bit) << position
                current_word = module._inverse_word_section(current_word, bit)
            assert recovered == state


def test_campaign_limits_fail_closed() -> None:
    with pytest.raises(module.PeriodTwoQuotientLimitError, match="width"):
        module.run_campaign(width=4_097)
    with pytest.raises(module.PeriodTwoQuotientLimitError, match="maximum block"):
        module.run_campaign(driver_max_block=513)
    with pytest.raises(module.PeriodTwoQuotientLimitError, match="cross-check"):
        module.run_campaign(schedule_crosscheck_blocks=17)
    with pytest.raises(ValueError, match="twice"):
        module.run_campaign(width=64, driver_max_block=32)
    with pytest.raises(module.PeriodTwoQuotientLimitError, match="work"):
        module.run_campaign(maximum_work_points=10)
    with pytest.raises(module.PeriodTwoQuotientLimitError, match="schedule period"):
        module.run_campaign(
            width=64,
            driver_max_block=12,
            schedule_crosscheck_blocks=12,
            maximum_schedule_period=64,
        )


def test_script_emits_strictly_scoped_json() -> None:
    completed = subprocess.run(
        (
            sys.executable,
            str(SCRIPT),
            "--width",
            "64",
            "--driver-max-block",
            "20",
            "--schedule-crosscheck-blocks",
            "8",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == (
        "problem1-period-two-quotient-obstruction-v1"
    )
    assert payload["status"] == "finite-exhaustive"
    assert any(
        "do not exclude every period-two quotient" in limitation
        for limitation in payload["limitations"]
    )
