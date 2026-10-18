"""Focused source-bound BN tests with endpoint/forward-substitution oracle.

Only the new driver is lazily loaded. No fixture, engine, or oracle executes
at import; numerical work remains held until the first source-bound release.
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
    spec = importlib.util.spec_from_file_location("_qr05bn_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("BN driver cannot be loaded")
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
        for key in wanted:
            exact_tree(test, actual[key], wanted[key], path + "." + key)
    elif type(wanted) is list:
        test.assertEqual(len(actual), len(wanted), path)
        for index, (a, b) in enumerate(zip(actual, wanted, strict=True)):
            exact_tree(test, a, b, path + "[" + str(index) + "]")
    else:
        test.assertEqual(actual, wanted, path)


def moment(bounds, degree):
    a, b, c, d = bounds
    return (
        (b ** (degree + 1) - a ** (degree + 1))
        * (d ** (degree + 1) - c ** (degree + 1))
        / (degree + 1) ** 2
    )


def mass(bounds, eta, scale, delta):
    return (
        scale
        / 2
        * (moment(bounds, 0) + (eta + delta) * moment(bounds, 1) + eta * delta * moment(bounds, 2))
    )


def geometry_oracle(item, protocol):
    eta, scale = Fraction(item["eta"]), Fraction(item["scale"])
    domains = {
        name: [Fraction(*value) for value in bounds] for name, bounds in protocol["regions"].items()
    }
    coeffs = {
        name: [
            mass(bounds, eta, scale, Fraction(0)),
            scale / 2 * (moment(bounds, 1) + eta * moment(bounds, 2)),
        ]
        for name, bounds in domains.items()
    }
    a, b = coeffs["I"]
    c, d = coeffs["Q"]
    ranges = []
    for bound in protocol["density_bounds"]:
        low, high = [Fraction(*value) for value in bound["interval"]]
        ranges.append(
            {
                "bound": bound["id"],
                "delta": [low, high],
                "q": [(a + b * high) / (c + d * high), (a + b * low) / (c + d * low)],
            }
        )
    return {
        "id": item["id"],
        "eta": item["eta"],
        "scale": item["scale"],
        "volume_Q": c,
        "volume_I": a,
        "target": a / c,
        "mass_I_coeffs": [a, b],
        "mass_Q_coeffs": [c, d],
        "derivative_numerator": b * c - a * d,
        "ranges": ranges,
    }


def hypothesis(geometry, bound_index, q, protocol):
    a, b = geometry["mass_I_coeffs"]
    c, d = geometry["mass_Q_coeffs"]
    numerator, denominator = a - q * c, q * d - b
    candidate = [numerator / denominator] if denominator else []
    interval = geometry["ranges"][bound_index]
    # Range admission is independently necessary/sufficient by strict monotonicity;
    # substitute the recovered value back into freshly integrated mass formulas.
    feasible = interval["q"][0] <= q <= interval["q"][1]
    normalized, mass_q, mass_i, admitted = [], [], [], []
    if feasible:
        if not candidate or not interval["delta"][0] <= candidate[0] <= interval["delta"][1]:
            raise ValueError("independent range/inverse contradiction")
        delta = candidate[0]
        eta, scale = Fraction(geometry["eta"]), Fraction(geometry["scale"])
        domains = {
            name: [Fraction(*value) for value in bounds]
            for name, bounds in protocol["regions"].items()
        }
        mass_q = [mass(domains["Q"], eta, scale, delta)]
        mass_i = [mass(domains["I"], eta, scale, delta)]
        if mass_i[0] / mass_q[0] != q:
            raise ValueError("independent inverse fails forward substitution")
        admitted = [delta]
        normalized = [
            [degree, degree, value / mass_q[0]]
            for degree, value in enumerate(
                (scale / 2, scale * (eta + delta) / 2, scale * eta * delta / 2)
            )
            if value
        ]
    return {
        "id": geometry["id"],
        "q_range": interval["q"],
        "inverse_numerator": numerator,
        "inverse_denominator": denominator,
        "candidate": candidate,
        "delta_set": admitted,
        "status": "feasible" if feasible else "infeasible",
        "normalized_point": normalized,
        "mass_Q": mass_q,
        "mass_I": mass_i,
    }


def word_law(q, quota):
    return [
        {"y": list(y), "k": sum(y), "p": q ** sum(y) * (1 - q) ** (quota - sum(y))}
        for y in itertools.product((0, 1), repeat=quota)
    ]


def point_classes(rows, geometries):
    grouped, polynomials = [], []
    for row in rows:
        if not row["delta_set"]:
            continue
        polynomial = row["normalized_point"]
        if polynomial not in polynomials:
            polynomials.append(polynomial)
            grouped.append([])
        grouped[polynomials.index(polynomial)].append(row["id"])
    targets = {geometry["id"]: geometry["target"] for geometry in geometries}
    return [
        {
            "worlds": ids,
            "targets": sorted({targets[name] for name in ids}),
            "identified": len({targets[name] for name in ids}) == 1,
        }
        for ids in grouped
    ]


def expected(protocol):
    geometries = [geometry_oracle(item, protocol) for item in protocol["geometries"]]
    by_geometry = {row["id"]: row for row in geometries}
    cases = []
    for bound_index, bound in enumerate(protocol["density_bounds"]):
        for data in protocol["population_data"]:
            q = Fraction(*data["q"])
            rows = [hypothesis(geometry, bound_index, q, protocol) for geometry in geometries]
            worlds = [row["id"] for row in rows if row["delta_set"]]
            targets = sorted({by_geometry[name]["target"] for name in worlds})
            cases.append(
                {
                    "id": bound["id"] + "/" + data["id"],
                    "bound": bound["id"],
                    "data": data["id"],
                    "q": q,
                    "hypotheses": rows,
                    "worlds": worlds,
                    "targets": targets,
                    "status": "infeasible"
                    if not targets
                    else "identified"
                    if len(targets) == 1
                    else "ambiguous",
                    "point_classes": point_classes(rows, geometries),
                }
            )
    by_case = {row["id"]: row for row in cases}
    laws = [
        {
            "data": data["id"],
            "q": Fraction(*data["q"]),
            "rows": word_law(Fraction(*data["q"]), protocol["quota"]),
        }
        for data in protocol["population_data"]
    ]
    monotonicity = []
    for tight, broad in itertools.pairwise(protocol["density_bounds"]):
        for data in protocol["population_data"]:
            left = by_case[tight["id"] + "/" + data["id"]]
            right = by_case[broad["id"] + "/" + data["id"]]
            delta = {row["id"]: row["delta_set"] for row in right["hypotheses"]}
            monotonicity.append(
                {
                    "tight": tight["id"],
                    "broad": broad["id"],
                    "data": data["id"],
                    "world_subset": set(left["worlds"]).issubset(right["worlds"]),
                    "target_subset": set(left["targets"]).issubset(right["targets"]),
                    "nuisance_preserved": all(
                        row["delta_set"] == delta[row["id"]]
                        for row in left["hypotheses"]
                        if row["delta_set"]
                    ),
                }
            )
    finite = []
    for index, bound in enumerate(protocol["density_bounds"]):
        strict = all(
            0 < row["ranges"][index]["q"][0] <= row["ranges"][index]["q"][1] < 1
            for row in geometries
        )
        finite.append(
            {
                "bound": bound["id"],
                "strict_support": strict,
                "rows": [
                    {
                        "y": list(y),
                        "k": sum(y),
                        "frequency": Fraction(sum(y), protocol["quota"]),
                        "worlds": [row["id"] for row in geometries],
                        "targets": sorted({row["target"] for row in geometries}),
                    }
                    for y in itertools.product((0, 1), repeat=protocol["quota"])
                ],
            }
        )
    collisions = []
    for name, data_id in (("inherited_whole_point", "overlap"), ("membership_only", "interior")):
        case = by_case[protocol["density_bounds"][-1]["id"] + "/" + data_id]
        left, right = [
            next(row for row in case["hypotheses"] if row["id"] == name)
            for name in ("flat", "conformal")
        ]
        left_law = word_law(left["mass_I"][0] / left["mass_Q"][0], protocol["quota"])
        right_law = word_law(right["mass_I"][0] / right["mass_Q"][0], protocol["quota"])
        collisions.append(
            {
                "id": name,
                "case": case["id"],
                "worlds": ["flat", "conformal"],
                "deltas": [left["delta_set"][0], right["delta_set"][0]],
                "target_gap": by_geometry["flat"]["target"] - by_geometry["conformal"]["target"],
                "membership_equal": left_law == right_law,
                "point_equal": left["normalized_point"] == right["normalized_point"],
            }
        )
    scale_pairs = []
    for first, second in (("flat", "flat_x4"), ("conformal", "conformal_x4")):
        pairs = [
            tuple(
                next(row for row in case["hypotheses"] if row["id"] == name)
                for name in (first, second)
            )
            for case in cases
        ]
        scale_pairs.append(
            {
                "worlds": [first, second],
                "volume_factor": by_geometry[second]["volume_Q"] / by_geometry[first]["volume_Q"],
                "target_equal": by_geometry[first]["target"] == by_geometry[second]["target"],
                "nuisance_sets_equal": all(a["delta_set"] == b["delta_set"] for a, b in pairs),
                "point_laws_equal": all(
                    a["normalized_point"] == b["normalized_point"] for a, b in pairs
                ),
            }
        )
    return {
        "schema": "qr05bn-report-v1",
        "geometries": geometries,
        "cases": cases,
        "laws": laws,
        "monotonicity": monotonicity,
        "finite_records": finite,
        "collisions": collisions,
        "scale_pairs": scale_pairs,
    }


def query(data, bound):
    return {
        "schema": "qr05bn-query-v1",
        "data_kind": "population_probability",
        "q": list(data),
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
        cls.cases = {case["id"]: case for case in cls.report["cases"]}

    def test_entire_independent_native_report_and_fixed_coverage(self):
        exact_tree(self, self.report, expected(self.protocol))
        self.assertEqual(len(self.report["geometries"]), 4)
        self.assertEqual(len(self.report["cases"]), 36)
        self.assertEqual(sum(len(case["hypotheses"]) for case in self.report["cases"]), 144)
        self.assertEqual(sum(len(law["rows"]) for law in self.report["laws"]), 144)
        self.assertEqual(len(self.report["monotonicity"]), 27)
        self.assertEqual(sum(len(group["rows"]) for group in self.report["finite_records"]), 64)
        self.assertEqual(len(self.report["collisions"]), 2)
        self.assertEqual(len(self.report["scale_pairs"]), 2)

    def test_endpoint_mass_coefficients_and_strict_monotone_forward_ranges(self):
        for row in self.report["geometries"]:
            eta, scale = Fraction(row["eta"]), Fraction(row["scale"])
            factor = scale / 1152
            self.assertEqual(row["mass_I_coeffs"], [factor * (144 + 9 * eta), factor * (9 + eta)])
            self.assertEqual(
                row["mass_Q_coeffs"], [factor * (576 + 144 * eta), factor * (144 + 64 * eta)]
            )
            self.assertEqual(
                row["derivative_numerator"], factor**2 * (-432 * (eta**2 + 20 * eta + 36))
            )
            self.assertLess(row["derivative_numerator"], 0)
            a, b = row["mass_I_coeffs"]
            c, d = row["mass_Q_coeffs"]
            for interval in row["ranges"]:
                low, high = interval["delta"]
                self.assertGreater(c + d * low, 0)
                self.assertGreater(c + d * high, 0)
                self.assertEqual(
                    interval["q"], [(a + b * high) / (c + d * high), (a + b * low) / (c + d * low)]
                )
                self.assertGreater(interval["q"][0], 0)
                self.assertLess(interval["q"][1], 1)
            self.assertEqual(row["ranges"][0]["q"][0], row["ranges"][0]["q"][1])

    def test_closed_boundaries_poles_and_rejected_candidates_remain_visible(self):
        for bound in self.protocol["density_bounds"]:
            for name, geometry_ids in (
                ("flat_pole", ("flat", "flat_x4")),
                ("conformal_pole", ("conformal", "conformal_x4")),
            ):
                case = self.cases[bound["id"] + "/" + name]
                for row in case["hypotheses"]:
                    if row["id"] in geometry_ids:
                        self.assertEqual(row["inverse_denominator"], Fraction(0))
                        self.assertNotEqual(row["inverse_numerator"], 0)
                        self.assertEqual(row["candidate"], [])
                        self.assertEqual(row["delta_set"], [])
                        self.assertEqual(row["normalized_point"], [])
                        self.assertEqual(row["mass_I"], [])
                        self.assertEqual(row["mass_Q"], [])
        for data, ids in (
            ("flat_edge", ("flat", "flat_x4")),
            ("lower_edge", ("conformal", "conformal_x4")),
        ):
            wide = self.cases["two/" + data]
            narrow = self.cases["one/" + data]
            for name in ids:
                accepted = next(row for row in wide["hypotheses"] if row["id"] == name)
                refused = next(row for row in narrow["hypotheses"] if row["id"] == name)
                self.assertEqual(accepted["delta_set"], [Fraction(2)])
                self.assertEqual(refused["candidate"], [Fraction(2)])
                self.assertEqual(refused["delta_set"], [])
        for case in self.report["cases"]:
            for row in case["hypotheses"]:
                if row["candidate"]:
                    self.assertEqual(
                        row["candidate"][0] * row["inverse_denominator"], row["inverse_numerator"]
                    )
                if row["delta_set"]:
                    self.assertEqual(row["mass_I"][0] / row["mass_Q"][0], case["q"])
                    self.assertEqual(row["status"], "feasible")
                else:
                    self.assertEqual(row["status"], "infeasible")

    def test_bound_inclusions_preserve_labels_and_nuisance_without_fitting(self):
        for row in self.report["monotonicity"]:
            self.assertIs(row["world_subset"], True)
            self.assertIs(row["target_subset"], True)
            self.assertIs(row["nuisance_preserved"], True)
            left, right = [self.cases[row[name] + "/" + row["data"]] for name in ("tight", "broad")]
            self.assertTrue(set(left["worlds"]).issubset(right["worlds"]))
            self.assertTrue(set(left["targets"]).issubset(right["targets"]))
            deltas = {candidate["id"]: candidate["delta_set"] for candidate in right["hypotheses"]}
            for candidate in left["hypotheses"]:
                if candidate["delta_set"]:
                    self.assertEqual(candidate["delta_set"], deltas[candidate["id"]])
        for case in self.report["cases"]:
            self.assertEqual(case["targets"], sorted(set(case["targets"])))
            self.assertTrue(set(case["targets"]).issubset({Fraction(17, 80), Fraction(1, 4)}))
            self.assertEqual(
                case["status"],
                "infeasible"
                if not case["targets"]
                else "identified"
                if len(case["targets"]) == 1
                else "ambiguous",
            )
        for pair in self.report["scale_pairs"]:
            self.assertEqual(pair["volume_factor"], Fraction(4))
            for name in ("target_equal", "nuisance_sets_equal", "point_laws_equal"):
                self.assertIs(pair[name], True)

    def test_point_law_collision_is_stronger_than_membership_collision(self):
        whole, membership = self.report["collisions"]
        self.assertEqual(whole["deltas"], [Fraction(1), Fraction(0)])
        self.assertEqual(membership["deltas"], [Fraction(16, 11), Fraction(45, 158)])
        self.assertIs(whole["point_equal"], True)
        self.assertIs(membership["point_equal"], False)
        for collision in (whole, membership):
            self.assertIs(collision["membership_equal"], True)
            self.assertEqual(collision["target_gap"], Fraction(3, 80))
        case = self.cases[membership["case"]]
        flat = next(row for row in case["hypotheses"] if row["id"] == "flat")
        conformal = next(row for row in case["hypotheses"] if row["id"] == "conformal")
        self.assertFalse(any(i == j == 2 for i, j, _ in flat["normalized_point"]))
        self.assertTrue(
            any(i == j == 2 and value != 0 for i, j, value in conformal["normalized_point"])
        )
        self.assertEqual(
            [[row["worlds"], row["targets"]] for row in case["point_classes"]],
            [
                [["flat", "flat_x4"], [Fraction(1, 4)]],
                [["conformal", "conformal_x4"], [Fraction(17, 80)]],
            ],
        )

    def test_data_laws_keep_zero_rows_but_finite_word_support_does_not_invert_frequency(self):
        for law in self.report["laws"]:
            self.assertEqual(sum(row["p"] for row in law["rows"]), 1)
            self.assertEqual(
                [row["y"] for row in law["rows"]],
                [list(y) for y in itertools.product((0, 1), repeat=4)],
            )
            if law["q"] in (Fraction(0), Fraction(1)):
                self.assertEqual(sum(row["p"] == 0 for row in law["rows"]), 15)
        ids = [row["id"] for row in self.report["geometries"]]
        for group in self.report["finite_records"]:
            self.assertIs(group["strict_support"], True)
            for row in group["rows"]:
                self.assertEqual(row["worlds"], ids)
                self.assertEqual(row["frequency"], Fraction(row["k"], 4))
            for name in ("zero", "one"):
                exact = self.cases[group["bound"] + "/" + name]
                self.assertEqual(exact["worlds"], [])
                self.assertEqual(exact["status"], "infeasible")


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_all_registered_queries_and_detached_response(self):
        _study, protocol, report = evaluated()
        cases = {case["id"]: case for case in report["cases"]}
        for bound in protocol["density_bounds"]:
            for data in protocol["population_data"]:
                supplied = query(data["q"], bound["id"])
                saved = copy.deepcopy(supplied)
                wanted = query_answer(cases[bound["id"] + "/" + data["id"]])
                returned = self.study.identify(supplied)
                exact_tree(self, returned, wanted)
                self.assertEqual(supplied, saved)
                returned["worlds"].append("changed")
                returned["targets"].append(Fraction(99))
                if returned["nuisance"]:
                    returned["nuisance"][0]["delta"] = Fraction(99)
                exact_tree(self, self.study.identify(supplied), wanted)
                supplied["q"][0] = 999
                self.assertEqual(saved["q"], data["q"])

    def test_strict_query_mode_rationals_bound_and_private_fields(self):
        class DictChild(dict):
            pass

        class ListChild(list):
            pass

        class IntChild(int):
            pass

        class StringChild(str):
            pass

        base = query([1, 4], "two")
        changes = [None, [], (), DictChild(base), {StringChild(k): v for k, v in base.items()}]
        for key in base:
            changed = copy.deepcopy(base)
            del changed[key]
            changes.append(changed)
        for key, value in [
            ("schema", "qr05bm-v1"),
            ("data_kind", "sample_frequency"),
            ("bound_basis", "estimated_from_packet"),
            ("density_bound", "three"),
            ("density_bound", [0, 2]),
            ("schema", StringChild(base["schema"])),
            ("data_kind", True),
            ("density_bound", StringChild("two")),
            ("bound_basis", StringChild(base["bound_basis"])),
        ]:
            changed = copy.deepcopy(base)
            changed[key] = value
            changes.append(changed)
        for value in [
            Fraction(1, 4),
            [2, 8],
            [0, 2],
            [1, -4],
            [1, 0],
            [True, 4],
            [1, True],
            [1.0, 4],
            ["1", 4],
            [IntChild(1), 4],
            ListChild([1, 4]),
            (1, 4),
            [],
            [1],
            [1, 4, 0],
            [1, 3],
            [-1, 4],
            [5, 4],
            float("nan"),
        ]:
            changed = copy.deepcopy(base)
            changed["q"] = value
            changes.append(changed)
        for key in (
            "records",
            "quota",
            "count",
            "frequency",
            "actual_world",
            "eta",
            "delta",
            "target",
            "probability",
            "state",
            "coordinates",
            "extra",
        ):
            changed = copy.deepcopy(base)
            changed[key] = 0
            changes.append(changed)
        for index, changed in enumerate(changes):
            with self.subTest(case=index), self.assertRaises(ValueError):
                self.study.identify(changed)

    def test_query_needs_no_producer_file_or_old_wrapper_and_valid_empty_is_not_refusal(self):
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
            mock.patch.object(
                self.study.UTILITY, "analyze", side_effect=AssertionError("old analysis")
            ),
            mock.patch.object(
                self.study.UTILITY, "estimate", side_effect=AssertionError("old estimator")
            ),
            mock.patch.object(
                self.study.UTILITY,
                "read_bounded",
                side_effect=AssertionError("utility file access"),
            ),
        ):
            for data in ([0, 1], [1, 1]):
                result = self.study.identify(query(data, "two"))
                exact_tree(
                    self,
                    result,
                    {"worlds": [], "targets": [], "status": "infeasible", "nuisance": []},
                )
            result = self.study.identify(query([1, 4], "uniform"))
            self.assertEqual(result["worlds"], ["flat", "flat_x4"])


def fixture_snapshot(study):
    """New synthetic engine blobs; authentic protocol and utility identities only."""
    snapshot = {name: ("synthetic:" + name).encode() for name in study.SOURCE_PATHS}
    snapshot["protocol.json"] = (HERE / "protocol.json").read_bytes()
    snapshot[study.UTILITY_SOURCE] = study.UTILITY_BYTES
    snapshot["primary.py"] = b"primary synthetic source"
    snapshot["reference.py"] = b"reference synthetic source"
    return snapshot


def replace_path(value, path, replacement):
    changed = copy.deepcopy(value)
    current = changed
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement
    return changed


def report_mutations(report):
    """Bounded non-noop witnesses across every retained top-level collection."""
    paths = [
        (["schema"], "wrong"),
        (["geometries", 0, "volume_Q"], Fraction(99)),
        (["geometries", 1, "mass_I_coeffs", 1], Fraction(99)),
        (["geometries", 3, "ranges", 3, "q", 0], Fraction(99)),
        (["geometries", 0, "eta"], False),
        (["cases", 0, "q"], 0),
        (["cases", 0, "hypotheses", 0, "candidate"], []),
        (["cases", 0, "hypotheses", 0, "status"], "feasible"),
        (["cases", -1, "targets"], [Fraction(1)]),
        (["laws", 0, "rows", 0, "p"], 1),
        (["laws", -1, "rows", -1, "y", 0], True),
        (["monotonicity", -1, "world_subset"], False),
        (["finite_records", -1, "rows", -1, "frequency"], 1),
        (["finite_records", 0, "rows", 0, "worlds"], []),
        (["collisions", -1, "point_equal"], True),
        (["scale_pairs", -1, "volume_factor"], Fraction(3)),
    ]
    for path, replacement in paths:
        yield replace_path(report, path, replacement)
    feasible_index = next(
        index for index, case in enumerate(report["cases"]) if case["point_classes"]
    )
    yield replace_path(report, ["cases", feasible_index, "point_classes", 0, "identified"], "yes")
    hypothesis_index = next(
        index
        for index, row in enumerate(report["cases"][feasible_index]["hypotheses"])
        if row["delta_set"]
    )
    yield replace_path(
        report, ["cases", feasible_index, "hypotheses", hypothesis_index, "normalized_point"], []
    )


class UtilityBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_pinned_fresh_utility_aliases_keep_isolated_globals_and_nine_sources(self):
        study, other = self.study, load_study()
        self.assertIsNot(study.UTILITY, other.UTILITY)
        self.assertEqual(study.UTILITY_BYTES, other.UTILITY_BYTES)
        self.assertEqual(hashlib.sha256(study.UTILITY_BYTES).hexdigest(), study.UTILITY_SHA256)
        self.assertEqual(study.ROOT, HERE)
        self.assertEqual(study.UTILITY.ROOT, study.UTILITY_PATH.resolve().parent)
        self.assertNotEqual(study.UTILITY.ROOT, study.ROOT)
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
        self.assertEqual(set(snapshot), set(study.SOURCE_PATHS))
        self.assertEqual(len(snapshot), 9)
        self.assertEqual(len({str((HERE / name).resolve()) for name in snapshot}), 9)
        self.assertNotIn("results.json", snapshot)
        self.assertEqual(snapshot[study.UTILITY_SOURCE], study.UTILITY_BYTES)
        for name, data in snapshot.items():
            self.assertLessEqual(len(data), study.SOURCE_LIMIT)
            self.assertEqual(
                study.identities(snapshot)[name],
                {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()},
            )
        self.assertEqual(
            hashlib.sha256(snapshot["protocol.json"]).hexdigest(), study.PROTOCOL_SHA256
        )

    def test_utility_authentication_precedes_execution_and_snapshot_rebinding(self):
        study = self.study
        with tempfile.TemporaryDirectory(prefix="qr05bn-utility-") as directory:
            path = Path(directory) / "utility.py"
            path.write_bytes(b"raise AssertionError('unauthenticated execution')\n")
            with self.assertRaises(ValueError):
                study._load_utilities(path)
            path.write_bytes(study.UTILITY_BYTES)
            blob, module = study._load_utilities(path)
            self.assertEqual(blob, study.UTILITY_BYTES)
            self.assertIsNot(module, study.UTILITY)
            path.write_bytes(study.UTILITY_BYTES + b"\n")
            with self.assertRaises(ValueError):
                study._load_utilities(path)
            link = Path(directory) / "symlink.py"
            link.symlink_to(path)
            with self.assertRaises(ValueError):
                study._load_utilities(link)
        original = study.read_bounded

        def altered(path, *args):
            if Path(path).resolve() == study.UTILITY_PATH.resolve():
                return study.UTILITY_BYTES + b"\n"
            return original(path, *args)

        with (
            mock.patch.object(study, "read_bounded", side_effect=altered),
            self.assertRaises(ValueError),
        ):
            study.source_snapshot()
        snapshot = fixture_snapshot(study)
        snapshot[study.UTILITY_SOURCE] += b"\n"
        with (
            mock.patch.object(
                study, "strict_loads", side_effect=AssertionError("parsed before utility check")
            ),
            self.assertRaises(ValueError),
        ):
            study._protocol(snapshot)

    def test_exact_codec_and_native_comparison_integrate_without_null_or_type_coercion(self):
        study = self.study
        native = {
            "rational": Fraction(-2, 3),
            "zero": Fraction(0),
            "integer": 1,
            "flag": True,
            "empty": [],
        }
        encoded = study.encode(native)
        exact_tree(self, study.decode(study.strict_loads(study.canonical(encoded))), native)
        self.assertEqual(encoded["rational"], {"$fraction": [-2, 3]})
        self.assertEqual(encoded["zero"], {"$fraction": [0, 1]})
        for value in (
            None,
            1.0,
            (1,),
            {"$unknown": 1},
            {"$fraction": [2, 6]},
            {"$fraction": [0, 2]},
            {"$fraction": [True, 1]},
            {"$fraction": [1, 0]},
            {"$fraction": [1, -2]},
            {"$fraction": [1, 2], "extra": 0},
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                study.decode(value)
        for value in (None, 1.0, (1,), {"$fraction": [1, 2]}):
            with self.subTest(native=value), self.assertRaises(ValueError):
                study.encode(value)
        for value in (None, 1.0, Fraction(1), (1,)):
            with self.subTest(canonical=value), self.assertRaises(ValueError):
                study.canonical(value)
        for left, right in ((True, 1), (Fraction(1), 1), ([], ()), ({"a": 1}, {"a": 1, "b": 0})):
            with self.subTest(types=(type(left), type(right))), self.assertRaises(ValueError):
                study.require_equal(left, right)
        for blob in (b'{"a":1,"a":2}', b'{"a":1.0}', b'{"a":NaN}', b'{"a":Infinity}', b"\xff"):
            with self.subTest(blob=blob), self.assertRaises(ValueError):
                study.strict_loads(blob)

    def test_read_caps_regular_files_and_alias_limit_globals(self):
        study = self.study
        with tempfile.TemporaryDirectory(prefix="qr05bn-read-") as directory:
            path = Path(directory) / "small"
            path.write_bytes(b"1234")
            self.assertEqual(study.read_bounded(path, 4), b"1234")
            for limit in (3, 0, -1, True, 4.0, study.ARTIFACT_LIMIT + 1):
                with self.subTest(limit=limit), self.assertRaises(ValueError):
                    study.read_bounded(path, limit)
            with mock.patch.object(study, "ARTIFACT_LIMIT", 1):
                self.assertEqual(study.read_bounded(path, 4), b"1234")
            with (
                mock.patch.object(study.UTILITY, "ARTIFACT_LIMIT", 3),
                self.assertRaises(ValueError),
            ):
                study.read_bounded(path, 4)
            symlink = Path(directory) / "link"
            symlink.symlink_to(path)
            for target in (symlink, Path(directory), Path(directory) / "missing"):
                with self.subTest(target=target), self.assertRaises(ValueError):
                    study.read_bounded(target)
            if hasattr(study.UTILITY.os, "mkfifo"):
                fifo = Path(directory) / "fifo"
                study.UTILITY.os.mkfifo(fifo)
                with self.assertRaises(ValueError):
                    study.read_bounded(fifo)


class RouteBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()
        self.snapshot = fixture_snapshot(self.study)
        self.small = {"value": Fraction(1, 3), "count": 1, "flag": True, "empty": []}

    def routed(self, functions, snapshot=None):
        supplied_snapshot = self.snapshot if snapshot is None else snapshot
        modules = [
            type("SyntheticEngine", (), {"analyze": staticmethod(function)})
            for function in functions
        ]
        with (
            mock.patch.object(self.study, "source_snapshot", return_value=supplied_snapshot),
            mock.patch.object(self.study, "load_engine", side_effect=modules) as loader,
        ):
            result = self.study.analyze()
        self.assertEqual(
            loader.call_args_list,
            [
                mock.call(supplied_snapshot["primary.py"], "primary"),
                mock.call(supplied_snapshot["reference.py"], "reference"),
            ],
        )
        return result

    def test_fresh_snapshot_engines_ignore_module_cache_and_inputs_are_separate(self):
        study = self.study
        blob = b"from fractions import Fraction\ndef analyze(protocol):\n return {'value':Fraction(1,3)}\n"
        poison = type(
            "Poison",
            (),
            {"analyze": staticmethod(lambda _: (_ for _ in ()).throw(AssertionError("cache")))},
        )
        with mock.patch.dict(sys.modules, {"bn_synthetic": poison}):
            first = study.load_engine(blob, "bn_synthetic")
            second = study.load_engine(blob, "bn_synthetic")
        self.assertIsNot(first, second)
        exact_tree(self, first.analyze({}), {"value": Fraction(1, 3)})
        seen = []

        def collect(protocol):
            seen.append(protocol)
            return copy.deepcopy(self.small)

        exact_tree(self, self.routed([collect, collect]), self.small)
        self.assertIsNot(seen[0], seen[1])
        self.assertIsNot(seen[0]["geometries"], seen[1]["geometries"])

    def test_mismatched_native_reports_and_both_input_mutation_routes_refuse(self):
        for replacement in (Fraction(2, 3), "1/3", 1, None):
            changed = {**self.small, "value": replacement}
            with self.subTest(report=replacement), self.assertRaises(ValueError):
                self.routed([lambda _: copy.deepcopy(self.small), lambda _, x=changed: x])
        for slot in (0, 1):
            for field, replacement in (
                ("quota", True),
                ("quota", Fraction(4)),
                ("schema", "changed"),
            ):

                def bad(protocol, key=field, value=replacement):
                    protocol[key] = value
                    return copy.deepcopy(self.small)

                routes = [lambda _: copy.deepcopy(self.small), lambda _: copy.deepcopy(self.small)]
                routes[slot] = bad
                with (
                    self.subTest(slot=slot, field=field, type=type(replacement)),
                    self.assertRaises(ValueError),
                ):
                    self.routed(routes)
        with self.assertRaises(ValueError):
            self.routed([lambda _: {"illegal": None}, lambda _: {"illegal": None}])

    def test_protocol_pin_then_native_contract_and_source_bracketing(self):
        study = self.study
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["protocol.json"] += b"\n"
        with (
            mock.patch.object(
                study, "strict_loads", side_effect=AssertionError("hash must precede parse")
            ),
            self.assertRaises(ValueError),
        ):
            study._protocol(snapshot)
        protocol = json.loads(self.snapshot["protocol.json"])
        changes = [
            replace_path(protocol, ["quota"], True),
            replace_path(protocol, ["density_bounds", 3, "interval", 1, 0], 3),
            replace_path(protocol, ["population_data", -1, "q", 0], 0),
            replace_path(protocol, ["geometries", -1, "scale"], 5),
            replace_path(protocol, ["observer", "data_kind"], "sample_frequency"),
            replace_path(protocol, ["coverage", "hypotheses"], 143),
        ]
        for changed in changes:
            snapshot = {**self.snapshot, "protocol.json": study.canonical(changed)}
            with (
                mock.patch.object(
                    study, "PROTOCOL_SHA256", hashlib.sha256(snapshot["protocol.json"]).hexdigest()
                ),
                self.assertRaises(ValueError),
            ):
                study._protocol(snapshot)
        changed = {**self.snapshot, "reference.py": b"changed"}
        module = type(
            "SyntheticEngine", (), {"analyze": staticmethod(lambda _: copy.deepcopy(self.small))}
        )
        with (
            mock.patch.object(study, "source_snapshot", side_effect=[self.snapshot, changed]),
            mock.patch.object(study, "load_engine", return_value=module),
            self.assertRaises(ValueError),
        ):
            study.analyze()

    def test_complete_report_representative_wire_corruptions_are_detected(self):
        _study, _protocol, report = evaluated()
        count = 0
        for changed in report_mutations(report):
            with self.subTest(mutation=count):
                with self.assertRaises(ValueError):
                    self.study.require_equal(report, changed)
                with self.assertRaises(ValueError):
                    self.routed([lambda _: report, lambda _, value=changed: value])
            count += 1
        self.assertEqual(count, 18)

    def test_population_menu_admission_precedes_supplied_integer_arithmetic(self):
        supplied = query([10**1000 + 1, 10**1000 + 3], "two")
        with (
            mock.patch.object(
                self.study.math, "gcd", side_effect=AssertionError("unregistered gcd")
            ),
            self.assertRaises(ValueError),
        ):
            self.study.identify(supplied)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()
        self.snapshot = fixture_snapshot(self.study)
        self.small = {"value": Fraction(1, 3), "count": 1, "flag": True, "empty": []}
        self.temporary = tempfile.TemporaryDirectory(prefix="qr05bn-evidence-")
        self.addCleanup(self.temporary.cleanup)
        self.freeze_path = Path(self.temporary.name) / "source-freeze.json"
        self.capture_path = Path(self.temporary.name) / "results.json"
        source_patch = mock.patch.object(self.study, "source_snapshot", return_value=self.snapshot)
        source_patch.start()
        self.addCleanup(source_patch.stop)
        analysis_patch = mock.patch.object(
            self.study, "analyze", return_value=copy.deepcopy(self.small)
        )
        self.analysis_mock = analysis_patch.start()
        self.addCleanup(analysis_patch.stop)

    def captured(self):
        self.study.freeze(self.freeze_path)
        self.study.capture(self.capture_path, self.freeze_path)
        return self.study.strict_loads(self.capture_path.read_bytes())

    def test_new_gate_schemas_defaults_create_only_roundtrip_without_old_wrappers(self):
        study = self.study
        patches = [
            mock.patch.object(study.UTILITY, name, side_effect=AssertionError("old wrapper"))
            for name in ("analyze", "estimate", "freeze", "capture", "replay")
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)
        artifact = study.freeze(self.freeze_path)
        self.assertEqual(artifact["schema"], "qr05bn-source-freeze-v1")
        self.assertEqual(len(artifact["sources"]), 9)
        self.analysis_mock.assert_not_called()
        exact_tree(self, study.capture(self.capture_path, self.freeze_path), self.small)
        exact_tree(self, study.replay(self.capture_path, self.freeze_path), self.small)
        self.assertEqual(self.analysis_mock.call_count, 2)
        captured = study.strict_loads(self.capture_path.read_bytes())
        self.assertEqual(captured["schema"], "qr05bn-capture-v1")
        self.assertEqual(
            captured["freeze_sha256"], hashlib.sha256(self.freeze_path.read_bytes()).hexdigest()
        )
        exact_tree(self, study.decode(captured["report"]), self.small)
        before = self.capture_path.read_bytes()
        for action, path in ((study.freeze, self.freeze_path), (study.capture, self.capture_path)):
            with self.assertRaises(FileExistsError):
                action(path)
        self.assertEqual(self.capture_path.read_bytes(), before)

    def test_streamed_capture_tampering_and_noncanonical_bytes_are_rejected(self):
        study = self.study
        artifact = self.captured()
        original_read = study.read_bounded
        changed_reports = [
            replace_path(artifact, ["schema"], "qr05bm-capture-v1"),
            replace_path(artifact, ["freeze_sha256"], "0" * 64),
            replace_path(artifact, ["sources", "primary.py", "bytes"], True),
            replace_path(artifact, ["sources", "reference.py", "sha256"], "f" * 64),
            replace_path(artifact, ["report", "value"], {"$fraction": [2, 3]}),
            replace_path(artifact, ["report", "value"], {"$fraction": [2, 6]}),
            replace_path(artifact, ["report", "count"], True),
            replace_path(artifact, ["report", "flag"], 1),
            replace_path(artifact, ["report", "empty"], 0),
            {**artifact, "extra": 0},
        ]
        blobs = [study.canonical(value) for value in changed_reports]
        blobs += [self.capture_path.read_bytes() + b"\n", b'{"schema":1,"schema":2}', b'{"x":1.0}']
        retained = self.capture_path.read_bytes()
        for index, blob in enumerate(blobs):
            self.assertNotEqual(blob, retained)

            def read(path, *args, data=blob):
                return data if Path(path) == self.capture_path else original_read(path, *args)

            with (
                self.subTest(mutation=index),
                mock.patch.object(study, "read_bounded", side_effect=read),
                self.assertRaises(ValueError),
            ):
                study.replay(self.capture_path, self.freeze_path)
        self.assertEqual(self.capture_path.read_bytes(), retained)

    def test_streamed_freeze_header_runtime_and_utility_identity_mutations(self):
        study = self.study
        self.captured()
        original_read = study.read_bounded
        artifact = study.strict_loads(self.freeze_path.read_bytes())
        changed = [
            replace_path(artifact, ["schema"], "qr05bm-source-freeze-v1"),
            replace_path(artifact, ["runtime", "optimization"], True),
            replace_path(artifact, ["runtime", "optimization"], 3),
            replace_path(artifact, ["runtime", "version"], ""),
            replace_path(artifact, ["runtime", "implementation"], ""),
            replace_path(artifact, ["sources", study.UTILITY_SOURCE, "sha256"], "f" * 64),
            replace_path(artifact, ["sources", "protocol.json", "bytes"], False),
            {**artifact, "extra": 0},
        ]
        blobs = [study.canonical(value) for value in changed]
        blobs.append(self.freeze_path.read_bytes() + b"\n")
        retained = self.freeze_path.read_bytes()
        for index, blob in enumerate(blobs):
            self.assertNotEqual(blob, retained)

            def read(path, *args, data=blob):
                return data if Path(path) == self.freeze_path else original_read(path, *args)

            with (
                self.subTest(mutation=index),
                mock.patch.object(study, "read_bounded", side_effect=read),
                self.assertRaises(ValueError),
            ):
                study.replay(self.capture_path, self.freeze_path)
        self.assertEqual(self.freeze_path.read_bytes(), retained)

    def test_analysis_and_postpublication_source_freeze_and_capture_changes_refuse(self):
        study = self.study
        study.freeze(self.freeze_path)
        original_freeze = self.freeze_path.read_bytes()

        def mutate_freeze():
            self.freeze_path.write_bytes(original_freeze + b"\n")
            return copy.deepcopy(self.small)

        with (
            mock.patch.object(study, "analyze", side_effect=mutate_freeze),
            self.assertRaises(ValueError),
        ):
            study.capture(self.capture_path, self.freeze_path)
        self.assertFalse(self.capture_path.exists())
        self.freeze_path.write_bytes(original_freeze)
        changed = {**self.snapshot, "reference.py": b"changed"}
        with (
            mock.patch.object(study, "source_snapshot", side_effect=[self.snapshot, changed]),
            self.assertRaises(ValueError),
        ):
            study.capture(self.capture_path, self.freeze_path)
        self.assertFalse(self.capture_path.exists())
        original_write = study._write_new

        def mutate_after_write(path, data):
            original_write(path, data)
            Path(path).write_bytes(data + b"\n")

        with (
            mock.patch.object(study, "_write_new", side_effect=mutate_after_write),
            self.assertRaises(ValueError),
        ):
            study.capture(self.capture_path, self.freeze_path)
        self.assertTrue(self.capture_path.exists(), "post-write failures preserve the artifact")

    def test_replay_rechecks_artifact_and_freeze_after_recomputation(self):
        study = self.study
        self.captured()
        capture_bytes = self.capture_path.read_bytes()
        freeze_bytes = self.freeze_path.read_bytes()
        for path, original in (
            (self.capture_path, capture_bytes),
            (self.freeze_path, freeze_bytes),
        ):

            def corrupt(target=path, blob=original):
                target.write_bytes(blob + b"\n")
                return copy.deepcopy(self.small)

            with (
                self.subTest(path=path.name),
                mock.patch.object(study, "analyze", side_effect=corrupt),
                self.assertRaises(ValueError),
            ):
                study.replay(self.capture_path, self.freeze_path)
            path.write_bytes(original)
        changed = {**self.small, "count": True}
        with (
            mock.patch.object(study, "analyze", return_value=changed),
            self.assertRaises(ValueError),
        ):
            study.replay(self.capture_path, self.freeze_path)

    def test_freeze_rechecks_publication_after_final_source_check(self):
        study = self.study
        calls = []

        def source_check(snapshot):
            self.assertEqual(snapshot, self.snapshot)
            calls.append(1)
            if len(calls) == 2:
                self.freeze_path.write_bytes(self.freeze_path.read_bytes() + b"\n")

        with (
            mock.patch.object(study, "_check_snapshot", side_effect=source_check),
            self.assertRaises(ValueError),
        ):
            study.freeze(self.freeze_path)
        self.assertEqual(len(calls), 2)
        self.assertTrue(self.freeze_path.exists())


class DeadlineTests(unittest.TestCase):
    def test_reused_deadline_checks_elapsed_work_and_preserves_earlier_outer_alarm(self):
        study = load_study()
        utility = study.UTILITY
        with (
            mock.patch.object(utility.signal, "getsignal", return_value=utility.signal.SIG_DFL),
            mock.patch.object(utility.signal, "getitimer", return_value=(0.0, 0.0)),
            mock.patch.object(utility.signal, "signal") as handlers,
            mock.patch.object(utility.signal, "setitimer") as timers,
            mock.patch.object(utility.time, "monotonic", side_effect=[0.0, 31.0]),
            self.assertRaises(ValueError),
            study._analysis_deadline(),
        ):
            pass
        self.assertEqual(timers.call_args_list[0], mock.call(utility.signal.ITIMER_REAL, 30))
        self.assertEqual(timers.call_args_list[-1], mock.call(utility.signal.ITIMER_REAL, 0))
        self.assertEqual(
            handlers.call_args_list[-1], mock.call(utility.signal.SIGALRM, utility.signal.SIG_DFL)
        )
        previous = mock.Mock(side_effect=KeyboardInterrupt("outer suite deadline"))
        with (
            mock.patch.object(utility.signal, "getsignal", return_value=previous),
            mock.patch.object(utility.signal, "getitimer", return_value=(5.0, 0.0)),
            mock.patch.object(utility.signal, "signal") as handlers,
            mock.patch.object(utility.signal, "setitimer") as timers,
            mock.patch.object(utility.time, "monotonic", side_effect=[0.0, 2.0]),
            self.assertRaises(KeyboardInterrupt),
            study._analysis_deadline(),
        ):
            installed = handlers.call_args_list[0].args[1]
            installed(utility.signal.SIGALRM, None)
        previous.assert_called_once_with(utility.signal.SIGALRM, None)
        self.assertEqual(timers.call_args_list[0], mock.call(utility.signal.ITIMER_REAL, 5.0))
        self.assertEqual(timers.call_args_list[-1], mock.call(utility.signal.ITIMER_REAL, 3.0, 0.0))


if __name__ == "__main__":
    import signal

    def suite_expired(_signum, _frame):
        raise KeyboardInterrupt("QR-05BN 120-second suite deadline")

    signal.signal(signal.SIGALRM, suite_expired)
    signal.setitimer(signal.ITIMER_REAL, 120)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
