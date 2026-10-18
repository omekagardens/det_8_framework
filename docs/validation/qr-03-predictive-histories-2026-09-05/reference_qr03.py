"""Independent exact predictive-history reference for the finite QR-03 study.

Only the SHA-pinned QR-01 superoperator reference is reused.  No operator
executor or other QR-03 implementation is imported.  This module independently
validates QR-03 tables, extracts real trace functionals, compares homogeneous
quadratics, constructs physical witnesses, and partitions the live histories.

The four real coordinates represent P0, P1, X, Y, not a Bloch vector.  A Bloch
vector (x,y,z) has those coordinates ((1+z)/2,(1-z)/2,x/2,y/2).  Identically
zero CP histories are retained as metadata but excluded from ratio comparison.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from fractions import Fraction
from pathlib import Path
from types import ModuleType

Record = tuple[tuple[str, str], ...]
Functional = tuple[Fraction, Fraction, Fraction, Fraction]

QR01_REFERENCE_SHA256 = "d7fab84717c22632e8be7cfd18aca68d439cbf611cf3a47a11abf25a8fca856f"
QR01_REFERENCE_PATH = (
    Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05" / "reference.py"
)
_MAX_BITS = 4096
_HALF = Fraction(1, 2)
_ZERO = (Fraction(0), Fraction(0))
_MONOMIALS = tuple((i, j) for i in range(4) for j in range(i, 4))
_PROBES = (
    (Fraction(0), Fraction(0), Fraction(0)),
    (_HALF, Fraction(0), Fraction(0)),
    (-_HALF, Fraction(0), Fraction(0)),
    (Fraction(0), _HALF, Fraction(0)),
    (Fraction(0), -_HALF, Fraction(0)),
    (Fraction(0), Fraction(0), _HALF),
    (Fraction(0), Fraction(0), -_HALF),
    (_HALF, _HALF, Fraction(0)),
    (_HALF, Fraction(0), _HALF),
    (Fraction(0), _HALF, _HALF),
)


def _load_qr01_reference() -> ModuleType:
    path = QR01_REFERENCE_PATH
    if not path.is_file() or path.is_symlink():
        raise ValueError("QR-03 reference requires a plain pinned QR-01 source file")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != QR01_REFERENCE_SHA256:
        raise ValueError("QR-03 reference dependency SHA differs from its pin")
    specification = importlib.util.spec_from_file_location("qr03_pinned_reference_qr01", path)
    if specification is None:
        raise ValueError("cannot construct the pinned QR-01 reference file import")
    module = importlib.util.module_from_spec(specification)
    # Only SHA-verified local dependency bytes reach execution.
    exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


_QR01 = _load_qr01_reference()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"QR-03 reference: {message}")


def _guard(value: Fraction) -> Fraction:
    _require(
        abs(value.numerator).bit_length() <= _MAX_BITS
        and value.denominator.bit_length() <= _MAX_BITS,
        "4096-bit rational arithmetic bound exceeded",
    )
    return value


def _add(left: Fraction, right: Fraction) -> Fraction:
    return _guard(left + right)


def _multiply(left: Fraction, right: Fraction) -> Fraction:
    return _guard(left * right)


def _keys(value: object, expected: set[str], context: str) -> dict:
    _require(type(value) is dict and set(value) == expected, f"invalid {context} fields")
    return value


def _label(value: object, context: str) -> str:
    _require(
        type(value) is str
        and 1 <= len(value) <= 128
        and re.fullmatch(r"[A-Za-z0-9_+.-]{1,128}", value) is not None,
        f"invalid bounded {context}",
    )
    return value


def _record(value: object, event_count: int) -> Record:
    _require(type(value) is list and len(value) == event_count, "invalid summary record length")
    decoded = []
    for pair in value:
        _require(type(pair) is list and len(pair) == 2, "invalid summary record pair")
        decoded.append((_label(pair[0], "record ID"), _label(pair[1], "record outcome")))
    result = tuple(decoded)
    _require(result == tuple(sorted(result)), "summary record is not canonical")
    _require(len({item[0] for item in result}) == len(result), "duplicate summary record ID")
    return result


def _decode(wire: object) -> tuple[dict, dict, dict]:
    data = _keys(wire, {"schema_version", "source", "schedule", "futures", "summary"}, "problem")
    _require(
        type(data["schema_version"]) is str and data["schema_version"] == "det8-qr03-problem-v1",
        "unsupported schema version",
    )
    source = _keys(
        data["source"], {"schema_version", "qubits", "events", "precedence"}, "source problem"
    )
    _require(type(source["qubits"]) is int and source["qubits"] == 1, "source must have one qubit")
    _require(
        type(source["events"]) is list and 1 <= len(source["events"]) <= 2,
        "source must have one or two events",
    )
    event_count = len(source["events"])
    schedule = data["schedule"]
    _require(type(schedule) is list and len(schedule) == event_count, "invalid schedule wire")
    for event_id in schedule:
        _label(event_id, "schedule event ID")
    source_maps = _QR01.reference_schedule(source, tuple(schedule))
    _require(1 <= len(source_maps) <= 4, "source record count outside QR-03 scope")

    future_rows = data["futures"]
    _require(
        type(future_rows) is list and 1 <= len(future_rows) <= 3,
        "one to three future settings required",
    )
    future_maps = {}
    seen_settings = set()
    for item in future_rows:
        row = _keys(item, {"setting", "instrument"}, "future row")
        setting = _label(row["setting"], "future setting")
        _require(setting not in seen_settings, "duplicate future setting")
        instrument = _keys(row["instrument"], {"support", "outcomes"}, "future instrument")
        wrapper = {
            "schema_version": "det8-qr01-problem-v1",
            "qubits": 1,
            "events": [
                {
                    "event_id": "stage",
                    "record_id": "stage",
                    "support": instrument["support"],
                    "outcomes": instrument["outcomes"],
                }
            ],
            "precedence": [],
        }
        for record, outcome_map in _QR01.reference_schedule(wrapper, ("stage",)).items():
            future_maps[(setting, record[0][1])] = outcome_map
        seen_settings.add(setting)

    summary_rows = data["summary"]
    _require(
        type(summary_rows) is list and len(summary_rows) == len(source_maps),
        "summary must cover every source record, including zero maps",
    )
    summary = {}
    for item in summary_rows:
        row = _keys(item, {"record", "label"}, "summary row")
        record = _record(row["record"], event_count)
        _require(
            record in source_maps and record not in summary, "unknown or duplicate summary record"
        )
        summary[record] = _label(row["label"], "summary label")
    _require(set(summary) == set(source_maps), "incomplete summary record inventory")
    return dict(sorted(source_maps.items())), dict(sorted(future_maps.items())), summary


def _real(pair: tuple[Fraction, Fraction]) -> Fraction:
    _require(pair[1] == 0, "trace functional is not real on a Hermitian basis element")
    return _guard(pair[0])


def _trace_functional(superoperator: tuple) -> Functional:
    # Row-major output trace selects superoperator rows 0 and 3.  The X and Y
    # basis columns are respectively (0,1,1,0) and (0,-i,+i,0).
    effect = tuple(_QR01._plus(superoperator[0][j], superoperator[3][j]) for j in range(4))
    x_value = _QR01._plus(effect[1], effect[2])
    y_value = _QR01._plus(
        _QR01._times(effect[1], (Fraction(0), Fraction(-1))),
        _QR01._times(effect[2], (Fraction(0), Fraction(1))),
    )
    return (_real(effect[0]), _real(effect[3]), _real(x_value), _real(y_value))


def _quadratic(a: Functional, b: Functional, c: Functional, e: Functional) -> tuple:
    coefficients = []
    for i, j in _MONOMIALS:
        value = _add(_multiply(b[i], c[j]), -_multiply(e[i], a[j]))
        if i != j:
            value = _add(value, _multiply(b[j], c[i]))
            value = _add(value, -_multiply(e[j], a[i]))
        coefficients.append(value)
    return tuple(coefficients)


def _evaluate(functional: Functional, coordinates: Functional) -> Fraction:
    result = Fraction(0)
    for coefficient, coordinate in zip(functional, coordinates, strict=True):
        result = _add(result, _multiply(coefficient, coordinate))
    return result


def _density(bloch: tuple[Fraction, Fraction, Fraction]) -> tuple[Functional, list]:
    x, y, z = bloch
    coordinates = (
        _multiply(_add(Fraction(1), z), _HALF),
        _multiply(_add(Fraction(1), -z), _HALF),
        _multiply(x, _HALF),
        _multiply(y, _HALF),
    )
    a, b, real, imag = coordinates
    wire = [
        [[str(a), "0"], [str(real), str(-imag)]],
        [[str(real), str(imag)], [str(b), "0"]],
    ]
    return coordinates, wire


def _witness(
    question: tuple[str, str], a: Functional, b: Functional, c: Functional, e: Functional
) -> dict:
    for bloch in _PROBES:
        coordinates, density = _density(bloch)
        left_d, right_d = _evaluate(a, coordinates), _evaluate(c, coordinates)
        _require(left_d > 0 and right_d > 0, "live CP history impossible on a full-rank probe")
        left_n, right_n = _evaluate(b, coordinates), _evaluate(e, coordinates)
        _require(
            0 <= left_n <= left_d and 0 <= right_n <= right_d,
            "conditional numerator lies outside its probability bounds",
        )
        left = _guard(left_n / left_d)
        right = _guard(right_n / right_d)
        if left != right:
            return {
                "setting": question[0],
                "outcome": question[1],
                "bloch": [str(value) for value in bloch],
                "density": density,
                "left_history_probability": str(left_d),
                "right_history_probability": str(right_d),
                "left_conditional": str(left),
                "right_conditional": str(right),
                "delta": str(_add(left, -right)),
            }
    raise ValueError(
        "QR-03 reference: nonzero quadratic lacks a witness in the unisolvent probe bank"
    )


def _record_wire(record: Record) -> list:
    return [list(pair) for pair in record]


def _classes(live: list[Record], equal: dict) -> list[list[Record]]:
    remaining = list(live)
    result = []
    while remaining:
        seed = remaining[0]
        members = [
            record for record in remaining if record == seed or equal[tuple(sorted((seed, record)))]
        ]
        for left in members:
            for right in remaining:
                if left == right:
                    continue
                _require(
                    equal[tuple(sorted((left, right)))] == (right in members),
                    "live prediction equality is not transitive",
                )
        result.append(members)
        remaining = [record for record in remaining if record not in members]
    return result


def analyze(wire: dict) -> dict:
    """Return the canonical JSON-compatible QR-03 analysis contract.

    Equality concerns conditional one-step predictions for the stated future
    family at the same supplied initial state.  Neither past probabilities nor
    unlisted future questions are discarded from the mathematical obligation by
    claiming a stronger kind of equivalence.  Zero maps never enter a pair.
    """
    source_maps, future_maps, summary = _decode(wire)
    denominators = {}
    numerators = {}
    histories = []
    live = []
    never = []
    settings = sorted({setting for setting, _ in future_maps})
    for record, source_map in source_maps.items():
        denominator = _trace_functional(source_map)
        denominators[record] = denominator
        rows = {}
        for question, future_map in future_maps.items():
            rows[question] = _trace_functional(_QR01._compose(future_map, source_map))
        numerators[record] = rows
        for setting in settings:
            for coordinate in range(4):
                total = Fraction(0)
                for question, functional in rows.items():
                    if question[0] == setting:
                        total = _add(total, functional[coordinate])
                _require(total == denominator[coordinate], "future outcomes do not sum to history")
        zero_map = all(value == _ZERO for row in source_map for value in row)
        if zero_map:
            _require(
                all(value == 0 for value in denominator), "zero map has nonzero trace functional"
            )
            _require(
                all(value == 0 for row in rows.values() for value in row),
                "zero map has nonzero future numerator",
            )
            never.append(record)
        else:
            mixed_probability = _multiply(_add(denominator[0], denominator[1]), _HALF)
            _require(mixed_probability > 0, "nonzero CP history has nonpositive mixed-state weight")
            live.append(record)
        histories.append(
            {
                "record": _record_wire(record),
                "status": "NEVER_POSSIBLE" if zero_map else "POSSIBLE",
                "denominator": [str(value) for value in denominator],
                "numerators": [
                    {
                        "setting": question[0],
                        "outcome": question[1],
                        "coefficients": [str(value) for value in functional],
                    }
                    for question, functional in rows.items()
                ],
            }
        )

    pairs = []
    equality = {}
    conflicts = []
    for index, left in enumerate(live):
        for right in live[index + 1 :]:
            questions = []
            first_difference = None
            for question in future_maps:
                coefficients = _quadratic(
                    denominators[left],
                    numerators[left][question],
                    denominators[right],
                    numerators[right][question],
                )
                questions.append(
                    {
                        "setting": question[0],
                        "outcome": question[1],
                        "coefficients": [str(value) for value in coefficients],
                    }
                )
                if first_difference is None and any(value != 0 for value in coefficients):
                    first_difference = question
            equal = first_difference is None
            equality[(left, right)] = equal
            witness = (
                None
                if equal
                else _witness(
                    first_difference,
                    denominators[left],
                    numerators[left][first_difference],
                    denominators[right],
                    numerators[right][first_difference],
                )
            )
            pair = {
                "left": _record_wire(left),
                "right": _record_wire(right),
                "equal": equal,
                "questions": questions,
                "witness": witness,
            }
            pairs.append(pair)
            if not equal and summary[left] == summary[right]:
                conflicts.append({**pair, "label": summary[left]})
    return {
        "basis": ["P0", "P1", "X", "Y"],
        "monomials": [list(pair) for pair in _MONOMIALS],
        "histories": histories,
        "pairs": pairs,
        "classes": [
            [_record_wire(record) for record in group] for group in _classes(live, equality)
        ],
        "never_possible": [_record_wire(record) for record in never],
        "candidate_valid": not conflicts,
        "candidate_conflicts": conflicts,
    }
