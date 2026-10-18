"""Independent exact local marked-volume observer for QR-05AG.

Own AF-lineage native guards are statically carried; there are no executor
imports. Marginals use dyadic mask blocks; membership uses local interval
intersection. Only retained eligible marks enter any estimate.
"""

import hashlib
import json
import re
from fractions import Fraction as F
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 64
MAX_NODES = 131072
MAX_BYTES = 4194304
MAX_EVENTS = 12
MAX_ELIGIBLE = 8
MAX_PROBES = 8
MAX_INCLUSION_TERMS = 1024
MAX_MEMBER_CANDIDATES = 64
MAX_ESTIMATOR_TERMS = 192
MAX_TOTAL_WORK = 2000
METHODS = ("raw", "uniform_rate", "inclusion")
SCOPE = (
    "missing_marks_inferred",
    "source_moments_inferred",
    "geometry_inferred",
    "mark_origin_authenticated",
    "observation_origin_authenticated",
)


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _fields(obj, names, message):
    _require(
        type(obj) is dict and all(type(k) is str for k in obj) and set(obj) == set(names), message
    )


def _string_bytes(value):
    # Exact ensure_ascii=True JSON size without serializing an unbounded tree.
    _require(type(value) is str, "native object key or string")
    _require(len(value) <= MAX_BYTES, "string byte cap")
    count = 2
    for char in value:
        code = ord(char)
        if char in ('"', "\\", "\b", "\t", "\n", "\f", "\r"):
            count += 2
        elif code < 32 or code >= 127:
            count += 6 if code <= 65535 else 12
        else:
            count += 1
        _require(count <= MAX_BYTES, "escaped string byte cap")
    return count


def _native(value):
    # Nodes are JSON values, not object keys. A scalar/empty container has
    # height zero: root depth is zero and deepest scalar leaves count.
    pending, active, complete = [(value, False, 0)], set(), {}

    def scalar(v):
        if v is None:
            return (1, 0, 4)
        if type(v) is bool:
            return (1, 0, 4 if v else 5)
        if type(v) is str:
            return (1, 0, _string_bytes(v))
        if type(v) is int:
            _require(abs(v).bit_length() <= MAX_BITS, "native integer component bit cap")
            return (1, 0, len(str(v)))
        _require(type(v) in (list, dict), "non-native JSON value")
        return None

    while pending:
        current, leaving, depth = pending.pop()
        _require(depth <= MAX_DEPTH, "early native traversal depth cap")
        simple = scalar(current)
        if simple is not None:
            continue
        identity = id(current)
        if leaving:
            children = list(current.values()) if type(current) is dict else current
            nodes, height = 1, 0
            size = 2 + max(0, len(children) - 1)
            if type(current) is dict:
                for key in current:
                    size += _string_bytes(key) + 1
                    _require(size <= MAX_BYTES, "object-key expanded byte cap")
            for child in children:
                info = complete[id(child)] if type(child) in (list, dict) else scalar(child)
                nodes += info[0]
                height = max(height, info[1] + 1)
                size += info[2]
                _require(nodes <= MAX_NODES, "expanded value-node cap")
                _require(height <= MAX_DEPTH, "native depth cap")
                _require(size <= MAX_BYTES, "expanded canonical byte cap")
            _require(
                nodes <= MAX_NODES and height <= MAX_DEPTH and size <= MAX_BYTES,
                "native tree resource cap",
            )
            complete[identity] = (nodes, height, size)
            active.remove(identity)
            continue
        _require(identity not in active, "cyclic JSON container")
        if identity in complete:
            _require(depth + complete[identity][1] <= MAX_DEPTH, "cached subtree depth cap")
            continue
        _require(len(current) + 1 <= MAX_NODES, "container width value-node lower bound")
        if type(current) is dict:
            _require(all(type(key) is str for key in current), "non-native object key")
        active.add(identity)
        pending.append((current, True, depth))
        children = current.values() if type(current) is dict else current
        pending.extend((child, False, depth + 1) for child in children)
    info = complete[id(value)] if type(value) in (list, dict) else scalar(value)
    _require(
        info[0] <= MAX_NODES and info[1] <= MAX_DEPTH and info[2] + 1 <= MAX_BYTES,
        "complete expanded native wire cap",
    )


def _canonical(value):
    try:
        return (
            json.dumps(
                value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
            )
            + "\n"
        ).encode("ascii")
    except (TypeError, OverflowError, RecursionError, ValueError) as error:
        raise ValueError("canonical JSON serialization failed") from error


def _fraction(value, probability=False):
    _require(type(value) is list and len(value) == 2, "native rational pair")
    n, d = value
    _require(type(n) is int and type(d) is int and d > 0, "native rational components")
    _require(gcd(n, d) == 1, "reduced rational")
    _require(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "input rational bit cap")
    if probability:
        _require(0 <= n <= d, "probability interval")
    else:
        _require(n > 0, "strictly positive volume mark")
    return F(n, d)


def _wire(value):
    _require(type(value) is F, "retained exact rational")
    _require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational bit cap",
    )
    return [value.numerator, value.denominator]


def _ids(values, size, name):
    _require(
        type(values) is list and all(type(v) is int and 0 <= v < size for v in values),
        "native bounded " + name,
    )
    _require(values == sorted(set(values)), "sorted distinct " + name)
    return values


def _marginals(masses):
    result = []
    m = len(masses).bit_length() - 1
    for bit in range(m):
        step = 1 << bit
        value = F(0)
        for start in range(step, len(masses), 2 * step):
            value += sum(masses[start : start + step], F(0))
        result.append(value)
    return result


def _members(kept, past, source, target, eligible):
    position = {event: i for i, event in enumerate(kept)}
    a, b = position[source], position[target]
    if a not in past[b]:
        return []
    return [
        event
        for event in eligible
        if event in position and position[event] in past[b] and a in past[position[event]]
    ]


def _weight(method, pi, pbar):
    _require(method in METHODS, "declared volume estimator")
    if method == "raw":
        return F(1)
    return F(1) / (pbar if method == "uniform_rate" else pi)


def _prepare(problem):
    _native(problem)
    _fields(
        problem,
        (
            "schema_version",
            "family",
            "frame_size",
            "fixed",
            "eligible",
            "probes",
            "mask_probabilities",
            "record",
        ),
        "exact AG packet fields",
    )
    _require(problem["schema_version"] == "det8-qr05ag-problem-v1", "AG schema")
    _require(problem["family"] == "qr05ag_local_volume", "AG family")
    n = problem["frame_size"]
    _require(type(n) is int and 3 <= n <= MAX_EVENTS, "native bounded event frame")
    fixed = _ids(problem["fixed"], n, "fixed IDs")
    eligible = _ids(problem["eligible"], n, "eligible IDs")
    _require(len(fixed) >= 2, "at least two fixed probe markers")
    _require(1 <= len(eligible) <= MAX_ELIGIBLE, "eligible bound before exponential allocation")
    _require(
        sorted(fixed + eligible) == list(range(n)), "complete disjoint fixed/eligible partition"
    )
    probes = problem["probes"]
    _require(type(probes) is list and 1 <= len(probes) <= MAX_PROBES, "bounded probe list")
    names, pairs = set(), set()
    for probe in probes:
        _fields(probe, ("name", "source", "target"), "exact probe fields")
        name, a, b = probe["name"], probe["source"], probe["target"]
        _require(
            type(name) is str and re.fullmatch(r"[a-z][a-z0-9_]{0,39}", name) is not None,
            "bounded probe name",
        )
        _require(name not in names, "unique probe names")
        _require(
            type(a) is int and type(b) is int and a in fixed and b in fixed and a < b,
            "native fixed ordered probe endpoints",
        )
        _require((a, b) not in pairs, "unique probe endpoint pairs")
        names.add(name)
        pairs.add((a, b))
    m = len(eligible)
    L = 1 << m
    law = problem["mask_probabilities"]
    _require(type(law) is list and len(law) == L, "complete mask law")
    masses = [_fraction(row, probability=True) for row in law]
    _require(sum(masses, F(0)) == 1, "normalized mask law")
    record = problem["record"]
    _fields(record, ("kept", "past", "marks"), "exact retained record")
    kept = _ids(record["kept"], n, "kept IDs")
    _require(set(fixed) <= set(kept), "every fixed marker is retained")
    past = record["past"]
    _require(type(past) is list and len(past) == len(kept), "one past row per retained ID")
    for i, row in enumerate(past):
        _ids(row, i, "local predecessor indices")
        for predecessor in row:
            _require(set(past[predecessor]) <= set(row), "transitive observation without repair")
    retained = [event for event in eligible if event in kept]
    marks = record["marks"]
    _require(type(marks) is list and len(marks) == len(retained), "exact retained mark alignment")
    volumes = {}
    for event, row in zip(retained, marks, strict=True):
        _fields(row, ("event", "volume"), "exact retained cell mark")
        _require(
            type(row["event"]) is int and row["event"] == event,
            "ID-sorted retained eligible marks only",
        )
        volumes[event] = _fraction(row["volume"])
    P, K = len(probes), len(retained)
    I = m * (1 << (m - 1))
    C = P * K
    W = L + I + 4 * C + 3 * P
    _require(I <= MAX_INCLUSION_TERMS, "marginal inclusion work cap")
    _require(C <= MAX_MEMBER_CANDIDATES, "member candidate work cap")
    _require(3 * C <= MAX_ESTIMATOR_TERMS, "reserved estimator work cap")
    _require(W <= MAX_TOTAL_WORK, "reserved total work cap")
    return n, fixed, eligible, probes, kept, past, masses, volumes, L, I, C, W


def analyze(problem):
    n, _fixed, eligible, probes, kept, past, masses, volumes, L, I, C, W = _prepare(problem)
    input_bytes = _canonical(problem)
    pi = _marginals(masses)
    _require(all(value > 0 for value in pi), "positive full-frame singleton marginals")
    pbar = sum(pi, F(0)) / len(eligible)
    by_event = dict(zip(eligible, pi, strict=True))
    mask = sum(1 << i for i, event in enumerate(eligible) if event in kept)
    questions, observed = [], 0
    for probe in probes:
        members = _members(kept, past, probe["source"], probe["target"], eligible)
        cells = []
        sums = {method: F(0) for method in METHODS}
        for event in members:
            volume, inclusion = volumes[event], by_event[event]
            cells.append({"event": event, "volume": _wire(volume), "inclusion": _wire(inclusion)})
            for method in METHODS:
                sums[method] += volume * _weight(method, inclusion, pbar)
        observed += len(members)
        questions.append(
            {
                "probe": probe["name"],
                "observed_cells": cells,
                "estimates": {method: _wire(value) for method, value in sums.items()},
            }
        )
    P = len(probes)
    result = {
        "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
        "mask": mask,
        "probability": _wire(masses[mask]),
        "possible": bool(masses[mask]),
        "marginals": [_wire(value) for value in pi],
        "questions": questions,
        "counts": {
            "events": n,
            "eligible_events": len(eligible),
            "kept_events": len(kept),
            "retained_cells": len(volumes),
            "mask_rows": L,
            "questions": P,
            "inclusion_terms": I,
            "member_candidates": C,
            "observed_member_terms": observed,
            "estimator_terms": 3 * observed,
            "reserved_estimator_terms": 3 * C,
            "reserved_total_work": W,
            "total_work": L + I + C + 3 * observed + 3 * P,
        },
        "scope": dict.fromkeys(SCOPE, False),
    }
    _native(result)
    return json.loads(_canonical(result))
