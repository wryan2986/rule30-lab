"""Fixed local identities for the conditional three-bit repair theorem.

See problem1_three_bit_exit_repair.md, Section 6, for pre-run admission.
No source, E shadow, or infinite FULL realization is constructed here.
"""

import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import time

from check_round306_two_bit_collapse import RULE, checked_step


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20260907_round306_three_bit_repair.json"
REFERENCE = "src/python/rule30_research_reference.py"
REFERENCE_SHA = "358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def right_truth(bits, center):
    return [RULE[4 * (center if i == 0 else bits[i - 1])
                 + 2 * bits[i] + bits[i + 1]] for i in range(len(bits) - 1)]


def right_packed(bits, center):
    word = center + sum(bit << (i + 1) for i, bit in enumerate(bits))
    output = ((word << 1) ^ (word | (word >> 1))) >> 1
    return [(output >> i) & 1 for i in range(len(bits) - 1)]


def checked_a(word):
    packed = (word >> 2) ^ ((word >> 1) | word)
    cells = sum(RULE[4 * ((word >> (i + 2)) & 1)
                     + 2 * ((word >> (i + 1)) & 1) + ((word >> i) & 1)] << i
                for i in range(word.bit_length()))
    assert packed == cells
    return packed


def deadline(_signal, _frame):
    raise TimeoutError("10-second fixed repair-algebra cap exceeded")


def main():
    started = time.perf_counter()
    cap = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (cap, cap))
    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(10)
    assert sha((ROOT / REFERENCE).read_bytes()) == REFERENCE_SHA
    for left in (0, 1):
        for center in (0, 1):
            for right in (0, 1):
                assert RULE[4 * left + 2 * center + right] == (left ^ (center | right))

    # Four-step hand cone with right bits 00001, center inputs 0,1,1,1.
    hand = [[0, 0, 0, 0, 1], [0, 0, 0, 1], [1, 0, 1], [0, 0], [1]]
    centers = [0, 1, 1, 1]
    for i, center in enumerate(centers):
        assert right_truth(hand[i], center) == hand[i + 1]
        assert right_packed(hand[i], center) == hand[i + 1]

    transition_cases = []
    for ell in (0, 1):
        for bit4 in (0, 1):
            for pair in range(4):
                h, k = pair & 1, pair >> 1
                hat_u = int(pair == 0)
                actual = {-4: bit4, -3: 1, -2: 0, -1: 1,
                          0: 1, 1: 1, 2: 0}
                shadow = {-4: bit4, -3: 1, -2: 0, -1: 0,
                          0: 1 ^ ell, 1: h, 2: k}
                a1, s1 = checked_step(actual), checked_step(shadow)
                a2, s2 = checked_step(a1), checked_step(s1)
                assert [actual[0], a1[0], a2[0]] == [1, 0, 1]
                odd = tuple(a1[i] ^ s1[i] for i in (-2, -1, 0))
                even = tuple(a2[i] ^ s2[i] for i in (-3, -2, -1, 0))
                assert odd == (1, ell, (1 ^ ell) | h)
                assert even == (bit4, 0, (1 ^ ell) | h, (1 ^ ell) | hat_u)
                assert all(a2[i] == s2[i] for i in (-5, -4))
                transition_cases.append({"ell": ell, "input_bit4": bit4,
                                         "shadow_right_pair": pair,
                                         "odd_discrepancies_minus2_through0": odd,
                                         "even_discrepancies_minus3_through0": even})

    transport_cases = []
    for word in range(16):
        a, b, c, d = [(word >> i) & 1 for i in range(4)]
        truth = [0, a, b, c, d]
        packed = list(truth)
        first_bits = []
        for center in centers:
            truth, packed = right_truth(truth, center), right_packed(packed, center)
            assert truth == packed
            first_bits.append(truth[0])
        assert first_bits[:3] == [a, 1 ^ (a | b), a]
        expected = (1 ^ a) * (1 ^ b) * (c | d)
        assert truth == [expected]
        transport_cases.append({"initial_right_bits": [0, a, b, c, d],
                                "first_right_bits_after_steps1_through4": first_bits,
                                "step4_flag": expected})

    constant_one_cases = []
    for u in (0, 1):
        for difference1 in (0, 1):
            for difference2 in (0, 1):
                for bit4 in (0, 1):
                    for bit5 in (0, 1):
                        actual = 3 + 4 * u + 8 * (1 ^ u) + 16 * bit4 + 32 * bit5
                        shadow = actual ^ (2 * difference1 + 4 * difference2)
                        a1, s1 = checked_a(actual), checked_a(shadow)
                        a2, s2 = checked_a(a1), checked_a(s1)
                        low_ones = (s1 & 1) == (s2 & 1) == 1
                        first_strip_necessary = (a1 ^ s1) >> 2 == 0
                        second_strip_necessary = (a2 ^ s2) >> 1 == 0
                        premises = low_ones and first_strip_necessary and second_strip_necessary
                        assert not premises or difference1 == difference2 == 0
                        constant_one_cases.append({"u": u, "d1": difference1,
                                                   "d2": difference2, "bit4": bit4,
                                                   "bit5": bit5, "shadow_next_two_lows_one": low_ones,
                                                   "first_strip_necessary": first_strip_necessary,
                                                   "second_strip_necessary": second_strip_necessary,
                                                   "all_premises": premises})

    odd_entry_cases = []
    for ell in (0, 1):
        for shared_high in range(4):
            for pair in range(4):
                actual = {-5: shared_high >> 1, -4: shared_high & 1,
                          -3: 1, -2: 0, -1: 1, 0: 1, 1: 1, 2: 0}
                shadow = {**actual, -2: 1, -1: 0, 0: 1 ^ ell,
                          1: pair & 1, 2: pair >> 1}
                a1, s1 = checked_step(actual), checked_step(shadow)
                a2, s2 = checked_step(a1), checked_step(s1)
                if ell == 0:
                    assert all(a1[i] == s1[i] for i in range(-5, -1))
                    assert a1[-1] ^ s1[-1] == 1 and a1[-2] == s1[-2] == 0
                    assert a2[-2] ^ s2[-2] == 1
                else:
                    assert all(a2[i] == s2[i] for i in range(-5, 0))
                    actual_cut = sum(actual.get(-i, 0) << i for i in range(6))
                    shadow_cut = sum(shadow.get(-i, 0) << i for i in range(6))
                    assert checked_a(actual_cut) == checked_a(shadow_cut)
                odd_entry_cases.append({"ell": ell, "shared_high_bits": shared_high,
                                        "shadow_right_pair": pair,
                                        "next_even_negative_half_agrees": ell == 1,
                                        "next_even_minus2_discrepancy": a2[-2] ^ s2[-2]})

    assert len(transition_cases) == len(transport_cases) == 16
    assert len(constant_one_cases) == len(odd_entry_cases) == 32
    elapsed = time.perf_counter() - started
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    assert elapsed < 10 and peak < cap
    payload = {"hand_cone": hand, "transition_cases": transition_cases,
               "transport_cases": transport_cases, "constant_one_cases": constant_one_cases,
               "odd_entry_cases": odd_entry_cases}
    sources = [str(Path(__file__).resolve().relative_to(ROOT)), REFERENCE,
               "experiments/problem1_nonperiodicity/check_round306_two_bit_collapse.py",
               "proofs/informal/problem1_three_bit_exit_repair.md",
               "proofs/informal/problem1_two_bit_strip_collapse.md",
               "proofs/informal/problem1_one_bit_shadow_exit.md"]
    cpu = next((line.split(":", 1)[1].strip() for line in
                Path("/proc/cpuinfo").read_text().splitlines()
                if line.startswith("model name")), "unreported")
    record = {
        "experiment_id": "round306-fixed-three-bit-exit-repair-algebra",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                             cwd=ROOT, text=True).strip(),
        "question": "problem1",
        "hypothesis": "The t-source table and four-step shadow flag hold on sixteen assignments each; the constant-one and odd-doubling entry implications hold on thirty-two assignments each.",
        "backend": "Python-hand-rule-truth-table/independent-packed-cut-and-right-row",
        "parameters": {"ell": [0, 1], "input_bit4": [0, 1],
                       "transition_shadow_right_pairs": [0, 1, 2, 3],
                       "transition_actual_right_pair": [1, 0],
                       "transition_actual_bits0_through4": [1, 1, 0, 1, "input_bit4"],
                       "transition_shadow_bit1": 0,
                       "transition_shadow_bit0": "1 XOR ell",
                       "other_initial_cells": 0,
                       "right_cone_first_bit": 0,
                       "right_cone_remaining_words": list(range(16)),
                       "right_cone_bit_order": "a,b,c,d are low-to-high input-word bits",
                       "shadow_center_inputs": centers,
                       "constant_one_variables": ["u", "d1", "d2", "bit4", "bit5"],
                       "constant_one_variable_values": [0, 1],
                       "odd_entry_ell": [0, 1],
                       "odd_entry_shared_bit4_bit5_words": [0, 1, 2, 3],
                       "odd_entry_shadow_right_pairs": [0, 1, 2, 3],
                       "odd_entry_initial_d1_d2": [1, 1],
                       "transition_steps": 2, "right_cone_steps": 4,
                       "cpu_workers": 1, "wall_cap_seconds": 10,
                       "memory_cap_bytes": cap, "output_cap_bytes": 128 * 1024},
        "hardware": {"cpu_model": cpu, "machine": platform.machine(),
                     "logical_cpus": os.cpu_count(), "peak_rss_bytes": peak},
        "software": {"python": sys.version, "platform": platform.platform(),
                     "executable": sys.executable},
        "runtime_seconds": elapsed,
        "runtime_scope": "Main entry through fixed checks; excludes final provenance and serialization.",
        "result_hashes": {"canonical_payload_sha256": sha(json.dumps(
            payload, sort_keys=True, separators=(",", ":")).encode())},
        "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in sources},
        "result_summary": {"all_checks_passed": True, "hand_rule_values": 8,
                           "hand_cone_steps": 4, "transition_cases": 16,
                           "transport_cases": 16, "constant_one_cases": 32,
                           "odd_entry_cases": 32, "caps_passed": True},
        "status": "finite-exhaustive",
        "interpretation": "The local table, transported shadow flag, and entry identities are verified. The no-five-t repair, delay profile, clock accounting, and eventual decomposition are separate conditional all-depth deductions.",
        "proof_scope": "Exactly ninety-six Boolean assignments, eight hand rule values, and one fixed four-step cone.",
        "limitations": ["Local rows are not asserted to be an actual/E-shadow pair.",
                        "Input bit4 is not asserted to equal the next actual gate without FULL.",
                        "The four boundary inputs are assumptions of the local fringe check, derived separately in the proof for the specified shadow passage.",
                        "No numerical check of no-ttttt, infinite induction, or clock growth.",
                        "No infinite FULL model, new source, or further-width search.",
                        "External adversarial review is missing."],
        "payload": payload,
    }
    encoded = (json.dumps(record, indent=2) + "\n").encode()
    assert len(encoded) < 128 * 1024
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=OUT.parent, prefix=OUT.name + ".",
                                         suffix=".tmp", delete=False) as handle:
            temporary = handle.name
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, OUT)
        fd = os.open(OUT.parent, os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    signal.alarm(0)
    print(json.dumps({"result": str(OUT.relative_to(ROOT)),
                      "transition_cases": 16, "transport_cases": 16,
                      "constant_one_cases": 32, "odd_entry_cases": 32,
                      "runtime_seconds": elapsed, "peak_rss_bytes": peak}))


if __name__ == "__main__":
    main()
