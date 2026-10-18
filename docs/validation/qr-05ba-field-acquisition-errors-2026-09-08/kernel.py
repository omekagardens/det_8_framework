"""Exact Cartesian field-plus-acquisition response-error certificates."""

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


def _aggregate_vector(values, lineage, parents):
    answer = [F(0)] * (4 * parents)
    for child, parent in enumerate(lineage):
        for basis in range(4):
            answer[4 * parent + basis] += values[4 * child + basis]
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


def _admit(input):
    _native(input)
    _fields(input, ("refinement", "receiver_radii", "budgets"))
    refinement = input["refinement"]
    _fields(refinement, ("parent", "children"))
    parent, children = refinement["parent"], refinement["children"]
    _, parent_records, _, _, _q, _rp, s, p = _problem_shape(parent)
    _require(type(children) is list and 1 <= len(children) <= 256, "child tile inventory cap")
    for child in children:
        _fields(child, ("parent", "bounds"))
        _require(type(child["parent"]) is int and 0 <= child["parent"] < p, "child parent index")
        _rectangle_shape(child["bounds"])
    _vector_shape(input["receiver_radii"], s)
    budgets = input["budgets"]
    _require(type(budgets) is list and 1 <= len(budgets) <= 8, "budget inventory cap")
    names = set()
    for budget in budgets:
        _fields(budget, ("name", "field", "acquisition"))
        name = budget["name"]
        _require(type(name) is str and name and name not in names, "unique native budget names")
        names.add(name)
        _pair_shape(budget["field"])
        _pair_shape(budget["acquisition"])
    # Every nested shape and index across all three inputs is now checked.
    parsed = _problem(parent)
    child_boxes = [_vector(child["bounds"]) for child in children]
    rho = _vector(input["receiver_radii"])
    parameters = [
        (_fraction(budget["field"]), _fraction(budget["acquisition"])) for budget in budgets
    ]
    _require(all(x >= 0 for x in rho), "nonnegative receiver radii")
    _require(all(epsilon >= 0 and eta >= 0 for epsilon, eta in parameters), "nonnegative budgets")
    return parsed, child_boxes, rho, parameters, parent_records


def _field_evidence(input, parsed, child_boxes, parent_records):
    parent = input["refinement"]["parent"]
    children = input["refinement"]["children"]
    probe, cells, parent_boxes, B, G, D, targets, q, _rp, _s, p = parsed
    lineage = [child["parent"] for child in children]
    m = len(children)
    V, cv, pv, scales, defined, undefined = _geometry(parent, probe, cells, parent_boxes, targets)
    for owner, box in enumerate(parent_boxes):
        _partition(
            [child for child, index in zip(child_boxes, lineage, strict=True) if index == owner],
            box,
        )
    child_problem = _detach(parent)
    child_problem["tiles"] = [
        {"event": parent_records[index]["event"], "bounds": _encode(box)}
        for index, box in zip(lineage, child_boxes, strict=True)
    ]
    child_problem["bank_labels"] = [{"tile": j, "basis": a} for j in range(m) for a in range(4)]
    Bc = [[x for owner in lineage for x in row[4 * owner : 4 * owner + 4]] for row in B]
    Gc = [[x for owner in lineage for x in row[4 * owner : 4 * owner + 4]] for row in G]
    child_problem["interface"], child_problem["geometric"] = _encode(Bc), _encode(Gc)
    _require(child_problem["decoder"] == parent["decoder"], "same receiver decoder")
    for j, owner in enumerate(lineage):
        _require(
            child_problem["tiles"][j]["event"] == parent_records[owner]["event"], "event lineage"
        )
        for derived, original in ((Bc, B), (Gc, G)):
            _require(
                all(
                    a[4 * j : 4 * j + 4] == b[4 * owner : 4 * owner + 4]
                    for a, b in zip(derived, original, strict=True)
                ),
                "raw global block lineage",
            )
    E = _restriction_blocks(parent_boxes, child_boxes, lineage)
    lp = _level(parent, probe, parent_boxes, B, G, D, scales, defined, undefined)
    lc = _level(child_problem, probe, child_boxes, Bc, Gc, D, scales, defined, undefined)
    for i in range(q):
        for j, owner in enumerate(lineage):
            pc = _vector(lp["kernels"]["corner_values"][i][owner])
            cc = _vector(lc["kernels"]["corner_values"][i][j])
            _require(_linear(E[j], pc) == cc, "same restricted physical kernel")
            if lp["kernels"]["tile_classes"][i][owner] != "mixed":
                _require(lc["kernels"]["tile_classes"][i][j] != "mixed", "kernel sign inheritance")
    for key in ("raw_bilinear_target", "normalized_bilinear_target"):
        pr = _nullable_matrix(lp["maps"][key])
        cr = _nullable_matrix(lc["maps"][key])
        restricted = _restrict_rows(cr, E, lineage, p)
        _require(
            _zero_nullable(_nullable_residual(restricted, pr)), "independent response transport"
        )
    fp = _bound_values(lp["bounds"])
    fc = _bound_values(lc["bounds"])
    for i in defined:
        _require(
            fp["constant_lower"][i] <= fc["constant_lower"][i]
            and fp["bilinear_lower"][i] <= fc["bilinear_lower"][i]
            and fp["corner_upper"][i] >= fc["corner_upper"][i],
            "field refinement bounds",
        )
    inherited = lp["certification"]["certified_rows"]
    _require(
        set(inherited) <= set(lc["certification"]["certified_rows"]),
        "field certification inherited",
    )
    _require(
        all(fp["certified_gain"][i] == fc["certified_gain"][i] for i in inherited),
        "inherited physical exact gain",
    )
    geometry = {
        "volume": V,
        "cell_volumes": cv,
        "target_scales": scales,
        "defined_rows": defined,
        "undefined_rows": undefined,
        "parent_tile_volumes": pv,
        "child_tile_volumes": list(map(_area, child_boxes)),
        "child_parents": lineage,
    }
    field = {
        "child_problem": child_problem,
        "geometry": geometry,
        "restriction_blocks": E,
        "levels": {"parent": lp, "child": lc},
    }
    _encode(field)
    return field, scales, defined, undefined, fp, fc


def _bound_values(bounds, exact_key="certified_gain"):
    return {
        key: [None if x is None else _fraction(x) for x in bounds[key]]
        for key in ("constant_lower", "bilinear_lower", "corner_upper", exact_key)
    }


def _case_level(field_bounds, epsilon, eta, gamma, defined, undefined):
    q = len(gamma)
    bounds = {
        key: [
            None if i not in defined else epsilon * field_bounds[key][i] + eta * gamma[i]
            for i in range(q)
        ]
        for key in ("constant_lower", "bilinear_lower", "corner_upper")
    }
    exact, reasons = [], []
    available, unavailable = [], []
    for i in range(q):
        if i in undefined:
            exact.append(None)
            reasons.append("undefined")
        elif epsilon == 0:
            exact.append(eta * gamma[i])
            reasons.append("zero_field_budget")
            available.append(i)
        elif field_bounds["certified_gain"][i] is not None:
            exact.append(epsilon * field_bounds["certified_gain"][i] + eta * gamma[i])
            reasons.append("field_certified")
            available.append(i)
        else:
            exact.append(None)
            reasons.append("unavailable")
            unavailable.append(i)
    bounds["exact_gain"] = exact
    maxima = {}
    for key, values in bounds.items():
        domain = available if key == "exact_gain" else defined
        gain, rows = _maximum(values, domain)
        maxima[key] = {"gain": gain, "rows": rows}
    bounds["maxima"] = maxima
    for i in defined:
        _require(
            0
            <= bounds["constant_lower"][i]
            <= bounds["bilinear_lower"][i]
            <= bounds["corner_upper"][i],
            "composed bound order",
        )
    _require(
        all(
            exact[i] == bounds["constant_lower"][i] == bounds["bilinear_lower"][i]
            for i in available
        ),
        "certified composed exactness",
    )
    _require(
        sorted(available + unavailable + undefined) == list(range(q)),
        "exact availability partition",
    )
    return {
        "bounds": bounds,
        "exactness": {
            "reason": reasons,
            "available_rows": available,
            "unavailable_rows": unavailable,
            "undefined_rows": undefined,
        },
    }


def _context(problem, level, scales, amplitude, rho, K, H):
    return {
        "problem": problem,
        "tiles": [tile["bounds"] for tile in problem["tiles"]],
        "scales": scales,
        "amplitude": amplitude,
        "rho": rho,
        "K": K,
        "K_wire": _encode(K),
        "H": H,
        "J": _matrix(level["maps"]["raw_bilinear_target"]),
        "A": _nullable_matrix(level["maps"]["normalized_bilinear_target"]),
    }


def _joint_pipeline(corners, coordinates, context, epsilon, eta, bounds):
    _require(all(abs(x) <= epsilon for x in corners), "field corner budget")
    _require(all(abs(x) <= eta for x in coordinates), "acquisition coordinate budget")
    p = context["problem"]
    integrated = integrate(p["probe"], context["tiles"], _encode(corners))
    bank_wire = integrated["raw_moments"]
    field_observed_wire = produce(p["interface"], bank_wire)
    field_direct_wire = produce(p["geometric"], bank_wire)
    acquisition_direct_wire = produce(context["K_wire"], _encode(coordinates))
    field_observed = _vector(field_observed_wire)
    noise = [radius * z for radius, z in zip(context["rho"], coordinates, strict=True)]
    total_observed = [a + b for a, b in zip(field_observed, noise, strict=True)]
    field_decoded = _vector(apply(p["decoder"], field_observed_wire))
    acquisition_decoded = _vector(apply(p["decoder"], _encode(noise)))
    total_decoded = _vector(apply(p["decoder"], _encode(total_observed)))
    field_direct = _vector(field_direct_wire)
    acquisition_direct = _vector(acquisition_direct_wire)
    total_direct = [a + b for a, b in zip(field_direct, acquisition_direct, strict=True)]
    _require(
        field_direct == field_decoded == _linear(context["J"], corners),
        "actual field component identity",
    )
    _require(
        acquisition_direct == acquisition_decoded == _linear(context["K"], coordinates),
        "actual acquisition component identity",
    )
    _require(
        total_direct
        == total_decoded
        == [a + b for a, b in zip(field_decoded, acquisition_decoded, strict=True)],
        "complete additive response identity",
    )
    normalized = _normalized(total_decoded, context["scales"])
    for i, scale in enumerate(context["scales"]):
        if scale:
            _require(
                normalized[i]
                == _dot(context["A"][i], corners) + _dot(context["H"][i], coordinates),
                "normalized joint response",
            )
            _require(
                abs(normalized[i]) <= bounds["bilinear_lower"][i] <= bounds["corner_upper"][i],
                "joint finite-class and envelope bound",
            )
    minima, maxima = _vector(integrated["minima"]), _vector(integrated["maxima"])
    _require(
        all(
            -epsilon * context["amplitude"] <= lo <= hi <= epsilon * context["amplitude"]
            for lo, hi in zip(minima, maxima, strict=True)
        ),
        "actual field amplitude budget",
    )
    _require(
        all(abs(n) <= eta * radius for n, radius in zip(noise, context["rho"], strict=True)),
        "actual receiver acquisition budget",
    )
    return {
        "corners": corners,
        "acquisition_coordinates": coordinates,
        "global_coefficients": _vector(integrated["global_coefficients"]),
        "bank_error": _vector(bank_wire),
        "field_observed_error": field_observed,
        "acquisition_error": noise,
        "total_observed_error": total_observed,
        "field_direct_error": field_direct,
        "field_decoded_error": field_decoded,
        "acquisition_direct_error": acquisition_direct,
        "acquisition_decoded_error": acquisition_decoded,
        "total_direct_error": total_direct,
        "total_decoded_error": total_decoded,
        "normalized_error": normalized,
        "tile_minima": minima,
        "tile_maxima": maxima,
    }


def _joint_pair(
    corners,
    coordinates,
    parent_context,
    child_context,
    epsilon,
    eta,
    parent_bounds,
    child_bounds,
    E,
    lineage,
    p,
):
    parent = _joint_pipeline(corners, coordinates, parent_context, epsilon, eta, parent_bounds)
    child = _joint_pipeline(
        _restrict_corners(corners, E, lineage),
        list(coordinates),
        child_context,
        epsilon,
        eta,
        child_bounds,
    )
    aggregated = _aggregate_vector(child["bank_error"], lineage, p)
    out = {
        "parent": parent,
        "child": child,
        "aggregated_bank_error": aggregated,
        "bank_residual": [a - b for a, b in zip(aggregated, parent["bank_error"], strict=True)],
    }
    for prefix, field in (
        ("field_observed", "field_observed_error"),
        ("acquisition", "acquisition_error"),
        ("total_observed", "total_observed_error"),
        ("field_direct", "field_direct_error"),
        ("field_decoded", "field_decoded_error"),
        ("acquisition_direct", "acquisition_direct_error"),
        ("acquisition_decoded", "acquisition_decoded_error"),
        ("total_direct", "total_direct_error"),
        ("total_decoded", "total_decoded_error"),
    ):
        out[prefix + "_residual"] = [
            a - b for a, b in zip(child[field], parent[field], strict=True)
        ]
    out["normalized_residual"] = [
        None if a is None else a - b
        for a, b in zip(child["normalized_error"], parent["normalized_error"], strict=True)
    ]
    out["field_coefficient_residual"] = [
        child["global_coefficients"][4 * j + b] - parent["global_coefficients"][4 * owner + b]
        for j, owner in enumerate(lineage)
        for b in range(4)
    ]
    _require(
        child["acquisition_coordinates"] == parent["acquisition_coordinates"]
        and child["acquisition_error"] == parent["acquisition_error"],
        "same acquisition perturbation",
    )
    for key, value in out.items():
        if key.endswith("_residual"):
            _require(all(x is None or x == 0 for x in value), "joint pair residual: " + key)
    return out


def _case_witnesses(
    budget, epsilon, eta, field, case_levels, parent_context, child_context, defined
):
    geometry = field["geometry"]
    lineage, E = geometry["child_parents"], field["restriction_blocks"]
    p, m, s = len(geometry["parent_tile_volumes"]), len(lineage), len(parent_context["rho"])
    rp = 4 * p

    def pair(c, z):
        return _joint_pair(
            c,
            z,
            parent_context,
            child_context,
            epsilon,
            eta,
            case_levels["parent"]["bounds"],
            case_levels["child"]["bounds"],
            E,
            lineage,
            p,
        )

    pattern = (F(-1), F(0), F(1), F(1, 2))
    patterns = [epsilon * x for _ in range(p) for x in pattern]
    zpattern = [eta * pattern[j % 4] for j in range(s)]
    witnesses = {
        "parent_pattern": {
            "positive": pair(patterns, zpattern),
            "negative": pair([-x for x in patterns], [-x for x in zpattern]),
        },
        "parent_constant": {
            "positive": pair([epsilon] * rp, [eta] * s),
            "negative": pair([-epsilon] * rp, [-eta] * s),
        },
    }
    for side, direction in (("positive", 1), ("negative", -1)):
        record = witnesses["parent_constant"][side]
        for name, context in (("parent", parent_context), ("child", child_context)):
            actual = record[name]
            _require(
                actual["corners"] == [direction * epsilon] * (4 * len(context["tiles"]))
                and actual["acquisition_coordinates"] == [direction * eta] * s,
                "constant controls",
            )
            _require(
                actual["global_coefficients"]
                == [
                    x
                    for _ in context["tiles"]
                    for x in (direction * epsilon * context["amplitude"], F(0), F(0), F(0))
                ],
                "actual constant physical field",
            )
            for i in defined:
                _require(
                    actual["normalized_error"][i]
                    == direction
                    * (epsilon * sum(context["A"][i], F(0)) + eta * sum(context["H"][i], F(0))),
                    "constant field-plus-acquisition response",
                )
    paired, standalone, sign_entries = 4, 0, 0
    for name, context in (("parent", parent_context), ("child", child_context)):
        level = case_levels[name]
        physical = field["levels"][name]
        t = p if name == "parent" else m
        for kind, key in (
            ("constant", "constant_lower"),
            ("bilinear", "bilinear_lower"),
            ("exact", "exact_gain"),
        ):
            group_key = name + "_" + kind + "_maximizer"
            rows = level["bounds"]["maxima"][key]["rows"]
            if not rows:
                witnesses[group_key] = None
                continue
            index = rows[0]
            field_values = (
                physical["maps"]["normalized_bilinear_target"][index]
                if kind == "bilinear"
                else physical["kernels"]["tile_integrals"][index]
            )
            field_signs = (
                [0] * (4 * t if kind == "bilinear" else t)
                if epsilon == 0
                else [_sign(_fraction(v)) for v in field_values]
            )
            if kind == "exact" and epsilon > 0:
                _require(
                    index in physical["certification"]["certified_rows"], "exact field sign witness"
                )
            acquisition_signs = [0] * s if eta == 0 else list(map(_sign, context["K"][index]))
            sign_entries += len(field_signs) + len(acquisition_signs)
            c = [epsilon * x for x in field_signs for _ in range(1 if kind == "bilinear" else 4)]
            z = [eta * x for x in acquisition_signs]
            group = {
                "target_row": index,
                "field_signs": field_signs,
                "acquisition_signs": acquisition_signs,
            }
            for side, direction in (("positive", 1), ("negative", -1)):
                cs, zs = [direction * x for x in c], [direction * x for x in z]
                endpoint = (
                    pair(cs, zs)
                    if name == "parent"
                    else _joint_pipeline(cs, zs, context, epsilon, eta, level["bounds"])
                )
                actual = endpoint["parent"] if name == "parent" else endpoint
                _require(
                    actual["normalized_error"][index] == direction * level["bounds"][key][index],
                    "designated joint maximum attainment",
                )
                group[side] = endpoint
            witnesses[group_key] = group
            if name == "parent":
                paired += 2
            else:
                standalone += 2
    return witnesses, paired, standalone, sign_entries


def build_family(input):
    """Compose independently admitted field and acquisition uncertainty sets."""
    parsed, child_boxes, rho, parameters, parent_records = _admit(input)
    field, scales, defined, undefined, fp, fc = _field_evidence(
        input, parsed, child_boxes, parent_records
    )
    parent = input["refinement"]["parent"]
    _probe, cells, _parent_boxes, _B, _G, D, _targets, q, rp, s, p = parsed
    m, rc, b = len(child_boxes), 4 * len(child_boxes), len(parameters)
    K = [[entry * radius for entry, radius in zip(row, rho, strict=True)] for row in D]
    H = [
        None if not scale else [v / scale for v in row]
        for row, scale in zip(K, scales, strict=True)
    ]
    gamma = [None if row is None else sum(map(abs, row), F(0)) for row in H]
    gain, rows = _maximum(gamma, defined)
    acquisition = {
        "raw_map": K,
        "normalized_map": H,
        "gain": gamma,
        "maxima": {"gain": gain, "rows": rows},
    }
    _encode(acquisition)
    amplitude = field["geometry"]["volume"] ** 2
    pc = _context(parent, field["levels"]["parent"], scales, amplitude, rho, K, H)
    cc = _context(field["child_problem"], field["levels"]["child"], scales, amplitude, rho, K, H)
    cases = []
    totals = {
        "parent_paired_witnesses": 0,
        "child_witnesses": 0,
        "sign_entries": 0,
        "witness_entries": 0,
        "case_bound_entries": 0,
        "case_exact_bridge_entries": 0,
        "constant_strict": 0,
        "bilinear_strict": 0,
        "upper_strict": 0,
        "inherited_exact_rows": 0,
        "newly_exact_rows": 0,
        "unavailable_exact_rows": 0,
    }
    d = len(defined)
    ep, ec = 3 * rp + 4 * s + 6 * q + d + 2 * p, 3 * rc + 4 * s + 6 * q + d + 2 * m
    e_pair = ep + ec + 2 * rp + 3 * s + 6 * q + d + rc
    for budget, (epsilon, eta) in zip(input["budgets"], parameters, strict=True):
        levels = {
            "parent": _case_level(fp, epsilon, eta, gamma, defined, undefined),
            "child": _case_level(fc, epsilon, eta, gamma, defined, undefined),
        }
        inherited = levels["parent"]["exactness"]["available_rows"]
        available_child = levels["child"]["exactness"]["available_rows"]
        _require(set(inherited) <= set(available_child), "composed exact availability inheritance")
        newly = [i for i in available_child if i not in inherited]
        unavailable = levels["child"]["exactness"]["unavailable_rows"]
        residual = [
            levels["child"]["bounds"]["exact_gain"][i] - levels["parent"]["bounds"]["exact_gain"][i]
            if i in inherited
            else None
            for i in range(q)
        ]
        _require(all(x is None or x == 0 for x in residual), "composed inherited exact gain")
        _require(
            sorted(inherited + newly + unavailable + undefined) == list(range(q)),
            "complete composed exact bridge",
        )
        bridge = {
            "inherited_rows": inherited,
            "newly_exact_rows": newly,
            "unavailable_rows": unavailable,
            "undefined_rows": undefined,
            "inherited_gain_residuals": residual,
        }
        pb, cb = levels["parent"]["bounds"], levels["child"]["bounds"]
        comparison = {
            "constant_increase": _comparison(cb["constant_lower"], pb["constant_lower"], defined),
            "bilinear_increase": _comparison(cb["bilinear_lower"], pb["bilinear_lower"], defined),
            "upper_decrease": _comparison(pb["corner_upper"], cb["corner_upper"], defined),
        }
        for name, key, direction in (
            ("constant_increase", "constant_lower", 1),
            ("bilinear_increase", "bilinear_lower", 1),
            ("upper_decrease", "corner_upper", -1),
        ):
            _require(
                all(
                    comparison[name]["gain_gap"][i]
                    == epsilon * direction * (fc[key][i] - fp[key][i])
                    for i in defined
                ),
                "acquisition cancels from refinement comparison",
            )
        _encode({"levels": levels, "comparison": comparison, "exact_bridge": bridge})
        witnesses, paired, standalone, signs = _case_witnesses(
            budget, epsilon, eta, field, levels, pc, cc, defined
        )
        zp, zc = len(inherited), len(available_child)
        expected_p, expected_c = 4 + 4 * bool(d) + 2 * bool(zp), 4 * bool(d) + 2 * bool(zc)
        _require((paired, standalone) == (expected_p, expected_c), "canonical pipeline inventory")
        _require(
            signs == bool(d) * (p + rp + m + rc + 4 * s) + bool(zp) * (p + s) + bool(zc) * (m + s),
            "maximum sign inventory",
        )
        totals["parent_paired_witnesses"] += paired
        totals["child_witnesses"] += standalone
        totals["sign_entries"] += signs
        totals["witness_entries"] += paired * e_pair + standalone * ec
        totals["case_bound_entries"] += sum(3 * d + z + 3 * bool(d) + bool(z) for z in (zp, zc))
        totals["case_exact_bridge_entries"] += zp
        for key, name in (
            ("constant_strict", "constant_increase"),
            ("bilinear_strict", "bilinear_increase"),
            ("upper_strict", "upper_decrease"),
        ):
            totals[key] += len(comparison[name]["strict_rows"])
        totals["inherited_exact_rows"] += zp
        totals["newly_exact_rows"] += len(newly)
        totals["unavailable_exact_rows"] += len(unavailable)
        cases.append(
            {
                "budget": budget,
                "levels": levels,
                "comparison": comparison,
                "exact_bridge": bridge,
                "witnesses": witnesses,
            }
        )
    zfp, zfc = (
        len(field["levels"][name]["certification"]["certified_rows"])
        for name in ("parent", "child")
    )
    counts = {
        "cells": len(cells),
        "positive_cells": sum(x is not None for x in cells),
        "parent_tiles": p,
        "child_tiles": m,
        "parent_bank_values": rp,
        "child_bank_values": rc,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": d,
        "undefined_rows": len(undefined),
        "budgets": b,
        "input_geometry_entries": 4 + 4 * sum(x is not None for x in cells) + 4 * p + 4 * m,
        "input_matrix_entries": s * rp + q * rp + q * s,
        "input_budget_entries": s + 2 * b,
        "geometry_entries": 1 + len(cells) + q + p + m,
        "restriction_entries": 16 * m,
        "parent_kernel_entries": 12 * q * p,
        "child_kernel_entries": 12 * q * m,
        "parent_map_entries": (3 * q + d) * rp,
        "child_map_entries": (3 * q + d) * rc,
        "field_bound_entries": sum(3 * d + z + 3 * bool(d) + bool(z) for z in (zfp, zfc)),
        "acquisition_entries": q * s + d * s + d + bool(d),
        "case_comparison_entries": b * (3 * d + 3 * bool(d)),
        **totals,
    }
    checks = {
        key: True
        for key in (
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
        )
    }
    return _detach(
        {
            "input": input,
            "field": field,
            "acquisition": acquisition,
            "cases": cases,
            "checks": checks,
            "counts": counts,
        }
    )
