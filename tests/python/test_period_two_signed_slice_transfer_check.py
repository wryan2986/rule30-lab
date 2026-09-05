#!/usr/bin/env python3
"""Tests for the signed-slice transfer closure check."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "python"))
import period_two_signed_slice_transfer_check as chk
def test_oracle_agreement_small():
    for ph in chk.PHASES:
        a = chk.build_levels(ph, 6, chk.frontier_children_primary)
        b = chk.build_levels(ph, 6, chk.oracle_frontier_children)
        for k in range(1, 7):
            assert a[k] == b[k], (ph, k)
def test_base_cases():
    assert chk.build_levels("p", 2, chk.frontier_children_primary)[1] == {3}
    assert chk.build_levels("u", 2, chk.frontier_children_primary)[1] == {1}
def test_direct_recursive_agree():
    lv = {ph: chk.build_levels(ph, 6, chk.frontier_children_primary) for ph in chk.PHASES}
    n = 0
    for ph in chk.PHASES:
        for k in range(2, 7):
            for x in sorted(lv[ph][k]):
                for L in range(1, min(k - 1, 3) + 1):
                    if 1 <= L <= k - 2:
                        assert chk.belief_direct(lv[ph], k, x, L) == chk.belief_recursive(lv[ph], k, x, L), (ph, k, hex(x), L)
                        n += 1
    assert n > 50
def test_slice_mass_consistent_and_lift():
    lv = {ph: chk.build_levels(ph, 7, chk.frontier_children_primary) for ph in chk.PHASES}
    rows = 0
    for rec in chk.iter_universal(lv, 6, None, False):
        assert sum(rec["Vp"]) == rec["Sp"]
        assert sum(rec["Vc"]) == rec["Sc"]
        m = int(rec["m"], 2)
        pred = sum(chk.local_signed_factor(m, n) * v for n, v in zip(chk.MASK_ORDER, rec["Vp"]))
        assert pred == rec["Sc"], rec
        assert rec["next_mask_source"] == "levels"
        rows += 1
        if rows >= 400:
            break
    assert rows == 400
def test_joint_tensor_identities_sample():
    lv = {ph: chk.build_levels(ph, 7, chk.frontier_children_primary) for ph in chk.PHASES}
    checked = 0
    for rec in chk.iter_universal(lv, 5, None, False):
        ph, pk = rec["phase"], rec["parent_k"]
        q, d = int(rec["parent_hex"], 16), rec["digit"]
        pL = rec["parent_L"]
        tab = chk.joint_fiber_tensor(lv[ph], pk, q, pL, d)
        for (n, r) in tab:
            assert ((1 << d) & n) != 0, (rec, hex(n))
        vp = tuple(rec["Vp"])
        marg = {n: 0 for n in chk.MASK_ORDER}
        for (n, r), v in tab.items():
            marg[n] += v
        for i, n in enumerate(chk.MASK_ORDER):
            assert marg[n] == (vp[i] if ((1 << d) & n) != 0 else 0), (rec, n, marg[n], vp[i])
        m = int(rec["m"], 2)
        recon = {r: 0 for r in chk.MASK_ORDER}
        for (n, r), v in tab.items():
            recon[r] += chk.local_signed_factor(m, n) * v
        assert list(recon[r] for r in chk.MASK_ORDER) == rec["Vc"], rec
        checked += 1
        if checked >= 60:
            break
    assert checked == 60
def test_joint_tensor_digit_two_nonempty_n12():
    lv = {ph: chk.build_levels(ph, 8, chk.frontier_children_primary) for ph in chk.PHASES}
    found = 0
    for rec in chk.iter_universal(lv, 7, None, False):
        if rec["digit"] != 2:
            continue
        ph, pk = rec["phase"], rec["parent_k"]
        q, pL = int(rec["parent_hex"], 16), rec["parent_L"]
        tab = chk.joint_fiber_tensor(lv[ph], pk, q, pL, 2)
        rows12 = {k: v for k, v in tab.items() if k[0] == 12 and v != 0}
        if not rows12:
            continue
        i12 = chk.MASK_ORDER.index(12)
        assert rec["Vp"][i12] != 0, rec
        assert sum(v for (n, r), v in tab.items() if n == 12) == rec["Vp"][i12], rec
        assert (2 & ~12) != 0, "old predicate would have skipped this nonempty row"
        found += 1
        if found >= 5:
            break
    assert found >= 5, "no nonempty digit-2 n=12 tensor rows in box"
def test_recursive_outgoing_fiber_agrees():
    lv = {ph: chk.build_levels(ph, 8, chk.frontier_children_primary) for ph in chk.PHASES}
    mod = chk.load_lift_module()
    n = 0
    for rec in chk.iter_universal(lv, 7, None, False):
        rm = chk.recursive_outgoing_fiber(mod, rec["phase"], rec["child_k"], int(rec["child_hex"], 16))
        assert format(rm, "04b") == rec["next_mask"], rec
        n += 1
        if n >= 100:
            break
    assert n == 100
def test_strong_key_has_both_masks():
    lv = {ph: chk.build_levels(ph, 7, chk.frontier_children_primary) for ph in chk.PHASES}
    for rec in chk.iter_universal(lv, 5, None, False):
        kb, ks = chk.base_key(rec), chk.strong_key(rec)
        assert ks[:len(kb)] == kb
        assert ks[len(kb):] == (rec["high_mask"], rec["next_mask"])
        break
def test_parent_cap_bound():
    try:
        chk.run_campaign(pcap=10, dmax=6, check_time=False)
    except chk.TransferLimitError:
        return
    raise AssertionError("pcap=10 accepted")
def test_truncation_forces_inconclusive():
    payload = chk.run_campaign(pcap=2, dmax=6, cap=1, check_time=False)
    assert payload["result"]["truncated_schedules"] > 0
    assert payload["result"]["completed_through_cap"] is False
    assert payload["status"] == "inconclusive", payload["status"]
def test_small_campaign_payload():
    import tempfile, json
    payload = chk.run_campaign(pcap=5, dmax=6, check_time=False)
    assert payload["question"] == "problem1"
    assert payload["result_summary"]["universal_transitions_total"] > 0
    assert "certificate_sha256" in payload["result_hashes"]
    assert payload["status"] in ("refuted", "finite-exhaustive", "inconclusive")
    assert payload["result"]["completed_through_cap"] is True
    for key in ("base_collision", "strong_collision"):
        col = payload["result"][key]
        if col is not None:
            a, b = col["first"], col["second"]
            ka = (a["phase"], a["parent_k"], a["parent_L"], a["digit"], a["m"], tuple(a["Vp"]))
            kb = (b["phase"], b["parent_k"], b["parent_L"], b["digit"], b["m"], tuple(b["Vp"]))
            assert ka == kb and tuple(a["Vc"]) != tuple(b["Vc"])
            sa = (a["high_mask"], a["next_mask"])
            sb = (b["high_mask"], b["next_mask"])
            if key == "strong_collision":
                assert sa == sb
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td) / "r.json"
        chk.write_record_atomic(payload, dest)
        assert json.loads(dest.read_text())["experiment_id"] == payload["experiment_id"]
def test_two_step_obstruction_replay():
    lv = {ph: chk.build_levels(ph, 9, chk.frontier_children_primary) for ph in chk.PHASES}
    mod = chk.load_lift_module()
    rec = chk.verify_two_step_obstruction(lv["p"], mod)
    assert rec["verified"] is True
    assert rec["two_step_key"] == {"phase": "p", "grandparent_k": 6, "grandparent_L": 1,
     "Vp": [2, 0, 0, 0, 1], "digits": [0, 0], "masks": ["1011", "1011"]}
    masses = [b["grandchild_signed_mass"] for b in rec["branches"]]
    assert masses == [-1, 1], masses
    assert rec["branches"][0]["child_Vc"] == [0, 0, 1, 0, 0]
    assert rec["branches"][1]["child_Vc"] == [0, 0, 0, 0, 1]
    assert len(rec["parent_tables"]["0xc82"]) == 3
    assert rec["child_tables"]["0x3208"] == [{"endpoint_hex": "0xc88", "cost": 0, "next_mask": "1011"}]
    assert rec["child_tables"]["0x3220"] == [{"endpoint_hex": "0xc80", "cost": 0, "next_mask": "1111"}]
def test_small_campaign_has_two_step():
    payload = chk.run_campaign(pcap=5, dmax=6, check_time=False)
    two = payload["result"]["two_step_obstruction"]
    assert two["verified"] is True
    assert [b["grandchild_signed_mass"] for b in two["branches"]] == [-1, 1]
def test_two_step_exact_tables():
    lv = {ph: chk.build_levels(ph, 9, chk.frontier_children_primary) for ph in chk.PHASES}
    mod = chk.load_lift_module()
    rec = chk.verify_two_step_obstruction(lv["p"], mod)
    assert rec["grandchild_tables"]["0xc820"] == [{"endpoint_hex": "0x3220", "cost": 1, "next_mask": "1011"}]
    assert rec["grandchild_tables"]["0xc880"] == [{"endpoint_hex": "0x3200", "cost": 0, "next_mask": "1100"}]
    assert rec["parent_tables"]["0xc82"] == [
     {"endpoint_hex": "0x322", "cost": 0, "next_mask": "1111"},
     {"endpoint_hex": "0x372", "cost": 0, "next_mask": "0000"},
     {"endpoint_hex": "0x376", "cost": 0, "next_mask": "0000"}]
def test_schedule_cap_bound():
    for bad in (0, 65):
        try:
            chk.run_campaign(pcap=2, dmax=6, cap=bad, check_time=False)
        except chk.TransferLimitError:
            continue
        raise AssertionError("cap accepted: %r" % bad)
