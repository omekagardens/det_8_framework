"""Independent fixed-table oracles and bounded evidence lifecycle checks."""

import itertools
import tempfile
import unittest
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch

import study

TABLE = {
    ("a", 0): [3, 4, 5, 6, 7, 8, 0, 1, 2],
    ("a", 1): [0, 1, 2, 6, 7, 8, 3, 4, 5],
    ("b", 0): [1, 2, 0, 4, 5, 3, 7, 8, 6],
    ("b", 1): [0, 2, 1, 3, 5, 4, 6, 8, 7],
    ("ab", 0): [0, 3, 6, 1, 4, 7, 2, 5, 8],
    ("ab", 1): [0, 1, 2, 4, 5, 3, 8, 6, 7],
}


class Mathematics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = study.snapshot()
        cls.engines = study.routes(cls.sources)
        cls.report = study.analyze(cls.sources)

    def test_fixed_census_and_exact_types(self):
        rows = self.report["rows"]
        self.assertEqual(len(rows), 260)
        self.assertEqual(
            [sum(len(row["history"]) == n for row in rows) for n in range(5)], [1, 6, 36, 216, 1]
        )
        self.assertEqual(len({row["case"] for row in rows}), 260)
        self.assertEqual(
            rows[-1]["history"], [[0, "ab", 0], [1, "a", 0], [2, "b", 0], [3, "ab", 0]]
        )
        for row in rows:
            self.assertIs(type(row["result"]["weight"]), F)
            self.assertEqual(row["result"]["weight"], F(1, 6 ** len(row["history"])))

    def test_complete_order_record_and_matrix_unit_oracle(self):
        for row in self.report["rows"]:
            history, result = row["history"], row["result"]
            relation = {
                (u, v)
                for position, (v, action, _) in enumerate(history)
                for u, prior, _ in history[:position]
                if set(prior) & set(action)
            }
            while True:
                extended = relation | {
                    (u, w) for u, v in relation for mid, w in relation if v == mid
                }
                if extended == relation:
                    break
                relation = extended
            self.assertEqual(result["order"], [list(edge) for edge in sorted(relation)])
            self.assertEqual(result["events"], sorted(event for event, _, _ in history))
            outcomes = {event: bit for event, _, bit in history}
            records = []
            permutation = list(range(9))
            for event, action, bit in history:
                past = {u for u, v in relation if v == event}
                setting = (bit + sum(outcomes[u] for u in past)) % 2
                records.append([event, action, bit, setting])
                permutation = [TABLE[action, setting][atom] for atom in permutation]
            self.assertEqual(result["records"], sorted(records))
            self.assertEqual(
                result["pasts"],
                [
                    [event, sorted(u for u, v in relation if v == event)]
                    for event in result["events"]
                ],
            )
            expected_cells = [
                9 * permutation[source // 9] + permutation[source % 9] for source in range(81)
            ]
            self.assertEqual(result["cell_map"], expected_cells)
            self.assertEqual(sorted(result["cell_map"]), list(range(81)))

    def test_all_next_branches_and_zero_maps(self):
        for row in self.report["rows"]:
            result = row["result"]
            branches = result["next"]
            self.assertEqual(
                [(b["action"], b["outcome"]) for b in branches],
                list(itertools.product(("a", "b", "ab"), (0, 1, None))),
            )
            self.assertEqual(sum(b["weight"] for b in branches), F(1))
            old = {event: (action, bit) for event, action, bit, _ in result["records"]}
            for branch in branches:
                relevant = {
                    event
                    for event, (action, _) in old.items()
                    if set(action) & set(branch["action"])
                }
                expected_past = relevant | {u for u, v in result["order"] if v in relevant}
                self.assertEqual(branch["past"], sorted(expected_past))
                if branch["outcome"] is None:
                    self.assertEqual(branch["weight"], F(0))
                    self.assertIsNone(branch["setting"])
                    self.assertEqual(branch["cell_map"], [None] * 81)
                    self.assertFalse(branch["committable"])
                else:
                    self.assertEqual(branch["weight"], F(1, 6))
                    self.assertTrue(branch["committable"])
                    setting = (branch["outcome"] + sum(old[u][1] for u in expected_past)) % 2
                    self.assertEqual(branch["setting"], setting)
                    perm = TABLE[branch["action"], setting]
                    self.assertEqual(
                        branch["cell_map"],
                        [9 * perm[i] + perm[j] for i in range(9) for j in range(9)],
                    )

    def test_extensions_and_label_transports_are_complete(self):
        total = 0
        for row in self.report["rows"]:
            result = row["result"]
            expected = [
                list(ordering)
                for ordering in itertools.permutations(result["events"])
                if all(ordering.index(u) < ordering.index(v) for u, v in result["order"])
            ]
            self.assertEqual(row["linear_extensions"], expected)
            total += len(expected)
            mapping = dict(row["label_map"])
            self.assertEqual(row["relabeled"]["cell_map"], result["cell_map"])
            self.assertEqual(row["relabeled"]["weight"], result["weight"])
            self.assertEqual(
                row["relabeled"]["order"],
                sorted([mapping[u], mapping[v]] for u, v in result["order"]),
            )
            self.assertEqual(
                row["relabeled"]["records"],
                sorted([mapping[e], a, x, s] for e, a, x, s in result["records"]),
            )
        self.assertEqual(self.report["scope"]["linear_extension_replays_per_route"], total)
        self.assertGreater(total, 260)

    def test_append_consistency_and_no_aliasing(self):
        for engine in self.engines:
            for _, history in study.histories():
                untouched = deepcopy(history)
                output = engine.evaluate(history)
                self.assertEqual(history, untouched)
                if history:
                    earlier = engine.evaluate(history[:-1])
                    old_events = earlier["events"]
                    self.assertEqual(
                        [r for r in output["records"] if r[0] in old_events], earlier["records"]
                    )
                    self.assertEqual(
                        [edge for edge in output["order"] if edge[1] in old_events],
                        earlier["order"],
                    )
                output["records"].clear()
                self.assertEqual(history, untouched)
                self.assertEqual(len(engine.evaluate(history)["records"]), len(history))

    def test_fork_join_and_four_birth_diamond(self):
        witness = self.report["controls"]["fork_join"]
        self.assertTrue(witness["same_payload"])
        self.assertTrue(witness["distinct_order"])
        self.assertEqual(witness["fork"]["order"], [[0, 1], [0, 2]])
        self.assertEqual(witness["join"]["order"], [[0, 2], [1, 2]])
        expected = [3 * ((atom % 3 + 1) % 3) + ((atom // 3 + 1) % 3) for atom in range(9)]
        self.assertEqual(
            witness["fork"]["cell_map"],
            [9 * expected[i] + expected[j] for i in range(9) for j in range(9)],
        )
        self.assertEqual(witness["fork"]["weight"], F(1, 216))
        self.assertEqual(
            self.report["rows"][-1]["result"]["order"], [[0, 1], [0, 2], [0, 3], [1, 3], [2, 3]]
        )

    def test_coordinate_inverses_and_negative_controls(self):
        controls = self.report["controls"]
        for entry in controls["coordinates"]:
            forward = TABLE[entry["action"], entry["setting"]]
            self.assertEqual(entry["forward"], forward)
            self.assertEqual(entry["inverse"], [forward.index(atom) for atom in range(9)])
        self.assertTrue(all(item["detected"] for item in controls["wrong_inverse"]))
        self.assertTrue(controls["same_port"]["unequal"])
        self.assertEqual(controls["same_port"]["cycle_after_reflection"][0], 3)
        self.assertEqual(controls["same_port"]["reflection_after_cycle"][0], 6)
        self.assertTrue(controls["stage_negative"]["detected"])
        self.assertNotEqual(controls["stage_negative"]["ab"], controls["stage_negative"]["ba"])
        self.assertTrue(controls["locality"]["equal"])
        self.assertEqual(controls["locality"]["outside_bit_zero"]["past"], [0])
        self.assertEqual(controls["locality"]["outside_bit_zero"]["setting"], 1)

    def test_all_disjoint_setting_maps_commute(self):
        for a_setting, b_setting in itertools.product((0, 1), repeat=2):
            a, b = TABLE["a", a_setting], TABLE["b", b_setting]
            self.assertEqual([a[b[v]] for v in range(9)], [b[a[v]] for v in range(9)])

    def test_exact_complex_kernel_mass_and_scope_witnesses(self):
        controls = self.report["controls"]
        star, conjugate, zero = controls["kernels"]
        self.assertEqual(star["mass"], (F(1), F(0)))
        self.assertEqual(conjugate["mass"], star["mass"])
        self.assertNotEqual(star["kernel"], conjugate["kernel"])
        self.assertEqual(
            [star["kernel"][10 * i] for i in range(9)],
            [conjugate["kernel"][10 * i] for i in range(9)],
        )
        self.assertEqual(star["kernel"][3], (F(1, 20), F(1, 20)))
        self.assertEqual(star["kernel"][27], (F(1, 20), F(-1, 20)))
        self.assertEqual(controls["dstar_unscaled_block_determinant"], F(1, 2))
        self.assertEqual(controls["interference"], F(1, 10))
        self.assertEqual(controls["singleton_restriction_total"], F(9, 10))
        self.assertEqual(
            star["branch_masses"], [(F(1, 6), F(0)), (F(1, 6), F(0)), (F(0), F(0))] * 3
        )
        self.assertEqual(conjugate["branch_masses"], star["branch_masses"])
        self.assertNotEqual(star["branch_outputs"], conjugate["branch_outputs"])
        self.assertEqual(zero["mass"], (F(0), F(0)))
        self.assertTrue(any(entry != (F(0), F(0)) for entry in zero["kernel"]))
        self.assertTrue(any(entry != (F(0), F(0)) for entry in zero["branch_outputs"][0]))
        self.assertEqual(zero["branch_masses"], [(F(0), F(0))] * 9)
        for index, output in enumerate(zero["branch_outputs"]):
            if index % 3 == 2:
                self.assertEqual(output, [(F(0), F(0))] * 81)

    def test_effect_identity_and_all_exact_kernel_outputs(self):
        controls = self.report["controls"]
        self.assertEqual(controls["sum_effect"], [F(1)] * 81)
        for index, effect in enumerate(controls["branch_effects"]):
            self.assertEqual(effect, [F(0) if index % 3 == 2 else F(1, 6)] * 81)
        for witness in controls["kernels"]:
            for branch, output in zip(
                self.report["rows"][0]["result"]["next"], witness["branch_outputs"], strict=True
            ):
                expected = [(F(0), F(0))] * 81
                if branch["outcome"] is not None:
                    perm = TABLE[branch["action"], branch["setting"]]
                    for i in range(9):
                        for j in range(9):
                            expected[9 * perm[i] + perm[j]] = tuple(
                                part / 6 for part in witness["kernel"][9 * i + j]
                            )
                self.assertEqual(output, expected)

    def test_malformed_and_resource_boundaries(self):
        class ListSubclass(list):
            pass

        class IntSubclass(int):
            pass

        malformed = [
            None,
            {},
            "",
            ListSubclass(),
            [[0, "a"]],
            [[0, "a", None]],
            [[0, "a", True]],
            [[True, "a", 0]],
            [[IntSubclass(0), "a", 0]],
            [[-1, "a", 0]],
            [[1000, "a", 0]],
            [[0, "ba", 0]],
            [[0, "", 0]],
            [[0, "a", 2]],
            [[0, "a", 0], [0, "b", 0]],
            [[i, "a", 0] for i in range(5)],
        ]
        for engine in self.engines:
            for value in malformed:
                with (
                    self.subTest(engine=engine.__name__, value=repr(value)),
                    self.assertRaises(ValueError),
                ):
                    engine.evaluate(value)
            self.assertEqual(engine.evaluate(((999, "a", 0),))["events"], [999])
            self.assertEqual(len(engine.evaluate([[i, "a", 0] for i in range(4)])["order"]), 6)
            for action in ("a", "b", "ab"):
                with self.assertRaises(ValueError):
                    engine.evaluate([[0, action, None]])


class Evidence(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="t8-q-renewal-evidence-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "study"
        self.root.mkdir()
        self.sources = study.snapshot()
        for name, blob in self.sources.items():
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(blob)
        self.report = {"scope": {"base_rows": 260}, "test_only": [F(1, 6)]}

    def captured(self):
        with patch.object(study, "analyze", return_value=self.report):
            return study.capture(self.root)

    def test_six_source_inventory_and_byte_snapshot(self):
        self.assertEqual(len(self.sources), 6)
        self.assertTrue(all(type(blob) is bytes for blob in self.sources.values()))
        self.assertEqual(study.snapshot(self.root), self.sources)
        self.assertEqual(set(study.manifest(self.sources)["sources"]), set(study.SOURCE_PATHS))

    def test_create_only_capture_and_read_only_replay(self):
        original = self.captured()
        before = {
            path.name: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.root.iterdir()
            if path.is_file()
        }
        with patch.object(study, "analyze", return_value=self.report):
            self.assertEqual(study.verify(self.root), study.encode(original))
            with self.assertRaises(ValueError):
                study.capture(self.root)
        after = {
            path.name: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.root.iterdir()
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_source_drift_refused_before_math(self):
        self.captured()
        (self.root / "primary.py").write_bytes(self.sources["primary.py"] + b"\n# drift\n")
        with patch.object(study, "analyze") as analyze, self.assertRaises(ValueError):
            study.verify(self.root)
        analyze.assert_not_called()

    def test_candidate_drift_refused(self):
        self.captured()
        name = study.SOURCE_PATHS[-1]
        (self.root / name).write_bytes(self.sources[name] + b"\nChanged premise\n")
        with patch.object(study, "analyze") as analyze, self.assertRaises(ValueError):
            study.verify(self.root)
        analyze.assert_not_called()

    def test_capture_report_tampering_refused(self):
        result = self.captured()
        result["report"] = {"wrong": True}
        (self.root / "results.json").write_bytes(study.canonical(result))
        with (
            patch.object(study, "analyze", return_value=self.report),
            self.assertRaises(ValueError),
        ):
            study.verify(self.root)

    def test_freeze_tampering_refused(self):
        self.captured()
        (self.root / "source-freeze.json").write_bytes(b"{}\n")
        with patch.object(study, "analyze") as analyze, self.assertRaises(ValueError):
            study.verify(self.root)
        analyze.assert_not_called()

    def test_partial_capture_not_overwritten(self):
        (self.root / "results.json").write_bytes(b"reserved\n")
        with patch.object(study, "analyze") as analyze, self.assertRaises(ValueError):
            study.capture(self.root)
        analyze.assert_not_called()
        self.assertEqual((self.root / "results.json").read_bytes(), b"reserved\n")
        self.assertFalse((self.root / "source-freeze.json").exists())

    def test_source_mutation_during_capture_refused(self):
        def changed(_sources):
            (self.root / "reference.py").write_bytes(b"changed")
            return self.report

        with patch.object(study, "analyze", side_effect=changed), self.assertRaises(ValueError):
            study.capture(self.root)
        self.assertFalse((self.root / "source-freeze.json").exists())
        self.assertFalse((self.root / "results.json").exists())

    def test_json_and_source_inventory_refusals(self):
        for blob in (b'{"x":1,"x":2}', b"NaN", b"Infinity", b"x" * 20_000_001):
            with self.assertRaises(ValueError):
                study.strict_loads(blob)
        with self.assertRaises(ValueError):
            study.manifest({})
        with self.assertRaises(ValueError):
            study.load_source(self.sources, "../elsewhere.py")
        with self.assertRaises(ValueError):
            study.encode(0.5)

    def test_exclusive_writer_never_overwrites(self):
        path = self.root / "reserved.json"
        study.write_exclusive(path, {"first": 1})
        before = path.read_bytes()
        with self.assertRaises(FileExistsError):
            study.write_exclusive(path, {"second": 2})
        self.assertEqual(path.read_bytes(), before)
