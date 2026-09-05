#!/usr/bin/env python3
"""Three-return signed-mass census over the full both-phase/all-triple domain.

Conjecture under test (status ``inconclusive`` before this run): for every
phase ``a in {p, u}``, complexity ``k >= 2``, state ``x in O_(a,k)``, cut
``c >= 0`` and gap triple ``g in {2,3,4,5}^3`` such that the exact forced zero
schedule of ``x`` begins ``w E(g)`` with ``|w| = c`` and ``w E(g) u`` avoids
``uu``, ``ttttt`` and ``ututtu``, the dominant adjacent-shadow belief at depth
``L = c + 1 < k`` has NONZERO signed mass over DISTINCT concrete endpoints
(cost = number of nonfull shadow fibers over the ``L`` low base-four digits).

Here ``E(g) = u t^(g0-1) u t^(g1-1) u t^(g2-1)``; the final appended ``u`` is an
admissibility condition only, not an observed branch.

Outcome gate (fixed before execution):
  * a zero signed mass REFUTES this unified certificate (not nonemptiness,
    not the adjacent-shadow inclusion, not Problem 1);
  * no zero through the cap is FINITE support only for an all-depth counting
    route: the run stops, the cap is not increased.

Finite evidence is never an infinite proof.

Method notes:
  * candidates are visited in source order: complexity ascending, phase ``p``
    then ``u``, integer state ascending, cut ascending, lexicographic triple;
    the scan halts at the first signed zero;
  * every evaluated occurrence compares a DIRECT shadow enumeration against
    the existing seed-and-lift RECURSIVE weighted belief (cross-checked in the
    test file against the audited weighted-shadow module itself);
  * the frontier is checked against an independent BIT-BY-BIT Boolean oracle
    (per-bit ``x_j XOR (x_{j-1} OR x_{j-2})`` word construction, no packed
    shift formula) through small complexity;
  * at ``L >= k - 1`` the parent separation lemma applies (no adjacent shadow
    exists); the implementation returns the mathematically empty belief there
    and INDEPENDENTLY verifies it with a direct congruence scan, raising
    loudly on any violation. Occurrences with ``L >= k`` lie outside the
    proposed domain and are counted as EXCLUDED, never as successes;
  * only the schedule-cap limit exception is treated as a truncation; every
    other exception propagates (no blanket swallowing, no partial run
    presented as exhaustive).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
from typing import Any

PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
ALLOWED_MASKS = (0b0000, 0b0011, 0b1011, 0b1100, 0b1111)
RELEVANT_CURRENT_MASKS = (0b0011, 0b1011, 0b1100, 0b1111)
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 16
DEFAULT_SCHEDULE_CAP = 64
ABSOLUTE_SCHEDULE_CAP = 64
ORACLE_COMPLEXITY = 8
TIME_BUDGET_SECONDS = 120.0
MEMORY_BUDGET_KIB = 1024 * 1024
RESULT_FILENAME = "20260905_three_return_signed_mass.json"
BASE_COMMIT = "b54f067210d5d8eeb1af3247c858c97af456497c"
WEIGHTED_RELATIVE = (
    "experiments/problem1_nonperiodicity/"
    "analyze_period_two_weighted_shadow_recursion.py"
)
TEST_RELATIVE = (
    "tests/python/test_period_two_three_return_signed_mass.py"
)
# Analyzer path: <worktree>/experiments/problem1_nonperiodicity/<file>,
# so the worktree root is parents[2]. Verified, not assumed: the regression
# test checks payload git context against the live worktree.
ROOT = Path(__file__).resolve().parents[2]

HYPOTHESIS = (
    "For every phase a in {p,u}, complexity 2<=k<=16, state x in O_(a,k), "
    "cut c>=0 and gap triple g in {2,3,4,5}^3 such that the exact forced "
    "zero schedule of x begins w E(g) with |w|=c, where "
    "E(g)=u t^(g0-1) u t^(g1-1) u t^(g2-1), and w E(g) u avoids uu, ttttt "
    "and ututtu, the dominant adjacent-shadow belief at depth L=c+1<k has "
    "nonzero signed mass sum_{y} (-1)^d(y) over DISTINCT concrete endpoints "
    "y in O_(a,k-1) with y=x mod 4^L, with d(y) the number of non-1111 "
    "shadow fibers over the L low base-four digits. The final u is an "
    "admissibility condition, not an observed branch."
)


class SignedMassLimitError(RuntimeError):
    """Raised when a run would exceed its declared bounds (cap/time/range)."""


class SeparationViolationError(RuntimeError):
    """Raised if a direct congruence scan contradicts the separation lemma."""


class OracleMismatchError(RuntimeError):
    """Raised if the bit-by-bit oracle frontier disagrees with the primary."""


# --------------------------------------------------------------------------
# Generators and frontiers
# --------------------------------------------------------------------------

def forward_generator(name: str, state: int) -> int:
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError(name)


def frontier_children_primary(state: int) -> tuple[int, ...]:
    return tuple(sorted({forward_generator(name, state) for name in "tup"}))


def oracle_frontier_children(state: int) -> tuple[int, ...]:
    """Independent bit-by-bit Boolean oracle (no packed shift formula).

    Each output bit is built individually from the Boolean rule
    ``T_j = x_j XOR (x_{j-1} OR x_{j-2})`` with zero padding above the word;
    the ``u``/``p`` low-bit corrections are applied per bit. The word width
    ``bit_length + 2`` provably covers every output bit of the packed form.
    """
    if state <= 0:
        raise ValueError("oracle frontier states are positive")
    width = state.bit_length() + 2
    bits = [(state >> j) & 1 for j in range(width)]
    tout = 0
    for j in range(width):
        xj = bits[j]
        lo1 = bits[j - 1] if j >= 1 else 0
        lo2 = bits[j - 2] if j >= 2 else 0
        if xj ^ (lo1 | lo2):
            tout |= 1 << j
    # u flips bit 0; p flips bit 0 and (for even sources) bit 1.
    # Low bit is (T_0 XOR 1), matching the stated p correction exactly; the
    # previous form forced it to 1, which duplicates t rather than p on odd
    # inputs with T_0 = 1.
    uout = tout ^ 0b1
    pbit0 = ((tout & 1) ^ 1)
    pbit1 = ((tout >> 1) & 1) ^ (1 if (state & 1) == 0 else 0)
    pout = (tout & ~0b11) ^ pbit0 ^ (pbit1 << 1)
    return tuple(sorted({tout, uout, pout}))


def phase_start(phase: str) -> int:
    if phase == "p":
        return 3
    if phase == "u":
        return 1
    raise ValueError(phase)


def expected_bits(phase: str, complexity: int) -> int:
    return 2 * complexity if phase == "p" else 2 * complexity - 1


def build_levels(phase: str, maximum_complexity: int, childfn) -> list[set[int]]:
    levels: list[set[int]] = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append(
            {child for state in levels[-1] for child in childfn(state)}
        )
    return levels


# --------------------------------------------------------------------------
# Schedules and three-return patterns
# --------------------------------------------------------------------------

def forced_zero_schedule(state: int, cap: int = DEFAULT_SCHEDULE_CAP) -> str:
    word: list[str] = []
    for _ in range(cap):
        residue = state & 15
        if residue == 7:
            branch = "u"
        elif residue == 11:
            branch = "t"
        else:
            return "".join(word)
        state = forward_generator(
            branch, forward_generator("p", (state - 3) >> 2)
        )
        word.append(branch)
    raise SignedMassLimitError("forced schedule reached safety cap")


def admissible(word: str) -> bool:
    return not any(factor in word for factor in FORBIDDEN)


def return_extension(gaps: tuple[int, ...], include_final_u: bool) -> str:
    word = "u"
    for index, gap in enumerate(gaps):
        word += "t" * (gap - 1)
        if index < len(gaps) - 1 or include_final_u:
            word += "u"
    return word


def three_return_patterns() -> tuple[tuple[tuple[int, ...], str, str], ...]:
    """Admissible (gaps, E(g), E(g)+u) rows in lexicographic gap order."""
    rows = []
    for gaps in product(GAPS, repeat=3):
        target = return_extension(gaps, False)
        complete = return_extension(gaps, True)
        if admissible(complete):
            rows.append((gaps, target, complete))
    return tuple(rows)


# --------------------------------------------------------------------------
# Shadow fibers, beliefs, signed mass
# --------------------------------------------------------------------------

def fiber_mask(levels: list[set[int]], complexity: int, quotient: int) -> int:
    mask = sum(
        1 << digit
        for digit in range(4)
        if 4 * quotient + digit in levels[complexity + 1]
    )
    if mask not in ALLOWED_MASKS:
        raise AssertionError("fiber escaped the five-mask alphabet")
    return mask


def mask_sequence(
    levels: list[set[int]], complexity: int, state: int, depth: int
) -> tuple[int, ...]:
    masks: list[int] = []
    for step in range(depth):
        quotient = state >> 2
        masks.append(fiber_mask(levels, complexity - 1 - step, quotient))
        state = quotient
    return tuple(masks)


def dominates(
    current: tuple[int, ...], shadow: tuple[int, ...]
) -> bool:
    return len(current) == len(shadow) and all(
        not (current_mask & ~shadow_mask)
        for current_mask, shadow_mask in zip(current, shadow)
    )


def defect_count(shadow: tuple[int, ...]) -> int:
    return sum(mask != 0b1111 for mask in shadow)


def local_signed_factor(current_mask: int, shadow_mask: int) -> int:
    if current_mask & ~shadow_mask:
        return 0
    return 1 if shadow_mask == 0b1111 else -1


def local_branching_derivative(current_mask: int, shadow_mask: int) -> int:
    if current_mask & ~shadow_mask:
        return 0
    if current_mask == 0b1111:
        return int(shadow_mask == 0b1111)
    if current_mask in (0b0011, 0b1011):
        return 2 * ((shadow_mask >> 2) & 1) - 1
    if current_mask == 0b1100:
        return 2 * (shadow_mask & 1) - 1
    raise ValueError("branching derivative excludes current mask 0000")


def congruent_witnesses(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> list[int]:
    """Direct congruence scan: y in O_(a,k-1) with y = x mod 4^depth."""
    modulus = 4**depth
    residue = current % modulus
    return sorted(
        shadow for shadow in levels[complexity - 1] if shadow % modulus == residue
    )


def belief_direct(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> dict[int, int]:
    """Direct shadow enumeration: endpoint -> defect cost.

    At ``depth >= complexity - 1`` the parent separation lemma gives the
    mathematically empty belief; this path still runs the independent direct
    congruence scan and raises :class:`SeparationViolationError` if any
    witness exists, instead of touching the level-zero fiber alphabet where
    the five-mask theorem does not apply.
    """
    if depth >= complexity - 1:
        witnesses = congruent_witnesses(levels, complexity, current, depth)
        if witnesses:
            raise SeparationViolationError(
                f"separation lemma violated at k={complexity} "
                f"depth={depth}: {len(witnesses)} congruent witnesses"
            )
        return {}
    modulus = 4**depth
    residue = current % modulus
    current_masks = mask_sequence(levels, complexity, current, depth)
    result: dict[int, int] = {}
    for shadow in levels[complexity - 1]:
        if shadow % modulus != residue:
            continue
        shadow_masks = mask_sequence(levels, complexity - 1, shadow, depth)
        if dominates(current_masks, shadow_masks):
            result[shadow] = defect_count(shadow_masks)
    return result


def belief_recursive(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> dict[int, int]:
    """Existing seed-and-lift recursion: endpoint -> defect cost.

    Valid only for ``1 <= depth <= complexity - 2`` (all fiber levels stay
    at one or above). Callers must use the separation-lemma path at
    ``depth >= complexity - 1``.
    """
    if not 1 <= depth <= complexity - 2:
        raise SignedMassLimitError(
            "recursive belief requires 1 <= depth <= complexity - 2"
        )
    digit = current & 3
    quotient = current >> 2
    current_mask = fiber_mask(levels, complexity - 1, quotient)
    if depth == 1:
        result: dict[int, int] = {}
        for shadow in levels[complexity - 1]:
            if shadow & 3 != digit:
                continue
            shadow_mask = fiber_mask(levels, complexity - 2, shadow >> 2)
            if not (current_mask & ~shadow_mask):
                result[shadow] = int(shadow_mask != 0b1111)
        return result
    lower = belief_recursive(levels, complexity - 1, quotient, depth - 1)
    target_level = levels[complexity - 1]
    result = {}
    for shadow_quotient, lower_cost in lower.items():
        shadow = 4 * shadow_quotient + digit
        if shadow not in target_level:
            continue
        shadow_mask = fiber_mask(levels, complexity - 2, shadow_quotient)
        if current_mask & ~shadow_mask:
            continue
        result[shadow] = lower_cost + int(shadow_mask != 0b1111)
    return result


def signed_mass(costs: list[int]) -> int:
    return sum(-1 if cost & 1 else 1 for cost in costs)


# --------------------------------------------------------------------------
# Campaign
# --------------------------------------------------------------------------

def verify_oracle(
    levels: dict[str, list[set[int]]], maximum_complexity: int
) -> dict[str, Any]:
    """Compare the bit-by-bit oracle against the primary frontier.

    The bound adapts to small campaigns: min(requested cap, built levels).
    A mismatch raises immediately; scanning never continues past it.
    """
    bound = min(ORACLE_COMPLEXITY, maximum_complexity)
    checked = 0
    for phase in PHASES:
        oracle_levels = build_levels(phase, bound,
                                     oracle_frontier_children)
        for complexity in range(1, bound + 1):
            if oracle_levels[complexity] != levels[phase][complexity]:
                raise OracleMismatchError(
                    f"oracle disagrees at phase {phase} k={complexity}"
                )
            checked += len(levels[phase][complexity])
    return {
        "oracle_complexity": bound,
        "oracle_cap": ORACLE_COMPLEXITY,
        "states_compared": checked,
        "agreement": True,
    }


def verify_base_cases(levels: dict[str, list[set[int]]]) -> dict[str, str]:
    expected = {"p": ({3}, {12, 13}), "u": ({1}, {6, 7})}
    for phase in PHASES:
        want1, want2 = expected[phase]
        if levels[phase][1] != want1 or levels[phase][2] != want2:
            raise AssertionError(f"base case failed for phase {phase}")
    return {"p": "O1={3} O2={12,13}", "u": "O1={1} O2={6,7}"}


def verify_separation(
    levels: dict[str, list[set[int]]], maximum_complexity: int
) -> dict[str, Any]:
    """Finite-instance check of the separation lemma through the cap.

    For each phase and 2 <= k <= cap: no x in O_(a,k) shares its mod-4^(k-1)
    residue with any y in O_(a,k-1). Residue dictionaries keep this linear.
    """
    per_level: list[dict[str, Any]] = []
    pairs_checked = 0
    for phase in PHASES:
        for complexity in range(2, maximum_complexity + 1):
            modulus = 4 ** (complexity - 1)
            shadow_residues = {
                shadow % modulus for shadow in levels[phase][complexity - 1]
            }
            violations = sorted(
                current
                for current in levels[phase][complexity]
                if current % modulus in shadow_residues
            )
            if violations:
                raise SeparationViolationError(
                    f"phase {phase} k={complexity}: "
                    f"{len(violations)} separation violations"
                )
            pairs_checked += len(levels[phase][complexity])
            per_level.append(
                {
                    "phase": phase,
                    "complexity": complexity,
                    "states_checked": len(levels[phase][complexity]),
                    "shadow_residues": len(shadow_residues),
                    "violations": 0,
                }
            )
    return {"pairs_checked": pairs_checked, "violations": 0, "levels": per_level}


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
    schedule_cap: int = DEFAULT_SCHEDULE_CAP,
    enforcement: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not 2 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise SignedMassLimitError("maximum complexity outside 2..16")
    if not 1 <= schedule_cap <= ABSOLUTE_SCHEDULE_CAP:
        raise SignedMassLimitError("schedule cap outside 1..64")
    # Monotonic clock covering preparation as well as the scan.
    wall_start = time.monotonic()
    for current_mask in RELEVANT_CURRENT_MASKS:
        for shadow_mask in ALLOWED_MASKS:
            if local_signed_factor(current_mask, shadow_mask) != (
                local_branching_derivative(current_mask, shadow_mask)
            ):
                raise AssertionError("local branching derivative identity failed")

    levels = {
        phase: build_levels(phase, maximum_complexity, frontier_children_primary)
        for phase in PHASES
    }
    for phase in PHASES:
        for complexity in range(1, maximum_complexity + 1):
            for state in levels[phase][complexity]:
                if state.bit_length() != expected_bits(phase, complexity):
                    raise AssertionError("phase frontier bit-length law failed")

    oracle_report = verify_oracle(levels, maximum_complexity)
    base_cases = verify_base_cases(levels)
    separation_report = verify_separation(levels, maximum_complexity)
    patterns = three_return_patterns()
    if len(patterns) != 56:
        raise AssertionError("admissible three-return pattern count changed")

    totals = {
        "survivor_states_scanned": 0,
        "occurrences_evaluated": 0,
        "cylinders_evaluated": 0,
        "excluded_depth_ge_k": 0,
        "truncated_schedules": 0,
        "direct_recursive_disagreements": 0,
        "signed_zero_cylinders": 0,
        "dominant_failures": 0,
    }
    per_phase: dict[str, Any] = {
        phase: {"occurrences": 0, "cylinders": 0, "min_abs_mass": None}
        for phase in PHASES
    }
    occurrences: list[dict[str, Any]] = []
    disagreement_rows: list[dict[str, Any]] = []
    seen_cylinders: set[tuple[str, int, int]] = set()
    first_cancellation: dict[str, Any] | None = None
    completed = True
    halt_reason: str | None = None
    min_abs_mass: int | None = None
    min_mass_row: dict[str, Any] | None = None

    for complexity in range(2, maximum_complexity + 1):
        if time.monotonic() - wall_start > TIME_BUDGET_SECONDS:
            completed = False
            halt_reason = "time budget exceeded"
            break
        for phase in PHASES:
            level = levels[phase]
            for current in sorted(level[complexity]):
                if first_cancellation is not None:
                    break
                if current & 3 != 3:
                    continue
                totals["survivor_states_scanned"] += 1
                try:
                    schedule = forced_zero_schedule(current, schedule_cap)
                except SignedMassLimitError:
                    totals["truncated_schedules"] += 1
                    continue
                for cut in range(len(schedule) + 1):
                    if first_cancellation is not None:
                        break
                    base = schedule[:cut]
                    for gaps, target, complete in patterns:
                        if not schedule[cut:].startswith(target):
                            continue
                        if not admissible(base + complete):
                            continue
                        depth = cut + 1
                        if not depth < complexity:
                            totals["excluded_depth_ge_k"] += 1
                            continue
                        direct = belief_direct(
                            level, complexity, current, depth
                        )
                        if depth <= complexity - 2:
                            recursive = belief_recursive(
                                level, complexity, current, depth
                            )
                            recursive_checked = True
                            if direct != recursive:
                                totals["direct_recursive_disagreements"] += 1
                                only_direct = sorted(
                                    str(hex(y)) for y in direct if y not in recursive
                                )
                                only_recursive = sorted(
                                    str(hex(y)) for y in recursive if y not in direct
                                )
                                cost_mismatch = sorted(
                                    str(hex(y))
                                    for y in direct
                                    if y in recursive and direct[y] != recursive[y]
                                )
                                disagreement_rows.append(
                                    {
                                        "phase": phase,
                                        "complexity": complexity,
                                        "state_hex": hex(current),
                                        "cut": cut,
                                        "gaps": list(gaps),
                                        "depth": depth,
                                        "direct_endpoints": len(direct),
                                        "recursive_endpoints": len(recursive),
                                        "only_direct": only_direct,
                                        "only_recursive": only_recursive,
                                        "cost_mismatch": cost_mismatch,
                                    }
                                )
                                raise OracleMismatchError(
                                    f"direct/recursive disagreement at "
                                    f"{phase}, k={complexity}, x={hex(current)}, "
                                    f"cut={cut}, gaps={gaps}"
                                )
                        else:
                            # depth == complexity - 1: separation-lemma path;
                            # direct() already verified emptiness by an
                            # independent congruence scan.
                            recursive_checked = False
                        totals["occurrences_evaluated"] += 1
                        modulus = 4**depth
                        residue = current % modulus
                        same_cylinder = sum(
                            1
                            for shadow in level[complexity - 1]
                            if shadow % modulus == residue
                        )
                        if (phase, current, cut) not in seen_cylinders:
                            seen_cylinders.add((phase, current, cut))
                            totals["cylinders_evaluated"] += 1
                            per_phase[phase]["cylinders"] += 1
                        per_phase[phase]["occurrences"] += 1
                        histogram: dict[str, int] = {}
                        for cost in direct.values():
                            histogram[str(cost)] = histogram.get(str(cost), 0) + 1
                        mass = signed_mass(list(direct.values()))
                        if not direct:
                            totals["dominant_failures"] += 1
                        row = {
                            "phase": phase,
                            "complexity": complexity,
                            "state_hex": hex(current),
                            "cut": cut,
                            "base_prefix": base,
                            "gaps": list(gaps),
                            "target_E": target,
                            "depth": depth,
                            "same_cylinder": same_cylinder,
                            "dominant_shadows": len(direct),
                            "defect_histogram": histogram,
                            "signed_mass": mass,
                            "recursive_checked": recursive_checked,
                        }
                        occurrences.append(row)
                        if min_abs_mass is None or abs(mass) < min_abs_mass:
                            min_abs_mass = abs(mass)
                            min_mass_row = row
                        phase_min = per_phase[phase]["min_abs_mass"]
                        if phase_min is None or abs(mass) < phase_min:
                            per_phase[phase]["min_abs_mass"] = abs(mass)
                        if mass == 0:
                            totals["signed_zero_cylinders"] += 1
                            first_cancellation = {
                                **row,
                                "endpoints_hex": sorted(
                                    hex(y) for y in direct
                                ),
                            }
                            break
                    # end gaps
                # end cuts
            # end states
            if first_cancellation is not None:
                break
        # end phases
        if first_cancellation is not None:
            completed = False
            halt_reason = "first signed zero: scan halted in source order"
            break

    # Unrestricted non-gap control: phase-u k=5 x=0x198 depth 1 cancels.
    # Small campaigns may not build level 5; then a tiny separate control
    # frontier is built and its source recorded truthfully.
    if maximum_complexity >= 5:
        control_levels = levels["u"]
        control_source = "main campaign frontier"
    else:
        control_levels = build_levels("u", 5, frontier_children_primary)
        control_source = "separate control-only frontier (campaign below k=5)"
    control_belief = belief_direct(control_levels, 5, 0x198, 1)
    control_costs = sorted(control_belief.values())
    nongap_control = {
        "phase": "u",
        "complexity": 5,
        "state_hex": "0x198",
        "depth": 1,
        "defect_costs": control_costs,
        "signed_mass": signed_mass(control_costs),
        "frontier": control_source,
        "note": (
            "unrestricted cancellation; NOT an admissible three-return "
            "witness (see regression test)"
        ),
    }

    # Completion accounting: ANY incompleteness (truncation, deadline,
    # direct/recursive disagreement) forces completed_through_cap=false and
    # blocks the finite-exhaustive status. Only a verified zero mass yields
    # "refuted".
    incompleteness: list[str] = []
    if not completed:
        incompleteness.append(halt_reason or "scan halted early")
    if totals["truncated_schedules"]:
        incompleteness.append(
            f"{totals['truncated_schedules']} truncated schedule(s): "
            "those states are unresolved, not successes"
        )
    if totals["direct_recursive_disagreements"]:
        incompleteness.append(
            f"{totals['direct_recursive_disagreements']} direct/recursive "
            "disagreement(s): implementations diverge, run not exhaustive"
        )
    completed_through_cap = (
        first_cancellation is None and not incompleteness
    )
    if incompleteness and halt_reason is None:
        halt_reason = "; ".join(incompleteness)
    elif incompleteness and halt_reason:
        halt_reason = halt_reason + "; " + "; ".join(
            note for note in incompleteness if note != halt_reason
        )
    exhaustive = completed_through_cap and first_cancellation is None
    if first_cancellation is not None:
        status = "refuted"
    elif exhaustive:
        status = "finite-exhaustive"
    else:
        status = "inconclusive"

    result: dict[str, Any] = {
        "hypothesis": HYPOTHESIS,
        "domain": {
            "phases": list(PHASES),
            "complexity_range": [2, maximum_complexity],
            "gap_domain": list(GAPS),
            "admissible_patterns": len(patterns),
            "forbidden_factors": list(FORBIDDEN),
            "depth_rule": "L=c+1<k",
            "order": [
                "complexity ascending",
                "phase p then u",
                "integer state ascending",
                "cut ascending",
                "lexicographic gap triple",
            ],
            "stop_rule": "halt at first zero signed mass",
        },
        "oracle": oracle_report,
        "base_cases": base_cases,
        "separation": separation_report,
        "totals": totals,
        "per_phase": per_phase,
        "minimum_absolute_signed_mass": min_abs_mass,
        "minimum_mass_row": min_mass_row,
        "occurrences": occurrences,
        "disagreement_rows": disagreement_rows,
        "first_cancellation": first_cancellation,
        "completed_through_cap": completed_through_cap,
        "halt_reason": halt_reason,
        "nongap_control_0x198": nongap_control,
    }
    runtime_seconds = time.monotonic() - wall_start
    peak_rss_kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    occurrences_canonical = json.dumps(
        occurrences, sort_keys=True, separators=(",", ":")
    ).encode()
    git_status_text = git_strict(["status", "--short"])
    analyzer_digest = sha256_strict(Path(__file__).resolve())
    test_digest = sha256_strict(ROOT / TEST_RELATIVE)
    weighted_digest = sha256_strict(ROOT / WEIGHTED_RELATIVE)
    payload: dict[str, Any] = {
        "experiment_id": "period-two-three-return-signed-mass-full-domain",
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hypothesis": hypothesis_text(maximum_complexity, schedule_cap),
        "git_commit": git_strict_commit(),
        "base_commit": BASE_COMMIT,
        "git_branch": git_strict(["branch", "--show-current"]),
        "git_status": git_status_text,
        "git_dirty": bool(git_status_text.strip()),
        "worktree": str(ROOT),
        "source_hashes": {
            "analyzer_sha256": analyzer_digest,
            "test_sha256": test_digest,
            "weighted_shadow_recursion_sha256": weighted_digest,
        },
        "question": "problem1",
        "backend": "python-direct-and-recursive",
        "parameters": {
            "maximum_complexity": maximum_complexity,
            "schedule_cap": schedule_cap,
            "oracle_complexity": oracle_report["oracle_complexity"],
            "oracle_cap": ORACLE_COMPLEXITY,
            "time_budget_seconds": TIME_BUDGET_SECONDS,
            "memory_budget_kib": MEMORY_BUDGET_KIB,
        },
        "enforcement": enforcement_record(enforcement),
        "hardware": hardware_facts(),
        "software": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "os": platform.platform(),
        },
        "runtime_seconds": runtime_seconds,
        "peak_rss_kib": peak_rss_kib,
        "result": result,
        "result_hashes": {
            "certificate_sha256": hashlib.sha256(canonical).hexdigest(),
            "occurrences_sha256": hashlib.sha256(
                occurrences_canonical
            ).hexdigest(),
        },
        "result_summary": {
            "occurrences_evaluated": totals["occurrences_evaluated"],
            "cylinders_evaluated": totals["cylinders_evaluated"],
            "excluded_depth_ge_k": totals["excluded_depth_ge_k"],
            "truncated_schedules": totals["truncated_schedules"],
            "direct_recursive_disagreements": totals[
                "direct_recursive_disagreements"
            ],
            "signed_zero_cylinders": totals["signed_zero_cylinders"],
            "minimum_absolute_signed_mass": min_abs_mass,
            "completed_through_cap": completed_through_cap,
        },
        "interpretation": (
            "Zero signed mass on an evaluated occurrence refutes the unified "
            "signed-mass certificate (not nonemptiness, not the "
            "adjacent-shadow inclusion, not Problem 1). No zero through the "
            "cap is finite support only for examining an all-depth counting "
            "identity on the full domain; the cap is not increased."
        ),
        "status": status,
        "proof_scope": (
            "finite-exhaustive over the explicitly bounded candidate set "
            "(both phases, 2<=k<=16, all 56 admissible gap triples, "
            "depth L=c+1<k, source order with halt at first zero)"
            if exhaustive
            else "bounded scan, not exhaustive: see halt_reason and totals"
        ),
        "limitations": [
            "finite complexity cap k<=16; infinite conjecture stays "
            "inconclusive regardless of outcome",
            "single local CPU process; wall budget 120s and 1GiB address "
            "space per scientific run",
            "occurrences with L>=k are outside the proposed domain and are "
            "counted as excluded, not proved absent",
            "schedules reaching the forced-schedule cap are counted as "
            "truncated, not resolved",
            "empty-belief zeros at depth L=k-1 (if any occurred) would also "
            "threaten the adjacent-shadow inclusion itself, not only the "
            "signed strengthening",
        ],
    }
    return payload


def hypothesis_text(maximum_complexity: int, schedule_cap: int) -> str:
    """Top-level hypothesis stamped with the actual requested parameters."""
    scoped = HYPOTHESIS.replace(
        "complexity 2<=k<=16", f"complexity 2<=k<={maximum_complexity}"
    )
    return (
        f"{scoped} Actual run parameters: "
        f"maximum_complexity={maximum_complexity}, "
        f"schedule_cap={schedule_cap}."
    )


def enforcement_record(
    enforcement: dict[str, Any] | None,
) -> dict[str, Any]:
    """Truthful enforcement record; never claims a hard wall it lacks."""
    if enforcement is not None:
        return dict(enforcement)
    return {
        "address_space_limit_applied": False,
        "deadline": (
            "cooperative monotonic budget checks inside run_campaign "
            "(preparation and scan); no in-process hard preemption"
        ),
    }


def hardware_facts() -> dict[str, Any]:
    cpu_model = None
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("model name"):
                    cpu_model = line.split(":", 1)[1].strip()
                    break
    except OSError:
        cpu_model = None
    memory_total_kib = None
    try:
        with open("/proc/meminfo", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("MemTotal:"):
                    memory_total_kib = int(line.split()[1])
                    break
    except (OSError, ValueError):
        memory_total_kib = None
    return {
        "cpu_model": cpu_model,
        "cpu_count": os.cpu_count(),
        "memory_total_kib": memory_total_kib,
        "architecture": platform.machine(),
    }


def git_strict(args: list[str]) -> str:
    """Run git in the worktree; raise loudly instead of defaulting to None."""
    try:
        completed = subprocess.run(
            ["git", "-C", str(ROOT), *args],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise SignedMassLimitError(f"git unavailable: {exc}") from exc
    if completed.returncode != 0:
        raise SignedMassLimitError(
            f"git {' '.join(args)} failed: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def git_strict_commit() -> str:
    commit = git_strict(["rev-parse", "HEAD"])
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise SignedMassLimitError(f"invalid full commit: {commit!r}")
    return commit


def sha256_strict(path: Path) -> str:
    """Hash a required source file; a missing dependency fails the run."""
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError as exc:
        raise SignedMassLimitError(
            f"required source unavailable: {path}: {exc}"
        ) from exc


def write_record_atomic(payload: dict[str, Any], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True).encode()
    with tempfile.NamedTemporaryFile(
        dir=str(destination.parent), delete=False
    ) as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
        temporary = handle.name
    os.replace(temporary, destination)
    return destination


def apply_address_space_limit() -> dict[str, Any]:
    """Enforce the 1GiB address-space cap for CLI science runs.

    Never raises the inherited hard cap: the target is min(budget, hard).
    Failures are reported honestly in the returned record (no silent skip).
    """
    budget_bytes = MEMORY_BUDGET_KIB * 1024
    record: dict[str, Any] = {
        "budget_bytes": budget_bytes,
        "deadline": (
            "cooperative monotonic budget checks inside run_campaign "
            "(preparation and scan); outer `timeout 120s` wrapper provides "
            "the hard wall; no in-process signal preemption"
        ),
    }
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    except (OSError, ValueError) as exc:
        record["address_space_limit_applied"] = False
        record["reason"] = f"getrlimit failed: {exc}"
        return record
    target = budget_bytes
    if hard != resource.RLIM_INFINITY and hard < budget_bytes:
        target = hard
    if soft != resource.RLIM_INFINITY:
        target = min(target, soft)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (target, hard))
    except (OSError, ValueError) as exc:
        record["address_space_limit_applied"] = False
        record["reason"] = f"setrlimit failed: {exc}"
        record["previous_soft_bytes"] = soft
        record["previous_hard_bytes"] = hard
        return record
    record["address_space_limit_applied"] = True
    record["soft_bytes"] = target
    record["hard_bytes"] = hard if hard != resource.RLIM_INFINITY else "infinity"
    record["capped_by_inherited_hard"] = target != budget_bytes
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-complexity", type=int,
                        default=DEFAULT_MAXIMUM_COMPLEXITY)
    parser.add_argument("--schedule-cap", type=int, default=DEFAULT_SCHEDULE_CAP)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()
    enforcement = apply_address_space_limit()
    if not enforcement["address_space_limit_applied"]:
        raise SignedMassLimitError("could not enforce the address-space cap")
    payload = run_campaign(args.maximum_complexity, args.schedule_cap,
                           enforcement=enforcement)
    destination = (
        Path(args.output) if args.output else ROOT / "results/problem1"
        / RESULT_FILENAME
    )
    resolved = destination.resolve()
    if not resolved.is_relative_to(ROOT):
        raise SignedMassLimitError(
            f"output destination outside worktree: {resolved}"
        )
    write_record_atomic(payload, resolved)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()