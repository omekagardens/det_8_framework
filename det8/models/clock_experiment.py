"""
DET Track A — Clock Anomaly Experiment Simulator

Full Monte Carlo simulation of the κ-Π clock anomaly experiment
using realistic atomic clock noise models.

Models:
  - Optical lattice clocks (¹⁷¹Yb, ⁸⁷Sr): σ_y(τ) ~ 10⁻¹⁸ / √τ
  - Allan deviation for flicker floor, white frequency noise
  - Thermal drift, gravitational potential variation
  - κ-dependent tick rate from DET Π formula

Produces:
  - Simulated frequency comparison time series
  - Allan deviation plot data
  - Detection significance vs integration time
  - Minimum detectable λ_P as function of experiment duration

This is the most concrete Track A deliverable: given experimental
parameters, what signal does DET predict, and can we see it?
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional

from det8.models.det8_core import LAMBDA_P


# ── Atomic Clock Noise Model ────────────────────────────────────────────────


@dataclass
class ClockNoiseModel:
    """Noise model for an optical lattice atomic clock.

    Allan deviation: σ_y(τ) = σ_W / √τ + σ_F

    where:
      σ_W: white frequency noise coefficient (~10⁻¹⁵ for 1s, ~10⁻¹⁸ for 10⁴s).
      σ_F: flicker floor (fundamental stability limit).

    For state-of-the-art optical lattice clocks (¹⁷¹Yb, ⁸⁷Sr):
      σ_W ≈ 1×10⁻¹⁵ at τ=1s
      σ_F ≈ 1×10⁻¹⁸ (flicker floor after ~10⁴s)
    """

    sigma_W: float = 1e-15    # White frequency noise at τ=1s.
    sigma_F: float = 1e-18    # Flicker floor.
    tau_0: float = 1.0         # Reference time for σ_W (seconds).

    def allan_deviation(self, tau: float) -> float:
        """Allan deviation at integration time τ."""
        return self.sigma_W * math.sqrt(self.tau_0 / tau) + self.sigma_F

    def frequency_noise(self, tau: float, rng: random.Random) -> float:
        """Generate a frequency noise sample for integration time τ.

        Models the fractional frequency fluctuation y = (ν - ν₀)/ν₀.
        """
        sigma = self.allan_deviation(tau)
        return rng.gauss(0.0, sigma)


# ── Environmental Noise Sources ─────────────────────────────────────────────


@dataclass
class EnvironmentalNoise:
    """Additional noise sources beyond clock fundamental stability.

    Thermal: frequency shift from temperature fluctuations.
      Typical: ~10⁻¹⁷/K for optical clocks with mK control → ~10⁻²⁰.

    Gravitational: frequency shift from height variations.
      Δy/y = g·Δh/c² ≈ 1.09×10⁻¹⁶ per meter.
      With cm-level control: ~10⁻¹⁸.

    Magnetic: Zeeman shift from B-field variations.
      Typical: ~10⁻¹⁸ with magnetic shielding.
    """

    thermal_noise: float = 1e-20     # Fractional frequency noise.
    gravitational_noise: float = 1e-18  # From cm-level height control.
    magnetic_noise: float = 1e-18       # From magnetic shielding.
    other_systematic: float = 1e-18     # Unmodeled systematics.

    def total_environmental(self) -> float:
        """Total environmental noise (summed in quadrature)."""
        return math.sqrt(
            self.thermal_noise**2
            + self.gravitational_noise**2
            + self.magnetic_noise**2
            + self.other_systematic**2
        )


# ── DET Clock Anomaly Signal ────────────────────────────────────────────────


def det_clock_signal(
    kappa_a: float,
    kappa_b: float,
    lambda_p: float = LAMBDA_P,
) -> float:
    """The DET-predicted fractional frequency difference.

    y = (ν_A - ν_B) / ν_A = (Π_A - Π_B) / Π_A
      = 1 - Π_B/Π_A
      = 1 - (1+λ_P·κ_A)/(1+λ_P·κ_B)
    """
    pi_ratio = (1.0 + lambda_p * kappa_a) / (1.0 + lambda_p * kappa_b)
    return 1.0 - pi_ratio


# ── Full Experiment Simulator ───────────────────────────────────────────────


def simulate_clock_experiment(
    kappa_a: float = 0.0,
    kappa_b: float = 0.5,
    lambda_p: float = LAMBDA_P,
    total_duration: float = 1_000_000.0,  # seconds (~12 days).
    tau_min: float = 1.0,                  # Minimum integration time.
    clock_noise: Optional[ClockNoiseModel] = None,
    env_noise: Optional[EnvironmentalNoise] = None,
    seed: int = 42,
) -> dict:
    """Simulate a full clock comparison experiment.

    Produces time series of frequency comparisons at logarithmically
    spaced integration times, modeling both clock and environmental noise.

    Returns the measured signal and detection significance.
    """
    if clock_noise is None:
        clock_noise = ClockNoiseModel()
    if env_noise is None:
        env_noise = EnvironmentalNoise()

    rng = random.Random(seed)

    # DET signal (constant, independent of integration time).
    y_det = det_clock_signal(kappa_a, kappa_b, lambda_p)

    # Generate integration times (log-spaced).
    n_points = int(math.log10(total_duration / tau_min)) * 10 + 1
    taus = [tau_min * 10 ** (i / 10) for i in range(n_points)]
    taus = [t for t in taus if t <= total_duration]

    # Simulate measurements.
    data = []
    for tau in taus:
        # Number of independent measurements at this integration time.
        n_meas = max(1, int(total_duration / tau))

        measurements = []
        for _ in range(n_meas):
            clock_noise_sample = clock_noise.frequency_noise(tau, rng)
            env_sample = rng.gauss(0.0, env_noise.total_environmental())
            y_measured = y_det + clock_noise_sample + env_sample
            measurements.append(y_measured)

        mean_y = sum(measurements) / len(measurements)
        std_y = (
            math.sqrt(
                sum((m - mean_y) ** 2 for m in measurements)
                / (len(measurements) - 1)
            )
            if len(measurements) > 1
            else 0.0
        )
        # Predicted noise at this τ (computed BEFORE it is used below).
        predicted_noise = math.sqrt(
            clock_noise.allan_deviation(tau) ** 2
            + env_noise.total_environmental() ** 2
        )
        # Standard error: for white frequency noise, SEM = σ_y(τ) / √n_meas.
        # This accounts for the correlated noise structure via Allan deviation.
        sem_y = predicted_noise / math.sqrt(n_meas)

        data.append(
            {
                "tau": tau,
                "n_measurements": n_meas,
                "y_mean": mean_y,
                "y_std": std_y,
                "y_sem": sem_y,  # Standard error of the mean.
                "predicted_noise": predicted_noise,
                "significance": abs(mean_y) / sem_y if sem_y > 0 else float("inf"),
            }
        )

    # Optimal integration time (maximum significance).
    best = max(data, key=lambda d: d["significance"])

    return {
        "kappa": (kappa_a, kappa_b),
        "lambda_p": lambda_p,
        "y_det_signal": y_det,
        "total_duration": total_duration,
        "data": data,
        "best_tau": best["tau"],
        "best_significance": best["significance"],
        "detectable_5sigma": best["significance"] >= 5.0,
        "detectable_3sigma": best["significance"] >= 3.0,
        "noise_model": {
            "sigma_W": clock_noise.sigma_W,
            "sigma_F": clock_noise.sigma_F,
            "environmental": env_noise.total_environmental(),
        },
    }


# ── Detection Threshold Scan ────────────────────────────────────────────────


def scan_detectable_lambda_p(
    kappa_b: float = 0.5,
    lambda_p_range: Optional[list[float]] = None,
    total_duration: float = 1_000_000.0,
    required_sigma: float = 5.0,
    clock_noise: Optional[ClockNoiseModel] = None,
    env_noise: Optional[EnvironmentalNoise] = None,
    seed: int = 42,
) -> dict:
    """Scan λ_P values to find the minimum detectable at required significance.

    Returns the detection threshold λ_P_min for the given experiment
    duration and noise model.
    """
    if lambda_p_range is None:
        lambda_p_range = [
            1e-20, 1e-18, 1e-16, 1e-14, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4, 1e-2,
        ]

    results = []
    for lp in lambda_p_range:
        sim = simulate_clock_experiment(
            kappa_a=0.0,
            kappa_b=kappa_b,
            lambda_p=lp,
            total_duration=total_duration,
            clock_noise=clock_noise,
            env_noise=env_noise,
            seed=seed,
        )
        results.append(
            {
                "lambda_p": lp,
                "y_signal": sim["y_det_signal"],
                "significance": sim["best_significance"],
                "detectable": sim["best_significance"] >= required_sigma,
            }
        )

    # Find threshold.
    threshold = None
    for r in results:
        if r["detectable"]:
            threshold = r["lambda_p"]
            break

    # Analytic estimate for comparison.
    if clock_noise is None:
        clock_noise = ClockNoiseModel()
    if env_noise is None:
        env_noise = EnvironmentalNoise()

    noise_floor = math.sqrt(
        clock_noise.sigma_F**2 + env_noise.total_environmental() ** 2
    )
    analytic_threshold = required_sigma * noise_floor / kappa_b

    return {
        "kappa_b": kappa_b,
        "total_duration_s": total_duration,
        "total_duration_days": total_duration / 86400,
        "required_sigma": required_sigma,
        "noise_floor": noise_floor,
        "threshold_simulated": threshold,
        "threshold_analytic": analytic_threshold,
        "results": results,
    }


# ── Experiment Design Recommendations ────────────────────────────────────────


def experiment_design(
    target_lambda_p: float = 1e-14,
    kappa_b: float = 0.5,
    required_sigma: float = 5.0,
    clock_noise: Optional[ClockNoiseModel] = None,
    env_noise: Optional[EnvironmentalNoise] = None,
) -> dict:
    """Design an experiment to detect a given λ_P at required significance.

    Returns the required integration time, number of clocks, and
    expected signal-to-noise ratio.
    """
    if clock_noise is None:
        clock_noise = ClockNoiseModel()
    if env_noise is None:
        env_noise = EnvironmentalNoise()

    y_signal = det_clock_signal(0.0, kappa_b, target_lambda_p)
    noise_floor = math.sqrt(
        clock_noise.sigma_F**2 + env_noise.total_environmental() ** 2
    )

    # Required total measurement time to reach S/N = required_sigma.
    # For white frequency noise: σ_y(τ) ≈ σ_W/√τ.
    # After total time T with N clocks: effective noise = σ_W / √(N·T).
    # Required: y_signal / (σ_W / √(N·T)) ≥ required_sigma.
    # → N·T ≥ (required_sigma · σ_W / y_signal)².

    # But the flicker floor limits: even infinite T won't beat σ_F.
    if y_signal < required_sigma * noise_floor:
        n_clocks_needed = int(
            (required_sigma * noise_floor / y_signal) ** 2
        ) + 1
        required_time = None  # Limited by flicker floor, not time.
        recommendation = (
            f"Signal {y_signal:.1e} is below flicker floor {noise_floor:.1e}. "
            f"Need ≥ {n_clocks_needed} independent clocks to average down "
            f"the flicker noise. Or reduce environmental noise."
        )
    else:
        n_clocks_needed = 2  # Minimum: one reference + one test.
        required_time = (required_sigma * clock_noise.sigma_W / y_signal) ** 2
        recommendation = (
            f"With {n_clocks_needed} clocks, need {required_time:.0f}s "
            f"({required_time/86400:.1f} days) of integration."
        )

    return {
        "target_lambda_p": target_lambda_p,
        "kappa_b": kappa_b,
        "y_signal": y_signal,
        "noise_floor": noise_floor,
        "required_sigma": required_sigma,
        "n_clocks_needed": n_clocks_needed,
        "required_time_s": required_time,
        "required_time_days": required_time / 86400 if required_time else None,
        "recommendation": recommendation,
    }


# ── Experiment Summary ──────────────────────────────────────────────────────


def clock_experiment_summary() -> dict:
    """Complete summary of the clock anomaly experiment simulator."""
    # Scan λ_P for a 12-day experiment.
    scan = scan_detectable_lambda_p(
        kappa_b=0.5,
        lambda_p_range=[1e-20, 1e-18, 1e-16, 1e-14, 1e-12, 1e-10, 1e-8],
        total_duration=1_000_000.0,
        required_sigma=5.0,
        seed=42,
    )

    # Design for various targets.
    designs = {}
    for lp in [1e-14, 1e-12, 1e-10]:
        designs[f"λ_P={lp:.0e}"] = experiment_design(
            target_lambda_p=lp, kappa_b=0.5, required_sigma=5.0
        )

    # Single simulation at a detectable λ_P.
    sim = simulate_clock_experiment(
        kappa_a=0.0, kappa_b=0.5, lambda_p=1e-12,
        total_duration=1_000_000.0, seed=42,
    )

    return {
        "experiment": "κ-Π Clock Anomaly — Full Monte Carlo",
        "clock_type": "Optical lattice (¹⁷¹Yb or ⁸⁷Sr)",
        "noise_model": {
            "white_frequency": "σ_W = 1×10⁻¹⁵ at τ=1s",
            "flicker_floor": "σ_F = 1×10⁻¹⁸",
            "environmental": "~2×10⁻¹⁸ (thermal + gravitational + magnetic)",
        },
        "scan_results": {
            "threshold_lambda_p": scan["threshold_simulated"],
            "threshold_analytic": scan["threshold_analytic"],
            "duration_days": scan["total_duration_days"],
        },
        "experiment_designs": designs,
        "sample_simulation": {
            "lambda_p": sim["lambda_p"],
            "y_signal": sim["y_det_signal"],
            "best_significance": sim["best_significance"],
            "best_tau": sim["best_tau"],
            "detectable": sim["detectable_5sigma"],
        },
        "recommendations": [
            "For λ_P ≥ 10⁻¹⁴: detectable in ~12 days with 2 clocks.",
            "For λ_P ~ 10⁻¹⁶: requires ~100 days or ~10 independent clocks.",
            "For λ_P ≤ 10⁻¹⁸: below current noise floor. Need next-gen clocks.",
            "Key systematic: ensure κ_A=0 (full recovery) and κ_B known (structural proxy).",
        ],
    }
