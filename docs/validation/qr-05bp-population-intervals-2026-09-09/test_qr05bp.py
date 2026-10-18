"""Independent BP endpoint/breakpoint oracle and mathematical query tests.

No mathematical code runs at import. The integration/deadline tail is
owned separately by the root author. Historical engines are never imported.
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
    spec = importlib.util.spec_from_file_location("_qr05bp_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load BP driver")
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


def data_oracle(protocol):
    points = {row["id"]: [Fraction(*pair) for pair in row["q"]] for row in protocol["points"]}
    data = [
        {
            "id": row["id"],
            "intervals": [[value, value] for value in points[row["id"]]],
            "nested_nonempty": points[row["id"]][0] <= points[row["id"]][1],
        }
        for row in protocol["points"]
    ]
    for row in protocol["boxes"]:
        if "center" in row:
            radius = Fraction(*row["radius"])
            intervals = [[value - radius, value + radius] for value in points[row["center"]]]
        else:
            intervals = [[Fraction(*pair) for pair in interval] for interval in row["intervals"]]
        data.append(
            {
                "id": row["id"],
                "intervals": intervals,
                "nested_nonempty": intervals[0][0] <= intervals[1][1],
            }
        )
    return data


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


def inclusion_row(left, right):
    broad = {row["id"]: row["delta_set"] for row in right["hypotheses"]}
    return {
        "world_subset": set(left["worlds"]).issubset(right["worlds"]),
        "target_subset": set(left["targets"]).issubset(right["targets"]),
        "nuisance_subset": all(
            interval_subset(row["delta_set"], broad[row["id"]]) for row in left["hypotheses"]
        ),
    }


def ratio_polynomial_equal(left_numerator, left_denominator, right_numerator, right_denominator):
    def product(left, right):
        return [left[0] * right[0], left[0] * right[1] + left[1] * right[0], left[1] * right[1]]

    return product(left_numerator, right_denominator) == product(right_numerator, left_denominator)


def expected(protocol):
    geometries = [geometry_oracle(item, protocol) for item in protocol["geometries"]]
    by_geometry = {row["id"]: row for row in geometries}
    data = data_oracle(protocol)
    cases = []
    for bound in protocol["density_bounds"]:
        domain = [Fraction(*pair) for pair in bound["interval"]]
        for datum in data:
            rows = [hypothesis(geometry, datum, domain) for geometry in geometries]
            worlds = [row["id"] for row in rows if row["delta_set"]]
            targets = sorted({by_geometry[name]["target"] for name in worlds})
            cases.append(
                {
                    "id": bound["id"] + "/" + datum["id"],
                    "bound": bound["id"],
                    "data": datum["id"],
                    "intervals": datum["intervals"],
                    "nested_nonempty": datum["nested_nonempty"],
                    "hypotheses": rows,
                    "worlds": worlds,
                    "targets": targets,
                    "status": "infeasible"
                    if not worlds
                    else "identified"
                    if len(targets) == 1
                    else "ambiguous",
                }
            )
    by_case = {row["id"]: row for row in cases}
    density_monotonicity = []
    for tight, broad in itertools.pairwise(protocol["density_bounds"]):
        for datum in data:
            density_monotonicity.append(
                {
                    "tight": tight["id"],
                    "broad": broad["id"],
                    "data": datum["id"],
                    **inclusion_row(
                        by_case[tight["id"] + "/" + datum["id"]],
                        by_case[broad["id"] + "/" + datum["id"]],
                    ),
                }
            )
    box_monotonicity = []
    for tight, broad in protocol["box_inclusions"]:
        for bound in protocol["density_bounds"]:
            box_monotonicity.append(
                {
                    "tight": tight,
                    "broad": broad,
                    "bound": bound["id"],
                    **inclusion_row(
                        by_case[bound["id"] + "/" + tight], by_case[bound["id"] + "/" + broad]
                    ),
                }
            )
    scale_pairs = []
    for first, second in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        a, b = by_geometry[first], by_geometry[second]
        factors = [right / left for left, right in zip(a["volumes"], b["volumes"], strict=True)]
        if len(set(factors)) != 1:
            raise ValueError("unequal region scale factors")
        nuisance_equal = True
        laws_equal = True
        for case in cases:
            left, right = [
                next(row for row in case["hypotheses"] if row["id"] == name)
                for name in (first, second)
            ]
            nuisance_equal = nuisance_equal and left["delta_set"] == right["delta_set"]
            if bool(left["curve"]) != bool(right["curve"]):
                laws_equal = False
            elif left["curve"]:
                laws_equal = laws_equal and all(
                    ratio_polynomial_equal(
                        nl, left["curve"]["denominator"], nr, right["curve"]["denominator"]
                    )
                    for nl, nr in zip(
                        left["curve"]["one_point_numerators"],
                        right["curve"]["one_point_numerators"],
                        strict=True,
                    )
                )
        scale_pairs.append(
            {
                "worlds": [first, second],
                "volume_factor": factors[0],
                "target_equal": a["target"] == b["target"],
                "nuisance_sets_equal": nuisance_equal,
                "curve_laws_equal": laws_equal,
            }
        )
    flat, conformal = by_geometry["flat"], by_geometry["conformal"]
    q = probabilities(flat["mass_coefficients"], Fraction(1))
    other_q = probabilities(conformal["mass_coefficients"], Fraction(0))
    normalized = []
    for item, delta in ((flat, Fraction(1)), (conformal, Fraction(0))):
        eta, scale = item["eta"], item["scale"]
        normalization = at(item["mass_coefficients"][0], delta)
        normalized.append(
            [
                Fraction(scale, 2) / normalization,
                Fraction(scale, 2) * (eta + delta) / normalization,
                Fraction(scale, 2) * eta * delta / normalization,
            ]
        )
    if q != other_q:
        raise ValueError("prespecified whole-point obstruction lost paired probabilities")
    obstruction_cases = []
    for case in cases:
        left, right = [
            next(row for row in case["hypotheses"] if row["id"] == name)["delta_set"]
            for name in ("flat", "conformal")
        ]
        flat_present = bool(left) and left[0] <= 1 <= left[1]
        conformal_present = bool(right) and right[0] <= 0 <= right[1]
        obstruction_cases.append(
            {
                "case": case["id"],
                "flat_present": flat_present,
                "conformal_present": conformal_present,
                "both": flat_present and conformal_present,
                "target_ambiguous": case["status"] == "ambiguous",
            }
        )
    return {
        "schema": "qr05bp-report-v1",
        "geometries": geometries,
        "data": data,
        "cases": cases,
        "density_monotonicity": density_monotonicity,
        "box_monotonicity": box_monotonicity,
        "scale_pairs": scale_pairs,
        "obstruction": {
            "worlds": ["flat", "conformal"],
            "deltas": [Fraction(1), Fraction(0)],
            "q": q,
            "point_equal": normalized[0] == normalized[1],
            "target_gap": flat["target"] - conformal["target"],
            "cases": obstruction_cases,
        },
        "support": {
            "quota": protocol["quota"],
            "symbols": [[0, 0], [0, 1], [1, 0], [1, 1]],
            "allowed": [[0, 0], [0, 1], [1, 1]],
            "possible_words": 3 ** protocol["quota"],
            "zero_words": 4 ** protocol["quota"] - 3 ** protocol["quota"],
            "continuous_certificate": all(row["strict_support"] for row in geometries),
        },
    }


def query(intervals, bound="two"):
    return {
        "schema": "qr05bp-query-v1",
        "data_kind": "population_intervals",
        "intervals": [
            [[value.numerator, value.denominator] for value in interval] for interval in intervals
        ],
        "density_bound": bound,
        "bound_basis": "external_assumption",
        "uncertainty_basis": "external_population_bounds",
    }


def query_answer(case):
    return {
        "nested_nonempty": case["nested_nonempty"],
        "worlds": case["worlds"],
        "targets": case["targets"],
        "status": case["status"],
        "nuisance": [
            {"id": row["id"], "delta": row["delta_set"]}
            for row in case["hypotheses"]
            if row["delta_set"]
        ],
    }


class MathematicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.cases = {row["id"]: row for row in cls.report["cases"]}

    def test_complete_native_report_and_exact_finite_inventory(self):
        exact_tree(self, self.report, expected(self.protocol))
        self.assertEqual(len(self.report["geometries"]), 4)
        self.assertEqual(len(self.report["data"]), 23)
        self.assertEqual(len(self.report["cases"]), 92)
        self.assertEqual(sum(len(row["hypotheses"]) for row in self.report["cases"]), 368)
        self.assertEqual(len(self.report["density_monotonicity"]), 69)
        self.assertEqual(len(self.report["box_monotonicity"]), 48)
        self.assertEqual(len(self.report["obstruction"]["cases"]), 92)
        self.assertNotIn("records", self.report)

    def test_affine_geometry_support_and_all_raw_scale_factors(self):
        geometries = {row["id"]: row for row in self.report["geometries"]}
        for row in geometries.values():
            denominator = row["mass_coefficients"][0]
            self.assertTrue(all(value < 0 for value in row["derivative_numerators"]))
            self.assertTrue(all(at(denominator, Fraction(delta)) > 0 for delta in (0, 2)))
            self.assertIs(row["strict_support"], True)
            for category in row["category_coefficients"]:
                self.assertGreater(at(category, Fraction(0)), 0)
                self.assertGreater(at(category, Fraction(2)), 0)
        for pair in self.report["scale_pairs"]:
            first, second = [geometries[name] for name in pair["worlds"]]
            self.assertEqual(second["volumes"], [4 * value for value in first["volumes"]])
            self.assertEqual(
                second["mass_coefficients"],
                [[4 * value for value in row] for row in first["mass_coefficients"]],
            )
            self.assertEqual(
                second["derivative_numerators"],
                [16 * value for value in first["derivative_numerators"]],
            )
            self.assertEqual(pair["volume_factor"], Fraction(4))
            self.assertTrue(
                pair["target_equal"] and pair["nuisance_sets_equal"] and pair["curve_laws_equal"]
            )
        self.assertEqual(self.report["support"]["possible_words"], 81)
        self.assertEqual(self.report["support"]["zero_words"], 175)
        self.assertIs(self.report["support"]["continuous_certificate"], True)

    def test_every_curve_uses_one_shared_parameter_and_closed_endpoints(self):
        for case in self.report["cases"]:
            for row in case["hypotheses"]:
                if not row["delta_set"]:
                    self.assertEqual(row["curve"], {})
                    continue
                curve = row["curve"]
                self.assertEqual(curve["domain"], row["delta_set"])
                self.assertEqual(len(curve["endpoints"]), 2)
                self.assertEqual(
                    [endpoint["delta"] for endpoint in curve["endpoints"]], row["delta_set"]
                )
                self.assertEqual(curve["one_point_numerators"][2], [Fraction(0), Fraction(0)])
                for endpoint in curve["endpoints"]:
                    denominator = at(curve["denominator"], endpoint["delta"])
                    paired = [
                        at(numerator, endpoint["delta"]) / denominator
                        for numerator in curve["numerators"]
                    ]
                    self.assertEqual(endpoint["q"], paired)
                    self.assertEqual(
                        endpoint["one_point"],
                        [1 - paired[1], paired[1] - paired[0], Fraction(0), paired[0]],
                    )
                    self.assertTrue(
                        all(
                            lo <= value <= hi
                            for value, (lo, hi) in zip(paired, case["intervals"], strict=True)
                        )
                    )
                midpoint = sum(row["delta_set"]) / 2
                self.assertTrue(
                    all(
                        lo <= at(numerator, midpoint) / at(curve["denominator"], midpoint) <= hi
                        for numerator, (lo, hi) in zip(
                            curve["numerators"], case["intervals"], strict=True
                        )
                    )
                )

    def test_small_wide_inconsistent_touch_and_nonnested_controls(self):
        for name, label in (("flat", "flat"), ("conformal", "conformal")):
            small = self.cases["two/" + name + "_small"]
            wide = self.cases["two/" + name + "_wide"]
            self.assertEqual(small["status"], "identified")
            self.assertEqual(small["worlds"], [label, label + "_x4"])
            self.assertEqual(wide["status"], "ambiguous")
        inconsistent = self.cases["two/inconsistent"]
        flat = next(row for row in inconsistent["hypotheses"] if row["id"] == "flat")
        self.assertTrue(all(flat["query_sets"]))
        self.assertEqual(flat["delta_set"], [])
        self.assertEqual(inconsistent["status"], "infeasible")
        touch = self.cases["two/touch"]
        flat = next(row for row in touch["hypotheses"] if row["id"] == "flat")
        self.assertEqual(flat["delta_set"], [Fraction(1), Fraction(1)])
        self.assertEqual(flat["curve"]["endpoints"][0], flat["curve"]["endpoints"][1])
        for bound in self.protocol["density_bounds"]:
            case = self.cases[bound["id"] + "/non_nested"]
            self.assertIs(case["nested_nonempty"], False)
            self.assertEqual(case["status"], "infeasible")
            self.assertEqual(case["worlds"], [])
        self.assertIs(self.cases["two/crossing"]["nested_nonempty"], True)

    def test_zero_slope_faces_no_pole_division_and_full_domain(self):
        for bound in self.protocol["density_bounds"]:
            domain = [Fraction(*pair) for pair in bound["interval"]]
            full = self.cases[bound["id"] + "/full"]
            for row in full["hypotheses"]:
                self.assertEqual(row["delta_set"], domain)
                self.assertEqual(row["query_sets"], [domain, domain])
            pole = self.cases[bound["id"] + "/pole_band"]
            self.assertEqual(pole["status"], "infeasible")
            flat = next(row for row in pole["hypotheses"] if row["id"] == "flat")
            self.assertEqual(flat["inequalities"][0]["slope"], Fraction(0))
            self.assertEqual(flat["inequalities"][1]["slope"], Fraction(0))
            self.assertEqual([row["kind"] for row in flat["inequalities"][:2]], ["all", "none"])
            self.assertEqual([row["boundary"] for row in flat["inequalities"][:2]], [[], []])

    def test_set_inclusions_keep_every_nuisance_and_obstruction_direction(self):
        for collection in ("density_monotonicity", "box_monotonicity"):
            for row in self.report[collection]:
                self.assertIs(row["world_subset"], True)
                self.assertIs(row["target_subset"], True)
                self.assertIs(row["nuisance_subset"], True)
        obstruction = self.report["obstruction"]
        self.assertIs(obstruction["point_equal"], True)
        self.assertEqual(obstruction["target_gap"], Fraction(3, 80))
        for row in obstruction["cases"]:
            self.assertEqual(row["both"], row["flat_present"] and row["conformal_present"])
            if row["both"]:
                self.assertIs(row["target_ambiguous"], True)
        # Wide membership-only boxes demonstrate that ambiguity does not imply
        # admission of this particular compensated point pair.
        for name in ("two/flat_wide", "two/conformal_wide"):
            row = next(row for row in obstruction["cases"] if row["case"] == name)
            self.assertIs(row["target_ambiguous"], True)
            self.assertIs(row["both"], False)

    def test_zero_width_projections_recover_authenticated_stored_bo_cases(self):
        previous = self.study._previous_report(self.study.source_snapshot())
        self.assertEqual(self.study._verify_point_recovery(self.report, previous), 48)
        self.assertEqual(len(previous["cases"]), 48)
        for old in previous["cases"]:
            current = self.cases[old["id"]]
            for field in ("id", "bound", "data", "worlds", "targets", "status"):
                exact_tree(self, current[field], old[field])
            exact_tree(self, current["intervals"], [[value, value] for value in old["q"]])
            self.assertIs(current["nested_nonempty"], True)
            self.assertEqual(len(current["hypotheses"]), len(old["hypotheses"]))
            for new_row, old_row in zip(current["hypotheses"], old["hypotheses"], strict=True):
                self.assertEqual(new_row["id"], old_row["id"])
                wanted = (
                    [old_row["delta_set"][0], old_row["delta_set"][0]]
                    if old_row["delta_set"]
                    else []
                )
                exact_tree(self, new_row["delta_set"], wanted)
                self.assertEqual(new_row["status"], old_row["status"])


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_all_declared_queries_match_complete_cases_and_are_detached(self):
        _study, _protocol, report = evaluated()
        for case in report["cases"]:
            supplied = query(case["intervals"], case["bound"])
            saved = copy.deepcopy(supplied)
            wanted = query_answer(case)
            returned = self.study.identify(supplied)
            exact_tree(self, returned, wanted)
            self.assertEqual(supplied, saved)
            returned["worlds"].append("changed")
            returned["targets"].append(Fraction(99))
            if returned["nuisance"]:
                returned["nuisance"][0]["delta"][0] = Fraction(99)
            exact_tree(self, self.study.identify(supplied), wanted)
            supplied["intervals"][0][0][0] += 1
            self.assertEqual(saved, query(case["intervals"], case["bound"]))

    def test_two_prescribed_nonfixture_point_queries(self):
        _study, protocol, report = evaluated()
        fixed = [row["intervals"] for row in report["data"]]
        for eta in (0, 1):
            delta = Fraction(1, 3)
            masses = mass_coefficients(protocol, eta, 1)
            paired = probabilities(masses, delta)
            intervals = [[value, value] for value in paired]
            self.assertNotIn(intervals, fixed)
            names = ["flat", "flat_x4"] if eta == 0 else ["conformal", "conformal_x4"]
            exact_tree(
                self,
                self.study.identify(query(intervals, "half")),
                {
                    "nested_nonempty": True,
                    "worlds": names,
                    "targets": [Fraction(16 + eta, 16 * (4 + eta))],
                    "status": "identified",
                    "nuisance": [{"id": name, "delta": [delta, delta]} for name in names],
                },
            )

    def test_wholly_nonnested_is_valid_empty_and_partial_crossing_is_admitted(self):
        nonnested = [[Fraction(3, 4), Fraction(1)], [Fraction(0), Fraction(1, 4)]]
        exact_tree(
            self,
            self.study.identify(query(nonnested)),
            {
                "nested_nonempty": False,
                "worlds": [],
                "targets": [],
                "status": "infeasible",
                "nuisance": [],
            },
        )
        crossing = [[Fraction(1, 5), Fraction(2, 5)], [Fraction(3, 10), Fraction(1, 2)]]
        result = self.study.identify(query(crossing))
        self.assertIs(result["nested_nonempty"], True)
        self.assertTrue(result["worlds"])

    def test_strict_six_field_schema_and_all_nested_container_types(self):
        class DictChild(dict):
            pass

        class ListChild(list):
            pass

        class IntChild(int):
            pass

        class StringChild(str):
            pass

        base = query([[Fraction(0), Fraction(1)], [Fraction(0), Fraction(1)]])
        bad = [None, [], DictChild(base), {StringChild(k): v for k, v in base.items()}]
        for key in base:
            changed = copy.deepcopy(base)
            del changed[key]
            bad.append(changed)
        for key, value in (
            ("schema", "qr05bo-query-v1"),
            ("data_kind", "sample_frequency"),
            ("uncertainty_basis", "estimated_from_records"),
            ("bound_basis", "calibrated_from_records"),
            ("density_bound", "three"),
            ("schema", StringChild(base["schema"])),
            ("data_kind", StringChild(base["data_kind"])),
            ("density_bound", StringChild("two")),
            ("bound_basis", True),
            ("uncertainty_basis", StringChild(base["uncertainty_basis"])),
        ):
            bad.append({**copy.deepcopy(base), key: value})
        intervals = [
            [],
            [[[0, 1], [1, 1]]],
            ([[0, 1], [1, 1]], [[0, 1], [1, 1]]),
            ListChild(copy.deepcopy(base["intervals"])),
            [ListChild([[0, 1], [1, 1]]), [[0, 1], [1, 1]]],
            [[[0, 1], [1, 1]], [[0, 1], ListChild([1, 1])]],
            [[[0, 1], [1, 1]], [[0, 1], (1, 1)]],
            [[[0, 1], [1, 1]], [[0, 1], [True, 1]]],
            [[[0, 1], [1, 1]], [[0, 1], [IntChild(1), 1]]],
            [[[0, 1], [1, 1]], [[0, 1], [1.0, 1]]],
            [[[0, 1], [1, 1]], [[0, 1], ["1", 1]]],
            [[[0, 2], [1, 1]], [[0, 1], [1, 1]]],
            [[[0, 1], [2, 2]], [[0, 1], [1, 1]]],
            [[[0, 1], [1, 0]], [[0, 1], [1, 1]]],
            [[[0, 1], [1, -1]], [[0, 1], [1, 1]]],
            [[[1, 1], [0, 1]], [[0, 1], [1, 1]]],
            [[[-1, 1], [1, 1]], [[0, 1], [1, 1]]],
            [[[0, 1], [2, 1]], [[0, 1], [1, 1]]],
            [[[0, 1], [1, 1]], [[0, 1], [2**31, 2**31 + 1]]],
        ]
        for value in intervals:
            bad.append({**copy.deepcopy(base), "intervals": value})
        for name in (
            "records",
            "frequency",
            "count",
            "quota",
            "actual_world",
            "eta",
            "delta",
            "state",
            "coordinates",
            "extra",
        ):
            bad.append({**copy.deepcopy(base), name: 0})
        for index, supplied in enumerate(bad):
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.study.identify(supplied)

    def test_complete_input_cap_before_gcd_and_file_engine_blind_queries(self):
        base = query([[Fraction(0), Fraction(1)], [Fraction(0), Fraction(1)]])
        base["intervals"][1][1] = [2**1000, 2**1000 + 1]
        with (
            mock.patch.object(self.study.math, "gcd", side_effect=AssertionError("early gcd")),
            self.assertRaises(ValueError),
        ):
            self.study.identify(base)
        with (
            mock.patch.object(self.study, "read_bounded", side_effect=AssertionError("file")),
            mock.patch.object(
                self.study, "source_snapshot", side_effect=AssertionError("snapshot")
            ),
            mock.patch.object(self.study, "load_engine", side_effect=AssertionError("engine")),
            mock.patch.object(self.study, "analyze", side_effect=AssertionError("analysis")),
            mock.patch.object(
                self.study.UTILITY, "analyze", side_effect=AssertionError("old analysis")
            ),
        ):
            result = self.study.identify(
                query([[Fraction(0), Fraction(1)], [Fraction(0), Fraction(1)]])
            )
            self.assertEqual(result["worlds"], ["flat", "conformal", "flat_x4", "conformal_x4"])
            capped = self.study.identify(
                query(
                    [[Fraction(0), Fraction(0)], [Fraction(1, 2147483647), Fraction(1, 2147483647)]]
                )
            )
            exact_tree(
                self,
                capped,
                {
                    "nested_nonempty": True,
                    "worlds": [],
                    "targets": [],
                    "status": "infeasible",
                    "nuisance": [],
                },
            )


def fixture_snapshot(study):
    snapshot = {name: ("synthetic:" + name).encode() for name in study.SOURCE_PATHS}
    snapshot["protocol.json"] = (HERE / "protocol.json").read_bytes()
    snapshot[study.UTILITY_SOURCE] = study.UTILITY_BYTES
    snapshot[study.PRIOR_SOURCE] = (HERE / study.PRIOR_SOURCE).read_bytes()
    return snapshot


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_authenticated_fresh_utility_aliases_ten_sources_and_owned_defaults(self):
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
        self.assertEqual(len(snapshot), 10)
        self.assertEqual(set(snapshot), set(study.SOURCE_PATHS))
        self.assertEqual(snapshot[study.UTILITY_SOURCE], study.UTILITY_BYTES)
        self.assertNotIn("results.json", snapshot)
        self.assertIn(study.PRIOR_SOURCE, snapshot)
        self.assertGreater(len(snapshot[study.PRIOR_SOURCE]), study.SOURCE_LIMIT)
        with mock.patch.object(study, "read_bounded", wraps=study.read_bounded) as reader:
            study.source_snapshot()
        self.assertEqual(
            reader.call_args_list,
            [
                mock.call(
                    study.ROOT / name,
                    study.ARTIFACT_LIMIT if name == study.PRIOR_SOURCE else study.SOURCE_LIMIT,
                )
                for name in study.SOURCE_PATHS
            ],
        )
        with tempfile.TemporaryDirectory(prefix="qr05bp-utility-") as directory:
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
        with tempfile.TemporaryDirectory(prefix="qr05bp-read-") as directory:
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
            mock.patch.object(study, "_previous_report", return_value={"previous": True}),
            mock.patch.object(study, "_verify_point_recovery", return_value=48) as recover,
        ):
            exact_tree(self, study.analyze(), {"value": Fraction(1, 3)})
        recover.assert_called_once_with({"value": Fraction(1, 3)}, {"previous": True})
        self.assertIsNot(seen[0], seen[1])
        self.assertIsNot(seen[0]["points"], seen[1]["points"])
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
            mock.patch.object(study, "_previous_report", return_value={}),
            mock.patch.object(study, "_verify_point_recovery", return_value=48),
            self.assertRaises(ValueError),
        ):
            study.analyze()

    def test_prior_capture_authentication_precedes_parse_and_owned_schema(self):
        study = self.study
        snapshot = fixture_snapshot(study)
        changed = {**snapshot, study.PRIOR_SOURCE: snapshot[study.PRIOR_SOURCE] + b"\n"}
        for operation in (study._previous_report, study._protocol):
            with (
                mock.patch.object(study, "strict_loads", side_effect=AssertionError("early parse")),
                self.assertRaises(ValueError),
            ):
                operation(changed)
        artifact = study.strict_loads(snapshot[study.PRIOR_SOURCE])
        malformed = [
            study.canonical({**artifact, "schema": "qr05bp-capture-v1"}),
            study.canonical({**artifact, "extra": 1}),
            study.canonical({**artifact, "report": {"schema": "qr05bp-report-v1"}}),
            snapshot[study.PRIOR_SOURCE] + b"\n",
        ]
        for blob in malformed:
            with (
                self.subTest(blob=blob[:60]),
                mock.patch.object(study, "PRIOR_SHA256", hashlib.sha256(blob).hexdigest()),
                self.assertRaises(ValueError),
            ):
                study._previous_report({**snapshot, study.PRIOR_SOURCE: blob})

    def test_every_shared_point_projection_is_compared_after_new_engine_agreement(self):
        study, _protocol, report = evaluated()
        previous = study._previous_report(study.source_snapshot())
        self.assertEqual(study._verify_point_recovery(report, previous), 48)
        for field in (
            "bound",
            "data",
            "worlds",
            "targets",
            "status",
            "intervals",
            "nested_nonempty",
        ):
            changed = copy.deepcopy(report)
            changed["cases"][0][field] = "changed"
            with self.subTest(field=field), self.assertRaises(ValueError):
                study._verify_point_recovery(changed, previous)
        for field, value in (
            ("id", "changed"),
            ("status", "infeasible"),
            ("delta_set", [Fraction(0), Fraction(1)]),
        ):
            changed = copy.deepcopy(report)
            changed["cases"][0]["hypotheses"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                study._verify_point_recovery(changed, previous)
        changed = copy.deepcopy(report)
        changed["cases"].append(copy.deepcopy(changed["cases"][0]))
        with self.assertRaises(ValueError):
            study._verify_point_recovery(changed, previous)

    def test_complete_retained_report_mutations_are_detected(self):
        _study, _protocol, report = evaluated()
        for key in report:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.study.require_equal(report, {**report, key: "corrupted"})
        for path, replacement in (
            (("geometries", 0, "mass_coefficients", 0, 0), Fraction(0)),
            (("geometries", 0, "strict_support"), 1),
            (("data", -1, "nested_nonempty"), 1),
            (("cases", -1, "hypotheses", -1, "status"), "feasible"),
            (("support", "possible_words"), 1),
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
        self.directory = tempfile.TemporaryDirectory(prefix="qr05bp-evidence-")
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
        self.assertEqual(freeze["schema"], "qr05bp-source-freeze-v1")
        self.assertEqual(capture["schema"], "qr05bp-capture-v1")
        self.assertEqual(len(freeze["sources"]), 10)
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
        raise KeyboardInterrupt("QR-05BP 120-second suite deadline")

    signal.signal(signal.SIGALRM, suite_expired)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
