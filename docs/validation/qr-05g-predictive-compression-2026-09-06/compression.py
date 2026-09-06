"""Exact observed-order route for the bounded QR-05G experiment.

No files are read or written here.  A supplied source produces each intermediate
observation; all subsequent prediction and estimation uses that observation.
"""

from fractions import Fraction
from itertools import combinations, pairwise, permutations
from math import comb

CASES = (
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
CANDIDATES = (
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
TARGETS = (
    "current_estimate",
    "future_means",
    "future_counts",
    "future_records",
)
BIT_LIMIT = 4096
ZERO = Fraction(0)
ONE = Fraction(1)


def wire(value):
    """Encode exact internal arithmetic without permissive container coercion."""
    if type(value) is Fraction:
        if max(value.numerator.bit_length(), value.denominator.bit_length()) > BIT_LIMIT:
            raise ValueError("rational exceeds the exact arithmetic bound")
        return str(value)
    if value is None or type(value) in (str, bool):
        return value
    if type(value) is int:
        if value.bit_length() > BIT_LIMIT:
            raise ValueError("integer exceeds the exact arithmetic bound")
        return value
    if type(value) is list:
        return [wire(item) for item in value]
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise TypeError("wire dictionary keys must be strings")
        return {key: wire(item) for key, item in value.items()}
    raise TypeError("unsupported exact wire value")


def _key(value):
    """Type-aware hashable identity of the native wire, not Python == coercion."""
    if type(value) is Fraction:
        return ("str", str(value))
    if value is None:
        return ("null",)
    if type(value) is str:
        return ("str", value)
    if type(value) is bool:
        return ("bool", value)
    if type(value) is int:
        return ("int", value)
    if type(value) is list:
        return ("list", tuple(_key(item) for item in value))
    if type(value) is dict and all(type(key) is str for key in value):
        return ("dict", tuple((key, _key(value[key])) for key in sorted(value)))
    raise TypeError("unsupported partition-key value")


def _source(profile):
    """The supplied source is used only to issue intermediate observations."""
    past = [[] for _ in range(8)]
    for right in range(1, 8):
        past[right].append(0)
    for right in range(1, 7):
        past[7].append(right)
    if profile == "chain6":
        for right in range(2, 7):
            past[right].extend(range(1, right))
    else:
        for left in range(1, 4):
            for right in range(4, 7):
                related = (
                    left - 1 != right - 4
                    if profile == "standard_example3"
                    else left - 1 <= right - 4
                )
                if related:
                    past[right].append(left)
    return [sorted(row) for row in past]


def _induce(parent_kept, parent_past, kept):
    """Restrict an already supplied labeled observation; never use hidden edges."""
    parent_indices = {vertex: index for index, vertex in enumerate(parent_kept)}
    local_indices = {vertex: index for index, vertex in enumerate(kept)}
    result = []
    for vertex in kept:
        predecessors = parent_past[parent_indices[vertex]]
        result.append(
            sorted(
                local_indices[parent_kept[index]]
                for index in predecessors
                if parent_kept[index] in local_indices
            )
        )
    return result


def _kept(fixed, eligible, mask):
    return sorted(fixed + [vertex for bit, vertex in enumerate(eligible) if mask & (1 << bit)])


def _supports(kept, past, eligible):
    """Enumerate chains only from the received induced order."""
    indices = {vertex: index for index, vertex in enumerate(kept)}
    eligible_bits = {vertex: 1 << bit for bit, vertex in enumerate(eligible)}
    internal = [vertex for vertex in kept if vertex not in (0, 7)]
    supports = [[] for _ in range(4)]
    for degree in range(4):
        for vertices in combinations(internal, degree):
            probe_chain = [0, *vertices, 7]
            if all(indices[left] in past[indices[right]] for left, right in pairwise(probe_chain)):
                supports[degree].append(sum(eligible_bits.get(vertex, 0) for vertex in vertices))
    return supports


def _graded(supports):
    table = [[0 for _ in range(4)] for _ in range(4)]
    for degree, chains in enumerate(supports):
        for support in chains:
            table[degree][support.bit_count()] += 1
    return table


def canonical_order(kept, past, anchors):
    """Canonical strict-order code under exactly the declared anchored action."""
    anchored = sorted(anchors)
    if len(set(anchored)) != len(anchored) or not set(anchored) <= set(kept):
        raise ValueError("canonical anchors must be distinct observed vertices")
    others = [vertex for vertex in kept if vertex not in anchored]
    if len(others) > 6:
        raise ValueError("canonical permutation bound exceeded")
    edges = [
        (kept[left], kept[right])
        for right, predecessors in enumerate(past)
        for left in predecessors
    ]
    size = len(kept)
    minimum = None
    for permuted in permutations(others):
        ordered = [*anchored, *permuted]
        positions = {vertex: index for index, vertex in enumerate(ordered)}
        code = sum(1 << (positions[left] * size + positions[right]) for left, right in edges)
        if minimum is None or code < minimum:
            minimum = code
    return [size, minimum]


def _first_probability(design, width, mask):
    if design == "first_pair":
        return Fraction(1, comb(width, 2)) if mask.bit_count() == 2 else ZERO
    return Fraction(1, 1 << width)


def _rate(design, stage1):
    if design == "parity_adaptive":
        return Fraction(2 if stage1.bit_count() % 2 else 1, 3)
    if design == "parity_hole":
        return Fraction(0 if stage1.bit_count() % 2 else 1)
    return Fraction(1, 2)


def _kernel(design, stage1, final):
    if final & ~stage1:
        return ZERO
    if design == "common_coin":
        if not stage1:
            return ONE
        return Fraction(1, 2) if final in (0, stage1) else ZERO
    rate = _rate(design, stage1)
    return rate ** final.bit_count() * (1 - rate) ** (stage1.bit_count() - final.bit_count())


def _conditional_inclusion(design, stage1, support):
    if support & ~stage1:
        return ZERO
    if not support:
        return ONE
    if design == "common_coin":
        return Fraction(1, 2)
    return _rate(design, stage1) ** support.bit_count()


def _moments(rows):
    mean = [
        sum((row["probability"] * row["chain_counts"][q] for row in rows), ZERO) for q in range(4)
    ]
    covariance = [
        [
            sum(
                (
                    row["probability"]
                    * (row["chain_counts"][q] - mean[q])
                    * (row["chain_counts"][r] - mean[r])
                    for row in rows
                ),
                ZERO,
            )
            for r in range(4)
        ]
        for q in range(4)
    ]
    return mean, covariance


def _observed_state(kept, past, fixed, eligible, design, stage1, probability):
    """Predict entirely from an intermediate observation and its public design."""
    supports = _supports(kept, past, eligible)
    graded = _graded(supports)
    repeat_rows = []
    repeat_supports = {}
    law = {}
    for repeated in range(1 << len(eligible)):
        if repeated & ~stage1:
            continue
        repeated_kept = _kept(fixed, eligible, repeated)
        repeated_past = _induce(kept, past, repeated_kept)
        observed_chains = _supports(repeated_kept, repeated_past, eligible)
        repeat_supports[repeated] = observed_chains
        counts = [len(chains) for chains in observed_chains]
        mass = _kernel(design, stage1, repeated)
        repeat_rows.append(
            {
                "mask": repeated,
                "probability": mass,
                "kept": repeated_kept,
                "past": repeated_past,
                "chain_counts": counts,
            }
        )
        if mass:
            atom = tuple(counts)
            law[atom] = law.get(atom, ZERO) + mass
    if sum((row["probability"] for row in repeat_rows), ZERO) != ONE:
        raise ValueError("declared repeat kernel is not normalized")
    count_law = [{"counts": list(counts), "probability": law[counts]} for counts in sorted(law)]
    mean, covariance = _moments(repeat_rows)
    inclusion_mean = [
        sum((_conditional_inclusion(design, stage1, a) for a in chains), ZERO)
        for chains in supports
    ]
    if mean != inclusion_mean:
        raise ValueError("repeat mean and observed-chain inclusion disagree")
    scales = [Fraction((-1) ** q, 2 ** (q + 1) * 12**q) for q in range(4)]
    state = {
        "mask": stage1,
        "probability": probability,
        "kept": kept,
        "past": past,
        "policy_token": _rate(design, stage1),
        "tagged_present": bool(stage1 & 1),
        "chain_counts": [len(chains) for chains in supports],
        "graded_counts": graded,
        "unmarked_order": canonical_order(kept, past, [0, 7]),
        "marked_order": canonical_order(kept, past, fixed),
        "repeat_rows": repeat_rows,
        "count_law": count_law,
        "count_mean": mean,
        "count_covariance": covariance,
        "coefficient_mean": [scales[q] * mean[q] for q in range(4)],
        "coefficient_covariance": [
            [scales[q] * scales[r] * covariance[q][r] for r in range(4)] for q in range(4)
        ],
    }
    return state, repeat_supports


def _current_estimate(observed_supports, design, stage1, first_inclusions):
    estimates = []
    omitted = []
    for chains in observed_supports:
        value = ZERO
        lost = 0
        for support in chains:
            first = first_inclusions[support]
            second = _conditional_inclusion(design, stage1, support)
            if first and second:
                value += 1 / (first * second)
            else:
                lost += 1
        estimates.append(value)
        omitted.append(lost)
    return estimates, omitted


def _candidate_suffixes(state):
    rate = state["policy_token"]
    tag = state["tagged_present"]
    graded = state["graded_counts"]
    return {
        "final_only": [],
        "policy_token": [rate],
        "tagged_policy": [rate, tag],
        "counts_policy": [rate, state["chain_counts"]],
        "graded_policy": [rate, graded],
        "tagged_graded": [rate, graded, tag],
        "unmarked_order": [rate, state["unmarked_order"]],
        "marked_order": [rate, state["marked_order"]],
        "full_record": [state["kept"], state["past"]],
    }


def _future_signatures(state):
    return {
        "future_means": state["count_mean"],
        "future_counts": state["count_law"],
        "future_records": [
            {
                "kept": row["kept"],
                "past": row["past"],
                "probability": row["probability"],
            }
            for row in state["repeat_rows"]
            if row["probability"]
        ],
    }


def _register(partition, identities, identity, history_id, mass, description):
    class_id = identities.get(identity)
    if class_id is None:
        class_id = len(partition)
        identities[identity] = class_id
        partition.append(
            {
                "class_id": class_id,
                "members": [],
                "joint_mass": ZERO,
                **description,
            }
        )
    group = partition[class_id]
    group["members"].append(history_id)
    group["joint_mass"] += mass
    return class_id


def _refines(rows, field, finer, coarser):
    seen = {}
    for row in rows:
        if not row["joint_probability"]:
            continue
        left = row[field][finer]
        right = row[field][coarser]
        if left in seen and seen[left] != right:
            return False
        seen[left] = right
    return True


def _assess(histories, candidate_partitions):
    assessments = {}
    for candidate in CANDIDATES:
        assessments[candidate] = {}
        for target in TARGETS:
            representatives = {}
            common_classes = set()
            collision = None
            for row in histories:
                if not row["joint_probability"]:
                    continue
                candidate_class = row["candidate_classes"][candidate]
                target_class = row["target_classes"][target]
                common_classes.add((candidate_class, target_class))
                previous = representatives.get(candidate_class)
                if previous is None:
                    representatives[candidate_class] = (
                        row["history_id"],
                        target_class,
                    )
                elif previous[1] != target_class and collision is None:
                    collision = {
                        "left_history": previous[0],
                        "right_history": row["history_id"],
                    }
            sufficient = collision is None
            if sufficient != (len(common_classes) == len(candidate_partitions[candidate])):
                raise ValueError("fiber constancy and common refinement disagree")
            assessments[candidate][target] = {
                "sufficient": sufficient,
                "first_collision": collision,
                "common_refinement_classes": len(common_classes),
            }
    return assessments


def analyze(problem):
    """Return the single declared ten-case universe in canonical exact wire form."""
    if (
        type(problem) is not dict
        or any(type(key) is not str for key in problem)
        or set(problem) != {"schema_version", "family"}
        or type(problem.get("schema_version")) is not str
        or problem.get("schema_version") != "det8-qr05g-problem-v1"
        or type(problem.get("family")) is not str
        or problem.get("family") != "qr05f_ten"
    ):
        raise ValueError("expected the exact QR-05G qr05f_ten problem")

    cases = []
    histories = []
    candidate_partitions = {name: [] for name in CANDIDATES}
    target_partitions = {name: [] for name in TARGETS}
    candidate_ids = {name: {} for name in CANDIDATES}
    target_ids = {name: {} for name in TARGETS}
    counts = {
        "cases": len(CASES),
        "states": 0,
        "positive_states": 0,
        "repeat_rows": 0,
        "positive_repeat_rows": 0,
        "histories": 0,
        "positive_histories": 0,
        "zero_histories": 0,
        "candidates": len(CANDIDATES),
        "targets": len(TARGETS),
        "current_estimator_cells": 0,
    }

    for case_index, (profile, design) in enumerate(CASES):
        source_past = _source(profile)
        fixed = [0, 3, 7] if profile == "ferrers6_fixed" else [0, 7]
        eligible = [vertex for vertex in range(1, 7) if vertex not in fixed]
        width = len(eligible)
        first_probabilities = [
            _first_probability(design, width, mask) for mask in range(1 << width)
        ]
        first_inclusions = [
            sum(
                (mass for mask, mass in enumerate(first_probabilities) if support & ~mask == 0),
                ZERO,
            )
            for support in range(1 << width)
        ]
        if sum(first_probabilities, ZERO) != ONE:
            raise ValueError("first-stage law is not normalized")
        context = [design, "12", fixed, eligible]
        states = []
        base_cache = {}
        for stage1, first_mass in enumerate(first_probabilities):
            kept = _kept(fixed, eligible, stage1)
            past = _induce(list(range(8)), source_past, kept)
            state, repeat_supports = _observed_state(
                kept, past, fixed, eligible, design, stage1, first_mass
            )
            states.append(state)
            counts["states"] += 1
            counts["positive_states"] += int(bool(first_mass))
            counts["repeat_rows"] += len(state["repeat_rows"])
            counts["positive_repeat_rows"] += sum(
                bool(row["probability"]) for row in state["repeat_rows"]
            )
            suffixes = _candidate_suffixes(state)
            suffix_keys = {name: _key(value) for name, value in suffixes.items()}
            future = _future_signatures(state)
            future_keys = {name: _key(value) for name, value in future.items()}
            for final_row in state["repeat_rows"]:
                final = final_row["mask"]
                conditional_mass = final_row["probability"]
                joint_mass = first_mass * conditional_mass
                estimate, omitted = _current_estimate(
                    repeat_supports[final], design, stage1, first_inclusions
                )
                history_id = len(histories)
                history = {
                    "history_id": history_id,
                    "case_index": case_index,
                    "stage1_mask": stage1,
                    "final_mask": final,
                    "conditional_probability": conditional_mass,
                    "joint_probability": joint_mass,
                    "current_estimate": estimate,
                    "omitted_terms": omitted,
                    "candidate_classes": {name: None for name in CANDIDATES},
                    "target_classes": {name: None for name in TARGETS},
                }
                histories.append(history)
                counts["histories"] += 1
                counts["current_estimator_cells"] += 4
                if not joint_mass:
                    counts["zero_histories"] += 1
                    continue
                counts["positive_histories"] += 1
                if final not in base_cache:
                    base = [context, final_row["kept"], final_row["past"]]
                    base_cache[final] = (base, _key(base))
                base, base_key = base_cache[final]
                for name in CANDIDATES:
                    history["candidate_classes"][name] = _register(
                        candidate_partitions[name],
                        candidate_ids[name],
                        (base_key, suffix_keys[name]),
                        history_id,
                        joint_mass,
                        {"key": [*base, *suffixes[name]]},
                    )
                for name in TARGETS:
                    signature = estimate if name == "current_estimate" else future[name]
                    signature_key = (
                        _key(estimate) if name == "current_estimate" else future_keys[name]
                    )
                    history["target_classes"][name] = _register(
                        target_partitions[name],
                        target_ids[name],
                        (base_key, signature_key),
                        history_id,
                        joint_mass,
                        {"base": base, "signature": signature},
                    )
        cases.append(
            {
                "case_index": case_index,
                "profile": profile,
                "design": design,
                "density": Fraction(12),
                "past": source_past,
                "fixed": fixed,
                "eligible": eligible,
                "stage1_inclusions": first_inclusions,
                "states": states,
            }
        )

    assessments = _assess(histories, candidate_partitions)
    candidate_refinement = [
        [_refines(histories, "candidate_classes", finer, coarser) for coarser in CANDIDATES]
        for finer in CANDIDATES
    ]
    target_refinement = [
        [_refines(histories, "target_classes", finer, coarser) for coarser in TARGETS]
        for finer in TARGETS
    ]
    for partition in [*candidate_partitions.values(), *target_partitions.values()]:
        if sum((group["joint_mass"] for group in partition), ZERO) != len(CASES):
            raise ValueError("pooled class masses lost per-case multiplicity")
    for target in TARGETS:
        if not assessments["full_record"][target]["sufficient"]:
            raise ValueError("full observed provenance failed a declared target")
    if not assessments["graded_policy"]["future_means"]["sufficient"]:
        raise ValueError("support-graded counts failed the mean positive control")
    if not assessments["marked_order"]["future_counts"]["sufficient"]:
        raise ValueError("marked isomorphism failed the count-law positive control")
    if not target_refinement[3][2] or not target_refinement[2][1]:
        raise ValueError("future-law pushforward partition hierarchy failed")

    return wire(
        {
            "cases": cases,
            "histories": histories,
            "candidate_partitions": candidate_partitions,
            "target_partitions": target_partitions,
            "assessments": assessments,
            "candidate_refinement": candidate_refinement,
            "target_refinement": target_refinement,
            "counts": counts,
        }
    )
