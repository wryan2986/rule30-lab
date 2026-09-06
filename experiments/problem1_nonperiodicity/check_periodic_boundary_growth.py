#!/usr/bin/env python3
"""Bounded periodic boundary-growth laws on named rational schedules.

Reuses ONLY the stored phase certificates for t, u, ututtt, ttututt in
results/problem1/20260905_periodic_rational_primary.json, plus the explicit
ut control pair -7/127 and -123/127 from the periodic-tail probe. No
rational recurrence or cycle is regenerated and no cap is increased.

Hypothesis under test: some admissible stored periodic schedule has
boundary mean >= 1 in some phase alignment, which would refute a uniform
subunit boundary bound by an exact periodic countermodel. Otherwise each
named schedule gets an exact all-age growth law and the broader subunit
bound stays open with no extension authorized.

Whole-tail relevance (either outcome matters): a countermodel forces any
future whole-tail argument to rely on ordinary membership or ordered-history
information rather than a schedule-only slope; absence of a countermodel
closes exactly these named periodic classes and leaves the general
inequality open, directing work toward history-sensitive observables.
Method A evaluates the score period from stored rational
numerators/denominators via 2-adic modular inversion. Method B replays the
same score period from stored spatial bit vectors (columns), or from the
constructive 7-bit words for the ut control. Both methods are labelled.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
from fractions import Fraction
from pathlib import Path
import platform
import subprocess
import tempfile
import time
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "results/problem1/20260905_periodic_rational_primary.json"
OUT = ROOT / "results/problem1/20260906_periodic_boundary_growth_primary.json"
WALL_CAP = 120
ADMISSION = """Bounded unit: reuse the four stored exact phase-cycle certificates
(t, u, ututtt, ttututt) plus the explicit ut control (-7/127, -123/127).
For schedule period p, spatial onset a, spatial period lam, d0=ceil(a/2),
L=lcm(p, lam/gcd(lam,2)), w_e(d)=J(pi^d X_(e-d mod p)),
M_e=sum_{d=d0}^{d0+L-1} w_e(d) with J=I(Ay)+I(pi y) testing low six bits
0/5. Growth law Psi_(s+L)(X_j)=Psi_s(X_j)+M_(j+s-2 mod p) for s>=d0+1.
Compute M_e exactly via modular inversion (method A) and replay via stored
spatial bit vectors (method B). t/u are inadmissible controls, never
countermodels. Either outcome changes the whole-tail argument as stated in
the module docstring. Local one CPU, 120 s, 1 GiB. No recurrence
regeneration, no cap increase, no new search."""
FORBIDDEN = ("uu", "ttttt", "ututtu")
def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(value, f, sort_keys=True, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
def admissible_cyclic(word):
    rep = word * (2 + 6 // len(word))
    return all(b not in rep for b in FORBIDDEN)
def A_of(v):
    return (v >> 2) ^ ((v >> 1) | v)
def I_of(z):
    return 1 if (z & 63) in (0, 5) else 0
def J_of(y):
    return I_of(A_of(y)) + I_of(y >> 2)
UT_WORDS = (7, 123)
def load_cases():
    data = json.loads(INPUT.read_text())
    rows = {r["q"]: r for r in data["result_summary"]["rows"]}
    cases = []
    for q in ("t", "u", "ututtt", "ttututt"):
        rec = rows[q]
        p = len(q)
        a = rec["spatial_onset"]
        lam = rec["lambda"]
        ph = sorted(rec["rational_phases"], key=lambda d: d["phase"])
        assert [d["phase"] for d in ph] == list(range(p))
        phases = [(int(d["numerator_hex"], 16), int(d["denominator_hex"], 16)) for d in ph]
        for _, den in phases:
            assert den & 1, "denominator must be odd for 2-adic inversion"
        cases.append({"q": q, "p": p, "a": a, "lam": lam, "phases": phases,
                      "cols": rec["columns"], "kind": "stored-certificate"})
    cases.append({"q": "ut", "p": 2, "a": 0, "lam": 7,
                  "phases": [(-7, 127), (-123, 127)], "cols": None,
                  "kind": "explicit-probe-control"})
    return cases
def bit_at(case, j, i):
    if case["cols"] is not None:
        cols, a, lam = case["cols"], case["a"], case["lam"]
        if i >= a:
            i = a + (i - a) % lam
        return (cols[i] >> j) & 1
    w = UT_WORDS[j]
    return (w >> (i % case["lam"])) & 1
def run_case(case):
    t0 = time.monotonic()
    p, a, lam = case["p"], case["a"], case["lam"]
    d0 = (a + 1) // 2
    base = lam // math.gcd(lam, 2)
    L = math.lcm(p, base)
    Dmax = d0 + 2 * L + 4
    N = 2 * Dmax + 12
    M = 1 << N
    Xa = [((num % M) * pow(den, -1, M)) % M for num, den in case["phases"]]
    Xb = [sum(bit_at(case, j, i) << i for i in range(N)) for j in range(p)]
    W = [[0] * (Dmax + 1) for _ in range(p)]
    Wb = [[0] * (Dmax + 1) for _ in range(p)]
    for e in range(p):
        for d in range(Dmax + 1):
            j = (e - d) % p
            W[e][d] = J_of(Xa[j] >> (2 * d))
            Wb[e][d] = J_of(Xb[j] >> (2 * d))
    method_agreement = (W == Wb)
    assert method_agreement, "method A/B score-period mismatch for " + case["q"]
    Me = [sum(W[e][d0:d0 + L]) for e in range(p)]
    P = [[0] * (Dmax + 2) for _ in range(p)]
    for e in range(p):
        acc = 0
        for d in range(Dmax + 1):
            acc += W[e][d]
            P[e][d + 1] = acc
    def Psi(s, j):
        if s <= 1:
            return 0
        return P[(j + s - 2) % p][s - 1]
    n_ok, n_tot = 0, 0
    for j in range(p):
        for s in range(d0 + 1, d0 + L + 3):
            n_tot += 1
            if Psi(s + L, j) - Psi(s, j) == Me[(j + s - 2) % p]:
                n_ok += 1
    assert n_ok == n_tot, "growth-law identity failed for " + case["q"]
    adm = admissible_cyclic(case["q"])
    slopes = [Fraction(m, L) for m in Me]
    overall = Fraction(sum(Me), p * L)
    offsets = [Psi(d0 + 1, j) for j in range(p)]
    is_counter = bool(adm and any(m >= L for m in Me))
    return {"q": case["q"], "kind": case["kind"], "p": p, "a": a, "lambda": lam,
            "d0": d0, "L": L, "admissible_cyclic": adm,
            "M_per_phase": Me, "slopes_per_phase": [str(s) for s in slopes],
            "score_period_sha256": digest([W[e][d0:d0+L] for e in range(p)]),
            "initial_scores_sha256": digest([W[e][:d0] for e in range(p)]),
            "overall_mean": str(overall), "offsets_at_d0_plus_1": offsets,
            "growth_checks_passed": n_ok, "growth_checks_total": n_tot,
            "method_A_B_agree": True, "is_countermodel": is_counter,
            "runtime_seconds": time.monotonic() - t0}
def main():
    started = time.monotonic()
    cases = load_cases()
    rows = [run_case(c) for c in cases]
    if time.monotonic() - started > WALL_CAP:
        raise TimeoutError("admitted wall cap exceeded")
    counter = [r["q"] for r in rows if r["is_countermodel"]]
    inad = [r["q"] for r in rows if not r["admissible_cyclic"]]
    summary = {"rows": rows, "countermodels": counter,
               "inadmissible_controls": inad,
               "hypothesis_outcome": ("REFUTED subunit bound: " + ",".join(counter)) if counter else "no admissible schedule reaches mean>=1; named classes get exact growth laws, broader bound stays open"}
    cpu = next((x.split(":", 1)[1].strip() for x in Path("/proc/cpuinfo").read_text().splitlines() if x.startswith("model name")), "unknown")
    paths = [Path(__file__).relative_to(ROOT), INPUT.relative_to(ROOT),
             Path("src/python/rule30_research_reference.py")]
    record = {"experiment_id": "20260906_periodic_boundary_growth_primary",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True).strip(),
        "question": "problem1",
        "hypothesis": "Some admissible stored periodic schedule has boundary mean>=1; else named controls get exact all-age growth laws.",
        "backend": "python-rational-modinv-and-bitvector",
        "parameters": {"schedules": [c["q"] for c in cases], "score": "J=I(Ay)+I(pi y), I=1 iff low6bits in {0,5}",
            "law": "Psi_(s+L)(X_j)=Psi_s(X_j)+M_(j+s-2 mod p), s>=d0+1", "wall_seconds": WALL_CAP, "memory_limit_gib": 1},
        "hardware": {"cpu": cpu, "machine": platform.machine(), "logical_cpu_count": os.cpu_count()},
        "software": {"python": platform.python_version(), "platform": platform.platform()},
        "runtime_seconds": time.monotonic() - started,
        "source_and_input_hashes": {str(p): hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
        "admission_snapshot": ADMISSION, "executed_source": Path(__file__).read_text(),
        "result_hashes": {"summary_sha256": digest(summary)},
        "result_summary": summary, "status": "finite-exhaustive",
        "interpretation": "The finite computations verify score periods and increments on the named certificates. The separate proof in problem1_periodic_boundary_growth.md derives all-age laws from spatial-tail periodicity and reversal of the boundary-sum index; t/u are inadmissible controls only.",
        "proof_scope": "Only the four stored certificates plus the explicit ut control; no regenerated recurrences, no new search, no cap increase.",
        "limitations": ["No claim about arbitrary or ordinary schedules.", "Growth-law identity depends on the separate mathematical note; this record supplies exact M_e, slopes, offsets and finite identity checks.", "Both methods ran locally in the Muse worker implementation; the lead cell-vector replay is a separate record.", "Lead integration corrected the proof-dependency and executor wording and added score-period hashes before this final run.", "Base Git plus source/input hashes identify exact contents."]}
    atomic(OUT, record)
    print(json.dumps({r["q"]: {k: r[k] for k in ("L", "M_per_phase", "overall_mean", "admissible_cyclic", "is_countermodel", "growth_checks_passed")} for r in rows}))
if __name__ == "__main__":
    main()
