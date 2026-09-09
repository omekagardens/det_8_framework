"""Independent physical-kernel signs, polynomial integrals and bounded-field checks.

Only test names containing fixed consume authenticated AX cases. Collection and generic
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
        load("_qr05ay_test_primary", "kernel.py"),
        load("_qr05ay_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05ay_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


CHECKS = (
    "geometry_partitions",
    "bank_label_identity",
    "frozen_bank_identity",
    "kernel_corner_identity",
    "kernel_integrals",
    "bernstein_integrals",
    "corner_envelope",
    "normalization_domain",
    "bound_order",
    "sign_partition",
    "obstruction_inventory",
    "certified_exactness",
    "endpoint_field_bound",
    "endpoint_pipeline",
    "lower_attainment",
    "constant_controls",
    "complete_comparisons",
)
SCOPE = (
    "source_dictionary_changed",
    "old_source_or_target_integrals_recomputed",
    "repair_overlay_regenerated",
    "decoder_refitted",
    "filters_reselected",
    "measurements_added",
    "normalization_row_added",
    "empirical_noise_calibrated",
    "total_source_nonnegativity_guaranteed",
    "global_field_continuity_required",
    "mixed_absolute_kernel_integrated",
    "uncertified_exact_gain_claimed",
    "corner_envelope_sharpness_claimed",
    "integrated_positivity_used_as_pointwise_certificate",
    "equal_noise_sensor_improvement_claimed",
    "full_field_stability_tested",
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


CORNERS = BASIS


def field_polynomial(corners, amplitude=F(1)):
    # Multiply the two linear corner basis factors into a coefficient dictionary.
    coefficients = {power: F() for power in BASIS}
    for (a, b), weight in zip(CORNERS, corners, strict=True):
        up = {0: F(1), 1: F(-1)} if a == 0 else {1: F(1)}
        vp = {0: F(1), 1: F(-1)} if b == 0 else {1: F(1)}
        for u, cu in up.items():
            for v, cv in vp.items():
                coefficients[u, v] += amplitude * weight * cu * cv
    return coefficients


def integrate_unit(coefficients, moment):
    i, j = moment
    return sum((value / F(a + i + 1) / F(b + j + 1) for (a, b), value in coefficients.items()), F())


def integrate_rectangle(coefficients, bounds, moment):
    i, j = moment
    u0, u1, v0, v1 = bounds
    return sum(
        (
            value
            * (u1 ** (a + i + 1) - u0 ** (a + i + 1))
            / F(a + i + 1)
            * (v1 ** (b + j + 1) - v0 ** (b + j + 1))
            / F(b + j + 1)
            / 2
            for (a, b), value in coefficients.items()
        ),
        F(),
    )


def integral_oracle(probe, tiles, corners):
    """Actual polynomial fields and physical antiderivatives; never defined by WQ."""
    probe = rect(probe)
    boxes = list(map(rect, tiles))
    c = list(map(fraction, corners))
    amp = volume(probe) ** 2
    assert len(c) == 4 * len(boxes)
    out = {
        key: []
        for key in (
            "local_coefficients",
            "global_coefficients",
            "local_moments",
            "raw_moments",
            "minima",
            "maxima",
        )
    }
    for index, bounds in enumerate(boxes):
        values = c[4 * index : 4 * index + 4]
        local = field_polynomial(values, amp)
        transform = polynomial_block(bounds, F(1), True)
        global_coefficients = {
            power: sum((local[BASIS[h]] * transform[h][i] for h in range(4)), F())
            for i, power in enumerate(BASIS)
        }
        out["local_coefficients"].extend(local[m] for m in BASIS)
        out["global_coefficients"].extend(global_coefficients[m] for m in BASIS)
        out["local_moments"].extend(integrate_unit(local, m) / amp for m in BASIS)
        out["raw_moments"].extend(
            integrate_rectangle(global_coefficients, bounds, m) for m in BASIS
        )
        out["minima"].append(amp * min(values))
        out["maxima"].append(amp * max(values))
    return encode(out)


def rational_wire(value):
    if type(value) in (list, tuple):
        return [rational_wire(x) for x in value]
    return fw(value)


def polynomial_product(a, b):
    result = {}
    for (u, v), x in a.items():
        for (h, k), y in b.items():
            result[u + h, v + k] = result.get((u + h, v + k), F()) + x * y
    return result


def kernel_oracle(probe, tiles, coefficients):
    boxes = list(map(rect, tiles))
    g = matrix(coefficients)
    out = {
        key: []
        for key in (
            "corner_values",
            "tile_integrals",
            "bernstein_integrals",
            "tile_abs_upper",
            "tile_minima",
            "tile_maxima",
            "tile_classes",
        )
    }
    for row in g:
        record = {key: [] for key in out}
        for t, box in enumerate(boxes):
            polynomial = dict(zip(BASIS, row[4 * t : 4 * t + 4], strict=True))
            u0, u1, v0, v1 = box
            corners = [
                sum((coefficient * u**i * v**j for (i, j), coefficient in polynomial.items()), F())
                for u, v in ((u0, v0), (u1, v0), (u0, v1), (u1, v1))
            ]
            record["corner_values"].append(corners)
            record["tile_integrals"].append(integrate_rectangle(polynomial, box, (0, 0)))
            inverse = polynomial_block(box, F(1), True)
            for corner in range(4):
                local = field_polynomial([F(i == corner) for i in range(4)])
                physical = {
                    power: sum((local[BASIS[h]] * inverse[h][i] for h in range(4)), F())
                    for i, power in enumerate(BASIS)
                }
                record["bernstein_integrals"].append(
                    integrate_rectangle(polynomial_product(polynomial, physical), box, (0, 0))
                )
            lo, hi = min(corners), max(corners)
            record["tile_abs_upper"].append(volume(box) * max(map(abs, corners)))
            record["tile_minima"].append(lo)
            record["tile_maxima"].append(hi)
            kind = (
                "zero"
                if lo == hi == 0
                else "nonnegative"
                if lo >= 0
                else "nonpositive"
                if hi <= 0
                else "mixed"
            )
            record["tile_classes"].append(kind)
        for key, values in out.items():
            values.append(record[key])
    return encode(out)


def geometry_oracle(p):
    probe = rect(p["probe"])
    cells = {row["event"]: rect(row["bounds"]) for row in p["cells"]}
    tiles = [rect(row["bounds"]) for row in p["tiles"]]
    cover_by_endpoint_cells(probe, [b for b in cells.values() if b is not None])
    for event, box in cells.items():
        owned = [
            bounds for row, bounds in zip(p["tiles"], tiles, strict=True) if row["event"] == event
        ]
        if box is None:
            assert not owned
        else:
            cover_by_endpoint_cells(box, owned)
    v = volume(probe)
    sigma = [
        v * v * volume(cells[row["first"]]) * volume(cells[row["second"]])
        for row in p["target_labels"]
    ]
    return encode(
        {
            "volume": v,
            "cell_volumes": [volume(b) for b in cells.values()],
            "tile_volumes": list(map(volume, tiles)),
            "target_scales": sigma,
            "defined_rows": [i for i, x in enumerate(sigma) if x > 0],
            "undefined_rows": [i for i, x in enumerate(sigma) if x == 0],
        }
    )


def maximum(values):
    domain = [i for i, x in enumerate(values) if x is not None]
    gain = max(values[i] for i in domain) if domain else None
    return {"gain": gain, "rows": [i for i in domain if values[i] == gain]}


def comparison(high, low):
    domain = [
        i for i, (a, b) in enumerate(zip(high, low, strict=True)) if a is not None and b is not None
    ]
    gap = [high[i] - low[i] if i in domain else None for i in range(len(high))]
    assert all(gap[i] >= 0 for i in domain)
    largest = maximum(gap)
    return {
        "gain_gap": gap,
        "strict_rows": [i for i in domain if gap[i] > 0],
        "tied_rows": [i for i in domain if gap[i] == 0],
        "unavailable_rows": [i for i in range(len(gap)) if i not in domain],
        "max_gap": largest["gain"],
        "max_gap_rows": largest["rows"],
    }


def expected(p):
    geometry = geometry_oracle(p)
    v = fraction(geometry["volume"])
    amp = v * v
    sigma = list(map(fraction, geometry["target_scales"]))
    defined, undefined = geometry["defined_rows"], geometry["undefined_rows"]
    b, g, d = (matrix(p[key]) for key in ("interface", "geometric", "decoder"))
    q, r, s, t = len(g), len(g[0]), len(b), len(p["tiles"])
    k = scalar_product(d, b, r)
    assert k == g and all(not any(g[i]) for i in undefined)
    boxes = [row["bounds"] for row in p["tiles"]]
    kernels = kernel_oracle(p["probe"], boxes, p["geometric"])
    ints = matrix(kernels["tile_integrals"])
    bernstein = matrix(kernels["bernstein_integrals"])
    raw = [[amp * x for x in row] for row in bernstein]
    a = [[x / sigma[i] for x in raw[i]] if i in defined else None for i in range(q)]
    const = [
        amp * sum(map(abs, ints[i]), F()) / sigma[i] if i in defined else None for i in range(q)
    ]
    lower = [sum(map(abs, a[i]), F()) if i in defined else None for i in range(q)]
    upper = [
        amp * sum(map(fraction, kernels["tile_abs_upper"][i]), F()) / sigma[i]
        if i in defined
        else None
        for i in range(q)
    ]
    obs = []
    for i in range(q):
        rows = []
        for tile, values in enumerate(kernels["corner_values"][i]):
            corners = list(map(fraction, values))
            if min(corners) < 0 < max(corners):
                rows.append(
                    {
                        "tile": tile,
                        "positive_corner": next(j for j, x in enumerate(corners) if x > 0),
                        "negative_corner": next(j for j, x in enumerate(corners) if x < 0),
                    }
                )
        obs.append(rows)
    certified = [i for i in defined if not obs[i]]
    uncertified = [i for i in defined if obs[i]]
    exact = [const[i] if i in certified else None for i in range(q)]
    assert all(const[i] <= lower[i] <= upper[i] for i in defined)
    assert all(const[i] == lower[i] for i in certified)
    all_corners = [[fraction(x) for tile in row for x in tile] for row in kernels["corner_values"]]
    nonneg = [i for i in defined if all(x >= 0 for x in all_corners[i])]
    nonpos = [i for i in defined if all(x <= 0 for x in all_corners[i])]
    zeros = [i for i in defined if not any(all_corners[i])]
    inonneg = [i for i in defined if all(x >= 0 for x in a[i])]
    inonpos = [i for i in defined if all(x <= 0 for x in a[i])]
    izeros = [i for i in defined if not any(a[i])]
    bounds = {
        "constant_lower": const,
        "bilinear_lower": lower,
        "corner_upper": upper,
        "certified_gain": exact,
    }
    bounds["maxima"] = {key: maximum(values) for key, values in bounds.items()}
    comparisons = {
        "bilinear_minus_constant": comparison(lower, const),
        "upper_minus_bilinear": comparison(upper, lower),
        "upper_minus_certified": comparison(upper, exact),
    }

    def endpoint(c, target=None):
        integrated = integral_oracle(p["probe"], boxes, encode(c))
        bank = list(map(fraction, integrated["raw_moments"]))
        observed = scalar_apply(b, bank)
        direct = scalar_apply(g, bank)
        decoded = scalar_apply(d, observed)
        normalized = [decoded[i] / sigma[i] if i in defined else None for i in range(q)]
        assert direct == decoded
        assert all(
            normalized[i] == dot(a[i], c) and abs(normalized[i]) <= lower[i] <= upper[i]
            for i in defined
        )
        assert all(
            -amp <= fraction(x) <= amp for key in ("minima", "maxima") for x in integrated[key]
        )
        out = {
            "corners": c,
            "local_coefficients": integrated["local_coefficients"],
            "global_coefficients": integrated["global_coefficients"],
            "local_moments": integrated["local_moments"],
            "bank_error": bank,
            "tile_minima": integrated["minima"],
            "tile_maxima": integrated["maxima"],
            "observed_error": observed,
            "direct_error": direct,
            "decoded_error": decoded,
            "normalized_error": normalized,
        }
        if target is not None:
            out["attained"] = normalized[target]
        return out

    tile_witness, bilinear_witness = [None] * q, [None] * q
    for i in defined:
        for group, signs, gain, repeat in (
            (tile_witness, list(map(sign, ints[i])), const[i], 4),
            (bilinear_witness, list(map(sign, a[i])), lower[i], 1),
        ):
            corners = [F(x) for x in signs for _ in range(repeat)]
            positive, negative = endpoint(corners, i), endpoint([-x for x in corners], i)
            assert positive["attained"] == gain and negative["attained"] == -gain
            group[i] = {"target_row": i, "signs": signs, "positive": positive, "negative": negative}
    certification = {
        "status": [
            "undefined" if i in undefined else "uncertified" if i in uncertified else "certified"
            for i in range(q)
        ],
        "mixed_obstructions": obs,
        "certified_rows": certified,
        "uncertified_rows": uncertified,
        "undefined_rows": undefined,
        "nonnegative_rows": nonneg,
        "nonpositive_rows": nonpos,
        "zero_rows": zeros,
        "integrated_nonnegative_rows": inonneg,
        "integrated_nonpositive_rows": inonpos,
        "integrated_zero_rows": izeros,
        "integrated_nonnegative_mixed_rows": [i for i in inonneg if i in uncertified],
    }
    nd, nz = len(defined), len(certified)
    counts = {
        "cells": len(p["cells"]),
        "positive_cells": sum(row["bounds"] is not None for row in p["cells"]),
        "tiles": t,
        "bank_values": r,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": nd,
        "undefined_rows": q - nd,
        "geometry_input_entries": 4
        + 4 * sum(row["bounds"] is not None for row in p["cells"])
        + 4 * t,
        "input_matrix_entries": s * r + q * r + q * s,
        "geometry_entries": 1 + len(p["cells"]) + t + q,
        "kernel_entries": 12 * q * t,
        "map_entries": (3 * q + nd) * r,
        "bound_entries": 3 * nd + nz + (3 if nd else 0) + (1 if nz else 0),
        "comparison_entries": 2 * nd + nz + (2 if nd else 0) + (1 if nz else 0),
        "mixed_tiles": sum(map(len, obs)),
        "mixed_rows": len(uncertified),
        "certified_rows": nz,
        "pointwise_nonnegative_rows": len(nonneg),
        "pointwise_nonpositive_rows": len(nonpos),
        "pointwise_zero_rows": len(zeros),
        "integrated_nonnegative_rows": len(inonneg),
        "integrated_nonpositive_rows": len(inonpos),
        "integrated_zero_rows": len(izeros),
        "integrated_nonnegative_mixed_rows": len(
            certification["integrated_nonnegative_mixed_rows"]
        ),
        "tile_constant_witnesses": 2 * nd,
        "bilinear_witnesses": 2 * nd,
        "constant_witnesses": 2,
        "tile_sign_entries": nd * t,
        "bilinear_sign_entries": nd * r,
        "endpoint_entries": 4 * nd * (5 * r + 2 * t + s + 2 * q + nd + 1),
        "constant_endpoint_entries": 2 * (5 * r + 2 * t + s + 2 * q + nd),
        "constant_gap_strict": len(comparisons["bilinear_minus_constant"]["strict_rows"]),
        "upper_gap_strict": len(comparisons["upper_minus_bilinear"]["strict_rows"]),
        "certified_upper_gap_strict": len(comparisons["upper_minus_certified"]["strict_rows"]),
        "constant_maximizers": len(bounds["maxima"]["constant_lower"]["rows"]),
        "bilinear_maximizers": len(bounds["maxima"]["bilinear_lower"]["rows"]),
        "upper_maximizers": len(bounds["maxima"]["corner_upper"]["rows"]),
        "certified_maximizers": len(bounds["maxima"]["certified_gain"]["rows"]),
    }
    return encode(
        {
            "problem": copy.deepcopy(p),
            "geometry": geometry,
            "kernels": kernels,
            "maps": {
                "decoder_bank": k,
                "bank_residual": [[F()] * r for _ in range(q)],
                "raw_bilinear_target": raw,
                "normalized_bilinear_target": a,
            },
            "bounds": bounds,
            "certification": certification,
            "witnesses": {
                "tile_constant": tile_witness,
                "bilinear": bilinear_witness,
                "constant_positive": endpoint([F(1)] * r),
                "constant_negative": endpoint([F(-1)] * r),
            },
            "comparison": comparisons,
            "checks": dict.fromkeys(CHECKS, True),
            "counts": counts,
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


def one_kernel(coefficients):
    p = unit_problem()
    row = rational_wire(coefficients)
    return p | {"geometric": [row], "decoder": [copy.deepcopy(row)]}


def mixed_kernel_problem():
    return one_kernel([F(-1, 4), 1, 0, 0])


def saddle_problem():
    return one_kernel([1, -2, -2, 4])


def opposite_tiles_problem():
    cell = {"event": 0, "bounds": [0, 1, 0, 1]}
    tiles = [{"event": 0, "bounds": [0, F(1, 2), 0, 1]}, {"event": 0, "bounds": [F(1, 2), 1, 0, 1]}]
    return make_problem(
        cell["bounds"], [cell], tiles, identity(8), [[1, 0, 0, 0, -1, 0, 0, 0]], name="opposite"
    )


def partial_certificate_problem():
    cells = [{"event": 0, "bounds": [0, F(1, 2), 0, 1]}, {"event": 1, "bounds": [F(1, 2), 1, 0, 1]}]
    rows = [[1, 0, 0, 0, 1, 0, 0, 0], [F(-1, 4), 1, 0, 0, 0, 0, 0, 0], [0] * 8]
    labels = [{"first": 0, "second": 0}, {"first": 0, "second": 1}, {"first": 1, "second": 1}]
    return make_problem([0, 1, 0, 1], cells, cells, identity(8), rows, labels, "partial")


@pytest.mark.parametrize(
    "factory",
    [
        unit_problem,
        mixed_kernel_problem,
        saddle_problem,
        opposite_tiles_problem,
        partial_certificate_problem,
        unequal_problem,
        thin_problem,
        mixed_problem,
        lambda: mixed_problem(True),
        positive_zero_problem,
        empty_receiver_problem,
    ],
)
def test_complete_independent_kernel_and_endpoint_oracle(engines, factory):
    p = factory()
    wanted = expected(p)
    for engine in engines:
        before = wire(p)
        assert wire(engine.build_family(p)) == wire(wanted)
        assert wire(p) == before


def test_positive_integrated_coefficients_do_not_certify_kernel_sign(engines):
    for engine in engines:
        f = engine.build_family(mixed_kernel_problem())
        assert f["kernels"]["corner_values"] == rational_wire(
            [[[F(-1, 4), F(3, 4), F(-1, 4), F(3, 4)]]]
        )
        assert f["maps"]["normalized_bilinear_target"] == rational_wire(
            [[F(1, 24), F(5, 24), F(1, 24), F(5, 24)]]
        )
        assert f["certification"]["status"] == ["uncertified"]
        assert f["certification"]["integrated_nonnegative_mixed_rows"] == [0]
        assert f["certification"]["mixed_obstructions"] == [
            [{"tile": 0, "positive_corner": 1, "negative_corner": 0}]
        ]
        assert f["bounds"]["constant_lower"] == f["bounds"]["bilinear_lower"] == [fw(F(1, 2))]
        assert f["bounds"]["corner_upper"] == [fw(F(3, 2))]
        assert f["bounds"]["certified_gain"] == [None]
        assert f["bounds"]["maxima"]["certified_gain"] == {"gain": None, "rows": []}
        assert f["comparison"]["upper_minus_certified"] == {
            "gain_gap": [None],
            "strict_rows": [],
            "tied_rows": [],
            "unavailable_rows": [0],
            "max_gap": None,
            "max_gap_rows": [],
        }


def test_opposite_tile_signs_need_tilewise_extremizers(engines):
    for engine in engines:
        f = engine.build_family(opposite_tiles_problem())
        assert f["kernels"]["tile_classes"] == [["nonnegative", "nonpositive"]]
        assert f["certification"]["certified_rows"] == [0]
        assert (
            f["certification"]["nonnegative_rows"] == f["certification"]["nonpositive_rows"] == []
        )
        assert all(
            f["bounds"][key] == [fw(2)]
            for key in ("constant_lower", "bilinear_lower", "corner_upper", "certified_gain")
        )
        w = f["witnesses"]["tile_constant"][0]
        assert w["signs"] == [1, -1]
        assert w["positive"]["corners"] == rational_wire([1] * 4 + [-1] * 4)
        assert w["positive"]["attained"] == fw(2) and w["negative"]["attained"] == fw(-2)
        for side in ("positive", "negative"):
            assert f["witnesses"]["constant_" + side]["normalized_error"] == [fw(0)]


def test_zero_edges_admit_exact_gain_but_corner_envelope_stays_loose(engines):
    for engine in engines:
        f = engine.build_family(one_kernel([0, 0, 0, 1]))
        assert f["kernels"]["corner_values"] == rational_wire([[[0, 0, 0, 1]]])
        assert f["kernels"]["tile_classes"] == [["nonnegative"]]
        assert f["certification"]["status"] == ["certified"]
        assert f["bounds"]["certified_gain"] == [fw(F(1, 2))]
        assert f["bounds"]["corner_upper"] == [fw(2)]
        assert f["comparison"]["upper_minus_certified"]["gain_gap"] == [fw(F(3, 2))]
        for coefficients, kind in (([0, -1, 0, 0], "nonpositive"), ([0] * 4, "zero")):
            z = engine.build_family(one_kernel(coefficients))
            assert z["kernels"]["tile_classes"] == [[kind]]
            assert z["certification"]["status"] == ["certified"]


def test_saddle_zero_mean_preserves_both_obstruction_and_nonzero_lower(engines):
    for engine in engines:
        f = engine.build_family(saddle_problem())
        assert f["kernels"]["corner_values"] == rational_wire([[[1, -1, -1, 1]]])
        assert f["kernels"]["tile_integrals"] == rational_wire([[0]])
        assert f["certification"]["mixed_obstructions"] == [
            [{"tile": 0, "positive_corner": 0, "negative_corner": 1}]
        ]
        assert f["bounds"]["constant_lower"] == [fw(0)]
        assert f["bounds"]["bilinear_lower"] == [fw(F(2, 9))]
        assert f["bounds"]["corner_upper"] == [fw(2)]
        assert f["bounds"]["certified_gain"] == [None]
        assert f["witnesses"]["tile_constant"][0]["signs"] == [0]
        assert f["witnesses"]["bilinear"][0]["signs"] == [1, -1, -1, 1]


def test_partial_certification_maximum_domain_and_all_null_controls(engines):
    for engine in engines:
        f = engine.build_family(partial_certificate_problem())
        assert f["certification"]["status"] == ["certified", "uncertified", "certified"]
        assert f["bounds"]["certified_gain"][1] is None
        assert f["comparison"]["upper_minus_certified"]["unavailable_rows"] == [1]
        assert f["certification"]["zero_rows"] == [2]
        assert f["certification"]["integrated_zero_rows"] == [2]
        zero = engine.build_family(positive_zero_problem())
        assert zero["bounds"]["certified_gain"] == [fw(0)]
        assert zero["bounds"]["maxima"]["certified_gain"] == {"gain": fw(0), "rows": [0]}
        assert zero["witnesses"]["tile_constant"][0]["signs"] == [0]
        null = engine.build_family(mixed_problem(True))
        assert null["certification"]["status"] == ["undefined", "undefined"]
        for key, value in null["bounds"]["maxima"].items():
            assert value == {"gain": None, "rows": []}, key
        for group in ("tile_constant", "bilinear"):
            assert null["witnesses"][group] == [None, None]
        for side in ("positive", "negative"):
            e = null["witnesses"]["constant_" + side]
            assert e["normalized_error"] == [None, None] and "attained" not in e
            assert len(e["bank_error"]) == 4 and e["corners"] == rational_wire(
                [1 if side == "positive" else -1] * 4
            )
        assert null["counts"]["constant_witnesses"] == 2


@pytest.mark.parametrize(
    "factory", [unit_problem, mixed_kernel_problem, saddle_problem, positive_zero_problem]
)
def test_small_cube_lower_extrema_and_finite_upper(engines, factory):
    p = factory()
    for engine in engines:
        f = engine.build_family(p)
        outputs = []
        for c in product((-1, 1), repeat=4):
            integrated = engine.integrate(
                p["probe"], [row["bounds"] for row in p["tiles"]], rational_wire(c)
            )
            assert wire(integrated) == wire(
                integral_oracle(p["probe"], [row["bounds"] for row in p["tiles"]], rational_wire(c))
            )
            bank = integrated["raw_moments"]
            outputs.append(
                list(
                    map(fraction, engine.apply(p["decoder"], engine.produce(p["interface"], bank)))
                )
            )
        sigma = list(map(fraction, f["geometry"]["target_scales"]))
        for i in f["geometry"]["defined_rows"]:
            assert max(row[i] for row in outputs) / sigma[i] == fraction(
                f["bounds"]["bilinear_lower"][i]
            )
            assert min(row[i] for row in outputs) / sigma[i] == -fraction(
                f["bounds"]["bilinear_lower"][i]
            )
            assert all(
                abs(row[i]) / sigma[i] <= fraction(f["bounds"]["corner_upper"][i])
                for row in outputs
            )


def test_standalone_kernel_and_field_partial_empty_geometry(engines):
    probe = rational_wire([-2, 3, -1, 2])
    boxes = rational_wire([[-2, 0, -1, 0], [0, 3, -1, 0]])
    rows = rational_wire([[1, 2, -3, 4, -1, F(1, 2), F(-1, 3), 2], [0] * 8])
    corners = rational_wire([2, -3, F(1, 2), 4, -7, 1, 3, -2])
    for engine in engines:
        assert wire(engine.inspect_kernel(probe, boxes, rows)) == wire(
            kernel_oracle(probe, boxes, rows)
        )
        assert wire(engine.integrate(probe, boxes, corners)) == wire(
            integral_oracle(probe, boxes, corners)
        )
        assert engine.inspect_kernel(probe, [], [[], []]) == {
            key: [[], []] for key in kernel_oracle(probe, [], [])
        }
        assert engine.inspect_kernel(probe, boxes, []) == {
            key: [] for key in kernel_oracle(probe, [], [])
        }
        assert engine.integrate(probe, [], []) == {
            key: [] for key in integral_oracle(probe, [], [])
        }
        negative = engine.integrate(probe, boxes, [fw(-fraction(x)) for x in corners])
        positive = engine.integrate(probe, boxes, corners)
        assert negative["minima"] == [fw(-fraction(x)) for x in positive["maxima"]]
        assert negative["maxima"] == [fw(-fraction(x)) for x in positive["minima"]]


def test_required_actual_endpoint_api_call_multisets(engines, monkeypatch):
    from collections import Counter

    for engine in engines:
        for p in (
            mixed_kernel_problem(),
            opposite_tiles_problem(),
            mixed_problem(True),
            empty_receiver_problem(),
        ):
            recorded = {name: [] for name in ("integrate", "produce", "apply")}
            with monkeypatch.context() as patch:
                for name, entries in recorded.items():
                    original = getattr(engine, name)

                    def spy(*args, original=original, entries=entries):
                        entries.append(wire(list(args)))
                        return original(*args)

                    patch.setattr(engine, name, spy)
                f = engine.build_family(p)
            required = {name: [] for name in recorded}
            endpoints = [
                row[side]
                for group in ("tile_constant", "bilinear")
                for row in f["witnesses"][group]
                if row is not None
                for side in ("positive", "negative")
            ]
            endpoints += [f["witnesses"]["constant_" + side] for side in ("positive", "negative")]
            for e in endpoints:
                required["integrate"].append(
                    wire([p["probe"], [x["bounds"] for x in p["tiles"]], e["corners"]])
                )
                for a in (p["interface"], p["geometric"]):
                    required["produce"].append(wire([a, e["bank_error"]]))
                required["apply"].append(wire([p["decoder"], e["observed_error"]]))
            d = len(f["geometry"]["defined_rows"])
            assert {key: len(value) for key, value in required.items()} == {
                "integrate": 4 * d + 2,
                "produce": 8 * d + 4,
                "apply": 4 * d + 2,
            }
            for name, values in required.items():
                actual, want = Counter(recorded[name]), Counter(values)
                assert all(actual[key] >= n for key, n in want.items())


def test_file_blind_raw_apis_no_intercept_aliases_and_detached_outputs(engines, monkeypatch):
    def forbidden(*args, **kwargs):
        raise RuntimeError("unexpected file access")

    for engine in engines:
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            assert engine.produce([], []) == engine.apply([], []) == []
            assert (
                engine.produce([[], []], []) == engine.apply([[], []], []) == rational_wire([0, 0])
            )
            with pytest.raises(TypeError):
                engine.apply([fw(0)], [[fw(1)]], [fw(1)])
            p = mixed_problem()
            p["tiles"][0] = p["cells"][0]
            p["interface"][1] = p["interface"][0]
            before = wire(p)
            f = engine.build_family(p)
            f["problem"]["tiles"][0]["bounds"][0][0] = 99
            f["witnesses"]["tile_constant"][0]["positive"]["corners"][0][0] = 99
            assert wire(p) == before
            assert f["witnesses"]["tile_constant"][0]["negative"]["corners"][0] == fw(-1)
            assert wire(engine.build_family(p)) == wire(expected(p))
            tiles = [p["tiles"][0]["bounds"]]
            c = rational_wire([1, 2, 3, 4])
            snapshot = wire([tiles, c])
            got = engine.integrate(p["probe"], tiles, c)
            got["raw_moments"][0][0] = 99
            assert wire([tiles, c]) == snapshot


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


@pytest.mark.parametrize(
    "factory", [unequal_problem, partial_certificate_problem, lambda: mixed_problem(True)]
)
def test_complete_affine_transport_actual_kernel_and_fields(engines, factory):
    p = factory()
    s = len(p["interface"])
    receiver = identity(s)
    inverse = identity(s)
    if s >= 2:
        receiver[0][1] = F(1)
        inverse[0][1] = F(-1)
    moved, bank, _bank_inverse, k = affine_problem(
        p, F(3, 2), F(-7, 5), F(5, 3), F(11, 7), receiver, inverse
    )
    for engine in engines:
        first, second = engine.build_family(p), engine.build_family(moved)
        assert wire(second) == wire(expected(moved))
        assert second["certification"] == first["certification"]
        assert second["bounds"] == first["bounds"] and second["comparison"] == first["comparison"]
        assert (
            second["maps"]["normalized_bilinear_target"]
            == first["maps"]["normalized_bilinear_target"]
        )
        for key in ("corner_values", "tile_minima", "tile_maxima"):

            def scale(value):
                if len(value) == 2 and all(type(x) is int for x in value):
                    return fw(k * fraction(value))
                return [scale(x) for x in value]

            assert second["kernels"][key] == scale(first["kernels"][key])
        for key in ("tile_integrals", "bernstein_integrals", "tile_abs_upper"):
            assert second["kernels"][key] == [
                [fw(k * k * fraction(x)) for x in row] for row in first["kernels"][key]
            ]
        assert second["kernels"]["tile_classes"] == first["kernels"]["tile_classes"]
        pairs = [
            (a[side], b[side])
            for group in ("tile_constant", "bilinear")
            for a, b in zip(first["witnesses"][group], second["witnesses"][group], strict=True)
            if a is not None
            for side in ("positive", "negative")
        ]
        pairs += [
            (first["witnesses"]["constant_" + side], second["witnesses"]["constant_" + side])
            for side in ("positive", "negative")
        ]
        for a, b in pairs:
            for key in ("corners", "local_moments", "normalized_error"):
                assert b[key] == a[key]
            for key in ("local_coefficients", "tile_minima", "tile_maxima"):
                assert b[key] == [fw(k * k * fraction(x)) for x in a[key]]
            assert b["bank_error"] == encode(
                scalar_synthesize(bank, list(map(fraction, a["bank_error"])))
            )
            assert b["observed_error"] == encode(
                mv(receiver, list(map(fraction, a["observed_error"])))
            )
            for key in ("direct_error", "decoded_error"):
                assert b[key] == [fw(k**4 * fraction(x)) for x in a[key]]


def test_actual_tile_order_requires_matching_coefficient_blocks(engines):
    p = unequal_problem()
    order = [2, 0, 1]
    moved = copy.deepcopy(p)
    moved["tiles"] = [p["tiles"][i] for i in order]
    for key in ("interface", "geometric"):
        moved[key] = [[x for i in order for x in row[4 * i : 4 * i + 4]] for row in p[key]]
    for engine in engines:
        first, second = engine.build_family(p), engine.build_family(moved)
        assert wire(second) == wire(expected(moved))
        assert second["bounds"] == first["bounds"]
        for a, b in zip(
            first["kernels"]["corner_values"], second["kernels"]["corner_values"], strict=True
        ):
            assert b == [a[i] for i in order]


def test_separate_bounded_cap_edges(engines):
    unit = {"event": 0, "bounds": [0, 1, 0, 1]}
    strips = [{"event": 0, "bounds": [F(i, 256), F(i + 1, 256), 0, 1]} for i in range(256)]
    cells = [unit, *[{"event": i, "bounds": None} for i in range(1, 8)]]
    labels = [{"first": i, "second": j} for i in range(8) for j in range(8)]
    cases = [
        make_problem(unit["bounds"], [unit], strips, [], [[]]),
        make_problem(unit["bounds"], [unit], [unit], [[0] * 4] * 320, [[0] * 320]),
        make_problem(unit["bounds"], cells, [unit], [], [[]] * 64, labels),
    ]
    for engine in engines:
        assert engine.produce([[]] * 1024, []) == rational_wire([0] * 1024)
        assert engine.produce([], rational_wire([0] * 1024)) == []
        assert engine.apply([[fw(0)] * 320] * 64, [fw(0)] * 320) == rational_wire([0] * 64)
        assert engine.inspect_kernel(rational_wire([0, 1, 0, 1]), [], [[]] * 64) == {
            key: [[]] * 64 for key in kernel_oracle([], [], [])
        }
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


def malformed_integrations():
    probe = rational_wire([0, 1, 0, 1])
    tiles = [copy.deepcopy(probe)]
    corners = rational_wire([1, 2, 3, 4])
    for value in (None, (), NativeListSubclass(probe), probe[:-1]):
        yield value, tiles, corners
    for value in (None, (), NativeListSubclass(tiles), tiles * 257):
        yield probe, value, corners
    for value in (None, (), NativeListSubclass(corners), corners[:-1], corners + [fw(0)]):
        yield probe, tiles, value
    yield probe, [{"event": 0, "bounds": probe}], corners
    yield probe, [None], corners
    yield probe, [probe, probe], corners * 2
    yield probe, [rational_wire([0, 2, 0, 1])], corners
    yield probe, [rational_wire([0, 0, 0, 1])], corners
    yield probe, [rational_wire([0, 1, 1, 0])], corners
    yield rational_wire([0, 0, 0, 1]), tiles, corners
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [2, 2], [1 << 4096, 1]):
        yield probe, tiles, replaced(corners, [-1], value)
        yield probe, replaced(tiles, [0, -1], value), corners
    yield probe, [], [fw(0)]


def malformed_inspections():
    probe = rational_wire([0, 1, 0, 1])
    tiles = [copy.deepcopy(probe)]
    rows = rational_wire([[1, 2, 3, 4]])
    for value in (None, (), NativeListSubclass(probe), probe[:-1]):
        yield value, tiles, rows
    for value in (None, (), NativeListSubclass(tiles), tiles * 257):
        yield probe, value, rows
    for value in (None, (), NativeListSubclass(rows), rows * 65):
        yield probe, tiles, value
    yield probe, [{"event": 0, "bounds": probe}], rows
    yield probe, [None], rows
    yield probe, [probe, probe], rows
    yield probe, [rational_wire([0, 2, 0, 1])], rows
    yield probe, [rational_wire([0, 0, 0, 1])], rows
    yield probe, tiles, [rows[0][:-1]]
    yield probe, tiles, [tuple(rows[0])]
    for value in (True, 0.0, F(0), (0, 1), [0], [0, 0], [2, 2], [1 << 4096, 1]):
        yield probe, tiles, replaced(rows, [0, -1], value)
        yield probe, replaced(tiles, [0, -1], value), rows


def explicit_guards(engine):
    count = 0
    for p in malformed_families():
        require_rejection(lambda p=p: engine.build_family(p))
        count += 1
    for name, rowcap, widthcap in (("produce", 1024, 1024), ("apply", 64, 320)):
        call = getattr(engine, name)
        for a, x in malformed_evaluators(rowcap, widthcap):
            require_rejection(lambda a=a, x=x, call=call: call(a, x))
            count += 1
    for name, fixtures in (
        ("integrate", malformed_integrations),
        ("inspect_kernel", malformed_inspections),
    ):
        call = getattr(engine, name)
        for probe, tiles, c in fixtures():
            require_rejection(
                lambda probe=probe, tiles=tiles, c=c, call=call: call(probe, tiles, c)
            )
            count += 1
    d = 1 << 4095
    for name in ("produce", "apply"):
        call = getattr(engine, name)
        if call(rational_wire([[d, -d]]), rational_wire([2, 2])) != [fw(0)]:
            raise RuntimeError("raw product cancellation")
        require_rejection(lambda call=call: call(rational_wire([[d, d]]), rational_wire([1, 1])))
        count += 1
    shift = 1 << 1500
    cell = {"event": 0, "bounds": [shift, shift + 1, shift, shift + 1]}
    p = make_problem(cell["bounds"], [cell], [cell], [], [[]])
    if engine.build_family(p)["bounds"]["certified_gain"] != [fw(0)]:
        raise RuntimeError("retained-safe antiderivative cancellation")
    huge = 1 << 2100
    bounds = rational_wire([huge, huge + 1, huge, huge + 1])
    require_rejection(lambda: engine.integrate(bounds, [bounds], rational_wire([1] * 4)))
    count += 1
    require_rejection(
        lambda: engine.inspect_kernel(bounds, [bounds], rational_wire([[0, 0, 0, 1]]))
    )
    count += 1
    large_probe = rational_wire([0, 4, 0, 4])
    require_rejection(lambda: engine.integrate(large_probe, [large_probe], rational_wire([d] * 4)))
    count += 1
    tiny = 1 << 1400
    cell = {"event": 0, "bounds": [0, F(1, tiny), 0, 1]}
    require_rejection(
        lambda: engine.build_family(make_problem(cell["bounds"], [cell], [cell], [], [[]]))
    )
    count += 1
    cycle = []
    cycle.append(cycle)
    p = unit_problem()
    p["tiles"].append(p["tiles"])
    for call in (
        lambda: engine.build_family(p),
        lambda: engine.produce(cycle, [fw(1)]),
        lambda: engine.apply([[fw(1)]], cycle),
        lambda: engine.integrate(rational_wire([0, 1, 0, 1]), [], cycle),
        lambda: engine.inspect_kernel(rational_wire([0, 1, 0, 1]), [], cycle),
    ):
        require_rejection(call)
        count += 1
    return count


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
            require_rejection(lambda value=value: engine.produce([[fw(1)], [value]], [fw(2)]))
            require_rejection(lambda value=value: engine.apply([[fw(1)], [value]], [fw(2)]))
            require_rejection(
                lambda value=value: engine.integrate(
                    rational_wire([0, 1, 0, 1]),
                    [rational_wire([0, 1, 0, 1])],
                    [fw(1)] * 3 + [value],
                )
            )
            require_rejection(
                lambda value=value: engine.inspect_kernel(
                    rational_wire([0, 1, 0, 1]),
                    [rational_wire([0, 1, 0, 1])],
                    [[fw(1)] * 3 + [value]],
                )
            )
    finally:
        engine._fraction = original
    names = [
        name
        for name in (
            "_geometry",
            "_partition",
            "_area",
            "_physical_integral",
            "_dot",
            "_mm",
            "_integration_geometry",
            "_integrals",
            "_moments",
            "_probe_maps",
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
        require_rejection(lambda: engine.produce([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(lambda: engine.apply([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(
            lambda: engine.integrate(
                rational_wire([0, 1, 0, 1]), [rational_wire([0, 1, 0, 1])], [fw(1)] * 3 + [[1, 0]]
            )
        )
        require_rejection(
            lambda: engine.inspect_kernel(
                rational_wire([0, 1, 0, 1]), [rational_wire([0, 1, 0, 1])], [[fw(1)] * 3 + [[1, 0]]]
            )
        )
    finally:
        for name, original in originals.items():
            setattr(engine, name, original)
    if calls:
        raise RuntimeError("late admission ordering")
    return 15


def test_explicit_native_geometry_and_retained_bit_guards(engines):
    counts = [explicit_guards(engine) for engine in engines]
    assert counts[0] == counts[1] and counts[0] > 200
    assert [pre_arithmetic_guards(engine) for engine in engines] == [15, 15]


@pytest.mark.parametrize("optimized", [False, True])
def test_isolated_explicit_normal_and_optimized_guards(tmp_path, optimized):
    script = r"""
import importlib.util,json,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("ay_guard_tests",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05ay_guard_"+name,file)
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
        timeout=180,
    )
    total = (
        len(list(malformed_families()))
        + len(list(malformed_evaluators(1024, 1024)))
        + len(list(malformed_evaluators(64, 320)))
        + len(list(malformed_integrations()))
        + len(list(malformed_inspections()))
        + 26
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
    "AX_problem_equal": True,
    "AX_geometry_equal": True,
    "AX_bilinear_map_equal": True,
    "AX_bilinear_gain_equal": True,
    "AX_constant_response_equal": True,
    "same_response_maps": True,
    "broader_field_error_domain": True,
    "AX_endpoints_replayed": False,
    "other_historical_mathematics_replayed": False,
    "older_executors_run": False,
}


def changed_fraction(tree, path):
    value = tree
    for key in path:
        value = value[key]
    return replaced(tree, path, fw(fraction(value) + 1) if value is not None else fw(0))


def family_mutations(f):
    # One representative value per scientific field; full literal arithmetic is checked separately.
    for key in f:
        yield {k: v for k, v in f.items() if k != key}
    yield {**f, "extra": 0}
    yield changed_fraction(f, ["problem", "probe", 0])
    for key, value in f["geometry"].items():
        if key in ("defined_rows", "undefined_rows"):
            yield replaced(f, ["geometry", key], [*value, -1])
        elif key == "volume":
            yield changed_fraction(f, ["geometry", key])
        else:
            yield changed_fraction(f, ["geometry", key, 0])
    for key in f["kernels"]:
        path = ["kernels", key, 0, 0]
        if key == "corner_values":
            yield changed_fraction(f, path + [0])
        elif key == "tile_classes":
            yield replaced(f, path, "wrong")
        else:
            yield changed_fraction(f, path)
    for key, value in f["maps"].items():
        path = ["maps", key]
        yield changed_fraction(f, path + [0, 0]) if value[0] else replaced(f, path, [[fw(0)]])
    for key, value in f["bounds"].items():
        if key == "maxima":
            for name, maximum in value.items():
                yield changed_fraction(f, ["bounds", "maxima", name, "gain"])
                yield replaced(f, ["bounds", "maxima", name, "rows"], [*maximum["rows"], -1])
        else:
            yield changed_fraction(f, ["bounds", key, 0])
    for key, value in f["certification"].items():
        if key == "status":
            yield replaced(f, ["certification", key, 0], "wrong")
        elif key == "mixed_obstructions":
            yield replaced(
                f,
                ["certification", key, 0],
                [*value[0], {"tile": -1, "positive_corner": 0, "negative_corner": 1}],
            )
            found = next(((i, j) for i, row in enumerate(value) for j, _ in enumerate(row)), None)
            if found is not None:
                i, j = found
                for name in ("tile", "positive_corner", "negative_corner"):
                    yield replaced(f, ["certification", key, i, j, name], -1)
        else:
            yield replaced(f, ["certification", key], [*value, -1])
    for group in ("tile_constant", "bilinear"):
        rows = f["witnesses"][group]
        yield replaced(f, ["witnesses", group], rows[:-1])
        i = next((i for i, row in enumerate(rows) if row is not None), None)
        if i is not None:
            row = rows[i]
            path = ["witnesses", group, i]
            yield replaced(f, path + ["target_row"], -1)
            yield replaced(f, path + ["signs", 0], False)
            for key, values in row["positive"].items():
                where = path + ["positive", key]
                if key == "attained":
                    yield changed_fraction(f, where)
                elif values:
                    yield changed_fraction(f, where + [0])
                else:
                    yield replaced(f, where, [fw(0)])
            yield changed_fraction(f, path + ["negative", "attained"])
        null = next((i for i, row in enumerate(rows) if row is None), None)
        if null is not None:
            yield replaced(f, ["witnesses", group, null], {})
    for key, values in f["witnesses"]["constant_positive"].items():
        path = ["witnesses", "constant_positive", key]
        yield changed_fraction(f, path + [0]) if values else replaced(f, path, [fw(0)])
    yield replaced(
        f,
        ["witnesses", "constant_negative"],
        {**f["witnesses"]["constant_negative"], "attained": fw(0)},
    )
    yield changed_fraction(f, ["witnesses", "constant_negative", "bank_error", 0])
    for group, row in f["comparison"].items():
        yield changed_fraction(f, ["comparison", group, "gain_gap", 0])
        yield changed_fraction(f, ["comparison", group, "max_gap"])
        for key in ("strict_rows", "tied_rows", "unavailable_rows", "max_gap_rows"):
            yield replaced(f, ["comparison", group, key], [*row[key], -1])
    for key in CHECKS:
        yield replaced(f, ["checks", key], False)
    for key in ("kernel_entries", "endpoint_entries", "mixed_tiles"):
        yield replaced(f, ["counts", key], f["counts"][key] + 1)


def fraction_entries(value):
    if value is None:
        return 0
    if type(value) is dict:
        return sum(fraction_entries(x) for x in value.values())
    if type(value) is list:
        if len(value) == 2 and all(type(x) is int for x in value):
            fraction(value)
            return 1
        return sum(fraction_entries(x) for x in value)
    raise AssertionError("not a scientific rational occurrence")


def literal_count_checks(f):
    p, c = f["problem"], f["counts"]
    assert c["cells"] == len(p["cells"])
    assert c["positive_cells"] == sum(row["bounds"] is not None for row in p["cells"])
    for count, values in (
        ("tiles", p["tiles"]),
        ("bank_values", p["bank_labels"]),
        ("receiver_values", p["interface"]),
        ("target_rows", p["target_labels"]),
        ("defined_rows", f["geometry"]["defined_rows"]),
        ("undefined_rows", f["geometry"]["undefined_rows"]),
    ):
        assert c[count] == len(values)
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
    assert c["kernel_entries"] == sum(
        fraction_entries(value) for key, value in f["kernels"].items() if key != "tile_classes"
    )
    assert c["map_entries"] == fraction_entries(f["maps"])
    assert c["bound_entries"] == sum(
        fraction_entries(value) for key, value in f["bounds"].items() if key != "maxima"
    ) + sum(fraction_entries(value["gain"]) for value in f["bounds"]["maxima"].values())
    assert c["comparison_entries"] == sum(
        fraction_entries(row[key])
        for row in f["comparison"].values()
        for key in ("gain_gap", "max_gap")
    )
    cert = f["certification"]
    assert c["mixed_tiles"] == sum(map(len, cert["mixed_obstructions"]))
    mappings = {
        "mixed_rows": "uncertified_rows",
        "certified_rows": "certified_rows",
        "pointwise_nonnegative_rows": "nonnegative_rows",
        "pointwise_nonpositive_rows": "nonpositive_rows",
        "pointwise_zero_rows": "zero_rows",
        **{
            key: key
            for key in (
                "integrated_nonnegative_rows",
                "integrated_nonpositive_rows",
                "integrated_zero_rows",
                "integrated_nonnegative_mixed_rows",
            )
        },
    }
    for name, key in mappings.items():
        assert c[name] == len(cert[key])
    witnesses = [
        row
        for group in ("tile_constant", "bilinear")
        for row in f["witnesses"][group]
        if row is not None
    ]
    assert c["endpoint_entries"] == sum(
        fraction_entries(row[side]) for row in witnesses for side in ("positive", "negative")
    )
    for group, key in (
        ("tile_constant", "tile_sign_entries"),
        ("bilinear", "bilinear_sign_entries"),
    ):
        rows = [row for row in f["witnesses"][group] if row is not None]
        assert c[group + "_witnesses"] == 2 * len(rows)
        assert c[key] == sum(len(row["signs"]) for row in rows)
    assert c["constant_witnesses"] == 2
    assert c["constant_endpoint_entries"] == sum(
        fraction_entries(f["witnesses"]["constant_" + side]) for side in ("positive", "negative")
    )
    for name, key in (
        ("constant_gap_strict", "bilinear_minus_constant"),
        ("upper_gap_strict", "upper_minus_bilinear"),
        ("certified_upper_gap_strict", "upper_minus_certified"),
    ):
        assert c[name] == len(f["comparison"][key]["strict_rows"])
    for name, key in (
        ("constant", "constant_lower"),
        ("bilinear", "bilinear_lower"),
        ("upper", "corner_upper"),
        ("certified", "certified_gain"),
    ):
        assert c[name + "_maximizers"] == len(f["bounds"]["maxima"][key]["rows"])
    assert len(c) == 39


def test_generic_whole_wire_corruptions_and_complete_literal_counts(runner):
    for factory in (partial_certificate_problem, mixed_kernel_problem, lambda: mixed_problem(True)):
        f = expected(factory())
        literal_count_checks(f)
        original = wire(f)
        for bad in family_mutations(f):
            assert wire(bad) != original
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)


def independent_history_checks(families, previous):
    assert [f["problem"]["family"] for f in previous] == list(FAMILIES)
    for f, old in zip(families, previous, strict=True):
        assert wire(f["problem"]) == wire(old["problem"])
        assert wire(f["geometry"]) == wire(old["geometry"])
        assert f["maps"]["raw_bilinear_target"] == old["maps"]["target_error"]
        assert f["maps"]["normalized_bilinear_target"] == old["maps"]["normalized_target"]
        assert f["bounds"]["bilinear_lower"] == old["field"]["row_gains"]
        assert (
            f["witnesses"]["constant_positive"]["normalized_error"]
            == old["positivity"]["constant_response"]
        )
        literal_count_checks(f)


def payload(families):
    keys = {
        "input": "problem",
        "geometry": "geometry",
        "kernel": "kernels",
        "map": "maps",
        "bound": "bounds",
        "certification": "certification",
        "witness": "witnesses",
        "comparison": "comparison",
    }
    return [
        {
            "family": f["problem"]["family"],
            **{name + "_bytes": len(wire(f[key])) for name, key in keys.items()},
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


def synthetic_history(f):
    # Project only new synthetic selected quantities, never construct old Q/W or endpoints.
    return {
        "problem": copy.deepcopy(f["problem"]),
        "geometry": copy.deepcopy(f["geometry"]),
        "maps": {
            "target_error": copy.deepcopy(f["maps"]["raw_bilinear_target"]),
            "normalized_target": copy.deepcopy(f["maps"]["normalized_bilinear_target"]),
        },
        "field": {
            "row_gains": copy.deepcopy(f["bounds"]["bilinear_lower"]),
            "witnesses": "not replayed",
        },
        "positivity": {
            "constant_response": copy.deepcopy(
                f["witnesses"]["constant_positive"]["normalized_error"]
            ),
            "constant_positive": "not replayed",
        },
        "coordinates": "not replayed",
        "baseline": "not replayed",
        "enclosure": "not replayed",
        "comparison": "not replayed",
        "checks": "not replayed",
    }


def test_synthetic_history_full_suite_and_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(
        FAMILIES, (partial_certificate_problem, lambda: mixed_problem(True)), strict=True
    ):
        p = factory()
        p["family"] = name
        problems.append(p)
    families = list(map(expected, problems))
    previous = list(map(synthetic_history, families))
    independent_history_checks(families, previous)
    wanted = expected_suite(families)
    lookup = {f["problem"]["family"]: f for f in families}
    monkeypatch.setattr(
        runner,
        "project_inputs",
        lambda prior: ([copy.deepcopy(x["problem"]) for x in prior], prior),
    )
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
    bad = replaced(previous, [0, "field", "witnesses"], "changed")
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
    previous = [{"problem": copy.deepcopy(p)} for _ in FAMILIES]
    for name, family in zip(FAMILIES, previous, strict=True):
        family["problem"]["family"] = name
    before = wire(previous)
    projected, consumed = runner.project_inputs(previous)
    assert consumed is previous and projected == [row["problem"] for row in previous]
    projected[0]["tiles"][0]["bounds"][0][0] = 999
    assert wire(previous) == before
    changes = [
        {},
        previous[:1],
        list(reversed(previous)),
        replaced(previous, [0, "problem"], {**previous[0]["problem"], "extra": 0}),
        replaced(previous, [0, "problem", "tiles"], []),
        replaced(previous, [0, "problem", "bank_labels"], []),
        replaced(previous, [0, "problem", "target_labels"], []),
        replaced(previous, [0, "problem", "decoder", -1], []),
        replaced(previous, [0, "problem", "cells"], []),
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
def test_fixed_full_independent_kernel_oracle_and_endpoint_samples(engines, fixed_data, index):
    problems, _, wanted, _ = fixed_data
    for engine in engines:
        p = copy.deepcopy(problems[index])
        before = wire(p)
        f = engine.build_family(p)
        assert wire(p) == before and wire(f) == wire(wanted[index])
        boxes = [row["bounds"] for row in p["tiles"]]
        assert engine.inspect_kernel(p["probe"], boxes, p["geometric"]) == f["kernels"]
        # Entire endpoint wires were compared above; re-execute bounded representative
        # endpoint pipelines here, with complete generic call-inventory checks elsewhere.
        endpoints = []
        for group in ("tile_constant", "bilinear"):
            row = next((row for row in f["witnesses"][group] if row is not None), None)
            if row is not None:
                endpoints.extend(row[side] for side in ("positive", "negative"))
        endpoints.extend(f["witnesses"]["constant_" + side] for side in ("positive", "negative"))
        for e in endpoints:
            integrated = engine.integrate(p["probe"], boxes, e["corners"])
            assert integrated["raw_moments"] == e["bank_error"]
            assert integrated["local_moments"] == e["local_moments"]
            for key in ("local_coefficients", "global_coefficients"):
                assert integrated[key] == e[key]
            assert (
                integrated["minima"] == e["tile_minima"]
                and integrated["maxima"] == e["tile_maxima"]
            )
            observed = engine.produce(p["interface"], e["bank_error"])
            assert observed == e["observed_error"]
            assert engine.produce(p["geometric"], e["bank_error"]) == e["direct_error"]
            assert engine.apply(p["decoder"], observed) == e["direct_error"] == e["decoded_error"]


def test_fixed_full_suite_payload_and_selected_bilinear_history(runner, fixed_data):
    problems, previous, families, wanted = fixed_data
    assert wire(runner.assemble_suite(families, previous)) == wire(wanted)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert runner.payload_sizes(families) == payload(families)
    for p, f in zip(problems, families, strict=True):
        assert len(p["cells"]) == 8 and len(p["tiles"]) == 12
        assert (
            len(p["bank_labels"]) == 48
            and len(p["target_labels"]) == 64
            and len(p["interface"]) == 37
        )
        d = len(f["geometry"]["defined_rows"])
        assert f["counts"]["endpoint_entries"] == 4 * d * (240 + 24 + 37 + 128 + d + 1)
        assert f["counts"]["constant_endpoint_entries"] == 2 * (240 + 24 + 37 + 128 + d)
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


def test_fixed_bounded_family_and_suite_corruptions_are_nonvacuous(runner, fixed_data):
    _, _, families, wanted = fixed_data
    for f in families:
        original = wire(f)
        for bad in family_mutations(f):
            assert wire(bad) != original
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)
    changes = [
        replaced(wanted, ["families"], list(reversed(families))),
        replaced(wanted, ["prior_bridges", "AX_bilinear_map_equal"], False),
        replaced(wanted, ["prior_bridges", "AX_endpoints_replayed"], True),
        replaced(
            wanted,
            ["payload_sizes", 0, "kernel_bytes"],
            wanted["payload_sizes"][0]["kernel_bytes"] + 1,
        ),
        replaced(wanted, ["totals", "certified_rows"], wanted["totals"]["certified_rows"] + 1),
        replaced(wanted, ["scope", "mixed_absolute_kernel_integrated"], True),
        replaced(wanted, ["scope", "uncertified_exact_gain_claimed"], True),
        {**wanted, "extra": 0},
    ]
    for bad in changes:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)


def selected_history_mutations(previous):
    for path in (
        [0, "problem", "probe", 0],
        [0, "problem", "interface", 0, 0],
        [0, "problem", "geometric", 0, 0],
        [0, "problem", "decoder", 0, 0],
        [0, "geometry", "volume"],
        [0, "maps", "target_error", 0, 0],
        [0, "field", "row_gains", 0],
        [0, "positivity", "constant_response", 0],
    ):
        yield changed_fraction(previous, path)
    i = next(
        (i for i, row in enumerate(previous[0]["maps"]["normalized_target"]) if row is not None),
        None,
    )
    if i is None:
        yield replaced(previous, [0, "maps", "normalized_target", 0], [fw(0)])
    else:
        yield changed_fraction(previous, [0, "maps", "normalized_target", i, 0])
    yield replaced(previous, [0, "problem", "target_labels", 0, "first"], False)
    yield replaced(previous, [0, "problem", "bank_labels", 0, "basis"], False)


def test_fixed_selected_problem_geometry_and_bilinear_history_mutations(runner, fixed_data):
    _, previous, families, _ = fixed_data
    for bad in selected_history_mutations(previous):
        assert wire(bad) != wire(previous)
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)


def test_fixed_unselected_ax_endpoint_coordinate_and_enclosure_not_replayed(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    changes = [
        replaced(previous, [0, "field", "witnesses"], []),
        replaced(previous, [0, "positivity", "constant_positive"], {"not": "read"}),
        replaced(previous, [0, "coordinates"], {"not": "read"}),
        replaced(previous, [0, "baseline"], {"not": "read"}),
        replaced(previous, [0, "enclosure"], {"not": "read"}),
        replaced(previous, [0, "comparison"], {"not": "read"}),
        replaced(previous, [0, "checks"], {"not": "read"}),
    ]
    for bad in changes:
        assert wire(bad) != wire(previous)
        assert runner.project_inputs(bad)[0] == problems
        assert runner.historical_bridges(families, bad) == BRIDGES


def test_fixed_source_and_ancestor_identity_inventory(runner):
    current = runner.identities()
    assert {key: len(current[key]) for key in current} == {
        "source_ledger": 5,
        "prior_artifacts": 55,
        "ancestor_sources": 94,
    }
    assert set(current["source_ledger"]) == set(runner.SOURCES)
    raw = runner.AX.read_bytes()
    assert (
        len(raw) == 1925803
        and hashlib.sha256(raw).hexdigest()
        == "80020730e21d2c5731b6f6d5a94add1faa6739c815ac3e82087126d45667f1b0"
    )
    for name, want in current["source_ledger"].items():
        raw = (HERE / name).read_bytes()
        assert len(raw) == want["bytes"] and hashlib.sha256(raw).hexdigest() == want["sha256"]
