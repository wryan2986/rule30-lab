#!/usr/bin/env python3
"""Round 9 one-hole control: SINGLE fixed-word Phi-nilpotence test (k3 only).

Fixed claim: the deterministic cyclic-Phi orbit of the period-8 word
u = (2,2,2,2,2,2,2,0) reaches 00000000 (nilpotent) or repeats a nonzero word.
No other k value and no period/lag/source scan is performed here.

Two independent simple implementations:
  impl_formula: g from the bit definition r=b0 XOR (a0 OR a1),
    s=b1 XOR (a1 OR r) on decoded (low, high) bits;
  impl_table: g from the hand-verified literal 4x4 table
    [[0,3,2,1],[3,0,1,2],[3,2,1,0],[3,2,1,0]] (Sec 4 rows for g, not h).
The two are cross-checked on all 16 pairs before the single orbit run.
Each implementation iterates cyclic Phi until all-zero or first repeat,
cap 65536 = 4^8 (full period-8 state space). Single-threaded, local only.

Provenance JSON is written atomically (tmp + fsync + os.replace) to
results/problem1/20260907_round9_one_hole_control.json with full git commit,
reference hash, source, hardware, timings, and hashes.
"""
import hashlib
import json
import os
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAP = 65536
WORD0 = (2, 2, 2, 2, 2, 2, 2, 0)
ZERO = (0,) * 8
OUT_PATH = "results/problem1/20260907_round9_one_hole_control.json"
REFERENCE = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"
K2_HAND = "2220 1132 0212 2213 1221 1120 0133 3203 1310 2233 1001 3030 3131 2222 1111 0000".split()
K3_HAND = "22222220 11111132 00000212 00002213 00021223 00221103 02120313".split()


def g_formula(a, b):
    a0 = a & 1
    a1 = (a >> 1) & 1
    b0 = b & 1
    b1 = (b >> 1) & 1
    r = b0 ^ (a0 | a1)
    s = b1 ^ (a1 | r)
    return int(r | (s << 1))


G_LITERAL = (
    (0, 3, 2, 1),
    (3, 0, 1, 2),
    (3, 2, 1, 0),
    (3, 2, 1, 0),
)


def g_table(a, b):
    return int(G_LITERAL[a][b])


def step(word, g):
    n = len(word)
    return tuple(g(word[i], word[(i + 1) % n]) for i in range(n))


def run_orbit(word0, g, cap):
    seen = {word0: 0}
    chain = [word0]
    w = word0
    t0 = time.perf_counter()
    idx = 0
    while idx < cap:
        w = step(w, g)
        idx += 1
        if w == ZERO:
            chain.append(w)
            return {
                "outcome": "nilpotent",
                "index": idx,
                "first_repeat": None,
                "chain": [list(x) for x in chain],
            }, time.perf_counter() - t0
        if w in seen:
            chain.append(w)
            return {
                "outcome": "repeat_nonzero",
                "index": idx,
                "first_repeat": {
                    "word": list(w),
                    "first_seen_at": seen[w],
                    "repeated_at": idx,
                },
                "chain": [list(x) for x in chain],
            }, time.perf_counter() - t0
        seen[w] = idx
        if len(chain) < 100000:
            chain.append(w)
    return {
        "outcome": "cap_reached",
        "index": idx,
        "first_repeat": None,
        "chain": None,
    }, time.perf_counter() - t0


def sha256_text(s):
    return hashlib.sha256(s.encode()).hexdigest()


def run_table_orbit():
    """Separate string representation and orbit loop, with literal hand rows."""
    rows = ("0321", "3012", "3210", "3210")
    word, index = "22222220", 0
    visited, occurrence, chain = set(), {}, []
    started = time.perf_counter()
    while word not in visited and word != "00000000":
        assert index < CAP
        visited.add(word)
        occurrence[word] = index
        chain.append(list(map(int, word)))
        rotated = word[1:] + word[0]
        word = "".join(rows[int(a)][int(b)] for a, b in zip(word, rotated))
        index += 1
    chain.append(list(map(int, word)))
    repeat = None if word == "00000000" else {
        "word": list(map(int, word)), "first_seen_at": occurrence[word], "repeated_at": index}
    return {"outcome": "nilpotent" if repeat is None else "repeat_nonzero",
            "index": index, "first_repeat": repeat, "chain": chain}, time.perf_counter() - started


def main():
    t_start = time.perf_counter()
    os.chdir(ROOT)
    signal.alarm(120)
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    pairs_agree = all(
        g_formula(a, b) == g_table(a, b)
        for a in range(4) for b in range(4)
    )
    if not pairs_agree:
        print("FATAL: g implementations disagree on 16 pairs", file=sys.stderr)
        sys.exit(1)
    for frozen in (K2_HAND, K3_HAND):
        for before, after in zip(frozen, frozen[1:]):
            for implementation in (g_formula, g_table):
                assert step(tuple(map(int, before)), implementation) == tuple(map(int, after))
    res_f, dt_f = run_orbit(WORD0, g_formula, CAP)
    res_t, dt_t = run_table_orbit()
    agree = (
        res_f["outcome"] == res_t["outcome"]
        and res_f["index"] == res_t["index"]
        and res_f["first_repeat"] == res_t["first_repeat"]
        and res_f["chain"] == res_t["chain"]
    )
    if not agree:
        print("FATAL: implementations disagree on k3 orbit", file=sys.stderr)
        sys.exit(1)
    outcome = res_f["outcome"]
    assert outcome == "repeat_nonzero" and res_f["first_repeat"] == {
        "word": [0, 3, 0, 3, 3, 0, 0, 3], "first_seen_at": 286, "repeated_at": 818}
    chain = res_f["chain"]
    chain_text = "".join("".join(str(d) for d in w) for w in chain) if chain else ""
    try:
        git_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        git_commit = "unavailable"
    try:
        with open("src/python/rule30_research_reference.py", "rb") as fh:
            ref_sha = hashlib.sha256(fh.read()).hexdigest()
    except Exception:
        ref_sha = "unavailable"
    assert len(git_commit) == 40 and all(c in "0123456789abcdef" for c in git_commit)
    assert ref_sha == REFERENCE
    import datetime
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    total = time.perf_counter() - t_start
    hypothesis = (
        "The cyclic-Phi orbit of fixed 8-word 22222220 reaches 00000000 "
        "(Phi-nilpotent) or repeats a nonzero word first."
    )
    if outcome == "nilpotent":
        interpretation = (
            "k3 one-hole word is Phi-nilpotent: supplies a finite {0,2}-odd "
            "222 cycle of period dividing 8 for the Sec 3 construction. "
            "No all-k inference is made."
        )
        status = "finite-exhaustive"
    elif outcome == "repeat_nonzero":
        interpretation = (
            "k3 one-hole word is NOT Phi-nilpotent: repeats nonzero first, "
            "refuting the one-hole all-k supply at k3. Sec 3 conditional "
            "theorem retained; 222 supply must come from elsewhere."
        )
        status = "finite-exhaustive"
    else:
        interpretation = (
            "Cap reached without decision; orbit exceeds the full 4^8 state "
            "space bound, which is impossible for a deterministic map unless "
            "cap < reachable set -- report as inconclusive, rerun forbidden "
            "beyond this single test."
        )
        status = "inconclusive"
    record = {
        "experiment_id": "round9_one_hole_control_k3_corrected_verification",
        "timestamp_utc": ts,
        "git_commit": git_commit,
        "question": "problem1",
        "hypothesis": hypothesis,
        "backend": "python-stdlib-single-cpu",
        "parameters": {
            "word0": list(WORD0),
            "period": 8,
            "cap_per_impl": CAP,
            "cap_basis": "4^8 full period-8 state space",
            "impls": ["bit_formula", "hand_table_literal"],
            "pairs_crosscheck": "16/16 agree",
            "frozen_hand_vectors": {"k2": K2_HAND, "k3_initial": K3_HAND},
            "frozen_transition_checks_per_impl": 21,
            "same_input_verification_correction": True,
            "admission": "Only undecided k3 word22222220: nilpotence would leave all-k induction open; nonzero repeat refutes the exact all-k one-hole supply. No additional candidate or period is searched. The hand k2 chain is a verification vector.",
            "limits": {"cpu": "1 thread", "wall_s": 120, "mem_MiB": 256},
        },
        "hardware": {
            "platform": platform.platform(),
            "node": platform.uname().node,
            "machine": platform.uname().machine,
            "cpu_count": os.cpu_count(),
        },
        "software": {
            "python": platform.python_version(),
            "deps": "none",
            "source": "experiments/problem1_nonperiodicity/check_round9_one_hole_control.py",
        },
        "runtime_seconds": total,
        "implementation_seconds": {
            "impl_formula": dt_f,
            "impl_table": dt_t,
            "total": total,
        },
        "result_hashes": {
            "word0_sha256": sha256_text("".join(str(d) for d in WORD0)),
            "chain_sha256": sha256_text(chain_text) if chain_text else None,
            "script_sha256": None,
            "reference_sha256": ref_sha,
            "superseded_archive_sha256": hashlib.sha256((ROOT / "results/problem1/20260907_round9_superseded_run.json").read_bytes()).hexdigest(),
        },
        "result_summary": {
            "outcome": outcome,
            "index": res_f["index"],
            "first_repeat": res_f["first_repeat"],
            "impl_agreement": agree,
            "chain": chain,
            "chain_length": len(chain) if chain else None,
            "zero_seen": [0]*8 in chain,
            "cycle_length": res_f["index"] - res_f["first_repeat"]["first_seen_at"],
        },
        "interpretation": interpretation,
        "status": status,
        "proof_scope": "Complete finite certificate for one orbit. A verified nonzero repeat proves all-future nonnilpotence and refutes the all-k family, not Problem1.",
        "limitations": [
            "Tests exactly one word (k3); says nothing about k>=4.",
            "Both implementations share Python; representations and orbit loops are separate.",
            "This reruns the same input to correct the archived original provenance and strengthen independent verification.",
            "Git is pre-checkpoint HEAD; exact current source bytes are snapshotted below.",
        ],
    }
    try:
        with open(__file__, "rb") as fh:
            record["result_hashes"]["script_sha256"] = hashlib.sha256(fh.read()).hexdigest()
    except Exception:
        pass
    source_raw = Path(__file__).read_bytes()
    assert record["result_hashes"]["script_sha256"] == hashlib.sha256(source_raw).hexdigest()
    record["source_snapshot"] = source_raw.decode()
    record["peak_resident_KiB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    assert record["runtime_seconds"] < 120 and not record["result_summary"]["zero_seen"]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=os.path.dirname(OUT_PATH), prefix=Path(OUT_PATH).name,
                                     suffix=".tmp", mode="w", delete=False) as fh:
        tmp = fh.name
        json.dump(record, fh, indent=2)
        fh.write(chr(10))
        fh.flush()
        os.fsync(fh.fileno())
    assert os.path.getsize(tmp) < 4 * 1024**2
    os.replace(tmp, OUT_PATH)
    print(json.dumps({
        "outcome": outcome,
        "index": res_f["index"],
        "first_repeat": res_f["first_repeat"],
        "impl_agreement": agree,
        "dt_formula": dt_f,
        "dt_table": dt_t,
        "json": OUT_PATH,
    }, indent=2))


if __name__ == "__main__":
    main()
