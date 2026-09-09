"""Source-bound BG tests: independent Boole/cofactor/scalar oracle.

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
PROTOCOL_SHA256 = "0944940c7da1f7e15e9d103695cc023964d602cf750056154346b01b35a98256"


def load_module(name):
    spec = importlib.util.spec_from_file_location("qr05bg_test_" + name, HERE / (name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("BG source could not be loaded")
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


def expected(protocol):
    """Whole report from verified Boole, cofactor inversion and scalar laws."""
    q = [functional(row) for row in identity(5)]
    volume = integrate(lambda _u, _v: Fraction(protocol["geometry"]["measure_factor"]))
    positions = []
    for declared in protocol["positions"]:
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
    for declared in protocol["cases"]:
        means = list(map(Fraction, declared["population_means"]))
        candidates = []
        for position in positions:
            coefficients = [dot(row, means) for row in position["coefficient_decoder"]]
            points = [
                *([Fraction(x), Fraction(y)] for x, y in protocol["corners"]),
                position["position"],
            ]
            reconstructed = [dot(coefficients, basis(*point)) for point in points]
            bound = max(map(abs, coefficients[:4])) + abs(coefficients[-1]) / 16
            admitted = bound <= 1
            target = functional(coefficients)
            candidates.append(
                {
                    "position_id": position["id"],
                    "coefficients": coefficients,
                    "admission_bound": bound,
                    "admission_status": "admitted" if admitted else "outside_sufficient_class",
                    "reconstructed_means": reconstructed,
                    "reconstruction_residual": [
                        x - y for x, y in zip(reconstructed, means, strict=True)
                    ],
                    "target": target,
                    "law": law(reconstructed),
                    "disclosure": {
                        "status": "identified" if admitted else "infeasible",
                        "target": target if admitted else None,
                    },
                }
            )
        by_id = {c["position_id"]: c for c in candidates}
        menus = []
        for menu in protocol["menus"]:
            feasible = [
                {key: by_id[name][key] for key in ("position_id", "coefficients", "target")}
                for name in menu["position_ids"]
                if by_id[name]["admission_status"] == "admitted"
            ]
            targets = sorted({item["target"] for item in feasible})
            interval = (
                None
                if not targets
                else {
                    "minimum": targets[0],
                    "maximum": targets[-1],
                    "width": targets[-1] - targets[0],
                }
            )
            menus.append(
                {
                    "id": menu["id"],
                    "position_ids": list(menu["position_ids"]),
                    "feasible": feasible,
                    "distinct_targets": targets,
                    "target_range": interval,
                    "gap_probe": (targets[0] + targets[1]) / 2 if len(targets) > 1 else None,
                    "status": "infeasible"
                    if not targets
                    else "identified"
                    if len(targets) == 1
                    else "ambiguous",
                }
            )
        cases.append(
            {
                "id": declared["id"],
                "population_means": means,
                "law": law(means),
                "candidates": candidates,
                "menus": menus,
            }
        )
    cases_by_id = {case["id"]: case for case in cases}
    witnesses = []
    for declared in protocol["witnesses"]:
        candidate_by_id = {
            c["position_id"]: c for c in cases_by_id[declared["case_id"]]["candidates"]
        }
        left, right = [candidate_by_id[name] for name in declared["position_ids"]]
        witnesses.append(
            {
                "id": declared["id"],
                "case_id": declared["case_id"],
                "position_ids": list(declared["position_ids"]),
                "admission_bounds": [left["admission_bound"], right["admission_bound"]],
                "coefficients_difference": [
                    y - x for x, y in zip(left["coefficients"], right["coefficients"], strict=True)
                ],
                "means_difference": [
                    y - x
                    for x, y in zip(
                        left["reconstructed_means"], right["reconstructed_means"], strict=True
                    )
                ],
                "target_difference": right["target"] - left["target"],
                "law_total_variation": sum(
                    (
                        abs(y["probability"] - x["probability"])
                        for x, y in zip(left["law"]["rows"], right["law"]["rows"], strict=True)
                    ),
                    Fraction(0),
                )
                / 2,
                "branch_state_disagreements": sum(
                    x["state_diagonal"] != y["state_diagonal"]
                    for x, y in zip(left["law"]["rows"], right["law"]["rows"], strict=True)
                ),
                "averaged_state_difference": [
                    y - x
                    for x, y in zip(
                        left["law"]["averaged_state"], right["law"]["averaged_state"], strict=True
                    )
                ],
                "disclosed_targets": [left["disclosure"]["target"], right["disclosure"]["target"]],
            }
        )
    declared = protocol["domain_control"]
    candidate = next(
        c
        for c in cases_by_id[declared["case_id"]]["candidates"]
        if c["position_id"] == declared["position_id"]
    )
    at_center = basis(Fraction(1, 2), Fraction(1, 2))[-1]
    domain_control = {
        "case_id": declared["case_id"],
        "position_id": declared["position_id"],
        "coefficients": list(candidate["coefficients"]),
        "admission_bound": candidate["admission_bound"],
        "admission_status": candidate["admission_status"],
        "bubble_range": [Fraction(0), at_center],
        "profile_range": [1 - 16 * at_center, Fraction(1)],
        "minimum_position": [Fraction(1, 2), Fraction(1, 2)],
        "maximum_position": [Fraction(0), Fraction(0)],
    }
    return {
        "geometry": {"volume": volume, "sigma": volume**4, "coefficient_integrals": q},
        "positions": positions,
        "cases": cases,
        "witnesses": witnesses,
        "domain_control": domain_control,
    }


@lru_cache(maxsize=1)
def evaluated():
    study = load_module("study")
    protocol = study.load_protocol()
    return study, protocol, study.compare_routes()


class ProtocolTests(unittest.TestCase):
    def test_pinned_public_population_and_finite_menu_contract(self):
        data = (HERE / "protocol.json").read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), PROTOCOL_SHA256)
        protocol = json.loads(data)
        self.assertEqual(protocol["study"], "QR-05BG")
        self.assertEqual(len(protocol["positions"]), 6)
        self.assertEqual(len(protocol["cases"]), 7)
        self.assertEqual(
            [m["id"] for m in protocol["menus"]],
            ["all", "center_only", "equality_pair", "shifted_pair", "center_near"],
        )
        names = [p["id"] for p in protocol["positions"]]
        self.assertEqual(len(set(names)), len(names))
        for p in protocol["positions"]:
            self.assertTrue(all(0 < Fraction(x) < 1 for x in p["position"]))
        for case in protocol["cases"]:
            exact_keys(self, case, "id population_means")
            self.assertEqual(len(case["population_means"]), 5)
            self.assertTrue(all(-1 <= Fraction(x) <= 1 for x in case["population_means"]))
        for menu in protocol["menus"]:
            exact_keys(self, menu, "id position_ids")
            self.assertEqual(len(menu["position_ids"]), len(set(menu["position_ids"])))
            self.assertTrue(set(menu["position_ids"]).issubset(names))

    def test_boole_moments_are_verified_before_tensor_integrals(self):
        protocol = json.loads((HERE / "protocol.json").read_bytes())
        nodes, weights = boole_rule()
        self.assertEqual(nodes, tuple(map(Fraction, protocol["third_oracle"]["nodes"])))
        self.assertEqual(weights, tuple(map(Fraction, protocol["third_oracle"]["weights"])))
        self.assertEqual(protocol["third_oracle"]["verify_moments_through"], 5)
        for a, b in itertools.product(range(6), repeat=2):
            self.assertEqual(
                integrate(lambda u, v, a=a, b=b: u**a * v**b), Fraction(1, (a + 1) * (b + 1))
            )


class MathematicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.oracle = expected(cls.protocol)

    def test_complete_native_wire_against_independent_oracle(self):
        self.assertEqual(self.report, self.oracle)
        self.assertEqual(self.study.encode(self.report), self.study.encode(self.oracle))

    def test_exact_fraction_fields_native_labels_and_typed_nulls(self):
        string_fields = {"id", "case_id", "position_id", "admission_status", "status"}

        def visit(value, path=()):
            if type(value) is dict:
                self.assertTrue(all(type(k) is str for k in value))
                for key, child in value.items():
                    visit(child, (*path, key))
            elif type(value) is list:
                for i, child in enumerate(value):
                    visit(child, (*path, i))
            elif value is None:
                self.assertTrue(
                    path[-1] in {"target_range", "gap_probe"}
                    or path[-2:] == ("disclosure", "target"),
                    path,
                )
            elif path[-1] in string_fields or "position_ids" in path:
                self.assertIs(type(value), str, path)
            elif path[-1] == "branch_state_disagreements" or "outcomes" in path:
                self.assertIs(type(value), int, path)
            else:
                self.assertIs(type(value), Fraction, path)
                encoded = self.study.encode(value)
                self.assertIs(type(encoded), str)
                self.assertEqual(str(Fraction(encoded)), encoded)

        visit(self.report)

    def test_inversion_reconstruction_and_integrals_use_each_hypothesis(self):
        q = self.report["geometry"]["coefficient_integrals"]
        positions = {p["id"]: p for p in self.report["positions"]}
        for position in positions.values():
            a, d = position["evaluation_matrix"], position["coefficient_decoder"]
            self.assertEqual(multiply(a, d), identity(5))
            self.assertEqual(multiply(d, a), identity(5))
            self.assertEqual(position["left_inverse"], identity(5))
            self.assertEqual(position["right_inverse"], identity(5))
            self.assertEqual(row_rank(a), 5)
            self.assertEqual(position["full_residual"], [0] * 5)
        for case in self.report["cases"]:
            means = case["population_means"]
            for candidate in case["candidates"]:
                position = positions[candidate["position_id"]]
                coefficients = candidate["coefficients"]
                self.assertEqual(coefficients[:4], means[:4])
                self.assertEqual(
                    coefficients[4],
                    (means[4] - dot(position["basis"][:4], means[:4])) / position["basis"][4],
                )
                points = [[Fraction(x), Fraction(y)] for x, y in self.protocol["corners"]] + [
                    position["position"]
                ]
                reconstructed = [dot(coefficients, basis(*point)) for point in points]
                self.assertEqual(reconstructed, means)
                self.assertEqual(candidate["reconstructed_means"], reconstructed)
                self.assertEqual(candidate["reconstruction_residual"], [0] * 5)
                self.assertEqual(candidate["target"], functional(coefficients))
                self.assertEqual(candidate["target"], dot(q, coefficients))

    def test_all_local_laws_including_rejected_hypotheses_and_zero_branches(self):
        count = zeros = rejected = 0
        for case in self.report["cases"]:
            self.assertEqual(
                [c["position_id"] for c in case["candidates"]],
                [p["id"] for p in self.protocol["positions"]],
            )
            for candidate in case["candidates"]:
                self.assertEqual(candidate["law"], law(candidate["reconstructed_means"]))
                self.assertEqual(candidate["law"], case["law"])
                rejected += candidate["admission_status"] == "outside_sufficient_class"
            laws = [case["law"], *[c["law"] for c in case["candidates"]]]
            for result in laws:
                rows = result["rows"]
                self.assertEqual(len(rows), 32)
                self.assertEqual(sum(r["probability"] for r in rows), 1)
                self.assertEqual(sum(result["averaged_state"]), 1)
                for row in rows:
                    self.assertGreaterEqual(row["probability"], 0)
                    self.assertEqual(sum(row["state_diagonal"]), row["probability"])
                    self.assertTrue(all(x >= 0 for x in row["state_diagonal"]))
                    zeros += row["probability"] == 0
                count += len(rows)
        self.assertEqual(count, 1568)
        self.assertGreater(zeros, 0)
        self.assertGreater(rejected, 0)

    def test_menu_filtering_order_and_monotonicity_without_position_averaging(self):
        for case in self.report["cases"]:
            candidates = {c["position_id"]: c for c in case["candidates"]}
            menus = case["menus"]
            for menu in menus:
                expected_feasible = [
                    {
                        key: candidates[name][key]
                        for key in ("position_id", "coefficients", "target")
                    }
                    for name in menu["position_ids"]
                    if candidates[name]["admission_status"] == "admitted"
                ]
                self.assertEqual(menu["feasible"], expected_feasible)
                self.assertEqual(
                    menu["distinct_targets"], sorted({x["target"] for x in expected_feasible})
                )
                for entry in menu["feasible"]:
                    self.assertEqual(entry["target"], candidates[entry["position_id"]]["target"])
            for small, large in itertools.product(menus, repeat=2):
                if set(small["position_ids"]).issubset(large["position_ids"]):
                    selected = {x["position_id"]: x for x in large["feasible"]}
                    self.assertEqual(
                        small["feasible"],
                        [selected[name] for name in small["position_ids"] if name in selected],
                    )
                    self.assertTrue(
                        set(small["distinct_targets"]).issubset(large["distinct_targets"])
                    )

    def test_exact_finite_sets_empty_refusal_and_nonattainable_hull_gap(self):
        statuses = set()
        for case in self.report["cases"]:
            for menu in case["menus"]:
                targets = menu["distinct_targets"]
                statuses.add(menu["status"])
                self.assertEqual(targets, sorted(set(targets)))
                if not targets:
                    self.assertEqual(menu["status"], "infeasible")
                    self.assertEqual(menu["feasible"], [])
                    self.assertIsNone(menu["target_range"])
                    self.assertIsNone(menu["gap_probe"])
                else:
                    self.assertEqual(
                        menu["target_range"],
                        {
                            "minimum": targets[0],
                            "maximum": targets[-1],
                            "width": targets[-1] - targets[0],
                        },
                    )
                    self.assertEqual(
                        menu["status"], "identified" if len(targets) == 1 else "ambiguous"
                    )
                    if len(targets) == 1:
                        self.assertIsNone(menu["gap_probe"])
                    else:
                        probe = menu["gap_probe"]
                        self.assertEqual(probe, (targets[0] + targets[1]) / 2)
                        self.assertLess(targets[0], probe)
                        self.assertLess(probe, targets[1])
                        self.assertNotIn(probe, targets)
        self.assertEqual(statuses, {"infeasible", "identified", "ambiguous"})

    def test_target_uniqueness_fixes_coefficients_but_not_position_in_this_model(self):
        q = self.report["geometry"]["coefficient_integrals"]
        self.assertNotEqual(q[4], 0)
        repeated_positions = 0
        for case in self.report["cases"]:
            for menu in case["menus"]:
                coefficients = {tuple(entry["coefficients"]) for entry in menu["feasible"]}
                self.assertEqual(len(coefficients), len(menu["distinct_targets"]))
                for entry in menu["feasible"]:
                    self.assertEqual(entry["coefficients"][:4], case["population_means"][:4])
                    self.assertEqual(
                        entry["coefficients"][4],
                        (entry["target"] - dot(q[:4], case["population_means"][:4])) / q[4],
                    )
                if menu["status"] == "identified":
                    self.assertEqual(len(coefficients), 1)
                    repeated_positions += len(menu["feasible"]) > 1
        self.assertGreater(repeated_positions, 0)
        zero = next(c for c in self.report["cases"] if c["id"] == "zero")
        all_menu = next(m for m in zero["menus"] if m["id"] == "all")
        self.assertEqual(len(all_menu["feasible"]), 6)
        self.assertEqual(len(all_menu["distinct_targets"]), 1)

    def test_admission_boundary_and_disclosure_do_not_change_public_law(self):
        boundary_admitted = refused = 0
        for case in self.report["cases"]:
            for candidate in case["candidates"]:
                c = candidate["coefficients"]
                bound = max(map(abs, c[:4])) + abs(c[4]) / 16
                admitted = bound <= 1
                self.assertEqual(candidate["admission_bound"], bound)
                self.assertEqual(
                    candidate["admission_status"],
                    "admitted" if admitted else "outside_sufficient_class",
                )
                self.assertEqual(
                    candidate["disclosure"],
                    {
                        "status": "identified" if admitted else "infeasible",
                        "target": candidate["target"] if admitted else None,
                    },
                )
                boundary_admitted += admitted and bound == 1
                refused += not admitted
                self.assertEqual(candidate["law"], case["law"])
        self.assertGreater(boundary_admitted, 0)
        self.assertGreater(refused, 0)
        unit = next(c for c in self.report["cases"] if c["id"] == "unit_interior")
        center = next(c for c in unit["candidates"] if c["position_id"] == "center")
        self.assertEqual(center["admission_bound"], 1)
        self.assertEqual(center["disclosure"]["status"], "identified")

    def test_witnesses_distinguish_target_ambiguity_from_harmless_position_ambiguity(self):
        cases = {c["id"]: c for c in self.report["cases"]}
        for witness in self.report["witnesses"]:
            candidates = {c["position_id"]: c for c in cases[witness["case_id"]]["candidates"]}
            left, right = [candidates[name] for name in witness["position_ids"]]
            self.assertTrue(all(c["admission_status"] == "admitted" for c in (left, right)))
            self.assertEqual(left["law"], right["law"])
            self.assertEqual(witness["law_total_variation"], 0)
            self.assertEqual(witness["branch_state_disagreements"], 0)
            self.assertEqual(witness["averaged_state_difference"], [0] * 32)
            self.assertEqual(witness["means_difference"], [0] * 5)
            self.assertEqual(witness["target_difference"], right["target"] - left["target"])
            self.assertEqual(witness["disclosed_targets"], [left["target"], right["target"]])
            if witness["id"] == "target_ambiguity":
                self.assertNotEqual(witness["target_difference"], 0)
                self.assertNotEqual(left["coefficients"], right["coefficients"])
            else:
                self.assertEqual(witness["id"], "harmless_position_ambiguity")
                self.assertEqual(witness["target_difference"], 0)
                self.assertEqual(left["coefficients"], right["coefficients"])

    def test_globally_valid_but_domain_excluded_is_not_physical_refusal(self):
        control = self.report["domain_control"]
        self.assertEqual(control["coefficients"], [1, 1, 1, 1, -16])
        self.assertGreater(control["admission_bound"], 1)
        self.assertEqual(control["admission_status"], "outside_sufficient_class")
        self.assertEqual(control["bubble_range"], [0, Fraction(1, 16)])
        self.assertEqual(control["profile_range"], [0, 1])
        # u(1-u)=1/4-(u-1/2)^2 and the analogous v identity bound b.
        for x in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
            self.assertEqual(x * (1 - x), Fraction(1, 4) - (x - Fraction(1, 2)) ** 2)
        self.assertEqual(dot(control["coefficients"], basis(*control["minimum_position"])), 0)
        self.assertEqual(dot(control["coefficients"], basis(*control["maximum_position"])), 1)
        case = next(c for c in self.report["cases"] if c["id"] == control["case_id"])
        candidate = next(
            c for c in case["candidates"] if c["position_id"] == control["position_id"]
        )
        self.assertEqual(candidate["disclosure"], {"status": "infeasible", "target": None})
        self.assertEqual(candidate["law"], case["law"])


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
        with tempfile.TemporaryDirectory(prefix="det8-qr05bg-loader-") as temporary:
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


def analysis_mutations(original):
    """Stream representative wire fields plus late, refusal and finite-set mutations."""
    leaves = []

    def collect(value, path=()):
        if type(value) is dict:
            for key, child in value.items():
                collect(child, (*path, key))
        elif type(value) is list:
            if value:
                collect(value[0], (*path, 0))
        else:
            leaves.append((path, value))

    collect(original)
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
        yield "scalar " + repr(path), changed
    paths = [
        ("mathematics", "cases", -1, "law", "rows", -1, "probability"),
        ("mathematics", "cases", -1, "law", "rows", -1, "state_diagonal", -1),
        ("mathematics", "cases", -1, "candidates", -1, "target"),
        ("mathematics", "cases", -1, "candidates", -1, "law", "rows", -1, "probability"),
        ("mathematics", "cases", -1, "candidates", -1, "law", "rows", -1, "state_diagonal", -1),
        ("mathematics", "cases", -1, "candidates", -1, "law", "averaged_state", -1),
        ("mathematics", "witnesses", -1, "averaged_state_difference", -1),
        ("mathematics", "domain_control", "profile_range", -1),
    ]
    for path in paths:
        changed = copy.deepcopy(original)
        set_path(changed, path, str(Fraction(get_path(changed, path)) + 1))
        yield "late " + repr(path), changed
    for case_index, case in enumerate(original["mathematics"]["cases"]):
        for candidate_index, candidate in enumerate(case["candidates"]):
            if candidate["disclosure"]["target"] is None:
                path = (
                    "mathematics",
                    "cases",
                    case_index,
                    "candidates",
                    candidate_index,
                    "disclosure",
                    "target",
                )
                changed = copy.deepcopy(original)
                set_path(changed, path, "0")
                yield "refusal target " + repr(path), changed
                break
        for menu_index, menu in enumerate(case["menus"]):
            prefix = ("mathematics", "cases", case_index, "menus", menu_index)
            if menu["status"] == "infeasible":
                changed = copy.deepcopy(original)
                set_path(
                    changed,
                    (*prefix, "target_range"),
                    {"minimum": "0", "maximum": "0", "width": "0"},
                )
                yield "false empty hull " + repr(prefix), changed
                break
            if menu["status"] == "ambiguous":
                changed = copy.deepcopy(original)
                set_path(changed, (*prefix, "gap_probe"), menu["distinct_targets"][0])
                yield "attainable false gap " + repr(prefix), changed
                break
    for path in [
        ("mathematics", "positions"),
        ("mathematics", "positions", 0, "coefficient_decoder", 0),
        ("mathematics", "cases", -1, "candidates", -1, "law", "rows"),
        ("mathematics", "cases", 0, "menus", 0, "feasible"),
    ]:
        changed = copy.deepcopy(original)
        set_path(changed, path, get_path(changed, path)[:-1])
        yield "truncated " + repr(path), changed
    for path in [
        ("mathematics", "cases", 0, "law", "rows", -1, "outcomes", 0),
        ("mathematics", "witnesses", 0, "branch_state_disagreements"),
        ("bf_restriction", "positions"),
    ]:
        changed = copy.deepcopy(original)
        set_path(changed, path, True)
        yield "native type " + repr(path), changed
    for key in original:
        changed = copy.deepcopy(original)
        del changed[key]
        yield "missing " + key, changed
    changed = copy.deepcopy(original)
    changed["actual_position"] = "hidden origin"
    yield "extra hidden origin", changed


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_module("study")
        self.directory = tempfile.TemporaryDirectory(prefix="det8-qr05bg-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.freeze = self.root / "freeze.json"
        self.capture_path = self.root / "capture.json"
        self.sources = {"synthetic/source.py": {"bytes": 1, "sha256": "a" * 64}}
        self.small = {
            "mathematics": {"exact": "1/3", "count": 1},
            "bf_restriction": {"branches": 1},
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
        self.assertEqual(evidence["schema"], "QR-05BG-evidence-v1")
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
            (("analysis", "bf_restriction", "branches"), True),
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


def selected_bf_fixture(study, report):
    """Selected predecessor-shaped data authored solely from the new report."""
    previous = {"geometry": copy.deepcopy(report["geometry"]), "placements": []}
    mapping = {"zero": "zero", "plus": "plus", "minus": "minus", "asymmetric": "asymmetric_bubble"}
    for position in report["positions"]:
        old = copy.deepcopy(position)
        old["profiles"] = "unselected moved-profile branches"
        old["collision"] = "unselected"
        old["candidate_residual"] = "unselected"
        if position["id"] == "center":
            old["profiles"] = []
            for case in report["cases"]:
                if case["id"] not in mapping:
                    continue
                candidate = next(c for c in case["candidates"] if c["position_id"] == "center")
                old["profiles"].append(
                    {
                        "id": mapping[case["id"]],
                        "coefficients": candidate["coefficients"],
                        "admission_bound": candidate["admission_bound"],
                        "sample_means": candidate["reconstructed_means"],
                        "target": candidate["target"],
                        "full": {
                            "rows": [
                                {**row, "estimate": Fraction(0)} for row in candidate["law"]["rows"]
                            ],
                            "mean": "unselected",
                            "variance": "unselected",
                        },
                        "reduced": "unselected",
                        "marginalization": "unselected",
                    }
                )
        previous["placements"].append(old)
    return study.encode({"analysis": {"mathematics": previous}})


class HistoricalBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def restriction(self, document, current=None):
        data = json.dumps(document, sort_keys=True).encode()
        identities = dict(self.study.BF_IDENTITIES)
        identities["results.json"] = hashlib.sha256(data).hexdigest()
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=data),
            mock.patch.object(self.study, "BF_IDENTITIES", identities),
            mock.patch.object(
                self.study, "_load_engine", side_effect=AssertionError("historical executor")
            ),
        ):
            return self.study._bf_restriction(self.report if current is None else current)

    def test_selected_geometry_and_center_laws_exclude_old_moved_and_score_controls(self):
        document = selected_bf_fixture(self.study, self.report)
        summary = {"status": "matched", "positions": 6, "profiles": 4, "branches": 128}
        self.assertEqual(self.restriction(document), summary)
        changed = copy.deepcopy(document)
        placements = changed["analysis"]["mathematics"]["placements"]
        for p in placements:
            p["collision"] = None
            p["candidate_residual"] = None
            if p["id"] != "center":
                p["profiles"] = None
            else:
                for profile in p["profiles"]:
                    profile["reduced"] = None
                    profile["marginalization"] = None
                    profile["full"]["mean"] = None
                    profile["full"]["variance"] = None
                    for row in profile["full"]["rows"]:
                        row["estimate"] = "not selected"
        self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
        self.assertEqual(self.restriction(changed), summary)

    def test_selected_historical_geometry_and_branch_mutations(self):
        document = selected_bf_fixture(self.study, self.report)
        old = document["analysis"]["mathematics"]
        center_index = next(i for i, p in enumerate(old["placements"]) if p["id"] == "center")
        paths = [
            ("geometry", "volume"),
            ("geometry", "sigma"),
            ("geometry", "coefficient_integrals", -1),
        ]
        for i in range(6):
            paths += [
                ("placements", i, key, -1)
                for key in ("position", "basis", "full_weights", "full_residual")
            ]
            paths += [
                ("placements", i, key, -1, -1)
                for key in (
                    "evaluation_matrix",
                    "coefficient_decoder",
                    "left_inverse",
                    "right_inverse",
                )
            ]
        profile = ("placements", center_index, "profiles", -1)
        paths += [(*profile, key) for key in ("admission_bound", "target")]
        paths += [(*profile, key, -1) for key in ("coefficients", "sample_means")]
        paths += [
            (*profile, "full", "rows", -1, "probability"),
            (*profile, "full", "rows", -1, "state_diagonal", -1),
        ]
        for path in paths:
            changed = copy.deepcopy(document)
            full = ("analysis", "mathematics", *path)
            set_path(changed, full, str(Fraction(get_path(changed, full)) + 1))
            self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)
        changed = copy.deepcopy(document)
        path = ("analysis", "mathematics", *profile, "full", "rows", -1, "outcomes", 0)
        set_path(changed, path, True)
        self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
        with self.assertRaises(ValueError):
            self.restriction(changed)

    def test_both_public_and_candidate_laws_and_unique_center_are_selected(self):
        document = selected_bf_fixture(self.study, self.report)
        case_index = next(i for i, c in enumerate(self.report["cases"]) if c["id"] == "asymmetric")
        candidate_index = next(
            i
            for i, c in enumerate(self.report["cases"][case_index]["candidates"])
            if c["position_id"] == "center"
        )
        candidate = ("cases", case_index, "candidates", candidate_index)
        mutations = [
            (("cases", case_index, "population_means", 0), Fraction(7)),
            ((*candidate, "admission_status"), "outside_sufficient_class"),
            ((*candidate, "reconstructed_means", 0), Fraction(7)),
            ((*candidate, "position_id"), "absent"),
            (("cases", case_index, "law", "rows", -1, "probability"), Fraction(7)),
            ((*candidate, "law", "rows", -1, "state_diagonal", -1), Fraction(7)),
        ]
        for path, value in mutations:
            current = copy.deepcopy(self.report)
            set_path(current, path, value)
            self.assertNotEqual(self.study.canonical(current), self.study.canonical(self.report))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(document, current)
        current = copy.deepcopy(self.report)
        current["cases"].append(copy.deepcopy(current["cases"][0]))
        with self.assertRaises(ValueError):
            self.restriction(document, current)
        current = copy.deepcopy(self.report)
        candidates = current["cases"][case_index]["candidates"]
        candidates.append(copy.deepcopy(candidates[candidate_index]))
        with self.assertRaises(ValueError):
            self.restriction(document, current)
        # BF had no corresponding base-profile averaged-state field. That
        # new quantity is checked by our oracle, not invented as old evidence.
        current = copy.deepcopy(self.report)
        current["cases"][case_index]["law"]["averaged_state"][0] += 1
        self.assertEqual(
            self.restriction(document, current),
            {"status": "matched", "positions": 6, "profiles": 4, "branches": 128},
        )

    def test_historical_identity_precedes_parsing(self):
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=b"{}"),
            mock.patch.object(
                self.study, "_parse_json", side_effect=AssertionError("unverified historical input")
            ),
            self.assertRaises(ValueError),
        ):
            self.study._bf_restriction(self.report)

    def test_analysis_is_only_math_and_selected_restriction_not_new_observer(self):
        with mock.patch.object(self.study, "compare_routes", return_value=self.report):
            result = self.study.analysis()
        exact_keys(self, result, "mathematics bf_restriction")
        self.assertEqual(result["mathematics"], self.study.encode(self.report))
        self.assertEqual(
            result["bf_restriction"],
            {"status": "matched", "positions": 6, "profiles": 4, "branches": 128},
        )


class SourceIdentityTests(unittest.TestCase):
    def test_exact_eleven_current_and_bf_source_identities(self):
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
                "test_qr05bg.py",
            )
        ]
        previous = [
            HERE.parent / "qr-05bf-known-placement-portability-2026-09-08" / name
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

    def test_protocol_hash_and_parse_share_one_snapshot(self):
        study = load_module("study")
        data = (HERE / "protocol.json").read_bytes()
        with (
            mock.patch.object(study, "_read_bounded", return_value=data) as read,
            mock.patch.object(study, "_bytes_identity", wraps=study._bytes_identity) as hashed,
            mock.patch.object(study, "_parse_json", wraps=study._parse_json) as parsed,
        ):
            self.assertEqual(study.load_protocol(), json.loads(data))
        self.assertEqual(read.call_count, 1)
        self.assertEqual(hashed.call_count, 1)
        self.assertEqual(parsed.call_count, 1)
        self.assertIs(hashed.call_args.args[0], data)
        self.assertIs(parsed.call_args.args[0], data)
        with (
            mock.patch.object(study, "_read_bounded", return_value=b"{}"),
            mock.patch.object(
                study, "_parse_json", side_effect=AssertionError("unverified protocol")
            ),
            self.assertRaises(ValueError),
        ):
            study.load_protocol()

    def test_authenticated_protocol_names_order_and_native_menu_schema(self):
        study = load_module("study")
        protocol = json.loads((HERE / "protocol.json").read_bytes())
        for path, value in (
            (("positions", 0, "id"), True),
            (("cases", 0, "id"), "unknown"),
            (("stations", 4), "unknown"),
            (("menus", 0, "position_ids", 1), "center"),
            (("menus", 1, "position_ids"), []),
            (("menus", 1), {"id": "center_only", "position_ids": ["center"], "prior": "1"}),
        ):
            changed = copy.deepcopy(protocol)
            set_path(changed, path, value)
            data = json.dumps(changed).encode()
            with (
                self.subTest(path=path),
                mock.patch.object(study, "_read_bounded", return_value=data),
                mock.patch.object(
                    study, "_bytes_identity", return_value={"sha256": PROTOCOL_SHA256}
                ),
                self.assertRaises(ValueError),
            ):
                study.load_protocol()


if __name__ == "__main__":
    unittest.main()
