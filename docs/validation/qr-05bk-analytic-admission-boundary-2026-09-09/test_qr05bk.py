"""Source-bound BK tests: independent Boole/Gram/cofactor and Hermite oracle.

No fixture evaluation or engine execution occurs at import. The complete
suite is held until the first source-bound release. Checks survive -O.
Only this gate's study driver is imported; no historical executor is used.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import tempfile
import unittest
from fractions import Fraction
from functools import cmp_to_key, lru_cache
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = "924461cf18794bae1e6b022b92550f544246aad7595b59b8afb535968f7a86f5"


def load_module(name):
    spec = importlib.util.spec_from_file_location("qr05bk_test_" + name, HERE / (name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("BK source could not be loaded")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def exact_keys(test, value, names):
    test.assertIs(type(value), dict)
    test.assertEqual(set(value), set(names.split()))


@lru_cache(maxsize=1)
def boole_rule():
    nodes = tuple(Fraction(i, 4) for i in range(5))
    weights = tuple(Fraction(n, 90) for n in (7, 32, 12, 32, 7))
    for degree in range(6):
        if sum(w * x**degree for x, w in zip(nodes, weights, strict=True)) != Fraction(
            1, degree + 1
        ):
            raise ValueError("Independent quadrature certificate failed")
    return nodes, weights


def integrate(function):
    nodes, weights = boole_rule()
    return sum(
        (
            wu * wv * function(u, v)
            for u, wu in zip(nodes, weights, strict=True)
            for v, wv in zip(nodes, weights, strict=True)
        ),
        Fraction(0),
    )


def basis(u, v):
    return [(1 - u) * (1 - v), u * (1 - v), (1 - u) * v, u * v, u * (1 - u) * v * (1 - v)]


def functional(coefficients):
    return integrate(lambda u, v: dot(coefficients, basis(u, v)) * (1 - u) * (1 - v))


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), Fraction(0))


def multiply(a, b):
    return [[dot(row, list(column)) for column in zip(*b, strict=True)] for row in a]


def identity(n):
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def determinant(matrix):
    """Permutation expansion, independent of either implementation's solver."""
    n = len(matrix)
    result = Fraction(0)
    for permutation in itertools.permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j] for i in range(n) for j in range(i + 1, n))
        term = Fraction((-1) ** inversions)
        for i, j in enumerate(permutation):
            term *= matrix[i][j]
        result += term
    return result


def cofactor_inverse(matrix):
    denominator = determinant(matrix)
    if not denominator:
        raise ValueError("Singular independent test matrix")
    n = len(matrix)
    return [
        [
            Fraction((-1) ** (i + j))
            * determinant(
                [
                    [matrix[row][column] for column in range(n) if column != i]
                    for row in range(n)
                    if row != j
                ]
            )
            / denominator
            for j in range(n)
        ]
        for i in range(n)
    ]


def row_rank(matrix):
    """Exact rational Gram-Schmidt, not an echelon implementation."""
    vectors = []
    for row in matrix:
        residual = list(row)
        for vector in vectors:
            coefficient = dot(residual, vector) / dot(vector, vector)
            residual = [x - coefficient * y for x, y in zip(residual, vector, strict=True)]
        if any(residual):
            vectors.append(residual)
    return len(vectors)


def probability(means, outcomes):
    result = Fraction(1)
    for mean, outcome in zip(means, outcomes, strict=True):
        result *= (1 + mean * outcome) / 2
    return result


def branch_state(outcomes, mass):
    return [
        mass
        if all(outcome == 1 - 2 * bit for outcome, bit in zip(outcomes, bits, strict=True))
        else Fraction(0)
        for bits in itertools.product((0, 1), repeat=len(outcomes))
    ]


def law(means):
    rows = []
    for outcomes in itertools.product((-1, 1), repeat=5):
        mass = probability(means, outcomes)
        rows.append(
            {
                "outcomes": list(outcomes),
                "probability": mass,
                "state_diagonal": branch_state(outcomes, mass),
            }
        )
    return {
        "rows": rows,
        "averaged_state": [
            sum((row["state_diagonal"][i] for row in rows), Fraction(0)) for i in range(32)
        ],
    }


def bernstein(i, x):
    return ((1 - x) ** 2, 2 * x * (1 - x), x * x)[i]


@lru_cache(maxsize=1)
def bernstein_gram():
    nodes, weights = boole_rule()
    matrix = [
        [
            sum(
                (
                    w * bernstein(i, x) * bernstein(j, x)
                    for x, w in zip(nodes, weights, strict=True)
                ),
                Fraction(0),
            )
            for j in range(3)
        ]
        for i in range(3)
    ]
    return matrix, cofactor_inverse(matrix)


def moment_patch(coefficients, declared, local_nodes):
    """Recover C from N=M C M^T using independently integrated moments."""
    bounds = [list(map(Fraction, interval)) for interval in declared["bounds"]]
    (a, b), (c, d) = bounds
    nodes, weights = boole_rule()
    samples = [
        [dot(coefficients, basis(a + (b - a) * s, c + (d - c) * t)) for t in nodes] for s in nodes
    ]
    moments = [
        [
            sum(
                (
                    weights[k] * weights[l] * samples[k][l] * bernstein(i, s) * bernstein(j, t)
                    for k, s in enumerate(nodes)
                    for l, t in enumerate(nodes)
                ),
                Fraction(0),
            )
            for j in range(3)
        ]
        for i in range(3)
    ]
    _gram, inverse = bernstein_gram()
    net = multiply(
        multiply(inverse, moments), [list(column) for column in zip(*inverse, strict=True)]
    )
    residuals = []
    for s in local_nodes:
        row = []
        for t in local_nodes:
            represented = sum(
                (net[i][j] * bernstein(i, s) * bernstein(j, t) for i in range(3) for j in range(3)),
                Fraction(0),
            )
            row.append(dot(coefficients, basis(a + (b - a) * s, c + (d - c) * t)) - represented)
        residuals.append(row)
    low, high = min(min(row) for row in net), max(max(row) for row in net)
    return {
        "id": declared["id"],
        "bounds": bounds,
        "coefficients": net,
        "reconstruction_residual": residuals,
        "range_bound": [low, high],
        "bound_status": "within" if -1 <= low and high <= 1 else "outside",
    }


def merge_union(intervals):
    """Independent connected-component union; includes infinite endpoints."""
    todo = [list(interval) for interval in intervals if interval is not None]
    result = []

    def touches(a, b):
        return not (
            (a[1] is not None and b[0] is not None and a[1] < b[0])
            or (b[1] is not None and a[0] is not None and b[1] < a[0])
        )

    while todo:
        component = [todo.pop()]
        changed = True
        while changed:
            changed = False
            for index in range(len(todo) - 1, -1, -1):
                if any(touches(todo[index], interval) for interval in component):
                    component.append(todo.pop(index))
                    changed = True
        lows, highs = [x[0] for x in component], [x[1] for x in component]
        result.append([None if None in lows else min(lows), None if None in highs else max(highs)])
    return sorted(result, key=lambda x: (x[0] is not None, x[0] or Fraction(0)))


def intersect_union(left, right):
    pieces = []
    for a, b in itertools.product(left, right):
        lows = [x for x in (a[0], b[0]) if x is not None]
        highs = [x for x in (a[1], b[1]) if x is not None]
        lo, hi = max(lows) if lows else None, min(highs) if highs else None
        if lo is None or hi is None or lo <= hi:
            pieces.append([lo, hi])
    return merge_union(pieces)


def project_union(union, offset, slope):
    if not slope:
        return [[offset, offset]] if union else []
    result = []
    for interval in union:
        ends = [None if x is None else offset + slope * x for x in interval]
        result.append(ends if slope > 0 else ends[::-1])
    return merge_union(result)


def arrangement(pairs):
    """Test roots and open cells, never sequentially clip scalar bounds."""
    roots = sorted({(sign - a) / b for a, b in pairs if b for sign in (-1, 1)})

    def feasible(x):
        return all(abs(a + b * x) <= 1 for a, b in pairs)

    if not roots:
        return [None, None] if feasible(Fraction(0)) else None
    pieces = [[x, x] for x in roots if feasible(x)]
    ends = [None, *roots, None]
    for lo, hi in itertools.pairwise(ends):
        sample = hi - 1 if lo is None else lo + 1 if hi is None else (lo + hi) / 2
        if feasible(sample):
            pieces.append([lo, hi])
    merged = merge_union(pieces)
    if len(merged) > 1:
        raise ValueError("Affine conjunction unexpectedly disconnected")
    return merged[0] if merged else None


def summary(union):
    intervals = merge_union(union)
    gaps = [[left[1], right[0]] for left, right in itertools.pairwise(intervals)]
    return {
        "intervals": intervals,
        "hull": [intervals[0][0], intervals[-1][1]] if intervals else None,
        "gaps": gaps,
        "gap_probes": [(a + b) / 2 for a, b in gaps],
    }


def expected_menus(menus, positions):
    by_id = {p["position_id"]: p for p in positions}
    reports = []
    for declared in menus:
        groups = {}
        sets = {}
        for route in ("old", "inner", "outer"):
            groups[route] = [
                {
                    "position_id": name,
                    "theta": by_id[name][route + "_theta"],
                    "targets": by_id[name][route + "_targets"],
                }
                for name in declared["position_ids"]
                if by_id[name][route + "_theta"]
            ]
            sets[route] = summary(
                [interval for entry in groups[route] for interval in entry["targets"]]
            )
        outer, inner = sets["outer"]["intervals"], sets["inner"]["intervals"]
        single = len(outer) == 1 and outer[0][0] == outer[0][1]
        plural = len(inner) > 1 or any(a != b for a, b in inner)
        existence = (
            "infeasible" if not groups["outer"] else "feasible" if groups["inner"] else "unresolved"
        )
        target = (
            "infeasible"
            if not outer
            else "identified"
            if inner and single
            else "ambiguous"
            if plural
            else "unresolved"
        )
        reports.append(
            {
                "id": declared["id"],
                "position_ids": list(declared["position_ids"]),
                **groups,
                "target_sets": sets,
                "existence_status": existence,
                "target_status": target,
                "hypothesis_set_status": "exact"
                if groups["inner"] == groups["outer"]
                else "bounded",
                "target_set_status": "exact" if inner == outer else "bounded",
            }
        )
    return reports


def affine_patch(corners, declared, nodes):
    base = moment_patch([*corners, Fraction(0)], declared, nodes)
    unit = moment_patch([Fraction(0)] * 4 + [Fraction(1)], declared, nodes)
    coefficients = [
        [[base["coefficients"][i][j], unit["coefficients"][i][j]] for j in range(3)]
        for i in range(3)
    ]
    residual = [
        [
            [base["reconstruction_residual"][i][j], unit["reconstruction_residual"][i][j]]
            for j in range(3)
        ]
        for i in range(3)
    ]
    return {
        "id": declared["id"],
        "bounds": base["bounds"],
        "coefficients": coefficients,
        "reconstruction_residual": residual,
        "allowed": [[arrangement([pair]) for pair in row] for row in coefficients],
        "theta_interval": arrangement([pair for row in coefficients for pair in row]),
    }


def affine_law(corners):
    """Derive both affine components from two complete scalar endpoint laws."""
    negative, positive = law([*corners, Fraction(-1)]), law([*corners, Fraction(1)])

    def pair(a, b):
        return [(a + b) / 2, (b - a) / 2]

    rows = [
        {
            "outcomes": list(lo["outcomes"]),
            "probability": pair(lo["probability"], hi["probability"]),
            "state_diagonal": [
                pair(a, b) for a, b in zip(lo["state_diagonal"], hi["state_diagonal"], strict=True)
            ],
        }
        for lo, hi in zip(negative["rows"], positive["rows"], strict=True)
    ]
    return {
        "rows": rows,
        "averaged_state": [
            pair(a, b)
            for a, b in zip(negative["averaged_state"], positive["averaged_state"], strict=True)
        ],
    }


def at(pair, parameter):
    return pair[0] + pair[1] * parameter


def evaluate_law(family, mean):
    return {
        "rows": [
            {
                "outcomes": list(row["outcomes"]),
                "probability": at(row["probability"], mean),
                "state_diagonal": [at(pair, mean) for pair in row["state_diagonal"]],
            }
            for row in family["rows"]
        ],
        "averaged_state": [at(pair, mean) for pair in family["averaged_state"]],
    }


def endpoint_check(family, mean):
    report = evaluate_law(family, mean)
    return {
        "mean": mean,
        "probability_sum": sum((r["probability"] for r in report["rows"]), Fraction(0)),
        "averaged_trace": sum(report["averaged_state"], Fraction(0)),
        "minimum_probability": min(r["probability"] for r in report["rows"]),
        "minimum_state_entry": min(x for r in report["rows"] for x in r["state_diagonal"]),
        "maximum_trace_residual": max(
            abs(sum(r["state_diagonal"], Fraction(0)) - r["probability"]) for r in report["rows"]
        ),
    }


def bi_expected(protocol):
    model = protocol["model"]["model"]
    certificate = protocol["model"]["certificate"]
    nodes = list(map(Fraction, certificate["local_nodes"]))
    q = [functional(row) for row in identity(5)]
    volume = integrate(lambda _u, _v: Fraction(model["geometry"]["measure_factor"]))
    positions = []
    for declared in model["positions"]:
        u, v = map(Fraction, declared["position"])
        a = identity(5)[:4] + [basis(u, v)]
        decoder = cofactor_inverse(a)
        weights = multiply([q], decoder)[0]
        positions.append(
            {
                "id": declared["id"],
                "position": [u, v],
                "basis": basis(u, v),
                "evaluation_matrix": a,
                "coefficient_decoder": decoder,
                "left_inverse": multiply(decoder, a),
                "right_inverse": multiply(a, decoder),
                "full_weights": weights,
                "full_residual": [x - y for x, y in zip(multiply([weights], a)[0], q, strict=True)],
            }
        )
    cases = []
    for declared in model["cases"]:
        *corners, center = map(Fraction, declared["population_means"])
        offset = functional([*corners, Fraction(0)])
        patches = [
            affine_patch(corners, p, nodes) for p in [certificate["root"], *certificate["leaves"]]
        ]
        witnesses = []
        for point in certificate["witness_points"]:
            position = list(map(Fraction, point))
            value = [dot(corners, basis(*position)[:4]), basis(*position)[4]]
            witnesses.append(
                {"position": position, "value": value, "allowed": arrangement([value])}
            )
        gap = 16 * (1 - max(map(abs, corners)))
        old = [-gap, gap] if gap >= 0 else None
        bern = arrangement(
            [pair for patch in patches[1:] for row in patch["coefficients"] for pair in row]
        )
        witness = arrangement([w["value"] for w in witnesses])
        inner, outer = merge_union([old, bern]), merge_union([witness])
        family = affine_law(corners)
        budgets = []
        for budget in protocol["interval_budgets"]:
            radius = Fraction(budget["radius"])
            response = [max(Fraction(-1), center - radius), min(Fraction(1), center + radius)]
            rows = []
            for position in positions:
                r, s = dot(corners, position["basis"][:4]), position["basis"][4]
                theta = [(x - r) / s for x in response]
                residual = []
                for parameter, mean in zip(theta, response, strict=True):
                    sites = [*model["corners"], position["position"]]
                    reconstructed = [
                        dot([*corners, parameter], basis(*map(Fraction, site))) for site in sites
                    ]
                    residual.append(
                        [x - y for x, y in zip(reconstructed, [*corners, mean], strict=True)]
                    )
                routes = {
                    "old": intersect_union(merge_union([old]), [theta]),
                    "bernstein": intersect_union(merge_union([bern]), [theta]),
                    "inner": intersect_union(inner, [theta]),
                    "outer": intersect_union(outer, [theta]),
                }
                rows.append(
                    {
                        "position_id": position["id"],
                        "response_intercept": r,
                        "response_slope": s,
                        "data_theta": theta,
                        "data_target": [functional([*corners, x]) for x in theta],
                        "reconstruction_residual": residual,
                        **{name + "_theta": u for name, u in routes.items()},
                        **{
                            name + "_targets": project_union(u, offset, q[4])
                            for name, u in routes.items()
                        },
                        "point_classification": (
                            "certified"
                            if routes["inner"]
                            else "refuted"
                            if not routes["outer"]
                            else "unresolved"
                        )
                        if budget["id"] == "point"
                        else None,
                    }
                )
            budgets.append(
                {
                    "id": budget["id"],
                    "response_interval": response,
                    "endpoint_checks": [endpoint_check(family, x) for x in response],
                    "positions": rows,
                    "menus": expected_menus(model["menus"], rows),
                }
            )
        cases.append(
            {
                "id": declared["id"],
                "corners": list(corners),
                "center_mean": center,
                "target_offset": offset,
                "target_slope": q[4],
                "constraints": {
                    "old_theta": old,
                    "patches": patches,
                    "witnesses": witnesses,
                    "bernstein_theta": bern,
                    "witness_theta": witness,
                    "inner_theta": inner,
                    "outer_theta": outer,
                },
                "law_family": family,
                "budgets": budgets,
            }
        )
    return {
        "geometry": {"volume": volume, "sigma": volume**4, "coefficient_integrals": q},
        "positions": positions,
        "cases": cases,
    }


def expected_refinement(protocol, baseline):
    """Direct quarter nets; no parent coefficients enter reconstruction."""
    contract = protocol["refinement"]
    model = protocol["model"]["model"]["model"]
    nodes = list(map(Fraction, contract["nodes"]))
    witness_nodes = list(map(Fraction, contract["witness_nodes"]))
    reports = []
    for case in baseline["cases"]:
        corners = case["corners"]
        patches = [affine_patch(corners, leaf, nodes) for leaf in contract["leaves"]]
        witnesses = []
        for point in itertools.product(witness_nodes, repeat=2):
            value = [dot(corners, basis(*point)[:4]), basis(*point)[4]]
            witnesses.append(
                {"position": list(point), "value": value, "allowed": arrangement([value])}
            )
        gap = 16 * (1 - max(map(abs, corners)))
        old = [-gap, gap] if gap >= 0 else None
        bern = arrangement(
            [pair for patch in patches for row in patch["coefficients"] for pair in row]
        )
        witness = arrangement([w["value"] for w in witnesses])
        inner, outer = merge_union([old, bern]), merge_union([witness])
        budgets = []
        for config in protocol["model"]["interval_budgets"]:
            radius = Fraction(config["radius"])
            response = [
                max(Fraction(-1), case["center_mean"] - radius),
                min(Fraction(1), case["center_mean"] + radius),
            ]
            rows = []
            for position in baseline["positions"]:
                r, s = dot(corners, position["basis"][:4]), position["basis"][4]
                theta = [(x - r) / s for x in response]
                residual = []
                for parameter, mean in zip(theta, response, strict=True):
                    sites = [*model["corners"], position["position"]]
                    values = [
                        dot([*corners, parameter], basis(*map(Fraction, site))) for site in sites
                    ]
                    residual.append([x - y for x, y in zip(values, [*corners, mean], strict=True)])
                routes = {
                    "old": intersect_union(merge_union([old]), [theta]),
                    "bernstein": intersect_union(merge_union([bern]), [theta]),
                    "inner": intersect_union(inner, [theta]),
                    "outer": intersect_union(outer, [theta]),
                }
                rows.append(
                    {
                        "position_id": position["id"],
                        "response_intercept": r,
                        "response_slope": s,
                        "data_theta": theta,
                        "data_target": [functional([*corners, x]) for x in theta],
                        "reconstruction_residual": residual,
                        **{name + "_theta": value for name, value in routes.items()},
                        **{
                            name + "_targets": project_union(
                                value, case["target_offset"], case["target_slope"]
                            )
                            for name, value in routes.items()
                        },
                        "point_classification": (
                            "certified"
                            if routes["inner"]
                            else "refuted"
                            if not routes["outer"]
                            else "unresolved"
                        )
                        if config["id"] == "point"
                        else None,
                    }
                )
            budgets.append(
                {
                    "id": config["id"],
                    "response_interval": response,
                    "positions": rows,
                    "menus": expected_menus(model["menus"], rows),
                }
            )
        reports.append(
            {
                "id": case["id"],
                "constraints": {
                    "old_theta": old,
                    "patches": patches,
                    "witnesses": witnesses,
                    "bernstein_theta": bern,
                    "witness_theta": witness,
                    "inner_theta": inner,
                    "outer_theta": outer,
                },
                "budgets": budgets,
            }
        )
    return reports


def bj_expected(protocol):
    baseline = bi_expected(protocol["model"])
    return {"bi_model": baseline, "refinement": expected_refinement(protocol, baseline)}


def trim(poly):
    result = list(poly)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result or [Fraction(0)]


def pa(left, right):
    return trim(
        [
            (left[i] if i < len(left) else Fraction(0))
            + (right[i] if i < len(right) else Fraction(0))
            for i in range(max(len(left), len(right)))
        ]
    )


def ps(poly, scalar):
    return trim([scalar * value for value in poly])


def pm(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def pd(poly):
    return trim([i * value for i, value in enumerate(poly)][1:])


def pe(poly, value):
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def pdiv(left, right):
    remainder, divisor = trim(left), trim(right)
    if divisor == [0]:
        raise ValueError("zero polynomial divisor")
    quotient = [Fraction(0)] * max(1, len(remainder) - len(divisor) + 1)
    while remainder != [0] and len(remainder) >= len(divisor):
        shift = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[shift] += coefficient
        remainder = pa(remainder, [Fraction(0)] * shift + ps(divisor, -coefficient))
    return trim(quotient), remainder


def pgcd(left, right):
    a, b = trim(left), trim(right)
    while b != [0]:
        a, b = b, pdiv(a, b)[1]
    return ps(a, 1 / a[-1]) if a != [0] else a


def primitive(poly):
    denominator = math.lcm(*(x.denominator for x in poly))
    integers = [int(x * denominator) for x in poly]
    content = math.gcd(*integers)
    if not content:
        raise ValueError("zero eliminant")
    signed_content = content if integers[-1] > 0 else -content
    return [Fraction(x // signed_content) for x in integers], Fraction(signed_content, denominator)


def polynomial_determinant(matrix):
    """Sylvester determinant by permutations, not the engines' expanded formulas."""
    size = len(matrix)
    result = [Fraction(0)]
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j] for i in range(size) for j in range(i + 1, size)
        )
        term = [Fraction((-1) ** inversions)]
        for i, j in enumerate(permutation):
            term = pm(term, matrix[i][j])
        result = pa(result, term)
    return result


def symmetric_signature(matrix):
    """Exact congruence inertia, including zero-diagonal 2x2 pivots."""
    work = [list(row) for row in matrix]
    signature = 0
    while work:
        pivot = next((i for i in range(len(work)) if work[i][i]), None)
        if pivot is not None:
            order = [pivot] + [i for i in range(len(work)) if i != pivot]
            work = [[work[i][j] for j in order] for i in order]
            d = work[0][0]
            signature += 1 if d > 0 else -1
            work = [
                [work[i][j] - work[i][0] * work[0][j] / d for j in range(1, len(work))]
                for i in range(1, len(work))
            ]
            continue
        pair = next(
            ((i, j) for i in range(len(work)) for j in range(i + 1, len(work)) if work[i][j]),
            None,
        )
        if pair is None:
            break
        i, j = pair
        order = [i, j] + [k for k in range(len(work)) if k not in pair]
        work = [[work[a][b] for b in order] for a in order]
        d = work[0][1]
        work = [
            [
                work[a][b] - (work[a][0] * work[1][b] + work[a][1] * work[0][b]) / d
                for b in range(2, len(work))
            ]
            for a in range(2, len(work))
        ]
    return signature


@lru_cache(maxsize=24)
def quotient_traces(polynomial):
    """Traces of multiplication by powers in Q[x]/P, using direct remainders."""
    degree = len(polynomial) - 1
    traces = []
    for power in range(2 * degree + 1):
        total = Fraction(0)
        for column in range(degree):
            monomial = [Fraction(0)] * (power + column) + [Fraction(1)]
            remainder = pdiv(monomial, polynomial)[1]
            total += remainder[column] if column < len(remainder) else Fraction(0)
        traces.append(total)
    return tuple(traces)


def hermite_signature(polynomial, weight):
    traces = quotient_traces(tuple(polynomial))
    degree = len(polynomial) - 1
    matrix = [
        [
            sum(
                (coefficient * traces[i + j + k] for k, coefficient in enumerate(weight)),
                Fraction(0),
            )
            for j in range(degree)
        ]
        for i in range(degree)
    ]
    return symmetric_signature(matrix)


def hermite_count(polynomial, low, high):
    """Hermite trace-form query: roots in an open interval, not Sturm/Descartes."""
    real_roots = hermite_signature(polynomial, [Fraction(1)])
    signed = hermite_signature(polynomial, [-low * high, low + high, Fraction(-1)])
    endpoint_roots = int(pe(polynomial, low) == 0) + int(pe(polynomial, high) == 0)
    doubled = real_roots + signed - endpoint_roots
    if doubled < 0 or doubled % 2:
        raise ValueError("invalid independent Hermite count")
    return doubled // 2


def isolate_by_hermite(polynomial, depth, max_depth, max_nodes):
    polynomial = trim(polynomial)
    if polynomial == [0] or len(pgcd(polynomial, pd(polynomial))) != 1:
        raise ValueError("zero or repeated independent polynomial")
    if len(polynomial) == 1:
        return []
    visited = 0

    def visit(low, high, level):
        nonlocal visited
        visited += 1
        if visited > max_nodes:
            raise ValueError("independent isolation node cap")
        count = hermite_count(polynomial, low, high)
        if not count:
            return []
        middle = (low + high) / 2
        if pe(polynomial, middle) == 0:
            if count == 1:
                return [[middle, middle]]
            if level >= max_depth:
                raise ValueError("independent isolation depth cap")
            return (
                visit(low, middle, level + 1) + [[middle, middle]] + visit(middle, high, level + 1)
            )
        if level >= depth and count == 1 and pe(polynomial, low) and pe(polynomial, high):
            return [[low, high]]
        if level >= max_depth:
            raise ValueError("independent isolation depth cap")
        return visit(low, middle, level + 1) + visit(middle, high, level + 1)

    return visit(Fraction(0), Fraction(1), 0)


def certificate_parts(protocol):
    config = protocol["boundary"]
    a, c, d, delta = [list(map(Fraction, config[name])) for name in ("A", "C", "D", "delta")]
    p = pa(pm(pd(a), d), ps(pm(a, pd(d)), -1))
    q = pa(pm(pd(c), d), ps(pm(c, pd(d)), -1))
    zero = [Fraction(0)]
    raw = polynomial_determinant([[c, ps(a, 2), ps(a, -1)], [q, p, zero], [zero, q, p]])
    defining, scalar = primitive(raw)
    if len(pgcd(defining, pd(defining))) != 1:
        raise ValueError("fixed defining polynomial is not squarefree")
    s = pm(a, pa(a, c))
    k = pa(pm(c, d), ps(pm(s, delta), -2))
    u_num = ps(pm(delta, a), 11)
    return {
        "A": a,
        "C": c,
        "D": d,
        "delta": delta,
        "p": p,
        "q": q,
        "S": s,
        "k": k,
        "raw": raw,
        "P": defining,
        "scalar": scalar,
        "u_image": {"numerator": u_num, "denominator": pa(u_num, k)},
        "beta_image": {
            "numerator": pa(ps(delta, 121), ps(k, 2)),
            "denominator": ps(pm(delta, d), 66),
        },
    }


def imul(left, right):
    values = [a * b for a in left for b in right]
    return [min(values), max(values)]


def ihorner(polynomial, interval):
    result = [Fraction(0), Fraction(0)]
    for coefficient in reversed(polynomial):
        result = [value + coefficient for value in imul(result, interval)]
    return result


def iquotient(numerator, denominator):
    if denominator[0] <= 0 <= denominator[1]:
        raise ValueError("independent image denominator includes zero")
    return imul(numerator, sorted([1 / denominator[0], 1 / denominator[1]]))


def contact_remainders(parts):
    """Rational arithmetic in Q[v]/P; bounded residues avoid huge symbolic powers."""
    defining = parts["P"]
    for name in ("u", "beta"):
        if pgcd(defining, parts[name + "_image"]["denominator"]) != [Fraction(1)]:
            raise ValueError("nonunit contact denominator in quotient algebra")

    def reduce(poly):
        return pdiv(poly, defining)[1]

    def const(value):
        return [Fraction(value)], [Fraction(1)]

    def add(left, right):
        return reduce(pa(pm(left[0], right[1]), pm(right[0], left[1]))), reduce(
            pm(left[1], right[1])
        )

    def mul(left, right):
        return reduce(pm(left[0], right[0])), reduce(pm(left[1], right[1]))

    def neg(value):
        return ps(value[0], -1), value[1]

    def sub(left, right):
        return add(left, neg(right))

    one = const(1)
    u = tuple(parts["u_image"][key] for key in ("numerator", "denominator"))
    beta = tuple(parts["beta_image"][key] for key in ("numerator", "denominator"))
    v = ([Fraction(0), Fraction(1)], [Fraction(1)])
    bubble = mul(mul(u, sub(one, u)), mul(v, sub(one, v)))
    r = add(
        add(const(Fraction(1, 2)), mul(const(Fraction(-5, 6)), u)),
        add(mul(const(Fraction(1, 6)), v), mul(const(Fraction(-1, 3)), mul(u, v))),
    )
    value = sub(add(r, mul(beta, bubble)), one)
    du = add(
        add(const(Fraction(-5, 6)), mul(const(Fraction(-1, 3)), v)),
        mul(beta, mul(sub(one, mul(const(2), u)), mul(v, sub(one, v)))),
    )
    dv = add(
        add(const(Fraction(1, 6)), mul(const(Fraction(-1, 3)), u)),
        mul(beta, mul(mul(u, sub(one, u)), sub(one, mul(const(2), v)))),
    )
    return {name: reduce(result[0]) for name, result in (("value", value), ("du", du), ("dv", dv))}


def expected_certificate(protocol):
    parts = certificate_parts(protocol)
    config = protocol["boundary"]["isolation"]
    intervals = isolate_by_hermite(
        parts["P"], config["depth"], config["max_depth"], config["max_nodes"]
    )
    roots, admitted = [], []
    for cell in intervals:
        k_range = ihorner(parts["k"], cell)
        if cell[1] <= Fraction(1, 2):
            label = "rejected_nonpositive_delta"
        elif cell[0] > Fraction(1, 2) and k_range[1] < 0:
            label = "rejected_wrong_radical_sign"
        elif cell[0] > Fraction(1, 2) and k_range[0] > 0:
            label = "admissible"
            admitted.append(cell)
        else:
            raise ValueError("independent root sign unresolved")
        roots.append({"interval": cell, "classification": label})
    if len(admitted) != 1:
        raise ValueError("independent admissible-root census")
    alpha = admitted[0]
    denominator = {
        name: ihorner(parts[name + "_image"]["denominator"], alpha) for name in ("u", "beta")
    }
    images = {
        name: iquotient(ihorner(parts[name + "_image"]["numerator"], alpha), denominator[name])
        for name in ("u", "beta")
    }
    return {
        "raw_eliminant": parts["raw"],
        "normalization_scalar": parts["scalar"],
        "defining_polynomial": parts["P"],
        "roots": roots,
        "alpha_interval": alpha,
        "k_interval": ihorner(parts["k"], alpha),
        "u_image": parts["u_image"],
        "beta_image": parts["beta_image"],
        "u_interval": images["u"],
        "beta_interval": images["beta"],
        "denominator_intervals": denominator,
        "contact_remainders": contact_remainders(parts),
        "convexity": {
            "corner_gaps": list(map(Fraction, ("1/2", "4/3", "1/3", "3/2"))),
            "hessian_determinant_numerator": 3,
            "minimum_corner_gap": Fraction(1, 3),
        },
        "status": "exact_positive_boundary",
    }


def beta_affine(offset, scale):
    return offset if scale == 0 else {"kind": "beta_affine", "offset": offset, "scale": scale}


def endpoint_coefficients(value):
    return (value, Fraction(0)) if type(value) is Fraction else (value["offset"], value["scale"])


def endpoint_compare(left, right, beta_interval):
    a, b = endpoint_coefficients(left)
    c, d = endpoint_coefficients(right)
    offset, scale = a - c, b - d
    if offset == 0 and scale == 0:
        return 0
    values = [offset + scale * x for x in beta_interval]
    if min(values) > 0:
        return 1
    if max(values) < 0:
        return -1
    raise ValueError("independent endpoint order unresolved")


def endpoint_project(value, offset, scale):
    a, b = endpoint_coefficients(value)
    return beta_affine(offset + scale * a, scale * b)


def endpoint_merge(intervals, beta_interval):
    """Connected components of the closed overlap graph; independent union route."""
    pending = copy.deepcopy(intervals)
    components = []
    compare = lambda a, b: endpoint_compare(a, b, beta_interval)
    while pending:
        low, high = pending.pop()
        changed = True
        while changed:
            changed = False
            for index, (a, b) in enumerate(pending):
                if compare(low, b) <= 0 and compare(a, high) <= 0:
                    low = a if compare(a, low) < 0 else low
                    high = b if compare(b, high) > 0 else high
                    pending.pop(index)
                    changed = True
                    break
        components.append([low, high])
    return sorted(components, key=cmp_to_key(lambda a, b: compare(a[0], b[0])))


def endpoint_intersection(left, right, beta_interval):
    pieces = []
    for (a, b), (c, d) in itertools.product(left, right):
        low = a if endpoint_compare(a, c, beta_interval) >= 0 else c
        high = b if endpoint_compare(b, d, beta_interval) <= 0 else d
        if endpoint_compare(low, high, beta_interval) <= 0:
            pieces.append([low, high])
    return endpoint_merge(pieces, beta_interval)


def endpoint_summary(intervals, beta_interval):
    normalized = endpoint_merge(intervals, beta_interval)
    return {
        "intervals": normalized,
        "hull": [normalized[0][0], normalized[-1][1]] if normalized else None,
        "gaps": [[a[1], b[0]] for a, b in itertools.pairwise(normalized)],
    }


def expected_resolution(protocol, baseline, certificate):
    interval = certificate["beta_interval"]
    boundary = beta_affine(Fraction(0), Fraction(1))
    positive = [[Fraction(0), boundary]]
    offset, slope = [
        Fraction(protocol["boundary"][key]) for key in ("target_offset", "target_slope")
    ]
    case = next(case for case in baseline["refinement"] if case["id"] == "asymmetric")
    budgets = []
    for old in case["budgets"]:
        positions = []
        for row in old["positions"]:
            negative = intersect_union(row["inner_theta"], [[None, Fraction(0)]])
            if negative != intersect_union(row["outer_theta"], [[None, Fraction(0)]]):
                raise ValueError("unresolved inherited negative piece")
            theta = endpoint_merge(
                negative + endpoint_intersection([row["data_theta"]], positive, interval), interval
            )
            targets = endpoint_merge(
                [
                    [endpoint_project(a, offset, slope), endpoint_project(b, offset, slope)]
                    for a, b in theta
                ],
                interval,
            )
            positions.append(
                {
                    "position_id": row["position_id"],
                    "data_theta": row["data_theta"],
                    "negative_theta": negative,
                    "theta": theta,
                    "targets": targets,
                    "status": "exact",
                }
            )
        menus = []
        for old_menu in old["menus"]:
            hypotheses = [
                {key: row[key] for key in ("position_id", "theta", "targets")}
                for row in positions
                if row["position_id"] in old_menu["position_ids"] and row["theta"]
            ]
            target_set = endpoint_summary(
                [piece for row in hypotheses for piece in row["targets"]], interval
            )
            components = target_set["intervals"]
            identified = len(components) == 1 and endpoint_compare(*components[0], interval) == 0
            menus.append(
                {
                    "id": old_menu["id"],
                    "position_ids": old_menu["position_ids"],
                    "hypotheses": hypotheses,
                    "target_set": target_set,
                    "existence_status": "feasible" if components else "infeasible",
                    "target_status": "identified"
                    if identified
                    else "ambiguous"
                    if components
                    else "infeasible",
                    "status": "exact",
                }
            )
        budgets.append(
            {
                "id": old["id"],
                "response_interval": old["response_interval"],
                "positions": positions,
                "menus": menus,
            }
        )
    others = [case for case in baseline["refinement"] if case["id"] != "asymmetric"]
    return {
        "case_id": "asymmetric",
        "positive_theta": positive,
        "budgets": budgets,
        "summary": {
            "resolved_positions": sum(len(b["positions"]) for b in budgets),
            "resolved_menus": sum(len(b["menus"]) for b in budgets),
            "collection_exact_positions": sum(len(b["positions"]) for b in budgets)
            + sum(
                row["inner_theta"] == row["outer_theta"]
                for case in others
                for budget in case["budgets"]
                for row in budget["positions"]
            ),
            "collection_exact_menus": sum(len(b["menus"]) for b in budgets)
            + sum(
                row["hypothesis_set_status"] == "exact" and row["target_set_status"] == "exact"
                for case in others
                for budget in case["budgets"]
                for row in budget["menus"]
            ),
            "remaining_global_negative_gap": True,
        },
    }


def expected(protocol):
    baseline = bj_expected(protocol["model"])
    certificate = expected_certificate(protocol)
    return {
        "bj_model": baseline,
        "certificate": certificate,
        "resolution": expected_resolution(protocol, baseline, certificate),
    }


@lru_cache(maxsize=1)
def evaluated():
    study = load_module("study")
    protocol = study.load_protocol()
    return study, protocol, study.compare_routes()


@lru_cache(maxsize=1)
def semantic_engines():
    study = load_module("study")
    identities = study.source_identities()
    return [
        study._load_engine(
            name, identities[str((study.ROOT / (name + ".py")).relative_to(study.REPO))]
        )
        for name in ("quantum", "reference")
    ]


def exact_tree(test, actual, wanted, path=()):
    test.assertIs(type(actual), type(wanted), str(path))
    if type(wanted) is dict:
        test.assertEqual(set(actual), set(wanted), str(path))
        for key in wanted:
            exact_tree(test, actual[key], wanted[key], (*path, key))
    elif type(wanted) is list:
        test.assertEqual(len(actual), len(wanted), str(path))
        for i, (a, b) in enumerate(zip(actual, wanted, strict=True)):
            exact_tree(test, a, b, (*path, i))
    else:
        test.assertEqual(actual, wanted, str(path))


def union_subset(left, right):
    return intersect_union(left, right) == merge_union(left)


class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.certificate = cls.report["certificate"]
        cls.parts = certificate_parts(cls.protocol)

    def test_complete_independent_native_report(self):
        exact_keys(self, self.report, "bj_model certificate resolution")
        exact_tree(self, self.report, expected(self.protocol))
        self.assertIs(type(self.certificate["convexity"]["hessian_determinant_numerator"]), int)
        self.assertIs(self.report["resolution"]["summary"]["remaining_global_negative_gap"], True)
        self.assertEqual(
            self.study.encode(self.report)["certificate"]["status"], "exact_positive_boundary"
        )

    def test_verified_geometry_and_primitive_sylvester_identity(self):
        for i, j in itertools.product(range(6), repeat=2):
            self.assertEqual(
                integrate(lambda u, v, i=i, j=j: u**i * v**j), Fraction(1, (i + 1) * (j + 1))
            )
        gram, inverse = bernstein_gram()
        self.assertEqual(multiply(gram, inverse), identity(3))
        self.assertEqual(multiply(inverse, gram), identity(3))
        p = self.parts
        raw = self.certificate["raw_eliminant"]
        self.assertEqual(
            raw,
            ps(self.certificate["defining_polynomial"], self.certificate["normalization_scalar"]),
        )
        self.assertEqual(pa(ps(p["p"], 2), p["q"]), ps(p["delta"], 11))
        self.assertEqual(p["k"], pa(ps(p["p"], -11), ps(pm(p["A"], p["q"]), -1)))
        squared = pa(pm(p["k"], p["k"]), ps(pm(pm(p["delta"], p["delta"]), p["S"]), -121))
        self.assertEqual(squared, pm(p["C"], raw))
        self.assertEqual(pdiv(squared, p["C"]), (raw, [Fraction(0)]))
        defining = self.certificate["defining_polynomial"]
        self.assertTrue(all(type(x) is Fraction and x.denominator == 1 for x in defining))
        self.assertEqual(math.gcd(*(x.numerator for x in defining)), 1)
        self.assertGreater(defining[-1], 0)
        self.assertEqual(pgcd(defining, pd(defining)), [Fraction(1)])
        self.assertNotEqual(pe(defining, Fraction(1, 2)), 0)
        self.assertEqual(
            functional(
                [Fraction(1, 2), Fraction(-1, 3), Fraction(2, 3), Fraction(-1, 2), Fraction(0)]
            ),
            Fraction(13, 216),
        )
        self.assertEqual(functional([Fraction(0)] * 4 + [Fraction(1)]), Fraction(1, 144))

    def test_full_root_census_canonical_cells_and_unsquared_filter(self):
        defining = self.certificate["defining_polynomial"]
        roots = self.certificate["roots"]
        self.assertEqual(len(roots), hermite_count(defining, Fraction(0), Fraction(1)))
        config = self.protocol["boundary"]["isolation"]
        self.assertEqual(
            [row["interval"] for row in roots],
            isolate_by_hermite(defining, config["depth"], config["max_depth"], config["max_nodes"]),
        )
        admissible = []
        for index, row in enumerate(roots):
            low, high = row["interval"]
            self.assertLess(Fraction(0), low)
            self.assertLess(high, Fraction(1))
            if index:
                self.assertLess(roots[index - 1]["interval"][1], low)
            if low == high:
                self.assertEqual(pe(defining, low), 0)
            else:
                self.assertEqual(hermite_count(defining, low, high), 1)
                self.assertNotEqual(pe(defining, low), 0)
                self.assertNotEqual(pe(defining, high), 0)
                self.assertNotEqual(pe(defining, (low + high) / 2), 0)
                self.assertEqual(high - low, Fraction(1, 2 ** config["depth"]))
            k_interval = ihorner(self.parts["k"], row["interval"])
            if row["classification"] == "admissible":
                self.assertGreater(low, Fraction(1, 2))
                self.assertGreater(k_interval[0], 0)
                admissible.append(row["interval"])
            elif row["classification"] == "rejected_nonpositive_delta":
                self.assertLessEqual(high, Fraction(1, 2))
            else:
                self.assertEqual(row["classification"], "rejected_wrong_radical_sign")
                self.assertGreater(low, Fraction(1, 2))
                self.assertLess(k_interval[1], 0)
        self.assertEqual(admissible, [self.certificate["alpha_interval"]])

    def test_unreduced_images_horner_enclosures_and_contact_remainders(self):
        c, p = self.certificate, self.parts
        for name in ("u", "beta"):
            self.assertEqual(c[name + "_image"], p[name + "_image"])
            denominator = ihorner(p[name + "_image"]["denominator"], c["alpha_interval"])
            numerator = ihorner(p[name + "_image"]["numerator"], c["alpha_interval"])
            self.assertEqual(c["denominator_intervals"][name], denominator)
            self.assertGreater(denominator[0], 0)
            self.assertEqual(c[name + "_interval"], iquotient(numerator, denominator))
        for interval in (c["alpha_interval"], c["u_interval"]):
            self.assertGreater(interval[0], 0)
            self.assertLess(interval[1], 1)
        self.assertGreater(c["beta_interval"][0], 0)
        self.assertEqual(c["k_interval"], ihorner(p["k"], c["alpha_interval"]))
        self.assertEqual(c["contact_remainders"], contact_remainders(p))
        self.assertEqual(
            c["contact_remainders"], {name: [Fraction(0)] for name in ("value", "du", "dv")}
        )
        # None of the physical contact denominators can vanish at the selected root.
        for name in ("u", "beta"):
            self.assertEqual(pgcd(p["P"], p[name + "_image"]["denominator"]), [Fraction(1)])

    def test_convexity_reciprocals_boundary_and_closed_contact_reasoning(self):
        gaps = list(map(Fraction, ("1/2", "4/3", "1/3", "3/2")))
        self.assertEqual(self.certificate["convexity"]["corner_gaps"], gaps)
        self.assertEqual(self.certificate["convexity"]["minimum_corner_gap"], min(gaps))
        corners = list(map(Fraction, ("1/2", "-1/3", "2/3", "-1/2")))
        # Finite regression controls check the decomposition and Hessian wiring;
        # globality relies on the displayed algebraic proof in the README.
        for u, v in itertools.product(map(Fraction, ("1/5", "1/2", "4/5")), repeat=2):
            r, bubble = dot(corners, basis(u, v)[:4]), basis(u, v)[4]
            reciprocal = (
                gaps[0] / (u * v)
                + gaps[1] / ((1 - u) * v)
                + gaps[2] / (u * (1 - v))
                + gaps[3] / ((1 - u) * (1 - v))
            )
            self.assertEqual((1 - r) / bubble, reciprocal)
            self.assertGreaterEqual(1 - r, min(gaps))
            xx, xy, yy = 2 / (u**3 * v), 1 / (u**2 * v**2), 2 / (u * v**3)
            self.assertGreater(xx, 0)
            self.assertEqual(xx * yy - xy**2, Fraction(3) / (u**4 * v**4))
        for u, v in itertools.product((Fraction(0), Fraction(1)), repeat=2):
            self.assertEqual(basis(u, v)[4], 0)
            self.assertLessEqual(abs(dot(corners, basis(u, v)[:4])), 1)
        u, v = self.certificate["u_interval"], self.certificate["alpha_interval"]
        bubble_lower = u[0] * (1 - u[1]) * v[0] * (1 - v[1])
        self.assertGreater(bubble_lower, 0)
        for excess in (Fraction(1, 100), Fraction(1), Fraction(3)):
            # At the exact zero-residue contact, f_(beta+excess)-1=excess*b>0.
            self.assertGreater(excess * bubble_lower, 0)
        boundary = self.report["resolution"]["positive_theta"][0][1]
        exact_tree(self, boundary, beta_affine(Fraction(0), Fraction(1)))
        self.assertIs(type(boundary), dict)
        self.assertNotEqual(boundary, sum(self.certificate["beta_interval"]) / 2)


class ResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.beta = cls.report["certificate"]["beta_interval"]
        cls.resolution = cls.report["resolution"]
        cls.old = next(c for c in cls.report["bj_model"]["refinement"] if c["id"] == "asymmetric")

    def subset(self, left, right):
        self.assertEqual(
            endpoint_intersection(left, right, self.beta), endpoint_merge(left, self.beta)
        )

    def test_negative_preservation_closed_beta_sandwich_and_projection(self):
        offset, slope = Fraction(13, 216), Fraction(1, 144)
        for budget, old in zip(self.resolution["budgets"], self.old["budgets"], strict=True):
            self.assertEqual(budget["id"], old["id"])
            self.assertEqual(budget["response_interval"], old["response_interval"])
            for row, previous in zip(budget["positions"], old["positions"], strict=True):
                self.assertEqual(row["position_id"], previous["position_id"])
                self.assertEqual(row["data_theta"], previous["data_theta"])
                negative = intersect_union(previous["inner_theta"], [[None, Fraction(0)]])
                self.assertEqual(
                    negative, intersect_union(previous["outer_theta"], [[None, Fraction(0)]])
                )
                self.assertEqual(row["negative_theta"], negative)
                self.subset(previous["inner_theta"], row["theta"])
                self.subset(row["theta"], previous["outer_theta"])
                self.subset(previous["inner_targets"], row["targets"])
                self.subset(row["targets"], previous["outer_targets"])
                if previous["inner_theta"] == previous["outer_theta"]:
                    exact_tree(self, row["theta"], previous["inner_theta"])
                self.assertEqual(
                    row["targets"],
                    endpoint_merge(
                        [
                            [endpoint_project(a, offset, slope), endpoint_project(b, offset, slope)]
                            for a, b in row["theta"]
                        ],
                        self.beta,
                    ),
                )
                self.assertEqual(row["status"], "exact")
        expected = expected_resolution(
            self.protocol, self.report["bj_model"], self.report["certificate"]
        )
        exact_tree(self, self.resolution, expected)

    def test_menu_hypotheses_components_gaps_statuses_and_data_nesting(self):
        for budget, old in zip(self.resolution["budgets"], self.old["budgets"], strict=True):
            for menu, previous in zip(budget["menus"], old["menus"], strict=True):
                self.assertEqual(menu["position_ids"], previous["position_ids"])
                selected = [
                    {key: row[key] for key in ("position_id", "theta", "targets")}
                    for row in budget["positions"]
                    if row["position_id"] in menu["position_ids"] and row["theta"]
                ]
                self.assertEqual(menu["hypotheses"], selected)
                self.assertEqual(
                    menu["target_set"],
                    endpoint_summary(
                        [piece for row in selected for piece in row["targets"]], self.beta
                    ),
                )
                intervals = menu["target_set"]["intervals"]
                self.assertEqual(
                    menu["target_set"]["hull"],
                    [intervals[0][0], intervals[-1][1]] if intervals else None,
                )
                for left, right in menu["target_set"]["gaps"]:
                    self.assertLess(endpoint_compare(left, right, self.beta), 0)
                self.subset(previous["target_sets"]["inner"]["intervals"], intervals)
                self.subset(intervals, previous["target_sets"]["outer"]["intervals"])
                if previous["target_set_status"] == "exact":
                    self.assertEqual(intervals, previous["target_sets"]["inner"]["intervals"])
                if previous["existence_status"] in ("feasible", "infeasible"):
                    self.assertEqual(menu["existence_status"], previous["existence_status"])
                if previous["target_status"] in ("identified", "ambiguous", "infeasible"):
                    self.assertEqual(menu["target_status"], previous["target_status"])
                self.assertEqual(menu["status"], "exact")
        for small, large in itertools.pairwise(self.resolution["budgets"]):
            for left, right in zip(small["positions"], large["positions"], strict=True):
                self.subset(left["theta"], right["theta"])
                self.subset(left["targets"], right["targets"])
            for left, right in zip(small["menus"], large["menus"], strict=True):
                self.subset(left["target_set"]["intervals"], right["target_set"]["intervals"])

    def test_census_other_cases_and_unchanged_coupled_quantum_laws(self):
        baseline = self.report["bj_model"]
        summary = self.resolution["summary"]
        other = [case for case in baseline["refinement"] if case["id"] != "asymmetric"]
        self.assertEqual(len(other), 6)
        exact_positions = sum(
            row["inner_theta"] == row["outer_theta"]
            for case in other
            for b in case["budgets"]
            for row in b["positions"]
        )
        exact_menus = sum(
            row["hypothesis_set_status"] == row["target_set_status"] == "exact"
            for case in other
            for b in case["budgets"]
            for row in b["menus"]
        )
        self.assertEqual(summary["resolved_positions"], 18)
        self.assertEqual(summary["resolved_menus"], 15)
        self.assertEqual(summary["collection_exact_positions"], 18 + exact_positions)
        self.assertEqual(summary["collection_exact_menus"], 15 + exact_menus)
        self.assertIs(summary["remaining_global_negative_gap"], True)
        self.assertEqual(
            sum(len(c["law_family"]["rows"]) for c in baseline["bi_model"]["cases"]), 224
        )
        self.assertEqual(
            sum(
                len(b["endpoint_checks"])
                for c in baseline["bi_model"]["cases"]
                for b in c["budgets"]
            ),
            42,
        )
        for case in baseline["bi_model"]["cases"]:
            law = case["law_family"]
            for mean in (Fraction(-1), Fraction(0), Fraction(1)):
                probabilities = [at(row["probability"], mean) for row in law["rows"]]
                self.assertEqual(sum(probabilities), 1)
                self.assertTrue(all(x >= 0 for x in probabilities))
                for row, probability in zip(law["rows"], probabilities, strict=True):
                    state = [at(pair, mean) for pair in row["state_diagonal"]]
                    self.assertEqual(sum(state), probability)
                    self.assertEqual(state, branch_state(row["outcomes"], probability))
                self.assertEqual(
                    [
                        sum(at(row["state_diagonal"][i], mean) for row in law["rows"])
                        for i in range(32)
                    ],
                    [at(pair, mean) for pair in law["averaged_state"]],
                )


class ScalarSemanticTests(unittest.TestCase):
    def test_hermite_inertia_and_open_root_counts_independent_known_controls(self):
        f = Fraction
        for matrix, signature in [
            ([[f(0), f(1)], [f(1), f(0)]], 0),
            ([[f(0), f(1), f(2)], [f(1), f(0), f(3)], [f(2), f(3), f(0)]], -1),
            ([[f(2), f(0)], [f(0), f(-3)]], 0),
            ([[f(0)]], 0),
        ]:
            self.assertEqual(symmetric_signature(matrix), signature)
        polynomial = [f(1)]
        for root in (f(-1), f(0), f(1, 4), f(1, 2), f(3, 4), f(1), f(2)):
            polynomial = pm(polynomial, [-root, f(1)])
        self.assertEqual(hermite_count(polynomial, f(0), f(1)), 3)
        self.assertEqual(hermite_count(polynomial, f(1, 4), f(3, 4)), 1)
        self.assertEqual(hermite_count(pm(polynomial, [f(1), f(0), f(1)]), f(0), f(1)), 3)
        self.assertEqual(
            isolate_by_hermite(polynomial, 4, 64, 4096),
            [[f(1, 4)] * 2, [f(1, 2)] * 2, [f(3, 4)] * 2],
        )

    def test_both_isolators_canonical_known_roots_midpoint_first_and_endpoints(self):
        f = Fraction
        controls = [
            ([f(7)], 4, 64, 4096, []),
            ([-f(1, 2), f(1)], 0, 0, 1, [[f(1, 2), f(1, 2)]]),
            ([f(0), f(-1), f(1)], 4, 64, 4096, []),
            ([-f(1, 4), f(0), f(1)], 4, 64, 4096, [[f(1, 2), f(1, 2)]]),
            ([-f(1, 3), f(0), f(1)], 4, 64, 4096, [[f(9, 16), f(5, 8)]]),
            ([-f(9, 32), f(1)], 4, 64, 4096, [[f(9, 32), f(9, 32)]]),
            ([f(1), f(0), f(1)], 4, 64, 4096, []),
        ]
        for engine in semantic_engines():
            for poly, depth, maximum, nodes, wanted in controls:
                before = copy.deepcopy(poly)
                with self.subTest(engine=engine.__name__, poly=poly, depth=depth):
                    self.assertEqual(
                        engine._isolate_unit_roots(poly, depth, maximum, nodes), wanted
                    )
                    self.assertEqual(poly, before)
            product = pm([-f(1, 4), f(1)], [-f(3, 4), f(1)])
            self.assertEqual(
                engine._isolate_unit_roots(product, 4, 64, 4096),
                isolate_by_hermite(product, 4, 64, 4096),
            )

    def test_isolator_malformed_degenerate_caps_and_exhaustion_guards(self):
        f = Fraction

        class FractionChild(Fraction):
            pass

        malformed = [
            (None, 4, 64, 4096),
            ((f(1),), 4, 64, 4096),
            ([], 4, 64, 4096),
            ([f(0)], 4, 64, 4096),
            ([f(1), f(-2), f(1)], 4, 64, 4096),
            ([f(1)] + [f(0)] * 13, 4, 64, 4096),
            ([1, f(1)], 4, 64, 4096),
            ([True, f(1)], 4, 64, 4096),
            ([f(1), 0.0], 4, 64, 4096),
            ([f(1), "1"], 4, 64, 4096),
            ([f(1), FractionChild(1)], 4, 64, 4096),
            ([f(1)], True, 64, 4096),
            ([f(1)], -1, 64, 4096),
            ([f(1)], 4, 3, 4096),
            ([f(1)], 4, 65, 4096),
            ([f(1)], 4, 64, 0),
            ([f(1)], 4, 64, 4097),
            ([f(1)], 4, True, 4096),
            ([f(1)], 4, 64, True),
            ([-f(1, 3), f(1)], 4, 64, 1),
            ([-f(1, 3), f(1)], 4, 4, 1),
            (pm([-f(1, 4), f(1)], [-f(3, 4), f(1)]), 0, 0, 4096),
        ]
        for engine in semantic_engines():
            for args in malformed:
                with self.subTest(engine=engine.__name__, args=args), self.assertRaises(ValueError):
                    engine._isolate_unit_roots(*args)

    def test_endpoint_order_normalization_closed_merges_gaps_and_detachment(self):
        f = Fraction
        enclosure = [f(10), f(11)]
        boundary = beta_affine(f(0), f(1))
        controls = [
            (f(1), f(2), -1),
            (boundary, f(9), 1),
            (beta_affine(f(0), f(-1)), f(-9), -1),
            (boundary, copy.deepcopy(boundary), 0),
            (beta_affine(f(3), f(0)), f(3), 0),
            (beta_affine(f(2), f(1)), boundary, 1),
        ]
        for engine in semantic_engines():
            self.assertEqual(engine._beta_affine(f(3), f(0)), f(3))
            self.assertEqual(engine._beta_affine(f(0), f(1)), boundary)
            for a, b, expected_order in controls:
                with self.subTest(engine=engine.__name__, left=a, right=b):
                    self.assertEqual(engine._endpoint_compare(a, b, enclosure), expected_order)
                    self.assertEqual(engine._endpoint_compare(b, a, enclosure), -expected_order)
            union = [
                [boundary, beta_affine(f(2), f(1))],
                [f(0), boundary],
                [f(-3), f(-2)],
                [f(-3), f(-3)],
            ]
            before = copy.deepcopy(union)
            wanted = [[f(-3), f(-2)], [f(0), beta_affine(f(2), f(1))]]
            got = engine._merge_endpoint_intervals(union, enclosure)
            self.assertEqual(got, wanted)
            self.assertEqual(got, endpoint_merge(union, enclosure))
            self.assertEqual(union, before)
            got[-1][-1]["offset"] = f(100)
            self.assertEqual(union, before)
            self.assertEqual(engine._merge_endpoint_intervals([], enclosure), [])
            self.assertEqual(
                engine._merge_endpoint_intervals([[boundary, boundary]], enclosure),
                [[boundary, boundary]],
            )

    def test_endpoint_unresolved_orders_and_strict_native_admission(self):
        f = Fraction
        beta = beta_affine(f(0), f(1))
        interval = [f(10), f(11)]
        bad_endpoints = [
            None,
            1,
            True,
            0.0,
            "1",
            [],
            (),
            {},
            {"kind": "beta_affine", "offset": f(0)},
            {**beta, "extra": None},
            {**beta, "kind": "other"},
            {**beta, "scale": 1},
            {**beta, "offset": True},
        ]
        bad_intervals = [
            None,
            (),
            [],
            [f(10)],
            [f(11), f(10)],
            [f(0), None],
            [10, f(11)],
            [f(10), True],
            [f(10), f(11), f(12)],
        ]
        for engine in semantic_engines():
            for bad in bad_endpoints:
                with (
                    self.subTest(engine=engine.__name__, endpoint=bad),
                    self.assertRaises(ValueError),
                ):
                    engine._endpoint_compare(bad, f(0), interval)
            for bad in bad_intervals:
                with (
                    self.subTest(engine=engine.__name__, enclosure=bad),
                    self.assertRaises(ValueError),
                ):
                    engine._endpoint_compare(f(0), f(0), bad)
            for rational in (f(10), f(21, 2), f(11)):
                with (
                    self.subTest(engine=engine.__name__, rational=rational),
                    self.assertRaises(ValueError),
                ):
                    engine._endpoint_compare(beta, rational, interval)
            for args in [(0, f(1)), (f(0), True), (f(0), 1.0)]:
                with self.assertRaises(ValueError):
                    engine._beta_affine(*args)
            for union in [
                None,
                (),
                [None],
                [[f(1)]],
                [[f(2), f(1)]],
                [[f(0), beta], [f(21, 2), f(12)]],
            ]:
                with (
                    self.subTest(engine=engine.__name__, union=union),
                    self.assertRaises(ValueError),
                ):
                    engine._merge_endpoint_intervals(union, interval)


class RouteBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_module("study")
        self.protocol = {"public": [1, "contract"], "ratio": "1/3"}
        self.report = {
            "rational": Fraction(1, 3),
            "integer": 1,
            "rows": [Fraction(0)],
            "empty": None,
        }
        self.freeze = {
            "sources": {
                str((self.study.ROOT / (name + ".py")).relative_to(self.study.REPO)): {
                    "bytes": 1,
                    "sha256": "a" * 64,
                }
                for name in ("quantum", "reference")
            }
        }

    def compare(self, left, right):
        with (
            mock.patch.object(self.study, "_frozen", return_value=self.freeze),
            mock.patch.object(
                self.study, "load_protocol", return_value=copy.deepcopy(self.protocol)
            ),
            mock.patch.object(
                self.study,
                "_load_engine",
                side_effect=lambda name, _identity: SimpleNamespace(
                    analyze=left if name == "quantum" else right
                ),
            ),
        ):
            return self.study.compare_routes()

    def test_raw_report_numeric_type_and_extra_field_mutations(self):
        mutations = []
        for key, value in (
            ("rational", "1/3"),
            ("rational", Fraction(2, 3)),
            ("integer", True),
            ("integer", Fraction(1)),
            ("rows", [Fraction(1)]),
            ("rows", (Fraction(0),)),
            ("empty", "null"),
        ):
            changed = copy.deepcopy(self.report)
            changed[key] = value
            mutations.append(changed)
        changed = copy.deepcopy(self.report)
        changed["private"] = "unrecorded"
        mutations.append(changed)
        changed = copy.deepcopy(self.report)
        del changed["empty"]
        mutations.append(changed)
        for changed in mutations:
            with self.subTest(mutation=repr(changed)), self.assertRaises(ValueError):
                self.compare(
                    lambda _p: copy.deepcopy(self.report), lambda _p, changed=changed: changed
                )

    def test_equal_reports_and_input_copy_ownership(self):
        seen = []

        def analyzer(problem):
            seen.append(problem)
            return copy.deepcopy(self.report)

        self.assertEqual(self.compare(analyzer, analyzer), self.report)
        self.assertEqual(seen, [self.protocol, self.protocol])
        self.assertIsNot(seen[0], seen[1])
        self.assertIsNot(seen[0]["public"], seen[1]["public"])

    def test_mutating_either_engine_input_refused(self):
        def corrupt(problem):
            problem["public"].append("changed")
            return copy.deepcopy(self.report)

        def corrupt_type(problem):
            problem["ratio"] = Fraction(problem["ratio"])
            return copy.deepcopy(self.report)

        for corruption in (corrupt, corrupt_type):
            for left, right in (
                (corruption, lambda _p: copy.deepcopy(self.report)),
                (lambda _p: copy.deepcopy(self.report), corruption),
            ):
                with (
                    self.subTest(corruption=corruption.__name__, primary=left is corruption),
                    self.assertRaises(ValueError),
                ):
                    self.compare(left, right)

    def test_changed_freeze_after_route_refused(self):
        engine = SimpleNamespace(analyze=lambda _p: copy.deepcopy(self.report))
        changed = copy.deepcopy(self.freeze)
        changed["extra"] = "changed"
        with (
            mock.patch.object(self.study, "_frozen", side_effect=[self.freeze, changed]),
            mock.patch.object(self.study, "load_protocol", return_value=self.protocol),
            mock.patch.object(self.study, "_load_engine", return_value=engine),
            self.assertRaises(ValueError),
        ):
            self.study.compare_routes()

    def test_hashed_source_loader_ignores_import_caches_and_checks_bytes(self):
        with tempfile.TemporaryDirectory(prefix="det8-qr05bk-loader-") as temporary:
            root = Path(temporary)
            source = root / "quantum.py"
            source.write_bytes(
                b"def analyze(protocol):\n    return {'public': protocol['public']}\n"
            )
            identity = {
                "bytes": source.stat().st_size,
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
            poisoned = SimpleNamespace(analyze=lambda _p: "cached hidden answer")
            with (
                mock.patch.object(self.study, "ROOT", root),
                mock.patch.dict(sys.modules, {"quantum": poisoned}),
            ):
                first = self.study._load_engine("quantum", identity)
                second = self.study._load_engine("quantum", identity)
                self.assertIsNot(first, second)
                self.assertEqual(first.analyze({"public": "supplied"}), {"public": "supplied"})
                self.assertIs(sys.modules["quantum"], poisoned)
                source.write_bytes(source.read_bytes() + b"\n")
                with self.assertRaises(ValueError):
                    self.study._load_engine("quantum", identity)
                with self.assertRaises(ValueError):
                    self.study._load_engine("old_executor", identity)


def set_path(value, path, replacement):
    current = value
    for component in path[:-1]:
        current = current[component]
    current[path[-1]] = replacement


def get_path(value, path):
    for component in path:
        value = value[component]
    return value


def scalar_changes(original):
    leaves = []

    def walk(value, path=()):
        if type(value) is dict:
            for key, child in value.items():
                walk(child, (*path, key))
        elif type(value) is list:
            if value:
                walk(value[0], (*path, 0))
        else:
            leaves.append((path, value))

    walk(original)
    for path, value in leaves:
        if type(value) is str:
            try:
                replacement = str(Fraction(value) + 1)
            except ValueError:
                replacement = value + "-changed"
        elif type(value) is int:
            replacement = value + 1
        else:
            replacement = "changed"
        changed = copy.deepcopy(original)
        set_path(changed, path, replacement)
        yield path, changed


def analysis_mutations(original):
    """Representative field-complete changes plus late and typed algebraic changes."""
    yield from (("scalar " + repr(path), changed) for path, changed in scalar_changes(original))
    certificate = ("mathematics", "certificate")
    late = ("mathematics", "resolution", "budgets", -1)
    paths = [
        (*certificate, "raw_eliminant", -1),
        (*certificate, "defining_polynomial", -1),
        (*certificate, "roots", -1, "interval", -1),
        (*certificate, "u_image", "denominator", -1),
        (*certificate, "beta_image", "numerator", -1),
        (*certificate, "beta_interval", -1),
        (*late, "positions", -1, "data_theta", -1),
        (
            "mathematics",
            "bj_model",
            "refinement",
            -1,
            "constraints",
            "patches",
            -1,
            "coefficients",
            -1,
            -1,
            -1,
        ),
        (
            "mathematics",
            "bj_model",
            "bi_model",
            "cases",
            -1,
            "law_family",
            "rows",
            -1,
            "state_diagonal",
            -1,
            -1,
        ),
    ]
    for path in paths:
        changed = copy.deepcopy(original)
        set_path(changed, path, str(Fraction(get_path(changed, path)) + 1))
        yield "late " + repr(path), changed
    for path in [
        (*certificate, "roots"),
        (*certificate, "u_image", "numerator"),
        ("mathematics", "resolution", "budgets"),
        (*late, "positions"),
        (*late, "menus"),
        (*late, "menus", 0, "hypotheses"),
        ("mathematics", "bj_model", "refinement", -1, "constraints", "witnesses"),
    ]:
        changed = copy.deepcopy(original)
        set_path(changed, path, get_path(changed, path)[:-1])
        yield "truncated " + repr(path), changed
    for path, replacement in [
        ((*certificate, "convexity", "hessian_determinant_numerator"), "3"),
        (("mathematics", "resolution", "summary", "remaining_global_negative_gap"), 1),
        (("mathematics", "resolution", "summary", "resolved_menus"), True),
        (("mathematics", "resolution", "positive_theta", 0, 1, "scale"), "0"),
        (
            ("mathematics", "resolution", "positive_theta", 0, 1),
            original["mathematics"]["certificate"]["beta_interval"][0],
        ),
        (("mathematics", "resolution", "positive_theta", 0, 0), 0),
        ((*certificate, "status"), "stationary_only"),
        (
            (
                "mathematics",
                "bj_model",
                "bi_model",
                "cases",
                0,
                "law_family",
                "rows",
                -1,
                "outcomes",
                0,
            ),
            True,
        ),
    ]:
        changed = copy.deepcopy(original)
        set_path(changed, path, replacement)
        yield "typed " + repr(path), changed
    for index, budget in enumerate(original["mathematics"]["resolution"]["budgets"]):
        for menu_index, menu in enumerate(budget["menus"]):
            if menu["target_set"]["gaps"]:
                path = (
                    "mathematics",
                    "resolution",
                    "budgets",
                    index,
                    "menus",
                    menu_index,
                    "target_set",
                    "intervals",
                )
                changed = copy.deepcopy(original)
                set_path(changed, path, [menu["target_set"]["hull"]])
                yield "improper convexification " + repr(path), changed
                break
        path = ("mathematics", "resolution", "budgets", index, "menus", 0, "target_set", "hull")
        changed = copy.deepcopy(original)
        set_path(changed, path, None if get_path(changed, path) is not None else ["0", "0"])
        yield "null hull " + repr(path), changed
    for path, key in [
        (certificate, "decimal_beta"),
        (late, "endpoint_checks"),
        (("mathematics", "resolution"), "negative_boundary"),
    ]:
        changed = copy.deepcopy(original)
        get_path(changed, path)[key] = "undeclared"
        yield "undeclared " + key, changed
    for key in original:
        changed = copy.deepcopy(original)
        del changed[key]
        yield "missing " + key, changed


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_module("study")
        self.directory = tempfile.TemporaryDirectory(prefix="det8-qr05bk-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.freeze = self.root / "freeze.json"
        self.capture_path = self.root / "capture.json"
        self.sources = {"synthetic/source.py": {"bytes": 1, "sha256": "a" * 64}}
        self.small = {
            "mathematics": {"exact": "1/3", "count": 1},
            "bj_restriction": {"branches": 1},
        }
        source_mock = mock.patch.object(
            self.study, "source_identities", side_effect=lambda: copy.deepcopy(self.sources)
        )
        source_mock.start()
        self.addCleanup(source_mock.stop)
        self.study.freeze_source(self.freeze)

    def write_json(self, path, value):
        path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")

    def capture_small(self):
        with mock.patch.object(self.study, "analysis", return_value=copy.deepcopy(self.small)):
            return self.study.capture(self.capture_path, self.freeze)

    def replay_small(self, path=None):
        with mock.patch.object(self.study, "analysis", return_value=copy.deepcopy(self.small)):
            return self.study.replay(path or self.capture_path, self.freeze)

    def test_create_replay_and_readonly_identity(self):
        evidence = self.capture_small()
        exact_keys(self, evidence, "schema freeze sources analysis")
        self.assertEqual(evidence["schema"], "QR-05BK-evidence-v1")
        self.assertEqual(evidence["sources"], self.sources)
        self.assertEqual(evidence["analysis"], self.small)
        self.assertEqual(evidence["freeze"], self.study.identity(self.freeze))
        before = self.capture_path.read_bytes(), self.freeze.read_bytes()
        self.assertEqual(self.replay_small(), evidence)
        self.assertEqual((self.capture_path.read_bytes(), self.freeze.read_bytes()), before)

    def test_create_only_existing_paths_and_symlinks(self):
        self.capture_small()
        saved = self.capture_path.read_bytes(), self.freeze.read_bytes()
        for operation, path in (
            (self.study.capture, self.capture_path),
            (self.study.freeze_source, self.freeze),
        ):
            with (
                self.subTest(operation=operation.__name__),
                self.assertRaises((ValueError, FileExistsError)),
            ):
                operation(path)
        target = self.root / "absent.json"
        link = self.root / "dangling.json"
        link.symlink_to(target)
        with mock.patch.object(self.study, "analysis", return_value=self.small):
            with self.assertRaises((ValueError, FileExistsError)):
                self.study.capture(link, self.freeze)
            with self.assertRaises((ValueError, FileExistsError)):
                self.study.freeze_source(link)
        self.assertFalse(target.exists())
        self.assertTrue(link.is_symlink())
        self.assertEqual((self.capture_path.read_bytes(), self.freeze.read_bytes()), saved)

    def test_malformed_json_duplicates_nonfinite_and_size_limits(self):
        invalid = [
            b"",
            b"{",
            b"\xff",
            b'{"x":1,"x":2}',
            b'{"nested":{"x":1,"x":2}}',
            b"1.0",
            b"1e0",
            b"NaN",
            b"Infinity",
            b"-Infinity",
        ]
        for index, data in enumerate(invalid):
            path = self.root / ("bad-" + str(index) + ".json")
            path.write_bytes(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.study.read_json(path)
            self.assertEqual(path.read_bytes(), data)
        with self.assertRaises(ValueError):
            self.study.read_json(self.root / "missing.json")
        with self.assertRaises(ValueError):
            self.study.read_json(self.root)
        link = self.root / "read-link.json"
        link.symlink_to(self.freeze)
        with self.assertRaises(ValueError):
            self.study.read_json(link)
        path = self.root / "sized.json"
        path.write_bytes(b"[0]")
        with mock.patch.object(self.study, "MAX_JSON_BYTES", 3):
            self.assertEqual(self.study.read_json(path), [0])
        with mock.patch.object(self.study, "MAX_JSON_BYTES", 2), self.assertRaises(ValueError):
            self.study.read_json(path)

    def test_freeze_schema_runtime_and_source_mutations(self):
        base = self.study.read_json(self.freeze)
        candidates = [None, [], {}, {**base, "extra": 0}, {**base, "schema": "wrong"}]
        for key, replacement in (
            ("python", ""),
            ("python", 3),
            ("implementation", None),
            ("optimized", True),
            ("optimized", -1),
            ("optimized", 3),
        ):
            changed = copy.deepcopy(base)
            changed["runtime_at_source_freeze"][key] = replacement
            candidates.append(changed)
        for key in ("schema", "sources", "runtime_at_source_freeze"):
            changed = copy.deepcopy(base)
            del changed[key]
            candidates.append(changed)
        changed = copy.deepcopy(base)
        changed["sources"]["synthetic/source.py"]["bytes"] = True
        candidates.append(changed)
        changed = copy.deepcopy(base)
        changed["sources"]["synthetic/source.py"]["sha256"] = "b" * 64
        candidates.append(changed)
        for index, changed in enumerate(candidates):
            path = self.root / ("bad-freeze-" + str(index) + ".json")
            self.write_json(path, changed)
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.study.capture(self.root / ("unused-" + str(index)), path)

    def test_evidence_header_and_complete_identity_mutations(self):
        base = self.capture_small()
        changes = [None, [], {}, {**base, "schema": "wrong"}, {**base, "extra": 0}]
        for key in base:
            changed = copy.deepcopy(base)
            del changed[key]
            changes.append(changed)
        for path, replacement in (
            (("freeze", "bytes"), True),
            (("freeze", "sha256"), "b" * 64),
            (("sources", "synthetic/source.py", "bytes"), True),
            (("sources", "synthetic/source.py", "sha256"), "b" * 64),
            (("analysis", "mathematics", "exact"), "2/6"),
            (("analysis", "mathematics", "count"), True),
            (("analysis", "bj_restriction", "branches"), True),
        ):
            changed = copy.deepcopy(base)
            set_path(changed, path, replacement)
            changes.append(changed)
        for index, changed in enumerate(changes):
            path = self.root / ("bad-capture-" + str(index) + ".json")
            self.write_json(path, changed)
            before = path.read_bytes()
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.replay_small(path)
            self.assertEqual(path.read_bytes(), before)

    def test_changed_sources_before_and_during_creation_refused(self):
        self.sources["synthetic/source.py"]["bytes"] = 2
        with self.assertRaises(ValueError):
            self.capture_small()
        self.assertFalse(self.capture_path.exists())
        self.sources["synthetic/source.py"]["bytes"] = 1

        def change(_freeze):
            self.sources["synthetic/source.py"]["bytes"] = 2
            return copy.deepcopy(self.small)

        with (
            mock.patch.object(self.study, "analysis", side_effect=change),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze)
        self.assertFalse(self.capture_path.exists())

    def test_source_changes_during_freeze_refused(self):
        changed = copy.deepcopy(self.sources)
        changed["synthetic/source.py"]["bytes"] += 1
        path = self.root / "new-freeze.json"
        with (
            mock.patch.object(self.study, "source_identities", side_effect=[self.sources, changed]),
            self.assertRaises(ValueError),
        ):
            self.study.freeze_source(path)
        self.assertFalse(path.exists())

    def test_freeze_byte_changes_during_capture_and_replay_refused(self):
        before = self.freeze.read_bytes()

        def change(_freeze):
            self.freeze.write_bytes(before + b"\n")
            return copy.deepcopy(self.small)

        with (
            mock.patch.object(self.study, "analysis", side_effect=change),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze)
        self.assertFalse(self.capture_path.exists())
        self.freeze.write_bytes(before)
        self.capture_small()
        evidence_before = self.capture_path.read_bytes()
        with (
            mock.patch.object(self.study, "analysis", side_effect=change),
            self.assertRaises(ValueError),
        ):
            self.study.replay(self.capture_path, self.freeze)
        self.assertEqual(self.capture_path.read_bytes(), evidence_before)

    def test_failed_analysis_does_not_publish_or_replace_evidence(self):
        with (
            mock.patch.object(
                self.study, "analysis", side_effect=ValueError("declared failed comparison")
            ),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze)
        self.assertFalse(self.capture_path.exists())
        self.capture_small()
        before = self.capture_path.read_bytes()
        with (
            mock.patch.object(
                self.study, "analysis", side_effect=ValueError("declared failed replay")
            ),
            self.assertRaises(ValueError),
        ):
            self.study.replay(self.capture_path, self.freeze)
        self.assertEqual(self.capture_path.read_bytes(), before)

    def test_changed_published_bytes_are_rejected_and_retained(self):
        original_create = self.study._create_json

        def corrupt(path, value):
            identity = original_create(path, value)
            path.write_bytes(path.read_bytes() + b"\n")
            return identity

        with (
            mock.patch.object(self.study, "analysis", return_value=self.small),
            mock.patch.object(self.study, "_create_json", side_effect=corrupt),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze)
        self.assertTrue(self.capture_path.is_file())
        before = self.capture_path.read_bytes()
        with self.assertRaises((ValueError, FileExistsError)):
            self.study.capture(self.capture_path, self.freeze)
        self.assertEqual(self.capture_path.read_bytes(), before)

    def test_artifact_byte_change_during_replay_refused(self):
        self.capture_small()
        before = self.capture_path.read_bytes()

        def corrupt(_freeze):
            self.capture_path.write_bytes(before + b"\n")
            return copy.deepcopy(self.small)

        with (
            mock.patch.object(self.study, "analysis", side_effect=corrupt),
            self.assertRaises(ValueError),
        ):
            self.study.replay(self.capture_path, self.freeze)
        self.assertEqual(self.capture_path.read_bytes(), before + b"\n")

    def test_output_byte_cap_precedes_creation(self):
        path = self.root / "capped.json"
        with mock.patch.object(self.study, "MAX_JSON_BYTES", 1), self.assertRaises(ValueError):
            self.study._create_json(path, {"larger": "value"})
        self.assertFalse(path.exists())

    def test_complete_report_and_restriction_non_noop_mutations(self):
        study, _protocol, report = evaluated()
        with mock.patch.object(study, "compare_routes", return_value=report):
            expected = study.analysis()
        with mock.patch.object(self.study, "analysis", return_value=expected):
            evidence = self.study.capture(self.capture_path, self.freeze)
            before = self.capture_path.read_bytes()
            original_parse = self.study._parse_json
            count = 0
            for name, changed in analysis_mutations(expected):
                with self.subTest(case=name):
                    self.assertNotEqual(
                        self.study.canonical(changed), self.study.canonical(expected)
                    )
                    bad = copy.deepcopy(evidence)
                    bad["analysis"] = changed

                    # Inject only this parsed artifact; freeze/source reads use
                    # the real parser. Keep large field corruptions in memory.
                    def parse(data, mutation=bad):
                        return mutation if data == before else original_parse(data)

                    with (
                        mock.patch.object(self.study, "_parse_json", side_effect=parse),
                        self.assertRaises(ValueError),
                    ):
                        self.study.replay(self.capture_path, self.freeze)
                    self.assertEqual(self.capture_path.read_bytes(), before)
                    count += 1
            self.assertGreater(count, 50)

    def test_encoding_rejects_unsupported_native_types(self):
        for value in (0.0, float("nan"), float("inf"), (), {1: "bad"}, {"set": {1}}, b"bytes"):
            with self.subTest(value=repr(value)), self.assertRaises(ValueError):
                self.study.encode(value)
        self.assertFalse(self.study.same({"integer": 1}, {"integer": True}))
        self.assertEqual(self.study.encode(Fraction(2, 6)), "1/3")


class HistoricalBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def receipt(self):
        return {
            "status": "matched",
            "positions": 6,
            "cases": 7,
            "budgets": 21,
            "hypothesis_intervals": 126,
            "menus": 105,
            "affine_patches": 112,
            "affine_coefficients": 1008,
            "affine_witnesses": 175,
            "exact_menus": 103,
        }

    def document(self):
        return {
            "analysis": {
                "mathematics": self.study.encode(self.report["bj_model"]),
                "bi_restriction": "not replayed",
            },
            "sources": "not replayed",
        }

    def restriction(self, document, current=None):
        data = json.dumps(document, sort_keys=True).encode()
        identities = dict(self.study.BJ_IDENTITIES)
        identities["results.json"] = hashlib.sha256(data).hexdigest()
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=data),
            mock.patch.object(self.study, "BJ_IDENTITIES", identities),
            mock.patch.object(
                self.study, "_load_engine", side_effect=AssertionError("historical executor")
            ),
        ):
            return self.study._bj_restriction(self.report if current is None else current)

    def test_complete_bj_baseline_only_not_old_lifecycle_or_new_certificate(self):
        document = self.document()
        self.assertEqual(self.restriction(document), self.receipt())
        changed = copy.deepcopy(document)
        changed["analysis"]["bi_restriction"] = None
        changed["sources"] = None
        self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
        self.assertEqual(self.restriction(changed), self.receipt())
        current = copy.deepcopy(self.report)
        current["certificate"] = None
        current["resolution"] = None
        self.assertFalse(self.study.raw_same(current, self.report))
        self.assertEqual(self.restriction(document, current), self.receipt())

    def test_selected_whole_baseline_late_coefficients_laws_and_types(self):
        document = self.document()
        for path, mutation in scalar_changes(document["analysis"]["mathematics"]):
            changed = copy.deepcopy(document)
            changed["analysis"]["mathematics"] = mutation
            self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)
        paths = [
            ("refinement", -1, "constraints", "patches", -1, "coefficients", -1, -1, -1),
            ("refinement", -1, "constraints", "witnesses", -1, "value", -1),
            ("refinement", -1, "budgets", -1, "positions", -1, "data_target", -1),
            ("bi_model", "cases", -1, "law_family", "rows", -1, "state_diagonal", -1, -1),
            (
                "bi_model",
                "cases",
                -1,
                "budgets",
                -1,
                "endpoint_checks",
                -1,
                "maximum_trace_residual",
            ),
        ]
        for path in paths:
            changed = copy.deepcopy(document)
            target = ("analysis", "mathematics", *path)
            set_path(changed, target, str(Fraction(get_path(changed, target)) + 1))
            self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)
        for path, replacement in [
            (("bj_model", "bi_model", "cases", 0, "law_family", "rows", -1, "outcomes", 0), True),
            (("bj_model", "bi_model", "cases", 0, "law_family", "rows", 0, "probability", 0), 0),
            (
                ("bj_model", "refinement", -1, "budgets", -1, "menus", -1, "target_set_status"),
                "changed",
            ),
        ]:
            changed = copy.deepcopy(self.report)
            set_path(changed, path, replacement)
            self.assertFalse(self.study.raw_same(changed, self.report))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(document, changed)
        for changed in [{"bj_model": self.report["bj_model"]}, {**self.report, "extra": None}]:
            with self.assertRaises(ValueError):
                self.restriction(document, changed)

    def test_history_hash_precedes_parse_and_real_full_bj_receipt(self):
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=b"{}"),
            mock.patch.object(
                self.study, "_parse_json", side_effect=AssertionError("unverified history")
            ),
            self.assertRaises(ValueError),
        ):
            self.study._bj_restriction(self.report)
        with mock.patch.object(self.study, "compare_routes", return_value=self.report):
            result = self.study.analysis()
        exact_keys(self, result, "mathematics bj_restriction")
        self.assertEqual(result["mathematics"], self.study.encode(self.report))
        self.assertEqual(result["bj_restriction"], self.receipt())


class SourceIdentityTests(unittest.TestCase):
    def test_exact_eleven_current_and_bj_source_identities(self):
        study = load_module("study")
        actual = study.source_identities()
        current = [
            HERE / name
            for name in (
                "README.md",
                "protocol.json",
                "quantum.py",
                "reference.py",
                "study.py",
                "test_qr05bk.py",
            )
        ]
        previous = [
            study.BJ_DIRECTORY / name
            for name in (
                "README.md",
                "RESULTS.md",
                "protocol.json",
                "source-freeze.json",
                "results.json",
            )
        ]
        self.assertEqual(len(actual), 11)
        self.assertEqual(set(actual), {str(p.relative_to(study.REPO)) for p in current + previous})
        for path in current + previous:
            data = path.read_bytes()
            self.assertEqual(
                actual[str(path.relative_to(study.REPO))],
                {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()},
            )
        self.assertEqual(study.read_json(study.FREEZE_PATH)["sources"], actual)
        self.assertEqual(
            hashlib.sha256((HERE / "protocol.json").read_bytes()).hexdigest(), PROTOCOL_SHA256
        )

    def snapshots(self, study, bk_data=None, bj_data=None):
        bk_path, bj_path = HERE / "protocol.json", study.BJ_DIRECTORY / "protocol.json"
        data = bk_path.read_bytes() if bk_data is None else bk_data
        model = bj_path.read_bytes() if bj_data is None else bj_data

        def read(path):
            if Path(path) == bk_path:
                return data
            if Path(path) == bj_path:
                return model
            raise AssertionError("unexpected protocol snapshot: " + str(path))

        return data, model, read

    def test_both_protocol_hashes_and_parses_use_same_snapshots(self):
        study = load_module("study")
        data, model, reader = self.snapshots(study)
        with (
            mock.patch.object(study, "_read_bounded", side_effect=reader) as read,
            mock.patch.object(study, "_bytes_identity", wraps=study._bytes_identity) as hashed,
            mock.patch.object(study, "_parse_json", wraps=study._parse_json) as parsed,
        ):
            self.assertEqual(study.load_protocol(), json.loads(data))
        self.assertEqual(read.call_count, 2)
        self.assertEqual(hashed.call_count, 2)
        self.assertEqual(parsed.call_count, 2)
        for index, blob in enumerate((data, model)):
            self.assertIs(hashed.call_args_list[index].args[0], blob)
            self.assertIs(parsed.call_args_list[index].args[0], blob)
        self.assertEqual(json.loads(data)["model"], json.loads(model))

    def test_each_protocol_hash_refuses_before_its_own_parse(self):
        study = load_module("study")
        _data, _model, reader = self.snapshots(study, bk_data=b"{}")
        with (
            mock.patch.object(study, "_read_bounded", side_effect=reader),
            mock.patch.object(
                study, "_parse_json", side_effect=AssertionError("unverified BK parse")
            ),
            self.assertRaisesRegex(ValueError, "protocol identity changed"),
        ):
            study.load_protocol()
        data, _model, reader = self.snapshots(study, bj_data=b"{}")
        original_parse = study._parse_json

        def parse(blob):
            if blob is not data:
                raise AssertionError("unverified BJ parse")
            return original_parse(blob)

        with (
            mock.patch.object(study, "_read_bounded", side_effect=reader),
            mock.patch.object(study, "_parse_json", side_effect=parse) as parsed,
            self.assertRaisesRegex(ValueError, "preceding BJ protocol identity changed"),
        ):
            study.load_protocol()
        self.assertEqual(parsed.call_count, 1)

    def test_authenticated_boundary_budgets_and_complete_nested_model_guards(self):
        study = load_module("study")
        protocol = json.loads((HERE / "protocol.json").read_bytes())
        mutations = [
            (("version",), True, "version differs"),
            (("study",), "QR-05BJ", "study differs"),
            (("base_commit",), "not-authoritative", "base commit differs"),
            (("boundary", "case_id"), "zero", "boundary contract differs"),
            (("boundary", "A", 0), "4", "boundary contract differs"),
            (("boundary", "isolation", "depth"), 25, "boundary contract differs"),
            (("boundary", "isolation", "max_nodes"), 4097, "boundary contract differs"),
            (("boundary", "isolation", "max_degree"), True, "boundary contract differs"),
            (
                ("boundary", "negative_rule"),
                "discard uncertain pieces",
                "boundary contract differs",
            ),
            (("model", "refinement", "leaves", -1, "id"), "changed", "complete BJ input differs"),
            (
                ("model", "model", "interval_budgets", 1, "radius"),
                "1/63",
                "complete BJ input differs",
            ),
        ]
        for path, value, message in mutations:
            changed = copy.deepcopy(protocol)
            set_path(changed, path, value)
            self.assertNotEqual(study.canonical(changed), study.canonical(protocol))
            data = json.dumps(changed).encode()
            _data, model, reader = self.snapshots(study, bk_data=data)
            identity_fn = study._bytes_identity

            def authenticate(blob, current=data, original=identity_fn):
                identity = original(blob)
                if blob is current:
                    identity["sha256"] = PROTOCOL_SHA256
                return identity

            with (
                self.subTest(path=path),
                mock.patch.object(study, "_read_bounded", side_effect=reader),
                mock.patch.object(study, "_bytes_identity", side_effect=authenticate),
                self.assertRaisesRegex(ValueError, message),
            ):
                study.load_protocol()
            self.assertEqual(
                hashlib.sha256(model).hexdigest(), study.BJ_IDENTITIES["protocol.json"]
            )


if __name__ == "__main__":
    unittest.main()
