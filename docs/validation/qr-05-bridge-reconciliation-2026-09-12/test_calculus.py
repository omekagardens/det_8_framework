"""Independent pair-separator oracle and branch-audit regression controls."""

import copy
import hashlib
import importlib.util
import itertools
import json
import signal
import tempfile
import unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent


def load_study():
    spec = importlib.util.spec_from_file_location("reconciliation_study", HERE / "study.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def context():
    study = load_study()
    snapshot = study.source_snapshot()
    protocol = study._protocol(snapshot)
    engine = study.load_engine(snapshot["calculus.py"])
    return study, protocol, engine, study.analyze(snapshot)


def oracle(packet):
    """Pair separators decide identification; equivalence graph supplies blocks."""
    channels, rows = packet["channels"], packet["rows"]
    count = len(channels)
    subsets = sorted(
        ([i for i in range(count) if mask & (1 << i)] for mask in range(1 << count)),
        key=lambda selected: (len(selected), selected),
    )
    pairs = []
    obstructions = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i]["target"] != rows[j]["target"]:
                separating = [
                    k
                    for k in range(count)
                    if rows[i]["observations"][k] != rows[j]["observations"][k]
                ]
                pairs.append(set(separating))
                obstructions.append(
                    {
                        "worlds": [rows[i]["id"], rows[j]["id"]],
                        "separators": [channels[k] for k in separating],
                    }
                )

    def hits(selected):
        return all(bool(set(selected) & separating) for separating in pairs)

    partitions = []
    for selected in subsets:
        relation = [
            [all(a["observations"][k] == b["observations"][k] for k in selected) for b in rows]
            for a in rows
        ]
        remaining = set(range(len(rows)))
        blocks = []
        while remaining:
            first = min(remaining)
            connected = {first}
            pending = [first]
            while pending:
                current = pending.pop()
                for other in sorted(remaining - connected):
                    if relation[current][other]:
                        connected.add(other)
                        pending.append(other)
            remaining -= connected
            blocks.append([rows[k]["id"] for k in sorted(connected)])
        partitions.append(
            {
                "selected": [channels[k] for k in selected],
                "blocks": blocks,
                "identifying": hits(selected),
            }
        )
    good = [s for s in subsets if hits(s)]
    minimal = [s for s in good if all(not hits([k for k in s if k != removed]) for removed in s)]
    least = [len(good[0])] if good else []
    return {
        "channels": list(channels),
        "partitions": partitions,
        "minimal_identifying_sets": [[channels[k] for k in s] for s in minimal],
        "minimum_size": least,
        "minimum_identifying_sets": [[channels[k] for k in s] for s in good if len(s) == least[0]],
        "obstructions": obstructions,
    }


class CalculusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.protocol, cls.engine, cls.report = context()
        cls.packets = {case["id"]: case["packet"] for case in cls.protocol["cases"]}
        cls.results = {case["id"]: case["result"] for case in cls.report["cases"]}

    def test_complete_independent_oracle_and_census(self):
        expected = {
            "schema": "qr05-reconciliation-report-v1",
            "source_branch_commit": self.protocol["source_branch_commit"],
            "cases": [
                {"id": name, "result": oracle(packet)} for name, packet in self.packets.items()
            ],
        }
        self.study.require_equal(self.report, expected)
        self.assertEqual(len(self.results), 5)
        self.assertEqual(sum(len(r["partitions"]) for r in self.results.values()), 27)

    def test_joint_xor_and_slice_counterexample(self):
        packet = self.packets["xor_joint"]
        self.assertFalse(self.engine.identifying(packet, ["xor"]))
        self.assertEqual(self.engine.partition(packet, ["xor"]), [["00", "11"], ["01", "10"]])
        self.assertEqual(
            self.results["xor_joint"]["minimal_identifying_sets"],
            [["a", "b"], ["a", "xor"], ["b", "xor"]],
        )
        for fixed, target in ((1, 0), (0, 1)):
            sliced = copy.deepcopy(packet)
            sliced["rows"] = [r for r in sliced["rows"] if r["target"][fixed] == 0]
            for row in sliced["rows"]:
                row["target"] = [row["target"][target]]
            self.assertTrue(self.engine.identifying(sliced, ["xor"]))

    def test_minimal_is_not_minimum(self):
        result = self.results["minimal_not_minimum"]
        self.assertEqual(result["minimal_identifying_sets"], [["a"], ["b", "xor"]])
        self.assertEqual(result["minimum_size"], [1])
        self.assertEqual(result["minimum_identifying_sets"], [["a"]])

    def test_constant_and_impossible_target_boundaries(self):
        self.assertEqual(self.results["constant"]["minimum_size"], [0])
        self.assertEqual(self.results["constant"]["minimal_identifying_sets"], [[]])
        self.assertEqual(self.results["constant"]["obstructions"], [])
        self.assertEqual(self.results["blind"]["minimum_size"], [])
        self.assertEqual(self.results["blind"]["minimal_identifying_sets"], [])
        self.assertEqual(
            self.results["blind"]["obstructions"], [{"worlds": ["x", "y"], "separators": []}]
        )

    def test_perfect_anchor_is_explicit_and_internal_channels_stay_blind(self):
        result = self.results["scale_anchor"]
        self.assertEqual(
            result["minimal_identifying_sets"],
            [["colour", "external_scale"], ["colour_copy", "external_scale"]],
        )
        for row in result["partitions"]:
            if "external_scale" not in row["selected"]:
                self.assertFalse(row["identifying"])
        self.assertFalse(self.engine.identifying(self.packets["scale_anchor"], ["external_scale"]))

    def test_all_fixed_refinements_and_pair_witnesses(self):
        for result in self.results.values():
            for coarse in result["partitions"]:
                for fine in result["partitions"]:
                    if set(coarse["selected"]) <= set(fine["selected"]):
                        if coarse["identifying"]:
                            self.assertTrue(fine["identifying"])
                        for block in fine["blocks"]:
                            self.assertTrue(any(set(block) <= set(old) for old in coarse["blocks"]))
                bad = [
                    w
                    for w in result["obstructions"]
                    if not set(w["separators"]) & set(coarse["selected"])
                ]
                self.assertEqual(coarse["identifying"], not bad)

    def test_fresh_outputs_and_input_immutability(self):
        for packet in self.packets.values():
            supplied = copy.deepcopy(packet)
            output = self.engine.analyze(supplied)
            output["channels"].append("mutation")
            output["partitions"][0]["blocks"][0].append("mutation")
            self.study.require_equal(supplied, packet)
            self.study.require_equal(self.engine.analyze(packet), oracle(packet))

    def test_selected_order_does_not_change_fibers(self):
        for packet in self.packets.values():
            for row in oracle(packet)["partitions"]:
                reversed_names = list(reversed(row["selected"]))
                self.assertEqual(self.engine.partition(packet, reversed_names), row["blocks"])
                self.assertIs(self.engine.identifying(packet, reversed_names), row["identifying"])

    def test_malformed_native_packets_are_rejected(self):
        packet = self.packets["xor_joint"]
        bad = [
            None,
            [],
            {**packet, "extra": 0},
            {**packet, "rows": []},
            {**packet, "channels": tuple(packet["channels"])},
            {**packet, "channels": ["a", "a", "xor"]},
            {**packet, "channels": [str(i) for i in range(9)]},
            {**packet, "rows": packet["rows"] * 17},
        ]
        for path, value in (
            (("rows", 0, "id"), True),
            (("rows", 1, "id"), "00"),
            (("rows", 0, "observations", 0), True),
            (("rows", 0, "target", 0), F(0)),
            (("rows", 0, "target"), []),
            (("rows", 0, "target"), [0] * 9),
            (("rows", 0, "target"), [0]),
            (("rows", 0, "observations"), [0, 0]),
            (("rows", 0, "observations", 0), 0.0),
        ):
            changed = copy.deepcopy(packet)
            node = changed
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value
            bad.append(changed)

        class DictSubclass(dict):
            pass

        bad.append(DictSubclass(packet))
        for changed in bad:
            for operation in (
                self.engine.analyze,
                lambda p: self.engine.partition(p, []),
                lambda p: self.engine.identifying(p, []),
            ):
                with self.subTest(value=repr(changed)[:70]), self.assertRaises(ValueError):
                    operation(changed)

    def test_malformed_selections_are_rejected(self):
        for selected in (None, (), [True], ["missing"], ["a", "a"], ["a"] * 9):
            for operation in (self.engine.partition, self.engine.identifying):
                with self.subTest(selected=selected), self.assertRaises(ValueError):
                    operation(self.packets["xor_joint"], selected)


class MathematicalRegressionTests(unittest.TestCase):
    def test_dependent_same_data_events_need_no_independence_for_union(self):
        E, G = {0, 1}, {1, 2}
        probability = lambda event: F(len(event), 3)
        alpha, beta = 1 - probability(E), 1 - probability(G)
        self.assertEqual(probability(E & G), 1 - alpha - beta)
        self.assertLess(probability(E & G), (1 - alpha) * (1 - beta))
        H = {0}
        self.assertEqual(probability(H & E & G), max(F(0), probability(H) - alpha - beta))
        self.assertEqual(min(F(1), F(3, 4) + F(3, 4)), F(1))

    def test_all_pair_max_plus_not_link_only_characterization(self):
        def maximum_path(weights, left, right):
            interiors = list(range(left + 1, right))
            candidates = []
            for length in range(len(interiors) + 1):
                for middle in itertools.combinations(interiors, length):
                    path = (left,) + middle + (right,)
                    if all((a, b) in weights for a, b in itertools.pairwise(path)):
                        candidates.append(sum(weights[a, b] for a, b in itertools.pairwise(path)))
            return max(candidates)

        weights = {(0, 1): 1, (1, 2): 1, (0, 2): 3}
        self.assertGreaterEqual(weights[0, 2], weights[0, 1] + weights[1, 2])
        self.assertEqual(maximum_path(weights, 0, 2), 3)
        self.assertEqual(maximum_path({(0, 1): 1, (1, 2): 1}, 0, 2), 2)

    def test_full_visibility_does_not_imply_chsh_violation(self):
        alice, bob = [1, 1], [1, -1]
        matrix = [[a * b for b in bob] for a in alice]
        for row in matrix:
            amplitude = F(max(row) - min(row), 2)
            self.assertGreater(amplitude**2, F(1, 2))
        signs = [s for s in itertools.product((-1, 1), repeat=4) if s[0] * s[1] * s[2] * s[3] == -1]
        values = [
            abs(sum(s * x for s, x in zip(sign, [v for row in matrix for v in row], strict=True)))
            for sign in signs
        ]
        self.assertEqual(max(values), 2)

    def test_signed_path_cancellation_and_orientation_reversal(self):
        def inverse(matrix):
            n = len(matrix)
            augmented = [
                [F(x) for x in row] + [F(i == j) for j in range(n)] for i, row in enumerate(matrix)
            ]
            for i in range(n):
                pivot = augmented[i][i]
                augmented[i] = [x / pivot for x in augmented[i]]
                for j in range(n):
                    if i != j:
                        factor = augmented[j][i]
                        augmented[j] = [
                            x - factor * y for x, y in zip(augmented[j], augmented[i], strict=True)
                        ]
            return [row[n:] for row in augmented]

        zero = inverse([[-3, 0, 0], [3, -3, 0], [-3, 3, -3]])
        self.assertEqual(zero[2][0], 0)
        changed = inverse([[-5, 0, 0], [3, -5, 0], [-3, 3, -5]])
        self.assertEqual(changed[0][1] - changed[1][0], F(3, 25))
        self.assertEqual(changed[0][2] - changed[2][0], F(-6, 125))


class EvidenceTests(unittest.TestCase):
    def test_protocol_and_utility_pins_before_parse_or_execution(self):
        study = load_study()
        snapshot = study.source_snapshot()
        with (
            mock.patch.object(study, "strict_loads", side_effect=AssertionError("early parse")),
            self.assertRaises(ValueError),
        ):
            study._protocol({**snapshot, "protocol.json": snapshot["protocol.json"] + b"\n"})
        with tempfile.TemporaryDirectory(prefix="qr05-reconciliation-utility-") as directory:
            path = Path(directory) / "probe.py"
            path.write_bytes(b"raise AssertionError('untrusted execution')\n")
            with self.assertRaises(ValueError):
                study._load_utilities(path)

    def test_exact_native_codec_and_mismatch(self):
        study = load_study()
        value = {"r": F(1, 3), "i": 1, "b": True, "none": []}
        study.require_equal(
            study.decode(study.strict_loads(study.canonical(study.encode(value)))), value
        )
        for a, b in ((True, 1), (F(1), 1), ([], ()), ({"x": 1}, {"x": 1, "y": 0})):
            with self.assertRaises(ValueError):
                study.require_equal(a, b)
        for blob in (b'{"x":1,"x":2}', b'{"x":1.0}', b'{"x":NaN}'):
            with self.assertRaises(ValueError):
                study.strict_loads(blob)

    def test_authenticated_roundtrip_is_exclusive_and_source_bound(self):
        study = load_study()
        with tempfile.TemporaryDirectory(prefix="qr05-reconciliation-evidence-") as directory:
            freeze = Path(directory) / "freeze.json"
            capture = Path(directory) / "capture.json"
            with mock.patch.object(study, "analyze", return_value={"value": 1}):
                study.freeze(freeze)
                study.capture(capture, freeze)
                self.assertEqual(study.replay(capture, freeze), {"value": 1})
                for operation, path in (
                    (study.freeze, freeze),
                    (lambda p: study.capture(p, freeze), capture),
                ):
                    with self.assertRaises(FileExistsError):
                        operation(path)
                original = capture.read_bytes()
                data = json.loads(original)
                data["report"]["value"] = True
                capture.write_bytes(study.canonical(data))
                with self.assertRaises(ValueError):
                    study.replay(capture, freeze)
                capture.write_bytes(original)
                freeze.write_bytes(freeze.read_bytes() + b"\n")
                with self.assertRaises(ValueError):
                    study.replay(capture, freeze)

    def test_existing_capture_full_native_identity_without_extra_analysis(self):
        study, _, _, report = context()
        snapshot = study.source_snapshot()
        freeze_data = study._checked_freeze(HERE / "source-freeze.json", snapshot)
        capture_data = study.read_bounded(HERE / "results.json")
        artifact = study.strict_loads(capture_data)
        self.assertEqual(study.canonical(artifact), capture_data)
        study.require_equal(artifact["sources"], study.identities(snapshot))
        self.assertEqual(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
        study.require_equal(study.decode(artifact["report"]), report)

    def test_mutation_and_late_source_change_abort(self):
        study = load_study()
        snapshot = study.source_snapshot()

        def mutate(packet):
            packet["rows"][0]["target"][0] = 999
            return {}

        engine = type("Synthetic", (), {"analyze": staticmethod(mutate)})
        with (
            mock.patch.object(study, "load_engine", return_value=engine),
            self.assertRaises(ValueError),
        ):
            study.analyze(snapshot)
        original = study.read_bounded

        def reader(path, *args):
            return (
                snapshot["calculus.py"] + b"\n"
                if Path(path) == HERE / "calculus.py"
                else original(path, *args)
            )

        with (
            mock.patch.object(study, "read_bounded", side_effect=reader),
            self.assertRaises(ValueError),
        ):
            study._check_snapshot(snapshot)


if __name__ == "__main__":

    def expired(_signum, _frame):
        raise KeyboardInterrupt("60-second reconciliation suite deadline")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 60)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
