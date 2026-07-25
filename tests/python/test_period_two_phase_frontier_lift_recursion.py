import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "experiments/problem1_nonperiodicity/analyze_period_two_phase_frontier_lift_recursion.py"
spec = importlib.util.spec_from_file_location("lift_recursion", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def levels(phase: str, count: int):
    current = {mod.phase_start(phase)}
    rows = [current]
    for _ in range(1, count):
        current = {child for state in current for child in mod.frontier_children(state)}
        rows.append(current)
    return rows


def test_exact_partial_inverses_round_trip():
    for state in range(512):
        for name in "tup":
            output = mod.forward_generator(name, state)
            assert mod.inverse_generator(name, output) == state
    assert mod.inverse_generator("t", 1) is None


def test_parent_digit_contribution_masks():
    observed = {}
    for digit in range(4):
        parent = 4 * 37 + digit
        generator = "t" if digit == 0 else "u" if digit == 1 else "p"
        quotient = mod.forward_generator(generator, 37)
        child_digits = {
            mod.forward_generator(name, parent) & 3 for name in "tup"
        }
        mask = sum(1 << value for value in child_digits)
        assert mask == mod.CHILD_DIGIT_MASK[digit]
        for name in "tup":
            assert mod.forward_generator(name, parent) >> 2 == quotient
        observed[digit] = mask
    assert observed == {0: 0b1011, 1: 0b1100, 2: 0b1110, 3: 0b0011}


def test_recursive_membership_matches_small_exact_frontiers():
    mod.frontier_member.cache_clear()
    for phase in mod.PHASES:
        rows = levels(phase, 6)
        for complexity, frontier in enumerate(rows, start=1):
            width = mod.expected_bit_length(phase, complexity)
            for target in range(1 << (width - 1), 1 << width):
                assert mod.frontier_member(phase, complexity, target) == (
                    target in frontier
                )


def test_five_mask_alphabet_and_exact_prediction():
    for phase in mod.PHASES:
        rows = levels(phase, 11)
        seen = set()
        for current, next_level in zip(rows, rows[1:]):
            for quotient in current:
                predecessor, predicted = mod.predicted_fiber_mask(current, quotient)
                actual = mod.actual_fiber_mask(next_level, quotient)
                assert predicted == actual
                assert predicted in mod.ALLOWED_FIBER_MASKS
                assert not (predecessor & 0b0100 and not predecessor & 0b1000)
                seen.add(predicted)
        assert seen == set(mod.ALLOWED_FIBER_MASKS)


def test_strict_lift_examples():
    examples = mod.strict_examples()
    assert examples["phase_p"]["quotient"] == 12
    assert examples["phase_p"]["fiber_mask"] == "0b1100"
    assert examples["phase_p"]["lifts"] == [50, 51]
    assert examples["phase_u"]["quotient"] == 26
    assert examples["phase_u"]["fiber_mask"] == "0b1011"
    assert examples["phase_u"]["lifts"] == [104, 105, 107]


def test_known_counterexample_recursive_certificate():
    mod.frontier_member.cache_clear()
    mod.frontier_witness.cache_clear()
    assert mod.frontier_member("u", 25, mod.KNOWN_COUNTEREXAMPLE)
    word = mod.frontier_witness("u", 25, mod.KNOWN_COUNTEREXAMPLE)
    assert word == "uuuuttttutuptuputtputtpuu"
    assert len(word) == 25
    assert mod.apply_word(word) == mod.KNOWN_COUNTEREXAMPLE
    assert mod.frontier_member.cache_info().currsize == 767


def test_default_certificate_and_limit_guard():
    payload = mod.run_campaign(16)
    assert payload["certificate_sha256"] == (
        "0aa325f03d0e9f7c0640e7ca64d05a6f4e1c3db6558497ba7db7374d81f1319d"
    )
    assert payload["phases"]["p"]["outputs_checked"] == 52446
    assert payload["phases"]["u"]["outputs_checked"] == 43970
    try:
        mod.run_campaign(mod.ABSOLUTE_MAXIMUM_COMPLEXITY + 1)
    except mod.LiftRecursionLimitError:
        pass
    else:
        raise AssertionError("limit guard did not trigger")
