"""Independent exact analytic-portability oracle for QR-05I.

Source-chain-set indicators give the observations.  Complete joint count
laws are evaluated at sixteen rational nodes and reconstructed by exact
tensor interpolation, without binomial coefficient expansion.  No primary,
earlier executor, or artifact is imported or read at runtime.

Only analyze(problem) is advertised.  This is a bounded classical family
of supplied observation laws, not physics or an arbitrary-law certificate.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, pairwise, permutations
from math import comb

F = Fraction
_CASES = (
    ("ferrers6", "independent"),
    ("ferrers6", "parity_adaptive"),
    ("ferrers6", "common_coin"),
    ("ferrers6", "parity_hole"),
    ("ferrers6", "first_pair"),
    ("standard_example3", "independent"),
    ("chain6", "parity_adaptive"),
    ("chain6", "parity_hole"),
    ("chain6", "first_pair"),
    ("ferrers6_fixed", "independent"),
)
_CANDIDATES = (
    "final_only",
    "policy_token",
    "tagged_policy",
    "counts_policy",
    "graded_policy",
    "tagged_graded",
    "unmarked_order",
    "marked_order",
    "full_record",
    "color_graded",
    "block_order",
    "color_order",
)
_TARGETS = ("analytic_means", "analytic_counts")
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


def _wire(value):
    return str(_bounded(value))


def _vector(values):
    return [_wire(value) for value in values]


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
        and problem["schema_version"] == "det8-qr05i-problem-v1",
        "reference schema is unsupported",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05h_two_color",
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


def _current_law(design, size):
    number = 1 << size
    first = (
        [F(1, comb(size, 2)) if mask.bit_count() == 2 else F(0) for mask in range(number)]
        if design == "first_pair"
        else [F(1, number)] * number
    )
    conditional, tokens = [], []
    for mask in range(number):
        token = (
            F(1, 3)
            if design == "parity_adaptive" and mask.bit_count() % 2 == 0
            else F(2, 3)
            if design == "parity_adaptive"
            else F(int(mask.bit_count() % 2 == 0))
            if design == "parity_hole"
            else F(1, 2)
        )
        tokens.append(token)
        row = []
        for retained in range(number):
            if retained & mask != retained:
                continue
            if design == "common_coin":
                probability = F(1) if mask == 0 else F(1, 2) if retained in (0, mask) else F(0)
            else:
                probability = token ** retained.bit_count() * (1 - token) ** (
                    mask.bit_count() - retained.bit_count()
                )
            row.append((retained, _bounded(probability)))
        _require(
            sum((probability for _, probability in row), F(0)) == 1,
            "reference current conditional law is not normalized",
        )
        conditional.append(row)
    pi1 = [
        sum(
            (probability for mask, probability in enumerate(first) if mask & support == support),
            F(0),
        )
        for support in range(number)
    ]
    _require(sum(first, F(0)) == pi1[0] == 1, "reference first law is not normalized")
    return first, conditional, tokens, pi1


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


def _canon(kept, past, anchors, decorated):
    """Canonicalize an observed relation with precisely the declared anchors."""
    edges = {(kept[source], kept[target]) for target, row in enumerate(past) for source in row}
    others = [node for node in kept if node not in anchors]
    n = len(kept)
    minimum_relation, minimum_block, minimum_color = None, None, None
    for perm in permutations(others):
        arranged = (*anchors, *perm)
        positions = {node: index for index, node in enumerate(arranged)}
        relation = sum(1 << (positions[source] * n + positions[target]) for source, target in edges)
        minimum_relation = relation if minimum_relation is None else min(minimum_relation, relation)
        if decorated:
            color = sum(1 << positions[node] for node in perm if node % 2 == 1)
            block = sum(
                1 << (positions[first] * n + positions[second])
                for first, second in combinations(perm, 2)
                if first % 2 == second % 2
            )
            colored_pair, blocked_pair = (relation, color), (relation, block)
            minimum_color = (
                colored_pair if minimum_color is None else min(minimum_color, colored_pair)
            )
            minimum_block = (
                blocked_pair if minimum_block is None else min(minimum_block, blocked_pair)
            )
    _require(
        type(minimum_relation) is int and minimum_relation.bit_length() <= 4096,
        "reference canonical relation is invalid",
    )
    plain = [n, minimum_relation]
    if not decorated:
        return plain
    _require(
        max(minimum_block).bit_length() <= 4096 and max(minimum_color).bit_length() <= 4096,
        "reference canonical decoration exceeds the component bound",
    )
    return plain, [n, *minimum_block], [n, *minimum_color]


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


def _population_states(past, fixed, eligible, inverse):
    families = _source_chains(past, eligible)
    all_observations, gradings = _observations(past, fixed, eligible, families)
    states = []
    for mask, observation in enumerate(all_observations):
        observations = [row for row in all_observations if row["mask"] & mask == row["mask"]]
        graded, colors = gradings[mask]
        marked, block, color = _canon(observation["kept"], observation["past"], fixed, True)
        unmarked = (
            marked
            if fixed == [0, 7]
            else _canon(observation["kept"], observation["past"], [0, 7], False)
        )
        sizes, polynomials, means = _polynomial_laws(mask, eligible, observations, colors, inverse)
        states.append(
            {
                "mask": mask,
                "kept": observation["kept"],
                "past": observation["past"],
                "tagged_present": bool(mask & 1),
                "chain_counts": observation["chain_counts"],
                "graded_counts": graded,
                "unmarked_order": unmarked,
                "marked_order": marked,
                "color_graded": colors,
                "block_order": block,
                "color_order": color,
                "observations": observations,
                "color_sizes": sizes,
                "count_polynomials": polynomials,
                "mean_polynomials": means,
            }
        )
    return states, all_observations


def _candidate_keys(base, state):
    token = state["policy_token"]
    return {
        "final_only": base,
        "policy_token": [*base, token],
        "tagged_policy": [*base, token, state["tagged_present"]],
        "counts_policy": [*base, token, state["chain_counts"]],
        "graded_policy": [*base, token, state["graded_counts"]],
        "tagged_graded": [*base, token, state["graded_counts"], state["tagged_present"]],
        "unmarked_order": [*base, token, state["unmarked_order"]],
        "marked_order": [*base, token, state["marked_order"]],
        "full_record": [*base, state["kept"], state["past"]],
        "color_graded": [*base, token, state["color_graded"]],
        "block_order": [*base, token, state["block_order"]],
        "color_order": [*base, token, state["color_order"]],
    }


def _target_signatures(state):
    return state["mean_polynomials"], state["count_polynomials"]


def _register(groups, indices, masses, identity, description, history_id, joint):
    if identity not in indices:
        class_id = len(groups)
        indices[identity] = class_id
        groups.append({"class_id": class_id, "members": [], "joint_mass": "0", **description})
        masses.append(F(0))
    class_id = indices[identity]
    groups[class_id]["members"].append(history_id)
    masses[class_id] += joint
    return class_id


def _assess(histories, candidate_partitions):
    assessments = {}
    for candidate in _CANDIDATES:
        targets = {}
        for target in _TARGETS:
            first, common, collision = {}, set(), None
            for history in histories:
                candidate_id = history["candidate_classes"][candidate]
                if candidate_id is None:
                    continue
                target_id = history["target_classes"][target]
                common.add((candidate_id, target_id))
                if candidate_id not in first:
                    first[candidate_id] = (history["history_id"], target_id)
                elif collision is None and first[candidate_id][1] != target_id:
                    collision = {
                        "left_history": first[candidate_id][0],
                        "right_history": history["history_id"],
                    }
            sufficient = collision is None
            _require(
                sufficient == (len(common) == len(candidate_partitions[candidate])),
                "reference fiber constancy/common-refinement identity failed",
            )
            targets[target] = {
                "sufficient": sufficient,
                "first_collision": collision,
                "common_refinement_classes": len(common),
            }
        assessments[candidate] = targets
    return assessments


def _refinement(histories, names, field):
    matrix = []
    for fine in names:
        row = []
        for coarse in names:
            mapping, valid = {}, True
            for history in histories:
                left = history[field][fine]
                if left is None:
                    continue
                right = history[field][coarse]
                if left not in mapping:
                    mapping[left] = right
                elif mapping[left] != right:
                    valid = False
                    break
            row.append(valid)
        matrix.append(row)
    return matrix


def analyze(problem):
    """Return the bounded analytic law family and same-domain pooled partitions."""
    _parse(problem)
    inverse = _inverse_vandermonde()
    cases, case_laws, population_cache = [], [], {}
    for case_index, (profile, design) in enumerate(_CASES):
        past, fixed, eligible = _population(profile)
        # Cache identical supplied order/frame computations, not hidden profile labels.
        population_key = (tuple(tuple(row) for row in past), tuple(fixed), tuple(eligible))
        if population_key not in population_cache:
            population_cache[population_key] = _population_states(past, fixed, eligible, inverse)
        templates, observations = population_cache[population_key]
        first, conditional, tokens, pi1 = _current_law(design, len(eligible))
        states = [
            {**template, "probability": _wire(first[mask]), "policy_token": _wire(tokens[mask])}
            for mask, template in enumerate(templates)
        ]
        cases.append(
            {
                "case_index": case_index,
                "profile": profile,
                "design": design,
                "density": "12",
                "past": past,
                "fixed": fixed,
                "eligible": eligible,
                "stage1_inclusions": _vector(pi1),
                "states": states,
            }
        )
        case_laws.append((first, conditional, observations))
    candidate_partitions = {name: [] for name in _CANDIDATES}
    target_partitions = {name: [] for name in _TARGETS}
    candidate_ids, candidate_masses = (
        {name: {} for name in _CANDIDATES},
        {name: [] for name in _CANDIDATES},
    )
    target_ids, target_masses = {name: {} for name in _TARGETS}, {name: [] for name in _TARGETS}
    histories = []
    for case, (first, conditional, observations) in zip(cases, case_laws):
        context = [case["design"], case["density"], case["fixed"], case["eligible"]]
        for intermediate, conditional_row in enumerate(conditional):
            state = case["states"][intermediate]
            signatures = _target_signatures(state)
            for retained, probability in conditional_row:
                history_id = len(histories)
                joint = _bounded(first[intermediate] * probability)
                candidate_classes = {name: None for name in _CANDIDATES}
                target_classes = {name: None for name in _TARGETS}
                if joint > 0:
                    base = [context, observations[retained]["kept"], observations[retained]["past"]]
                    keys = _candidate_keys(base, state)
                    for name in _CANDIDATES:
                        candidate_classes[name] = _register(
                            candidate_partitions[name],
                            candidate_ids[name],
                            candidate_masses[name],
                            _canonical(keys[name]),
                            {"key": keys[name]},
                            history_id,
                            joint,
                        )
                    for name, signature in zip(_TARGETS, signatures):
                        target_classes[name] = _register(
                            target_partitions[name],
                            target_ids[name],
                            target_masses[name],
                            _canonical([base, signature]),
                            {"base": base, "signature": signature},
                            history_id,
                            joint,
                        )
                histories.append(
                    {
                        "history_id": history_id,
                        "case_index": case["case_index"],
                        "stage1_mask": intermediate,
                        "final_mask": retained,
                        "conditional_probability": _wire(probability),
                        "joint_probability": _wire(joint),
                        "candidate_classes": candidate_classes,
                        "target_classes": target_classes,
                    }
                )
    for partitions, masses in (
        (candidate_partitions, candidate_masses),
        (target_partitions, target_masses),
    ):
        for name, groups in partitions.items():
            _require(sum(masses[name], F(0)) == 10, "reference pooled masses do not sum to ten")
            for group, mass in zip(groups, masses[name]):
                group["joint_mass"] = _wire(mass)
    assessments = _assess(histories, candidate_partitions)
    candidate_refinement = _refinement(histories, _CANDIDATES, "candidate_classes")
    target_refinement = _refinement(histories, _TARGETS, "target_classes")
    _require(target_refinement[1][0], "reference complete laws fail to refine their means")
    for target in _TARGETS:
        _require(
            assessments["full_record"][target]["sufficient"]
            and assessments["color_order"][target]["sufficient"],
            "reference complete-record or color-order positive control failed",
        )
    _require(
        assessments["color_graded"]["analytic_means"]["sufficient"],
        "reference color grading fails to determine the mean polynomials",
    )
    forward, backward = {}, {}
    for history in histories:
        candidate = history["candidate_classes"]["color_graded"]
        if candidate is None:
            continue
        target = history["target_classes"]["analytic_means"]
        _require(
            candidate not in forward or forward[candidate] == target,
            "reference color-graded class splits across analytic means",
        )
        _require(
            target not in backward or backward[target] == candidate,
            "reference mean class splits across color-graded classes",
        )
        forward[candidate], backward[target] = target, candidate
    states = [state for case in cases for state in case["states"]]
    polynomial_atoms = sum(len(state["count_polynomials"]) for state in states)
    positive_histories = sum(F(history["joint_probability"]) > 0 for history in histories)
    result = {
        "cases": cases,
        "histories": histories,
        "candidate_partitions": candidate_partitions,
        "target_partitions": target_partitions,
        "assessments": assessments,
        "candidate_refinement": candidate_refinement,
        "target_refinement": target_refinement,
        "counts": {
            "cases": len(cases),
            "states": len(states),
            "positive_states": sum(F(state["probability"]) > 0 for state in states),
            "observations": sum(len(state["observations"]) for state in states),
            "histories": len(histories),
            "positive_histories": positive_histories,
            "zero_histories": len(histories) - positive_histories,
            "candidates": len(_CANDIDATES),
            "targets": len(_TARGETS),
            "polynomial_atoms": polynomial_atoms,
            "polynomial_coefficient_cells": polynomial_atoms * 16,
            "mean_coefficient_cells": len(states) * 4 * 16,
        },
    }
    _native_json(result)
    return result
