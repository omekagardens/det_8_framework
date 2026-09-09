"""Source-bound BM tests; endpoint integration and scalar complete-law oracle.

No numerical fixture evaluation or engine import occurs at module import.
Only the current driver is lazily loaded, after the root's execution release.
All checks use unittest assertions and remain active under optimized Python.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import math
import os
import sys
import tempfile
import unittest
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent


def load_study():
    spec = importlib.util.spec_from_file_location("_qr05bm_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("current BM driver cannot be loaded")
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


def terms(coefficients):
    return [[i, j, value] for (i, j), value in sorted(coefficients.items()) if value]


def coefficients(polynomial):
    return {(i, j): value for i, j, value in polynomial}


def rescale(polynomial, scalar):
    return [[i, j, scalar * value] for i, j, value in polynomial if scalar * value]


def rectangle_monomial(bounds, i, j):
    a, b, c, d = bounds
    return (b ** (i + 1) - a ** (i + 1)) * (d ** (j + 1) - c ** (j + 1)) / ((i + 1) * (j + 1))


def endpoint_integral(polynomial, bounds):
    return sum(
        (value * rectangle_monomial(bounds, i, j) for i, j, value in polynomial), Fraction(0)
    )


def chart_polynomial(polynomial, chart, jacobian=False):
    """Explicit binomial expansion of each monomial under the inverse affine map."""
    a, b = Fraction(chart["U_scale"]), Fraction(chart["U_offset"])
    c, d = Fraction(chart["V_scale"]), Fraction(chart["V_offset"])
    result = {}
    for i, j, value in polynomial:
        for x, y in itertools.product(range(i + 1), range(j + 1)):
            coefficient = value * math.comb(i, x) * math.comb(j, y)
            coefficient *= (-b) ** (i - x) * (-d) ** (j - y) / (a**i * c**j)
            if jacobian:
                coefficient /= a * c
            result[x, y] = result.get((x, y), Fraction(0)) + coefficient
    return terms(result)


def geometry_oracle(world, protocol):
    eta, scale, density = (Fraction(world[key]) for key in ("eta", "scale", "density_uv"))
    metric = terms({(0, 0): scale, (1, 1): scale * eta})
    weight = terms({(0, 0): Fraction(1), (1, 1): density})
    proper = rescale(metric, Fraction(1, 2))
    weighted = terms(
        {
            (0, 0): scale / 2,
            (1, 1): scale * (eta + density) / 2,
            (2, 2): scale * eta * density / 2,
        }
    )
    regions = {
        name: [Fraction(*pair) for pair in bounds] for name, bounds in protocol["regions"].items()
    }

    def scalars(p, w, domains):
        result = {"volume_" + key: endpoint_integral(p, domains[key]) for key in ("Q", "I")}
        result.update({"mass_" + key: endpoint_integral(w, domains[key]) for key in ("Q", "I")})
        result["target"] = result["volume_I"] / result["volume_Q"]
        result["q"] = result["mass_I"] / result["mass_Q"]
        return result

    values = scalars(proper, weighted, regions)
    chart = protocol["chart"]
    transported = {
        name: [
            chart["U_scale"] * bounds[0] + chart["U_offset"],
            chart["U_scale"] * bounds[1] + chart["U_offset"],
            chart["V_scale"] * bounds[2] + chart["V_offset"],
            chart["V_scale"] * bounds[3] + chart["V_offset"],
        ]
        for name, bounds in regions.items()
    }
    chart_proper = chart_polynomial(proper, chart, True)
    chart_weighted = chart_polynomial(weighted, chart, True)
    chart_values = scalars(chart_proper, chart_weighted, transported)
    return {
        "metric_uv": metric,
        "density_uv": weight,
        "proper_uv": proper,
        "weighted_uv": weighted,
        "normalized_uv": rescale(weighted, 1 / values["mass_Q"]),
        **values,
        "chart": {
            "metric_UV": chart_polynomial(metric, chart, True),
            "density_UV": chart_polynomial(weight, chart),
            "proper_UV": chart_proper,
            "weighted_UV": chart_weighted,
            "normalized_UV": rescale(chart_weighted, 1 / chart_values["mass_Q"]),
            **chart_values,
        },
    }


def one_hot(z):
    position = sum((value == -1) * 2 ** (len(z) - index - 1) for index, value in enumerate(z))
    return [Fraction(index == position) for index in range(2 ** len(z))]


def world_oracle(world, protocol):
    quota = protocol["quota"]
    geometry = geometry_oracle(world, protocol)
    q = geometry["q"]
    membership = []
    cq = []
    for y in itertools.product((0, 1), repeat=quota):
        k = sum(y)
        probability = q**k * (1 - q) ** (quota - k)
        membership.append({"y": list(y), "k": k, "p": probability, "estimate": Fraction(k, quota)})
        for z in itertools.product((-1, 1), repeat=quota):
            conditional = one_hot(z)
            joint = probability / 2**quota
            cq.append(
                {
                    "y": list(y),
                    "z": list(z),
                    "p": joint,
                    "trace": joint,
                    "diagonal": [joint * value for value in conditional],
                    "conditional_diagonal": conditional,
                }
            )
    histogram = [
        {
            "k": k,
            "multiplicity": math.comb(quota, k),
            "p": math.comb(quota, k) * q**k * (1 - q) ** (quota - k),
        }
        for k in range(quota + 1)
    ]
    mean = sum((row["p"] * row["estimate"] for row in membership), Fraction(0))
    variance = sum((row["p"] * (row["estimate"] - mean) ** 2 for row in membership), Fraction(0))
    return {
        "id": world["id"],
        "geometry": geometry,
        "membership": membership,
        "histogram": histogram,
        "moments": {"mean": mean, "variance": variance, "bias": mean - geometry["target"]},
        "cq": cq,
    }


def law_classes(worlds, kind):
    groups = []
    vectors = []
    for world in worlds:
        vector = [row["p"] for row in world[kind]]
        if vector not in vectors:
            vectors.append(vector)
            groups.append([])
        groups[vectors.index(vector)].append(world)
    return [
        {
            "worlds": [world["id"] for world in group],
            "targets": sorted({world["geometry"]["target"] for world in group}),
            "identified": len({world["geometry"]["target"] for world in group}) == 1,
        }
        for group in groups
    ]


def expected(protocol):
    worlds = [world_oracle(world, protocol) for world in protocol["worlds"]]
    by_id = {world["id"]: world for world in worlds}
    menus = []
    for menu in protocol["menus"]:
        selected = [by_id[name] for name in menu["worlds"]]
        classes = law_classes(selected, "membership")
        menus.append(
            {
                "id": menu["id"],
                "worlds": list(menu["worlds"]),
                "classes": classes,
                "cq_classes": law_classes(selected, "cq"),
                "identified": all(row["identified"] for row in classes),
                "support": [
                    {
                        "y": list(y),
                        "worlds": [
                            world["id"] for world in selected if world["membership"][index]["p"] > 0
                        ],
                    }
                    for index, y in enumerate(itertools.product((0, 1), repeat=protocol["quota"]))
                ],
            }
        )
    b, c = by_id["B"]["geometry"], by_id["C"]["geometry"]
    scale_pairs = []
    for first, second in (("A", "D"), ("B", "E")):
        a, b_world = by_id[first], by_id[second]
        scale_pairs.append(
            {
                "worlds": [first, second],
                "volume_factor": b_world["geometry"]["volume_Q"] / a["geometry"]["volume_Q"],
                "normalized_equal": a["geometry"]["normalized_uv"]
                == b_world["geometry"]["normalized_uv"],
                "target_equal": a["geometry"]["target"] == b_world["geometry"]["target"],
                "law_equal": [row["p"] for row in a["membership"]]
                == [row["p"] for row in b_world["membership"]],
                "cq_equal": a["cq"] == b_world["cq"],
            }
        )
    scalar_names = ("volume_Q", "volume_I", "mass_Q", "mass_I", "target", "q")
    marginals = all(
        sum((row["p"] for row in world["cq"] if row["y"] == membership["y"]), Fraction(0))
        == membership["p"]
        for world in worlds
        for membership in world["membership"]
    )
    conditionals = all(
        row["conditional_diagonal"] == one_hot(row["z"]) for world in worlds for row in world["cq"]
    )
    return {
        "schema": "qr05bm-report-v1",
        "quota": protocol["quota"],
        "worlds": worlds,
        "menus": menus,
        "controls": {
            "density_equal": b["weighted_uv"] == c["weighted_uv"] and b["mass_Q"] == c["mass_Q"],
            "density_target_gap": c["target"] - b["target"],
            "scale_pairs": scale_pairs,
            "chart_invariant": [
                world["id"]
                for world in worlds
                if all(
                    world["geometry"][key] == world["geometry"]["chart"][key]
                    for key in scalar_names
                )
            ],
            "cq_marginals_match": marginals,
            "cq_conditionals_common": conditionals,
        },
    }


def packet(y, z=None):
    records = []
    for index, value in enumerate(y, start=1):
        row = {"attempt": index, "y": value}
        if z is not None:
            row["z"] = z[index - 1]
        records.append(row)
    return {
        "protocol": "qr05bm-v1",
        "query": "o-m-t",
        "variant": "membership" if z is None else "membership-z",
        "records": records,
    }


class MathematicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.report = evaluated()

    def test_complete_independent_native_report(self):
        exact_tree(self, self.report, expected(self.protocol))

    def test_integrals_independent_of_precomputed_ratios_and_chart_jacobians(self):
        by_id = {world["id"]: world["geometry"] for world in self.report["worlds"]}
        anticipated = {
            "A": ("1/2", "1/8", "1/2", "1/8", "1/4", "1/4"),
            "B": ("5/8", "17/128", "5/8", "17/128", "17/80", "17/80"),
            "C": ("1/2", "1/8", "5/8", "17/128", "1/4", "17/80"),
            "D": ("2", "1/2", "2", "1/2", "1/4", "1/4"),
            "E": ("5/2", "17/32", "5/2", "17/32", "17/80", "17/80"),
        }
        names = ("volume_Q", "volume_I", "mass_Q", "mass_I", "target", "q")
        for name, values in anticipated.items():
            with self.subTest(world=name):
                self.assertEqual([by_id[name][key] for key in names], list(map(Fraction, values)))
                self.assertEqual(
                    [by_id[name]["chart"][key] for key in names], list(map(Fraction, values))
                )
        bounds = [Fraction(1), Fraction(3), Fraction(-1), Fraction(2)]
        for geometry in by_id.values():
            self.assertEqual(endpoint_integral(geometry["chart"]["normalized_UV"], bounds), 1)
            self.assertEqual(
                geometry["chart"]["proper_UV"],
                rescale(geometry["chart"]["metric_UV"], Fraction(1, 2)),
            )
        # Scalar density receives composition only; a second Jacobian would be wrong.
        self.assertEqual(by_id["A"]["chart"]["density_UV"], [[0, 0, Fraction(1)]])
        self.assertEqual(by_id["A"]["chart"]["proper_UV"], [[0, 0, Fraction(1, 12)]])
        self.assertNotEqual(
            by_id["C"]["chart"]["density_UV"], rescale(by_id["C"]["density_uv"], Fraction(1, 6))
        )

    def test_full_membership_laws_histograms_moments_and_finite_support(self):
        quota = self.report["quota"]
        for world in self.report["worlds"]:
            q = world["geometry"]["q"]
            self.assertEqual(
                [row["y"] for row in world["membership"]],
                [list(y) for y in itertools.product((0, 1), repeat=quota)],
            )
            self.assertEqual(sum(row["p"] for row in world["membership"]), 1)
            self.assertTrue(all(row["p"] > 0 for row in world["membership"]))
            for row in world["histogram"]:
                matching = [item for item in world["membership"] if item["k"] == row["k"]]
                self.assertEqual(len(matching), row["multiplicity"])
                self.assertEqual(sum(item["p"] for item in matching), row["p"])
                self.assertEqual(row["p"] / row["multiplicity"], matching[0]["p"])
            self.assertEqual(world["moments"]["mean"], q)
            self.assertEqual(world["moments"]["variance"], q * (1 - q) / quota)
            self.assertEqual(world["moments"]["bias"], q - world["geometry"]["target"])
            for row in world["membership"]:
                self.assertEqual(self.study.estimate(packet(row["y"])), row["estimate"])
        self.assertEqual(
            [w["moments"]["bias"] for w in self.report["worlds"]],
            [Fraction(0), Fraction(0), Fraction(-3, 80), Fraction(0), Fraction(0)],
        )

    def test_all_quantum_entries_traces_marginals_and_conditional_world_independence(self):
        for world in self.report["worlds"]:
            self.assertEqual(len(world["cq"]), 256)
            self.assertEqual(sum(row["p"] for row in world["cq"]), 1)
            for row in world["cq"]:
                self.assertIs(type(row["p"]), Fraction)
                self.assertEqual(row["trace"], sum(row["diagonal"]))
                self.assertEqual(row["p"], row["trace"])
                self.assertGreater(row["trace"], 0)
                self.assertEqual(sum(row["conditional_diagonal"]), 1)
                self.assertEqual(row["conditional_diagonal"], one_hot(row["z"]))
                self.assertEqual(
                    [x / row["trace"] for x in row["diagonal"]], row["conditional_diagonal"]
                )
                self.assertEqual(sum(x == 0 for x in row["diagonal"]), 15)
            for membership in world["membership"]:
                related = [row for row in world["cq"] if row["y"] == membership["y"]]
                self.assertEqual(sum(row["p"] for row in related), membership["p"])
                self.assertEqual(
                    [sum(row["diagonal"][i] for row in related) for i in range(16)],
                    [membership["p"] / 16] * 16,
                )
        self.assertTrue(self.report["controls"]["cq_marginals_match"])
        self.assertTrue(self.report["controls"]["cq_conditionals_common"])

    def test_labeled_law_classes_not_one_word_candidate_selection(self):
        positive, expanded = self.report["menus"]
        self.assertTrue(positive["identified"])
        self.assertFalse(expanded["identified"])
        self.assertEqual(
            expanded["classes"],
            [
                {"worlds": ["A", "D"], "targets": [Fraction(1, 4)], "identified": True},
                {
                    "worlds": ["B", "C", "E"],
                    "targets": [Fraction(17, 80), Fraction(1, 4)],
                    "identified": False,
                },
            ],
        )
        for menu in self.report["menus"]:
            self.assertEqual(menu["classes"], menu["cq_classes"])
            self.assertTrue(all(row["worlds"] == menu["worlds"] for row in menu["support"]))
        controls = self.report["controls"]
        self.assertTrue(controls["density_equal"])
        self.assertEqual(controls["density_target_gap"], Fraction(3, 80))
        for row in controls["scale_pairs"]:
            self.assertEqual(row["volume_factor"], Fraction(4))
            for key in ("normalized_equal", "target_equal", "law_equal", "cq_equal"):
                self.assertIs(row[key], True)
        self.assertEqual(controls["chart_invariant"], ["A", "B", "C", "D", "E"])

    def test_prespecified_coverage_and_scalar_native_types(self):
        self.assertEqual(len(self.report["worlds"]), 5)
        self.assertEqual(sum(len(w["membership"]) for w in self.report["worlds"]), 80)
        self.assertEqual(sum(len(w["histogram"]) for w in self.report["worlds"]), 25)
        self.assertEqual(sum(len(w["cq"]) for w in self.report["worlds"]), 1280)
        for world in self.report["worlds"]:
            for geometry, suffix in ((world["geometry"], "uv"), (world["geometry"]["chart"], "UV")):
                for name in ("metric", "density", "proper", "weighted", "normalized"):
                    polynomial = geometry[name + "_" + suffix]
                    self.assertEqual(
                        [(i, j) for i, j, _ in polynomial],
                        sorted({(i, j) for i, j, _ in polynomial}),
                    )
                    for i, j, value in polynomial:
                        self.assertIs(type(i), int)
                        self.assertIs(type(j), int)
                        self.assertIs(type(value), Fraction)
                        self.assertNotEqual(value, 0)
                for name in ("volume_Q", "volume_I", "mass_Q", "mass_I", "target", "q"):
                    self.assertIs(type(geometry[name]), Fraction)
            for value in world["moments"].values():
                self.assertIs(type(value), Fraction)


class ObserverTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_every_declared_word_and_z_variant_has_exact_estimate(self):
        for y in itertools.product((0, 1), repeat=4):
            plain = packet(y)
            before = copy.deepcopy(plain)
            result = self.study.estimate(plain)
            self.assertIs(type(result), Fraction)
            self.assertEqual(result, Fraction(sum(y), 4))
            self.assertEqual(plain, before)
            for z in itertools.product((-1, 1), repeat=4):
                data = packet(y, z)
                before = copy.deepcopy(data)
                self.assertEqual(self.study.estimate(data), result)
                self.assertEqual(data, before)

    def test_top_level_schema_types_context_and_privacy(self):
        base = packet([0, 1, 0, 1])

        class DictChild(dict):
            pass

        class ListChild(list):
            pass

        class StringChild(str):
            pass

        bad = [None, [], (), DictChild(base)]
        bad.append({StringChild(key): value for key, value in base.items()})
        for key in base:
            changed = copy.deepcopy(base)
            del changed[key]
            bad.append(changed)
        for key, value in [
            ("protocol", "wrong"),
            ("query", "other"),
            ("variant", "membership_z"),
            ("protocol", StringChild("qr05bm-v1")),
            ("query", True),
            ("variant", StringChild("membership")),
            ("records", tuple(base["records"])),
            ("records", ListChild(base["records"])),
            ("records", []),
            ("records", base["records"][:-1]),
            ("records", base["records"] + [base["records"][-1]]),
        ]:
            changed = copy.deepcopy(base)
            changed[key] = value
            bad.append(changed)
        for key in (
            "world",
            "eta",
            "density",
            "scale",
            "seed",
            "target",
            "probability",
            "branch",
            "coordinates",
            "extra",
        ):
            changed = copy.deepcopy(base)
            changed[key] = None
            bad.append(changed)
        for index, value in enumerate(bad):
            with self.subTest(case=index), self.assertRaises(ValueError):
                self.study.estimate(value)

    def test_attempt_order_and_late_record_strict_native_values(self):
        class DictChild(dict):
            pass

        class IntChild(int):
            pass

        class StringChild(str):
            pass

        for z in (None, [-1, 1, -1, 1]):
            base = packet([0, 1, 1, 0], z)
            changes = []
            changed = copy.deepcopy(base)
            changed["records"].reverse()
            changes.append(changed)
            changed = copy.deepcopy(base)
            changed["records"][0], changed["records"][1] = (
                changed["records"][1],
                changed["records"][0],
            )
            changes.append(changed)
            changed = copy.deepcopy(base)
            changed["records"][-1] = DictChild(changed["records"][-1])
            changes.append(changed)
            changed = copy.deepcopy(base)
            changed["records"][-1] = {
                StringChild(key): value for key, value in changed["records"][-1].items()
            }
            changes.append(changed)
            for key in base["records"][-1]:
                changed = copy.deepcopy(base)
                del changed["records"][-1][key]
                changes.append(changed)
            for key, values in [
                ("attempt", [0, -1, 1, 5, True, 4.0, "4", IntChild(4), None]),
                (
                    "y",
                    [
                        -1,
                        2,
                        True,
                        False,
                        0.0,
                        float("nan"),
                        float("inf"),
                        "0",
                        IntChild(0),
                        None,
                        [],
                    ],
                ),
            ]:
                for value in values:
                    changed = copy.deepcopy(base)
                    changed["records"][-1][key] = value
                    changes.append(changed)
            if z is not None:
                for value in (0, 2, True, -1.0, "-1", IntChild(1), None):
                    changed = copy.deepcopy(base)
                    changed["records"][-1]["z"] = value
                    changes.append(changed)
            else:
                changed = copy.deepcopy(base)
                changed["records"][-1]["z"] = 1
                changes.append(changed)
            for key in ("world", "probability", "state", "coordinates", "extra"):
                changed = copy.deepcopy(base)
                changed["records"][-1][key] = None
                changes.append(changed)
            for index, changed in enumerate(changes):
                with (
                    self.subTest(variant=base["variant"], case=index),
                    self.assertRaises(ValueError),
                ):
                    self.study.estimate(changed)

    def test_receiver_uses_no_source_world_or_analysis_access(self):
        with (
            mock.patch.object(
                self.study, "source_snapshot", side_effect=AssertionError("source access")
            ),
            mock.patch.object(self.study, "analyze", side_effect=AssertionError("producer access")),
            mock.patch.object(
                self.study, "read_bounded", side_effect=AssertionError("file access")
            ),
        ):
            self.assertEqual(self.study.estimate(packet([1, 0, 0, 1])), Fraction(1, 2))
            self.assertEqual(
                self.study.estimate(packet([1, 0, 0, 1], [1, -1, -1, 1])), Fraction(1, 2)
            )


def set_path(value, path, replacement):
    target = value
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = replacement


def get_path(value, path):
    for part in path:
        value = value[part]
    return value


def representative_mutations(report):
    """Bounded retained-wire mutations; do not build a giant artifact corpus."""
    paths = [
        (("schema",), "changed"),
        (("quota",), True),
        (("worlds", -1, "id"), "changed"),
        (("worlds", -1, "geometry", "metric_uv", -1, 2), Fraction(9)),
        (("worlds", -1, "geometry", "density_uv", -1, 2), Fraction(9)),
        (("worlds", -1, "geometry", "proper_uv", -1, 2), Fraction(9)),
        (("worlds", -1, "geometry", "weighted_uv", -1, 2), Fraction(9)),
        (("worlds", -1, "geometry", "normalized_uv", -1, 2), Fraction(9)),
        (("worlds", -1, "geometry", "volume_Q"), Fraction(9)),
        (("worlds", -1, "geometry", "mass_I"), Fraction(9)),
        (("worlds", -1, "geometry", "target"), Fraction(9)),
        (("worlds", -1, "geometry", "chart", "metric_UV", -1, 2), Fraction(9)),
        (("worlds", -1, "geometry", "chart", "density_UV", -1, 2), Fraction(9)),
        (("worlds", -1, "geometry", "chart", "volume_Q"), Fraction(9)),
        (("worlds", -1, "geometry", "chart", "q"), Fraction(9)),
        (("worlds", -1, "membership", -1, "p"), Fraction(9)),
        (("worlds", -1, "membership", -1, "estimate"), Fraction(9)),
        (("worlds", -1, "membership", -1, "y", -1), True),
        (("worlds", -1, "histogram", -1, "multiplicity"), True),
        (("worlds", -1, "moments", "variance"), Fraction(9)),
        (("worlds", -1, "cq", -1, "p"), Fraction(9)),
        (("worlds", -1, "cq", -1, "trace"), Fraction(9)),
        (("worlds", -1, "cq", -1, "diagonal", -1), Fraction(9)),
        (("worlds", -1, "cq", -1, "conditional_diagonal", -1), Fraction(9)),
        (("worlds", -1, "cq", -1, "z", -1), True),
        (("menus", -1, "classes", -1, "targets"), [Fraction(17, 80)]),
        (("menus", -1, "cq_classes", -1, "identified"), True),
        (("menus", -1, "support", -1, "worlds"), ["B"]),
        (("menus", -1, "identified"), 0),
        (("controls", "density_equal"), 1),
        (("controls", "density_target_gap"), Fraction(-3, 80)),
        (("controls", "scale_pairs", -1, "volume_factor"), Fraction(2)),
        (("controls", "chart_invariant"), ["A"]),
        (("controls", "cq_marginals_match"), False),
        (("controls", "cq_conditionals_common"), False),
    ]
    for path, replacement in paths:
        changed = copy.deepcopy(report)
        set_path(changed, path, replacement)
        yield path, changed
    for key in report:
        changed = copy.deepcopy(report)
        del changed[key]
        yield ("missing", key), changed
    for path in (
        ("worlds",),
        ("worlds", -1, "cq"),
        ("worlds", -1, "cq", -1, "diagonal"),
        ("menus",),
    ):
        changed = copy.deepcopy(report)
        set_path(changed, path, get_path(changed, path)[:-1])
        yield ("truncated", *path), changed
    changed = copy.deepcopy(report)
    changed["actual_world"] = "E"
    yield ("extra",), changed


class CodecTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()

    def test_tagged_fraction_roundtrip_and_exact_native_comparison(self):
        native = {
            "fractions": [Fraction(0), Fraction(-2, 3), Fraction(1)],
            "integer": 1,
            "boolean": True,
            "word": "1",
        }
        wire = {
            "fractions": [{"$fraction": [0, 1]}, {"$fraction": [-2, 3]}, {"$fraction": [1, 1]}],
            "integer": 1,
            "boolean": True,
            "word": "1",
        }
        exact_tree(self, self.study.encode(native), wire)
        exact_tree(self, self.study.decode(wire), native)
        exact_tree(
            self, self.study.decode(self.study.strict_loads(self.study.canonical(wire))), native
        )
        self.study.require_equal(native, copy.deepcopy(native))
        self.assertIs(type(self.study.canonical(wire)), bytes)
        for left, right in [
            (True, 1),
            (Fraction(1), 1),
            (Fraction(1), "1"),
            ([1], (1,)),
            ({"one": 1}, {"one": 1, "extra": 0}),
            ([1], [1, 2]),
            (0.0, 0.0),
            (None, None),
            ({1: "bad"}, {1: "bad"}),
        ]:
            with self.subTest(left=left, right=right), self.assertRaises(ValueError):
                self.study.require_equal(left, right)

    def test_fraction_tags_canonicality_unknown_tags_and_unsupported_types(self):
        class IntChild(int):
            pass

        bad = [
            {"$fraction": [2, 4]},
            {"$fraction": [0, 2]},
            {"$fraction": [1, 0]},
            {"$fraction": [1, -2]},
            {"$fraction": [True, 1]},
            {"$fraction": [1, True]},
            {"$fraction": [1]},
            {"$fraction": [1, 2, 3]},
            {"$fraction": (1, 2)},
            {"$fraction": [1, 2], "extra": 0},
            {"$fraction": ["1", 2]},
            {"$fraction": [IntChild(1), 2]},
            {"$unknown": [1, 2]},
            None,
            0.0,
            float("nan"),
            float("inf"),
            (),
            {1: "bad"},
        ]
        for value in bad:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.study.decode(value)
        for value in (None, 0.0, (), {"$fraction": [1, 2]}, {1: "bad"}, IntChild(1)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.study.encode(value)
        for value in (None, 0.0, float("nan"), Fraction(1), (), {1: "bad"}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.study.canonical(value)

    def test_strict_json_duplicate_keys_nonfinite_and_byte_cap(self):
        invalid = [
            b"",
            b"{",
            b"\xff",
            b'{"a":1,"a":2}',
            b'{"a":{"b":1,"b":2}}',
            b"0.0",
            b"1e0",
            b"NaN",
            b"Infinity",
            b"-Infinity",
            "{}",
            bytearray(b"{}"),
        ]
        for data in invalid:
            with self.subTest(data=repr(data)), self.assertRaises(ValueError):
                self.study.strict_loads(data)
        with mock.patch.object(self.study, "ARTIFACT_LIMIT", 3):
            self.assertEqual(self.study.strict_loads(b"[1]"), [1])
            with self.assertRaises(ValueError):
                self.study.strict_loads(b"[10]")
            with self.assertRaises(ValueError):
                self.study.canonical({"long": "value"})


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()
        self.protocol_bytes = (HERE / "protocol.json").read_bytes()
        self.protocol = json.loads(self.protocol_bytes)
        self.report = {"value": Fraction(1, 3), "count": 1, "flag": True}
        self.snapshot = {
            "protocol.json": self.protocol_bytes,
            "primary.py": b"primary",
            "reference.py": b"reference",
        }

    def compare(self, first, second, snapshot=None):
        snapshots = self.snapshot if snapshot is None else snapshot
        with (
            mock.patch.object(
                self.study, "source_snapshot", side_effect=lambda: copy.deepcopy(snapshots)
            ),
            mock.patch.object(
                self.study,
                "load_engine",
                side_effect=lambda _blob, name: type(
                    "Engine", (), {"analyze": staticmethod(first if name == "primary" else second)}
                )(),
            ),
        ):
            return self.study.analyze()

    def test_fresh_independent_inputs_and_type_sensitive_whole_report_comparison(self):
        seen = []

        def correct(value):
            seen.append(value)
            return copy.deepcopy(self.report)

        self.assertEqual(self.compare(correct, correct), self.report)
        self.assertIsNot(seen[0], seen[1])
        self.assertIsNot(seen[0]["worlds"], seen[1]["worlds"])
        self.assertEqual(seen, [self.protocol, self.protocol])
        for key, value in [
            ("value", "1/3"),
            ("value", 1),
            ("count", True),
            ("flag", 1),
            ("value", Fraction(2, 3)),
            ("extra", 0),
        ]:
            changed = copy.deepcopy(self.report)
            changed[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.compare(lambda _p: self.report, lambda _p, changed=changed: changed)
        with self.assertRaises(ValueError):
            self.compare(lambda _p: {"bad": 0.0}, lambda _p: {"bad": 0.0})

    def test_protocol_shapes_values_and_both_input_mutation_directions(self):
        for path, value in [
            (("quota",), True),
            (("worlds", -1, "scale"), 5),
            (("chart", "U_scale"), 3),
            (("limits", "analysis_seconds"), 31),
        ]:
            changed = copy.deepcopy(self.protocol)
            set_path(changed, path, value)
            snapshot = {**self.snapshot, "protocol.json": json.dumps(changed).encode()}
            with (
                self.subTest(path=path),
                mock.patch.object(self.study, "source_snapshot", return_value=snapshot),
                mock.patch.object(
                    self.study,
                    "PROTOCOL_SHA256",
                    hashlib.sha256(snapshot["protocol.json"]).hexdigest(),
                ),
                mock.patch.object(
                    self.study,
                    "load_engine",
                    side_effect=AssertionError("invalid protocol executed"),
                ),
                self.assertRaises(ValueError),
            ):
                self.study.analyze()

        def corrupt(value):
            value["worlds"][-1]["scale"] = 5
            return copy.deepcopy(self.report)

        def type_corrupt(value):
            value["quota"] = Fraction(4)
            return copy.deepcopy(self.report)

        for bad in (corrupt, type_corrupt):
            for first, second in ((bad, lambda _p: self.report), (lambda _p: self.report, bad)):
                with (
                    self.subTest(corruption=bad.__name__, primary=first is bad),
                    self.assertRaises(ValueError),
                ):
                    self.compare(first, second)

    def test_source_bytes_change_and_fresh_blob_loading_ignore_module_cache(self):
        changed = copy.deepcopy(self.snapshot)
        changed["primary.py"] += b"\n"
        engine = type("Engine", (), {"analyze": staticmethod(lambda _p: self.report)})()
        with (
            mock.patch.object(self.study, "source_snapshot", side_effect=[self.snapshot, changed]),
            mock.patch.object(self.study, "load_engine", return_value=engine),
            self.assertRaises(ValueError),
        ):
            self.study.analyze()
        code = b"def analyze(value):\n    return {'seen': value['public']}\n"
        poison = type("Poison", (), {"analyze": staticmethod(lambda _p: "cached")})()
        with mock.patch.dict(sys.modules, {"primary": poison}):
            first = self.study.load_engine(code, "primary")
            second = self.study.load_engine(code, "primary")
        self.assertIsNot(first, second)
        self.assertEqual(first.analyze({"public": 3}), {"seen": 3})
        self.assertEqual(second.analyze({"public": 4}), {"seen": 4})

    def test_analysis_deadline_is_fail_closed_and_restores_timer(self):
        with (
            mock.patch.object(self.study.signal, "getsignal", return_value="prior-handler"),
            mock.patch.object(self.study.signal, "getitimer", return_value=(0.0, 0.0)),
            mock.patch.object(self.study.signal, "signal") as handler,
            mock.patch.object(self.study.signal, "setitimer") as timer,
            mock.patch.object(self.study.time, "monotonic", side_effect=[0.0, 31.0]),
            self.assertRaises(ValueError),
            self.study._analysis_deadline(),
        ):
            pass
        self.assertEqual(handler.call_count, 2)
        self.assertEqual(timer.call_args_list[-1].args[1], 0)
        prior = mock.Mock(side_effect=TimeoutError("outer suite deadline"))
        with (
            mock.patch.object(self.study.signal, "getsignal", return_value=prior),
            mock.patch.object(self.study.signal, "getitimer", return_value=(5.0, 0.0)),
            mock.patch.object(self.study.signal, "signal") as handler,
            mock.patch.object(self.study.signal, "setitimer") as timer,
            mock.patch.object(self.study.time, "monotonic", side_effect=[0.0, 2.0]),
            self.assertRaises(TimeoutError),
            self.study._analysis_deadline(),
        ):
            handler.call_args_list[0].args[1](self.study.signal.SIGALRM, None)
        prior.assert_called_once_with(self.study.signal.SIGALRM, None)
        self.assertEqual(timer.call_args_list[0].args[1], 5.0)
        self.assertEqual(timer.call_args_list[-1].args[1], 3.0)
        self.assertIs(handler.call_args_list[-1].args[1], prior)

    def test_prospective_protocol_byte_pin_precedes_parse_and_execution(self):
        altered = {**self.snapshot, "protocol.json": self.protocol_bytes + b"\n"}
        with (
            mock.patch.object(self.study, "source_snapshot", return_value=altered),
            mock.patch.object(
                self.study, "strict_loads", side_effect=AssertionError("unverified parse")
            ),
            mock.patch.object(
                self.study, "load_engine", side_effect=AssertionError("unverified execution")
            ),
            self.assertRaises(ValueError),
        ):
            self.study.analyze()


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.study = load_study()
        self.directory = tempfile.TemporaryDirectory(prefix="det8-qr05bm-evidence-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.freeze_path, self.capture_path = self.root / "freeze.json", self.root / "capture.json"
        self.snapshot = {
            "protocol.json": (HERE / "protocol.json").read_bytes(),
            "source.py": b"opaque source\n",
        }
        self.small = {"value": Fraction(1, 3), "count": 1, "flag": True}
        patcher = mock.patch.object(
            self.study, "source_snapshot", side_effect=lambda: copy.deepcopy(self.snapshot)
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.freeze_artifact = self.study.freeze(self.freeze_path)

    def capture(self, report=None):
        with mock.patch.object(
            self.study, "analyze", return_value=self.small if report is None else report
        ):
            return self.study.capture(self.capture_path, self.freeze_path)

    def replay(self, path=None, report=None):
        with mock.patch.object(
            self.study, "analyze", return_value=self.small if report is None else report
        ):
            return self.study.replay(path or self.capture_path, self.freeze_path)

    def test_create_only_canonical_artifacts_and_readonly_replay(self):
        self.assertEqual(self.freeze_artifact["schema"], "qr05bm-source-freeze-v1")
        self.assertEqual(self.freeze_artifact["sources"], self.study.identities(self.snapshot))
        self.assertEqual(self.study.canonical(self.freeze_artifact), self.freeze_path.read_bytes())
        self.assertEqual(self.capture(), self.small)
        saved = self.freeze_path.read_bytes(), self.capture_path.read_bytes()
        artifact = self.study.strict_loads(saved[1])
        self.assertEqual(set(artifact), {"schema", "sources", "freeze_sha256", "report"})
        self.assertEqual(artifact["freeze_sha256"], hashlib.sha256(saved[0]).hexdigest())
        exact_tree(self, self.study.decode(artifact["report"]), self.small)
        exact_tree(self, self.replay(), self.small)
        self.assertEqual((self.freeze_path.read_bytes(), self.capture_path.read_bytes()), saved)
        with self.assertRaises((ValueError, FileExistsError)):
            self.study.freeze(self.freeze_path)
        with self.assertRaises((ValueError, FileExistsError)):
            self.capture()
        self.assertEqual((self.freeze_path.read_bytes(), self.capture_path.read_bytes()), saved)

    def test_bounded_regular_reads_symlinks_and_output_cap(self):
        path = self.root / "small.json"
        path.write_bytes(b"{}")
        self.assertEqual(self.study.read_bounded(path, 2), b"{}")
        for limit in (0, -1, True, 1, self.study.ARTIFACT_LIMIT + 1):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                self.study.read_bounded(path, limit)
        for bad_path in (self.root, self.root / "absent"):
            with self.assertRaises(ValueError):
                self.study.read_bounded(bad_path)
        fifo = self.root / "pipe"
        os.mkfifo(fifo)
        with self.assertRaises(ValueError):
            self.study.read_bounded(fifo)
        symlink = self.root / "alias.json"
        symlink.symlink_to(path)
        with self.assertRaises(ValueError):
            self.study.read_bounded(symlink)
        dangling = self.root / "dangling.json"
        target = self.root / "not-created"
        dangling.symlink_to(target)
        with self.assertRaises((ValueError, FileExistsError)):
            self.study.capture(dangling, self.freeze_path)
        self.assertFalse(target.exists())
        with mock.patch.object(self.study, "ARTIFACT_LIMIT", 1), self.assertRaises(ValueError):
            self.study._write_new(self.root / "too-large", b"{}")
        self.assertFalse((self.root / "too-large").exists())

    def test_invalid_freeze_schema_runtime_identity_and_noncanonical_bytes(self):
        base = self.freeze_artifact
        changes = [None, [], {}, {**base, "extra": 1}, {**base, "schema": "wrong"}]
        for key in base:
            changed = copy.deepcopy(base)
            del changed[key]
            changes.append(changed)
        for path, value in [
            (("runtime", "implementation"), ""),
            (("runtime", "version"), 3),
            (("runtime", "optimization"), True),
            (("runtime", "optimization"), 3),
            (("sources", "source.py", "bytes"), True),
            (("sources", "source.py", "sha256"), "b" * 64),
        ]:
            changed = copy.deepcopy(base)
            set_path(changed, path, value)
            changes.append(changed)
        path = self.root / "bad-freeze.json"
        for index, changed in enumerate(changes):
            data = json.dumps(changed).encode()
            path.write_bytes(data)
            with self.subTest(case=index), self.assertRaises(ValueError):
                self.study.capture(self.root / "never-created", path)
            self.assertEqual(path.read_bytes(), data)
            self.assertFalse((self.root / "never-created").exists())
        path.write_bytes(self.freeze_path.read_bytes() + b"\n")
        with self.assertRaises(ValueError):
            self.study._checked_freeze(path, self.snapshot)

    def test_capture_header_tagged_values_and_noncanonical_bytes_refused(self):
        self.capture()
        data = self.capture_path.read_bytes()
        base = self.study.strict_loads(data)
        changes = [None, [], {}, {**base, "schema": "wrong"}, {**base, "extra": 1}]
        for key in base:
            changed = copy.deepcopy(base)
            del changed[key]
            changes.append(changed)
        for path, value in [
            (("freeze_sha256",), "b" * 64),
            (("sources", "source.py", "bytes"), True),
            (("report", "value"), {"$fraction": [2, 6]}),
            (("report", "value"), "1/3"),
            (("report", "count"), True),
            (("report", "flag"), 1),
        ]:
            changed = copy.deepcopy(base)
            set_path(changed, path, value)
            changes.append(changed)
        path = self.root / "bad-capture.json"
        for index, changed in enumerate(changes):
            blob = json.dumps(changed, sort_keys=True, separators=(",", ":")).encode() + b"\n"
            path.write_bytes(blob)
            with self.subTest(case=index), self.assertRaises(ValueError):
                self.replay(path)
            self.assertEqual(path.read_bytes(), blob)
        path.write_bytes(data + b"\n")
        with self.assertRaises(ValueError):
            self.replay(path)

    def test_source_and_freeze_changes_before_or_during_analysis_refused(self):
        self.snapshot["source.py"] += b"\n"
        with self.assertRaises(ValueError):
            self.capture()
        self.assertFalse(self.capture_path.exists())
        self.snapshot["source.py"] = b"opaque source\n"

        def source_change():
            self.snapshot["source.py"] += b"\n"
            return self.small

        with (
            mock.patch.object(self.study, "analyze", side_effect=source_change),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze_path)
        self.assertFalse(self.capture_path.exists())
        self.snapshot["source.py"] = b"opaque source\n"
        saved = self.freeze_path.read_bytes()

        def freeze_change():
            self.freeze_path.write_bytes(saved + b"\n")
            return self.small

        with (
            mock.patch.object(self.study, "analyze", side_effect=freeze_change),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze_path)
        self.assertFalse(self.capture_path.exists())

    def test_publication_and_replay_races_preserve_failed_bytes(self):
        write = self.study._write_new

        def corrupt(path, data):
            write(path, data)
            path.write_bytes(data + b"\n")

        with (
            mock.patch.object(self.study, "_write_new", side_effect=corrupt),
            self.assertRaises(ValueError),
        ):
            self.capture()
        bad = self.capture_path.read_bytes()
        with self.assertRaises((ValueError, FileExistsError)):
            self.capture()
        self.assertEqual(self.capture_path.read_bytes(), bad)
        second = self.root / "second.json"
        with mock.patch.object(self.study, "analyze", return_value=self.small):
            self.study.capture(second, self.freeze_path)
        saved = second.read_bytes()

        def replay_change():
            second.write_bytes(saved + b"\n")
            return self.small

        with (
            mock.patch.object(self.study, "analyze", side_effect=replay_change),
            self.assertRaises(ValueError),
        ):
            self.study.replay(second, self.freeze_path)
        self.assertEqual(second.read_bytes(), saved + b"\n")

    def test_failed_computation_does_not_publish_and_freeze_source_race(self):
        with (
            mock.patch.object(self.study, "analyze", side_effect=ValueError("analysis failure")),
            self.assertRaises(ValueError),
        ):
            self.study.capture(self.capture_path, self.freeze_path)
        self.assertFalse(self.capture_path.exists())
        changed = {**self.snapshot, "source.py": b"changed"}
        path = self.root / "second-freeze.json"
        with (
            mock.patch.object(self.study, "source_snapshot", side_effect=[self.snapshot, changed]),
            self.assertRaises(ValueError),
        ):
            self.study.freeze(path)
        self.assertFalse(path.exists())
        checks = 0

        def alter_after_publication(_snapshot):
            nonlocal checks
            checks += 1
            if checks == 2:
                path.write_bytes(path.read_bytes() + b"\n")

        with (
            mock.patch.object(self.study, "_check_snapshot", side_effect=alter_after_publication),
            self.assertRaises(ValueError),
        ):
            self.study.freeze(path)
        self.assertTrue(path.is_file())
        retained = path.read_bytes()
        with self.assertRaises((ValueError, FileExistsError)):
            self.study.freeze(path)
        self.assertEqual(path.read_bytes(), retained)

    def test_full_native_report_replay_mutations_in_memory(self):
        _study, _protocol, report = evaluated()
        self.capture(report)
        original_bytes = self.capture_path.read_bytes()
        artifact = self.study.strict_loads(original_bytes)
        parse = self.study.strict_loads
        count = 0
        for path, changed in representative_mutations(report):
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    self.study.require_equal(changed, report)
                bad = copy.deepcopy(artifact)
                bad["report"] = self.study.encode(changed)
                # Feed canonical changed evidence to the reader, not a noncanonical
                # shortcut: the failure must reach native report comparison.
                bad_bytes = self.study.canonical(bad)
                reader = self.study.read_bounded

                def read(candidate, limit=None, blob=bad_bytes, original=reader):
                    if Path(candidate) == self.capture_path:
                        return blob
                    return original(candidate) if limit is None else original(candidate, limit)

                with (
                    mock.patch.object(self.study, "read_bounded", side_effect=read),
                    self.assertRaises(ValueError),
                ):
                    self.replay(report=report)
                self.assertEqual(self.capture_path.read_bytes(), original_bytes)
                count += 1
        self.assertGreater(count, 35)
        self.assertEqual(self.study.strict_loads(original_bytes), parse(original_bytes))


class SourceTests(unittest.TestCase):
    def test_exact_eight_source_snapshot_and_frozen_identities(self):
        study = load_study()
        expected_names = {
            "README.md",
            "protocol.json",
            "primary.py",
            "reference.py",
            "study.py",
            "test_qr05bm.py",
            "../qr-05bl-relative-volume-design-2026-09-09/README.md",
            "../qr-05bl-relative-volume-design-2026-09-09/RESULTS.md",
        }
        self.assertEqual(set(study.SOURCE_PATHS), expected_names)
        self.assertEqual(len(study.SOURCE_PATHS), 8)
        snapshot = study.source_snapshot()
        self.assertEqual(set(snapshot), expected_names)
        for name, data in snapshot.items():
            self.assertIs(type(data), bytes)
            self.assertEqual(data, (HERE / name).read_bytes())
            self.assertLessEqual(len(data), 262144)
        identities = study.identities(snapshot)
        self.assertEqual(
            identities,
            {
                name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                for name, data in snapshot.items()
            },
        )
        freeze = study.strict_loads(study.read_bounded(HERE / "source-freeze.json"))
        self.assertEqual(freeze["sources"], identities)

    def test_source_snapshot_applies_source_not_artifact_limit(self):
        study = load_study()
        with mock.patch.object(study, "read_bounded", return_value=b"source") as reader:
            self.assertEqual(set(study.source_snapshot()), set(study.SOURCE_PATHS))
        self.assertEqual(len(reader.call_args_list), 8)
        for call in reader.call_args_list:
            self.assertEqual(call.args[1], 262144)


def main():
    """Enforce the separately declared complete-suite wall-time budget."""
    import signal
    import time

    def expired(_signum, _frame):
        # unittest re-raises KeyboardInterrupt instead of recording an error
        # and continuing after the one-shot timer has expired.
        raise KeyboardInterrupt("120-second BM test-suite bound exceeded")

    previous = signal.signal(signal.SIGALRM, expired)
    old_timer = signal.setitimer(signal.ITIMER_REAL, 120)
    started = time.monotonic()
    try:
        unittest.main()
    finally:
        elapsed = time.monotonic() - started
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
        if old_timer[0] > 0:
            signal.setitimer(
                signal.ITIMER_REAL, max(0.000001, old_timer[0] - elapsed), old_timer[1]
            )


if __name__ == "__main__":
    main()
