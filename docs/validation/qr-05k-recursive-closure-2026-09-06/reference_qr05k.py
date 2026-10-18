"""Independent source-law/interpolation oracle for QR-05K.

Supplied source-chain indicators and locally reconstructed count laws give
the summaries.  Individual successor probabilities are independently evaluated
on a rational tensor grid and interpolated; no transition binomial expansion
or observed chain-pair enumeration is used.  Quotients and four-variable
composition checks are constructed afresh on the deduplicated state domain.

Only analyze(problem) is advertised.  No primary, earlier executor, artifact,
or filesystem input is read.  Closure concerns this finite observation family
and fresh independent thinning, not physical dynamics or universal sufficiency.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, pairwise, permutations

F = Fraction
_PROFILES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed")
_PARTITIONS = ("mean_graded", "pair_graded", "color_order", "full_record")
_NODES = (F(0), F(1, 3), F(2, 3), F(1))


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


def _parse(problem):
    _require(
        type(problem) is dict
        and all(type(key) is str for key in problem)
        and set(problem) == {"schema_version", "family"},
        "reference problem keys are invalid",
    )
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05k-problem-v1",
        "reference schema is unsupported",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05j_recursive_iid",
        "reference family is unsupported",
    )


def _population(profile):
    past = [[]]
    for node in range(6):
        if profile == "chain6":
            row = list(range(node + 1))
        elif node < 3:
            row = [0]
        else:
            right = node - 3
            row = [
                0,
                *(
                    left + 1
                    for left in range(3)
                    if (left != right if profile == "standard_example3" else left <= right)
                ),
            ]
        past.append(row)
    past.append(list(range(7)))
    fixed = [0, 3, 7] if profile == "ferrers6_fixed" else [0, 7]
    eligible = [node for node in range(1, 7) if node not in fixed]
    _require(
        all(
            row == sorted(set(row)) and all(0 <= node < target for node in row)
            for target, row in enumerate(past)
        ),
        "reference population is not naturally labeled",
    )
    _require(
        all(set(past[node]).issubset(row) for row in past for node in row),
        "reference population is not transitively closed",
    )
    return past, fixed, eligible


def _source_chains(past, eligible):
    positions = {node: bit for bit, node in enumerate(eligible)}
    families = []
    for degree in range(4):
        chains = []
        for vertices in combinations(range(1, 7), degree):
            if all(first in past[second] for first, second in pairwise((0, *vertices, 7))):
                support = sum(1 << positions[node] for node in vertices if node in positions)
                odd = sum(node % 2 == 1 for node in vertices if node in positions)
                even = sum(node % 2 == 0 for node in vertices if node in positions)
                chains.append((support, odd, even))
        families.append(chains)
    return families


def _observations(past, fixed, eligible, families):
    observations = []
    gradings = []
    for mask in range(1 << len(eligible)):
        kept = sorted([*fixed, *(node for bit, node in enumerate(eligible) if mask & (1 << bit))])
        positions = {node: index for index, node in enumerate(kept)}
        observed = [
            [positions[ancestor] for ancestor in past[node] if ancestor in positions]
            for node in kept
        ]
        colors = [[[0] * 4 for _ in range(4)] for _ in range(4)]
        graded = [[0] * 4 for _ in range(4)]
        for degree, chains in enumerate(families):
            for support, odd, even in chains:
                if mask & support == support:
                    colors[degree][odd][even] += 1
                    graded[degree][support.bit_count()] += 1
        for degree in range(4):
            for size in range(4):
                _require(
                    graded[degree][size]
                    == sum(colors[degree][odd][size - odd] for odd in range(size + 1)),
                    "reference color/support grading identity failed",
                )
        observations.append(
            {
                "mask": mask,
                "kept": kept,
                "past": observed,
                "chain_counts": [sum(row) for row in graded],
            }
        )
        gradings.append((graded, colors))
    return observations, gradings


def _color_code(kept, past, fixed):
    """Minimize a fixed-marked colored relation independently of source names."""
    others = [vertex for vertex in kept if vertex not in fixed]
    edges = [(kept[ancestor], kept[target]) for target, row in enumerate(past) for ancestor in row]
    size, minimum = len(kept), None
    for perm in permutations(others):
        positions = {vertex: index for index, vertex in enumerate((*fixed, *perm))}
        relation = sum(1 << (positions[left] * size + positions[right]) for left, right in edges)
        color = sum(1 << positions[vertex] for vertex in others if vertex % 2)
        candidate = relation, color
        minimum = candidate if minimum is None else min(minimum, candidate)
    _require(minimum is not None, "reference canonical order has no arrangement")
    return [size, *minimum]


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


def _subset_probability(mask, retained, eligible, x, y):
    probability = F(1)
    for bit, vertex in enumerate(eligible):
        if mask & (1 << bit):
            rate = x if vertex % 2 else y
            probability *= rate if retained & (1 << bit) else 1 - rate
    return _bounded(probability)


def _evaluate(table, x, y):
    return _bounded(
        sum(
            (F(table[a][b]) * x**a * y**b for a in range(4) for b in range(4)),
            F(0),
        )
    )


def _polynomial_laws(mask, eligible, observations, colors, inverse):
    """Recover atom laws solely from source-indicator observations and grid PMFs."""
    odd_size = sum(
        bool(mask & (1 << bit)) and vertex % 2 == 1 for bit, vertex in enumerate(eligible)
    )
    even_size = mask.bit_count() - odd_size
    _require(
        0 <= odd_size <= 3 and 0 <= even_size <= 3,
        "reference color population exceeds interpolation degree",
    )
    atoms = sorted({tuple(observation["chain_counts"]) for observation in observations})
    grid = {atom: [[F(0) for _ in range(4)] for _ in range(4)] for atom in atoms}
    for i, x in enumerate(_NODES):
        for j, y in enumerate(_NODES):
            normalization = F(0)
            for observation in observations:
                probability = _subset_probability(mask, observation["mask"], eligible, x, y)
                grid[tuple(observation["chain_counts"])][i][j] += probability
                normalization += probability
            _require(normalization == 1, "reference interpolation-node law is not normalized")
    polynomials = [
        {"counts": list(atom), "coefficients": _tensor_interpolate(grid[atom], inverse)}
        for atom in atoms
    ]
    for polynomial in polynomials:
        table = polynomial["coefficients"]
        _require(
            any(value != 0 for row in table for value in row),
            "reference attainable atom has an identically zero polynomial",
        )
        _require(
            all(
                table[a][b] == 0
                for a in range(4)
                for b in range(4)
                if a > odd_size or b > even_size
            ),
            "reference atom exceeds its observed color degree",
        )
        for i, x in enumerate(_NODES):
            for j, y in enumerate(_NODES):
                _require(
                    _evaluate(table, x, y) == grid[tuple(polynomial["counts"])][i][j],
                    "reference polynomial does not reproduce its interpolation grid",
                )
    _require(
        all(
            sum(polynomial["coefficients"][a][b] for polynomial in polynomials)
            == int(a == 0 and b == 0)
            for a in range(4)
            for b in range(4)
        ),
        "reference atom polynomials do not sum coefficientwise to one",
    )
    mean_polynomials = [
        [
            [
                sum(
                    polynomial["counts"][degree] * polynomial["coefficients"][a][b]
                    for polynomial in polynomials
                )
                for b in range(4)
            ]
            for a in range(4)
        ]
        for degree in range(4)
    ]
    _require(mean_polynomials == colors, "reference mean coefficients differ from chain grading")
    # These points do not enter the interpolation construction.
    for x, y in (
        (F(2, 5), F(3, 7)),
        (F(1, 5), F(4, 5)),
        (F(1, 2), F(1, 3)),
        (F(0), F(2, 5)),
        (F(3, 7), F(1)),
    ):
        expected = {atom: F(0) for atom in atoms}
        for observation in observations:
            expected[tuple(observation["chain_counts"])] += _subset_probability(
                mask, observation["mask"], eligible, x, y
            )
        for polynomial in polynomials:
            value = _evaluate(polynomial["coefficients"], x, y)
            _require(
                value == expected[tuple(polynomial["counts"])] and value >= 0,
                "reference held-out direct law disagrees with interpolation",
            )
    return [odd_size, even_size], polynomials, mean_polynomials


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


def _state_domain(inverse):
    frames, profiles, states = [], [], []
    frame_ids, state_ids = {}, {}
    for profile_index, name in enumerate(_PROFILES):
        past, fixed, eligible = _population(name)
        frame = ["12", fixed, eligible]
        frame_identity = _canonical(frame)
        if frame_identity not in frame_ids:
            frame_id = len(frames)
            frame_ids[frame_identity] = frame_id
            frames.append(
                {"frame_id": frame_id, "density": "12", "fixed": fixed, "eligible": eligible}
            )
        frame_id = frame_ids[frame_identity]
        chains = _source_chains(past, eligible)
        observations, gradings = _observations(past, fixed, eligible, chains)
        aliases = []
        for mask, observation in enumerate(observations):
            identity = _canonical([frame, observation["kept"], observation["past"]])
            alias = {"profile_index": profile_index, "mask": mask}
            if identity in state_ids:
                state_id = state_ids[identity]
                state = states[state_id]
                _require(
                    state["mean_graded"] == gradings[mask][1]
                    and state["chain_counts"] == observation["chain_counts"]
                    and state["frame_id"] == frame_id
                    and state["mask"] == mask,
                    "reference duplicate source issues inconsistent observed data",
                )
                state["aliases"].append(alias)
            else:
                state_id = len(states)
                state_ids[identity] = state_id
                successors = [row for row in observations if row["mask"] & mask == row["mask"]]
                sizes, law, means = _polynomial_laws(
                    mask, eligible, successors, gradings[mask][1], inverse
                )
                states.append(
                    {
                        "state_id": state_id,
                        "frame_id": frame_id,
                        "mask": mask,
                        "kept": observation["kept"],
                        "past": observation["past"],
                        "aliases": [alias],
                        "color_sizes": sizes,
                        "chain_counts": observation["chain_counts"],
                        "mean_graded": means,
                        "pair_graded": _raw_summary(law, means, observation["chain_counts"], sizes),
                        "color_order": _color_code(observation["kept"], observation["past"], fixed),
                        "classes": {},
                        "transitions": [],
                        "summary_laws": {},
                    }
                )
            aliases.append(state_id)
        profiles.append(
            {
                "profile_index": profile_index,
                "name": name,
                "frame_id": frame_id,
                "past": past,
                "state_ids": aliases,
            }
        )
    _require(
        len(frames) == 2
        and len(states) == 188
        and sum(len(profile["state_ids"]) for profile in profiles) == 224,
        "reference observed-state domain differs from the frozen universe",
    )
    return frames, profiles, states


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


def _fine_transitions(frames, profiles, states, inverse):
    coefficient_cache = {}
    for state in states:
        eligible = frames[state["frame_id"]]["eligible"]
        profile = profiles[state["aliases"][0]["profile_index"]]
        mask = state["mask"]
        children = [u for u in range(1 << len(eligible)) if u & mask == u]
        transitions = []
        for retained in children:
            target_id = profile["state_ids"][retained]
            target = states[target_id]
            for alias in state["aliases"]:
                _require(
                    profiles[alias["profile_index"]]["state_ids"][retained] == target_id,
                    "reference aliases disagree on an induced successor",
                )
            _require(
                target["frame_id"] == state["frame_id"],
                "reference transition changes its public frame",
            )
            positions = {vertex: index for index, vertex in enumerate(target["kept"])}
            current_positions = {vertex: index for index, vertex in enumerate(state["kept"])}
            induced = [
                [
                    positions[state["kept"][ancestor]]
                    for ancestor in state["past"][current_positions[vertex]]
                    if state["kept"][ancestor] in positions
                ]
                for vertex in target["kept"]
            ]
            _require(induced == target["past"], "reference successor relation is not induced")
            cache_key = (tuple(eligible), mask, retained)
            if cache_key not in coefficient_cache:
                samples = [
                    [_subset_probability(mask, retained, eligible, x, y) for y in _NODES]
                    for x in _NODES
                ]
                table = _tensor_interpolate(samples, inverse)
                for i, x in enumerate(_NODES):
                    for j, y in enumerate(_NODES):
                        _require(
                            _evaluate(table, x, y) == samples[i][j],
                            "reference fine interpolation does not reproduce its grid",
                        )
                _require(
                    all(
                        table[i][j] == 0
                        for i in range(4)
                        for j in range(4)
                        if i > state["color_sizes"][0] or j > state["color_sizes"][1]
                    ),
                    "reference fine transition exceeds its observed color degree",
                )
                coefficient_cache[cache_key] = table
            transitions.append(
                {"target_state": target_id, "coefficients": coefficient_cache[cache_key]}
            )
        state["transitions"] = sorted(transitions, key=lambda edge: edge["target_state"])
        _check_row(state["transitions"], "target_state")


def _partition_key(name, frame, state):
    if name == "full_record":
        return [frame, state["kept"], state["past"]]
    return [frame, state[name]]


def _partitions(frames, states):
    partitions = {name: [] for name in _PARTITIONS}
    identities = {name: {} for name in _PARTITIONS}
    for state in states:
        frame = _frame_key(frames[state["frame_id"]])
        for name in _PARTITIONS:
            key = _partition_key(name, frame, state)
            identity = _canonical(key)
            if identity not in identities[name]:
                class_id = len(partitions[name])
                identities[name][identity] = class_id
                partitions[name].append({"class_id": class_id, "key": key, "members": []})
            class_id = identities[name][identity]
            partitions[name][class_id]["members"].append(state["state_id"])
            state["classes"][name] = class_id
    refinement = []
    for fine in _PARTITIONS:
        row = []
        for coarse in _PARTITIONS:
            mapping, valid = {}, True
            for state in states:
                left, right = state["classes"][fine], state["classes"][coarse]
                if left in mapping and mapping[left] != right:
                    valid = False
                    break
                mapping[left] = right
            row.append(valid)
        refinement.append(row)
    return partitions, refinement


def _pushforwards(states):
    for state in states:
        for name in _PARTITIONS:
            masses = {}
            for edge in state["transitions"]:
                target = states[edge["target_state"]]["classes"][name]
                if target not in masses:
                    masses[target] = _zero_table()
                _add_table(masses[target], edge["coefficients"])
            row = [
                {"target_class": target, "coefficients": masses[target]}
                for target in sorted(masses)
            ]
            _check_row(row, "target_class")
            state["summary_laws"][name] = row


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


def _closure(states, partitions):
    result = {}
    for name in _PARTITIONS:
        collision = None
        for state in states:
            class_id = state["classes"][name]
            representative = partitions[name][class_id]["members"][0]
            left = {
                edge["target_class"]: edge["coefficients"]
                for edge in states[representative]["summary_laws"][name]
            }
            right = {
                edge["target_class"]: edge["coefficients"] for edge in state["summary_laws"][name]
            }
            targets = sorted(set(left) | set(right))
            different = next(
                (
                    target
                    for target in targets
                    if left.get(target, _zero_table()) != right.get(target, _zero_table())
                ),
                None,
            )
            if different is not None:
                collision = {
                    "class_id": class_id,
                    "left_state": representative,
                    "right_state": state["state_id"],
                    "target_class": different,
                    "left_coefficients": left.get(different, _zero_table()),
                    "right_coefficients": right.get(different, _zero_table()),
                }
                break
        if collision is not None:
            result[name] = {
                "closed": False,
                "first_collision": collision,
                "quotient_rows": None,
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
        result[name] = {
            "closed": True,
            "first_collision": None,
            "quotient_rows": quotient,
            "semigroup": _semigroup(quotient),
        }
    _require(
        result["color_order"]["closed"] and result["full_record"]["closed"],
        "reference declared positive closure control failed",
    )
    _require(
        not result["mean_graded"]["closed"],
        "reference declared mean-only closure counterexample disappeared",
    )
    return result


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


def analyze(problem):
    """Return only the frozen finite recursive-closure analysis."""
    _parse(problem)
    inverse = _inverse_vandermonde()
    frames, profiles, states = _state_domain(inverse)
    _fine_transitions(frames, profiles, states, inverse)
    partitions, refinement = _partitions(frames, states)
    _pushforwards(states)
    closure = _closure(states, partitions)
    expected = _expected_updates(states)
    fine_atoms = sum(len(state["transitions"]) for state in states)
    summary_atoms = sum(len(row) for state in states for row in state["summary_laws"].values())
    closed = [entry for entry in closure.values() if entry["closed"]]
    result = {
        "frames": frames,
        "profiles": profiles,
        "states": states,
        "partitions": partitions,
        "partition_refinement": refinement,
        "closure": closure,
        "expected_updates": expected,
        "counts": {
            "frames": len(frames),
            "profiles": len(profiles),
            "aliases": sum(len(state["aliases"]) for state in states),
            "states": len(states),
            "partitions": len(_PARTITIONS),
            "fine_transition_atoms": fine_atoms,
            "summary_transition_atoms": summary_atoms,
            "transition_coefficient_cells": 16 * (fine_atoms + summary_atoms),
            "mean_feature_cells": len(states) * 64,
            "pair_feature_cells": len(states) * 256,
            "expected_update_coefficient_cells": expected["coefficient_cells"],
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
    return result
