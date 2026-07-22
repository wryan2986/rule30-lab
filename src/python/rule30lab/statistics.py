"""Validated descriptive statistics for finite binary prefixes.

Nothing in this module interprets a finite measurement as evidence of a
limiting distribution, randomness, normality, or any infinite mathematical
claim.  Functions return exact integer numerators wherever practical and make
floating-point normalizations explicit.
"""

from __future__ import annotations

import math
import operator
from collections import Counter
from collections.abc import Iterable, Sequence
from typing import Any


def _integer(value: int, *, name: str, minimum: int | None = None) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer, not bool")
    try:
        result = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if minimum is not None and result < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return result


def _validated_bits(bits: Iterable[int]) -> bytes:
    """Copy an iterable into an immutable, checked one-byte-per-bit prefix."""
    output = bytearray()
    for position, value in enumerate(bits):
        try:
            bit = operator.index(value)
        except TypeError as exc:
            raise ValueError(f"bit at index {position} is not an integer") from exc
        if bit not in (0, 1):
            raise ValueError(f"bit at index {position} must be 0 or 1, got {value!r}")
        output.append(bit)
    return bytes(output)


def discrepancy(bits: Iterable[int]) -> int:
    """Return ``D(N) = sum(2*c_t - 1)`` for the supplied finite prefix."""
    data = _validated_bits(bits)
    return 2 * sum(data) - len(data)


def balance_checkpoints(
    bits: Iterable[int], checkpoints: Iterable[int]
) -> list[dict[str, int | float | None]]:
    """Return exact balance data at sorted, unique prefix lengths.

    A checkpoint of zero is accepted.  Ratios whose denominator would be zero
    are represented by ``None`` so the result remains strict JSON data (with no
    NaN or infinity values).  A checkpoint beyond the supplied prefix is an
    error rather than a silently shortened computation.
    """
    data = _validated_bits(bits)
    requested = sorted(
        {
            _integer(checkpoint, name="checkpoint", minimum=0)
            for checkpoint in checkpoints
        }
    )
    if requested and requested[-1] > len(data):
        raise ValueError(
            f"checkpoint {requested[-1]} exceeds prefix length {len(data)}"
        )

    results: list[dict[str, int | float | None]] = []
    previous = 0
    ones = 0
    for count in requested:
        ones += sum(data[previous:count])
        zeros = count - ones
        signed = ones - zeros
        results.append(
            {
                "n": count,
                "ones": ones,
                "zeros": zeros,
                "discrepancy": signed,
                "ones_fraction": None if count == 0 else ones / count,
                "discrepancy_over_sqrt_n": (
                    None if count == 0 else signed / math.sqrt(count)
                ),
                "discrepancy_over_n": None if count == 0 else signed / count,
            }
        )
        previous = count
    return results


def max_absolute_prefix_discrepancy(bits: Iterable[int]) -> dict[str, int]:
    """Return the first prefix attaining the largest ``abs(D(N))``.

    The empty prefix ``N=0`` is included, so an empty input has a well-defined
    result with discrepancy zero at ``N=0``.
    """
    data = _validated_bits(bits)
    signed = 0
    best_signed = 0
    best_n = 0
    best_absolute = 0
    for count, bit in enumerate(data, start=1):
        signed += 1 if bit else -1
        absolute = abs(signed)
        if absolute > best_absolute:
            best_absolute = absolute
            best_signed = signed
            best_n = count
    return {
        "n": best_n,
        "discrepancy": best_signed,
        "absolute_discrepancy": best_absolute,
    }


def _dyadic_widths(
    length: int, widths: Iterable[int] | None
) -> tuple[int, ...]:
    if widths is None:
        result: list[int] = []
        width = 1
        while width <= length:
            result.append(width)
            width <<= 1
        return tuple(result)

    checked = sorted(
        {
            _integer(width, name="dyadic width", minimum=1)
            for width in widths
        }
    )
    for width in checked:
        if width & (width - 1):
            raise ValueError(f"dyadic width {width} is not a power of two")
        if width > length:
            raise ValueError(
                f"dyadic width {width} exceeds prefix length {length}"
            )
    return tuple(checked)


def _spin_prefix_sums(data: Sequence[int]) -> list[int]:
    sums = [0] * (len(data) + 1)
    running = 0
    for index, bit in enumerate(data, start=1):
        running += 1 if bit else -1
        sums[index] = running
    return sums


def dyadic_interval_discrepancies(
    bits: Iterable[int],
    *,
    widths: Iterable[int] | None = None,
    include_partial: bool = False,
    max_intervals: int = 1_000_000,
) -> list[dict[str, int | bool]]:
    """Measure discrepancy on aligned intervals of power-of-two width.

    For width ``w``, intervals are ``[k*w, (k+1)*w)``.  An incomplete final
    interval is omitted unless ``include_partial`` is true.  ``max_intervals``
    is checked before allocating the result list and is an explicit cap on its
    number of records.
    """
    data = _validated_bits(bits)
    selected = _dyadic_widths(len(data), widths)
    interval_limit = _integer(max_intervals, name="max_intervals", minimum=1)
    interval_count = sum(
        (
            (len(data) + width - 1) // width
            if include_partial
            else len(data) // width
        )
        for width in selected
    )
    if interval_count > interval_limit:
        raise MemoryError(
            f"dyadic result needs {interval_count} records, exceeding "
            f"max_intervals={interval_limit}"
        )

    prefix = _spin_prefix_sums(data)
    output: list[dict[str, int | bool]] = []
    for width in selected:
        for start in range(0, len(data), width):
            stop = min(start + width, len(data))
            if stop - start < width and not include_partial:
                break
            output.append(
                {
                    "width": width,
                    "start": start,
                    "stop": stop,
                    "length": stop - start,
                    "discrepancy": prefix[stop] - prefix[start],
                    "partial": stop - start < width,
                }
            )
    return output


def dyadic_discrepancy_summary(
    bits: Iterable[int],
    *,
    widths: Iterable[int] | None = None,
    include_partial: bool = False,
) -> list[dict[str, int | bool]]:
    """Return one exact aggregate record per dyadic interval width."""
    data = _validated_bits(bits)
    selected = _dyadic_widths(len(data), widths)
    prefix = _spin_prefix_sums(data)
    summaries: list[dict[str, int | bool]] = []

    for width in selected:
        values: list[tuple[int, int, int]] = []
        for start in range(0, len(data), width):
            stop = min(start + width, len(data))
            if stop - start < width and not include_partial:
                break
            values.append((prefix[stop] - prefix[start], start, stop))

        maximum_absolute, maximum_record = max(
            ((abs(value[0]), value) for value in values),
            key=lambda item: item[0],
        )
        discrepancy_value, maximum_start, maximum_stop = maximum_record
        summaries.append(
            {
                "width": width,
                "interval_count": len(values),
                "include_partial": include_partial,
                "minimum_discrepancy": min(value[0] for value in values),
                "maximum_discrepancy": max(value[0] for value in values),
                "maximum_absolute_discrepancy": maximum_absolute,
                "first_maximum_start": maximum_start,
                "first_maximum_stop": maximum_stop,
                "first_maximum_discrepancy": discrepancy_value,
                "sum_of_interval_discrepancies": sum(value[0] for value in values),
            }
        )
    return summaries


def block_frequencies(
    bits: Iterable[int],
    width: int,
    *,
    include_zero_counts: bool = False,
    max_table_entries: int = 1_048_576,
    max_width: int = 64,
) -> dict[str, Any]:
    """Count overlapping binary blocks under explicit table and width caps.

    Integer block keys use most-significant-bit-first input order.  Sparse mode
    (the default) stores observed blocks only.  Dense mode includes zero counts
    and is allowed only when all ``2**width`` entries fit under
    ``max_table_entries``.  The entry cap bounds mapping cardinality rather than
    exact Python object bytes, which vary by interpreter.
    """
    data = _validated_bits(bits)
    block_width = _integer(width, name="width", minimum=1)
    width_limit = _integer(max_width, name="max_width", minimum=1)
    entry_limit = _integer(
        max_table_entries, name="max_table_entries", minimum=1
    )
    if block_width > width_limit:
        raise MemoryError(
            f"width {block_width} exceeds explicit max_width={width_limit}"
        )
    if block_width > len(data):
        raise ValueError(
            f"width {block_width} exceeds prefix length {len(data)}"
        )

    window_count = len(data) - block_width + 1
    possible_count = 1 << block_width
    maximum_entries = (
        possible_count
        if include_zero_counts
        else min(possible_count, window_count)
    )
    if maximum_entries > entry_limit:
        raise MemoryError(
            f"block table may need {maximum_entries} entries, exceeding "
            f"max_table_entries={entry_limit}"
        )

    value = 0
    for bit in data[:block_width]:
        value = (value << 1) | bit
    counts: Counter[int] = Counter((value,))
    mask = possible_count - 1
    for bit in data[block_width:]:
        value = ((value << 1) & mask) | bit
        counts[value] += 1

    if include_zero_counts:
        for candidate in range(possible_count):
            counts[candidate] += 0

    return {
        "width": block_width,
        "window_count": window_count,
        "possible_block_count": possible_count,
        "observed_block_count": sum(count > 0 for count in counts.values()),
        "include_zero_counts": include_zero_counts,
        "max_table_entries": entry_limit,
        "max_width": width_limit,
        "key_convention": "integer_value_most_significant_bit_first",
        "counts": dict(sorted(counts.items())),
    }


def spin_autocorrelation(bits: Iterable[int], lag: int) -> dict[str, int | float | str]:
    """Return the uncentered spin-product mean at one lag.

    Bits are mapped to spins by ``s_t = 2*c_t - 1``.  The exact numerator is
    ``sum(s_t*s_(t+lag))`` and the exact denominator is ``N-lag``.  This is not
    a mean-centered Pearson correlation coefficient.
    """
    data = _validated_bits(bits)
    checked_lag = _integer(lag, name="lag", minimum=0)
    if checked_lag >= len(data):
        raise ValueError(
            f"lag {checked_lag} must be smaller than prefix length {len(data)}"
        )

    denominator = len(data) - checked_lag
    numerator = sum(
        (1 if data[index] else -1)
        * (1 if data[index + checked_lag] else -1)
        for index in range(denominator)
    )
    return {
        "lag": checked_lag,
        "numerator": numerator,
        "denominator": denominator,
        "value": numerator / denominator,
        "normalization": "uncentered_mean_spin_product",
    }


def run_lengths(bits: Iterable[int]) -> tuple[tuple[int, int], ...]:
    """Return ``(bit, length)`` pairs for maximal constant runs."""
    data = _validated_bits(bits)
    if not data:
        return ()

    output: list[tuple[int, int]] = []
    current = data[0]
    length = 1
    for bit in data[1:]:
        if bit == current:
            length += 1
        else:
            output.append((current, length))
            current = bit
            length = 1
    output.append((current, length))
    return tuple(output)


def run_statistics(bits: Iterable[int]) -> dict[str, Any]:
    """Summarize maximal constant runs in a finite binary prefix."""
    data = _validated_bits(bits)
    runs = run_lengths(data)
    histogram = Counter(length for _, length in runs)
    zero_lengths = [length for bit, length in runs if bit == 0]
    one_lengths = [length for bit, length in runs if bit == 1]
    return {
        "sample_count": len(data),
        "run_count": len(runs),
        "zero_run_count": len(zero_lengths),
        "one_run_count": len(one_lengths),
        "longest_run": max(histogram, default=0),
        "longest_zero_run": max(zero_lengths, default=0),
        "longest_one_run": max(one_lengths, default=0),
        "mean_run_length": None if not runs else len(data) / len(runs),
        "first_bit": None if not data else data[0],
        "last_bit": None if not data else data[-1],
        "length_histogram": dict(sorted(histogram.items())),
    }


def _block_phi(counts: dict[int, int], window_count: int, base: float) -> float:
    return sum(
        (count / window_count) * (math.log(count / window_count) / math.log(base))
        for count in counts.values()
        if count
    )


def approximate_entropy(
    bits: Iterable[int],
    pattern_length: int,
    *,
    base: float = 2.0,
    max_table_entries: int = 1_048_576,
    max_width: int = 64,
) -> dict[str, Any]:
    """Return the exact-match symbolic finite-prefix ApEn analogue.

    This computes ``phi(m) - phi(m+1)`` from overlapping empirical block
    frequencies, including self-matches.  It is a descriptive plug-in estimate
    for this one finite prefix, not a randomness test or limiting entropy claim.
    """
    data = _validated_bits(bits)
    length = _integer(pattern_length, name="pattern_length", minimum=1)
    numeric_base = float(base)
    if (
        not math.isfinite(numeric_base)
        or numeric_base <= 0.0
        or numeric_base == 1.0
    ):
        raise ValueError("base must be finite, positive, and different from 1")
    if len(data) < length + 1:
        raise ValueError(
            "prefix must contain at least pattern_length + 1 bits"
        )

    at_length = block_frequencies(
        data,
        length,
        max_table_entries=max_table_entries,
        max_width=max_width,
    )
    at_next = block_frequencies(
        data,
        length + 1,
        max_table_entries=max_table_entries,
        max_width=max_width,
    )
    phi_m = _block_phi(at_length["counts"], at_length["window_count"], numeric_base)
    phi_next = _block_phi(
        at_next["counts"], at_next["window_count"], numeric_base
    )
    return {
        "sample_count": len(data),
        "pattern_length": length,
        "base": numeric_base,
        "phi_m": phi_m,
        "phi_m_plus_1": phi_next,
        "approximate_entropy": phi_m - phi_next,
        "method": "overlapping_exact_match_symbolic_plugin_with_self_matches",
        "status": "descriptive_finite_prefix",
        "limitations": [
            "not a randomness test",
            "not an estimate with an asymptotic guarantee",
            "does not establish a limiting entropy rate",
        ],
    }


def power_spectral_summary(
    bits: Iterable[int], *, top_k: int = 8
) -> dict[str, Any]:
    """Return an optional NumPy periodogram summary of centered spins.

    The one-sided power is scaled so its sum agrees with the population
    variance of the centered spin samples (up to floating-point roundoff).
    NumPy is imported lazily; callers not using this function do not need it.
    """
    data = _validated_bits(bits)
    if len(data) < 2:
        raise ValueError("spectral analysis requires at least two bits")
    requested_top_k = _integer(top_k, name="top_k", minimum=0)
    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover - depends on optional environment
        raise RuntimeError(
            "NumPy is required for power_spectral_summary; install the analysis extra"
        ) from exc

    spins = np.fromiter(
        (1.0 if bit else -1.0 for bit in data),
        dtype=np.float64,
        count=len(data),
    )
    spin_mean = float(spins.mean())
    centered = spins - spin_mean
    transform = np.fft.rfft(centered)
    power = (np.abs(transform) ** 2) / (len(data) ** 2)
    if len(data) % 2 == 0:
        power[1:-1] *= 2.0
    else:
        power[1:] *= 2.0
    frequencies = np.fft.rfftfreq(len(data), d=1.0)

    positive_bins = list(range(1, len(power)))
    ranked = sorted(
        positive_bins,
        key=lambda index: (-float(power[index]), index),
    )[:requested_top_k]
    positive_power = [float(power[index]) for index in positive_bins]
    arithmetic_mean = (
        sum(positive_power) / len(positive_power) if positive_power else 0.0
    )
    if arithmetic_mean == 0.0:
        flatness: float | None = None
    elif any(value <= 0.0 for value in positive_power):
        flatness = 0.0
    else:
        flatness = math.exp(
            sum(math.log(value) for value in positive_power) / len(positive_power)
        ) / arithmetic_mean

    return {
        "sample_count": len(data),
        "spin_mean": spin_mean,
        "spin_variance": float(np.mean(centered**2)),
        "one_sided_power_sum": float(power.sum()),
        "spectral_flatness_positive_bins": flatness,
        "top_bins": [
            {
                "bin": index,
                "cycles_per_sample": float(frequencies[index]),
                "power": float(power[index]),
            }
            for index in ranked
        ],
        "normalization": "mean_centered_spin_one_sided_parseval",
        "status": "descriptive_finite_prefix",
        "limitations": [
            "periodogram ordinates are finite-sample descriptive measurements",
            "no randomness, mixing, or asymptotic spectral claim is implied",
        ],
    }


def _berlekamp_massey_state(bits: Iterable[int]) -> tuple[int, tuple[int, ...]]:
    data = _validated_bits(bits)
    count = len(data)
    if count == 0:
        return 0, (1,)

    connection = [0] * (count + 1)
    previous = [0] * (count + 1)
    connection[0] = previous[0] = 1
    complexity = 0
    shift = 1

    for index in range(count):
        delta = data[index]
        for offset in range(1, complexity + 1):
            delta ^= connection[offset] & data[index - offset]

        if delta == 0:
            shift += 1
            continue

        saved = connection.copy()
        for offset in range(count + 1 - shift):
            connection[offset + shift] ^= previous[offset]

        if 2 * complexity <= index:
            complexity = index + 1 - complexity
            previous = saved
            shift = 1
        else:
            shift += 1

    return complexity, tuple(connection[: complexity + 1])


def berlekamp_massey_binary(bits: Iterable[int]) -> int:
    """Return finite-prefix GF(2) linear complexity; the empty value is zero."""
    complexity, _ = _berlekamp_massey_state(bits)
    return complexity


def berlekamp_massey_connection_polynomial(
    bits: Iterable[int],
) -> tuple[int, ...]:
    """Return ``(1, c_1, ..., c_L)`` for a shortest GF(2) recurrence."""
    _, polynomial = _berlekamp_massey_state(bits)
    return polynomial
