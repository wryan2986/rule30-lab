import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_renormalized_front.py"
)
spec = importlib.util.spec_from_file_location("renormalized_front", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_explicit_formula_matches_packed_map():
    for value in range(1, 1 << 12):
        assert module.renormalized_front(value) == module.renormalized_front_formula(value)


def test_inverse_is_two_sided_and_preserves_shells():
    for value in range(1, 1 << 12):
        image = module.renormalized_front(value)
        assert image.bit_length() == value.bit_length()
        assert module.inverse_renormalized_front(image) == value
        assert module.renormalized_front(module.inverse_renormalized_front(value)) == value


def test_each_small_shell_is_a_permutation():
    for bits in range(1, 11):
        lower = 1 << (bits - 1)
        upper = 1 << bits
        images = {module.renormalized_front(value) for value in range(lower, upper)}
        assert images == set(range(lower, upper))


def test_truncation_commutes_with_one_block():
    for value in range(1, 1 << 10):
        for shift in range(11):
            assert (
                module.advance_fringe(value) >> (shift + 2)
                == module.renormalized_front(value >> shift)
            )


def test_iterated_semiconjugacy():
    for value in range(1, 1 << 10):
        for blocks in range(9):
            left = module.iterate_fringe(4 * value, blocks) >> (2 * blocks + 2)
            assert left == module.iterate_front(value, blocks)


def test_return_high_front_recovers_coordinate_and_history():
    for value in range(1, 1 << 10):
        word, span, final = module.follow_returns(value, 4)
        high = final >> (2 * span)
        assert high == module.iterate_front(value, span)
        recovered = high
        for _ in range(span):
            recovered = module.inverse_renormalized_front(recovered)
        assert recovered == value
        assert module.follow_returns(recovered, 4) == (word, span, final)


def test_default_campaign_certificate_and_dyadic_cycles():
    payload = module.run_campaign()
    assert (
        payload["certificate_sha256"]
        == "ae54a368999a0467f5a86a67073a235f669365d71a634621504b3e5b93417229"
    )
    assert payload["validation"]["shell_states"] == (1 << 14) - 1
    for row in payload["cycle_census"]:
        assert all(
            int(length) & (int(length) - 1) == 0
            for length in row["cycle_counts"]
        )
