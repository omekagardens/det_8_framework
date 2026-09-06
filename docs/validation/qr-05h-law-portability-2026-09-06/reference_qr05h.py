"""Independent exact observation-law portability oracle for QR-05H.

This implementation imports no primary/prior executor or artifact.  Locally
encoded source-chain indicators provide a separate oracle route to observed
counts.  Acquisition colors are declared public marks, not geometric data.
Fine/coarse changes of measure retain missing mass without renormalization.

Only ``analyze(problem)`` is advertised.  All laws are finite supplied laws;
class masses sum to ten as per-case bookkeeping, never as a source prior.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, pairwise, permutations, product
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
_POLICIES = ("iid_half", "iid_color", "block_coin")
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
_TARGETS = (
    "iid_half_means",
    "iid_half_counts",
    "iid_color_means",
    "iid_color_counts",
    "block_coin_means",
    "block_coin_counts",
    "menu_means",
    "menu_counts",
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
        and problem["schema_version"] == "det8-qr05h-problem-v1",
        "reference schema is unsupported",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05g_menu3",
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


def _menu_laws(mask, eligible, observations):
    present = [node for bit, node in enumerate(eligible) if mask & (1 << bit)]
    groups = [
        sum(
            1 << bit for bit, node in enumerate(eligible) if mask & (1 << bit) and node % 2 == color
        )
        for color in (0, 1)
    ]
    active = [group for group in groups if group]
    laws = {name: [] for name in _POLICIES}
    for observation in observations:
        retained = observation["mask"]
        kept_set = set(observation["kept"])
        laws["iid_half"].append(F(1, 1 << len(present)))
        color_probability = F(1)
        for node in present:
            rate = F(1, 3) if node % 2 else F(2, 3)
            color_probability *= rate if node in kept_set else 1 - rate
        laws["iid_color"].append(_bounded(color_probability))
        compatible = all(retained & group in (0, group) for group in active)
        laws["block_coin"].append(F(1, 1 << len(active)) if compatible else F(0))
    _require(
        all(sum(row, F(0)) == 1 and all(value >= 0 for value in row) for row in laws.values()),
        "reference continuation menu law is not normalized",
    )
    return laws


def _law_wire(atom_masses):
    return [
        {"counts": list(atom), "probability": _wire(mass)}
        for atom, mass in sorted(atom_masses.items())
        if mass > 0
    ]


def _predictions(observations, laws, colors):
    predictions = {}
    scales = [F((-1) ** degree, 2 ** (degree + 1) * 12**degree) for degree in range(4)]
    for policy in _POLICIES:
        probabilities = laws[policy]
        atoms = {}
        for observation, probability in zip(observations, probabilities):
            atom = tuple(observation["chain_counts"])
            atoms[atom] = atoms.get(atom, F(0)) + probability
        means = [
            sum(
                (
                    probability * observation["chain_counts"][degree]
                    for observation, probability in zip(observations, probabilities)
                ),
                F(0),
            )
            for degree in range(4)
        ]
        for degree in range(4):
            oracle = F(0)
            for odd in range(4):
                for even in range(4):
                    if policy == "iid_half":
                        factor = F(1, 2 ** (odd + even))
                    elif policy == "iid_color":
                        factor = F(1, 3) ** odd * F(2, 3) ** even
                    else:
                        factor = F(1, 2 ** (int(odd > 0) + int(even > 0)))
                    oracle += colors[degree][odd][even] * factor
            _require(means[degree] == oracle, "reference color-graded mean prediction failed")
        predictions[policy] = {
            "probabilities": _vector(probabilities),
            "count_law": _law_wire(atoms),
            "count_mean": _vector(means),
            "coefficient_mean": _vector([mean * scale for mean, scale in zip(means, scales)]),
        }
    block_atoms = {}
    for keep_odd, keep_even in product((False, True), repeat=2):
        atom = tuple(
            sum(
                colors[degree][odd][even]
                for odd in range(4)
                for even in range(4)
                if (odd == 0 or keep_odd) and (even == 0 or keep_even)
            )
            for degree in range(4)
        )
        block_atoms[atom] = block_atoms.get(atom, F(0)) + F(1, 4)
    _require(
        _law_wire(block_atoms) == predictions["block_coin"]["count_law"],
        "reference color-graded complete block law failed",
    )
    return predictions


def _transports(observations, laws):
    atoms = sorted({tuple(row["chain_counts"]) for row in observations})
    results = []
    for source in _POLICIES:
        for target in _POLICIES:
            source_law, target_law = laws[source], laws[target]
            masses = {atom: [F(0), F(0), F(0)] for atom in atoms}
            fine_weights, missing_masks = [], []
            fine_missing = F(0)
            representatives = {}
            collision = None
            for observation, q, p in zip(observations, source_law, target_law):
                atom = tuple(observation["chain_counts"])
                masses[atom][0] += q
                masses[atom][1] += p
                if q > 0:
                    weight = _bounded(p / q)
                    fine_weights.append(_wire(weight))
                    masses[atom][2] += p
                    if atom not in representatives:
                        representatives[atom] = (observation["mask"], weight)
                    elif collision is None and representatives[atom][1] != weight:
                        collision = {
                            "left_mask": representatives[atom][0],
                            "right_mask": observation["mask"],
                        }
                else:
                    fine_weights.append(None)
                    if p > 0:
                        missing_masks.append(observation["mask"])
                        fine_missing += p
            coarse_rows = []
            coarse_missing, residual_sum = F(0), F(0)
            coarse_weighted, fine_weighted = {}, {}
            for atom, (q, p, accessible) in sorted(masses.items()):
                missing = p - accessible
                _require(missing >= 0, "reference inaccessible target mass is negative")
                if q > 0:
                    weight, conditional_weight = p / q, accessible / q
                    _require(
                        weight - conditional_weight == missing / q,
                        "reference pointwise fine/coarse residual identity failed",
                    )
                    residual_sum += q * (weight - conditional_weight)
                    coarse_weighted[atom] = p
                    weighted_probability = p
                else:
                    weight, conditional_weight = None, None
                    coarse_missing += p
                    weighted_probability = F(0)
                fine_weighted[atom] = accessible
                coarse_rows.append(
                    {
                        "counts": list(atom),
                        "source_probability": _wire(q),
                        "target_probability": _wire(p),
                        "fine_supported_target_probability": _wire(accessible),
                        "missing_fine_probability": _wire(missing),
                        "weight": None if weight is None else _wire(weight),
                        "conditional_fine_weight": None
                        if conditional_weight is None
                        else _wire(conditional_weight),
                        "weighted_probability": _wire(weighted_probability),
                    }
                )
            _require(
                sum(fine_weighted.values(), F(0)) == 1 - fine_missing,
                "reference fine supported subprobability mass failed",
            )
            _require(
                sum(coarse_weighted.values(), F(0)) == 1 - coarse_missing,
                "reference coarse supported subprobability mass failed",
            )
            _require(
                residual_sum == fine_missing - coarse_missing,
                "reference integrated fine/coarse residual identity failed",
            )
            _require(
                fine_missing != 0 or coarse_missing == 0,
                "reference support pushforward implication failed",
            )
            results.append(
                {
                    "source": source,
                    "target": target,
                    "fine_weights": fine_weights,
                    "missing_masks": missing_masks,
                    "fine_missing_mass": _wire(fine_missing),
                    "fine_supported": fine_missing == 0,
                    "weighted_count_law": _law_wire(fine_weighted),
                    "coarse_rows": coarse_rows,
                    "coarse_missing_mass": _wire(coarse_missing),
                    "coarse_supported": coarse_missing == 0,
                    "coarse_weighted_count_law": _law_wire(coarse_weighted),
                    "fine_weight_count_measurable": collision is None,
                    "first_weight_collision": collision,
                }
            )
    return results


def _population_states(past, fixed, eligible):
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
        laws = _menu_laws(mask, eligible, observations)
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
                "predictions": _predictions(observations, laws, colors),
                "transports": _transports(observations, laws),
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
    means = [state["predictions"][policy]["count_mean"] for policy in _POLICIES]
    laws = [state["predictions"][policy]["count_law"] for policy in _POLICIES]
    return (means[0], laws[0], means[1], laws[1], means[2], laws[2], means, laws)


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


def _check_menu_refinement(histories, individual, menu):
    forward, backward = {}, {}
    for history in histories:
        target_ids = history["target_classes"]
        menu_id = target_ids[menu]
        if menu_id is None:
            continue
        triple = tuple(target_ids[name] for name in individual)
        _require(
            triple not in forward or forward[triple] == menu_id,
            "reference menu partition splits an individual common-refinement class",
        )
        _require(
            menu_id not in backward or backward[menu_id] == triple,
            "reference menu partition merges different individual prediction triples",
        )
        forward[triple], backward[menu_id] = menu_id, triple


def analyze(problem):
    """Return the integrated finite menu, transports, and pooled partitions."""
    _parse(problem)
    cases, case_laws, population_cache = [], [], {}
    for case_index, (profile, design) in enumerate(_CASES):
        past, fixed, eligible = _population(profile)
        # Cache identical supplied order/frame computations, not hidden profile labels.
        population_key = (tuple(tuple(row) for row in past), tuple(fixed), tuple(eligible))
        if population_key not in population_cache:
            population_cache[population_key] = _population_states(past, fixed, eligible)
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
    _check_menu_refinement(
        histories, ("iid_half_means", "iid_color_means", "block_coin_means"), "menu_means"
    )
    _check_menu_refinement(
        histories, ("iid_half_counts", "iid_color_counts", "block_coin_counts"), "menu_counts"
    )
    _require(
        all(target_refinement[i + 1][i] for i in (0, 2, 4, 6)),
        "reference count-to-mean refinement failed",
    )
    for target in _TARGETS:
        _require(
            assessments["full_record"][target]["sufficient"]
            and assessments["color_order"][target]["sufficient"],
            "reference complete-record or named-color-order control failed",
        )
    _require(
        assessments["color_graded"]["menu_means"]["sufficient"]
        and assessments["color_graded"]["block_coin_counts"]["sufficient"],
        "reference color-graded menu-mean/block-law control failed",
    )
    _require(
        assessments["block_order"]["iid_half_counts"]["sufficient"]
        and assessments["block_order"]["block_coin_counts"]["sufficient"],
        "reference anonymous-block control failed",
    )
    states = [state for case in cases for state in case["states"]]
    transports = [transport for state in states for transport in state["transports"]]
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
            "policies": len(_POLICIES),
            "predictions": len(states) * len(_POLICIES),
            "probability_cells": sum(
                len(prediction["probabilities"])
                for state in states
                for prediction in state["predictions"].values()
            ),
            "histories": len(histories),
            "positive_histories": positive_histories,
            "zero_histories": len(histories) - positive_histories,
            "candidates": len(_CANDIDATES),
            "targets": len(_TARGETS),
            "transports": len(transports),
            "fine_weight_cells": sum(len(transport["fine_weights"]) for transport in transports),
            "coarse_weight_cells": sum(len(transport["coarse_rows"]) for transport in transports),
        },
    }
    _native_json(result)
    return result
