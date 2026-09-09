"""Source-bound BD contract tests, using only the standard library.

Import performs no fixture mathematics or engine execution. All tests wait
for the first source-bound release. Checks remain active under Python -O.
The degree-five geometry oracle is new; only owned BC test mechanics are
adapted. No preceding numerical executor is imported.
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
PROTOCOL_SHA256 = "68a49ef25e379663a04fa7742d06b28fe3490d12d431ed4f3adc2fddcb907d73"


def load_module(name):
    spec = importlib.util.spec_from_file_location("qr05bd_test_" + name, HERE / (name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("BD source could not be loaded")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def rational(value):
    if type(value) is not str:
        raise ValueError("The evidence quantity must be a canonical rational string")
    result = Fraction(value)
    if str(result) != value:
        raise ValueError("Noncanonical rational string")
    return result


@lru_cache(maxsize=1)
def boole_rule():
    """Validate the independent one-variable exactness certificate before use."""
    nodes = tuple(Fraction(i, 4) for i in range(5))
    weights = tuple(Fraction(value, 90) for value in (7, 32, 12, 32, 7))
    for power in range(6):
        moment = sum(weight * node**power for node, weight in zip(nodes, weights, strict=True))
        if moment != Fraction(1, power + 1):
            raise ValueError("Invalid degree-five quadrature certificate")
    return nodes, weights


def integrate_unit(function):
    nodes, weights = boole_rule()
    return sum(
        weights[i] * weights[j] * function(u, v)
        for i, u in enumerate(nodes)
        for j, v in enumerate(nodes)
    )


def basis(station, u, v):
    return (u if station[0] == "1" else 1 - u) * (v if station[1] == "1" else 1 - v)


def bubble(u, v):
    return u * (1 - u) * v * (1 - v)


def profile_value(corners, theta, u, v):
    return sum(
        corners[index] * basis(station, u, v)
        for index, station in enumerate(("00", "10", "01", "11"))
    ) + theta * bubble(u, v)


def functional(function):
    # For the frozen unit chart, V²/σ and the two measure factors cancel.
    return integrate_unit(lambda u, v: function(u, v) * (1 - u) * (1 - v))


@lru_cache(maxsize=1)
def compiled_weights():
    corners = [
        functional(lambda u, v, station=station: basis(station, u, v))
        for station in ("00", "10", "01", "11")
    ]
    center = Fraction(1, 2)
    at_center = bubble(center, center)
    center_basis = [basis(station, center, center) for station in ("00", "10", "01", "11")]
    bubble_target = functional(bubble)
    repair = [
        weight - bubble_target * coefficient / at_center
        for weight, coefficient in zip(corners, center_basis, strict=True)
    ]
    repair.append(bubble_target / at_center)
    return corners, repair


def probability(means, outcomes):
    result = Fraction(1)
    for mean, outcome in zip(means, outcomes, strict=True):
        result *= (1 + mean * outcome) / 2
    return result


def event_weights(plan, corner, repair):
    stations = (
        ("00", "10", "01", "11", "cc") if plan["id"] == "repair5" else ("00", "10", "01", "11")
    )
    weights = dict(zip(stations, repair if plan["id"] == "repair5" else corner, strict=True))
    return [
        weights[station] / sum(other == station for other, _shot in plan["slots"])
        for station, _shot in plan["slots"]
    ]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right, strict=True))


def product(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def read_protocol():
    return json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def evaluated():
    """One full new-engine comparison per test process, after root release."""
    study = load_module("study")
    return study, study.load_protocol(), study.compare_routes()


def exact_keys(test, value, keys):
    test.assertIs(type(value), dict)
    test.assertEqual(set(value), set(keys.split()))


class ProtocolTests(unittest.TestCase):
    def test_frozen_protocol_identity_and_declared_domain(self):
        self.assertEqual(
            hashlib.sha256((HERE / "protocol.json").read_bytes()).hexdigest(), PROTOCOL_SHA256
        )
        protocol = read_protocol()
        self.assertEqual(protocol["study"], "QR-05BD")
        self.assertEqual(protocol["stations"], ["00", "10", "01", "11", "cc"])
        self.assertEqual(protocol["outcomes"], [-1, 1])
        self.assertEqual(len(protocol["profiles"]), 10)
        self.assertEqual(
            [plan["id"] for plan in protocol["plans"]], ["corner4", "repair5", "corner5"]
        )
        self.assertEqual([len(plan["slots"]) for plan in protocol["plans"]], [4, 5, 5])
        self.assertEqual(len(protocol["record_keys"]), 15)
        self.assertEqual(protocol["observer_orders"], ["forward", "reverse"])
        self.assertEqual(len(protocol["global_controls"]), 2)

    def test_boole_moment_certificate_precedes_all_geometry(self):
        nodes, weights = boole_rule()
        protocol = read_protocol()["third_oracle"]
        self.assertEqual(nodes, tuple(map(Fraction, protocol["nodes"])))
        self.assertEqual(weights, tuple(map(Fraction, protocol["weights"])))
        self.assertEqual(protocol["verify_moments_through"], 5)
        for power in range(6):
            self.assertEqual(
                sum(w * x**power for x, w in zip(nodes, weights, strict=True)),
                Fraction(1, power + 1),
            )
        for u_power, v_power in itertools.product(range(6), repeat=2):
            self.assertEqual(
                integrate_unit(lambda u, v, a=u_power, b=v_power: u**a * v**b),
                Fraction(1, (u_power + 1) * (v_power + 1)),
            )


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.corner, cls.repair = compiled_weights()
        cls.coordinates = [tuple(map(Fraction, point)) for point in cls.protocol["coordinates"]]

    def test_complete_report_and_geometry_inverse_certificate(self):
        exact_keys(
            self,
            self.report,
            "geometry operators schedule_counts plans profiles off_model global_controls",
        )
        geometry = self.report["geometry"]
        exact_keys(
            self,
            geometry,
            "volume sigma corner_weights bubble_target bubble_at_center center_basis evaluation_matrix coefficient_decoder repair_weights weight_sum",
        )
        volume = Fraction(self.protocol["geometry"]["measure_factor"])
        self.assertEqual(geometry["volume"], volume)
        self.assertEqual(geometry["sigma"], volume**4)
        self.assertEqual(geometry["corner_weights"], self.corner)
        self.assertEqual(geometry["repair_weights"], self.repair)
        self.assertEqual(geometry["bubble_target"], functional(bubble))
        center = self.coordinates[-1]
        self.assertEqual(geometry["bubble_at_center"], bubble(*center))
        self.assertEqual(
            geometry["center_basis"],
            [basis(station, *center) for station in self.protocol["stations"][:4]],
        )
        matrix = [
            [basis(station, u, v) for station in self.protocol["stations"][:4]] + [bubble(u, v)]
            for u, v in self.coordinates
        ]
        self.assertEqual(geometry["evaluation_matrix"], matrix)
        decoder = geometry["coefficient_decoder"]
        self.assertEqual(len(decoder), 5)
        self.assertTrue(all(len(row) == 5 for row in decoder))
        identity = [[Fraction(i == j) for j in range(5)] for i in range(5)]
        self.assertEqual(product(decoder, matrix), identity)
        self.assertEqual(product(matrix, decoder), identity)
        targets = self.corner + [functional(bubble)]
        self.assertEqual(
            [sum(targets[j] * decoder[j][i] for j in range(5)) for i in range(5)], self.repair
        )
        self.assertEqual(geometry["weight_sum"], sum(self.repair))
        self.assertEqual(sum(self.repair), sum(self.corner))

    def test_all_operator_entries_and_factor_schedule_domains(self):
        exact_keys(self, self.report["operators"], "corner4 five_factor")
        exact_keys(self, self.report["schedule_counts"], "corner4 five_factor")
        for name, dimensions in (("corner4", 4), ("five_factor", 5)):
            items = self.report["operators"][name]
            self.assertEqual(len(items), 2**dimensions)
            schedules = list(itertools.permutations(range(dimensions)))
            self.assertEqual(self.report["schedule_counts"][name], len(schedules))
            for item, outcomes in zip(
                items, itertools.product((-1, 1), repeat=dimensions), strict=True
            ):
                exact_keys(self, item, "outcomes kraus_diagonal")
                self.assertEqual(item["outcomes"], list(outcomes))
                diagonal = [
                    Fraction(
                        all(
                            outcome == 1 - 2 * bit
                            for outcome, bit in zip(outcomes, bits, strict=True)
                        )
                    )
                    for bits in itertools.product((0, 1), repeat=dimensions)
                ]
                self.assertEqual(item["kraus_diagonal"], diagonal)
                self.assertEqual(sum(diagonal), 1)
                # The support criterion remains exactly the same under every
                # event-factor permutation; event labels are never discarded.
                for order in schedules:
                    self.assertEqual(
                        [
                            Fraction(all(outcomes[i] == 1 - 2 * bits[i] for i in order))
                            for bits in itertools.product((0, 1), repeat=dimensions)
                        ],
                        diagonal,
                    )
            self.assertEqual(
                [sum(item["kraus_diagonal"][i] for item in items) for i in range(2**dimensions)],
                [Fraction(1)] * (2**dimensions),
            )

    def test_compiled_plans_and_matched_cost(self):
        self.assertEqual(len(self.report["plans"]), 3)
        for actual, fixture in zip(self.report["plans"], self.protocol["plans"], strict=True):
            exact_keys(self, actual, "id slots cost event_weights")
            self.assertEqual(actual["id"], fixture["id"])
            self.assertEqual(actual["slots"], fixture["slots"])
            self.assertEqual(actual["cost"], fixture["cost"])
            self.assertEqual(actual["cost"], len(actual["slots"]))
            self.assertEqual(
                actual["event_weights"], event_weights(fixture, self.corner, self.repair)
            )
        self.assertEqual(self.report["plans"][1]["cost"], self.report["plans"][2]["cost"])
        self.assertEqual(self.report["plans"][2]["event_weights"][:2], [self.corner[0] / 2] * 2)

    def test_all_profiles_coefficients_targets_admission_and_complete_plan_laws(self):
        self.assertEqual(len(self.report["profiles"]), 10)
        for actual, fixture in zip(self.report["profiles"], self.protocol["profiles"], strict=True):
            with self.subTest(profile=fixture["id"]):
                exact_keys(
                    self,
                    actual,
                    "id corners theta admission_bound sample_means recovered_coefficients target corner_target plans repair_decomposition mse_differences",
                )
                corners = list(map(Fraction, fixture["corners"]))
                theta = Fraction(fixture["theta"])
                means = [profile_value(corners, theta, *point) for point in self.coordinates]
                target = functional(lambda u, v, c=corners, t=theta: profile_value(c, t, u, v))
                self.assertEqual(actual["id"], fixture["id"])
                self.assertEqual(actual["corners"], corners)
                self.assertEqual(actual["theta"], theta)
                self.assertEqual(
                    actual["admission_bound"], max(map(abs, corners)) + abs(theta) / 16
                )
                self.assertLessEqual(actual["admission_bound"], 1)
                self.assertTrue(all(-1 <= value <= 1 for value in means))
                self.assertEqual(actual["sample_means"], means)
                self.assertEqual(actual["recovered_coefficients"], corners + [theta])
                self.assertEqual(
                    [dot(row, means) for row in self.report["geometry"]["coefficient_decoder"]],
                    corners + [theta],
                )
                self.assertEqual(actual["target"], target)
                self.assertEqual(
                    actual["corner_target"],
                    functional(lambda u, v, c=corners: profile_value(c, Fraction(0), u, v)),
                )
                exact_keys(self, actual["plans"], "corner4 repair5 corner5")
                by_station = dict(zip(self.protocol["stations"], means, strict=True))
                for plan in self.protocol["plans"]:
                    result = actual["plans"][plan["id"]]
                    exact_keys(self, result, "rows mean bias variance mse")
                    n = len(plan["slots"])
                    self.assertEqual(len(result["rows"]), 2**n)
                    event_means = [by_station[station] for station, _shot in plan["slots"]]
                    coefficients = event_weights(plan, self.corner, self.repair)
                    operators = self.report["operators"]["corner4" if n == 4 else "five_factor"]
                    total = first = second = Fraction(0)
                    marginal_density = [Fraction(0)] * (2**n)
                    for row, outcomes, operator in zip(
                        result["rows"], itertools.product((-1, 1), repeat=n), operators, strict=True
                    ):
                        exact_keys(self, row, "outcomes probability state_diagonal estimate")
                        mass = probability(event_means, outcomes)
                        estimate = dot(coefficients, outcomes)
                        self.assertEqual(row["outcomes"], list(outcomes))
                        self.assertEqual(row["probability"], mass)
                        self.assertEqual(row["estimate"], estimate)
                        self.assertEqual(
                            row["state_diagonal"],
                            [mass * entry for entry in operator["kraus_diagonal"]],
                        )
                        self.assertEqual(sum(row["state_diagonal"]), mass)
                        total += mass
                        first += mass * estimate
                        second += mass * estimate**2
                        for i, entry in enumerate(row["state_diagonal"]):
                            marginal_density[i] += entry
                    self.assertEqual(total, 1)
                    self.assertEqual(
                        marginal_density,
                        [
                            probability(event_means, tuple(1 - 2 * bit for bit in bits))
                            for bits in itertools.product((0, 1), repeat=n)
                        ],
                    )
                    variance = second - first**2
                    self.assertEqual(
                        variance,
                        sum(
                            weight**2 * (1 - mean**2)
                            for weight, mean in zip(coefficients, event_means, strict=True)
                        ),
                    )
                    self.assertEqual(result["mean"], first)
                    self.assertEqual(result["bias"], first - target)
                    self.assertEqual(result["variance"], variance)
                    self.assertEqual(result["mse"], variance + (first - target) ** 2)
                    if plan["id"] == "repair5":
                        self.assertEqual(first, target)
                    else:
                        self.assertEqual(result["bias"], -theta * functional(bubble))

    def test_repair_covariance_and_false_independence_sum(self):
        discrepancies = 0
        center_basis = self.report["geometry"]["center_basis"]
        b_center = bubble(*self.coordinates[-1])
        b_target = functional(bubble)
        for profile in self.report["profiles"]:
            decomposition = profile["repair_decomposition"]
            exact_keys(
                self,
                decomposition,
                "base_variance theta_variance base_theta_covariance independence_shortcut_variance covariance_corrected_variance",
            )
            rows = profile["plans"]["repair5"]["rows"]
            base_mean = theta_mean = base_second = theta_second = cross = Fraction(0)
            for row in rows:
                base = dot(self.corner, row["outcomes"][:4])
                theta = (row["outcomes"][4] - dot(center_basis, row["outcomes"][:4])) / b_center
                mass = row["probability"]
                self.assertEqual(base + b_target * theta, row["estimate"])
                base_mean += mass * base
                theta_mean += mass * theta
                base_second += mass * base**2
                theta_second += mass * theta**2
                cross += mass * base * theta
            base_variance = base_second - base_mean**2
            theta_variance = theta_second - theta_mean**2
            covariance = cross - base_mean * theta_mean
            shortcut = base_variance + b_target**2 * theta_variance
            corrected = shortcut + 2 * b_target * covariance
            self.assertEqual(
                decomposition,
                {
                    "base_variance": base_variance,
                    "theta_variance": theta_variance,
                    "base_theta_covariance": covariance,
                    "independence_shortcut_variance": shortcut,
                    "covariance_corrected_variance": corrected,
                },
            )
            self.assertEqual(corrected, profile["plans"]["repair5"]["variance"])
            discrepancies += shortcut != corrected
        self.assertGreater(discrepancies, 0)

    def test_signed_mse_differences_and_no_single_shot_exactness(self):
        for profile in self.report["profiles"]:
            exact_keys(
                self, profile["mse_differences"], "repair_minus_corner4 repair_minus_corner5"
            )
            for old in ("corner4", "corner5"):
                self.assertEqual(
                    profile["mse_differences"]["repair_minus_" + old],
                    profile["plans"]["repair5"]["mse"] - profile["plans"][old]["mse"],
                )
        zero = next(profile for profile in self.report["profiles"] if profile["id"] == "zero")
        self.assertGreater(zero["plans"]["repair5"]["variance"], 0)
        self.assertTrue(
            any(
                row["probability"] > 0 and row["estimate"] != zero["target"]
                for row in zero["plans"]["repair5"]["rows"]
            )
        )

    def test_center_access_resolves_old_bubble_but_off_model_law_still_collides(self):
        by_id = {profile["id"]: profile for profile in self.report["profiles"]}
        zero, original_bubble = by_id["zero"], by_id["bubble"]
        self.assertEqual(
            [row["probability"] for row in zero["plans"]["corner4"]["rows"]],
            [row["probability"] for row in original_bubble["plans"]["corner4"]["rows"]],
        )
        self.assertNotEqual(
            [row["probability"] for row in zero["plans"]["repair5"]["rows"]],
            [row["probability"] for row in original_bubble["plans"]["repair5"]["rows"]],
        )
        off = self.report["off_model"]
        exact_keys(
            self,
            off,
            "sample_means global_bound target probabilities state_diagonals estimator_mean estimator_bias estimator_variance mse",
        )
        amplitude = Fraction(self.protocol["off_model"]["amplitude"])

        def h(u, v):
            return (
                amplitude * bubble(u, v) * ((u - Fraction(1, 2)) ** 2 + (v - Fraction(1, 2)) ** 2)
            )

        self.assertEqual(off["sample_means"], [h(*point) for point in self.coordinates])
        self.assertEqual(off["sample_means"], zero["sample_means"])
        self.assertEqual(off["global_bound"], Fraction(self.protocol["off_model"]["global_bound"]))
        self.assertEqual(
            off["probabilities"], [row["probability"] for row in zero["plans"]["repair5"]["rows"]]
        )
        self.assertEqual(
            off["state_diagonals"],
            [row["state_diagonal"] for row in zero["plans"]["repair5"]["rows"]],
        )
        self.assertEqual(off["target"], functional(h))
        self.assertGreater(off["target"], zero["target"])
        self.assertEqual(off["estimator_mean"], zero["plans"]["repair5"]["mean"])
        self.assertEqual(off["estimator_bias"], off["estimator_mean"] - off["target"])
        self.assertEqual(off["estimator_variance"], zero["plans"]["repair5"]["variance"])
        self.assertEqual(off["mse"], off["estimator_variance"] + off["estimator_bias"] ** 2)

    def test_global_invalidity_is_not_the_same_as_failed_sufficient_admission(self):
        self.assertEqual(len(self.report["global_controls"]), 2)
        for actual, fixture in zip(
            self.report["global_controls"], self.protocol["global_controls"], strict=True
        ):
            exact_keys(
                self,
                actual,
                "id admission_bound admission sample_means witness witness_value witness_min_eigenvalue global_interval classification",
            )
            corners = list(map(Fraction, fixture["corners"]))
            theta = Fraction(fixture["theta"])
            witness = list(map(Fraction, fixture["witness"]))
            value = profile_value(corners, theta, *witness)
            self.assertEqual(actual["id"], fixture["id"])
            self.assertEqual(actual["classification"], fixture["classification"])
            self.assertEqual(actual["admission"], "outside_sufficient_domain")
            self.assertEqual(actual["admission_bound"], max(map(abs, corners)) + abs(theta) / 16)
            self.assertGreater(actual["admission_bound"], 1)
            self.assertEqual(
                actual["sample_means"],
                [profile_value(corners, theta, *point) for point in self.coordinates],
            )
            self.assertTrue(all(-1 <= mean <= 1 for mean in actual["sample_means"]))
            self.assertEqual(actual["witness"], witness)
            self.assertEqual(actual["witness_value"], value)
            self.assertEqual(actual["witness_min_eigenvalue"], (1 - abs(value)) / 2)
            self.assertEqual(
                actual["global_interval"],
                [min(corners) + min(theta, 0) / 16, max(corners) + max(theta, 0) / 16],
            )
            if fixture["id"] == "overshoot":
                self.assertLess(actual["witness_min_eigenvalue"], 0)
            else:
                self.assertGreaterEqual(actual["global_interval"][0], 0)
                self.assertLessEqual(actual["global_interval"][1], 1)
                self.assertGreaterEqual(actual["witness_min_eigenvalue"], 0)
        admitted_ids = {profile["id"] for profile in self.report["profiles"]}
        self.assertTrue(
            all(control["id"] not in admitted_ids for control in self.report["global_controls"])
        )

    def test_strict_quantity_and_event_metadata_types(self):
        wire = self.study.encode(self.report)

        def visit(raw, encoded, path=()):
            if type(raw) is dict:
                self.assertIs(type(encoded), dict)
                self.assertEqual(set(raw), set(encoded))
                for key in raw:
                    visit(raw[key], encoded[key], (*path, key))
            elif type(raw) is list:
                self.assertIs(type(encoded), list)
                self.assertEqual(len(raw), len(encoded))
                for index, (left, right) in enumerate(zip(raw, encoded, strict=True)):
                    visit(left, right, (*path, index))
            elif path[-1] in ("id", "admission", "classification") or (
                "slots" in path and path[-1] == 0
            ):
                self.assertIs(type(raw), str, path)
                self.assertIs(type(encoded), str)
                self.assertEqual(raw, encoded)
            elif (
                path[0] == "schedule_counts"
                or path[-1] == "cost"
                or "outcomes" in path
                or ("slots" in path and path[-1] == 1)
            ):
                self.assertIs(type(raw), int, path)
                self.assertIs(type(encoded), int)
                self.assertEqual(raw, encoded)
            else:
                self.assertIs(type(raw), Fraction, path)
                self.assertIs(type(encoded), str)
                self.assertEqual(rational(encoded), raw)

        visit(self.report, wire)


def malformed_records(base, protocol):
    yield "missing slot", copy.deepcopy(base[:-1])
    yield "extra slot", copy.deepcopy(base + [base[0]])
    yield "tuple records", tuple(copy.deepcopy(base))
    yield "no records", None
    changed = copy.deepcopy(base)
    changed[-1] = copy.deepcopy(changed[0])
    yield "duplicate slot", changed
    for key in protocol["record_keys"]:
        changed = copy.deepcopy(base)
        del changed[-1][key]
        yield "missing " + key, changed
    for key in (
        "profile",
        "profile_id",
        "f",
        "theta",
        "rho",
        "state",
        "likelihood",
        "probability",
        "target",
        "seed",
        "weights",
    ):
        changed = copy.deepcopy(base)
        changed[-1][key] = "private"
        yield "private " + key, changed
    values = {
        "outcome": [True, False, 0, 2, -2, 1.0, "1", Fraction(1), None],
        "shot_id": [True, 0, 2, 3, "1", Fraction(1)],
        "station_id": ["unknown", 0, None],
        "attempted": [False, 1, "true", None],
        "available": [False, 1, "true", None],
        "status": ["nondetection", "postselected", "missing", True],
        "raw_registration_ref": ["packet:00:1", "private-profile", "", None],
        "acquisition_plan_id": ["unknown", "", None, 0],
    }
    for key, options in values.items():
        for index, value in enumerate(options):
            changed = copy.deepcopy(base)
            changed[-1][key] = value
            yield key + " invalid " + str(index), changed
    for key in protocol["public_context"]:
        for value in ("mismatched", None):
            changed = copy.deepcopy(base)
            changed[-1][key] = value
            yield "context " + key + " " + repr(value), changed


class ObserverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        corner, repair = compiled_weights()
        cls.weights = {
            plan: dict(
                zip(
                    cls.protocol["stations"] if plan == "repair5" else cls.protocol["stations"][:4],
                    repair if plan == "repair5" else corner,
                    strict=True,
                )
            )
            for plan in ("corner4", "repair5", "corner5")
        }

    def test_public_slot_construction_and_context(self):
        self.assertEqual(
            {key: [list(slot) for slot in value] for key, value in self.study.PLAN_SLOTS.items()},
            {plan["id"]: plan["slots"] for plan in self.protocol["plans"]},
        )
        for plan in self.protocol["plans"]:
            outcomes = [-1] * len(plan["slots"])
            records = self.study.make_records(outcomes, plan["id"])
            self.assertEqual(len(records), len(plan["slots"]))
            for record, (station, shot) in zip(records, plan["slots"], strict=True):
                self.assertEqual(set(record), set(self.protocol["record_keys"]))
                self.assertEqual(record["station_id"], station)
                self.assertIs(type(record["shot_id"]), int)
                self.assertEqual(record["shot_id"], shot)
                self.assertEqual(record["acquisition_plan_id"], plan["id"])
                self.assertEqual(record["raw_registration_ref"], f"packet:{station}:{shot}")
                self.assertIs(record["attempted"], True)
                self.assertIs(record["available"], True)
                self.assertEqual(record["outcome"], -1)
                self.assertEqual(record["status"], "registered")
                for key, value in self.protocol["public_context"].items():
                    self.assertEqual(record[key], value)

    def test_every_plan_branch_forward_reverse_and_ownership(self):
        for profile in self.report["profiles"]:
            for plan in self.protocol["plans"]:
                plan_id = plan["id"]
                weights = self.weights[plan_id]
                for row in profile["plans"][plan_id]["rows"]:
                    records = self.study.make_records(row["outcomes"], plan_id)
                    snapshot = copy.deepcopy(records)
                    weight_snapshot = copy.deepcopy(weights)
                    coefficients = event_weights(plan, *compiled_weights())
                    expected = dot(coefficients, row["outcomes"])
                    self.assertEqual(self.study.estimate(records, weights, plan_id), expected)
                    self.assertEqual(
                        self.study.estimate(list(reversed(records)), weights, plan_id), expected
                    )
                    self.assertEqual(expected, row["estimate"])
                    self.assertEqual(records, snapshot)
                    self.assertEqual(weights, weight_snapshot)
        first = self.study.make_records([-1] * 5)
        second = self.study.make_records([-1] * 5)
        self.assertIsNot(first, second)
        for left, right in zip(first, second, strict=True):
            self.assertIsNot(left, right)

    def test_multishot_mean_and_distinct_fresh_slot_identity(self):
        records = self.study.make_records([-1, 1, -1, -1, -1], "corner5")
        weights = {
            station: Fraction(index + 1)
            for index, station in enumerate(self.protocol["stations"][:4])
        }
        self.assertEqual(
            self.study.estimate(records, weights, "corner5"),
            -sum(value for station, value in weights.items() if station != "00"),
        )
        self.assertEqual(records[0]["station_id"], records[1]["station_id"])
        self.assertNotEqual(records[0]["shot_id"], records[1]["shot_id"])
        self.assertNotEqual(records[0]["raw_registration_ref"], records[1]["raw_registration_ref"])
        changed = copy.deepcopy(records)
        changed[1] = copy.deepcopy(changed[0])
        with self.assertRaises(ValueError):
            self.study.estimate(changed, weights, "corner5")
        for plan in ("corner4", "repair5"):
            changed = self.study.make_records([-1] * len(self.study.PLAN_SLOTS[plan]), plan)
            changed[0]["shot_id"] = 2
            changed[0]["raw_registration_ref"] = "packet:00:2"
            with self.subTest(plan=plan), self.assertRaises(ValueError):
                self.study.estimate(changed, self.weights[plan], plan)

    def test_all_zero_weights_still_require_every_planned_record(self):
        for plan in self.protocol["plans"]:
            records = self.study.make_records([-1] * len(plan["slots"]), plan["id"])
            weights = dict.fromkeys(self.weights[plan["id"]], Fraction(0))
            self.assertEqual(self.study.estimate(records, weights, plan["id"]), 0)
            for index in range(len(records)):
                changed = records[:index] + records[index + 1 :]
                with self.subTest(plan=plan["id"], missing=index), self.assertRaises(ValueError):
                    self.study.estimate(changed, weights, plan["id"])

    def test_record_only_decoder_has_no_private_protocol_or_file_access(self):
        for plan in self.protocol["plans"]:
            records = self.study.make_records([-1] * len(plan["slots"]), plan["id"])
            weights = self.weights[plan["id"]]
            expected = -sum(weights.values())
            with (
                mock.patch.object(
                    self.study, "load_protocol", side_effect=AssertionError("private protocol read")
                ),
                mock.patch.object(
                    self.study, "compare_routes", side_effect=AssertionError("private report read")
                ),
                mock.patch("builtins.open", side_effect=AssertionError("file read")),
                mock.patch.object(Path, "read_bytes", side_effect=AssertionError("file read")),
                mock.patch.object(Path, "read_text", side_effect=AssertionError("file read")),
            ):
                self.assertEqual(self.study.estimate(records, weights, plan["id"]), expected)

    def test_private_access_context_and_slot_refusals_for_all_plans(self):
        for plan in self.protocol["plans"]:
            records = self.study.make_records([-1] * len(plan["slots"]), plan["id"])
            for name, changed in malformed_records(records, self.protocol):
                with self.subTest(plan=plan["id"], case=name), self.assertRaises(ValueError):
                    self.study.estimate(changed, self.weights[plan["id"]], plan["id"])
            for other in self.study.PLAN_SLOTS:
                if other != plan["id"]:
                    with (
                        self.subTest(plan=plan["id"], wrong_plan=other),
                        self.assertRaises(ValueError),
                    ):
                        self.study.estimate(records, self.weights[plan["id"]], other)

    def test_unknown_plan_invalid_constructor_and_strict_native_types(self):
        class StringSubclass(str):
            pass

        class ListSubclass(list):
            pass

        class DictSubclass(dict):
            pass

        class FractionSubclass(Fraction):
            pass

        for bad_plan in (None, True, 1, "unknown", StringSubclass("repair5")):
            with self.subTest(plan=repr(bad_plan)):
                with self.assertRaises(ValueError):
                    self.study.make_records([-1] * 5, bad_plan)
                with self.assertRaises(ValueError):
                    self.study.estimate([], {}, bad_plan)
        for plan in self.protocol["plans"]:
            plan_id, n = plan["id"], len(plan["slots"])
            for outcomes in (
                None,
                [],
                [-1] * (n - 1),
                [-1] * (n + 1),
                [True] + [-1] * (n - 1),
                [0] + [-1] * (n - 1),
                [1.0] + [-1] * (n - 1),
            ):
                with (
                    self.subTest(plan=plan_id, outcomes=repr(outcomes)),
                    self.assertRaises(ValueError),
                ):
                    self.study.make_records(outcomes, plan_id)
            records = self.study.make_records([-1] * n, plan_id)
            weights = self.weights[plan_id]
            bad_records = [ListSubclass(records)]
            changed = copy.deepcopy(records)
            changed[-1] = DictSubclass(changed[-1])
            bad_records.append(changed)
            for key in ("station_id", "acquisition_plan_id"):
                changed = copy.deepcopy(records)
                changed[-1][key] = StringSubclass(changed[-1][key])
                bad_records.append(changed)
            for changed in bad_records:
                with self.assertRaises(ValueError):
                    self.study.estimate(changed, weights, plan_id)
            bad_weights = [None, [], {}, DictSubclass(weights), list(weights.values())]
            for value in (0, True, "1", 1.0, None, FractionSubclass(1)):
                changed = dict(weights)
                changed[next(iter(changed))] = value
                bad_weights.append(changed)
            changed = dict(weights)
            station = next(iter(changed))
            changed[StringSubclass(station)] = changed.pop(station)
            bad_weights.append(changed)
            for changed in bad_weights:
                with (
                    self.subTest(plan=plan_id, weights=repr(changed)),
                    self.assertRaises(ValueError),
                ):
                    self.study.estimate(records, changed, plan_id)

    def test_complete_observer_analysis_and_selected_bc_bridge(self):
        with mock.patch.object(self.study, "compare_routes", return_value=self.report):
            result = self.study.analysis()
        exact_keys(self, result, "mathematics observer bc_restriction")
        self.assertEqual(result["mathematics"], self.study.encode(self.report))
        self.assertEqual(
            result["bc_restriction"], {"status": "matched", "profiles": 6, "branches": 96}
        )
        observer = result["observer"]
        exact_keys(self, observer, "estimates record_order_checks record_refusals")
        self.assertEqual(
            observer["estimates"],
            [
                {
                    "profile": profile["id"],
                    "plans": [
                        {
                            "id": plan["id"],
                            "estimates": [
                                str(row["estimate"]) for row in profile["plans"][plan["id"]]["rows"]
                            ],
                        }
                        for plan in self.protocol["plans"]
                    ],
                }
                for profile in self.report["profiles"]
            ],
        )
        self.assertEqual(
            observer["record_order_checks"],
            sum(
                2 * len(profile["plans"][plan["id"]]["rows"])
                for profile in self.report["profiles"]
                for plan in self.protocol["plans"]
            ),
        )
        labels = [(item["plan"], item["case"]) for item in observer["record_refusals"]]
        self.assertEqual(len(labels), len(set(labels)))
        for plan in self.protocol["plans"]:
            cases = {case for name, case in labels if name == plan["id"]}
            self.assertTrue(
                {"missing_slot", "extra_slot", "duplicate_slot", "missing_outcome"}.issubset(cases)
            )
            self.assertTrue(
                {
                    "private_" + key
                    for key in ("profile", "f", "theta", "rho", "likelihood", "target", "seed")
                }.issubset(cases)
            )


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
        with tempfile.TemporaryDirectory(prefix="det8-qr05bd-loader-") as temporary:
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
    """One representative scalar per field, plus late-row and shape corruptions."""
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
                changed_value = str(Fraction(value) + 1)
            except ValueError:
                changed_value = value + "-changed"
        elif type(value) is int:
            changed_value = value + 1
        else:
            changed_value = "changed"
        changed = copy.deepcopy(original)
        set_path(changed, path, changed_value)
        yield "scalar " + repr(path), changed
    for plan in ("corner4", "repair5", "corner5"):
        for key in ("probability", "estimate"):
            path = ("mathematics", "profiles", -1, "plans", plan, "rows", -1, key)
            changed = copy.deepcopy(original)
            set_path(changed, path, str(Fraction(get_path(changed, path)) + 1))
            yield "late " + repr(path), changed
        path = ("mathematics", "profiles", -1, "plans", plan, "rows", -1, "state_diagonal", -1)
        changed = copy.deepcopy(original)
        set_path(changed, path, str(Fraction(get_path(changed, path)) + 1))
        yield "late " + repr(path), changed
    for path in (
        ("mathematics", "profiles"),
        ("mathematics", "geometry", "coefficient_decoder", 0),
        ("mathematics", "profiles", -1, "plans", "corner5", "rows"),
        ("mathematics", "off_model", "state_diagonals", -1),
        ("observer", "record_refusals"),
    ):
        changed = copy.deepcopy(original)
        set_path(changed, path, get_path(changed, path)[:-1])
        yield "truncated " + repr(path), changed
    for path in (("mathematics", "plans", 0, "cost"), ("bc_restriction", "profiles")):
        changed = copy.deepcopy(original)
        set_path(changed, path, True)
        yield "type " + repr(path), changed
    for key in original:
        changed = copy.deepcopy(original)
        del changed[key]
        yield "missing " + key, changed
    changed = copy.deepcopy(original)
    changed["private"] = "hidden"
    yield "extra private field", changed


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_module("study")
        self.directory = tempfile.TemporaryDirectory(prefix="det8-qr05bd-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.freeze = self.root / "freeze.json"
        self.capture_path = self.root / "capture.json"
        self.sources = {"synthetic/source.py": {"bytes": 1, "sha256": "a" * 64}}
        self.small = {"mathematics": {"exact": "1/3", "count": 1}, "observer": {"available": True}}
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
        self.assertEqual(evidence["schema"], "QR-05BD-evidence-v1")
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
            (("analysis", "observer", "available"), 1),
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

    def test_complete_report_and_observer_non_noop_mutations(self):
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


def selected_bc_fixture(study, report):
    """New in-memory producer fixture containing precisely the selected overlap."""
    previous = {
        "geometry": {
            "volume": report["geometry"]["volume"],
            "sigma": report["geometry"]["sigma"],
            "weights": report["geometry"]["corner_weights"],
        },
        "profiles": [],
        "unselected_auxiliary": {"label_control": "not replayed"},
    }
    for current in report["profiles"][:6]:
        plan = current["plans"]["corner4"]
        previous["profiles"].append(
            {
                "id": current["id"],
                "corners": current["corners"],
                "target": current["target"],
                "mean": plan["mean"],
                "variance": plan["variance"],
                "rows": plan["rows"],
                "swapped_mean": "not selected",
                "naive_target": "not selected",
            }
        )
    return study.encode({"analysis": {"mathematics": previous}})


class HistoricalBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def restriction(self, document, current=None):
        data = json.dumps(document, sort_keys=True).encode("utf-8")
        identities = dict(self.study.BC_IDENTITIES)
        identities["results.json"] = hashlib.sha256(data).hexdigest()
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=data),
            mock.patch.object(self.study, "BC_IDENTITIES", identities),
            mock.patch.object(
                self.study, "_load_engine", side_effect=AssertionError("old executor read")
            ),
        ):
            return self.study._bc_restriction(self.report if current is None else current)

    def test_selected_bc_restriction_without_auxiliary_replay(self):
        document = selected_bc_fixture(self.study, self.report)
        self.assertEqual(
            self.restriction(document), {"status": "matched", "profiles": 6, "branches": 96}
        )
        changed = copy.deepcopy(document)
        changed["analysis"]["mathematics"]["unselected_auxiliary"] = None
        changed["analysis"]["mathematics"]["profiles"][0]["swapped_mean"] = "changed unused control"
        changed["analysis"]["mathematics"]["profiles"][0]["naive_target"] = "changed unused control"
        self.assertNotEqual(changed, document)
        self.assertEqual(
            self.restriction(changed), {"status": "matched", "profiles": 6, "branches": 96}
        )

    def test_semantic_selected_producer_mutations_after_identity_admission(self):
        document = selected_bc_fixture(self.study, self.report)
        paths = [("geometry", key) for key in ("volume", "sigma")]
        paths += [("geometry", "weights", 0), ("profiles", -1, "corners", 0)]
        paths += [("profiles", -1, key) for key in ("target", "mean", "variance")]
        paths += [("profiles", -1, "rows", -1, key) for key in ("probability", "estimate")]
        paths += [("profiles", -1, "rows", -1, "state_diagonal", -1)]
        for path in paths:
            changed = copy.deepcopy(document)
            full = ("analysis", "mathematics", *path)
            set_path(changed, full, str(Fraction(get_path(changed, full)) + 1))
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)
        for path, value in (
            (("profiles", 0, "id"), "wrong"),
            (("profiles", -1, "rows", -1, "outcomes", 0), True),
            (("profiles", -1, "rows"), []),
        ):
            changed = copy.deepcopy(document)
            set_path(changed, ("analysis", "mathematics", *path), value)
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)
        current = copy.deepcopy(self.report)
        current["profiles"][0]["theta"] = Fraction(1)
        with self.assertRaises(ValueError):
            self.restriction(document, current)

    def test_historical_capture_hash_precedes_semantic_parsing(self):
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=b"{}"),
            mock.patch.object(
                self.study, "_parse_json", side_effect=AssertionError("unverified historical parse")
            ),
            self.assertRaises(ValueError),
        ):
            self.study._bc_restriction(self.report)


class SourceIdentityTests(unittest.TestCase):
    def test_exact_eleven_current_and_bc_source_identities(self):
        study = load_module("study")
        identities = study.source_identities()
        current = [
            HERE / name
            for name in (
                "README.md",
                "protocol.json",
                "quantum.py",
                "reference.py",
                "study.py",
                "test_qr05bd.py",
            )
        ]
        previous = [
            HERE.parent / "qr-05bc-local-record-estimator-2026-09-08" / name
            for name in (
                "README.md",
                "RESULTS.md",
                "protocol.json",
                "source-freeze.json",
                "results.json",
            )
        ]
        expected = current + previous
        self.assertEqual(len(identities), 11)
        self.assertEqual(set(identities), {str(path.relative_to(study.REPO)) for path in expected})
        for path in expected:
            data = path.read_bytes()
            self.assertEqual(
                identities[str(path.relative_to(study.REPO))],
                {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()},
            )
        self.assertEqual(study.read_json(study.FREEZE_PATH)["sources"], identities)

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
                study, "_parse_json", side_effect=AssertionError("unverified protocol parse")
            ),
            self.assertRaises(ValueError),
        ):
            study.load_protocol()

    def test_protocol_public_plan_and_context_native_types(self):
        study = load_module("study")
        protocol = read_protocol()
        paths = [
            (("plans", 0, "slots", 0, 1), True),
            (("plans", 1, "cost"), True),
            (("plans", 2, "slots", 1, 1), 1),
            (("public_context", "setting_id"), "X"),
        ]
        for path, value in paths:
            changed = copy.deepcopy(protocol)
            set_path(changed, path, value)
            data = json.dumps(changed).encode("utf-8")
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
