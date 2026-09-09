"""Bounded independent BO tests; no mathematical evaluation at import.

The oracle uses endpoint antiderivatives, rational orthogonalization, a
permutation determinant, and scalar probability contractions. Only the new
driver is loaded lazily; old numerical engines or test modules are not used.
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
SYMBOLS = ((0, 0), (0, 1), (1, 0), (1, 1))


def load_study():
    spec = importlib.util.spec_from_file_location("_qr05bo_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load BO driver")
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


def endpoint_moment(rectangle, degree):
    a, b, c, d = [Fraction(*pair) for pair in rectangle]
    order = degree + 1
    return (b**order - a**order) * (d**order - c**order) / order**2


def moment_matrix(protocol):
    return [
        [endpoint_moment(protocol["regions"][region], degree) for degree in range(3)]
        for region in ("Q", "I1", "I2")
    ]


def permutation_determinant(matrix):
    total = Fraction(0)
    for order in itertools.permutations(range(len(matrix))):
        inversions = sum(
            order[i] > order[j] for i in range(len(order)) for j in range(i + 1, len(order))
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(order):
            term *= matrix[row][column]
        total += term
    return total


def orthogonal_solve(matrix, rhs):
    """Orthogonalize equations and their right sides, not a pivoted elimination."""
    basis = []
    for original, value in zip(matrix, rhs, strict=True):
        row = list(original)
        for previous, previous_value in basis:
            factor = dot(row, previous) / dot(previous, previous)
            row = [a - factor * b for a, b in zip(row, previous, strict=True)]
            value -= factor * previous_value
        if not any(row):
            raise ValueError("independent oracle requires nonsingular moment equations")
        basis.append((row, value))
    return [
        sum((value * row[index] / dot(row, row) for row, value in basis), Fraction(0))
        for index in range(len(rhs))
    ]


def multiply(left, right):
    return [[dot(row, list(column)) for column in zip(*right, strict=True)] for row in left]


def inverse_oracle(matrix):
    columns = [
        orthogonal_solve(matrix, [Fraction(index == column) for index in range(len(matrix))])
        for column in range(len(matrix))
    ]
    return [list(row) for row in zip(*columns, strict=True)]


def mass_coefficients(moments, eta, scale):
    eta, scale = Fraction(eta), Fraction(scale)
    return [
        [scale * (row[0] + eta * row[1]) / 2, scale * (row[1] + eta * row[2]) / 2]
        for row in moments
    ]


def forward_mass(moments, eta, scale, delta):
    coefficients = [
        Fraction(scale, 2),
        Fraction(scale, 2) * (eta + delta),
        Fraction(scale, 2) * eta * delta,
    ]
    return [dot(row, coefficients) for row in moments]


def one_point(q):
    first, second = q
    return [1 - second, second - first, Fraction(0), first]


def records(q, quota):
    probabilities = one_point(q)
    result = []
    for word in itertools.product(range(4), repeat=quota):
        probability = Fraction(1)
        for symbol in word:
            probability *= probabilities[symbol]
        result.append({"y": [list(SYMBOLS[symbol]) for symbol in word], "p": probability})
    return result


def first_law(q, quota):
    return [
        {"y": list(word), "p": q ** sum(word) * (1 - q) ** (quota - sum(word))}
        for word in itertools.product((0, 1), repeat=quota)
    ]


def world_oracle(item, moments, quota):
    eta, scale, delta = item["eta"], item["scale"], Fraction(*item["delta"])
    coefficients = mass_coefficients(moments, eta, scale)
    masses = forward_mass(moments, eta, scale, delta)
    normalized = [
        Fraction(scale, 2) / masses[0],
        Fraction(scale, 2) * (eta + delta) / masses[0],
        Fraction(scale, 2) * eta * delta / masses[0],
    ]
    q = [masses[1] / masses[0], masses[2] / masses[0]]
    rows = records(q, quota)
    marginal = []
    for word in itertools.product((0, 1), repeat=quota):
        probability = sum(
            (row["p"] for row in rows if [pair[0] for pair in row["y"]] == list(word)), Fraction(0)
        )
        marginal.append({"y": list(word), "p": probability})
    recovered = orthogonal_solve(moments, [Fraction(1), *q])
    return {
        "id": item["id"],
        "eta": eta,
        "scale": scale,
        "delta": delta,
        "volumes": [row[0] for row in coefficients],
        "target": coefficients[1][0] / coefficients[0][0],
        "mass_coefficients": coefficients,
        "mass": masses,
        "normalized_coefficients": normalized,
        "q": q,
        "one_point": one_point(q),
        "records": rows,
        "marginal": marginal,
        "recovered": recovered,
        "reconstruction_equal": recovered == normalized,
        "marginal_equal": marginal == first_law(q[0], quota),
        "independent_10": q[0] * (1 - q[1]),
    }


def hypothesis(geometry, q, solution, bound, moments):
    eta, scale = geometry["eta"], geometry["scale"]
    coefficients = mass_coefficients(moments, eta, scale)
    a, b = coefficients[1]
    c, d = coefficients[0]
    numerator, divisor = a - q[0] * c, q[0] * d - b
    candidate = [numerator / divisor] if divisor else []
    lower, upper = [Fraction(*pair) for pair in bound["interval"]]
    residual = []
    if candidate and lower <= candidate[0] <= upper:
        masses = forward_mass(moments, eta, scale, candidate[0])
        residual = [masses[2] - q[1] * masses[0]]
    admitted, normalized = [], []
    # Independently use the reconstructed polynomial to certify factorization.
    # Do not divide by a zero/negative constant coefficient.
    if solution[0] > 0:
        alpha, beta = solution[1] / solution[0], solution[2] / solution[0]
        delta = alpha - eta
        if beta == eta * delta and lower <= delta <= upper:
            masses = forward_mass(moments, eta, scale, delta)
            normalized = [
                Fraction(scale, 2) / masses[0],
                Fraction(scale, 2) * (eta + delta) / masses[0],
                Fraction(scale, 2) * eta * delta / masses[0],
            ]
            if normalized != solution or [masses[1] / masses[0], masses[2] / masses[0]] != q:
                raise ValueError("factorization did not pass independent forward equations")
            admitted = [delta]
    if bool(admitted) != (residual == [Fraction(0)]) or (admitted and admitted != candidate):
        raise ValueError("independent reconstructed factorization and inverse diagnostics disagree")
    return {
        "id": geometry["id"],
        "inverse_numerator": numerator,
        "inverse_denominator": divisor,
        "candidate": candidate,
        "delta_set": admitted,
        "status": "feasible" if admitted else "infeasible",
        "second_residual": residual,
        "normalized_coefficients": normalized,
    }


def classes(worlds, field):
    keys, members = [], []
    for row in worlds:
        value = row[field]
        if value not in keys:
            keys.append(value)
            members.append([])
        members[keys.index(value)].append(row)
    return [
        {
            "worlds": [row["id"] for row in group],
            "targets": sorted({row["target"] for row in group}),
            "identified": len({row["target"] for row in group}) == 1,
        }
        for group in members
    ]


def expected(protocol):
    moments = moment_matrix(protocol)
    inverse = inverse_oracle(moments)
    identity = [[Fraction(i == j) for j in range(3)] for i in range(3)]
    worlds = [world_oracle(item, moments, protocol["quota"]) for item in protocol["fixtures"]]
    by_world = {row["id"]: row for row in worlds}
    data = [{"id": name, "q": list(by_world[name]["q"])} for name in protocol["fixture_data"]]
    data += [
        {"id": row["id"], "q": [Fraction(*pair) for pair in row["q"]]}
        for row in protocol["control_data"]
    ]
    for row in data:
        row["moment_solution"] = orthogonal_solve(moments, [Fraction(1), *row["q"]])
        row["one_point"] = one_point(row["q"])
    cases = []
    target_by_label = {
        row["id"]: Fraction(16 + row["eta"], 16 * (4 + row["eta"]))
        for row in protocol["geometries"]
    }
    for bound in protocol["density_bounds"]:
        for datum in data:
            hypotheses = [
                hypothesis(item, datum["q"], datum["moment_solution"], bound, moments)
                for item in protocol["geometries"]
            ]
            feasible = [row["id"] for row in hypotheses if row["delta_set"]]
            targets = sorted({target_by_label[name] for name in feasible})
            cases.append(
                {
                    "id": bound["id"] + "/" + datum["id"],
                    "bound": bound["id"],
                    "data": datum["id"],
                    "q": datum["q"],
                    "hypotheses": hypotheses,
                    "worlds": feasible,
                    "targets": targets,
                    "status": "infeasible"
                    if not targets
                    else "identified"
                    if len(targets) == 1
                    else "ambiguous",
                }
            )
    by_case = {row["id"]: row for row in cases}
    monotonicity = []
    for tight, broad in itertools.pairwise(protocol["density_bounds"]):
        for datum in data:
            left, right = [by_case[bound["id"] + "/" + datum["id"]] for bound in (tight, broad)]
            broad_deltas = {row["id"]: row["delta_set"] for row in right["hypotheses"]}
            monotonicity.append(
                {
                    "tight": tight["id"],
                    "broad": broad["id"],
                    "data": datum["id"],
                    "world_subset": set(left["worlds"]).issubset(right["worlds"]),
                    "target_subset": set(left["targets"]).issubset(right["targets"]),
                    "nuisance_preserved": all(
                        row["delta_set"] == broad_deltas[row["id"]]
                        for row in left["hypotheses"]
                        if row["delta_set"]
                    ),
                }
            )
    collisions = []
    for name, first, second in (
        ("inherited_whole_point", "flat_1", "conformal_0"),
        ("membership_only", "flat_interior", "conformal_interior"),
    ):
        left, right = by_world[first], by_world[second]
        collisions.append(
            {
                "id": name,
                "worlds": [first, second],
                "first_equal": left["marginal"] == right["marginal"],
                "joint_equal": left["records"] == right["records"],
                "point_equal": left["normalized_coefficients"] == right["normalized_coefficients"],
                "q2_gap": left["q"][1] - right["q"][1],
                "target_gap": left["target"] - right["target"],
            }
        )
    scale_pairs = []
    for name in protocol["fixture_data"]:
        first, second = by_world[name], by_world[name + "_x4"]
        factors = [a / b for a, b in zip(second["volumes"], first["volumes"], strict=True)]
        if len(set(factors)) != 1:
            raise ValueError("inconsistent geometric volume transport")
        scale_pairs.append(
            {
                "worlds": [name, name + "_x4"],
                "volume_factor": factors[0],
                "target_equal": first["target"] == second["target"],
                "point_equal": first["normalized_coefficients"]
                == second["normalized_coefficients"],
                "joint_equal": first["records"] == second["records"],
            }
        )
    support = []
    for word in itertools.product(SYMBOLS, repeat=protocol["quota"]):
        possible = (1, 0) not in word
        support.append(
            {
                "y": [list(pair) for pair in word],
                "possible": possible,
                "worlds": [row["id"] for row in protocol["geometries"]] if possible else [],
                "targets": sorted(set(target_by_label.values())) if possible else [],
            }
        )
    return {
        "schema": "qr05bo-report-v1",
        "reconstruction": {
            "moments": moments,
            "determinant": permutation_determinant(moments),
            "inverse": inverse,
            "left_identity": multiply(inverse, moments) == identity,
            "right_identity": multiply(moments, inverse) == identity,
        },
        "worlds": worlds,
        "data": data,
        "cases": cases,
        "classes": {
            "first": classes(worlds, "marginal"),
            "joint": classes(worlds, "records"),
            "point": classes(worlds, "normalized_coefficients"),
        },
        "collisions": collisions,
        "scale_pairs": scale_pairs,
        "monotonicity": monotonicity,
        "support": support,
    }


def query(q, bound="two"):
    return {
        "schema": "qr05bo-query-v1",
        "data_kind": "population_pair",
        "q": [[value.numerator, value.denominator] for value in q],
        "density_bound": bound,
        "bound_basis": "external_assumption",
    }


def query_answer(case):
    return {
        "worlds": case["worlds"],
        "targets": case["targets"],
        "status": case["status"],
        "nuisance": [
            {"id": row["id"], "delta": row["delta_set"][0]}
            for row in case["hypotheses"]
            if row["delta_set"]
        ],
    }


class MathematicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def test_entire_native_report_and_declared_census(self):
        exact_tree(self, self.report, expected(self.protocol))
        self.assertEqual(len(self.report["worlds"]), 16)
        self.assertEqual(sum(len(row["records"]) for row in self.report["worlds"]), 4096)
        self.assertEqual(sum(len(row["marginal"]) for row in self.report["worlds"]), 256)
        self.assertEqual(len(self.report["data"]), 12)
        self.assertEqual(len(self.report["cases"]), 48)
        self.assertEqual(sum(len(row["hypotheses"]) for row in self.report["cases"]), 192)
        self.assertEqual(len(self.report["monotonicity"]), 36)
        self.assertEqual(len(self.report["support"]), 256)

    def test_three_moments_nonsingular_and_both_inverse_orientations(self):
        reconstruction = self.report["reconstruction"]
        matrix, inverse = reconstruction["moments"], reconstruction["inverse"]
        identity = [[Fraction(i == j) for j in range(3)] for i in range(3)]
        for row, name in zip(matrix, ("Q", "I1", "I2"), strict=True):
            rectangle = self.protocol["regions"][name]
            area = Fraction(*rectangle[1]) * Fraction(*rectangle[3])
            self.assertEqual(row, [area, area**2 / 4, area**3 / 9])
        self.assertNotEqual(permutation_determinant(matrix), 0)
        self.assertEqual(reconstruction["determinant"], permutation_determinant(matrix))
        self.assertEqual(multiply(matrix, inverse), identity)
        self.assertEqual(multiply(inverse, matrix), identity)
        self.assertIs(reconstruction["left_identity"], True)
        self.assertIs(reconstruction["right_identity"], True)
        for row in self.report["data"]:
            self.assertEqual(
                [dot(moment, row["moment_solution"]) for moment in matrix], [Fraction(1), *row["q"]]
            )

    def test_same_point_joint_law_structural_zero_and_complete_old_marginal(self):
        expected_words = [
            [list(symbol) for symbol in word] for word in itertools.product(SYMBOLS, repeat=4)
        ]
        for world in self.report["worlds"]:
            self.assertEqual([row["y"] for row in world["records"]], expected_words)
            self.assertEqual(sum(row["p"] for row in world["records"]), 1)
            self.assertEqual(sum(row["p"] > 0 for row in world["records"]), 81)
            self.assertEqual(sum(row["p"] == 0 for row in world["records"]), 175)
            self.assertEqual(world["one_point"][2], Fraction(0))
            self.assertGreater(world["independent_10"], 0)
            self.assertEqual(world["independent_10"], world["q"][0] * (1 - world["q"][1]))
            for row in world["records"]:
                self.assertEqual(row["p"] == 0, [1, 0] in row["y"])
            exact_tree(self, world["marginal"], first_law(world["q"][0], 4))
            self.assertIs(world["marginal_equal"], True)
            for marginal in world["marginal"]:
                self.assertEqual(
                    marginal["p"],
                    sum(
                        (
                            row["p"]
                            for row in world["records"]
                            if [pair[0] for pair in row["y"]] == marginal["y"]
                        ),
                        Fraction(0),
                    ),
                )

    def test_point_reconstruction_does_not_erase_factorization_or_scale_ambiguity(self):
        by_world = {row["id"]: row for row in self.report["worlds"]}
        self.assertEqual(self.report["classes"]["joint"], self.report["classes"]["point"])
        inherited, added = self.report["collisions"]
        for field in ("first_equal", "joint_equal", "point_equal"):
            self.assertIs(inherited[field], True)
        self.assertEqual(inherited["q2_gap"], Fraction(0))
        self.assertIs(added["first_equal"], True)
        self.assertIs(added["joint_equal"], False)
        self.assertIs(added["point_equal"], False)
        self.assertNotEqual(added["q2_gap"], 0)
        for row in self.report["collisions"]:
            self.assertEqual(row["target_gap"], Fraction(3, 80))
        for row in self.report["scale_pairs"]:
            first, second = [by_world[name] for name in row["worlds"]]
            self.assertEqual(second["volumes"], [4 * value for value in first["volumes"]])
            self.assertEqual(second["mass"], [4 * value for value in first["mass"]])
            self.assertEqual(row["volume_factor"], Fraction(4))
            for field in ("target_equal", "point_equal", "joint_equal"):
                self.assertIs(row[field], True)
        for row in self.report["worlds"]:
            self.assertIs(row["reconstruction_equal"], True)
            self.assertEqual(row["recovered"], row["normalized_coefficients"])

    def test_zero_constant_poles_and_closed_bound_diagnostics(self):
        data = {row["id"]: row for row in self.report["data"]}
        self.assertEqual(
            data["zero_constant"]["moment_solution"], [Fraction(0), Fraction(4), Fraction(0)]
        )
        for case in self.report["cases"]:
            bound = next(
                row for row in self.protocol["density_bounds"] if row["id"] == case["bound"]
            )
            lower, upper = [Fraction(*pair) for pair in bound["interval"]]
            for row in case["hypotheses"]:
                if row["inverse_denominator"] == 0:
                    self.assertNotEqual(row["inverse_numerator"], 0)
                    self.assertEqual(row["candidate"], [])
                    self.assertEqual(row["second_residual"], [])
                else:
                    self.assertEqual(
                        row["candidate"][0] * row["inverse_denominator"], row["inverse_numerator"]
                    )
                    in_bound = lower <= row["candidate"][0] <= upper
                    self.assertEqual(bool(row["second_residual"]), in_bound)
                self.assertEqual(bool(row["delta_set"]), row["second_residual"] == [Fraction(0)])
                if row["delta_set"]:
                    self.assertEqual(row["candidate"], row["delta_set"])
            if case["data"] in ("zero", "one", "equal", "zero_constant"):
                self.assertEqual(case["status"], "infeasible")
                self.assertEqual(case["worlds"], [])
            if case["data"] in ("flat_2", "conformal_2"):
                owner = "flat" if case["data"] == "flat_2" else "conformal"
                row = next(row for row in case["hypotheses"] if row["id"] == owner)
                self.assertEqual(row["candidate"], [Fraction(2)])
                self.assertEqual(row["delta_set"], [Fraction(2)] if case["bound"] == "two" else [])

    def test_bound_monotonicity_and_support_do_not_promote_finite_frequencies(self):
        for row in self.report["monotonicity"]:
            for field in ("world_subset", "target_subset", "nuisance_preserved"):
                self.assertIs(row[field], True)
        geometry_ids = [row["id"] for row in self.protocol["geometries"]]
        self.assertEqual(sum(row["possible"] for row in self.report["support"]), 81)
        for row in self.report["support"]:
            possible = [1, 0] not in row["y"]
            self.assertIs(row["possible"], possible)
            self.assertEqual(row["worlds"], geometry_ids if possible else [])
            self.assertEqual(row["targets"], [Fraction(17, 80), Fraction(1, 4)] if possible else [])
        # Both all-00 and all-11 packets are possible, while their exact population
        # frequency pairs are outside the geometric model. This is support only.
        self.assertTrue(self.report["support"][0]["possible"])
        self.assertTrue(self.report["support"][-1]["possible"])
        for datum in ("zero", "one"):
            self.assertTrue(
                all(
                    case["status"] == "infeasible"
                    for case in self.report["cases"]
                    if case["data"] == datum
                )
            )


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_all_fixture_queries_and_detached_replies(self):
        _study, _protocol, report = evaluated()
        for case in report["cases"]:
            supplied = query(case["q"], case["bound"])
            saved = copy.deepcopy(supplied)
            wanted = query_answer(case)
            returned = self.study.identify(supplied)
            exact_tree(self, returned, wanted)
            self.assertEqual(supplied, saved)
            returned["worlds"].append("corrupted")
            returned["targets"].append(Fraction(99))
            if returned["nuisance"]:
                returned["nuisance"][0]["delta"] = Fraction(99)
            exact_tree(self, self.study.identify(supplied), wanted)
            supplied["q"][0][0] += 1
            self.assertEqual(saved, query(case["q"], case["bound"]))

    def test_nonfixture_continuous_candidates_and_legal_model_empty_pairs(self):
        _study, protocol, report = evaluated()
        moments = moment_matrix(protocol)
        fixed_pairs = [row["q"] for row in report["data"]]
        for eta in (0, 1):
            delta = Fraction(1, 3)
            masses = forward_mass(moments, eta, 1, delta)
            pair = [masses[1] / masses[0], masses[2] / masses[0]]
            self.assertNotIn(pair, fixed_pairs)
            names = ["flat", "flat_x4"] if eta == 0 else ["conformal", "conformal_x4"]
            wanted = {
                "worlds": names,
                "targets": [Fraction(16 + eta, 16 * (4 + eta))],
                "status": "identified",
                "nuisance": [{"id": name, "delta": delta} for name in names],
            }
            exact_tree(self, self.study.identify(query(pair, "half")), wanted)
        for pair in ([Fraction(0), Fraction(1)], [Fraction(1, 2), Fraction(1, 2)]):
            exact_tree(
                self,
                self.study.identify(query(pair)),
                {"worlds": [], "targets": [], "status": "infeasible", "nuisance": []},
            )

    def test_strict_query_schema_nested_pairs_native_types_and_bounds(self):
        class DictChild(dict):
            pass

        class ListChild(list):
            pass

        class IntChild(int):
            pass

        class StringChild(str):
            pass

        base = query([Fraction(1, 4), Fraction(3, 8)])
        invalid = [
            None,
            [],
            DictChild(base),
            {StringChild(key): value for key, value in base.items()},
        ]
        for key in base:
            changed = copy.deepcopy(base)
            del changed[key]
            invalid.append(changed)
        for key, value in (
            ("schema", "qr05bn-query-v1"),
            ("data_kind", "sample_frequency"),
            ("density_bound", "three"),
            ("bound_basis", "observed"),
            ("schema", StringChild(base["schema"])),
            ("data_kind", StringChild(base["data_kind"])),
            ("density_bound", StringChild("two")),
            ("bound_basis", True),
        ):
            changed = copy.deepcopy(base)
            changed[key] = value
            invalid.append(changed)
        bad_pairs = [
            Fraction(1, 4),
            [],
            [[1, 4]],
            [[1, 4], [3, 8], [0, 1]],
            ([1, 4], [3, 8]),
            ListChild([[1, 4], [3, 8]]),
            [[1, 4], (3, 8)],
            [[1, 4], ListChild([3, 8])],
            [[2, 8], [3, 8]],
            [[0, 2], [3, 8]],
            [[1, -4], [3, 8]],
            [[1, 0], [3, 8]],
            [[True, 4], [3, 8]],
            [[1, 4], [3, True]],
            [[IntChild(1), 4], [3, 8]],
            [[1, 4], [3.0, 8]],
            [[1, 4], ["3", 8]],
            [[1, 2], [1, 4]],
            [[-1, 4], [3, 8]],
            [[1, 4], [9, 8]],
            [[1, 4], [2**31, 2**31 + 1]],
        ]
        for value in bad_pairs:
            changed = copy.deepcopy(base)
            changed["q"] = value
            invalid.append(changed)
        for name in (
            "records",
            "count",
            "quota",
            "frequency",
            "actual_world",
            "eta",
            "delta",
            "state",
            "coordinates",
            "extra",
        ):
            invalid.append({**copy.deepcopy(base), name: 0})
        for index, supplied in enumerate(invalid):
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.study.identify(supplied)

    def test_query_is_file_engine_and_old_wrapper_blind(self):
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
            mock.patch.object(
                self.study.UTILITY, "estimate", side_effect=AssertionError("old estimate")
            ),
        ):
            exact_tree(
                self,
                self.study.identify(query([Fraction(0), Fraction(0)])),
                {"worlds": [], "targets": [], "status": "infeasible", "nuisance": []},
            )
            result = self.study.identify(query([Fraction(1, 4), Fraction(3, 8)], "uniform"))
            self.assertEqual(result["worlds"], ["flat", "flat_x4"])


def fixture_snapshot(study):
    snapshot = {name: ("synthetic:" + name).encode() for name in study.SOURCE_PATHS}
    snapshot["protocol.json"] = (HERE / "protocol.json").read_bytes()
    snapshot[study.UTILITY_SOURCE] = study.UTILITY_BYTES
    return snapshot


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_entire_pair_cap_precedes_arithmetic_and_exact_cap_is_accepted(self):
        for pairs in (
            [[0, 1], [2**1000, 2**1000 + 1]],
            [[2**1000, 2**1000 + 1], [1, 1]],
            [[0, 1], [-(2**31), 1]],
        ):
            supplied = query([Fraction(0), Fraction(1)])
            supplied["q"] = pairs
            with (
                self.subTest(pairs=pairs),
                mock.patch.object(self.study.math, "gcd", side_effect=AssertionError("early gcd")),
                self.assertRaises(ValueError),
            ):
                self.study.identify(supplied)
        exact_tree(
            self,
            self.study.identify(query([Fraction(0), Fraction(1, 2147483647)])),
            {"worlds": [], "targets": [], "status": "infeasible", "nuisance": []},
        )

    def test_authenticated_fresh_utility_aliases_nine_sources_and_owned_defaults(self):
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
        self.assertEqual(len(snapshot), 9)
        self.assertEqual(set(snapshot), set(study.SOURCE_PATHS))
        self.assertEqual(snapshot[study.UTILITY_SOURCE], study.UTILITY_BYTES)
        self.assertNotIn("results.json", snapshot)
        with tempfile.TemporaryDirectory(prefix="qr05bo-utility-") as directory:
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
        with tempfile.TemporaryDirectory(prefix="qr05bo-read-") as directory:
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
            (("reconstruction", "inverse", 2, 2), Fraction(0)),
            (("worlds", -1, "records", -1, "p"), False),
            (("worlds", 0, "one_point", 2), 0),
            (("data", -1, "moment_solution", 0), 0),
            (("cases", -1, "hypotheses", -1, "status"), "feasible"),
            (("support", -1, "possible"), 1),
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
        self.directory = tempfile.TemporaryDirectory(prefix="qr05bo-evidence-")
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
        self.assertEqual(freeze["schema"], "qr05bo-source-freeze-v1")
        self.assertEqual(capture["schema"], "qr05bo-capture-v1")
        self.assertEqual(len(freeze["sources"]), 9)
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
        raise KeyboardInterrupt("QR-05BO 120-second suite deadline")

    signal.signal(signal.SIGALRM, suite_expired)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
