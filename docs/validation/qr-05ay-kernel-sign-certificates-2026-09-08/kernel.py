"""Exact bilinear-kernel sign certificates and bounded-field envelopes."""

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


def _problem(problem):
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
    # Complete all structural inventories before constructing any Fraction.
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


def _endpoint(index, direction, signs, wires, A, J, scales, L, U, gain, defined, amplitude):
    corners = [F(direction * sign) for sign in signs]
    _require(all(abs(x) <= 1 for x in corners), "endpoint corner bound")
    integrated = integrate(wires["probe"], wires["tiles"], _encode(corners))
    bank_wire = integrated["raw_moments"]
    observed_wire = produce(wires["B"], bank_wire)
    direct_wire = produce(wires["G"], bank_wire)
    decoded_wire = apply(wires["D"], observed_wire)
    bank, observed = _vector(bank_wire), _vector(observed_wire)
    direct, decoded = _vector(direct_wire), _vector(decoded_wire)
    minima, maxima = _vector(integrated["minima"]), _vector(integrated["maxima"])
    _require(direct == decoded == _linear(J, corners), "actual endpoint response identity")
    _require(
        all(-amplitude <= lo <= hi <= amplitude for lo, hi in zip(minima, maxima, strict=True)),
        "actual endpoint field bound",
    )
    normalized = _normalized(decoded, scales)
    for i in defined:
        _require(normalized[i] == _dot(A[i], corners), "endpoint normalized response")
        _require(abs(normalized[i]) <= L[i] <= U[i], "endpoint lower-class and corner bounds")
    out = {
        "corners": corners,
        "local_coefficients": _vector(integrated["local_coefficients"]),
        "global_coefficients": _vector(integrated["global_coefficients"]),
        "local_moments": _vector(integrated["local_moments"]),
        "bank_error": bank,
        "tile_minima": minima,
        "tile_maxima": maxima,
        "observed_error": observed,
        "direct_error": direct,
        "decoded_error": decoded,
        "normalized_error": normalized,
    }
    if index is not None:
        _require(normalized[index] == direction * gain, "lower-bound endpoint attainment")
        out["attained"] = normalized[index]
    return out


def build_family(problem):
    """Certify the supplied kernel rows without assuming pointwise positivity."""
    probe, cells, tiles, B, G, D, targets, q, r, s, t = _problem(problem)
    V, cell_volumes, tile_volumes, scales, defined, undefined = _geometry(
        problem, probe, cells, tiles, targets
    )
    _require(
        all(all(x == 0 for x in G[i]) for i in undefined),
        "null-cell target requires zero raw geometric row",
    )
    K = _mm(D, B, r)
    residual = _subtract(K, G)
    _require(_zero(residual), "frozen bank identity")
    geometry = {
        "volume": V,
        "cell_volumes": cell_volumes,
        "tile_volumes": tile_volumes,
        "target_scales": scales,
        "defined_rows": defined,
        "undefined_rows": undefined,
    }
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
    # Encode retained maps/bounds before public pipelines, without bounding
    # unretained antiderivative products or partial sums.
    _encode({"geometry": geometry, "maps": maps, "bounds": bounds})
    wires = {
        "probe": problem["probe"],
        "tiles": [tile["bounds"] for tile in problem["tiles"]],
        "B": problem["interface"],
        "G": problem["geometric"],
        "D": problem["decoder"],
    }
    constant_witnesses, bilinear_witnesses = [], []
    for i in range(q):
        if not scales[i]:
            constant_witnesses.append(None)
            bilinear_witnesses.append(None)
            continue
        constant_signs = [_sign(v) for v in integrals[i]]
        bilinear_signs = [_sign(v) for v in A[i]]
        for destination, signs, expanded, gain in (
            (
                constant_witnesses,
                constant_signs,
                [v for v in constant_signs for _ in range(4)],
                C[i],
            ),
            (bilinear_witnesses, bilinear_signs, bilinear_signs, L[i]),
        ):
            destination.append(
                {
                    "target_row": i,
                    "signs": signs,
                    "positive": _endpoint(
                        i, 1, expanded, wires, A, J, scales, L, U, gain, defined, amplitude
                    ),
                    "negative": _endpoint(
                        i, -1, expanded, wires, A, J, scales, L, U, gain, defined, amplitude
                    ),
                }
            )
    positive = _endpoint(None, 1, [1] * r, wires, A, J, scales, L, U, None, defined, amplitude)
    negative = _endpoint(None, -1, [1] * r, wires, A, J, scales, L, U, None, defined, amplitude)
    for i in defined:
        response = sum(A[i], F(0))
        _require(
            positive["normalized_error"][i] == response
            and negative["normalized_error"][i] == -response,
            "global constant controls",
        )
    witnesses = {
        "tile_constant": constant_witnesses,
        "bilinear": bilinear_witnesses,
        "constant_positive": positive,
        "constant_negative": negative,
    }
    comparison = {
        "bilinear_minus_constant": _comparison(L, C, defined),
        "upper_minus_bilinear": _comparison(U, L, defined),
        "upper_minus_certified": _comparison(U, exact, certified),
    }
    d, z = len(defined), len(certified)
    a = sum(cell is not None for cell in cells)
    counts = {
        "cells": len(cells),
        "positive_cells": a,
        "tiles": t,
        "bank_values": r,
        "receiver_values": s,
        "target_rows": q,
        "defined_rows": d,
        "undefined_rows": len(undefined),
        "geometry_input_entries": 4 + 4 * a + 4 * t,
        "input_matrix_entries": s * r + q * r + q * s,
        "geometry_entries": 1 + len(cells) + t + q,
        "kernel_entries": 12 * q * t,
        "map_entries": (3 * q + d) * r,
        "bound_entries": 3 * d + z + (3 if d else 0) + (1 if z else 0),
        "comparison_entries": 2 * d + z + (2 if d else 0) + (1 if z else 0),
        "mixed_tiles": sum(map(len, obstructions)),
        "mixed_rows": len(uncertified),
        "certified_rows": z,
        "pointwise_nonnegative_rows": len(nonnegative),
        "pointwise_nonpositive_rows": len(nonpositive),
        "pointwise_zero_rows": len(zero),
        "integrated_nonnegative_rows": len(integrated_nonnegative),
        "integrated_nonpositive_rows": len(integrated_nonpositive),
        "integrated_zero_rows": len(integrated_zero),
        "integrated_nonnegative_mixed_rows": len(integrated_mixed),
        "tile_constant_witnesses": 2 * d,
        "bilinear_witnesses": 2 * d,
        "constant_witnesses": 2,
        "tile_sign_entries": d * t,
        "bilinear_sign_entries": d * r,
        "endpoint_entries": 4 * d * (5 * r + 2 * t + s + 2 * q + d + 1),
        "constant_endpoint_entries": 2 * (5 * r + 2 * t + s + 2 * q + d),
        "constant_gap_strict": len(comparison["bilinear_minus_constant"]["strict_rows"]),
        "upper_gap_strict": len(comparison["upper_minus_bilinear"]["strict_rows"]),
        "certified_upper_gap_strict": len(comparison["upper_minus_certified"]["strict_rows"]),
        "constant_maximizers": len(maxima["constant_lower"]["rows"]),
        "bilinear_maximizers": len(maxima["bilinear_lower"]["rows"]),
        "upper_maximizers": len(maxima["corner_upper"]["rows"]),
        "certified_maximizers": len(maxima["certified_gain"]["rows"]),
    }
    checks = {
        key: True
        for key in (
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
    }
    return _detach(
        {
            "problem": problem,
            "geometry": geometry,
            "kernels": kernel_wire,
            "maps": maps,
            "bounds": bounds,
            "certification": certification,
            "witnesses": witnesses,
            "comparison": comparison,
            "checks": checks,
            "counts": counts,
        }
    )
