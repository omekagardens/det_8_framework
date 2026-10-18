"""Independent checks for the bounded frozen-map measurement stability diagnostic.

Only test names containing fixed consume authenticated AO cases. Collection and generic
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
        load("_qr05ap_test_primary", "kernel.py"),
        load("_qr05ap_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05ap_test_runner", "study.py")


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
UNIT = (F(0), F(1), F(0), F(1))
CHECKS = (
    "raw_response_identity",
    "coordinate_inverse",
    "normalized_response_identity",
    "witness_box",
    "witness_attainment",
    "complete_gain_partition",
)
SCOPE = (
    "empirical_noise_calibrated",
    "field_realizable_errors_required",
    "decoder_optimized",
    "canonical_policy_refitted",
    "source_span_expanded",
    "fine_response_stability_tested",
    "full_field_stability_tested",
    "unknown_geometry_reconstructed",
    "physical_sensor_validated",
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


def matrix(values):
    return [[fraction(v) for v in row] for row in values]


def zeros(rows, columns):
    return [[F() for _ in range(columns)] for _ in range(rows)]


def mm(left, right):
    return [
        [
            sum((x * y for x, y in zip(row, col, strict=True)), F())
            for col in zip(*right, strict=True)
        ]
        for row in left
    ]


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), F())


def basis_change(sx, sy, tx, ty):
    """Polynomial binomial substitution, not corner fitting or matrix inversion."""
    return [
        [
            F(comb(i, p) * comb(j, q)) * tx ** (i - p) * ty ** (j - q) * sx**p * sy**q
            if p <= i and q <= j
            else F()
            for p, q in BASIS
        ]
        for i, j in BASIS
    ]


def blocks(probe, tile_bounds):
    volume = area(probe)
    ts, ks = [], []
    identity = [[F(i == j) for j in range(4)] for i in range(4)]
    for a, b, c, d in tile_bounds:
        forward = basis_change(b - a, d - c, a, c)
        backward = basis_change(1 / (b - a), 1 / (d - c), -a / (b - a), -c / (d - c))
        scalar = volume**2 * area((a, b, c, d))
        t = [[scalar * x for x in row] for row in forward]
        k = [[x / scalar for x in row] for row in backward]
        assert mm(t, k) == identity == mm(k, t)
        ts.append(t)
        ks.append(k)
    return ts, ks


def dense(problem):
    m = len(problem["observations"])
    q = len(problem["targets"])
    intercept, linear = [F()] * q, zeros(q, m)
    for j, row in enumerate(matrix(problem["canonical"]["decoder"])):
        for index, value in zip(problem["canonical"]["row_basis"], row, strict=True):
            if index == 0:
                intercept[j] = value
            else:
                linear[j][index - 1] = value
    return intercept, linear


def expected(problem):
    """Full wire from polynomial coordinate substitution and literal products.

    Generic corner tests below independently check sharpness, rather than
    treating the row absolute-sum formula as its own verification.
    """
    native(problem)
    probe = tuple(map(fraction, problem["probe"]))
    cells = problem["cells"]
    ids = [c["event"] for c in cells]
    bounds = [None if c["bounds"] is None else tuple(map(fraction, c["bounds"])) for c in cells]
    tile_bounds = [tuple(map(fraction, t["bounds"])) for t in problem["tiles"]]
    assert ids == sorted(set(ids))
    partition_of(probe, [b for b in bounds if b is not None])
    for index, event in enumerate(ids):
        owned = [
            b for t, b in zip(problem["tiles"], tile_bounds, strict=True) if t["event"] == event
        ]
        if bounds[index] is None:
            assert owned == []
        else:
            partition_of(bounds[index], owned)
    volume = area(probe)
    hs = [F() if b is None else area(b) for b in bounds]
    ht = [area(b) for b in tile_bounds]
    scales = [volume**2 * x * y for x in hs for y in hs]
    raw_o, raw_q = matrix(problem["observations"]), matrix(problem["targets"])
    m, q, n = len(raw_o), len(raw_q), len(raw_o[0])
    tblocks, kblocks = blocks(probe, tile_bounds)
    z = [row for i, k in enumerate(kblocks) for row in mm(k, raw_o[4 * i : 4 * i + 4])]
    y = [None if not s else [x / s for x in row] for row, s in zip(raw_q, scales, strict=True)]
    policies = [
        ("canonical", *dense(problem)),
        ("geometric", [F()] * q, matrix(problem["geometric"])),
    ]
    decoders = []
    for name, raw_a, raw_l in policies:
        assert [
            [a + dot(row, column) for column in zip(*raw_o, strict=True)]
            for a, row in zip(raw_a, raw_l, strict=True)
        ] == raw_q
        assert all(s or all(x == 0 for x in row) for s, row in zip(scales, raw_q, strict=True))
        intercept = [a / s if s else None for a, s in zip(raw_a, scales, strict=True)]
        linear = [
            None
            if not s
            else [x / s for i, t in enumerate(tblocks) for x in mm([row[4 * i : 4 * i + 4]], t)[0]]
            for row, s in zip(raw_l, scales, strict=True)
        ]
        assert [
            None if row is None else [a + dot(row, col) for col in zip(*z, strict=True)]
            for a, row in zip(intercept, linear, strict=True)
        ] == y
        gains, witnesses = [], []
        for j, row in enumerate(linear):
            if row is None:
                gains.append(None)
                witnesses.append(None)
                continue
            positive = sum((x for x in row if x > 0), F())
            negative = sum((x for x in row if x < 0), F())
            gain = positive - negative
            signs = [int(x > 0) - int(x < 0) for x in row]
            output = [None if other is None else dot(other, signs) for other in linear]
            assert output[j] == gain
            gains.append(gain)
            witnesses.append({"signs": signs, "output": output, "attained": output[j]})
        maximum = max(g for g in gains if g is not None)
        decoders.append(
            {
                "name": name,
                "raw_intercept": raw_a,
                "raw_matrix": raw_l,
                "intercept": intercept,
                "matrix": linear,
                "row_gains": gains,
                "witnesses": witnesses,
                "max_gain": maximum,
                "max_rows": [j for j, g in enumerate(gains) if g == maximum],
            }
        )
    differences = [
        None if a is None else a - b
        for a, b in zip(decoders[0]["row_gains"], decoders[1]["row_gains"], strict=True)
    ]
    comparison = {
        "gain_difference": differences,
        "canonical_lower_rows": [j for j, d in enumerate(differences) if d is not None and d < 0],
        "geometric_lower_rows": [j for j, d in enumerate(differences) if d is not None and d > 0],
        "tied_rows": [j for j, d in enumerate(differences) if d == 0],
        "undefined_rows": [j for j, d in enumerate(differences) if d is None],
    }
    defined = sum(bool(s) for s in scales)
    counts = {
        "cells": len(cells),
        "positive_cells": sum(bool(h) for h in hs),
        "tiles": len(ht),
        "generators": n,
        "observations": m,
        "responses": q,
        "defined_responses": defined,
        "undefined_responses": q - defined,
        "transform_entries": sum(len(row) for b in tblocks + kblocks for row in b),
        "dimensionless_observation_entries": sum(map(len, z)),
        "dimensionless_target_entries": sum(len(row) for row in y if row is not None),
        "raw_decoder_entries": sum(
            len(d["raw_intercept"]) + sum(map(len, d["raw_matrix"])) for d in decoders
        ),
        "normalized_decoder_entries": sum(
            sum(x is not None for x in d["intercept"])
            + sum(len(row) for row in d["matrix"] if row is not None)
            for d in decoders
        ),
        "gain_entries": sum(sum(x is not None for x in d["row_gains"]) for d in decoders),
        "witnesses": sum(sum(w is not None for w in d["witnesses"]) for d in decoders),
        "witness_sign_entries": sum(
            len(w["signs"]) for d in decoders for w in d["witnesses"] if w is not None
        ),
        "witness_output_entries": sum(
            sum(x is not None for x in w["output"])
            for d in decoders
            for w in d["witnesses"]
            if w is not None
        ),
        "maximizing_rows": sum(len(d["max_rows"]) for d in decoders),
        **{
            k: len(comparison[k])
            for k in ("canonical_lower_rows", "geometric_lower_rows", "tied_rows")
        },
    }
    return encode(
        {
            "problem": copy.deepcopy(problem),
            "geometry": {
                "volume": volume,
                "cell_volumes": hs,
                "tile_volumes": ht,
                "response_rows": [{"first": a, "second": b} for a in ids for b in ids],
                "response_scales": scales,
            },
            "coordinates": {
                "raw_from_local": tblocks,
                "local_from_raw": kblocks,
                "observations": z,
                "targets": y,
            },
            "decoders": decoders,
            "comparison": comparison,
            "checks": dict.fromkeys(CHECKS, True),
            "counts": counts,
        }
    )


def unit_problem():
    return {
        "family": "unit-intercept",
        "probe": rect(UNIT),
        "cells": [{"event": -4, "bounds": rect(UNIT)}],
        "tiles": [{"event": -4, "bounds": rect(UNIT)}],
        "observations": [[fw(F(1, d))] for d in (288, 384, 384, 512)],
        "targets": [[fw(F(1, 9216))]],
        "canonical": {"row_basis": [0], "decoder": [[fw(F(1, 9216))]]},
        "geometric": [list(map(fw, (F(1, 2), -F(1, 2), -F(1, 2), F(1, 2))))],
    }


def signed_problem(all_zero=False):
    probe = tuple(map(F, (-2, 1, 1, 3)))
    cells = [
        {"event": -2, "bounds": rect((-2, -1, 1, 3))},
        {"event": 0, "bounds": None},
        {"event": 9, "bounds": rect((-1, 1, 1, 3))},
    ]
    hs = [F(1), F(), F(2)]
    _, ks = blocks(probe, [tuple(map(F, (-2, -1, 1, 3))), tuple(map(F, (-1, 1, 1, 3)))])
    scales = [area(probe) ** 2 * a * b for a in hs for b in hs]
    desired = [zeros(9, 8), zeros(9, 8)]
    if not all_zero:
        desired[0][0][:2] = [F(2), F(-3)]
        desired[0][2][:2] = [F(-2), F(3)]
        desired[0][8][0] = F(1)
        desired[1][0][0] = F(1)
        desired[1][2][:2] = [F(-2), F(3)]
        desired[1][6][:2] = [F(1), F(-1)]
        desired[1][8][1] = F(1)
    maps = []
    for policy in desired:
        raw = []
        for j, (row, s) in enumerate(zip(policy, scales, strict=True)):
            raw.append(
                [s * x for t, k in enumerate(ks) for x in mm([row[4 * t : 4 * t + 4]], k)[0]]
                if s
                else [F(j + 1), F(-j - 1), *[F()] * 6]
            )
        maps.append(raw)
    return encode(
        {
            "family": "signed-null",
            "probe": list(probe),
            "cells": cells,
            "tiles": [copy.deepcopy(cells[0]), copy.deepcopy(cells[2])],
            "observations": zeros(8, 2),
            "targets": zeros(9, 2),
            "canonical": {"row_basis": list(range(9)), "decoder": [[F(), *row] for row in maps[0]]},
            "geometric": maps[1],
        }
    )


def split_problem():
    p = unit_problem()
    p["family"] = "two-unequal-tiles"
    p["tiles"] = [
        {"event": -4, "bounds": rect((0, F(1, 3), 0, 1))},
        {"event": -4, "bounds": rect((F(1, 3), 1, 0, 1))},
    ]
    p["observations"] = encode(zeros(8, 1))
    p["targets"] = [[fw(0)]]
    p["canonical"] = {"row_basis": [0], "decoder": [[fw(0)]]}
    p["geometric"] = encode(zeros(1, 8))
    return p


def affine_problem(problem, alpha, beta, shift_u, shift_v):
    """Transport the SAME maps; never solve or select a new decoder."""
    p = copy.deepcopy(problem)
    alpha, beta, shift_u, shift_v = map(F, (alpha, beta, shift_u, shift_v))
    k = alpha * beta
    assert alpha > 0 and beta > 0
    transform = [[k**3 * x for x in row] for row in basis_change(alpha, beta, shift_u, shift_v)]
    inverse = [
        [x / k**3 for x in row]
        for row in basis_change(1 / alpha, 1 / beta, -shift_u / alpha, -shift_v / beta)
    ]

    def moved(bounds):
        if bounds is None:
            return None
        a, b, c, d = map(fraction, bounds)
        return rect(
            (alpha * a + shift_u, alpha * b + shift_u, beta * c + shift_v, beta * d + shift_v)
        )

    p["probe"] = moved(p["probe"])
    for cell in p["cells"] + p["tiles"]:
        cell["bounds"] = moved(cell["bounds"])
    o = matrix(problem["observations"])
    p["observations"] = encode(
        [row for t in range(len(problem["tiles"])) for row in mm(transform, o[4 * t : 4 * t + 4])]
    )
    p["targets"] = encode([[k**4 * x for x in row] for row in matrix(problem["targets"])])
    a, linear = dense(problem)
    m = len(o)
    assert m + 1 <= 64

    def transported(rows):
        return [
            [
                k**4 * x
                for t in range(len(problem["tiles"]))
                for x in mm([row[4 * t : 4 * t + 4]], inverse)[0]
            ]
            for row in rows
        ]

    p["canonical"] = {
        "row_basis": list(range(m + 1)),
        "decoder": encode(
            [[k**4 * x, *row] for x, row in zip(a, transported(linear), strict=True)]
        ),
    }
    p["geometric"] = encode(transported(matrix(problem["geometric"])))
    return p


@pytest.mark.parametrize(
    "factory", [unit_problem, signed_problem, split_problem, lambda: signed_problem(True)]
)
def test_generic_complete_wire(engines, factory):
    p = factory()
    want = expected(p)
    before = wire(p)
    for engine in engines:
        assert wire(engine.build_family(p)) == wire(want)
        assert wire(p) == before


def test_exact_normalization_intercept_not_noisy_and_no_clipping(engines):
    want = expected(unit_problem())
    for engine in engines:
        result = engine.build_family(unit_problem())
        assert wire(result) == wire(want)
        canonical, geometric = result["decoders"]
        assert canonical["intercept"] == [fw(F(1, 576))]
        assert canonical["row_gains"] == [fw(0)]
        assert geometric["matrix"] == [list(map(fw, (1, -1, -1, 1)))]
        assert geometric["row_gains"] == [fw(4)]
        z = [row[0] for row in result["coordinates"]["observations"]]
        assert engine.apply(canonical["intercept"], canonical["matrix"], z) == [fw(F(1, 576))]
        assert engine.apply(geometric["intercept"], geometric["matrix"], z) == [fw(F(1, 576))]
        assert geometric["witnesses"][0]["output"] == [fw(4)]
        assert canonical["witnesses"][0]["output"] == [fw(0)]
        assert engine.apply(
            geometric["intercept"], geometric["matrix"], list(map(fw, (-1, 1, 1, -1)))
        ) == [fw(-4)]
        # Raw-coordinate unit errors give gain 2 in unnormalized U units.
        raw_gain = sum(abs(x) for x in matrix(geometric["raw_matrix"])[0])
        assert raw_gain == 2
        # For the SAME normalized y, that raw-coordinate box has gain 32,
        # distinct from the dimensionless local-coordinate box's gain 4.
        assert raw_gain / fraction(result["geometry"]["response_scales"][0]) == 32


def test_all_signs_full_outputs_null_rows_and_ties(engines):
    for engine in engines:
        result = engine.build_family(signed_problem())
        c, g = result["decoders"]
        assert c["max_rows"] == [0, 2] and g["max_rows"] == [2]
        assert c["witnesses"][0] == {
            "signs": [1, -1, 0, 0, 0, 0, 0, 0],
            "output": [fw(5), None, fw(-5), None, None, None, fw(0), None, fw(1)],
            "attained": fw(5),
        }
        assert c["witnesses"][6]["signs"] == [0] * 8
        assert c["witnesses"][6]["output"] == [
            fw(0) if j in (0, 2, 6, 8) else None for j in range(9)
        ]
        assert result["comparison"] == {
            "gain_difference": [fw(4), None, fw(0), None, None, None, fw(-2), None, fw(0)],
            "canonical_lower_rows": [6],
            "geometric_lower_rows": [0],
            "tied_rows": [2, 8],
            "undefined_rows": [1, 3, 4, 5, 7],
        }
        for j in (1, 3, 4, 5, 7):
            assert any(fraction(x) for x in c["raw_matrix"][j])
            assert c["matrix"][j] is None and result["coordinates"]["targets"][j] is None
        zero = engine.build_family(signed_problem(True))
        for decoder in zero["decoders"]:
            assert decoder["max_gain"] == fw(0) and decoder["max_rows"] == [0, 2, 6, 8]


@pytest.mark.parametrize("factory", [unit_problem, signed_problem])
def test_exact_small_box_corner_extrema_and_epsilon(engines, factory):
    result = expected(factory())
    for decoder in result["decoders"]:
        rows = [None if r is None else list(map(fraction, r)) for r in decoder["matrix"]]
        corners = list(product((F(-1), F(1)), repeat=len(factory()["observations"])))
        for j, row in enumerate(rows):
            if row is None:
                continue
            values = [dot(row, corner) for corner in corners]
            gain = fraction(decoder["row_gains"][j])
            assert max(values) == gain and min(values) == -gain
            for epsilon in (F(), F(1, 7), F(3, 2)):
                assert max(epsilon * v for v in values) == epsilon * gain
            for engine in engines:
                witness = decoder["witnesses"][j]
                error = engine.apply(
                    [None if r is None else fw(0) for r in rows],
                    decoder["matrix"],
                    list(map(fw, witness["signs"])),
                )
                assert error == witness["output"]


@pytest.mark.parametrize("factory", [unit_problem, signed_problem, split_problem])
@pytest.mark.parametrize("transform", [(F(2), F(1, 2), F(-3), F(5)), (F(3), F(2), F(-2), F(1))])
def test_complete_affine_transport_same_dense_frozen_map(engines, factory, transform):
    p = factory()
    moved = affine_problem(p, *transform)
    before = expected(p)
    want = expected(moved)
    assert moved["canonical"]["row_basis"] == list(range(len(p["observations"]) + 1))
    assert moved["canonical"] != p["canonical"]
    for key in ("observations", "targets"):
        assert want["coordinates"][key] == before["coordinates"][key]
    for a, b in zip(want["decoders"], before["decoders"], strict=True):
        for key in ("intercept", "matrix", "row_gains", "witnesses", "max_gain", "max_rows"):
            assert a[key] == b[key]
    assert want["comparison"] == before["comparison"]
    for engine in engines:
        assert wire(engine.build_family(moved)) == wire(want)


def test_restricted_apply_uses_only_supplied_affine_map(engines, monkeypatch):
    def forbidden(*args, **kwargs):
        raise RuntimeError("off-contract access")

    for engine in engines:
        monkeypatch.setattr(engine, "build_family", forbidden)
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            assert engine.apply(
                [fw(F(3, 2)), None],
                [[fw(2), fw(-1), fw(0), fw(1)], None],
                list(map(fw, (2, 5, 8, -3))),
            ) == [fw(F(-5, 2)), None]
    # No field-realizability or model semantics are authenticated by apply.


def test_native_sharing_and_output_detachment(engines):
    p = unit_problem()
    p["tiles"][0]["bounds"] = p["cells"][0]["bounds"] = p["probe"]
    for engine in engines:
        before = wire(p)
        result = engine.build_family(p)
        want = wire(result)
        assert wire(p) == before
        result["problem"]["probe"][0][0] = 77
        assert wire(p) == before
        result = engine.build_family(p)
        result["decoders"][0]["raw_matrix"][0][0][0] = 19
        assert wire(engine.build_family(p)) == want
        b, mat, z = [fw(3)], [[fw(1)] * 4], [fw(2)] * 4
        snapshots = [wire(v) for v in (b, mat, z)]
        output = engine.apply(b, mat, z)
        output[0][0] = 99
        assert snapshots == [wire(v) for v in (b, mat, z)]


def test_tiny_positive_is_not_zero_and_unretained_cancellation(engines):
    d = 1 << 4095
    tiny = F(1, d)
    p = unit_problem()
    p["observations"] = encode(zeros(4, 1))
    p["targets"] = [[fw(0)]]
    p["canonical"] = {"row_basis": [0], "decoder": [[fw(0)]]}
    p["geometric"] = [[fw(tiny), fw(0), fw(0), fw(0)]]
    for engine in engines:
        result = engine.build_family(p)
        # T/s =2 for the unit single-cell geometry.
        assert result["decoders"][1]["row_gains"] == [fw(2 * tiny)]
        assert result["comparison"]["canonical_lower_rows"] == [0]
        assert engine.apply(
            [fw(0)], [[fw(d), fw(-d), fw(0), fw(0)]], list(map(fw, (2, 2, 0, 0)))
        ) == [fw(0)]
        with pytest.raises(ValueError):
            engine.apply([fw(0)], [[fw(d), fw(0), fw(0), fw(0)]], list(map(fw, (2, 0, 0, 0))))


class ListSubclass(list):
    pass


class DictSubclass(dict):
    pass


class IntSubclass(int):
    pass


def invalid_families():
    p = unit_problem()
    signed, split = signed_problem(), split_problem()
    problems = [
        None,
        [],
        DictSubclass(p),
        {**p, "extra": 0},
        {k: v for k, v in p.items() if k != "geometric"},
        {**p, "family": ""},
        {**p, "family": 1},
        replaced(p, ("cells",), ListSubclass(p["cells"])),
        replaced(p, ("probe", 0), [0.0, 1]),
        replaced(p, ("probe", 0), [False, 1]),
        replaced(p, ("probe", 0), [IntSubclass(0), 1]),
        replaced(p, ("probe", 0), [0, -1]),
        replaced(p, ("probe", 1), [2, 2]),
        replaced(p, ("probe", 1), [1 << 4096, 1]),
        replaced(p, ("probe",), rect((0, 0, 0, 1))),
        replaced(p, ("cells",), []),
        replaced(p, ("cells",), p["cells"] * 9),
        replaced(p, ("cells", 0, "event"), True),
        replaced(signed, ("cells",), signed["cells"][::-1]),
        replaced(signed, ("cells", 2, "event"), -2),
        replaced(p, ("cells", 0, "bounds"), None),
        replaced(p, ("cells", 0, "bounds"), rect((0, F(1, 2), 0, 1))),
        replaced(p, ("cells", 0, "bounds"), rect((-1, 1, 0, 1))),
        replaced(signed, ("cells", 2, "bounds"), rect((-2, 1, 1, 3))),
        replaced(p, ("tiles",), []),
        replaced(p, ("tiles",), p["tiles"] * 65),
        replaced(p, ("tiles", 0, "event"), 99),
        replaced(signed, ("tiles", 0, "event"), 0),
        replaced(p, ("tiles", 0, "bounds"), None),
        replaced(p, ("tiles", 0, "bounds"), rect((0, 0, 0, 1))),
        replaced(p, ("tiles", 0, "bounds"), rect((-1, 1, 0, 1))),
        replaced(split, ("tiles",), split["tiles"][::-1]),
        replaced(split, ("tiles", 0, "bounds"), rect((0, F(1, 2), 0, 1))),
        replaced(split, ("tiles", 0, "bounds"), rect((0, F(1, 4), 0, 1))),
        replaced(p, ("observations",), []),
        replaced(p, ("observations",), p["observations"][:-1]),
        replaced(p, ("observations", 3), []),
        replaced(p, ("observations",), [[fw(0)] * 65] * 4),
        replaced(p, ("observations", 3, 0), F(1, 512)),
        replaced(p, ("targets",), []),
        replaced(p, ("targets", 0), [fw(0), fw(0)]),
        replaced(p, ("targets", 0, 0), fw(0)),
        replaced(signed, ("targets", 1, 1), fw(1)),
        replaced(p, ("canonical",), {**p["canonical"], "extra": 0}),
        replaced(p, ("canonical", "row_basis"), []),
        replaced(p, ("canonical", "row_basis"), [1]),
        replaced(p, ("canonical", "row_basis"), [0, 0]),
        replaced(p, ("canonical", "row_basis"), [0, 5]),
        replaced(p, ("canonical", "row_basis"), [False]),
        replaced(p, ("canonical", "row_basis"), list(range(65))),
        replaced(signed, ("canonical", "row_basis"), [0, 2, 1, *range(3, 9)]),
        replaced(p, ("canonical", "decoder"), []),
        replaced(p, ("canonical", "decoder", 0), []),
        replaced(p, ("canonical", "decoder", 0, 0), fw(1)),
        replaced(p, ("geometric",), []),
        replaced(p, ("geometric", 0), [fw(0)] * 3),
        replaced(p, ("geometric", 0, 3), fw(0)),
    ]
    # The last target column must be checked, not merely the first generator.
    late = copy.deepcopy(p)
    late["observations"] = [row * 2 for row in late["observations"]]
    late["targets"] = [row * 2 for row in late["targets"]]
    late["observations"][3][1] = fw(0)
    problems.append(late)
    return problems


def valid_apply():
    return ([fw(1), None], [[fw(1), fw(-2), fw(0), fw(3)], None], list(map(fw, (2, 1, 3, 4))))


def invalid_applications():
    b, m, z = valid_apply()
    return [
        (None, m, z),
        ([], [], z),
        (b[:-1], m, z),
        (b, m[:-1], z),
        (b, m, []),
        (b, m, z[:-1]),
        (b, m, z * 65),
        (b * 33, m * 33, z),
        (ListSubclass(b), m, z),
        (b, ListSubclass(m), z),
        (b, m, tuple(z)),
        (b, m, ListSubclass(z)),
        ([fw(1), fw(0)], m, z),
        (b, [m[0], m[0]], z),
        ([None, None], m, z),
        (b, [m[0][:-1], None], z),
        (b, [tuple(m[0]), None], z),
        ([True, None], m, z),
        ([[1, False], None], m, z),
        ([fw(1), None], [m[0], None], [0.0, *z[1:]]),
        (b, m, [[2, 2], *z[1:]]),
        (b, m, [[1, 0], *z[1:]]),
        (b, m, [[1 << 4096, 1], *z[1:]]),
        (b, m, [[IntSubclass(1), 1], *z[1:]]),
    ]


@pytest.mark.parametrize("route", [0, 1])
def test_complete_schema_and_native_rejection_inventory(engines, route):
    engine = engines[route]
    problems = invalid_families()
    for p in problems:
        with pytest.raises(ValueError):
            engine.build_family(p)
    for args in invalid_applications():
        with pytest.raises(ValueError):
            engine.apply(*args)
    assert len(problems) == 58
    assert len(invalid_applications()) == 24


def test_empty_rows_raw_cancellation_and_generic_basis_are_admitted(engines):
    p = signed_problem()
    # Every supplied observation row is dependent. This API validates response
    # identity, not generic basis independence or AO canonical provenance.
    assert len(set(map(tuple, matrix(p["observations"])))) == 1
    for engine in engines:
        assert wire(engine.build_family(p)) == wire(expected(p))
        assert engine.apply([None], [None], [fw(7)] * 4) == [None]


def test_retained_normalized_map_overflow_is_rejected(engines):
    p = unit_problem()
    p["observations"] = encode(zeros(4, 1))
    p["targets"] = [[fw(0)]]
    p["canonical"] = {"row_basis": [0], "decoder": [[fw(0)]]}
    p["geometric"] = [[fw(1 << 4095), fw(0), fw(0), fw(0)]]
    for engine in engines:
        with pytest.raises(ValueError):
            engine.build_family(p)


def test_full_api_needs_no_hidden_input_files(engines, monkeypatch):
    p = signed_problem()
    want = wire(expected(p))

    def forbidden(*args, **kwargs):
        raise RuntimeError("hidden file access")

    for engine in engines:
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            assert wire(engine.build_family(p)) == want


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_isolated_guards_survive_optimized_python(tmp_path, optimized):
    program = r"""
import importlib.util
import sys
from pathlib import Path
here = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ap_guard_fixtures", here/"test_qr05ap.py")
test = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test)
count = 0
def reject(fn, *args):
    global count
    try:
        fn(*args)
    except ValueError:
        count += 1
    else:
        raise RuntimeError("explicit ValueError guard missing")
for filename in ("kernel.py", "reference.py"):
    spec = importlib.util.spec_from_file_location("ap_guard_"+filename[:-3], here/filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for problem in test.invalid_families():
        reject(module.build_family, problem)
    for args in test.invalid_applications():
        reject(module.apply, *args)
    d = 1 << 4095
    got = module.apply([test.fw(0)], [[test.fw(d),test.fw(-d),test.fw(0),test.fw(0)]],
                       list(map(test.fw,(2,2,0,0))))
    if got != [test.fw(0)]:
        raise RuntimeError("unretained cancellation rejected or changed")
    reject(module.apply,[test.fw(0)],[[test.fw(d),test.fw(0),test.fw(0),test.fw(0)]],
           list(map(test.fw,(2,0,0,0))))
    got = module.build_family(test.unit_problem())
    if got["decoders"][1]["row_gains"] != [test.fw(4)]:
        raise RuntimeError("valid hand changed under optimization")
if count != 166:
    raise RuntimeError("guard inventory changed: "+str(count))
print(count)
"""
    args = [sys.executable, "-I"]
    if optimized:
        args.append("-O")
    args += ["-X", f"pycache_prefix={tmp_path / 'bytecode'}", "-c", program, str(HERE)]
    completed = subprocess.run(
        args,
        cwd=tmp_path,
        env={**os.environ, "PYTHONHASHSEED": "0"},
        capture_output=True,
        text=True,
        check=True,
    )
    assert completed.stdout.strip() == "166"


def family_mutations(good):
    """One mutation per materially distinct retained claim, guaranteed non-noop."""
    q = good["counts"]["responses"]
    defined = [j for j, s in enumerate(good["geometry"]["response_scales"]) if fraction(s)]
    j = defined[0]
    scalar_paths = [
        ("problem", "observations", 0, 0),
        ("problem", "targets", j, 0),
        ("problem", "canonical", "decoder", j, 0),
        ("problem", "geometric", j, 0),
        ("geometry", "volume"),
        ("geometry", "cell_volumes", 0),
        ("geometry", "tile_volumes", 0),
        ("geometry", "response_scales", j),
        ("coordinates", "raw_from_local", 0, 0, 0),
        ("coordinates", "local_from_raw", 0, 0, 0),
        ("coordinates", "observations", 0, 0),
        ("coordinates", "targets", j, 0),
        ("decoders", 0, "raw_intercept", j),
        ("decoders", 0, "raw_matrix", j, 0),
        ("decoders", 0, "intercept", j),
        ("decoders", 0, "matrix", j, 0),
        ("decoders", 0, "row_gains", j),
        ("decoders", 0, "witnesses", j, "output", defined[-1]),
        ("decoders", 0, "witnesses", j, "attained"),
        ("decoders", 0, "max_gain"),
        ("comparison", "gain_difference", j),
    ]
    mutations = []
    for path in scalar_paths:
        value = good
        for part in path:
            value = value[part]
        mutations.append(replaced(good, path, fw(fraction(value) + 1)))
    signs = good["decoders"][0]["witnesses"][j]["signs"]
    mutations += [
        replaced(good, ("decoders", 0, "witnesses", j, "signs", 0), 0 if signs[0] else 1),
        replaced(good, ("decoders", 0, "max_rows"), []),
        replaced(
            good,
            ("geometry", "response_rows", j, "first"),
            good["geometry"]["response_rows"][j]["first"] + 1,
        ),
        replaced(good, ("checks", "witness_attainment"), False),
        replaced(
            good, ("counts", "witness_output_entries"), good["counts"]["witness_output_entries"] + 1
        ),
        replaced(good, ("comparison", "undefined_rows"), list(range(q))),
    ]
    assert all(wire(bad) != wire(good) for bad in mutations)
    return mutations


def test_nonvacuous_complete_family_and_null_corruptions(runner):
    good = expected(signed_problem())
    mutations = family_mutations(good)
    mutations += [
        replaced(good, ("coordinates", "targets", 1), [fw(0), fw(0)]),
        replaced(good, ("decoders", 0, "matrix", 1), [fw(0)] * 8),
        replaced(
            good,
            ("decoders", 0, "witnesses", 1),
            {"signs": [0] * 8, "output": [fw(0)] * 9, "attained": fw(0)},
        ),
        replaced(good, ("decoders", 0, "witnesses", 0, "output", 1), fw(0)),
    ]
    assert len(mutations) == 31
    for bad in mutations:
        assert wire(bad) != wire(good)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, good)


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


def test_lower_worst_case_gain_is_not_pointwise_error_dominance(engines):
    for engine in engines:
        result = engine.build_family(signed_problem())
        c, g = result["decoders"]
        assert fraction(c["row_gains"][0]) > fraction(g["row_gains"][0])
        # Higher-gain canonical cancels on one admissible error direction.
        first = list(map(fw, (F(1), F(2, 3), 0, 0, 0, 0, 0, 0)))
        # Lower-gain geometric cancels on a different admissible direction.
        second = list(map(fw, (0, 1, 0, 0, 0, 0, 0, 0)))
        zero_b = [fw(0) if row is not None else None for row in c["matrix"]]
        assert engine.apply(zero_b, c["matrix"], first)[0] == fw(0)
        assert engine.apply(zero_b, g["matrix"], first)[0] == fw(1)
        assert engine.apply(zero_b, c["matrix"], second)[0] == fw(-3)
        assert engine.apply(zero_b, g["matrix"], second)[0] == fw(0)


def test_apply_admits_maximum_shape_and_all_null_rows(engines):
    for engine in engines:
        z = [fw(F(1, 3))] * 256
        assert engine.apply([fw(1)] * 64, [[fw(0)] * 256] * 64, z) == [fw(1)] * 64
        assert engine.apply([None] * 64, [None] * 64, z) == [None] * 64


def projected_inputs(previous):
    """Only the documented inherited AO maps, no historical arithmetic replay."""
    answer = []
    assert [f["problem"]["family"] for f in previous] == list(FAMILIES)
    for f in previous:
        p, g, m = f["problem"], f["geometry"], f["matrices"]
        cert = next(
            row["certificate"]
            for row in f["certificates"]
            if row["observation"] == "weighted" and row["target"] == "coarse"
        )
        answer.append(
            copy.deepcopy(
                {
                    "family": p["family"],
                    "probe": p["probe"]["bounds"],
                    "cells": [
                        {"event": c["event"], "bounds": c["bounds"]} for c in g["coarse_cells"]
                    ],
                    "tiles": [
                        {"event": t["event"], "bounds": t["bounds"]} for t in g["coarse_tiles"]
                    ],
                    "observations": next(
                        row["matrix"] for row in m["observations"] if row["name"] == "weighted"
                    ),
                    "targets": next(
                        row["matrix"] for row in m["targets"] if row["name"] == "coarse"
                    ),
                    "canonical": {key: cert[key] for key in ("row_basis", "decoder")},
                    "geometric": m["coarse_decoder"],
                }
            )
        )
    return answer


def expected_suite(families):
    return {
        "families": copy.deepcopy(families),
        "prior_bridges": {
            "AO_selected_families": list(FAMILIES),
            "AO_selected_inputs_equal": True,
            "AO_frozen_decoders_consumed": True,
            "AO_selected_response_identities_rechecked": True,
            "AO_other_mathematics_replayed": False,
            "older_executors_run": False,
        },
        "payload_sizes": [
            {
                "family": f["problem"]["family"],
                "input_bytes": len(wire(f["problem"])),
                "geometry_bytes": len(wire(f["geometry"])),
                "coordinate_bytes": len(wire(f["coordinates"])),
                "decoder_bytes": len(wire(f["decoders"])),
                "comparison_bytes": len(wire(f["comparison"])),
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


@pytest.fixture(scope="session")
def fixed_bundle(runner, engines):
    """Lazy: this body never executes in collection or -k 'not fixed'."""
    problems, previous = runner.load_inputs()
    own_inputs = projected_inputs(previous)
    assert wire(problems) == wire(own_inputs)
    original = wire(problems)
    wants = [expected(p) for p in own_inputs]
    actual = [[engine.build_family(copy.deepcopy(p)) for p in problems] for engine in engines]
    assert wire(problems) == original
    return problems, previous, wants, actual


@pytest.mark.parametrize("family_index", [0, 1])
def test_fixed_complete_two_engine_wire_and_online_responses(fixed_bundle, engines, family_index):
    problems, _, wants, actual = fixed_bundle
    p = problems[family_index]
    want = wants[family_index]
    for index, engine in enumerate(engines):
        got = actual[index][family_index]
        assert wire(got) == wire(want)
        z = matrix(got["coordinates"]["observations"])
        targets = [
            None if row is None else list(map(fraction, row))
            for row in got["coordinates"]["targets"]
        ]
        n = len(z[0])
        for weights in ([F(1, n)] * n, [F(1), *[F()] * (n - 1)]):
            observed = list(map(fw, [dot(row, weights) for row in z]))
            truth = [None if row is None else fw(dot(row, weights)) for row in targets]
            for decoder in got["decoders"]:
                assert engine.apply(decoder["intercept"], decoder["matrix"], observed) == truth
    assert got["problem"] == p


def test_fixed_complete_suite_payload_counts_and_selected_bridge(fixed_bundle, runner):
    _, previous, wants, actual = fixed_bundle
    want = expected_suite(wants)
    for route in actual:
        assert wire(runner.assemble_suite(route, previous)) == wire(want)
        assert runner.ao_bridges(route, previous) == want["prior_bridges"]
    assert set(runner.COUNT_FIELDS) == set(wants[0]["counts"])
    assert set(runner.CHECK_FIELDS) == set(CHECKS)
    assert set(runner.SCOPE) == set(SCOPE)


@pytest.mark.parametrize("route", ["compare", "primary", "reference"])
def test_fixed_cached_orchestration_routes_preserve_full_math(
    fixed_bundle, runner, monkeypatch, route
):
    problems, previous, wants, actual = fixed_bundle
    calls = []
    originals = wire(problems)

    def loader(name):
        index = {"primary": 0, "reference": 1}[name]

        def build(problem):
            assert wire(problem) == wire(problems[FAMILIES.index(problem["family"])])
            calls.append((name, problem["family"]))
            return copy.deepcopy(actual[index][FAMILIES.index(problem["family"])])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    assert wire(runner.run_suite(route)) == wire(expected_suite(wants))
    names = ["primary", "reference"] if route == "compare" else [route]
    assert calls == [(name, family) for family in FAMILIES for name in names]
    assert wire(problems) == originals


def test_fixed_nonvacuous_whole_wire_and_suite_corruptions(fixed_bundle, runner):
    _, _, wants, _ = fixed_bundle
    for good in wants:
        mutations = family_mutations(good)
        assert len(mutations) == 27
        for bad in mutations:
            with pytest.raises(ValueError):
                runner.verify_suite(bad, good)
    suite = expected_suite(wants)
    mutations = [
        replaced(suite, ("families",), suite["families"][::-1]),
        replaced(suite, ("prior_bridges", "AO_selected_inputs_equal"), False),
        replaced(suite, ("prior_bridges", "AO_other_mathematics_replayed"), True),
        replaced(
            suite,
            ("payload_sizes", 0, "decoder_bytes"),
            suite["payload_sizes"][0]["decoder_bytes"] + 1,
        ),
        replaced(
            suite,
            ("payload_sizes", 0, "coordinate_bytes"),
            suite["payload_sizes"][0]["coordinate_bytes"] + 1,
        ),
        replaced(suite, ("totals", "witnesses"), suite["totals"]["witnesses"] + 1),
        replaced(suite, ("scope", "decoder_optimized"), True),
        replaced(suite, ("scope", "field_realizable_errors_required"), True),
    ]
    for bad in mutations:
        assert wire(bad) != wire(suite)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, suite)


def test_fixed_selected_producer_mutations_and_identity_only_boundary(fixed_bundle, runner):
    problems, previous, wants, _ = fixed_bundle
    paths = [
        (0, "problem", "probe", "bounds", 0),
        (0, "geometry", "coarse_cells", 0, "bounds", 0),
        (0, "geometry", "coarse_tiles", 0, "bounds", 0),
        (0, "matrices", "observations", 1, "matrix", 0, 0),
        (0, "matrices", "targets", 0, "matrix", 0, 0),
        (0, "certificates", 3, "certificate", "decoder", 0, 0),
        (0, "matrices", "coarse_decoder", 0, 0),
    ]
    mutations = []
    for path in paths:
        value = previous
        for part in path:
            value = value[part]
        mutations.append(replaced(previous, path, fw(fraction(value) + 1)))
    mutations += [
        replaced(previous, (0, "certificates", 3, "certificate", "row_basis", 0), 1),
        replaced(previous, (0, "certificates", 3, "certificate", "recoverable"), False),
    ]
    for bad in mutations:
        assert wire(bad) != wire(previous)
        with pytest.raises(ValueError):
            runner.ao_bridges(wants, bad)
    # Full-file authentication belongs to load_inputs/identities. This projection
    # helper does not claim to replay unrelated AO ranks or target dictionaries.
    unselected = copy.deepcopy(previous)
    unselected[0]["matrices"]["targets"][2]["matrix"][0][0] = fw(
        fraction(unselected[0]["matrices"]["targets"][2]["matrix"][0][0]) + 1
    )
    assert wire(unselected) != wire(previous)
    assert wire(runner.project_inputs(unselected)[0]) == wire(problems)


def test_fixed_all_current_and_prior_source_identities_are_pinned(runner):
    ids = runner.identities()
    assert set(ids) == {"source_ledger", "prior_artifacts", "ancestor_sources"}
    assert set(ids["source_ledger"]) == {
        "README.md",
        "kernel.py",
        "reference.py",
        "study.py",
        "test_qr05ap.py",
    }
    assert len(ids["prior_artifacts"]) == 46 and len(ids["ancestor_sources"]) == 49
    assert sum(map(len, ids.values())) == 100
    assert runner.AO_ID == {
        "bytes": 451698,
        "sha256": "55938309ba8ea8c205a9c6e127ce324e485b5e0bf5ff02bc5f513503e2f5fbf1",
    }
