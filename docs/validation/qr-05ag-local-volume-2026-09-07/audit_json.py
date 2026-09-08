"""Independent stdlib JSON-only QR-05AG marked-volume audit.

No engine, runner or test imports. Own AF-lineage helpers are statically
carried; all new geometric recipes and marked-observation laws are rebuilt.
Sources are read only as bytes for identity authentication.
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
AFDIR = ROOT / "docs/validation/qr-05af-local-geometry-2026-09-07"
AF_PRIOR = "qr-05af-local-geometry-2026-09-07/results.json"
AF_ID = {
    "bytes": 11744906,
    "sha256": "8a823b6253d4862bcea8f774f7d46278b288186a0361f38b39cdefd18974d7a3",
}
METHODS = ("raw", "uniform_rate", "inclusion")
PACKET_SCOPE = (
    "missing_marks_inferred",
    "source_moments_inferred",
    "geometry_inferred",
    "mark_origin_authenticated",
    "observation_origin_authenticated",
)
SUITE_SCOPE = (
    "unknown_geometry_reconstructed",
    "annotations_proved_necessary_or_minimal",
    "continuum_limit_established",
    "poisson_ensemble_validated",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
    "unknown_sampling_law_inferred",
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


DESIGNS = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2", "singleton")
SOURCE_NAMES = ("grid", "warp", "warp_stale", "boost", "dilate")


def supplied_source(name):
    """Transform original representatives, boundaries and markers, never recenter."""
    check(name in SOURCE_NAMES, "prescribed source name")
    points = [
        ("bottom", F(0), F(0)),
        ("aligned", F(2, 3), F(1, 2)),
        ("unaligned", F(3, 5), F(2, 5)),
        ("top", F(1), F(1)),
    ]
    bounds = {}
    for i in range(3):
        for j in range(2):
            label = f"c_{i}_{j}"
            points.append((label, F(2 * i + 1, 6), F(2 * j + 1, 4)))
            bounds[label] = (F(i, 3), F(i + 1, 3), F(j, 2), F(j + 1, 2))
    points.sort(key=lambda row: (row[1] + row[2], row[1], row[2], row[0]))
    ids = {label: i for i, (label, _, _) in enumerate(points)}

    def u_image(u):
        return (
            u * u
            if name in ("warp", "warp_stale")
            else u * (2 if name in ("boost", "dilate") else 1)
        )

    def v_image(v):
        if name in ("warp", "warp_stale"):
            return v * v
        return v / 2 if name == "boost" else v * (2 if name == "dilate" else 1)

    coords = [(u_image(u), v_image(v)) for _, u, v in points]
    past = [
        [i for i in range(j) if coords[i][0] < u and coords[i][1] < v]
        for j, (u, v) in enumerate(coords)
    ]
    for j, row in enumerate(past):
        for i in row:
            check(
                i < j and set(past[i]) <= set(row),
                "generated product order is transitive/topological",
            )
    cells = []
    for event, (label, _, _) in enumerate(points):
        if label not in bounds:
            continue
        low_u, high_u, low_v, high_v = bounds[label]
        image = [u_image(low_u), u_image(high_u), v_image(low_v), v_image(high_v)]
        mark = (image[1] - image[0]) * (image[3] - image[2]) / 2
        supplied = (high_u - low_u) * (high_v - low_v) / 2 if name == "warp_stale" else mark
        check(mark > 0 and supplied > 0, "positive supplied/geometric marks")
        check(
            image[0] < coords[event][0] < image[1] and image[2] < coords[event][1] < image[3],
            "transformed ORIGINAL representative remains in its cell",
        )
        cells.append(
            {
                "event": event,
                "bounds": vector(image),
                "geometric_mark": wire(mark),
                "supplied_mark": wire(supplied),
            }
        )
    probes = [
        {"name": label, "source": ids[a], "target": ids[b]}
        for label, a, b in (
            ("whole", "bottom", "top"),
            ("lower_aligned", "bottom", "aligned"),
            ("upper_aligned", "aligned", "top"),
            ("lower_unaligned", "bottom", "unaligned"),
            ("upper_unaligned", "unaligned", "top"),
        )
    ]
    total_area = sum((fraction(c["geometric_mark"]) for c in cells), F(0))
    eq(
        total_area,
        (u_image(F(1)) - u_image(F(0))) * (v_image(F(1)) - v_image(F(0))) / 2,
        "entire cell partition area",
    )
    return {
        "name": name,
        "coordinates": [vector(row) for row in coords],
        "past": past,
        "fixed": sorted(ids[label] for label in ("bottom", "aligned", "unaligned", "top")),
        "eligible": [c["event"] for c in cells],
        "probes": probes,
        "cells": cells,
        "mark_kind": "stale_base" if name == "warp_stale" else "geometric_cell_volume",
    }


def selection_law(name, m):
    check(m == 6 and name in DESIGNS, "prescribed six-cell design")
    masses = [F(0)] * (1 << m)
    if name == "identity":
        masses[-1] = F(1)
    elif name == "all_or_none":
        masses[0] = masses[-1] = F(1, 2)
    elif name in ("singleton", "fixed_size2"):
        k = 1 if name == "singleton" else 2
        for subset in itertools.combinations(range(m), k):
            masses[sum(1 << i for i in subset)] = F(1, math.comb(m, k))
    else:
        rates = [F(1, 2) if name == "iid_half" else F(1 + i % 2, 3) for i in range(m)]
        for mask in range(1 << m):
            masses[mask] = math.prod(p if mask & (1 << i) else 1 - p for i, p in enumerate(rates))
    eq(sum(masses, F(0)), F(1), "original design normalization")
    return {"name": name, "mask_probabilities": vector(masses)}


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


def overlap_length(left, right, a, b):
    """Integrate indicator products on endpoint-defined open segments."""
    cuts = sorted({left, right, a, b})
    value = F(0)
    for lo, hi in itertools.pairwise(cuts):
        middle = (lo + hi) / 2
        if left < middle < right and a < middle < b:
            value += hi - lo
        COUNTS["overlap_indicator_segments"] += 1
    return value


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


def specifications():
    return [(name, design) for name in ("grid", "warp") for design in DESIGNS] + [
        (name, design)
        for name in ("warp_stale", "boost", "dilate")
        for design in ("identity", "iid_half")
    ]


def expected_case(name, design_name):
    source = supplied_source(name)
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
        "full projected inclusion covariance equals observed centered law",
    )
    return {
        "case_id": name + "__" + design_name,
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


def expected_controls(cases):
    by_name = {case["case_id"]: case for case in cases}
    controls = {
        name: [] for name in ("warp", "stale_marks", "boost", "dilation", "boundaries", "sampling")
    }
    for design in DESIGNS:
        base, warp = by_name["grid__" + design], by_name["warp__" + design]
        controls["warp"].append(
            {
                "design": design,
                "unmarked_packets_equal": same(
                    unmarked_projection(base), unmarked_projection(warp)
                ),
                "marked_positive_laws_equal": same(positive_law(base), positive_law(warp)),
                "base_targets": field_vector(base, "supplied_target"),
                "warped_targets": field_vector(warp, "supplied_target"),
                "base_volumes": field_vector(base, "continuum_volume"),
                "warped_volumes": field_vector(warp, "continuum_volume"),
            }
        )
    for design in ("identity", "iid_half"):
        base, warp, stale = (
            by_name[name + "__" + design] for name in ("grid", "warp", "warp_stale")
        )
        controls["stale_marks"].append(
            {
                "design": design,
                "packets_equal_base": same(base["samples"], stale["samples"]),
                "geometric_targets_equal_warp": same(
                    field_vector(warp, "geometric_target"), field_vector(stale, "geometric_target")
                ),
                "supplied_targets": field_vector(stale, "supplied_target"),
                "geometric_targets": field_vector(stale, "geometric_target"),
                "annotation_errors": field_vector(stale, "annotation_error"),
            }
        )
        for source, key, factor in (("boost", "boost", F(1)), ("dilate", "dilation", F(4))):
            other = by_name[source + "__" + design]
            controls[key].append(
                {
                    "design": design,
                    "order_equal": same(base["source"]["past"], other["source"]["past"]),
                    "packet_estimate_scaling": packet_scaling(base, other, factor),
                    "moment_scaling": same(
                        scaled_moments(base["moments"], factor), other["moments"]
                    ),
                    "population_scaling": same(
                        scaled_population(base["population"], factor), other["population"]
                    ),
                    "volume_factor": wire(factor),
                }
            )
    for name in SOURCE_NAMES:
        case = by_name[name + "__identity"]
        controls["boundaries"].append(
            {
                "source": name,
                "overlaps_sum_to_volume": all(
                    sum((fraction(c["volume"]) for c in row["overlaps"]), F(0))
                    == fraction(row["continuum_volume"])
                    for row in case["population"]
                ),
                "aligned_geometric_exact": all(
                    fraction(row["geometric_target"]) == fraction(row["continuum_volume"])
                    for row in case["population"][:3]
                ),
                "unaligned_quadrature_errors": field_vector(case, "quadrature_error")[3:],
            }
        )
    for name in ("grid", "warp"):
        for design in DESIGNS:
            case = by_name[name + "__" + design]
            controls["sampling"].append(
                {
                    "case_id": case["case_id"],
                    "inclusion_unbiased": all(
                        fraction(value) == 0 for value in case["moments"]["inclusion"]["bias"]
                    ),
                    "uniform_bias": case["moments"]["uniform_rate"]["bias"],
                    "raw_bias": case["moments"]["raw"]["bias"],
                    "covariance_formula_equal": same(
                        case["joint_covariance"], case["moments"]["inclusion"]["covariance"]
                    ),
                }
            )
    return controls


def expected_suite():
    cases = [expected_case(name, design) for name, design in specifications()]
    totals = {"cases": len(cases)}
    totals.update({key: sum(case["counts"][key] for case in cases) for key in cases[0]["counts"]})
    return {
        "cases": cases,
        "controls": expected_controls(cases),
        "public_controls": {
            "ordinary_packet_calls": totals["packet_calls"],
            "independent_route_equal": True,
            "invalid_calls_rejected": 16,
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
    # Full byte identity authenticates it; the current AG envelope is separately
    # required to use AG's compact canonical byte encoding.
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


AG_SOURCES = (
    "README.md",
    "volume.py",
    "reference_qr05ag.py",
    "study.py",
    "test_qr05ag.py",
    "test_capture.py",
    "audit_json.py",
)
AF_SOURCES = (
    "README.md",
    "geometry.py",
    "reference_qr05af.py",
    "study.py",
    "test_qr05af.py",
    "test_capture.py",
    "audit_json.py",
)


def identity_inventory(doc):
    af = pinned_json(AFDIR / "results.json", AF_ID)
    fields(
        af, "schema_version runtime source_ledger prior_artifacts suite", "AF checkpoint envelope"
    )
    native_eq(af["schema_version"], "det8-qr05af-results-v1", "AF checkpoint schema")
    check(
        type(af["prior_artifacts"]) is dict and len(af["prior_artifacts"]) == 36,
        "AF authenticated 36-prior inventory",
    )
    prior_expected = {**af["prior_artifacts"], AF_PRIOR: AF_ID}
    native_eq(
        doc["prior_artifacts"],
        prior_expected,
        "all 37 current prior identities match pinned lineage",
    )
    native_eq(sorted(doc["source_ledger"]), sorted(AG_SOURCES), "seven exact AG source filenames")
    native_eq(
        sorted(af["source_ledger"]), sorted(AF_SOURCES), "seven exact pinned AF source filenames"
    )
    targets = {HERE / name: doc["source_ledger"][name] for name in AG_SOURCES}
    for name, record in prior_expected.items():
        path = Path(name)
        check(
            not path.is_absolute()
            and len(path.parts) == 2
            and path.parts[0].startswith("qr-")
            and path.parts[1] in ("results.json", "results-v2.json"),
            "bounded prior path",
        )
        targets[HERE.parent / name] = record
    targets.update({AFDIR / name: af["source_ledger"][name] for name in AF_SOURCES})
    eq(len(targets), 51, "51 distinct AG/prior/AF source identity targets")
    for path, record in targets.items():
        identity_record(record)
        native_eq(
            raw_identity(plain_bytes(path)), record, "initial source/prior identity: " + str(path)
        )
    return targets


def audit_capture(path=None):
    """Complete read-only raw reconstruction; previous gates are identity only."""
    COUNTS.clear()
    started = time.perf_counter()
    path = HERE / "results.json" if path is None else Path(path)
    raw = plain_bytes(path)
    check(len(raw) <= 64 * 1024 * 1024, "AG capture 64 MiB cap")
    before = raw_identity(raw)
    doc = json.loads(raw)
    fields(doc, "schema_version runtime source_ledger prior_artifacts suite", "AG envelope")
    native_eq(doc["schema_version"], "det8-qr05ag-results-v1", "AG capture schema")
    check(canon(doc) == raw, "complete canonical AG envelope bytes")
    for key in ("suite", "source_ledger", "prior_artifacts"):
        native_tree(doc[key])
    check(len(canon(doc["suite"])) <= 128 * 1024 * 1024, "working suite cap")
    runtime_metadata(doc["runtime"])
    targets = identity_inventory(doc)
    expected = expected_suite()
    native_tree(expected)
    native_eq(expected, doc["suite"], "complete independent raw AG suite wire")
    for source_path, record in targets.items():
        native_eq(
            raw_identity(plain_bytes(source_path)),
            record,
            "final source/prior identity: " + str(source_path),
        )
    native_eq(raw_identity(plain_bytes(path)), before, "artifact unchanged during raw audit")
    return {
        "status": "VERIFIED_JSON_ONLY_RAW_AG",
        "artifact": {**before, "path": str(path)},
        "suite": raw_identity(canon(expected)),
        "seconds": time.perf_counter() - started,
        "counts": dict(sorted(COUNTS.items())),
        "totals": expected["totals"],
        "identity_targets": {"total": 51, "AG_sources": 7, "prior_captures": 37, "AF_sources": 7},
        "all_identities_unchanged": True,
        "scope": {
            "full_AG_sources_boundaries_marks_orders_packets_reconstructed": True,
            "cell_overlap_indicator_integrals_independently_reconstructed": True,
            "centered_and_second_moment_covariances_independently_equal": True,
            "full_cell_inclusion_covariance_independently_projected_to_probes": True,
            "three_signed_error_terms_and_all_controls_reconstructed": True,
            "source_code_read_only_as_identity_bytes": True,
            "prior_math_replayed": False,
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
