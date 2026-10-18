"""Independent finite predictive-compression oracle for QR-05G.

Populations and acquisition laws are encoded locally.  Full-source chain
indicators independently supply observed counts and estimates.  Future record
signatures include the induced order on retained original IDs, not merely a
mask law.  No primary executor, previous executor, or artifact is imported.

The integrated fixed universe is exposed only through ``analyze(problem)``.
Pooled masses are unnormalized per-case bookkeeping and sum to ten; they are
not a prior or posterior over hidden source profiles.
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
)
_TARGETS = ("current_estimate", "future_means", "future_counts", "future_records")


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


def _matrix(matrix):
    return [_vector(row) for row in matrix]


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
        _require(all(type(key) is str for key in value), "reference JSON keys must be strings")
        for child in value.values():
            _native_json(child)
        return
    raise ValueError("reference result contains a non-native JSON value")


def _canonical(value):
    # Type-exact native JSON encoding prevents Python's bool/int key equality.
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    )


def _parse(problem):
    _require(
        type(problem) is dict
        and all(type(key) is str for key in problem)
        and set(problem) == {"schema_version", "family"},
        "reference problem must have exactly the specified keys",
    )
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05g-problem-v1",
        "reference schema is unsupported",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05f_ten",
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


def _token(design, mask):
    if design == "parity_adaptive":
        return F(1, 3) if mask.bit_count() % 2 == 0 else F(2, 3)
    if design == "parity_hole":
        return F(int(mask.bit_count() % 2 == 0))
    return F(1, 2)


def _laws(design, size):
    number = 1 << size
    first = (
        [F(1, comb(size, 2)) if mask.bit_count() == 2 else F(0) for mask in range(number)]
        if design == "first_pair"
        else [F(1, number)] * number
    )
    conditional, tokens = [], []
    for mask in range(number):
        token = _token(design, mask)
        tokens.append(token)
        row = []
        for repeat in range(number):
            if repeat & mask != repeat:
                continue
            if design == "common_coin":
                probability = F(1) if mask == 0 else F(1, 2) if repeat in (0, mask) else F(0)
            else:
                probability = token ** repeat.bit_count() * (1 - token) ** (
                    mask.bit_count() - repeat.bit_count()
                )
            row.append((repeat, _bounded(probability)))
        _require(
            sum((probability for _, probability in row), F(0)) == 1,
            "reference conditional repeat law is not normalized",
        )
        conditional.append(row)
    pi1 = [
        sum(
            (probability for mask, probability in enumerate(first) if mask & support == support),
            F(0),
        )
        for support in range(number)
    ]
    pi2 = [
        [
            sum((probability for repeat, probability in row if repeat & support == support), F(0))
            for support in range(number)
        ]
        for row in conditional
    ]
    _require(
        sum(first, F(0)) == pi1[0] == 1 and all(row[0] == 1 for row in pi2),
        "reference first law or empty-support inclusion is invalid",
    )
    return first, conditional, tokens, pi1, pi2


def _chains(past, eligible):
    positions = {node: bit for bit, node in enumerate(eligible)}
    families = []
    for degree in range(4):
        row = []
        for vertices in combinations(range(1, 7), degree):
            if all(first in past[second] for first, second in pairwise((0, *vertices, 7))):
                support = sum(1 << positions[node] for node in vertices if node in positions)
                row.append((vertices, support))
        families.append(row)
    return families


def _observations(past, fixed, eligible, families):
    observations = []
    for mask in range(1 << len(eligible)):
        kept = sorted([*fixed, *(node for bit, node in enumerate(eligible) if mask & (1 << bit))])
        positions = {node: index for index, node in enumerate(kept)}
        observed = [
            [positions[ancestor] for ancestor in past[node] if ancestor in positions]
            for node in kept
        ]
        graded = [[0] * 4 for _ in range(4)]
        for degree, chains in enumerate(families):
            for _, support in chains:
                if mask & support == support:
                    graded[degree][support.bit_count()] += 1
        observations.append((kept, observed, [sum(row) for row in graded], graded))
    return observations


def _order_signature(kept, past, anchors):
    """Canonicalize only the supplied observed relation, with named anchors."""
    relation = {(kept[source], kept[target]) for target, row in enumerate(past) for source in row}
    others = [node for node in kept if node not in anchors]
    n = len(kept)
    best = None
    for perm in permutations(others):
        ordered = (*anchors, *perm)
        positions = {node: index for index, node in enumerate(ordered)}
        code = sum(1 << (positions[source] * n + positions[target]) for source, target in relation)
        if best is None or code < best:
            best = code
    _require(type(best) is int and best.bit_length() <= 4096, "reference canonical code is invalid")
    return [n, best]


def _repeat_statistics(row, observations):
    count_law = {}
    for mask, probability in row:
        if probability > 0:
            counts = tuple(observations[mask][2])
            count_law[counts] = count_law.get(counts, F(0)) + probability
    means = [
        sum((probability * counts[i] for counts, probability in count_law.items()), F(0))
        for i in range(4)
    ]
    covariance = [[F(0)] * 4 for _ in range(4)]
    # Centered outer products over the explicit observation law, not matrix powers.
    for mask, probability in row:
        if probability == 0:
            continue
        centered = [F(value) - mean for value, mean in zip(observations[mask][2], means)]
        for first in range(4):
            for second in range(first, 4):
                covariance[first][second] += probability * centered[first] * centered[second]
    for first in range(4):
        for second in range(first, 4):
            covariance[first][second] = covariance[second][first] = _bounded(
                covariance[first][second]
            )
    public_law = [
        {"counts": list(counts), "probability": _wire(probability)}
        for counts, probability in sorted(count_law.items())
    ]
    _require(sum(count_law.values(), F(0)) == 1, "reference count law lost probability mass")
    return public_law, means, covariance


def _case(case_index, profile, design):
    past, fixed, eligible = _population(profile)
    first, conditional, tokens, pi1, pi2 = _laws(design, len(eligible))
    families = _chains(past, eligible)
    observations = _observations(past, fixed, eligible, families)
    scales = [F((-1) ** degree, 2 ** (degree + 1) * 12**degree) for degree in range(4)]
    states = []
    future_signatures = []
    for mask, row in enumerate(conditional):
        kept, observed, counts, graded = observations[mask]
        repeats = [
            {
                "mask": repeat,
                "probability": _wire(probability),
                "kept": observations[repeat][0],
                "past": observations[repeat][1],
                "chain_counts": observations[repeat][2],
            }
            for repeat, probability in row
        ]
        law, mean, covariance = _repeat_statistics(row, observations)
        unmarked = _order_signature(kept, observed, [0, 7])
        marked = unmarked if fixed == [0, 7] else _order_signature(kept, observed, fixed)
        states.append(
            {
                "mask": mask,
                "probability": _wire(first[mask]),
                "kept": kept,
                "past": observed,
                "policy_token": _wire(tokens[mask]),
                "tagged_present": bool(mask & 1),
                "chain_counts": counts,
                "graded_counts": graded,
                "unmarked_order": unmarked,
                "marked_order": marked,
                "repeat_rows": repeats,
                "count_law": law,
                "count_mean": _vector(mean),
                "count_covariance": _matrix(covariance),
                "coefficient_mean": _vector([value * scale for value, scale in zip(mean, scales)]),
                "coefficient_covariance": _matrix(
                    [[covariance[i][j] * scales[i] * scales[j] for j in range(4)] for i in range(4)]
                ),
            }
        )
        record_law = [
            {
                "kept": observations[repeat][0],
                "past": observations[repeat][1],
                "probability": _wire(probability),
            }
            for repeat, probability in row
            if probability > 0
        ]
        future_signatures.append((_vector(mean), law, record_law))
    public = {
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
    internal = (first, conditional, pi1, pi2, families, observations, future_signatures)
    return public, internal


def _current_estimate(retained, intermediate, families, pi1, pi2):
    estimates, omissions = [], []
    for chains in families:
        value, omitted = F(0), 0
        for _, support in chains:
            if retained & support != support:
                continue
            denominator = pi1[support] * pi2[intermediate][support]
            if denominator > 0:
                value += 1 / denominator
            else:
                omitted += 1
        estimates.append(_wire(value))
        omissions.append(omitted)
    return estimates, omissions


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
    }


def _refinement(names, histories, field):
    matrix = []
    for fine in names:
        row = []
        for coarse in names:
            mapping = {}
            valid = True
            for history in histories:
                fine_id = history[field][fine]
                if fine_id is None:
                    continue
                coarse_id = history[field][coarse]
                if fine_id not in mapping:
                    mapping[fine_id] = coarse_id
                elif mapping[fine_id] != coarse_id:
                    valid = False
                    break
            row.append(valid)
        matrix.append(row)
    return matrix


def _assess(histories, candidate_partitions):
    result = {}
    for candidate in _CANDIDATES:
        targets = {}
        for target in _TARGETS:
            first_members = {}
            first_collision = None
            common = set()
            for history in histories:
                candidate_id = history["candidate_classes"][candidate]
                if candidate_id is None:
                    continue
                target_id = history["target_classes"][target]
                common.add((candidate_id, target_id))
                if candidate_id not in first_members:
                    first_members[candidate_id] = (history["history_id"], target_id)
                elif first_collision is None and first_members[candidate_id][1] != target_id:
                    first_collision = {
                        "left_history": first_members[candidate_id][0],
                        "right_history": history["history_id"],
                    }
            sufficient = first_collision is None
            _require(
                sufficient == (len(common) == len(candidate_partitions[candidate])),
                "reference finite minimality/class-splitting identity failed",
            )
            targets[target] = {
                "sufficient": sufficient,
                "first_collision": first_collision,
                "common_refinement_classes": len(common),
            }
        result[candidate] = targets
    return result


def analyze(problem):
    """Return the complete pooled ten-case universe with type-exact partitions."""
    _parse(problem)
    cases, internals = [], []
    for index, (profile, design) in enumerate(_CASES):
        case, internal = _case(index, profile, design)
        cases.append(case)
        internals.append(internal)
    candidate_partitions = {name: [] for name in _CANDIDATES}
    target_partitions = {name: [] for name in _TARGETS}
    candidate_indices = {name: {} for name in _CANDIDATES}
    target_indices = {name: {} for name in _TARGETS}
    candidate_masses = {name: [] for name in _CANDIDATES}
    target_masses = {name: [] for name in _TARGETS}
    histories = []
    for case, internal in zip(cases, internals):
        first, conditional, pi1, pi2, families, observations, future_signatures = internal
        context = [case["design"], case["density"], case["fixed"], case["eligible"]]
        for intermediate, conditional_row in enumerate(conditional):
            state = case["states"][intermediate]
            for retained, probability in conditional_row:
                history_id = len(histories)
                joint = _bounded(first[intermediate] * probability)
                current, omitted = _current_estimate(retained, intermediate, families, pi1, pi2)
                candidate_classes = {name: None for name in _CANDIDATES}
                target_classes = {name: None for name in _TARGETS}
                if joint > 0:
                    base = [context, observations[retained][0], observations[retained][1]]
                    keys = _candidate_keys(base, state)
                    signatures = (current, *future_signatures[intermediate])
                    for name in _CANDIDATES:
                        encoded = _canonical(keys[name])
                        if encoded not in candidate_indices[name]:
                            class_id = len(candidate_partitions[name])
                            candidate_indices[name][encoded] = class_id
                            candidate_partitions[name].append(
                                {
                                    "class_id": class_id,
                                    "members": [],
                                    "joint_mass": "0",
                                    "key": keys[name],
                                }
                            )
                            candidate_masses[name].append(F(0))
                        class_id = candidate_indices[name][encoded]
                        candidate_partitions[name][class_id]["members"].append(history_id)
                        candidate_masses[name][class_id] += joint
                        candidate_classes[name] = class_id
                    for name, signature in zip(_TARGETS, signatures):
                        encoded = _canonical([base, signature])
                        if encoded not in target_indices[name]:
                            class_id = len(target_partitions[name])
                            target_indices[name][encoded] = class_id
                            target_partitions[name].append(
                                {
                                    "class_id": class_id,
                                    "members": [],
                                    "joint_mass": "0",
                                    "base": base,
                                    "signature": signature,
                                }
                            )
                            target_masses[name].append(F(0))
                        class_id = target_indices[name][encoded]
                        target_partitions[name][class_id]["members"].append(history_id)
                        target_masses[name][class_id] += joint
                        target_classes[name] = class_id
                histories.append(
                    {
                        "history_id": history_id,
                        "case_index": case["case_index"],
                        "stage1_mask": intermediate,
                        "final_mask": retained,
                        "conditional_probability": _wire(probability),
                        "joint_probability": _wire(joint),
                        "current_estimate": current,
                        "omitted_terms": omitted,
                        "candidate_classes": candidate_classes,
                        "target_classes": target_classes,
                    }
                )
    for partitions, masses in (
        (candidate_partitions, candidate_masses),
        (target_partitions, target_masses),
    ):
        for name, groups in partitions.items():
            _require(
                sum(masses[name], F(0)) == 10,
                "reference pooled design bookkeeping does not sum to ten",
            )
            for group, mass in zip(groups, masses[name]):
                group["joint_mass"] = _wire(mass)
    assessments = _assess(histories, candidate_partitions)
    candidate_refinement = _refinement(_CANDIDATES, histories, "candidate_classes")
    target_refinement = _refinement(_TARGETS, histories, "target_classes")
    _require(
        target_refinement[3][2] and target_refinement[2][1],
        "reference predictive-law nesting failed",
    )
    _require(
        all(assessments["full_record"][target]["sufficient"] for target in _TARGETS),
        "reference full observed intermediate record failed a declared target",
    )
    _require(
        assessments["graded_policy"]["future_means"]["sufficient"],
        "reference graded-support mean control failed",
    )
    _require(
        assessments["marked_order"]["future_counts"]["sufficient"],
        "reference marked-order count-law control failed",
    )
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
            "states": sum(len(case["states"]) for case in cases),
            "positive_states": sum(
                F(state["probability"]) > 0 for case in cases for state in case["states"]
            ),
            "repeat_rows": sum(
                len(state["repeat_rows"]) for case in cases for state in case["states"]
            ),
            "positive_repeat_rows": sum(
                F(row["probability"]) > 0
                for case in cases
                for state in case["states"]
                for row in state["repeat_rows"]
            ),
            "histories": len(histories),
            "positive_histories": positive_histories,
            "zero_histories": len(histories) - positive_histories,
            "candidates": len(_CANDIDATES),
            "targets": len(_TARGETS),
            "current_estimator_cells": len(histories) * 4,
        },
    }
    _native_json(result)
    return result
