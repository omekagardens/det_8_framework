"""Non-Exodus thermal-drift fixture demonstrating general RET reuse."""

from __future__ import annotations

import random

from det8.models.relational_scheduler import (
    CostWeights,
    SchedulerObjective,
    rank_actions,
)
from det8.models.relational_tomography import (
    GaussianPrior,
    PracticalCost,
    Question,
    RelationalAction,
    RelationalModel,
    initialize_ret_posterior,
    update_ret_posterior,
)


def thermal_models() -> list[RelationalModel]:
    bias = {"sensor_bias": GaussianPrior(0.0, 2.0, "nuisance")}
    internal = {"internal_rate": GaussianPrior(1.0, 0.5)}
    ambient = {"ambient_coupling": GaussianPrior(0.0, 1.0)}
    history = {"history_offset": GaussianPrior(0.0, 0.5)}

    def merge(*parts):
        result = {}
        for part in parts:
            result.update(part)
        return result

    return [
        RelationalModel("thermal_null", "none", merge(bias), 0.0),
        RelationalModel("thermal_internal", "internal", merge(internal, bias), 1.0),
        RelationalModel("thermal_ambient", "ambient", merge(ambient, bias), 1.0),
        RelationalModel("thermal_full", "internal_plus_ambient", merge(internal, ambient, bias), 2.0),
        RelationalModel("thermal_full_history", "internal_plus_ambient", merge(internal, ambient, history, bias), 3.0),
    ]


def thermal_questions() -> dict[str, Question]:
    models = thermal_models()
    return {
        "ambient_required": Question(
            "ambient_required",
            {
                model.name: (
                    "ambient_present"
                    if "ambient_coupling" in model.parameter_priors
                    else "ambient_absent"
                )
                for model in models
            },
        ),
        "history_required": Question(
            "history_required",
            {
                model.name: (
                    "history_present"
                    if "history_offset" in model.parameter_priors
                    else "history_absent"
                )
                for model in models
            },
        ),
    }


def thermal_actions() -> list[RelationalAction]:
    actions = []
    index = 0
    for power in (1.0, 2.0):
        for airflow in (0.0, 1.0):
            for preparation_sign in (-1.0, 1.0):
                actions.append(
                    RelationalAction(
                        name=f"thermal_science_{index}",
                        kind="science",
                        known_response=(0.0, 0.0),
                        feature_vectors={
                            "internal_rate": (power, 0.2 * power),
                            "ambient_coupling": (power * airflow, 0.5 * airflow),
                            "history_offset": (preparation_sign, 0.0),
                            "sensor_bias": (1.0, 0.0),
                        },
                        cost=PracticalCost(
                            time=power,
                            money=0.1 * power,
                            risk=0.1 * power,
                            wear=0.5 * airflow,
                        ),
                        metadata={
                            "fixture": "thermal_drift",
                            "power": power,
                            "airflow": airflow,
                            "preparation_sign": preparation_sign,
                        },
                    )
                )
                index += 1
    actions.append(
        RelationalAction(
            name="thermal_sensor_calibration",
            kind="calibration",
            known_response=(10.0, 0.0),
            feature_vectors={"sensor_bias": (1.0, 0.0)},
            cost=PracticalCost(time=0.2),
            metadata={"fixture": "thermal_drift", "calibration": "reference_temperature"},
        )
    )
    return actions


def run_thermal_ret_fixture(seed: int = 71) -> dict[str, object]:
    models = thermal_models()
    questions = thermal_questions()
    actions = thermal_actions()
    posterior = initialize_ret_posterior(
        models,
        complexity_penalty=0.6,
        open_model_prior=0.03,
        open_model_scale=10.0,
    )
    calibration_objective = SchedulerObjective(
        question=questions["ambient_required"],
        nuisance_parameters=("sensor_bias",),
        nuisance_information_weight=2.0,
        cost_weights=CostWeights(time=0.02, risk=0.02, wear=0.02),
        monte_carlo_samples_per_model=8,
    )
    initial_ranking = rank_actions(
        posterior, actions, 0.1, calibration_objective, seed=seed
    )
    calibration = next(action for action in actions if action.kind == "calibration")
    rng = random.Random(seed)
    observation = (
        10.4 + rng.gauss(0.0, 0.1),
        rng.gauss(0.0, 0.1),
    )
    posterior = update_ret_posterior(posterior, calibration, observation, 0.1)

    science_actions = [action for action in actions if action.kind == "science"]
    ambient_ranking = rank_actions(
        posterior,
        science_actions,
        0.1,
        SchedulerObjective(
            question=questions["ambient_required"],
            cost_weights=CostWeights(time=0.01, risk=0.01, wear=0.01),
            monte_carlo_samples_per_model=10,
        ),
        seed=seed + 1,
    )
    history_ranking = rank_actions(
        posterior,
        science_actions,
        0.1,
        SchedulerObjective(
            question=questions["history_required"],
            cost_weights=CostWeights(time=0.01, risk=0.01, wear=0.01),
            monte_carlo_samples_per_model=10,
        ),
        seed=seed + 2,
    )
    action_by_name = {action.name: action for action in actions}
    ambient_top = action_by_name[str(ambient_ranking[0]["action"])]
    history_top = action_by_name[str(history_ranking[0]["action"])]
    return {
        "fixture": "thermal drift and ambient coupling",
        "models": tuple(model.name for model in models),
        "initial_top_action": initial_ranking[0],
        "ambient_question_top_action": {
            **ambient_ranking[0],
            "metadata": dict(ambient_top.metadata),
        },
        "history_question_top_action": {
            **history_ranking[0],
            "metadata": dict(history_top.metadata),
        },
        "posterior_open_model_probability": posterior.model_weights["M_bottom"],
    }
