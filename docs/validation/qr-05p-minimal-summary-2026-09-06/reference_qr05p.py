"""Independent exact-grid reference for QR-05P.

The explicit raw observation table is the only model input. Locally carried
O-reference utilities implement directed chains, full-count-law moments,
common-neighbor/central-edge motifs and rational kernel interpolation.
Refinement signatures in analyze use direct product-probability grids.
No artifact, other executor, or source file is read or imported at runtime.
The certificate concerns the supplied finite domain and declared thinning law,
not unrestricted minimality, physical dynamics, or application performance.
"""

from __future__ import annotations

import hashlib
import json
import re
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
_QUESTIONS = (
    "chain_counts",
    "motif_count",
    "path_count",
    "counts_motif_path",
    "named_relation_1_7",
)
_MAX_WORK = 512 * 1024 * 1024
_PAYLOAD_CACHE = {}


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


def _parse(problem):
    _native_json(problem)
    _fields(problem, ("schema_version", "family", "model"), "invalid P problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05p-problem-v1",
        "invalid P schema",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05p_summary_contract",
        "invalid P family",
    )
    model = problem["model"]
    _fields(model, ("frames", "states"), "invalid model fields")
    frames = [
        {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
        {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
    ]
    _require(_canonical(model["frames"]) == _canonical(frames), "invalid fixed frames")
    states = model["states"]
    _require(type(states) is list and 2 <= len(states) <= 2470, "state count bound")
    seen, represented = set(), set()
    for sid, state in enumerate(states):
        _fields(state, ("state_id", "frame_id", "kept", "past"), "invalid raw state fields")
        _require(
            type(state["state_id"]) is int and state["state_id"] == sid, "noncanonical state ID"
        )
        fid = state["frame_id"]
        _require(type(fid) is int and 0 <= fid < 2, "invalid native frame ID")
        represented.add(fid)
        kept, past = state["kept"], state["past"]
        _require(
            type(kept) is list
            and all(type(v) is int and 0 <= v < 8 for v in kept)
            and kept == sorted(set(kept)),
            "invalid native kept vertices",
        )
        frame = frames[fid]
        _require(
            set(frame["fixed"]) <= set(kept) <= set(frame["fixed"] + frame["eligible"]),
            "invalid observation marks",
        )
        _require(type(past) is list and len(past) == len(kept), "invalid past outer shape")
        for j, before in enumerate(past):
            _require(
                type(before) is list
                and all(type(i) is int and 0 <= i < len(kept) for i in before)
                and before == sorted(set(before))
                and j not in before,
                "invalid native strict predecessor indices",
            )
        ancestor = [set(row) for row in past]
        _require(
            all(ancestor[i] <= ancestor[j] for j in range(len(kept)) for i in ancestor[j]),
            "relation is not transitive",
        )
        bottom, top = kept.index(0), kept.index(7)
        _require(
            all(bottom in ancestor[j] for j in range(len(kept)) if j != bottom)
            and ancestor[top] == set(range(len(kept))) - {top},
            "fixed endpoints do not bound the observation",
        )
        key = _observation_key(fid, kept, past)
        _require(key not in seen, "duplicate raw observation")
        seen.add(key)
    _require(represented == {0, 1}, "both frames must be represented")
    _require(len(_canonical(problem)) <= _MAX_WORK, "input working byte cap")
    return model


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
        _require(atoms <= 99180, "fine atom bound")
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


def _partitions(model, features):
    result = {}
    for name in ("C", "H"):
        registry, vector, classes = {}, [], []
        for raw, feature in zip(model["states"], features, strict=True):
            key = [
                _frame_key(model["frames"][raw["frame_id"]]),
                feature["pair_graded"],
                feature["motif_count"],
            ]
            if name == "H":
                key.append(feature["path_count"])
            encoded = _canonical(key)
            if encoded not in registry:
                registry[encoded] = len(classes)
                classes.append({"class_id": len(classes), "key": key, "members": []})
            cid = registry[encoded]
            vector.append(cid)
            classes[cid]["members"].append(raw["state_id"])
        result[name] = {"state_classes": vector, "classes": classes}
    return result


def _groups(vector):
    groups = []
    for sid, cid in enumerate(vector):
        _require(type(cid) is int and 0 <= cid <= len(groups), "noncanonical class vector")
        if cid == len(groups):
            groups.append({"class_id": cid, "members": []})
        groups[cid]["members"].append(sid)
    return groups


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


def _refine_grid(fine, initial, direct_grids):
    vector = list(initial)
    initial_count = len(_groups(vector))
    rounds = []
    while True:
        groups = _groups(vector)
        pushed = _push(fine, vector)
        grid_signatures = []
        for sid, row in enumerate(direct_grids):
            masses = {}
            for target, samples in row:
                values = masses.setdefault(vector[target], [F(0)] * 16)
                for node, value in enumerate(samples):
                    values[node] += value
            # Every structural probability is positive at an interior grid node,
            # so sparse target keys are safe for these stochastic polynomial laws.
            signature = (
                vector[sid],
                tuple(
                    (cid, tuple(values)) for cid, values in sorted(masses.items()) if any(values)
                ),
            )
            grid_signatures.append(signature)
        registry, following = {}, []
        for signature in grid_signatures:
            if signature not in registry:
                registry[signature] = len(registry)
            following.append(registry[signature])
        children = _groups(following)
        _require(
            all(len({vector[sid] for sid in g["members"]}) == 1 for g in children),
            "refinement merged old classes",
        )
        separations = []
        by_old = {}
        maps = [
            {a["target_class"]: a["coefficients"] for a in row["transitions"]} for row in pushed
        ]
        for child in children:
            right = child["members"][0]
            parent = vector[right]
            if parent not in by_old:
                by_old[parent] = child["class_id"]
                continue
            left = groups[parent]["members"][0]
            target = next(
                (
                    t
                    for t in sorted(maps[left].keys() | maps[right].keys())
                    if maps[left].get(t, _zero_table()) != maps[right].get(t, _zero_table())
                ),
                None,
            )
            _require(target is not None, "grid split has no polynomial distinction")
            lhs, rhs = maps[left].get(target, _zero_table()), maps[right].get(target, _zero_table())
            rates = next(
                (
                    [str(x), str(y)]
                    for x, y in _POINTS[:16]
                    if _evaluate(lhs, x, y) != _evaluate(rhs, x, y)
                ),
                None,
            )
            _require(rates is not None, "polynomial distinction absent on unisolvent grid")
            separations.append(
                {
                    "parent_class_id": parent,
                    "child_class_id": child["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": target,
                    "left_coefficients": lhs,
                    "right_coefficients": rhs,
                    "first_distinguishing_rates": rates,
                }
            )
        stable = following == vector
        if not stable:
            _require(len(children) > len(groups), "non-strict alleged refinement")
        rounds.append(
            {
                "round_index": len(rounds),
                "state_classes": vector,
                "classes": groups,
                "pushed_rows_sha256": _digest(pushed),
                "pushed_atoms": sum(len(row["transitions"]) for row in pushed),
                "stable": stable,
                "separations": separations,
            }
        )
        _require(len(rounds) <= len(vector) - initial_count + 1, "finite refinement round bound")
        _require(len(_canonical(rounds)) <= _MAX_WORK, "refinement working byte cap")
        if stable:
            return rounds
        vector = following


def _validate_fine(fine_rows, initial):
    _native_json(fine_rows)
    _native_json(initial)
    _require(
        type(fine_rows) is list
        and type(initial) is list
        and 1 <= len(initial) == len(fine_rows) <= 2470,
        "finite helper domain",
    )
    _groups(initial)
    grids = []
    for sid, row in enumerate(fine_rows):
        _fields(row, ("state_id", "transitions"), "fine helper row fields")
        _require(type(row["state_id"]) is int and row["state_id"] == sid, "fine helper source")
        _require(type(row["transitions"]) is list and row["transitions"], "fine helper transitions")
        sample_row = []
        for edge in row["transitions"]:
            _fields(edge, ("target_state", "coefficients"), "fine helper atom")
            _require(
                type(edge["target_state"]) is int and 0 <= edge["target_state"] < len(initial),
                "fine helper target",
            )
            _table(edge["coefficients"])
            samples = tuple(_evaluate(edge["coefficients"], x, y) for x, y in _POINTS[:16])
            _require(all(value >= 0 for value in samples), "fine helper negative grid probability")
            sample_row.append((edge["target_state"], samples))
        _check_row(row["transitions"], "target_state")
        grids.append(sample_row)
    return grids


def refine(fine_rows, initial):
    """Synchronous exact-grid rounds for a bounded supplied polynomial helper.

    Unlike analyze's source-product grid, synthetic helpers supply coefficients;
    evaluating those at the unisolvent grid is the declared helper-only route.
    """
    return _refine_grid(fine_rows, initial, _validate_fine(fine_rows, initial))


def _class_map(finer, coarser):
    values = [set() for _ in _groups(finer)]
    for first, second in zip(finer, coarser, strict=True):
        values[first].add(second)
    return (
        [next(iter(value)) for value in values]
        if all(len(value) == 1 for value in values)
        else None
    )


def _terminal(fine, partitions, rounds):
    vector = rounds[-1]["state_classes"]
    classes = _groups(vector)
    rows = _push(fine, vector)
    quotient = []
    for group in classes:
        rep = group["members"][0]
        _require(
            all(rows[sid]["transitions"] == rows[rep]["transitions"] for sid in group["members"]),
            "terminal fiber is not closed",
        )
        quotient.append(
            {
                "class_id": group["class_id"],
                "representative_state": rep,
                "transitions": rows[rep]["transitions"],
            }
        )
    sg = _semigroup(quotient)
    vectors = [partitions["C"]["state_classes"], vector, partitions["H"]["state_classes"]]
    comparison = {
        "names": ["C", "R", "H"],
        "refinement": [[_class_map(a, b) is not None for b in vectors] for a in vectors],
        "same_memberships_as_H": vector == vectors[2],
        "R_to_C": _class_map(vector, vectors[0]),
        "R_to_H": _class_map(vector, vectors[2]),
        "H_to_R": _class_map(vectors[2], vector),
    }
    # O's H closure is verified from this input, not presumed for an alternate table.
    h_rows = _push(fine, vectors[2])
    h_closed = all(
        all(
            h_rows[sid]["transitions"] == h_rows[group["members"][0]]["transitions"]
            for sid in group["members"]
        )
        for group in partitions["H"]["classes"]
    )
    if h_closed:
        _require(comparison["H_to_R"] is not None, "closed H violates refinement induction")
    strict = len(rounds) - 1
    counts = {
        "rounds": len(rounds),
        "strict_rounds": strict,
        "classes": len(classes),
        "round_transition_atoms": sum(r["pushed_atoms"] for r in rounds),
        "round_coefficient_cells": 16 * sum(r["pushed_atoms"] for r in rounds),
        "separation_witnesses": sum(len(r["separations"]) for r in rounds),
        "quotient_transition_atoms": sum(len(row["transitions"]) for row in quotient),
        "semigroup_intermediate_paths": sg["totals"]["intermediate_paths"],
        "semigroup_coefficient_cells": sg["totals"]["coefficient_cells"],
    }
    return {
        "initial_partition": "C",
        "rounds": rounds,
        "strict_rounds": strict,
        "final_round": len(rounds) - 1,
        "state_classes": vector,
        "classes": classes,
        "quotient_rows": quotient,
        "semigroup": sg,
        "comparison": comparison,
        "counts": counts,
    }


def _table(table):
    _require(
        type(table) is list
        and len(table) == 4
        and all(
            type(row) is list
            and len(row) == 4
            and all(type(c) is int and abs(c).bit_length() <= 4096 for c in row)
            for row in table
        ),
        "invalid native 4x4 polynomial table",
    )


def _observable_value(name, value):
    if name in ("chain_counts", "counts_motif_path"):
        length = 4 if name == "chain_counts" else 6
        _require(
            type(value) is list
            and len(value) == length
            and all(type(v) is int and v >= 0 for v in value),
            "invalid vector observable",
        )
        _require(
            value[0] == 1 and value[1] <= 6 and value[2] <= 15 and value[3] <= 20,
            "invalid endpoint chain-count value",
        )
        if length == 6:
            _require(value[4] <= 9 and value[5] <= 9, "invalid joint motif counts")
    else:
        upper = 1 if name == "named_relation_1_7" else 9
        _require(type(value) is int and 0 <= value <= upper, "invalid scalar observable")


def _validate_consumer(consumer):
    """Validate a native payload before content-sensitive reuse; no identity cache."""
    _native_json(consumer)
    _fields(
        consumer,
        (
            "schema_version",
            "model_sha256",
            "state_classes_sha256",
            "class_count",
            "quotient_rows",
            "observables",
        ),
        "consumer fields",
    )
    _require(consumer["schema_version"] == "det8-qr05p-consumer-v1", "consumer schema")
    for field in ("model_sha256", "state_classes_sha256"):
        _require(
            type(consumer[field]) is str
            and re.fullmatch(r"[0-9a-f]{64}", consumer[field]) is not None,
            "invalid consumer digest",
        )
    encoded = _canonical(consumer)
    _require(len(encoded) <= _MAX_WORK, "consumer working byte cap")
    if encoded in _PAYLOAD_CACHE:
        return _PAYLOAD_CACHE[encoded]
    # Own the validated snapshot: later caller mutation cannot change this cache entry.
    payload = json.loads(encoded)
    count = payload["class_count"]
    _require(type(count) is int and 1 <= count <= 2470, "invalid native class count")
    rows = payload["quotient_rows"]
    _require(type(rows) is list and len(rows) == count, "consumer quotient row count")
    representatives = []
    atom_count = 0
    for cid, row in enumerate(rows):
        _fields(row, ("class_id", "representative_state", "transitions"), "consumer row fields")
        _require(
            type(row["class_id"]) is int and row["class_id"] == cid, "consumer class numbering"
        )
        rep = row["representative_state"]
        _require(type(rep) is int and 0 <= rep < 2470, "consumer representative state")
        representatives.append(rep)
        _require(
            type(row["transitions"]) is list and row["transitions"],
            "consumer transitions must be nonempty",
        )
        for edge in row["transitions"]:
            _fields(edge, ("target_class", "coefficients"), "consumer transition fields")
            _require(
                type(edge["target_class"]) is int and 0 <= edge["target_class"] < count,
                "consumer target class",
            )
            _table(edge["coefficients"])
        _check_row(row["transitions"], "target_class")
        atom_count += len(row["transitions"])
        _require(atom_count <= 99180, "consumer transition atom bound")
    _require(
        representatives == sorted(set(representatives)) and representatives[0] == 0,
        "consumer representatives are not canonical",
    )
    observables = payload["observables"]
    _require(
        type(observables) is list and len(observables) == len(_QUESTIONS),
        "consumer observable count",
    )
    for expected, observable in zip(_QUESTIONS, observables, strict=True):
        _fields(
            observable,
            ("name", "measurable", "class_values", "first_failure"),
            "consumer observable fields",
        )
        _require(
            type(observable["name"]) is str
            and observable["name"] == expected
            and type(observable["measurable"]) is bool,
            "consumer observable identity",
        )
        if observable["measurable"]:
            values = observable["class_values"]
            _require(
                type(values) is list
                and len(values) == count
                and observable["first_failure"] is None,
                "consumer measurable question shape",
            )
            for value in values:
                _observable_value(expected, value)
        else:
            _require(observable["class_values"] is None, "nonmeasurable class values")
            failure = observable["first_failure"]
            _fields(
                failure,
                ("class_id", "left_state", "right_state", "left_value", "right_value"),
                "consumer nonmeasurability witness",
            )
            _require(
                type(failure["class_id"]) is int
                and 0 <= failure["class_id"] < count
                and type(failure["left_state"]) is int
                and type(failure["right_state"]) is int
                and 0 <= failure["left_state"] < failure["right_state"] < 2470,
                "consumer nonmeasurability IDs",
            )
            for field in ("left_value", "right_value"):
                _observable_value(expected, failure[field])
            _require(
                _canonical(failure["left_value"]) != _canonical(failure["right_value"]),
                "nonmeasurability witness values are equal",
            )
    prepared = {
        "payload": payload,
        "observables": {o["name"]: o for o in observables},
        "evaluations": {},
    }
    if len(_PAYLOAD_CACHE) >= 2:
        _PAYLOAD_CACHE.clear()
    _PAYLOAD_CACHE[encoded] = prepared
    return prepared


def _rates(rates):
    _require(type(rates) is list and len(rates) == 2, "rates must be a native pair list")
    values = []
    for value in rates:
        _require(
            type(value) is str
            and len(value) <= 3000
            and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is not None,
            "invalid canonical rational rate",
        )
        rational = _bounded(F(value))
        _require(
            str(rational) == value and 0 <= rational <= 1, "rate outside canonical unit interval"
        )
        values.append(rational)
    return values


def _predict_core(prepared, question, class_id, rates, values):
    observable = prepared["observables"][question]
    _require(observable["measurable"], "question is not measurable from this summary")
    row = prepared["payload"]["quotient_rows"][class_id]["transitions"]
    key = (class_id, *rates)
    cache = prepared["evaluations"]
    if key not in cache:
        evaluated = [_evaluate(atom["coefficients"], *values) for atom in row]
        _require(
            all(value >= 0 for value in evaluated) and sum(evaluated) == 1,
            "requested row has invalid selected-rate probabilities",
        )
        if len(cache) >= 4096:
            cache.clear()
        cache[key] = evaluated
    probabilities = cache[key]
    grouped = {}
    for atom, probability in zip(row, probabilities, strict=True):
        value = observable["class_values"][atom["target_class"]]
        encoded = _canonical(value)
        if encoded not in grouped:
            grouped[encoded] = [value, F(0)]
        grouped[encoded][1] += probability
    return {
        "question": question,
        "class_id": class_id,
        "rates": list(rates),
        "outcomes": [
            {
                "value": list(value) if type(value) is list else value,
                "probability": str(_bounded(probability)),
            }
            for _, (value, probability) in sorted(grouped.items())
        ],
    }


def predict(consumer, question, class_id, rates):
    """Predict a measurable observable using only a verified consumer payload.

    Structural validation is not artifact authentication or domain membership.
    The caller must bind this payload and initial class to verified evidence.
    """
    prepared = _validate_consumer(consumer)
    _require(type(question) is str and question in _QUESTIONS, "unknown native question")
    _require(
        type(class_id) is int and 0 <= class_id < prepared["payload"]["class_count"],
        "invalid native requested class",
    )
    values = _rates(rates)
    return _predict_core(prepared, question, class_id, rates, values)


def _question_values(model, features):
    values = {name: [] for name in _QUESTIONS}
    for raw, feature in zip(model["states"], features, strict=True):
        values["chain_counts"].append(feature["chain_counts"])
        values["motif_count"].append(feature["motif_count"])
        values["path_count"].append(feature["path_count"])
        values["counts_motif_path"].append(
            feature["chain_counts"] + [feature["motif_count"], feature["path_count"]]
        )
        kept = raw["kept"]
        named = int(1 in kept and kept.index(1) in raw["past"][kept.index(7)])
        values["named_relation_1_7"].append(named)
    return values


def _make_consumer(model, features, refinement):
    values = _question_values(model, features)
    observables = []
    for name in _QUESTIONS:
        failure, class_values = None, []
        for group in refinement["classes"]:
            left = group["members"][0]
            class_values.append(values[name][left])
            for right in group["members"][1:]:
                if _canonical(values[name][left]) != _canonical(values[name][right]):
                    failure = {
                        "class_id": group["class_id"],
                        "left_state": left,
                        "right_state": right,
                        "left_value": values[name][left],
                        "right_value": values[name][right],
                    }
                    break
            if failure is not None:
                break
        observables.append(
            {
                "name": name,
                "measurable": failure is None,
                "class_values": class_values if failure is None else None,
                "first_failure": failure,
            }
        )
    return {
        "schema_version": "det8-qr05p-consumer-v1",
        "model_sha256": _digest(model),
        "state_classes_sha256": _digest(refinement["state_classes"]),
        "class_count": len(refinement["classes"]),
        "quotient_rows": refinement["quotient_rows"],
        "observables": observables,
    }, values


def _marginal_outcomes(atoms, class_values):
    grouped = {}
    for atom in atoms:
        value = class_values[atom["target_class"]]
        encoded = _canonical(value)
        if encoded not in grouped:
            grouped[encoded] = [value, _zero_table()]
        _add_table(grouped[encoded][1], atom["coefficients"])
    return [
        {"value": value, "coefficients": table} for _, (value, table) in sorted(grouped.items())
    ]


def _consumer_audit(model, features, fine, grid_rows, partitions, refinement, consumer, values):
    prepared = _validate_consumer(consumer)
    inverse = _inverse_vandermonde()
    interpolation_cache = {}
    marginals, checks, nonmeasurable = [], 0, []
    for observable in consumer["observables"]:
        name = observable["name"]
        if not observable["measurable"]:
            nonmeasurable.append(name)
            try:
                predict(consumer, name, 0, ["1/2", "1/2"])
            except ValueError:
                pass
            else:
                raise ValueError("nonmeasurable consumer question was accepted")
            continue
        rows = [
            {
                "class_id": row["class_id"],
                "outcomes": _marginal_outcomes(row["transitions"], observable["class_values"]),
            }
            for row in refinement["quotient_rows"]
        ]
        cells = 0
        for sid, grid_row in enumerate(grid_rows):
            groups = {}
            for target, samples in grid_row:
                value = values[name][target]
                encoded = _canonical(value)
                if encoded not in groups:
                    groups[encoded] = [value, [F(0)] * 16]
                for node, probability in enumerate(samples):
                    groups[encoded][1][node] += probability
            actual = []
            for _, (value, samples) in sorted(groups.items()):
                key = tuple(samples)
                if key not in interpolation_cache:
                    interpolation_cache[key] = _tensor_interpolate(
                        [samples[i : i + 4] for i in range(0, 16, 4)], inverse
                    )
                actual.append({"value": value, "coefficients": interpolation_cache[key]})
            wanted = rows[refinement["state_classes"][sid]]["outcomes"]
            _require(
                _canonical(actual) == _canonical(wanted),
                "summary marginal differs from independently interpolated fine law",
            )
            cells += 16 * len(actual)
        for row in rows:
            for x, y in _POINTS:
                rates = [str(x), str(y)]
                prediction = _predict_core(prepared, name, row["class_id"], rates, (x, y))
                expected = {
                    "question": name,
                    "class_id": row["class_id"],
                    "rates": rates,
                    "outcomes": [
                        {
                            "value": atom["value"],
                            "probability": str(_evaluate(atom["coefficients"], x, y)),
                        }
                        for atom in row["outcomes"]
                    ],
                }
                _require(
                    _canonical(prediction) == _canonical(expected),
                    "consumer core differs from marginal polynomial",
                )
                checks += 1
        marginals.append({"name": name, "rows": rows, "fine_coefficient_cells": cells})
    raw_lookup = {
        _observation_key(s["frame_id"], s["kept"], s["past"]): s["state_id"]
        for s in model["states"]
    }
    keys = [_observation_key(0, [0, v, 7], [[], [0], [0, 1]]) for v in (1, 3)]
    _require(all(key in raw_lookup for key in keys), "required named singleton controls absent")
    ids = [raw_lookup[key] for key in keys]
    tables = []
    for sid in ids:
        table = _zero_table()
        for atom in fine[sid]["transitions"]:
            _add_table(
                table, atom["coefficients"], values["named_relation_1_7"][atom["target_state"]]
            )
        tables.append(table)
    x_table = _zero_table()
    x_table[1][0] = 1
    _require(tables == [x_table, _zero_table()], "named singleton future exclusion")
    c = [partitions["C"]["state_classes"][sid] for sid in ids]
    h = [partitions["H"]["state_classes"][sid] for sid in ids]
    r = [refinement["state_classes"][sid] for sid in ids]
    _require(
        c[0] == c[1] and h[0] == h[1] and r[0] == r[1],
        "singleton closed-summary equivalence failed",
    )
    control = {
        "state_ids": ids,
        "C_classes": c,
        "H_classes": h,
        "R_classes": r,
        "current_values": [values["named_relation_1_7"][sid] for sid in ids],
        "next_coefficients": tables,
        "half_probabilities": [str(_evaluate(table, F(1, 2), F(1, 2))) for table in tables],
        "same_R_class": r[0] == r[1],
    }
    return {
        "marginals": marginals,
        "prediction_checks": checks,
        "nonmeasurable_questions": nonmeasurable,
        "named_singleton_control": control,
        "verified": True,
    }


def analyze(problem):
    """Reconstruct and certify the bounded raw-model summary contract."""
    model = _parse(problem)
    features, fine, grid_rows, fine_audit = _features_and_fine(model)
    partitions = _partitions(model, features)
    rounds = _refine_grid(fine, partitions["C"]["state_classes"], grid_rows)
    refinement = _terminal(fine, partitions, rounds)
    consumer, values = _make_consumer(model, features, refinement)
    consumer_audit = _consumer_audit(
        model, features, fine, grid_rows, partitions, refinement, consumer, values
    )
    result = {
        "model_sha256": _digest(model),
        "features": features,
        "partitions": partitions,
        "fine_kernel": fine_audit,
        "refinement": refinement,
        "consumer": consumer,
        "consumer_audit": consumer_audit,
        "counts": {
            "states": len(model["states"]),
            "features": len(features),
            "C_classes": len(partitions["C"]["classes"]),
            "H_classes": len(partitions["H"]["classes"]),
            "R_classes": len(refinement["classes"]),
            "fine_atoms": fine_audit["transition_atoms"],
            "refinement_rounds": len(rounds),
            "strict_rounds": refinement["strict_rounds"],
            "measurable_questions": sum(o["measurable"] for o in consumer["observables"]),
            "consumer_prediction_checks": consumer_audit["prediction_checks"],
            "consumer_fine_coefficient_cells": sum(
                m["fine_coefficient_cells"] for m in consumer_audit["marginals"]
            ),
        },
    }
    _native_json(result)
    _require(len(_canonical(result)) <= _MAX_WORK, "analysis working byte cap")
    return result
