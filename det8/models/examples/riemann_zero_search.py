"""Bounded Riemann-zero statistics search for the RET methodology.

This module searches sign changes of the real Riemann-Siegel Z function on the
critical line and compares normalized spacing summaries with declared
statistical families. It cannot detect zeros away from the critical line and
therefore cannot verify or falsify the Riemann hypothesis.
"""

from __future__ import annotations

import cmath
import json
import math
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


RIEMANN_PROOF_WARNING = (
    "This bounded computation samples Z(t) on Re(s)=1/2. It is evidence about "
    "the sampled zero-spacing record, not a proof of the Riemann hypothesis "
    "and not a search for off-critical-line zeros."
)

_BERNOULLI_2K = (
    1.0 / 6.0,
    -1.0 / 30.0,
    1.0 / 42.0,
    -1.0 / 30.0,
    5.0 / 66.0,
    -691.0 / 2730.0,
    7.0 / 6.0,
    -3617.0 / 510.0,
)


def riemann_zeta(s: complex) -> complex:
    """Evaluate zeta by Euler-Maclaurin continuation for Im(s) >= 0."""

    if s == 1.0:
        raise ValueError("zeta has a pole at s=1")
    # Keep the Euler-Maclaurin tail comfortably inside its decreasing regime.
    # The larger cutoff is still inexpensive at the bounded heights used here
    # and prevents an approximate imaginary residual from shifting a Z root.
    cutoff = max(64, int(abs(s.imag) / 2.0) + 32)
    total = sum(n ** (-s) for n in range(1, cutoff))
    total += cutoff ** (1.0 - s) / (s - 1.0) + 0.5 * cutoff ** (-s)
    rising = s
    for order, bernoulli in enumerate(_BERNOULLI_2K, 1):
        if order > 1:
            rising *= (s + 2 * order - 3) * (s + 2 * order - 2)
        total += (
            bernoulli
            / math.factorial(2 * order)
            * rising
            * cutoff ** (-s - 2 * order + 1)
        )
    return total


def riemann_siegel_theta(height: float) -> float:
    if height <= 0.0:
        raise ValueError("Riemann-Siegel height must be positive")
    return (
        0.5 * height * math.log(height / (2.0 * math.pi))
        - 0.5 * height
        - math.pi / 8.0
        + 1.0 / (48.0 * height)
        + 7.0 / (5760.0 * height**3)
        + 31.0 / (80640.0 * height**5)
    )


def riemann_siegel_z(height: float) -> float:
    zeta = riemann_zeta(0.5 + 1j * height)
    return (cmath.exp(1j * riemann_siegel_theta(height)) * zeta).real


@lru_cache(maxsize=8)
def critical_line_zeros(count: int, scan_step: float = 0.05) -> tuple[float, ...]:
    """Locate a bounded list of simple sign-changing zeros of Z(t)."""

    if count < 1:
        raise ValueError("zero count must be positive")
    if not 0.0 < scan_step <= 0.25:
        raise ValueError("scan step must lie in (0, 0.25]")
    zeros = []
    left = 10.0
    left_value = riemann_siegel_z(left)
    safety_height = 10_000.0
    while len(zeros) < count and left < safety_height:
        right = left + scan_step
        right_value = riemann_siegel_z(right)
        if left_value * right_value < 0.0:
            bracket_left = left
            bracket_right = right
            bracket_value = left_value
            for _ in range(55):
                midpoint = 0.5 * (bracket_left + bracket_right)
                midpoint_value = riemann_siegel_z(midpoint)
                if bracket_value * midpoint_value <= 0.0:
                    bracket_right = midpoint
                else:
                    bracket_left = midpoint
                    bracket_value = midpoint_value
            zeros.append(0.5 * (bracket_left + bracket_right))
        left = right
        left_value = right_value
    if len(zeros) != count:
        raise RuntimeError("bounded critical-line zero scan exhausted its safety range")
    return tuple(zeros)


def _gue_small_gap_probability(threshold: float = 0.5) -> float:
    coefficient = 32.0 / math.pi**2
    exponent = 4.0 / math.pi
    return coefficient * (
        math.sqrt(math.pi)
        * math.erf(math.sqrt(exponent) * threshold)
        / (4.0 * exponent**1.5)
        - threshold
        * math.exp(-exponent * threshold**2)
        / (2.0 * exponent)
    )


def riemann_spacing_models() -> list[RelationalModel]:
    return [
        RelationalModel(
            "riemann_gue_limit",
            "gue_limit",
            {
                "spacing_variance": GaussianPrior(3.0 * math.pi / 8.0 - 1.0, 0.05),
                "small_gap_fraction": GaussianPrior(_gue_small_gap_probability(), 0.04),
            },
            0.0,
        ),
        RelationalModel(
            "riemann_poisson",
            "poisson",
            {
                "spacing_variance": GaussianPrior(1.0, 0.12),
                "small_gap_fraction": GaussianPrior(1.0 - math.exp(-0.5), 0.06),
            },
            0.0,
        ),
        RelationalModel(
            "riemann_finite_height",
            "finite_height_correction",
            {
                "spacing_variance": GaussianPrior(0.14, 0.06),
                "small_gap_fraction": GaussianPrior(0.06, 0.05),
                "finite_height_drift": GaussianPrior(0.0, 0.05),
            },
            1.0,
        ),
        RelationalModel(
            "riemann_overrigid",
            "overrigid",
            {
                "spacing_variance": GaussianPrior(0.04, 0.03),
                "small_gap_fraction": GaussianPrior(0.0, 0.02),
            },
            1.0,
        ),
    ]


def riemann_question() -> Question:
    return Question(
        "zero_spacing_family",
        {model.name: model.family for model in riemann_spacing_models()},
        "Which declared family best describes bounded normalized zero spacings?",
    )


def _height_coordinate(start_index: int) -> float:
    return 2.0 * math.log(max(start_index, 1)) / math.log(97.0) - 1.0


def riemann_window_action(start_index: int, zero_count: int = 24) -> RelationalAction:
    if start_index < 1 or zero_count < 4:
        raise ValueError("Riemann windows require start >= 1 and at least four zeros")
    coordinate = _height_coordinate(start_index)
    return RelationalAction(
        f"riemann_window_{start_index}_{zero_count}",
        "science",
        (0.0, 0.0),
        {
            "spacing_variance": (1.0, 0.0),
            "small_gap_fraction": (0.0, 1.0),
            "finite_height_drift": (coordinate, 0.5 * coordinate),
        },
        cost=PracticalCost(time=(start_index + zero_count) / 100.0),
        metadata={
            "fixture": "riemann_zero_statistics",
            "start_index": start_index,
            "zero_count": zero_count,
            "height_coordinate": coordinate,
        },
    )


def riemann_window_covariance(zero_count: int) -> tuple[tuple[float, float], ...]:
    scale = math.sqrt(24.0 / zero_count)
    variance_sd = 0.08 * scale
    fraction_sd = 0.07 * scale
    cross = 0.25 * variance_sd * fraction_sd
    return (
        (variance_sd**2, cross),
        (cross, fraction_sd**2),
    )


def zero_window_statistics(start_index: int, zero_count: int = 24) -> dict[str, object]:
    pool = critical_line_zeros(max(128, start_index + zero_count - 1))
    window = pool[start_index - 1 : start_index - 1 + zero_count]
    spacings = tuple(
        (right - left) * math.log(left / (2.0 * math.pi)) / (2.0 * math.pi)
        for left, right in zip(window, window[1:])
    )
    spacing_mean = sum(spacings) / len(spacings)
    normalized = tuple(value / spacing_mean for value in spacings)
    variance = sum((value - 1.0) ** 2 for value in normalized) / (
        len(normalized) - 1
    )
    small_gap_fraction = sum(value < 0.5 for value in normalized) / len(normalized)
    residual = max(abs(riemann_zeta(0.5 + 1j * height)) for height in window)
    return {
        "start_index": start_index,
        "zero_count": zero_count,
        "first_height": window[0],
        "last_height": window[-1],
        "spacing_variance": variance,
        "small_gap_fraction": small_gap_fraction,
        "minimum_normalized_spacing": min(normalized),
        "maximum_normalized_spacing": max(normalized),
        "maximum_zeta_residual": residual,
        "observation": (variance, small_gap_fraction),
    }


def run_riemann_zero_search(seed: int = 1_859) -> dict[str, object]:
    posterior = initialize_ret_posterior(
        riemann_spacing_models(),
        complexity_penalty=0.8,
        open_model_prior=0.03,
        open_model_scale=1.0,
    )
    actions = [riemann_window_action(start) for start in (1, 25, 49, 73, 97)]
    noise_by_action = {
        action.name: riemann_window_covariance(int(action.metadata["zero_count"]))
        for action in actions
    }
    objective = SchedulerObjective(
        riemann_question(),
        cost_weights=CostWeights(time=0.02),
        monte_carlo_samples_per_model=24,
    )
    remaining = list(actions)
    trace = []
    for step in range(4):
        ranking = rank_actions(
            posterior,
            remaining,
            {action.name: noise_by_action[action.name] for action in remaining},
            objective,
            seed=seed + step,
        )
        selected_name = str(ranking[0]["action"])
        selected = next(action for action in remaining if action.name == selected_name)
        remaining.remove(selected)
        statistics = zero_window_statistics(
            int(selected.metadata["start_index"]),
            int(selected.metadata["zero_count"]),
        )
        posterior = update_ret_posterior(
            posterior,
            selected,
            statistics["observation"],
            noise_by_action[selected.name],
        )
        trace.append(
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
        "search": "bounded Riemann critical-line zero statistics",
        "proof_warning": RIEMANN_PROOF_WARNING,
        "numerical_method": "Euler-Maclaurin zeta plus sign-bracketed Riemann-Siegel Z roots",
        "candidate_windows": tuple(action.name for action in actions),
        "trace": trace,
        "selected_model": selected_model,
        "final_posterior": dict(posterior.model_weights),
        "selected_model_parameters": (
            parameter_summary(posterior, selected_model)
            if selected_model in posterior.models
            else {}
        ),
        "bounded_zero_count": 128,
        "critical_line_only": True,
        "off_line_zero_search_performed": False,
    }


if __name__ == "__main__":
    print(json.dumps(run_riemann_zero_search(), indent=2))
