"""Private exact breakpoint/moment contract on explicitly supplied geometry.

Incoming and outgoing volumes are piecewise bilinear in global coordinates.
All pair/triple results come from their raw-moment contractions, not a stored
pair table or historical integration engine. This is not a production API.
"""

import json
from fractions import Fraction as F
from itertools import combinations, pairwise, product
from math import gcd

LINKS = ((0, 1), (1, 2), (0, 2))
EXPONENTS = ((0, 0), (1, 0), (0, 1), (1, 1))


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
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
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


def _moments(bounds):
    """Nine tensor antiderivatives, using one common global coordinate basis."""
    u0, u1, v0, v1 = bounds
    us = [(u1 ** (i + 1) - u0 ** (i + 1)) / (i + 1) for i in range(3)]
    vs = [(v1 ** (j + 1) - v0 ** (j + 1)) / (j + 1) for j in range(3)]
    values = [u * v / 2 for u, v in product(us, vs)]
    # These moments are retained contract data. Cancellation in a later scalar
    # answer never licenses an oversized component in this vector.
    _encode(values)
    return values


def rectangle_moments(bounds):
    """Return exact M00,M01,M02,M10,M11,M12,M20,M21,M22 for a rectangle."""
    return _encode(_moments(_rectangle(bounds)))


def _gram(moments):
    first = [moments[3 * i + j] for i, j in EXPONENTS]
    gram = [[moments[3 * (i + k) + j + l] for k, l in EXPONENTS] for i, j in EXPONENTS]
    h = moments[0]
    _require(h > 0 and gram[0][0] == h, "positive moment volume required")
    for a, (i, j) in enumerate(EXPONENTS):
        for b, (k, l) in enumerate(EXPONENTS):
            _require(
                gram[a][b] == gram[b][a] == moments[3 * (i + k) + j + l],
                "Gram symmetry or repeated entry differs",
            )
    _require(
        all(gram[0][a] - first[0] * first[a] / h == 0 for a in range(4))
        and all(gram[a][0] - first[a] * first[0] / h == 0 for a in range(4)),
        "centered Gram constant row or column differs",
    )
    return first, gram


def _branch(endpoint, tile, incoming):
    a, b = endpoint
    lo, hi = tile
    if hi <= a:
        return (F(0), F(0)) if incoming else (b - a, F(0))
    if lo >= b:
        return (b - a, F(0)) if incoming else (F(0), F(0))
    _require(a <= lo and hi <= b, "shared breakpoint grid missed a clamp branch")
    return (-a, F(1)) if incoming else (b, F(-1))


def _coefficients(endpoint, tile, incoming):
    if endpoint is None:
        return [F(0)] * 4
    uc, us = _branch(endpoint[:2], tile[:2], incoming)
    vc, vs = _branch(endpoint[2:], tile[2:], incoming)
    return [uc * vc / 2, us * vc / 2, uc * vs / 2, us * vs / 2]


def _linear(coefficients, moments):
    return sum((a * b for a, b in zip(coefficients, moments, strict=True)), F(0))


def _contract(left, gram, right):
    return sum((left[a] * gram[a][b] * right[b] for a, b in product(range(4), repeat=2)), F(0))


def _center(coefficients, mean):
    return [coefficients[0] - mean, *coefficients[1:]]


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
        parent = parents[0]["event"]
        groups[parent].append(child["event"])
        inverse[child["event"]] = parent
    areas = {c["event"]: c["area"] for c in fine["cells"]}
    for parent in coarse["cells"]:
        children = groups[parent["event"]]
        _require(
            children and sum((areas[c] for c in children), F(0)) == parent["area"],
            "children must cover each parent, not only global area",
        )
    return groups, inverse


def _middle(event, clips, moment_cache):
    bounds = clips[event]
    if bounds is None:
        return {
            "event": event,
            "bounds": None,
            "u_breaks": [],
            "v_breaks": [],
            "moments": [F(0)] * 9,
            "tiles": [],
        }, []

    def moments(b):
        if b not in moment_cache:
            moment_cache[b] = _moments(b)
        return moment_cache[b]

    breaks = []
    for offset in (0, 2):
        lo, hi = bounds[offset : offset + 2]
        values = {lo, hi}
        for clip in clips.values():
            if clip is not None:
                values.update(x for x in clip[offset : offset + 2] if lo < x < hi)
        breaks.append(sorted(values))
    ub, vb = breaks
    _require((len(ub) - 1) * (len(vb) - 1) <= 289, "bounded shared tile inventory")
    tiles, data = [], []
    for u, v in product(pairwise(ub), pairwise(vb)):
        tile = (*u, *v)
        raw = moments(tile)
        first, gram = _gram(raw)
        incoming = {e: _coefficients(b, tile, True) for e, b in clips.items()}
        outgoing = {e: _coefficients(b, tile, False) for e, b in clips.items()}
        incoming_integrals = {e: _linear(c, first) for e, c in incoming.items()}
        outgoing_integrals = {e: _linear(c, first) for e, c in outgoing.items()}
        _require(
            all(x >= 0 for x in (*incoming_integrals.values(), *outgoing_integrals.values())),
            "causal-volume contraction is negative",
        )
        tiles.append(
            {
                "bounds": list(tile),
                "moments": list(raw),
                "incoming": [{"event": e, "coefficients": list(c)} for e, c in incoming.items()],
                "outgoing": [{"event": e, "coefficients": list(c)} for e, c in outgoing.items()],
            }
        )
        data.append((raw[0], gram, incoming, outgoing, incoming_integrals, outgoing_integrals))
    whole = moments(bounds)
    _require(
        all(sum((tile["moments"][i] for tile in tiles), F(0)) == whole[i] for i in range(9)),
        "tile raw moments do not add in the global basis",
    )
    return {
        "event": event,
        "bounds": list(bounds),
        "u_breaks": ub,
        "v_breaks": vb,
        "moments": list(whole),
        "tiles": tiles,
    }, data


def _geometry(level, probes, moment_cache):
    geometry, retained_data = [], []
    for probe in probes:
        clips = {c["event"]: _clip(c["bounds"], probe["bounds"]) for c in level["cells"]}
        h = {e: _area(b) if b is not None else F(0) for e, b in clips.items()}
        volume = _area(probe["bounds"])
        _require(sum(h.values(), F(0)) == volume, "cell clips must cover every query")
        middles, tile_data = [], {}
        for e in clips:
            row, data = _middle(e, clips, moment_cache)
            _require(row["moments"][0] == h[e], "middle zeroth moment differs from volume")
            middles.append(row)
            tile_data[e] = data
        pairs, j = [], {}
        for a, b in product(h, repeat=2):
            value = sum((tile[4][a] for tile in tile_data[b]), F(0))
            outgoing_value = sum((tile[5][b] for tile in tile_data[a]), F(0))
            _require(value == outgoing_value, "incoming/outgoing pair contractions disagree")
            denominator = h[a] * h[b]
            conditional = value / denominator if denominator else None
            _require(conditional is None or 0 <= conditional <= 1, "pair conditional out of range")
            if a == b:
                _require(value == h[a] ** 2 / 4, "within-region pair identity failed")
            j[a, b] = value
            pairs.append(
                {
                    "first": a,
                    "second": b,
                    "clipped_product": denominator,
                    "causal_integral": value,
                    "conditional": conditional,
                }
            )
        _require(sum(j.values(), F(0)) == volume**2 / 4, "complete pair integral differs")
        triples, t = [], {}
        for a, b, c in product(h, repeat=3):
            integral = sum(
                (_contract(tile[2][a], tile[1], tile[3][c]) for tile in tile_data[b]), F(0)
            )
            denominator = h[a] * h[b] * h[c]
            p = pt = error = tile_error = between = centered = within_centered = covariance = None
            if h[b]:
                p = j[a, b] * j[b, c] / h[b]
                pt = sum((tile[4][a] * tile[5][c] / tile[0] for tile in tile_data[b]), F(0))
                centered = sum(
                    (
                        _contract(
                            _center(tile[2][a], j[a, b] / h[b]),
                            tile[1],
                            _center(tile[3][c], j[b, c] / h[b]),
                        )
                        for tile in tile_data[b]
                    ),
                    F(0),
                )
                within_centered = sum(
                    (
                        _contract(
                            _center(tile[2][a], tile[4][a] / tile[0]),
                            tile[1],
                            _center(tile[3][c], tile[5][c] / tile[0]),
                        )
                        for tile in tile_data[b]
                    ),
                    F(0),
                )
                error, tile_error, between = p - integral, pt - integral, p - pt
                _require(
                    centered == -error and within_centered == -tile_error,
                    "centered coefficient contractions disagree with product errors",
                )
                _require(error == tile_error + between, "mean-only error decomposition differs")
                covariance = centered / h[b]
            else:
                _require(integral == j[a, b] == j[b, c] == 0, "empty middle carries causal mass")
            conditional = integral / denominator if denominator else None
            pc = p / denominator if denominator else None
            ptc = pt / denominator if denominator else None
            _require(0 <= integral <= denominator, "triple integral outside product volume")
            _require(
                all(x is None or 0 <= x <= 1 for x in (conditional, pc, ptc)),
                "normalized triple quantity out of range",
            )
            if a == b == c:
                _require(integral == h[a] ** 3 / 36, "within-region triple identity failed")
            triples.append(
                {
                    "first": a,
                    "middle": b,
                    "last": c,
                    "volume_product": denominator,
                    "causal_integral": integral,
                    "pair_product": p,
                    "product_error": error,
                    "conditional": conditional,
                    "product_conditional": pc,
                    "middle_covariance": covariance,
                    "tile_pair_product": pt,
                    "tile_product_error": tile_error,
                    "between_tile_error": between,
                    "tile_product_conditional": ptc,
                    "centered_integral": centered,
                    "within_tile_centered_integral": within_centered,
                }
            )
            t[a, b, c] = integral
        total = sum(t.values(), F(0))
        original = sum((r["pair_product"] for r in triples if r["pair_product"] is not None), F(0))
        tiled = sum(
            (r["tile_pair_product"] for r in triples if r["tile_pair_product"] is not None), F(0)
        )
        _require(total == volume**3 / 36, "complete shared-middle integral differs")
        geometry.append(
            {
                "probe": probe["name"],
                "volume": volume,
                "cells": [{"event": e, "clipped_volume": v} for e, v in h.items()],
                "middles": middles,
                "pairs": pairs,
                "triples": triples,
                "summary": {
                    "true_integral": total,
                    "continuum_integral": volume**3 / 36,
                    "original_product_sum": original,
                    "tile_product_sum": tiled,
                    "original_error": original - total,
                    "tile_error": tiled - total,
                    "between_error": original - tiled,
                },
            }
        )
        retained_data.append(({r["event"]: r["moments"] for r in middles}, t))
    return {"level": level["level"], "geometry": geometry}, retained_data


def _coarsening(coarse, fine, groups, probes, old_data, new_data, via=None):
    geometry = []
    for qi, probe in enumerate(probes):
        old_moments, old_t = old_data[qi]
        moments, t = new_data[qi]
        moment_blocks = []
        for parent, children in groups.items():
            child_sum = [sum((moments[e][i] for e in children), F(0)) for i in range(9)]
            _require(child_sum == old_moments[parent], "coarsened raw moments differ")
            moment_blocks.append(
                {
                    "parent": parent,
                    "children": list(children),
                    "coarse_moments": list(old_moments[parent]),
                    "child_moment_sum": child_sum,
                }
            )
        via_table = None
        if via is not None:
            via_groups, reconstructed = via
            via_table = {
                (r["first"], r["middle"], r["last"]): r["child_integral_sum"]
                for r in reconstructed["geometry"][qi]["blocks"]
            }
        blocks = []
        for a, b, c in product(groups, repeat=3):
            children = list(product(groups[a], groups[b], groups[c]))
            total = sum((t[row] for row in children), F(0))
            _require(total == old_t[a, b, c], "true triple block additivity differs")
            via_integral = None
            if via_table is not None:
                via_integral = sum(
                    (
                        via_table[row]
                        for row in product(via_groups[a], via_groups[b], via_groups[c])
                    ),
                    F(0),
                )
                _require(via_integral == total, "via-middle true triple sum differs")
            blocks.append(
                {
                    "first": a,
                    "middle": b,
                    "last": c,
                    "children": [list(row) for row in children],
                    "coarse_integral": old_t[a, b, c],
                    "child_integral_sum": total,
                    "via_middle_integral": via_integral,
                }
            )
        geometry.append({"probe": probe["name"], "moment_blocks": moment_blocks, "blocks": blocks})
    return {
        "coarse": coarse["level"],
        "fine": fine["level"],
        "parents": [{"parent": p, "children": list(xs)} for p, xs in groups.items()],
        "geometry": geometry,
    }


def _counts(levels, coarsenings, probe_count):
    names = (
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
    counts = dict.fromkeys(names, 0)
    counts.update({"levels": len(levels), "probes": probe_count})
    for level in levels:
        for q in level["geometry"]:
            counts["level_pairs"] += len(q["pairs"])
            counts["level_triples"] += len(q["triples"])
            for middle in q["middles"]:
                counts["middle_cells"] += 1
                counts["positive_middle_cells"] += middle["bounds"] is not None
                counts["breakpoint_entries"] += len(middle["u_breaks"]) + len(middle["v_breaks"])
                counts["tiles"] += len(middle["tiles"])
                for tile in middle["tiles"]:
                    counts["coefficient_vectors"] += len(tile["incoming"]) + len(tile["outgoing"])
            for row in q["triples"]:
                counts["positive_triples"] += row["causal_integral"] > 0
                counts["undefined_level_conditionals"] += row["conditional"] is None
                if row["pair_product"] is None:
                    counts["zero_middle_level_triples"] += 1
                else:
                    for prefix, field in (
                        ("original", "product_error"),
                        ("tile", "tile_product_error"),
                        ("between", "between_tile_error"),
                    ):
                        value = row[field]
                        sign = "positive" if value > 0 else "negative" if value < 0 else "zero"
                        counts[prefix + "_" + sign + "_errors"] += 1
    for link in coarsenings:
        for q in link["geometry"]:
            counts["coarsening_moment_blocks"] += len(q["moment_blocks"])
            counts["blocks"] += len(q["blocks"])
            counts["child_terms"] += sum(len(r["children"]) for r in q["blocks"])
    counts.update(
        {
            "middle_bound_entries": 4 * counts["positive_middle_cells"],
            "tile_bound_entries": 4 * counts["tiles"],
            "middle_moment_entries": 9 * counts["middle_cells"],
            "tile_moment_entries": 9 * counts["tiles"],
            "coefficient_entries": 4 * counts["coefficient_vectors"],
            "coarsening_moment_entries": 18 * counts["coarsening_moment_blocks"],
        }
    )
    return counts


def build_family(problem):
    """Return the complete detached moment contract and exact comparisons."""
    probes, sources = _parse(problem)
    lineages = {(a, b): _lineage(sources[a], sources[b]) for a, b in LINKS}
    for child, parent in lineages[0, 2][1].items():
        _require(
            lineages[0, 1][1][lineages[1, 2][1][child]] == parent,
            "direct and composed full-rectangle parent maps differ",
        )
    cache = {}
    generated = [_geometry(level, probes, cache) for level in sources]
    levels, data = [x[0] for x in generated], [x[1] for x in generated]
    coarsenings = []
    for a, b in LINKS:
        via = (lineages[0, 1][0], coarsenings[1]) if (a, b) == (0, 2) else None
        coarsenings.append(
            _coarsening(sources[a], sources[b], lineages[a, b][0], probes, data[a], data[b], via)
        )
    result = _encode(
        {
            "problem": problem,
            "levels": levels,
            "coarsenings": coarsenings,
            "counts": _counts(levels, coarsenings, len(probes)),
        }
    )
    return json.loads(canonical(result))
