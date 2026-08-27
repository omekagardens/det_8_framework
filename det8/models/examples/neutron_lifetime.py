"""Neutron-lifetime discrepancy adapter for the general RET calculus.

The adapter treats published lifetime values as aggregate records, not as raw
experimental data.  It separates confinement method from decay-product
readout so that the J-PARC electron-counting beam result can update a more
specific question than the usual binary label "beam versus bottle".
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from typing import Mapping, Sequence

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
    response_for_parameters,
    update_ret_posterior,
)


REFERENCE_LIFETIME_S = 880.0


@dataclass(frozen=True)
class PublishedLifetimeRecord:
    name: str
    lifetime_s: float
    standard_error_s: float
    method: str
    readout: str
    spectrum_coordinate: float
    citation_url: str

    def __post_init__(self) -> None:
        if self.standard_error_s <= 0.0:
            raise ValueError("published standard error must be positive")
        if self.method not in ("beam", "bottle"):
            raise ValueError("record method must be beam or bottle")


def neutron_models() -> list[RelationalModel]:
    lifetime = {"lifetime_offset_s": GaussianPrior(0.0, 12.0)}
    anchored_lifetime = {"lifetime_offset_s": GaussianPrior(0.0, 5.0)}
    return [
        RelationalModel("neutron_common", "common_lifetime", lifetime, 0.0),
        RelationalModel(
            "neutron_proton_pipeline",
            "method_systematic",
            {
                **anchored_lifetime,
                "proton_pipeline_bias_s": GaussianPrior(0.0, 10.0, "nuisance"),
            },
            1.0,
        ),
        RelationalModel(
            "neutron_bottle_storage",
            "method_systematic",
            {
                **anchored_lifetime,
                "bottle_storage_bias_s": GaussianPrior(0.0, 10.0, "nuisance"),
            },
            1.0,
        ),
        RelationalModel(
            "neutron_spectrum_state",
            "state_systematic",
            {
                **anchored_lifetime,
                "spectrum_shift_s": GaussianPrior(0.0, 10.0, "nuisance"),
            },
            1.5,
        ),
        RelationalModel(
            "neutron_exotic_decay",
            "additional_decay_channel",
            {
                **anchored_lifetime,
                "exotic_beta_shift_s": GaussianPrior(0.0, 10.0),
            },
            3.0,
        ),
    ]


def neutron_questions() -> dict[str, Question]:
    models = neutron_models()
    return {
        "relational_family": Question(
            "relational_family",
            {model.name: model.family for model in models},
            "Which broad family carries the lifetime discrepancy?",
        ),
        "discrepancy_source": Question(
            "discrepancy_source",
            {
                "neutron_common": "common_lifetime",
                "neutron_proton_pipeline": "proton_pipeline",
                "neutron_bottle_storage": "bottle_storage",
                "neutron_spectrum_state": "spectrum_state",
                "neutron_exotic_decay": "additional_decay_channel",
            },
            "Which predictive relationship carries the lifetime discrepancy?",
        ),
        "proton_pipeline_required": Question(
            "proton_pipeline_required",
            {
                model.name: (
                    "proton_pipeline_required"
                    if "proton_pipeline_bias_s" in model.parameter_priors
                    else "proton_pipeline_not_required"
                )
                for model in models
            },
        ),
        "additional_decay_required": Question(
            "additional_decay_required",
            {
                model.name: (
                    "additional_decay_required"
                    if "exotic_beta_shift_s" in model.parameter_priors
                    else "additional_decay_not_required"
                )
                for model in models
            },
        ),
    }


def published_lifetime_records() -> tuple[PublishedLifetimeRecord, ...]:
    return (
        PublishedLifetimeRecord(
            "nist_bl1_proton_beam_2013",
            887.7,
            math.hypot(1.2, 1.9),
            "beam",
            "proton",
            1.0,
            "https://arxiv.org/abs/1309.2623",
        ),
        PublishedLifetimeRecord(
            "ucntau_magnetic_bottle_2021",
            877.75,
            math.hypot(0.28, 0.22),
            "bottle",
            "survivor",
            -1.0,
            "https://arxiv.org/abs/2106.10375",
        ),
        PublishedLifetimeRecord(
            "jparc_electron_beam_2024",
            877.2,
            math.hypot(1.7, 4.0),
            "beam",
            "electron",
            0.25,
            "https://arxiv.org/abs/2412.19519",
        ),
    )


def _lifetime_action(
    name: str,
    *,
    kind: str,
    method: str,
    readout: str,
    spectrum_coordinate: float,
    cost: PracticalCost,
    metadata: Mapping[str, object] | None = None,
) -> RelationalAction:
    return RelationalAction(
        name=name,
        kind=kind,
        known_response=(REFERENCE_LIFETIME_S,),
        feature_vectors={
            "lifetime_offset_s": (1.0,),
            "proton_pipeline_bias_s": (
                1.0 if method == "beam" and readout == "proton" else 0.0,
            ),
            "bottle_storage_bias_s": (1.0 if method == "bottle" else 0.0,),
            "spectrum_shift_s": (spectrum_coordinate,),
            "exotic_beta_shift_s": (1.0 if method == "beam" else 0.0,),
        },
        cost=cost,
        metadata={
            "fixture": "neutron_lifetime",
            "method": method,
            "readout": readout,
            "spectrum_coordinate": spectrum_coordinate,
            **dict(metadata or {}),
        },
    )


def published_record_action(record: PublishedLifetimeRecord) -> RelationalAction:
    return _lifetime_action(
        record.name,
        kind="science",
        method=record.method,
        readout=record.readout,
        spectrum_coordinate=record.spectrum_coordinate,
        cost=PracticalCost(),
        metadata={"record_type": "published_aggregate", "citation_url": record.citation_url},
    )


def joint_published_record_action() -> RelationalAction:
    """Represent the aggregate literature record as one vector observation."""

    records = published_lifetime_records()
    actions = tuple(published_record_action(record) for record in records)
    parameter_names = tuple(actions[0].feature_vectors)
    return RelationalAction(
        "joint_neutron_literature_record",
        "science",
        tuple(REFERENCE_LIFETIME_S for _ in records),
        {
            parameter: tuple(
                action.feature_vectors[parameter][0] for action in actions
            )
            for parameter in parameter_names
        },
        metadata={
            "fixture": "neutron_lifetime",
            "record_type": "joint_published_aggregate",
            "record_names": tuple(record.name for record in records),
        },
    )


def joint_published_covariance(
    *, beam_readout_correlation: float = 0.0
) -> tuple[tuple[float, ...], ...]:
    """Build a declared covariance sensitivity model for the three records.

    The optional correlation connects the two beam records only. It is a
    sensitivity parameter, not an empirical covariance claim.
    """

    if not -0.99 < beam_readout_correlation < 0.99:
        raise ValueError("beam correlation must lie strictly between -0.99 and 0.99")
    records = published_lifetime_records()
    covariance = [
        [0.0 for _ in records]
        for _ in records
    ]
    for index, record in enumerate(records):
        covariance[index][index] = record.standard_error_s**2
    shared = (
        beam_readout_correlation
        * records[0].standard_error_s
        * records[2].standard_error_s
    )
    covariance[0][2] = shared
    covariance[2][0] = shared
    return tuple(tuple(row) for row in covariance)


def assimilate_joint_published_records(*, beam_readout_correlation: float = 0.0):
    posterior = initialize_neutron_posterior()
    records = published_lifetime_records()
    return update_ret_posterior(
        posterior,
        joint_published_record_action(),
        tuple(record.lifetime_s for record in records),
        joint_published_covariance(
            beam_readout_correlation=beam_readout_correlation
        ),
    )


def neutron_survival_curve_action(
    storage_times_s: Sequence[float] = (200.0, 1_000.0),
) -> RelationalAction:
    """Nonlinear raw-level survival-fraction observation for bottle studies."""

    times = tuple(float(value) for value in storage_times_s)
    if not times or any(value <= 0.0 for value in times):
        raise ValueError("storage times must be positive")

    def survival(parameters: Mapping[str, float]) -> tuple[float, ...]:
        lifetime = (
            REFERENCE_LIFETIME_S
            + parameters.get("lifetime_offset_s", 0.0)
            + parameters.get("bottle_storage_bias_s", 0.0)
            - parameters.get("spectrum_shift_s", 0.0)
        )
        if lifetime <= 0.0:
            raise ValueError("declared neutron lifetime must remain positive")
        return tuple(math.exp(-storage_time / lifetime) for storage_time in times)

    return RelationalAction(
        "paired_storage_survival_fraction",
        "science",
        tuple(0.0 for _ in times),
        {},
        cost=PracticalCost(time=3.0, money=2.0, risk=0.4, wear=1.0),
        metadata={
            "fixture": "neutron_lifetime",
            "observable": "survival_fraction",
            "storage_times_s": times,
        },
        nonlinear_increment=survival,
    )


def prospective_neutron_actions() -> list[RelationalAction]:
    actions = [
        _lifetime_action(
            "precision_proton_beam",
            kind="science",
            method="beam",
            readout="proton",
            spectrum_coordinate=0.8,
            cost=PracticalCost(time=4.0, money=4.0, risk=1.0, wear=1.0),
        ),
        _lifetime_action(
            "precision_electron_beam",
            kind="science",
            method="beam",
            readout="electron",
            spectrum_coordinate=0.2,
            cost=PracticalCost(time=3.5, money=3.5, risk=1.0, wear=1.0),
        ),
        _lifetime_action(
            "magnetic_bottle_spectral_scan",
            kind="science",
            method="bottle",
            readout="survivor",
            spectrum_coordinate=-0.2,
            cost=PracticalCost(time=3.0, money=2.0, risk=0.5, wear=1.0),
        ),
        _lifetime_action(
            "material_bottle_storage_scan",
            kind="science",
            method="bottle",
            readout="survivor",
            spectrum_coordinate=-1.2,
            cost=PracticalCost(time=2.5, money=2.0, risk=0.8, wear=1.5),
        ),
    ]
    actions.extend(
        [
            RelationalAction(
                "absolute_proton_flux_audit",
                "calibration",
                (0.0,),
                {"proton_pipeline_bias_s": (1.0,)},
                PracticalCost(time=1.5, money=1.0, risk=0.2, wear=0.2),
                {"fixture": "neutron_lifetime", "calibration": "proton_flux_and_readout"},
            ),
            RelationalAction(
                "bottle_loss_audit",
                "calibration",
                (0.0,),
                {"bottle_storage_bias_s": (1.0,)},
                PracticalCost(time=1.5, money=1.0, risk=0.2, wear=0.5),
                {"fixture": "neutron_lifetime", "calibration": "storage_loss"},
            ),
            RelationalAction(
                "spectrum_response_audit",
                "calibration",
                (0.0,),
                {"spectrum_shift_s": (1.0,)},
                PracticalCost(time=1.0, money=0.8, risk=0.1, wear=0.2),
                {"fixture": "neutron_lifetime", "calibration": "spectral_response"},
            ),
            RelationalAction(
                "coincident_beta_survivor_comparison",
                "science",
                (0.0,),
                {"exotic_beta_shift_s": (1.0,)},
                PracticalCost(time=6.0, money=6.0, risk=1.0, wear=1.0),
                {"fixture": "neutron_lifetime", "comparison": "beta_partial_vs_total"},
            ),
        ]
    )
    return actions


def initialize_neutron_posterior():
    return initialize_ret_posterior(
        neutron_models(),
        complexity_penalty=0.8,
        open_model_prior=0.03,
        open_model_scale=30.0,
    )


def assimilate_published_records():
    posterior = initialize_neutron_posterior()
    trace = []
    for record in published_lifetime_records():
        action = published_record_action(record)
        posterior = update_ret_posterior(
            posterior,
            action,
            (record.lifetime_s,),
            record.standard_error_s,
        )
        trace.append(
            {
                "record": record.name,
                "lifetime_s": record.lifetime_s,
                "standard_error_s": record.standard_error_s,
                "model_weights": dict(posterior.model_weights),
            }
        )
    return posterior, trace


def simulate_neutron_observation(
    action: RelationalAction,
    parameters: Mapping[str, float],
    *,
    observation_noise_s: float,
    rng: random.Random,
    misspecification_s: float = 0.0,
) -> tuple[float, ...]:
    mean = response_for_parameters(action, parameters)
    return tuple(
        value + misspecification_s + rng.gauss(0.0, observation_noise_s)
        for value in mean
    )


def run_neutron_lifetime_fixture(seed: int = 2_025) -> dict[str, object]:
    posterior, trace = assimilate_published_records()
    correlation_sensitivity = []
    for assumed_correlation in (-0.5, 0.0, 0.5):
        correlated_posterior = assimilate_joint_published_records(
            beam_readout_correlation=assumed_correlation
        )
        correlation_sensitivity.append(
            {
                "assumed_beam_readout_correlation": assumed_correlation,
                "model_weights": dict(correlated_posterior.model_weights),
            }
        )
    questions = neutron_questions()
    actions = prospective_neutron_actions()
    thresholds = GovernanceThresholds(
        family_probability=0.90,
        novelty_probability=0.99,
        open_model_probability=0.50,
        nuisance_standard_deviation=1.0,
        characterization_relative_uncertainty=0.20,
    )
    literature_state = ret_governance_state(
        posterior,
        questions["relational_family"],
        novel_parameters=("exotic_beta_shift_s",),
        nuisance_parameters=(
            "proton_pipeline_bias_s",
            "bottle_storage_bias_s",
            "spectrum_shift_s",
        ),
        thresholds=thresholds,
    )
    source_objective = SchedulerObjective(
        question=questions["discrepancy_source"],
        nuisance_parameters=(
            "proton_pipeline_bias_s",
            "bottle_storage_bias_s",
            "spectrum_shift_s",
        ),
        nuisance_information_weight=0.8,
        cost_weights=CostWeights(time=0.03, money=0.03, risk=0.02, wear=0.02),
        monte_carlo_samples_per_model=24,
    )
    exotic_objective = SchedulerObjective(
        question=questions["additional_decay_required"],
        nuisance_parameters=("proton_pipeline_bias_s",),
        nuisance_information_weight=0.1,
        cost_weights=CostWeights(time=0.02, money=0.02, risk=0.01, wear=0.01),
        monte_carlo_samples_per_model=24,
    )
    source_ranking = rank_actions(
        posterior, actions, 0.8, source_objective, seed=seed
    )
    exotic_ranking = rank_actions(
        posterior, actions, 0.8, exotic_objective, seed=seed + 100
    )

    source_by_name = {action.name: action for action in actions}
    selected = source_by_name[str(source_ranking[0]["action"])]
    synthetic_truth = {
        "lifetime_offset_s": -2.0,
        "proton_pipeline_bias_s": 9.5,
        "bottle_storage_bias_s": 0.0,
        "spectrum_shift_s": 0.0,
        "exotic_beta_shift_s": 0.0,
    }
    prospective_observation = simulate_neutron_observation(
        selected,
        synthetic_truth,
        observation_noise_s=0.8,
        rng=random.Random(seed),
    )
    posterior_after_next = update_ret_posterior(
        posterior, selected, prospective_observation, 0.8
    )
    after_next_state = ret_governance_state(
        posterior_after_next,
        questions["relational_family"],
        novel_parameters=("exotic_beta_shift_s",),
        nuisance_parameters=(
            "proton_pipeline_bias_s",
            "bottle_storage_bias_s",
            "spectrum_shift_s",
        ),
        thresholds=thresholds,
    )

    attack_action = source_by_name["precision_electron_beam"]
    attacked = update_ret_posterior(
        posterior,
        attack_action,
        (950.0,),
        0.8,
    )
    attack_state = ret_governance_state(
        attacked,
        questions["relational_family"],
        thresholds=thresholds,
    )
    return {
        "fixture": "neutron lifetime discrepancy",
        "reference_lifetime_s": REFERENCE_LIFETIME_S,
        "published_records": tuple(record.__dict__ for record in published_lifetime_records()),
        "published_assimilation_trace": trace,
        "correlation_sensitivity": correlation_sensitivity,
        "literature_posterior": dict(posterior.model_weights),
        "literature_state": literature_state,
        "proton_pipeline_parameters": parameter_summary(
            posterior, "neutron_proton_pipeline"
        ),
        "exotic_endpoint_inclusion_probability": endpoint_inclusion_probability(
            posterior, "exotic_beta_shift_s"
        ),
        "source_question_top_action": {
            **source_ranking[0],
            "metadata": dict(selected.metadata),
        },
        "exotic_question_top_action": {
            **exotic_ranking[0],
            "metadata": dict(
                source_by_name[str(exotic_ranking[0]["action"])].metadata
            ),
        },
        "synthetic_next_observation": {
            "declared_truth": synthetic_truth,
            "action": selected.name,
            "observed_value": prospective_observation[0],
            "posterior": dict(posterior_after_next.model_weights),
            "state": after_next_state,
        },
        "model_failure_attack": {
            "observation_s": 950.0,
            "open_model_probability": attacked.model_weights["M_bottom"],
            "state": attack_state,
        },
    }


def run_neutron_truth_suite(seed: int = 100) -> dict[str, object]:
    """Pressure-test recovery under each declared generative family."""

    scenarios = {
        "common_lifetime": (
            "neutron_common",
            {"lifetime_offset_s": -2.0},
        ),
        "proton_pipeline": (
            "neutron_proton_pipeline",
            {"lifetime_offset_s": -2.0, "proton_pipeline_bias_s": 9.5},
        ),
        "bottle_storage": (
            "neutron_bottle_storage",
            {"lifetime_offset_s": 7.5, "bottle_storage_bias_s": -9.5},
        ),
        "spectrum_state": (
            "neutron_spectrum_state",
            {"lifetime_offset_s": -2.0, "spectrum_shift_s": 7.0},
        ),
        "additional_decay": (
            "neutron_exotic_decay",
            {"lifetime_offset_s": -2.0, "exotic_beta_shift_s": 9.5},
        ),
    }
    objective = SchedulerObjective(
        question=neutron_questions()["discrepancy_source"],
        nuisance_parameters=(
            "proton_pipeline_bias_s",
            "bottle_storage_bias_s",
            "spectrum_shift_s",
        ),
        nuisance_information_weight=0.5,
        cost_weights=CostWeights(time=0.01, money=0.01, risk=0.01, wear=0.01),
        monte_carlo_samples_per_model=16,
    )
    cases = []
    for case_index, (scenario, (expected_model, truth)) in enumerate(scenarios.items()):
        posterior = initialize_neutron_posterior()
        remaining = prospective_neutron_actions()
        rng = random.Random(seed + case_index)
        trace = []
        for step in range(6):
            ranking = rank_actions(
                posterior,
                remaining,
                0.5,
                objective,
                seed=seed + 100 + 10 * case_index + step,
            )
            action_name = str(ranking[0]["action"])
            action = next(item for item in remaining if item.name == action_name)
            remaining.remove(action)
            observation = simulate_neutron_observation(
                action,
                truth,
                observation_noise_s=0.5,
                rng=rng,
            )
            posterior = update_ret_posterior(
                posterior, action, observation, 0.5
            )
            trace.append(
                {
                    "step": step + 1,
                    "action": action.name,
                    "observation": observation[0],
                    "leading_model": max(
                        posterior.model_weights,
                        key=posterior.model_weights.get,
                    ),
                }
            )
        selected_model = max(
            posterior.model_weights, key=posterior.model_weights.get
        )
        cases.append(
            {
                "scenario": scenario,
                "expected_model": expected_model,
                "selected_model": selected_model,
                "expected_model_probability": posterior.model_weights[expected_model],
                "recovered": selected_model == expected_model,
                "trace": trace,
            }
        )
    return {
        "fixture": "neutron lifetime declared-truth recovery",
        "steps_per_case": 6,
        "all_recovered": all(case["recovered"] for case in cases),
        "cases": cases,
    }


if __name__ == "__main__":
    print(
        json.dumps(
            {
                "published_record_fixture": run_neutron_lifetime_fixture(),
                "declared_truth_suite": run_neutron_truth_suite(),
            },
            indent=2,
        )
    )
