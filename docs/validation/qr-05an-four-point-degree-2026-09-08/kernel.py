"""Private degree-aware four-point contractions on supplied rectangles.

The two intermediate points remain coupled through an integrated predecessor
field. Geometry, global raw moments and field coefficients are explicitly
retained; this is not a production API or a universal fixed-degree closure.
"""

import json
from fractions import Fraction as F
from itertools import combinations, pairwise, product
from math import gcd

LINKS = ((0, 1), (1, 2), (0, 2))
LINEAR = ((0, 0), (1, 0), (0, 1), (1, 1))
QUADRATIC = tuple(product(range(3), repeat=2))


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
        return {key: _encode(child) for key, child in value.items()}
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
    u0, u1, v0, v1 = bounds
    us = [(u1 ** (i + 1) - u0 ** (i + 1)) / (i + 1) for i in range(4)]
    vs = [(v1 ** (j + 1) - v0 ** (j + 1)) / (j + 1) for j in range(4)]
    result = tuple(u * v / 2 for u, v in product(us, vs))
    # The raw moments themselves are retained, even if later contractions
    # cancel large translated powers. Only these reduced retained values bind.
    _encode(list(result))
    return result


def rectangle_moments(bounds):
    """Sixteen exact M_ij, i outer/j inner, 0 <= i,j <= 3."""
    return _encode(list(_moments(_rectangle(bounds))))


def _primitive(a, t):
    return (max(t - a[0], F(0)) ** 2 - max(t - a[1], F(0)) ** 2) / 2


def _axis_field(a, b, tile):
    """Coefficients of integral_(B below t) predecessor_A(y) dy."""
    lo, hi = tile
    base = _primitive(a, b[0])
    if hi <= b[0]:
        return (F(0), F(0), F(0))
    if lo >= b[1]:
        return (_primitive(a, b[1]) - base, F(0), F(0))
    _require(b[0] <= lo and hi <= b[1], "shared grid missed B saturation")
    if hi <= a[0]:
        result = (-base, F(0), F(0))
    elif lo >= a[1]:
        result = ((a[0] ** 2 - a[1] ** 2) / 2 - base, a[1] - a[0], F(0))
    else:
        _require(a[0] <= lo and hi <= a[1], "shared grid missed A primitive branch")
        result = (a[0] ** 2 / 2 - base, -a[0], F(1, 2))
    _require(result[2] >= 0, "propagated branch is not convex")
    return result


def _propagated(a, b, tile):
    if a is None or b is None:
        return (F(0),) * 9
    us = _axis_field(a[:2], b[:2], tile[:2])
    vs = _axis_field(a[2:], b[2:], tile[2:])
    return tuple(u * v / 4 for u, v in product(us, vs))


def _successor_axis(interval, tile):
    a, b = interval
    lo, hi = tile
    if hi <= a:
        return b - a, F(0)
    if lo >= b:
        return F(0), F(0)
    _require(a <= lo and hi <= b, "shared grid missed outgoing branch")
    return b, F(-1)


def _outgoing(endpoint, tile):
    if endpoint is None:
        return (F(0),) * 4
    uc, us = _successor_axis(endpoint[:2], tile[:2])
    vc, vs = _successor_axis(endpoint[2:], tile[2:])
    return uc * vc / 2, us * vc / 2, uc * vs / 2, us * vs / 2


def _evaluate(coefficients, powers, u, v):
    return sum((c * u**i * v**j for c, (i, j) in zip(coefficients, powers, strict=True)), F(0))


def _corner_fit(field, tile):
    u0, u1, v0, v1 = tile
    f00, f01, f10, f11 = (_evaluate(field, QUADRATIC, u, v) for u, v in product((u0, u1), (v0, v1)))
    uv = (f11 - f10 - f01 + f00) / ((u1 - u0) * (v1 - v0))
    u = (f10 - f00) / (u1 - u0) - uv * v0
    v = (f01 - f00) / (v1 - v0) - uv * u0
    return f00 - u * u0 - v * v0 - uv * u0 * v0, u, v, uv


def _linear(coefficients, powers, moments):
    return sum(
        (c * moments[4 * i + j] for c, (i, j) in zip(coefficients, powers, strict=True)), F(0)
    )


def _cross(left, left_powers, right, moments, cache):
    key = (left, left_powers, right, moments)
    if key not in cache:
        cache[key] = sum(
            (
                a * b * moments[4 * (i + k) + j + l]
                for a, (i, j) in zip(left, left_powers, strict=True)
                for b, (k, l) in zip(right, LINEAR, strict=True)
            ),
            F(0),
        )
    return cache[key]


def _center(coefficients, mean):
    return (coefficients[0] - mean, *coefficients[1:])


def _parse(problem):
    _native(problem)
    _fields(problem, ("family", "probes", "levels"))
    _label(problem["family"])
    _require(
        type(problem["probes"]) is list and 1 <= len(problem["probes"]) <= 3,
        "bounded probes required",
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
            "bounded positive cells required",
        )
        cells = []
        for c in row["cells"]:
            _fields(c, ("event", "bounds"))
            event = c["event"]
            _require(type(event) is int, "native level-local integer ID required")
            bounds = _rectangle(c["bounds"])
            cells.append({"event": event, "bounds": bounds, "area": _area(bounds)})
        ids = [c["event"] for c in cells]
        _require(ids == sorted(set(ids)), "event-ordered unique cell IDs required")
        _require(
            all(_clip(a["bounds"], b["bounds"]) is None for a, b in combinations(cells, 2)),
            "cell interiors overlap",
        )
        for probe in probes:
            clips = [_clip(c["bounds"], probe["bounds"]) for c in cells]
            _require(
                sum((_area(b) for b in clips if b is not None), F(0)) == _area(probe["bounds"]),
                "cell clips must cover each probe",
            )
        levels.append({"level": name, "cells": cells})
    return probes, levels


def _lineage(coarse, fine):
    groups = {c["event"]: [] for c in coarse["cells"]}
    inverse = {}
    for child in fine["cells"]:
        parents = [p for p in coarse["cells"] if _contains(p["bounds"], child["bounds"])]
        _require(len(parents) == 1, "child requires one full-rectangle parent")
        parent = parents[0]["event"]
        groups[parent].append(child["event"])
        inverse[child["event"]] = parent
    areas = {c["event"]: c["area"] for c in fine["cells"]}
    for parent in coarse["cells"]:
        children = groups[parent["event"]]
        _require(
            children and sum((areas[e] for e in children), F(0)) == parent["area"],
            "children must cover every full parent",
        )
    return groups, inverse


def _middle(event, clips, cache):
    bounds = clips[event]
    if bounds is None:
        return {
            "event": event,
            "bounds": None,
            "u_breaks": [],
            "v_breaks": [],
            "moments": [F(0)] * 16,
            "tiles": [],
        }, []

    def moments(b):
        if b not in cache["moments"]:
            cache["moments"][b] = _moments(b)
        return cache["moments"][b]

    breaks = []
    for offset in (0, 2):
        lo, hi = bounds[offset : offset + 2]
        values = {lo, hi}
        for clip in clips.values():
            if clip is not None:
                values.update(x for x in clip[offset : offset + 2] if lo < x < hi)
        breaks.append(sorted(values))
    ub, vb = breaks
    _require((len(ub) - 1) * (len(vb) - 1) <= 289, "bounded shared tile inventory required")
    tiles, data = [], []
    for u, v in product(pairwise(ub), pairwise(vb)):
        tile = (*u, *v)
        raw = moments(tile)
        propagated, forced, flags = {}, {}, {}
        for a, b in product(clips, repeat=2):
            key = (clips[a], clips[b], tile)
            if key not in cache["fields"]:
                field = _propagated(clips[a], clips[b], tile)
                fit = _corner_fit(field, tile)
                flag = all(
                    c == 0 for c, (i, j) in zip(field, QUADRATIC, strict=True) if i == 2 or j == 2
                )
                cache["fields"][key] = field, fit, flag
            propagated[a, b], forced[a, b], flags[a, b] = cache["fields"][key]
        outgoing = {}
        for d, endpoint in clips.items():
            key = (endpoint, tile)
            if key not in cache["outgoing"]:
                cache["outgoing"][key] = _outgoing(endpoint, tile)
            outgoing[d] = cache["outgoing"][key]
        tiles.append(
            {
                "bounds": list(tile),
                "moments": list(raw),
                "propagated": [
                    {
                        "first": a,
                        "second": b,
                        "coefficients": list(field),
                        "forced_coefficients": list(forced[a, b]),
                        "bilinear_admissible": flags[a, b],
                    }
                    for (a, b), field in propagated.items()
                ],
                "outgoing": [{"event": d, "coefficients": list(c)} for d, c in outgoing.items()],
            }
        )
        data.append(
            {
                "moments": raw,
                "propagated": propagated,
                "forced": forced,
                "flags": flags,
                "outgoing": outgoing,
            }
        )
    whole = moments(bounds)
    _require(
        all(sum((t["moments"][i] for t in tiles), F(0)) == whole[i] for i in range(16)),
        "tile moments do not add in the global basis",
    )
    return {
        "event": event,
        "bounds": list(bounds),
        "u_breaks": ub,
        "v_breaks": vb,
        "moments": list(whole),
        "tiles": tiles,
    }, data


def _geometry(level, probes, cache):
    geometry, retained_data = [], []
    for probe in probes:
        clips = {c["event"]: _clip(c["bounds"], probe["bounds"]) for c in level["cells"]}
        h = {e: _area(b) if b is not None else F(0) for e, b in clips.items()}
        volume = _area(probe["bounds"])
        middles, data = [], {}
        for e in clips:
            row, tiles = _middle(e, clips, cache)
            _require(row["moments"][0] == h[e], "middle volume differs from zeroth moment")
            middles.append(row)
            data[e] = tiles
        pairs, j = [], {}
        for c, d in product(h, repeat=2):
            value = sum((_linear(t["outgoing"][d], LINEAR, t["moments"]) for t in data[c]), F(0))
            denominator = h[c] * h[d]
            _require(0 <= value <= denominator, "pair integral outside product volume")
            j[c, d] = value
            pairs.append(
                {
                    "first": c,
                    "second": d,
                    "volume_product": denominator,
                    "causal_integral": value,
                    "conditional": value / denominator if denominator else None,
                }
            )
        triples, triple_values, flags = [], {}, {}
        for a, b, c in product(h, repeat=3):
            value = sum(
                (_linear(t["propagated"][a, b], QUADRATIC, t["moments"]) for t in data[c]), F(0)
            )
            forced = sum((_linear(t["forced"][a, b], LINEAR, t["moments"]) for t in data[c]), F(0))
            flag = all(t["flags"][a, b] for t in data[c])
            denominator = h[a] * h[b] * h[c]
            _require(0 <= value <= forced <= denominator, "triple or forced bound failed")
            triple_values[a, b, c], flags[a, b, c] = value, flag
            triples.append(
                {
                    "first": a,
                    "second": b,
                    "third": c,
                    "volume_product": denominator,
                    "causal_integral": value,
                    "forced_integral": forced,
                    "forced_error": forced - value,
                    "conditional": value / denominator if denominator else None,
                    "forced_conditional": forced / denominator if denominator else None,
                    "propagated_bilinear": flag,
                }
            )
        quadruples, quad_values = [], {}
        for a, b, c, d in product(h, repeat=4):
            value = sum(
                (
                    _cross(
                        t["propagated"][a, b],
                        QUADRATIC,
                        t["outgoing"][d],
                        t["moments"],
                        cache["cross"],
                    )
                    for t in data[c]
                ),
                F(0),
            )
            forced = sum(
                (
                    _cross(
                        t["forced"][a, b], LINEAR, t["outgoing"][d], t["moments"], cache["cross"]
                    )
                    for t in data[c]
                ),
                F(0),
            )
            denominator = h[a] * h[b] * h[c] * h[d]
            _require(
                0 <= value <= forced <= denominator,
                "four-point or corner-forced upper bound failed",
            )
            mean = error = covariance = centered = None
            if h[c]:
                f_mean, r_mean = triple_values[a, b, c] / h[c], j[c, d] / h[c]
                mean = triple_values[a, b, c] * j[c, d] / h[c]
                centered = sum(
                    (
                        _cross(
                            _center(t["propagated"][a, b], f_mean),
                            QUADRATIC,
                            _center(t["outgoing"][d], r_mean),
                            t["moments"],
                            cache["cross"],
                        )
                        for t in data[c]
                    ),
                    F(0),
                )
                _require(centered == value - mean, "centered coefficient contraction differs")
                error, covariance = mean - value, centered / h[c]
            else:
                _require(
                    value == forced == triple_values[a, b, c] == j[c, d] == 0,
                    "empty C has nonzero measure",
                )
            quad_values[a, b, c, d] = value
            quadruples.append(
                {
                    "first": a,
                    "second": b,
                    "third": c,
                    "last": d,
                    "volume_product": denominator,
                    "causal_integral": value,
                    "forced_integral": forced,
                    "forced_error": forced - value,
                    "mean_product": mean,
                    "mean_error": error,
                    "conditional": value / denominator if denominator else None,
                    "forced_conditional": forced / denominator if denominator else None,
                    "mean_conditional": mean / denominator if denominator else None,
                    "third_covariance": covariance,
                    "centered_integral": centered,
                    "propagated_bilinear": flags[a, b, c],
                }
            )
        pair_total = sum(j.values(), F(0))
        triple_total = sum(triple_values.values(), F(0))
        quad_total = sum(quad_values.values(), F(0))
        _require(pair_total == volume**2 / 4, "complete pair partition identity failed")
        _require(triple_total == volume**3 / 36, "complete triple partition identity failed")
        _require(quad_total == volume**4 / 576, "complete four-point partition identity failed")
        forced_total = sum((q["forced_integral"] for q in quadruples), F(0))
        mean_total = sum(
            (q["mean_product"] for q in quadruples if q["mean_product"] is not None), F(0)
        )
        geometry.append(
            {
                "probe": probe["name"],
                "volume": volume,
                "cells": [{"event": e, "clipped_volume": v} for e, v in h.items()],
                "middles": middles,
                "pairs": pairs,
                "triples": triples,
                "quadruples": quadruples,
                "summary": {
                    "pair_integral": pair_total,
                    "pair_continuum_integral": volume**2 / 4,
                    "triple_integral": triple_total,
                    "triple_continuum_integral": volume**3 / 36,
                    "quadruple_integral": quad_total,
                    "quadruple_continuum_integral": volume**4 / 576,
                    "forced_integral": forced_total,
                    "forced_error": forced_total - quad_total,
                    "mean_product": mean_total,
                    "mean_error": mean_total - quad_total,
                },
            }
        )
        retained_data.append(({r["event"]: r for r in middles}, data, quad_values))
    return {"level": level["level"], "geometry": geometry}, retained_data


def _coarsening(coarse, fine, groups, probes, old_data, new_data, via=None):
    geometry = []
    for qi, probe in enumerate(probes):
        old_middles, old_tiles, old_values = old_data[qi]
        middles, tiles, values = new_data[qi]
        moment_blocks = []
        for parent, children in groups.items():
            child_sum = [sum((middles[e]["moments"][i] for e in children), F(0)) for i in range(16)]
            _require(child_sum == old_middles[parent]["moments"], "coarsened raw moments differ")
            moment_blocks.append(
                {
                    "parent": parent,
                    "children": list(children),
                    "coarse_moments": list(old_middles[parent]["moments"]),
                    "child_moment_sum": child_sum,
                }
            )
        placement = {}
        for c, children in groups.items():
            for child in children:
                for fi, fine_tile in enumerate(middles[child]["tiles"]):
                    matches = [
                        i
                        for i, old_tile in enumerate(old_middles[c]["tiles"])
                        if _contains(old_tile["bounds"], fine_tile["bounds"])
                    ]
                    _require(len(matches) == 1, "fine tile requires exactly one coarse tile")
                    placement[child, fi] = matches[0]
        field_blocks = []
        for a, b, c in product(groups, repeat=3):
            pieces = []
            for child in groups[c]:
                for fi, fine_tile in enumerate(tiles[child]):
                    ci = placement[child, fi]
                    field = old_tiles[c][ci]["propagated"][a, b]
                    child_sum = [
                        sum(
                            (
                                fine_tile["propagated"][x, y][i]
                                for x, y in product(groups[a], groups[b])
                            ),
                            F(0),
                        )
                        for i in range(9)
                    ]
                    _require(
                        child_sum == list(field), "pointwise propagated-field coarsening differs"
                    )
                    pieces.append(
                        {
                            "child": child,
                            "fine_tile": fi,
                            "coarse_tile": ci,
                            "coarse_coefficients": list(field),
                            "child_coefficient_sum": child_sum,
                        }
                    )
            field_blocks.append({"first": a, "second": b, "third": c, "pieces": pieces})
        via_table = None
        if via is not None:
            via_groups, reconstructed = via
            via_table = {
                (r["first"], r["second"], r["third"], r["last"]): r["child_integral_sum"]
                for r in reconstructed["geometry"][qi]["blocks"]
            }
        blocks = []
        for a, b, c, d in product(groups, repeat=4):
            children = list(product(groups[a], groups[b], groups[c], groups[d]))
            total = sum((values[row] for row in children), F(0))
            _require(total == old_values[a, b, c, d], "true four-point block additivity differs")
            via_integral = None
            if via_table is not None:
                via_integral = sum(
                    (
                        via_table[row]
                        for row in product(
                            via_groups[a], via_groups[b], via_groups[c], via_groups[d]
                        )
                    ),
                    F(0),
                )
                _require(via_integral == total, "via-middle true four-point sum differs")
            blocks.append(
                {
                    "first": a,
                    "second": b,
                    "third": c,
                    "last": d,
                    "children": [list(row) for row in children],
                    "coarse_integral": old_values[a, b, c, d],
                    "child_integral_sum": total,
                    "via_middle_integral": via_integral,
                }
            )
        geometry.append(
            {
                "probe": probe["name"],
                "moment_blocks": moment_blocks,
                "field_blocks": field_blocks,
                "blocks": blocks,
            }
        )
    return {
        "coarse": coarse["level"],
        "fine": fine["level"],
        "parents": [{"parent": p, "children": list(xs)} for p, xs in groups.items()],
        "geometry": geometry,
    }


def _counts(levels, coarsenings, probe_count):
    names = [
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
    counts = dict.fromkeys(names, 0)
    counts.update({"levels": len(levels), "probes": probe_count})
    for level in levels:
        for q in level["geometry"]:
            counts["level_pairs"] += len(q["pairs"])
            counts["level_triples"] += len(q["triples"])
            counts["level_quadruples"] += len(q["quadruples"])
            n = len(q["cells"])
            for middle in q["middles"]:
                counts["middle_cells"] += 1
                counts["positive_middle_cells"] += middle["bounds"] is not None
                counts["breakpoint_entries"] += len(middle["u_breaks"]) + len(middle["v_breaks"])
                counts["tiles"] += len(middle["tiles"])
                counts["quadruple_tile_visits"] += n**3 * len(middle["tiles"])
                for tile in middle["tiles"]:
                    counts["propagated_vectors"] += len(tile["propagated"])
                    counts["outgoing_vectors"] += len(tile["outgoing"])
                    counts["nonbilinear_propagated_vectors"] += sum(
                        not r["bilinear_admissible"] for r in tile["propagated"]
                    )
            for row in q["quadruples"]:
                counts["positive_quadruples"] += row["causal_integral"] > 0
                counts["undefined_quad_conditionals"] += row["conditional"] is None
                counts["zero_third_quadruples"] += row["mean_product"] is None
                counts["nonbilinear_quadruples"] += not row["propagated_bilinear"]
                counts["nonbilinear_forced_equalities"] += (
                    not row["propagated_bilinear"] and row["forced_error"] == 0
                )
                for prefix, field in (("forced", "forced_error"), ("mean", "mean_error")):
                    value = row[field]
                    if value is not None:
                        sign = "positive" if value > 0 else "negative" if value < 0 else "zero"
                        counts[prefix + "_" + sign + "_errors"] += 1
    for link in coarsenings:
        groups = {row["parent"]: row["children"] for row in link["parents"]}
        for q in link["geometry"]:
            counts["coarsening_moment_blocks"] += len(q["moment_blocks"])
            counts["field_blocks"] += len(q["field_blocks"])
            for field in q["field_blocks"]:
                count = len(field["pieces"])
                counts["field_pieces"] += count
                counts["field_child_terms"] += (
                    count * len(groups[field["first"]]) * len(groups[field["second"]])
                )
            counts["blocks"] += len(q["blocks"])
            counts["child_terms"] += sum(len(r["children"]) for r in q["blocks"])
            counts["via_middle_blocks"] += sum(
                r["via_middle_integral"] is not None for r in q["blocks"]
            )
    counts.update(
        {
            "middle_bound_entries": 4 * counts["positive_middle_cells"],
            "tile_bound_entries": 4 * counts["tiles"],
            "middle_moment_entries": 16 * counts["middle_cells"],
            "tile_moment_entries": 16 * counts["tiles"],
            "propagated_entries": 9 * counts["propagated_vectors"],
            "forced_vectors": counts["propagated_vectors"],
            "forced_entries": 4 * counts["propagated_vectors"],
            "outgoing_entries": 4 * counts["outgoing_vectors"],
            "coarsening_moment_entries": 32 * counts["coarsening_moment_blocks"],
            "field_coefficient_entries": 18 * counts["field_pieces"],
        }
    )
    return counts


def build_family(problem):
    """Return the complete detached degree-aware representation and evidence."""
    probes, sources = _parse(problem)
    lineages = {(a, b): _lineage(sources[a], sources[b]) for a, b in LINKS}
    for child, parent in lineages[0, 2][1].items():
        _require(
            lineages[0, 1][1][lineages[1, 2][1][child]] == parent,
            "direct and composed full parent maps differ",
        )
    cache = {"moments": {}, "fields": {}, "outgoing": {}, "cross": {}}
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
