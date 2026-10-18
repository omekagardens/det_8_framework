"""Independent QR-05AN reference: interpolation, Simpson, ordered atoms.

Private supplied-geometry diagnostic. No other executor is imported. All caches
are constructed inside one build and contain only explicit geometric values.
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
COUNT_NAMES = [
    "levels",
    "probes",
    "level_pairs",
    "level_triples",
    "level_quadruples",
    "middle_cells",
    "positive_middle_cells",
    "tiles",
    "breakpoint_entries",
    "middle_bound_entries",
    "tile_bound_entries",
    "middle_moment_entries",
    "tile_moment_entries",
    "propagated_vectors",
    "propagated_entries",
    "forced_vectors",
    "forced_entries",
    "outgoing_vectors",
    "outgoing_entries",
    "nonbilinear_propagated_vectors",
    "quadruple_tile_visits",
    "positive_quadruples",
    "undefined_quad_conditionals",
    "zero_third_quadruples",
    "forced_positive_errors",
    "forced_zero_errors",
    "forced_negative_errors",
    "mean_positive_errors",
    "mean_zero_errors",
    "mean_negative_errors",
    "nonbilinear_quadruples",
    "nonbilinear_forced_equalities",
    "coarsening_moment_blocks",
    "coarsening_moment_entries",
    "field_blocks",
    "field_pieces",
    "field_child_terms",
    "field_coefficient_entries",
    "blocks",
    "child_terms",
    "via_middle_blocks",
]


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


def rectangle_moments(bounds):
    """Sixteen exact tensor-Simpson moments of a positive supplied rectangle."""
    _native(bounds)
    return _wire(_moments(_rectangle(bounds)))


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


def _integrate(coefficients, basis, moments):
    return sum((value * moments[4 * i + j] for value, (i, j) in zip(coefficients, basis)), ZERO)


def _contract(left, lbasis, right, rbasis, moments):
    return sum(
        (
            x * y * moments[4 * (i + k) + j + l]
            for x, (i, j) in zip(left, lbasis)
            for y, (k, l) in zip(right, rbasis)
        ),
        ZERO,
    )


def _bilinear(coefficients):
    return all(value == 0 for value, (i, j) in zip(coefficients, F_BASIS) if i == 2 or j == 2)


def _divide(value, denominator):
    return value / denominator if denominator else None


def _sign_count(counts, prefix, value):
    if value is not None:
        sign = "positive" if value > 0 else "negative" if value < 0 else "zero"
        counts[f"{prefix}_{sign}_errors"] += 1


def _parse(problem):
    _native(problem)
    _keys(problem, ("family", "probes", "levels"))
    _label(problem["family"])
    _need(type(problem["probes"]) is list and 1 <= len(problem["probes"]) <= 3, "probe count")
    probes = []
    for p in problem["probes"]:
        _keys(p, ("name", "bounds"))
        probes.append((_label(p["name"]), _rectangle(p["bounds"])))
    _need(len({p[0] for p in probes}) == len(probes), "distinct probes")
    _need(type(problem["levels"]) is list and len(problem["levels"]) == 3, "three levels")
    levels = []
    for level in problem["levels"]:
        _keys(level, ("level", "cells"))
        name = _label(level["level"])
        _need(type(level["cells"]) is list and 1 <= len(level["cells"]) <= 8, "cell count")
        cells = []
        for cell in level["cells"]:
            _keys(cell, ("event", "bounds"))
            _need(type(cell["event"]) is int, "native event ID")
            cells.append((cell["event"], _rectangle(cell["bounds"])))
        ids = [i for i, _ in cells]
        _need(ids == sorted(set(ids)), "sorted unique cell IDs")
        for i, (_, a) in enumerate(cells):
            _need(all(_clip(a, b) is None for _, b in cells[i + 1 :]), "disjoint full cells")
        for _, q in probes:
            _need(sum((_area(_clip(b, q)) for _, b in cells), ZERO) == _area(q), "probe coverage")
        levels.append((name, cells))
    _need(len({name for name, _ in levels}) == 3, "distinct levels")
    lineage = {}
    for coarse, fine in ((0, 1), (1, 2), (0, 2)):
        parents = {i: [] for i, _ in levels[coarse][1]}
        for child, b in levels[fine][1]:
            matches = [i for i, a in levels[coarse][1] if _inside(b, a)]
            _need(len(matches) == 1, "unique full parent")
            parents[matches[0]].append(child)
        fine_bounds = dict(levels[fine][1])
        for parent, a in levels[coarse][1]:
            _need(
                sum((_area(fine_bounds[i]) for i in parents[parent]), ZERO) == _area(a),
                "full child coverage",
            )
        lineage[coarse, fine] = parents
    for parent, children in lineage[0, 2].items():
        composed = sorted(c for middle in lineage[0, 1][parent] for c in lineage[1, 2][middle])
        _need(children == composed, "composed full lineage")
    return probes, levels, lineage


def _middle(event, bounds, ids, clips, route, counts):
    counts["middle_cells"] += 1
    counts["middle_moment_entries"] += 16
    moments = route.raw_moments(bounds)
    if bounds is None:
        return {
            "event": event,
            "bounds": None,
            "u_breaks": [],
            "v_breaks": [],
            "moments": moments,
            "tiles": [],
        }, []
    counts["positive_middle_cells"] += 1
    counts["middle_bound_entries"] += 4
    axes = []
    for k in (0, 2):
        axes.append(
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
    ub, vb = axes
    counts["breakpoint_entries"] += len(ub) + len(vb)
    _need((len(ub) - 1) * (len(vb) - 1) <= 289, "tile count")
    wire_tiles, internals = [], []
    for u0, u1 in pairwise(ub):
        for v0, v1 in pairwise(vb):
            tile = (u0, u1, v0, v1)
            raw = route.raw_moments(tile)
            nodes = _nodes(tile)
            propagated, outgoing, fp, rp = [], [], {}, {}
            for first, second in product(ids, repeat=2):
                a, b = clips[first], clips[second]
                function = lambda u, v, a=a, b=b: route.field(a, b, u, v)
                coefficients = _quadratic(tile, function)
                forced = _corners(tile, function)
                admissible = _bilinear(coefficients)
                samples = tuple(function(u, v) for u, v, _ in nodes)
                for (u, v, _), sample in zip(nodes, samples):
                    _need(
                        _evaluate(coefficients, F_BASIS, u, v) == sample, "propagated interpolation"
                    )
                    _need(_evaluate(forced, R_BASIS, u, v) >= sample, "corner majorization")
                # Off-interpolation nodes make this a separate pointwise check.
                for i, j in product((1, 2), repeat=2):
                    u, v = u0 + (u1 - u0) * i / 3, v0 + (v1 - v0) * j / 3
                    _need(
                        _evaluate(coefficients, F_BASIS, u, v) == function(u, v),
                        "off-node field certificate",
                    )
                propagated.append(
                    {
                        "first": first,
                        "second": second,
                        "coefficients": coefficients,
                        "forced_coefficients": forced,
                        "bilinear_admissible": admissible,
                    }
                )
                fp[first, second] = (coefficients, forced, admissible, samples)
                counts["nonbilinear_propagated_vectors"] += not admissible
            for last in ids:
                d = clips[last]
                function = lambda u, v, d=d: route.successor(d, u, v)
                coefficients = _corners(tile, function)
                samples = tuple(function(u, v) for u, v, _ in nodes)
                _need(
                    all(
                        _evaluate(coefficients, R_BASIS, u, v) == sample
                        for (u, v, _), sample in zip(nodes, samples)
                    ),
                    "outgoing interpolation",
                )
                outgoing.append({"event": last, "coefficients": coefficients})
                rp[last] = (coefficients, samples)
            wire_tiles.append(
                {"bounds": tile, "moments": raw, "propagated": propagated, "outgoing": outgoing}
            )
            internals.append({"bounds": tile, "moments": raw, "nodes": nodes, "f": fp, "r": rp})
    count = len(wire_tiles)
    n = len(ids)
    counts["tiles"] += count
    counts["tile_bound_entries"] += 4 * count
    counts["tile_moment_entries"] += 16 * count
    counts["propagated_vectors"] += n * n * count
    counts["propagated_entries"] += 9 * n * n * count
    counts["forced_vectors"] += n * n * count
    counts["forced_entries"] += 4 * n * n * count
    counts["outgoing_vectors"] += n * count
    counts["outgoing_entries"] += 4 * n * count
    _need(
        tuple(sum((t["moments"][i] for t in internals), ZERO) for i in range(16)) == moments,
        "tile moment additivity",
    )
    return {
        "event": event,
        "bounds": bounds,
        "u_breaks": ub,
        "v_breaks": vb,
        "moments": moments,
        "tiles": wire_tiles,
    }, internals


def _geometry(probe, q, cells, route, counts):
    ids = [i for i, _ in cells]
    clips = {i: _clip(b, q) for i, b in cells}
    volumes = {i: _area(b) for i, b in clips.items()}
    middles, middle_map, internal = [], {}, {}
    for i in ids:
        row, local = _middle(i, clips[i], ids, clips, route, counts)
        middles.append(row)
        middle_map[i], internal[i] = row, local
    pairs, pair_map = [], {}
    for first, second in product(ids, repeat=2):
        exact = sum(
            (_integrate(t["r"][second][0], R_BASIS, t["moments"]) for t in internal[first]), ZERO
        )
        _need(exact == route.ordered((clips[first], clips[second])), "direct pair integral")
        denominator = volumes[first] * volumes[second]
        pairs.append(
            {
                "first": first,
                "second": second,
                "volume_product": denominator,
                "causal_integral": exact,
                "conditional": _divide(exact, denominator),
            }
        )
        pair_map[first, second] = exact
    triples, triple_map = [], {}
    for first, second, third in product(ids, repeat=3):
        tiles = internal[third]
        exact = sum(
            (_integrate(t["f"][first, second][0], F_BASIS, t["moments"]) for t in tiles), ZERO
        )
        forced = sum(
            (_integrate(t["f"][first, second][1], R_BASIS, t["moments"]) for t in tiles), ZERO
        )
        _need(
            exact == route.ordered((clips[first], clips[second], clips[third])),
            "direct triple integral",
        )
        _need(forced >= exact, "forced triple upper bound")
        admissible = all(t["f"][first, second][2] for t in tiles)
        denominator = volumes[first] * volumes[second] * volumes[third]
        triples.append(
            {
                "first": first,
                "second": second,
                "third": third,
                "volume_product": denominator,
                "causal_integral": exact,
                "forced_integral": forced,
                "forced_error": forced - exact,
                "conditional": _divide(exact, denominator),
                "forced_conditional": _divide(forced, denominator),
                "propagated_bilinear": admissible,
            }
        )
        triple_map[first, second, third] = (exact, forced, admissible)
    quadruples, quad_map = [], {}
    for first, second, third, last in product(ids, repeat=4):
        tiles = internal[third]
        exact = sum(
            (
                _contract(t["f"][first, second][0], F_BASIS, t["r"][last][0], R_BASIS, t["moments"])
                for t in tiles
            ),
            ZERO,
        )
        forced = sum(
            (
                _contract(t["f"][first, second][1], R_BASIS, t["r"][last][0], R_BASIS, t["moments"])
                for t in tiles
            ),
            ZERO,
        )
        _need(
            exact == route.ordered(tuple(clips[i] for i in (first, second, third, last))),
            "direct four-point integral",
        )
        h = volumes[third]
        triple, _, admissible = triple_map[first, second, third]
        pair = pair_map[third, last]
        mean = triple * pair / h if h else None
        if h:
            mf, mr = triple / h, pair / h
            centered = sum(
                (
                    weight * (fv - mf) * (rv - mr)
                    for t in tiles
                    for (_, _, weight), fv, rv in zip(
                        t["nodes"], t["f"][first, second][3], t["r"][last][1]
                    )
                ),
                ZERO,
            )
            _need(centered == exact - mean, "direct centered quadrature")
            covariance = centered / h
            mean_error = mean - exact
        else:
            centered = covariance = mean_error = None
        denominator = volumes[first] * volumes[second] * h * volumes[last]
        error = forced - exact
        _need(error >= 0, "forced four-point upper bound")
        quadruples.append(
            {
                "first": first,
                "second": second,
                "third": third,
                "last": last,
                "volume_product": denominator,
                "causal_integral": exact,
                "forced_integral": forced,
                "forced_error": error,
                "mean_product": mean,
                "mean_error": mean_error,
                "conditional": _divide(exact, denominator),
                "forced_conditional": _divide(forced, denominator),
                "mean_conditional": _divide(mean, denominator),
                "third_covariance": covariance,
                "centered_integral": centered,
                "propagated_bilinear": admissible,
            }
        )
        quad_map[first, second, third, last] = exact
        counts["positive_quadruples"] += exact > 0
        counts["undefined_quad_conditionals"] += denominator == 0
        counts["zero_third_quadruples"] += h == 0
        counts["nonbilinear_quadruples"] += not admissible
        counts["nonbilinear_forced_equalities"] += not admissible and error == 0
        _sign_count(counts, "forced", error)
        _sign_count(counts, "mean", mean_error)
    n = len(ids)
    counts["level_pairs"] += n**2
    counts["level_triples"] += n**3
    counts["level_quadruples"] += n**4
    counts["quadruple_tile_visits"] += n**3 * sum(len(t) for t in internal.values())
    volume = _area(q)
    ps, ts, qs = (
        sum(pair_map.values(), ZERO),
        sum((x[0] for x in triple_map.values()), ZERO),
        sum(quad_map.values(), ZERO),
    )
    _need(ps == volume**2 / 4, "pair partition")
    _need(ts == volume**3 / 36, "triple partition")
    _need(qs == volume**4 / 576, "quadruple partition")
    fs = sum((x["forced_integral"] for x in quadruples), ZERO)
    ms = sum((x["mean_product"] for x in quadruples if x["mean_product"] is not None), ZERO)
    summary = {
        "pair_integral": ps,
        "pair_continuum_integral": volume**2 / 4,
        "triple_integral": ts,
        "triple_continuum_integral": volume**3 / 36,
        "quadruple_integral": qs,
        "quadruple_continuum_integral": volume**4 / 576,
        "forced_integral": fs,
        "forced_error": fs - qs,
        "mean_product": ms,
        "mean_error": ms - qs,
    }
    wire = {
        "probe": probe,
        "volume": volume,
        "cells": [{"event": i, "clipped_volume": volumes[i]} for i in ids],
        "middles": middles,
        "pairs": pairs,
        "triples": triples,
        "quadruples": quadruples,
        "summary": summary,
    }
    return wire, {"ids": ids, "middle": middle_map, "tiles": internal, "quad": quad_map}


def _coarsen(coarse, fine, parents, intermediate, counts):
    ids = coarse["ids"]
    moment_blocks, field_blocks, blocks = [], [], []
    for parent in ids:
        children = parents[parent]
        old = coarse["middle"][parent]["moments"]
        new = tuple(
            sum((fine["middle"][c]["moments"][i] for c in children), ZERO) for i in range(16)
        )
        _need(old == new, "coarsening moments")
        moment_blocks.append(
            {"parent": parent, "children": children, "coarse_moments": old, "child_moment_sum": new}
        )
    for first, second, third in product(ids, repeat=3):
        pieces = []
        coarse_tiles = coarse["tiles"][third]
        for child in parents[third]:
            for fine_index, tile in enumerate(fine["tiles"][child]):
                matches = [
                    i for i, t in enumerate(coarse_tiles) if _inside(tile["bounds"], t["bounds"])
                ]
                _need(len(matches) == 1, "unique coarse tile")
                coarse_index = matches[0]
                old = coarse_tiles[coarse_index]["f"][first, second][0]
                child_pairs = list(product(parents[first], parents[second]))
                new = tuple(
                    sum((tile["f"][a, b][0][i] for a, b in child_pairs), ZERO) for i in range(9)
                )
                _need(old == new, "pointwise field additivity")
                pieces.append(
                    {
                        "child": child,
                        "fine_tile": fine_index,
                        "coarse_tile": coarse_index,
                        "coarse_coefficients": old,
                        "child_coefficient_sum": new,
                    }
                )
                counts["field_child_terms"] += len(child_pairs)
        field_blocks.append({"first": first, "second": second, "third": third, "pieces": pieces})
        counts["field_pieces"] += len(pieces)
    for indices in product(ids, repeat=4):
        children = list(product(*(parents[i] for i in indices)))
        old = coarse["quad"][indices]
        new = sum((fine["quad"][c] for c in children), ZERO)
        _need(old == new, "true quadruple additivity")
        via = None
        if intermediate is not None:
            middle_parents, middle_blocks = intermediate
            via = sum(
                (middle_blocks[c] for c in product(*(middle_parents[i] for i in indices))), ZERO
            )
            _need(via == old, "via-middle true quadruples")
            counts["via_middle_blocks"] += 1
        first, second, third, last = indices
        blocks.append(
            {
                "first": first,
                "second": second,
                "third": third,
                "last": last,
                "children": children,
                "coarse_integral": old,
                "child_integral_sum": new,
                "via_middle_integral": via,
            }
        )
        counts["child_terms"] += len(children)
    counts["coarsening_moment_blocks"] += len(moment_blocks)
    counts["coarsening_moment_entries"] += 32 * len(moment_blocks)
    counts["field_blocks"] += len(field_blocks)
    counts["field_coefficient_entries"] += 18 * sum(len(r["pieces"]) for r in field_blocks)
    counts["blocks"] += len(blocks)
    return {"moment_blocks": moment_blocks, "field_blocks": field_blocks, "blocks": blocks}


def build_family(problem):
    """Build the full declared private AN wire from supplied rectangular geometry."""
    probes, levels, lineage = _parse(problem)
    route = _Geometry()
    counts = {name: 0 for name in COUNT_NAMES}
    counts["levels"], counts["probes"] = len(levels), len(probes)
    out_levels, internal = [], {}
    for level_index, (name, cells) in enumerate(levels):
        geometry = []
        for probe, q in probes:
            wire, data = _geometry(probe, q, cells, route, counts)
            geometry.append(wire)
            internal[level_index, probe] = data
        out_levels.append({"level": name, "geometry": geometry})
    coarsenings, blocks = [], {}
    for coarse, fine in ((0, 1), (1, 2), (0, 2)):
        parents = lineage[coarse, fine]
        geometry = []
        for probe, _ in probes:
            via = (lineage[0, 1], blocks[1, 2, probe]) if (coarse, fine) == (0, 2) else None
            witness = _coarsen(internal[coarse, probe], internal[fine, probe], parents, via, counts)
            blocks[coarse, fine, probe] = {
                (r["first"], r["second"], r["third"], r["last"]): r["child_integral_sum"]
                for r in witness["blocks"]
            }
            geometry.append({"probe": probe, **witness})
        coarsenings.append(
            {
                "coarse": levels[coarse][0],
                "fine": levels[fine][0],
                "parents": [{"parent": p, "children": c} for p, c in parents.items()],
                "geometry": geometry,
            }
        )
    return _wire(
        {
            "problem": deepcopy(problem),
            "levels": out_levels,
            "coarsenings": coarsenings,
            "counts": counts,
        }
    )
