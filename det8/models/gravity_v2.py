"""
DET v8.0 — Gravity v2: Two-Source Field Equation (κ-modified, mass-conserving)

Resolves the Round 3 red-team finding F2 by retiring the mass-independent
"κ replaces mass" law (`det_gravity.py` / `gravity_experiment.py` /
`PHYSICS.md` §2.2 v1) and adopting the two-source form:

    ∇²Φ = 4π G (ρ_m + ρ_κ)

Three-quantity split (per Team A decision, August 2026):

  1. κ      : structural history — dimensionless, record-side, in [0, 1].
  2. χ(κ)   : gravitational response field — dimensionless,
              χ(κ) = (κ − κ_eq) / κ_earth.
  3. ρ_κ    : DET structural source density — kg/m³,  ρ_κ = ρ_m · χ(κ).

Consequences:

  - Effective coupling:  G_eff = G (1 + α·χ(κ))   — LINEAR in κ.
  - Point-source force:  F = G_eff · m₁m₂ / r²    — scales ∝ m₁m₂, so the
    equivalence principle is preserved exactly.
  - κ is a history-dependent MODIFIER of the gravitational response, not
    the replacement source, and not a hidden mass variable. κ stays
    dimensionless in [0, 1].

Decoupling prediction (v2): recovering κ (κ → κ_eq ⇒ χ → 0) removes only
the anomalous component F_κ = G·α·χ·m₁m₂/r², leaving standard Newtonian
F_N = G·m₁m₂/r².  The experimental signature is ΔF = F_κ ≠ 0, NOT F → 0.

Status: P (proposed physical) — a correspondence to Newtonian gravity with
a κ-response term. G is Newton's constant (empirical input, already used by
`post_newtonian.py` and `sparc_analysis.py`); nothing here claims to derive
G from DET primitives.
"""

from __future__ import annotations

import math


# ── Empirical / free parameters ─────────────────────────────────────────────

G_NEWTON = 6.67430e-11        # Newton's constant (SI: m³·kg⁻¹·s⁻²).
KAPPA_EQ_DEFAULT = 0.0        # Equilibrium κ (fully recovered).
KAPPA_EARTH_DEFAULT = 1.0     # Reference normalization (Earth κ).
ALPHA_DEFAULT = 1.0           # Dimensionless coupling of the κ-response term.


# ── Three-quantity split ────────────────────────────────────────────────────


def response_field(
    kappa: float,
    kappa_eq: float = KAPPA_EQ_DEFAULT,
    kappa_earth: float = KAPPA_EARTH_DEFAULT,
) -> float:
    """Dimensionless gravitational response field χ(κ) = (κ − κ_eq)/κ_earth."""
    if kappa_earth <= 0.0:
        raise ValueError("kappa_earth must be > 0")
    return (kappa - kappa_eq) / kappa_earth


def effective_G(
    kappa: float,
    kappa_eq: float = KAPPA_EQ_DEFAULT,
    kappa_earth: float = KAPPA_EARTH_DEFAULT,
    alpha: float = ALPHA_DEFAULT,
) -> float:
    """Effective coupling G_eff = G·(1 + α·χ(κ)). Linear in κ."""
    return G_NEWTON * (1.0 + alpha * response_field(kappa, kappa_eq, kappa_earth))


def source_density_kappa(
    rho_m: float,
    chi: float,
) -> float:
    """DET structural source density ρ_κ = ρ_m·χ (kg/m³)."""
    return rho_m * chi


# ── Point-source force (equivalence principle preserved) ───────────────────


def point_source_force(
    m1: float,
    m2: float,
    r: float,
    kappa: float,
    kappa_eq: float = KAPPA_EQ_DEFAULT,
    kappa_earth: float = KAPPA_EARTH_DEFAULT,
    alpha: float = ALPHA_DEFAULT,
) -> float:
    """F = G_eff·m₁m₂/r². Scales ∝ m₁m₂ (equivalence principle)."""
    if r <= 0.0:
        raise ValueError("separation r must be > 0")
    return effective_G(kappa, kappa_eq, kappa_earth, alpha) * m1 * m2 / (r * r)


def anomalous_force_component(
    m1: float,
    m2: float,
    r: float,
    kappa: float,
    kappa_eq: float = KAPPA_EQ_DEFAULT,
    kappa_earth: float = KAPPA_EARTH_DEFAULT,
    alpha: float = ALPHA_DEFAULT,
) -> float:
    """F_κ = G·α·χ·m₁m₂/r² — the removable κ-dependent component."""
    if r <= 0.0:
        raise ValueError("separation r must be > 0")
    chi = response_field(kappa, kappa_eq, kappa_earth)
    return G_NEWTON * alpha * chi * m1 * m2 / (r * r)


# ── Dimensional consistency ─────────────────────────────────────────────────


def dimensional_consistency() -> dict:
    """Verify ∇²Φ = 4πG(ρ_m + ρ_κ) is dimensionally consistent.

    Dimensions are encoded as (kg, m, s) exponent triples.
    """
    dim_grad2_phi = (0, 0, -2)    # Φ [m²/s²], ∇² → divide by m².
    dim_G = (-1, 3, -2)           # G [m³·kg⁻¹·s⁻²].
    dim_rho = (1, -3, 0)          # ρ [kg·m⁻³].
    dim_4piG_rho = tuple(a + b for a, b in zip(dim_G, dim_rho))  # (0, 0, -2)

    return {
        "dim_grad2_phi": dim_grad2_phi,
        "dim_4piG_rho": dim_4piG_rho,
        "consistent": dim_grad2_phi == dim_4piG_rho,
        "note": (
            "∇²Φ has units s⁻²; 4πG·ρ has units s⁻². ρ_κ = ρ_m·χ keeps the "
            "units of mass density, so the κ term needs no new dimension."
        ),
    }


# ── Decoupling prediction (v2) ──────────────────────────────────────────────


def decoupling_prediction_v2(
    m1: float = 1.0,
    m2: float = 1.0,
    r: float = 0.1,
    kappa: float = 0.5,
    kappa_eq: float = KAPPA_EQ_DEFAULT,
    kappa_earth: float = KAPPA_EARTH_DEFAULT,
    alpha: float = ALPHA_DEFAULT,
) -> dict:
    """Rewritten gravity-decoupling prediction.

    Before recovery:  F = F_N + F_κ  (Newtonian + anomalous κ-component).
    After recovery:   κ → κ_eq ⇒ χ → 0 ⇒ F_κ → 0, leaving F = F_N.
    Signature:        ΔF = F_κ ≠ 0  (NOT F → 0).
    """
    if r <= 0.0:
        raise ValueError("separation r must be > 0")

    chi = response_field(kappa, kappa_eq, kappa_earth)
    F_N = G_NEWTON * m1 * m2 / (r * r)
    F_kappa = anomalous_force_component(m1, m2, r, kappa, kappa_eq, kappa_earth, alpha)
    F_before = F_N + F_kappa
    F_after = F_N  # κ recovered.

    return {
        "kappa": kappa,
        "kappa_eq": kappa_eq,
        "chi": chi,
        "alpha": alpha,
        "F_N": F_N,
        "F_kappa": F_kappa,
        "F_before": F_before,
        "F_after": F_after,
        "delta_F": F_kappa,
        "fractional_change": F_kappa / F_N if F_N > 0 else float("inf"),
        "signature": (
            f"Recovering κ removes only the anomalous component: "
            f"ΔF = F_κ = {F_kappa:.3e} N (fraction {F_kappa/F_N:.3f} of F_N). "
            f"Gravity does NOT go to zero; standard Newtonian F_N = {F_N:.3e} N remains."
        ),
    }


# ── Three-law comparison (historical audit) ─────────────────────────────────


def compare_force_laws(
    kappa1: float = 0.5,
    kappa2: float = 0.5,
    m1: float = 1.0,
    m2: float = 1.0,
    r: float = 1.0,
    kappa_eq: float = KAPPA_EQ_DEFAULT,
    kappa_earth: float = KAPPA_EARTH_DEFAULT,
    alpha: float = ALPHA_DEFAULT,
    G_q: float = 1.0,          # legacy free parameter (law a).
    lambda_gamma: float = 1.0,  # legacy free parameter (law a).
) -> dict:
    """Historical audit of the four gravity laws (F2 resolution).

    (a)  κ-only (DEPRECATED):        F = G_q·λ_γ²·κ₁κ₂/r²     — mass-independent.
    (b)  linear modifier (post_newt): F = G·(κ/κ_earth)·m₁m₂/r² — mass retained.
    (c)  quadratic modifier (SPARC): F = G·(κ/κ_earth)²·m₁m₂/r² — mass retained.
    (v2) two-source (NEW):           F = G(1+α·χ)·m₁m₂/r²      — mass retained.
    """
    if r <= 0.0:
        raise ValueError("separation r must be > 0")

    # (a) κ-only (mass-independent).
    F_a = G_q * lambda_gamma**2 * kappa1 * kappa2 / (r * r)
    # (b) linear.
    F_b = G_NEWTON * (kappa1 / kappa_earth) * m1 * m2 / (r * r)
    # (c) quadratic.
    F_c = G_NEWTON * (kappa1 / kappa_earth) ** 2 * m1 * m2 / (r * r)
    # (v2) two-source.
    F_v2 = point_source_force(m1, m2, r, kappa1, kappa_eq, kappa_earth, alpha)

    # Mass-scaling audit: does F double under m1 → 2·m1 at fixed κ?
    F_a_doubled = G_q * lambda_gamma**2 * kappa1 * kappa2 / (r * r)  # unchanged.
    F_v2_doubled = point_source_force(2.0 * m1, m2, r, kappa1, kappa_eq, kappa_earth, alpha)

    return {
        "kappa": (kappa1, kappa2),
        "masses": (m1, m2),
        "separation": r,
        "forces": {
            "a_kappa_only_deprecated": F_a,
            "b_linear_modifier": F_b,
            "c_quadratic_modifier_sparc": F_c,
            "v2_two_source": F_v2,
        },
        "mass_scaling_audit": {
            "a_scales_with_mass": abs(F_a_doubled - F_a) > 1e-30 * F_a,  # False.
            "v2_scales_with_mass": abs(F_v2_doubled / F_v2 - 2.0) < 1e-12,  # True.
        },
        "interpretation": (
            f"Law (a) gives F={F_a:.3e} regardless of mass (1g vs 1000kg identical) "
            f"— empirically falsified. Laws (b)/(c)/(v2) all retain mass; v2 is the "
            f"two-source law with the anomalous component explicitly separated."
        ),
    }
