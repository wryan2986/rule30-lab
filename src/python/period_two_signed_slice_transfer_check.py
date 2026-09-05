#!/usr/bin/env python3
"""Signed-slice vector transfer closure falsification (Problem 1)."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, resource, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any
PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
MASK_ORDER = (0, 3, 11, 12, 15)
ALLOWED_MASKS = (0, 3, 11, 12, 15)
UNIVERSAL_PARENT_CAP = 9
DOMAIN_MAX_K = 16
LEVELS_MAX = 16
SCHEDULE_CAP = 64
ORACLE_K = 8
TIME_BUDGET_SECONDS = 120.0
MEMORY_BUDGET_KIB = 1024 * 1024
RESULT_FILENAME = "20260905_signed_slice_transfer_check.json"
ROOT = Path(__file__).resolve().parents[2]
TEST_RELATIVE = "tests/python/test_period_two_signed_slice_transfer_check.py"
HYPOTHESIS = ("Closure: for fixed phase, parent complexity/depth, adjoined digit, "
 "local current mask and full five-component parent slice vector determine the "
 "child slice vector; stronger key adds the high current mask and the outgoing "
 "fiber of the child.")
LIFT_MODULE_RELATIVE = ("experiments/problem1_nonperiodicity/"
 "analyze_period_two_phase_frontier_lift_recursion.py")
class TransferLimitError(RuntimeError):
    pass
class SeparationViolationError(RuntimeError):
    pass
class OracleMismatchError(RuntimeError):
    pass
def forward_generator(name, state):
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError(name)
def frontier_children_primary(state):
    return tuple(sorted({forward_generator(n, state) for n in "tup"}))
def oracle_frontier_children(state):
    if state <= 0:
        raise ValueError("oracle states are positive")
    width = state.bit_length() + 2
    bits = [(state >> j) & 1 for j in range(width)]
    tout = 0
    for j in range(width):
        xj = bits[j]
        lo1 = bits[j - 1] if j >= 1 else 0
        lo2 = bits[j - 2] if j >= 2 else 0
        if xj ^ (lo1 | lo2):
            tout |= 1 << j
    uout = tout ^ 0b1
    pbit0 = ((tout & 1) ^ 1)
    pbit1 = ((tout >> 1) & 1) ^ (1 if (state & 1) == 0 else 0)
    pout = (tout & ~0b11) ^ pbit0 ^ (pbit1 << 1)
    return tuple(sorted({tout, uout, pout}))
def phase_start(phase):
    if phase == "p":
        return 3
    if phase == "u":
        return 1
    raise ValueError(phase)
def build_levels(phase, maximum_complexity, childfn):
    levels = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append({c for s in levels[-1] for c in childfn(s)})
    return levels
def load_lift_module():
    import importlib.util
    path = ROOT / LIFT_MODULE_RELATIVE
    spec = importlib.util.spec_from_file_location("lift_recursion_member", path)
    if spec is None or spec.loader is None:
        raise TransferLimitError("lift membership module unavailable")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
def outgoing_fiber_levels(levels_ph, ck, x):
    return sum(1 << d for d in range(4) if 4 * x + d in levels_ph[ck + 1])
def recursive_outgoing_fiber(lift_mod, phase, ck, x):
    m = 0
    for d in range(4):
        if lift_mod.frontier_member(phase, ck + 1, 4 * x + d):
            m |= 1 << d
    if m not in ALLOWED_MASKS:
        raise AssertionError("recursive fiber escaped five-mask alphabet")
    return m
def outgoing_fiber(levels_ph, lift_mod, phase, ck, x):
    if ck + 1 <= len(levels_ph) - 1:
        m = outgoing_fiber_levels(levels_ph, ck, x)
        if m not in ALLOWED_MASKS:
            raise AssertionError("fiber escaped five-mask alphabet")
        return m, "levels"
    if lift_mod is None:
        raise TransferLimitError("outgoing fiber beyond built frontier without lift module")
    return recursive_outgoing_fiber(lift_mod, phase, ck, x), "recursive"
def fiber_mask(levels, complexity, quotient):
    mask = sum(1 << d for d in range(4) if 4 * quotient + d in levels[complexity + 1])
    if mask not in ALLOWED_MASKS:
        raise AssertionError("fiber escaped five-mask alphabet")
    return mask
def mask_sequence(levels, complexity, state, depth):
    out = []
    for step in range(depth):
        q = state >> 2
        out.append(fiber_mask(levels, complexity - 1 - step, q))
        state = q
    return tuple(out)
def dominates(current, shadow):
    return len(current) == len(shadow) and all(not (a & ~b) for a, b in zip(current, shadow))
def defect_count(shadow):
    return sum(m != 0b1111 for m in shadow)
def local_signed_factor(current_mask, shadow_mask):
    if current_mask & ~shadow_mask:
        return 0
    return 1 if shadow_mask == 0b1111 else -1
def congruent_witnesses(levels, complexity, current, depth):
    mod = 4 ** depth
    res = current % mod
    return sorted(s for s in levels[complexity - 1] if s % mod == res)
def belief_direct(levels, complexity, current, depth):
    if depth >= complexity - 1:
        wit = congruent_witnesses(levels, complexity, current, depth)
        if wit:
            raise SeparationViolationError("separation violated k=%d L=%d" % (complexity, depth))
        return {}
    mod = 4 ** depth
    res = current % mod
    cur = mask_sequence(levels, complexity, current, depth)
    out = {}
    for sh in levels[complexity - 1]:
        if sh % mod != res:
            continue
        sm = mask_sequence(levels, complexity - 1, sh, depth)
        if dominates(cur, sm):
            out[sh] = defect_count(sm)
    return out
def belief_recursive(levels, complexity, current, depth):
    if not 1 <= depth <= complexity - 2:
        raise TransferLimitError("recursive belief needs 1<=L<=k-2")
    digit = current & 3
    quotient = current >> 2
    cmask = fiber_mask(levels, complexity - 1, quotient)
    if depth == 1:
        out = {}
        for sh in levels[complexity - 1]:
            if sh & 3 != digit:
                continue
            sm = fiber_mask(levels, complexity - 2, sh >> 2)
            if not (cmask & ~sm):
                out[sh] = int(sm != 0b1111)
        return out
    lower = belief_recursive(levels, complexity - 1, quotient, depth - 1)
    tgt = levels[complexity - 1]
    out = {}
    for sq, lc in lower.items():
        sh = 4 * sq + digit
        if sh not in tgt:
            continue
        sm = fiber_mask(levels, complexity - 2, sq)
        if cmask & ~sm:
            continue
        out[sh] = lc + int(sm != 0b1111)
    return out
def forced_zero_schedule(state, cap=SCHEDULE_CAP):
    word = []
    for _ in range(cap):
        res = state & 15
        if res == 7:
            br = "u"
        elif res == 11:
            br = "t"
        else:
            return "".join(word)
        state = forward_generator(br, forward_generator("p", (state - 3) >> 2))
        word.append(br)
    raise TransferLimitError("schedule cap reached")
def admissible(word):
    return not any(f in word for f in FORBIDDEN)
def return_extension(gaps, final_u):
    w = "u"
    for i, g in enumerate(gaps):
        w += "t" * (g - 1)
        if i < len(gaps) - 1 or final_u:
            w += "u"
    return w
def three_return_patterns():
    rows = []
    for gaps in product(GAPS, repeat=3):
        tgt = return_extension(gaps, False)
        full = return_extension(gaps, True)
        if admissible(full):
            rows.append((gaps, tgt, full))
    return tuple(rows)
def slice_vector(levels, complexity, state, depth):
    bel = belief_direct(levels, complexity, state, depth)
    vec = {m: 0 for m in MASK_ORDER}
    for y, c in bel.items():
        n = fiber_mask(levels, complexity - 1, y)
        vec[n] += 1 if c % 2 == 0 else -1
    return tuple(vec[m] for m in MASK_ORDER), bel
def joint_fiber_tensor(levels, parent_k, parent_q, parent_L, digit):
    pbel = belief_direct(levels, parent_k, parent_q, parent_L)
    tab = {}
    for p, c in pbel.items():
        n = fiber_mask(levels, parent_k - 1, p)
        if (1 << digit) & ~n:
            continue
        y = 4 * p + digit
        if y not in levels[parent_k]:
            continue
        r = fiber_mask(levels, parent_k, y)
        w = 1 if c % 2 == 0 else -1
        tab[(n, r)] = tab.get((n, r), 0) + w
    return tab
TWO_STEP_MIN_LEVEL = 8
TWO_STEP_EXPECTED = {
    "parents": {0xc82: [(0x322, 0, 15), (0x372, 0, 0), (0x376, 0, 0)],
                0xc88: [(0x320, 0, 15), (0x370, 0, 0), (0x374, 0, 0)]},
    "children": {0x3208: [(0xc88, 0, 11)], 0x3220: [(0xc80, 0, 15)]},
    "grandchild_mass": {0xc820: -1, 0xc880: 1},
    "grandchildren": {0xc820: [(0x3220, 1, 11)], 0xc880: [(0x3200, 0, 12)]},
    "joint": {(0xc82, 0): {(15, 11): 1}, (0xc88, 0): {(15, 15): 1}},
}
def verify_two_step_obstruction(levels_ph, lift_mod):
    lv = levels_ph
    def table(k, x, L):
        bel = belief_direct(lv, k, x, L)
        if 1 <= L <= k - 2 and bel != belief_recursive(lv, k, x, L):
            raise OracleMismatchError("two-step direct/recursive disagree at " + hex(x))
        return bel
    ptabs, ctabs, gtabs = {}, {}, {}
    for q, rows in TWO_STEP_EXPECTED["parents"].items():
        if q not in lv[6]:
            raise TransferLimitError("two-step parent left the frontier")
        bel = table(6, q, 1)
        got = sorted((y, c, fiber_mask(lv, 5, y)) for y, c in bel.items())
        if got != sorted(rows):
            raise OracleMismatchError("two-step parent table changed at " + hex(q))
        ptabs[hex(q)] = [{"endpoint_hex": hex(y), "cost": c, "next_mask": format(n, "04b")} for y, c, n in got]
    for x, rows in TWO_STEP_EXPECTED["children"].items():
        if x not in lv[7]:
            raise TransferLimitError("two-step child left the frontier")
        bel = table(7, x, 2)
        got = sorted((y, c, fiber_mask(lv, 6, y)) for y, c in bel.items())
        if got != sorted(rows):
            raise OracleMismatchError("two-step child table changed at " + hex(x))
        ctabs[hex(x)] = [{"endpoint_hex": hex(y), "cost": c, "next_mask": format(n, "04b")} for y, c, n in got]
    gmasses = {}
    for g, want in TWO_STEP_EXPECTED["grandchild_mass"].items():
        if g not in lv[8]:
            raise TransferLimitError("two-step grandchild left the frontier")
        bel = table(8, g, 3)
        got_mass = sum(1 if c % 2 == 0 else -1 for c in bel.values())
        if got_mass != want:
            raise OracleMismatchError("two-step grandchild mass changed at " + hex(g))
        got_tab = sorted((y, c, fiber_mask(lv, 7, y)) for y, c in bel.items())
        if got_tab != sorted(TWO_STEP_EXPECTED["grandchildren"][g]):
            raise OracleMismatchError("two-step grandchild table changed at " + hex(g))
        gmasses[hex(g)] = got_mass
        gtabs[hex(g)] = [{"endpoint_hex": hex(y), "cost": c, "next_mask": format(fiber_mask(lv, 7, y), "04b")} for y, c in sorted(bel.items())]
    for q, d, want in ((0xc82, 0, {(15, 11): 1}), (0xc88, 0, {(15, 15): 1})):
        tab = joint_fiber_tensor(lv, 6, q, 1, d)
        if tab != want:
            raise OracleMismatchError("two-step joint table changed at " + hex(q))
    r1 = transition_record(lv, lift_mod, "p", 6, 0xc82, 1, 0)
    r2 = transition_record(lv, lift_mod, "p", 6, 0xc88, 1, 0)
    if base_key(r1) != base_key(r2) or strong_key(r1) != strong_key(r2):
        raise OracleMismatchError("two-step one-step keys diverged")
    if tuple(r1["Vc"]) == tuple(r2["Vc"]):
        raise OracleMismatchError("two-step child vectors agree: no one-step collision")
    if r1["next_mask"] != "1011" or r2["next_mask"] != "1011":
        raise OracleMismatchError("two-step outgoing masks changed")
    for rec, g in ((r1, 0xc820), (r2, 0xc880)):
        m = int(rec["next_mask"], 2)
        pred = sum(local_signed_factor(m, n) * v for n, v in zip(MASK_ORDER, rec["Vc"]))
        if pred != gmasses[hex(g)]:
            raise OracleMismatchError("two-step lift prediction failed at " + hex(g))
    return {"verified": True, "scope": "universal box only (not a domain claim)",
     "two_step_key": {"phase": "p", "grandparent_k": 6, "grandparent_L": 1,
      "Vp": r1["Vp"], "digits": [0, 0], "masks": [r1["m"], r1["next_mask"]]},
     "branches": [
      {"grandparent_hex": "0xc82", "child_hex": "0x3208", "grandchild_hex": "0xc820",
       "child_Vc": r1["Vc"], "grandchild_signed_mass": gmasses["0xc820"]},
      {"grandparent_hex": "0xc88", "child_hex": "0x3220", "grandchild_hex": "0xc880",
       "child_Vc": r2["Vc"], "grandchild_signed_mass": gmasses["0xc880"]}],
     "parent_tables": ptabs, "child_tables": ctabs, "grandchild_tables": gtabs}
def transition_record(levels_ph, lift_mod, phase, pk, q, pL, digit):
    ck = pk + 1
    x = 4 * q + digit
    cL = pL + 1
    m = fiber_mask(levels_ph, pk, q)
    masks = mask_sequence(levels_ph, ck, x, cL)
    high_mask = masks[1]
    next_mask, next_source = outgoing_fiber(levels_ph, lift_mod, phase, ck, x)
    vp, pbel = slice_vector(levels_ph, pk, q, pL)
    vc, cbel = slice_vector(levels_ph, ck, x, cL)
    sp = sum(vp)
    sc = sum(vc)
    return {"phase": phase, "parent_k": pk, "parent_L": pL, "parent_hex": hex(q),
     "digit": digit, "child_k": ck, "child_L": cL, "child_hex": hex(x),
     "m": format(m, "04b"), "high_mask": format(high_mask, "04b"),
     "next_mask": format(next_mask, "04b"), "next_mask_source": next_source,
     "Vp": list(vp), "Vc": list(vc), "Sp": sp, "Sc": sc,
     "parent_endpoints": len(pbel), "child_endpoints": len(cbel)}
def base_key(rec):
    return (rec["phase"], rec["parent_k"], rec["parent_L"], rec["digit"], rec["m"], tuple(rec["Vp"]))
def strong_key(rec):
    return base_key(rec) + (rec["high_mask"], rec["next_mask"])
def iter_universal(levels, pcap, t0, check_time, lift_mod=None):
    for pk in range(2, pcap + 1):
        for phase in PHASES:
            lv = levels[phase]
            for pL in range(1, pk):
                for q in sorted(lv[pk]):
                    for digit in range(4):
                        x = 4 * q + digit
                        if x not in lv[pk + 1]:
                            continue
                        if check_time and time.monotonic() - t0 > TIME_BUDGET_SECONDS:
                            raise TransferLimitError("time budget exceeded in universal scan")
                        yield transition_record(lv, lift_mod, phase, pk, q, pL, digit)
def find_first_collision(records):
    seen_b, seen_s = {}, {}
    col_b, col_s = None, None
    counts = {"transitions": 0}
    for rec in records:
        counts["transitions"] += 1
        kb, ks = base_key(rec), strong_key(rec)
        if col_b is None:
            if kb in seen_b and tuple(seen_b[kb]["Vc"]) != tuple(rec["Vc"]):
                col_b = {"first": seen_b[kb], "second": rec}
            else:
                seen_b.setdefault(kb, rec)
        if col_s is None:
            if ks in seen_s and tuple(seen_s[ks]["Vc"]) != tuple(rec["Vc"]):
                col_s = {"first": seen_s[ks], "second": rec}
            else:
                seen_s.setdefault(ks, rec)
        if col_b is not None and col_s is not None:
            break
    return col_b, col_s, counts
def three_return_occurrences(levels, maxK, cap, t0, check_time=True):
    pats = three_return_patterns()
    if len(pats) != 56:
        raise AssertionError("pattern count changed")
    occ = []
    truncated = 0
    excluded_ge_k = 0
    for k in range(2, maxK + 1):
        for phase in PHASES:
            lv = levels[phase]
            for cur in sorted(lv[k]):
                if cur & 3 != 3:
                    continue
                try:
                    sched = forced_zero_schedule(cur, cap)
                except TransferLimitError:
                    truncated += 1
                    continue
                for cut in range(len(sched) + 1):
                    base = sched[:cut]
                    for gaps, tgt, full in pats:
                        if not sched[cut:].startswith(tgt):
                            continue
                        if not admissible(base + full):
                            continue
                        L = cut + 1
                        if not L < k:
                            excluded_ge_k += 1
                            continue
                        if check_time and time.monotonic() - t0 > TIME_BUDGET_SECONDS:
                            raise TransferLimitError("time budget exceeded in domain scan")
                        occ.append((phase, k, cur, L))
    return occ, truncated, excluded_ge_k
def ancestor_closure(occ):
    out = set()
    for phase, k, x, L in occ:
        for s in range(L):
            out.add((phase, k - s, x >> (2 * s), L - s))
    return out
def git_strict(args):
    import subprocess as sp
    c = sp.run(["git", "-C", str(ROOT)] + args, capture_output=True, text=True, timeout=30)
    if c.returncode != 0:
        raise TransferLimitError("git failed: " + c.stderr.strip())
    return c.stdout.strip()
def sha256_file(path):
    import hashlib as hl
    h = hl.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(65536), b""):
            h.update(ch)
    return h.hexdigest()
def hardware_facts():
    model, total = None, None
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    model = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    total = int(line.split()[1])
                    break
    except (OSError, ValueError):
        pass
    return {"cpu_model": model, "cpu_count": os.cpu_count(), "memory_total_kib": total, "architecture": platform.machine()}
def write_record_atomic(payload, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    enc = json.dumps(payload, indent=2, sort_keys=True).encode()
    with tempfile.NamedTemporaryFile(dir=str(dest.parent), delete=False) as h:
        h.write(enc)
        h.flush()
        os.fsync(h.fileno())
        tmp = h.name
    os.replace(tmp, dest)
    return dest
def apply_address_space_limit():
    budget = MEMORY_BUDGET_KIB * 1024
    rec = {"budget_bytes": budget}
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    except (OSError, ValueError) as exc:
        rec["address_space_limit_applied"] = False
        rec["reason"] = "getrlimit failed: %s" % exc
        return rec
    target = budget
    if hard != resource.RLIM_INFINITY and hard < budget:
        target = hard
    try:
        resource.setrlimit(resource.RLIMIT_AS, (target, hard))
    except (OSError, ValueError) as exc:
        rec["address_space_limit_applied"] = False
        rec["reason"] = "setrlimit failed: %s" % exc
        return rec
    rec["address_space_limit_applied"] = True
    rec["soft_bytes"] = target
    return rec
def run_campaign(pcap=UNIVERSAL_PARENT_CAP, dmax=DOMAIN_MAX_K, cap=SCHEDULE_CAP, check_time=True, enforcement=None):
    t0 = time.monotonic()
    if not 2 <= pcap <= 9:
        raise TransferLimitError("parent cap outside 2..9")
    if not 1 <= cap <= 64:
        raise TransferLimitError("schedule cap outside 1..64")
    if not 2 <= dmax <= 16:
        raise TransferLimitError("domain cap outside 2..16")
    need = max(pcap + 1, dmax, TWO_STEP_MIN_LEVEL)
    lift_mod = load_lift_module()
    levels = {ph: build_levels(ph, need, frontier_children_primary) for ph in PHASES}
    oracle_checked = 0
    for ph in PHASES:
        oc = build_levels(ph, min(ORACLE_K, need), oracle_frontier_children)
        for k in range(1, min(ORACLE_K, need) + 1):
            if oc[k] != levels[ph][k]:
                raise OracleMismatchError("oracle disagrees %s k=%d" % (ph, k))
            oracle_checked += len(levels[ph][k])
    halt_reason = None
    rec_bel_checks, lift_rows, lift_bad, rec_mask_checks = 0, 0, 0, 0
    uni_recs = []
    truncated = 0
    excluded_ge_k = 0
    occ = []
    dom = set()
    dom_recs = []
    col_b = col_s = dcol_b = dcol_s = None
    ucounts = {"transitions": 0}
    two_step = {"verified": False, "scope": "universal box only (not a domain claim)"}
    dcounts = {"transitions": 0}
    complete = True
    try:
        for rec in iter_universal(levels, pcap, t0, check_time, lift_mod):
            lv = levels[rec["phase"]]
            pk = rec["parent_k"]
            if 1 <= rec["parent_L"] <= pk - 2:
                if belief_direct(lv, pk, int(rec["parent_hex"], 16), rec["parent_L"]) != belief_recursive(lv, pk, int(rec["parent_hex"], 16), rec["parent_L"]):
                    raise OracleMismatchError("direct/recursive disagree at parent " + str(rec))
                rec_bel_checks += 1
            if 1 <= rec["child_L"] <= rec["child_k"] - 2:
                if belief_direct(lv, rec["child_k"], int(rec["child_hex"], 16), rec["child_L"]) != belief_recursive(lv, rec["child_k"], int(rec["child_hex"], 16), rec["child_L"]):
                    raise OracleMismatchError("direct/recursive disagree at child " + str(rec))
                rec_bel_checks += 1
            m = int(rec["m"], 2)
            pred = sum(local_signed_factor(m, n) * v for n, v in zip(MASK_ORDER, rec["Vp"]))
            lift_rows += 1
            if pred != rec["Sc"]:
                lift_bad += 1
                raise OracleMismatchError("lift identity failed at " + str(rec))
            if rec_mask_checks < 150:
                rm = recursive_outgoing_fiber(lift_mod, rec["phase"], rec["child_k"], int(rec["child_hex"], 16))
                rec_mask_checks += 1
                if format(rm, "04b") != rec["next_mask"]:
                    raise OracleMismatchError("recursive outgoing fiber disagrees at " + str(rec))
            uni_recs.append(rec)
        col_b, col_s, ucounts = find_first_collision(iter(uni_recs))
        occ, truncated, excluded_ge_k = three_return_occurrences(levels, dmax, cap, t0, check_time)
        if truncated:
            complete = False
            halt_reason = "%d schedule(s) hit the cap: domain box unresolved" % truncated
        dom = ancestor_closure(occ)
        dom_list = sorted(dom, key=lambda e: (e[1], 0 if e[0] == "p" else 1, e[3], e[2]))
        for phase, ck, x, cL in dom_list:
            if cL < 2 or ck < 3 or ck > dmax:
                continue
            pk, q, pL, digit = ck - 1, x >> 2, cL - 1, x & 3
            if (phase, pk, q, pL) not in dom:
                continue
            if x not in levels[phase][ck] or q not in levels[phase][pk]:
                raise TransferLimitError("domain strip left the frontier")
            if check_time and time.monotonic() - t0 > TIME_BUDGET_SECONDS:
                raise TransferLimitError("time budget exceeded in domain transitions")
            dom_recs.append(transition_record(levels[phase], lift_mod, phase, pk, q, pL, digit))
        for rec in dom_recs:
            if rec["child_k"] + 1 <= need:
                rm = recursive_outgoing_fiber(lift_mod, rec["phase"], rec["child_k"], int(rec["child_hex"], 16))
                rec_mask_checks += 1
                if format(rm, "04b") != rec["next_mask"]:
                    raise OracleMismatchError("recursive outgoing fiber disagrees at " + str(rec))
        dom_recs.sort(key=lambda r: (r["parent_k"], 0 if r["phase"] == "p" else 1, r["parent_L"], int(r["parent_hex"], 16), r["digit"]))
        dcol_b, dcol_s, dcounts = find_first_collision(iter(dom_recs))
        two_step = verify_two_step_obstruction(levels["p"], lift_mod)
        dcounts["ancestor_cylinders"] = len(dom)
        dcounts["occurrences"] = len(occ)
    except TransferLimitError as exc:
        complete = False
        halt_reason = str(exc) if halt_reason is None else halt_reason + "; " + str(exc)
    runtime = time.monotonic() - t0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    any_collision = any(c is not None for c in (col_b, col_s, dcol_b, dcol_s))
    if any_collision:
        status = "refuted"
    elif complete:
        status = "finite-exhaustive"
    else:
        status = "inconclusive"
    result = {"universal_transitions": ucounts["transitions"],
     "universal_transitions_total": len(uni_recs),
     "universal_belief_pair_checks": rec_bel_checks, "lift_identity_rows": lift_rows,
     "lift_disagreements": lift_bad, "oracle_states_compared": oracle_checked,
     "recursive_outgoing_fiber_checks": rec_mask_checks,
     "base_collision": col_b, "strong_collision": col_s,
     "domain_transitions": dcounts["transitions"],
     "domain_transitions_total": len(dom_recs),
     "domain_ancestors": len(dom), "domain_occurrences": len(occ),
     "truncated_schedules": truncated, "excluded_depth_ge_k": excluded_ge_k,
     "domain_base_collision": dcol_b, "domain_strong_collision": dcol_s,
     "two_step_obstruction": two_step,
     "completed_through_cap": complete, "halt_reason": halt_reason,
     "order": ["parent-k ascending", "phase p then u", "parent-L ascending",
      "parent state ascending", "digit 0..3"],
     "stopping": "first collision per key or cap; no cap increase"}
    canon = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    gs = git_strict(["status", "--short"])
    if enforcement is None:
        enforcement = {"address_space_limit_applied": False,
         "reason": "no CLI enforcement record passed (library call)",
         "deadline": "cooperative monotonic budget checks when check_time is true; no in-process preemption"}
    payload = {"experiment_id": "period-two-signed-slice-transfer-check",
     "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
     "git_commit": git_strict(["rev-parse", "HEAD"]),
     "git_branch": git_strict(["branch", "--show-current"]),
     "git_status": gs, "git_dirty": bool(gs.strip()), "worktree": str(ROOT),
     "source_hashes": {"analyzer_sha256": sha256_file(Path(__file__).resolve()),
      "lift_recursion_sha256": sha256_file(ROOT / LIFT_MODULE_RELATIVE)},
     "question": "problem1", "hypothesis": HYPOTHESIS, "backend": "python-direct-and-recursive",
     "parameters": {"universal_parent_cap": pcap, "domain_max_k": dmax,
      "schedule_cap": cap, "levels_built": need, "oracle_k": ORACLE_K,
      "time_budget_seconds": TIME_BUDGET_SECONDS, "memory_budget_kib": MEMORY_BUDGET_KIB},
     "enforcement": enforcement,
     "hardware": hardware_facts(),
     "software": {"python_version": platform.python_version(),
      "python_implementation": platform.python_implementation(), "os": platform.platform()},
     "runtime_seconds": runtime, "peak_rss_kib": peak, "result": result,
     "result_hashes": {"certificate_sha256": hashlib.sha256(canon).hexdigest()},
     "result_summary": {"universal_transitions": ucounts["transitions"],
      "universal_transitions_total": len(uni_recs), "domain_transitions_total": len(dom_recs),
      "base_collision_found": col_b is not None, "strong_collision_found": col_s is not None,
      "domain_transitions": dcounts["transitions"],
      "domain_base_collision_found": dcol_b is not None,
      "domain_strong_collision_found": dcol_s is not None,
      "truncated_schedules": truncated, "completed_through_cap": complete},
     "interpretation": ("A base- or strong-key collision is an exact finite counterexample that refutes the universal deterministic vector-closure claim; "
      "it does not rule out a preserved region under multiple successors, the signed-mass certificate, or Problem 1. "
      "The domain-specific closure on stripped three-return ancestors stays unresolved: absence of a collision through k<=16 is finite evidence only. "
      "The universal colliding pair is outside the finite k<=16 stripped-ancestor box; that does not show anything about the all-depth ancestor domain."),
     "status": status,
     "proof_scope": "bounded boxes only: universal parents 2<=k<=%d; stripped ancestors of the full three-return domain 2<=k<=%d" % (pcap, dmax),
     "limitations": ["finite caps; finite absence leaves the domain-specific closure unresolved (a domain collision would refute it)",
      "single local process; cooperative 120s wall budget plus outer timeout wrapper; 1GiB address-space cap enforced in CLI runs",
      "occurrences with L>=k are outside the proposed domain and counted as excluded, not successes",
      "schedules reaching the forced-schedule cap are counted as truncated and force inconclusive, never presented as exhaustive",
      "empty-belief transitions included; see endpoint counts in witnesses",
      "no sibling k>=17 sign-witness recomputation (lead reviews separately)"]}
    try:
        payload["source_hashes"]["test_sha256"] = sha256_file(ROOT / TEST_RELATIVE)
    except OSError:
        pass
    return payload
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parent-cap", type=int, default=UNIVERSAL_PARENT_CAP)
    ap.add_argument("--domain-max", type=int, default=DOMAIN_MAX_K)
    ap.add_argument("--schedule-cap", type=int, default=SCHEDULE_CAP)
    ap.add_argument("--output", type=str, default=None)
    a = ap.parse_args()
    enforcement = apply_address_space_limit()
    if not enforcement["address_space_limit_applied"]:
        raise TransferLimitError("could not enforce the address-space cap")
    import signal as _sig
    def _alarm(signum, frame):
        raise TransferLimitError("wall-clock alarm: 115s budget reached")
    _sig.signal(_sig.SIGALRM, _alarm)
    enforcement["alarm_seconds"] = 115
    enforcement["deadline"] = "SIGALRM at 115s plus cooperative monotonic checks plus outer timeout wrapper"
    _sig.alarm(115)
    try:
        payload = run_campaign(a.parent_cap, a.domain_max, a.schedule_cap, True, enforcement)
    finally:
        _sig.alarm(0)
    dest = Path(a.output) if a.output else ROOT / "results/problem1" / RESULT_FILENAME
    res = dest.resolve()
    if not res.is_relative_to(ROOT):
        raise TransferLimitError("output outside worktree")
    write_record_atomic(payload, res)
    print(json.dumps(payload, indent=2, sort_keys=True))
if __name__ == "__main__":
    main()
