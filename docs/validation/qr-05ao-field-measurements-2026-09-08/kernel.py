"""Private exact coarse-field observations and canonical recovery certificates.

Geometry and matrices are offline evidence. The public decoder receives only
an observation vector and its fixed compact linear map, never hidden weights.
"""

import json
from fractions import Fraction as F
from itertools import combinations, pairwise, product
from math import gcd

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


def canonical(value):
    _native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def _detach(value):
    return json.loads(canonical(_encode(value)))


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


def _matrix_shape(value, minimum, width=None):
    _require(
        type(value) is list and minimum <= len(value) <= 32768,
        "bounded native matrix rows required",
    )
    if value and width is None:
        _require(
            type(value[0]) is list and 1 <= len(value[0]) <= 64,
            "bounded positive column dimension required",
        )
        width = len(value[0])
    _require(type(width) is int and 1 <= width <= 64, "bounded positive column dimension required")
    _require(
        all(type(row) is list and len(row) == width for row in value),
        "matrix rows must share their column dimension",
    )
    return width


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True) if x and y), F(0))


def _mv(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _mm(left, right):
    columns = list(zip(*right, strict=True))
    return [[_dot(row, column) for column in columns] for row in left]


def _independent_rows(matrix):
    """Greedy original-row basis using an independent incremental echelon form."""
    selected, echelon = [], {}
    for index, original in enumerate(matrix):
        row = list(original)
        for p in sorted(echelon):
            if row[p]:
                factor = row[p]
                row = [a - factor * b for a, b in zip(row, echelon[p], strict=True)]
        nonzero = next((j for j, x in enumerate(row) if x), None)
        if nonzero is not None:
            scale = row[nonzero]
            echelon[nonzero] = [x / scale for x in row]
            selected.append(index)
    return selected


def _rref(matrix, column_limit):
    """Gauss-Jordan form; columns after the limit are transformed augmentations."""
    rows = [list(row) for row in matrix]
    pivots = []
    for column in range(column_limit):
        k = len(pivots)
        found = next((i for i in range(k, len(rows)) if rows[i][column]), None)
        if found is None:
            continue
        rows[k], rows[found] = rows[found], rows[k]
        pivot = rows[k][column]
        rows[k] = [x / pivot for x in rows[k]]
        for i in range(len(rows)):
            if i != k and rows[i][column]:
                factor = rows[i][column]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[k], strict=True)]
        pivots.append(column)
        if len(pivots) == len(rows):
            break
    return rows, pivots


def _observation_data(observation, columns, cache):
    key = (columns, tuple(tuple(row) for row in observation))
    if key not in cache:
        augmented = [[F(1)] * columns, *observation]
        basis = _independent_rows(augmented)
        original = [augmented[i] for i in basis]
        reduced, pivots = _rref(original, columns)
        rank = len(basis)
        _require(len(pivots) == rank and basis[0] == 0, "observation basis differs")
        square = [[row[j] for j in pivots] for row in original]
        inverse, inverse_pivots = _rref(
            [row + [F(i == j) for j in range(rank)] for i, row in enumerate(square)], rank
        )
        _require(inverse_pivots == list(range(rank)), "basis pivot square is singular")
        cache[key] = augmented, basis, original, reduced, pivots, [row[rank:] for row in inverse]
    return cache[key]


def _certificate(observation, target, cache):
    columns = len(target[0])
    augmented, basis, original, reduced, pivots, inverse = _observation_data(
        observation, columns, cache
    )
    rank = len(basis)
    target_rank = len(_independent_rows(target))
    joint_rank = len(_independent_rows(augmented + target))
    recoverable = joint_rank == rank
    decoder = collision = None
    if recoverable:
        decoder = _mm([[row[j] for j in pivots] for row in target], inverse)
        _require(_mm(decoder, original) == target, "complete canonical decoder identity failed")
    else:
        # The protocol selects a FREE COLUMN before selecting a target row.
        # RREF has a unique standard vector for each such free column.
        for free in range(columns):
            if free in pivots:
                continue
            difference = [F(0)] * columns
            difference[free] = F(1)
            for i, p in enumerate(pivots):
                difference[p] = -reduced[i][free]
            target_direction = _mv(target, difference)
            if not any(target_direction):
                continue
            mass = sum((x for x in difference if x > 0), F(0))
            _require(
                mass > 0 and mass == -sum((x for x in difference if x < 0), F(0)),
                "kernel direction lacks convex-mixture normalization",
            )
            positive = [max(x, F(0)) / mass for x in difference]
            negative = [max(-x, F(0)) / mass for x in difference]
            op, om = _mv(observation, positive), _mv(observation, negative)
            qp, qm = _mv(target, positive), _mv(target, negative)
            delta = [a - b for a, b in zip(qp, qm, strict=True)]
            separating = next(i for i, value in enumerate(delta) if value)
            _require(
                all(x >= 0 for x in positive + negative)
                and sum(positive, F(0)) == sum(negative, F(0)) == 1,
                "mixture weights are invalid",
            )
            _require(
                _mv(augmented, difference) == [F(0)] * len(augmented) and op == om,
                "complete collision observations differ",
            )
            _require(
                delta == [x / mass for x in target_direction],
                "normalized target difference differs",
            )
            collision = {
                "free_column": free,
                "difference": difference,
                "positive_weights": positive,
                "negative_weights": negative,
                "observed_positive": op,
                "observed_negative": om,
                "target_positive": qp,
                "target_negative": qm,
                "target_difference": delta,
                "separating_row": separating,
            }
            break
        _require(collision is not None, "rank failure has no detecting canonical kernel vector")
    return {
        "observation_rank": rank,
        "target_rank": target_rank,
        "joint_rank": joint_rank,
        "row_basis": list(basis),
        "pivot_columns": list(pivots),
        "recoverable": recoverable,
        "decoder": decoder,
        "collision": collision,
    }


def certify(O, Q):
    """Canonical exact decoder or normalized nonnegative-mixture collision."""
    _native(O)
    _native(Q)
    columns = _matrix_shape(Q, 1)
    _matrix_shape(O, 0, columns)
    observation = [list(map(_fraction, row)) for row in O]
    target = [list(map(_fraction, row)) for row in Q]
    return _detach(_certificate(observation, target, {}))


def decode(row_basis, decoder, observed):
    """Apply a supplied compact decoder without accessing hidden field data."""
    _native([row_basis, decoder, observed])
    _require(
        type(observed) is list and len(observed) <= 32768, "bounded raw observation vector required"
    )
    _require(
        type(row_basis) is list
        and 1 <= len(row_basis) <= 64
        and all(type(i) is int for i in row_basis),
        "native nonempty basis indices required",
    )
    _require(
        row_basis == sorted(set(row_basis))
        and row_basis[0] == 0
        and row_basis[-1] <= len(observed),
        "sorted unique in-range normalization-first basis required",
    )
    _matrix_shape(decoder, 1, len(row_basis))
    supplied = [F(1), *map(_fraction, observed)]
    coefficients = [list(map(_fraction, row)) for row in decoder]
    return _detach(_mv(coefficients, [supplied[i] for i in row_basis]))


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
    _encode(list(result))
    return result


def _primitive(a, t):
    return (max(t - a[0], F(0)) ** 2 - max(t - a[1], F(0)) ** 2) / 2


def _axis_field(a, b, tile):
    lo, hi = tile
    base = _primitive(a, b[0])
    if hi <= b[0]:
        return F(0), F(0), F(0)
    if lo >= b[1]:
        return _primitive(a, b[1]) - base, F(0), F(0)
    _require(b[0] <= lo and hi <= b[1], "shared grid missed B saturation")
    if hi <= a[0]:
        return -base, F(0), F(0)
    if lo >= a[1]:
        return (a[0] ** 2 - a[1] ** 2) / 2 - base, a[1] - a[0], F(0)
    _require(a[0] <= lo and hi <= a[1], "shared grid missed A primitive branch")
    return a[0] ** 2 / 2 - base, -a[0], F(1, 2)


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


def _weighted(field, power, moments):
    k, l = power
    return sum(
        (x * moments[4 * (i + k) + j + l] for x, (i, j) in zip(field, QUADRATIC, strict=True)), F(0)
    )


def _cross(field, outgoing, moments):
    return sum(
        (
            a * b * moments[4 * (i + k) + j + l]
            for a, (i, j) in zip(field, QUADRATIC, strict=True)
            for b, (k, l) in zip(outgoing, LINEAR, strict=True)
            if a and b
        ),
        F(0),
    )


def _parse(problem):
    _native(problem)
    _fields(problem, ("family", "probe", "coarse", "fine"))
    _label(problem["family"])
    _fields(problem["probe"], ("name", "bounds"))
    probe = {
        "name": _label(problem["probe"]["name"]),
        "bounds": _rectangle(problem["probe"]["bounds"]),
    }
    sources = []
    for key in ("coarse", "fine"):
        level = problem[key]
        _fields(level, ("level", "cells"))
        _label(level["level"])
        _require(
            type(level["cells"]) is list and 1 <= len(level["cells"]) <= 8,
            "bounded positive cell inventory required",
        )
        cells = []
        for c in level["cells"]:
            _fields(c, ("event", "bounds"))
            _require(type(c["event"]) is int, "native level-local integer ID required")
            b = _rectangle(c["bounds"])
            cells.append({"event": c["event"], "bounds": b, "area": _area(b)})
        ids = [c["event"] for c in cells]
        _require(ids == sorted(set(ids)), "event-ordered unique cell IDs required")
        _require(
            all(_clip(a["bounds"], b["bounds"]) is None for a, b in combinations(cells, 2)),
            "same-level cell interiors overlap",
        )
        sources.append(cells)
    _require(
        problem["coarse"]["level"] != problem["fine"]["level"], "distinct level labels required"
    )
    coarse, fine = sources
    groups = {c["event"]: [] for c in coarse}
    inverse = {}
    for child in fine:
        parents = [p for p in coarse if _contains(p["bounds"], child["bounds"])]
        _require(len(parents) == 1, "fine cell requires exactly one full coarse parent")
        parent = parents[0]["event"]
        groups[parent].append(child["event"])
        inverse[child["event"]] = parent
    areas = {c["event"]: c["area"] for c in fine}
    for parent in coarse:
        _require(
            groups[parent["event"]]
            and sum((areas[e] for e in groups[parent["event"]]), F(0)) == parent["area"],
            "fine children must cover every full coarse parent",
        )
    for cells in sources:
        clips = [_clip(c["bounds"], probe["bounds"]) for c in cells]
        _require(
            sum((_area(b) for b in clips if b is not None), F(0)) == _area(probe["bounds"]),
            "clipped cells must cover the probe",
        )
    return probe, coarse, fine, groups, inverse


def _tiles(clips, cache):
    tiles = []
    for event, bounds in clips.items():
        if bounds is None:
            continue
        breaks = []
        for offset in (0, 2):
            lo, hi = bounds[offset : offset + 2]
            cuts = {lo, hi}
            for b in clips.values():
                if b is not None:
                    cuts.update(x for x in b[offset : offset + 2] if lo < x < hi)
            breaks.append(sorted(cuts))
        for us, vs in product(pairwise(breaks[0]), pairwise(breaks[1])):
            b = (*us, *vs)
            if b not in cache:
                cache[b] = _moments(b)
            tiles.append(
                {
                    "event": event,
                    "bounds": list(b),
                    "moments": list(cache[b]),
                    "outgoing": [
                        {"event": d, "coefficients": list(_outgoing(endpoint, b))}
                        for d, endpoint in clips.items()
                    ],
                }
            )
    return tiles


def _counts(
    coarse, fine, coarse_tiles, fine_tiles, generators, observations, targets, certificates
):
    nc, nf, ct, ft, n = len(coarse), len(fine), len(coarse_tiles), len(fine_tiles), len(generators)
    pc = sum(c["bounds"] is not None for c in coarse)
    pf = sum(c["bounds"] is not None for c in fine)
    basis_entries = pivot_entries = decoder_entries = collision_entries = recoverable = 0
    sizes_o = {o["name"]: len(o["matrix"]) for o in observations}
    sizes_q = {q["name"]: len(q["matrix"]) for q in targets}
    for row in certificates:
        certificate = row["certificate"]
        basis_entries += len(certificate["row_basis"])
        pivot_entries += len(certificate["pivot_columns"])
        if certificate["recoverable"]:
            recoverable += 1
            decoder_entries += len(certificate["decoder"]) * len(certificate["row_basis"])
        else:
            collision_entries += (
                3 * n + 2 * sizes_o[row["observation"]] + 3 * sizes_q[row["target"]]
            )
    return {
        "coarse_cells": nc,
        "fine_cells": nf,
        "positive_coarse_cells": pc,
        "positive_fine_cells": pf,
        "generators": n,
        "coarse_tiles": ct,
        "fine_tiles": ft,
        "input_bound_entries": 4 * (1 + nc + nf),
        "clipped_bound_entries": 4 * (pc + pf),
        "tile_bound_entries": 4 * (ct + ft),
        "coarse_moment_entries": 16 * ct,
        "fine_moment_entries": 16 * ft,
        "coarse_outgoing_vectors": ct * nc,
        "coarse_outgoing_entries": 4 * ct * nc,
        "fine_outgoing_vectors": ft * nf,
        "fine_outgoing_entries": 4 * ft * nf,
        "observation_rows": 5 * ct,
        "observation_entries": 5 * ct * n,
        "fine_weighted_rows": 4 * ft,
        "fine_weighted_entries": 4 * ft * n,
        "coarse_response_rows": nc**2,
        "fine_response_rows": nf**2,
        "field_rows": 9 * ft,
        "target_entries": (nc**2 + nf**2 + 9 * ft) * n,
        "geometric_decoder_entries": nc**2 * 4 * ct,
        "certificates": len(certificates),
        "recoverable": recoverable,
        "failed": len(certificates) - recoverable,
        "row_basis_entries": basis_entries,
        "pivot_column_entries": pivot_entries,
        "canonical_decoder_entries": decoder_entries,
        "collision_entries": collision_entries,
    }


def build_family(problem):
    """Build supplied-geometry maps and six exact finite-mixture certificates."""
    probe, coarse, fine, groups, inverse = _parse(problem)
    volume = _area(probe["bounds"])
    cc = {c["event"]: _clip(c["bounds"], probe["bounds"]) for c in coarse}
    fc = {c["event"]: _clip(c["bounds"], probe["bounds"]) for c in fine}
    moment_cache = {}
    coarse_tiles, fine_tiles = _tiles(cc, moment_cache), _tiles(fc, moment_cache)
    for tile in fine_tiles:
        parent = inverse[tile["event"]]
        matches = [
            i
            for i, coarse_tile in enumerate(coarse_tiles)
            if coarse_tile["event"] == parent and _contains(coarse_tile["bounds"], tile["bounds"])
        ]
        _require(len(matches) == 1, "fine tile must lie in one appropriate coarse tile")
        tile["coarse_tile"] = matches[0]
        for row in coarse_tiles[matches[0]]["outgoing"]:
            _require(
                list(_outgoing(cc[row["event"]], tile["bounds"])) == row["coefficients"],
                "coarse outgoing branch differs on a fine tile",
            )
    generator_pairs = list(product(fc, repeat=2))
    generators = [{"first": a, "second": b} for a, b in generator_pairs]
    n = len(generators)
    fields = [
        [_propagated(fc[a], fc[b], tile["bounds"]) for a, b in generator_pairs]
        for tile in fine_tiles
    ]
    fine_weighted = [
        [_weighted(field, power, fine_tiles[t]["moments"]) for field in row]
        for t, row in enumerate(fields)
        for power in LINEAR
    ]
    weighted = [[F(0)] * n for _ in range(4 * len(coarse_tiles))]
    for t, tile in enumerate(fine_tiles):
        for basis in range(4):
            destination = 4 * tile["coarse_tile"] + basis
            weighted[destination] = [
                a + b
                for a, b in zip(weighted[destination], fine_weighted[4 * t + basis], strict=True)
            ]
    integral = [list(weighted[4 * t]) for t in range(len(coarse_tiles))]
    observations = [
        {
            "name": "integral",
            "rows": [{"tile": t, "basis": 0} for t in range(len(coarse_tiles))],
            "matrix": integral,
        },
        {
            "name": "weighted",
            "rows": [{"tile": t, "basis": j} for t in range(len(coarse_tiles)) for j in range(4)],
            "matrix": weighted,
        },
    ]
    coarse_pairs, fine_pairs = list(product(cc, repeat=2)), list(product(fc, repeat=2))
    qcoarse, qfine = [], []
    for c, d in coarse_pairs:
        qcoarse.append(
            [
                sum(
                    (
                        _cross(fields[t][g], _outgoing(cc[d], tile["bounds"]), tile["moments"])
                        for t, tile in enumerate(fine_tiles)
                        if inverse[tile["event"]] == c
                    ),
                    F(0),
                )
                for g in range(n)
            ]
        )
    for c, d in fine_pairs:
        qfine.append(
            [
                sum(
                    (
                        _cross(fields[t][g], _outgoing(fc[d], tile["bounds"]), tile["moments"])
                        for t, tile in enumerate(fine_tiles)
                        if tile["event"] == c
                    ),
                    F(0),
                )
                for g in range(n)
            ]
        )
    synthesis = [
        [fields[t][g][i] for g in range(n)] for t in range(len(fine_tiles)) for i in range(9)
    ]
    targets = [
        {
            "name": "coarse",
            "rows": [{"first": c, "second": d} for c, d in coarse_pairs],
            "matrix": qcoarse,
        },
        {
            "name": "fine",
            "rows": [{"first": c, "second": d} for c, d in fine_pairs],
            "matrix": qfine,
        },
        {
            "name": "field",
            "rows": [
                {"tile": t, "power": list(p)} for t in range(len(fine_tiles)) for p in QUADRATIC
            ],
            "matrix": synthesis,
        },
    ]
    geometric_decoder = []
    for c, d in coarse_pairs:
        geometric_decoder.append(
            [
                coefficient if tile["event"] == c else F(0)
                for tile in coarse_tiles
                for coefficient in next(
                    row["coefficients"] for row in tile["outgoing"] if row["event"] == d
                )
            ]
        )
    _require(_mm(geometric_decoder, weighted) == qcoarse, "direct geometric decoder differs")
    fine_response = dict(zip(fine_pairs, qfine, strict=True))
    for (c, d), target in zip(coarse_pairs, qcoarse, strict=True):
        _require(
            [
                sum((fine_response[a, b][g] for a, b in product(groups[c], groups[d])), F(0))
                for g in range(n)
            ]
            == target,
            "complete child response sum differs",
        )
    for ct in range(len(coarse_tiles)):
        for basis in range(4):
            _require(
                [
                    sum(
                        (
                            fine_weighted[4 * t + basis][g]
                            for t, tile in enumerate(fine_tiles)
                            if tile["coarse_tile"] == ct
                        ),
                        F(0),
                    )
                    for g in range(n)
                ]
                == weighted[4 * ct + basis],
                "coarse field moments differ from fine sums",
            )
        _require(weighted[4 * ct] == integral[ct], "weighted observations do not contain integrals")
    _require(
        sum((sum(row, F(0)) for row in qcoarse), F(0))
        == sum((sum(row, F(0)) for row in qfine), F(0))
        == volume**4 / 576,
        "unweighted complete response partition differs",
    )
    cache = {}
    certificates = [
        {
            "observation": o["name"],
            "target": q["name"],
            "certificate": _certificate(o["matrix"], q["matrix"], cache),
        }
        for o in observations
        for q in targets
    ]
    flags = {(c["observation"], c["target"]): c["certificate"]["recoverable"] for c in certificates}
    _require(flags["weighted", "coarse"], "weighted coarse response must be recoverable")
    _require(
        all(
            not flags["integral", name] or flags["weighted", name]
            for name in ("coarse", "fine", "field")
        ),
        "adding weighted observations lost recoverability",
    )
    coarse_cells = [
        {
            "event": e,
            "bounds": list(b) if b is not None else None,
            "volume": _area(b) if b is not None else F(0),
        }
        for e, b in cc.items()
    ]
    fine_cells = [
        {
            "event": e,
            "bounds": list(b) if b is not None else None,
            "volume": _area(b) if b is not None else F(0),
        }
        for e, b in fc.items()
    ]
    return _detach(
        {
            "problem": problem,
            "geometry": {
                "volume": volume,
                "parents": [
                    {"parent": p, "children": list(children)} for p, children in groups.items()
                ],
                "coarse_cells": coarse_cells,
                "fine_cells": fine_cells,
                "coarse_tiles": coarse_tiles,
                "fine_tiles": fine_tiles,
            },
            "matrices": {
                "generators": generators,
                "observations": observations,
                "targets": targets,
                "fine_weighted": fine_weighted,
                "coarse_decoder": geometric_decoder,
            },
            "certificates": certificates,
            "checks": dict.fromkeys(
                (
                    "weighted_contains_integral",
                    "coarse_decoder_exact",
                    "coarse_refinement_exact",
                    "response_partition_exact",
                    "measurement_refinement_exact",
                ),
                True,
            ),
            "counts": _counts(
                coarse_cells,
                fine_cells,
                coarse_tiles,
                fine_tiles,
                generators,
                observations,
                targets,
                certificates,
            ),
        }
    )
