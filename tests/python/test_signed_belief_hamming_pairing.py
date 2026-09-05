#!/usr/bin/env python3
"""Tests for the Hamming-neighbor pairing check."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import check_signed_belief_hamming_pairing as chk
def test_edge_bit_rule_and_residue():
    bel = {4: 0, 5: 1}
    _, _, adj, edges = chk.build_hamming_graph(bel, 1)
    assert edges == [] and adj == {4: [], 5: []}
    bel2 = {4: 0, 0: 1}
    _, _, adj2, edges2 = chk.build_hamming_graph(bel2, 1)
    assert edges2 == [(0, 4)] and adj2 == {0: [4], 4: [0]}
def test_hall_deficient_instance():
    bel = {0: 0, 4: 0, 5: 1}
    stats, edges = chk.analyze_instance(bel, 1)
    assert stats["saturated"] is False
    assert stats["single_sign_components"] == 3
    hv = stats["hall_violator"]
    assert hv["vertices_hex"] == ["0x5"] and hv["neighbor_size"] == 0
    assert hv["size"] == 1
def test_saturated_instance_with_essential():
    bel = {0: 0, 4: 1, 8: 1}
    stats, edges = chk.analyze_instance(bel, 1)
    assert stats["vertices"] == 3 and stats["edges"] == 2
    assert stats["saturated"] is True
    assert stats["hall_violator"] is None
def test_augment_matches_brute_force():
    cases = [
        (["a"], {"a": []}),
        (["a", "b"], {"a": ["x"], "b": ["x"]}),
        (["a", "b", "c"], {"a": ["x", "y"], "b": ["y", "z"], "c": ["x"]}),
    ]
    for left, adj in cases:
        ml, _ = chk.max_bipartite_matching(left, adj)
        assert len(ml) == chk.brute_max_matching_size(left, adj)
def test_hall_violator_independent():
    edges = [(0, 8), (4, 8)]
    viol = [0, 4]
    nbrs = chk.independent_hall_check(viol, edges)
    assert nbrs == [8] and len(nbrs) < len(viol)
def test_oracle_small():
    for ph in chk.PHASES:
        a = chk.build_levels(ph, 5, chk.frontier_children_primary)
        b = chk.build_levels(ph, 5, chk.oracle_frontier_children)
        for k in range(1, 6):
            assert a[k] == b[k]
def test_cap_bounds():
    for kw in ({"cap": 0}, {"cap": 65}, {"dmax": 17}):
        try:
            chk.run_campaign(check_time=False, **kw)
        except chk.PairingLimitError:
            continue
        raise AssertionError("bound accepted: %r" % kw)
def test_small_campaign_payload():
    import tempfile, json
    payload = chk.run_campaign(dmax=6, check_time=False)
    assert payload["question"] == "problem1"
    assert payload["status"] in ("refuted", "finite-exhaustive", "inconclusive")
    assert "certificate_sha256" in payload["result_hashes"]
    assert payload["result"]["completed_through_cap"] is True
    for row in payload["result"]["rows"]:
        g = row["graph"]
        assert g["saturated"] is True
        assert g["signed_mass"] != 0
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td) / "r.json"
        chk.write_record_atomic(payload, dest)
        assert json.loads(dest.read_text())["experiment_id"] == payload["experiment_id"]
def test_bitflip_edge_set_matches_build():
    cases = [{0: 0, 4: 0, 5: 1}, {0: 0, 4: 1, 8: 1, 12: 0, 16: 1},
              {3: 0, 19: 1, 35: 0, 51: 1}]
    for bel in cases:
        _, _, _, bedges = chk.build_hamming_graph(bel, 1)
        builtin = set((y, z) if y < z else (z, y) for y, z in bedges)
        assert chk.independent_edge_set(bel, 1) == builtin, bel
def test_first_obstruction_evidence():
    lv = chk.build_levels("u", 14, chk.frontier_children_primary)
    bel = chk.belief_direct(lv, 14, 0x642fdfb, 2)
    stats, _ = chk.analyze_instance(bel, 2)
    assert stats["saturated"] is False
    ev = chk.obstruction_evidence(lv, "u", 14, 0x642fdfb, 1, (2, 2, 2), 2, bel, stats)
    assert ev["edge_sets_match"] is True and ev["independent_edge_count"] == 10
    assert ev["full_word_admissible"] is True
    assert ev["base_prefix"] == "t" and ev["extension_word_E"] == "ututut"
    w = ev["isolated_vertex"]
    assert w["vertex_hex"] == "0x190825b" and w["cost"] == 1
    assert w["opposite_neighbors"] == 0 and w["positives_checked"] == 84
    assert w["bits_checked"][0] == 4
