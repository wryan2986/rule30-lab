"""Primary fixed checks for the temporal activity deficit note.

Method: modular 2-adic bit operations at precision 2**128 with the
A-diagonal form of D_s. The independent lead method uses direct-T
cell arrays with rational long division and is not implemented here.

Admitted finite domains only (see admission snapshot in the record):
  * 12 named rational inputs in fixed order, ages 1..16: exact D_s / Z_s
    and temporal-order score vectors (r = 0..s-1).
  * finite-entry certificates h/k with the max(h,k) bound check.
  * 256 local eight-bit neighborhoods (charge-5 transition).
  * 64 length-three temporal word pairs (last-activity identity).
  * exact rational harmonic thresholds K = 0, 1, 2.
  * gate replay: exactly first 2 updates each for x = 7 and x = 43;
    x = 7 afterward 111 verifies stopped; 43 not continued longer.
  * forced seam identity on inputs 7 and 43, ages 1..16.
Single CPU, stdlib only. No other input is admitted.
"""
import hashlib
import json
import os
import platform
from pathlib import Path
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction

REPO = str(Path(__file__).resolve().parents[2])
NOTE_REL = "proofs/informal/problem1_temporal_activity_deficit.md"
V_NOTE_REL = "proofs/informal/problem1_single_column_activity.md"
SELF_REL = "experiments/problem1_nonperiodicity/check_temporal_activity_deficit_primary.py"
OUT_REL = "results/problem1/20260906_temporal_activity_deficit_primary.json"
REF_REL = "src/python/rule30_research_reference.py"
MOD_BITS = 128
MASK = (1 << MOD_BITS) - 1
AGES = list(range(1, 17))
ORDER = ["0", "1", "2", "3", "5", "7", "-1", "-2", "-3", "-1/7", "1/3", "-1/3"]

def inv_odd(a):
    a &= MASK
    x = 1
    for _ in range(7):
        x = (x * (2 - a * x)) & MASK
    return x

def Tmod(v):
    return (v ^ ((((v << 1) & MASK) | ((v << 2) & MASK)))) & MASK

def pimod(v):
    return (v >> 2) & MASK

def Amob(v):
    return Tmod(v) >> 2

def apow(v, k):
    for _ in range(k):
        v = Amob(v)
    return v

def I64(v):
    return 1 if (v & 63) in (0, 5) else 0

def Texact_small(v):
    return v ^ ((v << 1) | (v << 2))

def Aexact_small(v):
    return Texact_small(v) >> 2

def D_of(s, x):
    tot = 0
    for d in range(s):
        tot += I64(apow(x >> (2 * d), s - 1 - d))
    return tot

def scores_of(s, x):
    return [I64(apow(x >> (2 * (s - 1 - r)), r)) for r in range(s)]

def v_bits(s, x):
    return [apow(x >> (2 * (s - t)), t) & 1 for t in range(s)]

def V_of(s, x):
    return sum(v_bits(s, x))

def Jon(w):
    return I64(Amob(w)) + I64(pimod(w))

def Fon(x):
    return ((4 * apow(x, 2)) + 3) & MASK

def last_active3(w):
    m = -1
    for t in range(3):
        if (w >> t) & 1:
            m = t
    return m

def run(cmd):
    try:
        p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=30)
        return p.stdout.strip()
    except Exception as e:
        return "unavailable: " + str(e)

def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()

def main():
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_AS, (1024 ** 3, 1024 ** 3))
    t_all = time.perf_counter()
    phases = {}
    t0 = time.perf_counter()
    INV3 = inv_odd(3)
    INV7 = inv_odd(7)
    assert (3 * INV3) & MASK == 1
    assert (7 * INV7) & MASK == 1
    X = {
        "0": 0, "1": 1, "2": 2, "3": 3, "5": 5, "7": 7,
        "-1": (-1) & MASK, "-2": (-2) & MASK, "-3": (-3) & MASK,
        "-1/7": (-INV7) & MASK, "1/3": INV3, "-1/3": (-INV3) & MASK,
    }
    phases["setup"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    dz_rows = []
    dz_ok = True
    for name in ORDER:
        x = X[name]
        for s in AGES:
            sc = scores_of(s, x)
            D = sum(sc)
            Z = s - D
            if not (0 <= Z <= s and D + Z == s):
                dz_ok = False
            dz_rows.append({"input": name, "s": s, "temporal_scores": sc, "D": D, "Z": Z})
    phases["dz"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    entry = {}
    entry_ok = True
    stipulated = {name: (0, int(name)) for name in ORDER[:6]}
    stipulated.update({"-1": (1, 1), "-2": (1, 2), "-3": (1, 3), "-1/7": (2, 1)})
    for name in ORDER:
        x = X[name]
        if name not in stipulated:
            entry[name] = {"h": None, "c": None, "k": None, "bound_ok": None,
                           "note": "no finite-entry claim; exact two-cycle proved separately"}
        else:
            h, c = stipulated[name]
            v = x
            for _ in range(h):
                v = Tmod(v)
            assert v == c  # finite modular corroboration of the stipulated identity
            k = (c.bit_length() + 1) // 2
            ok = True
            for s in AGES:
                Z = s - D_of(s, x)
                if Z > min(s, max(h, k)):
                    ok = False
            entry[name] = {"h": h, "c": c, "k": k, "bound_ok": ok,
                           "note": "stipulated exact entry; equality checked only modulo 2**128 here"}
            entry_ok = entry_ok and ok
    swap_ok = (Tmod(X["1/3"]) == X["-1/3"] and Tmod(X["-1/3"]) == X["1/3"])
    thirds_ok = True
    for name in ("1/3", "-1/3"):
        for s in AGES:
            if s - D_of(s, X[name]) != s:
                thirds_ok = False
    phases["entry"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    local_rows = []
    local_ok = True
    images5 = set()
    for v in range(256):
        w = (v >> 2) & 63
        Tv = Texact_small(v)
        z = (Tv >> 2) & 63
        imp = True if (w != 5 or z not in (0, 5)) else False
        if not imp:
            local_ok = False
        if w == 5:
            images5.add(z)
        local_rows.append([v, w, z, imp])
    phases["local"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    temporal_rows = []
    temporal_ok = True
    for a in range(8):
        for b in range(8):
            u = [(((a >> t) & 1) | ((b >> t) & 1)) for t in range(3)]
            c = [0, 0, 0, 0]
            c[3] = 0
            for t in (2, 1, 0):
                c[t] = c[t + 1] ^ u[t]
            cc = c[0] | (c[1] << 1) | (c[2] << 2)
            la = last_active3(a)
            lb = last_active3(b)
            lc = last_active3(cc)
            ok = (lc == max(la, lb))
            if not ok:
                temporal_ok = False
            temporal_rows.append([a, b, cc, la, lb, lc])
    phases["temporal"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    harmonic = {}
    harmonic_ok = True
    for K in (0, 1, 2):
        s = Fraction(0, 1)
        r = 0
        while True:
            s = s + Fraction(1, 2 * r + 1)
            if s > 2 * K:
                break
            r = r + 1
        prev = s - Fraction(1, 2 * r + 1)
        harmonic[str(K)] = {
            "K": K, "h": r,
            "sum_num": s.numerator, "sum_den": s.denominator,
            "prev_num": prev.numerator, "prev_den": prev.denominator,
        }
        if not (prev <= 2 * K < s):
            harmonic_ok = False
    phases["harmonic"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    F7 = 4 * Aexact_small(Aexact_small(7)) + 3
    F27 = 4 * Aexact_small(Aexact_small(27)) + 3
    F43 = 4 * Aexact_small(Aexact_small(43)) + 3
    F203 = 4 * Aexact_small(Aexact_small(203)) + 3
    gates = {"x7": [7, F7, F27], "x43": [43, F43, F203]}
    gates_ok = (F7 == 27 and F27 == 111 and F43 == 203)
    stopped111 = ((111 & 15) not in (7, 11))
    gates_ok = gates_ok and stopped111
    gate7 = 7 & 15
    gate43 = 43 & 15
    gates_ok = gates_ok and gate7 == 7 and gate43 == 11
    if Fon(7) != 27 or Fon(43) != 203:
        gates_ok = False
    seam_rows = []
    seam_ok = True
    for name, xv in (("7", 7), ("43", 43)):
        Fx = Fon(xv)
        for s in AGES:
            Zl = (s + 1) - D_of(s + 1, xv)
            Zr = s - D_of(s, Fx)
            lhs = Zl - Zr
            term_i = I64(apow(Fx, s - 1))
            term_j = Jon(xv >> (2 * (s - 1)))
            rhs = 1 + term_i - term_j
            ok = (lhs == rhs) and (-1 <= lhs <= 2)
            if not ok:
                seam_ok = False
            seam_rows.append({"input": name, "s": s, "Z_next": Zl, "Z_F": Zr,
                              "I": term_i, "J": term_j, "lhs": lhs, "rhs": rhs, "ok": ok})
    phases["gates_seam"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    v_rows, v_entry_bounds, v_comparisons, v_seams = [], [], [], []
    for name in ORDER:
        x = X[name]
        vals = []
        for s in range(17):
            bits = v_bits(s, x)
            value = sum(bits)
            vals.append(value)
            v_rows.append({"input": name, "s": s, "temporal_bits": bits, "V": value})
            if name in stipulated:
                h, c = stipulated[name]
                k = (c.bit_length() + 1) // 2
                bound = min(s, max(h, k - 1))
                assert value <= bound
                v_entry_bounds.append([name, s, h, k, value, bound])
            if s:
                assert value <= 2 * (s - D_of(s, x)) + 1
        for s in range(1, 15):
            z = s - D_of(s, x)
            upper = vals[s - 1] + 3 * vals[s] + 3 * vals[s + 1] + 2 * vals[s + 2] + 2
            assert z <= upper
            v_comparisons.append([name, s, vals[s], z, upper])
    for x in (7, 43):
        for s in range(1, 16):
            vx, vf = V_of(s + 1, x), V_of(s, Fon(x))
            b0 = (x >> (2 * s + 2)) & 1
            b1 = (Tmod(x) >> (2 * s + 2)) & 1
            end = apow(x, s + 1) & 1
            assert vx - vf == b0 + b1 - end
            assert -1 <= vx - vf <= 2
            v_seams.append({"x": x, "s": s, "V_next_age": vx, "V_forced": vf,
                            "initial_bit": b0, "next_bit": b1, "aged_bit": end,
                            "difference": vx - vf})
    phases["single_column"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    note_p = os.path.join(REPO, NOTE_REL)
    with open(note_p, "rb") as f:
        note_bytes = f.read()
    note_sha = sha_bytes(note_bytes)
    note_text = note_bytes.decode("utf-8")
    v_note_bytes = Path(REPO, V_NOTE_REL).read_bytes()
    a0 = note_text.find("## Admission and route selection")
    a1 = note_text.find("## 1.")
    admission_text = note_text[a0:a1].strip() if (a0 >= 0 and a1 > a0) else ""
    self_p = os.path.join(REPO, SELF_REL)
    with open(self_p, "rb") as f:
        self_bytes = f.read()
    self_sha = sha_bytes(self_bytes)
    ref_p = os.path.join(REPO, REF_REL)
    with open(ref_p, "rb") as f:
        ref_bytes = f.read()
    ref_sha = sha_bytes(ref_bytes)
    git_head = run(["git", "rev-parse", "HEAD"])
    git_log = run(["git", "log", "-1", "--format=%H %ci %s"])
    git_status = run(["git", "status", "--porcelain"])
    mem_total = ""
    try:
        fp = open("/proc/meminfo")
        for line in fp:
            if line.startswith("MemTotal"):
                mem_total = line.strip()
                break
        fp.close()
    except Exception:
        mem_total = "unavailable"
    peak_kb = None
    try:
        peak_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:
        peak_kb = None
    phases["provenance"] = time.perf_counter() - t0
    checks = {
        "dz_rows": dz_rows,
        "entry": entry,
        "thirds_swap_ok": swap_ok,
        "thirds_Zeqs_ok": thirds_ok,
        "local256": {"rows": local_rows, "charge5_images": sorted(images5)},
        "temporal64": {"rows": temporal_rows},
        "harmonic": harmonic,
        "gates": gates,
        "stopped111": stopped111,
        "gate43_endpoint_note": "803 recorded as orbit endpoint; its gate not evaluated per admission",
        "seam_rows": seam_rows,
        "v_rows": v_rows,
        "v_entry_bounds": v_entry_bounds,
        "v_comparisons": v_comparisons,
        "v_seams": v_seams,
    }
    payload_sha = sha_bytes(json.dumps(checks, sort_keys=True).encode("utf-8"))
    all_ok = dz_ok and entry_ok and swap_ok and thirds_ok and local_ok and temporal_ok and harmonic_ok and gates_ok and seam_ok
    assert all_ok
    assert time.perf_counter() - t_all < 120
    record = {
        "experiment_id": "20260906_temporal_activity_deficit_primary",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_head,
        "git_log": git_log,
        "git_status": git_status[:2000],
        "question": "problem1",
        "hypothesis": "Admitted finite controls of the temporal activity deficit note: A-diagonal D_s/Z_s values on 12 named inputs x ages 1..16 with temporal-order score vectors; finite-entry max(h,k) bound; charge-5 local transition on 256 neighborhoods; last-activity identity on 64 temporal word pairs; exact harmonic thresholds K=0,1,2; gate replay of first 2 updates for x=7,43 with 111 stopped; one-step deficit seam identity and bounds.",
        "backend": "python3-modular-A-diagonal",
        "parameters": {
            "inputs": ORDER, "ages": AGES, "mod_bits": MOD_BITS,
            "dz_rows": 192, "local_rows": 256, "temporal_rows": 64,
            "harmonic_K": [0, 1, 2], "seam_inputs": ["7", "43"],
            "gate_updates_each": 2, "cpu": 1, "time_cap_s": 120, "mem_cap": "1GiB",
            "V_ages": [0, 16], "V_comparison_ages": [1, 14], "V_seam_ages": [1, 15],
        },
        "hardware": {"uname": list(platform.uname()), "cpu_count": os.cpu_count(), "mem_total": mem_total, "peak_rss_kb": peak_kb},
        "software": {"python": sys.version, "executable": sys.executable},
        "runtime_seconds": time.perf_counter() - t_all,
        "phase_seconds": phases,
        "result_hashes": {"primary_payload_sha256": payload_sha, "note_sha256": note_sha, "self_sha256": self_sha, "reference_sha256": ref_sha},
        "result_summary": {
            "dz_rows": len(dz_rows), "dz_ok": dz_ok,
            "entry": {k: {"h": v["h"], "c": v["c"], "k": v["k"], "bound_ok": v["bound_ok"]} for k, v in entry.items()},
            "entry_ok": entry_ok, "thirds_swap_ok": swap_ok, "thirds_Zeqs_ok": thirds_ok,
            "local_rows": len(local_rows), "local_ok": local_ok,
            "temporal_rows": len(temporal_rows), "temporal_ok": temporal_ok,
            "harmonic": {k: {"h": v["h"], "sum": "%d/%d" % (v["sum_num"], v["sum_den"])} for k, v in harmonic.items()},
            "harmonic_ok": harmonic_ok,
            "gates": gates, "gates_ok": gates_ok, "stopped111": stopped111,
            "seam_rows": len(seam_rows), "seam_ok": seam_ok,
            "v_rows": len(v_rows), "v_entry_bounds": len(v_entry_bounds),
            "v_comparisons": len(v_comparisons), "v_seams": len(v_seams),
            "all_ok": all_ok,
        },
        "interpretation": "PASS: all admitted finite controls agree." if all_ok else "FAIL: a finite control mismatches; see flags.",
        "status": "finite-exhaustive",
        "proof_scope": "Exact finite identities on declared domains: 192 D/Z rows with temporal-order score vectors; 256 local rows; 64 temporal rows; 3 exact harmonic thresholds; 32 seam rows; gate orbits [7,27,111] and [43,203,803] with stopped-111. D/Z/score/seam outputs need at most 40 low bits and are exact under 128-bit modular arithmetic. Finite-entry h/c matches are congruences mod 2**128 corroborating exact note identities.",
        "limitations": [
            "Finite-entry h/c certificates are modular (mod 2**128) corroborations, not standalone 2-adic equality proofs.",
            "Finite agreement cannot establish compactness, limit, or all-depth implications; those need derivation and review.",
            "Lead direct-T cell comparison pending; no occurrence, frontier, or width claims made.",
            "Gate of orbit endpoint 803 not evaluated per admission.",
        ],
        "admission": {"note": NOTE_REL, "note_sha256": note_sha, "admission_text": admission_text,
                      "note_text": note_text, "V_note": V_NOTE_REL,
                      "V_note_sha256": sha_bytes(v_note_bytes), "V_note_text": v_note_bytes.decode()},
        "integration": {"executor": "lead Astra",
                        "primary_method_origin": "Muse partial implementation before its second provider429",
                        "corrections": ["Removed unadmitted modular finite-entry detection; use exact stipulated identities.",
                                        "Added separately admitted single-column A-diagonal controls.",
                                        "Enforced resources and portable root; embedded both full executed notes."],
                        "superseded_record": "results/problem1/20260906_temporal_activity_deficit_initial.json"},
        "self_source": {"path": SELF_REL, "sha256": self_sha, "embedded_text": self_bytes.decode("utf-8")},
        "reference": {"path": REF_REL, "sha256": ref_sha},
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
    print("all_ok=" + str(all_ok))
    print("harmonic=" + str({k: v["h"] for k, v in harmonic.items()}))
    print("entry=" + str({k: (v["h"], v["c"], v["k"]) for k, v in entry.items()}))
    print("payload_sha=" + payload_sha)

main()
