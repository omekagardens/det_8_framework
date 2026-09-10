"""Independent BV moment, forward-law, and closed-cell mathematical tests.

Only definitions run at import. Integration/evidence tests and the bounded
suite entry point are appended separately. No old mathematical executor loads.
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
    spec = importlib.util.spec_from_file_location("_qr05bv_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load BV driver")
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


def norm(point):
    return max(abs(value) for value in point)


def affine(row, delta):
    return row[0] + row[1] * delta


def nested(point):
    return 0 <= point[0] <= point[1] <= 1


def law(point):
    return [1 - point[1], point[1] - point[0], Fraction(0), point[0]]


def box_contains(box, point):
    return all(lo <= value <= hi for value, (lo, hi) in zip(point, box, strict=True))


def moment(rectangle, degree):
    """Product of the two exact antiderivative increments of u^degree v^degree."""
    lo_u, hi_u, lo_v, hi_v = [Fraction(*pair) for pair in rectangle]
    power = degree + 1
    integral_u = (hi_u**power - lo_u**power) / power
    integral_v = (hi_v**power - lo_v**power) / power
    return integral_u * integral_v


def mass_coefficients(protocol, eta, scale):
    rows = []
    for name in ("Q", "I1", "I2"):
        moments = [moment(protocol["regions"][name], degree) for degree in range(3)]
        rows.append(
            [
                Fraction(scale, 2) * (moments[0] + eta * moments[1]),
                Fraction(scale, 2) * (moments[1] + eta * moments[2]),
            ]
        )
    return rows


def forward(masses, delta):
    denominator = affine(masses[0], delta)
    if denominator <= 0:
        raise ValueError("oracle requires a positive original mass normalizer")
    return [affine(row, delta) / denominator for row in masses[1:]]


def primitive_line(first, second):
    vector = difference(second, first)
    normal = [vector[1], -vector[0]]
    rational = normal + [dot(normal, first)]
    common = math.lcm(*(value.denominator for value in rational))
    integers = [value.numerator * (common // value.denominator) for value in rational]
    divisor = math.gcd(*(abs(value) for value in integers))
    if not divisor:
        raise ValueError("cannot derive a line from a singleton")
    if integers[1] < 0:
        divisor = -divisor
    return [Fraction(value // divisor) for value in integers]


def geometry_oracle(protocol, item):
    masses = mass_coefficients(protocol, item["eta"], item["scale"])
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
            affine(masses[0], delta) > 0 for delta in (Fraction(0), Fraction(2))
        ),
        "decreasing": all(value < 0 for value in derivatives),
    }


def segment(masses, upper):
    start, end = forward(masses, Fraction(0)), forward(masses, upper)
    return {"start": start, "end": end, "vector": difference(end, start)}


def segment_parameter(seg, point):
    if seg["start"] == seg["end"]:
        if point != seg["start"]:
            raise ValueError("point segment lost its contact")
        return Fraction(0)
    parameter = (point[0] - seg["start"][0]) / seg["vector"][0]
    if point != [a + parameter * v for a, v in zip(seg["start"], seg["vector"], strict=True)]:
        raise ValueError("the contact coordinates require different parameters")
    return parameter


def class_oracle(bound, masses):
    upper = Fraction(*bound["upper"])
    segments = [segment(masses[eta], upper) for eta in (0, 1)]
    deltas = [upper if upper < 1 else Fraction(1), Fraction(0)]
    points = [forward(masses[eta], delta) for eta, delta in enumerate(deltas)]
    parameters = [
        segment_parameter(seg, point) for seg, point in zip(segments, points, strict=True)
    ]
    residual = difference(points[0], points[1])
    distance = norm(residual)
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
    if min(corners) != distance or distance != closed_form:
        raise ValueError("forward contacts did not attain the global four-corner lower bound")
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
        "lower": {
            "normal": normal,
            "coefficients": [constant, flat_slope, conformal_slope],
            "corner_values": corners,
            "norm": sum((abs(value) for value in normal), Fraction(0)),
            "value": min(corners),
        },
    }


def case_oracle(item, ideal):
    fraction = Fraction(*item["fraction"])
    distance = ideal["distance"]
    error = distance * fraction
    interpolation = min(error / distance, Fraction(1, 2)) if distance else Fraction(0)
    first, second = ideal["points"]
    actual = [
        [(1 - interpolation) * a + interpolation * b for a, b in zip(first, second, strict=True)],
        [interpolation * a + (1 - interpolation) * b for a, b in zip(first, second, strict=True)],
    ]
    displacement = [difference(r, p) for r, p in zip(actual, ideal["points"], strict=True)]
    attained = norm(difference(actual[0], actual[1]))
    signed_remaining = distance - 2 * error
    penalty = 2 * error * ideal["lower"]["norm"]
    signed_value = min(ideal["lower"]["corner_values"]) - penalty
    if attained != max(signed_remaining, Fraction(0)) or attained != max(signed_value, Fraction(0)):
        raise ValueError("actual contacts did not attain the global distortion lower bound")
    return {
        "id": item["id"],
        "bound": item["bound"],
        "upper": ideal["upper"],
        "fraction": fraction,
        "error": error,
        "ideal_distance": distance,
        "signed_remaining": signed_remaining,
        "distance": attained,
        "ideal_deltas": list(ideal["deltas"]),
        "ideal_contacts": copy.deepcopy(ideal["points"]),
        "actual_contacts": actual,
        "displacements": displacement,
        "distortion_norms": [norm(value) for value in displacement],
        "laws": [law(point) for point in actual],
        "nested": [nested(point) for point in actual],
        "interpolation": interpolation,
        "kind": "separated" if attained else "new_collision" if distance else "inherited_collision",
        "lower": {
            "normal": list(ideal["lower"]["normal"]),
            "norm": ideal["lower"]["norm"],
            "ideal_corner_values": list(ideal["lower"]["corner_values"]),
            "penalty": penalty,
            "signed_value": signed_value,
            "value": max(signed_value, Fraction(0)),
        },
    }


def plan_oracle(case, protocol):
    step = Fraction(1, protocol["grid_denominator"])
    slack = case["signed_remaining"] - 2 * step
    score = protocol["quota"] * slack**2
    positive, threshold = slack > 0, score >= 10
    sufficient = positive and threshold
    alpha = Fraction(*protocol["alpha"])
    return {
        "id": case["id"],
        "ideal_distance": case["ideal_distance"],
        "error": case["error"],
        "signed_remaining": case["signed_remaining"],
        "distance": case["distance"],
        "step": step,
        "slack": slack,
        "score": score,
        "grid_positive": positive,
        "threshold_holds": threshold,
        "sufficient": sufficient,
        "status": "certified" if sufficient else "not_certified",
        "guarantees": [
            {"correct_singleton_at_least": 1 - alpha, "conditional_wrong_singleton_at_most": alpha}
        ]
        if sufficient
        else [],
    }


def enlarged(box, error):
    return [[max(Fraction(0), lo - error), min(Fraction(1), hi + error)] for lo, hi in box]


def constraints(masses, box):
    aq, bq = masses[0]
    output = []
    for (ai, bi), (lo, hi) in zip(masses[1:], box, strict=True):
        output.extend([[ai - lo * aq, bi - lo * bq], [hi * aq - ai, hi * bq - bi]])
    return output


def closed_cell_inverse(masses, box, upper):
    """Enumerate the exact original-ratio boundary arrangement, never clip bounds.

    Between consecutive roots each continuous original ratio remains on
    the same side of every boundary. Testing one interior value determines
    a whole open cell; closed endpoints are tested independently.
    """
    nodes = {Fraction(0), upper}
    for constant, slope in constraints(masses, box):
        if slope:
            root = -constant / slope
            if 0 <= root <= upper:
                nodes.add(root)
    ordered = sorted(nodes)
    pieces = [[value, value] for value in ordered if box_contains(box, forward(masses, value))]
    for left, right in itertools.pairwise(ordered):
        if box_contains(box, forward(masses, (left + right) / 2)):
            if not box_contains(box, forward(masses, left)) or not box_contains(
                box, forward(masses, right)
            ):
                raise ValueError("a closed original-ratio cell lost an endpoint")
            pieces.append([left, right])
    joined = []
    for left, right in sorted(pieces):
        if joined and left <= joined[-1][1]:
            joined[-1][1] = max(joined[-1][1], right)
        else:
            joined.append([left, right])
    if len(joined) > 1:
        raise ValueError("the shared-density inverse is disconnected")
    return joined[0] if joined else []


def inverse_oracle(geometry, box, error, upper):
    if box[0][0] > box[1][1]:
        return {"delta_set": [], "constraints": [], "endpoints": []}
    expanded = enlarged(box, error)
    masses = geometry["mass_coefficients"]
    inequalities = constraints(masses, expanded)
    delta_set = closed_cell_inverse(masses, expanded, upper)
    endpoints = []
    for delta in delta_set:
        q = forward(masses, delta)
        lower = [max(lo, value - error) for (lo, _), value in zip(box, q, strict=True)]
        higher = [min(hi, value + error) for (_, hi), value in zip(box, q, strict=True)]
        witness = [lower[0], max(lower[1], lower[0])]
        offset = difference(witness, q)
        endpoints.append(
            {
                "delta": delta,
                "q": q,
                "constraint_values": [affine(row, delta) for row in inequalities],
                "A": lower,
                "B": higher,
                "r": witness,
                "law": law(witness),
                "offset": offset,
                "norm": norm(offset),
                "nested": nested(witness),
                "inside_box": box_contains(box, witness),
                "within_error": norm(offset) <= error,
            }
        )
    return {"delta_set": delta_set, "constraints": inequalities, "endpoints": endpoints}


def hypothesis_oracle(geometry, box, error, upper):
    result = {key: geometry[key] for key in ("id", "eta", "scale", "target")}
    result.update(inverse_oracle(geometry, box, error, upper))
    return result


def target_summary(hypotheses):
    targets = sorted({row["target"] for row in hypotheses if row["delta_set"]})
    return targets, "empty" if not targets else "singleton" if len(targets) == 1 else "ambiguous"


def box_oracle(item, ideal, geometries):
    fraction = Fraction(*item["fraction"])
    error = ideal["distance"] * fraction
    first, second = ideal["points"]
    point = (
        list(first)
        if item["point"] == "flat"
        else list(second)
        if item["point"] == "conformal"
        else [(a + b) / 2 for a, b in zip(first, second, strict=True)]
    )
    box = [[value, value] for value in point]
    hypotheses = [
        hypothesis_oracle(geometry, box, error, ideal["upper"]) for geometry in geometries
    ]
    old = [hypothesis_oracle(geometry, box, Fraction(0), ideal["upper"]) for geometry in geometries]
    targets, status = target_summary(hypotheses)
    old_targets, old_status = target_summary(old)
    return {
        "id": item["id"],
        "bound": item["bound"],
        "upper": ideal["upper"],
        "fraction": fraction,
        "error": error,
        "point": point,
        "intervals": box,
        "nested_box": box[0][0] <= box[1][1],
        "expanded": enlarged(box, error),
        "hypotheses": hypotheses,
        "targets": targets,
        "status": status,
        "unexpanded": {"hypotheses": old, "targets": old_targets, "status": old_status},
    }


def negative_oracle(protocol, masses):
    item = protocol["negative"]
    delta, allowance = Fraction(*item["delta"]), Fraction(*item["lambda"])
    ideal = forward(masses[item["eta"]], delta)
    ideal_law = law(ideal)
    actual_law = [
        value + sign * allowance for value, sign in zip(ideal_law, (-1, 1, 1, -1), strict=True)
    ]
    marginals = [actual_law[2] + actual_law[3], actual_law[1] + actual_law[3]]
    error, alpha = Fraction(0), Fraction(*protocol["alpha"])
    return {
        "eta": item["eta"],
        "delta": delta,
        "error": error,
        "lambda": allowance,
        "ideal_q": ideal,
        "ideal_law": ideal_law,
        "actual_law": actual_law,
        "actual_marginals": marginals,
        "marginals_equal": marginals == ideal,
        "within_error": norm(difference(marginals, ideal)) <= error,
        "population_in_S": nested(marginals),
        "nonnegative": all(value >= 0 for value in actual_law),
        "normalized": sum(actual_law, Fraction(0)) == 1,
        "nested_support": actual_law[2] == 0,
        "forbidden_mass": actual_law[2],
        "refusal_lower": actual_law[2],
        "alpha": alpha,
        "refusal_exceeds_alpha": actual_law[2] > alpha,
        "status": "outside_nested_law",
    }


def normalized_inverse(hypothesis):
    return {
        "delta_set": list(hypothesis["delta_set"]),
        "endpoints": [
            {key: value for key, value in endpoint.items() if key != "constraint_values"}
            for endpoint in hypothesis["endpoints"]
        ],
    }


def legacy_plan(plan, bound):
    return {
        "id": "class/" + bound,
        "kind": "class",
        "source": bound,
        "distance": plan["ideal_distance"],
        "in_premise": True,
        "slack": plan["slack"],
        "score": plan["score"],
        "grid_positive": plan["grid_positive"],
        "threshold_holds": plan["threshold_holds"],
        "sufficient": plan["sufficient"],
        "eligible": plan["sufficient"],
        "status": plan["status"],
        "guarantees": copy.deepcopy(plan["guarantees"]),
    }


def expected(protocol, baseline):
    geometries = [geometry_oracle(protocol, item) for item in protocol["geometries"]]
    masses = {row["eta"]: row["mass_coefficients"] for row in geometries if row["scale"] == 1}
    classes = [class_oracle(bound, masses) for bound in protocol["density_bounds"]]
    by_class = {row["bound"]: row for row in classes}
    cases = [case_oracle(item, by_class[item["bound"]]) for item in protocol["cases"]]
    plans = [plan_oracle(case, protocol) for case in cases]
    boxes = [box_oracle(item, by_class[item["bound"]], geometries) for item in protocol["boxes"]]
    scaled_masses = {
        row["eta"]: row["mass_coefficients"] for row in geometries if row["scale"] == 4
    }
    scaled_classes = [class_oracle(bound, scaled_masses) for bound in protocol["density_bounds"]]
    scaled_by_class = {row["bound"]: row for row in scaled_classes}
    scaled_cases = [case_oracle(item, scaled_by_class[item["bound"]]) for item in protocol["cases"]]
    by_geometry = {row["id"]: row for row in geometries}
    scale_pairs = []
    for unit_id, scaled_id in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        unit, scaled = by_geometry[unit_id], by_geometry[scaled_id]
        factor = scaled["volumes"][0] / unit["volumes"][0]
        actual_scaling = (
            scaled["volumes"] == [factor * value for value in unit["volumes"]]
            and scaled["mass_coefficients"]
            == [[factor * value for value in row] for row in unit["mass_coefficients"]]
            and scaled["derivative_numerators"]
            == [factor**2 * value for value in unit["derivative_numerators"]]
        )
        inverses_equal, constraints_scaled = True, True
        targets_equal = unit["target"] == scaled["target"]
        for box in boxes:
            for hypotheses in (box["hypotheses"], box["unexpanded"]["hypotheses"]):
                by_id = {row["id"]: row for row in hypotheses}
                left, right = by_id[unit_id], by_id[scaled_id]
                inverses_equal = inverses_equal and normalized_inverse(left) == normalized_inverse(
                    right
                )
                targets_equal = targets_equal and left["target"] == right["target"]
                constraints_scaled = constraints_scaled and right["constraints"] == [
                    [factor * value for value in row] for row in left["constraints"]
                ]
                constraints_scaled = constraints_scaled and all(
                    b["constraint_values"] == [factor * value for value in a["constraint_values"]]
                    for a, b in zip(left["endpoints"], right["endpoints"], strict=True)
                )
        scale_pairs.append(
            {
                "worlds": [unit_id, scaled_id],
                "volume_factor": factor,
                "actual_scaling": actual_scaling,
                "classes_equal": classes == scaled_classes,
                "cases_equal": cases == scaled_cases,
                "inverses_equal": inverses_equal,
                "constraints_scaled": constraints_scaled,
                "targets_equal": targets_equal,
            }
        )
    by_plan = {row["id"]: row for row in plans}
    zero_ids = [bound["id"] + "/zero" for bound in protocol["density_bounds"]]
    legacy = [legacy_plan(by_plan[identifier], identifier.split("/")[0]) for identifier in zero_ids]
    return {
        "schema": "qr05bv-report-v1",
        "planning": {
            "quota": protocol["quota"],
            "grid_denominator": protocol["grid_denominator"],
            "alpha": Fraction(*protocol["alpha"]),
            "tail_allocations": [Fraction(*pair) for pair in protocol["tail_allocations"]],
            "threshold": Fraction(10),
            "log_upper": Fraction(5),
            "basis": "ln80_lt_5",
        },
        "geometries": geometries,
        "classes": classes,
        "cases": cases,
        "plans": plans,
        "boxes": boxes,
        "negative": negative_oracle(protocol, masses),
        "scale_pairs": scale_pairs,
        "baseline": {
            "schema": "qr05bv-bt-comparison-v1",
            "zero_ids": zero_ids,
            "classes_equal": classes == baseline["classes"],
            "plans_equal": legacy == baseline["plans"],
            "plans": legacy,
        },
    }


class MathematicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.baseline = cls.study._baseline(cls.study.source_snapshot())
        cls.protocol_before = copy.deepcopy(cls.protocol)
        cls.baseline_before = copy.deepcopy(cls.baseline)
        cls.oracle = expected(cls.protocol, cls.baseline)

    def test_complete_native_report_and_fixed_census(self):
        exact_tree(self, self.report, self.oracle)
        report = self.report
        census = {
            "geometries": len(report["geometries"]),
            "classes": len(report["classes"]),
            "cases": len(report["cases"]),
            "plans": len(report["plans"]),
            "boxes": len(report["boxes"]),
            "hypotheses": sum(len(box["hypotheses"]) for box in report["boxes"]),
            "unexpanded_hypotheses": sum(
                len(box["unexpanded"]["hypotheses"]) for box in report["boxes"]
            ),
            "negative_controls": 1,
            "scale_pairs": len(report["scale_pairs"]),
            "baseline_classes": len(self.baseline["classes"]),
            "baseline_plans": len(report["baseline"]["plans"]),
        }
        exact_tree(self, census, self.protocol["coverage"])
        self.assertNotIn("counts", report)
        self.assertNotIn("tails", report)
        self.assertNotIn("fixtures", report)

    def test_oracle_preserves_inputs_and_zero_error_complete_bt_evidence(self):
        exact_tree(self, self.protocol, self.protocol_before)
        exact_tree(self, self.baseline, self.baseline_before)
        exact_tree(self, self.report["classes"], self.baseline["classes"])
        exact_tree(self, self.report["baseline"]["plans"], self.baseline["plans"])
        self.assertEqual(self.baseline["schema"], "qr05bv-bt-baseline-v1")
        self.assertTrue(self.report["baseline"]["classes_equal"])
        self.assertTrue(self.report["baseline"]["plans_equal"])
        self.assertEqual(
            self.report["baseline"]["zero_ids"],
            ["uniform/zero", "half/zero", "one/zero", "two/zero"],
        )

    def test_original_masses_lines_and_continuous_normalization(self):
        for geometry in self.report["geometries"]:
            masses = geometry["mass_coefficients"]
            self.assertTrue(geometry["positive_normalizer"])
            self.assertTrue(geometry["decreasing"])
            self.assertEqual(geometry["volumes"], [row[0] for row in masses])
            self.assertEqual(geometry["target"], masses[1][0] / masses[0][0])
            self.assertTrue(all(value < 0 for value in geometry["derivative_numerators"]))
            for delta in (Fraction(0), Fraction(2)):
                self.assertGreater(affine(masses[0], delta), 0)
                point = forward(masses, delta)
                self.assertTrue(nested(point))
                self.assertEqual(dot(geometry["line"][:2], point), geometry["line"][2])
            wanted = (
                [Fraction(-20), Fraction(16), Fraction(1)]
                if geometry["eta"] == 0
                else [Fraction(-9520), Fraction(7296), Fraction(371)]
            )
            self.assertEqual(geometry["line"], wanted)
            self.assertEqual(
                geometry["target"], Fraction(1, 4) if geometry["eta"] == 0 else Fraction(17, 80)
            )

    def test_ideal_contacts_and_affine_global_lower_certificates(self):
        masses = {
            row["eta"]: row["mass_coefficients"]
            for row in self.report["geometries"]
            if row["scale"] == 1
        }
        for row in self.report["classes"]:
            lower, segments = row["lower"], row["segments"]
            for eta in (0, 1):
                self.assertTrue(0 <= row["deltas"][eta] <= row["upper"])
                self.assertTrue(0 <= row["parameters"][eta] <= 1)
                self.assertEqual(row["points"][eta], forward(masses[eta], row["deltas"][eta]))
                self.assertEqual(segments[eta], segment(masses[eta], row["upper"]))
            c, mt, ms = lower["coefficients"]
            self.assertEqual(lower["corner_values"], [c, c + ms, c + mt, c + mt + ms])
            self.assertEqual(
                c, dot(lower["normal"], difference(segments[0]["start"], segments[1]["start"]))
            )
            self.assertEqual(mt, dot(lower["normal"], segments[0]["vector"]))
            self.assertEqual(ms, -dot(lower["normal"], segments[1]["vector"]))
            self.assertLessEqual(lower["norm"], 1)
            self.assertEqual(min(lower["corner_values"]), row["distance"])
            self.assertEqual(
                c + mt * row["parameters"][0] + ms * row["parameters"][1], row["distance"]
            )
            self.assertEqual(norm(difference(row["points"][0], row["points"][1])), row["distance"])
            self.assertEqual(row["residual"], difference(row["points"][0], row["points"][1]))
            if row["upper"] == 0:
                self.assertEqual(row["parameters"], [Fraction(0), Fraction(0)])
            if row["distance"]:
                self.assertEqual(
                    row["residual"], [row["distance"] * Fraction(4, 5), row["distance"]]
                )

    def test_actual_contacts_attain_bound_and_complete_nested_laws(self):
        classes = {row["bound"]: row for row in self.report["classes"]}
        for row in self.report["cases"]:
            ideal = classes[row["bound"]]
            self.assertEqual(row["ideal_contacts"], ideal["points"])
            self.assertEqual(row["ideal_deltas"], ideal["deltas"])
            self.assertEqual(row["signed_remaining"], ideal["distance"] - 2 * row["error"])
            self.assertEqual(row["distance"], max(row["signed_remaining"], Fraction(0)))
            self.assertEqual(row["distance"], norm(difference(*row["actual_contacts"])))
            self.assertTrue(all(row["nested"]))
            for index in (0, 1):
                point = row["actual_contacts"][index]
                offset = difference(point, row["ideal_contacts"][index])
                self.assertTrue(nested(point))
                self.assertEqual(row["displacements"][index], offset)
                self.assertEqual(row["distortion_norms"][index], norm(offset))
                self.assertLessEqual(norm(offset), row["error"])
                self.assertEqual(row["laws"][index], law(point))
                self.assertTrue(all(value >= 0 for value in row["laws"][index]))
                self.assertEqual(sum(row["laws"][index], Fraction(0)), 1)
                self.assertEqual(row["laws"][index][2], 0)
            lower = row["lower"]
            self.assertEqual(lower["ideal_corner_values"], ideal["lower"]["corner_values"])
            self.assertEqual(lower["penalty"], 2 * row["error"] * lower["norm"])
            self.assertEqual(
                lower["signed_value"], min(lower["ideal_corner_values"]) - lower["penalty"]
            )
            self.assertEqual(lower["value"], max(lower["signed_value"], Fraction(0)))
            self.assertEqual(lower["value"], row["distance"])
            self.assertEqual(
                dot(lower["normal"], difference(*row["actual_contacts"])), row["distance"]
            )
            if row["ideal_distance"] == 0:
                self.assertEqual(row["interpolation"], Fraction(0))
                self.assertEqual(row["kind"], "inherited_collision")

    def test_closed_collision_laws_and_unequal_ideal_targets(self):
        cases = {row["id"]: row for row in self.report["cases"]}
        wanted = {
            "uniform/contact": [Fraction(37, 160), Fraction(45, 128)],
            "half/contact": [Fraction(53, 240), Fraction(65, 192)],
            "one/zero": [Fraction(17, 80), Fraction(21, 64)],
            "two/zero": [Fraction(17, 80), Fraction(21, 64)],
        }
        for identifier, point in wanted.items():
            row = cases[identifier]
            self.assertEqual(row["actual_contacts"], [point, point])
            self.assertEqual(row["laws"], [law(point), law(point)])
            self.assertEqual(row["distance"], 0)
        targets = {geometry["target"] for geometry in self.report["geometries"]}
        self.assertEqual(targets, {Fraction(1, 4), Fraction(17, 80)})
        self.assertEqual(max(targets) - min(targets), Fraction(3, 80))

    def test_signed_budget_all_eight_fixed_analytical_controls(self):
        expected_rows = [
            ("uniform/zero", Fraction(0), Fraction(3, 64), Fraction(5, 128), Fraction(100), True),
            (
                "uniform/quarter",
                Fraction(3, 256),
                Fraction(3, 128),
                Fraction(1, 64),
                Fraction(16),
                True,
            ),
            (
                "uniform/contact",
                Fraction(3, 128),
                Fraction(0),
                Fraction(-1, 128),
                Fraction(4),
                False,
            ),
            ("half/zero", Fraction(0), Fraction(1, 48), Fraction(5, 384), Fraction(100, 9), True),
            (
                "half/quarter",
                Fraction(1, 192),
                Fraction(1, 96),
                Fraction(1, 384),
                Fraction(4, 9),
                False,
            ),
            ("half/contact", Fraction(1, 96), Fraction(0), Fraction(-1, 128), Fraction(4), False),
            ("one/zero", Fraction(0), Fraction(0), Fraction(-1, 128), Fraction(4), False),
            ("two/zero", Fraction(0), Fraction(0), Fraction(-1, 128), Fraction(4), False),
        ]
        for row, wanted in zip(self.report["plans"], expected_rows, strict=True):
            self.assertEqual(
                tuple(
                    row[key] for key in ("id", "error", "distance", "slack", "score", "sufficient")
                ),
                wanted,
            )
            self.assertEqual(
                row["slack"], row["ideal_distance"] - 2 * row["error"] - 2 * row["step"]
            )
            self.assertEqual(row["score"], self.protocol["quota"] * row["slack"] ** 2)
            self.assertIs(row["grid_positive"], row["slack"] > 0)
            self.assertIs(row["threshold_holds"], row["score"] >= 10)
            self.assertIs(row["sufficient"], row["grid_positive"] and row["threshold_holds"])
            if not row["sufficient"]:
                self.assertEqual(row["guarantees"], [])
        half = next(row for row in self.report["plans"] if row["id"] == "half/quarter")
        self.assertGreater(half["distance"], 0)
        self.assertTrue(half["grid_positive"])
        self.assertFalse(half["threshold_holds"])

    def test_population_box_full_inverse_and_every_original_law_witness(self):
        geometries = {row["id"]: row for row in self.report["geometries"]}
        for box in self.report["boxes"]:
            self.assertTrue(box["nested_box"])
            self.assertEqual(box["intervals"], [[value, value] for value in box["point"]])
            self.assertEqual(box["expanded"], enlarged(box["intervals"], box["error"]))
            for error, hypotheses in (
                (box["error"], box["hypotheses"]),
                (Fraction(0), box["unexpanded"]["hypotheses"]),
            ):
                for hypothesis in hypotheses:
                    geometry = geometries[hypothesis["id"]]
                    independent = inverse_oracle(geometry, box["intervals"], error, box["upper"])
                    for key in ("delta_set", "constraints", "endpoints"):
                        exact_tree(self, hypothesis[key], independent[key])
                    self.assertEqual(len(hypothesis["constraints"]), 4)
                    self.assertEqual(len(hypothesis["endpoints"]), len(hypothesis["delta_set"]))
                    for endpoint in hypothesis["endpoints"]:
                        self.assertTrue(0 <= endpoint["delta"] <= box["upper"])
                        self.assertEqual(
                            endpoint["q"], forward(geometry["mass_coefficients"], endpoint["delta"])
                        )
                        self.assertTrue(all(value >= 0 for value in endpoint["constraint_values"]))
                        self.assertTrue(
                            all(a <= b for a, b in zip(endpoint["A"], endpoint["B"], strict=True))
                        )
                        self.assertLessEqual(endpoint["A"][0], endpoint["B"][1])
                        self.assertEqual(endpoint["r"], [endpoint["A"][0], max(endpoint["A"])])
                        self.assertEqual(endpoint["r"], box["point"])
                        self.assertEqual(
                            endpoint["offset"], difference(endpoint["r"], endpoint["q"])
                        )
                        self.assertEqual(endpoint["law"], law(endpoint["r"]))
                        self.assertLessEqual(endpoint["norm"], error)
                        self.assertTrue(
                            endpoint["nested"]
                            and endpoint["inside_box"]
                            and endpoint["within_error"]
                        )
                        self.assertEqual(sum(endpoint["law"], Fraction(0)), 1)
            targets, status = target_summary(box["hypotheses"])
            self.assertEqual(box["targets"], targets)
            self.assertEqual(box["status"], status)

    def test_half_positive_shared_density_intervals_and_closed_midpoints(self):
        boxes = {row["id"]: row for row in self.report["boxes"]}
        wanted = {
            "half/flat": [[Fraction(16, 41), Fraction(1, 2)], []],
            "half/conformal": [[], [Fraction(0), Fraction(18, 209)]],
            "half/midpoint_quarter": [[], []],
            "half/midpoint_contact": [[Fraction(1, 2), Fraction(1, 2)], [Fraction(0), Fraction(0)]],
            "uniform/flat": [[Fraction(0), Fraction(0)], []],
            "uniform/conformal": [[], [Fraction(0), Fraction(0)]],
            "uniform/midpoint_quarter": [[], []],
            "uniform/midpoint_contact": [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]],
            "one/collision": [[Fraction(1), Fraction(1)], [Fraction(0), Fraction(0)]],
            "two/collision": [[Fraction(1), Fraction(1)], [Fraction(0), Fraction(0)]],
        }
        for identifier, intervals in wanted.items():
            box = boxes[identifier]
            for hypothesis in box["hypotheses"]:
                self.assertEqual(hypothesis["delta_set"], intervals[hypothesis["eta"]])
                if (
                    hypothesis["delta_set"]
                    and hypothesis["delta_set"][0] == hypothesis["delta_set"][1]
                ):
                    self.assertEqual(hypothesis["endpoints"][0], hypothesis["endpoints"][1])
        for bound in ("uniform", "half"):
            box = boxes[bound + "/midpoint_contact"]
            self.assertEqual(box["status"], "ambiguous")
            self.assertEqual(box["unexpanded"]["status"], "empty")
            self.assertEqual(box["unexpanded"]["targets"], [])
            self.assertEqual(box["targets"], [Fraction(17, 80), Fraction(1, 4)])

    def test_midpoint_distance_to_both_complete_families(self):
        boxes = {row["id"]: row for row in self.report["boxes"]}
        for ideal in self.report["classes"][:2]:
            midpoint = boxes[ideal["bound"] + "/midpoint_quarter"]["point"]
            half_distance = ideal["distance"] / 2
            self.assertEqual(norm(difference(ideal["points"][0], midpoint)), half_distance)
            self.assertEqual(norm(difference(ideal["points"][1], midpoint)), half_distance)
            # The second-coordinate affine endpoints bound every segment point.
            flat, conformal = ideal["segments"]
            self.assertEqual(min(flat["start"][1], flat["end"][1]) - midpoint[1], half_distance)
            self.assertEqual(
                midpoint[1] - max(conformal["start"][1], conformal["end"][1]), half_distance
            )
            self.assertGreater(half_distance, boxes[ideal["bound"] + "/midpoint_quarter"]["error"])
            self.assertEqual(boxes[ideal["bound"] + "/midpoint_quarter"]["status"], "empty")

    def test_enlargement_is_monotone_on_existing_population_boxes(self):
        for box in self.report["boxes"]:
            for expanded, original in zip(
                box["hypotheses"], box["unexpanded"]["hypotheses"], strict=True
            ):
                if original["delta_set"]:
                    self.assertTrue(expanded["delta_set"])
                    self.assertLessEqual(expanded["delta_set"][0], original["delta_set"][0])
                    self.assertGreaterEqual(expanded["delta_set"][1], original["delta_set"][1])
                if box["error"] == 0:
                    exact_tree(self, expanded, original)
            self.assertTrue(set(box["unexpanded"]["targets"]).issubset(box["targets"]))

    def test_private_original_empty_nested_box_guard_both_routes(self):
        snapshot = self.study.source_snapshot()
        geometry = self.report["geometries"][0]
        box = [[Fraction(3, 4), Fraction(1)], [Fraction(0), Fraction(1, 4)]]
        self.assertGreater(box[0][0], box[1][1])
        self.assertTrue(
            box_contains(
                enlarged(box, Fraction(1)), forward(geometry["mass_coefficients"], Fraction(0))
            )
        )
        wanted = {"delta_set": [], "constraints": [], "endpoints": []}
        exact_tree(self, inverse_oracle(geometry, box, Fraction(1), Fraction(0)), wanted)
        for filename in ("primary.py", "reference.py"):
            engine = self.study.load_engine(snapshot[filename], filename[:-3] + "_empty_box_test")
            supplied_geometry, supplied_box = copy.deepcopy(geometry), copy.deepcopy(box)
            exact_tree(
                self,
                engine._inverse(supplied_geometry, supplied_box, Fraction(1), Fraction(0)),
                wanted,
            )
            exact_tree(self, supplied_geometry, geometry)
            exact_tree(self, supplied_box, box)
        self.study._check_snapshot(snapshot)

    def test_nonnested_control_preserves_marginals_but_requires_refusal(self):
        negative = self.report["negative"]
        self.assertEqual(
            negative["actual_law"],
            [Fraction(9, 16), Fraction(3, 16), Fraction(1, 16), Fraction(3, 16)],
        )
        self.assertEqual(negative["actual_marginals"], [Fraction(1, 4), Fraction(3, 8)])
        self.assertTrue(
            negative["marginals_equal"] and negative["within_error"] and negative["population_in_S"]
        )
        self.assertTrue(negative["nonnegative"] and negative["normalized"])
        self.assertFalse(negative["nested_support"])
        self.assertEqual(negative["forbidden_mass"], negative["lambda"])
        self.assertEqual(negative["refusal_lower"], Fraction(1, 16))
        self.assertGreater(negative["refusal_lower"], negative["alpha"])
        self.assertTrue(negative["refusal_exceeds_alpha"])
        self.assertEqual(negative["status"], "outside_nested_law")
        # The first attempt alone supplies this lower bound; no word bank or
        # n-dependent refusal power is evaluated by this test or either engine.

    def test_same_input_scale_comparisons_and_actual_coefficient_scaling(self):
        geometries = {row["id"]: row for row in self.report["geometries"]}
        for pair in self.report["scale_pairs"]:
            unit, scaled = [geometries[name] for name in pair["worlds"]]
            self.assertEqual(pair["volume_factor"], Fraction(4))
            self.assertTrue(
                all(
                    pair[key]
                    for key in (
                        "actual_scaling",
                        "classes_equal",
                        "cases_equal",
                        "inverses_equal",
                        "constraints_scaled",
                        "targets_equal",
                    )
                )
            )
            self.assertEqual(scaled["volumes"], [4 * value for value in unit["volumes"]])
            self.assertEqual(
                scaled["mass_coefficients"],
                [[4 * value for value in row] for row in unit["mass_coefficients"]],
            )
            self.assertEqual(
                scaled["derivative_numerators"],
                [16 * value for value in unit["derivative_numerators"]],
            )
            self.assertEqual(scaled["target"], unit["target"])
            for box in self.report["boxes"]:
                for hypotheses in (box["hypotheses"], box["unexpanded"]["hypotheses"]):
                    by_id = {row["id"]: row for row in hypotheses}
                    first, second = [by_id[name] for name in pair["worlds"]]
                    exact_tree(self, normalized_inverse(first), normalized_inverse(second))
                    self.assertEqual(
                        second["constraints"],
                        [[4 * value for value in row] for row in first["constraints"]],
                    )
                    for a, b in zip(first["endpoints"], second["endpoints"], strict=True):
                        self.assertEqual(
                            b["constraint_values"], [4 * value for value in a["constraint_values"]]
                        )

    def test_guarantees_use_every_box_separation_and_fixed_sampling_allocation(self):
        planning = self.report["planning"]
        self.assertEqual(planning["quota"], 65536)
        self.assertEqual(planning["grid_denominator"], 256)
        self.assertEqual(planning["alpha"], Fraction(1, 20))
        self.assertEqual(planning["tail_allocations"], [Fraction(1, 80)] * 4)
        self.assertEqual(sum(planning["tail_allocations"], Fraction(0)), planning["alpha"])
        self.assertEqual(planning["threshold"], Fraction(10))
        self.assertEqual(planning["log_upper"], Fraction(5))
        self.assertEqual(planning["basis"], "ln80_lt_5")
        for row in self.report["plans"]:
            if row["sufficient"]:
                (guarantee,) = row["guarantees"]
                self.assertEqual(guarantee["correct_singleton_at_least"], 1 - planning["alpha"])
                self.assertEqual(
                    guarantee["conditional_wrong_singleton_at_most"], planning["alpha"]
                )
                self.assertGreater(row["slack"], 0)
                self.assertGreaterEqual(
                    planning["quota"] * row["slack"] ** 2, 2 * planning["log_upper"]
                )
            else:
                self.assertEqual(row["guarantees"], [])
        # A valid deterministic e adds no failure allocation. If separate
        # calibration has failure beta, only the symbolic union bound
        # P(E∩G)≥1−alpha−beta is licensed; no numerical beta, calibration
        # procedure, independence, or accepted-batch guarantee is supplied.


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
        with tempfile.TemporaryDirectory(prefix="qr05bv-utility-") as directory:
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
        with tempfile.TemporaryDirectory(prefix="qr05bv-read-") as directory:
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
        self.assertIsNot(seen[0][0]["cases"], seen[1][0]["cases"])
        self.assertIsNot(seen[0][1], seen[1][1])
        self.assertIsNot(seen[0][1]["classes"], seen[1][1]["classes"])
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
        class_index = next(
            i for i, row in enumerate(original["report"]["plans"]) if row["kind"] == "class"
        )
        for path, replacement in (
            (("schema",), "qr05bv-capture-v1"),
            (("report", "schema"), "qr05bv-report-v1"),
            (("report", "classes", -1, "upper"), 2),
            (("report", "classes", -1, "lower", "norm"), True),
            (("report", "classes", 0, "bound"), "wrong"),
            (("report", "plans", class_index, "eligible"), 1),
            (("report", "plans", class_index, "guarantees", 0, "correct_singleton_at_least"), 1),
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
        self.assertIsNot(one["classes"], two["classes"])
        self.assertIsNot(one["plans"], two["plans"])
        self.assertEqual(one["schema"], "qr05bv-bt-baseline-v1")
        self.assertEqual(len(one["classes"]), 4)
        self.assertEqual(len(one["plans"]), 4)
        exact_tree(self, one["classes"], study.decode(original["report"]["classes"]))
        exact_tree(
            self,
            one["plans"],
            study.decode([r for r in original["report"]["plans"] if r["kind"] == "class"]),
        )
        # Same-type mathematical changes are not called shape errors. The fresh
        # engines compare complete values after their independent derivations.
        modified = copy.deepcopy(one)
        modified["classes"][0]["distance"] += Fraction(1)
        exact_tree(self, study._baseline_shape(modified), modified)

    def test_both_route_input_mutations_native_mismatch_and_late_source_changes(self):
        study = self.study
        snapshot = fixture_snapshot(study)

        def good(_protocol, _baseline):
            return {"value": Fraction(1)}

        def mutate_protocol(protocol, baseline):
            protocol["quota"] = True
            return good(protocol, baseline)

        def mutate_baseline(protocol, baseline):
            baseline["classes"][-1]["lower"]["norm"] = True
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
            ("protocol", ("coverage", "unexpanded_hypotheses"), True),
            ("protocol", ("regions", "Q", 0, 0), Fraction(0)),
            ("protocol", ("cases", 0, "fraction"), (0, 1)),
            ("protocol", ("density_bounds", 0, "upper", 1), 0),
            ("protocol", ("alpha",), [2, 40]),
            ("protocol", ("negative", "lambda"), [2, 32]),
            ("protocol", ("boxes", -1, "point"), "flat"),
            ("baseline", ("schema",), "qr05bt-br-baseline-v1"),
            ("baseline", ("classes", 0, "kind"), "collision"),
            ("baseline", ("classes", -1, "upper"), 2),
            ("baseline", ("classes", -1, "lower", "norm"), False),
            ("baseline", ("classes", -1, "points", 0, 0), 0),
            ("baseline", ("plans", -1, "eligible"), 0),
            ("baseline", ("plans", -1, "source"), "uniform"),
            ("baseline", ("plans", 0, "guarantees", 0, "correct_singleton_at_least"), 1),
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
            (("classes", -1, "lower", "norm"), Fraction(1)),
            (("cases", 1, "actual_contacts", 0, 0), Fraction(0)),
            (("cases", 2, "lower", "signed_value"), Fraction(-1)),
            (("plans", 4, "sufficient"), 0),
            (("baseline", "classes_equal"), 1),
            (("boxes", 3, "hypotheses", 0, "endpoints", 0, "within_error"), 1),
            (("boxes", -1, "unexpanded", "status"), "empty"),
            (("negative", "nested_support"), True),
            (("scale_pairs", -1, "constraints_scaled"), 1),
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
        self.directory = tempfile.TemporaryDirectory(prefix="qr05bv-evidence-")
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
        self.assertEqual(freeze["schema"], "qr05bv-source-freeze-v1")
        self.assertEqual(capture["schema"], "qr05bv-capture-v1")
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
        raise KeyboardInterrupt("QR-05BV 120-second suite deadline")

    signal.signal(signal.SIGALRM, suite_expired)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
