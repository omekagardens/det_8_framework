"""Private exact weighted scalar-kernel diagnostic on supplied AH fixtures.

This is not a hardened generic production API. Geometry stays in build_case;
observe receives only a retained-order packet. No artifacts or other engines
are imported, and all mathematical calculations use exact rational arithmetic.
"""

import copy
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd

ALPHA = (F(1, 2), F(-1, 4), F(1, 8))
METHODS = ("raw", "joint_supported")


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    """Basic exact-wire consistency, not adversarial resource admission."""
    kind = type(value)
    if kind is int:
        _require(value.bit_length() <= 4096, "retained integer exceeds component bound")
    elif value is None or kind in (bool, str):
        return
    elif kind is list:
        for child in value:
            _native(child)
    elif kind is dict:
        _require(all(type(k) is str for k in value), "native string keys required")
        for child in value.values():
            _native(child)
    else:
        raise ValueError("native exact mathematical wire required")


def canonical(value):
    _native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")


def _fields(value, keys):
    _require(type(value) is dict and set(value) == set(keys), "unexpected fixture fields")


def _fraction(value):
    _require(type(value) is list and len(value) == 2, "native fraction pair required")
    a, b = value
    _require(
        type(a) is int
        and type(b) is int
        and b > 0
        and max(a.bit_length(), b.bit_length()) <= 4096
        and gcd(a, b) == 1,
        "reduced bounded native fraction required",
    )
    return F(a, b)


def _wire(value):
    value = F(value)
    _require(
        max(value.numerator.bit_length(), value.denominator.bit_length()) <= 4096,
        "retained fraction exceeds component bound",
    )
    return [value.numerator, value.denominator]


def _vector(values):
    return [_wire(x) for x in values]


def _matrix(values):
    return [_vector(row) for row in values]


def _ids(values, n):
    _require(
        type(values) is list and all(type(v) is int and 0 <= v < n for v in values),
        "bounded original IDs required",
    )
    _require(values == sorted(set(values)), "IDs must be sorted and unique")


def causal_area(a, b, c, d):
    """Integral of 1(x<y) on [a,b] x [c,d], using a positive-part primitive."""
    _require(all(type(x) in (int, F) for x in (a, b, c, d)), "exact rational endpoints required")
    a, b, c, d = map(F, (a, b, c, d))
    _require(a <= b and c <= d, "directed interval endpoints are reversed")
    positive_square = lambda x: max(F(0), x) ** 2
    result = (
        positive_square(d - a)
        - positive_square(d - b)
        - positive_square(c - a)
        + positive_square(c - b)
    ) / 2
    _require(0 <= result <= (b - a) * (d - c), "directed integral outside its volume bound")
    return result


def _area(bounds):
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) / 2


def _rectangle(raw):
    _require(type(raw) is list and len(raw) == 4, "four rectangle coordinates required")
    b = tuple(map(_fraction, raw))
    _require(b[0] < b[1] and b[2] < b[3], "positive cell rectangle required")
    return b


def _clip(cell, query):
    b = (
        max(cell[0], query[0]),
        min(cell[1], query[1]),
        max(cell[2], query[2]),
        min(cell[3], query[3]),
    )
    return b if b[0] < b[1] and b[2] < b[3] else None


def _integral(left, right):
    if left is None or right is None:
        return F(0)
    return (
        causal_area(left[0], left[1], right[0], right[1])
        * causal_area(left[2], left[3], right[2], right[3])
        / 4
    )


def _masses(raw, M):
    _require(type(raw) is list and len(raw) == 1 << M, "complete mask law required")
    values = list(map(_fraction, raw))
    _require(
        all(0 <= p <= 1 for p in values) and sum(values, F(0)) == 1, "normalized mask law required"
    )
    positive = [(mask, p) for mask, p in enumerate(values) if p]
    _require(
        all(sum((p for mask, p in positive if mask & (1 << i)), F(0)) > 0 for i in range(M)),
        "all eligible singleton marginals must be positive",
    )
    return values, positive


def _inclusion(positive, support):
    return sum((p for mask, p in positive if mask & support == support), F(0))


def _probe_checks(probes, fixed, n):
    _require(type(probes) is list and 1 <= len(probes) <= 5, "bounded probe inventory required")
    names, pairs = set(), set()
    for q in probes:
        _fields(q, ("name", "source", "target"))
        name, a, b = q["name"], q["source"], q["target"]
        _require(type(name) is str and name and name not in names, "unique probe names required")
        _require(
            type(a) is int and type(b) is int and 0 <= a < b < n and a in fixed and b in fixed,
            "ordered fixed probe endpoints required",
        )
        _require((a, b) not in pairs, "unique probe endpoint pairs required")
        names.add(name)
        pairs.add((a, b))


def _record(kept, past, fixed, n):
    _ids(kept, n)
    _require(set(fixed) <= set(kept), "all fixed markers must be retained")
    _require(
        type(past) is list and len(past) == len(kept), "one past row per retained event required"
    )
    for i, row in enumerate(past):
        _ids(row, i)
    for row in past:
        _require(all(set(past[j]) <= set(row) for j in row), "record order must be transitive")


def _chains(kept, past, eligible, a, b, degree):
    local = {event: pos for pos, event in enumerate(kept)}
    if local[a] not in past[local[b]]:
        return []
    if degree == 0:
        return [[]]
    internal = [
        event
        for event in eligible
        if event in local and local[a] in past[local[event]] and local[event] in past[local[b]]
    ]
    if degree == 1:
        return [[event] for event in internal]
    return [[i, j] for i, j in combinations(internal, 2) if local[i] in past[local[j]]]


def _chain_wire(vertices, weights, bits, probability):
    support = sum(bits[event] for event in vertices)
    weight = F(1)
    for event in vertices:
        weight *= weights[event]
    return {
        "vertices": vertices,
        "eligible_mask": support,
        "inclusion": _wire(probability(support)),
        "weight": _wire(weight),
    }


def observe(packet):
    _native(packet)
    _fields(packet, ("frame_size", "fixed", "eligible", "probes", "mask_probabilities", "record"))
    n = packet["frame_size"]
    _require(type(n) is int and 3 <= n <= 12, "bounded event frame required")
    fixed, eligible = packet["fixed"], packet["eligible"]
    _ids(fixed, n)
    _ids(eligible, n)
    _require(
        len(fixed) >= 2 and 1 <= len(eligible) <= 8 and sorted(fixed + eligible) == list(range(n)),
        "fixed and eligible IDs must partition the frame",
    )
    _probe_checks(packet["probes"], fixed, n)
    masses, positive = _masses(packet["mask_probabilities"], len(eligible))
    record = packet["record"]
    _fields(record, ("kept", "past", "marks"))
    kept, past = record["kept"], record["past"]
    _record(kept, past, fixed, n)
    marks = record["marks"]
    retained = [event for event in eligible if event in kept]
    _require(
        type(marks) is list and len(marks) == len(retained), "exact retained-cell marks required"
    )
    weights = {}
    for event, row in zip(retained, marks):
        _fields(row, ("event", "volume"))
        _require(
            type(row["event"]) is int and row["event"] == event, "retained mark alignment required"
        )
        weight = _fraction(row["volume"])
        _require(weight > 0, "positive supplied mark required")
        weights[event] = weight
    bits = {event: 1 << i for i, event in enumerate(eligible)}
    cache = {0: F(1)}

    def probability(support):
        if support not in cache:
            cache[support] = _inclusion(positive, support)
        return cache[support]

    mask = sum(bits.get(event, 0) for event in kept)
    questions = []
    for probe in packet["probes"]:
        for degree, alpha in enumerate(ALPHA):
            chains = [
                _chain_wire(v, weights, bits, probability)
                for v in _chains(kept, past, eligible, probe["source"], probe["target"], degree)
            ]
            raw = sum((_fraction(c["weight"]) for c in chains), F(0))
            corrected = sum(
                (
                    _fraction(c["weight"]) / _fraction(c["inclusion"])
                    for c in chains
                    if _fraction(c["inclusion"]) > 0
                ),
                F(0),
            )
            omitted = sum(_fraction(c["inclusion"]) == 0 for c in chains)
            _require(
                masses[mask] == 0 or omitted == 0,
                "positive record cannot contain impossible support",
            )
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "chains": chains,
                    "unsupported_observed_terms": omitted,
                    "estimates": {
                        "raw": _wire(alpha * raw),
                        "joint_supported": _wire(alpha * corrected),
                    },
                }
            )
    result = {
        "mask": mask,
        "probability": _wire(masses[mask]),
        "possible": masses[mask] > 0,
        "record": copy.deepcopy(record),
        "packet_sha256": hashlib.sha256(canonical(packet)).hexdigest(),
        "questions": questions,
    }
    return json.loads(canonical(result))


def _source(source, design):
    _native(source)
    _native(design)
    _fields(
        source, ("name", "coordinates", "past", "fixed", "eligible", "probes", "cells", "mark_kind")
    )
    _fields(design, ("name", "mask_probabilities"))
    coordinates = source["coordinates"]
    _require(
        type(coordinates) is list and 3 <= len(coordinates) <= 12,
        "bounded source coordinates required",
    )
    points = []
    for point in coordinates:
        _require(type(point) is list and len(point) == 2, "two point coordinates required")
        points.append(tuple(map(_fraction, point)))
    n = len(points)
    fixed, eligible = source["fixed"], source["eligible"]
    _ids(fixed, n)
    _ids(eligible, n)
    _require(
        len(fixed) >= 2 and 1 <= len(eligible) <= 8 and sorted(fixed + eligible) == list(range(n)),
        "source frame partition required",
    )
    _record(list(range(n)), source["past"], fixed, n)
    strict_past = [
        [i for i, left in enumerate(points) if left[0] < right[0] and left[1] < right[1]]
        for right in points
    ]
    _require(
        strict_past == source["past"], "source order must exactly match strict supplied geometry"
    )
    _probe_checks(source["probes"], fixed, n)
    _require(
        all(q["source"] in strict_past[q["target"]] for q in source["probes"]),
        "source probes must be strictly timelike",
    )
    raw_cells = source["cells"]
    _require(
        type(raw_cells) is list and len(raw_cells) == len(eligible),
        "one source cell per eligible ID required",
    )
    cells = []
    for event, cell in zip(eligible, raw_cells):
        _fields(cell, ("event", "bounds", "geometric_mark", "supplied_mark"))
        _require(
            type(cell["event"]) is int and cell["event"] == event, "source cell alignment required"
        )
        bounds = _rectangle(cell["bounds"])
        u, v = points[event]
        _require(
            bounds[0] < u < bounds[1] and bounds[2] < v < bounds[3],
            "representative must be cell-interior",
        )
        g, w = _area(bounds), _fraction(cell["supplied_mark"])
        _require(g == _fraction(cell["geometric_mark"]) and w > 0, "source marks/area inconsistent")
        cells.append({"event": event, "bounds": bounds, "geometric": g, "supplied": w})
    _require(
        all(_clip(a["bounds"], b["bounds"]) is None for a, b in combinations(cells, 2)),
        "source cell interiors must not overlap",
    )
    masses, positive = _masses(design["mask_probabilities"], len(eligible))
    return points, cells, masses, positive


def _geometry(source, points, cells):
    geometry = []
    for probe in source["probes"]:
        a, b = points[probe["source"]], points[probe["target"]]
        query = (a[0], b[0], a[1], b[1])
        V = _area(query)
        clips = [_clip(cell["bounds"], query) for cell in cells]
        h = [_area(clip) if clip is not None else F(0) for clip in clips]
        _require(sum(h, F(0)) == V, "clipped source cells must cover each query")
        rows = []
        K = cross = diagonal = P_g = F(0)
        for i, j in product(range(len(cells)), repeat=2):
            first, second = cells[i]["event"], cells[j]["event"]
            precedes = first in source["past"][second]
            integral = _integral(clips[i], clips[j])
            rows.append(
                {
                    "first": first,
                    "second": second,
                    "representative_precedes": precedes,
                    "clipped_product": _wire(h[i] * h[j]),
                    "causal_integral": _wire(integral),
                }
            )
            if i == j:
                _require(integral == h[i] * h[i] / 4, "within-cell causal integral mismatch")
                diagonal += integral
            else:
                cross += integral
                if precedes:
                    K += h[i] * h[j]
                    if (
                        probe["source"] in source["past"][first]
                        and second in source["past"][probe["target"]]
                    ):
                        P_g += cells[i]["geometric"] * cells[j]["geometric"]
        J = V * V / 4
        _require(
            cross + diagonal == J, "all directed cell integrals must equal rectangle continuum"
        )
        boundary, order, omission = P_g - K, K - cross, -diagonal
        _require(boundary + order + omission == P_g - J, "pair-discrepancy identity failed")
        geometry.append(
            {
                "probe": probe["name"],
                "volume": _wire(V),
                "cell_clips": [
                    {"event": cell["event"], "volume": _wire(volume)}
                    for cell, volume in zip(cells, h)
                ],
                "pair_cells": rows,
                "pair_discrepancy": {
                    key: _wire(value)
                    for key, value in {
                        "geometric_target": P_g,
                        "clipped_order_sum": K,
                        "cross_cell_integral": cross,
                        "within_cell_integral": diagonal,
                        "continuum_pair": J,
                        "boundary_error": boundary,
                        "cross_order_error": order,
                        "omission_error": omission,
                        "total_error": P_g - J,
                    }.items()
                },
            }
        )
    return geometry


def _packet(source, design, mask):
    kept = sorted(
        source["fixed"] + [event for i, event in enumerate(source["eligible"]) if mask & (1 << i)]
    )
    positions = {event: i for i, event in enumerate(kept)}
    return {
        "frame_size": len(source["past"]),
        "fixed": copy.deepcopy(source["fixed"]),
        "eligible": copy.deepcopy(source["eligible"]),
        "probes": copy.deepcopy(source["probes"]),
        "mask_probabilities": copy.deepcopy(design["mask_probabilities"]),
        "record": {
            "kept": kept,
            "past": [
                [positions[p] for p in source["past"][event] if p in positions] for event in kept
            ],
            "marks": [
                {"event": c["event"], "volume": copy.deepcopy(c["supplied_mark"])}
                for c in source["cells"]
                if c["event"] in positions
            ],
        },
    }


def _population(source, cells, geometry, positive):
    eligible = source["eligible"]
    weights = {c["event"]: c["supplied"] for c in cells}
    true = {c["event"]: c["geometric"] for c in cells}
    bits = {event: 1 << i for i, event in enumerate(eligible)}
    population = []
    for probe, geom in zip(source["probes"], geometry):
        V = _fraction(geom["volume"])
        continuum = (F(1, 2), -V / 4, V * V / 32)
        for degree, alpha in enumerate(ALPHA):
            vertices = _chains(
                list(range(len(source["past"]))),
                source["past"],
                eligible,
                probe["source"],
                probe["target"],
                degree,
            )
            chains = [
                _chain_wire(v, weights, bits, lambda s: _inclusion(positive, s)) for v in vertices
            ]
            T = alpha * sum((_fraction(c["weight"]) for c in chains), F(0))
            G = F(0)
            for chain in vertices:
                weight = F(1)
                for event in chain:
                    weight *= true[event]
                G += alpha * weight
            supported = alpha * sum(
                (_fraction(c["weight"]) for c in chains if _fraction(c["inclusion"]) > 0), F(0)
            )
            unsupported = [c["vertices"] for c in chains if _fraction(c["inclusion"]) == 0]
            if degree == 2:
                _require(
                    G == _fraction(geom["pair_discrepancy"]["geometric_target"]) / 8,
                    "source chain and geometric pair target differ",
                )
            population.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": _wire(alpha),
                    "chains": chains,
                    "supplied_target": _wire(T),
                    "geometric_target": _wire(G),
                    "continuum_target": _wire(continuum[degree]),
                    "supported_target": _wire(supported),
                    "unsupported_chains": unsupported,
                    "annotation_error": _wire(T - G),
                    "quadrature_error": _wire(G - continuum[degree]),
                    "full_target_supported": not unsupported,
                }
            )
    return population


def _moments(population, samples):
    probabilities = [_fraction(sample["probability"]) for sample in samples]
    result = {}
    for method in METHODS:
        values = [
            [_fraction(q["estimates"][method]) for q in sample["questions"]] for sample in samples
        ]
        # Structural-zero rows stay in samples; they contribute zero to these
        # sums under the unchanged, unrenormalized original probability law.
        weighted = [(p, row) for p, row in zip(probabilities, values) if p]
        means = [sum((p * row[q] for p, row in weighted), F(0)) for q in range(len(population))]
        covariance = [
            [
                sum(
                    (p * (row[q] - means[q]) * (row[r] - means[r]) for p, row in weighted),
                    F(0),
                )
                for r in range(len(population))
            ]
            for q in range(len(population))
        ]
        errors, biases = [], []
        for q, mean in zip(population, means):
            T, G, continuum = (
                _fraction(q[k]) for k in ("supplied_target", "geometric_target", "continuum_target")
            )
            bias, annotation, quadrature, total = mean - T, T - G, G - continuum, mean - continuum
            _require(
                bias + annotation + quadrature == total, "coefficient error decomposition failed"
            )
            if method == "joint_supported":
                _require(
                    mean == _fraction(q["supported_target"]),
                    "joint-supported mean differs from supported target",
                )
            biases.append(bias)
            errors.append(
                {
                    "probe": q["probe"],
                    "degree": q["degree"],
                    "sampling_bias": _wire(bias),
                    "annotation_error": _wire(annotation),
                    "quadrature_error": _wire(quadrature),
                    "total_error": _wire(total),
                }
            )
        result[method] = {
            "mean": _vector(means),
            "bias": _vector(biases),
            "covariance": _matrix(covariance),
            "errors": errors,
        }
    return result


def _union_covariance(population, positive):
    supported = [[c for c in q["chains"] if _fraction(c["inclusion"]) > 0] for q in population]
    cache = {0: F(1)}
    pairs = zeros = maximum = 0
    covariance = []
    for q, left in zip(population, supported):
        row = []
        for r, right in zip(population, supported):
            value = F(0)
            for a, b in product(left, right):
                union = a["eligible_mask"] | b["eligible_mask"]
                if union not in cache:
                    cache[union] = _inclusion(positive, union)
                joint = cache[union]
                pairs += 1
                zeros += joint == 0
                maximum = max(maximum, union.bit_count())
                value += (
                    _fraction(a["weight"])
                    * _fraction(b["weight"])
                    * (joint / (_fraction(a["inclusion"]) * _fraction(b["inclusion"])) - 1)
                )
            row.append(_fraction(q["scale"]) * _fraction(r["scale"]) * value)
        covariance.append(row)
    return _matrix(covariance), pairs, zeros, maximum


def build_case(case_id, level, source, design):
    _require(
        type(case_id) is str and case_id and type(level) is str and level,
        "case and level labels required",
    )
    points, cells, masses, positive = _source(source, design)
    geometry = _geometry(source, points, cells)
    population = _population(source, cells, geometry, positive)
    samples = [observe(_packet(source, design, mask)) for mask in range(len(masses))]
    moments = _moments(population, samples)
    covariance, pairs, zero, maximum = _union_covariance(population, positive)
    _require(
        covariance == moments["joint_supported"]["covariance"],
        "centered and chain-union covariance differ",
    )
    result = {
        "case_id": case_id,
        "level": level,
        "source": copy.deepcopy(source),
        "design": copy.deepcopy(design),
        "geometry": geometry,
        "population": population,
        "samples": samples,
        "moments": moments,
        "union_covariance": covariance,
        "counts": {
            "mask_rows": len(samples),
            "positive_rows": sum(sample["possible"] for sample in samples),
            "questions": len(population),
            "source_chain_terms": sum(len(q["chains"]) for q in population),
            "observed_chain_terms": sum(
                len(q["chains"]) for sample in samples for q in sample["questions"]
            ),
            "ordered_supported_chain_pairs": pairs,
            "zero_union_pairs": zero,
            "max_union_size": maximum,
        },
    }
    return json.loads(canonical(result))
