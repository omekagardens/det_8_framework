"""QR-02 exact operator execution with explicit, deterministic record grouping.

Trusted finite research helpers, not a RET API. QR-01 is reused read-only.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05" / "exact.py"
BASE_SHA = "4238096b5de4b6aeeee2559b5200e0458a5635be88c06aa960bd50d0c2e3db56"


def _load_exact():
    raw = BASE_PATH.read_bytes()
    if BASE_PATH.is_symlink() or hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise ValueError("QR-01 exact source differs from the pinned research dependency")
    name = "qr02_pinned_exact"
    if name in sys.modules:
        raise ValueError("QR-02 exact module name collision")
    spec = importlib.util.spec_from_file_location(name, BASE_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load pinned QR-01 exact source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    # Only the exact SHA-pinned local dependency bytes can reach execution.
    exec(compile(raw, str(BASE_PATH), "exec"), module.__dict__)  # noqa: S102
    return module


ex = _load_exact()


def _keys(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError("object fields differ from the fixed QR-02 schema")


def _instrument(wire, qubits):
    _keys(wire, ("support", "outcomes"))
    return ex.parse_problem(
        {
            "schema_version": "det8-qr01-problem-v1",
            "qubits": qubits,
            "events": [{"event_id": "stage", "record_id": "stage", **wire}],
            "precedence": [],
        }
    )


def _table(items, label_field, value_field):
    if type(items) is not list or not 1 <= len(items) <= 2:
        raise ValueError("QR-02 tables require one or two entries")
    result = {}
    for item in items:
        _keys(item, (label_field, value_field))
        label = ex._identifier(item[label_field])
        if label in result:
            raise ValueError("duplicate QR-02 table key")
        result[label] = item[value_field]
    return result


@dataclass(frozen=True)
class Parsed:
    qubits: int
    source: ex.Problem
    groups: tuple[tuple[str, str], ...]
    fine_future: tuple[tuple[str, ex.Problem], ...]
    coarse_future: tuple[tuple[str, ex.Problem], ...]

    @property
    def dimension(self):
        return 2**self.qubits


def parse(wire):
    _keys(wire, ("schema_version", "qubits", "source", "groups", "fine_future", "coarse_future"))
    if type(wire["schema_version"]) is not str or wire["schema_version"] != "det8-qr02-problem-v1":
        raise ValueError("unsupported QR-02 schema")
    n = wire["qubits"]
    if type(n) is not int or n not in (1, 2):
        raise ValueError("QR-02 supports one or two qubits")
    source = _instrument(wire["source"], n)
    fine_labels = {o.label for o in source.events[0].outcomes}
    groups = _table(wire["groups"], "fine", "coarse")
    for label in groups.values():
        ex._identifier(label)
    if set(groups) != fine_labels:
        raise ValueError("group map must cover every source outcome exactly")
    fine = _table(wire["fine_future"], "fine", "instrument")
    coarse = _table(wire["coarse_future"], "coarse", "instrument")
    if set(fine) != fine_labels or set(coarse) != set(groups.values()):
        raise ValueError("future tables must match their entire fine/coarse label inventories")
    fine = {label: _instrument(value, n) for label, value in fine.items()}
    coarse = {label: _instrument(value, n) for label, value in coarse.items()}
    inventories = [
        {o.label for o in p.events[0].outcomes} for p in (*fine.values(), *coarse.values())
    ]
    if any(labels != inventories[0] for labels in inventories):
        raise ValueError("all future instruments require the same fixed outcome labels")
    return Parsed(
        n,
        source,
        tuple(sorted(groups.items())),
        tuple(sorted(fine.items())),
        tuple(sorted(coarse.items())),
    )


def _apply(instrument, operator):
    return {
        record[0][1]: value
        for record, value in ex.execute_operator(instrument, ("stage",), operator).items()
    }


def propagate(parsed, operator):
    """Return four state-block bundles for any exact input operator (not only states)."""
    fine_source = _apply(parsed.source, operator)
    groups = dict(parsed.groups)
    fine_future, coarse_future = dict(parsed.fine_future), dict(parsed.coarse_future)
    coarse_source = {z: ex.zeros(parsed.dimension) for z in sorted(set(groups.values()))}
    fine_then_forget = {}
    for x, branch in fine_source.items():
        z = groups[x]
        coarse_source[z] = ex.add(coarse_source[z], branch)
        for y, output in _apply(fine_future[x], branch).items():
            key = (("coarse", z), ("future", y))
            fine_then_forget[key] = ex.add(
                fine_then_forget.get(key, ex.zeros(parsed.dimension)), output
            )
    forget_then_candidate = {}
    for z, branch in coarse_source.items():
        for y, output in _apply(coarse_future[z], branch).items():
            forget_then_candidate[(("coarse", z), ("future", y))] = output
    return {
        "source_fine": {(("fine", x),): v for x, v in sorted(fine_source.items())},
        "source_coarse": {(("coarse", z),): v for z, v in sorted(coarse_source.items())},
        "fine_then_forget": dict(sorted(fine_then_forget.items())),
        "forget_then_candidate": dict(sorted(forget_then_candidate.items())),
    }


def maps(wire):
    """Recover complete reachable maps from all initial matrix units, plus all-CQ maps."""
    parsed = parse(wire)
    d = parsed.dimension
    columns = {}
    for k in range(d):
        for l in range(d):
            basis = tuple(tuple(ex.q(int((i, j) == (k, l))) for j in range(d)) for i in range(d))
            for bundle, blocks in propagate(parsed, basis).items():
                for record, state in blocks.items():
                    columns.setdefault(bundle, {}).setdefault(record, []).append(
                        tuple(value for row in state for value in row)
                    )
    result = {
        bundle: {
            record: tuple(tuple(cols[j][i] for j in range(d * d)) for i in range(d * d))
            for record, cols in blocks.items()
        }
        for bundle, blocks in columns.items()
    }
    fine_maps = {x: ex.operator_maps(inst, ("stage",)) for x, inst in parsed.fine_future}
    coarse_maps = {z: ex.operator_maps(inst, ("stage",)) for z, inst in parsed.coarse_future}
    result["unrestricted_fine_future"] = {}
    result["unrestricted_coarse_future"] = {}
    for x, z in parsed.groups:
        for record, future_map in fine_maps[x].items():
            key = (("fine", x), ("future", record[0][1]))
            result["unrestricted_fine_future"][key] = future_map
            result["unrestricted_coarse_future"][key] = coarse_maps[z][record]
    return result
