"""Independent exact chain-indicator reference for QR-05E sampling fixtures.

The reference locally encodes the finite populations and sampling designs.
Sample estimates are sums of full-source chain indicators, independently of
the primary observed-order chain enumeration.  No prior or primary executor
is imported.  Source-chain support and the covariance identity are oracle
audit information, not missing information supplied to an observer.

Only ``analyze(wire)`` is the advertised bounded interface.  All masks survive,
including probability-zero rows and explicitly omitted zero-inclusion terms.
The scalar coefficients are not probabilities or quantum channels.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, pairwise
from math import comb

F = Fraction
_REGULAR_ORDERS = ("ferrers6", "standard_example3", "mesh3_center")
_REGULAR_DESIGNS = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2")
_METHODS = ("raw", "marginal_product", "uniform_rate", "joint_supported")


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _bounded(value):
    _require(type(value) is F, "reference arithmetic must remain rational")
    _require(
        abs(value.numerator).bit_length() <= 4096 and value.denominator.bit_length() <= 4096,
        "reference rational exceeds 4096-bit component bound",
    )
    return value


def _rational_wire(value):
    return str(_bounded(value))


def _native_json(value):
    if value is None or type(value) in (str, bool):
        return
    if type(value) is int:
        _require(abs(value).bit_length() <= 4096, "reference integer exceeds component bound")
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
    raise ValueError("reference output contains a non-native JSON value")


def _parse(wire):
    _require(
        type(wire) is dict and set(wire) == {"schema_version", "order", "design"},
        "reference problem must have exactly the specified keys",
    )
    _require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr05e-problem-v1",
        "reference schema is unsupported",
    )
    order, design = wire["order"], wire["design"]
    _require(type(order) is str and type(design) is str, "reference fixture names must be strings")
    permitted = (
        order in _REGULAR_ORDERS
        and design in _REGULAR_DESIGNS
        or order in ("ferrers6", "chain6")
        and design == "singleton"
    )
    _require(permitted, "reference order/design combination is unsupported")
    return order, design


def _population(name):
    if name == "mesh3_center":
        grid = tuple((i, j) for i in range(1, 4) for j in range(1, 4))
        past = [[]]
        for target, (u, v) in enumerate(grid):
            past.append(
                [
                    0,
                    *(
                        source + 1
                        for source, (a, b) in enumerate(grid)
                        if source != target and a <= u and b <= v
                    ),
                ]
            )
        past.append(list(range(10)))
        fixed, eligible = [0, 5, 10], [1, 2, 3, 4, 6, 7, 8, 9]
        probes = [
            {"name": "whole", "source": 0, "target": 10},
            {"name": "bottom_to_middle", "source": 0, "target": 5},
            {"name": "middle_to_top", "source": 5, "target": 10},
        ]
        density = F(18)
    else:
        past = [[]]
        for node in range(6):
            if name == "chain6":
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
                        if (left <= right if name == "ferrers6" else left != right)
                    ),
                ]
            past.append(row)
        past.append(list(range(7)))
        fixed, eligible = [0, 7], list(range(1, 7))
        probes = [{"name": "whole", "source": 0, "target": 7}]
        density = F(12)
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
    return past, fixed, eligible, probes, density


def _probabilities(design, eligible_count):
    full = (1 << eligible_count) - 1
    probabilities = []
    for mask in range(full + 1):
        if design == "identity":
            probability = F(int(mask == full))
        elif design == "iid_half":
            probability = F(1, 1 << eligible_count)
        elif design == "heterogeneous":
            probability = F(1)
            for bit in range(eligible_count):
                rate = F(1, 3) if bit % 2 == 0 else F(2, 3)
                probability *= rate if mask & (1 << bit) else 1 - rate
        elif design == "all_or_none":
            probability = F(1, 2) if mask in (0, full) else F(0)
        elif design == "fixed_size2":
            probability = F(1, comb(eligible_count, 2)) if mask.bit_count() == 2 else F(0)
        else:
            probability = F(1, eligible_count) if mask.bit_count() == 1 else F(0)
        probabilities.append(_bounded(probability))
    _require(
        sum(probabilities, F(0)) == 1 and all(value >= 0 for value in probabilities),
        "reference sampling design is not normalized",
    )
    return probabilities


def _inclusions(probabilities):
    table = []
    for required in range(len(probabilities)):
        table.append(
            _bounded(
                sum(
                    (
                        probability
                        for mask, probability in enumerate(probabilities)
                        if mask & required == required
                    ),
                    F(0),
                )
            )
        )
    _require(table[0] == 1, "reference empty-set inclusion differs from one")
    return table


def _source_questions(past, eligible, probes, density, inclusion):
    bit_of = {node: bit for bit, node in enumerate(eligible)}
    public, families, scales, targets = [], [], [], []
    for probe in probes:
        first, last = probe["source"], probe["target"]
        inside = tuple(node for node in past[last] if first in past[node])
        for degree in range(4):
            chains = []
            for vertices in combinations(inside, degree):
                full_path = (first, *vertices, last)
                if not all(a in past[b] for a, b in pairwise(full_path)):
                    continue
                mask = sum(1 << bit_of[node] for node in vertices if node in bit_of)
                chains.append((vertices, mask, inclusion[mask]))
            scale = _bounded(F((-1) ** degree, 2 ** (degree + 1)) / density**degree)
            target = len(chains)
            unsupported = [
                list(vertices) for vertices, _, probability in chains if probability == 0
            ]
            public.append(
                {
                    "probe": probe["name"],
                    "degree": degree,
                    "scale": _rational_wire(scale),
                    "target_count": target,
                    "target_coefficient": _rational_wire(scale * target),
                    "chains": [
                        {
                            "vertices": list(vertices),
                            "eligible_mask": mask,
                            "inclusion": _rational_wire(probability),
                        }
                        for vertices, mask, probability in chains
                    ],
                    "zero_inclusion_chains": unsupported,
                    "supported_count": target - len(unsupported),
                    "full_target_supported": not unsupported,
                }
            )
            families.append(chains)
            scales.append(scale)
            targets.append(target)
    return public, families, scales, targets


def _chain_weights(families, inclusion, eligible_count):
    marginals = [inclusion[1 << bit] for bit in range(eligible_count)]
    _require(all(value > 0 for value in marginals), "reference fixture has a zero vertex marginal")
    average = sum(marginals, F(0)) / eligible_count
    result = []
    for chains in families:
        row = []
        for _, mask, joint in chains:
            marginal_product = F(1)
            for bit in range(eligible_count):
                if mask & (1 << bit):
                    marginal_product *= marginals[bit]
            row.append(
                (
                    mask,
                    (
                        F(1),
                        _bounded(1 / marginal_product),
                        _bounded(1 / average ** mask.bit_count()),
                        None if joint == 0 else _bounded(1 / joint),
                    ),
                )
            )
        result.append(row)
    return result


def _cover_successors(past):
    result = [[] for _ in past]
    for target, row in enumerate(past):
        for source in row:
            if not any(source in past[middle] for middle in row):
                result[source].append(target)
    return result


def _hasse_reachability(kept, successors, probes):
    present = set(kept)
    reachable = []
    for probe in probes:
        seen = {probe["source"]}
        frontier = [probe["source"]]
        while frontier:
            source = frontier.pop()
            for target in successors[source]:
                if target in present and target not in seen:
                    seen.add(target)
                    frontier.append(target)
        reachable.append(probe["target"] in seen)
    return reachable


def _samples(past, fixed, eligible, probes, probabilities, chain_weights):
    successors = _cover_successors(past)
    public, estimates = [], {method: [] for method in _METHODS}
    observation_law = []
    mismatch_probability, first_mismatch = F(0), None
    for mask, probability in enumerate(probabilities):
        kept = sorted([*fixed, *(node for bit, node in enumerate(eligible) if mask & (1 << bit))])
        position = {node: index for index, node in enumerate(kept)}
        observed_past = [
            [position[ancestor] for ancestor in past[node] if ancestor in position] for node in kept
        ]
        counts, omitted = [], []
        by_method = [[] for _ in _METHODS]
        for chains in chain_weights:
            values = [F(0)] * len(_METHODS)
            chain_count, omitted_count = 0, 0
            for support, weights in chains:
                if mask & support != support:
                    continue
                chain_count += 1
                for method, weight in enumerate(weights):
                    if weight is None:
                        omitted_count += 1
                    else:
                        values[method] += weight
            counts.append(chain_count)
            omitted.append(omitted_count)
            for method, value in enumerate(values):
                by_method[method].append(_bounded(value))
        _require(
            probability == 0 or not any(omitted),
            "reference positive sample contains a zero-inclusion chain",
        )
        hasse = _hasse_reachability(kept, successors, probes)
        if probability > 0:
            observation_law.append(
                {"kept": kept, "past": observed_past, "probability": _rational_wire(probability)}
            )
            if not all(hasse):
                mismatch_probability += probability
                if first_mismatch is None:
                    first_mismatch = {
                        "mask": mask,
                        "kept": kept,
                        "probes": [
                            probe["name"] for probe, reached in zip(probes, hasse) if not reached
                        ],
                    }
        wire_estimates = {}
        for method, name in enumerate(_METHODS):
            estimates[name].append(by_method[method])
            wire_estimates[name] = [_rational_wire(value) for value in by_method[method]]
        public.append(
            {
                "mask": mask,
                "probability": _rational_wire(probability),
                "kept": kept,
                "observed_past": observed_past,
                "chain_counts": counts,
                "unsupported_observed_terms": omitted,
                "estimates": wire_estimates,
                "hasse_only_reachability": hasse,
            }
        )
    return (
        public,
        estimates,
        observation_law,
        {
            "mismatch_probability": _rational_wire(mismatch_probability),
            "first_mismatch": first_mismatch,
        },
    )


def _moments(probabilities, estimates, targets, scales):
    dimensions = len(targets)
    public, count_covariances = {}, {}
    for method in _METHODS:
        vectors = estimates[method]
        means = [
            _bounded(
                sum(
                    (
                        probability * vector[question]
                        for probability, vector in zip(probabilities, vectors)
                    ),
                    F(0),
                )
            )
            for question in range(dimensions)
        ]
        covariance = [[F(0)] * dimensions for _ in range(dimensions)]
        # Exact centered outer products, independently of raw-second-moment subtraction.
        for probability, vector in zip(probabilities, vectors):
            if probability == 0:
                continue
            centered = [value - mean for value, mean in zip(vector, means)]
            for first in range(dimensions):
                for second in range(first, dimensions):
                    covariance[first][second] += probability * centered[first] * centered[second]
        for first in range(dimensions):
            for second in range(first, dimensions):
                value = _bounded(covariance[first][second])
                covariance[first][second] = covariance[second][first] = value
        biases = [_bounded(mean - target) for mean, target in zip(means, targets)]
        exact_probabilities = [
            sum(
                (
                    probability
                    for probability, vector in zip(probabilities, vectors)
                    if vector[question] == targets[question]
                ),
                F(0),
            )
            for question in range(dimensions)
        ]
        vector_exact = sum(
            (
                probability
                for probability, vector in zip(probabilities, vectors)
                if all(value == target for value, target in zip(vector, targets))
            ),
            F(0),
        )
        coefficient_covariance = [
            [_bounded(covariance[i][j] * scales[i] * scales[j]) for j in range(dimensions)]
            for i in range(dimensions)
        ]
        public[method] = {
            "mean_counts": [_rational_wire(value) for value in means],
            "bias_counts": [_rational_wire(value) for value in biases],
            "covariance_counts": [[_rational_wire(value) for value in row] for row in covariance],
            "mean_coefficients": [
                _rational_wire(mean * scale) for mean, scale in zip(means, scales)
            ],
            "bias_coefficients": [
                _rational_wire(bias * scale) for bias, scale in zip(biases, scales)
            ],
            "covariance_coefficients": [
                [_rational_wire(value) for value in row] for row in coefficient_covariance
            ],
            "exact_target_probabilities": [_rational_wire(value) for value in exact_probabilities],
            "vector_exact_target_probability": _rational_wire(vector_exact),
        }
        count_covariances[method] = covariance
    return public, count_covariances


def _covariance_identity(families, inclusion):
    supported = [
        [(mask, probability) for _, mask, probability in chains if probability > 0]
        for chains in families
    ]
    result = []
    for first in supported:
        row = []
        for second in supported:
            value = F(0)
            for left, left_probability in first:
                for right, right_probability in second:
                    value += inclusion[left | right] / (left_probability * right_probability) - 1
            row.append(_bounded(value))
        result.append(row)
    return result


def analyze(wire):
    """Return complete native-JSON evidence for one of the seventeen fixtures."""
    order_name, design = _parse(wire)
    past, fixed, eligible, probes, density = _population(order_name)
    probabilities = _probabilities(design, len(eligible))
    inclusion = _inclusions(probabilities)
    questions, families, scales, targets = _source_questions(
        past, eligible, probes, density, inclusion
    )
    chain_weights = _chain_weights(families, inclusion, len(eligible))
    samples, estimates, observation_law, hasse_control = _samples(
        past,
        fixed,
        eligible,
        probes,
        probabilities,
        chain_weights,
    )
    moments, covariance = _moments(probabilities, estimates, targets, scales)
    identity = _covariance_identity(families, inclusion)
    _require(
        identity == covariance["joint_supported"],
        "reference joint-inclusion covariance identity failed",
    )
    supported_means = [F(question["supported_count"]) for question in questions]
    _require(
        [F(value) for value in moments["joint_supported"]["mean_counts"]] == supported_means,
        "reference supported-projection expectation identity failed",
    )
    result = {
        "order_name": order_name,
        "design": design,
        "density": _rational_wire(density),
        "past": past,
        "fixed": fixed,
        "eligible": eligible,
        "probes": probes,
        "inclusion_probabilities": [_rational_wire(value) for value in inclusion],
        "questions": questions,
        "samples": samples,
        "moments": moments,
        "joint_covariance_formula": [[_rational_wire(value) for value in row] for row in identity],
        "observation_law": observation_law,
        "hasse_control": hasse_control,
        "counts": {
            "events": len(past),
            "eligible_events": len(eligible),
            "mask_rows": len(samples),
            "positive_rows": sum(probability > 0 for probability in probabilities),
            "questions": len(questions),
            "chain_terms": sum(len(chains) for chains in families),
            "estimator_cells": len(samples) * len(questions) * len(_METHODS),
        },
    }
    _native_json(result)
    return result
