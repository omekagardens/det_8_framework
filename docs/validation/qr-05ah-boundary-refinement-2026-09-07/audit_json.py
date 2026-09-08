"""Independent stdlib JSON-only raw QR-05AH certificate and observation audit.

No engine, runner or test imports. Own AG observer and exact arithmetic
lineage is statically carried. New geometry, refinements and all sampling laws
are independently rebuilt; only nine complete pinned AG cases are consumed.
"""

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
import time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AGDIR = ROOT / "docs/validation/qr-05ag-local-volume-2026-09-07"
AG_PRIOR = "qr-05ag-local-volume-2026-09-07/results.json"
AG_ID = {
    "bytes": 3027867,
    "sha256": "5af957be534af3096c7f61ec444349ec49c739ebf70364146b7f4568a8832f91",
}
METHODS = ("raw", "uniform_rate", "inclusion")
PACKET_SCOPE = (
    "missing_marks_inferred",
    "source_moments_inferred",
    "geometry_inferred",
    "mark_origin_authenticated",
    "observation_origin_authenticated",
)
CERT_SCOPE = (
    "observer_has_geometry",
    "marks_authenticated",
    "unknown_geometry_reconstructed",
    "monotone_absolute_error_guaranteed",
    "continuum_limit_established",
    "gravity_derived",
)
SUITE_SCOPE = (
    "unknown_geometry_reconstructed",
    "continuum_limit_established",
    "marks_authenticated",
    "observer_bounds_inferred",
    "monotone_absolute_error_guaranteed",
    "cross_level_observation_transport_proved",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
)

COUNTS = defaultdict(int)


def check(condition, message):
    COUNTS["checks"] += 1
    if not condition:
        raise RuntimeError(message)


def eq(left, right, message):
    check(left == right, message)


def canon(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def digest(value):
    return hashlib.sha256(canon(value)).hexdigest()


def ident(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def native_tree(value, depth=0):
    check(depth <= 128, "native mathematical depth")
    kind = type(value)
    if value is None or kind in (str, bool):
        return
    if kind is int:
        check(abs(value).bit_length() <= 4096, "native integer bits")
        return
    check(kind in (list, dict), "native mathematical JSON value")
    if kind is dict:
        check(all(type(k) is str for k in value), "native dictionary keys")
        children = value.values()
    else:
        children = value
    for child in children:
        native_tree(child, depth + 1)


def native_eq(left, right, message):
    check(canon(left) == canon(right), message)


def fields(value, names, message):
    check(type(value) is dict and set(value) == set(names.split()), message + " fields")


def fraction(value, lower=None, upper=None):
    check(
        type(value) is list and len(value) == 2 and all(type(x) is int for x in value),
        "native reduced fraction pair",
    )
    n, d = value
    check(d > 0 and math.gcd(n, d) == 1, "canonical fraction")
    check(max(abs(n).bit_length(), d.bit_length()) <= 4096, "fraction component bits")
    result = F(n, d)
    check(
        (lower is None or result >= lower) and (upper is None or result <= upper),
        "fraction interval",
    )
    return result


def wire(value):
    check(type(value) is F, "exact retained fraction")
    check(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
        "retained reduced component bits",
    )
    return [value.numerator, value.denominator]


def old_fraction(value):
    check(type(value) is str, "pinned D/E rational string")
    parsed = F(value)
    eq(str(parsed), value, "canonical pinned rational string")
    check(
        max(abs(parsed.numerator).bit_length(), parsed.denominator.bit_length()) <= 4096,
        "pinned rational bits",
    )
    return parsed


def exact_ids(value, n):
    check(
        type(value) is list and all(type(i) is int and 0 <= i < n for i in value),
        "native bounded ID list",
    )
    native_eq(value, sorted(set(value)), "strict sorted ID list")


def marginal_probabilities(masses):
    result = []
    for bit in range(len(masses).bit_length() - 1):
        terms = [p for mask, p in enumerate(masses) if mask & (1 << bit)]
        result.append(sum(terms, F(0)))
        COUNTS["marginal_mass_terms"] += len(terms)
    return result


def membership(kept, past, a, b, eligible):
    position = {event: i for i, event in enumerate(kept)}
    answer = []
    for event in kept:
        if event in eligible:
            if position[a] in past[position[event]] and position[event] in past[position[b]]:
                answer.append(event)
            COUNTS["eligible_member_candidates"] += 1
    return answer


def expected_packet(problem):
    """Generic full-wire regression helper without hidden-source arguments."""
    native_tree(problem)
    fields(
        problem,
        "schema_version family frame_size fixed eligible probes mask_probabilities record",
        "AG problem",
    )
    native_eq(problem["schema_version"], "det8-qr05ag-problem-v1", "AG schema")
    native_eq(problem["family"], "qr05ag_local_volume", "AG family")
    n = problem["frame_size"]
    check(type(n) is int and 3 <= n <= 12, "AG native bounded frame")
    fixed, eligible = problem["fixed"], problem["eligible"]
    exact_ids(fixed, n)
    exact_ids(eligible, n)
    check(len(fixed) >= 2 and 1 <= len(eligible) <= 8, "bounded marked/eligible frame")
    native_eq(sorted(fixed + eligible), list(range(n)), "complete disjoint ID partition")
    probes = problem["probes"]
    check(type(probes) is list and 1 <= len(probes) <= 8, "bounded probe list")
    labels, pairs = set(), set()
    for probe in probes:
        fields(probe, "name source target", "probe")
        a, b, name = probe["source"], probe["target"], probe["name"]
        check(type(name) is str and re.fullmatch(r"[a-z][a-z0-9_]{0,39}", name), "valid probe name")
        check(name not in labels, "unique probe name")
        check(
            type(a) is int and type(b) is int and a in fixed and b in fixed and a < b,
            "native ordered fixed probe IDs",
        )
        check((a, b) not in pairs, "unique probe endpoints")
        labels.add(name)
        pairs.add((a, b))
    M, P = len(eligible), len(probes)
    L = 1 << M
    check(
        type(problem["mask_probabilities"]) is list and len(problem["mask_probabilities"]) == L,
        "complete selection law",
    )
    masses = [fraction(p, F(0), F(1)) for p in problem["mask_probabilities"]]
    eq(sum(masses, F(0)), F(1), "normalized original mask law")
    record = problem["record"]
    fields(record, "kept past marks", "record")
    kept, past = record["kept"], record["past"]
    exact_ids(kept, n)
    check(set(fixed) <= set(kept), "all fixed markers retained")
    check(type(past) is list and len(past) == len(kept), "aligned observed past")
    for i, row in enumerate(past):
        exact_ids(row, i)
        for ancestor in row:
            check(set(past[ancestor]) <= set(row), "transitivity without repair")
    retained = [event for event in eligible if event in kept]
    marks = record["marks"]
    check(type(marks) is list and len(marks) == len(retained), "exact mark row count")
    volumes = {}
    for event, row in zip(retained, marks, strict=True):
        fields(row, "event volume", "retained mark")
        check(
            type(row["event"]) is int and row["event"] == event,
            "sorted retained eligible marks only",
        )
        value = fraction(row["volume"])
        check(value > 0, "positive volume mark")
        volumes[event] = value
    K = len(retained)
    I, C = M * (1 << (M - 1)), P * K
    W = L + I + 4 * C + 3 * P
    check(I <= 1024 and C <= 64 and 3 * C <= 192 and W <= 2000, "complete logical work reservation")
    check(len(canon(problem)) <= 4194304, "public input canonical bytes")
    marginal = marginal_probabilities(masses)
    check(all(p > 0 for p in marginal), "all full-frame singleton marginals positive")
    mean_rate = sum(marginal, F(0)) / M
    pi = dict(zip(eligible, marginal, strict=True))
    questions, A = [], 0
    for probe in probes:
        members = membership(kept, past, probe["source"], probe["target"], eligible)
        raw = sum((volumes[event] for event in members), F(0))
        corrected = sum((volumes[event] / pi[event] for event in members), F(0))
        estimates = {"raw": raw, "uniform_rate": raw / mean_rate, "inclusion": corrected}
        questions.append(
            {
                "probe": probe["name"],
                "observed_cells": [
                    {"event": event, "volume": wire(volumes[event]), "inclusion": wire(pi[event])}
                    for event in members
                ],
                "estimates": {method: wire(estimates[method]) for method in METHODS},
            }
        )
        A += len(members)
    mask = sum(1 << i for i, event in enumerate(eligible) if event in kept)
    answer = {
        "input_sha256": digest(problem),
        "mask": mask,
        "probability": wire(masses[mask]),
        "possible": bool(masses[mask]),
        "marginals": [wire(p) for p in marginal],
        "questions": questions,
        "counts": {
            "events": n,
            "eligible_events": M,
            "kept_events": len(kept),
            "retained_cells": K,
            "mask_rows": L,
            "questions": P,
            "inclusion_terms": I,
            "member_candidates": C,
            "observed_member_terms": A,
            "estimator_terms": 3 * A,
            "reserved_estimator_terms": 3 * C,
            "reserved_total_work": W,
            "total_work": L + I + C + 3 * A + 3 * P,
        },
        "scope": dict.fromkeys(PACKET_SCOPE, False),
    }
    native_tree(answer)
    check(len(canon(answer)) <= 4194304, "public output canonical bytes")
    return json.loads(canon(answer))


def vector(values):
    return [wire(F(value)) for value in values]


def matrix(rows):
    return [vector(row) for row in rows]


def design_moments(pop, samples):
    P = len(pop)
    positive = [s for s in samples if s["analysis"]["possible"]]
    masses = [fraction(s["analysis"]["probability"]) for s in positive]
    result = {}
    for method in METHODS:
        values = [
            [fraction(q["estimates"][method]) for q in s["analysis"]["questions"]] for s in positive
        ]
        mean = [
            sum((p * row[i] for p, row in zip(masses, values, strict=True)), F(0)) for i in range(P)
        ]
        covariance = [[F(0)] * P for _ in range(P)]
        for i in range(P):
            for j in range(i, P):
                second = sum(
                    (p * row[i] * row[j] for p, row in zip(masses, values, strict=True)), F(0)
                )
                centered = sum(
                    (
                        p * (row[i] - mean[i]) * (row[j] - mean[j])
                        for p, row in zip(masses, values, strict=True)
                    ),
                    F(0),
                )
                eq(
                    second - mean[i] * mean[j],
                    centered,
                    "independent centered/second-moment covariance",
                )
                covariance[i][j] = covariance[j][i] = centered
                COUNTS["centered_covariance_entries"] += 1
                COUNTS["centered_outer_product_terms"] += len(masses)
            check(covariance[i][i] >= 0, "nonnegative variance from centered Gram identity")
        biases, decompositions = [], []
        for q, mu in zip(pop, mean, strict=True):
            T, G, V = [
                fraction(q[k]) for k in ("supplied_target", "geometric_target", "continuum_volume")
            ]
            sampling, annotation, quadrature = mu - T, T - G, G - V
            total = mu - V
            eq(total, sampling + annotation + quadrature, "three separate signed errors")
            biases.append(sampling)
            decompositions.append(
                {
                    "probe": q["probe"],
                    "mean": wire(mu),
                    "finite_target": wire(T),
                    "true_finite_target": wire(G),
                    "continuum": wire(V),
                    "sampling_bias": wire(sampling),
                    "annotation_error": wire(annotation),
                    "quadrature_error": wire(quadrature),
                    "total_error": wire(total),
                }
            )
            COUNTS["signed_three_error_decompositions"] += 1
        result[method] = {
            "mean": vector(mean),
            "bias": vector(biases),
            "covariance": matrix(covariance),
            "decompositions": decompositions,
        }
    native_eq(
        result["inclusion"]["bias"],
        vector(F(0) for _ in pop),
        "positive singleton support suffices for all linear means",
    )
    return result


def cell_covariance(source, pop, design):
    """Build one full cell-indicator covariance, then project it into probes."""
    masses = [fraction(p) for p in design["mask_probabilities"]]
    pi = marginal_probabilities(masses)
    cells = source["cells"]
    index = {c["event"]: i for i, c in enumerate(cells)}
    weights = [fraction(c["supplied_mark"]) for c in cells]
    covariance, joint = [], []
    for i in range(len(cells)):
        row, pair_row = [], []
        for j in range(len(cells)):
            probability = sum(
                (p for mask, p in enumerate(masses) if mask & (1 << i) and mask & (1 << j)), F(0)
            )
            if i == j:
                eq(probability, pi[i], "diagonal pair inclusion equals singleton")
            row.append(weights[i] * weights[j] * (probability / (pi[i] * pi[j]) - 1))
            pair_row.append(probability)
            COUNTS["full_cell_covariance_entries"] += 1
        covariance.append(row)
        joint.append(pair_row)
    result, pairs, zero = [], 0, 0
    for a in pop:
        row = []
        for b in pop:
            total = F(0)
            for event_a in a["members"]:
                for event_b in b["members"]:
                    i, j = index[event_a], index[event_b]
                    total += covariance[i][j]
                    pairs += 1
                    zero += joint[i][j] == 0
                    COUNTS["ordered_probe_cell_pairs"] += 1
            row.append(total)
        result.append(row)
    COUNTS["zero_joint_probe_cell_pairs"] += zero
    return matrix(result), pairs, zero


def same(left, right):
    return canon(left) == canon(right)


def field_vector(case, field):
    return [q[field] for q in case["population"]]


def positive_law(case):
    return [
        {"problem": s["problem"], "probability": s["analysis"]["probability"]}
        for s in case["samples"]
        if s["analysis"]["possible"]
    ]


def unmarked_projection(case):
    """Information erasure only; these are never submitted as valid packets."""
    packets = []
    for sample in case["samples"]:
        packet = {key: value for key, value in sample["problem"].items() if key != "record"}
        packet["record"] = {
            key: value for key, value in sample["problem"]["record"].items() if key != "marks"
        }
        packets.append(packet)
    return packets


def packet_scaling(base, other, factor):
    scaled = []
    for sample in base["samples"]:
        problem = json.loads(canon(sample["problem"]))
        for row in problem["record"]["marks"]:
            row["volume"] = wire(fraction(row["volume"]) * factor)
        # Independently re-evaluate the complete scaled observer output instead
        # of merely multiplying the retained old estimate fields.
        scaled.append({"problem": problem, "analysis": expected_packet(problem)})
    return same(scaled, other["samples"])


def scaled_population(pop, factor):
    result = []
    for row in pop:
        transformed = {key: row[key] for key in ("probe", "members")}
        for key in (
            "supplied_target",
            "geometric_target",
            "continuum_volume",
            "annotation_error",
            "quadrature_error",
        ):
            transformed[key] = wire(fraction(row[key]) * factor)
        transformed["overlaps"] = [
            {"event": c["event"], "volume": wire(fraction(c["volume"]) * factor)}
            for c in row["overlaps"]
        ]
        result.append(transformed)
    return result


def scaled_moments(moments, factor):
    result = {}
    for method in METHODS:
        old = moments[method]
        result[method] = {
            "mean": vector(fraction(v) * factor for v in old["mean"]),
            "bias": vector(fraction(v) * factor for v in old["bias"]),
            "covariance": matrix(
                [[fraction(v) * factor**2 for v in row] for row in old["covariance"]]
            ),
            "decompositions": [
                {
                    key: value if key == "probe" else wire(fraction(value) * factor)
                    for key, value in row.items()
                }
                for row in old["decompositions"]
            ],
        }
    return result


def rectangle(values):
    check(type(values) is list and len(values) == 4, "native four-coordinate rectangle")
    rect = [fraction(value) for value in values]
    check(rect[0] < rect[1] and rect[2] < rect[3], "positive rectangle widths")
    return rect


def contained(inner, outer):
    return (
        outer[0] <= inner[0]
        and inner[1] <= outer[1]
        and outer[2] <= inner[2]
        and inner[3] <= outer[3]
    )


def rect_area(rect):
    return (rect[1] - rect[0]) * (rect[3] - rect[2]) / 2


def point_inside(point, rect):
    return rect[0] < point[0] < rect[1] and rect[2] < point[1] < rect[3]


def overlap_length(left, right, a, b):
    cuts = sorted({left, right, a, b})
    result = F(0)
    for low, high in itertools.pairwise(cuts):
        middle = (low + high) / 2
        if left < middle < right and a < middle < b:
            result += high - low
        COUNTS["overlap_indicator_segments"] += 1
    return result


def overlap_area(a, b):
    return overlap_length(a[0], a[1], b[0], b[1]) * overlap_length(a[2], a[3], b[2], b[3]) / 2


def tile_partition(domain, cells):
    """Explicit exact coverage, used for whole levels AND each declared parent."""
    xs = sorted({domain[0], domain[1]} | {x for c in cells for x in c["bounds"][:2]})
    ys = sorted({domain[2], domain[3]} | {y for c in cells for y in c["bounds"][2:]})
    covered_area = F(0)
    for xl, xh in itertools.pairwise(xs):
        for yl, yh in itertools.pairwise(ys):
            middle = ((xl + xh) / 2, (yl + yh) / 2)
            count = 0
            for cell in cells:
                count += point_inside(middle, cell["bounds"])
                COUNTS["partition_tile_cell_checks"] += 1
            eq(count, 1, "exactly one interior covers each endpoint tile")
            covered_area += (xh - xl) * (yh - yl) / 2
    eq(covered_area, rect_area(domain), "all endpoint tiles cover domain area")
    eq(
        sum((rect_area(c["bounds"]) for c in cells), F(0)),
        rect_area(domain),
        "partition area consequence, not sole proof",
    )


def parsed_certificate(problem):
    native_tree(problem)
    fields(problem, "schema_version family domain probes levels", "AH certificate input")
    native_eq(problem["schema_version"], "det8-qr05ah-problem-v1", "AH certificate schema")
    native_eq(problem["family"], "qr05ah_partition_bounds", "AH certificate family")
    domain = rectangle(problem["domain"])

    def name(value):
        check(
            type(value) is str and re.fullmatch(r"[a-z][a-z0-9_]{0,39}", value),
            "bounded native name",
        )
        return value

    check(type(problem["probes"]) is list and 1 <= len(problem["probes"]) <= 8, "probe cap")
    probes = []
    for row in problem["probes"]:
        fields(row, "name bounds", "certificate probe")
        q = {"name": name(row["name"]), "bounds": rectangle(row["bounds"])}
        check(contained(q["bounds"], domain), "contained probe")
        probes.append(q)
    eq(len({q["name"] for q in probes}), len(probes), "unique probe names")
    check(type(problem["levels"]) is list and 1 <= len(problem["levels"]) <= 4, "level cap")
    levels, previous = [], {}
    for i, raw_level in enumerate(problem["levels"]):
        fields(raw_level, "name cells", "certificate level")
        check(
            type(raw_level["cells"]) is list and 1 <= len(raw_level["cells"]) <= 8,
            "per-level cell cap",
        )
        cells = []
        for row in raw_level["cells"]:
            fields(row, "name parent bounds representative volume", "certificate cell")
            rect = rectangle(row["bounds"])
            check(contained(rect, domain), "contained full-source cell")
            check(
                type(row["representative"]) is list and len(row["representative"]) == 2,
                "two-coordinate representative",
            )
            point = [fraction(v) for v in row["representative"]]
            check(point_inside(point, rect), "strict cell representative interiority")
            volume = fraction(row["volume"])
            check(volume > 0, "positive supplied mark")
            parent = row["parent"]
            if i:
                check(type(parent) is str and parent in previous, "previous-level parent name")
                check(
                    contained(rect, previous[parent]["bounds"]), "child inside its declared parent"
                )
            else:
                check(parent is None, "initial null parent")
            cells.append(
                {
                    "name": name(row["name"]),
                    "parent": parent,
                    "bounds": rect,
                    "representative": point,
                    "volume": volume,
                }
            )
        names = [c["name"] for c in cells]
        native_eq(names, sorted(set(names)), "unique name-sorted cells")
        levels.append({"name": name(raw_level["name"]), "cells": cells})
        previous = {c["name"]: c for c in cells}
    eq(len({level["name"] for level in levels}), len(levels), "distinct ordered level names")
    sizes = [len(level["cells"]) for level in levels]
    T = sum(c * (2 * c + 1) ** 2 for c in sizes)
    D = sum(c * (c - 1) // 2 for c in sizes)
    Q, R = len(probes) * sum(sizes), sum(sizes[1:])
    W = T + D + 3 * Q + R
    check(T <= 9248 and D <= 112 and Q <= 256 and W <= 12000, "complete AH work reservation")
    check(len(canon(problem)) <= 4194304, "AH public canonical byte cap")
    counts = {
        "levels": len(levels),
        "cells": sum(sizes),
        "probes": len(probes),
        "tile_checks": T,
        "pair_checks": D,
        "query_cell_terms": Q,
        "refinement_links": R,
        "total_work": W,
    }
    return domain, probes, levels, counts


def expected_certificate(problem):
    """Complete generic source-aware certificate oracle, independent of engines."""
    domain, probes, levels, counts = parsed_certificate(problem)
    parent_rows = []
    for level in levels:
        tile_partition(domain, level["cells"])
    for old, new in itertools.pairwise(levels):
        rows = []
        for parent in old["cells"]:
            children = [c for c in new["cells"] if c["parent"] == parent["name"]]
            check(bool(children), "every declared parent has children")
            tile_partition(parent["bounds"], children)
            supplied = sum((c["volume"] for c in children), F(0))
            eq(supplied, parent["volume"], "per-parent supplied additivity")
            rows.append(
                {
                    "parent": parent["name"],
                    "children": [c["name"] for c in children],
                    "geometric_volume": wire(rect_area(parent["bounds"])),
                    "supplied_volume": wire(supplied),
                }
            )
        parent_rows.append(rows)
    results = []
    for level in levels:
        questions = []
        for probe in probes:
            inside_names, outside_names, selected_names = [], [], []
            L, U, G, T = F(0), F(0), F(0), F(0)
            V = rect_area(probe["bounds"])
            for cell in level["cells"]:
                area = rect_area(cell["bounds"])
                overlap = overlap_area(cell["bounds"], probe["bounds"])
                if overlap == area:
                    inside_names.append(cell["name"])
                    L += area
                if overlap > 0:
                    outside_names.append(cell["name"])
                    U += area
                if point_inside(cell["representative"], probe["bounds"]):
                    selected_names.append(cell["name"])
                    G += area
                    T += cell["volume"]
            check(L <= G <= U and L <= V <= U, "two geometric enclosures")
            gap, error = U - L, G - V
            check(
                G - U <= error <= G - L and abs(error) <= gap,
                "signed and absolute quadrature enclosure",
            )
            scalars = {
                "lower_bound": L,
                "upper_bound": U,
                "boundary_gap": gap,
                "geometric_target": G,
                "supplied_target": T,
                "continuum_volume": V,
                "annotation_error": T - G,
                "quadrature_error": error,
                "total_error": T - V,
                "error_lower": G - U,
                "error_upper": G - L,
            }
            questions.append(
                {
                    "probe": probe["name"],
                    "inner_cells": inside_names,
                    "outer_cells": outside_names,
                    "representative_cells": selected_names,
                    **{k: wire(v) for k, v in scalars.items()},
                }
            )
            COUNTS["geometric_enclosure_questions"] += 1
        results.append(
            {
                "name": level["name"],
                "cells": [
                    {
                        "name": c["name"],
                        "geometric_volume": wire(rect_area(c["bounds"])),
                        "annotation_error": wire(c["volume"] - rect_area(c["bounds"])),
                    }
                    for c in level["cells"]
                ],
                "questions": questions,
            }
        )
    refinements = []
    for i, (coarse, fine) in enumerate(itertools.pairwise(results)):
        changes = []
        for old, new in zip(coarse["questions"], fine["questions"], strict=True):
            lower = fraction(new["lower_bound"]) - fraction(old["lower_bound"])
            upper = fraction(old["upper_bound"]) - fraction(new["upper_bound"])
            gap = fraction(old["boundary_gap"]) - fraction(new["boundary_gap"])
            error_change = fraction(new["quadrature_error"]) - fraction(old["quadrature_error"])
            absolute_change = abs(fraction(new["quadrature_error"])) - abs(
                fraction(old["quadrature_error"])
            )
            check(lower >= 0 and upper >= 0 and gap >= 0, "nested lower/upper/gap monotonicity")
            changes.append(
                {
                    "probe": old["probe"],
                    "lower_gain": wire(lower),
                    "upper_drop": wire(upper),
                    "gap_drop": wire(gap),
                    "quadrature_error_change": wire(error_change),
                    "absolute_error_change": wire(absolute_change),
                }
            )
        refinements.append(
            {
                "coarse": coarse["name"],
                "fine": fine["name"],
                "parents": parent_rows[i],
                "questions": changes,
            }
        )
    result = {
        "input_sha256": digest(problem),
        "domain_volume": wire(rect_area(domain)),
        "levels": results,
        "refinements": refinements,
        "counts": counts,
        "scope": dict.fromkeys(CERT_SCOPE, False),
    }
    native_tree(result)
    check(len(canon(result)) <= 4194304, "AH retained public output byte cap")
    return json.loads(canon(result))


def raw_packet(source, design, mask):
    eligible_kept = {event for i, event in enumerate(source["eligible"]) if mask & (1 << i)}
    kept = sorted(set(source["fixed"]) | eligible_kept)
    index = {event: i for i, event in enumerate(kept)}
    return {
        "schema_version": "det8-qr05ag-problem-v1",
        "family": "qr05ag_local_volume",
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
                if c["event"] in eligible_kept
            ],
        },
    }


def population(source):
    coords = [[fraction(v) for v in row] for row in source["coordinates"]]
    result = []
    for probe in source["probes"]:
        a, b = probe["source"], probe["target"]
        au, av = coords[a]
        bu, bv = coords[b]
        check(au < bu and av < bv, "strict supplied timelike probe")
        members = [
            c["event"]
            for c in source["cells"]
            if au < coords[c["event"]][0] < bu and av < coords[c["event"]][1] < bv
        ]
        by_order = membership(list(range(len(coords))), source["past"], a, b, source["eligible"])
        native_eq(members, by_order, "raw coordinates / transitive membership bridge")
        T = sum(
            (fraction(c["supplied_mark"]) for c in source["cells"] if c["event"] in members), F(0)
        )
        G = sum(
            (fraction(c["geometric_mark"]) for c in source["cells"] if c["event"] in members), F(0)
        )
        V = (bu - au) * (bv - av) / 2
        overlaps = []
        for cell in source["cells"]:
            ul, uh, vl, vh = [fraction(v) for v in cell["bounds"]]
            area = overlap_length(ul, uh, au, bu) * overlap_length(vl, vh, av, bv) / 2
            overlaps.append({"event": cell["event"], "volume": wire(area)})
        eq(
            sum((fraction(c["volume"]) for c in overlaps), F(0)),
            V,
            "partition indicator integral equals continuum rectangle",
        )
        result.append(
            {
                "probe": probe["name"],
                "members": members,
                "supplied_target": wire(T),
                "geometric_target": wire(G),
                "continuum_volume": wire(V),
                "annotation_error": wire(T - G),
                "quadrature_error": wire(G - V),
                "overlaps": overlaps,
            }
        )
    return result


FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")
LEVELS = ("l0", "l1", "l2")
PROBE_LABELS = (
    ("whole", "bottom", "top"),
    ("lower_aligned", "bottom", "aligned"),
    ("upper_aligned", "aligned", "top"),
    ("lower_unaligned", "bottom", "unaligned"),
    ("upper_unaligned", "unaligned", "top"),
)


def base_markers():
    return {
        "bottom": (F(0), F(0)),
        "aligned": (F(2, 3), F(1, 2)),
        "unaligned": (F(3, 5), F(2, 5)),
        "top": (F(1), F(1)),
    }


def base_levels():
    initial = [
        {
            "name": f"c_{i}_{j}",
            "parent": None,
            "bounds": [F(i, 3), F(i + 1, 3), F(j, 2), F(j + 1, 2)],
        }
        for i in range(3)
        for j in range(2)
    ]
    stages = [initial]
    for parent_name, axis, split, suffixes in (
        ("c_1_0", 0, F(1, 2), ("l", "r")),
        ("c_1_0_l", 2, F(1, 4), ("b", "t")),
    ):
        next_stage = []
        for cell in stages[-1]:
            if cell["name"] != parent_name:
                next_stage.append(
                    {"name": cell["name"], "parent": cell["name"], "bounds": list(cell["bounds"])}
                )
                continue
            for side, suffix in enumerate(suffixes):
                bounds = list(cell["bounds"])
                bounds[axis + (1 if side == 0 else 0)] = split
                child = parent_name + ("_" if parent_name == "c_1_0" else "") + suffix
                next_stage.append({"name": child, "parent": parent_name, "bounds": bounds})
        stages.append(sorted(next_stage, key=lambda c: c["name"]))
    return stages


def transform(name, u, v):
    check(name in FAMILIES, "fixed supplied source family")
    if name in ("warp", "warp_stale"):
        return u * u, v * v
    if name == "boost":
        return 2 * u, v / 2
    if name == "dilate":
        return 2 * u, 2 * v
    return u, v


def image_rectangle(name, bounds):
    lower = transform(name, bounds[0], bounds[2])
    upper = transform(name, bounds[1], bounds[3])
    return [lower[0], upper[0], lower[1], upper[1]]


def certificate_problem(name):
    markers = base_markers()
    probes = []
    for label, a, b in PROBE_LABELS:
        au, av = transform(name, *markers[a])
        bu, bv = transform(name, *markers[b])
        probes.append({"name": label, "bounds": vector([au, bu, av, bv])})
    levels = []
    for label, cells in zip(LEVELS, base_levels(), strict=True):
        transformed = []
        for cell in cells:
            rect = cell["bounds"]
            point = ((rect[0] + rect[1]) / 2, (rect[2] + rect[3]) / 2)
            bounds = image_rectangle(name, rect)
            mark = rect_area(rect if name == "warp_stale" else bounds)
            transformed.append(
                {
                    "name": cell["name"],
                    "parent": cell["parent"],
                    "bounds": vector(bounds),
                    "representative": vector(transform(name, *point)),
                    "volume": wire(mark),
                }
            )
        levels.append({"name": label, "cells": transformed})
    return {
        "schema_version": "det8-qr05ah-problem-v1",
        "family": "qr05ah_partition_bounds",
        "domain": vector(image_rectangle(name, [F(0), F(1), F(0), F(1)])),
        "probes": probes,
        "levels": levels,
    }


def label_ids(level):
    points = base_markers()
    for cell in base_levels()[level]:
        rect = cell["bounds"]
        points[cell["name"]] = ((rect[0] + rect[1]) / 2, (rect[2] + rect[3]) / 2)
    ordered = sorted(
        points, key=lambda name: (points[name][0] + points[name][1], *points[name], name)
    )
    return {label: i for i, label in enumerate(ordered)}


def supplied_source(name, level):
    ids = label_ids(level)
    coords = [None] * len(ids)
    for label, point in base_markers().items():
        coords[ids[label]] = transform(name, *point)
    cells = []
    for cell in base_levels()[level]:
        rect, label = cell["bounds"], cell["name"]
        point = ((rect[0] + rect[1]) / 2, (rect[2] + rect[3]) / 2)
        coords[ids[label]] = transform(name, *point)
        bounds = image_rectangle(name, rect)
        geometric = rect_area(bounds)
        supplied = rect_area(rect) if name == "warp_stale" else geometric
        cells.append(
            {
                "event": ids[label],
                "bounds": vector(bounds),
                "geometric_mark": wire(geometric),
                "supplied_mark": wire(supplied),
            }
        )
    cells.sort(key=lambda c: c["event"])
    past = [
        [i for i in range(j) if coords[i][0] < u and coords[i][1] < v]
        for j, (u, v) in enumerate(coords)
    ]
    return {
        "name": name,
        "coordinates": [vector(row) for row in coords],
        "past": past,
        "fixed": sorted(ids[label] for label in base_markers()),
        "eligible": [c["event"] for c in cells],
        "probes": [
            {"name": label, "source": ids[a], "target": ids[b]} for label, a, b in PROBE_LABELS
        ],
        "cells": cells,
        "mark_kind": "stale_base" if name == "warp_stale" else "geometric_cell_volume",
    }


def selection_law(name, m):
    check(
        1 <= m <= 8 and name in ("identity", "iid_half", "singleton"),
        "prescribed level-specific selection law",
    )
    masses = [F(0)] * (1 << m)
    if name == "identity":
        masses[-1] = F(1)
    elif name == "iid_half":
        masses = [F(1, 1 << m)] * (1 << m)
    else:
        for i in range(m):
            masses[1 << i] = F(1, m)
    eq(sum(masses, F(0)), F(1), "normalized original level selection law")
    return {"name": name, "mask_probabilities": vector(masses)}


def expected_case(name, level, design_name):
    source = supplied_source(name, level)
    design = selection_law(design_name, len(source["eligible"]))
    pop = population(source)
    samples = []
    for mask in range(len(design["mask_probabilities"])):
        problem = raw_packet(source, design, mask)
        samples.append({"problem": problem, "analysis": expected_packet(problem)})
    moments = design_moments(pop, samples)
    covariance, pairs, zero = cell_covariance(source, pop, design)
    native_eq(
        covariance,
        moments["inclusion"]["covariance"],
        "full refined inclusion covariance equals observed law",
    )
    return {
        "case_id": name + "__" + LEVELS[level] + "__" + design_name,
        "level": LEVELS[level],
        "source": source,
        "design": design,
        "population": pop,
        "samples": samples,
        "moments": moments,
        "joint_covariance": covariance,
        "counts": {
            "events": len(source["past"]),
            "eligible_events": len(source["eligible"]),
            "mask_rows": len(samples),
            "positive_rows": sum(s["analysis"]["possible"] for s in samples),
            "questions": len(pop),
            "source_member_terms": sum(len(q["members"]) for q in pop),
            "observed_member_terms": sum(
                s["analysis"]["counts"]["observed_member_terms"] for s in samples
            ),
            "ordered_cell_pairs": pairs,
            "zero_joint_pairs": zero,
            "packet_calls": 2 * len(samples),
        },
    }


def specifications():
    return [
        (name, level, design)
        for name in FAMILIES
        for level in range(3)
        for design in (
            ("identity", "iid_half", "singleton") if name in ("grid", "warp") else ("identity",)
        )
    ]


def counter_problem():
    def cell(name, parent, bounds, point, mark):
        return {
            "name": name,
            "parent": parent,
            "bounds": vector(bounds),
            "representative": vector(point),
            "volume": wire(mark),
        }

    return {
        "schema_version": "det8-qr05ah-problem-v1",
        "family": "qr05ah_partition_bounds",
        "domain": vector([0, 1, 0, 1]),
        "probes": [{"name": "q", "bounds": vector([0, F(1, 5), 0, 1])}],
        "levels": [
            {"name": "a", "cells": [cell("c", None, [0, 1, 0, 1], [F(3, 4), F(1, 2)], F(1, 2))]},
            {
                "name": "b",
                "cells": [
                    cell("c_l", "c", [0, F(1, 2), 0, 1], [F(1, 10), F(1, 2)], F(1, 4)),
                    cell("c_r", "c", [F(1, 2), 1, 0, 1], [F(3, 4), F(1, 2)], F(1, 4)),
                ],
            },
        ],
    }


def geometric_projection(analysis):
    result = {
        k: v for k, v in analysis.items() if k not in ("input_sha256", "levels", "refinements")
    }
    result["levels"] = [
        {
            "name": level["name"],
            "cells": [
                {"name": c["name"], "geometric_volume": c["geometric_volume"]}
                for c in level["cells"]
            ],
            "questions": [
                {
                    k: v
                    for k, v in q.items()
                    if k not in ("supplied_target", "annotation_error", "total_error")
                }
                for q in level["questions"]
            ],
        }
        for level in analysis["levels"]
    ]
    result["refinements"] = [
        {
            "coarse": row["coarse"],
            "fine": row["fine"],
            "questions": row["questions"],
            "parents": [
                {k: v for k, v in parent.items() if k != "supplied_volume"}
                for parent in row["parents"]
            ],
        }
        for row in analysis["refinements"]
    ]
    return result


def scaled_certificate(analysis, factor, input_hash):
    result = json.loads(canon(analysis))
    result["input_sha256"] = input_hash
    result["domain_volume"] = wire(fraction(result["domain_volume"]) * factor)
    for level in result["levels"]:
        for cell in level["cells"]:
            for key in ("geometric_volume", "annotation_error"):
                cell[key] = wire(fraction(cell[key]) * factor)
        for question in level["questions"]:
            for key in question:
                if key not in ("probe", "inner_cells", "outer_cells", "representative_cells"):
                    question[key] = wire(fraction(question[key]) * factor)
    for row in result["refinements"]:
        for parent in row["parents"]:
            for key in ("geometric_volume", "supplied_volume"):
                parent[key] = wire(fraction(parent[key]) * factor)
        for question in row["questions"]:
            for key in question:
                if key != "probe":
                    question[key] = wire(fraction(question[key]) * factor)
    return result


def certificate_observation_bridge(case, certificate):
    level = LEVELS.index(case["level"])
    ids = label_ids(level)
    certified = certificate["levels"][level]
    for pop, question in zip(case["population"], certified["questions"], strict=True):
        native_eq(
            pop["members"],
            sorted(ids[name] for name in question["representative_cells"]),
            "certificate names / observation IDs membership bridge",
        )
        for key in (
            "supplied_target",
            "geometric_target",
            "continuum_volume",
            "annotation_error",
            "quadrature_error",
        ):
            native_eq(
                pop[key], question[key], "complete source-observation geometric bridge: " + key
            )
        COUNTS["certificate_observation_probe_bridges"] += 1
    by_id = {c["event"]: c for c in case["source"]["cells"]}
    for cell in certified["cells"]:
        source = by_id[ids[cell["name"]]]
        native_eq(
            source["geometric_mark"],
            cell["geometric_volume"],
            "every certificate/source true cell volume",
        )
        native_eq(
            wire(fraction(source["supplied_mark"]) - fraction(source["geometric_mark"])),
            cell["annotation_error"],
            "every certificate/source cell annotation",
        )


def expected_controls(certificates, cases, counter):
    cert = {c["source"]: c["analysis"] for c in certificates}
    by_id = {case["case_id"]: case for case in cases}
    answer = {"enclosures": [], "refinement": [], "stale_marks": []}
    for name in FAMILIES:
        questions = [q for level in cert[name]["levels"] for q in level["questions"]]
        changes = [q for row in cert[name]["refinements"] for q in row["questions"]]
        annotation_separate = all(
            fraction(q["annotation_error"])
            == fraction(q["supplied_target"]) - fraction(q["geometric_target"])
            and fraction(q["quadrature_error"])
            == fraction(q["geometric_target"]) - fraction(q["continuum_volume"])
            and fraction(q["total_error"])
            == fraction(q["supplied_target"]) - fraction(q["continuum_volume"])
            and fraction(q["total_error"])
            == fraction(q["annotation_error"]) + fraction(q["quadrature_error"])
            for q in questions
        )
        answer["enclosures"].append(
            {
                "source": name,
                "sandwiches_hold": all(
                    fraction(q["lower_bound"]) <= fraction(q[k]) <= fraction(q["upper_bound"])
                    for q in questions
                    for k in ("geometric_target", "continuum_volume")
                ),
                "annotation_separate": annotation_separate,
                "aligned_exact": all(
                    len(
                        {
                            fraction(q[k])
                            for k in (
                                "lower_bound",
                                "upper_bound",
                                "geometric_target",
                                "continuum_volume",
                            )
                        }
                    )
                    == 1
                    for level in cert[name]["levels"]
                    for q in level["questions"][:3]
                ),
            }
        )
        answer["refinement"].append(
            {
                "source": name,
                "lower_nondecreasing": all(fraction(q["lower_gain"]) >= 0 for q in changes),
                "upper_nonincreasing": all(fraction(q["upper_drop"]) >= 0 for q in changes),
                "gap_nonincreasing": all(fraction(q["gap_drop"]) >= 0 for q in changes),
                "all_absolute_errors_nonincreasing": all(
                    fraction(q["absolute_error_change"]) <= 0 for q in changes
                ),
                "absolute_error_changes": [q["absolute_error_change"] for q in changes],
            }
        )
    for level in LEVELS:
        stale, base = (
            by_id["warp_stale__" + level + "__identity"],
            by_id["grid__" + level + "__identity"],
        )
        answer["stale_marks"].append(
            {
                "level": level,
                "geometric_certificate_equal_warp": same(
                    geometric_projection(cert["warp_stale"]), geometric_projection(cert["warp"])
                ),
                "public_samples_equal_base": same(stale["samples"], base["samples"]),
                "annotation_errors": field_vector(stale, "annotation_error"),
            }
        )
    for name, key, factor in (("boost", "boost", F(1)), ("dilate", "dilation", F(4))):
        answer[key] = {
            "volume_factor": wire(factor),
            "complete_certificate_scaling": same(
                scaled_certificate(cert["grid"], factor, cert[name]["input_sha256"]), cert[name]
            ),
            "complete_observer_scaling": all(
                packet_scaling(
                    by_id["grid__" + level + "__identity"],
                    by_id[name + "__" + level + "__identity"],
                    factor,
                )
                for level in LEVELS
            ),
            "complete_moment_scaling": all(
                same(
                    scaled_moments(by_id["grid__" + level + "__identity"]["moments"], factor),
                    by_id[name + "__" + level + "__identity"]["moments"],
                )
                for level in LEVELS
            ),
        }
    change = counter["analysis"]["refinements"][0]["questions"][0]
    answer["counterexample"] = {
        **counter,
        "bounds_tightened": fraction(change["gap_drop"]) > 0,
        "absolute_error_increased": fraction(change["absolute_error_change"]) > 0,
    }
    return answer


def consumed_ag_bridges(cases, ag):
    previous = {case["case_id"]: case for case in ag["suite"]["cases"]}
    ids = []
    for case in cases:
        if case["level"] != "l0":
            continue
        key = case["source"]["name"] + "__" + case["design"]["name"]
        expected = {k: v for k, v in case.items() if k != "level"}
        expected["case_id"] = key
        native_eq(expected, previous[key], "complete consumed AG level-zero case bridge")
        ids.append(key)
        COUNTS["complete_AG_case_bridges"] += 1
    eq(len(ids), 9, "nine complete AG bridges only")
    return {
        "AG_level0_case_ids": ids,
        "AG_level0_complete_cases_equal": True,
        "AG_other_math_replayed": False,
    }


def expected_suite(ag):
    certificates = []
    for name in FAMILIES:
        problem = certificate_problem(name)
        certificates.append(
            {"source": name, "problem": problem, "analysis": expected_certificate(problem)}
        )
    cases = [expected_case(name, level, design) for name, level, design in specifications()]
    for case in cases:
        certificate_observation_bridge(
            case, certificates[FAMILIES.index(case["source"]["name"])]["analysis"]
        )
    counter_input = counter_problem()
    counter = {"problem": counter_input, "analysis": expected_certificate(counter_input)}
    totals = {"cases": len(cases)}
    totals.update({key: sum(c["counts"][key] for c in cases) for key in cases[0]["counts"]})
    return {
        "certificates": certificates,
        "cases": cases,
        "controls": expected_controls(certificates, cases, counter),
        "prior_bridges": consumed_ag_bridges(cases, ag),
        "public_controls": {
            "certificate_calls": 12,
            "observer_calls": totals["packet_calls"],
            "independent_certificate_routes_equal": True,
            "independent_observer_routes_equal": True,
            "invalid_certificate_calls_rejected": 16,
        },
        "totals": totals,
        "scope": dict.fromkeys(SUITE_SCOPE, False),
    }


def plain_bytes(path):
    check(path.is_file() and not path.is_symlink(), "plain evidence/source file: " + str(path))
    return path.read_bytes()


def raw_identity(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def identity_record(value):
    fields(value, "bytes sha256", "identity record")
    check(type(value["bytes"]) is int and value["bytes"] > 0, "identity positive native size")
    check(
        type(value["sha256"]) is str and re.fullmatch("[a-f0-9]{64}", value["sha256"]),
        "identity SHA256 spelling",
    )


def pinned_json(path, identity):
    raw = plain_bytes(path)
    native_eq(raw_identity(raw), identity, "pinned artifact identity: " + str(path))
    # Pinned prior packaging remains immutable, not a new serialization promise.
    # Full byte identity authenticates it; the current AH envelope is separately
    # required to use AH's compact canonical byte encoding.
    return json.loads(raw)


def runtime_metadata(runtime):
    fields(
        runtime,
        "bytecode_cache executable isolated optimized platform python rss_high_water_at_suite_end rss_units scope suite_seconds",
        "runtime metadata",
    )
    native_eq(runtime["isolated"], True, "recorded isolated capture")
    check(
        type(runtime["optimized"]) is int and runtime["optimized"] in (0, 1),
        "recorded optimization metadata",
    )
    native_eq(runtime["executable"], str(ROOT / ".venv/bin/python"), "recorded executable")
    check(
        type(runtime["rss_units"]) is str and runtime["rss_units"] in ("bytes", "KiB"),
        "recorded RSS units",
    )
    native_eq(
        runtime["scope"],
        "suite and internal exact JSON checks; excludes final report serialization; no application performance claim",
        "recorded runtime scope",
    )
    for key in ("bytecode_cache", "platform", "python"):
        check(type(runtime[key]) is str and bool(runtime[key]), "recorded runtime text " + key)
    cache = Path(runtime["bytecode_cache"])
    check(
        cache.is_absolute()
        and cache != Path(cache.anchor)
        and not cache.resolve().is_relative_to(ROOT),
        "recorded external bytecode cache",
    )
    check(
        type(runtime["rss_high_water_at_suite_end"]) is int
        and runtime["rss_high_water_at_suite_end"] >= 0,
        "recorded RSS metadata",
    )
    seconds = runtime["suite_seconds"]
    check(
        type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0,
        "recorded duration outside mathematical suite",
    )


AH_SOURCES = (
    "README.md",
    "certificate.py",
    "reference_qr05ah.py",
    "study.py",
    "test_qr05ah.py",
    "test_capture.py",
    "audit_json.py",
)
AG_SOURCES = (
    "README.md",
    "volume.py",
    "reference_qr05ag.py",
    "study.py",
    "test_qr05ag.py",
    "test_capture.py",
    "audit_json.py",
)


def identity_inventory(doc):
    ag = pinned_json(AGDIR / "results.json", AG_ID)
    fields(
        ag, "schema_version runtime source_ledger prior_artifacts suite", "AG checkpoint envelope"
    )
    native_eq(ag["schema_version"], "det8-qr05ag-results-v1", "AG checkpoint schema")
    check(
        type(ag["prior_artifacts"]) is dict and len(ag["prior_artifacts"]) == 37,
        "AG authenticated 37-prior inventory",
    )
    previous = {**ag["prior_artifacts"], AG_PRIOR: AG_ID}
    native_eq(doc["prior_artifacts"], previous, "all 38 prior capture identities")
    native_eq(sorted(doc["source_ledger"]), sorted(AH_SOURCES), "seven exact AH source filenames")
    native_eq(
        sorted(ag["source_ledger"]), sorted(AG_SOURCES), "seven exact pinned AG source filenames"
    )
    targets = {HERE / name: doc["source_ledger"][name] for name in AH_SOURCES}
    for name, record in previous.items():
        path = Path(name)
        check(
            not path.is_absolute()
            and len(path.parts) == 2
            and path.parts[0].startswith("qr-")
            and path.parts[1] in ("results.json", "results-v2.json"),
            "bounded prior path",
        )
        targets[HERE.parent / name] = record
    targets.update({AGDIR / name: ag["source_ledger"][name] for name in AG_SOURCES})
    eq(len(targets), 52, "52 distinct AH/prior/AG source identity targets")
    for path, record in targets.items():
        identity_record(record)
        native_eq(
            raw_identity(plain_bytes(path)), record, "initial source/prior identity: " + str(path)
        )
    return targets, ag


def audit_capture(path=None):
    """Read-only complete AH reconstruction and nine declared complete AG bridges."""
    COUNTS.clear()
    started = time.perf_counter()
    path = HERE / "results.json" if path is None else Path(path)
    raw = plain_bytes(path)
    check(len(raw) <= 64 * 1024 * 1024, "AH capture 64 MiB cap")
    before = raw_identity(raw)
    doc = json.loads(raw)
    fields(doc, "schema_version runtime source_ledger prior_artifacts suite", "AH envelope")
    native_eq(doc["schema_version"], "det8-qr05ah-results-v1", "AH capture schema")
    check(canon(doc) == raw, "complete canonical AH envelope bytes")
    for key in ("suite", "source_ledger", "prior_artifacts"):
        native_tree(doc[key])
    check(len(canon(doc["suite"])) <= 128 * 1024 * 1024, "working suite cap")
    runtime_metadata(doc["runtime"])
    targets, ag = identity_inventory(doc)
    expected = expected_suite(ag)
    native_tree(expected)
    native_eq(expected, doc["suite"], "complete independent raw AH suite wire")
    for source_path, record in targets.items():
        native_eq(
            raw_identity(plain_bytes(source_path)),
            record,
            "final source/prior identity: " + str(source_path),
        )
    native_eq(raw_identity(plain_bytes(path)), before, "artifact unchanged during raw audit")
    return {
        "status": "VERIFIED_JSON_ONLY_RAW_AH",
        "artifact": {**before, "path": str(path)},
        "suite": raw_identity(canon(expected)),
        "seconds": time.perf_counter() - started,
        "counts": dict(sorted(COUNTS.items())),
        "totals": expected["totals"],
        "identity_targets": {"total": 52, "AH_sources": 7, "prior_captures": 38, "AG_sources": 7},
        "all_identities_unchanged": True,
        "scope": {
            "complete_generic_partition_and_parent_tile_proofs_reconstructed": True,
            "five_fixed_certificate_families_and_countercontrol_reconstructed": True,
            "full_refined_sources_marks_orders_packets_reconstructed": True,
            "cell_overlap_indicator_integrals_independently_reconstructed": True,
            "centered_and_second_moment_covariances_independently_equal": True,
            "full_cell_inclusion_covariance_independently_projected_to_probes": True,
            "three_signed_errors_and_all_controls_reconstructed": True,
            "nine_complete_AG_level_zero_cases_consumed": True,
            "source_code_read_only_as_identity_bytes": True,
            "other_prior_math_replayed": False,
            "historical_public_API_call_counts_are_metadata_only": True,
            "runtime_metadata_is_not_a_mathematical_benchmark": True,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    check(sys.flags.isolated and sys.pycache_prefix, "run with -I and an external bytecode cache")
    cache = Path(sys.pycache_prefix).resolve()
    check(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT),
        "external bytecode cache boundary",
    )
    print(json.dumps(audit_capture(args.artifact), sort_keys=True))


if __name__ == "__main__":
    main()
