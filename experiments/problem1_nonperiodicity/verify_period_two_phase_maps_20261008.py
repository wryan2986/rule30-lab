#!/usr/bin/env python3
"""Independent finite controls for Rule 30's two-step half-row maps.

The checker uses a sparse cell dictionary and literal Rule 30 updates; it does
not import the producer's A, D, Psi, F, or inverse routines.  The bounded
control outcomes can catch an error in the proposed reduction before it is
used in whole-tail reasoning.  They cannot prove the infinite-orbit
termination claim.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import resource
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).resolve()
OUT = ROOT / "results/problem1/20261008_period_two_phase_maps_independent.json"
START = time.monotonic()
WALL_CAP_SECONDS = 60
MEMORY_CAP_BYTES = 256 * 1024 * 1024


def enforce_caps() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_CAP_BYTES, MEMORY_CAP_BYTES))
    resource.setrlimit(resource.RLIMIT_CPU, (WALL_CAP_SECONDS, WALL_CAP_SECONDS + 1))
    signal.alarm(WALL_CAP_SECONDS)


def bit(z: int, j: int) -> int:
    return (z >> j) & 1


def raw_rule30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def raw_step(cells: dict[int, int]) -> dict[int, int]:
    if not cells:
        return {}
    lo, hi = min(cells), max(cells)
    out: dict[int, int] = {}
    for i in range(lo - 1, hi + 2):
        value = raw_rule30(cells.get(i - 1, 0), cells.get(i, 0), cells.get(i + 1, 0))
        if value:
            out[i] = value
    return out


def raw_halves(L: int, R: int) -> dict[int, int]:
    cells: dict[int, int] = {}
    for j in range(L.bit_length()):
        if bit(L, j):
            cells[-j] = 1
    for j in range(R.bit_length()):
        if bit(R, j):
            cells[j + 1] = 1
    return cells


def halves(cells: dict[int, int]) -> tuple[int, int]:
    L = R = 0
    for i, value in cells.items():
        if value:
            if i <= 0:
                L |= 1 << (-i)
            else:
                R |= 1 << (i - 1)
    return L, R


def A(z: int) -> int:
    return (z >> 2) ^ ((z >> 1) | z)


def A2(z: int) -> int:
    return A(A(z))


def psi(L: int) -> int:
    return 4 * A2(L) + 3


def D(R: int) -> int:
    return (R << 1) ^ (R | (R >> 1))


def phase_F(R: int) -> int:
    return D(D(R) ^ 1)


def J(z: int) -> int:
    return z ^ ((z >> 1) | (z >> 2))


def invJ(y: int) -> int:
    """Invert J on ordinary finite integers by descending bit recurrence."""
    x = 0
    for j in range(y.bit_length() - 1, -1, -1):
        x |= (bit(y, j) ^ (bit(x, j + 1) | bit(x, j + 2))) << j
    return x


def invF_candidate(R_next: int) -> int:
    return invJ(invJ(R_next >> 2))


def a2_local_rhs(L: int, j: int) -> int:
    e = [bit(L, j + k) for k in range(5)]
    # A^2(L)_j = ell_(j+4) XOR B(ell_j,...,ell_(j+3)).
    a_j = e[2] ^ (e[1] | e[0])
    a_j1 = e[3] ^ (e[2] | e[1])
    b = (e[3] | e[2]) ^ (a_j1 | a_j)
    return e[4] ^ b


def recover_left_from_branch(y: int, low4: int, total_bits: int) -> int:
    """Generate the unique bit string through total_bits for fixed low four."""
    bits = [bit(low4, j) for j in range(4)]
    for j in range(total_bits - 4):
        local = bits[j:j + 4]
        a_j = local[2] ^ (local[1] | local[0])
        a_j1 = local[3] ^ (local[2] | local[1])
        b = (local[3] | local[2]) ^ (a_j1 | a_j)
        bits.append(bit(y, j) ^ b)
    return sum(v << j for j, v in enumerate(bits))


def inverse_branch_transducer(z: int, low4: int) -> tuple[int, tuple[int, int, int, int]]:
    """Run the proof note's 16-state inverse on all significant output bits."""
    window = [bit(low4, j) for j in range(4)]
    recovered = window[:]
    for j in range(z.bit_length()):
        a, b, c, d = window
        B = (d | c) ^ ((d ^ (c | b)) | (c ^ (b | a)))
        e = bit(z, j) ^ B
        window = [b, c, d, e]
        recovered.append(e)
    return sum(v << j for j, v in enumerate(recovered)), tuple(window)


def git_commit() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def main() -> None:
    enforce_caps()
    # Sparse-cell literal controls: every L=3 (mod 4), 0 <= L < 256,
    # crossed with every 0 <= R < 64.  This also tests both valid and invalid
    # compatibility gates with a second implementation of the CA dynamics.
    ls = [L for L in range(256) if L % 4 == 3]
    rs = list(range(64))
    pair_count = valid_count = invalid_count = 0
    valid_left_exact = invalid_lowpair = 0
    right_exact = left_high_exact = phase1_center_zero = 0
    full_outputs: dict[tuple[int, int], tuple[int, int]] = {}
    actual_output_pair_collisions = []
    invalid_examples = []
    for L in ls:
        for R in rs:
            pair_count += 1
            gate = L % 16 == (7 if R % 4 == 0 else 11)
            cells0 = raw_halves(L, R)
            cells1 = raw_step(cells0)
            cells2 = raw_step(cells1)
            phase1_center_zero += int(cells1.get(0, 0) == 0)
            actual_L, actual_R = halves(cells2)
            returned_lowpair = (actual_L & 3) == 3
            assert returned_lowpair == gate, (L, R, gate, actual_L)
            assert actual_L >> 2 == A2(L), (L, R, actual_L, A2(L))
            assert actual_R == phase_F(R), (L, R, actual_R, phase_F(R))
            left_high_exact += 1
            right_exact += 1
            if gate:
                valid_count += 1
                assert actual_L == psi(L)
                valid_left_exact += 1
                out = (psi(L), phase_F(R))
                if out in full_outputs:
                    actual_output_pair_collisions.append((full_outputs[out], (L, R), out))
                full_outputs[out] = (L, R)
            else:
                invalid_count += 1
                assert not returned_lowpair
                invalid_lowpair += 1
                assert actual_L != psi(L)
                if len(invalid_examples) < 4:
                    invalid_examples.append({"L": L, "R": R, "actual_L_low2": actual_L & 3,
                                             "required_L_mod16": 7 if R % 4 == 0 else 11})
    assert pair_count == 4096 and valid_count == 1024 and invalid_count == 3072
    assert phase1_center_zero == pair_count
    assert len(full_outputs) == valid_count and not actual_output_pair_collisions

    # Check exact bit-length claims and small identities on larger, still tiny
    # integer domains, independent of the sparse CA enumeration.
    len_cases = 4096
    for L in range(3, 4096, 4):
        assert psi(L).bit_length() == L.bit_length() + 2
    for R in range(4096):
        expected_growth = R.bit_length() + 2
        assert phase_F(R).bit_length() == expected_growth
    for L in range(4096):
        for j in range(12):
            assert bit(A2(L), j) == a2_local_rhs(L, j), (L, j)
    recurrence_cases = 4096 * 12

    # Right-map identities, finite J bijection, and inverse-forward check.
    for z in range(4096):
        assert D(z) >> 1 == J(z)
        assert J(z) >> 1 == J(z >> 1)
        assert phase_F(z) >> 2 == J(J(z))
        assert invJ(J(z)) == z
    for y in range(4096):
        assert J(invJ(y)) == y
    inverse_cases = 4096
    for R in range(4096):
        assert invF_candidate(phase_F(R)) == R
    forward_checked_successors = 0
    forward_rejected_successors = 0
    first_rejected_successor = None
    for R_next in range(1024):
        candidate = invF_candidate(R_next)
        if phase_F(candidate) == R_next:
            forward_checked_successors += 1
        else:
            forward_rejected_successors += 1
            if first_rejected_successor is None:
                first_rejected_successor = {"R_next": R_next, "candidate": candidate,
                                            "forward_image": phase_F(candidate)}

    # Fixed gate branches recover a unique finite left input in representative
    # collisions and across the full finite control range.
    left_branch_checks = 0
    for L in ls:
        recovered = recover_left_from_branch(A2(L), L & 15, 20)
        assert recovered & ((1 << 8) - 1) == L
        assert recovered >> 8 == 0
        left_branch_checks += 1
    rec171 = recover_left_from_branch(A2(171), 171 & 15, 20)
    rec199 = recover_left_from_branch(A2(199), 199 & 15, 20)
    assert (A(171), A2(171), psi(171)) == (213, 202, 811)
    assert (A(199), A2(199), psi(199)) == (214, 202, 811)
    assert (rec171, rec199) == (171, 199)
    assert (171 % 16, 199 % 16, phase_F(1), phase_F(0)) == (11, 7, 7, 3)

    # Exhaust the proposed four-bit-window inverse rule on every local window
    # and next bit, then compare its terminal-zero criterion against literal
    # finite preimages for every z<4096 and both gate branches.
    b_truth_cases = 0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    B = (d | c) ^ ((d ^ (c | b)) | (c ^ (b | a)))
                    for e in range(2):
                        word = a | (b << 1) | (c << 2) | (d << 3) | (e << 4)
                        assert bit(A2(word), 0) == (e ^ B)
                        b_truth_cases += 1
    preimages: dict[tuple[int, int], list[int]] = {}
    for L in range(4096):
        if L % 16 in (7, 11):
            preimages.setdefault((A2(L), L % 16), []).append(L)
    finite_criterion_checks = 0
    terminal_zero_positive = 0
    for z in range(4096):
        for low4 in (7, 11):
            candidate, terminal = inverse_branch_transducer(z, low4)
            has_finite = bool(preimages.get((z, low4), []))
            assert (terminal == (0, 0, 0, 0)) == has_finite, (z, low4, candidate, terminal, has_finite)
            if terminal == (0, 0, 0, 0):
                assert A2(candidate) == z
                assert candidate % 16 == low4
                assert candidate == preimages[(z, low4)][0]
                terminal_zero_positive += int(z > 0)
            finite_criterion_checks += 1

    payload = {
        "experiment_id": "problem1_period_two_phase_maps_independent_20261008",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(),
        "question": "problem1",
        "detailed_question": "Do literal Rule 30 controls agree with the proposed period-two half-row maps and compatibility gate, and do the stated integer inverse identities hold on targeted finite domains?",
        "hypothesis": "For L=3 mod 4, center and left neighbor return to 11 after two steps exactly on the stated gate; on that gate the whole halves are (Psi(L),F(R)). The finite J inverse and fixed-branch A^2 recurrence behave as stated.",
        "interpretation": "All bounded controls passed, including the 32-case inverse local rule and finite preimage terminal criterion for both branches over z<4096. This independently supports the exact local formulas and one-step finite inverse test but does not establish termination of the compatibility gate for all iterates or exclude eventual period two.",
        "status": "finite-exhaustive",
        "proof_scope": "Finite control only; the all-integer algebraic derivations are reviewed in the companion review note.",
        "backend": "Independent Python sparse-cell dictionary using literal Rule 30 updates, plus separate elementary integer bit-map implementations; no producer code imported.",
        "parameters": {
            "literal_control_domain": {"L": "0 <= L < 256 and L mod 4 = 3", "R": "0 <= R < 64", "pairs": pair_count},
            "integer_identity_domains": {"A2_local_recurrence_L": "0 <= L < 4096, bit positions 0..11", "right_map_R": "0 <= R < 4096", "arbitrary_successor_candidates": "0 <= R_next < 1024"},
            "left_inverse_branches": "all L in literal domain; 20 output bits generated for each fixed low-four branch"
        },
        "results": {
            "literal_pairs": pair_count,
            "valid_gate_pairs": valid_count,
            "invalid_gate_pairs": invalid_count,
            "valid_pairs_matching_full_Psi_left_map": valid_left_exact,
            "invalid_pairs_rejected_by_low_pair_return": invalid_lowpair,
            "all_pairs_matching_A2_high_left_bits": left_high_exact,
            "all_pairs_matching_full_right_F_map": right_exact,
            "all_first_step_centers_zero": phase1_center_zero,
            "valid_full_pair_map_outputs_unique": len(full_outputs) == valid_count,
            "valid_full_pair_output_collisions": actual_output_pair_collisions,
            "invalid_examples": invalid_examples,
            "bitlength_cases": len_cases,
            "A2_local_recurrence_bit_checks": recurrence_cases,
            "J_inverse_checks_each_direction": inverse_cases,
            "right_inverse_candidates_forward_accepted": forward_checked_successors,
            "right_inverse_candidates_forward_rejected": forward_rejected_successors,
            "first_rejected_arbitrary_successor": first_rejected_successor,
            "fixed_branch_left_recovery_checks": left_branch_checks,
            "inverse_B_truth_table_cases": b_truth_cases,
            "finite_inverse_terminal_criterion_checks": finite_criterion_checks,
            "finite_inverse_terminal_zero_cases": terminal_zero_positive,
            "collision": {"L1": 171, "L2": 199, "A2_both": 202, "Psi_both": 811,
                          "gate_residues": [11, 7], "F_of_R1": phase_F(1), "F_of_R0": phase_F(0)}
        },
        "resource_limits": {"wall_seconds": WALL_CAP_SECONDS, "address_space_bytes": MEMORY_CAP_BYTES,
                            "enforced": True},
        "runtime_seconds": round(time.monotonic() - START, 6),
        "hardware": {"platform": platform.platform(), "machine": platform.machine(),
                     "processor": platform.processor() or "unspecified", "logical_cpu_count": os.cpu_count()},
        "software": {"python": sys.version, "implementation": platform.python_implementation()},
        "result_hashes": {"verifier_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest()},
        "result_summary": {"literal_pairs": pair_count, "valid_gate_pairs": valid_count,
                           "invalid_gate_pairs": invalid_count,
                           "valid_pairs_matching_full_Psi_left_map": valid_left_exact,
                           "all_pairs_matching_full_right_F_map": right_exact,
                           "inverse_B_truth_table_cases": b_truth_cases,
                           "finite_inverse_terminal_criterion_checks": finite_criterion_checks},
        "provenance": {
            "git_commit": git_commit(),
            "script_path": str(SCRIPT.relative_to(ROOT)),
            "script_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
            "reviewed_note_path": "proofs/informal/problem1_period_two_phase_maps_20261008.md",
            "reviewed_note_sha256": hashlib.sha256((ROOT / "proofs/informal/problem1_period_two_phase_maps_20261008.md").read_bytes()).hexdigest(),
            "independent_implementation": True,
            "imports_producer_transition_or_inverse": False,
            "hardware": {"platform": platform.platform(), "machine": platform.machine(),
                         "processor": platform.processor() or "unspecified"},
            "software": {"python": sys.version, "implementation": platform.python_implementation()}
        },
        "limitations": [
            "The sparse-cell control exhausts only L<256 with L mod 4=3 and R<64.",
            "Finite identity domains corroborate the local inverse algebra but do not replace its symbolic proof.",
            "No experiment here proves that every finite pair eventually violates the gate.",
            "No conclusion about Problem 1 or all eventual temporal periods follows from these checks."
        ]
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256_excluding_this_field"] = hashlib.sha256(canonical).hexdigest()
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    atomic_write(OUT, encoded)
    print(json.dumps({"output": str(OUT), "pairs": pair_count, "valid": valid_count,
                      "invalid": invalid_count, "runtime_seconds": payload["runtime_seconds"],
                      "script_sha256": payload["provenance"]["script_sha256"],
                      "result_sha256": hashlib.sha256(encoded).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
