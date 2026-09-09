"""Bounded, exact BC contract tests using only the standard library.

Import and collection perform no fixture mathematics or engine execution.
The first test run is authorized only after the source-bound first capture.
All checks use unittest methods or explicit exceptions, including under -O.
No preceding numerical executor is imported.
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
PROTOCOL_SHA256 = "7b07d4961163f4241c2eb0452fc78d992f38995918418b20fd38acdf911cf340"


def load_module(name):
    """Load only a new BC source, lazily from a test body."""
    spec = importlib.util.spec_from_file_location("qr05bc_test_" + name, HERE / (name + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("BC source could not be loaded")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def rational(value):
    if type(value) is not str:
        raise ValueError("The report must retain a rational string")
    result = Fraction(value)
    if str(result) != value:
        raise ValueError("The report fraction must be canonical")
    return result


def exact_simpson(function):
    """Third route: integrate degree-at-most-three coordinates on the unit square."""
    nodes = (Fraction(0), Fraction(1, 2), Fraction(1))
    weights = (1, 4, 1)
    return (
        sum(
            weights[i] * weights[j] * function(u, v)
            for i, u in enumerate(nodes)
            for j, v in enumerate(nodes)
        )
        / 36
    )


def basis(station, u, v):
    return (u if station[0] == "1" else 1 - u) * (v if station[1] == "1" else 1 - v)


def direct_target(corners, stations):
    return exact_simpson(
        lambda u, v: (
            sum(corners[i] * basis(station, u, v) for i, station in enumerate(stations))
            * (1 - u)
            * (1 - v)
        )
    )


def direct_weights(stations):
    return {
        station: exact_simpson(
            lambda u, v, station=station: basis(station, u, v) * (1 - u) * (1 - v)
        )
        for station in stations
    }


def scalar_probability(corners, outcomes):
    probability = Fraction(1)
    for mean, outcome in zip(corners, outcomes, strict=True):
        probability *= (1 + mean * outcome) / 2
    return probability


def scalar_estimate(weights, stations, outcomes):
    return sum(
        weights[station] * outcome for station, outcome in zip(stations, outcomes, strict=True)
    )


def read_protocol():
    return json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def evaluated():
    """A single bounded engine comparison, first called after root release."""
    study = load_module("study")
    report = study.compare_routes()
    return study, study.load_protocol(), report


def exact_keys(test, value, keys):
    test.assertIs(type(value), dict)
    test.assertEqual(set(value), set(keys.split()))


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()
        cls.stations = cls.protocol["stations"]
        cls.weights = direct_weights(cls.stations)

    def test_complete_top_level_and_geometry(self):
        exact_keys(
            self,
            self.report,
            "geometry operators schedule_count schedule_discrepancies profiles "
            "bubble repeat calibrations error",
        )
        geometry = self.report["geometry"]
        exact_keys(self, geometry, "volume sigma weights weight_sum")
        measure = Fraction(self.protocol["geometry"]["measure_factor"])
        u0, u1 = map(Fraction, self.protocol["geometry"]["u"])
        v0, v1 = map(Fraction, self.protocol["geometry"]["v"])
        volume = measure * (u1 - u0) * (v1 - v0)
        self.assertEqual(geometry["volume"], volume)
        self.assertEqual(geometry["sigma"], volume**4)
        self.assertEqual(geometry["weights"], list(self.weights.values()))
        self.assertEqual(geometry["weight_sum"], sum(self.weights.values()))
        self.assertTrue(all(weight > 0 for weight in self.weights.values()))
        self.assertNotEqual(self.weights["00"], self.weights["11"])

    def test_kraus_operators_and_entire_schedule_domain(self):
        operators = self.report["operators"]
        outcomes = list(itertools.product((-1, 1), repeat=4))
        self.assertEqual(len(operators), len(outcomes))
        self.assertIs(type(self.report["schedule_count"]), int)
        self.assertEqual(self.report["schedule_count"], len(list(itertools.permutations(range(4)))))
        self.assertEqual(self.report["schedule_discrepancies"], [])
        for item, outcome in zip(operators, outcomes, strict=True):
            exact_keys(self, item, "outcomes kraus_diagonal")
            self.assertEqual(item["outcomes"], list(outcome))
            diagonal = []
            for bits in itertools.product((0, 1), repeat=4):
                diagonal.append(
                    Fraction(all(x == 1 - 2 * bit for x, bit in zip(outcome, bits, strict=True)))
                )
            self.assertEqual(item["kraus_diagonal"], diagonal)
            self.assertEqual(sum(diagonal), 1)
            # Every permutation preserves each local projector factor, not
            # merely the trace of its selected state.
            for order in itertools.permutations(range(4)):
                permuted = []
                for bits in itertools.product((0, 1), repeat=4):
                    entry = Fraction(1)
                    for index in order:
                        entry *= Fraction(outcome[index] == 1 - 2 * bits[index])
                    permuted.append(entry)
                self.assertEqual(diagonal, permuted)
        self.assertEqual(
            [sum(item["kraus_diagonal"][i] for item in operators) for i in range(16)],
            [Fraction(1)] * 16,
        )

    def test_complete_profile_branch_laws_and_unnormalized_states(self):
        profiles = self.report["profiles"]
        self.assertEqual(len(profiles), len(self.protocol["profiles"]))
        outcome_vectors = list(itertools.product((-1, 1), repeat=4))
        for actual, fixture in zip(profiles, self.protocol["profiles"], strict=True):
            with self.subTest(profile=fixture["id"]):
                exact_keys(
                    self,
                    actual,
                    "id corners target naive_target rows mean variance swapped_mean "
                    "histogram_law reconstructed_corner_means",
                )
                corners = list(map(Fraction, fixture["corners"]))
                self.assertEqual(actual["id"], fixture["id"])
                self.assertEqual(actual["corners"], corners)
                self.assertEqual(len(actual["rows"]), 16)
                histogram = [Fraction(0)] * 5
                reconstructed = [Fraction(0)] * 4
                mean = second = swapped_mean = Fraction(0)
                marginal_density = [Fraction(0)] * 16
                for row, outcome, operator in zip(
                    actual["rows"], outcome_vectors, self.report["operators"], strict=True
                ):
                    exact_keys(
                        self,
                        row,
                        "outcomes probability state_diagonal estimate swapped_estimate relabeled_estimate",
                    )
                    probability = scalar_probability(corners, outcome)
                    estimate = scalar_estimate(self.weights, self.stations, outcome)
                    swapped = list(outcome)
                    swapped[0], swapped[3] = swapped[3], swapped[0]
                    wrong_estimate = scalar_estimate(self.weights, self.stations, swapped)
                    self.assertEqual(row["outcomes"], list(outcome))
                    self.assertEqual(row["probability"], probability)
                    self.assertEqual(
                        row["state_diagonal"],
                        [probability * entry for entry in operator["kraus_diagonal"]],
                    )
                    self.assertEqual(sum(row["state_diagonal"]), probability)
                    self.assertEqual(row["estimate"], estimate)
                    self.assertEqual(row["swapped_estimate"], wrong_estimate)
                    self.assertEqual(row["relabeled_estimate"], estimate)
                    histogram[outcome.count(1)] += probability
                    mean += probability * estimate
                    second += probability * estimate**2
                    swapped_mean += probability * wrong_estimate
                    for i, sign in enumerate(outcome):
                        reconstructed[i] += probability * sign
                    for i, entry in enumerate(row["state_diagonal"]):
                        marginal_density[i] += entry
                self.assertEqual(sum(histogram), 1)
                self.assertEqual(actual["histogram_law"], histogram)
                self.assertEqual(actual["reconstructed_corner_means"], reconstructed)
                self.assertEqual(reconstructed, corners)
                self.assertEqual(actual["mean"], mean)
                self.assertEqual(actual["variance"], second - mean**2)
                self.assertEqual(
                    actual["variance"],
                    sum(
                        self.weights[station] ** 2 * (1 - corners[i] ** 2)
                        for i, station in enumerate(self.stations)
                    ),
                )
                self.assertEqual(actual["swapped_mean"], swapped_mean)
                expected_density = [
                    scalar_probability(corners, tuple(1 - 2 * bit for bit in bits))
                    for bits in itertools.product((0, 1), repeat=4)
                ]
                self.assertEqual(marginal_density, expected_density)

    def test_independent_integrals_and_wrong_nodal_quadrature(self):
        mismatches = 0
        for actual, fixture in zip(self.report["profiles"], self.protocol["profiles"], strict=True):
            corners = list(map(Fraction, fixture["corners"]))
            target = direct_target(corners, self.stations)
            self.assertEqual(actual["target"], target)
            self.assertEqual(actual["mean"], target)
            naive = (
                sum(
                    corners[i] * (1 - int(station[0])) * (1 - int(station[1]))
                    for i, station in enumerate(self.stations)
                )
                / 4
            )
            self.assertEqual(actual["naive_target"], naive)
            mismatches += target != naive
        self.assertGreater(mismatches, 0)
        # Integrating the product is essential; R vanishes at station 11,
        # yet its bilinear basis contributes a strictly positive weight.
        self.assertGreater(self.weights["11"], 0)

    def test_deterministic_zero_branches_and_finite_record_not_exact(self):
        by_id = {profile["id"]: profile for profile in self.report["profiles"]}
        for name in ("plus", "minus", "corner00", "corner11"):
            profile = by_id[name]
            self.assertEqual(sum(row["probability"] > 0 for row in profile["rows"]), 1)
            self.assertEqual(profile["variance"], 0)
            self.assertEqual(sum(row["probability"] == 0 for row in profile["rows"]), 15)
            for row in profile["rows"]:
                if row["probability"] == 0:
                    self.assertEqual(row["state_diagonal"], [Fraction(0)] * 16)
        zero = by_id["zero"]
        self.assertGreater(zero["variance"], 0)
        self.assertTrue(any(row["estimate"] != zero["target"] for row in zero["rows"]))

    def test_histogram_collision_and_labeled_information(self):
        by_id = {profile["id"]: profile for profile in self.report["profiles"]}
        first, second = by_id["corner00"], by_id["corner11"]
        self.assertEqual(first["histogram_law"], second["histogram_law"])
        self.assertNotEqual(first["target"], second["target"])
        self.assertNotEqual(
            [row["probability"] for row in first["rows"]],
            [row["probability"] for row in second["rows"]],
        )
        self.assertEqual(first["swapped_mean"], second["target"])
        self.assertEqual(second["swapped_mean"], first["target"])

    def test_full_law_bubble_collision_and_distinct_interior_target(self):
        bubble = self.report["bubble"]
        exact_keys(self, bubble, "corners target probabilities state_diagonals")
        zero = next(profile for profile in self.report["profiles"] if profile["id"] == "zero")
        amplitude = Fraction(self.protocol["bubble"]["amplitude"])
        bubble_function = lambda u, v: (
            amplitude
            * sum(
                Fraction(coefficient) * u**i * v**j
                for i, j, coefficient in self.protocol["bubble"]["polynomial"]
            )
        )
        self.assertEqual(
            bubble["corners"],
            [bubble_function(Fraction(s[0]), Fraction(s[1])) for s in self.stations],
        )
        self.assertEqual(bubble["corners"], zero["corners"])
        self.assertEqual(bubble["probabilities"], [row["probability"] for row in zero["rows"]])
        self.assertEqual(bubble["state_diagonals"], [row["state_diagonal"] for row in zero["rows"]])
        self.assertEqual(
            bubble["target"], exact_simpson(lambda u, v: bubble_function(u, v) * (1 - u) * (1 - v))
        )
        self.assertGreater(bubble["target"], zero["target"])

    def test_fresh_and_unreset_two_shot_controls(self):
        repeat = self.report["repeat"]
        exact_keys(self, repeat, "rows fresh_mean unreset_mean fresh_variance unreset_variance")
        self.assertEqual(len(repeat["rows"]), 4)
        means = {"fresh": Fraction(0), "unreset": Fraction(0)}
        seconds = means.copy()
        masses = means.copy()
        marginals = {key: [Fraction(0), Fraction(0)] for key in means}
        for row, outcome in zip(repeat["rows"], itertools.product((-1, 1), repeat=2), strict=True):
            exact_keys(self, row, "outcomes fresh_probability unreset_probability")
            self.assertEqual(row["outcomes"], list(outcome))
            self.assertEqual(row["fresh_probability"], Fraction(1, 4))
            self.assertEqual(row["unreset_probability"], Fraction(outcome[0] == outcome[1], 2))
            statistic = Fraction(sum(outcome), 2)
            for mode in means:
                probability = row[mode + "_probability"]
                masses[mode] += probability
                means[mode] += probability * statistic
                seconds[mode] += probability * statistic**2
                for index, sign in enumerate(outcome):
                    marginals[mode][index] += probability * sign
        self.assertEqual(marginals["fresh"], marginals["unreset"])
        for mode, mean in means.items():
            self.assertEqual(masses[mode], 1)
            self.assertEqual(repeat[mode + "_mean"], mean)
            self.assertEqual(repeat[mode + "_variance"], seconds[mode] - mean**2)
        self.assertNotEqual(repeat["fresh_variance"], repeat["unreset_variance"])

    def test_calibration_entire_assignment_laws(self):
        self.assertEqual(len(self.report["calibrations"]), len(self.protocol["calibrations"]))
        by_id = {}
        for row, fixture in zip(
            self.report["calibrations"], self.protocol["calibrations"], strict=True
        ):
            exact_keys(
                self,
                row,
                "id true_mean alpha beta offset contrast assignments observed_law observed_mean corrected_mean",
            )
            mean, alpha, beta = (
                Fraction(fixture[key]) for key in ("polarization", "alpha", "beta")
            )
            self.assertEqual(row["id"], fixture["id"])
            self.assertEqual([row["true_mean"], row["alpha"], row["beta"]], [mean, alpha, beta])
            offset, contrast = beta - alpha, 1 - alpha - beta
            self.assertEqual([row["offset"], row["contrast"]], [offset, contrast])
            self.assertEqual(len(row["assignments"]), 4)
            registered_law = [Fraction(0), Fraction(0)]
            for assignment, (true, registered) in zip(
                row["assignments"], itertools.product((-1, 1), repeat=2), strict=True
            ):
                exact_keys(self, assignment, "true registered probability")
                channel = (
                    (1 - alpha if registered == 1 else alpha)
                    if true == 1
                    else (beta if registered == 1 else 1 - beta)
                )
                probability = (1 + true * mean) / 2 * channel
                self.assertEqual(
                    assignment, {"true": true, "registered": registered, "probability": probability}
                )
                registered_law[(registered + 1) // 2] += probability
            self.assertEqual(row["observed_law"], registered_law)
            self.assertEqual(sum(registered_law), 1)
            self.assertEqual(row["observed_mean"], registered_law[1] - registered_law[0])
            self.assertEqual(row["observed_mean"], offset + contrast * mean)
            self.assertEqual(row["corrected_mean"], mean if contrast else None)
            by_id[row["id"]] = row
        self.assertEqual(by_id["confound_a"]["observed_law"], by_id["confound_b"]["observed_law"])
        self.assertNotEqual(by_id["confound_a"]["true_mean"], by_id["confound_b"]["true_mean"])
        self.assertIsNone(by_id["blind"]["corrected_mean"])

    def test_separate_model_and_readout_error_identity(self):
        error = self.report["error"]
        exact_keys(
            self,
            error,
            "epsilon corner_errors field_target bound signed_error reconstruction_term field_envelope readout_envelope",
        )
        epsilon = Fraction(self.protocol["error_control"]["epsilon"])
        errors = list(map(Fraction, self.protocol["error_control"]["corner_errors"]))
        reconstruction = sum(
            self.weights[station] * value
            for station, value in zip(self.stations, errors, strict=True)
        )
        field_envelope = epsilon * exact_simpson(lambda u, v: (1 - u) * (1 - v))
        readout_envelope = sum(
            abs(self.weights[station] * value)
            for station, value in zip(self.stations, errors, strict=True)
        )
        self.assertEqual(error["epsilon"], epsilon)
        self.assertEqual(error["corner_errors"], errors)
        self.assertEqual(error["field_target"], self.report["bubble"]["target"])
        self.assertEqual(error["reconstruction_term"], reconstruction)
        self.assertEqual(error["signed_error"], reconstruction - error["field_target"])
        self.assertEqual(error["field_envelope"], field_envelope)
        self.assertEqual(error["readout_envelope"], readout_envelope)
        self.assertEqual(error["bound"], field_envelope + readout_envelope)
        self.assertLessEqual(abs(error["signed_error"]), error["bound"])

    def test_report_fraction_types_and_canonical_encoding(self):
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
                for index, (first, second) in enumerate(zip(raw, encoded, strict=True)):
                    visit(first, second, (*path, index))
            elif path[-1] == "id":
                self.assertIs(type(raw), str, path)
                self.assertIs(type(encoded), str)
                self.assertEqual(raw, encoded)
            elif (
                path == ("schedule_count",)
                or "outcomes" in path
                or path[-1] in ("true", "registered")
            ):
                self.assertIs(type(raw), int, path)
                self.assertIs(type(encoded), int)
                self.assertEqual(raw, encoded)
            elif path[-1] == "corrected_mean" and raw is None:
                self.assertIsNone(encoded)
            else:
                self.assertIs(type(raw), Fraction, path)
                self.assertIs(type(encoded), str)
                self.assertEqual(rational(encoded), raw)

        visit(self.report, wire)


class ProtocolTests(unittest.TestCase):
    def test_frozen_protocol_identity(self):
        self.assertEqual(
            hashlib.sha256((HERE / "protocol.json").read_bytes()).hexdigest(),
            PROTOCOL_SHA256,
        )

    def test_prespecified_finite_domain(self):
        protocol = read_protocol()
        self.assertEqual(protocol["study"], "QR-05BC")
        self.assertEqual(protocol["stations"], ["00", "10", "01", "11"])
        self.assertEqual(protocol["outcomes"], [-1, 1])
        self.assertEqual(protocol["shots_per_station"], 1)
        self.assertEqual(len(protocol["profiles"]), 6)
        self.assertEqual(len(protocol["calibrations"]), 4)
        self.assertEqual(protocol["repeat_control"]["shots"], 2)
        self.assertEqual(protocol["repeat_control"]["station"], "00")
        self.assertEqual(protocol["repeat_control"]["modes"], ["fresh", "unreset"])
        self.assertEqual(len(protocol["record_keys"]), 14)


def malformed_records(base, protocol):
    """Bounded independent refusals; no private-data oracle or file reads."""
    yield "missing station", copy.deepcopy(base[:-1])
    yield "extra station", copy.deepcopy(base + [base[0]])
    yield "tuple container", tuple(copy.deepcopy(base))
    yield "no records", None
    changed = copy.deepcopy(base)
    changed[-1] = copy.deepcopy(changed[0])
    yield "duplicate station and shot", changed
    for key in protocol["record_keys"]:
        changed = copy.deepcopy(base)
        del changed[-1][key]
        yield "missing " + key, changed
    for key in (
        "profile",
        "profile_id",
        "f",
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
        "shot_id": [True, 0, 2, "1", Fraction(1)],
        "station_id": ["unknown", 0, None],
        "attempted": [False, 1, "true", None],
        "available": [False, 1, "true", None],
        "status": ["nondetection", "postselected", "missing", True],
        "raw_registration_ref": ["packet:00:1", "private-profile", "", None],
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

    def setUp(self):
        self.records = self.study.make_records([-1, 1, -1, 1])
        self.weights = direct_weights(self.protocol["stations"])

    def test_record_constructor_and_public_context(self):
        for row, station, outcome in zip(
            self.records, self.protocol["stations"], (-1, 1, -1, 1), strict=True
        ):
            self.assertEqual(set(row), set(self.protocol["record_keys"]))
            for key, value in self.protocol["public_context"].items():
                self.assertEqual(row[key], value)
            self.assertEqual(row["station_id"], station)
            self.assertEqual(row["outcome"], outcome)
            self.assertIs(type(row["shot_id"]), int)
            self.assertEqual(row["shot_id"], 1)
            self.assertEqual(row["raw_registration_ref"], "packet:" + station + ":1")
            self.assertIs(row["attempted"], True)
            self.assertIs(row["available"], True)
            self.assertEqual(row["status"], "registered")
        for bad in (None, [], [-1] * 3, [-1] * 5, [True, 1, 1, 1], [1.0, 1, 1, 1], [0, 1, 1, 1]):
            with self.subTest(value=bad), self.assertRaises(ValueError):
                self.study.make_records(bad)

    def test_all_registered_estimates_and_record_orders(self):
        for profile in self.report["profiles"]:
            for row in profile["rows"]:
                records = self.study.make_records(row["outcomes"])
                snapshot = copy.deepcopy(records)
                expected = scalar_estimate(self.weights, self.protocol["stations"], row["outcomes"])
                self.assertEqual(self.study.estimate(records, self.weights), expected)
                self.assertEqual(expected, row["estimate"])
                for permutation in itertools.permutations(records):
                    self.assertEqual(self.study.estimate(list(permutation), self.weights), expected)
                self.assertEqual(records, snapshot)

    def test_decoder_does_not_consult_private_protocol_or_files(self):
        expected = scalar_estimate(self.weights, self.protocol["stations"], (-1, 1, -1, 1))
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
            self.assertEqual(self.study.estimate(self.records, self.weights), expected)

    def test_wrong_labels_and_joint_relabeling(self):
        outcomes = [-1, 1, -1, 1]
        answer = self.study.estimate(self.study.make_records(outcomes), self.weights)
        outcomes[0], outcomes[3] = outcomes[3], outcomes[0]
        changed = self.study.make_records(outcomes)
        self.assertNotEqual(self.study.estimate(changed, self.weights), answer)
        swapped_weights = dict(self.weights)
        swapped_weights["00"], swapped_weights["11"] = swapped_weights["11"], swapped_weights["00"]
        self.assertEqual(self.study.estimate(changed, swapped_weights), answer)

    def test_all_private_access_label_and_record_refusals(self):
        count = 0
        for name, bad in malformed_records(self.records, self.protocol):
            with self.subTest(case=name), self.assertRaises(ValueError):
                self.study.estimate(bad, self.weights)
            count += 1
        self.assertGreater(count, 60)

    def test_exact_container_scalar_and_weight_types(self):
        class ListSubclass(list):
            pass

        class DictSubclass(dict):
            pass

        class StringSubclass(str):
            pass

        class FractionSubclass(Fraction):
            pass

        bad_records = [ListSubclass(self.records)]
        changed = copy.deepcopy(self.records)
        changed[-1] = DictSubclass(changed[-1])
        bad_records.append(changed)
        changed = copy.deepcopy(self.records)
        changed[-1]["station_id"] = StringSubclass("11")
        bad_records.append(changed)
        changed = copy.deepcopy(self.records)
        changed[-1][StringSubclass("outcome")] = changed[-1].pop("outcome")
        bad_records.append(changed)
        for bad in bad_records:
            with self.subTest(kind=repr(bad)), self.assertRaises(ValueError):
                self.study.estimate(bad, self.weights)
        bad_weights = [None, [], list(self.weights.values()), DictSubclass(self.weights), {}]
        for value in (0, True, "1", 1.0, None, FractionSubclass(1)):
            changed = dict(self.weights)
            changed["11"] = value
            bad_weights.append(changed)
        changed = dict(self.weights)
        changed["unknown"] = changed.pop("11")
        bad_weights.append(changed)
        changed = dict(self.weights)
        changed[StringSubclass("11")] = changed.pop("11")
        bad_weights.append(changed)
        for bad in bad_weights:
            with self.subTest(weights=repr(bad)), self.assertRaises(ValueError):
                self.study.estimate(self.records, bad)

    def test_constructor_and_decoder_ownership(self):
        first = self.study.make_records([-1, 1, -1, 1])
        second = self.study.make_records([-1, 1, -1, 1])
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        for left, right in zip(first, second, strict=True):
            self.assertIsNot(left, right)
        snapshot = copy.deepcopy(self.weights)
        self.study.estimate(first, self.weights)
        self.assertEqual(self.weights, snapshot)
        first[0]["outcome"] = 1
        self.assertEqual(second[0]["outcome"], -1)

    def test_known_calibration_and_negative_contrast(self):
        for row in self.report["calibrations"]:
            if row["contrast"]:
                self.assertEqual(
                    self.study.invert_readout(
                        row["observed_mean"], offset=row["offset"], contrast=row["contrast"]
                    ),
                    row["true_mean"],
                )
        self.assertEqual(
            self.study.invert_readout(Fraction(1, 2), offset=Fraction(0), contrast=Fraction(-1)),
            Fraction(-1, 2),
        )
        # Inverting a finite record is not a physical-state certificate.
        self.assertGreater(
            self.study.invert_readout(Fraction(1), offset=Fraction(0), contrast=Fraction(1, 2)), 1
        )

    def test_unknown_blind_invalid_and_nonexact_calibration_refused(self):
        cases = [
            (Fraction(0), {}),
            (Fraction(0), {"offset": Fraction(0)}),
            (Fraction(0), {"contrast": Fraction(1)}),
            (Fraction(0), {"offset": Fraction(0), "contrast": Fraction(0)}),
            (Fraction(0), {"offset": Fraction(2), "contrast": Fraction(1)}),
            (Fraction(0), {"offset": Fraction(0), "contrast": Fraction(2)}),
            (Fraction(2), {"offset": Fraction(0), "contrast": Fraction(1)}),
        ]
        for bad in (0, True, 0.0, "0", None):
            cases.append((bad, {"offset": Fraction(0), "contrast": Fraction(1)}))
            cases.append((Fraction(0), {"offset": bad, "contrast": Fraction(1)}))
            cases.append((Fraction(0), {"offset": Fraction(0), "contrast": bad}))
        for mean, kwargs in cases:
            with self.subTest(mean=repr(mean), kwargs=repr(kwargs)), self.assertRaises(ValueError):
                self.study.invert_readout(mean, **kwargs)

    def test_complete_observer_analysis_and_canonical_public_results(self):
        with mock.patch.object(self.study, "compare_routes", return_value=self.report):
            result = self.study.analysis()
        exact_keys(self, result, "mathematics observer")
        self.assertEqual(result["mathematics"], self.study.encode(self.report))
        observer = result["observer"]
        exact_keys(
            self,
            observer,
            "estimates record_permutation_checks record_refusals calibration_checks unknown_calibration_refusals",
        )
        self.assertEqual(
            observer["estimates"],
            [
                {"profile": item["id"], "estimates": [str(row["estimate"]) for row in item["rows"]]}
                for item in self.report["profiles"]
            ],
        )
        self.assertEqual(observer["record_permutation_checks"], 6 * 16 * 24)
        self.assertEqual(len(observer["record_refusals"]), len(set(observer["record_refusals"])))
        self.assertTrue(all(type(name) is str and name for name in observer["record_refusals"]))
        self.assertTrue(
            {"missing_station", "extra_shot", "duplicate_station", "missing_outcome"}.issubset(
                observer["record_refusals"]
            )
        )
        self.assertTrue(
            {
                "private_" + key for key in ("profile", "f", "rho", "likelihood", "target", "seed")
            }.issubset(observer["record_refusals"])
        )
        self.assertEqual(observer["unknown_calibration_refusals"], 2)
        self.assertEqual(
            observer["calibration_checks"],
            [
                {
                    "id": row["id"],
                    "status": "known_channel_inverted"
                    if row["contrast"]
                    else "zero_contrast_refused",
                }
                for row in self.report["calibrations"]
            ],
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
        with tempfile.TemporaryDirectory(prefix="det8-qr05bc-loader-") as temporary:
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
    """Representative non-noop changes covering every retained report field."""
    numeric = [
        ("geometry", "volume"),
        ("geometry", "sigma"),
        ("geometry", "weights", 0),
        ("geometry", "weight_sum"),
        ("operators", 0, "kraus_diagonal", 0),
        ("profiles", 0, "corners", 0),
        ("profiles", 0, "target"),
        ("profiles", 0, "naive_target"),
        ("profiles", 0, "mean"),
        ("profiles", 0, "variance"),
        ("profiles", 0, "swapped_mean"),
        ("profiles", 0, "histogram_law", 0),
        ("profiles", 0, "reconstructed_corner_means", 0),
        ("bubble", "corners", 0),
        ("bubble", "target"),
        ("bubble", "probabilities", 0),
        ("bubble", "state_diagonals", 0, 0),
    ]
    numeric.extend(
        ("profiles", -1, "rows", -1, key)
        for key in ("probability", "estimate", "swapped_estimate", "relabeled_estimate")
    )
    numeric.append(("profiles", -1, "rows", -1, "state_diagonal", 0))
    numeric.extend(
        ("repeat", key)
        for key in ("fresh_mean", "unreset_mean", "fresh_variance", "unreset_variance")
    )
    numeric.extend(
        ("repeat", "rows", -1, key) for key in ("fresh_probability", "unreset_probability")
    )
    numeric.extend(
        ("calibrations", 0, key)
        for key in (
            "true_mean",
            "alpha",
            "beta",
            "offset",
            "contrast",
            "observed_mean",
            "corrected_mean",
        )
    )
    numeric.extend(
        (
            ("calibrations", 0, "assignments", -1, "probability"),
            ("calibrations", 0, "observed_law", 0),
        )
    )
    numeric.extend(
        ("error", key)
        for key in (
            "epsilon",
            "field_target",
            "bound",
            "signed_error",
            "reconstruction_term",
            "field_envelope",
            "readout_envelope",
        )
    )
    numeric.append(("error", "corner_errors", 0))
    for path in numeric:
        changed = copy.deepcopy(original)
        full = ("mathematics", *path)
        set_path(changed, full, str(Fraction(get_path(original, full)) + 1))
        yield "numeric " + repr(path), changed
    replacements = [
        (("mathematics", "schedule_count"), 0),
        (("mathematics", "schedule_discrepancies"), ["unreported mismatch"]),
        (("mathematics", "operators", 0, "outcomes", 0), 1),
        (("mathematics", "profiles", 0, "id"), "changed"),
        (("mathematics", "profiles", -1, "rows", -1, "outcomes", 0), -1),
        (("mathematics", "repeat", "rows", 0, "outcomes", 0), 1),
        (("mathematics", "calibrations", 0, "id"), "changed"),
        (("mathematics", "calibrations", 0, "assignments", 0, "true"), 1),
        (("mathematics", "calibrations", 0, "assignments", 0, "registered"), 1),
        (("mathematics", "calibrations", -1, "corrected_mean"), "0"),
        (("observer", "estimates", 0, "profile"), "changed"),
        (("observer", "estimates", 0, "estimates", 0), "999"),
        (("observer", "record_permutation_checks"), True),
        (("observer", "record_refusals"), []),
        (("observer", "calibration_checks", 0, "id"), "changed"),
        (("observer", "calibration_checks", 0, "status"), "changed"),
        (("observer", "unknown_calibration_refusals"), False),
    ]
    for path, replacement in replacements:
        changed = copy.deepcopy(original)
        set_path(changed, path, replacement)
        yield "field " + repr(path), changed
    for key in ("mathematics", "observer"):
        changed = copy.deepcopy(original)
        del changed[key]
        yield "missing " + key, changed
    changed = copy.deepcopy(original)
    changed["private"] = "hidden"
    yield "unexpected field", changed


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_module("study")
        self.directory = tempfile.TemporaryDirectory(prefix="det8-qr05bc-test-")
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
        self.assertEqual(evidence["schema"], "QR-05BC-evidence-v1")
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
            mutations = list(analysis_mutations(expected))
            self.assertGreater(len(mutations), 50)
            for index, (name, changed) in enumerate(mutations):
                with self.subTest(case=name):
                    self.assertNotEqual(
                        self.study.canonical(changed), self.study.canonical(expected)
                    )
                    bad = copy.deepcopy(evidence)
                    bad["analysis"] = changed
                    path = self.root / ("report-mutation-" + str(index) + ".json")
                    self.write_json(path, bad)
                    before = path.read_bytes()
                    with self.assertRaises(ValueError):
                        self.study.replay(path, self.freeze)
                    self.assertEqual(path.read_bytes(), before)

    def test_encoding_rejects_unsupported_native_types(self):
        for value in (0.0, float("nan"), float("inf"), (), {1: "bad"}, {"set": {1}}, b"bytes"):
            with self.subTest(value=repr(value)), self.assertRaises(ValueError):
                self.study.encode(value)
        self.assertFalse(self.study.same({"integer": 1}, {"integer": True}))
        self.assertEqual(self.study.encode(Fraction(2, 6)), "1/3")


class SourceIdentityTests(unittest.TestCase):
    def test_exact_eight_current_and_bb_source_identities(self):
        study = load_module("study")
        identities = study.source_identities()
        expected = [
            HERE / name
            for name in (
                "README.md",
                "protocol.json",
                "quantum.py",
                "reference.py",
                "study.py",
                "test_qr05bc.py",
            )
        ]
        expected += [
            HERE.parent / "qr-05bb-operational-bridge-design-2026-09-08" / name
            for name in ("README.md", "RESULTS.md")
        ]
        self.assertEqual(len(identities), 8)
        self.assertEqual(set(identities), {str(path.relative_to(study.REPO)) for path in expected})
        for path in expected:
            data = path.read_bytes()
            self.assertEqual(
                identities[str(path.relative_to(study.REPO))],
                {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()},
            )
        frozen = study.read_json(study.FREEZE_PATH)
        self.assertEqual(frozen["sources"], identities)

    def test_protocol_identity_is_checked_before_parsing(self):
        study = load_module("study")
        with (
            mock.patch.object(study, "identity", return_value={"bytes": 1, "sha256": "0" * 64}),
            mock.patch.object(
                study, "read_json", side_effect=AssertionError("parsed unpinned protocol")
            ),
            self.assertRaises(ValueError),
        ):
            study.load_protocol()


if __name__ == "__main__":
    unittest.main()
