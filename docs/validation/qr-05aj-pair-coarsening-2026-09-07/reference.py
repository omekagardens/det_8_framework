"""Independent exact pair-measure coarsening on explicitly supplied rectangles.

This private bounded research implementation reads no files and imports no
other mathematical engine. Directed integrals use affine overlap trapezoids;
all lineage and block computations are derived from the input rectangles.
"""

from fractions import Fraction
from itertools import combinations, pairwise, product
from math import gcd

MAX_BITS = 4096


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _keys(value, names, context):
    _require(type(value) is dict and set(value) == set(names), context)


def _integer(value):
    _require(type(value) is int and value.bit_length() <= MAX_BITS, "native integer")
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
    _require(type(value) is str and bool(value), "nonempty native label")
    return value


def _copy(value):
    if type(value) is dict:
        _require(all(type(key) is str for key in value), "native object keys")
        return {key: _copy(item) for key, item in value.items()}
    if type(value) is list:
        return [_copy(item) for item in value]
    _require(type(value) in (str, int, bool) or value is None, "native JSON value")
    if type(value) is int:
        _integer(value)
    return value


def _rectangle(value):
    _require(type(value) is list and len(value) == 4, "rectangle bounds")
    result = tuple(_fraction(item) for item in value)
    _require(result[0] < result[1] and result[2] < result[3], "positive rectangle")
    return result


def _volume(rectangle):
    if rectangle is None:
        return Fraction(0)
    return (rectangle[1] - rectangle[0]) * (rectangle[3] - rectangle[2]) / 2


def _clip(left, right):
    bounds = (
        max(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        min(left[3], right[3]),
    )
    if bounds[0] >= bounds[1] or bounds[2] >= bounds[3]:
        return None
    return bounds


def _contains(parent, child):
    return (
        parent[0] <= child[0] <= child[1] <= parent[1]
        and parent[2] <= child[2] <= child[3] <= parent[3]
    )


def causal_area(a, b, c, d):
    """Integrate 1(x<y), x in [a,b], y in [c,d], by affine y-segments."""
    _require(all(type(x) in (int, Fraction) for x in (a, b, c, d)), "exact endpoints")
    a, b, c, d = (Fraction(x) for x in (a, b, c, d))
    _require(a <= b and c <= d, "ordered interval endpoints")
    if a == b or c == d:
        return Fraction(0)
    knots = sorted({c, d, *(point for point in (a, b) if c < point < d)})
    total = Fraction(0)
    for start, end in pairwise(knots):
        left_length = max(Fraction(0), min(b, start) - a)
        right_length = max(Fraction(0), min(b, end) - a)
        total += (end - start) * (left_length + right_length) / 2
    return total


def _pair_measure(first, second):
    if first is None or second is None:
        return Fraction(0)
    return (
        causal_area(first[0], first[1], second[0], second[1])
        * causal_area(first[2], first[3], second[2], second[3])
        / 4
    )


def _prepare(problem):
    _keys(problem, ("family", "probes", "levels"), "problem schema")
    _label(problem["family"])
    _require(type(problem["probes"]) is list and 1 <= len(problem["probes"]) <= 5, "probes")
    probes = []
    for row in problem["probes"]:
        _keys(row, ("name", "bounds"), "probe schema")
        probes.append((_label(row["name"]), _rectangle(row["bounds"])))
    _require(len({name for name, _ in probes}) == len(probes), "unique probes")
    _require(type(problem["levels"]) is list and len(problem["levels"]) == 3, "three levels")
    levels = []
    for row in problem["levels"]:
        _keys(row, ("level", "cells"), "level schema")
        name = _label(row["level"])
        _require(type(row["cells"]) is list and 1 <= len(row["cells"]) <= 8, "cells")
        cells = []
        for item in row["cells"]:
            _keys(item, ("event", "bounds", "supplied_mark"), "cell schema")
            event = _integer(item["event"])
            rectangle = _rectangle(item["bounds"])
            mark = _fraction(item["supplied_mark"])
            _require(mark > 0, "positive supplied mark")
            cells.append({"id": event, "rectangle": rectangle, "mark": mark})
        ids = [cell["id"] for cell in cells]
        _require(ids == sorted(set(ids)), "unique event-ordered cells")
        for left, right in combinations(cells, 2):
            _require(
                _clip(left["rectangle"], right["rectangle"]) is None, "disjoint cell interiors"
            )
        for _, query in probes:
            covered = sum((_volume(_clip(cell["rectangle"], query)) for cell in cells), Fraction(0))
            _require(covered == _volume(query), "query coverage")
        levels.append((name, cells))
    _require(len({name for name, _ in levels}) == 3, "distinct level labels")
    return probes, levels


def _lineage(coarse_cells, fine_cells):
    children = {cell["id"]: [] for cell in coarse_cells}
    for child in fine_cells:
        parents = [
            parent for parent in coarse_cells if _contains(parent["rectangle"], child["rectangle"])
        ]
        _require(len(parents) == 1, "unique full-rectangle parent")
        children[parents[0]["id"]].append(child["id"])
    fine_lookup = {cell["id"]: cell for cell in fine_cells}
    for parent in coarse_cells:
        descendants = [fine_lookup[event] for event in children[parent["id"]]]
        _require(
            sum((_volume(child["rectangle"]) for child in descendants), Fraction(0))
            == _volume(parent["rectangle"]),
            "complete parent coverage",
        )
    return children


def _geometry(cells, query):
    clips = {cell["id"]: _clip(cell["rectangle"], query) for cell in cells}
    volumes = {event: _volume(rectangle) for event, rectangle in clips.items()}
    integrals = {}
    conditionals = {}
    for first, second in product(clips, repeat=2):
        value = _pair_measure(clips[first], clips[second])
        denominator = volumes[first] * volumes[second]
        _require(0 <= value <= denominator, "causal submeasure")
        if first == second:
            _require(value == denominator / 4, "same-cell pair measure")
        integrals[first, second] = value
        conditionals[first, second] = value / denominator if denominator else None
    _require(
        sum(integrals.values(), Fraction(0)) == _volume(query) ** 2 / 4, "complete causal measure"
    )
    return {"volumes": volumes, "integrals": integrals, "conditionals": conditionals}


def _middle_reconstruction(first, second, lower_map, upper_map, fine_geometry):
    middle_ids = lower_map[first] + ([] if first == second else lower_map[second])
    volumes = {
        middle: sum((fine_geometry["volumes"][child] for child in upper_map[middle]), Fraction(0))
        for middle in middle_ids
    }
    first_volume = sum((volumes[middle] for middle in lower_map[first]), Fraction(0))
    second_volume = sum((volumes[middle] for middle in lower_map[second]), Fraction(0))
    denominator = first_volume * second_volume
    measure = Fraction(0)
    normalized = Fraction(0) if denominator else None
    for left, right in product(lower_map[first], lower_map[second]):
        middle_measure = sum(
            (
                fine_geometry["integrals"][a, b]
                for a, b in product(upper_map[left], upper_map[right])
            ),
            Fraction(0),
        )
        measure += middle_measure
        middle_product = volumes[left] * volumes[right]
        if middle_product:
            _require(denominator > 0, "positive middle denominator")
            middle_conditional = middle_measure / middle_product
            normalized += middle_product / denominator * middle_conditional
        else:
            _require(middle_measure == 0, "zero-volume middle measure")
    return measure, normalized


def build_family(problem):
    """Recompute the complete specified pair-coarsening wire from supplied data."""
    probes, levels = _prepare(problem)
    links = ((0, 1), (1, 2), (0, 2))
    maps = {(i, j): _lineage(levels[i][1], levels[j][1]) for i, j in links}
    for parent, children in maps[0, 2].items():
        composed = sorted(child for middle in maps[0, 1][parent] for child in maps[1, 2][middle])
        _require(children == composed, "direct/composed lineage")
    counts = dict.fromkeys(
        (
            "levels",
            "probes",
            "level_pairs",
            "blocks",
            "child_terms",
            "undefined_level_pairs",
            "undefined_blocks",
            "unweighted_mismatches",
            "annotation_mismatches",
            "diagonal_omission_mismatches",
            "cross_child_omission_mismatches",
        ),
        0,
    )
    counts["levels"] = len(levels)
    counts["probes"] = len(probes)
    calculated = {}
    level_output = []
    for index, (name, cells) in enumerate(levels):
        geometry_rows = []
        for probe, query in probes:
            geometry = _geometry(cells, query)
            calculated[index, probe] = geometry
            pairs = []
            for first, second in product(geometry["volumes"], repeat=2):
                conditional = geometry["conditionals"][first, second]
                pairs.append(
                    {
                        "first": first,
                        "second": second,
                        "clipped_product": _wire(
                            geometry["volumes"][first] * geometry["volumes"][second]
                        ),
                        "causal_integral": _wire(geometry["integrals"][first, second]),
                        "conditional": _wire(conditional),
                    }
                )
                counts["level_pairs"] += 1
                counts["undefined_level_pairs"] += int(conditional is None)
            geometry_rows.append(
                {
                    "probe": probe,
                    "volume": _wire(_volume(query)),
                    "cells": [
                        {"event": event, "clipped_volume": _wire(volume)}
                        for event, volume in geometry["volumes"].items()
                    ],
                    "pairs": pairs,
                }
            )
        level_output.append({"level": name, "geometry": geometry_rows})
    coarsenings = []
    for coarse_index, fine_index in links:
        descendants = maps[coarse_index, fine_index]
        fine_cells = {cell["id"]: cell for cell in levels[fine_index][1]}
        probe_rows = []
        for probe, _ in probes:
            coarse = calculated[coarse_index, probe]
            fine = calculated[fine_index, probe]
            volume_rows = []
            for parent, children in descendants.items():
                total = sum((fine["volumes"][child] for child in children), Fraction(0))
                _require(total == coarse["volumes"][parent], "clipped volume block")
                volume_rows.append(
                    {
                        "parent": parent,
                        "coarse_volume": _wire(coarse["volumes"][parent]),
                        "child_volume_sum": _wire(total),
                    }
                )
            annotation = {
                event: cell["mark"] * fine["volumes"][event] / _volume(cell["rectangle"])
                for event, cell in fine_cells.items()
            }
            blocks = []
            for first, second in product(descendants, repeat=2):
                block_pairs = list(product(descendants[first], descendants[second]))
                denominator = coarse["volumes"][first] * coarse["volumes"][second]
                annotation_denominator = sum(
                    (annotation[a] * annotation[b] for a, b in block_pairs), Fraction(0)
                )
                _require(bool(denominator) == bool(annotation_denominator), "annotation support")
                child_measure = Fraction(0)
                diagonal_measure = Fraction(0)
                offdiagonal_measure = Fraction(0)
                normalized = Fraction(0) if denominator else None
                annotated = Fraction(0) if annotation_denominator else None
                defined_conditionals = []
                child_rows = []
                for a, b in block_pairs:
                    counts["child_terms"] += 1
                    geometric_weight = (
                        fine["volumes"][a] * fine["volumes"][b] / denominator
                        if denominator
                        else None
                    )
                    annotation_weight = (
                        annotation[a] * annotation[b] / annotation_denominator
                        if annotation_denominator
                        else None
                    )
                    child_rows.append(
                        {
                            "first": a,
                            "second": b,
                            "geometric_weight": _wire(geometric_weight),
                            "annotation_weight": _wire(annotation_weight),
                        }
                    )
                    integral = fine["integrals"][a, b]
                    child_measure += integral
                    if a == b:
                        diagonal_measure += integral
                    else:
                        offdiagonal_measure += integral
                    conditional = fine["conditionals"][a, b]
                    if conditional is not None:
                        defined_conditionals.append(conditional)
                        normalized += geometric_weight * conditional
                        annotated += annotation_weight * conditional
                unweighted = (
                    sum(defined_conditionals, Fraction(0)) / len(defined_conditionals)
                    if defined_conditionals
                    else None
                )
                coarse_measure = coarse["integrals"][first, second]
                coarse_conditional = coarse["conditionals"][first, second]
                _require(child_measure == coarse_measure, "causal measure block")
                _require(
                    diagonal_measure + offdiagonal_measure == child_measure,
                    "diagonal decomposition",
                )
                _require(normalized == coarse_conditional, "geometric conditional block")
                via_measure = via_conditional = None
                if (coarse_index, fine_index) == (0, 2):
                    via_measure, via_conditional = _middle_reconstruction(
                        first, second, maps[0, 1], maps[1, 2], fine
                    )
                    _require(
                        via_measure == child_measure and via_conditional == normalized,
                        "via-middle agreement",
                    )
                blocks.append(
                    {
                        "first": first,
                        "second": second,
                        "children": child_rows,
                        "coarse_integral": _wire(coarse_measure),
                        "child_integral_sum": _wire(child_measure),
                        "child_diagonal_integral": _wire(diagonal_measure),
                        "child_offdiagonal_integral": _wire(offdiagonal_measure),
                        "coarse_conditional": _wire(coarse_conditional),
                        "weighted_child_conditional": _wire(normalized),
                        "unweighted_child_conditional": _wire(unweighted),
                        "annotation_weighted_child_conditional": _wire(annotated),
                        "via_middle_integral": _wire(via_measure),
                        "via_middle_conditional": _wire(via_conditional),
                    }
                )
                counts["blocks"] += 1
                counts["undefined_blocks"] += int(coarse_conditional is None)
                counts["unweighted_mismatches"] += int(unweighted != coarse_conditional)
                counts["annotation_mismatches"] += int(annotated != coarse_conditional)
                counts["diagonal_omission_mismatches"] += int(offdiagonal_measure != coarse_measure)
                counts["cross_child_omission_mismatches"] += int(diagonal_measure != coarse_measure)
            probe_rows.append({"probe": probe, "volumes": volume_rows, "blocks": blocks})
        coarsenings.append(
            {
                "coarse": levels[coarse_index][0],
                "fine": levels[fine_index][0],
                "parents": [
                    {"parent": parent, "children": children[:]}
                    for parent, children in descendants.items()
                ],
                "geometry": probe_rows,
            }
        )
    return {
        "problem": _copy(problem),
        "levels": level_output,
        "coarsenings": coarsenings,
        "counts": counts,
    }
