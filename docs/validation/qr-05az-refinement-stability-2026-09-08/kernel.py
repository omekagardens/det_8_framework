"""Exact refinement transport of supplied bounded-field response kernels."""

import json
from fractions import Fraction as F
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind is int:
        _require(value.bit_length() <= 4096, "integer exceeds retained component bound")
    elif value is None or kind in (str, bool):
        return
    elif kind in (list, dict):
        identity = id(value)
        _require(identity not in active, "cyclic native containers are not supported")
        if kind is dict:
            _require(all(type(key) is str for key in value), "native string keys required")
        active.add(identity)
        try:
            for child in value if kind is list else value.values():
                _native(child, active)
        finally:
            active.remove(identity)
    else:
        raise ValueError("exact native mathematical wire required")


def _encode(value):
    if type(value) is F:
        _require(
            max(value.numerator.bit_length(), value.denominator.bit_length()) <= 4096,
            "retained fraction exceeds component bound",
        )
        return [value.numerator, value.denominator]
    if type(value) is list:
        return [_encode(x) for x in value]
    if type(value) is dict:
        return {key: _encode(child) for key, child in value.items()}
    return value


def canonical(value):
    _native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def _detach(value):
    return json.loads(canonical(_encode(value)))


def _fields(value, keys):
    _require(type(value) is dict and set(value) == set(keys), "unexpected fixture fields")


def _fraction(pair):
    _require(type(pair) is list and len(pair) == 2, "native fraction pair required")
    n, d = pair
    _require(
        type(n) is int
        and type(d) is int
        and d > 0
        and max(n.bit_length(), d.bit_length()) <= 4096
        and gcd(n, d) == 1,
        "reduced bounded fraction required",
    )
    return F(n, d)


def _pair_shape(value):
    _require(type(value) is list and len(value) == 2, "native rational-pair shape required")


def _vector_shape(value, width):
    _require(type(value) is list and len(value) == width, "vector width differs")
    for pair in value:
        _pair_shape(pair)


def _matrix_shape(value, rows, columns):
    _require(type(value) is list and len(value) == rows, "matrix row inventory differs")
    for row in value:
        _vector_shape(row, columns)


def _matrix(value):
    return [list(map(_fraction, row)) for row in value]


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True) if x and y), F(0))


def _mm(left, right, columns=None):
    if not right:
        _require(columns is not None, "empty product requires its column dimension")
        return [[F(0)] * columns for _ in left]
    transposed = list(zip(*right, strict=True))
    return [[_dot(row, column) for column in transposed] for row in left]


def _raw_product(matrix, values, row_cap, width_cap):
    _native(matrix)
    _native(values)
    _require(type(matrix) is list and len(matrix) <= row_cap, "matrix row cap")
    _require(type(values) is list and len(values) <= width_cap, "raw width cap")
    _matrix_shape(matrix, len(matrix), len(values))
    _vector_shape(values, len(values))
    parsed = _matrix(matrix)
    vector = list(map(_fraction, values))
    return _detach([_dot(row, vector) for row in parsed])


def produce(matrix, values):
    """Evaluate a supplied raw matrix without source or geometry access."""
    return _raw_product(matrix, values, 1024, 1024)


def apply(matrix, observed):
    """Evaluate a supplied zero-intercept receiver."""
    return _raw_product(matrix, observed, 64, 320)


def _rectangle_shape(value, nullable=False):
    if value is None and nullable:
        return
    _vector_shape(value, 4)


def _problem_shape(problem):
    _native(problem)
    _fields(
        problem,
        (
            "family",
            "probe",
            "cells",
            "tiles",
            "bank_labels",
            "target_labels",
            "interface",
            "geometric",
            "decoder",
        ),
    )
    _require(type(problem["family"]) is str and problem["family"], "family label required")
    _rectangle_shape(problem["probe"])
    cells = problem["cells"]
    tiles = problem["tiles"]
    _require(type(cells) is list and 1 <= len(cells) <= 8, "cell inventory cap")
    _require(type(tiles) is list and 1 <= len(tiles) <= 256, "tile inventory cap")
    ids = []
    for cell in cells:
        _fields(cell, ("event", "bounds"))
        _require(type(cell["event"]) is int, "native cell ID required")
        ids.append(cell["event"])
        _rectangle_shape(cell["bounds"], True)
    _require(ids == sorted(set(ids)), "sorted unique cell IDs required")
    owners = set(ids)
    for tile in tiles:
        _fields(tile, ("event", "bounds"))
        _require(type(tile["event"]) is int and tile["event"] in owners, "unknown tile owner")
        _rectangle_shape(tile["bounds"])
    t = len(tiles)
    r = 4 * t
    labels = problem["bank_labels"]
    _require(type(labels) is list and len(labels) == r, "bank label inventory")
    for index, label in enumerate(labels):
        _fields(label, ("tile", "basis"))
        _require(
            type(label["tile"]) is int
            and type(label["basis"]) is int
            and label["tile"] == index // 4
            and label["basis"] == index % 4,
            "bank labels must follow the supplied tile order",
        )
    targets = problem["target_labels"]
    _require(type(targets) is list and 1 <= len(targets) <= 64, "target inventory cap")
    target_order = []
    for target in targets:
        _fields(target, ("first", "second"))
        _require(
            type(target["first"]) is int
            and type(target["second"]) is int
            and target["first"] in owners
            and target["second"] in owners,
            "target cell IDs required",
        )
        target_order.append((target["first"], target["second"]))
    _require(target_order == sorted(set(target_order)), "sorted unique targets required")
    q = len(targets)
    B = problem["interface"]
    _require(type(B) is list and len(B) <= 320, "receiver inventory cap")
    s = len(B)
    _matrix_shape(B, s, r)
    _matrix_shape(problem["geometric"], q, r)
    _matrix_shape(problem["decoder"], q, s)
    return cells, tiles, B, target_order, q, r, s, t


def _problem(problem):
    cells, tiles, B, target_order, q, r, s, t = _problem_shape(problem)
    # This parser is called only after the outer parent/child shape pass.
    probe = list(map(_fraction, problem["probe"]))
    parsed_cells = [
        None if cell["bounds"] is None else list(map(_fraction, cell["bounds"])) for cell in cells
    ]
    parsed_tiles = [list(map(_fraction, tile["bounds"])) for tile in tiles]
    B = _matrix(B)
    G = _matrix(problem["geometric"])
    D = _matrix(problem["decoder"])
    # Every supplied scalar has been admitted before geometry or products.
    return probe, parsed_cells, parsed_tiles, B, G, D, target_order, q, r, s, t


def _inside(rectangle, outer):
    return (
        outer[0] <= rectangle[0] < rectangle[1] <= outer[1]
        and outer[2] <= rectangle[2] < rectangle[3] <= outer[3]
    )


def _positive(rectangle):
    return rectangle[0] < rectangle[1] and rectangle[2] < rectangle[3]


def _area(rectangle):
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2]) / 2


def _overlap(left, right):
    return max(left[0], right[0]) < min(left[1], right[1]) and max(left[2], right[2]) < min(
        left[3], right[3]
    )


def _partition(rectangles, outer):
    _require(all(_inside(rectangle, outer) for rectangle in rectangles), "partition containment")
    for i, left in enumerate(rectangles):
        _require(
            all(not _overlap(left, right) for right in rectangles[i + 1 :]),
            "partition interiors overlap",
        )
    _require(
        sum((_area(rectangle) for rectangle in rectangles), F(0)) == _area(outer),
        "partition area differs",
    )


def _geometry(problem, probe, cells, tiles, target_order):
    _require(_positive(probe), "positive probe required")
    _require(
        all(cell is None or _positive(cell) for cell in cells), "positive or null cells required"
    )
    _require(all(_positive(tile) for tile in tiles), "positive bank tiles required")
    _partition([cell for cell in cells if cell is not None], probe)
    ids = [cell["event"] for cell in problem["cells"]]
    owned = {event: [] for event in ids}
    cell_by_id = dict(zip(ids, cells, strict=True))
    for tile, item in zip(tiles, problem["tiles"], strict=True):
        owner = item["event"]
        _require(cell_by_id[owner] is not None, "bank tile has a null owner")
        owned[owner].append(tile)
    for event, cell in cell_by_id.items():
        if cell is not None:
            _partition(owned[event], cell)
    V = _area(probe)
    cell_volumes = [F(0) if cell is None else _area(cell) for cell in cells]
    tile_volumes = list(map(_area, tiles))
    by_id = dict(zip(ids, cell_volumes, strict=True))
    scales = [V * V * by_id[first] * by_id[second] for first, second in target_order]
    defined = [i for i, scale in enumerate(scales) if scale > 0]
    undefined = [i for i, scale in enumerate(scales) if scale == 0]
    return V, cell_volumes, tile_volumes, scales, defined, undefined


def _subtract(left, right):
    return [[x - y for x, y in zip(a, b, strict=True)] for a, b in zip(left, right, strict=True)]


def _zero(matrix):
    return all(value == 0 for row in matrix for value in row)


def _sign(value):
    return int(value > 0) - int(value < 0)


def _vector(value):
    return list(map(_fraction, value))


def _linear(matrix, values):
    return [_dot(row, values) for row in matrix]


def _normalized(values, scales):
    return [value / scale if scale else None for value, scale in zip(values, scales, strict=True)]


def _maximum(values, defined):
    if not defined:
        return None, []
    maximum = max(values[i] for i in defined)
    return maximum, [i for i in defined if values[i] == maximum]


def _power_integral(lower, upper, power):
    return (upper ** (power + 1) - lower ** (power + 1)) / (power + 1)


def _physical_integral(coefficients, rectangle, test_u, test_v):
    u0, u1, v0, v1 = rectangle
    powers = ((0, 0), (1, 0), (0, 1), (1, 1))
    terms = []
    for coefficient, (i, j) in zip(coefficients, powers, strict=True):
        for p, left in enumerate(test_u):
            for q, right in enumerate(test_v):
                terms.append(
                    coefficient
                    * left
                    * right
                    * _power_integral(u0, u1, i + p)
                    * _power_integral(v0, v1, j + q)
                    / 2
                )
    return sum(terms, F(0))


def integrate(probe, tiles, corners):
    """Integrate the actual signed bilinear field; standalone corners are unbounded."""
    _native(probe)
    _native(tiles)
    _native(corners)
    _rectangle_shape(probe)
    _require(type(tiles) is list and len(tiles) <= 256, "integration tile cap")
    for tile in tiles:
        _rectangle_shape(tile)
    _vector_shape(corners, 4 * len(tiles))
    rectangle = list(map(_fraction, probe))
    boxes = [list(map(_fraction, tile)) for tile in tiles]
    values = list(map(_fraction, corners))
    _require(_positive(rectangle), "positive integration probe")
    _require(all(_inside(box, rectangle) for box in boxes), "integration tile containment")
    for i, box in enumerate(boxes):
        _require(
            all(not _overlap(box, other) for other in boxes[i + 1 :]),
            "integration tiles overlap",
        )
    V = _area(rectangle)
    amplitude = V * V
    local_coefficients, global_coefficients = [], []
    local_moments, raw_moments, minima, maxima = [], [], [], []
    for t, box in enumerate(boxes):
        c00, c10, c01, c11 = values[4 * t : 4 * t + 4]
        local = [amplitude * c for c in [c00, c10 - c00, c01 - c00, c00 - c10 - c01 + c11]]
        a, u1, b, v1 = box
        du, dv = u1 - a, v1 - b
        g = [
            local[0] - a * local[1] / du - b * local[2] / dv + a * b * local[3] / (du * dv),
            local[1] / du - b * local[3] / (du * dv),
            local[2] / dv - a * local[3] / (du * dv),
            local[3] / (du * dv),
        ]
        local_coefficients.extend(local)
        global_coefficients.extend(g)
        weight = amplitude * _area(box)
        for pu, pv in ((0, 0), (1, 0), (0, 1), (1, 1)):
            raw_u = [F(1)] if pu == 0 else [F(0), F(1)]
            raw_v = [F(1)] if pv == 0 else [F(0), F(1)]
            local_u = [F(1)] if pu == 0 else [-a / du, 1 / du]
            local_v = [F(1)] if pv == 0 else [-b / dv, 1 / dv]
            raw_moments.append(_physical_integral(g, box, raw_u, raw_v))
            local_moments.append(_physical_integral(g, box, local_u, local_v) / weight)
        minima.append(amplitude * min(values[4 * t : 4 * t + 4]))
        maxima.append(amplitude * max(values[4 * t : 4 * t + 4]))
    return _detach(
        {
            "local_coefficients": local_coefficients,
            "global_coefficients": global_coefficients,
            "local_moments": local_moments,
            "raw_moments": raw_moments,
            "minima": minima,
            "maxima": maxima,
        }
    )


def inspect_kernel(probe, tiles, coefficients):
    """Inspect actual raw kernels, including partial or empty tile collections."""
    _native(probe)
    _native(tiles)
    _native(coefficients)
    _rectangle_shape(probe)
    _require(type(tiles) is list and len(tiles) <= 256, "kernel tile cap")
    for tile in tiles:
        _rectangle_shape(tile)
    _require(type(coefficients) is list and len(coefficients) <= 64, "kernel row cap")
    _matrix_shape(coefficients, len(coefficients), 4 * len(tiles))
    rectangle = _vector(probe)
    boxes = [_vector(tile) for tile in tiles]
    rows = _matrix(coefficients)
    _require(_positive(rectangle), "positive kernel probe")
    _require(all(_inside(box, rectangle) for box in boxes), "kernel tile containment")
    for i, box in enumerate(boxes):
        _require(all(not _overlap(box, other) for other in boxes[i + 1 :]), "kernel tiles overlap")
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
    for row in rows:
        corners, integrals, bernstein, upper, minima, maxima, classes = ([] for _ in range(7))
        for t, box in enumerate(boxes):
            a, u1, b, v1 = box
            du, dv = u1 - a, v1 - b
            g = row[4 * t : 4 * t + 4]
            values = [_dot(g, [F(1), u, v, u * v]) for u, v in ((a, b), (u1, b), (a, v1), (u1, v1))]
            integral = _physical_integral(g, box, [F(1)], [F(1)])
            basis_u = ([u1 / du, -1 / du], [-a / du, 1 / du])
            basis_v = ([v1 / dv, -1 / dv], [-b / dv, 1 / dv])
            basis_integrals = [
                _physical_integral(g, box, basis_u[i], basis_v[j])
                for i, j in ((0, 0), (1, 0), (0, 1), (1, 1))
            ]
            h = _area(box)
            lo, hi = min(values), max(values)
            bound = h * max(abs(lo), abs(hi))
            _require(integral == h * sum(values, F(0)) / 4, "kernel corner integral identity")
            _require(sum(basis_integrals, F(0)) == integral, "kernel basis partition identity")
            _require(abs(integral) <= bound, "kernel corner envelope")
            _require(
                all(lo * h / 4 <= x <= hi * h / 4 for x in basis_integrals),
                "nonnegative basis integral envelope",
            )
            if lo == hi == 0:
                kind = "zero"
            elif lo >= 0:
                kind = "nonnegative"
            elif hi <= 0:
                kind = "nonpositive"
            else:
                kind = "mixed"
            corners.append(values)
            integrals.append(integral)
            bernstein.extend(basis_integrals)
            upper.append(bound)
            minima.append(lo)
            maxima.append(hi)
            classes.append(kind)
        for key, value in zip(
            out, (corners, integrals, bernstein, upper, minima, maxima, classes), strict=True
        ):
            out[key].append(value)
    return _detach(out)


def _comparison(upper, lower, domain):
    available = set(domain)
    gap = [upper[i] - lower[i] if i in available else None for i in range(len(upper))]
    _require(all(gap[i] >= 0 for i in domain), "bound comparison order")
    strict = [i for i in domain if gap[i] > 0]
    tied = [i for i in domain if gap[i] == 0]
    unavailable = [i for i in range(len(upper)) if i not in available]
    maximum, rows = _maximum(gap, domain)
    _require(
        sorted(strict + tied + unavailable) == list(range(len(upper))),
        "complete comparison partition",
    )
    return {
        "gain_gap": gap,
        "strict_rows": strict,
        "tied_rows": tied,
        "unavailable_rows": unavailable,
        "max_gap": maximum,
        "max_gap_rows": rows,
    }


def _level(problem, probe, tiles, B, G, D, scales, defined, undefined):
    """Recompute only the common level record, never a prior family executor."""
    q, r = len(G), 4 * len(tiles)
    V = _area(probe)
    _require(
        all(all(x == 0 for x in G[i]) for i in undefined),
        "null-cell target requires zero raw geometric row",
    )
    K = _mm(D, B, r)
    residual = _subtract(K, G)
    _require(_zero(residual), "frozen bank identity")
    kernel_wire = inspect_kernel(
        problem["probe"], [tile["bounds"] for tile in problem["tiles"]], problem["geometric"]
    )
    corners = [[_vector(v) for v in row] for row in kernel_wire["corner_values"]]
    integrals = _matrix(kernel_wire["tile_integrals"])
    bernstein = _matrix(kernel_wire["bernstein_integrals"])
    upper = _matrix(kernel_wire["tile_abs_upper"])
    classes = kernel_wire["tile_classes"]
    amplitude = V * V
    J = [[amplitude * x for x in row] for row in bernstein]
    A = [
        None if not scale else [x / scale for x in row]
        for row, scale in zip(J, scales, strict=True)
    ]
    C, L, U, exact = ([None] * q for _ in range(4))
    statuses, obstructions = [], []
    certified, uncertified = [], []
    for i in range(q):
        mixed = [
            {
                "tile": j,
                "positive_corner": next(a for a, v in enumerate(values) if v > 0),
                "negative_corner": next(a for a, v in enumerate(values) if v < 0),
            }
            for j, values in enumerate(corners[i])
            if classes[i][j] == "mixed"
        ]
        obstructions.append(mixed)
        if not scales[i]:
            statuses.append("undefined")
            _require(
                not mixed and all(kind == "zero" for kind in classes[i]),
                "undefined kernel must be zero",
            )
            continue
        C[i] = amplitude * sum(map(abs, integrals[i]), F(0)) / scales[i]
        L[i] = sum(map(abs, A[i]), F(0))
        U[i] = amplitude * sum(upper[i], F(0)) / scales[i]
        _require(0 <= C[i] <= L[i] <= U[i], "kernel bound order")
        if mixed:
            statuses.append("uncertified")
            uncertified.append(i)
        else:
            statuses.append("certified")
            certified.append(i)
            _require(C[i] == L[i], "sign-definite exactness")
            exact[i] = C[i]
            for values, integral in zip(corners[i], integrals[i], strict=True):
                sign = _sign(integral)
                _require(
                    all(sign * v == abs(v) for v in values),
                    "tile constant aligns with the kernel sign",
                )
    _require(
        sorted(certified + uncertified + undefined) == list(range(q)),
        "complete certification partition",
    )
    nonnegative = [i for i in defined if all(v >= 0 for values in corners[i] for v in values)]
    nonpositive = [i for i in defined if all(v <= 0 for values in corners[i] for v in values)]
    zero = [i for i in defined if all(v == 0 for values in corners[i] for v in values)]
    integrated_nonnegative = [i for i in defined if all(v >= 0 for v in A[i])]
    integrated_nonpositive = [i for i in defined if all(v <= 0 for v in A[i])]
    integrated_zero = [i for i in defined if all(v == 0 for v in A[i])]
    integrated_mixed = [i for i in integrated_nonnegative if i in uncertified]
    _require(set(nonnegative) & set(nonpositive) == set(zero), "pointwise sign intersection")
    _require(
        set(integrated_nonnegative) & set(integrated_nonpositive) == set(integrated_zero),
        "integrated sign intersection",
    )
    _require(zero == integrated_zero, "bilinear basis separates a zero kernel")
    certification = {
        "status": statuses,
        "mixed_obstructions": obstructions,
        "certified_rows": certified,
        "uncertified_rows": uncertified,
        "undefined_rows": undefined,
        "nonnegative_rows": nonnegative,
        "nonpositive_rows": nonpositive,
        "zero_rows": zero,
        "integrated_nonnegative_rows": integrated_nonnegative,
        "integrated_nonpositive_rows": integrated_nonpositive,
        "integrated_zero_rows": integrated_zero,
        "integrated_nonnegative_mixed_rows": integrated_mixed,
    }
    maxima = {}
    for key, values, domain in (
        ("constant_lower", C, defined),
        ("bilinear_lower", L, defined),
        ("corner_upper", U, defined),
        ("certified_gain", exact, certified),
    ):
        gain, rows = _maximum(values, domain)
        maxima[key] = {"gain": gain, "rows": rows}
    bounds = {
        "constant_lower": C,
        "bilinear_lower": L,
        "corner_upper": U,
        "certified_gain": exact,
        "maxima": maxima,
    }
    maps = {
        "decoder_bank": K,
        "bank_residual": residual,
        "raw_bilinear_target": J,
        "normalized_bilinear_target": A,
    }

    return _detach(
        {"kernels": kernel_wire, "maps": maps, "bounds": bounds, "certification": certification}
    )


def _restriction_blocks(parent_boxes, child_boxes, lineage):
    blocks = []
    for child, parent in zip(child_boxes, lineage, strict=True):
        a, u1, b, v1 = parent_boxes[parent]
        du, dv = u1 - a, v1 - b
        block = []
        for u, v in (
            (child[0], child[2]),
            (child[1], child[2]),
            (child[0], child[3]),
            (child[1], child[3]),
        ):
            x, y = (u - a) / du, (v - b) / dv
            row = [(1 - x) * (1 - y), x * (1 - y), (1 - x) * y, x * y]
            _require(all(v >= 0 for v in row) and sum(row, F(0)) == 1, "convex corner restriction")
            block.append(row)
        blocks.append(block)
    return blocks


def _moment_blocks(amplitude, boxes):
    """Independently integrate each box's own physical corner basis."""
    answer = []
    for a, u1, b, v1 in boxes:
        du, dv = u1 - a, v1 - b
        bu = ([u1 / du, -1 / du], [-a / du, 1 / du])
        bv = ([v1 / dv, -1 / dv], [-b / dv, 1 / dv])
        columns = []
        for i, j in ((0, 0), (1, 0), (0, 1), (1, 1)):
            g = [amplitude * bu[i][pu] * bv[j][pv] for pu, pv in ((0, 0), (1, 0), (0, 1), (1, 1))]
            column = []
            for pu, pv in ((0, 0), (1, 0), (0, 1), (1, 1)):
                utest = [F(1)] if pu == 0 else [F(0), F(1)]
                vtest = [F(1)] if pv == 0 else [F(0), F(1)]
                column.append(_physical_integral(g, [a, u1, b, v1], utest, vtest))
            columns.append(column)
        answer.append([list(row) for row in zip(*columns, strict=True)])
    return answer


def _aggregate_vector(values, lineage, parents):
    answer = [F(0)] * (4 * parents)
    for child, parent in enumerate(lineage):
        for basis in range(4):
            answer[4 * parent + basis] += values[4 * child + basis]
    return answer


def _aggregate_integrals(rows, lineage, parents):
    answer = []
    for row in rows:
        aggregated = [F(0)] * parents
        for child, parent in enumerate(lineage):
            aggregated[parent] += row[child]
        answer.append(aggregated)
    return answer


def _restrict_rows(rows, blocks, lineage, parents):
    answer = []
    for row in rows:
        if row is None:
            answer.append(None)
            continue
        aggregated = [F(0)] * (4 * parents)
        for child, (parent, block) in enumerate(zip(lineage, blocks, strict=True)):
            values = row[4 * child : 4 * child + 4]
            for basis, column in enumerate(zip(*block, strict=True)):
                aggregated[4 * parent + basis] += _dot(values, column)
        answer.append(aggregated)
    return answer


def _restrict_corners(corners, blocks, lineage):
    return [
        value
        for parent, block in zip(lineage, blocks, strict=True)
        for value in _linear(block, corners[4 * parent : 4 * parent + 4])
    ]


def _nullable_matrix(rows):
    return [None if row is None else _vector(row) for row in rows]


def _nullable_residual(left, right):
    result = []
    for a, b in zip(left, right, strict=True):
        _require((a is None) == (b is None), "transport normalization domain")
        result.append(None if a is None else [x - y for x, y in zip(a, b, strict=True)])
    return result


def _zero_nullable(rows):
    return all(row is None or all(x == 0 for x in row) for row in rows)


def _pipeline_context(problem, level, scales, amplitude):
    return {
        "problem": problem,
        "tiles": [x["bounds"] for x in problem["tiles"]],
        "scales": scales,
        "amplitude": amplitude,
        "J": _matrix(level["maps"]["raw_bilinear_target"]),
        "A": _nullable_matrix(level["maps"]["normalized_bilinear_target"]),
        "L": [None if x is None else _fraction(x) for x in level["bounds"]["bilinear_lower"]],
        "U": [None if x is None else _fraction(x) for x in level["bounds"]["corner_upper"]],
    }


def _pipeline(corners, context):
    _require(all(abs(x) <= 1 for x in corners), "bounded pipeline corners")
    p = context["problem"]
    integrated = integrate(p["probe"], context["tiles"], _encode(corners))
    bank_wire = integrated["raw_moments"]
    observed_wire = produce(p["interface"], bank_wire)
    direct_wire = produce(p["geometric"], bank_wire)
    decoded_wire = apply(p["decoder"], observed_wire)
    bank, observed = _vector(bank_wire), _vector(observed_wire)
    direct, decoded = _vector(direct_wire), _vector(decoded_wire)
    _require(decoded == direct == _linear(context["J"], corners), "actual field response pipeline")
    normalized = _normalized(decoded, context["scales"])
    for i, scale in enumerate(context["scales"]):
        if scale:
            _require(
                normalized[i] == _dot(context["A"][i], corners), "pipeline normalized moment map"
            )
            _require(
                abs(normalized[i]) <= context["L"][i] <= context["U"][i],
                "pipeline field-response bounds",
            )
    minima, maxima = _vector(integrated["minima"]), _vector(integrated["maxima"])
    _require(
        all(
            -context["amplitude"] <= lo <= hi <= context["amplitude"]
            for lo, hi in zip(minima, maxima, strict=True)
        ),
        "actual pipeline field bound",
    )
    return {
        "corners": corners,
        "global_coefficients": _vector(integrated["global_coefficients"]),
        "bank_error": bank,
        "observed_error": observed,
        "direct_error": direct,
        "decoded_error": decoded,
        "normalized_error": normalized,
        "tile_minima": minima,
        "tile_maxima": maxima,
    }


def _paired_pipeline(corners, parent_context, child_context, blocks, lineage, parents):
    parent = _pipeline(corners, parent_context)
    child_corners = _restrict_corners(corners, blocks, lineage)
    child = _pipeline(child_corners, child_context)
    aggregated = _aggregate_vector(child["bank_error"], lineage, parents)
    out = {
        "parent": parent,
        "child": child,
        "aggregated_bank_error": aggregated,
        "bank_residual": [a - b for a, b in zip(aggregated, parent["bank_error"], strict=True)],
    }
    for key in ("observed", "direct", "decoded"):
        field = key + "_error"
        out[key + "_residual"] = [a - b for a, b in zip(child[field], parent[field], strict=True)]
    out["normalized_residual"] = [
        None if a is None else a - b
        for a, b in zip(child["normalized_error"], parent["normalized_error"], strict=True)
    ]
    out["field_coefficient_residual"] = [
        child["global_coefficients"][4 * j + basis]
        - parent["global_coefficients"][4 * owner + basis]
        for j, owner in enumerate(lineage)
        for basis in range(4)
    ]
    for key, value in out.items():
        if key.endswith("_residual"):
            _require(all(x is None or x == 0 for x in value), "paired field transport: " + key)
    return out


def build_family(input):
    """Refine only representation, preserving the supplied response functional."""
    _native(input)
    _fields(input, ("parent", "children"))
    parent = input["parent"]
    _, parent_records, _, _, _, _, _, _ = _problem_shape(parent)
    children = input["children"]
    _require(type(children) is list and 1 <= len(children) <= 256, "child tile inventory cap")
    for child in children:
        _fields(child, ("parent", "bounds"))
        _require(
            type(child["parent"]) is int and 0 <= child["parent"] < len(parent_records),
            "child parent index",
        )
        _rectangle_shape(child["bounds"])
    # No Fraction has been constructed until BOTH structural passes complete.
    probe, cells, parent_boxes, B, G, D, targets, q, rp, s, p = _problem(parent)
    child_boxes = [_vector(child["bounds"]) for child in children]
    lineage = [child["parent"] for child in children]
    m, rc = len(children), 4 * len(children)
    # Every parent and child scalar is now admitted, before geometric work.
    V, cell_volumes, parent_volumes, scales, defined, undefined = _geometry(
        parent, probe, cells, parent_boxes, targets
    )
    for owner, box in enumerate(parent_boxes):
        _partition(
            [child for child, index in zip(child_boxes, lineage, strict=True) if index == owner],
            box,
        )
    child_volumes = list(map(_area, child_boxes))
    child_problem = _detach(parent)
    child_problem["tiles"] = [
        {"event": parent_records[index]["event"], "bounds": _encode(box)}
        for index, box in zip(lineage, child_boxes, strict=True)
    ]
    child_problem["bank_labels"] = [
        {"tile": j, "basis": basis} for j in range(m) for basis in range(4)
    ]
    Bc = [[x for index in lineage for x in row[4 * index : 4 * index + 4]] for row in B]
    Gc = [[x for index in lineage for x in row[4 * index : 4 * index + 4]] for row in G]
    child_problem["interface"], child_problem["geometric"] = _encode(Bc), _encode(Gc)
    for j, index in enumerate(lineage):
        _require(
            child_problem["tiles"][j]["event"] == parent_records[index]["event"],
            "inherited event identity",
        )
        _require(
            all(
                row[4 * j : 4 * j + 4] == source[4 * index : 4 * index + 4]
                for row, source in zip(Gc, G, strict=True)
            ),
            "physical kernel identity",
        )
    _require(child_problem["decoder"] == parent["decoder"], "unchanged receiver decoder")
    amplitude = V * V
    E = _restriction_blocks(parent_boxes, child_boxes, lineage)
    Pp, Pc = _moment_blocks(amplitude, parent_boxes), _moment_blocks(amplitude, child_boxes)
    aggregated_P = [[[F(0)] * 4 for _ in range(4)] for _ in range(p)]
    for owner, block, restriction in zip(lineage, Pc, E, strict=True):
        values = _mm(block, restriction)
        for i in range(4):
            for j in range(4):
                aggregated_P[owner][i][j] += values[i][j]
    moment_residual = [_subtract(a, b) for a, b in zip(aggregated_P, Pp, strict=True)]
    _require(all(_zero(block) for block in moment_residual), "raw basis moment additivity")
    restriction = {
        "blocks": E,
        "parent_moment_blocks": Pp,
        "child_moment_blocks": Pc,
        "aggregated_moment_blocks": aggregated_P,
        "moment_residuals": moment_residual,
        "row_sums": [[sum(row, F(0)) for row in block] for block in E],
        "min_weights": [min(x for row in block for x in row) for block in E],
        "max_weights": [max(x for row in block for x in row) for block in E],
    }
    _encode(restriction)
    parent_level = _level(parent, probe, parent_boxes, B, G, D, scales, defined, undefined)
    child_level = _level(child_problem, probe, child_boxes, Bc, Gc, D, scales, defined, undefined)
    for i in range(q):
        for child, owner in enumerate(lineage):
            pc = _vector(parent_level["kernels"]["corner_values"][i][owner])
            cc = _vector(child_level["kernels"]["corner_values"][i][child])
            _require(_linear(E[child], pc) == cc, "actual child kernel corner restriction")
            if parent_level["kernels"]["tile_classes"][i][owner] != "mixed":
                _require(
                    child_level["kernels"]["tile_classes"][i][child] != "mixed",
                    "sign-definite tile restriction",
                )
    parent_integrals = _matrix(parent_level["kernels"]["tile_integrals"])
    parent_bernstein = _matrix(parent_level["kernels"]["bernstein_integrals"])
    agg_integrals = _aggregate_integrals(
        _matrix(child_level["kernels"]["tile_integrals"]), lineage, p
    )
    agg_bernstein = _restrict_rows(
        _matrix(child_level["kernels"]["bernstein_integrals"]), E, lineage, p
    )
    restricted_J = _restrict_rows(
        _matrix(child_level["maps"]["raw_bilinear_target"]), E, lineage, p
    )
    restricted_A = _restrict_rows(
        _nullable_matrix(child_level["maps"]["normalized_bilinear_target"]), E, lineage, p
    )
    transport = {
        "aggregate_kernel_integrals": agg_integrals,
        "aggregate_bernstein_integrals": agg_bernstein,
        "kernel_integral_residuals": _subtract(agg_integrals, parent_integrals),
        "bernstein_residuals": _subtract(agg_bernstein, parent_bernstein),
        "restricted_raw_target": restricted_J,
        "raw_target_residuals": _subtract(
            restricted_J, _matrix(parent_level["maps"]["raw_bilinear_target"])
        ),
        "restricted_normalized_target": restricted_A,
        "normalized_target_residuals": _nullable_residual(
            restricted_A, _nullable_matrix(parent_level["maps"]["normalized_bilinear_target"])
        ),
    }
    for key, value in transport.items():
        if key.endswith("_residuals"):
            _require(_zero_nullable(value), "complete additive transport: " + key)
    parent_bounds = {
        k: [None if x is None else _fraction(x) for x in parent_level["bounds"][k]]
        for k in ("constant_lower", "bilinear_lower", "corner_upper", "certified_gain")
    }
    child_bounds = {
        k: [None if x is None else _fraction(x) for x in child_level["bounds"][k]]
        for k in parent_bounds
    }
    comparison = {
        "constant_increase": _comparison(
            child_bounds["constant_lower"], parent_bounds["constant_lower"], defined
        ),
        "bilinear_increase": _comparison(
            child_bounds["bilinear_lower"], parent_bounds["bilinear_lower"], defined
        ),
        "upper_decrease": _comparison(
            parent_bounds["corner_upper"], child_bounds["corner_upper"], defined
        ),
    }
    inherited = parent_level["certification"]["certified_rows"]
    child_certified = child_level["certification"]["certified_rows"]
    _require(set(inherited) <= set(child_certified), "certification cannot be lost")
    newly = [i for i in child_certified if i not in inherited]
    still = child_level["certification"]["uncertified_rows"]
    residual = [
        child_bounds["certified_gain"][i] - parent_bounds["certified_gain"][i]
        if i in inherited
        else None
        for i in range(q)
    ]
    _require(all(x is None or x == 0 for x in residual), "inherited exact gain")
    _require(
        sorted(inherited + newly + still + undefined) == list(range(q)),
        "certificate bridge partition",
    )
    cert_bridge = {
        "inherited_rows": inherited,
        "newly_certified_rows": newly,
        "still_uncertified_rows": still,
        "undefined_rows": undefined,
        "inherited_gain_residuals": residual,
    }
    geometry = {
        "volume": V,
        "cell_volumes": cell_volumes,
        "target_scales": scales,
        "defined_rows": defined,
        "undefined_rows": undefined,
        "parent_tile_volumes": parent_volumes,
        "child_tile_volumes": child_volumes,
        "child_parents": lineage,
    }
    _encode(
        {
            "transport": transport,
            "comparison": comparison,
            "geometry": geometry,
            "certification_bridge": cert_bridge,
        }
    )
    pctx = _pipeline_context(parent, parent_level, scales, amplitude)
    cctx = _pipeline_context(child_problem, child_level, scales, amplitude)

    def pair(c):
        return _paired_pipeline(c, pctx, cctx, E, lineage, p)

    pattern = [v for _ in range(p) for v in (F(-1), F(0), F(1), F(1, 2))]
    witnesses = {
        "parent_pattern": {"positive": pair(pattern), "negative": pair([-v for v in pattern])},
        "parent_constant": {"positive": pair([F(1)] * rp), "negative": pair([F(-1)] * rp)},
    }
    for side, direction in (("positive", 1), ("negative", -1)):
        record = witnesses["parent_constant"][side]
        for level, context in (("parent", pctx), ("child", cctx)):
            _require(
                all(v == direction for v in record[level]["corners"]), "constant field restriction"
            )
            _require(
                record[level]["global_coefficients"]
                == [
                    value
                    for _ in context["tiles"]
                    for value in (direction * amplitude, F(0), F(0), F(0))
                ],
                "actual constant amplitude",
            )
            for i in defined:
                _require(
                    record[level]["normalized_error"][i] == direction * sum(context["A"][i], F(0)),
                    "constant response",
                )
    sign_entries = 0
    for level_name, level, context in (
        ("parent", parent_level, pctx),
        ("child", child_level, cctx),
    ):
        for class_name, bound_key in (
            ("constant", "constant_lower"),
            ("bilinear", "bilinear_lower"),
        ):
            key = level_name + "_" + class_name + "_maximizer"
            if not defined:
                witnesses[key] = None
                continue
            index = level["bounds"]["maxima"][bound_key]["rows"][0]
            gain = _fraction(level["bounds"][bound_key][index])
            raw = (
                level["kernels"]["tile_integrals"][index]
                if class_name == "constant"
                else level["maps"]["normalized_bilinear_target"][index]
            )
            signs = [_sign(_fraction(x)) for x in raw]
            sign_entries += len(signs)
            corners = [F(x) for x in signs for _ in range(4 if class_name == "constant" else 1)]
            record = {"target_row": index, "signs": signs}
            for side, direction in (("positive", 1), ("negative", -1)):
                values = [direction * v for v in corners]
                endpoint = pair(values) if level_name == "parent" else _pipeline(values, context)
                attained = (
                    endpoint["parent"]["normalized_error"][index]
                    if level_name == "parent"
                    else endpoint["normalized_error"][index]
                )
                _require(attained == direction * gain, "canonical maximum attainment")
                record[side] = endpoint
            witnesses[key] = record
    d, zp, zc = len(defined), len(inherited), len(child_certified)
    a = sum(cell is not None for cell in cells)
    paired_count, child_count = (8, 4) if d else (4, 0)
    ep, ec = 3 * rp + s + 2 * q + d + 2 * p, 3 * rc + s + 2 * q + d + 2 * m
    e_pair = ep + ec + 2 * rp + s + 2 * q + d + rc
    counts = {
        "cells": len(cells),
        "positive_cells": a,
        "parent_tiles": p,
        "child_tiles": m,
        "parent_bank_values": rp,
        "child_bank_values": rc,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": d,
        "undefined_rows": len(undefined),
        "input_geometry_entries": 4 + 4 * a + 4 * p + 4 * m,
        "input_matrix_entries": s * rp + q * rp + q * s,
        "child_problem_geometry_entries": 4 + 4 * a + 4 * m,
        "child_problem_matrix_entries": s * rc + q * rc + q * s,
        "geometry_entries": 1 + len(cells) + q + p + m,
        "restriction_entries": 38 * m + 48 * p,
        "parent_kernel_entries": 12 * q * p,
        "child_kernel_entries": 12 * q * m,
        "parent_map_entries": (3 * q + d) * rp,
        "child_map_entries": (3 * q + d) * rc,
        "bound_entries": sum(3 * d + z + (3 if d else 0) + (1 if z else 0) for z in (zp, zc)),
        "certification_bridge_entries": zp,
        "transport_entries": 2 * q * p + 4 * q * rp + 2 * d * rp,
        "comparison_entries": 3 * d + (3 if d else 0),
        "parent_paired_witnesses": paired_count,
        "child_witnesses": child_count,
        "sign_entries": sign_entries,
        "witness_entries": paired_count * e_pair + child_count * ec,
        "constant_strict": len(comparison["constant_increase"]["strict_rows"]),
        "bilinear_strict": len(comparison["bilinear_increase"]["strict_rows"]),
        "upper_strict": len(comparison["upper_decrease"]["strict_rows"]),
        "inherited_rows": zp,
        "newly_certified_rows": len(newly),
        "still_uncertified_rows": len(still),
    }
    checks = {
        key: True
        for key in (
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
    }
    return _detach(
        {
            "input": input,
            "child_problem": child_problem,
            "geometry": geometry,
            "restriction": restriction,
            "levels": {"parent": parent_level, "child": child_level},
            "transport": transport,
            "comparison": comparison,
            "certification_bridge": cert_bridge,
            "witnesses": witnesses,
            "checks": checks,
            "counts": counts,
        }
    )
