"""Independent, exact standard-QM reference for the bounded QR-01 study.

This module deliberately imports neither DET8 nor the study's other arithmetic
or execution modules.  It constructs outcome superoperators directly from the
Kraus formula, then composes those superoperators.  Rows and columns use the
row-major operator basis: ``(i, j)`` has index ``i * dimension + j``.

Qubit 0 is the most-significant computational-basis bit.  Record slots are
identified by ``record_id``, not scheduler position.  Zero maps and zero-weight
branches are retained.  No normalization, probability sampling, state-dependent
branch pruning, adaptive callbacks, or floating-point arithmetic is performed.

The wire format has exact keys, canonical rational strings, at most two qubits,
four events, two outcomes per event, and two Kraus operators per outcome.  Input
rational numerators and denominators are bounded by 64 bits; intermediate exact
components by 4096 bits.  Those are computational scope bounds, not restrictions
asserted for physical quantum mechanics.  An empty event set returns the
identity map and is not evidence of nontrivial event independence.
"""

from __future__ import annotations

import re
from fractions import Fraction

ComplexPair = tuple[Fraction, Fraction]
Matrix = tuple[tuple[ComplexPair, ...], ...]
Record = tuple[tuple[str, str], ...]

_ZERO: ComplexPair = (Fraction(0), Fraction(0))
_ONE: ComplexPair = (Fraction(1), Fraction(0))
_INPUT_BITS = 64
_INTERMEDIATE_BITS = 4096
_TOKEN_CHARACTERS = 256
_ID_CHARACTERS = 128


def _bounded(value: Fraction) -> Fraction:
    if (
        abs(value.numerator).bit_length() > _INTERMEDIATE_BITS
        or value.denominator.bit_length() > _INTERMEDIATE_BITS
    ):
        raise ValueError("reference intermediate rational exceeds 4096-bit bound")
    return value


def _plus(left: ComplexPair, right: ComplexPair) -> ComplexPair:
    return (_bounded(left[0] + right[0]), _bounded(left[1] + right[1]))


def _times(left: ComplexPair, right: ComplexPair) -> ComplexPair:
    return (
        _bounded(left[0] * right[0] - left[1] * right[1]),
        _bounded(left[0] * right[1] + left[1] * right[0]),
    )


def _conjugate(value: ComplexPair) -> ComplexPair:
    return (value[0], -value[1])


def _keys(value: object, expected: set[str], context: str) -> dict:
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"{context} must have exactly the specified keys")
    return value


def _identifier(value: object, context: str) -> str:
    if (
        type(value) is not str
        or not 1 <= len(value) <= _ID_CHARACTERS
        or re.fullmatch(r"[A-Za-z0-9_+.-]{1,128}", value) is None
    ):
        raise ValueError(f"{context} must match [A-Za-z0-9_+.-]{{1,128}}")
    return value


def _rational(token: object) -> Fraction:
    if type(token) is not str or not 1 <= len(token) <= _TOKEN_CHARACTERS:
        raise ValueError("reference rational must be a bounded canonical string")
    # Reject exponent notation before Fraction can expand an enormous exponent.
    if re.fullmatch(r"(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?", token) is None:
        raise ValueError("reference rational string is not canonical")
    try:
        value = Fraction(token)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("reference rational is invalid") from exc
    if str(value) != token:
        raise ValueError("reference rational string is not canonical")
    if (
        abs(value.numerator).bit_length() > _INPUT_BITS
        or value.denominator.bit_length() > _INPUT_BITS
    ):
        raise ValueError("reference input rational exceeds 64-bit bound")
    return value


def _wire_matrix(value: object, dimension: int) -> Matrix:
    if type(value) is not list or len(value) != dimension:
        raise ValueError("reference matrix must be a full square wire matrix")
    result = []
    for row in value:
        if type(row) is not list or len(row) != dimension:
            raise ValueError("reference matrix has an invalid row")
        result_row = []
        for cell in row:
            if type(cell) is not list or len(cell) != 2:
                raise ValueError("reference matrix cell must contain real and imaginary strings")
            result_row.append((_rational(cell[0]), _rational(cell[1])))
        result.append(tuple(result_row))
    return tuple(result)


def _basis_bits(index: int, qubits: int, selected: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((index >> (qubits - 1 - qubit)) & 1 for qubit in selected)


def _support_consistent(matrix: Matrix, qubits: int, support: tuple[int, ...]) -> None:
    """Check M = A_support tensor I_complement in the declared bit ordering."""
    outside = tuple(qubit for qubit in range(qubits) if qubit not in support)
    inside_blocks: dict[tuple[tuple[int, ...], tuple[int, ...]], ComplexPair] = {}
    for row in range(len(matrix)):
        for column in range(len(matrix)):
            value = matrix[row][column]
            if _basis_bits(row, qubits, outside) != _basis_bits(column, qubits, outside):
                if value != _ZERO:
                    raise ValueError("reference Kraus operator changes a qubit outside its support")
                continue
            key = (
                _basis_bits(row, qubits, support),
                _basis_bits(column, qubits, support),
            )
            if key in inside_blocks and inside_blocks[key] != value:
                raise ValueError("reference Kraus operator depends on a qubit outside its support")
            inside_blocks[key] = value


def _complete(outcomes: tuple[tuple[str, tuple[Matrix, ...]], ...], dimension: int) -> None:
    """Check every entry of sum_(outcome,Kraus) M-dagger M = I exactly."""
    for row in range(dimension):
        for column in range(dimension):
            total = _ZERO
            for _, kraus_operators in outcomes:
                for operator in kraus_operators:
                    for inner in range(dimension):
                        total = _plus(
                            total,
                            _times(_conjugate(operator[inner][row]), operator[inner][column]),
                        )
            if total != (_ONE if row == column else _ZERO):
                raise ValueError("reference event is not a complete quantum instrument")


def _decode(problem: object, schedule: object) -> tuple[int, dict, tuple[str, ...]]:
    data = _keys(problem, {"schema_version", "qubits", "events", "precedence"}, "problem")
    if type(data["schema_version"]) is not str or data["schema_version"] != "det8-qr01-problem-v1":
        raise ValueError("reference problem schema version is unsupported")
    qubits = data["qubits"]
    if type(qubits) is not int or qubits not in (1, 2):
        raise ValueError("reference problem must contain one or two qubits")
    dimension = 1 << qubits
    if type(data["events"]) is not list or len(data["events"]) > 4:
        raise ValueError("reference problem must contain zero to four events")
    events = {}
    record_ids = set()
    for event_wire in data["events"]:
        event = _keys(
            event_wire,
            {"event_id", "record_id", "support", "outcomes"},
            "event",
        )
        event_id = _identifier(event["event_id"], "event_id")
        record_id = _identifier(event["record_id"], "record_id")
        if event_id in events or record_id in record_ids:
            raise ValueError("reference event IDs and record IDs must each be unique")
        support = event["support"]
        if (
            type(support) is not list
            or len(support) > qubits
            or any(type(qubit) is not int or not 0 <= qubit < qubits for qubit in support)
            or support != sorted(set(support))
        ):
            raise ValueError("reference support must be a sorted list of distinct qubit indices")
        outcome_wires = event["outcomes"]
        if type(outcome_wires) is not list or not 1 <= len(outcome_wires) <= 2:
            raise ValueError("reference event must contain one or two outcomes")
        outcomes = []
        labels = set()
        for outcome_wire in outcome_wires:
            outcome = _keys(outcome_wire, {"label", "kraus"}, "outcome")
            label = _identifier(outcome["label"], "outcome label")
            if label in labels:
                raise ValueError("reference outcome labels must be unique within their event")
            kraus_wires = outcome["kraus"]
            if type(kraus_wires) is not list or not 1 <= len(kraus_wires) <= 2:
                raise ValueError("reference outcome must contain one or two Kraus operators")
            kraus_operators = tuple(_wire_matrix(value, dimension) for value in kraus_wires)
            for operator in kraus_operators:
                _support_consistent(operator, qubits, tuple(support))
            outcomes.append((label, kraus_operators))
            labels.add(label)
        decoded_outcomes = tuple(outcomes)
        _complete(decoded_outcomes, dimension)
        events[event_id] = (record_id, decoded_outcomes)
        record_ids.add(record_id)
    if (
        type(schedule) is not tuple
        or any(type(event_id) is not str for event_id in schedule)
        or len(schedule) != len(events)
        or set(schedule) != set(events)
    ):
        raise ValueError("reference schedule must be a tuple permutation of all event IDs")
    precedence = data["precedence"]
    if type(precedence) is not list or len(precedence) > 12:
        raise ValueError("reference precedence must be a bounded list")
    positions = {event_id: index for index, event_id in enumerate(schedule)}
    edges = set()
    for edge in precedence:
        if (
            type(edge) is not list
            or len(edge) != 2
            or any(type(event_id) is not str or event_id not in events for event_id in edge)
        ):
            raise ValueError("reference precedence edge must name two known events")
        pair = (edge[0], edge[1])
        if pair in edges:
            raise ValueError("reference precedence edges must be distinct")
        if positions[edge[0]] >= positions[edge[1]]:
            raise ValueError("reference schedule violates precedence or precedence is cyclic")
        edges.add(pair)
    return dimension, events, schedule


def _outcome_superoperator(operators: tuple[Matrix, ...], dimension: int) -> Matrix:
    """Directly fill S[(i,j),(k,l)] = sum_a M_a[i,k] conj(M_a[j,l])."""
    super_rows = []
    for output_row in range(dimension):
        for output_column in range(dimension):
            super_row = []
            for input_row in range(dimension):
                for input_column in range(dimension):
                    value = _ZERO
                    for operator in operators:
                        value = _plus(
                            value,
                            _times(
                                operator[output_row][input_row],
                                _conjugate(operator[output_column][input_column]),
                            ),
                        )
                    super_row.append(value)
            super_rows.append(tuple(super_row))
    return tuple(super_rows)


def _compose(after: Matrix, before: Matrix) -> Matrix:
    dimension = len(after)
    rows = []
    for output_index in range(dimension):
        row = []
        for input_index in range(dimension):
            value = _ZERO
            for intermediate_index in range(dimension):
                left = after[output_index][intermediate_index]
                right = before[intermediate_index][input_index]
                if left != _ZERO and right != _ZERO:
                    value = _plus(value, _times(left, right))
            row.append(value)
        rows.append(tuple(row))
    return tuple(rows)


def reference_schedule(problem: dict, schedule: tuple[str, ...]) -> dict[Record, Matrix]:
    """Return exact unnormalized maps for every canonical complete record.

    Each value is a ``d*d`` square superoperator, where ``d = 2**qubits``.
    Every scalar is a ``(Fraction(real), Fraction(imag))`` pair.  The canonical
    record key is the sorted tuple of ``(record_id, outcome_label)`` pairs.
    All input validation is local to this independent reference implementation.
    """
    dimension, events, checked_schedule = _decode(problem, schedule)
    operator_dimension = dimension * dimension
    identity = tuple(
        tuple(_ONE if row == column else _ZERO for column in range(operator_dimension))
        for row in range(operator_dimension)
    )
    branches: dict[Record, Matrix] = {(): identity}
    for event_id in checked_schedule:
        record_id, outcomes = events[event_id]
        outcome_maps = tuple(
            (label, _outcome_superoperator(operators, dimension)) for label, operators in outcomes
        )
        updated_branches = {}
        for record, before in branches.items():
            for label, after in outcome_maps:
                key = tuple(sorted((*record, (record_id, label))))
                updated_branches[key] = _compose(after, before)
        branches = updated_branches
    return dict(sorted(branches.items()))


def apply_superoperator(superoperator: Matrix, input_matrix_wire: list) -> Matrix:
    """Apply an exact reference map to an arbitrary bounded wire operator.

    Inputs need not be density matrices: operator-basis inputs are useful for
    comparing the complete linear maps, rather than selected physical states.
    This helper does not assert positivity or trace preservation of a supplied
    superoperator; the caller may supply a single trace-decreasing branch map.
    """
    if type(superoperator) is not tuple or len(superoperator) not in (4, 16):
        raise ValueError("reference superoperator must describe one or two qubits")
    operator_dimension = len(superoperator)
    dimension = 2 if operator_dimension == 4 else 4
    for row in superoperator:
        if type(row) is not tuple or len(row) != operator_dimension:
            raise ValueError("reference superoperator has an invalid row")
        for cell in row:
            if (
                type(cell) is not tuple
                or len(cell) != 2
                or any(type(component) is not Fraction for component in cell)
            ):
                raise ValueError("reference superoperator must contain exact Fraction pairs")
            for component in cell:
                _bounded(component)
    input_matrix = _wire_matrix(input_matrix_wire, dimension)
    rows = []
    for output_row in range(dimension):
        row = []
        for output_column in range(dimension):
            value = _ZERO
            for input_row in range(dimension):
                for input_column in range(dimension):
                    value = _plus(
                        value,
                        _times(
                            superoperator[output_row * dimension + output_column][
                                input_row * dimension + input_column
                            ],
                            input_matrix[input_row][input_column],
                        ),
                    )
            row.append(value)
        rows.append(tuple(row))
    return tuple(rows)
