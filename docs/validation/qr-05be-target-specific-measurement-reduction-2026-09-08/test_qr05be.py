"""Source-bound BE contract tests, using only the standard library.

Import performs no fixture mathematics or engine execution. All tests wait
for the first source-bound release. Checks remain active under Python -O.
The degree-five geometry oracle is new; owned BD test mechanics are
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
PROTOCOL_SHA256 = "35c28b24b399c282eaaea62410d8ac1044050462e7080abe90bb868755ece979"


def load_module(name):
    spec = importlib.util.spec_from_file_location("qr05be_test_" + name, HERE / (name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("BE source could not be loaded")
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


def station_weights(plan_id, corner, repair):
    full = dict(zip(("00", "10", "01", "11", "cc"), repair, strict=True))
    if plan_id in ("corner4", "corner5"):
        return dict(zip(("00", "10", "01", "11"), corner, strict=True))
    if plan_id == "repair5":
        return full
    if plan_id in ("target4", "repeatcc5"):
        return {station: full[station] for station in ("00", "10", "01", "cc")}
    raise ValueError("Unknown test acquisition plan")


def event_weights(plan, corner, repair):
    weights = station_weights(plan["id"], corner, repair)
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


def row_rank(rows):
    """Independent exact Gram–Schmidt rank; no engine elimination helper."""
    orthogonal = []
    for source in rows:
        residual = list(source)
        for vector in orthogonal:
            coefficient = dot(residual, vector) / dot(vector, vector)
            residual = [
                value - coefficient * entry for value, entry in zip(residual, vector, strict=True)
            ]
        if any(residual):
            orthogonal.append(residual)
    return len(orthogonal)


def traced_diagonal(diagonal, omitted):
    """Construct each retained bit string and insert the two discarded bits."""
    result = []
    for retained in itertools.product((0, 1), repeat=4):
        entry = Fraction(0)
        for discarded in (0, 1):
            bits = (*retained[:omitted], discarded, *retained[omitted:])
            index = 0
            for bit in bits:
                index = 2 * index + bit
            entry += diagonal[index]
        result.append(entry)
    return result


class ProtocolTests(unittest.TestCase):
    def test_frozen_protocol_and_finite_plan_domain(self):
        self.assertEqual(
            hashlib.sha256((HERE / "protocol.json").read_bytes()).hexdigest(), PROTOCOL_SHA256
        )
        protocol = read_protocol()
        self.assertEqual(protocol["study"], "QR-05BE")
        self.assertEqual(protocol["stations"], ["00", "10", "01", "11", "cc"])
        self.assertEqual(protocol["outcomes"], [-1, 1])
        self.assertEqual(len(protocol["profiles"]), 12)
        self.assertEqual(
            [p["id"] for p in protocol["plans"]],
            ["corner4", "repair5", "corner5", "target4", "repeatcc5"],
        )
        self.assertEqual([len(p["slots"]) for p in protocol["plans"]], [4, 5, 5, 4, 5])
        self.assertEqual(len(protocol["record_keys"]), 15)
        self.assertEqual(protocol["reduction"]["omitted_station"], "11")
        self.assertEqual(protocol["off_model"]["plans"], ["repair5", "target4", "repeatcc5"])

    def test_boole_certificate_before_any_product_integration(self):
        nodes, weights = boole_rule()
        declared = read_protocol()["third_oracle"]
        self.assertEqual(nodes, tuple(map(Fraction, declared["nodes"])))
        self.assertEqual(weights, tuple(map(Fraction, declared["weights"])))
        self.assertEqual(declared["verify_moments_through"], 5)
        for power in range(6):
            self.assertEqual(
                sum(weight * node**power for node, weight in zip(nodes, weights, strict=True)),
                Fraction(1, power + 1),
            )
        for a, b in itertools.product(range(6), repeat=2):
            self.assertEqual(
                integrate_unit(lambda u, v, a=a, b=b: u**a * v**b), Fraction(1, (a + 1) * (b + 1))
            )


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.corner, cls.repair = compiled_weights()
        cls.coordinates = [tuple(map(Fraction, point)) for point in cls.protocol["coordinates"]]
        cls.plans = {plan["id"]: plan for plan in cls.protocol["plans"]}

    def test_geometry_inverse_and_target_specific_null_certificate(self):
        exact_keys(
            self,
            self.report,
            "geometry operators schedule_counts plans reduction profiles collision off_model",
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
        self.assertEqual(geometry["bubble_at_center"], bubble(*self.coordinates[-1]))
        self.assertEqual(
            geometry["center_basis"],
            [basis(s, *self.coordinates[-1]) for s in self.protocol["stations"][:4]],
        )
        matrix = [
            [basis(s, u, v) for s in self.protocol["stations"][:4]] + [bubble(u, v)]
            for u, v in self.coordinates
        ]
        self.assertEqual(geometry["evaluation_matrix"], matrix)
        decoder = geometry["coefficient_decoder"]
        self.assertEqual(len(decoder), 5)
        self.assertTrue(all(len(row) == 5 for row in decoder))
        identity = [[Fraction(i == j) for j in range(5)] for i in range(5)]
        self.assertEqual(product(matrix, decoder), identity)
        self.assertEqual(product(decoder, matrix), identity)
        q = self.corner + [functional(bubble)]
        self.assertEqual(
            [sum(q[j] * decoder[j][i] for j in range(5)) for i in range(5)], self.repair
        )
        self.assertEqual(
            [sum(self.repair[j] * matrix[j][i] for j in range(5)) for i in range(5)], q
        )
        self.assertEqual(geometry["weight_sum"], sum(self.repair))
        reduction = self.report["reduction"]
        exact_keys(
            self,
            reduction,
            "retained_indices omitted_index retained_evaluation_matrix retained_rank omission_direction retained_null_image target_null_image target_weights",
        )
        indices = [
            self.protocol["stations"].index(s)
            for s in self.protocol["reduction"]["retained_stations"]
        ]
        omitted = self.protocol["stations"].index(self.protocol["reduction"]["omitted_station"])
        self.assertEqual(reduction["retained_indices"], indices)
        self.assertEqual(reduction["omitted_index"], omitted)
        retained = [matrix[i] for i in indices]
        direction = [row[omitted] for row in decoder]
        self.assertEqual(reduction["retained_evaluation_matrix"], retained)
        self.assertEqual(reduction["retained_rank"], row_rank(retained))
        self.assertLess(reduction["retained_rank"], row_rank(matrix))
        self.assertEqual(reduction["omission_direction"], direction)
        self.assertTrue(any(direction))
        self.assertEqual(
            [dot(row, direction) for row in matrix], [Fraction(i == omitted) for i in range(5)]
        )
        self.assertEqual(
            reduction["retained_null_image"], [dot(row, direction) for row in retained]
        )
        self.assertEqual(reduction["retained_null_image"], [Fraction(0)] * 4)
        self.assertEqual(reduction["target_null_image"], dot(q, direction))
        self.assertEqual(reduction["target_null_image"], 0)
        self.assertEqual(reduction["target_weights"], [self.repair[i] for i in indices])

    def test_operators_full_factor_orders_and_plan_weights(self):
        exact_keys(self, self.report["operators"], "corner4 five_factor")
        exact_keys(self, self.report["schedule_counts"], "corner4 five_factor")
        for name, n in (("corner4", 4), ("five_factor", 5)):
            operators = self.report["operators"][name]
            orders = list(itertools.permutations(range(n)))
            self.assertEqual(self.report["schedule_counts"][name], len(orders))
            self.assertEqual(len(operators), 2**n)
            for row, outcomes in zip(operators, itertools.product((-1, 1), repeat=n), strict=True):
                exact_keys(self, row, "outcomes kraus_diagonal")
                self.assertEqual(row["outcomes"], list(outcomes))
                expected = [
                    Fraction(
                        all(
                            outcome == 1 - 2 * bit
                            for outcome, bit in zip(outcomes, bits, strict=True)
                        )
                    )
                    for bits in itertools.product((0, 1), repeat=n)
                ]
                self.assertEqual(row["kraus_diagonal"], expected)
                for order in orders:
                    self.assertEqual(
                        [
                            Fraction(all(outcomes[i] == 1 - 2 * bits[i] for i in order))
                            for bits in itertools.product((0, 1), repeat=n)
                        ],
                        expected,
                    )
            self.assertEqual(
                [sum(row["kraus_diagonal"][i] for row in operators) for i in range(2**n)],
                [Fraction(1)] * (2**n),
            )
        self.assertEqual(len(self.report["plans"]), 5)
        for actual, plan in zip(self.report["plans"], self.protocol["plans"], strict=True):
            exact_keys(self, actual, "id slots cost event_weights")
            self.assertEqual(actual["id"], plan["id"])
            self.assertEqual(actual["slots"], plan["slots"])
            self.assertEqual(actual["cost"], len(plan["slots"]))
            self.assertEqual(actual["cost"], plan["cost"])
            self.assertEqual(actual["event_weights"], event_weights(plan, self.corner, self.repair))

    def check_plan(self, result, plan, means, target):
        exact_keys(self, result, "rows mean bias variance mse")
        event_means = [means[station] for station, _shot in plan["slots"]]
        coefficients = event_weights(plan, self.corner, self.repair)
        n = len(plan["slots"])
        self.assertEqual(len(result["rows"]), 2**n)
        total = first = second = Fraction(0)
        state = [Fraction(0)] * (2**n)
        operators = self.report["operators"]["corner4" if n == 4 else "five_factor"]
        for row, outcomes, operator in zip(
            result["rows"], itertools.product((-1, 1), repeat=n), operators, strict=True
        ):
            exact_keys(self, row, "outcomes probability state_diagonal estimate")
            mass, estimate = probability(event_means, outcomes), dot(coefficients, outcomes)
            self.assertEqual(row["outcomes"], list(outcomes))
            self.assertEqual(row["probability"], mass)
            self.assertEqual(row["estimate"], estimate)
            self.assertEqual(
                row["state_diagonal"], [mass * value for value in operator["kraus_diagonal"]]
            )
            self.assertEqual(sum(row["state_diagonal"]), mass)
            total += mass
            first += mass * estimate
            second += mass * estimate**2
            for i, value in enumerate(row["state_diagonal"]):
                state[i] += value
        self.assertEqual(total, 1)
        self.assertEqual(
            state,
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

    def test_all_twelve_profile_integrals_and_five_complete_plan_laws(self):
        self.assertEqual(len(self.report["profiles"]), 12)
        for current, fixture in zip(
            self.report["profiles"], self.protocol["profiles"], strict=True
        ):
            with self.subTest(profile=fixture["id"]):
                exact_keys(
                    self,
                    current,
                    "id corners theta admission_bound sample_means recovered_coefficients target corner_target plans marginalization reallocation mse_differences",
                )
                corners, theta = list(map(Fraction, fixture["corners"])), Fraction(fixture["theta"])
                means = [profile_value(corners, theta, *point) for point in self.coordinates]
                target = functional(lambda u, v, c=corners, t=theta: profile_value(c, t, u, v))
                self.assertEqual(current["id"], fixture["id"])
                self.assertEqual(current["corners"], corners)
                self.assertEqual(current["theta"], theta)
                self.assertEqual(
                    current["admission_bound"], max(map(abs, corners)) + abs(theta) / 16
                )
                self.assertLessEqual(current["admission_bound"], 1)
                self.assertEqual(current["sample_means"], means)
                self.assertTrue(all(-1 <= value <= 1 for value in means))
                self.assertEqual(current["recovered_coefficients"], corners + [theta])
                self.assertEqual(
                    [dot(row, means) for row in self.report["geometry"]["coefficient_decoder"]],
                    corners + [theta],
                )
                self.assertEqual(current["target"], target)
                self.assertEqual(
                    current["corner_target"],
                    functional(lambda u, v, c=corners: profile_value(c, Fraction(0), u, v)),
                )
                exact_keys(self, current["plans"], "corner4 repair5 corner5 target4 repeatcc5")
                station_means = dict(zip(self.protocol["stations"], means, strict=True))
                for plan in self.protocol["plans"]:
                    self.check_plan(current["plans"][plan["id"]], plan, station_means, target)
                    if plan["weights"] != "corner":
                        self.assertEqual(current["plans"][plan["id"]]["bias"], 0)
                    else:
                        self.assertEqual(
                            current["plans"][plan["id"]]["bias"], -theta * functional(bubble)
                        )

    def check_marginal(self, current):
        marginal = current["marginalization"]
        exact_keys(
            self, marginal, "rows pathwise_checks wrong_trace_disagreements moment_differences"
        )
        full, reduced = current["plans"]["repair5"], current["plans"]["target4"]
        retained = self.report["reduction"]["retained_indices"]
        omitted = self.report["reduction"]["omitted_index"]
        self.assertEqual(len(marginal["rows"]), 16)
        pathwise = wrong_count = 0
        for row, target_row in zip(marginal["rows"], reduced["rows"], strict=True):
            exact_keys(
                self,
                row,
                "outcomes full_indices full_estimates probability summed_full_state reduced_state wrong_trace_state estimate",
            )
            self.assertEqual(row["outcomes"], target_row["outcomes"])
            indices = [
                i
                for i, old in enumerate(full["rows"])
                if [old["outcomes"][index] for index in retained] == row["outcomes"]
            ]
            self.assertEqual(len(indices), 2)
            self.assertEqual(row["full_indices"], indices)
            old_rows = [full["rows"][i] for i in indices]
            self.assertEqual(row["full_estimates"], [old["estimate"] for old in old_rows])
            for old in old_rows:
                self.assertEqual(old["estimate"], target_row["estimate"])
                pathwise += 1
            summed = [sum(old["state_diagonal"][i] for old in old_rows) for i in range(32)]
            self.assertEqual(row["summed_full_state"], summed)
            self.assertEqual(len(row["summed_full_state"]), 32)
            self.assertEqual(row["probability"], sum(old["probability"] for old in old_rows))
            self.assertEqual(row["probability"], target_row["probability"])
            self.assertEqual(row["reduced_state"], traced_diagonal(summed, omitted))
            self.assertEqual(row["reduced_state"], target_row["state_diagonal"])
            self.assertEqual(len(row["reduced_state"]), 16)
            self.assertEqual(sum(summed), sum(row["reduced_state"]))
            self.assertEqual(row["wrong_trace_state"], traced_diagonal(summed, 4))
            self.assertEqual(row["estimate"], target_row["estimate"])
            wrong_count += row["wrong_trace_state"] != row["reduced_state"]
        self.assertEqual(marginal["pathwise_checks"], pathwise)
        self.assertEqual(pathwise, len(full["rows"]))
        self.assertEqual(marginal["wrong_trace_disagreements"], wrong_count)
        exact_keys(self, marginal["moment_differences"], "mean variance mse")
        for key in ("mean", "variance", "mse"):
            self.assertEqual(marginal["moment_differences"][key], reduced[key] - full[key])
            self.assertEqual(marginal["moment_differences"][key], 0)

    def test_full_and_reduced_states_pathwise_zero_branches_and_wrong_subsystem(self):
        for profile in self.report["profiles"]:
            with self.subTest(profile=profile["id"]):
                self.check_marginal(profile)
        self.assertTrue(
            any(
                profile["marginalization"]["wrong_trace_disagreements"] > 0
                for profile in self.report["profiles"]
            )
        )
        self.assertTrue(
            any(
                row["probability"] == 0
                for profile in self.report["profiles"]
                for row in profile["plans"]["repair5"]["rows"]
            )
        )

    def test_reallocation_variance_identity_and_all_signed_cost_comparisons(self):
        self.assertEqual(self.plans["target4"]["cost"], self.plans["corner4"]["cost"])
        self.assertEqual(self.plans["repeatcc5"]["cost"], self.plans["corner5"]["cost"])
        for profile in self.report["profiles"]:
            reallocation = profile["reallocation"]
            exact_keys(
                self,
                reallocation,
                "direct_variance_reduction predicted_variance_reduction direct_mse_reduction",
            )
            target, repeat = profile["plans"]["target4"], profile["plans"]["repeatcc5"]
            direct = target["variance"] - repeat["variance"]
            predicted = self.repair[-1] ** 2 * (1 - profile["sample_means"][-1] ** 2) / 2
            self.assertEqual(reallocation["direct_variance_reduction"], direct)
            self.assertEqual(reallocation["predicted_variance_reduction"], predicted)
            self.assertEqual(direct, predicted)
            self.assertGreaterEqual(direct, 0)
            self.assertEqual(target["mean"], repeat["mean"])
            self.assertEqual(target["bias"], repeat["bias"])
            self.assertEqual(reallocation["direct_mse_reduction"], target["mse"] - repeat["mse"])
            self.assertEqual(reallocation["direct_mse_reduction"], direct)
            exact_keys(
                self,
                profile["mse_differences"],
                "target4_minus_corner4 repeatcc5_minus_corner5 repeatcc5_minus_repair5",
            )
            for key, left, right in (
                ("target4_minus_corner4", "target4", "corner4"),
                ("repeatcc5_minus_corner5", "repeatcc5", "corner5"),
                ("repeatcc5_minus_repair5", "repeatcc5", "repair5"),
            ):
                self.assertEqual(
                    profile["mse_differences"][key],
                    profile["plans"][left]["mse"] - profile["plans"][right]["mse"],
                )

    def test_collision_preserves_target_not_full_coefficients_or_full_states(self):
        collision = self.report["collision"]
        exact_keys(
            self,
            collision,
            "profiles coefficients_difference full_means_difference target_difference omitted_states full_averaged_states full_law_total_variation retained_law_total_variation",
        )
        self.assertEqual(collision["profiles"], self.protocol["collision"]["profiles"])
        by_id = {profile["id"]: profile for profile in self.report["profiles"]}
        first, second = [by_id[name] for name in collision["profiles"]]
        self.assertEqual(
            collision["coefficients_difference"],
            [
                b - a
                for a, b in zip(
                    first["recovered_coefficients"], second["recovered_coefficients"], strict=True
                )
            ],
        )
        self.assertTrue(any(collision["coefficients_difference"]))
        self.assertEqual(
            collision["full_means_difference"],
            [b - a for a, b in zip(first["sample_means"], second["sample_means"], strict=True)],
        )
        self.assertEqual(collision["target_difference"], second["target"] - first["target"])
        self.assertEqual(collision["target_difference"], 0)
        omitted = self.report["reduction"]["omitted_index"]
        states = [
            [(1 + profile["sample_means"][omitted]) / 2, (1 - profile["sample_means"][omitted]) / 2]
            for profile in (first, second)
        ]
        self.assertEqual(collision["omitted_states"], states)
        self.assertNotEqual(states[0], states[1])
        averaged = [
            [
                sum(row["state_diagonal"][i] for row in profile["plans"]["repair5"]["rows"])
                for i in range(32)
            ]
            for profile in (first, second)
        ]
        self.assertEqual(collision["full_averaged_states"], averaged)
        self.assertNotEqual(averaged[0], averaged[1])
        for plan, key in (
            ("repair5", "full_law_total_variation"),
            ("target4", "retained_law_total_variation"),
        ):
            left, right = first["plans"][plan]["rows"], second["plans"][plan]["rows"]
            variation = (
                sum(
                    abs(b["probability"] - a["probability"])
                    for a, b in zip(left, right, strict=True)
                )
                / 2
            )
            self.assertEqual(collision[key], variation)
        self.assertGreater(collision["full_law_total_variation"], 0)
        self.assertEqual(collision["retained_law_total_variation"], 0)

    def test_off_model_all_three_plans_and_full_marginal_certificate(self):
        off = self.report["off_model"]
        exact_keys(self, off, "id sample_means global_bound target plans marginalization")
        amplitude = Fraction(self.protocol["off_model"]["amplitude"])

        def h(u, v):
            return (
                amplitude * bubble(u, v) * ((u - Fraction(1, 2)) ** 2 + (v - Fraction(1, 2)) ** 2)
            )

        self.assertEqual(off["id"], self.protocol["off_model"]["id"])
        self.assertEqual(off["sample_means"], [h(*point) for point in self.coordinates])
        self.assertEqual(off["global_bound"], Fraction(self.protocol["off_model"]["global_bound"]))
        self.assertEqual(off["target"], functional(h))
        self.assertGreater(off["target"], 0)
        exact_keys(self, off["plans"], "repair5 target4 repeatcc5")
        zero = next(profile for profile in self.report["profiles"] if profile["id"] == "zero")
        self.assertEqual(off["sample_means"], zero["sample_means"])
        means = dict(zip(self.protocol["stations"], off["sample_means"], strict=True))
        for plan_id in self.protocol["off_model"]["plans"]:
            self.check_plan(off["plans"][plan_id], self.plans[plan_id], means, off["target"])
            self.assertEqual(off["plans"][plan_id]["rows"], zero["plans"][plan_id]["rows"])
            self.assertEqual(off["plans"][plan_id]["bias"], -off["target"])
        self.check_marginal(off)

    def test_strict_fraction_quantities_and_native_label_indices(self):
        wire = self.study.encode(self.report)
        integer_keys = {
            "cost",
            "omitted_index",
            "retained_rank",
            "pathwise_checks",
            "wrong_trace_disagreements",
        }
        integer_vectors = {"outcomes", "retained_indices", "full_indices"}

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
            elif (
                path[-1] == "id"
                or path[:2] == ("collision", "profiles")
                or ("slots" in path and path[-1] == 0)
            ):
                self.assertIs(type(raw), str, path)
                self.assertIs(type(encoded), str)
                self.assertEqual(raw, encoded)
            elif (
                path[0] == "schedule_counts"
                or path[-1] in integer_keys
                or any(key in path for key in integer_vectors)
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
            if type(value) is type(base[-1][key]) and value == base[-1][key]:
                continue
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
            plan["id"]: station_weights(plan["id"], corner, repair)
            for plan in cls.protocol["plans"]
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
        for profile in [*self.report["profiles"], self.report["off_model"]]:
            for plan in self.protocol["plans"]:
                plan_id = plan["id"]
                if plan_id not in profile["plans"]:
                    continue
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
        for plan in ("corner4", "repair5", "target4", "repeatcc5"):
            changed = self.study.make_records([-1] * len(self.study.PLAN_SLOTS[plan]), plan)
            changed[0]["shot_id"] = 2
            changed[0]["raw_registration_ref"] = "packet:00:2"
            with self.subTest(plan=plan), self.assertRaises(ValueError):
                self.study.estimate(changed, self.weights[plan], plan)

        records = self.study.make_records([-1, -1, -1, -1, 1], "repeatcc5")
        weights = {
            station: Fraction(index + 1) for index, station in enumerate(("00", "10", "01", "cc"))
        }
        self.assertEqual(
            self.study.estimate(records, weights, "repeatcc5"),
            -sum(value for station, value in weights.items() if station != "cc"),
        )
        self.assertEqual(records[-2]["station_id"], records[-1]["station_id"])
        self.assertNotEqual(records[-2]["shot_id"], records[-1]["shot_id"])
        self.assertNotEqual(
            records[-2]["raw_registration_ref"], records[-1]["raw_registration_ref"]
        )
        changed = copy.deepcopy(records)
        changed[-1] = copy.deepcopy(changed[-2])
        with self.assertRaises(ValueError):
            self.study.estimate(changed, weights, "repeatcc5")

    def test_target_plan_omission_does_not_relax_repair5_contract(self):
        records = self.study.make_records([-1] * 5, "repair5")
        missing = [record for record in records if record["station_id"] != "11"]
        with self.assertRaises(ValueError):
            self.study.estimate(missing, self.weights["repair5"], "repair5")
        with self.assertRaises(ValueError):
            self.study.estimate(missing, self.weights["target4"], "target4")
        target_records = self.study.make_records([-1] * 4, "target4")
        self.assertEqual(
            self.study.estimate(target_records, self.weights["target4"], "target4"),
            -sum(self.weights["target4"].values()),
        )
        self.assertNotIn("11", {record["station_id"] for record in target_records})

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

    def test_complete_observer_analysis_and_selected_bd_bridge(self):
        with mock.patch.object(self.study, "compare_routes", return_value=self.report):
            result = self.study.analysis()
        exact_keys(self, result, "mathematics observer bd_restriction")
        self.assertEqual(result["mathematics"], self.study.encode(self.report))
        self.assertEqual(
            result["bd_restriction"],
            {
                "status": "matched",
                "profiles": 10,
                "plans": 3,
                "branches": 800,
                "off_model_branches": 32,
            },
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
                        if plan["id"] in profile["plans"]
                    ],
                }
                for profile in [*self.report["profiles"], self.report["off_model"]]
            ],
        )
        self.assertEqual(
            observer["record_order_checks"],
            sum(
                2 * len(profile["plans"][plan["id"]]["rows"])
                for profile in [*self.report["profiles"], self.report["off_model"]]
                for plan in self.protocol["plans"]
                if plan["id"] in profile["plans"]
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
        with tempfile.TemporaryDirectory(prefix="det8-qr05be-loader-") as temporary:
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
    for plan in ("corner4", "repair5", "corner5", "target4", "repeatcc5"):
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
        ("mathematics", "off_model", "plans", "repair5", "rows", -1, "state_diagonal"),
        ("observer", "record_refusals"),
    ):
        changed = copy.deepcopy(original)
        set_path(changed, path, get_path(changed, path)[:-1])
        yield "truncated " + repr(path), changed
    for path in (("mathematics", "plans", 0, "cost"), ("bd_restriction", "profiles")):
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
        self.directory = tempfile.TemporaryDirectory(prefix="det8-qr05be-test-")
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
        self.assertEqual(evidence["schema"], "QR-05BE-evidence-v1")
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


def selected_bd_fixture(study, report):
    """New in-memory producer fixture containing precisely the selected overlap."""
    old_plans = ("corner4", "repair5", "corner5")
    previous = {
        "geometry": report["geometry"],
        "operators": report["operators"],
        "schedule_counts": report["schedule_counts"],
        "plans": report["plans"][:3],
        "profiles": [],
        "global_controls": "not selected",
    }
    for current in report["profiles"][:10]:
        selected = {
            key: current[key]
            for key in (
                "id",
                "corners",
                "theta",
                "admission_bound",
                "sample_means",
                "recovered_coefficients",
                "target",
                "corner_target",
            )
        }
        selected["plans"] = {plan: current["plans"][plan] for plan in old_plans}
        selected["repair_decomposition"] = "not selected"
        selected["mse_differences"] = "not selected"
        previous["profiles"].append(selected)
    off = report["off_model"]
    repair = off["plans"]["repair5"]
    previous["off_model"] = {
        "sample_means": off["sample_means"],
        "global_bound": off["global_bound"],
        "target": off["target"],
        "estimator_mean": repair["mean"],
        "estimator_bias": repair["bias"],
        "estimator_variance": repair["variance"],
        "mse": repair["mse"],
        "probabilities": [row["probability"] for row in repair["rows"]],
        "state_diagonals": [row["state_diagonal"] for row in repair["rows"]],
    }
    return study.encode({"analysis": {"mathematics": previous}})


class HistoricalBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def restriction(self, document, current=None):
        data = json.dumps(document, sort_keys=True).encode("utf-8")
        identities = dict(self.study.BD_IDENTITIES)
        identities["results.json"] = hashlib.sha256(data).hexdigest()
        with (
            mock.patch.object(self.study, "_read_bounded", return_value=data),
            mock.patch.object(self.study, "BD_IDENTITIES", identities),
            mock.patch.object(
                self.study, "_load_engine", side_effect=AssertionError("old executor read")
            ),
        ):
            return self.study._bd_restriction(self.report if current is None else current)

    def test_selected_bd_restriction_without_auxiliary_replay(self):
        document = selected_bd_fixture(self.study, self.report)
        summary = {
            "status": "matched",
            "profiles": 10,
            "plans": 3,
            "branches": 800,
            "off_model_branches": 32,
        }
        self.assertEqual(self.restriction(document), summary)
        changed = copy.deepcopy(document)
        old = changed["analysis"]["mathematics"]
        old["global_controls"] = None
        old["profiles"][0]["repair_decomposition"] = "changed unused control"
        old["profiles"][0]["mse_differences"] = "changed unused control"
        self.assertNotEqual(changed, document)
        self.assertEqual(self.restriction(changed), summary)

    def test_semantic_selected_producer_mutations_after_identity_admission(self):
        document = selected_bd_fixture(self.study, self.report)
        paths = [("geometry", key) for key in ("volume", "sigma")]
        paths += [("geometry", key, 0) for key in ("corner_weights", "repair_weights")]
        paths += [("geometry", "evaluation_matrix", -1, -1)]
        paths += [("operators", "five_factor", -1, "kraus_diagonal", -1)]
        paths += [("plans", -1, "event_weights", -1)]
        paths += [
            ("profiles", -1, key, 0)
            for key in (
                "corners",
                "sample_means",
                "recovered_coefficients",
            )
        ]
        paths += [
            ("profiles", -1, key)
            for key in (
                "theta",
                "admission_bound",
                "target",
                "corner_target",
            )
        ]
        for plan in ("corner4", "repair5", "corner5"):
            prefix = ("profiles", -1, "plans", plan)
            paths += [(*prefix, key) for key in ("mean", "bias", "variance", "mse")]
            paths += [(*prefix, "rows", -1, key) for key in ("probability", "estimate")]
            paths += [(*prefix, "rows", -1, "state_diagonal", -1)]
        paths += [
            ("off_model", key)
            for key in (
                "global_bound",
                "target",
                "estimator_mean",
                "estimator_bias",
                "estimator_variance",
                "mse",
            )
        ]
        paths += [
            ("off_model", "sample_means", -1),
            ("off_model", "probabilities", -1),
            ("off_model", "state_diagonals", -1, -1),
        ]
        for path in paths:
            changed = copy.deepcopy(document)
            full = ("analysis", "mathematics", *path)
            set_path(changed, full, str(Fraction(get_path(changed, full)) + 1))
            self.assertNotEqual(changed, document)
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.restriction(changed)
        for path, value in (
            (("profiles", 0, "id"), "wrong"),
            (("schedule_counts", "corner4"), True),
            (("plans", -1, "cost"), True),
            (("plans", -1, "slots", -1, 1), True),
            (("profiles", -1, "plans", "repair5", "rows", -1, "outcomes", 0), True),
            (("profiles", -1, "plans", "corner5", "rows"), []),
        ):
            changed = copy.deepcopy(document)
            set_path(changed, ("analysis", "mathematics", *path), value)
            self.assertNotEqual(self.study.canonical(changed), self.study.canonical(document))
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
            self.study._bd_restriction(self.report)


class SourceIdentityTests(unittest.TestCase):
    def test_exact_eleven_current_and_bd_source_identities(self):
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
                "test_qr05be.py",
            )
        ]
        previous = [
            HERE.parent / "qr-05bd-interior-measurement-repair-2026-09-08" / name
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
