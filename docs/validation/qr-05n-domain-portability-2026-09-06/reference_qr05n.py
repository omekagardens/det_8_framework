"""Independent source-count-law reference for QR-05N.

Utility lineage: the separately carried QR-05M reference, with generalized
directed-chain recognition for original IDs that need not be topological.
No executor, artifact, or source file is imported or read at runtime.

D/B come from source-chain indicators and full induced count-law moments,
not ordered chain-pair enumeration. One hundred exact rational-grid kernels
are interpolated once and linearly aggregated into count laws. Features
are computed once per distinct observed order, retaining every source alias.
Motifs use incomparable pairs and common neighbors. Failed closure remains
evidence; this module does not construct a refined replacement partition.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations

F = Fraction
_PARTITIONS = ("pair_graded", "motif_pair")
_NODES = (F(0), F(1, 3), F(2, 3), F(1))
_BASE_NAMES = (
    "ferrers6",
    "standard_example3",
    "chain6",
    "ferrers6_fixed",
    "path6",
    "cycle4_edge",
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


def _canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    )


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


def _feature_vector(state):
    return [value for table in state["mean_graded"] for row in table for value in row] + [
        value for block in state["pair_graded"] for table in block for row in table for value in row
    ]


def _expected_updates(states):
    vectors = [_feature_vector(state) for state in states]
    _require(all(len(vector) == 320 for vector in vectors), "reference feature-vector size differs")
    rows = []
    for state in states:
        expected = [[0] * 16 for _ in range(320)]
        for edge in state["transitions"]:
            child = vectors[edge["target_state"]]
            terms = _nonzero(edge["coefficients"])
            for index, value in enumerate(child):
                if value:
                    for power, coefficient in terms:
                        expected[index][power] += value * coefficient
        parent = vectors[state["state_id"]]
        maximum = max(
            abs(expected[index][power] - (value if power == index % 16 else 0))
            for index, value in enumerate(parent)
            for power in range(16)
        )
        _require(maximum == 0, "reference diagonal expected-feature update failed")
        rows.append(
            {
                "state_id": state["state_id"],
                "mean_features": 64,
                "pair_features": 256,
                "coefficient_cells": 5120,
                "max_abs_residual": maximum,
            }
        )
    return {
        "verified": True,
        "rows": rows,
        "coefficient_cells": sum(row["coefficient_cells"] for row in rows),
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


def _parse(problem):
    _require(
        type(problem) is dict
        and all(type(key) is str for key in problem)
        and set(problem) == {"schema_version", "family"},
        "reference N problem keys are invalid",
    )
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05n-problem-v1",
        "reference N schema is unsupported",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05n_layered_iid",
        "reference N family is unsupported",
    )


def _profile_name(index):
    if index < 6:
        return _BASE_NAMES[index]
    if index < 518:
        return f"layered_oe_{index - 6:03d}"
    return f"layered_eo_{index - 518:03d}"


def _source(index):
    relation = {(0, vertex) for vertex in range(1, 8)}
    relation.update((vertex, 7) for vertex in range(1, 7))
    if index >= 6:
        reverse = index >= 518
        incidence = index - (518 if reverse else 6)
        _require(0 <= incidence < 512, "reference incidence mask exceeds its bound")
        for odd_index in range(3):
            for even_index in range(3):
                if incidence & (1 << (3 * odd_index + even_index)):
                    odd, even = 2 * odd_index + 1, 2 * even_index + 2
                    relation.add((even, odd) if reverse else (odd, even))
    elif index == 2:
        relation.update((first, second) for first in range(1, 7) for second in range(first + 1, 7))
    elif index in (4, 5):
        relation.update(
            ((1, 2), (1, 4), (3, 4), (3, 6), (5, 6))
            if index == 4
            else ((1, 4), (1, 6), (3, 4), (3, 6), (2, 5))
        )
    else:
        relation.update(
            (left + 1, right + 4)
            for left in range(3)
            for right in range(3)
            if (left != right if index == 1 else left <= right)
        )
    _require(all(left != right for left, right in relation), "reference source is not strict")
    _require(
        all(
            (first, third) in relation
            for first, second in relation
            for other, third in relation
            if second == other
        ),
        "reference source is not transitively closed",
    )
    past = [[first for first in range(8) if (first, target) in relation] for target in range(8)]
    fixed = [0, 3, 7] if index == 3 else [0, 7]
    eligible = [vertex for vertex in range(1, 7) if vertex not in fixed]
    return past, fixed, eligible


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


def _induce(kept, original_past):
    positions = {vertex: index for index, vertex in enumerate(kept)}
    return [
        sorted(positions[ancestor] for ancestor in original_past[vertex] if ancestor in positions)
        for vertex in kept
    ]


def _subsets(mask):
    return [retained for retained in range(64) if retained & mask == retained]


def _sizes(mask, eligible):
    odd = sum(bool(mask & (1 << bit)) and vertex % 2 == 1 for bit, vertex in enumerate(eligible))
    return odd, mask.bit_count() - odd


def _domain():
    frames, profiles, states, source_families = [], [], [], []
    frame_ids, state_ids, chain_cache = {}, {}, {}
    for profile_index in range(1030):
        past, fixed, eligible = _source(profile_index)
        frame_key = ("12", tuple(fixed), tuple(eligible))
        if frame_key not in frame_ids:
            frame_id = len(frames)
            frame_ids[frame_key] = frame_id
            frames.append(
                {"frame_id": frame_id, "density": "12", "fixed": fixed, "eligible": eligible}
            )
        frame_id = frame_ids[frame_key]
        chain_key = (tuple(tuple(row) for row in past), tuple(eligible))
        if chain_key not in chain_cache:
            chain_cache[chain_key] = _source_chains(past, eligible)
        source_families.append(chain_cache[chain_key])
        aliases = []
        for mask in range(1 << len(eligible)):
            _require(mask < 64, "reference source observation mask exceeds its bound")
            kept = sorted(
                [*fixed, *(vertex for bit, vertex in enumerate(eligible) if mask & (1 << bit))]
            )
            induced = _induce(kept, past)
            identity = (frame_id, tuple(kept), tuple(tuple(row) for row in induced))
            if identity not in state_ids:
                state_id = len(states)
                state_ids[identity] = state_id
                states.append(
                    {
                        "state_id": state_id,
                        "frame_id": frame_id,
                        "mask": mask,
                        "kept": kept,
                        "past": induced,
                        "aliases": [],
                        "color_sizes": list(_sizes(mask, eligible)),
                        "classes": {},
                        "transitions": [],
                        "summary_laws": {},
                    }
                )
            state_id = state_ids[identity]
            state = states[state_id]
            _require(state["mask"] == mask, "reference deduplicated observations disagree on mask")
            state["aliases"].append({"profile_index": profile_index, "mask": mask})
            aliases.append(state_id)
        profiles.append(
            {
                "profile_index": profile_index,
                "name": _profile_name(profile_index),
                "frame_id": frame_id,
                "past": past,
                "state_ids": aliases,
            }
        )
        if profile_index == 5:
            _require(len(states) == 257, "reference M observed prefix differs")
    _require(
        len(frames) == 2
        and len(profiles) == 1030
        and len(states) == 2470
        and len(states) <= 2579
        and sum(len(state["aliases"]) for state in states) == 65888,
        "reference N source/alias/state inventory differs",
    )

    # Source-chain support indicators are calculated once for each unique state.
    for state in states:
        families = source_families[state["aliases"][0]["profile_index"]]
        frame = frames[state["frame_id"]]
        eligible = frame["eligible"]
        mask = state["mask"]
        means = [[[0] * 4 for _ in range(4)] for _ in range(4)]
        counts = []
        for degree, family in enumerate(families):
            retained = [support for support in family if support & mask == support]
            counts.append(len(retained))
            for support in retained:
                odd, even = _sizes(support, eligible)
                means[degree][odd][even] += 1
        state["chain_counts"] = counts
        state["mean_graded"] = means
        supports = motif_supports(state["kept"], state["past"], eligible)
        state["motif_supports"] = supports
        state["motif_count"] = len(supports)
        _require(0 <= len(supports) <= 9, "reference N motif count exceeds its bound")
        _require(
            max(state["color_sizes"]) <= 3 and sum(state["color_sizes"]) <= 6,
            "reference color population exceeds its bound",
        )
    return frames, profiles, states


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


def _fine_rows(frames, profiles, states, kernels, grids):
    fine_atoms = 0
    for state in states:
        frame = frames[state["frame_id"]]
        representative = profiles[state["aliases"][0]["profile_index"]]
        odd, even = state["color_sizes"]
        row = []
        grid_sum = [F(0)] * 16
        for retained in _subsets(state["mask"]):
            target_id = representative["state_ids"][retained]
            target = states[target_id]
            _require(
                target["frame_id"] == state["frame_id"] and target["mask"] == retained,
                "reference induced successor frame/mask differs",
            )
            for alias in state["aliases"]:
                _require(
                    profiles[alias["profile_index"]]["state_ids"][retained] == target_id,
                    "reference source aliases disagree on an induced successor",
                )
            present = set(target["kept"])
            local = {vertex: index for index, vertex in enumerate(target["kept"])}
            inherited = [
                sorted(local[state["kept"][i]] for i in before if state["kept"][i] in present)
                for vertex, before in zip(state["kept"], state["past"], strict=True)
                if vertex in present
            ]
            _require(inherited == target["past"], "reference fine successor is not induced")
            kept_odd, kept_even = target["color_sizes"]
            key = (odd, even, kept_odd, kept_even)
            row.append({"target_state": target_id, "coefficients": kernels[key]})
            for node, probability in enumerate(grids[key]):
                _require(probability >= 0, "reference fine grid has a negative probability")
                grid_sum[node] += probability
                if node in (0, 3, 12, 15) and probability:
                    expected = sorted(
                        vertex
                        for vertex in state["kept"]
                        if vertex in frame["fixed"]
                        or ((_NODES[node // 4] if vertex % 2 else _NODES[node % 4]) == 1)
                    )
                    _require(target["kept"] == expected, "reference deterministic corner differs")
        row.sort(key=lambda atom: atom["target_state"])
        _check_row(row, "target_state")
        _require(all(total == 1 for total in grid_sum), "reference fine grid row is not normalized")
        state["transitions"] = row
        fine_atoms += len(row)
    _require(
        fine_atoms == 99180 and fine_atoms <= 100393,
        "reference fine induced-subset inventory differs",
    )


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


def _partitions(frames, states):
    partitions = {name: [] for name in _PARTITIONS}
    registries = {name: {} for name in _PARTITIONS}
    for state in states:
        frame = _frame_key(frames[state["frame_id"]])
        for name in _PARTITIONS:
            key = [frame, state["pair_graded"]]
            if name == "motif_pair":
                key.append(state["motif_count"])
            identity = _canonical(key)
            if identity not in registries[name]:
                class_id = len(partitions[name])
                registries[name][identity] = class_id
                partitions[name].append({"class_id": class_id, "key": key, "members": []})
            class_id = registries[name][identity]
            state["classes"][name] = class_id
            partitions[name][class_id]["members"].append(state["state_id"])
    return partitions


def _pushforwards(states):
    for state in states:
        for name in _PARTITIONS:
            atoms = {}
            for edge in state["transitions"]:
                target = states[edge["target_state"]]["classes"][name]
                table = atoms.setdefault(target, _zero_table())
                _add_table(table, edge["coefficients"])
            row = [
                {"target_class": target, "coefficients": atoms[target]} for target in sorted(atoms)
            ]
            _check_row(row, "target_class")
            state["summary_laws"][name] = row


def _closure(states, partitions):
    results = {}
    for name in _PARTITIONS:
        maps = [
            {edge["target_class"]: edge["coefficients"] for edge in state["summary_laws"][name]}
            for state in states
        ]
        collision = None
        for group in partitions[name]:
            left = group["members"][0]
            for right in group["members"][1:]:
                for target in sorted(set(maps[left]) | set(maps[right])):
                    first = maps[left].get(target, _zero_table())
                    second = maps[right].get(target, _zero_table())
                    if first != second:
                        collision = {
                            "class_id": group["class_id"],
                            "left_state": left,
                            "right_state": right,
                            "target_class": target,
                            "left_coefficients": first,
                            "right_coefficients": second,
                        }
                        break
                if collision is not None:
                    break
            if collision is not None:
                break
        if collision is not None:
            results[name] = {
                "closed": False,
                "first_collision": collision,
                "quotient_rows": [],
                "semigroup": None,
            }
            continue
        quotient = [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                "transitions": states[group["members"][0]]["summary_laws"][name],
            }
            for group in partitions[name]
        ]
        results[name] = {
            "closed": True,
            "first_collision": None,
            "quotient_rows": quotient,
            "semigroup": _semigroup(quotient),
        }
    return results


def _motif_expectation(states):
    rows = []
    for state in states:
        actual = _zero_table()
        for edge in state["transitions"]:
            _add_table(actual, edge["coefficients"], states[edge["target_state"]]["motif_count"])
        expected = _zero_table()
        expected[2][2] = state["motif_count"]
        maximum = max(abs(actual[i][j] - expected[i][j]) for i in range(4) for j in range(4))
        _require(maximum == 0, "reference N motif survival identity failed")
        rows.append(
            {
                "state_id": state["state_id"],
                "coefficients": actual,
                "expected_coefficients": expected,
                "max_abs_residual": maximum,
            }
        )
    return {"verified": True, "rows": rows, "coefficient_cells": 16 * len(states)}


def analyze(problem):
    """Return only the fixed larger-family evidence, retaining any closure failure."""
    _parse(problem)
    frames, profiles, states = _domain()
    kernels, grids = _kernel_cache(_inverse_vandermonde())
    _fine_rows(frames, profiles, states, kernels, grids)
    _count_law_features(states)
    partitions = _partitions(frames, states)
    _pushforwards(states)
    closure = _closure(states, partitions)
    expected = _expected_updates(states)
    motif_expected = _motif_expectation(states)
    fine_atoms = sum(len(state["transitions"]) for state in states)
    pushed_atoms = sum(len(row) for state in states for row in state["summary_laws"].values())
    closed = [entry for entry in closure.values() if entry["closed"]]
    result = {
        "frames": frames,
        "profiles": profiles,
        "states": states,
        "partitions": partitions,
        "closure": closure,
        "expected_updates": expected,
        "motif_expected_update": motif_expected,
        "counts": {
            "frames": len(frames),
            "profiles": len(profiles),
            "aliases": sum(len(state["aliases"]) for state in states),
            "states": len(states),
            "partitions": len(_PARTITIONS),
            "fine_transition_atoms": fine_atoms,
            "summary_transition_atoms": pushed_atoms,
            "transition_coefficient_cells": 16 * (fine_atoms + pushed_atoms),
            "mean_feature_cells": 64 * len(states),
            "pair_feature_cells": 256 * len(states),
            "motif_support_occurrences": sum(state["motif_count"] for state in states),
            "motif_positive_states": sum(state["motif_count"] > 0 for state in states),
            "max_motif_count": max(state["motif_count"] for state in states),
            "expected_update_coefficient_cells": expected["coefficient_cells"],
            "motif_expected_update_coefficient_cells": motif_expected["coefficient_cells"],
            "closed_partitions": len(closed),
            "quotient_transition_atoms": sum(
                len(row["transitions"]) for entry in closed for row in entry["quotient_rows"]
            ),
            "semigroup_intermediate_paths": sum(
                entry["semigroup"]["totals"]["intermediate_paths"] for entry in closed
            ),
            "semigroup_coefficient_cells": sum(
                entry["semigroup"]["totals"]["coefficient_cells"] for entry in closed
            ),
        },
    }
    _native_json(result)
    _require(
        len(_canonical(result).encode("utf-8")) <= 64 * 1024 * 1024,
        "reference N analysis exceeds the capture byte cap",
    )
    return result
