"""Exact two-stage diagnostics, with estimators formed only from observed orders."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, pairwise
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
METHODS = ("final_joint", "sequential_supported", "naive_quarter")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def wire(value):
    """Explicitly encode exact arithmetic; reject implicit JSON coercions."""
    if type(value) is F:
        require(
            max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
            "rational component bound",
        )
        return str(value)
    if type(value) is list:
        return [wire(item) for item in value]
    if type(value) is dict:
        require(all(type(key) is str for key in value), "string wire keys required")
        return {key: wire(item) for key, item in value.items()}
    require(value is None or type(value) in (bool, int, str), "native exact wire types required")
    if type(value) is int:
        require(abs(value).bit_length() <= 4096, "integer component bound")
    return value


def population(profile):
    if profile == "chain6":
        past = [list(range(j)) for j in range(8)]
    else:
        past = [[], [0], [0], [0]]
        for j in range(3):
            past.append(
                [
                    0,
                    *(
                        i + 1
                        for i in range(3)
                        if (i != j if profile == "standard_example3" else i <= j)
                    ),
                ]
            )
        past.append(list(range(7)))
    fixed = [0, 3, 7] if profile == "ferrers6_fixed" else [0, 7]
    eligible = [i for i in range(8) if i not in fixed]
    return past, fixed, eligible


def policy_token(design, stage1):
    if design == "parity_adaptive":
        return F(1, 3) if stage1.bit_count() % 2 == 0 else F(2, 3)
    if design == "parity_hole":
        return F(int(stage1.bit_count() % 2 == 0))
    return F(1, 2)


def second_probability(design, stage1, final):
    if final & stage1 != final:
        return F(0)
    if design == "common_coin":
        if stage1 == 0:
            return F(int(final == 0))
        return F(1, 2) if final in (0, stage1) else F(0)
    rate = policy_token(design, stage1)
    return rate ** final.bit_count() * (1 - rate) ** (stage1.bit_count() - final.bit_count())


def second_inclusion(design, stage1, support):
    if support & stage1 != support:
        return F(0)
    if support == 0:
        return F(1)
    if design == "common_coin":
        return F(1, 2)
    return policy_token(design, stage1) ** support.bit_count()


def observed_order(past, fixed, eligible, mask):
    kept = sorted([*fixed, *(v for i, v in enumerate(eligible) if mask & (1 << i))])
    local_past = [[i for i, vertex in enumerate(kept) if vertex in past[target]] for target in kept]
    return kept, local_past


def chain_vertices(past, source, target, degree):
    if source not in past[target]:
        return []
    internal = [i for i in past[target] if source in past[i]]
    return [
        list(vertices)
        for vertices in combinations(internal, degree)
        if all(a in past[b] for a, b in pairwise((source, *vertices, target)))
    ]


def support_mask(vertices, positions):
    return sum(1 << positions[vertex] for vertex in vertices if vertex in positions)


def observed_chain_supports(local_past, kept, positions):
    """No source inventory or target is accepted by this operational helper."""
    source, target = kept.index(0), kept.index(7)
    return [
        [
            support_mask([kept[i] for i in vertices], positions)
            for vertices in chain_vertices(local_past, source, target, degree)
        ]
        for degree in range(4)
    ]


def operational_estimates(observed_supports, stage1, design, pi1, pif):
    """Use observed final chains and design-only inclusion information."""
    estimates = {method: [] for method in METHODS}
    omitted = {method: [] for method in METHODS[:2]}
    for family in observed_supports:
        final_values, sequential_values = [], []
        for support in family:
            if pif[support] > 0:
                final_values.append(1 / pif[support])
            conditional = second_inclusion(design, stage1, support)
            if pi1[support] > 0 and conditional > 0:
                sequential_values.append(1 / (pi1[support] * conditional))
        estimates["final_joint"].append(sum(final_values, F(0)))
        estimates["sequential_supported"].append(sum(sequential_values, F(0)))
        estimates["naive_quarter"].append(sum((F(4 ** s.bit_count()) for s in family), F(0)))
        omitted["final_joint"].append(len(family) - len(final_values))
        omitted["sequential_supported"].append(len(family) - len(sequential_values))
    return estimates, omitted


def weighted_moments(weighted_vectors):
    """Weights are normalized design or conditional probabilities."""
    positive = [(weight, vector) for weight, vector in weighted_vectors if weight > 0]
    require(sum((weight for weight, _ in positive), F(0)) == 1, "moment weights not normalized")
    mean = [sum((weight * vector[i] for weight, vector in positive), F(0)) for i in range(4)]
    covariance = [
        [
            sum(
                (
                    weight * (vector[i] - mean[i]) * (vector[j] - mean[j])
                    for weight, vector in positive
                ),
                F(0),
            )
            for j in range(4)
        ]
        for i in range(4)
    ]
    return mean, covariance


def moment_report(weighted_vectors, targets, scales):
    mean, covariance = weighted_moments(weighted_vectors)
    bias = [mean[i] - targets[i] for i in range(4)]
    return {
        "mean_counts": mean,
        "bias_counts": bias,
        "covariance_counts": covariance,
        "mean_coefficients": [mean[i] * scales[i] for i in range(4)],
        "bias_coefficients": [bias[i] * scales[i] for i in range(4)],
        "covariance_coefficients": [
            [covariance[i][j] * scales[i] * scales[j] for j in range(4)] for i in range(4)
        ],
    }


def access_comparison(transcripts, design, key_name, repeat):
    representatives = {}
    first = None
    for row in transcripts:
        if row["joint_probability"] == 0:
            continue
        stage1, final = row["stage1_mask"], row["final_mask"]
        if key_name == "final_only":
            key = final
        elif key_name == "policy_token":
            key = (final, policy_token(design, stage1))
        else:
            key = (final, stage1)
        values = (
            [second_inclusion(design, stage1, 1)]
            if repeat
            else row["estimates"]["sequential_supported"]
        )
        if key not in representatives:
            representatives[key] = (stage1, final, values)
            continue
        previous_stage1, previous_final, previous_values = representatives[key]
        for index, (left, right) in enumerate(zip(previous_values, values, strict=True)):
            if left != right:
                first = {
                    "question_index": index,
                    "left": {
                        "stage1_mask": previous_stage1,
                        "final_mask": previous_final,
                        "value": left,
                    },
                    "right": {"stage1_mask": stage1, "final_mask": final, "value": right},
                }
                break
        if first is not None:
            break
    return {"measurable": first is None, "first_collision": first}


def analyze(problem):
    require(
        type(problem) is dict and set(problem) == {"schema_version", "profile", "design"},
        "exact problem fields required",
    )
    require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05f-problem-v1",
        "unsupported schema",
    )
    require(
        type(problem["profile"]) is str
        and type(problem["design"]) is str
        and (problem["profile"], problem["design"]) in CASES,
        "unsupported fixed combination",
    )
    profile, design = problem["profile"], problem["design"]
    past, fixed, eligible = population(profile)
    density, m = F(12), len(eligible)
    positions = {vertex: i for i, vertex in enumerate(eligible)}
    limit = 1 << m
    first_probabilities = (
        [F(1, comb(m, 2)) if mask.bit_count() == 2 else F(0) for mask in range(limit)]
        if design == "first_pair"
        else [F(1, limit)] * limit
    )
    pi1 = [
        sum(
            (p for stage1, p in enumerate(first_probabilities) if stage1 & support == support), F(0)
        )
        for support in range(limit)
    ]
    pif = [
        sum(
            (
                p * second_inclusion(design, stage1, support)
                for stage1, p in enumerate(first_probabilities)
            ),
            F(0),
        )
        for support in range(limit)
    ]

    # This cache contains only data in an observed induced order and the ID frame.
    observations, observed_supports = [], []
    for mask in range(limit):
        kept, local_past = observed_order(past, fixed, eligible, mask)
        observations.append((kept, local_past))
        observed_supports.append(observed_chain_supports(local_past, kept, positions))

    transcripts = []
    final_probabilities = [F(0)] * limit
    by_first, by_final = [[] for _ in range(limit)], [[] for _ in range(limit)]
    for stage1, first_probability in enumerate(first_probabilities):
        conditional_total = F(0)
        for final in range(limit):
            if final & stage1 != final:
                continue
            conditional = second_probability(design, stage1, final)
            conditional_total += conditional
            joint = first_probability * conditional
            estimates, omitted = operational_estimates(
                observed_supports[final], stage1, design, pi1, pif
            )
            row = {
                "stage1_mask": stage1,
                "final_mask": final,
                "conditional_probability": conditional,
                "joint_probability": joint,
                "estimates": estimates,
                "omitted_terms": omitted,
            }
            if joint > 0:
                require(
                    not any(omitted["final_joint"]) and not any(omitted["sequential_supported"]),
                    "positive transcript contains an impossible observed chain",
                )
            transcripts.append(row)
            by_first[stage1].append(row)
            by_final[final].append(row)
            final_probabilities[final] += joint
        require(conditional_total == 1, "conditional law not normalized")
    require(sum(final_probabilities, F(0)) == 1, "final law not normalized")
    require(
        pif
        == [
            sum(
                (p for final, p in enumerate(final_probabilities) if final & support == support),
                F(0),
            )
            for support in range(limit)
        ],
        "final inclusion composition",
    )

    first_rows = []
    for stage1, probability in enumerate(first_probabilities):
        kept, local_past = observations[stage1]
        first_estimates = [
            sum((1 / pi1[s] for s in family if pi1[s] > 0), F(0))
            for family in observed_supports[stage1]
        ]
        conditional_mean = [
            sum(
                (
                    row["conditional_probability"] * row["estimates"]["sequential_supported"][i]
                    for row in by_first[stage1]
                ),
                F(0),
            )
            for i in range(4)
        ]
        conditional_support = [
            not any(pi1[s] > 0 and second_inclusion(design, stage1, s) == 0 for s in family)
            for family in observed_supports[stage1]
        ]
        first_rows.append(
            {
                "mask": stage1,
                "probability": probability,
                "kept": kept,
                "past": local_past,
                "policy_token": policy_token(design, stage1),
                "first_estimates": first_estimates,
                "sequential_conditional_mean": conditional_mean,
                "conditional_defect": [conditional_mean[i] - first_estimates[i] for i in range(4)],
                "conditional_full_support": conditional_support,
                "repeat_probability": second_inclusion(design, stage1, 1),
            }
        )

    final_rows = []
    for final, probability in enumerate(final_probabilities):
        kept, local_past = observations[final]
        final_estimates, _ = operational_estimates(
            observed_supports[final], final, design, pi1, pif
        )
        conditional_mean, conditional_covariance = (None, None)
        if probability > 0:
            conditional_mean, conditional_covariance = weighted_moments(
                [
                    (
                        row["joint_probability"] / probability,
                        row["estimates"]["sequential_supported"],
                    )
                    for row in by_final[final]
                ]
            )
        final_rows.append(
            {
                "mask": final,
                "probability": probability,
                "kept": kept,
                "past": local_past,
                "chain_counts": [len(family) for family in observed_supports[final]],
                "final_estimate": final_estimates["final_joint"],
                "naive_estimate": final_estimates["naive_quarter"],
                "conditional_sequential_mean": conditional_mean,
                "conditional_sequential_covariance": conditional_covariance,
            }
        )

    # Only this audit inventory uses full-source chain sets and target values.
    questions = []
    for degree in range(4):
        source_family = chain_vertices(past, 0, 7, degree)
        entries = []
        for vertices in source_family:
            support = support_mask(vertices, positions)
            covered = sum(
                (
                    p
                    for stage1, p in enumerate(first_probabilities)
                    if stage1 & support == support and second_inclusion(design, stage1, support) > 0
                ),
                F(0),
            )
            coverage = covered / pi1[support] if pi1[support] > 0 else F(0)
            entries.append(
                {
                    "vertices": vertices,
                    "eligible_mask": support,
                    "pi1": pi1[support],
                    "pif": pif[support],
                    "path_coverage": coverage,
                    "conditional_hole_masks": [
                        stage1
                        for stage1, p in enumerate(first_probabilities)
                        if p > 0
                        and stage1 & support == support
                        and second_inclusion(design, stage1, support) == 0
                    ],
                }
            )
        scale = F((-1) ** degree, 2 ** (degree + 1)) / density**degree
        questions.append(
            {
                "degree": degree,
                "scale": scale,
                "target_count": len(source_family),
                "target_coefficient": scale * len(source_family),
                "chains": entries,
                "first_supported_count": sum(c["pi1"] > 0 for c in entries),
                "final_supported_count": sum(c["pif"] > 0 for c in entries),
                "sequential_coverage_target": sum((c["path_coverage"] for c in entries), F(0)),
                "full_final_support": all(c["pif"] > 0 for c in entries),
                "full_sequential_coverage": all(c["path_coverage"] == 1 for c in entries),
            }
        )
    targets = [F(q["target_count"]) for q in questions]
    scales = [q["scale"] for q in questions]
    moments = {
        method: moment_report(
            [(row["joint_probability"], row["estimates"][method]) for row in transcripts],
            targets,
            scales,
        )
        for method in METHODS
    }
    moments["rb_sequential"] = moment_report(
        [
            (row["probability"], row["conditional_sequential_mean"])
            for row in final_rows
            if row["probability"] > 0
        ],
        targets,
        scales,
    )
    require(
        moments["final_joint"]["mean_counts"] == [F(q["final_supported_count"]) for q in questions],
        "final supported expectation",
    )
    require(
        moments["sequential_supported"]["mean_counts"]
        == [q["sequential_coverage_target"] for q in questions],
        "sequential path-coverage expectation",
    )
    require(
        moments["rb_sequential"]["mean_counts"] == moments["sequential_supported"]["mean_counts"],
        "conditional averaging changed the mean",
    )
    seq_cov = moments["sequential_supported"]["covariance_counts"]
    rb_cov = moments["rb_sequential"]["covariance_counts"]
    mean_conditional = [
        [
            sum(
                (
                    row["probability"] * row["conditional_sequential_covariance"][i][j]
                    for row in final_rows
                    if row["probability"] > 0
                ),
                F(0),
            )
            for j in range(4)
        ]
        for i in range(4)
    ]
    residual = [
        [seq_cov[i][j] - rb_cov[i][j] - mean_conditional[i][j] for j in range(4)] for i in range(4)
    ]
    require(not any(value for row in residual for value in row), "total covariance decomposition")
    access = {
        key: {
            "estimator": access_comparison(transcripts, design, key, False),
            "repeat_prediction": access_comparison(transcripts, design, key, True),
        }
        for key in ("final_only", "policy_token", "full_stage1")
    }
    return wire(
        {
            "profile": profile,
            "design": design,
            "density": density,
            "past": past,
            "fixed": fixed,
            "eligible": eligible,
            "stage1_probabilities": first_probabilities,
            "final_probabilities": final_probabilities,
            "stage1_inclusions": pi1,
            "final_inclusions": pif,
            "questions": questions,
            "first_rows": first_rows,
            "transcripts": transcripts,
            "final_rows": final_rows,
            "moments": moments,
            "variance_decomposition": {
                "sequential_covariance": seq_cov,
                "rb_covariance": rb_cov,
                "mean_conditional_covariance": mean_conditional,
                "residual": residual,
            },
            "access": access,
            "counts": {
                "events": len(past),
                "eligible_events": m,
                "first_rows": limit,
                "positive_first_rows": sum(p > 0 for p in first_probabilities),
                "final_rows": limit,
                "positive_final_rows": sum(p > 0 for p in final_probabilities),
                "transcript_rows": len(transcripts),
                "positive_transcript_rows": sum(
                    row["joint_probability"] > 0 for row in transcripts
                ),
                "questions": 4,
                "chain_terms": sum(q["target_count"] for q in questions),
                "estimator_cells": len(transcripts) * 4 * len(METHODS),
            },
        }
    )
