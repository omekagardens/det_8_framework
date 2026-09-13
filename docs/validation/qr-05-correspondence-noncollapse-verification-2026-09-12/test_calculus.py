"""Prospective independent exact oracles; do not execute before source freeze.

Relations are selected by cardinality/combinations, independently of either
engine traversal. Explicit analytical distances, profile gaps and closure
entries supplement reconstruction of every retained ordered discrepancy cell.
"""

import copy
import itertools
import signal
import unittest
from fractions import Fraction as F
from functools import lru_cache
from unittest import mock

VARIANTS = ("identity", "cyclic", "reversal", "rescale")


def load_study():
    # The supported authenticated runner prebinds these frozen driver bytes.
    import study

    return study


@lru_cache(maxsize=1)
def context():
    """One genuine complete two-route study analysis per mathematical suite."""
    study = load_study()
    report = study.build_report()
    return study, report


def exact(test, actual, expected, path="result"):
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
        test.assertIn(type(expected), (F, int, bool, str, type(None)), path)
        test.assertEqual(actual, expected, path)


def mutable_ids(value):
    result = {id(value)} if isinstance(value, (dict, list)) else set()
    children = value.values() if isinstance(value, dict) else value
    if isinstance(value, (dict, list, tuple)):
        for child in children:
            result.update(mutable_ids(child))
    return result


def matrix(n, entries=()):
    result = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, j, value in entries:
        result[i][j] = F(value)
    return result


def transpose(values):
    return [list(column) for column in zip(*values, strict=True)]


def scale(values, factor):
    return [[factor * value for value in row] for row in values]


def relabel(values, mapping):
    n = len(values)
    inverse = [mapping.index(i) for i in range(n)]
    return [[values[inverse[i]][inverse[j]] for j in range(n)] for i in range(n)]


def variant_matrix(values, variant):
    if variant == "cyclic":
        return relabel(values, [(i + 1) % len(values) for i in range(len(values))])
    if variant == "reversal":
        return transpose(values)
    if variant == "rescale":
        return scale(values, F(3, 2))
    return copy.deepcopy(values)


def comparison_bases():
    """The design's fixed seven bases, not fixture/engine-derived inputs."""
    chain = matrix(2, [(0, 1, 1)])
    incoming = matrix(3, [(0, 2, 1), (1, 2, F(11, 10))])
    outgoing = matrix(3, [(0, 1, 1), (0, 2, F(11, 10))])
    return [
        ("zero_multiplicity", matrix(1), matrix(2), F(0), None, None, None),
        ("scale_pair", chain, scale(chain, F(3, 2)), F(1, 2), F(1, 2), F(0), F(0)),
        ("fork_correspondence", incoming, outgoing, F(1, 10), F(1), F(1, 11), F(10, 11)),
        ("duplicate_fork", chain, matrix(3, [(0, 2, 1), (1, 2, 1)]), F(0), None, F(0), None),
        ("near_twins", incoming, chain, F(1, 10), None, F(1, 11), None),
        (
            "endpoint_excess",
            matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 3)]),
            matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 2)]),
            F(1),
            F(1),
            F(1, 6),
            F(1, 6),
        ),
        ("orientation_mismatch", chain, matrix(2, [(0, 1, 1), (1, 0, 1)]), F(1), F(1), F(1), F(1)),
    ]


def inspect_oracle(values):
    d = [list(row) for row in values]
    n = len(d)
    support = [[value > 0 for value in row] for row in d]
    strict = all(not support[i][i] for i in range(n)) and all(
        not (support[i][j] and support[j][k]) or support[i][k]
        for i, j, k in itertools.product(range(n), repeat=3)
    )
    residuals = [
        [i, j, k, d[i][k] - d[i][j] - d[j][k]]
        for i, j, k in itertools.product(range(n), repeat=3)
        if d[i][j] > 0 and d[j][k] > 0
    ]
    gamma = [
        [
            max(
                [abs(d[i][k] - d[j][k]) for k in range(n)]
                + [abs(d[k][i] - d[k][j]) for k in range(n)]
            )
            for j in range(n)
        ]
        for i in range(n)
    ]
    profiles = [tuple(d[i]) + tuple(d[k][i] for k in range(n)) for i in range(n)]
    classes = []
    remaining = set(range(n))
    while remaining:
        first = min(remaining)
        group = [j for j in sorted(remaining) if profiles[j] == profiles[first]]
        classes.append(group)
        remaining.difference_update(group)
    representatives = [group[0] for group in classes]
    return {
        "n": n,
        "kernel": d,
        "diameter": max(value for row in d for value in row),
        "support": support,
        "strict_support": strict,
        "conditional_residuals": residuals,
        "causal_valid": strict and all(row[3] >= 0 for row in residuals),
        "gamma": gamma,
        "gap": min(gamma[i][j] for i in range(n) for j in range(n) if i != j) if n > 1 else None,
        "twins": classes,
        "quotient": [[d[i][j] for j in representatives] for i in representatives],
        "distinguishes": all(len(group) == 1 for group in classes),
    }


def error_oracle(d, e, members):
    errors = [[abs(d[x][xx] - e[y][yy]) for xx, yy in members] for x, y in members]
    maximum = max(value for row in errors for value in row)
    return {
        "errors": errors,
        "maximum": maximum,
        "argmax": [
            [i, j]
            for i, row in enumerate(errors)
            for j, value in enumerate(row)
            if value == maximum
        ],
    }


def relation_oracle(d, e, members):
    members = [list(pair) for pair in sorted(members)]
    a = max(value for row in d for value in row)
    b = max(value for row in e for value in row)
    return {
        "members": members,
        "raw": error_oracle(d, e, members),
        "normalized": error_oracle(scale(d, 1 / a), scale(e, 1 / b), members) if a and b else None,
    }


def onto_relations(m, n):
    """Third route: cardinality strata of Cartesian-member combinations."""
    pairs = list(itertools.product(range(m), range(n)))
    relations = []
    for size in range(max(m, n), m * n + 1):
        for members in itertools.combinations(pairs, size):
            if {x for x, _ in members} == set(range(m)) and {y for _, y in members} == set(
                range(n)
            ):
                relations.append(members)
    return sorted(relations)


def compare_oracle(d, e):
    m, n = len(d), len(e)
    records = [relation_oracle(d, e, members) for members in onto_relations(m, n)]
    x, y = inspect_oracle(d), inspect_oracle(e)
    raw = min(record["raw"]["maximum"] for record in records)
    normalized = bool(x["diameter"] and y["diameter"])
    shape = min(record["normalized"]["maximum"] for record in records) if normalized else None
    bijections = (
        [i for i, record in enumerate(records) if len(record["members"]) == n] if m == n else None
    )
    raw_bijection = (
        min(records[i]["raw"]["maximum"] for i in bijections) if bijections is not None else None
    )
    normalized_bijection = (
        min(records[i]["normalized"]["maximum"] for i in bijections)
        if bijections is not None and normalized
        else None
    )
    return {
        "x": x,
        "y": y,
        "relations": records,
        "raw_distance": raw,
        "normalized_distance": shape,
        "raw_minimizers": [
            i for i, record in enumerate(records) if record["raw"]["maximum"] == raw
        ],
        "normalized_minimizers": [
            i for i, record in enumerate(records) if record["normalized"]["maximum"] == shape
        ]
        if normalized
        else None,
        "bijections": bijections,
        "raw_bijection_distance": raw_bijection,
        "normalized_bijection_distance": normalized_bijection,
        "raw_bijection_minimizers": [
            i for i in bijections if records[i]["raw"]["maximum"] == raw_bijection
        ]
        if bijections is not None
        else None,
        "normalized_bijection_minimizers": [
            i for i in bijections if records[i]["normalized"]["maximum"] == normalized_bijection
        ]
        if bijections is not None and normalized
        else None,
        "bitmask_universe": 2 ** (m * n),
        "safe_gap": all(2 * raw < gap for gap in (x["gap"], y["gap"]) if gap is not None),
    }


def closure_bases():
    order = [[i < j for j in range(3)] for i in range(3)]
    return [
        ("singleton", [[False]], matrix(1), matrix(1)),
        (
            "endpoint_excess",
            order,
            matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 3)]),
            matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 3)]),
        ),
        ("zero_cover", order, matrix(3, [(1, 2, 1)]), matrix(3, [(1, 2, 1), (0, 2, 1)])),
        (
            "unit_all_pairs",
            order,
            matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)]),
            matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 2)]),
        ),
    ]


def reachable(mask):
    n = len(mask)
    result = [[False] * n for _ in range(n)]
    for source in range(n):
        visited = set()
        frontier = {source}
        while frontier:
            next_nodes = {j for i in frontier for j in range(n) if mask[i][j]} - visited
            visited.update(next_nodes)
            frontier = next_nodes
        for target in visited:
            result[source][target] = True
    return result


def residuals(order, weights):
    return [
        [i, j, k, weights[i][k] - weights[i][j] - weights[j][k]]
        for i, j, k in itertools.product(range(len(order)), repeat=3)
        if order[i][j] and order[j][k]
    ]


def closure_oracle(order, weights):
    n = len(order)
    covers = [
        [order[i][j] and not any(order[i][k] and order[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]
    nodes_list = sorted(
        nodes
        for length in range(2, n + 1)
        for nodes in itertools.permutations(range(n), length)
        if all(order[i][j] for i, j in itertools.pairwise(nodes))
    )
    paths = [
        {
            "nodes": list(nodes),
            "weights": [weights[i][j] for i, j in itertools.pairwise(nodes)],
            "sum": sum((weights[i][j] for i, j in itertools.pairwise(nodes)), F(0)),
            "cover_only": all(covers[i][j] for i, j in itertools.pairwise(nodes)),
        }
        for nodes in nodes_list
    ]
    closed, cover_closed = matrix(n), matrix(n)
    maxima, cover_maxima = [], []
    for i, j in itertools.product(range(n), repeat=2):
        if not order[i][j]:
            continue
        indices = [
            k for k, path in enumerate(paths) if path["nodes"][0] == i and path["nodes"][-1] == j
        ]
        only_covers = [k for k in indices if paths[k]["cover_only"]]
        closed[i][j] = max(paths[k]["sum"] for k in indices)
        cover_closed[i][j] = max(paths[k]["sum"] for k in only_covers)
        maxima.append(
            {"pair": [i, j], "paths": [k for k in indices if paths[k]["sum"] == closed[i][j]]}
        )
        cover_maxima.append(
            {
                "pair": [i, j],
                "paths": [k for k in only_covers if paths[k]["sum"] == cover_closed[i][j]],
            }
        )
    input_support = [[value > 0 for value in row] for row in weights]
    return {
        "order": [list(row) for row in order],
        "weights": [list(row) for row in weights],
        "covers": covers,
        "paths": paths,
        "closure": closed,
        "cover_closure": cover_closed,
        "maximizers": maxima,
        "cover_maximizers": cover_maxima,
        "input_support": input_support,
        "closure_support": [[value > 0 for value in row] for row in closed],
        "positive_reachability": reachable(input_support),
        "input_residuals": residuals(order, weights),
        "residuals": residuals(order, closed),
        "covers_positive": all(
            weights[i][j] > 0 for i in range(n) for j in range(n) if covers[i][j]
        ),
    }


def label_map(n, variant):
    return [(i + 1) % n if variant == "cyclic" else i for i in range(n)]


def comparison_case(name, d, e, variant):
    return {
        "id": name + "/" + variant,
        "base": name,
        "variant": variant,
        "x": variant_matrix(d, variant),
        "y": variant_matrix(e, variant),
        "x_map": label_map(len(d), variant),
        "y_map": label_map(len(e), variant),
        "scale": F(3, 2) if variant == "rescale" else F(1),
    }


def closure_case(name, order, weights, variant):
    transformed_order = (
        variant_matrix(order, variant) if variant != "rescale" else copy.deepcopy(order)
    )
    return {
        "id": name + "/" + variant,
        "base": name,
        "variant": variant,
        "order": transformed_order,
        "weights": variant_matrix(weights, variant),
        "map": label_map(len(order), variant),
        "scale": F(3, 2) if variant == "rescale" else F(1),
    }


@lru_cache(maxsize=1)
def expected_rows():
    comparisons, closures = [], []
    for name, d, e, *_distances in comparison_bases():
        for variant in VARIANTS:
            case = comparison_case(name, d, e, variant)
            comparisons.append(
                {
                    "case": case,
                    "inverse_x_map": [case["x_map"].index(i) for i in range(len(d))],
                    "inverse_y_map": [case["y_map"].index(i) for i in range(len(e))],
                    "result": compare_oracle(case["x"], case["y"]),
                }
            )
    for name, order, weights, _closed in closure_bases():
        for variant in VARIANTS:
            case = closure_case(name, order, weights, variant)
            closures.append(
                {
                    "case": case,
                    "inverse_map": [case["map"].index(i) for i in range(len(order))],
                    "result": closure_oracle(case["order"], case["weights"]),
                }
            )
    return comparisons, closures


EXPECTED_CENSUS = {
    "comparison_rows": 28,
    "input_nodes": 132,
    "input_cells": 332,
    "bitmask_universe": 4752,
    "relations": 2380,
    "relation_members": 12576,
    "raw_cells": 69976,
    "normalized_cells": 69960,
    "bijections": 64,
    "closure_rows": 16,
    "closure_nodes": 40,
    "closure_cells": 112,
    "comparable_slots": 36,
}


def control_oracle():
    """Fixed retained controls, with analytic scalar anchors written literally."""
    x = matrix(2, [(0, 1, 1)])
    y = matrix(2, [(0, 1, F(3, 2))])
    z = matrix(2, [(0, 1, 2)])
    identity = [[0, 0], [1, 1]]
    gap_x = matrix(3, [(0, 2, 1), (1, 2, 3)])
    gap_members = [[0, 0], [1, 0], [2, 1]]
    symmetric = matrix(2, [(0, 1, 1), (1, 0, 1)])
    half_symmetric = matrix(2, [(0, 1, F(1, 2)), (1, 0, F(1, 2))])
    excess = matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 3)])
    endpoint_two = matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 2)])
    triple_identity = [[0, 0], [1, 1], [2, 2]]
    order = [[i < j for j in range(3)] for i in range(3)]
    unit = matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)])
    return {
        "triangle": {
            "input": {"chains": [x, y, z], "members": identity},
            "composed_members": [[0, 0], [1, 1]],
            "xy": compare_oracle(x, y),
            "yz": compare_oracle(y, z),
            "xz": compare_oracle(x, z),
            "yx": compare_oracle(y, x),
            "relation_xy": relation_oracle(x, y, identity),
            "relation_yz": relation_oracle(y, z, identity),
            "relation_xz": relation_oracle(x, z, identity),
        },
        "gap_boundary": {
            "input": {"x": gap_x, "y": z, "members": gap_members},
            "comparison": compare_oracle(gap_x, z),
            "relation": relation_oracle(gap_x, z, gap_members),
        },
        "fit_asymmetry": {
            "input": {"a": x, "b": symmetric, "scale": F(1, 2), "members": identity},
            "scaled_b": half_symmetric,
            "a_half_b": compare_oracle(x, half_symmetric),
            "b_a": compare_oracle(symmetric, x),
        },
        "paired_list": {
            "input": {
                "L": [F(1), F(1), F(2)],
                "tau": [F(1), F(1), F(3)],
                "ell": F(1, 2),
                "c": F(3, 4),
            },
            "residuals": [F(1, 4), F(1, 4), F(-1, 4)],
            "u": F(1, 4),
            "mean": F(4, 3),
            "declared": F(1, 8),
            "surrogate": F(3, 16),
            "scale_factor": F(2, 3),
            "lower_bound_identity": F(1),
        },
        "endpoint_trim": {
            "input": {
                "x": excess,
                "y": endpoint_two,
                "members": triple_identity,
                "included": [[0, 1], [1, 2]],
            },
            "relation": relation_oracle(excess, endpoint_two, triple_identity),
            "full_mean": F(1, 9),
            "positive_mean": F(1, 3),
            "trimmed_mean": F(0),
        },
        "lipschitz": {
            "input": {"order": order, "zero": matrix(3), "unit": unit},
            "zero": closure_oracle(order, matrix(3)),
            "unit": closure_oracle(order, unit),
            "input_norm": F(1),
            "output_norm": F(2),
            "bound": F(2),
        },
    }


class CalculusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study, cls.report = context()

    def engines(self):
        return zip(("primary", "reference"), self.study.load_engines(), strict=True)

    def comparison_index(self):
        return {row["case"]["id"]: row["result"] for row in self.report["comparison_rows"]}

    def closure_index(self):
        return {row["case"]["id"]: row["result"] for row in self.report["closure_rows"]}

    def test_complete_native_comparison_oracle(self):
        # Includes every input, relation, raw/normalized matrix, attaining cell,
        # minimizing relation, bijection and unavailable field with exact types.
        exact(self, self.report["comparison_rows"], expected_rows()[0])

    def test_complete_report_schema_and_retained_named_controls(self):
        self.assertEqual(
            set(self.report), {"schema", "comparison_rows", "closure_rows", "controls", "census"}
        )
        exact(self, self.report["schema"], "qr05-correspondence-noncollapse-report-v1")
        exact(self, self.report["controls"], control_oracle())

    def test_complete_native_closure_oracle(self):
        exact(self, self.report["closure_rows"], expected_rows()[1])
        index = self.closure_index()
        for name, _order, _weights, expected in closure_bases():
            for variant in VARIANTS:
                with self.subTest(base=name, variant=variant):
                    exact(
                        self,
                        index[name + "/" + variant]["closure"],
                        variant_matrix(expected, variant),
                    )

    def test_fixed_census_and_cardinality_polynomials(self):
        exact(self, self.report["census"], EXPECTED_CENSUS)
        coefficients = {
            (1, 2): {2: 1},
            (2, 2): {2: 2, 3: 4, 4: 1},
            (2, 3): {3: 6, 4: 12, 5: 6, 6: 1},
            (3, 2): {3: 6, 4: 12, 5: 6, 6: 1},
            (3, 3): {3: 6, 4: 45, 5: 90, 6: 78, 7: 36, 8: 9, 9: 1},
        }
        totals = {key: 0 for key in EXPECTED_CENSUS}
        for row in self.report["comparison_rows"]:
            result = row["result"]
            m, n = result["x"]["n"], result["y"]["n"]
            observed = {}
            for record in result["relations"]:
                size = len(record["members"])
                observed[size] = observed.get(size, 0) + 1
                totals["relation_members"] += size
                totals["raw_cells"] += sum(map(len, record["raw"]["errors"]))
                if record["normalized"] is not None:
                    totals["normalized_cells"] += sum(map(len, record["normalized"]["errors"]))
            self.assertEqual(observed, coefficients[m, n], row["case"]["id"])
            totals["comparison_rows"] += 1
            totals["input_nodes"] += m + n
            totals["input_cells"] += m * m + n * n
            totals["bitmask_universe"] += result["bitmask_universe"]
            totals["relations"] += len(result["relations"])
            totals["bijections"] += len(result["bijections"] or [])
        for row in self.report["closure_rows"]:
            n = len(row["case"]["order"])
            totals["closure_rows"] += 1
            totals["closure_nodes"] += n
            totals["closure_cells"] += n * n
            totals["comparable_slots"] += sum(sum(values) for values in row["case"]["order"])
        exact(self, totals, EXPECTED_CENSUS)

    def test_seven_analytical_optima_and_scale_bounds(self):
        index = self.comparison_index()
        for name, _d, _e, raw, bijection, shape, shape_bijection in comparison_bases():
            for variant in VARIANTS:
                factor = F(3, 2) if variant == "rescale" else F(1)
                result = index[name + "/" + variant]
                with self.subTest(base=name, variant=variant):
                    exact(self, result["raw_distance"], factor * raw)
                    exact(
                        self,
                        result["raw_bijection_distance"],
                        factor * bijection if bijection is not None else None,
                    )
                    exact(self, result["normalized_distance"], shape)
                    exact(self, result["normalized_bijection_distance"], shape_bijection)
                    a, b = result["x"]["diameter"], result["y"]["diameter"]
                    self.assertLessEqual(abs(a - b), result["raw_distance"])
                    self.assertLessEqual(result["raw_distance"], max(a, b))
                    if a and b:
                        self.assertLessEqual(shape, 2 * result["raw_distance"] / max(a, b))
                        self.assertLessEqual(result["raw_distance"], min(a, b) * shape + abs(a - b))

    def test_analytical_gamma_twins_quotient_and_causal_anchors(self):
        index = self.comparison_index()
        incoming_gamma = matrix(
            3,
            [
                (0, 1, F(1, 10)),
                (1, 0, F(1, 10)),
                (0, 2, F(11, 10)),
                (2, 0, F(11, 10)),
                (1, 2, F(11, 10)),
                (2, 1, F(11, 10)),
            ],
        )
        outgoing_gamma = matrix(
            3,
            [
                (0, 1, F(11, 10)),
                (1, 0, F(11, 10)),
                (0, 2, F(11, 10)),
                (2, 0, F(11, 10)),
                (1, 2, F(1, 10)),
                (2, 1, F(1, 10)),
            ],
        )
        fork = index["fork_correspondence/identity"]
        exact(self, fork["x"]["gamma"], incoming_gamma)
        exact(self, fork["y"]["gamma"], outgoing_gamma)
        exact(self, fork["x"]["gap"], F(1, 10))
        duplicate = index["duplicate_fork/identity"]
        exact(self, duplicate["y"]["twins"], [[0, 1], [2]])
        exact(self, duplicate["y"]["quotient"], matrix(2, [(0, 1, 1)]))
        exact(self, duplicate["y"]["gap"], F(0))
        zero = index["zero_multiplicity/identity"]
        exact(self, zero["x"]["gap"], None)
        exact(self, zero["y"]["gap"], F(0))
        exact(self, zero["y"]["twins"], [[0, 1]])
        exact(self, zero["y"]["quotient"], matrix(1))
        excess = index["endpoint_excess/identity"]
        for side, endpoint, gap in (("x", F(3), F(2)), ("y", F(2), F(1))):
            expected = matrix(
                3,
                [
                    (0, 1, gap),
                    (1, 0, gap),
                    (1, 2, gap),
                    (2, 1, gap),
                    (0, 2, endpoint),
                    (2, 0, endpoint),
                ],
            )
            exact(self, excess[side]["gamma"], expected)
            exact(self, excess[side]["gap"], gap)
        for row in self.report["comparison_rows"]:
            for side in ("x", "y"):
                causal = not (row["case"]["base"] == "orientation_mismatch" and side == "y")
                exact(self, row["result"][side]["causal_valid"], causal)

    def test_every_relation_transport_reversal_and_rescaling(self):
        index = self.comparison_index()
        for name, d, e, *_distances in comparison_bases():
            original = index[name + "/identity"]
            for variant in VARIANTS[1:]:
                current = index[name + "/" + variant]
                lookup = {
                    tuple(map(tuple, record["members"])): record for record in current["relations"]
                }
                xm, ym = label_map(len(d), variant), label_map(len(e), variant)
                factor = F(3, 2) if variant == "rescale" else F(1)
                for record in original["relations"]:
                    mapped = [(xm[x], ym[y]) for x, y in record["members"]]
                    ordered = sorted(mapped)
                    inverse = [mapped.index(pair) for pair in ordered]
                    transported = lookup[tuple(ordered)]
                    for channel in ("raw", "normalized"):
                        if record[channel] is None:
                            self.assertIsNone(transported[channel])
                            continue
                        old_errors = record[channel]["errors"]
                        errors = [[old_errors[i][j] for j in inverse] for i in inverse]
                        if variant == "reversal":
                            errors = transpose(errors)
                        if channel == "raw":
                            errors = scale(errors, factor)
                        exact(self, transported[channel]["errors"], errors)
                    exact(self, transported["raw"]["maximum"], factor * record["raw"]["maximum"])
                for side, mapping in (("x", xm), ("y", ym)):
                    gamma = relabel(original[side]["gamma"], mapping)
                    exact(self, current[side]["gamma"], scale(gamma, factor))

    def test_named_correspondence_beats_every_bijection(self):
        result = self.comparison_index()["fork_correspondence/identity"]
        witness = [[0, 0], [1, 0], [2, 1], [2, 2]]
        records = [record for record in result["relations"] if record["members"] == witness]
        self.assertEqual(len(records), 1)
        exact(self, records[0]["raw"]["maximum"], F(1, 10))
        self.assertTrue(
            all(result["relations"][i]["raw"]["maximum"] >= 1 for i in result["bijections"])
        )
        self.assertLess(result["raw_distance"], result["raw_bijection_distance"])
        self.assertFalse(result["safe_gap"])

    def test_all_retained_fiber_bounds_and_safe_gap_minimizers(self):
        comparisons = [row["result"] for row in self.report["comparison_rows"]]
        controls = self.report["controls"]
        comparisons.extend(controls["triangle"][key] for key in ("xy", "yz", "xz", "yx"))
        comparisons.append(controls["gap_boundary"]["comparison"])
        comparisons.extend(controls["fit_asymmetry"][key] for key in ("a_half_b", "b_a"))
        safe_cases = 0
        for result in comparisons:
            left, right = result["x"], result["y"]
            for record in result["relations"]:
                bound = 2 * record["raw"]["maximum"]
                normalized_bound = (
                    2 * record["normalized"]["maximum"]
                    if record["normalized"] is not None
                    else None
                )
                for x, y in record["members"]:
                    for xx, yy in record["members"]:
                        if y == yy:
                            self.assertLessEqual(left["gamma"][x][xx], bound)
                            if normalized_bound is not None:
                                self.assertLessEqual(
                                    left["gamma"][x][xx] / left["diameter"], normalized_bound
                                )
                        if x == xx:
                            self.assertLessEqual(right["gamma"][y][yy], bound)
                            if normalized_bound is not None:
                                self.assertLessEqual(
                                    right["gamma"][y][yy] / right["diameter"], normalized_bound
                                )
            if result["safe_gap"]:
                safe_cases += 1
                self.assertEqual(left["n"], right["n"])
                self.assertIsNotNone(result["bijections"])
                self.assertTrue(set(result["raw_minimizers"]) <= set(result["bijections"]))
                exact(self, result["raw_distance"], result["raw_bijection_distance"])
                exact(self, result["raw_minimizers"], result["raw_bijection_minimizers"])
        # The retained triangle's 3/2 versus 2 pair makes this implication
        # nonvacuous without adding a study row or another engine invocation.
        self.assertGreater(safe_cases, 0)

    def test_named_zero_leg_cover_only_and_idempotence_controls(self):
        index = self.closure_index()
        excess = index["endpoint_excess/identity"]
        exact(self, excess["closure"][0][2], F(3))
        exact(self, excess["cover_closure"][0][2], F(2))
        zero = index["zero_cover/identity"]
        exact(self, zero["input_residuals"], [[0, 1, 2, F(-1)]])
        exact(self, zero["residuals"], [[0, 1, 2, F(0)]])
        self.assertTrue(zero["closure_support"][0][2])
        self.assertFalse(zero["positive_reachability"][0][2])
        self.assertFalse(zero["closure_support"][0][1])
        self.assertFalse(zero["covers_positive"])
        for name, engine in self.engines():
            for base, order, weights, expected in closure_bases():
                with self.subTest(engine=name, base=base):
                    result = engine.closure(order, weights)
                    exact(self, result, closure_oracle(order, weights))
                    exact(self, engine.closure(order, result["closure"])["closure"], expected)
                    self.assertTrue(
                        all(
                            result["closure"][i][j] >= weights[i][j]
                            for i in range(len(order))
                            for j in range(len(order))
                        )
                    )

    def test_all_closure_paths_transport_and_zero_sum_ties(self):
        index = self.closure_index()
        for base, order, _weights, _closed in closure_bases():
            original = index[base + "/identity"]
            for variant in VARIANTS[1:]:
                current = index[base + "/" + variant]
                mapping = label_map(len(order), variant)
                factor = F(3, 2) if variant == "rescale" else F(1)
                transformed = []
                for path in original["paths"]:
                    nodes = [mapping[i] for i in path["nodes"]]
                    weights = [factor * value for value in path["weights"]]
                    if variant == "reversal":
                        nodes.reverse()
                        weights.reverse()
                    transformed.append(
                        {
                            "nodes": nodes,
                            "weights": weights,
                            "sum": factor * path["sum"],
                            "cover_only": path["cover_only"],
                        }
                    )
                transformed.sort(key=lambda path: path["nodes"])
                exact(self, current["paths"], transformed)
        order = [[i < j for j in range(3)] for i in range(3)]
        for name, engine in self.engines():
            with self.subTest(engine=name):
                zero = engine.closure(order, matrix(3))
                exact(self, zero, closure_oracle(order, matrix(3)))
                endpoint = next(record for record in zero["maximizers"] if record["pair"] == [0, 2])
                self.assertEqual(len(endpoint["paths"]), 2)
                self.assertTrue(all(path["sum"] == F(0) for path in zero["paths"]))

    def test_safe_gap_and_zero_distance_quotient_controls(self):
        index = self.comparison_index()
        scale_result = index["scale_pair/identity"]
        # Equality at the smallest gap is not the strict sufficient condition.
        self.assertEqual(2 * scale_result["raw_distance"], scale_result["x"]["gap"])
        self.assertFalse(scale_result["safe_gap"])
        for name, engine in self.engines():
            chain = matrix(2, [(0, 1, 1)])
            with self.subTest(engine=name):
                same = engine.compare(chain, chain)
                exact(self, same, compare_oracle(chain, chain))
                self.assertTrue(same["safe_gap"])
                self.assertEqual(same["raw_minimizers"], same["raw_bijection_minimizers"])
                singleton = engine.compare(matrix(1), matrix(1))
                self.assertTrue(singleton["safe_gap"])
                self.assertIsNone(singleton["normalized_distance"])

    def test_named_triangle_composition_symmetry_and_strict_gap_boundary(self):
        triangle = self.report["controls"]["triangle"]
        exact(self, triangle["composed_members"], [[0, 0], [1, 1]])
        for key, expected in (("xy", F(1, 2)), ("yz", F(1, 2)), ("xz", F(1)), ("yx", F(1, 2))):
            exact(self, triangle[key]["raw_distance"], expected)
        self.assertEqual(
            triangle["xz"]["raw_distance"],
            triangle["xy"]["raw_distance"] + triangle["yz"]["raw_distance"],
        )
        self.assertEqual(
            triangle["relation_xz"]["raw"]["maximum"],
            triangle["relation_xy"]["raw"]["maximum"] + triangle["relation_yz"]["raw"]["maximum"],
        )
        boundary = self.report["controls"]["gap_boundary"]
        result = boundary["comparison"]
        exact(self, result["x"]["gap"], F(2))
        exact(self, result["y"]["gap"], F(2))
        exact(self, result["raw_distance"], F(1))
        exact(self, boundary["relation"]["raw"]["maximum"], F(1))
        self.assertFalse(result["safe_gap"])
        self.assertIsNone(result["bijections"])

    def test_named_one_sided_fit_witness_and_paired_list_scale_factor(self):
        fitted = self.report["controls"]["fit_asymmetry"]
        exact(self, fitted["a_half_b"]["raw_distance"], F(1, 2))
        exact(self, fitted["b_a"]["raw_distance"], F(1))
        # For every onto R, some positive B pair meets a zero A direction.
        # This supplies the c-independent lower bound D_C(B,cA) >= 1;
        # the other direction combines c with the diameter bound |1-c|.
        a, b = fitted["input"]["a"], fitted["input"]["b"]
        for record in fitted["b_a"]["relations"]:
            self.assertTrue(
                any(
                    b[u][v] == F(1) and a[x][y] == F(0)
                    for u, x in record["members"]
                    for v, y in record["members"]
                )
            )
        paired = self.report["controls"]["paired_list"]
        exact(self, paired["lower_bound_identity"], F(1))
        self.assertEqual(4 * paired["u"], paired["lower_bound_identity"])
        self.assertEqual(paired["declared"], paired["scale_factor"] * paired["surrogate"])
        self.assertNotEqual(paired["declared"], paired["surrogate"])

    def test_named_full_supremum_trim_and_sharp_lipschitz(self):
        trimmed = self.report["controls"]["endpoint_trim"]
        exact(self, trimmed["relation"]["raw"]["errors"], matrix(3, [(0, 2, 1)]))
        exact(self, trimmed["relation"]["raw"]["argmax"], [[0, 2]])
        self.assertEqual(trimmed["relation"]["raw"]["maximum"], 9 * trimmed["full_mean"])
        self.assertEqual(trimmed["positive_mean"], F(1, 3))
        self.assertEqual(trimmed["trimmed_mean"], F(0))
        self.assertGreater(trimmed["relation"]["raw"]["maximum"], trimmed["positive_mean"])
        lipschitz = self.report["controls"]["lipschitz"]
        exact(self, lipschitz["input_norm"], F(1))
        exact(self, lipschitz["output_norm"], F(2))
        exact(self, lipschitz["unit"]["closure"][0][2], F(2))
        exact(self, lipschitz["zero"]["closure"][0][2], F(0))
        self.assertEqual(lipschitz["output_norm"], lipschitz["bound"])

    def test_pure_api_tuple_inputs_sorted_members_and_fresh_outputs(self):
        chain = matrix(2, [(0, 1, 1)])
        order = [[False, True], [False, False]]
        for name, engine in self.engines():
            d = tuple(tuple(row) for row in chain)
            supplied_order = tuple(tuple(row) for row in order)
            members = ((1, 1), (0, 0))
            original = copy.deepcopy((d, supplied_order, members))
            with (
                self.subTest(engine=name),
                mock.patch("builtins.open", side_effect=AssertionError("pure API file I/O")),
            ):
                inspection = engine.inspect_kernel(d)
                comparison = engine.compare(d, d)
                record = engine.relation_record(d, d, members)
                closed = engine.closure(supplied_order, d)
            exact(self, inspection, inspect_oracle(chain))
            exact(self, comparison, compare_oracle(chain, chain))
            exact(self, record, relation_oracle(chain, chain, members))
            exact(self, closed, closure_oracle(order, chain))
            self.assertEqual((d, supplied_order, members), original)
            first = engine.compare(chain, chain)
            second = engine.compare(chain, chain)
            self.assertFalse(mutable_ids(first) & mutable_ids(second))
            self.assertFalse(mutable_ids(first) & mutable_ids(chain))
            first["x"]["kernel"][0][1] = F(99)
            first["relations"][0]["members"][0][0] = 99
            exact(self, second, compare_oracle(chain, chain))
            exact(self, chain, matrix(2, [(0, 1, 1)]))

    def test_shared_zero_rows_accepted_without_aliasing_caller(self):
        for name, engine in self.engines():
            zero_row = [F(0)] * 3
            false_row = [False] * 3
            supplied = [zero_row] * 3
            order = [false_row] * 3
            with self.subTest(engine=name):
                inspected = engine.inspect_kernel(supplied)
                closed = engine.closure(order, supplied)
                exact(self, inspected, inspect_oracle(matrix(3)))
                exact(self, closed, closure_oracle([[False] * 3 for _ in range(3)], matrix(3)))
                self.assertFalse(mutable_ids(supplied) & mutable_ids(inspected))
                self.assertFalse(mutable_ids(supplied) & mutable_ids(closed))
                self.assertFalse(mutable_ids(order) & mutable_ids(closed))
                self.assertIs(supplied[0], supplied[1])
                self.assertIs(order[0], order[1])
                exact(self, supplied, matrix(3))

    def test_native_type_refusals(self):
        class ListSubclass(list):
            pass

        class TupleSubclass(tuple):
            pass

        class FractionSubclass(F):
            pass

        class IntSubclass(int):
            pass

        valid = matrix(2, [(0, 1, 1)])
        bad_containers = [
            None,
            {},
            "matrix",
            1,
            ListSubclass(valid),
            TupleSubclass(valid),
            [None, valid[1]],
            [ListSubclass(valid[0]), valid[1]],
            [TupleSubclass(valid[0]), valid[1]],
        ]
        bad_values = []
        for value in (1, False, 1.0, "1", None, FractionSubclass(1)):
            changed = copy.deepcopy(valid)
            changed[0][1] = value
            bad_values.append(changed)
        for name, engine in self.engines():
            for value in bad_containers + bad_values:
                with self.subTest(engine=name, value=repr(value)), self.assertRaises(TypeError):
                    engine.inspect_kernel(value)
            for value in (
                None,
                {},
                ListSubclass([[0, 0], [1, 1]]),
                [(0, 0), (True, 1)],
                [(0, 0), (IntSubclass(1), 1)],
                [(0, 0), (F(1), 1)],
                [ListSubclass([0, 0]), [1, 1]],
            ):
                with self.subTest(engine=name, members=repr(value)), self.assertRaises(TypeError):
                    engine.relation_record(valid, valid, value)
            with self.assertRaises(TypeError):
                engine.closure([[0, 1], [0, 0]], valid)
            with self.assertRaises(TypeError):
                engine.compare(valid, [[F(0), 1], [F(0), F(0)]])
            with self.assertRaises(TypeError):
                engine.closure([[False, True], [False, False]], [[F(0), 1], [F(0), F(0)]])

    def test_shape_range_diagonal_and_relation_refusals(self):
        valid = matrix(2, [(0, 1, 1)])
        bad = [[], matrix(4), [[]], [valid[0]], [valid[0], []], [valid[0], valid[1] + [F(0)]]]
        for value in (F(-1), F(2**128), F(1, 2**128)):
            changed = copy.deepcopy(valid)
            changed[0][1] = value
            bad.append(changed)
        diagonal = copy.deepcopy(valid)
        diagonal[0][0] = F(1)
        bad.append(diagonal)
        malformed_relations = [
            [],
            [[0, 0]],
            [[0, 0], [0, 0], [1, 1]],
            [[0, 0], [1]],
            [[0, 0], [1, 1, 1]],
            [[0, 0], [-1, 1]],
            [[0, 0], [2, 1]],
            [[0, 0], [1, 2]],
        ]
        for name, engine in self.engines():
            for value in bad:
                with self.subTest(engine=name, value=value), self.assertRaises(ValueError):
                    engine.inspect_kernel(value)
            for members in malformed_relations:
                with self.subTest(engine=name, members=members), self.assertRaises(ValueError):
                    engine.relation_record(valid, valid, members)
            with self.assertRaises(ValueError):
                engine.compare(valid, matrix(4))

    def test_invalid_causal_kernels_reported_not_repaired_or_rejected(self):
        symmetric = matrix(2, [(0, 1, 1), (1, 0, 1)])
        short_endpoint = matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)])
        missing_transitive = matrix(3, [(0, 1, 1), (1, 2, 1)])
        for name, engine in self.engines():
            for supplied in (symmetric, short_endpoint, missing_transitive):
                original = copy.deepcopy(supplied)
                with self.subTest(engine=name, supplied=supplied):
                    result = engine.inspect_kernel(supplied)
                    exact(self, result, inspect_oracle(supplied))
                    self.assertFalse(result["causal_valid"])
                    exact(self, supplied, original)
            self.assertTrue(engine.inspect_kernel(short_endpoint)["strict_support"])
            self.assertFalse(engine.inspect_kernel(missing_transitive)["strict_support"])

    def test_order_and_off_order_zero_boundaries(self):
        full = [[i < j for j in range(3)] for i in range(3)]
        zero = matrix(3)
        reflexive = copy.deepcopy(full)
        reflexive[0][0] = True
        missing = copy.deepcopy(full)
        missing[0][2] = False
        cycle = [[False, True, False], [True, False, False], [False, False, False]]
        for name, engine in self.engines():
            for order in (
                reflexive,
                missing,
                cycle,
                [[False]],
                [],
                [[False] * 4 for _ in range(4)],
            ):
                with self.subTest(engine=name, order=order), self.assertRaises(ValueError):
                    engine.closure(order, zero)
            for i, j in ((1, 0), (2, 0), (2, 1)):
                off_order = matrix(3, [(i, j, 1)])
                with self.subTest(engine=name, off_order=(i, j)), self.assertRaises(ValueError):
                    engine.closure(full, off_order)
            antichain = [[False] * 3 for _ in range(3)]
            result = engine.closure(antichain, zero)
            exact(self, result, closure_oracle(antichain, zero))
            exact(self, result["paths"], [])
            self.assertTrue(result["covers_positive"])

    def test_inclusive_128_bit_inputs_and_exact_large_derived_output(self):
        for name, engine in self.engines():
            for value in (F(2**127), F(1, 2**127)):
                supplied = matrix(2, [(0, 1, value)])
                with self.subTest(engine=name, value=value):
                    exact(self, engine.inspect_kernel(supplied), inspect_oracle(supplied))
                    exact(
                        self, engine.compare(supplied, supplied), compare_oracle(supplied, supplied)
                    )
            order = [[i < j for j in range(3)] for i in range(3)]
            weights = matrix(3, [(0, 1, F(2**127)), (1, 2, F(2**127))])
            result = engine.closure(order, weights)
            exact(self, result, closure_oracle(order, weights))
            exact(self, result["closure"][0][2], F(2**128))
            self.assertEqual(result["closure"][0][2].numerator.bit_length(), 129)


if __name__ == "__main__":

    def expired(_signum, _frame):
        raise KeyboardInterrupt("60-second correspondence calculus suite deadline")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 60)
    try:
        unittest.main()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
