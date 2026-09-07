"""Independent inverse-basis/count-law reference for QR-05R.

Only the declared raw observation model enters this executor. Directed chains,
full induced count-law moments, alternative M/T recognizers, and rational fine
interpolation are locally carried from the independent P/Q utility lineage.
Integer deletion profiles are recovered by Gaussian tensor-basis inversion
and checked against a separately enumerated odd/even subset census.
No prior artifact, executor, mutable core or source file is read at runtime.
This verifies finite deletion laws, not expanded minimality or physical time.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import comb

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
        abs(value.numerator).bit_length() <= BIT_LIMIT
        and value.denominator.bit_length() <= BIT_LIMIT,
        "reference rational exceeds the 4096-bit bound",
    )
    return value


def _native_json(value):
    if value is None or type(value) in (str, bool):
        return
    if type(value) is int:
        _require(
            abs(value).bit_length() <= BIT_LIMIT, "reference integer exceeds the component bound"
        )
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
    _fields(problem, ("schema_version", "family", "model"), "invalid R problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05r-problem-v1",
        "invalid R schema",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05r_deletion_profile",
        "invalid R family",
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


def _table(table):
    _require(type(table) is list and len(table) == 4, "table must have four native rows")
    for row in table:
        _require(type(row) is list and len(row) == 4, "table must have four native columns")
        for value in row:
            _require(
                type(value) is int and abs(value).bit_length() <= BIT_LIMIT,
                "table coefficient must be a bounded native integer",
            )


def _choose(n, k):
    return comb(n, k) if n >= 0 and 0 <= k <= n else 0


@lru_cache(maxsize=16)
def _one_basis(degree, retained):
    # Multiply x^retained by (1-x) one factor at a time; no basis-inverse formula.
    coefficients = [0] * retained + [1]
    for _ in range(degree - retained):
        updated = [0] * (len(coefficients) + 1)
        for i, value in enumerate(coefficients):
            updated[i] += value
            updated[i + 1] -= value
        coefficients = updated
    return tuple(coefficients + [0] * (4 - len(coefficients)))


@lru_cache(maxsize=4)
def _inverse_matrix(degree):
    n = degree + 1
    work = [
        [F(_one_basis(degree, grade)[power]) for grade in range(n)]
        + [F(int(power == j)) for j in range(n)]
        for power in range(n)
    ]
    for column in range(n):
        pivot = next(i for i in range(column, n) if work[i][column])
        work[pivot], work[column] = work[column], work[pivot]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for i in range(n):
            if i == column:
                continue
            scale = work[i][column]
            work[i] = [a - scale * b for a, b in zip(work[i], work[column], strict=True)]
    _require(
        all(work[i][j] == int(i == j) for i in range(n) for j in range(n)),
        "exact basis inverse failed",
    )
    return tuple(tuple(row[n:]) for row in work)


def expand_grade_table(grades, parent_color_sizes):
    """Expand signed integer coefficients in the unscaled Bernstein tensor basis."""
    _native_json(grades)
    _table(grades)
    _colors(parent_color_sizes)
    O, E = parent_color_sizes
    _require(
        all(grades[o][e] == 0 for o in range(4) for e in range(4) if o > O or e > E),
        "grade table exceeds parent degree",
    )
    power = _zero_table()
    for o in range(O + 1):
        odd = _one_basis(O, o)
        for e in range(E + 1):
            even = _one_basis(E, e)
            for i in range(4):
                for j in range(4):
                    power[i][j] += grades[o][e] * odd[i] * even[j]
    _table(power)
    return power


@lru_cache(maxsize=1024)
def _inverse_table(power, O, E):
    """Immutable-content memoization of the exact Gaussian tensor operation."""
    left, right = _inverse_matrix(O), _inverse_matrix(E)
    grades = _zero_table()
    for o in range(O + 1):
        for e in range(E + 1):
            value = _bounded(
                sum(
                    (
                        left[o][i] * F(power[i][j]) * right[e][j]
                        for i in range(O + 1)
                        for j in range(E + 1)
                    ),
                    F(0),
                )
            )
            _require(value.denominator == 1, "inverse basis coefficient is not integral")
            grades[o][e] = value.numerator
    return tuple(tuple(row) for row in grades)


def inverse_basis(power, parent_color_sizes):
    """Recover the full signed grade table by two exact Gaussian inverse matrices."""
    _native_json(power)
    _table(power)
    _colors(parent_color_sizes)
    O, E = parent_color_sizes
    _require(
        all(power[i][j] == 0 for i in range(4) for j in range(4) if i > O or j > E),
        "power polynomial exceeds declared parent degree",
    )
    grades = [list(row) for row in _inverse_table(tuple(tuple(row) for row in power), O, E)]
    # These checks remain outside the cache: input mutation or a stricter bit
    # limit cannot be hidden by a previously evaluated polynomial.
    _table(grades)
    _require(expand_grade_table(grades, parent_color_sizes) == power, "basis inverse round trip")
    return grades


def _partition(model, features):
    vector, classes, registry = [], [], {}
    for raw, feature in zip(model["states"], features, strict=True):
        _require(
            [feature["pair_graded"][0][1][1][0], feature["pair_graded"][0][1][0][1]]
            == feature["color_sizes"],
            "H does not recover raw parent colors",
        )
        key = [
            _frame_key(model["frames"][raw["frame_id"]]),
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
        classes[cid]["members"].append(raw["state_id"])
    for group in classes:
        rep = group["members"][0]
        _require(
            all(
                features[sid]["color_sizes"] == features[rep]["color_sizes"]
                for sid in group["members"]
            ),
            "H fiber has mixed parent degrees",
        )
    return {"state_classes": vector, "classes": classes}


def _subset_census(model, vector):
    """Separate rank-first odd/even combination enumeration, not a fine-row sum."""
    lookup = {
        _observation_key(s["frame_id"], s["kept"], s["past"]): s["state_id"]
        for s in model["states"]
    }
    result = []
    for raw in model["states"]:
        frame = model["frames"][raw["frame_id"]]
        present = set(raw["kept"]) & set(frame["eligible"])
        odd = sorted(v for v in present if v % 2)
        even = sorted(v for v in present if not v % 2)
        counts = {}
        for o in range(len(odd) + 1):
            for odds in combinations(odd, o):
                for e in range(len(even) + 1):
                    for evens in combinations(even, e):
                        kept = sorted(frame["fixed"] + list(odds) + list(evens))
                        key = _observation_key(raw["frame_id"], kept, _induced(raw, kept))
                        _require(key in lookup, "census induced successor absent")
                        cid = vector[lookup[key]]
                        counts[(cid, o, e)] = counts.get((cid, o, e), 0) + 1
        result.append(counts)
    return result


def _validate_payload(payload):
    _native_json(payload)
    _fields(payload, ("parent_color_sizes", "transitions"), "probability-row payload fields")
    _colors(payload["parent_color_sizes"])
    O, E = payload["parent_color_sizes"]
    atoms = payload["transitions"]
    _require(type(atoms) is list and 1 <= len(atoms) <= 64, "profile atom count")
    totals = _zero_table()
    previous = -1
    for atom in atoms:
        _fields(
            atom, ("target_class", "retained_color_sizes", "multiplicity"), "profile atom fields"
        )
        _integer(atom["target_class"], 0, 4446)
        _require(atom["target_class"] > previous, "target IDs must be sorted unique")
        previous = atom["target_class"]
        _colors(atom["retained_color_sizes"])
        o, e = atom["retained_color_sizes"]
        _require(o <= O and e <= E, "child grade exceeds parent")
        _integer(atom["multiplicity"], 1, min(9, _choose(O, o) * _choose(E, e)))
        totals[o][e] += atom["multiplicity"]
    for o in range(4):
        for e in range(4):
            _require(totals[o][e] == _choose(O, o) * _choose(E, e), "rankwise subset normalization")
    _require(sum(map(sum, totals)) == 2 ** (O + E), "total subset normalization")


def _profile_rows(model, features, partition, pushed):
    census = _subset_census(model, partition["state_classes"])
    class_colors = [features[g["members"][0]]["color_sizes"] for g in partition["classes"]]
    result = []
    atoms = 0
    for sid, row in enumerate(pushed):
        parent = features[sid]["color_sizes"]
        transitions = []
        _require(
            {cid for cid, _, _ in census[sid]}
            == {atom["target_class"] for atom in row["transitions"]},
            "inverse/census structural target sets differ",
        )
        for atom in row["transitions"]:
            target = atom["target_class"]
            grades = inverse_basis(atom["coefficients"], parent)
            o, e = class_colors[target]
            multiplicity = grades[o][e]
            _integer(multiplicity, 1, 9)
            wanted = _zero_table()
            wanted[o][e] = multiplicity
            _require(grades == wanted, "inverse profile is nonpositive or has wrong child grade")
            direct = [[census[sid].get((target, i, j), 0) for j in range(4)] for i in range(4)]
            _require(grades == direct, "complete inverse basis differs from separate subset census")
            _require(
                expand_grade_table(grades, parent) == atom["coefficients"],
                "profile-to-power conversion residual",
            )
            transitions.append(
                {
                    "target_class": target,
                    "retained_color_sizes": list(class_colors[target]),
                    "multiplicity": multiplicity,
                }
            )
            atoms += 1
        payload = {"parent_color_sizes": list(parent), "transitions": transitions}
        _validate_payload(payload)
        result.append({"state_id": sid, **payload})
    return result, atoms


def _validated_profile_partition(profiles, partition):
    _native_json(profiles)
    _native_json(partition)
    _fields(partition, ("state_classes", "classes"), "profile partition fields")
    _require(
        type(profiles) is list
        and 1 <= len(profiles) <= 4447
        and type(partition["state_classes"]) is list
        and len(partition["state_classes"]) == len(profiles),
        "profile state universe",
    )
    groups = []
    for sid, cid in enumerate(partition["state_classes"]):
        _integer(cid, 0, len(groups))
        if cid == len(groups):
            groups.append({"class_id": cid, "members": []})
        groups[cid]["members"].append(sid)
    _require(
        type(partition["classes"]) is list and len(partition["classes"]) == len(groups),
        "profile class count",
    )
    for wanted, supplied in zip(groups, partition["classes"], strict=True):
        _require(
            type(supplied) is dict
            and set(supplied) in ({"class_id", "members"}, {"class_id", "key", "members"}),
            "profile class fields",
        )
        _require(
            _canonical({k: supplied[k] for k in ("class_id", "members")}) == _canonical(wanted),
            "canonical profile partition fibers",
        )
    for sid, row in enumerate(profiles):
        _fields(row, ("state_id", "parent_color_sizes", "transitions"), "profile row fields")
        _integer(row["state_id"], sid, sid)
        _validate_payload({k: row[k] for k in ("parent_color_sizes", "transitions")})
    class_colors = [profiles[g["members"][0]]["parent_color_sizes"] for g in groups]
    for group in groups:
        _require(
            all(
                profiles[sid]["parent_color_sizes"] == class_colors[group["class_id"]]
                for sid in group["members"]
            ),
            "profile closure requires common parent degree",
        )
    for row in profiles:
        for atom in row["transitions"]:
            _integer(atom["target_class"], 0, len(groups) - 1)
            _require(
                atom["retained_color_sizes"] == class_colors[atom["target_class"]],
                "profile child H color rank differs",
            )
    return groups


def closure_from_profiles(profiles, partition):
    """Check all members and retain the first rank-consistent multiplicity failure."""
    groups = _validated_profile_partition(profiles, partition)
    witness = None
    comparisons = 0
    for group in groups:
        left = group["members"][0]
        lhs = {a["target_class"]: a for a in profiles[left]["transitions"]}
        for right in group["members"][1:]:
            comparisons += 1
            rhs = {a["target_class"]: a for a in profiles[right]["transitions"]}
            different = [
                target
                for target in sorted(lhs.keys() | rhs.keys())
                if lhs.get(target, {}).get("multiplicity", 0)
                != rhs.get(target, {}).get("multiplicity", 0)
            ]
            if different and witness is None:
                target = different[0]
                first = lhs.get(target, {}).get("multiplicity", 0)
                second = rhs.get(target, {}).get("multiplicity", 0)
                retained = (lhs.get(target) or rhs[target])["retained_color_sizes"]
                O, E = profiles[left]["parent_color_sizes"]
                o, e = retained
                rates = next(
                    (
                        [str(x), str(y)]
                        for x, y in _POINTS[:16]
                        if (first - second) * x**o * (1 - x) ** (O - o) * y**e * (1 - y) ** (E - e)
                    ),
                    None,
                )
                _require(
                    rates is not None, "unequal profile undistinguished on degree-bounded grid"
                )
                witness = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "target_class": target,
                    "retained_color_sizes": list(retained),
                    "left_multiplicity": first,
                    "right_multiplicity": second,
                    "first_distinguishing_rates": rates,
                }
    return {
        "closed": witness is None,
        "classes_checked": len(groups),
        "member_comparisons": comparisons,
        "witness": witness,
    }


def _composition(class_profiles):
    rows = []
    for parent in class_profiles:
        O, E = parent["parent_color_sizes"]
        accum = {}
        for first in parent["transitions"]:
            k, l = first["retained_color_sizes"]
            for final in class_profiles[first["target_class"]]["transitions"]:
                table = accum.setdefault(final["target_class"], _zero_table())
                table[k][l] += first["multiplicity"] * final["multiplicity"]
        direct = {atom["target_class"]: atom for atom in parent["transitions"]}
        _require(set(accum) == set(direct), "one/two-stage structural targets differ")
        nested = 0
        for target, atom in direct.items():
            m, n = atom["retained_color_sizes"]
            for k in range(4):
                for l in range(4):
                    expected = atom["multiplicity"] * _choose(O - m, k - m) * _choose(E - n, l - n)
                    actual = accum[target][k][l]
                    _integer(actual)
                    _require(actual == expected, "nested subset supersets identity")
                    nested += actual
        _require(nested == 3 ** (O + E), "nested pairs must count three statuses per vertex")
        rows.append(
            {
                "class_id": parent["class_id"],
                "final_targets": len(accum),
                "rank_cells": 16 * len(accum),
                "nested_pairs": nested,
                "max_abs_residual": 0,
            }
        )
    return {
        "verified": True,
        "rows": rows,
        "totals": {
            field: sum(row[field] for row in rows)
            for field in ("final_targets", "rank_cells", "nested_pairs", "max_abs_residual")
        },
    }


def _closure(partition, profiles):
    closure = closure_from_profiles(profiles, partition)
    if not closure["closed"]:
        return closure, [], None
    classes = [
        {
            "class_id": group["class_id"],
            "representative_state": group["members"][0],
            "parent_color_sizes": list(profiles[group["members"][0]]["parent_color_sizes"]),
            "transitions": profiles[group["members"][0]]["transitions"],
        }
        for group in partition["classes"]
    ]
    return closure, classes, _composition(classes)


def _rates(rates):
    _require(type(rates) is list and len(rates) == 2, "rates must be a native pair list")
    values = []
    for value in rates:
        _require(
            type(value) is str
            and len(value) <= 3000
            and re.fullmatch(r"(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is not None,
            "unsigned canonical rational syntax",
        )
        rational = _bounded(F(value))
        _require(str(rational) == value and 0 <= rational <= 1, "canonical unit-interval rate")
        values.append(rational)
    return values


@lru_cache(maxsize=32768)
def _basis_probability(O, E, o, e, x, y):
    return x**o * (1 - x) ** (O - o) * y**e * (1 - y) ** (E - e)


def _evaluate_core(payload, rates, values):
    O, E = payload["parent_color_sizes"]
    outcomes = []
    total = F(0)
    for atom in payload["transitions"]:
        o, e = atom["retained_color_sizes"]
        probability = _bounded(atom["multiplicity"] * _basis_probability(O, E, o, e, *values))
        total = _bounded(total + probability)
        outcomes.append({"target_class": atom["target_class"], "probability": str(probability)})
    _require(_bounded(total) == 1, "evaluated profile row does not normalize")
    return {"rates": list(rates), "outcomes": outcomes}


def evaluate_row(payload, rates):
    """Evaluate a detached trusted count row; structural validation is not authentication."""
    _validate_payload(payload)
    values = _rates(rates)
    return _evaluate_core(payload, rates, values)


@lru_cache(maxsize=32768)
def _power_probability(table, x, y):
    return _evaluate(table, x, y)


def _evaluation(profiles, pushed):
    atom_count = 0
    for row, powers in zip(profiles, pushed, strict=True):
        payload = {k: row[k] for k in ("parent_color_sizes", "transitions")}
        _validate_payload(payload)
        atom_count += len(row["transitions"])
        for x, y in _POINTS:
            output = _evaluate_core(payload, [str(x), str(y)], (x, y))
            _require(
                len(output["outcomes"]) == len(powers["transitions"]), "probability target count"
            )
            for actual, power in zip(output["outcomes"], powers["transitions"], strict=True):
                expected = _bounded(
                    _power_probability(tuple(map(tuple, power["coefficients"])), x, y)
                )
                _require(
                    actual == {"target_class": power["target_class"], "probability": str(expected)},
                    "positive count law differs from converted power law",
                )
    return {
        "rate_points": 22,
        "profile_atoms": atom_count,
        "probability_evaluations": 22 * atom_count,
        "normalization_rows": 22 * len(profiles),
        "max_abs_residual": 0,
    }


def analyze(problem):
    """Construct the nonnegative finite deletion contract from explicit raw observations."""
    model = _parse(problem)
    features, fine, _, metadata = _features_and_fine(model)
    partition = _partition(model, features)
    pushed = _push(fine, partition["state_classes"])
    profiles, atoms = _profile_rows(model, features, partition, pushed)
    closure, class_profiles, composition = _closure(partition, profiles)
    quotient = (
        []
        if not closure["closed"]
        else [
            {
                "class_id": row["class_id"],
                "representative_state": row["representative_state"],
                "transitions": pushed[row["representative_state"]]["transitions"],
            }
            for row in class_profiles
        ]
    )
    evaluation = _evaluation(profiles, pushed)
    result = {
        "model_sha256": _digest(model),
        "features": features,
        "partition": partition,
        "profiles": profiles,
        "closure": closure,
        "class_profiles": class_profiles,
        "conversion": {
            "fine_kernel_sha256": metadata["sha256"],
            "pushed_rows_sha256": _digest(pushed),
            "quotient_rows_sha256": _digest(quotient) if closure["closed"] else None,
            "profile_cells": 16 * atoms,
            "power_cells": 16 * atoms,
            "normalization_cells": 16 * len(profiles),
            "max_abs_residual": 0,
        },
        "composition": composition,
        "evaluation": evaluation,
        "counts": {
            "states": len(features),
            "classes": len(partition["classes"]),
            "fine_atoms": metadata["transition_atoms"],
            "profile_atoms": atoms,
            "class_profile_atoms": sum(len(row["transitions"]) for row in class_profiles),
        },
    }
    _native_json(result)
    _require(len(_canonical(result)) <= _MAX_WORK, "analysis working byte cap")
    return result
