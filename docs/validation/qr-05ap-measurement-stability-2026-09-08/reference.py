"""QR-05AP independent reference: frozen-map probes and interval endpoints.

No decoder fitting, field construction, executor imports or hidden reads.
"""

from copy import deepcopy
from fractions import Fraction
from itertools import product
from math import gcd

MAX_BITS = 4096
ZERO = Fraction(0)


def _need(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    """Reject foreign types and cycles, while allowing shared native containers."""
    pending = [(value, False)]
    active = set()
    done = set()
    while pending:
        current, leaving = pending.pop()
        kind = type(current)
        if kind in (dict, list):
            identity = id(current)
            if leaving:
                active.remove(identity)
                done.add(identity)
                continue
            _need(identity not in active, "cyclic native input")
            if identity in done:
                continue
            active.add(identity)
            pending.append((current, True))
            if kind is dict:
                _need(all(type(k) is str for k in current), "native object keys")
                pending.extend((v, False) for v in current.values())
            else:
                pending.extend((v, False) for v in current)
        else:
            _need(kind in (str, int, type(None)), "non-native mathematical input")
            if kind is int:
                _need(abs(current).bit_length() <= MAX_BITS, "integer bits")


def _keys(value, expected):
    _need(type(value) is dict and set(value) == set(expected), "object fields")


def _label(value):
    _need(type(value) is str and bool(value), "nonempty native label")
    return value


def _fraction(value):
    _need(type(value) is list and len(value) == 2, "fraction pair")
    n, d = value
    _need(type(n) is int and type(d) is int and d > 0, "fraction integers")
    _need(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "fraction bits")
    _need(gcd(n, d) == 1, "reduced fraction")
    return Fraction(n, d)


def _rectangle(value):
    _need(type(value) is list and len(value) == 4, "rectangle bounds")
    b = tuple(_fraction(x) for x in value)
    _need(b[0] < b[1] and b[2] < b[3], "positive rectangle")
    return b


def _area(bounds):
    if bounds is None:
        return ZERO
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) / 2


def _clip(a, b):
    if a is None or b is None:
        return None
    out = (max(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), min(a[3], b[3]))
    return out if out[0] < out[1] and out[2] < out[3] else None


def _inside(inner, outer):
    return (
        outer[0] <= inner[0] < inner[1] <= outer[1] and outer[2] <= inner[2] < inner[3] <= outer[3]
    )


def _wire(value):
    if type(value) is Fraction:
        _need(
            max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
            "retained rational bits",
        )
        return [value.numerator, value.denominator]
    if type(value) in (list, tuple):
        return [_wire(x) for x in value]
    if type(value) is dict:
        return {k: _wire(v) for k, v in value.items()}
    if type(value) is int:
        _need(abs(value).bit_length() <= MAX_BITS, "retained integer bits")
    _need(type(value) in (str, int, bool, type(None)), "internal output type")
    return value


COUNT_NAMES = [
    "cells",
    "positive_cells",
    "tiles",
    "generators",
    "observations",
    "responses",
    "defined_responses",
    "undefined_responses",
    "transform_entries",
    "dimensionless_observation_entries",
    "dimensionless_target_entries",
    "raw_decoder_entries",
    "normalized_decoder_entries",
    "gain_entries",
    "witnesses",
    "witness_sign_entries",
    "witness_output_entries",
    "maximizing_rows",
    "canonical_lower_rows",
    "geometric_lower_rows",
    "tied_rows",
]


def _dot(row, vector):
    return sum((x * y for x, y in zip(row, vector)), ZERO)


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _matmul(left, right):
    columns = list(zip(*right))
    return [[_dot(row, column) for column in columns] for row in left]


def _dimensions(matrix, rows, columns):
    _need(type(matrix) is list and len(matrix) == rows, "matrix rows")
    _need(
        all(type(row) is list and len(row) == columns for row in matrix),
        "matrix width",
    )


def _parse_matrix(matrix):
    return [[_fraction(x) for x in row] for row in matrix]


def apply(intercept, matrix, z):
    """Apply only a supplied affine measurement map, including undefined rows."""
    _native(intercept)
    _native(matrix)
    _native(z)
    _need(type(z) is list and 4 <= len(z) <= 256 and len(z) % 4 == 0, "local width")
    _need(type(intercept) is list and 1 <= len(intercept) <= 64, "output rows")
    _need(type(matrix) is list and len(matrix) == len(intercept), "paired output rows")
    for b, row in zip(intercept, matrix):
        _need(
            (b is None and row is None)
            or (b is not None and type(row) is list and len(row) == len(z)),
            "null pairing and matrix width",
        )
    values = [_fraction(x) for x in z]
    result = []
    for b, row in zip(intercept, matrix):
        result.append(
            None if b is None else _fraction(b) + _dot([_fraction(x) for x in row], values)
        )
    return _wire(result)


def _parse(problem):
    _native(problem)
    _keys(
        problem,
        ("family", "probe", "cells", "tiles", "observations", "targets", "canonical", "geometric"),
    )
    _label(problem["family"])
    _need(type(problem["probe"]) is list and len(problem["probe"]) == 4, "probe bounds")
    _need(type(problem["cells"]) is list and 1 <= len(problem["cells"]) <= 8, "cell inventory")
    _need(type(problem["tiles"]) is list and 1 <= len(problem["tiles"]) <= 64, "tile inventory")
    c, t = len(problem["cells"]), len(problem["tiles"])
    m, q = 4 * t, c * c
    for row in problem["cells"] + problem["tiles"]:
        _keys(row, ("event", "bounds"))
        _need(type(row["event"]) is int, "native event ID")
    _need(
        type(problem["observations"]) is list and len(problem["observations"]) == m,
        "observation rows",
    )
    _need(type(problem["observations"][0]) is list, "observation row")
    n = len(problem["observations"][0])
    _need(1 <= n <= 64, "generator columns")
    _dimensions(problem["observations"], m, n)
    _dimensions(problem["targets"], q, n)
    _dimensions(problem["geometric"], q, m)
    _keys(problem["canonical"], ("row_basis", "decoder"))
    basis = problem["canonical"]["row_basis"]
    _need(
        type(basis) is list and 1 <= len(basis) <= 64 and all(type(i) is int for i in basis),
        "canonical basis size/types",
    )
    _need(
        basis == sorted(set(basis)) and basis[0] == 0 and basis[-1] <= m,
        "canonical basis indices",
    )
    _dimensions(problem["canonical"]["decoder"], q, len(basis))
    # All list/matrix inventories are admitted before exact arithmetic loops.
    probe = _rectangle(problem["probe"])
    cells = [
        (row["event"], None if row["bounds"] is None else _rectangle(row["bounds"]))
        for row in problem["cells"]
    ]
    ids = [i for i, _ in cells]
    _need(ids == sorted(set(ids)), "sorted unique cell IDs")
    for j, (_, bounds) in enumerate(cells):
        if bounds is not None:
            _need(_inside(bounds, probe), "cell inside probe")
            _need(
                all(_clip(bounds, other) is None for _, other in cells[j + 1 :]),
                "disjoint cell interiors",
            )
    volume = _area(probe)
    _need(sum((_area(bounds) for _, bounds in cells), ZERO) == volume, "cell coverage")
    cell_map = dict(cells)
    tiles = [(row["event"], _rectangle(row["bounds"])) for row in problem["tiles"]]
    ordering = [(event, b[0], b[2], b[1], b[3]) for event, b in tiles]
    _need(ordering == sorted(ordering), "declared tile ordering")
    for j, (event, bounds) in enumerate(tiles):
        _need(event in cell_map and cell_map[event] is not None, "nonempty tile owner")
        _need(_inside(bounds, cell_map[event]), "tile within cell")
        _need(
            all(_clip(bounds, other) is None for _, other in tiles[j + 1 :]),
            "disjoint tile interiors",
        )
    for event, bounds in cells:
        _need(
            sum((_area(b) for i, b in tiles if i == event), ZERO) == _area(bounds),
            "complete tile coverage",
        )
    observations = _parse_matrix(problem["observations"])
    targets = _parse_matrix(problem["targets"])
    compact = _parse_matrix(problem["canonical"]["decoder"])
    geometric = _parse_matrix(problem["geometric"])
    raw_intercept = [ZERO] * q
    raw_matrix = [[ZERO] * m for _ in range(q)]
    for i, row in enumerate(compact):
        for index, coefficient in zip(basis, row):
            if index == 0:
                raw_intercept[i] = coefficient
            else:
                raw_matrix[i][index - 1] = coefficient
    cell_volumes = [_area(bounds) for _, bounds in cells]
    tile_volumes = [_area(bounds) for _, bounds in tiles]
    response_rows = [{"first": first, "second": second} for first, second in product(ids, repeat=2)]
    scales = [volume**2 * hc * hd for hc, hd in product(cell_volumes, repeat=2)]
    for scale, target in zip(scales, targets):
        _need(scale > 0 or not any(target), "empty response has zero raw targets")
    policies = [
        ("canonical", raw_intercept, raw_matrix),
        ("geometric", [ZERO] * q, geometric),
    ]
    columns = list(zip(*observations))
    for _, intercept, matrix in policies:
        for a, row, target in zip(intercept, matrix, targets):
            _need(
                [a + _dot(row, column) for column in columns] == target,
                "complete inherited raw response identity",
            )
    return {
        "volume": volume,
        "cells": cells,
        "tiles": tiles,
        "cell_volumes": cell_volumes,
        "tile_volumes": tile_volumes,
        "response_rows": response_rows,
        "scales": scales,
        "observations": observations,
        "targets": targets,
        "policies": policies,
        "generators": n,
        "width": m,
    }


def _corner_transform(bounds, volume):
    """Recover each global monomial's local polynomial from four corner values."""
    u0, u1, v0, v1 = bounds
    points = ((u0, v0), (u1, v0), (u0, v1), (u1, v1))
    functions = (
        lambda u, v: Fraction(1),
        lambda u, v: u,
        lambda u, v: v,
        lambda u, v: u * v,
    )
    factor = volume**2 * _area(bounds)
    rows = []
    for function in functions:
        ll, hl, lh, hh = [function(u, v) for u, v in points]
        rows.append([factor * x for x in (ll, hl - ll, lh - ll, hh - hl - lh + ll)])
    return rows


def _inverse(matrix):
    """Forward elimination, then four independent back substitutions."""
    n = len(matrix)
    left = [list(row) for row in matrix]
    right = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for pivot in range(n):
        selected = next((j for j in range(pivot, n) if left[j][pivot]), None)
        _need(selected is not None, "invertible coordinate block")
        left[pivot], left[selected] = left[selected], left[pivot]
        right[pivot], right[selected] = right[selected], right[pivot]
        for row in range(pivot + 1, n):
            factor = left[row][pivot] / left[pivot][pivot]
            left[row] = [x - factor * y for x, y in zip(left[row], left[pivot])]
            right[row] = [x - factor * y for x, y in zip(right[row], right[pivot])]
    columns = []
    for column in range(n):
        result = [ZERO] * n
        for row in reversed(range(n)):
            result[row] = (
                right[row][column]
                - sum((left[row][j] * result[j] for j in range(row + 1, n)), ZERO)
            ) / left[row][row]
        columns.append(result)
    return [list(row) for row in zip(*columns)]


def _raw_from_local(transforms, z):
    result = []
    for tile, transform in enumerate(transforms):
        result.extend(_matvec(transform, z[4 * tile : 4 * tile + 4]))
    return result


def _raw_evaluate(intercept, matrix, x):
    return [a + _dot(row, x) for a, row in zip(intercept, matrix)]


def _decoder(name, intercept, raw_matrix, transforms, scales, observation_map, target_map):
    width = 4 * len(transforms)
    raw_zero = _raw_evaluate(intercept, raw_matrix, _raw_from_local(transforms, [ZERO] * width))
    normalized_intercept = [a / scale if scale else None for a, scale in zip(raw_zero, scales)]
    normalized = [([] if scale else None) for scale in scales]
    for index in range(width):
        basis = [ZERO] * width
        basis[index] = Fraction(1)
        raw_response = _raw_evaluate(intercept, raw_matrix, _raw_from_local(transforms, basis))
        for row, (value, base, scale) in enumerate(zip(raw_response, raw_zero, scales)):
            if scale:
                normalized[row].append((value - base) / scale)
    columns = list(zip(*observation_map))
    for b, row, target in zip(normalized_intercept, normalized, target_map):
        if row is None:
            _need(b is None and target is None, "undefined normalized row")
        else:
            _need([b + _dot(row, column) for column in columns] == target, "normalized identity")
    gains, witnesses = [], []
    for index, row in enumerate(normalized):
        if row is None:
            gains.append(None)
            witnesses.append(None)
            continue
        # Independent coordinate interval endpoints: Minkowski-sum extrema.
        lower = upper = ZERO
        signs = []
        for coefficient in row:
            left, right = -coefficient, coefficient
            lower += min(left, right)
            upper += max(left, right)
            signs.append(1 if coefficient > 0 else -1 if coefficient < 0 else 0)
        _need(lower == -upper and upper >= 0, "symmetric error interval")
        _need(all(type(s) is int and -1 <= s <= 1 for s in signs), "witness box")
        output = [None if r is None else _dot(r, signs) for r in normalized]
        raw_witness = _raw_evaluate(intercept, raw_matrix, _raw_from_local(transforms, signs))
        direct_error = [
            (value - base) / scale if scale else None
            for value, base, scale in zip(raw_witness, raw_zero, scales)
        ]
        _need(output == direct_error, "same-map witness output")
        attained = output[index]
        _need(attained == upper, "sharp interval attained by witness")
        gains.append(upper)
        witnesses.append({"signs": signs, "output": output, "attained": attained})
    defined = [value for value in gains if value is not None]
    maximum = max(defined) if defined else None
    maximizers = [i for i, value in enumerate(gains) if value is not None and value == maximum]
    return {
        "name": name,
        "raw_intercept": intercept,
        "raw_matrix": raw_matrix,
        "intercept": normalized_intercept,
        "matrix": normalized,
        "row_gains": gains,
        "witnesses": witnesses,
        "max_gain": maximum,
        "max_rows": maximizers,
    }


def build_family(problem):
    """Analyze exactly the two inherited maps under the declared coordinate box."""
    parsed = _parse(problem)
    volume, width = parsed["volume"], parsed["width"]
    transforms = [_corner_transform(b, volume) for _, b in parsed["tiles"]]
    inverses = [_inverse(transform) for transform in transforms]
    identity = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    for forward, backward in zip(transforms, inverses):
        _need(_matmul(forward, backward) == identity, "forward inverse")
        _need(_matmul(backward, forward) == identity, "backward inverse")
    observations = []
    for tile, inverse in enumerate(inverses):
        observations.extend(_matmul(inverse, parsed["observations"][4 * tile : 4 * tile + 4]))
    targets = [
        [x / scale for x in row] if scale else None
        for row, scale in zip(parsed["targets"], parsed["scales"])
    ]
    decoders = [
        _decoder(name, a, matrix, transforms, parsed["scales"], observations, targets)
        for name, a, matrix in parsed["policies"]
    ]
    differences, clower, glower, tied, undefined = [], [], [], [], []
    for index, (left, right) in enumerate(zip(decoders[0]["row_gains"], decoders[1]["row_gains"])):
        if left is None or right is None:
            _need(left is None and right is None, "paired undefined response")
            differences.append(None)
            undefined.append(index)
        else:
            difference = left - right
            differences.append(difference)
            (clower if difference < 0 else glower if difference > 0 else tied).append(index)
    _need(
        sorted(clower + glower + tied + undefined) == list(range(len(parsed["scales"]))),
        "complete disjoint gain comparison",
    )
    defined = sum(scale > 0 for scale in parsed["scales"])
    q, n, t = len(parsed["scales"]), parsed["generators"], len(transforms)
    counts = dict.fromkeys(COUNT_NAMES, 0)
    counts.update(
        cells=len(parsed["cells"]),
        positive_cells=sum(b is not None for _, b in parsed["cells"]),
        tiles=t,
        generators=n,
        observations=width,
        responses=q,
        defined_responses=defined,
        undefined_responses=q - defined,
        transform_entries=32 * t,
        dimensionless_observation_entries=width * n,
        dimensionless_target_entries=defined * n,
        raw_decoder_entries=2 * q * (width + 1),
        normalized_decoder_entries=2 * defined * (width + 1),
        gain_entries=2 * defined,
        witnesses=2 * defined,
        witness_sign_entries=2 * defined * width,
        witness_output_entries=2 * defined * defined,
        maximizing_rows=sum(len(d["max_rows"]) for d in decoders),
        canonical_lower_rows=len(clower),
        geometric_lower_rows=len(glower),
        tied_rows=len(tied),
    )
    return _wire(
        {
            "problem": deepcopy(problem),
            "geometry": {
                "volume": volume,
                "cell_volumes": parsed["cell_volumes"],
                "tile_volumes": parsed["tile_volumes"],
                "response_rows": parsed["response_rows"],
                "response_scales": parsed["scales"],
            },
            "coordinates": {
                "raw_from_local": transforms,
                "local_from_raw": inverses,
                "observations": observations,
                "targets": targets,
            },
            "decoders": decoders,
            "comparison": {
                "gain_difference": differences,
                "canonical_lower_rows": clower,
                "geometric_lower_rows": glower,
                "tied_rows": tied,
                "undefined_rows": undefined,
            },
            "checks": dict.fromkeys(
                (
                    "raw_response_identity",
                    "coordinate_inverse",
                    "normalized_response_identity",
                    "witness_box",
                    "witness_attainment",
                    "complete_gain_partition",
                ),
                True,
            ),
            "counts": counts,
        }
    )
