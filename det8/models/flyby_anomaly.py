"""
DET κ-Gravity Flyby Anomaly Model

Models the Earth flyby anomaly using DET κ-gravity:
  - Earth has κ_earth (calibrated to match Newtonian gravity).
  - Spacecraft has κ_sc ≠ κ_earth (accumulated during space travel).
  - The effective gravitational coupling during flyby differs from
    the calibrated Newtonian value, producing an anomalous Δv.

Physics:
  Newton: F = G · M_earth · m_sc / r²
  DET:    F = G_q · (λ_γ·κ_earth) · (λ_γ·κ_sc) / r²

  Calibrate at Earth's surface:
    G_q · λ_γ² · κ_earth² / R_earth² = G · M_earth / R_earth²
    → G_q · λ_γ² · κ_earth² = G · M_earth  (per unit test mass).

  For spacecraft with κ_sc:
    F_DET = (G · M_earth) · (κ_sc / κ_earth) / r².
    F_Newton = G · M_earth / r².

  Ratio: F_DET / F_Newton = κ_sc / κ_earth.

  If κ_sc < κ_earth: weaker gravity → spacecraft gains velocity.
  If κ_sc > κ_earth: stronger gravity → spacecraft loses velocity.

Known flyby anomalies (approximate):
  Galileo I (1990):  Δv ≈ +3.9 mm/s
  Galileo II (1992): Δv ≈ -4.6 mm/s (but large uncertainty)
  NEAR (1998):      Δv ≈ +13.5 mm/s
  Rosetta (2005):   Δv ≈ +1.8 mm/s
  Cassini (1999):   Δv ≈ -2 mm/s (within uncertainty, ~0)
  Juno (2013):      Δv ≈ 0 mm/s (no anomaly detected)
  Messenger (2005): Δv ≈ +0.02 mm/s (within uncertainty)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Physical Constants
# ═══════════════════════════════════════════════════════════════════════════

G = 6.67430e-11         # Newton's constant (m³/(kg·s²))
M_EARTH = 5.972e24       # Earth mass (kg)
R_EARTH = 6.371e6        # Earth radius (m)
V_EARTH_ESCAPE = 11186.0 # Earth escape velocity at surface (m/s)


# ═══════════════════════════════════════════════════════════════════════════
# Flyby Trajectory Model
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class FlybyParameters:
    """Parameters for an Earth flyby."""

    name: str
    year: int

    # Incoming trajectory.
    v_inf: float          # Hyperbolic excess speed at infinity (m/s).
    perigee_altitude: float  # Closest approach altitude (m).

    # Observed anomaly.
    delta_v_observed: Optional[float]  # Observed Δv (m/s). None if consistent with zero.
    delta_v_uncertainty: float         # Uncertainty in Δv (m/s).

    # Post-flyby.
    v_out_expected: Optional[float] = None  # Expected outgoing v_inf (m/s).
    delta_v_expected: float = 0.0           # Expected Δv from standard gravity.


# Published flyby data (Anderson et al. 2008, PRL; updated with Juno/Messenger).
PUBLISHED_FLYBYS = [
    FlybyParameters(
        name="Galileo I",
        year=1990,
        v_inf=8890.0,
        perigee_altitude=960e3,
        delta_v_observed=3.92e-3,
        delta_v_uncertainty=0.08e-3,
    ),
    FlybyParameters(
        name="Galileo II",
        year=1992,
        v_inf=8900.0,
        perigee_altitude=303e3,
        delta_v_observed=-4.6e-3,  # Negative = spacecraft lost energy.
        delta_v_uncertainty=1.0e-3,
    ),
    FlybyParameters(
        name="NEAR",
        year=1998,
        v_inf=6170.0,
        perigee_altitude=539e3,
        delta_v_observed=13.46e-3,
        delta_v_uncertainty=0.01e-3,
    ),
    FlybyParameters(
        name="Cassini",
        year=1999,
        v_inf=16010.0,
        perigee_altitude=1175e3,
        delta_v_observed=-2.0e-3,  # Marginal, consistent with zero at 2σ.
        delta_v_uncertainty=1.0e-3,
    ),
    FlybyParameters(
        name="Rosetta",
        year=2005,
        v_inf=3830.0,
        perigee_altitude=1954e3,
        delta_v_observed=1.80e-3,
        delta_v_uncertainty=0.05e-3,
    ),
    FlybyParameters(
        name="Messenger",
        year=2005,
        v_inf=4000.0,
        perigee_altitude=2347e3,
        delta_v_observed=0.02e-3,  # Consistent with zero.
        delta_v_uncertainty=0.05e-3,
    ),
    FlybyParameters(
        name="Juno",
        year=2013,
        v_inf=5500.0,
        perigee_altitude=559e3,
        delta_v_observed=0.0,  # No anomaly detected.
        delta_v_uncertainty=0.01e-3,
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# DET κ-Gravity Flyby Model
# ═══════════════════════════════════════════════════════════════════════════


def det_gravity_acceleration(
    r: float,
    kappa_earth: float = 1.0,
    kappa_sc: float = 1.0,
) -> float:
    """DET gravitational acceleration at distance r from Earth's center.

    a_DET = (κ_sc / κ_earth) · a_Newton

    where a_Newton = G·M_earth / r².

    If κ_sc < κ_earth: weaker gravity than Newton predicts.
    If κ_sc > κ_earth: stronger gravity than Newton predicts.
    """
    a_newton = G * M_EARTH / (r * r)
    return a_newton * (kappa_sc / kappa_earth)


def estimate_kappa_ratio_from_flyby(
    flyby: FlybyParameters,
) -> dict:
    """Estimate κ_sc/κ_earth required to explain the flyby anomaly.

    The anomalous Δv is produced by the difference between DET gravity
    and Newtonian gravity during the close-approach phase.

    Simplified model: the velocity change Δv at perigee is approximately:

      Δv_DET ≈ (1 - κ_sc/κ_earth) · v_escape(r_perigee)

    where v_escape = √(2G·M_earth/r_perigee) is the escape velocity
    at the perigee distance. This is a rough estimate; a full trajectory
    integration would be more precise.

    Solving for κ_sc/κ_earth:

      κ_sc/κ_earth ≈ 1 - Δv_obs / v_escape(r_perigee)
    """
    r_perigee = R_EARTH + flyby.perigee_altitude
    v_escape_perigee = math.sqrt(2 * G * M_EARTH / r_perigee)

    if flyby.delta_v_observed is not None:
        kappa_ratio = 1.0 - flyby.delta_v_observed / v_escape_perigee
    else:
        kappa_ratio = 1.0  # No anomaly → κ_sc = κ_earth.

    return {
        "flyby": flyby.name,
        "perigee_altitude_km": flyby.perigee_altitude / 1000,
        "v_escape_perigee_kms": v_escape_perigee / 1000,
        "delta_v_obs_mms": (
            flyby.delta_v_observed * 1000 if flyby.delta_v_observed else 0
        ),
        "kappa_ratio_estimated": kappa_ratio,
        "kappa_sc_lower_than_earth": kappa_ratio < 1.0,
        "delta_kappa_percent": abs(kappa_ratio - 1.0) * 100,
        "interpretation": (
            f"To explain Δv = {flyby.delta_v_observed*1000:.2f} mm/s, "
            f"κ_sc/κ_earth ≈ {kappa_ratio:.10f}. "
            f"Spacecraft κ is {abs(kappa_ratio-1.0)*100:.6f}% "
            f"{'lower' if kappa_ratio < 1 else 'higher'} than Earth's κ."
        ),
    }


def analyze_all_flybys() -> dict:
    """Analyze all published flybys for κ-gravity signatures.

    Key prediction: if the anomaly is real and due to κ-gravity,
    then κ_sc/κ_earth should be consistent across all flybys for
    the same spacecraft (e.g., both Galileo flybys should give
    similar κ_ratio).
    """
    results = []
    for flyby in PUBLISHED_FLYBYS:
        results.append(estimate_kappa_ratio_from_flyby(flyby))

    # Check consistency: Galileo I and II had the same spacecraft.
    galileo_results = [r for r in results if "Galileo" in r["flyby"]]
    consistent = False
    if len(galileo_results) == 2:
        k1 = galileo_results[0]["kappa_ratio_estimated"]
        k2 = galileo_results[1]["kappa_ratio_estimated"]
        # Both should be similar (same spacecraft, same κ_sc).
        consistent = abs(k1 - k2) < 0.0001

    return {
        "model": (
            "Δv ≈ (1 - κ_sc/κ_earth) · v_escape(r_perigee). "
            "Simplified — full trajectory integration would be more precise."
        ),
        "results": results,
        "galileo_consistency": consistent,
        "galileo_note": (
            f"Galileo I: κ_sc < κ_earth (anomalous +Δv). "
            f"Galileo II: κ_sc > κ_earth (anomalous -Δv). "
            "These have OPPOSITE signs — inconsistent with a single κ_sc "
            "for the same spacecraft. Either κ changed between flybys, "
            "or the anomaly is not κ-gravity (or Galileo II uncertainty is large)."
        ) if len(galileo_results) == 2 and not consistent else "",
        "juno_messenger": (
            "Juno and Messenger show no anomaly (Δv ≈ 0). "
            "This implies κ_sc ≈ κ_earth for these spacecraft, "
            "or the anomaly mechanism is not active for all flybys."
        ),
        "conclusion": (
            "The flyby anomaly has inconsistent signs across flybys of "
            "the SAME spacecraft (Galileo I vs II). This is difficult "
            "to explain with a single κ_sc value. Possible explanations: "
            "(a) κ_sc changes during the mission (accumulated from cosmic "
            "ray exposure or thermal cycling between flybys), "
            "(b) the anomaly is not gravitational, "
            "(c) the κ-gravity model needs refinement (e.g., κ depends "
            "on trajectory geometry, not just a scalar)."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Full Trajectory Simulation
# ═══════════════════════════════════════════════════════════════════════════


def simulate_flyby_trajectory(
    v_inf: float,
    perigee_altitude: float,
    kappa_sc: float = 1.0,
    kappa_earth: float = 1.0,
    n_steps: int = 100000,
    dt: float = 0.1,
    integration_radius: float = 1e8,  # Start/stop integration at 100,000 km.
) -> dict:
    """Simulate a flyby trajectory with DET κ-gravity.

    Integrates equations of motion from r_start to perigee and back.
    Compares DET trajectory with Newtonian to compute Δv anomaly.

    Returns the anomalous velocity change at infinity.
    """
    r_perigee = R_EARTH + perigee_altitude

    # Start far from Earth, approaching at v_inf with impact parameter b.
    # For a hyperbolic trajectory: b = r_p · √(1 + 2GM/(r_p·v_inf²)).
    v_inf_sq = v_inf * v_inf
    b = r_perigee * math.sqrt(1 + 2 * G * M_EARTH / (r_perigee * v_inf_sq))

    # Initial position: far away, approaching.
    r_start = integration_radius
    x = -math.sqrt(r_start**2 - b**2) if r_start > b else -r_start
    y = b
    r = math.sqrt(x*x + y*y)

    # Initial velocity: toward Earth with v_inf.
    vx = v_inf * (-x / r)  # Toward Earth along the line of approach.
    vy = v_inf * (-y / r)

    # Integrate DET trajectory.
    x_det, y_det = x, y
    vx_det, vy_det = vx, vy

    for _ in range(n_steps):
        r_det = math.sqrt(x_det**2 + y_det**2)
        if r_det < R_EARTH + 100e3:  # Hit Earth — stop.
            break

        # DET acceleration.
        a_mag = det_gravity_acceleration(r_det, kappa_earth, kappa_sc)
        ax = a_mag * (-x_det / r_det)
        ay = a_mag * (-y_det / r_det)

        vx_det += ax * dt
        vy_det += ay * dt
        x_det += vx_det * dt
        y_det += vy_det * dt

        # Stop when far away and moving away.
        r_det = math.sqrt(x_det**2 + y_det**2)
        if r_det > r_start and vx_det * x_det + vy_det * y_det > 0:
            break

    # Outgoing velocity magnitude.
    v_out_det = math.sqrt(vx_det**2 + vy_det**2)

    # Newtonian outgoing velocity (energy conservation).
    # v_out² = v_inf² + 2GM/r_perigee - 2GM/r_perigee = v_inf² (no net change).
    v_out_newton = v_inf  # Hyperbolic: v_out = v_inf.

    delta_v = v_out_det - v_out_newton

    return {
        "v_inf_kms": v_inf / 1000,
        "perigee_altitude_km": perigee_altitude / 1000,
        "kappa_sc": kappa_sc,
        "kappa_earth": kappa_earth,
        "kappa_ratio": kappa_sc / kappa_earth,
        "v_out_det_kms": v_out_det / 1000,
        "v_out_newton_kms": v_out_newton / 1000,
        "delta_v_mms": delta_v * 1000,
        "delta_v_sign": "positive (gained)" if delta_v > 0 else "negative (lost)",
    }


def scan_kappa_ratio_for_flybys() -> dict:
    """Scan κ_sc/κ_earth to reproduce observed flyby anomalies.

    For each flyby, find the κ_ratio that produces the observed Δv.
    """
    results = []
    for flyby in PUBLISHED_FLYBYS:
        if flyby.delta_v_observed is None:
            continue

        # Try to match the observed Δv by varying κ_ratio.
        # Initial guess from the simple model.
        r_perigee = R_EARTH + flyby.perigee_altitude
        v_escape = math.sqrt(2 * G * M_EARTH / r_perigee)
        kappa_ratio_guess = 1.0 - flyby.delta_v_observed / v_escape

        # Simulate with this κ_ratio.
        sim = simulate_flyby_trajectory(
            v_inf=flyby.v_inf,
            perigee_altitude=flyby.perigee_altitude,
            kappa_sc=kappa_ratio_guess,
            kappa_earth=1.0,
            n_steps=200000,
            dt=0.1,
        )

        results.append({
            "flyby": flyby.name,
            "kappa_ratio_needed": kappa_ratio_guess,
            "delta_v_simulated_mms": sim["delta_v_mms"],
            "delta_v_observed_mms": flyby.delta_v_observed * 1000,
            "match": abs(sim["delta_v_mms"] - flyby.delta_v_observed * 1000) < 0.1,
        })

    return {
        "results": results,
        "interpretation": (
            "If κ_sc/κ_earth is consistent across all flybys, the anomaly "
            "is well-explained by κ-gravity. If different flybys require "
            "different κ_ratios, κ_sc must vary between missions (or the "
            "anomaly has multiple causes)."
        ),
    }
