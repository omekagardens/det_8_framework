"""Exact conditional-prediction equivalence for bounded one-qubit histories."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05" / "exact.py"
BASE_SHA = "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _load_exact():
    require(
        BASE_PATH.is_file() and not BASE_PATH.is_symlink(), "pinned dependency must be a plain file"
    )
    raw = BASE_PATH.read_bytes()
    require(
        hashlib.sha256(raw).hexdigest() == BASE_SHA, "QR-01 exact source differs from pinned bytes"
    )
    name = "qr03_pinned_exact"
    require(name not in sys.modules, "QR-03 private module name collision")
    spec = importlib.util.spec_from_file_location(name, BASE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load pinned QR-01 source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    # Execute only these exact SHA-verified local dependency bytes.
    exec(compile(raw, str(BASE_PATH), "exec"), module.__dict__)  # noqa: S102
    return module


ex = _load_exact()
BASIS = ("P0", "P1", "X", "Y")
MONOMIALS = tuple((i, j) for i in range(4) for j in range(i, 4))
HALF = Fraction(1, 2)
PROBES = (
    (0, 0, 0),
    (HALF, 0, 0),
    (-HALF, 0, 0),
    (0, HALF, 0),
    (0, -HALF, 0),
    (0, 0, HALF),
    (0, 0, -HALF),
    (HALF, HALF, 0),
    (HALF, 0, HALF),
    (0, HALF, HALF),
)


def _keys(value, keys):
    require(
        type(value) is dict and set(value) == set(keys), "object differs from fixed QR-03 schema"
    )


def _instrument(value):
    _keys(value, ("support", "outcomes"))
    return ex.parse_problem(
        {
            "schema_version": "det8-qr01-problem-v1",
            "qubits": 1,
            "events": [{"event_id": "stage", "record_id": "stage", **value}],
            "precedence": [],
        }
    )


def _record(value, expected):
    require(type(value) is list and 1 <= len(value) <= 2, "bounded canonical record list required")
    pairs = []
    for pair in value:
        require(type(pair) is list and len(pair) == 2, "record slots require two labels")
        pairs.append((ex._identifier(pair[0]), ex._identifier(pair[1])))
    result = tuple(pairs)
    require(
        result == tuple(sorted(result)) and result in expected, "unknown or noncanonical record"
    )
    return result


def parse(wire):
    _keys(wire, ("schema_version", "source", "schedule", "futures", "summary"))
    require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr03-problem-v1",
        "unsupported QR-03 schema",
    )
    source = ex.parse_problem(wire["source"])
    require(
        source.qubits == 1 and 1 <= len(source.events) <= 2,
        "QR-03 requires one qubit and one/two source events",
    )
    order = wire["schedule"]
    require(
        type(order) is list
        and len(order) == len(source.events)
        and all(type(v) is str for v in order),
        "bounded full source schedule required",
    )
    order = tuple(order)
    require(order in ex.schedules(source), "source schedule is not permitted")
    items = wire["futures"]
    require(type(items) is list and 1 <= len(items) <= 3, "one to three future settings required")
    futures = {}
    for item in items:
        _keys(item, ("setting", "instrument"))
        setting = ex._identifier(item["setting"])
        require(setting not in futures, "duplicate future setting")
        futures[setting] = _instrument(item["instrument"])
    expected = {
        tuple(
            sorted(
                (event.record_id, outcome.label)
                for event, outcome in zip(source.events, choices, strict=True)
            )
        )
        for choices in product(*(event.outcomes for event in source.events))
    }
    table = wire["summary"]
    require(
        type(table) is list and len(table) == len(expected),
        "summary must cover every source history",
    )
    summary = {}
    for item in table:
        _keys(item, ("record", "label"))
        record = _record(item["record"], expected)
        require(record not in summary, "duplicate summary record")
        summary[record] = ex._identifier(item["label"])
    require(set(summary) == expected, "summary omits a source history")
    return source, order, dict(sorted(futures.items())), summary


def hermitian_basis():
    return (
        ((ex.ONE, ex.ZERO), (ex.ZERO, ex.ZERO)),
        ((ex.ZERO, ex.ZERO), (ex.ZERO, ex.ONE)),
        ((ex.ZERO, ex.ONE), (ex.ONE, ex.ZERO)),
        ((ex.ZERO, ex.q(0, -1)), (ex.q(0, 1), ex.ZERO)),
    )


def _real_trace(matrix):
    value = ex.trace(matrix)
    require(value.imag == 0, "Hermitian output acquired a complex trace")
    return value.real


def _bounded(value):
    ex.q(value)  # Reuse the exact component-size guard, never a float conversion.
    return value


def coefficients(wire):
    source, order, futures, summary = parse(wire)
    rows, images = {}, {}
    for basis in hermitian_basis():
        for record, state in ex.execute_operator(source, order, basis).items():
            row = rows.setdefault(record, {"denominator": [], "numerators": {}})
            row["denominator"].append(_real_trace(state))
            images.setdefault(record, []).append(state)
            for setting, future in futures.items():
                outputs = ex.execute_operator(future, ("stage",), state)
                for future_record, output in outputs.items():
                    question = (setting, future_record[0][1])
                    row["numerators"].setdefault(question, []).append(_real_trace(output))
    require(
        [sum(row["denominator"][i] for row in rows.values()) for i in range(4)] == [1, 1, 0, 0],
        "source history effects do not sum to trace",
    )
    for record, row in rows.items():
        zero = all(state == ex.zeros(2) for state in images[record])
        require(
            zero == all(value == 0 for value in row["denominator"]),
            "CP zero-map/effect inconsistency",
        )
        row["status"] = "NEVER_POSSIBLE" if zero else "POSSIBLE"
        if not zero:
            require(
                (row["denominator"][0] + row["denominator"][1]) / 2 > 0,
                "nonzero CP history is impossible on maximally mixed state",
            )
        for setting in futures:
            selected = [values for (u, _), values in row["numerators"].items() if u == setting]
            require(
                [sum(values[i] for values in selected) for i in range(4)] == row["denominator"],
                "future outcome functionals do not sum to history effect",
            )
    return dict(sorted(rows.items())), summary


def polynomial(a, b, c, e):
    return tuple(
        _bounded(
            b[i] * c[j] - e[i] * a[j]
            if i == j
            else b[i] * c[j] + b[j] * c[i] - e[i] * a[j] - e[j] * a[i]
        )
        for i, j in MONOMIALS
    )


def _dot(coefficients, coordinates):
    return _bounded(
        sum((a * b for a, b in zip(coefficients, coordinates, strict=True)), Fraction(0))
    )


def probe_state(bloch):
    x, y, z = (Fraction(v) for v in bloch)
    coordinates = ((1 + z) / 2, (1 - z) / 2, x / 2, y / 2)
    state = (
        (ex.q(coordinates[0]), ex.q(x / 2, -y / 2)),
        (ex.q(x / 2, y / 2), ex.q(coordinates[1])),
    )
    require(x * x + y * y + z * z < 1, "witness bank must be strictly full rank")
    return coordinates, state


def _witness(left, right, question):
    for bloch in PROBES:
        coordinates, state = probe_state(bloch)
        dh, dk = _dot(left["denominator"], coordinates), _dot(right["denominator"], coordinates)
        require(dh > 0 and dk > 0, "live history vanished on a full-rank probe")
        nh = _dot(left["numerators"][question], coordinates)
        nk = _dot(right["numerators"][question], coordinates)
        require(0 <= nh <= dh and 0 <= nk <= dk, "invalid conditional probability")
        ph, pk = _bounded(nh / dh), _bounded(nk / dk)
        if ph != pk:
            return {
                "setting": question[0],
                "outcome": question[1],
                "bloch": [str(Fraction(v)) for v in bloch],
                "density": ex.matrix_wire(state),
                "left_history_probability": str(dh),
                "right_history_probability": str(dk),
                "left_conditional": str(ph),
                "right_conditional": str(pk),
                "delta": str(_bounded(ph - pk)),
            }
    raise ValueError("nonzero polynomial has no witness in the unisolvent full-rank bank")


def record_wire(record):
    return [list(pair) for pair in record]


def analyze(wire):
    rows, summary = coefficients(wire)
    live = [record for record, row in rows.items() if row["status"] == "POSSIBLE"]
    never = [record for record, row in rows.items() if row["status"] == "NEVER_POSSIBLE"]
    pairs, equality, conflicts = [], {}, []
    for h, k in combinations(live, 2):
        left, right = rows[h], rows[k]
        questions, first_failure = [], None
        for question in sorted(left["numerators"]):
            values = polynomial(
                left["denominator"],
                left["numerators"][question],
                right["denominator"],
                right["numerators"][question],
            )
            questions.append(
                {
                    "setting": question[0],
                    "outcome": question[1],
                    "coefficients": [str(v) for v in values],
                }
            )
            if any(values) and first_failure is None:
                first_failure = question
        equal = first_failure is None
        equality[h, k] = equality[k, h] = equal
        pair = {
            "left": record_wire(h),
            "right": record_wire(k),
            "equal": equal,
            "questions": questions,
            "witness": None if equal else _witness(left, right, first_failure),
        }
        pairs.append(pair)
        if not equal and summary[h] == summary[k]:
            conflicts.append({**pair, "label": summary[h]})
    classes, unused = [], set(live)
    for record in live:
        if record not in unused:
            continue
        members = [
            other for other in live if other == record or equality.get((record, other), False)
        ]
        require(all(other in unused for other in members), "equivalence classes overlap")
        require(
            all(equality[a, b] for a, b in combinations(members, 2)),
            "equivalence is not transitive",
        )
        unused.difference_update(members)
        classes.append([record_wire(other) for other in members])
    histories = [
        {
            "record": record_wire(record),
            "status": row["status"],
            "denominator": [str(v) for v in row["denominator"]],
            "numerators": [
                {"setting": u, "outcome": y, "coefficients": [str(v) for v in values]}
                for (u, y), values in sorted(row["numerators"].items())
            ],
        }
        for record, row in rows.items()
    ]
    return {
        "basis": list(BASIS),
        "monomials": [list(pair) for pair in MONOMIALS],
        "histories": histories,
        "pairs": pairs,
        "classes": classes,
        "never_possible": [record_wire(record) for record in never],
        "candidate_valid": not conflicts,
        "candidate_conflicts": conflicts,
    }
