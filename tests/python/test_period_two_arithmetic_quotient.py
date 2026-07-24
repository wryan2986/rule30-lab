from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_arithmetic_quotient.py"
)
spec = spec_from_file_location("arithq", MODULE_PATH)
assert spec is not None and spec.loader is not None
arithq = module_from_spec(spec)
spec.loader.exec_module(arithq)


def test_generator_parity_and_odd_collision():
    for state in range(1, 257):
        t_value = arithq.forward_generator("t", state)
        p_value = arithq.forward_generator("p", state)
        u_value = arithq.forward_generator("u", state)
        assert (t_value & 1) == (state & 1)
        assert (p_value & 1) != (state & 1)
        assert (u_value & 1) != (state & 1)
        assert (p_value == u_value) == bool(state & 1)


def test_pell_sequence_and_sum_identity():
    assert arithq.pell_numbers(8) == [0, 1, 2, 5, 12, 29, 70, 169, 408]
    assert [arithq.pell_cumulative_bound(n) for n in range(1, 7)] == [
        1,
        3,
        8,
        20,
        49,
        119,
    ]


def test_small_reachable_counts():
    rows, _ = arithq.reachable_rows(6)
    assert [row["distinct_exact_length_states"] for row in rows["p"]] == [
        1,
        2,
        5,
        11,
        20,
        39,
    ]
    assert [row["distinct_exact_length_states"] for row in rows["u"]] == [
        1,
        2,
        4,
        9,
        18,
        36,
    ]
    for phase in arithq.PHASES:
        for row in rows[phase]:
            assert row["distinct_exact_length_states"] <= row["pell_exact_bound"]
            assert row["distinct_cumulative_states"] <= row["pell_cumulative_bound"]


def test_actual_survivor_residue_32_bits():
    driver = arithq.actual_driver(16)
    residue = arithq.schedule_survivor_residue(driver, 32)
    assert residue == 0x88C146C7


def test_actual_agreement_small_campaign():
    result = arithq.actual_agreement_rows(8, 32)
    assert result["actual_survivor_residue_hex"] == "0x88c146c7"
    assert result["by_phase"]["p"][-1]["best_matching_bits"] == 11
    assert result["by_phase"]["u"][-1]["best_matching_bits"] == 8


def test_certificate_stability():
    result = arithq.run_campaign(8, 32)
    assert (
        result["certificate_sha256"]
        == "0a097269543109be9d88c64e779271a13872b3b2fac8623a3bc7d672a3e870f1"
    )
