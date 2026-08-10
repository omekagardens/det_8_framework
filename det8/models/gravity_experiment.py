"""
DET Track A — Gravity Decoupling Experiment Simulator

Full Monte Carlo simulation of the κ-gravity decoupling experiment.
Tests the DET prediction that gravitational force changes when κ
changes, independently of mass/energy changes.

Experimental approaches modeled:
  1. Torsion balance: measure force between test masses before/after κ-recovery.
  2. Atom interferometry: measure local g with κ-modified test masses.
  3. Orbital timing: measure period changes in a binary system under κ-recovery.

Key DET prediction:
  F = G_q · (λ_γ·κ)² / r²
  After κ-recovery (κ → 0): F → 0 while M (standard mass) unchanged.
  Standard gravity: F = G·M²/r² — no change when M is constant.

This is the gravity analogue of the clock anomaly: two independent
measurements of the same κ-field.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ── Torsion Balance Model ───────────────────────────────────────────────────


@dataclass
class TorsionBalance:
    """A torsion balance experiment for measuring weak forces.

    Typical sensitivity: ~10⁻¹⁵ N at 1m separation (Eöt-Wash group).
    Next-generation: ~10⁻¹⁷ N (atom interferometry-based).
    """

    force_resolution: float = 1e-15    # Minimum detectable force (N).
    separation: float = 0.1             # Test mass separation (m).
    integration_time: float = 1000.0    # Measurement integration (s).

    def force_noise(self, rng: random.Random) -> float:
        """Generate a force measurement noise sample."""
        return rng.gauss(0.0, self.force_resolution)

    def measure_force(
        self,
        true_force: float,
        rng: random.Random,
    ) -> float:
        """Measure a force with realistic noise."""
        return true_force + self.force_noise(rng)


# ── DET Gravity Signal ──────────────────────────────────────────────────────


def det_gravity_force(
    kappa_1: float,
    kappa_2: float,
    lambda_gamma: float = 1.0,
    G_q: float = 1.0,
    separation: float = 0.1,
) -> float:
    """DET gravitational force between two masses.

    F = G_q · (λ_γ·κ_1) · (λ_γ·κ_2) / r².
    """
    gamma_1 = lambda_gamma * kappa_1
    gamma_2 = lambda_gamma * kappa_2
    return G_q * gamma_1 * gamma_2 / (separation**2)


def newton_gravity_force(
    mass_1: float,
    mass_2: float,
    G: float = 6.67430e-11,
    separation: float = 0.1,
) -> float:
    """Standard Newtonian gravitational force."""
    return G * mass_1 * mass_2 / (separation**2)


# ── Gravity Decoupling Experiment ───────────────────────────────────────────


def simulate_gravity_experiment(
    kappa_before: float = 0.5,
    kappa_after: float = 0.0,
    lambda_gamma: float = 1.0,
    G_q: float = 1.0,  # Use normalized units for toy; calibrate to G for real.
    mass_kg: float = 1.0,
    separation: float = 0.1,
    force_resolution: float = 1e-15,
    n_measurements: int = 100,
    seed: int = 42,
) -> dict:
    """Simulate a gravity decoupling experiment.

    Measure gravitational force between two identical test masses
    before and after κ-recovery on one mass. Standard mass is unchanged.

    DET predicts: F ∝ κ². After κ → 0, F → 0.
    Standard physics: F unchanged (mass unchanged).
    """
    rng = random.Random(seed)
    balance = TorsionBalance(
        force_resolution=force_resolution,
        separation=separation,
    )

    # Before recovery.
    F_det_before = det_gravity_force(kappa_before, kappa_before, lambda_gamma, G_q, separation)
    F_newton = newton_gravity_force(mass_kg, mass_kg, separation=separation)

    # After recovery (κ → 0 on one mass; the other stays at κ_before for detection).
    # Actually: both masses start with κ_before. We recover one to κ_after.
    F_det_after = det_gravity_force(kappa_after, kappa_before, lambda_gamma, G_q, separation)

    # True DET force change.
    delta_F_det = F_det_before - F_det_after

    # Simulate measurements.
    before_measurements = [
        balance.measure_force(F_det_before, rng) for _ in range(n_measurements)
    ]
    after_measurements = [
        balance.measure_force(F_det_after, rng) for _ in range(n_measurements)
    ]

    mean_before = sum(before_measurements) / len(before_measurements)
    mean_after = sum(after_measurements) / len(after_measurements)
    delta_F_measured = mean_before - mean_after

    # Uncertainty (standard error of the difference).
    var_before = (
        sum((m - mean_before) ** 2 for m in before_measurements)
        / (len(before_measurements) - 1)
        if len(before_measurements) > 1
        else 0.0
    )
    var_after = (
        sum((m - mean_after) ** 2 for m in after_measurements)
        / (len(after_measurements) - 1)
        if len(after_measurements) > 1
        else 0.0
    )
    se_diff = math.sqrt(
        var_before / len(before_measurements) + var_after / len(after_measurements)
    )

    significance = abs(delta_F_measured) / se_diff if se_diff > 0 else float("inf")

    # Null model: no force change (δF = 0).
    null_significance = abs(delta_F_measured) / se_diff if se_diff > 0 else 0.0

    return {
        "kappa": (kappa_before, kappa_after),
        "lambda_gamma": lambda_gamma,
        "F_det_before": F_det_before,
        "F_det_after": F_det_after,
        "delta_F_det_true": delta_F_det,
        "delta_F_measured": delta_F_measured,
        "se_difference": se_diff,
        "significance": significance,
        "detectable_5sigma": significance >= 5.0,
        "newton_force": F_newton,
        "newton_no_change": True,  # Newton predicts zero change.
        "force_resolution": force_resolution,
        "n_measurements": n_measurements,
    }


# ── Sensitivity Scan ────────────────────────────────────────────────────────


def scan_gravity_sensitivity(
    kappa_before: float = 0.5,
    lambda_gamma_range: Optional[list[float]] = None,
    separation: float = 0.1,
    force_resolution: float = 1e-15,
    G_q: float = 1.0,
    n_measurements: int = 100,
    required_sigma: float = 5.0,
    seed: int = 42,
) -> dict:
    """Scan λ_γ to find the minimum detectable for gravity decoupling.

    The DET force change is ΔF = G_q·λ_γ²·(κ_before² - κ_after²) / r².

    For κ_before=0.5, κ_after=0: ΔF = G_q·λ_γ²·0.25 / r².
    """
    if lambda_gamma_range is None:
        lambda_gamma_range = [
            1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4,
        ]

    results = []
    for lg in lambda_gamma_range:
        sim = simulate_gravity_experiment(
            kappa_before=kappa_before,
            kappa_after=0.0,
            lambda_gamma=lg,
            G_q=G_q,
            separation=separation,
            force_resolution=force_resolution,
            n_measurements=n_measurements,
            seed=seed,
        )
        results.append(
            {
                "lambda_gamma": lg,
                "F_det_before": sim["F_det_before"],
                "delta_F": sim["delta_F_det_true"],
                "significance": sim["significance"],
                "detectable": sim["detectable_5sigma"],
            }
        )

    # Analytic threshold.
    delta_F_min = required_sigma * force_resolution / math.sqrt(n_measurements)
    # ΔF = G_q·λ_γ²·(κ²_before - κ²_after) / r².
    # λ_γ_min = √(ΔF_min · r² / (G_q · (κ²_before - κ²_after))).
    kappa_sq_diff = kappa_before**2 - 0.0**2
    if kappa_sq_diff > 1e-15 and G_q > 0:
        analytic_lg = math.sqrt(
            delta_F_min * separation**2 / (G_q * kappa_sq_diff)
        )
    else:
        analytic_lg = float("inf")

    # Find simulated threshold.
    threshold = None
    for r in results:
        if r["detectable"]:
            threshold = r["lambda_gamma"]
            break

    return {
        "kappa_before": kappa_before,
        "force_resolution": force_resolution,
        "n_measurements": n_measurements,
        "required_sigma": required_sigma,
        "threshold_simulated": threshold,
        "threshold_analytic": analytic_lg,
        "results": results,
    }


# ── Calibration to Real Parameters ──────────────────────────────────────────


def calibrate_gravity_to_real(
    earth_mass_kg: float = 5.972e24,
    earth_kappa: float = 1.0,
    G_measured: float = 6.67430e-11,
    separation: float = 0.1,
    test_mass_kg: float = 1.0,
) -> dict:
    """Calibrate DET gravity parameters to match measured gravity.

    If Earth has κ≈1, and we measure F = G·M_earth·m_test/r²,
    then the DET force must match:
      G_q · (λ_γ·κ_earth) · (λ_γ·κ_test) / r² = G · M_earth · m_test / r².

    With κ_earth=1, κ_test (unknown for the test mass):
      G_q · λ_γ² · κ_test = G · M_earth · m_test.

    This gives ONE constraint on THREE unknowns (G_q, λ_γ, κ_test).
    The structural proxy measures κ_test independently, breaking one degeneracy.
    The clock anomaly measures λ_P (different coupling), providing a second constraint.
    G_q then remains as the single free gravitational parameter.
    """
    # Constraint: G_q · λ_γ² · κ_test = G · M_earth · m_test.
    constraint_rhs = G_measured * earth_mass_kg * test_mass_kg

    return {
        "constraint": f"G_q · λ_γ² · κ_test = G · M_earth · m_test = {constraint_rhs:.4e}",
        "constraint_value": constraint_rhs,
        "free_parameters": ["G_q", "λ_γ", "κ_test"],
        "degeneracy_broken_by": [
            "κ_test from structural proxy",
            "λ_P from clock anomaly (different coupling, constrains κ independently)",
            "G_q remains as the single free gravitational parameter",
        ],
        "example_calibration": {
            "if_kappa_test_equals_1": {
                "G_q_times_lambda_gamma_sq": constraint_rhs,
                "if_lambda_gamma_equals_1": f"G_q = {constraint_rhs:.4e}",
                "if_G_q_equals_G": f"λ_γ = {math.sqrt(constraint_rhs/G_measured):.4e}",
            },
        },
    }


# ── Experiment Summary ──────────────────────────────────────────────────────


def gravity_experiment_summary() -> dict:
    """Complete summary of the gravity decoupling experiment."""
    scan = scan_gravity_sensitivity(
        kappa_before=0.5,
        lambda_gamma_range=[1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6, 1e-5],
        separation=0.1,
        force_resolution=1e-15,
        n_measurements=100,
        seed=42,
    )

    calibration = calibrate_gravity_to_real()

    return {
        "experiment": "κ-Gravity Decoupling — Full Monte Carlo",
        "apparatus": "Torsion balance (Eöt-Wash type) or atom interferometry",
        "sensitivity": {
            "force_resolution": "10⁻¹⁵ N (current), 10⁻¹⁷ N (next-gen)",
            "separation": "0.1 m (laboratory scale)",
        },
        "scan_results": {
            "threshold_lambda_gamma": scan["threshold_simulated"],
            "threshold_analytic": scan["threshold_analytic"],
        },
        "calibration": calibration,
        "detectable_scenarios": [
            "If λ_γ·κ ~ G·M (i.e., κ-gravity matches standard gravity strength), trivially detectable.",
            "If λ_γ·κ ≪ G·M, the effect is below current force resolution.",
            "The experiment constrains λ_γ from below: λ_γ ≥ threshold for given κ.",
        ],
        "synergy_with_clock": (
            "The clock anomaly measures λ_P·κ. Gravity measures λ_γ·κ. "
            "Together, they determine κ independently and break the "
            "G_q/λ_γ degeneracy. The structural proxy provides a third "
            "independent measurement. Three-way consistency is the smoking gun."
        ),
    }
