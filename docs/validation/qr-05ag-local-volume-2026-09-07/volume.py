"""Exact single-record estimates of a supplied finite marked volume.

Only retained cell marks and induced order are observed; no coordinates,
missing marks, full-source targets or moments are inferred. The native guard
is statically carried from this primary's lineage without executor imports.
"""

import hashlib
import json
import re
from fractions import Fraction
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


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _string_size(value):
    _require(len(value) <= MAX_BYTES, "native string exceeds its byte cap")
    size = 2
    _require(size <= MAX_BYTES, "escaped string exceeds its byte cap")
    for character in value:
        code = ord(character)
        if character in ('"', "\\") or code in (8, 9, 10, 12, 13):
            size += 2
        elif 32 <= code <= 126:
            size += 1
        elif code <= 65535:
            size += 6
        else:
            size += 12
        _require(size <= MAX_BYTES, "escaped string exceeds its byte cap")
    return size


def _scalar_info(value):
    kind = type(value)
    if value is None:
        return 1, 0, 4
    if kind is bool:
        return 1, 0, 4 if value else 5
    if kind is str:
        return 1, 0, _string_size(value)
    if kind is int:
        _require(value.bit_length() <= MAX_BITS, "native integer exceeds its bit cap")
        return 1, 0, len(str(value))
    raise ValueError("expected exact native JSON value")


def _native(value):
    """Preflight expanded JSON value nodes, root-zero depth and exact bytes."""
    active, completed = set(), {}
    pending = [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        _require(depth <= MAX_DEPTH, "native value exceeds depth cap")
        kind = type(item)
        if kind not in (list, dict):
            nodes, height, size = _scalar_info(item)
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "native scalar exceeds cap")
            continue
        if leaving:
            active.remove(id(item))
            nodes, height, size = 1, 0, 2 + max(0, len(item) - 1)
            values = item if kind is list else item.values()
            if kind is dict:
                size += sum(_string_size(key) + 1 for key in item)
            for child in values:
                info = completed[id(child)] if type(child) in (list, dict) else _scalar_info(child)
                child_nodes, child_height, child_size = info
                nodes += child_nodes
                height = max(height, child_height + 1)
                size += child_size
                _require(nodes <= MAX_NODES, "expanded native node cap exceeded")
                _require(size + 1 <= MAX_BYTES, "expanded canonical byte cap exceeded")
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "native container exceeds cap")
            completed[id(item)] = nodes, height, size
            continue
        _require(id(item) not in active, "cyclic native JSON is invalid")
        if id(item) in completed:
            nodes, height, size = completed[id(item)]
            _require(depth + height <= MAX_DEPTH, "shared subtree exceeds depth cap")
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "shared subtree exceeds cap")
            continue
        if kind is dict:
            _require(all(type(key) is str for key in item), "object keys must be native strings")
        _require(1 + len(item) <= MAX_NODES, "expanded native node cap exceeded")
        active.add(id(item))
        pending.append((item, depth, True))
        children = item if kind is list else list(item.values())
        pending.extend((child, depth + 1, False) for child in reversed(children))
    if type(value) in (list, dict):
        nodes, height, size = completed[id(value)]
    else:
        nodes, height, size = _scalar_info(value)
    _require(height <= MAX_DEPTH and nodes <= MAX_NODES, "expanded native tree cap exceeded")
    _require(size + 1 <= MAX_BYTES, "expanded canonical byte cap exceeded")
    return size + 1


def canonical(value):
    expected_bytes = _native(value)
    data = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")
    _require(len(data) == expected_bytes, "canonical size preflight disagrees with serialization")
    _require(len(data) <= MAX_BYTES, "canonical byte cap exceeded")
    return data


def _fields(value, names):
    _require(type(value) is dict and set(value) == set(names), "unexpected object fields")


def _integer(value, minimum, maximum):
    _require(
        type(value) is int and minimum <= value <= maximum and value.bit_length() <= MAX_BITS,
        "native integer outside declared bounds",
    )


def _fraction(value, lower=None, upper=None):
    _require(type(value) is list and len(value) == 2, "expected native reduced fraction pair")
    numerator, denominator = value
    _require(
        type(numerator) is int
        and type(denominator) is int
        and denominator > 0
        and max(numerator.bit_length(), denominator.bit_length()) <= MAX_BITS,
        "invalid native fraction components",
    )
    _require(gcd(numerator, denominator) == 1, "fraction must already be reduced")
    result = Fraction(numerator, denominator)
    _require(
        (lower is None or lower <= result) and (upper is None or result <= upper),
        "fraction outside declared range",
    )
    return result


def _retained(value, lower=None, upper=None):
    _require(
        type(value) is Fraction
        and (lower is None or lower <= value)
        and (upper is None or value <= upper)
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational outside range or bit bounds",
    )
    return value


def _pair(value, lower=None, upper=None):
    _retained(value, lower, upper)
    return [value.numerator, value.denominator]


def _ids(values, upper):
    _require(type(values) is list, "IDs must be a native list")
    for value in values:
        _integer(value, 0, upper - 1)
    _require(values == sorted(set(values)), "IDs must be sorted and unique")


def _marginals(masses):
    """Visit exactly M * 2**(M-1) singleton/superset pairs."""
    M = (len(masses) - 1).bit_length()
    result = []
    for bit in range(M):
        step = 1 << bit
        total = Fraction(0)
        for block in range(step, len(masses), 2 * step):
            for mask in range(block, block + step):
                total += masses[mask]
        result.append(total)
    return result


def _members(kept, past, source, target, eligible):
    """Inspect retained eligible IDs only, without filling absent relations."""
    local = {event: index for index, event in enumerate(kept)}
    a, b = local[source], local[target]
    return [
        event
        for event in eligible
        if event in local and a in past[local[event]] and local[event] in past[b]
    ]


def _weight(method, pi, pbar):
    # This individual inverse is unretained. Only the final method sum is
    # component-bound; inverse/product components may exceed the cap and cancel.
    if method == "raw":
        return Fraction(1)
    if method == "uniform_rate":
        _require(pbar > 0, "positive eligible marginal mean required")
        return 1 / pbar
    _require(method == "inclusion" and pi > 0, "positive vertex inclusion required")
    return 1 / pi


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
    )
    _require(
        problem["schema_version"] == "det8-qr05ag-problem-v1"
        and problem["family"] == "qr05ag_local_volume",
        "unknown local-volume schema",
    )
    n = problem["frame_size"]
    _integer(n, 3, min(12, MAX_EVENTS))
    fixed, eligible = problem["fixed"], problem["eligible"]
    _ids(fixed, n)
    _ids(eligible, n)
    M = len(eligible)
    _require(len(fixed) >= 2, "at least two fixed probe markers required")
    _require(1 <= M <= min(8, MAX_ELIGIBLE), "eligible inventory exceeds live bound")
    _require(
        sorted(fixed + eligible) == list(range(n)),
        "fixed and eligible must disjointly partition the frame",
    )
    probes = problem["probes"]
    _require(
        type(probes) is list and 1 <= len(probes) <= min(8, MAX_PROBES),
        "probe inventory exceeds live bound",
    )
    names, endpoint_pairs = set(), set()
    for probe in probes:
        _fields(probe, ("name", "source", "target"))
        name, source, target = probe["name"], probe["source"], probe["target"]
        _require(
            type(name) is str and re.fullmatch(r"[a-z][a-z0-9_]{0,39}", name) is not None,
            "invalid probe name",
        )
        _integer(source, 0, n - 1)
        _integer(target, 0, n - 1)
        _require(
            source < target and source in fixed and target in fixed,
            "ordered fixed endpoints required",
        )
        _require(
            name not in names and (source, target) not in endpoint_pairs,
            "probe names and endpoint pairs must be unique",
        )
        names.add(name)
        endpoint_pairs.add((source, target))

    # M is bounded before exponential allocation or traversal.
    L = 1 << M
    raw_masses = problem["mask_probabilities"]
    _require(type(raw_masses) is list and len(raw_masses) == L, "complete mask law required")
    masses = [_fraction(value, 0, 1) for value in raw_masses]
    _require(sum(masses, Fraction(0)) == 1, "mask probabilities must sum to one")

    record = problem["record"]
    _fields(record, ("kept", "past", "marks"))
    kept, past, marks = record["kept"], record["past"], record["marks"]
    _ids(kept, n)
    _require(set(fixed) <= set(kept), "all fixed events must be kept")
    _require(type(past) is list and len(past) == len(kept), "one local past row per retained event")
    for i, row in enumerate(past):
        _ids(row, i)
    for row in past:
        received = set(row)
        _require(
            all(set(past[j]) <= received for j in row),
            "received order must be transitive; missing relations are not repaired",
        )

    retained = [event for event in eligible if event in kept]
    _require(
        type(marks) is list and len(marks) == len(retained),
        "exact retained mark inventory required",
    )
    volumes = {}
    for event, mark in zip(retained, marks):
        _fields(mark, ("event", "volume"))
        _integer(mark["event"], 0, n - 1)
        _require(mark["event"] == event, "marks must exactly align with retained eligible IDs")
        volume = _fraction(mark["volume"], 0)
        _require(volume > 0, "cell volumes must be positive")
        volumes[event] = volume

    K, P = len(retained), len(probes)
    I, C = M * (1 << (M - 1)), P * K
    W = L + I + 4 * C + 3 * P
    for amount, cap, name in (
        (I, MAX_INCLUSION_TERMS, "inclusion terms"),
        (C, MAX_MEMBER_CANDIDATES, "member candidates"),
        (3 * C, MAX_ESTIMATOR_TERMS, "reserved estimator terms"),
        (W, MAX_TOTAL_WORK, "reserved total work"),
    ):
        _require(amount <= cap, name + " exceed live cap")
    return n, eligible, probes, masses, kept, past, volumes, (L, I, C, P, W)


def analyze(problem):
    n, eligible, probes, masses, kept, past, volumes, reserved = _prepare(problem)
    L, I, C, P, W = reserved
    input_sha = hashlib.sha256(canonical(problem)).hexdigest()
    marginals = _marginals(masses)
    _require(len(marginals) == len(eligible), "complete singleton marginal table required")
    marginal_wire = [_pair(value, 0, 1) for value in marginals]
    _require(
        all(value > 0 for value in marginals), "every eligible vertex marginal must be positive"
    )
    pbar = sum(marginals, Fraction(0)) / len(eligible)
    pi_by_id = dict(zip(eligible, marginals))
    mask = sum(1 << bit for bit, event in enumerate(eligible) if event in kept)
    probability = masses[mask]

    questions = []
    A = estimator_visits = 0
    for probe in probes:
        members = _members(kept, past, probe["source"], probe["target"], eligible)
        _require(
            members == sorted(set(members)) and set(members) <= set(volumes),
            "members must be unique retained eligible IDs in order",
        )
        estimates = dict.fromkeys(METHODS, Fraction(0))
        cells = []
        for event in members:
            volume, pi = volumes[event], pi_by_id[event]
            cells.append({"event": event, "volume": _pair(volume, 0), "inclusion": _pair(pi, 0, 1)})
            for method in METHODS:
                weight = _weight(method, pi, pbar)
                _require(
                    type(weight) is Fraction and weight > 0, "positive rational multiplier required"
                )
                estimates[method] += volume * weight
                estimator_visits += 1
        A += len(members)
        questions.append(
            {
                "probe": probe["name"],
                "observed_cells": cells,
                "estimates": {method: _pair(estimates[method], 0) for method in METHODS},
            }
        )
    _require(len(questions) == P and A <= C, "question/member inventory exceeds reservation")
    _require(
        estimator_visits == 3 * A and estimator_visits <= 3 * C,
        "estimator visit inventory differs",
    )
    total_work = L + I + C + estimator_visits + 3 * P
    _require(total_work <= W, "executed logical work exceeds reservation")
    result = {
        "input_sha256": input_sha,
        "mask": mask,
        "probability": _pair(probability, 0, 1),
        "possible": probability > 0,
        "marginals": marginal_wire,
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
            "observed_member_terms": A,
            "estimator_terms": estimator_visits,
            "reserved_estimator_terms": 3 * C,
            "reserved_total_work": W,
            "total_work": total_work,
        },
        "scope": {
            "missing_marks_inferred": False,
            "source_moments_inferred": False,
            "geometry_inferred": False,
            "mark_origin_authenticated": False,
            "observation_origin_authenticated": False,
        },
    }
    return json.loads(canonical(result))
