from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_canonical_relations.py"
)
SPEC = importlib.util.spec_from_file_location(
    "period_two_canonical_relations", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_conditional_relations() -> None:
    assert MODULE.verify_conditional_relations(1 << 10)["all_checks_pass"]


def test_known_rewrites() -> None:
    reduced, _ = MODULE.reduce_word(0, "ptup")
    assert reduced == "pttt"
    assert MODULE.apply_word(0, "ptup") == MODULE.apply_word(0, reduced)

    reduced, _ = MODULE.reduce_word(0, "uuut")
    assert reduced == "uutp"
    assert MODULE.apply_word(0, "uuut") == MODULE.apply_word(0, reduced)


def test_automaton_matrix_matches_direct_canonical_enumeration() -> None:
    for _, start in MODULE.PHASE_START.items():
        for length in range(1, 8):
            count = 0
            for suffix in itertools.product(MODULE.LETTERS, repeat=length - 1):
                if MODULE.is_canonical(start, "".join(suffix)):
                    count += 1
            assert count == MODULE.matrix_count(start, length - 1)


def test_every_small_word_reduces_to_canonical() -> None:
    assert MODULE.verify_reduction(7)["all_checks_pass"]


def test_arithmetic_counts_stay_below_canonical_bound() -> None:
    result = MODULE.verify_arithmetic_state_counts(12)
    assert result["all_checks_pass"]
    final = result["rows"][-1]
    assert (
        final["p"]["distinct_arithmetic_states"]
        < final["p"]["canonical_automaton_bound"]
    )
    assert (
        final["u"]["distinct_arithmetic_states"]
        < final["u"]["canonical_automaton_bound"]
    )


def test_certificate_stability() -> None:
    assert (
        MODULE.run_campaign(9, 18)["certificate_sha256"]
        == "713a91dd3a69fbbcbcbfd946bbaba3a15e61c55e80d034ca7e4799fad98300a0"
    )
