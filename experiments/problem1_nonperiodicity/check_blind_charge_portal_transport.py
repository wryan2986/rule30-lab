#!/usr/bin/env python3
"""Bounded counterexample test of naive nonincrease of the blind charge.

Conjecture: whenever the first zero return z of the doubled portal of a
finite terminating odd word w is an odd singleton, kappa(z) <= kappa(w),
with kappa(w) = sum_{r=1..min(p-1,h)} max(k_r(w)-1, 0) over the dynamic
layers of w's doubled portal up to its first all-zero layer h.

Domain: the eight known odd singleton p32 root certificates of
results/problem1/20261002_period32_complete_portal_root_census.json.
The source word of portal i is P16_LEAVES[i] of analyze_blind_visit_rank.py;
the target is that root's canonical_target.

Admission: one violating portal kills naive nonincrease under an actual
singleton portal. No violation leaves this exact bounded test insufficient.
Nothing here proves or refits an infinite statement.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CENSUS = ROOT / "results/problem1/20261002_period32_complete_portal_root_census.json"
SOURCES = [
    Path(__file__).resolve(),
    HERE / "analyze_blind_visit_rank.py",
    HERE / "check_cyclic_blind_cone_independent.py",
    ROOT / "proofs/informal/problem1_cyclic_blind_cone_bound.md",
    ROOT / "src/python/rule30_research_reference.py",
]

sys.path.insert(0, str(HERE))
import analyze_blind_visit_rank as A  # noqa: E402


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
            temporary = Path(f.name)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
        temporary = None
        fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def packed_step(st: int, r: int, label: int) -> int:
    """Eq. (1) of the blind-cone lemma, boundaries reinserted each step."""
    xm2, xm1, ym2, ym1 = 1, 0, 0, 1
    out = 0
    for j in range(r):
        x = (st >> (2 * j)) & 1
        y = (st >> (2 * j + 1)) & 1
        d = ym2 ^ ym1 ^ y ^ (xm1 & y) ^ (ym1 & x) ^ (ym1 & y)
        f = xm2 ^ (xm1 | x)
        out |= (f ^ (label & d)) << (2 * j)
        out |= d << (2 * j + 1)
        xm2, xm1, ym2, ym1 = xm1, x, ym1, y
    return out


def flat(st: int, r: int) -> tuple[int, ...]:
    """Flat 2r binary bits (X1,Y1,X2,Y2,...): the encoding the independent
    two-row verifier consumes. Never r packed pair codes."""
    return tuple((st >> i) & 1 for i in range(2 * r))


def step_tuple(st: int, r: int, label: int) -> tuple[int, ...]:
    return flat(packed_step(st, r, label), r)


def check_transition_agreement(cone) -> int:
    """Cross-check packed_step and blind_state against the independent
    two-row Rule 30 implementation."""
    cases = 0
    for r in range(1, 6):
        for st in range(1 << (2 * r)):
            for label in (0, 1):
                if cone.step(flat(st, r), label) != flat(packed_step(st, r, label), r):
                    raise AssertionError(("transition", r, st, label))
                cases += 1
            if cone.blind(flat(st, r)) != A.blind_state(st, r):
                raise AssertionError(("blind", r, st))
            cases += 1
    return cases


def dynamic_layers(word: str, max_r: int) -> list[int]:
    """Retain the first all-zero layer if encountered; stop before trying
    to build its non-unique or period-doubling child."""
    p = len(word)
    w = A.parse_lsb(word)
    n = 2 * p
    low, high = A.portal_lift(w, p), (1 << n) - 1
    layers: list[int] = []
    for _ in range(max_r):
        if low == 0:
            break
        ch = A.broad_child(low, high, n)
        layers.append(ch)
        high, low = low, ch
    return layers


def states_from_layers(w: int, p: int, layers: list[int], r: int) -> list[int]:
    x = A.portal_lift(w, p)
    seq = []
    for s in range(p):
        q = (x >> s) & 1
        st = 0
        for j, z in enumerate(layers[:r]):
            X = (z >> s) & 1
            Y = X ^ ((z >> (s + p)) & 1)
            if q:
                X ^= Y
            st |= X << (2 * j)
            st |= Y << (2 * j + 1)
        seq.append(st)
    return seq


def profile(word: str, max_r: int) -> tuple[list[int], int, bool]:
    """Exact k_r for r=1..max_r, the effective height, and whether the
    retained prefix was cut by the depth bound rather than by a zero layer."""
    p = len(word)
    w = A.parse_lsb(word)
    layers = dynamic_layers(word, max_r)
    ks = []
    for r in range(1, len(layers) + 1):
        st = states_from_layers(w, p, layers, r)
        if st != A.quotient_seq(w, p, r):
            raise AssertionError(("layer mismatch", word, r))
        ks.append(sum(A.blind_state(s, r) for s in st))
    return ks, len(layers), len(layers) == max_r and layers[-1] != 0


def kappa(ks: list[int], height: int, p: int) -> tuple[int, int]:
    top = min(p - 1, height)
    return sum(max(ks[r - 1] - 1, 0) for r in range(1, top + 1)), top


def check_cyclic(word: str, retained_layers: int, cases: int, cone) -> int:
    """Apply the tuple transition with the driver's own label (w>>s)&1 at
    every returned state, including wraparound, instead of trusting the
    quotient_seq profiles."""
    p = len(word)
    w = A.parse_lsb(word)
    for r in range(1, retained_layers + 1):
        seq = A.quotient_seq(w, p, r)
        for s in range(p):
            if step_tuple(seq[s], r, (w >> s) & 1) != flat(seq[(s + 1) % p], r):
                raise AssertionError(("not cyclic", word, r, s))
            if cone.step(flat(seq[s], r), (w >> s) & 1) != flat(seq[(s + 1) % p], r):
                raise AssertionError(("independent two-row cycle", word, r, s))
            if cone.blind(flat(seq[s], r)) != A.blind_state(seq[s], r):
                raise AssertionError(("independent deep blindness", word, r, s))
            cases += 1
    return cases


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "results/problem1/20261002_blind_charge_portal_transport.json")
    parser.add_argument("--max-p16-depth", type=int, default=15)
    parser.add_argument("--max-p32-depth", type=int, default=31)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--max-memory-mib", type=int, default=256)
    parser.add_argument("--max-output-kib", type=int, default=128)
    args = parser.parse_args()
    if args.max_p16_depth != 15 or args.max_p32_depth != 31:
        parser.error("Exact charge evaluation requires the proved depths 15 and 31.")
    if min(args.max_seconds, args.max_memory_mib, args.max_output_kib) <= 0:
        parser.error("Resource caps must be positive.")
    resource.setrlimit(resource.RLIMIT_AS, (args.max_memory_mib * 2**20,) * 2)
    started = time.monotonic()

    def cap() -> None:
        if time.monotonic() - started > args.max_seconds:
            raise TimeoutError("wall-time cap reached; no final record written")

    spec = importlib.util.spec_from_file_location(
        "cone", HERE / "check_cyclic_blind_cone_independent.py")
    cone = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cone)
    reference = ROOT / "src/python/rule30_research_reference.py"
    if hashlib.sha256(reference.read_bytes()).hexdigest() != cone.REFERENCE_HASH:
        raise AssertionError("immutable reference hash mismatch")
    agreement = check_transition_agreement(cone)

    census = json.loads(CENSUS.read_text())
    rows = []
    cyclic_cases = 0
    for entry in census["portal_roots"]:
        cap()
        if entry["parity"] != "odd" or not entry["type"].startswith("singleton"):
            continue
        index = entry["portal"]
        w = A.P16_LEAVES[index]
        if w != entry["parent_leaf"]:
            raise AssertionError(("parent leaf mismatch", index))
        z = entry["canonical_target"]
        if len(w) != 16 or len(z) != 32 or entry["exact_period"] != 32:
            raise AssertionError(("certificate period", index))
        if A.parity(A.parse_lsb(w)) != 1 or A.parity(A.parse_lsb(z)) != 1:
            raise AssertionError(("parity", index))
        kw, hw, tw = profile(w, args.max_p16_depth)
        kz, hz, tz = profile(z, args.max_p32_depth)
        raw = entry["raw_target"]
        if len(raw) != len(z) or raw not in z + z:
            raise AssertionError(("target rotation", index))
        kr, hr, tr = profile(raw, args.max_p32_depth)
        if kr != kz or hr != hz or tr != tz:
            raise AssertionError(("phase-dependent profile", index, kr, kz))
        uw, topw = kappa(kw, hw, len(w))
        uz, topz = kappa(kz, hz, len(z))
        cyclic_cases = check_cyclic(w, hw, cyclic_cases, cone)
        cyclic_cases = check_cyclic(z, hz, cyclic_cases, cone)
        cyclic_cases = check_cyclic(raw, hr, cyclic_cases, cone)
        rows.append({
            "portal": index,
            "source_word": w,
            "target_word": z,
            "raw_target_word": raw,
            "raw_target_charge": uz,
            "source_period": len(w),
            "target_period": len(z),
            "k_source": kw,
            "k_target": kz,
            "height_source": hw,
            "height_target": hz,
            "height_source_truncated": tw,
            "height_target_truncated": tz,
            "imported_parent_portal_first_zero_depth": entry["first_zero_depth"],
            "first_blind_free_observer_source": next((i+1 for i,k in enumerate(kw) if k == 0), None),
            "first_blind_free_observer_target": next((i+1 for i,k in enumerate(kz) if k == 0), None),
            "charge_depth_source": topw,
            "charge_depth_target": topz,
            "kappa_source": uw,
            "kappa_target": uz,
            "violates_nonincrease": uz > uw,
        })

    rows.sort(key=lambda e: e["portal"])
    if [e["portal"] for e in rows] != sorted(census["singleton_portals"]):
        raise AssertionError("singleton domain differs from complete input census")
    violating = [e for e in rows if e["violates_nonincrease"]]
    first = violating[0] if violating else None
    payload = {
        "admission": ("counterexample-kills-naive-nonincrease" if first else
                      "bounded-test-insufficient"),
        "conjecture": ("kappa(z) <= kappa(w) whenever the first zero return z of w's "
                       "doubled portal is an odd singleton target."),
        "singletons_tested": len(rows),
        "violating_portals": [e["portal"] for e in violating],
        "smallest_violating_portal": first["portal"] if first else None,
        "smallest_violation": first,
        "rows": rows,
        "transition_agreement_cases": agreement,
        "cyclic_transition_cases": cyclic_cases,
    }
    record = {
        "experiment_id": "blind-charge-portal-transport-20261002",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": ("Naive monotone original-ancestry charge: kappa does not "
                       "increase across an odd singleton portal doubling."),
        "backend": ("64-bit broadword child transducer, packed step cross-checked "
                    "against independent two-row Rule 30"),
        "parameters": {
            "max_p16_depth": args.max_p16_depth,
            "max_p32_depth": args.max_p32_depth,
            "source_words": "P16_LEAVES[portal] of analyze_blind_visit_rank.py",
            "targets": "canonical_target of odd singleton portal_roots",
            "charge_rule": "kappa(w)=sum_{r=1..min(p-1,h)} max(k_r-1,0)",
            "max_seconds": args.max_seconds,
            "max_memory_mib": args.max_memory_mib,
            "max_output_kib": args.max_output_kib,
        },
        "hardware": {"machine": platform.machine(), "processor": platform.processor(),
                     "logical_cpu_count": os.cpu_count()},
        "software": {"python": sys.version, "platform": platform.platform()},
        "runtime_seconds": time.monotonic() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "source_hashes": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in SOURCES
        } | {"census": hashlib.sha256(CENSUS.read_bytes()).hexdigest()},
        "result_hashes": {
            "canonical_payload_sha256": hashlib.sha256(canonical_bytes(payload)).hexdigest()},
        "result_summary": payload,
        "status": "finite-exhaustive",
        "proof_scope": ("Only the eight odd singleton p32 roots listed above, at "
                        "depths 1..15 for sources and 1..31 for targets."),
        "interpretation": (
            "kappa strictly increases across an actual odd singleton portal in "
            "every tested case, so a naive monotone original-ancestry charge "
            "cannot be transported through a portal doubling." if first else
            "No violation in this exact bounded domain; this test is insufficient "
            "for the conjecture."),
        "limitations": [
            "Only eight certified odd singleton p32 roots were available; even and branching portals, and all p>=64 targets, are untested.",
            "The all-period cone theorem proves u_r=0 for r>=p, so the charges are exact despite not searching deeper layers; portal return heights are not bounded here.",
            "The old first-return endpoint certificates are imported and hashed, not freshly traversed at billion-lift depth.",
            "A strict increase refutes only the naive monotone transport heuristic, not the cyclic blind-cone lemma and not any corrected potential.",
            "No connector traversal, no new p32 graph expansion, no proof, no refit, no generalization.",
        ],
    }
    data = json.dumps(record, sort_keys=True, indent=2).encode() + b"\n"
    if len(data) > args.max_output_kib * 1024:
        raise RuntimeError("output cap reached; no final record written")
    cap()
    atomic_write(args.output, data)
    print(json.dumps({
        "output": str(args.output),
        "singletons": len(rows),
        "violating_portals": payload["violating_portals"],
        "smallest_violating_portal": payload["smallest_violating_portal"],
        "canonical_payload_sha256": record["result_hashes"]["canonical_payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
