"""Independent exact chain-indicator oracle for the QR-05F finite fixtures.

The source populations and two-stage laws are encoded locally.  Estimates are
computed from full-source chain indicators as an audit route independent of
the primary executor's observed-order chain enumeration.  No other executor
or prior artifact is imported.  Source targets remain audit information, not
extra information made available to the observer.

Only ``analyze(problem)`` is the advertised interface.  It preserves impossible
transcripts, explicit unsupported terms, and undefined final conditioning.
Scalar-kernel coefficients are not quantum channels or probabilities.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, pairwise
from math import comb

F = Fraction
_CASES = {
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
}
_METHODS = ("final_joint", "sequential_supported", "naive_quarter")
_ACCESS_KEYS = ("final_only", "policy_token", "full_stage1")


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _bounded(value):
    _require(type(value) is F, "reference arithmetic must remain rational")
    _require(
        abs(value.numerator).bit_length() <= 4096 and value.denominator.bit_length() <= 4096,
        "reference rational exceeds the 4096-bit component bound",
    )
    return value


def _wire(value):
    return str(_bounded(value))


def _vector_wire(values):
    return [_wire(value) for value in values]


def _matrix_wire(matrix):
    return [_vector_wire(row) for row in matrix]


def _native_json(value):
    if value is None or type(value) in (str, bool):
        return
    if type(value) is int:
        _require(abs(value).bit_length() <= 4096, "reference integer exceeds the component bound")
        return
    if type(value) is list:
        for item in value:
            _native_json(item)
        return
    if type(value) is dict:
        _require(
            all(type(key) is str for key in value), "reference JSON object keys must be strings"
        )
        for item in value.values():
            _native_json(item)
        return
    raise ValueError("reference result contains a non-native JSON value")


def _parse(problem):
    _require(
        type(problem) is dict and set(problem) == {"schema_version", "profile", "design"},
        "reference problem must have exactly the specified keys",
    )
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05f-problem-v1",
        "reference schema is unsupported",
    )
    profile, design = problem["profile"], problem["design"]
    _require(
        type(profile) is str and type(design) is str, "reference fixture names must be strings"
    )
    _require((profile, design) in _CASES, "reference profile/design combination is unsupported")
    return profile, design


def _population(profile):
    past = [[]]
    for interior in range(6):
        if profile == "chain6":
            row = list(range(interior + 1))
        elif interior < 3:
            row = [0]
        else:
            right = interior - 3
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
        "reference population relation is not transitive",
    )
    return past, fixed, eligible, F(12)


def _policy(design, mask):
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
    conditional = []
    final = [F(0)] * number
    tokens = []
    for stage1 in range(number):
        token = _policy(design, stage1)
        tokens.append(token)
        row = []
        for retained in range(number):
            if retained & stage1 != retained:
                continue
            if design == "common_coin":
                probability = F(1) if stage1 == 0 else F(1, 2) if retained in (0, stage1) else F(0)
            else:
                probability = token ** retained.bit_count() * (1 - token) ** (
                    stage1.bit_count() - retained.bit_count()
                )
            probability = _bounded(probability)
            row.append((retained, probability))
            final[retained] += first[stage1] * probability
        _require(
            sum((probability for _, probability in row), F(0)) == 1,
            "reference conditional acquisition law is not normalized",
        )
        conditional.append(row)
    _require(
        sum(first, F(0)) == sum(final, F(0)) == 1, "reference acquisition law is not normalized"
    )
    return first, conditional, [_bounded(value) for value in final], tokens


def _inclusion_tables(first, conditional, final):
    number = len(first)
    pi1 = [
        sum(
            (probability for mask, probability in enumerate(first) if mask & support == support),
            F(0),
        )
        for support in range(number)
    ]
    pif = [
        sum(
            (probability for mask, probability in enumerate(final) if mask & support == support),
            F(0),
        )
        for support in range(number)
    ]
    pi2 = []
    for row in conditional:
        pi2.append(
            [
                sum(
                    (probability for retained, probability in row if retained & support == support),
                    F(0),
                )
                for support in range(number)
            ]
        )
    _require(
        pi1[0] == pif[0] == 1 and all(row[0] == 1 for row in pi2),
        "reference empty-support inclusion differs from one",
    )
    for support in range(number):
        _require(
            pif[support] == sum((first[mask] * pi2[mask][support] for mask in range(number)), F(0)),
            "reference composed inclusion identity failed",
        )
    return pi1, pi2, pif


def _questions(past, eligible, density, first, pi1, pi2, pif):
    bit_of = {node: bit for bit, node in enumerate(eligible)}
    families, public, scales, targets = [], [], [], []
    coverage, holes = [], []
    for support in range(len(first)):
        omitted_at = [
            mask
            for mask, probability in enumerate(first)
            if probability > 0 and mask & support == support and pi2[mask][support] == 0
        ]
        covered_probability = sum(
            (
                probability
                for mask, probability in enumerate(first)
                if mask & support == support and pi2[mask][support] > 0
            ),
            F(0),
        )
        coverage.append(F(0) if pi1[support] == 0 else _bounded(covered_probability / pi1[support]))
        holes.append(omitted_at)
    for degree in range(4):
        chains = []
        for vertices in combinations(range(1, 7), degree):
            if all(left in past[right] for left, right in pairwise((0, *vertices, 7))):
                support = sum(1 << bit_of[node] for node in vertices if node in bit_of)
                chains.append((vertices, support))
        scale = _bounded(F((-1) ** degree, 2 ** (degree + 1)) / density**degree)
        sequential_target = sum((coverage[support] for _, support in chains), F(0))
        public.append(
            {
                "degree": degree,
                "scale": _wire(scale),
                "target_count": len(chains),
                "target_coefficient": _wire(scale * len(chains)),
                "chains": [
                    {
                        "vertices": list(vertices),
                        "eligible_mask": support,
                        "pi1": _wire(pi1[support]),
                        "pif": _wire(pif[support]),
                        "path_coverage": _wire(coverage[support]),
                        "conditional_hole_masks": holes[support],
                    }
                    for vertices, support in chains
                ],
                "first_supported_count": sum(pi1[support] > 0 for _, support in chains),
                "final_supported_count": sum(pif[support] > 0 for _, support in chains),
                "sequential_coverage_target": _wire(sequential_target),
                "full_final_support": all(pif[support] > 0 for _, support in chains),
                "full_sequential_coverage": all(coverage[support] == 1 for _, support in chains),
            }
        )
        families.append(chains)
        scales.append(scale)
        targets.append(len(chains))
    return public, families, scales, targets


def _observation(mask, past, fixed, eligible):
    kept = sorted([*fixed, *(node for bit, node in enumerate(eligible) if mask & (1 << bit))])
    positions = {node: index for index, node in enumerate(kept)}
    observed = [[positions[node] for node in past[target] if node in positions] for target in kept]
    return kept, observed


def _final_estimates(families, number, pif):
    result = []
    for mask in range(number):
        counts, final, naive, omitted = [], [], [], []
        for chains in families:
            observed = [
                (vertices, support) for vertices, support in chains if mask & support == support
            ]
            counts.append(len(observed))
            final.append(
                _bounded(
                    sum((1 / pif[support] for _, support in observed if pif[support] > 0), F(0))
                )
            )
            naive.append(F(sum(4 ** support.bit_count() for _, support in observed)))
            omitted.append(sum(pif[support] == 0 for _, support in observed))
        result.append((counts, final, naive, omitted))
    return result


def _sequential_estimate(mask, intermediate, families, pi1, pi2):
    result, omitted = [], []
    for chains in families:
        value, missed = F(0), 0
        for _, support in chains:
            if mask & support != support:
                continue
            denominator = pi1[support] * pi2[intermediate][support]
            if denominator > 0:
                value += 1 / denominator
            else:
                missed += 1
        result.append(_bounded(value))
        omitted.append(missed)
    return result, omitted


def _first_rows(past, fixed, eligible, families, first, tokens, pi1, pi2):
    rows = []
    for mask, probability in enumerate(first):
        first_values, means, flags = [], [], []
        for chains in families:
            observed = [
                support for _, support in chains if mask & support == support and pi1[support] > 0
            ]
            first_values.append(_bounded(sum((1 / pi1[support] for support in observed), F(0))))
            means.append(
                _bounded(
                    sum((1 / pi1[support] for support in observed if pi2[mask][support] > 0), F(0))
                )
            )
            flags.append(all(pi2[mask][support] > 0 for support in observed))
        kept, observed_past = _observation(mask, past, fixed, eligible)
        rows.append(
            {
                "mask": mask,
                "probability": _wire(probability),
                "kept": kept,
                "past": observed_past,
                "policy_token": _wire(tokens[mask]),
                "first_estimates": _vector_wire(first_values),
                "sequential_conditional_mean": _vector_wire(means),
                "conditional_defect": _vector_wire(
                    [mean - comparator for mean, comparator in zip(means, first_values)]
                ),
                "conditional_full_support": flags,
                "repeat_probability": _wire(pi2[mask][1]),
            }
        )
    return rows


def _transcripts(conditional, first, families, pi1, pi2, final_estimates):
    rows, internal = [], []
    for intermediate, conditional_row in enumerate(conditional):
        conditional_mean = [F(0)] * 4
        for retained, probability in conditional_row:
            _, final, naive, omitted_final = final_estimates[retained]
            sequential, omitted_seq = _sequential_estimate(
                retained, intermediate, families, pi1, pi2
            )
            joint = _bounded(first[intermediate] * probability)
            estimates = (final, sequential, naive)
            rows.append(
                {
                    "stage1_mask": intermediate,
                    "final_mask": retained,
                    "conditional_probability": _wire(probability),
                    "joint_probability": _wire(joint),
                    "estimates": {
                        name: _vector_wire(vector) for name, vector in zip(_METHODS, estimates)
                    },
                    "omitted_terms": {
                        "final_joint": omitted_final,
                        "sequential_supported": omitted_seq,
                    },
                }
            )
            internal.append((intermediate, retained, probability, joint, estimates))
            for question, value in enumerate(sequential):
                conditional_mean[question] += probability * value
        # Check the independently derived conditional chain-indicator expression.
        for question, chains in enumerate(families):
            oracle = sum(
                (
                    1 / pi1[support]
                    for _, support in chains
                    if intermediate & support == support
                    and pi1[support] > 0
                    and pi2[intermediate][support] > 0
                ),
                F(0),
            )
            _require(
                conditional_mean[question] == oracle,
                "reference conditional expectation identity failed",
            )
    return rows, internal


def _centered_moments(weighted_vectors):
    _require(
        sum((weight for weight, _ in weighted_vectors), F(0)) == 1,
        "reference moment law must be normalized",
    )
    means = [
        sum((weight * vector[i] for weight, vector in weighted_vectors), F(0)) for i in range(4)
    ]
    covariance = [[F(0)] * 4 for _ in range(4)]
    for weight, vector in weighted_vectors:
        if weight == 0:
            continue
        centered = [value - mean for value, mean in zip(vector, means)]
        for first in range(4):
            for second in range(first, 4):
                covariance[first][second] += weight * centered[first] * centered[second]
    for first in range(4):
        for second in range(first, 4):
            value = _bounded(covariance[first][second])
            covariance[first][second] = covariance[second][first] = value
    return [_bounded(value) for value in means], covariance


def _final_rows(past, fixed, eligible, probabilities, estimates, transcripts):
    by_final = [[] for _ in probabilities]
    for _, retained, _, joint, vectors in transcripts:
        if joint > 0:
            by_final[retained].append((joint, vectors[1]))
    rows, conditional_moments, rb_law = [], [], []
    for retained, probability in enumerate(probabilities):
        kept, observed_past = _observation(retained, past, fixed, eligible)
        counts, final, naive, _ = estimates[retained]
        if probability == 0:
            means, covariance = None, None
        else:
            means, covariance = _centered_moments(
                [(joint / probability, vector) for joint, vector in by_final[retained]]
            )
            rb_law.append((probability, means))
        conditional_moments.append((means, covariance))
        rows.append(
            {
                "mask": retained,
                "probability": _wire(probability),
                "kept": kept,
                "past": observed_past,
                "chain_counts": counts,
                "final_estimate": _vector_wire(final),
                "naive_estimate": _vector_wire(naive),
                "conditional_sequential_mean": None if means is None else _vector_wire(means),
                "conditional_sequential_covariance": None
                if covariance is None
                else _matrix_wire(covariance),
            }
        )
    return rows, conditional_moments, rb_law


def _moment_wire(means, covariance, targets, scales):
    biases = [mean - target for mean, target in zip(means, targets)]
    return {
        "mean_counts": _vector_wire(means),
        "bias_counts": _vector_wire(biases),
        "covariance_counts": _matrix_wire(covariance),
        "mean_coefficients": _vector_wire([mean * scale for mean, scale in zip(means, scales)]),
        "bias_coefficients": _vector_wire([bias * scale for bias, scale in zip(biases, scales)]),
        "covariance_coefficients": _matrix_wire(
            [[covariance[i][j] * scales[i] * scales[j] for j in range(4)] for i in range(4)]
        ),
    }


def _moments(transcripts, rb_law, final_probabilities, conditional_moments, targets, scales):
    public, internal = {}, {}
    for method, name in enumerate(_METHODS):
        means, covariance = _centered_moments(
            [(joint, vectors[method]) for _, _, _, joint, vectors in transcripts]
        )
        internal[name] = (means, covariance)
        public[name] = _moment_wire(means, covariance, targets, scales)
    rb_means, rb_covariance = _centered_moments(rb_law)
    public["rb_sequential"] = _moment_wire(rb_means, rb_covariance, targets, scales)
    _require(
        rb_means == internal["sequential_supported"][0],
        "reference conditional averaging changed the mean",
    )
    expected_conditional = [[F(0)] * 4 for _ in range(4)]
    for probability, (_, covariance) in zip(final_probabilities, conditional_moments):
        if probability == 0:
            _require(
                covariance is None,
                "reference impossible final observation has a conditional covariance",
            )
            continue
        for first in range(4):
            for second in range(4):
                expected_conditional[first][second] += probability * covariance[first][second]
    sequential_covariance = internal["sequential_supported"][1]
    residual = [
        [
            sequential_covariance[i][j] - rb_covariance[i][j] - expected_conditional[i][j]
            for j in range(4)
        ]
        for i in range(4)
    ]
    _require(
        all(value == 0 for row in residual for value in row),
        "reference total covariance identity failed",
    )
    decomposition = {
        "sequential_covariance": _matrix_wire(sequential_covariance),
        "rb_covariance": _matrix_wire(rb_covariance),
        "mean_conditional_covariance": _matrix_wire(expected_conditional),
        "residual": _matrix_wire(residual),
    }
    return public, internal, decomposition


def _access(transcripts, tokens, pi2):
    result = {}
    for kind in _ACCESS_KEYS:
        representatives = {}
        estimator_collision, repeat_collision = None, None
        for intermediate, retained, _, joint, vectors in transcripts:
            if joint == 0:
                continue
            key = (
                retained
                if kind == "final_only"
                else (retained, tokens[intermediate])
                if kind == "policy_token"
                else (retained, intermediate)
            )
            current = (intermediate, retained, vectors[1], pi2[intermediate][1])
            if key not in representatives:
                representatives[key] = current
                continue
            previous = representatives[key]
            if estimator_collision is None:
                question = next(
                    (
                        i
                        for i, (left, right) in enumerate(zip(previous[2], current[2]))
                        if left != right
                    ),
                    None,
                )
                if question is not None:
                    estimator_collision = {
                        "question_index": question,
                        "left": {
                            "stage1_mask": previous[0],
                            "final_mask": previous[1],
                            "value": _wire(previous[2][question]),
                        },
                        "right": {
                            "stage1_mask": current[0],
                            "final_mask": current[1],
                            "value": _wire(current[2][question]),
                        },
                    }
            if repeat_collision is None and previous[3] != current[3]:
                repeat_collision = {
                    "question_index": 0,
                    "left": {
                        "stage1_mask": previous[0],
                        "final_mask": previous[1],
                        "value": _wire(previous[3]),
                    },
                    "right": {
                        "stage1_mask": current[0],
                        "final_mask": current[1],
                        "value": _wire(current[3]),
                    },
                }
        result[kind] = {
            "estimator": {
                "measurable": estimator_collision is None,
                "first_collision": estimator_collision,
            },
            "repeat_prediction": {
                "measurable": repeat_collision is None,
                "first_collision": repeat_collision,
            },
        }
    return result


def analyze(problem):
    """Return exact native-JSON analysis of one prescribed two-stage design."""
    profile, design = _parse(problem)
    past, fixed, eligible, density = _population(profile)
    first, conditional, final, tokens = _laws(design, len(eligible))
    pi1, pi2, pif = _inclusion_tables(first, conditional, final)
    questions, families, scales, targets = _questions(past, eligible, density, first, pi1, pi2, pif)
    final_estimates = _final_estimates(families, len(first), pif)
    first_rows = _first_rows(past, fixed, eligible, families, first, tokens, pi1, pi2)
    transcripts, transcript_data = _transcripts(
        conditional, first, families, pi1, pi2, final_estimates
    )
    final_rows, conditional_moments, rb_law = _final_rows(
        past, fixed, eligible, final, final_estimates, transcript_data
    )
    moments, internal_moments, decomposition = _moments(
        transcript_data,
        rb_law,
        final,
        conditional_moments,
        targets,
        scales,
    )
    _require(
        internal_moments["final_joint"][0]
        == [F(question["final_supported_count"]) for question in questions],
        "reference final supported-count expectation failed",
    )
    _require(
        internal_moments["sequential_supported"][0]
        == [F(question["sequential_coverage_target"]) for question in questions],
        "reference sequential path-coverage expectation failed",
    )
    result = {
        "profile": profile,
        "design": design,
        "density": _wire(density),
        "past": past,
        "fixed": fixed,
        "eligible": eligible,
        "stage1_probabilities": _vector_wire(first),
        "final_probabilities": _vector_wire(final),
        "stage1_inclusions": _vector_wire(pi1),
        "final_inclusions": _vector_wire(pif),
        "questions": questions,
        "first_rows": first_rows,
        "transcripts": transcripts,
        "final_rows": final_rows,
        "moments": moments,
        "variance_decomposition": decomposition,
        "access": _access(transcript_data, tokens, pi2),
        "counts": {
            "events": len(past),
            "eligible_events": len(eligible),
            "first_rows": len(first),
            "positive_first_rows": sum(probability > 0 for probability in first),
            "final_rows": len(final),
            "positive_final_rows": sum(probability > 0 for probability in final),
            "transcript_rows": len(transcripts),
            "positive_transcript_rows": sum(row[3] > 0 for row in transcript_data),
            "questions": len(questions),
            "chain_terms": sum(len(chains) for chains in families),
            "estimator_cells": len(transcripts) * 4 * 3,
        },
    }
    _native_json(result)
    return result
