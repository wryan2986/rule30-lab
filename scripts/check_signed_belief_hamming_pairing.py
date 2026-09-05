#!/usr/bin/env python3
"""Sign-reversing Hamming-neighbor pairing on three-return beliefs (Problem 1).

ADMISSION (bounded falsification; lead owns theorem and reduction judgment).
On each EXISTING full three-return instance through k<=16 (19 occurrences
 expected, both phases, all 56 admissible gap triples, final-u admissibility,
 depth L=c+1<k, source order k / phase p-then-u / state / cut / gaps), build a
graph whose vertices are the DISTINCT dominant concrete shadows B with signs
(-1)^cost, joining opposite-sign y,z whose xor is a power of two with the
single free bit b>=2L (above the fixed low 2L bits: exact, no splicing).
Hypothesis: every occurrence graph has a matching saturating the smaller sign
class. An obstruction refutes those sign-reversing involutions whose nonfixed
pairs are Hamming neighbors and whose fixed set is nonempty of a common sign
(equivalently here: the nonfixed pairs saturate the minority) on that
occurrence only; the all-fixed identity always exists, so the bare universal
Hamming class is not refuted as a whole. It does not refute arbitrary nonlocal
pairings, signed nonvanishing, or Problem 1. If all pass, report per-instance
matching counts rather than enlarging any cap. Stop at the first obstruction.
Either outcome bears on the route: obstruction kills the fixed-restricted
Hamming involution; passage isolates the exact matching data a pairing proof
must use. Finite boxes never prove infinite statements.

Caps: one local CPU, 120s wall, 1GiB address space, schedule cap 64, no
frontier beyond k<=16, no new census. Status refuted means the stated
per-occurrence matching hypothesis is falsified; finite-exhaustive means all
19 boxed occurrences pass; inconclusive means the box was not completed.
"""
from __future__ import annotations
import argparse, hashlib, json, os, platform, resource, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any
PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
ALLOWED_MASKS = (0, 3, 11, 12, 15)
DOMAIN_MAX_K = 16
EXPECTED_OCCURRENCES = 19
SCHEDULE_CAP = 64
ORACLE_K = 8
TIME_BUDGET_SECONDS = 120.0
MEMORY_BUDGET_KIB = 1024 * 1024
RESULT_FILENAME = "20260905_signed_belief_hamming_pairing.json"
ROOT = Path(__file__).resolve().parents[1]
TEST_RELATIVE = "tests/python/test_signed_belief_hamming_pairing.py"
HYPOTHESIS = ("For every full three-return occurrence (both phases, 2<=k<=16, "
 "all 56 admissible gap triples, final-u admissibility, depth L=c+1<k), the "
 "opposite-sign Hamming graph on distinct dominant shadows (edges join y,z of "
 "opposite sign with y^z a power of two at bit>=2L) has a matching saturating "
 "the smaller sign class.")
class PairingLimitError(RuntimeError):
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
    return 3 if phase == "p" else 1
def build_levels(phase, maximum_complexity, childfn):
    levels = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append({c for s in levels[-1] for c in childfn(s)})
    return levels
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
        raise PairingLimitError("recursive belief needs 1<=L<=k-2")
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
    raise PairingLimitError("schedule cap reached")
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
def build_hamming_graph(belief, depth):
    verts = sorted(belief)
    sign = {y: (1 if c % 2 == 0 else -1) for y, c in belief.items()}
    mod = 4 ** depth
    adj = {y: [] for y in verts}
    edges = []
    for i, y in enumerate(verts):
        for z in verts[i + 1:]:
            if sign[y] == sign[z]:
                continue
            x = y ^ z
            if x == 0 or x & (x - 1):
                continue
            if x.bit_length() - 1 < 2 * depth:
                continue
            if y % mod != z % mod:
                raise OracleMismatchError("edge joins distinct residues")
            edges.append((y, z))
            adj[y].append(z)
            adj[z].append(y)
    for y in verts:
        adj[y].sort()
    return verts, sign, adj, edges
def connected_components(verts, adj):
    seen = {}
    comps = []
    for y in verts:
        if y in seen:
            continue
        stack, comp = [y], []
        seen[y] = True
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen[v] = True
                    stack.append(v)
        comps.append(sorted(comp))
    return comps
def max_bipartite_matching(left, adj_left):
    match_r = {}
    def dfs(u, seen):
        for v in adj_left[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in match_r or dfs(match_r[v], seen):
                match_r[v] = u
                return True
        return False
    for u in left:
        dfs(u, set())
    return {u: v for v, u in match_r.items()}, match_r
def brute_max_matching_size(left, adj_left):
    order = list(left)
    best = [0]
    used = set()
    def rec(i, n):
        if n + (len(order) - i) <= best[0]:
            return
        if i == len(order):
            best[0] = max(best[0], n)
            return
        rec(i + 1, n)
        for v in adj_left[order[i]]:
            if v not in used:
                used.add(v)
                rec(i + 1, n + 1)
                used.discard(v)
    rec(0, 0)
    return best[0]
def hall_violator(small, large_set, adj, mate):
    mate_all = {}
    for u, v in mate.items():
        mate_all[u] = v
        mate_all[v] = u
    free = [u for u in small if u not in mate]
    seen, stack = set(free), list(free)
    while stack:
        u = stack.pop()
        u_small = u in small
        for v in adj[u]:
            if v in seen:
                continue
            if u_small and mate.get(u) == v:
                continue
            if not u_small and mate_all.get(u) != v:
                continue
            seen.add(v)
            stack.append(v)
    return sorted(u for u in seen if u in small)
def independent_hall_check(violator, edges):
    vset = set(violator)
    nbrs = set()
    for y, z in edges:
        if y in vset:
            nbrs.add(z)
        if z in vset:
            nbrs.add(y)
    return sorted(nbrs)
def independent_edge_set(belief, depth):
    vset = set(belief)
    sign = dict((y, 1 if c % 2 == 0 else -1) for y, c in belief.items())
    maxlen = max(vset).bit_length()
    out = set()
    for y in vset:
        for b in range(2 * depth, maxlen):
            z = y ^ (1 << b)
            if z != y and z in vset and sign[z] != sign[y]:
                out.add((y, z) if y < z else (z, y))
    return out
def independent_edge_set(belief, depth):
    pos = sorted(y for y, c in belief.items() if c % 2 == 0)
    neg = sorted(y for y, c in belief.items() if c % 2 == 1)
    out = set()
    for y in pos:
        for z in neg:
            x = y ^ z
            if x != 0 and x & (x - 1) == 0 and x.bit_length() - 1 >= 2 * depth:
                out.add((y, z) if y < z else (z, y))
    return out
def minimal_isolated_witness(belief, levels, complexity, depth, violator):
    y0 = min(violator)
    if y0 != 0x190825b:
        raise OracleMismatchError("theorem vertex changed")
    cost = belief[y0]
    masks = [format(m, "04b") for m in mask_sequence(levels, complexity - 1, y0, depth)]
    positives = sorted(y for y, c in belief.items() if c % 2 == 0)
    maxlen = max([y0] + positives, key=lambda v: v.bit_length()).bit_length()
    checked = 0
    for z in positives:
        x = y0 ^ z
        checked += 1
        if x != 0 and x & (x - 1) == 0 and x.bit_length() - 1 >= 2 * depth:
            raise OracleMismatchError("theorem vertex has a neighbor")
    return {"vertex_hex": hex(y0), "cost": cost, "sign": -1,
     "shadow_masks": masks, "bit_length": y0.bit_length(),
     "bits_checked": [2 * depth, maxlen - 1],
     "positives_checked": len(positives), "opposite_neighbors": 0}
def obstruction_evidence(levels, phase, k, cur, cut, gaps, depth, belief, stats):
    sched = forced_zero_schedule(cur, SCHEDULE_CAP)
    base = sched[:cut]
    word = return_extension(tuple(gaps), False)
    full = base + return_extension(tuple(gaps), True)
    if not sched[cut:].startswith(word) or not admissible(full):
        raise OracleMismatchError("occurrence word inconsistent")
    fresh = independent_edge_set(belief, depth)
    builtin = set()
    _, _, _, bedges = build_hamming_graph(belief, depth)
    for y, z in bedges:
        builtin.add((y, z) if y < z else (z, y))
    if fresh != builtin:
        raise OracleMismatchError("edge set mismatch")
    hv = stats["hall_violator"]
    viol = [int(h, 16) for h in hv["vertices_hex"]]
    wit = minimal_isolated_witness(belief, levels, k, depth, viol)
    return {"schedule": sched, "base_prefix": base, "extension_word_E": word,
     "full_word_admissible": True, "independent_edge_count": len(fresh),
     "edge_sets_match": True, "isolated_vertex": wit}
def three_return_occurrences(levels, maxK, cap, t0, check_time):
    pats = three_return_patterns()
    if len(pats) != 56:
        raise AssertionError("pattern count changed")
    occ = []
    truncated = 0
    excluded = 0
    for k in range(2, maxK + 1):
        for phase in PHASES:
            lv = levels[phase]
            for cur in sorted(lv[k]):
                if cur & 3 != 3:
                    continue
                try:
                    sched = forced_zero_schedule(cur, cap)
                except PairingLimitError:
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
                            excluded += 1
                            continue
                        if check_time and time.monotonic() - t0 > TIME_BUDGET_SECONDS:
                            raise PairingLimitError("time budget exceeded in occurrence scan")
                        occ.append((phase, k, cur, cut, tuple(gaps), L))
    return occ, truncated, excluded
def analyze_instance(belief, depth):
    verts, sign, adj, edges = build_hamming_graph(belief, depth)
    pos = sorted(y for y in verts if sign[y] == 1)
    neg = sorted(y for y in verts if sign[y] == -1)
    comps = connected_components(verts, adj)
    single_sign = sum(1 for c in comps if len({sign[y] for y in c}) == 1)
    if len(pos) <= len(neg):
        small, large = pos, neg
    else:
        small, large = neg, pos
    adj_small = {u: [v for v in adj[u] if v in set(large)] for u in small}
    mate_l, mate_r = max_bipartite_matching(small, adj_small)
    matched_small = len(mate_l)
    saturated = matched_small == len(small)
    out = {"vertices": len(verts), "positive": len(pos), "negative": len(neg),
     "edges": len(edges), "components": len(comps),
     "single_sign_components": single_sign, "matched_small": matched_small,
     "saturated": saturated, "signed_mass": len(pos) - len(neg)}
    if saturated:
        out["hall_violator"] = None
    else:
        viol = hall_violator(set(small), set(large), adj, mate_l)
        nbrs = independent_hall_check(viol, edges)
        if not (len(nbrs) < len(viol)):
            raise OracleMismatchError("Hall violator failed independent check")
        for u in viol:
            if u not in set(small):
                raise OracleMismatchError("violator outside small side")
        out["hall_violator"] = {"vertices_hex": [hex(u) for u in viol],
         "size": len(viol), "neighbor_hex": [hex(v) for v in nbrs],
         "neighbor_size": len(nbrs)}
    return out, edges
def sanity_checks():
    hands = [
        (["a"], ["x"], {"a": ["x"]}, 1),
        (["a"], ["x"], {"a": []}, 0),
        (["a", "b"], ["x"], {"a": ["x"], "b": ["x"]}, 1),
        (["a", "b"], ["x", "y"], {"a": ["x", "y"], "b": ["x", "y"]}, 2),
        (["a", "b"], ["x", "y"], {"a": ["x"], "b": ["x"]}, 1),
        (["a", "b", "c"], ["x", "y"], {"a": ["x"], "b": ["x", "y"], "c": ["y"]}, 2),
        (["a", "b", "c"], ["x", "y"], {"a": ["x"], "b": [], "c": ["y"]}, 2),
    ]
    for left, right, adj, want in hands:
        ml, _ = max_bipartite_matching(left, {u: list(adj[u]) for u in left})
        got = len(ml)
        if got != want or brute_max_matching_size(left, adj) != want:
            raise OracleMismatchError("hand matching case failed")
    n = 0
    for nl in (1, 2):
        for nr in (1, 2):
            L = ["L%d" % i for i in range(nl)]
            R = ["R%d" % j for j in range(nr)]
            pairs = [(u, v) for u in L for v in R]
            for mask in range(1 << len(pairs)):
                adj = {u: [] for u in L}
                for i, (u, v) in enumerate(pairs):
                    if mask >> i & 1:
                        adj[u].append(v)
                ml, _ = max_bipartite_matching(L, adj)
                if len(ml) != brute_max_matching_size(L, adj):
                    raise OracleMismatchError("exhaustive tiny matching mismatch")
                n += 1
    return {"hand_cases": len(hands), "exhaustive_tiny_graphs": n}
def git_strict(args):
    import subprocess as sp
    c = sp.run(["git", "-C", str(ROOT)] + args, capture_output=True, text=True, timeout=30)
    if c.returncode != 0:
        raise PairingLimitError("git failed: " + c.stderr.strip())
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
def run_campaign(dmax=DOMAIN_MAX_K, cap=SCHEDULE_CAP, check_time=True, enforcement=None):
    t0 = time.monotonic()
    if not 2 <= dmax <= 16:
        raise PairingLimitError("domain cap outside 2..16")
    if not 1 <= cap <= 64:
        raise PairingLimitError("schedule cap outside 1..64")
    levels = {ph: build_levels(ph, dmax, frontier_children_primary) for ph in PHASES}
    oracle_checked = 0
    for ph in PHASES:
        oc = build_levels(ph, min(ORACLE_K, dmax), oracle_frontier_children)
        for k in range(1, min(ORACLE_K, dmax) + 1):
            if oc[k] != levels[ph][k]:
                raise OracleMismatchError("oracle disagrees %s k=%d" % (ph, k))
            oracle_checked += len(levels[ph][k])
    sanity = sanity_checks()
    halt_reason = None
    complete = True
    occ, truncated, excluded = [], 0, 0
    rows = []
    belief_pair_checks = 0
    first_obstruction = None
    try:
        occ, truncated, excluded = three_return_occurrences(levels, dmax, cap, t0, check_time)
        if dmax == DOMAIN_MAX_K and len(occ) != EXPECTED_OCCURRENCES:
            raise PairingLimitError("occurrence count changed: %d" % len(occ))
        if truncated:
            complete = False
            halt_reason = "%d schedule(s) hit the cap: box unresolved" % truncated
        for phase, k, cur, cut, gaps, L in occ:
            if check_time and time.monotonic() - t0 > TIME_BUDGET_SECONDS:
                raise PairingLimitError("time budget exceeded in instance scan")
            lv = levels[phase]
            bel = belief_direct(lv, k, cur, L)
            if not bel:
                raise SeparationViolationError("empty belief at %s k=%d x=%s L=%d" % (phase, k, hex(cur), L))
            if 1 <= L <= k - 2 and bel != belief_recursive(lv, k, cur, L):
                raise OracleMismatchError("direct/recursive disagree at %s k=%d" % (phase, k))
            belief_pair_checks += 1
            stats, _ = analyze_instance(bel, L)
            mass = sum(1 if c % 2 == 0 else -1 for c in bel.values())
            if mass == 0:
                raise PairingLimitError("zero signed mass at %s k=%d x=%s" % (phase, k, hex(cur)))
            if stats["signed_mass"] != mass:
                raise OracleMismatchError("mass mismatch at %s k=%d" % (phase, k))
            rows.append({"phase": phase, "complexity": k, "state_hex": hex(cur),
             "cut": cut, "gaps": list(gaps), "depth": L, "endpoints": len(bel),
             "signed_mass": mass, "graph": stats})
            if not stats["saturated"]:
                rows[-1]["evidence"] = obstruction_evidence(lv, phase, k, cur, cut, gaps, L, bel, stats)
                first_obstruction = rows[-1]
                break
    except (PairingLimitError, SeparationViolationError) as exc:
        complete = False
        halt_reason = str(exc) if halt_reason is None else halt_reason + "; " + str(exc)
    runtime = time.monotonic() - t0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    tested = len(rows)
    pairing_exhausted = first_obstruction is None and tested == len(occ)
    if first_obstruction is not None:
        status = "refuted"
    elif complete and tested == len(occ):
        status = "finite-exhaustive"
    else:
        status = "inconclusive"
    result = {"occurrences": len(occ), "tested": tested,
     "truncated_schedules": truncated, "excluded_depth_ge_k": excluded,
     "belief_pair_checks": belief_pair_checks,
     "oracle_states_compared": oracle_checked, "sanity": sanity,
     "rows": rows, "first_obstruction": first_obstruction,
     "completed_through_cap": complete and pairing_exhausted, "halt_reason": halt_reason,
     "occurrence_domain_complete": complete, "pairing_search_exhausted": pairing_exhausted,
     "order": ["complexity ascending", "phase p then u", "state ascending",
      "cut ascending", "lexicographic gaps"],
     "stopping": "first obstruction or cap; no cap increase"}
    canon = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    gs = git_strict(["status", "--short"])
    if enforcement is None:
        enforcement = {"address_space_limit_applied": False,
         "reason": "no CLI enforcement record passed (library call)",
         "deadline": "cooperative monotonic budget checks when check_time is true"}
    payload = {"experiment_id": "signed-belief-hamming-pairing",
     "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
     "git_commit": git_strict(["rev-parse", "HEAD"]),
     "git_branch": git_strict(["branch", "--show-current"]),
     "git_status": gs, "git_dirty": bool(gs.strip()), "worktree": str(ROOT),
     "source_hashes": {"analyzer_sha256": sha256_file(Path(__file__).resolve())},
     "question": "problem1", "hypothesis": HYPOTHESIS, "backend": "python-direct-and-recursive",
     "parameters": {"domain_max_k": dmax, "schedule_cap": cap,
      "expected_occurrences": EXPECTED_OCCURRENCES, "oracle_k": ORACLE_K,
      "time_budget_seconds": TIME_BUDGET_SECONDS, "memory_budget_kib": MEMORY_BUDGET_KIB},
     "enforcement": enforcement, "hardware": hardware_facts(),
     "software": {"python_version": platform.python_version(),
      "python_implementation": platform.python_implementation(), "os": platform.platform()},
     "runtime_seconds": runtime, "peak_rss_kib": peak, "result": result,
     "result_hashes": {"certificate_sha256": hashlib.sha256(canon).hexdigest()},
     "result_summary": {"occurrences": len(occ), "tested": tested,
      "obstruction_found": first_obstruction is not None,
      "completed_through_cap": complete and pairing_exhausted,
      "occurrence_domain_complete": complete, "pairing_search_exhausted": pairing_exhausted},
     "interpretation": ("An obstruction refutes sign-reversing involutions with Hamming "
      "nonfixed pairs whose fixed set is nonempty of a common sign (equivalently: "
      "nonfixed pairs saturating the minority) on that occurrence only; the identity "
      "involution always exists. It does not refute arbitrary nonlocal pairings, "
      "signed nonvanishing, or Problem 1. Passage through the cap is finite "
      "evidence only."),
     "status": status,
     "proof_scope": "bounded box only: full three-return domain 2<=k<=%d" % dmax,
     "limitations": ["finite cap; the fixed-restricted Hamming class is refuted exactly "
      "by the recorded counterexample while arbitrary nonlocal pairings remain open",
      "single local process; cooperative 120s wall budget plus outer timeout; 1GiB cap in CLI runs",
      "occurrences with L>=k excluded by domain definition, counted not successes",
      "schedules hitting the cap force inconclusive, never exhaustive"]}
    try:
        payload["source_hashes"]["test_sha256"] = sha256_file(ROOT / TEST_RELATIVE)
    except OSError:
        pass
    return payload
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain-max", type=int, default=DOMAIN_MAX_K)
    ap.add_argument("--schedule-cap", type=int, default=SCHEDULE_CAP)
    ap.add_argument("--output", type=str, default=None)
    a = ap.parse_args()
    enforcement = apply_address_space_limit()
    if not enforcement["address_space_limit_applied"]:
        raise PairingLimitError("could not enforce the address-space cap")
    import signal as _sig
    def _alarm(signum, frame):
        raise PairingLimitError("wall-clock alarm: 115s budget reached")
    _sig.signal(_sig.SIGALRM, _alarm)
    enforcement["alarm_seconds"] = 115
    enforcement["deadline"] = "SIGALRM at 115s plus cooperative checks plus outer timeout"
    _sig.alarm(115)
    try:
        payload = run_campaign(a.domain_max, a.schedule_cap, True, enforcement)
    finally:
        _sig.alarm(0)
    dest = Path(a.output) if a.output else ROOT / "results/problem1" / RESULT_FILENAME
    res = dest.resolve()
    if not res.is_relative_to(ROOT):
        raise PairingLimitError("output outside worktree")
    write_record_atomic(payload, res)
    print(json.dumps(payload, indent=2, sort_keys=True))
if __name__ == "__main__":
    main()
