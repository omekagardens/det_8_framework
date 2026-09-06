"""Independent exact superoperator reference for the bounded QR-04 study.

QR-01's SHA-pinned reference supplies instrument validation and direct quantum
superoperators.  This module separately validates causal availability, complete
outcome-reading policies and settings, then composes maps with retained setting
and outcome records.  No operator executor or other QR-04 helper is imported.

Source-reachable schedule comparison and universal formal pair-context
comparison remain distinct.  Neither zero maps nor unreachable formal contexts
are pruned.  Universal pair commutation is sufficient, not necessary, for the
source-reachable schedule certificate.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
from types import ModuleType

ComplexPair = tuple[Fraction, Fraction]
Matrix = tuple[tuple[ComplexPair, ...], ...]
Record = tuple[tuple[str, str, str], ...]
Context = tuple[tuple[str, str], ...]
RecordMaps = dict[Record, Matrix]

QR01_REFERENCE_SHA256 = "d7fab84717c22632e8be7cfd18aca68d439cbf611cf3a47a11abf25a8fca856f"
QR01_REFERENCE_PATH = (
    Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05" / "reference.py"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"QR-04 reference: {message}")


def _load_qr01_reference() -> ModuleType:
    path = QR01_REFERENCE_PATH
    _require(path.is_file() and not path.is_symlink(), "pinned reference must be a plain file")
    raw = path.read_bytes()
    _require(
        hashlib.sha256(raw).hexdigest() == QR01_REFERENCE_SHA256, "pinned reference SHA changed"
    )
    name = "qr04_pinned_reference_qr01"
    _require(name not in sys.modules, "private pinned-reference module name collision")
    specification = importlib.util.spec_from_file_location(name, path)
    _require(
        specification is not None and specification.loader is not None,
        "cannot construct pinned reference file import",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    # Import exactly the verified source bytes, not a second read or stale cache.
    exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


_QR01 = _load_qr01_reference()


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


def _record_ids(value: object, limit: int, context: str) -> tuple[str, ...]:
    _require(type(value) is list and len(value) <= limit, f"invalid bounded {context} list")
    checked = tuple(_label(item, context) for item in value)
    _require(checked == tuple(sorted(set(checked))), f"{context} list is not sorted and unique")
    return checked


def _setting_maps(setting: dict, support: object, qubits: int) -> dict[str, Matrix]:
    wrapper = {
        "schema_version": "det8-qr01-problem-v1",
        "qubits": qubits,
        "events": [
            {
                "event_id": "stage",
                "record_id": "stage",
                "support": support,
                "outcomes": setting["outcomes"],
            }
        ],
        "precedence": [],
    }
    return {
        record[0][1]: matrix
        for record, matrix in _QR01.reference_schedule(wrapper, ("stage",)).items()
    }


def _contexts(reads: tuple[str, ...], domains: dict[str, tuple[str, ...]]) -> tuple[Context, ...]:
    return tuple(
        tuple(zip(reads, assignment, strict=True))
        for assignment in product(*(domains[record] for record in reads))
    )


def _policy(
    value: object, reads: tuple[str, ...], domains: dict, settings: dict
) -> dict[Context, str]:
    expected = _contexts(reads, domains)
    _require(
        type(value) is list and len(value) == len(expected),
        "policy must cover every formal read context exactly",
    )
    result = {}
    for item in value:
        row = _keys(item, {"when", "setting"}, "policy row")
        chosen = _label(row["setting"], "policy setting")
        _require(chosen in settings, "policy names an unknown setting")
        when = row["when"]
        _require(type(when) is list and len(when) == len(reads), "invalid policy context length")
        pairs = []
        for pair in when:
            _require(
                type(pair) is list and len(pair) == 2,
                "policy context requires record/outcome pairs",
            )
            pairs.append((_label(pair[0], "policy record"), _label(pair[1], "policy outcome")))
        context = tuple(pairs)
        _require(
            tuple(record for record, _ in context) == reads,
            "policy context does not use the exact canonical read set",
        )
        _require(
            context in expected and context not in result,
            "unknown or duplicate policy outcome context",
        )
        result[context] = chosen
    _require(set(result) == set(expected), "policy omits a formal read context")
    return dict(sorted(result.items()))


def parse(wire: dict) -> tuple[int, dict, tuple, set]:
    """Independently validate the complete finite wire, including unused settings.

    The returned objects are private research data, not a supported public API.
    Every record read must have a declared available strict-ancestor writer.
    """
    data = _keys(wire, {"schema_version", "qubits", "events", "precedence"}, "problem")
    _require(
        type(data["schema_version"]) is str and data["schema_version"] == "det8-qr04-problem-v1",
        "unsupported schema version",
    )
    qubits = data["qubits"]
    _require(type(qubits) is int and qubits in (1, 2), "one or two qubits required")
    raw_events = data["events"]
    _require(type(raw_events) is list and 1 <= len(raw_events) <= 4, "one to four events required")
    events = {}
    writers = {}
    domains = {}
    for item in raw_events:
        row = _keys(
            item,
            {
                "event_id",
                "record_id",
                "support",
                "available_records",
                "read_records",
                "settings",
                "policy",
            },
            "event",
        )
        event_id = _label(row["event_id"], "event ID")
        record_id = _label(row["record_id"], "record ID")
        _require(
            event_id not in events and record_id not in writers,
            "event IDs and record IDs must each be unique",
        )
        available = _record_ids(row["available_records"], 3, "available record")
        reads = _record_ids(row["read_records"], 2, "read record")
        _require(set(reads) <= set(available), "a read record lacks declared availability")
        setting_rows = row["settings"]
        _require(
            type(setting_rows) is list and 1 <= len(setting_rows) <= 2,
            "one or two settings required",
        )
        settings = {}
        outcome_domain = None
        for setting_wire in setting_rows:
            setting = _keys(setting_wire, {"setting", "outcomes"}, "setting")
            setting_id = _label(setting["setting"], "setting ID")
            _require(setting_id not in settings, "duplicate event setting")
            maps = _setting_maps(setting, row["support"], qubits)
            labels = tuple(sorted(maps))
            _require(
                outcome_domain is None or labels == outcome_domain,
                "all event settings must have the same outcome domain",
            )
            outcome_domain = labels
            settings[setting_id] = maps
        events[event_id] = {
            "record_id": record_id,
            "available": available,
            "reads": reads,
            "settings": dict(sorted(settings.items())),
            "policy_wire": row["policy"],
        }
        writers[record_id] = event_id
        domains[record_id] = outcome_domain
    events = dict(sorted(events.items()))

    edge_rows = data["precedence"]
    _require(type(edge_rows) is list and len(edge_rows) <= 12, "invalid bounded precedence list")
    edges = set()
    for edge in edge_rows:
        _require(type(edge) is list and len(edge) == 2, "precedence edges require two event IDs")
        before, after = _label(edge[0], "precedence event"), _label(edge[1], "precedence event")
        _require(
            before in events and after in events and before != after, "invalid precedence edge"
        )
        _require((before, after) not in edges, "duplicate precedence edge")
        edges.add((before, after))
    orders = tuple(
        order
        for order in permutations(events)
        if all(order.index(before) < order.index(after) for before, after in edges)
    )
    _require(bool(orders), "cyclic precedence")
    ancestors = set(edges)
    for pivot in events:
        for before in events:
            for after in events:
                if (before, pivot) in ancestors and (pivot, after) in ancestors:
                    ancestors.add((before, after))
    for event_id, event in events.items():
        for record in event["available"]:
            _require(record in writers, "available record has no writer")
            _require(
                (writers[record], event_id) in ancestors,
                "available record is not written by a strict ancestor",
            )
        event["policy"] = _policy(
            event.pop("policy_wire"), event["reads"], domains, event["settings"]
        )
        event["domains"] = domains
    return 1 << qubits, events, orders, ancestors


def _identity(dimension: int) -> Matrix:
    return tuple(
        tuple(_QR01._ONE if row == column else _QR01._ZERO for column in range(dimension))
        for row in range(dimension)
    )


def _selected(event: dict, context: Context) -> str:
    known = dict(context)
    _require(all(record in known for record in event["reads"]), "required past outcome is absent")
    key = tuple((record, known[record]) for record in event["reads"])
    _require(key in event["policy"], "past outcomes do not match a declared policy context")
    return event["policy"][key]


def _schedule_maps(dimension: int, events: dict, order: tuple[str, ...]) -> RecordMaps:
    branches: RecordMaps = {(): _identity(dimension * dimension)}
    for event_id in order:
        event = events[event_id]
        updated = {}
        for record, before in branches.items():
            chosen = _selected(event, tuple((rid, outcome) for rid, _, outcome in record))
            for outcome, after in event["settings"][chosen].items():
                _require(all(rid != event["record_id"] for rid, _, _ in record), "record overwrite")
                new_record = tuple(sorted((*record, (event["record_id"], chosen, outcome))))
                _require(new_record not in updated, "record branch collision")
                updated[new_record] = _QR01._compose(after, before)
        branches = dict(sorted(updated.items()))
    return branches


def _pair_maps(first: dict, first_setting: str, second: dict, second_setting: str) -> RecordMaps:
    maps = {}
    for first_outcome, before in first["settings"][first_setting].items():
        for second_outcome, after in second["settings"][second_setting].items():
            record = tuple(
                sorted(
                    (
                        (first["record_id"], first_setting, first_outcome),
                        (second["record_id"], second_setting, second_outcome),
                    )
                )
            )
            _require(record not in maps, "pair record collision")
            maps[record] = _QR01._compose(after, before)
    return dict(sorted(maps.items()))


def _record_wire(record: Record) -> list:
    return [list(triple) for triple in record]


def _matrix_wire(matrix: Matrix) -> list:
    return [[[str(real), str(imag)] for real, imag in row] for row in matrix]


def _maps_wire(maps: RecordMaps) -> list:
    return [
        {"record": _record_wire(record), "superoperator": _matrix_wire(matrix)}
        for record, matrix in sorted(maps.items())
    ]


def _difference(left: RecordMaps, right: RecordMaps) -> dict | None:
    if set(left) != set(right):
        return {
            "kind": "record_inventory",
            "left": [_record_wire(r) for r in sorted(left)],
            "right": [_record_wire(r) for r in sorted(right)],
        }
    for record in sorted(left):
        for row, (left_row, right_row) in enumerate(zip(left[record], right[record], strict=True)):
            for column, (a, b) in enumerate(zip(left_row, right_row, strict=True)):
                if a != b:
                    delta = _QR01._plus(a, (-b[0], -b[1]))
                    return {
                        "kind": "map_entry",
                        "record": _record_wire(record),
                        "output_index": row,
                        "input_index": column,
                        "left": [str(a[0]), str(a[1])],
                        "right": [str(b[0]), str(b[1])],
                        "delta": [str(delta[0]), str(delta[1])],
                    }
    return None


def analyze(wire: dict) -> dict:
    """Return both bounded schedule and universal-context certificates.

    The matrix-unit count describes the independent direct executor's logical
    work under the shared output contract, not this reference's operation count.
    """
    dimension, events, orders, ancestors = parse(wire)
    schedule_maps = [_schedule_maps(dimension, events, order) for order in orders]
    schedules = [
        {"order": list(order), "maps": _maps_wire(maps)}
        for order, maps in zip(orders, schedule_maps, strict=True)
    ]
    comparisons = []
    for order, maps in zip(orders[1:], schedule_maps[1:], strict=True):
        difference = _difference(schedule_maps[0], maps)
        comparisons.append(
            {
                "left": list(orders[0]),
                "right": list(order),
                "equal": difference is None,
                "difference": difference,
            }
        )
    schedule_equal = all(comparison["equal"] for comparison in comparisons)
    pairs = []
    pair_context_count = 0
    pair_block_count = 0
    for first_id, second_id in combinations(events, 2):
        if (first_id, second_id) in ancestors or (second_id, first_id) in ancestors:
            continue
        first, second = events[first_id], events[second_id]
        reads = tuple(sorted(set(first["reads"]) | set(second["reads"])))
        contexts = []
        for context in _contexts(reads, first["domains"]):
            first_setting, second_setting = _selected(first, context), _selected(second, context)
            forward = _pair_maps(first, first_setting, second, second_setting)
            reverse = _pair_maps(second, second_setting, first, first_setting)
            difference = _difference(forward, reverse)
            contexts.append(
                {
                    "read_context": [list(pair) for pair in context],
                    "selected_settings": [[first_id, first_setting], [second_id, second_setting]],
                    "forward": _maps_wire(forward),
                    "reverse": _maps_wire(reverse),
                    "equal": difference is None,
                    "difference": difference,
                }
            )
            pair_context_count += 1
            pair_block_count += len(forward) + len(reverse)
        pairs.append(
            {
                "events": [first_id, second_id],
                "universal_equal": all(context["equal"] for context in contexts),
                "contexts": contexts,
            }
        )
    universal_equal = all(pair["universal_equal"] for pair in pairs)
    _require(
        not universal_equal or schedule_equal, "universal pair certificate failed its implication"
    )
    return {
        "schedules": schedules,
        "schedule_comparisons": comparisons,
        "schedule_equal": schedule_equal,
        "nontrivial_schedule_comparison": len(orders) > 1,
        "pairs": pairs,
        "universal_pair_equal": universal_equal,
        "adaptive_events": [
            event_id for event_id, event in events.items() if len(set(event["policy"].values())) > 1
        ],
        "counts": {
            "schedules": len(orders),
            "schedule_map_blocks": sum(len(maps) for maps in schedule_maps),
            "incomparable_pairs": len(pairs),
            "pair_contexts": pair_context_count,
            "pair_map_blocks": pair_block_count,
            "matrix_unit_executions": dimension
            * dimension
            * (len(orders) + 2 * pair_context_count),
            "zero_schedule_blocks": sum(
                all(value == _QR01._ZERO for row in matrix for value in row)
                for maps in schedule_maps
                for matrix in maps.values()
            ),
        },
    }
