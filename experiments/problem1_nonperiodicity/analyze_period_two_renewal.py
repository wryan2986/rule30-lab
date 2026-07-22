#!/usr/bin/env python3
"""Reduce period-two zero emissions to an exact renewal and integer map.

For the pure alternating temporal trace, the accumulated inverse word satisfies
``H_(m+1) = (H_m)_11 p q_m``.  This analyzer checks two exact structural
reductions used by the accompanying informal proof:

* a zero emitted base-4 block extends the leading ``t`` run by one, while a
  nonzero block resets it;
* during a zero streak, the normalized word preimage ``x = K^-1(0)`` evolves
  by a partial ordinary-integer recurrence controlled by ``x mod 16``.

The exhaustive checks are finite regression evidence for all-width identities
proved separately.  They do not exclude eventual period two or solve Rule 30
center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import product
from typing import Any


DEFAULT_MAX_WORD_LENGTH = 8
DEFAULT_ACTUAL_BLOCKS = 512
ABSOLUTE_MAX_WORD_LENGTH = 10
ABSOLUTE_ACTUAL_BLOCKS = 4_096
LETTERS = ("t", "p", "u")
_ROOT_FLIP = {"t": 0, "p": 1, "u": 1}
_SECTIONS = {
    "t": ("t", "p"),
    "p": ("p", "u"),
    "u": ("p", "t"),
}


class PeriodTwoRenewalLimitError(RuntimeError):
    """Raised before an explicitly capped finite campaign is exceeded."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def inverse_word_root(word: tuple[str, ...], root: int) -> int:
    """Apply the root action of an inverse word to one bit."""

    if root not in (0, 1):
        raise ValueError("root must be binary")
    return root ^ (sum(_ROOT_FLIP[name] for name in word) & 1)


def inverse_word_section(
    word: tuple[str, ...], root: int
) -> tuple[str, ...]:
    """Section an outermost-to-innermost composition word."""

    if root not in (0, 1):
        raise ValueError("root must be binary")
    selected = [""] * len(word)
    current = root
    for index in range(len(word) - 1, -1, -1):
        name = word[index]
        selected[index] = _SECTIONS[name][current]
        current ^= _ROOT_FLIP[name]
    return tuple(selected)


def section_along(
    word: tuple[str, ...], path: tuple[int, ...]
) -> tuple[str, ...]:
    """Take successive binary-tree sections along ``path``."""

    for root in path:
        word = inverse_word_section(word, root)
    return word


def emitted_block(word: tuple[str, ...]) -> int:
    """Return the two spatial bits emitted by temporal block ``10``."""

    return (1 ^ inverse_word_root(word, 0)) + 2 * (
        1 ^ inverse_word_root(inverse_word_section(word, 1), 0)
    )


def forward_generator(name: str, state: int) -> int:
    """Apply the forward map inverse to one letter ``t``, ``p``, or ``u``."""

    if state < 0:
        raise ValueError("state must be nonnegative")
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    if name == "u":
        return stepped ^ 1
    raise ValueError(f"unknown generator {name!r}")


def inverse_word_preimage_zero(word: tuple[str, ...]) -> int:
    """Return the ordinary integer ``word^-1(0)``."""

    state = 0
    for name in word:
        state = forward_generator(name, state)
    return state


def normalize_word(word: tuple[str, ...]) -> tuple[str, ...]:
    """Remove the leading run of letters ``t``."""

    offset = next(
        (index for index, name in enumerate(word) if name != "t"),
        len(word),
    )
    return word[offset:]


def leading_signature(word: tuple[str, ...]) -> tuple[int, str | None]:
    """Return the leading-``t`` length and first non-``t`` letter."""

    normalized = normalize_word(word)
    leading = len(word) - len(normalized)
    return leading, normalized[0] if normalized else None


def block_update(word: tuple[str, ...], q_name: str) -> tuple[str, ...]:
    """Apply ``H -> H_11 p q`` for ``q`` equal to ``t`` or ``u``."""

    if q_name not in ("t", "u"):
        raise ValueError("q_name must be 't' or 'u'")
    return section_along(word, (1, 1)) + ("p", q_name)


def combined_section_table() -> list[dict[str, Any]]:
    """Return the exact four-state letter transducer for section ``11``.

    State ``(a,b)`` is the pair of roots presented to the first and second
    section passes while scanning the original word from inner to outer.
    """

    rows: list[dict[str, Any]] = []
    for first_root, second_root in product((0, 1), repeat=2):
        for name in LETTERS:
            first_section = _SECTIONS[name][first_root]
            output = _SECTIONS[first_section][second_root]
            next_state = (
                first_root ^ _ROOT_FLIP[name],
                second_root ^ _ROOT_FLIP[first_section],
            )
            rows.append(
                {
                    "state": [first_root, second_root],
                    "input": name,
                    "output": output,
                    "next_state": list(next_state),
                }
            )
    return rows


def expected_renewal_successor(
    word: tuple[str, ...], beta: int
) -> tuple[int, str]:
    """Return the all-width renewal-law prediction for the next signature."""

    leading, first_non_t = leading_signature(word)
    if first_non_t is None:
        raise ValueError("renewal law is stated only for a non-all-t word")
    if beta == 0:
        return leading + 1, first_non_t
    if beta == 1:
        return 0, "u"
    if beta in (2, 3):
        return 0, "p"
    raise ValueError("beta must be a two-bit block")


def verify_word_reductions(maximum_length: int) -> dict[str, Any]:
    """Exhaust finite words as regression checks for the exact reductions."""

    if maximum_length <= 0:
        raise ValueError("maximum length must be positive")
    words_checked = 0
    renewal_branches_checked = 0
    integer_branches_checked = 0
    beta_counts: Counter[int] = Counter()

    for length in range(1, maximum_length + 1):
        for word in product(LETTERS, repeat=length):
            if all(name == "t" for name in word):
                continue
            words_checked += 1
            beta = emitted_block(word)
            beta_counts[beta] += 1
            normalized = normalize_word(word)
            x_value = inverse_word_preimage_zero(normalized)
            if (beta == 0) != (x_value % 4 == 3):
                raise AssertionError("zero emission and x mod 4 disagree")

            for q_name in ("t", "u"):
                updated = block_update(word, q_name)
                expected = expected_renewal_successor(word, beta)
                if leading_signature(updated) != expected:
                    raise AssertionError("renewal signature identity failed")
                renewal_branches_checked += 1

                if beta != 0:
                    continue
                normalized_updated = normalize_word(updated)
                updated_x = inverse_word_preimage_zero(normalized_updated)
                predicted_x = forward_generator(
                    q_name,
                    forward_generator("p", x_value >> 2),
                )
                if updated_x != predicted_x:
                    raise AssertionError("normalized integer recurrence failed")
                if emitted_block(normalized_updated) == 0:
                    if updated_x.bit_length() != x_value.bit_length() + 2:
                        raise AssertionError("continuing integer degree law failed")
                expected_continuation = (
                    x_value % 16 == (11 if q_name == "t" else 7)
                )
                if (emitted_block(normalized_updated) == 0) != expected_continuation:
                    raise AssertionError("mod-16 continuation criterion failed")
                integer_branches_checked += 1

    return {
        "maximum_word_length": maximum_length,
        "non_all_t_words_checked": words_checked,
        "renewal_q_branches_checked": renewal_branches_checked,
        "zero_emission_integer_q_branches_checked": integer_branches_checked,
        "beta_counts": {str(key): beta_counts[key] for key in range(4)},
        "all_checks_pass": True,
    }


def forced_zero_step(x_value: int) -> tuple[str, int] | None:
    """Advance the normalized integer when another zero block is possible.

    Returns the uniquely required ``q`` letter and successor.  ``None`` means
    neither schedule branch can emit another zero block.
    """

    if x_value < 0 or x_value % 4 != 3:
        raise ValueError("x must be a nonnegative integer congruent to 3 mod 4")
    residue = x_value % 16
    if residue == 7:
        q_name = "u"
    elif residue == 11:
        q_name = "t"
    else:
        return None
    return q_name, forward_generator(
        q_name,
        forward_generator("p", x_value >> 2),
    )


def continuation_table() -> list[dict[str, Any]]:
    """Return the four exact low-residue outcomes for a zero-emitting state."""

    rows = []
    for y_mod_4 in range(4):
        x_mod_16 = 4 * y_mod_4 + 3
        p_value = forward_generator("p", y_mod_4)
        outcomes = {
            q_name: forward_generator(q_name, p_value) % 4
            for q_name in ("t", "u")
        }
        rows.append(
            {
                "x_mod_16": x_mod_16,
                "x_shifted_mod_4": y_mod_4,
                "successor_mod_4": outcomes,
                "zero_continuation_q": next(
                    (
                        q_name
                        for q_name, residue in outcomes.items()
                        if residue == 3
                    ),
                    None,
                ),
            }
        )
    return rows


def section_head_for_pair(pair: tuple[int, int]) -> str:
    if pair == (0, 0):
        return "T"
    if pair == (1, 0):
        return "U"
    if pair in ((0, 1), (1, 1)):
        return "P"
    raise ValueError("pair must be binary")


def advance_fringe(tail: tuple[int, ...]) -> tuple[int, ...]:
    """Apply the exact two-step alternating moving-fringe map."""

    radius = len(tail)
    row = (1,) + tail + (0, 0)
    first = tuple(
        row[index] ^ (row[index + 1] | row[index + 2])
        for index in range(radius + 1)
    )
    return tuple(
        (0 if distance == 1 else first[distance - 2])
        ^ (first[distance - 1] | first[distance])
        for distance in range(1, radius + 1)
    )


def fringe_heads(maximum_block: int) -> list[str]:
    """Generate exact period-two schedule heads through ``maximum_block``."""

    width = 2 * maximum_block + 8
    tail = (0,) * width
    heads = []
    for block in range(maximum_block + 1):
        heads.append(section_head_for_pair((tail[1], tail[0])))
        if block < maximum_block:
            tail = advance_fringe(tail)
    return heads


def actual_renewal_path(maximum_block: int) -> dict[str, Any]:
    """Check the exact renewal law along the true alternating inverse path."""

    heads = fringe_heads(maximum_block)
    word: tuple[str, ...] = ()
    previous_deficit = -1
    maximum_leading = -1
    leading_records: list[dict[str, Any]] = []
    leading_counts: Counter[int] = Counter()
    first_run_above_two = None

    for block in range(maximum_block + 1):
        beta = emitted_block(word)
        leading, first_non_t = leading_signature(word)
        deficit = block - leading
        if block > 0 and deficit < previous_deficit:
            raise AssertionError("leading-run deficit must be nondecreasing")
        previous_deficit = deficit
        leading_counts[leading] += 1
        if leading > maximum_leading:
            maximum_leading = leading
            entry = {
                "block": block,
                "leading_t_run": leading,
                "emitted_block": beta,
                "first_non_t": first_non_t,
                "block_minus_leading_t_run": deficit,
            }
            leading_records.append(entry)
            if leading > 2 and first_run_above_two is None:
                first_run_above_two = entry

        if block == maximum_block:
            break
        q_name = "u" if heads[block] == "T" else "t"
        updated = block_update(word, q_name)
        if block > 0:
            expected = expected_renewal_successor(word, beta)
            if leading_signature(updated) != expected:
                raise AssertionError("actual path violates renewal law")
        word = updated

    return {
        "maximum_block": maximum_block,
        "states_checked_inclusive": maximum_block + 1,
        "maximum_leading_t_run": maximum_leading,
        "first_record_for_each_new_maximum": leading_records,
        "first_leading_run_above_two": first_run_above_two,
        "leading_run_counts": {
            str(key): leading_counts[key] for key in sorted(leading_counts)
        },
        "deficit_monotonicity_checked": True,
    }


def run_campaign(
    *,
    maximum_word_length: int = DEFAULT_MAX_WORD_LENGTH,
    actual_blocks: int = DEFAULT_ACTUAL_BLOCKS,
) -> dict[str, Any]:
    """Run the bounded regression campaign for the exact renewal reduction."""

    if maximum_word_length > ABSOLUTE_MAX_WORD_LENGTH:
        raise PeriodTwoRenewalLimitError(
            f"word length exceeds absolute maximum {ABSOLUTE_MAX_WORD_LENGTH}"
        )
    if actual_blocks > ABSOLUTE_ACTUAL_BLOCKS:
        raise PeriodTwoRenewalLimitError(
            f"actual blocks exceed absolute maximum {ABSOLUTE_ACTUAL_BLOCKS}"
        )

    word_checks = verify_word_reductions(maximum_word_length)
    actual_path = actual_renewal_path(actual_blocks)
    table = continuation_table()
    transducer = combined_section_table()

    payload = {
        "word_reduction_checks": word_checks,
        "actual_alternating_path": actual_path,
        "combined_section_11_transducer": transducer,
        "integer_continuation_table": table,
        "exact_reductions": {
            "renewal_law": (
                "beta=0 extends the leading t run by one and preserves its "
                "first non-t letter; beta=1 resets to u; beta=2 or 3 resets "
                "to p"
            ),
            "deficit_law": (
                "d_m=m-ell_m is unchanged on beta_m=0 and becomes m+1 on "
                "beta_m!=0"
            ),
            "normalized_integer_law": (
                "for beta=0, x'=Q(P(x>>2)); another zero is possible only "
                "for x=7 mod 16 with Q=U or x=11 mod 16 with Q=T, and "
                "every continuing step raises bit length by exactly two"
            ),
        },
    }
    certificate = hashlib.sha256()
    certificate.update(b"rule30-period-two-renewal-reduction-v1\0")
    certificate.update(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    )
    payload["certificate_sha256"] = certificate.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check the period-two renewal and integer reductions."
    )
    parser.add_argument(
        "--maximum-word-length",
        type=_positive_integer,
        default=DEFAULT_MAX_WORD_LENGTH,
    )
    parser.add_argument(
        "--actual-blocks",
        type=_positive_integer,
        default=DEFAULT_ACTUAL_BLOCKS,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(
        maximum_word_length=args.maximum_word_length,
        actual_blocks=args.actual_blocks,
    )
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-renewal-reduction-v1",
        "question": "problem1",
        "hypothesis": (
            "Zero-emitting period-two inverse blocks obey an exact renewal "
            "law and reduce to a partial ordinary-integer recurrence whose "
            "continuation branch is fixed by x modulo 16."
        ),
        "backend": "python-exact-word-and-integer",
        "parameters": {
            "maximum_word_length": args.maximum_word_length,
            "actual_blocks": args.actual_blocks,
            "absolute_maximum_word_length": ABSOLUTE_MAX_WORD_LENGTH,
            "absolute_actual_blocks": ABSOLUTE_ACTUAL_BLOCKS,
        },
        "result_summary": result,
        "status": "finite-exhaustive",
        "proof_scope": (
            "The all-width renewal and integer identities are proved in "
            "proofs/informal/problem1_period_two_renewal_reduction.md. The "
            "script exhausts only the stated finite word lengths and actual "
            "path prefix as regression checks."
        ),
        "interpretation": (
            "The original target m-leading_t_run(H_m)->infinity is exactly "
            "equivalent to infinitely many nonzero emitted base-4 blocks. "
            "Any hypothetical final zero streak must follow the displayed "
            "partial integer recurrence forever while matching the unique "
            "period-two schedule branch."
        ),
        "limitations": [
            "finite word exhaustion is not the proof of the all-width identities",
            "the bounded actual path does not prove infinitely many renewals",
            "long zero runs refute only small constant run bounds",
            "the partial integer recurrence may have unclassified infinite orbits",
            "the result does not exclude eventual center period two",
            "the result does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
