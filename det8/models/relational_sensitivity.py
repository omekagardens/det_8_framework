"""Prior-hyperparameter and cost-weight sensitivity sweeps for RET.

The RET core reports one posterior and one schedule under fixed prior and cost
settings. This module answers the robustness question directly: how far do the
model weights and the top action move when those settings are perturbed? It
sweeps one axis at a time so each perturbation's influence is separable and is
reported alongside the reference configuration.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from det8.models.relational_scheduler import (
    ActionNoise,
    CostWeights,
    SchedulerObjective,
    rank_actions,
)
from det8.models.relational_tomography import (
    ObservationNoise,
    POSTERIOR_IS_NOT_ONTOLOGY,
    RETPosterior,
    RelationalAction,
    RelationalModel,
    initialize_ret_posterior,
    update_ret_posterior,
)


def _updated_weights(
    models: Sequence[RelationalModel],
    action: RelationalAction,
    observation: Sequence[float],
    observation_noise: ObservationNoise,
    **initialize_kwargs,
) -> Mapping[str, float]:
    posterior = initialize_ret_posterior(models, **initialize_kwargs)
    updated = update_ret_posterior(
        posterior, action, observation, observation_noise
    )
    return dict(updated.model_weights)


def prior_sensitivity_sweep(
    models: Sequence[RelationalModel],
    action: RelationalAction,
    observation: Sequence[float],
    observation_noise: ObservationNoise,
    *,
    complexity_penalties: Sequence[float] = (0.4, 0.8, 1.6),
    open_model_priors: Sequence[float] = (0.01, 0.03, 0.06),
    open_model_scales: Sequence[float] = (10.0, 30.0, 90.0),
    reference_complexity_penalty: float = 0.8,
    reference_open_model_prior: float = 0.03,
    reference_open_model_scale: float = 30.0,
) -> dict[str, object]:
    """Sweep prior hyperparameters one axis at a time around a reference.

    For each axis the other two axes are held at their reference values. The
    result reports, for every declared model plus ``M_bottom``, the minimum and
    maximum posterior weight attained across every perturbation. A fragile
    conclusion therefore shows up as a wide weight range rather than a single
    point estimate.
    """

    names = [model.name for model in models] + ["M_bottom"]
    ranges = {name: [1.0, 0.0] for name in names}
    axes = []
    for penalty in complexity_penalties:
        weights = _updated_weights(
            models,
            action,
            observation,
            observation_noise,
            complexity_penalty=penalty,
            open_model_prior=reference_open_model_prior,
            open_model_scale=reference_open_model_scale,
        )
        axes.append(
            {"axis": "complexity_penalty", "value": penalty, "weights": weights}
        )
    for prior in open_model_priors:
        weights = _updated_weights(
            models,
            action,
            observation,
            observation_noise,
            complexity_penalty=reference_complexity_penalty,
            open_model_prior=prior,
            open_model_scale=reference_open_model_scale,
        )
        axes.append({"axis": "open_model_prior", "value": prior, "weights": weights})
    for scale in open_model_scales:
        weights = _updated_weights(
            models,
            action,
            observation,
            observation_noise,
            complexity_penalty=reference_complexity_penalty,
            open_model_prior=reference_open_model_prior,
            open_model_scale=scale,
        )
        axes.append({"axis": "open_model_scale", "value": scale, "weights": weights})
    for axis in axes:
        for name in names:
            weight = axis["weights"].get(name, 0.0)
            ranges[name][0] = min(ranges[name][0], weight)
            ranges[name][1] = max(ranges[name][1], weight)
    return {
        "weight_ranges": {name: tuple(bounds) for name, bounds in ranges.items()},
        "axes": axes,
        "reference": {
            "complexity_penalty": reference_complexity_penalty,
            "open_model_prior": reference_open_model_prior,
            "open_model_scale": reference_open_model_scale,
        },
        "warning": POSTERIOR_IS_NOT_ONTOLOGY,
    }


def cost_weight_sensitivity_sweep(
    posterior: RETPosterior,
    actions: Sequence[RelationalAction],
    observation_noise: ActionNoise,
    objective: SchedulerObjective,
    *,
    scales: Sequence[float] = (0.0, 0.5, 1.0, 2.0, 4.0),
    seed: int = 0,
) -> dict[str, object]:
    """Rank actions under uniformly rescaled cost weights.

    A single top action across every scale indicates the schedule is not being
    decided by the arbitrary cost scale; several distinct top actions means the
    cost weighting is load-bearing and should be calibrated rather than
    assumed.
    """

    rows = []
    for scale in scales:
        scaled_objective = SchedulerObjective(
            question=objective.question,
            nuisance_parameters=objective.nuisance_parameters,
            nuisance_information_weight=objective.nuisance_information_weight,
            cost_weights=CostWeights(
                time=scale * objective.cost_weights.time,
                money=scale * objective.cost_weights.money,
                risk=scale * objective.cost_weights.risk,
                wear=scale * objective.cost_weights.wear,
            ),
            monte_carlo_samples_per_model=objective.monte_carlo_samples_per_model,
        )
        ranking = rank_actions(
            posterior, actions, observation_noise, scaled_objective, seed=seed
        )
        rows.append(
            {
                "cost_scale": scale,
                "top_action": ranking[0]["action"],
                "top_utility": ranking[0]["utility"],
            }
        )
    top_actions = tuple(sorted({row["top_action"] for row in rows}))
    return {
        "top_actions": top_actions,
        "single_stable_top_action": len(top_actions) == 1,
        "rows": rows,
    }
