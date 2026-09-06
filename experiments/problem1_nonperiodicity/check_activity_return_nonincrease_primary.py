"""Primary packed-int ordinary-history closed-vector certificate for activity return nonincrease.

Admission: proofs/informal/problem1_activity_return_nonincrease.md (read in full).
Scope ONLY: fixed u18 state x0=0x6473d46ab with from-zero history
  uutuuttuupupuuupup (first u creates root 1, excluded from nonroot
  positions), replay exactly the TEN observed forced branches ttttututut,
  confirm the unobserved final u gate at time10 WITHOUT executing it.
Compare R(x4) and R(x10) over the three-return block times4..10.

Method (primary only): packed Python ints, ordinary generator/scanner
histories. For an ordinary history with n nonroot letters and prefix
endpoints v0=root..vn=x, V_s(x)=sum_{i<n} bit0(A^s(v_i)) for s>=n.
Direct V_s for s=0..n+2 via packed T evolution; tail scores from age n
until the FIRST repeated full endpoint vector. No imports from older
scientific implementations; stdlib only. The independent cell/projection
checker is a separate lead-owned file and is not duplicated here.

Bounds: 1 CPU, 120 s, 1 GiB, at most 65536 tail transitions per endpoint.
Stop inconclusive at any cap, with no scope expansion.
"""
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = str(Path(__file__).resolve().parents[2])
NOTE_REL = "proofs/informal/problem1_activity_return_nonincrease.md"
SELF_REL = "experiments/problem1_nonperiodicity/check_activity_return_nonincrease_primary.py"
OUT_REL = "results/problem1/20260906_activity_return_nonincrease_primary.json"

X0 = 0x6473d46ab
FROM_ZERO = "uutuuttuupupuuupup"
NONROOT0 = "utuuttuupupuuupup"
BRANCHES = "ttttututut"
ROOT = 1
MAX_TAIL = 65536


def T(v):
    return v ^ ((v << 1) | (v << 2))


def A(v):
    return T(v) >> 2


def pi(v):
    return v >> 2


def Gt(z):
    return A(4 * z)


def Gu(z):
    return A(4 * z + 1)


def Gp(z):
    return A(4 * z + 2)


GEN = {"t": Gt, "u": Gu, "p": Gp}
SCAN = {0: "t", 1: "u", 2: "p", 3: "p"}


def apply_word(start, word):
    v = start
    for ch in word:
        v = GEN[ch](v)
    return v


def endpoints_of(start, word):
    pts = [start]
    for ch in word:
        pts.append(GEN[ch](pts[-1]))
    return pts


def h_step(letters, endpoints):
    new_letters = [SCAN[e & 3] for e in endpoints[1:]]
    new_endpoints = [A(e) for e in endpoints]
    assert new_endpoints[0] == ROOT
    check = endpoints_of(ROOT, new_letters)
    assert check == new_endpoints, "H-step endpoint/letter mismatch"
    return new_letters, new_endpoints


def V_direct(x, s):
    if s == 0:
        return 0, []
    row = x
    bits = []
    for _ in range(s):
        bits.append((row >> (2 * s)) & 1)
        row = T(row)
    return sum(bits), bits


def run(cmd):
    try:
        p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=30)
        return p.stdout.strip()
    except Exception as e:
        return "unavailable: " + str(e)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def certify(x, letters, endpoints, cap):
    n = len(letters)
    assert endpoints[-1] == x
    assert len(endpoints) == n + 1
    direct = []
    for s in range(n + 3):
        val, bits = V_direct(x, s)
        direct.append({"s": s, "V": val, "temporal_bits": bits})
    for s in range(n, n + 3):
        tail_val = sum((A_pow(e, s)) & 1 for e in endpoints[:-1])
        assert tail_val == direct[s]["V"], (s, tail_val, direct[s]["V"])
    vec = tuple(A_pow(e, n) for e in endpoints[:-1])
    seen = {vec: 0}
    scores = [sum(v & 1 for v in vec)]
    steps = 0
    while True:
        if steps >= cap:
            return {"inconclusive": True, "reason": "tail cap reached"}
        vec = tuple(A(v) for v in vec)
        steps += 1
        if vec in seen:
            entry = seen[vec]
            cycle = steps - entry
            break
        seen[vec] = steps
        scores.append(sum(v & 1 for v in vec))
    tail_R = max(scores)
    direct_R = max(d["V"] for d in direct[:n]) if n else 0
    R = max(direct_R, tail_R)
    candidates = []
    if direct_R == R and n:
        candidates.append(min(d["s"] for d in direct[:n] if d["V"] == R))
    if tail_R == R:
        candidates.append(scores.index(R) + n)
    maximizer = min(candidates)
    return {
        "inconclusive": False,
        "n": n,
        "direct": direct,
        "tail_scores": scores,
        "tail_entry_age": entry + n,
        "tail_cycle_length": cycle,
        "tail_transitions": steps,
        "tail_R": tail_R,
        "direct_R": direct_R,
        "R": R,
        "maximizer_age": maximizer,
        "closed_vector": list(vec),
    }


def A_pow(v, k):
    for _ in range(k):
        v = A(v)
    return v


def main():
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_AS, (1024 ** 3, 1024 ** 3))
    t_all = time.perf_counter()
    assert apply_word(0, FROM_ZERO) == X0, "from-zero reconstruction failed"
    assert NONROOT0 == FROM_ZERO[1:], "nonroot split"
    assert endpoints_of(ROOT, NONROOT0)[-1] == X0, "rooted reconstruction failed"
    letters, endpoints = list(NONROOT0), endpoints_of(ROOT, NONROOT0)
    x = X0
    orbit = [x]
    for t, ch in enumerate(BRANCHES):
        gate = x & 15
        assert gate in (7, 11), (t, gate)
        want = "u" if gate == 7 else "t"
        assert want == ch, (t, want, ch)
        letters, endpoints = h_step(letters, endpoints)
        Q = Gu if gate == 7 else Gt
        xn = Q(A(x))
        assert xn == 4 * A(A(x)) + 3, (t, "F identity")
        letters = letters + [want]
        x = xn
        orbit.append(x)
        assert endpoints_of(ROOT, letters)[-1] == x, (t, "history endpoint drift")
        endpoints = endpoints_of(ROOT, letters)
    assert len(orbit) == 11
    x4, x10 = orbit[4], orbit[10]
    assert (x10 & 15) == 7, "final unobserved gate must be u"
    # rebuild per-time histories deterministically for the record
    hist = {}
    letters_r, x_r = list(NONROOT0), X0
    e_r = endpoints_of(ROOT, letters_r)
    hist["0"] = {"letters": "".join(letters_r), "x": hex(x_r)}
    for t, ch in enumerate(BRANCHES):
        gate = x_r & 15
        letters_r, e_r = h_step(letters_r, e_r)
        Q = Gu if gate == 7 else Gt
        xn = Q(A(x_r))
        letters_r = letters_r + [ch]
        x_r = xn
        e_r = endpoints_of(ROOT, letters_r)
        assert e_r[-1] == x_r
        hist[str(t + 1)] = {"letters": "".join(letters_r), "x": hex(x_r)}
    for r in (4, 10):
        assert hist[str(r)]["x"] == hex(orbit[r])
    e4 = endpoints_of(ROOT, list(hist["4"]["letters"]))
    e10 = endpoints_of(ROOT, list(hist["10"]["letters"]))
    c4 = certify(x4, list(hist["4"]["letters"]), e4, MAX_TAIL)
    c10 = certify(x10, list(hist["10"]["letters"]), e10, MAX_TAIL)
    assert not c4["inconclusive"] and not c10["inconclusive"]
    decision = "nonincrease_holds" if c10["R"] <= c4["R"] else "REFUTED_increase"
    note_p = os.path.join(REPO, NOTE_REL)
    with open(note_p, "rb") as f:
        note_bytes = f.read()
    note_sha = sha_bytes(note_bytes)
    note_text = note_bytes.decode("utf-8")
    self_p = os.path.join(REPO, SELF_REL)
    with open(self_p, "rb") as f:
        self_bytes = f.read()
    self_sha = sha_bytes(self_bytes)
    ref_p = os.path.join(REPO, "src/python/rule30_research_reference.py")
    with open(ref_p, "rb") as f:
        ref_bytes = f.read()
    ref_sha = sha_bytes(ref_bytes)
    cpu_model = "unavailable"
    try:
        with open("/proc/cpuinfo") as fp:
            for line in fp:
                if line.startswith("model name"):
                    cpu_model = line.split(":", 1)[1].strip()
                    break
    except Exception:
        pass
    git_head = run(["git", "rev-parse", "HEAD"])
    git_log = run(["git", "log", "-1", "--format=%H %ci %s"])
    git_status = run(["git", "status", "--porcelain"])
    mem_total = "unavailable"
    try:
        with open("/proc/meminfo") as fp:
            for line in fp:
                if line.startswith("MemTotal"):
                    mem_total = line.strip()
                    break
    except Exception:
        pass
    try:
        peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:
        peak_kb = None
    checks = {
        "x0": hex(X0),
        "from_zero_history": FROM_ZERO,
        "observed_branches": BRANCHES,
        "orbit": [hex(v) for v in orbit],
        "final_gate_unexecuted": int(x10 & 15),
        "histories": hist,
        "x4": {"x": hex(x4), "cert": c4},
        "x10": {"x": hex(x10), "cert": c10},
        "decision": decision,
    }
    canonical = json.loads(json.dumps(checks, sort_keys=True))
    payload_sha = sha_bytes(json.dumps(canonical, sort_keys=True).encode("utf-8"))
    record = {
        "experiment_id": "20260906_activity_return_nonincrease_primary",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_head,
        "git_log": git_log,
        "git_status": git_status[:2000],
        "question": "problem1",
        "hypothesis": "Named control: R(x10)<=R(x4) on the fixed u18 return block times4..10 (x0=0x6473d46ab, branches ttttututut, final u gate confirmed unexecuted).",
        "backend": "python3-packed-int-ordinary-history",
        "parameters": {
            "x0": hex(X0), "from_zero_history": FROM_ZERO, "root": ROOT,
            "observed_branches": BRANCHES, "final_gate": "u_unexecuted",
            "block": "times4..10", "cpu": 1, "time_cap_s": 120,
            "mem_cap": "1GiB", "max_tail_transitions_per_endpoint": MAX_TAIL,
        },
        "hardware": {"uname": list(platform.uname()), "cpu_count": os.cpu_count(), "cpu_model": cpu_model, "mem_total": mem_total, "peak_rss_kb": peak_kb},
        "software": {"python": sys.version, "executable": sys.executable},
        "runtime_seconds": time.perf_counter() - t_all,
        "result_hashes": {"primary_payload_sha256": payload_sha, "note_sha256": note_sha, "self_sha256": self_sha, "reference_sha256": ref_sha},
        "result_summary": {
            "R_x4": c4["R"], "R_x10": c10["R"], "decision": decision,
            "x4_n": c4["n"], "x10_n": c10["n"],
            "x4_tail": [c4["tail_entry_age"], c4["tail_cycle_length"], c4["maximizer_age"], c4["tail_transitions"]],
            "x10_tail": [c10["tail_entry_age"], c10["tail_cycle_length"], c10["maximizer_age"], c10["tail_transitions"]],
        },
        "interpretation": ("Named control holds" if decision == "nonincrease_holds" else "Named nonincrease REFUTED") + ": R(x4)=%d R(x10)=%d. One exact control only." % (c4["R"], c10["R"]),
        "status": "finite-exhaustive",
        "proof_scope": "Exact closed endpoint-vector orbits for the two named prescribed histories; all-age maxima from first-repeat closure plus direct ages 0..n-1.",
        "corrections": ["Regenerated: fixed summary x10_n typo (21->27); maximizer now earliest across direct and tail on ties (x10 33->25); added immutable-reference hash and CPU model. Score streams and R values unchanged.", "Reloadability: histories keys are strings and payload hash is over JSON-roundtripped canonical checks, so sha256 of the reloaded checks reproduces primary_payload_sha256."],
        "reference": {"path": "src/python/rule30_research_reference.py", "sha256": ref_sha},
        "limitations": ["Single named return block; no all-depth inequality inferred.", "Independent cell/projection comparison pending in the separate lead-owned checker.", "Inconclusive (not refuting) if any cap were reached; no cap was reached."],
        "admission": {"note": NOTE_REL, "note_sha256": note_sha, "note_text": note_text},
        "self_source": {"path": SELF_REL, "sha256": self_sha, "embedded_text": self_bytes.decode("utf-8")},
        "checks": checks,
    }
    out_p = os.path.join(REPO, OUT_REL)
    os.makedirs(os.path.dirname(out_p), exist_ok=True)
    tmp_p = out_p + ".tmp." + str(os.getpid())
    fp = open(tmp_p, "w")
    json.dump(record, fp, indent=1)
    fp.flush()
    os.fsync(fp.fileno())
    fp.close()
    os.replace(tmp_p, out_p)
    print("wrote " + out_p)
    print("R_x4=%d R_x10=%d %s" % (c4["R"], c10["R"], decision))
    print("x4 tail entry=%d cycle=%d maxage=%d trans=%d" % (c4["tail_entry_age"], c4["tail_cycle_length"], c4["maximizer_age"], c4["tail_transitions"]))
    print("x10 tail entry=%d cycle=%d maxage=%d trans=%d" % (c10["tail_entry_age"], c10["tail_cycle_length"], c10["maximizer_age"], c10["tail_transitions"]))
    print("payload_sha=" + payload_sha)


main()
