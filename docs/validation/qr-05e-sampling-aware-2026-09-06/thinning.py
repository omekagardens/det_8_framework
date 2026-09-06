"""Exact finite thinning diagnostics from observed induced orders."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, pairwise
from math import comb, prod

ORDERS = ("ferrers6", "standard_example3", "mesh3_center")
DESIGNS = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2")
CASES = tuple((o, d) for o in ORDERS for d in DESIGNS) + (
    ("ferrers6", "singleton"),
    ("chain6", "singleton"),
)
METHODS = ("raw", "marginal_product", "uniform_rate", "joint_supported")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def wire(value):
    if type(value) is F:
        require(
            max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
            "rational component bound",
        )
        return str(value)
    if type(value) is list:
        return [wire(v) for v in value]
    if type(value) is dict:
        require(all(type(k) is str for k in value), "string wire keys required")
        return {k: wire(v) for k, v in value.items()}
    require(value is None or type(value) in (str, bool, int), "native exact wire types required")
    if type(value) is int:
        require(abs(value).bit_length() <= 4096, "integer component bound")
    return value


def population(name):
    if name == "mesh3_center":
        grid = [(i, j) for i in range(1, 4) for j in range(1, 4)]
        past = [[]]
        for index, (i, j) in enumerate(grid):
            past.append([0, *(k + 1 for k, (a, b) in enumerate(grid[:index]) if a <= i and b <= j)])
        past.append(list(range(10)))
        fixed, density = [0, 5, 10], F(18)
        probes = [
            {"name": "whole", "source": 0, "target": 10},
            {"name": "bottom_to_middle", "source": 0, "target": 5},
            {"name": "middle_to_top", "source": 5, "target": 10},
        ]
    else:
        if name == "chain6":
            past = [list(range(j)) for j in range(8)]
        else:
            past = [[], [0], [0], [0]]
            for j in range(3):
                past.append(
                    [0, *(i + 1 for i in range(3) if (i <= j if name == "ferrers6" else i != j))]
                )
            past.append(list(range(7)))
        fixed, density = [0, 7], F(12)
        probes = [{"name": "whole", "source": 0, "target": 7}]
    eligible = [i for i in range(len(past)) if i not in fixed]
    return past, fixed, eligible, probes, density


def probabilities(design, m):
    result = []
    for mask in range(1 << m):
        size = mask.bit_count()
        if design == "identity":
            p = F(mask == (1 << m) - 1)
        elif design == "iid_half":
            p = F(1, 1 << m)
        elif design == "heterogeneous":
            vertex = [F(1, 3) if i % 2 == 0 else F(2, 3) for i in range(m)]
            p = prod((v if mask & (1 << i) else 1 - v for i, v in enumerate(vertex)), start=F(1))
        elif design == "all_or_none":
            p = F(1, 2) if mask in (0, (1 << m) - 1) else F(0)
        else:
            size_required = 1 if design == "singleton" else 2
            p = F(1, comb(m, size_required)) if size == size_required else F(0)
        result.append(p)
    require(sum(result) == 1, "design not normalized")
    return result


def chains(past, source, target, degree):
    if source not in past[target]:
        return []
    interior = [i for i in past[target] if source in past[i]]
    return [
        list(c)
        for c in combinations(interior, degree)
        if all(a in past[b] for a, b in pairwise((source, *c, target)))
    ]


def support_mask(vertices, positions):
    return sum(1 << positions[v] for v in vertices if v in positions)


def induced(past, kept):
    return [[i for i, a in enumerate(kept) if a in past[b]] for b in kept]


def links(past):
    return [[i for i in row if not any(i in past[k] for k in row)] for row in past]


def hasse_support(link_past, kept, probes):
    reach = {}
    for v in kept:
        direct = set(link_past[v]) & set(kept)
        reach[v] = direct | set().union(*(reach[i] for i in direct))
    return [p["source"] in reach[p["target"]] for p in probes]


def observed_estimates(observed_past, kept, probes, positions, inclusion, pbar):
    """Use only the received order, frame/probes, and known selection design."""
    local = {original: index for index, original in enumerate(kept)}
    counts, omitted = [], []
    estimates = {name: [] for name in METHODS}
    for probe in probes:
        for degree in range(4):
            local_chains = chains(
                observed_past, local[probe["source"]], local[probe["target"]], degree
            )
            masks = [support_mask([kept[i] for i in c], positions) for c in local_chains]
            counts.append(len(masks))
            omitted.append(sum(inclusion[s] == 0 for s in masks))
            estimates["raw"].append(F(len(masks)))
            estimates["marginal_product"].append(
                sum(
                    (
                        1
                        / prod(
                            (inclusion[1 << k] for k in range(len(positions)) if s & (1 << k)),
                            start=F(1),
                        )
                        for s in masks
                    ),
                    start=F(0),
                )
            )
            estimates["uniform_rate"].append(
                sum((1 / pbar ** s.bit_count() for s in masks), start=F(0))
            )
            estimates["joint_supported"].append(
                sum((1 / inclusion[s] for s in masks if inclusion[s] > 0), start=F(0))
            )
    return counts, omitted, estimates


def moments(samples, questions):
    result = {}
    q = len(questions)
    target = [F(row["target_count"]) for row in questions]
    scales = [row["scale"] for row in questions]
    positive = [s for s in samples if s["probability"] > 0]
    for method in METHODS:
        mean = [
            sum((s["probability"] * s["estimates"][method][i] for s in positive), start=F(0))
            for i in range(q)
        ]
        covariance = [[F(0)] * q for _ in range(q)]
        for i in range(q):
            for j in range(i, q):
                second = sum(
                    (
                        s["probability"] * s["estimates"][method][i] * s["estimates"][method][j]
                        for s in positive
                    ),
                    start=F(0),
                )
                covariance[i][j] = covariance[j][i] = second - mean[i] * mean[j]
        result[method] = {
            "mean_counts": mean,
            "bias_counts": [mean[i] - target[i] for i in range(q)],
            "covariance_counts": covariance,
            "mean_coefficients": [mean[i] * scales[i] for i in range(q)],
            "bias_coefficients": [(mean[i] - target[i]) * scales[i] for i in range(q)],
            "covariance_coefficients": [
                [covariance[i][j] * scales[i] * scales[j] for j in range(q)] for i in range(q)
            ],
            "exact_target_probabilities": [
                sum(
                    (s["probability"] for s in positive if s["estimates"][method][i] == target[i]),
                    start=F(0),
                )
                for i in range(q)
            ],
            "vector_exact_target_probability": sum(
                (s["probability"] for s in positive if s["estimates"][method] == target), start=F(0)
            ),
        }
    return result


def covariance_formula(questions, inclusion):
    supports = [
        Counter(c["eligible_mask"] for c in question["chains"] if c["inclusion"] > 0)
        for question in questions
    ]
    return [
        [
            sum(
                (
                    F(a_count * b_count) * (inclusion[a | b] / (inclusion[a] * inclusion[b]) - 1)
                    for a, a_count in left.items()
                    for b, b_count in right.items()
                ),
                start=F(0),
            )
            for right in supports
        ]
        for left in supports
    ]


def analyze(value):
    require(
        type(value) is dict and set(value) == {"schema_version", "order", "design"},
        "exact problem fields required",
    )
    require(
        type(value["schema_version"]) is str and value["schema_version"] == "det8-qr05e-problem-v1",
        "unsupported schema",
    )
    require(
        type(value["order"]) is str
        and type(value["design"]) is str
        and (value["order"], value["design"]) in CASES,
        "unsupported fixed combination",
    )
    order_name, design = value["order"], value["design"]
    past, fixed, eligible, probes, density = population(order_name)
    m, positions = len(eligible), {v: i for i, v in enumerate(eligible)}
    probs = probabilities(design, m)
    inclusion = [
        sum((p for s, p in enumerate(probs) if s & a == a), start=F(0)) for a in range(1 << m)
    ]
    require(
        inclusion[0] == 1 and all(inclusion[1 << i] > 0 for i in range(m)), "inclusion contract"
    )
    pbar = sum((inclusion[1 << i] for i in range(m)), start=F(0)) / m
    questions = []
    for probe in probes:
        for degree in range(4):
            family = chains(past, probe["source"], probe["target"], degree)
            entries = [
                {
                    "vertices": c,
                    "eligible_mask": support_mask(c, positions),
                    "inclusion": inclusion[support_mask(c, positions)],
                }
                for c in family
            ]
            missing = [c["vertices"] for c in entries if c["inclusion"] == 0]
            scale = F((-1) ** degree, 2 ** (degree + 1)) / density**degree
            questions.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": scale,
                    "target_count": len(family),
                    "target_coefficient": scale * len(family),
                    "chains": entries,
                    "zero_inclusion_chains": missing,
                    "supported_count": len(family) - len(missing),
                    "full_target_supported": not missing,
                }
            )
    samples, law, mismatch, first = [], [], F(0), None
    link_past = links(past)
    for mask, probability in enumerate(probs):
        kept = sorted([*fixed, *(v for i, v in enumerate(eligible) if mask & (1 << i))])
        observed = induced(past, kept)
        count, omitted, estimates = observed_estimates(
            observed, kept, probes, positions, inclusion, pbar
        )
        support = hasse_support(link_past, kept, probes)
        samples.append(
            {
                "mask": mask,
                "probability": probability,
                "kept": kept,
                "observed_past": observed,
                "chain_counts": count,
                "unsupported_observed_terms": omitted,
                "estimates": estimates,
                "hasse_only_reachability": support,
            }
        )
        if probability > 0:
            require(not any(omitted), "positive sample contains zero-inclusion chain")
            law.append({"kept": kept, "past": observed, "probability": probability})
            if not all(support):
                mismatch += probability
                if first is None:
                    first = {
                        "mask": mask,
                        "kept": kept,
                        "probes": [
                            p["name"]
                            for p, reached in zip(probes, support, strict=True)
                            if not reached
                        ],
                    }
    statistics = moments(samples, questions)
    formula = covariance_formula(questions, inclusion)
    require(
        formula == statistics["joint_supported"]["covariance_counts"], "joint covariance identity"
    )
    require(
        statistics["joint_supported"]["mean_counts"] == [q["supported_count"] for q in questions],
        "supported expectation identity",
    )
    return wire(
        {
            "order_name": order_name,
            "design": design,
            "density": density,
            "past": past,
            "fixed": fixed,
            "eligible": eligible,
            "probes": probes,
            "inclusion_probabilities": inclusion,
            "questions": questions,
            "samples": samples,
            "moments": statistics,
            "joint_covariance_formula": formula,
            "observation_law": law,
            "hasse_control": {"mismatch_probability": mismatch, "first_mismatch": first},
            "counts": {
                "events": len(past),
                "eligible_events": m,
                "mask_rows": len(samples),
                "positive_rows": len(law),
                "questions": len(questions),
                "chain_terms": sum(len(q["chains"]) for q in questions),
                "estimator_cells": len(samples) * len(questions) * len(METHODS),
            },
        }
    )
