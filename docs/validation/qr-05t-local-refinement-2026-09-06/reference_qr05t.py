"""Independent full-profile-first/local refinement reference for QR-05T.

Raw features use the locally carried directed-chain/count-law/motif lineage.
Both refinement traces are rebuilt from target-state counts; H is only a later
comparison. Terminal profiles use the independent local-only word/factorial
constructor. No prior artifact, other executor or mutable core is read.
Certificates concern this bounded rank-preserving domain, not physical time.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from math import comb, factorial

F = Fraction
BIT_LIMIT = 4096
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


def _canonical(value):
    try:
        return (
            json.dumps(
                value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
            )
            + "\n"
        ).encode("ascii")
    except (RecursionError, TypeError, OverflowError) as error:
        raise ValueError("native JSON serialization failed") from error


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
        abs(value.numerator).bit_length() <= BIT_LIMIT
        and value.denominator.bit_length() <= BIT_LIMIT,
        "reference rational exceeds the 4096-bit bound",
    )
    return value


def _native_json(value):
    # Memoize completed containers but still count each occurrence in the
    # expanded JSON tree. Node count is a lower bound on serialized bytes, so
    # the existing working cap rejects explosive DAGs before serialization.
    pending = [(value, False)]
    active = set()
    completed = {}
    while pending:
        current, leaving = pending.pop()
        if leaving:
            children = current.values() if type(current) is dict else current
            expanded = 1
            for child in children:
                expanded += completed[id(child)] if type(child) in (list, dict) else 1
                _require(expanded <= _MAX_WORK, "expanded JSON tree exceeds working cap")
            completed[id(current)] = expanded
            active.remove(id(current))
            continue
        if current is None or type(current) in (str, bool):
            continue
        if type(current) is int:
            _require(
                abs(current).bit_length() <= BIT_LIMIT,
                "reference integer exceeds the component bound",
            )
            continue
        _require(type(current) in (list, dict), "reference contains a non-native JSON value")
        identity = id(current)
        _require(identity not in active, "cyclic native container")
        if identity in completed:
            continue
        active.add(identity)
        pending.append((current, True))
        if type(current) is dict:
            _require(
                all(type(key) is str for key in current),
                "reference JSON keys must be native strings",
            )
            children = current.values()
        else:
            children = current
        pending.extend((child, False) for child in children)


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
    return [frame["density"], list(frame["fixed"]), list(frame["eligible"])]


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
    _fields(problem, ("schema_version", "family", "model"), "invalid T problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05t-problem-v1",
        "invalid T schema",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05t_local_refinement",
        "invalid T family",
    )
    model = problem["model"]
    _fields(model, ("frames", "states"), "invalid model fields")
    frames = [
        {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
        {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
    ]
    _require(_canonical(model["frames"]) == _canonical(frames), "invalid fixed frames")
    states = model["states"]
    _require(type(states) is list and 2 <= len(states) <= 4447, "state count bound")
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
    fine_choices = 0
    subset_atoms = 0
    for state in states:
        frame = frames[state["frame_id"]]
        eligible = sorted(set(state["kept"]) & set(frame["eligible"]))
        fine_choices += len(eligible)
        subset_atoms += 2 ** len(eligible)
        for vertex in eligible:
            kept = [v for v in state["kept"] if v != vertex]
            _require(
                _observation_key(state["frame_id"], kept, _induced(state, kept)) in seen,
                "missing single-deletion successor",
            )
    _require(fine_choices <= 26682 and subset_atoms <= 168388, "raw deletion resource bound")
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
        _require(atoms <= 168388, "fine atom bound")
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


def _integer(value, low=0, high=None):
    _require(
        type(value) is int
        and value >= low
        and (high is None or value <= high)
        and abs(value).bit_length() <= BIT_LIMIT,
        "native integer outside bound",
    )


def _colors(value):
    _require(type(value) is list and len(value) == 2, "colors must be a native pair")
    for color in value:
        _integer(color, 0, 3)


def _choose(n, k):
    return comb(n, k) if n >= 0 and 0 <= k <= n else 0


def _copy(value):
    return json.loads(_canonical(value))


def _validate_color_row(atoms, parent, color, classes):
    _require(type(atoms) is list and len(atoms) <= 3, "local color row bound")
    previous = -1
    total = 0
    for atom in atoms:
        _fields(atom, ("target_class", "multiplicity"), "local atom fields")
        target = atom["target_class"]
        _integer(target, 0, len(classes) - 1)
        _require(target > previous, "local targets must be sorted unique")
        previous = target
        _integer(atom["multiplicity"], 1, 3)
        total += atom["multiplicity"]
        child = classes[target]
        expected = list(parent["parent_color_sizes"])
        expected[color] -= 1
        _require(
            child["frame_id"] == parent["frame_id"] and child["parent_color_sizes"] == expected,
            "local target must preserve frame and lower exactly one color",
        )
    _require(total == parent["parent_color_sizes"][color], "local color row mass")


def _validate_local_model(local_model):
    _native_json(local_model)
    _fields(local_model, ("schema_version", "classes"), "local-only model fields")
    _require(
        type(local_model["schema_version"]) is str
        and local_model["schema_version"] == "det8-qr05s-local-v1",
        "local-only model schema",
    )
    classes = local_model["classes"]
    _require(type(classes) is list and 1 <= len(classes) <= 512, "local class resource bound")
    for cid, row in enumerate(classes):
        _fields(
            row,
            ("class_id", "frame_id", "parent_color_sizes", "odd", "even"),
            "local class fields",
        )
        _integer(row["class_id"], cid, cid)
        _integer(row["frame_id"], 0, 1)
        _colors(row["parent_color_sizes"])
    for row in classes:
        for color, name in enumerate(("odd", "even")):
            _validate_color_row(row[name], row, color, classes)
    _require(
        sum(len(row[name]) for row in classes for name in ("odd", "even")) <= 3072,
        "local atom resource bound",
    )
    _require(len(_canonical(local_model)) <= _MAX_WORK, "local input byte cap")
    return classes


def _advance(vector, rows):
    result = {}
    for source, paths in vector.items():
        for target, multiplicity in rows[source].items():
            result[target] = result.get(target, 0) + paths * multiplicity
            _integer(result[target])
    return result


def _word_profiles(classes):
    """One fixed color word: odd deletion powers followed by even powers."""
    operators = [
        [{edge["target_class"]: edge["multiplicity"] for edge in row[name]} for row in classes]
        for name in ("odd", "even")
    ]
    profiles = []
    atoms = 0
    for source, parent in enumerate(classes):
        O, E = parent["parent_color_sizes"]
        counts = {}
        odds = {source: 1}  # An empty word is identity, not a zero-color deletion.
        for a in range(O + 1):
            word = dict(odds)
            for b in range(E + 1):
                divisor = factorial(a) * factorial(b)
                for target, paths in word.items():
                    _require(paths % divisor == 0, "ordered-word count is not factorial divisible")
                    count = paths // divisor
                    _integer(count, 1)
                    wanted = [O - a, E - b]
                    _require(
                        classes[target]["frame_id"] == parent["frame_id"]
                        and classes[target]["parent_color_sizes"] == wanted,
                        "word target rank/frame",
                    )
                    _require(target not in counts, "one target reached at inconsistent word rank")
                    counts[target] = count
                word = _advance(word, operators[1])
            _require(not word, "even deletion beyond its boundary is not zero")
            odds = _advance(odds, operators[0])
        _require(not odds, "odd deletion beyond its boundary is not zero")
        transitions = []
        for target, count in sorted(counts.items()):
            o, e = classes[target]["parent_color_sizes"]
            _integer(count, 1, min(9, _choose(O, o) * _choose(E, e)))
            transitions.append(
                {"target_class": target, "retained_color_sizes": [o, e], "multiplicity": count}
            )
        atoms += len(transitions)
        _require(atoms <= 32768, "reconstructed profile atom resource bound")
        profiles.append(
            {"class_id": source, "parent_color_sizes": [O, E], "transitions": transitions}
        )
    return profiles, operators


def _recurrence_certificate(classes, profiles, operators):
    maps = [
        {edge["target_class"]: edge["multiplicity"] for edge in row["transitions"]}
        for row in profiles
    ]
    base_cells = 0
    recurrence_cells = 0
    for source, parent in enumerate(classes):
        O, E = parent["parent_color_sizes"]
        ranks = _zero_table()
        for target, child in enumerate(classes):
            value = maps[source].get(target, 0)
            m, n = child["parent_color_sizes"]
            compatible = child["frame_id"] == parent["frame_id"] and m <= O and n <= E
            if not compatible:
                _require(value == 0, "other-frame or impossible target is nonzero")
                continue
            ranks[m][n] += value
            if (O, E) == (m, n):
                base_cells += 1
                _require(value == int(source == target), "zero-deletion identity/base delta")
            for color, difference in enumerate((O - m, E - n)):
                if difference == 0:
                    continue
                recurrence_cells += 1
                total = sum(
                    multiplicity * maps[middle].get(target, 0)
                    for middle, multiplicity in operators[color][source].items()
                )
                _integer(total)
                _require(
                    total % difference == 0 and total // difference == value,
                    "independent local recurrence or exact division failed",
                )
        for o, e in product(range(4), repeat=2):
            _require(ranks[o][e] == _choose(O, o) * _choose(E, e), "full rank normalization")
        _require(sum(map(sum, ranks)) == 2 ** (O + E), "full subset mass")
    return {
        "target_cells": len(classes) ** 2,
        "base_cells": base_cells,
        "recurrence_cells": recurrence_cells,
        "normalization_cells": 16 * len(classes),
        "max_abs_residual": 0,
    }


def _operator_checks(classes, profiles, operators):
    rows = []
    for source, parent in enumerate(classes):
        O, E = parent["parent_color_sizes"]
        oo = _advance(operators[0][source], operators[0])
        ee = _advance(operators[1][source], operators[1])
        oe = _advance(operators[0][source], operators[1])
        eo = _advance(operators[1][source], operators[0])
        _require(oe == eo, "odd/even deletion words do not commute")
        targets = {}
        for grade, scale in (((O - 2, E), 2), ((O, E - 2), 2), ((O - 1, E - 1), 1)):
            targets[grade] = {
                edge["target_class"]: scale * edge["multiplicity"]
                for edge in profiles[source]["transitions"]
                if tuple(edge["retained_color_sizes"]) == grade
            }
        _require(oo == targets[(O - 2, E)], "odd-odd paths lack the 2! profile factor")
        _require(ee == targets[(O, E - 2)], "even-even paths lack the 2! profile factor")
        _require(oe == targets[(O - 1, E - 1)], "mixed words differ from the full profile")
        masses = (sum(oo.values()), sum(ee.values()), sum(oe.values()))
        _require(masses == (O * (O - 1), E * (E - 1), O * E), "two-deletion word masses")
        rows.append(
            {
                "class_id": source,
                "odd_odd_targets": len(oo),
                "even_even_targets": len(ee),
                "mixed_targets": len(oe),
                "coefficient_cells": len(oo) + len(ee) + 2 * len(oe),
                "odd_odd_pairs": masses[0],
                "even_even_pairs": masses[1],
                "mixed_pairs": masses[2],
                "max_abs_residual": 0,
            }
        )
    return {
        "verified": True,
        "rows": rows,
        "totals": {
            field: sum(row[field] for row in rows)
            for field in (
                "odd_odd_targets",
                "even_even_targets",
                "mixed_targets",
                "coefficient_cells",
                "odd_odd_pairs",
                "even_even_pairs",
                "mixed_pairs",
                "max_abs_residual",
            )
        },
    }


def reconstruct_profiles(local_model):
    """Construct complete profiles using only validated local class counts.

    Structural/algebraic validity does not authenticate H labels, raw-domain
    membership, or realization by an observed partial order.
    """
    classes = _validate_local_model(local_model)
    profiles, operators = _word_profiles(classes)
    certificate = _recurrence_certificate(classes, profiles, operators)
    checks = _operator_checks(classes, profiles, operators)
    result = {"profiles": profiles, "certificate": certificate, "operator_checks": checks}
    _native_json(result)
    _require(len(_canonical(result)) <= _MAX_WORK, "local output byte cap")
    return _copy(result)


def _validate_local_partition(local_rows, partition):
    _native_json(local_rows)
    _native_json(partition)
    _fields(partition, ("state_classes", "classes"), "local partition fields")
    _require(type(local_rows) is list and 1 <= len(local_rows) <= 4447, "local state bound")
    vector = partition["state_classes"]
    _require(type(vector) is list and len(vector) == len(local_rows), "local state class vector")
    groups = []
    for sid, cid in enumerate(vector):
        _integer(cid, 0, len(groups))
        if cid == len(groups):
            groups.append({"class_id": cid, "members": []})
        groups[cid]["members"].append(sid)
    _require(len(groups) <= 512, "local partition class bound")
    supplied = partition["classes"]
    _require(type(supplied) is list and len(supplied) == len(groups), "local class fibers")
    for expected, group in zip(groups, supplied, strict=True):
        _require(
            type(group) is dict
            and set(group) in ({"class_id", "members"}, {"class_id", "key", "members"}),
            "local class fields",
        )
        _require(
            _canonical({name: group[name] for name in ("class_id", "members")})
            == _canonical(expected),
            "local fibers must be canonical and exact",
        )
    for sid, row in enumerate(local_rows):
        _fields(
            row, ("state_id", "frame_id", "parent_color_sizes", "odd", "even"), "fine local row"
        )
        _integer(row["state_id"], sid, sid)
        _integer(row["frame_id"], 0, 1)
        _colors(row["parent_color_sizes"])
    classes = [local_rows[g["members"][0]] for g in groups]
    for group in groups:
        rep = classes[group["class_id"]]
        for sid in group["members"]:
            row = local_rows[sid]
            _require(
                row["frame_id"] == rep["frame_id"]
                and row["parent_color_sizes"] == rep["parent_color_sizes"],
                "local class does not fix frame and parent rank",
            )
            for color, name in enumerate(("odd", "even")):
                _validate_color_row(row[name], row, color, classes)
    return groups


def closure_from_local(local_rows, partition):
    groups = _validate_local_partition(local_rows, partition)
    witness = None
    comparisons = 0
    for group in groups:
        left = group["members"][0]
        for right in group["members"][1:]:
            comparisons += 1
            for color in ("odd", "even"):
                lhs = {a["target_class"]: a["multiplicity"] for a in local_rows[left][color]}
                rhs = {a["target_class"]: a["multiplicity"] for a in local_rows[right][color]}
                different = [
                    target
                    for target in sorted(lhs.keys() | rhs.keys())
                    if lhs.get(target, 0) != rhs.get(target, 0)
                ]
                if different and witness is None:
                    target = different[0]
                    witness = {
                        "class_id": group["class_id"],
                        "left_state": left,
                        "right_state": right,
                        "color": color,
                        "target_class": target,
                        "left_multiplicity": lhs.get(target, 0),
                        "right_multiplicity": rhs.get(target, 0),
                    }
    return {
        "closed": witness is None,
        "classes_checked": len(groups),
        "member_comparisons": comparisons,
        "witness": witness,
    }


def _closure(partition, local_rows):
    closure = closure_from_local(local_rows, partition)
    if not closure["closed"]:
        return closure, [], None
    local_classes = []
    for group in partition["classes"]:
        sid = group["members"][0]
        local_classes.append(
            {
                "class_id": group["class_id"],
                "representative_state": sid,
                **{
                    name: _copy(local_rows[sid][name])
                    for name in ("frame_id", "parent_color_sizes", "odd", "even")
                },
            }
        )
    # This is the only information passed to the public local-only constructor.
    local_model = {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {
                name: row[name]
                for name in ("class_id", "frame_id", "parent_color_sizes", "odd", "even")
            }
            for row in local_classes
        ],
    }
    built = reconstruct_profiles(local_model)
    class_profiles = [
        {
            "class_id": row["class_id"],
            "representative_state": local_classes[row["class_id"]]["representative_state"],
            "parent_color_sizes": row["parent_color_sizes"],
            "transitions": row["transitions"],
        }
        for row in built["profiles"]
    ]
    return (
        closure,
        local_classes,
        {
            "class_profiles": class_profiles,
            "certificate": built["certificate"],
            "operator_checks": built["operator_checks"],
        },
    )


def _local_closure(partition, local_rows):
    return _closure(partition, local_rows)


def _expand_profiles(profiles):
    kernels, _ = _kernel_cache(_inverse_vandermonde())
    rows = []
    for profile in profiles:
        O, E = profile["parent_color_sizes"]
        rows.append(
            {
                "state_id": profile["state_id"],
                "transitions": [
                    {
                        "target_class": atom["target_class"],
                        "coefficients": [
                            [atom["multiplicity"] * cell for cell in line]
                            for line in kernels[(O, E, *atom["retained_color_sizes"])]
                        ],
                    }
                    for atom in profile["transitions"]
                ],
            }
        )
    return rows


def _feature_partition(model, features, with_path):
    vector, groups, registry = [], [], {}
    for state, feature in zip(model["states"], features, strict=True):
        _require(
            [feature["pair_graded"][0][1][1][0], feature["pair_graded"][0][1][0][1]]
            == feature["color_sizes"],
            "feature key does not observe colors",
        )
        key = [
            _frame_key(model["frames"][state["frame_id"]]),
            feature["pair_graded"],
            feature["motif_count"],
        ]
        if with_path:
            key.append(feature["path_count"])
        encoded = _canonical(key)
        if encoded not in registry:
            registry[encoded] = len(groups)
            groups.append({"class_id": len(groups), "key": key, "members": []})
        cid = registry[encoded]
        vector.append(cid)
        groups[cid]["members"].append(state["state_id"])
    _require(len(groups) <= 512, "feature partition class bound")
    return {"state_classes": vector, "classes": groups}


def _validate_raw_counts(rows, mode):
    _native_json(rows)
    _require(type(rows) is list and 1 <= len(rows) <= 4447, "raw count state bound")
    names = ("odd", "even") if mode == "local" else ("transitions",)
    fields = ("state_id", "frame_id", "parent_color_sizes", *names)
    for sid, row in enumerate(rows):
        _fields(row, fields, "raw count fields")
        _integer(row["state_id"], sid, sid)
        _integer(row["frame_id"], 0, 1)
        _colors(row["parent_color_sizes"])
    total_choices = 0
    total_atoms = 0
    for sid, row in enumerate(rows):
        O, E = row["parent_color_sizes"]
        rank_counts = _zero_table()
        for color, name in enumerate(names):
            atoms = row[name]
            _require(
                type(atoms) is list and len(atoms) <= (3 if mode == "local" else 64),
                "raw atom bound",
            )
            previous = -1
            mass = 0
            for atom in atoms:
                _fields(atom, ("target_state", "multiplicity"), "raw count atom fields")
                target = atom["target_state"]
                _integer(target, 0, len(rows) - 1)
                _require(target > previous, "raw targets must be sorted unique")
                previous = target
                child = rows[target]
                m, n = child["parent_color_sizes"]
                _require(child["frame_id"] == row["frame_id"], "raw transition changes frame")
                if mode == "local":
                    expected = [O, E]
                    expected[color] -= 1
                    _require([m, n] == expected, "raw local color decrement")
                    _integer(atom["multiplicity"], 1, 3)
                else:
                    _require(m <= O and n <= E, "raw full target grade exceeds parent")
                    _integer(atom["multiplicity"], 1, min(9, _choose(O, m) * _choose(E, n)))
                    if (m, n) == (O, E):
                        _require(
                            target == sid and atom["multiplicity"] == 1, "raw full-rank self delta"
                        )
                    rank_counts[m][n] += atom["multiplicity"]
                mass += atom["multiplicity"]
            if mode == "local":
                _require(mass == (O, E)[color], "raw local row mass")
            total_choices += mass
            total_atoms += len(atoms)
        if mode == "full":
            for m, n in product(range(4), repeat=2):
                _require(
                    rank_counts[m][n] == _choose(O, m) * _choose(E, n),
                    "raw full binomial normalization",
                )
    cap = 26682 if mode == "local" else 168388
    _require(total_choices <= cap and total_atoms <= cap, "raw count resource bound")
    _require(len(_canonical(rows)) <= _MAX_WORK, "raw count working cap")


def _groups(vector, rows):
    _native_json(vector)
    _require(type(vector) is list and len(vector) == len(rows), "partition vector shape")
    groups = []
    for sid, cid in enumerate(vector):
        _integer(cid, 0, len(groups))
        if cid == len(groups):
            groups.append({"class_id": cid, "members": []})
        groups[cid]["members"].append(sid)
    _require(1 <= len(groups) <= 512, "partition class bound")
    for group in groups:
        rep = rows[group["members"][0]]
        _require(
            all(
                rows[sid]["frame_id"] == rep["frame_id"]
                and rows[sid]["parent_color_sizes"] == rep["parent_color_sizes"]
                for sid in group["members"]
            ),
            "partition does not fix frame/ranks",
        )
    return groups


def _aggregate(rows, vector, mode):
    _groups(vector, rows)
    result = []
    for row in rows:
        if mode == "local":
            pushed = {
                "state_id": row["state_id"],
                "frame_id": row["frame_id"],
                "parent_color_sizes": list(row["parent_color_sizes"]),
            }
            for color, name in enumerate(("odd", "even")):
                counts = {}
                for atom in row[name]:
                    target = vector[atom["target_state"]]
                    counts[target] = counts.get(target, 0) + atom["multiplicity"]
                pushed[name] = [
                    {"target_class": target, "multiplicity": count}
                    for target, count in sorted(counts.items())
                ]
                _require(
                    sum(counts.values()) == row["parent_color_sizes"][color],
                    "aggregated local row mass",
                )
        else:
            counts = {}
            colors = {}
            for atom in row["transitions"]:
                target = vector[atom["target_state"]]
                rank = rows[atom["target_state"]]["parent_color_sizes"]
                if target in colors:
                    _require(colors[target] == rank, "aggregated target has ambiguous rank")
                colors[target] = rank
                counts[target] = counts.get(target, 0) + atom["multiplicity"]
            rank_counts = _zero_table()
            transitions = []
            O, E = row["parent_color_sizes"]
            for target, count in sorted(counts.items()):
                m, n = colors[target]
                _integer(count, 1, min(9, _choose(O, m) * _choose(E, n)))
                rank_counts[m][n] += count
                transitions.append(
                    {"target_class": target, "retained_color_sizes": [m, n], "multiplicity": count}
                )
            for m, n in product(range(4), repeat=2):
                _require(
                    rank_counts[m][n] == _choose(O, m) * _choose(E, n),
                    "aggregated full normalization",
                )
            pushed = {
                "state_id": row["state_id"],
                "parent_color_sizes": list(row["parent_color_sizes"]),
                "transitions": transitions,
            }
        result.append(pushed)
    return result


def _signature(row, old_class, mode):
    if mode == "local":
        return [old_class, row["odd"], row["even"]]
    return [old_class, row["transitions"]]


def _next_vector(current, pushed, mode):
    ids = {}
    result = []
    for sid, row in enumerate(pushed):
        key = _canonical(_signature(row, current[sid], mode))
        if key not in ids:
            ids[key] = len(ids)
        result.append(ids[key])
    _require(len(ids) <= 512, "refined class resource bound")
    return result


def _difference(lhs, rhs, mode):
    names = ("odd", "even") if mode == "local" else ("transitions",)
    for name in names:
        left = {a["target_class"]: a for a in lhs[name]}
        right = {a["target_class"]: a for a in rhs[name]}
        for target in sorted(left.keys() | right.keys()):
            l = left.get(target, {}).get("multiplicity", 0)
            r = right.get(target, {}).get("multiplicity", 0)
            if l != r:
                result = {"target_class": target, "left_multiplicity": l, "right_multiplicity": r}
                if mode == "local":
                    result["color"] = name
                else:
                    result["retained_color_sizes"] = list(
                        (left.get(target) or right[target])["retained_color_sizes"]
                    )
                return result
    raise ValueError("claimed split has no complete-row difference")


def _refine(rows, initial, mode):
    current = list(initial)
    initial_groups = _groups(current, rows)
    bound = min(6, len(rows) - len(initial_groups))
    rounds = []
    for index in range(bound + 1):
        groups = _groups(current, rows)
        pushed = _aggregate(rows, current, mode)
        next_vector = _next_vector(current, pushed, mode)
        next_groups = _groups(next_vector, rows)
        comparisons = 0
        for group in groups:
            left = group["members"][0]
            lhs = _signature(pushed[left], current[left], mode)
            for right in group["members"][1:]:
                comparisons += 1
                rhs = _signature(pushed[right], current[right], mode)
                _require(
                    (next_vector[left] == next_vector[right]) == (lhs == rhs),
                    "all-member signature classification",
                )
        separations = []
        for child in next_groups:
            right = child["members"][0]
            parent = current[right]
            _require(
                all(current[sid] == parent for sid in child["members"]),
                "refinement merged inherited classes",
            )
            left = groups[parent]["members"][0]
            if next_vector[left] == child["class_id"]:
                continue
            separations.append(
                {
                    "parent_class_id": parent,
                    "child_class_id": child["class_id"],
                    "left_state": left,
                    "right_state": right,
                    **_difference(pushed[left], pushed[right], mode),
                }
            )
        _require(len(separations) == len(next_groups) - len(groups), "one witness per new child")
        stable = next_vector == current
        _require(stable or len(next_groups) > len(groups), "nonstable refinement does not split")
        names = ("odd", "even") if mode == "local" else ("transitions",)
        atoms = sum(len(row[name]) for row in pushed for name in names)
        rounds.append(
            {
                "round_index": index,
                "state_classes": list(current),
                "classes": groups,
                "rows_sha256": _digest(pushed),
                "signature_atoms": atoms,
                "member_comparisons": comparisons,
                "stable": stable,
                "separations": separations,
            }
        )
        if stable:
            break
        _require(index < bound, "rank-based strict-round bound exceeded")
        current = next_vector
    _require(rounds[-1]["stable"], "refinement ended before stability")
    result = {
        "mode": mode,
        "rounds": rounds,
        "strict_rounds": len(rounds) - 1,
        "state_classes": list(current),
        "classes": _groups(current, rows),
        "counts": {
            "rounds": len(rounds),
            "signature_atoms": sum(row["signature_atoms"] for row in rounds),
            "member_comparisons": sum(row["member_comparisons"] for row in rounds),
            "separations": sum(len(row["separations"]) for row in rounds),
        },
    }
    _native_json(result)
    _require(len(_canonical(result)) <= _MAX_WORK, "refinement output working cap")
    return _copy(result)


def refine_local(local_problem):
    _native_json(local_problem)
    _fields(
        local_problem,
        ("schema_version", "state_classes", "rows"),
        "local refinement problem fields",
    )
    _require(
        type(local_problem["schema_version"]) is str
        and local_problem["schema_version"] == "det8-qr05t-local-v1",
        "local refinement schema",
    )
    _validate_raw_counts(local_problem["rows"], "local")
    _groups(local_problem["state_classes"], local_problem["rows"])
    _require(len(_canonical(local_problem)) <= _MAX_WORK, "local refinement input cap")
    return _refine(local_problem["rows"], local_problem["state_classes"], "local")


def _refine_full(rows, state_classes):
    _validate_raw_counts(rows, "full")
    _groups(state_classes, rows)
    return _refine(rows, state_classes, "full")


def _raw_rows(model, features, fine):
    lookup = {
        _observation_key(s["frame_id"], s["kept"], s["past"]): s["state_id"]
        for s in model["states"]
    }
    local = []
    full = []
    for sid, state in enumerate(model["states"]):
        frame = model["frames"][state["frame_id"]]
        counts = [{}, {}]
        for vertex in sorted(set(state["kept"]) & set(frame["eligible"])):
            kept = [v for v in state["kept"] if v != vertex]
            key = _observation_key(state["frame_id"], kept, _induced(state, kept))
            _require(key in lookup, "raw singleton deletion absent")
            target = lookup[key]
            color = 0 if vertex % 2 else 1
            counts[color][target] = counts[color].get(target, 0) + 1
        row = {
            "state_id": sid,
            "frame_id": state["frame_id"],
            "parent_color_sizes": list(features[sid]["color_sizes"]),
            **{
                name: [
                    {"target_state": target, "multiplicity": count}
                    for target, count in sorted(counts[color].items())
                ]
                for color, name in enumerate(("odd", "even"))
            },
        }
        _require(
            all(atom["multiplicity"] == 1 for name in ("odd", "even") for atom in row[name]),
            "raw deletion target is not one vertex",
        )
        local.append(row)
        full.append(
            {
                "state_id": sid,
                "frame_id": state["frame_id"],
                "parent_color_sizes": list(features[sid]["color_sizes"]),
                "transitions": [
                    {"target_state": atom["target_state"], "multiplicity": 1}
                    for atom in fine[sid]["transitions"]
                ],
            }
        )
    _validate_raw_counts(local, "local")
    _validate_raw_counts(full, "full")
    for sid, row in enumerate(local):
        for color, name in enumerate(("odd", "even")):
            target_rank = list(row["parent_color_sizes"])
            target_rank[color] -= 1
            expected = [
                atom
                for atom in full[sid]["transitions"]
                if full[atom["target_state"]]["parent_color_sizes"] == target_rank
            ]
            _require(expected == row[name], "local counts are not full one-deletion rank slices")
    return local, full


def _partition_map(finer, coarser):
    result = []
    for sid, cid in enumerate(finer):
        if cid == len(result):
            result.append(coarser[sid])
        elif result[cid] != coarser[sid]:
            return None
    return result


def analyze(problem):
    model = _parse(problem)
    features, fine, _, fine_audit = _features_and_fine(model)
    c = _feature_partition(model, features, False)
    raw_local, raw_full = _raw_rows(model, features, fine)
    # Full profiles are the priority reference construction. Neither trace
    # receives H, path counts, or any previously grouped result.
    full_trace = _refine_full(raw_full, c["state_classes"])
    local_trace = refine_local(
        {
            "schema_version": "det8-qr05t-local-v1",
            "state_classes": c["state_classes"],
            "rows": raw_local,
        }
    )
    lv, fv = local_trace["state_classes"], full_trace["state_classes"]
    _require(lv == fv, "local/full terminal actual fibers differ")
    local_pushed = _aggregate(raw_local, lv, "local")
    direct_profiles = _aggregate(raw_full, lv, "full")
    closure, class_locals, reconstruction = _closure(
        {"state_classes": lv, "classes": local_trace["classes"]}, local_pushed
    )
    _require(closure["closed"] and reconstruction is not None, "terminal local closure failed")
    for group in local_trace["classes"]:
        reference = direct_profiles[group["members"][0]]["transitions"]
        for sid in group["members"][1:]:
            _require(
                direct_profiles[sid]["transitions"] == reference, "terminal full closure failed"
            )
    class_profiles = reconstruction["class_profiles"]
    rebuilt = [
        {
            "state_id": sid,
            "parent_color_sizes": list(class_profiles[cid]["parent_color_sizes"]),
            "transitions": class_profiles[cid]["transitions"],
        }
        for sid, cid in enumerate(lv)
    ]
    _require(
        _canonical(rebuilt) == _canonical(direct_profiles),
        "terminal local-only reconstruction differs from full raw census",
    )
    pushed = _push(fine, lv)
    _require(
        _canonical(_expand_profiles(direct_profiles)) == _canonical(pushed),
        "terminal full-profile power expansion differs",
    )
    quotient = [
        {
            "class_id": group["class_id"],
            "representative_state": group["members"][0],
            "transitions": pushed[group["members"][0]]["transitions"],
        }
        for group in local_trace["classes"]
    ]
    # H is constructed only after both terminal traces and reconstruction.
    h = _feature_partition(model, features, True)
    h_rows = _aggregate(raw_local, h["state_classes"], "local")
    h_closed = closure_from_local(h_rows, h)["closed"]
    vectors = [c["state_classes"], lv, fv, h["state_classes"]]
    relation = [[_partition_map(left, right) is not None for right in vectors] for left in vectors]
    maps = {
        "L_to_C": _partition_map(lv, vectors[0]),
        "F_to_C": _partition_map(fv, vectors[0]),
        "L_to_F": _partition_map(lv, fv),
        "F_to_L": _partition_map(fv, lv),
        "L_to_H": _partition_map(lv, vectors[3]),
        "H_to_L": _partition_map(vectors[3], lv),
    }
    aligned = []
    for index in range(max(len(local_trace["rounds"]), len(full_trace["rounds"]))):
        l = local_trace["rounds"][min(index, len(local_trace["rounds"]) - 1)]["state_classes"]
        f = full_trace["rounds"][min(index, len(full_trace["rounds"]) - 1)]["state_classes"]
        aligned.append(_partition_map(f, l) is not None)
    _require(all(aligned), "aligned full refinement does not refine local")
    _require(not h_closed or maps["H_to_L"] is not None, "closed H does not refine the terminal")
    all_refine = all(
        _partition_map(row["state_classes"], c["state_classes"]) is not None
        for trace in (local_trace, full_trace)
        for row in trace["rounds"]
    )
    _require(all_refine, "a trace does not refine C")
    for trace in (local_trace, full_trace):
        for row in trace["rounds"]:
            _groups(row["state_classes"], raw_local)
    profile_atoms = sum(len(row["transitions"]) for row in direct_profiles)
    result = {
        "model_sha256": _digest(model),
        "features": features,
        "partitions": {"C": c, "H": h},
        "fine_kernel": {"sha256": fine_audit["sha256"], "atoms": fine_audit["transition_atoms"]},
        "fine_deletions": {
            "sha256": _digest(raw_local),
            "atoms": sum(len(row[name]) for row in raw_local for name in ("odd", "even")),
            "choices": sum(
                atom["multiplicity"]
                for row in raw_local
                for name in ("odd", "even")
                for atom in row[name]
            ),
        },
        "local_refinement": local_trace,
        "full_refinement": full_trace,
        "comparison": {
            "names": ["C", "L", "F", "H"],
            "refinement": relation,
            "maps": maps,
            "same_terminal_memberships": lv == fv,
            "same_memberships_as_H": maps["L_to_H"] is not None and maps["H_to_L"] is not None,
            "H_local_closed": h_closed,
            "aligned_full_refines_local": aligned,
        },
        "terminal": {
            "local_rows": class_locals,
            "class_profiles": class_profiles,
            "reconstruction": {
                "certificate": reconstruction["certificate"],
                "operator_checks": reconstruction["operator_checks"],
            },
            "closure": {
                "local_closed": True,
                "full_closed": True,
                "classes_checked": closure["classes_checked"],
                "member_comparisons": closure["member_comparisons"],
            },
            "comparison": {
                "direct_profiles_sha256": _digest(direct_profiles),
                "reconstructed_profiles_sha256": _digest(rebuilt),
                "pushed_rows_sha256": _digest(pushed),
                "quotient_rows_sha256": _digest(quotient),
                "profile_cells": 16 * profile_atoms,
                "power_cells": 16 * profile_atoms,
                "max_abs_residual": 0,
            },
        },
        "minimality": {
            "verified": True,
            "initial_partition": "C",
            "terminal_partition": "L",
            "all_rounds_refine_C": all_refine,
            "all_rounds_rank_frame_measurable": True,
            "local_full_terminals_equal": lv == fv,
            "H_used_in_construction": False,
            "strict_round_bound": min(6, len(features) - len(c["classes"])),
            "relative_to_C": True,
            "arbitrary_partitions_enumerated": False,
        },
        "counts": {
            "states": len(features),
            "C_classes": len(c["classes"]),
            "H_classes": len(h["classes"]),
            "L_classes": len(local_trace["classes"]),
            "F_classes": len(full_trace["classes"]),
            "fine_atoms": fine_audit["transition_atoms"],
            "fine_local_choices": sum(
                sum(atom["multiplicity"] for atom in row[name])
                for row in raw_local
                for name in ("odd", "even")
            ),
            "local_strict_rounds": local_trace["strict_rounds"],
            "full_strict_rounds": full_trace["strict_rounds"],
            "terminal_local_atoms": sum(
                len(row[name]) for row in class_locals for name in ("odd", "even")
            ),
            "terminal_profile_atoms": sum(len(row["transitions"]) for row in class_profiles),
        },
    }
    _native_json(result)
    _require(len(_canonical(result)) <= _MAX_WORK, "analysis working cap")
    return _copy(result)
