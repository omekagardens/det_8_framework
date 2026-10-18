"""Independent polynomial refinement, sparse transport and bounded-field checks.

Only test names containing fixed consume authenticated AY cases. Collection and generic
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
        load("_qr05az_test_primary", "kernel.py"),
        load("_qr05az_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05az_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


CHECKS = (
    "parent_geometry",
    "child_partition",
    "lineage_identity",
    "frozen_bank_identity",
    "restriction_convexity",
    "raw_moment_additivity",
    "kernel_restriction",
    "kernel_integral_additivity",
    "bernstein_transport",
    "response_transport",
    "normalization_domain",
    "bound_monotonicity",
    "certification_inheritance",
    "parent_field_pipelines",
    "child_extremizer_pipelines",
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
    "independent_child_fields_called_parent_fields",
    "full_bounded_field_domain_changed",
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


def level_oracle(p):
    geometry = geometry_oracle(p)
    v = fraction(geometry["volume"])
    amp = v * v
    sigma = list(map(fraction, geometry["target_scales"]))
    defined, undefined = geometry["defined_rows"], geometry["undefined_rows"]
    b, g, d = (matrix(p[key]) for key in ("interface", "geometric", "decoder"))
    q, r = len(g), len(g[0])
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
    return encode(
        {
            "kernels": kernels,
            "maps": {
                "decoder_bank": k,
                "bank_residual": [[F()] * r for _ in range(q)],
                "raw_bilinear_target": raw,
                "normalized_bilinear_target": a,
            },
            "bounds": bounds,
            "certification": certification,
        }
    )


def child_problem(data):
    parent = data["parent"]
    child = copy.deepcopy(parent)
    child["tiles"] = [
        {"event": parent["tiles"][row["parent"]]["event"], "bounds": copy.deepcopy(row["bounds"])}
        for row in data["children"]
    ]
    child["bank_labels"] = [
        {"tile": i, "basis": j} for i in range(len(data["children"])) for j in range(4)
    ]
    for key in ("interface", "geometric"):
        child[key] = [
            [
                copy.deepcopy(x)
                for c in data["children"]
                for x in row[4 * c["parent"] : 4 * c["parent"] + 4]
            ]
            for row in parent[key]
        ]
    return child


def restriction_blocks(data):
    out = []
    for child in data["children"]:
        parent = rect(data["parent"]["tiles"][child["parent"]]["bounds"])
        box = rect(child["bounds"])
        u0, u1, v0, v1 = box
        a, b, c, d = parent
        block = []
        for u, v in ((u0, v0), (u1, v0), (u0, v1), (u1, v1)):
            x, y = (u - a) / (b - a), (v - c) / (d - c)
            block.append([(x if i else 1 - x) * (y if j else 1 - y) for i, j in CORNERS])
        assert all(x >= 0 for row in block for x in row) and all(
            sum(row, F()) == 1 for row in block
        )
        out.append(block)
    return out


def physical_basis_blocks(probe, boxes):
    # Four separate physical polynomial fields, independently integrated per actual tile.
    result = []
    for box in boxes:
        columns = []
        for i in range(4):
            c = encode([F(i == j) for j in range(4)])
            column = integral_oracle(probe, [box], c)["raw_moments"]
            columns.append(list(map(fraction, column)))
        result.append([list(row) for row in zip(*columns, strict=True)])
    return result


def restrict_corners(values, blocks, parents):
    return [
        sum((block[i][j] * values[4 * parents[t] + j] for j in range(4)), F())
        for t, block in enumerate(blocks)
        for i in range(4)
    ]


def aggregate_bank(values, parents, p):
    return [
        sum((values[4 * t + j] for t, owner in enumerate(parents) if owner == i), F())
        for i in range(p)
        for j in range(4)
    ]


def aggregate_rows(rows, blocks, parents, p):
    return [
        None
        if row is None
        else [
            sum(
                (
                    row[4 * t + h] * blocks[t][h][j]
                    for t, owner in enumerate(parents)
                    if owner == i
                    for h in range(4)
                ),
                F(),
            )
            for i in range(p)
            for j in range(4)
        ]
        for row in rows
    ]


def matrix_nullable(value):
    return [None if row is None else list(map(fraction, row)) for row in value]


def residual(a, b):
    return [None if x is None else x - y for x, y in zip(a, b, strict=True)]


def matrix_residual(a, b):
    return [None if x is None else residual(x, y) for x, y in zip(a, b, strict=True)]


def expected(data):
    parent = data["parent"]
    child = child_problem(data)
    p, m = len(parent["tiles"]), len(child["tiles"])
    rp, rc = 4 * p, 4 * m
    q, s = len(parent["geometric"]), len(parent["interface"])
    owners = [row["parent"] for row in data["children"]]
    for i, row in enumerate(parent["tiles"]):
        boxes = [rect(c["bounds"]) for c in data["children"] if c["parent"] == i]
        cover_by_endpoint_cells(rect(row["bounds"]), boxes)
    geometry = geometry_oracle(parent)
    child_geometry = geometry_oracle(child)
    for key in ("volume", "cell_volumes", "target_scales", "defined_rows", "undefined_rows"):
        assert child_geometry[key] == geometry[key]
    defined, undefined = geometry["defined_rows"], geometry["undefined_rows"]
    amp = fraction(geometry["volume"]) ** 2
    sigma = list(map(fraction, geometry["target_scales"]))
    lp, lc = level_oracle(parent), level_oracle(child)
    e = restriction_blocks(data)
    pp = physical_basis_blocks(parent["probe"], [row["bounds"] for row in parent["tiles"]])
    pc = physical_basis_blocks(parent["probe"], [row["bounds"] for row in child["tiles"]])
    aggregp = [
        [
            [
                sum(
                    (
                        pc[t][i][h] * e[t][h][j]
                        for t, owner in enumerate(owners)
                        if owner == n
                        for h in range(4)
                    ),
                    F(),
                )
                for j in range(4)
            ]
            for i in range(4)
        ]
        for n in range(p)
    ]
    assert aggregp == pp
    ip, ic = matrix(lp["kernels"]["tile_integrals"]), matrix(lc["kernels"]["tile_integrals"])
    aggint = [
        [sum((row[t] for t, owner in enumerate(owners) if owner == i), F()) for i in range(p)]
        for row in ic
    ]
    bp, bc = (
        matrix(lp["kernels"]["bernstein_integrals"]),
        matrix(lc["kernels"]["bernstein_integrals"]),
    )
    aggbern = aggregate_rows(bc, e, owners, p)
    jp, jc = (matrix(level["maps"]["raw_bilinear_target"]) for level in (lp, lc))
    ap, ac = (matrix_nullable(level["maps"]["normalized_bilinear_target"]) for level in (lp, lc))
    restrictj = aggregate_rows(jc, e, owners, p)
    restricta = aggregate_rows(ac, e, owners, p)
    assert aggint == ip and aggbern == bp and restrictj == jp and restricta == ap
    for i in range(q):
        for t, owner in enumerate(owners):
            old = list(map(fraction, lp["kernels"]["corner_values"][i][owner]))
            assert scalar_apply(e[t], old) == list(
                map(fraction, lc["kernels"]["corner_values"][i][t])
            )
    bparent = {
        key: [fraction(x) if x is not None else None for x in lp["bounds"][key]]
        for key in ("constant_lower", "bilinear_lower", "corner_upper", "certified_gain")
    }
    bchild = {
        key: [fraction(x) if x is not None else None for x in lc["bounds"][key]] for key in bparent
    }
    compare = {
        "constant_increase": comparison(bchild["constant_lower"], bparent["constant_lower"]),
        "bilinear_increase": comparison(bchild["bilinear_lower"], bparent["bilinear_lower"]),
        "upper_decrease": comparison(bparent["corner_upper"], bchild["corner_upper"]),
    }
    inherited = lp["certification"]["certified_rows"]
    new = [i for i in lc["certification"]["certified_rows"] if i not in inherited]
    still = lc["certification"]["uncertified_rows"]
    assert set(inherited) <= set(lc["certification"]["certified_rows"])
    assert all(bparent["certified_gain"][i] == bchild["certified_gain"][i] for i in inherited)

    def pipeline(problem, level, corners):
        integrated = integral_oracle(
            problem["probe"], [row["bounds"] for row in problem["tiles"]], encode(corners)
        )
        bank = list(map(fraction, integrated["raw_moments"]))
        b, g, d = (matrix(problem[key]) for key in ("interface", "geometric", "decoder"))
        observed = scalar_apply(b, bank)
        direct = scalar_apply(g, bank)
        decoded = scalar_apply(d, observed)
        norm = [decoded[i] / sigma[i] if i in defined else None for i in range(q)]
        target = matrix(level["maps"]["raw_bilinear_target"])
        assert direct == decoded == scalar_apply(target, corners)
        for i in defined:
            assert norm[i] == dot(
                list(map(fraction, level["maps"]["normalized_bilinear_target"][i])), corners
            )
            assert (
                abs(norm[i])
                <= fraction(level["bounds"]["bilinear_lower"][i])
                <= fraction(level["bounds"]["corner_upper"][i])
            )
        assert all(
            -amp <= fraction(x) <= amp for key in ("minima", "maxima") for x in integrated[key]
        )
        return {
            "corners": corners,
            "global_coefficients": integrated["global_coefficients"],
            "bank_error": bank,
            "observed_error": observed,
            "direct_error": direct,
            "decoded_error": decoded,
            "normalized_error": norm,
            "tile_minima": integrated["minima"],
            "tile_maxima": integrated["maxima"],
        }

    def pair(corners):
        a = pipeline(parent, lp, corners)
        b = pipeline(child, lc, restrict_corners(corners, e, owners))
        aggregate = aggregate_bank(b["bank_error"], owners, p)
        assert aggregate == a["bank_error"]
        assert all(
            a[key] == b[key]
            for key in ("observed_error", "direct_error", "decoded_error", "normalized_error")
        )
        parentcoeff = list(map(fraction, a["global_coefficients"]))
        childcoeff = list(map(fraction, b["global_coefficients"]))
        duplicated = [parentcoeff[4 * owner + j] for owner in owners for j in range(4)]
        assert childcoeff == duplicated
        return {
            "parent": a,
            "child": b,
            "aggregated_bank_error": aggregate,
            "bank_residual": residual(aggregate, a["bank_error"]),
            "observed_residual": residual(b["observed_error"], a["observed_error"]),
            "direct_residual": residual(b["direct_error"], a["direct_error"]),
            "decoded_residual": residual(b["decoded_error"], a["decoded_error"]),
            "normalized_residual": residual(b["normalized_error"], a["normalized_error"]),
            "field_coefficient_residual": residual(childcoeff, duplicated),
        }

    pattern = [F(x) for _ in range(p) for x in (-1, 0, 1, F(1, 2))]
    constants = [F(1)] * rp
    witnesses = {
        "parent_pattern": {"positive": pair(pattern), "negative": pair([-x for x in pattern])},
        "parent_constant": {"positive": pair(constants), "negative": pair([-x for x in constants])},
    }
    for side, problem, level in (("parent", parent, lp), ("child", child, lc)):
        for name, boundkey in (("constant", "constant_lower"), ("bilinear", "bilinear_lower")):
            group = side + "_" + name + "_maximizer"
            if not defined:
                witnesses[group] = None
                continue
            maximum_record = level["bounds"]["maxima"][boundkey]
            i = maximum_record["rows"][0]
            if name == "constant":
                signs = list(map(sign, map(fraction, level["kernels"]["tile_integrals"][i])))
                corners = [F(x) for x in signs for _ in range(4)]
            else:
                signs = list(
                    map(sign, map(fraction, level["maps"]["normalized_bilinear_target"][i]))
                )
                corners = list(map(F, signs))
            if side == "parent":
                positive, negative = pair(corners), pair([-x for x in corners])
                posout, negout = positive["parent"], negative["parent"]
            else:
                positive, negative = (
                    pipeline(problem, level, corners),
                    pipeline(problem, level, [-x for x in corners]),
                )
                posout, negout = positive, negative
            gain = fraction(maximum_record["gain"])
            assert posout["normalized_error"][i] == gain and negout["normalized_error"][i] == -gain
            witnesses[group] = {
                "target_row": i,
                "signs": signs,
                "positive": positive,
                "negative": negative,
            }
    d, zp, zc = len(defined), len(inherited), len(lc["certification"]["certified_rows"])
    paired, childw = (8, 4) if d else (4, 0)
    ep = 3 * rp + s + 2 * q + d + 2 * p
    ec = 3 * rc + s + 2 * q + d + 2 * m
    epair = ep + ec + 2 * rp + s + 2 * q + d + rc
    counts = {
        "cells": len(parent["cells"]),
        "positive_cells": sum(row["bounds"] is not None for row in parent["cells"]),
        "parent_tiles": p,
        "child_tiles": m,
        "parent_bank_values": rp,
        "child_bank_values": rc,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": d,
        "undefined_rows": q - d,
        "input_geometry_entries": 4
        + 4 * sum(row["bounds"] is not None for row in parent["cells"])
        + 4 * p
        + 4 * m,
        "input_matrix_entries": s * rp + q * rp + q * s,
        "child_problem_geometry_entries": 4
        + 4 * sum(row["bounds"] is not None for row in parent["cells"])
        + 4 * m,
        "child_problem_matrix_entries": s * rc + q * rc + q * s,
        "geometry_entries": 1 + len(parent["cells"]) + q + p + m,
        "restriction_entries": 38 * m + 48 * p,
        "parent_kernel_entries": 12 * q * p,
        "child_kernel_entries": 12 * q * m,
        "parent_map_entries": (3 * q + d) * rp,
        "child_map_entries": (3 * q + d) * rc,
        "bound_entries": sum(3 * d + z + (3 if d else 0) + (1 if z else 0) for z in (zp, zc)),
        "certification_bridge_entries": zp,
        "transport_entries": 2 * q * p + 4 * q * rp + 2 * d * rp,
        "comparison_entries": 3 * d + (3 if d else 0),
        "parent_paired_witnesses": paired,
        "child_witnesses": childw,
        "sign_entries": p + rp + m + rc if d else 0,
        "witness_entries": paired * epair + childw * ec,
        "constant_strict": len(compare["constant_increase"]["strict_rows"]),
        "bilinear_strict": len(compare["bilinear_increase"]["strict_rows"]),
        "upper_strict": len(compare["upper_decrease"]["strict_rows"]),
        "inherited_rows": zp,
        "newly_certified_rows": len(new),
        "still_uncertified_rows": len(still),
    }
    return encode(
        {
            "input": copy.deepcopy(data),
            "child_problem": child,
            "geometry": {key: value for key, value in geometry.items() if key != "tile_volumes"}
            | {
                "parent_tile_volumes": geometry["tile_volumes"],
                "child_tile_volumes": child_geometry["tile_volumes"],
                "child_parents": owners,
            },
            "restriction": {
                "blocks": e,
                "parent_moment_blocks": pp,
                "child_moment_blocks": pc,
                "aggregated_moment_blocks": aggregp,
                "moment_residuals": [[[F()] * 4 for _ in range(4)] for _ in range(p)],
                "row_sums": [[sum(row, F()) for row in block] for block in e],
                "min_weights": [min(x for row in block for x in row) for block in e],
                "max_weights": [max(x for row in block for x in row) for block in e],
            },
            "levels": {"parent": lp, "child": lc},
            "transport": {
                "aggregate_kernel_integrals": aggint,
                "aggregate_bernstein_integrals": aggbern,
                "kernel_integral_residuals": matrix_residual(aggint, ip),
                "bernstein_residuals": matrix_residual(aggbern, bp),
                "restricted_raw_target": restrictj,
                "raw_target_residuals": matrix_residual(restrictj, jp),
                "restricted_normalized_target": restricta,
                "normalized_target_residuals": matrix_residual(restricta, ap),
            },
            "comparison": compare,
            "certification_bridge": {
                "inherited_rows": inherited,
                "newly_certified_rows": new,
                "still_uncertified_rows": still,
                "undefined_rows": undefined,
                "inherited_gain_residuals": [F() if i in inherited else None for i in range(q)],
            },
            "witnesses": witnesses,
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


def identity_refinement(p):
    return {
        "parent": copy.deepcopy(p),
        "children": [
            {"parent": i, "bounds": copy.deepcopy(t["bounds"])} for i, t in enumerate(p["tiles"])
        ],
    }


def vertical_refinement(p, cut=F(1, 2)):
    children = []
    for i, tile in enumerate(p["tiles"]):
        u0, u1, v0, v1 = rect(tile["bounds"])
        mid = u0 + cut * (u1 - u0)
        children.extend(
            {"parent": i, "bounds": rational_wire(b)}
            for b in ((u0, mid, v0, v1), (mid, u1, v0, v1))
        )
    return {"parent": copy.deepcopy(p), "children": children}


def quarter_children(p):
    children = []
    for i, tile in enumerate(p["tiles"]):
        u0, u1, v0, v1 = rect(tile["bounds"])
        u = (u0 + u1) / 2
        v = (v0 + v1) / 2
        children.extend(
            {"parent": i, "bounds": rational_wire(b)}
            for b in ((u0, u, v0, v), (u, u1, v0, v), (u0, u, v, v1), (u, u1, v, v1))
        )
    return children


def mixed_midpoint():
    return vertical_refinement(mixed_kernel_problem())


def mixed_zero_split():
    return vertical_refinement(mixed_kernel_problem(), F(1, 4))


def unresolved_saddle():
    p = one_kernel([F(-1, 4), 0, 0, 1])
    return {"parent": p, "children": quarter_children(p)}


def unequal_refinement():
    data = vertical_refinement(unequal_problem(), F(1, 3))
    data["children"] = [data["children"][i] for i in (4, 0, 5, 2, 1, 3)]
    return data


@pytest.mark.parametrize(
    "factory",
    [
        mixed_midpoint,
        mixed_zero_split,
        unresolved_saddle,
        unequal_refinement,
        lambda: identity_refinement(unit_problem()),
        lambda: vertical_refinement(opposite_tiles_problem()),
        lambda: vertical_refinement(partial_certificate_problem()),
        lambda: identity_refinement(thin_problem()),
        lambda: vertical_refinement(mixed_problem()),
        lambda: vertical_refinement(mixed_problem(True)),
        lambda: vertical_refinement(positive_zero_problem()),
        lambda: vertical_refinement(empty_receiver_problem()),
    ],
)
def test_complete_independent_refinement_family_wire(engines, factory):
    data = factory()
    wanted = expected(data)
    for engine in engines:
        before = wire(data)
        assert wire(engine.build_family(data)) == wire(wanted)
        assert wire(data) == before


def test_identity_refinement_all_weak_inequalities_tie(engines):
    data = identity_refinement(unit_problem())
    for engine in engines:
        f = engine.build_family(data)
        assert f["child_problem"] == data["parent"]
        assert f["restriction"]["blocks"] == [encode(identity(4))]
        assert f["levels"]["parent"] == f["levels"]["child"]
        assert f["certification_bridge"]["newly_certified_rows"] == []
        for comparison in f["comparison"].values():
            assert comparison["strict_rows"] == [] and comparison["tied_rows"] == [0]
            assert comparison["gain_gap"] == [fw(0)]
        assert (
            f["witnesses"]["parent_pattern"]["positive"]["parent"]
            == f["witnesses"]["parent_pattern"]["positive"]["child"]
        )


def test_midpoint_enlarges_bilinear_subclass_but_leaves_mixed_certificate_null(engines):
    for engine in engines:
        f = engine.build_family(mixed_midpoint())
        p, c = f["levels"]["parent"]["bounds"], f["levels"]["child"]["bounds"]
        assert p["constant_lower"] == p["bilinear_lower"] == [fw(F(1, 2))]
        assert p["corner_upper"] == [fw(F(3, 2))]
        assert c["constant_lower"] == [fw(F(1, 2))]
        assert c["bilinear_lower"] == [fw(F(7, 12))]
        assert c["corner_upper"] == [fw(1)]
        assert p["certified_gain"] == c["certified_gain"] == [None]
        assert f["certification_bridge"]["still_uncertified_rows"] == [0]
        assert f["levels"]["child"]["certification"]["mixed_obstructions"] == [
            [{"tile": 0, "positive_corner": 1, "negative_corner": 0}]
        ]
        assert f["comparison"]["bilinear_increase"]["gain_gap"] == [fw(F(1, 12))]
        # New maximum witness exceeds every correlated parent-cube response.
        w = f["witnesses"]["child_bilinear_maximizer"]["positive"]
        assert w["normalized_error"] == [fw(F(7, 12))]
        assert fraction(w["normalized_error"][0]) > fraction(p["bilinear_lower"][0])


def test_zero_split_certifies_same_functional_without_filling_parent_null(engines):
    for engine in engines:
        f = engine.build_family(mixed_zero_split())
        p, c = f["levels"]["parent"]["bounds"], f["levels"]["child"]["bounds"]
        assert p["certified_gain"] == [None]
        assert c["certified_gain"] == c["constant_lower"] == c["bilinear_lower"] == [fw(F(5, 8))]
        assert c["corner_upper"] == [fw(F(5, 4))]
        assert f["certification_bridge"] == {
            "inherited_rows": [],
            "newly_certified_rows": [0],
            "still_uncertified_rows": [],
            "undefined_rows": [],
            "inherited_gain_residuals": [None],
        }
        assert f["levels"]["child"]["kernels"]["tile_classes"] == [["nonpositive", "nonnegative"]]
        assert f["witnesses"]["child_constant_maximizer"]["signs"] == [-1, 1]


def test_refinement_need_not_resolve_bilinear_zero_curve(engines):
    for engine in engines:
        f = engine.build_family(unresolved_saddle())
        assert f["levels"]["parent"]["certification"]["status"] == ["uncertified"]
        assert f["levels"]["child"]["certification"]["status"] == ["uncertified"]
        assert [
            x["tile"] for x in f["levels"]["child"]["certification"]["mixed_obstructions"][0]
        ] == [1, 2]
        assert f["certification_bridge"]["still_uncertified_rows"] == [0]


def test_correlated_and_independent_child_cubes_have_distinct_extrema(engines):
    data = mixed_midpoint()
    for engine in engines:
        f = engine.build_family(data)
        e = [matrix(x) for x in f["restriction"]["blocks"]]
        owners = f["geometry"]["child_parents"]
        parent, child = data["parent"], f["child_problem"]
        boxes = [r["bounds"] for r in child["tiles"]]
        correlated = []
        independent = []
        for c in product((-1, 1), repeat=4):
            c = list(map(F, c))
            restricted = restrict_corners(c, e, owners)
            integrals = engine.integrate(parent["probe"], boxes, encode(restricted))
            coarse = engine.integrate(parent["probe"], [parent["tiles"][0]["bounds"]], encode(c))
            assert aggregate_bank(list(map(fraction, integrals["raw_moments"])), owners, 1) == list(
                map(fraction, coarse["raw_moments"])
            )
            y = engine.apply(
                child["decoder"], engine.produce(child["interface"], integrals["raw_moments"])
            )
            correlated.append(fraction(y[0]) / fraction(f["geometry"]["target_scales"][0]))
        for c in product((-1, 1), repeat=8):
            # Exhaustive finite child cube via independently retained exact coefficients.
            independent.append(
                dot(
                    matrix(f["levels"]["child"]["maps"]["normalized_bilinear_target"])[0],
                    list(map(F, c)),
                )
            )
        assert max(correlated) == F(1, 2) and max(independent) == F(7, 12)
        bad = [F(1)] * 4 + [F(-1)] * 4
        # Incompatible values at the shared physical edge cannot represent one parent field.
        assert bad[1] != bad[4] and bad[3] != bad[6]


def test_unequal_raw_additivity_not_unweighted_local_moment_additivity(engines):
    data = vertical_refinement(unit_problem(), F(1, 3))
    for engine in engines:
        f = engine.build_family(data)
        p = data["parent"]
        c = f["child_problem"]
        coarse = engine.integrate(p["probe"], [p["tiles"][0]["bounds"]], rational_wire([1] * 4))
        fine = engine.integrate(
            p["probe"], [row["bounds"] for row in c["tiles"]], rational_wire([1] * 8)
        )
        assert aggregate_bank(list(map(fraction, fine["raw_moments"])), [0, 0], 1) == list(
            map(fraction, coarse["raw_moments"])
        )
        assert aggregate_bank(list(map(fraction, fine["local_moments"])), [0, 0], 1) != list(
            map(fraction, coarse["local_moments"])
        )
        assert fine["global_coefficients"] == rational_wire([F(1, 4), 0, 0, 0] * 2)
        assert c["decoder"] == p["decoder"] and len(c["interface"]) == len(p["interface"])
        assert f["geometry"]["volume"] == fw(F(1, 2)) and f["geometry"]["target_scales"] == [
            fw(F(1, 16))
        ]
        assert (
            c["probe"] == p["probe"]
            and c["cells"] == p["cells"]
            and c["target_labels"] == p["target_labels"]
        )


def test_two_stage_restriction_and_raw_aggregation_compose(engines):
    first = mixed_midpoint()
    middle = child_problem(first)
    second = {
        "parent": middle,
        "children": [
            {"parent": 0, "bounds": rational_wire([0, F(1, 4), 0, 1])},
            {"parent": 0, "bounds": rational_wire([F(1, 4), F(1, 2), 0, 1])},
            {"parent": 1, "bounds": rational_wire([F(1, 2), 1, 0, 1])},
        ],
    }
    direct = {
        "parent": first["parent"],
        "children": [{"parent": 0, "bounds": x["bounds"]} for x in second["children"]],
    }
    for engine in engines:
        a, b, c = (engine.build_family(x) for x in (first, second, direct))
        assert (
            b["child_problem"] == c["child_problem"]
            and b["levels"]["child"] == c["levels"]["child"]
        )
        e0, e1, ed = ([matrix(x) for x in f["restriction"]["blocks"]] for f in (a, b, c))
        owners = b["geometry"]["child_parents"]
        for i, owner in enumerate(owners):
            assert scalar_product(e1[i], e0[owner], 4) == ed[i]
        sample = list(map(F, range(12)))
        staged = aggregate_bank(aggregate_bank(sample, owners, 2), [0, 0], 1)
        assert staged == aggregate_bank(sample, [0, 0, 0], 1)
        assert a["levels"]["child"]["bounds"]["bilinear_lower"] == [fw(F(7, 12))]
        assert c["levels"]["child"]["bounds"]["certified_gain"] == [fw(F(5, 8))]
        assert (
            c["levels"]["child"]["bounds"]["corner_upper"]
            == a["levels"]["child"]["bounds"]["corner_upper"]
        )


def test_undefined_zero_and_empty_receiver_witness_domains(engines):
    for engine in engines:
        f = engine.build_family(vertical_refinement(mixed_problem(True)))
        assert f["certification_bridge"]["undefined_rows"] == [0, 1]
        assert f["counts"]["parent_paired_witnesses"] == 4 and f["counts"]["child_witnesses"] == 0
        for key in (
            "parent_constant_maximizer",
            "parent_bilinear_maximizer",
            "child_constant_maximizer",
            "child_bilinear_maximizer",
        ):
            assert f["witnesses"][key] is None
        for group in ("parent_pattern", "parent_constant"):
            for sign_name in ("positive", "negative"):
                for level in ("parent", "child"):
                    assert f["witnesses"][group][sign_name][level]["normalized_error"] == [
                        None,
                        None,
                    ]
        z = engine.build_family(vertical_refinement(positive_zero_problem()))
        assert z["certification_bridge"]["inherited_rows"] == [0]
        assert z["levels"]["child"]["bounds"]["certified_gain"] == [fw(0)]
        empty = engine.build_family(vertical_refinement(empty_receiver_problem()))
        assert empty["child_problem"]["interface"] == [] and empty["child_problem"]["decoder"] == [
            []
        ]


def pipeline_records(f):
    records = []
    for name, group in f["witnesses"].items():
        if group is None:
            continue
        if name.startswith("parent_"):
            records.extend(
                (which, group[side][which])
                for side in ("positive", "negative")
                for which in ("parent", "child")
            )
        else:
            records.extend(("child", group[side]) for side in ("positive", "negative"))
    return records


def test_every_prescribed_pipeline_calls_actual_public_apis(engines, monkeypatch):
    from collections import Counter

    for engine in engines:
        for data in (
            mixed_midpoint(),
            mixed_zero_split(),
            vertical_refinement(mixed_problem(True)),
        ):
            recorded = {name: [] for name in ("integrate", "produce", "apply")}
            with monkeypatch.context() as patch:
                for name, entries in recorded.items():
                    original = getattr(engine, name)

                    def spy(*args, entries=entries, original=original):
                        entries.append(wire(list(args)))
                        return original(*args)

                    patch.setattr(engine, name, spy)
                f = engine.build_family(data)
            required = {name: [] for name in recorded}
            for level, e in pipeline_records(f):
                p = data["parent"] if level == "parent" else f["child_problem"]
                required["integrate"].append(
                    wire([p["probe"], [row["bounds"] for row in p["tiles"]], e["corners"]])
                )
                for a in (p["interface"], p["geometric"]):
                    required["produce"].append(wire([a, e["bank_error"]]))
                required["apply"].append(wire([p["decoder"], e["observed_error"]]))
            n = 20 if f["geometry"]["defined_rows"] else 8
            assert {k: len(v) for k, v in required.items()} == {
                "integrate": n,
                "produce": 2 * n,
                "apply": n,
            }
            for key, values in required.items():
                actual, want = Counter(recorded[key]), Counter(values)
                assert all(actual[a] >= number for a, number in want.items())


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
    "factory",
    [unequal_refinement, mixed_zero_split, lambda: vertical_refinement(mixed_problem(True))],
)
def test_full_affine_transport_same_physical_field_and_receiver(engines, factory):
    data = factory()
    p = data["parent"]
    receiver = identity(len(p["interface"]))
    inverse = identity(len(receiver))
    if len(receiver) >= 2:
        receiver[0][1], inverse[0][1] = F(1), F(-1)
    au, bv, cu, dv = F(3, 2), F(-7, 5), F(5, 3), F(11, 7)
    moved, bank, _, k = affine_problem(p, au, bv, cu, dv, receiver, inverse)
    children = []
    for c in data["children"]:
        u0, u1, v0, v1 = rect(c["bounds"])
        children.append(
            {
                "parent": c["parent"],
                "bounds": rational_wire([au * u0 + bv, au * u1 + bv, cu * v0 + dv, cu * v1 + dv]),
            }
        )
    transformed = {"parent": moved, "children": children}
    want = expected(transformed)
    for engine in engines:
        a, b = engine.build_family(data), engine.build_family(transformed)
        assert wire(b) == wire(want)
        assert b["restriction"]["blocks"] == a["restriction"]["blocks"]
        assert b["comparison"] == a["comparison"]
        assert b["certification_bridge"] == a["certification_bridge"]
        for level in ("parent", "child"):
            first, second = a["levels"][level], b["levels"][level]
            assert (
                first["bounds"] == second["bounds"]
                and first["certification"] == second["certification"]
            )
            assert (
                first["maps"]["normalized_bilinear_target"]
                == second["maps"]["normalized_bilinear_target"]
            )
            assert second["kernels"]["corner_values"] == [
                [[fw(k * fraction(x)) for x in tile] for tile in row]
                for row in first["kernels"]["corner_values"]
            ]
            for key in ("tile_integrals", "bernstein_integrals", "tile_abs_upper"):
                assert second["kernels"][key] == [
                    [fw(k * k * fraction(x)) for x in row] for row in first["kernels"][key]
                ]
        for (la, x), (lb, y) in zip(pipeline_records(a), pipeline_records(b), strict=True):
            assert la == lb and x["corners"] == y["corners"]
            assert x["normalized_error"] == y["normalized_error"]
            blocks = bank if la == "parent" else [bank[0]] * len(children)
            assert y["bank_error"] == encode(
                scalar_synthesize(blocks, list(map(fraction, x["bank_error"])))
            )
            assert y["observed_error"] == encode(
                mv(receiver, list(map(fraction, x["observed_error"])))
            )
            for key in ("direct_error", "decoded_error"):
                assert y[key] == [fw(k**4 * fraction(v)) for v in x[key]]
            for key in ("tile_minima", "tile_maxima"):
                assert y[key] == [fw(k * k * fraction(v)) for v in x[key]]


def test_child_order_is_not_event_order_and_parent_indices_are_not_ids(engines):
    p = unequal_refinement()
    q = copy.deepcopy(p)
    q["children"] = list(reversed(q["children"]))
    for engine in engines:
        a, b = engine.build_family(p), engine.build_family(q)
        assert wire(b) == wire(expected(q))
        assert a["levels"]["parent"] == b["levels"]["parent"]
        assert a["levels"]["child"]["bounds"] == b["levels"]["child"]["bounds"]
        assert b["restriction"]["blocks"] == list(reversed(a["restriction"]["blocks"]))
        assert b["child_problem"]["tiles"] == list(reversed(a["child_problem"]["tiles"]))
        assert a["transport"] == b["transport"]


def test_detached_shared_native_inputs_and_no_file_access(engines, monkeypatch):
    for engine in engines:
        data = identity_refinement(positive_zero_problem())
        data["children"][0]["bounds"] = data["parent"]["tiles"][0]["bounds"]
        original = wire(data)
        want = expected(data)

        def forbidden(*args, **kwargs):
            raise RuntimeError("public mathematics must not read files")

        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "open", forbidden)
            actual = engine.build_family(data)
        assert wire(actual) == wire(want) and wire(data) == original
        actual["input"]["children"][0]["bounds"][0][0] += 1
        actual["restriction"]["blocks"][0][0][0][0] += 1
        assert wire(data) == original
        fresh = engine.build_family(data)
        assert wire(fresh) == wire(want)


def test_raw_helpers_partial_empty_unbounded_and_signed_fields(engines):
    probe = rational_wire([-2, 3, -1, 2])
    tiles = [rational_wire([-2, -1, -1, 2]), rational_wire([1, 3, 0, 1])]
    c = rational_wire([-3, 0, 2, 7, 1, -2, 4, -5])
    rows = rational_wire([[1, -2, 3, -4, 4, 3, -2, 1], [0] * 8])
    want = integral_oracle(probe, tiles, c)
    kern = kernel_oracle(probe, tiles, rows)
    for engine in engines:
        assert wire(engine.integrate(probe, tiles, c)) == wire(want)
        assert wire(engine.inspect_kernel(probe, tiles, rows)) == wire(kern)
        assert engine.integrate(probe, [], []) == {key: [] for key in want}
        assert engine.inspect_kernel(probe, [], [[], []]) == {key: [[], []] for key in kern}
        assert engine.produce([[], []], []) == [fw(0), fw(0)]
        assert engine.apply([], []) == []


def test_separate_cap_edges_do_not_multiply_maximum_dimensions(engines):
    unit = {"event": 0, "bounds": [0, 1, 0, 1]}
    null = {"event": 1, "bounds": None}
    strips = [{"event": 0, "bounds": [F(i, 256), F(i + 1, 256), 0, 1]} for i in range(256)]
    p = make_problem(unit["bounds"], [unit, null], strips, [], [[]], [{"first": 1, "second": 1}])
    one = make_problem(unit["bounds"], [unit, null], [unit], [], [[]], [{"first": 1, "second": 1}])
    max_children = {
        "parent": one,
        "children": [{"parent": 0, "bounds": rational_wire(x["bounds"])} for x in strips],
    }
    wide = make_problem(unit["bounds"], [unit], [unit], [[0] * 4] * 320, [[0] * 320])
    cells = [unit, *[{"event": i, "bounds": None} for i in range(1, 8)]]
    labels = [{"first": i, "second": j} for i in range(8) for j in range(8)]
    targets = make_problem(unit["bounds"], cells, [unit], [], [[]] * 64, labels)
    for engine in engines:
        for data in (
            identity_refinement(p),
            max_children,
            identity_refinement(wide),
            identity_refinement(targets),
        ):
            assert wire(engine.build_family(data)) == wire(expected(data))
        assert engine.produce([[]] * 1024, []) == rational_wire([0] * 1024)
        assert engine.produce([], rational_wire([0] * 1024)) == []
        assert engine.apply([[]] * 64, []) == rational_wire([0] * 64)
        assert engine.apply([], rational_wire([0] * 320)) == []


class NativeListSubclass(list):
    pass


class NativeDictSubclass(dict):
    pass


class NativeIntSubclass(int):
    pass


def malformed_families():
    data = unequal_refinement()
    for parent in malformed_parents():
        yield {"parent": parent, "children": copy.deepcopy(data["children"])}
    yield None
    yield []
    yield NativeDictSubclass(data)
    yield {"parent": data["parent"]}
    yield {"children": data["children"]}
    yield {**data, "moment_bank": []}
    for value in (None, (), [], NativeListSubclass(data["children"]), data["children"] * 43):
        yield replaced(data, ["children"], value)
    for value in (None, [], {}, {"parent": 0}, {"bounds": data["children"][0]["bounds"]}):
        yield replaced(data, ["children", -1], value)
    for value in (True, -1, 3, 7, 0.0, F(0)):
        yield replaced(data, ["children", -1, "parent"], value)
    yield replaced(data, ["children", -1, "extra"], 0)
    for value in (None, (), [fw(0)] * 3):
        yield replaced(data, ["children", -1, "bounds"], value)
    for value in ([0], [0, 0], [2, 2], True, 0.0):
        yield replaced(data, ["children", -1, "bounds", -1], value)
    # Missing, duplicated, overlapping, degenerate, outside, wrong-lineage covers.
    yield replaced(data, ["children"], data["children"][:-1])
    yield replaced(data, ["children", -1], data["children"][0])
    yield replaced(data, ["children", 0, "parent"], 1)
    one = vertical_refinement(unit_problem())
    yield replaced(one, ["children", 0, "bounds", 1], fw(F(3, 4)))
    yield replaced(one, ["children", 0, "bounds", 1], fw(F(1, 4)))
    yield replaced(one, ["children", 0, "bounds", 1], fw(0))
    yield replaced(one, ["children", 0, "bounds", 0], fw(-1))


def malformed_parents():
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
    if engine.build_family(identity_refinement(p))["levels"]["parent"]["bounds"][
        "certified_gain"
    ] != [fw(0)]:
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
        lambda: engine.build_family(
            identity_refinement(make_problem(cell["bounds"], [cell], [cell], [], [[]]))
        )
    )
    count += 1
    cycle = []
    cycle.append(cycle)
    p = unit_problem()
    p["tiles"].append(p["tiles"])
    for call in (
        lambda: engine.build_family({"parent": p, "children": []}),
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
                    replaced(unequal_refinement(), ["children", -1, "bounds", -1], value)
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
            "_child_partition",
            "_restrictions",
            "_restriction_blocks",
            "_moment_blocks",
            "_level",
        )
        if hasattr(engine, name)
    ]
    originals = {name: getattr(engine, name) for name in names}
    for name in names:
        setattr(engine, name, forbidden)
    try:
        require_rejection(
            lambda: engine.build_family(
                replaced(unequal_refinement(), ["parent", "decoder", -1, -1], [1, 0])
            )
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
spec=importlib.util.spec_from_file_location("az_guard_tests",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05az_guard_"+name,file)
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


def get_at(value, path):
    for key in path:
        value = value[key]
    return value


def is_fraction(value):
    return type(value) is list and len(value) == 2 and all(type(x) is int for x in value)


def first_leaf(value, path=()):
    rational = is_fraction(value) and value[1] > 0 and F(*value).denominator == value[1]
    if rational or value is None or type(value) not in (dict, list) or not value:
        return list(path), value
    key = next(iter(value)) if type(value) is dict else 0
    return first_leaf(value[key], (*path, key))


def changed_leaf(value, path):
    suffix, old = first_leaf(get_at(value, path))
    if is_fraction(old):
        new = fw(fraction(old) + 1)
    elif old is None:
        new = fw(0)
    elif type(old) is bool:
        new = not old
    elif type(old) is int:
        new = old + 1
    elif type(old) is str:
        new = "changed:" + old
    else:
        new = {"unexpected": True}
    return replaced(value, [*path, *suffix], new)


def family_mutation_paths(f):
    # One representative per scientific field; full wire and every literal count
    # are checked independently, without repetitively mutating all entries.
    for name in (
        "input",
        "child_problem",
        "geometry",
        "restriction",
        "transport",
        "certification_bridge",
    ):
        for key in f[name]:
            if name == "input" and key == "parent":
                for field in f[name][key]:
                    yield [name, key, field]
            else:
                yield [name, key]
    for level in ("parent", "child"):
        for name in ("kernels", "maps", "certification"):
            for key in f["levels"][level][name]:
                yield ["levels", level, name, key]
        for key in ("constant_lower", "bilinear_lower", "corner_upper", "certified_gain"):
            yield ["levels", level, "bounds", key]
            yield ["levels", level, "bounds", "maxima", key, "gain"]
            yield ["levels", level, "bounds", "maxima", key, "rows"]
    for name in f["comparison"]:
        for key in f["comparison"][name]:
            yield ["comparison", name, key]
    for name, group in f["witnesses"].items():
        if group is None:
            yield ["witnesses", name]
            continue
        if "target_row" in group:
            yield ["witnesses", name, "target_row"]
            yield ["witnesses", name, "signs"]
        # Detailed pair and pipeline structures are covered once each; all other
        # selected extrema retain designated row/sign and both signed outputs.
        if name == "parent_pattern":
            for key in group["positive"]:
                if key in ("parent", "child"):
                    for field in group["positive"][key]:
                        yield ["witnesses", name, "positive", key, field]
                else:
                    yield ["witnesses", name, "positive", key]
        elif name == "child_bilinear_maximizer":
            for field in group["positive"]:
                yield ["witnesses", name, "positive", field]
        else:
            yield ["witnesses", name, "positive"]
        yield ["witnesses", name, "negative"]
    for key in f["checks"]:
        yield ["checks", key]
    for key in ("restriction_entries", "transport_entries", "witness_entries"):
        yield ["counts", key]


def family_mutations(f):
    yield {**copy.deepcopy(f), "unrequested": True}
    for path in family_mutation_paths(f):
        yield changed_leaf(f, path)


def rationals(value):
    if is_fraction(value):
        fraction(value)
        return 1
    if type(value) is dict:
        return sum(rationals(v) for v in value.values())
    if type(value) is list:
        return sum(rationals(v) for v in value)
    return 0


def literal_count_checks(f):
    c = f["counts"]
    parent = f["input"]["parent"]
    child = f["child_problem"]
    g = f["geometry"]
    geometric_fields = ("probe", "cells", "tiles")

    def geom(p):
        return rationals(p["probe"]) + sum(
            rationals(x["bounds"]) for key in ("cells", "tiles") for x in p[key]
        )

    assert c["input_geometry_entries"] == geom(parent) + sum(
        rationals(x["bounds"]) for x in f["input"]["children"]
    )
    assert set(geometric_fields) <= set(parent)
    assert c["child_problem_geometry_entries"] == geom(child)
    for name, p in (("input", parent), ("child_problem", child)):
        assert c[name + "_matrix_entries"] == sum(
            rationals(p[key]) for key in ("interface", "geometric", "decoder")
        )
    assert c["geometry_entries"] == sum(
        rationals(g[key])
        for key in (
            "volume",
            "cell_volumes",
            "target_scales",
            "parent_tile_volumes",
            "child_tile_volumes",
        )
    )
    assert c["restriction_entries"] == rationals(f["restriction"])
    assert c["transport_entries"] == rationals(f["transport"])
    for level in ("parent", "child"):
        k = f["levels"][level]
        assert c[level + "_kernel_entries"] == sum(
            rationals(v) for key, v in k["kernels"].items() if key != "tile_classes"
        )
        assert c[level + "_map_entries"] == rationals(k["maps"])
    assert c["bound_entries"] == sum(
        sum(rationals(v) for key, v in f["levels"][level]["bounds"].items() if key != "maxima")
        + sum(rationals(x["gain"]) for x in f["levels"][level]["bounds"]["maxima"].values())
        for level in ("parent", "child")
    )
    assert c["certification_bridge_entries"] == rationals(
        f["certification_bridge"]["inherited_gain_residuals"]
    )
    assert c["comparison_entries"] == sum(
        rationals(x["gain_gap"]) + rationals(x["max_gap"]) for x in f["comparison"].values()
    )
    pair_count = child_count = entries = signs = 0
    for name, group in f["witnesses"].items():
        if group is None:
            continue
        if "signs" in group:
            signs += len(group["signs"])
        for side in ("positive", "negative"):
            e = group[side]
            entries += rationals(e)
            if name.startswith("parent_"):
                pair_count += 1
            else:
                child_count += 1
    assert (pair_count, child_count, entries, signs) == tuple(
        c[key]
        for key in ("parent_paired_witnesses", "child_witnesses", "witness_entries", "sign_entries")
    )
    assert len(c) == 34 and len(f["checks"]) == 17


@pytest.mark.parametrize(
    "factory", [mixed_midpoint, mixed_zero_split, lambda: vertical_refinement(mixed_problem(True))]
)
def test_complete_generic_wire_mutations_and_literal_payload_counts(runner, factory):
    f = expected(factory())
    literal_count_checks(f)
    raw = wire(f)
    for bad in family_mutations(f):
        assert wire(bad) != raw
        with pytest.raises(ValueError):
            runner.verify_suite(bad, f)


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
    "independent_child_fields_called_parent_fields",
    "full_bounded_field_domain_changed",
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
BRIDGES = {
    "selected_families": list(FAMILIES),
    **dict.fromkeys(
        (
            "AY_problem_equal",
            "AY_geometry_equal",
            "AY_kernels_equal",
            "AY_maps_equal",
            "AY_bounds_equal",
            "AY_certification_equal",
            "same_physical_kernel",
            "same_receiver_observations",
            "same_bounded_field_domain",
        ),
        True,
    ),
    **dict.fromkeys(
        ("AY_endpoints_replayed", "other_historical_mathematics_replayed", "older_executors_run"),
        False,
    ),
}


def parent_geometry(f):
    out = {
        key: copy.deepcopy(f["geometry"][key])
        for key in ("volume", "cell_volumes", "target_scales", "defined_rows", "undefined_rows")
    }
    out["tile_volumes"] = copy.deepcopy(f["geometry"]["parent_tile_volumes"])
    return out


def independent_history_checks(families, previous):
    assert [f["problem"]["family"] for f in previous] == list(FAMILIES)
    for f, old in zip(families, previous, strict=True):
        assert wire(f["input"]["parent"]) == wire(old["problem"])
        assert wire(parent_geometry(f)) == wire(old["geometry"])
        for key in ("kernels", "maps", "bounds", "certification"):
            assert wire(f["levels"]["parent"][key]) == wire(old[key])
        literal_count_checks(f)


def payload(families):
    keys = {
        "input": "input",
        "child_problem": "child_problem",
        "geometry": "geometry",
        "restriction": "restriction",
        "level": "levels",
        "transport": "transport",
        "comparison": "comparison",
        "certification_bridge": "certification_bridge",
        "witness": "witnesses",
    }
    return [
        {
            "family": f["input"]["parent"]["family"],
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
    # Selected retained quantities only: no AY witness or comparison reconstruction.
    return {
        "problem": copy.deepcopy(f["input"]["parent"]),
        "geometry": parent_geometry(f),
        **copy.deepcopy(f["levels"]["parent"]),
        "witnesses": "not replayed",
        "comparison": "not replayed",
        "checks": "not replayed",
        "counts": "not replayed",
    }


def test_synthetic_selected_history_full_suite_and_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(
        FAMILIES, (mixed_zero_split, lambda: vertical_refinement(mixed_problem(True))), strict=True
    ):
        p = factory()
        p["parent"]["family"] = name
        problems.append(p)
    families = list(map(expected, problems))
    previous = list(map(synthetic_history, families))
    independent_history_checks(families, previous)
    want = expected_suite(families)
    lookup = {f["input"]["parent"]["family"]: f for f in families}

    def project(prior):
        return (
            [
                {
                    "parent": copy.deepcopy(row["problem"]),
                    "children": copy.deepcopy(
                        lookup[row["problem"]["family"]]["input"]["children"]
                    ),
                }
                for row in prior
            ],
            prior,
        )

    monkeypatch.setattr(runner, "project_inputs", project)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    calls = []

    def loader(name):
        def build(p):
            assert p == lookup[p["parent"]["family"]]["input"]
            calls.append(name)
            return copy.deepcopy(lookup[p["parent"]["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    assert wire(runner.assemble_suite(families, previous)) == wire(want)
    for route, count in (("primary", 2), ("reference", 2), ("compare", 4)):
        calls.clear()
        assert wire(runner.run_suite(route)) == wire(want) and len(calls) == count
    with pytest.raises(ValueError):
        runner.run_suite("unknown")
    bad = replaced(previous, [0, "witnesses"], "changed")
    with pytest.raises(ValueError):
        runner.assemble_suite(families, bad)
    assert runner.historical_bridges(families, bad) == BRIDGES

    def changing(p):
        f = copy.deepcopy(lookup[p["parent"]["family"]])
        p["children"].reverse()
        return f

    monkeypatch.setattr(runner, "load_engine", lambda name: SimpleNamespace(build_family=changing))
    with pytest.raises(ValueError):
        runner.run_suite("primary")


def test_synthetic_selected_projection_quarters_inventory_and_detachment(runner):
    cell = {"event": 0, "bounds": [0, 1, 0, 1]}
    cells = [cell, *[{"event": i, "bounds": None} for i in range(1, 8)]]
    tiles = [{"event": 0, "bounds": [F(i, 12), F(i + 1, 12), 0, 1]} for i in range(12)]
    labels = [{"first": i, "second": j} for i in range(8) for j in range(8)]
    p = make_problem(cell["bounds"], cells, tiles, [[0] * 48] * 37, [[0] * 37] * 64, labels)
    previous = [{"problem": copy.deepcopy(p)} for _ in FAMILIES]
    for name, row in zip(FAMILIES, previous, strict=True):
        row["problem"]["family"] = name
    before = wire(previous)
    projected, consumed = runner.project_inputs(previous)
    assert consumed is previous
    for data, old in zip(projected, previous, strict=True):
        assert data == {"parent": old["problem"], "children": quarter_children(old["problem"])}
        assert len(data["children"]) == 48
    projected[0]["children"][0]["bounds"][0][0] = 999
    projected[0]["parent"]["probe"][0][0] = 999
    assert wire(previous) == before
    changes = [
        {},
        previous[:1],
        list(reversed(previous)),
        replaced(previous, [0, "problem"], {**p, "extra": 0}),
        replaced(previous, [0, "problem", "tiles"], []),
        replaced(previous, [0, "problem", "bank_labels"], []),
        replaced(previous, [0, "problem", "target_labels"], []),
        replaced(previous, [0, "problem", "decoder", -1], []),
        replaced(previous, [0, "problem", "cells"], []),
        replaced(previous, [0, "problem", "tiles", -1, "bounds", -1], [0]),
        replaced(previous, [0, "problem", "tiles", -1, "bounds", 1], fw(-1)),
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
def test_fixed_whole_family_independent_refinement_oracle(engines, fixed_data, index):
    problems, _, families, _ = fixed_data
    for engine in engines:
        supplied = copy.deepcopy(problems[index])
        before = wire(supplied)
        f = engine.build_family(supplied)
        assert wire(supplied) == before and wire(f) == wire(families[index])
        # Complete signed pipelines are compared above; re-execute one parent pair
        # and one child maximum (if defined), not an unprescribed all-row witness bank.
        endpoints = [
            ("parent", f["witnesses"]["parent_pattern"]["positive"]["parent"]),
            ("child", f["witnesses"]["parent_pattern"]["positive"]["child"]),
        ]
        group = f["witnesses"]["child_bilinear_maximizer"]
        if group is not None:
            endpoints.append(("child", group["negative"]))
        for level, e in endpoints:
            p = supplied["parent"] if level == "parent" else f["child_problem"]
            integrated = engine.integrate(
                p["probe"], [x["bounds"] for x in p["tiles"]], e["corners"]
            )
            assert integrated["global_coefficients"] == e["global_coefficients"]
            assert integrated["raw_moments"] == e["bank_error"]
            assert (
                integrated["minima"] == e["tile_minima"]
                and integrated["maxima"] == e["tile_maxima"]
            )
            observed = engine.produce(p["interface"], e["bank_error"])
            assert observed == e["observed_error"]
            assert engine.produce(p["geometric"], e["bank_error"]) == e["direct_error"]
            assert engine.apply(p["decoder"], observed) == e["decoded_error"]


def test_fixed_full_suite_counts_payload_and_selected_ay_history(runner, fixed_data):
    problems, previous, families, want = fixed_data
    assert wire(runner.assemble_suite(families, previous)) == wire(want)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert runner.payload_sizes(families) == payload(families)
    for data, f in zip(problems, families, strict=True):
        p = data["parent"]
        assert (
            len(p["cells"]),
            len(p["tiles"]),
            len(p["bank_labels"]),
            len(p["interface"]),
            len(p["target_labels"]),
        ) == (8, 12, 48, 37, 64)
        assert data["children"] == quarter_children(p) and len(data["children"]) == 48
        assert len(f["child_problem"]["bank_labels"]) == 192
        literal_count_checks(f)
    assert set(want["scope"]) == set(SCOPE) and not any(want["scope"].values())


@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_cached_orchestration_routes(runner, fixed_data, monkeypatch, route):
    _, _, families, want = fixed_data
    lookup = {f["input"]["parent"]["family"]: f for f in families}
    seen = []

    def loader(name):
        def build(p):
            assert p == lookup[p["parent"]["family"]]["input"]
            seen.append(name)
            return copy.deepcopy(lookup[p["parent"]["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    assert wire(runner.run_suite(route)) == wire(want)
    assert seen == (["primary", "reference"] * 2 if route == "compare" else [route] * 2)


def test_fixed_bounded_family_and_suite_corruptions(runner, fixed_data):
    _, _, families, want = fixed_data
    for f in families:
        raw = wire(f)
        for bad in family_mutations(f):
            assert wire(bad) != raw
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)
    changes = [
        replaced(want, ["families"], list(reversed(families))),
        replaced(want, ["prior_bridges", "AY_bounds_equal"], False),
        replaced(want, ["prior_bridges", "AY_endpoints_replayed"], True),
        replaced(
            want,
            ["payload_sizes", 0, "restriction_bytes"],
            want["payload_sizes"][0]["restriction_bytes"] + 1,
        ),
        replaced(want, ["totals", "witness_entries"], want["totals"]["witness_entries"] + 1),
        replaced(want, ["scope", "measurements_added"], True),
        replaced(want, ["scope", "independent_child_fields_called_parent_fields"], True),
        {**want, "extra": 0},
    ]
    original = wire(want)
    for bad in changes:
        assert wire(bad) != original
        with pytest.raises(ValueError):
            runner.verify_suite(bad, want)


def selected_history_mutations(previous):
    for path in (
        [0, "problem", "probe"],
        [0, "problem", "interface"],
        [0, "problem", "geometric"],
        [0, "problem", "decoder"],
        [0, "geometry", "volume"],
        [0, "kernels", "corner_values"],
        [0, "kernels", "bernstein_integrals"],
        [0, "maps", "raw_bilinear_target"],
        [0, "maps", "normalized_bilinear_target"],
        [0, "bounds", "certified_gain"],
        [0, "bounds", "bilinear_lower"],
        [0, "certification", "status"],
    ):
        yield changed_leaf(previous, path)
    yield replaced(previous, [0, "problem", "bank_labels", 0, "basis"], False)
    yield replaced(previous, [0, "problem", "target_labels", 0, "first"], False)


def test_fixed_selected_problem_geometry_level_and_domain_mutations(runner, fixed_data):
    _, previous, families, _ = fixed_data
    raw = wire(previous)
    for bad in selected_history_mutations(previous):
        assert wire(bad) != raw
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)


def test_fixed_unselected_ay_endpoints_comparisons_counts_not_replayed(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    for key in ("witnesses", "comparison", "checks", "counts"):
        bad = replaced(previous, [0, key], {"not": "read"})
        assert wire(bad) != wire(previous)
        assert runner.project_inputs(bad)[0] == problems
        assert runner.historical_bridges(families, bad) == BRIDGES


def test_fixed_source_and_ancestor_identity_inventory(runner):
    current = runner.identities()
    assert {key: len(value) for key, value in current.items()} == {
        "source_ledger": 5,
        "prior_artifacts": 56,
        "ancestor_sources": 99,
    }
    assert set(current["source_ledger"]) == set(runner.SOURCES)
    raw = runner.AY.read_bytes()
    assert (
        len(raw) == 2115070
        and hashlib.sha256(raw).hexdigest()
        == "a4dda392b4dd8f148389cb82c4187611c10b11e3f3e05f82e2779fbe3bf90874"
    )
    for name, want in current["source_ledger"].items():
        raw = (HERE / name).read_bytes()
        assert len(raw) == want["bytes"] and hashlib.sha256(raw).hexdigest() == want["sha256"]
