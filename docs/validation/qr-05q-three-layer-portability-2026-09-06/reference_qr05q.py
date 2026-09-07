"""Independent reachability/count-law/interpolation reference for QR-05Q.

All source generation is local. Full-source reachability precedes induced
restriction. Directed chain traversal and induced full-count-law moments
recover D/B; common-neighbor and central-edge recognizers recover M/T.
Cached exact rational interpolation supplies the fine probability kernels.
No other executor, prior artifact, source file, RET or core module is read
or imported at runtime. A failed H is retained without refinement or repair;
any conclusion concerns only the prespecified finite supplied-order family.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations, product

F = Fraction
_NODES = (F(0), F(1, 3), F(2, 3), F(1))
_POINTS = tuple(product(_NODES, repeat=2)) + (
    (F(1, 2), F(1, 2)),
    (F(2, 5), F(3, 7)),
    (F(1, 5), F(4, 5)),
    (F(1, 2), F(1, 3)),
    (F(0), F(2, 5)),
    (F(3, 7), F(1)),
)
_MAX_WORK = 512 * 1024 * 1024
_BASE_NAMES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed", "path6", "cycle4_edge")
_THREE_LAYER_EDGES = ((1, 3), (1, 4), (2, 3), (2, 4), (3, 5), (3, 6), (4, 5), (4, 6))


def _canonical(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def _digest(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _fields(value, names, message):
    _require(
        type(value) is dict and all(type(key) is str for key in value) and set(value) == set(names),
        message,
    )


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _bounded(value):
    _require(type(value) is F, "reference arithmetic must remain rational")
    _require(
        abs(value.numerator).bit_length() <= 4096 and value.denominator.bit_length() <= 4096,
        "reference rational exceeds the 4096-bit bound",
    )
    return value


def _native_json(value):
    if value is None or type(value) in (str, bool):
        return
    if type(value) is int:
        _require(abs(value).bit_length() <= 4096, "reference integer exceeds the component bound")
        return
    if type(value) is list:
        for child in value:
            _native_json(child)
        return
    if type(value) is dict:
        _require(
            all(type(key) is str for key in value), "reference JSON keys must be native strings"
        )
        for child in value.values():
            _native_json(child)
        return
    raise ValueError("reference result contains a non-native JSON value")


def _inverse_vandermonde():
    """Invert the four-node evaluation map by independent rational elimination."""
    augmented = [
        [node**power for power in range(4)] + [F(int(row == column)) for column in range(4)]
        for row, node in enumerate(_NODES)
    ]
    for column in range(4):
        pivot = next(row for row in range(column, 4) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [_bounded(value / scale) for value in augmented[column]]
        for row in range(4):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                _bounded(left - scale * right)
                for left, right in zip(augmented[row], augmented[column], strict=True)
            ]
    _require(
        all(
            augmented[row][column] == int(row == column) for row in range(4) for column in range(4)
        ),
        "reference Vandermonde elimination failed",
    )
    inverse = [row[4:] for row in augmented]
    _require(
        all(
            sum((inverse[power][index] * node**degree for index, node in enumerate(_NODES)), F(0))
            == int(power == degree)
            for power in range(4)
            for degree in range(4)
        ),
        "reference interpolation inverse failed its identity",
    )
    return inverse


def _tensor_interpolate(samples, inverse):
    """Apply inverse evaluation matrices in x and then y, returning exact ints."""
    x_coefficients = [
        [
            sum((inverse[power][index] * samples[index][y] for index in range(4)), F(0))
            for y in range(4)
        ]
        for power in range(4)
    ]
    table = [
        [
            sum(
                (inverse[y_power][index] * x_coefficients[x_power][index] for index in range(4)),
                F(0),
            )
            for y_power in range(4)
        ]
        for x_power in range(4)
    ]
    for row in table:
        for value in row:
            _bounded(value)
            _require(value.denominator == 1, "reference interpolation is not integral")
    return [[value.numerator for value in row] for row in table]


def _evaluate(table, x, y):
    return _bounded(
        sum(
            (F(table[a][b]) * x**a * y**b for a in range(4) for b in range(4)),
            F(0),
        )
    )


def _raw_summary(polynomials, means, counts, sizes):
    """Derive all raw count moments from full-law atoms, never chain pairs."""
    result = [
        [
            [
                [
                    sum(
                        atom["counts"][q] * atom["counts"][r] * atom["coefficients"][a][b]
                        for atom in polynomials
                    )
                    for b in range(4)
                ]
                for a in range(4)
            ]
            for r in range(4)
        ]
        for q in range(4)
    ]
    _require(result[0] == means, "reference raw-moment zero row does not recover D")
    for q in range(4):
        for r in range(4):
            _require(result[q][r] == result[r][q], "reference raw-moment symmetry failed")
            _require(
                sum(map(sum, result[q][r])) == counts[q] * counts[r],
                "reference raw-moment total failed",
            )
            _require(
                all(value >= 0 for row in result[q][r] for value in row),
                "reference raw-moment coefficient is negative",
            )
            _require(
                all(
                    result[q][r][a][b] == 0
                    for a in range(4)
                    for b in range(4)
                    if a > sizes[0] or b > sizes[1] or a + b > q + r
                ),
                "reference raw-moment degree failed",
            )
    return result


def _frame_key(frame):
    return [frame["density"], frame["fixed"], frame["eligible"]]


def _zero_table():
    return [[0] * 4 for _ in range(4)]


def _add_table(target, source, scale=1):
    for i in range(4):
        for j in range(4):
            target[i][j] += scale * source[i][j]


def _nonzero(table):
    return [
        (4 * i + j, value) for i, row in enumerate(table) for j, value in enumerate(row) if value
    ]


def _check_row(transitions, target_field):
    targets = [edge[target_field] for edge in transitions]
    _require(targets == sorted(set(targets)), "reference transition targets are not sorted unique")
    total = _zero_table()
    for edge in transitions:
        _require(
            bool(_nonzero(edge["coefficients"])),
            "reference structural transition has an identically zero polynomial",
        )
        _add_table(total, edge["coefficients"])
    _require(
        total == [[1, 0, 0, 0], [0] * 4, [0] * 4, [0] * 4],
        "reference transition row is not coefficientwise normalized",
    )


def _semigroup(quotient_rows):
    """Check all four-variable cells, with disjoint degree indices for the stages."""
    result = []
    total_pairs, total_paths, total_cells = 0, 0, 0
    sparse = [
        [(edge["target_class"], _nonzero(edge["coefficients"])) for edge in row["transitions"]]
        for row in quotient_rows
    ]
    for class_id, row in enumerate(quotient_rows):
        residuals, paths = {}, 0
        for intermediate, first in sparse[class_id]:
            for target, second in sparse[intermediate]:
                paths += 1
                if target not in residuals:
                    residuals[target] = [0] * 256
                for left_power, left_value in first:
                    for right_power, right_value in second:
                        residuals[target][16 * left_power + right_power] += left_value * right_value
        direct_targets = [edge["target_class"] for edge in row["transitions"]]
        _require(
            sorted(residuals) == direct_targets,
            "reference two-step and one-step structural target sets differ",
        )
        for target, polynomial in sparse[class_id]:
            for power, value in polynomial:
                residuals[target][16 * power + power] -= value
        maximum = max((abs(value) for table in residuals.values() for value in table), default=0)
        _require(maximum == 0, "reference four-variable quotient semigroup identity failed")
        pairs = len(residuals)
        cells = 256 * pairs
        result.append(
            {
                "class_id": class_id,
                "transition_pairs": pairs,
                "intermediate_paths": paths,
                "coefficient_cells": cells,
                "max_abs_residual": maximum,
            }
        )
        total_pairs += pairs
        total_paths += paths
        total_cells += cells
    return {
        "verified": True,
        "rows": result,
        "totals": {
            "transition_pairs": total_pairs,
            "intermediate_paths": total_paths,
            "coefficient_cells": total_cells,
            "max_abs_residual": 0,
        },
    }


def motif_supports(kept, past, eligible):
    """Return eligible color-layered K2,2 supports of a well-formed strict order.

    Local positions need not be topological or numerically sorted. Original-ID
    parity supplies the named colors; fixed and absent vertices are excluded.
    Both orientation cases are counted, with one occurrence per four-set.
    """
    ancestors = {
        vertex: {kept[index] for index in past[position]} for position, vertex in enumerate(kept)
    }
    observed = set(kept).intersection(eligible)
    odd = sorted(vertex for vertex in observed if vertex % 2)
    even = sorted(vertex for vertex in observed if vertex % 2 == 0)

    def incomparable(left, right):
        return left not in ancestors[right] and right not in ancestors[left]

    supports = []
    seen = set()
    for left, right in combinations(odd, 2):
        if not incomparable(left, right):
            continue
        common_successors = [
            vertex for vertex in even if left in ancestors[vertex] and right in ancestors[vertex]
        ]
        common_predecessors = [
            vertex for vertex in even if vertex in ancestors[left] and vertex in ancestors[right]
        ]
        for common in (common_successors, common_predecessors):
            for first, second in combinations(common, 2):
                if not incomparable(first, second):
                    continue
                support = tuple(sorted((left, right, first, second)))
                _require(
                    support not in seen,
                    "reference common-neighbor recognition counted a support twice",
                )
                seen.add(support)
                supports.append(list(support))
    return sorted(supports)


def _source_chains(past, eligible):
    """Traverse strict directed paths, independent of numeric original-ID order."""
    positions = {vertex: bit for bit, vertex in enumerate(eligible)}
    families = [[] for _ in range(4)]
    seen = [set() for _ in range(4)]

    def visit(current, interior):
        if current in past[7]:
            degree = len(interior)
            identity = frozenset(interior)
            _require(identity not in seen[degree], "reference source chain counted more than once")
            seen[degree].add(identity)
            support = sum(1 << positions[vertex] for vertex in interior if vertex in positions)
            families[degree].append(support)
        if len(interior) == 3:
            return
        for target in range(1, 7):
            if current in past[target]:
                _require(target not in interior, "reference source relation has a directed cycle")
                visit(target, (*interior, target))

    visit(0, ())
    _require(families[0] == [0], "reference fixed-probe zero-chain differs")
    return families


def _kernel_cache(inverse):
    """Interpolate each of the100 possible fixed-subset retention laws once."""
    kernels, grids = {}, {}
    for odd in range(4):
        for even in range(4):
            for kept_odd in range(odd + 1):
                for kept_even in range(even + 1):
                    key = (odd, even, kept_odd, kept_even)

                    def probability(x, y, population=key):
                        full_odd, full_even, retained_odd, retained_even = population
                        return _bounded(
                            x**retained_odd
                            * (1 - x) ** (full_odd - retained_odd)
                            * y**retained_even
                            * (1 - y) ** (full_even - retained_even)
                        )

                    samples = [[probability(x, y) for y in _NODES] for x in _NODES]
                    coefficients = _tensor_interpolate(samples, inverse)
                    _require(
                        all(
                            not coefficients[i][j] or (i <= odd and j <= even)
                            for i in range(4)
                            for j in range(4)
                        ),
                        "reference interpolated kernel violates its degree bound",
                    )
                    for i, x in enumerate(_NODES):
                        for j, y in enumerate(_NODES):
                            _require(
                                _evaluate(coefficients, x, y) == samples[i][j],
                                "reference kernel interpolation does not recover its grid",
                            )
                    for x, y in ((F(1, 2), F(1, 2)), (F(2, 5), F(3, 7))):
                        _require(
                            _evaluate(coefficients, x, y) == probability(x, y),
                            "reference kernel fails held-out probability evaluation",
                        )
                    kernels[key] = coefficients
                    grids[key] = tuple(value for row in samples for value in row)
    _require(len(kernels) == 100, "reference kernel cache inventory differs")
    return kernels, grids


def _count_law_features(states):
    """Take full count-law moments; no ordered chain pairs are enumerated."""
    for state in states:
        atoms = {}
        for edge in state["transitions"]:
            counts = tuple(states[edge["target_state"]]["chain_counts"])
            table = atoms.setdefault(counts, _zero_table())
            # Interpolation is linear: summing the cached interpolants gives the
            # exact interpolation of this full count atom's summed grid values.
            _add_table(table, edge["coefficients"])
        polynomials = [
            {"counts": list(counts), "coefficients": atoms[counts]} for counts in sorted(atoms)
        ]
        normalization = _zero_table()
        means = [[[0] * 4 for _ in range(4)] for _ in range(4)]
        for atom in polynomials:
            _require(
                bool(_nonzero(atom["coefficients"])), "reference count atom is identically zero"
            )
            _add_table(normalization, atom["coefficients"])
            for degree in range(4):
                _add_table(means[degree], atom["coefficients"], atom["counts"][degree])
        _require(
            normalization == [[1, 0, 0, 0], [0] * 4, [0] * 4, [0] * 4],
            "reference full count law is not coefficientwise normalized",
        )
        _require(
            means == state["mean_graded"], "reference count-law mean differs from source chains"
        )
        state["pair_graded"] = _raw_summary(
            polynomials, means, state["chain_counts"], state["color_sizes"]
        )


def path_supports(kept, past, eligible):
    """Find each color-layered induced P4 from its unique degree-two central edge.

    Numeric IDs and local positions are not causal orderings. All edges are
    comparisons in the supplied strict relation; outside vertices do not enter
    the four-set test. The unique absent cross pair must be incomparable.
    """
    ancestors = {
        vertex: {kept[index] for index in past[position]} for position, vertex in enumerate(kept)
    }
    present = set(kept).intersection(eligible)
    odds = sorted(vertex for vertex in present if vertex % 2)
    evens = sorted(vertex for vertex in present if vertex % 2 == 0)

    def incomparable(left, right):
        return left not in ancestors[right] and right not in ancestors[left]

    supports = []
    seen = set()
    for odd_center in odds:
        for even_center in evens:
            if odd_center in ancestors[even_center]:
                forward = True
            elif even_center in ancestors[odd_center]:
                forward = False
            else:
                continue
            odd_leaves = [
                vertex
                for vertex in odds
                if vertex != odd_center
                and incomparable(vertex, odd_center)
                and (
                    vertex in ancestors[even_center]
                    if forward
                    else even_center in ancestors[vertex]
                )
            ]
            even_leaves = [
                vertex
                for vertex in evens
                if vertex != even_center
                and incomparable(vertex, even_center)
                and (
                    odd_center in ancestors[vertex] if forward else vertex in ancestors[odd_center]
                )
            ]
            for odd_leaf in odd_leaves:
                for even_leaf in even_leaves:
                    if not incomparable(odd_leaf, even_leaf):
                        continue
                    support = tuple(sorted((odd_center, even_center, odd_leaf, even_leaf)))
                    _require(
                        support not in seen,
                        "reference central-edge recognition counted a P4 support twice",
                    )
                    seen.add(support)
                    supports.append(list(support))
    return sorted(supports)


def _observation_key(fid, kept, past):
    return fid, tuple(kept), tuple(tuple(row) for row in past)


def _induced(state, kept):
    present = set(kept)
    positions = {v: i for i, v in enumerate(kept)}
    return [
        sorted(positions[state["kept"][i]] for i in before if state["kept"][i] in present)
        for vertex, before in zip(state["kept"], state["past"], strict=True)
        if vertex in present
    ]


def _features_and_fine(model):
    states = []
    for raw in model["states"]:
        frame = model["frames"][raw["frame_id"]]
        eligible = frame["eligible"]
        full_past = [set() for _ in range(8)]
        for vertex, before in zip(raw["kept"], raw["past"], strict=True):
            full_past[vertex] = {raw["kept"][i] for i in before}
        families = _source_chains(full_past, eligible)
        odd_bits = sum(1 << i for i, v in enumerate(eligible) if v % 2)
        d = [[[0] * 4 for _ in range(4)] for _ in range(4)]
        for q, supports in enumerate(families):
            for support in supports:
                d[q][(support & odd_bits).bit_count()][(support & ~odd_bits).bit_count()] += 1
        motifs = motif_supports(raw["kept"], raw["past"], eligible)
        paths = path_supports(raw["kept"], raw["past"], eligible)
        sizes = [
            sum(v % 2 for v in raw["kept"] if v in eligible),
            sum(not v % 2 for v in raw["kept"] if v in eligible),
        ]
        _require(
            len(motifs) + len(paths) <= 9
            and not (set(map(tuple, motifs)) & set(map(tuple, paths))),
            "motif support bound/disjointness",
        )
        states.append(
            {
                **raw,
                "color_sizes": sizes,
                "chain_counts": list(map(len, families)),
                "mean_graded": d,
                "motif_supports": motifs,
                "motif_count": len(motifs),
                "path_supports": paths,
                "path_count": len(paths),
            }
        )
    lookup = {_observation_key(s["frame_id"], s["kept"], s["past"]): s["state_id"] for s in states}
    kernels, grids = _kernel_cache(_inverse_vandermonde())
    rate_values = {}
    for key, table in kernels.items():
        O, E, o, e = key
        values = tuple(
            _bounded(x**o * (1 - x) ** (O - o) * y**e * (1 - y) ** (E - e)) for x, y in _POINTS
        )
        _require(
            all(
                _evaluate(table, x, y) == value
                for (x, y), value in zip(_POINTS, values, strict=True)
            ),
            "interpolated fine law differs at audit rates",
        )
        rate_values[key] = values
    fine, grid_rows, atoms = [], [], 0
    for state in states:
        frame = model["frames"][state["frame_id"]]
        present = [v for v in state["kept"] if v in frame["eligible"]]
        row, samples = [], []
        totals = [F(0)] * len(_POINTS)
        for mask in range(1 << len(present)):
            kept = sorted(frame["fixed"] + [v for i, v in enumerate(present) if mask & (1 << i)])
            key = _observation_key(state["frame_id"], kept, _induced(state, kept))
            _require(key in lookup, "missing induced successor")
            target = lookup[key]
            child = states[target]
            kernel_key = (*state["color_sizes"], *child["color_sizes"])
            row.append({"target_state": target, "coefficients": kernels[kernel_key]})
            samples.append((target, grids[kernel_key]))
            for n, value in enumerate(rate_values[kernel_key]):
                _require(value >= 0, "negative direct retention probability")
                totals[n] += value
                if n in (0, 3, 12, 15) and value:
                    x, y = _POINTS[n]
                    expected = sorted(
                        v for v in state["kept"] if v in frame["fixed"] or (x if v % 2 else y) == 1
                    )
                    _require(kept == expected, "deterministic fine corner")
        row.sort(key=lambda edge: edge["target_state"])
        samples.sort(key=lambda edge: edge[0])
        _check_row(row, "target_state")
        _require(all(total == 1 for total in totals), "fine probability normalization")
        state["transitions"] = row
        fine.append({"state_id": state["state_id"], "transitions": row})
        grid_rows.append(samples)
        atoms += len(row)
        _require(atoms <= 472428, "fine atom bound")
    _count_law_features(states)
    names = (
        "state_id",
        "color_sizes",
        "chain_counts",
        "mean_graded",
        "pair_graded",
        "motif_supports",
        "motif_count",
        "path_supports",
        "path_count",
    )
    features = [{name: state[name] for name in names} for state in states]
    audit = {
        "sha256": _digest(fine),
        "transition_atoms": atoms,
        "coefficient_cells": 16 * atoms,
        "normalization_rows": len(states),
        "deterministic_corner_rows": 4 * len(states),
        "rate_points": len(_POINTS),
        "evaluated_atoms": len(_POINTS) * atoms,
    }
    return features, fine, grid_rows, audit


def _push(fine, vector):
    rows = []
    for row in fine:
        tables = {}
        for edge in row["transitions"]:
            _add_table(
                tables.setdefault(vector[edge["target_state"]], _zero_table()), edge["coefficients"]
            )
        transitions = [
            {"target_class": cid, "coefficients": table} for cid, table in sorted(tables.items())
        ]
        _check_row(transitions, "target_class")
        rows.append({"state_id": row["state_id"], "transitions": transitions})
    return rows


def _parse(problem):
    _native_json(problem)
    _fields(problem, ("schema_version", "family"), "invalid Q problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05q-problem-v1",
        "invalid Q problem schema",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05q_three_layer",
        "invalid Q family",
    )


def _source(index):
    """Generate arrows, then independently traverse all reachable descendants."""
    _require(type(index) is int and 0 <= index < 1542, "invalid source index")
    adjacency = [set() for _ in range(8)]
    adjacency[0].update(range(1, 8))
    for v in range(1, 7):
        adjacency[v].add(7)
    if index >= 1030:
        reverse = index >= 1286
        incidence = index - (1286 if reverse else 1030)
        for bit, (left, right) in enumerate(_THREE_LAYER_EDGES):
            if incidence & (1 << bit):
                if reverse:
                    left, right = right, left
                adjacency[left].add(right)
        name = f"three_layer_{'reverse' if reverse else 'forward'}_{incidence:03d}"
    elif index >= 6:
        reverse = index >= 518
        incidence = index - (518 if reverse else 6)
        for i in range(3):
            for j in range(3):
                if incidence & (1 << (3 * i + j)):
                    left, right = 2 * i + 1, 2 * j + 2
                    if reverse:
                        left, right = right, left
                    adjacency[left].add(right)
        name = f"layered_{'eo' if reverse else 'oe'}_{incidence:03d}"
    else:
        name = _BASE_NAMES[index]
        if index == 2:
            for left in range(1, 7):
                adjacency[left].update(range(left + 1, 7))
        elif index in (4, 5):
            for left, right in (
                ((1, 2), (1, 4), (3, 4), (3, 6), (5, 6))
                if index == 4
                else ((1, 4), (1, 6), (3, 4), (3, 6), (2, 5))
            ):
                adjacency[left].add(right)
        else:
            for i in range(3):
                for j in range(3):
                    if i != j if index == 1 else i <= j:
                        adjacency[i + 1].add(j + 4)
    descendants = []
    for origin in range(8):
        reached, pending = set(), list(adjacency[origin])
        while pending:
            target = pending.pop()
            _require(target != origin, "generated source contains a directed cycle")
            if target in reached:
                continue
            reached.add(target)
            pending.extend(adjacency[target])
        descendants.append(reached)
    past = [[u for u in range(8) if v in descendants[u]] for v in range(8)]
    _require(
        all(set(past[u]) <= set(past[v]) for v in range(8) for u in past[v]),
        "source reachability is not transitive",
    )
    _require(
        all(0 in past[v] for v in range(1, 8)) and past[7] == list(range(7)),
        "fixed probes changed under reversal",
    )
    return name, past


def _domain():
    frames = [
        {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
        {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
    ]
    registry, profiles, states = {}, [], []
    aliases = 0
    for pid in range(1542):
        if pid == 1030:
            _require(len(states) == 2470 and aliases == 65888, "old family inventory changed")
        name, past = _source(pid)
        fid = int(pid == 3)
        frame = frames[fid]
        full = {"kept": list(range(8)), "past": past}
        ids = []
        for mask in range(1 << len(frame["eligible"])):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(frame["eligible"]) if mask & (1 << bit)]
            )
            restricted = _induced(full, kept)
            key = _observation_key(fid, kept, restricted)
            if key not in registry:
                registry[key] = len(states)
                states.append(
                    {"state_id": len(states), "frame_id": fid, "kept": kept, "past": restricted}
                )
            ids.append(registry[key])
            aliases += 1
        profiles.append(
            {"profile_index": pid, "name": name, "frame_id": fid, "past": past, "state_ids": ids}
        )
    _require(len(profiles) == 1542 and aliases == 98656, "expanded source/alias inventory")
    _require(len(states) <= 35238, "raw observation cap")
    return {"frames": frames, "profiles": profiles, "states": states}


def _partition(domain, features):
    vector, classes, registry = [], [], {}
    for state, feature in zip(domain["states"], features, strict=True):
        key = [
            _frame_key(domain["frames"][state["frame_id"]]),
            feature["pair_graded"],
            feature["motif_count"],
            feature["path_count"],
        ]
        encoded = _canonical(key)
        if encoded not in registry:
            registry[encoded] = len(classes)
            classes.append({"class_id": len(classes), "key": key, "members": []})
        cid = registry[encoded]
        vector.append(cid)
        classes[cid]["members"].append(state["state_id"])
    return {"state_classes": vector, "classes": classes}


def _closure(partition, pushed):
    """Check every member, preserving only the canonical first obstruction."""
    maps = [{a["target_class"]: a["coefficients"] for a in row["transitions"]} for row in pushed]
    comparisons = 0
    witness = None
    for group in partition["classes"]:
        left = group["members"][0]
        for right in group["members"][1:]:
            comparisons += 1
            unequal = [
                target
                for target in sorted(maps[left].keys() | maps[right].keys())
                if maps[left].get(target, _zero_table()) != maps[right].get(target, _zero_table())
            ]
            if unequal and witness is None:
                target = unequal[0]
                lhs = maps[left].get(target, _zero_table())
                rhs = maps[right].get(target, _zero_table())
                rates = next(
                    (
                        [str(x), str(y)]
                        for x, y in _POINTS[:16]
                        if _evaluate(lhs, x, y) != _evaluate(rhs, x, y)
                    ),
                    None,
                )
                _require(rates is not None, "unequal bounded polynomials coincide on full grid")
                witness = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": target,
                    "left_coefficients": lhs,
                    "right_coefficients": rhs,
                    "first_distinguishing_rates": rates,
                }
    classes = len(partition["classes"])
    _require(comparisons == len(pushed) - classes, "closure member comparison inventory")
    quotient = []
    semigroup = None
    if witness is None:
        quotient = [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                "transitions": pushed[group["members"][0]]["transitions"],
            }
            for group in partition["classes"]
        ]
        semigroup = _semigroup(quotient)
    return (
        {
            "closed": witness is None,
            "classes_checked": classes,
            "member_comparisons": comparisons,
            "witness": witness,
        },
        quotient,
        semigroup,
    )


def _expected_updates(features, fine, direct_grids):
    # Reconstruct support expectation from direct product probabilities, and
    # tensor-interpolate independently of summing already-produced coefficients.
    inverse = _inverse_vandermonde()
    cache = {}
    maximum = 0
    for feature, row in zip(features, direct_grids, strict=True):
        for field in ("motif_count", "path_count"):
            samples = [F(0)] * 16
            for target, probabilities in row:
                value = features[target][field]
                if value:
                    for node, probability in enumerate(probabilities):
                        samples[node] += value * probability
            key = tuple(samples)
            if key not in cache:
                cache[key] = _tensor_interpolate(
                    [samples[i : i + 4] for i in range(0, 16, 4)], inverse
                )
            expected = _zero_table()
            expected[2][2] = feature[field]
            maximum = max(
                maximum,
                max(abs(cache[key][i][j] - expected[i][j]) for i in range(4) for j in range(4)),
            )
    _require(maximum == 0, "M/T conditional expectation failed")
    _require(len(fine) == len(features), "expectation state inventory")
    return {
        "motif_cells": 16 * len(features),
        "path_cells": 16 * len(features),
        "max_abs_residual": maximum,
    }


def analyze(problem):
    """Return complete unchanged-H evidence; retain failure without repair."""
    _parse(problem)
    domain = _domain()
    features, fine, direct_grids, metadata = _features_and_fine(domain)
    partition = _partition(domain, features)
    pushed = _push(fine, partition["state_classes"])
    closure, quotient, semigroup = _closure(partition, pushed)
    expected = _expected_updates(features, fine, direct_grids)
    result = {
        "domain": domain,
        "features": features,
        "partition": partition,
        "fine_kernel": metadata,
        "pushed_rows": pushed,
        "closure": closure,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "expected_updates": expected,
        "counts": {
            "profiles": len(domain["profiles"]),
            "aliases": sum(len(p["state_ids"]) for p in domain["profiles"]),
            "states": len(features),
            "classes": len(partition["classes"]),
            "fine_atoms": metadata["transition_atoms"],
            "pushed_atoms": sum(len(row["transitions"]) for row in pushed),
        },
    }
    _native_json(result)
    _require(len(_canonical(result)) <= _MAX_WORK, "analysis working byte cap")
    return result
