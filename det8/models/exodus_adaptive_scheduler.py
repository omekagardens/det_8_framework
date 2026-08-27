"""Adaptive information-gain scheduler for DET relational endpoint tomography.

The scheduler treats each chamber/electrical/history intervention as a possible
experiment.  It chooses the next unmeasured condition that maximizes expected
Bayesian information gain among declared endpoint hypotheses, observes a
synthetic noisy three-vector force, and updates the model probabilities.

This is an experiment-design layer over the reduced-order tomography model.
The hypotheses and effect sizes are declared and calibrated; results are not
evidence for Exodus thrust or for a novel DET coupling.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict
from typing import Callable, Dict, Iterable, List, Mapping, Sequence, Tuple

from det8.models.exodus_relational_tomography import (
    BASE_DEVICE_FORCE_N,
    TomographyCondition,
    condition_features,
    intervention_conditions,
)


Vector3 = Tuple[float, float, float]

EARTH_CHANNEL_EFFECT_N = 50.0e-6
HISTORY_CHANNEL_DIFFERENCE_N = 10.0e-6


HYPOTHESIS_NAMES = (
    "null",
    "device_internal",
    "common_mode_only",
    "boundary_electrode",
    "lead_only",
    "full_relational",
    "full_plus_earth",
    "full_plus_history",
)

RELATIONAL_FAMILY = (
    "full_relational",
    "full_plus_earth",
    "full_plus_history",
)


def _scale(vector: Sequence[float], scalar: float) -> Vector3:
    return tuple(scalar * value for value in vector)


def _add(*vectors: Sequence[float]) -> Vector3:
    return tuple(sum(vector[axis] for vector in vectors) for axis in range(3))


def hypothesis_predictions(condition: TomographyCondition) -> Dict[str, Vector3]:
    """Return fully declared vector predictions for one candidate experiment."""

    features = condition_features(condition)
    boundary = features["boundary_electrode"]
    lead = features["lead_boundary"]
    full = _add(boundary, lead)
    internal = _scale(features["internal_constant"], BASE_DEVICE_FORCE_N[0])
    return {
        "null": (0.0, 0.0, 0.0),
        "device_internal": internal,
        "common_mode_only": features["common_mode_device"],
        "boundary_electrode": boundary,
        "lead_only": lead,
        "full_relational": full,
        "full_plus_earth": _add(
            full,
            _scale(features["earth_fixed"], EARTH_CHANNEL_EFFECT_N),
        ),
        "full_plus_history": _add(
            full,
            _scale(
                features["matched_history"],
                0.5 * HISTORY_CHANNEL_DIFFERENCE_N,
            ),
        ),
    }


def _entropy_bits(weights: Mapping[str, float]) -> float:
    return -sum(
        weight * math.log2(weight)
        for weight in weights.values()
        if weight > 0.0
    )


def _posterior_weights(
    prior: Mapping[str, float],
    predictions: Mapping[str, Vector3],
    observation_n: Sequence[float],
    noise_sigma_n: float,
) -> Dict[str, float]:
    if noise_sigma_n <= 0.0:
        raise ValueError("noise sigma must be positive")
    log_weights = {}
    variance = noise_sigma_n**2
    for name, prior_weight in prior.items():
        if prior_weight <= 0.0:
            log_weights[name] = -math.inf
            continue
        squared_residual = sum(
            (observation_n[axis] - predictions[name][axis]) ** 2
            for axis in range(3)
        )
        log_weights[name] = math.log(prior_weight) - 0.5 * squared_residual / variance
    maximum = max(log_weights.values())
    unnormalized = {
        name: (math.exp(value - maximum) if value > -math.inf else 0.0)
        for name, value in log_weights.items()
    }
    total = sum(unnormalized.values())
    return {name: value / total for name, value in unnormalized.items()}


def monte_carlo_information_gain_bits(
    weights: Mapping[str, float],
    predictions: Mapping[str, Vector3],
    noise_sigma_n: float,
    *,
    samples_per_hypothesis: int = 12,
    seed: int = 0,
) -> float:
    """Monte Carlo estimate of I(hypothesis; vector observation)."""

    if samples_per_hypothesis < 1:
        raise ValueError("samples_per_hypothesis must be positive")
    rng = random.Random(seed)
    prior_entropy = _entropy_bits(weights)
    expected_posterior_entropy = 0.0
    for truth_name, truth_weight in weights.items():
        if truth_weight <= 0.0:
            continue
        for _ in range(samples_per_hypothesis):
            observation = tuple(
                predictions[truth_name][axis] + rng.gauss(0.0, noise_sigma_n)
                for axis in range(3)
            )
            posterior = _posterior_weights(
                weights,
                predictions,
                observation,
                noise_sigma_n,
            )
            expected_posterior_entropy += (
                truth_weight
                * _entropy_bits(posterior)
                / samples_per_hypothesis
            )
    return max(0.0, prior_entropy - expected_posterior_entropy)


def expected_information_gain_bits(
    weights: Mapping[str, float],
    predictions: Mapping[str, Vector3],
    noise_sigma_n: float,
) -> float:
    """Fast moment-matched approximation to Bayesian information gain.

    The discrete predictive mixture is replaced by a Gaussian with the same
    weighted mean and covariance.  The entropy gain over the measurement-noise
    Gaussian is analytic.  Capping it at the discrete prior entropy preserves
    the maximum information available about model identity.  A slower direct
    Monte Carlo estimator remains available for auditing this ranking.
    """

    return min(
        _entropy_bits(weights),
        predictive_disagreement_bits(weights, predictions, noise_sigma_n),
    )


def predictive_disagreement_bits(
    weights: Mapping[str, float],
    predictions: Mapping[str, Vector3],
    noise_sigma_n: float,
) -> float:
    """Uncapped moment-matched predictive separation used for shortlisting."""

    if noise_sigma_n <= 0.0:
        raise ValueError("noise sigma must be positive")
    mean = tuple(
        sum(weights[name] * predictions[name][axis] for name in weights)
        for axis in range(3)
    )
    covariance = [[0.0 for _ in range(3)] for _ in range(3)]
    for name, weight in weights.items():
        difference = tuple(predictions[name][axis] - mean[axis] for axis in range(3))
        for row in range(3):
            for column in range(3):
                covariance[row][column] += weight * difference[row] * difference[column]
    variance = noise_sigma_n**2
    matrix = [
        [
            (1.0 if row == column else 0.0) + covariance[row][column] / variance
            for column in range(3)
        ]
        for row in range(3)
    ]
    determinant = (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )
    return 0.5 * math.log2(max(determinant, 1.0))


def _condition_record(condition: TomographyCondition) -> Dict[str, object]:
    return asdict(condition)


def initial_information_ranking(
    *,
    noise_sigma_n: float = 50.0e-6,
    conditions: Sequence[TomographyCondition] | None = None,
    limit: int = 10,
) -> List[Dict[str, object]]:
    conditions = list(conditions or intervention_conditions())
    weights = {name: 1.0 / len(HYPOTHESIS_NAMES) for name in HYPOTHESIS_NAMES}
    scored = []
    for index, condition in enumerate(conditions):
        disagreement = predictive_disagreement_bits(
            weights,
            hypothesis_predictions(condition),
            noise_sigma_n,
        )
        scored.append(
            {
                "candidate_index": index,
                "moment_matched_information_gain_bits": min(
                    _entropy_bits(weights), disagreement
                ),
                "predictive_disagreement_bits": disagreement,
                "condition": _condition_record(condition),
            }
        )
    return sorted(
        scored,
        key=lambda row: (-row["predictive_disagreement_bits"], row["candidate_index"]),
    )[:limit]


def run_adaptive_schedule(
    *,
    truth_model: str = "full_relational",
    noise_sigma_n: float = 50.0e-6,
    posterior_threshold: float = 0.95,
    max_steps: int = 20,
    target_models: Sequence[str] = RELATIONAL_FAMILY,
    shortlist_size: int = 12,
    monte_carlo_samples_per_hypothesis: int = 10,
    seed: int = 2_026,
    conditions: Sequence[TomographyCondition] | None = None,
) -> Dict[str, object]:
    if truth_model not in HYPOTHESIS_NAMES:
        raise ValueError("unknown truth model")
    if not 0.5 < posterior_threshold < 1.0:
        raise ValueError("posterior threshold must lie between 0.5 and 1")
    if max_steps < 1:
        raise ValueError("max_steps must be positive")
    if not target_models or any(name not in HYPOTHESIS_NAMES for name in target_models):
        raise ValueError("target_models must contain declared hypotheses")
    if shortlist_size < 1:
        raise ValueError("shortlist_size must be positive")

    candidates = list(conditions or intervention_conditions())
    weights = {name: 1.0 / len(HYPOTHESIS_NAMES) for name in HYPOTHESIS_NAMES}
    observation_rng = random.Random(seed)
    remaining = set(range(len(candidates)))
    steps = []

    for step_index in range(max_steps):
        prior_entropy = _entropy_bits(weights)
        ranked = []
        for candidate_index in remaining:
            condition = candidates[candidate_index]
            predictions = hypothesis_predictions(condition)
            disagreement = predictive_disagreement_bits(
                weights,
                predictions,
                noise_sigma_n,
            )
            ranked.append((disagreement, candidate_index))
        shortlist = sorted(
            ranked,
            key=lambda item: (-item[0], item[1]),
        )[: min(shortlist_size, len(ranked))]
        audited = []
        for disagreement, candidate_index in shortlist:
            information_gain = monte_carlo_information_gain_bits(
                weights,
                hypothesis_predictions(candidates[candidate_index]),
                noise_sigma_n,
                samples_per_hypothesis=monte_carlo_samples_per_hypothesis,
                seed=seed * 100_003 + step_index * 1_009 + candidate_index,
            )
            audited.append((information_gain, disagreement, candidate_index))
        expected_gain, selected_disagreement, selected_index = max(
            audited,
            key=lambda item: (item[0], item[1], -item[2]),
        )
        remaining.remove(selected_index)
        condition = candidates[selected_index]
        predictions = hypothesis_predictions(condition)
        truth_prediction = predictions[truth_model]
        observation = tuple(
            truth_prediction[axis] + observation_rng.gauss(0.0, noise_sigma_n)
            for axis in range(3)
        )
        weights = _posterior_weights(
            weights,
            predictions,
            observation,
            noise_sigma_n,
        )
        posterior_entropy = _entropy_bits(weights)
        best_model = max(weights, key=weights.get)
        target_probability = sum(weights[name] for name in target_models)
        steps.append(
            {
                "step": step_index + 1,
                "selected_candidate_index": selected_index,
                "condition": _condition_record(condition),
                "expected_information_gain_bits": expected_gain,
                "predictive_disagreement_bits": selected_disagreement,
                "realized_information_gain_bits": prior_entropy - posterior_entropy,
                "observation_n": {
                    "x": observation[0],
                    "y": observation[1],
                    "z": observation[2],
                },
                "best_model": best_model,
                "best_model_probability": weights[best_model],
                "truth_model_probability": weights[truth_model],
                "target_probability": target_probability,
                "posterior_entropy_bits": posterior_entropy,
            }
        )
        if target_probability >= posterior_threshold:
            break

    final_target_probability = sum(weights[name] for name in target_models)
    achieved = final_target_probability >= posterior_threshold
    return {
        "strategy": "adaptive_expected_information_gain",
        "truth_model": truth_model,
        "noise_sigma_n": noise_sigma_n,
        "posterior_threshold": posterior_threshold,
        "target_models": tuple(target_models),
        "max_steps": max_steps,
        "threshold_achieved": achieved,
        "steps_to_threshold": len(steps) if achieved else None,
        "steps_run": len(steps),
        "final_entropy_bits": _entropy_bits(weights),
        "final_target_probability": final_target_probability,
        "final_posterior": weights,
        "steps": steps,
    }


def run_random_schedule(
    *,
    truth_model: str = "full_relational",
    noise_sigma_n: float = 50.0e-6,
    posterior_threshold: float = 0.95,
    max_steps: int = 20,
    target_models: Sequence[str] = RELATIONAL_FAMILY,
    seed: int = 2_026,
    conditions: Sequence[TomographyCondition] | None = None,
) -> Dict[str, object]:
    candidates = list(conditions or intervention_conditions())
    rng = random.Random(seed)
    order = list(range(len(candidates)))
    rng.shuffle(order)
    weights = {name: 1.0 / len(HYPOTHESIS_NAMES) for name in HYPOTHESIS_NAMES}
    steps = []
    for step_index, selected_index in enumerate(order[:max_steps]):
        condition = candidates[selected_index]
        predictions = hypothesis_predictions(condition)
        truth_prediction = predictions[truth_model]
        observation = tuple(
            truth_prediction[axis] + rng.gauss(0.0, noise_sigma_n)
            for axis in range(3)
        )
        prior_entropy = _entropy_bits(weights)
        weights = _posterior_weights(weights, predictions, observation, noise_sigma_n)
        posterior_entropy = _entropy_bits(weights)
        target_probability = sum(weights[name] for name in target_models)
        steps.append(
            {
                "step": step_index + 1,
                "selected_candidate_index": selected_index,
                "condition": _condition_record(condition),
                "realized_information_gain_bits": prior_entropy - posterior_entropy,
                "truth_model_probability": weights[truth_model],
                "target_probability": target_probability,
                "posterior_entropy_bits": posterior_entropy,
            }
        )
        if target_probability >= posterior_threshold:
            break
    final_target_probability = sum(weights[name] for name in target_models)
    achieved = final_target_probability >= posterior_threshold
    return {
        "strategy": "random_without_replacement",
        "truth_model": truth_model,
        "noise_sigma_n": noise_sigma_n,
        "posterior_threshold": posterior_threshold,
        "target_models": tuple(target_models),
        "max_steps": max_steps,
        "threshold_achieved": achieved,
        "steps_to_threshold": len(steps) if achieved else None,
        "steps_run": len(steps),
        "final_entropy_bits": _entropy_bits(weights),
        "final_target_probability": final_target_probability,
        "final_posterior": weights,
        "steps": steps,
    }


def _median(values: Sequence[float]) -> float:
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return 0.5 * (ordered[midpoint - 1] + ordered[midpoint])


def benchmark_schedulers(
    *,
    trials: int = 30,
    truth_model: str = "full_relational",
    noise_sigma_n: float = 50.0e-6,
    posterior_threshold: float = 0.95,
    max_steps: int = 20,
    seed: int = 76_021,
) -> Dict[str, object]:
    adaptive_results = []
    random_results = []
    for trial in range(trials):
        trial_seed = seed + trial * 101
        adaptive_results.append(
            run_adaptive_schedule(
                truth_model=truth_model,
                noise_sigma_n=noise_sigma_n,
                posterior_threshold=posterior_threshold,
                max_steps=max_steps,
                seed=trial_seed,
            )
        )
        random_results.append(
            run_random_schedule(
                truth_model=truth_model,
                noise_sigma_n=noise_sigma_n,
                posterior_threshold=posterior_threshold,
                max_steps=max_steps,
                seed=trial_seed,
            )
        )

    def summarize(results: Sequence[Mapping[str, object]]) -> Dict[str, float]:
        successes = [result for result in results if result["threshold_achieved"]]
        capped_steps = [
            float(result["steps_to_threshold"] or (max_steps + 1))
            for result in results
        ]
        return {
            "success_fraction": len(successes) / len(results),
            "median_steps_capped": _median(capped_steps),
            "mean_steps_capped": sum(capped_steps) / len(capped_steps),
            "mean_final_truth_probability": sum(
                result["final_posterior"][truth_model] for result in results
            ) / len(results),
            "mean_final_target_probability": sum(
                result["final_target_probability"] for result in results
            ) / len(results),
            "mean_final_entropy_bits": sum(
                result["final_entropy_bits"] for result in results
            ) / len(results),
        }

    adaptive_summary = summarize(adaptive_results)
    random_summary = summarize(random_results)
    return {
        "trials": trials,
        "truth_model": truth_model,
        "noise_sigma_n": noise_sigma_n,
        "posterior_threshold": posterior_threshold,
        "max_steps": max_steps,
        "target_models": RELATIONAL_FAMILY,
        "adaptive": adaptive_summary,
        "random": random_summary,
        "median_step_reduction": (
            random_summary["median_steps_capped"]
            - adaptive_summary["median_steps_capped"]
        ),
    }


def intervention_ablation(
    *,
    truth_model: str = "full_relational",
    noise_sigma_n: float = 50.0e-6,
    max_steps: int = 20,
    seed: int = 4_044,
) -> Dict[str, object]:
    all_conditions = intervention_conditions()
    filters: Dict[str, Callable[[TomographyCondition], bool]] = {
        "all_controls": lambda condition: True,
        "no_chamber_rotation": lambda condition: condition.chamber_angle_deg == 0.0,
        "no_lead_rerouting": lambda condition: condition.lead_routing == "same_end",
        "no_preparation_reversal": lambda condition: condition.preparation_sign == 1,
        "single_static_geometry": lambda condition: (
            condition.chamber_angle_deg == 0.0
            and condition.device_angle_deg == 0.0
            and condition.lead_routing == "same_end"
            and condition.wall_distance_m == 0.12
            and condition.preparation_sign == 1
        ),
    }
    cases = []
    for case_index, (name, keep) in enumerate(filters.items()):
        conditions = [condition for condition in all_conditions if keep(condition)]
        result = run_adaptive_schedule(
            truth_model=truth_model,
            noise_sigma_n=noise_sigma_n,
            max_steps=min(max_steps, len(conditions)),
            seed=seed + case_index,
            conditions=conditions,
        )
        cases.append(
            {
                "available_control_set": name,
                "candidate_conditions": len(conditions),
                "threshold_achieved": result["threshold_achieved"],
                "steps_to_threshold": result["steps_to_threshold"],
                "final_truth_probability": result["final_posterior"][truth_model],
                "final_target_probability": result["final_target_probability"],
                "final_entropy_bits": result["final_entropy_bits"],
            }
        )
    return {"cases": cases}


def novel_channel_recovery(
    *,
    noise_sigma_n: float = 10.0e-6,
    posterior_threshold: float = 0.95,
    max_steps: int = 40,
    seed: int = 98_011,
) -> Dict[str, object]:
    cases = []
    for truth_index, truth_model in enumerate(
        ("full_relational", "full_plus_earth", "full_plus_history")
    ):
        result = run_adaptive_schedule(
            truth_model=truth_model,
            noise_sigma_n=noise_sigma_n,
            posterior_threshold=posterior_threshold,
            max_steps=max_steps,
            target_models=(truth_model,),
            seed=seed + truth_index,
        )
        cases.append(
            {
                "truth_model": truth_model,
                "threshold_achieved": result["threshold_achieved"],
                "steps_to_threshold": result["steps_to_threshold"],
                "selected_model": max(
                    result["final_posterior"],
                    key=result["final_posterior"].get,
                ),
                "truth_probability": result["final_posterior"][truth_model],
                "final_entropy_bits": result["final_entropy_bits"],
            }
        )
    return {
        "declared_earth_effect_n": EARTH_CHANNEL_EFFECT_N,
        "declared_history_difference_n": HISTORY_CHANNEL_DIFFERENCE_N,
        "cases": cases,
    }


def run_adaptive_scheduler_suite() -> Dict[str, object]:
    return {
        "status": "synthetic adaptive experiment design; no new DET force prediction",
        "hypotheses": HYPOTHESIS_NAMES,
        "declared_novel_effect_scales": {
            "earth_channel_n": EARTH_CHANNEL_EFFECT_N,
            "matched_history_difference_n": HISTORY_CHANNEL_DIFFERENCE_N,
        },
        "initial_information_ranking": initial_information_ranking(),
        "example_adaptive_schedule": run_adaptive_schedule(),
        "scheduler_benchmark": benchmark_schedulers(),
        "intervention_ablation": intervention_ablation(),
        "novel_channel_recovery": novel_channel_recovery(),
    }


if __name__ == "__main__":
    print(json.dumps(run_adaptive_scheduler_suite(), indent=2, sort_keys=True))
