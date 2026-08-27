"""Multiscale, source-disjoint discovery run for the first 512 zeta zeros.

The validated extension supplies the numerical admission gate.  This module
then divides the admitted critical-line roots into eight *disjoint* 64-root
blocks. Blocks one through six are used for model comparison; the highest two
are withheld from this fit and used only for predictive scoring. They are not
historically fresh: the earlier validated-extension run summarized a window
overlapping block eight, although that posterior is not consumed here.

The statistical families below are deliberately modest reference families,
not propositions about RH.  They use exponential spacings for Poisson and the
generalized Wigner density

    p_beta(s) proportional to s**beta exp(-b_beta s**2), E[s] = 1,

as deterministic synthetic calibration targets.  ``finite_height`` and
``overrigid`` are beta alternatives, not derived finite-height zeta laws.
Deleted-root and jitter attacks test whether the histogram evidence can notice
two important scanner failure modes.
"""

from __future__ import annotations

import bisect
import hashlib
import json
import math
import random
from collections.abc import Mapping, Sequence
from typing import Optional

from det8.models.examples.riemann_validated_extension import (
    run_validated_riemann_extension,
)
from det8.models.examples.riemann_zero_search import (
    critical_line_zeros,
    riemann_siegel_theta,
)

try:  # The general evidence layer may be installed independently.
    from det8.models.relational_evidence import (  # type: ignore
        DirichletMultinomial as _EvidenceDirichletMultinomial,
        EVIDENCE_POSTERIOR_WARNING as _EVIDENCE_POSTERIOR_WARNING,
        OPEN_EVIDENCE_NAME as _OPEN_EVIDENCE_NAME,
        EvidenceHypothesis as _EvidenceHypothesis,
        EvidenceLedger as _EvidenceLedger,
        EvidenceRecord as _EvidenceRecord,
        evidence_payload_digest as _evidence_payload_digest,
        initialize_evidence_posterior as _initialize_evidence_posterior,
        update_evidence_posterior as _update_evidence_posterior,
    )
except (ImportError, AttributeError):  # pragma: no cover - fallback is tested by execution.
    _EvidenceDirichletMultinomial = None
    _EVIDENCE_POSTERIOR_WARNING = None
    _OPEN_EVIDENCE_NAME = "M_bottom"
    _EvidenceHypothesis = None
    _EvidenceLedger = None
    _EvidenceRecord = None
    _evidence_payload_digest = None
    _initialize_evidence_posterior = None
    _update_evidence_posterior = None


RIEMANN_MULTISCALE_WARNING = (
    "These observables describe 512 numerically certified sign-changing zeros "
    "on Re(s)=1/2. Synthetic family support is finite-record predictive evidence, "
    "not a probability of RH, not an off-line zero search, and not a rigorous "
    "interval or Turing-method certificate."
)

BLOCK_SIZE = 64
TRAINING_BLOCKS = 6
HOLDOUT_BLOCKS = 2
NUMBER_VARIANCE_SCALES = (1.0, 2.0, 4.0, 8.0)
PAIR_CORRELATION_BINS = ((0.0, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, 4.0))
SPACING_HISTOGRAM_EDGES = (
    0.0,
    0.35,
    0.55,
    0.75,
    1.0,
    1.3,
    1.7,
    2.2,
    math.inf,
)
REFERENCE_FAMILIES = (
    "poisson",
    "gue_beta_2",
    "finite_height_beta_3",
    "overrigid_beta_5",
    "deleted_root_attack",
    "jittered_root_attack",
)
CLEAN_FAMILIES = REFERENCE_FAMILIES[:4]
ATTACK_FAMILIES = REFERENCE_FAMILIES[4:]


def _mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("a mean requires at least one value")
    return sum(values) / len(values)


def _sample_variance(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    center = _mean(values)
    return sum((value - center) ** 2 for value in values) / (len(values) - 1)


def _normalize_spacings(spacings: Sequence[float]) -> tuple[float, ...]:
    if not spacings or any(value <= 0.0 for value in spacings):
        raise ValueError("spacings must be a nonempty positive sequence")
    center = _mean(spacings)
    return tuple(value / center for value in spacings)


def _positions_from_spacings(spacings: Sequence[float]) -> tuple[float, ...]:
    position = 0.0
    positions = [position]
    for spacing in spacings:
        position += spacing
        positions.append(position)
    return tuple(positions)


def _histogram_counts(spacings: Sequence[float]) -> tuple[int, ...]:
    counts = [0] * (len(SPACING_HISTOGRAM_EDGES) - 1)
    for spacing in spacings:
        index = bisect.bisect_right(SPACING_HISTOGRAM_EDGES, spacing) - 1
        index = min(max(index, 0), len(counts) - 1)
        counts[index] += 1
    return tuple(counts)


def _window_origins(span: float, scale: float, count: int = 48) -> tuple[float, ...]:
    available = span - scale
    if available <= 0.0:
        return ()
    # Midpoint origins avoid giving either finite boundary a special weight.
    return tuple(available * (index + 0.5) / count for index in range(count))


def _number_variance(
    positions: Sequence[float], scale: float
) -> tuple[float, float]:
    origins = _window_origins(positions[-1] - positions[0], scale)
    if not origins:
        return math.nan, math.nan
    counts = []
    for origin in origins:
        left = bisect.bisect_left(positions, origin)
        right = bisect.bisect_left(positions, origin + scale)
        counts.append(right - left)
    return _mean(tuple((count - scale) ** 2 for count in counts)), _mean(counts)


def _delta3_for_window(
    positions: Sequence[float], origin: float, scale: float, grid_size: int = 40
) -> float:
    xs = tuple(scale * (index + 0.5) / grid_size for index in range(grid_size))
    before = bisect.bisect_right(positions, origin)
    staircase = tuple(
        bisect.bisect_right(positions, origin + x) - before for x in xs
    )
    x_mean = _mean(xs)
    y_mean = _mean(staircase)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    slope = sum(
        (x - x_mean) * (y - y_mean) for x, y in zip(xs, staircase)
    ) / denominator
    intercept = y_mean - slope * x_mean
    return _mean(
        tuple(
            (y - (intercept + slope * x)) ** 2
            for x, y in zip(xs, staircase)
        )
    )


def _spectral_rigidity(positions: Sequence[float], scale: float) -> float:
    origins = _window_origins(positions[-1] - positions[0], scale, count=24)
    if not origins:
        return math.nan
    return _mean(tuple(_delta3_for_window(positions, origin, scale) for origin in origins))


def _pair_correlation(positions: Sequence[float]) -> dict[str, float]:
    span = positions[-1] - positions[0]
    counts = [0] * len(PAIR_CORRELATION_BINS)
    for left_index, left in enumerate(positions):
        for right in positions[left_index + 1 :]:
            distance = right - left
            if distance >= PAIR_CORRELATION_BINS[-1][1]:
                break
            for index, (lower, upper) in enumerate(PAIR_CORRELATION_BINS):
                if lower <= distance < upper:
                    counts[index] += 1
                    break
    summary = {}
    for count, (lower, upper) in zip(counts, PAIR_CORRELATION_BINS):
        # For a unit-rate Poisson process in a finite interval, the expected
        # unordered pair count is integral_lower^upper (span-r) dr.
        clipped_upper = min(upper, span)
        clipped_lower = min(lower, clipped_upper)
        exposure = (
            span * (clipped_upper - clipped_lower)
            - 0.5 * (clipped_upper**2 - clipped_lower**2)
        )
        summary[f"{lower:g}_{upper:g}"] = count / exposure if exposure > 0 else math.nan
    return summary


def spacing_observables(spacings: Sequence[float]) -> dict[str, object]:
    """Return all block observables from already-unfolded positive spacings."""

    normalized = _normalize_spacings(spacings)
    positions = _positions_from_spacings(normalized)
    ratios = tuple(
        min(left, right) / max(left, right)
        for left, right in zip(normalized, normalized[1:])
    )
    ratio_mean = _mean(ratios)
    ratio_se = math.sqrt(_sample_variance(ratios) / len(ratios))
    number_variance = {}
    delta3 = {}
    number_mean = {}
    for scale in NUMBER_VARIANCE_SCALES:
        variance, count_mean = _number_variance(positions, scale)
        key = f"L={scale:g}"
        number_variance[key] = variance
        number_mean[key] = count_mean
        delta3[key] = _spectral_rigidity(positions, scale)
    return {
        "gap_count": len(normalized),
        "adjacent_gap_ratio_mean": ratio_mean,
        "adjacent_gap_ratio_standard_error": ratio_se,
        "unfolded_spacing_variance": _sample_variance(normalized),
        "small_gap_fraction_below_0.5": (
            sum(value < 0.5 for value in normalized) / len(normalized)
        ),
        "number_variance": number_variance,
        "number_count_mean": number_mean,
        "approximate_delta3": delta3,
        "pair_correlation_over_poisson": _pair_correlation(positions),
        "maximum_normalized_gap": max(normalized),
        "large_gap_fraction_above_2": (
            sum(value > 2.0 for value in normalized) / len(normalized)
        ),
        "spacing_histogram_counts": _histogram_counts(normalized),
    }


def zero_block_observables(
    roots: Sequence[float], block_index: int
) -> dict[str, object]:
    if len(roots) != BLOCK_SIZE:
        raise ValueError(f"each block must contain exactly {BLOCK_SIZE} roots")
    if block_index < 1:
        raise ValueError("block index is one based")
    smooth_positions = tuple(
        1.0 + riemann_siegel_theta(height) / math.pi for height in roots
    )
    spacings = tuple(
        right - left for left, right in zip(smooth_positions, smooth_positions[1:])
    )
    observables = spacing_observables(spacings)
    first_index = (block_index - 1) * BLOCK_SIZE + 1
    last_index = first_index + BLOCK_SIZE - 1
    digest = hashlib.sha256(
        "\n".join(f"{height:.15f}" for height in roots).encode("ascii")
    ).hexdigest()
    return {
        "block": block_index,
        "partition": "training" if block_index <= TRAINING_BLOCKS else "locked_holdout",
        "first_zero_index": first_index,
        "last_zero_index": last_index,
        "first_height": roots[0],
        "last_height": roots[-1],
        "source_ids": tuple(f"riemann-zero-{index}" for index in range(first_index, last_index + 1)),
        "source_digest": digest,
        **observables,
    }


def _generalized_wigner_spacing(beta: float, rng: random.Random) -> float:
    if beta <= -1.0:
        raise ValueError("generalized-Wigner beta must exceed -1")
    shape = 0.5 * (beta + 1.0)
    b = (math.gamma(0.5 * (beta + 2.0)) / math.gamma(shape)) ** 2
    return math.sqrt(rng.gammavariate(shape, 1.0) / b)


def _synthetic_spacings(label: str, gap_count: int, rng: random.Random) -> tuple[float, ...]:
    if label == "poisson":
        return tuple(rng.expovariate(1.0) for _ in range(gap_count))
    beta_by_label = {
        "gue_beta_2": 2.0,
        "finite_height_beta_3": 3.0,
        "overrigid_beta_5": 5.0,
    }
    if label in beta_by_label:
        return tuple(
            _generalized_wigner_spacing(beta_by_label[label], rng)
            for _ in range(gap_count)
        )
    if label == "deleted_root_attack":
        # Generate one extra gap and remove one internal synthetic root.  Its
        # two incident gaps merge, preserving the requested output length.
        gaps = [
            _generalized_wigner_spacing(2.0, rng) for _ in range(gap_count + 1)
        ]
        removed = rng.randrange(1, gap_count + 1)
        return tuple(gaps[: removed - 1] + [gaps[removed - 1] + gaps[removed]] + gaps[removed + 1 :])
    if label == "jittered_root_attack":
        gaps = [_generalized_wigner_spacing(2.0, rng) for _ in range(gap_count)]
        positions = list(_positions_from_spacings(gaps))
        for index in range(1, len(positions) - 1):
            positions[index] += rng.gauss(0.0, 0.16)
        positions.sort()
        attacked = tuple(
            right - left for left, right in zip(positions, positions[1:])
        )
        # Sorting almost surely leaves positive gaps; guard pathological RNG
        # collisions without silently changing the number of observations.
        return tuple(max(value, 1.0e-9) for value in attacked)
    raise ValueError(f"unknown synthetic family {label}")


def _log_dirichlet_multinomial(
    counts: Sequence[int], concentration: Sequence[float]
) -> float:
    if len(counts) != len(concentration) or any(count < 0 for count in counts):
        raise ValueError("counts and concentration must have matching valid dimensions")
    trials = sum(counts)
    if _EvidenceDirichletMultinomial is not None:
        distribution = _EvidenceDirichletMultinomial(
            trials=trials,
            concentration=tuple(concentration),
        )
        return float(distribution.log_prob(tuple(counts)))
    alpha_total = sum(concentration)
    return (
        math.lgamma(trials + 1)
        - sum(math.lgamma(count + 1) for count in counts)
        + math.lgamma(alpha_total)
        - math.lgamma(alpha_total + trials)
        + sum(
            math.lgamma(alpha + count) - math.lgamma(alpha)
            for alpha, count in zip(concentration, counts)
        )
    )


def _prototype_probabilities(
    *, seed: int, blocks_per_family: int
) -> dict[str, tuple[float, ...]]:
    prototypes = {}
    for family_index, family in enumerate(REFERENCE_FAMILIES):
        rng = random.Random(seed + 100_003 * family_index)
        counts = [0.5] * (len(SPACING_HISTOGRAM_EDGES) - 1)
        for _ in range(blocks_per_family):
            spacings = _synthetic_spacings(family, BLOCK_SIZE - 1, rng)
            histogram = _histogram_counts(_normalize_spacings(spacings))
            counts = [left + right for left, right in zip(counts, histogram)]
        total = sum(counts)
        prototypes[family] = tuple(value / total for value in counts)
    return prototypes


def _softmax(log_weights: Mapping[str, float]) -> dict[str, float]:
    maximum = max(log_weights.values())
    raw = {name: math.exp(value - maximum) for name, value in log_weights.items()}
    total = sum(raw.values())
    return {name: value / total for name, value in raw.items()}


def _score_training_sequence(
    histograms: Sequence[Sequence[int]],
    prototypes: Mapping[str, Sequence[float]],
    *,
    prototype_strength: float,
) -> tuple[dict[str, float], dict[str, tuple[float, ...]], tuple[dict[str, object], ...]]:
    concentrations = {
        family: tuple(1.0 + prototype_strength * probability for probability in probabilities)
        for family, probabilities in prototypes.items()
    }
    scores = {family: 0.0 for family in prototypes}
    trace = []
    for block_index, histogram in enumerate(histograms, 1):
        increments = {}
        for family in prototypes:
            increment = _log_dirichlet_multinomial(histogram, concentrations[family])
            increments[family] = increment
            scores[family] += increment
            concentrations[family] = tuple(
                alpha + count for alpha, count in zip(concentrations[family], histogram)
            )
        trace.append(
            {
                "training_block": block_index,
                "log_predictive_increment": increments,
                "posterior": _softmax(scores),
            }
        )
    return scores, concentrations, tuple(trace)


def _score_locked_holdout(
    histograms: Sequence[Sequence[int]],
    concentrations: Mapping[str, Sequence[float]],
    training_posterior: Mapping[str, float],
) -> dict[str, object]:
    family_scores = {family: 0.0 for family in concentrations}
    per_block = []
    for offset, histogram in enumerate(histograms, 1):
        block_scores = {
            family: _log_dirichlet_multinomial(histogram, alpha)
            for family, alpha in concentrations.items()
        }
        for family, score in block_scores.items():
            family_scores[family] += score
        mixture_terms = {
            family: math.log(max(training_posterior[family], 1.0e-300)) + score
            for family, score in block_scores.items()
        }
        maximum = max(mixture_terms.values())
        mixture_score = maximum + math.log(
            sum(math.exp(value - maximum) for value in mixture_terms.values())
        )
        per_block.append(
            {
                "holdout_block": TRAINING_BLOCKS + offset,
                "family_log_scores": block_scores,
                "locked_mixture_log_score": mixture_score,
            }
        )
    ordered = sorted(family_scores, key=family_scores.get, reverse=True)
    return {
        "family_log_scores": family_scores,
        "best_family": ordered[0],
        "best_over_second_log_score_margin": (
            family_scores[ordered[0]] - family_scores[ordered[1]]
        ),
        "per_block": tuple(per_block),
        "parameters_updated_on_holdout": False,
        "posterior_updated_on_holdout": False,
    }


def _run_shared_evidence_posterior(
    blocks: Sequence[Mapping[str, object]],
    prototypes: Mapping[str, Sequence[float]],
    *,
    prototype_strength: float,
) -> Optional[dict[str, object]]:
    """Assimilate training blocks through the likelihood-agnostic RET layer."""

    required = (
        _EvidenceDirichletMultinomial,
        _EvidenceHypothesis,
        _EvidenceRecord,
        _initialize_evidence_posterior,
        _update_evidence_posterior,
    )
    if any(value is None for value in required):
        return None

    def predictive(action, state):
        trials = int(action.metadata.get("trials", BLOCK_SIZE - 1))
        return _EvidenceDirichletMultinomial(
            trials=trials,
            concentration=tuple(state),
        )

    def update_state(state, record, distribution):
        del distribution
        return tuple(
            alpha + count for alpha, count in zip(state, record.observation)
        )

    hypotheses = []
    for family, probabilities in prototypes.items():
        initial = tuple(
            1.0 + prototype_strength * probability for probability in probabilities
        )
        hypotheses.append(
            _EvidenceHypothesis(
                name=family,
                family=family,
                predictive=predictive,
                initial_state=initial,
                state_update=update_state,
                metadata={"synthetic_reference": True},
            )
        )
    dimension = len(SPACING_HISTOGRAM_EDGES) - 1
    open_hypothesis = _EvidenceHypothesis(
        name=_OPEN_EVIDENCE_NAME,
        family="model_inadequate",
        predictive=predictive,
        initial_state=tuple(1.0 for _ in range(dimension)),
        state_update=update_state,
        robust=True,
        metadata={"role": "broad adaptive histogram"},
    )
    posterior = _initialize_evidence_posterior(
        hypotheses,
        open_hypothesis,
        complexity_penalty=0.0,
        open_prior=0.03,
    )
    trace = []
    previous_scores = dict(posterior.cumulative_log_scores)
    for block in blocks:
        observation = tuple(block["spacing_histogram_counts"])
        assert _evidence_payload_digest is not None
        record = _EvidenceRecord(
            record_id=f"riemann-multiscale-training-{block['block']}",
            source_ids=tuple(block["source_ids"]),
            action="riemann_multiscale_64_zero_block",
            coordinate=float(block["first_height"]),
            digest=_evidence_payload_digest(observation),
            family="spacing_histogram",
            scope="training",
            observation=observation,
            metadata={
                "trials": BLOCK_SIZE - 1,
                "first_zero_index": int(block["first_zero_index"]),
                "last_zero_index": int(block["last_zero_index"]),
                "source_digest": str(block["source_digest"]),
            },
            joint=False,
        )
        posterior = _update_evidence_posterior(posterior, record)
        increments = {
            name: posterior.cumulative_log_scores[name] - previous_scores[name]
            for name in posterior.cumulative_log_scores
        }
        previous_scores = dict(posterior.cumulative_log_scores)
        trace.append(
            {
                "training_block": int(block["block"]),
                "log_predictive_increment": increments,
                "posterior": dict(posterior.weights),
                "mixture_prequential_log_score": posterior.mixture_prequential_log_score,
            }
        )
    return {
        "backend": "det8.models.relational_evidence.EvidencePosterior",
        "posterior": dict(posterior.weights),
        "states": {
            name: tuple(state) for name, state in posterior.states.items()
        },
        "cumulative_log_scores": dict(posterior.cumulative_log_scores),
        "mixture_prequential_log_score": posterior.mixture_prequential_log_score,
        "prequential_trace": tuple(trace),
        "ledger_record_count": len(posterior.ledger.records),
        "ledger_source_count": len(posterior.ledger.source_ids),
        "warning": _EVIDENCE_POSTERIOR_WARNING,
    }


def synthetic_recovery_calibration(
    *,
    prototypes: Mapping[str, Sequence[float]],
    seed: int = 91_771,
    trials_per_family: int = 24,
    prototype_strength: float = 192.0,
) -> dict[str, object]:
    """Run deterministic family recovery and scanner-attack challenges."""

    if trials_per_family < 2:
        raise ValueError("calibration requires at least two trials per family")
    confusion = {
        truth: {prediction: 0 for prediction in REFERENCE_FAMILIES}
        for truth in REFERENCE_FAMILIES
    }
    holdout_wins = {truth: 0 for truth in REFERENCE_FAMILIES}
    attack_detection_count = 0
    attack_trials = 0
    for truth_index, truth in enumerate(REFERENCE_FAMILIES):
        for trial in range(trials_per_family):
            rng = random.Random(seed + 1_000_003 * truth_index + 7_919 * trial)
            histograms = tuple(
                _histogram_counts(
                    _normalize_spacings(
                        _synthetic_spacings(truth, BLOCK_SIZE - 1, rng)
                    )
                )
                for _ in range(TRAINING_BLOCKS + HOLDOUT_BLOCKS)
            )
            training_scores, concentrations, _ = _score_training_sequence(
                histograms[:TRAINING_BLOCKS],
                prototypes,
                prototype_strength=prototype_strength,
            )
            posterior = _softmax(training_scores)
            predicted = max(posterior, key=posterior.get)
            confusion[truth][predicted] += 1
            holdout = _score_locked_holdout(
                histograms[TRAINING_BLOCKS:], concentrations, posterior
            )
            if holdout["best_family"] == truth:
                holdout_wins[truth] += 1
            if truth in ATTACK_FAMILIES:
                attack_trials += 1
                attack_detection_count += int(predicted in ATTACK_FAMILIES)

    recovery_rates = {
        truth: confusion[truth][truth] / trials_per_family
        for truth in REFERENCE_FAMILIES
    }
    holdout_recovery_rates = {
        truth: holdout_wins[truth] / trials_per_family
        for truth in REFERENCE_FAMILIES
    }
    clean_correct = sum(confusion[truth][truth] for truth in CLEAN_FAMILIES)
    return {
        "seed": seed,
        "trials_per_family": trials_per_family,
        "confusion": confusion,
        "training_recovery_rate_by_family": recovery_rates,
        "locked_holdout_winner_rate_by_family": holdout_recovery_rates,
        "aggregate_clean_family_recovery_rate": (
            clean_correct / (len(CLEAN_FAMILIES) * trials_per_family)
        ),
        "attack_detection_rate": attack_detection_count / attack_trials,
        "calibration_gate": {
            "clean_recovery_at_least_0.75": (
                clean_correct / (len(CLEAN_FAMILIES) * trials_per_family) >= 0.75
            ),
            "attack_detection_at_least_0.75": (
                attack_detection_count / attack_trials >= 0.75
            ),
        },
    }


def _build_evidence_ledger(blocks: Sequence[Mapping[str, object]]) -> dict[str, object]:
    """Record block provenance, using the shared immutable ledger when present."""

    seen_sources: set[str] = set()
    overlap = []
    for block in blocks:
        for source in block["source_ids"]:
            if source in seen_sources:
                overlap.append(source)
            seen_sources.add(source)
    fallback = {
        "backend": "local_source_disjoint_manifest",
        "record_count": len(blocks),
        "unique_source_count": len(seen_sources),
        "overlapping_source_ids": tuple(overlap),
        "source_disjoint": not overlap,
    }
    if _EvidenceLedger is None or _EvidenceRecord is None:
        return fallback
    try:
        ledger = _EvidenceLedger()
        for block in blocks:
            observation = tuple(block["spacing_histogram_counts"])
            assert _evidence_payload_digest is not None
            record = _EvidenceRecord(
                record_id=f"riemann-multiscale-block-{block['block']}",
                source_ids=tuple(block["source_ids"]),
                action="riemann_multiscale_64_zero_block",
                coordinate=float(block["first_height"]),
                digest=_evidence_payload_digest(observation),
                family="dirichlet_multinomial",
                scope=str(block["partition"]),
                observation=observation,
                metadata={
                    "first_zero_index": int(block["first_zero_index"]),
                    "last_zero_index": int(block["last_zero_index"]),
                    "source_digest": str(block["source_digest"]),
                },
                joint=False,
            )
            ledger = ledger.append(record)
        return {
            **fallback,
            "backend": "det8.models.relational_evidence.EvidenceLedger",
            "external_ledger_record_count": len(ledger.records),
        }
    except (TypeError, ValueError, AttributeError) as error:
        return {
            **fallback,
            "backend": "local_source_disjoint_manifest_after_external_api_rejection",
            "external_api_error": str(error),
        }


def _aggregate_actual(blocks: Sequence[Mapping[str, object]]) -> dict[str, object]:
    def average_scalar(key: str) -> float:
        return _mean(tuple(float(block[key]) for block in blocks))

    ratio_values = tuple(float(block["adjacent_gap_ratio_mean"]) for block in blocks)
    variance_values = tuple(float(block["unfolded_spacing_variance"]) for block in blocks)
    return {
        "mean_adjacent_gap_ratio": _mean(ratio_values),
        "between_block_gap_ratio_standard_error": math.sqrt(
            _sample_variance(ratio_values) / len(ratio_values)
        ),
        "mean_unfolded_spacing_variance": _mean(variance_values),
        "between_block_spacing_variance_standard_error": math.sqrt(
            _sample_variance(variance_values) / len(variance_values)
        ),
        "mean_small_gap_fraction": average_scalar("small_gap_fraction_below_0.5"),
        "largest_observed_normalized_gap": max(
            float(block["maximum_normalized_gap"]) for block in blocks
        ),
        "number_variance_mean_by_scale": {
            key: _mean(tuple(float(block["number_variance"][key]) for block in blocks))
            for key in blocks[0]["number_variance"]
        },
        "approximate_delta3_mean_by_scale": {
            key: _mean(tuple(float(block["approximate_delta3"][key]) for block in blocks))
            for key in blocks[0]["approximate_delta3"]
        },
        "pair_correlation_mean_over_poisson": {
            key: _mean(
                tuple(float(block["pair_correlation_over_poisson"][key]) for block in blocks)
            )
            for key in blocks[0]["pair_correlation_over_poisson"]
        },
    }


def run_riemann_multiscale_discovery(
    *,
    prototype_seed: int = 18_593,
    prototype_blocks_per_family: int = 192,
    calibration_trials_per_family: int = 24,
    prototype_strength: float = 192.0,
) -> dict[str, object]:
    """Run the certified-input, train/locked-holdout multiscale analysis."""

    certification = run_validated_riemann_extension(zero_count=512)
    if not certification["certification_passed"]:
        raise RuntimeError("the 512-zero numerical admission gate did not pass")
    roots = critical_line_zeros(512)
    blocks = tuple(
        zero_block_observables(
            roots[(index - 1) * BLOCK_SIZE : index * BLOCK_SIZE], index
        )
        for index in range(1, TRAINING_BLOCKS + HOLDOUT_BLOCKS + 1)
    )
    training = blocks[:TRAINING_BLOCKS]
    holdout = blocks[TRAINING_BLOCKS:]
    prototypes = _prototype_probabilities(
        seed=prototype_seed,
        blocks_per_family=prototype_blocks_per_family,
    )
    fallback_scores, fallback_concentrations, fallback_trace = _score_training_sequence(
        tuple(block["spacing_histogram_counts"] for block in training),
        prototypes,
        prototype_strength=prototype_strength,
    )
    shared_posterior = _run_shared_evidence_posterior(
        training,
        prototypes,
        prototype_strength=prototype_strength,
    )
    if shared_posterior is None:
        training_scores = fallback_scores
        trained_concentrations = fallback_concentrations
        prequential_trace = fallback_trace
        training_posterior = _softmax(training_scores)
        evidence_backend = "local Dirichlet-multinomial fallback"
        mixture_prequential_score = None
        evidence_warning = None
    else:
        training_scores = shared_posterior["cumulative_log_scores"]
        trained_concentrations = shared_posterior["states"]
        prequential_trace = shared_posterior["prequential_trace"]
        training_posterior = shared_posterior["posterior"]
        evidence_backend = shared_posterior["backend"]
        mixture_prequential_score = shared_posterior[
            "mixture_prequential_log_score"
        ]
        evidence_warning = shared_posterior["warning"]
    locked_holdout = _score_locked_holdout(
        tuple(block["spacing_histogram_counts"] for block in holdout),
        trained_concentrations,
        training_posterior,
    )
    calibration = synthetic_recovery_calibration(
        prototypes=prototypes,
        trials_per_family=calibration_trials_per_family,
        prototype_strength=prototype_strength,
    )
    ledger = _build_evidence_ledger(blocks)
    training_winner = max(training_posterior, key=training_posterior.get)
    actual = _aggregate_actual(blocks)
    training_holdout_agree = training_winner == locked_holdout["best_family"]
    attack_gate_passed = bool(
        calibration["calibration_gate"]["attack_detection_at_least_0.75"]
    )
    return {
        "search": "source-disjoint multiscale Riemann spacing discovery",
        "proof_warning": RIEMANN_MULTISCALE_WARNING,
        "certified_input_gate": {
            "certification_passed": certification["certification_passed"],
            "certification_kind": certification["certification_kind"],
            "zero_count": certification["zero_count"],
            "last_height": certification["last_height"],
            "zero_record_sha256": certification["zero_record_sha256"],
            "count_agreement": certification["count_agreement"],
            "interval_enclosure_performed": certification["interval_enclosure_performed"],
        },
        "partition": {
            "block_size_roots": BLOCK_SIZE,
            "training_block_indices": tuple(range(1, TRAINING_BLOCKS + 1)),
            "locked_holdout_block_indices": tuple(
                range(TRAINING_BLOCKS + 1, TRAINING_BLOCKS + HOLDOUT_BLOCKS + 1)
            ),
            "inter_block_gaps_excluded": HOLDOUT_BLOCKS + TRAINING_BLOCKS - 1,
            "holdout_locked_before_model_scoring": True,
            "holdout_updates_parameters": False,
            "holdout_updates_posterior": False,
            "historically_untouched": False,
            "historical_overlap_note": (
                "The prior validated-extension analysis summarized a window "
                "beginning at zero 489, overlapping block 8. No prior "
                "posterior enters this fit, but fresh confirmation requires "
                "zeros beyond 512."
            ),
        },
        "source_disjointness": ledger,
        "histogram": {
            "edges": SPACING_HISTOGRAM_EDGES,
            "likelihood": "Dirichlet-multinomial",
            "prototype_strength": prototype_strength,
            "prototype_seed": prototype_seed,
            "prototype_blocks_per_family": prototype_blocks_per_family,
            "prototype_probabilities": prototypes,
        },
        "blocks": blocks,
        "synthetic_calibration": calibration,
        "training": {
            "backend": evidence_backend,
            "prequential_trace": prequential_trace,
            "family_log_scores": training_scores,
            "mixture_prequential_log_score": mixture_prequential_score,
            "posterior": training_posterior,
            "selected_family": training_winner,
            "evidence_posterior_warning": evidence_warning,
        },
        "locked_holdout": locked_holdout,
        "actual_multiscale_findings": actual,
        "interpretation": {
            "training_family": training_winner,
            "holdout_best_family": locked_holdout["best_family"],
            "training_holdout_agree": training_holdout_agree,
            "holdout_family_margin_log_units": locked_holdout[
                "best_over_second_log_score_margin"
            ],
            "scanner_attack_supported_in_training": training_winner in ATTACK_FAMILIES,
            "sparse_attack_calibration_gate_passed": attack_gate_passed,
            "generalization_result": (
                "training and locked holdout select the same reference family"
                if training_holdout_agree
                else "training preference does not reproduce as the locked holdout winner"
            ),
            "scanner_diagnostic_result": (
                "histogram evidence cleared the declared synthetic attack-recovery gate"
                if attack_gate_passed
                else "histogram evidence did not reliably recover the sparse scanner attacks"
            ),
            "finite_height_beta_is_reference_not_theory": True,
            "gue_beta_2_is_nearest_neighbor_wigner_not_determinantal_gue": True,
            "proof_claim": False,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_riemann_multiscale_discovery(), indent=2))
