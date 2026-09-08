"""Private reuse of supplied middle moments with explicit new-child derivation.

Old higher moments are trusted data, not geometrically authenticated here.
No historical executor is imported and no old moment is silently regenerated.
"""

import json
from fractions import Fraction as F
from itertools import combinations, pairwise, product
from math import gcd

EXPONENTS = ((0, 0), (1, 0), (0, 1), (1, 1))
QUERY_COUNTS = (
    "old_tiles",
    "admissible_old_tiles",
    "unsupported_old_tiles",
    "retained_pieces",
    "derived_pieces",
    "replaced_old_tiles",
    "moment_derivation_calls",
    "forced_coefficient_vectors",
    "forced_coefficient_entries",
    "exact_coefficient_vectors",
    "exact_coefficient_entries",
    "new_moment_entries",
    "retained_moment_entries",
    "piece_bound_entries",
    "moment_blocks",
    "moment_block_entries",
)


def _require(ok, message):
    if not ok:
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
        _require(all(type(k) is str for k in value), "native string keys required")
        for child in value.values():
            _native(child)
    else:
        raise ValueError("native mathematical wire required")


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
        and gcd(n, d) == 1
        and max(n.bit_length(), d.bit_length()) <= 4096,
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
        return [_encode(v) for v in value]
    if type(value) is dict:
        return {k: _encode(v) for k, v in value.items()}
    return value


def _rectangle(value):
    _require(type(value) is list and len(value) == 4, "four rational bounds required")
    b = tuple(map(_fraction, value))
    _require(b[0] < b[1] and b[2] < b[3], "positive rectangle required")
    return b


def _nine(value):
    _require(type(value) is list and len(value) == 9, "nine supplied raw moments required")
    return list(map(_fraction, value))


def _area(b):
    return F(0) if b is None else (b[1] - b[0]) * (b[3] - b[2]) / 2


def _contains(a, b):
    return a[0] <= b[0] <= b[1] <= a[1] and a[2] <= b[2] <= b[3] <= a[3]


def _overlap(a, b):
    return max(a[0], b[0]) < min(a[1], b[1]) and max(a[2], b[2]) < min(a[3], b[3])


def derive_moments(bounds):
    """Explicit once-per-derived-piece hook; never used to validate old moments."""
    u0, u1, v0, v1 = _rectangle(bounds)
    us = [(u1 ** (i + 1) - u0 ** (i + 1)) / (i + 1) for i in range(3)]
    vs = [(v1 ** (j + 1) - v0 ** (j + 1)) / (j + 1) for j in range(3)]
    return _encode([u * v / 2 for u, v in product(us, vs)])


def _breaks(value, low, high):
    _require(type(value) is list and len(value) >= 2, "boundary-complete breakpoints required")
    points = list(map(_fraction, value))
    _require(
        points == sorted(set(points)) and points[0] == low and points[-1] == high,
        "strictly ordered boundary-complete breakpoints required",
    )
    return points


def _parse_middle(row):
    _fields(row, ("event", "bounds", "u_breaks", "v_breaks", "moments", "tiles", "queries"))
    _require(type(row["event"]) is int, "native level-local integer ID required")
    bounds = None if row["bounds"] is None else _rectangle(row["bounds"])
    moments = _nine(row["moments"])
    _require(type(row["tiles"]) is list and len(row["tiles"]) <= 289, "bounded old tile inventory")
    tiles = []
    if bounds is None:
        _require(
            row["u_breaks"] == []
            and type(row["u_breaks"]) is list
            and row["v_breaks"] == []
            and type(row["v_breaks"]) is list
            and row["tiles"] == []
            and moments == [F(0)] * 9,
            "empty middle must retain empty grid and zero moments",
        )
        ub, vb = [], []
    else:
        ub, vb = _breaks(row["u_breaks"], *bounds[:2]), _breaks(row["v_breaks"], *bounds[2:])
        _require(
            (len(ub) - 1) * (len(vb) - 1) == len(row["tiles"]),
            "complete old Cartesian grid required",
        )
        for supplied, (u, v) in zip(row["tiles"], product(pairwise(ub), pairwise(vb)), strict=True):
            _fields(supplied, ("bounds", "moments"))
            b, raw = _rectangle(supplied["bounds"]), _nine(supplied["moments"])
            _require(b == (*u, *v), "old tile grid order or bounds differ")
            _require(raw[0] == _area(b), "old zeroth moment differs from geometric volume")
            tiles.append({"bounds": b, "moments": raw})
        _require(moments[0] == _area(bounds), "whole-middle zeroth moment differs")
        _require(
            all(sum((t["moments"][i] for t in tiles), F(0)) == moments[i] for i in range(9)),
            "supplied whole and tile moments are not additive",
        )
    _require(
        type(row["queries"]) is list and 1 <= len(row["queries"]) <= 5,
        "bounded query inventory required",
    )
    queries, names = [], set()
    for q in row["queries"]:
        _fields(q, ("name", "incoming", "outgoing"))
        name = _label(q["name"])
        _require(name not in names, "unique middle query names required")
        names.add(name)
        queries.append(
            {
                "name": name,
                "incoming": None if q["incoming"] is None else _rectangle(q["incoming"]),
                "outgoing": None if q["outgoing"] is None else _rectangle(q["outgoing"]),
            }
        )
    return {
        "event": row["event"],
        "bounds": bounds,
        "moments": moments,
        "u_breaks": ub,
        "v_breaks": vb,
        "tiles": tiles,
        "queries": queries,
    }


def _parse(problem):
    _native(problem)
    _fields(problem, ("family", "contexts"))
    _label(problem["family"])
    _require(
        type(problem["contexts"]) is list and 1 <= len(problem["contexts"]) <= 15,
        "bounded context inventory required",
    )
    contexts, levels, probes, seen = [], set(), set(), set()
    for row in problem["contexts"]:
        _fields(row, ("level", "probe", "probe_bounds", "middles"))
        level, probe = _label(row["level"]), _label(row["probe"])
        _require((level, probe) not in seen, "unique level/probe contexts required")
        seen.add((level, probe))
        levels.add(level)
        probes.add(probe)
        _require(len(levels) <= 3 and len(probes) <= 5, "bounded level/probe label inventory")
        bounds = _rectangle(row["probe_bounds"])
        _require(
            type(row["middles"]) is list and 1 <= len(row["middles"]) <= 8,
            "bounded middle inventory required",
        )
        middles = [_parse_middle(m) for m in row["middles"]]
        ids = [m["event"] for m in middles]
        _require(ids == sorted(set(ids)), "sorted unique middle IDs required")
        positive = [m["bounds"] for m in middles if m["bounds"] is not None]
        _require(
            all(_contains(bounds, b) for b in positive)
            and all(not _overlap(a, b) for a, b in combinations(positive, 2))
            and sum(map(_area, positive), F(0)) == _area(bounds),
            "middle rectangles must disjointly cover the probe",
        )
        contexts.append(
            {"level": level, "probe": probe, "probe_bounds": bounds, "middles": middles}
        )
    return contexts


def _zero(endpoint, tile, incoming):
    if endpoint is None:
        return True
    return (
        (tile[1] <= endpoint[0] or tile[3] <= endpoint[2])
        if incoming
        else (tile[0] >= endpoint[1] or tile[2] >= endpoint[3])
    )


def _admissible(endpoint, tile, incoming):
    if _zero(endpoint, tile, incoming):
        return True
    return not any(
        tile[offset] < x < tile[offset + 1]
        for offset in (0, 2)
        for x in endpoint[offset : offset + 2]
    )


def _branch(endpoint, tile, incoming):
    a, b = endpoint
    lo, hi = tile
    if hi <= a:
        return (F(0), F(0)) if incoming else (b - a, F(0))
    if lo >= b:
        return (b - a, F(0)) if incoming else (F(0), F(0))
    _require(a <= lo and hi <= b, "piece crosses an active clamp branch")
    return (-a, F(1)) if incoming else (b, F(-1))


def _coefficients(endpoint, tile, incoming):
    _require(_admissible(endpoint, tile, incoming), "exact piece function is not bilinear")
    if _zero(endpoint, tile, incoming):
        return [F(0)] * 4
    uc, us = _branch(endpoint[:2], tile[:2], incoming)
    vc, vs = _branch(endpoint[2:], tile[2:], incoming)
    return [uc * vc / 2, us * vc / 2, uc * vs / 2, us * vs / 2]


def _value(endpoint, u, v, incoming):
    if endpoint is None:
        return F(0)
    a, b, c, d = endpoint
    if incoming:
        return max(F(0), min(u - a, b - a)) * max(F(0), min(v - c, d - c)) / 2
    return max(F(0), min(b - u, b - a)) * max(F(0), min(d - v, d - c)) / 2


def _corner_fit(endpoint, bounds, incoming):
    u0, u1, v0, v1 = bounds
    z00, z10, z01, z11 = [
        _value(endpoint, u, v, incoming) for u, v in ((u0, v0), (u1, v0), (u0, v1), (u1, v1))
    ]
    cross = (z11 - z10 - z01 + z00) / ((u1 - u0) * (v1 - v0))
    cu = (z10 - z00) / (u1 - u0) - cross * v0
    cv = (z01 - z00) / (v1 - v0) - cross * u0
    return [z00 - cu * u0 - cv * v0 - cross * u0 * v0, cu, cv, cross]


def _moments_for_contraction(raw):
    return (
        [raw[3 * i + j] for i, j in EXPONENTS],
        [[raw[3 * (i + k) + j + l] for k, l in EXPONENTS] for i, j in EXPONENTS],
    )


def _linear(coefficients, first):
    return sum((a * b for a, b in zip(coefficients, first, strict=True)), F(0))


def _contract(left, gram, right):
    return sum((left[a] * gram[a][b] * right[b] for a, b in product(range(4), repeat=2)), F(0))


def _center(coefficients, mean):
    return [coefficients[0] - mean, *coefficients[1:]]


def _subdivide(tile, incoming, outgoing):
    axes = []
    for offset in (0, 2):
        lo, hi = tile[offset : offset + 2]
        points = {lo, hi}
        for endpoint in (incoming, outgoing):
            if endpoint is not None:
                points.update(x for x in endpoint[offset : offset + 2] if lo < x < hi)
        axes.append(sorted(points))
    rectangles = [(*u, *v) for u, v in product(pairwise(axes[0]), pairwise(axes[1]))]
    _require(1 < len(rectangles) <= 25, "bounded nontrivial child grid required")
    return rectangles


def _query(middle, query):
    incoming, outgoing = query["incoming"], query["outgoing"]
    h = _area(middle["bounds"])
    old_tiles, pieces, moment_blocks = [], [], []
    exact_data, forced_data = [], []
    calls = unsupported = 0
    for index, old in enumerate(middle["tiles"]):
        bounds, moments = old["bounds"], old["moments"]
        ia, oa = _admissible(incoming, bounds, True), _admissible(outgoing, bounds, False)
        forced_in, forced_out = (
            _corner_fit(incoming, bounds, True),
            _corner_fit(outgoing, bounds, False),
        )
        old_tiles.append(
            {
                "tile": index,
                "incoming_admissible": ia,
                "outgoing_admissible": oa,
                "forced_incoming": forced_in,
                "forced_outgoing": forced_out,
            }
        )
        first, gram = _moments_for_contraction(moments)
        forced_data.append((first, gram, forced_in, forced_out))
        retained = ia and oa
        unsupported += not retained
        new_bounds = [bounds] if retained else _subdivide(bounds, incoming, outgoing)
        indices = []
        for b in new_bounds:
            if retained:
                raw = list(moments)
            else:
                # Intentionally no memoization: this public hook is the declared
                # once-per-new-piece work, even for equal geometry across queries.
                raw = _nine(derive_moments(_encode(list(b))))
                calls += 1
                _require(raw[0] == _area(b), "derived child zeroth moment differs")
            ell, r = _coefficients(incoming, b, True), _coefficients(outgoing, b, False)
            if retained:
                _require(
                    ell == forced_in and r == forced_out, "admitted fit disagrees with branches"
                )
            indices.append(len(pieces))
            pieces.append(
                {
                    "parent": index,
                    "bounds": list(b),
                    "moments": list(raw),
                    "moment_source": "retained" if retained else "derived",
                    "incoming_coefficients": ell,
                    "outgoing_coefficients": r,
                }
            )
            first, gram = _moments_for_contraction(raw)
            exact_data.append((first, gram, ell, r))
        summed = [sum((pieces[i]["moments"][j] for i in indices), F(0)) for j in range(9)]
        _require(summed == moments, "piece moments do not recover the supplied old vector")
        moment_blocks.append(
            {
                "parent": index,
                "children": indices,
                "old_moments": list(moments),
                "piece_moment_sum": summed,
            }
        )
    admission = "empty_middle" if not h else "refine" if unsupported else "reuse"
    ji = sum((_linear(ell, first) for first, _, ell, _ in exact_data), F(0))
    jo = sum((_linear(r, first) for first, _, _, r in exact_data), F(0))
    total = sum((_contract(ell, gram, r) for _, gram, ell, r in exact_data), F(0))
    fi = sum((_linear(ell, first) for first, _, ell, _ in forced_data), F(0))
    fo = sum((_linear(r, first) for first, _, _, r in forced_data), F(0))
    forced = sum((_contract(ell, gram, r) for _, gram, ell, r in forced_data), F(0))
    pair_product = ji * jo / h if h else None
    forced_product = fi * fo / h if h else None
    centered = covariance = None
    if h:
        centered = sum(
            (
                _contract(_center(ell, ji / h), gram, _center(r, jo / h))
                for _, gram, ell, r in exact_data
            ),
            F(0),
        )
        _require(centered == total - pair_product, "centered coefficient identity differs")
        covariance = centered / h
    volume_in, volume_out = _area(incoming), _area(outgoing)
    denominator = volume_in * h * volume_out
    result = {
        "middle_volume": h,
        "incoming_volume": volume_in,
        "outgoing_volume": volume_out,
        "volume_product": denominator,
        "incoming_pair": ji,
        "outgoing_pair": jo,
        "causal_integral": total,
        "pair_product": pair_product,
        "conditional": total / denominator if denominator else None,
        "product_conditional": pair_product / denominator if denominator else None,
        "middle_covariance": covariance,
        "centered_integral": centered,
        "forced_incoming_pair": fi,
        "forced_outgoing_pair": fo,
        "forced_integral": forced,
        "forced_pair_product": forced_product,
        "forced_conditional": forced / denominator if denominator else None,
        "forced_product_conditional": forced_product / denominator if denominator else None,
        "incoming_pair_error": fi - ji,
        "outgoing_pair_error": fo - jo,
        "forced_error": forced - total,
        "reuse_incoming_pair": ji if admission == "reuse" else None,
        "reuse_outgoing_pair": jo if admission == "reuse" else None,
        "reuse_integral": total if admission == "reuse" else None,
    }
    retained_count = sum(p["moment_source"] == "retained" for p in pieces)
    derived_count = len(pieces) - retained_count
    _require(calls == derived_count, "derivation hook count differs from derived pieces")
    counts = {
        "old_tiles": len(old_tiles),
        "admissible_old_tiles": len(old_tiles) - unsupported,
        "unsupported_old_tiles": unsupported,
        "retained_pieces": retained_count,
        "derived_pieces": derived_count,
        "replaced_old_tiles": unsupported,
        "moment_derivation_calls": calls,
        "forced_coefficient_vectors": 2 * len(old_tiles),
        "forced_coefficient_entries": 8 * len(old_tiles),
        "exact_coefficient_vectors": 2 * len(pieces),
        "exact_coefficient_entries": 8 * len(pieces),
        "new_moment_entries": 9 * derived_count,
        "retained_moment_entries": 9 * retained_count,
        "piece_bound_entries": 4 * len(pieces),
        "moment_blocks": len(moment_blocks),
        "moment_block_entries": 18 * len(moment_blocks),
    }
    return {
        "name": query["name"],
        "admission": admission,
        "old_tiles": old_tiles,
        "pieces": pieces,
        "moment_blocks": moment_blocks,
        "result": result,
        "counts": counts,
    }


def _counts(contexts, output):
    counts = dict.fromkeys(QUERY_COUNTS, 0)
    counts.update(
        dict.fromkeys(
            (
                "contexts",
                "middle_rows",
                "positive_middle_rows",
                "snapshot_tiles",
                "snapshot_moment_entries",
                "snapshot_bound_entries",
                "endpoint_bound_entries",
                "queries",
                "empty_middle_queries",
                "reuse_queries",
                "refinement_queries",
                "positive_exact_queries",
                "forced_positive_errors",
                "forced_zero_errors",
                "forced_negative_errors",
                "refinement_forced_equalities",
                "incoming_pair_disagreements",
                "outgoing_pair_disagreements",
            ),
            0,
        )
    )
    counts["contexts"] = len(contexts)
    for source, target in zip(contexts, output, strict=True):
        for middle, result in zip(source["middles"], target["middles"], strict=True):
            counts["middle_rows"] += 1
            counts["positive_middle_rows"] += middle["bounds"] is not None
            counts["snapshot_tiles"] += len(middle["tiles"])
            counts["snapshot_moment_entries"] += 9 * (1 + len(middle["tiles"]))
            counts["snapshot_bound_entries"] += (
                (4 if middle["bounds"] is not None else 0)
                + 4 * len(middle["tiles"])
                + len(middle["u_breaks"])
                + len(middle["v_breaks"])
            )
            counts["endpoint_bound_entries"] += sum(
                4 * ((q["incoming"] is not None) + (q["outgoing"] is not None))
                for q in middle["queries"]
            )
            for q in result["queries"]:
                counts["queries"] += 1
                key = {
                    "empty_middle": "empty_middle_queries",
                    "reuse": "reuse_queries",
                    "refine": "refinement_queries",
                }[q["admission"]]
                counts[key] += 1
                for name in QUERY_COUNTS:
                    counts[name] += q["counts"][name]
                values = q["result"]
                counts["positive_exact_queries"] += values["causal_integral"] > 0
                if values["middle_volume"]:
                    error = values["forced_error"]
                    sign = "positive" if error > 0 else "negative" if error < 0 else "zero"
                    counts["forced_" + sign + "_errors"] += 1
                    counts["refinement_forced_equalities"] += (
                        q["admission"] == "refine" and error == 0
                    )
                    counts["incoming_pair_disagreements"] += values["incoming_pair_error"] != 0
                    counts["outgoing_pair_disagreements"] += values["outgoing_pair_error"] != 0
    return counts


def build_family(problem):
    """Structurally validate and contract old data, deriving only new children."""
    contexts = _parse(problem)
    output = [
        {
            "level": c["level"],
            "probe": c["probe"],
            "middles": [
                {"event": m["event"], "queries": [_query(m, q) for q in m["queries"]]}
                for m in c["middles"]
            ],
        }
        for c in contexts
    ]
    result = _encode({"problem": problem, "contexts": output, "counts": _counts(contexts, output)})
    return json.loads(canonical(result))
