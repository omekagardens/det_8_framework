"""Exodus electrostatic apparatus as one fixture for the general RET core."""

from __future__ import annotations

import random
from typing import Dict, Mapping, Sequence

from det8.models.exodus_relational_tomography import (
    BASE_DEVICE_FORCE_N,
    condition_features,
    intervention_conditions,
)
from det8.models.relational_scheduler import (
    CostWeights,
    GovernanceThresholds,
    SchedulerObjective,
    rank_actions,
    ret_governance_state,
)
from det8.models.relational_tomography import (
    GaussianPrior,
    PracticalCost,
    Question,
    RelationalAction,
    RelationalModel,
    endpoint_inclusion_probability,
    initialize_ret_posterior,
    parameter_summary,
    update_ret_posterior,
)


def exodus_models() -> list[RelationalModel]:
    nuisance = {"cross_axis_xz": GaussianPrior(0.0, 0.08, "nuisance")}
    boundary = {"boundary_scale": GaussianPrior(1.0, 0.30)}
    lead = {"lead_scale": GaussianPrior(1.0, 0.30)}
    internal = {"internal_scale": GaussianPrior(1.0, 0.50)}
    earth = {"earth_amplitude_n": GaussianPrior(0.0, 50.0e-6)}
    history = {"history_amplitude_n": GaussianPrior(0.0, 15.0e-6)}

    def combined(*parts: Mapping[str, GaussianPrior]) -> Dict[str, GaussianPrior]:
        result: Dict[str, GaussianPrior] = {}
        for part in parts:
            result.update(part)
        return result

    return [
        RelationalModel("null", "no_endpoint", combined(nuisance), 0.0),
        RelationalModel("device_internal", "internal", combined(internal, nuisance), 1.0),
        RelationalModel("boundary_only", "boundary", combined(boundary, nuisance), 1.0),
        RelationalModel("lead_only", "boundary", combined(lead, nuisance), 1.0),
        RelationalModel("full_relational", "boundary_plus_lead", combined(boundary, lead, nuisance), 2.0),
        RelationalModel("full_plus_earth", "boundary_plus_lead", combined(boundary, lead, earth, nuisance), 3.0),
        RelationalModel("full_plus_history", "boundary_plus_lead", combined(boundary, lead, history, nuisance), 3.0),
        RelationalModel("full_plus_both", "boundary_plus_lead", combined(boundary, lead, earth, history, nuisance), 4.0),
    ]


def exodus_questions() -> dict[str, Question]:
    models = exodus_models()
    family = {
        model.name: (
            "no_external_relation"
            if model.family in ("no_endpoint", "internal")
            else "external_relational_endpoint"
        )
        for model in models
    }
    extension = {}
    for model in models:
        has_earth = "earth_amplitude_n" in model.parameter_priors
        has_history = "history_amplitude_n" in model.parameter_priors
        if has_earth and has_history:
            answer = "earth_and_history"
        elif has_earth:
            answer = "earth"
        elif has_history:
            answer = "history"
        else:
            answer = "no_novel_extension"
        extension[model.name] = answer
    return {
        "external_endpoint_required": Question(
            "external_endpoint_required",
            family,
            "Does the force require a relation beyond the apparatus-only cut?",
        ),
        "novel_extension_required": Question(
            "novel_extension_required",
            extension,
            "Does the residual require Earth or matched-history structure?",
        ),
    }


def _science_action(index: int) -> RelationalAction:
    condition = intervention_conditions()[index]
    features = condition_features(condition)
    lead = features["lead_boundary"]
    feature_vectors = {
        "internal_scale": tuple(
            BASE_DEVICE_FORCE_N[0] * value
            for value in features["internal_constant"]
        ),
        "boundary_scale": features["boundary_electrode"],
        "lead_scale": lead,
        "earth_amplitude_n": features["earth_fixed"],
        "history_amplitude_n": features["matched_history"],
        "cross_axis_xz": (lead[2], 0.0, 0.0),
    }
    risk = abs(condition.common_mode_kv) / 20.0 + (0.2 if condition.wall_distance_m == 0.08 else 0.0)
    wear = 0.4 if condition.lead_routing != "same_end" else 0.0
    return RelationalAction(
        name=f"exodus_science_{index}",
        kind="science",
        known_response=(0.0, 0.0, 0.0),
        feature_vectors=feature_vectors,
        cost=PracticalCost(time=1.0, money=0.1, risk=risk, wear=wear),
        metadata={
            "fixture": "exodus",
            "condition_index": index,
            "wall_distance_m": condition.wall_distance_m,
            "common_mode_kv": condition.common_mode_kv,
            "lead_routing": condition.lead_routing,
            "device_angle_deg": condition.device_angle_deg,
            "chamber_angle_deg": condition.chamber_angle_deg,
            "preparation_sign": condition.preparation_sign,
        },
    )


def exodus_actions() -> list[RelationalAction]:
    # A balanced 24-action subset spans every intervention axis without making
    # the fixture responsible for the general scheduler's combinatorics.
    indices = (0, 9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 99,
               108, 117, 126, 135, 8, 13, 56, 61, 80, 85, 128, 133)
    actions = [_science_action(index) for index in indices]
    for sign in (-1.0, 1.0):
        calibration_load = sign * 500.0e-6
        actions.append(
            RelationalAction(
                name=f"cross_axis_calibration_{'positive' if sign > 0 else 'negative'}",
                kind="calibration",
                known_response=(0.0, 0.0, calibration_load),
                feature_vectors={
                    "cross_axis_xz": (calibration_load, 0.0, 0.0),
                },
                cost=PracticalCost(time=0.2, money=0.0, risk=0.0, wear=0.0),
                metadata={"fixture": "exodus", "calibration": "sensor_cross_axis"},
            )
        )
    return actions


def simulate_exodus_observation(
    action: RelationalAction,
    parameters: Mapping[str, float],
    *,
    noise_sigma_n: float,
    rng: random.Random,
    misspecification_n: Sequence[float] = (0.0, 0.0, 0.0),
) -> tuple[float, ...]:
    observation = list(action.known_response)
    for parameter, value in parameters.items():
        vector = action.feature_vectors.get(parameter)
        if vector is None:
            continue
        for axis in range(action.dimension):
            observation[axis] += value * vector[axis]
    return tuple(
        observation[axis] + misspecification_n[axis] + rng.gauss(0.0, noise_sigma_n)
        for axis in range(action.dimension)
    )


def run_exodus_ret_fixture(seed: int = 8_808) -> dict[str, object]:
    models = exodus_models()
    questions = exodus_questions()
    actions = exodus_actions()
    posterior = initialize_ret_posterior(
        models,
        complexity_penalty=0.7,
        open_model_prior=0.03,
        open_model_scale=1.0e-3,
    )
    thresholds = GovernanceThresholds(
        family_probability=0.95,
        novelty_probability=0.99,
        nuisance_standard_deviation=0.05,
    )
    initial_state = ret_governance_state(
        posterior,
        questions["external_endpoint_required"],
        novel_parameters=("earth_amplitude_n", "history_amplitude_n"),
        nuisance_parameters=("cross_axis_xz",),
        thresholds=thresholds,
    )
    calibration_objective = SchedulerObjective(
        question=questions["external_endpoint_required"],
        nuisance_parameters=("cross_axis_xz",),
        nuisance_information_weight=3.0,
        cost_weights=CostWeights(time=0.02, risk=0.02, wear=0.02),
        monte_carlo_samples_per_model=6,
    )
    initial_ranking = rank_actions(
        posterior,
        actions,
        5.0e-6,
        calibration_objective,
        seed=seed,
    )
    selected_name = str(initial_ranking[0]["action"])
    selected = next(action for action in actions if action.name == selected_name)
    truth = {
        "boundary_scale": 1.0,
        "lead_scale": 1.0,
        "earth_amplitude_n": 17.0e-6,
        "history_amplitude_n": 0.0,
        "cross_axis_xz": 0.03,
    }
    observation = simulate_exodus_observation(
        selected,
        truth,
        noise_sigma_n=5.0e-6,
        rng=random.Random(seed),
    )
    posterior = update_ret_posterior(posterior, selected, observation, 5.0e-6)
    posterior_after_first = posterior
    post_first_action_state = ret_governance_state(
        posterior,
        questions["external_endpoint_required"],
        novel_parameters=("earth_amplitude_n", "history_amplitude_n"),
        nuisance_parameters=("cross_axis_xz",),
        thresholds=thresholds,
    )

    # Characterize an Earth-correlated amplitude that was not one of the old
    # point hypotheses. The 17 uN truth is inferred through its Gaussian slab.
    extension_objective = SchedulerObjective(
        question=questions["novel_extension_required"],
        nuisance_parameters=("cross_axis_xz",),
        nuisance_information_weight=0.2,
        cost_weights=CostWeights(time=0.01, risk=0.01, wear=0.01),
        monte_carlo_samples_per_model=8,
    )
    remaining_science = [
        action for action in actions
        if action.kind == "science" and action.name != selected.name
    ]
    characterization_steps = []
    characterization_rng = random.Random(seed + 1)
    for step in range(12):
        ranking = rank_actions(
            posterior,
            remaining_science,
            5.0e-6,
            extension_objective,
            seed=seed + 100 + step,
        )
        action_name = str(ranking[0]["action"])
        action = next(item for item in remaining_science if item.name == action_name)
        remaining_science.remove(action)
        observed = simulate_exodus_observation(
            action,
            truth,
            noise_sigma_n=5.0e-6,
            rng=characterization_rng,
        )
        posterior = update_ret_posterior(posterior, action, observed, 5.0e-6)
        characterization_steps.append(
            {
                "step": step + 1,
                "action": action.name,
                "earth_inclusion_probability": endpoint_inclusion_probability(
                    posterior, "earth_amplitude_n"
                ),
            }
        )
    final_state = ret_governance_state(
        posterior,
        questions["external_endpoint_required"],
        novel_parameters=("earth_amplitude_n", "history_amplitude_n"),
        nuisance_parameters=("cross_axis_xz",),
        thresholds=thresholds,
    )

    # Explicitly attack the model set with a response outside every declared
    # predictive scale. M_bottom should stop discrimination and request review.
    science_action = next(action for action in actions if action.kind == "science")
    attacked = update_ret_posterior(
        posterior_after_first,
        science_action,
        (5.0e-3, 5.0e-3, 5.0e-3),
        5.0e-6,
    )
    failure_state = ret_governance_state(
        attacked,
        questions["external_endpoint_required"],
        novel_parameters=("earth_amplitude_n", "history_amplitude_n"),
        nuisance_parameters=("cross_axis_xz",),
        thresholds=thresholds,
    )
    return {
        "fixture": "Exodus 3-D relational response",
        "models": tuple(model.name for model in models),
        "science_actions": sum(action.kind == "science" for action in actions),
        "calibration_actions": sum(action.kind == "calibration" for action in actions),
        "declared_truth_earth_amplitude_n": truth["earth_amplitude_n"],
        "initial_state": initial_state,
        "initial_top_action": initial_ranking[0],
        "post_first_action_state": post_first_action_state,
        "post_first_action_cross_axis": parameter_summary(
            posterior_after_first, "full_relational"
        )["cross_axis_xz"],
        "hierarchical_earth_characterization": {
            "steps": characterization_steps,
            "earth_inclusion_probability": endpoint_inclusion_probability(
                posterior, "earth_amplitude_n"
            ),
            "full_plus_earth_parameter": parameter_summary(
                posterior, "full_plus_earth"
            )["earth_amplitude_n"],
            "state": final_state,
        },
        "model_failure_attack": {
            "open_model_probability": attacked.model_weights["M_bottom"],
            "state": failure_state,
        },
    }
