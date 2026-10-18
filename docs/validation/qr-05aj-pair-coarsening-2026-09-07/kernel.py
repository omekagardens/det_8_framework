"""Private exact coarsening of a supplied geometric causal pair measure.

All geometry is explicit input. Event IDs are level-local, and supplied marks
are used only for the declared incorrect annotation-weight candidate. This is
not a hardened production API and imports no other mathematical engine.
"""

import copy
import json
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd

LINKS = ((0, 1), (1, 2), (0, 2))


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    kind = type(value)
    if kind is int:
        _require(value.bit_length() <= 4096, "integer exceeds retained component bound")
    elif value is None or kind in (str, bool):
        return
    elif kind is list:
        for child in value:
            _native(child)
    elif kind is dict:
        _require(all(type(key) is str for key in value), "native string keys required")
        for child in value.values():
            _native(child)
    else:
        raise ValueError("exact native mathematical wire required")


def canonical(value):
    _native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")


def _fields(value, keys):
    _require(type(value) is dict and set(value) == set(keys), "unexpected fixture fields")


def _label(value):
    _require(type(value) is str and value, "nonempty native label required")
    return value


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


def _wire(value):
    if value is None:
        return None
    value = F(value)
    _require(
        max(value.numerator.bit_length(), value.denominator.bit_length()) <= 4096,
        "retained fraction exceeds component bound",
    )
    return [value.numerator, value.denominator]


def _rectangle(value):
    _require(type(value) is list and len(value) == 4, "four rectangle coordinates required")
    b = tuple(map(_fraction, value))
    _require(b[0] < b[1] and b[2] < b[3], "positive rectangle required")
    return b


def _area(b):
    return (b[1] - b[0]) * (b[3] - b[2]) / 2


def _contains(outer, inner):
    return (
        outer[0] <= inner[0]
        and inner[1] <= outer[1]
        and outer[2] <= inner[2]
        and inner[3] <= outer[3]
    )


def _clip(a, b):
    c = (max(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), min(a[3], b[3]))
    return c if c[0] < c[1] and c[2] < c[3] else None


def causal_area(a, b, c, d):
    """Directed interval integral, via exact positive-part antiderivatives."""
    _require(all(type(x) in (int, F) for x in (a, b, c, d)), "exact rational endpoints required")
    a, b, c, d = map(F, (a, b, c, d))
    _require(a <= b and c <= d, "reversed interval endpoints")
    positive_square = lambda x: max(F(0), x) ** 2
    answer = (
        positive_square(d - a)
        - positive_square(d - b)
        - positive_square(c - a)
        + positive_square(c - b)
    ) / 2
    _require(0 <= answer <= (b - a) * (d - c), "directed integral outside product volume")
    return answer


def _pair_integral(a, b):
    if a is None or b is None:
        return F(0)
    return causal_area(a[0], a[1], b[0], b[1]) * causal_area(a[2], a[3], b[2], b[3]) / 4


def _parse(problem):
    _native(problem)
    _fields(problem, ("family", "probes", "levels"))
    _label(problem["family"])
    _require(
        type(problem["probes"]) is list and 1 <= len(problem["probes"]) <= 5,
        "bounded probe inventory required",
    )
    probes, names = [], set()
    for q in problem["probes"]:
        _fields(q, ("name", "bounds"))
        name = _label(q["name"])
        _require(name not in names, "unique probe names required")
        names.add(name)
        probes.append({"name": name, "bounds": _rectangle(q["bounds"])})
    _require(
        type(problem["levels"]) is list and len(problem["levels"]) == 3,
        "exactly three levels required",
    )
    levels, names = [], set()
    for row in problem["levels"]:
        _fields(row, ("level", "cells"))
        name = _label(row["level"])
        _require(name not in names, "distinct level labels required")
        names.add(name)
        _require(
            type(row["cells"]) is list and 1 <= len(row["cells"]) <= 8,
            "bounded positive cell inventory required",
        )
        cells = []
        for c in row["cells"]:
            _fields(c, ("event", "bounds", "supplied_mark"))
            event = c["event"]
            _require(type(event) is int, "native level-local integer ID required")
            b, mark = _rectangle(c["bounds"]), _fraction(c["supplied_mark"])
            _require(mark > 0, "positive supplied mark required")
            cells.append({"event": event, "bounds": b, "mark": mark, "area": _area(b)})
        ids = [c["event"] for c in cells]
        _require(ids == sorted(set(ids)), "event-ordered unique cell IDs required")
        _require(
            all(_clip(a["bounds"], b["bounds"]) is None for a, b in combinations(cells, 2)),
            "cell interiors must be disjoint",
        )
        levels.append({"level": name, "cells": cells})
    return probes, levels


def _lineage(coarse, fine):
    """Map full rectangles; equal integer IDs across levels play no role."""
    groups = {cell["event"]: [] for cell in coarse["cells"]}
    inverse = {}
    for child in fine["cells"]:
        parents = [p for p in coarse["cells"] if _contains(p["bounds"], child["bounds"])]
        _require(len(parents) == 1, "each child requires one full-rectangle parent")
        parent = parents[0]["event"]
        groups[parent].append(child)
        inverse[child["event"]] = parent
    for parent in coarse["cells"]:
        children = groups[parent["event"]]
        _require(
            children and sum((c["area"] for c in children), F(0)) == parent["area"],
            "children must cover each parent, not only global area",
        )
    return groups, inverse


def _geometry(level, probes):
    out = []
    for q in probes:
        clips = {cell["event"]: _clip(cell["bounds"], q["bounds"]) for cell in level["cells"]}
        h = {event: _area(b) if b is not None else F(0) for event, b in clips.items()}
        volume = _area(q["bounds"])
        _require(sum(h.values(), F(0)) == volume, "cell clips must cover each positive query")
        pairs, total = [], F(0)
        for first, second in product(h, repeat=2):
            denominator = h[first] * h[second]
            integral = _pair_integral(clips[first], clips[second])
            conditional = integral / denominator if denominator else None
            _require(
                conditional is None or 0 <= conditional <= 1, "conditional outside unit interval"
            )
            if first == second:
                _require(integral == denominator / 4, "within-cell pair identity failed")
            total += integral
            pairs.append(
                {
                    "first": first,
                    "second": second,
                    "clipped_product": _wire(denominator),
                    "causal_integral": _wire(integral),
                    "conditional": _wire(conditional),
                }
            )
        _require(
            total == volume * volume / 4, "complete pair measure must match rectangle integral"
        )
        out.append(
            {
                "probe": q["name"],
                "volume": _wire(volume),
                "cells": [{"event": event, "clipped_volume": _wire(v)} for event, v in h.items()],
                "pairs": pairs,
            }
        )
    return {"level": level["level"], "geometry": out}


def _table(geometry):
    h = {c["event"]: _fraction(c["clipped_volume"]) for c in geometry["cells"]}
    pairs = {(r["first"], r["second"]): r for r in geometry["pairs"]}
    return h, pairs


def _via_middle(first, second, middle_groups, reconstructed):
    """Compose independently reconstructed l1<-l2 blocks, not stored l1 J."""
    volumes = {r["parent"]: _fraction(r["child_volume_sum"]) for r in reconstructed["volumes"]}
    blocks = {
        (r["first"], r["second"]): _fraction(r["child_integral_sum"])
        for r in reconstructed["blocks"]
    }
    left = [c["event"] for c in middle_groups[first]]
    right = [c["event"] for c in middle_groups[second]]
    denominator = sum((volumes[x] for x in left), F(0)) * sum((volumes[x] for x in right), F(0))
    integral = F(0)
    conditional = F(0) if denominator else None
    for a, b in product(left, right):
        value = blocks[a, b]
        integral += value
        middle_product = volumes[a] * volumes[b]
        if middle_product:
            _require(denominator > 0, "positive middle product needs positive parent product")
            intermediate_conditional = value / middle_product
            conditional += (middle_product / denominator) * intermediate_conditional
        else:
            _require(value == 0, "zero middle volume cannot carry pair mass")
    _require(
        conditional is None or conditional == integral / denominator,
        "via-middle normalization differs",
    )
    return integral, conditional


def _coarsening(coarse, fine, groups, coarse_geometry, fine_geometry, middle=None):
    geometry = []
    for qi, (a, b) in enumerate(zip(coarse_geometry["geometry"], fine_geometry["geometry"])):
        h_old, pairs_old = _table(a)
        h_new, pairs_new = _table(b)
        volumes = []
        for parent in coarse["cells"]:
            event = parent["event"]
            child_sum = sum((h_new[c["event"]] for c in groups[event]), F(0))
            _require(child_sum == h_old[event], "clipped child volumes must reproduce parent")
            volumes.append(
                {
                    "parent": event,
                    "coarse_volume": _wire(h_old[event]),
                    "child_volume_sum": _wire(child_sum),
                }
            )
        blocks = []
        for first, second in product(h_old, repeat=2):
            target = pairs_old[first, second]
            coarse_integral = _fraction(target["causal_integral"])
            coarse_conditional = (
                None if target["conditional"] is None else _fraction(target["conditional"])
            )
            denominator = h_old[first] * h_old[second]
            child_pairs = list(product(groups[first], groups[second]))
            annotation_products = []
            for left, right in child_pairs:
                sa = left["mark"] * h_new[left["event"]] / left["area"]
                sb = right["mark"] * h_new[right["event"]] / right["area"]
                annotation_products.append(sa * sb)
            annotation_denominator = sum(annotation_products, F(0))
            _require(
                bool(annotation_denominator) == bool(denominator),
                "positive marks must preserve volume support",
            )
            children = []
            total = diagonal = F(0)
            weighted = annotation_weighted = F(0) if denominator else None
            conditionals = []
            for (left, right), annotation_product in zip(child_pairs, annotation_products):
                i, j = left["event"], right["event"]
                child = pairs_new[i, j]
                integral = _fraction(child["causal_integral"])
                child_product = h_new[i] * h_new[j]
                geometric_weight = child_product / denominator if denominator else None
                annotation_weight = (
                    annotation_product / annotation_denominator if annotation_denominator else None
                )
                conditional = (
                    None if child["conditional"] is None else _fraction(child["conditional"])
                )
                total += integral
                if i == j:
                    diagonal += integral
                if child_product:
                    _require(
                        conditional is not None
                        and geometric_weight is not None
                        and annotation_weight is not None,
                        "positive child pair requires defined conditional weights",
                    )
                    weighted += geometric_weight * conditional
                    annotation_weighted += annotation_weight * conditional
                    conditionals.append(conditional)
                else:
                    _require(
                        integral == 0 and conditional is None,
                        "zero child pair must remain undefined",
                    )
                children.append(
                    {
                        "first": i,
                        "second": j,
                        "geometric_weight": _wire(geometric_weight),
                        "annotation_weight": _wire(annotation_weight),
                    }
                )
            unweighted = sum(conditionals, F(0)) / len(conditionals) if conditionals else None
            offdiagonal = total - diagonal
            _require(
                total == coarse_integral and weighted == coarse_conditional,
                "geometric pair coarsening identity failed",
            )
            if denominator:
                _require(
                    sum((_fraction(c["geometric_weight"]) for c in children), F(0)) == 1
                    and sum((_fraction(c["annotation_weight"]) for c in children), F(0)) == 1,
                    "complete block weights must normalize",
                )
            via_integral = via_conditional = None
            if middle is not None:
                middle_groups, reconstructed = middle
                via_integral, via_conditional = _via_middle(
                    first, second, middle_groups, reconstructed["geometry"][qi]
                )
                _require(
                    via_integral == total and via_conditional == weighted,
                    "direct and middle-route coarsening differ",
                )
            blocks.append(
                {
                    "first": first,
                    "second": second,
                    "children": children,
                    "coarse_integral": _wire(coarse_integral),
                    "child_integral_sum": _wire(total),
                    "child_diagonal_integral": _wire(diagonal),
                    "child_offdiagonal_integral": _wire(offdiagonal),
                    "coarse_conditional": _wire(coarse_conditional),
                    "weighted_child_conditional": _wire(weighted),
                    "unweighted_child_conditional": _wire(unweighted),
                    "annotation_weighted_child_conditional": _wire(annotation_weighted),
                    "via_middle_integral": _wire(via_integral),
                    "via_middle_conditional": _wire(via_conditional),
                }
            )
        geometry.append({"probe": a["probe"], "volumes": volumes, "blocks": blocks})
    return {
        "coarse": coarse["level"],
        "fine": fine["level"],
        "parents": [
            {"parent": p["event"], "children": [c["event"] for c in groups[p["event"]]]}
            for p in coarse["cells"]
        ],
        "geometry": geometry,
    }


def build_family(problem):
    probes, levels = _parse(problem)
    lineage = {link: _lineage(levels[link[0]], levels[link[1]]) for link in LINKS}
    inverse01, inverse12, inverse02 = (lineage[link][1] for link in LINKS)
    _require(
        inverse02 == {child: inverse01[middle] for child, middle in inverse12.items()},
        "direct parent map must equal level-qualified composition",
    )
    output_levels = [_geometry(level, probes) for level in levels]
    coarsenings = []
    for coarse, fine in LINKS:
        middle = (lineage[0, 1][0], coarsenings[1]) if (coarse, fine) == (0, 2) else None
        coarsenings.append(
            _coarsening(
                levels[coarse],
                levels[fine],
                lineage[coarse, fine][0],
                output_levels[coarse],
                output_levels[fine],
                middle,
            )
        )
    level_pairs = [
        pair for level in output_levels for row in level["geometry"] for pair in row["pairs"]
    ]
    blocks = [block for link in coarsenings for row in link["geometry"] for block in row["blocks"]]
    result = {
        "problem": copy.deepcopy(problem),
        "levels": output_levels,
        "coarsenings": coarsenings,
        "counts": {
            "levels": len(levels),
            "probes": len(probes),
            "level_pairs": len(level_pairs),
            "blocks": len(blocks),
            "child_terms": sum(len(block["children"]) for block in blocks),
            "undefined_level_pairs": sum(pair["conditional"] is None for pair in level_pairs),
            "undefined_blocks": sum(block["coarse_conditional"] is None for block in blocks),
            "unweighted_mismatches": sum(
                block["unweighted_child_conditional"] != block["coarse_conditional"]
                for block in blocks
            ),
            "annotation_mismatches": sum(
                block["annotation_weighted_child_conditional"] != block["coarse_conditional"]
                for block in blocks
            ),
            "diagonal_omission_mismatches": sum(
                block["child_offdiagonal_integral"] != block["coarse_integral"] for block in blocks
            ),
            "cross_child_omission_mismatches": sum(
                block["child_diagonal_integral"] != block["coarse_integral"] for block in blocks
            ),
        },
    }
    return json.loads(canonical(result))
