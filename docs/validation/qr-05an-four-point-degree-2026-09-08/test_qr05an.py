"""Bounded independent checks for the private four-point degree diagnostic.

Only tests marked fixed consume authenticated AM cases. Collection and generic
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
from itertools import combinations, pairwise, product
from math import comb
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
FAMILIES = ("grid", "warp")


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
        load("_qr05an_test_primary", "kernel.py"),
        load("_qr05an_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05an_test_runner", "study.py")


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


LINKS = ((0, 1), (1, 2), (0, 2))
BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))
PROP = tuple((i, j) for i in range(3) for j in range(3))
MOM = tuple((i, j) for i in range(4) for j in range(4))
UNIT = (F(0), F(1), F(0), F(1))


def nullable(value):
    return None if value is None else fw(value)


def poly_value(poly, x):
    return sum((c * x**i for i, c in enumerate(poly)), F())


def prefix_order(intervals):
    """Direct cumulative polynomial recursion, not atom assignment enumeration.

    P_k(t) integrates the previous ordered prefix P_(k-1) only across the
    kth region. A common endpoint partition makes each current polynomial
    exact. Continuity carries the prefix mass into the next interval.
    """
    if any(a >= b for a, b in intervals):
        return F()
    atoms = list(pairwise(sorted({x for interval in intervals for x in interval})))
    polynomials = [[F(1)] for _ in atoms]
    for a, b in intervals:
        cumulative, updated = F(), []
        for (left, right), prior in zip(atoms, polynomials, strict=True):
            if a <= left < right <= b:
                primitive = [F()] + [c / (i + 1) for i, c in enumerate(prior)]
                primitive[0] = cumulative - poly_value(primitive, left)
                cumulative = poly_value(primitive, right)
                updated.append(primitive)
            else:
                updated.append([cumulative])
        polynomials = updated
    return cumulative


def power_integral(a, b, p):
    return (b - a) * sum((a**i * b ** (p - i) for i in range(p + 1)), F()) / (p + 1)


def raw_moments(bounds):
    if not area(bounds):
        return [F()] * 16
    a, b, c, d = bounds
    return [power_integral(a, b, i) * power_integral(c, d, j) / 2 for i, j in MOM]


def interpolate(nodes, values):
    result = [F()] * len(nodes)
    for n, (x, value) in enumerate(zip(nodes, values, strict=True)):
        term = [F(1)]
        divisor = F(1)
        for m, y in enumerate(nodes):
            if m == n:
                continue
            out = [F()] * (len(term) + 1)
            for i, c in enumerate(term):
                out[i] -= y * c
                out[i + 1] += c
            term = out
            divisor *= x - y
        for i, c in enumerate(term):
            result[i] += value * c / divisor
    return result


def field_coefficients(first, second, tile, ordered, forced=False):
    if not area(first) or not area(second):
        return [F()] * (4 if forced else 9)
    lines = []
    for axis in (0, 2):
        a = first[axis : axis + 2]
        b0, b1 = second[axis : axis + 2]
        lo, hi = tile[axis : axis + 2]
        nodes = [lo, hi] if forced else [(3 * lo + hi) / 4, (lo + hi) / 2, (lo + 3 * hi) / 4]
        values = [ordered((a, (b0, min(b1, x)))) if x > b0 else F() for x in nodes]
        lines.append(interpolate(nodes, values))
    return [lines[0][i] * lines[1][j] / 4 for i, j in (BASIS if forced else PROP)]


def outgoing_coefficients(endpoint, tile):
    if not area(endpoint):
        return [F()] * 4
    lines = []
    for axis in (0, 2):
        a, b = endpoint[axis : axis + 2]
        lo, hi = tile[axis : axis + 2]
        nodes = [(2 * lo + hi) / 3, (lo + 2 * hi) / 3]
        lines.append(interpolate(nodes, [max(F(), b - max(a, x)) for x in nodes]))
    return [lines[0][i] * lines[1][j] / 2 for i, j in BASIS]


def integrate_coefficients(coeff, basis, moments):
    return sum((c * moments[4 * i + j] for c, (i, j) in zip(coeff, basis, strict=True)), F())


def integrate_product(left, lb, right, rb, moments):
    # Convolve into a coefficient dictionary before integrating. The direct
    # four-point answer below does not use this contraction.
    poly = {}
    for x, (i, j) in zip(left, lb, strict=True):
        for y, (k, l) in zip(right, rb, strict=True):
            poly[i + k, j + l] = poly.get((i + k, j + l), F()) + x * y
    return sum((c * moments[4 * i + j] for (i, j), c in poly.items()), F())


def vector_sum(rows, width):
    return [sum((row[i] for row in rows), F()) for i in range(width)]


def counts_from_family(levels, coarsenings, probe_count):
    gs = [g for level in levels for g in level["geometry"]]
    ms = [m for g in gs for m in g["middles"]]
    tiles = [t for m in ms for t in m["tiles"]]
    propagated = [p for t in tiles for p in t["propagated"]]
    outgoing = [p for t in tiles for p in t["outgoing"]]
    quads = [q for g in gs for q in g["quadruples"]]
    bgs = [g for link in coarsenings for g in link["geometry"]]
    mb = [b for g in bgs for b in g["moment_blocks"]]
    fb = [b for g in bgs for b in g["field_blocks"]]
    fp = [p for b in fb for p in b["pieces"]]
    blocks = [b for g in bgs for b in g["blocks"]]
    errors = [fraction(q["forced_error"]) for q in quads]
    mean = [fraction(q["mean_error"]) for q in quads if q["mean_error"] is not None]
    count = {
        "levels": len(levels),
        "probes": probe_count,
        "level_pairs": sum(len(g["pairs"]) for g in gs),
        "level_triples": sum(len(g["triples"]) for g in gs),
        "level_quadruples": len(quads),
        "middle_cells": len(ms),
        "positive_middle_cells": sum(m["bounds"] is not None for m in ms),
        "tiles": len(tiles),
        "breakpoint_entries": sum(len(m["u_breaks"]) + len(m["v_breaks"]) for m in ms),
        "middle_bound_entries": sum(len(m["bounds"] or []) for m in ms),
        "tile_bound_entries": sum(len(t["bounds"]) for t in tiles),
        "middle_moment_entries": sum(len(m["moments"]) for m in ms),
        "tile_moment_entries": sum(len(t["moments"]) for t in tiles),
        "propagated_vectors": len(propagated),
        "propagated_entries": sum(len(p["coefficients"]) for p in propagated),
        "forced_vectors": len(propagated),
        "forced_entries": sum(len(p["forced_coefficients"]) for p in propagated),
        "outgoing_vectors": len(outgoing),
        "outgoing_entries": sum(len(p["coefficients"]) for p in outgoing),
        "nonbilinear_propagated_vectors": sum(not p["bilinear_admissible"] for p in propagated),
        "quadruple_tile_visits": sum(
            len(g["cells"]) ** 3 * sum(len(m["tiles"]) for m in g["middles"]) for g in gs
        ),
        "positive_quadruples": sum(fraction(q["causal_integral"]) > 0 for q in quads),
        "undefined_quad_conditionals": sum(q["conditional"] is None for q in quads),
        "zero_third_quadruples": sum(q["mean_product"] is None for q in quads),
        "forced_positive_errors": sum(e > 0 for e in errors),
        "forced_zero_errors": sum(e == 0 for e in errors),
        "forced_negative_errors": sum(e < 0 for e in errors),
        "mean_positive_errors": sum(e > 0 for e in mean),
        "mean_zero_errors": sum(e == 0 for e in mean),
        "mean_negative_errors": sum(e < 0 for e in mean),
        "nonbilinear_quadruples": sum(not q["propagated_bilinear"] for q in quads),
        "nonbilinear_forced_equalities": sum(
            not q["propagated_bilinear"] and fraction(q["forced_error"]) == 0 for q in quads
        ),
        "coarsening_moment_blocks": len(mb),
        "coarsening_moment_entries": sum(
            len(b["coarse_moments"]) + len(b["child_moment_sum"]) for b in mb
        ),
        "field_blocks": len(fb),
        "field_pieces": len(fp),
        "field_child_terms": sum(
            len(next(p["children"] for p in link["parents"] if p["parent"] == b["first"]))
            * len(next(p["children"] for p in link["parents"] if p["parent"] == b["second"]))
            * len(b["pieces"])
            for link in coarsenings
            for g in link["geometry"]
            for b in g["field_blocks"]
        ),
        "field_coefficient_entries": sum(
            len(p["coarse_coefficients"]) + len(p["child_coefficient_sum"]) for p in fp
        ),
        "blocks": len(blocks),
        "child_terms": sum(len(b["children"]) for b in blocks),
        "via_middle_blocks": sum(b["via_middle_integral"] is not None for b in blocks),
    }
    return count


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
    cache = {}

    def ordered(intervals):
        key = tuple(tuple(x) for x in intervals)
        if key not in cache:
            cache[key] = prefix_order(key)
        return cache[key]

    def rectangle_order(bounds):
        if any(not area(b) for b in bounds):
            return F()
        return (
            ordered([b[:2] for b in bounds]) * ordered([b[2:] for b in bounds]) / 2 ** len(bounds)
        )

    levels, internals = [], []
    for li, rawlevel in enumerate(problem["levels"]):
        geometries, data = [], []
        for probe in problem["probes"]:
            query = tuple(map(fraction, probe["bounds"]))
            clips = {event: clipped(b, query) for event, b in boxes[li].items()}
            hs = {event: area(b) for event, b in clips.items()}
            assert sum(hs.values(), F()) == area(query)
            ids = list(clips)
            js = {(a, b): rectangle_order([clips[a], clips[b]]) for a, b in product(ids, repeat=2)}
            ts = {
                (a, b, c): rectangle_order([clips[a], clips[b], clips[c]])
                for a, b, c in product(ids, repeat=3)
            }
            us = {
                (a, b, c, d): rectangle_order([clips[a], clips[b], clips[c], clips[d]])
                for a, b, c, d in product(ids, repeat=4)
            }
            middles, fields, forced_fields, outfields, tilemaps, momentmaps = [], {}, {}, {}, {}, {}
            for c, bounds in clips.items():
                breaks = [
                    sorted(
                        {
                            bounds[axis],
                            bounds[axis + 1],
                            *(
                                v
                                for b in clips.values()
                                if area(b)
                                for v in b[axis : axis + 2]
                                if bounds[axis] < v < bounds[axis + 1]
                            ),
                        }
                    )
                    if hs[c]
                    else []
                    for axis in (0, 2)
                ]
                tiles = []
                for ti, ((u0, u1), (v0, v1)) in enumerate(
                    product(pairwise(breaks[0]), pairwise(breaks[1]))
                ):
                    tb = (u0, u1, v0, v1)
                    moments = raw_moments(tb)
                    propagated = []
                    for a, b in product(ids, repeat=2):
                        exact = field_coefficients(clips[a], clips[b], tb, ordered)
                        forced = field_coefficients(clips[a], clips[b], tb, ordered, True)
                        admissible = all(
                            x == 0
                            for x, (i, j) in zip(exact, PROP, strict=True)
                            if i == 2 or j == 2
                        )
                        fields[c, ti, a, b] = exact
                        forced_fields[c, ti, a, b] = forced
                        propagated.append(
                            {
                                "first": a,
                                "second": b,
                                "coefficients": list(map(fw, exact)),
                                "forced_coefficients": list(map(fw, forced)),
                                "bilinear_admissible": admissible,
                            }
                        )
                    outgoing = []
                    for d in ids:
                        coeff = outgoing_coefficients(clips[d], tb)
                        outfields[c, ti, d] = coeff
                        outgoing.append({"event": d, "coefficients": list(map(fw, coeff))})
                    tiles.append(
                        {
                            "bounds": rect(tb),
                            "moments": list(map(fw, moments)),
                            "propagated": propagated,
                            "outgoing": outgoing,
                        }
                    )
                    tilemaps[c, ti] = tb
                    momentmaps[c, ti] = moments
                whole = raw_moments(bounds)
                assert vector_sum([momentmaps[c, ti] for ti in range(len(tiles))], 16) == whole
                middles.append(
                    {
                        "event": c,
                        "bounds": rect(bounds) if hs[c] else None,
                        "u_breaks": list(map(fw, breaks[0])),
                        "v_breaks": list(map(fw, breaks[1])),
                        "moments": list(map(fw, whole)),
                        "tiles": tiles,
                    }
                )
            middlemap = {m["event"]: m for m in middles}
            triples, bilinear, forced_ts = [], {}, {}
            for a, b, c in product(ids, repeat=3):
                indices = range(len(middlemap[c]["tiles"]))
                exact = sum(
                    (
                        integrate_coefficients(fields[c, ti, a, b], PROP, momentmaps[c, ti])
                        for ti in indices
                    ),
                    F(),
                )
                forced = sum(
                    (
                        integrate_coefficients(forced_fields[c, ti, a, b], BASIS, momentmaps[c, ti])
                        for ti in indices
                    ),
                    F(),
                )
                assert exact == ts[a, b, c] and forced >= exact
                admissible = all(
                    all(
                        x == 0
                        for x, (i, j) in zip(fields[c, ti, a, b], PROP, strict=True)
                        if i == 2 or j == 2
                    )
                    for ti in indices
                )
                bilinear[a, b, c] = admissible
                forced_ts[a, b, c] = forced
                vp = hs[a] * hs[b] * hs[c]
                triples.append(
                    {
                        "first": a,
                        "second": b,
                        "third": c,
                        "volume_product": fw(vp),
                        "causal_integral": fw(exact),
                        "forced_integral": fw(forced),
                        "forced_error": fw(forced - exact),
                        "conditional": nullable(ratio(exact, vp)),
                        "forced_conditional": nullable(ratio(forced, vp)),
                        "propagated_bilinear": admissible,
                    }
                )
            quadruples = []
            for a, b, c, d in product(ids, repeat=4):
                exact = us[a, b, c, d]
                forced = F()
                centered = F() if hs[c] else None
                checked_t = checked_j = checked_u = F()
                for ti in range(len(middlemap[c]["tiles"])):
                    ff = fields[c, ti, a, b]
                    rr = outfields[c, ti, d]
                    mm = momentmaps[c, ti]
                    checked_t += integrate_coefficients(ff, PROP, mm)
                    checked_j += integrate_coefficients(rr, BASIS, mm)
                    checked_u += integrate_product(ff, PROP, rr, BASIS, mm)
                    forced += integrate_product(forced_fields[c, ti, a, b], BASIS, rr, BASIS, mm)
                    cf, cr = ff.copy(), rr.copy()
                    cf[0] -= ts[a, b, c] / hs[c]
                    cr[0] -= js[c, d] / hs[c]
                    centered += integrate_product(cf, PROP, cr, BASIS, mm)
                assert (checked_t, checked_j, checked_u) == (ts[a, b, c], js[c, d], exact)
                mean = ratio(ts[a, b, c] * js[c, d], hs[c])
                assert centered == (exact - mean if mean is not None else None)
                assert forced >= exact
                vp = hs[a] * hs[b] * hs[c] * hs[d]
                quadruples.append(
                    {
                        "first": a,
                        "second": b,
                        "third": c,
                        "last": d,
                        "volume_product": fw(vp),
                        "causal_integral": fw(exact),
                        "forced_integral": fw(forced),
                        "forced_error": fw(forced - exact),
                        "mean_product": nullable(mean),
                        "mean_error": nullable(mean - exact if mean is not None else None),
                        "conditional": nullable(ratio(exact, vp)),
                        "forced_conditional": nullable(ratio(forced, vp)),
                        "mean_conditional": nullable(mean / vp) if vp else None,
                        "third_covariance": nullable(centered / hs[c]) if hs[c] else None,
                        "centered_integral": nullable(centered),
                        "propagated_bilinear": bilinear[a, b, c],
                    }
                )
            sumj, sumt, sumu = sum(js.values(), F()), sum(ts.values(), F()), sum(us.values(), F())
            assert (
                sumj == area(query) ** 2 / 4
                and sumt == area(query) ** 3 / 36
                and sumu == area(query) ** 4 / 576
            )
            forcedsum = sum((fraction(q["forced_integral"]) for q in quadruples), F())
            meansum = sum(
                (fraction(q["mean_product"]) for q in quadruples if q["mean_product"] is not None),
                F(),
            )
            geometries.append(
                {
                    "probe": probe["name"],
                    "volume": fw(area(query)),
                    "cells": [{"event": a, "clipped_volume": fw(h)} for a, h in hs.items()],
                    "middles": middles,
                    "pairs": [
                        {
                            "first": a,
                            "second": b,
                            "volume_product": fw(hs[a] * hs[b]),
                            "causal_integral": fw(j),
                            "conditional": nullable(ratio(j, hs[a] * hs[b])),
                        }
                        for (a, b), j in js.items()
                    ],
                    "triples": triples,
                    "quadruples": quadruples,
                    "summary": {
                        "pair_integral": fw(sumj),
                        "pair_continuum_integral": fw(area(query) ** 2 / 4),
                        "triple_integral": fw(sumt),
                        "triple_continuum_integral": fw(area(query) ** 3 / 36),
                        "quadruple_integral": fw(sumu),
                        "quadruple_continuum_integral": fw(area(query) ** 4 / 576),
                        "forced_integral": fw(forcedsum),
                        "forced_error": fw(forcedsum - sumu),
                        "mean_product": fw(meansum),
                        "mean_error": fw(meansum - sumu),
                    },
                }
            )
            data.append({"us": us, "middles": middlemap, "fields": fields, "tiles": tilemaps})
        levels.append({"level": rawlevel["level"], "geometry": geometries})
        internals.append(data)
    coarsenings = []
    for coarse, fine in LINKS:
        children = {
            p: [c for c in boxes[fine] if maps[coarse, fine][c] == p] for p in boxes[coarse]
        }
        geometries = []
        for qi, probe in enumerate(problem["probes"]):
            old, new = internals[coarse][qi], internals[fine][qi]
            momentblocks = []
            for p, cc in children.items():
                oldm = old["middles"][p]["moments"]
                summ = vector_sum(
                    [[fraction(x) for x in new["middles"][c]["moments"]] for c in cc], 16
                )
                assert summ == list(map(fraction, oldm))
                momentblocks.append(
                    {
                        "parent": p,
                        "children": cc,
                        "coarse_moments": copy.deepcopy(oldm),
                        "child_moment_sum": list(map(fw, summ)),
                    }
                )
            fieldblocks = []
            for a, b, c in product(children, repeat=3):
                pieces = []
                for child in children[c]:
                    for ti, t in enumerate(new["middles"][child]["tiles"]):
                        tb = tuple(map(fraction, t["bounds"]))
                        candidates = [
                            i
                            for i in range(len(old["middles"][c]["tiles"]))
                            if contained(tb, old["tiles"][c, i])
                        ]
                        assert len(candidates) == 1
                        ci = candidates[0]
                        coeff = old["fields"][c, ci, a, b]
                        summed = vector_sum(
                            [
                                new["fields"][child, ti, x, y]
                                for x in children[a]
                                for y in children[b]
                            ],
                            9,
                        )
                        assert coeff == summed
                        pieces.append(
                            {
                                "child": child,
                                "fine_tile": ti,
                                "coarse_tile": ci,
                                "coarse_coefficients": list(map(fw, coeff)),
                                "child_coefficient_sum": list(map(fw, summed)),
                            }
                        )
                fieldblocks.append({"first": a, "second": b, "third": c, "pieces": pieces})
            blocks = []
            for a, b, c, d in product(children, repeat=4):
                tuples = list(product(children[a], children[b], children[c], children[d]))
                summed = sum((new["us"][t] for t in tuples), F())
                assert summed == old["us"][a, b, c, d]
                via = None
                if (coarse, fine) == (0, 2):
                    midchildren = {p: [x for x in boxes[1] if maps[0, 1][x] == p] for p in children}
                    descendants = {x: [y for y in boxes[2] if maps[1, 2][y] == x] for x in boxes[1]}
                    via = sum(
                        (
                            sum(
                                (
                                    new["us"][row]
                                    for row in product(*(descendants[x] for x in midtuple))
                                ),
                                F(),
                            )
                            for midtuple in product(*(midchildren[x] for x in (a, b, c, d)))
                        ),
                        F(),
                    )
                    assert via == summed
                blocks.append(
                    {
                        "first": a,
                        "second": b,
                        "third": c,
                        "last": d,
                        "children": [list(x) for x in tuples],
                        "coarse_integral": fw(old["us"][a, b, c, d]),
                        "child_integral_sum": fw(summed),
                        "via_middle_integral": nullable(via),
                    }
                )
            geometries.append(
                {
                    "probe": probe["name"],
                    "moment_blocks": momentblocks,
                    "field_blocks": fieldblocks,
                    "blocks": blocks,
                }
            )
        coarsenings.append(
            {
                "coarse": problem["levels"][coarse]["level"],
                "fine": problem["levels"][fine]["level"],
                "parents": [{"parent": p, "children": cc} for p, cc in children.items()],
                "geometry": geometries,
            }
        )
    return {
        "problem": copy.deepcopy(problem),
        "levels": levels,
        "coarsenings": coarsenings,
        "counts": counts_from_family(levels, coarsenings, len(problem["probes"])),
    }


def single_problem():
    return make_problem([(name, [(7, UNIT)]) for name in ("a", "b", "c")], [("unit", UNIT)])


def transformed_problem(problem, alpha, beta, du=F(), dv=F()):
    out = copy.deepcopy(problem)

    def change(bounds):
        a, b, c, d = map(fraction, bounds)
        return rect((alpha * a + du, alpha * b + du, beta * c + dv, beta * d + dv))

    for q in out["probes"]:
        q["bounds"] = change(q["bounds"])
    for level in out["levels"]:
        for cell in level["cells"]:
            cell["bounds"] = change(cell["bounds"])
    return out


def affine_expected(family, alpha, beta, du=F(), dv=F()):
    k = alpha * beta

    def bounds(raw):
        if raw is None:
            return None
        a, b, c, d = map(fraction, raw)
        return rect((alpha * a + du, alpha * b + du, beta * c + dv, beta * d + dv))

    def moments(raw):
        old = list(map(fraction, raw))
        return [
            fw(
                k
                * sum(
                    (
                        F(comb(i, p) * comb(j, q))
                        * alpha**p
                        * beta**q
                        * du ** (i - p)
                        * dv ** (j - q)
                        * old[4 * p + q]
                        for p in range(i + 1)
                        for q in range(j + 1)
                    ),
                    F(),
                )
            )
            for i, j in MOM
        ]

    def coefficients(raw, basis, degree):
        old = list(map(fraction, raw))
        answer = []
        for p, q in basis:
            answer.append(
                fw(
                    sum(
                        (
                            c
                            * k**degree
                            * F(comb(i, p) * comb(j, q))
                            * (-du) ** (i - p)
                            * (-dv) ** (j - q)
                            / (alpha**i * beta**j)
                            for c, (i, j) in zip(old, basis, strict=True)
                            if i >= p and j >= q
                        ),
                        F(),
                    )
                )
            )
        return answer

    def walk(value, scope=None):
        if type(value) is list:
            return [walk(v, scope) for v in value]
        if type(value) is not dict:
            return copy.deepcopy(value)
        answer = {}
        for key, child in value.items():
            if key == "bounds":
                result = bounds(child)
            elif key in ("u_breaks", "v_breaks"):
                scale, shift = (alpha, du) if key == "u_breaks" else (beta, dv)
                result = [fw(scale * fraction(x) + shift) for x in child]
            elif key in ("moments", "coarse_moments", "child_moment_sum"):
                result = moments(child)
            elif key in ("coarse_coefficients", "child_coefficient_sum"):
                result = coefficients(child, PROP, 2)
            elif key == "forced_coefficients":
                result = coefficients(child, BASIS, 2)
            elif key == "coefficients":
                result = (
                    coefficients(child, PROP, 2)
                    if "first" in value
                    else coefficients(child, BASIS, 1)
                )
            else:
                degree = None
                if key in ("volume", "clipped_volume"):
                    degree = 1
                elif key == "volume_product":
                    degree = {"pairs": 2, "triples": 3, "quadruples": 4}[scope]
                elif key in ("causal_integral", "forced_integral", "forced_error"):
                    degree = {"pairs": 2, "triples": 3, "quadruples": 4, "summary": 4}[scope]
                elif key in (
                    "mean_product",
                    "mean_error",
                    "centered_integral",
                    "coarse_integral",
                    "child_integral_sum",
                    "via_middle_integral",
                ):
                    degree = 4
                elif key == "third_covariance":
                    degree = 3
                elif key in ("pair_integral", "pair_continuum_integral"):
                    degree = 2
                elif key in ("triple_integral", "triple_continuum_integral"):
                    degree = 3
                elif key in ("quadruple_integral", "quadruple_continuum_integral"):
                    degree = 4
                result = (
                    nullable(fraction(child) * k**degree)
                    if degree is not None and child is not None
                    else (
                        None
                        if degree is not None
                        else walk(
                            child,
                            key if key in ("pairs", "triples", "quadruples", "summary") else scope,
                        )
                    )
                )
            answer[key] = result
        return answer

    return walk(family)


@pytest.mark.parametrize(
    "factory",
    [single_problem, unit_problem, problem_of],
    ids=["unit", "repeated_cross_children", "unequal_partial"],
)
def test_generic_complete_prefix_polynomial_oracle(engines, factory):
    problem = factory()
    expected = independent_family(problem)
    before = wire(problem)
    for module in engines:
        assert wire(module.build_family(problem)) == wire(expected)
        assert wire(problem) == before


def test_unit_quadratic_field_requires_sixteen_moments_and_two_distinct_controls(engines):
    for module in engines:
        family = module.build_family(single_problem())
        geometry = family["levels"][0]["geometry"][0]
        tile = geometry["middles"][0]["tiles"][0]
        prop = tile["propagated"][0]
        assert prop["coefficients"] == [[0, 1]] * 8 + [[1, 16]]
        assert prop["forced_coefficients"] == [[0, 1]] * 3 + [[1, 16]]
        assert prop["bilinear_admissible"] is False
        assert len(tile["moments"]) == 16 and tile["moments"][15] == [1, 32]
        row = geometry["quadruples"][0]
        expected = {
            "causal_integral": F(1, 9216),
            "forced_integral": F(1, 2304),
            "forced_error": F(1, 3072),
            "mean_product": F(1, 2304),
            "mean_error": F(1, 3072),
            "third_covariance": -F(1, 1536),
            "centered_integral": -F(1, 3072),
        }
        assert {key: fraction(row[key]) for key in expected} == expected
        triple = geometry["triples"][0]
        assert triple["causal_integral"] == [1, 288] and triple["forced_integral"] == [1, 128]
        # The highest mixed moment contributes +M33/32. Dropping just that
        # required entry cannot preserve the exact tensor contraction.
        assert fraction(row["causal_integral"]) - fraction(tile["moments"][15]) / 32 == -F(1, 1152)


def test_full_cross_child_quadruples_and_direct_adjacent_sums(engines):
    problem = unit_problem()
    for module in engines:
        family = module.build_family(problem)
        geom = family["levels"][1]["geometry"][0]
        values = {
            tuple(row[k] for k in ("first", "second", "third", "last")): fraction(
                row["causal_integral"]
            )
            for row in geom["quadruples"]
        }
        left, right = 9, -2
        positive = {
            (left, left, left, left): F(1, 147456),
            (left, left, left, right): F(1, 36864),
            (left, left, right, right): F(1, 24576),
            (left, right, right, right): F(1, 36864),
            (right, right, right, right): F(1, 147456),
        }
        assert {key: v for key, v in values.items() if v} == positive
        assert sum(values.values(), F()) == F(1, 9216)
        assert values[(left,) * 4] + values[(right,) * 4] == F(1, 73728)
        block = family["coarsenings"][0]["geometry"][0]["blocks"][0]
        assert len(block["children"]) == 16 and block["child_integral_sum"] == [1, 9216]
        direct = family["coarsenings"][2]["geometry"][0]["blocks"][0]
        assert len(direct["children"]) == 256
        assert (
            direct["via_middle_integral"]
            == direct["child_integral_sum"]
            == direct["coarse_integral"]
        )
        assert all(
            b["via_middle_integral"] is None
            for link in family["coarsenings"][:2]
            for g in link["geometry"]
            for b in g["blocks"]
        )


def test_field_admission_is_separate_from_outgoing_support_and_endpoint_clipping(engines):
    for module in engines:
        family = module.build_family(unit_problem())
        g = family["levels"][2]["geometry"][0]
        rows = {
            tuple(q[k] for k in ("first", "second", "third", "last")): q for q in g["quadruples"]
        }
        # Both integrated regions lie outside C. Clipping A or B to C would
        # erase this positive constant propagated field.
        positive = rows[9, 9, 8, 8]
        assert positive["propagated_bilinear"] is True and fraction(positive["causal_integral"]) > 0
        assert positive["forced_error"] == [0, 1]
        hidden = rows[8, 8, 8, 3]
        assert hidden["propagated_bilinear"] is False
        assert hidden["causal_integral"] == hidden["forced_integral"] == [0, 1]
        assert any(q["mean_product"] != q["forced_integral"] for q in rows.values())
        partial = family["levels"][2]["geometry"][1]
        positive_ids = {c["event"] for c in partial["cells"] if fraction(c["clipped_volume"]) > 0}
        saw_empty = saw_endpoint = False
        for row in partial["quadruples"]:
            if row["third"] not in positive_ids:
                saw_empty = True
                assert (
                    row["causal_integral"]
                    == row["forced_integral"]
                    == row["forced_error"]
                    == [0, 1]
                )
                assert all(
                    row[k] is None
                    for k in (
                        "mean_product",
                        "mean_error",
                        "third_covariance",
                        "centered_integral",
                        "conditional",
                    )
                )
            elif any(row[k] not in positive_ids for k in ("first", "second", "last")):
                saw_endpoint = True
                assert row["mean_product"] == row["causal_integral"] == [0, 1]
                assert row["third_covariance"] == row["centered_integral"] == [0, 1]
        assert saw_empty and saw_endpoint


def test_shared_grid_inactive_cuts_signed_coefficients_and_field_additivity(engines):
    problem = transformed_problem(problem_of(), F(2), F(3), F(-3), F(5))
    expected = independent_family(problem)
    assert any(
        len(m["tiles"]) > 1 for l in expected["levels"] for g in l["geometry"] for m in g["middles"]
    )
    assert any(
        fraction(x) < 0
        for l in expected["levels"]
        for g in l["geometry"]
        for m in g["middles"]
        for t in m["tiles"]
        for p in t["propagated"]
        for x in p["coefficients"]
    )
    for module in engines:
        actual = module.build_family(problem)
        assert wire(actual) == wire(expected)
        for link in actual["coarsenings"]:
            for g in link["geometry"]:
                for block in g["moment_blocks"]:
                    assert len(block["coarse_moments"]) == 16
                    assert block["coarse_moments"] == block["child_moment_sum"]
                for block in g["field_blocks"]:
                    for piece in block["pieces"]:
                        assert len(piece["coarse_coefficients"]) == 9
                        assert piece["coarse_coefficients"] == piece["child_coefficient_sum"]


@pytest.mark.parametrize(
    "transform",
    [(F(2), F(1, 2), F(), F()), (F(2), F(3), F(-3), F(5))],
    ids=["boost", "signed_affine"],
)
def test_complete_affine_family_transport(engines, runner, transform):
    problem = problem_of()
    expected = independent_family(problem)
    moved = affine_expected(expected, *transform)
    assert wire(moved) == wire(independent_family(transformed_problem(problem, *transform)))
    assert wire(runner.affine_family(expected, *transform)) == wire(moved)
    for module in engines:
        assert wire(module.build_family(transformed_problem(problem, *transform))) == wire(moved)


def test_sixteen_signed_nonsquare_moments_and_retained_degree_overflow(engines):
    rectangles = [
        (F(a, 3), F(a + 1, 3), F(c, 2), F(c + 2, 2)) for a in range(-2, 3) for c in range(-1, 2)
    ]
    for module in engines:
        for bounds in rectangles:
            actual = module.rectangle_moments(rect(bounds))
            assert actual == list(map(fw, raw_moments(bounds)))
        # A large translation is valid when every retained moment still fits.
        bounds = (F(1 << 900), F((1 << 900) + 1), F(), F(1))
        assert module.rectangle_moments(rect(bounds)) == list(map(fw, raw_moments(bounds)))
        huge = rect((F(1 << 1400), F((1 << 1400) + 1), F(), F(1)))
        with pytest.raises(ValueError):
            module.rectangle_moments(huge)
        with pytest.raises(ValueError):
            module.build_family(transformed_problem(single_problem(), F(1), F(1), F(1 << 1400)))


def test_detached_outputs_shared_native_inputs_and_no_hidden_reads(engines, monkeypatch):
    problem = single_problem()
    problem["levels"][1]["cells"][0]["bounds"] = problem["levels"][0]["cells"][0]["bounds"]
    before = wire(problem)
    expected = wire(independent_family(problem))

    def forbidden(*args, **kwargs):
        raise RuntimeError("hidden file read")

    for module in engines:
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            actual = module.build_family(problem)
        assert wire(actual) == expected and wire(problem) == before
        actual["problem"]["levels"][0]["cells"][0]["bounds"][0][0] = 77
        actual["levels"][0]["geometry"][0]["middles"][0]["moments"][0][0] = 77
        assert wire(problem) == before and wire(module.build_family(problem)) == expected


MALFORMED = (
    "extra",
    "missing",
    "bool_id",
    "float",
    "tuple",
    "subclass",
    "unreduced",
    "zero_denominator",
    "degenerate",
    "duplicate_id",
    "unsorted",
    "overlap",
    "hole",
    "bad_parent",
    "duplicate_level",
    "duplicate_probe",
    "too_many_levels",
    "oversized",
)


def malformed(kind):
    p = unit_problem()
    path = ("levels", 1, "cells", 0)
    if kind == "extra":
        return {**p, "extra": 0}
    if kind == "missing":
        return {k: v for k, v in p.items() if k != "family"}
    if kind == "bool_id":
        return replaced(p, path + ("event",), False)
    if kind == "float":
        return replaced(p, path + ("bounds", 0, 0), 0.5)
    if kind == "tuple":
        return replaced(p, ("levels",), tuple(p["levels"]))
    if kind == "subclass":

        class NativeList(list):
            pass

        return replaced(p, path + ("bounds",), NativeList(p["levels"][1]["cells"][0]["bounds"]))
    if kind == "unreduced":
        return replaced(p, path + ("bounds", 0), [2, 4])
    if kind == "zero_denominator":
        return replaced(p, path + ("bounds", 0, 1), 0)
    if kind == "degenerate":
        return replaced(p, path + ("bounds", 1), [1, 2])
    if kind == "duplicate_id":
        return replaced(p, ("levels", 1, "cells", 1, "event"), -2)
    if kind == "unsorted":
        return replaced(p, ("levels", 1, "cells"), p["levels"][1]["cells"][::-1])
    if kind == "overlap":
        return replaced(p, ("levels", 1, "cells", 1, "bounds", 1), [3, 4])
    if kind == "hole":
        return replaced(p, ("levels", 1, "cells", 1, "bounds", 1), [1, 4])
    if kind == "bad_parent":
        return replaced(p, ("levels", 2, "cells", 0, "bounds", 1), [3, 4])
    if kind == "duplicate_level":
        return replaced(p, ("levels", 2, "level"), p["levels"][0]["level"])
    if kind == "duplicate_probe":
        return replaced(p, ("probes", 1, "name"), p["probes"][0]["name"])
    if kind == "too_many_levels":
        return replaced(p, ("levels",), p["levels"] + [copy.deepcopy(p["levels"][0])])
    if kind == "oversized":
        return replaced(p, path + ("bounds", 0, 0), 1 << 4096)
    raise AssertionError(kind)


@pytest.mark.parametrize("kind", MALFORMED)
def test_bounded_native_geometry_and_lineage_rejections(engines, kind):
    for module in engines:
        with pytest.raises(ValueError):
            module.build_family(malformed(kind))


def invalid_rectangles():
    bounds = rect(UNIT)
    return [
        None,
        tuple(bounds),
        replaced(bounds, (0, 0), False),
        replaced(bounds, (0, 1), 0),
        replaced(bounds, (1,), [2, 2]),
        replaced(bounds, (0, 0), 0.0),
        rect((0, 0, 0, 1)),
        rect((1, 0, 0, 1)),
        bounds[:-1],
    ]


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_normal_and_optimized_exceptions_and_ownership(tmp_path, optimized):
    program = r"""
import importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location("an_test_guard",sys.argv[1])
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
engines=[t.load("an_guard_primary","kernel.py"),t.load("an_guard_reference","reference.py")]
rejections=0
def reject(fn,arg):
    global rejections
    try: fn(arg)
    except ValueError: rejections+=1
    else: raise RuntimeError("invalid admission accepted")
for module in engines:
    for kind in t.MALFORMED: reject(module.build_family,t.malformed(kind))
    for bounds in t.invalid_rectangles(): reject(module.rectangle_moments,bounds)
    p=t.single_problem(); before=t.wire(p)
    actual=module.build_family(p)
    if actual["levels"][0]["geometry"][0]["quadruples"][0]["causal_integral"] != [1,9216]:
        raise RuntimeError("unit integral")
    actual["problem"]["family"]="mutated"
    if t.wire(p)!=before or module.build_family(p)["problem"]["family"]!="synthetic":
        raise RuntimeError("ownership")
if rejections!=54: raise RuntimeError(("rejections",rejections))
print(json.dumps({"rejections":rejections}))
"""
    cmd = [sys.executable, "-I"]
    if optimized:
        cmd.append("-O")
    cmd += [
        "-X",
        f"pycache_prefix={tmp_path / 'cache'}",
        "-c",
        program,
        str(HERE / "test_qr05an.py"),
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, check=True, env={**os.environ, "PYTEST_ADDOPTS": ""}
    )
    assert json.loads(result.stdout) == {"rejections": 54}


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


def independent_projection(previous):
    assert [x["problem"]["family"] for x in previous] == [
        "grid",
        "warp",
        "warp_stale",
        "boost",
        "dilate",
    ]
    problems = []
    for old in previous[:2]:
        contexts = old["problem"]["contexts"]
        chosen = [c for c in contexts if c["probe"] == "whole"]
        assert [c["level"] for c in chosen] == ["l0", "l1", "l2"]
        assert [len(c["middles"]) for c in chosen] == [6, 7, 8]
        assert all(c["probe_bounds"] == chosen[0]["probe_bounds"] for c in chosen)
        levels = []
        for c in chosen:
            assert all(m["bounds"] is not None for m in c["middles"])
            levels.append(
                {
                    "level": c["level"],
                    "cells": [
                        {"event": m["event"], "bounds": copy.deepcopy(m["bounds"])}
                        for m in c["middles"]
                    ],
                }
            )
        problems.append(
            {
                "family": old["problem"]["family"],
                "probes": [{"name": "whole", "bounds": copy.deepcopy(chosen[0]["probe_bounds"])}],
                "levels": levels,
            }
        )
    return problems


def independent_payload(families):
    rows = []
    for family in families:
        contract = [
            {
                "level": level["level"],
                "geometry": [
                    {"probe": g["probe"], "middles": g["middles"]} for g in level["geometry"]
                ],
            }
            for level in family["levels"]
        ]
        rows.append(
            {
                "family": family["problem"]["family"],
                "moment_contract_bytes": len(wire(contract)),
                "coarsening_witness_bytes": len(wire(family["coarsenings"])),
                "native_family_bytes": len(wire(family)),
            }
        )
    return rows


SCOPE = (
    "generic_production_API_hardened",
    "AM_moment_reuse_tested",
    "minimal_encoding_proved",
    "universal_fixed_degree_closure",
    "unknown_geometry_reconstructed",
    "arbitrary_dynamics_closure",
    "continuum_limit_established",
    "marks_authenticated",
    "stochastic_transition_constructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "empirical_data_used",
    "ret_integration_tested",
    "lean_verification_performed",
    "fixed_affine_families_run",
)


def independent_suite(families, previous):
    assert [f["problem"] for f in families] == independent_projection(previous)
    for f in families:
        for level in f["levels"]:
            for g in level["geometry"]:
                v = fraction(g["volume"])
                for key, power, denominator in (
                    ("pair", 2, 4),
                    ("triple", 3, 36),
                    ("quadruple", 4, 576),
                ):
                    actual = (
                        sum((fraction(row["causal_integral"]) for row in g[key + "s"]), F())
                        if key != "pair"
                        else sum((fraction(row["causal_integral"]) for row in g["pairs"]), F())
                    )
                    assert actual == v**power / denominator
                    assert (
                        g["summary"][key + "_integral"]
                        == g["summary"][key + "_continuum_integral"]
                        == fw(actual)
                    )
        assert f["counts"] == counts_from_family(
            f["levels"], f["coarsenings"], len(f["problem"]["probes"])
        )
    return {
        "families": families,
        "controls": {"pair_partition": True, "triple_partition": True, "quadruple_partition": True},
        "prior_bridges": {
            "AM_selected_families": list(FAMILIES),
            "AM_selected_whole_bounds_ids_equal": True,
            "AM_selected_probe_bounds_equal": True,
            "AM_moments_consumed": False,
            "AM_query_answers_replayed": False,
            "older_math_replayed": False,
        },
        "payload_sizes": independent_payload(families),
        "totals": {
            "families": len(families),
            **{key: sum(f["counts"][key] for f in families) for key in families[0]["counts"]},
        },
        "scope": dict.fromkeys(SCOPE, False),
    }


@pytest.fixture(scope="session")
def fixed_data(runner):
    # This fixture is reached only from explicitly marked fixed tests. Neither
    # import nor generic collection projects AM geometry or performs AN math.
    problems, previous = runner.load_inputs()
    assert wire(problems) == wire(independent_projection(previous))
    expected = [independent_family(problem) for problem in problems]
    return problems, previous, expected


@pytest.fixture(scope="session")
def fixed_outputs(fixed_data, engines):
    problems, _previous, expected = fixed_data
    actual = []
    for problem, wanted in zip(problems, expected, strict=True):
        before = wire(problem)
        routes = []
        for module in engines:
            supplied = copy.deepcopy(problem)
            result = module.build_family(supplied)
            assert wire(supplied) == before and wire(problem) == before
            assert wire(result) == wire(wanted)
            routes.append(result)
        actual.append(routes[0])
    return actual


@pytest.fixture(scope="session")
def fixed_suite(fixed_data, fixed_outputs, runner):
    _, previous, _ = fixed_data
    suite = runner.assemble_suite(fixed_outputs, previous)
    assert wire(suite) == wire(independent_suite(fixed_outputs, previous))
    return suite


@pytest.mark.fixed
@pytest.mark.parametrize("index", range(2), ids=FAMILIES)
def test_fixed_complete_two_engine_and_prefix_oracle_families(fixed_data, fixed_outputs, index):
    assert wire(fixed_outputs[index]) == wire(fixed_data[2][index])


@pytest.mark.fixed
def test_fixed_full_suite_literal_payload_partition_and_selected_AM_boundary(
    fixed_data, fixed_suite, runner
):
    problems, previous, expected = fixed_data
    wanted = independent_suite(expected, previous)
    assert wire(fixed_suite) == wire(wanted)
    assert runner.payload_sizes(expected) == independent_payload(expected)
    assert runner.project_inputs(previous)[0] == problems
    assert [len(p["levels"][i]["cells"]) for p in problems for i in range(3)] == [6, 7, 8] * 2
    assert (
        wanted["totals"]["level_pairs"],
        wanted["totals"]["level_triples"],
        wanted["totals"]["level_quadruples"],
    ) == (298, 2142, 15586)
    # AM's higher moments, old queries and derived answers are explicitly NOT
    # in AN's access path. They must not silently enter its selected projection.
    changed = copy.deepcopy(previous)
    c = next(c for c in changed[0]["problem"]["contexts"] if c["probe"] == "whole")
    c["middles"][0]["moments"][8] = [777, 1]
    c["middles"][0]["queries"][0]["name"] = "not_consumed"
    changed[0]["contexts"] = []
    assert wire(independent_projection(changed)) == wire(problems)
    assert wire(runner.project_inputs(changed)[0]) == wire(problems)


@pytest.mark.fixed
@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_cached_orchestration_routes(
    fixed_data, fixed_outputs, fixed_suite, runner, monkeypatch, route
):
    problems, previous, _ = fixed_data
    calls = []
    by_name = {p["family"]: f for p, f in zip(problems, fixed_outputs, strict=True)}

    def loader(name):
        def build(problem):
            calls.append((name, problem["family"]))
            return copy.deepcopy(by_name[problem["family"]])

        return SimpleNamespace(build_family=build)

    with monkeypatch.context() as patch:
        patch.setattr(
            runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
        )
        patch.setattr(runner, "load_engine", loader)
        got = runner.run_suite(route)
    assert wire(got) == wire(fixed_suite)
    names = ["primary", "reference"] if route == "compare" else [route]
    assert calls == [(name, p["family"]) for p in problems for name in names]


def at_path(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def changed_fraction(tree, path):
    return replaced(tree, path, fw(fraction(at_path(tree, path)) + 1))


@pytest.mark.fixed
def test_fixed_complete_family_nonvacuous_mutations(fixed_outputs, runner):
    original = fixed_outputs[0]
    g = ("levels", 0, "geometry", 0)
    m = g + ("middles", 0)
    t = m + ("tiles", 0)
    pr = t + ("propagated", 0)
    q = g + ("quadruples", 0)
    cg = ("coarsenings", 0, "geometry", 0)
    piece = cg + ("field_blocks", 0, "pieces", 0)
    numeric = [
        ("problem", "levels", 0, "cells", 0, "bounds", 0),
        m + ("moments", 15),
        t + ("moments", 15),
        pr + ("coefficients", 8),
        pr + ("forced_coefficients", 3),
        t + ("outgoing", 0, "coefficients", 3),
        g + ("pairs", 0, "causal_integral"),
        g + ("triples", 0, "causal_integral"),
        g + ("triples", 0, "forced_integral"),
        q + ("causal_integral",),
        q + ("forced_integral",),
        q + ("forced_error",),
        q + ("mean_product",),
        q + ("mean_error",),
        q + ("third_covariance",),
        q + ("centered_integral",),
        q + ("conditional",),
        cg + ("moment_blocks", 0, "child_moment_sum", 15),
        piece + ("coarse_coefficients", 8),
        piece + ("child_coefficient_sum", 8),
        cg + ("blocks", 0, "child_integral_sum"),
        ("coarsenings", 2, "geometry", 0, "blocks", 0, "via_middle_integral"),
    ]
    mutations = [changed_fraction(original, path) for path in numeric]
    mutations.extend(
        [
            replaced(
                original,
                pr + ("bilinear_admissible",),
                not at_path(original, pr + ("bilinear_admissible",)),
            ),
            replaced(
                original,
                q + ("propagated_bilinear",),
                not at_path(original, q + ("propagated_bilinear",)),
            ),
            replaced(
                original, piece + ("fine_tile",), at_path(original, piece + ("fine_tile",)) + 1
            ),
            replaced(
                original,
                cg + ("blocks", 0, "children"),
                at_path(original, cg + ("blocks", 0, "children"))[:-1],
            ),
            replaced(
                original,
                ("counts", "propagated_entries"),
                original["counts"]["propagated_entries"] + 1,
            ),
            replaced(
                original,
                ("counts", "field_child_terms"),
                original["counts"]["field_child_terms"] + 1,
            ),
        ]
    )
    assert len(mutations) == 28
    expected = wire(original)
    for changed in mutations:
        assert wire(changed) != expected
        with pytest.raises(ValueError):
            runner.verify_suite(changed, original)


@pytest.mark.fixed
def test_fixed_nonvacuous_suite_payload_controls_and_scope_mutations(fixed_suite, runner):
    mutations = [
        replaced(fixed_suite, ("controls", "quadruple_partition"), False),
        replaced(fixed_suite, ("prior_bridges", "AM_moments_consumed"), True),
        replaced(fixed_suite, ("scope", "universal_fixed_degree_closure"), True),
        replaced(
            fixed_suite,
            ("payload_sizes", 0, "moment_contract_bytes"),
            fixed_suite["payload_sizes"][0]["moment_contract_bytes"] + 1,
        ),
        replaced(
            fixed_suite,
            ("payload_sizes", 0, "coarsening_witness_bytes"),
            fixed_suite["payload_sizes"][0]["coarsening_witness_bytes"] + 1,
        ),
        replaced(
            fixed_suite,
            ("totals", "quadruple_tile_visits"),
            fixed_suite["totals"]["quadruple_tile_visits"] + 1,
        ),
    ]
    before = wire(fixed_suite)
    for changed in mutations:
        assert wire(changed) != before
        with pytest.raises(ValueError):
            runner.verify_suite(changed, fixed_suite)
    for key in ("pair", "triple", "quadruple"):
        path = (0, "levels", 0, "geometry", 0, "summary", key + "_integral")
        bad = changed_fraction(fixed_suite["families"], path)
        assert wire(bad) != wire(fixed_suite["families"])
        with pytest.raises(ValueError):
            runner.controls(bad)


@pytest.mark.fixed
def test_fixed_nonvacuous_selected_AM_projection_mutations(fixed_data, fixed_outputs, runner):
    _, original, _ = fixed_data
    contexts = original[0]["problem"]["contexts"]
    index = next(i for i, c in enumerate(contexts) if c["probe"] == "whole")
    c = (0, "problem", "contexts", index)
    m = c + ("middles", 0)
    mutations = [
        changed_fraction(original, c + ("probe_bounds", 0)),
        changed_fraction(original, m + ("bounds", 0)),
        replaced(original, m + ("event",), at_path(original, m + ("event",)) + 100),
        replaced(original, c + ("level",), "wrong"),
        replaced(original, c + ("probe",), "not_whole"),
        replaced(original, c + ("middles",), at_path(original, c + ("middles",))[:-1]),
        replaced(original, (0, "problem", "family"), "not_grid"),
    ]
    before = wire(original)
    for changed in mutations:
        assert wire(changed) != before
        with pytest.raises(ValueError):
            runner.am_bridges(fixed_outputs, changed)


@pytest.mark.fixed
def test_fixed_authenticated_source_and_prior_inventory(runner):
    identities = runner.identities()
    assert set(identities) == {"source_ledger", "prior_artifacts", "ancestor_sources"}
    assert (
        len(identities["source_ledger"]),
        len(identities["prior_artifacts"]),
        len(identities["ancestor_sources"]),
    ) == (5, 44, 39)
    assert set(identities["source_ledger"]) == {
        "README.md",
        "kernel.py",
        "reference.py",
        "study.py",
        "test_qr05an.py",
    }
    for key in ("source_ledger", "prior_artifacts", "ancestor_sources"):
        for value in identities[key].values():
            assert value["bytes"] > 0 and len(value["sha256"]) == 64
