from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "problem1_nonperiodicity" / "analyze_period_two_return_residue_lifts.py"
spec = importlib.util.spec_from_file_location("return_lifts", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_return_gap_is_always_two_through_five_on_dependency_quotient() -> None:
    assert {module.return_outcome(z)[0] for z in range(1 << 16)} == {2, 3, 4, 5}


def test_bad_cylinder_classes_have_consecutive_gap_two() -> None:
    for residue in module.BAD_RESIDUES:
        gap, successor = module.return_outcome(residue)
        assert gap == 2
        assert module.return_outcome(successor)[0] == 2


def test_sixteen_bits_are_sufficient_and_lower_precisions_fail() -> None:
    result = module.precision_minimality(module.complete_outcomes())
    assert result["minimal"]
    assert result["sufficient_coordinate_bits"] == 16
    assert [row["bits"] for row in result["insufficient_precision_witnesses"]] == list(range(6, 16))


def test_observed_actual_residue_set_is_not_universally_closed() -> None:
    relation = module.transition_relation(module.complete_outcomes())
    rows = relation["observed_actual_residue_rows"]
    assert [4, 44] in rows["0"]
    assert [5, 28] in rows["63"]
    assert [5, 60] in rows["63"]


def test_universal_closure_reaches_every_bad_class() -> None:
    closure = module.universal_closure(module.complete_outcomes())
    assert closure["bad_residues_reached"] == [28, 44, 60]
    assert closure["closure_size"] == 25
    assert closure["first_bad_layer"] == 1


def test_campaign_certificate_is_stable() -> None:
    result = module.run_campaign()
    assert result["certificate_sha256"] == "0cebdaf943c77e8479198e07c98ab32e8a3b82e80013756cf5d7585fdfd69436"
