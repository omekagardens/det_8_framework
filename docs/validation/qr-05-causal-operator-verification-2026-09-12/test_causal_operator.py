"""Prospective native oracle, pure-API boundaries and authenticated evidence tests.

Do not execute before the complete first source freeze. The inverse oracle
uses the design's explicit thirteen-case table, not either engine. Engine
modules are loaded only from authenticated snapshot bytes during tests.
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
VARIANTS = ["identity", "cyclic", "reversal", "rescale"]
WITNESSES = [
    ("zero_cover_order", "G", "missing_cover", "single_edge"),
    ("signed_orientation", "Delta", "forward_pair", "reversed_signed_pair"),
    ("signed_nonisomorphic", "Delta", "fork", "signed_relabelled_chain"),
]


def load_study():
    spec = importlib.util.spec_from_file_location("causal_operator_test_study", HERE / "study.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load authenticated causal-operator driver")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def context():
    """Exactly one genuine full two-route analysis per suite."""
    study = load_study()
    snapshot = study.source_snapshot()
    protocol = study._protocol(snapshot)
    original_load = study.load_engine

    def guarded_load(blob, name):
        engine = original_load(blob, name)
        original_analyze = engine.analyze

        def guarded_analyze():
            with mock.patch("builtins.open", side_effect=AssertionError("pure analysis I/O")):
                return original_analyze()

        engine.analyze = guarded_analyze
        return engine

    with mock.patch.object(study, "load_engine", side_effect=guarded_load):
        report = study.analyze(snapshot)
    return study, snapshot, protocol, report


def exact(test, actual, expected, path="report"):
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


def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def multiply(left, right):
    n = len(left)
    return [
        [sum((left[i][k] * right[k][j] for k in range(n)), F(0)) for j in range(n)]
        for i in range(n)
    ]


def scaled(matrix, factor):
    return [[factor * value for value in row] for row in matrix]


def transposed(matrix):
    return [list(column) for column in zip(*matrix, strict=True)]


def cyclic(matrix):
    n = len(matrix)
    return [[matrix[(i - 1) % n][(j - 1) % n] for j in range(n)] for i in range(n)]


def product(values):
    result = F(1)
    for value in values:
        result *= value
    return result


def support(matrix):
    return [
        [int(i != j and value != 0) for j, value in enumerate(row)] for i, row in enumerate(matrix)
    ]


def closure(mask):
    """Independent sender-by-sender graph exploration, with no order input."""
    n = len(mask)
    result = [[0 for _ in range(n)] for _ in range(n)]
    for sender in range(n):
        found = set()
        frontier = {sender}
        while frontier:
            reached = {i for j in frontier for i in range(n) if mask[i][j]} - found
            found.update(reached)
            frontier = reached
        for receiver in found:
            result[receiver][sender] = 1
    return result


def base_cases():
    """Explicit analytical G entries: no inverse/power/path calculation selects G."""
    chain = [(1, 0), (2, 0), (2, 1)]
    fork = [(1, 0), (2, 0)]
    diamond = [(1, 0), (2, 0), (3, 0), (3, 1), (3, 2)]
    chain_weights = [(1, 0, 1), (2, 1, 1)]
    diamond_weights = [(1, 0, 1), (2, 0, 1), (3, 1, 1), (3, 2, 1)]
    signed_weights = [(1, 0, 3), (2, 0, -3), (2, 1, 3)]
    specifications = [
        ("singleton", 1, [], [], 1, []),
        ("antichain", 3, [], [], 1, []),
        ("chain", 3, chain, chain_weights, 1, [(1, 0, 1), (2, 0, 1), (2, 1, 1)]),
        ("fork", 3, fork, [(1, 0, 1), (2, 0, 1)], 1, [(1, 0, 1), (2, 0, 1)]),
        ("diamond", 4, diamond, diamond_weights, 1, [*diamond_weights, (3, 0, 2)]),
        ("missing_cover", 3, chain, [(1, 0, 1)], 1, [(1, 0, 1)]),
        ("single_edge", 3, [(1, 0)], [(1, 0, 1)], 1, [(1, 0, 1)]),
        (
            "signed_diamond",
            4,
            diamond,
            [(1, 0, 1), (2, 0, 1), (3, 1, 1), (3, 2, -1)],
            1,
            [(1, 0, 1), (2, 0, 1), (3, 1, 1), (3, 2, -1)],
        ),
        ("toy_cancel", 3, chain, signed_weights, 3, [(1, 0, F(1, 3)), (2, 1, F(1, 3))]),
        (
            "toy_sign",
            3,
            chain,
            signed_weights,
            5,
            [(1, 0, F(3, 25)), (2, 0, F(-6, 125)), (2, 1, F(3, 25))],
        ),
        ("forward_pair", 2, [(1, 0)], [(1, 0, 1)], 1, [(1, 0, 1)]),
        ("reversed_signed_pair", 2, [(0, 1)], [(0, 1, -1)], 1, [(0, 1, -1)]),
        (
            "signed_relabelled_chain",
            3,
            [(0, 1), (2, 0), (2, 1)],
            [(0, 1, -1), (2, 0, 1), (2, 1, 1)],
            1,
            [(0, 1, -1), (2, 0, 1)],
        ),
    ]
    result = []
    for name, n, relation, weights, diagonal, entries in specifications:
        C = [[int((i, j) in relation) for j in range(n)] for i in range(n)]
        A, G = zero(n), scaled(identity(n), F(1, diagonal))
        for i, j, value in weights:
            A[i][j] = F(value)
        for i, j, value in entries:
            G[i][j] = F(value)
        result.append((name, {"C": C, "A": A, "d": F(diagonal)}, G))
    return result


def variant_world(world, variant):
    result = copy.deepcopy(world)
    if variant == "cyclic":
        result["C"], result["A"] = cyclic(world["C"]), cyclic(world["A"])
    elif variant == "reversal":
        result["C"], result["A"] = transposed(world["C"]), transposed(world["A"])
    elif variant == "rescale":
        result["A"] = scaled(world["A"], F(3, 2))
        result["d"] = F(3, 2) * world["d"]
    return result


def variant_inverse(G, variant):
    if variant == "cyclic":
        return cyclic(G)
    if variant == "reversal":
        return transposed(G)
    if variant == "rescale":
        return scaled(G, F(2, 3))
    return copy.deepcopy(G)


def oracle_row(world, G):
    """All raw fields independently reconstructed around the declared inverse."""
    C, A, d = world["C"], world["A"], world["d"]
    n = len(C)
    L = [
        [int(C[i][j] == 1 and not any(C[i][k] and C[k][j] for k in range(n))) for j in range(n)]
        for i in range(n)
    ]
    powers = [identity(n)]
    for _ in range(n):
        powers.append(multiply(powers[-1], A))
    M = [[d * F(int(i == j)) - A[i][j] for j in range(n)] for i in range(n)]
    Delta = [[G[i][j] - G[j][i] for j in range(n)] for i in range(n)]
    paths = []
    # Lexicographic permutations differ from recursive path discovery; all
    # C-admissible paths are retained, including paths with a zero A factor.
    for count in range(1, n + 1):
        for nodes in itertools.permutations(range(n), count):
            if all(C[right][left] for left, right in itertools.pairwise(nodes)):
                weights = [A[right][left] for left, right in itertools.pairwise(nodes)]
                paths.append(
                    {
                        "nodes": list(nodes),
                        "weights": weights,
                        "contribution": product(weights) / d**count,
                    }
                )
    sa, sg = support(A), support(G)
    ca, cg = closure(sa), closure(sg)
    covers = [
        {"pair": [i, j], "A": A[i][j], "G": G[i][j], "expected": A[i][j] / d**2}
        for i in range(n)
        for j in range(n)
        if L[i][j]
    ]
    differences = {}
    for label, observed in (("direct", sg), ("reachable", cg)):
        differences["missing_" + label] = [
            [i, j] for i in range(n) for j in range(n) if C[i][j] == 1 and observed[i][j] == 0
        ]
        differences["extra_" + label] = [
            [i, j] for i in range(n) for j in range(n) if C[i][j] == 0 and observed[i][j] == 1
        ]
    flags = {
        "direct_equal": sg == C,
        "reachability_equal": cg == C,
        "closures_equal": ca == cg,
        "covers_nonzero": all(item["A"] != 0 for item in covers),
        "covers_positive": all(item["A"] > 0 for item in covers),
        "A_nonnegative": all(value >= 0 for row in A for value in row),
        "positive_sign_rule": all(
            (Delta[i][j] > 0) == bool(C[i][j]) and (Delta[i][j] < 0) == bool(C[j][i])
            for i in range(n)
            for j in range(n)
        ),
    }
    return {
        "world": copy.deepcopy(world),
        "L": L,
        "powers": powers,
        "M": M,
        "G": copy.deepcopy(G),
        "Delta": Delta,
        "MG": multiply(M, G),
        "GM": multiply(G, M),
        "paths": paths,
        "support_A": sa,
        "support_G": sg,
        "closure_A": ca,
        "closure_G": cg,
        "covers": covers,
        **differences,
        "flags": flags,
    }


@lru_cache(maxsize=1)
def full_oracle():
    rows = []
    for name, world, G in base_cases():
        for variant in VARIANTS:
            rows.append(
                {
                    "id": name + ":" + variant,
                    "base": name,
                    "variant": variant,
                    **oracle_row(variant_world(world, variant), variant_inverse(G, variant)),
                }
            )
    by_id = {row["id"]: row for row in rows}
    witnesses = []
    for kind, channel, left, right in WITNESSES:
        for variant in VARIANTS:
            ids = [left + ":" + variant, right + ":" + variant]
            witnesses.append(
                {
                    "kind": kind,
                    "variant": variant,
                    "channel": channel,
                    "rows": ids,
                    "value": copy.deepcopy(by_id[ids[0]][channel]),
                    "targets": [copy.deepcopy(by_id[name]["world"]["C"]) for name in ids],
                }
            )
    return {"schema": "qr05-causal-operator-report-v1", "rows": rows, "witnesses": witnesses}


def mutable_ids(value):
    found = set()
    if type(value) in (list, dict):
        found.add(id(value))
        children = value.values() if type(value) is dict else value
        for child in children:
            found.update(mutable_ids(child))
    return found


class CausalOperatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.snapshot, cls.protocol, cls.report = context()

    def engines(self):
        for name in ("primary.py", "reference.py"):
            yield name, self.study.load_engine(self.snapshot[name], name)

    def test_full_independent_native_report_and_codec(self):
        exact(self, self.report, full_oracle())
        exact(
            self,
            self.study.decode(
                self.study.strict_loads(self.study.canonical(self.study.encode(self.report)))
            ),
            self.report,
        )

    def test_protocol_inputs_independent_case_ledger_and_order(self):
        expected = base_cases()
        self.assertEqual(len(self.protocol["cases"]), 13)
        exact(self, self.protocol["variants"], VARIANTS)
        exact(self, self.protocol["scale_multiplier"], [3, 2])
        for case, (name, world, _) in zip(self.protocol["cases"], expected, strict=True):
            n = len(world["C"])
            self.assertEqual(case["id"], name)
            self.assertEqual(case["n"], n)
            exact(
                self,
                case["relation"],
                [[i, j] for i in range(n) for j in range(n) if world["C"][i][j]],
            )
            exact(
                self,
                case["weights"],
                [
                    [i, j, value.numerator, value.denominator]
                    for i, row in enumerate(world["A"])
                    for j, value in enumerate(row)
                    if value
                ],
            )
            exact(self, case["d"], [world["d"].numerator, world["d"].denominator])
        exact(
            self,
            self.protocol["witnesses"],
            [
                {"kind": kind, "channel": channel, "cases": [left, right]}
                for kind, channel, left, right in WITNESSES
            ],
        )
        self.assertEqual(
            [row["id"] for row in self.report["rows"]],
            [name + ":" + variant for name, _, _ in expected for variant in VARIANTS],
        )

    def test_complete_analytical_census(self):
        rows = self.report["rows"]
        all_paths = [path for row in rows for path in row["paths"]]
        actual = {
            "rows": len(rows),
            "event_occurrences": sum(len(row["G"]) for row in rows),
            "matrix_cells": sum(len(row["G"]) ** 2 for row in rows),
            "strict_pairs": sum(sum(line) for row in rows for line in row["world"]["C"]),
            "covers": sum(len(row["covers"]) for row in rows),
            "nonzero_A": sum(sum(line) for row in rows for line in row["support_A"]),
            "nonzero_G_off": sum(sum(line) for row in rows for line in row["support_G"]),
            "paths": len(all_paths),
            "trivial_paths": sum(len(path["nodes"]) == 1 for path in all_paths),
            "one_edge_paths": sum(len(path["nodes"]) == 2 for path in all_paths),
            "two_edge_paths": sum(len(path["nodes"]) == 3 for path in all_paths),
            "zero_paths": sum(path["contribution"] == 0 for path in all_paths),
            "direct_equal": sum(row["flags"]["direct_equal"] for row in rows),
            "reachability_equal": sum(row["flags"]["reachability_equal"] for row in rows),
            "witnesses": len(self.report["witnesses"]),
        }
        expected = {
            "rows": 52,
            "event_occurrences": 148,
            "matrix_cells": 452,
            "strict_pairs": 120,
            "covers": 92,
            "nonzero_A": 100,
            "nonzero_G_off": 100,
            "paths": 304,
            "trivial_paths": 148,
            "one_edge_paths": 120,
            "two_edge_paths": 36,
            "zero_paths": 24,
            "direct_equal": 36,
            "reachability_equal": 48,
            "witnesses": 12,
        }
        exact(self, actual, expected)
        exact(self, self.protocol["coverage"], expected)

    def test_complete_powers_nilpotence_and_both_inverse_products(self):
        for row in self.report["rows"]:
            n, A, d = len(row["G"]), row["world"]["A"], row["world"]["d"]
            with self.subTest(row=row["id"]):
                self.assertEqual(len(row["powers"]), n + 1)
                exact(self, row["powers"][0], identity(n))
                exact(self, row["powers"][1], A)
                exact(self, row["powers"][-1], zero(n))
                for k in range(n):
                    exact(self, multiply(A, row["powers"][k]), row["powers"][k + 1])
                total = [
                    [
                        sum((row["powers"][k][i][j] / d ** (k + 1) for k in range(n)), F(0))
                        for j in range(n)
                    ]
                    for i in range(n)
                ]
                exact(self, total, row["G"])
                for name, left, right in (("MG", row["M"], row["G"]), ("GM", row["G"], row["M"])):
                    exact(self, row[name], multiply(left, right))
                    exact(self, row[name], identity(n))

    def test_every_path_term_order_zero_term_and_summed_inverse(self):
        for row in self.report["rows"]:
            C, A, d = row["world"]["C"], row["world"]["A"], row["world"]["d"]
            n = len(C)
            total = zero(n)
            keys = [(len(path["nodes"]), path["nodes"]) for path in row["paths"]]
            self.assertEqual(keys, sorted(keys))
            self.assertEqual(len(keys), len({tuple(path["nodes"]) for path in row["paths"]}))
            for path in row["paths"]:
                nodes = path["nodes"]
                weights = [A[right][left] for left, right in itertools.pairwise(nodes)]
                self.assertEqual(len(nodes), len(set(nodes)))
                self.assertTrue(all(C[right][left] for left, right in itertools.pairwise(nodes)))
                exact(self, path["weights"], weights)
                exact(self, path["contribution"], product(weights) / d ** len(nodes))
                total[nodes[-1]][nodes[0]] += path["contribution"]
            exact(self, total, row["G"])
            exact(
                self,
                [path["nodes"] for path in row["paths"] if len(path["nodes"]) == 1],
                [[i] for i in range(n)],
            )

    def test_support_closure_covers_and_complete_differences(self):
        for row in self.report["rows"]:
            C, A, G = row["world"]["C"], row["world"]["A"], row["G"]
            exact(self, row["support_A"], support(A))
            exact(self, row["support_G"], support(G))
            exact(self, row["closure_A"], closure(support(A)))
            exact(self, row["closure_G"], closure(support(G)))
            exact(self, row["closure_A"], row["closure_G"])
            self.assertEqual(row["extra_direct"], [])
            self.assertEqual(row["extra_reachable"], [])
            for item in row["covers"]:
                i, j = item["pair"]
                exact(self, item["A"], A[i][j])
                exact(self, item["G"], G[i][j])
                exact(self, item["G"], item["expected"])
                exact(self, item["expected"], A[i][j] / row["world"]["d"] ** 2)
            for label, field in (("direct", "support_G"), ("reachable", "closure_G")):
                exact(
                    self,
                    row["missing_" + label],
                    [
                        [i, j]
                        for i in range(len(C))
                        for j in range(len(C))
                        if C[i][j] and not row[field][i][j]
                    ],
                )
                self.assertIs(
                    row["flags"][label + "_equal" if label == "direct" else "reachability_equal"],
                    row[field] == C,
                )

    def test_signed_reachability_and_full_positivity_premise(self):
        by_id = {row["id"]: row for row in self.report["rows"]}
        for row in self.report["rows"]:
            flags = row["flags"]
            self.assertTrue(flags["closures_equal"])
            self.assertIs(flags["reachability_equal"], flags["covers_nonzero"])
            if flags["A_nonnegative"]:
                self.assertIs(flags["direct_equal"], flags["covers_positive"])
                self.assertIs(flags["positive_sign_rule"], flags["covers_positive"])
            if flags["A_nonnegative"] and flags["covers_positive"]:
                self.assertTrue(flags["positive_sign_rule"])
            C, D = row["world"]["C"], row["Delta"]
            actual = all(
                (D[i][j] > 0) == bool(C[i][j]) and (D[i][j] < 0) == bool(C[j][i])
                for i in range(len(C))
                for j in range(len(C))
            )
            self.assertIs(flags["positive_sign_rule"], actual)
        for base in ("toy_cancel", "toy_sign"):
            flags = by_id[base + ":identity"]["flags"]
            self.assertTrue(flags["covers_positive"])
            self.assertFalse(flags["A_nonnegative"])
            self.assertFalse(flags["positive_sign_rule"])
        for base in ("singleton", "antichain"):
            self.assertTrue(all(by_id[base + ":identity"]["flags"].values()))

    def test_exact_signed_cancellation_and_old_whole_sign_convention(self):
        rows = {row["id"]: row for row in self.report["rows"]}
        cancelled = rows["toy_cancel:identity"]
        exact(self, cancelled["G"][2][0], F(0))
        terms = [
            path["contribution"]
            for path in cancelled["paths"]
            if path["nodes"][0] == 0 and path["nodes"][-1] == 2
        ]
        exact(self, terms, [F(-1, 3), F(1, 3)])
        changed = rows["toy_sign:identity"]
        exact(self, changed["G"][1][0], F(3, 25))
        exact(self, changed["G"][2][0], F(-6, 125))
        old_G = scaled(changed["G"], F(-1))
        old_Delta = scaled(changed["Delta"], F(-1))
        exact(self, multiply(scaled(changed["M"], F(-1)), old_G), identity(3))
        exact(self, old_Delta[0][1], F(3, 25))
        exact(self, old_Delta[0][2], F(-6, 125))
        diamond = rows["signed_diamond:identity"]
        exact(self, diamond["G"][3][0], F(0))
        exact(
            self,
            [path["contribution"] for path in diamond["paths"] if len(path["nodes"]) == 3],
            [F(1), F(-1)],
        )
        self.assertTrue(diamond["flags"]["covers_nonzero"])
        self.assertFalse(diamond["flags"]["direct_equal"])
        self.assertTrue(diamond["flags"]["reachability_equal"])

    def test_all_twelve_native_information_collision_witnesses(self):
        exact(self, self.report["witnesses"], full_oracle()["witnesses"])
        rows = {row["id"]: row for row in self.report["rows"]}
        for witness in self.report["witnesses"]:
            left, right = [rows[name] for name in witness["rows"]]
            exact(self, witness["value"], left[witness["channel"]])
            exact(self, witness["value"], right[witness["channel"]])
            exact(self, witness["targets"], [left["world"]["C"], right["world"]["C"]])
            self.assertNotEqual(witness["targets"][0], witness["targets"][1])
            if witness["kind"] == "zero_cover_order":
                self.assertFalse(left["flags"]["covers_nonzero"])
                self.assertTrue(right["flags"]["covers_nonzero"])
            else:
                self.assertTrue(left["flags"]["covers_nonzero"])
                self.assertTrue(right["flags"]["covers_nonzero"])
                self.assertNotEqual(left["G"], right["G"])
            if witness["kind"] == "signed_nonisomorphic":
                self.assertEqual(sum(map(sum, witness["targets"][0])), 2)
                self.assertEqual(sum(map(sum, witness["targets"][1])), 3)

    def test_all_transformations_include_powers_and_path_data(self):
        rows = {row["id"]: row for row in self.report["rows"]}
        matrix_fields = [
            "L",
            "M",
            "G",
            "Delta",
            "MG",
            "GM",
            "support_A",
            "support_G",
            "closure_A",
            "closure_G",
        ]
        for base, _, _ in base_cases():
            original = rows[base + ":identity"]
            n = len(original["G"])
            for variant in VARIANTS[1:]:
                row = rows[base + ":" + variant]
                exact(self, row["world"], variant_world(original["world"], variant))
                for field in matrix_fields:
                    wanted = copy.deepcopy(original[field])
                    if variant == "cyclic":
                        wanted = cyclic(wanted)
                    elif variant == "reversal":
                        wanted = transposed(wanted)
                    elif field == "M":
                        wanted = scaled(wanted, F(3, 2))
                    elif field in ("G", "Delta"):
                        wanted = scaled(wanted, F(2, 3))
                    exact(self, row[field], wanted)
                for exponent, power in enumerate(original["powers"]):
                    wanted = (
                        cyclic(power)
                        if variant == "cyclic"
                        else transposed(power)
                        if variant == "reversal"
                        else scaled(power, F(3, 2) ** exponent)
                    )
                    exact(self, row["powers"][exponent], wanted)
                paths = copy.deepcopy(original["paths"])
                for path in paths:
                    if variant == "cyclic":
                        path["nodes"] = [(node + 1) % n for node in path["nodes"]]
                    elif variant == "reversal":
                        path["nodes"].reverse()
                        path["weights"].reverse()
                    else:
                        path["weights"] = [F(3, 2) * value for value in path["weights"]]
                        path["contribution"] *= F(2, 3)
                paths.sort(key=lambda path: (len(path["nodes"]), path["nodes"]))
                exact(self, row["paths"], paths)
                exact(self, row["flags"], original["flags"])
                if variant == "reversal":
                    exact(self, row["Delta"], scaled(original["Delta"], F(-1)))

    def test_fresh_pure_evaluate_all_fixed_worlds_and_arbitrary_labels(self):
        for name, engine in self.engines():
            for expected in full_oracle()["rows"]:
                with self.subTest(engine=name, row=expected["id"]):
                    supplied = copy.deepcopy(expected["world"])
                    original = copy.deepcopy(supplied)
                    with mock.patch(
                        "builtins.open", side_effect=AssertionError("pure evaluator I/O")
                    ):
                        computed = engine.evaluate(supplied)
                    exact(
                        self,
                        computed,
                        {
                            key: value
                            for key, value in expected.items()
                            if key not in ("id", "base", "variant")
                        },
                    )
                    exact(self, supplied, original)
                    self.assertFalse(mutable_ids(supplied) & mutable_ids(computed))

    def test_native_world_shape_and_scalar_refusals(self):
        class DictSubclass(dict):
            pass

        class ListSubclass(list):
            pass

        class IntSubclass(int):
            pass

        class FractionSubclass(F):
            pass

        world = copy.deepcopy(base_cases()[10][1])
        bad = [
            None,
            [],
            DictSubclass(world),
            {**world, "extra": 0},
            {key: value for key, value in world.items() if key != "d"},
        ]
        for key in ("C", "A"):
            for value in (
                None,
                (),
                ListSubclass(world[key]),
                [],
                [world[key][0]],
                [[], []],
                [world[key][0], world[key][1] + [world[key][1][0]]],
                [ListSubclass(world[key][0]), world[key][1]],
                [tuple(world[key][0]), world[key][1]],
            ):
                bad.append({**world, key: value})
        for value in (True, F(0), 0.0, IntSubclass(0), -1, 2):
            altered = copy.deepcopy(world)
            altered["C"][0][0] = value
            bad.append(altered)
        for value in (0, False, 0.0, FractionSubclass(0), F(2**128), F(-(2**128)), F(1, 2**128)):
            altered = copy.deepcopy(world)
            altered["A"][1][0] = value
            bad.append(altered)
        for value in (1, True, 1.0, FractionSubclass(1), F(0), F(-1), F(2**128), F(1, 2**128)):
            bad.append({**world, "d": value})
        bad.append({"C": [[0] * 5 for _ in range(5)], "A": zero(5), "d": F(1)})
        for name, engine in self.engines():
            for value in bad:
                with (
                    self.subTest(engine=name, value=repr(value)[:160]),
                    self.assertRaises(ValueError),
                ):
                    engine.evaluate(value)

    def test_order_axioms_forbidden_support_and_no_automatic_repair(self):
        chain = copy.deepcopy(base_cases()[2][1])
        bad = []
        reflexive = copy.deepcopy(chain)
        reflexive["C"][0][0] = 1
        bad.append(reflexive)
        missing = copy.deepcopy(chain)
        missing["C"][2][0] = 0
        bad.append(missing)
        cycle = copy.deepcopy(base_cases()[10][1])
        cycle["C"][0][1] = 1
        bad.append(cycle)
        for i, j, value in ((0, 0, F(1)), (0, 1, F(-1)), (1, 2, F(1))):
            altered = copy.deepcopy(chain)
            altered["A"][i][j] = value
            bad.append(altered)
        for name, engine in self.engines():
            for value in bad:
                original = copy.deepcopy(value)
                with self.subTest(engine=name, value=value), self.assertRaises(ValueError):
                    engine.evaluate(value)
                exact(self, value, original)

    def test_inclusive_128_bit_inputs_and_no_output_cutoff(self):
        # Named two-event API boundary controls, not an additional case sweep.
        pair = copy.deepcopy(base_cases()[10][1])
        boundaries = [
            (F(2**127), F(1)),
            (F(-(2**127)), F(1)),
            (F(1, 2**127), F(1)),
            (F(-1, 2**127), F(1)),
            (F(1), F(2**127)),
            (F(1), F(1, 2**127)),
        ]
        for name, engine in self.engines():
            for weight, diagonal in boundaries:
                world = copy.deepcopy(pair)
                world["A"][1][0], world["d"] = weight, diagonal
                G = [[F(1) / diagonal, F(0)], [weight / diagonal**2, F(1) / diagonal]]
                with self.subTest(engine=name, A=weight, d=diagonal):
                    exact(self, engine.evaluate(world), oracle_row(world, G))
            self.assertGreater((F(1) / F(1, 2**127) ** 2).numerator.bit_length(), 128)

    def test_named_maximum_depth_four_chain_boundary(self):
        world = {
            "C": [[int(i > j) for j in range(4)] for i in range(4)],
            "A": [[F(int(i == j + 1)) for j in range(4)] for i in range(4)],
            "d": F(1),
        }
        G = [[F(int(i >= j)) for j in range(4)] for i in range(4)]
        for name, engine in self.engines():
            with self.subTest(engine=name):
                row = engine.evaluate(copy.deepcopy(world))
                exact(self, row, oracle_row(world, G))
                exact(self, row["powers"][3][3][0], F(1))
                exact(self, row["powers"][4], zero(4))
                exact(self, row["G"][3][0], F(1))
                exact(
                    self,
                    [path for path in row["paths"] if len(path["nodes"]) == 4],
                    [{"nodes": [0, 1, 2, 3], "weights": [F(1), F(1), F(1)], "contribution": F(1)}],
                )

    def test_valid_shared_antichain_input_rows_are_accepted_and_copied(self):
        for name, engine in self.engines():
            relation_row = [0, 0, 0]
            weight_row = [F(0), F(0), F(0)]
            supplied = {"C": [relation_row] * 3, "A": [weight_row] * 3, "d": F(1)}
            original = copy.deepcopy(supplied)
            with self.subTest(engine=name):
                row = engine.evaluate(supplied)
                exact(self, row, oracle_row(original, identity(3)))
                exact(self, supplied, original)
                self.assertIs(supplied["C"][0], supplied["C"][1])
                self.assertIs(supplied["A"][0], supplied["A"][1])
                self.assertFalse(mutable_ids(supplied) & mutable_ids(row))

    def test_fresh_containers_no_cross_call_mutation(self):
        for name, engine in self.engines():
            supplied = copy.deepcopy(base_cases()[2][1])
            original = copy.deepcopy(supplied)
            first = engine.evaluate(supplied)
            expected = oracle_row(original, base_cases()[2][2])
            second = engine.evaluate(copy.deepcopy(original))
            self.assertFalse(mutable_ids(first) & mutable_ids(second), name)
            self.assertFalse(mutable_ids(supplied) & mutable_ids(first), name)
            first["world"]["C"][0][0] = 1
            first["world"]["A"][1][0] = F(999)
            first["G"][2][0] = F(999)
            first["paths"][0]["nodes"].append(999)
            exact(self, supplied, original)
            exact(self, second, expected)
            exact(self, engine.evaluate(copy.deepcopy(original)), expected)


class EvidenceTests(unittest.TestCase):
    def test_nine_sources_and_pins_checked_before_protocol_parse(self):
        study = load_study()
        snapshot = study.source_snapshot()
        self.assertEqual(len(study.SOURCE_PATHS), 9)
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

    def test_utility_authentication_regular_file_and_size_refusals(self):
        study = load_study()
        with tempfile.TemporaryDirectory(prefix="qr05-causal-utility-") as directory:
            root = Path(directory)
            untrusted = root / "probe.py"
            untrusted.write_bytes(b"raise AssertionError('untrusted execution')\n")
            oversize = root / "oversize.py"
            oversize.write_bytes(b" " * (study.SOURCE_LIMIT + 1))
            link = root / "link.py"
            link.symlink_to(untrusted)
            for path in (untrusted, oversize, link, root, root / "missing.py"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    study._load_utilities(path)

    def test_native_codec_and_strict_json_refusals(self):
        study = load_study()
        value = {"fraction": F(1), "integer": 1, "flag": True, "rows": []}
        exact(self, study.decode(study.strict_loads(study.canonical(study.encode(value)))), value)
        for left, right in ((F(1), 1), (True, 1), ([], ()), ({"x": 1}, {"x": 1, "extra": 0})):
            with self.assertRaises(ValueError):
                study.require_equal(left, right)
        for blob in (b'{"x":1,"x":2}', b'{"x":1.0}', b'{"x":NaN}'):
            with self.assertRaises(ValueError):
                study.strict_loads(blob)

    def test_authenticated_synthetic_roundtrip_and_exclusive_publication(self):
        study = load_study()
        synthetic = {"value": F(1, 3), "integer": 1, "flag": True}
        with tempfile.TemporaryDirectory(prefix="qr05-causal-evidence-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            with mock.patch.object(study, "analyze", return_value=synthetic):
                artifact = study.freeze(freeze)
                self.assertEqual(artifact["schema"], "qr05-causal-operator-source-freeze-v1")
                self.assertEqual(len(artifact["sources"]), 9)
                exact(self, study.capture(capture, freeze), synthetic)
                exact(self, study.replay(capture, freeze), synthetic)
                with self.assertRaises(FileExistsError):
                    study.freeze(freeze)
                with self.assertRaises(FileExistsError):
                    study.capture(capture, freeze)
                original = capture.read_bytes()
                decoded = json.loads(original)
                self.assertEqual(decoded["schema"], "qr05-causal-operator-capture-v1")
                decoded["report"]["integer"] = True
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

    def test_freeze_schema_identity_runtime_and_canonical_refusals(self):
        study = load_study()
        snapshot = study.source_snapshot()
        with tempfile.TemporaryDirectory(prefix="qr05-causal-freeze-") as directory:
            path = Path(directory) / "freeze.json"
            study.freeze(path)
            original = json.loads(path.read_bytes())
            bad = [
                {**original, field: value}
                for field, value in (("schema", "wrong"), ("sources", {}), ("extra", 1))
            ]
            for field, value in (
                ("optimization", True),
                ("optimization", 3),
                ("version", ""),
                ("implementation", []),
            ):
                bad.append({**original, "runtime": {**original["runtime"], field: value}})
            for value in bad:
                path.write_bytes(study.canonical(value))
                with self.subTest(value=value), self.assertRaises(ValueError):
                    study._checked_freeze(path, snapshot)
            path.write_bytes(study.canonical(original) + b"\n")
            with self.assertRaises(ValueError):
                study._checked_freeze(path, snapshot)

    def test_capture_schema_sources_and_tampering_refuse_before_analysis(self):
        study = load_study()
        with tempfile.TemporaryDirectory(prefix="qr05-causal-capture-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            study.freeze(freeze)
            with mock.patch.object(study, "analyze", return_value={"value": F(1)}):
                study.capture(capture, freeze)
            original = json.loads(capture.read_bytes())
            for field, value in (
                ("schema", "wrong"),
                ("sources", {}),
                ("extra", 1),
                ("freeze_sha256", "0" * 64),
            ):
                capture.write_bytes(study.canonical({**original, field: value}))
                with (
                    self.subTest(field=field),
                    mock.patch.object(
                        study, "analyze", side_effect=AssertionError("early analysis")
                    ),
                    self.assertRaises(ValueError),
                ):
                    study.replay(capture, freeze)

    def test_first_capture_full_native_binding_without_another_analysis(self):
        study, snapshot, _, report = context()
        freeze = study._checked_freeze(HERE / "source-freeze.json", snapshot)
        data = study.read_bounded(HERE / "results.json")
        artifact = study.strict_loads(data)
        self.assertEqual(set(artifact), {"schema", "sources", "freeze_sha256", "report"})
        self.assertEqual(artifact["schema"], "qr05-causal-operator-capture-v1")
        self.assertEqual(study.canonical(artifact), data)
        study.require_equal(artifact["sources"], study.identities(snapshot))
        self.assertEqual(artifact["freeze_sha256"], hashlib.sha256(freeze).hexdigest())
        exact(self, study.decode(artifact["report"]), report)

    def test_complete_route_type_mismatch_and_late_source_drift_refuse(self):
        study, snapshot, _, report = context()
        changed = copy.deepcopy(report)
        changed["rows"][0]["G"][0][0] = 1
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

    def test_freeze_and_source_rechecks_around_capture(self):
        study = load_study()
        snapshot = study.source_snapshot()
        with tempfile.TemporaryDirectory(prefix="qr05-causal-races-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            study.freeze(freeze)
            original = freeze.read_bytes()

            def mutate_freeze(_snapshot):
                freeze.write_bytes(original + b"\n")
                return {"value": F(1)}

            with (
                mock.patch.object(study, "analyze", side_effect=mutate_freeze),
                self.assertRaises(ValueError),
            ):
                study.capture(capture, freeze)
            self.assertFalse(capture.exists())
            freeze.write_bytes(original)
            drifted = {**snapshot, "reference.py": snapshot["reference.py"] + b"\n"}
            with (
                mock.patch.object(study, "source_snapshot", side_effect=[snapshot, drifted]),
                mock.patch.object(study, "analyze", return_value={"value": F(1)}),
                self.assertRaises(ValueError),
            ):
                study.capture(capture, freeze)
            self.assertFalse(capture.exists())

    def test_publication_readback_and_replay_input_stability(self):
        study = load_study()
        with tempfile.TemporaryDirectory(prefix="qr05-causal-publish-") as directory:
            freeze, capture = Path(directory) / "freeze.json", Path(directory) / "capture.json"
            study.freeze(freeze)
            actual_write = study._write_new

            def altered_write(path, blob):
                actual_write(path, blob)
                Path(path).write_bytes(blob + b"\n")

            with (
                mock.patch.object(study, "_write_new", side_effect=altered_write),
                mock.patch.object(study, "analyze", return_value={"value": F(1)}),
                self.assertRaises(ValueError),
            ):
                study.capture(capture, freeze)
            capture.unlink()
            with mock.patch.object(study, "analyze", return_value={"value": F(1)}):
                study.capture(capture, freeze)
            original = capture.read_bytes()

            def alter_capture(_snapshot):
                capture.write_bytes(original + b"\n")
                return {"value": F(1)}

            with (
                mock.patch.object(study, "analyze", side_effect=alter_capture),
                self.assertRaises(ValueError),
            ):
                study.replay(capture, freeze)


if __name__ == "__main__":

    def expired(_signum, _frame):
        raise KeyboardInterrupt("60-second causal-operator suite deadline")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 60)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
