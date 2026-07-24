from analyze_period_two_witness_lifts import (
    KAPPA_P,
    KAPPA_U,
    actual_pair,
    actual_survivor_residue,
    forward_generator,
    inverse_generator_mod,
    phase_lift_profile,
    run_campaign,
)


def test_generator_inverses_small_quotients() -> None:
    for width in range(1, 11):
        mask = (1 << width) - 1
        for state in range(1 << width):
            for letter in ("t", "p", "u"):
                image = forward_generator(letter, state, width)
                assert inverse_generator_mod(letter, image, width) == (state & mask)


def test_actual_survivor_pair_prefix() -> None:
    residue = actual_survivor_residue(12)
    pairs = [(residue >> (2 * index)) & 3 for index in range(12)]
    assert pairs == [3, 1, 0, 3, 2, 1, 0, 1, 1, 0, 0, 3]


def test_known_depth_three_profiles() -> None:
    assert phase_lift_profile(3, "p") == (7, 10, 7, 8)
    assert phase_lift_profile(3, "u") == (2, 6, 9, 7)


def test_profile_projection_minimum() -> None:
    for depth in range(1, 7):
        assert min(phase_lift_profile(depth, "p")) == KAPPA_P[depth]
        assert min(phase_lift_profile(depth, "u")) == KAPPA_U[depth]


def test_actual_coordinate_recovers_next_complexity() -> None:
    for depth in range(1, 7):
        digit = actual_pair(depth)
        assert phase_lift_profile(depth, "p")[digit] == KAPPA_P[depth + 1]
        assert phase_lift_profile(depth, "u")[digit] == KAPPA_U[depth + 1]


def test_deterministic_campaign_certificate() -> None:
    result = run_campaign(6)
    assert result["certificate"] == "8cbb471a6ee29272f7ba9813af2b74ce1dc85ce1e1fbacc6b047a44fc287581b"
