#!/usr/bin/env python3
"""Finite over-approximate gate-difference reachability, depths 1..7."""
import base64, hashlib, json, os, platform, resource, signal, subprocess, sys, tempfile, time, zlib
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20261008_gate_difference_reachability.json"
START = time.monotonic()
WALL_LIMIT = 60
MEMORY_LIMIT = 256 * 1024 * 1024
MAX_OUTPUT = 1024 * 1024
RULE30 = {(a,b,c): a ^ (b | c) for a in (0,1) for b in (0,1) for c in (0,1)}

def wall_alarm(_signum, _frame):
    raise TimeoutError("60-second wall cap exceeded")

def bit(x, i):
    return (x >> i) & 1

def raw_normalized_step(state, label, depth):
    """Independent two-raw-row Rule 30 transition, with fixed boundaries."""
    pairs = [(1,0), (0,1)]
    pairs.extend((bit(state,2*j), bit(state,2*j+1)) for j in range(depth))
    out = 0
    for j in range(depth):
        h,l,x = pairs[j:j+3]
        first = RULE30[(h[0],l[0],x[0])]
        second = RULE30[(h[0]^h[1],l[0]^l[1],x[0]^x[1])]
        y = first ^ second
        xx = first ^ (label & y)
        out |= xx << (2*j)
        out |= y << (2*j+1)
    return out

def direct_gate(prev, last, child, label):
    """One normalized output pair from raw Rule-30 truth-table evaluations."""
    first = RULE30[(prev[0], last[0], child[0])]
    second = RULE30[(prev[0]^prev[1], last[0]^last[1], child[0]^child[1])]
    y = first ^ second
    return (first ^ (label & y), y)

def expected_delta(last, delta, label):
    L,M = last
    e,f = delta
    fp = (M & e) ^ ((1 ^ L ^ M) & f)
    ep = ((1 ^ L) & e) ^ (label & fp)
    return ep,fp

def unpack_pairs(word, depth):
    return [(bit(word,2*j),bit(word,2*j+1)) for j in range(depth)]

def word_from_u(u, depth):
    return unpack_pairs(u,depth)

def encode_word(word):
    return sum((x | (y<<1)) << (2*j) for j,(x,y) in enumerate(word))

def suffix_report(masks, depth):
    report = []
    for k in range(1, min(4,depth)+1):
        first_for_suffix = {}
        conflict = None
        for u,mask in enumerate(masks):
            suffix = u >> (2*(depth-k))
            if suffix not in first_for_suffix:
                first_for_suffix[suffix] = (u,mask)
            elif first_for_suffix[suffix][1] != mask and conflict is None:
                u0,m0 = first_for_suffix[suffix]
                conflict = {
                    "suffix_length": k,
                    "suffix_pairs": word_from_u(suffix,k),
                    "u_a": u0, "word_a": word_from_u(u0,depth), "mask_a": m0,
                    "u_b": u, "word_b": word_from_u(u,depth), "mask_b": mask,
                }
        report.append({"suffix_length":k,"depends_only_on_suffix":conflict is None,
                       "counterexample":conflict})
    return report

def find_witness(r, n, blind, uppers):
    # State id = 4*U + delta, where delta=e+2*f. All U seed from delta zero.
    size = n * 4
    distance = [-1] * size
    predecessor = [-1] * size
    action = bytearray(size)  # bit 0 label w, bit 1 impulse lambda
    queue = deque()
    for u in range(n):
        idx = 4*u
        distance[idx] = 0
        queue.append(idx)
    while queue:
        idx = queue.popleft()
        u,delta = divmod(idx,4)
        e,f = delta & 1, (delta >> 1) & 1
        pairs = unpack_pairs(u,r)
        L,M = pairs[-1]
        fp = (M & e) ^ ((1 ^ L ^ M) & f)
        if blind[u] and fp:
            # Reconstruct shortest seed-to-state path; all seeds are distance 0.
            path = []
            cur = idx
            while predecessor[cur] >= 0:
                path.append({"u":predecessor[cur]//4,
                             "delta":predecessor[cur]%4,
                             "label":action[cur]&1,
                             "impulse_lambda":(action[cur]>>1)&1})
                cur = predecessor[cur]
            path.reverse()
            return {"distance":distance[idx], "u":u, "upper_word":pairs,
                    "delta":delta, "delta_pair":[e,f], "last_upper_pair":[L,M],
                    "homogeneous_f_prime":fp, "seed_upper":cur//4,
                    "path_transitions":path}
        for w in (0,1):
            unext = uppers[u][w]
            ep = ((1 ^ L) & e) ^ (w & fp)
            for lam in ((0,1) if blind[u] else (0,)):
                dnext = (ep ^ lam) + 2*fp
                nxt = 4*unext + dnext
                if distance[nxt] < 0:
                    distance[nxt] = distance[idx] + 1
                    predecessor[nxt] = idx
                    action[nxt] = w | (lam << 1)
                    queue.append(nxt)
    return None

def verify_delta_formula():
    checks = 0
    for prev in ((0,0),(0,1),(1,0),(1,1)):
        for last in ((0,0),(0,1),(1,0),(1,1)):
            for child in ((0,0),(0,1),(1,0),(1,1)):
                for delta in ((0,0),(0,1),(1,0),(1,1)):
                    other = (child[0]^delta[0], child[1]^delta[1])
                    for w in (0,1):
                        got = direct_gate(prev,last,child,w)
                        other_out = direct_gate(prev,last,other,w)
                        observed = (got[0]^other_out[0], got[1]^other_out[1])
                        assert observed == expected_delta(last,delta,w), (prev,last,child,delta,w,observed,expected_delta(last,delta,w))
                        checks += 1
    return checks

def actual_r5_product_witness():
    """Replay the overapproximate r=5 trace in the exact two-copy graph."""
    r = 5
    mask = (1 << (2*r)) - 1
    u, v, z = 255, 0, 0
    label_pairs = [(0,1),(1,1),(1,1),(1,1),(0,0),(0,0)]
    records = []
    upper_path = [u]
    for k,(a,b) in enumerate(label_pairs):
        blind = raw_normalized_step(u,0,r) == raw_normalized_step(u,1,r)
        out_a = raw_normalized_step(u | (v << (2*r)),a,r+1)
        out_b = raw_normalized_step(u | (z << (2*r)),b,r+1)
        ua,ub = out_a & mask,out_b & mask
        assert ua == ub
        vn,zn = (out_a >> (2*r)) & 3,(out_b >> (2*r)) & 3
        ya,yb = (vn >> 1)&1,(zn >> 1)&1
        records.append({"step":k,"source_U":u,"source_V":v,"source_Z":z,
                        "labels":[a,b],"source_U_blind":bool(blind),
                        "output_upper_A":ua,"output_upper_B":ub,
                        "output_V":vn,"output_Z":zn,
                        "outgoing_Y_A":ya,"outgoing_Y_B":yb,
                        "bad_edge":bool(blind and a==b and ya!=yb)})
        u,v,z = ua,vn,zn
        upper_path.append(u)
    assert upper_path == [255,4,90,162,194,995,340], upper_path
    assert records[0]["source_U_blind"] and records[0]["labels"] == [0,1]
    assert records[4]["output_upper_A"] == 995
    assert records[5]["source_U_blind"] and records[5]["bad_edge"]

    # Test whether 255 is on any cycle in the upper graph U->T_w(U): for each
    # outgoing target, exhaustively search for a path back to 255.
    n = 1 << (2*r)
    starts = [raw_normalized_step(255,w,r) for w in (0,1)]
    return_paths = []
    for target in sorted(set(starts)):
        seen = bytearray(n)
        seen[target] = 1
        q = deque([target])
        found = False
        while q and not found:
            x = q.popleft()
            if x == 255:
                found = True
                break
            for w in (0,1):
                y = raw_normalized_step(x,w,r)
                if not seen[y]:
                    seen[y] = 1
                    q.append(y)
        return_paths.append({"target":target,"reaches_255":found,
                             "visited_upper_states":sum(seen)})
    return {"observer_depth":r,"upper_path":upper_path,
            "label_pairs":label_pairs,"product_steps":records,
            "terminal_bad_edge_index":5,
            "upper_255_cycle_test":{"graph":"U -> T_w(U), w in {0,1}",
                "outgoing_targets":starts,"target_to_source_searches":return_paths,
                "upper_255_on_any_directed_cycle":any(x["reaches_255"] for x in return_paths)},
            "interpretation":"This exact finite two-child path witnesses a transient selector effect, but its initial upper state 255 is not on an upper-state directed cycle. Therefore it does not refute the proved cyclic S5 statement."}

def main():
    resource.setrlimit(resource.RLIMIT_AS,(MEMORY_LIMIT,MEMORY_LIMIT))
    resource.setrlimit(resource.RLIMIT_CPU,(WALL_LIMIT,WALL_LIMIT))
    signal.signal(signal.SIGALRM,wall_alarm)
    signal.alarm(WALL_LIMIT)
    delta_checks = verify_delta_formula()
    depths = []
    trie_label_chunks = []
    trie_offsets = []
    total_words = 0
    all_witnesses = []
    for r in range(1,8):
        n = 1 << (2*r)
        blind = bytearray(n)
        uppers = [[0,0] for _ in range(n)]
        for u in range(n):
            a = raw_normalized_step(u,0,r)
            b = raw_normalized_step(u,1,r)
            blind[u] = (a == b)
            uppers[u][0] = a
            uppers[u][1] = b

        # Multi-source BFS implements independent delta=0 seed for every U.
        masks = bytearray(n)
        reachable = bytearray(n*4)
        q = deque(4*u for u in range(n))
        for u in range(n):
            reachable[4*u] = 1
        while q:
            idx = q.popleft()
            u,delta = divmod(idx,4)
            masks[u] |= 1 << delta
            e,f = delta & 1,(delta>>1)&1
            L,M = unpack_pairs(u,r)[-1]
            fp = (M & e) ^ ((1 ^ L ^ M) & f)
            ep0 = (1 ^ L) & e
            for w in (0,1):
                unext = uppers[u][w]
                ep = ep0 ^ (w & fp)
                for lam in ((0,1) if blind[u] else (0,)):
                    dn = (ep ^ lam) + 2*fp
                    nxt = 4*unext + dn
                    if not reachable[nxt]:
                        reachable[nxt]=1
                        q.append(nxt)

        # Trie labels are serialized in lexicographic pair-word order. The
        # implicit trie has all four pair-symbol children at each internal node.
        lex_masks = bytearray(n)
        for u,mask in enumerate(masks):
            x=u; rev=0
            for _ in range(r):
                rev = (rev<<2) | (x&3)
                x >>= 2
            lex_masks[rev]=mask
        trie_offsets.append({"depth":r,"offset":total_words,"count":n})
        trie_label_chunks.append(bytes(lex_masks))
        total_words += n

        hist = Counter(masks)
        witness = find_witness(r,n,blind,uppers)
        if witness is not None:
            all_witnesses.append({"r":r,**witness})
        depths.append({
            "r":r,"upper_states":n,"blind_upper_states":sum(blind),
            "reachable_state_pairs":sum(reachable),
            "reachable_delta_mask_histogram":{str(k):v for k,v in sorted(hist.items())},
            "mask_suffix_dependence":suffix_report(masks,r),
            "shortest_bad_incoming_witness":witness,
            "reachable_masks_base64_zlib":base64.b64encode(zlib.compress(bytes(masks),9)).decode(),
        })

    actual_witness = actual_r5_product_witness()

    elapsed = time.monotonic()-START
    signal.alarm(0)
    if elapsed > WALL_LIMIT:
        raise TimeoutError("60-second wall cap exceeded")
    trie_raw = b"".join(trie_label_chunks)
    result = {
        "schema":"problem1-gate-difference-reachability-v1",
        "experiment_id":"20261008-gate-difference-reachability",
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "git_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "question":"problem1",
        "hypothesis":"For every tested depth r=1,...,7, the specified blind-impulse over-approximation has no reachable state with a blind upper state and homogeneous f_prime=1.",
        "backend":"independent Python raw two-row Rule 30 and breadth-first reachability",
        "parameters":{"depths":[1,2,3,4,5,6,7],"delta_encoding":"e+2*f","seed":"delta=0 for every upper state U","wall_limit_seconds":WALL_LIMIT,"memory_limit_bytes":MEMORY_LIMIT,"trie_pair_alphabet":[[0,0],[1,0],[0,1],[1,1]]},
        "hardware":{"machine":platform.machine(),"platform":platform.platform(),"logical_cpu_count":os.cpu_count()},
        "software":{"python":sys.version},
        "runtime_seconds":elapsed,
        "peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
        "result_summary":{"difference_formula_direct_checks":delta_checks,"depths":[{"r":d["r"],"states":d["upper_states"],"blind":d["blind_upper_states"],"reachable_pairs":d["reachable_state_pairs"],"reachable_mask_histogram":d["reachable_delta_mask_histogram"],"bad_witness_found":d["shortest_bad_incoming_witness"] is not None} for d in depths]},
        "depth_records":depths,
        "trie":{"meaning":"Implicit full four-ary trie of spatial pair words (pair j is the jth symbol); each node at depth r is labelled by that U's reachable-delta mask. Concatenated endpoint labels are lexicographic by pair word at each depth.","depth_offsets":trie_offsets,"total_labeled_nodes":total_words,"labels_base64_zlib":base64.b64encode(zlib.compress(trie_raw,9)).decode()},
        "witnesses":all_witnesses,
        "actual_r5_product_witness_review":actual_witness,
        "interpretation":"Finite exact reachability for the specified over-approximation at r=1..7 finds bad incoming witnesses at r=1,5,7, refuting the stated uniform finite-depth absence hypothesis. Absence at r=2,3,4,6 is depth-specific and does not prove an arbitrary-depth invariant.",
        "status":"refuted",
        "proof_scope":"Exact finite states/transitions for each tested depth and exhaustive direct local verification of the homogeneous delta formula.",
        "limitations":["The arbitrary lambda impulse at blind states over-approximates actual differing-label behavior.","Depths 1..7 do not imply an all-depth invariant or prove S_r at arbitrary r.","This computation addresses no temporal reset, zero-return, or original-support budget claim."],
        "provenance":{"base_commit":"ddc53f28dbe30a98764f3dec8a7725ec5be1dbe8","python":sys.version,"platform":platform.platform(),"peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,"elapsed_seconds":elapsed,"cpu_limit_seconds":WALL_LIMIT,"wall_limit_seconds":WALL_LIMIT,"address_space_limit_bytes":MEMORY_LIMIT},
    }
    result["result_hashes"]={"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    canonical=json.dumps(result,sort_keys=True,separators=(",",":")).encode()
    result["payload_sha256_excluding_this_field"]=hashlib.sha256(canonical).hexdigest()
    raw=(json.dumps(result,sort_keys=True,indent=2)+"\n").encode()
    if len(raw)>MAX_OUTPUT:
        raise ValueError(f"result exceeds {MAX_OUTPUT} bytes: {len(raw)}")
    OUT.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=OUT.name+".",suffix=".tmp",dir=OUT.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,OUT)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    print(json.dumps(result["result_summary"]))

if __name__ == "__main__":
    main()
