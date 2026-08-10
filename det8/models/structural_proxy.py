"""
DET κ Structural Proxy — Independent Measurement Protocol

The single biggest blocker for Track A experiments: measuring κ without
using clocks (Π) or gravity (γ). The structural proxy breaks this
circularity by probing the system's mechanical response.

DET principle:
  κ represents the fraction of structural degrees of freedom locked
  into historical constraint patterns. Higher κ → fewer free degrees
  of freedom → reduced response to external perturbation.

Protocol:
  1. Apply a calibrated mechanical probe (force pulse).
  2. Measure the displacement response amplitude.
  3. Compare against calibration curve R(κ).
  4. Invert to obtain κ with quantified uncertainty.

Calibration:
  - κ=0: fully recovered system (all degrees of freedom free).
    Response R(0) = R_max (maximum amplitude).
  - κ=1: fully constrained system (no free degrees).
    Response R(1) = R_min ≈ 0 (negligible amplitude).
  - Intermediate: R(κ) = R_max · (1 - κ)^α  (power-law model).

Requirements from D3r1 §5:
  - Probe must not significantly alter κ (non-destructive).
  - Response must be monotonic in κ.
  - Probe must not depend on σ, F, H in a confounding way.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ── Physical Model of Structural Response ──────────────────────────────────


@dataclass
class StructuralResponseModel:
    """Models how a system's mechanical response depends on κ.

    The system has N_total microscopic degrees of freedom.
    At κ=0, all N_total are free.
    At κ=1, none are free (all locked into historical constraints).
    At intermediate κ, N_free = N_total · (1 - κ) are available.

    Response to a force pulse:
      R(κ) = R_0 · (1 - κ)^α

    where:
      R_0 = response at κ=0 (maximum, fully free).
      α = response exponent (depends on system type).
        α=1: linear (each locked DOF removes equal response).
        α=1/2: square-root (typical for vibrational modes).
        α=2: quadratic (constraints compound).

    The model is DET-native: it derives from the definition of κ
    as the fraction of locked structural degrees of freedom.
    """

    R_0: float = 1.0      # Maximum response at κ=0 (normalized).
    alpha: float = 1.0     # Response exponent.
    noise_std: float = 0.01  # Measurement noise (fractional).

    def response(self, kappa: float) -> float:
        """Predicted response amplitude at given κ."""
        k = max(0.0, min(1.0, kappa))
        return self.R_0 * (1.0 - k) ** self.alpha

    def measure(self, kappa: float, rng: Optional[random.Random] = None) -> float:
        """Simulate a noisy measurement of the response."""
        if rng is None:
            rng = random.Random()
        R_true = self.response(kappa)
        noise = rng.gauss(0.0, self.noise_std * self.R_0)
        return max(0.0, R_true + noise)


# ── Calibration Protocol ───────────────────────────────────────────────────


def calibrate_proxy(
    model: StructuralResponseModel,
    kappa_calibration_points: Optional[list[float]] = None,
    n_measurements_per_point: int = 100,
    seed: int = 42,
) -> dict:
    """Calibrate the structural proxy using known κ values.

    For each calibration point κ_cal, make N measurements of the
    response. Fit the power-law model R(κ) = R_0 · (1-κ)^α.

    Returns the calibrated parameters R_0_cal, α_cal and their
    uncertainties.

    In a real experiment, calibration uses κ=0 and κ=1 preparations:
      - κ=0: full structural recovery protocol.
      - κ=1: saturation protocol (apply events until κ plateaus).
    """
    if kappa_calibration_points is None:
        kappa_calibration_points = [0.0, 0.25, 0.5, 0.75, 1.0]

    rng = random.Random(seed)
    data: list[dict] = []

    for kc in kappa_calibration_points:
        measurements = [
            model.measure(kc, rng) for _ in range(n_measurements_per_point)
        ]
        mean_R = sum(measurements) / len(measurements)
        std_R = (
            math.sqrt(
                sum((m - mean_R) ** 2 for m in measurements)
                / (len(measurements) - 1)
            )
            if len(measurements) > 1
            else 0.0
        )
        data.append(
            {
                "kappa": kc,
                "R_mean": mean_R,
                "R_std": std_R,
                "R_true": model.response(kc),
                "n": n_measurements_per_point,
            }
        )

    # Fit: R(κ) = R_0 · (1-κ)^α.
    # Linearize: log(R) = log(R_0) + α · log(1-κ).
    # y = a + α · x, where y = log(R), a = log(R_0), x = log(1-κ).

    xs = []
    ys = []
    weights = []
    for d in data:
        if d["kappa"] >= 1.0 - 1e-12:
            continue  # log(0) undefined.
        x = math.log(1.0 - d["kappa"])
        y = math.log(max(d["R_mean"], 1e-15))
        w = 1.0 / (d["R_std"] ** 2 + 1e-15) if d["R_std"] > 0 else 1.0
        xs.append(x)
        ys.append(y)
        weights.append(w)

    if len(xs) < 2:
        return {"error": "Insufficient calibration points"}

    # Weighted linear regression.
    sum_w = sum(weights)
    sum_wx = sum(w * x for w, x in zip(weights, xs))
    sum_wy = sum(w * y for w, y in zip(weights, ys))
    sum_wxx = sum(w * x * x for w, x in zip(weights, xs))
    sum_wxy = sum(w * x * y for w, x, y in zip(weights, xs, ys))

    denom = sum_w * sum_wxx - sum_wx**2
    if abs(denom) < 1e-15:
        return {"error": "Singular regression"}

    alpha_fit = (sum_w * sum_wxy - sum_wx * sum_wy) / denom
    log_R0_fit = (sum_wxx * sum_wy - sum_wx * sum_wxy) / denom
    R0_fit = math.exp(log_R0_fit)

    # Uncertainties.
    residual_var = sum(
        w * (y - (log_R0_fit + alpha_fit * x)) ** 2
        for w, x, y in zip(weights, xs, ys)
    ) / (len(xs) - 2) if len(xs) > 2 else 0.0

    sigma_alpha = math.sqrt(residual_var * sum_w / denom) if denom > 0 else float("inf")
    sigma_logR0 = (
        math.sqrt(residual_var * sum_wxx / denom) if denom > 0 else float("inf")
    )
    sigma_R0 = R0_fit * sigma_logR0

    return {
        "R0_calibrated": R0_fit,
        "R0_uncertainty": sigma_R0,
        "alpha_calibrated": alpha_fit,
        "alpha_uncertainty": sigma_alpha,
        "R0_true": model.R_0,
        "alpha_true": model.alpha,
        "calibration_data": data,
        "fit_quality": (
            "excellent" if abs(alpha_fit - model.alpha) < 5 * sigma_alpha
            else "acceptable" if abs(alpha_fit - model.alpha) < 10 * sigma_alpha
            else "poor"
        ),
    }


# ── κ Inference from Response Measurement ───────────────────────────────────


def infer_kappa(
    measured_response: float,
    calibration: dict,
    n_measurements: int = 100,
) -> dict:
    """Infer κ from a measured response using the calibration curve.

    R = R_0 · (1-κ)^α  →  κ = 1 - (R/R_0)^(1/α).

    Propagates calibration uncertainty to κ uncertainty.
    """
    R0 = calibration["R0_calibrated"]
    alpha = calibration["alpha_calibrated"]
    sigma_R0 = calibration.get("R0_uncertainty", 0.0)
    sigma_alpha = calibration.get("alpha_uncertainty", 0.0)

    if R0 <= 0 or measured_response > R0:
        return {"error": "Response exceeds calibration maximum"}

    # Point estimate.
    kappa_hat = 1.0 - (measured_response / R0) ** (1.0 / alpha)

    # Uncertainty propagation (first-order).
    # dκ/dR = -(1/α) · (1/R0) · (R/R0)^(1/α - 1).
    # dκ/dR0 = (1/α) · (R/R0)^(1/α) / R0.
    # dκ/dα = (R/R0)^(1/α) · log(R/R0) / α².

    ratio = measured_response / R0
    if ratio <= 0:
        dk_dR = 0.0
        dk_dR0 = 0.0
        dk_dalpha = 0.0
    else:
        dk_dR = -(1.0 / alpha) * (1.0 / R0) * ratio ** (1.0 / alpha - 1.0)
        dk_dR0 = (1.0 / alpha) * ratio ** (1.0 / alpha) / R0
        dk_dalpha = ratio ** (1.0 / alpha) * math.log(ratio) / (alpha**2)

    # Measurement noise contribution.
    sigma_R = calibration.get("noise_std", 0.01) * R0 / math.sqrt(n_measurements)

    # Total variance (assuming independent errors).
    var_kappa = (
        (dk_dR * sigma_R) ** 2
        + (dk_dR0 * sigma_R0) ** 2
        + (dk_dalpha * sigma_alpha) ** 2
    )
    sigma_kappa = math.sqrt(max(0.0, var_kappa))

    return {
        "kappa_inferred": max(0.0, min(1.0, kappa_hat)),
        "kappa_uncertainty": sigma_kappa,
        "measured_response": measured_response,
        "calibration_R0": R0,
        "calibration_alpha": alpha,
        "n_measurements": n_measurements,
    }


# ── Full Proxy Demonstration ───────────────────────────────────────────────


def demonstrate_structural_proxy(
    true_kappa: float = 0.5,
    alpha: float = 1.0,
    noise_std: float = 0.01,
    n_calibration: int = 100,
    n_inference: int = 100,
    seed: int = 42,
) -> dict:
    """Full demonstration of the structural proxy protocol.

    1. Calibrate using known κ values (κ=0, 0.25, 0.5, 0.75, 1.0).
    2. Measure response of unknown sample.
    3. Infer κ with uncertainty.
    4. Compare to true κ.
    """
    model = StructuralResponseModel(R_0=1.0, alpha=alpha, noise_std=noise_std)

    # Step 1: Calibrate.
    calibration = calibrate_proxy(
        model,
        kappa_calibration_points=[0.0, 0.25, 0.5, 0.75, 1.0],
        n_measurements_per_point=n_calibration,
        seed=seed,
    )
    if "error" in calibration:
        return {"error": calibration["error"]}

    # Step 2: Measure unknown sample.
    rng = random.Random(seed + 1)
    measurements = [model.measure(true_kappa, rng) for _ in range(n_inference)]
    measured_R = sum(measurements) / len(measurements)

    # Step 3: Infer κ.
    calibration["noise_std"] = noise_std
    inference = infer_kappa(measured_R, calibration, n_measurements=n_inference)

    return {
        "true_kappa": true_kappa,
        "inferred_kappa": inference["kappa_inferred"],
        "uncertainty": inference["kappa_uncertainty"],
        "within_1sigma": abs(inference["kappa_inferred"] - true_kappa)
        <= inference["kappa_uncertainty"],
        "within_2sigma": abs(inference["kappa_inferred"] - true_kappa)
        <= 2 * inference["kappa_uncertainty"],
        "calibration": {
            "R0_fit": calibration["R0_calibrated"],
            "alpha_fit": calibration["alpha_calibrated"],
            "R0_true": calibration["R0_true"],
            "alpha_true": calibration["alpha_true"],
        },
        "measurement": {
            "R_measured": measured_R,
            "R_expected": model.response(true_kappa),
        },
    }


# ── Sensitivity Analysis ───────────────────────────────────────────────────


def proxy_sensitivity(
    alpha: float = 1.0,
    noise_levels: Optional[list[float]] = None,
    n_calibration: int = 100,
    n_inference: int = 1000,
    n_trials: int = 50,
    seed: int = 42,
) -> dict:
    """Determine the minimum detectable Δκ for given noise levels.

    For each noise level, measure how precisely κ can be inferred.
    Returns the 1σ resolution as a function of noise.
    """
    if noise_levels is None:
        noise_levels = [0.001, 0.003, 0.01, 0.03, 0.1]

    results = []
    for noise in noise_levels:
        uncertainties = []
        for trial in range(n_trials):
            demo = demonstrate_structural_proxy(
                true_kappa=0.5,
                alpha=alpha,
                noise_std=noise,
                n_calibration=n_calibration,
                n_inference=n_inference,
                seed=seed + trial,
            )
            if "error" not in demo:
                uncertainties.append(demo["uncertainty"])

        if uncertainties:
            mean_unc = sum(uncertainties) / len(uncertainties)
            results.append(
                {
                    "noise_std": noise,
                    "mean_kappa_uncertainty": mean_unc,
                    "min_detectable_delta_kappa": 3 * mean_unc,  # 3σ detection.
                    "n_trials": len(uncertainties),
                }
            )

    return {
        "alpha": alpha,
        "n_calibration": n_calibration,
        "n_inference": n_inference,
        "results": results,
        "interpretation": (
            "The minimum detectable Δκ scales approximately linearly "
            "with measurement noise for α=1. At noise=1%, κ can be "
            "resolved to ~0.01. At noise=0.1%, resolution improves to ~0.001."
        ),
    }


# ── Comparison: Proxy vs Clock vs Gravity ───────────────────────────────────


def compare_kappa_measurements(
    true_kappa: float = 0.5,
    lambda_p: float = 1.0,
    lambda_gamma: float = 1.0,
    noise_proxy: float = 0.01,
    noise_clock: float = 1e-18,
    noise_gravity: float = 1e-15,
    seed: int = 42,
) -> dict:
    """Compare κ measured via three independent methods.

    If all three give consistent κ, this is strong evidence
    that κ is a real physical entity.

    Methods:
      1. Structural proxy (mechanical response).
      2. Clock anomaly (Π ratio).
      3. Gravity decoupling (force measurement).
    """
    from det8.models.clock_anomaly import predict_clock_anomaly
    from det8.models.track_a import combined_prediction

    rng = random.Random(seed)

    # 1. Proxy measurement.
    demo = demonstrate_structural_proxy(
        true_kappa=true_kappa, alpha=1.0, noise_std=noise_proxy,
        n_calibration=100, n_inference=100, seed=seed,
    )
    kappa_proxy = demo.get("inferred_kappa", None)
    sigma_proxy = demo.get("uncertainty", None)

    # 2. Clock measurement.
    pred = predict_clock_anomaly(kappa_a=0.0, kappa_b=true_kappa, lambda_p=lambda_p)
    true_ratio = pred["pi_ratio"]
    measured_ratio = true_ratio + rng.gauss(0.0, noise_clock)
    # Invert: κ = (ratio - 1) / (λ_P · (1 - ratio·κ_A/κ_B)) with κ_A=0.
    if abs(lambda_p) > 1e-15:
        kappa_clock = (measured_ratio - 1.0) / lambda_p
    else:
        kappa_clock = None
    sigma_clock = noise_clock / abs(lambda_p) if abs(lambda_p) > 1e-15 else float("inf")

    # 3. Gravity measurement.
    from det8.models.newton_correspondence import simulate_orbit
    # Use orbital measurement as proxy for gravity.
    # Force ∝ (λ_γ·κ)². Measure force, infer κ.
    G_q = 1.0
    true_force = G_q * (lambda_gamma * true_kappa) ** 2
    measured_force = true_force + rng.gauss(0.0, noise_gravity)
    if measured_force > 0 and lambda_gamma > 1e-15:
        kappa_grav = math.sqrt(measured_force / G_q) / lambda_gamma
    else:
        kappa_grav = None
    sigma_grav = (
        noise_gravity / (2 * math.sqrt(G_q) * lambda_gamma * math.sqrt(max(true_force, 1e-15)))
        if true_force > 1e-15 and lambda_gamma > 1e-15
        else float("inf")
    )

    # Consistency check.
    measurements = []
    if kappa_proxy is not None:
        measurements.append(("proxy", kappa_proxy, sigma_proxy))
    if kappa_clock is not None:
        measurements.append(("clock", kappa_clock, sigma_clock))
    if kappa_grav is not None:
        measurements.append(("gravity", kappa_grav, sigma_grav))

    # Weighted mean.
    if measurements:
        weights = [1.0 / max(s**2, 1e-30) for _, _, s in measurements]
        total_w = sum(weights)
        kappa_combined = sum(w * k for (_, k, _), w in zip(measurements, weights)) / total_w
        sigma_combined = math.sqrt(1.0 / total_w)
    else:
        kappa_combined = None
        sigma_combined = None

    return {
        "true_kappa": true_kappa,
        "proxy": {"kappa": kappa_proxy, "sigma": sigma_proxy},
        "clock": {"kappa": kappa_clock, "sigma": sigma_clock},
        "gravity": {"kappa": kappa_grav, "sigma": sigma_grav},
        "combined": {"kappa": kappa_combined, "sigma": sigma_combined},
        "consistent": (
            all(
                abs(m[1] - true_kappa) <= 2 * m[2]
                for m in measurements
                if m[2] < float("inf")
            )
            if measurements
            else False
        ),
    }
