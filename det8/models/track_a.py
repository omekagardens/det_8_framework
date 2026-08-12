"""
DET v8.0 — Track A: Physical Predictions and Experimental Designs

Track A is the falsifiable physical calculus. Unlike Track B (ontological
grammar), Track A must produce risky, testable predictions that differ
from standard physics.

Two primary predictions:
  1. κ-Π Clock Anomaly: Clocks with different κ tick at different rates.
  2. κ-Gravity Decoupling: Gravity changes with κ independently of mass.

Includes:
  - Sensitivity analysis: what parameter ranges are testable.
  - Parameter estimation from simulated data.
  - Combined signatures: if both effects exist, joint constraints.
  - Pre-registration templates following F8-OPEN v2 protocol.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Callable, Optional

from det8.models.det8_core import LAMBDA_P, LAMBDA_GAMMA, NodeRecord
from det8.models.clock_anomaly import (
    predict_clock_anomaly,
    null_model_prediction,
)


# ── 1. Clock Anomaly Sensitivity Analysis ──────────────────────────────────


def clock_sensitivity(
    lambda_p_values: Optional[list[float]] = None,
    kappa_values: Optional[list[float]] = None,
    noise_floor: float = 1e-18,
    required_sigma: float = 5.0,
) -> dict:
    """Determine which (λ_P, κ) combinations are detectable.

    For each (λ_P, κ_B) pair with κ_A=0, compute the fractional
    frequency difference and whether it exceeds the noise floor
    at the required significance.

    Returns the detectable region in (λ_P, κ) space.
    """
    if lambda_p_values is None:
        lambda_p_values = [
            1e-20, 1e-18, 1e-16, 1e-14, 1e-12, 1e-10, 1e-8,
            1e-6, 1e-4, 1e-2, 0.1, 1.0, 10.0,
        ]
    if kappa_values is None:
        kappa_values = [1e-6, 1e-4, 1e-2, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]

    detectable = []
    undetectable = []
    boundary: list[dict] = []

    for lp in lambda_p_values:
        for kb in kappa_values:
            pred = predict_clock_anomaly(kappa_a=0.0, kappa_b=kb, lambda_p=lp)
            delta = pred["fractional_difference"]
            sigma_achieved = delta / noise_floor if noise_floor > 0 else float("inf")

            entry = {
                "lambda_p": lp,
                "kappa_b": kb,
                "fractional_difference": delta,
                "sigma": sigma_achieved,
                "detectable": sigma_achieved >= required_sigma,
            }

            if sigma_achieved >= required_sigma:
                detectable.append(entry)
            else:
                undetectable.append(entry)

    # Find the boundary: minimum λ_P detectable for each κ.
    boundary_map: dict[float, float] = {}
    for kb in kappa_values:
        min_detectable = float("inf")
        for lp in lambda_p_values:
            pred = predict_clock_anomaly(kappa_a=0.0, kappa_b=kb, lambda_p=lp)
            delta = pred["fractional_difference"]
            sigma = delta / noise_floor
            if sigma >= required_sigma and lp < min_detectable:
                min_detectable = lp
        if min_detectable < float("inf"):
            boundary_map[kb] = min_detectable

    return {
        "noise_floor": noise_floor,
        "required_sigma": required_sigma,
        "n_detectable": len(detectable),
        "n_undetectable": len(undetectable),
        "boundary": [
            {"kappa_b": kb, "min_lambda_p_detectable": lp}
            for kb, lp in sorted(boundary_map.items())
        ],
        "interpretation": (
            f"At noise floor {noise_floor:.0e}, the boundary λ_P(κ) ≈ "
            f"{noise_floor:.0e} / κ. For κ=1, λ_P ≥ {noise_floor:.0e} is detectable. "
            f"For κ=10⁻⁶, λ_P ≥ {noise_floor/1e-6:.0e} is needed."
        ),
    }


# ── 2. Gravity Decoupling Sensitivity ───────────────────────────────────────


def gravity_sensitivity(
    lambda_gamma_values: Optional[list[float]] = None,
    kappa_values: Optional[list[float]] = None,
    force_resolution: float = 1e-15,  # Best force sensitivity (N).
    separation: float = 0.1,  # meters.
    G_q: float = 1.0,
) -> dict:
    """Determine which (λ_γ, κ) combinations produce detectable gravity changes.

    The DET gravitational force between two identical masses with κ:
      F_DET = G_q · (λ_γ·κ)² / r².

    If κ changes by Δκ, the force changes by:
      ΔF/F ≈ 2·Δκ/κ  (for small changes).

    The force resolution gives the minimum detectable Δκ.
    """
    if lambda_gamma_values is None:
        lambda_gamma_values = [1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1.0, 1e2]
    if kappa_values is None:
        kappa_values = [0.01, 0.1, 0.5, 1.0]

    results = []
    for lg in lambda_gamma_values:
        for k in kappa_values:
            force = G_q * (lg * k) ** 2 / (separation**2)
            detectable = force > force_resolution
            results.append(
                {
                    "lambda_gamma": lg,
                    "kappa": k,
                    "force": force,
                    "detectable": detectable,
                    "required_resolution": f"< {force:.1e} N",
                }
            )

    return {
        "force_resolution": force_resolution,
        "separation": separation,
        "G_q": G_q,
        "n_detectable": sum(1 for r in results if r["detectable"]),
        "n_total": len(results),
        "results": results[:10],
    }


# ── 3. Parameter Estimation from Simulated Data ─────────────────────────────


def estimate_lambda_p(
    measured_ratios: Optional[list[float]],
    kappa_values: list[float],
    kappa_ref: float = 0.0,
    noise_std: float = 0.0,
    seed: int = 42,
) -> dict:
    """Estimate λ_P from a set of clock ratio measurements.

    Given measurements of τ_ref/τ_i for clocks with known κ_i,
    the expected ratio is (1+λ_P·κ_i)/(1+λ_P·κ_ref).

    Uses least-squares fitting (linear after transformation):
      y_i = (ratio_i - 1) / (κ_i - κ_ref · ratio_i)
    which estimates λ_P when the model is correct.

    The supplied `measured_ratios` are USED as the data (this parameter was
    previously ignored — a bug). If `measured_ratios` is None/empty/wrong
    length, synthetic data are generated (with true λ_P = 0.5) for demo
    purposes; `synthetic` is set accordingly.
    """
    rng = random.Random(seed)

    synthetic = (
        measured_ratios is None
        or len(measured_ratios) != len(kappa_values)
    )

    data = []
    true_lp = 0.5 if synthetic else None  # Only meaningful in synthetic mode.
    for i, kb in enumerate(kappa_values):
        if synthetic:
            true_ratio = (1.0 + true_lp * kb) / (1.0 + true_lp * kappa_ref)
            measured_ratio = true_ratio + rng.gauss(0.0, noise_std)
        else:
            true_ratio = None
            measured_ratio = measured_ratios[i]
        data.append(
            {
                "kappa": kb,
                "true_ratio": true_ratio,
                "measured_ratio": measured_ratio,
            }
        )

    # Linearized estimator: y_i = λ_P · x_i + noise.
    # From ratio = (1+λ_P·κ)/(1+λ_P·κ_ref):
    #   ratio · (1+λ_P·κ_ref) = 1+λ_P·κ
    #   ratio - 1 = λ_P·(κ - κ_ref·ratio)
    #   y_i = ratio_i - 1,  x_i = κ_i - κ_ref·ratio_i
    #   λ_P = y_i / x_i.
    xs = []
    ys = []
    for d in data:
        ratio = d["measured_ratio"]
        y = ratio - 1.0
        x = d["kappa"] - kappa_ref * ratio
        xs.append(x)
        ys.append(y)

    # Weighted mean of y/x (weights proportional to 1/σ² ∝ x²).
    weights = [x**2 for x in xs]
    total_weight = sum(weights)
    if total_weight > 1e-15:
        lp_estimated = sum(w * y / x for w, x, y in zip(weights, xs, ys) if abs(x) > 1e-15) / total_weight
    else:
        lp_estimated = 0.0

    # Uncertainty: σ(λ_P) ≈ σ_noise / √(Σ x_i²).
    sigma_lp = noise_std / math.sqrt(sum(x**2 for x in xs)) if sum(x**2 for x in xs) > 0 else float("inf")

    result = {
        "estimated_lambda_p": lp_estimated,
        "uncertainty": sigma_lp,
        "within_1sigma": abs(lp_estimated - true_lp) <= sigma_lp if true_lp is not None else None,
        "data_points": len(data),
        "noise_std": noise_std,
        "synthetic": synthetic,
    }
    if true_lp is not None:
        result["true_lambda_p"] = true_lp
    return result


# ── 4. Combined Signature ──────────────────────────────────────────────────


def combined_prediction(
    kappa_a: float = 0.0,
    kappa_b: float = 0.5,
    lambda_p: float = LAMBDA_P,
    lambda_gamma: float = LAMBDA_GAMMA,
    G_q: float = 1.0,
    separation: float = 1.0,
) -> dict:
    """If both the clock anomaly and gravity decoupling are real,
    they provide joint constraints on (λ_P, λ_γ, κ).

    The clock anomaly measures: τ_A/τ_B = (1+λ_P·κ_B)/(1+λ_P·κ_A).
    The gravity decoupling measures: F ∝ (λ_γ·κ)².

    Together, they can independently determine κ and break the
    degeneracy between G_q and λ_γ.

    This is the DET "smoking gun": two independent measurements
    of the same κ producing consistent values.
    """
    # Clock: ratio → λ_P·κ.
    clock_ratio = (1.0 + lambda_p * kappa_b) / (1.0 + lambda_p * kappa_a)
    # Invert ratio = (1+λ_P·κ_B)/(1+λ_P·κ_A) for κ_B given κ_A:
    #   λ_P·κ_B = ratio·(1+λ_P·κ_A) − 1  ⟹  κ_B = (ratio−1)/λ_P + ratio·κ_A.
    if abs(lambda_p) > 1e-15:
        kappa_clock = (clock_ratio - 1.0) / lambda_p + clock_ratio * kappa_a
    else:
        kappa_clock = None

    # Gravity: force → λ_γ·κ.
    # F = G_q·(λ_γ·κ)²/r² → κ_grav = √(F·r²/G_q) / λ_γ.
    force_det = G_q * (lambda_gamma * kappa_b) ** 2 / (separation**2)
    kappa_grav = math.sqrt(force_det * separation**2 / G_q) / lambda_gamma

    # Null model: no κ effect.
    clock_null = 1.0
    force_null = 0.0

    return {
        "clock": {
            "ratio": clock_ratio,
            "kappa_inferred": kappa_clock,
            "null_ratio": clock_null,
        },
        "gravity": {
            "force": force_det,
            "kappa_inferred": kappa_grav,
            "null_force": force_null,
        },
        "consistency": (
            abs(kappa_clock - kappa_grav) < 1e-12
            if kappa_clock is not None
            else None
        ),
        "smoking_gun": (
            "If κ inferred from clock matches κ inferred from gravity, "
            "and both differ from null model, this is strong evidence "
            "for the DET κ-field as a real physical entity."
        ),
    }


# ── 5. Track A Pre-Registration Summary ────────────────────────────────────


def track_a_preregistration() -> dict:
    """Complete Track A pre-registration package."""
    return {
        "predictions": [
            {
                "name": "κ-Π Clock Anomaly",
                "formula": "τ_A/τ_B = (1+λ_P·κ_B)/(1+λ_P·κ_A)",
                "null": "τ_A/τ_B = 1.0 (after known corrections)",
                "free_parameters": ["λ_P", "κ_A", "κ_B"],
                "measurement": "Atomic clock frequency comparison",
                "status": "Ready for experimental design",
            },
            {
                "name": "κ-Gravity Decoupling",
                "formula": "F = G_q·(λ_γ·κ)²/r²",
                "null": "F = G·M²/r² (standard Newton)",
                "free_parameters": ["G_q", "λ_γ", "κ"],
                "measurement": "Torsion balance or atom interferometry",
                "status": "Ready for experimental design",
            },
            {
                "name": "Combined κ Signature",
                "formula": "κ from clock = κ from gravity",
                "null": "No consistent κ across independent measurements",
                "free_parameters": ["λ_P", "λ_γ", "G_q"],
                "measurement": "Joint clock + gravity experiment",
                "status": "Requires both individual anomalies confirmed",
            },
        ],
        "what_constitutes_discovery": [
            "Clock anomaly detected at ≥ 5σ after all known corrections.",
            "Gravity decoupling detected: ΔF ≠ 0 when ΔM = 0 but Δκ ≠ 0.",
            "κ values inferred from clock and gravity are consistent.",
        ],
        "what_constitutes_falsification": [
            "Clock anomaly excluded at 95% CL for λ_P > λ_P_min (set by experiment precision).",
            "Gravity decoupling excluded: no residual force after controlling for mass changes.",
            "Consistent null results across both experiments → λ_P and λ_γ bounded from above.",
        ],
        "current_limitations": [
            "κ must be independently measurable (structural proxy not yet developed).",
            "λ_P and λ_γ are free parameters — only upper bounds can be set.",
            "Clock experiments require κ=0 and κ=1 preparations (protocol not yet validated).",
            "Gravity experiments require force resolution beyond current technology for small κ.",
        ],
    }
