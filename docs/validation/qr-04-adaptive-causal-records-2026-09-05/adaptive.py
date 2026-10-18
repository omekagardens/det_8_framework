"""Bounded QR-04 exact adaptive quantum/record executor; not a RET API."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05" / "exact.py"
BASE_SHA = "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _load_exact():
    require(BASE_PATH.is_file() and not BASE_PATH.is_symlink(), "pinned source must be plain file")
    raw = BASE_PATH.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == BASE_SHA, "QR-01 exact source identity differs")
    name = "qr04_pinned_exact"
    require(name not in sys.modules, "QR-04 private module name collision")
    spec = importlib.util.spec_from_file_location(name, BASE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load pinned source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(BASE_PATH), "exec"), module.__dict__)  # noqa: S102
    return module


ex = _load_exact()


@dataclass(frozen=True)
class Event:
    event_id: str
    record_id: str
    support: tuple[int, ...]
    available_records: tuple[str, ...]
    read_records: tuple[str, ...]
    settings: tuple
    policy: tuple

    @property
    def labels(self):
        return tuple(sorted(o.label for o in self.settings[0][1]))


@dataclass(frozen=True)
class Problem:
    qubits: int
    events: tuple[Event, ...]
    precedence: tuple

    @property
    def dimension(self):
        return 2**self.qubits


def _keys(value, keys):
    require(type(value) is dict and set(value) == set(keys), "object differs from QR-04 schema")


def _ids(value, bound):
    require(type(value) is list and len(value) <= bound, "bounded record ID list required")
    result = tuple(ex._identifier(v) for v in value)
    require(result == tuple(sorted(set(result))), "record IDs must be sorted and unique")
    return result


def _contexts(records, writers):
    return tuple(
        tuple(zip(records, labels, strict=True))
        for labels in product(*(writers[rid].labels for rid in records))
    )


def parse(wire):
    _keys(wire, ("schema_version", "qubits", "events", "precedence"))
    require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr04-problem-v1",
        "unsupported QR-04 schema",
    )
    n = wire["qubits"]
    require(type(n) is int and n in (1, 2), "one or two qubits required")
    items = wire["events"]
    require(type(items) is list and 1 <= len(items) <= 4, "one to four events required")
    events, first_settings, policies = [], [], {}
    for item in items:
        _keys(
            item,
            (
                "event_id",
                "record_id",
                "support",
                "available_records",
                "read_records",
                "settings",
                "policy",
            ),
        )
        eid, rid = ex._identifier(item["event_id"]), ex._identifier(item["record_id"])
        require(eid not in policies, "duplicate event ID")
        available, reads = _ids(item["available_records"], 3), _ids(item["read_records"], 2)
        require(set(reads) <= set(available), "read is not available")
        settings = item["settings"]
        require(type(settings) is list and 1 <= len(settings) <= 2, "one or two settings required")
        checked, labels = {}, None
        for setting in settings:
            _keys(setting, ("setting", "outcomes"))
            sid = ex._identifier(setting["setting"])
            require(sid not in checked, "duplicate setting label")
            static = {
                "event_id": eid,
                "record_id": rid,
                "support": item["support"],
                "outcomes": setting["outcomes"],
            }
            instrument = ex.parse_problem(
                {
                    "schema_version": "det8-qr01-problem-v1",
                    "qubits": n,
                    "events": [static],
                    "precedence": [],
                }
            ).events[0]
            setting_labels = tuple(sorted(o.label for o in instrument.outcomes))
            require(labels is None or labels == setting_labels, "setting outcome domains differ")
            labels = setting_labels
            checked[sid] = tuple(sorted(instrument.outcomes, key=lambda o: o.label))
        first_settings.append(
            {
                "event_id": eid,
                "record_id": rid,
                "support": item["support"],
                "outcomes": settings[0]["outcomes"],
            }
        )
        policies[eid] = item["policy"]
        events.append(
            Event(
                eid,
                rid,
                tuple(item["support"]),
                available,
                reads,
                tuple(sorted(checked.items())),
                (),
            )
        )

    graph = ex.parse_problem(
        {
            "schema_version": "det8-qr01-problem-v1",
            "qubits": n,
            "events": first_settings,
            "precedence": wire["precedence"],
        }
    )
    ancestors = {event.event_id: set() for event in events}
    for left, right in graph.precedence:
        ancestors[right].add(left)
    for _ in events:
        for known in ancestors.values():
            known.update(set().union(*(ancestors[a] for a in tuple(known))))
    writers = {event.record_id: event for event in events}
    finished = []
    for event in events:
        require(
            all(
                rid in writers and writers[rid].event_id in ancestors[event.event_id]
                for rid in event.available_records
            ),
            "available record is not written by a strict ancestor",
        )
        expected = set(_contexts(event.read_records, writers))
        rows = policies[event.event_id]
        require(type(rows) is list and len(rows) == len(expected), "policy must cover all contexts")
        policy = {}
        for row in rows:
            _keys(row, ("when", "setting"))
            sid = ex._identifier(row["setting"])
            require(sid in dict(event.settings), "policy names unknown setting")
            pairs = row["when"]
            require(
                type(pairs) is list and len(pairs) == len(event.read_records),
                "invalid policy context size",
            )
            context = []
            for pair in pairs:
                require(type(pair) is list and len(pair) == 2, "policy pair requires two labels")
                context.append((ex._identifier(pair[0]), ex._identifier(pair[1])))
            key = tuple(context)
            require(
                key in expected and key not in policy, "unknown, noncanonical or duplicate context"
            )
            policy[key] = sid
        require(set(policy) == expected, "policy omits a formal context")
        finished.append(
            Event(
                event.event_id,
                event.record_id,
                event.support,
                event.available_records,
                event.read_records,
                event.settings,
                tuple(sorted(policy.items())),
            )
        )
    return Problem(n, tuple(sorted(finished, key=lambda e: e.event_id)), graph.precedence)


def _setting(event, context):
    require(all(rid in context for rid in event.read_records), "required record not present")
    key = tuple((rid, context[rid]) for rid in event.read_records)
    require(key in dict(event.policy), "context outside policy domain")
    return dict(event.policy)[key]


def _execute(problem, order, operator, prior):
    d = problem.dimension
    require(
        len(operator) == d and all(len(row) == d for row in operator), "operator shape mismatch"
    )
    state = {(): operator}
    by_id = {e.event_id: e for e in problem.events}
    for eid in order:
        event = by_id[eid]
        advanced = {}
        for record, branch in state.items():
            context = dict(prior)
            for rid, _, outcome in record:
                require(rid not in context, "duplicate prior/produced record")
                context[rid] = outcome
            require(event.record_id not in context, "record overwrite")
            sid = _setting(event, context)
            for outcome in dict(event.settings)[sid]:
                image = ex.zeros(d)
                for kraus in outcome.kraus:
                    image = ex.add(image, ex.mul(ex.mul(kraus, branch), ex.dagger(kraus)))
                key = tuple(sorted((*record, (event.record_id, sid, outcome.label))))
                require(key not in advanced, "record collision")
                advanced[key] = image
        state = advanced
    return dict(sorted(state.items()))


def execute_operator(problem, order, operator):
    require(type(order) is tuple and order in ex.schedules(problem), "invalid full schedule")
    return _execute(problem, order, operator, {})


def _maps(problem, order, prior):
    d = problem.dimension
    columns = {}
    for k in range(d):
        for l in range(d):
            basis = tuple(
                tuple(ex.ONE if (i, j) == (k, l) else ex.ZERO for j in range(d)) for i in range(d)
            )
            for record, output in _execute(problem, order, basis, prior).items():
                columns.setdefault(record, []).append(tuple(x for row in output for x in row))
    return {
        record: tuple(tuple(cols[j][i] for j in range(d * d)) for i in range(d * d))
        for record, cols in sorted(columns.items())
    }


def _json(value):
    if isinstance(value, (tuple, list)):
        return [_json(v) for v in value]
    if isinstance(value, dict):
        return {key: _json(v) for key, v in value.items()}
    return value


def maps_wire(blocks):
    return [
        {"record": _json(record), "superoperator": ex.matrix_wire(matrix)}
        for record, matrix in sorted(blocks.items())
    ]


def analyze(wire):
    problem = parse(wire)
    orders = ex.schedules(problem)
    by_id = {e.event_id: e for e in problem.events}
    writers = {e.record_id: e for e in problem.events}
    full = [_maps(problem, order, {}) for order in orders]
    comparisons = []
    for order, blocks in zip(orders[1:], full[1:], strict=True):
        diff = _json(ex.difference(full[0], blocks))
        comparisons.append(
            {
                "left": list(orders[0]),
                "right": list(order),
                "equal": diff is None,
                "difference": diff,
            }
        )
    pairs = []
    for left, right in ex.incomparable_pairs(problem):
        read_ids = tuple(sorted(set(by_id[left].read_records) | set(by_id[right].read_records)))
        contexts = []
        for context in _contexts(read_ids, writers):
            prior = dict(context)
            forward, reverse = (
                _maps(problem, (left, right), prior),
                _maps(problem, (right, left), prior),
            )
            diff = _json(ex.difference(forward, reverse))
            contexts.append(
                {
                    "read_context": _json(context),
                    "selected_settings": [
                        [eid, _setting(by_id[eid], prior)] for eid in (left, right)
                    ],
                    "forward": maps_wire(forward),
                    "reverse": maps_wire(reverse),
                    "equal": diff is None,
                    "difference": diff,
                }
            )
        pairs.append(
            {
                "events": [left, right],
                "universal_equal": all(c["equal"] for c in contexts),
                "contexts": contexts,
            }
        )
    pair_contexts = sum(len(pair["contexts"]) for pair in pairs)
    pair_equal = all(pair["universal_equal"] for pair in pairs)
    schedule_equal = all(comparison["equal"] for comparison in comparisons)
    require(
        not pair_equal or schedule_equal, "universal swap certificate contradicts full schedules"
    )
    return {
        "schedules": [
            {"order": list(order), "maps": maps_wire(blocks)}
            for order, blocks in zip(orders, full, strict=True)
        ],
        "schedule_comparisons": comparisons,
        "schedule_equal": schedule_equal,
        "nontrivial_schedule_comparison": len(orders) > 1,
        "pairs": pairs,
        "universal_pair_equal": pair_equal,
        "adaptive_events": [
            e.event_id for e in problem.events if len({sid for _, sid in e.policy}) > 1
        ],
        "counts": {
            "schedules": len(orders),
            "schedule_map_blocks": sum(map(len, full)),
            "incomparable_pairs": len(pairs),
            "pair_contexts": pair_contexts,
            "pair_map_blocks": sum(
                len(c["forward"]) + len(c["reverse"]) for p in pairs for c in p["contexts"]
            ),
            "matrix_unit_executions": problem.dimension**2 * (len(orders) + 2 * pair_contexts),
            "zero_schedule_blocks": sum(
                matrix == ex.zeros(problem.dimension**2)
                for blocks in full
                for matrix in blocks.values()
            ),
        },
    }
