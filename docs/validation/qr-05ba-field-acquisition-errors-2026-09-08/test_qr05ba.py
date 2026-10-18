"""Independent polynomial field/acquisition product-domain checks.

Only test names containing fixed consume authenticated AZ cases. Collection and generic
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
        load("_qr05ba_test_primary", "kernel.py"),
        load("_qr05ba_test_reference", "reference.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return load("_qr05ba_test_runner", "study.py")


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


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


def parse_nullable(values):
    return [None if x is None else fraction(x) for x in values]


def field_evidence(refinement):
    parent = refinement["parent"]
    child = child_problem(refinement)
    p = len(parent["tiles"])
    owners = [c["parent"] for c in refinement["children"]]
    for i, row in enumerate(parent["tiles"]):
        cover_by_endpoint_cells(
            rect(row["bounds"]),
            [rect(c["bounds"]) for c in refinement["children"] if c["parent"] == i],
        )
    gp, gc = geometry_oracle(parent), geometry_oracle(child)
    for key in ("volume", "cell_volumes", "target_scales", "defined_rows", "undefined_rows"):
        assert gp[key] == gc[key]
    geometry = {
        key: copy.deepcopy(gp[key])
        for key in ("volume", "cell_volumes", "target_scales", "defined_rows", "undefined_rows")
    }
    geometry.update(
        parent_tile_volumes=gp["tile_volumes"],
        child_tile_volumes=gc["tile_volumes"],
        child_parents=owners,
    )
    blocks = restriction_blocks(refinement)
    levels = {"parent": level_oracle(parent), "child": level_oracle(child)}
    for key in ("raw_bilinear_target", "normalized_bilinear_target"):
        assert aggregate_rows(
            matrix_nullable(levels["child"]["maps"][key]), blocks, owners, p
        ) == matrix_nullable(levels["parent"]["maps"][key])
    for row, child_row in zip(
        levels["parent"]["kernels"]["corner_values"],
        levels["child"]["kernels"]["corner_values"],
        strict=True,
    ):
        assert [mv(e, list(map(fraction, row[owners[i]]))) for i, e in enumerate(blocks)] == [
            list(map(fraction, x)) for x in child_row
        ]
    return {
        "child_problem": child,
        "geometry": geometry,
        "restriction_blocks": encode(blocks),
        "levels": levels,
    }


def expected(data):
    field = field_evidence(data["refinement"])
    parent = data["refinement"]["parent"]
    child = field["child_problem"]
    geometry = field["geometry"]
    defined, undefined = geometry["defined_rows"], geometry["undefined_rows"]
    n, p, m, q, s = (
        len(parent["cells"]),
        len(parent["tiles"]),
        len(child["tiles"]),
        len(parent["geometric"]),
        len(parent["interface"]),
    )
    rp, rc = 4 * p, 4 * m
    d = len(defined)
    sigma = list(map(fraction, geometry["target_scales"]))
    amplitude = fraction(geometry["volume"]) ** 2
    rho = list(map(fraction, data["receiver_radii"]))
    decoder = matrix(parent["decoder"])
    raw = [[decoder[i][j] * rho[j] for j in range(s)] for i in range(q)]
    normalized = [[x / sigma[i] for x in raw[i]] if i in defined else None for i in range(q)]
    gain = [sum(map(abs, normalized[i]), F()) if i in defined else None for i in range(q)]
    acquisition = {
        "raw_map": raw,
        "normalized_map": normalized,
        "gain": gain,
        "maxima": maximum(gain),
    }
    owners = geometry["child_parents"]
    blocks = [matrix(x) for x in field["restriction_blocks"]]
    cases = []
    for budget in data["budgets"]:
        epsilon, eta = fraction(budget["field"]), fraction(budget["acquisition"])
        levels = {}
        for name in ("parent", "child"):
            source = field["levels"][name]
            bounds = {}
            for key in ("constant_lower", "bilinear_lower", "corner_upper"):
                values = parse_nullable(source["bounds"][key])
                bounds[key] = [
                    epsilon * values[i] + eta * gain[i] if i in defined else None for i in range(q)
                ]
            certified = source["certification"]["certified_rows"]
            available = [i for i in defined if epsilon == 0 or i in certified]
            unavailable = [i for i in defined if i not in available]
            exact = parse_nullable(source["bounds"]["certified_gain"])
            bounds["exact_gain"] = [
                None
                if i not in available
                else eta * gain[i]
                if epsilon == 0
                else epsilon * exact[i] + eta * gain[i]
                for i in range(q)
            ]
            bounds["maxima"] = {key: maximum(values) for key, values in bounds.items()}
            reason = [
                "undefined"
                if i in undefined
                else "zero_field_budget"
                if epsilon == 0
                else "field_certified"
                if i in certified
                else "unavailable"
                for i in range(q)
            ]
            levels[name] = {
                "bounds": bounds,
                "exactness": {
                    "reason": reason,
                    "available_rows": available,
                    "unavailable_rows": unavailable,
                    "undefined_rows": undefined,
                },
            }
        inherited = levels["parent"]["exactness"]["available_rows"]
        new = [i for i in levels["child"]["exactness"]["available_rows"] if i not in inherited]
        for i in inherited:
            assert (
                levels["parent"]["bounds"]["exact_gain"][i]
                == levels["child"]["bounds"]["exact_gain"][i]
            )
        bridge = {
            "inherited_rows": inherited,
            "newly_exact_rows": new,
            "unavailable_rows": levels["child"]["exactness"]["unavailable_rows"],
            "undefined_rows": undefined,
            "inherited_gain_residuals": [F() if i in inherited else None for i in range(q)],
        }
        comparison_rows = {}
        for key, bound, reverse in (
            ("constant_increase", "constant_lower", False),
            ("bilinear_increase", "bilinear_lower", False),
            ("upper_decrease", "corner_upper", True),
        ):
            first, second = levels["parent"]["bounds"][bound], levels["child"]["bounds"][bound]
            comparison_rows[key] = (
                comparison(first, second) if reverse else comparison(second, first)
            )
            assert all(x is None or x >= 0 for x in comparison_rows[key]["gain_gap"])

        def pipeline(name, c, z, epsilon=epsilon, eta=eta, levels=levels):
            problem = parent if name == "parent" else child
            count = len(problem["tiles"])
            assert len(c) == 4 * count and len(z) == s
            assert all(abs(x) <= epsilon for x in c) and all(abs(x) <= eta for x in z)
            integrated = integral_oracle(
                problem["probe"], [row["bounds"] for row in problem["tiles"]], encode(c)
            )
            e = list(map(fraction, integrated["raw_moments"]))
            observed = mv(matrix(problem["interface"]), e)
            field_direct = mv(matrix(problem["geometric"]), e)
            field_decoded = mv(decoder, observed)
            noise = [rho[j] * z[j] for j in range(s)]
            total = [observed[j] + noise[j] for j in range(s)]
            acq_direct = mv(raw, z)
            acq_decoded = mv(decoder, noise)
            direct = [field_direct[i] + acq_direct[i] for i in range(q)]
            decoded = mv(decoder, total)
            assert field_direct == field_decoded and acq_direct == acq_decoded and direct == decoded
            normal = [direct[i] / sigma[i] if i in defined else None for i in range(q)]
            a = matrix_nullable(field["levels"][name]["maps"]["normalized_bilinear_target"])
            assert all(normal[i] == dot(a[i], c) + dot(normalized[i], z) for i in defined)
            assert all(
                abs(normal[i])
                <= levels[name]["bounds"]["bilinear_lower"][i]
                <= levels[name]["bounds"]["corner_upper"][i]
                for i in defined
            )
            assert all(
                abs(fraction(x)) <= epsilon * amplitude
                for key in ("minima", "maxima")
                for x in integrated[key]
            )
            assert all(abs(noise[j]) <= eta * rho[j] for j in range(s))
            return {
                "corners": c,
                "acquisition_coordinates": z,
                "global_coefficients": list(map(fraction, integrated["global_coefficients"])),
                "bank_error": e,
                "field_observed_error": observed,
                "acquisition_error": noise,
                "total_observed_error": total,
                "field_direct_error": field_direct,
                "field_decoded_error": field_decoded,
                "acquisition_direct_error": acq_direct,
                "acquisition_decoded_error": acq_decoded,
                "total_direct_error": direct,
                "total_decoded_error": decoded,
                "normalized_error": normal,
                "tile_minima": list(map(fraction, integrated["minima"])),
                "tile_maxima": list(map(fraction, integrated["maxima"])),
            }

        def pair(c, z):
            first = pipeline("parent", c, z)
            second = pipeline("child", restrict_corners(c, blocks, owners), z)
            aggregated = aggregate_bank(second["bank_error"], owners, p)
            assert aggregated == first["bank_error"]
            out = {
                "parent": first,
                "child": second,
                "aggregated_bank_error": aggregated,
                "bank_residual": residual(aggregated, first["bank_error"]),
            }
            stems = (
                "field_observed",
                "acquisition",
                "total_observed",
                "field_direct",
                "field_decoded",
                "acquisition_direct",
                "acquisition_decoded",
                "total_direct",
                "total_decoded",
                "normalized",
            )
            for stem in stems:
                key = stem + "_error"
                out[stem + "_residual"] = residual(second[key], first[key])
                assert all(x is None or x == 0 for x in out[stem + "_residual"])
            duplicated = [
                x
                for owner in owners
                for x in first["global_coefficients"][4 * owner : 4 * owner + 4]
            ]
            out["field_coefficient_residual"] = residual(second["global_coefficients"], duplicated)
            assert not any(out["field_coefficient_residual"])
            return out

        pattern = [F(-1), F(0), F(1), F(1, 2)]
        witnesses = {}
        for name, c, z in (
            (
                "parent_pattern",
                [epsilon * x for _ in range(p) for x in pattern],
                [eta * pattern[j % 4] for j in range(s)],
            ),
            ("parent_constant", [epsilon] * rp, [eta] * s),
        ):
            witnesses[name] = {
                "positive": pair(c, z),
                "negative": pair([-x for x in c], [-x for x in z]),
            }
        for name, count in (("parent", p), ("child", m)):
            source = field["levels"][name]
            for kind, key in (
                ("constant", "constant_lower"),
                ("bilinear", "bilinear_lower"),
                ("exact", "exact_gain"),
            ):
                group = name + "_" + kind + "_maximizer"
                highest = levels[name]["bounds"]["maxima"][key]
                if highest["gain"] is None:
                    witnesses[group] = None
                    continue
                row = highest["rows"][0]
                values = (
                    source["maps"]["normalized_bilinear_target"][row]
                    if kind == "bilinear"
                    else source["kernels"]["tile_integrals"][row]
                )
                field_signs = [sign(fraction(x)) if epsilon else 0 for x in values]
                noise_signs = [sign(x) if eta else 0 for x in raw[row]]
                c = [
                    epsilon * x for x in field_signs for _ in range(1 if kind == "bilinear" else 4)
                ]
                z = [eta * x for x in noise_signs]
                if name == "parent":
                    positive, negative = pair(c, z), pair([-x for x in c], [-x for x in z])
                    attained = (
                        positive["parent"]["normalized_error"][row],
                        negative["parent"]["normalized_error"][row],
                    )
                else:
                    positive, negative = (
                        pipeline(name, c, z),
                        pipeline(name, [-x for x in c], [-x for x in z]),
                    )
                    attained = positive["normalized_error"][row], negative["normalized_error"][row]
                assert attained == (highest["gain"], -highest["gain"])
                witnesses[group] = {
                    "target_row": row,
                    "field_signs": field_signs,
                    "acquisition_signs": noise_signs,
                    "positive": positive,
                    "negative": negative,
                }
        cases.append(
            {
                "budget": copy.deepcopy(budget),
                "levels": levels,
                "comparison": comparison_rows,
                "exact_bridge": bridge,
                "witnesses": witnesses,
            }
        )
    zfp, zfc = (
        len(field["levels"][name]["certification"]["certified_rows"])
        for name in ("parent", "child")
    )
    total_pairs = total_child = total_signs = total_entries = case_bounds = 0
    ep, ec = (3 * r + 4 * s + 6 * q + d + 2 * t for r, t in ((rp, p), (rc, m)))
    epair = ep + ec + 2 * rp + 3 * s + 6 * q + d + rc
    for case in cases:
        zp, zc = (
            len(case["levels"][name]["exactness"]["available_rows"]) for name in ("parent", "child")
        )
        pairs = 4 + 4 * bool(d) + 2 * bool(zp)
        child_witnesses = 4 * bool(d) + 2 * bool(zc)
        total_pairs += pairs
        total_child += child_witnesses
        total_signs += bool(d) * (p + rp + m + rc + 4 * s) + bool(zp) * (p + s) + bool(zc) * (m + s)
        total_entries += pairs * epair + child_witnesses * ec
        case_bounds += sum(3 * d + z + 3 * bool(d) + bool(z) for z in (zp, zc))
    counts = {
        "cells": n,
        "positive_cells": sum(x["bounds"] is not None for x in parent["cells"]),
        "parent_tiles": p,
        "child_tiles": m,
        "parent_bank_values": rp,
        "child_bank_values": rc,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": d,
        "undefined_rows": q - d,
        "budgets": len(cases),
        "input_geometry_entries": 4
        + 4 * sum(x["bounds"] is not None for x in parent["cells"])
        + 4 * p
        + 4 * m,
        "input_matrix_entries": s * rp + q * rp + q * s,
        "input_budget_entries": s + 2 * len(cases),
        "geometry_entries": 1 + n + q + p + m,
        "restriction_entries": 16 * m,
        "parent_kernel_entries": 12 * q * p,
        "child_kernel_entries": 12 * q * m,
        "parent_map_entries": (3 * q + d) * rp,
        "child_map_entries": (3 * q + d) * rc,
        "field_bound_entries": sum(3 * d + z + 3 * bool(d) + bool(z) for z in (zfp, zfc)),
        "acquisition_entries": q * s + d * s + d + bool(d),
        "case_bound_entries": case_bounds,
        "case_exact_bridge_entries": sum(len(c["exact_bridge"]["inherited_rows"]) for c in cases),
        "case_comparison_entries": len(cases) * (3 * d + 3 * bool(d)),
        "parent_paired_witnesses": total_pairs,
        "child_witnesses": total_child,
        "sign_entries": total_signs,
        "witness_entries": total_entries,
        "constant_strict": sum(
            len(c["comparison"]["constant_increase"]["strict_rows"]) for c in cases
        ),
        "bilinear_strict": sum(
            len(c["comparison"]["bilinear_increase"]["strict_rows"]) for c in cases
        ),
        "upper_strict": sum(len(c["comparison"]["upper_decrease"]["strict_rows"]) for c in cases),
        "inherited_exact_rows": sum(len(c["exact_bridge"]["inherited_rows"]) for c in cases),
        "newly_exact_rows": sum(len(c["exact_bridge"]["newly_exact_rows"]) for c in cases),
        "unavailable_exact_rows": sum(len(c["exact_bridge"]["unavailable_rows"]) for c in cases),
    }
    checks = dict.fromkeys(
        (
            "parent_geometry",
            "child_partition",
            "lineage_identity",
            "full_bank_identity",
            "same_receiver_contract",
            "restriction_convexity",
            "field_level_evidence",
            "response_transport",
            "acquisition_map",
            "normalization_domain",
            "composed_bounds",
            "exact_availability",
            "refinement_comparison",
            "paired_field_noise_pipelines",
            "joint_maximum_attainment",
            "complete_inventory",
        ),
        True,
    )
    return encode(
        {
            "input": copy.deepcopy(data),
            "field": field,
            "acquisition": acquisition,
            "cases": cases,
            "checks": checks,
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


def make_input(refinement=None, radii=None, budgets=None):
    if refinement is None:
        refinement = identity_refinement(one_kernel([1, 0, 0, 0]))
    s = len(refinement["parent"]["interface"])
    if radii is None:
        radii = [F(1)] * s
    if budgets is None:
        budgets = [("zero", 0, 0), ("field", 1, 0), ("acquisition", 0, 1), ("joint", 1, 1)]
    return {
        "refinement": copy.deepcopy(refinement),
        "receiver_radii": rational_wire(radii),
        "budgets": [
            {"name": name, "field": fw(epsilon), "acquisition": fw(eta)}
            for name, epsilon, eta in budgets
        ],
    }


def literal_product_problem():
    cell = {"event": 0, "bounds": [0, 1, 0, 1]}
    # sigma=1/16; G=1/16 makes field gain1/8 and acquisition gain1.
    p = make_problem(cell["bounds"], [cell], [cell], [[F(1, 16), 0, 0, 0]], [[1]])
    return make_input(identity_refinement(p), [F(1, 16)])


def null_acquisition_problem(all_undefined=False):
    return make_input(vertical_refinement(mixed_problem(all_undefined)), [1, 2])


def subset_exact_problem():
    p = partial_certificate_problem()
    return make_input(vertical_refinement(p), [F(1, 100)] * len(p["interface"]))


def ba_unequal_problem():
    return make_input(
        unequal_refinement(),
        [F(2), F(3)],
        [("fractional", F(2, 3), F(5, 7)), ("noise_only", 0, F(1, 2)), ("field_only", F(3, 2), 0)],
    )


def subset_dominant_problem():
    p = partial_certificate_problem()
    for key in ("decoder", "geometric"):
        p[key][1] = [fw(100 * fraction(x)) for x in p[key][1]]
    return make_input(identity_refinement(p), [0] * len(p["interface"]))


def opposite_target_problem():
    cells = [{"event": 0, "bounds": [0, F(1, 2), 0, 1]}, {"event": 1, "bounds": [F(1, 2), 1, 0, 1]}]
    p = make_problem(
        [0, 1, 0, 1],
        cells,
        cells,
        [[F(1, 16), 0, 0, 0, F(1, 16), 0, 0, 0]],
        [[1], [-1]],
        [{"first": 0, "second": 0}, {"first": 0, "second": 1}],
    )
    return make_input(identity_refinement(p), [F(1, 16)])


@pytest.mark.parametrize(
    "factory",
    [
        literal_product_problem,
        lambda: make_input(mixed_midpoint()),
        lambda: make_input(mixed_zero_split()),
        lambda: make_input(unresolved_saddle()),
        ba_unequal_problem,
        lambda: null_acquisition_problem(False),
        lambda: null_acquisition_problem(True),
        subset_dominant_problem,
        opposite_target_problem,
        lambda: make_input(vertical_refinement(positive_zero_problem()), [1, 2]),
        lambda: make_input(identity_refinement(empty_receiver_problem()), []),
        lambda: make_input(vertical_refinement(opposite_tiles_problem()), [0] * 8),
    ],
)
def test_complete_independent_field_acquisition_family_wire(engines, factory):
    data = factory()
    before = wire(data)
    want = expected(data)
    for engine in engines:
        actual = engine.build_family(data)
        assert wire(actual) == wire(want) and wire(data) == before


def test_literal_product_sharpness_is_not_coupled_error_sharpness(engines):
    data = literal_product_problem()
    data["budgets"] = [{"name": "coupled-control", "field": fw(1), "acquisition": fw(F(1, 8))}]
    for engine in engines:
        f = engine.build_family(data)
        case = f["cases"][0]
        assert f["acquisition"]["gain"] == [fw(1)]
        assert f["field"]["levels"]["parent"]["bounds"]["certified_gain"] == [fw(F(1, 8))]
        assert case["levels"]["parent"]["bounds"]["exact_gain"] == [fw(F(1, 4))]
        witness = case["witnesses"]["parent_exact_maximizer"]["positive"]["parent"]
        assert witness["corners"] == [fw(1)] * 4 and witness["acquisition_coordinates"] == [
            fw(F(1, 8))
        ]
        assert witness["normalized_error"] == [fw(F(1, 4))]
        # A proper subset with z=-c/8 forces cancellation of every constant field.
        p = data["refinement"]["parent"]
        for c in (F(-1), F(-2, 3), F(0), F(1, 2), F(1)):
            e = engine.integrate(p["probe"], [p["tiles"][0]["bounds"]], [fw(c)] * 4)["raw_moments"]
            observed = engine.produce(p["interface"], e)
            n = F(1, 16) * (-c / 8)
            total = [fw(fraction(observed[0]) + n)]
            assert engine.apply(p["decoder"], total) == [fw(0)]
        # Opposite input signs can cancel; they are not a worst case over a product.
        assert fraction(witness["field_direct_error"][0]) == fraction(
            witness["acquisition_direct_error"][0]
        )


def test_small_cartesian_cube_extrema_against_direct_scalar_pipeline(engines):
    data = literal_product_problem()
    data["budgets"] = [{"name": "vertices", "field": fw(F(2, 3)), "acquisition": fw(F(3, 5))}]
    for engine in engines:
        f = engine.build_family(data)
        case = f["cases"][0]
        p = data["refinement"]["parent"]
        values = []
        for signs in product((-1, 1), repeat=5):
            corners = [F(2, 3) * x for x in signs[:4]]
            z = F(3, 5) * signs[-1]
            e = engine.integrate(p["probe"], [p["tiles"][0]["bounds"]], encode(corners))[
                "raw_moments"
            ]
            observed = engine.produce(p["interface"], e)
            total = [fw(fraction(observed[0]) + F(1, 16) * z)]
            values.append(fraction(engine.apply(p["decoder"], total)[0]) / F(1, 16))
        bound = fraction(case["levels"]["parent"]["bounds"]["bilinear_lower"][0])
        assert (min(values), max(values)) == (-bound, bound) == (-F(41, 60), F(41, 60))


def test_zero_field_budget_makes_mixed_total_exact_without_recertifying_field(engines):
    data = make_input(mixed_midpoint())
    for engine in engines:
        f = engine.build_family(data)
        assert f["field"]["levels"]["parent"]["certification"]["uncertified_rows"] == [0]
        assert f["field"]["levels"]["child"]["certification"]["uncertified_rows"] == [0]
        for case in f["cases"]:
            eps = fraction(case["budget"]["field"])
            for level in ("parent", "child"):
                info = case["levels"][level]
                assert info["exactness"]["reason"] == [
                    "zero_field_budget" if eps == 0 else "unavailable"
                ]
                assert (info["bounds"]["exact_gain"][0] is None) == (eps > 0)
                for key in ("constant", "bilinear", "exact"):
                    group = case["witnesses"][level + "_" + key + "_maximizer"]
                    if eps == 0:
                        assert group is not None and not any(group["field_signs"])
            if eps == 0:
                assert case["exact_bridge"]["inherited_rows"] == [0]
                assert all(c["gain_gap"] == [fw(0)] for c in case["comparison"].values())


def test_exact_subset_maxima_and_new_child_certificates(engines):
    for engine in engines:
        f = engine.build_family(subset_dominant_problem())
        case = f["cases"][1]
        for level in ("parent", "child"):
            bounds = case["levels"][level]["bounds"]
            exactness = case["levels"][level]["exactness"]
            assert exactness["available_rows"] == [0, 2] and exactness["unavailable_rows"] == [1]
            assert bounds["maxima"]["exact_gain"]["rows"] == [0]
            assert fraction(bounds["bilinear_lower"][1]) > fraction(
                bounds["maxima"]["exact_gain"]["gain"]
            )
        refined = engine.build_family(make_input(mixed_zero_split()))
        field_case = refined["cases"][1]
        assert field_case["exact_bridge"]["newly_exact_rows"] == [0]
        assert field_case["levels"]["parent"]["bounds"]["exact_gain"] == [None]
        assert field_case["levels"]["child"]["exactness"]["reason"] == ["field_certified"]


def test_opposite_row_endpoints_and_complete_zero_ties(engines):
    for engine in engines:
        f = engine.build_family(opposite_target_problem())
        case = f["cases"][3]
        bounds = case["levels"]["parent"]["bounds"]
        assert bounds["maxima"]["exact_gain"]["rows"] == [0, 1]
        gain = fraction(bounds["maxima"]["exact_gain"]["gain"])
        e = case["witnesses"]["parent_exact_maximizer"]["positive"]["parent"]
        assert e["normalized_error"] == encode([gain, -gain])
        zero = f["cases"][0]
        assert all(
            value["rows"] == [0, 1] and value["gain"] == fw(0)
            for value in zero["levels"]["parent"]["bounds"]["maxima"].values()
        )
        for group in zero["witnesses"].values():
            if "field_signs" in group:
                assert not any(group["field_signs"]) and not any(group["acquisition_signs"])


def test_null_raw_acquisition_cancelled_field_and_all_undefined(engines):
    for engine in engines:
        for allnull in (False, True):
            f = engine.build_family(null_acquisition_problem(allnull))
            case = f["cases"][2]
            e = case["witnesses"]["parent_constant"]["positive"]["parent"]
            assert any(fraction(x) for x in e["acquisition_direct_error"])
            assert e["acquisition_direct_error"] == e["total_decoded_error"]
            assert all(x == fw(0) for x in e["field_direct_error"])
            for row in f["field"]["geometry"]["undefined_rows"]:
                assert e["normalized_error"][row] is None
                assert f["acquisition"]["normalized_map"][row] is None
                assert all(
                    x == fw(0) for x in f["field"]["levels"]["parent"]["maps"]["decoder_bank"][row]
                )
            if allnull:
                assert all(
                    case["witnesses"][name] is None
                    for name in case["witnesses"]
                    if name.endswith("_maximizer")
                )
                assert all(
                    x["gain"] is None and x["rows"] == []
                    for x in case["levels"]["parent"]["bounds"]["maxima"].values()
                )
        zero = engine.build_family(make_input(identity_refinement(positive_zero_problem()), [1, 2]))
        assert zero["field"]["levels"]["parent"]["bounds"]["certified_gain"] == [fw(0)]
        assert zero["acquisition"]["gain"] == [fw(48)]
        assert zero["cases"][3]["levels"]["parent"]["bounds"]["exact_gain"] == [fw(48)]


def test_nonzero_radii_zero_noise_budget_and_zero_radii_are_distinct(engines):
    data = literal_product_problem()
    for engine in engines:
        f = engine.build_family(data)
        field = f["cases"][1]
        assert f["acquisition"]["gain"] == [fw(1)]
        for name, group in field["witnesses"].items():
            if group is not None and name.endswith("_maximizer"):
                assert group["acquisition_signs"] == [0]
        data0 = replaced(data, ["receiver_radii"], [fw(0)])
        g = engine.build_family(data0)
        assert g["acquisition"]["raw_map"] == [[fw(0)]] and g["acquisition"]["gain"] == [fw(0)]
        assert g["cases"][3]["levels"]["parent"]["bounds"]["exact_gain"] == [fw(F(1, 8))]
        empty = engine.build_family(make_input(identity_refinement(empty_receiver_problem()), []))
        assert empty["acquisition"]["raw_map"] == [[]] and empty["acquisition"]["gain"] == [fw(0)]


def case_pipeline_records(case):
    records = []
    for name, group in case["witnesses"].items():
        if group is None:
            continue
        for side in ("positive", "negative"):
            if name.startswith("parent_"):
                records.extend((level, group[side][level]) for level in ("parent", "child"))
            else:
                records.append(("child", group[side]))
    return records


def test_every_joint_endpoint_uses_actual_declared_public_apis(engines, monkeypatch):
    from collections import Counter

    for engine in engines:
        for data in (
            make_input(mixed_midpoint()),
            make_input(mixed_zero_split()),
            null_acquisition_problem(True),
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
            for case in f["cases"]:
                for level, e in case_pipeline_records(case):
                    p = (
                        data["refinement"]["parent"]
                        if level == "parent"
                        else f["field"]["child_problem"]
                    )
                    required["integrate"].append(
                        wire([p["probe"], [x["bounds"] for x in p["tiles"]], e["corners"]])
                    )
                    for a, x in (
                        (p["interface"], e["bank_error"]),
                        (p["geometric"], e["bank_error"]),
                        (f["acquisition"]["raw_map"], e["acquisition_coordinates"]),
                    ):
                        required["produce"].append(wire([a, x]))
                    for x in ("field_observed_error", "acquisition_error", "total_observed_error"):
                        required["apply"].append(wire([p["decoder"], e[x]]))
            count = 2 * f["counts"]["parent_paired_witnesses"] + f["counts"]["child_witnesses"]
            assert {k: len(v) for k, v in required.items()} == {
                "integrate": count,
                "produce": 3 * count,
                "apply": 3 * count,
            }
            for name, want in required.items():
                actual, needed = Counter(recorded[name]), Counter(want)
                assert all(actual[key] >= v for key, v in needed.items())


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


def affine_input(data, au, bv, cu, dv, receiver, inverse):
    out = copy.deepcopy(data)
    p, blocks, back, k = affine_problem(
        data["refinement"]["parent"], au, bv, cu, dv, receiver, inverse
    )
    out["refinement"]["parent"] = p
    for old, new in zip(data["refinement"]["children"], out["refinement"]["children"], strict=True):
        u0, u1, v0, v1 = rect(old["bounds"])
        new["bounds"] = rational_wire([au * u0 + bv, au * u1 + bv, cu * v0 + dv, cu * v1 + dv])
    out["receiver_radii"] = encode(mv(receiver, list(map(fraction, data["receiver_radii"]))))
    return out, blocks, back, k


@pytest.mark.parametrize("factory", [ba_unequal_problem, lambda: null_acquisition_problem(True)])
def test_positive_scale_permutation_affine_transport_same_box(engines, factory):
    data = factory()
    receiver = [[F(0), F(2)], [F(3), F(0)]]
    inverse = [[F(0), F(1, 3)], [F(1, 2), F(0)]]
    moved, bank, _, k = affine_input(data, F(3, 2), F(-7, 5), F(5, 3), F(11, 7), receiver, inverse)
    want = expected(moved)
    for engine in engines:
        a, b = engine.build_family(data), engine.build_family(moved)
        assert wire(b) == wire(want)
        assert a["field"]["restriction_blocks"] == b["field"]["restriction_blocks"]
        assert a["acquisition"]["gain"] == b["acquisition"]["gain"]
        for name in ("parent", "child"):
            assert a["field"]["levels"][name]["bounds"] == b["field"]["levels"][name]["bounds"]
            assert (
                a["field"]["levels"][name]["certification"]
                == b["field"]["levels"][name]["certification"]
            )
        for first, second in zip(a["cases"], b["cases"], strict=True):
            assert (
                first["levels"] == second["levels"] and first["comparison"] == second["comparison"]
            )
            assert first["exact_bridge"] == second["exact_bridge"]
            # The index-pattern noise control is intentionally not tensorial under
            # permutation. Transport the SAME inputs separately, then compare.
            x = first["witnesses"]["parent_pattern"]["positive"]["parent"]
            z = list(reversed(x["acquisition_coordinates"]))
            p = moved["refinement"]["parent"]
            raw = engine.integrate(p["probe"], [t["bounds"] for t in p["tiles"]], x["corners"])[
                "raw_moments"
            ]
            assert raw == encode(scalar_synthesize(bank, list(map(fraction, x["bank_error"]))))
            observed = engine.produce(p["interface"], raw)
            noise = [
                fraction(r) * fraction(v) for r, v in zip(moved["receiver_radii"], z, strict=True)
            ]
            assert encode(noise) == encode(
                mv(receiver, list(map(fraction, x["acquisition_error"])))
            )
            total = [fraction(y) + n for y, n in zip(observed, noise, strict=True)]
            actual = engine.apply(p["decoder"], encode(total))
            assert actual == [fw(k**4 * fraction(v)) for v in x["total_decoded_error"]]
            for name in first["witnesses"]:
                if name == "parent_pattern" or first["witnesses"][name] is None:
                    continue
                for side in ("positive", "negative"):
                    u, v = first["witnesses"][name][side], second["witnesses"][name][side]
                    if name.startswith("parent_"):
                        u, v = u["parent"], v["parent"]
                    assert u["normalized_error"] == v["normalized_error"]
                    assert v["acquisition_coordinates"] == list(
                        reversed(u["acquisition_coordinates"])
                    )


def test_mixed_receiver_transform_requires_transporting_the_set_not_a_fresh_box():
    # n=(x,y), |x|,|y|<=1, D=(1,0). T mixes outputs into (x+y,x-y).
    # Transported D'=(1/2,1/2) retains gain1 on that parallelogram.
    receiver = [[F(1), F(1)], [F(1), F(-1)]]
    decoded = [F(1, 2), F(1, 2)]
    transported = [
        dot(decoded, mv(receiver, list(map(F, vertex)))) for vertex in product((-1, 1), repeat=2)
    ]
    enclosing_independent = [
        dot(decoded, list(map(F, vertex))) for vertex in product((-2, 2), repeat=2)
    ]
    assert max(transported) == 1 and max(enclosing_independent) == 2
    # Keeping unit radii instead would also silently change the physical set.
    assert [F(2), F(0)] not in [list(map(F, v)) for v in product((-1, 1), repeat=2)]


def test_budget_scaling_order_zero_radii_and_detached_aliases(engines, monkeypatch):
    base = literal_product_problem()
    base["budgets"] = [
        {"name": "fraction", "field": fw(F(1, 3)), "acquisition": fw(F(2, 5))},
        {"name": "double", "field": fw(F(2, 3)), "acquisition": fw(F(4, 5))},
    ]
    base["receiver_radii"][0] = base["budgets"][0]["field"]
    before = wire(base)
    want = expected(base)
    for engine in engines:

        def forbidden(*args, **kwargs):
            raise RuntimeError("mathematics may not read files")

        with monkeypatch.context() as patch:
            patch.setattr(builtins, "open", forbidden)
            patch.setattr(Path, "open", forbidden)
            f = engine.build_family(base)
        assert wire(f) == wire(want) and wire(base) == before
        assert [x["budget"]["name"] for x in f["cases"]] == ["fraction", "double"]
        a, b = f["cases"]
        for level in ("parent", "child"):
            for key in ("constant_lower", "bilinear_lower", "corner_upper", "exact_gain"):
                assert b["levels"][level]["bounds"][key] == [
                    fw(2 * fraction(x)) for x in a["levels"][level]["bounds"][key]
                ]
        f["input"]["receiver_radii"][0][0] += 1
        f["cases"][0]["budget"]["field"][0] += 1
        assert wire(base) == before and wire(engine.build_family(base)) == wire(want)


def test_separate_cap_edges_with_small_independent_workloads(engines):
    unit = {"event": 0, "bounds": [0, 1, 0, 1]}
    null = {"event": 1, "bounds": None}
    strips = [{"event": 0, "bounds": [F(i, 256), F(i + 1, 256), 0, 1]} for i in range(256)]
    labels = [{"first": 1, "second": 1}]
    p = make_problem(unit["bounds"], [unit, null], strips, [], [[]], labels)
    one = make_problem(unit["bounds"], [unit, null], [unit], [], [[]], labels)
    many = {
        "parent": one,
        "children": [{"parent": 0, "bounds": rational_wire(t["bounds"])} for t in strips],
    }
    wide = make_problem(unit["bounds"], [unit], [unit], [[0] * 4] * 320, [[0] * 320])
    cells = [unit, *[{"event": i, "bounds": None} for i in range(1, 8)]]
    q64 = make_problem(
        unit["bounds"],
        cells,
        [unit],
        [],
        [[]] * 64,
        [{"first": i, "second": j} for i in range(8) for j in range(8)],
    )
    cases = [
        make_input(identity_refinement(p), [], [("one", 0, 0)]),
        make_input(many, [], [("one", 0, 0)]),
        make_input(identity_refinement(wide), [0] * 320, [("one", 0, 0)]),
        make_input(identity_refinement(q64), [], [("one", 0, 0)]),
        make_input(
            identity_refinement(empty_receiver_problem()),
            [],
            [(str(i), i % 2, (i + 1) % 2) for i in range(8)],
        ),
    ]
    for engine in engines:
        for data in cases:
            assert wire(engine.build_family(data)) == wire(expected(data))
        assert engine.produce([[]] * 1024, []) == [fw(0)] * 1024
        assert engine.produce([], [fw(0)] * 1024) == []
        assert engine.apply([[]] * 64, []) == [fw(0)] * 64
        assert engine.apply([], [fw(0)] * 320) == []


def test_raw_partial_empty_unbounded_signed_helper_semantics(engines):
    probe = rational_wire([-2, 3, -1, 2])
    tiles = [rational_wire([-2, -1, -1, 2]), rational_wire([1, 3, 0, 1])]
    c = rational_wire([-3, 0, 2, 7, 1, -2, 4, -5])
    rows = rational_wire([[1, -2, 3, -4, 4, 3, -2, 1], [0] * 8])
    want = integral_oracle(probe, tiles, c)
    kernels = kernel_oracle(probe, tiles, rows)
    for engine in engines:
        assert wire(engine.integrate(probe, tiles, c)) == wire(want)
        assert wire(engine.inspect_kernel(probe, tiles, rows)) == wire(kernels)
        assert engine.integrate(probe, [], []) == {key: [] for key in want}
        assert engine.inspect_kernel(probe, [], [[], []]) == {key: [[], []] for key in kernels}


class NativeListSubclass(list):
    pass


class NativeDictSubclass(dict):
    pass


class NativeIntSubclass(int):
    pass


def malformed_refinements():
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


def refinement_explicit_guards(engine):
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
    if engine.build_family(make_input(identity_refinement(p)))["field"]["levels"]["parent"][
        "bounds"
    ]["certified_gain"] != [fw(0)]:
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
            make_input(identity_refinement(make_problem(cell["bounds"], [cell], [cell], [], [[]])))
        )
    )
    count += 1
    cycle = []
    cycle.append(cycle)
    p = unit_problem()
    p["tiles"].append(p["tiles"])
    for call in (
        lambda: engine.build_family(
            {"refinement": {"parent": p, "children": []}, "receiver_radii": [], "budgets": []}
        ),
        lambda: engine.produce(cycle, [fw(1)]),
        lambda: engine.apply([[fw(1)]], cycle),
        lambda: engine.integrate(rational_wire([0, 1, 0, 1]), [], cycle),
        lambda: engine.inspect_kernel(rational_wire([0, 1, 0, 1]), [], cycle),
    ):
        require_rejection(call)
        count += 1
    return count


def refinement_pre_arithmetic_guards(engine):
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
                    replaced(
                        make_input(unequal_refinement()),
                        ["refinement", "children", -1, "bounds", -1],
                        value,
                    )
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
                replaced(
                    make_input(unequal_refinement()),
                    ["refinement", "parent", "decoder", -1, -1],
                    [1, 0],
                )
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
    assert [pre_arithmetic_guards(engine) for engine in engines] == [27, 27]


@pytest.mark.parametrize("optimized", [False, True])
def test_isolated_explicit_normal_and_optimized_guards(tmp_path, optimized):
    script = r"""
import importlib.util,json,sys
from pathlib import Path
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("ba_guard_tests",path)
t=importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
counts=[]
for name,file in (("primary","kernel.py"),("reference","reference.py")):
    engine=t.load("_qr05ba_guard_"+name,file)
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
        + 42
    )
    assert json.loads(result.stdout) == [total, total]


def malformed_families():
    data = make_input(unequal_refinement())
    for ref in malformed_refinements():
        yield {**data, "refinement": ref}
    yield None
    yield []
    yield NativeDictSubclass(data)
    for key in data:
        yield {k: v for k, v in data.items() if k != key}
    yield {**data, "confidence": fw(1)}
    for value in (None, (), [], NativeListSubclass(data["receiver_radii"]), [fw(0)] * 3):
        yield replaced(data, ["receiver_radii"], value)
    for value in (None, (), [], NativeListSubclass(data["budgets"]), data["budgets"] * 3):
        yield replaced(data, ["budgets"], value)
    for value in (
        None,
        [],
        {},
        {"name": "bad", "field": fw(1)},
        {"name": "bad", "acquisition": fw(1)},
    ):
        yield replaced(data, ["budgets", -1], value)
    for value in ("", False, 1, data["budgets"][0]["name"]):
        yield replaced(data, ["budgets", -1, "name"], value)
    yield replaced(data, ["budgets", -1, "extra"], 0)
    for value in (True, 0.0, F(1), (1, 1), [0], [1, 0], [2, 2], [-1, 1], [1 << 4096, 1]):
        for path in (
            ["receiver_radii", -1],
            ["budgets", -1, "field"],
            ["budgets", -1, "acquisition"],
        ):
            yield replaced(data, path, value)


def explicit_guards(engine):
    count = refinement_explicit_guards(engine)
    d = 1 << 4095
    unit = {"event": 0, "bounds": [0, 1, 0, 1]}
    p = make_problem(unit["bounds"], [unit], [unit], [[0] * 4], [[d]])
    for rho in (1, 2):
        data = make_input(identity_refinement(p), [rho], [("zero", 0, 0)])
        require_rejection(lambda data=data: engine.build_family(data))
        count += 1
    data = literal_product_problem()
    data["budgets"] = [{"name": "composed-overflow", "field": fw(0), "acquisition": fw(d)}]
    data["receiver_radii"] = [fw(1)]
    require_rejection(lambda: engine.build_family(data))
    count += 1
    raw = null_acquisition_problem(True)
    raw["receiver_radii"] = [fw(1), fw(0)]
    raw["budgets"] = [{"name": "undefined-raw-overflow", "field": fw(0), "acquisition": fw(d)}]
    require_rejection(lambda: engine.build_family(raw))
    count += 1
    return count


def pre_arithmetic_guards(engine):
    count = refinement_pre_arithmetic_guards(engine)
    called = []

    def forbidden(*args, **kwargs):
        called.append(1)
        raise RuntimeError("budget/radius arithmetic before complete admission")

    original = engine._fraction
    engine._fraction = forbidden
    try:
        for path in (
            ["receiver_radii", -1],
            ["budgets", -1, "field"],
            ["budgets", -1, "acquisition"],
        ):
            for value in ([], [0]):
                bad = replaced(make_input(unequal_refinement()), path, value)
                require_rejection(lambda bad=bad: engine.build_family(bad))
                count += 1
    finally:
        engine._fraction = original
    names = [
        name
        for name in (
            "_geometry",
            "_area",
            "_partition",
            "_child_partition",
            "_restriction_blocks",
            "_restrictions",
            "_physical_integral",
            "_dot",
            "_mm",
            "_level",
            "_acquisition",
        )
        if hasattr(engine, name)
    ]
    old = {name: getattr(engine, name) for name in names}
    for name in names:
        setattr(engine, name, forbidden)
    try:
        for path in (
            ["receiver_radii", -1],
            ["budgets", -1, "field"],
            ["budgets", -1, "acquisition"],
        ):
            for value in ([1, 0], [-1, 1]):
                bad = replaced(make_input(unequal_refinement()), path, value)
                require_rejection(lambda bad=bad: engine.build_family(bad))
                count += 1
    finally:
        for name, value in old.items():
            setattr(engine, name, value)
    if called:
        raise RuntimeError("early work occurred")
    return count


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
    p = f["input"]["refinement"]["parent"]
    for key in p:
        yield ["input", "refinement", "parent", key]
    yield ["input", "refinement", "children"]
    yield ["input", "receiver_radii"]
    for key in ("name", "field", "acquisition"):
        yield ["input", "budgets", -1, key]
    for key in f["field"]["child_problem"]:
        yield ["field", "child_problem", key]
    for key in f["field"]["geometry"]:
        yield ["field", "geometry", key]
    yield ["field", "restriction_blocks"]
    for level in ("parent", "child"):
        for group in ("kernels", "maps"):
            for key in f["field"]["levels"][level][group]:
                yield ["field", "levels", level, group, key]
        for key in ("constant_lower", "bilinear_lower", "corner_upper", "certified_gain"):
            yield ["field", "levels", level, "bounds", key]
        yield ["field", "levels", level, "bounds", "maxima"]
        yield ["field", "levels", level, "certification", "status"]
        yield ["field", "levels", level, "certification", "mixed_obstructions"]
        yield ["field", "levels", level, "certification", "integrated_nonnegative_mixed_rows"]
    for key in ("raw_map", "normalized_map", "gain"):
        yield ["acquisition", key]
    for key in ("gain", "rows"):
        yield ["acquisition", "maxima", key]
    # Detailed scientific case corruption is bounded to the last supplied budget.
    # Complete independent comparisons/counts cover every budget, including zero.
    last = len(f["cases"]) - 1
    case = f["cases"][last]
    yield ["cases", last, "budget"]
    for level in ("parent", "child"):
        for key in ("constant_lower", "bilinear_lower", "corner_upper", "exact_gain"):
            yield ["cases", last, "levels", level, "bounds", key]
            yield ["cases", last, "levels", level, "bounds", "maxima", key]
        for key in case["levels"][level]["exactness"]:
            yield ["cases", last, "levels", level, "exactness", key]
    for name in case["comparison"]:
        for key in case["comparison"][name]:
            yield ["cases", last, "comparison", name, key]
    for key in case["exact_bridge"]:
        yield ["cases", last, "exact_bridge", key]
    for name, group in case["witnesses"].items():
        prefix = ["cases", last, "witnesses", name]
        if group is None:
            yield prefix
            continue
        if "target_row" in group:
            for key in ("target_row", "field_signs", "acquisition_signs"):
                yield [*prefix, key]
        if name == "parent_pattern":
            for key in group["positive"]:
                if key in ("parent", "child"):
                    for field in group["positive"][key]:
                        yield [*prefix, "positive", key, field]
                else:
                    yield [*prefix, "positive", key]
        elif name == "child_exact_maximizer":
            for field in group["positive"]:
                yield [*prefix, "positive", field]
        else:
            yield [*prefix, "positive"]
        yield [*prefix, "negative"]
    for key in f["checks"]:
        yield ["checks", key]
    for key in ("input_budget_entries", "case_bound_entries", "witness_entries"):
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
        return sum(rationals(x) for x in value.values())
    if type(value) is list:
        return sum(rationals(x) for x in value)
    return 0


def bound_rationals(bounds):
    return sum(rationals(x) for key, x in bounds.items() if key != "maxima") + sum(
        rationals(x["gain"]) for x in bounds["maxima"].values()
    )


def literal_count_checks(f):
    counts = f["counts"]
    data = f["input"]
    parent = data["refinement"]["parent"]
    children = data["refinement"]["children"]
    field = f["field"]
    geometry = field["geometry"]
    assert counts["input_geometry_entries"] == rationals(parent["probe"]) + sum(
        rationals(x["bounds"]) for key in ("cells", "tiles") for x in parent[key]
    ) + sum(rationals(x["bounds"]) for x in children)
    assert counts["input_matrix_entries"] == sum(
        rationals(parent[key]) for key in ("interface", "geometric", "decoder")
    )
    assert counts["input_budget_entries"] == rationals(data["receiver_radii"]) + sum(
        rationals(x["field"]) + rationals(x["acquisition"]) for x in data["budgets"]
    )
    assert counts["geometry_entries"] == sum(
        rationals(geometry[key])
        for key in (
            "volume",
            "cell_volumes",
            "target_scales",
            "parent_tile_volumes",
            "child_tile_volumes",
        )
    )
    assert counts["restriction_entries"] == rationals(field["restriction_blocks"])
    for level in ("parent", "child"):
        k = field["levels"][level]
        assert counts[level + "_kernel_entries"] == sum(
            rationals(x) for key, x in k["kernels"].items() if key != "tile_classes"
        )
        assert counts[level + "_map_entries"] == rationals(k["maps"])
    assert counts["field_bound_entries"] == sum(
        bound_rationals(x["bounds"]) for x in field["levels"].values()
    )
    a = f["acquisition"]
    assert counts["acquisition_entries"] == sum(
        rationals(a[key]) for key in ("raw_map", "normalized_map", "gain")
    ) + rationals(a["maxima"]["gain"])
    assert counts["case_bound_entries"] == sum(
        bound_rationals(level["bounds"]) for c in f["cases"] for level in c["levels"].values()
    )
    assert counts["case_exact_bridge_entries"] == sum(
        rationals(c["exact_bridge"]["inherited_gain_residuals"]) for c in f["cases"]
    )
    assert counts["case_comparison_entries"] == sum(
        rationals(x["gain_gap"]) + rationals(x["max_gap"])
        for c in f["cases"]
        for x in c["comparison"].values()
    )
    pairs = child = entries = signs = 0
    for c in f["cases"]:
        for name, group in c["witnesses"].items():
            if group is None:
                continue
            if "field_signs" in group:
                signs += len(group["field_signs"]) + len(group["acquisition_signs"])
            for side in ("positive", "negative"):
                entries += rationals(group[side])
                if name.startswith("parent_"):
                    pairs += 1
                else:
                    child += 1
    assert (pairs, child, entries, signs) == tuple(
        counts[key]
        for key in ("parent_paired_witnesses", "child_witnesses", "witness_entries", "sign_entries")
    )
    assert counts["budgets"] == len(f["cases"])
    assert len(counts) == 35 and len(f["checks"]) == 16


@pytest.mark.parametrize(
    "factory",
    [
        lambda: make_input(mixed_zero_split()),
        subset_dominant_problem,
        lambda: null_acquisition_problem(True),
    ],
)
def test_complete_generic_corruptions_and_literal_count_inventory(runner, factory):
    f = expected(factory())
    literal_count_checks(f)
    before = wire(f)
    for bad in family_mutations(f):
        assert wire(bad) != before
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
    "statistical_independence_assumed",
    "field_receiver_error_double_counted",
    "total_source_nonnegativity_guaranteed",
    "global_field_continuity_required",
    "mixed_absolute_kernel_integrated",
    "uncertified_exact_gain_claimed",
    "corner_envelope_sharpness_claimed",
    "subset_exact_max_called_full_query_max",
    "independent_child_fields_called_parent_fields",
    "full_bounded_field_domain_changed",
    "equal_noise_sensor_improvement_claimed",
    "cross_geometry_physical_noise_ranking_claimed",
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
            "AZ_refinement_equal",
            "AZ_child_problem_equal",
            "AZ_geometry_equal",
            "AZ_restriction_blocks_equal",
            "AZ_levels_equal",
            "same_physical_field_domain",
            "same_receiver_contract",
        ),
        True,
    ),
    **dict.fromkeys(
        ("AZ_endpoints_replayed", "AZ_unselected_mathematics_replayed", "older_executors_run"),
        False,
    ),
}


def independent_history_checks(families, previous):
    assert [f["input"]["parent"]["family"] for f in previous] == list(FAMILIES)
    for f, old in zip(families, previous, strict=True):
        assert wire(f["input"]["refinement"]) == wire(old["input"])
        field = f["field"]
        for key in ("child_problem", "geometry", "levels"):
            assert wire(field[key]) == wire(old[key])
        assert wire(field["restriction_blocks"]) == wire(old["restriction"]["blocks"])
        literal_count_checks(f)


def payload(families):
    keys = {"input": "input", "field": "field", "acquisition": "acquisition", "case": "cases"}
    return [
        {
            "family": f["input"]["refinement"]["parent"]["family"],
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
    # New synthetic selected field evidence only. Never construct a discarded
    # AZ family, moment-block bank, transport calculation, or old endpoint.
    field = f["field"]
    return {
        "input": copy.deepcopy(f["input"]["refinement"]),
        **{key: copy.deepcopy(field[key]) for key in ("child_problem", "geometry", "levels")},
        "restriction": {
            "blocks": copy.deepcopy(field["restriction_blocks"]),
            "parent_moment_blocks": "not replayed",
            "child_moment_blocks": "not replayed",
            "aggregated_moment_blocks": "not replayed",
            "moment_residuals": "not replayed",
        },
        "transport": "not replayed",
        "comparison": "not replayed",
        "certification_bridge": "not replayed",
        "witnesses": "not replayed",
        "checks": "not replayed",
        "counts": "not replayed",
    }


def test_synthetic_history_full_suite_and_cached_routes(runner, monkeypatch):
    problems = []
    for name, factory in zip(
        FAMILIES,
        (lambda: make_input(mixed_zero_split()), lambda: null_acquisition_problem(True)),
        strict=True,
    ):
        data = factory()
        data["refinement"]["parent"]["family"] = name
        problems.append(data)
    families = list(map(expected, problems))
    previous = list(map(synthetic_history, families))
    independent_history_checks(families, previous)
    want = expected_suite(families)
    lookup = {f["input"]["refinement"]["parent"]["family"]: f for f in families}

    def project(prior):
        result = []
        for row in prior:
            data = copy.deepcopy(lookup[row["input"]["parent"]["family"]]["input"])
            data["refinement"] = copy.deepcopy(row["input"])
            result.append(data)
        return result, prior

    monkeypatch.setattr(runner, "project_inputs", project)
    monkeypatch.setattr(
        runner, "load_inputs", lambda: (copy.deepcopy(problems), copy.deepcopy(previous))
    )
    calls = []

    def loader(name):
        def build(p):
            assert p == lookup[p["refinement"]["parent"]["family"]]["input"]
            calls.append(name)
            return copy.deepcopy(lookup[p["refinement"]["parent"]["family"]])

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
        f = copy.deepcopy(lookup[p["refinement"]["parent"]["family"]])
        p["budgets"].reverse()
        return f

    monkeypatch.setattr(runner, "load_engine", lambda name: SimpleNamespace(build_family=changing))
    with pytest.raises(ValueError):
        runner.run_suite("primary")


def test_synthetic_selected_projection_declared_shapes_budget_order_and_detachment(runner):
    cell = {"event": 0, "bounds": [0, 1, 0, 1]}
    cells = [cell, *[{"event": i, "bounds": None} for i in range(1, 8)]]
    tiles = [{"event": 0, "bounds": [F(i, 12), F(i + 1, 12), 0, 1]} for i in range(12)]
    labels = [{"first": i, "second": j} for i in range(8) for j in range(8)]
    p = make_problem(cell["bounds"], cells, tiles, [[0] * 48] * 37, [[0] * 37] * 64, labels)
    refinement = {"parent": p, "children": quarter_children(p)}
    previous = [{"input": copy.deepcopy(refinement)} for _ in FAMILIES]
    for name, row in zip(FAMILIES, previous, strict=True):
        row["input"]["parent"]["family"] = name
    before = wire(previous)
    projected, consumed = runner.project_inputs(previous)
    assert consumed is previous
    for data, old in zip(projected, previous, strict=True):
        assert data == make_input(old["input"], [1] * 37)
    projected[0]["refinement"]["children"][0]["bounds"][0][0] = 999
    projected[0]["refinement"]["parent"]["probe"][0][0] = 999
    assert wire(previous) == before
    changes = [
        {},
        previous[:1],
        list(reversed(previous)),
        replaced(previous, [0, "input"], {**refinement, "extra": 0}),
        replaced(previous, [0, "input", "parent"], {**p, "extra": 0}),
        replaced(previous, [0, "input", "parent", "tiles"], []),
        replaced(previous, [0, "input", "parent", "bank_labels"], []),
        replaced(previous, [0, "input", "parent", "target_labels"], []),
        replaced(previous, [0, "input", "parent", "decoder", -1], []),
        replaced(previous, [0, "input", "children"], []),
        replaced(previous, [0, "input", "children", -1, "parent"], False),
        replaced(previous, [0, "input", "children", -1, "bounds", -1], [0]),
        replaced(previous, [0, "input", "children", -1, "bounds", 1], fw(-1)),
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
def test_fixed_complete_independent_field_acquisition_oracle(engines, fixed_data, index):
    problems, _, families, _ = fixed_data
    for engine in engines:
        supplied = copy.deepcopy(problems[index])
        before = wire(supplied)
        f = engine.build_family(supplied)
        assert wire(supplied) == before and wire(f) == wire(families[index])
        # Every budget and signed endpoint is covered by the complete oracle.
        # Re-execute two representative pipelines per budget through actual APIs.
        for case in f["cases"]:
            pair = case["witnesses"]["parent_pattern"]["positive"]
            for level in ("parent", "child"):
                e = pair[level]
                p = (
                    supplied["refinement"]["parent"]
                    if level == "parent"
                    else f["field"]["child_problem"]
                )
                field = engine.integrate(
                    p["probe"], [x["bounds"] for x in p["tiles"]], e["corners"]
                )
                assert field["raw_moments"] == e["bank_error"]
                assert field["global_coefficients"] == e["global_coefficients"]
                assert field["minima"] == e["tile_minima"] and field["maxima"] == e["tile_maxima"]
                observed = engine.produce(p["interface"], e["bank_error"])
                direct = engine.produce(p["geometric"], e["bank_error"])
                acquisition = engine.produce(
                    f["acquisition"]["raw_map"], e["acquisition_coordinates"]
                )
                assert observed == e["field_observed_error"] and direct == e["field_direct_error"]
                assert acquisition == e["acquisition_direct_error"]
                for key, target in (
                    ("field_observed_error", "field_decoded_error"),
                    ("acquisition_error", "acquisition_decoded_error"),
                    ("total_observed_error", "total_decoded_error"),
                ):
                    assert engine.apply(p["decoder"], e[key]) == e[target]


def test_fixed_full_suite_selected_history_counts_payload(runner, fixed_data):
    problems, previous, families, want = fixed_data
    assert wire(runner.assemble_suite(families, previous)) == wire(want)
    assert runner.historical_bridges(families, previous) == BRIDGES
    assert runner.payload_sizes(families) == payload(families)
    for data, f in zip(problems, families, strict=True):
        p = data["refinement"]["parent"]
        assert (
            len(p["cells"]),
            len(p["tiles"]),
            len(data["refinement"]["children"]),
            len(p["bank_labels"]),
            len(p["interface"]),
            len(p["target_labels"]),
        ) == (8, 12, 48, 48, 37, 64)
        assert data["receiver_radii"] == [fw(1)] * 37
        assert data["budgets"] == make_input(data["refinement"])["budgets"]
        literal_count_checks(f)
    assert len(SCOPE) == 30 and not any(want["scope"].values())


@pytest.mark.parametrize("route", ["primary", "reference", "compare"])
def test_fixed_cached_orchestration_routes(runner, fixed_data, monkeypatch, route):
    _, _, families, want = fixed_data
    lookup = {f["input"]["refinement"]["parent"]["family"]: f for f in families}
    seen = []

    def loader(name):
        def build(p):
            assert p == lookup[p["refinement"]["parent"]["family"]]["input"]
            seen.append(name)
            return copy.deepcopy(lookup[p["refinement"]["parent"]["family"]])

        return SimpleNamespace(build_family=build)

    monkeypatch.setattr(runner, "load_engine", loader)
    assert wire(runner.run_suite(route)) == wire(want)
    assert seen == (["primary", "reference"] * 2 if route == "compare" else [route] * 2)


def test_fixed_nonnoop_family_and_suite_corruptions(runner, fixed_data):
    _, _, families, want = fixed_data
    for f in families:
        original = wire(f)
        for bad in family_mutations(f):
            assert wire(bad) != original
            with pytest.raises(ValueError):
                runner.verify_suite(bad, f)
    changes = [
        replaced(want, ["families"], list(reversed(families))),
        replaced(want, ["prior_bridges", "AZ_levels_equal"], False),
        replaced(want, ["prior_bridges", "AZ_endpoints_replayed"], True),
        replaced(
            want, ["payload_sizes", 0, "case_bytes"], want["payload_sizes"][0]["case_bytes"] + 1
        ),
        replaced(want, ["totals", "witness_entries"], want["totals"]["witness_entries"] + 1),
        replaced(want, ["scope", "statistical_independence_assumed"], True),
        replaced(want, ["scope", "field_receiver_error_double_counted"], True),
        {**want, "extra": 0},
    ]
    original = wire(want)
    for bad in changes:
        assert wire(bad) != original
        with pytest.raises(ValueError):
            runner.verify_suite(bad, want)


def selected_history_mutations(previous):
    for path in (
        [0, "input", "parent", "probe"],
        [0, "input", "parent", "interface"],
        [0, "input", "parent", "geometric"],
        [0, "input", "parent", "decoder"],
        [0, "input", "children"],
        [0, "child_problem", "interface"],
        [0, "geometry", "volume"],
        [0, "geometry", "target_scales"],
        [0, "restriction", "blocks"],
        [0, "levels", "parent", "kernels", "bernstein_integrals"],
        [0, "levels", "parent", "maps", "raw_bilinear_target"],
        [0, "levels", "parent", "bounds", "certified_gain"],
        [0, "levels", "child", "bounds", "corner_upper"],
        [0, "levels", "child", "certification", "status"],
    ):
        yield changed_leaf(previous, path)
    yield replaced(previous, [0, "input", "parent", "bank_labels", 0, "basis"], False)
    yield replaced(previous, [0, "input", "parent", "target_labels", 0, "first"], False)


def test_fixed_selected_refinement_field_and_budget_projection_mutations(runner, fixed_data):
    _, previous, families, _ = fixed_data
    original = wire(previous)
    for bad in selected_history_mutations(previous):
        assert wire(bad) != original
        with pytest.raises(ValueError):
            runner.historical_bridges(families, bad)


def test_fixed_unselected_az_old_endpoints_moments_transport_not_replayed(runner, fixed_data):
    problems, previous, families, _ = fixed_data
    paths = [
        [0, key]
        for key in (
            "transport",
            "comparison",
            "certification_bridge",
            "witnesses",
            "checks",
            "counts",
        )
    ]
    paths += [
        [0, "restriction", key]
        for key in (
            "parent_moment_blocks",
            "child_moment_blocks",
            "aggregated_moment_blocks",
            "moment_residuals",
        )
    ]
    for path in paths:
        bad = replaced(previous, path, {"not": "read"})
        assert wire(bad) != wire(previous)
        assert runner.project_inputs(bad)[0] == problems
        assert runner.historical_bridges(families, bad) == BRIDGES


def test_fixed_source_and_ancestor_identity_inventory(runner):
    current = runner.identities()
    assert {key: len(value) for key, value in current.items()} == {
        "source_ledger": 5,
        "prior_artifacts": 57,
        "ancestor_sources": 104,
    }
    assert set(current["source_ledger"]) == set(runner.SOURCES)
    raw = runner.AZ.read_bytes()
    assert (
        len(raw) == 2380556
        and hashlib.sha256(raw).hexdigest()
        == "cbb04f7a4af49a5714ecf80652393933557f490f7e16dab0848b8d32cda27585"
    )
    for name, want in current["source_ledger"].items():
        raw = (HERE / name).read_bytes()
        assert len(raw) == want["bytes"] and hashlib.sha256(raw).hexdigest() == want["sha256"]
