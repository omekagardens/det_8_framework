"""
DET-Native κ(r) Derivation from Galaxy Formation Physics

DEPRECATED (Round 6, Option B): the gravity-modification program is retired.
κ does NOT couple to gravity, so a κ(r) rotation-curve profile is no longer
needed. Retained for historical audit (including the F6 wrong-sign finding).

Derives κ(r) from DET primitives using known galaxy observables:
  - Star formation rate surface density Σ_SFR(r)
  - Stellar mass surface density Σ_*(r)
  - Gas surface density Σ_gas(r)
  - Inside-out growth: r_SFR > r_d (SFR more extended than mass)

DET mechanism:
  κ = structural history per unit mass = (gentle events) / (violent resets)

  "Gentle" events (secular evolution, gas accretion): add to κ.
    Rate ∝ Σ_*(r) · t_age (cumulative stellar mass formed).

  "Violent" events (supernovae, major mergers): reset κ.
    Rate ∝ Σ_SFR(r) (recent star formation drives SNe).

  κ(r) ∝ Σ_*(r)·t_age / (Σ_SFR(r)·t_reset + κ_min)

  ⚠ SIGN CAVEAT (Round 3, verified): for the observed inside-out growth
  (r_SFR > r_d), Σ_SFR decays SLOWER than Σ_*, so this formula gives κ(r)
  DECREASING with radius — the OPPOSITE of what flat rotation curves need.
  The "reset ∝ recent SFR" mechanism has the wrong radial profile. A correct
  derivation needs a reset driver MORE concentrated than the stars (r_reset <
  r_d), or an accumulation term MORE extended than the SFR.

Prediction: κ(r) can be predicted from observed Σ_*(r), Σ_SFR(r), and
galaxy age — independently of rotation curve fitting. This makes DET
predictive, not just fitting (subject to the sign caveat above).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Galaxy Observables (from SPARC + literature)
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class GalaxyObservables:
    """Observed galaxy properties that determine κ(r).

    All surface densities are exponential with scale lengths.
    Inside-out growth: r_SFR > r_d (observed in most spirals).
    """

    name: str
    M_star: float          # Total stellar mass (10^9 M_sun).
    r_d: float             # Stellar disk scale length (kpc).
    M_gas: float           # Total gas mass (10^9 M_sun).
    r_gas: float           # Gas disk scale length (kpc).
    SFR: float             # Total star formation rate (M_sun/yr).
    r_SFR: float           # SFR scale length (kpc). Typically > r_d.
    age: float = 10.0      # Galaxy age (Gyr).
    V_flat: float = 0.0    # Observed flat velocity (km/s).


# ═══════════════════════════════════════════════════════════════════════════
# DET κ(r) from Galaxy Properties
# ═══════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════
# Surface-density profiles (observable inputs)
# ═══════════════════════════════════════════════════════════════════════════


def stellar_surface_density(
    r: float,
    M_star: float,
    r_d: float,
) -> float:
    """Σ_*(r) = M_star·exp(−r/r_d) / (2π r_d²)  [10⁹ M_sun/kpc²]."""
    if r_d <= 0.0:
        return 0.0
    return M_star * math.exp(-r / r_d) / (2.0 * math.pi * r_d**2)


def sfr_surface_density(
    r: float,
    SFR: float,
    r_SFR: float,
) -> float:
    """Σ_SFR(r) = SFR·exp(−r/r_SFR) / (2π r_SFR²)  [M_sun/yr/kpc²]."""
    if r_SFR <= 0.0:
        return 0.0
    return SFR * math.exp(-r / r_SFR) / (2.0 * math.pi * r_SFR**2)


# ═══════════════════════════════════════════════════════════════════════════
# DET κ(r) from Galaxy Properties (F6 — actually implemented)
# ═══════════════════════════════════════════════════════════════════════════


def kappa_from_galaxy_properties(
    r: float,
    galaxy: GalaxyObservables,
    t_reset: float = 0.01,     # SN reset timescale (Gyr).
    kappa_min: float = 1e-6,   # floor to avoid 0/0 in the outskirts.
    q_sat: float = 1.0,        # saturation scale (κ = Q/(Q+q_sat)).
) -> float:
    """κ(r) from the documented F6 formula, using the real observables.

    Q(r) = Σ_*(r)·t_age / (Σ_SFR(r)·t_reset + κ_min)
    κ(r) = Q(r) / (Q(r) + q_sat)

    M_star, SFR, age, r_d, r_SFR are now actually used (the previous
    implementation only used r_SFR and two fitted constants).

    ⚠ HONEST FINDING (Round 3): for the observed inside-out growth
    (r_SFR > r_d), Σ_SFR decays SLOWER than Σ_*, so Q — and hence κ —
    DECREASES with radius. The "reset ∝ recent SFR" mechanism therefore
    gives the WRONG radial direction for flat rotation curves. See
    `radial_gradient_check`. This is not a bug in the code; it is a
    physics problem in the proposed derivation.
    """
    s_star = stellar_surface_density(r, galaxy.M_star, galaxy.r_d)
    s_sfr = sfr_surface_density(r, galaxy.SFR, galaxy.r_SFR)
    Q = s_star * galaxy.age / (s_sfr * t_reset + kappa_min)
    return Q / (Q + q_sat)


def radial_gradient_check(
    galaxy: GalaxyObservables,
    r_max: float = 30.0,
    t_reset: float = 0.01,
    kappa_min: float = 1e-6,
    q_sat: float = 1.0,
) -> dict:
    """Does κ(r) increase or decrease with radius under the F6 formula?

    Flat rotation curves require κ(r) to INCREASE with radius (more gravity
    in the outskirts). This check reports whether the documented formula
    achieves that for a given galaxy.
    """
    k_core = kappa_from_galaxy_properties(0.1, galaxy, t_reset, kappa_min, q_sat)
    k_out = kappa_from_galaxy_properties(r_max, galaxy, t_reset, kappa_min, q_sat)
    delta = k_out - k_core
    return {
        "galaxy": galaxy.name,
        "r_SFR_over_r_d": galaxy.r_SFR / galaxy.r_d if galaxy.r_d > 0 else float("inf"),
        "kappa_core": k_core,
        "kappa_outskirts": k_out,
        "delta_kappa": delta,
        "increases_with_radius": delta > 0.0,
        "verdict": (
            f"κ({'increases' if delta > 0 else 'decreases'}) with radius "
            f"(Δκ = {delta:+.3f}). r_SFR/r_d = {galaxy.r_SFR/galaxy.r_d:.2f}. "
            f"{'OK for flat curves.' if delta > 0 else 'WRONG DIRECTION: the reset-by-SFR mechanism is inconsistent with the observed inside-out growth (r_SFR > r_d).'}"
        ),
    }


def delta_kappa_from_galaxy(
    galaxy: GalaxyObservables,
    r_max: float = 30.0,
    t_reset: float = 0.01,
    kappa_min: float = 1e-6,
    q_sat: float = 1.0,
) -> float:
    """Derived Δκ = κ_outskirts − κ_core from galaxy observables (F6)."""
    return radial_gradient_check(galaxy, r_max, t_reset, kappa_min, q_sat)["delta_kappa"]


def predict_kappa_profile(
    galaxy: GalaxyObservables,
    t_reset: float = 0.01,
    kappa_min: float = 1e-6,
    q_sat: float = 1.0,
    alpha: float = 20.0,
    kappa_eq: float = 0.5,
    kappa_earth: float = 1.0,
    n_points: int = 50,
    r_max: float = 30.0,
) -> dict:
    """Predict κ(r) for a galaxy from its observables (F6 formula).

    Returns κ(r) and the LINEAR two-source enhancement 1 + α·χ.
    """
    radii = [r_max * i / (n_points - 1) for i in range(n_points)]
    radii[0] = 0.1

    kappa_vals = []
    enhancement = []

    for r in radii:
        k = kappa_from_galaxy_properties(r, galaxy, t_reset, kappa_min, q_sat)
        kappa_vals.append(k)
        chi = (k - kappa_eq) / kappa_earth
        enhancement.append(1.0 + alpha * chi)

    return {
        "galaxy": galaxy.name,
        "radii_kpc": radii,
        "kappa_r": kappa_vals,
        "enhancement": enhancement,
        "kappa_core": kappa_vals[0],
        "kappa_outskirts": kappa_vals[-1],
        "delta_kappa": kappa_vals[-1] - kappa_vals[0],
        "enhancement_core": enhancement[0],
        "enhancement_outskirts": enhancement[-1],
    }


# ═══════════════════════════════════════════════════════════════════════════
# Test on Known Galaxies
# ═══════════════════════════════════════════════════════════════════════════


# Known galaxy parameters with SFR data (from literature).
# SFR in M_sun/yr, r_SFR typically 1.5-2.5× r_d (inside-out growth).
KNOWN_GALAXIES = [
    GalaxyObservables("NGC 2403", 3.2, 1.4, 2.5, 3.0, SFR=1.2, r_SFR=2.5, age=10.0, V_flat=131),
    GalaxyObservables("NGC 3198", 10.9, 3.1, 5.0, 6.0, SFR=2.0, r_SFR=5.0, age=10.0, V_flat=150),
    GalaxyObservables("NGC 2841", 9.8, 3.6, 8.5, 8.0, SFR=0.5, r_SFR=6.0, age=11.0, V_flat=285),
    GalaxyObservables("NGC 7331", 11.1, 5.0, 9.0, 7.0, SFR=3.0, r_SFR=8.0, age=10.0, V_flat=239),
    GalaxyObservables("NGC 5055", 11.7, 3.2, 8.0, 8.0, SFR=2.5, r_SFR=5.5, age=10.0, V_flat=179),
    GalaxyObservables("DDO 154", 0.28, 0.37, 0.25, 1.0, SFR=0.005, r_SFR=1.0, age=12.0, V_flat=47),
    GalaxyObservables("NGC 6503", 1.7, 2.2, 0.8, 2.5, SFR=0.4, r_SFR=3.5, age=10.0, V_flat=116),
    GalaxyObservables("NGC 2903", 2.6, 2.3, 2.5, 3.0, SFR=1.5, r_SFR=4.0, age=10.0, V_flat=185),
]


def analyze_kappa_predictions(
    t_reset: float = 0.01,
    kappa_min: float = 1e-6,
    q_sat: float = 1.0,
) -> dict:
    """Analyze κ(r) predictions (F6) for all known galaxies, incl. the sign."""
    results = []
    n_increasing = 0
    for galaxy in KNOWN_GALAXIES:
        pred = predict_kappa_profile(galaxy, t_reset, kappa_min, q_sat)
        check = radial_gradient_check(galaxy, t_reset=t_reset, kappa_min=kappa_min, q_sat=q_sat)
        if check["increases_with_radius"]:
            n_increasing += 1
        results.append({
            "galaxy": galaxy.name,
            "r_SFR_over_r_d": galaxy.r_SFR / galaxy.r_d,
            "delta_kappa": pred["delta_kappa"],
            "increases_with_radius": check["increases_with_radius"],
        })

    return {
        "parameters": {"t_reset": t_reset, "kappa_min": kappa_min, "q_sat": q_sat},
        "n_increasing": n_increasing,
        "n_total": len(KNOWN_GALAXIES),
        "predictions": results,
        "finding": (
            f"Under the documented F6 formula, κ increases with radius in "
            f"{n_increasing}/{len(KNOWN_GALAXIES)} galaxies. For inside-out growth "
            f"(r_SFR > r_d, all of these), the reset-by-SFR mechanism gives the "
            f"wrong radial direction — Δκ is negative, the opposite of what flat "
            f"rotation curves require."
        ),
    }
