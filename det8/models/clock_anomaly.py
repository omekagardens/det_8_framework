"""
DET κ-Π Clock Anomaly — Track A Physical Prediction

The first concrete, falsifiable DET prediction:
  Two identical clocks with different structural history density (κ)
  accumulate different amounts of proper time. The damaged clock
  (higher κ) runs slower by factor 1/(1+λ_P·Δκ).

This is a pure DET prediction with no standard-physics analog.
It is risky because:
  1. Predicts a specific functional form: τ_A/τ_B = (1+λ_P·κ_B)/(1+λ_P·κ_A).
  2. The effect must survive correction for ALL known physical effects.
  3. λ_P must be calibratable from κ=0 and κ=1 preparations.
  4. If no effect is found, DET's Π formula is falsified.

Experimental design:
  - Prepare two identical clocks (atomic clocks, precision ~10⁻¹⁸).
  - Clock A: calibrate to κ=0 (full recovery protocol).
  - Clock B: subject to controlled damage protocol to reach target κ.
  - Measure relative tick rate over extended period.
  - Correct for all known effects (thermal, gravitational, kinematic).
  - Residual difference is the κ-Π anomaly.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from det8.models.det8_core import (
    LAMBDA_P,
    NodeRecord,
    participation_aperture,
    accumulate_proper_time,
)


# ── Clock Model ─────────────────────────────────────────────────────────────


@dataclass
class DETClock:
    """A DET-native clock: a node accumulating proper time via Π.

    The clock's tick rate is determined by its participation aperture Π,
    which depends on κ (structural history), σ (conductivity), F (resource),
    H (coordination load), and γ_v (velocity factor).
    """

    record: NodeRecord = field(default_factory=lambda: NodeRecord(kappa=0.0, sigma=1.0))
    proper_time: float = 0.0

    def tick(self, delta_kappa: float = 1.0, lambda_p: float = LAMBDA_P) -> float:
        """Advance the clock by one coordinate interval.

        Returns the proper-time increment Δτ = Π · Δκ.
        """
        dtau = accumulate_proper_time(self.record, delta_kappa, lambda_p=lambda_p)
        self.proper_time += dtau
        return dtau

    @property
    def current_rate(self) -> float:
        """Current tick rate Π (proper time per coordinate interval)."""
        return participation_aperture(self.record, lambda_p=LAMBDA_P)

    def set_kappa(self, kappa: float) -> None:
        self.record.kappa = max(0.0, min(1.0, kappa))


# ── Clock Anomaly Prediction ────────────────────────────────────────────────


def predict_clock_anomaly(
    kappa_a: float = 0.0,
    kappa_b: float = 0.5,
    lambda_p: float = LAMBDA_P,
) -> dict:
    """Predict the κ-Π clock anomaly.

    The ratio of proper times accumulated by two identical clocks
    differing only in κ is:

      τ_A / τ_B = Π_A / Π_B = (1 + λ_P·κ_B) / (1 + λ_P·κ_A)

    For κ_A = 0 (pristine) and κ_B = 0.5 (damaged):
      τ_A / τ_B = (1 + λ_P·0.5) / (1 + λ_P·0) = 1 + 0.5·λ_P.

    With λ_P = 1 (default, to be calibrated):
      Clock A ticks 1.5× faster than Clock B.
      Over 1 year, Clock B falls behind by 4 months.
    """
    pi_a = 1.0 / (1.0 + lambda_p * kappa_a)  # Baseline factors = 1.
    pi_b = 1.0 / (1.0 + lambda_p * kappa_b)
    ratio = pi_a / pi_b

    # Fractional frequency difference, canonical convention y = (ν_A − ν_B)/ν_A
    # = 1 − Π_B/Π_A = 1 − (1+λ_P·κ_A)/(1+λ_P·κ_B).
    # NOTE: this is the SAME definition used by clock_experiment.det_clock_signal.
    fractional_difference = 1.0 - 1.0 / ratio

    # Effect over 1 year (365.25 days).
    seconds_per_year = 365.25 * 24 * 3600
    delta_t_per_year = seconds_per_year * fractional_difference

    return {
        "kappa": (kappa_a, kappa_b),
        "lambda_p": lambda_p,
        "pi_ratio": ratio,
        "fractional_difference": fractional_difference,
        "delta_per_year_seconds": delta_t_per_year,
        "delta_per_year_days": delta_t_per_year / 86400,
        "formula": f"τ_A/τ_B = (1+λ_P·κ_B)/(1+λ_P·κ_A) = {ratio:.6f}",
    }


# ── Null Model ──────────────────────────────────────────────────────────────


def null_model_prediction(
    kappa_a: float = 0.0,
    kappa_b: float = 0.5,
) -> dict:
    """Null model: κ has no effect on clock rate.

    H₀: Π is independent of κ. Clock rate depends only on σ, F, H, γ_v.
    After correcting for all known physical effects, the residual
    tick-rate difference between Clock A and Clock B is zero.

    τ_A / τ_B = 1.0 (no κ effect).
    """
    return {
        "prediction": "τ_A / τ_B = 1.0",
        "fractional_difference": 0.0,
        "interpretation": (
            "Clocks with different structural history tick at the same rate "
            "after correcting for material, thermal, gravitational, and "
            "kinematic effects. κ is not a physical drag on proper time."
        ),
    }


# ── Required Precision ──────────────────────────────────────────────────────


def required_measurement_precision(
    kappa_b: float = 0.5,
    lambda_p: float = LAMBDA_P,
) -> dict:
    """Estimate the measurement precision required to detect the anomaly.

    The fractional frequency difference is
        y = (ν_A − ν_B)/ν_A = 1 − (1+λ_P·κ_A)/(1+λ_P·κ_B),
    which for κ_A = 0 gives y = λ_P·κ_B / (1 + λ_P·κ_B).

    For λ_P ∈ [0.01, 10] and κ_B ∈ [0.01, 0.5], compute required precision.

    Current best atomic clocks: fractional precision ~10⁻¹⁸ (optical lattice).
    """
    results = []
    for lp in [0.01, 0.1, 1.0, 10.0]:
        delta = lp * kappa_b / (1.0 + lp * kappa_b)  # κ_A = 0.
        detectable = delta > 1e-18  # Above atomic clock noise floor.
        results.append(
            {
                "lambda_p": lp,
                "fractional_difference": delta,
                "detectable_with_best_clocks": detectable,
                "required_precision": f"< {delta:.1e}",
            }
        )

    return {
        "kappa_b": kappa_b,
        "best_clock_precision": 1e-18,
        "results": results,
        "summary": (
            "If λ_P ≥ 10⁻¹⁶, the effect is detectable with current "
            "optical lattice clocks. If λ_P is much smaller, the effect "
            "requires next-generation nuclear clocks (~10⁻¹⁹)."
        ),
    }


# ── Experimental Protocol ───────────────────────────────────────────────────


def experimental_protocol() -> dict:
    """Pre-registration template for the κ-Π clock anomaly experiment.

    Follows the F8-OPEN v2 pre-registration template.
    """
    return {
        "experiment": "κ-Π Clock Anomaly",
        "hypothesis": {
            "H_DET": (
                "Two identical clocks with κ_A ≠ κ_B accumulate proper time "
                "at different rates: τ_A/τ_B = (1+λ_P·κ_B)/(1+λ_P·κ_A). "
                "The effect survives correction for all known physical effects."
            ),
            "H_0": (
                "After correcting for all known physical effects (thermal, "
                "gravitational, kinematic, material), the residual tick-rate "
                "difference is zero. κ does not affect proper time."
            ),
        },
        "system": {
            "clock_type": "Optical lattice atomic clock (¹⁷¹Yb or ⁸⁷Sr).",
            "clock_a": "κ=0 preparation: full structural recovery protocol.",
            "clock_b": "κ=κ_target preparation: controlled damage protocol.",
            "n_clocks": "≥ 3 per κ value (statistics).",
        },
        "observable": {
            "quantity": "Fractional frequency difference y = (ν_A - ν_B)/ν_A.",
            "measurement": "Direct frequency comparison via optical frequency comb.",
            "duration": "≥ 10⁶ seconds (~12 days) for 10⁻¹⁸ statistical resolution.",
        },
        "statistic": {
            "estimator": "Weighted mean of y over measurement period.",
            "null_distribution": "y ~ N(0, σ²) under H₀, where σ² includes all known noise sources.",
            "confidence": "5σ threshold for discovery.",
        },
        "threshold": {
            "discovery": "y > 5σ with correct sign (A faster than B when κ_A < κ_B).",
            "exclusion": "|y| < σ at 95% CL for λ_P > λ_P_min.",
        },
        "controls": {
            "thermal": "Both clocks at identical temperature (mK-level control).",
            "gravitational": "Both clocks at identical gravitational potential (cm-level height control).",
            "kinematic": "Both clocks at rest in laboratory frame.",
            "material": "Same clock design, same materials, same fabrication batch.",
            "aging": "Both clocks have same chronological age; only κ differs.",
        },
        "failure_condition": (
            "If no residual y is detected at 5σ after controlling for all "
            "known effects, H_DET is rejected at the tested λ_P sensitivity. "
            "The Π(κ) formula is falsified for λ_P above the exclusion limit."
        ),
        "kappa_protocol": {
            "kappa_0": (
                "Full structural recovery: isolate clock from all event-generating "
                "interactions, allow natural recovery to κ_eq, verify Π has reached "
                "asymptotic maximum."
            ),
            "kappa_target": (
                "Apply controlled structural damage: subject clock to high rate of "
                "actualization events (e.g., rapid thermal cycling, mechanical stress) "
                "until target κ is reached. Verify via structural proxy measurement."
            ),
            "verification": (
                "Independent κ measurement via structural proxy (calibrated probe "
                "response). Cross-validate that σ, F, H are unchanged."
            ),
        },
    }


# ── Simulation of Clock Anomaly Experiment ──────────────────────────────────


def simulate_clock_experiment(
    kappa_a: float = 0.0,
    kappa_b: float = 0.5,
    n_ticks: int = 10_000_000,
    lambda_p: float = LAMBDA_P,
    noise_level: float = 1e-18,
    seed: int = 42,
) -> dict:
    """Simulate the clock anomaly experiment with realistic noise.

    Two clocks tick for n_ticks coordinate intervals. Clock B has
    higher κ and should accumulate less proper time.

    Adds Gaussian noise at the specified level to simulate
    realistic measurement uncertainty.

    Returns whether the anomaly is detectable at 5σ.
    """
    import random

    rng = random.Random(seed)

    clock_a = DETClock(record=NodeRecord(kappa=kappa_a, sigma=1.0))
    clock_b = DETClock(record=NodeRecord(kappa=kappa_b, sigma=1.0))

    tau_a_true = 0.0
    tau_b_true = 0.0

    for _ in range(n_ticks):
        tau_a_true += clock_a.tick(lambda_p=lambda_p)
        tau_b_true += clock_b.tick(lambda_p=lambda_p)

    # Add measurement noise.
    tau_a_measured = tau_a_true + rng.gauss(0.0, noise_level * tau_a_true)
    tau_b_measured = tau_b_true + rng.gauss(0.0, noise_level * tau_b_true)

    # Fractional frequency difference.
    y_measured = (tau_a_measured - tau_b_measured) / tau_a_measured

    # True anomaly.
    y_true = (tau_a_true - tau_b_true) / tau_a_true
    y_predicted = 1.0 - 1.0 / predict_clock_anomaly(kappa_a, kappa_b, lambda_p)["pi_ratio"]

    # Significance.
    sigma_y = noise_level  # Simplified: noise per measurement ≈ noise level.
    significance = abs(y_measured) / sigma_y if sigma_y > 0 else float("inf")

    return {
        "n_ticks": n_ticks,
        "kappa": (kappa_a, kappa_b),
        "lambda_p": lambda_p,
        "tau_a_true": tau_a_true,
        "tau_b_true": tau_b_true,
        "tau_a_measured": tau_a_measured,
        "tau_b_measured": tau_b_measured,
        "y_true": y_true,
        "y_predicted": y_predicted,
        "y_measured": y_measured,
        "noise_level": noise_level,
        "significance_sigma": significance,
        "detectable_5sigma": significance >= 5.0,
    }


# ── Clock Anomaly Summary ───────────────────────────────────────────────────


def clock_anomaly_summary() -> dict:
    """Complete summary of the κ-Π clock anomaly as a Track A prediction."""
    prediction = predict_clock_anomaly(kappa_a=0.0, kappa_b=0.5, lambda_p=1.0)
    null_model = null_model_prediction()
    precision = required_measurement_precision(kappa_b=0.5)
    protocol = experimental_protocol()

    # Simulate with different noise levels.
    simulations = {}
    for noise, label in [(1e-18, "best_clocks"), (1e-15, "current_commercial")]:
        sim = simulate_clock_experiment(
            kappa_a=0.0, kappa_b=0.5,
            n_ticks=10_000_000, lambda_p=1.0,
            noise_level=noise, seed=42,
        )
        simulations[label] = {
            "detectable": sim["detectable_5sigma"],
            "significance": sim["significance_sigma"],
        }

    return {
        "track": "A — Physical Prediction",
        "prediction": prediction,
        "null_model": null_model,
        "required_precision": precision,
        "experimental_protocol": protocol,
        "simulations": simulations,
        "status": (
            "Ready for pre-registration. The κ-Π clock anomaly is DET's "
            "first concrete, falsifiable physical prediction. It requires "
            "independent κ measurement (structural proxy) to break the "
            "degeneracy between κ and other record variables (σ, F, H). "
            "If λ_P ≥ 10⁻¹⁶, detectable with current optical lattice clocks."
        ),
    }
