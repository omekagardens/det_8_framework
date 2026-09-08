"""Private exact shared-middle geometry on supplied rectangular partitions.

No observation law or historical executor is consumed. Pair-product errors are
signed diagnostics, not a transition model or a generic hardening contract.
"""

import json
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd

LINKS = ((0, 1), (1, 2), (0, 2))
PATTERNS = ("all_equal", "first_middle", "first_last", "middle_last", "all_distinct")


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
        return {k: _encode(v) for k, v in value.items()}
    return value


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


def _endpoints(values):
    _require(all(type(x) in (int, F) for x in values), "exact rational endpoints required")
    values = tuple(map(F, values))
    _require(
        all(values[i] <= values[i + 1] for i in range(0, len(values), 2)),
        "reversed interval endpoints",
    )
    return values


def causal_area(a, b, c, d):
    """Directed interval integral, via exact positive-part antiderivatives."""
    a, b, c, d = _endpoints((a, b, c, d))
    positive_square = lambda x: max(F(0), x) ** 2
    answer = (
        positive_square(d - a)
        - positive_square(d - b)
        - positive_square(c - a)
        + positive_square(c - b)
    ) / 2
    _require(0 <= answer <= (b - a) * (d - c), "pair integral outside product length")
    return answer


def triple_area(a, b, c, d, e, f):
    """Integrate one shared middle coordinate using positive-part cubics."""
    a, b, c, d, e, f = _endpoints((a, b, c, d, e, f))

    def positive_product(r, s):
        lo, hi = max(c, r), min(d, s)
        if hi <= lo:
            return F(0)
        # Integrate (y-r)(s-y) only where both positive parts are active.
        # No premature bit bound is imposed on these unretained differences.
        primitive = lambda y: -(y**3) / 3 + (r + s) * y**2 / 2 - r * s * y
        return primitive(hi) - primitive(lo)

    answer = (
        positive_product(a, f)
        - positive_product(a, e)
        - positive_product(b, f)
        + positive_product(b, e)
    )
    _require(
        0 <= answer <= (b - a) * (d - c) * (f - e),
        "triple integral outside product length",
    )
    return answer


class _Integrals:
    """Exact primitive caches live for only one build; no fixture IDs as keys."""

    def __init__(self):
        self.pairs = {}
        self.triples = {}

    def _pair(self, endpoints):
        if endpoints not in self.pairs:
            self.pairs[endpoints] = causal_area(*endpoints)
        return self.pairs[endpoints]

    def _triple(self, endpoints):
        if endpoints not in self.triples:
            self.triples[endpoints] = triple_area(*endpoints)
        return self.triples[endpoints]

    def pair(self, a, b):
        if a is None or b is None:
            return F(0)
        return self._pair(a[:2] + b[:2]) * self._pair(a[2:] + b[2:]) / 4

    def triple(self, a, b, c):
        if a is None or b is None or c is None:
            return F(0)
        return self._triple(a[:2] + b[:2] + c[:2]) * self._triple(a[2:] + b[2:] + c[2:]) / 8


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
            _fields(c, ("event", "bounds"))
            event = c["event"]
            _require(type(event) is int, "native level-local integer ID required")
            b = _rectangle(c["bounds"])
            cells.append({"event": event, "bounds": b, "area": _area(b)})
        ids = [c["event"] for c in cells]
        _require(ids == sorted(set(ids)), "event-ordered unique cell IDs required")
        _require(
            all(_clip(a["bounds"], b["bounds"]) is None for a, b in combinations(cells, 2)),
            "cell interiors must be disjoint",
        )
        levels.append({"level": name, "cells": cells})
    return probes, levels


def _lineage(coarse, fine):
    groups = {cell["event"]: [] for cell in coarse["cells"]}
    inverse = {}
    for child in fine["cells"]:
        parents = [p for p in coarse["cells"] if _contains(p["bounds"], child["bounds"])]
        _require(len(parents) == 1, "each child requires one full-rectangle parent")
        event = child["event"]
        parent = parents[0]["event"]
        groups[parent].append(event)
        inverse[event] = parent
    areas = {c["event"]: c["area"] for c in fine["cells"]}
    for parent in coarse["cells"]:
        children = groups[parent["event"]]
        _require(
            children and sum((areas[c] for c in children), F(0)) == parent["area"],
            "children must cover each parent, not only global area",
        )
    return groups, inverse


def _geometry(level, probes, integrals):
    out, data = [], []
    for q in probes:
        clips = {cell["event"]: _clip(cell["bounds"], q["bounds"]) for cell in level["cells"]}
        h = {event: _area(b) if b is not None else F(0) for event, b in clips.items()}
        volume = _area(q["bounds"])
        _require(sum(h.values(), F(0)) == volume, "cell clips must cover each positive query")
        pair_rows, pair_table = [], {}
        for a, b in product(h, repeat=2):
            denominator = h[a] * h[b]
            integral = integrals.pair(clips[a], clips[b])
            conditional = integral / denominator if denominator else None
            _require(conditional is None or 0 <= conditional <= 1, "pair conditional out of range")
            if a == b:
                _require(integral == denominator / 4, "within-cell pair identity failed")
            pair_table[a, b] = integral
            pair_rows.append(
                {
                    "first": a,
                    "second": b,
                    "clipped_product": denominator,
                    "causal_integral": integral,
                    "conditional": conditional,
                }
            )
        _require(sum(pair_table.values(), F(0)) == volume**2 / 4, "complete pair integral differs")
        triple_rows, triple_table = [], {}
        for a, b, c in product(h, repeat=3):
            denominator = h[a] * h[b] * h[c]
            integral = integrals.triple(clips[a], clips[b], clips[c])
            projected = pair_table[a, b] * pair_table[b, c] / h[b] if h[b] else None
            error = projected - integral if h[b] else None
            conditional = integral / denominator if denominator else None
            product_conditional = projected / denominator if denominator else None
            covariance = -error / h[b] if h[b] else None
            _require(
                conditional is None or 0 <= conditional <= 1, "triple conditional out of range"
            )
            _require(
                product_conditional is None or 0 <= product_conditional <= 1,
                "product conditional out of range",
            )
            if a == b == c:
                _require(integral == h[a] ** 3 / 36, "within-region triple identity failed")
            row = {
                "first": a,
                "middle": b,
                "last": c,
                "volume_product": denominator,
                "causal_integral": integral,
                "pair_product": projected,
                "product_error": error,
                "conditional": conditional,
                "product_conditional": product_conditional,
                "middle_covariance": covariance,
            }
            triple_rows.append(row)
            triple_table[a, b, c] = row
        true_total = sum((r["causal_integral"] for r in triple_rows), F(0))
        extended_product = sum(
            (r["pair_product"] for r in triple_rows if r["pair_product"] is not None), F(0)
        )
        _require(true_total == volume**3 / 36, "complete triple integral differs")
        out.append(
            {
                "probe": q["name"],
                "volume": volume,
                "cells": [{"event": e, "clipped_volume": v} for e, v in h.items()],
                "pairs": pair_rows,
                "triples": triple_rows,
                "summary": {
                    "true_integral": true_total,
                    "continuum_integral": volume**3 / 36,
                    "extended_product_sum": extended_product,
                    "product_error": extended_product - true_total,
                },
            }
        )
        data.append((h, pair_table, triple_table))
    return {"level": level["level"], "geometry": out}, data


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


def _coarsening(coarse, fine, groups, probes, old_data, new_data, via=None):
    geometry = []
    for qi, q in enumerate(probes):
        old_h, _old_j, old_t = old_data[qi]
        h, j, t = new_data[qi]
        volumes = []
        for parent, children in groups.items():
            total = sum((h[x] for x in children), F(0))
            _require(total == old_h[parent], "clipped child volumes must reproduce parent")
            volumes.append(
                {"parent": parent, "coarse_volume": old_h[parent], "child_volume_sum": total}
            )
        via_table = None
        if via is not None:
            via_groups, reconstructed = via
            via_table = {
                (r["first"], r["middle"], r["last"]): r["child_integral_sum"]
                for r in reconstructed["geometry"][qi]["blocks"]
            }
        blocks = []
        for a, b, c in product(old_h, repeat=3):
            target = old_t[a, b, c]
            children = list(product(groups[a], groups[b], groups[c]))
            patterns = {name: F(0) for name in PATTERNS}
            child_total, zero_middle = F(0), 0
            parent_product = old_h[a] * old_h[b] * old_h[c]
            weighted = F(0) if parent_product else None
            fine_product = F(0) if old_h[b] else None
            for x, y, z in children:
                row = t[x, y, z]
                integral = row["causal_integral"]
                patterns[_pattern(x, y, z)] += integral
                child_total += integral
                if not h[y]:
                    zero_middle += 1
                    _require(
                        row["pair_product"] is None and integral == 0,
                        "zero-middle child must retain a null product and zero measure",
                    )
                else:
                    _require(
                        fine_product is not None, "positive child middle needs positive parent"
                    )
                    fine_product += row["pair_product"]
                child_product = h[x] * h[y] * h[z]
                if child_product:
                    _require(weighted is not None, "positive child product needs positive parent")
                    weighted += (child_product / parent_product) * row["conditional"]
                else:
                    _require(
                        row["conditional"] is None and integral == 0,
                        "zero child product carries mass",
                    )
            _require(
                child_total == target["causal_integral"], "true triple block additivity failed"
            )
            _require(
                sum(patterns.values(), F(0)) == child_total,
                "child equality patterns do not partition",
            )
            _require(weighted == target["conditional"], "weighted true conditional differs")
            endpoint = middle = within = between = None
            if old_h[b]:
                endpoint = sum(
                    (
                        sum((j[x, y] for y in groups[b]), F(0))
                        * sum((j[y, z] for y in groups[b]), F(0))
                        / old_h[b]
                        for x, z in product(groups[a], groups[c])
                    ),
                    F(0),
                )
                middle = sum(
                    (
                        sum((j[x, y] for x in groups[a]), F(0))
                        * sum((j[y, z] for z in groups[c]), F(0))
                        / h[y]
                        for y in groups[b]
                        if h[y]
                    ),
                    F(0),
                )
                _require(
                    endpoint == target["pair_product"], "endpoint-only refinement changed product"
                )
                _require(
                    middle == fine_product, "middle-only refinement disagrees with fine product sum"
                )
                within = fine_product - child_total
                between = target["pair_product"] - fine_product
                _require(
                    target["product_error"] == within + between,
                    "signed error decomposition differs",
                )
            else:
                _require(
                    fine_product is None and child_total == 0,
                    "zero parent middle accounting differs",
                )
            via_integral = None
            if via_table is not None:
                via_integral = sum(
                    (
                        via_table[x, y, z]
                        for x, y, z in product(via_groups[a], via_groups[b], via_groups[c])
                    ),
                    F(0),
                )
                _require(via_integral == child_total, "via-middle true triple sum differs")
            blocks.append(
                {
                    "first": a,
                    "middle": b,
                    "last": c,
                    "children": [list(row) for row in children],
                    "zero_middle_children": zero_middle,
                    "coarse_integral": target["causal_integral"],
                    "child_integral_sum": child_total,
                    "child_pattern_integrals": patterns,
                    "coarse_conditional": target["conditional"],
                    "weighted_child_conditional": weighted,
                    "coarse_pair_product": target["pair_product"],
                    "child_pair_product_sum": fine_product,
                    "endpoint_refined_product": endpoint,
                    "middle_refined_product": middle,
                    "coarse_product_error": target["product_error"],
                    "within_child_error": within,
                    "between_child_error": between,
                    "via_middle_integral": via_integral,
                }
            )
        geometry.append({"probe": q["name"], "volumes": volumes, "blocks": blocks})
    return {
        "coarse": coarse["level"],
        "fine": fine["level"],
        "parents": [{"parent": p, "children": list(xs)} for p, xs in groups.items()],
        "geometry": geometry,
    }


def _counts(levels, coarsenings, probe_count):
    counts = {
        name: 0
        for name in (
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
    }
    counts.update({"levels": len(levels), "probes": probe_count})
    for level in levels:
        for q in level["geometry"]:
            counts["level_pairs"] += len(q["pairs"])
            counts["level_triples"] += len(q["triples"])
            for row in q["triples"]:
                error = row["product_error"]
                if error is None:
                    counts["zero_middle_level_triples"] += 1
                else:
                    sign = "positive" if error > 0 else "negative" if error < 0 else "zero"
                    counts[sign + "_level_errors"] += 1
                counts["undefined_level_conditionals"] += row["conditional"] is None
                counts["positive_repeated_region_triples"] += (
                    row["causal_integral"] > 0
                    and len({row["first"], row["middle"], row["last"]}) < 3
                )
    for link in coarsenings:
        for q in link["geometry"]:
            counts["blocks"] += len(q["blocks"])
            for row in q["blocks"]:
                counts["child_terms"] += len(row["children"])
                error = row["between_child_error"]
                if error is None:
                    counts["zero_middle_blocks"] += 1
                else:
                    sign = "positive" if error > 0 else "negative" if error < 0 else "zero"
                    counts[sign + "_between_errors"] += 1
    return counts


def build_family(problem):
    """Build the complete detached, exact geometry and signed dependence wire."""
    probes, source_levels = _parse(problem)
    lineages = {(a, b): _lineage(source_levels[a], source_levels[b]) for a, b in LINKS}
    for child, parent in lineages[0, 2][1].items():
        _require(
            lineages[0, 1][1][lineages[1, 2][1][child]] == parent,
            "direct and composed full-rectangle parent maps differ",
        )
    integrals = _Integrals()
    generated = [_geometry(level, probes, integrals) for level in source_levels]
    levels = [row[0] for row in generated]
    data = [row[1] for row in generated]
    coarsenings = []
    for a, b in LINKS:
        via = (lineages[0, 1][0], coarsenings[1]) if (a, b) == (0, 2) else None
        coarsenings.append(
            _coarsening(
                source_levels[a], source_levels[b], lineages[a, b][0], probes, data[a], data[b], via
            )
        )
    result = _encode(
        {
            "problem": problem,
            "levels": levels,
            "coarsenings": coarsenings,
            "counts": _counts(levels, coarsenings, len(probes)),
        }
    )
    # One native round-trip both validates retained integer components and detaches
    # all input/container aliases. Caches and unretained arithmetic do not escape.
    return json.loads(canonical(result))
