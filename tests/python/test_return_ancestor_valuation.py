#!/usr/bin/env python3
"""Tests for the restricted ancestor valuation check."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import check_return_ancestor_valuation as chk
def test_gate_arithmetic():
    assert chk.gate_arith_selftest() == 7
    assert chk.gate(3, 1) is True
    assert chk.gate(6, 5) is False
    assert chk.gate(0, 0) is False
def test_oracle_small():
    a = chk.build_levels(6, chk.frontier_children_primary)
    b = chk.build_levels(6, chk.oracle_frontier_children)
    for k in range(1, 7):
        assert a[k] == b[k]
def test_belief_agreement_and_counts():
    lv = chk.build_levels(9, chk.frontier_children_primary)
    n = 0
    for k in (5, 8):
        for x in sorted(lv[k])[:40]:
            for L in (1, 2):
                if 1 <= L <= k - 2:
                    d = chk.belief_direct(lv, k, x, L)
                    assert d == chk.belief_recursive(lv, k, x, L)
                    n += 1
    assert n > 20
def test_ancestry_mapping():
    occ = [(10, 0x1234, 2, 3, "tututut"), (12, 0x5678, 0, 1, "ututut")]
    nodes = chk.ancestor_closure(occ)
    assert (10, 0x1234, 3) in nodes and (9, 0x1234 >> 2, 2) in nodes
    assert (8, 0x1234 >> 4, 1) in nodes
    assert nodes[(8, 0x1234 >> 4, 1)][0] == 10
def test_cap_bounds():
    for kw in ({"cap": 0}, {"cap": 65}, {"dmax": 19}):
        try:
            chk.run_campaign(check_time=False, **kw)
        except chk.ValuationLimitError:
            continue
        raise AssertionError("bound accepted")
def test_small_campaign_shape():
    import tempfile, json
    payload = chk.run_campaign(dmax=8, check_time=False)
    assert payload["question"] == "problem1"
    assert payload["status"] in ("refuted", "finite-exhaustive", "inconclusive")
    assert "certificate_sha256" in payload["result_hashes"]
    for row in payload["result"]["rows"]:
        assert row["endpoints"] == row["E"] + row["O"]
        assert row["signed_mass"] == row["E"] - row["O"]
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td) / "r.json"
        chk.write_record_atomic(payload, dest)
        assert json.loads(dest.read_text())["experiment_id"] == payload["experiment_id"]


def test_named_admissible_ancestor_failure():
    levels = chk.build_levels(16, chk.frontier_children_primary)
    row = chk.node_record(levels, 16, 0x6473d46a, 3)
    assert (row["E"], row["O"], row["endpoints"], row["signed_mass"]) == (52, 36, 88, 16)
    assert row["valuations"] == [3, 3] and not row["gate_pass"]
    occurrence = 0x6473d46ab
    word = chk.forced_zero_schedule(occurrence)
    assert word == "ttttutututu"
    assert word[4:10] == chk.GAP_WORD
    assert chk.admissible(word[:4] + chk.GAP_WORD + "u")
    assert occurrence >> 4 == 0x6473d46a
    assert 18 - 2 == 16 and 5 - 2 == 3
