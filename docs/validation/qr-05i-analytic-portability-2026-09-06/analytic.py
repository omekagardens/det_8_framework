"""QR-05I exact polynomial laws from supplied intermediate observations.

No files, retained artifacts, or previous executors are accessed at runtime.
Binomial expansion uses only the induced S/U orders and public color marks.
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
    "color_graded",
    "block_order",
    "color_order",
)
TARGETS = ("analytic_means", "analytic_counts")
BIT_LIMIT = 4096
ZERO = Fraction(0)
ONE = Fraction(1)


def wire(value):
    """Encode exact arithmetic and reject implicit container/type coercion."""
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
            raise TypeError("wire dictionary keys must be native strings")
        return {key: wire(item) for key, item in value.items()}
    raise TypeError("unsupported exact wire value")


def _key(value):
    """Hashable, type-aware identity of the eventual exact native wire."""
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
    past = [[] for _ in range(8)]
    for right in range(1, 8):
        past[right].append(0)
    past[7].extend(range(1, 7))
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
    old = {vertex: index for index, vertex in enumerate(parent_kept)}
    new = {vertex: index for index, vertex in enumerate(kept)}
    return [
        sorted(
            new[parent_kept[index]]
            for index in parent_past[old[vertex]]
            if parent_kept[index] in new
        )
        for vertex in kept
    ]


def _kept(fixed, eligible, mask):
    return sorted(fixed + [vertex for bit, vertex in enumerate(eligible) if mask & (1 << bit)])


def _supports(kept, past, eligible):
    """Observed chain supports only; no source inventory enters this function."""
    indices = {vertex: index for index, vertex in enumerate(kept)}
    eligible_bits = {vertex: 1 << bit for bit, vertex in enumerate(eligible)}
    internal = [vertex for vertex in kept if vertex not in (0, 7)]
    result = [[] for _ in range(4)]
    for degree in range(4):
        for vertices in combinations(internal, degree):
            chain = [0, *vertices, 7]
            if all(indices[left] in past[indices[right]] for left, right in pairwise(chain)):
                result[degree].append(sum(eligible_bits.get(vertex, 0) for vertex in vertices))
    return result


def _gradings(supports, odd_mask):
    graded = [[0 for _ in range(4)] for _ in range(4)]
    colored = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for degree, chains in enumerate(supports):
        for support in chains:
            odd = (support & odd_mask).bit_count()
            even = (support & ~odd_mask).bit_count()
            graded[degree][odd + even] += 1
            colored[degree][odd][even] += 1
    return graded, colored


def _canonical_codes(kept, past, anchors, decorated):
    """Minimum relation code and, optionally, lexicographic decorated codes."""
    anchored = sorted(anchors)
    if len(set(anchored)) != len(anchored) or not set(anchored) <= set(kept):
        raise ValueError("anchors must be distinct observed vertices")
    eligible = [vertex for vertex in kept if vertex not in anchored]
    if len(eligible) > 6:
        raise ValueError("canonical permutation bound exceeded")
    edges = [
        (kept[left], kept[right])
        for right, predecessors in enumerate(past)
        for left in predecessors
    ]
    size = len(kept)
    relation_min = block_min = color_min = None
    for remaining in permutations(eligible):
        arranged = [*anchored, *remaining]
        positions = {vertex: index for index, vertex in enumerate(arranged)}
        relation = sum(1 << (positions[left] * size + positions[right]) for left, right in edges)
        if relation_min is None or relation < relation_min:
            relation_min = relation
        if decorated:
            color = sum(1 << positions[vertex] for vertex in remaining if vertex % 2)
            block = sum(
                1 << (i * size + j)
                for i in range(len(anchored), size)
                for j in range(i + 1, size)
                if arranged[i] % 2 == arranged[j] % 2
            )
            if color_min is None or (relation, color) < color_min:
                color_min = (relation, color)
            if block_min is None or (relation, block) < block_min:
                block_min = (relation, block)
    plain = [size, relation_min]
    if decorated:
        return plain, [size, *block_min], [size, *color_min]
    return plain


def _first_probability(design, width, mask):
    if design == "first_pair":
        return Fraction(1, comb(width, 2)) if mask.bit_count() == 2 else ZERO
    return Fraction(1, 1 << width)


def _current_rate(design, stage1):
    if design == "parity_adaptive":
        return Fraction(2 if stage1.bit_count() % 2 else 1, 3)
    if design == "parity_hole":
        return Fraction(0 if stage1.bit_count() % 2 else 1)
    return Fraction(1, 2)


def _current_kernel(design, stage1, final):
    if final & ~stage1:
        return ZERO
    if design == "common_coin":
        if not stage1:
            return ONE
        return Fraction(1, 2) if final in (0, stage1) else ZERO
    rate = _current_rate(design, stage1)
    return rate ** final.bit_count() * (1 - rate) ** (stage1.bit_count() - final.bit_count())


def _count_polynomials(observations, odd_mask, color_sizes):
    """Binomial-expand the observed subset law in the integer monomial basis."""
    odd_total, even_total = color_sizes
    if not (0 <= odd_total <= 3 and 0 <= even_total <= 3):
        raise ValueError("two-color degree bound exceeded")
    atoms = {}
    for observation in observations:
        atom = tuple(observation["chain_counts"])
        coefficients = atoms.setdefault(atom, [[0 for _ in range(4)] for _ in range(4)])
        odd = (observation["mask"] & odd_mask).bit_count()
        even = (observation["mask"] & ~odd_mask).bit_count()
        if odd > odd_total or even > even_total:
            raise ValueError("observed subset exceeds supplied color frame")
        for i in range(odd_total - odd + 1):
            for j in range(even_total - even + 1):
                coefficients[odd + i][even + j] += (
                    (-1) ** (i + j) * comb(odd_total - odd, i) * comb(even_total - even, j)
                )
    count_polynomials = []
    for atom in sorted(atoms):
        coefficients = atoms[atom]
        if not any(cell for row in coefficients for cell in row):
            raise ValueError("attainable count atom has a zero polynomial")
        count_polynomials.append({"counts": list(atom), "coefficients": coefficients})
    normalization = [
        [sum(coefficients[i][j] for coefficients in atoms.values()) for j in range(4)]
        for i in range(4)
    ]
    if normalization != [[int(i == 0 and j == 0) for j in range(4)] for i in range(4)]:
        raise ValueError("polynomial laws do not normalize coefficientwise")
    means = [
        [
            [
                sum(atom[q] * coefficients[i][j] for atom, coefficients in atoms.items())
                for j in range(4)
            ]
            for i in range(4)
        ]
        for q in range(4)
    ]
    return count_polynomials, means


def _observed_state(kept, past, fixed, eligible, design, stage1, probability):
    """All polynomial inputs are the observed S order and public eligibility."""
    odd_mask = sum(1 << bit for bit, vertex in enumerate(eligible) if vertex % 2)
    color_sizes = [(stage1 & odd_mask).bit_count(), (stage1 & ~odd_mask).bit_count()]
    supports = _supports(kept, past, eligible)
    graded, colored = _gradings(supports, odd_mask)
    marked, block, color = _canonical_codes(kept, past, fixed, True)
    unmarked = marked if fixed == [0, 7] else _canonical_codes(kept, past, [0, 7], False)
    observations = []
    for repeated in range(1 << len(eligible)):
        if repeated & ~stage1:
            continue
        observed_kept = _kept(fixed, eligible, repeated)
        observed_past = _induce(kept, past, observed_kept)
        observed_supports = _supports(observed_kept, observed_past, eligible)
        observations.append(
            {
                "mask": repeated,
                "kept": observed_kept,
                "past": observed_past,
                "chain_counts": [len(chains) for chains in observed_supports],
            }
        )
    polynomials, means = _count_polynomials(observations, odd_mask, color_sizes)
    if means != colored:
        raise ValueError("polynomial expectations disagree with observed color grading")
    return {
        "mask": stage1,
        "probability": probability,
        "kept": kept,
        "past": past,
        "policy_token": _current_rate(design, stage1),
        "tagged_present": bool(stage1 & 1),
        "chain_counts": [len(chains) for chains in supports],
        "graded_counts": graded,
        "unmarked_order": unmarked,
        "marked_order": marked,
        "color_graded": colored,
        "block_order": block,
        "color_order": color,
        "observations": observations,
        "color_sizes": color_sizes,
        "count_polynomials": polynomials,
        "mean_polynomials": means,
    }


def _candidate_suffixes(state):
    rate, tag, graded = state["policy_token"], state["tagged_present"], state["graded_counts"]
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
        "color_graded": [rate, state["color_graded"]],
        "block_order": [rate, state["block_order"]],
        "color_order": [rate, state["color_order"]],
    }


def _target_signatures(state):
    return {
        "analytic_means": state["mean_polynomials"],
        "analytic_counts": state["count_polynomials"],
    }


def _register(partition, identities, identity, history_id, mass, description):
    class_id = identities.get(identity)
    if class_id is None:
        class_id = len(partition)
        identities[identity] = class_id
        partition.append({"class_id": class_id, "members": [], "joint_mass": ZERO, **description})
    group = partition[class_id]
    group["members"].append(history_id)
    group["joint_mass"] += mass
    return class_id


def _refines(rows, field, finer, coarser):
    seen = {}
    for row in rows:
        if not row["joint_probability"]:
            continue
        left, right = row[field][finer], row[field][coarser]
        if left in seen and seen[left] != right:
            return False
        seen[left] = right
    return True


def _assess(histories, candidate_partitions):
    assessments = {}
    for candidate in CANDIDATES:
        assessments[candidate] = {}
        for target in TARGETS:
            representatives, common_classes, collision = {}, set(), None
            for row in histories:
                if not row["joint_probability"]:
                    continue
                candidate_class = row["candidate_classes"][candidate]
                target_class = row["target_classes"][target]
                common_classes.add((candidate_class, target_class))
                previous = representatives.get(candidate_class)
                if previous is None:
                    representatives[candidate_class] = (row["history_id"], target_class)
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
    """Compute the exact fixed H-history / two-color polynomial universe."""
    if (
        type(problem) is not dict
        or any(type(key) is not str for key in problem)
        or set(problem) != {"schema_version", "family"}
        or type(problem.get("schema_version")) is not str
        or problem.get("schema_version") != "det8-qr05i-problem-v1"
        or type(problem.get("family")) is not str
        or problem.get("family") != "qr05h_two_color"
    ):
        raise ValueError("expected the exact QR-05I qr05h_two_color problem")

    cases, histories = [], []
    candidate_partitions = {name: [] for name in CANDIDATES}
    target_partitions = {name: [] for name in TARGETS}
    candidate_ids = {name: {} for name in CANDIDATES}
    target_ids = {name: {} for name in TARGETS}
    counts = {
        "cases": len(CASES),
        "states": 0,
        "positive_states": 0,
        "observations": 0,
        "histories": 0,
        "positive_histories": 0,
        "zero_histories": 0,
        "candidates": len(CANDIDATES),
        "targets": len(TARGETS),
        "polynomial_atoms": 0,
        "polynomial_coefficient_cells": 0,
        "mean_coefficient_cells": 0,
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
        context = [design, Fraction(12), fixed, eligible]
        states, base_cache = [], {}
        for stage1, first_mass in enumerate(first_probabilities):
            kept = _kept(fixed, eligible, stage1)
            past = _induce(list(range(8)), source_past, kept)
            state = _observed_state(kept, past, fixed, eligible, design, stage1, first_mass)
            states.append(state)
            observations = state["observations"]
            counts["states"] += 1
            counts["positive_states"] += int(bool(first_mass))
            counts["observations"] += len(observations)
            counts["polynomial_atoms"] += len(state["count_polynomials"])
            counts["polynomial_coefficient_cells"] += 16 * len(state["count_polynomials"])
            counts["mean_coefficient_cells"] += 64
            suffixes = _candidate_suffixes(state)
            suffix_keys = {name: _key(value) for name, value in suffixes.items()}
            signatures = _target_signatures(state)
            signature_keys = {name: _key(value) for name, value in signatures.items()}
            current_mass = ZERO
            for observation in observations:
                final = observation["mask"]
                conditional_mass = _current_kernel(design, stage1, final)
                current_mass += conditional_mass
                joint_mass = first_mass * conditional_mass
                history_id = len(histories)
                history = {
                    "history_id": history_id,
                    "case_index": case_index,
                    "stage1_mask": stage1,
                    "final_mask": final,
                    "conditional_probability": conditional_mass,
                    "joint_probability": joint_mass,
                    "candidate_classes": {name: None for name in CANDIDATES},
                    "target_classes": {name: None for name in TARGETS},
                }
                histories.append(history)
                counts["histories"] += 1
                if not joint_mass:
                    counts["zero_histories"] += 1
                    continue
                counts["positive_histories"] += 1
                if final not in base_cache:
                    base = [context, observation["kept"], observation["past"]]
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
                    history["target_classes"][name] = _register(
                        target_partitions[name],
                        target_ids[name],
                        (base_key, signature_keys[name]),
                        history_id,
                        joint_mass,
                        {"base": base, "signature": signatures[name]},
                    )
            if current_mass != ONE:
                raise ValueError("current diagnostic kernel is not normalized")
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
            raise ValueError("pooled partition lost per-case mass multiplicity")
    for row in histories:
        if row["joint_probability"] and (
            row["candidate_classes"]["color_graded"] != row["target_classes"]["analytic_means"]
        ):
            raise ValueError("analytic means and color grading have different fibers")
    for target in TARGETS:
        for candidate in ("full_record", "color_order"):
            if not assessments[candidate][target]["sufficient"]:
                raise ValueError("analytic sufficient control failed")
    if not target_refinement[1][0]:
        raise ValueError("polynomial count laws failed to refine polynomial means")
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
