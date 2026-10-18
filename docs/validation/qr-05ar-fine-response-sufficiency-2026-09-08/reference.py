"""QR-05AR reference: forward certificates and direct Simpson integration.

No decoder fitting, external reads, historical executors or coefficient/moment
contraction is used to obtain the new measurements and true responses.
"""

from copy import deepcopy
from fractions import Fraction
from itertools import pairwise, product
from math import gcd

MAX_BITS = 4096
ZERO = Fraction(0)
ONE = Fraction(1)
BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))


def _need(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    """Native containers may share children, but may not contain cycles."""
    pending = [(value, False)]
    active, done = set(), set()
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


def _fraction(value):
    _need(type(value) is list and len(value) == 2, "fraction pair")
    n, d = value
    _need(type(n) is int and type(d) is int and d > 0, "fraction integers")
    _need(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "fraction bits")
    _need(gcd(n, d) == 1, "reduced fraction")
    return Fraction(n, d)


def _rectangle(value):
    _need(type(value) is list and len(value) == 4, "rectangle bounds")
    bounds = tuple(_fraction(x) for x in value)
    _need(bounds[0] < bounds[1] and bounds[2] < bounds[3], "positive rectangle")
    return bounds


def _area(bounds):
    if bounds is None:
        return ZERO
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) / 2


def _inside(inner, outer):
    return (
        outer[0] <= inner[0] < inner[1] <= outer[1] and outer[2] <= inner[2] < inner[3] <= outer[3]
    )


def _overlap(left, right):
    if left is None or right is None:
        return False
    return max(left[0], right[0]) < min(left[1], right[1]) and max(left[2], right[2]) < min(
        left[3], right[3]
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


def _dimensions(matrix, rows, columns):
    _need(type(matrix) is list and len(matrix) == rows, "matrix rows")
    _need(
        all(type(row) is list and len(row) == columns for row in matrix),
        "matrix width",
    )


def _matrix(matrix):
    return [[_fraction(x) for x in row] for row in matrix]


def _dot(row, vector):
    return sum((a * b for a, b in zip(row, vector) if a and b), ZERO)


def apply(intercept, matrix, observed):
    """Apply only the supplied dense RAW affine map; raw rows are never null."""
    _native(intercept)
    _native(matrix)
    _native(observed)
    _need(type(intercept) is list and 1 <= len(intercept) <= 64, "output rows")
    _need(
        type(observed) is list and 4 <= len(observed) <= 1024 and len(observed) % 4 == 0,
        "observation width",
    )
    _dimensions(matrix, len(intercept), len(observed))
    a, x, rows = (
        [_fraction(v) for v in intercept],
        [_fraction(v) for v in observed],
        _matrix(matrix),
    )
    return _wire([b + _dot(row, x) for b, row in zip(a, rows)])


def _cell_partition(rows, probe):
    cells = [(r["event"], None if r["bounds"] is None else _rectangle(r["bounds"])) for r in rows]
    ids = [event for event, _ in cells]
    _need(ids == sorted(set(ids)), "sorted unique cell IDs")
    for index, (_, bounds) in enumerate(cells):
        if bounds is not None:
            _need(_inside(bounds, probe), "cell inside probe")
            _need(
                all(not _overlap(bounds, other) for _, other in cells[index + 1 :]),
                "disjoint cell interiors",
            )
    _need(sum((_area(b) for _, b in cells), ZERO) == _area(probe), "cell coverage")
    return cells


def _tile_partition(rows, cells):
    cell_map = dict(cells)
    tiles = [(row["event"], _rectangle(row["bounds"])) for row in rows]
    keys = [(event, b[0], b[2], b[1], b[3]) for event, b in tiles]
    _need(keys == sorted(keys), "tile ordering")
    for index, (event, bounds) in enumerate(tiles):
        _need(event in cell_map and cell_map[event] is not None, "positive tile owner")
        _need(_inside(bounds, cell_map[event]), "tile within cell")
        _need(
            all(not _overlap(bounds, other) for _, other in tiles[index + 1 :]),
            "disjoint tile interiors",
        )
    for event, bounds in cells:
        _need(
            sum((_area(b) for owner, b in tiles if owner == event), ZERO) == _area(bounds),
            "tile coverage",
        )
    return tiles


def _rectangle_shape(value, nullable=False):
    if nullable and value is None:
        return
    _need(type(value) is list and len(value) == 4, "rectangle shape")
    _need(all(type(x) is list and len(x) == 2 for x in value), "rectangle rational shape")


def _parse(problem):
    _native(problem)
    _keys(problem, ("family", "probe", "coarse_cells", "fine_cells", "coarse_tiles", "fine_tiles"))
    _need(type(problem["family"]) is str and bool(problem["family"]), "family label")
    _rectangle_shape(problem["probe"])
    for key in ("coarse_cells", "fine_cells"):
        _need(type(problem[key]) is list and 1 <= len(problem[key]) <= 8, "cell inventory")
        for row in problem[key]:
            _keys(row, ("event", "bounds"))
            _need(type(row["event"]) is int, "cell ID")
            _rectangle_shape(row["bounds"], True)
    for key in ("coarse_tiles", "fine_tiles"):
        _need(type(problem[key]) is list and 1 <= len(problem[key]) <= 64, "tile inventory")
        for row in problem[key]:
            _keys(
                row,
                ("event", "bounds")
                if key == "coarse_tiles"
                else ("event", "bounds", "coarse_tile"),
            )
            _need(type(row["event"]) is int, "tile ID")
            _rectangle_shape(row["bounds"])
    t = len(problem["coarse_tiles"])
    for row in problem["fine_tiles"]:
        _need(type(row["coarse_tile"]) is int and 0 <= row["coarse_tile"] < t, "coarse tile index")
    # All input shapes precede geometric arithmetic.
    probe = _rectangle(problem["probe"])
    coarse = _cell_partition(problem["coarse_cells"], probe)
    fine = _cell_partition(problem["fine_cells"], probe)
    parents = {}
    for event, bounds in fine:
        containing = [
            owner
            for owner, cb in coarse
            if cb is not None and bounds is not None and _inside(bounds, cb)
        ]
        _need(bounds is None or len(containing) == 1, "unique clipped parent")
        parents[event] = None if bounds is None else containing[0]
    for event, bounds in coarse:
        _need(
            sum((_area(b) for e, b in fine if parents[e] == event), ZERO) == _area(bounds),
            "fine cell coverage",
        )
    ct = _tile_partition(problem["coarse_tiles"], coarse)
    ft = _tile_partition(problem["fine_tiles"], fine)
    ownership = [row["coarse_tile"] for row in problem["fine_tiles"]]
    for (event, bounds), index in zip(ft, ownership):
        owner, cb = ct[index]
        _need(parents[event] == owner and _inside(bounds, cb), "fine tile ancestry")
    for index, (_, bounds) in enumerate(ct):
        _need(
            sum((_area(b) for (_, b), owner in zip(ft, ownership) if owner == index), ZERO)
            == _area(bounds),
            "coarse tile descendants",
        )
    return probe, coarse, fine, ct, ft, parents, ownership


def _overlay(fine_tiles, fine_cells, ownership):
    """Plan the FULL unconditional endpoint overlay before any moments/matrices."""
    plans = []
    total = 0
    for _, bounds in fine_tiles:
        us = sorted(
            {
                bounds[0],
                bounds[1],
                *(
                    x
                    for _, b in fine_cells
                    if b is not None
                    for x in b[:2]
                    if bounds[0] < x < bounds[1]
                ),
            }
        )
        vs = sorted(
            {
                bounds[2],
                bounds[3],
                *(
                    x
                    for _, b in fine_cells
                    if b is not None
                    for x in b[2:]
                    if bounds[2] < x < bounds[3]
                ),
            }
        )
        count = (len(us) - 1) * (len(vs) - 1)
        _need(count >= 1, "positive overlay piece count")
        total += count
        _need(total <= 256, "repair piece cap")
        plans.append((us, vs))
    repair = []
    for index, ((event, _), (us, vs)) in enumerate(zip(fine_tiles, plans)):
        for u0, u1 in pairwise(us):
            for v0, v1 in pairwise(vs):
                repair.append((event, (u0, u1, v0, v1), index, ownership[index]))
    _need(len(repair) == total, "complete overlay inventory")
    return repair


def _reduce(row, echelon):
    """Forward reduction plus its expression in the original accepted rows."""
    remainder = list(row)
    expression = {}
    for pivot in sorted(echelon):
        factor = remainder[pivot]
        if not factor:
            continue
        basis, combination = echelon[pivot]
        for index in range(pivot, len(row)):
            remainder[index] -= factor * basis[index]
        for original, value in combination.items():
            expression[original] = expression.get(original, ZERO) + factor * value
    return remainder, expression


def _echelon(rows):
    """Greedy original-row admission, with pivot-sorted forward rows."""
    accepted = []
    echelon = {}
    for index, row in enumerate(rows):
        remainder, expression = _reduce(row, echelon)
        pivot = next((j for j, x in enumerate(remainder) if x), None)
        if pivot is None:
            continue
        factor = remainder[pivot]
        combination = {j: -x / factor for j, x in expression.items() if x}
        combination[index] = ONE / factor
        echelon[pivot] = ([x / factor for x in remainder], combination)
        accepted.append(index)
    return accepted, echelon


def _null_vector(echelon, n, column):
    vector = [ZERO] * n
    vector[column] = ONE
    for pivot in sorted(echelon, reverse=True):
        row = echelon[pivot][0]
        vector[pivot] = -_dot(row[pivot + 1 :], vector[pivot + 1 :])
    return vector


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _matmul(left, right):
    columns = list(zip(*right))
    return [[_dot(row, column) for column in columns] for row in left]


def _certificate(observations, targets):
    n = len(targets[0])
    augmented = [[ONE] * n] + observations
    selected, echelon = _echelon(augmented)
    _need(selected and selected[0] == 0, "normalization basis")
    pivots = sorted(echelon)
    free = [j for j in range(n) if j not in echelon]
    basis = [augmented[j] for j in selected]
    row_decoders = []
    for target in targets:
        remainder, expression = _reduce(target, echelon)
        if any(remainder):
            row_decoders.append(None)
        else:
            coefficients = [expression.get(j, ZERO) for j in selected]
            _need(
                [
                    sum((d * row[j] for d, row in zip(coefficients, basis) if d and row[j]), ZERO)
                    for j in range(n)
                ]
                == target,
                "recovered complete identity",
            )
            row_decoders.append(coefficients)
    recovered = [j for j, row in enumerate(row_decoders) if row is not None]
    failed = [j for j, row in enumerate(row_decoders) if row is None]
    target_rank = len(_echelon(targets)[0])
    joint_rank = len(_echelon(augmented + targets)[0])
    _need((joint_rank == len(selected)) == (not failed), "joint-rank membership")
    _need(
        target_rank <= joint_rank and len(selected) <= joint_rank <= len(selected) + target_rank,
        "rank bounds",
    )
    collision = None
    # Back substitution constructs the unique RREF free-column vector without
    # performing primary-style Gauss-Jordan elimination.
    for column in free:
        vector = _null_vector(echelon, n, column)
        _need(not any(_matvec(augmented, vector)), "complete null identity")
        delta = _matvec(targets, vector)
        detected = next((j for j, x in enumerate(delta) if x), None)
        if detected is None:
            continue
        _need(bool(failed), "null witness contradicts recovery")
        mass = sum((x for x in vector if x > 0), ZERO)
        _need(
            mass > 0 and mass == -sum((x for x in vector if x < 0), ZERO), "positive collision mass"
        )
        plus = [max(x, ZERO) / mass for x in vector]
        minus = [max(-x, ZERO) / mass for x in vector]
        _need(sum(plus, ZERO) == 1 and sum(minus, ZERO) == 1, "normalized mixtures")
        _need(
            all(x >= 0 and y >= 0 and x * y == 0 for x, y in zip(plus, minus)),
            "disjoint positive supports",
        )
        observed_plus, observed_minus = _matvec(observations, plus), _matvec(observations, minus)
        truth_plus, truth_minus = _matvec(targets, plus), _matvec(targets, minus)
        difference = [x - y for x, y in zip(truth_plus, truth_minus)]
        _need(observed_plus == observed_minus, "identical coarse observations")
        _need(difference == [x / mass for x in delta], "normalized collision difference")
        _need(
            difference[detected] != 0 and all(x == 0 for x in difference[:detected]),
            "first detecting row",
        )
        collision = {
            "free_column": column,
            "separating_row": detected,
            "null_vector": vector,
            "positive_mass": mass,
            "weights_plus": plus,
            "weights_minus": minus,
            "observed_plus": observed_plus,
            "observed_minus": observed_minus,
            "truth_plus": truth_plus,
            "truth_minus": truth_minus,
            "truth_difference": difference,
        }
        break
    _need((collision is None) == (not failed), "complete recovery-or-collision alternative")
    return {
        "observation_rank": len(selected),
        "target_rank": target_rank,
        "joint_rank": joint_rank,
        "row_basis": selected,
        "pivot_columns": pivots,
        "free_columns": free,
        "recoverable": not failed,
        "decoder": row_decoders if not failed else None,
        "recoverable_rows": recovered,
        "failed_rows": failed,
        "row_decoders": row_decoders,
        "collision": collision,
    }


def certify(observations, targets):
    """Exact finite simplex sufficiency; no geometry/provenance is assumed."""
    _native(observations)
    _native(targets)
    _need(
        type(targets) is list and 1 <= len(targets) <= 64 and type(targets[0]) is list,
        "target inventory",
    )
    n = len(targets[0])
    _need(1 <= n <= 576, "source inventory")
    _need(type(observations) is list and len(observations) <= 256, "observation inventory")
    _dimensions(observations, len(observations), n)
    _dimensions(targets, len(targets), n)
    return _wire(_certificate(_matrix(observations), _matrix(targets)))


def _nodes(lo, hi, knots=()):
    cuts = sorted({lo, hi, *(x for x in knots if lo < x < hi)})
    result = {}
    for left, right in pairwise(cuts):
        width = (right - left) / 6
        for x, factor in ((left, 1), ((left + right) / 2, 4), (right, 1)):
            result[x] = result.get(x, ZERO) + factor * width
    return tuple(result.items())


def _integral(bounds, function, outgoing=None):
    """Exact on each cubic piece; evaluate the support polynomial at endpoints."""
    if bounds is None:
        return ZERO
    uk, vk = ((), ()) if outgoing is None else (outgoing[:2], outgoing[2:])
    un, vn = _nodes(bounds[0], bounds[1], uk), _nodes(bounds[2], bounds[3], vk)
    return sum((wu * wv * function(u, v) / 2 for u, wu in un for v, wv in vn), ZERO)


def _moments(bounds):
    return [
        _integral(bounds, lambda u, v, i=i, j=j: u**i * v**j) for i in range(4) for j in range(4)
    ]


def _tail(x, lo, hi):
    return max(ZERO, min(hi - lo, hi - x))


def _response(bounds, u, v):
    if bounds is None:
        return ZERO
    return _tail(u, bounds[0], bounds[1]) * _tail(v, bounds[2], bounds[3]) / 2


def _outgoing(tile, destination):
    if destination is None:
        return [ZERO] * 4
    if tile[0] >= destination[1] or tile[2] >= destination[3]:
        return [ZERO] * 4
    _need(
        all(not tile[0] < x < tile[1] for x in destination[:2])
        and all(not tile[2] < x < tile[3] for x in destination[2:]),
        "active outgoing knot inside coarse tile",
    )
    u0, u1, v0, v1 = tile
    f00, f10, f01, f11 = (
        _response(destination, u, v) for u, v in ((u0, v0), (u1, v0), (u0, v1), (u1, v1))
    )
    cross = (f11 - f10 - f01 + f00) / ((u1 - u0) * (v1 - v0))
    cu = (f10 - f00) / (u1 - u0) - cross * v0
    cv = (f01 - f00) / (v1 - v0) - cross * u0
    coefficients = [f00 - cu * u0 - cv * v0 - cross * u0 * v0, cu, cv, cross]
    for u, v in product((u0, (u0 + u1) / 2, u1), (v0, (v0 + v1) / 2, v1)):
        _need(
            _dot(coefficients, [ONE, u, v, u * v]) == _response(destination, u, v),
            "outgoing corner interpolation",
        )
    return coefficients


def _bernstein(index, x):
    if index == 0:
        return (1 - x) ** 2
    if index == 1:
        return 2 * x * (1 - x)
    return x * x


def _source(bounds, i, j, amplitude, u, v):
    # Deliberately the polynomial extension, NOT a boundary-zeroed indicator.
    return (
        amplitude
        * _bernstein(i, (u - bounds[0]) / (bounds[1] - bounds[0]))
        * _bernstein(j, (v - bounds[2]) / (bounds[3] - bounds[2]))
    )


def _quadratic(nodes, values):
    x0, x1, x2 = nodes
    y0, y1, y2 = values
    first = (y1 - y0) / (x1 - x0)
    second = ((y2 - y1) / (x2 - x1) - first) / (x2 - x0)
    return [y0 - first * x0 + second * x0 * x1, first - second * (x0 + x1), second]


def _source_coefficients(bounds, i, j, amplitude):
    us = (bounds[0], (bounds[0] + bounds[1]) / 2, bounds[1])
    vs = (bounds[2], (bounds[2] + bounds[3]) / 2, bounds[3])
    along_u = [_quadratic(us, [_source(bounds, i, j, amplitude, u, v) for u in us]) for v in vs]
    coefficients = [x for p in range(3) for x in _quadratic(vs, [row[p] for row in along_u])]
    for u, v in product(us, vs):
        actual = sum(
            (coefficients[3 * p + q] * u**p * v**q for p in range(3) for q in range(3)), ZERO
        )
        _need(actual == _source(bounds, i, j, amplitude, u, v), "source interpolation")
    return coefficients


def _geometric(cells, tiles, outgoing):
    size = len(cells)
    matrix = [[ZERO] * (4 * len(tiles)) for _ in range(size * size)]
    for first, (event, _) in enumerate(cells):
        for tile, (owner, *_) in enumerate(tiles):
            if owner == event:
                for second in range(size):
                    matrix[first * size + second][4 * tile : 4 * tile + 4] = outgoing[tile][second]
    return matrix


def _repair_collision(certificate, fine_o, repair_o, matrix, scales):
    witness = certificate["collision"]
    if witness is None:
        return None
    plus, minus = witness["weights_plus"], witness["weights_minus"]
    fine_plus, fine_minus = _matvec(fine_o, plus), _matvec(fine_o, minus)
    op, om = _matvec(repair_o, plus), _matvec(repair_o, minus)
    diff = [x - y for x, y in zip(op, om)]
    _need(any(diff), "repair distinguishes collision")
    pp, pm = _matvec(matrix, op), _matvec(matrix, om)
    rp = [x - y for x, y in zip(pp, witness["truth_plus"])]
    rm = [x - y for x, y in zip(pm, witness["truth_minus"])]
    _need(not any(rp) and not any(rm), "both repaired truths")
    normalized = [
        None if scale == 0 else x / scale for x, scale in zip(witness["truth_difference"], scales)
    ]
    for x, scale in zip(witness["truth_difference"], scales):
        _need(scale != 0 or x == 0, "empty response collision")
    return {
        "fine_observed_plus": fine_plus,
        "fine_observed_minus": fine_minus,
        "observed_plus": op,
        "observed_minus": om,
        "difference": diff,
        "predicted_plus": pp,
        "predicted_minus": pm,
        "residual_plus": rp,
        "residual_minus": rm,
        "normalized_truth_difference": normalized,
    }


def build_family(problem):
    probe, coarse, fine, ct, ft, parents, ownership = _parse(problem)
    rt = _overlay(ft, fine, ownership)
    c, d, t, f, r = len(coarse), len(fine), len(ct), len(ft), len(rt)
    n, mc, mf, mr, qc, qf = 9 * f, 4 * t, 4 * f, 4 * r, c * c, d * d
    volume = _area(probe)
    amplitude = volume**2
    cm = [_moments(b) for _, b in ct]
    fm = [_moments(b) for _, b in ft]
    rm = [_moments(b) for _, b, _, _ in rt]
    co = [[_outgoing(b, dest) for _, dest in coarse] for _, b in ct]
    ro = [[_outgoing(b, dest) for _, dest in fine] for _, b, _, _ in rt]
    for index in range(f):
        for k in range(16):
            _need(
                fm[index][k]
                == sum(
                    (rm[j][k] for j, (_, _, parent, _) in enumerate(rt) if parent == index), ZERO
                ),
                "fine-repair moment sum",
            )
    for index in range(t):
        for k in range(16):
            from_fine = sum((fm[j][k] for j, p in enumerate(ownership) if p == index), ZERO)
            from_repair = sum((rm[j][k] for j, (_, _, _, p) in enumerate(rt) if p == index), ZERO)
            _need(cm[index][k] == from_fine == from_repair, "complete coarse moment sums")
    oc, of, orr = (
        [[ZERO] * n for _ in range(mc)],
        [[ZERO] * n for _ in range(mf)],
        [[ZERO] * n for _ in range(mr)],
    )
    tc, tf = [[ZERO] * n for _ in range(qc)], [[ZERO] * n for _ in range(qf)]
    ci, fi = {e: i for i, (e, _) in enumerate(coarse)}, {e: i for i, (e, _) in enumerate(fine)}
    generators, masses = [], []
    for tile, (event, bounds) in enumerate(ft):
        owner = ownership[tile]
        first_c, first_f = ci[parents[event]], fi[event]
        coefficients_for_tile = []
        for i, j in product(range(3), repeat=2):
            column = len(generators)
            coefficients = _source_coefficients(bounds, i, j, amplitude)
            coefficients_for_tile.append(coefficients)
            generators.append({"tile": tile, "i": i, "j": j, "coefficients": coefficients})

            def field(u, v, b=bounds, i=i, j=j):
                return _source(b, i, j, amplitude, u, v)

            for basis, (p, q) in enumerate(BASIS):
                oc[4 * owner + basis][column] = _integral(
                    bounds, lambda u, v, p=p, q=q: field(u, v) * u**p * v**q
                )
                of[4 * tile + basis][column] = _integral(
                    bounds, lambda u, v, p=p, q=q: field(u, v) * u**p * v**q
                )
                for piece, (_, b, original, _) in enumerate(rt):
                    if original == tile:
                        orr[4 * piece + basis][column] = _integral(
                            b, lambda u, v, p=p, q=q: field(u, v) * u**p * v**q
                        )
            mass = _integral(bounds, field)
            _need(mass == amplitude * _area(bounds) / 9, "generator integral")
            masses.append(mass)
            for second, (_, destination) in enumerate(coarse):
                tc[first_c * c + second][column] = _integral(
                    bounds,
                    lambda u, v, dest=destination: field(u, v) * _response(dest, u, v),
                    destination,
                )
            for second, (_, destination) in enumerate(fine):
                tf[first_f * d + second][column] = _integral(
                    bounds,
                    lambda u, v, dest=destination: field(u, v) * _response(dest, u, v),
                    destination,
                )
        _need(
            [sum((row[k] for row in coefficients_for_tile), ZERO) for k in range(9)]
            == [amplitude] + [ZERO] * 8,
            "source coefficient partition",
        )
        for x in (ZERO, Fraction(1, 3), Fraction(1, 2), ONE):
            factors = [_bernstein(i, x) for i in range(3)]
            _need(
                all(x >= 0 for x in factors) and sum(factors, ZERO) == 1,
                "nonnegative Bernstein partition",
            )
    for tile in range(f):
        descendants = [j for j, (_, _, original, _) in enumerate(rt) if original == tile]
        for basis in range(4):
            _need(
                of[4 * tile + basis]
                == [sum((orr[4 * j + basis][g] for j in descendants), ZERO) for g in range(n)],
                "fine observations from repair",
            )
    for tile in range(t):
        children = [j for j, parent in enumerate(ownership) if parent == tile]
        descendants = [j for j, (_, _, _, parent) in enumerate(rt) if parent == tile]
        for basis in range(4):
            via_fine = [sum((of[4 * j + basis][g] for j in children), ZERO) for g in range(n)]
            direct = [sum((orr[4 * j + basis][g] for j in descendants), ZERO) for g in range(n)]
            _need(oc[4 * tile + basis] == via_fine == direct, "all coarse observation sums")
    aggregated = [[ZERO] * n for _ in range(qc)]
    for row, ((first, _), (second, _)) in enumerate(product(fine, repeat=2)):
        pc, pd = parents[first], parents[second]
        if pc is not None and pd is not None:
            target = ci[pc] * c + ci[pd]
            for g, x in enumerate(tf[row]):
                aggregated[target][g] += x
    _need(tc == aggregated, "two-parent response sums")
    gc, gr = _geometric(coarse, ct, co), _geometric(fine, rt, ro)
    _need(_matmul(gc, oc) == tc, "coarse geometric identity")
    predicted = _matmul(gr, orr)
    residual = [[x - y for x, y in zip(row, truth)] for row, truth in zip(predicted, tf)]
    _need(all(x == 0 for row in residual for x in row), "fine geometric identity")
    constant_c = [
        amplitude * _integral(b, lambda u, v, p=p, q=q: u**p * v**q)
        for _, b in ct
        for p, q in BASIS
    ]
    constant_f = [
        amplitude * _integral(b, lambda u, v, p=p, q=q: u**p * v**q)
        for _, b in ft
        for p, q in BASIS
    ]
    constant_r = [
        amplitude * _integral(b, lambda u, v, p=p, q=q: u**p * v**q)
        for _, b, _, _ in rt
        for p, q in BASIS
    ]
    constants_qc = [
        amplitude * _integral(cb, lambda u, v, dest=db: _response(dest, u, v), db)
        for (_, cb), (_, db) in product(coarse, repeat=2)
    ]
    constants_qf = [
        amplitude * _integral(cb, lambda u, v, dest=db: _response(dest, u, v), db)
        for (_, cb), (_, db) in product(fine, repeat=2)
    ]
    for constant, matrix in (
        (constant_c, oc),
        (constant_f, of),
        (constant_r, orr),
        (constants_qc, tc),
        (constants_qf, tf),
    ):
        _need(constant == [sum(row, ZERO) for row in matrix], "constant field column sums")
    _need(sum(masses, ZERO) == volume**3, "dictionary total integral")
    scales_c = [amplitude * _area(cb) * _area(db) for (_, cb), (_, db) in product(coarse, repeat=2)]
    scales_f = [amplitude * _area(cb) * _area(db) for (_, cb), (_, db) in product(fine, repeat=2)]
    certificate = _certificate(oc, tf)
    repair_collision = _repair_collision(certificate, of, orr, gr, scales_f)
    repair = {
        "intercept": [ZERO] * qf,
        "matrix": gr,
        "predicted": predicted,
        "residuals": residual,
        "exact": True,
        "collision": repair_collision,
    }
    defined = sum(scale != 0 for scale in scales_f)
    collision = int(certificate["collision"] is not None)
    decoder_entries = sum(len(row) for row in certificate["row_decoders"] if row is not None)
    if certificate["decoder"] is not None:
        decoder_entries += sum(len(row) for row in certificate["decoder"])
    counts = {
        "coarse_cells": c,
        "fine_cells": d,
        "positive_coarse_cells": sum(b is not None for _, b in coarse),
        "positive_fine_cells": sum(b is not None for _, b in fine),
        "coarse_tiles": t,
        "fine_tiles": f,
        "repair_tiles": r,
        "added_repair_tiles": r - f,
        "generators": n,
        "coarse_observation_rows": mc,
        "fine_observation_rows": mf,
        "repair_observation_rows": mr,
        "coarse_response_rows": qc,
        "fine_response_rows": qf,
        "defined_fine_response_rows": defined,
        "undefined_fine_response_rows": qf - defined,
        "coarse_moment_entries": 16 * t,
        "fine_moment_entries": 16 * f,
        "repair_moment_entries": 16 * r,
        "outgoing_entries": 4 * (t * c + r * d),
        "source_coefficient_entries": 9 * n,
        "observation_entries": (mc + mf + mr) * n,
        "target_entries": (qc + qf) * n,
        "constant_observation_entries": mc + mf + mr,
        "constant_target_entries": qc + qf,
        "generator_integral_entries": n,
        "raw_geometric_entries": qc * mc + qf * (1 + mr),
        "certificate_decoder_entries": decoder_entries,
        "recoverable_rows": len(certificate["recoverable_rows"]),
        "failed_rows": len(certificate["failed_rows"]),
        "collisions": collision,
        "collision_entries": collision * (3 * n + 2 * mc + 3 * qf + 1),
        "repair_prediction_entries": qf * n,
        "repair_residual_entries": qf * n,
        "repair_collision_entries": collision * (2 * mf + 3 * mr + 4 * qf + defined),
    }
    return _wire(
        {
            "problem": deepcopy(problem),
            "geometry": {
                "volume": volume,
                "coarse_cells": [{"event": e, "bounds": b, "volume": _area(b)} for e, b in coarse],
                "fine_cells": [{"event": e, "bounds": b, "volume": _area(b)} for e, b in fine],
                "parents": [{"event": e, "parent": parents[e]} for e, _ in fine],
                "coarse_tiles": [
                    {
                        "event": e,
                        "bounds": b,
                        "moments": cm[j],
                        "outgoing": [
                            {"event": de, "coefficients": coef}
                            for (de, _), coef in zip(coarse, co[j])
                        ],
                    }
                    for j, (e, b) in enumerate(ct)
                ],
                "fine_tiles": [
                    {"event": e, "bounds": b, "coarse_tile": ownership[j], "moments": fm[j]}
                    for j, (e, b) in enumerate(ft)
                ],
                "repair_tiles": [
                    {
                        "event": e,
                        "bounds": b,
                        "fine_tile": original,
                        "coarse_tile": owner,
                        "moments": rm[j],
                        "outgoing": [
                            {"event": de, "coefficients": coef}
                            for (de, _), coef in zip(fine, ro[j])
                        ],
                    }
                    for j, (e, b, original, owner) in enumerate(rt)
                ],
                "coarse_response_scales": scales_c,
                "fine_response_scales": scales_f,
            },
            "generators": generators,
            "matrices": {
                "coarse_observation_rows": [
                    {"tile": tile, "basis": basis} for tile in range(t) for basis in range(4)
                ],
                "fine_observation_rows": [
                    {"tile": tile, "basis": basis} for tile in range(f) for basis in range(4)
                ],
                "repair_observation_rows": [
                    {"tile": tile, "basis": basis} for tile in range(r) for basis in range(4)
                ],
                "coarse_response_rows": [
                    {"first": ce, "second": de} for ce, _ in coarse for de, _ in coarse
                ],
                "fine_response_rows": [
                    {"first": ce, "second": de} for ce, _ in fine for de, _ in fine
                ],
                "coarse_observations": oc,
                "fine_observations": of,
                "repair_observations": orr,
                "coarse_targets": tc,
                "fine_targets": tf,
                "coarse_geometric": gc,
                "generator_integrals": masses,
                "constant_coarse_observations": constant_c,
                "constant_fine_observations": constant_f,
                "constant_repair_observations": constant_r,
                "constant_coarse_targets": constants_qc,
                "constant_fine_targets": constants_qf,
            },
            "certificate": certificate,
            "repair": repair,
            "checks": {
                name: True
                for name in (
                    "geometry_partitions",
                    "bernstein_partition",
                    "generator_integrals",
                    "moment_additivity",
                    "observation_additivity",
                    "response_additivity",
                    "geometric_coarse_identity",
                    "geometric_fine_identity",
                    "coarse_certificate_valid",
                    "collision_valid",
                    "repair_collision_valid",
                    "constant_field_sums",
                )
            },
            "counts": counts,
        }
    )
