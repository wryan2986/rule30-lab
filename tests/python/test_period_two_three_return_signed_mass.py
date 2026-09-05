"""Tests for the full-domain three-return signed-mass census.

Covers: hand-derived generator base cases, the independent bit-by-bit
Boolean oracle, pattern/final-u conventions, the local derivative identity,
direct-vs-recursive agreement (including a cross-check against the audited
existing weighted-shadow module), the separation-lemma boundary, cap guards,
the known unrestricted 0x198 cancellation (marked NOT an admissible
three-return witness), source ordering, certificate hashes, and the verified
full-campaign totals.
"""
from __future__ import annotations

import functools
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_three_return_signed_mass.py"
)
SPEC = importlib.util.spec_from_file_location("three_return_signed_mass",
                                              MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

WEIGHTED_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_weighted_shadow_recursion.py"
)
WEIGHTED_SPEC = importlib.util.spec_from_file_location(
    "weighted_shadow_recursion_existing", WEIGHTED_PATH
)
assert WEIGHTED_SPEC and WEIGHTED_SPEC.loader
weighted = importlib.util.module_from_spec(WEIGHTED_SPEC)
WEIGHTED_SPEC.loader.exec_module(weighted)

BASE_COMMIT = "b54f067210d5d8eeb1af3247c858c97af456497c"


def live_head() -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True, text=True, timeout=30,
    )
    assert completed.returncode == 0
    head = completed.stdout.strip()
    assert len(head) == 40
    return head


@functools.lru_cache(maxsize=1)
def campaign() -> dict:
    return module.run_campaign()


def test_belief_disagreement_fails_closed() -> None:
    original = module.belief_recursive
    try:
        setattr(module, "belief_recursive", lambda *args: {})
        try:
            module.run_campaign(maximum_complexity=12)
        except module.OracleMismatchError:
            pass
        else:
            raise AssertionError("belief mismatch must stop the campaign")
    finally:
        setattr(module, "belief_recursive", original)


def test_hand_derived_generator_children() -> None:
    # t(3) = 3^(6|12) = 13; u(3) = 12; p(3) = 12 (odd source).
    assert module.frontier_children_primary(3) == (12, 13)
    # t(1) = 1^(2|4) = 7; u(1) = 6; p(1) = 6 (odd source).
    assert module.frontier_children_primary(1) == (6, 7)
    assert module.oracle_frontier_children(3) == (12, 13)
    assert module.oracle_frontier_children(1) == (6, 7)


def test_base_cases_both_builders() -> None:
    for builder in (module.frontier_children_primary,
                    module.oracle_frontier_children):
        assert module.build_levels("p", 2, builder)[1] == {3}
        assert module.build_levels("p", 2, builder)[2] == {12, 13}
        assert module.build_levels("u", 2, builder)[1] == {1}
        assert module.build_levels("u", 2, builder)[2] == {6, 7}


def test_bitwise_oracle_agrees_with_primary() -> None:
    for phase in module.PHASES:
        primary = module.build_levels(phase, module.ORACLE_COMPLEXITY,
                                      module.frontier_children_primary)
        oracle = module.build_levels(phase, module.ORACLE_COMPLEXITY,
                                     module.oracle_frontier_children)
        for complexity in range(1, module.ORACLE_COMPLEXITY + 1):
            assert primary[complexity] == oracle[complexity]


def test_oracle_children_per_input_odd_and_even() -> None:
    # Per-input agreement (not just level sets), covering odd and even
    # sources: the p-oracle low bit must be T_0 XOR 1, so on odd inputs the
    # oracle p duplicates u exactly as the primary does.
    checked_odd = checked_even = 0
    for state in range(1, 500):
        primary = module.frontier_children_primary(state)
        oracle = module.oracle_frontier_children(state)
        assert oracle == primary, f"oracle child mismatch at {state}"
        if state & 1:
            checked_odd += 1
        else:
            checked_even += 1
    assert checked_odd > 0 and checked_even > 0
    # Odd input with T_0 = 1: oracle p must equal oracle u (not t).
    tout_set = {
        state for state in range(1, 500, 2)
        if (module.forward_generator("t", state) & 1) == 1
    }
    assert tout_set, "no odd input with T_0=1 in range"
    for state in sorted(tout_set)[:25]:
        children = module.oracle_frontier_children(state)
        u = module.forward_generator("t", state) ^ 1
        assert u in children
        assert children == module.frontier_children_primary(state)


def test_three_return_pattern_conventions() -> None:
    patterns = module.three_return_patterns()
    assert len(patterns) == 56
    gaps = [row[0] for row in patterns]
    assert gaps == sorted(gaps)
    by_gaps = {row[0]: (row[1], row[2]) for row in patterns}
    assert by_gaps[(2, 2, 2)] == ("ututut", "utututu")
    for _, target, complete in patterns:
        assert complete == target + "u"
        assert module.admissible(complete)


def test_final_u_is_admissibility_only() -> None:
    target, complete = "ututut", "utututu"
    # Bare complete word is admissible.
    assert module.admissible("" + complete)
    # A base ending in "u" makes base+complete inadmissible: rejected even
    # though the schedule remainder matches E(g) exactly.
    assert not module.admissible("u" + complete)
    # Exact-prefix matching: a shorter remainder is not a match.
    assert not "ututu"[0:].startswith(target)
    assert "ututut"[0:].startswith(target)


def test_local_branching_derivative_identity() -> None:
    for current in module.RELEVANT_CURRENT_MASKS:
        for shadow in module.ALLOWED_MASKS:
            assert module.local_signed_factor(current, shadow) == (
                module.local_branching_derivative(current, shadow)
            )


def test_direct_and_recursive_agree_small() -> None:
    for phase in module.PHASES:
        levels = module.build_levels(phase, 9,
                                     module.frontier_children_primary)
        for complexity in range(2, 10):
            for current in levels[complexity]:
                for depth in range(1, complexity - 1):
                    assert module.belief_direct(
                        levels, complexity, current, depth
                    ) == module.belief_recursive(
                        levels, complexity, current, depth
                    )


def test_recursive_guard_rejects_boundary_depth() -> None:
    levels = module.build_levels("p", 6, module.frontier_children_primary)
    current = next(state for state in sorted(levels[6]) if state & 3 == 3)
    try:
        module.belief_recursive(levels, 6, current, 5)
    except module.SignedMassLimitError:
        pass
    else:
        raise AssertionError("recursive guard did not fire at depth k-1")


def test_separation_path_is_empty_and_verified() -> None:
    for phase in module.PHASES:
        levels = module.build_levels(phase, 10,
                                     module.frontier_children_primary)
        for complexity in range(2, 11):
            for current in levels[complexity]:
                depth = complexity - 1
                assert module.belief_direct(
                    levels, complexity, current, depth
                ) == {}
                assert module.congruent_witnesses(
                    levels, complexity, current, depth
                ) == []


def test_separation_verification_pass() -> None:
    levels = {
        phase: module.build_levels(phase, 10,
                                   module.frontier_children_primary)
        for phase in module.PHASES
    }
    report = module.verify_separation(levels, 10)
    assert report["violations"] == 0
    assert report["pairs_checked"] == sum(
        len(levels[phase][k])
        for phase in module.PHASES for k in range(2, 11)
    )


def test_agreement_with_existing_weighted_module() -> None:
    for phase in module.PHASES:
        mine = module.build_levels(phase, 7,
                                   module.frontier_children_primary)
        theirs = weighted.build_levels(phase, 7)
        assert mine == theirs
        for complexity in range(2, 8):
            for current in mine[complexity]:
                for depth in range(1, complexity - 1):
                    assert module.belief_recursive(
                        mine, complexity, current, depth
                    ) == weighted.weighted_shadow_belief_recursive(
                        theirs, complexity, current, depth
                    )


def test_known_unrestricted_cancellation_is_not_a_witness() -> None:
    levels = module.build_levels("u", 5, module.frontier_children_primary)
    belief = module.belief_direct(levels, 5, 0x198, 1)
    assert sorted(belief.values()) == [0, 1]
    assert module.signed_mass(list(belief.values())) == 0
    # No admissible three-return occurrence at (u,5,0x198) carries zero mass:
    # every eligible occurrence of that state has nonzero signed mass.
    full = module.build_levels("u", 16, module.frontier_children_primary)
    schedule = module.forced_zero_schedule(0x198)
    patterns = module.three_return_patterns()
    checked = 0
    for cut in range(len(schedule) + 1):
        base = schedule[:cut]
        for gaps, target, complete in patterns:
            if not schedule[cut:].startswith(target):
                continue
            if not module.admissible(base + complete):
                continue
            depth = cut + 1
            if not depth < 5:
                continue
            checked += 1
            mass = module.signed_mass(
                list(module.belief_direct(full, 5, 0x198, depth).values())
            )
            assert mass != 0
    control = campaign()["result"]["nongap_control_0x198"]
    assert control["signed_mass"] == 0
    assert control["defect_costs"] == [0, 1]


def test_schedule_cap_and_parameter_guards() -> None:
    assert module.forced_zero_schedule(3) == ""
    assert module.forced_zero_schedule(7).startswith("u")
    try:
        module.forced_zero_schedule(7, cap=1)
    except module.SignedMassLimitError:
        pass
    else:
        raise AssertionError("schedule cap did not fire")
    for kwargs in ({"maximum_complexity": 17},
                   {"maximum_complexity": 1},
                   {"schedule_cap": 65}):
        try:
            module.run_campaign(**kwargs)
        except module.SignedMassLimitError:
            pass
        else:
            raise AssertionError(f"parameter guard did not fire for {kwargs}")


def test_truncated_run_is_inconclusive_not_exhaustive() -> None:
    payload = module.run_campaign(8, 1)
    summary = payload["result_summary"]
    assert summary["truncated_schedules"] > 0
    assert summary["completed_through_cap"] is False
    assert payload["status"] == "inconclusive"
    assert payload["result"]["halt_reason"] is not None
    assert "truncated" in payload["result"]["halt_reason"]


def test_small_campaign_adapts_oracle_and_control() -> None:
    payload = module.run_campaign(4)
    assert payload["result"]["oracle"]["oracle_complexity"] == 4
    assert payload["result"]["oracle"]["agreement"] is True
    assert payload["parameters"]["oracle_complexity"] == 4
    control = payload["result"]["nongap_control_0x198"]
    assert control["signed_mass"] == 0
    assert control["defect_costs"] == [0, 1]
    assert "separate control-only" in control["frontier"]
    assert payload["result"]["completed_through_cap"] is True
    assert payload["status"] == "finite-exhaustive"


def test_occurrence_rows_in_source_order_and_nonzero() -> None:
    rows = campaign()["result"]["occurrences"]
    assert rows, "campaign found no occurrences"
    phase_rank = {"p": 0, "u": 1}
    keys = [
        (row["complexity"], phase_rank[row["phase"]],
         int(row["state_hex"], 16), row["cut"], tuple(row["gaps"]))
        for row in rows
    ]
    assert keys == sorted(keys)
    for row in rows:
        assert row["signed_mass"] != 0
        assert row["dominant_shadows"] > 0
        assert row["depth"] == row["cut"] + 1
        assert row["depth"] < row["complexity"]


def test_full_campaign_totals() -> None:
    payload = campaign()
    assert payload["status"] == "finite-exhaustive"
    summary = payload["result_summary"]
    assert summary["occurrences_evaluated"] == 19
    assert summary["cylinders_evaluated"] == 17
    assert summary["excluded_depth_ge_k"] == 0
    assert summary["truncated_schedules"] == 0
    assert summary["direct_recursive_disagreements"] == 0
    assert summary["signed_zero_cylinders"] == 0
    assert summary["minimum_absolute_signed_mass"] == 6
    assert summary["completed_through_cap"] is True
    assert payload["result"]["first_cancellation"] is None
    assert payload["result"]["per_phase"]["p"]["occurrences"] == 8
    assert payload["result"]["per_phase"]["u"]["occurrences"] == 11
    assert payload["result"]["oracle"]["agreement"] is True
    assert payload["result"]["separation"]["violations"] == 0
    minimum = payload["result"]["minimum_mass_row"]
    assert minimum["signed_mass"] == 6
    assert minimum["phase"] == "u"
    assert minimum["complexity"] == 15
    assert minimum["state_hex"] == "0x1bd9c36b"
    assert minimum["cut"] == 2
    assert minimum["gaps"] == [2, 2, 2]


def test_certificate_hashes_and_provenance() -> None:
    payload = campaign()
    result = payload["result"]
    canonical = json.dumps(result, sort_keys=True,
                           separators=(",", ":")).encode()
    assert payload["result_hashes"]["certificate_sha256"] == (
        hashlib.sha256(canonical).hexdigest()
    )
    occurrences_canonical = json.dumps(
        result["occurrences"], sort_keys=True, separators=(",", ":")
    ).encode()
    assert payload["result_hashes"]["occurrences_sha256"] == (
        hashlib.sha256(occurrences_canonical).hexdigest()
    )
    # Live HEAD comparison: the parent commits source first, then regenerates
    # results, so the payload commit must equal the actual current HEAD.
    assert payload["git_commit"] == live_head()
    assert payload["base_commit"] == BASE_COMMIT
    assert payload["worktree"] == str(ROOT)
    assert payload["git_branch"] == "research/signed-full-domain-pass"
    if payload["git_dirty"]:
        assert "three_return_signed_mass" in payload["git_status"]
    assert payload["git_dirty"] == bool(payload["git_status"].strip())
    for key in ("analyzer_sha256", "test_sha256",
                "weighted_shadow_recursion_sha256"):
        digest = payload["source_hashes"][key]
        assert digest is not None and len(digest) == 64
    analyzer_digest = hashlib.sha256(MODULE_PATH.read_bytes()).hexdigest()
    assert payload["source_hashes"]["analyzer_sha256"] == analyzer_digest
    test_path = (
        Path(__file__).resolve().parent / "test_period_two_three_return_signed_mass.py"
    )
    assert payload["source_hashes"]["test_sha256"] == (
        hashlib.sha256(test_path.read_bytes()).hexdigest()
    )
    assert payload["source_hashes"]["weighted_shadow_recursion_sha256"] == (
        hashlib.sha256(WEIGHTED_PATH.read_bytes()).hexdigest()
    )
    assert "maximum_complexity=16" in payload["hypothesis"]
    assert "schedule_cap=64" in payload["hypothesis"]
    assert payload["parameters"]["maximum_complexity"] == 16
    assert payload["parameters"]["schedule_cap"] == 64
    assert payload["parameters"]["oracle_complexity"] == 8
    assert payload["runtime_seconds"] < 120
    assert "enforcement" in payload
