"""Bounded independent checks for the private middle-moment diagnostic.

Only tests marked fixed consume authenticated AK cases. Collection and generic
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
from itertools import combinations, pairwise
from math import comb
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
        load("_qr05al_test_primary", "kernel.py"),
        load("_qr05al_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05al_test_runner", "study.py")


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
    # Direct shared-middle polynomial integration is independent of the AL
    # primary's Gram contractions and the reference's Simpson evaluations.
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


POWERS = tuple((i, j) for i in range(3) for j in range(3))
BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))


def power_integral(a, b, p):
    # Factored endpoint-power sum: independent of subtracting antiderivatives
    # and of the reference's tensor-Simpson evaluations.
    return (b - a) * sum((a**i * b ** (p - i) for i in range(p + 1)), F()) / (p + 1)


def raw_moments(bounds):
    a, b, c, d = bounds
    return [power_integral(a, b, i) * power_integral(c, d, j) / 2 for i, j in POWERS]


def gram(moments):
    return [[moments[3 * (i + k) + j + l] for k, l in BASIS] for i, j in BASIS]


def coefficients(endpoint, tile, incoming):
    if area(endpoint) == 0:
        return [F()] * 4
    lines = []
    for axis in (0, 2):
        a, b = endpoint[axis : axis + 2]
        left, right = tile[axis : axis + 2]
        # Two strict interior nodes, not the engine's endpoint/corner recipe.
        x, y = (2 * left + right) / 3, (left + 2 * right) / 3

        def length(z, a=a, b=b):
            return max(F(), min(b - a, z - a if incoming else b - z))

        slope = (length(y) - length(x)) / (y - x)
        lines.append((length(x) - slope * x, slope))
    return [lines[0][i] * lines[1][j] / 2 for i, j in BASIS]


def mean_integral(coeff, moments):
    return sum((x * moments[3 * i + j] for x, (i, j) in zip(coeff, BASIS, strict=True)), F())


def product_integral(left, right, moments):
    # Convolve the two bivariate polynomials first, then integrate the nine
    # monomials. No flattened 4x4 production contraction is reused.
    poly = {(i, j): F() for i, j in POWERS}
    for x, (i, j) in zip(left, BASIS, strict=True):
        for y, (k, l) in zip(right, BASIS, strict=True):
            poly[i + k, j + l] += x * y
    return sum((poly[key] * value for key, value in zip(POWERS, moments, strict=True)), F())


def centered(left, right, mean_left, mean_right, moments):
    a, b = left.copy(), right.copy()
    a[0] -= mean_left
    b[0] -= mean_right
    return product_integral(a, b, moments)


def middle_contract(event, clips):
    bounds = clips[event]
    if not area(bounds):
        return {
            "event": event,
            "bounds": None,
            "u_breaks": [],
            "v_breaks": [],
            "moments": [[0, 1] for _ in POWERS],
            "tiles": [],
        }, []
    breaks = []
    for axis in (0, 2):
        lo, hi = bounds[axis : axis + 2]
        breaks.append(
            sorted(
                {
                    lo,
                    hi,
                    *(
                        v
                        for other in clips.values()
                        if area(other)
                        for v in other[axis : axis + 2]
                        if lo < v < hi
                    ),
                }
            )
        )
    tiles, internal = [], []
    for u0, u1 in pairwise(breaks[0]):
        for v0, v1 in pairwise(breaks[1]):
            tile = u0, u1, v0, v1
            moments = raw_moments(tile)
            incoming = {a: coefficients(box, tile, True) for a, box in clips.items()}
            outgoing = {a: coefficients(box, tile, False) for a, box in clips.items()}
            left = {a: mean_integral(c, moments) for a, c in incoming.items()}
            right = {a: mean_integral(c, moments) for a, c in outgoing.items()}
            internal.append((moments, incoming, outgoing, left, right))
            tiles.append(
                {
                    "bounds": rect(tile),
                    "moments": list(map(fw, moments)),
                    "incoming": [
                        {"event": a, "coefficients": list(map(fw, c))} for a, c in incoming.items()
                    ],
                    "outgoing": [
                        {"event": a, "coefficients": list(map(fw, c))} for a, c in outgoing.items()
                    ],
                }
            )
    moments = raw_moments(bounds)
    assert [sum((t[0][i] for t in internal), F()) for i in range(9)] == moments
    return {
        "event": event,
        "bounds": rect(bounds),
        "u_breaks": list(map(fw, breaks[0])),
        "v_breaks": list(map(fw, breaks[1])),
        "moments": list(map(fw, moments)),
        "tiles": tiles,
    }, internal


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
    levels, internals = [], []
    for li, level in enumerate(problem["levels"]):
        geometry, data = [], []
        for probe in problem["probes"]:
            query = tuple(map(fraction, probe["bounds"]))
            clips = {a: clipped(b, query) for a, b in boxes[li].items()}
            hs = {a: area(b) for a, b in clips.items()}
            assert sum(hs.values(), F()) == area(query)
            middle_rows, contracts, middle_moments = [], {}, {}
            for b in clips:
                row, contract = middle_contract(b, clips)
                middle_rows.append(row)
                contracts[b] = contract
                middle_moments[b] = list(map(fraction, row["moments"]))
            js = {}
            for a, x in clips.items():
                for b, y in clips.items():
                    js[a, b] = (
                        directed_integral(*x[:2], *y[:2]) * directed_integral(*x[2:], *y[2:]) / 4
                        if hs[a] * hs[b]
                        else F()
                    )
                    assert sum((tile[3][a] for tile in contracts[b]), F()) == js[a, b]
                    assert sum((tile[4][b] for tile in contracts[a]), F()) == js[a, b]
            triples, ts = [], {}
            for a, x in clips.items():
                for b, y in clips.items():
                    for c, z in clips.items():
                        volume = hs[a] * hs[b] * hs[c]
                        true = (
                            triple_integral(*x[:2], *y[:2], *z[:2])
                            * triple_integral(*x[2:], *y[2:], *z[2:])
                            / 8
                            if volume
                            else F()
                        )
                        ts[a, b, c] = true
                        assert (
                            sum(
                                (
                                    product_integral(inc[a], out[c], mom)
                                    for mom, inc, out, _, _ in contracts[b]
                                ),
                                F(),
                            )
                            == true
                        )
                        p = ratio(js[a, b] * js[b, c], hs[b])
                        ptile = (
                            sum(
                                (
                                    left[a] * right[c] / mom[0]
                                    for mom, _, _, left, right in contracts[b]
                                ),
                                F(),
                            )
                            if hs[b]
                            else None
                        )
                        cent = (
                            sum(
                                (
                                    centered(
                                        inc[a], out[c], js[a, b] / hs[b], js[b, c] / hs[b], mom
                                    )
                                    for mom, inc, out, _, _ in contracts[b]
                                ),
                                F(),
                            )
                            if hs[b]
                            else None
                        )
                        within = (
                            sum(
                                (
                                    centered(
                                        inc[a], out[c], left[a] / mom[0], right[c] / mom[0], mom
                                    )
                                    for mom, inc, out, left, right in contracts[b]
                                ),
                                F(),
                            )
                            if hs[b]
                            else None
                        )
                        assert cent is None or cent == true - p
                        assert within is None or within == true - ptile
                        triples.append(
                            {
                                "first": a,
                                "middle": b,
                                "last": c,
                                "volume_product": fw(volume),
                                "causal_integral": fw(true),
                                "pair_product": nullable(p),
                                "product_error": nullable(p - true if p is not None else None),
                                "conditional": nullable(ratio(true, volume)),
                                "product_conditional": nullable(p / volume if volume else None),
                                "middle_covariance": nullable(cent / hs[b] if hs[b] else None),
                                "tile_pair_product": nullable(ptile),
                                "tile_product_error": nullable(
                                    ptile - true if ptile is not None else None
                                ),
                                "between_tile_error": nullable(
                                    p - ptile if p is not None else None
                                ),
                                "tile_product_conditional": nullable(
                                    ptile / volume if volume else None
                                ),
                                "centered_integral": nullable(cent),
                                "within_tile_centered_integral": nullable(within),
                            }
                        )
            true_sum = sum(ts.values(), F())
            original_sum = sum(
                (fraction(t["pair_product"]) for t in triples if t["pair_product"] is not None), F()
            )
            tile_sum = sum(
                (
                    fraction(t["tile_pair_product"])
                    for t in triples
                    if t["tile_pair_product"] is not None
                ),
                F(),
            )
            assert (
                true_sum == area(query) ** 3 / 36 and sum(js.values(), F()) == area(query) ** 2 / 4
            )
            geometry.append(
                {
                    "probe": probe["name"],
                    "volume": fw(area(query)),
                    "cells": [{"event": a, "clipped_volume": fw(h)} for a, h in hs.items()],
                    "middles": middle_rows,
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
                        "original_product_sum": fw(original_sum),
                        "tile_product_sum": fw(tile_sum),
                        "original_error": fw(original_sum - true_sum),
                        "tile_error": fw(tile_sum - true_sum),
                        "between_error": fw(original_sum - tile_sum),
                    },
                }
            )
            data.append((hs, ts, middle_moments))
        levels.append({"level": level["level"], "geometry": geometry})
        internals.append(data)
    coarsenings = []
    for coarse, fine in LINKS:
        children = {
            p: [c for c in boxes[fine] if maps[coarse, fine][c] == p] for p in boxes[coarse]
        }
        geometry = []
        for qi, probe in enumerate(problem["probes"]):
            _hc, tc, mc = internals[coarse][qi]
            _hf, tf, mf = internals[fine][qi]
            moment_blocks = []
            for p, cc in children.items():
                summed = [sum((mf[c][i] for c in cc), F()) for i in range(9)]
                assert summed == mc[p]
                moment_blocks.append(
                    {
                        "parent": p,
                        "children": cc,
                        "coarse_moments": list(map(fw, mc[p])),
                        "child_moment_sum": list(map(fw, summed)),
                    }
                )
            blocks = []
            for a, aa in children.items():
                for b, bb in children.items():
                    for c, cc in children.items():
                        rows = [(x, y, z) for x in aa for y in bb for z in cc]
                        summed = sum((tf[row] for row in rows), F())
                        assert summed == tc[a, b, c]
                        via = None
                        if (coarse, fine) == (0, 2):
                            ma, mb, mmc = (
                                [m for m in boxes[1] if maps[0, 1][m] == p] for p in (a, b, c)
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
                                    for k in mmc
                                ),
                                F(),
                            )
                            assert via == summed
                        blocks.append(
                            {
                                "first": a,
                                "middle": b,
                                "last": c,
                                "children": [list(row) for row in rows],
                                "coarse_integral": fw(tc[a, b, c]),
                                "child_integral_sum": fw(summed),
                                "via_middle_integral": nullable(via),
                            }
                        )
            geometry.append(
                {"probe": probe["name"], "moment_blocks": moment_blocks, "blocks": blocks}
            )
        coarsenings.append(
            {
                "coarse": problem["levels"][coarse]["level"],
                "fine": problem["levels"][fine]["level"],
                "parents": [{"parent": p, "children": cc} for p, cc in children.items()],
                "geometry": geometry,
            }
        )
    middles = [m for level in levels for q in level["geometry"] for m in q["middles"]]
    tiles = [tile for m in middles for tile in m["tiles"]]
    triples = [t for level in levels for q in level["geometry"] for t in q["triples"]]
    blocks = [b for link in coarsenings for q in link["geometry"] for b in q["blocks"]]
    mblocks = [m for link in coarsenings for q in link["geometry"] for m in q["moment_blocks"]]
    counts = {
        "levels": len(levels),
        "probes": len(problem["probes"]),
        "level_pairs": sum(len(q["pairs"]) for level in levels for q in level["geometry"]),
        "level_triples": len(triples),
        "blocks": len(blocks),
        "child_terms": sum(len(b["children"]) for b in blocks),
        "middle_cells": len(middles),
        "positive_middle_cells": sum(m["bounds"] is not None for m in middles),
        "tiles": len(tiles),
        "breakpoint_entries": sum(len(m["u_breaks"]) + len(m["v_breaks"]) for m in middles),
        "middle_bound_entries": sum(len(m["bounds"]) for m in middles if m["bounds"] is not None),
        "tile_bound_entries": sum(len(t["bounds"]) for t in tiles),
        "middle_moment_entries": sum(len(m["moments"]) for m in middles),
        "tile_moment_entries": sum(len(t["moments"]) for t in tiles),
        "coefficient_vectors": sum(
            len(t[direction]) for t in tiles for direction in ("incoming", "outgoing")
        ),
        "coefficient_entries": sum(
            len(row["coefficients"])
            for t in tiles
            for direction in ("incoming", "outgoing")
            for row in t[direction]
        ),
        "coarsening_moment_blocks": len(mblocks),
        "coarsening_moment_entries": sum(
            len(m["coarse_moments"]) + len(m["child_moment_sum"]) for m in mblocks
        ),
        "zero_middle_level_triples": sum(t["pair_product"] is None for t in triples),
        "undefined_level_conditionals": sum(t["conditional"] is None for t in triples),
        "positive_triples": sum(fraction(t["causal_integral"]) > 0 for t in triples),
    }
    for label, field in (
        ("original", "product_error"),
        ("tile", "tile_product_error"),
        ("between", "between_tile_error"),
    ):
        values = [fraction(t[field]) for t in triples if t[field] is not None]
        for sign, predicate in (
            ("positive", lambda x: x > 0),
            ("zero", lambda x: x == 0),
            ("negative", lambda x: x < 0),
        ):
            counts[f"{label}_{sign}_errors"] = sum(predicate(x) for x in values)
    return {
        "problem": copy.deepcopy(problem),
        "levels": levels,
        "coarsenings": coarsenings,
        "counts": counts,
    }


def five_cell_problem():
    q = F(1, 3)
    cells = [
        (-3, (0, 2 * q, 0, q)),
        (0, (2 * q, 1, 0, q)),
        (2, (0, 1, q, 2 * q)),
        (7, (0, q, 2 * q, 1)),
        (9, (q, 1, 2 * q, 1)),
    ]
    return make_problem([(name, cells) for name in ("a", "b", "c")], [("whole", (0, 1, 0, 1))])


def transported_moments(values, alpha, beta, du=F(), dv=F()):
    moments = dict(zip(POWERS, values, strict=True))
    return [
        alpha
        * beta
        * sum(
            (
                F(comb(i, r) * comb(j, s))
                * alpha**r
                * du ** (i - r)
                * beta**s
                * dv ** (j - s)
                * moments[r, s]
                for r in range(i + 1)
                for s in range(j + 1)
            ),
            F(),
        )
        for i, j in POWERS
    ]


def transported_coefficients(values, alpha, beta, du=F(), dv=F()):
    result = {key: F() for key in BASIS}
    for value, (i, j) in zip(values, BASIS, strict=True):
        for r in range(i + 1):
            for s in range(j + 1):
                result[r, s] += (
                    value
                    * alpha
                    * beta
                    * comb(i, r)
                    * comb(j, s)
                    * (-du) ** (i - r)
                    * (-dv) ** (j - s)
                    / alpha**i
                    / beta**j
                )
    return [result[key] for key in BASIS]


def affine_family(value, alpha, beta, du=F(), dv=F(), path=()):
    if value is None:
        return None
    key = path[-1] if path else None
    factor = alpha * beta
    if key == "bounds":
        return [
            fw(fraction(x) * scale + shift)
            for x, scale, shift in zip(
                value, (alpha, alpha, beta, beta), (du, du, dv, dv), strict=True
            )
        ]
    if key in ("u_breaks", "v_breaks"):
        scale, shift = (alpha, du) if key == "u_breaks" else (beta, dv)
        return [fw(fraction(x) * scale + shift) for x in value]
    if key in ("moments", "coarse_moments", "child_moment_sum"):
        return list(map(fw, transported_moments(list(map(fraction, value)), alpha, beta, du, dv)))
    if key == "coefficients":
        return list(
            map(fw, transported_coefficients(list(map(fraction, value)), alpha, beta, du, dv))
        )
    powers = {
        **dict.fromkeys(("volume", "clipped_volume"), 1),
        **dict.fromkeys(("clipped_product", "middle_covariance"), 2),
        **dict.fromkeys(
            (
                "volume_product",
                "pair_product",
                "product_error",
                "tile_pair_product",
                "tile_product_error",
                "between_tile_error",
                "centered_integral",
                "within_tile_centered_integral",
                "true_integral",
                "continuum_integral",
                "original_product_sum",
                "tile_product_sum",
                "original_error",
                "tile_error",
                "between_error",
                "coarse_integral",
                "child_integral_sum",
                "via_middle_integral",
            ),
            3,
        ),
    }
    power = powers.get(key)
    if key == "causal_integral":
        power = 2 if "pairs" in path else 3
    if power is not None:
        return fw(fraction(value) * factor**power)
    if type(value) is dict:
        return {k: affine_family(v, alpha, beta, du, dv, (*path, k)) for k, v in value.items()}
    if type(value) is list:
        return [affine_family(v, alpha, beta, du, dv, (*path, i)) for i, v in enumerate(value)]
    return value


def evaluate(coeff, u, v):
    return sum((c * u**i * v**j for c, (i, j) in zip(coeff, BASIS, strict=True)), F())


def check_contract(family):
    for level, source in zip(family["levels"], family["problem"]["levels"], strict=True):
        for query, probe in zip(level["geometry"], family["problem"]["probes"], strict=True):
            bounds = tuple(map(fraction, probe["bounds"]))
            clips = {
                c["event"]: clipped(tuple(map(fraction, c["bounds"])), bounds)
                for c in source["cells"]
            }
            for middle in query["middles"]:
                whole = list(map(fraction, middle["moments"]))
                assert whole == [
                    sum((fraction(t["moments"][i]) for t in middle["tiles"]), F()) for i in range(9)
                ]
                for tile in middle["tiles"]:
                    box = tuple(map(fraction, tile["bounds"]))
                    values = list(map(fraction, tile["moments"]))
                    assert values == raw_moments(box)
                    matrix = gram(values)
                    m = [values[3 * i + j] for i, j in BASIS]
                    centered_matrix = [
                        [matrix[i][j] - m[i] * m[j] / values[0] for j in range(4)] for i in range(4)
                    ]
                    assert matrix == [list(row) for row in zip(*matrix, strict=True)]
                    assert matrix[0][0] == area(box) and matrix[1][2] == matrix[0][3] == values[4]
                    assert (
                        centered_matrix[0] == [F()] * 4
                        and [r[0] for r in centered_matrix] == [F()] * 4
                    )
                    for vector in (
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                        [1, -2, 3, -4],
                        [-4, 0, 1, 2],
                    ):
                        assert (
                            sum(
                                (
                                    vector[i] * matrix[i][j] * vector[j]
                                    for i in range(4)
                                    for j in range(4)
                                ),
                                F(),
                            )
                            > 0
                        )
                        assert (
                            sum(
                                (
                                    vector[i] * centered_matrix[i][j] * vector[j]
                                    for i in range(4)
                                    for j in range(4)
                                ),
                                F(),
                            )
                            >= 0
                        )
                    for direction in ("incoming", "outgoing"):
                        assert [row["event"] for row in tile[direction]] == list(clips)
                        for row in tile[direction]:
                            coeff = list(map(fraction, row["coefficients"]))
                            endpoint = clips[row["event"]]
                            assert len(coeff) == 4
                            for u in ((2 * box[0] + box[1]) / 3, (box[0] + 2 * box[1]) / 3):
                                for v in ((2 * box[2] + box[3]) / 3, (box[2] + 2 * box[3]) / 3):
                                    lengths = [
                                        max(
                                            F(),
                                            min(
                                                endpoint[k + 1] - endpoint[k],
                                                x - endpoint[k]
                                                if direction == "incoming"
                                                else endpoint[k + 1] - x,
                                            ),
                                        )
                                        for k, x in ((0, u), (2, v))
                                    ]
                                    direct = lengths[0] * lengths[1] / 2 if area(endpoint) else F()
                                    assert evaluate(coeff, u, v) == direct
    counts = family["counts"]
    assert counts["middle_bound_entries"] == 4 * counts["positive_middle_cells"]
    assert counts["tile_bound_entries"] == 4 * counts["tiles"]
    assert counts["middle_moment_entries"] == 9 * counts["middle_cells"]
    assert counts["tile_moment_entries"] == 9 * counts["tiles"]
    assert counts["coefficient_entries"] == 4 * counts["coefficient_vectors"]
    assert counts["coarsening_moment_entries"] == 18 * counts["coarsening_moment_blocks"]


@pytest.mark.parametrize(
    "factory",
    [unit_problem, problem_of, five_cell_problem],
    ids=["unit", "unequal_relabelled", "two_controls"],
)
def test_generic_complete_family_literal_oracle_and_contract(engines, factory):
    p = factory()
    expected = independent_family(p)
    check_contract(expected)
    before = wire(p)
    for module in engines:
        actual = module.build_family(p)
        assert wire(actual) == wire(expected) and wire(p) == before
        check_contract(actual)


def test_unit_unsplit_tile_requires_within_tile_dependence(engines):
    for module in engines:
        family = module.build_family(unit_problem())
        query = family["levels"][0]["geometry"][0]
        tile = query["middles"][0]["tiles"][0]
        assert len(query["middles"][0]["tiles"]) == 1
        assert tile["moments"] == [fw(F(1, 2 * (i + 1) * (j + 1))) for i, j in POWERS]
        assert tile["incoming"][0]["coefficients"] == rect((0, 0, 0, F(1, 2)))
        assert tile["outgoing"][0]["coefficients"] == rect((F(1, 2), F(-1, 2), F(-1, 2), F(1, 2)))
        triple = query["triples"][0]
        assert triple["causal_integral"] == [1, 288]
        assert triple["pair_product"] == triple["tile_pair_product"] == [1, 128]
        assert triple["middle_covariance"] == [-5, 576]
        assert triple["centered_integral"] == triple["within_tile_centered_integral"] == [-5, 1152]
        assert triple["between_tile_error"] == [0, 1]


def test_five_cell_control_separates_breakpoints_from_within_tile_moments(engines):
    for module in engines:
        family = module.build_family(five_cell_problem())
        query = family["levels"][0]["geometry"][0]
        middle = next(m for m in query["middles"] if m["event"] == 2)
        assert middle["u_breaks"] == rect((0, F(1, 3), F(2, 3), 1)) and len(middle["tiles"]) == 3
        triple = next(
            t for t in query["triples"] if (t["first"], t["middle"], t["last"]) == (-3, 2, 9)
        )
        assert triple["causal_integral"] == [25, 34992]
        assert triple["pair_product"] == [2, 2187] and triple["tile_pair_product"] == [17, 23328]
        assert triple["between_tile_error"] == [13, 69984] and triple["tile_product_error"] == [
            1,
            69984,
        ]
        assert triple["centered_integral"] == [-7, 34992]
        assert triple["within_tile_centered_integral"] == [-1, 69984]


@pytest.mark.parametrize(
    "bounds", [(0, 1, 0, 1), (-2, 1, -3, -1), (F(1, 3), F(4, 3), F(-5, 2), F(1, 2)), (2, 3, 5, 9)]
)
def test_rectangle_moments_signed_nonsquare_and_binomial_affine_transport(engines, bounds):
    box = tuple(map(F, bounds))
    alpha, beta, du, dv = F(2), F(3), F(3), F(-5)
    moved = tuple(
        x * s + d for x, s, d in zip(box, (alpha, alpha, beta, beta), (du, du, dv, dv), strict=True)
    )
    expected = raw_moments(box)
    assert transported_moments(expected, alpha, beta, du, dv) == raw_moments(moved)
    for module in engines:
        assert module.rectangle_moments(rect(box)) == list(map(fw, expected))
        assert module.rectangle_moments(rect(moved)) == list(map(fw, raw_moments(moved)))
    if box == (F(-2), F(1), F(-3), F(-1)):
        assert expected[1] < 0 and expected[3] < 0


def test_full_affine_transport_changes_raw_payload_not_only_scalar_answers(engines):
    p = five_cell_problem()
    old = independent_family(p)
    expected = affine_family(old, F(2), F(3), F(3), F(-5))
    assert wire(expected) == wire(independent_family(expected["problem"]))
    assert (
        expected["levels"][0]["geometry"][0]["middles"]
        != old["levels"][0]["geometry"][0]["middles"]
    )
    for module in engines:
        assert wire(module.build_family(expected["problem"])) == wire(expected)


def test_empty_middle_has_no_tiles_and_empty_endpoint_keeps_full_zero_vectors(engines):
    for module in engines:
        family = module.build_family(unit_problem())
        query = family["levels"][2]["geometry"][1]
        empty = next(m for m in query["middles"] if m["event"] == -2)
        assert empty == {
            "event": -2,
            "bounds": None,
            "u_breaks": [],
            "v_breaks": [],
            "moments": [[0, 1] for _ in range(9)],
            "tiles": [],
        }
        positive = next(m for m in query["middles"] if m["event"] == 9)
        for tile in positive["tiles"]:
            for direction in ("incoming", "outgoing"):
                assert next(r for r in tile[direction] if r["event"] == -2)["coefficients"] == [
                    [0, 1] for _ in range(4)
                ]
        triples = {(t["first"], t["middle"], t["last"]): t for t in query["triples"]}
        for key in (
            "pair_product",
            "tile_pair_product",
            "product_error",
            "tile_product_error",
            "between_tile_error",
            "middle_covariance",
            "centered_integral",
            "within_tile_centered_integral",
        ):
            assert triples[9, -2, 9][key] is None and triples[-2, 9, 9][key] == [0, 1]
        assert triples[-2, 9, 9]["tile_product_conditional"] is None


def test_no_hidden_artifact_reads_or_input_output_aliases(engines, monkeypatch):
    p = unit_problem()
    before, expected = wire(p), wire(independent_family(p))

    def forbidden(*args, **kwargs):
        raise RuntimeError("mathematical engine read hidden input")

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
            first, second = module.build_family(p), module.build_family(p)
            assert wire(first) == wire(second) == expected and wire(p) == before
            first["levels"][0]["geometry"][0]["middles"][0]["tiles"][0]["moments"][0][0] = -1
            first["problem"]["levels"][0]["cells"][0]["bounds"][0][0] = -1
            assert (
                wire(second) == expected
                and wire(p) == before
                and wire(module.build_family(p)) == expected
            )


def test_retained_raw_moment_overflow_rejects_even_when_scalar_geometry_is_translation_invariant(
    engines,
):
    shift = F(1 << 1100)
    box = (shift, shift + 1, shift, shift + 1)
    assert all(abs(x.numerator).bit_length() <= 4096 for x in box)
    assert raw_moments(box)[-1].numerator.bit_length() > 4096
    p = make_problem([(name, [(1, box)]) for name in ("a", "b", "c")], [("whole", box)])
    for module in engines:
        with pytest.raises(ValueError):
            module.rectangle_moments(rect(box))
        with pytest.raises(ValueError):
            module.build_family(p)


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
def test_basic_geometry_only_admission_and_lineage(engines, kind):
    for module in engines:
        with pytest.raises(ValueError):
            module.build_family(malformed_problem(kind))


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


def invalid_rectangles():
    bounds = rect((0, 1, 0, 1))
    return [
        tuple(bounds),
        replaced(bounds, (0, 0), False),
        replaced(bounds, (0, 1), 0),
        replaced(bounds, (1,), [2, 2]),
        replaced(bounds, (0, 0), 0.0),
        rect((0, 0, 0, 1)),
        rect((1, 0, 0, 1)),
        bounds[:-1],
    ]


@pytest.mark.parametrize("index", range(8))
def test_rectangle_moment_admission_is_explicit_and_native(engines, index):
    for module in engines:
        with pytest.raises(ValueError):
            module.rectangle_moments(invalid_rectangles()[index])


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guard_subprocess_survives_optimization(tmp_path, optimized):
    program = r"""
import importlib.util,json,pathlib,sys
directory = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("al_guard_tests",directory / "test_qr05al.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
count = 0
def reject(fn,*args):
    global count
    try:
        fn(*args)
    except ValueError:
        count += 1
    else:
        raise RuntimeError("invalid input accepted")
for name,filename in (("primary","kernel.py"),("reference","reference.py")):
    module = t.load("al_guard_"+name,filename)
    for kind in t.MALFORMED:
        reject(module.build_family,t.malformed_problem(kind))
    for bounds in t.invalid_rectangles():
        reject(module.rectangle_moments,bounds)
    n = 1 << 1100
    reject(module.rectangle_moments,t.rect((n,n+1,n,n+1)))
    p = t.unit_problem()
    before,expected = t.wire(p),t.wire(t.independent_family(p))
    first,second = module.build_family(p),module.build_family(p)
    if t.wire(first) != expected or t.wire(second) != expected or t.wire(p) != before:
        raise RuntimeError("complete wire or input changed")
    first["levels"][0]["geometry"][0]["middles"][0]["tiles"][0]["moments"][0][0] = -1
    if t.wire(second) != expected or t.wire(p) != before:
        raise RuntimeError("output alias leaked")
if count != 44:
    raise RuntimeError("guard inventory changed")
print(json.dumps({"rejections":count,"engines":2}))
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
    assert json.loads(result.stdout) == {"rejections": 44, "engines": 2}


AK_TRIPLES = (
    "first",
    "middle",
    "last",
    "volume_product",
    "causal_integral",
    "pair_product",
    "product_error",
    "conditional",
    "product_conditional",
    "middle_covariance",
)
AK_BLOCKS = (
    "first",
    "middle",
    "last",
    "children",
    "coarse_integral",
    "child_integral_sum",
    "via_middle_integral",
)


@pytest.fixture(scope="session")
def fixed_inputs(runner):
    # Lazy fixture: collection and every generic test remain fixed-data-free.
    path = HERE.parent / "qr-05ak-shared-middle-2026-09-07/results.json"
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == 16462744
    assert (
        hashlib.sha256(raw).hexdigest()
        == "15fce56375af7e44bfc2f955559c55628c77338d11a1911161c4e3bb6f038db4"
    )
    previous = json.loads(raw)["suite"]["families"]
    assert [f["problem"]["family"] for f in previous] == list(FAMILIES)
    problems = [copy.deepcopy(f["problem"]) for f in previous]
    for problem in problems:
        assert [level["level"] for level in problem["levels"]] == ["l0", "l1", "l2"]
        assert [len(level["cells"]) for level in problem["levels"]] == [6, 7, 8]
        assert len(problem["probes"]) == 5
    supplied, consumed = runner.load_inputs()
    assert wire(supplied) == wire(problems) and wire(consumed) == wire(previous)
    return problems, previous


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
def test_fixed_all_five_complete_independent_family_wires(
    actual_families, expected_families, index
):
    expected = wire(expected_families[index])
    assert all(wire(actual) == expected for actual in actual_families[index])


def without_family(family):
    return {**family, "problem": {k: v for k, v in family["problem"].items() if k != "family"}}


def independent_controls(families):
    by = {f["problem"]["family"]: f for f in families}
    base = without_family(by["grid"])
    assert wire(without_family(by["boost"])) == wire(affine_family(base, F(2), F(1, 2)))
    assert wire(without_family(by["dilate"])) == wire(affine_family(base, F(2), F(2)))
    assert wire(without_family(by["warp_stale"])) == wire(without_family(by["warp"]))
    return {"boost": True, "dilation": True, "stale_geometric": True}


def level_projection(family):
    return [
        {
            "level": level["level"],
            "geometry": [
                {
                    **{key: q[key] for key in ("probe", "volume", "cells", "pairs")},
                    "triples": [{key: t[key] for key in AK_TRIPLES} for t in q["triples"]],
                }
                for q in level["geometry"]
            ],
        }
        for level in family["levels"]
    ]


def coarsening_projection(family):
    return [
        {
            **{key: link[key] for key in ("coarse", "fine", "parents")},
            "geometry": [
                {
                    "probe": q["probe"],
                    "blocks": [{key: b[key] for key in AK_BLOCKS} for b in q["blocks"]],
                }
                for q in link["geometry"]
            ],
        }
        for link in family["coarsenings"]
    ]


def independent_bridges(families, previous):
    assert len(families) == len(previous) == 5
    names = []
    for family, old in zip(families, previous, strict=True):
        assert wire(family["problem"]) == wire(old["problem"])
        assert wire(level_projection(family)) == wire(level_projection(old))
        assert wire(coarsening_projection(family)) == wire(coarsening_projection(old))
        names.append(family["problem"]["family"])
    return {
        "AK_family_names": names,
        "AK_projected_inputs_equal": True,
        "AK_complete_clipped_volumes_pairs_triples_equal": True,
        "AK_true_coarsening_equal": True,
        "other_AK_math_replayed": False,
        "other_prior_math_replayed": False,
    }


def independent_payload_sizes(families):
    rows = []
    for family in families:
        contract = [
            {
                "level": level["level"],
                "geometry": [
                    {"probe": q["probe"], "middles": q["middles"]} for q in level["geometry"]
                ],
            }
            for level in family["levels"]
        ]
        rows.append(
            {
                "family": family["problem"]["family"],
                "native_family_bytes": len(wire(family)),
                "moment_contract_bytes": len(wire(contract)),
            }
        )
    return rows


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
        "payload_sizes": independent_payload_sizes(expected_families),
        "totals": totals,
        "scope": dict.fromkeys(
            (
                "generic_production_API_hardened",
                "unknown_geometry_reconstructed",
                "minimal_encoding_proved",
                "universal_query_closure",
                "arbitrary_dynamics_closure",
                "continuum_limit_established",
                "marks_authenticated",
                "stochastic_transition_constructed",
                "quantum_channel_constructed",
                "gravity_derived",
                "empirical_data_used",
                "ret_integration_tested",
                "lean_verification_performed",
            ),
            False,
        ),
    }


@pytest.mark.fixed
def test_fixed_complete_suite_payloads_transformations_and_AK_bridges(
    runner, actual_families, expected_suite, fixed_inputs
):
    actual = runner.assemble_suite([pair[0] for pair in actual_families], fixed_inputs[1])
    assert wire(actual) == wire(expected_suite)
    runner.verify_suite(actual, expected_suite)


@pytest.mark.fixed
@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_route_orchestration_uses_declared_engines_only(
    runner, fixed_inputs, expected_suite, monkeypatch, route
):
    # Five real complete two-engine wires are tested separately. Cached exact
    # oracle values isolate route dispatch here, not additional mathematics.
    by = {f["problem"]["family"]: f for f in expected_suite["families"]}
    calls = []

    def loader(name):
        def build(problem):
            expected = by[problem["family"]]
            assert wire(problem) == wire(expected["problem"])
            calls.append((name, problem["family"]))
            return copy.deepcopy(expected)

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
def test_fixed_nonvacuous_payload_moment_contraction_and_coarsening_corruptions(
    runner, expected_families
):
    original = expected_families[0]
    q = ("levels", 0, "geometry", 0)
    m = (*q, "middles", 0)
    tile = (*m, "tiles", 0)
    t = (*q, "triples", 0)
    mb = ("coarsenings", 2, "geometry", 0, "moment_blocks", 0)
    b = ("coarsenings", 2, "geometry", 0, "blocks", 0)
    empty = next(
        ("levels", li, "geometry", qi, "triples", ti, "tile_pair_product")
        for li, level in enumerate(original["levels"])
        for qi, query in enumerate(level["geometry"])
        for ti, row in enumerate(query["triples"])
        if row["tile_pair_product"] is None
    )
    changes = [
        add_fraction(original, ("problem", "probes", 0, "bounds", 0)),
        add_fraction(original, (*q, "volume")),
        add_fraction(original, (*m, "bounds", 0)),
        add_fraction(original, (*m, "u_breaks", 0)),
        add_fraction(original, (*m, "moments", 8)),
        add_fraction(original, (*tile, "bounds", 0)),
        add_fraction(original, (*tile, "moments", 1)),
        add_fraction(original, (*tile, "moments", 4)),
        add_fraction(original, (*tile, "incoming", 0, "coefficients", 3)),
        add_fraction(original, (*tile, "outgoing", 0, "coefficients", 0)),
        replaced(original, (*tile, "incoming"), at_path(original, (*tile, "incoming"))[:-1]),
        replaced(original, (*m, "tiles"), at_path(original, (*m, "tiles"))[:-1]),
        replaced(
            original,
            ("counts", "tile_moment_entries"),
            original["counts"]["tile_moment_entries"] + 1,
        ),
        replaced(
            original,
            ("counts", "coefficient_entries"),
            original["counts"]["coefficient_entries"] + 1,
        ),
        add_fraction(original, (*t, "causal_integral")),
        add_fraction(original, (*t, "tile_pair_product")),
        add_fraction(original, (*t, "pair_product")),
        add_fraction(original, (*t, "tile_product_error")),
        add_fraction(original, (*t, "between_tile_error")),
        add_fraction(original, (*t, "centered_integral")),
        add_fraction(original, (*t, "within_tile_centered_integral")),
        replaced(original, empty, [0, 1]),
        add_fraction(original, (*t, "middle_covariance")),
        add_fraction(original, (*q, "summary", "tile_error")),
        add_fraction(original, (*mb, "child_moment_sum", 8)),
        add_fraction(original, (*mb, "coarse_moments", 6)),
        replaced(original, (*b, "children"), at_path(original, (*b, "children"))[:-1]),
        add_fraction(original, (*b, "via_middle_integral")),
        add_fraction(original, (*b, "child_integral_sum")),
        add_fraction(original, (*t, "tile_product_conditional")),
    ]
    assert len(changes) == 30
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_nonvacuous_payload_scope_and_complete_transform_controls(runner, expected_suite):
    original = expected_suite
    changes = [
        replaced(original, ("controls", "boost"), False),
        replaced(original, ("controls", "dilation"), False),
        replaced(original, ("controls", "stale_geometric"), False),
        replaced(original, ("prior_bridges", "other_AK_math_replayed"), True),
        replaced(original, ("scope", "minimal_encoding_proved"), True),
        replaced(original, ("scope", "universal_query_closure"), True),
        replaced(
            original,
            ("totals", "coefficient_entries"),
            original["totals"]["coefficient_entries"] + 1,
        ),
        replaced(
            original,
            ("payload_sizes", 0, "moment_contract_bytes"),
            original["payload_sizes"][0]["moment_contract_bytes"] + 1,
        ),
        replaced(
            original,
            ("payload_sizes", 0, "native_family_bytes"),
            original["payload_sizes"][0]["native_family_bytes"] + 1,
        ),
    ]
    assert len(changes) == 9
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.verify_suite(bad, original)
    # Two further changes preserve all scalar pair/triple answers but must fail
    # the runner's claimed complete input/raw-payload transformation checks.
    for path in (
        (3, "levels", 0, "geometry", 0, "middles", 0, "moments", 4),
        (2, "problem", "probes", 0, "bounds", 0),
    ):
        bad = add_fraction(original["families"], path)
        assert wire(bad) != wire(original["families"])
        with pytest.raises(ValueError):
            runner.controls(bad)
    assert wire(original) == before


@pytest.mark.fixed
def test_fixed_AK_projection_mutations_check_inputs_pairs_triples_and_true_coarsening(
    runner, expected_families, fixed_inputs
):
    original = fixed_inputs[1][0]
    q = ("levels", 0, "geometry", 0)
    pair = at_path(original, (*q, "pairs", 1))
    changes = [
        add_fraction(original, ("problem", "probes", 0, "bounds", 0)),
        add_fraction(original, (*q, "cells", 0, "clipped_volume")),
        add_fraction(original, (*q, "pairs", 0, "causal_integral")),
        replaced(
            original, (*q, "pairs", 1), {**pair, "first": pair["second"], "second": pair["first"]}
        ),
        add_fraction(original, (*q, "triples", 0, "causal_integral")),
        add_fraction(original, (*q, "triples", 0, "middle_covariance")),
        replaced(original, ("coarsenings", 2, "parents", 0, "children"), []),
        add_fraction(
            original, ("coarsenings", 2, "geometry", 0, "blocks", 0, "via_middle_integral")
        ),
    ]
    assert len(changes) == 8
    before = wire(original)
    for bad in changes:
        assert wire(bad) != before
        with pytest.raises(ValueError):
            runner.ak_bridges(expected_families, [bad, *fixed_inputs[1][1:]])
    assert wire(original) == before
