"""Independent corner/Simpson verification of a supplied middle-moment contract.

This bounded research engine has no file reads or historical-engine imports.
Global bilinear coefficients come from corner values. Tensor-Simpson integrals
of raw monomials and direct causal-volume clamps independently check every
moment contraction, including both centered controls.
"""

from copy import deepcopy
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, product
from math import gcd

MAX_BITS = 4096
EXPONENTS = ((0, 0), (1, 0), (0, 1), (1, 1))
LINKS = ((0, 1), (1, 2), (0, 2))
COUNT_KEYS = (
    "levels",
    "probes",
    "level_pairs",
    "level_triples",
    "blocks",
    "child_terms",
    "middle_cells",
    "positive_middle_cells",
    "tiles",
    "breakpoint_entries",
    "middle_bound_entries",
    "tile_bound_entries",
    "middle_moment_entries",
    "tile_moment_entries",
    "coefficient_vectors",
    "coefficient_entries",
    "coarsening_moment_blocks",
    "coarsening_moment_entries",
    "zero_middle_level_triples",
    "undefined_level_conditionals",
    "positive_triples",
    "original_positive_errors",
    "original_zero_errors",
    "original_negative_errors",
    "tile_positive_errors",
    "tile_zero_errors",
    "tile_negative_errors",
    "between_positive_errors",
    "between_zero_errors",
    "between_negative_errors",
)


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _object(value, keys):
    _require(
        type(value) is dict and all(type(key) is str for key in value) and set(value) == set(keys),
        "exact native object schema",
    )


def _integer(value):
    _require(type(value) is int and value.bit_length() <= MAX_BITS, "bounded native integer")
    return value


def _fraction(value):
    _require(type(value) is list and len(value) == 2, "rational pair")
    numerator, denominator = map(_integer, value)
    _require(denominator > 0 and gcd(numerator, denominator) == 1, "reduced rational")
    return Fraction(numerator, denominator)


def _wire(value):
    if value is None:
        return None
    _require(type(value) in (int, Fraction), "exact retained rational")
    value = Fraction(value)
    return [_integer(value.numerator), _integer(value.denominator)]


def _label(value):
    _require(type(value) is str and bool(value), "nonempty label")
    return value


def _rectangle(bounds):
    _require(type(bounds) is list and len(bounds) == 4, "rectangle bounds")
    result = tuple(_fraction(value) for value in bounds)
    _require(result[0] < result[1] and result[2] < result[3], "positive rectangle")
    return result


def _volume(rectangle):
    if rectangle is None:
        return Fraction(0)
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2]) / 2


def _intersection(a, b):
    result = (max(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), min(a[3], b[3]))
    return result if result[0] < result[1] and result[2] < result[3] else None


def _contains(parent, child):
    return (
        parent[0] <= child[0] <= child[1] <= parent[1]
        and parent[2] <= child[2] <= child[3] <= parent[3]
    )


def _nodes(rectangle):
    u0, u1, v0, v1 = rectangle
    us = ((u0, 1), ((u0 + u1) / 2, 4), (u1, 1))
    vs = ((v0, 1), ((v0 + v1) / 2, 4), (v1, 1))
    volume = _volume(rectangle)
    return tuple((u, v, volume * wu * wv / 36) for (u, wu), (v, wv) in product(us, vs))


def _raw_moments(rectangle):
    if rectangle is None:
        return (Fraction(0),) * 9
    nodes = _nodes(rectangle)
    return tuple(
        sum((weight * u**i * v**j for u, v, weight in nodes), Fraction(0))
        for i, j in product(range(3), repeat=2)
    )


def rectangle_moments(bounds):
    """Nine global raw moments, i outer/j inner, from exact tensor Simpson."""
    return [_wire(moment) for moment in _raw_moments(_rectangle(bounds))]


def _gram(moments):
    means = tuple(moments[3 * i + j] for i, j in EXPONENTS)
    gram = tuple(
        tuple(moments[3 * (i + k) + j + ell] for k, ell in EXPONENTS) for i, j in EXPONENTS
    )
    h = moments[0]
    _require(h > 0 and gram[0][0] == h, "positive tile Gram volume")
    for i, j in product(range(4), repeat=2):
        _require(gram[i][j] == gram[j][i], "Gram symmetry")
        if i == 0 or j == 0:
            _require(gram[i][j] - means[i] * means[j] / h == 0, "centered constant row")
    _require(gram[0][3] == gram[1][2], "repeated mixed moment")
    return means, gram


def _clamp_value(rectangle, u, v, incoming):
    if rectangle is None:
        return Fraction(0)
    u0, u1, v0, v1 = rectangle
    if incoming:
        first = max(Fraction(0), min(u1, u) - u0)
        second = max(Fraction(0), min(v1, v) - v0)
    else:
        first = max(Fraction(0), u1 - max(u0, u))
        second = max(Fraction(0), v1 - max(v0, v))
    return first * second / 2


def _corners(endpoint, tile, incoming):
    u0, u1, v0, v1 = tile
    f00 = _clamp_value(endpoint, u0, v0, incoming)
    f10 = _clamp_value(endpoint, u1, v0, incoming)
    f01 = _clamp_value(endpoint, u0, v1, incoming)
    f11 = _clamp_value(endpoint, u1, v1, incoming)
    mixed = (f11 - f10 - f01 + f00) / ((u1 - u0) * (v1 - v0))
    linear_u = (f10 - f00) / (u1 - u0) - mixed * v0
    linear_v = (f01 - f00) / (v1 - v0) - mixed * u0
    constant = f00 - linear_u * u0 - linear_v * v0 - mixed * u0 * v0
    return (constant, linear_u, linear_v, mixed)


def _dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def _tile(rectangle, clips, moment_function, counts):
    nodes = _nodes(rectangle)
    moments = moment_function(rectangle)
    means, gram = _gram(moments)
    coefficients, values, integrals = {}, {}, {}
    output = {
        "bounds": [_wire(value) for value in rectangle],
        "moments": [_wire(value) for value in moments],
    }
    for incoming, name in ((True, "incoming"), (False, "outgoing")):
        coefficients[name], values[name], integrals[name] = {}, {}, {}
        rows = []
        for event, endpoint in clips.items():
            vector = _corners(endpoint, rectangle, incoming)
            nodal = tuple(_clamp_value(endpoint, u, v, incoming) for u, v, _ in nodes)
            for (u, v, _), direct in zip(nodes, nodal, strict=True):
                _require(
                    _dot(vector, (1, u, v, u * v)) == direct,
                    "corner interpolation on declared tile",
                )
            direct_integral = sum(
                (weight * value for (_, _, weight), value in zip(nodes, nodal, strict=True)),
                Fraction(0),
            )
            _require(_dot(vector, means) == direct_integral, "pair moment/direct agreement")
            coefficients[name][event] = vector
            values[name][event] = nodal
            integrals[name][event] = direct_integral
            rows.append({"event": event, "coefficients": [_wire(value) for value in vector]})
        output[name] = rows
    gram_outgoing = {
        event: tuple(_dot(row, vector) for row in gram)
        for event, vector in coefficients["outgoing"].items()
    }
    triples = {}
    for first, last in product(clips, repeat=2):
        direct = sum(
            (
                weight * left * right
                for (_, _, weight), left, right in zip(
                    nodes, values["incoming"][first], values["outgoing"][last], strict=True
                )
            ),
            Fraction(0),
        )
        contracted = _dot(coefficients["incoming"][first], gram_outgoing[last])
        _require(contracted == direct, "triple moment/direct agreement")
        triples[first, last] = direct
    counts["tiles"] += 1
    counts["tile_bound_entries"] += 4
    counts["tile_moment_entries"] += 9
    counts["coefficient_vectors"] += 2 * len(clips)
    counts["coefficient_entries"] += 8 * len(clips)
    return {
        "nodes": nodes,
        "moments": moments,
        "values": values,
        "integrals": integrals,
        "T": triples,
        "h": moments[0],
    }, output


def _middle(event, clips, moment_function, counts):
    rectangle = clips[event]
    whole_moments = moment_function(rectangle)
    output = {
        "event": event,
        "bounds": None,
        "u_breaks": [],
        "v_breaks": [],
        "moments": [_wire(value) for value in whole_moments],
        "tiles": [],
    }
    counts["middle_cells"] += 1
    counts["middle_moment_entries"] += 9
    tiles = []
    if rectangle is not None:
        u0, u1, v0, v1 = rectangle
        u_breaks, v_breaks = {u0, u1}, {v0, v1}
        for endpoint in clips.values():
            if endpoint is not None:
                u_breaks.update(x for x in endpoint[:2] if u0 < x < u1)
                v_breaks.update(x for x in endpoint[2:] if v0 < x < v1)
        u_breaks, v_breaks = sorted(u_breaks), sorted(v_breaks)
        _require((len(u_breaks) - 1) * (len(v_breaks) - 1) <= 289, "bounded shared tile grid")
        output["bounds"] = [_wire(value) for value in rectangle]
        output["u_breaks"] = [_wire(value) for value in u_breaks]
        output["v_breaks"] = [_wire(value) for value in v_breaks]
        counts["positive_middle_cells"] += 1
        counts["middle_bound_entries"] += 4
        counts["breakpoint_entries"] += len(u_breaks) + len(v_breaks)
        for (left, right), (bottom, top) in product(pairwise(u_breaks), pairwise(v_breaks)):
            tile, row = _tile((left, right, bottom, top), clips, moment_function, counts)
            tiles.append(tile)
            output["tiles"].append(row)
    summed = tuple(
        sum((tile["moments"][index] for tile in tiles), Fraction(0)) for index in range(9)
    )
    _require(summed == whole_moments, "tile/whole global moment additivity")
    incoming = {
        endpoint: sum((tile["integrals"]["incoming"][endpoint] for tile in tiles), Fraction(0))
        for endpoint in clips
    }
    outgoing = {
        endpoint: sum((tile["integrals"]["outgoing"][endpoint] for tile in tiles), Fraction(0))
        for endpoint in clips
    }
    return {
        "h": whole_moments[0],
        "moments": whole_moments,
        "tiles": tiles,
        "incoming": incoming,
        "outgoing": outgoing,
    }, output


def _signed(counts, prefix, error):
    if error is not None:
        sign = "positive" if error > 0 else "negative" if error < 0 else "zero"
        counts[prefix + "_" + sign + "_errors"] += 1


def _geometry(cells, query, moment_function, counts):
    clips = {event: _intersection(rectangle, query) for event, rectangle in cells}
    volumes = {event: _volume(rectangle) for event, rectangle in clips.items()}
    middles, middle_rows = {}, []
    for event in clips:
        middles[event], row = _middle(event, clips, moment_function, counts)
        middle_rows.append(row)
    pairs = []
    for first, second in product(clips, repeat=2):
        integral = middles[second]["incoming"][first]
        _require(integral == middles[first]["outgoing"][second], "independent pair orientations")
        denominator = volumes[first] * volumes[second]
        pairs.append(
            {
                "first": first,
                "second": second,
                "clipped_product": _wire(denominator),
                "causal_integral": _wire(integral),
                "conditional": _wire(integral / denominator if denominator else None),
            }
        )
        counts["level_pairs"] += 1
    true_values, triple_rows = {}, []
    original_sum = tile_sum = Fraction(0)
    for first, middle, last in product(clips, repeat=3):
        source = middles[middle]
        h = source["h"]
        incoming, outgoing = source["incoming"][first], source["outgoing"][last]
        integral = sum((tile["T"][first, last] for tile in source["tiles"]), Fraction(0))
        denominator = volumes[first] * h * volumes[last]
        original = tile_product = centered = within_centered = covariance = None
        original_error = tile_error = between_error = None
        if h:
            original = incoming * outgoing / h
            tile_product = centered = within_centered = Fraction(0)
            mean_in, mean_out = incoming / h, outgoing / h
            for tile in source["tiles"]:
                local_in = tile["integrals"]["incoming"][first] / tile["h"]
                local_out = tile["integrals"]["outgoing"][last] / tile["h"]
                tile_product += tile["h"] * local_in * local_out
                for (_, _, weight), left, right in zip(
                    tile["nodes"],
                    tile["values"]["incoming"][first],
                    tile["values"]["outgoing"][last],
                    strict=True,
                ):
                    centered += weight * (left - mean_in) * (right - mean_out)
                    within_centered += weight * (left - local_in) * (right - local_out)
            _require(centered == integral - original, "direct whole-centered clamp identity")
            _require(
                within_centered == integral - tile_product, "direct tile-centered clamp identity"
            )
            covariance = centered / h
            original_error, tile_error, between_error = (
                original - integral,
                tile_product - integral,
                original - tile_product,
            )
            _require(original_error == tile_error + between_error, "mean-only error decomposition")
            original_sum += original
            tile_sum += tile_product
        else:
            _require(integral == 0 and incoming == 0 and outgoing == 0, "empty middle measure")
        true_values[first, middle, last] = integral
        triple_rows.append(
            {
                "first": first,
                "middle": middle,
                "last": last,
                "volume_product": _wire(denominator),
                "causal_integral": _wire(integral),
                "pair_product": _wire(original),
                "product_error": _wire(original_error),
                "conditional": _wire(integral / denominator if denominator else None),
                "product_conditional": _wire(original / denominator if denominator else None),
                "middle_covariance": _wire(covariance),
                "tile_pair_product": _wire(tile_product),
                "tile_product_error": _wire(tile_error),
                "between_tile_error": _wire(between_error),
                "tile_product_conditional": _wire(
                    tile_product / denominator if denominator else None
                ),
                "centered_integral": _wire(centered),
                "within_tile_centered_integral": _wire(within_centered),
            }
        )
        counts["level_triples"] += 1
        counts["zero_middle_level_triples"] += int(not h)
        counts["undefined_level_conditionals"] += int(not denominator)
        counts["positive_triples"] += int(integral > 0)
        for prefix, error in (
            ("original", original_error),
            ("tile", tile_error),
            ("between", between_error),
        ):
            _signed(counts, prefix, error)
    volume = _volume(query)
    true_sum = sum(true_values.values(), Fraction(0))
    _require(
        sum((middles[b]["incoming"][a] for a, b in product(clips, repeat=2)), Fraction(0))
        == volume**2 / 4,
        "complete pair integral",
    )
    _require(true_sum == volume**3 / 36, "complete shared-middle triple integral")
    output = {
        "volume": _wire(volume),
        "cells": [
            {"event": event, "clipped_volume": _wire(value)} for event, value in volumes.items()
        ],
        "middles": middle_rows,
        "pairs": pairs,
        "triples": triple_rows,
        "summary": {
            "true_integral": _wire(true_sum),
            "continuum_integral": _wire(volume**3 / 36),
            "original_product_sum": _wire(original_sum),
            "tile_product_sum": _wire(tile_sum),
            "original_error": _wire(original_sum - true_sum),
            "tile_error": _wire(tile_sum - true_sum),
            "between_error": _wire(original_sum - tile_sum),
        },
    }
    return {
        "moments": {event: row["moments"] for event, row in middles.items()},
        "T": true_values,
    }, output


def _prepare(problem):
    _object(problem, ("family", "probes", "levels"))
    _label(problem["family"])
    _require(
        type(problem["probes"]) is list and 1 <= len(problem["probes"]) <= 5, "probe inventory"
    )
    probes = []
    for row in problem["probes"]:
        _object(row, ("name", "bounds"))
        probes.append((_label(row["name"]), _rectangle(row["bounds"])))
    _require(len({name for name, _ in probes}) == len(probes), "unique probe names")
    _require(type(problem["levels"]) is list and len(problem["levels"]) == 3, "three levels")
    levels = []
    for row in problem["levels"]:
        _object(row, ("level", "cells"))
        name = _label(row["level"])
        _require(type(row["cells"]) is list and 1 <= len(row["cells"]) <= 8, "cell inventory")
        cells = []
        for cell in row["cells"]:
            _object(cell, ("event", "bounds"))
            cells.append((_integer(cell["event"]), _rectangle(cell["bounds"])))
        ids = [event for event, _ in cells]
        _require(ids == sorted(set(ids)), "ordered unique signed IDs")
        for (_, first), (_, second) in combinations(cells, 2):
            _require(_intersection(first, second) is None, "disjoint cell interiors")
        for _, query in probes:
            _require(
                sum(
                    (_volume(_intersection(rectangle, query)) for _, rectangle in cells),
                    Fraction(0),
                )
                == _volume(query),
                "query coverage",
            )
        levels.append((name, cells))
    _require(len({name for name, _ in levels}) == 3, "distinct level names")
    return probes, levels


def _lineage(coarse, fine):
    children = {event: [] for event, _ in coarse}
    for event, rectangle in fine:
        matches = [parent for parent, bounds in coarse if _contains(bounds, rectangle)]
        _require(len(matches) == 1, "unique full-rectangle parent")
        children[matches[0]].append(event)
    fine_lookup = dict(fine)
    for parent, rectangle in coarse:
        _require(
            sum((_volume(fine_lookup[child]) for child in children[parent]), Fraction(0))
            == _volume(rectangle),
            "complete local parent coverage",
        )
    return children


def build_family(problem):
    """Build the entire specified moment/geometry wire from supplied rectangles."""
    probes, levels = _prepare(problem)
    maps = {(i, j): _lineage(levels[i][1], levels[j][1]) for i, j in LINKS}
    for parent, direct in maps[0, 2].items():
        composed = sorted(child for middle in maps[0, 1][parent] for child in maps[1, 2][middle])
        _require(direct == composed, "direct/composed lineage")
    counts = dict.fromkeys(COUNT_KEYS, 0)
    counts["levels"], counts["probes"] = len(levels), len(probes)
    moment_function = cache(_raw_moments)
    calculated, level_rows = {}, []
    for index, (label, cells) in enumerate(levels):
        geometry = []
        for probe, query in probes:
            calculated[index, probe], output = _geometry(cells, query, moment_function, counts)
            geometry.append({"probe": probe, **output})
        level_rows.append({"level": label, "geometry": geometry})
    coarsenings, block_sums = [], {}
    for i, j in LINKS:
        descendants = maps[i, j]
        geometries = []
        for probe, _ in probes:
            coarse, fine = calculated[i, probe], calculated[j, probe]
            moment_blocks = []
            for parent, children in descendants.items():
                moments = tuple(
                    sum((fine["moments"][child][index] for child in children), Fraction(0))
                    for index in range(9)
                )
                _require(moments == coarse["moments"][parent], "full child moment additivity")
                moment_blocks.append(
                    {
                        "parent": parent,
                        "children": children[:],
                        "coarse_moments": [_wire(value) for value in coarse["moments"][parent]],
                        "child_moment_sum": [_wire(value) for value in moments],
                    }
                )
                counts["coarsening_moment_blocks"] += 1
                counts["coarsening_moment_entries"] += 18
            blocks, sums = [], {}
            for first, middle, last in product(descendants, repeat=3):
                children = list(product(descendants[first], descendants[middle], descendants[last]))
                value = sum((fine["T"][child] for child in children), Fraction(0))
                _require(value == coarse["T"][first, middle, last], "true child triple additivity")
                sums[first, middle, last] = value
                via = None
                if (i, j) == (0, 2):
                    via = sum(
                        (
                            block_sums[1, 2, probe][a, b, c]
                            for a, b, c in product(
                                maps[0, 1][first], maps[0, 1][middle], maps[0, 1][last]
                            )
                        ),
                        Fraction(0),
                    )
                    _require(via == value, "true via-middle block additivity")
                blocks.append(
                    {
                        "first": first,
                        "middle": middle,
                        "last": last,
                        "children": [list(child) for child in children],
                        "coarse_integral": _wire(coarse["T"][first, middle, last]),
                        "child_integral_sum": _wire(value),
                        "via_middle_integral": _wire(via),
                    }
                )
                counts["blocks"] += 1
                counts["child_terms"] += len(children)
            block_sums[i, j, probe] = sums
            geometries.append({"probe": probe, "moment_blocks": moment_blocks, "blocks": blocks})
        coarsenings.append(
            {
                "coarse": levels[i][0],
                "fine": levels[j][0],
                "parents": [
                    {"parent": parent, "children": children[:]}
                    for parent, children in descendants.items()
                ],
                "geometry": geometries,
            }
        )
    return {
        "problem": deepcopy(problem),
        "levels": level_rows,
        "coarsenings": coarsenings,
        "counts": counts,
    }
