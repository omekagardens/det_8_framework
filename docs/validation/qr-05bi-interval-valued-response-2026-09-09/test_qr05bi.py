"""Source-bound BI tests: independent Boole/cofactor/scalar oracle.

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
import sys
import tempfile
import unittest
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA256 = "8da402d79a93108711929ede1af63e99be2e07f8097e5f33921edcafa6134127"


def load_module(name):
    spec = importlib.util.spec_from_file_location("qr05bi_test_" + name, HERE / (name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("BI source could not be loaded")
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


def expected(protocol):
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


class ProtocolTests(unittest.TestCase):
    def test_protocol_and_prescribed_nonadaptive_budgets(self):
        data = (HERE / "protocol.json").read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), PROTOCOL_SHA256)
        p = json.loads(data)
        self.assertEqual(p["study"], "QR-05BI")
        self.assertEqual(p["model"]["study"], "QR-05BH")
        self.assertEqual(p["model"]["model"]["study"], "QR-05BG")
        self.assertEqual(
            p["interval_budgets"],
            [
                {"id": "point", "radius": "0"},
                {"id": "narrow", "radius": "1/64"},
                {"id": "wide", "radius": "1/8"},
            ],
        )
        certificate = p["model"]["certificate"]
        self.assertEqual(certificate["degree"], [2, 2])
        bounds = [
            [[Fraction(x) for x in axis] for axis in leaf["bounds"]]
            for leaf in certificate["leaves"]
        ]
        half = [[Fraction(0), Fraction(1, 2)], [Fraction(1, 2), Fraction(1)]]
        self.assertEqual(bounds, [list(pair) for pair in itertools.product(half, repeat=2)])
        self.assertEqual(
            certificate["witness_points"],
            [list(pair) for pair in itertools.product(["0", "1/2", "1"], repeat=2)],
        )

    def test_verified_boole_and_gram_moments(self):
        p = json.loads((HERE / "protocol.json").read_bytes())["model"]["model"]["third_oracle"]
        nodes, weights = boole_rule()
        self.assertEqual(nodes, tuple(map(Fraction, p["nodes"])))
        self.assertEqual(weights, tuple(map(Fraction, p["weights"])))
        for i, j in itertools.product(range(6), repeat=2):
            self.assertEqual(
                integrate(lambda u, v, i=i, j=j: u**i * v**j), Fraction(1, (i + 1) * (j + 1))
            )
        gram, inverse = bernstein_gram()
        self.assertEqual(multiply(gram, inverse), identity(3))
        self.assertEqual(multiply(inverse, gram), identity(3))


class CompleteMathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def test_complete_independent_native_report(self):
        exact_tree(self, self.report, expected(self.protocol))
        self.assertEqual(set(self.report), {"geometry", "positions", "cases"})

    def test_geometry_inverse_orientation_and_target_integration(self):
        q = self.report["geometry"]["coefficient_integrals"]
        self.assertEqual(q, [functional(row) for row in identity(5)])
        self.assertEqual(self.report["geometry"]["volume"], Fraction(1, 2))
        self.assertEqual(self.report["geometry"]["sigma"], Fraction(1, 16))
        for p in self.report["positions"]:
            a, d = p["evaluation_matrix"], p["coefficient_decoder"]
            self.assertEqual(row_rank(a), 5)
            self.assertEqual(multiply(d, a), p["left_inverse"])
            self.assertEqual(multiply(a, d), p["right_inverse"])
            self.assertEqual(p["left_inverse"], identity(5))
            self.assertEqual(p["right_inverse"], identity(5))
            self.assertEqual(multiply([p["full_weights"]], a), [q])
            self.assertEqual(p["full_residual"], [Fraction(0)] * 5)

    def test_affine_nets_at_extra_points_and_constraint_preimages(self):
        for case in self.report["cases"]:
            c = case["constraints"]
            self.assertEqual([p["id"] for p in c["patches"]], ["root", "ll", "lh", "hl", "hh"])
            for patch in c["patches"]:
                (u0, u1), (v0, v1) = patch["bounds"]
                for s, t in itertools.product([Fraction(1, 3), Fraction(2, 3)], repeat=2):
                    for theta in [Fraction(-2), Fraction(0), Fraction(3)]:
                        represented = sum(
                            (
                                at(patch["coefficients"][i][j], theta)
                                * bernstein(i, s)
                                * bernstein(j, t)
                                for i in range(3)
                                for j in range(3)
                            ),
                            Fraction(0),
                        )
                        self.assertEqual(
                            represented,
                            dot(
                                [*case["corners"], theta],
                                basis(u0 + (u1 - u0) * s, v0 + (v1 - v0) * t),
                            ),
                        )
                for i, j in itertools.product(range(3), repeat=2):
                    pair = patch["coefficients"][i][j]
                    self.assertEqual(patch["allowed"][i][j], arrangement([pair]))
                    self.assertEqual(patch["reconstruction_residual"][i][j], [Fraction(0)] * 2)
                self.assertEqual(
                    patch["theta_interval"],
                    arrangement([pair for row in patch["coefficients"] for pair in row]),
                )
            for witness in c["witnesses"]:
                point = witness["position"]
                self.assertEqual(
                    witness["value"], [dot(case["corners"], basis(*point)[:4]), basis(*point)[4]]
                )
                self.assertEqual(witness["allowed"], arrangement([witness["value"]]))

    def test_global_routes_root_is_diagnostic_and_old_union_not_intersection(self):
        saw_root_failure = False
        for case in self.report["cases"]:
            c = case["constraints"]
            leaf_pairs = [
                pair for patch in c["patches"][1:] for row in patch["coefficients"] for pair in row
            ]
            self.assertEqual(c["bernstein_theta"], arrangement(leaf_pairs))
            self.assertEqual(c["witness_theta"], arrangement([w["value"] for w in c["witnesses"]]))
            self.assertEqual(c["inner_theta"], merge_union([c["old_theta"], c["bernstein_theta"]]))
            self.assertTrue(
                union_subset([[Fraction(0), Fraction(0)]], merge_union([c["old_theta"]]))
            )
            self.assertTrue(
                union_subset([[Fraction(0), Fraction(0)]], merge_union([c["bernstein_theta"]]))
            )
            self.assertEqual(len(c["inner_theta"]), 1)
            self.assertTrue(union_subset(merge_union([c["old_theta"]]), c["inner_theta"]))
            self.assertTrue(union_subset(c["inner_theta"], c["outer_theta"]))
            for point in case["budgets"][0]["positions"]:
                theta = point["data_theta"]
                if point["inner_theta"] and not intersect_union(
                    [theta], merge_union([c["patches"][0]["theta_interval"]])
                ):
                    saw_root_failure = True
        self.assertTrue(saw_root_failure)

    def test_data_endpoints_direct_reconstruction_and_finite_route_payloads(self):
        for case, declared in zip(
            self.report["cases"], self.protocol["model"]["model"]["cases"], strict=True
        ):
            center = Fraction(declared["population_means"][4])
            for budget, config in zip(
                case["budgets"], self.protocol["interval_budgets"], strict=True
            ):
                radius = Fraction(config["radius"])
                response = [max(Fraction(-1), center - radius), min(Fraction(1), center + radius)]
                self.assertEqual(budget["response_interval"], response)
                for row, p in zip(budget["positions"], self.report["positions"], strict=True):
                    r, s = row["response_intercept"], row["response_slope"]
                    self.assertGreater(s, 0)
                    self.assertEqual(r, dot(case["corners"], p["basis"][:4]))
                    self.assertEqual(s, p["basis"][4])
                    self.assertEqual([r + s * t for t in row["data_theta"]], response)
                    self.assertEqual(row["reconstruction_residual"], [[Fraction(0)] * 5] * 2)
                    for theta, target in zip(row["data_theta"], row["data_target"], strict=True):
                        self.assertEqual(functional([*case["corners"], theta]), target)
                    for route in ("old", "bernstein", "inner", "outer"):
                        theta, targets = row[route + "_theta"], row[route + "_targets"]
                        self.assertTrue(
                            all(
                                type(x) is Fraction
                                for interval in theta + targets
                                for x in interval
                            )
                        )
                        self.assertEqual(
                            targets,
                            project_union(theta, case["target_offset"], case["target_slope"]),
                        )
                    self.assertTrue(union_subset(row["old_theta"], row["inner_theta"]))
                    self.assertTrue(union_subset(row["inner_theta"], row["outer_theta"]))
                    self.assertEqual(
                        row["inner_theta"], merge_union(row["old_theta"] + row["bernstein_theta"])
                    )
                    self.assertEqual(
                        row["point_classification"],
                        None
                        if budget["id"] != "point"
                        else "certified"
                        if row["inner_theta"]
                        else "refuted"
                        if not row["outer_theta"]
                        else "unresolved",
                    )

    def test_budget_narrowing_and_exact_menu_filtering(self):
        declared_menus = self.protocol["model"]["model"]["menus"]
        for case in self.report["cases"]:
            for lower, upper in zip(case["budgets"][:-1], case["budgets"][1:], strict=True):
                self.assertTrue(
                    union_subset([lower["response_interval"]], [upper["response_interval"]])
                )
                for a, b in zip(lower["positions"], upper["positions"], strict=True):
                    for name in ("data_theta", "data_target"):
                        self.assertTrue(union_subset([a[name]], [b[name]]))
                    for name in (
                        "old_theta",
                        "bernstein_theta",
                        "inner_theta",
                        "outer_theta",
                        "old_targets",
                        "bernstein_targets",
                        "inner_targets",
                        "outer_targets",
                    ):
                        self.assertTrue(union_subset(a[name], b[name]))
                for a, b in zip(lower["menus"], upper["menus"], strict=True):
                    for route in ("old", "inner", "outer"):
                        self.assertTrue(
                            union_subset(
                                a["target_sets"][route]["intervals"],
                                b["target_sets"][route]["intervals"],
                            )
                        )
            for budget in case["budgets"]:
                self.assertEqual(
                    budget["menus"], expected_menus(declared_menus, budget["positions"])
                )
                all_menu = budget["menus"][0]
                for menu in budget["menus"]:
                    for route in ("old", "inner", "outer"):
                        self.assertEqual(
                            menu[route],
                            [
                                entry
                                for entry in all_menu[route]
                                if entry["position_id"] in menu["position_ids"]
                            ],
                        )
                        target = menu["target_sets"][route]
                        self.assertEqual(
                            target,
                            summary(
                                [interval for entry in menu[route] for interval in entry["targets"]]
                            ),
                        )
                        for (lo, hi), probe in zip(
                            target["gaps"], target["gap_probes"], strict=True
                        ):
                            self.assertLess(lo, probe)
                            self.assertLess(probe, hi)
                            self.assertFalse(intersect_union([[probe, probe]], target["intervals"]))

    def test_complete_coupled_law_family_and_endpoint_checks(self):
        for case in self.report["cases"]:
            family = case["law_family"]
            self.assertEqual(len(family["rows"]), 32)
            for row, labels in zip(
                family["rows"], itertools.product((-1, 1), repeat=5), strict=True
            ):
                self.assertEqual(row["outcomes"], list(labels))
                self.assertEqual(len(row["state_diagonal"]), 32)
            for mean in [
                Fraction(-1),
                Fraction(-1, 3),
                case["center_mean"],
                Fraction(2, 5),
                Fraction(1),
            ]:
                self.assertEqual(evaluate_law(family, mean), law([*case["corners"], mean]))
            self.assertEqual(sum((row["probability"][0] for row in family["rows"]), Fraction(0)), 1)
            self.assertEqual(sum((row["probability"][1] for row in family["rows"]), Fraction(0)), 0)
            for budget in case["budgets"]:
                for mean, check in zip(
                    budget["response_interval"], budget["endpoint_checks"], strict=True
                ):
                    self.assertEqual(check, endpoint_check(family, mean))
                    self.assertEqual(check["probability_sum"], 1)
                    self.assertEqual(check["averaged_trace"], 1)
                    self.assertEqual(check["maximum_trace_residual"], 0)
                    self.assertGreaterEqual(check["minimum_probability"], 0)
                    self.assertGreaterEqual(check["minimum_state_entry"], 0)

    def test_affine_laws_are_not_midpoint_or_independent_probability_boxes(self):
        family = self.report["cases"][0]["law_family"]
        minus, plus = evaluate_law(family, Fraction(-1)), evaluate_law(family, Fraction(1))
        midpoint = evaluate_law(family, Fraction(0))
        self.assertNotEqual(minus, plus)
        self.assertNotEqual(midpoint, plus)
        independent_upper = sum(
            (
                max(a["probability"], b["probability"])
                for a, b in zip(minus["rows"], plus["rows"], strict=True)
            ),
            Fraction(0),
        )
        self.assertGreater(independent_upper, 1)
        self.assertTrue(
            any(pair[1] < 0 for row in family["rows"] for pair in row["state_diagonal"])
        )
        mean = Fraction(1, 3)
        blend = [(1 - mean) / 2, (1 + mean) / 2]
        actual = evaluate_law(family, mean)
        for row, a, b in zip(actual["rows"], minus["rows"], plus["rows"], strict=True):
            self.assertEqual(
                row["probability"], blend[0] * a["probability"] + blend[1] * b["probability"]
            )
            self.assertEqual(
                row["state_diagonal"],
                [
                    blend[0] * x + blend[1] * y
                    for x, y in zip(a["state_diagonal"], b["state_diagonal"], strict=True)
                ],
            )

    def test_compact_literal_report_counts(self):
        cases = self.report["cases"]
        self.assertEqual(len(self.report["positions"]), 6)
        self.assertEqual(len(cases), 7)
        patches = [p for c in cases for p in c["constraints"]["patches"]]
        self.assertEqual(len(patches), 35)
        self.assertEqual(sum(len(row) for p in patches for row in p["coefficients"]), 315)
        self.assertEqual(
            sum(len(pair) for p in patches for row in p["coefficients"] for pair in row), 630
        )
        self.assertEqual(
            sum(len(pair) for p in patches for row in p["reconstruction_residual"] for pair in row),
            630,
        )
        self.assertEqual(sum(len(c["constraints"]["witnesses"]) for c in cases), 63)
        self.assertEqual(sum(len(c["law_family"]["rows"]) for c in cases), 224)
        self.assertEqual(
            sum(len(row["state_diagonal"]) for c in cases for row in c["law_family"]["rows"]), 7168
        )
        self.assertEqual(sum(len(c["law_family"]["averaged_state"]) for c in cases), 224)
        budgets = [b for c in cases for b in c["budgets"]]
        self.assertEqual(len(budgets), 21)
        self.assertEqual(sum(len(b["endpoint_checks"]) for b in budgets), 42)
        self.assertEqual(sum(len(b["positions"]) for b in budgets), 126)
        self.assertEqual(sum(len(b["menus"]) for b in budgets), 105)


class ScalarSemanticTests(unittest.TestCase):
    def test_constraint_arrangements_zero_slopes_endpoints_empty_and_unbounded(self):
        F = Fraction
        hands = [
            ([], [None, None]),
            ([[F(1), F(0)]], [None, None]),
            ([[F(2), F(0)]], None),
            ([[F(0), F(1)]], [F(-1), F(1)]),
            ([[F(1), F(2)]], [F(-1), F(0)]),
            ([[F(1), F(-2)]], [F(0), F(1)]),
            ([[F(0), F(1)], [F(2), F(1)]], [F(-1), F(-1)]),
            ([[F(0), F(1)], [F(3), F(1)]], None),
            ([[F(1), F(0)], [F(0), F(1, 10**9)]], [F(-(10**9)), F(10**9)]),
        ]
        for pairs, wanted in hands:
            self.assertEqual(arrangement(pairs), wanted)
            for engine in semantic_engines():
                with self.subTest(pairs=pairs, engine=engine.__name__):
                    saved = copy.deepcopy(pairs)
                    self.assertEqual(engine._solve_constraints(pairs), wanted)
                    self.assertEqual(pairs, saved)
        for a, b, c, d in itertools.product([F(-1), F(0), F(1)], repeat=4):
            pairs = [[a, b], [c, d]]
            for engine in semantic_engines():
                self.assertEqual(engine._solve_constraints(pairs), arrangement(pairs))

    def test_union_touching_overlap_disjoint_singleton_empty_and_infinite(self):
        F = Fraction
        hands = [
            ([], []),
            ([None], []),
            ([[None, None]], [[None, None]]),
            ([[F(2), F(3)], [F(0), F(1)]], [[F(0), F(1)], [F(2), F(3)]]),
            ([[F(0), F(1)], [F(1), F(2)], [F(2), F(2)]], [[F(0), F(2)]]),
            ([[F(1), F(3)], [F(0), F(2)], [F(0), F(0)]], [[F(0), F(3)]]),
            ([[None, F(0)], [F(0), None]], [[None, None]]),
            ([[None, F(-1)], [F(1), None]], [[None, F(-1)], [F(1), None]]),
        ]
        for values, wanted in hands:
            self.assertEqual(merge_union(values), wanted)
            for engine in semantic_engines():
                self.assertEqual(engine._merge_intervals(copy.deepcopy(values)), wanted)
        sources = [
            [],
            [[F(0), F(0)]],
            [[F(-2), F(-1)], [F(1), F(3)]],
            [[None, F(0)]],
            [[F(0), None]],
            [[None, None]],
        ]
        for a, b in itertools.product(sources, repeat=2):
            for engine in semantic_engines():
                self.assertEqual(
                    engine._intersect_unions(copy.deepcopy(a), copy.deepcopy(b)),
                    intersect_union(a, b),
                )
        for values in sources:
            for offset, slope in itertools.product([F(-2), F(0), F(3)], [-1, 0, 1]):
                for engine in semantic_engines():
                    self.assertEqual(
                        engine._project_union(copy.deepcopy(values), offset, F(slope)),
                        project_union(values, offset, F(slope)),
                    )

    def test_projection_reverses_sorts_coalesces_and_does_not_convexify(self):
        F = Fraction
        original = [[F(0), F(1)], [F(3), F(4)]]
        self.assertEqual(project_union(original, F(2), F(-2)), [[F(-6), F(-4)], [F(0), F(2)]])
        self.assertEqual(project_union(original, F(7), F(0)), [[F(7), F(7)]])
        self.assertEqual(project_union([], F(7), F(0)), [])
        data = summary(original)
        self.assertEqual(
            data,
            {
                "intervals": original,
                "hull": [F(0), F(4)],
                "gaps": [[F(1), F(3)]],
                "gap_probes": [F(2)],
            },
        )
        self.assertFalse(intersect_union([[F(2), F(2)]], original))

    def test_menu_existence_identification_ambiguity_and_separate_exactness(self):
        F = Fraction

        def position(name, old, inner, outer):
            shift = F(0)
            return {
                "position_id": name,
                "old_theta": old,
                "inner_theta": inner,
                "outer_theta": outer,
                "old_targets": project_union(old, shift, F(1)),
                "inner_targets": project_union(inner, shift, F(1)),
                "outer_targets": project_union(outer, shift, F(1)),
            }

        a, b, c = [[F(0), F(0)]], [[F(1), F(1)]], [[F(2), F(2)]]
        hands = [
            ([position("a", [], [], [])], ("infeasible", "infeasible", "exact", "exact")),
            ([position("a", [], [], a)], ("unresolved", "unresolved", "bounded", "bounded")),
            ([position("a", a, a, a)], ("feasible", "identified", "exact", "exact")),
            (
                [position("a", a, a, a), position("b", [], [], a)],
                ("feasible", "identified", "bounded", "exact"),
            ),
            (
                [position("a", a, a, a), position("b", [], [], b)],
                ("feasible", "unresolved", "bounded", "bounded"),
            ),
            (
                [position("a", a, a, a), position("b", b, b, b), position("c", [], [], c)],
                ("feasible", "ambiguous", "bounded", "bounded"),
            ),
            (
                [position("a", [], [], a), position("b", [], [], b)],
                ("unresolved", "unresolved", "bounded", "bounded"),
            ),
            (
                [position("a", a, a, a), position("b", a, a, a)],
                ("feasible", "identified", "exact", "exact"),
            ),
            (
                [position("a", [], [[F(0), F(1)]], [[F(0), F(2)]])],
                ("feasible", "ambiguous", "bounded", "bounded"),
            ),
        ]
        for positions, statuses in hands:
            menus = [
                {"id": "all", "position_ids": [p["position_id"] for p in positions]},
                {"id": "empty", "position_ids": []},
                {"id": "last", "position_ids": [positions[-1]["position_id"]]},
            ]
            wanted = expected_menus(menus, positions)
            self.assertEqual(
                tuple(
                    wanted[0][key]
                    for key in (
                        "existence_status",
                        "target_status",
                        "hypothesis_set_status",
                        "target_set_status",
                    )
                ),
                statuses,
            )
            for engine in semantic_engines():
                saved = copy.deepcopy(positions)
                self.assertEqual(engine._menus(copy.deepcopy(menus), positions), wanted)
                self.assertEqual(positions, saved)
                self.assertEqual(engine._menus([], []), [])


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
        with tempfile.TemporaryDirectory(prefix="det8-qr05bi-loader-") as temporary:
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
    yield from (("scalar " + repr(path), changed) for path, changed in scalar_changes(original))
    late = ("mathematics", "cases", -1)
    paths = [
        (*late, "constraints", "patches", -1, "coefficients", -1, -1, -1),
        (*late, "constraints", "patches", -1, "reconstruction_residual", -1, -1, -1),
        (*late, "constraints", "witnesses", -1, "value", -1),
        (*late, "law_family", "rows", -1, "probability", -1),
        (*late, "law_family", "rows", -1, "state_diagonal", -1, -1),
        (*late, "law_family", "averaged_state", -1, -1),
        (*late, "budgets", -1, "positions", -1, "data_theta", -1),
        (*late, "budgets", -1, "positions", -1, "data_target", -1),
        (*late, "budgets", -1, "positions", -1, "reconstruction_residual", -1, -1),
        (*late, "budgets", -1, "endpoint_checks", -1, "maximum_trace_residual"),
    ]
    for path in paths:
        changed = copy.deepcopy(original)
        set_path(changed, path, str(Fraction(get_path(changed, path)) + 1))
        yield "late " + repr(path), changed
    for path in [
        (*late, "constraints", "patches"),
        (*late, "constraints", "patches", -1, "coefficients"),
        (*late, "constraints", "witnesses"),
        (*late, "law_family", "rows"),
        (*late, "budgets"),
        (*late, "budgets", -1, "positions"),
        (*late, "budgets", -1, "menus"),
    ]:
        changed = copy.deepcopy(original)
        set_path(changed, path, get_path(changed, path)[:-1])
        yield "truncated " + repr(path), changed
    for i, case in enumerate(original["mathematics"]["cases"]):
        for j, budget in enumerate(case["budgets"]):
            menu = budget["menus"][0]
            for route in ("old", "inner", "outer"):
                path = (
                    "mathematics",
                    "cases",
                    i,
                    "budgets",
                    j,
                    "menus",
                    0,
                    "target_sets",
                    route,
                    "hull",
                )
                changed = copy.deepcopy(original)
                value = get_path(changed, path)
                set_path(changed, path, None if value is not None else ["0", "0"])
                yield "typed hull " + repr(path), changed
            path = ("mathematics", "cases", i, "budgets", j, "positions", 0, "point_classification")
            changed = copy.deepcopy(original)
            set_path(changed, path, None if budget["id"] == "point" else "certified")
            yield "point-only classification " + repr(path), changed
            for route in ("inner", "outer"):
                target = menu["target_sets"][route]
                if target["gaps"]:
                    path = (
                        "mathematics",
                        "cases",
                        i,
                        "budgets",
                        j,
                        "menus",
                        0,
                        "target_sets",
                        route,
                    )
                    changed = copy.deepcopy(original)
                    get_path(changed, path)["intervals"] = [target["hull"]]
                    yield "incorrect convex hull " + repr(path), changed
                    break
    for path in [
        ("mathematics", "cases", 0, "law_family", "rows", -1, "outcomes", 0),
        ("bh_restriction", "positions"),
    ]:
        changed = copy.deepcopy(original)
        set_path(changed, path, True)
        yield "native type " + repr(path), changed
    for value in (None, ["0", "0"], []):
        path = ("mathematics", "cases", 0, "constraints", "patches", 0, "allowed", 0, 0)
        if value != get_path(original, path):
            changed = copy.deepcopy(original)
            set_path(changed, path, value)
            yield "empty versus all-real " + repr(value), changed
    for key in original:
        changed = copy.deepcopy(original)
        del changed[key]
        yield "missing " + key, changed
    changed = copy.deepcopy(original)
    changed["unrecorded_budget"] = "adaptive"
    yield "extra budget", changed


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_module("study")
        self.directory = tempfile.TemporaryDirectory(prefix="det8-qr05bi-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.freeze = self.root / "freeze.json"
        self.capture_path = self.root / "capture.json"
        self.sources = {"synthetic/source.py": {"bytes": 1, "sha256": "a" * 64}}
        self.small = {
            "mathematics": {"exact": "1/3", "count": 1},
            "bh_restriction": {"branches": 1},
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
        self.assertEqual(evidence["schema"], "QR-05BI-evidence-v1")
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
            (("analysis", "bh_restriction", "branches"), True),
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
        # Historical bytes are boundary data, never inputs to expected().
        cls.previous = cls.study.read_json(cls.study.BH_DIRECTORY / "results.json")

    def restriction(self, document, current=None):
        data = json.dumps(document, sort_keys=True).encode()
        identities = dict(self.study.BH_IDENTITIES)
        identities["results.json"] = hashlib.sha256(data).hexdigest()
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=data),
            mock.patch.object(self.study, "BH_IDENTITIES", identities),
            mock.patch.object(
                self.study, "_load_engine", side_effect=AssertionError("historical executor")
            ),
        ):
            return self.study._bh_restriction(self.report if current is None else current)

    def receipt(self):
        return {
            "status": "matched",
            "positions": 6,
            "cases": 7,
            "candidates": 42,
            "menus": 35,
            "branches": 1568,
            "coefficients": 1890,
            "witnesses": 378,
        }

    def test_selected_zero_width_history_and_complete_laws(self):
        self.assertEqual(self.restriction(self.previous), self.receipt())
        previous = self.previous["analysis"]["mathematics"]
        self.assertEqual(
            self.study.encode(self.report["geometry"]), previous["bg_model"]["geometry"]
        )
        self.assertEqual(
            self.study.encode(self.report["positions"]), previous["bg_model"]["positions"]
        )
        for case, old, refined in zip(
            self.report["cases"], previous["bg_model"]["cases"], previous["refinement"], strict=True
        ):
            point = case["budgets"][0]
            self.assertEqual(point["id"], "point")
            current_law = self.study.encode(evaluate_law(case["law_family"], case["center_mean"]))
            self.assertEqual(current_law, old["law"])
            for row, old_candidate, old_refined in zip(
                point["positions"], old["candidates"], refined["candidates"], strict=True
            ):
                theta = row["data_theta"][0]
                self.assertEqual(row["data_theta"], [theta, theta])
                self.assertEqual(
                    self.study.encode([*case["corners"], theta]), old_candidate["coefficients"]
                )
                self.assertEqual(str(row["data_target"][0]), old_candidate["target"])
                self.assertEqual(row["point_classification"], old_refined["classification"])
                self.assertEqual(current_law, old_candidate["law"])
                for patch, old_patch in zip(
                    case["constraints"]["patches"],
                    [old_refined["root"], *old_refined["leaves"]],
                    strict=True,
                ):
                    self.assertEqual(
                        self.study.encode(
                            [[at(pair, theta) for pair in line] for line in patch["coefficients"]]
                        ),
                        old_patch["coefficients"],
                    )
                for witness, old_witness in zip(
                    case["constraints"]["witnesses"], old_refined["witnesses"], strict=True
                ):
                    self.assertEqual(str(at(witness["value"], theta)), old_witness["value"])
            for new, old_menu in zip(point["menus"], refined["menus"], strict=True):
                for layer in ("old", "inner", "outer"):
                    projected = [
                        {
                            "position_id": entry["position_id"],
                            "coefficients": self.study.encode(
                                [*case["corners"], entry["theta"][0][0]]
                            ),
                            "target": str(entry["targets"][0][0]),
                        }
                        for entry in new[layer]
                    ]
                    self.assertEqual(projected, old_menu[layer])
                    self.assertEqual(
                        [str(interval[0]) for interval in new["target_sets"][layer]["intervals"]],
                        old_menu[layer + "_targets"],
                    )
                for name in (
                    "existence_status",
                    "target_status",
                    "hypothesis_set_status",
                    "target_set_status",
                ):
                    self.assertEqual(new[name], old_menu[name])

    def test_selected_historical_fields_and_late_native_mutations_refused(self):
        base = ("analysis", "mathematics")
        paths = [
            ((*base, "bg_model", "geometry", "volume"), "7"),
            ((*base, "bg_model", "positions", -1, "basis", -1), "7"),
            ((*base, "bg_model", "positions", -1, "coefficient_decoder", -1, -1), "7"),
            ((*base, "bg_model", "cases", -1, "id"), "changed"),
            ((*base, "bg_model", "cases", -1, "population_means", -1), "7"),
            ((*base, "bg_model", "cases", -1, "law", "rows", -1, "probability"), "7"),
            ((*base, "bg_model", "cases", -1, "law", "rows", -1, "state_diagonal", -1), "7"),
            ((*base, "bg_model", "cases", -1, "law", "averaged_state", -1), "7"),
            ((*base, "bg_model", "cases", -1, "candidates", -1, "coefficients", -1), "7"),
            ((*base, "bg_model", "cases", -1, "candidates", -1, "target"), "7"),
            ((*base, "bg_model", "cases", -1, "candidates", -1, "admission_status"), "changed"),
            (
                (
                    *base,
                    "bg_model",
                    "cases",
                    -1,
                    "candidates",
                    -1,
                    "law",
                    "rows",
                    -1,
                    "state_diagonal",
                    -1,
                ),
                "7",
            ),
            ((*base, "bg_model", "cases", 0, "law", "rows", -1, "outcomes", 0), True),
            ((*base, "refinement", -1, "id"), "changed"),
            ((*base, "refinement", -1, "candidates", -1, "position_id"), "changed"),
            ((*base, "refinement", -1, "candidates", -1, "classification"), "changed"),
            ((*base, "refinement", -1, "candidates", -1, "old_admission_status"), "changed"),
            ((*base, "refinement", -1, "candidates", -1, "certificate_routes"), ["unknown"]),
            (
                (*base, "refinement", -1, "candidates", -1, "leaves", -1, "coefficients", -1, -1),
                "7",
            ),
            ((*base, "refinement", -1, "candidates", -1, "leaves", -1, "id"), "changed"),
            ((*base, "refinement", -1, "candidates", -1, "leaves", -1, "bounds", -1, -1), "7"),
            ((*base, "refinement", -1, "candidates", -1, "witnesses", -1, "position", -1), "7"),
            ((*base, "refinement", -1, "candidates", -1, "witnesses", -1, "value"), "7"),
            ((*base, "refinement", -1, "candidates", -1, "witnesses", -1, "status"), "changed"),
            ((*base, "refinement", -1, "candidates", -1, "violating_indices"), [99]),
            ((*base, "refinement", -1, "menus", -1, "id"), "changed"),
            ((*base, "refinement", -1, "menus", -1, "position_ids"), []),
            ((*base, "refinement", -1, "menus", -1, "target_status"), "changed"),
            ((*base, "refinement", 0, "menus", 0, "inner", 0, "coefficients", 0), "7"),
            ((*base, "refinement", 0, "menus", 0, "outer_targets", 0), "7"),
            ((*base, "refinement", 0, "menus", 0, "inner_range", "maximum"), "7"),
        ]
        for path, value in paths:
            changed = copy.deepcopy(self.previous)
            set_path(changed, path, value)
            self.assertNotEqual(self.study.canonical(changed), self.study.canonical(self.previous))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)
        for path in [
            (*base, "bg_model", "cases", -1, "candidates"),
            (*base, "refinement", -1, "candidates", -1, "leaves"),
            (*base, "refinement", -1, "candidates", -1, "witnesses"),
            (*base, "refinement", -1, "menus"),
        ]:
            changed = copy.deepcopy(self.previous)
            set_path(changed, path, get_path(changed, path)[:-1])
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)

    def test_current_point_and_typed_affine_restriction_mutations(self):
        paths = [
            (("cases", -1, "budgets", 0, "positions", -1, "data_theta", 1), Fraction(99)),
            (("cases", -1, "budgets", 0, "positions", -1, "point_classification"), None),
            (("cases", 0, "law_family", "rows", 0, "probability", 0), 0),
            (("cases", 0, "constraints", "patches", 0, "coefficients", 0, 0, 0), 0),
            (("cases", 0, "budgets", 0, "response_interval", 0), 0),
            (("cases", 0, "budgets", 0, "menus", 0, "inner", 0, "theta"), []),
            (
                ("cases", 0, "budgets", 0, "menus", 0, "target_sets", "inner", "intervals", 0),
                [None, None],
            ),
        ]
        for path, value in paths:
            changed = copy.deepcopy(self.report)
            set_path(changed, path, value)
            self.assertFalse(self.study.raw_same(changed, self.report))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(self.previous, changed)

    def test_unselected_history_and_nonpoint_output_are_not_old_replay(self):
        changed = copy.deepcopy(self.previous)
        old = changed["analysis"]["mathematics"]
        changed["analysis"]["bg_restriction"] = None
        changed["sources"] = None
        old["bg_model"]["witnesses"] = None
        old["bg_model"]["domain_control"] = None
        old["bg_model"]["cases"][0]["menus"] = None
        old["refinement"][0]["candidates"][0]["root"]["reconstruction_residual"] = None
        old["refinement"][0]["candidates"][0]["root"]["range_bound"] = None
        self.assertNotEqual(self.study.canonical(changed), self.study.canonical(self.previous))
        self.assertEqual(self.restriction(changed), self.receipt())
        current = copy.deepcopy(self.report)
        for case in current["cases"]:
            case["budgets"] = case["budgets"][:1]
        self.assertFalse(self.study.raw_same(current, self.report))
        self.assertEqual(self.restriction(self.previous, current), self.receipt())

    def test_historical_hash_precedes_parse_and_analysis_has_only_selected_receipt(self):
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=b"{}"),
            mock.patch.object(
                self.study, "_parse_json", side_effect=AssertionError("unverified history")
            ),
            self.assertRaises(ValueError),
        ):
            self.study._bh_restriction(self.report)
        with mock.patch.object(self.study, "compare_routes", return_value=self.report):
            result = self.study.analysis()
        exact_keys(self, result, "mathematics bh_restriction")
        self.assertEqual(result["mathematics"], self.study.encode(self.report))
        self.assertEqual(result["bh_restriction"], self.receipt())


class SourceIdentityTests(unittest.TestCase):
    def test_exact_eleven_current_and_bh_source_identities(self):
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
                "test_qr05bi.py",
            )
        ]
        previous = [
            study.BH_DIRECTORY / name
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

    def snapshots(self, study, bi_data=None, bh_data=None):
        bi_path = HERE / "protocol.json"
        bh_path = study.BH_DIRECTORY / "protocol.json"
        data = bi_path.read_bytes() if bi_data is None else bi_data
        model = bh_path.read_bytes() if bh_data is None else bh_data

        def read(path):
            if Path(path) == bi_path:
                return data
            if Path(path) == bh_path:
                return model
            raise AssertionError("unexpected protocol snapshot: " + str(path))

        return data, model, read

    def test_both_protocol_hashes_and_parses_use_their_same_read_snapshots(self):
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

    def test_each_protocol_hash_rejects_before_its_own_semantic_parse(self):
        study = load_module("study")
        _data, _model, reader = self.snapshots(study, bi_data=b"{}")
        with (
            mock.patch.object(study, "_read_bounded", side_effect=reader),
            mock.patch.object(
                study, "_parse_json", side_effect=AssertionError("unverified BI parse")
            ),
            self.assertRaisesRegex(ValueError, "protocol identity changed"),
        ):
            study.load_protocol()
        data, _model, reader = self.snapshots(study, bh_data=b"{}")
        original_parse = study._parse_json

        def parse(blob):
            if blob is not data:
                raise AssertionError("unverified BH parse")
            return original_parse(blob)

        with (
            mock.patch.object(study, "_read_bounded", side_effect=reader),
            mock.patch.object(study, "_parse_json", side_effect=parse) as parsed,
            self.assertRaisesRegex(ValueError, "preceding BH protocol identity changed"),
        ):
            study.load_protocol()
        self.assertEqual(parsed.call_count, 1)

    def test_authenticated_budget_shape_and_nested_model_mutations_reach_own_guards(self):
        study = load_module("study")
        protocol = json.loads((HERE / "protocol.json").read_bytes())
        mutations = [
            (("version",), True, "version differs"),
            (("study",), "QR-05BH", "study differs"),
            (("interval_budgets", 1, "radius"), "1/63", "interval budget differs"),
            (("interval_budgets", 0, "radius"), 0, "interval budget differs"),
            (("interval_budgets", 2, "id"), "adaptive", "interval budget differs"),
            (("interval_budgets",), protocol["interval_budgets"][:-1], "interval budget differs"),
            (("model", "certificate", "degree", 0), True, "complete BH input differs"),
            (
                ("model", "certificate", "leaves"),
                protocol["model"]["certificate"]["leaves"][:-1],
                "complete BH input differs",
            ),
            (("model", "model", "cases", 0, "population_means", 0), 0, "complete BH input differs"),
            (("model", "model", "positions", 0, "id"), "unknown", "complete BH input differs"),
            (
                ("model", "model", "menus", 0, "position_ids", 1),
                "center",
                "complete BH input differs",
            ),
        ]
        for path, value, message in mutations:
            changed = copy.deepcopy(protocol)
            set_path(changed, path, value)
            self.assertNotEqual(study.canonical(changed), study.canonical(protocol))
            data = json.dumps(changed).encode()
            _data, model, reader = self.snapshots(study, bi_data=data)
            original_identity = study._bytes_identity

            def authenticate(blob, bi=data, identity_fn=original_identity):
                identity = identity_fn(blob)
                if blob is bi:
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
                hashlib.sha256(model).hexdigest(), study.BH_IDENTITIES["protocol.json"]
            )


if __name__ == "__main__":
    unittest.main()
