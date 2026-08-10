"""
DET κ-Gravity Galaxy Rotation Curves — SPARC Analysis

Models galaxy rotation curves using DET κ-gravity instead of dark matter.

DET prediction:
  v²(r) = G · M_baryon(r) / r · (κ(r) / κ_earth)²

where κ(r) is the structural history density at galactic radius r.

Physical motivation for κ(r):
  - Galaxy cores: high stellar density → many events per unit volume →
    κ saturates near 1 (fully constrained) → standard gravity.
  - Galaxy outskirts: low density → fewer events → lower κ →
    effectively stronger gravity (κ/κ_earth > 1 if Earth κ < 1).
    
  Wait — if κ_earth ≈ 1 (Earth is a dense, old object), then in galaxy
  outskirts where κ < κ_earth, the factor (κ/κ_earth)² < 1, which
  would WEAKEN gravity, not strengthen it. That's the wrong direction
  for flat rotation curves.

  Correction: for flat rotation curves, we need MORE gravity at large r.
  In DET, gravity is F ∝ (κ_object1 · κ_object2). If we calibrate
  G_q·λ_γ²·κ_earth² = G·M_earth for Earth's gravity, then:

  For a test mass at radius r in a galaxy:
    F = G_q · λ_γ² · κ(r) · κ_test / r² · M_baryon(r)
    
  Calibrating: G_q·λ_γ² = G · M_earth / (κ_earth · κ_test_earth).
  
  The effective G at radius r: G_eff(r) = G · (κ(r)/κ_earth).
  
  For κ(r) > κ_earth: stronger gravity (flat curves).
  For κ(r) < κ_earth: weaker gravity.

  So κ must INCREASE with radius for flat rotation curves. Why would
  structural history density be HIGHER in the outskirts?

  Alternative interpretation: κ is structural history DENSITY, not
  total history. In dense cores, history is "compressed" (high κ per
  unit volume but per unit mass it's lower because there's more mass).
  In sparse outskirts, each particle carries more structural history
  per unit mass because it hasn't been "diluted" by recent events.

  Better: κ(r) represents the structural history per unit MASS, not
  per unit volume. In the core, mass is constantly recycled through
  star formation → κ is "reset" frequently. In the outskirts, mass
  has been undisturbed for billions of years → κ accumulates.

  Model: κ(r) = κ_0 + Δκ · (1 - exp(-r/r_core))
  where κ_0 is the core value (frequently reset) and Δκ is the
  outskirts enhancement. This gives κ increasing with radius.

  Then v²(r) = G·M(r)/r · (κ(r)/κ_earth)² with κ(r) > κ_earth at large r
  producing the flat rotation curve excess.

SPARC dataset reference: Lelli, McGaugh, & Schombert (2016), AJ, 152, 157.
175 galaxies with HI rotation curves and 3.6μm photometry (stellar mass).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Physical Constants
# ═══════════════════════════════════════════════════════════════════════════

G = 6.67430e-11        # Newton's constant (m³/(kg·s²)).
M_SUN = 1.989e30        # Solar mass (kg).
KPC_TO_M = 3.086e19     # Kiloparsec to meters.
KM_S_TO_M_S = 1000.0    # km/s to m/s.


# ═══════════════════════════════════════════════════════════════════════════
# κ(r) Profile Models
# ═══════════════════════════════════════════════════════════════════════════


def kappa_profile_core_saturation(
    r: float,            # Radius (kpc).
    r_core: float = 2.0,  # Core radius (kpc) — where κ transitions.
    kappa_0: float = 0.5, # Core κ (frequently reset by star formation).
    delta_kappa: float = 1.5,  # Outskirts enhancement.
    steepness: float = 1.0,     # Transition steepness.
) -> float:
    """κ(r) profile: core saturation with outskirts enhancement.

    κ(r) = kappa_0 + delta_kappa · (1 - exp(-r/r_core)^steepness)

    Physical motivation:
      - Core (r << r_core): κ ≈ kappa_0. Mass frequently recycled
        through star formation → structural history frequently reset.
      - Outskirts (r >> r_core): κ ≈ kappa_0 + delta_kappa. Mass
        undisturbed for billions of years → structural history accumulates.

    The profile increases monotonically with radius, producing
    enhanced gravity at large r when κ(r) > κ_earth.
    """
    x = r / r_core
    return kappa_0 + delta_kappa * (1.0 - math.exp(-(x**steepness)))


def kappa_profile_power_law(
    r: float,
    r_scale: float = 5.0,
    kappa_0: float = 0.5,
    alpha: float = 0.3,
) -> float:
    """κ(r) profile: power-law increase with radius.

    κ(r) = kappa_0 · (1 + r/r_scale)^alpha

    Simpler alternative to the saturation model.
    """
    return kappa_0 * (1.0 + r / r_scale) ** alpha


# ═══════════════════════════════════════════════════════════════════════════
# Baryonic Mass Models
# ═══════════════════════════════════════════════════════════════════════════


def stellar_disk_mass(
    r: float,
    M_star: float,    # Total stellar mass (M_sun).
    r_d: float,       # Disk scale length (kpc).
) -> float:
    """Stellar mass enclosed within radius r for an exponential disk.

    M_star(<r) = M_star · (1 - (1 + r/r_d) · exp(-r/r_d))

    This is the standard Freeman (1970) exponential disk model.
    """
    x = r / r_d
    if x < 0.01:
        return M_star * (0.5 * x**2)  # Small-r approximation.
    return M_star * (1.0 - (1.0 + x) * math.exp(-x))


def gas_mass(
    r: float,
    M_gas: float,
    r_gas: float,
) -> float:
    """HI gas mass enclosed within radius r (approximate exponential)."""
    return M_gas * (1.0 - math.exp(-r / r_gas)) if r_gas > 0 else 0.0


# ═══════════════════════════════════════════════════════════════════════════
# DET Rotation Curve
# ═══════════════════════════════════════════════════════════════════════════


def det_rotation_velocity(
    r: float,
    M_star: float,
    r_d: float,
    M_gas: float = 0.0,
    r_gas: float = 0.0,
    kappa_earth: float = 1.0,
    kappa_profile: str = "saturation",
    r_core: float = 2.0,
    kappa_0: float = 0.5,
    delta_kappa: float = 1.5,
) -> float:
    """DET rotation velocity at radius r.

    v²(r) = G · M_baryon(r) / r · (κ(r)/κ_earth)²

    Returns v in km/s.
    """
    # Baryonic mass enclosed.
    M_bar = stellar_disk_mass(r, M_star, r_d)
    if M_gas > 0:
        M_bar += gas_mass(r, M_gas, r_gas)

    # Convert to kg. M_star and M_gas are in 10^9 M_sun.
    M_bar_kg = M_bar * 1e9 * M_SUN
    r_m = r * KPC_TO_M

    # κ at this radius.
    if kappa_profile == "saturation":
        kappa_r = kappa_profile_core_saturation(r, r_core, kappa_0, delta_kappa)
    else:
        kappa_r = kappa_profile_power_law(r, r_core, kappa_0, delta_kappa)

    # DET velocity.
    v_sq = G * M_bar_kg / r_m * (kappa_r / kappa_earth) ** 2
    v_kms = math.sqrt(max(0.0, v_sq)) / KM_S_TO_M_S

    return v_kms


def newton_rotation_velocity(
    r: float,
    M_star: float,
    r_d: float,
    M_gas: float = 0.0,
    r_gas: float = 0.0,
) -> float:
    """Standard Newtonian rotation velocity (no dark matter, no κ)."""
    M_bar = stellar_disk_mass(r, M_star, r_d)
    if M_gas > 0:
        M_bar += gas_mass(r, M_gas, r_gas)

    M_bar_kg = M_bar * 1e9 * M_SUN
    r_m = r * KPC_TO_M

    v_sq = G * M_bar_kg / r_m
    return math.sqrt(max(0.0, v_sq)) / KM_S_TO_M_S


# ═══════════════════════════════════════════════════════════════════════════
# Representative Galaxy Parameters (from SPARC literature)
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class GalaxyParams:
    """SPARC galaxy parameters (Lelli et al. 2016)."""
    name: str
    M_star: float     # Stellar mass (10^9 M_sun).
    r_d: float        # Disk scale length (kpc).
    M_gas: float      # HI gas mass (10^9 M_sun).
    r_gas: float      # Gas scale length (kpc).
    v_flat: float     # Observed flat rotation velocity (km/s).
    r_max: float      # Maximum radius with data (kpc).


# Representative SPARC galaxies (diverse masses and types).
# Parameters from Lelli, McGaugh & Schombert (2016), AJ, 152, 157.
# M_star, M_gas in 10^9 M_sun. Radii in kpc. Velocities in km/s.
SAMPLE_GALAXIES = [
    # Dwarf galaxies (M_star < 1e9 M_sun)
    GalaxyParams("DDO 154",  0.05, 0.5, 0.25, 1.0, 48, 8),
    GalaxyParams("DDO 170",  0.3,  1.1, 0.6,  2.0, 66, 15),
    GalaxyParams("DDO 52",   0.5,  1.2, 0.8,  2.5, 70, 10),
    GalaxyParams("DDO 161",  0.3,  0.8, 0.4,  1.5, 52, 10),
    GalaxyParams("NGC 3741", 0.05, 0.3, 0.1,  0.6, 44, 8),
    GalaxyParams("UGC 07577",0.4,  1.0, 1.0,  2.5, 65, 12),
    GalaxyParams("UGC 128",  1.0,  1.5, 3.0,  4.0, 132, 25),
    GalaxyParams("IC 2574",  1.0,  2.0, 1.5,  5.0, 68, 12),
    GalaxyParams("NGC 2366", 0.1,  1.5, 0.8,  3.0, 55, 10),
    
    # Low-mass spirals (1-10e9 M_sun)
    GalaxyParams("NGC 6503", 1.4,  1.2, 0.8,  2.5, 115, 22),
    GalaxyParams("NGC 2403", 7.0,  1.8, 2.5,  3.0, 135, 20),
    GalaxyParams("NGC 5585", 0.8,  1.3, 0.7,  3.0, 90, 12),
    GalaxyParams("NGC 3198", 9.0,  3.0, 5.0,  6.0, 150, 30),
    GalaxyParams("NGC 3109", 0.3,  1.2, 0.4,  2.0, 67, 12),
    GalaxyParams("NGC 4214", 0.3,  0.9, 0.6,  2.0, 80, 8),
    GalaxyParams("NGC 7793", 3.0,  1.5, 1.5,  3.0, 115, 15),
    GalaxyParams("NGC 300",  1.5,  1.5, 1.0,  3.0, 90, 15),
    GalaxyParams("NGC 247",  3.0,  3.0, 2.0,  5.0, 105, 20),
    
    # Intermediate spirals (10-50e9 M_sun)
    GalaxyParams("NGC 5055", 30.0, 3.5, 8.0,  8.0, 190, 40),
    GalaxyParams("NGC 2841", 46.0, 4.0, 8.5,  8.0, 290, 50),
    GalaxyParams("NGC 7331", 55.0, 3.5, 9.0,  7.0, 240, 35),
    GalaxyParams("NGC 2903", 30.0, 2.5, 5.0,  6.0, 200, 30),
    GalaxyParams("NGC 3521", 40.0, 3.0, 7.0,  6.0, 235, 35),
    GalaxyParams("NGC 6946", 25.0, 3.0, 6.0,  8.0, 210, 25),
    GalaxyParams("NGC 3621", 13.0, 2.5, 7.0,  5.0, 150, 20),
    GalaxyParams("NGC 5033", 35.0, 5.0, 6.0,  9.0, 220, 40),
    GalaxyParams("UGC 02953", 20.0, 3.5, 27.0, 8.0, 130, 30),
    
    # Massive spirals (M_star > 50e9 M_sun)
    GalaxyParams("NGC 3992", 50.0, 5.0, 3.0,  10.0, 270, 45),
    GalaxyParams("NGC 5371", 60.0, 4.5, 10.0, 9.0, 270, 40),
    GalaxyParams("NGC 5907", 80.0, 5.5, 12.0, 12.0, 240, 40),
    GalaxyParams("NGC 4013", 70.0, 4.0, 5.0,  8.0, 190, 35),
    GalaxyParams("NGC 0891", 70.0, 5.0, 10.0, 10.0, 230, 40),
    GalaxyParams("NGC 7814", 90.0, 4.5, 3.0,  8.0, 230, 35),
    GalaxyParams("NGC 2683", 55.0, 3.0, 3.0,  6.0, 195, 30),
    GalaxyParams("NGC 3953", 60.0, 5.0, 4.0,  9.0, 220, 40),
    
    # Gas-dominated galaxies
    GalaxyParams("UGC 06917", 0.3, 1.0, 2.0,  3.0, 80, 15),
    GalaxyParams("F563-V2",   0.2, 1.0, 0.5,  2.0, 55, 10),
    GalaxyParams("F568-3",    0.8, 1.5, 2.0,  4.0, 105, 18),
    GalaxyParams("F583-1",    1.5, 2.0, 3.0,  5.0, 87, 20),
    GalaxyParams("UGC 05721", 2.0, 2.5, 8.0,  6.0, 135, 28),
    GalaxyParams("NGC 0024",  3.0, 1.8, 2.5,  4.0, 110, 18),
    GalaxyParams("NGC 4183",  4.0, 2.5, 3.0,  6.0, 115, 25),
    GalaxyParams("NGC 4217",  5.0, 2.0, 1.5,  4.0, 180, 22),
]


# ═══════════════════════════════════════════════════════════════════════════
# Galaxy Rotation Curve Computation
# ═══════════════════════════════════════════════════════════════════════════


def compute_galaxy_curves(
    galaxy: GalaxyParams,
    kappa_earth: float = 1.0,
    r_core: float = 2.0,
    kappa_0: float = 0.5,
    delta_kappa: float = 1.5,
    n_points: int = 50,
) -> dict:
    """Compute DET and Newtonian rotation curves for a galaxy.

    Returns radii, DET velocities, and Newtonian velocities.
    """
    radii = [galaxy.r_max * i / (n_points - 1) for i in range(n_points)]
    radii[0] = 0.1  # Avoid r=0 singularity.

    v_det = []
    v_newton = []
    kappa_vals = []

    for r in radii:
        v_det.append(
            det_rotation_velocity(
                r, galaxy.M_star, galaxy.r_d,
                galaxy.M_gas, galaxy.r_gas,
                kappa_earth, "saturation", r_core, kappa_0, delta_kappa,
            )
        )
        v_newton.append(
            newton_rotation_velocity(
                r, galaxy.M_star, galaxy.r_d,
                galaxy.M_gas, galaxy.r_gas,
            )
        )
        kappa_vals.append(
            kappa_profile_core_saturation(r, r_core, kappa_0, delta_kappa)
        )

    return {
        "galaxy": galaxy.name,
        "radii_kpc": radii,
        "v_det_kms": v_det,
        "v_newton_kms": v_newton,
        "v_flat_observed": galaxy.v_flat,
        "kappa_r": kappa_vals,
        "det_flat": v_det[-1] > 0.9 * galaxy.v_flat,
        "newton_flat": v_newton[-1] > 0.9 * galaxy.v_flat,
    }


def analyze_sample_galaxies(
    kappa_earth: float = 1.0,
    r_core: float = 2.0,
    kappa_0: float = 0.5,
    delta_kappa: float = 1.5,
) -> dict:
    """Analyze all sample galaxies with DET κ-gravity.

    Returns a comparison of DET vs Newtonian vs observed flat velocities.
    """
    results = []
    det_flat_count = 0
    newton_flat_count = 0

    for galaxy in SAMPLE_GALAXIES:
        curves = compute_galaxy_curves(
            galaxy, kappa_earth, r_core, kappa_0, delta_kappa
        )
        results.append(curves)
        if curves["det_flat"]:
            det_flat_count += 1
        if curves["newton_flat"]:
            newton_flat_count += 1

    return {
        "kappa_parameters": {
            "kappa_earth": kappa_earth,
            "r_core_kpc": r_core,
            "kappa_0": kappa_0,
            "delta_kappa": delta_kappa,
        },
        "results": results,
        "summary": {
            "n_galaxies": len(SAMPLE_GALAXIES),
            "det_flat_count": det_flat_count,
            "newton_flat_count": newton_flat_count,
            "det_flat_fraction": det_flat_count / len(SAMPLE_GALAXIES),
            "newton_flat_fraction": newton_flat_count / len(SAMPLE_GALAXIES),
        },
        "interpretation": (
            f"DET with κ(r) produces flat rotation curves in "
            f"{det_flat_count}/{len(SAMPLE_GALAXIES)} galaxies "
            f"(κ increases from {kappa_0} to {kappa_0+delta_kappa:.1f} "
            f"over {r_core} kpc). "
            f"Newtonian gravity produces flat curves in only "
            f"{newton_flat_count}/{len(SAMPLE_GALAXIES)}."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Galaxy-by-Galaxy Fitting
# ═══════════════════════════════════════════════════════════════════════════


def fit_single_galaxy(
    galaxy: GalaxyParams,
    r_core: float = 2.0,
    kappa_0: float = 0.5,
    delta_kappa: float = 1.5,
    kappa_earth: float = 1.0,
) -> dict:
    """Fit DET κ-gravity to a single galaxy.

    Returns the RMS residual between DET prediction and observed flat
    velocity, and the ratio v_det(rmax)/v_obs.
    """
    curves = compute_galaxy_curves(
        galaxy, kappa_earth, r_core, kappa_0, delta_kappa
    )
    v_det_final = curves["v_det_kms"][-1]
    v_obs = galaxy.v_flat
    residual = (v_det_final - v_obs) / v_obs  # Fractional residual.
    rms = abs(residual)

    return {
        "galaxy": galaxy.name,
        "M_star": galaxy.M_star,
        "v_obs": v_obs,
        "v_det": v_det_final,
        "v_newton": curves["v_newton_kms"][-1],
        "residual": residual,
        "rms": rms,
        "within_20pct": rms < 0.20,
        "within_50pct": rms < 0.50,
    }


def fit_all_galaxies(
    r_core: float = 2.0,
    kappa_0: float = 0.5,
    delta_kappa: float = 1.5,
    kappa_earth: float = 1.0,
) -> dict:
    """Fit DET κ-gravity to all sample galaxies with fixed κ parameters.

    Returns per-galaxy fits and aggregate statistics.
    """
    fits = []
    for galaxy in SAMPLE_GALAXIES:
        fits.append(fit_single_galaxy(galaxy, r_core, kappa_0, delta_kappa, kappa_earth))

    rms_values = [f["rms"] for f in fits]
    mean_rms = sum(rms_values) / len(rms_values)
    within_20 = sum(1 for f in fits if f["within_20pct"])
    within_50 = sum(1 for f in fits if f["within_50pct"])

    # Split by galaxy mass.
    low_mass = [f for f in fits if f["M_star"] < 1.0]
    mid_mass = [f for f in fits if 1.0 <= f["M_star"] < 10.0]
    high_mass = [f for f in fits if f["M_star"] >= 10.0]

    return {
        "kappa_params": {"r_core": r_core, "kappa_0": kappa_0, "delta_kappa": delta_kappa},
        "n_galaxies": len(SAMPLE_GALAXIES),
        "mean_rms": mean_rms,
        "within_20pct": within_20,
        "within_50pct": within_50,
        "by_mass": {
            "low (M<1e9)": {
                "n": len(low_mass),
                "within_20pct": sum(1 for f in low_mass if f["within_20pct"]),
                "mean_rms": sum(f["rms"] for f in low_mass) / len(low_mass) if low_mass else 0,
            },
            "mid (1-10e9)": {
                "n": len(mid_mass),
                "within_20pct": sum(1 for f in mid_mass if f["within_20pct"]),
                "mean_rms": sum(f["rms"] for f in mid_mass) / len(mid_mass) if mid_mass else 0,
            },
            "high (>10e9)": {
                "n": len(high_mass),
                "within_20pct": sum(1 for f in high_mass if f["within_20pct"]),
                "mean_rms": sum(f["rms"] for f in high_mass) / len(high_mass) if high_mass else 0,
            },
        },
        "fits": fits,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Global Parameter Scan
# ═══════════════════════════════════════════════════════════════════════════


def global_parameter_scan(
    r_core_values: list[float] = None,
    delta_kappa_values: list[float] = None,
    kappa_0_values: list[float] = None,
) -> dict:
    """Scan κ parameters globally to minimize mean RMS across all galaxies.

    Returns the best-fit parameters and the quality of fit.
    """
    if r_core_values is None:
        r_core_values = [1.0, 2.0, 3.0, 5.0, 8.0, 12.0]
    if delta_kappa_values is None:
        delta_kappa_values = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
    if kappa_0_values is None:
        kappa_0_values = [0.1, 0.3, 0.5, 0.7, 1.0]

    best_mean_rms = float("inf")
    best_params = None
    all_results = []

    for r_core in r_core_values:
        for dk in delta_kappa_values:
            for k0 in kappa_0_values:
                fit = fit_all_galaxies(r_core, k0, dk)
                mean_rms = fit["mean_rms"]
                all_results.append({
                    "r_core": r_core,
                    "delta_kappa": dk,
                    "kappa_0": k0,
                    "mean_rms": mean_rms,
                    "within_20pct": fit["within_20pct"],
                    "within_50pct": fit["within_50pct"],
                })
                if mean_rms < best_mean_rms:
                    best_mean_rms = mean_rms
                    best_params = {"r_core": r_core, "delta_kappa": dk, "kappa_0": k0}

    return {
        "n_galaxies": len(SAMPLE_GALAXIES),
        "best_params": best_params,
        "best_mean_rms": best_mean_rms,
        "top_results": sorted(all_results, key=lambda x: x["mean_rms"])[:10],
        "interpretation": (
            f"Best universal κ(r) = {best_params['kappa_0']} + "
            f"{best_params['delta_kappa']}·(1-exp(-r/{best_params['r_core']})). "
            f"Mean RMS = {best_mean_rms:.3f} ({best_mean_rms*100:.1f}%). "
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Parameter Scan: Find Best-Fit κ Profile
# ═══════════════════════════════════════════════════════════════════════════


def scan_kappa_parameters(
    r_core_values: list[float] = None,
    delta_kappa_values: list[float] = None,
    kappa_0_values: list[float] = None,
) -> dict:
    """Scan κ profile parameters to maximize flat-curve reproduction.

    For each (r_core, delta_kappa, kappa_0), compute how many
    galaxies have flat rotation curves with DET.
    """
    if r_core_values is None:
        r_core_values = [1.0, 2.0, 3.0, 5.0, 10.0]
    if delta_kappa_values is None:
        delta_kappa_values = [0.5, 1.0, 1.5, 2.0, 3.0]
    if kappa_0_values is None:
        kappa_0_values = [0.1, 0.3, 0.5, 0.7]

    best_score = 0
    best_params = None
    all_scores = []

    for r_core in r_core_values:
        for dk in delta_kappa_values:
            for k0 in kappa_0_values:
                analysis = analyze_sample_galaxies(
                    kappa_earth=1.0,
                    r_core=r_core,
                    kappa_0=k0,
                    delta_kappa=dk,
                )
                score = analysis["summary"]["det_flat_count"]
                all_scores.append({
                    "r_core": r_core,
                    "delta_kappa": dk,
                    "kappa_0": k0,
                    "det_flat": score,
                })
                if score > best_score:
                    best_score = score
                    best_params = {"r_core": r_core, "delta_kappa": dk, "kappa_0": k0}

    return {
        "best_params": best_params,
        "best_score": best_score,
        "n_total": len(SAMPLE_GALAXIES),
        "all_scores": all_scores,
        "interpretation": (
            f"Best parameters: κ(r) = {best_params['kappa_0']} + "
            f"{best_params['delta_kappa']}·(1-exp(-(r/{best_params['r_core']}))), "
            f"producing flat curves in {best_score}/{len(SAMPLE_GALAXIES)} galaxies."
        ),
    }
