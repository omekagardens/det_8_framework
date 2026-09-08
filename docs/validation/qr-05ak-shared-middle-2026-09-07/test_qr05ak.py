"""Bounded independent checks for the private shared-middle diagnostic.

Only tests marked fixed consume authenticated AJ cases. Collection and generic
hands use explicit synthetic data, never fixed fixture calculations.
"""

from __future__ import annotations

import builtins
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from fractions import Fraction as F
from itertools import combinations, pairwise, permutations
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
FAMILIES = ("grid", "warp", "warp_stale", "boost", "dilate")


def fw(value):
    value = F(value)
    return [value.numerator, value.denominator]


def fraction(value):
    assert type(value) is list and len(value) == 2
    n, d = value
    assert type(n) is int and type(d) is int and d > 0
    answer = F(n, d)
    assert [answer.numerator, answer.denominator] == value
    assert max(abs(n).bit_length(), d.bit_length()) <= 4096
    return answer


def native(value):
    if value is None or type(value) in (bool, int, str):
        if type(value) is int:
            assert abs(value).bit_length() <= 4096
        return
    if type(value) is list:
        for child in value:
            native(child)
        return
    if type(value) is dict:
        assert all(type(k) is str for k in value)
        for child in value.values():
            native(child)
        return
    raise AssertionError(f"non-native mathematical type {type(value)}")


def wire(value):
    native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode()


def digest(value):
    return hashlib.sha256(wire(value)).hexdigest()


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def engines():
    return (
        load("_qr05ak_test_primary", "kernel.py"),
        load("_qr05ak_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05ak_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


def rect(values):
    return list(map(fw, values))


def area(bounds):
    a, b, c, d = bounds
    return max(F(), b - a) * max(F(), d - c) / 2


def clipped(bounds, query):
    a, b, c, d = bounds
    u, v, x, y = query
    return max(a, u), min(b, v), max(c, x), min(d, y)


def directed_integral(a, b, c, d):
    assert a <= b and c <= d
    points = sorted({a, b, c, d})
    result = F()
    for left, right in pairwise(points):
        if a <= left < right <= b:
            heights = [max(F(), d - max(c, x)) for x in (left, right)]
            result += (right - left) * sum(heights, F()) / 2
    return result


LINKS = ((0, 1), (1, 2), (0, 2))

PATTERNS = ("all_equal", "first_middle", "first_last", "middle_last", "all_distinct")


def affine_length(a, b, left, right, predecessor):
    def value(y):
        return max(F(), min(b - a, y - a if predecessor else b - y))

    slope = (value(right) - value(left)) / (right - left)
    return value(left) - slope * left, slope


def integral_polynomial(coefficients, left, right):
    return sum(
        (
            c * (right ** (power + 1) - left ** (power + 1)) / (power + 1)
            for power, c in enumerate(coefficients)
        ),
        F(),
    )


def triple_integral(a, b, c, d, e, f):
    # Literal coefficient integration is separate from both positive-part cubic
    # antiderivatives and the reference engine's Simpson evaluations.
    assert a <= b and c <= d and e <= f
    total = F()
    for left, right in pairwise(sorted({a, b, c, d, e, f})):
        if c <= left < right <= d:
            l0, l1 = affine_length(a, b, left, right, True)
            r0, r1 = affine_length(e, f, left, right, False)
            total += integral_polynomial((l0 * r0, l0 * r1 + l1 * r0, l1 * r1), left, right)
    return total


def make_problem(boxlevels, probes, name="synthetic"):
    return {
        "family": name,
        "probes": [{"name": label, "bounds": rect(bounds)} for label, bounds in probes],
        "levels": [
            {
                "level": label,
                "cells": [{"event": event, "bounds": rect(bounds)} for event, bounds in rows],
            }
            for label, rows in boxlevels
        ],
    }


def problem_of():
    return make_problem(
        [
            ("coarse", [(-2, (0, F(1, 2), 0, 1)), (9, (F(1, 2), 1, 0, 1))]),
            (
                "middle",
                [(1, (F(1, 2), 1, 0, 1)), (3, (0, F(1, 4), 0, 1)), (9, (F(1, 4), F(1, 2), 0, 1))],
            ),
            (
                "fine",
                [
                    (-2, (F(1, 4), F(1, 2), 0, 1)),
                    (3, (0, F(1, 4), F(1, 2), 1)),
                    (8, (F(1, 2), 1, 0, 1)),
                    (9, (0, F(1, 4), 0, F(1, 2))),
                ],
            ),
        ],
        [
            ("whole", (0, 1, 0, 1)),
            ("partial", (0, F(3, 8), 0, F(3, 4))),
            ("small", (0, F(1, 8), 0, F(1, 4))),
        ],
    )


def unit_problem():
    return make_problem(
        [
            ("one", [(9, (0, 1, 0, 1))]),
            ("two", [(-2, (F(1, 2), 1, 0, 1)), (9, (0, F(1, 2), 0, 1))]),
            (
                "four",
                [
                    (-2, (0, F(1, 2), F(1, 2), 1)),
                    (3, (F(1, 2), 1, 0, F(1, 2))),
                    (8, (F(1, 2), 1, F(1, 2), 1)),
                    (9, (0, F(1, 2), 0, F(1, 2))),
                ],
            ),
        ],
        [("whole", (0, 1, 0, 1)), ("corner", (0, F(1, 4), 0, F(1, 4)))],
    )


def separated_problem():
    q = F(1, 3)
    cells = [
        (-3, (0, q, 0, q)),
        (-1, (0, q, q, 1)),
        (0, (q, 2 * q, 0, q)),
        (2, (q, 2 * q, q, 2 * q)),
        (5, (q, 2 * q, 2 * q, 1)),
        (8, (2 * q, 1, 0, 2 * q)),
        (9, (2 * q, 1, 2 * q, 1)),
    ]
    return make_problem([(label, cells) for label in ("a", "b", "c")], [("whole", (0, 1, 0, 1))])


def contained(inner, outer):
    a, b, c, d = inner
    x, y, z, t = outer
    return x <= a < b <= y and z <= c < d <= t


def partition_of(parent, children):
    assert all(contained(c, parent) for c in children)
    us = sorted({parent[0], parent[1], *(x for c in children for x in c[:2])})
    vs = sorted({parent[2], parent[3], *(x for c in children for x in c[2:])})
    for a, b in pairwise(us):
        for c, d in pairwise(vs):
            u, v = (a + b) / 2, (c + d) / 2
            if parent[0] < u < parent[1] and parent[2] < v < parent[3]:
                assert sum(x < u < y and z < v < t for x, y, z, t in children) == 1


def ratio(n, d):
    return n / d if d else None


def nullable(value):
    return fw(value) if value is not None else None


def pattern(a, b, c):
    if a == b == c:
        return "all_equal"
    if a == b:
        return "first_middle"
    if a == c:
        return "first_last"
    if b == c:
        return "middle_last"
    return "all_distinct"


def independent_family(problem):
    boxes = [
        {c["event"]: tuple(map(fraction, c["bounds"])) for c in level["cells"]}
        for level in problem["levels"]
    ]
    assert all(
        area(clipped(a, b)) == 0 for level in boxes for a, b in combinations(level.values(), 2)
    )
    maps = {}
    for coarse, fine in LINKS:
        mapping = {}
        for child, bounds in boxes[fine].items():
            parents = [p for p, b in boxes[coarse].items() if contained(bounds, b)]
            assert len(parents) == 1
            mapping[child] = parents[0]
        for p, b in boxes[coarse].items():
            partition_of(b, [boxes[fine][c] for c in mapping if mapping[c] == p])
        maps[coarse, fine] = mapping
    assert all(maps[0, 2][c] == maps[0, 1][maps[1, 2][c]] for c in boxes[2])
    levels, internal = [], []
    for li, rawlevel in enumerate(problem["levels"]):
        geometry, data = [], []
        for probe in problem["probes"]:
            query = tuple(map(fraction, probe["bounds"]))
            clips = {event: clipped(b, query) for event, b in boxes[li].items()}
            hs = {event: area(b) for event, b in clips.items()}
            assert sum(hs.values(), F()) == area(query)
            js = {}
            for a, x in clips.items():
                for b, y in clips.items():
                    js[a, b] = (
                        directed_integral(x[0], x[1], y[0], y[1])
                        * directed_integral(x[2], x[3], y[2], y[3])
                        / 4
                        if hs[a] and hs[b]
                        else F()
                    )
            ts, ps, triples = {}, {}, []
            for a, x in clips.items():
                for b, y in clips.items():
                    for c, z in clips.items():
                        product = hs[a] * hs[b] * hs[c]
                        t = (
                            triple_integral(x[0], x[1], y[0], y[1], z[0], z[1])
                            * triple_integral(x[2], x[3], y[2], y[3], z[2], z[3])
                            / 8
                            if product
                            else F()
                        )
                        p = ratio(js[a, b] * js[b, c], hs[b])
                        ts[a, b, c], ps[a, b, c] = t, p
                        triples.append(
                            {
                                "first": a,
                                "middle": b,
                                "last": c,
                                "volume_product": fw(product),
                                "causal_integral": fw(t),
                                "pair_product": nullable(p),
                                "product_error": nullable(p - t if p is not None else None),
                                "conditional": nullable(ratio(t, product)),
                                "product_conditional": nullable(ratio(p, product))
                                if product
                                else None,
                                "middle_covariance": nullable((t - p) / hs[b] if hs[b] else None),
                            }
                        )
            true_sum = sum(ts.values(), F())
            extended_sum = sum((p for p in ps.values() if p is not None), F())
            assert (
                true_sum == area(query) ** 3 / 36 and sum(js.values(), F()) == area(query) ** 2 / 4
            )
            assert all(ts[a, a, a] == h**3 / 36 for a, h in hs.items())
            geometry.append(
                {
                    "probe": probe["name"],
                    "volume": fw(area(query)),
                    "cells": [{"event": a, "clipped_volume": fw(h)} for a, h in hs.items()],
                    "pairs": [
                        {
                            "first": a,
                            "second": b,
                            "clipped_product": fw(hs[a] * hs[b]),
                            "causal_integral": fw(j),
                            "conditional": nullable(ratio(j, hs[a] * hs[b])),
                        }
                        for (a, b), j in js.items()
                    ],
                    "triples": triples,
                    "summary": {
                        "true_integral": fw(true_sum),
                        "continuum_integral": fw(area(query) ** 3 / 36),
                        "extended_product_sum": fw(extended_sum),
                        "product_error": fw(extended_sum - true_sum),
                    },
                }
            )
            data.append((hs, js, ts, ps))
        levels.append({"level": rawlevel["level"], "geometry": geometry})
        internal.append(data)
    coarsenings = []
    for coarse, fine in LINKS:
        mapping = maps[coarse, fine]
        children = {p: [c for c in boxes[fine] if mapping[c] == p] for p in boxes[coarse]}
        geometry = []
        for qi, probe in enumerate(problem["probes"]):
            hc, _jc, tc, pc = internal[coarse][qi]
            hf, jf, tf, pf = internal[fine][qi]
            blocks = []
            for a, aa in children.items():
                for b, bb in children.items():
                    for c, cc in children.items():
                        child_triples = [(x, y, z) for x in aa for y in bb for z in cc]
                        tsum = sum((tf[row] for row in child_triples), F())
                        assert tsum == tc[a, b, c]
                        patterns = {
                            key: sum(
                                (tf[row] for row in child_triples if pattern(*row) == key), F()
                            )
                            for key in PATTERNS
                        }
                        product = hc[a] * hc[b] * hc[c]
                        weighted = (
                            sum(
                                (
                                    (hf[x] * hf[y] * hf[z] / product)
                                    * (tf[x, y, z] / (hf[x] * hf[y] * hf[z]))
                                    for x, y, z in child_triples
                                    if hf[x] * hf[y] * hf[z]
                                ),
                                F(),
                            )
                            if product
                            else None
                        )
                        psum = (
                            sum((pf[row] for row in child_triples if pf[row] is not None), F())
                            if hc[b]
                            else None
                        )
                        endpoint = (
                            sum(
                                (
                                    sum((jf[x, y] for y in bb), F())
                                    * sum((jf[y, z] for y in bb), F())
                                    / hc[b]
                                    for x in aa
                                    for z in cc
                                ),
                                F(),
                            )
                            if hc[b]
                            else None
                        )
                        middle = (
                            sum(
                                (
                                    sum((jf[x, y] for x in aa), F())
                                    * sum((jf[y, z] for z in cc), F())
                                    / hf[y]
                                    for y in bb
                                    if hf[y]
                                ),
                                F(),
                            )
                            if hc[b]
                            else None
                        )
                        pcoarse = pc[a, b, c]
                        assert endpoint == pcoarse and middle == psum
                        assert weighted == ratio(tsum, product)
                        via = None
                        if (coarse, fine) == (0, 2):
                            ma, mb, mc = (
                                [m for m in boxes[1] if maps[0, 1][m] == parent]
                                for parent in (a, b, c)
                            )
                            descendants = {
                                m: [x for x in boxes[2] if maps[1, 2][x] == m] for m in boxes[1]
                            }
                            via = sum(
                                (
                                    sum(
                                        (
                                            tf[x, y, z]
                                            for x in descendants[i]
                                            for y in descendants[j]
                                            for z in descendants[k]
                                        ),
                                        F(),
                                    )
                                    for i in ma
                                    for j in mb
                                    for k in mc
                                ),
                                F(),
                            )
                            assert via == tsum
                        coarse_error = pcoarse - tsum if pcoarse is not None else None
                        within = psum - tsum if psum is not None else None
                        between = pcoarse - psum if pcoarse is not None else None
                        assert coarse_error is None or coarse_error == within + between
                        blocks.append(
                            {
                                "first": a,
                                "middle": b,
                                "last": c,
                                "children": [list(row) for row in child_triples],
                                "zero_middle_children": sum(not hf[y] for x, y, z in child_triples),
                                "coarse_integral": fw(tc[a, b, c]),
                                "child_integral_sum": fw(tsum),
                                "child_pattern_integrals": {
                                    key: fw(value) for key, value in patterns.items()
                                },
                                "coarse_conditional": nullable(ratio(tsum, product)),
                                "weighted_child_conditional": nullable(weighted),
                                "coarse_pair_product": nullable(pcoarse),
                                "child_pair_product_sum": nullable(psum),
                                "endpoint_refined_product": nullable(endpoint),
                                "middle_refined_product": nullable(middle),
                                "coarse_product_error": nullable(coarse_error),
                                "within_child_error": nullable(within),
                                "between_child_error": nullable(between),
                                "via_middle_integral": nullable(via),
                            }
                        )
            geometry.append(
                {
                    "probe": probe["name"],
                    "volumes": [
                        {
                            "parent": p,
                            "coarse_volume": fw(h),
                            "child_volume_sum": fw(sum((hf[c] for c in children[p]), F())),
                        }
                        for p, h in hc.items()
                    ],
                    "blocks": blocks,
                }
            )
        coarsenings.append(
            {
                "coarse": problem["levels"][coarse]["level"],
                "fine": problem["levels"][fine]["level"],
                "parents": [{"parent": p, "children": cc} for p, cc in children.items()],
                "geometry": geometry,
            }
        )
    triples = [t for level in levels for q in level["geometry"] for t in q["triples"]]
    blocks = [b for link in coarsenings for q in link["geometry"] for b in q["blocks"]]
    errors = [fraction(t["product_error"]) for t in triples if t["product_error"] is not None]
    between = [
        fraction(b["between_child_error"]) for b in blocks if b["between_child_error"] is not None
    ]
    counts = {
        "levels": len(levels),
        "probes": len(problem["probes"]),
        "level_pairs": sum(len(q["pairs"]) for level in levels for q in level["geometry"]),
        "level_triples": len(triples),
        "blocks": len(blocks),
        "child_terms": sum(len(b["children"]) for b in blocks),
        "zero_middle_level_triples": sum(t["pair_product"] is None for t in triples),
        "undefined_level_conditionals": sum(t["conditional"] is None for t in triples),
        "positive_level_errors": sum(x > 0 for x in errors),
        "zero_level_errors": sum(x == 0 for x in errors),
        "negative_level_errors": sum(x < 0 for x in errors),
        "zero_middle_blocks": sum(b["coarse_pair_product"] is None for b in blocks),
        "positive_between_errors": sum(x > 0 for x in between),
        "zero_between_errors": sum(x == 0 for x in between),
        "negative_between_errors": sum(x < 0 for x in between),
        "positive_repeated_region_triples": sum(
            fraction(t["causal_integral"]) > 0 and len({t["first"], t["middle"], t["last"]}) < 3
            for t in triples
        ),
    }
    return {
        "problem": copy.deepcopy(problem),
        "levels": levels,
        "coarsenings": coarsenings,
        "counts": counts,
    }


def centered_covariance(a, b, c):
    # Integrate (L_A-E L_A)(R_C-E R_C) literally over the shared middle
    # rectangle. The bivariate centered polynomials retain their cross terms.
    h = area(b)
    assert h > 0

    def pair(x, y):
        return (
            directed_integral(x[0], x[1], y[0], y[1])
            * directed_integral(x[2], x[3], y[2], y[3])
            / 4
        )

    means = pair(a, b) / h, pair(b, c) / h
    us = sorted({*a[:2], *b[:2], *c[:2]})
    vs = sorted({*a[2:], *b[2:], *c[2:]})
    total = F()
    for u0, u1 in pairwise(us):
        for v0, v1 in pairwise(vs):
            if not (b[0] <= u0 < u1 <= b[1] and b[2] <= v0 < v1 <= b[3]):
                continue
            polys = []
            for bounds, predecessor, mean in ((a, True, means[0]), (c, False, means[1])):
                up = affine_length(*bounds[:2], u0, u1, predecessor)
                vp = affine_length(*bounds[2:], v0, v1, predecessor)
                poly = {(i, j): x * y / 2 for i, x in enumerate(up) for j, y in enumerate(vp)}
                poly[0, 0] -= mean
                polys.append(poly)
            for (i, j), x in polys[0].items():
                for (k, l), y in polys[1].items():
                    total += (
                        x
                        * y
                        * (u1 ** (i + k + 1) - u0 ** (i + k + 1))
                        / (i + k + 1)
                        * (v1 ** (j + l + 1) - v0 ** (j + l + 1))
                        / (j + l + 1)
                    )
    return total / (2 * h)


@pytest.mark.parametrize(
    "factory", [problem_of, unit_problem], ids=["unequal_relabelled", "unit_split"]
)
def test_generic_complete_literal_family_wire(engines, factory):
    p = factory()
    before = wire(p)
    expected = independent_family(p)
    assert expected["counts"]["positive_repeated_region_triples"] > 0
    assert expected["counts"]["zero_middle_level_triples"] > 0
    for module in engines:
        assert wire(module.build_family(p)) == wire(expected) and wire(p) == before


@pytest.mark.parametrize(
    "bounds",
    [
        (0, 1, 0, 1, 0, 1),
        (0, 1, 2, 3, 4, 5),
        (4, 5, 2, 3, 0, 1),
        (0, 2, 1, 3, 2, 4),
        (-2, 1, -1, 2, 0, 3),
        (0, 1, 0, 2, 1, 2),
        (0, 0, 0, 1, 0, 1),
        (0, 1, 1, 1, 0, 2),
        (0, 1, 0, 1, 1, 1),
        (0, 2, 1, 2, 1, 3),
        (0, 1, 1, 2, 2, 3),
        (F(1, 3), F(4, 3), F(-1, 2), F(3, 2), F(2, 3), F(5, 3)),
    ],
)
def test_triple_interval_exact_polynomial_hands_and_all_six_orders(engines, bounds):
    vals = tuple(map(F, bounds))
    intervals = tuple(zip(vals[::2], vals[1::2], strict=True))
    expected = triple_integral(*vals)
    for module in engines:
        assert module.triple_area(*vals) == expected
        assert module.triple_area(*(3 * x - 2 for x in vals)) == 27 * expected
        assert sum(
            (
                module.triple_area(*(x for pair in order for x in pair))
                for order in permutations(intervals)
            ),
            F(),
        ) == ((vals[1] - vals[0]) * (vals[3] - vals[2]) * (vals[5] - vals[4]))


def test_unit_repeated_regions_shared_middle_and_nonadditive_pair_products(engines):
    p = unit_problem()
    expected = independent_family(p)
    row = expected["levels"][0]["geometry"][0]["triples"][0]
    assert row["first"] == row["middle"] == row["last"] == 9
    assert row["causal_integral"] == [1, 288] and row["pair_product"] == [1, 128]
    assert row["conditional"] == [1, 36] and row["product_conditional"] == [1, 16]
    assert row["product_error"] == [5, 1152] and row["middle_covariance"] == [-5, 576]
    block = expected["coarsenings"][0]["geometry"][0]["blocks"][0]
    assert block["coarse_pair_product"] == block["endpoint_refined_product"] == [1, 128]
    assert block["child_pair_product_sum"] == block["middle_refined_product"] == [3, 512]
    assert block["between_child_error"] == [1, 512]
    assert block["child_integral_sum"] == [1, 288]
    assert sum(map(fraction, block["child_pattern_integrals"].values()), F()) == F(1, 288)
    assert any(len(set(child)) < 3 for child in block["children"])
    direct = expected["coarsenings"][2]["geometry"][0]["blocks"][0]
    assert direct["via_middle_integral"] == direct["coarse_integral"] == [1, 288]
    assert any(len(set(child)) == 3 for child in direct["children"])
    assert set(direct["child_pattern_integrals"]) == set(PATTERNS)
    for module in engines:
        assert wire(module.build_family(p)) == wire(expected)


def test_zero_middle_is_undefined_but_zero_endpoint_with_positive_middle_is_defined_zero(engines):
    p = unit_problem()
    expected = independent_family(p)
    rows = {
        (r["first"], r["middle"], r["last"]): r
        for r in expected["levels"][2]["geometry"][1]["triples"]
    }
    empty_middle, empty_endpoint = rows[9, -2, 9], rows[-2, 9, 9]
    for key in (
        "pair_product",
        "product_error",
        "middle_covariance",
        "conditional",
        "product_conditional",
    ):
        assert empty_middle[key] is None
    for key in ("causal_integral", "pair_product", "product_error", "middle_covariance"):
        assert empty_endpoint[key] == [0, 1]
    assert empty_endpoint["conditional"] is None and empty_endpoint["product_conditional"] is None
    blocks = expected["coarsenings"][1]["geometry"][1]["blocks"]
    empty = next(b for b in blocks if b["middle"] == -2)
    assert empty["coarse_integral"] == empty["child_integral_sum"] == [0, 1]
    for key in (
        "coarse_pair_product",
        "child_pair_product_sum",
        "endpoint_refined_product",
        "middle_refined_product",
        "coarse_product_error",
        "within_child_error",
        "between_child_error",
    ):
        assert empty[key] is None
    assert empty["zero_middle_children"] == len(empty["children"])
    positive = expected["coarsenings"][2]["geometry"][1]["blocks"][0]
    assert 0 < positive["zero_middle_children"] < len(positive["children"])
    for module in engines:
        assert wire(module.build_family(p)) == wire(expected)


@pytest.mark.parametrize(
    "boxes",
    [
        ((0, 1, 0, 1), (0, 1, 0, 1), (0, 1, 0, 1)),
        ((0, F(1, 2), 0, 1), (F(1, 4), F(3, 4), 0, 1), (F(1, 2), 1, F(1, 3), 1)),
        ((0, 1, 0, 1), (2, 3, 2, 3), (4, 5, 4, 5)),
    ],
)
def test_centered_middle_covariance_is_literal_not_only_a_renamed_difference(engines, boxes):
    a, b, c = [tuple(map(F, x)) for x in boxes]
    expected = centered_covariance(a, b, c)
    for module in engines:
        t = (
            module.triple_area(*a[:2], *b[:2], *c[:2])
            * module.triple_area(*a[2:], *b[2:], *c[2:])
            / 8
        )
        left = module.causal_area(*a[:2], *b[:2]) * module.causal_area(*a[2:], *b[2:]) / 4
        right = module.causal_area(*b[:2], *c[:2]) * module.causal_area(*b[2:], *c[2:]) / 4
        assert (t - left * right / area(b)) / area(b) == expected
    if a == b == c:
        assert expected == F(-5, 576)


def test_strictly_separated_regions_have_positive_exact_composition_equality(engines):
    p = separated_problem()
    expected = independent_family(p)
    rows = {
        (r["first"], r["middle"], r["last"]): r
        for r in expected["levels"][0]["geometry"][0]["triples"]
    }
    yes, reverse = rows[-3, 2, 9], rows[9, 2, -3]
    assert yes["causal_integral"] == yes["pair_product"] == [1, 5832]
    assert yes["conditional"] == yes["product_conditional"] == [1, 1]
    assert yes["product_error"] == yes["middle_covariance"] == [0, 1]
    assert reverse["causal_integral"] == reverse["pair_product"] == [0, 1]
    for module in engines:
        assert wire(module.build_family(p)) == wire(expected)


MALFORMED = (
    "extra",
    "marks",
    "level_count",
    "duplicate_level",
    "duplicate_id",
    "bool_id",
    "unsorted_id",
    "unreduced",
    "outside_query",
    "degenerate",
    "overlap_hole",
    "nonnested",
    "hidden_hole",
)


def malformed_problem(kind):
    p = problem_of()
    if kind == "extra":
        p["triple_answers"] = []
    elif kind == "marks":
        p["levels"][2]["cells"][0]["supplied_mark"] = [1, 1]
    elif kind == "level_count":
        p["levels"].pop()
    elif kind == "duplicate_level":
        p["levels"][1]["level"] = p["levels"][0]["level"]
    elif kind == "duplicate_id":
        p["levels"][0]["cells"][1]["event"] = -2
    elif kind == "bool_id":
        p["levels"][0]["cells"][0]["event"] = False
    elif kind == "unsorted_id":
        p["levels"][2]["cells"].reverse()
    elif kind == "unreduced":
        p["levels"][2]["cells"][0]["bounds"][0] = [2, 8]
    elif kind == "outside_query":
        p["probes"][0]["bounds"] = rect((0, 2, 0, 1))
    elif kind == "degenerate":
        p["levels"][2]["cells"][0]["bounds"] = rect((0, 0, 0, 1))
    elif kind == "overlap_hole":
        p["levels"][0]["cells"][0]["bounds"] = rect((0, F(3, 4), 0, 1))
        p["levels"][0]["cells"][1]["bounds"] = rect((F(1, 2), F(3, 4), 0, 1))
    elif kind == "nonnested":
        for cell, bounds in zip(
            p["levels"][1]["cells"],
            ((F(3, 5), 1, 0, 1), (0, F(2, 5), 0, 1), (F(2, 5), F(3, 5), 0, 1)),
            strict=True,
        ):
            cell["bounds"] = rect(bounds)
    elif kind == "hidden_hole":
        p["probes"] = p["probes"][-1:]
        p["levels"][2]["cells"][2]["bounds"] = rect((F(1, 2), F(9, 10), 0, 1))
    else:
        raise AssertionError(kind)
    return p


@pytest.mark.parametrize("kind", MALFORMED)
def test_bounded_geometry_only_input_consistency_and_full_lineage(engines, kind):
    for module in engines:
        with pytest.raises(ValueError):
            module.build_family(malformed_problem(kind))


def test_no_hidden_file_reads_no_mutation_and_detached_outputs(engines, monkeypatch):
    p = unit_problem()
    before, expected = wire(p), wire(independent_family(p))

    def forbidden(*args, **kwargs):
        raise RuntimeError("mathematical engine read a hidden file")

    with monkeypatch.context() as patch:
        for host, name in (
            (builtins, "open"),
            (os, "open"),
            (Path, "open"),
            (Path, "read_bytes"),
            (Path, "read_text"),
        ):
            patch.setattr(host, name, forbidden)
        for module in engines:
            a, b = module.build_family(p), module.build_family(p)
            assert wire(a) == wire(b) == expected and wire(p) == before
            a["problem"]["levels"][0]["cells"][0]["bounds"][0][0] = -1
            a["levels"][0]["geometry"][0]["triples"][0]["causal_integral"][0] = -1
            assert (
                wire(b) == expected
                and wire(p) == before
                and wire(module.build_family(p)) == expected
            )


@pytest.fixture
def lifecycle(runner, tmp_path, monkeypatch):
    identity = {
        "source_ledger": {"source": {"bytes": 1, "sha256": "fixed"}},
        "prior_artifacts": {"prior": {"bytes": 1, "sha256": "fixed"}},
        "ancestor_sources": {"ancestor": {"bytes": 1, "sha256": "fixed"}},
    }
    monkeypatch.setattr(runner, "identities", lambda: copy.deepcopy(identity))
    monkeypatch.setattr(runner, "run_suite", lambda route="compare": {"totals": {"stub": 1}})
    monkeypatch.setattr(runner.platform, "platform", lambda: "lifecycle-test-platform")
    monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=1, optimize=0))
    monkeypatch.setattr(sys, "pycache_prefix", str(tmp_path / "external-cache"))
    return runner, tmp_path / "capture.json"


def test_capture_create_only_and_both_readonly_routes_preserve_runtime(lifecycle):
    runner, path = lifecycle
    created = runner.capture(path)
    before = path.read_bytes()
    assert created["status"] == "CREATED_EXACT_FINITE_RESULT"
    with pytest.raises(FileExistsError):
        runner.capture(path)
    for route in ("primary", "reference"):
        replay = runner.capture(path, route=route, verify=True)
        assert replay["status"] == "VERIFIED_EXACT_REPLAY" and replay["sha256"] == created["sha256"]
        assert path.read_bytes() == before


@pytest.mark.parametrize(
    "field", ["schema_version", "source_ledger", "prior_artifacts", "ancestor_sources", "suite"]
)
def test_capture_replay_rejects_changed_evidence_without_overwriting(lifecycle, field):
    runner, path = lifecycle
    runner.capture(path)
    envelope = json.loads(path.read_bytes())
    envelope[field] = "changed"
    raw = runner.canonical(envelope)
    path.write_bytes(raw)
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    assert path.read_bytes() == raw


@pytest.mark.parametrize("kind", ["extra", "noncanonical", "wrong_type"])
def test_capture_requires_known_canonical_envelope(lifecycle, kind):
    runner, path = lifecycle
    runner.capture(path)
    raw = path.read_bytes()
    if kind == "noncanonical":
        changed = b" " + raw
    elif kind == "extra":
        changed = runner.canonical({**json.loads(raw), "extra": 0})
    else:
        changed = runner.canonical([])
    path.write_bytes(changed)
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    assert path.read_bytes() == changed


@pytest.mark.parametrize("verify", [False, True])
def test_capture_never_follows_result_symlink(lifecycle, verify):
    runner, path = lifecycle
    target = path.with_name("untouched.json")
    target.write_bytes(b"original")
    path.symlink_to(target)
    with pytest.raises(ValueError if verify else FileExistsError):
        runner.capture(path, verify=verify)
    assert target.read_bytes() == b"original"


def test_capture_identity_change_midrun_prevents_write(lifecycle, monkeypatch):
    runner, path = lifecycle

    def changed(route="compare"):
        monkeypatch.setattr(runner, "identities", lambda: {"changed": True})
        return {"totals": {"stub": 1}}

    monkeypatch.setattr(runner, "run_suite", changed)
    with pytest.raises(ValueError):
        runner.capture(path)
    assert not path.exists()


def test_capture_replay_detects_concurrent_artifact_change(lifecycle, monkeypatch):
    runner, path = lifecycle
    runner.capture(path)

    def changed(route="compare"):
        path.write_bytes(b"concurrent")
        return {"totals": {"stub": 1}}

    monkeypatch.setattr(runner, "run_suite", changed)
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    assert path.read_bytes() == b"concurrent"


@pytest.mark.parametrize("kind", ["not_isolated", "no_cache", "root_cache", "checkout_cache"])
def test_capture_runtime_boundary(lifecycle, monkeypatch, kind):
    runner, path = lifecycle
    if kind == "not_isolated":
        monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=0, optimize=0))
    elif kind == "no_cache":
        monkeypatch.setattr(sys, "pycache_prefix", None)
    elif kind == "root_cache":
        monkeypatch.setattr(sys, "pycache_prefix", runner.ROOT.anchor)
    else:
        monkeypatch.setattr(sys, "pycache_prefix", str(runner.ROOT / "local-cache"))
    with pytest.raises(ValueError):
        runner.capture(path)
    assert not path.exists()


@pytest.mark.parametrize("verify", [False, True])
def test_capture_size_caps_are_live_without_overwrite(lifecycle, monkeypatch, verify):
    runner, path = lifecycle
    if verify:
        runner.capture(path)
        before = path.read_bytes()
    monkeypatch.setattr(runner, "MAX_CAPTURE_BYTES", 2)
    with pytest.raises(ValueError):
        runner.capture(path, verify=verify)
    if verify:
        assert path.read_bytes() == before
    else:
        assert not path.exists()


def test_working_suite_byte_cap_prevents_capture(lifecycle, monkeypatch):
    runner, path = lifecycle
    monkeypatch.setattr(runner, "MAX_WORKING_BYTES", 2)
    with pytest.raises(ValueError):
        runner.capture(path)
    assert not path.exists()


@pytest.mark.parametrize(
    "value",
    [
        {"totals": (1,)},
        {"totals": {"value": F(1, 2)}},
        {"totals": {"value": 1.0}},
        {"totals": {"value": 1 << 4096}},
    ],
)
def test_mathematical_suite_requires_native_bounded_integer_components(
    lifecycle, monkeypatch, value
):
    runner, path = lifecycle
    monkeypatch.setattr(runner, "run_suite", lambda route="compare": value)
    with pytest.raises(ValueError):
        runner.capture(path)
    assert not path.exists()


def test_readonly_mathematical_comparison_distinguishes_bool_from_integer(runner):
    with pytest.raises(ValueError):
        runner.verify_suite({"value": True}, {"value": 1})


def test_large_translation_cancels_unretained_cubics_without_changing_measures(engines):
    old = make_problem(
        [(name, [(1, (0, 1, 0, 1))]) for name in ("a", "b", "c")], [("whole", (0, 1, 0, 1))]
    )
    p = copy.deepcopy(old)
    shift = 1 << 4090
    for row in [*p["probes"], *(c for level in p["levels"] for c in level["cells"])]:
        row["bounds"] = [fw(fraction(x) + shift) for x in row["bounds"]]
    expected = independent_family(old)
    expected["problem"] = p
    for module in engines:
        assert wire(module.build_family(p)) == wire(expected)


def test_retained_triple_overflow_is_not_hidden_by_bounded_pair_components(engines):
    side = F(1 << 800)
    h = side * side / 2
    assert (h * h / 4).numerator.bit_length() <= 4096 < (h**3 / 36).numerator.bit_length()
    p = make_problem(
        [(name, [(1, (0, side, 0, side))]) for name in ("a", "b", "c")],
        [("whole", (0, side, 0, side))],
    )
    for module in engines:
        with pytest.raises(ValueError):
            module.build_family(p)


@pytest.mark.parametrize("optimized", [False, True])
def test_bounded_explicit_guards_survive_optimization(tmp_path, optimized):
    program = r"""
import importlib.util, json, pathlib, sys
directory = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ak_guard_tests", directory / "test_qr05ak.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
count = 0
def reject(fn, *args):
    global count
    try:
        fn(*args)
    except ValueError:
        count += 1
    else:
        raise RuntimeError("invalid input accepted")
for name, filename in (("primary", "kernel.py"), ("reference", "reference.py")):
    m = t.load("ak_guard_" + name, filename)
    for kind in t.MALFORMED:
        reject(m.build_family, t.malformed_problem(kind))
    for args in ((True,1,0,1), (0.0,1,0,1), (1,0,0,1), (0,1,1,0), ("0",1,0,1)):
        reject(m.causal_area, *args)
    for args in ((True,1,0,1,0,1), (0.0,1,0,1,0,1), ("0",1,0,1,0,1),
                 (1,0,0,1,0,1), (0,1,1,0,0,1), (0,1,0,1,1,0)):
        reject(m.triple_area, *args)
    p = t.unit_problem()
    before, expected = t.wire(p), t.wire(t.independent_family(p))
    first, second = m.build_family(p), m.build_family(p)
    if t.wire(first) != expected or t.wire(second) != expected or t.wire(p) != before:
        raise RuntimeError("generic complete wire or input changed")
    first["levels"][0]["geometry"][0]["triples"][0]["causal_integral"][0] = -1
    if t.wire(second) != expected or t.wire(p) != before:
        raise RuntimeError("output alias leaked")
if count != 48:
    raise RuntimeError("guard inventory changed")
print(json.dumps({"rejections": count, "engines": 2}))
"""
    args = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'cache'}"]
    if optimized:
        args.append("-O")
    result = subprocess.run(
        [*args, "-c", program, str(HERE)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    assert json.loads(result.stdout) == {"rejections": 48, "engines": 2}


def independent_inputs(previous):
    assert len(previous) == 5
    problems = []
    for family, old in zip(FAMILIES, previous, strict=True):
        source = old["problem"]
        assert source["family"] == family
        assert [level["level"] for level in source["levels"]] == ["l0", "l1", "l2"]
        assert [len(level["cells"]) for level in source["levels"]] == [6, 7, 8]
        assert len(source["probes"]) == 5
        problems.append(
            {
                "family": family,
                "probes": copy.deepcopy(source["probes"]),
                "levels": [
                    {
                        "level": level["level"],
                        "cells": [
                            {"event": c["event"], "bounds": copy.deepcopy(c["bounds"])}
                            for c in level["cells"]
                        ],
                    }
                    for level in source["levels"]
                ],
            }
        )
    return problems, previous


@pytest.fixture(scope="session")
def fixed_inputs(runner):
    # Lazy: only marked fixed tests use this authenticated historical input.
    path = HERE.parent / "qr-05aj-pair-coarsening-2026-09-07/results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 1825670
    assert (
        hashlib.sha256(raw).hexdigest()
        == "4be2fbc4a7f62322416fd2a2e256a529eb03f54fad3ca88674c060d31d94e8d1"
    )
    previous = json.loads(raw)["suite"]["families"]
    problems, consumed = independent_inputs(previous)
    actual, prior = runner.load_inputs()
    assert wire(actual) == wire(problems) and wire(prior) == wire(consumed)
    return problems, consumed


@pytest.fixture(scope="session")
def expected_families(fixed_inputs):
    return [independent_family(p) for p in fixed_inputs[0]]


@pytest.fixture(scope="session")
def actual_families(fixed_inputs, engines):
    outputs = []
    for problem in fixed_inputs[0]:
        pair = []
        for module in engines:
            supplied = copy.deepcopy(problem)
            before = wire(supplied)
            pair.append(module.build_family(supplied))
            assert wire(supplied) == before
        outputs.append(pair)
    return outputs


@pytest.mark.fixed
@pytest.mark.parametrize("index", range(5), ids=FAMILIES)
def test_fixed_all_five_complete_literal_engine_wires(actual_families, expected_families, index):
    expected = wire(expected_families[index])
    assert all(wire(actual) == expected for actual in actual_families[index])


def geometric_projection(family, scale=F(1)):
    powers = {
        **dict.fromkeys(("volume", "clipped_volume", "coarse_volume", "child_volume_sum"), 1),
        **dict.fromkeys(("clipped_product", "middle_covariance"), 2),
        **dict.fromkeys(
            (
                "volume_product",
                "pair_product",
                "product_error",
                "true_integral",
                "continuum_integral",
                "extended_product_sum",
                "coarse_integral",
                "child_integral_sum",
                "coarse_pair_product",
                "child_pair_product_sum",
                "endpoint_refined_product",
                "middle_refined_product",
                "coarse_product_error",
                "within_child_error",
                "between_child_error",
                "via_middle_integral",
            ),
            3,
        ),
    }

    def visit(value, path=()):
        if value is None:
            return None
        key = path[-1] if path else None
        power = powers.get(key)
        if key == "causal_integral":
            power = 2 if "pairs" in path else 3
        if len(path) > 1 and path[-2] == "child_pattern_integrals":
            power = 3
        if power is not None:
            return fw(fraction(value) * scale**power)
        if type(value) is dict:
            return {k: visit(v, (*path, k)) for k, v in value.items()}
        if type(value) is list:
            return [visit(v, (*path, i)) for i, v in enumerate(value)]
        return value

    return visit({k: family[k] for k in ("levels", "coarsenings", "counts")})


def independent_controls(families):
    by = {family["problem"]["family"]: family for family in families}
    assert wire(geometric_projection(by["boost"])) == wire(geometric_projection(by["grid"]))
    assert wire(geometric_projection(by["dilate"])) == wire(geometric_projection(by["grid"], F(4)))
    assert wire(geometric_projection(by["warp_stale"])) == wire(geometric_projection(by["warp"]))
    assert wire({k: v for k, v in by["warp_stale"]["problem"].items() if k != "family"}) == wire(
        {k: v for k, v in by["warp"]["problem"].items() if k != "family"}
    )
    return {"boost": True, "dilation": True, "stale_geometric": True}


def independent_bridges(families, previous):
    names = []
    projected, _ = independent_inputs(previous)
    assert wire([f["problem"] for f in families]) == wire(projected)
    for family, old in zip(families, previous, strict=True):
        assert family["problem"]["family"] == old["problem"]["family"]
        names.append(family["problem"]["family"])
        assert len(family["levels"]) == len(old["levels"])
        for level, prior in zip(family["levels"], old["levels"], strict=True):
            assert level["level"] == prior["level"] and len(level["geometry"]) == len(
                prior["geometry"]
            )
            for current, oldquery in zip(level["geometry"], prior["geometry"], strict=True):
                assert wire(
                    {key: current[key] for key in ("probe", "volume", "cells", "pairs")}
                ) == wire(oldquery)
    return {
        "AJ_family_names": names,
        "AJ_projected_inputs_equal": True,
        "AJ_complete_clipped_volumes_and_pairs_equal": True,
        "AJ_coarsening_math_replayed": False,
        "other_prior_math_replayed": False,
    }


@pytest.fixture(scope="session")
def expected_suite(expected_families, fixed_inputs):
    totals = {"families": len(expected_families)}
    totals.update(
        {
            key: sum(f["counts"][key] for f in expected_families)
            for key in expected_families[0]["counts"]
        }
    )
    return {
        "families": expected_families,
        "controls": independent_controls(expected_families),
        "prior_bridges": independent_bridges(expected_families, fixed_inputs[1]),
        "totals": totals,
        "scope": dict.fromkeys(
            (
                "generic_production_API_hardened",
                "unknown_geometry_reconstructed",
                "marks_authenticated",
                "continuum_limit_established",
                "cross_level_observation_transport_proved",
                "higher_chain_composition_closed",
                "universal_pair_summary_insufficiency_proved",
                "stochastic_transition_constructed",
                "quantum_channel_constructed",
                "gravity_derived",
                "empirical_data_used",
                "ret_integration_tested",
            ),
            False,
        ),
    }


@pytest.mark.fixed
def test_fixed_complete_suite_and_all_AJ_pair_volume_projections(
    runner, actual_families, expected_suite, fixed_inputs
):
    actual = runner.assemble_suite([pair[0] for pair in actual_families], fixed_inputs[1])
    assert wire(actual) == wire(expected_suite)
    runner.verify_suite(actual, expected_suite)


@pytest.mark.fixed
@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_route_orchestration_uses_only_declared_engines(
    runner, fixed_inputs, expected_suite, monkeypatch, route
):
    # All five real two-engine wires are independently compared above; cached
    # exact outputs isolate only route orchestration in these three tests.
    calls = []
    by = {f["problem"]["family"]: f for f in expected_suite["families"]}

    def loader(name):
        def build(problem):
            target = by[problem["family"]]
            assert wire(problem) == wire(target["problem"])
            calls.append((name, problem["family"]))
            return copy.deepcopy(target)

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    monkeypatch.setattr(runner, "load_inputs", lambda: fixed_inputs)
    assert wire(runner.run_suite(route)) == wire(expected_suite)
    names = ("primary", "reference") if route == "compare" else (route,)
    assert calls == [(name, family) for family in FAMILIES for name in names]


def at_path(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def add_fraction(tree, path):
    return replaced(tree, path, fw(fraction(at_path(tree, path)) + 1))


@pytest.mark.fixed
def test_fixed_nonvacuous_triple_and_coarsening_corruptions(runner, expected_families):
    original = expected_families[0]
    q = ("levels", 0, "geometry", 0)
    t = (*q, "triples", 0)
    block = ("coarsenings", 2, "geometry", 0, "blocks", 0)
    directed_path = next(
        (*q, "triples", i)
        for i, row in enumerate(at_path(original, (*q, "triples")))
        if row["first"] != row["last"]
    )
    directed = at_path(original, directed_path)
    pair = at_path(original, (*q, "pairs", 1))
    zero_middle = next(
        ("levels", li, "geometry", qi, "triples", ti, "pair_product")
        for li, level in enumerate(original["levels"])
        for qi, query in enumerate(level["geometry"])
        for ti, row in enumerate(query["triples"])
        if row["pair_product"] is None
    )
    changes = [
        add_fraction(original, ("problem", "levels", 0, "cells", 0, "bounds", 0)),
        add_fraction(original, (*q, "volume")),
        replaced(
            original, (*q, "pairs", 1), {**pair, "first": pair["second"], "second": pair["first"]}
        ),
        add_fraction(original, (*t, "causal_integral")),
        add_fraction(original, (*t, "pair_product")),
        add_fraction(original, (*t, "product_error")),
        add_fraction(original, (*t, "middle_covariance")),
        add_fraction(original, (*t, "conditional")),
        replaced(original, zero_middle, [0, 1]),
        replaced(
            original,
            directed_path,
            {**directed, "first": directed["last"], "last": directed["first"]},
        ),
        add_fraction(original, (*q, "summary", "product_error")),
        replaced(original, ("coarsenings", 2, "parents", 0, "children"), []),
        replaced(original, (*block, "children"), at_path(original, (*block, "children"))[:-1]),
        replaced(
            original,
            (*block, "zero_middle_children"),
            at_path(original, (*block, "zero_middle_children")) + 1,
        ),
        replaced(
            original,
            (*block, "child_pattern_integrals"),
            {
                key: fw(fraction(value) + 1)
                for key, value in at_path(original, (*block, "child_pattern_integrals")).items()
            },
        ),
        add_fraction(original, (*block, "weighted_child_conditional")),
        add_fraction(original, (*block, "child_integral_sum")),
        add_fraction(original, (*block, "child_pair_product_sum")),
        add_fraction(original, (*block, "endpoint_refined_product")),
        add_fraction(original, (*block, "middle_refined_product")),
        add_fraction(original, (*block, "within_child_error")),
        add_fraction(original, (*block, "between_child_error")),
        add_fraction(original, (*block, "via_middle_integral")),
        replaced(original, ("counts", "child_terms"), original["counts"]["child_terms"] + 1),
    ]
    assert len(changes) == 24
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_nonvacuous_suite_claims_and_stale_problem_control(runner, expected_suite):
    original = expected_suite
    changes = [
        replaced(original, ("controls", "boost"), False),
        replaced(original, ("controls", "dilation"), False),
        replaced(original, ("controls", "stale_geometric"), False),
        replaced(original, ("prior_bridges", "AJ_coarsening_math_replayed"), True),
        replaced(original, ("scope", "universal_pair_summary_insufficiency_proved"), True),
        replaced(original, ("scope", "higher_chain_composition_closed"), True),
        replaced(original, ("totals", "blocks"), original["totals"]["blocks"] + 1),
        replaced(original, ("prior_bridges", "AJ_family_names"), []),
    ]
    assert len(changes) == 8
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    # Ninth corruption changes only stale-warp problem geometry; unchanged
    # computed output cannot be used to claim the supplied inputs are equal.
    badfamilies = add_fraction(original["families"], (2, "problem", "probes", 0, "bounds", 0))
    assert wire(badfamilies) != wire(original["families"])
    with pytest.raises(ValueError):
        runner.controls(badfamilies)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_AJ_geometry_projection_corruptions_are_checked_not_merely_flagged(
    runner, expected_families, fixed_inputs
):
    original = fixed_inputs[1][0]
    q = ("levels", 0, "geometry", 0)
    pair = at_path(original, (*q, "pairs", 1))
    changes = [
        add_fraction(original, (*q, "volume")),
        add_fraction(original, (*q, "cells", 0, "clipped_volume")),
        add_fraction(original, (*q, "pairs", 0, "clipped_product")),
        add_fraction(original, (*q, "pairs", 0, "causal_integral")),
        replaced(
            original, (*q, "pairs", 1), {**pair, "first": pair["second"], "second": pair["first"]}
        ),
        replaced(original, (*q, "pairs"), at_path(original, (*q, "pairs"))[:-1]),
    ]
    assert len(changes) == 6
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.aj_bridges(expected_families, [bad, *fixed_inputs[1][1:]])
    assert wire(original) == before
