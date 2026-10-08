#!/usr/bin/env python3
"""Independent all-width checker for the equal-output raw-row language.

Builds the four-bit raw-context NFA, determinizes it, and minimizes the DFA
using pair distinguishability (not the producer's subset/minimizer code).
"""
import hashlib, json, os, platform, resource, subprocess, sys, tempfile, time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20261008_blind_image_language_independent.json"
LIMIT = 256 * 1024 * 1024
START = time.monotonic()
RULE = {(a, b, c): a ^ (b | c) for a in (0, 1) for b in (0, 1) for c in (0, 1)}

def encode(ctx):
    a0, b0, a1, b1 = ctx
    return a0 | (b0 << 1) | (a1 << 2) | (b1 << 3)

def decode(s):
    return tuple((s >> i) & 1 for i in range(4))

def main():
    resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
    # For each context, enumerate the next independent inputs x,y. The label
    # is the common raw output only when the two truth-table outputs agree.
    edges = [[] for _ in range(16)]
    records = []
    for s in range(16):
        a0, b0, a1, b1 = decode(s)
        for x in (0, 1):
            for y in (0, 1):
                ca = RULE[(a0, a1, x)]
                cb = RULE[(b0, b1, y)]
                if ca != cb:
                    continue
                # Correct shifted context is (a_(j-1), b_(j-1), a_j,b_j).
                target = encode((a1, b1, x, y))
                edges[s].append((ca, target))
                records.append([s, x, y, ca, target])
    start = encode((1, 1, 0, 1))

    # Exact subset construction: finite word accepted iff at least one raw
    # context path realizes every requested common output bit.
    subsets = [frozenset((start,))]
    subset_id = {subsets[0]: 0}
    dfa = []
    queue = deque([subsets[0]])
    while queue:
        subset = queue.popleft()
        row = []
        for letter in (0, 1):
            dest = frozenset(t for s in subset for c, t in edges[s] if c == letter)
            if dest not in subset_id:
                subset_id[dest] = len(subsets)
                subsets.append(dest)
                queue.append(dest)
            row.append(subset_id[dest])
        dfa.append(row)
    accepting = [bool(s) for s in subsets]

    # DFA minimization by the classical table-filling distinguishability
    # relation, independently of iterative signature/Moore refinement.
    n = len(subsets)
    distinguishable = {(i, j) for i in range(n) for j in range(i+1, n)
                       if accepting[i] != accepting[j]}
    while True:
        added = []
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) in distinguishable:
                    continue
                for letter in (0, 1):
                    a, b = dfa[i][letter], dfa[j][letter]
                    if a != b and (min(a, b), max(a, b)) in distinguishable:
                        added.append((i, j))
                        break
        if not added:
            break
        distinguishable.update(added)

    classes = []
    class_of = [-1] * n
    for i in range(n):
        if class_of[i] >= 0:
            continue
        ci = len(classes)
        members = [j for j in range(i, n)
                   if j == i or (min(i, j), max(i, j)) not in distinguishable]
        for j in members:
            class_of[j] = ci
        classes.append(members)
    qtrans = [[class_of[dfa[members[0]][letter]] for letter in (0, 1)]
              for members in classes]
    qaccept = [accepting[members[0]] for members in classes]
    # Canonical BFS numbering from the initial equivalence class.
    order = [class_of[0]]
    for c in order:
        for t in qtrans[c]:
            if t not in order:
                order.append(t)
    renumber = {c: i for i, c in enumerate(order)}
    minimal_transitions = [[renumber[t] for t in qtrans[c]] for c in order]
    minimal_acceptance = [qaccept[c] for c in order]
    expected = [[1,2],[2,3],[2,2],[4,5],[4,6],[2,1],[2,7],[4,4]]
    assert minimal_transitions == expected
    assert minimal_acceptance == [True, True, False, True, True, True, True, True]

    # The 8-state graph has all states except dead state 2 coaccessible to an
    # infinite path. Its infinite paths decompose as described in the review:
    # initial 0, then 1 mod 3 ones, then either all ones forever or exit 0 and
    # concatenate the return-to-state-4 tokens 0, 110, 111 forever.
    assert all(any(minimal_transitions[s][x] != 2 for x in (0, 1)) for s in range(8) if s != 2)
    # Check return tokens from state 4 and forced transition after one 1.
    assert minimal_transitions[4][0] == 4
    assert minimal_transitions[4][1] == 6 and minimal_transitions[6][1] == 7
    assert minimal_transitions[7][0] == 4 and minimal_transitions[7][1] == 4

    elapsed = time.monotonic() - START
    result = {
        "experiment_id": "20261008-blind-image-language-independent",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The all-width common raw Rule 30 output language is recognized by the claimed minimal 8-state DFA.",
        "backend": "independent Python context-NFA subset construction and pair-distinguishability minimization",
        "parameters": {"context_count": 16, "input_pairs_per_context": 4, "address_space_limit_bytes": LIMIT, "cpu_limit_seconds": 60},
        "hardware": {"machine": platform.machine(), "platform": platform.platform(), "logical_cpu_count": os.cpu_count()},
        "software": {"python": sys.version},
        "runtime_seconds": elapsed,
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        "result_summary": {"raw_context_edges": len(records), "reachable_subset_states": len(subsets), "minimal_states": len(order), "transitions": minimal_transitions, "acceptance": minimal_acceptance},
        "certificate": {"initial_context": start, "raw_context_edges_s_x_y_c_t": records, "subsets": [sorted(s) for s in subsets], "subset_dfa": dfa, "accepting_subsets": accepting, "distinguishable_pairs": sorted([list(x) for x in distinguishable]), "minimized_transitions": minimal_transitions, "minimized_acceptance": minimal_acceptance},
        "all_width_argument": "By induction on word length, a path starting at context (a[j-2],b[j-2],a[j-1],b[j-1]) adds exactly one next pair (a[j],b[j]) per edge, labelled by the common Rule-30 output at column j. Conversely every pair of raw rows with equal outputs at all columns follows these edges. Thus NFA paths, hence its subset DFA, describe every width without a cutoff.",
        "infinite_language": "01 1^omega OR 01(111)^k 0 (0|110|111)^omega, k>=0; finite accepted words are exactly prefixes since every nondead DFA state has an infinite continuation.",
        "interpretation": "An independent finite-context reconstruction and minimization agrees with the supplied all-width regular-language construction. The arbitrary-width conclusion follows from the local context-shift induction; this does not prove a temporal reset or Problem 1.",
        "status": "finite-exhaustive",
        "proof_scope": "Exact finite local transducer, all-width chaining argument, and minimal DFA certificate.",
        "limitations": ["Does not establish a reset/cycle exclusion without a separate argument.", "Does not prove Problem 1 or a portal return bound."],
    }
    result["result_hashes"] = {"script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256_excluding_this_field"] = hashlib.sha256(canonical).hexdigest()
    raw = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=OUT.name + ".", dir=OUT.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, OUT)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    print(json.dumps(result["result_summary"]))

if __name__ == "__main__":
    main()
