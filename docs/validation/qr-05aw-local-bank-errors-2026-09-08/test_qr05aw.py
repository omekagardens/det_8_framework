"""Independent polynomial local-bank coordinates and exact error-box checks.

Only test names containing fixed consume authenticated AV/AR cases. Collection and generic
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
        load("_qr05aw_test_primary", "kernel.py"),
        load("_qr05aw_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05aw_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


CHECKS = (
    "geometry_partitions",
    "bank_label_identity",
    "coordinate_inverse",
    "frozen_bank_identity",
    "error_map_identity",
    "normalization_domain",
    "primitive_box",
    "shared_pipeline",
    "shared_attainment",
    "enclosure_box",
    "enclosure_attainment",
    "complete_gain_partition",
)
SCOPE = (
    "source_dictionary_changed",
    "source_or_target_integrals_recomputed",
    "repair_overlay_regenerated",
    "decoder_refitted",
    "filters_reselected",
    "measurements_added",
    "normalization_row_added",
    "empirical_noise_calibrated",
    "stochastic_independence_assumed",
    "field_realizable_errors_required",
    "common_bank_feasibility_solved",
    "same_error_domain_as_AV_claimed",
    "equal_noise_sensor_improvement_claimed",
    "full_field_stability_tested",
    "minimality_recomputed",
    "unknown_geometry_reconstructed",
    "physical_sensor_validated",
    "quantum_channel_constructed",
    "gravity_derived",
    "ret_integration_tested",
    "lean_verification_performed",
    "generic_production_API_hardened",
    "fixed_affine_families_run",
    "older_executors_run",
)


def encode(value):
    if isinstance(value, F):
        return fw(value)
    if isinstance(value, list):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    return value


def matrix(value):
    return [[fraction(x) for x in row] for row in value]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), F())


def mv(a, b):
    return [dot(row, b) for row in a]


def mm(a, b, width=None):
    if not b:
        assert width is not None
        return [[F()] * width for _ in a]
    return [[dot(row, col) for col in zip(*b, strict=True)] for row in a]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))


def scalar_product(left, right, width):
    return [
        [sum((left[i][h] * right[h][j] for h in range(len(right))), F()) for j in range(width)]
        for i in range(len(left))
    ]


def scalar_apply(a, values):
    return [sum((row[j] * values[j] for j in range(len(values))), F()) for row in a]


def rect(bounds):
    return list(map(fraction, bounds)) if bounds is not None else None


def volume(bounds):
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) / 2 if bounds is not None else F()


def cover_by_endpoint_cells(parent, children):
    """Literal grid occupancy, independent of global area-sum-only partition tests."""
    assert all(
        parent[0] <= b[0] < b[1] <= parent[1] and parent[2] <= b[2] < b[3] <= parent[3]
        for b in children
    )
    us = sorted({parent[0], parent[1], *(x for b in children for x in b[:2])})
    vs = sorted({parent[2], parent[3], *(x for b in children for x in b[2:])})
    for u0, u1 in pairwise(us):
        for v0, v1 in pairwise(vs):
            u, v = (u0 + u1) / 2, (v0 + v1) / 2
            assert sum(b[0] < u < b[1] and b[2] < v < b[3] for b in children) == 1


def polynomial_block(bounds, weight=F(1), inverse=False):
    """Expand u^a v^b, or local monomials, via independent coefficient dictionaries."""
    u0, u1, v0, v1 = bounds
    du, dv = u1 - u0, v1 - v0
    if inverse:
        u = {0: -u0 / du, 1: 1 / du}
        v = {0: -v0 / dv, 1: 1 / dv}
        scale = 1 / weight
    else:
        u = {0: u0, 1: du}
        v = {0: v0, 1: dv}
        scale = weight
    rows = []
    for a, b in BASIS:
        ux = u if a else {0: F(1)}
        vy = v if b else {0: F(1)}
        rows.append([scale * ux.get(i, F()) * vy.get(j, F()) for i, j in BASIS])
    return rows


def scalar_synthesize(blocks, values):
    assert len(values) == 4 * len(blocks)
    return [
        sum((blocks[t][i][j] * values[4 * t + j] for j in range(4)), F())
        for t in range(len(blocks))
        for i in range(4)
    ]


def right_blocks(a, blocks):
    # Never construct a dense bank-size squared matrix.
    return [
        [
            sum((row[4 * t + h] * blocks[t][h][j] for h in range(4)), F())
            for t in range(len(blocks))
            for j in range(4)
        ]
        for row in a
    ]


def sign(x):
    return int(x > 0) - int(x < 0)


def expected(problem):
    probe = rect(problem["probe"])
    cells = {row["event"]: rect(row["bounds"]) for row in problem["cells"]}
    tiles = [rect(row["bounds"]) for row in problem["tiles"]]
    cover_by_endpoint_cells(probe, [b for b in cells.values() if b is not None])
    for event, bounds in cells.items():
        owned = [
            tile for row, tile in zip(problem["tiles"], tiles, strict=True) if row["event"] == event
        ]
        if bounds is None:
            assert not owned
        else:
            cover_by_endpoint_cells(bounds, owned)
    v = volume(probe)
    cell_volumes = [volume(b) for b in cells.values()]
    tile_volumes = list(map(volume, tiles))
    weights = [v * v * h for h in tile_volumes]
    blocks = [polynomial_block(b, w) for b, w in zip(tiles, weights, strict=True)]
    inverse = [polynomial_block(b, w, True) for b, w in zip(tiles, weights, strict=True)]
    for a, z in zip(blocks, inverse, strict=True):
        assert scalar_product(a, z, 4) == identity(4)
        assert scalar_product(z, a, 4) == identity(4)
    scales = [
        v * v * volume(cells[row["first"]]) * volume(cells[row["second"]])
        for row in problem["target_labels"]
    ]
    b, g, d = (matrix(problem[key]) for key in ("interface", "geometric", "decoder"))
    q, r, s, t = len(g), len(g[0]), len(b), len(tiles)
    defined = [i for i, x in enumerate(scales) if x > 0]
    undefined = [i for i, x in enumerate(scales) if x == 0]
    assert all(not any(g[i]) for i in undefined)
    k = scalar_product(d, b, r)
    assert k == g
    h, j = right_blocks(b, blocks), right_blocks(g, blocks)
    ell = scalar_product(d, h, r)
    assert ell == j
    a = [([x / scales[i] for x in j[i]] if i in defined else None) for i in range(q)]
    beta = [sum(map(abs, row), F()) for row in h]
    e = [
        ([d[i][l] * beta[l] / scales[i] for l in range(s)] if i in defined else None)
        for i in range(q)
    ]
    alpha = [sum(map(abs, row), F()) if row is not None else None for row in a]
    gamma = [sum(map(abs, row), F()) if row is not None else None for row in e]
    gap = [gamma[i] - alpha[i] if i in defined else None for i in range(q)]
    assert all(gap[i] >= 0 for i in defined)
    shared, enclosure = [None] * q, [None] * q
    for i in defined:
        signs = list(map(sign, a[i]))
        outer_signs = list(map(sign, e[i]))
        inner, outer = {}, {}
        for name, direction in (("positive", 1), ("negative", -1)):
            x = [F(direction * z) for z in signs]
            bank = scalar_synthesize(blocks, x)
            roundtrip = scalar_synthesize(inverse, bank)
            observed = scalar_apply(b, bank)
            direct = scalar_apply(g, bank)
            decoded = scalar_apply(d, observed)
            normalized = [decoded[z] / scales[z] if z in defined else None for z in range(q)]
            assert roundtrip == x and direct == decoded
            assert observed == scalar_apply(h, x)
            assert all(
                normalized[z] == dot(a[z], x) and abs(normalized[z]) <= alpha[z] for z in defined
            )
            assert all(abs(observed[l]) <= beta[l] for l in range(s))
            assert normalized[i] == direction * alpha[i]
            inner[name] = {
                "primitive": x,
                "bank_error": bank,
                "roundtrip_primitive": roundtrip,
                "observed_error": observed,
                "direct_error": direct,
                "decoded_error": decoded,
                "normalized_error": normalized,
                "attained": normalized[i],
            }
            eta = [direction * beta[l] * outer_signs[l] for l in range(s)]
            raw = scalar_apply(d, eta)
            normalized = [raw[z] / scales[z] if z in defined else None for z in range(q)]
            assert normalized[i] == direction * gamma[i]
            assert all(abs(normalized[z]) <= gamma[z] for z in defined)
            outer[name] = {
                "observed_error": eta,
                "decoded_error": raw,
                "normalized_error": normalized,
                "attained": normalized[i],
            }
        shared[i] = {"target_row": i, "signs": signs, **inner}
        enclosure[i] = {"target_row": i, "signs": outer_signs, **outer}
    maxima = [
        max(values[i] for i in defined) if defined else None for values in (alpha, gamma, gap)
    ]
    sets = [
        [i for i in defined if values[i] == maximum]
        for values, maximum in zip((alpha, gamma, gap), maxima, strict=True)
    ]
    strict = [i for i in defined if gap[i] > 0]
    tied = [i for i in defined if gap[i] == 0]
    nd, np = len(defined), sum(x is not None for x in cells.values())
    return encode(
        {
            "problem": copy.deepcopy(problem),
            "geometry": {
                "volume": v,
                "cell_volumes": cell_volumes,
                "tile_volumes": tile_volumes,
                "target_scales": scales,
                "defined_rows": defined,
                "undefined_rows": undefined,
            },
            "coordinates": {
                "bank_scales": weights,
                "raw_from_local": blocks,
                "local_from_raw": inverse,
            },
            "maps": {
                "decoder_bank": k,
                "bank_residual": [[F()] * r for _ in range(q)],
                "interface_error": h,
                "target_error": j,
                "decoded_error": ell,
                "error_residual": [[F()] * r for _ in range(q)],
                "normalized_target": a,
                "enclosure_target": e,
            },
            "shared": {
                "row_gains": alpha,
                "witnesses": shared,
                "max_gain": maxima[0],
                "max_rows": sets[0],
            },
            "enclosure": {
                "receiver_radii": beta,
                "row_gains": gamma,
                "witnesses": enclosure,
                "max_gain": maxima[1],
                "max_rows": sets[1],
                "common_bank_feasibility_tested": False,
            },
            "comparison": {
                "gain_gap": gap,
                "strict_rows": strict,
                "tied_rows": tied,
                "undefined_rows": undefined,
                "max_gap": maxima[2],
                "max_gap_rows": sets[2],
            },
            "checks": dict.fromkeys(CHECKS, True),
            "counts": {
                "cells": len(cells),
                "positive_cells": np,
                "tiles": t,
                "bank_values": r,
                "receiver_values": s,
                "target_rows": q,
                "defined_rows": nd,
                "undefined_rows": q - nd,
                "geometry_input_entries": 4 + 4 * np + 4 * t,
                "input_matrix_entries": s * r + q * r + q * s,
                "geometry_entries": 1 + len(cells) + t + q,
                "coordinate_entries": 33 * t,
                "map_entries": 5 * q * r + s * r + nd * (r + s),
                "gain_entries": s + 3 * nd + (3 if nd else 0),
                "shared_witnesses": 2 * nd,
                "shared_sign_entries": nd * r,
                "shared_witness_entries": 2 * nd * (3 * r + s + 2 * q + nd + 1),
                "enclosure_witnesses": 2 * nd,
                "enclosure_sign_entries": nd * s,
                "enclosure_witness_entries": 2 * nd * (s + q + nd + 1),
                "shared_maximizers": len(sets[0]),
                "enclosure_maximizers": len(sets[1]),
                "gap_maximizers": len(sets[2]),
                "strict_rows": len(strict),
                "tied_rows": len(tied),
            },
        }
    )


def make_problem(probe, cells, tiles, b, d, labels=None, name="synthetic"):
    b, d = ([[F(x) for x in row] for row in a] for a in (b, d))
    if labels is None:
        event = cells[0]["event"]
        labels = [{"first": event, "second": event}]
    return encode(
        {
            "family": name,
            "probe": list(map(F, probe)),
            "cells": [
                {
                    "event": row["event"],
                    "bounds": list(map(F, row["bounds"])) if row["bounds"] is not None else None,
                }
                for row in cells
            ],
            "tiles": [
                {"event": row["event"], "bounds": list(map(F, row["bounds"]))} for row in tiles
            ],
            "bank_labels": [{"tile": i, "basis": j} for i in range(len(tiles)) for j in range(4)],
            "target_labels": copy.deepcopy(labels),
            "interface": b,
            "geometric": scalar_product(d, b, 4 * len(tiles)),
            "decoder": d,
        }
    )


def unit_problem():
    cell = {"event": 0, "bounds": [0, 1, 0, 1]}
    return make_problem(cell["bounds"], [cell], [cell], identity(4), [[1, -1, -1, 1]], name="unit")


def mixed_problem(all_undefined=False):
    cells = [{"event": 0, "bounds": [0, 1, 0, 1]}, {"event": 1, "bounds": None}]
    labels = (
        [{"first": 0, "second": 1}, {"first": 1, "second": 1}]
        if all_undefined
        else [{"first": 0, "second": 0}, {"first": 0, "second": 1}]
    )
    d = [[1, -1], [2, -2]] if all_undefined else [[1, 0], [1, -1]]
    return make_problem(
        [0, 1, 0, 1],
        cells,
        [cells[0]],
        [[1, 0, 0, 0], [1, 0, 0, 0]],
        d,
        labels,
        "undefined" if all_undefined else "mixed",
    )


def positive_zero_problem():
    p = mixed_problem()
    return replaced(
        replaced(p, ["target_labels"], [p["target_labels"][0]]), ["decoder"], [[fw(1), fw(-1)]]
    ) | {"geometric": [[fw(0)] * 4]}


def unequal_problem():
    probe = [-2, 2, -1, 2]
    cells = [{"event": -3, "bounds": [-2, 0, -1, 2]}, {"event": 7, "bounds": [0, 2, -1, 2]}]
    tiles = [
        cells[1],
        {"event": -3, "bounds": [-2, 0, -1, 0]},
        {"event": -3, "bounds": [-2, 0, 0, 2]},
    ]
    b = [[F(j % 4 == 0) for j in range(12)], [F(j % 4 == 1) - F(j % 4 == 2) for j in range(12)]]
    d = [[1, -1], [0, 2], [-1, 1]]
    labels = [{"first": -3, "second": -3}, {"first": -3, "second": 7}, {"first": 7, "second": 7}]
    return make_problem(probe, cells, tiles, b, d, labels, "unequal")


def empty_receiver_problem():
    cell = {"event": 0, "bounds": [0, 1, 0, 1]}
    return make_problem(cell["bounds"], [cell], [cell], [], [[]], name="empty")


def thin_problem():
    cell = {"event": -1, "bounds": [F(-1, 3), F(-1, 3) + F(1, 1009), F(2, 5), F(2, 5) + F(1, 1013)]}
    return make_problem(cell["bounds"], [cell], [cell], [[1, 0, 0, 0]], [[1]], name="thin")


@pytest.mark.parametrize(
    "factory",
    [
        unit_problem,
        mixed_problem,
        lambda: mixed_problem(True),
        positive_zero_problem,
        unequal_problem,
        empty_receiver_problem,
        thin_problem,
    ],
)
def test_generic_complete_expansion_oracle(engines, factory):
    p = factory()
    wanted = expected(p)
    for engine in engines:
        before = wire(p)
        a = engine.build_family(p)
        assert wire(a) == wire(wanted)
        assert wire(p) == before


@pytest.mark.parametrize(
    "factory", [unit_problem, mixed_problem, positive_zero_problem, empty_receiver_problem]
)
def test_exhaustive_small_local_and_receiver_cubes(engines, factory):
    p = factory()
    want = expected(p)
    w = [matrix(block) for block in want["coordinates"]["raw_from_local"]]
    b, d = matrix(p["interface"]), matrix(p["decoder"])
    sigma = list(map(fraction, want["geometry"]["target_scales"]))
    defined = want["geometry"]["defined_rows"]
    beta = list(map(fraction, want["enclosure"]["receiver_radii"]))
    primitive_outputs = [
        scalar_apply(d, scalar_apply(b, scalar_synthesize(w, list(x))))
        for x in product((-1, 1), repeat=len(p["bank_labels"]))
    ]
    enclosure_outputs = [
        scalar_apply(d, [v * z for v, z in zip(beta, x, strict=True)])
        for x in product((-1, 1), repeat=len(b))
    ]
    for i in defined:
        assert max(row[i] / sigma[i] for row in primitive_outputs) == fraction(
            want["shared"]["row_gains"][i]
        )
        assert min(row[i] / sigma[i] for row in primitive_outputs) == -fraction(
            want["shared"]["row_gains"][i]
        )
        assert max(row[i] / sigma[i] for row in enclosure_outputs) == fraction(
            want["enclosure"]["row_gains"][i]
        )
        assert min(row[i] / sigma[i] for row in enclosure_outputs) == -fraction(
            want["enclosure"]["row_gains"][i]
        )
    for engine in engines:
        assert wire(engine.build_family(p)) == wire(want)


def test_null_rows_do_not_erase_nonzero_raw_enclosure_errors(engines):
    for engine in engines:
        a = engine.build_family(mixed_problem())
        assert a["geometry"]["target_scales"] == [fw(F(1, 16)), fw(0)]
        assert a["geometry"]["defined_rows"] == [0] and a["geometry"]["undefined_rows"] == [1]
        assert a["shared"]["row_gains"] == a["enclosure"]["row_gains"] == [fw(2), None]
        for name in ("shared", "enclosure"):
            assert a[name]["witnesses"][1] is None
        endpoint = a["enclosure"]["witnesses"][0]["positive"]
        assert endpoint["decoded_error"] == [fw(F(1, 8)), fw(F(1, 8))]
        assert endpoint["normalized_error"] == [fw(2), None]
        assert a["shared"]["witnesses"][0]["positive"]["direct_error"] == [fw(F(1, 8)), fw(0)]
        for key in ("normalized_target", "enclosure_target"):
            assert a["maps"][key][1] is None
        empty = engine.build_family(mixed_problem(True))
        for name in ("shared", "enclosure"):
            assert empty[name]["max_gain"] is None and empty[name]["max_rows"] == []
            assert empty[name]["witnesses"] == [None, None]
        assert empty["comparison"]["max_gap"] is None and empty["comparison"]["max_gap_rows"] == []
        assert empty["comparison"]["undefined_rows"] == [0, 1]
        positive = engine.build_family(positive_zero_problem())
        assert positive["shared"]["row_gains"] == [fw(0)]
        assert positive["enclosure"]["row_gains"] == [fw(4)]
        assert positive["shared"]["witnesses"][0] is not None


def test_actual_tile_origins_and_volumes_not_probe_or_coarse_blocks(engines):
    p = unequal_problem()
    want = expected(p)
    assert want["geometry"]["volume"] == fw(6)
    assert want["geometry"]["tile_volumes"] == list(map(fw, [3, 1, 2]))
    assert want["coordinates"]["bank_scales"] == list(map(fw, [108, 36, 72]))
    probe_block = encode(polynomial_block(rect(p["probe"]), F(108)))
    assert probe_block != want["coordinates"]["raw_from_local"][0]
    # Left original cell has two unequal children: neither may use its whole-cell block.
    cell_block = encode(polynomial_block(rect(p["cells"][0]["bounds"]), F(108)))
    assert all(block != cell_block for block in want["coordinates"]["raw_from_local"][1:])
    for engine in engines:
        a = engine.build_family(p)
        assert wire(a) == wire(want)
        values = list(map(fw, range(12)))
        raw = engine.synthesize(a["coordinates"]["raw_from_local"], values)
        assert engine.synthesize(a["coordinates"]["local_from_raw"], raw) == values


def affine_problem(p, au, bv, cu, dv, receiver, receiver_inverse):
    k = au * cu
    global_block = polynomial_block([bv, bv + au, dv, dv + cu], k**3)
    inverse_block = polynomial_block([bv, bv + au, dv, dv + cu], k**3, True)
    blocks = [global_block for _ in p["tiles"]]
    inverse = [inverse_block for _ in p["tiles"]]

    def move(bounds):
        if bounds is None:
            return None
        u0, u1, v0, v1 = rect(bounds)
        return list(map(fw, [au * u0 + bv, au * u1 + bv, cu * v0 + dv, cu * v1 + dv]))

    out = copy.deepcopy(p)
    out["family"] = "affine"
    out["probe"] = move(p["probe"])
    for key in ("cells", "tiles"):
        for row in out[key]:
            row["bounds"] = move(row["bounds"])
    out["interface"] = encode(mm(receiver, right_blocks(matrix(p["interface"]), inverse)))
    out["geometric"] = encode(
        [[k**4 * x for x in row] for row in right_blocks(matrix(p["geometric"]), inverse)]
    )
    out["decoder"] = encode(
        [[k**4 * x for x in row] for row in mm(matrix(p["decoder"]), receiver_inverse)]
    )
    return out, blocks, inverse, k


@pytest.mark.parametrize("factory", [unequal_problem, mixed_problem, lambda: mixed_problem(True)])
def test_full_affine_transport_local_domain_and_undefined_semantics(engines, factory):
    p = factory()
    receiver = [[F(1), F(1)], [F(1), F(-1)]]
    inverse = [[F(1, 2), F(1, 2)], [F(1, 2), F(-1, 2)]]
    moved, bank, bank_inverse, k = affine_problem(
        p, F(3, 2), F(-7, 5), F(5, 3), F(11, 7), receiver, inverse
    )
    for engine in engines:
        before, after = engine.build_family(p), engine.build_family(moved)
        assert wire(after) == wire(expected(moved))
        for key in ("defined_rows", "undefined_rows"):
            assert after["geometry"][key] == before["geometry"][key]
        assert after["geometry"]["volume"] == fw(k * fraction(before["geometry"]["volume"]))
        assert after["geometry"]["target_scales"] == [
            fw(k**4 * fraction(x)) for x in before["geometry"]["target_scales"]
        ]
        for i, (old, new) in enumerate(
            zip(
                before["coordinates"]["raw_from_local"],
                after["coordinates"]["raw_from_local"],
                strict=True,
            )
        ):
            assert new == encode(scalar_product(bank[i], matrix(old), 4))
            assert after["coordinates"]["local_from_raw"][i] == encode(
                scalar_product(
                    matrix(before["coordinates"]["local_from_raw"][i]), bank_inverse[i], 4
                )
            )
        assert after["maps"]["normalized_target"] == before["maps"]["normalized_target"]
        assert after["shared"]["row_gains"] == before["shared"]["row_gains"]
        assert after["shared"]["max_rows"] == before["shared"]["max_rows"]
        for first, second in zip(
            before["shared"]["witnesses"], after["shared"]["witnesses"], strict=True
        ):
            if first is None:
                assert second is None
                continue
            assert first["signs"] == second["signs"]
            for side in ("positive", "negative"):
                a, b = first[side], second[side]
                assert b["primitive"] == a["primitive"] == b["roundtrip_primitive"]
                assert b["bank_error"] == encode(
                    scalar_synthesize(bank, list(map(fraction, a["bank_error"])))
                )
                assert b["observed_error"] == encode(
                    mv(receiver, list(map(fraction, a["observed_error"])))
                )
                for key in ("direct_error", "decoded_error"):
                    assert b[key] == [fw(k**4 * fraction(x)) for x in a[key]]
                assert b["normalized_error"] == a["normalized_error"]
        # Receiver mixing is deliberately not required to preserve enclosure gains.
        monomial = [[F(0), F(-3)], [F(2), F(0)]]
        monomial_inverse = [[F(0), F(1, 2)], [F(-1, 3), F(0)]]
        other, _, _, _ = affine_problem(
            p, F(3, 2), F(-7, 5), F(5, 3), F(11, 7), monomial, monomial_inverse
        )
        result = engine.build_family(other)
        assert result["enclosure"]["row_gains"] == before["enclosure"]["row_gains"]


def test_bank_tile_order_changes_require_matching_matrix_columns(engines):
    p = unequal_problem()
    order = [2, 0, 1]
    moved = copy.deepcopy(p)
    moved["tiles"] = [p["tiles"][i] for i in order]
    for key in ("interface", "geometric"):
        moved[key] = [[x for i in order for x in row[4 * i : 4 * i + 4]] for row in p[key]]
    for engine in engines:
        old, new = engine.build_family(p), engine.build_family(moved)
        assert wire(new) == wire(expected(moved))
        assert new["geometry"]["tile_volumes"] == [
            old["geometry"]["tile_volumes"][i] for i in order
        ]
        assert new["shared"]["row_gains"] == old["shared"]["row_gains"]
        assert new["enclosure"]["row_gains"] == old["enclosure"]["row_gains"]
        for first, second in zip(
            old["shared"]["witnesses"], new["shared"]["witnesses"], strict=True
        ):
            assert second["signs"] == [x for i in order for x in first["signs"][4 * i : 4 * i + 4]]
            for side in ("positive", "negative"):
                assert second[side]["normalized_error"] == first[side]["normalized_error"]


def test_epsilon_scales_actual_errors_without_clipping(engines):
    for engine in engines:
        p = unit_problem()
        result = engine.build_family(p)
        w = result["coordinates"]["raw_from_local"]
        for epsilon in (F(0), F(3, 2), F(9)):
            for row in result["shared"]["witnesses"]:
                for side in ("positive", "negative"):
                    original = row[side]
                    x = [fw(epsilon * fraction(z)) for z in original["primitive"]]
                    bank = engine.synthesize(w, x)
                    observed = engine.produce(p["interface"], bank)
                    decoded = engine.apply(p["decoder"], observed)
                    assert decoded == [fw(epsilon * fraction(z)) for z in original["decoded_error"]]
                    assert bank == [fw(epsilon * fraction(z)) for z in original["bank_error"]]
                    assert engine.synthesize(result["coordinates"]["local_from_raw"], bank) == x
        # The local box is not AV's raw unit box even on the unit rectangle.
        assert result["coordinates"]["raw_from_local"] == [
            encode([[F(i == j, 8) for j in range(4)] for i in range(4)])
        ]


def test_every_defined_endpoint_calls_actual_synthesis_inverse_and_evaluators(engines, monkeypatch):
    from collections import Counter

    for engine in engines:
        for p in (unit_problem(), mixed_problem(), mixed_problem(True)):
            recorded = {name: [] for name in ("synthesize", "produce", "apply")}
            originals = {name: getattr(engine, name) for name in recorded}
            for name, original in originals.items():

                def spy(a, x, name=name, original=original, recorded=recorded):
                    recorded[name].append(wire([a, x]))
                    return original(a, x)

                monkeypatch.setattr(engine, name, spy)
            f = engine.build_family(p)
            required = {name: [] for name in recorded}
            for row in f["shared"]["witnesses"]:
                if row is None:
                    continue
                for side in ("positive", "negative"):
                    e = row[side]
                    required["synthesize"].append(
                        wire([f["coordinates"]["raw_from_local"], e["primitive"]])
                    )
                    required["synthesize"].append(
                        wire([f["coordinates"]["local_from_raw"], e["bank_error"]])
                    )
                    for a in (p["interface"], p["geometric"]):
                        required["produce"].append(wire([a, e["bank_error"]]))
                    required["apply"].append(wire([p["decoder"], e["observed_error"]]))
            for row in f["enclosure"]["witnesses"]:
                if row is None:
                    continue
                for side in ("positive", "negative"):
                    required["apply"].append(wire([p["decoder"], row[side]["observed_error"]]))
            for name, original in originals.items():
                actual, want = Counter(recorded[name]), Counter(required[name])
                assert all(actual[key] >= count for key, count in want.items())
                monkeypatch.setattr(engine, name, original)


def test_raw_linear_apis_file_blind_empty_and_no_intercept(engines, monkeypatch):
    def forbidden(*args, **kwargs):
        raise RuntimeError("raw evaluator tried file access")

    for engine in engines:
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            assert engine.synthesize([], []) == []
            assert engine.synthesize([encode(identity(4))], list(map(fw, [1, -2, 3, -4]))) == list(
                map(fw, [1, -2, 3, -4])
            )
            assert engine.produce([[], []], []) == engine.apply([[], []], []) == [fw(0), fw(0)]
            assert engine.produce([], list(map(fw, [1, 2, 3]))) == []
            assert engine.apply([], []) == []
            a, x = [[fw(2), fw(-3), fw(F(1, 2))]], list(map(fw, [-1, 7, 4]))
            assert engine.produce(a, x) == engine.apply(a, x) == [fw(-21)]
            with pytest.raises(TypeError):
                engine.apply([fw(9)], a, x)


def test_shared_children_and_detached_null_and_raw_outputs(engines):
    p = mixed_problem()
    p["interface"][1] = p["interface"][0]
    p["tiles"][0] = p["cells"][0]
    before = wire(p)
    for engine in engines:
        f = engine.build_family(p)
        f["problem"]["tiles"][0]["bounds"][0][0] += 9
        f["shared"]["witnesses"][0]["positive"]["primitive"][0][0] += 7
        assert f["shared"]["witnesses"][0]["negative"]["primitive"][0] == fw(-1)
        assert f["shared"]["witnesses"][1] is None
        assert wire(p) == before and wire(engine.build_family(p)) == wire(expected(p))
        blocks = [encode(identity(4))]
        x = list(map(fw, [1, 2, 3, 4]))
        raw = engine.synthesize(blocks, x)
        raw[0][0] = 99
        assert x[0] == fw(1) and blocks[0][0][0] == fw(1)


def test_separate_bounded_admitted_cap_edges(engines):
    unit = {"event": 0, "bounds": [0, 1, 0, 1]}
    strips = [{"event": 0, "bounds": [F(i, 256), F(i + 1, 256), 0, 1]} for i in range(256)]
    cases = [
        make_problem(unit["bounds"], [unit], strips, [], [[]]),
        make_problem(unit["bounds"], [unit], [unit], [[0] * 4] * 320, [[0] * 320]),
    ]
    cells = [unit, *[{"event": i, "bounds": None} for i in range(1, 8)]]
    labels = [{"first": i, "second": j} for i in range(8) for j in range(8)]
    cases.append(make_problem(unit["bounds"], cells, [unit], [], [[]] * 64, labels))
    for engine in engines:
        assert engine.synthesize([encode(identity(4))] * 256, [fw(0)] * 1024) == [fw(0)] * 1024
        assert engine.produce([[]] * 1024, []) == [fw(0)] * 1024
        assert engine.apply([[fw(0)] * 320] * 64, [fw(0)] * 320) == [fw(0)] * 64
        for p in cases:
            assert wire(engine.build_family(p)) == wire(expected(p))


class NativeListSubclass(list):
    pass


class NativeDictSubclass(dict):
    pass


class NativeIntSubclass(int):
    pass


def malformed_families():
    p = unequal_problem()
    yield None
    yield []
    yield NativeDictSubclass(p)
    yield {**p, "reference_scale": [fw(1)]}
    for key in p:
        yield {k: v for k, v in p.items() if k != key}
    for value in ("", False, 1):
        yield replaced(p, ["family"], value)
    for key in p.keys() - {"family"}:
        for value in (None, tuple(p[key]), NativeListSubclass(p[key])):
            yield replaced(p, [key], value)
    for key in ("interface", "geometric", "decoder"):
        yield replaced(p, [key, -1], [])
        yield replaced(p, [key, -1], tuple(p[key][-1]))
    yield replaced(p, ["interface"], p["interface"] * 161)
    yield replaced(p, ["geometric"], p["geometric"] * 22)
    yield replaced(p, ["cells"], p["cells"] * 5)
    yield replaced(p, ["tiles"], p["tiles"] * 86)
    yield replaced(p, ["cells"], [])
    yield replaced(p, ["tiles"], [])
    yield replaced(p, ["target_labels"], [])
    yield replaced(p, ["geometric"], [])
    yield replaced(p, ["cells"], list(reversed(p["cells"])))
    yield replaced(p, ["cells", 1, "event"], p["cells"][0]["event"])
    yield replaced(p, ["cells", 0, "event"], True)
    yield replaced(p, ["tiles", 0, "event"], 999)
    yield replaced(p, ["tiles", 0, "bounds"], None)
    yield replaced(p, ["tiles", 0, "extra"], 0)
    yield replaced(p, ["cells", 0, "extra"], 0)
    yield replaced(p, ["target_labels"], list(reversed(p["target_labels"])))
    yield replaced(p, ["target_labels", 0, "first"], 999)
    yield replaced(p, ["target_labels", 0, "first"], True)
    yield replaced(p, ["target_labels", 0, "extra"], 0)
    yield replaced(p, ["bank_labels", 0, "tile"], 1)
    yield replaced(p, ["bank_labels", 0, "basis"], False)
    yield replaced(p, ["bank_labels", 0, "extra"], 0)
    yield replaced(p, ["bank_labels"], list(reversed(p["bank_labels"])))
    for path in (["probe", 1], ["cells", 0, "bounds", 1], ["tiles", 0, "bounds", 1]):
        yield replaced(p, path, fw(-99))
    yield replaced(p, ["cells", 1, "bounds"], p["cells"][0]["bounds"])
    yield replaced(p, ["tiles", 1, "bounds"], p["tiles"][2]["bounds"])
    yield replaced(p, ["tiles", 1, "bounds", 1], fw(-1))
    yield replaced(p, ["tiles", 0, "bounds", 1], fw(3))
    yield replaced(p, ["cells", 0, "bounds"], None)
    yield replaced(p, ["geometric", 0, 0], fw(99))
    null = mixed_problem()
    bad = replaced(null, ["geometric", 1, 0], fw(1))
    bad["decoder"][1] = [fw(1), fw(0)]  # DB remains equal, but null target G is forbidden.
    yield bad
    for value in (
        True,
        0.0,
        F(0),
        (0, 1),
        [0],
        [0, 1, 2],
        [0, 0],
        [0, -1],
        [2, 2],
        [1 << 4096, 1],
        [0, True],
        [NativeIntSubclass(0), 1],
        NativeListSubclass([0, 1]),
    ):
        yield replaced(p, ["decoder", -1, -1], value)
        yield replaced(p, ["tiles", -1, "bounds", -1], value)


def malformed_syntheses():
    blocks = [encode(identity(4))]
    values = list(map(fw, [1, 2, 3, 4]))
    for value in (None, {}, (), NativeListSubclass(blocks), blocks * 257):
        yield value, values
    for value in (None, {}, (), NativeListSubclass(values), values[:-1], values + [fw(5)]):
        yield blocks, value
    yield [[]], values
    yield [blocks[0][:-1]], values
    yield [[*blocks[0][:-1], []]], values
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [2, 2], [1 << 4096, 1]):
        yield replaced(blocks, [0, 3, 3], value), values
        yield blocks, replaced(values, [3], value)
    yield [], [fw(1)]


def malformed_evaluators(row_cap, width_cap):
    a, x = [[fw(1), fw(-1), fw(2)]], list(map(fw, [3, 4, 5]))
    for value in (None, {}, (), NativeListSubclass(a), a * (row_cap + 1)):
        yield value, x
    for value in (None, {}, (), NativeListSubclass(x), x[:-1], [fw(0)] * (width_cap + 1)):
        yield a, value
    yield a + [[fw(0)] * 2], x
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [2, 2], [1 << 4096, 1]):
        yield replaced(a, [0, 2], value), x
        yield a, replaced(x, [2], value)
    yield [], [True]


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
    for blocks, values in malformed_syntheses():
        require_rejection(lambda blocks=blocks, values=values: engine.synthesize(blocks, values))
        count += 1
    for name, rowcap, widthcap in (("produce", 1024, 1024), ("apply", 64, 320)):
        call = getattr(engine, name)
        for a, x in malformed_evaluators(rowcap, widthcap):
            require_rejection(lambda a=a, x=x, call=call: call(a, x))
            count += 1
    d = 1 << 4095
    for name in ("produce", "apply"):
        call = getattr(engine, name)
        if call([[fw(d), fw(-d)]], [fw(2), fw(2)]) != [fw(0)]:
            raise RuntimeError("raw product cancellation")
        require_rejection(lambda call=call: call([[fw(d), fw(d)]], [fw(1), fw(1)]))
    block = [[fw(d), fw(-d), fw(0), fw(0)], *[list(map(fw, [0, 0, 0, 0])) for _ in range(3)]]
    if engine.synthesize([block], list(map(fw, [2, 2, 0, 0]))) != [fw(0)] * 4:
        raise RuntimeError("block intermediate cancellation")
    require_rejection(lambda: engine.synthesize([block], list(map(fw, [2, -2, 0, 0]))))
    canceled = mixed_problem(True)
    canceled["interface"] = [[fw(d), fw(0), fw(0), fw(0)]] * 2
    if engine.build_family(canceled)["maps"]["decoder_bank"] != [[fw(0)] * 4] * 2:
        raise RuntimeError("bank coefficient cancellation")
    large = 1 << 1400
    cell = {"event": 0, "bounds": [0, F(1, large), 0, 1]}
    too_small = make_problem(cell["bounds"], [cell], [cell], [], [[]])
    require_rejection(lambda: engine.build_family(too_small))
    thin = 1 << 2050
    cell = {"event": 0, "bounds": [0, 1, 0, 1]}
    tiles = [
        {"event": 0, "bounds": [0, F(1, thin), 0, 1]},
        {"event": 0, "bounds": [F(1, thin), 1, 0, 1]},
    ]
    inverse_overflow = make_problem(cell["bounds"], [cell], tiles, [], [[]])
    require_rejection(lambda: engine.build_family(inverse_overflow))
    big_matrix = unit_problem()
    big_matrix["interface"] = [[fw(d), fw(0), fw(0), fw(0)]]
    big_matrix["decoder"] = [[fw(1)]]
    big_matrix["geometric"] = [[fw(d), fw(0), fw(0), fw(0)]]
    require_rejection(lambda: engine.build_family(big_matrix))
    cyclic = unit_problem()
    cyclic["tiles"].append(cyclic["tiles"])
    require_rejection(lambda: engine.build_family(cyclic))
    cycle = []
    cycle.append(cycle)
    require_rejection(lambda: engine.synthesize(cycle, [fw(1)] * 4))
    require_rejection(lambda: engine.produce(cycle, [fw(1)]))
    require_rejection(lambda: engine.apply([[fw(1)]], cycle))
    return count + 10


def pre_arithmetic_guards(engine):
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(1)
        raise RuntimeError("arithmetic before complete admission")

    original = engine._fraction
    engine._fraction = forbidden
    try:
        for value in ([], [0]):
            require_rejection(
                lambda value=value: engine.build_family(
                    replaced(unequal_problem(), ["tiles", -1, "bounds", -1], value)
                )
            )
            require_rejection(
                lambda value=value: engine.synthesize(
                    [replaced(encode(identity(4)), [3, 3], value)], [fw(1)] * 4
                )
            )
            require_rejection(lambda value=value: engine.produce([[fw(1)], [value]], [fw(2)]))
            require_rejection(lambda value=value: engine.apply([[fw(1)], [value]], [fw(2)]))
    finally:
        engine._fraction = original
    names = [
        name
        for name in (
            "_geometry",
            "_partition",
            "_area",
            "_coordinates",
            "_blocks",
            "_mm",
            "_dot",
            "_right_blocks",
            "_probe_maps",
            "_radius",
        )
        if hasattr(engine, name)
    ]
    originals = {name: getattr(engine, name) for name in names}
    for name in names:
        setattr(engine, name, forbidden)
    try:
        require_rejection(
            lambda: engine.build_family(replaced(unequal_problem(), ["decoder", -1, -1], [1, 0]))
        )
        require_rejection(
            lambda: engine.synthesize([replaced(encode(identity(4)), [3, 3], [1, 0])], [fw(1)] * 4)
        )
        require_rejection(lambda: engine.produce([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(lambda: engine.apply([[fw(1)], [[1, 0]]], [fw(1)]))
    finally:
        for name, original in originals.items():
            setattr(engine, name, original)
    if calls:
        raise RuntimeError("late admission ordering")
    return 12


def test_native_geometry_label_identity_and_retained_bit_guards(engines):
    counts = [explicit_guards(engine) for engine in engines]
    assert counts[0] == counts[1] and counts[0] > 150
    assert [pre_arithmetic_guards(engine) for engine in engines] == [12, 12]


@pytest.mark.parametrize("optimized", [False, True])
def test_isolated_explicit_normal_and_optimized_guards(tmp_path, optimized):
    script = r"""
import importlib.util,json,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("aw_guard_tests",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05aw_guard_"+name,file)
    counts.append(t.explicit_guards(engine)+t.pre_arithmetic_guards(engine))
print(json.dumps(counts))
"""
    args = [sys.executable, "-I", "-X", "pycache_prefix=" + str(tmp_path / "cache")]
    if optimized:
        args.append("-O")
    result = subprocess.run(
        [*args, "-c", script, str(Path(__file__).resolve())],
        capture_output=True,
        text=True,
        check=True,
        timeout=120,
    )
    total = (
        len(list(malformed_families()))
        + len(list(malformed_syntheses()))
        + len(list(malformed_evaluators(1024, 1024)))
        + len(list(malformed_evaluators(64, 320)))
        + 22
    )
    assert json.loads(result.stdout) == [total, total]


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


BRIDGES = {
    "selected_families": list(FAMILIES),
    "AV_frozen_maps_equal": True,
    "AR_selected_geometry_equal": True,
    "AR_bank_target_labels_equal": True,
    "AR_geometric_map_equal": True,
    "local_error_domain_is_new": True,
    "selected_partitions_rechecked": True,
    "frozen_bank_identity_rechecked": True,
    "old_raw_error_analysis_replayed": False,
    "other_historical_mathematics_replayed": False,
    "older_executors_run": False,
}


def changed_fraction(tree, path):
    value = tree
    for key in path:
        value = value[key]
    return replaced(tree, path, fw(fraction(value) + 1) if value is not None else fw(0))


def family_mutations(f):
    for key in f:
        yield {k: v for k, v in f.items() if k != key}
    yield {**f, "extra": 0}
    yield replaced(f, ["problem", "family"], f["problem"]["family"] + "-wrong")
    yield changed_fraction(f, ["problem", "probe", 0])
    for key, value in f["geometry"].items():
        if key in ("defined_rows", "undefined_rows"):
            yield replaced(f, ["geometry", key], [*value, -1])
        elif key == "volume":
            yield changed_fraction(f, ["geometry", key])
        else:
            yield changed_fraction(f, ["geometry", key, 0])
    yield changed_fraction(f, ["coordinates", "bank_scales", 0])
    for key in ("raw_from_local", "local_from_raw"):
        yield changed_fraction(f, ["coordinates", key, 0, 0, 0])
        yield replaced(f, ["coordinates", key], f["coordinates"][key][:-1])
    for key, value in f["maps"].items():
        if value and value[0] is not None and value[0]:
            yield changed_fraction(f, ["maps", key, 0, 0])
        else:
            yield replaced(f, ["maps", key], [[fw(0)]])
    for group in ("shared", "enclosure"):
        part = f[group]
        yield changed_fraction(f, [group, "row_gains", 0])
        yield changed_fraction(f, [group, "max_gain"])
        yield replaced(f, [group, "max_rows"], [*part["max_rows"], -1])
        yield replaced(f, [group, "witnesses"], part["witnesses"][:-1])
        index = next((i for i, row in enumerate(part["witnesses"]) if row is not None), None)
        if index is not None:
            row = part["witnesses"][index]
            yield replaced(f, [group, "witnesses", index, "target_row"], -1)
            if row["signs"]:
                yield replaced(f, [group, "witnesses", index, "signs", 0], 2)
                yield replaced(f, [group, "witnesses", index, "signs", 0], False)
            else:
                yield replaced(f, [group, "witnesses", index, "signs"], [0])
            for side in ("positive", "negative"):
                for key, value in row[side].items():
                    if key == "attained":
                        yield changed_fraction(f, [group, "witnesses", index, side, key])
                    elif value:
                        yield changed_fraction(f, [group, "witnesses", index, side, key, 0])
                    else:
                        yield replaced(f, [group, "witnesses", index, side, key], [fw(0)])
        null_index = next((i for i, row in enumerate(part["witnesses"]) if row is None), None)
        if null_index is not None:
            yield replaced(f, [group, "witnesses", null_index], {})
            yield replaced(f, [group, "row_gains", null_index], fw(0))
    yield replaced(f, ["enclosure", "common_bank_feasibility_tested"], True)
    if f["enclosure"]["receiver_radii"]:
        yield changed_fraction(f, ["enclosure", "receiver_radii", 0])
    else:
        yield replaced(f, ["enclosure", "receiver_radii"], [fw(0)])
    yield changed_fraction(f, ["comparison", "gain_gap", 0])
    yield changed_fraction(f, ["comparison", "max_gap"])
    for key in ("strict_rows", "tied_rows", "undefined_rows", "max_gap_rows"):
        yield replaced(f, ["comparison", key], [*f["comparison"][key], -1])
    for key in CHECKS:
        yield replaced(f, ["checks", key], False)
    for key in (
        "coordinate_entries",
        "map_entries",
        "gain_entries",
        "shared_witness_entries",
        "enclosure_witness_entries",
        "undefined_rows",
        "gap_maximizers",
    ):
        yield replaced(f, ["counts", key], f["counts"][key] + 1)


def literal_count_checks(f):
    p, c = f["problem"], f["counts"]
    assert c["geometry_input_entries"] == len(p["probe"]) + sum(
        len(row["bounds"])
        for key in ("cells", "tiles")
        for row in p[key]
        if row["bounds"] is not None
    )
    assert c["input_matrix_entries"] == sum(
        len(row) for key in ("interface", "geometric", "decoder") for row in p[key]
    )
    assert c["geometry_entries"] == 1 + sum(
        len(f["geometry"][key]) for key in ("cell_volumes", "tile_volumes", "target_scales")
    )
    assert c["coordinate_entries"] == len(f["coordinates"]["bank_scales"]) + sum(
        len(row)
        for key in ("raw_from_local", "local_from_raw")
        for block in f["coordinates"][key]
        for row in block
    )
    assert c["map_entries"] == sum(
        len(row) for a in f["maps"].values() for row in a if row is not None
    )
    assert c["gain_entries"] == len(f["enclosure"]["receiver_radii"]) + sum(
        x is not None
        for group, key in (
            ("shared", "row_gains"),
            ("enclosure", "row_gains"),
            ("comparison", "gain_gap"),
        )
        for x in f[group][key]
    ) + sum(
        f[group][key] is not None
        for group, key in (
            ("shared", "max_gain"),
            ("enclosure", "max_gain"),
            ("comparison", "max_gap"),
        )
    )
    for group in ("shared", "enclosure"):
        witnesses = [row for row in f[group]["witnesses"] if row is not None]
        assert c[group + "_witnesses"] == 2 * len(witnesses)
        assert c[group + "_sign_entries"] == sum(len(row["signs"]) for row in witnesses)
        assert c[group + "_witness_entries"] == sum(
            1 if key == "attained" else sum(x is not None for x in value)
            for row in witnesses
            for side in ("positive", "negative")
            for key, value in row[side].items()
        )
        assert c[group + "_maximizers"] == len(f[group]["max_rows"])
    assert c["gap_maximizers"] == len(f["comparison"]["max_gap_rows"])


def test_generic_full_wire_corruptions_and_literal_null_excluding_counts(runner):
    for factory in (unit_problem, mixed_problem, lambda: mixed_problem(True), unequal_problem):
        f = expected(factory())
        literal_count_checks(f)
        for bad in family_mutations(f):
            assert wire(bad) != wire(f)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)


def projected_problem(av, ar):
    p = av["problem"]
    return {
        "family": p["family"],
        "probe": copy.deepcopy(ar["problem"]["probe"]),
        "cells": copy.deepcopy(ar["problem"]["fine_cells"]),
        "tiles": [
            {key: copy.deepcopy(row[key]) for key in ("event", "bounds")}
            for row in ar["geometry"]["repair_tiles"]
        ],
        "bank_labels": copy.deepcopy(ar["matrices"]["repair_observation_rows"]),
        "target_labels": copy.deepcopy(p["target_labels"]),
        **{key: copy.deepcopy(p[key]) for key in ("interface", "geometric", "decoder")},
    }


def independent_history_checks(families, previous):
    assert set(previous) == {"AV", "AR"}
    for key in previous:
        assert [row["problem"]["family"] for row in previous[key]] == list(FAMILIES)
    for f, av, ar in zip(families, previous["AV"], previous["AR"], strict=True):
        assert wire(f["problem"]) == wire(projected_problem(av, ar))
        assert wire(av["problem"]["geometric"]) == wire(ar["repair"]["matrix"])
        assert wire(av["problem"]["target_labels"]) == wire(ar["matrices"]["fine_response_rows"])
        assert f["problem"]["bank_labels"] == [
            {"tile": i, "basis": j} for i in range(len(f["problem"]["tiles"])) for j in range(4)
        ]
        literal_count_checks(f)


def payload(families):
    return [
        {
            "family": f["problem"]["family"],
            "input_bytes": len(wire(f["problem"])),
            "geometry_bytes": len(wire(f["geometry"])),
            "coordinate_bytes": len(wire(f["coordinates"])),
            "map_bytes": len(wire(f["maps"])),
            "shared_bytes": len(wire(f["shared"])),
            "enclosure_bytes": len(wire(f["enclosure"])),
            "comparison_bytes": len(wire(f["comparison"])),
            "native_family_bytes": len(wire(f)),
        }
        for f in families
    ]


def expected_suite(families):
    return {
        "families": families,
        "prior_bridges": copy.deepcopy(BRIDGES),
        "payload_sizes": payload(families),
        "totals": {
            "families": 2,
            **{key: sum(f["counts"][key] for f in families) for key in families[0]["counts"]},
        },
        "scope": dict.fromkeys(SCOPE, False),
    }


def synthetic_histories(p):
    av = {
        "problem": {
            key: copy.deepcopy(p[key])
            for key in ("family", "target_labels", "interface", "geometric", "decoder")
        }
    }
    av["problem"].update({"primitive_map": "not read", "target_scales": "not read"})
    av.update({"maps": "not read", "shared": "not read"})
    ar = {
        "problem": {
            "family": p["family"],
            "probe": copy.deepcopy(p["probe"]),
            "fine_cells": copy.deepcopy(p["cells"]),
        },
        "geometry": {"repair_tiles": copy.deepcopy(p["tiles"]), "volume": "not read"},
        "matrices": {
            "repair_observation_rows": copy.deepcopy(p["bank_labels"]),
            "fine_response_rows": copy.deepcopy(p["target_labels"]),
        },
        "repair": {"matrix": copy.deepcopy(p["geometric"]), "intercept": "not read"},
        "certificate": "not read",
    }
    return av, ar


def test_synthetic_joined_history_full_suite_and_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(FAMILIES, (mixed_problem, lambda: mixed_problem(True)), strict=True):
        p = factory()
        p["family"] = name
        problems.append(p)
    families = list(map(expected, problems))
    histories = list(map(synthetic_histories, problems))
    previous = {"AV": [row[0] for row in histories], "AR": [row[1] for row in histories]}
    independent_history_checks(families, previous)
    wanted = expected_suite(families)
    lookup = {f["problem"]["family"]: f for f in families}

    def projection(prior):
        return [
            projected_problem(av, ar) for av, ar in zip(prior["AV"], prior["AR"], strict=True)
        ], prior

    monkeypatch.setattr(runner, "project_inputs", projection)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    calls = []

    def loader(name):
        def build(p):
            assert set(p) == set(problems[0])
            calls.append(name)
            return copy.deepcopy(lookup[p["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    for route, count in (("primary", 2), ("reference", 2), ("compare", 4)):
        calls.clear()
        assert wire(runner.run_suite(route)) == wire(wanted)
        assert len(calls) == count
    with pytest.raises(ValueError):
        runner.run_suite("unknown")
    bad = replaced(previous, ["AV", 0, "shared"], "changed")
    with pytest.raises(ValueError):
        runner.assemble_suite(families, bad)
    assert runner.historical_bridges(families, bad) == BRIDGES

    def changing(p):
        out = copy.deepcopy(lookup[p["family"]])
        p["family"] = "changed"
        return out

    monkeypatch.setattr(runner, "load_engine", lambda name: SimpleNamespace(build_family=changing))
    with pytest.raises(ValueError):
        runner.run_suite("primary")


def test_synthetic_selected_projection_inventory_order_and_detachment(runner):
    cell = {"event": 0, "bounds": [0, 1, 0, 1]}
    cells = [cell, *[{"event": i, "bounds": None} for i in range(1, 8)]]
    tiles = [{"event": 0, "bounds": [F(i, 12), F(i + 1, 12), 0, 1]} for i in range(12)]
    labels = [{"first": i, "second": j} for i in range(8) for j in range(8)]
    p = make_problem(cell["bounds"], cells, tiles, [[0] * 48] * 37, [[0] * 37] * 64, labels)
    histories = []
    for name in FAMILIES:
        current = copy.deepcopy(p)
        current["family"] = name
        histories.append(synthetic_histories(current))
    previous = {"AV": [r[0] for r in histories], "AR": [r[1] for r in histories]}
    before = wire(previous)
    projected, consumed = runner.project_inputs(previous)
    assert consumed is previous
    assert projected == [
        projected_problem(a, b) for a, b in zip(previous["AV"], previous["AR"], strict=True)
    ]
    projected[0]["tiles"][0]["bounds"][0][0] = 999
    assert wire(previous) == before
    changes = [
        [],
        {"AV": previous["AV"]},
        replaced(previous, ["AR"], previous["AR"][:1]),
        replaced(previous, ["AV"], list(reversed(previous["AV"]))),
        replaced(previous, ["AR", 0, "geometry", "repair_tiles"], []),
        replaced(previous, ["AR", 0, "matrices", "repair_observation_rows"], []),
        replaced(previous, ["AR", 0, "repair", "matrix", 0, 0], fw(1)),
        replaced(previous, ["AR", 0, "matrices", "fine_response_rows", 0, "first"], False),
        replaced(previous, ["AV", 0, "problem", "decoder", -1], []),
    ]
    for bad in changes:
        with pytest.raises(ValueError):
            runner.project_inputs(bad)


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
def test_fixed_full_expansion_oracle_and_actual_signed_endpoints(engines, fixed_data, index):
    problems, _, wanted, _ = fixed_data
    for engine in engines:
        p = copy.deepcopy(problems[index])
        before = wire(p)
        f = engine.build_family(p)
        assert wire(p) == before and wire(f) == wire(wanted[index])
        for row in f["shared"]["witnesses"]:
            if row is None:
                continue
            for side in ("positive", "negative"):
                e = row[side]
                raw = engine.synthesize(f["coordinates"]["raw_from_local"], e["primitive"])
                local = engine.synthesize(f["coordinates"]["local_from_raw"], raw)
                observed = engine.produce(p["interface"], raw)
                direct = engine.produce(p["geometric"], raw)
                decoded = engine.apply(p["decoder"], observed)
                assert local == e["primitive"] == e["roundtrip_primitive"]
                assert raw == e["bank_error"] and observed == e["observed_error"]
                assert direct == decoded == e["direct_error"] == e["decoded_error"]
        for row in f["enclosure"]["witnesses"]:
            if row is None:
                continue
            for side in ("positive", "negative"):
                e = row[side]
                assert engine.apply(p["decoder"], e["observed_error"]) == e["decoded_error"]


def test_fixed_full_suite_payload_and_selected_geometry(runner, fixed_data):
    problems, previous, families, wanted = fixed_data
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert runner.payload_sizes(families) == payload(families)
    for p, f in zip(problems, families, strict=True):
        assert len(p["cells"]) == 8 and len(p["tiles"]) == 12
        assert len(p["bank_labels"]) == 48 and len(p["target_labels"]) == 64
        assert len(p["interface"]) == 37
        d = len(f["geometry"]["defined_rows"])
        assert f["counts"]["shared_witness_entries"] == 2 * d * (144 + 37 + 128 + d + 1)
        assert f["counts"]["enclosure_witness_entries"] == 2 * d * (37 + 64 + d + 1)
        literal_count_checks(f)
    assert set(wanted["scope"]) == set(SCOPE) and not any(wanted["scope"].values())


@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_cached_orchestration_routes(runner, fixed_data, monkeypatch, route):
    _, _, families, wanted = fixed_data
    lookup = {f["problem"]["family"]: f for f in families}
    seen = []

    def loader(name):
        def build(p):
            assert p == lookup[p["family"]]["problem"]
            seen.append(name)
            return copy.deepcopy(lookup[p["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    assert wire(runner.run_suite(route)) == wire(wanted)
    assert seen == (["primary", "reference"] * 2 if route == "compare" else [route] * 2)


def test_fixed_full_family_and_suite_corruptions_are_nonvacuous(runner, fixed_data):
    _, _, families, wanted = fixed_data
    for f in families:
        for bad in family_mutations(f):
            assert wire(bad) != wire(f)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)
    changes = [
        replaced(wanted, ["families"], list(reversed(families))),
        replaced(wanted, ["prior_bridges", "AR_bank_target_labels_equal"], False),
        replaced(wanted, ["prior_bridges", "local_error_domain_is_new"], False),
        replaced(
            wanted,
            ["payload_sizes", 0, "coordinate_bytes"],
            wanted["payload_sizes"][0]["coordinate_bytes"] + 1,
        ),
        replaced(wanted, ["totals", "undefined_rows"], wanted["totals"]["undefined_rows"] + 1),
        replaced(wanted, ["scope", "same_error_domain_as_AV_claimed"], True),
        replaced(wanted, ["scope", "equal_noise_sensor_improvement_claimed"], True),
        {**wanted, "extra": 0},
    ]
    for bad in changes:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)


def test_fixed_selected_geometry_map_label_history_mutations(runner, fixed_data):
    _, previous, families, _ = fixed_data
    positive = next(
        i
        for i, row in enumerate(previous["AR"][0]["problem"]["fine_cells"])
        if row["bounds"] is not None
    )
    changes = [
        changed_fraction(previous, path)
        for path in (
            ["AV", 0, "problem", "interface", 0, 0],
            ["AV", 0, "problem", "geometric", 0, 0],
            ["AV", 0, "problem", "decoder", 0, 0],
            ["AR", 0, "repair", "matrix", 0, 0],
            ["AR", 0, "problem", "probe", 0],
            ["AR", 0, "problem", "fine_cells", positive, "bounds", 0],
            ["AR", 0, "geometry", "repair_tiles", 0, "bounds", 0],
        )
    ]
    changes.extend(
        [
            replaced(previous, ["AV", 0, "problem", "target_labels", 0, "first"], False),
            replaced(previous, ["AR", 0, "matrices", "fine_response_rows", 0, "first"], False),
            replaced(previous, ["AR", 0, "matrices", "repair_observation_rows", 0, "basis"], 4),
            replaced(
                previous,
                ["AR", 0, "matrices", "repair_observation_rows"],
                list(reversed(previous["AR"][0]["matrices"]["repair_observation_rows"])),
            ),
            replaced(previous, ["AR", 0, "geometry", "repair_tiles", 0, "event"], False),
            replaced(
                previous,
                ["AR", 0, "geometry", "repair_tiles"],
                list(reversed(previous["AR"][0]["geometry"]["repair_tiles"])),
            ),
            replaced(previous, ["AR", 0, "problem", "family"], "changed"),
        ]
    )
    for bad in changes:
        assert wire(bad) != wire(previous)
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)


def test_fixed_unselected_old_error_geometry_math_not_replayed(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    changes = [
        changed_fraction(previous, ["AV", 0, "problem", "primitive_map", 0, 0]),
        changed_fraction(previous, ["AV", 0, "problem", "target_scales", 0]),
        changed_fraction(previous, ["AV", 0, "shared", "row_gains", 0]),
        replaced(previous, ["AV", 0, "enclosure", "witnesses"], []),
        replaced(previous, ["AR", 0, "certificate"], {"not": "read"}),
        replaced(previous, ["AR", 0, "repair", "intercept"], []),
    ]
    for bad in changes:
        assert wire(bad) != wire(previous)
        assert runner.project_inputs(bad)[0] == problems
        assert runner.historical_bridges(families, bad) == BRIDGES


def test_fixed_source_and_ancestor_identity_inventory(runner):
    current = runner.identities()
    assert {k: len(current[k]) for k in current} == {
        "source_ledger": 5,
        "prior_artifacts": 53,
        "ancestor_sources": 84,
    }
    assert set(current["source_ledger"]) == set(runner.SOURCES)
    for path, count, sha in (
        (runner.AV, 1265211, "db498dfae4d1659f0fe35eef72efc916c6d9c8fedbd375830145e78a680c4ef5"),
        (runner.AR, 704842, "c9ed0e299c057eb6503238a3bc5ce18352abe81bc111615464afaa6ed264e4f8"),
    ):
        raw = path.read_bytes()
        assert len(raw) == count and hashlib.sha256(raw).hexdigest() == sha
    for name, want in current["source_ledger"].items():
        raw = (HERE / name).read_bytes()
        assert len(raw) == want["bytes"] and hashlib.sha256(raw).hexdigest() == want["sha256"]
