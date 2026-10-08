#!/usr/bin/env python3
"""Exact finite screen for a symbolic collision-segment reset candidate.

This does not extend the S_r depth sweep. It tests the stronger candidate
that the last-parent two raw halves have equal no-reset selectors between
consecutive upper-blind transitions. Both outcomes affect the proposed
all-depth proof bridge. Output is an atomic JSON file at an explicit path.
"""
import argparse
import base64
from collections import deque
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import tempfile
import time
import zlib

ROOT = Path(__file__).resolve().parents[2]


class DFA:
    """Complete DFA on the four ordered raw-pair letters x+2y."""
    def __init__(self, rows, accept, start=0):
        self.rows = tuple(tuple(row) for row in rows)
        self.accept = frozenset(accept)
        self.start = start

    def minimal(self):
        reachable, todo = {self.start: 0}, [self.start]
        for s in todo:
            for t in self.rows[s]:
                if t not in reachable:
                    reachable[t] = len(reachable)
                    todo.append(t)
        rows = [[reachable[t] for t in self.rows[s]] for s in todo]
        flags = [s in self.accept for s in todo]
        blocks = [int(flag) for flag in flags]
        while True:
            classes = {}
            new = []
            for s, row in enumerate(rows):
                signature = (flags[s], *(blocks[t] for t in row))
                if signature not in classes:
                    classes[signature] = len(classes)
                new.append(classes[signature])
            if new == blocks:
                break
            blocks = new
        reps = [blocks.index(c) for c in range(max(blocks)+1)]
        quotient = [[blocks[t] for t in rows[s]] for s in reps]
        qflags = [flags[s] for s in reps]
        order, ids = [blocks[0]], {blocks[0]: 0}
        for s in order:
            for t in quotient[s]:
                if t not in ids:
                    ids[t] = len(ids)
                    order.append(t)
        return DFA([[ids[t] for t in quotient[s]] for s in order],
                   [ids[s] for s in order if qflags[s]])

    def combine(self, other, mode):
        initial = (self.start, other.start)
        states, ids, rows, acc = [initial], {initial: 0}, [], []
        for s, t in states:
            if ((s in self.accept or t in other.accept) if mode == "union" else
                (s in self.accept and t in other.accept)):
                acc.append(ids[(s, t)])
            row = []
            for letter in range(4):
                nxt = (self.rows[s][letter], other.rows[t][letter])
                if nxt not in ids:
                    ids[nxt] = len(ids)
                    states.append(nxt)
                row.append(ids[nxt])
            rows.append(row)
        return DFA(rows, acc).minimal()

    def filter_last(self, letters):
        # A two-state DFA recording only whether the last letter is allowed.
        rows = [[int(c in letters) for c in range(4)]]*2
        return self.combine(DFA(rows, [1]), "intersection")

    def filter_diagonal(self):
        return self.combine(DFA([[0, 1, 1, 0], [1, 1, 1, 1]], [0]), "intersection")

    def witness(self):
        prior, todo = {self.start: None}, deque([self.start])
        end = None
        while todo:
            s = todo.popleft()
            if s in self.accept:
                end = s
                break
            for letter, t in enumerate(self.rows[s]):
                if t not in prior:
                    prior[t] = (s, letter)
                    todo.append(t)
        if end is None:
            return None
        word = []
        while prior[end] is not None:
            end, letter = prior[end]
            word.append(letter)
        return word[::-1]

    def raw_image(self, state_cap, deadline):
        """Exact simultaneous raw update, union over complementary q=0/1."""
        initial = frozenset((self.start, 3, q | ((q ^ 1) << 1)) for q in (0, 1))
        subsets, ids, rows, acc = [initial], {initial: 0}, [], []
        for subset in subsets:
            if time.monotonic() > deadline:
                raise RuntimeError("regular closure wall-time cap exceeded")
            if any(s in self.accept for s, _, _ in subset):
                acc.append(ids[subset])
            successors = [set() for _ in range(4)]
            for s, h, l in subset:
                for x in range(4):
                    out0 = (h & 1) ^ ((l & 1) | (x & 1))
                    out1 = ((h >> 1) & 1) ^ (((l >> 1) & 1) | ((x >> 1) & 1))
                    letter = out0 | (out1 << 1)
                    successors[letter].add((self.rows[s][x], l, x))
            row = []
            for successor in successors:
                nxt = frozenset(successor)
                if nxt not in ids:
                    if len(ids) >= state_cap:
                        raise RuntimeError("regular image subset-state cap exceeded")
                    ids[nxt] = len(ids)
                    subsets.append(nxt)
                row.append(ids[nxt])
            rows.append(row)
        return DFA(rows, acc).minimal(), len(subsets)

    def raw_preimage(self, state_cap, deadline):
        """Exact raw preimage; boundary choice is the only nondeterminism."""
        initial = frozenset((self.start, 3, q | ((q ^ 1) << 1)) for q in (0, 1))
        subsets, ids, rows, acc = [initial], {initial: 0}, [], []
        for subset in subsets:
            if time.monotonic() > deadline:
                raise RuntimeError("regular preimage wall-time cap exceeded")
            if any(s in self.accept for s, _, _ in subset):
                acc.append(ids[subset])
            row = []
            for x in range(4):
                successor = set()
                for s, h, l in subset:
                    out0 = (h & 1) ^ ((l & 1) | (x & 1))
                    out1 = ((h >> 1) & 1) ^ (((l >> 1) & 1) | ((x >> 1) & 1))
                    letter = out0 | (out1 << 1)
                    successor.add((self.rows[s][letter], l, x))
                nxt = frozenset(successor)
                if nxt not in ids:
                    if len(ids) >= state_cap:
                        raise RuntimeError("regular preimage state cap exceeded")
                    ids[nxt] = len(ids)
                    subsets.append(nxt)
                row.append(ids[nxt])
            rows.append(row)
        return DFA(rows, acc).minimal(), len(subsets)

    def signature(self):
        return self.rows, tuple(sorted(self.accept))

    def record(self):
        result = {"start": self.start, "rows": self.rows, "accept": sorted(self.accept)}
        if len(self.rows) > 128:
            raw = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
            return {"encoding": "base64 zlib-compressed UTF8 canonical JSON of start,rows,accept",
                    "states": len(self.rows), "uncompressed_bytes": len(raw),
                    "uncompressed_sha256": hashlib.sha256(raw).hexdigest(),
                    "base64_zlib": base64.b64encode(zlib.compress(raw, 9)).decode()}
        return result

    def widen(self, rounds, state_cap, deadline):
        """Sound overapproximation by merging finite-lookahead residuals.

        The quotient is an NFA. Every original run maps to a quotient run;
        hence determinization cannot discard an original accepted word.
        Empty/dead residuals stay separate, preserving prefix viability.
        """
        # Mark states having some accepted continuation, to avoid merging dead
        # states with merely distant accepting continuations.
        live = set(self.accept)
        reverse = [[] for _ in self.rows]
        for s, row in enumerate(self.rows):
            for t in row:
                reverse[t].append(s)
        todo = list(live)
        for t in todo:
            for s in reverse[t]:
                if s not in live:
                    live.add(s)
                    todo.append(s)
        ids = {}
        blocks = []
        for s in range(len(self.rows)):
            sig = (s in self.accept, s in live)
            if sig not in ids:
                ids[sig] = len(ids)
            blocks.append(ids[sig])
        for _ in range(rounds):
            ids, new = {}, []
            for s, row in enumerate(self.rows):
                sig = (s in self.accept, s in live, *(blocks[t] for t in row))
                if sig not in ids:
                    ids[sig] = len(ids)
                new.append(ids[sig])
            blocks = new
        nfa = [[set() for _ in range(4)] for _ in range(max(blocks)+1)]
        accept = {blocks[s] for s in self.accept}
        for s, row in enumerate(self.rows):
            for c, t in enumerate(row):
                nfa[blocks[s]][c].add(blocks[t])
        initial = frozenset([blocks[self.start]])
        subsets, ids, rows, acc = [initial], {initial: 0}, [], []
        for subset in subsets:
            if time.monotonic() > deadline:
                raise RuntimeError("widening wall-time cap exceeded")
            if subset & accept:
                acc.append(ids[subset])
            row = []
            for letter in range(4):
                nxt = frozenset(t for s in subset for t in nfa[s][letter])
                if nxt not in ids:
                    if len(ids) >= state_cap:
                        raise RuntimeError("widening subset-state cap exceeded")
                    ids[nxt] = len(ids)
                    subsets.append(nxt)
                row.append(ids[nxt])
            rows.append(row)
        return DFA(rows, acc).minimal()


def common_postblind_language(canonical=False):
    # Derive the two-row preimage NFA independently from the raw truth table.
    initial = frozenset([(3, 2, 0)])  # preceding pairs (1,1),(0,1)
    subsets, ids, rows, acc = [initial], {initial: 0}, [], []
    for subset in subsets:
        if subset:
            acc.append(ids[subset])
        successors = [set() for _ in range(4)]
        for h, l, prefix in subset:
            allowed = ({1} if prefix == 0 else {0} if prefix == 1 else
                       {1, 2} if prefix == 2 else range(4)) if canonical else range(4)
            for x in allowed:
                out0 = (h & 1) ^ ((l & 1) | (x & 1))
                out1 = ((h >> 1) & 1) ^ (((l >> 1) & 1) | ((x >> 1) & 1))
                if out0 == out1:
                    successors[3*out0].add((l, x, min(prefix+1, 3)))
        row = []
        for successor in successors:
            nxt = frozenset(successor)
            if nxt not in ids:
                ids[nxt] = len(ids)
                subsets.append(nxt)
            row.append(ids[nxt])
        rows.append(row)
    # Length at least two; designated last half must initially be zero.
    length = DFA([[1]*4, [2]*4, [2]*4], [2])
    return DFA(rows, acc).minimal().combine(length, "intersection").filter_last({0})


def backward_screen(start_time, time_cap, iterations, state_cap, widening, canonical):
    initial = common_postblind_language(canonical)
    length = DFA([[1]*4, [2]*4, [2]*4], [2])
    diagonal = DFA([[0, 1, 1, 0], [1, 1, 1, 1]], [0]).combine(length, "intersection")
    one, _ = diagonal.raw_preimage(state_cap, start_time+time_cap)
    one = one.filter_last({0, 2})
    zero = DFA([[0]*4], [])
    history = []
    status = "inconclusive"
    bad_word = None
    for iteration in range(iterations):
        bad_word = zero.combine(initial, "intersection").witness()
        entry = {"iteration": iteration, "unsafe_without_other_reset_states": len(zero.rows),
                 "unsafe_after_other_reset_states": len(one.rows), "bad_initial_word": bad_word}
        history.append(entry)
        if bad_word is not None:
            status = "counterexample-candidate"
            break
        try:
            pre0, states0 = zero.raw_preimage(state_cap, start_time+time_cap)
            pre1, states1 = one.raw_preimage(state_cap, start_time+time_cap)
            pre_new1, states_new1 = one.filter_last({2}).raw_preimage(state_cap, start_time+time_cap)
            next0 = zero.combine(pre0.filter_last({0}), "union").combine(pre_new1.filter_last({0}), "union")
            next1 = one.combine(pre1.filter_last({0, 2}), "union")
            if widening >= 0:
                next0 = next0.widen(widening, state_cap, start_time+time_cap).filter_last({0}).combine(length, "intersection")
                next1 = next1.widen(widening, state_cap, start_time+time_cap).filter_last({0, 2}).combine(length, "intersection")
        except (RuntimeError, MemoryError) as exc:
            entry["resource_stop"] = str(exc) or "MemoryError"
            break
        entry.update({"pre0_states": states0, "pre1_states": states1,
                      "pre_new_reset_states": states_new1,
                      "next0_states": len(next0.rows), "next1_states": len(next1.rows)})
        if next0.signature() == zero.signature() and next1.signature() == one.signature():
            status = "closed-invariant-candidate"
            break
        zero, one = next0, next1
    return {"mode": "backward-regular-language-closure", "status": status,
            "alphabet": "raw pair x+2*y; x is the designated no-reset half",
            "initial_language": initial.record(), "no_other_reset_language": zero.record(),
            "other_reset_language": one.record(), "iterations": history,
            "canonical_blind_prefix": canonical,
            "widening_lookahead_rounds": widening, "last_bad_word": bad_word}


def regular_screen(start_time, time_cap, iterations, state_cap, widening, canonical):
    zero = common_postblind_language(canonical)
    one = DFA([[0]*4], [])
    initial = zero
    history = []
    status = "inconclusive"
    bad_word = None
    for iteration in range(iterations):
        try:
            image0, subset0 = zero.raw_image(state_cap, start_time+time_cap)
            image1, subset1 = one.raw_image(state_cap, start_time+time_cap)
        except (RuntimeError, MemoryError) as exc:
            history.append({"iteration": iteration,
                            "no_other_reset_dfa_states": len(zero.rows),
                            "other_reset_dfa_states": len(one.rows),
                            "resource_stop": str(exc) or "MemoryError"})
            break
        bad = image1.filter_diagonal()
        bad_word = bad.witness()
        entry = {"iteration": iteration, "no_other_reset_dfa_states": len(zero.rows),
                 "other_reset_dfa_states": len(one.rows),
                 "image0_subset_states": subset0, "image1_subset_states": subset1,
                 "image0_minimal_states": len(image0.rows), "image1_minimal_states": len(image1.rows),
                 "bad_return_word": bad_word}
        history.append(entry)
        if bad_word is not None:
            status = "counterexample-candidate"
            break
        next0 = zero.combine(image0.filter_last({0}), "union")
        next1 = one.combine(image0.filter_last({2}), "union").combine(
            image1.filter_last({0, 2}), "union")
        if widening >= 0:
            try:
                next0 = next0.widen(widening, state_cap, start_time+time_cap).filter_last({0})
                next1 = next1.widen(widening, state_cap, start_time+time_cap).filter_last({0, 2})
            except (RuntimeError, MemoryError) as exc:
                entry["resource_stop"] = str(exc) or "MemoryError"
                break
        entry["next0_states"], entry["next1_states"] = len(next0.rows), len(next1.rows)
        if next0.signature() == zero.signature() and next1.signature() == one.signature():
            status = "closed-invariant-candidate"
            break
        zero, one = next0, next1
    return {"mode": "regular-language-closure", "status": status,
            "alphabet": "raw pair x+2*y; x is the designated no-reset half",
            "initial_language": initial.record(), "no_other_reset_language": zero.record(),
            "other_reset_language": one.record(), "iterations": history,
            "canonical_blind_prefix": canonical,
            "widening_lookahead_rounds": widening, "last_bad_word": bad_word}


def transition(state, label, depth):
    rows = [(1, 0), (0, 1)] + [
        ((state >> (2*j)) & 1, (state >> (2*j+1)) & 1)
        for j in range(depth)
    ]
    out = 0
    for j in range(depth):
        h, l, x = rows[j:j+3]
        f = h[0] ^ (l[0] | x[0])
        d = h[1] ^ l[1] ^ (l[1] & x[0]) ^ ((1 ^ l[0] ^ l[1]) & x[1])
        out |= (f ^ (label & d)) << (2*j)
        out |= d << (2*j+1)
    return out


def independent_transition(state, label, depth):
    a = [1, 0] + [(state >> (2*j)) & 1 for j in range(depth)]
    b = [1, 1] + [((state >> (2*j)) ^ (state >> (2*j+1))) & 1 for j in range(depth)]
    aa = [a[j] ^ (a[j+1] | a[j+2]) for j in range(depth)]
    bb = [b[j] ^ (b[j+1] | b[j+2]) for j in range(depth)]
    out = 0
    for j, (x, z) in enumerate(zip(aa, bb)):
        d = x ^ z
        out |= (x ^ (label & d)) << (2*j)
        out |= d << (2*j+1)
    return out


def shallow_proof_controls():
    """Tiny finite truth-table controls for the separately stated hand proof."""
    table = [[independent_transition(u, a, 2) for a in (0, 1)] for u in range(16)]
    cyclic = []
    for u in range(16):
        reached = set(table[u])
        todo = deque(reached)
        while todo:
            v = todo.popleft()
            for w in table[v]:
                if w not in reached:
                    reached.add(w)
                    todo.append(w)
        if u in reached:
            cyclic.append(u)
    assert cyclic == [2, 3, 4, 7, 10, 12, 15]
    assert [u for u in range(16) if table[u][0] == table[u][1]] == [3, 15]
    reset_cases = 0
    for label in (0, 1):
        for child in range(4):
            value = independent_transition(4 | (child << 4), label, 3)
            assert ((value >> 4) & 3) == 1
            reset_cases += 1
    forced_prefix_cases = 0
    for u in range(1 << 10):
        if (u & 63) not in (35, 51):
            continue
        v = independent_transition(u, 0, 5)
        if v != independent_transition(u, 1, 5):
            continue
        assert ((v >> 6) & 3) == 1
        assert ((v >> 8) & 3) == 1
        forced_prefix_cases += 1
    return {"depth_two_transition_table": table, "depth_two_cyclic_states": cyclic,
            "depth_two_blind_states": [3, 15], "layer_three_A_reset_cases": reset_cases,
            "depth_five_canonical_blind_sources_checked": forced_prefix_cases,
            "depth_four_and_five_postblind_parent_pair": [1, 0],
            "status": "finite-exhaustive",
            "scope": "Small independent raw truth-table controls; all-period S4/S5 follows from the hand proof, not from these counts."}


def upper_components(t0, t1):
    size = len(t0)
    seen = bytearray(size)
    order = []
    for root in range(size):
        if seen[root]:
            continue
        seen[root] = 1
        work = [(root, 0)]
        while work:
            u, edge = work[-1]
            if edge == 2:
                order.append(u)
                work.pop()
                continue
            work[-1] = (u, edge+1)
            v = t1[u] if edge else t0[u]
            if not seen[v]:
                seen[v] = 1
                work.append((v, 0))
    reverse = [[] for _ in range(size)]
    for u in range(size):
        reverse[t0[u]].append(u)
        reverse[t1[u]].append(u)
    comp = [-1]*size
    sizes = []
    for root in reversed(order):
        if comp[root] != -1:
            continue
        c = len(sizes)
        comp[root] = c
        work = [root]
        for u in work:
            for v in reverse[u]:
                if comp[v] == -1:
                    comp[v] = c
                    work.append(v)
        sizes.append(len(work))
    return comp, sizes


def screen(depth, start_time, time_cap, cyclic=False, canonical=False):
    size = 1 << (2*depth)
    t0 = [transition(u, 0, depth) for u in range(size)]
    t1 = [transition(u, 1, depth) for u in range(size)]
    for u in range(size):
        assert t0[u] == independent_transition(u, 0, depth)
        assert t1[u] == independent_transition(u, 1, depth)
    blind = {u for u in range(size) if t0[u] == t1[u]}
    all_blind = blind
    if canonical and depth >= 3:
        blind = {u for u in blind if (u & 63) in (35, 51)}
    if cyclic:
        comp, sizes = upper_components(t0, t1)
        blind = {u for u in blind if comp[u] == comp[t0[u]] and
                 (sizes[comp[u]] > 1 or t0[u] == u)}
    roots = sorted({t0[u] for u in blind})
    assert all((u & 15) == 4 for u in roots) if depth >= 2 else True
    # Keys are (upper_state, gauge_q, two no-reset selector bits).
    prev = {(u, 0, 3): None for u in roots}
    queue = deque(prev)
    end_checks = 0
    witness = None
    while queue:
        if time.monotonic() - start_time > time_cap:
            raise RuntimeError("wall-time cap exceeded")
        key = queue.popleft()
        u, q, selectors = key
        l = (u >> (2*(depth-1))) & 1
        m = (u >> (2*(depth-1)+1)) & 1
        raw0 = l ^ (q & m)
        raw1 = l ^ ((q ^ 1) & m)
        next_selectors = selectors & ((1-raw0) | ((1-raw1) << 1))
        if u in all_blind:
            end_checks += 1
            if next_selectors in (1, 2):
                witness = (key, next_selectors)
                break
            continue
        for a in (0, 1):
            v = t1[u] if a else t0[u]
            if cyclic and comp[u] != comp[v]:
                continue
            nxt = (v, q ^ a, next_selectors)
            if nxt not in prev:
                prev[nxt] = (key, a)
                queue.append(nxt)
    result = {"depth": depth, "upper_states": size, "blind_states": len(all_blind),
              "eligible_blind_starts": len(blind), "cyclic_upper_only": cyclic,
              "canonical_blind_prefix": canonical,
              "postblind_states": len(roots), "reachable_selector_states": len(prev),
              "consecutive_blind_end_checks": end_checks,
              "transition_controls": 2*size,
              "candidate_refuted": witness is not None}
    if witness:
        key, selectors = witness
        keys, labels = [key], []
        while prev[key] is not None:
            p, a = prev[key]
            labels.append(a)
            keys.append(p)
            key = p
        keys.reverse()
        labels.reverse()
        origin = keys[0][0]
        preblind = next(u for u in sorted(blind) if t0[u] == origin)
        # Append any terminal label; upper blind output does not depend on it.
        labels.append(0)
        terminal = transition(keys[-1][0], 0, depth)
        result["witness"] = {"preblind_state": preblind,
                             "segment_upper_states": [k[0] for k in keys] + [terminal],
                             "segment_labels": labels,
                             "gauges_at_inputs": [k[1] for k in keys],
                             "no_reset_selectors_after_terminal_blind": selectors}
        # Independently run raw half rows and verify exact reset products.
        a = [1, 0] + [(origin >> (2*j)) & 1 for j in range(depth)]
        b = [1, 1] + [((origin >> (2*j)) ^ (origin >> (2*j+1))) & 1 for j in range(depth)]
        q = 0
        ds = [1, 1]
        raw_history = []
        for step, label in enumerate(labels):
            a[1], b[1] = q, q ^ 1
            ds[0] &= 1-a[-1]
            ds[1] &= 1-b[-1]
            raw_history.append([a[2:], b[2:]])
            aa = [a[j] ^ (a[j+1] | a[j+2]) for j in range(depth)]
            bb = [b[j] ^ (b[j+1] | b[j+2]) for j in range(depth)]
            a, b = [1, 0]+aa, [1, 1]+bb
            q ^= label
            normalized = sum(((x ^ (q & (x ^ z))) << (2*j)) |
                             ((x ^ z) << (2*j+1)) for j, (x, z) in enumerate(zip(aa, bb)))
            assert normalized == result["witness"]["segment_upper_states"][step+1]
        assert ds[0] | (ds[1] << 1) == selectors
        assert a[2:] == b[2:]
        result["witness"]["independent_raw_rows_at_inputs"] = raw_history
        result["witness"]["independent_raw_selectors"] = ds
        # Realize the nonzero swap amplitude with two actual added copies.
        # At the initial blind use labels0/1 and a common child(0,0).
        ua, ub = preblind, preblind
        product = []
        for label_a, label_b in [(0, 1)] + [(a, a) for a in labels]:
            va = transition(ua, label_a, depth+1)
            vb = transition(ub, label_b, depth+1)
            assert va == independent_transition(ua, label_a, depth+1)
            assert vb == independent_transition(ub, label_b, depth+1)
            mask = (1 << (2*depth))-1
            assert (ua & mask) == (ub & mask)
            assert (va & mask) == (vb & mask)
            u = ua & mask
            bad = (u in blind and label_a == label_b and
                   ((va >> (2*depth+1)) & 1) != ((vb >> (2*depth+1)) & 1))
            product.append({"upper_state": u,
                            "child_A": (ua >> (2*depth)) & 3,
                            "child_B": (ub >> (2*depth)) & 3,
                            "labels": [label_a, label_b],
                            "upper_next": va & mask,
                            "child_A_next": (va >> (2*depth)) & 3,
                            "child_B_next": (vb >> (2*depth)) & 3,
                            "bad": bad})
            ua, ub = va, vb
        assert product[-1]["bad"]
        result["witness"]["actual_product_replay"] = product
        # Independently check why this finite path cannot become a cycle:
        # exhibit a complete forward-closed upper set containing its end
        # and excluding its postblind start and preblind source.
        reached, todo = {terminal}, deque([terminal])
        while todo:
            u = todo.popleft()
            for v in (t0[u], t1[u]):
                if v not in reached:
                    reached.add(v)
                    todo.append(v)
        assert all(t0[u] in reached and t1[u] in reached for u in reached)
        result["witness"]["upper_end_forward_closed_set"] = sorted(reached)
        result["witness"]["can_return_to_postblind_start"] = origin in reached
        result["witness"]["can_return_to_preblind_source"] = preblind in reached
        # Actual two-child replay, not an arbitrary-amplitude approximation.
        actual = []
        for seed in range(4):
            aa = preblind | (seed << (2*depth))
            bb = aa
            phase_rows = []
            outputs = [transition(aa, 0, depth+1), transition(bb, 1, depth+1)]
            assert outputs[0] == independent_transition(aa, 0, depth+1)
            assert outputs[1] == independent_transition(bb, 1, depth+1)
            mask = (1 << (2*depth))-1
            assert (outputs[0] & mask) == (outputs[1] & mask) == origin
            aa, bb = outputs
            phase_rows.append([origin, (aa >> (2*depth)) & 3, (bb >> (2*depth)) & 3])
            for label in labels:
                out_a = transition(aa, label, depth+1)
                out_b = transition(bb, label, depth+1)
                assert out_a == independent_transition(aa, label, depth+1)
                assert out_b == independent_transition(bb, label, depth+1)
                aa, bb = out_a, out_b
                assert (aa & mask) == (bb & mask)
                phase_rows.append([aa & mask, (aa >> (2*depth)) & 3, (bb >> (2*depth)) & 3])
            actual.append({"common_initial_child": seed,
                           "initial_labels": [0, 1], "subsequent_common_labels": labels,
                           "upper_childA_childB_after_each_edge": phase_rows,
                           "final_added_output_y_difference": ((aa ^ bb) >> (2*depth+1)) & 1})
        result["witness"]["actual_product_replays_all_four_common_child_seeds"] = actual
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=6)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--time-cap", type=float, default=30)
    parser.add_argument("--regular", action="store_true")
    parser.add_argument("--backward", action="store_true")
    parser.add_argument("--iterations", type=int, default=8)
    parser.add_argument("--state-cap", type=int, default=4096)
    parser.add_argument("--widening", type=int, default=-1)
    parser.add_argument("--canonical-prefix", action="store_true")
    parser.add_argument("--cyclic-only", action="store_true")
    args = parser.parse_args()
    if not 2 <= args.depth <= 8:
        parser.error("this hypothesis screen admits only depths 2 through 8")
    resource.setrlimit(resource.RLIMIT_AS, (128*1024*1024, 128*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
    start = time.monotonic()
    record = {
        "experiment_id": "20261008-blind-return-segment-r"+str(args.depth),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "equal two raw last-parent no-reset selectors between any consecutive depth-r blind transitions, starting in a genuine postblind state",
        "backend": "independent-python-polynomial-and-two-raw-row",
        "parameters": {"depth": args.depth, "wall_time_cap_seconds": args.time_cap,
                       "address_space_cap_bytes": 128*1024*1024,
                       "cpu_time_cap_seconds": 60,
                       "output_cap_bytes": 262144,
                       "cyclic_upper_only": args.cyclic_only,
                       "canonical_blind_prefix": args.canonical_prefix,
                       "complete_finite_selector_state_closure": True},
        "hardware": {"machine": platform.machine(), "processor": platform.processor(),
                     "logical_cpu_count": os.cpu_count()},
        "software": {"python": sys.version, "platform": platform.platform()},
        "result_hashes": {"source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
    }
    if args.regular or args.backward:
        record["experiment_id"] = ("20261008-blind-return-backward" if args.backward else
                                   "20261008-blind-return-regular") + ("-canonical" if args.canonical_prefix else "-unrestricted")
        record["backend"] = "exact-Python-word-transducer/subset/minimization with independent raw shallow controls"
        result = (backward_screen if args.backward else regular_screen)(
            start, args.time_cap, args.iterations, args.state_cap, args.widening,
            args.canonical_prefix)
        record["hypothesis"] = "equal last-parent raw reset selectors between consecutive upper collisions, at every word length, checked by exact regular-language reachability"
        record["parameters"].update({"regular_iterations": args.iterations,
                                     "subset_state_cap": args.state_cap,
                                     "widening_lookahead_rounds": args.widening,
                                     "canonical_blind_prefix": args.canonical_prefix,
                                     "depth": "unbounded spatial word length"})
    else:
        result = screen(args.depth, start, args.time_cap, args.cyclic_only,
                        args.canonical_prefix)
    record["result_summary"] = result
    record["runtime_seconds"] = time.monotonic()-start
    record["status"] = ("inconclusive" if args.regular or args.backward else
                        "refuted" if result["candidate_refuted"] else "finite-exhaustive")
    record["proof_scope"] = ("Exact finite automata at all spatial word lengths; only the listed finite number of temporal image/preimage stages were completed, and no inductive closure was obtained."
                             if args.regular or args.backward else
                             "Exact finite collision-segment graph at the stated observer depth; explicit transient product path and independent raw replay.")
    record["interpretation"] = ("Exact regular-language exploration requires an independently checked inductive closure certificate or a replayed segment witness."
                               if args.regular or args.backward else
                               "The stronger noncyclic segment law is false; cyclic eligibility must still be checked."
                               if result["candidate_refuted"] else
                               "No unequal segment selectors exist at this one finite depth; no all-depth inference.")
    record["limitations"] = ["Does not prove S_r at all depths.",
                              "A transient segment witness is not a cyclic-product counterexample.",
                              "Does not settle global original-support transport or Problem 1."]
    record["shallow_hand_proof_controls"] = shallow_proof_controls()
    record["result_hashes"]["immutable_reference_sha256"] = hashlib.sha256(
        (ROOT / "src/python/rule30_research_reference.py").read_bytes()).hexdigest()
    assert record["result_hashes"]["immutable_reference_sha256"] == "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
    record["runtime_seconds"] = time.monotonic()-start
    record["peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    record["result_hashes"]["payload_without_payload_hash_sha256"] = hashlib.sha256(payload).hexdigest()
    data = (json.dumps(record, sort_keys=True, indent=2)+"\n").encode()
    assert len(data) <= 262144
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=args.out.name+".", suffix=".tmp", dir=args.out.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, args.out)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    summary = ({key: value for key, value in result.items() if key not in
                {"initial_language", "no_other_reset_language", "other_reset_language"}}
               if args.regular or args.backward else result)
    print(json.dumps({"status": record["status"], "result_summary": summary,
                      "runtime_seconds": record["runtime_seconds"], "output": str(args.out)}))


if __name__ == "__main__":
    main()
