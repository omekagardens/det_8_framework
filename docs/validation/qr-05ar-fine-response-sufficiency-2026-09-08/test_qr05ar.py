"""Independent beta-integral and Gram-Schmidt fine-response sufficiency checks.

Only test names containing fixed consume authenticated AQ cases. Collection and generic
hands use explicit synthetic data, never fixed fixture calculations.
"""

from __future__ import annotations

import builtins
import copy
import hashlib
import importlib.util
import json
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
        load("_qr05ar_test_primary", "kernel.py"),
        load("_qr05ar_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05ar_test_runner", "study.py")


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
    "geometry_partitions",
    "bernstein_partition",
    "generator_integrals",
    "moment_additivity",
    "observation_additivity",
    "response_additivity",
    "geometric_coarse_identity",
    "geometric_fine_identity",
    "coarse_certificate_valid",
    "collision_valid",
    "repair_collision_valid",
    "constant_field_sums",
)
SCOPE = (
    "source_dictionary_changed",
    "old_convex_hull_inclusion_proved",
    "full_field_recovery_tested",
    "repair_minimality_proved",
    "fine_measurements_recovered_from_coarse",
    "physical_sources_established",
    "empirical_noise_calibrated",
    "unknown_geometry_reconstructed",
    "quantum_channel_constructed",
    "gravity_derived",
    "ret_integration_tested",
    "lean_verification_performed",
    "generic_production_API_hardened",
    "fixed_affine_families_run",
    "older_executors_run",
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


class OrthogonalSpan:
    """Exact rational Gram-Schmidt; no Gaussian row operations or square roots."""

    def __init__(self, vectors):
        self.indices = []
        self.orthogonal = []
        self.combinations = []
        self.norms = []
        for index, vector in enumerate(vectors):
            residual, projection = self.decompose(vector)
            if any(residual):
                self.indices.append(index)
                self.orthogonal.append(residual)
                self.norms.append(dot(residual, residual))
                self.combinations.append(
                    {index: F(1), **{i: -x for i, x in projection.items() if x}}
                )

    def decompose(self, vector):
        residual = list(vector)
        combination = {}
        for orthogonal, norm, representation in zip(
            self.orthogonal, self.norms, self.combinations, strict=True
        ):
            factor = dot(vector, orthogonal) / norm
            if factor:
                residual = [a - factor * b for a, b in zip(residual, orthogonal, strict=True)]
                for index, value in representation.items():
                    combination[index] = combination.get(index, F()) + factor * value
        return residual, combination


def gram_certificate(observations, targets):
    n = len(targets[0])
    augmented = [[F(1)] * n, *observations]
    rows = OrthogonalSpan(augmented)
    columns = [list(c) for c in zip(*augmented, strict=True)]
    cols = OrthogonalSpan(columns)
    assert len(rows.indices) == len(cols.indices)
    free = [j for j in range(n) if j not in cols.indices]
    decoders = []
    for target in targets:
        residual, coefficients = rows.decompose(target)
        decoders.append(None if any(residual) else [coefficients.get(j, F()) for j in rows.indices])
    recovered = [j for j, d in enumerate(decoders) if d is not None]
    failed = [j for j, d in enumerate(decoders) if d is None]
    basis = [augmented[j] for j in rows.indices]
    for d, target in zip(decoders, targets, strict=True):
        if d is not None:
            assert [dot(d, col) for col in zip(*basis, strict=True)] == target
    collision = None
    if failed:
        for j in free:
            remainder, coefficients = cols.decompose(columns[j])
            assert not any(remainder)
            w = [F()] * n
            w[j] = F(1)
            for pivot in cols.indices:
                w[pivot] = -coefficients.get(pivot, F())
            assert not any(dot(row, w) for row in augmented)
            difference = [dot(row, w) for row in targets]
            if any(difference):
                r = next(r for r, x in enumerate(difference) if x)
                mass = sum((x for x in w if x > 0), F())
                assert mass > 0 and mass == -sum((x for x in w if x < 0), F())
                plus = [max(F(), x) / mass for x in w]
                minus = [max(F(), -x) / mass for x in w]
                assert sum(plus, F()) == sum(minus, F()) == 1
                op, om = (
                    [dot(row, plus) for row in observations],
                    [dot(row, minus) for row in observations],
                )
                tp, tm = [dot(row, plus) for row in targets], [dot(row, minus) for row in targets]
                assert op == om
                collision = {
                    "free_column": j,
                    "separating_row": r,
                    "null_vector": w,
                    "positive_mass": mass,
                    "weights_plus": plus,
                    "weights_minus": minus,
                    "observed_plus": op,
                    "observed_minus": om,
                    "truth_plus": tp,
                    "truth_minus": tm,
                    "truth_difference": [a - b for a, b in zip(tp, tm, strict=True)],
                }
                assert collision["truth_difference"] == [x / mass for x in difference]
                break
        assert collision is not None
    return {
        "observation_rank": len(rows.indices),
        "target_rank": len(OrthogonalSpan(targets).indices),
        "joint_rank": len(OrthogonalSpan([*augmented, *targets]).indices),
        "row_basis": rows.indices,
        "pivot_columns": cols.indices,
        "free_columns": free,
        "recoverable": not failed,
        "decoder": copy.deepcopy(decoders) if not failed else None,
        "recoverable_rows": recovered,
        "failed_rows": failed,
        "row_decoders": decoders,
        "collision": collision,
    }


def expected_certificate(observations, targets):
    return encode(gram_certificate(matrix(observations), matrix(targets)))


def overlay(problem):
    positive = [
        tuple(map(fraction, c["bounds"])) for c in problem["fine_cells"] if c["bounds"] is not None
    ]
    result = []
    for index, tile in enumerate(problem["fine_tiles"]):
        a, b, c, d = map(fraction, tile["bounds"])
        us = sorted({a, b, *[x for box in positive for x in box[:2] if a < x < b]})
        vs = sorted({c, d, *[x for box in positive for x in box[2:] if c < x < d]})
        for left, right in pairwise(us):
            for bottom, top in pairwise(vs):
                result.append(
                    {
                        "event": tile["event"],
                        "bounds": rect((left, right, bottom, top)),
                        "fine_tile": index,
                        "coarse_tile": tile["coarse_tile"],
                    }
                )
    return result


def expected(problem):
    """Independent source integration, complete additivity and Gram certificates."""
    native(problem)
    probe = tuple(map(fraction, problem["probe"]))
    volume = area(probe)

    def cells_of(key):
        answer = []
        for row in problem[key]:
            b = None if row["bounds"] is None else tuple(map(fraction, row["bounds"]))
            answer.append((row["event"], b, F() if b is None else area(b)))
        assert [x[0] for x in answer] == sorted({x[0] for x in answer})
        partition_of(probe, [b for _, b, _ in answer if b is not None])
        return answer

    coarse, fine = cells_of("coarse_cells"), cells_of("fine_cells")
    parents = {}
    for event, bounds, _ in fine:
        choices = [
            e for e, b, _ in coarse if b is not None and bounds is not None and contained(bounds, b)
        ]
        assert len(choices) == (0 if bounds is None else 1)
        parents[event] = choices[0] if choices else None
    for e, b, _ in coarse:
        if b is not None:
            partition_of(b, [child for event, child, _ in fine if parents[event] == e])
    original = copy.deepcopy(problem["fine_tiles"])
    repair = overlay(problem)
    assert len(repair) <= 256
    ct = copy.deepcopy(problem["coarse_tiles"])
    for tile in ct:
        b = tuple(map(fraction, tile["bounds"]))
        tile["moments"] = rectangle_moments(b)
        tile["outgoing"] = [{"event": e, "coefficients": outgoing(b, d)} for e, d, _ in coarse]
    for tile in original:
        b = tuple(map(fraction, tile["bounds"]))
        tile["moments"] = rectangle_moments(b)
        owner = ct[tile["coarse_tile"]]
        assert parents[tile["event"]] == owner["event"]
        assert contained(b, tuple(map(fraction, owner["bounds"])))
    for tile in repair:
        b = tuple(map(fraction, tile["bounds"]))
        tile["moments"] = rectangle_moments(b)
        tile["outgoing"] = [{"event": e, "coefficients": outgoing(b, d)} for e, d, _ in fine]
    for level, tiles in ((coarse, ct), (fine, original)):
        for event, b, _ in level:
            pieces = [tuple(map(fraction, t["bounds"])) for t in tiles if t["event"] == event]
            if b is None:
                assert not pieces
            else:
                partition_of(b, pieces)
    for index, tile in enumerate(original):
        children = [r for r in repair if r["fine_tile"] == index]
        partition_of(
            tuple(map(fraction, tile["bounds"])),
            [tuple(map(fraction, r["bounds"])) for r in children],
        )
        assert tile["moments"] == [sum((r["moments"][j] for r in children), F()) for j in range(16)]
    for index, tile in enumerate(ct):
        children = [t for t in original if t["coarse_tile"] == index]
        descendants = [r for r in repair if r["coarse_tile"] == index]
        partition_of(
            tuple(map(fraction, tile["bounds"])),
            [tuple(map(fraction, r["bounds"])) for r in children],
        )
        assert tile["moments"] == [sum((r["moments"][j] for r in children), F()) for j in range(16)]
        assert tile["moments"] == [
            sum((r["moments"][j] for r in descendants), F()) for j in range(16)
        ]
    c, d, t, f, r = len(coarse), len(fine), len(ct), len(original), len(repair)
    n = 9 * f
    oc, of, orr = zeros(4 * t, n), zeros(4 * f, n), zeros(4 * r, n)
    qc, qf = zeros(c * c, n), zeros(d * d, n)
    generators = []
    for source, tile in enumerate(original):
        a, b, u, v = map(fraction, tile["bounds"])
        support = (a, b, u, v)
        parent = parents[tile["event"]]
        for i, j in POWERS:
            column = len(generators)
            cu, cv = bernstein_coefficients(i, a, b), bernstein_coefficients(j, u, v)
            generators.append(
                {
                    "tile": source,
                    "i": i,
                    "j": j,
                    "coefficients": [volume**2 * cu[p] * cv[q] for p, q in POWERS],
                }
            )
            for basis, (p, q) in enumerate(BASIS):
                value = (
                    volume**2
                    * beta_integral(i, a, b, a, b, p)
                    * beta_integral(j, u, v, u, v, q)
                    / 2
                )
                of[4 * source + basis][column] = value
                oc[4 * tile["coarse_tile"] + basis][column] = value
                for index, piece in enumerate(repair):
                    if piece["fine_tile"] == source:
                        x, y, z, w = map(fraction, piece["bounds"])
                        orr[4 * index + basis][column] = (
                            volume**2
                            * beta_integral(i, a, b, x, y, p)
                            * beta_integral(j, u, v, z, w, q)
                            / 2
                        )
            for row, (event, _, _) in enumerate(coarse):
                for target, (_, dest, _) in enumerate(coarse):
                    qc[row * c + target][column] = (
                        response_integral(support, dest, i, j, volume) if event == parent else F()
                    )
            for row, (event, _, _) in enumerate(fine):
                for target, (_, dest, _) in enumerate(fine):
                    qf[row * d + target][column] = (
                        response_integral(support, dest, i, j, volume)
                        if event == tile["event"]
                        else F()
                    )
        assert [sum((g["coefficients"][j] for g in generators[-9:]), F()) for j in range(9)] == [
            volume**2,
            *[F()] * 8,
        ]
    for index in range(f):
        for basis in range(4):
            assert of[4 * index + basis] == [
                sum(
                    (
                        orr[4 * k + basis][j]
                        for k, piece in enumerate(repair)
                        if piece["fine_tile"] == index
                    ),
                    F(),
                )
                for j in range(n)
            ]
    for index in range(t):
        for basis in range(4):
            assert oc[4 * index + basis] == [
                sum(
                    (
                        of[4 * k + basis][j]
                        for k, piece in enumerate(original)
                        if piece["coarse_tile"] == index
                    ),
                    F(),
                )
                for j in range(n)
            ]
            assert oc[4 * index + basis] == [
                sum(
                    (
                        orr[4 * k + basis][j]
                        for k, piece in enumerate(repair)
                        if piece["coarse_tile"] == index
                    ),
                    F(),
                )
                for j in range(n)
            ]
    for i, (a, _, _) in enumerate(coarse):
        for j, (b, _, _) in enumerate(coarse):
            selected = [
                x * d + y
                for x, (e, _, _) in enumerate(fine)
                for y, (h, _, _) in enumerate(fine)
                if parents[e] == a and parents[h] == b
            ]
            assert qc[i * c + j] == [
                sum((qf[k][column] for k in selected), F()) for column in range(n)
            ]

    def response_map(cells, tiles):
        return [
            [
                x
                for tile in tiles
                for x in (
                    tile["outgoing"][j]["coefficients"] if tile["event"] == owner else [F()] * 4
                )
            ]
            for owner, _, _ in cells
            for j in range(len(cells))
        ]

    gc, gr = response_map(coarse, ct), response_map(fine, repair)
    assert mm(gc, oc) == qc and mm(gr, orr) == qf

    def constants(tiles):
        return [
            volume**2 * tile["moments"][MOMENTS.index(exponent)]
            for tile in tiles
            for exponent in BASIS
        ]

    constant_oc, constant_of, constant_orr = constants(ct), constants(original), constants(repair)
    constant_qc = [constant_response(a, b, volume) for _, a, _ in coarse for _, b, _ in coarse]
    constant_qf = [constant_response(a, b, volume) for _, a, _ in fine for _, b, _ in fine]
    for values, want in (
        (oc, constant_oc),
        (of, constant_of),
        (orr, constant_orr),
        (qc, constant_qc),
        (qf, constant_qf),
    ):
        assert [sum(row, F()) for row in values] == want
    integrals = [sum((oc[4 * k][j] for k in range(t)), F()) for j in range(n)]
    assert integrals == [
        volume**2 * area(tuple(map(fraction, tile["bounds"]))) / 9
        for tile in original
        for _ in range(9)
    ]
    assert sum(integrals, F()) == volume**3
    cs = [volume**2 * a * b for _, _, a in coarse for _, _, b in coarse]
    fs = [volume**2 * a * b for _, _, a in fine for _, _, b in fine]
    cert = gram_certificate(oc, qf)
    predicted = mm(gr, orr)
    residuals = [
        [a - b for a, b in zip(p, q, strict=True)] for p, q in zip(predicted, qf, strict=True)
    ]
    repaired = None
    if cert["collision"] is not None:
        collision = cert["collision"]
        plus, minus = collision["weights_plus"], collision["weights_minus"]
        fp, fm = [dot(row, plus) for row in of], [dot(row, minus) for row in of]
        rp, rm = [dot(row, plus) for row in orr], [dot(row, minus) for row in orr]
        pp, pm = [dot(row, rp) for row in gr], [dot(row, rm) for row in gr]
        assert pp == collision["truth_plus"] and pm == collision["truth_minus"]
        difference = [a - b for a, b in zip(rp, rm, strict=True)]
        assert any(difference)
        repaired = {
            "fine_observed_plus": fp,
            "fine_observed_minus": fm,
            "observed_plus": rp,
            "observed_minus": rm,
            "difference": difference,
            "predicted_plus": pp,
            "predicted_minus": pm,
            "residual_plus": [F()] * (d * d),
            "residual_minus": [F()] * (d * d),
            "normalized_truth_difference": [
                x / s if s else None for x, s in zip(collision["truth_difference"], fs, strict=True)
            ],
        }
    bound_rows = sum(bool(s) for s in fs)
    collision = cert["collision"]
    counts = {
        "coarse_cells": c,
        "fine_cells": d,
        "positive_coarse_cells": sum(bool(h) for _, _, h in coarse),
        "positive_fine_cells": sum(bool(h) for _, _, h in fine),
        "coarse_tiles": t,
        "fine_tiles": f,
        "repair_tiles": r,
        "added_repair_tiles": r - f,
        "generators": n,
        "coarse_observation_rows": 4 * t,
        "fine_observation_rows": 4 * f,
        "repair_observation_rows": 4 * r,
        "coarse_response_rows": c * c,
        "fine_response_rows": d * d,
        "defined_fine_response_rows": bound_rows,
        "undefined_fine_response_rows": d * d - bound_rows,
        "coarse_moment_entries": 16 * t,
        "fine_moment_entries": 16 * f,
        "repair_moment_entries": 16 * r,
        "outgoing_entries": sum(
            len(z["coefficients"]) for tile in ct + repair for z in tile["outgoing"]
        ),
        "source_coefficient_entries": sum(len(g["coefficients"]) for g in generators),
        "observation_entries": sum(sum(map(len, m)) for m in (oc, of, orr)),
        "target_entries": sum(sum(map(len, m)) for m in (qc, qf)),
        "constant_observation_entries": len(constant_oc) + len(constant_of) + len(constant_orr),
        "constant_target_entries": len(constant_qc) + len(constant_qf),
        "generator_integral_entries": len(integrals),
        "raw_geometric_entries": sum(map(len, gc)) + d * d + sum(map(len, gr)),
        "certificate_decoder_entries": sum(
            len(row) for row in cert["row_decoders"] if row is not None
        )
        + (sum(map(len, cert["decoder"])) if cert["decoder"] is not None else 0),
        "recoverable_rows": len(cert["recoverable_rows"]),
        "failed_rows": len(cert["failed_rows"]),
        "collisions": int(collision is not None),
        "collision_entries": 0
        if collision is None
        else 1
        + sum(
            len(collision[key])
            for key in (
                "null_vector",
                "weights_plus",
                "weights_minus",
                "observed_plus",
                "observed_minus",
                "truth_plus",
                "truth_minus",
                "truth_difference",
            )
        ),
        "repair_prediction_entries": sum(map(len, predicted)),
        "repair_residual_entries": sum(map(len, residuals)),
        "repair_collision_entries": 0
        if repaired is None
        else sum(sum(x is not None for x in values) for values in repaired.values()),
    }
    return encode(
        {
            "problem": copy.deepcopy(problem),
            "geometry": {
                "volume": volume,
                "coarse_cells": [
                    {"event": e, "bounds": None if b is None else rect(b), "volume": h}
                    for e, b, h in coarse
                ],
                "fine_cells": [
                    {"event": e, "bounds": None if b is None else rect(b), "volume": h}
                    for e, b, h in fine
                ],
                "parents": [{"event": e, "parent": parents[e]} for e, _, _ in fine],
                "coarse_tiles": ct,
                "fine_tiles": original,
                "repair_tiles": repair,
                "coarse_response_scales": cs,
                "fine_response_scales": fs,
            },
            "generators": generators,
            "matrices": {
                "coarse_observation_rows": [
                    {"tile": k, "basis": b} for k in range(t) for b in range(4)
                ],
                "fine_observation_rows": [
                    {"tile": k, "basis": b} for k in range(f) for b in range(4)
                ],
                "repair_observation_rows": [
                    {"tile": k, "basis": b} for k in range(r) for b in range(4)
                ],
                "coarse_response_rows": [
                    {"first": a, "second": b} for a, _, _ in coarse for b, _, _ in coarse
                ],
                "fine_response_rows": [
                    {"first": a, "second": b} for a, _, _ in fine for b, _, _ in fine
                ],
                "coarse_observations": oc,
                "fine_observations": of,
                "repair_observations": orr,
                "coarse_targets": qc,
                "fine_targets": qf,
                "coarse_geometric": gc,
                "generator_integrals": integrals,
                "constant_coarse_observations": constant_oc,
                "constant_fine_observations": constant_of,
                "constant_repair_observations": constant_orr,
                "constant_coarse_targets": constant_qc,
                "constant_fine_targets": constant_qf,
            },
            "certificate": cert,
            "repair": {
                "intercept": [F()] * (d * d),
                "matrix": gr,
                "predicted": predicted,
                "residuals": residuals,
                "exact": True,
                "collision": repaired,
            },
            "checks": dict.fromkeys(CHECKS, True),
            "counts": counts,
        }
    )


def unit_problem():
    return {
        "family": "same-level",
        "probe": rect(UNIT),
        "coarse_cells": [{"event": -4, "bounds": rect(UNIT)}],
        "fine_cells": [{"event": -4, "bounds": rect(UNIT)}],
        "coarse_tiles": [{"event": -4, "bounds": rect(UNIT)}],
        "fine_tiles": [{"event": -4, "bounds": rect(UNIT), "coarse_tile": 0}],
    }


def partition_problem(rectangles, coarse_empty=False, fine_empty=False):
    coarse_id = 4
    coarse = [{"event": coarse_id, "bounds": rect(UNIT)}]
    fine = [{"event": i + 1, "bounds": rect(b)} for i, b in enumerate(rectangles)]
    if coarse_empty:
        coarse.insert(0, {"event": -5, "bounds": None})
    if fine_empty:
        fine.insert(0, {"event": -7, "bounds": None})
    return {
        "family": "partition-hand",
        "probe": rect(UNIT),
        "coarse_cells": coarse,
        "fine_cells": fine,
        "coarse_tiles": [{"event": coarse_id, "bounds": rect(UNIT)}],
        "fine_tiles": [
            {"event": i + 1, "bounds": rect(b), "coarse_tile": 0} for i, b in enumerate(rectangles)
        ],
    }


def split_problem():
    return partition_problem([(0, F(1, 2), 0, 1), (F(1, 2), 1, 0, 1)])


def overlay_problem(inactive=False):
    if inactive:
        boxes = [(0, F(1, 2), 0, F(1, 3)), (0, F(1, 2), F(1, 3), 1), (F(1, 2), 1, 0, 1)]
    else:
        boxes = [(0, F(1, 2), 0, 1), (F(1, 2), 1, 0, F(1, 3)), (F(1, 2), 1, F(1, 3), 1)]
    return partition_problem(boxes)


def null_problem():
    return partition_problem([(0, F(1, 2), 0, 1), (F(1, 2), 1, 0, 1)], True, True)


def oversized_overlay_problem():
    rectangles = [(0, F(1, 2), 0, 1)] + [(F(1, 2), 1, F(j, 7), F(j + 1, 7)) for j in range(7)]
    p = partition_problem(rectangles)
    p["fine_tiles"] = [
        {"event": 1, "bounds": rect((F(j, 114), F(j + 1, 114), 0, 1)), "coarse_tile": 0}
        for j in range(57)
    ] + [{"event": j + 2, "bounds": rect(rectangles[j + 1]), "coarse_tile": 0} for j in range(7)]
    assert len(p["fine_tiles"]) == 64
    return p


def densify_certificate(cert, observations):
    m = len(observations)
    rows = cert["row_decoders"]
    intercept = [None] * len(rows)
    linear = [None] * len(rows)
    for j, row in enumerate(rows):
        if row is None:
            continue
        intercept[j] = F()
        linear[j] = [F()] * m
        for index, value in zip(cert["row_basis"], map(fraction, row), strict=True):
            if index == 0:
                intercept[j] = value
            else:
                linear[j][index - 1] = value
    return intercept, linear


def certificate_validity(observations, targets, certificate):
    o, q = matrix(observations), matrix(targets)
    a = [[F(1)] * len(q[0]), *o]
    basis = [a[i] for i in certificate["row_basis"]]
    for j, row in enumerate(certificate["row_decoders"]):
        if row is not None:
            assert [dot(list(map(fraction, row)), col) for col in zip(*basis, strict=True)] == q[j]
    collision = certificate["collision"]
    if collision is not None:
        w, plus, minus = (
            list(map(fraction, collision[key]))
            for key in ("null_vector", "weights_plus", "weights_minus")
        )
        assert not any(dot(row, w) for row in a)
        assert sum(plus, F()) == sum(minus, F()) == 1
        assert all(x >= 0 and y >= 0 and not x * y for x, y in zip(plus, minus, strict=True))
        assert [dot(row, plus) for row in o] == [dot(row, minus) for row in o]
        for key, rows, weights in (
            ("observed_plus", o, plus),
            ("observed_minus", o, minus),
            ("truth_plus", q, plus),
            ("truth_minus", q, minus),
        ):
            assert list(map(fraction, collision[key])) == [dot(row, weights) for row in rows]
        mass = fraction(collision["positive_mass"])
        assert list(map(fraction, collision["truth_difference"])) == [
            dot(row, w) / mass for row in q
        ]
        assert fraction(collision["truth_difference"][collision["separating_row"]]) != 0


@pytest.mark.parametrize(
    "observations,targets",
    [
        ([], [[1, 1, 1], [0, 0, 0]]),
        ([[0, 0, 0]], [[0, 1, 0]]),
        ([[0, 0, 1, 1]], [[0, 0, 0, 1], [0, 1, 0, 0]]),
        ([[1, 1, 1], [2, 2, 2], [0, 0, 0]], [[0, 0, 0], [7, 7, 7]]),
        ([[0, 1, 2]], [[1, 3, 5], [0, 0, 1], [4, 4, 4]]),
        ([[0, F(1, 1 << 3500)]], [[0, 1]]),
    ],
)
def test_complete_standalone_gram_certificates(engines, observations, targets):
    o, q = (
        encode([[F(x) for x in row] for row in observations]),
        encode([[F(x) for x in row] for row in targets]),
    )
    want = expected_certificate(o, q)
    for engine in engines:
        got = engine.certify(o, q)
        assert wire(got) == wire(want)
        certificate_validity(o, q, got)


def test_free_column_first_not_target_first_and_mass_normalization(engines):
    o = encode([[F(0), F(0), F(1), F(1)]])
    q = encode([[F(0), F(0), F(0), F(1)], [F(0), F(1), F(0), F(0)]])
    for engine in engines:
        c = engine.certify(o, q)["collision"]
        assert c["free_column"] == 1 and c["separating_row"] == 1
        assert c["null_vector"] == list(map(fw, (-1, 1, 0, 0)))
        # A separate relation has positive mass2, so raw Q*w is not the retained difference.
        o2 = encode([[F(0), F(1), F(2)]])
        q2 = encode([[F(0), F(0), F(1)]])
        c2 = engine.certify(o2, q2)["collision"]
        assert c2["null_vector"] == list(map(fw, (1, -2, 1)))
        assert c2["positive_mass"] == fw(2)
        assert c2["truth_difference"] == [fw(F(1, 2))]
        assert c2["weights_plus"] == list(map(fw, (F(1, 2), 0, F(1, 2))))


def test_normalization_only_and_partial_target_recovery(engines):
    for engine in engines:
        c = engine.certify([], [[fw(7), fw(7)]])
        assert c["recoverable"] and c["row_basis"] == [0] and c["decoder"] == [[fw(7)]]
        c = engine.certify(
            [[fw(0), fw(1), fw(2)]], [[fw(1), fw(3), fw(5)], [fw(0), fw(0), fw(1)], [fw(4)] * 3]
        )
        assert not c["recoverable"] and c["decoder"] is None
        assert c["recoverable_rows"] == [0, 2] and c["failed_rows"] == [1]
        assert c["row_decoders"] == [[fw(1), fw(2)], None, [fw(4), fw(0)]]


@pytest.mark.parametrize(
    "factory",
    [unit_problem, split_problem, overlay_problem, lambda: overlay_problem(True), null_problem],
)
def test_generic_full_family_independent_integral_and_gram_oracle(engines, factory):
    p = factory()
    want = expected(p)
    before = wire(p)
    for engine in engines:
        got = engine.build_family(p)
        assert wire(got) == wire(want) and wire(p) == before
        certificate_validity(
            got["matrices"]["coarse_observations"],
            got["matrices"]["fine_targets"],
            got["certificate"],
        )


def test_analytic_two_nonnegative_mixtures_collide_but_fine_truths_differ(engines):
    for engine in engines:
        result = engine.build_family(split_problem())
        m = result["matrices"]
        plus = [F(j == 7) for j in range(18)]
        minus = [F(1, 2) if j in (1, 10) else F() for j in range(18)]
        oc, qf = matrix(m["coarse_observations"]), matrix(m["fine_targets"])
        observed = list(map(fw, (F(1, 144), F(1, 384), F(1, 288), F(1, 768))))
        assert list(map(fw, [dot(row, plus) for row in oc])) == observed
        assert list(map(fw, [dot(row, minus) for row in oc])) == observed
        assert [dot(row, plus) for row in qf] == [F(1, 4608), F(1, 1152), F(), F()]
        assert [dot(row, minus) for row in qf] == [F(1, 3072), F(1, 2304), F(), F(1, 3072)]
        assert sum(dot(row, plus) for row in qf) == sum(dot(row, minus) for row in qf) == F(5, 4608)
        assert not result["certificate"]["recoverable"]
        assert result["repair"]["exact"]
        new = matrix(m["repair_observations"])
        assert [dot(row, plus) for row in new] != [dot(row, minus) for row in new]


def test_same_level_recovery_is_not_full_field_identification(engines):
    for engine in engines:
        result = engine.build_family(unit_problem())
        c = result["certificate"]
        assert c["recoverable"] and c["collision"] is None
        assert result["repair"]["collision"] is None
        assert c["observation_rank"] < result["counts"]["generators"]
        a, l = densify_certificate(c, result["matrices"]["coarse_observations"])
        for index, column in enumerate(
            zip(*result["matrices"]["coarse_observations"], strict=True)
        ):
            assert engine.apply(encode(a), encode(l), list(column)) == [
                row[index] for row in result["matrices"]["fine_targets"]
            ]


def test_overlay_integrates_original_source_not_restarted_piece_sources(engines):
    for engine in engines:
        result = engine.build_family(overlay_problem())
        assert result["counts"]["fine_tiles"] == 3 and result["counts"]["repair_tiles"] == 4
        assert result["counts"]["generators"] == 27
        first = result["geometry"]["repair_tiles"][:2]
        assert [r["fine_tile"] for r in first] == [0, 0]
        o = result["matrices"]["repair_observations"]
        assert o[0][0] == fw(F(19, 3888)) and o[4][0] == fw(F(8, 3888))
        assert result["matrices"]["fine_observations"][0][0] == fw(F(1, 144))
        # Reinitializing local Bernstein coordinates would instead give these:
        assert o[0][0] != fw(F(1, 432)) and o[4][0] != fw(F(1, 216))
        inactive = engine.build_family(overlay_problem(True))
        assert inactive["counts"]["repair_tiles"] == 4
        assert [r["fine_tile"] for r in inactive["geometry"]["repair_tiles"][-2:]] == [2, 2]
        for tile in inactive["geometry"]["repair_tiles"][-2:]:
            assert tile["outgoing"][0]["coefficients"] == [fw(0)] * 4


def test_empty_fine_targets_keep_recovery_rows_and_normalized_collision_nulls(engines):
    for engine in engines:
        result = engine.build_family(null_problem())
        c = result["certificate"]
        for row in (0, 1, 2, 3, 6):
            assert row in c["recoverable_rows"]
            assert all(x == fw(0) for x in c["row_decoders"][row])
            assert result["geometry"]["fine_response_scales"][row] == fw(0)
            assert result["repair"]["collision"]["normalized_truth_difference"][row] is None
            assert c["collision"]["truth_difference"][row] == fw(0)
        assert result["geometry"]["parents"][0] == {"event": -7, "parent": None}


def affine_problem(problem, alpha=F(3, 2), beta=F(5, 3), du=F(-7, 4), dv=F(2, 7)):
    result = copy.deepcopy(problem)

    def bounds(b):
        if b is None:
            return None
        u0, u1, v0, v1 = map(fraction, b)
        return rect((alpha * u0 + du, alpha * u1 + du, beta * v0 + dv, beta * v1 + dv))

    result["probe"] = bounds(result["probe"])
    for kind in ("coarse_cells", "fine_cells", "coarse_tiles", "fine_tiles"):
        for row in result[kind]:
            row["bounds"] = bounds(row["bounds"])
    return result


def basis_change(alpha, beta, du, dv):
    return [
        [F(1), F(), F(), F()],
        [du, alpha, F(), F()],
        [dv, F(), beta, F()],
        [du * dv, alpha * dv, beta * du, alpha * beta],
    ]


def transform_observations(rows, alpha, beta, du, dv):
    k = alpha * beta
    t = basis_change(alpha, beta, du, dv)
    return [
        row
        for start in range(0, len(rows), 4)
        for row in mm([[k**3 * x for x in r] for r in t], rows[start : start + 4])
    ]


def assert_affine(base, moved, alpha, beta, du, dv):
    k = alpha * beta
    assert moved["generators"] != base["generators"]

    def pullback(coefficients, exponents, degree):
        return [
            k**degree
            * sum(
                fraction(c)
                * F(comb(p, r) * comb(q, s))
                * (-du) ** (p - r)
                * (-dv) ** (q - s)
                / (alpha**p * beta**q)
                for c, (p, q) in zip(coefficients, exponents, strict=True)
                if p >= r and q >= s
            )
            for r, s in exponents
        ]

    for a, b in zip(base["generators"], moved["generators"], strict=True):
        assert {key: a[key] for key in ("tile", "i", "j")} == {
            key: b[key] for key in ("tile", "i", "j")
        }
        assert list(map(fraction, b["coefficients"])) == pullback(a["coefficients"], POWERS, 2)
    assert moved["geometry"]["parents"] == base["geometry"]["parents"]
    for name in ("coarse", "fine", "repair"):
        old = base["geometry"][name + "_tiles"]
        new = moved["geometry"][name + "_tiles"]
        assert len(old) == len(new)
        for a, b in zip(old, new, strict=True):
            om = list(map(fraction, a["moments"]))
            nm = list(map(fraction, b["moments"]))
            for index, (i, j) in enumerate(MOMENTS):
                want = k * sum(
                    F(comb(i, p) * comb(j, q))
                    * alpha**p
                    * beta**q
                    * du ** (i - p)
                    * dv ** (j - q)
                    * om[MOMENTS.index((p, q))]
                    for p in range(i + 1)
                    for q in range(j + 1)
                )
                assert nm[index] == want
            for key in ("event", "fine_tile", "coarse_tile"):
                if key in a:
                    assert a[key] == b[key]
            if "outgoing" in a:
                for first, second in zip(a["outgoing"], b["outgoing"], strict=True):
                    assert first["event"] == second["event"]
                    assert list(map(fraction, second["coefficients"])) == pullback(
                        first["coefficients"], BASIS, 1
                    )
        original = matrix(base["matrices"][name + "_observations"])
        assert matrix(moved["matrices"][name + "_observations"]) == transform_observations(
            original, alpha, beta, du, dv
        )
        original_c = [[fraction(x)] for x in base["matrices"]["constant_" + name + "_observations"]]
        assert [
            [fraction(x)] for x in moved["matrices"]["constant_" + name + "_observations"]
        ] == transform_observations(original_c, alpha, beta, du, dv)
    for name in ("coarse", "fine"):
        assert matrix(moved["matrices"][name + "_targets"]) == [
            [k**4 * x for x in row] for row in matrix(base["matrices"][name + "_targets"])
        ]
        assert list(map(fraction, moved["matrices"]["constant_" + name + "_targets"])) == [
            k**4 * fraction(x) for x in base["matrices"]["constant_" + name + "_targets"]
        ]
    cert, mc = base["certificate"], moved["certificate"]
    for key in (
        "observation_rank",
        "target_rank",
        "joint_rank",
        "row_basis",
        "pivot_columns",
        "free_columns",
        "recoverable",
        "recoverable_rows",
        "failed_rows",
    ):
        assert cert[key] == mc[key]
    if cert["collision"] is not None:
        c, d = cert["collision"], mc["collision"]
        for key in (
            "free_column",
            "separating_row",
            "null_vector",
            "positive_mass",
            "weights_plus",
            "weights_minus",
        ):
            assert c[key] == d[key]
        for key in ("truth_plus", "truth_minus", "truth_difference"):
            assert list(map(fraction, d[key])) == [k**4 * fraction(x) for x in c[key]]
        assert (
            base["repair"]["collision"]["normalized_truth_difference"]
            == moved["repair"]["collision"]["normalized_truth_difference"]
        )
    # A canonical compact decoder need not transport by its selected submatrix:
    # recover the full dense map first, then transport the SAME map blockwise.
    a, l = densify_certificate(cert, base["matrices"]["coarse_observations"])
    inverse = basis_change(1 / alpha, 1 / beta, -du / alpha, -dv / beta)
    repair = []
    for row in matrix(base["repair"]["matrix"]):
        repair.append(
            [
                k * sum(row[start + i] * inverse[i][j] for i in range(4))
                for start in range(0, len(row), 4)
                for j in range(4)
            ]
        )
    assert matrix(moved["repair"]["matrix"]) == repair
    assert list(map(fraction, moved["repair"]["intercept"])) == [
        k**4 * fraction(x) for x in base["repair"]["intercept"]
    ]
    for row, intercept in zip(l, a, strict=True):
        if row is None:
            continue
        transported = []
        for start in range(0, len(row), 4):
            transported.extend(
                [k * sum(row[start + i] * inverse[i][j] for i in range(4)) for j in range(4)]
            )
        actual = [
            k**4 * intercept + dot(transported, column)
            for column in zip(*matrix(moved["matrices"]["coarse_observations"]), strict=True)
        ]
        original = [
            intercept + dot(row, column)
            for column in zip(*matrix(base["matrices"]["coarse_observations"]), strict=True)
        ]
        assert actual == [k**4 * x for x in original]


@pytest.mark.parametrize("factory", [unit_problem, overlay_problem, null_problem])
def test_signed_unequal_affine_full_wire_and_same_dense_maps(engines, factory):
    problem = factory()
    moved = affine_problem(problem)
    want, want_moved = expected(problem), expected(moved)
    assert_affine(want, want_moved, F(3, 2), F(5, 3), F(-7, 4), F(2, 7))
    for engine in engines:
        assert wire(engine.build_family(problem)) == wire(want)
        actual = engine.build_family(moved)
        assert wire(actual) == wire(want_moved)
        assert wire(
            engine.certify(
                actual["matrices"]["coarse_observations"], actual["matrices"]["fine_targets"]
            )
        ) == wire(actual["certificate"])


def test_restricted_apply_uses_only_intercept_map_and_observed_values(engines, monkeypatch):
    expected_family = expected(overlay_problem())
    a = expected_family["repair"]["intercept"]
    l = expected_family["repair"]["matrix"]
    observation = expected_family["repair"]["collision"]["observed_plus"]
    truth = expected_family["certificate"]["collision"]["truth_plus"]

    def forbidden(*args, **kwargs):
        raise AssertionError("restricted apply attempted file access")

    with monkeypatch.context() as m:
        m.setattr(builtins, "open", forbidden)
        m.setattr(Path, "open", forbidden)
        m.setattr(Path, "read_bytes", forbidden)
        m.setattr(Path, "read_text", forbidden)
        for engine in engines:
            assert engine.apply(a, l, observation) == truth
            # No normalization is inferred from arbitrary supplied observations.
            assert engine.apply(
                [fw(2)], [[fw(1), fw(-1), fw(0), fw(0)]], [fw(7), fw(4), fw(-8), fw(9)]
            ) == [fw(5)]


def test_native_shared_input_and_all_output_ownership(engines):
    problem = unit_problem()
    shared = problem["probe"]
    for key in ("coarse_cells", "fine_cells", "coarse_tiles", "fine_tiles"):
        problem[key][0]["bounds"] = shared
    before = wire(problem)
    for engine in engines:
        result = engine.build_family(problem)
        frozen = wire(result)
        assert wire(problem) == before
        problem["family"] = "changed-input"
        assert wire(result) == frozen
        problem["family"] = "same-level"
        result["geometry"]["coarse_tiles"][0]["moments"][0][0] += 1
        assert wire(problem) == before
        assert wire(engine.build_family(problem)) == frozen
        o, q = encode([[F(0), F(1), F(2)]]), encode([[F(0), F(0), F(1)]])
        certificate = engine.certify(o, q)
        unchanged = wire(certificate)
        q[0][2] = fw(2)
        assert wire(certificate) == unchanged
        assert engine.certify(o, encode([[F(0), F(0), F(1)]])) == certificate


def test_apply_and_certificate_accepted_dimension_edges(engines):
    for engine in engines:
        o = encode([[F()] * 576 for _ in range(256)])
        q = encode([[F(i % 2)] * 576 for i in range(64)])
        c = engine.certify(o, q)
        assert c["row_basis"] == [0] and c["observation_rank"] == 1
        assert c["recoverable"] and len(c["row_decoders"]) == 64
        assert len(c["free_columns"]) == 575
        assert (
            engine.apply([fw(2)] * 64, [[fw(0)] * 1024 for _ in range(64)], [fw(5)] * 1024)
            == [fw(2)] * 64
        )


class NativeListSubclass(list):
    pass


def malformed_families():
    p = unit_problem()
    yield None
    yield []
    yield {**p, "old_targets": []}
    yield {key: value for key, value in p.items() if key != "fine_tiles"}
    for value in ("", 1, False):
        yield replaced(p, ["family"], value)
    for value in (None, [], [fw(0)] * 3, [[0], [1, 1], [0, 1], [1, 1]]):
        yield replaced(p, ["probe"], value)
    for value in (True, 0.0, F(0), (0, 1), [0, 0], [0, -1], [2, 2], [1 << 4096, 1]):
        yield replaced(p, ["probe", 0], value)
    for key in ("coarse_cells", "fine_cells", "coarse_tiles", "fine_tiles"):
        yield replaced(p, [key], [])
        yield replaced(p, [key], tuple(p[key]))
        yield replaced(p, [key, 0, "extra"], 0)
        yield replaced(p, [key, 0, "event"], True)
    yield replaced(p, ["fine_cells"], p["fine_cells"] * 9)
    yield replaced(p, ["fine_tiles"], p["fine_tiles"] * 65)
    yield replaced(p, ["coarse_tiles"], p["coarse_tiles"] * 65)
    yield replaced(p, ["fine_tiles", 0, "coarse_tile"], True)
    yield replaced(p, ["fine_tiles", 0, "coarse_tile"], 1)
    yield replaced(p, ["fine_cells", 0, "bounds"], None)
    yield replaced(p, ["coarse_cells", 0, "bounds"], None)
    yield replaced(p, ["fine_tiles", 0, "bounds"], None)
    yield replaced(p, ["coarse_tiles", 0, "bounds"], rect((0, F(1, 2), 0, 1)))
    yield replaced(p, ["fine_cells", 0, "bounds"], rect((0, 2, 0, 1)))
    yield replaced(p, ["fine_tiles", 0, "bounds"], rect((0, 1, 0, 0)))
    yield NativeListSubclass()
    split = split_problem()
    yield replaced(split, ["fine_cells"], list(reversed(split["fine_cells"])))
    yield replaced(split, ["fine_cells", 1, "event"], 1)
    yield replaced(split, ["fine_cells", 1, "bounds"], rect((F(1, 3), 1, 0, 1)))
    yield replaced(split, ["fine_cells", 1, "bounds"], rect((F(2, 3), 1, 0, 1)))
    yield replaced(split, ["fine_tiles", 1, "event"], 1)
    yield oversized_overlay_problem()


def malformed_certificates():
    o, q = encode([[F(), F(1)]]), encode([[F(1), F()]])
    for value in (None, {}, (), NativeListSubclass(o)):
        yield value, q
    for value in (None, [], {}, (), [[]], [[fw(0)]], q * 65):
        yield o, value
    yield o * 257, q
    yield [], [[fw(0)] * 577]
    yield [[fw(0)]], q
    yield [[fw(0), fw(1)], [fw(0)]], q
    for value in (True, 0.0, F(0), (0, 1), [1, 0], [2, 2], [1 << 4096, 1]):
        yield replaced(o, [0, 0], value), q
        yield o, replaced(q, [0, 1], value)


def malformed_applications():
    a, l, x = [fw(0)], [[fw(1)] * 4], [fw(1)] * 4
    for value in (None, [], (), [fw(0)] * 65, [True], [[2, 2]]):
        yield value, l, x
    for value in (
        None,
        [],
        (),
        [[]],
        [[fw(1)] * 3],
        [[fw(1)] * 1028],
        [[fw(1)] * 4] * 2,
        [[True] * 4],
    ):
        yield a, value, x
    for value in (None, [], (), [fw(1)] * 3, [True] * 4):
        yield a, l, value
    yield a, [[fw(1)] * 4, [fw(1)] * 3], x
    yield [fw(0)] * 2, [[fw(1)] * 4, [fw(1)] * 3], x


def require_rejection(call):
    try:
        call()
    except ValueError:
        return
    raise RuntimeError("expected explicit ValueError")


def explicit_guards(engine):
    count = 0
    for p in malformed_families():
        require_rejection(lambda p=p: engine.build_family(p))
        count += 1
    for o, q in malformed_certificates():
        require_rejection(lambda o=o, q=q: engine.certify(o, q))
        count += 1
    for a, l, x in malformed_applications():
        require_rejection(lambda a=a, l=l, x=x: engine.apply(a, l, x))
        count += 1
    d = 1 << 4095
    # Products overflow internally but the retained result is exactly zero.
    if engine.apply([fw(0)], [[fw(d), fw(-d), fw(0), fw(0)]], [fw(2)] * 4) != [fw(0)]:
        raise RuntimeError("unretained cancellation rejected")
    require_rejection(lambda: engine.apply([fw(0)], [[fw(d), fw(d), fw(0), fw(0)]], [fw(1)] * 4))
    return count + 1


def test_strict_public_guard_inventory(engines):
    counts = [explicit_guards(engine) for engine in engines]
    assert counts[0] == counts[1] and counts[0] > 70


def test_late_pair_shape_and_complete_overlay_cap_precede_arithmetic(engines, monkeypatch):
    for engine in engines:
        calls = []

        def forbidden(*args, calls=calls, **kwargs):
            calls.append(1)
            raise AssertionError("arithmetic before admission")

        with monkeypatch.context() as m:
            m.setattr(engine, "_rectangle", forbidden)
            for value in ([], [0]):
                problem = replaced(unit_problem(), ["fine_tiles", 0, "bounds", 3], value)
                with pytest.raises(ValueError):
                    engine.build_family(problem)
            assert calls == []
        with monkeypatch.context() as m:
            m.setattr(engine, "_moments", forbidden)
            with pytest.raises(ValueError):
                engine.build_family(oversized_overlay_problem())
            assert calls == []
        hook = "_row_basis" if engine.__name__.endswith("primary") else "_echelon"
        with monkeypatch.context() as m:
            m.setattr(engine, hook, forbidden)
            with pytest.raises(ValueError):
                engine.certify([[fw(0), fw(1)]], [[fw(1), fw(0)], [fw(1)]])
            assert calls == []


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guards_in_isolated_normal_and_optimized_python(tmp_path, optimized):
    script = r"""
import importlib.util,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("ar_guard_tests",path)
tests=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tests)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=tests.load("_qr05ar_guard_"+name,file)
    counts.append(tests.explicit_guards(engine))
    calls=[]
    def forbidden(*args,**kwargs):
        calls.append(1)
        raise RuntimeError("early arithmetic")
    original=engine._moments
    engine._moments=forbidden
    tests.require_rejection(lambda:engine.build_family(tests.oversized_overlay_problem()))
    engine._moments=original
    rectangle=engine._rectangle
    engine._rectangle=forbidden
    for value in ([],[0]):
        p=tests.replaced(tests.unit_problem(),["fine_tiles",0,"bounds",3],value)
        tests.require_rejection(lambda p=p:engine.build_family(p))
    engine._rectangle=rectangle
    if calls:
        raise RuntimeError("reservation/shape preflight not early")
print(counts)
"""
    args = [sys.executable, "-I", "-X", "pycache_prefix=" + str(tmp_path / "cache")]
    if optimized:
        args.append("-O")
    result = subprocess.run(
        [*args, "-c", script, str(Path(__file__).resolve())],
        check=True,
        capture_output=True,
        text=True,
        timeout=90,
    )
    inventory = (
        len(list(malformed_families()))
        + len(list(malformed_certificates()))
        + len(list(malformed_applications()))
        + 1
    )
    assert json.loads(result.stdout) == [inventory, inventory]


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


def changed_fraction(tree, path):
    current = tree
    for key in path:
        current = current[key]
    return replaced(tree, path, fw(fraction(current) + 1))


def certificate_mutations(certificate):
    for key in ("observation_rank", "target_rank", "joint_rank"):
        yield replaced(certificate, [key], certificate[key] + 1)
    for key in ("row_basis", "pivot_columns", "free_columns", "recoverable_rows", "failed_rows"):
        yield replaced(certificate, [key], certificate[key] + [-1])
    yield replaced(certificate, ["recoverable"], not certificate["recoverable"])
    for index, row in enumerate(certificate["row_decoders"]):
        if row is not None:
            yield changed_fraction(certificate, ["row_decoders", index, 0])
            break
    if certificate["decoder"] is not None:
        yield changed_fraction(certificate, ["decoder", 0, 0])
    else:
        yield replaced(certificate, ["decoder"], [])
    collision = certificate["collision"]
    if collision is None:
        yield replaced(certificate, ["collision"], {})
    else:
        for key in ("free_column", "separating_row"):
            yield replaced(certificate, ["collision", key], collision[key] + 1)
        yield changed_fraction(certificate, ["collision", "positive_mass"])
        for key in (
            "null_vector",
            "weights_plus",
            "weights_minus",
            "observed_plus",
            "observed_minus",
            "truth_plus",
            "truth_minus",
            "truth_difference",
        ):
            yield changed_fraction(certificate, ["collision", key, 0])


def family_mutations(family):
    paths = [
        ["problem", "probe", 0],
        ["geometry", "volume"],
        ["geometry", "coarse_cells", -1, "volume"],
        ["geometry", "fine_cells", -1, "bounds", 0],
        ["geometry", "coarse_tiles", 0, "moments", 15],
        ["geometry", "fine_tiles", 0, "moments", 15],
        ["geometry", "repair_tiles", 0, "moments", 15],
        ["geometry", "coarse_tiles", 0, "outgoing", 0, "coefficients", 0],
        ["geometry", "repair_tiles", 0, "outgoing", 0, "coefficients", 0],
        ["geometry", "coarse_response_scales", 0],
        ["geometry", "fine_response_scales", 0],
        ["generators", 0, "coefficients", 8],
    ]
    for key in (
        "coarse_observations",
        "fine_observations",
        "repair_observations",
        "coarse_targets",
        "fine_targets",
        "coarse_geometric",
    ):
        paths.append(["matrices", key, 0, 0])
    for key in (
        "generator_integrals",
        "constant_coarse_observations",
        "constant_fine_observations",
        "constant_repair_observations",
        "constant_coarse_targets",
        "constant_fine_targets",
    ):
        paths.append(["matrices", key, 0])
    for key in ("matrix", "predicted", "residuals"):
        paths.append(["repair", key, 0, 0])
    paths.append(["repair", "intercept", 0])
    for path in paths:
        yield changed_fraction(family, path)
    for name in ("coarse_observation_rows", "fine_observation_rows", "repair_observation_rows"):
        yield replaced(family, ["matrices", name, 0, "tile"], -1)
    for name in ("coarse_response_rows", "fine_response_rows"):
        yield replaced(family, ["matrices", name, 0, "first"], "wrong-source")
    for key in ("fine_tile", "coarse_tile"):
        yield replaced(family, ["geometry", "repair_tiles", 0, key], -1)
    yield replaced(family, ["geometry", "parents", 0, "parent"], "not-a-parent")
    yield replaced(family, ["geometry", "repair_tiles"], family["geometry"]["repair_tiles"][:-1])
    yield replaced(family, ["checks", "observation_additivity"], False)
    yield replaced(
        family, ["counts", "repair_moment_entries"], family["counts"]["repair_moment_entries"] + 1
    )
    yield replaced(family, ["repair", "exact"], False)
    for changed in certificate_mutations(family["certificate"]):
        yield replaced(family, ["certificate"], changed)
    repaired = family["repair"]["collision"]
    if repaired is None:
        yield replaced(family, ["repair", "collision"], {})
    else:
        for key in (
            "fine_observed_plus",
            "fine_observed_minus",
            "observed_plus",
            "observed_minus",
            "difference",
            "predicted_plus",
            "predicted_minus",
            "residual_plus",
            "residual_minus",
        ):
            yield changed_fraction(family, ["repair", "collision", key, 0])
        index = next(
            i
            for i, value in enumerate(repaired["normalized_truth_difference"])
            if value is not None
        )
        yield changed_fraction(
            family, ["repair", "collision", "normalized_truth_difference", index]
        )


def test_generic_complete_output_corruptions_are_nonvacuous(runner):
    count = 0
    for problem in (unit_problem(), overlay_problem()):
        wanted = expected(problem)
        for changed in family_mutations(wanted):
            assert wire(changed) != wire(wanted)
            with pytest.raises(ValueError):
                runner.verify_suite(changed, wanted)
            count += 1
    assert count > 100


def test_null_repair_witness_and_partial_decoder_corruptions(runner):
    wanted = expected(null_problem())
    paths = [
        ["geometry", "fine_response_scales", 0],
        ["matrices", "fine_targets", 0, 0],
        ["certificate", "row_decoders", 0, 0],
        ["certificate", "collision", "truth_difference", 0],
        ["repair", "collision", "residual_plus", 0],
    ]
    changed = [changed_fraction(wanted, path) for path in paths]
    changed.append(
        replaced(wanted, ["repair", "collision", "normalized_truth_difference", 0], fw(0))
    )
    for bad in changed:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)


BRIDGES = {
    "AQ_selected_families": ["grid", "warp"],
    "AQ_geometry_inputs_equal": True,
    "AQ_selected_geometry_equal": True,
    "AQ_sources_equal": True,
    "AQ_coarse_measurements_equal": True,
    "AQ_coarse_targets_equal": True,
    "AQ_geometric_map_equal": True,
    "AQ_source_sums_equal": True,
    "other_historical_mathematics_replayed": False,
    "older_executors_run": False,
}


def payload(families):
    result = []
    for family in families:
        matrices = family["matrices"]
        measurements = {
            key: matrices[key]
            for key in (
                "coarse_observation_rows",
                "fine_observation_rows",
                "repair_observation_rows",
                "coarse_observations",
                "fine_observations",
                "repair_observations",
            )
        }
        targets = {
            key: matrices[key]
            for key in (
                "coarse_response_rows",
                "fine_response_rows",
                "coarse_targets",
                "fine_targets",
            )
        }
        result.append(
            {
                "family": family["problem"]["family"],
                "input_bytes": len(wire(family["problem"])),
                "geometry_bytes": len(wire(family["geometry"])),
                "generator_bytes": len(wire(family["generators"])),
                "measurement_bytes": len(wire(measurements)),
                "target_bytes": len(wire(targets)),
                "certificate_bytes": len(wire(family["certificate"])),
                "repair_bytes": len(wire(family["repair"])),
                "native_family_bytes": len(wire(family)),
            }
        )
    return result


def expected_suite(families):
    return {
        "families": families,
        "prior_bridges": copy.deepcopy(BRIDGES),
        "payload_sizes": payload(families),
        "totals": {
            "families": len(families),
            **{key: sum(f["counts"][key] for f in families) for key in families[0]["counts"]},
        },
        "scope": dict.fromkeys(SCOPE, False),
    }


def synthetic_history(family):
    geometry = copy.deepcopy(
        {
            key: family["geometry"][key]
            for key in (
                "volume",
                "coarse_cells",
                "fine_cells",
                "parents",
                "coarse_tiles",
                "fine_tiles",
            )
        }
    )
    geometry["response_scales"] = copy.deepcopy(family["geometry"]["coarse_response_scales"])
    fields = {
        "observation_rows": "coarse_observation_rows",
        "response_rows": "coarse_response_rows",
        "observations": "coarse_observations",
        "targets": "coarse_targets",
        "generator_integrals": "generator_integrals",
        "constant_observations": "constant_coarse_observations",
        "constant_targets": "constant_coarse_targets",
    }
    return {
        "problem": {
            **copy.deepcopy(family["problem"]),
            "geometric": copy.deepcopy(family["matrices"]["coarse_geometric"]),
            "canonical_intercept": [fw(9)],
        },
        "geometry": geometry,
        "generators": copy.deepcopy(family["generators"]),
        "matrices": {
            key: copy.deepcopy(family["matrices"][value]) for key, value in fields.items()
        },
        "canonical": {"unselected": True},
    }


def independent_history_checks(families, previous):
    for current, old in zip(families, previous, strict=True):
        assert current["problem"] == {
            key: old["problem"][key]
            for key in (
                "family",
                "probe",
                "coarse_cells",
                "fine_cells",
                "coarse_tiles",
                "fine_tiles",
            )
        }
        projected = synthetic_history(current)
        assert projected["geometry"] == old["geometry"]
        assert projected["generators"] == old["generators"]
        for key, value in projected["matrices"].items():
            assert value == old["matrices"][key]
        assert current["matrices"]["coarse_geometric"] == old["problem"]["geometric"]


def test_synthetic_native_list_history_assembly_and_all_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(FAMILIES, (unit_problem, overlay_problem), strict=True):
        p = factory()
        p["family"] = name
        problems.append(p)
    families = list(map(expected, problems))
    previous = list(map(synthetic_history, families))
    by_name = {f["problem"]["family"]: f for f in families}
    wanted = expected_suite(families)

    # Only fixed inventory sizes are bypassed here, not the selected historical
    # geometry/source/matrix comparisons. Real projection is tested after release.
    def projected(old):
        return [
            {
                key: f["problem"][key]
                for key in (
                    "family",
                    "probe",
                    "coarse_cells",
                    "fine_cells",
                    "coarse_tiles",
                    "fine_tiles",
                )
            }
            for f in old
        ], old

    monkeypatch.setattr(runner, "project_inputs", projected)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    calls = []

    def engine(route):
        def build(p):
            assert set(p) == set(problems[0])
            calls.append((route, p["family"]))
            return copy.deepcopy(by_name[p["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", engine)
    independent_history_checks(families, previous)
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    for route, n in (("primary", 2), ("reference", 2), ("compare", 4)):
        calls.clear()
        assert wire(runner.run_suite(route)) == wire(wanted)
        assert len(calls) == n
    with pytest.raises(ValueError):
        runner.assemble_suite(families, tuple(previous))
    with pytest.raises(ValueError):
        runner.run_suite("unknown")

    def mutates(p):
        result = copy.deepcopy(by_name[p["family"]])
        p["family"] = "mutated"
        return result

    monkeypatch.setattr(runner, "load_engine", lambda route: SimpleNamespace(build_family=mutates))
    with pytest.raises(ValueError):
        runner.run_suite("primary")


def test_missing_and_broken_symlink_replay_are_readonly(lifecycle):
    runner, path = lifecycle
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    target = path.with_name("missing.json")
    path.symlink_to(target)
    with pytest.raises(FileExistsError):
        runner.capture(path)
    with pytest.raises(ValueError):
        runner.capture(path, verify=True)
    assert path.is_symlink() and not target.exists()


@pytest.fixture(scope="session")
def fixed_data(runner):
    problems, previous = runner.load_inputs()
    before = wire(problems)
    families = list(map(expected, problems))
    assert wire(problems) == before
    independent_history_checks(families, previous)
    return problems, previous, families, expected_suite(families)


@pytest.mark.parametrize("index", [0, 1])
def test_fixed_both_engines_match_complete_independent_integral_and_gram_oracle(
    engines, fixed_data, index
):
    problems, _, wanted, _ = fixed_data
    for engine in engines:
        p = copy.deepcopy(problems[index])
        before = wire(p)
        actual = engine.build_family(p)
        assert wire(p) == before
        assert wire(actual) == wire(wanted[index])
        assert wire(
            engine.certify(
                actual["matrices"]["coarse_observations"], actual["matrices"]["fine_targets"]
            )
        ) == wire(actual["certificate"])
        certificate_validity(
            actual["matrices"]["coarse_observations"],
            actual["matrices"]["fine_targets"],
            actual["certificate"],
        )
        if actual["certificate"]["collision"] is not None:
            for sign in ("plus", "minus"):
                witness = actual["repair"]["collision"]
                assert (
                    engine.apply(
                        actual["repair"]["intercept"],
                        actual["repair"]["matrix"],
                        witness["observed_" + sign],
                    )
                    == actual["certificate"]["collision"]["truth_" + sign]
                )


def test_fixed_complete_suite_payload_counts_and_historical_bridges(runner, fixed_data):
    problems, previous, families, wanted = fixed_data
    assert len(problems) == 2 and [p["family"] for p in problems] == list(FAMILIES)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    assert runner.payload_sizes(families) == payload(families)
    for p, family in zip(problems, families, strict=True):
        counts = family["counts"]
        assert len(p["coarse_cells"]) == 7 and len(p["fine_cells"]) == 8
        assert len(p["coarse_tiles"]) == 8 and len(p["fine_tiles"]) == 12
        assert counts["generators"] == 108
        assert counts["repair_tiles"] == len(overlay(p))
        assert counts["outgoing_entries"] == 4 * (8 * 7 + counts["repair_tiles"] * 8)
        assert counts["repair_moment_entries"] == 16 * counts["repair_tiles"]
        assert counts["raw_geometric_entries"] == 49 * 32 + 64 * (1 + 4 * counts["repair_tiles"])
    assert set(wanted["scope"]) == set(SCOPE) and not any(wanted["scope"].values())


@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_cached_orchestration_routes(runner, fixed_data, monkeypatch, route):
    _, _, families, wanted = fixed_data
    lookup = {family["problem"]["family"]: family for family in families}
    seen = []

    def load_cached(name):
        def build(problem):
            seen.append(name)
            assert problem == lookup[problem["family"]]["problem"]
            return copy.deepcopy(lookup[problem["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", load_cached)
    assert wire(runner.run_suite(route)) == wire(wanted)
    assert seen == (["primary", "reference"] * 2 if route == "compare" else [route] * 2)


def test_fixed_full_wire_and_suite_mutations_are_rejected(runner, fixed_data):
    _, _, families, wanted = fixed_data
    inventory = 0
    for family in families:
        for bad in family_mutations(family):
            assert wire(bad) != wire(family)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, family)
            inventory += 1
    suite_changes = [
        replaced(wanted, ["families"], list(reversed(families))),
        replaced(wanted, ["prior_bridges", "AQ_sources_equal"], False),
        replaced(wanted, ["prior_bridges", "older_executors_run"], True),
        replaced(
            wanted,
            ["payload_sizes", 0, "measurement_bytes"],
            wanted["payload_sizes"][0]["measurement_bytes"] + 1,
        ),
        replaced(wanted, ["totals", "generators"], wanted["totals"]["generators"] + 1),
        replaced(wanted, ["scope", "repair_minimality_proved"], True),
        replaced(wanted, ["scope", "physical_sources_established"], True),
        {**wanted, "extra": 0},
    ]
    for bad in suite_changes:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)
    assert inventory >= 100 and len(suite_changes) == 8


def test_fixed_selected_producer_changes_and_unselected_projection_boundary(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    paths = [
        [0, "problem", "probe", 0],
        [0, "geometry", "volume"],
        [0, "geometry", "coarse_tiles", 0, "moments", 15],
        [0, "geometry", "fine_tiles", 0, "moments", 15],
        [0, "geometry", "response_scales", 0],
        [0, "generators", 0, "coefficients", 8],
        [0, "matrices", "observations", 0, 0],
        [0, "matrices", "targets", 0, 0],
        [0, "problem", "geometric", 0, 0],
        [0, "matrices", "generator_integrals", 0],
        [0, "matrices", "constant_observations", 0],
        [0, "matrices", "constant_targets", 0],
    ]
    for path in paths:
        bad = changed_fraction(previous, path)
        assert wire(bad) != wire(previous)
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)
    # Historical origin is authenticated by the full artifact ledger, whereas the
    # selected mathematical bridge deliberately does not replay canonical failures.
    bad = copy.deepcopy(previous)
    bad[0]["decoders"][0]["residuals"][0][0] = fw(
        fraction(bad[0]["decoders"][0]["residuals"][0][0]) + 1
    )
    assert wire(bad) != wire(previous)
    projected, _ = runner.project_inputs(bad)
    assert projected == problems
    assert runner.historical_bridges(families, bad) == BRIDGES


def test_fixed_source_and_ancestor_identity_inventory(runner):
    identity = runner.identities()
    assert len(identity["source_ledger"]) == 5
    assert len(identity["prior_artifacts"]) == 48
    assert len(identity["ancestor_sources"]) == 59
    assert set(identity["source_ledger"]) == set(runner.SOURCES)
    raw = runner.plain_bytes(runner.AQ)
    assert len(raw) == 934498 and hashlib.sha256(raw).hexdigest() == (
        "c9c0bb0b20cd3646217e6ad97eaf2f41ca40406fc94d8fac975b67267eec6a08"
    )
    document = json.loads(raw)
    # Runtime floats are envelope metadata, not mathematical native-wire values.
    assert runner.canonical(document) == raw
    native(document["suite"])
    for collection, base in (
        (identity["source_ledger"], HERE),
        (identity["prior_artifacts"], HERE.parent),
        (identity["ancestor_sources"], HERE.parent),
    ):
        for path, wanted in collection.items():
            data = runner.plain_bytes(base / path)
            assert (
                len(data) == wanted["bytes"]
                and hashlib.sha256(data).hexdigest() == wanted["sha256"]
            )
