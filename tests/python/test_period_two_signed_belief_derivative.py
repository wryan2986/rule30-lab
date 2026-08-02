from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments/problem1_nonperiodicity/analyze_period_two_signed_belief_derivative.py"
)
SPEC = spec_from_file_location("signed_belief", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_local_derivative_identity():
    for current in MODULE.RELEVANT_CURRENT_MASKS:
        for shadow in MODULE.MASK_ALPHABET:
            assert MODULE.local_signed_factor(current, shadow) == (
                MODULE.local_branching_derivative(current, shadow)
            )


def test_controlled_campaign_nonvanishing():
    row = MODULE.run_campaign(16)
    assert row["gap_222_occurrences"] == 10
    assert row["dominant_failures"] == 0
    assert row["signed_zero_cylinders"] == 0


def test_controlled_campaign_derivative_agreement():
    row = MODULE.run_campaign(16)
    assert row["derivative_disagreements"] == 0
    assert row["synchronized_failures"] == 0


def test_nonzero_mass_certifies_nonempty_belief():
    row = MODULE.run_campaign(16)
    for example in row["examples"]:
        if example["signed_mass"]:
            assert example["dominant_shadows"] > 0


def test_nongap_cancellation_is_explicit():
    row = MODULE.run_campaign(16)
    cancellation = row["nongap_cancellation"]
    assert cancellation["signed_mass"] == 0
    assert cancellation["defect_histogram"] == {"0": 1, "1": 1}


def test_complexity_18_totals():
    row = MODULE.run_campaign(18)
    assert row["gap_222_occurrences"] == 26
    assert row["signed_zero_cylinders"] == 0
    assert row["minimum_absolute_signed_mass"] == 2


def test_limit_guard():
    try:
        MODULE.run_campaign(MODULE.ABSOLUTE_MAXIMUM_COMPLEXITY + 1)
    except MODULE.SignedBeliefLimitError:
        pass
    else:
        raise AssertionError("limit guard did not fire")
