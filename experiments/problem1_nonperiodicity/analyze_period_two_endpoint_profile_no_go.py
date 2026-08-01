#!/usr/bin/env python3
"""Exact one-step endpoint profiles and a concrete two-step path-lifting no-go."""
from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

PHASE = "u"
ALLOWED_MASKS = (0b0000, 0b0011, 0b1011, 0b1100, 0b1111)
DEFAULT_MAXIMUM_COMPLEXITY = 22
ABSOLUTE_MAXIMUM_COMPLEXITY = 22

CURRENT_COMPLEXITY = 19
CURRENT = 0x1BCD3A1C36
GOOD_SHADOW = 0x642E240C2
BAD_SHADOW = 0x642E27436
CONTINUATION_WORD = (3, 0)


class EndpointProfileLimitError(RuntimeError):
    """Raised before a controlled campaign exceeds its configured cap."""


def forward_generator(name: str, state: int) -> int:
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def frontier_children(state: int) -> tuple[int, ...]:
    return tuple(sorted({forward_generator(name, state) for name in "tup"}))


def build_levels(maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {1}]
    for _ in range(2, maximum_complexity + 1):
        levels.append(
            {child for state in levels[-1] for child in frontier_children(state)}
        )
    return levels


def fiber_mask(levels: list[set[int]], complexity: int, state: int) -> int:
    mask = sum(
        1 << digit
        for digit in range(4)
        if 4 * state + digit in levels[complexity + 1]
    )
    if mask not in ALLOWED_MASKS:
        raise AssertionError("fiber escaped the five-mask alphabet")
    return mask


def endpoint_profile(
    levels: list[set[int]], complexity: int, state: int
) -> tuple[int, tuple[int | None, ...]]:
    """Return own fiber and presence-sensitive child fibers.

    ``None`` means the child does not exist. A present child whose own fiber is
    ``0000`` is retained as the integer zero, so absence and a terminal child
    are not conflated.
    """
    own = fiber_mask(levels, complexity, state)
    children: list[int | None] = []
    for digit in range(4):
        child = 4 * state + digit
        if child in levels[complexity + 1]:
            children.append(fiber_mask(levels, complexity + 1, child))
        else:
            children.append(None)
    return own, tuple(children)


def synchronized_or_full_pair(
    levels: list[set[int]], complexity: int, current: int, shadow: int
) -> bool:
    if current not in levels[complexity]:
        return False
    if shadow not in levels[complexity - 1]:
        return False
    if current & 3 != shadow & 3:
        return False
    current_mask = fiber_mask(levels, complexity, current)
    shadow_mask = fiber_mask(levels, complexity - 1, shadow)
    return not (current_mask & ~shadow_mask) and (
        shadow_mask == 0b1111 or shadow_mask == current_mask
    )


def lift_pair(
    levels: list[set[int]], complexity: int, current: int, shadow: int, digit: int
) -> tuple[int, int] | None:
    if digit not in range(4):
        raise ValueError("digit must lie in {0,1,2,3}")
    next_current = 4 * current + digit
    next_shadow = 4 * shadow + digit
    if synchronized_or_full_pair(
        levels, complexity + 1, next_current, next_shadow
    ):
        return next_current, next_shadow
    return None


def follow_word(
    levels: list[set[int]],
    complexity: int,
    current: int,
    shadow: int,
    word: tuple[int, ...],
) -> tuple[tuple[int, int], ...] | None:
    path: list[tuple[int, int]] = [(current, shadow)]
    for digit in word:
        lifted = lift_pair(levels, complexity, current, shadow, digit)
        if lifted is None:
            return None
        current, shadow = lifted
        complexity += 1
        path.append(lifted)
    return tuple(path)


def pair_step_details(
    levels: list[set[int]],
    complexity: int,
    current: int,
    shadow: int,
    word: tuple[int, ...],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for digit in word:
        next_current = 4 * current + digit
        next_shadow = 4 * shadow + digit
        current_exists = next_current in levels[complexity + 1]
        shadow_exists = next_shadow in levels[complexity]
        current_mask = (
            fiber_mask(levels, complexity + 1, next_current)
            if current_exists
            else None
        )
        shadow_mask = (
            fiber_mask(levels, complexity, next_shadow) if shadow_exists else None
        )
        dominant = bool(
            current_exists
            and shadow_exists
            and current_mask is not None
            and shadow_mask is not None
            and not (current_mask & ~shadow_mask)
        )
        synchronized = bool(
            dominant
            and (shadow_mask == 0b1111 or shadow_mask == current_mask)
        )
        rows.append(
            {
                "digit": digit,
                "current_hex": hex(next_current),
                "shadow_hex": hex(next_shadow),
                "current_exists": current_exists,
                "shadow_exists": shadow_exists,
                "current_mask": (
                    f"{current_mask:04b}" if current_mask is not None else None
                ),
                "shadow_mask": (
                    f"{shadow_mask:04b}" if shadow_mask is not None else None
                ),
                "dominant": dominant,
                "synchronized_or_full": synchronized,
            }
        )
        if not synchronized:
            break
        current, shadow = next_current, next_shadow
        complexity += 1
    return rows


def legal_one_digit_summary(
    levels: list[set[int]], complexity: int, current: int, shadow: int
) -> dict[int, tuple[int, int] | None]:
    return {
        digit: lift_pair(levels, complexity, current, shadow, digit)
        for digit in range(4)
    }


def one_digit_type_summary(
    levels: list[set[int]], complexity: int, current: int, shadow: int
) -> tuple[tuple[bool, int | None, int | None], ...]:
    rows: list[tuple[bool, int | None, int | None]] = []
    for digit in range(4):
        next_current = 4 * current + digit
        next_shadow = 4 * shadow + digit
        current_exists = next_current in levels[complexity + 1]
        shadow_exists = next_shadow in levels[complexity]
        if not current_exists or not shadow_exists:
            rows.append((False, None, None))
            continue
        current_mask = fiber_mask(levels, complexity + 1, next_current)
        shadow_mask = fiber_mask(levels, complexity, next_shadow)
        legal = not (current_mask & ~shadow_mask) and (
            shadow_mask == 0b1111 or shadow_mask == current_mask
        )
        rows.append((legal, current_mask, shadow_mask))
    return tuple(rows)


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
) -> dict[str, Any]:
    if not CURRENT_COMPLEXITY + len(CONTINUATION_WORD) + 1 <= maximum_complexity:
        raise EndpointProfileLimitError(
            "maximum complexity is too small for the explicit two-step obstruction"
        )
    if maximum_complexity > ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise EndpointProfileLimitError("maximum complexity outside controlled range")

    levels = build_levels(maximum_complexity)
    current_profile = endpoint_profile(levels, CURRENT_COMPLEXITY, CURRENT)
    good_profile = endpoint_profile(
        levels, CURRENT_COMPLEXITY - 1, GOOD_SHADOW
    )
    bad_profile = endpoint_profile(levels, CURRENT_COMPLEXITY - 1, BAD_SHADOW)

    if good_profile != bad_profile:
        raise AssertionError("shadow endpoint profiles unexpectedly differ")
    if not synchronized_or_full_pair(
        levels, CURRENT_COMPLEXITY, CURRENT, GOOD_SHADOW
    ):
        raise AssertionError("good starting pair is not synchronized/full")
    if not synchronized_or_full_pair(
        levels, CURRENT_COMPLEXITY, CURRENT, BAD_SHADOW
    ):
        raise AssertionError("bad starting pair is not synchronized/full")

    good_path = follow_word(
        levels,
        CURRENT_COMPLEXITY,
        CURRENT,
        GOOD_SHADOW,
        CONTINUATION_WORD,
    )
    bad_path = follow_word(
        levels,
        CURRENT_COMPLEXITY,
        CURRENT,
        BAD_SHADOW,
        CONTINUATION_WORD,
    )
    if good_path is None or bad_path is not None:
        raise AssertionError("two-step profile obstruction changed")

    payload: dict[str, Any] = {
        "status": "exact-one-step-endpoint-profile-and-two-step-path-lifting-no-go",
        "maximum_complexity": maximum_complexity,
        "phase": PHASE,
        "outputs_built": sum(len(levels[k]) for k in range(1, maximum_complexity + 1)),
        "theorem": {
            "endpoint_profile": (
                "The exact one-step endpoint profile records the endpoint fiber and, "
                "for each digit, absence or the existing child's fiber."
            ),
            "one_step_exactness": (
                "For a synchronized/full concrete endpoint pair, the paired profile "
                "determines every legal common one-digit lift and the lifted local "
                "fiber pair."
            ),
            "path_lifting_no_go": (
                "Equal paired one-step profiles do not imply equal two-digit "
                "synchronized/full continuation languages."
            ),
        },
        "obstruction": {
            "complexity": CURRENT_COMPLEXITY,
            "current_hex": hex(CURRENT),
            "good_shadow_hex": hex(GOOD_SHADOW),
            "bad_shadow_hex": hex(BAD_SHADOW),
            "current_profile": {
                "own_mask": f"{current_profile[0]:04b}",
                "child_masks": [
                    f"{mask:04b}" if mask is not None else None
                    for mask in current_profile[1]
                ],
            },
            "common_shadow_profile": {
                "own_mask": f"{good_profile[0]:04b}",
                "child_masks": [
                    f"{mask:04b}" if mask is not None else None
                    for mask in good_profile[1]
                ],
            },
            "profiles_equal": good_profile == bad_profile,
            "one_digit_summaries_equal": (
                one_digit_type_summary(
                    levels, CURRENT_COMPLEXITY, CURRENT, GOOD_SHADOW
                )
                == one_digit_type_summary(
                    levels, CURRENT_COMPLEXITY, CURRENT, BAD_SHADOW
                )
            ),
            "continuation_word": list(CONTINUATION_WORD),
            "good_path": [
                {"current_hex": hex(current), "shadow_hex": hex(shadow)}
                for current, shadow in good_path
            ],
            "good_steps": pair_step_details(
                levels,
                CURRENT_COMPLEXITY,
                CURRENT,
                GOOD_SHADOW,
                CONTINUATION_WORD,
            ),
            "bad_steps": pair_step_details(
                levels,
                CURRENT_COMPLEXITY,
                CURRENT,
                BAD_SHADOW,
                CONTINUATION_WORD,
            ),
            "conclusion": (
                "The profile quotient can splice the digit-3 transition of the bad "
                "pair with the digit-0 continuation witnessed by the good pair. The "
                "bad concrete realization instead reaches masks 0000/1011 and leaves "
                "the synchronized/full relation."
            ),
        },
        "scientific_boundary": (
            "The one-step exactness and the explicit two-step obstruction are exact. "
            "This rules out this paired one-step profile as a path-lifting invariant, "
            "but it does not rule out richer finite endpoint states or prove the "
            "all-depth adjacent-shadow inclusion."
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--maximum-complexity", type=int, default=DEFAULT_MAXIMUM_COMPLEXITY
    )
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_complexity), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
