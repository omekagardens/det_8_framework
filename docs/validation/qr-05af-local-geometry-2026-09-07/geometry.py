"""Exact record-local order and scalar-kernel estimates.

The packet contains no coordinates, missing relations or source targets.
Only this primary's own native guard is statically carried; no prior or
alternative executor is imported.
"""

import hashlib
import json
import re
from fractions import Fraction
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


def _inclusions(masses):
    """Sum every canonical support/superset pair exactly once."""
    full = len(masses) - 1
    result = []
    for support in range(len(masses)):
        free = full ^ support
        subset, total = free, Fraction(0)
        while True:
            total += masses[support | subset]
            if subset == 0:
                break
            subset = (subset - 1) & free
        result.append(total)
    return result


def _chains(kept, past, source, target, degree):
    """Enumerate candidate sets in this packet only; never fill missing edges."""
    a, b = kept.index(source), kept.index(target)
    result = []
    for candidate in combinations(range(len(kept)), degree):
        path = (a, *candidate, b)
        if all(path[j] in past[path[j + 1]] for j in range(len(path) - 1)):
            result.append([kept[i] for i in candidate])
    return result


def _weight(method, support, inclusions, pbar):
    # The individual inverse is not retained. Only the final method sum is
    # component-bound; rational products and denominators may cancel there.
    if method == "raw":
        return Fraction(1)
    if method == "joint_supported":
        value = inclusions[support]
        return None if value == 0 else 1 / value
    if method == "uniform_rate":
        _require(pbar > 0, "positive eligible marginal mean required")
        return 1 / pbar ** support.bit_count()
    _require(method == "marginal_product", "unknown method")
    probability = Fraction(1)
    for bit in range((len(inclusions) - 1).bit_length()):
        if support & (1 << bit):
            probability *= inclusions[1 << bit]
    _require(probability > 0, "positive vertex marginals required")
    return 1 / probability


def _scale(rho, degree):
    _require(rho > 0 and degree in (0, 1, 2), "positive density and declared degree required")
    return _retained(Fraction((-1) ** degree, 2 ** (degree + 1)) / rho**degree)


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
    )
    _require(
        problem["schema_version"] == "det8-qr05af-problem-v1"
        and problem["family"] == "qr05af_local_geometry",
        "unknown local-geometry schema",
    )
    n = problem["frame_size"]
    _integer(n, 2, min(12, MAX_EVENTS))
    fixed, eligible = problem["fixed"], problem["eligible"]
    _ids(fixed, n)
    _ids(eligible, n)
    M = len(eligible)
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
    names, pairs = set(), set()
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
            name not in names and (source, target) not in pairs,
            "probe names and pairs must be unique",
        )
        names.add(name)
        pairs.add((source, target))
    rho = _fraction(problem["density"], 0)
    _require(rho > 0, "density must be positive")
    # M is bounded before this exponential allocation/size check.
    L = 1 << M
    raw_masses = problem["mask_probabilities"]
    _require(type(raw_masses) is list and len(raw_masses) == L, "complete mask law required")
    masses = [_fraction(value, 0, 1) for value in raw_masses]
    _require(sum(masses, Fraction(0)) == 1, "mask probabilities must sum to one")

    record = problem["record"]
    _fields(record, ("kept", "past"))
    kept, past = record["kept"], record["past"]
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

    K, P = len(kept), len(probes)
    Q, I = 3 * P, 3**M
    C = P * (1 + K + K * (K - 1) // 2)
    W = L + I + 5 * C + 4 * Q
    for amount, cap, name in (
        (I, MAX_INCLUSION_TERMS, "inclusion terms"),
        (C, MAX_CHAIN_CANDIDATES, "chain candidates"),
        (4 * C, MAX_ESTIMATOR_TERMS, "reserved estimator terms"),
        (W, MAX_TOTAL_WORK, "reserved total work"),
    ):
        _require(amount <= cap, name + " exceed live cap")
    return n, fixed, eligible, probes, rho, masses, kept, past, (L, I, C, Q, W)


def analyze(problem):
    n, _fixed, eligible, probes, rho, masses, kept, past, reserved = _prepare(problem)
    L, I, C, Q, W = reserved
    input_sha = hashlib.sha256(canonical(problem)).hexdigest()
    inclusions = _inclusions(masses)
    _require(len(inclusions) == L and inclusions[0] == 1, "complete inclusion table required")
    inclusion_wire = [_pair(value, 0, 1) for value in inclusions]
    marginals = [inclusions[1 << bit] for bit in range(len(eligible))]
    _require(
        all(value > 0 for value in marginals), "every eligible vertex marginal must be positive"
    )
    pbar = sum(marginals, Fraction(0)) / len(eligible)
    bit_by_id = {vertex: 1 << bit for bit, vertex in enumerate(eligible)}
    mask = sum(bit_by_id.get(vertex, 0) for vertex in kept)
    probability = masses[mask]

    questions = []
    A = estimator_visits = coefficient_visits = 0
    for probe in probes:
        for degree in range(3):
            chains = _chains(kept, past, probe["source"], probe["target"], degree)
            _require(
                chains == sorted(chains) and len({tuple(c) for c in chains}) == len(chains),
                "observed chains must be lexicographically unique",
            )
            scale = _scale(rho, degree)
            terms, omitted = [], 0
            estimates = dict.fromkeys(METHODS, Fraction(0))
            for vertices in chains:
                support = sum(bit_by_id.get(vertex, 0) for vertex in vertices)
                terms.append(
                    {
                        "vertices": vertices,
                        "eligible_mask": support,
                        "inclusion": _pair(inclusions[support], 0, 1),
                    }
                )
                for method in METHODS:
                    weight = _weight(method, support, inclusions, pbar)
                    estimator_visits += 1
                    if weight is None:
                        _require(
                            method == "joint_supported" and inclusions[support] == 0,
                            "only unsupported joint terms may be omitted",
                        )
                        omitted += 1
                    else:
                        _require(
                            type(weight) is Fraction and weight >= 0,
                            "method weight must be a nonnegative rational",
                        )
                        estimates[method] += weight
            count_wire, coefficient_wire = {}, {}
            for method in METHODS:
                count_wire[method] = _pair(estimates[method], 0)
                coefficient_wire[method] = _pair(scale * estimates[method])
                coefficient_visits += 1
            _require(
                omitted == sum(inclusions[term["eligible_mask"]] == 0 for term in terms),
                "joint omission inventory differs",
            )
            if probability > 0:
                _require(
                    omitted == 0, "a positive-probability record cannot contain unsupported chains"
                )
            A += len(chains)
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": _pair(scale),
                    "observed_count": len(chains),
                    "observed_chains": terms,
                    "unsupported_observed_terms": omitted,
                    "count_estimates": count_wire,
                    "coefficient_estimates": coefficient_wire,
                }
            )
    _require(len(questions) == Q and A <= C, "question/chain inventory exceeds reservation")
    _require(
        estimator_visits == 4 * A and estimator_visits <= 4 * C, "estimator visit inventory differs"
    )
    _require(coefficient_visits == 4 * Q, "coefficient visit inventory differs")
    total_work = L + I + C + estimator_visits + coefficient_visits
    _require(total_work <= W, "executed logical work exceeds reservation")
    result = {
        "input_sha256": input_sha,
        "mask": mask,
        "probability": _pair(probability, 0, 1),
        "possible": probability > 0,
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
            "observed_chain_terms": A,
            "estimator_terms": estimator_visits,
            "coefficient_evaluations": coefficient_visits,
            "reserved_estimator_terms": 4 * C,
            "reserved_total_work": W,
            "total_work": total_work,
        },
        "scope": {
            "full_target_support_inferred": False,
            "source_moments_inferred": False,
            "geometry_inferred": False,
            "observation_origin_authenticated": False,
            "kernel_is_quantum_channel": False,
        },
    }
    return json.loads(canonical(result))
