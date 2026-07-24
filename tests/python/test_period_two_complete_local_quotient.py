from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_complete_local_quotient.py"
)
SPEC = importlib.util.spec_from_file_location("complete_local_quotient", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_generators_are_permutations_mod_64() -> None:
    inverses = MODULE.inverse_tables(64)
    for letter in MODULE.LETTERS:
        for state in range(64):
            image = MODULE.forward_generator(letter, state) & 63
            assert inverses[letter][image] == state


def test_complete_span_three_table() -> None:
    row = MODULE.verify_locality_tables(3)
    assert row["finite_table_checks"] == 1884
    assert row["nonminimal_entries"] == 1098
    assert row["all_checks_pass"] is True


def test_reduction_preserves_state_and_reaches_language() -> None:
    row = MODULE.verify_reduction(3, 7)
    assert row["words_checked"] == 2186
    assert row["words_changed"] > 0
    assert row["all_checks_pass"] is True


def test_span_roots_strictly_decrease() -> None:
    roots = [
        MODULE.CompleteLocalAutomaton(span).spectral_radius()
        for span in (1, 2, 3)
    ]
    assert roots[0] > roots[1] > roots[2]
    assert abs(roots[0] - (1 + 2**0.5)) < 1e-12
    assert abs(roots[2] - 2.0837007908733396) < 1e-12


def test_canonical_counts_bound_arithmetic_image() -> None:
    automaton = MODULE.CompleteLocalAutomaton(3)
    canonical = automaton.count_by_phase(12)
    arithmetic = MODULE.exact_arithmetic_counts(12)
    for left, right in zip(canonical, arithmetic, strict=True):
        assert right["p"] <= left["p"]
        assert right["u"] <= left["u"]


def test_default_certificate_is_deterministic() -> None:
    payload = MODULE.run_campaign()
    assert payload["reachable_automaton_states"] == 332
    assert payload["certificate_sha256"] == (
        "7cff92eabff299c41c71d1a5146ddcc330ae555684bfe22afa33e299edb194fd"
    )
