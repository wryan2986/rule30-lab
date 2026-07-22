"""Auditable finite sideways reconstruction for Rule 30.

The standard convention in this module is explicit: a trace with ``H + 1``
entries contains ``c_0, ..., c_H`` and therefore has reconstruction horizon
``H``.  It determines exactly the finite initial-left prefix
``x_{-1}(0), ..., x_{-H}(0)`` when the initial right half-line is fixed to
zero.

All claims made by the search helpers are about explicitly bounded finite
sets and finite horizons.  In particular, a finite exclusion is not a proof
that the infinite Rule 30 center trace is not eventually periodic.
"""

from __future__ import annotations

import base64
import hashlib
from collections import Counter, deque
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any


class SidewaysResourceLimitError(RuntimeError):
    """Raised before a configured finite-search resource bound is exceeded."""


@dataclass(frozen=True)
class SidewaysLimits:
    """Conservative, deterministic bounds for reconstruction and searches.

    ``max_logical_cell_updates`` counts the scalar Boolean updates in the two
    finite triangles represented by the packed implementation.  It is a
    worst-case accounting bound, not a runtime estimate.
    """

    max_horizon: int = 10_000
    max_candidates: int = 1_000_000
    max_logical_cell_updates: int = 2_000_000_000
    max_certificate_bytes: int = 16 * 1024 * 1024
    max_graph_states: int = 1_000_000
    max_reported_survivors: int = 128

    def __post_init__(self) -> None:
        nonnegative = {
            "max_horizon": self.max_horizon,
            "max_candidates": self.max_candidates,
            "max_logical_cell_updates": self.max_logical_cell_updates,
            "max_certificate_bytes": self.max_certificate_bytes,
            "max_graph_states": self.max_graph_states,
            "max_reported_survivors": self.max_reported_survivors,
        }
        for name, value in nonnegative.items():
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")


DEFAULT_LIMITS = SidewaysLimits()


def _checked_nonnegative(value: int, *, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _checked_positive(value: int, *, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _checked_bits(
    values: Sequence[int] | Iterable[int],
    *,
    name: str,
    allow_empty: bool,
) -> bytes:
    checked = bytearray()
    for index, value in enumerate(values):
        if not isinstance(value, int) or value not in (0, 1):
            raise ValueError(f"{name}[{index}] must be 0 or 1, got {value!r}")
        checked.append(value)
    if not allow_empty and not checked:
        raise ValueError(f"{name} must be nonempty")
    return bytes(checked)


def _checked_horizon(center: bytes, limits: SidewaysLimits) -> int:
    horizon = len(center) - 1
    if horizon > limits.max_horizon:
        raise SidewaysResourceLimitError(
            f"horizon {horizon} exceeds configured maximum {limits.max_horizon}"
        )
    work = logical_reconstruction_work(horizon)
    if work > limits.max_logical_cell_updates:
        raise SidewaysResourceLimitError(
            f"logical work {work} exceeds configured maximum "
            f"{limits.max_logical_cell_updates}"
        )
    return horizon


def logical_reconstruction_work(horizon: int) -> int:
    """Return the conservative scalar-work count for one reconstruction.

    The packed right-half evolution accounts for ``H * H`` logical sites and
    the shrinking sideways triangle accounts for ``H * (H + 1) / 2`` sites.
    """

    horizon = _checked_nonnegative(horizon, name="horizon")
    return horizon * horizon + horizon * (horizon + 1) // 2


def _pack_time_bits(bits: Sequence[int]) -> int:
    packed = 0
    for time, bit in enumerate(bits):
        packed |= bit << time
    return packed


def _unpack_time_bits(packed: int, count: int) -> bytearray:
    return bytearray((packed >> time) & 1 for time in range(count))


def _right_neighbor_packed(center: bytes, horizon: int) -> int:
    """Return packed ``x_1(0), ..., x_1(H)`` for a checked center trace.

    Spatial bit ``j - 1`` of ``right_row`` stores ``x_j(t)`` for ``j >= 1``.
    At each update, the supplied center bit is the left boundary and the
    initial right half-line is all zero.  Width ``H`` contains the complete
    causal cone needed through time ``H``.
    """

    if horizon == 0:
        return 0
    spatial_mask = (1 << horizon) - 1
    right_row = 0
    neighbor_trace = 0  # x_1(0) = 0
    for time in range(horizon):
        left_inputs = (right_row << 1) | center[time]
        center_or_right = right_row | (right_row >> 1)
        right_row = (left_inputs ^ center_or_right) & spatial_mask
        neighbor_trace |= (right_row & 1) << (time + 1)
    return neighbor_trace


def right_neighbor_trace(
    center: Sequence[int] | Iterable[int],
    *,
    limits: SidewaysLimits = DEFAULT_LIMITS,
) -> bytearray:
    """Return ``x_1(0), ..., x_1(H)`` forced by ``c_0, ..., c_H``.

    The initial conditions are ``x_j(0) = 0`` for every ``j > 0``.  The
    returned trace has the same length as ``center``.
    """

    checked = _checked_bits(center, name="center", allow_empty=False)
    horizon = _checked_horizon(checked, limits)
    return _unpack_time_bits(_right_neighbor_packed(checked, horizon), horizon + 1)


def _reconstruct_checked(center: bytes, horizon: int) -> bytearray:
    current = _pack_time_bits(center)
    right_neighbor = _right_neighbor_packed(center, horizon)
    initial_left = bytearray(horizon)

    for depth in range(1, horizon + 1):
        new_length = horizon + 1 - depth
        new_mask = (1 << new_length) - 1
        previous_current = current
        # At time t, x_{j-1}(t) = x_j(t+1) XOR
        #                            (x_j(t) OR x_{j+1}(t)).
        current = (
            (previous_current >> 1) ^ (previous_current | right_neighbor)
        ) & new_mask
        initial_left[depth - 1] = current & 1
        right_neighbor = previous_current & new_mask

    return initial_left


def reconstruct_left_initial(
    center: Sequence[int] | Iterable[int],
    *,
    limits: SidewaysLimits = DEFAULT_LIMITS,
) -> bytearray:
    """Reconstruct ``x_{-1}(0), ..., x_{-H}(0)`` from ``c_0, ..., c_H``.

    The result has exactly ``H`` bits.  A one-bit input is the horizon-zero
    trace and returns an empty initial-left prefix.  An empty input is rejected
    because it does not contain the required ``c_0`` convention.
    """

    checked = _checked_bits(center, name="center", allow_empty=False)
    horizon = _checked_horizon(checked, limits)
    return _reconstruct_checked(checked, horizon)


def _first_nonzero_checked(center: bytes, horizon: int) -> int | None:
    current = _pack_time_bits(center)
    right_neighbor = _right_neighbor_packed(center, horizon)
    for depth in range(1, horizon + 1):
        new_length = horizon + 1 - depth
        new_mask = (1 << new_length) - 1
        previous_current = current
        current = (
            (previous_current >> 1) ^ (previous_current | right_neighbor)
        ) & new_mask
        if current & 1:
            return depth
        right_neighbor = previous_current & new_mask
    return None


def first_nonzero_left_depth(
    center: Sequence[int] | Iterable[int],
    *,
    limits: SidewaysLimits = DEFAULT_LIMITS,
) -> int | None:
    """Return the first 1-based left depth containing a reconstructed one.

    ``None`` means all ``H`` reconstructed bits are zero.  It does not make a
    statement about any depth beyond the supplied finite horizon.
    """

    checked = _checked_bits(center, name="center", allow_empty=False)
    horizon = _checked_horizon(checked, limits)
    return _first_nonzero_checked(checked, horizon)


def periodic_trace(
    period: Sequence[int] | Iterable[int],
    horizon: int,
) -> bytearray:
    """Return exactly ``c_0, ..., c_H`` by repeating a nonempty word."""

    checked_period = _checked_bits(period, name="period", allow_empty=False)
    horizon = _checked_nonnegative(horizon, name="horizon")
    return bytearray(
        checked_period[time % len(checked_period)] for time in range(horizon + 1)
    )


def eventually_periodic_trace(
    preperiod: Sequence[int] | Iterable[int],
    period: Sequence[int] | Iterable[int],
    horizon: int,
) -> bytearray:
    """Return ``c_0, ..., c_H`` for an arbitrary preperiod and period.

    If the preperiod has length ``m``, its entries occupy times ``0`` through
    ``m-1``.  The nonempty period starts at time ``m`` with phase zero.
    """

    checked_preperiod = _checked_bits(
        preperiod, name="preperiod", allow_empty=True
    )
    checked_period = _checked_bits(period, name="period", allow_empty=False)
    horizon = _checked_nonnegative(horizon, name="horizon")
    preperiod_length = len(checked_preperiod)
    return bytearray(
        checked_preperiod[time]
        if time < preperiod_length
        else checked_period[(time - preperiod_length) % len(checked_period)]
        for time in range(horizon + 1)
    )


def word_from_index(index: int, width: int) -> bytes:
    """Return a fixed-width binary word in most-significant-bit-first order."""

    width = _checked_nonnegative(width, name="width")
    index = _checked_nonnegative(index, name="index")
    if index >= (1 << width):
        raise ValueError(f"index {index} does not fit in width {width}")
    return bytes((index >> (width - position - 1)) & 1 for position in range(width))


def _word_text(word: bytes) -> str:
    return "".join(str(bit) for bit in word)


def _primitive_root(word: bytes) -> bytes:
    for width in range(1, len(word) + 1):
        if len(word) % width == 0 and word == word[:width] * (len(word) // width):
            return word[:width]
    raise AssertionError("every nonempty word has itself as a primitive root")


def _bounded_power_of_two(exponent: int, bound: int, *, description: str) -> int:
    exponent = _checked_nonnegative(exponent, name="exponent")
    if bound < 1 or exponent >= bound.bit_length():
        raise SidewaysResourceLimitError(
            f"{description} exceeds configured candidate/state bound {bound}"
        )
    return 1 << exponent


def _check_search_budget(
    candidate_count: int,
    horizon: int,
    limits: SidewaysLimits,
) -> None:
    if candidate_count > limits.max_candidates:
        raise SidewaysResourceLimitError(
            f"candidate count {candidate_count} exceeds configured maximum "
            f"{limits.max_candidates}"
        )
    work = candidate_count * logical_reconstruction_work(horizon)
    if work > limits.max_logical_cell_updates:
        raise SidewaysResourceLimitError(
            f"worst-case logical search work {work} exceeds configured maximum "
            f"{limits.max_logical_cell_updates}"
        )


def _append_unsigned_varint(output: bytearray, value: int) -> None:
    while value >= 0x80:
        output.append((value & 0x7F) | 0x80)
        value >>= 7
    output.append(value)


def _certificate(
    *,
    search_kind: str,
    horizon: int,
    candidate_order: str,
    outcomes: bytes,
    candidate_count: int,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "search_kind": search_kind,
        "horizon": horizon,
        "candidate_order": candidate_order,
        "candidate_count": candidate_count,
        "outcome_semantics": (
            "unsigned value 0 means no reconstructed one at depths 1..H; "
            "value d>=1 is the first reconstructed nonzero depth"
        ),
        "encoding": "unsigned-varint-base64",
        "payload_bytes": len(outcomes),
        "payload_sha256": hashlib.sha256(outcomes).hexdigest(),
        "payload_base64": base64.b64encode(outcomes).decode("ascii"),
    }


def decode_certificate_outcomes(certificate: Mapping[str, Any]) -> tuple[int, ...]:
    """Decode and integrity-check a certificate's first-failure outcomes."""

    if certificate.get("encoding") != "unsigned-varint-base64":
        raise ValueError("unsupported certificate encoding")
    try:
        payload = base64.b64decode(certificate["payload_base64"], validate=True)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("invalid certificate payload") from exc
    if len(payload) != certificate.get("payload_bytes"):
        raise ValueError("certificate payload length mismatch")
    if hashlib.sha256(payload).hexdigest() != certificate.get("payload_sha256"):
        raise ValueError("certificate payload hash mismatch")

    values: list[int] = []
    value = 0
    shift = 0
    for byte in payload:
        value |= (byte & 0x7F) << shift
        if byte & 0x80:
            shift += 7
            if shift > 63:
                raise ValueError("certificate varint is too long")
        else:
            values.append(value)
            value = 0
            shift = 0
    if shift:
        raise ValueError("certificate ends with an incomplete varint")
    if len(values) != certificate.get("candidate_count"):
        raise ValueError("certificate outcome count mismatch")
    return tuple(values)


def _record_outcome(
    encoded_outcomes: bytearray,
    failure_depth: int | None,
    limits: SidewaysLimits,
) -> None:
    _append_unsigned_varint(
        encoded_outcomes, 0 if failure_depth is None else failure_depth
    )
    if len(encoded_outcomes) > limits.max_certificate_bytes:
        raise SidewaysResourceLimitError(
            f"certificate exceeds configured maximum {limits.max_certificate_bytes} bytes"
        )


def search_pure_periods(
    max_period: int,
    horizon: int,
    *,
    limits: SidewaysLimits = DEFAULT_LIMITS,
) -> dict[str, Any]:
    """Exhaust every binary period-word description of lengths ``1..P``.

    Descriptions are not deduplicated: for example, ``0`` and ``00`` are both
    tested, while their common primitive root records that they induce the same
    infinite trace.  Candidate order is period length first, then unsigned word
    value in most-significant-bit-first representation.
    """

    max_period = _checked_positive(max_period, name="max_period")
    horizon = _checked_nonnegative(horizon, name="horizon")
    if horizon > limits.max_horizon:
        raise SidewaysResourceLimitError(
            f"horizon {horizon} exceeds configured maximum {limits.max_horizon}"
        )
    if horizon + 1 < max_period:
        raise ValueError(
            "horizon must expose every bit of the longest period description"
        )

    counts_by_period: list[int] = []
    candidate_count = 0
    for period_length in range(1, max_period + 1):
        count = _bounded_power_of_two(
            period_length,
            limits.max_candidates - candidate_count,
            description=f"period length {period_length}",
        )
        counts_by_period.append(count)
        candidate_count += count
    _check_search_budget(candidate_count, horizon, limits)

    encoded_outcomes = bytearray()
    per_period: list[dict[str, Any]] = []
    survivor_descriptions: list[dict[str, Any]] = []
    survivor_primitive_roots: set[bytes] = set()
    survivor_count = 0
    single_seed_survivor_count = 0
    nonzero_trace_survivor_count = 0
    first_nonzero_survivor: dict[str, Any] | None = None

    for period_length, period_count in enumerate(counts_by_period, start=1):
        failure_histogram: Counter[int] = Counter()
        period_survivors = 0
        period_seed_survivors = 0
        for word_index in range(period_count):
            word = word_from_index(word_index, period_length)
            center = bytes(periodic_trace(word, horizon))
            failure_depth = _first_nonzero_checked(center, horizon)
            _record_outcome(encoded_outcomes, failure_depth, limits)
            if failure_depth is None:
                period_survivors += 1
                survivor_count += 1
                root = _primitive_root(word)
                survivor_primitive_roots.add(root)
                descriptor = {
                    "period_length": period_length,
                    "word_index": word_index,
                    "word": _word_text(word),
                    "primitive_root": _word_text(root),
                }
                if len(survivor_descriptions) < limits.max_reported_survivors:
                    survivor_descriptions.append(descriptor)
                if center[0] == 1:
                    period_seed_survivors += 1
                    single_seed_survivor_count += 1
                if any(word):
                    nonzero_trace_survivor_count += 1
                    if first_nonzero_survivor is None:
                        first_nonzero_survivor = descriptor
            else:
                failure_histogram[failure_depth] += 1

        per_period.append(
            {
                "period_length": period_length,
                "candidate_descriptions": period_count,
                "zero_left_survivor_descriptions": period_survivors,
                "single_seed_survivor_descriptions": period_seed_survivors,
                "first_nonzero_depth_histogram": {
                    str(depth): failure_histogram[depth]
                    for depth in sorted(failure_histogram)
                },
                "maximum_first_nonzero_depth": (
                    max(failure_histogram) if failure_histogram else None
                ),
            }
        )

    certificate = _certificate(
        search_kind="pure-period",
        horizon=horizon,
        candidate_order=(
            "period_length=1..max_period; within each length, word_index "
            "in increasing unsigned order; fixed-width word is MSB-first"
        ),
        outcomes=bytes(encoded_outcomes),
        candidate_count=candidate_count,
    )
    return {
        "status": "finite-exhaustive",
        "parameters": {"max_period": max_period, "horizon": horizon},
        "candidate_descriptions": candidate_count,
        "zero_left_survivor_descriptions": survivor_count,
        "distinct_survivor_periodic_sequences": len(survivor_primitive_roots),
        "survivor_primitive_roots": sorted(
            _word_text(root) for root in survivor_primitive_roots
        ),
        "single_seed_survivor_descriptions": single_seed_survivor_count,
        "nonzero_trace_survivor_descriptions": nonzero_trace_survivor_count,
        "only_constant_zero_trace_survives": (
            survivor_count > 0 and nonzero_trace_survivor_count == 0
        ),
        "first_counterexample_to_only_constant_zero": first_nonzero_survivor,
        "survivor_descriptions": survivor_descriptions,
        "survivor_descriptions_truncated": (
            survivor_count > len(survivor_descriptions)
        ),
        "per_period": per_period,
        "certificate": certificate,
        "interpretation": (
            "Every listed period-word description was checked exactly through "
            "the stated finite horizon. No conclusion beyond that horizon follows."
        ),
    }


def search_eventually_periodic(
    max_preperiod: int,
    max_period: int,
    horizon: int,
    *,
    limits: SidewaysLimits = DEFAULT_LIMITS,
) -> dict[str, Any]:
    """Exhaust preperiod lengths ``0..M`` and period lengths ``1..P``.

    Each binary prefix and each nonempty binary period word is enumerated.
    Equivalent descriptions are intentionally retained, so all counts are
    counts of descriptions rather than equivalence classes.
    """

    max_preperiod = _checked_nonnegative(max_preperiod, name="max_preperiod")
    max_period = _checked_positive(max_period, name="max_period")
    horizon = _checked_nonnegative(horizon, name="horizon")
    if horizon > limits.max_horizon:
        raise SidewaysResourceLimitError(
            f"horizon {horizon} exceeds configured maximum {limits.max_horizon}"
        )
    if horizon + 1 < max_preperiod + max_period:
        raise ValueError(
            "horizon must expose every bit of the longest preperiod+period description"
        )

    block_counts: list[tuple[int, int, int]] = []
    candidate_count = 0
    for preperiod_length in range(max_preperiod + 1):
        for period_length in range(1, max_period + 1):
            remaining = limits.max_candidates - candidate_count
            count = _bounded_power_of_two(
                preperiod_length + period_length,
                remaining,
                description=(
                    f"preperiod {preperiod_length}, period {period_length} block"
                ),
            )
            block_counts.append((preperiod_length, period_length, count))
            candidate_count += count
    _check_search_budget(candidate_count, horizon, limits)

    encoded_outcomes = bytearray()
    per_shape: list[dict[str, Any]] = []
    survivor_descriptions: list[dict[str, Any]] = []
    survivor_count = 0
    all_zero_survivor_count = 0
    single_seed_survivor_count = 0
    first_nonzero_survivor: dict[str, Any] | None = None

    for preperiod_length, period_length, shape_count in block_counts:
        prefix_count = 1 << preperiod_length
        period_count = 1 << period_length
        shape_survivors = 0
        shape_seed_survivors = 0
        shape_all_zero_survivors = 0
        failure_histogram: Counter[int] = Counter()
        for prefix_index in range(prefix_count):
            preperiod = word_from_index(prefix_index, preperiod_length)
            for period_index in range(period_count):
                period = word_from_index(period_index, period_length)
                center = bytes(
                    eventually_periodic_trace(preperiod, period, horizon)
                )
                failure_depth = _first_nonzero_checked(center, horizon)
                _record_outcome(encoded_outcomes, failure_depth, limits)
                if failure_depth is None:
                    shape_survivors += 1
                    survivor_count += 1
                    all_zero_description = not any(preperiod) and not any(period)
                    if all_zero_description:
                        shape_all_zero_survivors += 1
                        all_zero_survivor_count += 1
                    descriptor = {
                        "preperiod_length": preperiod_length,
                        "period_length": period_length,
                        "preperiod_index": prefix_index,
                        "period_index": period_index,
                        "preperiod": _word_text(preperiod),
                        "period": _word_text(period),
                    }
                    if len(survivor_descriptions) < limits.max_reported_survivors:
                        survivor_descriptions.append(descriptor)
                    if center[0] == 1:
                        shape_seed_survivors += 1
                        single_seed_survivor_count += 1
                    if not all_zero_description and first_nonzero_survivor is None:
                        first_nonzero_survivor = descriptor
                else:
                    failure_histogram[failure_depth] += 1

        if shape_count != prefix_count * period_count:
            raise AssertionError("candidate accounting mismatch")
        per_shape.append(
            {
                "preperiod_length": preperiod_length,
                "period_length": period_length,
                "candidate_descriptions": shape_count,
                "zero_left_survivor_descriptions": shape_survivors,
                "all_zero_trace_survivor_descriptions": shape_all_zero_survivors,
                "single_seed_survivor_descriptions": shape_seed_survivors,
                "first_nonzero_depth_histogram": {
                    str(depth): failure_histogram[depth]
                    for depth in sorted(failure_histogram)
                },
                "maximum_first_nonzero_depth": (
                    max(failure_histogram) if failure_histogram else None
                ),
            }
        )

    certificate = _certificate(
        search_kind="preperiod-plus-period",
        horizon=horizon,
        candidate_order=(
            "preperiod_length=0..max_preperiod; period_length=1..max_period; "
            "prefix_index increasing; period_index increasing; fixed-width words "
            "are MSB-first"
        ),
        outcomes=bytes(encoded_outcomes),
        candidate_count=candidate_count,
    )
    return {
        "status": "finite-exhaustive",
        "parameters": {
            "max_preperiod": max_preperiod,
            "max_period": max_period,
            "horizon": horizon,
        },
        "candidate_descriptions": candidate_count,
        "zero_left_survivor_descriptions": survivor_count,
        "all_zero_trace_survivor_descriptions": all_zero_survivor_count,
        "single_seed_survivor_descriptions": single_seed_survivor_count,
        "only_all_zero_descriptions_survive": (
            survivor_count > 0 and survivor_count == all_zero_survivor_count
        ),
        "first_counterexample_to_only_all_zero": first_nonzero_survivor,
        "survivor_descriptions": survivor_descriptions,
        "survivor_descriptions_truncated": (
            survivor_count > len(survivor_descriptions)
        ),
        "per_shape": per_shape,
        "certificate": certificate,
        "interpretation": (
            "Every description in the stated finite preperiod/period box was "
            "checked through the stated horizon. Unbounded preperiods, periods, "
            "and reconstruction depths remain untreated."
        ),
    }


def truncated_right_transition(state: int, boundary_bit: int, width: int) -> int:
    """Advance an explicitly width-truncated right half by one Rule 30 step.

    Spatial bit ``j - 1`` stores site ``j`` for ``1 <= j <= width``.  The
    outer site ``width + 1`` is fixed to zero at every step.  This is a finite
    model, not the full semi-infinite right half for arbitrarily long times.
    """

    width = _checked_positive(width, name="width")
    if not isinstance(state, int) or isinstance(state, bool) or state < 0:
        raise ValueError("state must be a nonnegative integer")
    state_count = 1 << width
    if state >= state_count:
        raise ValueError(f"state does not fit in width {width}")
    checked_boundary = _checked_bits(
        (boundary_bit,), name="boundary", allow_empty=False
    )[0]
    mask = state_count - 1
    return (
        ((state << 1) | checked_boundary) ^ (state | (state >> 1))
    ) & mask


def truncated_periodic_state_graph(
    period: Sequence[int] | Iterable[int],
    width: int,
    *,
    limits: SidewaysLimits = DEFAULT_LIMITS,
) -> dict[str, Any]:
    """Summarize the exact finite functional graph for fixed ``period,width``.

    A node is ``(phase, right_state)``.  There are exactly
    ``len(period) * 2**width`` nodes.  This bound grows exponentially with
    width; the function makes no claim that a depth-independent finite state
    space suffices for the original semi-infinite reconstruction problem.
    """

    checked_period = _checked_bits(period, name="period", allow_empty=False)
    width = _checked_positive(width, name="width")
    states_per_phase = _bounded_power_of_two(
        width,
        limits.max_graph_states,
        description=f"width {width} state space",
    )
    node_count = len(checked_period) * states_per_phase
    if node_count > limits.max_graph_states:
        raise SidewaysResourceLimitError(
            f"graph has {node_count} nodes, exceeding configured maximum "
            f"{limits.max_graph_states}"
        )

    successors = [0] * node_count
    indegrees = [0] * node_count
    digest = hashlib.sha256()
    state_bytes = max(1, (width + 7) // 8)
    phase_bytes = max(1, (len(checked_period).bit_length() + 7) // 8)

    for phase, boundary in enumerate(checked_period):
        next_phase = (phase + 1) % len(checked_period)
        for state in range(states_per_phase):
            node = phase * states_per_phase + state
            next_state = truncated_right_transition(state, boundary, width)
            successor = next_phase * states_per_phase + next_state
            successors[node] = successor
            indegrees[successor] += 1
            digest.update(phase.to_bytes(phase_bytes, "little"))
            digest.update(state.to_bytes(state_bytes, "little"))
            digest.update(next_phase.to_bytes(phase_bytes, "little"))
            digest.update(next_state.to_bytes(state_bytes, "little"))

    remaining_indegrees = indegrees.copy()
    queue = deque(index for index, degree in enumerate(remaining_indegrees) if degree == 0)
    while queue:
        node = queue.popleft()
        successor = successors[node]
        remaining_indegrees[successor] -= 1
        if remaining_indegrees[successor] == 0:
            queue.append(successor)

    cycle_lengths: list[int] = []
    visited_cycle_nodes: set[int] = set()
    for node, degree in enumerate(remaining_indegrees):
        if degree == 0 or node in visited_cycle_nodes:
            continue
        length = 0
        current = node
        while current not in visited_cycle_nodes:
            visited_cycle_nodes.add(current)
            length += 1
            current = successors[current]
        cycle_lengths.append(length)

    orbit_seen: dict[int, int] = {}
    orbit_node = 0  # phase zero, all-zero right state
    step = 0
    while orbit_node not in orbit_seen:
        orbit_seen[orbit_node] = step
        orbit_node = successors[orbit_node]
        step += 1
    transient_length = orbit_seen[orbit_node]

    return {
        "model": "fixed-width periodically driven right-half functional graph",
        "period": _word_text(checked_period),
        "period_length": len(checked_period),
        "width": width,
        "node_bound_formula": "period_length * 2**width",
        "node_count": node_count,
        "edge_count": node_count,
        "transition_sha256": digest.hexdigest(),
        "indegree_histogram": {
            str(degree): count
            for degree, count in sorted(Counter(indegrees).items())
        },
        "cycle_count": len(cycle_lengths),
        "cycle_length_histogram": {
            str(length): count
            for length, count in sorted(Counter(cycle_lengths).items())
        },
        "zero_initial_orbit": {
            "transient_length": transient_length,
            "cycle_length": step - transient_length,
            "visited_nodes_before_repeat": step,
        },
        "scope": (
            "exact for this fixed-width system with a permanently zero outer "
            "boundary; width must grow with the finite causal depth used to "
            "represent the semi-infinite zero right half"
        ),
    }
