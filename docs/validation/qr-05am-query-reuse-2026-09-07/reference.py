"""Independent exact query reuse with explicit new-child moment derivation.

Old supplied moments are geometrically checked, never replaced. That reference
verification uses private tensor-Simpson integration, not the derive_moments
hook. The hook is called once per derived piece and never for a retained piece.
Function admission uses full knot-grid certification of corner interpolants;
exact contractions are checked against direct clamp and centered integrals.
"""

from copy import deepcopy
from fractions import Fraction
from itertools import combinations, pairwise, product
from math import gcd

MAX_BITS = 4096
BASIS = ((0, 0), (1, 0), (0, 1), (1, 1))
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
FAMILY_COUNTS = (
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
    _require(type(value) is list and len(value) == 2, "native rational pair")
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


def _rectangle(value):
    _require(type(value) is list and len(value) == 4, "rectangle bounds")
    bounds = tuple(_fraction(item) for item in value)
    _require(bounds[0] < bounds[1] and bounds[2] < bounds[3], "positive rectangle")
    return bounds


def _volume(bounds):
    if bounds is None:
        return Fraction(0)
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) / 2


def _contains(parent, child):
    return (
        parent[0] <= child[0] <= child[1] <= parent[1]
        and parent[2] <= child[2] <= child[3] <= parent[3]
    )


def _overlap(first, second):
    return max(first[0], second[0]) < min(first[1], second[1]) and max(first[2], second[2]) < min(
        first[3], second[3]
    )


def _nodes(bounds):
    u0, u1, v0, v1 = bounds
    us = ((u0, 1), ((u0 + u1) / 2, 4), (u1, 1))
    vs = ((v0, 1), ((v0 + v1) / 2, 4), (v1, 1))
    h = _volume(bounds)
    return tuple((u, v, h * wu * wv / 36) for (u, wu), (v, wv) in product(us, vs))


def _geometric_moments(bounds):
    """Reference verification primitive, deliberately separate from the hook."""
    if bounds is None:
        return (Fraction(0),) * 9
    nodes = _nodes(bounds)
    return tuple(
        sum((weight * u**i * v**j for u, v, weight in nodes), Fraction(0))
        for i, j in product(range(3), repeat=2)
    )


def derive_moments(bounds):
    """Explicit derivation hook: one call for EACH new positive child piece."""
    return [_wire(value) for value in _geometric_moments(_rectangle(bounds))]


def _moment_vector(value):
    _require(type(value) is list and len(value) == 9, "nine raw moments")
    return tuple(_fraction(item) for item in value)


def _check_old_moments(supplied, bounds):
    values = _moment_vector(supplied)
    _require(values == _geometric_moments(bounds), "supplied old moments disagree with geometry")
    return values


def _gram(moments):
    m = tuple(moments[3 * i + j] for i, j in BASIS)
    gram = tuple(tuple(moments[3 * (i + k) + j + ell] for k, ell in BASIS) for i, j in BASIS)
    _require(m[0] > 0, "positive piece moment volume")
    for i, j in product(range(4), repeat=2):
        _require(gram[i][j] == gram[j][i], "symmetric Gram matrix")
        if i == 0 or j == 0:
            _require(gram[i][j] == m[i] * m[j] / m[0], "constant centered row")
    return m, gram


def _dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def _bilinear(left, gram, right):
    return _dot(left, tuple(_dot(row, right) for row in gram))


def _clamp(endpoint, u, v, incoming):
    if endpoint is None:
        return Fraction(0)
    a, b, c, d = endpoint
    if incoming:
        first, second = max(Fraction(0), min(b, u) - a), max(Fraction(0), min(d, v) - c)
    else:
        first, second = max(Fraction(0), b - max(a, u)), max(Fraction(0), d - max(c, v))
    return first * second / 2


def _corner_fit(endpoint, bounds, incoming):
    u0, u1, v0, v1 = bounds
    f00, f10 = _clamp(endpoint, u0, v0, incoming), _clamp(endpoint, u1, v0, incoming)
    f01, f11 = _clamp(endpoint, u0, v1, incoming), _clamp(endpoint, u1, v1, incoming)
    mixed = (f11 - f10 - f01 + f00) / ((u1 - u0) * (v1 - v0))
    cu = (f10 - f00) / (u1 - u0) - mixed * v0
    cv = (f01 - f00) / (v1 - v0) - mixed * u0
    return (f00 - cu * u0 - cv * v0 - mixed * u0 * v0, cu, cv, mixed)


def _breaks(bounds, endpoints):
    u0, u1, v0, v1 = bounds
    us, vs = {u0, u1}, {v0, v1}
    for endpoint in endpoints:
        if endpoint is not None:
            us.update(value for value in endpoint[:2] if u0 < value < u1)
            vs.update(value for value in endpoint[2:] if v0 < value < v1)
    return sorted(us), sorted(vs)


def _certify(endpoint, bounds, incoming):
    coefficients = _corner_fit(endpoint, bounds, incoming)
    us, vs = _breaks(bounds, (endpoint,))
    # Each knot rectangle has a bilinear clamp function. Checking ALL its
    # corners certifies equality everywhere, including inactive/zero factors.
    admissible = all(
        _dot(coefficients, (1, u, v, u * v)) == _clamp(endpoint, u, v, incoming)
        for u, v in product(us, vs)
    )
    return admissible, coefficients


def _piece(bounds, supplied_moments, incoming, outgoing):
    moments = _moment_vector(supplied_moments)
    _require(moments[0] == _volume(bounds), "piece volume moment")
    left_ok, left = _certify(incoming, bounds, True)
    right_ok, right = _certify(outgoing, bounds, False)
    _require(left_ok and right_ok, "exact refined/retained piece admission")
    means, gram = _gram(moments)
    nodes = _nodes(bounds)
    values_left = tuple(_clamp(incoming, u, v, True) for u, v, _ in nodes)
    values_right = tuple(_clamp(outgoing, u, v, False) for u, v, _ in nodes)
    jin = sum(
        (weight * value for (_, _, weight), value in zip(nodes, values_left, strict=True)),
        Fraction(0),
    )
    jout = sum(
        (weight * value for (_, _, weight), value in zip(nodes, values_right, strict=True)),
        Fraction(0),
    )
    triple = sum(
        (
            weight * a * b
            for (_, _, weight), a, b in zip(nodes, values_left, values_right, strict=True)
        ),
        Fraction(0),
    )
    _require(
        _dot(left, means) == jin and _dot(right, means) == jout,
        "pair contraction/direct clamp agreement",
    )
    _require(_bilinear(left, gram, right) == triple, "triple contraction/direct clamp agreement")
    return {
        "moments": moments,
        "left": left,
        "right": right,
        "gram": gram,
        "nodes": nodes,
        "left_values": values_left,
        "right_values": values_right,
        "jin": jin,
        "jout": jout,
        "triple": triple,
    }


def _query(middle, query):
    incoming, outgoing = query["incoming"], query["outgoing"]
    old_rows, pieces, internal, moment_blocks = [], [], [], []
    counts = dict.fromkeys(QUERY_COUNTS, 0)
    forced_in = forced_out = forced_triple = Fraction(0)
    for parent, old in enumerate(middle["tiles"]):
        bounds, moments = old["bounds"], old["moments"]
        left_ok, forced_left = _certify(incoming, bounds, True)
        right_ok, forced_right = _certify(outgoing, bounds, False)
        admissible = left_ok and right_ok
        old_rows.append(
            {
                "tile": parent,
                "incoming_admissible": left_ok,
                "outgoing_admissible": right_ok,
                "forced_incoming": [_wire(value) for value in forced_left],
                "forced_outgoing": [_wire(value) for value in forced_right],
            }
        )
        means, gram = _gram(moments)
        forced_in += _dot(forced_left, means)
        forced_out += _dot(forced_right, means)
        forced_triple += _bilinear(forced_left, gram, forced_right)
        counts["old_tiles"] += 1
        counts["admissible_old_tiles"] += int(admissible)
        counts["unsupported_old_tiles"] += int(not admissible)
        counts["replaced_old_tiles"] += int(not admissible)
        counts["forced_coefficient_vectors"] += 2
        counts["forced_coefficient_entries"] += 8
        if admissible:
            specifications = [
                (
                    bounds,
                    deepcopy(old["wire"]["bounds"]),
                    deepcopy(old["wire"]["moments"]),
                    "retained",
                )
            ]
        else:
            us, vs = _breaks(bounds, (incoming, outgoing))
            _require((len(us) - 1) * (len(vs) - 1) <= 25, "bounded child grid")
            specifications = []
            for (u0, u1), (v0, v1) in product(pairwise(us), pairwise(vs)):
                child = (u0, u1, v0, v1)
                child_wire = [_wire(value) for value in child]
                derived = derive_moments(deepcopy(child_wire))
                counts["moment_derivation_calls"] += 1
                _moment_vector(derived)
                specifications.append((child, child_wire, deepcopy(derived), "derived"))
        indices = []
        for child, child_wire, moment_wire, source in specifications:
            calculated = _piece(child, moment_wire, incoming, outgoing)
            indices.append(len(pieces))
            internal.append(calculated)
            pieces.append(
                {
                    "parent": parent,
                    "bounds": child_wire,
                    "moments": moment_wire,
                    "moment_source": source,
                    "incoming_coefficients": [_wire(value) for value in calculated["left"]],
                    "outgoing_coefficients": [_wire(value) for value in calculated["right"]],
                }
            )
            counts[source + "_pieces"] += 1
            counts["new_moment_entries" if source == "derived" else "retained_moment_entries"] += 9
            counts["piece_bound_entries"] += 4
            counts["exact_coefficient_vectors"] += 2
            counts["exact_coefficient_entries"] += 8
        moment_sum = tuple(
            sum((internal[index]["moments"][coordinate] for index in indices), Fraction(0))
            for coordinate in range(9)
        )
        _require(moment_sum == moments, "all nine old/piece moments preserved")
        moment_blocks.append(
            {
                "parent": parent,
                "children": indices,
                "old_moments": deepcopy(old["wire"]["moments"]),
                "piece_moment_sum": [_wire(value) for value in moment_sum],
            }
        )
        counts["moment_blocks"] += 1
        counts["moment_block_entries"] += 18
    h = _volume(middle["bounds"])
    if not h:
        admission = "empty_middle"
    elif counts["unsupported_old_tiles"]:
        admission = "refine"
    else:
        admission = "reuse"
    jin = sum((piece["jin"] for piece in internal), Fraction(0))
    jout = sum((piece["jout"] for piece in internal), Fraction(0))
    triple = sum((piece["triple"] for piece in internal), Fraction(0))
    pair_product = forced_product = covariance = centered = None
    if h:
        pair_product, forced_product = jin * jout / h, forced_in * forced_out / h
        mean_left, mean_right = jin / h, jout / h
        centered = Fraction(0)
        for piece in internal:
            left, right = list(piece["left"]), list(piece["right"])
            left[0] -= mean_left
            right[0] -= mean_right
            contracted = _bilinear(left, piece["gram"], right)
            direct = sum(
                (
                    weight * (a - mean_left) * (b - mean_right)
                    for (_, _, weight), a, b in zip(
                        piece["nodes"], piece["left_values"], piece["right_values"], strict=True
                    )
                ),
                Fraction(0),
            )
            _require(contracted == direct, "centered contraction/direct clamp agreement")
            centered += direct
        _require(centered == triple - pair_product, "whole-middle centered identity")
        covariance = centered / h
    incoming_volume, outgoing_volume = _volume(incoming), _volume(outgoing)
    denominator = incoming_volume * h * outgoing_volume
    incoming_error, outgoing_error, forced_error = (
        forced_in - jin,
        forced_out - jout,
        forced_triple - triple,
    )
    result = {
        "middle_volume": _wire(h),
        "incoming_volume": _wire(incoming_volume),
        "outgoing_volume": _wire(outgoing_volume),
        "volume_product": _wire(denominator),
        "incoming_pair": _wire(jin),
        "outgoing_pair": _wire(jout),
        "causal_integral": _wire(triple),
        "pair_product": _wire(pair_product),
        "conditional": _wire(triple / denominator if denominator else None),
        "product_conditional": _wire(pair_product / denominator if denominator else None),
        "middle_covariance": _wire(covariance),
        "centered_integral": _wire(centered),
        "forced_incoming_pair": _wire(forced_in),
        "forced_outgoing_pair": _wire(forced_out),
        "forced_integral": _wire(forced_triple),
        "forced_pair_product": _wire(forced_product),
        "forced_conditional": _wire(forced_triple / denominator if denominator else None),
        "forced_product_conditional": _wire(forced_product / denominator if denominator else None),
        "incoming_pair_error": _wire(incoming_error),
        "outgoing_pair_error": _wire(outgoing_error),
        "forced_error": _wire(forced_error),
        "reuse_incoming_pair": _wire(jin if admission == "reuse" else None),
        "reuse_outgoing_pair": _wire(jout if admission == "reuse" else None),
        "reuse_integral": _wire(triple if admission == "reuse" else None),
    }
    _require(
        counts["moment_derivation_calls"] == counts["derived_pieces"],
        "explicit derivation accounting",
    )
    return {
        "name": query["name"],
        "admission": admission,
        "old_tiles": old_rows,
        "pieces": pieces,
        "moment_blocks": moment_blocks,
        "result": result,
        "counts": counts,
    }


def _prepare(problem):
    _object(problem, ("family", "contexts"))
    _label(problem["family"])
    _require(
        type(problem["contexts"]) is list and 1 <= len(problem["contexts"]) <= 15,
        "bounded context inventory",
    )
    contexts, context_keys, levels, probes = [], set(), set(), set()
    for context in problem["contexts"]:
        _object(context, ("level", "probe", "probe_bounds", "middles"))
        level, probe = _label(context["level"]), _label(context["probe"])
        _require((level, probe) not in context_keys, "unique level/probe context")
        context_keys.add((level, probe))
        levels.add(level)
        probes.add(probe)
        query_bounds = _rectangle(context["probe_bounds"])
        _require(
            type(context["middles"]) is list and 1 <= len(context["middles"]) <= 8,
            "middle inventory",
        )
        middles, ids, positive_rectangles = [], [], []
        for old in context["middles"]:
            _object(old, ("event", "bounds", "u_breaks", "v_breaks", "moments", "tiles", "queries"))
            event = _integer(old["event"])
            ids.append(event)
            bounds = None if old["bounds"] is None else _rectangle(old["bounds"])
            whole = _check_old_moments(old["moments"], bounds)
            _require(
                type(old["u_breaks"]) is list
                and type(old["v_breaks"]) is list
                and type(old["tiles"]) is list,
                "native grid lists",
            )
            us, vs = (
                tuple(_fraction(value) for value in old["u_breaks"]),
                tuple(_fraction(value) for value in old["v_breaks"]),
            )
            tiles = []
            if bounds is None:
                _require(not us and not vs and not old["tiles"], "empty middle grid")
            else:
                _require(_contains(query_bounds, bounds), "middle inside probe")
                positive_rectangles.append(bounds)
                _require(
                    len(us) >= 2
                    and len(vs) >= 2
                    and list(us) == sorted(set(us))
                    and list(vs) == sorted(set(vs)),
                    "strict grid breakpoints",
                )
                _require((us[0], us[-1], vs[0], vs[-1]) == bounds, "boundary-complete grid")
                expected = [(a, b, c, d) for (a, b), (c, d) in product(pairwise(us), pairwise(vs))]
                _require(
                    len(expected) <= 289 and len(old["tiles"]) == len(expected),
                    "complete bounded tile grid",
                )
                for tile, expected_bounds in zip(old["tiles"], expected, strict=True):
                    _object(tile, ("bounds", "moments"))
                    tile_bounds = _rectangle(tile["bounds"])
                    _require(tile_bounds == expected_bounds, "tile Cartesian order")
                    tile_moments = _check_old_moments(tile["moments"], tile_bounds)
                    tiles.append({"bounds": tile_bounds, "moments": tile_moments, "wire": tile})
                summed = tuple(
                    sum((tile["moments"][index] for tile in tiles), Fraction(0))
                    for index in range(9)
                )
                _require(summed == whole, "whole/tile moment additivity")
            _require(
                type(old["queries"]) is list and 1 <= len(old["queries"]) <= 5, "query inventory"
            )
            queries, names = [], set()
            for query in old["queries"]:
                _object(query, ("name", "incoming", "outgoing"))
                name = _label(query["name"])
                _require(name not in names, "unique query names")
                names.add(name)
                incoming = None if query["incoming"] is None else _rectangle(query["incoming"])
                outgoing = None if query["outgoing"] is None else _rectangle(query["outgoing"])
                queries.append({"name": name, "incoming": incoming, "outgoing": outgoing})
            middles.append(
                {"event": event, "bounds": bounds, "tiles": tiles, "queries": queries, "wire": old}
            )
        _require(ids == sorted(set(ids)), "sorted unique signed middle IDs")
        for first, second in combinations(positive_rectangles, 2):
            _require(not _overlap(first, second), "disjoint middle interiors")
        _require(
            sum((_volume(rectangle) for rectangle in positive_rectangles), Fraction(0))
            == _volume(query_bounds),
            "complete probe coverage",
        )
        contexts.append({"level": level, "probe": probe, "middles": middles})
    _require(len(levels) <= 3 and len(probes) <= 5, "distinct context label bounds")
    return contexts


def build_family(problem):
    """Consume the supplied snapshot and independently verify exact query reuse."""
    prepared = _prepare(problem)
    counts = dict.fromkeys(QUERY_COUNTS + FAMILY_COUNTS, 0)
    counts["contexts"] = len(prepared)
    output = []
    for context in prepared:
        middle_rows = []
        for middle in context["middles"]:
            old = middle["wire"]
            positive = middle["bounds"] is not None
            counts["middle_rows"] += 1
            counts["positive_middle_rows"] += int(positive)
            counts["snapshot_tiles"] += len(middle["tiles"])
            counts["snapshot_moment_entries"] += 9 * (1 + len(middle["tiles"]))
            counts["snapshot_bound_entries"] += (
                4 * int(positive)
                + 4 * len(middle["tiles"])
                + len(old["u_breaks"])
                + len(old["v_breaks"])
            )
            results = []
            for query in middle["queries"]:
                row = _query(middle, query)
                results.append(row)
                counts["queries"] += 1
                counts["endpoint_bound_entries"] += 4 * (
                    (query["incoming"] is not None) + (query["outgoing"] is not None)
                )
                category = {
                    "empty_middle": "empty_middle_queries",
                    "reuse": "reuse_queries",
                    "refine": "refinement_queries",
                }[row["admission"]]
                counts[category] += 1
                counts["positive_exact_queries"] += int(
                    _fraction(row["result"]["causal_integral"]) > 0
                )
                if positive:
                    error = _fraction(row["result"]["forced_error"])
                    sign = "positive" if error > 0 else "negative" if error < 0 else "zero"
                    counts["forced_" + sign + "_errors"] += 1
                    counts["refinement_forced_equalities"] += int(
                        row["admission"] == "refine" and error == 0
                    )
                    counts["incoming_pair_disagreements"] += int(
                        _fraction(row["result"]["incoming_pair_error"]) != 0
                    )
                    counts["outgoing_pair_disagreements"] += int(
                        _fraction(row["result"]["outgoing_pair_error"]) != 0
                    )
                for name in QUERY_COUNTS:
                    counts[name] += row["counts"][name]
            middle_rows.append({"event": middle["event"], "queries": results})
        output.append(
            {"level": context["level"], "probe": context["probe"], "middles": middle_rows}
        )
    return {"problem": deepcopy(problem), "contexts": output, "counts": counts}
