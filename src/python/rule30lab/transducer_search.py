"""Bounded affine-transducer and finite 2-kernel refinement searches.

All conclusions produced here have explicitly finite scope.  A failed bounded
search does not prove nonautomaticity, rule out another exact representation,
or establish any computational lower bound for the Rule 30 center sequence.
"""

from __future__ import annotations

import hashlib
import operator
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any


def _integer(value: int, *, name: str, minimum: int = 0) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer, not bool")
    try:
        checked = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if checked < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return checked


def _bits_and_split(bits: Iterable[int], train_length: int) -> tuple[bytes, int]:
    data = bytearray()
    for index, value in enumerate(bits):
        try:
            bit = operator.index(value)
        except TypeError as exc:
            raise ValueError(f"bit at index {index} is not an integer") from exc
        if bit not in (0, 1):
            raise ValueError(f"bit at index {index} must be 0 or 1")
        data.append(bit)
    checked_train = _integer(train_length, name="train_length", minimum=1)
    if checked_train >= len(data):
        raise ValueError("train_length must leave at least one held-out bit")
    return bytes(data), checked_train


def _canonical_digits(n: int, *, lsb_first: bool = False) -> tuple[int, ...]:
    checked = _integer(n, name="n")
    digits = (0,) if checked == 0 else tuple(int(ch) for ch in f"{checked:b}")
    return tuple(reversed(digits)) if lsb_first else digits


def _contract(
    *, machine_model: str, digit_order: str, preprocessing: str
) -> dict[str, Any]:
    return {
        "machine_model": machine_model,
        "index_input_convention": {
            "domain": "nonnegative integer n",
            "binary_encoding": (
                "canonical base-2 without leading zeroes; n=0 is encoded as 0"
            ),
            "digit_order": digit_order,
        },
        "output_convention": "one exact bit c_n in {0,1}",
        "preprocessing_and_advice_assumptions": preprocessing,
        "uniformity_assumption": (
            "one fixed finite candidate is applied to every queried n; a model "
            "selected from a finite prefix is not thereby a proved uniform "
            "algorithm for the infinite sequence"
        ),
        "determinism": {"randomness_used": False, "deterministic_seed": 0},
        "finite_only_status": "bounded_finite_search",
    }


@dataclass(frozen=True)
class AffineDigitModel:
    """An MSB-first affine digit-matrix product over GF(2).

    For digit ``b``, the state update is ``s <- A_b s + v_b``.  The output is
    ``output_mask . s + output_bias``.  Rows and vectors are bit packed, with
    coordinate zero in the least-significant bit.
    """

    dimension: int
    initial_state: int
    matrices: tuple[tuple[int, ...], tuple[int, ...]]
    translations: tuple[int, int]
    output_mask: int
    output_bias: int

    def __post_init__(self) -> None:
        dimension = _integer(self.dimension, name="dimension", minimum=1)
        limit = 1 << dimension
        if not 0 <= self.initial_state < limit:
            raise ValueError("initial_state is outside the state space")
        if len(self.matrices) != 2 or len(self.translations) != 2:
            raise ValueError("exactly two digit maps are required")
        for digit, rows in enumerate(self.matrices):
            if len(rows) != dimension:
                raise ValueError(f"matrix {digit} must have dimension rows")
            if any(row < 0 or row >= limit for row in rows):
                raise ValueError(f"matrix {digit} row is outside GF(2)^dimension")
        if any(vector < 0 or vector >= limit for vector in self.translations):
            raise ValueError("translation is outside the state space")
        if not 0 <= self.output_mask < limit:
            raise ValueError("output_mask is outside the dual state space")
        if self.output_bias not in (0, 1):
            raise ValueError("output_bias must be a bit")

    def as_record(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "state_count_upper_bound": 1 << self.dimension,
            "initial_state": self.initial_state,
            "matrices_row_masks": [list(rows) for rows in self.matrices],
            "translations": list(self.translations),
            "output_mask": self.output_mask,
            "output_bias": self.output_bias,
            "field": "GF(2)",
            "digit_order": "msb_first",
        }


def affine_encoding_bits(dimension: int) -> int:
    """Return the exact number of bits in the canonical labeled encoding."""
    d = _integer(dimension, name="dimension", minimum=1)
    return 2 * d * d + 4 * d + 1


def affine_model_count(dimension: int) -> int:
    """Return the number of labeled affine models of one dimension."""
    return 1 << affine_encoding_bits(dimension)


def decode_affine_model(dimension: int, model_id: int) -> AffineDigitModel:
    """Decode a deterministic little-endian field-by-field model identifier."""
    d = _integer(dimension, name="dimension", minimum=1)
    identifier = _integer(model_id, name="model_id")
    count = affine_model_count(d)
    if identifier >= count:
        raise ValueError(f"model_id must be smaller than {count}")

    code = identifier

    def take(width: int) -> int:
        nonlocal code
        value = code & ((1 << width) - 1)
        code >>= width
        return value

    initial = take(d)
    matrices: list[tuple[int, ...]] = []
    translations: list[int] = []
    for _digit in (0, 1):
        matrices.append(tuple(take(d) for _row in range(d)))
        translations.append(take(d))
    output_mask = take(d)
    output_bias = take(1)
    assert code == 0
    return AffineDigitModel(
        dimension=d,
        initial_state=initial,
        matrices=(matrices[0], matrices[1]),
        translations=(translations[0], translations[1]),
        output_mask=output_mask,
        output_bias=output_bias,
    )


def evaluate_affine_model(model: AffineDigitModel, n: int) -> int:
    """Evaluate one exact affine digit product on canonical binary ``n``."""
    state = model.initial_state
    for digit in _canonical_digits(n):
        next_state = model.translations[digit]
        for coordinate, row_mask in enumerate(model.matrices[digit]):
            next_state ^= ((row_mask & state).bit_count() & 1) << coordinate
        state = next_state
    return ((model.output_mask & state).bit_count() & 1) ^ model.output_bias


def locate_first_counterexample(
    model: AffineDigitModel,
    bits: Sequence[int],
    *,
    start: int,
    stop: int | None = None,
) -> dict[str, Any] | None:
    """Return the first finite mismatch, or ``None`` after exact comparison."""
    first = _integer(start, name="start")
    final = len(bits) if stop is None else _integer(stop, name="stop")
    if first > final or final > len(bits):
        raise ValueError("counterexample interval is outside the supplied bits")
    for index in range(first, final):
        observed = operator.index(bits[index])
        if observed not in (0, 1):
            raise ValueError(f"bit at index {index} must be 0 or 1")
        predicted = evaluate_affine_model(model, index)
        if predicted != observed:
            return {
                "index": index,
                "index_binary": f"{index:b}",
                "predicted": predicted,
                "observed": observed,
            }
    return None


def search_affine_digit_models(
    bits: Iterable[int],
    *,
    train_length: int,
    min_dimension: int = 1,
    max_dimension: int = 2,
    start_dimension: int | None = None,
    start_model_id: int = 0,
    max_models: int = 1_000_000,
    max_selected_training_fits: int = 32,
    max_dimension_cap: int = 4,
) -> dict[str, Any]:
    """Enumerate affine models using training only, then seek counterexamples.

    Enumeration order is dimension ascending, then model identifier ascending.
    Held-out bits are not accessed until enumeration and the deterministic
    first-fit selection have both completed.
    """
    data, train = _bits_and_split(bits, train_length)
    minimum = _integer(min_dimension, name="min_dimension", minimum=1)
    maximum = _integer(max_dimension, name="max_dimension", minimum=1)
    dimension_cap = _integer(
        max_dimension_cap, name="max_dimension_cap", minimum=1
    )
    first_dimension = (
        minimum
        if start_dimension is None
        else _integer(start_dimension, name="start_dimension", minimum=1)
    )
    first_identifier = _integer(start_model_id, name="start_model_id")
    model_limit = _integer(max_models, name="max_models", minimum=1)
    selected_limit = _integer(
        max_selected_training_fits,
        name="max_selected_training_fits",
        minimum=1,
    )
    if minimum > maximum:
        raise ValueError("min_dimension must not exceed max_dimension")
    if maximum > dimension_cap:
        raise MemoryError("max_dimension exceeds max_dimension_cap")
    if not minimum <= first_dimension <= maximum:
        raise ValueError("start_dimension is outside the requested range")
    if first_identifier >= affine_model_count(first_dimension):
        raise ValueError("start_model_id is outside the starting dimension")

    examined = 0
    fit_count = 0
    selected: list[tuple[int, int, AffineDigitModel]] = []
    checkpoint: dict[str, int] | None = None
    completed = True
    per_dimension: list[dict[str, Any]] = []

    for dimension in range(first_dimension, maximum + 1):
        count = affine_model_count(dimension)
        begin = first_identifier if dimension == first_dimension else 0
        dimension_examined = 0
        dimension_fits = 0
        stop = begin
        for model_id in range(begin, count):
            if examined >= model_limit:
                completed = False
                checkpoint = {
                    "next_dimension": dimension,
                    "next_model_id": model_id,
                }
                break
            model = decode_affine_model(dimension, model_id)
            examined += 1
            dimension_examined += 1
            stop = model_id + 1
            mismatch = locate_first_counterexample(
                model, data, start=0, stop=train
            )
            if mismatch is None:
                fit_count += 1
                dimension_fits += 1
                if len(selected) < selected_limit:
                    selected.append((dimension, model_id, model))
        per_dimension.append(
            {
                "dimension": dimension,
                "encoded_bits": affine_encoding_bits(dimension),
                "full_labeled_model_count": count,
                "start_model_id": begin,
                "stop_model_id_exclusive": stop,
                "models_examined": dimension_examined,
                "training_fit_count": dimension_fits,
                "completed_dimension": stop == count,
            }
        )
        if not completed:
            break

    candidate_records: list[dict[str, Any]] = []
    for dimension, model_id, model in selected:
        counterexample = locate_first_counterexample(
            model, data, start=train, stop=len(data)
        )
        candidate_records.append(
            {
                "dimension": dimension,
                "model_id": model_id,
                "model": model.as_record(),
                "training_validation": {
                    "start": 0,
                    "stop": train,
                    "exact_on_segment": True,
                },
                "held_out_validation": {
                    "start": train,
                    "stop": len(data),
                    "exact_on_segment": counterexample is None,
                    "first_counterexample": counterexample,
                    "comparisons_before_decision": (
                        len(data) - train
                        if counterexample is None
                        else counterexample["index"] - train + 1
                    ),
                },
            }
        )

    total_requested = sum(
        affine_model_count(dimension)
        - (first_identifier if dimension == first_dimension else 0)
        for dimension in range(first_dimension, maximum + 1)
    )
    all_training_fits_validated = fit_count == len(selected)
    all_requested_completed = completed and all_training_fits_validated
    report: dict[str, Any] = {
        "search_name": "affine_gf2_binary_digit_matrix_products",
        "parameters": {
            "min_dimension": minimum,
            "max_dimension": maximum,
            "start_dimension": first_dimension,
            "start_model_id": first_identifier,
            "max_models": model_limit,
            "max_selected_training_fits": selected_limit,
            "max_dimension_cap": dimension_cap,
        },
        "split": {
            "sample_count": len(data),
            "training": {"start": 0, "stop": train},
            "held_out_validation": {"start": train, "stop": len(data)},
            "selection_rule": (
                "enumerate and rank by (dimension, model_id) using training "
                "bits only; freeze the first bounded training fits; inspect "
                "held-out bits only after enumeration terminates"
            ),
        },
        "enumeration": {
            "ordering": "dimension ascending, then model_id ascending",
            "requested_model_count": total_requested,
            "models_examined": examined,
            "training_fit_count": fit_count,
            "per_dimension": per_dimension,
            "completed_requested_range": completed,
            "termination": (
                "completed_requested_range" if completed else "max_models_reached"
            ),
            "checkpoint": checkpoint,
        },
        "selected_training_fit_count": len(selected),
        "unreported_training_fit_count": fit_count - len(selected),
        "selected_candidates": candidate_records,
        "completion": {
            "enumeration_completed": completed,
            "selected_candidates_validated": len(candidate_records) == len(selected),
            "all_training_fits_validated": all_training_fits_validated,
            "all_requested_searches_completed": all_requested_completed,
        },
        "status": "finite-exhaustive" if all_requested_completed else "inconclusive",
        "proof_scope": (
            "exact enumeration only of the reported labeled affine GF(2) "
            "models and exact comparison with the reported finite segments"
        ),
        "interpretation": (
            "A held-out mismatch refutes that fixed candidate on the supplied "
            "finite bit. No search outcome has an asymptotic interpretation."
        ),
        "limitations": [
            "a bounded failure does not establish nonautomaticity",
            "the affine family is only a structured subclass of finite transducers",
            "a finite held-out fit does not prove correctness for all n",
            "no outcome establishes an o(n) algorithm or an Omega(n) lower bound",
        ],
        "complexity_measure": {
            "search_time": (
                "O(models_examined * train_length * log(sample_count)) in the "
                "direct evaluator, usually less due to first-mismatch stopping"
            ),
            "search_space": "O(max_selected_training_fits * model_size)",
            "single_query_time": "O(dimension^2 * log(n+1)) bit operations",
            "single_query_space": "O(dimension) mutable state bits",
            "unit": "deterministic Python integer and GF(2) bit operations",
        },
    }
    report.update(
        _contract(
            machine_model=(
                "two affine GF(2) state maps selected by each canonical binary "
                "digit, followed by an affine output functional"
            ),
            digit_order="most-significant bit first",
            preprocessing=(
                "candidate selection uses only training bits; no held-out bit, "
                "per-index advice, oracle, or randomness is used"
            ),
        )
    )
    return report


def _assign_colors(signatures: Iterable[object]) -> tuple[list[int], int]:
    identifiers: dict[object, int] = {}
    colors: list[int] = []
    for signature in signatures:
        color = identifiers.get(signature)
        if color is None:
            color = len(identifiers)
            identifiers[signature] = color
        colors.append(color)
    return colors, len(identifiers)


def _kernel_node_offsets(max_level: int) -> tuple[int, ...]:
    return tuple((1 << level) - 1 for level in range(max_level + 1))


def finite_two_kernel_refinement(
    bits: Iterable[int],
    *,
    train_length: int,
    max_level: int,
    refinement_rounds: int,
    max_nodes: int = 1_000_000,
    max_work_entries: int = 8_000_000,
) -> dict[str, Any]:
    """Refine exact finite 2-kernel classes and test transition congruence.

    Round ``r`` classifies every sampled kernel element by its first ``2**r``
    terms.  Unlike a same-level distinct-prefix count, classes are compared
    across every level through ``max_level``.  Final child classes are checked
    at the same resolution, which can expose a non-closed or non-congruent
    finite quotient.  All construction data come from the training prefix.
    """
    data, train = _bits_and_split(bits, train_length)
    level_limit = _integer(max_level, name="max_level")
    rounds = _integer(refinement_rounds, name="refinement_rounds")
    node_limit = _integer(max_nodes, name="max_nodes", minimum=1)
    work_limit = _integer(max_work_entries, name="max_work_entries", minimum=1)
    if level_limit + rounds + 2 > 62:
        raise MemoryError("requested kernel tree is too deep")
    deepest_level = level_limit + rounds + 1
    required_training = 1 << deepest_level
    node_count = (1 << (deepest_level + 1)) - 1
    work_entries = sum(
        (1 << (deepest_level - round_index + 1)) - 1
        for round_index in range(rounds + 1)
    )
    if node_count > node_limit:
        raise MemoryError("kernel tree exceeds max_nodes")
    if work_entries > work_limit:
        raise MemoryError("kernel refinement exceeds max_work_entries")
    if train < required_training:
        raise ValueError(
            f"train_length must be at least {required_training} for the "
            "requested same-resolution child check"
        )

    offsets = _kernel_node_offsets(deepest_level)
    base_signatures = (
        data[residue]
        for level in range(deepest_level + 1)
        for residue in range(1 << level)
    )
    colors, _ = _assign_colors(base_signatures)
    profiles: list[dict[str, Any]] = []

    def target_colors(current: Sequence[int], available_level: int) -> list[int]:
        output: list[int] = []
        for level in range(min(level_limit, available_level) + 1):
            begin = offsets[level]
            output.extend(current[begin : begin + (1 << level)])
        return output

    selected = target_colors(colors, deepest_level)
    profiles.append(
        {
            "round": 0,
            "observations_per_kernel_element": 1,
            "sampled_kernel_node_count": len(selected),
            "distinct_class_count_across_levels": len(set(selected)),
        }
    )
    available = deepest_level
    for round_index in range(1, rounds + 1):
        next_available = available - 1
        signatures: list[tuple[int, int]] = []
        for level in range(next_available + 1):
            child_begin = offsets[level + 1]
            for residue in range(1 << level):
                signatures.append(
                    (
                        colors[child_begin + residue],
                        colors[child_begin + residue + (1 << level)],
                    )
                )
        colors, _ = _assign_colors(signatures)
        available = next_available
        selected = target_colors(colors, available)
        profiles.append(
            {
                "round": round_index,
                "observations_per_kernel_element": 1 << round_index,
                "sampled_kernel_node_count": len(selected),
                "distinct_class_count_across_levels": len(set(selected)),
            }
        )

    final_observations = 1 << rounds
    nodes: list[tuple[int, int, int, bytes]] = []
    for level in range(level_limit + 1):
        begin = offsets[level]
        stride = 1 << level
        for residue in range(stride):
            prefix = bytes(data[residue : stride * final_observations : stride])
            assert len(prefix) == final_observations
            nodes.append((level, residue, colors[begin + residue], prefix))

    color_to_state: dict[int, int] = {}
    state_occurrences: list[list[tuple[int, int]]] = []
    state_prefixes: list[bytes] = []
    for level, residue, color, prefix in nodes:
        state = color_to_state.get(color)
        if state is None:
            state = len(color_to_state)
            color_to_state[color] = state
            state_occurrences.append([])
            state_prefixes.append(prefix)
        state_occurrences[state].append((level, residue))

    structural_counterexample: dict[str, Any] | None = None
    transitions = [[-1, -1] for _ in state_occurrences]
    for state, occurrences in enumerate(state_occurrences):
        for digit in (0, 1):
            expected: int | None = None
            source: tuple[int, int] | None = None
            for level, residue in occurrences:
                child_residue = residue + digit * (1 << level)
                child_color = colors[offsets[level + 1] + child_residue]
                target = color_to_state.get(child_color)
                if target is None:
                    structural_counterexample = {
                        "kind": "same_resolution_child_class_not_closed",
                        "state": state,
                        "source_level": level,
                        "source_residue": residue,
                        "digit": digit,
                        "child_level": level + 1,
                        "child_residue": child_residue,
                    }
                    break
                if expected is None:
                    expected = target
                    source = (level, residue)
                elif target != expected:
                    assert source is not None
                    structural_counterexample = {
                        "kind": "same_class_has_incongruent_child_classes",
                        "state": state,
                        "digit": digit,
                        "first_source": {
                            "level": source[0],
                            "residue": source[1],
                            "target_state": expected,
                        },
                        "conflicting_source": {
                            "level": level,
                            "residue": residue,
                            "target_state": target,
                        },
                    }
                    break
            if structural_counterexample is not None:
                break
            assert expected is not None
            transitions[state][digit] = expected
        if structural_counterexample is not None:
            break

    certificate = bytearray()
    for level, residue, _color, prefix in nodes:
        certificate.extend(level.to_bytes(4, "little"))
        certificate.extend(residue.to_bytes(8, "little"))
        certificate.extend(prefix)

    state_records = [
        {
            "state": state,
            "representative_prefix_sha256_u8": hashlib.sha256(prefix).hexdigest(),
            "output": prefix[0],
            "occurrence_count": len(state_occurrences[state]),
            "first_occurrence": {
                "level": state_occurrences[state][0][0],
                "residue": state_occurrences[state][0][1],
            },
        }
        for state, prefix in enumerate(state_prefixes)
    ]

    candidate: dict[str, Any] | None = None
    if structural_counterexample is None:
        outputs = [prefix[0] for prefix in state_prefixes]
        root_state = color_to_state[colors[offsets[0]]]

        def evaluate_candidate(index: int) -> int:
            state = root_state
            for digit in _canonical_digits(index, lsb_first=True):
                state = transitions[state][digit]
            return outputs[state]

        training_counterexample = next(
            (
                {
                    "index": index,
                    "index_binary": f"{index:b}",
                    "predicted": evaluate_candidate(index),
                    "observed": data[index],
                }
                for index in range(train)
                if evaluate_candidate(index) != data[index]
            ),
            None,
        )
        held_out_counterexample = next(
            (
                {
                    "index": index,
                    "index_binary": f"{index:b}",
                    "predicted": evaluate_candidate(index),
                    "observed": data[index],
                }
                for index in range(train, len(data))
                if evaluate_candidate(index) != data[index]
            ),
            None,
        )
        candidate = {
            "digit_order": "lsb_first",
            "initial_state": root_state,
            "transitions": transitions,
            "outputs": outputs,
            "training_validation": {
                "exact_on_segment": training_counterexample is None,
                "first_counterexample": training_counterexample,
            },
            "held_out_validation": {
                "start": train,
                "stop": len(data),
                "exact_on_segment": held_out_counterexample is None,
                "first_counterexample": held_out_counterexample,
            },
        }

    report: dict[str, Any] = {
        "search_name": "multiscale_finite_two_kernel_partition_refinement",
        "parameters": {
            "max_level": level_limit,
            "refinement_rounds": rounds,
            "observations_per_kernel_element": final_observations,
            "required_training_length": required_training,
            "max_nodes": node_limit,
            "max_work_entries": work_limit,
        },
        "split": {
            "sample_count": len(data),
            "training": {"start": 0, "stop": train},
            "held_out_validation": {"start": train, "stop": len(data)},
            "selection_rule": (
                "all partition refinement, class naming, closure checks, and "
                "candidate construction use training bits only"
            ),
        },
        "construction": {
            "deepest_sampled_level": deepest_level,
            "allocated_node_upper_bound": node_count,
            "work_entry_upper_bound": work_entries,
            "refinement_profile": profiles,
            "sampled_nodes_through_max_level": len(nodes),
            "distinct_class_count_across_levels": len(state_occurrences),
            "pairwise_distinct_class_pairs": (
                len(state_occurrences) * (len(state_occurrences) - 1) // 2
            ),
            "finite_distinction_certificate_sha256": hashlib.sha256(
                certificate
            ).hexdigest(),
            "state_classes": state_records,
            "closed_and_transition_congruent": structural_counterexample is None,
            "first_structural_counterexample": structural_counterexample,
        },
        "candidate_model": candidate,
        "completion": {
            "training_tree_completed": True,
            "all_refinement_rounds_completed": True,
            "same_resolution_child_check_completed": True,
            "candidate_validated_if_constructed": candidate is None
            or (
                "training_validation" in candidate
                and "held_out_validation" in candidate
            ),
            "all_requested_searches_completed": True,
        },
        "status": "finite-exhaustive",
        "proof_scope": (
            "exact partition refinement and transition checks only for the "
            "reported finite kernel nodes and witnessed training prefixes"
        ),
        "interpretation": (
            "Different witnessed prefixes prove those sampled kernel elements "
            "are distinct, but finitely many classes or a failed finite quotient "
            "does not determine whether the full 2-kernel is finite."
        ),
        "limitations": [
            "finite 2-kernel growth does not establish nonautomaticity",
            "equal finite signatures need not denote equal infinite subsequences",
            "a finite closed quotient may fail at a longer observation horizon",
            "training-derived states are finite-prefix advice until proved uniform",
            "no outcome establishes a computational lower bound",
        ],
        "complexity_measure": {
            "search_time": "O(max_work_entries) deterministic refinement operations",
            "search_space": "O(max_nodes) integer colors plus reported class metadata",
            "single_query_time": "O(log(n+1)) table transitions if a quotient is built",
            "single_query_space": "O(log q) mutable state bits",
            "unit": "deterministic finite prefix and integer table operations",
        },
    }
    report.update(
        _contract(
            machine_model=(
                "finite LSB-first 2-kernel partition quotient when the sampled "
                "same-resolution classes are closed and transition-congruent"
            ),
            digit_order="least-significant bit first",
            preprocessing=(
                "multiscale signatures and tables are derived only from the "
                "training prefix and frozen before held-out validation"
            ),
        )
    )
    return report
