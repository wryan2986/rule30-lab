#!/usr/bin/env python3
"""Tests for the physical realizability check."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import check_physical_pairing_obstruction as chk
def test_cellarray_matches_packed_hand():
    for seed, w in ((1, 6), (3, 6), (7, 8), (21, 10), (255, 14), (4095, 18)):
        assert chk.T_cellarray(seed, w) == chk.T_packed(seed), seed
        assert chk.T_cellarray(chk.T_packed(seed), w + 2) == chk.T_packed(chk.T_packed(seed))
def test_bitlength_law_and_target_shape():
    assert chk.TARGET_X.bit_length() == chk.TARGET_SUM == 27
    assert chk.TARGET_X & 3 == 3
    for s in (1, 7, 13):
        seed = 2 ** s - 1
        traj = chk.iterate_packed(seed, 27 - s)
        assert traj[27 - s].bit_length() == s + 2 * (27 - s)
        assert (traj[27 - s] >> (27 - s)).bit_length() == 27
def test_packed_hand_trajectory():
    assert chk.iterate_packed(1, 4) == [1, 7, 25, 111, 401]


def test_physical_last_step_and_driver(monkeypatch):
    monkeypatch.setattr(chk, "TARGET_X", 27)
    monkeypatch.setattr(chk, "TARGET_SCHEDULE", "t")
    hit = chk.assess_hit(3, 2, 3)
    assert hit["centers"] == "1010"
    assert hit["coupled_halfrows"] and hit["cellarray_confirmed"]
    assert hit["rows"][0]["b"] == 0
    assert hit["rows"][0]["next_halfrow_hex"] == "0x6f"
    monkeypatch.setattr(chk, "TARGET_SCHEDULE", "u")
    mismatch = chk.assess_hit(3, 2, 3)
    assert not mismatch["coupled_halfrows"]
    assert not mismatch["rows"][0]["physical_branch_match"]
    assert not mismatch["rows"][0]["halfrow_step_match"]


def test_full_campaign_shape():
    import tempfile, json
    payload = chk.run_campaign(check_time=False)
    assert payload["question"] == "problem1"
    assert payload["result"]["seeds_enumerated"] == 4096
    assert payload["status"] in ("refuted", "finite-exhaustive")
    assert "certificate_sha256" in payload["result_hashes"]
    widths = payload["result"]["per_width"]
    assert [w["seeds"] for w in widths] == [1] + [2 ** (s - 2) for s in range(2, 14)]
    assert sum(w["seeds"] for w in widths) == 4096
    for hit in payload["result"]["hits"]:
        assert hit["cellarray_confirmed"] is True
        assert len(hit["centers"]) == 18 and len(hit["rows"]) == 8
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td) / "r.json"
        chk.write_record_atomic(payload, dest)
        assert json.loads(dest.read_text())["experiment_id"] == payload["experiment_id"]
