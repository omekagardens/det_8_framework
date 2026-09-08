"""QR-05AO independent reference: ordered atoms, Simpson and row-basis solves.

The online decoder consumes measurements only. No executor imports or file reads.
"""

from copy import deepcopy
from fractions import Fraction
from itertools import combinations_with_replacement, pairwise, product
from math import factorial, gcd

MAX_BITS = 4096
F_BASIS = tuple(product(range(3), repeat=2))
R_BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))
M_BASIS = tuple(product(range(4), repeat=2))
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


def _nodes(bounds):
    if bounds is None:
        return ()
    a, b, c, d = bounds
    ux = (a, (a + b) / 2, b)
    vx = (c, (c + d) / 2, d)
    scale = (b - a) * (d - c) / 72
    factors = (1, 4, 1)
    return tuple(
        (u, v, scale * factors[i] * factors[j]) for i, u in enumerate(ux) for j, v in enumerate(vx)
    )


def _moments(bounds):
    return tuple(
        sum((weight * u**i * v**j for u, v, weight in _nodes(bounds)), ZERO) for i, j in M_BASIS
    )


def _ordered_axis(intervals):
    """Ordered simplex volume using endpoint atoms, including shared atoms."""
    if any(a >= b for a, b in intervals):
        return ZERO
    points = sorted({x for interval in intervals for x in interval})
    atoms = tuple(pairwise(points))
    eligible = [tuple(a <= lo and hi <= b for lo, hi in atoms) for a, b in intervals]
    result = ZERO
    for assignment in combinations_with_replacement(range(len(atoms)), len(intervals)):
        if not all(eligible[i][atom] for i, atom in enumerate(assignment)):
            continue
        value = Fraction(1)
        start = 0
        while start < len(assignment):
            finish = start + 1
            while finish < len(assignment) and assignment[finish] == assignment[start]:
                finish += 1
            lo, hi = atoms[assignment[start]]
            multiplicity = finish - start
            value *= (hi - lo) ** multiplicity / factorial(multiplicity)
            start = finish
        result += value
    return result


class _Geometry:
    def __init__(self):
        self.axis = {}
        self.chains = {}
        self.fields = {}
        self.successors = {}
        self.moments = {}

    def ordered_axis(self, intervals):
        if intervals not in self.axis:
            self.axis[intervals] = _ordered_axis(intervals)
        return self.axis[intervals]

    def ordered(self, rectangles):
        if any(b is None for b in rectangles):
            return ZERO
        if rectangles not in self.chains:
            axes = (self.ordered_axis(tuple((b[k], b[k + 1]) for b in rectangles)) for k in (0, 2))
            u, v = axes
            self.chains[rectangles] = u * v / 2 ** len(rectangles)
        return self.chains[rectangles]

    def field(self, a, b, u, v):
        key = (a, b, u, v)
        if key not in self.fields:
            if a is None or b is None or u <= b[0] or v <= b[2]:
                result = ZERO
            else:
                truncated = (b[0], min(b[1], u), b[2], min(b[3], v))
                result = self.ordered((a, truncated))
            self.fields[key] = result
        return self.fields[key]

    def successor(self, d, u, v):
        key = (d, u, v)
        if key not in self.successors:
            self.successors[key] = (
                ZERO
                if d is None
                else max(ZERO, d[1] - max(d[0], u)) * max(ZERO, d[3] - max(d[2], v)) / 2
            )
        return self.successors[key]

    def raw_moments(self, b):
        if b not in self.moments:
            self.moments[b] = _moments(b)
        return self.moments[b]


def _lagrange(nodes):
    answer = []
    for i, x in enumerate(nodes):
        others = [y for j, y in enumerate(nodes) if j != i]
        denominator = (x - others[0]) * (x - others[1])
        answer.append(
            (others[0] * others[1] / denominator, -sum(others) / denominator, 1 / denominator)
        )
    return answer


def _quadratic(bounds, function):
    a, b, c, d = bounds
    ux, vx = (a, (a + b) / 2, b), (c, (c + d) / 2, d)
    ul, vl = _lagrange(ux), _lagrange(vx)
    samples = [[function(u, v) for v in vx] for u in ux]
    return tuple(
        sum(
            (samples[k][l] * ul[k][i] * vl[l][j] for k in range(3) for l in range(3)),
            ZERO,
        )
        for i, j in F_BASIS
    )


def _corners(bounds, function):
    a, b, c, d = bounds
    ll, hl, lh, hh = function(a, c), function(b, c), function(a, d), function(b, d)
    uv = (hh - hl - lh + ll) / ((b - a) * (d - c))
    u = (hl - ll) / (b - a) - uv * c
    v = (lh - ll) / (d - c) - uv * a
    return (ll - u * a - v * c - uv * a * c, u, v, uv)


def _evaluate(coefficients, basis, u, v):
    return sum((value * u**i * v**j for value, (i, j) in zip(coefficients, basis)), ZERO)


MAX_ROWS = 32768
MAX_COLUMNS = 64
COUNT_NAMES = [
    "coarse_cells",
    "fine_cells",
    "positive_coarse_cells",
    "positive_fine_cells",
    "generators",
    "coarse_tiles",
    "fine_tiles",
    "input_bound_entries",
    "clipped_bound_entries",
    "tile_bound_entries",
    "coarse_moment_entries",
    "fine_moment_entries",
    "coarse_outgoing_vectors",
    "coarse_outgoing_entries",
    "fine_outgoing_vectors",
    "fine_outgoing_entries",
    "observation_rows",
    "observation_entries",
    "fine_weighted_rows",
    "fine_weighted_entries",
    "coarse_response_rows",
    "fine_response_rows",
    "field_rows",
    "target_entries",
    "geometric_decoder_entries",
    "certificates",
    "recoverable",
    "failed",
    "row_basis_entries",
    "pivot_column_entries",
    "canonical_decoder_entries",
    "collision_entries",
]


def _matrix(value, columns, minimum):
    _need(type(value) is list and minimum <= len(value) <= MAX_ROWS, "matrix rows")
    _need(
        all(type(row) is list and len(row) == columns for row in value),
        "matrix width",
    )
    return [[_fraction(x) for x in row] for row in value]


def _matrices(observations, targets):
    _native(observations)
    _native(targets)
    _need(
        type(targets) is list and 1 <= len(targets) <= MAX_ROWS,
        "nonempty target matrix",
    )
    _need(type(targets[0]) is list, "native target row")
    n = len(targets[0])
    _need(1 <= n <= MAX_COLUMNS, "matrix columns")
    _need(
        type(observations) is list and len(observations) <= MAX_ROWS,
        "observation rows",
    )
    _need(
        all(type(row) is list and len(row) == n for row in observations + targets),
        "complete matrix dimensions before elimination",
    )
    return _matrix(observations, n, 0), _matrix(targets, n, 1)


def _dot(left, right):
    return sum((x * y for x, y in zip(left, right)), ZERO)


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _forward_basis(rows):
    """Greedy original row selection with normalized forward echelon rows."""
    echelon = {}
    selected = []
    for index, original in enumerate(rows):
        row = list(original)
        for pivot in sorted(echelon):
            factor = row[pivot]
            if factor:
                row = [x - factor * y for x, y in zip(row, echelon[pivot])]
        pivot = next((i for i, x in enumerate(row) if x), None)
        if pivot is not None:
            divisor = row[pivot]
            echelon[pivot] = [x / divisor for x in row]
            selected.append(index)
    return selected, echelon


def _expression_basis(original_rows):
    """Track combinations during forward reduction of the chosen original basis."""
    size = len(original_rows)
    echelon = {}
    for index, original in enumerate(original_rows):
        row = list(original)
        coefficients = [Fraction(int(j == index)) for j in range(size)]
        for pivot in sorted(echelon):
            old_row, old_coefficients = echelon[pivot]
            factor = row[pivot]
            if factor:
                row = [x - factor * y for x, y in zip(row, old_row)]
                coefficients = [x - factor * y for x, y in zip(coefficients, old_coefficients)]
        pivot = next((i for i, x in enumerate(row) if x), None)
        _need(pivot is not None, "independent chosen rows")
        divisor = row[pivot]
        echelon[pivot] = (
            [x / divisor for x in row],
            [x / divisor for x in coefficients],
        )
    return echelon


def _express(target, basis):
    remaining = list(target)
    result = [ZERO] * len(basis)
    for pivot in sorted(basis):
        row, coefficients = basis[pivot]
        factor = remaining[pivot]
        if factor:
            remaining = [x - factor * y for x, y in zip(remaining, row)]
            result = [x + factor * y for x, y in zip(result, coefficients)]
    _need(not any(remaining), "target in selected observation span")
    return result


def _certificate(observations, targets):
    n = len(targets[0])
    augmented = [[Fraction(1)] * n] + observations
    selected, echelon = _forward_basis(augmented)
    target_basis, _ = _forward_basis(targets)
    joint_basis, _ = _forward_basis(augmented + targets)
    pivots = sorted(echelon)
    recoverable = len(selected) == len(joint_basis)
    decoder = collision = None
    if recoverable:
        original_rows = [augmented[i] for i in selected]
        expression_basis = _expression_basis(original_rows)
        decoder = [_express(q, expression_basis) for q in targets]
        for coefficients, target in zip(decoder, targets):
            reconstructed = [
                sum((c * row[j] for c, row in zip(coefficients, original_rows)), ZERO)
                for j in range(n)
            ]
            _need(reconstructed == target, "complete canonical decoder")
    else:
        for free in (j for j in range(n) if j not in echelon):
            difference = [ZERO] * n
            difference[free] = Fraction(1)
            # Back substitution yields the standard unique RREF free-column vector.
            for pivot in reversed(pivots):
                row = echelon[pivot]
                difference[pivot] = -sum(
                    (row[j] * difference[j] for j in range(pivot + 1, n)), ZERO
                )
            _need(not any(_matvec(augmented, difference)), "null difference")
            detected = _matvec(targets, difference)
            if not any(detected):
                continue
            mass = sum((x for x in difference if x > 0), ZERO)
            _need(mass > 0 and sum(difference, ZERO) == 0, "normalized kernel split")
            plus = [max(ZERO, x) / mass for x in difference]
            minus = [max(ZERO, -x) / mass for x in difference]
            op, om = _matvec(observations, plus), _matvec(observations, minus)
            tp, tm = _matvec(targets, plus), _matvec(targets, minus)
            delta = [x - y for x, y in zip(tp, tm)]
            _need(sum(plus, ZERO) == sum(minus, ZERO) == 1, "mixture normalization")
            _need(all(x >= 0 for x in plus + minus), "mixture nonnegative")
            _need(op == om and any(delta), "admissible observation collision")
            _need(delta == [x / mass for x in detected], "normalized target difference")
            separating = next(i for i, x in enumerate(delta) if x)
            collision = {
                "free_column": free,
                "difference": difference,
                "positive_weights": plus,
                "negative_weights": minus,
                "observed_positive": op,
                "observed_negative": om,
                "target_positive": tp,
                "target_negative": tm,
                "target_difference": delta,
                "separating_row": separating,
            }
            break
        _need(collision is not None, "complete failed certificate witness")
    return {
        "observation_rank": len(selected),
        "target_rank": len(target_basis),
        "joint_rank": len(joint_basis),
        "row_basis": selected,
        "pivot_columns": pivots,
        "recoverable": recoverable,
        "decoder": decoder,
        "collision": collision,
    }


def certify(O, Q):
    """Canonical exact recovery certificate or normalized nonnegative collision."""
    observations, targets = _matrices(O, Q)
    return _wire(_certificate(observations, targets))


def decode(row_basis, decoder, observed):
    """Apply a fixed compact certificate to measurements; no hidden field input."""
    _native(row_basis)
    _native(decoder)
    _native(observed)
    _need(type(observed) is list and len(observed) <= MAX_ROWS, "observed vector")
    _need(
        type(row_basis) is list
        and 1 <= len(row_basis) <= MAX_COLUMNS
        and all(type(i) is int for i in row_basis),
        "basis indices",
    )
    _need(
        row_basis == sorted(set(row_basis))
        and row_basis[0] == 0
        and row_basis[-1] <= len(observed),
        "sorted augmented basis indices",
    )
    coefficients = _matrix(decoder, len(row_basis), 1)
    measurements = [Fraction(1)] + [_fraction(x) for x in observed]
    return _wire(_matvec(coefficients, [measurements[i] for i in row_basis]))


def _parse_level(value):
    _keys(value, ("level", "cells"))
    _label(value["level"])
    _need(type(value["cells"]) is list and 1 <= len(value["cells"]) <= 8, "cell count")
    cells = []
    for cell in value["cells"]:
        _keys(cell, ("event", "bounds"))
        _need(type(cell["event"]) is int, "native event ID")
        cells.append((cell["event"], _rectangle(cell["bounds"])))
    ids = [i for i, _ in cells]
    _need(ids == sorted(set(ids)), "sorted unique IDs")
    for j, (_, b) in enumerate(cells):
        _need(all(_clip(b, other) is None for _, other in cells[j + 1 :]), "full cell disjointness")
    return cells


def _parse_problem(problem):
    _native(problem)
    _keys(problem, ("family", "probe", "coarse", "fine"))
    _label(problem["family"])
    _keys(problem["probe"], ("name", "bounds"))
    _label(problem["probe"]["name"])
    probe = _rectangle(problem["probe"]["bounds"])
    coarse = _parse_level(problem["coarse"])
    fine = _parse_level(problem["fine"])
    _need(problem["coarse"]["level"] != problem["fine"]["level"], "distinct levels")
    parents = {i: [] for i, _ in coarse}
    for child, b in fine:
        matches = [i for i, a in coarse if _inside(b, a)]
        _need(len(matches) == 1, "unique full parent")
        parents[matches[0]].append(child)
    fine_bounds = dict(fine)
    for parent, b in coarse:
        _need(
            sum((_area(fine_bounds[i]) for i in parents[parent]), ZERO) == _area(b),
            "full child coverage",
        )
    for cells in (coarse, fine):
        _need(
            sum((_area(_clip(b, probe)) for _, b in cells), ZERO) == _area(probe),
            "clipped probe coverage",
        )
    return probe, coarse, fine, parents


def _tiles(clips, route):
    wire, internal = [], []
    for event, bounds in clips.items():
        if bounds is None:
            continue
        breaks = []
        for k in (0, 2):
            breaks.append(
                sorted(
                    {bounds[k], bounds[k + 1]}
                    | {
                        x
                        for b in clips.values()
                        if b is not None
                        for x in b[k : k + 2]
                        if bounds[k] < x < bounds[k + 1]
                    }
                )
            )
        _need((len(breaks[0]) - 1) * (len(breaks[1]) - 1) <= 289, "shared tile count")
        for u0, u1 in pairwise(breaks[0]):
            for v0, v1 in pairwise(breaks[1]):
                b = (u0, u1, v0, v1)
                nodes = _nodes(b)
                moments = route.raw_moments(b)
                outgoing, coefficients, samples = [], {}, {}
                for last, d in clips.items():
                    function = lambda u, v, d=d: route.successor(d, u, v)
                    cs = _corners(b, function)
                    values = tuple(function(u, v) for u, v, _ in nodes)
                    _need(
                        all(
                            _evaluate(cs, R_BASIS, u, v) == value
                            for (u, v, _), value in zip(nodes, values)
                        ),
                        "outgoing bilinearity",
                    )
                    outgoing.append({"event": last, "coefficients": cs})
                    coefficients[last], samples[last] = cs, values
                wire.append({"event": event, "bounds": b, "moments": moments, "outgoing": outgoing})
                internal.append(
                    {
                        "event": event,
                        "bounds": b,
                        "nodes": nodes,
                        "r": coefficients,
                        "samples": samples,
                    }
                )
    return wire, internal


def _responses(cells, clips, generators, fine_clips, fine_tiles, route, coarse):
    matrix = []
    labels = []
    for first, second in product(cells, repeat=2):
        row = []
        selected = [t for t in fine_tiles if (t["parent"] if coarse else t["event"]) == first]
        for generator_index, (a, b) in enumerate(generators):
            value = sum(
                (
                    weight * fv * route.successor(clips[second], u, v)
                    for tile in selected
                    for (u, v, weight), fv in zip(tile["nodes"], tile["f"][generator_index])
                ),
                ZERO,
            )
            _need(
                value == route.ordered((fine_clips[a], fine_clips[b], clips[first], clips[second])),
                "direct four-point causal response",
            )
            row.append(value)
        labels.append({"first": first, "second": second})
        matrix.append(row)
    return labels, matrix


def build_family(problem):
    """Construct all geometry, measurements, targets and exact certificates."""
    probe, coarse, fine, parents = _parse_problem(problem)
    route = _Geometry()
    coarse_clips = {i: _clip(b, probe) for i, b in coarse}
    fine_clips = {i: _clip(b, probe) for i, b in fine}
    cids, fids = list(coarse_clips), list(fine_clips)
    parent_of = {child: parent for parent, children in parents.items() for child in children}
    generators = list(product(fids, repeat=2))
    n = len(generators)
    coarse_wire, coarse_tiles = _tiles(coarse_clips, route)
    fine_wire, fine_tiles = _tiles(fine_clips, route)
    fine_weighted = []
    synthesis = []
    for index, (wire_tile, tile) in enumerate(zip(fine_wire, fine_tiles)):
        parent = parent_of[tile["event"]]
        owners = [
            i
            for i, c in enumerate(coarse_tiles)
            if c["event"] == parent and _inside(tile["bounds"], c["bounds"])
        ]
        _need(len(owners) == 1, "unique global coarse tile")
        owner = owners[0]
        wire_tile["coarse_tile"] = owner
        tile["parent"], tile["owner"] = parent, owner
        # Recheck every coarse successor on every positive fine tile.
        for last, d in coarse_clips.items():
            function = lambda u, v, d=d: route.successor(d, u, v)
            cs = _corners(tile["bounds"], function)
            _need(cs == coarse_tiles[owner]["r"][last], "coarse outgoing polynomial on fine tile")
            _need(
                all(_evaluate(cs, R_BASIS, u, v) == function(u, v) for u, v, _ in tile["nodes"]),
                "fine grid supports every coarse outgoing",
            )
        samples, coefficients = [], []
        for a, b in generators:
            function = lambda u, v, a=a, b=b: route.field(fine_clips[a], fine_clips[b], u, v)
            cs = _quadratic(tile["bounds"], function)
            values = tuple(function(u, v) for u, v, _ in tile["nodes"])
            lo, hi, bottom, top = tile["bounds"]
            for i, j in product((1, 2), repeat=2):
                u, v = lo + (hi - lo) * i / 3, bottom + (top - bottom) * j / 3
                _need(_evaluate(cs, F_BASIS, u, v) == function(u, v), "fine synthesis polynomial")
            samples.append(values)
            coefficients.append(cs)
        tile["f"] = samples
        for i, j in R_BASIS:
            fine_weighted.append(
                [
                    sum(
                        (
                            weight * value * u**i * v**j
                            for (u, v, weight), value in zip(tile["nodes"], sample)
                        ),
                        ZERO,
                    )
                    for sample in samples
                ]
            )
        synthesis.extend([[cs[j] for cs in coefficients] for j in range(9)])
    weighted = [[ZERO] * n for _ in range(4 * len(coarse_tiles))]
    for index, tile in enumerate(fine_tiles):
        for j in range(4):
            row = fine_weighted[4 * index + j]
            target = weighted[4 * tile["owner"] + j]
            for g, x in enumerate(row):
                target[g] += x
    integral = [list(weighted[4 * t]) for t in range(len(coarse_tiles))]
    coarse_labels, qc = _responses(
        cids, coarse_clips, generators, fine_clips, fine_tiles, route, True
    )
    fine_labels, qf = _responses(fids, fine_clips, generators, fine_clips, fine_tiles, route, False)
    geometric_decoder = []
    for c, d in product(cids, repeat=2):
        geometric_decoder.append(
            [
                tile["r"][d][j] if tile["event"] == c else ZERO
                for tile in coarse_tiles
                for j in range(4)
            ]
        )
    for coefficients, target in zip(geometric_decoder, qc):
        for g in range(n):
            _need(
                sum((x * row[g] for x, row in zip(coefficients, weighted)), ZERO) == target[g],
                "direct geometric decoder identity",
            )
    _need(
        all(weighted[4 * t] == row for t, row in enumerate(integral)),
        "integral observed inside weighted",
    )
    for owner in range(len(coarse_tiles)):
        children = [i for i, t in enumerate(fine_tiles) if t["owner"] == owner]
        for j in range(4):
            _need(
                [sum((fine_weighted[4 * i + j][g] for i in children), ZERO) for g in range(n)]
                == weighted[4 * owner + j],
                "all weighted observation refinement",
            )
    fine_response_map = {
        (label["first"], label["second"]): row for label, row in zip(fine_labels, qf)
    }
    for label, row in zip(coarse_labels, qc):
        children = list(product(parents[label["first"]], parents[label["second"]]))
        _need(
            [sum((fine_response_map[pair][g] for pair in children), ZERO) for g in range(n)] == row,
            "full child response additivity",
        )
    total = _area(probe) ** 4 / 576
    _need(sum((sum(row, ZERO) for row in qc), ZERO) == total, "coarse response partition")
    _need(sum((sum(row, ZERO) for row in qf), ZERO) == total, "fine response partition")
    observations = [
        {
            "name": "integral",
            "rows": [{"tile": t, "basis": 0} for t in range(len(coarse_tiles))],
            "matrix": integral,
        },
        {
            "name": "weighted",
            "rows": [{"tile": t, "basis": j} for t in range(len(coarse_tiles)) for j in range(4)],
            "matrix": weighted,
        },
    ]
    targets = [
        {"name": "coarse", "rows": coarse_labels, "matrix": qc},
        {"name": "fine", "rows": fine_labels, "matrix": qf},
        {
            "name": "field",
            "rows": [
                {"tile": t, "power": [i, j]} for t in range(len(fine_tiles)) for i, j in F_BASIS
            ],
            "matrix": synthesis,
        },
    ]
    certificates = []
    for observation in observations:
        for target in targets:
            certificate = _certificate(observation["matrix"], target["matrix"])
            certificates.append(
                {
                    "observation": observation["name"],
                    "target": target["name"],
                    "certificate": certificate,
                }
            )
    _need(certificates[3]["certificate"]["recoverable"], "weighted coarse recovery")
    for j in range(3):
        _need(
            not certificates[j]["certificate"]["recoverable"]
            or certificates[j + 3]["certificate"]["recoverable"],
            "adding weighted observations cannot remove recovery",
        )
    geometry = {
        "volume": _area(probe),
        "parents": [{"parent": p, "children": c} for p, c in parents.items()],
        "coarse_cells": [
            {"event": i, "bounds": b, "volume": _area(b)} for i, b in coarse_clips.items()
        ],
        "fine_cells": [
            {"event": i, "bounds": b, "volume": _area(b)} for i, b in fine_clips.items()
        ],
        "coarse_tiles": coarse_wire,
        "fine_tiles": fine_wire,
    }
    checks = dict.fromkeys(
        (
            "weighted_contains_integral",
            "coarse_decoder_exact",
            "coarse_refinement_exact",
            "response_partition_exact",
            "measurement_refinement_exact",
        ),
        True,
    )
    counts = dict.fromkeys(COUNT_NAMES, 0)
    counts.update(
        coarse_cells=len(coarse),
        fine_cells=len(fine),
        positive_coarse_cells=sum(b is not None for b in coarse_clips.values()),
        positive_fine_cells=sum(b is not None for b in fine_clips.values()),
        generators=n,
        coarse_tiles=len(coarse_tiles),
        fine_tiles=len(fine_tiles),
        input_bound_entries=4 * (1 + len(coarse) + len(fine)),
        clipped_bound_entries=4
        * sum(b is not None for b in list(coarse_clips.values()) + list(fine_clips.values())),
        tile_bound_entries=4 * (len(coarse_tiles) + len(fine_tiles)),
        coarse_moment_entries=16 * len(coarse_tiles),
        fine_moment_entries=16 * len(fine_tiles),
        coarse_outgoing_vectors=len(coarse_tiles) * len(coarse),
        coarse_outgoing_entries=4 * len(coarse_tiles) * len(coarse),
        fine_outgoing_vectors=len(fine_tiles) * len(fine),
        fine_outgoing_entries=4 * len(fine_tiles) * len(fine),
        observation_rows=len(integral) + len(weighted),
        observation_entries=n * (len(integral) + len(weighted)),
        fine_weighted_rows=len(fine_weighted),
        fine_weighted_entries=n * len(fine_weighted),
        coarse_response_rows=len(qc),
        fine_response_rows=len(qf),
        field_rows=len(synthesis),
        target_entries=n * (len(qc) + len(qf) + len(synthesis)),
        geometric_decoder_entries=len(qc) * len(weighted),
        certificates=6,
    )
    for row in certificates:
        certificate = row["certificate"]
        counts["row_basis_entries"] += len(certificate["row_basis"])
        counts["pivot_column_entries"] += len(certificate["pivot_columns"])
        if certificate["recoverable"]:
            counts["recoverable"] += 1
            counts["canonical_decoder_entries"] += sum(len(r) for r in certificate["decoder"])
        else:
            counts["failed"] += 1
            collision = certificate["collision"]
            counts["collision_entries"] += (
                3 * n
                + 2 * len(collision["observed_positive"])
                + 3 * len(collision["target_positive"])
            )
    matrices = {
        "generators": [{"first": a, "second": b} for a, b in generators],
        "observations": observations,
        "targets": targets,
        "fine_weighted": fine_weighted,
        "coarse_decoder": geometric_decoder,
    }
    return _wire(
        {
            "problem": deepcopy(problem),
            "geometry": geometry,
            "matrices": matrices,
            "certificates": certificates,
            "checks": checks,
            "counts": counts,
        }
    )
