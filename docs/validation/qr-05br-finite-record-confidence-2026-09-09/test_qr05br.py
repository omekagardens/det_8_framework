"""Independent BR polynomial/endpoint/arrangement oracle and record API tests.

No mathematical work runs at import. The root author owns the separate
integration/deadline tail. Historical numerical executors are never imported.
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
from unittest import mock

HERE = Path(__file__).resolve().parent


def load_study():
    spec = importlib.util.spec_from_file_location("_qr05br_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load BR driver")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def evaluated():
    study = load_study()
    protocol = json.loads((HERE / "protocol.json").read_bytes())
    return study, protocol, study.analyze()


def exact_tree(test, actual, wanted, path="$"):
    test.assertIs(type(actual), type(wanted), path)
    if type(wanted) is dict:
        test.assertEqual(set(actual), set(wanted), path)
        test.assertTrue(all(type(key) is str for key in actual), path)
        for key in wanted:
            exact_tree(test, actual[key], wanted[key], path + "." + key)
    elif type(wanted) is list:
        test.assertEqual(len(actual), len(wanted), path)
        for index, (left, right) in enumerate(zip(actual, wanted, strict=True)):
            exact_tree(test, left, right, path + "[" + str(index) + "]")
    else:
        test.assertEqual(actual, wanted, path)


def polynomial(coefficients, value):
    result = Fraction(0)
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def tail_pair(k, p):
    """Closed n=4 tail polynomials, not binomial summation or convolution."""
    upper = (
        (1,),
        (0, 4, -6, 4, -1),
        (0, 0, 6, -8, 3),
        (0, 0, 0, 4, -3),
        (0, 0, 0, 0, 1),
    )
    plus = polynomial(upper[k], p)
    minus = Fraction(1) if k == 4 else 1 - polynomial(upper[k + 1], p)
    return plus, minus


def endpoint_certificate(k, side, epsilon, table, denominator):
    column = "plus" if side == "lower" else "minus"
    rows = [row for row in table if row["k"] == k]
    default = (side == "lower" and k == 0) or (side == "upper" and k == 4)
    if default:
        index = 0 if side == "lower" else denominator
    else:
        eligible = [index for index, row in enumerate(rows) if row[column] <= epsilon]
        index = max(eligible) if side == "lower" else min(eligible)
    selected = rows[index]
    neighbor = []
    if not default:
        adjacent = rows[index + (1 if side == "lower" else -1)]
        neighbor = [[adjacent["grid"], adjacent[column]]]
    return {
        "kind": "default" if default else "tail",
        "grid": selected["grid"],
        "tail": selected[column],
        "neighbor": neighbor,
    }


def choose(n, k):
    """Select marked slots, then select the nested subset of those slots."""
    result = 1
    for step in range(1, k + 1):
        numerator = result * (n - k + step)
        if numerator % step:
            raise ValueError("binomial recurrence did not give an integer")
        result = numerator // step
    return result


def confidence_oracle(protocol):
    observer = protocol["observer"]
    return {
        "quota": protocol["quota"],
        "alpha": Fraction(*protocol["alpha"]),
        "tail_allocations": [Fraction(*pair) for pair in protocol["tail_allocations"]],
        "grid_denominator": protocol["grid_denominator"],
        "confidence_basis": observer["confidence_basis"],
        "bound_basis": observer["bound_basis"],
        "coverage_kind": observer["coverage_kind"],
    }


def endpoint_moment(rectangle, degree):
    a, b, c, d = [Fraction(*pair) for pair in rectangle]
    order = degree + 1
    return (b**order - a**order) * (d**order - c**order) / order**2


def mass_coefficients(protocol, eta, scale):
    rows = []
    for name in ("Q", "I1", "I2"):
        moments = [endpoint_moment(protocol["regions"][name], degree) for degree in range(3)]
        rows.append(
            [
                Fraction(scale, 2) * (moments[0] + eta * moments[1]),
                Fraction(scale, 2) * (moments[1] + eta * moments[2]),
            ]
        )
    return rows


def at(coefficients, delta):
    return coefficients[0] + delta * coefficients[1]


def probabilities(masses, delta):
    denominator = at(masses[0], delta)
    if denominator <= 0:
        raise ValueError("oracle requires positive denominator on the domain")
    return [at(row, delta) / denominator for row in masses[1:]]


def subtract(left, right):
    return [a - b for a, b in zip(left, right, strict=True)]


def inequality_rows(masses, intervals):
    rows = []
    denominator = masses[0]
    for numerator, (lower, upper) in zip(masses[1:], intervals, strict=True):
        rows.extend(
            [
                [a - lower * b for a, b in zip(numerator, denominator, strict=True)],
                [upper * b - a for a, b in zip(numerator, denominator, strict=True)],
            ]
        )
    return rows


def inequality_wire(row):
    constant, slope = row
    return {
        "constant": constant,
        "slope": slope,
        "kind": "lower"
        if slope > 0
        else "upper"
        if slope < 0
        else "all"
        if constant >= 0
        else "none",
        "boundary": [-constant / slope] if slope else [],
    }


def breakpoint_set(masses, intervals, domain, selected):
    """Evaluate original ratios on a finite exact arrangement, not halfspace clipping."""
    lower, upper = domain
    faces = inequality_rows(masses, intervals)
    nodes = {lower, upper}
    for index in selected:
        for constant, slope in faces[2 * index : 2 * index + 2]:
            if slope:
                root = -constant / slope
                if lower <= root <= upper:
                    nodes.add(root)
    nodes = sorted(nodes)

    def admitted(delta):
        q = probabilities(masses, delta)
        return all(intervals[index][0] <= q[index] <= intervals[index][1] for index in selected)

    pieces = [[node, node] for node in nodes if admitted(node)]
    for left, right in itertools.pairwise(nodes):
        if admitted((left + right) / 2):
            if not admitted(left) or not admitted(right):
                raise ValueError("closed continuous constraints lost an admitted cell endpoint")
            pieces.append([left, right])
    joined = []
    for left, right in sorted(pieces):
        if joined and left <= joined[-1][1]:
            joined[-1][1] = max(joined[-1][1], right)
        else:
            joined.append([left, right])
    if len(joined) > 1:
        raise ValueError("affine ratio constraints unexpectedly produced disconnected feasibility")
    return joined[0] if joined else []


def interval_subset(left, right):
    return not left or (bool(right) and right[0] <= left[0] <= left[1] <= right[1])


def curve_wire(masses, domain):
    if not domain:
        return {}
    numerators, denominator = masses[1:], masses[0]
    one_numerators = [
        subtract(denominator, numerators[1]),
        subtract(numerators[1], numerators[0]),
        [Fraction(0), Fraction(0)],
        numerators[0],
    ]
    endpoints = []
    for delta in domain:
        q = probabilities(masses, delta)
        endpoints.append(
            {"delta": delta, "q": q, "one_point": [1 - q[1], q[1] - q[0], Fraction(0), q[0]]}
        )
    return {
        "domain": list(domain),
        "numerators": copy.deepcopy(numerators),
        "denominator": list(denominator),
        "one_point_numerators": one_numerators,
        "endpoints": endpoints,
        "q_ranges": [
            sorted([endpoints[0]["q"][index], endpoints[1]["q"][index]]) for index in range(2)
        ],
    }


def geometry_oracle(item, protocol):
    masses = mass_coefficients(protocol, item["eta"], item["scale"])
    denominator = masses[0]
    categories = [subtract(denominator, masses[2]), subtract(masses[2], masses[1]), masses[1]]
    endpoint_q = [probabilities(masses, Fraction(delta)) for delta in (0, 2)]
    return {
        "id": item["id"],
        "eta": item["eta"],
        "scale": item["scale"],
        "volumes": [row[0] for row in masses],
        "target": masses[1][0] / masses[0][0],
        "mass_coefficients": masses,
        "derivative_numerators": [
            row[1] * denominator[0] - row[0] * denominator[1] for row in masses[1:]
        ],
        "full_q_ranges": [
            sorted([endpoint_q[0][index], endpoint_q[1][index]]) for index in range(2)
        ],
        "category_coefficients": categories,
        "strict_support": all(
            at(row, Fraction(delta)) > 0 for row in categories for delta in (0, 2)
        ),
    }


def hypothesis(geometry, datum, domain):
    masses, intervals = geometry["mass_coefficients"], datum["intervals"]
    query_sets = [breakpoint_set(masses, intervals, domain, [index]) for index in range(2)]
    coupled = breakpoint_set(masses, intervals, domain, [0, 1])
    if coupled and not all(interval_subset(coupled, single) for single in query_sets):
        raise ValueError("coupled interval escaped an individual query")
    return {
        "id": geometry["id"],
        "inequalities": [inequality_wire(row) for row in inequality_rows(masses, intervals)],
        "query_sets": query_sets,
        "delta_set": coupled,
        "status": "feasible" if coupled else "infeasible",
        "curve": curve_wire(masses, coupled),
    }


def ratio_polynomial_equal(left_numerator, left_denominator, right_numerator, right_denominator):
    def product(left, right):
        return [left[0] * right[0], left[0] * right[1] + left[1] * right[0], left[1] * right[1]]

    return product(left_numerator, right_denominator) == product(right_numerator, left_denominator)


def expected(protocol):
    confidence = confidence_oracle(protocol)
    denominator = protocol["grid_denominator"]
    epsilon = confidence["tail_allocations"][0]
    alpha = confidence["alpha"]
    tails = []
    for k in range(5):
        for index in range(denominator + 1):
            grid = Fraction(index, denominator)
            plus, minus = tail_pair(k, grid)
            tails.append({"k": k, "grid": grid, "plus": plus, "minus": minus})
    intervals = []
    for k in range(5):
        lower = endpoint_certificate(k, "lower", epsilon, tails, denominator)
        upper = endpoint_certificate(k, "upper", epsilon, tails, denominator)
        intervals.append(
            {"k": k, "interval": [lower["grid"], upper["grid"]], "lower": lower, "upper": upper}
        )
    counts = []
    for k1 in range(5):
        for k2 in range(k1, 5):
            box = [list(intervals[k]["interval"]) for k in (k1, k2)]
            counts.append(
                {
                    "id": str(k1) + "/" + str(k2),
                    "k": [k1, k2],
                    "category_counts": [4 - k2, k2 - k1, k1],
                    "multiplicity": choose(4, k2) * choose(k2, k1),
                    "intervals": box,
                    "nested_nonempty": box[0][0] <= box[1][1],
                }
            )
    geometries = [geometry_oracle(row, protocol) for row in protocol["geometries"]]
    targets_by_geometry = {row["id"]: row["target"] for row in geometries}
    cases = []
    for bound in protocol["density_bounds"]:
        domain = [Fraction(*pair) for pair in bound["interval"]]
        for count in counts:
            hypotheses = [hypothesis(geometry, count, domain) for geometry in geometries]
            worlds = [row["id"] for row in hypotheses if row["delta_set"]]
            targets = sorted({targets_by_geometry[name] for name in worlds})
            cases.append(
                {
                    "id": bound["id"] + "/" + count["id"],
                    "bound": bound["id"],
                    "count": count["id"],
                    "intervals": copy.deepcopy(count["intervals"]),
                    "nested_nonempty": count["nested_nonempty"],
                    "hypotheses": hypotheses,
                    "worlds": worlds,
                    "targets": targets,
                    "status": "infeasible"
                    if not targets
                    else "identified"
                    if len(targets) == 1
                    else "ambiguous",
                }
            )
    fixtures = []
    for fixture in protocol["fixtures"]:
        geometry = next(
            row for row in geometries if row["eta"] == fixture["eta"] and row["scale"] == 1
        )
        delta = Fraction(*fixture["delta"])
        q = probabilities(geometry["mass_coefficients"], delta)
        one_point = [1 - q[1], q[1] - q[0], Fraction(0), q[0]]
        law = []
        for count in counts:
            probability = Fraction(count["multiplicity"])
            for value, power in zip(
                (one_point[0], one_point[1], one_point[3]), count["category_counts"], strict=True
            ):
                probability *= value**power
            law.append(
                {
                    "count": count["id"],
                    "p": probability,
                    "population_covered": all(
                        lower <= value <= upper
                        for value, (lower, upper) in zip(q, count["intervals"], strict=True)
                    ),
                }
            )
        means = [
            sum(
                (row["p"] * count["k"][i] for row, count in zip(law, counts, strict=True)),
                Fraction(0),
            )
            for i in range(2)
        ]
        product_mean = sum(
            (
                row["p"] * count["k"][0] * count["k"][1]
                for row, count in zip(law, counts, strict=True)
            ),
            Fraction(0),
        )
        fixtures.append(
            {
                "id": fixture["id"],
                "eta": fixture["eta"],
                "delta": delta,
                "target": geometry["target"],
                "q": q,
                "one_point": one_point,
                "count_law": law,
                "independent_10": q[0] * (1 - q[1]),
                "count_covariance": product_mean - means[0] * means[1],
            }
        )
    case_by_id = {row["id"]: row for row in cases}
    summaries = []
    for fixture in fixtures:
        for bound in protocol["density_bounds"]:
            domain = [Fraction(*pair) for pair in bound["interval"]]
            population_miss = Fraction(0)
            target_miss = Fraction(0)
            totals = {status: Fraction(0) for status in ("infeasible", "identified", "ambiguous")}
            wrong = Fraction(0)
            for row in fixture["count_law"]:
                case = case_by_id[bound["id"] + "/" + row["count"]]
                p = row["p"]
                population_miss += p * (not row["population_covered"])
                missed = fixture["target"] not in case["targets"]
                target_miss += p * missed
                totals[case["status"]] += p
                wrong += p * (missed and case["status"] == "identified")
            singleton = totals["identified"]
            summaries.append(
                {
                    "id": fixture["id"] + "/" + bound["id"],
                    "fixture": fixture["id"],
                    "bound": bound["id"],
                    "in_premise": domain[0] <= fixture["delta"] <= domain[1],
                    "population_noncoverage": population_miss,
                    "target_noncoverage": target_miss,
                    "empty": totals["infeasible"],
                    "singleton": singleton,
                    "wrong_singleton": wrong,
                    "ambiguous": totals["ambiguous"],
                    "conditional_wrong_singleton": [wrong / singleton] if singleton else [],
                    "population_bound_holds": population_miss <= alpha,
                    "target_bound_holds": target_miss <= alpha,
                }
            )
    scale_pairs = []
    for left, right in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        a, b = (next(row for row in geometries if row["id"] == name) for name in (left, right))
        nuisance_equal = True
        curve_equal = True
        for case in cases:
            x, y = (
                next(row for row in case["hypotheses"] if row["id"] == name)
                for name in (left, right)
            )
            nuisance_equal = nuisance_equal and x["delta_set"] == y["delta_set"]
            if not x["curve"] or not y["curve"]:
                curve_equal = curve_equal and x["curve"] == y["curve"]
            else:
                curve_equal = curve_equal and x["curve"]["endpoints"] == y["curve"]["endpoints"]
                curve_equal = curve_equal and all(
                    ratio_polynomial_equal(
                        an, x["curve"]["denominator"], bn, y["curve"]["denominator"]
                    )
                    for an, bn in zip(
                        x["curve"]["numerators"], y["curve"]["numerators"], strict=True
                    )
                )
        scale_pairs.append(
            {
                "worlds": [left, right],
                "volume_factor": b["volumes"][0] / a["volumes"][0],
                "target_equal": a["target"] == b["target"],
                "nuisance_sets_equal": nuisance_equal,
                "curve_laws_equal": curve_equal,
            }
        )
    fixture_by_id = {row["id"]: row for row in fixtures}
    comparisons = []
    for name, left, right in (
        ("whole_point", "flat_1", "conformal_0"),
        ("membership_only", "flat_interior", "conformal_interior"),
    ):
        a, b = fixture_by_id[left], fixture_by_id[right]
        comparisons.append(
            {
                "id": name,
                "fixtures": [left, right],
                "q1_equal": a["q"][0] == b["q"][0],
                "q2_equal": a["q"][1] == b["q"][1],
                "count_law_equal": [row["p"] for row in a["count_law"]]
                == [row["p"] for row in b["count_law"]],
                "target_gap": a["target"] - b["target"],
                "q2_gap": a["q"][1] - b["q"][1],
            }
        )
    ties = [
        {
            "id": row["id"],
            "side": row["side"],
            "k": row["k"],
            "epsilon": Fraction(*row["epsilon"]),
            "certificate": endpoint_certificate(
                row["k"], row["side"], Fraction(*row["epsilon"]), tails, denominator
            ),
        }
        for row in protocol["ties"]
    ]
    obstruction_cases = []
    for case in cases:
        a, b = (
            next(row for row in case["hypotheses"] if row["id"] == name)
            for name in ("flat", "conformal")
        )
        flat = bool(a["delta_set"]) and a["delta_set"][0] <= 1 <= a["delta_set"][1]
        conformal = bool(b["delta_set"]) and b["delta_set"][0] <= 0 <= b["delta_set"][1]
        obstruction_cases.append(
            {
                "case": case["id"],
                "flat_present": flat,
                "conformal_present": conformal,
                "both": flat and conformal,
                "target_ambiguous": case["status"] == "ambiguous",
            }
        )
    common = fixture_by_id["flat_1"]
    coverage = []
    for bound in protocol["density_bounds"]:
        domain = [Fraction(*pair) for pair in bound["interval"]]
        both_probability = sum(
            (
                row["p"]
                for row in common["count_law"]
                if len(case_by_id[bound["id"] + "/" + row["count"]]["targets"]) == 2
            ),
            Fraction(0),
        )
        coverage.append(
            {
                "bound": bound["id"],
                "both_in_premise": domain[0] <= 0 and 1 <= domain[1],
                "both_target_probability": both_probability,
                "bound_holds": both_probability >= 1 - alpha,
            }
        )
    point_polynomials = []
    for eta, delta in ((0, Fraction(1)), (1, Fraction(0))):
        masses = mass_coefficients(protocol, eta, 1)
        normalizer = 2 * at(masses[0], delta)
        point_polynomials.append(
            [Fraction(1) / normalizer, (eta + delta) / normalizer, eta * delta / normalizer]
        )
    obstruction = {
        "worlds": ["flat", "conformal"],
        "deltas": [Fraction(1), Fraction(0)],
        "q": list(common["q"]),
        "point_equal": point_polynomials[0] == point_polynomials[1],
        "target_gap": common["target"] - fixture_by_id["conformal_0"]["target"],
        "cases": obstruction_cases,
        "coverage": coverage,
    }
    return {
        "schema": "qr05br-report-v1",
        "confidence": confidence,
        "tails": tails,
        "intervals": intervals,
        "counts": counts,
        "geometries": geometries,
        "cases": cases,
        "fixtures": fixtures,
        "summaries": summaries,
        "scale_pairs": scale_pairs,
        "comparisons": comparisons,
        "ties": ties,
        "obstruction": obstruction,
        "support": {
            "symbols": [[0, 0], [0, 1], [1, 0], [1, 1]],
            "allowed": [[0, 0], [0, 1], [1, 1]],
            "count_states": 15,
            "possible_words": 3**4,
            "zero_words": 4**4 - 3**4,
            "continuous_certificate": all(row["strict_support"] for row in geometries),
        },
    }


def packet(k1, k2, bound="two"):
    bits = (
        [[0, 0] for _ in range(4 - k2)]
        + [[0, 1] for _ in range(k2 - k1)]
        + [[1, 1] for _ in range(k1)]
    )
    return {
        "schema": "qr05br-record-query-v1",
        "protocol_id": "qr05br-n4-g256-a20-v1",
        "data_kind": "paired_causal_records",
        "records": [{"attempt": index + 1, "bits": row} for index, row in enumerate(bits)],
        "density_bound": bound,
        "bound_basis": "external_assumption",
    }


def answer(case):
    return {
        "nested_nonempty": case["nested_nonempty"],
        "worlds": list(case["worlds"]),
        "targets": list(case["targets"]),
        "status": case["status"],
        "nuisance": [
            {"id": row["id"], "delta": list(row["delta_set"])}
            for row in case["hypotheses"]
            if row["delta_set"]
        ],
    }


def accepted(report, case):
    count = next(row for row in report["counts"] if row["id"] == case["count"])
    return {
        "schema": "qr05br-record-result-v1",
        "status": "accepted",
        "reason": "",
        "confidence": copy.deepcopy(report["confidence"]),
        "counts": list(count["k"]),
        "intervals": copy.deepcopy(case["intervals"]),
        "answer": answer(case),
    }


class MathematicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.oracle = expected(cls.protocol)

    def test_complete_native_report_and_declared_finite_inventory(self):
        exact_tree(self, self.report, self.oracle)
        report = self.report
        census = {
            "tail_rows": len(report["tails"]),
            "tail_values": 2 * len(report["tails"]),
            "intervals": len(report["intervals"]),
            "counts": len(report["counts"]),
            "cases": len(report["cases"]),
            "hypotheses": sum(len(row["hypotheses"]) for row in report["cases"]),
            "fixtures": len(report["fixtures"]),
            "count_probabilities": sum(len(row["count_law"]) for row in report["fixtures"]),
            "summaries": len(report["summaries"]),
            "scale_pairs": len(report["scale_pairs"]),
            "comparisons": len(report["comparisons"]),
            "ties": len(report["ties"]),
            "obstruction_cases": len(report["obstruction"]["cases"]),
            "obstruction_coverage": len(report["obstruction"]["coverage"]),
        }
        exact_tree(self, census, self.protocol["coverage"])
        self.assertEqual(report["confidence"]["tail_allocations"], [Fraction(1, 80)] * 4)
        self.assertEqual(
            sum(report["confidence"]["tail_allocations"]), report["confidence"]["alpha"]
        )

    def test_closed_polynomial_tails_degenerate_laws_and_monotonicity(self):
        table = {(row["k"], row["grid"]): row for row in self.report["tails"]}
        denominator = self.protocol["grid_denominator"]
        for k in range(5):
            self.assertEqual(table[k, Fraction(0)]["plus"], Fraction(k == 0))
            self.assertEqual(table[k, Fraction(0)]["minus"], Fraction(1))
            self.assertEqual(table[k, Fraction(1)]["plus"], Fraction(1))
            self.assertEqual(table[k, Fraction(1)]["minus"], Fraction(k == 4))
            for index in range(denominator + 1):
                p = Fraction(index, denominator)
                row = table[k, p]
                plus, minus = tail_pair(k, p)
                self.assertEqual((row["plus"], row["minus"]), (plus, minus))
                self.assertEqual(plus, table[4 - k, 1 - p]["minus"])
                self.assertTrue(0 <= plus <= 1 and 0 <= minus <= 1)
                self.assertGreaterEqual(plus + minus, 1)
                self.assertNotEqual(plus, Fraction(1, 80))
                self.assertNotEqual(minus, Fraction(1, 80))
                if index:
                    previous = table[k, p - Fraction(1, denominator)]
                    self.assertGreaterEqual(plus, previous["plus"])
                    self.assertLessEqual(minus, previous["minus"])
                if k:
                    self.assertLessEqual(plus, table[k - 1, p]["plus"])
                    self.assertGreaterEqual(minus, table[k - 1, p]["minus"])

    def test_selected_adjacent_certificates_and_private_equality_controls(self):
        denominator = self.protocol["grid_denominator"]

        def check(certificate, k, side, epsilon):
            component = 0 if side == "lower" else 1
            grid = certificate["grid"]
            self.assertEqual(certificate["tail"], tail_pair(k, grid)[component])
            if certificate["kind"] == "default":
                self.assertEqual((k, side), (0, "lower") if side == "lower" else (4, "upper"))
                self.assertEqual(grid, Fraction(0 if side == "lower" else 1))
                self.assertEqual(certificate["tail"], Fraction(1))
                self.assertEqual(certificate["neighbor"], [])
            else:
                self.assertEqual(certificate["kind"], "tail")
                self.assertLessEqual(certificate["tail"], epsilon)
                self.assertEqual(len(certificate["neighbor"]), 1)
                adjacent, value = certificate["neighbor"][0]
                self.assertEqual(
                    adjacent - grid, Fraction(1 if side == "lower" else -1, denominator)
                )
                self.assertEqual(value, tail_pair(k, adjacent)[component])
                self.assertGreater(value, epsilon)

        for row in self.report["intervals"]:
            for side in ("lower", "upper"):
                check(row[side], row["k"], side, Fraction(1, 80))
            self.assertEqual(row["interval"], [row["lower"]["grid"], row["upper"]["grid"]])
            self.assertLessEqual(*row["interval"])
        for row in self.report["ties"]:
            check(row["certificate"], row["k"], row["side"], row["epsilon"])
            self.assertEqual(row["epsilon"], Fraction(1, 16))
            self.assertEqual(row["certificate"]["grid"], Fraction(1, 2))
            self.assertEqual(row["certificate"]["tail"], row["epsilon"])
        # An inward substitute violates the retained threshold certificate.
        # This is not a claim that a finite coverage census must detect it.
        row = self.report["intervals"][1]
        changed = copy.deepcopy(row["lower"])
        changed["grid"], changed["tail"] = changed["neighbor"][0]
        with self.assertRaises(AssertionError):
            check(changed, row["k"], "lower", Fraction(1, 80))

    def test_complete_count_coefficients_marginals_and_same_point_covariance(self):
        counts = self.report["counts"]
        self.assertEqual(
            [row["k"] for row in counts], [[a, b] for a in range(5) for b in range(a, 5)]
        )
        self.assertEqual(sum(row["multiplicity"] for row in counts), 3**4)
        for row in counts:
            k1, k2 = row["k"]
            self.assertEqual(row["category_counts"], [4 - k2, k2 - k1, k1])
            self.assertEqual(sum(row["category_counts"]), 4)
            self.assertEqual(row["multiplicity"], choose(4, k2) * choose(k2, k1))
        for fixture in self.report["fixtures"]:
            q1, q2 = fixture["q"]
            law = fixture["count_law"]
            self.assertEqual([row["count"] for row in law], [row["id"] for row in counts])
            self.assertEqual(sum(row["p"] for row in law), 1)
            self.assertTrue(all(row["p"] > 0 for row in law))
            self.assertEqual(sum(fixture["one_point"]), 1)
            self.assertEqual(fixture["one_point"][2], Fraction(0))
            self.assertGreater(fixture["independent_10"], 0)
            self.assertEqual(fixture["independent_10"], q1 * (1 - q2))
            means = []
            for i, q in enumerate((q1, q2)):
                marginal = [
                    sum(
                        (
                            row["p"]
                            for count, row in zip(counts, law, strict=True)
                            if count["k"][i] == k
                        ),
                        Fraction(0),
                    )
                    for k in range(5)
                ]
                for k in range(5):
                    pmf = tail_pair(k, q)[0] - (tail_pair(k + 1, q)[0] if k < 4 else 0)
                    self.assertEqual(marginal[k], pmf)
                means.append(sum((k * value for k, value in enumerate(marginal)), Fraction(0)))
                self.assertEqual(means[-1], 4 * q)
            product_mean = sum(
                (
                    row["p"] * count["k"][0] * count["k"][1]
                    for count, row in zip(counts, law, strict=True)
                ),
                Fraction(0),
            )
            covariance = product_mean - means[0] * means[1]
            self.assertEqual(covariance, fixture["count_covariance"])
            self.assertEqual(covariance, 4 * q1 * (1 - q2))
            self.assertGreater(covariance, 0)
            self.assertNotEqual(product_mean, means[0] * means[1])

    def test_all_coupled_nuisance_intervals_forward_endpoints_and_density_inclusion(self):
        geometries = {row["id"]: row for row in self.report["geometries"]}
        cases = {row["id"]: row for row in self.report["cases"]}
        for case in self.report["cases"]:
            for row in case["hypotheses"]:
                domain = row["delta_set"]
                if not domain:
                    self.assertEqual(row["curve"], {})
                    continue
                curve = row["curve"]
                self.assertEqual(len(curve["endpoints"]), 2)
                self.assertEqual(curve["domain"], domain)
                self.assertEqual(curve["one_point_numerators"][2], [Fraction(0), Fraction(0)])
                self.assertTrue(
                    all(interval_subset(domain, single) for single in row["query_sets"])
                )
                masses = geometries[row["id"]]["mass_coefficients"]
                for endpoint, delta in zip(curve["endpoints"], domain, strict=True):
                    self.assertEqual(endpoint["delta"], delta)
                    self.assertEqual(endpoint["q"], probabilities(masses, delta))
                    self.assertEqual(
                        endpoint["one_point"],
                        [
                            1 - endpoint["q"][1],
                            endpoint["q"][1] - endpoint["q"][0],
                            Fraction(0),
                            endpoint["q"][0],
                        ],
                    )
                for delta in (domain[0], (domain[0] + domain[1]) / 2, domain[1]):
                    q = probabilities(masses, delta)
                    self.assertTrue(
                        all(
                            lower <= value <= upper
                            for value, (lower, upper) in zip(q, case["intervals"], strict=True)
                        )
                    )
                    self.assertTrue(
                        all(
                            at([face["constant"], face["slope"]], delta) >= 0
                            for face in row["inequalities"]
                        )
                    )
                self.assertEqual(
                    curve["q_ranges"],
                    [
                        sorted([curve["endpoints"][0]["q"][i], curve["endpoints"][1]["q"][i]])
                        for i in range(2)
                    ],
                )
        for tight, broad in itertools.pairwise(self.protocol["density_bounds"]):
            for count in self.report["counts"]:
                a, b = (cases[bound["id"] + "/" + count["id"]] for bound in (tight, broad))
                self.assertTrue(set(a["worlds"]).issubset(b["worlds"]))
                self.assertTrue(set(a["targets"]).issubset(b["targets"]))
                for x, y in zip(a["hypotheses"], b["hypotheses"], strict=True):
                    self.assertEqual(x["id"], y["id"])
                    self.assertTrue(interval_subset(x["delta_set"], y["delta_set"]))

    def test_actual_scale_polynomials_support_and_discrete_target_projection(self):
        geometries = {row["id"]: row for row in self.report["geometries"]}
        for left, right in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
            a, b = geometries[left], geometries[right]
            self.assertEqual(b["volumes"], [4 * value for value in a["volumes"]])
            self.assertEqual(
                b["mass_coefficients"],
                [[4 * value for value in row] for row in a["mass_coefficients"]],
            )
            self.assertEqual(
                b["derivative_numerators"], [16 * value for value in a["derivative_numerators"]]
            )
            for case in self.report["cases"]:
                x, y = (
                    next(row for row in case["hypotheses"] if row["id"] == name)
                    for name in (left, right)
                )
                self.assertEqual(x["delta_set"], y["delta_set"])
                self.assertEqual(bool(x["curve"]), bool(y["curve"]))
                if x["curve"]:
                    for field in ("numerators", "one_point_numerators"):
                        self.assertEqual(
                            y["curve"][field],
                            [[4 * value for value in row] for row in x["curve"][field]],
                        )
                    self.assertEqual(
                        y["curve"]["denominator"],
                        [4 * value for value in x["curve"]["denominator"]],
                    )
                    self.assertEqual(x["curve"]["endpoints"], y["curve"]["endpoints"])
        for geometry in geometries.values():
            self.assertTrue(geometry["strict_support"])
            for coefficients in geometry["category_coefficients"]:
                # Affine mass positivity on the full closed density domain.
                self.assertGreater(at(coefficients, Fraction(0)), 0)
                self.assertGreater(at(coefficients, Fraction(2)), 0)
        self.assertEqual(self.report["support"]["count_states"], 15)
        self.assertEqual(self.report["support"]["possible_words"], 81)
        self.assertEqual(self.report["support"]["zero_words"], 175)
        for case in self.report["cases"]:
            self.assertEqual(
                case["targets"], sorted({geometries[name]["target"] for name in case["worlds"]})
            )
            self.assertTrue(set(case["targets"]).issubset({Fraction(17, 80), Fraction(1, 4)}))

    def test_two_prespecified_private_inverse_zero_slope_and_closed_shared_contacts(self):
        # These are the two declared helper regressions, not additional record
        # packets, population fixtures, or grid evaluations.
        pole = [[Fraction(1, 16), Fraction(1, 16)], [Fraction(0), Fraction(1)]]
        touch = [[Fraction(3, 16), Fraction(17, 80)], [Fraction(21, 64), Fraction(3, 8)]]
        for intervals in (pole, touch):
            hypotheses = [
                hypothesis(row, {"intervals": intervals}, [Fraction(0), Fraction(2)])
                for row in self.oracle["geometries"]
            ]
            worlds = [row["id"] for row in hypotheses if row["delta_set"]]
            targets = sorted(
                {row["target"] for row in self.oracle["geometries"] if row["id"] in worlds}
            )
            wanted = {
                "nested_nonempty": intervals[0][0] <= intervals[1][1],
                "worlds": worlds,
                "targets": targets,
                "status": "infeasible"
                if not targets
                else "identified"
                if len(targets) == 1
                else "ambiguous",
                "nuisance": [
                    {"id": row["id"], "delta": row["delta_set"]}
                    for row in hypotheses
                    if row["delta_set"]
                ],
            }
            actual = self.study._inverse(intervals, (2, 1))
            exact_tree(self, actual, wanted)
            if intervals == pole:
                self.assertEqual(actual["status"], "infeasible")
                self.assertEqual(actual["nuisance"], [])
                self.assertTrue(
                    any(
                        face["slope"] == 0 and face["kind"] == "none"
                        for row in hypotheses
                        for face in row["inequalities"]
                    )
                )
            else:
                self.assertEqual(actual["status"], "ambiguous")
                self.assertEqual(
                    actual["nuisance"],
                    [
                        {"id": "flat", "delta": [Fraction(1), Fraction(1)]},
                        {"id": "conformal", "delta": [Fraction(0), Fraction(0)]},
                        {"id": "flat_x4", "delta": [Fraction(1), Fraction(1)]},
                        {"id": "conformal_x4", "delta": [Fraction(0), Fraction(0)]},
                    ],
                )

    def test_coverage_accounting_keeps_empty_out_of_premise_and_selection_events(self):
        report = self.report
        fixtures = {row["id"]: row for row in report["fixtures"]}
        cases = {row["id"]: row for row in report["cases"]}
        alpha = report["confidence"]["alpha"]
        self.assertTrue(any(not row["in_premise"] for row in report["summaries"]))
        for summary in report["summaries"]:
            fixture = fixtures[summary["fixture"]]
            self.assertEqual(summary["empty"] + summary["singleton"] + summary["ambiguous"], 1)
            self.assertEqual(
                summary["target_noncoverage"], summary["empty"] + summary["wrong_singleton"]
            )
            self.assertEqual(
                summary["population_bound_holds"], summary["population_noncoverage"] <= alpha
            )
            self.assertTrue(summary["population_bound_holds"])
            self.assertEqual(summary["target_bound_holds"], summary["target_noncoverage"] <= alpha)
            if summary["singleton"]:
                self.assertEqual(
                    summary["conditional_wrong_singleton"],
                    [summary["wrong_singleton"] / summary["singleton"]],
                )
            else:
                self.assertEqual(summary["conditional_wrong_singleton"], [])
            population_miss = Fraction(0)
            target_miss = Fraction(0)
            for row in fixture["count_law"]:
                case = cases[summary["bound"] + "/" + row["count"]]
                missed = fixture["target"] not in case["targets"]
                population_miss += row["p"] * (not row["population_covered"])
                target_miss += row["p"] * missed
                if summary["in_premise"] and missed:
                    self.assertFalse(row["population_covered"])
            self.assertEqual(population_miss, summary["population_noncoverage"])
            self.assertEqual(target_miss, summary["target_noncoverage"])
            if summary["in_premise"]:
                self.assertLessEqual(target_miss, population_miss)
                self.assertLessEqual(summary["empty"] + summary["wrong_singleton"], alpha)
                if summary["singleton"]:
                    self.assertLessEqual(
                        summary["conditional_wrong_singleton"][0],
                        min(Fraction(1), alpha / summary["singleton"]),
                    )

    def test_prespecified_all_zero_all_one_and_distinct_selective_rule_controls(self):
        cases = {row["id"]: row for row in self.report["cases"]}
        for bound in self.protocol["density_bounds"]:
            zero = cases[bound["id"] + "/0/0"]
            all_one = cases[bound["id"] + "/4/4"]
            self.assertEqual(zero["status"], "ambiguous")
            self.assertEqual(zero["targets"], [Fraction(17, 80), Fraction(1, 4)])
            self.assertEqual(len(zero["worlds"]), 4)
            for row in zero["hypotheses"]:
                self.assertEqual(row["delta_set"], [Fraction(*pair) for pair in bound["interval"]])
            self.assertEqual(all_one["status"], "infeasible")
            self.assertEqual(all_one["targets"], [])
            self.assertEqual(all_one["worlds"], [])
        self.assertGreaterEqual(self.report["intervals"][4]["interval"][0], Fraction(5, 16))
        for fixture in self.report["fixtures"]:
            law = {row["count"]: row["p"] for row in fixture["count_law"]}
            self.assertEqual(law["0/0"], (1 - fixture["q"][1]) ** 4)
            self.assertGreaterEqual(law["0/0"], Fraction(625, 4096))
            self.assertGreater(law["0/0"], Fraction(1, 20))
            self.assertEqual(law["4/4"], fixture["q"][0] ** 4)
            self.assertTrue(0 < law["4/4"] <= Fraction(1, 256))
            # DIFFERENT reporting rule: conformal singleton only on all11.
            # It illustrates postselection, not an output of infer_records.
            wrong = law["4/4"] if fixture["eta"] == 0 else Fraction(0)
            self.assertGreaterEqual(1 - wrong, Fraction(19, 20))
            if fixture["eta"] == 0:
                self.assertEqual(wrong / law["4/4"], 1)

    def test_full_law_collision_distinct_marginal_pair_and_conditional_obstruction(self):
        fixtures = {row["id"]: row for row in self.report["fixtures"]}
        whole, membership = self.report["comparisons"]
        self.assertEqual(whole["id"], "whole_point")
        self.assertTrue(whole["q1_equal"] and whole["q2_equal"] and whole["count_law_equal"])
        self.assertEqual(membership["id"], "membership_only")
        self.assertTrue(membership["q1_equal"])
        self.assertFalse(membership["q2_equal"])
        self.assertFalse(membership["count_law_equal"])
        self.assertEqual(fixtures["flat_interior"]["q"][0], Fraction(1, 5))
        self.assertEqual(fixtures["conformal_interior"]["q"][0], Fraction(1, 5))
        obstruction = self.report["obstruction"]
        self.assertTrue(obstruction["point_equal"])
        self.assertGreater(obstruction["target_gap"], 0)
        cases = {row["id"]: row for row in self.report["cases"]}
        common_law = fixtures["flat_1"]["count_law"]
        for row in obstruction["cases"]:
            if row["both"]:
                self.assertTrue(row["target_ambiguous"])
        for row in obstruction["coverage"]:
            probability = sum(
                (
                    entry["p"]
                    for entry in common_law
                    if len(cases[row["bound"] + "/" + entry["count"]]["targets"]) == 2
                ),
                Fraction(0),
            )
            self.assertEqual(row["both_target_probability"], probability)
            self.assertEqual(
                row["bound_holds"], probability >= 1 - self.report["confidence"]["alpha"]
            )
            if row["both_in_premise"]:
                self.assertTrue(row["bound_holds"])


class QueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def test_all_sixty_canonical_packets_are_exact_detached_and_honestly_tagged(self):
        for case in self.report["cases"]:
            k1, k2 = map(int, case["count"].split("/"))
            supplied = packet(k1, k2, case["bound"])
            before = copy.deepcopy(supplied)
            result = self.study.infer_records(supplied)
            exact_tree(self, supplied, before)
            wanted = accepted(self.report, case)
            exact_tree(self, result, wanted)
            self.assertEqual(
                result["confidence"]["confidence_basis"], "fixed_iid_paired_binomial_union"
            )
            self.assertEqual(result["confidence"]["coverage_kind"], "unconditional_model_relative")
            self.assertNotIn("uncertainty_basis", result)
            result["counts"].append(9)
            result["intervals"][0][0] = Fraction(-1)
            result["confidence"]["tail_allocations"].append(Fraction(1))
            result["answer"]["worlds"].append("private")
            if result["answer"]["nuisance"]:
                result["answer"]["nuisance"][0]["delta"][0] = Fraction(-1)
            fresh = self.study.infer_records(supplied)
            exact_tree(self, fresh, wanted)
            supplied["records"][0]["bits"][0] = 7
            exact_tree(self, fresh, wanted)

    def test_symbol_reassociation_with_fresh_positional_ids_preserves_counts(self):
        original = packet(1, 3, "one")
        changed = copy.deepcopy(original)
        bits = [row["bits"] for row in reversed(changed["records"])]
        changed["records"] = [{"attempt": i + 1, "bits": list(row)} for i, row in enumerate(bits)]
        self.assertNotEqual(original, changed)
        exact_tree(self, self.study.infer_records(original), self.study.infer_records(changed))
        # Reordering rows without their required positional IDs is a different,
        # malformed packet, even though the count sufficient statistic agrees.
        changed["records"].reverse()
        with self.assertRaises(ValueError):
            self.study.infer_records(changed)

    def test_impossible_symbol_is_not_empty_inverse_and_is_detected_before_math(self):
        impossible = packet(0, 0)
        impossible["records"][0]["bits"] = [1, 0]
        impossible["records"][1]["bits"] = [0, 1]
        self.assertEqual(
            [sum(row["bits"][i] for row in impossible["records"]) for i in range(2)], [1, 1]
        )
        wanted = {
            "schema": "qr05br-record-result-v1",
            "status": "refused",
            "reason": "impossible_nested_symbol",
            "confidence": {},
            "counts": [],
            "intervals": [],
            "answer": {},
        }
        with (
            mock.patch.object(
                self.study, "_confidence", side_effect=AssertionError("confidence work")
            ),
            mock.patch.object(
                self.study, "_interval_for_count", side_effect=AssertionError("tail work")
            ),
            mock.patch.object(self.study, "_inverse", side_effect=AssertionError("inverse work")),
            mock.patch.object(self.study, "Fraction", side_effect=AssertionError("rational work")),
            mock.patch.object(self.study.math, "comb", side_effect=AssertionError("binomial work")),
        ):
            refused = self.study.infer_records(impossible)
            exact_tree(self, refused, wanted)
            refused["counts"].append(1)
            exact_tree(self, self.study.infer_records(impossible), wanted)
            later = copy.deepcopy(impossible)
            later["records"][-1]["bits"][1] = True
            with self.assertRaises(ValueError):
                self.study.infer_records(later)
            later = copy.deepcopy(impossible)
            later["records"][-1]["private"] = "world"
            with self.assertRaises(ValueError):
                self.study.infer_records(later)
        empty = self.study.infer_records(packet(4, 4))
        self.assertEqual(empty["status"], "accepted")
        self.assertEqual(empty["answer"]["status"], "infeasible")
        self.assertEqual(empty["answer"]["targets"], [])

    def test_strict_schema_native_types_quota_association_and_private_fields(self):
        class IntSubclass(int):
            pass

        class StrSubclass(str):
            pass

        class ListSubclass(list):
            pass

        class DictSubclass(dict):
            pass

        valid = packet(1, 3)
        malformed = [None, [], tuple(valid), DictSubclass(valid)]
        for key in valid:
            changed = copy.deepcopy(valid)
            del changed[key]
            malformed.append(changed)
            changed = copy.deepcopy(valid)
            changed[StrSubclass(key)] = changed.pop(key)
            malformed.append(changed)
        for key in ("schema", "protocol_id", "data_kind", "density_bound", "bound_basis"):
            for value in (None, False, 1, [], StrSubclass(valid[key]), valid[key] + "-wrong"):
                changed = copy.deepcopy(valid)
                changed[key] = value
                malformed.append(changed)
        for key, value in (
            ("world", "flat"),
            ("eta", 0),
            ("delta", [1, 1]),
            ("scale", 1),
            ("q", [[1, 4], [3, 8]]),
            ("intervals", []),
            ("counts", [1, 3]),
            ("frequency", [[1, 4], [3, 4]]),
            ("target", [1, 4]),
            ("seed", 1),
            ("alpha", [1, 20]),
            ("tail_allocations", [[1, 80]] * 4),
            ("grid_denominator", 256),
            ("quota", 4),
            ("uncertainty_basis", "external_population_bounds"),
        ):
            changed = copy.deepcopy(valid)
            changed[key] = value
            malformed.append(changed)
        for records in (
            None,
            {},
            tuple(valid["records"]),
            ListSubclass(valid["records"]),
            valid["records"][:3],
            valid["records"] + [copy.deepcopy(valid["records"][-1])],
        ):
            changed = copy.deepcopy(valid)
            changed["records"] = records
            malformed.append(changed)
        for replacement in (
            None,
            [],
            tuple(valid["records"][-1]),
            DictSubclass(valid["records"][-1]),
        ):
            changed = copy.deepcopy(valid)
            changed["records"][-1] = replacement
            malformed.append(changed)
        for field in ("attempt", "bits"):
            changed = copy.deepcopy(valid)
            del changed["records"][-1][field]
            malformed.append(changed)
            changed = copy.deepcopy(valid)
            row = changed["records"][-1]
            row[StrSubclass(field)] = row.pop(field)
            malformed.append(changed)
        for value in (True, 4.0, Fraction(4), IntSubclass(4), 0, 1, 5, 2**31):
            changed = copy.deepcopy(valid)
            changed["records"][-1]["attempt"] = value
            malformed.append(changed)
        for value in (None, (), [0], [0, 1, 1], ListSubclass([1, 1]), (1, 1), {"0": 1, "1": 1}):
            changed = copy.deepcopy(valid)
            changed["records"][-1]["bits"] = value
            malformed.append(changed)
        for value in (False, True, 1.0, Fraction(1), IntSubclass(1), "1", -1, 2, 2**31):
            changed = copy.deepcopy(valid)
            changed["records"][-1]["bits"][1] = value
            malformed.append(changed)
        changed = copy.deepcopy(valid)
        changed["records"][-1]["private"] = "world"
        malformed.append(changed)
        changed = copy.deepcopy(valid)
        changed["records"][-1] = copy.deepcopy(changed["records"][0])
        malformed.append(changed)
        with (
            mock.patch.object(
                self.study, "_confidence", side_effect=AssertionError("confidence work")
            ),
            mock.patch.object(
                self.study, "_interval_for_count", side_effect=AssertionError("tail work")
            ),
            mock.patch.object(self.study, "_inverse", side_effect=AssertionError("inverse work")),
            mock.patch.object(self.study, "Fraction", side_effect=AssertionError("rational work")),
            mock.patch.object(self.study.math, "comb", side_effect=AssertionError("binomial work")),
        ):
            for index, changed in enumerate(malformed):
                with self.subTest(index=index), self.assertRaises(ValueError):
                    self.study.infer_records(changed)

    def test_accepted_queries_do_not_read_files_engines_or_prior_results(self):
        supplied = packet(0, 0, "half")
        case = next(row for row in self.report["cases"] if row["id"] == "half/0/0")
        with (
            mock.patch.object(
                self.study, "source_snapshot", side_effect=AssertionError("source access")
            ),
            mock.patch.object(
                self.study, "read_bounded", side_effect=AssertionError("file access")
            ),
            mock.patch.object(
                self.study, "load_engine", side_effect=AssertionError("engine access")
            ),
            mock.patch.object(self.study, "analyze", side_effect=AssertionError("analysis access")),
            mock.patch.object(Path, "read_bytes", side_effect=AssertionError("path access")),
            mock.patch("builtins.open", side_effect=AssertionError("open access")),
        ):
            exact_tree(self, self.study.infer_records(supplied), accepted(self.report, case))
        for k in range(5):
            exact_tree(
                self, self.study._interval_for_count(k), self.report["intervals"][k]["interval"]
            )


def fixture_snapshot(study):
    snapshot = {name: ("synthetic:" + name).encode() for name in study.SOURCE_PATHS}
    snapshot["protocol.json"] = (HERE / "protocol.json").read_bytes()
    snapshot[study.UTILITY_SOURCE] = study.UTILITY_BYTES
    return snapshot


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_authenticated_fresh_utility_aliases_eleven_sources_and_owned_defaults(self):
        study, other = self.study, load_study()
        self.assertIsNot(study.UTILITY, other.UTILITY)
        self.assertEqual(hashlib.sha256(study.UTILITY_BYTES).hexdigest(), study.UTILITY_SHA256)
        self.assertEqual(study.ROOT, HERE)
        self.assertNotEqual(study.UTILITY.ROOT, HERE)
        for name in (
            "read_bounded",
            "strict_loads",
            "canonical",
            "encode",
            "decode",
            "require_equal",
            "identities",
            "_analysis_deadline",
            "_write_new",
        ):
            self.assertIs(getattr(study, name), getattr(study.UTILITY, name))
        for name in ("analyze", "freeze", "capture", "replay"):
            self.assertIsNot(getattr(study, name), getattr(study.UTILITY, name))
        self.assertEqual(study.capture.__defaults__, (HERE / "source-freeze.json",))
        self.assertEqual(study.replay.__defaults__, (HERE / "source-freeze.json",))
        snapshot = study.source_snapshot()
        self.assertEqual(len(snapshot), 11)
        self.assertEqual(set(snapshot), set(study.SOURCE_PATHS))
        self.assertEqual(snapshot[study.UTILITY_SOURCE], study.UTILITY_BYTES)
        self.assertNotIn("results.json", snapshot)
        with mock.patch.object(study, "read_bounded", wraps=study.read_bounded) as reader:
            study.source_snapshot()
        self.assertEqual(
            reader.call_args_list,
            [
                mock.call(
                    study.ROOT / name,
                    study.SOURCE_LIMIT,
                )
                for name in study.SOURCE_PATHS
            ],
        )
        with tempfile.TemporaryDirectory(prefix="qr05br-utility-") as directory:
            path = Path(directory) / "utility.py"
            path.write_bytes(b"raise AssertionError('untrusted source executed')\n")
            with self.assertRaises(ValueError):
                study._load_utilities(path)
            path.write_bytes(study.UTILITY_BYTES)
            blob, module = study._load_utilities(path)
            self.assertEqual(blob, study.UTILITY_BYTES)
            self.assertIsNot(module, study.UTILITY)
            link = Path(directory) / "link"
            link.symlink_to(path)
            with self.assertRaises(ValueError):
                study._load_utilities(link)
        original = study.read_bounded

        def changed(path, *args):
            return (
                study.UTILITY_BYTES + b"\n"
                if Path(path).resolve() == study.UTILITY_PATH.resolve()
                else original(path, *args)
            )

        with (
            mock.patch.object(study, "read_bounded", side_effect=changed),
            self.assertRaises(ValueError),
        ):
            study.source_snapshot()

    def test_exact_codec_types_json_and_regular_file_limits(self):
        study = self.study
        native = {
            "fraction": Fraction(1, 3),
            "zero": Fraction(0),
            "integer": 1,
            "flag": True,
            "empty": [],
        }
        exact_tree(
            self, study.decode(study.strict_loads(study.canonical(study.encode(native)))), native
        )
        for bad in (
            None,
            1.0,
            (1,),
            {"$fraction": [2, 6]},
            {"$fraction": [True, 1]},
            {"$fraction": [1, 0]},
            {"$unknown": 1},
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                study.decode(bad)
        for left, right in ((Fraction(1), 1), (True, 1), ([], ()), ({"x": 1}, {"x": 1, "y": 0})):
            with self.subTest(left=left), self.assertRaises(ValueError):
                study.require_equal(left, right)
        for blob in (b'{"a":1,"a":2}', b'{"a":1.0}', b'{"a":NaN}', b"\xff"):
            with self.subTest(blob=blob), self.assertRaises(ValueError):
                study.strict_loads(blob)
        with tempfile.TemporaryDirectory(prefix="qr05br-read-") as directory:
            path = Path(directory) / "small"
            path.write_bytes(b"1234")
            self.assertEqual(study.read_bounded(path, 4), b"1234")
            for limit in (3, 0, -1, True, study.ARTIFACT_LIMIT + 1):
                with self.subTest(limit=limit), self.assertRaises(ValueError):
                    study.read_bounded(path, limit)
            with mock.patch.object(study, "ARTIFACT_LIMIT", 1):
                self.assertEqual(study.read_bounded(path, 4), b"1234")
            with (
                mock.patch.object(study.UTILITY, "ARTIFACT_LIMIT", 3),
                self.assertRaises(ValueError),
            ):
                study.read_bounded(path, 4)
            link = Path(directory) / "link"
            link.symlink_to(path)
            for target in (link, Path(directory), Path(directory) / "missing"):
                with self.subTest(target=target), self.assertRaises(ValueError):
                    study.read_bounded(target)

    def test_protocol_pin_native_contract_and_fresh_separate_engine_inputs(self):
        study = self.study
        snapshot = fixture_snapshot(study)
        changed = {**snapshot, "protocol.json": snapshot["protocol.json"] + b"\n"}
        with (
            mock.patch.object(study, "strict_loads", side_effect=AssertionError("early parse")),
            self.assertRaises(ValueError),
        ):
            study._protocol(changed)
        changed_protocol = json.loads(snapshot["protocol.json"])
        changed_protocol["quota"] = True
        changed["protocol.json"] = study.canonical(changed_protocol)
        with (
            mock.patch.object(
                study, "PROTOCOL_SHA256", hashlib.sha256(changed["protocol.json"]).hexdigest()
            ),
            self.assertRaises(ValueError),
        ):
            study._protocol(changed)
        seen = []

        def collect(protocol):
            seen.append(protocol)
            return {"value": Fraction(1, 3)}

        module = type("Synthetic", (), {"analyze": staticmethod(collect)})
        with (
            mock.patch.object(study, "source_snapshot", return_value=snapshot),
            mock.patch.object(study, "load_engine", return_value=module) as loader,
        ):
            exact_tree(self, study.analyze(), {"value": Fraction(1, 3)})
        self.assertIsNot(seen[0], seen[1])
        self.assertIsNot(seen[0]["fixtures"], seen[1]["fixtures"])
        self.assertEqual(
            loader.call_args_list,
            [
                mock.call(snapshot["primary.py"], "primary"),
                mock.call(snapshot["reference.py"], "reference"),
            ],
        )
        blob = b"def analyze(protocol):\n return {'value': 1}\n"
        with mock.patch.dict(sys.modules, {"probe": object()}):
            first, second = study.load_engine(blob, "probe"), study.load_engine(blob, "probe")
        self.assertIsNot(first, second)
        self.assertEqual(first.analyze({}), {"value": 1})

    def test_both_route_input_mutations_native_mismatch_and_late_source_changes(self):
        study = self.study
        snapshot = fixture_snapshot(study)

        def good(_protocol):
            return {"value": Fraction(1)}

        def mutate(protocol):
            protocol["quota"] = True
            return good(protocol)

        routes = ((good, mutate), (mutate, good), (good, lambda _: {"value": 1}))
        for functions in routes:
            modules = [
                type("Synthetic", (), {"analyze": staticmethod(function)}) for function in functions
            ]
            with (
                mock.patch.object(study, "source_snapshot", return_value=snapshot),
                mock.patch.object(study, "load_engine", side_effect=modules),
                self.assertRaises(ValueError),
            ):
                study.analyze()
        module = type("Synthetic", (), {"analyze": staticmethod(good)})
        with (
            mock.patch.object(
                study,
                "source_snapshot",
                side_effect=[snapshot, {**snapshot, "reference.py": b"changed"}],
            ),
            mock.patch.object(study, "load_engine", return_value=module),
            self.assertRaises(ValueError),
        ):
            study.analyze()

    def test_complete_retained_report_mutations_are_detected(self):
        _study, _protocol, report = evaluated()
        for key in report:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.study.require_equal(report, {**report, key: "corrupted"})
        for path, replacement in (
            (("geometries", 0, "mass_coefficients", 0, 0), Fraction(0)),
            (("geometries", 0, "strict_support"), 1),
            (("counts", -1, "nested_nonempty"), 1),
            (("cases", -1, "hypotheses", -1, "status"), "feasible"),
            (("support", "possible_words"), 1),
            (("tails", -1, "plus"), Fraction(0)),
            (("intervals", 0, "lower", "kind"), "tail"),
            (("fixtures", -1, "count_law", -1, "p"), Fraction(0)),
            (("summaries", -1, "population_noncoverage"), Fraction(1)),
        ):
            changed = copy.deepcopy(report)
            node = changed
            for field in path[:-1]:
                node = node[field]
            node[path[-1]] = replacement
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.study.require_equal(report, changed)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()
        self.snapshot = fixture_snapshot(self.study)
        self.small = {"value": Fraction(1, 3), "count": 1, "flag": True}
        self.directory = tempfile.TemporaryDirectory(prefix="qr05br-evidence-")
        self.addCleanup(self.directory.cleanup)
        self.freeze_path = Path(self.directory.name) / "freeze.json"
        self.capture_path = Path(self.directory.name) / "capture.json"
        for name, value in (("source_snapshot", self.snapshot), ("analyze", self.small)):
            patcher = mock.patch.object(self.study, name, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def captured(self):
        self.study.freeze(self.freeze_path)
        self.study.capture(self.capture_path, self.freeze_path)

    def test_owned_schemas_exclusive_roundtrip_and_no_old_wrappers(self):
        for name in ("analyze", "estimate", "freeze", "capture", "replay"):
            patcher = mock.patch.object(
                self.study.UTILITY, name, side_effect=AssertionError("old wrapper")
            )
            patcher.start()
            self.addCleanup(patcher.stop)
        self.captured()
        exact_tree(self, self.study.replay(self.capture_path, self.freeze_path), self.small)
        freeze = json.loads(self.freeze_path.read_bytes())
        capture = json.loads(self.capture_path.read_bytes())
        self.assertEqual(freeze["schema"], "qr05br-source-freeze-v1")
        self.assertEqual(capture["schema"], "qr05br-capture-v1")
        self.assertEqual(len(freeze["sources"]), 11)
        self.assertEqual(
            capture["freeze_sha256"], hashlib.sha256(self.freeze_path.read_bytes()).hexdigest()
        )
        retained = self.capture_path.read_bytes()
        for operation, path in (
            (self.study.freeze, self.freeze_path),
            (self.study.capture, self.capture_path),
        ):
            with self.assertRaises(FileExistsError):
                operation(path)
        self.assertEqual(self.capture_path.read_bytes(), retained)

    def test_tampered_canonical_capture_and_freeze_are_rejected(self):
        self.captured()
        study = self.study
        original_read = study.read_bounded
        for path, mutations in (
            (
                self.capture_path,
                (
                    ("schema", "qr05bn-capture-v1"),
                    ("freeze_sha256", "0" * 64),
                    ("report", {"value": {"$fraction": [2, 3]}, "count": 1, "flag": True}),
                    ("report", {"value": {"$fraction": [1, 3]}, "count": True, "flag": True}),
                    ("sources", {}),
                ),
            ),
            (
                self.freeze_path,
                (
                    ("schema", "qr05bn-source-freeze-v1"),
                    ("sources", {}),
                    (
                        "runtime",
                        {"implementation": "CPython", "version": "3", "optimization": True},
                    ),
                ),
            ),
        ):
            retained = path.read_bytes()
            value = study.strict_loads(retained)
            blobs = [study.canonical({**value, key: replacement}) for key, replacement in mutations]
            blobs += [retained + b"\n", b'{"schema":1,"schema":2}']
            for blob in blobs:

                def read(target, *args, injected=blob, selected=path):
                    return injected if Path(target) == selected else original_read(target, *args)

                with (
                    self.subTest(path=path.name, blob=blob[:60]),
                    mock.patch.object(study, "read_bounded", side_effect=read),
                    self.assertRaises(ValueError),
                ):
                    study.replay(self.capture_path, self.freeze_path)
            self.assertEqual(path.read_bytes(), retained)

    def test_capture_preserves_failed_evidence_and_checks_final_freeze_bytes(self):
        study = self.study
        study.freeze(self.freeze_path)
        retained = self.freeze_path.read_bytes()

        def change_before_write():
            self.freeze_path.write_bytes(retained + b"\n")
            return self.small

        with (
            mock.patch.object(study, "analyze", side_effect=change_before_write),
            self.assertRaises(ValueError),
        ):
            study.capture(self.capture_path, self.freeze_path)
        self.assertFalse(self.capture_path.exists())
        self.freeze_path.write_bytes(retained)
        original_write = study._write_new

        def change_after_write(path, blob):
            original_write(path, blob)
            self.freeze_path.write_bytes(retained + b"\n")

        with (
            mock.patch.object(study, "_write_new", side_effect=change_after_write),
            self.assertRaises(ValueError),
        ):
            study.capture(self.capture_path, self.freeze_path)
        self.assertTrue(self.capture_path.exists())

    def test_replay_rechecks_capture_freeze_and_native_report_after_work(self):
        self.captured()
        study = self.study
        for path in (self.capture_path, self.freeze_path):
            original = path.read_bytes()

            def mutate(selected=path, blob=original):
                selected.write_bytes(blob + b"\n")
                return self.small

            with (
                mock.patch.object(study, "analyze", side_effect=mutate),
                self.assertRaises(ValueError),
            ):
                study.replay(self.capture_path, self.freeze_path)
            path.write_bytes(original)
        with (
            mock.patch.object(study, "analyze", return_value={**self.small, "count": True}),
            self.assertRaises(ValueError),
        ):
            study.replay(self.capture_path, self.freeze_path)

    def test_freeze_rechecks_bytes_after_final_source_check(self):
        calls = []

        def source_check(snapshot):
            self.assertEqual(snapshot, self.snapshot)
            calls.append(1)
            if len(calls) == 2:
                self.freeze_path.write_bytes(self.freeze_path.read_bytes() + b"\n")

        with (
            mock.patch.object(self.study, "_check_snapshot", side_effect=source_check),
            self.assertRaises(ValueError),
        ):
            self.study.freeze(self.freeze_path)
        self.assertEqual(len(calls), 2)
        self.assertTrue(self.freeze_path.exists())


class DeadlineTests(unittest.TestCase):
    def test_earlier_outer_deadline_is_forwarded_and_restored(self):
        study = load_study()
        utility = study.UTILITY
        previous = mock.Mock(side_effect=KeyboardInterrupt("outer deadline"))
        with (
            mock.patch.object(utility.signal, "getsignal", return_value=previous),
            mock.patch.object(utility.signal, "getitimer", return_value=(5.0, 0.0)),
            mock.patch.object(utility.signal, "signal") as handlers,
            mock.patch.object(utility.signal, "setitimer") as timers,
            mock.patch.object(utility.time, "monotonic", side_effect=[0.0, 2.0]),
            self.assertRaises(KeyboardInterrupt),
            study._analysis_deadline(),
        ):
            handlers.call_args_list[0].args[1](utility.signal.SIGALRM, None)
        previous.assert_called_once_with(utility.signal.SIGALRM, None)
        self.assertEqual(timers.call_args_list[0], mock.call(utility.signal.ITIMER_REAL, 5.0))
        self.assertEqual(timers.call_args_list[-1], mock.call(utility.signal.ITIMER_REAL, 3.0, 0.0))


if __name__ == "__main__":
    import signal

    def suite_expired(_signum, _frame):
        raise KeyboardInterrupt("QR-05BR 120-second suite deadline")

    signal.signal(signal.SIGALRM, suite_expired)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
