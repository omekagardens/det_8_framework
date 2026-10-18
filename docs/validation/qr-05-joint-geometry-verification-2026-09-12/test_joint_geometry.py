"""Independent finite-world oracle, API boundaries and source-bound evidence tests.

Prospective source: do not execute before the first complete source freeze.
The oracle uses the design's explicit integral table, not either engine's
quadrature or chronology implementation. No engine is imported by this file
until a test explicitly loads authenticated snapshot bytes.
"""

import copy
import hashlib
import importlib.util
import itertools
import json
import signal
import tempfile
import types
import unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
CHANNELS = ["O", "P", "T", "D", "R"]
WORLD_KEYS = ("kappa", "orientation", "a", "b", "L", "r")


def load_study():
    spec = importlib.util.spec_from_file_location("joint_geometry_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load source-bound joint-geometry driver")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def context():
    """One full two-route mathematical analysis per suite, never per test."""
    study = load_study()
    snapshot = study.source_snapshot()
    protocol = study._protocol(snapshot)
    return study, snapshot, protocol, study.analyze(snapshot)


def exact(test, actual, expected, path="report"):
    """Independent native comparison: Fraction/int/bool/list distinctions matter."""
    test.assertIs(type(actual), type(expected), path)
    if type(expected) is dict:
        test.assertEqual(set(actual), set(expected), path)
        for key in expected:
            exact(test, actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        test.assertEqual(len(actual), len(expected), path)
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            exact(test, left, right, f"{path}[{index}]")
    else:
        test.assertIn(type(expected), (str, int, bool, F), path)
        test.assertEqual(actual, expected, path)


def signature(value):
    """Injective native-value key, with no world label or hidden coordinate input."""
    if type(value) is F:
        return ("fraction", value.numerator, value.denominator)
    if type(value) is int:
        return ("int", value)
    if type(value) is list:
        return ("list", tuple(signature(item) for item in value))
    if type(value) is dict:
        return ("dict", tuple((key, signature(value[key])) for key in sorted(value)))
    raise ValueError("not a native observation or target value")


def fixed_worlds():
    values = ([1, 2], [-1, 1], [0, 1], [0, 1], [F(1), F(3, 2)], [F(1), F(2, 3)])
    return [dict(zip(WORLD_KEYS, parts, strict=True)) for parts in itertools.product(*values)]


def world_key(world):
    return tuple(world[name] for name in WORLD_KEYS)


def expected_row(world):
    """Third route: the four analytical integrals and two geometric cases."""
    table = {
        (0, 0): (F(1), F(1, 2)),
        (0, 1): (F(3, 2), F(5, 12)),
        (1, 0): (F(3, 2), F(5, 12)),
        (1, 1): (F(7, 3), F(19, 56)),
    }
    kappa, orientation, a, b, scale, rate = (world[name] for name in WORLD_KEYS)
    normalizer, probability = table[a, b]
    causal = [orientation, orientation if kappa == 1 else 0]
    proper = F(kappa) * scale
    intensity = proper * rate
    total = intensity * normalizer
    return {
        "world": dict(world),
        "channels": {"O": list(causal), "P": probability, "T": total, "D": b, "R": rate},
        "target": {
            "O": list(causal),
            "relative_volume": {0: F(1, 2), 1: F(5, 12)}[a],
            "volume": proper * {0: F(1), 1: F(3, 2)}[a],
        },
        "geometry_coefficients": [proper, proper * a],
        "intensity_coefficients": [intensity, intensity * (a + b), intensity * a * b],
        "point_density_coefficients": [
            F(1) / normalizer,
            F(a + b) / normalizer,
            F(a * b) / normalizer,
        ],
        "Z": normalizer,
        "recovered": dict(world),
        "fisher": [[total, total], [total, total]],
    }


@lru_cache(maxsize=1)
def full_oracle():
    """Retain all raw rows, full fibers, fiber targets and every obstruction."""
    rows = [{"id": f"w{i:03d}", **expected_row(world)} for i, world in enumerate(fixed_worlds())]
    menus = [list(menu) for size in range(6) for menu in itertools.combinations(CHANNELS, size)]
    obstructions = []
    for left, right in itertools.combinations(rows, 2):
        if signature(left["target"]) != signature(right["target"]):
            obstructions.append(
                {
                    "worlds": [left["id"], right["id"]],
                    "separators": [
                        name
                        for name in CHANNELS
                        if signature(left["channels"][name]) != signature(right["channels"][name])
                    ],
                }
            )
    partitions = []
    by_id = {row["id"]: row for row in rows}
    for menu in menus:
        unseen = list(range(len(rows)))
        blocks = []
        while unseen:
            first = rows[unseen[0]]
            indices = [
                i
                for i in unseen
                if all(
                    signature(first["channels"][name]) == signature(rows[i]["channels"][name])
                    for name in menu
                )
            ]
            blocks.append([rows[i]["id"] for i in indices])
            chosen = set(indices)
            unseen = [i for i in unseen if i not in chosen]
        targets = []
        for block in blocks:
            seen = set()
            values = []
            for name in block:
                target = by_id[name]["target"]
                key = signature(target)
                if key not in seen:
                    seen.add(key)
                    values.append(copy.deepcopy(target))
            targets.append(values)
        partitions.append(
            {
                "selected": list(menu),
                "blocks": blocks,
                "targets": targets,
                "identifying": all(set(menu) & set(pair["separators"]) for pair in obstructions),
            }
        )
    good = [row["selected"] for row in partitions if row["identifying"]]
    minimal = [menu for menu in good if not any(set(other) < set(menu) for other in good)]
    minimum = min((len(menu) for menu in good), default=None)
    lookup = {world_key(row["world"]): row["id"] for row in rows}

    def identifier(kappa, orientation, a, b, scale, rate):
        return lookup[kappa, orientation, a, b, F(scale), F(rate)]

    origin = (1, 1, 0, 0, F(1), F(1))
    omission_pairs = [
        ("O", origin, (1, -1, 0, 0, F(1), F(1))),
        ("P", (1, 1, 0, 0, F(3, 2), F(1)), (1, 1, 1, 0, F(1), F(1))),
        ("T", origin, (1, 1, 0, 0, F(3, 2), F(1))),
        ("D", (1, 1, 1, 0, F(1), F(1)), (1, 1, 0, 1, F(1), F(1))),
        ("R", origin, (1, 1, 0, 0, F(3, 2), F(2, 3))),
    ]
    omissions = [
        {"omitted": name, "worlds": [identifier(*left), identifier(*right)]}
        for name, left, right in omission_pairs
    ]
    collisions = []
    for kappa, orientation in itertools.product([1, 2], [-1, 1]):
        ids = [
            identifier(kappa, orientation, a, b, scale, rate)
            for a, b in ((1, 0), (0, 1))
            for scale, rate in ((F(1), F(1)), (F(3, 2), F(2, 3)))
        ]
        collisions.append({"kappa": kappa, "orientation": orientation, "worlds": ids})
    return {
        "schema": "qr05-joint-geometry-report-v1",
        "channels": list(CHANNELS),
        "worlds": rows,
        "partitions": partitions,
        "minimal_identifying_sets": minimal,
        "minimum_size": [] if minimum is None else [minimum],
        "minimum_identifying_sets": [menu for menu in good if len(menu) == minimum],
        "obstructions": obstructions,
        "omission_witnesses": omissions,
        "collision_groups": collisions,
    }


def alphabet_packet(rows):
    """First-occurrence alphabets depend only on each channel's actual values."""
    alphabets = {name: {} for name in CHANNELS}
    target_alphabet = {}
    encoded = []
    for row in rows:
        observation = []
        for name in CHANNELS:
            value_key = signature(row["channels"][name])
            alphabet = alphabets[name]
            if value_key not in alphabet:
                alphabet[value_key] = len(alphabet)
            observation.append(alphabet[value_key])
        target_key = signature(row["target"])
        if target_key not in target_alphabet:
            target_alphabet[target_key] = len(target_alphabet)
        encoded.append(
            {"id": row["id"], "observations": observation, "target": [target_alphabet[target_key]]}
        )
    return {"channels": list(CHANNELS), "rows": encoded}


class JointGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.snapshot, cls.protocol, cls.report = context()

    def engines(self):
        for name in ("primary.py", "reference.py"):
            yield name, self.study.load_engine(self.snapshot[name], name)

    def test_complete_independent_raw_native_report(self):
        exact(self, self.report, full_oracle())
        encoded = self.study.encode(self.report)
        decoded = self.study.decode(self.study.strict_loads(self.study.canonical(encoded)))
        exact(self, decoded, self.report)

    def test_fixed_world_target_menu_and_pair_census(self):
        rows = self.report["worlds"]
        self.assertEqual([row["id"] for row in rows], [f"w{i:03d}" for i in range(64)])
        exact(self, [row["world"] for row in rows], fixed_worlds())
        targets = {}
        for row in rows:
            key = signature(row["target"])
            targets[key] = targets.get(key, 0) + 1
        self.assertEqual(len(targets), 16)
        self.assertEqual(set(targets.values()), {4})
        self.assertEqual(len(self.report["partitions"]), 32)
        self.assertEqual(len(self.report["obstructions"]), 1920)
        exact(self, self.report["minimal_identifying_sets"], [CHANNELS])
        exact(self, self.report["minimum_identifying_sets"], [CHANNELS])
        exact(self, self.report["minimum_size"], [5])
        self.assertEqual(sum(row["identifying"] for row in self.report["partitions"]), 1)

    def test_injective_value_alphabets_agree_with_frozen_quotient(self):
        packet = alphabet_packet(self.report["worlds"])
        for i, j in itertools.combinations(range(len(packet["rows"])), 2):
            for k, name in enumerate(CHANNELS):
                self.assertEqual(
                    signature(self.report["worlds"][i]["channels"][name])
                    == signature(self.report["worlds"][j]["channels"][name]),
                    packet["rows"][i]["observations"][k] == packet["rows"][j]["observations"][k],
                )
            self.assertEqual(
                signature(self.report["worlds"][i]["target"])
                == signature(self.report["worlds"][j]["target"]),
                packet["rows"][i]["target"] == packet["rows"][j]["target"],
            )
        quotient = self.study.load_engine(
            self.snapshot[self.study.QUOTIENT_SOURCE], "pinned_quotient"
        )
        supplied = copy.deepcopy(packet)
        computed = quotient.analyze(supplied)
        exact(self, supplied, packet)
        projected = {
            name: copy.deepcopy(self.report[name])
            for name in (
                "channels",
                "minimal_identifying_sets",
                "minimum_size",
                "minimum_identifying_sets",
                "obstructions",
            )
        }
        projected["partitions"] = [
            {name: copy.deepcopy(row[name]) for name in ("selected", "blocks", "identifying")}
            for row in self.report["partitions"]
        ]
        exact(self, computed, projected)

    def test_every_fiber_target_set_and_all_refinements(self):
        by_id = {row["id"]: row for row in self.report["worlds"]}
        partial_constant = False
        for coarse in self.report["partitions"]:
            self.assertEqual(len(coarse["blocks"]), len(coarse["targets"]))
            for block, targets in zip(coarse["blocks"], coarse["targets"], strict=True):
                expected = []
                for identifier in block:
                    candidate = by_id[identifier]["target"]
                    if not any(signature(candidate) == signature(old) for old in expected):
                        expected.append(candidate)
                exact(self, targets, expected)
                if not coarse["identifying"] and len(targets) == 1:
                    partial_constant = True
            self.assertIs(coarse["identifying"], all(len(t) == 1 for t in coarse["targets"]))
            for fine in self.report["partitions"]:
                if set(coarse["selected"]) <= set(fine["selected"]):
                    for block in fine["blocks"]:
                        self.assertTrue(
                            any(set(block) <= set(parent) for parent in coarse["blocks"])
                        )
                    if coarse["identifying"]:
                        self.assertTrue(fine["identifying"])
            unhit = [
                pair
                for pair in self.report["obstructions"]
                if not set(pair["separators"]) & set(coarse["selected"])
            ]
            self.assertIs(coarse["identifying"], not unhit)
        self.assertTrue(partial_constant, "global failure must not erase target-constant fibers")

    def test_all_five_exact_omission_witnesses(self):
        exact(self, self.report["omission_witnesses"], full_oracle()["omission_witnesses"])
        by_id = {row["id"]: row for row in self.report["worlds"]}
        for witness in self.report["omission_witnesses"]:
            left, right = [by_id[name] for name in witness["worlds"]]
            omitted = witness["omitted"]
            for name in CHANNELS:
                if name != omitted:
                    exact(self, left["channels"][name], right["channels"][name])
            self.assertNotEqual(
                signature(left["channels"][omitted]), signature(right["channels"][omitted])
            )
            self.assertNotEqual(signature(left["target"]), signature(right["target"]))
            if omitted == "P":
                exact(self, left["target"]["volume"], right["target"]["volume"])
                self.assertNotEqual(
                    left["target"]["relative_volume"], right["target"]["relative_volume"]
                )

    def test_simultaneous_four_world_record_law_collisions(self):
        exact(self, self.report["collision_groups"], full_oracle()["collision_groups"])
        by_id = {row["id"]: row for row in self.report["worlds"]}
        for group in self.report["collision_groups"]:
            rows = [by_id[name] for name in group["worlds"]]
            self.assertEqual(len(rows), 4)
            self.assertEqual(len({signature(row["target"]) for row in rows}), 4)
            for row in rows:
                exact(
                    self,
                    row["intensity_coefficients"],
                    [F(group["kappa"]), F(group["kappa"]), F(0)],
                )
                for field in ("intensity_coefficients", "point_density_coefficients"):
                    exact(self, row[field], rows[0][field])
                for name in ("O", "P", "T"):
                    exact(self, row["channels"][name], rows[0]["channels"][name])
                exact(self, row["channels"]["P"], F(5, 12))
                exact(self, row["channels"]["T"], F(3 * group["kappa"], 2))

    def test_known_integrals_and_coefficient_moments(self):
        for row in self.report["worlds"]:
            geometry, intensity, density = [
                row[key]
                for key in (
                    "geometry_coefficients",
                    "intensity_coefficients",
                    "point_density_coefficients",
                )
            ]
            integrate = lambda coefficients, bound: sum(
                (
                    coefficient * bound ** (power + 1) / F(power + 1)
                    for power, coefficient in enumerate(coefficients)
                ),
                F(0),
            )
            exact(self, integrate(geometry, F(1)), row["target"]["volume"])
            exact(
                self,
                integrate(geometry, F(1, 2)) / integrate(geometry, F(1)),
                row["target"]["relative_volume"],
            )
            exact(self, integrate(intensity, F(1)), row["channels"]["T"])
            exact(self, integrate(density, F(1)), F(1))
            exact(self, integrate(density, F(1, 2)), row["channels"]["P"])

    def test_fresh_engine_evaluate_and_joint_recovery_all_fixed_worlds(self):
        for name, engine in self.engines():
            for world in fixed_worlds():
                with self.subTest(engine=name, world=world_key(world)):
                    supplied = dict(world)
                    row = engine.evaluate(supplied)
                    exact(self, row, expected_row(world))
                    exact(self, supplied, world)
                    channels = copy.deepcopy(row["channels"])
                    exact(self, engine.recover(channels), world)
                    exact(self, channels, row["channels"])

    def test_scale_compensation_c_three_halves(self):
        multiplier = F(3, 2)
        for name, engine in self.engines():
            for world in fixed_worlds():
                altered = {**world, "L": world["L"] * multiplier, "r": world["r"] / multiplier}
                row, changed = engine.evaluate(dict(world)), engine.evaluate(dict(altered))
                with self.subTest(engine=name, world=world_key(world)):
                    exact(self, changed, expected_row(altered))
                    for field in ("intensity_coefficients", "point_density_coefficients"):
                        exact(self, row[field], changed[field])
                    for channel in ("O", "P", "T", "D"):
                        exact(self, row["channels"][channel], changed["channels"][channel])
                    exact(self, changed["channels"]["R"], row["channels"]["R"] / multiplier)
                    exact(
                        self, changed["target"]["relative_volume"], row["target"]["relative_volume"]
                    )
                    exact(self, changed["target"]["volume"], row["target"]["volume"] * multiplier)
                    exact(self, engine.recover(changed["channels"]), altered)

    def test_fisher_rank_one_null_direction_and_repetitions(self):
        for row in self.report["worlds"]:
            information, total = row["fisher"], row["channels"]["T"]
            self.assertGreater(total, 0)
            exact(self, information, [[total, total], [total, total]])
            for repetitions in (1, 3):
                repeated = [[repetitions * entry for entry in line] for line in information]
                exact(self, [line[0] - line[1] for line in repeated], [F(0), F(0)])
                exact(self, repeated[0][0] * repeated[1][1] - repeated[0][1] * repeated[1][0], F(0))
                self.assertGreater(sum(repeated[0]), 0)

    def test_chronology_probes_reversal_incomparable_equal_and_null(self):
        A, B, C = [F(1, 8), F(1, 8)], [F(7, 8), F(1, 8)], [F(7, 8), F(5, 8)]
        null_left, null_right = [F(1, 4), F(1, 4)], [F(3, 4), F(3, 4)]
        for name, engine in self.engines():
            for kappa, orientation in itertools.product((1, 2), (-1, 1)):
                for left, right, expected in (
                    (A, B, orientation),
                    (B, A, -orientation),
                    (A, C, orientation if kappa == 1 else 0),
                    (C, A, -orientation if kappa == 1 else 0),
                    (B, C, 0),
                    (A, A, 0),
                    (null_left, null_right, 0),
                    (null_right, null_left, 0),
                ):
                    with self.subTest(
                        engine=name, kappa=kappa, orientation=orientation, left=left, right=right
                    ):
                        original = copy.deepcopy([left, right])
                        exact(self, engine.chronological(kappa, orientation, left, right), expected)
                        exact(self, [left, right], original)

    def test_world_native_refusals_and_derived_overflow(self):
        class DictSubclass(dict):
            pass

        class IntSubclass(int):
            pass

        class FractionSubclass(F):
            pass

        world = fixed_worlds()[0]
        bad = [
            None,
            [],
            DictSubclass(world),
            {**world, "extra": 0},
            {key: value for key, value in world.items() if key != "L"},
        ]
        for field, values in (
            ("kappa", [True, F(1), 1.0, IntSubclass(1), 0, 3]),
            ("orientation", [True, F(1), 1.0, 0, 2]),
            ("a", [False, F(0), 0.0, -1, 2]),
            ("b", [False, F(0), 0.0, -1, 2]),
            ("L", [1, True, 1.0, F(0), F(-1), FractionSubclass(1), F(2**128), F(1, 2**128)]),
            ("r", [1, True, 1.0, F(0), F(-1), FractionSubclass(1), F(2**128), F(1, 2**128)]),
        ):
            bad.extend({**world, field: value} for value in values)
        bad.append({**world, "L": F(2**127), "r": F(2**127)})
        for name, engine in self.engines():
            for scale in (F(2**127), F(1, 2**127)):
                boundary = {
                    "kappa": 1,
                    "orientation": 1,
                    "a": 0,
                    "b": 0,
                    "L": scale,
                    "r": F(1),
                }
                with self.subTest(engine=name, accepted_boundary=scale):
                    supplied = dict(boundary)
                    evaluated = engine.evaluate(supplied)
                    exact(self, evaluated, expected_row(boundary))
                    exact(self, engine.recover(evaluated["channels"]), boundary)
                    exact(self, supplied, boundary)
            for changed in bad:
                with (
                    self.subTest(engine=name, value=repr(changed)[:120]),
                    self.assertRaises(ValueError),
                ):
                    engine.evaluate(changed)

    def test_channel_image_type_shape_and_recovered_overflow_refusals(self):
        class DictSubclass(dict):
            pass

        class ListSubclass(list):
            pass

        class IntSubclass(int):
            pass

        class FractionSubclass(F):
            pass

        channels = expected_row(fixed_worlds()[0])["channels"]
        bad = [
            None,
            [],
            DictSubclass(channels),
            {**channels, "extra": 0},
            {key: value for key, value in channels.items() if key != "R"},
        ]
        for field, values in (
            (
                "O",
                [
                    None,
                    (),
                    [-1],
                    [-1, -1, 0],
                    [0, 0],
                    [1, -1],
                    [True, 1],
                    [F(-1), -1],
                    ListSubclass([-1, -1]),
                ],
            ),
            ("P", [F(1, 3), 0.5, 1, True, FractionSubclass(1, 2)]),
            ("T", [1, True, 1.0, F(0), F(-1), FractionSubclass(1), F(2**128), F(1, 2**128)]),
            ("D", [False, F(0), 0.0, IntSubclass(0), -1, 2]),
            ("R", [1, True, 1.0, F(0), F(-1), FractionSubclass(1), F(2**128), F(1, 2**128)]),
        ):
            bad.extend({**channels, field: value} for value in values)
        bad.extend(
            [
                {**channels, "P": F(1, 2), "D": 1},
                {**channels, "P": F(19, 56), "D": 0},
                {"O": [1, 1], "P": F(1, 2), "T": F(2**127), "D": 0, "R": F(1, 2**127)},
            ]
        )
        for name, engine in self.engines():
            for changed in bad:
                with (
                    self.subTest(engine=name, value=repr(changed)[:120]),
                    self.assertRaises(ValueError),
                ):
                    engine.recover(changed)

    def test_chronology_native_input_refusals(self):
        class ListSubclass(list):
            pass

        class FractionSubclass(F):
            pass

        point = [F(1, 4), F(1, 4)]
        invalid_points = [
            None,
            (),
            [F(0)],
            [F(0)] * 3,
            [0, F(0)],
            [True, F(0)],
            [0.0, F(0)],
            [F(-1), F(0)],
            [F(0), F(2)],
            [F(1, 2**128), F(0)],
            [FractionSubclass(1, 4), F(0)],
            ListSubclass(point),
        ]
        for name, engine in self.engines():
            for kappa, orientation in (
                (True, 1),
                (F(1), 1),
                (1.0, 1),
                (0, 1),
                (3, 1),
                (1, True),
                (1, F(1)),
                (1, 1.0),
                (1, 0),
                (1, 2),
            ):
                with (
                    self.subTest(engine=name, kappa=kappa, orientation=orientation),
                    self.assertRaises(ValueError),
                ):
                    engine.chronological(kappa, orientation, point, point)
            for changed in invalid_points:
                for left, right in ((changed, point), (point, changed)):
                    with (
                        self.subTest(engine=name, value=repr(changed)),
                        self.assertRaises(ValueError),
                    ):
                        engine.chronological(1, 1, left, right)

    def test_pure_functions_fresh_results_and_no_mutable_input_aliases(self):
        world = fixed_worlds()[0]
        for name, engine in self.engines():
            supplied = dict(world)
            with mock.patch("builtins.open", side_effect=AssertionError("pure API performed I/O")):
                first = engine.evaluate(supplied)
                recovered = engine.recover(copy.deepcopy(first["channels"]))
            self.assertIsNot(first["world"], supplied, name)
            first["world"]["a"] = 1
            first["channels"]["O"][0] = 999
            first["target"]["O"][0] = 999
            recovered["a"] = 1
            exact(self, supplied, world)
            exact(self, engine.evaluate(dict(world)), expected_row(world))
            channels = copy.deepcopy(expected_row(world)["channels"])
            result = engine.recover(channels)
            result["a"] = 1
            exact(self, channels, expected_row(world)["channels"])


class EvidenceTests(unittest.TestCase):
    def test_ten_sources_are_bounded_bytes_and_all_pins_precede_parse(self):
        study = load_study()
        snapshot = study.source_snapshot()
        self.assertEqual(len(study.SOURCE_PATHS), 10)
        self.assertEqual(set(snapshot), set(study.SOURCE_PATHS))
        for name, blob in snapshot.items():
            self.assertIs(type(blob), bytes, name)
            self.assertLessEqual(len(blob), 262144, name)
        for name in ["protocol.json", *study.DEPENDENCY_PINS]:
            changed = {**snapshot, name: snapshot[name] + b"\n"}
            with (
                self.subTest(source=name),
                mock.patch.object(study, "strict_loads", side_effect=AssertionError("early parse")),
                self.assertRaises(ValueError),
            ):
                study._protocol(changed)

    def test_utility_loader_rejects_untrusted_nonregular_and_oversize_sources(self):
        study = load_study()
        with tempfile.TemporaryDirectory(prefix="qr05-joint-utility-") as directory:
            root = Path(directory)
            untrusted = root / "probe.py"
            untrusted.write_bytes(b"raise AssertionError('untrusted execution')\n")
            oversize = root / "oversize.py"
            oversize.write_bytes(b" " * (study.SOURCE_LIMIT + 1))
            link = root / "linked.py"
            link.symlink_to(untrusted)
            for path in (untrusted, oversize, link, root, root / "missing.py"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    study._load_utilities(path)

    def test_strict_codec_and_native_type_mismatches(self):
        study = load_study()
        value = {"fraction": F(1), "integer": 1, "boolean": True, "empty": []}
        exact(self, study.decode(study.strict_loads(study.canonical(study.encode(value)))), value)
        for left, right in ((True, 1), (F(1), 1), ([], ()), ({"x": 1}, {"x": 1, "y": 0})):
            with self.assertRaises(ValueError):
                study.require_equal(left, right)
        for blob in (b'{"x":1,"x":2}', b'{"x":1.0}', b'{"x":NaN}'):
            with self.assertRaises(ValueError):
                study.strict_loads(blob)

    def test_authenticated_synthetic_roundtrip_exclusive_and_bound(self):
        study = load_study()
        synthetic = {"fraction": F(1, 3), "flag": True, "value": 1, "rows": []}
        with tempfile.TemporaryDirectory(prefix="qr05-joint-evidence-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            with mock.patch.object(study, "analyze", return_value=synthetic):
                artifact = study.freeze(freeze)
                self.assertEqual(artifact["schema"], "qr05-joint-geometry-source-freeze-v1")
                self.assertEqual(len(artifact["sources"]), 10)
                exact(self, study.capture(capture, freeze), synthetic)
                exact(self, study.replay(capture, freeze), synthetic)
                for operation, path in (
                    (study.freeze, freeze),
                    (lambda target: study.capture(target, freeze), capture),
                ):
                    with self.assertRaises(FileExistsError):
                        operation(path)
                original = capture.read_bytes()
                decoded = json.loads(original)
                self.assertEqual(decoded["schema"], "qr05-joint-geometry-capture-v1")
                decoded["report"]["value"] = True
                capture.write_bytes(study.canonical(decoded))
                with self.assertRaises(ValueError):
                    study.replay(capture, freeze)
                capture.write_bytes(original)
                frozen = freeze.read_bytes()
                freeze.write_bytes(frozen + b"\n")
                with self.assertRaises(ValueError):
                    study.replay(capture, freeze)
                freeze.write_bytes(frozen)
                decoded = json.loads(original)
                decoded["freeze_sha256"] = "0" * 64
                capture.write_bytes(study.canonical(decoded))
                with self.assertRaises(ValueError):
                    study.replay(capture, freeze)

    def test_source_freeze_schema_identity_and_runtime_refusals(self):
        study = load_study()
        snapshot = study.source_snapshot()
        with tempfile.TemporaryDirectory(prefix="qr05-joint-freeze-") as directory:
            path = Path(directory) / "freeze.json"
            study.freeze(path)
            original = json.loads(path.read_bytes())
            bad = []
            for field, value in (("schema", "wrong"), ("sources", {}), ("extra", 1)):
                bad.append({**original, field: value})
            for field, value in (
                ("optimization", True),
                ("optimization", 3),
                ("version", ""),
                ("implementation", []),
            ):
                bad.append({**original, "runtime": {**original["runtime"], field: value}})
            for changed in bad:
                path.write_bytes(study.canonical(changed))
                with self.subTest(value=changed), self.assertRaises(ValueError):
                    study._checked_freeze(path, snapshot)

    def test_first_capture_full_native_identity_without_another_analysis(self):
        study, snapshot, _, report = context()
        frozen = study._checked_freeze(HERE / "source-freeze.json", snapshot)
        data = study.read_bounded(HERE / "results.json")
        artifact = study.strict_loads(data)
        self.assertEqual(set(artifact), {"schema", "sources", "freeze_sha256", "report"})
        self.assertEqual(artifact["schema"], "qr05-joint-geometry-capture-v1")
        self.assertEqual(study.canonical(artifact), data)
        study.require_equal(artifact["sources"], study.identities(snapshot))
        self.assertEqual(artifact["freeze_sha256"], hashlib.sha256(frozen).hexdigest())
        exact(self, study.decode(artifact["report"]), report)

    def test_route_mismatch_and_late_source_change_refuse(self):
        study, snapshot, _, report = context()
        changed = copy.deepcopy(report)
        changed["worlds"][0]["channels"]["T"] = int(changed["worlds"][0]["channels"]["T"])
        left = types.SimpleNamespace(analyze=lambda: copy.deepcopy(report))
        right = types.SimpleNamespace(analyze=lambda: copy.deepcopy(changed))
        with (
            mock.patch.object(study, "load_engine", side_effect=[left, right]),
            self.assertRaises(ValueError),
        ):
            study.analyze(snapshot)
        drifted = {**snapshot, "primary.py": snapshot["primary.py"] + b"\n"}
        with (
            mock.patch.object(study, "load_engine", side_effect=[left, left]),
            mock.patch.object(study, "source_snapshot", return_value=drifted),
            self.assertRaises(ValueError),
        ):
            study.analyze(snapshot)

    def test_capture_rechecks_freeze_after_analysis_and_output_after_publish(self):
        study = load_study()
        synthetic = {"value": F(1)}
        with tempfile.TemporaryDirectory(prefix="qr05-joint-race-") as directory:
            root = Path(directory)
            freeze, capture = root / "freeze.json", root / "capture.json"
            study.freeze(freeze)
            original_freeze = freeze.read_bytes()

            def mutate_freeze(_snapshot):
                freeze.write_bytes(original_freeze + b"\n")
                return synthetic

            with (
                mock.patch.object(study, "analyze", side_effect=mutate_freeze),
                self.assertRaises(ValueError),
            ):
                study.capture(capture, freeze)
            self.assertFalse(capture.exists())
            freeze.write_bytes(original_freeze)
            actual_write = study._write_new

            def alter_after_write(path, blob):
                actual_write(path, blob)
                Path(path).write_bytes(blob + b"\n")

            with (
                mock.patch.object(study, "analyze", return_value=synthetic),
                mock.patch.object(study, "_write_new", side_effect=alter_after_write),
                self.assertRaises(ValueError),
            ):
                study.capture(capture, freeze)


if __name__ == "__main__":

    def expired(_signum, _frame):
        raise KeyboardInterrupt("60-second joint-geometry suite deadline")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 60)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
