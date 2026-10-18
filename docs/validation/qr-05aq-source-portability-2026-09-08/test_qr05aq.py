"""Independent exact checks for frozen-policy source-span portability.

Only test names containing fixed consume authenticated AP/AO cases. Collection and generic
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
from itertools import pairwise, product
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
        load("_qr05aq_test_primary", "kernel.py"),
        load("_qr05aq_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05aq_test_runner", "study.py")


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


BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))
MOMENTS = tuple(product(range(4), repeat=2))
POWERS = tuple(product(range(3), repeat=2))
UNIT = (F(), F(1), F(), F(1))
CHECKS = (
    "old_response_identities",
    "geometric_policy_authenticated",
    "moment_additivity",
    "bernstein_partition",
    "generator_integrals",
    "constant_field_observations",
    "constant_field_responses",
    "geometric_portability",
    "witnesses_valid",
)
SCOPE = (
    "decoder_refitted",
    "old_convex_hull_inclusion_proved",
    "full_field_recovery_extended",
    "physical_sources_established",
    "empirical_noise_calibrated",
    "arbitrary_field_error_bound_proved",
    "unknown_geometry_reconstructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "ret_integration_tested",
    "lean_verification_performed",
    "generic_production_API_hardened",
    "fixed_affine_families_run",
)


def encode(value):
    if type(value) is F:
        return fw(value)
    if type(value) is list:
        return [encode(v) for v in value]
    if type(value) is dict:
        return {k: encode(v) for k, v in value.items()}
    return value


def matrix(value):
    return [[fraction(x) for x in row] for row in value]


def zeros(rows, columns):
    return [[F() for _ in range(columns)] for _ in range(rows)]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), F())


def mm(a, b):
    return [[dot(row, col) for col in zip(*b, strict=True)] for row in a]


def power_integral(a, b, p):
    return (b ** (p + 1) - a ** (p + 1)) / (p + 1) if a < b else F()


def rectangle_moments(bounds):
    a, b, c, d = bounds
    return [power_integral(a, b, i) * power_integral(c, d, j) / 2 for i, j in MOMENTS]


def bernstein_coefficients(i, a, b):
    """General binomial product expansion, not explicit coefficient triples."""
    out = [F()] * 3
    for r in range(i + 1):
        for s in range(3 - i):
            out[r + s] += (
                F(comb(2, i) * comb(i, r) * comb(2 - i, s) * (-1) ** s)
                * (-a) ** (i - r)
                * b ** (2 - i - s)
                / (b - a) ** 2
            )
    return out


def beta_integral(i, a, b, lower, upper, power=0):
    """Separable incomplete-beta integral of global u^power B_i(local u)."""
    lo, hi = max(a, lower), min(b, upper)
    if lo >= hi:
        return F()
    width = b - a
    x, y = (lo - a) / width, (hi - a) / width
    total = F()
    for r in range(power + 1):
        factor = F(comb(power, r)) * a ** (power - r) * width**r * comb(2, i)
        for k in range(3 - i):
            degree = i + r + k + 1
            total += factor * ((-1) ** k) * comb(2 - i, k) * (y**degree - x**degree) / degree
    return width * total


def beta_tail(i, a, b, c, d):
    """Integrate Bernstein times a direct outgoing clamp, independently of G."""
    constant = (d - c) * beta_integral(i, a, b, a, min(b, c))
    lo, hi = max(a, c), min(b, d)
    varying = (
        d * beta_integral(i, a, b, lo, hi) - beta_integral(i, a, b, lo, hi, 1) if lo < hi else F()
    )
    return constant + varying


def tail_integral(a, b, c, d):
    lower = (d - c) * max(F(), min(b, c) - a)
    lo, hi = max(a, c), min(b, d)
    return lower + (d * (hi - lo) - (hi**2 - lo**2) / 2 if lo < hi else F())


def response_integral(support, target, i, j, volume):
    if target is None:
        return F()
    a, b, c, d = support
    x, y, z, t = target
    return volume**2 * beta_tail(i, a, b, x, y) * beta_tail(j, c, d, z, t) / 4


def constant_response(source, target, volume):
    if source is None or target is None:
        return F()
    a, b, c, d = source
    x, y, z, t = target
    return volume**2 * tail_integral(a, b, x, y) * tail_integral(c, d, z, t) / 4


def outgoing(bounds, target):
    """Obtain the admitted bilinear polynomial from interior-point differences."""
    if target is None:
        return [F()] * 4
    a, b, c, d = bounds
    x, y, z, t = target
    if a >= y or c >= t:
        return [F()] * 4
    assert not any(a < k < b for k in (x, y))
    assert not any(c < k < d for k in (z, t))
    us = ((2 * a + b) / 3, (a + 2 * b) / 3)
    vs = ((2 * c + d) / 3, (c + 2 * d) / 3)

    def tail(point, lo, hi):
        return min(hi - lo, max(F(), hi - point))

    def linear(points, lo, hi):
        first, second = (tail(v, lo, hi) for v in points)
        slope = (second - first) / (points[1] - points[0])
        return first - slope * points[0], slope

    pu, pv = linear(us, x, y), linear(vs, z, t)
    return [pu[0] * pv[0] / 2, pu[1] * pv[0] / 2, pu[0] * pv[1] / 2, pu[1] * pv[1] / 2]


def geometric_matrix(problem):
    cells = problem["coarse_cells"]
    bounds = {
        c["event"]: None if c["bounds"] is None else tuple(map(fraction, c["bounds"]))
        for c in cells
    }
    return [
        [
            x
            for tile in problem["coarse_tiles"]
            for x in (
                outgoing(tuple(map(fraction, tile["bounds"])), bounds[d["event"]])
                if tile["event"] == c["event"]
                else [F()] * 4
            )
        ]
        for c in cells
        for d in cells
    ]


def dense(problem):
    q, m = len(problem["old_targets"]), len(problem["old_observations"])
    a, linear = [F()] * q, zeros(q, m)
    for row, values in enumerate(matrix(problem["canonical"]["decoder"])):
        for index, value in zip(problem["canonical"]["row_basis"], values, strict=True):
            if index == 0:
                a[row] = value
            else:
                linear[row][index - 1] = value
    return a, linear


def expected(problem):
    """Whole-family oracle; true responses never use either frozen decoder."""
    native(problem)
    probe = tuple(map(fraction, problem["probe"]))
    volume = area(probe)

    def cells_of(name):
        answer = []
        for cell in problem[name]:
            b = None if cell["bounds"] is None else tuple(map(fraction, cell["bounds"]))
            answer.append((cell["event"], b, F() if b is None else area(b)))
        assert [x[0] for x in answer] == sorted({x[0] for x in answer})
        partition_of(probe, [b for _, b, _ in answer if b is not None])
        return answer

    coarse, fine = cells_of("coarse_cells"), cells_of("fine_cells")
    parents = {}
    for event, bounds, _ in fine:
        choices = [
            event_c
            for event_c, b, _ in coarse
            if b is not None and bounds is not None and contained(bounds, b)
        ]
        assert len(choices) == (0 if bounds is None else 1)
        parents[event] = choices[0] if choices else None
    for event, bounds, _ in coarse:
        if bounds is not None:
            partition_of(bounds, [b for e, b, _ in fine if parents[e] == event])
    ct, ft = [], []
    for tile in problem["coarse_tiles"]:
        b = tuple(map(fraction, tile["bounds"]))
        ct.append(
            {
                **copy.deepcopy(tile),
                "moments": rectangle_moments(b),
                "outgoing": [{"event": e, "coefficients": outgoing(b, d)} for e, d, _ in coarse],
            }
        )
    for tile in problem["fine_tiles"]:
        b = tuple(map(fraction, tile["bounds"]))
        owner = ct[tile["coarse_tile"]]
        assert parents[tile["event"]] == owner["event"]
        assert contained(b, tuple(map(fraction, owner["bounds"])))
        ft.append({**copy.deepcopy(tile), "moments": rectangle_moments(b)})
    for level, tiles in ((coarse, ct), (fine, ft)):
        for e, b, _ in level:
            owned = [tuple(map(fraction, t["bounds"])) for t in tiles if t["event"] == e]
            if b is None:
                assert not owned
            else:
                partition_of(b, owned)
    for index, tile in enumerate(ct):
        children = [t for t in ft if t["coarse_tile"] == index]
        partition_of(
            tuple(map(fraction, tile["bounds"])),
            [tuple(map(fraction, t["bounds"])) for t in children],
        )
        assert tile["moments"] == [sum((t["moments"][j] for t in children), F()) for j in range(16)]
    g = geometric_matrix(problem)
    assert g == matrix(problem["geometric"])
    old_o, old_q = matrix(problem["old_observations"]), matrix(problem["old_targets"])
    policies = [("canonical", *dense(problem)), ("geometric", [F()] * len(old_q), g)]
    for _, a, linear in policies:
        assert [
            [x + dot(row, col) for col in zip(*old_o, strict=True)]
            for x, row in zip(a, linear, strict=True)
        ] == old_q
    rows = [{"first": a, "second": b} for a, _, _ in coarse for b, _, _ in coarse]
    scales = [volume**2 * a * b for _, _, a in coarse for _, _, b in coarse]
    assert all(s or not any(row) for s, row in zip(scales, old_q, strict=True))
    m, q, n = 4 * len(ct), len(rows), 9 * len(ft)
    o, new_q, integrals = zeros(m, n), zeros(q, n), []
    generators = []
    for tile_index, tile in enumerate(ft):
        bounds = tuple(map(fraction, tile["bounds"]))
        a, b, c, d = bounds
        ct_index = tile["coarse_tile"]
        owner = ct[ct_index]["event"]
        for i, j in POWERS:
            column = len(generators)
            cu, cv = bernstein_coefficients(i, a, b), bernstein_coefficients(j, c, d)
            generators.append(
                {
                    "tile": tile_index,
                    "i": i,
                    "j": j,
                    "coefficients": [volume**2 * cu[p] * cv[r] for p, r in POWERS],
                }
            )
            for basis, (p, r) in enumerate(BASIS):
                o[4 * ct_index + basis][column] = (
                    volume**2
                    * beta_integral(i, a, b, a, b, p)
                    * beta_integral(j, c, d, c, d, r)
                    / 2
                )
            integrals.append(sum((o[4 * t][column] for t in range(len(ct))), F()))
            assert integrals[-1] == volume**2 * area(bounds) / 9
            for row, (coarse_event, _, _) in enumerate(coarse):
                for k, (_, target, _) in enumerate(coarse):
                    new_q[row * len(coarse) + k][column] = (
                        response_integral(bounds, target, i, j, volume)
                        if coarse_event == owner
                        else F()
                    )
        subset = generators[-9:]
        assert [sum((gen["coefficients"][k] for gen in subset), F()) for k in range(9)] == [
            volume**2,
            *[F()] * 8,
        ]
    constant_o = [
        volume**2 * t["moments"][MOMENTS.index(exponent)] for t in ct for exponent in BASIS
    ]
    constant_q = [constant_response(a, b, volume) for _, a, _ in coarse for _, b, _ in coarse]
    assert [sum(row, F()) for row in o] == constant_o
    assert [sum(row, F()) for row in new_q] == constant_q
    assert sum(integrals, F()) == volume**3
    decoders = []
    for name, a, linear in policies:
        predicted = [
            [x + dot(row, col) for col in zip(*o, strict=True)]
            for x, row in zip(a, linear, strict=True)
        ]
        residuals = [
            [a - b for a, b in zip(x, y, strict=True)]
            for x, y in zip(predicted, new_q, strict=True)
        ]
        normalized = [
            None if not s else [v / s for v in row]
            for s, row in zip(scales, residuals, strict=True)
        ]
        failed_rows = [r for r, row in enumerate(residuals) if any(row)]
        failed_generators = [j for j in range(n) if any(row[j] for row in residuals)]
        bounds = []
        for row in normalized:
            if row is None:
                bounds.append(None)
                continue
            lower, upper = min(row), max(row)
            absolute = max(map(abs, row))
            bounds.append(
                {
                    "minimum": lower,
                    "minimum_generators": [j for j, x in enumerate(row) if x == lower],
                    "maximum": upper,
                    "maximum_generators": [j for j, x in enumerate(row) if x == upper],
                    "max_abs": absolute,
                    "max_abs_generators": [j for j, x in enumerate(row) if abs(x) == absolute],
                }
            )
        witness = None
        if failed_generators:
            j = failed_generators[0]
            r = next(r for r, row in enumerate(residuals) if row[j])
            witness = {
                "generator": j,
                "separating_row": r,
                "weights": [F(k == j) for k in range(n)],
                "observed": [row[j] for row in o],
                "truth": [row[j] for row in new_q],
                "predicted": [row[j] for row in predicted],
                "residual": [row[j] for row in residuals],
                "normalized_residual": [None if row is None else row[j] for row in normalized],
            }
            assert sum(witness["weights"], F()) == 1
        decoders.append(
            {
                "name": name,
                "intercept": a,
                "matrix": linear,
                "predicted": predicted,
                "residuals": residuals,
                "normalized_residuals": normalized,
                "exact": not failed_rows,
                "nonzero_entries": sum(bool(v) for row in residuals for v in row),
                "failed_rows": failed_rows,
                "failed_generators": failed_generators,
                "row_bounds": bounds,
                "witness": witness,
            }
        )
    assert decoders[1]["exact"]
    defined = sum(bool(s) for s in scales)
    counts = {
        "coarse_cells": len(coarse),
        "fine_cells": len(fine),
        "positive_coarse_cells": sum(bool(v) for _, _, v in coarse),
        "positive_fine_cells": sum(bool(v) for _, _, v in fine),
        "coarse_tiles": len(ct),
        "fine_tiles": len(ft),
        "old_generators": len(old_o[0]),
        "new_generators": n,
        "observation_rows": m,
        "response_rows": q,
        "defined_response_rows": defined,
        "undefined_response_rows": q - defined,
        "coarse_moment_entries": sum(len(t["moments"]) for t in ct),
        "fine_moment_entries": sum(len(t["moments"]) for t in ft),
        "coarse_outgoing_entries": sum(len(r["coefficients"]) for t in ct for r in t["outgoing"]),
        "source_coefficient_entries": sum(len(g["coefficients"]) for g in generators),
        "observation_entries": sum(map(len, o)),
        "target_entries": sum(map(len, new_q)),
        "generator_integral_entries": len(integrals),
        "constant_observation_entries": len(constant_o),
        "constant_target_entries": len(constant_q),
        "raw_decoder_entries": sum(
            len(d["intercept"]) + sum(map(len, d["matrix"])) for d in decoders
        ),
        "prediction_entries": sum(sum(map(len, d["predicted"])) for d in decoders),
        "residual_entries": sum(sum(map(len, d["residuals"])) for d in decoders),
        "normalized_residual_entries": sum(
            sum(len(r) for r in d["normalized_residuals"] if r is not None) for d in decoders
        ),
        "nonzero_residual_entries": sum(d["nonzero_entries"] for d in decoders),
        "failed_rows": sum(len(d["failed_rows"]) for d in decoders),
        "failed_generators": sum(len(d["failed_generators"]) for d in decoders),
        "row_bound_entries": sum(3 for d in decoders for r in d["row_bounds"] if r is not None),
        "bound_attainer_indices": sum(
            len(r[k])
            for d in decoders
            for r in d["row_bounds"]
            if r is not None
            for k in ("minimum_generators", "maximum_generators", "max_abs_generators")
        ),
        "witnesses": sum(d["witness"] is not None for d in decoders),
        "witness_entries": sum(
            sum(x is not None for x in w[k])
            for d in decoders
            if (w := d["witness"]) is not None
            for k in (
                "weights",
                "observed",
                "truth",
                "predicted",
                "residual",
                "normalized_residual",
            )
        ),
    }
    return encode(
        {
            "problem": copy.deepcopy(problem),
            "geometry": {
                "volume": volume,
                "coarse_cells": [
                    {"event": e, "bounds": None if b is None else rect(b), "volume": v}
                    for e, b, v in coarse
                ],
                "fine_cells": [
                    {"event": e, "bounds": None if b is None else rect(b), "volume": v}
                    for e, b, v in fine
                ],
                "parents": [{"event": e, "parent": parents[e]} for e, _, _ in fine],
                "coarse_tiles": ct,
                "fine_tiles": ft,
                "response_scales": scales,
            },
            "generators": generators,
            "matrices": {
                "observation_rows": [
                    {"tile": t, "basis": b} for t in range(len(ct)) for b in range(4)
                ],
                "response_rows": rows,
                "observations": o,
                "targets": new_q,
                "generator_integrals": integrals,
                "constant_observations": constant_o,
                "constant_targets": constant_q,
            },
            "decoders": decoders,
            "checks": dict.fromkeys(CHECKS, True),
            "counts": counts,
        }
    )


def unit_problem(policy="intercept", fine_tiles=1):
    p = {
        "family": "unit-" + policy,
        "probe": rect(UNIT),
        "coarse_cells": [{"event": -4, "bounds": rect(UNIT)}],
        "fine_cells": [{"event": -4, "bounds": rect(UNIT)}],
        "coarse_tiles": [{"event": -4, "bounds": rect(UNIT)}],
        "fine_tiles": [
            {
                "event": -4,
                "bounds": rect((F(t, fine_tiles), F(t + 1, fine_tiles), 0, 1)),
                "coarse_tile": 0,
            }
            for t in range(fine_tiles)
        ],
        "old_observations": [[fw(F(1, d))] for d in (288, 384, 384, 512)],
        "old_targets": [[fw(F(1, 9216))]],
        "canonical": {"row_basis": [0], "decoder": [[fw(F(1, 9216))]]},
        "geometric": [list(map(fw, (F(1, 2), -F(1, 2), -F(1, 2), F(1, 2))))],
    }
    if policy != "intercept":
        row = [F(1, 2), -F(1, 2), -F(1, 2), F(1, 2)]
        if policy == "signed":
            row[1] += 1
            row[2] -= 1
        else:
            assert policy == "portable"
        p["canonical"] = {"row_basis": list(range(5)), "decoder": [list(map(fw, [0, *row]))]}
    return p


def signed_problem():
    p = {
        "family": "unequal-signed-null",
        "probe": rect((-2, 1, 1, 3)),
        "coarse_cells": [
            {"event": -2, "bounds": rect((-2, -1, 1, 3))},
            {"event": 0, "bounds": None},
            {"event": 9, "bounds": rect((-1, 1, 1, 3))},
        ],
        "fine_cells": [
            {"event": -7, "bounds": rect((-2, -1, 1, 2))},
            {"event": 2, "bounds": rect((-2, -1, 2, 3))},
            {"event": 9, "bounds": None},
            {"event": 11, "bounds": rect((-1, 1, 1, 3))},
        ],
        "coarse_tiles": [
            {"event": -2, "bounds": rect((-2, -1, 1, 3))},
            {"event": 9, "bounds": rect((-1, 0, 1, 3))},
            {"event": 9, "bounds": rect((0, 1, 1, 3))},
        ],
        "fine_tiles": [
            {"event": -7, "bounds": rect((-2, -1, 1, 2)), "coarse_tile": 0},
            {"event": 2, "bounds": rect((-2, -1, 2, 3)), "coarse_tile": 0},
            {"event": 11, "bounds": rect((-1, 0, 1, 3)), "coarse_tile": 1},
            {"event": 11, "bounds": rect((0, 1, 1, 3)), "coarse_tile": 2},
        ],
        "old_observations": encode(zeros(12, 2)),
        "old_targets": encode(zeros(9, 2)),
    }
    g = geometric_matrix(p)
    alternate = copy.deepcopy(g)
    alternate[1][0] = F(1)
    p["geometric"] = encode(g)
    p["canonical"] = {
        "row_basis": list(range(13)),
        "decoder": encode([[F(), *r] for r in alternate]),
    }
    return p


def knot_problem(active=False):
    rectangles = (
        [(0, F(1, 2), 0, 1), (F(1, 2), 1, 0, F(1, 2)), (F(1, 2), 1, F(1, 2), 1)]
        if active
        else [(0, F(1, 2), 0, F(1, 2)), (0, F(1, 2), F(1, 2), 1), (F(1, 2), 1, 0, 1)]
    )
    p = {
        "family": "knot-control",
        "probe": rect(UNIT),
        "coarse_cells": [{"event": i, "bounds": rect(b)} for i, b in enumerate(rectangles)],
        "fine_cells": [{"event": i, "bounds": rect(b)} for i, b in enumerate(rectangles)],
        "coarse_tiles": [{"event": i, "bounds": rect(b)} for i, b in enumerate(rectangles)],
        "fine_tiles": [
            {"event": i, "bounds": rect(b), "coarse_tile": i} for i, b in enumerate(rectangles)
        ],
        "old_observations": encode(zeros(12, 1)),
        "old_targets": encode(zeros(9, 1)),
    }
    g = zeros(9, 12) if active else geometric_matrix(p)
    p["geometric"] = encode(g)
    p["canonical"] = {"row_basis": list(range(13)), "decoder": encode([[F(), *r] for r in g])}
    return p


def basis_change(sx, sy, tx, ty, exponents=BASIS):
    return [
        [
            F(comb(i, p) * comb(j, q)) * tx ** (i - p) * ty ** (j - q) * sx**p * sy**q
            if p <= i and q <= j
            else F()
            for p, q in exponents
        ]
        for i, j in exponents
    ]


def pullback(coefficients, exponents, alpha, beta, du, dv, factor):
    return [
        sum(
            (
                factor
                * c
                * comb(i, p)
                * comb(j, q)
                * (-du) ** (i - p)
                * (-dv) ** (j - q)
                / alpha**i
                / beta**j
                for c, (i, j) in zip(coefficients, exponents, strict=True)
                if p <= i and q <= j
            ),
            F(),
        )
        for p, q in exponents
    ]


def affine_problem(problem, alpha, beta, du, dv):
    alpha, beta, du, dv = map(F, (alpha, beta, du, dv))
    assert alpha > 0 and beta > 0
    k = alpha * beta
    p = copy.deepcopy(problem)

    def moved(bounds):
        if bounds is None:
            return None
        a, b, c, d = map(fraction, bounds)
        return rect((alpha * a + du, alpha * b + du, beta * c + dv, beta * d + dv))

    p["probe"] = moved(p["probe"])
    for key in ("coarse_cells", "fine_cells", "coarse_tiles", "fine_tiles"):
        for row in p[key]:
            row["bounds"] = moved(row["bounds"])
    old = matrix(problem["old_observations"])
    transform = [[k**3 * x for x in row] for row in basis_change(alpha, beta, du, dv)]
    inverse = [
        [x / k**3 for x in row]
        for row in basis_change(1 / alpha, 1 / beta, -du / alpha, -dv / beta)
    ]
    p["old_observations"] = encode(
        [r for t in range(len(old) // 4) for r in mm(transform, old[4 * t : 4 * t + 4])]
    )
    p["old_targets"] = encode([[k**4 * x for x in row] for row in matrix(problem["old_targets"])])

    def moved_map(rows):
        return [
            [
                k**4 * x
                for t in range(len(old) // 4)
                for x in mm([row[4 * t : 4 * t + 4]], inverse)[0]
            ]
            for row in rows
        ]

    a, linear = dense(problem)
    assert len(old) + 1 <= 64
    p["canonical"] = {
        "row_basis": list(range(len(old) + 1)),
        "decoder": encode([[k**4 * x, *row] for x, row in zip(a, moved_map(linear), strict=True)]),
    }
    p["geometric"] = encode(moved_map(matrix(problem["geometric"])))
    return p


def check_affine(base, moved, transform):
    alpha, beta, du, dv = map(F, transform)
    k = alpha * beta
    assert fraction(moved["geometry"]["volume"]) == k * fraction(base["geometry"]["volume"])
    assert base["counts"] == moved["counts"]
    assert base["geometry"]["parents"] == moved["geometry"]["parents"]
    for key in ("coarse_cells", "fine_cells"):
        assert [fraction(c["volume"]) for c in moved["geometry"][key]] == [
            k * fraction(c["volume"]) for c in base["geometry"][key]
        ]
    moment_map = basis_change(alpha, beta, du, dv, MOMENTS)
    for key in ("coarse_tiles", "fine_tiles"):
        for old, new in zip(base["geometry"][key], moved["geometry"][key], strict=True):
            assert list(map(fraction, new["moments"])) == [
                k * dot(row, list(map(fraction, old["moments"]))) for row in moment_map
            ]
            if key == "coarse_tiles":
                for a, b in zip(old["outgoing"], new["outgoing"], strict=True):
                    assert list(map(fraction, b["coefficients"])) == pullback(
                        list(map(fraction, a["coefficients"])), BASIS, alpha, beta, du, dv, k
                    )
    for old, new in zip(base["generators"], moved["generators"], strict=True):
        assert (old["tile"], old["i"], old["j"]) == (new["tile"], new["i"], new["j"])
        assert list(map(fraction, new["coefficients"])) == pullback(
            list(map(fraction, old["coefficients"])), POWERS, alpha, beta, du, dv, k**2
        )
    pm = [[k**3 * x for x in row] for row in basis_change(alpha, beta, du, dv)]
    old_o = matrix(base["matrices"]["observations"])
    assert matrix(moved["matrices"]["observations"]) == [
        r for t in range(len(old_o) // 4) for r in mm(pm, old_o[4 * t : 4 * t + 4])
    ]
    assert matrix(moved["matrices"]["targets"]) == [
        [k**4 * x for x in row] for row in matrix(base["matrices"]["targets"])
    ]
    for key, power in (("generator_integrals", 3), ("constant_targets", 4)):
        assert list(map(fraction, moved["matrices"][key])) == [
            k**power * fraction(x) for x in base["matrices"][key]
        ]
    old_constant = list(map(fraction, base["matrices"]["constant_observations"]))
    assert list(map(fraction, moved["matrices"]["constant_observations"])) == [
        dot(row, old_constant[4 * t : 4 * t + 4])
        for t in range(len(old_constant) // 4)
        for row in pm
    ]
    assert list(map(fraction, moved["geometry"]["response_scales"])) == [
        k**4 * fraction(x) for x in base["geometry"]["response_scales"]
    ]
    for old, new in zip(base["decoders"], moved["decoders"], strict=True):
        for key in (
            "normalized_residuals",
            "row_bounds",
            "failed_rows",
            "failed_generators",
            "exact",
            "nonzero_entries",
        ):
            assert old[key] == new[key]
        for key in ("predicted", "residuals"):
            assert matrix(new[key]) == [[k**4 * x for x in row] for row in matrix(old[key])]
        if old["witness"] is None:
            assert new["witness"] is None
        else:
            a, b = old["witness"], new["witness"]
            for key in ("generator", "separating_row", "weights", "normalized_residual"):
                assert a[key] == b[key]
            for key in ("truth", "predicted", "residual"):
                assert list(map(fraction, b[key])) == [k**4 * fraction(x) for x in a[key]]
            observed = list(map(fraction, a["observed"]))
            assert list(map(fraction, b["observed"])) == [
                dot(row, observed[4 * t : 4 * t + 4])
                for t in range(len(observed) // 4)
                for row in pm
            ]


@pytest.mark.parametrize(
    "factory",
    [
        unit_problem,
        lambda: unit_problem("signed"),
        lambda: unit_problem("portable"),
        signed_problem,
        knot_problem,
        lambda: unit_problem("portable", 8),
    ],
)
def test_generic_complete_independent_wire(engines, factory):
    p = factory()
    before = wire(p)
    want = expected(p)
    for engine in engines:
        assert wire(engine.build_family(p)) == wire(want)
        assert wire(p) == before


def test_all_nine_unit_beta_anchors_and_boundary_extensions(engines):
    for engine in engines:
        result = engine.build_family(unit_problem())
        m = result["matrices"]
        for g, (i, j) in enumerate(POWERS):
            assert [row[g] for row in m["observations"]] == list(
                map(fw, (F(1, 72), F(i + 1, 288), F(j + 1, 288), F((i + 1) * (j + 1), 1152)))
            )
            assert m["targets"][0][g] == fw(F((3 - i) * (3 - j), 2304))
        assert m["generator_integrals"] == [fw(F(1, 72))] * 9
        assert m["constant_observations"] == list(map(fw, (F(1, 8), F(1, 16), F(1, 16), F(1, 32))))
        assert m["constant_targets"] == [fw(F(1, 64))]
        assert sum(map(fraction, m["generator_integrals"]), F()) == F(1, 8)
        # The supported polynomial extension is nonzero at the boundary, even
        # though the source indicator itself is zero there. Endpoint quadrature
        # must use this one-sided extension, not the indicator value.
        assert result["generators"][0]["coefficients"][0] == fw(F(1, 4))
        for u, v in product((F(1, 7), F(1, 3), F(5, 6)), repeat=2):
            values = [
                sum(
                    (
                        fraction(c) * u**p * v**q
                        for c, (p, q) in zip(g["coefficients"], POWERS, strict=True)
                    ),
                    F(),
                )
                for g in result["generators"]
            ]
            assert all(x >= 0 for x in values) and sum(values, F()) == F(1, 4)
            assert sum(values, F()) / 9 == F(1, 36)


def test_signed_residuals_all_attainers_and_generator_first_witness(engines):
    for engine in engines:
        result = engine.build_family(unit_problem("signed"))
        c, g = result["decoders"]
        assert c["residuals"] == [[fw(F(i - j, 288)) for i, j in POWERS]]
        assert c["normalized_residuals"] == [[fw(F(i - j, 18)) for i, j in POWERS]]
        assert c["row_bounds"] == [
            {
                "minimum": fw(-F(1, 9)),
                "minimum_generators": [2],
                "maximum": fw(F(1, 9)),
                "maximum_generators": [6],
                "max_abs": fw(F(1, 9)),
                "max_abs_generators": [2, 6],
            }
        ]
        assert c["witness"]["generator"] == 1 and c["witness"]["separating_row"] == 0
        assert c["witness"]["weights"] == [fw(int(i == 1)) for i in range(9)]
        assert c["witness"]["residual"] == [fw(-F(1, 288))]
        assert g["exact"] and g["witness"] is None
        for key in ("minimum_generators", "maximum_generators", "max_abs_generators"):
            assert g["row_bounds"][0][key] == list(range(9))


def test_nonzero_intercept_and_source_sum_not_unnormalized_mixture(engines):
    for engine in engines:
        result = engine.build_family(unit_problem())
        d = result["decoders"][0]
        assert d["intercept"] == [fw(F(1, 9216))]
        assert d["predicted"] == [[fw(F(1, 9216))] * 9]
        assert d["witness"]["generator"] == 0
        assert d["witness"]["residual"] == [fw(-F(35, 9216))]
        prediction_sum = sum(map(fraction, d["predicted"][0]), F())
        applying_sum = engine.apply(
            d["intercept"], d["matrix"], result["matrices"]["constant_observations"]
        )
        assert prediction_sum == F(1, 1024)
        assert applying_sum == [fw(F(1, 9216))]
        assert prediction_sum != fraction(applying_sum[0])


def test_raw_empty_response_failures_remain_visible(engines):
    for engine in engines:
        result = engine.build_family(signed_problem())
        d = result["decoders"][0]
        assert result["geometry"]["response_scales"][1] == fw(0)
        assert result["geometry"]["parents"][2] == {"event": 9, "parent": None}
        assert d["failed_rows"] == [1] and not d["exact"]
        assert d["normalized_residuals"][1] is None and d["row_bounds"][1] is None
        assert any(map(fraction, d["predicted"][1]))
        assert d["witness"]["generator"] == 0 and d["witness"]["separating_row"] == 1
        assert fraction(d["witness"]["residual"][1]) > 0
        assert d["witness"]["normalized_residual"][1] is None
        assert (
            engine.apply(d["intercept"], d["matrix"], d["witness"]["observed"])
            == d["witness"]["predicted"]
        )


def test_inactive_axis_knots_admitted_but_active_knots_rejected(engines):
    p = knot_problem()
    for engine in engines:
        got = engine.build_family(p)
        assert wire(got) == wire(expected(p))
        assert got["geometry"]["coarse_tiles"][2]["outgoing"][0]["coefficients"] == [fw(0)] * 4
        with pytest.raises(ValueError):
            engine.build_family(knot_problem(True))


def test_geometric_authentication_goes_beyond_old_columns(engines):
    p = unit_problem("signed")
    p["geometric"] = [copy.deepcopy(p["canonical"]["decoder"][0][1:])]
    assert mm(matrix(p["geometric"]), matrix(p["old_observations"])) == matrix(p["old_targets"])
    for engine in engines:
        with pytest.raises(ValueError):
            engine.build_family(p)


@pytest.mark.parametrize("fine_tiles", [8, 64])
def test_new_generator_count_does_not_inherit_old_sixty_four_cap(engines, fine_tiles):
    problem = unit_problem("portable", fine_tiles)
    want = expected(problem)
    for engine in engines:
        result = engine.build_family(problem)
        assert wire(result) == wire(want)
        assert result["counts"]["old_generators"] == 1
        assert result["counts"]["new_generators"] == 9 * fine_tiles
        assert len(result["matrices"]["observations"][0]) == 9 * fine_tiles
        assert result["decoders"][0]["row_bounds"][0]["max_abs_generators"] == list(
            range(9 * fine_tiles)
        )


@pytest.mark.parametrize("factory", [unit_problem, lambda: unit_problem("signed"), signed_problem])
@pytest.mark.parametrize("transform", [(F(2), F(1, 2), F(-3), F(5)), (F(3), F(2), F(-2), F(1))])
def test_complete_affine_transport_same_maps_and_payloads(engines, factory, transform):
    p = factory()
    moved = affine_problem(p, *transform)
    want = expected(moved)
    check_affine(expected(p), want, transform)
    assert moved["canonical"]["row_basis"] == list(range(len(p["old_observations"]) + 1))
    for engine in engines:
        assert wire(engine.build_family(moved)) == wire(want)


def test_exact_convex_mixture_residuals_and_extrema(engines):
    for engine in engines:
        result = engine.build_family(unit_problem("signed"))
        for d in result["decoders"]:
            for weights in ([F(1, 9)] * 9, [F(1, 2), F(1, 2), *[F()] * 7]):
                observed = list(
                    map(
                        fw,
                        [
                            dot(list(map(fraction, row)), weights)
                            for row in result["matrices"]["observations"]
                        ],
                    )
                )
                truth = dot(list(map(fraction, result["matrices"]["targets"][0])), weights)
                error = fraction(engine.apply(d["intercept"], d["matrix"], observed)[0]) - truth
                assert error == dot(list(map(fraction, d["residuals"][0])), weights)
                normal = error / fraction(result["geometry"]["response_scales"][0])
                bounds = d["row_bounds"][0]
                assert fraction(bounds["minimum"]) <= normal <= fraction(bounds["maximum"])
            for g in d["row_bounds"][0]["max_abs_generators"]:
                assert abs(fraction(d["normalized_residuals"][0][g])) == fraction(
                    d["row_bounds"][0]["max_abs"]
                )


def test_restricted_apply_and_build_need_no_hidden_files(engines, monkeypatch):
    p = unit_problem("signed")
    want = expected(p)

    def forbidden(*args, **kwargs):
        raise RuntimeError("off-contract hidden access")

    for engine in engines:
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            assert wire(engine.build_family(p)) == wire(want)
            patch.setattr(engine, "build_family", forbidden)
            assert engine.apply(
                [fw(1)], [[fw(2), fw(-1), fw(0), fw(3)]], list(map(fw, (2, 5, 8, -1)))
            ) == [fw(-3)]


def test_native_sharing_and_detached_outputs(engines):
    p = unit_problem()
    for key in ("coarse_cells", "fine_cells", "coarse_tiles", "fine_tiles"):
        p[key][0]["bounds"] = p["probe"]
    before = wire(p)
    for engine in engines:
        got = engine.build_family(p)
        want = wire(got)
        assert wire(p) == before
        got["problem"]["probe"][0][0] = 17
        got["generators"][0]["coefficients"][0][0] = 19
        assert wire(p) == before and wire(engine.build_family(p)) == want
        a, l, x = [fw(1)], [[fw(0)] * 4], [fw(2)] * 4
        snapshots = [wire(v) for v in (a, l, x)]
        engine.apply(a, l, x)[0][0] = 99
        assert [wire(v) for v in (a, l, x)] == snapshots


def test_large_intermediate_cancellation_and_retained_overflow(engines):
    good = affine_problem(unit_problem("signed"), 1, 1, F(1 << 1100), 0)
    want = expected(good)
    for engine in engines:
        assert wire(engine.build_family(good)) == wire(want)
        with pytest.raises(ValueError):
            engine.build_family(affine_problem(unit_problem("signed"), 1, 1, F(1 << 1400), 0))
        d = 1 << 4095
        assert engine.apply(
            [fw(0)], [[fw(d), fw(-d), fw(0), fw(0)]], list(map(fw, (2, 2, 0, 0)))
        ) == [fw(0)]
        with pytest.raises(ValueError):
            engine.apply([fw(0)], [[fw(d), fw(0), fw(0), fw(0)]], list(map(fw, (2, 0, 0, 0))))


def test_apply_maximum_raw_dimensions(engines):
    for engine in engines:
        assert engine.apply([fw(1)] * 64, [[fw(0)] * 256] * 64, [fw(7)] * 256) == [fw(1)] * 64


def test_late_matrix_shape_rejected_before_rectangle_arithmetic(engines, monkeypatch):
    bad = unit_problem()
    bad["geometric"] = [[]]
    for engine in engines:
        calls = []

        def forbidden(*args, _calls=calls, **kwargs):
            _calls.append(True)
            raise RuntimeError("geometry began before complete shape admission")

        with monkeypatch.context() as patch:
            patch.setattr(engine, "_rectangle", forbidden)
            with pytest.raises(ValueError):
                engine.build_family(bad)
        assert calls == []


class ListSubclass(list):
    pass


class DictSubclass(dict):
    pass


class IntSubclass(int):
    pass


def invalid_families():
    p = unit_problem()
    s = signed_problem()
    split = unit_problem("portable", 2)
    problems = [
        None,
        [],
        DictSubclass(p),
        {**p, "extra": 0},
        {k: v for k, v in p.items() if k != "geometric"},
        {**p, "family": ""},
        {**p, "family": False},
        replaced(p, ("probe", 0), [0.0, 1]),
        replaced(p, ("probe", 0), [False, 1]),
        replaced(p, ("probe", 0), [IntSubclass(0), 1]),
        replaced(p, ("probe", 1), [2, 2]),
        replaced(p, ("probe", 0), [0, -1]),
        replaced(p, ("probe", 1), [1 << 4096, 1]),
        replaced(p, ("probe",), rect((0, 0, 0, 1))),
        replaced(p, ("coarse_cells",), []),
        replaced(p, ("fine_cells",), []),
        replaced(p, ("coarse_cells",), p["coarse_cells"] * 9),
        replaced(p, ("fine_cells",), p["fine_cells"] * 9),
        replaced(p, ("coarse_cells",), ListSubclass(p["coarse_cells"])),
        replaced(p, ("fine_cells", 0, "event"), True),
        replaced(s, ("coarse_cells",), s["coarse_cells"][::-1]),
        replaced(s, ("fine_cells",), s["fine_cells"][::-1]),
        replaced(s, ("fine_cells", 1, "event"), -7),
        replaced(p, ("coarse_cells", 0, "bounds"), None),
        replaced(p, ("fine_cells", 0, "bounds"), None),
        replaced(p, ("fine_cells", 0, "bounds"), rect((-1, 1, 0, 1))),
        replaced(p, ("fine_cells", 0, "bounds"), rect((0, F(1, 2), 0, 1))),
        replaced(s, ("fine_cells", 0, "bounds"), rect((-2, 0, 1, 2))),
        replaced(p, ("coarse_tiles",), []),
        replaced(p, ("fine_tiles",), []),
        replaced(p, ("coarse_tiles",), p["coarse_tiles"] * 65),
        replaced(p, ("fine_tiles",), p["fine_tiles"] * 65),
        replaced(p, ("coarse_tiles", 0, "event"), 7),
        replaced(p, ("fine_tiles", 0, "event"), 7),
        replaced(p, ("fine_tiles", 0, "coarse_tile"), True),
        replaced(p, ("fine_tiles", 0, "coarse_tile"), 1),
        replaced(s, ("fine_tiles", 0, "coarse_tile"), 1),
        replaced(p, ("fine_tiles", 0, "bounds"), None),
        replaced(p, ("coarse_tiles", 0, "bounds"), rect((0, 0, 0, 1))),
        replaced(p, ("fine_tiles", 0, "bounds"), rect((-1, 1, 0, 1))),
        replaced(split, ("fine_tiles",), split["fine_tiles"][::-1]),
        replaced(split, ("fine_tiles", 0, "bounds"), rect((0, F(2, 3), 0, 1))),
        replaced(split, ("fine_tiles", 0, "bounds"), rect((0, F(1, 3), 0, 1))),
        replaced(p, ("old_observations",), []),
        replaced(p, ("old_observations", 3), []),
        replaced(p, ("old_observations",), [[fw(0)] * 65] * 4),
        replaced(p, ("old_observations", 3, 0), F(1, 512)),
        replaced(p, ("old_targets",), []),
        replaced(p, ("old_targets", 0), [fw(0), fw(0)]),
        replaced(p, ("old_targets", 0, 0), fw(0)),
        replaced(s, ("old_targets", 1, 1), fw(1)),
        replaced(p, ("canonical",), {**p["canonical"], "extra": 0}),
        replaced(p, ("canonical", "row_basis"), []),
        replaced(p, ("canonical", "row_basis"), [1]),
        replaced(p, ("canonical", "row_basis"), [0, 0]),
        replaced(p, ("canonical", "row_basis"), [0, 5]),
        replaced(p, ("canonical", "row_basis"), [False]),
        replaced(p, ("canonical", "row_basis"), list(range(65))),
        replaced(p, ("canonical", "decoder"), []),
        replaced(p, ("canonical", "decoder", 0, 0), fw(1)),
        replaced(p, ("geometric",), []),
        replaced(p, ("geometric", 0), [fw(0)] * 3),
        replaced(p, ("geometric", 0, 0), fw(0)),
        knot_problem(True),
    ]
    late = copy.deepcopy(p)
    late["old_observations"] = [row * 2 for row in late["old_observations"]]
    late["old_targets"] = [row * 2 for row in late["old_targets"]]
    late["old_observations"][3][1] = fw(0)
    problems.append(late)
    return problems


def invalid_applications():
    a, l, x = [fw(1)], [[fw(1), fw(-1), fw(0), fw(2)]], [fw(1)] * 4
    return [
        (None, l, x),
        ([], [], x),
        (a * 2, l, x),
        (a, l * 2, x),
        (a, l, []),
        (a, l, x[:-1]),
        (a, l, x * 65),
        (a * 65, l * 65, x),
        (ListSubclass(a), l, x),
        (a, ListSubclass(l), x),
        (a, l, tuple(x)),
        ([None], l, x),
        (a, [None], x),
        (a, [l[0][:-1]], x),
        (a, [tuple(l[0])], x),
        ([True], l, x),
        ([[1, False]], l, x),
        (a, l, [0.0, *x[1:]]),
        (a, l, [[2, 2], *x[1:]]),
        (a, l, [[1, 0], *x[1:]]),
        (a, l, [[1 << 4096, 1], *x[1:]]),
        (a, l, [[IntSubclass(1), 1], *x[1:]]),
    ]


@pytest.mark.parametrize("route", [0, 1])
def test_strict_native_geometry_identity_and_dimension_guards(engines, route):
    engine = engines[route]
    for p in invalid_families():
        with pytest.raises(ValueError):
            engine.build_family(p)
    for args in invalid_applications():
        with pytest.raises(ValueError):
            engine.apply(*args)
    assert len(invalid_families()) == 65 and len(invalid_applications()) == 22


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guards_in_isolated_normal_and_optimized_python(tmp_path, optimized):
    program = r"""
import importlib.util,sys
from pathlib import Path
here=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("aq_guard_fixture",here/"test_qr05aq.py")
test=importlib.util.module_from_spec(spec)
spec.loader.exec_module(test)
count=0
def reject(fn,*args):
    global count
    try: fn(*args)
    except ValueError: count+=1
    else: raise RuntimeError("ValueError admission guard missing")
for filename in ("kernel.py","reference.py"):
    spec=importlib.util.spec_from_file_location("aq_guard_"+filename[:-3],here/filename)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for p in test.invalid_families(): reject(module.build_family,p)
    for args in test.invalid_applications(): reject(module.apply,*args)
    d=1<<4095
    got=module.apply([test.fw(0)],[[test.fw(d),test.fw(-d),test.fw(0),test.fw(0)]],list(map(test.fw,(2,2,0,0))))
    if got!=[test.fw(0)]: raise RuntimeError("cancellation failed")
    reject(module.apply,[test.fw(0)],[[test.fw(d),test.fw(0),test.fw(0),test.fw(0)]],list(map(test.fw,(2,0,0,0))))
    got=module.build_family(test.unit_problem("signed"))
    if got["decoders"][0]["residuals"]!=[[test.fw(test.F(i-j,288)) for i,j in test.POWERS]]:
        raise RuntimeError("signed analytic hand changed")
if count!=176: raise RuntimeError("guard inventory changed: "+str(count))
print(count)
"""
    args = [sys.executable, "-I"] + (["-O"] if optimized else [])
    args += ["-X", f"pycache_prefix={tmp_path / 'cache'}", "-c", program, str(HERE)]
    got = subprocess.run(
        args,
        cwd=tmp_path,
        env={**os.environ, "PYTHONHASHSEED": "0"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert got.stdout.strip() == "176"


def family_mutations(good):
    scalar_paths = [
        ("problem", "old_observations", 0, 0),
        ("problem", "old_targets", 0, 0),
        ("problem", "canonical", "decoder", 0, 0),
        ("problem", "geometric", 0, 0),
        ("geometry", "volume"),
        ("geometry", "response_scales", 0),
        ("geometry", "coarse_tiles", 0, "moments", 0),
        ("geometry", "fine_tiles", 0, "moments", 15),
        ("geometry", "coarse_tiles", 0, "outgoing", 0, "coefficients", 0),
        ("generators", 0, "coefficients", 0),
        ("matrices", "observations", 0, 0),
        ("matrices", "targets", 0, 0),
        ("matrices", "generator_integrals", 0),
        ("matrices", "constant_observations", 0),
        ("matrices", "constant_targets", 0),
        ("decoders", 0, "intercept", 0),
        ("decoders", 0, "matrix", 0, 0),
        ("decoders", 0, "predicted", 0, 0),
        ("decoders", 0, "residuals", 0, 0),
        ("decoders", 0, "normalized_residuals", 0, 0),
        ("decoders", 0, "row_bounds", 0, "minimum"),
        ("decoders", 0, "row_bounds", 0, "maximum"),
        ("decoders", 0, "row_bounds", 0, "max_abs"),
    ]
    mutations = []
    for path in scalar_paths:
        value = good
        for part in path:
            value = value[part]
        mutations.append(replaced(good, path, fw(fraction(value) + 1)))
    mutations += [
        replaced(good, ("geometry", "parents", 0, "parent"), None),
        replaced(good, ("geometry", "fine_tiles", 0, "coarse_tile"), 99),
        replaced(good, ("generators", 0, "i"), 9),
        replaced(good, ("matrices", "observation_rows", 0, "basis"), 3),
        replaced(good, ("decoders", 0, "exact"), not good["decoders"][0]["exact"]),
        replaced(good, ("decoders", 0, "failed_rows"), [good["counts"]["response_rows"]]),
        replaced(good, ("decoders", 0, "failed_generators"), [good["counts"]["new_generators"]]),
        replaced(good, ("decoders", 0, "row_bounds", 0, "minimum_generators"), []),
        replaced(good, ("decoders", 0, "row_bounds", 0, "maximum_generators"), []),
        replaced(good, ("decoders", 0, "row_bounds", 0, "max_abs_generators"), []),
        replaced(good, ("counts", "witness_entries"), good["counts"]["witness_entries"] + 1),
        replaced(good, ("checks", "geometric_portability"), False),
    ]
    witness = good["decoders"][0]["witness"]
    if witness is None:
        mutations.append(replaced(good, ("decoders", 0, "witness"), {"generator": 0}))
    else:
        for key in ("generator", "separating_row"):
            mutations.append(replaced(good, ("decoders", 0, "witness", key), witness[key] + 1))
        for key in ("weights", "observed", "truth", "predicted", "residual", "normalized_residual"):
            index = next(i for i, x in enumerate(witness[key]) if x is not None)
            mutations.append(
                replaced(
                    good,
                    ("decoders", 0, "witness", key, index),
                    fw(fraction(witness[key][index]) + 1),
                )
            )
    assert all(wire(bad) != wire(good) for bad in mutations)
    return mutations


def test_nonvacuous_full_family_and_null_raw_witness_corruptions(runner):
    good = expected(unit_problem("signed"))
    mutations = family_mutations(good)
    assert len(mutations) == 43
    for bad in mutations:
        with pytest.raises(ValueError):
            runner.verify_suite(bad, good)
    empty = expected(signed_problem())
    mutations = [
        replaced(empty, ("decoders", 0, "residuals", 1), [fw(0)] * 36),
        replaced(empty, ("decoders", 0, "normalized_residuals", 1), [fw(0)] * 36),
        replaced(empty, ("decoders", 0, "row_bounds", 1), empty["decoders"][0]["row_bounds"][0]),
        replaced(empty, ("decoders", 0, "witness", "residual", 1), fw(0)),
        replaced(empty, ("decoders", 0, "witness", "normalized_residual", 1), fw(0)),
        replaced(empty, ("geometry", "response_scales", 1), None),
    ]
    for bad in mutations:
        assert wire(bad) != wire(empty)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, empty)


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


def expected_suite(families):
    return {
        "families": copy.deepcopy(families),
        "prior_bridges": {
            "AP_selected_families": list(FAMILIES),
            "AP_frozen_inputs_equal": True,
            "AO_selected_fine_geometry_equal": True,
            "AO_selected_coarse_moments_equal": True,
            "AO_selected_fine_moments_equal": True,
            "old_maps_consumed": True,
            "old_response_identities_rechecked": True,
            "other_historical_mathematics_replayed": False,
            "older_executors_run": False,
        },
        "payload_sizes": [
            {
                "family": f["problem"]["family"],
                "input_bytes": len(wire(f["problem"])),
                "geometry_bytes": len(wire(f["geometry"])),
                "generator_bytes": len(wire(f["generators"])),
                "measurement_bytes": len(
                    wire(
                        {
                            "rows": f["matrices"]["observation_rows"],
                            "matrix": f["matrices"]["observations"],
                        }
                    )
                ),
                "target_bytes": len(
                    wire(
                        {"rows": f["matrices"]["response_rows"], "matrix": f["matrices"]["targets"]}
                    )
                ),
                "decoder_bytes": len(wire(f["decoders"])),
                "native_family_bytes": len(wire(f)),
            }
            for f in families
        ],
        "totals": {
            "families": len(families),
            **{key: sum(f["counts"][key] for f in families) for key in families[0]["counts"]},
        },
        "scope": dict.fromkeys(SCOPE, False),
    }


def test_generic_tuple_history_assembly_and_cached_routes(runner, monkeypatch):
    # This is a synthetic tuple-boundary/routing check, not historical authentication.
    problems = [unit_problem("signed"), unit_problem("portable")]
    for p, name in zip(problems, FAMILIES, strict=True):
        p["family"] = name
    families = [expected(p) for p in problems]
    previous = ([{"synthetic": "AP"}], [{"synthetic": "AO"}])
    want = expected_suite(families)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    monkeypatch.setattr(
        runner, "historical_bridges", lambda f, p: copy.deepcopy(want["prior_bridges"])
    )
    assert wire(runner.assemble_suite(families, previous)) == wire(want)
    calls = []

    def loader(name):
        def build(p):
            index = FAMILIES.index(p["family"])
            assert wire(p) == wire(problems[index])
            calls.append((name, p["family"]))
            return copy.deepcopy(families[index])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    for route in ("compare", "primary", "reference"):
        calls.clear()
        assert wire(runner.run_suite(route)) == wire(want)
        names = ("primary", "reference") if route == "compare" else (route,)
        assert calls == [(name, family) for family in FAMILIES for name in names]


def projected_inputs(previous):
    ap, ao = previous
    assert [f["problem"]["family"] for f in ap] == list(FAMILIES)
    out = []
    for a, b in zip(ap, ao, strict=True):
        p, g = a["problem"], b["geometry"]
        out.append(
            copy.deepcopy(
                {
                    "family": p["family"],
                    "probe": p["probe"],
                    "coarse_cells": p["cells"],
                    "fine_cells": [
                        {"event": c["event"], "bounds": c["bounds"]} for c in g["fine_cells"]
                    ],
                    "coarse_tiles": p["tiles"],
                    "fine_tiles": [
                        {k: t[k] for k in ("event", "bounds", "coarse_tile")}
                        for t in g["fine_tiles"]
                    ],
                    "old_observations": p["observations"],
                    "old_targets": p["targets"],
                    "canonical": p["canonical"],
                    "geometric": p["geometric"],
                }
            )
        )
    return out


@pytest.fixture(scope="session")
def fixed_bundle(runner, engines):
    """Lazy; never executes in collection or when -k 'not fixed' is selected."""
    problems, previous = runner.load_inputs()
    assert type(previous) is tuple and len(previous) == 2
    own = projected_inputs(previous)
    assert wire(problems) == wire(own)
    wants = [expected(p) for p in own]
    actual = []
    for engine in engines:
        result = []
        for p in problems:
            supplied = copy.deepcopy(p)
            result.append(engine.build_family(supplied))
            assert wire(supplied) == wire(p)
        actual.append(result)
    return problems, previous, wants, actual


@pytest.mark.parametrize("family_index", [0, 1])
def test_fixed_complete_two_engine_true_integrals_and_witnesses(
    fixed_bundle, engines, family_index
):
    _, _, wants, actual = fixed_bundle
    for i, engine in enumerate(engines):
        f = actual[i][family_index]
        assert wire(f) == wire(wants[family_index])
        m = f["matrices"]
        n = len(f["generators"])
        weights = [F(1, n)] * n
        observation = list(
            map(fw, [dot(list(map(fraction, row)), weights) for row in m["observations"]])
        )
        for d in f["decoders"]:
            assert engine.apply(d["intercept"], d["matrix"], observation) == [
                fw(dot(list(map(fraction, row)), weights)) for row in d["predicted"]
            ]
            if d["witness"] is not None:
                assert (
                    engine.apply(d["intercept"], d["matrix"], d["witness"]["observed"])
                    == d["witness"]["predicted"]
                )
    # No fixed outcome, nonzero count or first counterexample is prescribed.


def test_fixed_complete_suite_moments_payload_and_historical_bridge(fixed_bundle, runner):
    _, previous, wants, actual = fixed_bundle
    want = expected_suite(wants)
    for route in actual:
        assert wire(runner.assemble_suite(route, previous)) == wire(want)
        assert runner.historical_bridges(route, previous) == want["prior_bridges"]
    for f, old in zip(wants, previous[1], strict=True):
        for key in ("coarse_tiles", "fine_tiles"):
            assert [r["moments"] for r in f["geometry"][key]] == [
                r["moments"] for r in old["geometry"][key]
            ]
    assert set(runner.COUNT_FIELDS) == set(wants[0]["counts"])
    assert set(runner.CHECK_FIELDS) == set(CHECKS) and set(runner.SCOPE) == set(SCOPE)


@pytest.mark.parametrize("route", ["compare", "primary", "reference"])
def test_fixed_cached_orchestration_routes(fixed_bundle, runner, monkeypatch, route):
    problems, previous, wants, actual = fixed_bundle
    calls = []

    def loader(name):
        index = {"primary": 0, "reference": 1}[name]

        def build(p):
            j = FAMILIES.index(p["family"])
            assert wire(p) == wire(problems[j])
            calls.append((name, p["family"]))
            return copy.deepcopy(actual[index][j])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    assert wire(runner.run_suite(route)) == wire(expected_suite(wants))
    names = ("primary", "reference") if route == "compare" else (route,)
    assert calls == [(name, family) for family in FAMILIES for name in names]


def test_fixed_nonvacuous_full_result_and_suite_corruptions(fixed_bundle, runner):
    _, _, wants, _ = fixed_bundle
    for good in wants:
        for bad in family_mutations(good):
            with pytest.raises(ValueError):
                runner.verify_suite(bad, good)
    suite = expected_suite(wants)
    bads = [
        replaced(suite, ("families",), suite["families"][::-1]),
        replaced(suite, ("prior_bridges", "AP_frozen_inputs_equal"), False),
        replaced(suite, ("prior_bridges", "AO_selected_fine_moments_equal"), False),
        replaced(suite, ("prior_bridges", "other_historical_mathematics_replayed"), True),
        replaced(
            suite,
            ("payload_sizes", 0, "generator_bytes"),
            suite["payload_sizes"][0]["generator_bytes"] + 1,
        ),
        replaced(
            suite,
            ("payload_sizes", 0, "measurement_bytes"),
            suite["payload_sizes"][0]["measurement_bytes"] + 1,
        ),
        replaced(
            suite,
            ("totals", "bound_attainer_indices"),
            suite["totals"]["bound_attainer_indices"] + 1,
        ),
        replaced(suite, ("scope", "decoder_refitted"), True),
    ]
    for bad in bads:
        assert wire(bad) != wire(suite)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, suite)


def test_fixed_selected_input_and_postbuild_moment_mutations(fixed_bundle, runner):
    problems, previous, wants, _ = fixed_bundle
    ap, ao = previous
    paths = [
        ("probe", 0),
        ("cells", 0, "bounds", 0),
        ("tiles", 0, "bounds", 0),
        ("observations", 0, 0),
        ("targets", 0, 0),
        ("canonical", "decoder", 0, 0),
        ("geometric", 0, 0),
    ]
    bad_histories = []
    for path in paths:
        full = (0, "problem", *path)
        value = ap
        for part in full:
            value = value[part]
        bad_histories.append((replaced(ap, full, fw(fraction(value) + 1)), ao))
    for key in ("fine_cells", "fine_tiles"):
        full = (0, "geometry", key, 0, "bounds", 0)
        value = ao
        for part in full:
            value = value[part]
        bad_histories.append((ap, replaced(ao, full, fw(fraction(value) + 1))))
    bad_histories.append((ap, replaced(ao, (0, "geometry", "fine_tiles", 0, "coarse_tile"), 99)))
    for key in ("coarse_tiles", "fine_tiles"):
        full = (0, "geometry", key, 0, "moments", 15)
        value = ao
        for part in full:
            value = value[part]
        changed = replaced(ao, full, fw(fraction(value) + 1))
        # Old moments do not enter the input; rejection occurs at the postbuild bridge.
        assert wire(runner.project_inputs(ap, changed)[0]) == wire(problems)
        bad_histories.append((ap, changed))
    assert len(bad_histories) == 12
    for bad in bad_histories:
        assert wire(list(bad)) != wire(list(previous))
        with pytest.raises(ValueError):
            runner.historical_bridges(wants, bad)
    # These helpers do not replay unselected history. Whole artifacts remain pinned.
    changed = copy.deepcopy(ap)
    changed[0]["decoders"][0]["row_gains"][0] = fw(
        fraction(changed[0]["decoders"][0]["row_gains"][0]) + 1
    )
    assert wire(changed) != wire(ap)
    assert wire(runner.project_inputs(changed, ao)[0]) == wire(problems)


def test_fixed_complete_identity_inventory(runner):
    ids = runner.identities()
    assert set(ids) == {"source_ledger", "prior_artifacts", "ancestor_sources"}
    assert set(ids["source_ledger"]) == {
        "README.md",
        "kernel.py",
        "reference.py",
        "study.py",
        "test_qr05aq.py",
    }
    assert len(ids["prior_artifacts"]) == 47 and len(ids["ancestor_sources"]) == 54
    assert sum(map(len, ids.values())) == 106
    assert runner.AP_ID == {
        "bytes": 361276,
        "sha256": "823d9f5a5511853fe3dbff800f1a6561db985021002c24ec2beb0c55199ba048",
    }
    assert runner.AO_ID == {
        "bytes": 451698,
        "sha256": "55938309ba8ea8c205a9c6e127ce324e485b5e0bf5ff02bc5f513503e2f5fbf1",
    }
