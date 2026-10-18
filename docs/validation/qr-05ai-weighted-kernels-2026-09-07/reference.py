"""Independent exact private QR-05AI weighted-kernel diagnostic.

No other executor imports or artifact reads. The shared source/design input is
explicit fixture data. Directed integrals use an endpoint-grid decomposition;
sampling covariance uses second moments minus products of means. This is a
bounded private scientific calculation, not a hardened generic API contract.
"""

import hashlib
import itertools
import json
import math
from fractions import Fraction as F

METHODS = ("raw", "joint_supported")
ALPHA = (F(1, 2), F(-1, 4), F(1, 8))
MAX_BITS = 4096


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, names):
    require(
        type(value) is dict and set(value) == set(names.split()), "unexpected private wire fields"
    )


def native(value):
    kind = type(value)
    if value is None or kind in (str, bool):
        return
    if kind is int:
        require(abs(value).bit_length() <= MAX_BITS, "retained integer component limit")
        return
    require(kind in (dict, list), "mathematics must be native exact JSON")
    if kind is dict:
        require(all(type(k) is str for k in value), "native object keys")
        values = value.values()
    else:
        values = value
    for child in values:
        native(child)


def canonical(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def detached(value):
    native(value)
    return json.loads(canonical(value))


def fraction(pair):
    require(type(pair) is list and len(pair) == 2, "native fraction pair")
    n, d = pair
    require(
        type(n) is int and type(d) is int and d > 0 and math.gcd(n, d) == 1,
        "reduced exact fraction",
    )
    require(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "input component limit")
    return F(n, d)


def wire(value):
    require(type(value) is F, "exact retained rational")
    require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational component limit",
    )
    return [value.numerator, value.denominator]


def vector(values):
    return [wire(F(value)) for value in values]


def matrix(rows):
    return [vector(row) for row in rows]


def exact(value):
    require(type(value) in (int, F), "direct integral endpoints must be rational")
    return F(value)


def causal_area(a, b, c, d):
    """Integral of x<y by common endpoint tiles, including diagonal triangles."""
    a, b, c, d = map(exact, (a, b, c, d))
    require(a <= b and c <= d, "ordered integral endpoints")
    if a == b or c == d:
        return F(0)
    endpoints = sorted({a, b, c, d})
    intervals = list(itertools.pairwise(endpoints))
    first = [(lo, hi) for lo, hi in intervals if a <= lo < hi <= b]
    second = [(lo, hi) for lo, hi in intervals if c <= lo < hi <= d]
    result = F(0)
    for xl, xh in first:
        for yl, yh in second:
            if xh <= yl:
                result += (xh - xl) * (yh - yl)
            elif yh <= xl:
                continue
            else:
                require(xl == yl and xh == yh, "common endpoint tiles overlap only identically")
                result += (xh - xl) ** 2 / 2
    return result


def ids(values, n):
    require(
        type(values) is list and all(type(i) is int and 0 <= i < n for i in values),
        "bounded native ID list",
    )
    require(values == sorted(set(values)), "sorted distinct IDs")
    return values


def validate_past(past, n):
    require(type(past) is list and len(past) == n, "aligned transitive past")
    for j, row in enumerate(past):
        ids(row, j)
        for predecessor in row:
            require(set(past[predecessor]) <= set(row), "record must already be transitive")


def frame(n, fixed, eligible, probes):
    require(type(n) is int and 3 <= n <= 12, "bounded event frame")
    ids(fixed, n)
    ids(eligible, n)
    require(len(fixed) >= 2 and 1 <= len(eligible) <= 8, "bounded marked/eligible frame")
    require(sorted(fixed + eligible) == list(range(n)), "complete disjoint frame partition")
    require(type(probes) is list and 1 <= len(probes) <= 5, "bounded probe list")
    labels, pairs = set(), set()
    for probe in probes:
        fields(probe, "name source target")
        name, a, b = probe["name"], probe["source"], probe["target"]
        require(type(name) is str and bool(name) and name not in labels, "unique named probe")
        require(
            type(a) is int and type(b) is int and a in fixed and b in fixed and a < b,
            "ordered fixed probe endpoints",
        )
        require((a, b) not in pairs, "distinct fixed probe pairs")
        labels.add(name)
        pairs.add((a, b))


def law(values, m):
    require(type(values) is list and len(values) == 1 << m, "complete mask selection law")
    masses = [fraction(value) for value in values]
    require(
        all(0 <= p <= 1 for p in masses) and sum(masses, F(0)) == 1,
        "normalized nonnegative selection law",
    )
    inclusion = [F(0)] * len(masses)
    # Accumulate each original mass into every contained support, independently
    # of the source chains and their eventual use in estimates/covariances.
    for mask, mass in enumerate(masses):
        support = mask
        while True:
            inclusion[support] += mass
            if support == 0:
                break
            support = (support - 1) & mask
    require(
        inclusion[0] == 1 and all(inclusion[1 << i] > 0 for i in range(m)),
        "positive singleton support",
    )
    return masses, inclusion


def chain_vertices(kept, past, eligible, source, target, degree):
    local = {event: i for i, event in enumerate(kept)}
    a, b = local[source], local[target]
    if a not in past[b]:
        return []
    if degree == 0:
        return [[]]
    inside = [
        event
        for event in eligible
        if event in local and a in past[local[event]] and local[event] in past[b]
    ]
    if degree == 1:
        return [[event] for event in inside]
    require(degree == 2, "three declared kernel coefficients")
    answer = []
    for right in inside:
        for left in inside:
            if left < right and local[left] in past[local[right]]:
                answer.append([left, right])
    return sorted(answer)


def chain_wire(vertices, eligible, inclusion, weights):
    support = sum(1 << i for i, event in enumerate(eligible) if event in vertices)
    weight = math.prod((weights[event] for event in vertices), start=F(1))
    return {
        "vertices": vertices,
        "eligible_mask": support,
        "inclusion": wire(inclusion[support]),
        "weight": wire(weight),
    }


def observe(packet):
    native(packet)
    fields(packet, "frame_size fixed eligible probes mask_probabilities record")
    n, fixed, eligible, probes = (packet[k] for k in ("frame_size", "fixed", "eligible", "probes"))
    frame(n, fixed, eligible, probes)
    masses, inclusion = law(packet["mask_probabilities"], len(eligible))
    record = packet["record"]
    fields(record, "kept past marks")
    kept, past = record["kept"], record["past"]
    ids(kept, n)
    require(set(fixed) <= set(kept), "all fixed probe markers retained")
    validate_past(past, len(kept))
    retained = [event for event in eligible if event in kept]
    require(
        type(record["marks"]) is list and len(record["marks"]) == len(retained),
        "exact retained mark inventory",
    )
    weights = {}
    for event, mark in zip(retained, record["marks"], strict=True):
        fields(mark, "event volume")
        require(
            type(mark["event"]) is int and mark["event"] == event,
            "marks only for sorted retained eligible cells",
        )
        weights[event] = fraction(mark["volume"])
        require(weights[event] > 0, "positive supplied retained mark")
    questions = []
    for probe in probes:
        for q, alpha in enumerate(ALPHA):
            chains = [
                chain_wire(v, eligible, inclusion, weights)
                for v in chain_vertices(kept, past, eligible, probe["source"], probe["target"], q)
            ]
            raw = sum((fraction(c["weight"]) for c in chains), F(0))
            corrected, unsupported = F(0), 0
            for chain in chains:
                probability = inclusion[chain["eligible_mask"]]
                if probability:
                    corrected += fraction(chain["weight"]) / probability
                else:
                    unsupported += 1
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": q,
                    "chains": chains,
                    "unsupported_observed_terms": unsupported,
                    "estimates": {
                        "raw": wire(alpha * raw),
                        "joint_supported": wire(alpha * corrected),
                    },
                }
            )
    mask = sum(1 << i for i, event in enumerate(eligible) if event in kept)
    return detached(
        {
            "mask": mask,
            "probability": wire(masses[mask]),
            "possible": bool(masses[mask]),
            "record": record,
            "packet_sha256": hashlib.sha256(canonical(packet)).hexdigest(),
            "questions": questions,
        }
    )


def rectangle(values):
    require(type(values) is list and len(values) == 4, "four-coordinate rectangle")
    rect = [fraction(value) for value in values]
    require(rect[0] < rect[1] and rect[2] < rect[3], "positive cell rectangle")
    return rect


def area(rect):
    return (rect[1] - rect[0]) * (rect[3] - rect[2]) / 2


def precedes(a, b):
    return a[0] < b[0] and a[1] < b[1]


def clipped(rect, query):
    ul, vl = max(rect[0], query[0]), max(rect[2], query[2])
    return [ul, max(ul, min(rect[1], query[1])), vl, max(vl, min(rect[3], query[3]))]


def source_data(source, design):
    native(source)
    native(design)
    fields(source, "name coordinates past fixed eligible probes cells mark_kind")
    fields(design, "name mask_probabilities")
    require(
        type(source["name"]) is str and type(design["name"]) is str, "named private source/design"
    )
    require(type(source["coordinates"]) is list, "coordinate list")
    coords = []
    for row in source["coordinates"]:
        require(type(row) is list and len(row) == 2, "two null coordinates")
        coords.append([fraction(v) for v in row])
    n, eligible = len(coords), source["eligible"]
    frame(n, source["fixed"], eligible, source["probes"])
    validate_past(source["past"], n)
    computed = [[i for i in range(n) if precedes(coords[i], coords[j])] for j in range(n)]
    require(
        all(i < j for j, row in enumerate(computed) for i in row), "original IDs are topological"
    )
    require(computed == source["past"], "source order must match strict coordinate order")
    require(
        type(source["cells"]) is list and len(source["cells"]) == len(eligible),
        "complete source cells",
    )
    bounds, true_weights, supplied_weights = {}, {}, {}
    for event, cell in zip(eligible, source["cells"], strict=True):
        fields(cell, "event bounds geometric_mark supplied_mark")
        require(
            type(cell["event"]) is int and cell["event"] == event, "eligible-ordered source cells"
        )
        rect = rectangle(cell["bounds"])
        require(
            rect[0] < coords[event][0] < rect[1] and rect[2] < coords[event][1] < rect[3],
            "representative strictly inside its cell",
        )
        geometric, supplied = area(rect), fraction(cell["supplied_mark"])
        require(
            geometric == fraction(cell["geometric_mark"]),
            "geometric mark independently agrees with bounds",
        )
        require(supplied > 0, "positive supplied source mark")
        bounds[event], true_weights[event], supplied_weights[event] = rect, geometric, supplied
    masses, inclusion = law(design["mask_probabilities"], len(eligible))
    return coords, bounds, true_weights, supplied_weights, masses, inclusion


def probe_geometry(probe, source, coords, bounds, true_weights):
    a, b = coords[probe["source"]], coords[probe["target"]]
    require(precedes(a, b), "strictly timelike supplied source probe")
    query = [a[0], b[0], a[1], b[1]]
    V = area(query)
    eligible = source["eligible"]
    clips = {event: clipped(bounds[event], query) for event in eligible}
    h = {event: area(clips[event]) for event in eligible}
    require(sum(h.values(), F(0)) == V, "clipped cell measures cover query")
    pair_cells, K, cross, diagonal = [], F(0), F(0), F(0)
    for first in eligible:
        left = clips[first]
        for second in eligible:
            right = clips[second]
            integral = (
                causal_area(left[0], left[1], right[0], right[1])
                * causal_area(left[2], left[3], right[2], right[3])
                / 4
            )
            product = h[first] * h[second]
            ordered = precedes(coords[first], coords[second])
            pair_cells.append(
                {
                    "first": first,
                    "second": second,
                    "representative_precedes": ordered,
                    "clipped_product": wire(product),
                    "causal_integral": wire(integral),
                }
            )
            if first == second:
                require(
                    not ordered and integral == h[first] ** 2 / 4,
                    "distinct within-cell continuum pairs, not self representatives",
                )
                diagonal += integral
            else:
                cross += integral
                if ordered:
                    K += product
    vertices = chain_vertices(
        list(range(len(coords))), source["past"], eligible, probe["source"], probe["target"], 2
    )
    Pg = sum((true_weights[i] * true_weights[j] for i, j in vertices), F(0))
    continuum = V * V / 4
    require(
        cross + diagonal == continuum, "all ordered cell integrals recover continuum pair measure"
    )
    boundary, cross_error, omission = Pg - K, K - cross, -diagonal
    require(
        Pg - continuum == boundary + cross_error + omission, "three signed pair-discrepancy terms"
    )
    discrepancy = {
        "geometric_target": Pg,
        "clipped_order_sum": K,
        "cross_cell_integral": cross,
        "within_cell_integral": diagonal,
        "continuum_pair": continuum,
        "boundary_error": boundary,
        "cross_order_error": cross_error,
        "omission_error": omission,
        "total_error": Pg - continuum,
    }
    return {
        "probe": probe["name"],
        "volume": wire(V),
        "cell_clips": [{"event": event, "volume": wire(h[event])} for event in eligible],
        "pair_cells": pair_cells,
        "pair_discrepancy": {key: wire(value) for key, value in discrepancy.items()},
    }


def population(source, geometry, true_weights, weights, inclusion):
    rows = []
    kept = list(range(len(source["past"])))
    for probe, geometric in zip(source["probes"], geometry, strict=True):
        V = fraction(geometric["volume"])
        continuum = (F(1, 2), -V / 4, V * V / 32)
        for q, alpha in enumerate(ALPHA):
            vertices = chain_vertices(
                kept, source["past"], source["eligible"], probe["source"], probe["target"], q
            )
            chains = [chain_wire(v, source["eligible"], inclusion, weights) for v in vertices]
            T = alpha * sum((fraction(c["weight"]) for c in chains), F(0))
            G = alpha * sum(
                (math.prod((true_weights[event] for event in v), start=F(1)) for v in vertices),
                F(0),
            )
            supported = alpha * sum(
                (fraction(c["weight"]) for c in chains if inclusion[c["eligible_mask"]] > 0), F(0)
            )
            omitted = [c["vertices"] for c in chains if inclusion[c["eligible_mask"]] == 0]
            if q == 2:
                require(
                    G == alpha * fraction(geometric["pair_discrepancy"]["geometric_target"]),
                    "pair geometry / coefficient target bridge",
                )
            rows.append(
                {
                    "probe": probe["name"],
                    "degree": q,
                    "scale": wire(alpha),
                    "chains": chains,
                    "supplied_target": wire(T),
                    "geometric_target": wire(G),
                    "continuum_target": wire(continuum[q]),
                    "supported_target": wire(supported),
                    "unsupported_chains": omitted,
                    "annotation_error": wire(T - G),
                    "quadrature_error": wire(G - continuum[q]),
                    "full_target_supported": not omitted,
                }
            )
    return rows


def make_packet(source, design, mask):
    kept = sorted(
        source["fixed"] + [event for i, event in enumerate(source["eligible"]) if mask & (1 << i)]
    )
    index = {event: i for i, event in enumerate(kept)}
    return {
        "frame_size": len(source["past"]),
        "fixed": source["fixed"],
        "eligible": source["eligible"],
        "probes": source["probes"],
        "mask_probabilities": design["mask_probabilities"],
        "record": {
            "kept": kept,
            "past": [[index[v] for v in source["past"][event] if v in index] for event in kept],
            "marks": [
                {"event": c["event"], "volume": c["supplied_mark"]}
                for c in source["cells"]
                if c["event"] in index
            ],
        },
    }


def sampling_moments(pop, samples):
    positive = [sample for sample in samples if sample["possible"]]
    probabilities = [fraction(sample["probability"]) for sample in positive]
    Q = len(pop)
    result = {}
    for method in METHODS:
        values = [
            [fraction(q["estimates"][method]) for q in sample["questions"]] for sample in positive
        ]
        mean = [
            sum((p * row[i] for p, row in zip(probabilities, values, strict=True)), F(0))
            for i in range(Q)
        ]
        covariance = [[F(0)] * Q for _ in range(Q)]
        for i in range(Q):
            for j in range(i, Q):
                second = sum(
                    (p * row[i] * row[j] for p, row in zip(probabilities, values, strict=True)),
                    F(0),
                )
                covariance[i][j] = covariance[j][i] = second - mean[i] * mean[j]
            require(covariance[i][i] >= 0, "nonnegative exact variance")
        bias, errors = [], []
        for mu, question in zip(mean, pop, strict=True):
            T, G, C = [
                fraction(question[key])
                for key in ("supplied_target", "geometric_target", "continuum_target")
            ]
            sampling, annotation, quadrature = mu - T, T - G, G - C
            require(mu - C == sampling + annotation + quadrature, "three signed coefficient errors")
            bias.append(sampling)
            errors.append(
                {
                    "probe": question["probe"],
                    "degree": question["degree"],
                    "sampling_bias": wire(sampling),
                    "annotation_error": wire(annotation),
                    "quadrature_error": wire(quadrature),
                    "total_error": wire(mu - C),
                }
            )
        result[method] = {
            "mean": vector(mean),
            "bias": vector(bias),
            "covariance": matrix(covariance),
            "errors": errors,
        }
    require(
        result["joint_supported"]["mean"] == [q["supported_target"] for q in pop],
        "supported target, not automatically full target, is unbiased",
    )
    return result


def union_covariance(pop, inclusion):
    supported = [
        [
            (c["eligible_mask"], fraction(c["weight"]))
            for c in q["chains"]
            if inclusion[c["eligible_mask"]] > 0
        ]
        for q in pop
    ]
    covariance, pairs, zero, maximum = [], 0, 0, 0
    for i, left in enumerate(supported):
        row = []
        for j, right in enumerate(supported):
            value = F(0)
            for a, wa in left:
                for b, wb in right:
                    union = a | b
                    value += wa * wb * (inclusion[union] / (inclusion[a] * inclusion[b]) - 1)
                    pairs += 1
                    zero += inclusion[union] == 0
                    maximum = max(maximum, union.bit_count())
            row.append(fraction(pop[i]["scale"]) * fraction(pop[j]["scale"]) * value)
        covariance.append(row)
    return matrix(covariance), pairs, zero, maximum


def build_case(case_id, level, source, design):
    require(type(case_id) is str and type(level) is str, "named private case/level")
    coords, bounds, true_weights, weights, masses, inclusion = source_data(source, design)
    geometry = [
        probe_geometry(probe, source, coords, bounds, true_weights) for probe in source["probes"]
    ]
    pop = population(source, geometry, true_weights, weights, inclusion)
    samples = [observe(make_packet(source, design, mask)) for mask in range(len(masses))]
    moments = sampling_moments(pop, samples)
    covariance, pairs, zero, maximum = union_covariance(pop, inclusion)
    require(
        covariance == moments["joint_supported"]["covariance"],
        "independent source-union / sample-second-moment covariance",
    )
    result = {
        "case_id": case_id,
        "level": level,
        "source": source,
        "design": design,
        "geometry": geometry,
        "population": pop,
        "samples": samples,
        "moments": moments,
        "union_covariance": covariance,
        "counts": {
            "mask_rows": len(samples),
            "positive_rows": sum(s["possible"] for s in samples),
            "questions": len(pop),
            "source_chain_terms": sum(len(q["chains"]) for q in pop),
            "observed_chain_terms": sum(len(q["chains"]) for s in samples for q in s["questions"]),
            "ordered_supported_chain_pairs": pairs,
            "zero_union_pairs": zero,
            "max_union_size": maximum,
        },
    }
    return detached(result)
