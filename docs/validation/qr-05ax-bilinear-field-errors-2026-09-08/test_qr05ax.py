"""Independent integrated bilinear-field and exact error-box checks.

Only test names containing fixed consume authenticated AW cases. Collection and generic
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
        load("_qr05ax_test_primary", "kernel.py"),
        load("_qr05ax_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05ax_test_runner", "study.py")


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
    "moment_integrals",
    "moment_inverse",
    "local_box_containment",
    "frozen_bank_identity",
    "error_map_identity",
    "baseline_dominance",
    "normalization_domain",
    "field_bound",
    "field_pipeline",
    "field_attainment",
    "enclosure_box",
    "enclosure_attainment",
    "constant_fields",
    "coefficient_sign_partition",
    "complete_gain_partitions",
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
    "stochastic_independence_assumed",
    "total_source_nonnegativity_guaranteed",
    "global_field_continuity_required",
    "arbitrary_bounded_field_sharpness_claimed",
    "common_bank_feasibility_solved",
    "same_error_domain_as_AW_claimed",
    "equal_noise_sensor_improvement_claimed",
    "field_coordinate_dimension_reduced",
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


def baseline_oracle(problem):
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
    q, r, s = len(g), len(g[0]), len(b)
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

    return encode(
        {
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
            "baseline": {
                "interface_error": h,
                "target_error": j,
                "normalized_target": a,
                "receiver_radii": beta,
                "shared_gains": alpha,
                "enclosure_gains": gamma,
            },
            "decoder_bank": k,
        }
    )


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


def corner_maps():
    columns = []
    for corner in range(4):
        coefficients = field_polynomial([F(i == corner) for i in range(4)])
        columns.append([integrate_unit(coefficients, m) for m in BASIS])
    q = [list(row) for row in zip(*columns, strict=True)]
    # Invert the independent one-axis integral matrix analytically, then tensor it.
    moments = [[F(1, 2), F(1, 2)], [F(1, 6), F(1, 3)]]
    determinant = moments[0][0] * moments[1][1] - moments[0][1] * moments[1][0]
    inverse = [
        [moments[1][1] / determinant, -moments[0][1] / determinant],
        [-moments[1][0] / determinant, moments[0][0] / determinant],
    ]
    u = [[inverse[a][i] * inverse[b][j] for i, j in BASIS] for a, b in CORNERS]
    assert scalar_product(q, u, 4) == scalar_product(u, q, 4) == identity(4)
    return q, u


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


def compare_gains(high, low, undefined):
    domain = [i for i in range(len(high)) if i not in undefined]
    gap = [high[i] - low[i] if i in domain else None for i in range(len(high))]
    assert all(gap[i] >= 0 for i in domain)
    maximum = max(gap[i] for i in domain) if domain else None
    result = {
        "gain_gap": gap,
        "strict_rows": [i for i in domain if gap[i] > 0],
        "tied_rows": [i for i in domain if gap[i] == 0],
        "max_gap": maximum,
        "max_gap_rows": [i for i in domain if gap[i] == maximum],
    }
    return result


def expected(problem):
    base = baseline_oracle(problem)
    geometry, coords, baseline = base["geometry"], base["coordinates"], base["baseline"]
    sigma = list(map(fraction, geometry["target_scales"]))
    defined, undefined = geometry["defined_rows"], geometry["undefined_rows"]
    b, g, d = (matrix(problem[key]) for key in ("interface", "geometric", "decoder"))
    q, r, s, t = len(g), len(g[0]), len(b), len(problem["tiles"])
    amp = fraction(geometry["volume"]) ** 2
    w, z = (
        [matrix(block) for block in coords[key]] for key in ("raw_from_local", "local_from_raw")
    )
    moment, inverse = corner_maps()
    rho = [sum(row, F()) for row in moment]
    assert all(x >= 0 for row in moment for x in row) and all(0 < x <= 1 for x in rho)
    raw = [scalar_product(block, moment, 4) for block in w]
    h, j = right_blocks(b, raw), right_blocks(g, raw)
    ell = scalar_product(d, h, r)
    assert ell == j
    a = [([x / sigma[i] for x in j[i]] if i in defined else None) for i in range(q)]
    beta = [sum(map(abs, row), F()) for row in h]
    e = [
        ([d[i][l] * beta[l] / sigma[i] for l in range(s)] if i in defined else None)
        for i in range(q)
    ]
    alpha = [sum(map(abs, row), F()) if row is not None else None for row in a]
    gamma = [sum(map(abs, row), F()) if row is not None else None for row in e]
    alpha0 = [fraction(x) if x is not None else None for x in baseline["shared_gains"]]
    gamma0 = [fraction(x) if x is not None else None for x in baseline["enclosure_gains"]]
    beta0 = list(map(fraction, baseline["receiver_radii"]))
    assert all((alpha[i] == 0) == (alpha0[i] == 0) for i in defined)
    comparisons = {
        name: {**compare_gains(high, low, undefined), "undefined_rows": undefined[:]}
        for name, high, low in (
            ("field_vs_enclosure", gamma, alpha),
            ("field_vs_local", alpha0, alpha),
            ("enclosure_vs_local", gamma0, gamma),
        )
    }
    comparisons["receiver_reduction"] = compare_gains(beta0, beta, [])
    bounds = [row["bounds"] for row in problem["tiles"]]

    def endpoint(corners, target=None):
        integrated = integral_oracle(problem["probe"], bounds, encode(corners))
        local = scalar_synthesize([moment] * t, corners)
        bank = scalar_synthesize(raw, corners)
        assert integrated["local_moments"] == encode(local)
        assert integrated["raw_moments"] == encode(bank)
        roundtrip = scalar_synthesize(z, bank)
        reverse = scalar_synthesize([inverse] * t, roundtrip)
        assert roundtrip == local and reverse == corners
        observed = scalar_apply(b, bank)
        direct = scalar_apply(g, bank)
        decoded = scalar_apply(d, observed)
        normalized = [decoded[i] / sigma[i] if i in defined else None for i in range(q)]
        assert observed == scalar_apply(h, corners) and direct == decoded
        assert all(abs(observed[i]) <= beta[i] for i in range(s))
        assert all(abs(normalized[i]) <= alpha[i] for i in defined)
        assert all(
            -amp <= fraction(x) <= amp for key in ("minima", "maxima") for x in integrated[key]
        )
        result = {
            "corners": corners,
            "local_coefficients": integrated["local_coefficients"],
            "global_coefficients": integrated["global_coefficients"],
            "local_moments": local,
            "bank_error": bank,
            "integrated_bank_error": integrated["raw_moments"],
            "roundtrip_local": roundtrip,
            "roundtrip_corners": reverse,
            "tile_minima": integrated["minima"],
            "tile_maxima": integrated["maxima"],
            "observed_error": observed,
            "direct_error": direct,
            "decoded_error": decoded,
            "normalized_error": normalized,
        }
        if target is not None:
            result["attained"] = normalized[target]
        return result

    field, enclosure = [None] * q, [None] * q
    for i in defined:
        signs = list(map(sign, a[i]))
        outer_signs = list(map(sign, e[i]))
        inner, outer = {}, {}
        for side, direction in (("positive", 1), ("negative", -1)):
            c = [F(direction * x) for x in signs]
            inner[side] = endpoint(c, i)
            assert inner[side]["attained"] == direction * alpha[i]
            eta = [direction * beta[l] * outer_signs[l] for l in range(s)]
            decoded = scalar_apply(d, eta)
            normalized = [decoded[z] / sigma[z] if z in defined else None for z in range(q)]
            assert normalized[i] == direction * gamma[i]
            assert all(abs(normalized[z]) <= gamma[z] for z in defined)
            outer[side] = {
                "observed_error": eta,
                "decoded_error": decoded,
                "normalized_error": normalized,
                "attained": normalized[i],
            }
        field[i] = {"target_row": i, "signs": signs, **inner}
        enclosure[i] = {"target_row": i, "signs": outer_signs, **outer}
    positive, negative = endpoint([F(1)] * r), endpoint([F(-1)] * r)
    responses = [sum(a[i], F()) if i in defined else None for i in range(q)]
    assert positive["normalized_error"] == responses
    assert negative["normalized_error"] == [-x if x is not None else None for x in responses]
    nonnegative = [i for i in defined if all(x >= 0 for x in a[i])]
    nonpositive = [i for i in defined if all(x <= 0 for x in a[i])]
    zeros = [i for i in defined if not any(a[i])]
    mixed = [i for i in defined if i not in nonnegative and i not in nonpositive]
    maxima = [max(v[i] for i in defined) if defined else None for v in (alpha, gamma)]
    sets = [[i for i in defined if v[i] == m] for v, m in zip((alpha, gamma), maxima, strict=True)]
    nd = len(defined)
    counts = {
        "cells": len(problem["cells"]),
        "positive_cells": sum(row["bounds"] is not None for row in problem["cells"]),
        "tiles": t,
        "bank_values": r,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": nd,
        "undefined_rows": q - nd,
        "geometry_input_entries": 4
        + 4 * sum(row["bounds"] is not None for row in problem["cells"])
        + 4 * t,
        "input_matrix_entries": s * r + q * r + q * s,
        "geometry_entries": 1 + len(problem["cells"]) + t + q,
        "coordinate_entries": 49 * t + 36,
        "baseline_entries": (s + q + nd) * r + s + 2 * nd,
        "map_entries": 5 * q * r + s * r + nd * (r + s),
        "gain_entries": s + 2 * nd + (2 if nd else 0),
        "comparison_entries": 3 * nd + s + (3 if nd else 0) + (1 if s else 0),
        "positivity_entries": nd,
        "field_witnesses": 2 * nd,
        "field_sign_entries": nd * r,
        "field_witness_entries": 2 * nd * (8 * r + 2 * t + s + 2 * q + nd + 1),
        "enclosure_witnesses": 2 * nd,
        "enclosure_sign_entries": nd * s,
        "enclosure_witness_entries": 2 * nd * (s + q + nd + 1),
        "constant_witnesses": 2,
        "constant_witness_entries": 2 * (8 * r + 2 * t + s + 2 * q + nd),
        "field_maximizers": len(sets[0]),
        "enclosure_maximizers": len(sets[1]),
        "field_enclosure_strict": len(comparisons["field_vs_enclosure"]["strict_rows"]),
        "field_local_strict": len(comparisons["field_vs_local"]["strict_rows"]),
        "enclosure_local_strict": len(comparisons["enclosure_vs_local"]["strict_rows"]),
        "receiver_strict": len(comparisons["receiver_reduction"]["strict_rows"]),
        "nonnegative_rows": len(nonnegative),
        "nonpositive_rows": len(nonpositive),
        "mixed_rows": len(mixed),
        "zero_rows": len(zeros),
    }
    return encode(
        {
            "problem": copy.deepcopy(problem),
            "geometry": geometry,
            "coordinates": {
                **coords,
                "local_from_corner": moment,
                "corner_from_local": inverse,
                "raw_from_corner": raw,
                "corner_moment_row_sums": rho,
            },
            "baseline": baseline,
            "maps": {
                "decoder_bank": base["decoder_bank"],
                "bank_residual": [[F()] * r for _ in range(q)],
                "interface_error": h,
                "target_error": j,
                "decoded_error": ell,
                "error_residual": [[F()] * r for _ in range(q)],
                "normalized_target": a,
                "enclosure_target": e,
            },
            "field": {
                "row_gains": alpha,
                "witnesses": field,
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
            "comparison": comparisons,
            "positivity": {
                "nonnegative_rows": nonnegative,
                "nonpositive_rows": nonpositive,
                "mixed_rows": mixed,
                "zero_rows": zeros,
                "constant_response": responses,
                "positive_constant_attains": [i for i in defined if responses[i] == alpha[i]],
                "negative_constant_attains": [i for i in defined if -responses[i] == alpha[i]],
                "constant_positive": positive,
                "constant_negative": negative,
            },
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


@pytest.mark.parametrize(
    "factory",
    [
        unit_problem,
        unequal_problem,
        thin_problem,
        mixed_problem,
        lambda: mixed_problem(True),
        positive_zero_problem,
        empty_receiver_problem,
    ],
)
def test_complete_independent_polynomial_family_wires(engines, factory):
    p = factory()
    want = expected(p)
    for engine in engines:
        snapshot = copy.deepcopy(p)
        got = engine.build_family(p)
        assert wire(got) == wire(want)
        assert p == snapshot


def test_unit_corner_order_integrals_and_gap_need_not_shrink(engines):
    q, u = corner_maps()
    assert q == matrix(
        [
            [fw(F(1, 4))] * 4,
            [fw(F(1, 12)), fw(F(1, 6)), fw(F(1, 12)), fw(F(1, 6))],
            [fw(F(1, 12)), fw(F(1, 12)), fw(F(1, 6)), fw(F(1, 6))],
            [fw(F(1, 36)), fw(F(1, 18)), fw(F(1, 18)), fw(F(1, 9))],
        ]
    )
    assert q != u and scalar_product(q, u, 4) == identity(4)
    for engine in engines:
        f = engine.build_family(unit_problem())
        assert f["field"]["row_gains"] == [fw(F(1, 2))]
        assert f["baseline"]["shared_gains"] == [fw(8)]
        assert f["enclosure"]["row_gains"] == [fw(F(9, 2))]
        assert f["baseline"]["enclosure_gains"] == [fw(8)]
        assert f["comparison"]["field_vs_enclosure"]["gain_gap"] == [fw(4)]
        assert f["maps"]["normalized_target"] == rational_wire(
            [[F(2, 9), F(1, 9), F(1, 9), F(1, 18)]]
        )
        c = f["positivity"]["constant_positive"]
        assert c["corners"] == rational_wire([1] * 4)
        assert (
            c["local_coefficients"] == c["global_coefficients"] == rational_wire([F(1, 4), 0, 0, 0])
        )
        assert c["local_moments"] == rational_wire([1, F(1, 2), F(1, 2), F(1, 4)])
        assert c["bank_error"] == rational_wire([F(1, 8), F(1, 16), F(1, 16), F(1, 32)])
        assert c["roundtrip_local"] != c["roundtrip_corners"]
        assert c["tile_minima"] == c["tile_maxima"] == [fw(F(1, 4))]


def rational_wire(value):
    if type(value) in (list, tuple):
        return [rational_wire(x) for x in value]
    return fw(value)


def signed_problem():
    p = unit_problem()
    d = rational_wire([[-1, 2, 0, 0]])
    return p | {"geometric": d, "decoder": copy.deepcopy(d)}


def test_sign_changing_field_defeats_both_constant_controls(engines):
    for engine in engines:
        f = engine.build_family(signed_problem())
        assert wire(f) == wire(expected(signed_problem()))
        assert f["maps"]["normalized_target"] == rational_wire(
            [[F(-1, 6), F(1, 6), F(-1, 6), F(1, 6)]]
        )
        assert f["field"]["row_gains"] == [fw(F(2, 3))]
        p = f["positivity"]
        assert p["mixed_rows"] == [0]
        assert p["positive_constant_attains"] == p["negative_constant_attains"] == []
        assert p["constant_response"] == [fw(0)]
        for side in ("positive", "negative"):
            assert p["constant_" + side]["normalized_error"] == [fw(0)]
        e = f["field"]["witnesses"][0]["positive"]
        assert e["corners"] == rational_wire([-1, 1, -1, 1])
        assert e["local_coefficients"] == rational_wire([F(-1, 4), F(1, 2), 0, 0])
        assert e["tile_minima"] == [fw(F(-1, 4))] and e["tile_maxima"] == [fw(F(1, 4))]


def test_mass_higher_moment_and_all_zero_sign_ties(engines):
    for engine in engines:
        for column, gain in ((0, F(2)), (1, F(1)), (2, F(1)), (3, F(1, 2))):
            p = unit_problem()
            row = rational_wire([F(j == column) for j in range(4)])
            f = engine.build_family(p | {"geometric": [row], "decoder": [row]})
            assert f["field"]["row_gains"] == [fw(gain)]
            assert f["baseline"]["shared_gains"] == [fw(2)]
        f = engine.build_family(positive_zero_problem())
        assert f["field"]["row_gains"] == [fw(0)]
        assert f["enclosure"]["row_gains"] == [fw(4)]
        assert f["positivity"]["zero_rows"] == [0]
        for key in (
            "nonnegative_rows",
            "nonpositive_rows",
            "positive_constant_attains",
            "negative_constant_attains",
        ):
            assert f["positivity"][key] == [0]
        assert f["field"]["witnesses"][0]["signs"] == [0] * 4


def test_undefined_normalization_retains_constants_and_raw_enclosure_outputs(engines):
    for engine in engines:
        f = engine.build_family(mixed_problem())
        assert f["field"]["witnesses"][1] is None
        e = f["enclosure"]["witnesses"][0]["positive"]
        assert e["decoded_error"][1] == fw(F(1, 8)) and e["normalized_error"][1] is None
        z = engine.build_family(mixed_problem(True))
        for key in ("field", "enclosure"):
            assert z[key]["max_gain"] is None and z[key]["max_rows"] == []
            assert z[key]["witnesses"] == [None, None]
        for side in ("positive", "negative"):
            c = z["positivity"]["constant_" + side]
            assert c["corners"] == rational_wire([1 if side == "positive" else -1] * 4)
            assert c["normalized_error"] == [None, None]
            assert "attained" not in c
        assert z["counts"]["constant_witnesses"] == 2 and z["counts"]["field_witnesses"] == 0
        empty = engine.build_family(empty_receiver_problem())
        assert empty["comparison"]["receiver_reduction"] == {
            "gain_gap": [],
            "strict_rows": [],
            "tied_rows": [],
            "max_gap": None,
            "max_gap_rows": [],
        }


@pytest.mark.parametrize(
    "factory", [unit_problem, signed_problem, mixed_problem, positive_zero_problem]
)
def test_exhaustive_corner_cubes_certify_sharpness_and_containment(engines, factory):
    p = factory()
    assert len(p["tiles"]) == 1
    for engine in engines:
        f = engine.build_family(p)
        outputs = []
        observations = []
        for c in product((-1, 1), repeat=4):
            integrated = engine.integrate(p["probe"], [p["tiles"][0]["bounds"]], rational_wire(c))
            assert wire(integrated) == wire(
                integral_oracle(p["probe"], [p["tiles"][0]["bounds"]], rational_wire(c))
            )
            local = list(map(fraction, integrated["local_moments"]))
            assert all(
                abs(x) <= rho for x, rho in zip(local, (1, F(1, 2), F(1, 2), F(1, 4)), strict=True)
            )
            bank = integrated["raw_moments"]
            obs = engine.produce(p["interface"], bank)
            observations.append(list(map(fraction, obs)))
            outputs.append(list(map(fraction, engine.apply(p["decoder"], obs))))
        for j, beta in enumerate(f["enclosure"]["receiver_radii"]):
            assert max(abs(row[j]) for row in observations) == fraction(beta)
        for i in f["geometry"]["defined_rows"]:
            sigma = fraction(f["geometry"]["target_scales"][i])
            assert max(row[i] for row in outputs) / sigma == fraction(f["field"]["row_gains"][i])
            assert min(row[i] for row in outputs) / sigma == -fraction(f["field"]["row_gains"][i])


def test_integrate_partial_empty_signed_fields_and_discontinuous_tiles(engines):
    probe = rational_wire([-2, 3, -1, 2])
    boxes = rational_wire([[-2, 0, -1, 0], [0, 3, -1, 0]])
    corners = rational_wire([2, -3, F(1, 2), 4, -7, 1, 3, -2])
    for engine in engines:
        got = engine.integrate(probe, boxes, corners)
        assert wire(got) == wire(integral_oracle(probe, boxes, corners))
        amp = volume(rect(probe)) ** 2
        assert got["minima"] == rational_wire([-3 * amp, -7 * amp])
        assert got["maxima"] == rational_wire([4 * amp, 3 * amp])
        # Neighboring boundary values differ; partial coverage is a standalone admission.
        assert corners[1] != corners[4]
        empty = engine.integrate(probe, [], [])
        assert empty == {key: [] for key in got}
        for epsilon in (F(0), F(3, 2), F(-2)):
            scaled = engine.integrate(probe, boxes, [fw(epsilon * fraction(x)) for x in corners])
            assert wire(scaled) == wire(
                integral_oracle(probe, boxes, [fw(epsilon * fraction(x)) for x in corners])
            )


def test_actual_endpoint_integrate_and_restricted_pipeline_multisets(engines, monkeypatch):
    from collections import Counter

    for engine in engines:
        for p in (signed_problem(), mixed_problem(), mixed_problem(True), empty_receiver_problem()):
            recorded = {name: [] for name in ("integrate", "synthesize", "produce", "apply")}
            originals = {name: getattr(engine, name) for name in recorded}
            with monkeypatch.context() as patch:
                for name, original in originals.items():

                    def spy(*args, name=name, original=original, recorded=recorded):
                        recorded[name].append(wire(list(args)))
                        return original(*args)

                    patch.setattr(engine, name, spy)
                f = engine.build_family(p)
            required = {name: [] for name in recorded}
            endpoints = [
                row[side]
                for row in f["field"]["witnesses"]
                if row is not None
                for side in ("positive", "negative")
            ]
            endpoints += [f["positivity"]["constant_" + side] for side in ("positive", "negative")]
            c = f["coordinates"]
            t = len(p["tiles"])
            for e in endpoints:
                required["integrate"].append(
                    wire([p["probe"], [x["bounds"] for x in p["tiles"]], e["corners"]])
                )
                for blocks, x in (
                    ([c["local_from_corner"]] * t, e["corners"]),
                    (c["raw_from_corner"], e["corners"]),
                    (c["local_from_raw"], e["bank_error"]),
                    ([c["corner_from_local"]] * t, e["roundtrip_local"]),
                ):
                    required["synthesize"].append(wire([blocks, x]))
                for a in (p["interface"], p["geometric"]):
                    required["produce"].append(wire([a, e["bank_error"]]))
                required["apply"].append(wire([p["decoder"], e["observed_error"]]))
            for row in f["enclosure"]["witnesses"]:
                if row is not None:
                    for side in ("positive", "negative"):
                        required["apply"].append(wire([p["decoder"], row[side]["observed_error"]]))
            d = len(f["geometry"]["defined_rows"])
            assert {k: len(v) for k, v in required.items()} == {
                "integrate": 2 * d + 2,
                "synthesize": 8 * d + 8,
                "produce": 4 * d + 4,
                "apply": 4 * d + 2,
            }
            for name, entries in required.items():
                actual, want = Counter(recorded[name]), Counter(entries)
                assert all(actual[key] >= number for key, number in want.items())


def test_raw_apis_file_blind_empty_no_intercept_and_detached(engines, monkeypatch):
    def forbidden(*args, **kwargs):
        raise RuntimeError("unexpected external read")

    for engine in engines:
        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "read_bytes", forbidden)
            patch.setattr(Path, "read_text", forbidden)
            assert engine.produce([], []) == []
            assert engine.produce([[], []], []) == rational_wire([0, 0])
            assert engine.apply([], []) == []
            assert engine.apply([[], []], []) == rational_wire([0, 0])
            assert engine.synthesize([], []) == []
            assert engine.integrate(rational_wire([0, 1, 0, 1]), [], []) == {
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
            p = unit_problem()
            snap = copy.deepcopy(p)
            f = engine.build_family(p)
            assert p == snap
            f["problem"]["probe"][0][0] = 99
            f["coordinates"]["raw_from_local"][0][0][0][0] = 99
            assert p == snap and wire(engine.build_family(p)) == wire(expected(p))
            x = rational_wire([1, 2])
            a = rational_wire([[2, 3]])
            got = engine.apply(a, x)
            got[0][0] = 99
            assert a == rational_wire([[2, 3]]) and x == rational_wire([1, 2])
            with pytest.raises(TypeError):
                engine.apply([fw(0)], a, x)


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
    out["interface"] = rational_wire(mm(receiver, right_blocks(matrix(p["interface"]), inverse)))
    out["geometric"] = rational_wire(
        [[k**4 * x for x in row] for row in right_blocks(matrix(p["geometric"]), inverse)]
    )
    out["decoder"] = rational_wire(
        [[k**4 * x for x in row] for row in mm(matrix(p["decoder"]), receiver_inverse)]
    )
    return out, blocks, inverse, k


@pytest.mark.parametrize("factory", [unequal_problem, mixed_problem, lambda: mixed_problem(True)])
def test_full_affine_transport_fields_and_same_maps(engines, factory):
    p = factory()
    receiver = [[F(1), F(1)], [F(1), F(-1)]]
    inverse = [[F(1, 2), F(1, 2)], [F(1, 2), F(-1, 2)]]
    moved, bank, bank_inverse, k = affine_problem(
        p, F(3, 2), F(-7, 5), F(5, 3), F(11, 7), receiver, inverse
    )
    for engine in engines:
        before, after = engine.build_family(p), engine.build_family(moved)
        assert wire(after) == wire(expected(moved))
        assert after["geometry"]["defined_rows"] == before["geometry"]["defined_rows"]
        assert after["geometry"]["target_scales"] == [
            fw(k**4 * fraction(x)) for x in before["geometry"]["target_scales"]
        ]
        for key in ("local_from_corner", "corner_from_local", "corner_moment_row_sums"):
            assert after["coordinates"][key] == before["coordinates"][key]
        for i in range(len(bank)):
            for key in ("raw_from_local", "raw_from_corner"):
                assert after["coordinates"][key][i] == rational_wire(
                    scalar_product(bank[i], matrix(before["coordinates"][key][i]), 4)
                )
            assert after["coordinates"]["local_from_raw"][i] == rational_wire(
                scalar_product(
                    matrix(before["coordinates"]["local_from_raw"][i]), bank_inverse[i], 4
                )
            )
        assert after["maps"]["normalized_target"] == before["maps"]["normalized_target"]
        assert after["field"]["row_gains"] == before["field"]["row_gains"]
        pairs = [
            (a[side], b[side])
            for a, b in zip(before["field"]["witnesses"], after["field"]["witnesses"], strict=True)
            if a is not None
            for side in ("positive", "negative")
        ]
        pairs += [
            (before["positivity"]["constant_" + side], after["positivity"]["constant_" + side])
            for side in ("positive", "negative")
        ]
        for a, b in pairs:
            for key in (
                "corners",
                "local_moments",
                "roundtrip_local",
                "roundtrip_corners",
                "normalized_error",
            ):
                assert b[key] == a[key]
            for key in ("local_coefficients", "tile_minima", "tile_maxima"):
                assert b[key] == [fw(k**2 * fraction(x)) for x in a[key]]
            for key in ("bank_error", "integrated_bank_error"):
                assert b[key] == rational_wire(scalar_synthesize(bank, list(map(fraction, a[key]))))
            assert b["observed_error"] == rational_wire(
                mv(receiver, list(map(fraction, a["observed_error"])))
            )
            for key in ("direct_error", "decoded_error"):
                assert b[key] == [fw(k**4 * fraction(x)) for x in a[key]]
        monomial = [[F(0), F(-3)], [F(2), F(0)]]
        mono_inverse = [[F(0), F(1, 2)], [F(-1, 3), F(0)]]
        other, _, _, _ = affine_problem(
            p, F(3, 2), F(-7, 5), F(5, 3), F(11, 7), monomial, mono_inverse
        )
        assert (
            engine.build_family(other)["enclosure"]["row_gains"] == before["enclosure"]["row_gains"]
        )


def test_tile_permutation_shared_containers_and_field_ownership(engines):
    p = unequal_problem()
    order = [2, 0, 1]
    moved = copy.deepcopy(p)
    moved["tiles"] = [p["tiles"][i] for i in order]
    for key in ("interface", "geometric"):
        moved[key] = [[x for i in order for x in row[4 * i : 4 * i + 4]] for row in p[key]]
    for engine in engines:
        old, new = engine.build_family(p), engine.build_family(moved)
        assert wire(new) == wire(expected(moved))
        for key in ("field", "enclosure"):
            assert new[key]["row_gains"] == old[key]["row_gains"]
        shared = mixed_problem()
        shared["tiles"][0] = shared["cells"][0]
        shared["interface"][1] = shared["interface"][0]
        before = wire(shared)
        got = engine.build_family(shared)
        got["field"]["witnesses"][0]["positive"]["corners"][0][0] = 99
        got["problem"]["tiles"][0]["bounds"][0][0] = 99
        assert wire(shared) == before
        assert got["field"]["witnesses"][0]["negative"]["corners"][0] == fw(-1)
        assert wire(engine.build_family(shared)) == wire(expected(shared))


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
        assert (
            engine.synthesize([rational_wire(identity(4))] * 256, [fw(0)] * 1024) == [fw(0)] * 1024
        )
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
    blocks = [rational_wire(identity(4))]
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


def explicit_guards(engine):
    count = 0
    for p in malformed_families():
        require_rejection(lambda p=p: engine.build_family(p))
        count += 1
    for a, x in malformed_syntheses():
        require_rejection(lambda a=a, x=x: engine.synthesize(a, x))
        count += 1
    for name, rowcap, widthcap in (("produce", 1024, 1024), ("apply", 64, 320)):
        call = getattr(engine, name)
        for a, x in malformed_evaluators(rowcap, widthcap):
            require_rejection(lambda a=a, x=x, call=call: call(a, x))
            count += 1
    for probe, tiles, c in malformed_integrations():
        require_rejection(lambda probe=probe, tiles=tiles, c=c: engine.integrate(probe, tiles, c))
        count += 1
    d = 1 << 4095
    for name in ("produce", "apply"):
        call = getattr(engine, name)
        if call(rational_wire([[d, -d]]), rational_wire([2, 2])) != rational_wire([0]):
            raise RuntimeError("raw product cancellation")
        require_rejection(lambda call=call: call(rational_wire([[d, d]]), rational_wire([1, 1])))
        count += 1
    block = rational_wire([[d, -d, 0, 0], [0] * 4, [0] * 4, [0] * 4])
    if engine.synthesize([block], rational_wire([2, 2, 0, 0])) != rational_wire([0] * 4):
        raise RuntimeError("block cancellation")
    require_rejection(lambda: engine.synthesize([block], rational_wire([2, -2, 0, 0])))
    count += 1
    tiny = 1 << 1400
    cell = {"event": 0, "bounds": [0, F(1, tiny), 0, 1]}
    require_rejection(
        lambda: engine.build_family(make_problem(cell["bounds"], [cell], [cell], [], [[]]))
    )
    count += 1
    # Large global antiderivative terms cancel; all retained coordinates and integrals fit.
    shift = 1 << 1500
    cell = {"event": 0, "bounds": [shift, shift + 1, shift, shift + 1]}
    p = make_problem(cell["bounds"], [cell], [cell], [], [[]])
    if engine.build_family(p)["field"]["row_gains"] != [fw(0)]:
        raise RuntimeError("retained-safe translated cancellation")
    huge = 1 << 2100
    bounds = rational_wire([huge, huge + 1, huge, huge + 1])
    require_rejection(lambda: engine.integrate(bounds, [bounds], rational_wire([1] * 4)))
    count += 1
    cell = {"event": 0, "bounds": [0, 4, 0, 4]}
    require_rejection(
        lambda: engine.integrate(
            rational_wire(cell["bounds"]), [rational_wire(cell["bounds"])], rational_wire([d] * 4)
        )
    )
    count += 1
    cycle = []
    cycle.append(cycle)
    cyclic = unit_problem()
    cyclic["tiles"].append(cyclic["tiles"])
    for call in (
        lambda: engine.build_family(cyclic),
        lambda: engine.synthesize(cycle, rational_wire([1] * 4)),
        lambda: engine.produce(cycle, [fw(1)]),
        lambda: engine.apply([[fw(1)]], cycle),
        lambda: engine.integrate(rational_wire([0, 1, 0, 1]), [], cycle),
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
            require_rejection(
                lambda value=value: engine.synthesize(
                    [replaced(rational_wire(identity(4)), [3, 3], value)], [fw(1)] * 4
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
    finally:
        engine._fraction = original
    names = [
        name
        for name in (
            "_geometry",
            "_partition",
            "_area",
            "_blocks",
            "_mm",
            "_dot",
            "_right_blocks",
            "_probe_maps",
            "_physical_integral",
            "_integration_geometry",
            "_integrals",
            "_moments",
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
            lambda: engine.synthesize(
                [replaced(rational_wire(identity(4)), [3, 3], [1, 0])], [fw(1)] * 4
            )
        )
        require_rejection(lambda: engine.produce([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(lambda: engine.apply([[fw(1)], [[1, 0]]], [fw(1)]))
        require_rejection(
            lambda: engine.integrate(
                rational_wire([0, 1, 0, 1]), [rational_wire([0, 1, 0, 1])], [fw(1)] * 3 + [[1, 0]]
            )
        )
    finally:
        for name, original in originals.items():
            setattr(engine, name, original)
    if calls:
        raise RuntimeError("late admission ordering")
    return 15


def test_native_geometry_and_retained_bit_guards(engines):
    counts = [explicit_guards(engine) for engine in engines]
    assert counts[0] == counts[1] and counts[0] > 200
    assert [pre_arithmetic_guards(engine) for engine in engines] == [15, 15]


@pytest.mark.parametrize("optimized", [False, True])
def test_isolated_explicit_normal_and_optimized_guards(tmp_path, optimized):
    script = r"""
import importlib.util,json,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("ax_guard_tests",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05ax_guard_"+name,file)
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
        + len(list(malformed_syntheses()))
        + len(list(malformed_evaluators(1024, 1024)))
        + len(list(malformed_evaluators(64, 320)))
        + len(list(malformed_integrations()))
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
    "AW_problem_equal": True,
    "AW_geometry_equal": True,
    "AW_coordinates_equal": True,
    "AW_local_baseline_equal": True,
    "same_response_maps": True,
    "new_field_error_domain": True,
    "AW_endpoints_replayed": False,
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
    for key in ("bank_scales", "corner_moment_row_sums"):
        yield changed_fraction(f, ["coordinates", key, 0])
    for key in ("raw_from_local", "local_from_raw", "raw_from_corner"):
        yield changed_fraction(f, ["coordinates", key, 0, 0, 0])
        yield replaced(f, ["coordinates", key], f["coordinates"][key][:-1])
    for key in ("local_from_corner", "corner_from_local"):
        yield changed_fraction(f, ["coordinates", key, 0, 0])
    for group in ("maps", "baseline"):
        for key, value in f[group].items():
            path = [group, key]
            if not value:
                yield replaced(f, path, [fw(0)])
            elif key in ("receiver_radii", "shared_gains", "enclosure_gains"):
                yield changed_fraction(f, path + [0])
            elif value[0] is None or not value[0]:
                yield replaced(f, path, [[fw(0)]])
            else:
                yield changed_fraction(f, path + [0, 0])
    for group in ("field", "enclosure"):
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
                    path = [group, "witnesses", index, side, key]
                    if key == "attained":
                        yield changed_fraction(f, path)
                    elif value:
                        yield changed_fraction(f, path + [0])
                    else:
                        yield replaced(f, path, [fw(0)])
        null_index = next((i for i, row in enumerate(part["witnesses"]) if row is None), None)
        if null_index is not None:
            yield replaced(f, [group, "witnesses", null_index], {})
            yield replaced(f, [group, "row_gains", null_index], fw(0))
    yield replaced(f, ["enclosure", "common_bank_feasibility_tested"], True)
    if f["enclosure"]["receiver_radii"]:
        yield changed_fraction(f, ["enclosure", "receiver_radii", 0])
    else:
        yield replaced(f, ["enclosure", "receiver_radii"], [fw(0)])
    for name, row in f["comparison"].items():
        if row["gain_gap"]:
            yield changed_fraction(f, ["comparison", name, "gain_gap", 0])
        else:
            yield replaced(f, ["comparison", name, "gain_gap"], [fw(0)])
        yield changed_fraction(f, ["comparison", name, "max_gap"])
        for key in ("strict_rows", "tied_rows", "max_gap_rows"):
            yield replaced(f, ["comparison", name, key], [*row[key], -1])
        if "undefined_rows" in row:
            yield replaced(f, ["comparison", name, "undefined_rows"], [*row["undefined_rows"], -1])
    for key, value in f["positivity"].items():
        if key.startswith("constant_") and key != "constant_response":
            for field, vector in value.items():
                path = ["positivity", key, field]
                yield changed_fraction(f, path + [0]) if vector else replaced(f, path, [fw(0)])
        elif key == "constant_response":
            yield changed_fraction(f, ["positivity", key, 0])
        else:
            yield replaced(f, ["positivity", key], [*value, -1])
    for key in CHECKS:
        yield replaced(f, ["checks", key], False)
    for key in f["counts"]:
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
    raise AssertionError("nonfraction scientific entry")


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
    for name, key in (("coordinate", "coordinates"), ("baseline", "baseline"), ("map", "maps")):
        assert c[name + "_entries"] == fraction_entries(f[key])
    assert c["gain_entries"] == fraction_entries(f["enclosure"]["receiver_radii"]) + sum(
        fraction_entries(f[group][key])
        for group in ("field", "enclosure")
        for key in ("row_gains", "max_gain")
    )
    assert c["comparison_entries"] == sum(
        fraction_entries(row[key])
        for row in f["comparison"].values()
        for key in ("gain_gap", "max_gap")
    )
    assert c["positivity_entries"] == fraction_entries(f["positivity"]["constant_response"])
    for group in ("field", "enclosure"):
        witnesses = [row for row in f[group]["witnesses"] if row is not None]
        assert c[group + "_witnesses"] == 2 * len(witnesses)
        assert c[group + "_sign_entries"] == sum(len(row["signs"]) for row in witnesses)
        assert c[group + "_witness_entries"] == sum(
            fraction_entries(row[side]) for row in witnesses for side in ("positive", "negative")
        )
        assert c[group + "_maximizers"] == len(f[group]["max_rows"])
    assert c["constant_witnesses"] == 2
    assert c["constant_witness_entries"] == sum(
        fraction_entries(f["positivity"]["constant_" + side]) for side in ("positive", "negative")
    )
    for name, key in (
        ("field_enclosure", "field_vs_enclosure"),
        ("field_local", "field_vs_local"),
        ("enclosure_local", "enclosure_vs_local"),
        ("receiver", "receiver_reduction"),
    ):
        assert c[name + "_strict"] == len(f["comparison"][key]["strict_rows"])
    for key in ("nonnegative_rows", "nonpositive_rows", "mixed_rows", "zero_rows"):
        assert c[key] == len(f["positivity"][key])


def test_generic_nonvacuous_complete_wire_mutations_and_literal_counts(runner):
    for factory in (
        unit_problem,
        mixed_problem,
        lambda: mixed_problem(True),
        empty_receiver_problem,
    ):
        f = expected(factory())
        literal_count_checks(f)
        for bad in family_mutations(f):
            assert wire(bad) != wire(f)
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)


def independent_history_checks(families, previous):
    assert [f["problem"]["family"] for f in previous] == list(FAMILIES)
    for f, old in zip(families, previous, strict=True):
        assert wire(f["problem"]) == wire(old["problem"])
        assert wire(f["geometry"]) == wire(old["geometry"])
        for key in ("bank_scales", "raw_from_local", "local_from_raw"):
            assert f["coordinates"][key] == old["coordinates"][key]
        for key in ("interface_error", "target_error", "normalized_target"):
            assert f["baseline"][key] == old["maps"][key]
        assert f["baseline"]["receiver_radii"] == old["enclosure"]["receiver_radii"]
        assert f["baseline"]["shared_gains"] == old["shared"]["row_gains"]
        assert f["baseline"]["enclosure_gains"] == old["enclosure"]["row_gains"]
        literal_count_checks(f)


def payload(families):
    keys = {
        "input": "problem",
        "geometry": "geometry",
        "coordinate": "coordinates",
        "baseline": "baseline",
        "map": "maps",
        "field": "field",
        "enclosure": "enclosure",
        "comparison": "comparison",
        "positivity": "positivity",
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


def synthetic_history(p):
    # Selected AW baseline only: no old endpoint or old executor reconstruction.
    base = baseline_oracle(p)
    b = base["baseline"]
    return {
        "problem": copy.deepcopy(p),
        "geometry": base["geometry"],
        "coordinates": base["coordinates"],
        "maps": {key: b[key] for key in ("interface_error", "target_error", "normalized_target")},
        "shared": {"row_gains": b["shared_gains"], "witnesses": "not replayed"},
        "enclosure": {
            "row_gains": b["enclosure_gains"],
            "receiver_radii": b["receiver_radii"],
            "witnesses": "not replayed",
        },
        "comparison": "not replayed",
        "checks": "not replayed",
        "counts": "not replayed",
    }


def test_synthetic_history_full_suite_and_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(FAMILIES, (mixed_problem, lambda: mixed_problem(True)), strict=True):
        p = factory()
        p["family"] = name
        problems.append(p)
    families = list(map(expected, problems))
    previous = list(map(synthetic_history, problems))
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
    bad = replaced(previous, [0, "shared", "witnesses"], "changed")
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
def test_fixed_full_polynomial_oracle_and_actual_field_integrals(engines, fixed_data, index):
    problems, _, wanted, _ = fixed_data
    for engine in engines:
        p = copy.deepcopy(problems[index])
        before = wire(p)
        f = engine.build_family(p)
        assert wire(p) == before and wire(f) == wire(wanted[index])
        fields = [
            row[side]
            for row in f["field"]["witnesses"]
            if row is not None
            for side in ("positive", "negative")
        ]
        fields += [f["positivity"]["constant_" + side] for side in ("positive", "negative")]
        for e in fields:
            integrated = engine.integrate(
                p["probe"], [row["bounds"] for row in p["tiles"]], e["corners"]
            )
            assert integrated["raw_moments"] == e["bank_error"] == e["integrated_bank_error"]
            assert integrated["local_moments"] == e["local_moments"] == e["roundtrip_local"]
            for key in ("local_coefficients", "global_coefficients"):
                assert integrated[key] == e[key]
            assert (
                integrated["minima"] == e["tile_minima"]
                and integrated["maxima"] == e["tile_maxima"]
            )
            assert (
                engine.synthesize(
                    [f["coordinates"]["corner_from_local"]] * len(p["tiles"]), e["roundtrip_local"]
                )
                == e["corners"]
                == e["roundtrip_corners"]
            )
            observed = engine.produce(p["interface"], e["bank_error"])
            assert observed == e["observed_error"]
            assert engine.produce(p["geometric"], e["bank_error"]) == e["direct_error"]
            assert engine.apply(p["decoder"], observed) == e["direct_error"] == e["decoded_error"]
        for row in f["enclosure"]["witnesses"]:
            if row is not None:
                for side in ("positive", "negative"):
                    e = row[side]
                    assert engine.apply(p["decoder"], e["observed_error"]) == e["decoded_error"]


def test_fixed_full_suite_payload_and_selected_baseline(runner, fixed_data):
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
        assert f["counts"]["field_witness_entries"] == 2 * d * (384 + 24 + 37 + 128 + d + 1)
        assert f["counts"]["enclosure_witness_entries"] == 2 * d * (37 + 64 + d + 1)
        assert f["counts"]["constant_witness_entries"] == 2 * (384 + 24 + 37 + 128 + d)
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
        replaced(wanted, ["prior_bridges", "AW_local_baseline_equal"], False),
        replaced(wanted, ["prior_bridges", "AW_endpoints_replayed"], True),
        replaced(
            wanted,
            ["payload_sizes", 0, "coordinate_bytes"],
            wanted["payload_sizes"][0]["coordinate_bytes"] + 1,
        ),
        replaced(
            wanted,
            ["totals", "constant_witness_entries"],
            wanted["totals"]["constant_witness_entries"] + 1,
        ),
        replaced(wanted, ["scope", "same_error_domain_as_AW_claimed"], True),
        replaced(wanted, ["scope", "arbitrary_bounded_field_sharpness_claimed"], True),
        {**wanted, "extra": 0},
    ]
    for bad in changes:
        assert wire(bad) != wire(wanted)
        with pytest.raises(ValueError):
            runner.verify_suite(bad, wanted)


def selected_history_mutations(previous):
    paths = [
        [0, "problem", "probe", 0],
        [0, "problem", "interface", 0, 0],
        [0, "problem", "geometric", 0, 0],
        [0, "problem", "decoder", 0, 0],
        [0, "geometry", "volume"],
        [0, "coordinates", "bank_scales", 0],
        [0, "coordinates", "raw_from_local", 0, 0, 0],
        [0, "coordinates", "local_from_raw", 0, 0, 0],
        [0, "maps", "interface_error", 0, 0],
        [0, "maps", "target_error", 0, 0],
        [0, "enclosure", "receiver_radii", 0],
        [0, "shared", "row_gains", 0],
        [0, "enclosure", "row_gains", 0],
    ]
    for path in paths:
        yield changed_fraction(previous, path)
    row = next(
        (i for i, v in enumerate(previous[0]["maps"]["normalized_target"]) if v is not None), None
    )
    if row is not None:
        yield changed_fraction(previous, [0, "maps", "normalized_target", row, 0])
    else:
        yield replaced(previous, [0, "maps", "normalized_target", 0], [fw(0)])
    yield replaced(previous, [0, "problem", "target_labels", 0, "first"], False)
    yield replaced(previous, [0, "problem", "bank_labels", 0, "basis"], False)


def test_fixed_selected_problem_geometry_baseline_history_mutations(runner, fixed_data):
    _, previous, families, _ = fixed_data
    for bad in selected_history_mutations(previous):
        assert wire(bad) != wire(previous)
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)


def test_fixed_unselected_old_endpoint_and_ancillary_math_not_replayed(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    changes = [
        replaced(previous, [0, "shared", "witnesses"], []),
        replaced(previous, [0, "enclosure", "witnesses"], []),
        replaced(previous, [0, "shared", "max_gain"], fw(-1)),
        replaced(previous, [0, "comparison"], {"not": "read"}),
        replaced(previous, [0, "checks"], {"not": "read"}),
        replaced(previous, [0, "counts"], {"not": "read"}),
    ]
    for bad in changes:
        assert wire(bad) != wire(previous)
        assert runner.project_inputs(bad)[0] == problems
        assert runner.historical_bridges(families, bad) == BRIDGES


def test_fixed_source_and_ancestor_identity_inventory(runner):
    current = runner.identities()
    assert {key: len(current[key]) for key in current} == {
        "source_ledger": 5,
        "prior_artifacts": 54,
        "ancestor_sources": 89,
    }
    assert set(current["source_ledger"]) == set(runner.SOURCES)
    raw = runner.AW.read_bytes()
    assert (
        len(raw) == 1341549
        and hashlib.sha256(raw).hexdigest()
        == "e14e357309ff98f9f93c8f23c603f62d9bf17b01b4515ee122a464671b205916"
    )
    for name, want in current["source_ledger"].items():
        raw = (HERE / name).read_bytes()
        assert len(raw) == want["bytes"] and hashlib.sha256(raw).hexdigest() == want["sha256"]
