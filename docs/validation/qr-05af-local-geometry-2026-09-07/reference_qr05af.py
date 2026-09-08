"""Independent exact record-local geometry packet reference for QR-05AF.

Static own-lineage native guards; no source/fixture or coordinate access.
Inclusions use an upward subset transform. Observed chains use interval
intersections and comparable pairs rather than full-source chain indicators.
"""

import hashlib
import json
import re
from fractions import Fraction as F
from itertools import combinations
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 64
MAX_NODES = 131072
MAX_BYTES = 4194304
MAX_EVENTS = 12
MAX_ELIGIBLE = 8
MAX_PROBES = 8
MAX_INCLUSION_TERMS = 6561
MAX_CHAIN_CANDIDATES = 632
MAX_ESTIMATOR_TERMS = 2528
MAX_TOTAL_WORK = 20000
METHODS = ("raw", "marginal_product", "uniform_rate", "joint_supported")
SCOPE = (
    "full_target_support_inferred",
    "source_moments_inferred",
    "geometry_inferred",
    "observation_origin_authenticated",
    "kernel_is_quantum_channel",
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
        _require(n > 0, "strictly positive density")
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


def _inclusions(masses):
    # Upward Boolean-lattice zeta transform, independent of support/superset
    # pair enumeration. Public logical accounting remains the canonical3^M.
    result = list(masses)
    m = len(masses).bit_length() - 1
    for bit in range(m):
        for mask in range(len(result)):
            if not (mask & (1 << bit)):
                result[mask] += result[mask | (1 << bit)]
    return result


def _chains(kept, past, source, target, degree):
    local = {original: i for i, original in enumerate(kept)}
    a, b = local[source], local[target]
    if a not in past[b]:
        return []
    if degree == 0:
        return [[]]
    inside = [i for i in past[b] if a in past[i]]
    if degree == 1:
        return [[kept[i]] for i in inside]
    _require(degree == 2, "three declared chain degrees")
    return [[kept[i], kept[j]] for i, j in combinations(inside, 2) if i in past[j]]


def _weight(method, support, inclusions, pbar):
    _require(method in METHODS and type(support) is int, "declared estimator and support mask")
    if method == "raw":
        return F(1)
    if method == "joint_supported":
        return F(1) / inclusions[support] if inclusions[support] else None
    if method == "uniform_rate":
        return F(1) / pbar ** support.bit_count()
    product = F(1)
    for bit in range(len(inclusions).bit_length() - 1):
        if support & (1 << bit):
            product *= inclusions[1 << bit]
    return F(1) / product


def _scale(rho, degree):
    _require(
        type(rho) is F and rho > 0 and type(degree) is int and 0 <= degree <= 2,
        "exact positive density and declared degree",
    )
    value = F((-1) ** degree, 2 ** (degree + 1)) / rho**degree
    _wire(value)
    return value


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
            "density",
            "mask_probabilities",
            "record",
        ),
        "exact AF packet fields",
    )
    _require(problem["schema_version"] == "det8-qr05af-problem-v1", "AF schema")
    _require(problem["family"] == "qr05af_local_geometry", "AF family")
    n = problem["frame_size"]
    _require(type(n) is int and 2 <= n <= MAX_EVENTS, "native bounded event frame")
    fixed = _ids(problem["fixed"], n, "fixed IDs")
    eligible = _ids(problem["eligible"], n, "eligible IDs")
    _require(1 <= len(eligible) <= MAX_ELIGIBLE, "eligible cap before exponential allocation")
    _require(
        sorted(fixed + eligible) == list(range(n)), "disjoint complete fixed/eligible partition"
    )
    probes = problem["probes"]
    _require(type(probes) is list and 1 <= len(probes) <= MAX_PROBES, "probe cap")
    names, pairs = set(), set()
    for probe in probes:
        _fields(probe, ("name", "source", "target"), "exact probe fields")
        name, source, target = probe["name"], probe["source"], probe["target"]
        _require(
            type(name) is str
            and len(name) <= 40
            and re.fullmatch(r"[a-z][a-z0-9_]{0,39}", name) is not None,
            "bounded probe name",
        )
        _require(name not in names, "distinct probe names")
        names.add(name)
        _require(
            type(source) is int
            and type(target) is int
            and source in fixed
            and target in fixed
            and source < target,
            "ordered fixed probe endpoints",
        )
        _require((source, target) not in pairs, "distinct probe endpoint pairs")
        pairs.add((source, target))
    rho = _fraction(problem["density"])
    m = len(eligible)
    L = 1 << m
    raw_masses = problem["mask_probabilities"]
    _require(type(raw_masses) is list and len(raw_masses) == L, "complete mask-law dimension")
    masses = [_fraction(value, probability=True) for value in raw_masses]
    _require(sum(masses, F(0)) == 1, "original mask-law normalization")
    record = problem["record"]
    _fields(record, ("kept", "past"), "exact record fields")
    kept = _ids(record["kept"], n, "retained IDs")
    _require(set(fixed) <= set(kept), "all fixed IDs retained")
    past = record["past"]
    _require(type(past) is list and len(past) == len(kept), "local past row dimension")
    for i, row in enumerate(past):
        _ids(row, i, "strict local predecessor indices")
    for i, row in enumerate(past):
        _require(all(set(past[j]) <= set(row) for j in row), "received strict order is transitive")
    K, P = len(kept), len(probes)
    Q, I = 3 * P, 3**m
    C = P * (1 + K + K * (K - 1) // 2)
    W = L + I + 5 * C + 4 * Q
    _require(I <= MAX_INCLUSION_TERMS, "planned inclusion work")
    _require(C <= MAX_CHAIN_CANDIDATES, "planned chain candidates")
    _require(4 * C <= MAX_ESTIMATOR_TERMS, "planned estimator visits")
    _require(W <= MAX_TOTAL_WORK, "planned total work")
    return n, fixed, eligible, probes, rho, masses, kept, past, (L, I, C, Q, W)


def analyze(problem):
    """Estimate from one received record without inferring hidden-source facts."""
    n, _fixed, eligible, probes, rho, masses, kept, past, planned = _prepare(problem)
    L, I, C, Q, W = planned
    inclusion = _inclusions(masses)
    _require(
        len(inclusion) == L
        and inclusion[0] == 1
        and all(type(v) is F and 0 <= v <= 1 for v in inclusion),
        "complete inclusion probabilities",
    )
    inclusion_wire = [_wire(value) for value in inclusion]
    _require(
        all(inclusion[1 << bit] > 0 for bit in range(len(eligible))),
        "positive singleton marginals before weight division",
    )
    pbar = sum((inclusion[1 << bit] for bit in range(len(eligible))), F(0)) / len(eligible)
    positions = {value: bit for bit, value in enumerate(eligible)}
    mask = sum(1 << positions[value] for value in kept if value in positions)
    questions = []
    observed_terms = estimator_visits = coefficient_visits = 0
    for probe in probes:
        for degree in range(3):
            vertices = _chains(kept, past, probe["source"], probe["target"], degree)
            _require(vertices == sorted(vertices), "lexicographically ordered observed chains")
            chains = []
            counts = dict.fromkeys(METHODS, F(0))
            omitted = 0
            for chain in vertices:
                support = sum(1 << positions[v] for v in chain if v in positions)
                chains.append(
                    {
                        "vertices": chain,
                        "eligible_mask": support,
                        "inclusion": _wire(inclusion[support]),
                    }
                )
                omitted += int(inclusion[support] == 0)
                for method in METHODS:
                    weight = _weight(method, support, inclusion, pbar)
                    estimator_visits += 1
                    if weight is not None:
                        _require(
                            type(weight) is F and weight > 0, "exact positive internal chain weight"
                        )
                        counts[method] += weight
                    else:
                        _require(
                            method == "joint_supported" and inclusion[support] == 0,
                            "only explicit zero-inclusion omission",
                        )
                observed_terms += 1
            scale = _scale(rho, degree)
            coefficients = {}
            for method in METHODS:
                coefficients[method] = _wire(scale * counts[method])
                coefficient_visits += 1
            if masses[mask] > 0:
                _require(omitted == 0, "possible record has no zero-inclusion observed chain")
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": _wire(scale),
                    "observed_count": len(chains),
                    "observed_chains": chains,
                    "unsupported_observed_terms": omitted,
                    "count_estimates": {method: _wire(counts[method]) for method in METHODS},
                    "coefficient_estimates": coefficients,
                }
            )
    _require(
        observed_terms <= C
        and estimator_visits == 4 * observed_terms
        and coefficient_visits == 4 * Q
        and len(questions) == Q,
        "complete declared packet work",
    )
    total = L + I + C + estimator_visits + coefficient_visits
    _require(total <= W, "executed logical work below reservation")
    result = {
        "input_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "mask": mask,
        "probability": _wire(masses[mask]),
        "possible": masses[mask] > 0,
        "inclusion_probabilities": inclusion_wire,
        "questions": questions,
        "counts": {
            "events": n,
            "eligible_events": len(eligible),
            "kept_events": len(kept),
            "mask_rows": L,
            "questions": Q,
            "inclusion_terms": I,
            "chain_candidates": C,
            "observed_chain_terms": observed_terms,
            "estimator_terms": estimator_visits,
            "coefficient_evaluations": coefficient_visits,
            "reserved_estimator_terms": 4 * C,
            "reserved_total_work": W,
            "total_work": total,
        },
        "scope": dict.fromkeys(SCOPE, False),
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "complete detached packet output")
    return json.loads(encoded)
