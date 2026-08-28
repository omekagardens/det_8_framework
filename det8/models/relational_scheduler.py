"""General question-conditioned and cost-aware scheduler for RET.

The scheduler can choose science or calibration actions.  Its utility combines
information about the user's scientific question, information about nuisance
parameters, and practical burdens.  An explicit M_bottom posterior supports a
model-revision branch instead of forcing unexpected observations into the
least-bad declared model.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, Mapping, Sequence, Union

from det8.models.relational_tomography import (
    OPEN_MODEL_NAME,
    ObservationNoise,
    POSTERIOR_IS_NOT_ONTOLOGY,
    Question,
    RETPosterior,
    RelationalAction,
    endpoint_inclusion_probability,
    parameter_covariance_after_action,
    question_probabilities,
    sample_predictive,
    update_ret_posterior,
)


RG1 = "RG1: Relational identification precedes ontological extension."
ActionNoise = Union[ObservationNoise, Mapping[str, ObservationNoise]]

RET_STATES = (
    "CALIBRATE",
    "DISCOVER_FAMILY",
    "TEST_EXTENSIONS",
    "CHARACTERIZE",
    "CLOSE",
    "CLOSED",
    "MODEL_FAILURE",
    "INCONCLUSIVE",
)


@dataclass(frozen=True)
class CostWeights:
    time: float = 0.0
    money: float = 0.0
    risk: float = 0.0
    wear: float = 0.0


@dataclass(frozen=True)
class SchedulerObjective:
    question: Question
    nuisance_parameters: tuple[str, ...] = ()
    nuisance_information_weight: float = 0.0
    cost_weights: CostWeights = CostWeights()
    monte_carlo_samples_per_model: int = 12

    def __post_init__(self) -> None:
        if self.nuisance_information_weight < 0.0:
            raise ValueError("nuisance information weight cannot be negative")
        if self.monte_carlo_samples_per_model < 1:
            raise ValueError("Monte Carlo sample count must be positive")


@dataclass(frozen=True)
class GovernanceThresholds:
    family_probability: float = 0.95
    novelty_probability: float = 0.99
    open_model_probability: float = 0.50
    nuisance_standard_deviation: float = 0.05
    characterization_relative_uncertainty: float = 0.20

    def __post_init__(self) -> None:
        if not 0.5 < self.family_probability < 1.0:
            raise ValueError("family threshold must lie between 0.5 and 1")
        if not self.family_probability <= self.novelty_probability < 1.0:
            raise ValueError("novelty threshold must be at least the family threshold")


def _entropy_bits(probabilities: Mapping[str, float]) -> float:
    return -sum(
        probability * math.log2(probability)
        for probability in probabilities.values()
        if probability > 0.0
    )


def expected_question_information_bits(
    posterior: RETPosterior,
    action: RelationalAction,
    observation_noise: ObservationNoise,
    question: Question,
    *,
    samples_per_model: int = 12,
    seed: int = 0,
) -> float:
    """Estimate I(q(M);Y_action|D), integrating parameter uncertainty."""

    prior_entropy = _entropy_bits(question_probabilities(posterior, question))
    expected_entropy = 0.0
    rng = random.Random(seed)
    for model_name, model_weight in posterior.model_weights.items():
        if model_weight <= 0.0:
            continue
        for _ in range(samples_per_model):
            observation = sample_predictive(
                posterior,
                model_name,
                action,
                observation_noise,
                rng,
            )
            updated = update_ret_posterior(
                posterior,
                action,
                observation,
                observation_noise,
            )
            expected_entropy += (
                model_weight
                * _entropy_bits(question_probabilities(updated, question))
                / samples_per_model
            )
    return max(0.0, prior_entropy - expected_entropy)


def expected_nuisance_information_bits(
    posterior: RETPosterior,
    action: RelationalAction,
    observation_noise: ObservationNoise,
    nuisance_parameters: Sequence[str],
) -> float:
    """Marginal information gain for nuisance parameters.

    Under this core's Gaussian moment approximation the posterior covariance
    update is observation-independent for both linear and cubature-propagated
    nonlinear actions, so the covariance reduction below is the expected gain
    and needs no posterior-predictive averaging. A genuinely observation-
    dependent covariance would require a non-Gaussian parameter engine, which
    remains outside this core.
    """

    total = 0.0
    requested = set(nuisance_parameters)
    for model_name, model in posterior.models.items():
        weight = posterior.model_weights[model_name]
        if weight <= 0.0:
            continue
        state = posterior.parameters[model_name]
        if not state.parameter_names:
            continue
        new_covariance = parameter_covariance_after_action(
            posterior, model_name, action, observation_noise
        )
        for index, parameter in enumerate(state.parameter_names):
            prior = model.parameter_priors[parameter]
            if prior.role != "nuisance" or parameter not in requested:
                continue
            old_variance = max(state.covariance[index][index], 1.0e-300)
            new_variance = max(new_covariance[index][index], 1.0e-300)
            total += weight * 0.5 * math.log2(old_variance / new_variance)
    return max(0.0, total)


def practical_burden(action: RelationalAction, weights: CostWeights) -> float:
    return (
        weights.time * action.cost.time
        + weights.money * action.cost.money
        + weights.risk * action.cost.risk
        + weights.wear * action.cost.wear
    )


def action_utility(
    posterior: RETPosterior,
    action: RelationalAction,
    observation_noise: ObservationNoise,
    objective: SchedulerObjective,
    *,
    seed: int = 0,
) -> Dict[str, float | str]:
    question_gain = expected_question_information_bits(
        posterior,
        action,
        observation_noise,
        objective.question,
        samples_per_model=objective.monte_carlo_samples_per_model,
        seed=seed,
    )
    nuisance_gain = expected_nuisance_information_bits(
        posterior,
        action,
        observation_noise,
        objective.nuisance_parameters,
    )
    burden = practical_burden(action, objective.cost_weights)
    utility = question_gain + objective.nuisance_information_weight * nuisance_gain - burden
    return {
        "action": action.name,
        "kind": action.kind,
        "question_information_bits": question_gain,
        "nuisance_information_bits": nuisance_gain,
        "practical_burden": burden,
        "utility": utility,
    }


def rank_actions(
    posterior: RETPosterior,
    actions: Sequence[RelationalAction],
    observation_noise: ActionNoise,
    objective: SchedulerObjective,
    *,
    seed: int = 0,
    executed_action_names: Sequence[str] = (),
) -> list[Dict[str, float | str]]:
    def noise_for(action: RelationalAction) -> ObservationNoise:
        if isinstance(observation_noise, Mapping):
            if action.name not in observation_noise:
                raise ValueError(
                    f"missing observation noise for action {action.name}"
                )
            return observation_noise[action.name]
        return observation_noise

    executed = set(executed_action_names)
    eligible = [
        action
        for action in actions
        if not (action.destructive and action.name in executed)
    ]

    ranking = [
        action_utility(
            posterior,
            action,
            noise_for(action),
            objective,
            seed=seed + index,
        )
        for index, action in enumerate(eligible)
    ]
    return sorted(ranking, key=lambda row: (-float(row["utility"]), str(row["action"])))


def _maximum_nuisance_standard_deviation(
    posterior: RETPosterior,
    nuisance_parameters: Sequence[str],
) -> float:
    requested = set(nuisance_parameters)
    maximum = 0.0
    for model_name, model in posterior.models.items():
        if posterior.model_weights[model_name] < 0.01:
            continue
        state = posterior.parameters[model_name]
        for index, parameter in enumerate(state.parameter_names):
            if parameter in requested and model.parameter_priors[parameter].role == "nuisance":
                maximum = max(
                    maximum,
                    math.sqrt(max(state.covariance[index][index], 0.0)),
                )
    return maximum


def ret_governance_state(
    posterior: RETPosterior,
    family_question: Question,
    *,
    novel_parameters: Sequence[str] = (),
    nuisance_parameters: Sequence[str] = (),
    thresholds: GovernanceThresholds = GovernanceThresholds(),
    closure_passed: bool = False,
    budget_exhausted: bool = False,
    closure_requirement: str = "conservation closure",
) -> Dict[str, object]:
    """Evaluate the RET state machine and RG1 novelty gates.

    ``closure_requirement`` names the terminal consistency check that the
    ``CLOSE`` state demands. The default is the momentum-ledger conservation
    closure used by the thrust fixtures; a decay-lifetime or other domain may
    substitute its own label (for example "cross-method consistency").
    """

    open_probability = posterior.model_weights[OPEN_MODEL_NAME]
    family_probabilities = question_probabilities(posterior, family_question)
    best_family = max(family_probabilities, key=family_probabilities.get)
    best_family_probability = family_probabilities[best_family]
    novelty = {
        parameter: endpoint_inclusion_probability(posterior, parameter)
        for parameter in novel_parameters
    }
    nuisance_sd = _maximum_nuisance_standard_deviation(
        posterior, nuisance_parameters
    )

    if open_probability >= thresholds.open_model_probability:
        state = "MODEL_FAILURE"
        reason = "M_bottom dominates: declared model set is inadequate"
    elif budget_exhausted:
        state = "INCONCLUSIVE"
        reason = "experimental budget exhausted before a stopping gate cleared"
    elif nuisance_sd > thresholds.nuisance_standard_deviation:
        state = "CALIBRATE"
        reason = "nuisance uncertainty exceeds the calibration gate"
    elif best_family_probability < thresholds.family_probability:
        state = "DISCOVER_FAMILY"
        reason = "no relational family has crossed the Stage-A threshold"
    elif any(
        (1.0 - thresholds.novelty_probability) < probability < thresholds.novelty_probability
        for probability in novelty.values()
    ):
        state = "TEST_EXTENSIONS"
        reason = "family identified; optional endpoint existence remains unresolved"
    else:
        characterization_needed = False
        for parameter, probability in novelty.items():
            if probability < thresholds.novelty_probability:
                continue
            for model_name, model in posterior.models.items():
                if parameter not in model.parameter_priors:
                    continue
                summary_state = posterior.parameters[model_name]
                index = summary_state.parameter_names.index(parameter)
                mean = abs(summary_state.mean[index])
                sd = math.sqrt(max(summary_state.covariance[index][index], 0.0))
                if mean == 0.0 or sd / mean > thresholds.characterization_relative_uncertainty:
                    characterization_needed = True
        if characterization_needed:
            state = "CHARACTERIZE"
            reason = "endpoint supported but its amplitude remains imprecise"
        elif not closure_passed:
            state = "CLOSE"
            reason = f"inferred regime must now pass {closure_requirement}"
        else:
            state = "CLOSED"
            reason = (
                "relational identification, novelty gates, and "
                f"{closure_requirement} passed"
            )

    return {
        "state": state,
        "reason": reason,
        "rg1": RG1,
        "family_probabilities": family_probabilities,
        "best_family": best_family,
        "best_family_probability": best_family_probability,
        "novel_endpoint_probabilities": novelty,
        "open_model_probability": open_probability,
        "maximum_nuisance_standard_deviation": nuisance_sd,
        "closure_requirement": closure_requirement,
        "posterior_warning": POSTERIOR_IS_NOT_ONTOLOGY,
    }
