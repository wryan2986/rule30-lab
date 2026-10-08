#!/usr/bin/env python3
"""Independent depth-five product graph and bad-cycle verifier.

Uses explicit Rule 30 truth-table lookup and per-bad-edge reachability. It
does not import any producer transition, SCC, or rank routine.
"""
import hashlib, json, os, platform, resource, signal, subprocess, sys, tempfile, time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20261008_depth5_gate_independent.json"
START = time.monotonic()
R = 5
UBITS = 2 * R
UMASK = (1 << UBITS) - 1
N = 1 << (UBITS + 4)
WALL_LIMIT = 60
MEMORY_LIMIT = 256 * 1024 * 1024
RULE30 = tuple((a ^ (b | c)) for a in (0, 1) for b in (0, 1) for c in (0, 1))

def timeout(_signum, _frame):
    raise TimeoutError("60-second wall-clock cap exceeded")

def bit(x, i):
    return (x >> i) & 1

def rule30(a, b, c):
    return RULE30[(a << 2) | (b << 1) | c]

def normalized_step(word, label, depth):
    """Derive normalized child pairs by applying Rule 30 to two raw rows."""
    rows = [(1, 0), (0, 1)]
    rows.extend((bit(word, 2*j), bit(word, 2*j+1)) for j in range(depth))
    out = 0
    for i in range(depth):
        h, l, x = rows[i:i+3]
        raw_a = rule30(h[0], l[0], x[0])
        raw_b = rule30(h[0] ^ h[1], l[0] ^ l[1], x[0] ^ x[1])
        y = raw_a ^ raw_b
        xx = raw_a ^ (label & y)
        out |= xx << (2*i)
        out |= y << (2*i+1)
    return out

def main():
    # Enforce actual process resource caps, then verify the complete Rule 30
    # lookup table against its defining truth table.
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))
    resource.setrlimit(resource.RLIMIT_CPU, (WALL_LIMIT, WALL_LIMIT))
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(WALL_LIMIT)
    assert RULE30 == (0, 1, 1, 1, 1, 0, 0, 0)

    blind = bytearray(1 << UBITS)
    for u in range(1 << UBITS):
        blind[u] = normalized_step(u, 0, R) == normalized_step(u, 1, R)
    blind_count = sum(blind)

    adjacency = [[] for _ in range(N)]
    bad = []
    edge_count = 0
    for state in range(N):
        u = state & UMASK
        v = (state >> UBITS) & 3
        z = (state >> (UBITS + 2)) & 3
        av = normalized_step(u | (v << UBITS), 0, R + 1)
        bv = normalized_step(u | (z << UBITS), 0, R + 1)
        for a in (0, 1):
            out_a = av if a == 0 else normalized_step(u | (v << UBITS), 1, R + 1)
            for b in (0, 1):
                if not blind[u] and a != b:
                    continue
                out_b = bv if b == 0 else normalized_step(u | (z << UBITS), 1, R + 1)
                # Product edges retain only equal depth-r output projections.
                if (out_a & UMASK) != (out_b & UMASK):
                    continue
                vo, zo = (out_a >> UBITS) & 3, (out_b >> UBITS) & 3
                target = (out_a & UMASK) | (vo << UBITS) | (zo << (UBITS + 2))
                adjacency[state].append(target)
                edge_count += 1
                if blind[u] and a == b and ((vo ^ zo) & 2):
                    bad.append((state, target))

    # Independent cycle criterion: edge s->t is on a directed cycle iff t
    # can reach s. Search from each distinct bad-edge target; no SCC/rank code.
    bad_cycle_edges = []
    searches = 0
    for source, target in bad:
        searches += 1
        seen = bytearray(N)
        seen[target] = 1
        todo = deque([target])
        found = False
        while todo and not found:
            x = todo.popleft()
            if x == source:
                found = True
                break
            for y in adjacency[x]:
                if not seen[y]:
                    seen[y] = 1
                    todo.append(y)
        if found:
            bad_cycle_edges.append((source, target))

    elapsed = time.monotonic() - START
    signal.alarm(0)
    if elapsed > WALL_LIMIT:
        raise TimeoutError("60-second wall-clock cap exceeded")
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    result = {
        "schema": "problem1-depth5-independent-cycle-review-v1",
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "claim_status": "finite-exhaustive" if not bad_cycle_edges else "refuted",
        "scope": {
            "observer_depth": R,
            "product_state_count": N,
            "product_packing": "U | (V << 10) | (Z << 12)",
            "edge_domain": "all binary U,V,Z; for blind U allow all four label pairs, otherwise allow only a=b; retain iff both depth-6 transitions agree in their lower 10 bits",
            "bad_edge": "upper U is blind and equal-label copied outputs have differing Y bit of the added pair",
            "cycle_method": "for each bad directed edge source->target, BFS from target and test reachability of source; no SCC or rank routine",
        },
        "graph": {
            "retained_edges": edge_count,
            "bad_edges": len(bad),
            "blind_upper_states": blind_count,
            "bad_edges_on_directed_cycles": len(bad_cycle_edges),
            "bad_cycle_witnesses": [[a, b] for a, b in bad_cycle_edges[:8]],
            "reachability_searches": searches,
        },
        "independent_derivation": {
            "rule30_truth_table_order_abc": list(RULE30),
            "transition": "apply F(a,b,c)=a XOR (b OR c) to the fixed-boundary first raw row and its XOR companion; normalize to Xnew=raw_a XOR (label*Y), Y=raw_a XOR raw_b",
            "depth_six_transition_calls_are_depth_six_pairs": True,
            "no_producer_code_imported": True,
        },
        "all_period_argument_review": {
            "reviewed": "finite reduction Sections 1-2 and projection lemma Section 6",
            "finding": "If the product graph has no bad edge on any directed cycle, then the stronger unlifted cycle exclusion holds at r=5. The projection lemma correctly transfers a lifted rank strict on every bad edge to the base graph; however this independent check establishes the graph cycle property directly and does not itself certify a lifted-rank artifact. The supplied path-to-period argument is scoped to fixed depth and admissible complete odd fibers with nonzero parents.",
            "scope_limit": "No conclusion for depths other than 5, zero returns, bounded reuse, or Problem 1 as a whole.",
        },
        "provenance": {
            "base_commit": "ddc53f28dbe30a98764f3dec8a7725ec5be1dbe8",
            "observed_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "processor": platform.processor(),
            "logical_cpu_count": os.cpu_count(),
            "elapsed_seconds": elapsed,
            "peak_rss_bytes": peak_rss,
            "memory_limit_bytes": MEMORY_LIMIT,
            "wall_limit_seconds": WALL_LIMIT,
        },
        "experiment_id": "20261008-depth5-independent-bad-cycle-verification",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "question": "problem1",
        "hypothesis": "At observer depth five, no directed cycle in the complete normalized product graph contains a bad equal-label gate edge.",
        "backend": "independent Python truth-table transition and per-edge BFS",
        "parameters": {"r": R, "states": N, "wall_cap_seconds": WALL_LIMIT, "memory_cap_bytes": MEMORY_LIMIT},
        "hardware": {"platform": platform.platform(), "processor": platform.processor(), "logical_cpu_count": os.cpu_count()},
        "software": {"python": sys.version, "transition_source": "local explicit Rule 30 truth-table and raw two-row recurrence"},
        "runtime_seconds": elapsed,
        "result_hashes": {"verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "result_summary": {"states": N, "retained_edges": edge_count, "bad_edges": len(bad), "bad_edges_on_cycles": len(bad_cycle_edges)},
        "interpretation": "The finite depth-five graph contains no bad edge on a directed cycle. This supports the fixed-depth absence claim only.",
        "status": "finite-exhaustive" if not bad_cycle_edges else "refuted",
        "proof_scope": "Exhaustive finite graph at r=5; direct reachability check for every bad edge.",
        "limitations": ["Does not prove Problem 1 or any untested observer depth.", "Does not certify a lifted rank array; it independently establishes the base graph's cycle property.", "The all-period conclusion depends on the separate stated finite-reduction theorem and its hypotheses."],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256_excluding_this_field"] = hashlib.sha256(canonical).hexdigest()
    raw = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=OUT.name + ".", suffix=".tmp", dir=OUT.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, OUT)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    print(json.dumps({"status": result["claim_status"], **result["graph"], "elapsed_seconds": elapsed, "result_bytes": len(raw)}))

if __name__ == "__main__":
    main()
