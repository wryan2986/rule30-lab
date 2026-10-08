#!/usr/bin/env python3
"""Exact output-language automaton for a normalized blind transition.

Admission: a depth-independent description of postblind equal rows may prove
the return-to-blind double-reset lemma. An obstruction in this language fences
off that proof mechanism. This constructs an exact finite transducer; it does
not increase a temporal/connector census or assert any infinite nonperiodicity.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20261008_blind_image_language.json"
START = time.monotonic()
LIMIT = 256 * 1024 * 1024


def f(a: int, b: int, c: int) -> int:
    return a ^ (b | c)


def encode(a: int, b: int, c: int, d: int) -> int:
    return a | (b << 1) | (c << 2) | (d << 3)


def decode(s: int) -> tuple[int, int, int, int]:
    return tuple((s >> j) & 1 for j in range(4))


def normalized_step(s: int, r: int) -> int:
    pairs = [(1, 0), (0, 1)] + [((s >> (2*j)) & 1, (s >> (2*j+1)) & 1) for j in range(r)]
    ans = 0
    for j in range(r):
        h, l, x = pairs[j:j+3]
        xx = h[0] ^ (l[0] | x[0])
        yy = h[1] ^ l[1] ^ x[1] ^ (l[0] & x[1]) ^ (l[1] & x[0]) ^ (l[1] & x[1])
        ans |= xx << (2*j)
        ans |= yy << (2*j+1)
    return ans


def main() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
    # State (a_(j-2),b_(j-2),a_(j-1),b_(j-1)). Outputs of the
    # two raw rows must agree. All 16 contexts are accepting at finite depth.
    nfa = [[set(), set()] for _ in range(16)]
    transitions = []
    for s in range(16):
        h, hh, l, ll = decode(s)
        for x in (0, 1):
            for xx in (0, 1):
                c = f(h, l, x)
                if c != f(hh, ll, xx):
                    continue
                t = encode(l, ll, x, xx)
                nfa[s][c].add(t)
                transitions.append([s, x, xx, c, t])
    initial = frozenset([encode(1, 1, 0, 1)])
    subsets = [initial]
    ids = {initial: 0}
    dfa = []
    todo = deque([initial])
    while todo:
        ss = todo.popleft()
        row = []
        for c in (0, 1):
            tt = frozenset(t for s in ss for t in nfa[s][c])
            if tt not in ids:
                ids[tt] = len(subsets)
                subsets.append(tt)
                todo.append(tt)
            row.append(ids[tt])
        dfa.append(row)
    # Moore refinement: finite-word acceptance is nonempty subset.
    block = [int(bool(ss)) for ss in subsets]
    while True:
        signatures = [(bool(subsets[i]), *(block[t] for t in dfa[i])) for i in range(len(subsets))]
        keys = {s: k for k, s in enumerate(sorted(set(signatures)))}
        new = [keys[s] for s in signatures]
        if all((block[i] == block[j]) == (new[i] == new[j]) for i in range(len(new)) for j in range(len(new))):
            block = new
            break
        block = new
    classes = sorted(set(block))
    reps = [block.index(c) for c in classes]
    quotient = [[block[t] for t in dfa[i]] for i in reps]
    # Reindex minimized states by BFS from the start for readable provenance.
    start_class = block[0]
    order = [start_class]
    for c in order:
        for t in quotient[c]:
            if t not in order:
                order.append(t)
    qid = {c: i for i, c in enumerate(order)}
    small = [[qid[t] for t in quotient[c]] for c in order]
    accept = [bool(subsets[reps[c]]) for c in order]
    assert len(order) == len(classes)
    controls = []
    for r in range(1, 9):
        literal = set()
        blind_count = 0
        ymask = sum(1 << (2*j+1) for j in range(r))
        for s in range(1 << (2*r)):
            t = normalized_step(s, r)
            if not (t & ymask):
                blind_count += 1
                literal.add(sum(((t >> (2*j)) & 1) << j for j in range(r)))
        accepted = set()
        for word in range(1 << r):
            st = 0
            for j in range(r):
                st = small[st][(word >> j) & 1]
            if accept[st]:
                accepted.add(word)
        assert accepted == literal, (r, accepted ^ literal)
        controls.append({"r": r, "blind_sources": blind_count, "distinct_common_images": len(literal)})
    reference = ROOT / "src/python/rule30_research_reference.py"
    ref_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
    assert ref_hash == "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
    result = {
        "experiment_id": "20261008-blind-image-language",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The common output rows of arbitrary-depth blind normalized transitions admit an exact regular language derived from the two raw Rule-30 preimage contexts.",
        "backend": "Python exact subset construction and Moore minimization",
        "parameters": {"raw_contexts": 16, "literal_control_max_depth": 8, "cpu_limit_seconds": 60, "address_space_limit_bytes": LIMIT},
        "hardware": {"machine": platform.machine(), "platform": platform.platform(), "logical_cpu_count": os.cpu_count()},
        "software": {"python": sys.version},
        "runtime_seconds": time.monotonic() - START,
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        "result_hashes": {"script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "immutable_reference_sha256": ref_hash},
        "result_summary": {"raw_transition_count": len(transitions), "reachable_dfa_states": len(subsets), "minimal_dfa_states": len(small), "initial_state": 0, "transition_columns": [0, 1], "minimized_transitions": small, "minimized_acceptance": accept, "literal_controls": controls},
        "certificate": {"raw_context_encoding": "a_(j-2) | b_(j-2)<<1 | a_(j-1)<<2 | b_(j-1)<<3", "raw_initial": next(iter(initial)), "raw_transitions_s_x_xprime_output_t": transitions, "reachable_subsets": [sorted(ss) for ss in subsets], "dfa_transitions": dfa, "minimization_blocks": block, "readable_class_order": order},
        "interpretation": "Exact finite automaton for the postblind spatial word language. All-depth language equality follows by chaining local raw truth-table constraints; finite controls are separate. A reset/cycle exclusion does not follow without an additional argument.",
        "status": "finite-exhaustive",
        "proof_scope": "Finite local transducer and exact regular-language construction; controls through depth eight.",
        "limitations": ["No all-depth gate/reset lemma is asserted by this computation.", "No proof of Problem 1, portal return bound, or original-support budget."],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256_excluding_this_field"] = hashlib.sha256(canonical).hexdigest()
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    fd, temp = tempfile.mkstemp(prefix=OUT.name + ".", dir=OUT.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, OUT)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    print(json.dumps({"summary": result["result_summary"], "runtime_seconds": result["runtime_seconds"]}))


if __name__ == "__main__":
    main()
