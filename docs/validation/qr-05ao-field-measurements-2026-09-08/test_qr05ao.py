"""Bounded independent checks for the private field-measurement diagnostic.

Only tests marked fixed consume authenticated AN cases. Collection and generic
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
        load("_qr05ao_test_primary", "kernel.py"),
        load("_qr05ao_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05ao_test_runner", "study.py")


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


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True) if x and y), F())


def orthogonal_rows(rows):
    """Exact Euclidean residuals, independent of row elimination/RREF."""
    basis, orthogonal, norms, coordinates = [], [], [], []
    for index, row in enumerate(rows):
        residual = list(row)
        combination = [F()] * len(basis) + [F(1)]
        for u, norm, origin in zip(orthogonal, norms, coordinates, strict=True):
            factor = dot(row, u) / norm
            if factor:
                residual = [x - factor * y for x, y in zip(residual, u, strict=True)]
                for i, c in enumerate(origin):
                    combination[i] -= factor * c
        norm = dot(residual, residual)
        if norm:
            basis.append(index)
            orthogonal.append(residual)
            norms.append(norm)
            coordinates.append(combination)
    return basis, orthogonal, norms, coordinates


def basis_coordinates(row, orthogonal, norms, coordinates):
    out = [F()] * len(orthogonal)
    residual = list(row)
    for u, norm, origin in zip(orthogonal, norms, coordinates, strict=True):
        factor = dot(row, u) / norm
        if factor:
            residual = [x - factor * y for x, y in zip(residual, u, strict=True)]
            for i, c in enumerate(origin):
                out[i] += factor * c
    assert not any(residual)
    return out


def matvec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def matmul(left, right):
    columns = list(zip(*right, strict=True))
    return [[dot(row, column) for column in columns] for row in left]


def mw(matrix):
    return [list(map(fw, row)) for row in matrix]


def fm(matrix):
    return [list(map(fraction, row)) for row in matrix]


def expected_certificate(O, Q):
    n = len(Q[0])
    A = [[F(1)] * n] + O
    basis, us, norms, coords = orthogonal_rows(A)
    selected = [A[i] for i in basis]
    # The earliest independent columns of a row basis are exactly the unique
    # RREF pivot columns. Their coordinates give each standard free vector.
    pivots, cu, cn, cc = orthogonal_rows(list(map(list, zip(*selected, strict=True))))
    trank = len(orthogonal_rows(Q)[0])
    joint = len(orthogonal_rows(selected + Q)[0])
    success = joint == len(basis)
    decoder = collision = None
    if success:
        decoder = mw([basis_coordinates(q, us, norms, coords) for q in Q])
        assert matmul(fm(decoder), selected) == Q
    else:
        for free in range(n):
            if free in pivots:
                continue
            column = [row[free] for row in selected]
            coeff = basis_coordinates(column, cu, cn, cc)
            w = [F()] * n
            w[free] = F(1)
            for pivot, x in zip(pivots, coeff, strict=True):
                w[pivot] = -x
            assert not any(matvec(A, w))
            response = matvec(Q, w)
            if any(response):
                mass = sum((x for x in w if x > 0), F())
                positive = [max(x, F()) / mass for x in w]
                negative = [max(-x, F()) / mass for x in w]
                op, on = matvec(O, positive), matvec(O, negative)
                tp, tn = matvec(Q, positive), matvec(Q, negative)
                delta = [x - y for x, y in zip(tp, tn, strict=True)]
                assert sum(positive, F()) == sum(negative, F()) == 1 and op == on
                collision = {
                    "free_column": free,
                    "difference": list(map(fw, w)),
                    "positive_weights": list(map(fw, positive)),
                    "negative_weights": list(map(fw, negative)),
                    "observed_positive": list(map(fw, op)),
                    "observed_negative": list(map(fw, on)),
                    "target_positive": list(map(fw, tp)),
                    "target_negative": list(map(fw, tn)),
                    "target_difference": list(map(fw, delta)),
                    "separating_row": next(i for i, x in enumerate(delta) if x),
                }
                break
        assert collision is not None
    return {
        "observation_rank": len(basis),
        "target_rank": trank,
        "joint_rank": joint,
        "row_basis": basis,
        "pivot_columns": pivots,
        "recoverable": success,
        "decoder": decoder,
        "collision": collision,
    }


def certificate_validity(O, Q, cert):
    # Full canonical comparison plus separate certificate equations, including
    # the normalized collision distinction; no imported producer validator.
    assert cert == expected_certificate(O, Q)
    A = [[F(1)] * len(Q[0])] + O
    if cert["recoverable"]:
        assert cert["collision"] is None
        assert matmul(fm(cert["decoder"]), [A[i] for i in cert["row_basis"]]) == Q
    else:
        c = cert["collision"]
        plus, minus = (list(map(fraction, c[k])) for k in ("positive_weights", "negative_weights"))
        assert all(x >= 0 for x in plus + minus)
        assert sum(plus, F()) == sum(minus, F()) == 1
        assert matvec(O, plus) == matvec(O, minus) == list(map(fraction, c["observed_positive"]))
        assert matvec(Q, plus) == list(map(fraction, c["target_positive"]))
        assert matvec(Q, minus) == list(map(fraction, c["target_negative"]))


def make_problem(coarse, fine, probe=UNIT, name="synthetic"):
    return {
        "family": name,
        "probe": {"name": "test", "bounds": rect(probe)},
        "coarse": {"level": "old", "cells": [{"event": i, "bounds": rect(b)} for i, b in coarse]},
        "fine": {"level": "new", "cells": [{"event": i, "bounds": rect(b)} for i, b in fine]},
    }


def single_problem():
    return make_problem([(7, UNIT)], [(7, UNIT)])


def problem_of():
    return make_problem(
        [(-2, (0, F(1, 2), 0, 1)), (9, (F(1, 2), 1, 0, 1))],
        [
            (-3, (0, F(1, 4), 0, F(1, 2))),
            (0, (0, F(1, 4), F(1, 2), 1)),
            (4, (F(1, 4), F(1, 2), 0, 1)),
            (9, (F(1, 2), 1, 0, 1)),
        ],
    )


def partial_problem():
    p = problem_of()
    p["probe"]["bounds"] = rect((0, F(3, 8), 0, F(3, 4)))
    return p


def counts_from_family(problem, geometry, matrices, certificates):
    ct, ft = geometry["coarse_tiles"], geometry["fine_tiles"]
    obs, targets = matrices["observations"], matrices["targets"]
    certs = [row["certificate"] for row in certificates]
    failed = [row for row in certificates if not row["certificate"]["recoverable"]]
    n = len(matrices["generators"])
    orows = {row["name"]: len(row["matrix"]) for row in obs}
    qrows = {row["name"]: len(row["matrix"]) for row in targets}
    return {
        "coarse_cells": len(geometry["coarse_cells"]),
        "fine_cells": len(geometry["fine_cells"]),
        "positive_coarse_cells": sum(row["bounds"] is not None for row in geometry["coarse_cells"]),
        "positive_fine_cells": sum(row["bounds"] is not None for row in geometry["fine_cells"]),
        "generators": n,
        "coarse_tiles": len(ct),
        "fine_tiles": len(ft),
        "input_bound_entries": len(problem["probe"]["bounds"])
        + sum(len(c["bounds"]) for key in ("coarse", "fine") for c in problem[key]["cells"]),
        "clipped_bound_entries": sum(
            len(c["bounds"] or []) for key in ("coarse_cells", "fine_cells") for c in geometry[key]
        ),
        "tile_bound_entries": sum(len(t["bounds"]) for t in ct + ft),
        "coarse_moment_entries": sum(len(t["moments"]) for t in ct),
        "fine_moment_entries": sum(len(t["moments"]) for t in ft),
        "coarse_outgoing_vectors": sum(len(t["outgoing"]) for t in ct),
        "coarse_outgoing_entries": sum(len(r["coefficients"]) for t in ct for r in t["outgoing"]),
        "fine_outgoing_vectors": sum(len(t["outgoing"]) for t in ft),
        "fine_outgoing_entries": sum(len(r["coefficients"]) for t in ft for r in t["outgoing"]),
        "observation_rows": sum(len(r["matrix"]) for r in obs),
        "observation_entries": sum(len(row) for r in obs for row in r["matrix"]),
        "fine_weighted_rows": len(matrices["fine_weighted"]),
        "fine_weighted_entries": sum(len(row) for row in matrices["fine_weighted"]),
        "coarse_response_rows": qrows["coarse"],
        "fine_response_rows": qrows["fine"],
        "field_rows": qrows["field"],
        "target_entries": sum(len(row) for r in targets for row in r["matrix"]),
        "geometric_decoder_entries": sum(len(row) for row in matrices["coarse_decoder"]),
        "certificates": len(certs),
        "recoverable": sum(c["recoverable"] for c in certs),
        "failed": len(failed),
        "row_basis_entries": sum(len(c["row_basis"]) for c in certs),
        "pivot_column_entries": sum(len(c["pivot_columns"]) for c in certs),
        "canonical_decoder_entries": sum(
            len(row) for c in certs if c["decoder"] is not None for row in c["decoder"]
        ),
        "collision_entries": sum(
            3 * n + 2 * orows[r["observation"]] + 3 * qrows[r["target"]] for r in failed
        ),
    }


def independent_family(problem):
    query = tuple(map(fraction, problem["probe"]["bounds"]))
    boxes = {
        key: {c["event"]: tuple(map(fraction, c["bounds"])) for c in problem[key]["cells"]}
        for key in ("coarse", "fine")
    }
    for box in boxes.values():
        assert all(not area(clipped(a, b)) for a, b in combinations(box.values(), 2))
    parent = {}
    for c, b in boxes["fine"].items():
        matches = [p for p, old in boxes["coarse"].items() if contained(b, old)]
        assert len(matches) == 1
        parent[c] = matches[0]
    children = {p: [c for c in boxes["fine"] if parent[c] == p] for p in boxes["coarse"]}
    for p, b in boxes["coarse"].items():
        partition_of(b, [boxes["fine"][c] for c in children[p]])
    clips = {key: {c: clipped(b, query) for c, b in box.items()} for key, box in boxes.items()}
    cells = {
        key: [
            {"event": c, "bounds": rect(b) if area(b) else None, "volume": fw(area(b))}
            for c, b in box.items()
        ]
        for key, box in clips.items()
    }
    tiles = {}
    for key, box in clips.items():
        assert sum((area(b) for b in box.values()), F()) == area(query)
        rows = []
        for c, bounds in box.items():
            if not area(bounds):
                continue
            breaks = [
                sorted(
                    {
                        bounds[axis],
                        bounds[axis + 1],
                        *(
                            v
                            for b in box.values()
                            if area(b)
                            for v in b[axis : axis + 2]
                            if bounds[axis] < v < bounds[axis + 1]
                        ),
                    }
                )
                for axis in (0, 2)
            ]
            for (a, b), (c0, d) in product(pairwise(breaks[0]), pairwise(breaks[1])):
                tb = (a, b, c0, d)
                row = {
                    "event": c,
                    "bounds": rect(tb),
                    "moments": list(map(fw, raw_moments(tb))),
                    "outgoing": [
                        {
                            "event": event,
                            "coefficients": list(map(fw, outgoing_coefficients(endpoint, tb))),
                        }
                        for event, endpoint in box.items()
                    ],
                }
                if key == "fine":
                    matches = [
                        i
                        for i, t in enumerate(tiles["coarse"])
                        if t["event"] == parent[c]
                        and contained(tb, tuple(map(fraction, t["bounds"])))
                    ]
                    assert len(matches) == 1
                    row["coarse_tile"] = matches[0]
                rows.append(row)
        tiles[key] = rows
    cache = {}

    def ordered(intervals):
        k = tuple(tuple(v) for v in intervals)
        if k not in cache:
            cache[k] = prefix_order(k)
        return cache[k]

    def response(bounds):
        if any(not area(b) for b in bounds):
            return F()
        return ordered([b[:2] for b in bounds]) * ordered([b[2:] for b in bounds]) / 16

    fids = list(clips["fine"])
    cids = list(clips["coarse"])
    generators = list(product(fids, repeat=2))
    coefficients = []
    fineweighted = []
    for t in tiles["fine"]:
        tb = tuple(map(fraction, t["bounds"]))
        mm = list(map(fraction, t["moments"]))
        fields = [
            field_coefficients(clips["fine"][a], clips["fine"][b], tb, ordered)
            for a, b in generators
        ]
        coefficients.append(fields)
        for k, l in BASIS:
            fineweighted.append(
                [
                    sum(
                        (x * mm[4 * (i + k) + j + l] for x, (i, j) in zip(f, PROP, strict=True)),
                        F(),
                    )
                    for f in fields
                ]
            )
    weighted = []
    for ti, _ in enumerate(tiles["coarse"]):
        for basis in range(4):
            weighted.append(
                [
                    sum(
                        (
                            fineweighted[4 * fi + basis][col]
                            for fi, t in enumerate(tiles["fine"])
                            if t["coarse_tile"] == ti
                        ),
                        F(),
                    )
                    for col in range(len(generators))
                ]
            )
    integral = weighted[::4]
    qmaps = {}
    for key, ids in (("coarse", cids), ("fine", fids)):
        rows = []
        for c, d in product(ids, repeat=2):
            direct = [
                response([clips["fine"][a], clips["fine"][b], clips[key][c], clips[key][d]])
                for a, b in generators
            ]
            integrated = [F()] * len(generators)
            for ti, t in enumerate(tiles["fine"]):
                belongs = parent[t["event"]] == c if key == "coarse" else t["event"] == c
                if not belongs:
                    continue
                tb = tuple(map(fraction, t["bounds"]))
                outgoing = outgoing_coefficients(clips[key][d], tb)
                if key == "coarse":
                    old = tiles["coarse"][t["coarse_tile"]]
                    assert outgoing == list(
                        map(
                            fraction,
                            next(r["coefficients"] for r in old["outgoing"] if r["event"] == d),
                        )
                    )
                mm = list(map(fraction, t["moments"]))
                for col, field in enumerate(coefficients[ti]):
                    integrated[col] += integrate_product(field, PROP, outgoing, BASIS, mm)
            assert integrated == direct
            rows.append(direct)
        qmaps[key] = rows
    synthesis = [row for fields in coefficients for row in zip(*fields, strict=True)]
    synthesis = [list(row) for row in synthesis]
    geometric = []
    for c, d in product(cids, repeat=2):
        geometric.append(
            [
                x
                for t in tiles["coarse"]
                for x in (
                    list(
                        map(
                            fraction,
                            next(r["coefficients"] for r in t["outgoing"] if r["event"] == d),
                        )
                    )
                    if t["event"] == c
                    else [F()] * 4
                )
            ]
        )
    assert matmul(geometric, weighted) == qmaps["coarse"]
    fineindexes = {pair: i for i, pair in enumerate(product(fids, repeat=2))}
    for index, (c, d) in enumerate(product(cids, repeat=2)):
        summed = vector_sum(
            [qmaps["fine"][fineindexes[x, y]] for x in children[c] for y in children[d]],
            len(generators),
        )
        assert summed == qmaps["coarse"][index]
    assert all(
        sum((sum(row, F()) for row in qmaps[key]), F()) == area(query) ** 4 / 576
        for key in ("coarse", "fine")
    )
    geometry = {
        "volume": fw(area(query)),
        "parents": [{"parent": p, "children": cc} for p, cc in children.items()],
        "coarse_cells": cells["coarse"],
        "fine_cells": cells["fine"],
        "coarse_tiles": tiles["coarse"],
        "fine_tiles": tiles["fine"],
    }
    observations = [
        {
            "name": "integral",
            "rows": [{"tile": i, "basis": 0} for i in range(len(tiles["coarse"]))],
            "matrix": mw(integral),
        },
        {
            "name": "weighted",
            "rows": [
                {"tile": i, "basis": j} for i in range(len(tiles["coarse"])) for j in range(4)
            ],
            "matrix": mw(weighted),
        },
    ]
    targets = [
        {
            "name": key,
            "rows": [{"first": a, "second": b} for a, b in product(ids, repeat=2)],
            "matrix": mw(qmaps[key]),
        }
        for key, ids in (("coarse", cids), ("fine", fids))
    ]
    targets.append(
        {
            "name": "field",
            "rows": [
                {"tile": i, "power": list(power)}
                for i in range(len(tiles["fine"]))
                for power in PROP
            ],
            "matrix": mw(synthesis),
        }
    )
    matrices = {
        "generators": [{"first": a, "second": b} for a, b in generators],
        "observations": observations,
        "targets": targets,
        "fine_weighted": mw(fineweighted),
        "coarse_decoder": mw(geometric),
    }
    certificates = [
        {
            "observation": o["name"],
            "target": q["name"],
            "certificate": expected_certificate(fm(o["matrix"]), fm(q["matrix"])),
        }
        for o in observations
        for q in targets
    ]
    assert certificates[3]["certificate"]["recoverable"]
    assert all(
        not certificates[i]["certificate"]["recoverable"]
        or certificates[3 + i]["certificate"]["recoverable"]
        for i in range(3)
    )
    checks = dict.fromkeys(
        (
            "weighted_contains_integral",
            "coarse_decoder_exact",
            "coarse_refinement_exact",
            "response_partition_exact",
            "measurement_refinement_exact",
        ),
        True,
    )
    return {
        "problem": copy.deepcopy(problem),
        "geometry": geometry,
        "matrices": matrices,
        "certificates": certificates,
        "checks": checks,
        "counts": counts_from_family(problem, geometry, matrices, certificates),
    }


def transformed_problem(problem, alpha, beta, du=F(), dv=F()):
    out = copy.deepcopy(problem)

    def change(raw):
        a, b, c, d = map(fraction, raw)
        return rect((alpha * a + du, alpha * b + du, beta * c + dv, beta * d + dv))

    out["probe"]["bounds"] = change(out["probe"]["bounds"])
    for key in ("coarse", "fine"):
        for cell in out[key]["cells"]:
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
                        comb(i, p)
                        * comb(j, q)
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
        return [
            fw(
                sum(
                    (
                        x
                        * k**degree
                        * comb(i, p)
                        * comb(j, q)
                        * (-du) ** (i - p)
                        * (-dv) ** (j - q)
                        / (alpha**i * beta**j)
                        for x, (i, j) in zip(old, basis, strict=True)
                        if i >= p and j >= q
                    ),
                    F(),
                )
            )
            for p, q in basis
        ]

    out = copy.deepcopy(family)
    out["problem"] = transformed_problem(family["problem"], alpha, beta, du, dv)
    geom = out["geometry"]
    geom["volume"] = fw(fraction(geom["volume"]) * k)
    for key in ("coarse_cells", "fine_cells"):
        for cell in geom[key]:
            cell["bounds"] = bounds(cell["bounds"])
            cell["volume"] = fw(fraction(cell["volume"]) * k)
    for key in ("coarse_tiles", "fine_tiles"):
        for tile in geom[key]:
            tile["bounds"] = bounds(tile["bounds"])
            tile["moments"] = moments(tile["moments"])
            for row in tile["outgoing"]:
                row["coefficients"] = coefficients(row["coefficients"], BASIS, 1)
    mats = out["matrices"]
    mats["observations"][0]["matrix"] = [
        [fw(fraction(x) * k**3) for x in row] for row in mats["observations"][0]["matrix"]
    ]

    def weighted(raw):
        old = fm(raw)
        answer = []
        for base in range(0, len(old), 4):
            m0, mu, mv, muv = old[base : base + 4]
            answer.extend(
                [
                    [fw(k**3 * x) for x in m0],
                    [fw(k**3 * (alpha * x + du * y)) for x, y in zip(mu, m0, strict=True)],
                    [fw(k**3 * (beta * x + dv * y)) for x, y in zip(mv, m0, strict=True)],
                    [
                        fw(k**3 * (k * a + alpha * dv * b + beta * du * c + du * dv * d))
                        for a, b, c, d in zip(muv, mu, mv, m0, strict=True)
                    ],
                ]
            )
        return answer

    mats["observations"][1]["matrix"] = weighted(mats["observations"][1]["matrix"])
    mats["fine_weighted"] = weighted(mats["fine_weighted"])
    for target in mats["targets"][:2]:
        target["matrix"] = [[fw(fraction(x) * k**4) for x in row] for row in target["matrix"]]
    field = mats["targets"][2]["matrix"]
    newfield = []
    for base in range(0, len(field), 9):
        cols = list(zip(*field[base : base + 9], strict=True))
        newfield.extend(
            [
                list(row)
                for row in zip(*(coefficients(list(col), PROP, 2) for col in cols), strict=True)
            ]
        )
    mats["targets"][2]["matrix"] = newfield
    coarseids = [r["event"] for r in geom["coarse_cells"]]
    mats["coarse_decoder"] = mw(
        [
            [
                x
                for t in geom["coarse_tiles"]
                for x in (
                    list(
                        map(
                            fraction,
                            next(r["coefficients"] for r in t["outgoing"] if r["event"] == d),
                        )
                    )
                    if t["event"] == c
                    else [F()] * 4
                )
            ]
            for c, d in product(coarseids, repeat=2)
        ]
    )
    out["certificates"] = [
        {
            "observation": o["name"],
            "target": q["name"],
            "certificate": expected_certificate(fm(o["matrix"]), fm(q["matrix"])),
        }
        for o in mats["observations"]
        for q in mats["targets"]
    ]
    out["counts"] = counts_from_family(out["problem"], geom, mats, out["certificates"])
    return out


LINEAR_HANDS = [
    ([], [[2, 2], [-3, -3], [0, 0]]),
    ([[0, 1]], [[1, 2]]),
    ([[0, 1, 2]], [[0, 0, 1]]),
    ([[0, 1, 2]], [[1, 2, 3], [0, 0, 1]]),
    ([[1, 0, F(1, 2)]], [[1, 0, F(1, 2)], [0, 1, F(1, 2)]]),
    ([[0, 0, 0], [1, 1, 1], [0, 0, 0]], [[0, 0, 0]]),
    ([], [[0, 0, 1, 0], [0, 1, 0, 0]]),
    ([[0, 1, 0], [0, 1, 0], [0, 0, 1]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
]


@pytest.mark.parametrize(
    "O,Q",
    LINEAR_HANDS,
    ids=[
        "normalization_only",
        "normalization_enabled",
        "collision",
        "whole_target",
        "dependent_generators",
        "zero_duplicate",
        "free_column_first",
        "redundant_rows",
    ],
)
def test_exact_canonical_orthogonal_certificate_oracle(engines, O, Q):
    O = [[F(x) for x in row] for row in O]
    Q = [[F(x) for x in row] for row in Q]
    expected = expected_certificate(O, Q)
    for module in engines:
        supplied = (mw(O), mw(Q))
        before = wire(supplied[0]) + wire(supplied[1])
        actual = module.certify(*supplied)
        assert wire(actual) == wire(expected)
        certificate_validity(O, Q, actual)
        assert wire(supplied[0]) + wire(supplied[1]) == before


def test_normalization_and_full_field_are_not_mixture_weight_recovery(engines):
    O = [[F(1), F(), F(1, 2)]]
    S = [[F(1), F(), F(1, 2)], [F(), F(1), F(1, 2)]]
    I = [[F(i == j) for j in range(3)] for i in range(3)]
    for module in engines:
        cert = module.certify(mw(O), mw(S))
        assert cert["recoverable"] and cert["observation_rank"] == 2
        assert cert["row_basis"] == [0, 1] and cert["decoder"] == mw([[0, 1], [1, -1]])
        weights = module.certify(mw(O), mw(I))
        assert not weights["recoverable"]
        assert module.decode(cert["row_basis"], cert["decoder"], [fw(F(1, 2))]) == [fw(F(1, 2))] * 2
        normal = module.certify(mw([[0, 1]]), mw([[1, 2]]))
        assert normal["decoder"] == mw([[1, 1]])
        # Without the normalization row, w=(1,0) is a false "collision":
        # its positive and negative masses cannot both be one.
        assert dot([F(1), F(1)], [F(1), F()]) != 0


def test_collision_weights_use_positive_mass_and_free_column_precedes_target_row(engines):
    for module in engines:
        c = module.certify(mw([[0, 1, 2]]), mw([[0, 0, 1]]))["collision"]
        assert c["difference"] == list(map(fw, [1, -2, 1]))
        assert c["positive_weights"] == list(map(fw, [F(1, 2), 0, F(1, 2)]))
        assert c["negative_weights"] == list(map(fw, [0, 1, 0]))
        assert c["observed_positive"] == c["observed_negative"] == [fw(1)]
        assert c["target_difference"] == [fw(F(1, 2))]
        # Q*w=1 differs from the target difference between normalized mixtures.
        assert c["target_difference"] != [fw(1)]
        c = module.certify([], mw([[0, 0, 1, 0], [0, 1, 0, 0]]))["collision"]
        assert c["free_column"] == 1 and c["separating_row"] == 1
        assert c["difference"] == list(map(fw, [-1, 1, 0, 0]))


def test_exact_tiny_rank_and_retained_not_intermediate_bit_boundary(engines):
    d = 1 << 4095
    O = [[F(1), F(), F()], [F(), F(1, d), F()]]
    Q = [[F(i == j) for j in range(3)] for i in range(3)]
    for module in engines:
        actual = module.certify(mw(O), mw(Q))
        assert actual == expected_certificate(O, Q) and actual["observation_rank"] == 3
        zero = module.certify(mw([O[0], [0, 0, 0]]), mw(Q))
        assert zero["observation_rank"] == 2 and not zero["recoverable"]
        with pytest.raises(ValueError):
            module.certify(mw([[0, F(1, d)]]), mw([[0, 2]]))
        # Individual products have 4097 bits but the retained result is zero.
        assert module.decode([0, 1, 2], mw([[0, d, -d]]), list(map(fw, [2, 2]))) == [fw(0)]
        with pytest.raises(ValueError):
            module.decode([0, 1], mw([[0, d]]), [fw(2)])


def test_decode_is_restricted_linear_application_not_certificate_authentication(
    engines, monkeypatch
):
    for module in engines:
        cert = module.certify(mw([[0, 1]]), mw([[1, 2]]))
        observed = [fw(F(1, 3))]

        def forbidden(*args, **kwargs):
            raise RuntimeError("online decoder used forbidden offline access")

        with monkeypatch.context() as patch:
            patch.setattr(module, "certify", forbidden)
            patch.setattr(module, "build_family", forbidden)
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            assert module.decode(cert["row_basis"], cert["decoder"], observed) == [fw(F(4, 3))]
            # A different supplied linear map is applied, not semantically
            # authenticated. It does not authorize reading a hidden target.
            assert module.decode([0], mw([[7]]), observed) == [fw(7)]
        assert observed == [fw(F(1, 3))]


@pytest.mark.parametrize(
    "factory", [single_problem, problem_of, partial_problem], ids=["unit", "unequal", "empty_clips"]
)
def test_generic_complete_independent_family_oracle(engines, factory):
    problem = factory()
    expected = independent_family(problem)
    before = wire(problem)
    for module in engines:
        actual = module.build_family(problem)
        assert wire(actual) == wire(expected) and wire(problem) == before
        mats = actual["matrices"]
        for row in actual["certificates"]:
            O = fm(
                next(x["matrix"] for x in mats["observations"] if x["name"] == row["observation"])
            )
            Q = fm(next(x["matrix"] for x in mats["targets"] if x["name"] == row["target"]))
            certificate_validity(O, Q, row["certificate"])


def test_unit_field_moments_and_geometric_decoder_are_not_geometry_moments(engines):
    for module in engines:
        f = module.build_family(single_problem())
        mats = f["matrices"]
        assert mats["observations"][0]["matrix"] == [[fw(F(1, 288))]]
        assert mats["observations"][1]["matrix"] == [
            [fw(F(1, 288))],
            [fw(F(1, 384))],
            [fw(F(1, 384))],
            [fw(F(1, 512))],
        ]
        assert mats["targets"][0]["matrix"] == [[fw(F(1, 9216))]]
        assert mats["coarse_decoder"] == mw([[F(1, 2), -F(1, 2), -F(1, 2), F(1, 2)]])
        assert f["geometry"]["coarse_tiles"][0]["moments"][0] == fw(F(1, 2))
        assert (
            mats["observations"][0]["matrix"][0][0]
            != f["geometry"]["coarse_tiles"][0]["moments"][0]
        )


def test_concrete_nonnegative_fields_collide_and_weighted_information_contains_integral(engines):
    for module in engines:
        f = module.build_family(problem_of())
        m = f["matrices"]
        observations = {r["name"]: fm(r["matrix"]) for r in m["observations"]}
        targets = {r["name"]: fm(r["matrix"]) for r in m["targets"]}
        assert observations["weighted"][::4] == observations["integral"]
        certs = {(r["observation"], r["target"]): r["certificate"] for r in f["certificates"]}
        assert certs["weighted", "coarse"]["recoverable"]
        assert not certs["integral", "field"]["recoverable"]
        collision = certs["integral", "field"]["collision"]
        plus, minus = (
            list(map(fraction, collision[key])) for key in ("positive_weights", "negative_weights")
        )
        assert sum(plus, F()) == sum(minus, F()) == 1 and all(x >= 0 for x in plus + minus)
        assert matvec(observations["integral"], plus) == matvec(observations["integral"], minus)
        assert matvec(targets["field"], plus) != matvec(targets["field"], minus)
        for target in targets:
            assert (
                not certs["integral", target]["recoverable"]
                or certs["weighted", target]["recoverable"]
            )
        assert matmul(fm(m["coarse_decoder"]), observations["weighted"]) == targets["coarse"]


@pytest.mark.parametrize(
    "transform",
    [(F(2), F(1, 2), F(), F()), (F(2), F(3), F(-3), F(5))],
    ids=["boost", "signed_affine"],
)
def test_complete_affine_matrices_recertification_and_response_transport(engines, transform):
    p = problem_of()
    base = independent_family(p)
    moved = affine_expected(base, *transform)
    assert wire(moved) == wire(independent_family(transformed_problem(p, *transform)))
    for old, new in zip(base["certificates"], moved["certificates"], strict=True):
        assert tuple(
            old["certificate"][k]
            for k in ("observation_rank", "target_rank", "joint_rank", "recoverable")
        ) == tuple(
            new["certificate"][k]
            for k in ("observation_rank", "target_rank", "joint_rank", "recoverable")
        )
    for module in engines:
        actual = module.build_family(transformed_problem(p, *transform))
        assert wire(actual) == wire(moved)
        for row in actual["certificates"]:
            if not row["certificate"]["recoverable"]:
                continue
            O = next(
                x["matrix"]
                for x in actual["matrices"]["observations"]
                if x["name"] == row["observation"]
            )
            Q = next(
                x["matrix"] for x in actual["matrices"]["targets"] if x["name"] == row["target"]
            )
            n = len(Q[0])
            weights = [F(1, n)] * n
            result = module.decode(
                row["certificate"]["row_basis"],
                row["certificate"]["decoder"],
                list(map(fw, matvec(fm(O), weights))),
            )
            assert result == list(map(fw, matvec(fm(Q), weights)))


def test_native_aliases_output_detachment_and_no_hidden_geometry_reads(engines, monkeypatch):
    p = single_problem()
    p["fine"]["cells"][0]["bounds"] = p["coarse"]["cells"][0]["bounds"]
    before = wire(p)
    expected = wire(independent_family(p))

    def forbidden(*args, **kwargs):
        raise RuntimeError("hidden read")

    for module in engines:
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            actual = module.build_family(p)
        assert wire(actual) == expected and wire(p) == before
        actual["problem"]["coarse"]["cells"][0]["bounds"][0][0] = 99
        actual["matrices"]["observations"][0]["matrix"][0][0][0] = 99
        assert wire(p) == before and wire(module.build_family(p)) == expected
        O = mw([[0, 1]])
        Q = mw([[1, 2]])
        cert = module.certify(O, Q)
        cert["decoder"][0][0][0] = 99
        assert module.certify(O, Q)["decoder"] == mw([[1, 1]])


FAMILY_BAD = (
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
    "oversized",
)


def malformed_family(kind):
    p = problem_of()
    path = ("fine", "cells", 0)
    if kind == "extra":
        return {**p, "extra": 0}
    if kind == "missing":
        return {k: v for k, v in p.items() if k != "family"}
    if kind == "bool_id":
        return replaced(p, path + ("event",), False)
    if kind == "float":
        return replaced(p, path + ("bounds", 0, 0), 0.0)
    if kind == "tuple":
        return replaced(p, ("fine", "cells"), tuple(p["fine"]["cells"]))
    if kind == "subclass":

        class NativeList(list):
            pass

        return replaced(p, path + ("bounds",), NativeList(p["fine"]["cells"][0]["bounds"]))
    if kind == "unreduced":
        return replaced(p, path + ("bounds", 0), [0, 2])
    if kind == "zero_denominator":
        return replaced(p, path + ("bounds", 0, 1), 0)
    if kind == "degenerate":
        return replaced(p, path + ("bounds", 1), [0, 1])
    if kind == "duplicate_id":
        return replaced(p, ("fine", "cells", 1, "event"), -3)
    if kind == "unsorted":
        return replaced(p, ("fine", "cells"), p["fine"]["cells"][::-1])
    if kind == "overlap":
        return replaced(p, path + ("bounds", 3), [3, 4])
    if kind == "hole":
        return replaced(p, path + ("bounds", 3), [1, 4])
    if kind == "bad_parent":
        return replaced(p, path + ("bounds", 1), [3, 4])
    if kind == "duplicate_level":
        return replaced(p, ("fine", "level"), p["coarse"]["level"])
    if kind == "oversized":
        return replaced(p, path + ("bounds", 0, 0), 1 << 4096)
    raise AssertionError(kind)


def malformed_matrices():
    z = [0, 1]
    one = [1, 1]

    class NativeList(list):
        pass

    return [
        ((), [[z]]),
        ([], []),
        ([[z]], [[z, one]]),
        ([[z], []], [[z]]),
        ([[[False, 1]]], [[z]]),
        ([[[0.0, 1]]], [[z]]),
        ([[[0, 2]]], [[z]]),
        ([[[0, 0]]], [[z]]),
        ([[z]], [NativeList([z])]),
        ([[z]], [[[1 << 4096, 1]]]),
        ([], [[]]),
        ([], [[z] * 65]),
        ([[z]] * 32769, [[z]]),
        ([], [[z]] * 32769),
    ]


def malformed_decodes():
    z = [0, 1]
    one = [1, 1]
    return [
        ([], [[one]], []),
        ([False], [[one]], []),
        ([1], [[one]], [one]),
        ([0, 0], [[one, one]], []),
        ([0, 2, 1], [[one, one, one]], [one, one]),
        ([0, 2], [[one, one]], [one]),
        ([0], [], []),
        ([0], [[one, one]], []),
        ([0], [[[0, 2]]], []),
        ([0], [[[True, 1]]], []),
        ([0], [[one]], (one,)),
        ([0], [[one]], [[0.0, 1]]),
        ([0], [[one]], [[1 << 4096, 1]]),
        ([0], [[one]], [z] * 32769),
        ([0], [[one]] * 32769, []),
        (list(range(65)), [[one] * 65], [one] * 64),
    ]


@pytest.mark.parametrize("kind", FAMILY_BAD)
def test_bounded_native_geometry_admission(engines, kind):
    for module in engines:
        with pytest.raises(ValueError):
            module.build_family(malformed_family(kind))


def test_matrix_and_decoder_native_shape_limits(engines):
    for module in engines:
        for O, Q in malformed_matrices():
            with pytest.raises(ValueError):
                module.certify(O, Q)
        for args in malformed_decodes():
            with pytest.raises(ValueError):
                module.decode(*args)


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_normal_optimized_public_guards(tmp_path, optimized):
    program = r"""
import importlib.util,json,sys
spec=importlib.util.spec_from_file_location("ao_test_guard",sys.argv[1])
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
engines=[t.load("ao_guard_primary","kernel.py"),t.load("ao_guard_reference","reference.py")]
rejections=0
def reject(fn,*args):
    global rejections
    try: fn(*args)
    except ValueError: rejections+=1
    else: raise RuntimeError("invalid input accepted")
for e in engines:
    for kind in t.FAMILY_BAD: reject(e.build_family,t.malformed_family(kind))
    for args in t.malformed_matrices():reject(e.certify,*args)
    for args in t.malformed_decodes():reject(e.decode,*args)
    cert=e.certify(t.mw([[0,1,2]]),t.mw([[0,0,1]]))
    c=cert["collision"]
    if c["difference"]!=list(map(t.fw,[1,-2,1])) or c["target_difference"]!=[t.fw(t.F(1,2))]:
        raise RuntimeError("normalization")
    if e.decode([0,1],t.mw([[1,1]]),[t.fw(t.F(1,3))])!=[t.fw(t.F(4,3))]:
        raise RuntimeError("decode")
if rejections!=92:raise RuntimeError(("guard inventory",rejections))
print(json.dumps({"rejections":rejections}))
"""
    cmd = (
        [sys.executable, "-I"]
        + (["-O"] if optimized else [])
        + [
            "-X",
            f"pycache_prefix={tmp_path / 'cache'}",
            "-c",
            program,
            str(HERE / "test_qr05ao.py"),
        ]
    )
    result = subprocess.run(
        cmd, capture_output=True, text=True, check=True, env={**os.environ, "PYTEST_ADDOPTS": ""}
    )
    assert json.loads(result.stdout) == {"rejections": 92}


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


def at_path(tree, path):
    for key in path:
        tree = tree[key]
    return tree


def changed_fraction(tree, path):
    return replaced(tree, path, fw(fraction(at_path(tree, path)) + 1))


def test_nonvacuous_canonical_certificate_and_collision_corruptions():
    O = fm(mw([[0, 1, 2]]))
    Q = fm(mw([[0, 0, 1]]))
    original = expected_certificate(O, Q)
    paths = [
        ("collision", "difference", 0),
        ("collision", "positive_weights", 0),
        ("collision", "negative_weights", 1),
        ("collision", "observed_positive", 0),
        ("collision", "observed_negative", 0),
        ("collision", "target_positive", 0),
        ("collision", "target_negative", 0),
        ("collision", "target_difference", 0),
    ]
    changes = [changed_fraction(original, p) for p in paths]
    changes.extend(
        [
            replaced(original, ("collision", "free_column"), 1),
            replaced(original, ("collision", "separating_row"), 1),
            replaced(original, ("row_basis",), [0]),
            replaced(original, ("pivot_columns",), [0]),
            replaced(original, ("target_rank",), 2),
            replaced(original, ("joint_rank",), 2),
            replaced(original, ("recoverable",), True),
        ]
    )
    assert len(changes) == 15
    for changed in changes:
        assert wire(changed) != wire(original)
        with pytest.raises(AssertionError):
            certificate_validity(O, Q, changed)
    O = fm(mw([[0, 1]]))
    Q = fm(mw([[1, 2]]))
    original = expected_certificate(O, Q)
    changed = changed_fraction(original, ("decoder", 0, 0))
    assert wire(changed) != wire(original)
    with pytest.raises(AssertionError):
        certificate_validity(O, Q, changed)


def independent_projection(previous):
    assert [f["problem"]["family"] for f in previous] == list(FAMILIES)
    out = []
    for old in previous:
        p = old["problem"]
        assert [l["level"] for l in p["levels"]] == ["l0", "l1", "l2"]
        assert len(p["probes"]) == 1 and p["probes"][0]["name"] == "whole"
        assert [len(l["cells"]) for l in p["levels"]] == [6, 7, 8]
        out.append(
            {
                "family": p["family"],
                "probe": copy.deepcopy(p["probes"][0]),
                "coarse": copy.deepcopy(p["levels"][1]),
                "fine": copy.deepcopy(p["levels"][2]),
            }
        )
    return out


def independent_bridges(families, previous):
    assert [f["problem"] for f in families] == independent_projection(previous)
    checked = 0
    for family, old in zip(families, previous, strict=True):
        ids = [c["event"] for c in family["problem"]["fine"]["cells"]]
        oldg = old["levels"][2]["geometry"][0]
        assert oldg["probe"] == "whole"
        assert [m["event"] for m in oldg["middles"]] == ids
        oldtiles = [(m["event"], t) for m in oldg["middles"] for t in m["tiles"]]
        newtiles = family["geometry"]["fine_tiles"]
        assert len(oldtiles) == len(newtiles)
        field = []
        labels = []
        generators = family["matrices"]["generators"]
        assert generators == [{"first": a, "second": b} for a, b in product(ids, repeat=2)]
        for ti, ((event, oldtile), new) in enumerate(zip(oldtiles, newtiles, strict=True)):
            assert (event, oldtile["bounds"]) == (new["event"], new["bounds"])
            assert [
                {"first": r["first"], "second": r["second"]} for r in oldtile["propagated"]
            ] == generators
            for pi, power in enumerate(PROP):
                field.append([r["coefficients"][pi] for r in oldtile["propagated"]])
                labels.append({"tile": ti, "power": list(power)})
        target = family["matrices"]["targets"][2]
        assert target == {"name": "field", "rows": labels, "matrix": field}
        quadrows = oldg["quadruples"]
        oldanswers = {
            tuple(row[k] for k in ("first", "second", "third", "last")): row["causal_integral"]
            for row in quadrows
        }
        assert len(quadrows) == len(oldanswers) == len(ids) ** 4
        qfine = family["matrices"]["targets"][1]
        assert qfine["rows"] == [{"first": c, "second": d} for c, d in product(ids, repeat=2)]
        for row, (c, d) in zip(qfine["matrix"], product(ids, repeat=2), strict=True):
            for value, (a, b) in zip(row, product(ids, repeat=2), strict=True):
                assert value == oldanswers[a, b, c, d]
                checked += 1
    assert checked == 8192
    return {
        "AN_selected_families": list(FAMILIES),
        "AN_selected_input_geometry_equal": True,
        "AN_selected_fine_coefficients_equal": True,
        "AN_selected_fine_quadruples_equal": True,
        "AN_answers_consumed_by_engines": False,
        "AN_other_mathematics_replayed": False,
        "older_executors_run": False,
    }


def independent_payload(families):
    rows = []
    for family in families:
        m = family["matrices"]
        rows.append(
            {
                "family": family["problem"]["family"],
                "geometry_bytes": len(wire(family["geometry"])),
                "measurement_map_bytes": len(
                    wire({"generators": m["generators"], "observations": m["observations"]})
                ),
                "target_map_bytes": len(wire(m["targets"])),
                "geometric_decoder_bytes": len(wire(m["coarse_decoder"])),
                "certificate_bytes": len(wire(family["certificates"])),
                "native_family_bytes": len(wire(family)),
            }
        )
    return rows


SCOPE = (
    "generic_production_API_hardened",
    "unknown_geometry_reconstructed",
    "minimal_encoding_proved",
    "universal_compression_proved",
    "mixture_weights_recovered",
    "physical_mixture_preparation_established",
    "empirical_measurements_used",
    "noisy_measurement_robustness_tested",
    "quantum_channel_constructed",
    "gravity_derived",
    "continuum_limit_established",
    "ret_integration_tested",
    "lean_verification_performed",
    "fixed_affine_families_run",
    "full_retained_artifact_information_lost",
)


def independent_suite(families, previous):
    for f in families:
        assert f["counts"] == counts_from_family(
            f["problem"], f["geometry"], f["matrices"], f["certificates"]
        )
        assert all(f["checks"].values())
    return {
        "families": families,
        "prior_bridges": independent_bridges(families, previous),
        "payload_sizes": independent_payload(families),
        "totals": {
            "families": 2,
            **{key: sum(f["counts"][key] for f in families) for key in families[0]["counts"]},
        },
        "scope": dict.fromkeys(SCOPE, False),
    }


@pytest.fixture(scope="session")
def fixed_data(runner):
    # Lazy: generic test collection cannot project fixed AN data or run AO.
    problems, previous = runner.load_inputs()
    assert wire(problems) == wire(independent_projection(previous))
    expected = [independent_family(p) for p in problems]
    return problems, previous, expected


@pytest.fixture(scope="session")
def fixed_outputs(fixed_data, engines):
    problems, _previous, expected = fixed_data
    results = []
    for problem, wanted in zip(problems, expected, strict=True):
        before = wire(problem)
        outputs = []
        for module in engines:
            supplied = copy.deepcopy(problem)
            actual = module.build_family(supplied)
            assert wire(actual) == wire(wanted)
            assert wire(supplied) == before and wire(problem) == before
            outputs.append(actual)
        results.append(outputs[0])
    return results


@pytest.fixture(scope="session")
def fixed_suite(fixed_data, fixed_outputs, runner):
    _, previous, _ = fixed_data
    actual = runner.assemble_suite(fixed_outputs, previous)
    assert wire(actual) == wire(independent_suite(fixed_outputs, previous))
    return actual


@pytest.mark.fixed
@pytest.mark.parametrize("index", range(2), ids=FAMILIES)
def test_fixed_complete_independent_geometry_matrix_certificate_family(
    fixed_data, fixed_outputs, index
):
    assert wire(fixed_outputs[index]) == wire(fixed_data[2][index])


@pytest.mark.fixed
def test_fixed_complete_suite_selected_AN_answers_and_literal_payload(
    fixed_data, fixed_suite, runner
):
    problems, previous, expected = fixed_data
    assert wire(fixed_suite) == wire(independent_suite(expected, previous))
    assert runner.payload_sizes(expected) == independent_payload(expected)
    assert runner.project_inputs(previous)[0] == problems
    assert independent_bridges(expected, previous) == fixed_suite["prior_bridges"]
    # Nonselected AN mathematics stays outside this gate. This does not
    # bypass artifact authentication: it tests only the helper access boundary.
    changed = copy.deepcopy(previous)
    changed[0]["levels"][0]["geometry"] = []
    assert runner.an_bridges(expected, changed) == fixed_suite["prior_bridges"]


@pytest.mark.fixed
@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_cached_orchestration_routes(
    fixed_data, fixed_outputs, fixed_suite, runner, monkeypatch, route
):
    problems, previous, _ = fixed_data
    calls = []
    resultmap = {p["family"]: f for p, f in zip(problems, fixed_outputs, strict=True)}

    def loader(name):
        def build(problem):
            calls.append((name, problem["family"]))
            return copy.deepcopy(resultmap[problem["family"]])

        return SimpleNamespace(build_family=build)

    with monkeypatch.context() as patch:
        patch.setattr(
            runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
        )
        patch.setattr(runner, "load_engine", loader)
        result = runner.run_suite(route)
    assert wire(result) == wire(fixed_suite)
    names = ["primary", "reference"] if route == "compare" else [route]
    assert calls == [(name, p["family"]) for p in problems for name in names]


@pytest.mark.fixed
def test_fixed_complete_nonvacuous_family_and_certificate_wire_mutations(fixed_outputs, runner):
    original = fixed_outputs[0]
    numeric = [
        ("problem", "fine", "cells", 0, "bounds", 0),
        ("geometry", "coarse_tiles", 0, "moments", 15),
        ("geometry", "fine_tiles", 0, "moments", 15),
        ("geometry", "fine_tiles", 0, "outgoing", 0, "coefficients", 3),
        ("matrices", "observations", 0, "matrix", 0, 0),
        ("matrices", "observations", 1, "matrix", 1, 0),
        ("matrices", "fine_weighted", 0, 0),
        ("matrices", "targets", 0, "matrix", 0, 0),
        ("matrices", "targets", 1, "matrix", 0, 0),
        ("matrices", "targets", 2, "matrix", 0, 0),
        ("matrices", "coarse_decoder", 0, 0),
        ("certificates", 3, "certificate", "decoder", 0, 0),
    ]
    mutations = [changed_fraction(original, p) for p in numeric]
    mutations.extend(
        [
            replaced(
                original,
                ("geometry", "fine_tiles", 0, "coarse_tile"),
                original["geometry"]["fine_tiles"][0]["coarse_tile"] + 1,
            ),
            replaced(
                original,
                ("matrices", "generators", 0, "first"),
                original["matrices"]["generators"][0]["first"] + 99,
            ),
            replaced(original, ("matrices", "observations", 1, "rows", 0, "basis"), 1),
            replaced(original, ("matrices", "targets", 2, "rows", 0, "power"), [1, 0]),
            replaced(original, ("certificates", 3, "certificate", "row_basis"), []),
            replaced(
                original,
                ("certificates", 3, "certificate", "observation_rank"),
                original["certificates"][3]["certificate"]["observation_rank"] + 1,
            ),
            replaced(original, ("certificates", 3, "certificate", "recoverable"), False),
            replaced(original, ("checks", "measurement_refinement_exact"), False),
            replaced(
                original,
                ("counts", "collision_entries"),
                original["counts"]["collision_entries"] + 1,
            ),
            replaced(
                original,
                ("counts", "canonical_decoder_entries"),
                original["counts"]["canonical_decoder_entries"] + 1,
            ),
        ]
    )
    assert len(mutations) == 22
    before = wire(original)
    for changed in mutations:
        assert wire(changed) != before
        with pytest.raises(ValueError):
            runner.verify_suite(changed, original)


@pytest.mark.fixed
def test_fixed_nonvacuous_suite_scope_payload_and_controls(fixed_suite, runner):
    paths = [
        ("payload_sizes", 0, "geometry_bytes"),
        ("payload_sizes", 0, "measurement_map_bytes"),
        ("payload_sizes", 0, "target_map_bytes"),
        ("payload_sizes", 0, "geometric_decoder_bytes"),
        ("payload_sizes", 0, "certificate_bytes"),
        ("totals", "row_basis_entries"),
    ]
    mutations = [replaced(fixed_suite, p, at_path(fixed_suite, p) + 1) for p in paths]
    mutations.extend(
        [
            replaced(fixed_suite, ("prior_bridges", "AN_answers_consumed_by_engines"), True),
            replaced(fixed_suite, ("scope", "mixture_weights_recovered"), True),
        ]
    )
    before = wire(fixed_suite)
    for changed in mutations:
        assert wire(changed) != before
        with pytest.raises(ValueError):
            runner.verify_suite(changed, fixed_suite)
    bad = replaced(fixed_suite["families"], (0, "checks", "coarse_decoder_exact"), False)
    assert wire(bad) != wire(fixed_suite["families"])
    with pytest.raises(ValueError):
        runner.controls(bad)


@pytest.mark.fixed
def test_fixed_nonvacuous_selected_AN_geometry_coefficient_and_answer_changes(
    fixed_data, fixed_outputs, runner
):
    _, original, _ = fixed_data
    g = (0, "levels", 2, "geometry", 0)
    tile = g + ("middles", 0, "tiles", 0)
    paths = [
        (0, "problem", "probes", 0, "bounds", 0),
        (0, "problem", "levels", 1, "cells", 0, "bounds", 0),
        tile + ("bounds", 0),
        tile + ("propagated", 0, "coefficients", 8),
        g + ("quadruples", 0, "causal_integral"),
    ]
    mutations = [changed_fraction(original, p) for p in paths]
    mutations.extend(
        [
            replaced(
                original,
                g + ("middles", 0, "event"),
                at_path(original, g + ("middles", 0, "event")) + 99,
            ),
            replaced(
                original,
                tile + ("propagated", 0, "second"),
                at_path(original, tile + ("propagated", 0, "second")) + 99,
            ),
            replaced(original, g + ("quadruples",), at_path(original, g + ("quadruples",))[:-1]),
            replaced(original, g + ("middles", 0, "tiles"), []),
            replaced(original, (0, "problem", "fine"), {"unexpected": True}),
        ]
    )
    assert len(mutations) == 10
    before = wire(original)
    for changed in mutations:
        assert wire(changed) != before
        with pytest.raises(ValueError):
            runner.an_bridges(fixed_outputs, changed)


@pytest.mark.fixed
def test_fixed_source_and_prior_inventory(runner):
    ids = runner.identities()
    assert (
        len(ids["source_ledger"]),
        len(ids["prior_artifacts"]),
        len(ids["ancestor_sources"]),
    ) == (5, 45, 44)
    assert set(ids["source_ledger"]) == {
        "README.md",
        "kernel.py",
        "reference.py",
        "study.py",
        "test_qr05ao.py",
    }
    for rows in ids.values():
        for value in rows.values():
            assert value["bytes"] > 0 and len(value["sha256"]) == 64
