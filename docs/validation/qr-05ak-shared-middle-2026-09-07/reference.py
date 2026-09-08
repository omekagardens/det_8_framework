"""Independent exact shared-middle calculus for supplied nested rectangles.

No files or other engines are read. Directed triple integrals use exact
Simpson panels of the piecewise-quadratic middle-point integrand. Primitive
caches belong to one build only; every retained block is formed independently
from the supplied geometry and the resulting fine-level measure tables.
"""

from copy import deepcopy
from fractions import Fraction
from functools import cache
from itertools import combinations, pairwise, product
from math import gcd

MAX_BITS = 4096
PATTERNS = ("all_equal", "first_middle", "first_last", "middle_last", "all_distinct")
LINKS = ((0, 1), (1, 2), (0, 2))
COUNT_NAMES = (
    "levels",
    "probes",
    "level_pairs",
    "level_triples",
    "blocks",
    "child_terms",
    "zero_middle_level_triples",
    "undefined_level_conditionals",
    "positive_level_errors",
    "zero_level_errors",
    "negative_level_errors",
    "zero_middle_blocks",
    "positive_between_errors",
    "zero_between_errors",
    "negative_between_errors",
    "positive_repeated_region_triples",
)


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _object(value, keys):
    _require(type(value) is dict and set(value) == set(keys), "exact object schema")


def _integer(value):
    _require(type(value) is int and value.bit_length() <= MAX_BITS, "bounded native integer")
    return value


def _rational(value):
    _require(type(value) is list and len(value) == 2, "native rational pair")
    numerator, denominator = map(_integer, value)
    _require(denominator > 0 and gcd(numerator, denominator) == 1, "reduced rational")
    return Fraction(numerator, denominator)


def _wire(value):
    if value is None:
        return None
    _require(type(value) in (int, Fraction), "exact retained value")
    fraction = Fraction(value)
    return [_integer(fraction.numerator), _integer(fraction.denominator)]


def _name(value):
    _require(type(value) is str and bool(value), "nonempty native label")
    return value


def _rect(value):
    _require(type(value) is list and len(value) == 4, "rectangle bounds")
    result = tuple(_rational(item) for item in value)
    _require(result[0] < result[1] and result[2] < result[3], "positive rectangle")
    return result


def _volume(rectangle):
    if rectangle is None:
        return Fraction(0)
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2]) / 2


def _intersection(first, second):
    rectangle = (
        max(first[0], second[0]),
        min(first[1], second[1]),
        max(first[2], second[2]),
        min(first[3], second[3]),
    )
    return rectangle if rectangle[0] < rectangle[1] and rectangle[2] < rectangle[3] else None


def _contains(parent, child):
    return (
        parent[0] <= child[0] <= child[1] <= parent[1]
        and parent[2] <= child[2] <= child[3] <= parent[3]
    )


def _endpoints(values):
    _require(all(type(value) in (int, Fraction) for value in values), "exact endpoints")
    values = tuple(Fraction(value) for value in values)
    _require(all(values[i] <= values[i + 1] for i in range(0, len(values), 2)), "ordered endpoints")
    return values


def causal_area(a, b, c, d):
    """Exact directed pair integral by trapezoids of affine incoming length."""
    a, b, c, d = _endpoints((a, b, c, d))
    if a == b or c == d:
        return Fraction(0)
    knots = sorted({c, d, *(point for point in (a, b) if c < point < d)})
    result = Fraction(0)
    for left, right in pairwise(knots):
        f_left = max(Fraction(0), min(b, left) - a)
        f_right = max(Fraction(0), min(b, right) - a)
        result += (right - left) * (f_left + f_right) / 2
    return result


def triple_area(a, b, c, d, e, f):
    """Exact x<y<z integral using quadratic Simpson panels in the SAME y."""
    a, b, c, d, e, f = _endpoints((a, b, c, d, e, f))
    if a == b or c == d or e == f:
        return Fraction(0)

    def integrand(y):
        incoming = max(Fraction(0), min(b, y) - a)
        outgoing = max(Fraction(0), f - max(e, y))
        return incoming * outgoing

    knots = sorted({c, d, *(point for point in (a, b, e, f) if c < point < d)})
    total = Fraction(0)
    for left, right in pairwise(knots):
        middle = (left + right) / 2
        total += (right - left) * (integrand(left) + 4 * integrand(middle) + integrand(right)) / 6
    return total


def _prepare(problem):
    _object(problem, ("family", "probes", "levels"))
    _name(problem["family"])
    _require(
        type(problem["probes"]) is list and 1 <= len(problem["probes"]) <= 5, "probe inventory"
    )
    probes = []
    for row in problem["probes"]:
        _object(row, ("name", "bounds"))
        probes.append((_name(row["name"]), _rect(row["bounds"])))
    _require(len({name for name, _ in probes}) == len(probes), "unique probes")
    _require(type(problem["levels"]) is list and len(problem["levels"]) == 3, "three levels")
    levels = []
    for row in problem["levels"]:
        _object(row, ("level", "cells"))
        label = _name(row["level"])
        _require(type(row["cells"]) is list and 1 <= len(row["cells"]) <= 8, "cell inventory")
        cells = []
        for item in row["cells"]:
            _object(item, ("event", "bounds"))
            cells.append((_integer(item["event"]), _rect(item["bounds"])))
        ids = [event for event, _ in cells]
        _require(ids == sorted(set(ids)), "ordered unique level-local IDs")
        for (_, first), (_, second) in combinations(cells, 2):
            _require(_intersection(first, second) is None, "disjoint full cell interiors")
        for _, query in probes:
            _require(
                sum(
                    (_volume(_intersection(rectangle, query)) for _, rectangle in cells),
                    Fraction(0),
                )
                == _volume(query),
                "complete query coverage",
            )
        levels.append((label, cells))
    _require(len({label for label, _ in levels}) == 3, "distinct level labels")
    return probes, levels


def _children(coarse, fine):
    descendants = {event: [] for event, _ in coarse}
    for child_id, child_rectangle in fine:
        candidates = [event for event, rectangle in coarse if _contains(rectangle, child_rectangle)]
        _require(len(candidates) == 1, "unique full-cell containment")
        descendants[candidates[0]].append(child_id)
    fine_rectangles = dict(fine)
    for event, rectangle in coarse:
        total = sum((_volume(fine_rectangles[child]) for child in descendants[event]), Fraction(0))
        _require(total == _volume(rectangle), "complete local parent coverage")
    return descendants


def _sign_count(counts, value, suffix):
    if value is None:
        return
    sign = "positive" if value > 0 else "negative" if value < 0 else "zero"
    counts[sign + suffix] += 1


def _geometry(cells, query, pair_primitive, triple_primitive, counts):
    clips = {event: _intersection(rectangle, query) for event, rectangle in cells}
    h = {event: _volume(rectangle) for event, rectangle in clips.items()}
    pairs, pair_rows = {}, []
    for first, second in product(clips, repeat=2):
        left, right = clips[first], clips[second]
        denominator = h[first] * h[second]
        integral = Fraction(0)
        if left is not None and right is not None:
            integral = (
                pair_primitive(*left[:2], *right[:2]) * pair_primitive(*left[2:], *right[2:]) / 4
            )
        _require(0 <= integral <= denominator, "pair submeasure")
        if first == second:
            _require(integral == denominator / 4, "same-region pair")
        pairs[first, second] = integral
        pair_rows.append(
            {
                "first": first,
                "second": second,
                "clipped_product": _wire(denominator),
                "causal_integral": _wire(integral),
                "conditional": _wire(integral / denominator if denominator else None),
            }
        )
        counts["level_pairs"] += 1
    triples, pair_products, conditionals = {}, {}, {}
    triple_rows = []
    for first, middle, last in product(clips, repeat=3):
        rectangles = (clips[first], clips[middle], clips[last])
        denominator = h[first] * h[middle] * h[last]
        integral = Fraction(0)
        if all(rectangle is not None for rectangle in rectangles):
            one, two, three = rectangles
            integral = (
                triple_primitive(*one[:2], *two[:2], *three[:2])
                * triple_primitive(*one[2:], *two[2:], *three[2:])
                / 8
            )
        _require(0 <= integral <= denominator, "triple submeasure")
        if first == middle == last:
            _require(integral == denominator / 36, "same-region triple")
        projected = pairs[first, middle] * pairs[middle, last] / h[middle] if h[middle] else None
        error = projected - integral if projected is not None else None
        conditional = integral / denominator if denominator else None
        key = (first, middle, last)
        triples[key], pair_products[key], conditionals[key] = integral, projected, conditional
        triple_rows.append(
            {
                "first": first,
                "middle": middle,
                "last": last,
                "volume_product": _wire(denominator),
                "causal_integral": _wire(integral),
                "pair_product": _wire(projected),
                "product_error": _wire(error),
                "conditional": _wire(conditional),
                "product_conditional": _wire(projected / denominator if denominator else None),
                "middle_covariance": _wire(-error / h[middle] if h[middle] else None),
            }
        )
        counts["level_triples"] += 1
        counts["zero_middle_level_triples"] += int(h[middle] == 0)
        counts["undefined_level_conditionals"] += int(denominator == 0)
        counts["positive_repeated_region_triples"] += int(integral > 0 and len(set(key)) < 3)
        _sign_count(counts, error, "_level_errors")
    volume = _volume(query)
    true_integral = sum(triples.values(), Fraction(0))
    projected_sum = sum(
        (value for value in pair_products.values() if value is not None), Fraction(0)
    )
    _require(sum(pairs.values(), Fraction(0)) == volume**2 / 4, "complete pair measure")
    _require(true_integral == volume**3 / 36, "complete triple measure")
    wire = {
        "volume": _wire(volume),
        "cells": [{"event": event, "clipped_volume": _wire(value)} for event, value in h.items()],
        "pairs": pair_rows,
        "triples": triple_rows,
        "summary": {
            "true_integral": _wire(true_integral),
            "continuum_integral": _wire(volume**3 / 36),
            "extended_product_sum": _wire(projected_sum),
            "product_error": _wire(projected_sum - true_integral),
        },
    }
    return {"h": h, "J": pairs, "T": triples, "P": pair_products, "C": conditionals}, wire


def _pattern(a, b, c):
    if a == b == c:
        return "all_equal"
    if a == b:
        return "first_middle"
    if a == c:
        return "first_last"
    if b == c:
        return "middle_last"
    return "all_distinct"


def _block(first, middle, last, descendants, coarse, fine, counts):
    left, center, right = (descendants[event] for event in (first, middle, last))
    child_ids = list(product(left, center, right))
    patterns = dict.fromkeys(PATTERNS, Fraction(0))
    child_integral = Fraction(0)
    child_projected = Fraction(0)
    zero_middle = 0
    denominator = coarse["h"][first] * coarse["h"][middle] * coarse["h"][last]
    weighted = Fraction(0) if denominator else None
    for a, b, c in child_ids:
        integral = fine["T"][a, b, c]
        child_integral += integral
        patterns[_pattern(a, b, c)] += integral
        if fine["h"][b]:
            child_projected += fine["P"][a, b, c]
        else:
            zero_middle += 1
            _require(integral == 0 and fine["P"][a, b, c] is None, "zero-middle child")
        child_product = fine["h"][a] * fine["h"][b] * fine["h"][c]
        if child_product:
            _require(denominator > 0, "positive parent product")
            weighted += child_product / denominator * fine["C"][a, b, c]
    key = (first, middle, last)
    integral, projected, conditional = coarse["T"][key], coarse["P"][key], coarse["C"][key]
    _require(child_integral == integral, "true triple block additivity")
    _require(sum(patterns.values(), Fraction(0)) == child_integral, "equality pattern partition")
    _require(weighted == conditional, "normalized true triple block")
    endpoint = refined_middle = error = within = between = None
    if coarse["h"][middle]:
        endpoint = Fraction(0)
        for a, c in product(left, right):
            j_a_middle = sum((fine["J"][a, b] for b in center), Fraction(0))
            j_middle_c = sum((fine["J"][b, c] for b in center), Fraction(0))
            endpoint += j_a_middle * j_middle_c / coarse["h"][middle]
        refined_middle = Fraction(0)
        for b in center:
            if fine["h"][b]:
                incoming = sum((fine["J"][a, b] for a in left), Fraction(0))
                outgoing = sum((fine["J"][b, c] for c in right), Fraction(0))
                refined_middle += incoming * outgoing / fine["h"][b]
        _require(endpoint == projected, "endpoint-only product refinement")
        _require(refined_middle == child_projected, "middle-only product refinement")
        error = projected - integral
        within = child_projected - integral
        between = projected - child_projected
        _require(error == within + between, "within-between accounting")
    else:
        _require(child_integral == 0 and child_projected == 0, "zero-middle parent block")
        child_projected = None
    counts["blocks"] += 1
    counts["child_terms"] += len(child_ids)
    counts["zero_middle_blocks"] += int(coarse["h"][middle] == 0)
    _sign_count(counts, between, "_between_errors")
    return {
        "first": first,
        "middle": middle,
        "last": last,
        "children": [list(ids) for ids in child_ids],
        "zero_middle_children": zero_middle,
        "coarse_integral": _wire(integral),
        "child_integral_sum": _wire(child_integral),
        "child_pattern_integrals": {name: _wire(value) for name, value in patterns.items()},
        "coarse_conditional": _wire(conditional),
        "weighted_child_conditional": _wire(weighted),
        "coarse_pair_product": _wire(projected),
        "child_pair_product_sum": _wire(child_projected),
        "endpoint_refined_product": _wire(endpoint),
        "middle_refined_product": _wire(refined_middle),
        "coarse_product_error": _wire(error),
        "within_child_error": _wire(within),
        "between_child_error": _wire(between),
        "via_middle_integral": None,
    }, child_integral


def build_family(problem):
    """Construct the full protocol wire; this is a bounded private diagnostic."""
    probes, levels = _prepare(problem)
    maps = {(i, j): _children(levels[i][1], levels[j][1]) for i, j in LINKS}
    for parent, children in maps[0, 2].items():
        composed = sorted(child for middle in maps[0, 1][parent] for child in maps[1, 2][middle])
        _require(children == composed, "composed full-rectangle lineage")
    counts = dict.fromkeys(COUNT_NAMES, 0)
    counts["levels"], counts["probes"] = len(levels), len(probes)
    pair_primitive, triple_primitive = cache(causal_area), cache(triple_area)
    numerical, level_rows = {}, []
    for index, (label, cells) in enumerate(levels):
        geometries = []
        for probe, query in probes:
            numerical[index, probe], geometry = _geometry(
                cells, query, pair_primitive, triple_primitive, counts
            )
            geometries.append({"probe": probe, **geometry})
        level_rows.append({"level": label, "geometry": geometries})
    coarsenings, block_sums = [], {}
    for coarse_index, fine_index in LINKS:
        descendants = maps[coarse_index, fine_index]
        geometry_rows = []
        for probe, _ in probes:
            coarse, fine = numerical[coarse_index, probe], numerical[fine_index, probe]
            volumes = []
            for parent, children in descendants.items():
                volume_sum = sum((fine["h"][child] for child in children), Fraction(0))
                _require(volume_sum == coarse["h"][parent], "clipped parent volume")
                volumes.append(
                    {
                        "parent": parent,
                        "coarse_volume": _wire(coarse["h"][parent]),
                        "child_volume_sum": _wire(volume_sum),
                    }
                )
            blocks, current_sums = [], {}
            for first, middle, last in product(descendants, repeat=3):
                row, true_sum = _block(first, middle, last, descendants, coarse, fine, counts)
                current_sums[first, middle, last] = true_sum
                if (coarse_index, fine_index) == (0, 2):
                    via_middle = sum(
                        (
                            block_sums[1, 2, probe][a, b, c]
                            for a, b, c in product(
                                maps[0, 1][first], maps[0, 1][middle], maps[0, 1][last]
                            )
                        ),
                        Fraction(0),
                    )
                    _require(via_middle == true_sum, "true triple via-middle aggregation")
                    row["via_middle_integral"] = _wire(via_middle)
                blocks.append(row)
            block_sums[coarse_index, fine_index, probe] = current_sums
            geometry_rows.append({"probe": probe, "volumes": volumes, "blocks": blocks})
        coarsenings.append(
            {
                "coarse": levels[coarse_index][0],
                "fine": levels[fine_index][0],
                "parents": [
                    {"parent": parent, "children": children[:]}
                    for parent, children in descendants.items()
                ],
                "geometry": geometry_rows,
            }
        )
    return {
        "problem": deepcopy(problem),
        "levels": level_rows,
        "coarsenings": coarsenings,
        "counts": counts,
    }
