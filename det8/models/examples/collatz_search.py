"""Bounded Collatz search adapter for the RET methodology.

The exact layer classifies every trajectory as reaching one, exhausting a
declared resource limit, or entering a repeated nontrivial state.  The RET
layer is deliberately narrower: it compares descriptive workload families
for finite blocks of starting values.  Neither layer extrapolates a bounded
calculation into a proof of the Collatz conjecture.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache

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
    parameter_summary,
    update_ret_posterior,
)


COLLATZ_PROOF_WARNING = (
    "Convergence verified through a finite bound is not a proof of the Collatz "
    "conjecture. A resource-limit trajectory is unresolved, not a counterexample; "
    "only an explicitly repeated nontrivial cycle is classified as a verified cycle."
)
COLLATZ_MODEL_WARNING = (
    "RET weights describe finite-range stopping-time workload families under a "
    "declared predictive tolerance; they are not probabilities that the Collatz "
    "conjecture is true or false."
)


@dataclass(frozen=True)
class CollatzTrajectory:
    start: int
    status: str
    steps: int
    peak: int
    terminal: int
    repeated_value: int | None = None

    @property
    def is_counterexample_candidate(self) -> bool:
        return self.status == "verified_cycle"


@lru_cache(maxsize=None)
def _collatz_trajectory_cached(
    start: int,
    max_steps: int,
    max_value: int | None,
) -> CollatzTrajectory:
    if start < 1:
        raise ValueError("Collatz starting value must be a positive integer")
    if max_steps < 0:
        raise ValueError("maximum step count cannot be negative")
    if max_value is not None and max_value < 1:
        raise ValueError("maximum value must be positive when supplied")

    value = start
    peak = start
    seen: set[int] = set()
    steps = 0
    while True:
        if value == 1:
            return CollatzTrajectory(start, "reached_one", steps, peak, value)
        if value in seen:
            return CollatzTrajectory(
                start,
                "verified_cycle",
                steps,
                peak,
                value,
                repeated_value=value,
            )
        if steps >= max_steps:
            return CollatzTrajectory(start, "resource_limit", steps, peak, value)

        seen.add(value)
        value = value // 2 if value % 2 == 0 else 3 * value + 1
        steps += 1
        peak = max(peak, value)
        if max_value is not None and value > max_value:
            return CollatzTrajectory(start, "resource_limit", steps, peak, value)


def collatz_trajectory(
    start: int,
    *,
    max_steps: int = 10_000,
    max_value: int | None = None,
) -> CollatzTrajectory:
    """Return an exact bounded trajectory classification for one starting value."""

    return _collatz_trajectory_cached(start, max_steps, max_value)


def _residue_contrast(residue: int | None, modulus: int) -> float:
    if residue is None:
        return 0.0
    if modulus != 8:
        return 0.0
    return {1: 0.0, 3: 0.0, 5: -1.0, 7: 1.0}.get(residue, 0.0)


def collatz_block_statistics(
    start: int,
    stop: int,
    *,
    residue: int | None = None,
    modulus: int = 8,
    max_steps: int = 10_000,
) -> dict[str, object]:
    """Compute exact trajectory and descriptive statistics on a finite block."""

    if start < 1 or stop < start:
        raise ValueError("Collatz block must satisfy 1 <= start <= stop")
    if modulus < 2:
        raise ValueError("residue modulus must be at least two")
    if residue is not None and not 0 <= residue < modulus:
        raise ValueError("residue must lie in [0, modulus)")

    starts = tuple(
        value
        for value in range(start, stop + 1)
        if residue is None or value % modulus == residue
    )
    if not starts:
        raise ValueError("Collatz block contains no selected starting values")
    trajectories = tuple(
        collatz_trajectory(value, max_steps=max_steps) for value in starts
    )
    completed = tuple(
        trajectory for trajectory in trajectories if trajectory.status == "reached_one"
    )
    counts = {
        status: sum(trajectory.status == status for trajectory in trajectories)
        for status in ("reached_one", "resource_limit", "verified_cycle")
    }
    if completed:
        mean_steps = sum(item.steps for item in completed) / len(completed)
        variance = sum((item.steps - mean_steps) ** 2 for item in completed) / len(
            completed
        )
        standard_deviation = math.sqrt(variance)
        longest = max(completed, key=lambda item: (item.steps, -item.start))
        highest = max(completed, key=lambda item: (item.peak, -item.start))
        observation = (mean_steps, standard_deviation)
    else:
        mean_steps = math.nan
        standard_deviation = math.nan
        longest = None
        highest = None
        observation = None

    return {
        "start": start,
        "stop": stop,
        "residue": residue,
        "modulus": modulus if residue is not None else None,
        "tested_count": len(starts),
        "status_counts": counts,
        "all_reached_one": counts["reached_one"] == len(starts),
        "mean_total_stopping_time": mean_steps,
        "stopping_time_standard_deviation": standard_deviation,
        "maximum_total_stopping_time": longest.steps if longest else None,
        "maximum_total_stopping_time_start": longest.start if longest else None,
        "maximum_peak": highest.peak if highest else None,
        "maximum_peak_start": highest.start if highest else None,
        "verified_cycles": tuple(
            asdict(item)
            for item in trajectories
            if item.status == "verified_cycle"
        ),
        "resource_limited_starts": tuple(
            item.start for item in trajectories if item.status == "resource_limit"
        ),
        "observation": observation,
    }


def collatz_workload_models() -> list[RelationalModel]:
    spread = {"spread_level": GaussianPrior(45.0, 12.0)}
    return [
        RelationalModel(
            "collatz_plateau",
            "bounded_plateau",
            {"mean_level": GaussianPrior(85.0, 30.0), **spread},
            0.0,
        ),
        RelationalModel(
            "collatz_log_affine",
            "log_affine_growth",
            {
                "mean_intercept": GaussianPrior(-15.0, 20.0),
                "log2_slope": GaussianPrior(8.0, 2.5),
                **spread,
            },
            1.0,
        ),
        RelationalModel(
            "collatz_log_quadratic",
            "log_quadratic_growth",
            {
                "mean_intercept": GaussianPrior(10.0, 20.0),
                "log2_squared": GaussianPrior(0.42, 0.15),
                **spread,
            },
            1.0,
        ),
        RelationalModel(
            "collatz_residue_log_affine",
            "residue_sensitive_log_growth",
            {
                "mean_intercept": GaussianPrior(-15.0, 20.0),
                "log2_slope": GaussianPrior(8.0, 2.5),
                "residue_shift": GaussianPrior(0.0, 15.0),
                **spread,
            },
            2.0,
        ),
    ]


def collatz_question() -> Question:
    models = collatz_workload_models()
    return Question(
        "bounded_stopping_time_family",
        {model.name: model.family for model in models},
        "Which declared family best predicts finite-block stopping-time summaries?",
    )


def collatz_block_action(
    start: int,
    stop: int,
    *,
    residue: int | None = None,
    modulus: int = 8,
) -> RelationalAction:
    if start < 1 or stop < start:
        raise ValueError("Collatz block must satisfy 1 <= start <= stop")
    selected_count = sum(
        1
        for value in range(start, stop + 1)
        if residue is None or value % modulus == residue
    )
    if selected_count == 0:
        raise ValueError("Collatz action contains no selected starting values")
    log_coordinate = math.log2(0.5 * (start + stop))
    contrast = _residue_contrast(residue, modulus)
    suffix = "all" if residue is None else f"mod{modulus}_{residue}"
    return RelationalAction(
        f"collatz_block_{start}_{stop}_{suffix}",
        "science",
        (0.0, 0.0),
        {
            "mean_level": (1.0, 0.0),
            "mean_intercept": (1.0, 0.0),
            "log2_slope": (log_coordinate, 0.0),
            "log2_squared": (log_coordinate**2, 0.0),
            "residue_shift": (contrast, 0.0),
            "spread_level": (0.0, 1.0),
        },
        cost=PracticalCost(time=selected_count / 4_096.0),
        metadata={
            "fixture": "bounded_collatz_search",
            "start": start,
            "stop": stop,
            "residue": residue,
            "modulus": modulus,
            "selected_count": selected_count,
            "log2_coordinate": log_coordinate,
            "residue_contrast": contrast,
        },
    )


def collatz_summary_covariance() -> tuple[tuple[float, float], ...]:
    """Declared block-to-block predictive tolerance, not numerical error."""

    mean_sd = 5.0
    spread_sd = 4.0
    cross = 0.15 * mean_sd * spread_sd
    return ((mean_sd**2, cross), (cross, spread_sd**2))


def _observe_action(action: RelationalAction) -> dict[str, object]:
    statistics = collatz_block_statistics(
        int(action.metadata["start"]),
        int(action.metadata["stop"]),
        residue=action.metadata["residue"],
        modulus=int(action.metadata["modulus"]),
    )
    if statistics["observation"] is None:
        raise RuntimeError("selected Collatz block has no completed trajectories")
    return statistics


def bounded_collatz_verification(limit: int = 65_536) -> dict[str, object]:
    """Verify the ordinary Collatz map only for starting values 1..limit."""

    if limit < 1:
        raise ValueError("Collatz verification limit must be positive")
    statistics = collatz_block_statistics(1, limit)
    return {
        "verified_start_range": (1, limit),
        "tested_count": statistics["tested_count"],
        "status_counts": statistics["status_counts"],
        "all_reached_one": statistics["all_reached_one"],
        "maximum_total_stopping_time": statistics["maximum_total_stopping_time"],
        "maximum_total_stopping_time_start": statistics[
            "maximum_total_stopping_time_start"
        ],
        "maximum_peak": statistics["maximum_peak"],
        "maximum_peak_start": statistics["maximum_peak_start"],
        "verified_cycles": statistics["verified_cycles"],
        "resource_limited_starts": statistics["resource_limited_starts"],
        "proof_warning": COLLATZ_PROOF_WARNING,
    }


def run_collatz_search(
    *,
    verification_limit: int = 65_536,
    adaptive_steps: int = 5,
    seed: int = 2_811,
) -> dict[str, object]:
    """Run bounded verification and adaptive finite-range model comparison."""

    posterior = initialize_ret_posterior(
        collatz_workload_models(),
        complexity_penalty=0.8,
        open_model_prior=0.03,
        open_model_scale=150.0,
    )
    covariance = collatz_summary_covariance()
    calibration_actions = (
        collatz_block_action(2, 1_024),
        collatz_block_action(1_025, 4_096),
    )
    calibration_trace = []
    for action in calibration_actions:
        statistics = _observe_action(action)
        posterior = update_ret_posterior(
            posterior,
            action,
            statistics["observation"],
            covariance,
        )
        calibration_trace.append(
            {
                "action": action.name,
                "statistics": statistics,
                "posterior": dict(posterior.model_weights),
            }
        )

    candidates = [
        collatz_block_action(4_097, 8_192),
        collatz_block_action(8_193, 16_384),
        collatz_block_action(16_385, 32_768),
        collatz_block_action(32_769, 65_536),
        *(
            collatz_block_action(8_193, 32_768, residue=residue)
            for residue in (1, 3, 5, 7)
        ),
    ]
    if not 0 <= adaptive_steps <= len(candidates):
        raise ValueError("adaptive step count exceeds available Collatz actions")
    objective = SchedulerObjective(
        collatz_question(),
        cost_weights=CostWeights(time=0.002),
        monte_carlo_samples_per_model=24,
    )
    remaining = list(candidates)
    adaptive_trace = []
    for step in range(adaptive_steps):
        ranking = rank_actions(
            posterior,
            remaining,
            covariance,
            objective,
            seed=seed + step,
        )
        selected_name = str(ranking[0]["action"])
        selected = next(action for action in remaining if action.name == selected_name)
        remaining.remove(selected)
        statistics = _observe_action(selected)
        posterior = update_ret_posterior(
            posterior,
            selected,
            statistics["observation"],
            covariance,
        )
        adaptive_trace.append(
            {
                "step": step + 1,
                "action": selected.name,
                "ranking": ranking[0],
                "statistics": statistics,
                "posterior": dict(posterior.model_weights),
            }
        )

    selected_model = max(posterior.model_weights, key=posterior.model_weights.get)
    return {
        "search": "bounded Collatz verification and stopping-time workload search",
        "proof_warning": COLLATZ_PROOF_WARNING,
        "model_warning": COLLATZ_MODEL_WARNING,
        "trajectory_outcomes": (
            "reached_one",
            "resource_limit",
            "verified_cycle",
        ),
        "verification": bounded_collatz_verification(verification_limit),
        "predictive_tolerance_covariance": covariance,
        "predictive_tolerance_is_computational_error": False,
        "calibration_trace": calibration_trace,
        "adaptive_trace": adaptive_trace,
        "selected_model": selected_model,
        "final_posterior": dict(posterior.model_weights),
        "selected_model_parameters": (
            parameter_summary(posterior, selected_model)
            if selected_model in posterior.models
            else {}
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_collatz_search(), indent=2))
