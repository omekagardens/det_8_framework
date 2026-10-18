"""QR-01 research executor: exact outcome-resolved quantum/record operations.

Standalone finite research code, not a det8.ret API or a physical theory.
Qubit 0 is the most-significant computational-basis bit. No sampling occurs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations

MAX_BITS = 4096


@dataclass(frozen=True)
class C:
    real: Fraction = Fraction(0)
    imag: Fraction = Fraction(0)

    def __post_init__(self):
        for value in (self.real, self.imag):
            if type(value) is not Fraction:
                raise TypeError("exact complex components must be Fractions")
            if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > MAX_BITS:
                raise ValueError("internal rational arithmetic bound exceeded")

    def __add__(self, other):
        if not isinstance(other, C):
            return NotImplemented
        return C(self.real + other.real, self.imag + other.imag)

    def __neg__(self):
        return C(-self.real, -self.imag)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if not isinstance(other, C):
            return NotImplemented
        return C(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def conjugate(self):
        return C(self.real, -self.imag)

    def wire(self):
        return [str(self.real), str(self.imag)]


def q(real=0, imag=0):
    if any(type(v) not in (int, Fraction) for v in (real, imag)):
        raise TypeError("q accepts integers or Fractions, never floats or booleans")
    return C(Fraction(real), Fraction(imag))


ZERO = q()
ONE = q(1)
Matrix = tuple[tuple[C, ...], ...]
Record = tuple[tuple[str, str], ...]


def zeros(d: int) -> Matrix:
    return tuple(tuple(ZERO for _ in range(d)) for _ in range(d))


def identity(d: int) -> Matrix:
    return tuple(tuple(ONE if i == j else ZERO for j in range(d)) for i in range(d))


def add(a: Matrix, b: Matrix) -> Matrix:
    if len(a) != len(b) or any(len(x) != len(y) for x, y in zip(a, b, strict=True)):
        raise ValueError("matrix shape mismatch")
    return tuple(
        tuple(x + y for x, y in zip(ar, br, strict=True)) for ar, br in zip(a, b, strict=True)
    )


def scale(a: Matrix, value: C) -> Matrix:
    return tuple(tuple(value * x for x in row) for row in a)


def mul(a: Matrix, b: Matrix) -> Matrix:
    d = len(a)
    if len(b) != d or any(len(row) != d for row in (*a, *b)):
        raise ValueError("square matrix shape mismatch")
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(d)), ZERO) for j in range(d)) for i in range(d)
    )


def dagger(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i].conjugate() for j in range(len(a))) for i in range(len(a)))


def tensor(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(a[i][j] * b[k][l] for j in range(len(a)) for l in range(len(b)))
        for i in range(len(a))
        for k in range(len(b))
    )


def trace(a: Matrix) -> C:
    return sum((a[i][i] for i in range(len(a))), ZERO)


def matrix_wire(a: Matrix):
    return [[value.wire() for value in row] for row in a]


def _keys(value, expected):
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError("object fields differ from the fixed research schema")


def _identifier(value):
    if type(value) is not str or re.fullmatch(r"[A-Za-z0-9_+.-]{1,128}", value) is None:
        raise ValueError("invalid bounded identifier")
    return value


def _fraction(token):
    if (
        type(token) is not str
        or len(token) > 256
        or re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", token) is None
    ):
        raise ValueError("invalid rational token")
    try:
        value = Fraction(token)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational token") from exc
    if (
        str(value) != token
        or max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > 64
    ):
        raise ValueError("noncanonical or oversized rational token")
    return value


def decode_matrix(value, d):
    if type(value) is not list or len(value) != d:
        raise ValueError("matrix dimension differs from qubit count")
    result = []
    for row in value:
        if type(row) is not list or len(row) != d:
            raise ValueError("matrix must be square")
        entries = []
        for cell in row:
            if type(cell) is not list or len(cell) != 2:
                raise ValueError("complex scalar requires two rational tokens")
            entries.append(C(_fraction(cell[0]), _fraction(cell[1])))
        result.append(tuple(entries))
    return tuple(result)


@dataclass(frozen=True)
class Outcome:
    label: str
    kraus: tuple[Matrix, ...]


@dataclass(frozen=True)
class Event:
    event_id: str
    record_id: str
    support: tuple[int, ...]
    outcomes: tuple[Outcome, ...]


@dataclass(frozen=True)
class Problem:
    qubits: int
    events: tuple[Event, ...]
    precedence: tuple[tuple[str, str], ...]

    @property
    def dimension(self):
        return 2**self.qubits


def _support_check(matrix, support, qubits):
    """Prove M = M_support tensor I_spectator by entrywise equalities."""
    spectators = tuple(i for i in range(qubits) if i not in support)

    def bits(index, selected):
        return tuple((index >> (qubits - 1 - bit)) & 1 for bit in selected)

    local = {}
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if bits(i, spectators) != bits(j, spectators):
                if value != ZERO:
                    raise ValueError("Kraus operator violates declared support")
            else:
                key = (bits(i, support), bits(j, support))
                if key in local and local[key] != value:
                    raise ValueError("Kraus operator depends on spectator state")
                local[key] = value


def parse_problem(wire) -> Problem:
    _keys(wire, ("schema_version", "qubits", "events", "precedence"))
    if type(wire["schema_version"]) is not str or wire["schema_version"] != "det8-qr01-problem-v1":
        raise ValueError("unsupported research schema")
    n = wire["qubits"]
    if type(n) is not int or n not in (1, 2):
        raise ValueError("only one or two qubits are supported")
    items = wire["events"]
    if type(items) is not list or len(items) > 4:
        raise ValueError("at most four events are supported")
    events = []
    for item in items:
        _keys(item, ("event_id", "record_id", "support", "outcomes"))
        eid, rid = _identifier(item["event_id"]), _identifier(item["record_id"])
        support = item["support"]
        if (
            type(support) is not list
            or len(support) > n
            or any(type(i) is not int or i not in range(n) for i in support)
            or sorted(set(support)) != support
        ):
            raise ValueError("support must be unique sorted qubit indices")
        choices = item["outcomes"]
        if type(choices) is not list or not 1 <= len(choices) <= 2:
            raise ValueError("one or two outcomes required")
        outcomes = []
        completeness = zeros(2**n)
        for choice in choices:
            _keys(choice, ("label", "kraus"))
            label = _identifier(choice["label"])
            operators = choice["kraus"]
            if type(operators) is not list or not 1 <= len(operators) <= 2:
                raise ValueError("one or two Kraus operators per outcome required")
            matrices = tuple(decode_matrix(m, 2**n) for m in operators)
            for matrix in matrices:
                _support_check(matrix, tuple(support), n)
                completeness = add(completeness, mul(dagger(matrix), matrix))
            outcomes.append(Outcome(label, matrices))
        if len({o.label for o in outcomes}) != len(outcomes):
            raise ValueError("duplicate outcome label")
        if completeness != identity(2**n):
            raise ValueError("instrument is not exactly complete")
        events.append(Event(eid, rid, tuple(support), tuple(outcomes)))
    if len({e.event_id for e in events}) != len(events):
        raise ValueError("duplicate event ID")
    if len({e.record_id for e in events}) != len(events):
        raise ValueError("record writes must be unique")
    edges = wire["precedence"]
    if type(edges) is not list or len(edges) > 12:
        raise ValueError("invalid bounded precedence list")
    checked = []
    ids = {e.event_id for e in events}
    for edge in edges:
        if (
            type(edge) is not list
            or len(edge) != 2
            or any(type(i) is not str or i not in ids for i in edge)
            or edge[0] == edge[1]
        ):
            raise ValueError("invalid precedence edge")
        checked.append(tuple(edge))
    if len(set(checked)) != len(checked):
        raise ValueError("duplicate precedence edge")
    problem = Problem(n, tuple(events), tuple(checked))
    if not schedules(problem):
        raise ValueError("cyclic precedence")
    return problem


def schedules(problem: Problem):
    return tuple(
        order
        for order in permutations(sorted(e.event_id for e in problem.events))
        if all(order.index(a) < order.index(b) for a, b in problem.precedence)
    )


def execute_operator(problem: Problem, order: tuple[str, ...], operator: Matrix):
    """Apply a valid schedule to any exact operator, including non-Hermitian basis units."""
    if order not in schedules(problem):
        raise ValueError("invalid full schedule")
    d = problem.dimension
    if len(operator) != d or any(len(row) != d for row in operator):
        raise ValueError("input operator dimension mismatch")
    state: dict[Record, Matrix] = {(): operator}
    by_id = {event.event_id: event for event in problem.events}
    for eid in order:
        event = by_id[eid]
        advanced = {}
        for record, branch in state.items():
            for outcome in event.outcomes:
                image = zeros(d)
                for kraus in outcome.kraus:
                    image = add(image, mul(mul(kraus, branch), dagger(kraus)))
                key = tuple(sorted((*record, (event.record_id, outcome.label))))
                if key in advanced:
                    raise ValueError("record collision")
                advanced[key] = image  # Zero branches remain represented.
        state = advanced
    return dict(sorted(state.items()))


def operator_maps(problem: Problem, order):
    """Recover full superoperators from their action on all d² matrix units."""
    d = problem.dimension
    columns = {}
    for k in range(d):
        for l in range(d):
            basis = tuple(
                tuple(ONE if (i, j) == (k, l) else ZERO for j in range(d)) for i in range(d)
            )
            outputs = execute_operator(problem, order, basis)
            for key, output in outputs.items():
                columns.setdefault(key, []).append(tuple(x for row in output for x in row))
    return {
        key: tuple(tuple(cols[j][i] for j in range(d * d)) for i in range(d * d))
        for key, cols in columns.items()
    }


def incomparable_pairs(problem):
    reachable = set(problem.precedence)
    ids = sorted(e.event_id for e in problem.events)
    for pivot in ids:
        reachable |= {
            (a, b) for a in ids for b in ids if (a, pivot) in reachable and (pivot, b) in reachable
        }
    return tuple(
        (a, b)
        for i, a in enumerate(ids)
        for b in ids[i + 1 :]
        if (a, b) not in reachable and (b, a) not in reachable
    )


def difference(left, right):
    if set(left) != set(right):
        return {"kind": "record_inventory", "left": sorted(left), "right": sorted(right)}
    for record in sorted(left):
        for i, (ar, br) in enumerate(zip(left[record], right[record], strict=True)):
            for j, (a, b) in enumerate(zip(ar, br, strict=True)):
                if a != b:
                    return {
                        "kind": "map_entry",
                        "record": record,
                        "output_index": i,
                        "input_index": j,
                        "left": a.wire(),
                        "right": b.wire(),
                        "delta": (a - b).wire(),
                    }
    return None


def total_map(blocks):
    first = next(iter(blocks.values()))
    result = zeros(len(first))
    for block in blocks.values():
        result = add(result, block)
    return result


def maps_wire(blocks):
    return [
        {"record": list(key), "superoperator": matrix_wire(value)}
        for key, value in sorted(blocks.items())
    ]
