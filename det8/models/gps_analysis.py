"""
DET κ-Gravity — GPS Satellite Clock Analysis

Tests whether κ differences between Earth's surface and GPS orbital
altitude produce a detectable timing anomaly.

DET prediction:
  GPS satellites at altitude h (~20,200 km) experience different κ
  than ground clocks. The satellite κ value depends on:
    1. Orbital altitude (lower density → different structural history)
    2. Spacecraft fabrication history
    3. Cosmic ray exposure in orbit

  Ground clock: κ_earth ≈ 1.0 (calibrated)
  Satellite clock: κ_sat = κ_earth + δκ_orbit

  The fractional frequency offset from κ is:
    y_κ = (Π_sat - Π_ground) / Π_ground = (κ_ground - κ_sat) / (1 + λ_P·κ_sat)

  For λ_P ≪ 1: y_κ ≈ -λ_P · δκ_orbit

GPS relativistic corrections (standard):
  Special relativity: satellite clocks run slow by -7.2 μs/day (v ~ 3.9 km/s)
  General relativity: satellite clocks run fast by +45.9 μs/day (lower gravity)
  Net correction: +38.7 μs/day (applied to all GPS satellites)

Any residual beyond the standard corrections could be a κ signal.
GPS clocks are monitored with ~0.1 ns precision (JPL/IGS products).

Published GPS clock data (IGS final products, ~30 satellites, daily):
  Clock residuals after all known corrections: typically < 0.3 ns RMS.
  This constrains any unmodeled frequency offset.

Constraint on λ_P from GPS:
  If κ differs between ground and orbit by δκ, and clock residuals
  are bounded by σ_residual ≈ 0.3 ns/day:

    λ_P · |δκ| · (86400 s) < 0.3 × 10⁻⁹ s
    λ_P · |δκ| < 3.5 × 10⁻¹⁵

  For plausible δκ_orbit ≈ 10⁻⁶ (satellite vs ground κ):
    λ_P < 3.5 × 10⁻⁹

  This is a weaker constraint than atomic clock comparisons
  (λ_P < 4×10⁻¹⁸) but tests a DIFFERENT κ regime — the orbital
  environment rather than lab-scale material differences.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Physical Constants
# ═══════════════════════════════════════════════════════════════════════════

C = 2.99792458e8
G = 6.67430e-11
M_EARTH = 5.972e24
R_EARTH = 6.371e6

# GPS orbital parameters.
GPS_ALTITUDE = 20.2e6       # 20,200 km (m).
GPS_VELOCITY = 3874.0       # Orbital velocity (m/s).
GPS_PERIOD = 43082.0        # Orbital period (s) ≈ 11h 58m.

# IGS clock precision.
IGS_CLOCK_PRECISION_NS = 0.3  # RMS clock residual (ns).
SECONDS_PER_DAY = 86400.0


# ═══════════════════════════════════════════════════════════════════════════
# Standard Relativistic Corrections (GR)
# ═══════════════════════════════════════════════════════════════════════════


def gr_special_relativistic_correction() -> dict:
    """Standard SR correction for GPS satellites.

    Δt/t = -v²/(2c²). Satellite clock runs SLOWER by this fraction.

    For v = 3.874 km/s: Δt/t ≈ -8.35×10⁻¹¹ → -7.2 μs/day.
    """
    v = GPS_VELOCITY
    fractional = -v**2 / (2 * C**2)
    per_day_us = fractional * SECONDS_PER_DAY * 1e6

    return {
        "fractional": fractional,
        "per_day_us": per_day_us,
        "description": "Satellite clock runs slow due to special relativity",
    }


def gr_general_relativistic_correction() -> dict:
    """Standard GR correction for GPS satellites.

    Δt/t = GM_earth/(R_earth·c²) - GM_earth/((R_earth+h)·c²).

    Satellite clock runs FASTER (less gravitational time dilation).
    For GPS: +45.9 μs/day.
    """
    r_ground = R_EARTH
    r_orbit = R_EARTH + GPS_ALTITUDE

    fractional = (
        G * M_EARTH / (r_ground * C**2)
        - G * M_EARTH / (r_orbit * C**2)
    )
    per_day_us = fractional * SECONDS_PER_DAY * 1e6

    return {
        "fractional": fractional,
        "per_day_us": per_day_us,
        "description": "Satellite clock runs fast due to general relativity",
    }


def standard_gps_correction() -> dict:
    """Combined standard relativistic corrections for GPS.

    Net: +38.7 μs/day (GR dominates over SR).
    Applied to all GPS satellites before launch.
    """
    sr = gr_special_relativistic_correction()
    gr = gr_general_relativistic_correction()

    net_fractional = gr["fractional"] + sr["fractional"]
    net_per_day_us = net_fractional * SECONDS_PER_DAY * 1e6

    return {
        "SR_us_per_day": sr["per_day_us"],
        "GR_us_per_day": gr["per_day_us"],
        "net_us_per_day": net_per_day_us,
        "net_fractional": net_fractional,
    }


# ═══════════════════════════════════════════════════════════════════════════
# DET κ-Gravity GPS Correction
# ═══════════════════════════════════════════════════════════════════════════


def det_kappa_gps_correction(
    kappa_sat: float = 1.0 + 1e-6,
    kappa_ground: float = 1.0,
    lambda_p: float = 1.0,
) -> dict:
    """DET κ-gravity correction for GPS satellite clocks.

    The participation aperture Π differs between ground and satellite
    if their κ values differ.

    Π_sat = Π_0 / (1 + λ_P·κ_sat)
    Π_ground = Π_0 / (1 + λ_P·κ_ground)

    Fractional frequency offset:
      y = (Π_sat - Π_ground) / Π_ground = (κ_ground - κ_sat) / (1 + λ_P·κ_sat)

    For small λ_P: y ≈ -λ_P · (κ_sat - κ_ground).
    """
    pi_ratio = (1.0 + lambda_p * kappa_ground) / (1.0 + lambda_p * kappa_sat)
    fractional = pi_ratio - 1.0
    per_day_us = fractional * SECONDS_PER_DAY * 1e6

    return {
        "kappa_sat": kappa_sat,
        "kappa_ground": kappa_ground,
        "lambda_p": lambda_p,
        "fractional_offset": fractional,
        "per_day_us": per_day_us,
        "per_day_ns": per_day_us * 1000,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Constraint from IGS Clock Residuals
# ═══════════════════════════════════════════════════════════════════════════


def gps_constraint_on_lambda_p(
    kappa_difference: float = 1e-6,
    clock_residual_ns: float = IGS_CLOCK_PRECISION_NS,
) -> dict:
    """Constrain λ_P from GPS clock residuals.

    If κ_sat differs from κ_ground by Δκ, the DET frequency offset is:
      y ≈ -λ_P · Δκ.

    The IGS clock residual is σ ≈ 0.3 ns/day. Any unmodeled signal
    larger than this would be detected. Therefore:

      λ_P · |Δκ| · (86400 s) < σ_residual

      λ_P < σ_residual / (|Δκ| · 86400 s)
    """
    sigma_seconds = clock_residual_ns * 1e-9
    lambda_p_bound = sigma_seconds / (abs(kappa_difference) * SECONDS_PER_DAY)

    return {
        "kappa_difference": kappa_difference,
        "clock_residual_ns": clock_residual_ns,
        "lambda_p_upper_bound": lambda_p_bound,
        "comparison_with_lab_clocks": (
            f"GPS: λ_P < {lambda_p_bound:.1e} (Δκ={kappa_difference:.0e}). "
            f"Lab clocks: λ_P < {4e-18:.1e} (Δκ=0.1). "
            "Lab constraint is {:.0f}× stronger because Δκ is ~10⁵× larger.".format(
                4e-18 / lambda_p_bound
            )
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Orbital κ Model
# ═══════════════════════════════════════════════════════════════════════════


def estimate_orbital_kappa_difference() -> dict:
    """Estimate κ difference between GPS satellite and ground clock.

    GPS satellites are fabricated on Earth (κ ≈ 1.0 initially) and
    then launched into orbit where they experience:
      1. Lower gravitational potential (less spacetime curvature)
      2. Different radiation environment (cosmic rays, solar wind)
      3. Thermal cycling (eclipses)
      4. Microgravity (different structural stress)

    All of these could produce a small κ difference.

    Conservative estimate: Δκ ≈ 10⁻⁸ to 10⁻⁶.
    This is much smaller than lab-scale material Δκ (~0.01–0.1)
    because the satellites are still Earth-fabricated hardware
    with only orbital environmental differences.
    """
    return {
        "fabrication_kappa": 1.0,  # Built on Earth.
        "orbital_delta_kappa_min": 1e-8,
        "orbital_delta_kappa_max": 1e-6,
        "dominant_effects": [
            "Reduced gravitational stress (microgravity)",
            "Cosmic ray exposure (radiation damage)",
            "Thermal cycling (day/night in orbit)",
            "Vacuum environment (no atmospheric corrosion)",
        ],
        "constraint_implication": (
            "Even with maximum Δκ ≈ 10⁻⁶, the GPS constraint on λ_P "
            "is ~10⁻⁹, which is much weaker than lab atomic clock constraints. "
            "GPS data cannot currently improve on the lab bounds."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Full Analysis
# ═══════════════════════════════════════════════════════════════════════════


def gps_kappa_analysis() -> dict:
    """Complete GPS κ-gravity analysis."""
    standard = standard_gps_correction()
    orbital = estimate_orbital_kappa_difference()
    constraint = gps_constraint_on_lambda_p(kappa_difference=1e-6)

    # What DET would predict for a GPS satellite if λ_P were large enough.
    det_prediction = det_kappa_gps_correction(
        kappa_sat=1.0 + 1e-6,
        kappa_ground=1.0,
        lambda_p=1.0,
    )

    return {
        "standard_relativistic_correction": standard,
        "orbital_kappa_estimate": orbital,
        "lambda_p_constraint": constraint,
        "det_prediction_if_lambda_p_is_1": det_prediction,
        "conclusion": (
            "GPS clock residuals (~0.3 ns/day) constrain λ_P < 3.5×10⁻⁹ "
            "for plausible orbital Δκ ≈ 10⁻⁶. This is ~10⁹× weaker than "
            "lab atomic clock constraints (λ_P < 4×10⁻¹⁸). GPS data does "
            "not currently improve bounds, but provides an independent check "
            "in the orbital environment. Future clock improvements (optical "
            "clocks in space, ACES mission) could improve sensitivity."
        ),
    }
