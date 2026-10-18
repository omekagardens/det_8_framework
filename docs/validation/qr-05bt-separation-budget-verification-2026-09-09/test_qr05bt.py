"""Independent BT support-normal/forward-contact mathematical tests.

Only definitions run at import. Root separately owns integration/evidence
and the final suite deadline. No historical mathematical executor is loaded.
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
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent


def load_study():
    spec = importlib.util.spec_from_file_location("_qr05bt_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load BT driver")
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


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def difference(left, right):
    return [a - b for a, b in zip(left, right, strict=True)]


def sign(value):
    return Fraction((value > 0) - (value < 0))


def at(coefficients, delta):
    return coefficients[0] + delta * coefficients[1]


def moment(rectangle, degree):
    lower_u, upper_u, lower_v, upper_v = [Fraction(*pair) for pair in rectangle]
    power = degree + 1
    return (upper_u**power - lower_u**power) * (upper_v**power - lower_v**power) / power**2


def coefficients(protocol, eta, scale):
    rows = []
    for name in ("Q", "I1", "I2"):
        values = [moment(protocol["regions"][name], degree) for degree in range(3)]
        rows.append(
            [
                Fraction(scale, 2) * (values[0] + eta * values[1]),
                Fraction(scale, 2) * (values[1] + eta * values[2]),
            ]
        )
    return rows


def forward(masses, delta):
    normalizer = at(masses[0], delta)
    if normalizer <= 0:
        raise ValueError("oracle requires a positive mass normalizer")
    return [at(row, delta) / normalizer for row in masses[1:]]


def inverse_coordinate(masses, point):
    """Recover density from a coordinate's original mass equation."""
    aq, bq = masses[0]
    candidates = []
    for value, (ai, bi) in zip(point, masses[1:], strict=True):
        divisor = value * bq - bi
        if not divisor:
            if ai - value * aq:
                raise ValueError("inconsistent constant coordinate")
            continue
        candidates.append((ai - value * aq) / divisor)
    if not candidates or any(value != candidates[0] for value in candidates):
        raise ValueError("contact did not have one shared density")
    return candidates[0]


def segment(masses, upper):
    start, end = forward(masses, Fraction(0)), forward(masses, upper)
    return {"start": start, "end": end, "vector": difference(end, start)}


def primitive_line(start, end):
    """Primitive supporting equation derived from two actual forward points."""
    vector = difference(end, start)
    normal = [vector[1], -vector[0]]
    raw = normal + [dot(normal, start)]
    denominator = math.lcm(*(value.denominator for value in raw))
    integers = [value.numerator * (denominator // value.denominator) for value in raw]
    divisor = math.gcd(*(abs(value) for value in integers))
    if not divisor:
        raise ValueError("a point has no unique supporting line")
    if integers[1] < 0:
        divisor = -divisor
    return [Fraction(value // divisor) for value in integers]


def geometry_oracle(protocol, item):
    masses = coefficients(protocol, item["eta"], item["scale"])
    derivatives = [row[1] * masses[0][0] - row[0] * masses[0][1] for row in masses[1:]]
    return {
        "id": item["id"],
        "eta": item["eta"],
        "scale": item["scale"],
        "volumes": [row[0] for row in masses],
        "mass_coefficients": masses,
        "derivative_numerators": derivatives,
        "target": masses[1][0] / masses[0][0],
        "line": primitive_line(forward(masses, Fraction(0)), forward(masses, Fraction(2))),
        "positive_normalizer": all(
            at(masses[0], value) > 0 for value in (Fraction(0), Fraction(2))
        ),
        "decreasing": all(value < 0 for value in derivatives),
    }


def fixture_oracle(item, masses):
    delta = Fraction(*item["delta"])
    values = [at(row, delta) for row in masses]
    q = forward(masses, delta)
    return {
        "id": item["id"],
        "eta": item["eta"],
        "delta": delta,
        "target": masses[1][0] / masses[0][0],
        "masses": values,
        "q": q,
        "one_point": [1 - q[1], q[1] - q[0], Fraction(0), q[0]],
    }


def contact_oracle(point, masses, upper):
    """Find the supporting-line dual optimum, then enforce the finite segment.

    Unlike the clipped-sum route, derive the line distance from its normal
    and recover the contact by equality in the dual norm inequality.
    No minimization over reference breakpoint candidates is used.
    """
    seg = segment(masses, upper)
    start, end, vector = seg["start"], seg["end"], seg["vector"]
    if upper == 0:
        raw = []
        parameter = Fraction(0)
        location = "point"
        contact = list(start)
    else:
        if any(value >= 0 for value in vector):
            raise ValueError("oracle requires the declared decreasing segments")
        normal = [vector[1], -vector[0]]
        signed_offset = dot(normal, difference(point, start))
        norm = sum(abs(value) for value in normal)
        line_distance = abs(signed_offset) / norm
        orientation = sign(signed_offset)
        saturated_residual = [orientation * sign(value) * line_distance for value in normal]
        line_contact = difference(point, saturated_residual)
        unconstrained = (line_contact[0] - start[0]) / vector[0]
        if line_contact != [a + unconstrained * v for a, v in zip(start, vector, strict=True)]:
            raise ValueError("dual saturation did not land on the supporting line")
        raw = [unconstrained]
        location = (
            "before"
            if unconstrained < 0
            else "start"
            if unconstrained == 0
            else "interior"
            if unconstrained < 1
            else "end"
            if unconstrained == 1
            else "after"
        )
        if 0 <= unconstrained <= 1:
            parameter = unconstrained
            contact = line_contact
        else:
            # With the line optimum outside the interval, the convex norm
            # is monotone on this segment and minimizes at its nearer endpoint.
            endpoint_distances = [
                max(abs(value) for value in difference(point, endpoint))
                for endpoint in (start, end)
            ]
            parameter = Fraction(0 if endpoint_distances[0] <= endpoint_distances[1] else 1)
            contact = list(start if parameter == 0 else end)
    residual = difference(point, contact)
    distance = max(abs(value) for value in residual)
    delta = Fraction(0) if upper == 0 else inverse_coordinate(masses, contact)
    if not 0 <= delta <= upper or forward(masses, delta) != contact:
        raise ValueError("nearest contact was not in the original density family")
    kind = (
        "point"
        if upper == 0
        else "start"
        if parameter == 0
        else "end"
        if parameter == 1
        else "interior"
    )
    normal = [Fraction(0), Fraction(0)]
    if distance:
        if kind == "point":
            index = next(i for i, value in enumerate(residual) if abs(value) == distance)
            normal[index] = sign(residual[index])
        elif kind == "start":
            index = next(i for i, value in enumerate(residual) if value == distance)
            normal[index] = Fraction(1)
        elif kind == "end":
            index = next(i for i, value in enumerate(residual) if value == -distance)
            normal[index] = Fraction(-1)
        else:
            denominator = abs(vector[0]) + abs(vector[1])
            normal = [
                sign(residual[0]) * abs(vector[1]) / denominator,
                sign(residual[1]) * abs(vector[0]) / denominator,
            ]
    constant = dot(normal, difference(point, start))
    slope = -dot(normal, vector)
    values = [constant, constant + slope]
    lower = {
        "kind": kind,
        "normal": normal,
        "coefficients": [constant, slope],
        "endpoint_values": values,
        "norm": sum((abs(value) for value in normal), Fraction(0)),
        "value": min(values),
    }
    if lower["norm"] > 1 or lower["value"] != distance or constant + parameter * slope != distance:
        raise ValueError("contact lacked an exact global dual certificate")
    projection = {
        "raw": raw,
        "t": parameter,
        "location": location,
        "delta": delta,
        "q": contact,
        "residual": residual,
        "distance": distance,
    }
    return seg, projection, lower


def segment_parameter(seg, point):
    if seg["vector"] == [Fraction(0), Fraction(0)]:
        if point != seg["start"]:
            raise ValueError("point segment contact differs")
        return Fraction(0)
    parameter = (point[0] - seg["start"][0]) / seg["vector"][0]
    if [a + parameter * v for a, v in zip(seg["start"], seg["vector"], strict=True)] != point:
        raise ValueError("segment coordinates require different parameters")
    return parameter


def class_oracle(bound, mass_by_eta):
    upper = Fraction(*bound["upper"])
    segments = [segment(mass_by_eta[eta], upper) for eta in (0, 1)]
    deltas = [upper if upper < 1 else Fraction(1), Fraction(0)]
    points = [forward(mass_by_eta[eta], delta) for eta, delta in enumerate(deltas)]
    parameters = [
        segment_parameter(seg, point) for seg, point in zip(segments, points, strict=True)
    ]
    residual = difference(points[0], points[1])
    distance = max(abs(value) for value in residual)
    normal = [Fraction(0), Fraction(1) if upper < 1 else Fraction(0)]
    constant = dot(normal, difference(segments[0]["start"], segments[1]["start"]))
    flat_slope = dot(normal, segments[0]["vector"])
    conformal_slope = -dot(normal, segments[1]["vector"])
    corners = [
        constant,
        constant + conformal_slope,
        constant + flat_slope,
        constant + flat_slope + conformal_slope,
    ]
    closed_form = 3 * (1 - upper) / (16 * (4 + upper)) if upper < 1 else Fraction(0)
    lower = {
        "normal": normal,
        "coefficients": [constant, flat_slope, conformal_slope],
        "corner_values": corners,
        "norm": sum((abs(value) for value in normal), Fraction(0)),
        "value": min(corners),
    }
    if min(corners) != distance or distance != closed_form:
        raise ValueError("class contact does not attain the global affine lower bound")
    return {
        "bound": bound["id"],
        "upper": upper,
        "segments": segments,
        "kind": "ordered" if upper < 1 else "collision",
        "deltas": deltas,
        "parameters": parameters,
        "points": points,
        "residual": residual,
        "distance": distance,
        "closed_form": closed_form,
        "lower": lower,
    }


def plan_oracle(identifier, kind, source, distance, premise, protocol):
    step = Fraction(1, protocol["grid_denominator"])
    slack = distance - 2 * step
    score = protocol["quota"] * slack**2
    positive, threshold = slack > 0, score >= 10
    sufficient = positive and threshold
    eligible = premise and sufficient
    alpha = Fraction(*protocol["alpha"])
    return {
        "id": identifier,
        "kind": kind,
        "source": source,
        "distance": distance,
        "in_premise": premise,
        "slack": slack,
        "score": score,
        "grid_positive": positive,
        "threshold_holds": threshold,
        "sufficient": sufficient,
        "eligible": eligible,
        "status": "out_of_premise"
        if not premise
        else "certified"
        if sufficient
        else "not_certified",
        "guarantees": [
            {"correct_singleton_at_least": 1 - alpha, "conditional_wrong_singleton_at_most": alpha}
        ]
        if eligible
        else [],
    }


def box_contains(box, point):
    return all(lower <= value <= upper for value, (lower, upper) in zip(point, box, strict=True))


def box_inverse(masses, box, upper):
    """Closed-cell arrangement evaluated against the original mass ratios."""
    nodes = {Fraction(0), upper}
    aq, bq = masses[0]
    for (ai, bi), (lower, higher) in zip(masses[1:], box, strict=True):
        for constant, slope in (
            (ai - lower * aq, bi - lower * bq),
            (higher * aq - ai, higher * bq - bi),
        ):
            if slope:
                root = -constant / slope
                if 0 <= root <= upper:
                    nodes.add(root)
    nodes = sorted(nodes)
    pieces = [[value, value] for value in nodes if box_contains(box, forward(masses, value))]
    for left, right in itertools.pairwise(nodes):
        if box_contains(box, forward(masses, (left + right) / 2)):
            if not box_contains(box, forward(masses, left)) or not box_contains(
                box, forward(masses, right)
            ):
                raise ValueError("closed affine-ratio cell lost an endpoint")
            pieces.append([left, right])
    joined = []
    for left, right in sorted(pieces):
        if joined and left <= joined[-1][1]:
            joined[-1][1] = max(joined[-1][1], right)
        else:
            joined.append([left, right])
    if len(joined) > 1:
        raise ValueError("linear fractional box inverse became disconnected")
    return joined[0] if joined else []


def expected(protocol, baseline):
    geometries = [geometry_oracle(protocol, row) for row in protocol["geometries"]]
    masses = {row["eta"]: row["mass_coefficients"] for row in geometries if row["scale"] == 1}
    fixtures = [fixture_oracle(row, masses[row["eta"]]) for row in protocol["fixtures"]]
    distances = []
    for fixture in fixtures:
        for bound in protocol["density_bounds"]:
            upper = Fraction(*bound["upper"])
            seg, projection, lower = contact_oracle(fixture["q"], masses[1 - fixture["eta"]], upper)
            distances.append(
                {
                    "id": fixture["id"] + "/" + bound["id"],
                    "fixture": fixture["id"],
                    "bound": bound["id"],
                    "in_premise": 0 <= fixture["delta"] <= upper,
                    "opposite_eta": 1 - fixture["eta"],
                    "p": list(fixture["q"]),
                    "segment": seg,
                    "projection": projection,
                    "lower": lower,
                }
            )
    classes = [class_oracle(bound, masses) for bound in protocol["density_bounds"]]
    scaled_masses = {
        row["eta"]: row["mass_coefficients"] for row in geometries if row["scale"] == 4
    }
    scaled_classes = [class_oracle(bound, scaled_masses) for bound in protocol["density_bounds"]]
    plans = [
        plan_oracle(
            "pointwise/" + row["id"],
            "pointwise",
            row["id"],
            row["projection"]["distance"],
            row["in_premise"],
            protocol,
        )
        for row in distances
    ] + [
        plan_oracle("class/" + row["bound"], "class", row["bound"], row["distance"], True, protocol)
        for row in classes
    ]
    by_geometry = {row["id"]: row for row in geometries}
    scale_pairs = []
    for left, right in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        a, b = by_geometry[left], by_geometry[right]
        factor = b["volumes"][0] / a["volumes"][0]
        actual = b["volumes"] == [factor * value for value in a["volumes"]]
        actual = actual and b["mass_coefficients"] == [
            [factor * value for value in row] for row in a["mass_coefficients"]
        ]
        segments_equal = all(
            segment(a["mass_coefficients"], Fraction(*bound["upper"]))
            == segment(b["mass_coefficients"], Fraction(*bound["upper"]))
            for bound in protocol["density_bounds"]
        )
        equal = classes == scaled_classes
        opposite_scaled = next(
            row["mass_coefficients"]
            for row in geometries
            if row["eta"] == 1 - a["eta"] and row["scale"] == 4
        )
        for fixture in fixtures:
            if fixture["eta"] != a["eta"]:
                continue
            scaled_point = forward(b["mass_coefficients"], fixture["delta"])
            equal = equal and scaled_point == fixture["q"]
            for bound in protocol["density_bounds"]:
                upper = Fraction(*bound["upper"])
                equal = equal and contact_oracle(
                    fixture["q"], masses[1 - a["eta"]], upper
                ) == contact_oracle(scaled_point, opposite_scaled, upper)
        scale_pairs.append(
            {
                "worlds": [left, right],
                "volume_factor": factor,
                "actual_scaling": actual,
                "target_equal": a["target"] == b["target"],
                "segments_equal": segments_equal,
                "distances_equal": equal,
            }
        )
    base_intervals = [
        {
            "k": row["k"],
            "interval": list(row["interval"]),
            "width": row["interval"][1] - row["interval"][0],
        }
        for row in baseline["intervals"]
    ]
    max_width = max(row["width"] for row in base_intervals)
    retained_baseline = {
        "schema": baseline["schema"],
        "quota": baseline["quota"],
        "grid_denominator": baseline["grid_denominator"],
        "alpha": baseline["alpha"],
        "intervals": base_intervals,
        "max_width": max_width,
        "maximizers": [row["k"] for row in base_intervals if row["width"] == max_width],
        "comparisons": [
            {
                "id": row["id"],
                "distance": row["distance"],
                "strict_width_sufficient": max_width < row["distance"],
            }
            for row in plans
        ],
    }
    distance_by_id = {row["id"]: row for row in distances}
    fixture_by_id = {row["id"]: row for row in fixtures}
    boxes = []
    bound = next(
        row for row in protocol["density_bounds"] if row["id"] == protocol["boxes"]["bound"]
    )
    upper = Fraction(*bound["upper"])
    for fixture_id in protocol["boxes"]["fixtures"]:
        row = distance_by_id[fixture_id + "/" + bound["id"]]
        point, contact = row["p"], row["projection"]["q"]
        distance = row["projection"]["distance"]
        for kind in protocol["boxes"]["kinds"]:
            if kind == "contact_rectangle":
                box = [sorted(pair) for pair in zip(point, contact, strict=True)]
            else:
                radius = distance / 2 if kind == "half_square" else distance
                box = [[value - radius, value + radius] for value in point]
            widths = [higher - lower for lower, higher in box]
            width = max(widths)
            domain = box_inverse(masses[row["opposite_eta"]], box, upper)
            boxes.append(
                {
                    "id": fixture_id + "/" + kind,
                    "distance_id": row["id"],
                    "kind": kind,
                    "intervals": box,
                    "widths": widths,
                    "max_width": width,
                    "half_width": width / 2,
                    "contains_true": box_contains(box, point),
                    "contains_contact": box_contains(box, contact),
                    "opposite_delta_set": domain,
                    "admits_opposite": bool(domain),
                    "strict_width_condition": width < distance,
                    "half_width_condition": width / 2 < distance,
                    "nonstrict_width_condition": width <= distance,
                }
            )
    terms = [Fraction(1)]
    for index in range(1, 6):
        terms.append(terms[-1] * 5 / index)
    rational_bound = {
        "terms": terms,
        "partial_sum": sum(terms, Fraction(0)),
        "threshold": Fraction(80),
        "log_upper": Fraction(5),
        "strict": sum(terms, Fraction(0)) > 80,
    }
    control = protocol["rational_control"]
    n, m = control["quota"], control["grid_denominator"]
    radius, distance, step = (
        Fraction(*control["radius"]),
        Fraction(*control["distance"]),
        Fraction(1, m),
    )
    square, width, main_score = (
        2 * n * radius**2,
        2 * radius + 2 * step,
        n * (distance - 2 * step) ** 2,
    )
    rational_controls = [
        {
            "quota": n,
            "grid_denominator": m,
            "radius": radius,
            "distance": distance,
            "step": step,
            "square_score": square,
            "width": width,
            "main_score": main_score,
            "radius_test": radius >= 0 and square >= 5 and width <= distance,
            "direct_test": distance - 2 * step > 0 and main_score >= 10,
            "strict_slack_basis": "ln80_lt_5",
        }
    ]
    compensated = [(fixture_by_id["flat_1"], masses[0]), (fixture_by_id["conformal_0"], masses[1])]
    polynomials = []
    for fixture, mass in compensated:
        normalizer = 2 * at(mass[0], fixture["delta"])
        polynomials.append(
            [
                Fraction(1) / normalizer,
                (fixture["eta"] + fixture["delta"]) / normalizer,
                fixture["eta"] * fixture["delta"] / normalizer,
            ]
        )
    targets = [row[0]["target"] for row in compensated]
    obstruction = {
        "deltas": [row[0]["delta"] for row in compensated],
        "q": list(compensated[0][0]["q"]),
        "targets": targets,
        "target_gap": targets[0] - targets[1],
        "normalized_polynomials": polynomials,
        "point_equal": polynomials[0] == polynomials[1],
    }
    return {
        "schema": "qr05bt-report-v1",
        "geometries": geometries,
        "fixtures": fixtures,
        "distances": distances,
        "classes": classes,
        "plans": plans,
        "scale_pairs": scale_pairs,
        "baseline": retained_baseline,
        "boxes": boxes,
        "rational_bound": rational_bound,
        "rational_controls": rational_controls,
        "obstruction": obstruction,
    }


class MathematicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.baseline = cls.study._baseline(cls.study.source_snapshot())
        cls.protocol_before = copy.deepcopy(cls.protocol)
        cls.baseline_before = copy.deepcopy(cls.baseline)
        cls.oracle = expected(cls.protocol, cls.baseline)

    def test_complete_native_report_and_exact_bounded_inventory(self):
        exact_tree(self, self.report, self.oracle)
        report = self.report
        census = {
            "geometries": len(report["geometries"]),
            "fixtures": len(report["fixtures"]),
            "distances": len(report["distances"]),
            "classes": len(report["classes"]),
            "plans": len(report["plans"]),
            "scale_pairs": len(report["scale_pairs"]),
            "baseline_intervals": len(report["baseline"]["intervals"]),
            "baseline_comparisons": len(report["baseline"]["comparisons"]),
            "boxes": len(report["boxes"]),
            "rational_controls": len(report["rational_controls"]),
            "obstructions": 1,
        }
        exact_tree(self, census, self.protocol["coverage"])
        self.assertNotIn("tails", report)
        self.assertNotIn("counts", report)
        self.assertTrue(all("count_law" not in row for row in report["fixtures"]))

    def test_independent_oracle_preserves_both_authenticated_input_trees(self):
        exact_tree(self, self.protocol, self.protocol_before)
        exact_tree(self, self.baseline, self.baseline_before)
        self.assertEqual(self.baseline["schema"], "qr05bt-br-baseline-v1")
        self.assertEqual(self.baseline["quota"], 4)
        self.assertEqual(self.protocol["quota"], 65536)
        self.assertEqual(
            set(self.baseline), {"schema", "quota", "grid_denominator", "alpha", "intervals"}
        )
        self.assertEqual([row["k"] for row in self.baseline["intervals"]], list(range(5)))
        self.assertTrue(
            all(
                type(value) is Fraction
                for row in self.baseline["intervals"]
                for value in row["interval"]
            )
        )

    def test_endpoint_masses_primitive_lines_and_actual_scale_factors(self):
        geometries = {row["id"]: row for row in self.report["geometries"]}
        for geometry in geometries.values():
            self.assertTrue(geometry["positive_normalizer"])
            self.assertTrue(geometry["decreasing"])
            mass = geometry["mass_coefficients"]
            self.assertEqual(geometry["volumes"], [row[0] for row in mass])
            self.assertEqual(geometry["target"], mass[1][0] / mass[0][0])
            self.assertTrue(all(value < 0 for value in geometry["derivative_numerators"]))
            for bound in self.protocol["density_bounds"]:
                upper = Fraction(*bound["upper"])
                for delta in (Fraction(0), upper):
                    self.assertGreater(at(mass[0], delta), 0)
                    q = forward(mass, delta)
                    self.assertEqual(dot(geometry["line"][:2], q), geometry["line"][2])
        self.assertEqual(geometries["flat"]["line"], [Fraction(-20), Fraction(16), Fraction(1)])
        self.assertEqual(
            geometries["conformal"]["line"], [Fraction(-9520), Fraction(7296), Fraction(371)]
        )
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
            self.assertEqual(a["line"], b["line"])
            self.assertEqual(a["target"], b["target"])
            for bound in self.protocol["density_bounds"]:
                upper = Fraction(*bound["upper"])
                self.assertEqual(
                    segment(a["mass_coefficients"], upper), segment(b["mass_coefficients"], upper)
                )
            for fixture in self.report["fixtures"]:
                if fixture["eta"] == a["eta"]:
                    self.assertEqual(
                        forward(a["mass_coefficients"], fixture["delta"]),
                        forward(b["mass_coefficients"], fixture["delta"]),
                    )
        for row in self.report["scale_pairs"]:
            self.assertEqual(row["volume_factor"], Fraction(4))
            self.assertTrue(
                all(
                    row[key]
                    for key in (
                        "actual_scaling",
                        "target_equal",
                        "segments_equal",
                        "distances_equal",
                    )
                )
            )
        scaled_masses = {
            row["eta"]: row["mass_coefficients"] for row in geometries.values() if row["scale"] == 4
        }
        for bound, row in zip(self.protocol["density_bounds"], self.report["classes"], strict=True):
            exact_tree(self, class_oracle(bound, scaled_masses), row)

    def test_every_contact_attains_a_global_affine_dual_lower_bound(self):
        masses = {
            row["eta"]: row["mass_coefficients"]
            for row in self.report["geometries"]
            if row["scale"] == 1
        }
        bounds = {row["id"]: Fraction(*row["upper"]) for row in self.protocol["density_bounds"]}
        fixtures = {row["id"]: row for row in self.report["fixtures"]}
        for row in self.report["distances"]:
            seg, projection, lower = row["segment"], row["projection"], row["lower"]
            upper, p = bounds[row["bound"]], row["p"]
            q, parameter, distance = projection["q"], projection["t"], projection["distance"]
            normal = lower["normal"]
            self.assertEqual(p, fixtures[row["fixture"]]["q"])
            self.assertEqual(row["opposite_eta"], 1 - fixtures[row["fixture"]]["eta"])
            self.assertTrue(0 <= parameter <= 1)
            self.assertTrue(0 <= projection["delta"] <= upper)
            self.assertEqual(q, forward(masses[row["opposite_eta"]], projection["delta"]))
            self.assertEqual(
                q, [a + parameter * v for a, v in zip(seg["start"], seg["vector"], strict=True)]
            )
            self.assertEqual(projection["residual"], difference(p, q))
            self.assertEqual(distance, max(abs(value) for value in difference(p, q)))
            constant, slope = dot(normal, difference(p, seg["start"])), -dot(normal, seg["vector"])
            self.assertEqual(lower["coefficients"], [constant, slope])
            self.assertEqual(lower["endpoint_values"], [constant, constant + slope])
            self.assertEqual(lower["norm"], sum(abs(value) for value in normal))
            self.assertLessEqual(lower["norm"], 1)
            self.assertTrue(all(value >= distance for value in lower["endpoint_values"]))
            self.assertEqual(lower["value"], min(lower["endpoint_values"]))
            self.assertEqual(lower["value"], distance)
            self.assertEqual(constant + parameter * slope, distance)
            self.assertEqual(dot(normal, projection["residual"]), distance)
            # An affine function's minimum on [0,1] is attained at an endpoint.
            # These identities certify the whole continuous segment, not samples.
            if distance == 0:
                self.assertEqual(normal, [Fraction(0), Fraction(0)])
            if lower["kind"] == "interior" and distance:
                self.assertEqual(projection["residual"][0], -projection["residual"][1])
                self.assertEqual(slope, Fraction(0))
                self.assertEqual(lower["norm"], Fraction(1))

    def test_raw_balance_diagnostics_closed_ties_and_point_segments(self):
        for row in self.report["distances"]:
            upper = next(
                Fraction(*bound["upper"])
                for bound in self.protocol["density_bounds"]
                if bound["id"] == row["bound"]
            )
            projection, seg = row["projection"], row["segment"]
            if upper == 0:
                self.assertEqual(projection["raw"], [])
                self.assertEqual(projection["location"], "point")
                self.assertEqual(row["lower"]["kind"], "point")
                self.assertEqual(projection["t"], Fraction(0))
                self.assertEqual(projection["delta"], Fraction(0))
                self.assertEqual(seg["start"], seg["end"])
                self.assertEqual(seg["vector"], [Fraction(0), Fraction(0)])
            else:
                self.assertTrue(all(value < 0 for value in seg["vector"]))
                self.assertEqual(len(projection["raw"]), 1)
                raw = projection["raw"][0]
                # Diagnostic only: the independent minimizer came from dual
                # saturation, not from this primary-route quotient.
                self.assertEqual(raw * sum(seg["vector"]), sum(difference(row["p"], seg["start"])))
                location = (
                    "before"
                    if raw < 0
                    else "start"
                    if raw == 0
                    else "interior"
                    if raw < 1
                    else "end"
                    if raw == 1
                    else "after"
                )
                self.assertEqual(projection["location"], location)
                self.assertEqual(projection["t"], min(Fraction(1), max(Fraction(0), raw)))
                if raw in (0, 1):
                    self.assertEqual(projection["location"], "start" if raw == 0 else "end")
            parameter = projection["t"]
            expected_kind = (
                "point"
                if upper == 0
                else "start"
                if parameter == 0
                else "end"
                if parameter == 1
                else "interior"
            )
            self.assertEqual(row["lower"]["kind"], expected_kind)

    def test_whole_class_four_corner_certificates_and_uniform_margins(self):
        for row in self.report["classes"]:
            flat, conformal = row["segments"]
            lower, normal = row["lower"], row["lower"]["normal"]
            constant = dot(normal, difference(flat["start"], conformal["start"]))
            t_slope, s_slope = dot(normal, flat["vector"]), -dot(normal, conformal["vector"])
            corners = [
                constant,
                constant + s_slope,
                constant + t_slope,
                constant + t_slope + s_slope,
            ]
            self.assertEqual(lower["coefficients"], [constant, t_slope, s_slope])
            self.assertEqual(lower["corner_values"], corners)
            self.assertLessEqual(lower["norm"], 1)
            self.assertEqual(lower["norm"], sum(abs(value) for value in normal))
            self.assertTrue(all(value >= row["distance"] for value in corners))
            self.assertEqual(min(corners), row["distance"])
            self.assertEqual(lower["value"], row["distance"])
            t, s = row["parameters"]
            self.assertTrue(0 <= t <= 1 and 0 <= s <= 1)
            self.assertEqual(constant + t * t_slope + s * s_slope, row["distance"])
            self.assertEqual(row["residual"], difference(*row["points"]))
            self.assertEqual(max(abs(value) for value in row["residual"]), row["distance"])
            for seg, parameter, point in zip(
                row["segments"], row["parameters"], row["points"], strict=True
            ):
                self.assertEqual(
                    point,
                    [a + parameter * v for a, v in zip(seg["start"], seg["vector"], strict=True)],
                )
                if seg["start"] == seg["end"]:
                    self.assertEqual(parameter, Fraction(0))
            if row["upper"] < 1:
                self.assertEqual(row["kind"], "ordered")
                self.assertEqual(row["deltas"], [row["upper"], Fraction(0)])
                self.assertEqual(normal, [Fraction(0), Fraction(1)])
                self.assertGreater(row["distance"], 0)
            else:
                self.assertEqual(row["kind"], "collision")
                self.assertEqual(row["deltas"], [Fraction(1), Fraction(0)])
                self.assertEqual(row["distance"], Fraction(0))
                self.assertEqual(normal, [Fraction(0), Fraction(0)])
        margins = {row["bound"]: row["distance"] for row in self.report["classes"]}
        self.assertEqual(
            margins,
            {
                "uniform": Fraction(3, 64),
                "half": Fraction(1, 48),
                "one": Fraction(0),
                "two": Fraction(0),
            },
        )

    def test_all_plans_keep_sign_score_and_true_premise_separate(self):
        n, step = self.protocol["quota"], Fraction(1, self.protocol["grid_denominator"])
        rows = {row["id"]: row for row in self.report["distances"]}
        classes = {row["bound"]: row for row in self.report["classes"]}
        for plan in self.report["plans"]:
            distance = plan["distance"]
            slack = distance - 2 * step
            self.assertEqual(plan["slack"], slack)
            self.assertEqual(plan["score"], n * slack**2)
            self.assertEqual(plan["grid_positive"], slack > 0)
            self.assertEqual(plan["threshold_holds"], plan["score"] >= 10)
            self.assertEqual(plan["sufficient"], plan["grid_positive"] and plan["threshold_holds"])
            self.assertEqual(plan["eligible"], plan["in_premise"] and plan["sufficient"])
            if plan["kind"] == "pointwise":
                source = rows[plan["source"]]
                self.assertEqual(distance, source["projection"]["distance"])
                self.assertEqual(plan["in_premise"], source["in_premise"])
            else:
                self.assertEqual(plan["kind"], "class")
                self.assertEqual(distance, classes[plan["source"]]["distance"])
                self.assertTrue(plan["in_premise"])
            if not plan["in_premise"]:
                self.assertEqual(plan["status"], "out_of_premise")
                self.assertEqual(plan["guarantees"], [])
            elif plan["sufficient"]:
                self.assertEqual(plan["status"], "certified")
                self.assertEqual(
                    plan["guarantees"],
                    [
                        {
                            "correct_singleton_at_least": Fraction(19, 20),
                            "conditional_wrong_singleton_at_most": Fraction(1, 20),
                        }
                    ],
                )
            else:
                self.assertEqual(plan["status"], "not_certified")
                self.assertEqual(plan["guarantees"], [])
        class_plans = {row["source"]: row for row in self.report["plans"] if row["kind"] == "class"}
        self.assertEqual(class_plans["uniform"]["score"], Fraction(100))
        self.assertEqual(class_plans["half"]["score"], Fraction(100, 9))
        for name in ("uniform", "half"):
            self.assertTrue(class_plans[name]["eligible"])
        for name in ("one", "two"):
            self.assertFalse(class_plans[name]["grid_positive"])
            self.assertFalse(class_plans[name]["eligible"])
        self.assertTrue(any(not row["in_premise"] for row in self.report["plans"]))

    def test_rational_log_certificate_and_private_safe_equalities(self):
        row = self.report["rational_bound"]
        self.assertEqual(len(row["terms"]), 6)
        self.assertEqual(row["terms"][0], Fraction(1))
        for index in range(1, 6):
            self.assertEqual(index * row["terms"][index], 5 * row["terms"][index - 1])
        self.assertTrue(all(value > 0 for value in row["terms"]))
        self.assertEqual(sum(row["terms"]), row["partial_sum"])
        self.assertEqual(row["partial_sum"], Fraction(1097, 12))
        self.assertEqual(row["threshold"], Fraction(80))
        self.assertEqual(row["log_upper"], Fraction(5))
        self.assertGreater(row["partial_sum"], row["threshold"])
        self.assertTrue(row["strict"])
        (control,) = self.report["rational_controls"]
        self.assertEqual(control["quota"], 40)
        self.assertEqual(control["grid_denominator"], 8)
        self.assertEqual(control["radius"], Fraction(1, 4))
        self.assertEqual(control["distance"], Fraction(3, 4))
        self.assertEqual(control["step"], Fraction(1, 8))
        self.assertEqual(control["square_score"], Fraction(5))
        self.assertEqual(control["width"], control["distance"])
        self.assertEqual(control["main_score"], Fraction(10))
        self.assertTrue(control["radius_test"] and control["direct_test"])
        self.assertEqual(control["strict_slack_basis"], "ln80_lt_5")
        # Strict logarithmic slack, not a strict rational inequality, makes
        # these equality cases sufficient. No numerical logarithm is used.

    def test_six_boxes_distinguish_radius_full_width_and_closed_contact(self):
        distances = {row["id"]: row for row in self.report["distances"]}
        self.assertEqual(len(self.report["boxes"]), 6)
        for row in self.report["boxes"]:
            source = distances[row["distance_id"]]
            projection = source["projection"]
            distance, point, contact = projection["distance"], source["p"], projection["q"]
            self.assertEqual(source["lower"]["kind"], "interior")
            self.assertGreater(distance, 0)
            self.assertTrue(row["contains_true"])
            self.assertTrue(box_contains(row["intervals"], point))
            self.assertEqual(row["contains_contact"], box_contains(row["intervals"], contact))
            self.assertEqual(row["widths"], [upper - lower for lower, upper in row["intervals"]])
            self.assertEqual(row["max_width"], max(row["widths"]))
            self.assertEqual(row["half_width"], row["max_width"] / 2)
            self.assertEqual(row["strict_width_condition"], row["max_width"] < distance)
            self.assertEqual(row["half_width_condition"], row["half_width"] < distance)
            self.assertEqual(row["nonstrict_width_condition"], row["max_width"] <= distance)
            self.assertEqual(row["admits_opposite"], bool(row["opposite_delta_set"]))
            if row["kind"] == "half_square":
                self.assertEqual(row["max_width"], distance)
                self.assertTrue(row["half_width_condition"])
                self.assertTrue(row["nonstrict_width_condition"])
                self.assertFalse(row["strict_width_condition"])
                self.assertFalse(row["contains_contact"])
                self.assertEqual(row["opposite_delta_set"], [])
            else:
                self.assertTrue(row["contains_contact"])
                self.assertEqual(
                    row["opposite_delta_set"], [projection["delta"], projection["delta"]]
                )
                if row["kind"] == "contact_rectangle":
                    self.assertEqual(row["max_width"], distance)
                    self.assertEqual(row["half_width"], distance / 2)
                    self.assertTrue(row["half_width_condition"])
                    self.assertTrue(row["nonstrict_width_condition"])
                else:
                    self.assertEqual(row["kind"], "touch_square")
                    self.assertEqual(row["max_width"], 2 * distance)
                    self.assertFalse(row["half_width_condition"])
                    self.assertFalse(row["nonstrict_width_condition"])
                self.assertFalse(row["strict_width_condition"])

    def test_authenticated_coarse_baseline_is_not_a_new_quota_table(self):
        baseline = self.report["baseline"]
        self.assertEqual(baseline["quota"], self.baseline["quota"])
        self.assertNotEqual(baseline["quota"], self.protocol["quota"])
        self.assertEqual(baseline["alpha"], self.baseline["alpha"])
        self.assertEqual(baseline["grid_denominator"], self.baseline["grid_denominator"])
        for actual, retained in zip(baseline["intervals"], self.baseline["intervals"], strict=True):
            self.assertEqual(actual["k"], retained["k"])
            exact_tree(self, actual["interval"], retained["interval"])
            self.assertEqual(actual["width"], retained["interval"][1] - retained["interval"][0])
        maximum = max(row["width"] for row in baseline["intervals"])
        self.assertEqual(baseline["max_width"], maximum)
        self.assertEqual(
            baseline["maximizers"],
            [row["k"] for row in baseline["intervals"] if row["width"] == maximum],
        )
        self.assertEqual(
            [row["id"] for row in baseline["comparisons"]],
            [row["id"] for row in self.report["plans"]],
        )
        for comparison, plan in zip(baseline["comparisons"], self.report["plans"], strict=True):
            self.assertEqual(comparison["distance"], plan["distance"])
            self.assertEqual(comparison["strict_width_sufficient"], maximum < plan["distance"])

    def test_prespecified_interior_contacts_are_closer_than_selected_fixture_gap(self):
        rows = {row["id"]: row for row in self.report["distances"]}
        flat, conformal = rows["flat_interior/two"], rows["conformal_interior/two"]
        self.assertEqual(flat["projection"]["distance"], Fraction(5, 16816))
        self.assertEqual(flat["projection"]["delta"], Fraction(270, 973))
        self.assertEqual(conformal["projection"]["distance"], Fraction(5, 16416))
        self.assertEqual(conformal["projection"]["delta"], Fraction(16516, 11261))
        fixture_gap = max(abs(value) for value in difference(flat["p"], conformal["p"]))
        self.assertEqual(fixture_gap, Fraction(5, 7296))
        for row in (flat, conformal):
            self.assertLess(row["projection"]["distance"], fixture_gap)
            self.assertEqual(row["lower"]["kind"], "interior")
            self.assertEqual(row["projection"]["residual"][0], -row["projection"]["residual"][1])

    def test_compensation_zero_distance_and_out_of_premise_are_distinct(self):
        obstruction = self.report["obstruction"]
        self.assertEqual(obstruction["deltas"], [Fraction(1), Fraction(0)])
        self.assertEqual(obstruction["targets"], [Fraction(1, 4), Fraction(17, 80)])
        self.assertEqual(obstruction["target_gap"], Fraction(3, 80))
        self.assertEqual(
            obstruction["normalized_polynomials"],
            [[Fraction(4, 5), Fraction(4, 5), Fraction(0)]] * 2,
        )
        self.assertTrue(obstruction["point_equal"])
        rows = {row["id"]: row for row in self.report["distances"]}
        plans = {row["id"]: row for row in self.report["plans"]}
        for name in ("one", "two"):
            for fixture in ("flat_1", "conformal_0"):
                row = rows[fixture + "/" + name]
                self.assertTrue(row["in_premise"])
                self.assertEqual(row["projection"]["distance"], Fraction(0))
                self.assertFalse(plans["pointwise/" + row["id"]]["eligible"])
        excluded = rows["flat_1/half"]
        self.assertFalse(excluded["in_premise"])
        self.assertEqual(excluded["projection"]["distance"], Fraction(0))
        self.assertEqual(plans["pointwise/" + excluded["id"]]["status"], "out_of_premise")
        half = next(row for row in self.report["classes"] if row["bound"] == "half")
        self.assertGreater(half["distance"], 0)
        self.assertEqual(half["kind"], "ordered")


def fixture_snapshot(study):
    snapshot = {name: ("synthetic:" + name).encode() for name in study.SOURCE_PATHS}
    snapshot["protocol.json"] = (HERE / "protocol.json").read_bytes()
    snapshot[study.UTILITY_SOURCE] = study.UTILITY_BYTES
    snapshot[study.BASELINE_SOURCE] = (HERE / study.BASELINE_SOURCE).read_bytes()
    return snapshot


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_authenticated_fresh_utility_aliases_twelve_sources_and_owned_defaults(self):
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
        self.assertEqual(len(snapshot), 12)
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
                    study.ARTIFACT_LIMIT if name == study.BASELINE_SOURCE else study.SOURCE_LIMIT,
                )
                for name in study.SOURCE_PATHS
            ],
        )
        with tempfile.TemporaryDirectory(prefix="qr05bt-utility-") as directory:
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
        with tempfile.TemporaryDirectory(prefix="qr05bt-read-") as directory:
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

        def collect(protocol, baseline):
            seen.append((protocol, baseline))
            return {"value": Fraction(1, 3)}

        module = type("Synthetic", (), {"analyze": staticmethod(collect)})
        with (
            mock.patch.object(study, "source_snapshot", return_value=snapshot),
            mock.patch.object(study, "load_engine", return_value=module) as loader,
        ):
            exact_tree(self, study.analyze(), {"value": Fraction(1, 3)})
        self.assertIsNot(seen[0], seen[1])
        self.assertIsNot(seen[0][0], seen[1][0])
        self.assertIsNot(seen[0][0]["fixtures"], seen[1][0]["fixtures"])
        self.assertIsNot(seen[0][1], seen[1][1])
        self.assertIsNot(seen[0][1]["intervals"], seen[1][1]["intervals"])
        self.assertEqual(
            loader.call_args_list,
            [
                mock.call(snapshot["primary.py"], "primary"),
                mock.call(snapshot["reference.py"], "reference"),
            ],
        )
        blob = b"def analyze(protocol, baseline):\n return {'value': 1}\n"
        with mock.patch.dict(sys.modules, {"probe": object()}):
            first, second = study.load_engine(blob, "probe"), study.load_engine(blob, "probe")
        self.assertIsNot(first, second)
        self.assertEqual(first.analyze({}, {}), {"value": 1})

    def test_baseline_authentication_precedes_parse_and_exact_native_extraction(self):
        study = self.study
        snapshot = fixture_snapshot(study)
        changed = {**snapshot, study.BASELINE_SOURCE: snapshot[study.BASELINE_SOURCE] + b"\n"}
        for operation in (study._protocol, study._baseline):
            with (
                mock.patch.object(study, "strict_loads", side_effect=AssertionError("early parse")),
                self.assertRaises(ValueError),
            ):
                operation(changed)
        original = study.strict_loads(snapshot[study.BASELINE_SOURCE])
        for path, replacement in (
            (("schema",), "qr05bt-capture-v1"),
            (("report", "schema"), "qr05bt-report-v1"),
            (("report", "confidence", "quota"), True),
            (("report", "confidence", "grid_denominator"), True),
            (("report", "confidence", "alpha"), {"$fraction": [1, 21]}),
            (("report", "intervals", 0, "k"), False),
            (("report", "intervals", 0, "interval"), [0, {"$fraction": [171, 256]}]),
        ):
            altered = copy.deepcopy(original)
            node = altered
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = replacement
            blob = study.canonical(altered)
            with (
                self.subTest(path=path),
                mock.patch.object(study, "BASELINE_SHA256", hashlib.sha256(blob).hexdigest()),
                self.assertRaises(ValueError),
            ):
                study._baseline({**snapshot, study.BASELINE_SOURCE: blob})
        one, two = study._baseline(snapshot), study._baseline(snapshot)
        exact_tree(self, one, two)
        self.assertIsNot(one, two)
        self.assertIsNot(one["intervals"], two["intervals"])
        self.assertEqual(one["schema"], "qr05bt-br-baseline-v1")
        self.assertEqual(len(one["intervals"]), 5)

    def test_both_route_input_mutations_native_mismatch_and_late_source_changes(self):
        study = self.study
        snapshot = fixture_snapshot(study)

        def good(_protocol, _baseline):
            return {"value": Fraction(1)}

        def mutate_protocol(protocol, baseline):
            protocol["quota"] = True
            return good(protocol, baseline)

        def mutate_baseline(protocol, baseline):
            baseline["intervals"][0]["k"] = True
            return good(protocol, baseline)

        routes = (
            (good, mutate_protocol),
            (mutate_protocol, good),
            (good, mutate_baseline),
            (mutate_baseline, good),
            (good, lambda _p, _b: {"value": 1}),
        )
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

    def test_both_engines_validate_entire_inputs_before_mathematical_work(self):
        study = self.study
        snapshot = study.source_snapshot()
        protocol, baseline = study._protocol(snapshot), study._baseline(snapshot)
        mutations = (
            ("protocol", ("quota",), True),
            ("protocol", ("coverage", "geometries"), True),
            ("protocol", ("regions", "Q", 0, 0), Fraction(0)),
            ("protocol", ("fixtures", 0, "delta"), (0, 1)),
            ("protocol", ("density_bounds", 0, "upper", 1), 0),
            ("protocol", ("alpha",), [2, 40]),
            ("baseline", ("quota",), True),
            ("baseline", ("alpha",), 1),
            ("baseline", ("intervals", 0, "interval", 0), 0),
            ("baseline", ("intervals", 0, "interval", 1), Fraction(1)),
            ("baseline", ("intervals", 0, "k"), False),
        )
        for filename in ("primary.py", "reference.py"):
            engine = study.load_engine(snapshot[filename], filename[:-3])
            with mock.patch.object(
                engine, "_fraction", side_effect=AssertionError("arithmetic before validation")
            ):
                for target, path, value in mutations:
                    inputs = {
                        "protocol": copy.deepcopy(protocol),
                        "baseline": copy.deepcopy(baseline),
                    }
                    node = inputs[target]
                    for key in path[:-1]:
                        node = node[key]
                    node[path[-1]] = value
                    with (
                        self.subTest(engine=filename, target=target, path=path),
                        self.assertRaises(ValueError),
                    ):
                        engine.analyze(inputs["protocol"], inputs["baseline"])
                for target in ("protocol", "baseline"):
                    inputs = {
                        "protocol": copy.deepcopy(protocol),
                        "baseline": copy.deepcopy(baseline),
                    }
                    inputs[target]["cycle"] = inputs[target]
                    with self.subTest(engine=filename, cycle=target), self.assertRaises(ValueError):
                        engine.analyze(inputs["protocol"], inputs["baseline"])

    def test_complete_retained_report_mutations_are_detected(self):
        _study, _protocol, report = evaluated()
        for key in report:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.study.require_equal(report, {**report, key: "corrupted"})
        for path, replacement in (
            (("geometries", 0, "mass_coefficients", 0, 0), Fraction(0)),
            (("fixtures", 0, "one_point", 2), Fraction(1)),
            (("distances", 0, "projection", "distance"), Fraction(-1)),
            (("distances", 0, "in_premise"), 1),
            (("classes", -1, "lower", "norm"), Fraction(1)),
            (("plans", -1, "eligible"), 1),
            (("baseline", "max_width"), Fraction(0)),
            (("boxes", -1, "admits_opposite"), 1),
            (("rational_bound", "strict"), 1),
            (("rational_controls", 0, "square_score"), Fraction(0)),
            (("obstruction", "point_equal"), 1),
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
        self.directory = tempfile.TemporaryDirectory(prefix="qr05bt-evidence-")
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
        self.assertEqual(freeze["schema"], "qr05bt-source-freeze-v1")
        self.assertEqual(capture["schema"], "qr05bt-capture-v1")
        self.assertEqual(len(freeze["sources"]), 12)
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
        raise KeyboardInterrupt("QR-05BT 120-second suite deadline")

    signal.signal(signal.SIGALRM, suite_expired)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
