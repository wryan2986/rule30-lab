from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments/problem1_nonperiodicity/analyze_period_two_shadow_mask_closure_obstruction.py"
)
spec = spec_from_file_location("mask_closure", MODULE_PATH)
assert spec and spec.loader
m = module_from_spec(spec)
spec.loader.exec_module(m)


def test_universal_signature_table():
    assert m.universal_signature_table() == [
        (0b0000, 0b0000), (0b0001, 0b1011),
        (0b0010, 0b1100), (0b0011, 0b1111),
        (0b1000, 0b0011), (0b1001, 0b1011),
        (0b1010, 0b1111), (0b1011, 0b1111),
        (0b1100, 0b1111), (0b1101, 0b1111),
        (0b1110, 0b1111), (0b1111, 0b1111),
    ]


def test_digit_two_forces_digit_three():
    assert all(
        not (predecessor & 0b0100) or predecessor & 0b1000
        for predecessor, _ in m.universal_signature_table()
    )


def test_unsafe_mask_pair_successor():
    row = m.closure_counterexample()["unsafe"]
    assert row["visible_pair"] == ["0b1011", "0b1111"]
    assert row["shared_digit"] == 2
    assert row["lower_pair"] == ["0b1111", "0b1100"]
    assert not row["lower_is_dominant"]


def test_same_visible_state_has_safe_successor():
    row = m.closure_counterexample()["safe"]
    assert row["visible_pair"] == ["0b1011", "0b1111"]
    assert row["shared_digit"] == 2
    assert row["lower_pair"] == ["0b1111", "0b1111"]
    assert row["lower_is_dominant"]


def test_twelve_signature_transition_is_nondeterministic():
    rows = m.signature_nondeterminism()["examples"]
    assert {tuple(row["source_signature"]) for row in rows} == {
        ("0b1000", "0b0011")
    }
    assert {tuple(row["target_signature"]) for row in rows} == {
        ("0b0010", "0b1100"),
        ("0b1110", "0b1111"),
        ("0b0000", "0b0000"),
    }


def test_small_campaign_realizes_all_signatures():
    payload = m.run_campaign(12)
    assert all(
        len(payload["phases"][phase]["signature_counts"]) == 12
        for phase in m.PHASES
    )
    assert payload["phases"]["p"]["distinct_signature_edges"] == 149
    assert payload["phases"]["u"]["distinct_signature_edges"] == 142


def test_default_certificate_and_boundary():
    payload = m.run_campaign()
    assert payload["certificate_sha256"] == (
        "63e48b7d4c2f1a0751f58384477686c944ed35eafd92a9d059bc64c7fbf89f36"
    )
    assert "does not prove" in payload["scientific_boundary"]
