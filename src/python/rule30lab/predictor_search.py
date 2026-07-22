"""Bounded exact model searches for finite Rule 30 center prefixes.

Every routine in this module has finite scope.  Exhaustive means exhaustive
only over the explicitly bounded model identifiers and supplied finite data.
Neither a failed search nor a held-out counterexample establishes a lower
bound, nonautomaticity, or the nonexistence of another exact representation.
"""

from __future__ import annotations

import hashlib
import operator
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from .automaticity import (
    fit_berlekamp_massey_and_validate,
    two_kernel_prefixes,
    validate_binary_recurrence,
)


def _integer(value: int, *, name: str, minimum: int | None = None) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer, not bool")
    try:
        checked = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if minimum is not None and checked < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return checked


def _validated_bits(bits: Iterable[int]) -> bytes:
    output = bytearray()
    for index, value in enumerate(bits):
        try:
            bit = operator.index(value)
        except TypeError as exc:
            raise ValueError(f"bit at index {index} is not an integer") from exc
        if bit not in (0, 1):
            raise ValueError(
                f"bit at index {index} must be 0 or 1, got {value!r}"
            )
        output.append(bit)
    return bytes(output)


def _validated_split(
    bits: Iterable[int], train_length: int
) -> tuple[bytes, int]:
    data = _validated_bits(bits)
    checked_train = _integer(train_length, name="train_length", minimum=1)
    if checked_train >= len(data):
        raise ValueError("train_length must leave at least one held-out bit")
    return data, checked_train


def _search_contract(
    *,
    machine_model: str,
    digit_order: str,
    preprocessing_and_advice: str,
    search_time: str,
    search_space: str,
    query_time: str,
    query_space: str,
) -> dict[str, Any]:
    """Return metadata required on every Problem 3 search report."""
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
        "preprocessing_and_advice_assumptions": preprocessing_and_advice,
        "uniformity_assumption": (
            "one fixed finite candidate is applied to every queried n; a table "
            "learned from a finite prefix is not treated as a proved uniform "
            "algorithm for the infinite sequence"
        ),
        "complexity_measure": {
            "search_time": search_time,
            "search_space": search_space,
            "single_query_time": query_time,
            "single_query_space": query_space,
            "unit": "deterministic bit/table operations in the stated model",
        },
        "determinism": {
            "randomness_used": False,
            "deterministic_seed": 0,
        },
        "finite_only_status": "bounded_finite_search",
    }


def _split_record(sample_count: int, train_length: int) -> dict[str, Any]:
    return {
        "sample_count": sample_count,
        "training": {"start": 0, "stop": train_length},
        "held_out_validation": {"start": train_length, "stop": sample_count},
        "selection_rule": (
            "models are fitted and ordered using training bits only; held-out "
            "bits are read only after a training-fit model is fixed"
        ),
    }


def canonical_binary_digits(n: int, *, order: str = "msb_first") -> tuple[int, ...]:
    """Return the declared canonical binary representation of ``n``."""
    checked = _integer(n, name="n", minimum=0)
    if order not in ("msb_first", "lsb_first"):
        raise ValueError("order must be 'msb_first' or 'lsb_first'")
    digits = (0,) if checked == 0 else tuple(int(ch) for ch in f"{checked:b}")
    return digits if order == "msb_first" else tuple(reversed(digits))


@dataclass(frozen=True)
class DFAO:
    """A deterministic complete finite automaton with one output per state."""

    transitions: tuple[tuple[int, int], ...]
    outputs: tuple[int, ...]
    digit_order: str = "msb_first"
    initial_state: int = 0

    def __post_init__(self) -> None:
        state_count = len(self.transitions)
        if state_count < 1:
            raise ValueError("a DFAO must have at least one state")
        if len(self.outputs) != state_count:
            raise ValueError("outputs must contain one bit per state")
        if self.digit_order not in ("msb_first", "lsb_first"):
            raise ValueError("invalid digit order")
        if self.initial_state < 0 or self.initial_state >= state_count:
            raise ValueError("initial_state is outside the state set")
        for state, output in enumerate(self.outputs):
            if output not in (0, 1):
                raise ValueError(f"output for state {state} is not a bit")
        for state, row in enumerate(self.transitions):
            if len(row) != 2:
                raise ValueError(f"state {state} must have transitions for 0 and 1")
            for target in row:
                if target < 0 or target >= state_count:
                    raise ValueError(f"transition from state {state} is out of range")

    @property
    def state_count(self) -> int:
        return len(self.transitions)

    def as_record(self) -> dict[str, Any]:
        return {
            "state_count": self.state_count,
            "initial_state": self.initial_state,
            "digit_order": self.digit_order,
            "transitions": [list(row) for row in self.transitions],
            "outputs": list(self.outputs),
        }


def evaluate_dfao(model: DFAO, n: int) -> int:
    """Evaluate one DFAO on the canonical binary encoding of ``n``."""
    state = model.initial_state
    for digit in canonical_binary_digits(n, order=model.digit_order):
        state = model.transitions[state][digit]
    return model.outputs[state]


def labeled_dfao_model_count(state_count: int) -> int:
    """Count labeled complete binary DFAOs with initial state fixed at zero."""
    states = _integer(state_count, name="state_count", minimum=1)
    return (1 << states) * states ** (2 * states)


def decode_labeled_dfao(state_count: int, model_id: int) -> DFAO:
    """Decode the deterministic mixed-radix DFAO enumeration.

    The low ``state_count`` bits are state outputs.  Remaining base-q digits,
    least significant first, are transitions in ``(state, symbol)`` order.
    """
    states = _integer(state_count, name="state_count", minimum=1)
    identifier = _integer(model_id, name="model_id", minimum=0)
    count = labeled_dfao_model_count(states)
    if identifier >= count:
        raise ValueError(f"model_id must be smaller than {count}")

    output_mask = (1 << states) - 1
    output_code = identifier & output_mask
    transition_code = identifier >> states
    outputs = tuple((output_code >> state) & 1 for state in range(states))
    transitions: list[tuple[int, int]] = []
    for _state in range(states):
        zero_target = transition_code % states
        transition_code //= states
        one_target = transition_code % states
        transition_code //= states
        transitions.append((zero_target, one_target))
    return DFAO(tuple(transitions), outputs, digit_order="msb_first")


def _prediction_report(
    data: Sequence[int],
    predictions: Iterable[tuple[int, int]],
    *,
    start: int,
    stop: int,
    max_reported_errors: int,
) -> dict[str, Any]:
    error_count = 0
    first_counterexample: dict[str, Any] | None = None
    reported: list[dict[str, Any]] = []
    prediction_bytes = bytearray()
    for index, prediction in predictions:
        prediction_bytes.append(prediction)
        expected = data[index]
        if prediction != expected:
            error_count += 1
            counterexample = {
                "index": index,
                "index_binary": f"{index:b}",
                "expected": expected,
                "predicted": prediction,
            }
            if first_counterexample is None:
                first_counterexample = counterexample
            if len(reported) < max_reported_errors:
                reported.append(counterexample)
    return {
        "start": start,
        "stop": stop,
        "evaluated": stop - start,
        "error_count": error_count,
        "exact_on_segment": error_count == 0,
        "first_counterexample": first_counterexample,
        "reported_counterexamples": reported,
        "reported_counterexamples_truncated": error_count > len(reported),
        "prediction_sha256_u8": hashlib.sha256(prediction_bytes).hexdigest(),
    }


def _validate_dfao_segment(
    model: DFAO,
    data: Sequence[int],
    start: int,
    stop: int,
    max_reported_errors: int,
) -> dict[str, Any]:
    return _prediction_report(
        data,
        ((index, evaluate_dfao(model, index)) for index in range(start, stop)),
        start=start,
        stop=stop,
        max_reported_errors=max_reported_errors,
    )


def _first_dfao_training_mismatch(
    model: DFAO, data: Sequence[int], train_length: int
) -> int | None:
    for index in range(train_length):
        if evaluate_dfao(model, index) != data[index]:
            return index
    return None


def search_labeled_dfaos(
    bits: Iterable[int],
    *,
    train_length: int,
    min_states: int = 1,
    max_states: int = 3,
    start_state_count: int | None = None,
    start_model_id: int = 0,
    max_models: int = 100_000,
    stop_after_fits: int | None = 1,
    max_reported_fits: int = 16,
    max_reported_errors: int = 16,
    max_input_symbols: int = 10_000_000,
    max_state_count_cap: int = 16,
) -> dict[str, Any]:
    """Enumerate labeled MSB-first DFAOs and validate training-fit models.

    ``(start_state_count, start_model_id)`` is a stable checkpoint.  Model IDs
    are independent at each state count and are decoded by
    :func:`decode_labeled_dfao`.
    """
    data, checked_train = _validated_split(bits, train_length)
    first_states = _integer(min_states, name="min_states", minimum=1)
    last_states = _integer(max_states, name="max_states", minimum=1)
    if last_states < first_states:
        raise ValueError("max_states must be at least min_states")
    state_cap = _integer(
        max_state_count_cap, name="max_state_count_cap", minimum=1
    )
    if last_states > state_cap:
        raise MemoryError(
            f"max_states={last_states} exceeds max_state_count_cap={state_cap}"
        )
    resume_states = (
        first_states
        if start_state_count is None
        else _integer(start_state_count, name="start_state_count", minimum=1)
    )
    if resume_states < first_states or resume_states > last_states:
        raise ValueError("start_state_count is outside the requested state range")
    resume_id = _integer(start_model_id, name="start_model_id", minimum=0)
    model_limit = _integer(max_models, name="max_models", minimum=1)
    report_limit = _integer(
        max_reported_fits, name="max_reported_fits", minimum=0
    )
    error_limit = _integer(
        max_reported_errors, name="max_reported_errors", minimum=0
    )
    symbol_limit = _integer(
        max_input_symbols, name="max_input_symbols", minimum=1
    )
    if stop_after_fits is not None:
        fit_stop = _integer(stop_after_fits, name="stop_after_fits", minimum=1)
    else:
        fit_stop = None

    symbol_count = sum(max(1, index.bit_length()) for index in range(len(data)))
    if symbol_count > symbol_limit:
        raise MemoryError(
            f"encoded inputs need {symbol_count} symbols, exceeding "
            f"max_input_symbols={symbol_limit}"
        )
    if resume_id > labeled_dfao_model_count(resume_states):
        raise ValueError("start_model_id exceeds the selected state search space")

    began_at_origin = resume_states == first_states and resume_id == 0
    total_space = sum(
        labeled_dfao_model_count(states)
        for states in range(first_states, last_states + 1)
    )
    examined = 0
    training_fit_count = 0
    reported_fits: list[dict[str, Any]] = []
    state_summaries: list[dict[str, Any]] = []
    checkpoint: dict[str, int] | None = None
    termination_reason = "completed_requested_range"

    for states in range(resume_states, last_states + 1):
        model_count = labeled_dfao_model_count(states)
        first_id = resume_id if states == resume_states else 0
        if first_id == model_count:
            state_summaries.append(
                {
                    "state_count": states,
                    "model_count": model_count,
                    "start_model_id": first_id,
                    "stop_model_id_exclusive": first_id,
                    "models_examined": 0,
                    "training_fit_count": 0,
                }
            )
            continue
        state_examined = 0
        state_fits = 0
        next_id = first_id
        for identifier in range(first_id, model_count):
            if examined >= model_limit:
                checkpoint = {
                    "next_state_count": states,
                    "next_model_id": identifier,
                }
                termination_reason = "max_models_reached"
                break
            model = decode_labeled_dfao(states, identifier)
            examined += 1
            state_examined += 1
            next_id = identifier + 1
            if _first_dfao_training_mismatch(model, data, checked_train) is not None:
                continue

            training_fit_count += 1
            state_fits += 1
            validation = _validate_dfao_segment(
                model, data, checked_train, len(data), error_limit
            )
            if len(reported_fits) < report_limit:
                reported_fits.append(
                    {
                        "state_count": states,
                        "model_id": identifier,
                        "model": model.as_record(),
                        "training_exact": True,
                        "held_out_validation": validation,
                    }
                )
            if fit_stop is not None and training_fit_count >= fit_stop:
                if next_id < model_count:
                    checkpoint = {
                        "next_state_count": states,
                        "next_model_id": next_id,
                    }
                elif states < last_states:
                    checkpoint = {
                        "next_state_count": states + 1,
                        "next_model_id": 0,
                    }
                termination_reason = "training_fit_limit_reached"
                break

        state_summaries.append(
            {
                "state_count": states,
                "model_count": model_count,
                "start_model_id": first_id,
                "stop_model_id_exclusive": next_id,
                "models_examined": state_examined,
                "training_fit_count": state_fits,
            }
        )
        if termination_reason != "completed_requested_range":
            break

    completed = termination_reason == "completed_requested_range"
    full_bounded_exhaustion = completed and began_at_origin
    status = "finite-exhaustive" if completed else "inconclusive"
    result: dict[str, Any] = {
        "search_name": "labeled_complete_binary_dfao",
        "parameters": {
            "min_states": first_states,
            "max_states": last_states,
            "start_state_count": resume_states,
            "start_model_id": resume_id,
            "max_models": model_limit,
            "stop_after_fits": fit_stop,
            "max_reported_fits": report_limit,
            "max_reported_errors": error_limit,
            "max_input_symbols": symbol_limit,
            "max_state_count_cap": state_cap,
        },
        "split": _split_record(len(data), checked_train),
        "enumeration": {
            "order": (
                "state count ascending, then mixed-radix model_id ascending; "
                "state labels are significant and initial state is 0"
            ),
            "requested_model_space_size": total_space,
            "models_examined": examined,
            "training_fit_count": training_fit_count,
            "reported_fit_count": len(reported_fits),
            "state_summaries": state_summaries,
            "completed_requested_range": completed,
            "began_at_bounded_space_origin": began_at_origin,
            "completed_full_bounded_space": full_bounded_exhaustion,
            "termination_reason": termination_reason,
            "checkpoint": checkpoint,
        },
        "training_fit_models": reported_fits,
        "status": status,
        "proof_scope": (
            "exact enumeration of only the reported labeled DFAO model-ID range "
            "and exact comparison on the identified finite split"
        ),
        "interpretation": (
            "A complete no-fit run excludes only these bounded labeled DFAOs "
            "on the training prefix. A held-out mismatch is an explicit finite "
            "counterexample to that fitted model."
        ),
        "limitations": [
            "state relabelings are deliberately enumerated as separate models",
            "finite failure does not establish nonautomaticity",
            "finite failure does not imply any time lower bound",
            "finite held-out agreement does not prove correctness for all n",
        ],
    }
    result.update(
        _search_contract(
            machine_model=(
                "deterministic complete q-state binary DFAO with labeled states, "
                "initial state 0, two transitions per state, and one output bit "
                "per state"
            ),
            digit_order="most-significant bit first",
            preprocessing_and_advice=(
                "the finite automaton table is selected from training bits; no "
                "held-out bit, oracle, randomness, or per-index advice is used"
            ),
            search_time=(
                "O(models_examined * train_length * log(train_length)) time and "
                "early termination at each model's first training mismatch"
            ),
            search_space="O(sample_count + q + bounded reported output)",
            query_time="O(log(n+1)) table transitions",
            query_space="O(log q) mutable state bits plus read-only model tables",
        )
    )
    return result


def fit_two_kernel_quotient_dfao(
    bits: Iterable[int],
    *,
    train_length: int,
    depth: int,
    fingerprint_length: int,
    max_nodes: int = 131_071,
    max_fingerprint_bytes: int = 64 * 1024 * 1024,
    max_reported_errors: int = 16,
) -> dict[str, Any]:
    """Fit one closed LSB-first DFAO quotient from finite 2-kernel fingerprints.

    Nodes ``(level, residue)`` represent the sampled subsequence
    ``c[2**level * m + residue]``.  Equal fixed-length fingerprints are merged.
    The construction succeeds only if every observed child maps to an existing
    class and the induced transition is independent of the representative.
    """
    data, checked_train = _validated_split(bits, train_length)
    checked_depth = _integer(depth, name="depth", minimum=0)
    prefix = _integer(
        fingerprint_length, name="fingerprint_length", minimum=1
    )
    node_limit = _integer(max_nodes, name="max_nodes", minimum=1)
    byte_limit = _integer(
        max_fingerprint_bytes, name="max_fingerprint_bytes", minimum=1
    )
    error_limit = _integer(
        max_reported_errors, name="max_reported_errors", minimum=0
    )
    if checked_depth + 2 > node_limit.bit_length():
        raise MemoryError(
            "kernel depth exceeds max_nodes before node-tree construction"
        )
    node_count = (1 << (checked_depth + 2)) - 1
    fingerprint_bytes = node_count * prefix
    if node_count > node_limit:
        raise MemoryError(
            f"kernel tree needs {node_count} nodes, exceeding max_nodes={node_limit}"
        )
    if fingerprint_bytes > byte_limit:
        raise MemoryError(
            f"kernel fingerprints need {fingerprint_bytes} bytes, exceeding "
            f"max_fingerprint_bytes={byte_limit}"
        )
    required_training = prefix * (1 << (checked_depth + 1))
    if checked_train < required_training:
        raise ValueError(
            f"train_length must be at least {required_training} so every child "
            "has a full fingerprint"
        )

    training = data[:checked_train]
    levels = tuple(
        two_kernel_prefixes(training, level, prefix)
        for level in range(checked_depth + 2)
    )
    fingerprint_to_state: dict[bytes, int] = {}
    state_fingerprints: list[bytes] = []
    occurrences: list[list[tuple[int, int]]] = []
    for level in range(checked_depth + 1):
        for residue, fingerprint in enumerate(levels[level]):
            state = fingerprint_to_state.get(fingerprint)
            if state is None:
                state = len(state_fingerprints)
                fingerprint_to_state[fingerprint] = state
                state_fingerprints.append(fingerprint)
                occurrences.append([])
            occurrences[state].append((level, residue))

    transitions: list[list[int]] = [[-1, -1] for _ in state_fingerprints]
    structural_counterexample: dict[str, Any] | None = None
    for state, nodes in enumerate(occurrences):
        for digit in (0, 1):
            expected_target: int | None = None
            expected_source: tuple[int, int] | None = None
            for level, residue in nodes:
                child_residue = residue + digit * (1 << level)
                child_fingerprint = levels[level + 1][child_residue]
                target = fingerprint_to_state.get(child_fingerprint)
                if target is None:
                    structural_counterexample = {
                        "kind": "child_fingerprint_not_closed",
                        "state": state,
                        "representative_level": level,
                        "representative_residue": residue,
                        "input_digit": digit,
                        "child_level": level + 1,
                        "child_residue": child_residue,
                        "child_fingerprint_sha256": hashlib.sha256(
                            child_fingerprint
                        ).hexdigest(),
                    }
                    break
                if expected_target is None:
                    expected_target = target
                    expected_source = (level, residue)
                elif target != expected_target:
                    structural_counterexample = {
                        "kind": "merged_class_has_inconsistent_child_classes",
                        "state": state,
                        "input_digit": digit,
                        "first_source": {
                            "level": expected_source[0],
                            "residue": expected_source[1],
                            "target_state": expected_target,
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
            assert expected_target is not None
            transitions[state][digit] = expected_target
        if structural_counterexample is not None:
            break

    model: DFAO | None = None
    training_validation: dict[str, Any] | None = None
    held_out_validation: dict[str, Any] | None = None
    if structural_counterexample is None:
        model = DFAO(
            tuple((row[0], row[1]) for row in transitions),
            tuple(fingerprint[0] for fingerprint in state_fingerprints),
            digit_order="lsb_first",
        )
        training_validation = _validate_dfao_segment(
            model, data, 0, checked_train, error_limit
        )
        held_out_validation = _validate_dfao_segment(
            model, data, checked_train, len(data), error_limit
        )

    state_records = [
        {
            "state": state,
            "fingerprint_sha256": hashlib.sha256(fingerprint).hexdigest(),
            "output": fingerprint[0],
            "observed_occurrences": [
                {"level": level, "residue": residue}
                for level, residue in occurrences[state]
            ],
        }
        for state, fingerprint in enumerate(state_fingerprints)
    ]
    accepted = (
        model is not None
        and training_validation is not None
        and training_validation["exact_on_segment"]
    )
    result: dict[str, Any] = {
        "search_name": "finite_two_kernel_fingerprint_quotient",
        "parameters": {
            "depth": checked_depth,
            "fingerprint_length": prefix,
            "required_training_length": required_training,
            "max_nodes": node_limit,
            "max_fingerprint_bytes": byte_limit,
            "max_reported_errors": error_limit,
        },
        "split": _split_record(len(data), checked_train),
        "construction": {
            "sampled_node_count_including_children": node_count,
            "stored_fingerprint_bytes_upper_bound": fingerprint_bytes,
            "quotient_state_count": len(state_fingerprints),
            "state_classes": state_records,
            "closed_and_transition_consistent": structural_counterexample is None,
            "first_structural_counterexample": structural_counterexample,
        },
        "candidate_model": None if model is None else model.as_record(),
        "candidate_training_validation": training_validation,
        "candidate_accepted_from_training": accepted,
        "held_out_validation": held_out_validation,
        "status": "finite-exhaustive",
        "proof_scope": (
            "exact construction and consistency check for this single finite "
            "fingerprint equivalence relation, followed by exact finite validation"
        ),
        "interpretation": (
            "A structural conflict refutes only this fingerprint quotient. A "
            "held-out mismatch refutes only the resulting finite fitted DFAO."
        ),
        "limitations": [
            "finite fingerprints need not equal infinite 2-kernel subsequences",
            "a failed quotient does not establish nonautomaticity",
            "a successful finite quotient need not remain valid at greater depth",
            "the learned table is finite-prefix preprocessing, not a proved uniform algorithm",
            "no outcome implies a computational lower bound",
        ],
    }
    result.update(
        _search_contract(
            machine_model=(
                "deterministic complete binary DFAO induced, when possible, by "
                "equivalence classes of finite 2-kernel fingerprints"
            ),
            digit_order="least-significant bit first",
            preprocessing_and_advice=(
                "fingerprint classes and tables are derived only from the training "
                "prefix; they are fixed before held-out validation"
            ),
            search_time=(
                "O(fingerprint_length * 2**(depth+1)) sampled data plus finite "
                "hashing and transition-consistency checks"
            ),
            search_space=(
                "O(fingerprint_length * 2**(depth+1)) bytes, bounded before allocation"
            ),
            query_time="O(log(n+1)) table transitions",
            query_space="O(log q) mutable state bits plus read-only model tables",
        )
    )
    return result


def decode_canonical_gf2_recurrence(candidate_id: int) -> tuple[int, ...]:
    """Decode a unique exact-order homogeneous GF(2) recurrence.

    ID zero is the order-zero all-zero predictor.  For a positive ID, the
    order is its bit length, the highest-lag coefficient is one, and lower
    bits encode coefficients ``a_1, ..., a_(L-1)``.
    """
    identifier = _integer(candidate_id, name="candidate_id", minimum=0)
    if identifier == 0:
        return ()
    order = identifier.bit_length()
    lower = identifier - (1 << (order - 1))
    return tuple(
        [((lower >> offset) & 1) for offset in range(order - 1)] + [1]
    )


def _gf2_training_exact(
    data: Sequence[int], coefficients: Sequence[int], train_length: int
) -> bool:
    order = len(coefficients)
    for index in range(order, train_length):
        prediction = 0
        for offset, coefficient in enumerate(coefficients, start=1):
            prediction ^= coefficient & data[index - offset]
        if prediction != data[index]:
            return False
    return True


def search_short_gf2_recurrences(
    bits: Iterable[int],
    *,
    train_length: int,
    max_order: int,
    start_candidate_id: int = 0,
    max_candidates: int = 1_000_000,
    stop_after_fits: int | None = 1,
    max_reported_fits: int = 16,
    max_reported_errors: int = 16,
    max_order_cap: int = 64,
) -> dict[str, Any]:
    """Exhaustively enumerate canonical homogeneous GF(2) recurrences."""
    data, checked_train = _validated_split(bits, train_length)
    order_limit = _integer(max_order, name="max_order", minimum=0)
    order_cap = _integer(max_order_cap, name="max_order_cap", minimum=0)
    if order_limit > order_cap:
        raise MemoryError(
            f"max_order={order_limit} exceeds max_order_cap={order_cap}"
        )
    if order_limit > checked_train:
        raise ValueError("max_order must not exceed train_length")
    total = 1 << order_limit
    start = _integer(start_candidate_id, name="start_candidate_id", minimum=0)
    if start > total:
        raise ValueError("start_candidate_id exceeds the recurrence search space")
    candidate_limit = _integer(
        max_candidates, name="max_candidates", minimum=1
    )
    report_limit = _integer(
        max_reported_fits, name="max_reported_fits", minimum=0
    )
    error_limit = _integer(
        max_reported_errors, name="max_reported_errors", minimum=0
    )
    if stop_after_fits is not None:
        fit_stop = _integer(stop_after_fits, name="stop_after_fits", minimum=1)
    else:
        fit_stop = None

    examined = 0
    fit_count = 0
    fits: list[dict[str, Any]] = []
    next_id = start
    termination = "completed_requested_range"
    for identifier in range(start, total):
        if examined >= candidate_limit:
            next_id = identifier
            termination = "max_candidates_reached"
            break
        coefficients = decode_canonical_gf2_recurrence(identifier)
        examined += 1
        next_id = identifier + 1
        if not _gf2_training_exact(data, coefficients, checked_train):
            continue
        fit_count += 1
        validation = validate_binary_recurrence(
            data,
            coefficients,
            train_length=checked_train,
            max_reported_errors=error_limit,
        )
        if len(fits) < report_limit:
            fits.append(
                {
                    "candidate_id": identifier,
                    "order": len(coefficients),
                    "coefficients": list(coefficients),
                    "training": validation["training"],
                    "held_out_validation": {
                        **validation["held_out"],
                        "first_counterexample": (
                            None
                            if validation["held_out"]["first_error_index"] is None
                            else {
                                "index": validation["held_out"][
                                    "first_error_index"
                                ],
                                "index_binary": f"{validation['held_out']['first_error_index']:b}",
                                "expected": data[
                                    validation["held_out"]["first_error_index"]
                                ],
                                "predicted": _gf2_prediction_at(
                                    data,
                                    validation["held_out"]["first_error_index"],
                                    coefficients,
                                ),
                            }
                        ),
                    },
                }
            )
        if fit_stop is not None and fit_count >= fit_stop:
            termination = "training_fit_limit_reached"
            break

    completed = termination == "completed_requested_range"
    checkpoint = None if completed else {"next_candidate_id": next_id}
    result: dict[str, Any] = {
        "search_name": "canonical_homogeneous_gf2_recurrences",
        "parameters": {
            "max_order": order_limit,
            "start_candidate_id": start,
            "max_candidates": candidate_limit,
            "stop_after_fits": fit_stop,
            "max_reported_fits": report_limit,
            "max_reported_errors": error_limit,
            "max_order_cap": order_cap,
        },
        "split": _split_record(len(data), checked_train),
        "enumeration": {
            "order": (
                "candidate_id ascending; ID 0 is order zero, positive ID has "
                "order bit_length(ID) and highest-lag coefficient one"
            ),
            "candidate_space_size": total,
            "candidates_examined": examined,
            "training_fit_count": fit_count,
            "reported_fit_count": len(fits),
            "completed_requested_range": completed,
            "began_at_bounded_space_origin": start == 0,
            "completed_full_bounded_space": completed and start == 0,
            "termination_reason": termination,
            "checkpoint": checkpoint,
        },
        "training_fit_candidates": fits,
        "validation_protocol": (
            "exact recurrence equalities against observed history; the first "
            "held-out counterexample is found before any post-error history choice"
        ),
        "status": "finite-exhaustive" if completed else "inconclusive",
        "proof_scope": (
            "exact enumeration of the reported canonical GF(2) recurrence IDs "
            "and exact comparison on the identified finite split"
        ),
        "interpretation": (
            "A complete no-fit result excludes only homogeneous recurrences up "
            "to max_order on this finite training prefix."
        ),
        "limitations": [
            (
                "inhomogeneous, nonlinear, longer, or index-dependent "
                "recurrences are outside this class"
            ),
            "finite agreement does not establish a recurrence for the infinite sequence",
            "failed recurrence search does not imply a time lower bound",
        ],
    }
    result.update(
        _search_contract(
            machine_model=(
                "fixed homogeneous order-L linear recurrence over GF(2), with "
                "canonical highest-lag coefficient one"
            ),
            digit_order=(
                "binary n is not consumed by the sequential validator; a hypothetical "
                "random-access evaluator would read it most-significant bit first"
            ),
            preprocessing_and_advice=(
                "coefficients and L initial bits are selected from training data; "
                "no held-out data is used during fitting"
            ),
            search_time=(
                "O(candidates_examined * train_length * max_order), with early "
                "termination at each candidate's first training mismatch"
            ),
            search_space=(
                "O(sample_count + max_order + bounded reported coefficients)"
            ),
            query_time=(
                "sequential evaluation O(n*L); if globally proved, companion-matrix "
                "exponentiation gives a separate O(L**3 * log(n+1)) upper bound"
            ),
            query_space=(
                "O(L) sequential state, or O(L**2) for the stated dense matrix method"
            ),
        )
    )
    return result


def _gf2_prediction_at(
    data: Sequence[int], index: int, coefficients: Sequence[int]
) -> int:
    prediction = 0
    for offset, coefficient in enumerate(coefficients, start=1):
        prediction ^= coefficient & data[index - offset]
    return prediction


def fit_berlekamp_massey_candidate(
    bits: Iterable[int],
    *,
    train_length: int,
    max_reported_errors: int = 16,
) -> dict[str, Any]:
    """Fit Berlekamp--Massey strictly on training and validate held out."""
    data, checked_train = _validated_split(bits, train_length)
    error_limit = _integer(
        max_reported_errors, name="max_reported_errors", minimum=0
    )
    validation = fit_berlekamp_massey_and_validate(
        data,
        train_length=checked_train,
        max_reported_errors=error_limit,
    )
    first_error = validation["held_out"]["first_error_index"]
    coefficients = tuple(validation["coefficients"])
    result: dict[str, Any] = {
        "search_name": "berlekamp_massey_training_fit",
        "parameters": {"max_reported_errors": error_limit},
        "split": _split_record(len(data), checked_train),
        "candidate": {
            "method": validation["fit"]["method"],
            "order": validation["order"],
            "coefficients": validation["coefficients"],
            "connection_polynomial": validation["fit"][
                "connection_polynomial"
            ],
        },
        "training": validation["training"],
        "held_out_validation": {
            **validation["held_out"],
            "first_counterexample": (
                None
                if first_error is None
                else {
                    "index": first_error,
                    "index_binary": f"{first_error:b}",
                    "expected": data[first_error],
                    "predicted": _gf2_prediction_at(
                        data, first_error, coefficients
                    ),
                }
            ),
        },
        "validation_protocol": (
            "exact recurrence equalities against observed history; fitting uses "
            "training only and held-out checking begins after coefficients are fixed"
        ),
        "status": "empirical",
        "proof_scope": "exact fit and validation on the identified finite split only",
        "interpretation": (
            "Berlekamp--Massey returns a minimum linear recurrence for the "
            "training prefix; held-out testing actively seeks its first failure."
        ),
        "limitations": [
            "this is one data-dependent fit rather than exhaustive recurrence search",
            "finite agreement does not establish an infinite recurrence",
            "a held-out failure does not imply a lower bound",
        ],
    }
    result.update(
        _search_contract(
            machine_model="homogeneous linear recurrence over GF(2)",
            digit_order=(
                "binary n is not consumed by the sequential validator; a hypothetical "
                "matrix evaluator would read exponent bits most-significant first"
            ),
            preprocessing_and_advice=(
                "Berlekamp--Massey receives exactly c_0 through c_(train_length-1); "
                "coefficients and initial bits are training-derived advice"
            ),
            search_time="quadratic-time Berlekamp--Massey on the training prefix",
            search_space="O(train_length) bits plus the returned coefficients",
            query_time=(
                "sequential O(n*L), or O(L**3 * log(n+1)) by a separate fixed-matrix "
                "method if the recurrence were proved globally"
            ),
            query_space=(
                "O(L) sequential state, or O(L**2) for the stated dense matrix method"
            ),
        )
    )
    return result


def _window_constraints(
    data: Sequence[int], train_length: int, window: int
) -> tuple[list[int], list[int], dict[str, Any] | None]:
    table = [-1] * (1 << window)
    first_index = [-1] * (1 << window)
    mask = (1 << window) - 1
    context = 0
    for bit in data[:window]:
        context = (context << 1) | bit
    for index in range(window, train_length):
        expected = data[index]
        if table[context] == -1:
            table[context] = expected
            first_index[context] = index
        elif table[context] != expected:
            return table, first_index, {
                "kind": "same_window_has_two_following_bits",
                "window_value": context,
                "window_bits": f"{context:0{window}b}",
                "first_output_index": first_index[context],
                "first_output": table[context],
                "conflicting_output_index": index,
                "conflicting_output": expected,
            }
        context = ((context << 1) & mask) | expected
    return table, first_index, None


def _completed_truth_table(
    constrained: Sequence[int], unseen: Sequence[int], completion_id: int
) -> tuple[int, ...]:
    table = list(constrained)
    for offset, context in enumerate(unseen):
        table[context] = (completion_id >> offset) & 1
    return tuple(table)


def _validate_boolean_recurrence(
    data: Sequence[int],
    train_length: int,
    window: int,
    table: Sequence[int],
    max_reported_errors: int,
) -> dict[str, Any]:
    mask = (1 << window) - 1
    context = 0
    for bit in data[train_length - window : train_length]:
        context = (context << 1) | bit

    def autonomous_predictions() -> Iterable[tuple[int, int]]:
        nonlocal context
        for index in range(train_length, len(data)):
            prediction = table[context]
            yield index, prediction
            context = ((context << 1) & mask) | prediction

    report = _prediction_report(
        data,
        autonomous_predictions(),
        start=train_length,
        stop=len(data),
        max_reported_errors=max_reported_errors,
    )
    report["validation_protocol"] = (
        "autonomous_recursive_rollout_from_the_observed_training_boundary"
    )
    return report


def _truth_table_record(
    table: Sequence[int], max_reported_table_entries: int
) -> dict[str, Any]:
    raw = bytes(table)
    record: dict[str, Any] = {
        "entry_count": len(table),
        "sha256_u8": hashlib.sha256(raw).hexdigest(),
    }
    if len(table) <= max_reported_table_entries:
        record["outputs_by_unsigned_context"] = list(table)
    else:
        record["outputs_omitted_by_report_cap"] = True
    return record


def search_boolean_window_recurrences(
    bits: Iterable[int],
    *,
    train_length: int,
    min_window: int = 1,
    max_window: int = 12,
    start_window: int | None = None,
    start_completion_id: int = 0,
    max_completions: int = 1_000_000,
    max_unseen_contexts: int = 20,
    max_table_entries: int = 1_048_576,
    max_reported_candidates: int = 16,
    max_reported_table_entries: int = 256,
    max_reported_errors: int = 16,
) -> dict[str, Any]:
    """Search arbitrary Boolean recurrences of bounded suffix-window width.

    A model is a complete truth table ``c_n = f(c_(n-w), ..., c_(n-1))``.
    Training contradictions eliminate all truth tables at that width.  When
    training leaves contexts unseen, their outputs are enumerated by a stable
    completion ID and validation is an autonomous rollout.
    """
    data, checked_train = _validated_split(bits, train_length)
    first_window = _integer(min_window, name="min_window", minimum=1)
    last_window = _integer(max_window, name="max_window", minimum=1)
    if last_window < first_window:
        raise ValueError("max_window must be at least min_window")
    if last_window >= checked_train:
        raise ValueError("max_window must be smaller than train_length")
    resume_window = (
        first_window
        if start_window is None
        else _integer(start_window, name="start_window", minimum=1)
    )
    if resume_window < first_window or resume_window > last_window:
        raise ValueError("start_window is outside the requested range")
    resume_completion = _integer(
        start_completion_id, name="start_completion_id", minimum=0
    )
    completion_limit = _integer(
        max_completions, name="max_completions", minimum=1
    )
    unseen_limit = _integer(
        max_unseen_contexts, name="max_unseen_contexts", minimum=0
    )
    table_limit = _integer(
        max_table_entries, name="max_table_entries", minimum=2
    )
    candidate_report_limit = _integer(
        max_reported_candidates, name="max_reported_candidates", minimum=0
    )
    table_report_limit = _integer(
        max_reported_table_entries,
        name="max_reported_table_entries",
        minimum=0,
    )
    error_limit = _integer(
        max_reported_errors, name="max_reported_errors", minimum=0
    )
    if last_window > table_limit.bit_length() - 1:
        raise MemoryError(
            f"width {last_window} exceeds max_table_entries={table_limit} "
            "before truth-table construction"
        )
    if (1 << last_window) > table_limit:
        raise MemoryError(
            f"width {last_window} needs {1 << last_window} truth-table entries, "
            f"exceeding max_table_entries={table_limit}"
        )

    began_at_origin = resume_window == first_window and resume_completion == 0
    examined = 0
    held_out_fit_count = 0
    reported_candidates: list[dict[str, Any]] = []
    window_summaries: list[dict[str, Any]] = []
    checkpoint: dict[str, int] | None = None
    termination = "completed_requested_range"

    for window in range(resume_window, last_window + 1):
        constrained, _first_indices, contradiction = _window_constraints(
            data, checked_train, window
        )
        if contradiction is not None:
            window_summaries.append(
                {
                    "window": window,
                    "truth_table_entry_count": 1 << window,
                    "training_consistent": False,
                    "first_training_counterexample": contradiction,
                    "unseen_context_count": None,
                    "completion_space_size": 0,
                    "completions_examined": 0,
                    "held_out_fit_count": 0,
                    "completed": True,
                }
            )
            if window == resume_window and resume_completion != 0:
                raise ValueError(
                    "start_completion_id must be zero for a training-inconsistent window"
                )
            continue

        unseen = [context for context, value in enumerate(constrained) if value == -1]
        first_completion = resume_completion if window == resume_window else 0
        if len(unseen) > unseen_limit:
            checkpoint = {
                "next_window": window,
                "next_completion_id": first_completion,
            }
            termination = "max_unseen_contexts_exceeded"
            window_summaries.append(
                {
                    "window": window,
                    "truth_table_entry_count": 1 << window,
                    "training_consistent": True,
                    "first_training_counterexample": None,
                    "unseen_context_count": len(unseen),
                    "completion_space_size": None,
                    "completion_space_expression": f"2**{len(unseen)}",
                    "completions_examined": 0,
                    "held_out_fit_count": 0,
                    "completed": False,
                }
            )
            break
        completion_count = 1 << len(unseen)
        if first_completion > completion_count:
            raise ValueError("start_completion_id exceeds this completion space")

        window_examined = 0
        window_fits = 0
        next_completion = first_completion
        for completion_id in range(first_completion, completion_count):
            if examined >= completion_limit:
                checkpoint = {
                    "next_window": window,
                    "next_completion_id": completion_id,
                }
                termination = "max_completions_reached"
                break
            table = _completed_truth_table(constrained, unseen, completion_id)
            validation = _validate_boolean_recurrence(
                data,
                checked_train,
                window,
                table,
                error_limit,
            )
            examined += 1
            window_examined += 1
            next_completion = completion_id + 1
            if validation["exact_on_segment"]:
                held_out_fit_count += 1
                window_fits += 1
            if len(reported_candidates) < candidate_report_limit:
                reported_candidates.append(
                    {
                        "window": window,
                        "completion_id": completion_id,
                        "unseen_context_count": len(unseen),
                        "truth_table": _truth_table_record(
                            table, table_report_limit
                        ),
                        "held_out_validation": validation,
                    }
                )
        window_completed = next_completion >= completion_count
        window_summaries.append(
            {
                "window": window,
                "truth_table_entry_count": 1 << window,
                "training_consistent": True,
                "first_training_counterexample": None,
                "unseen_context_count": len(unseen),
                "completion_space_size": completion_count,
                "start_completion_id": first_completion,
                "stop_completion_id_exclusive": next_completion,
                "completions_examined": window_examined,
                "held_out_fit_count": window_fits,
                "completed": window_completed,
            }
        )
        if termination != "completed_requested_range":
            break

    completed = termination == "completed_requested_range"
    result: dict[str, Any] = {
        "search_name": "bounded_window_boolean_recurrences",
        "parameters": {
            "min_window": first_window,
            "max_window": last_window,
            "start_window": resume_window,
            "start_completion_id": resume_completion,
            "max_completions": completion_limit,
            "max_unseen_contexts": unseen_limit,
            "max_table_entries": table_limit,
            "max_reported_candidates": candidate_report_limit,
            "max_reported_table_entries": table_report_limit,
            "max_reported_errors": error_limit,
        },
        "split": _split_record(len(data), checked_train),
        "enumeration": {
            "order": (
                "window ascending; unseen contexts ascending; completion_id bits "
                "assign those context outputs least-significant bit first"
            ),
            "completions_examined": examined,
            "held_out_fit_count": held_out_fit_count,
            "window_summaries": window_summaries,
            "completed_requested_range": completed,
            "began_at_bounded_space_origin": began_at_origin,
            "completed_full_bounded_space": completed and began_at_origin,
            "termination_reason": termination,
            "checkpoint": checkpoint,
        },
        "reported_training_fit_candidates": reported_candidates,
        "status": "finite-exhaustive" if completed else "inconclusive",
        "proof_scope": (
            "exact constraint check and, when needed, exact completion enumeration "
            "for the reported window widths on this finite split"
        ),
        "interpretation": (
            "A repeated training window with conflicting next bits excludes every "
            "Boolean table at that width on the training prefix. Held-out rollout "
            "then supplies active finite counterexamples to consistent tables."
        ),
        "limitations": [
            "only contiguous suffix-window recurrences are searched",
            "initial window bits and the truth table are training-derived advice",
            "the validator generates sequentially and is not a sublinear random-access algorithm",
            (
                "finite failure does not imply a lower bound or nonexistence "
                "of another representation"
            ),
            "finite agreement does not prove an infinite recurrence",
        ],
    }
    result.update(
        _search_contract(
            machine_model=(
                "deterministic 2**w-state suffix transducer, equivalently an "
                "arbitrary Boolean truth table f:{0,1}**w->{0,1}"
            ),
            digit_order=(
                "binary n is not consumed; n is an implicit sequential counter "
                "whose canonical binary convention remains fixed for reporting"
            ),
            preprocessing_and_advice=(
                "the first w bits and truth-table constraints come only from the "
                "training prefix; unseen outputs are enumerated before validation"
            ),
            search_time=(
                "O(train_length + completions_examined * held_out_length) per width, "
                "with explicit truth-table and completion caps"
            ),
            search_space=(
                "O(sample_count + 2**w + bounded reported output), with the table "
                "cap checked before allocation"
            ),
            query_time=(
                "O(n) transitions from the fixed initial state in the stated "
                "sequential evaluator; if globally valid, separate O(2**w) "
                "finite-state cycle preprocessing could support index skipping"
            ),
            query_space="O(w) mutable state bits plus a read-only 2**w-entry table",
        )
    )
    return result
