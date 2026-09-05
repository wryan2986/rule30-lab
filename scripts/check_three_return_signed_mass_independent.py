#!/usr/bin/env python3
"""Independent falsification replay: signed mass on the full three-return domain.

Second-worker oracle, derived from the proof notes + the read-only reference
only. Never imports the first worker's module.

Conjecture under test (status: inconclusive):
  For a in {p,u}, k>=2, x in O_(a,k), cut c with L=c+1<k, gap triple
  g in {2,3,4,5}^3: if the forced zero schedule of x begins w E(g) with
  |w|=c and w E(g) u avoids uu/ttttt/ututtu, then P(-1) != 0, where P sums
  z^defects over DISTINCT concrete dominant adjacent-shadow endpoints sharing
  the low L base-four digits, defects counting nonfull shadow fibers at every
  common digit.

  E(g) = u t^(g0-1) u t^(g1-1) u t^(g2-1). The final appended u is an
  admissibility condition only; it is NOT required to be observed.

Outcome gate:
  Outcome A (P(-1)==0 on an admissible instance) refutes the proposed
    certificate (not nonempty belief, not Problem 1).
  Outcome B (no zero in the finite sweep) is FINITE evidence only.

Hard caps (validated fail-closed at API and CLI entry): 2<=max_k<=16,
0<wall_limit<=120s, schedule cap 64, 1GiB address space, one CPU.
Incomplete runs (wall limit, truncation, separation surprise) report
`inconclusive`, never `finite-exhaustive`.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from itertools import product
from pathlib import Path

PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
MIN_K = 2
ABSOLUTE_MAX_K = 16
DEFAULT_MAX_K = 16
SCHEDULE_CAP = 64
WALL_CAP = 120.0
DEFAULT_WALL_LIMIT = 120.0
ONE_GIB = 1024**3
FULL_MASK = frozenset((0, 1, 2, 3))


class ScheduleCapError(RuntimeError):
    pass


class WallLimit(Exception):
    """Internal: deadline exceeded; sweep must report inconclusive."""


def validate_caps(max_k: int, wall_limit: float) -> None:
    """Fail-closed cap validation. Raises ValueError outside the envelope."""
    if isinstance(max_k, bool) or not isinstance(max_k, int):
        raise ValueError("max_k must be an integer")
    if not MIN_K <= max_k <= ABSOLUTE_MAX_K:
        raise ValueError(f"max_k outside {MIN_K}..{ABSOLUTE_MAX_K}")
    if (
        isinstance(wall_limit, bool)
        or not isinstance(wall_limit, (int, float))
        or not 0 < wall_limit <= WALL_CAP
    ):
        raise ValueError(f"wall_limit outside (0, {WALL_CAP}]")


def check_deadline(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise WallLimit()


# --- Generators (proofs/informal/problem1_period_two_phase_frontier_lift_recursion.md) ---
def gen_t(x: int) -> int:
    return x ^ ((x << 1) | (x << 2))


def gen_u(x: int) -> int:
    return gen_t(x) ^ 1


def gen_p(x: int) -> int:
    return gen_t(x) ^ 1 ^ (0 if x & 1 else 2)


GENS = (gen_t, gen_u, gen_p)


def gen_t_bitwise(x: int) -> int:
    """Independent bit-by-bit Boolean oracle: T_j = x_j XOR (x_{j-1} OR x_{j-2}).

    Zero padding above the word; width bit_length+2 provably covers every
    output bit of the packed shift formula. Cross-checked against gen_t.
    """
    if x <= 0:
        raise ValueError("oracle states are positive")
    width = x.bit_length() + 2
    out = 0
    for j in range(width):
        xj = (x >> j) & 1
        lo1 = (x >> (j - 1)) & 1 if j >= 1 else 0
        lo2 = (x >> (j - 2)) & 1 if j >= 2 else 0
        if xj ^ (lo1 | lo2):
            out |= 1 << j
    return out


def phase_seed(phase: str) -> int:
    return 3 if phase == "p" else 1


def expected_bits(phase: str, complexity: int) -> int:
    return 2 * complexity if phase == "p" else 2 * complexity - 1


def build_frontiers(
    phase: str, max_k: int, deadline: float | None = None
) -> dict[int, set[int]]:
    """O_(a,k) as sets of DISTINCT ordinary integer outputs (dedup by value)."""
    frontiers: dict[int, set[int]] = {1: {phase_seed(phase)}}
    for k in range(1, max_k):
        if deadline is not None:
            check_deadline(deadline)
        nxt: set[int] = set()
        for s in frontiers[k]:
            for g in GENS:
                nxt.add(g(s))
        frontiers[k + 1] = nxt
    return frontiers


def build_multiplicities(
    phase: str, max_k: int, deadline: float | None = None
) -> dict[int, dict[int, int]]:
    """Representation counts: how many generator words yield each state.

    CONTROL ONLY for the dedup-sensitivity check (seam item 3). Counting
    generator words does not test the conjecture, which sums over DISTINCT
    concrete endpoints.
    """
    mults: dict[int, dict[int, int]] = {1: {phase_seed(phase): 1}}
    for k in range(1, max_k):
        if deadline is not None:
            check_deadline(deadline)
        nxt: dict[int, int] = {}
        for s, m in mults[k].items():
            for g in GENS:
                y = g(s)
                nxt[y] = nxt.get(y, 0) + m
        mults[k + 1] = nxt
    return mults


def forced_zero_schedule(state: int, cap: int = SCHEDULE_CAP) -> str:
    """Forced zero-branch schedule from the renewal/first-return notes.

    Branch u iff state == 7 mod 16, t iff state == 11 mod 16, else stop.
    Step: state <- Q(p((state-3)>>2)) with Q the emitted branch generator.
    Raises ScheduleCapError at the cap (counted as truncated, never success).
    """
    word: list[str] = []
    for _ in range(cap):
        residue = state & 15
        if residue == 7:
            branch = "u"
        elif residue == 11:
            branch = "t"
        else:
            return "".join(word)
        state = (gen_u if branch == "u" else gen_t)(gen_p((state - 3) >> 2))
        word.append(branch)
    raise ScheduleCapError("forced schedule reached the safety cap")


def admissible(word: str) -> bool:
    return not any(f in word for f in FORBIDDEN)


def return_extension(gaps: tuple[int, ...], include_final_u: bool) -> str:
    word = "u"
    for i, gap in enumerate(gaps):
        word += "t" * (gap - 1)
        if i < len(gaps) - 1 or include_final_u:
            word += "u"
    return word


def all_gap_triples() -> list[tuple[int, ...]]:
    return sorted(product(GAPS, repeat=3))


# --- Fibers (direct definition; mask as frozenset of digits) ---
def fiber(frontiers: dict[int, set[int]], level: int, quotient: int) -> frozenset[int]:
    """M_(a,level)(quotient) = {d : 4*quotient+d in O_(a,level+1)}.

    Level 0 (top-of-tower boundary, quotient must be 0) is PERMITTED per the
    recursive formulation: {d : d in O_(a,1)}. Recorded via `boundary_hits`.
    A mask-table routine that rejects level 0 would differ here; no swept
    instance reaches the boundary (boundary_hits stays empty).
    """
    if level == 0:
        assert quotient == 0, "level-0 quotient must be 0 by bit-length descent"
        return frozenset(d for d in range(4) if d in frontiers[1])
    return frozenset(d for d in range(4) if 4 * quotient + d in frontiers[level + 1])


def quotient_at(x: int, j: int) -> int:
    return x >> (2 * j)


def belief_direct(
    frontiers: dict[int, set[int]],
    k: int,
    x: int,
    depth: int,
    boundary_hits: list,
) -> dict[int, int]:
    """Endpoint -> defect count. Direct residue-grouping implementation."""
    assert 1 <= depth < k
    mod = 4**depth
    low = x & (mod - 1)
    out: dict[int, int] = {}
    for y in frontiers[k - 1]:
        if (y & (mod - 1)) != low:
            continue
        defects = 0
        ok = True
        for j in range(depth):
            cur = fiber(frontiers, k - 1 - j, quotient_at(x, j + 1))
            sh = fiber(frontiers, k - 2 - j, quotient_at(y, j + 1))
            if k - 2 - j == 0:
                boundary_hits.append((k, x, y, j))
            if not cur <= sh:
                ok = False
                break
            if sh != FULL_MASK:
                defects += 1
        if ok:
            out[y] = defects
    return out


def belief_recursive(
    frontiers: dict[int, set[int]],
    k: int,
    x: int,
    depth: int,
    boundary_hits: list,
) -> dict[int, int]:
    """Endpoint -> defect count via the literal W_(a,k,L) recursion.

    Base L=1 seed pairs; lift step with fiber test. Independent traversal of
    the same definition; cross-checked bit-for-bit against belief_direct on
    every swept instance.
    """
    assert 1 <= depth < k
    d = x & 3
    q = x >> 2
    if depth == 1:
        cur = fiber(frontiers, k - 1, q)
        out: dict[int, int] = {}
        for y in frontiers[k - 1]:
            if (y & 3) != d:
                continue
            sh = fiber(frontiers, k - 2, y >> 2)
            if k - 2 == 0:
                boundary_hits.append((k, x, y, 0))
            if cur <= sh:
                out[y] = 0 if sh == FULL_MASK else 1
        return out
    out = {}
    sub = belief_recursive(frontiers, k - 1, q, depth - 1, boundary_hits)
    cur = fiber(frontiers, k - 1, q)
    for p, c in sub.items():
        y = 4 * p + d
        if y not in frontiers[k - 1]:
            continue
        sh = fiber(frontiers, k - 2, p)
        if cur <= sh:
            out[y] = c + (0 if sh == FULL_MASK else 1)
    return out


def signed_mass(belief: dict[int, int]) -> int:
    return sum(-1 if c & 1 else 1 for c in belief.values())


def status_for(
    stop_reason: str, first_zero: dict | None, truncated: int
) -> str:
    """Fail-closed status mapping: incomplete runs are never finite-exhaustive."""
    if first_zero is not None:
        return "refuted"
    if stop_reason != "exhausted" or truncated > 0:
        return "inconclusive"
    return "finite-exhaustive"


def sweep(
    max_k: int = DEFAULT_MAX_K,
    wall_limit: float = DEFAULT_WALL_LIMIT,
    start_time: float | None = None,
) -> dict:
    validate_caps(max_k, wall_limit)
    t0 = start_time if start_time is not None else time.monotonic()
    deadline = t0 + wall_limit
    # All accumulators initialized before the guarded section so an early
    # deadline still returns a well-formed inconclusive record.
    stop_reason = "exhausted"
    frontiers: dict[str, dict[int, set[int]]] = {}
    mults: dict[str, dict[int, dict[int, int]]] | None = None
    separation_violations: list = []
    boundary_hits: list = []
    instances = 0
    checked = 0
    truncated = 0
    cross_mismatches = 0
    min_abs_mass: int | None = None
    min_mass_instance = None
    max_cut = 0
    first_zero = None
    last_position = None
    per_phase = {"p": 0, "u": 0}
    positive_cut = 0
    cylinders_seen: set = set()
    cylinders = 0
    occurrences: list = []
    outside_domain: list = []
    outside_count = 0
    final_u_rows: list = []
    final_u_excluded = 0
    dedup_diffs = 0
    weighted_zero_or_signflip = 0
    sign_flip_witness = None
    mass_values: list = []
    triples = all_gap_triples()
    ext = {
        g: (return_extension(g, False), return_extension(g, True)) for g in triples
    }
    self_adm = {g for g in triples if admissible(ext[g][1])}
    assert len(self_adm) == 56, len(self_adm)
    try:
        check_deadline(deadline)
        frontiers = {a: build_frontiers(a, max_k, deadline) for a in PHASES}
        # Sanity: levels disjoint, bit lengths exact, projection holds.
        for a in PHASES:
            seen: set[int] = set()
            for k in range(1, max_k + 1):
                check_deadline(deadline)
                assert not (frontiers[a][k] & seen), (a, k)
                seen |= frontiers[a][k]
                for s in frontiers[a][k]:
                    assert s.bit_length() == expected_bits(a, k), (a, k, s)
                    if k >= 2:
                        assert (s >> 2) in frontiers[a][k - 1], (a, k, s)
        # Finite separation check (parent lemma, attempted refutation target):
        # no x in O_(a,k) shares its mod-4^(k-1) residue with any y in O_(a,k-1).
        for a in PHASES:
            for k in range(2, max_k + 1):
                check_deadline(deadline)
                mod = 4 ** (k - 1)
                shadow_residues = {y % mod for y in frontiers[a][k - 1]}
                for x in frontiers[a][k]:
                    if x % mod in shadow_residues:
                        separation_violations.append((a, k, x))
        mults = {a: build_multiplicities(a, max_k, deadline) for a in PHASES}
        for k in range(2, max_k + 1):
            for a in PHASES:
                for x in sorted(frontiers[a][k]):
                    if x & 3 != 3:
                        continue
                    try:
                        sched = forced_zero_schedule(x)
                    except ScheduleCapError:
                        truncated += 1
                        continue
                    # ALL cuts: occurrences at every cut are found; only
                    # L=c+1<k is evaluated (signed domain). L>=k is counted
                    # as outside-domain, never a silent success.
                    for c in range(len(sched) + 1):
                        last_position = (a, k, x, c)
                        check_deadline(deadline)
                        L = c + 1
                        w = sched[:c]
                        for g in triples:
                            E, complete = ext[g]
                            B = len(E)
                            if len(sched) < c + B:
                                continue
                            if sched[c : c + B] != E:
                                continue
                            if not admissible(w + E):
                                continue
                            checked += 1
                            if L >= k:
                                outside_count += 1
                                outside_domain.append(
                                    {
                                        "phase": a,
                                        "complexity": k,
                                        "state": hex(x),
                                        "cut": c,
                                        "depth": L,
                                        "gaps": list(g),
                                        "reason": "L>=k outside signed domain",
                                    }
                                )
                                continue
                            b1 = belief_direct(frontiers[a], k, x, L, boundary_hits)
                            b2 = belief_recursive(
                                frontiers[a], k, x, L, boundary_hits
                            )
                            if b1 != b2:
                                cross_mismatches += 1
                                raise AssertionError(
                                    "oracle cross-check mismatch at "
                                    f"{(a, k, hex(x), c, g)}"
                                )
                            mass = signed_mass(b1)
                            # CONTROL ONLY: representation-weighted mass.
                            wmass = None
                            if mults is not None:
                                wmass = sum(
                                    mults[a][k - 1][y] * (-1 if d & 1 else 1)
                                    for y, d in b1.items()
                                )
                                if wmass != mass:
                                    dedup_diffs += 1
                                    if wmass == 0 or (wmass < 0) != (mass < 0):
                                        weighted_zero_or_signflip += 1
                                        if sign_flip_witness is None:
                                            sign_flip_witness = {
                                                "phase": a,
                                                "complexity": k,
                                                "state": hex(x),
                                                "cut": c,
                                                "depth": L,
                                                "gaps": list(g),
                                                "mass": mass,
                                                "weighted_mass": wmass,
                                            }
                            mod = 4**L
                            residue = x & (mod - 1)
                            same_cyl = sum(
                                1
                                for y in frontiers[a][k - 1]
                                if (y & (mod - 1)) == residue
                            )
                            if not admissible(w + complete):
                                # CONTROL ONLY: final-u admissibility required
                                # by the stated convention; these instances are
                                # not conjecture tests.
                                final_u_excluded += 1
                                final_u_rows.append(
                                    {
                                        "phase": a,
                                        "complexity": k,
                                        "state": hex(x),
                                        "cut": c,
                                        "depth": L,
                                        "gaps": list(g),
                                        "mass": mass,
                                        "weighted_mass": wmass,
                                        "note": (
                                            "control: wE admissible, "
                                            "wEu forbidden"
                                        ),
                                    }
                                )
                                continue
                            instances += 1
                            per_phase[a] += 1
                            if c > 0:
                                positive_cut += 1
                            max_cut = max(max_cut, c)
                            if (a, x, c) not in cylinders_seen:
                                cylinders_seen.add((a, x, c))
                                cylinders += 1
                            mass_values.append(mass)
                            row = {
                                "phase": a,
                                "complexity": k,
                                "state": hex(x),
                                "state_int": x,
                                "cut": c,
                                "depth": L,
                                "gaps": list(g),
                                "schedule_prefix": sched[: c + B + 2],
                                "mass": mass,
                                "belief_size": len(b1),
                                "weighted_mass": wmass,
                                "same_cylinder": same_cyl,
                            }
                            occurrences.append(row)
                            if min_abs_mass is None or abs(mass) < abs(min_abs_mass):
                                min_abs_mass = abs(mass)
                                min_mass_instance = dict(row)
                            if mass == 0:
                                first_zero = {
                                    **row,
                                    "belief": {
                                        hex(y): d for y, d in sorted(b1.items())
                                    },
                                }
                                stop_reason = "first-zero"
                                break
                        if stop_reason == "first-zero":
                            break
                    if stop_reason == "first-zero":
                        break
                if stop_reason == "first-zero":
                    break
            if stop_reason == "first-zero":
                break
    except WallLimit:
        stop_reason = "wall-limit"

    if separation_violations:
        stop_reason = "separation-violation"

    return {
        "instances": instances,
        "cylinders": cylinders,
        "per_phase": per_phase,
        "positive_cut": positive_cut,
        "checked_prefix_admissible": checked,
        "final_u_excluded": final_u_excluded,
        "final_u_rows": final_u_rows,
        "outside_domain_count": outside_count,
        "outside_domain_rows": outside_domain,
        "truncated_schedules": truncated,
        "dedup_diffs": dedup_diffs,
        "weighted_zero_or_signflip": weighted_zero_or_signflip,
        "sign_flip_witness": sign_flip_witness,
        "mass_values_sorted": sorted(mass_values),
        "occurrences": occurrences,
        "self_admissible_triples": len(self_adm),
        "cross_mismatches": cross_mismatches,
        "min_abs_mass": min_abs_mass,
        "min_mass_instance": min_mass_instance,
        "max_cut": max_cut,
        "first_zero": first_zero,
        "boundary_hits": len(boundary_hits),
        "separation_violations": separation_violations,
        "stop_reason": stop_reason,
        "status": status_for(stop_reason, first_zero, truncated),
        "last_position": last_position,
        "frontier_sizes": {
            a: {str(k): len(levels[k]) for k in sorted(levels)}
            for a, levels in frontiers.items()
        },
    }


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cpu_model() -> str | None:
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return None


def fail(msg: str) -> int:
    print(f"error: {msg}", file=sys.stderr)
    return 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-k", type=int, default=DEFAULT_MAX_K)
    ap.add_argument("--wall-limit", type=float, default=DEFAULT_WALL_LIMIT)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--tests-passed", type=int, default=-1)
    ap.add_argument("--tests-total", type=int, default=-1)
    args = ap.parse_args()

    try:
        validate_caps(args.max_k, args.wall_limit)
    except ValueError as e:
        return fail(f"cap validation: {e}")

    here = Path(__file__).resolve()
    repo = here.parents[1]
    ref = repo / "src" / "python" / "rule30_research_reference.py"
    test_file = (
        repo / "tests" / "python" / "test_three_return_signed_mass_independent.py"
    )
    runner_file = (
        repo / "tests" / "python" / "run_independent_signed_mass_tests.py"
    )

    if args.out:
        dest = Path(args.out).resolve()
        try:
            dest.relative_to(repo.resolve())
        except ValueError:
            return fail(f"output path confined to repository: {args.out}")

    # Fail-closed resource enforcement: do not run unbounded.
    try:
        resource.setrlimit(resource.RLIMIT_AS, (ONE_GIB, ONE_GIB))
        rlimit = "RLIMIT_AS=1GiB"
    except Exception as e:
        return fail(f"address-space limit enforcement failed: {e}; refusing to run")

    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(repo), text=True, timeout=30
        ).strip()
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=str(repo), text=True, timeout=30
        ).strip()
        dirty = subprocess.check_output(
            ["git", "status", "--short"], cwd=str(repo), text=True, timeout=30
        ).strip()
    except Exception as e:
        return fail(f"git provenance unavailable: {e}; refusing to run")
    if not commit:
        return fail("full git commit unavailable; refusing to run")

    t0 = time.monotonic()
    res = sweep(max_k=args.max_k, wall_limit=args.wall_limit, start_time=t0)
    elapsed = time.monotonic() - t0
    try:
        peak_rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:
        peak_rss_kb = -1

    record = {
        "experiment_id": "three-return-signed-mass-independent-k16",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "git_commit": commit,
        "git_branch": branch,
        "git_dirty_paths": dirty,
        "question": "problem1",
        "hypothesis": (
            "For a in {p,u}, k>=2, x in O_(a,k), cut c with L=c+1<k, "
            "g in {2,3,4,5}^3: schedule(x) begins w E(g) (|w|=c) and "
            "w E(g) u avoids uu/ttttt/ututtu => P(-1) != 0 over distinct "
            "concrete dominant adjacent-shadow endpoints."
        ),
        "backend": "python-independent-oracle",
        "parameters": {
            "max_k": args.max_k,
            "schedule_cap": SCHEDULE_CAP,
            "wall_limit_s": args.wall_limit,
            "memory_limit": "1GiB address space",
            "cpus": 1,
            "order": "k asc, phase p-then-u, x asc, cut asc, g lexicographic",
            "stop": "first-zero",
            "final_u_convention": "admissibility-required-observation-not-required",
            "dedup": "distinct-concrete-endpoints",
        },
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "script": os.path.basename(__file__),
        },
        "hardware": {
            "uname": " ".join(platform.uname()),
            "cpu_model": cpu_model(),
            "cpu_count": os.cpu_count(),
            "rlimit": rlimit,
            "peak_rss_kb_after": peak_rss_kb,
        },
        "runtime_seconds": elapsed,
        "verification": {
            "tests_passed": args.tests_passed,
            "tests_total": args.tests_total,
            "runner": (
                "tests/python/run_independent_signed_mass_tests.py "
                "(direct, no pytest)"
            ),
        },
        "result_summary": res,
        "status": res["status"],
        "proof_scope": (
            "Finite sweep only: k<=16, both phases, exact stated order. "
            "Not an infinite proof."
        ),
        "interpretation": (
            "Zero signed mass on an evaluated admissible occurrence refutes "
            "the unified signed-mass certificate (not nonempty belief, not "
            "the adjacent-shadow inclusion, not Problem 1). No zero through "
            "the cap is finite support only for examining an all-depth "
            "counting identity on the full domain; the cap is not increased. "
            "Dedup/final-u counterfactual numbers are controls only and do "
            "not test the conjecture."
        ),
        "limitations": [
            "k<=16 only",
            "schedule cap 64; capped schedules counted as truncated, never success",
            "occurrences with L>=k outside the signed domain: counted, not evaluated",
            "single CPU, 120s wall, 1GiB address space; incomplete runs report inconclusive",
            "level-0 top fiber permitted per recursive formulation; hits counted (0 in box)",
        ],
    }
    record["source_hashes"] = {
        "script_sha256": sha256_file(str(here)),
        "test_sha256": sha256_file(str(test_file)) if test_file.exists() else None,
        "runner_sha256": (
            sha256_file(str(runner_file)) if runner_file.exists() else None
        ),
        "reference_sha256": sha256_file(str(ref)),
    }
    record["result_hashes"] = {
        "summary_sha256": hashlib.sha256(
            json.dumps(res, sort_keys=True).encode()
        ).hexdigest()
    }
    print(json.dumps(res, indent=2))
    print(f"elapsed={elapsed:.2f}s status={record['status']}", file=sys.stderr)
    if args.out:
        dest = Path(args.out).resolve()
        dest.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(
            dir=str(dest.parent), prefix=dest.name + ".", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(record, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, dest)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
