"""
DET v8.0 — SI ↔ DET Units Conversion

Maps measurable (SI) quantities onto DET's free parameters, so that existing
lab data can be fit. NO smuggling: this is dimensional bookkeeping and
conversion. The SI quantities (frequency shifts, force differences, material
response ratios) are OBSERVED inputs; the DET parameters (κ, χ, λ_P, α) are
the model's own dimensionless couplings. Nothing here derives SI physics from
DET primitives.

Core statement (two-source law): every DET parameter is DIMENSIONLESS.
The only dimensional anchors are the empirical constants G (and c). The
"conversion" therefore maps dimensionless SI-measured RATIOS onto the
dimensionless DET parameters:

  Clock:    Δν/ν = λ_P·κ / (1 + λ_P·κ)              [κ-Π clock anomaly]
  Gravity:  ΔG/G = α·χ(κ),   χ = (κ − κ_eq)/κ_earth  [two-source law, gravity_v2]
  Proxy:    R/R_0 = (1 − κ)^p                        [structural proxy response]

The clock anomaly is a RATIO (anchor-free); absolute proper time would need a
"seconds per event" calibration that the ratio predictions do not require.

Degeneracy note: α and κ_earth enter gravity only through the single
combination β_eff = α/κ_earth (since χ = (κ−κ_eq)/κ_earth). α and κ_earth are
therefore NOT independently observable from gravity alone.
"""

from __future__ import annotations

import math

from det8.models.gravity_v2 import G_NEWTON, response_field


# ── Dimensional analysis ────────────────────────────────────────────────────


def dimensional_analysis() -> dict:
    """SI dimensions of every DET quantity.

    Dimensions as (kg, m, s) exponent triples; "1" = dimensionless.
    """
    return {
        "kappa": (0, 0, 0),
        "chi": (0, 0, 0),
        "lambda_P": (0, 0, 0),
        "alpha": (0, 0, 0),
        "Pi": (0, 0, 0),          # proper time in event units (anchor-free ratio).
        "G": (-1, 3, -2),
        "G_eff": (-1, 3, -2),
        "rho_m": (1, -3, 0),
        "rho_kappa": (1, -3, 0),
        "m": (1, 0, 0),
        "R": (0, 1, 0),
        "a_disp": (0, 1, -2),
        "statement": (
            "Every DET coupling (κ, χ, λ_P, α, Π) is dimensionless. The only "
            "dimensional anchors are the empirical G and c. All DET predictions "
            "are therefore dimensionless ratios; SI units enter only through "
            "the observed inputs."
        ),
    }


def natural_units() -> dict:
    """The DET-native reference scales (all dimensionless + empirical anchors)."""
    return {
        "reference_participation": "Π = 1 at κ=0, σ=η=1, F=H=0, v=0",
        "kappa_range": "[0, 1]",
        "chi": "(κ − κ_eq)/κ_earth",
        "beta_eff": "α/κ_earth — the single observable gravity combination",
        "dimensional_anchors": {
            "G": f"{G_NEWTON:.5e} m³·kg⁻¹·s⁻² (empirical)",
            "c": "2.99792458e8 m/s (empirical, borrowed)",
        },
        "note": (
            "The clock anomaly Δν/ν and gravity shift ΔG/G are dimensionless "
            "ratios and are anchor-free. A 'seconds per event' calibration is "
            "needed only for absolute proper-time rates, which no DET "
            "prediction currently requires."
        ),
    }


# ── Conversion: clock channel ───────────────────────────────────────────────


def clock_shift_from_lambda_p(lambda_p: float, kappa: float = 0.5) -> float:
    """Δν/ν = λ_P·κ / (1 + λ_P·κ) — forward (DET → SI observed ratio)."""
    return lambda_p * kappa / (1.0 + lambda_p * kappa)


def lambda_p_from_clock_shift(frac_shift: float, kappa: float = 0.5) -> float:
    """λ_P = Δ / (κ·(1 − Δ)) — inverse (SI observed ratio → DET coupling)."""
    if not (0.0 <= frac_shift < 1.0):
        raise ValueError("frac_shift must be in [0, 1)")
    if kappa <= 0.0:
        raise ValueError("kappa must be > 0")
    return frac_shift / (kappa * (1.0 - frac_shift))


# ── Conversion: gravity channel ─────────────────────────────────────────────


def gravity_shift_from_alpha(alpha: float, chi: float) -> float:
    """ΔG/G = α·χ — forward (DET → SI observed ratio)."""
    return alpha * chi


def alpha_from_gravity_shift(frac_g: float, chi: float) -> float:
    """α = (ΔG/G) / χ — inverse (SI observed ratio → DET coupling)."""
    if chi == 0.0:
        raise ValueError("chi must be nonzero to infer alpha")
    return frac_g / chi


# ── Conversion: proxy channel ───────────────────────────────────────────────


def proxy_response_from_kappa(kappa: float, p: float = 1.0, r0: float = 1.0) -> float:
    """R/R_0 = (1 − κ)^p — forward (DET → SI observed response ratio)."""
    return r0 * (1.0 - kappa) ** p


def kappa_from_proxy_response(r_ratio: float, p: float = 1.0) -> float:
    """κ = 1 − (R/R_0)^(1/p) — inverse (SI response ratio → DET κ)."""
    if not (0.0 <= r_ratio <= 1.0):
        raise ValueError("r_ratio must be in [0, 1]")
    if p <= 0.0:
        raise ValueError("p must be > 0")
    return 1.0 - r_ratio ** (1.0 / p)


# ── The coupling implications (α ≈ 5) ───────────────────────────────────────


def coupling_implications(
    alpha: float = 20.0,
    kappa_earth: float = 1.0,
    kappa_eq: float = 0.5,
    eotvos_eta: float = 1e-13,          # equivalence-principle bound (Δa/a).
    galactic_range: tuple[float, float] = (2.0, 50.0),  # mass discrepancy.
) -> dict:
    """What α implies, given lab and galactic constraints.

    (α ≈ 20 is the honest value from SPARC with κ clamped to [0,1].)

    The observable combination is β_eff = α/κ_earth (α and κ_earth are
    degenerate). It is constrained from BOTH ends:

      Lab (Eötvös):  Δa/a = β_eff·Δκ < η  ⇒  Δκ < η/β_eff   (lab materials
                     must have nearly equal κ).
      Galactic:      G_eff/G = 1 + β_eff·Δκ_galactic  must reach the observed
                     mass discrepancy (2–50); with κ ∈ [0,1], Δκ_galactic ≤
                     1 − κ_eq.

    The tension: a large β_eff (to reach dwarf discrepancies) shrinks the
    allowed lab Δκ, and the [0,1] bound on κ caps the reachable enhancement.
    """
    if kappa_earth <= 0.0:
        raise ValueError("kappa_earth must be > 0")

    beta_eff = alpha / kappa_earth

    # Lab constraint: Δκ_lab < η / β_eff.
    delta_kappa_lab_max = eotvos_eta / beta_eff

    # Galactic requirement: Δκ_galactic ∈ [(min−1)/β_eff, (max−1)/β_eff].
    delta_kappa_galactic_min = (galactic_range[0] - 1.0) / beta_eff
    delta_kappa_galactic_max = (galactic_range[1] - 1.0) / beta_eff

    # κ ∈ [0,1] bounds the reachable Δκ_galactic.
    kappa_range_capacity = 1.0 - kappa_eq
    reachable_enhancement = 1.0 + beta_eff * kappa_range_capacity

    # Maximum discrepancy reachable within κ ∈ [0,1].
    dwarf_reachable = reachable_enhancement >= galactic_range[1]

    return {
        "alpha": alpha,
        "kappa_earth": kappa_earth,
        "kappa_eq": kappa_eq,
        "beta_eff": beta_eff,
        "lab": {
            "eotvos_eta": eotvos_eta,
            "delta_kappa_lab_max": delta_kappa_lab_max,
            "implication": (
                f"α = {alpha} forces lab materials to have κ equal to within "
                f"{delta_kappa_lab_max:.2e} (absolute κ units), or the "
                f"equivalence principle is violated at η = {eotvos_eta:.0e}."
            ),
        },
        "galactic": {
            "delta_kappa_needed_range": (delta_kappa_galactic_min, delta_kappa_galactic_max),
            "kappa_range_capacity": kappa_range_capacity,
            "reachable_enhancement": reachable_enhancement,
            "dwarf_reachable": dwarf_reachable,
            "implication": (
                f"β_eff = {beta_eff:.1f} gives G_eff/G = {reachable_enhancement:.1f} at "
                f"most (κ ∈ [0,1]); the observed discrepancy range "
                f"{galactic_range} needs Δκ ∈ "
                f"[{delta_kappa_galactic_min:.1f}, {delta_kappa_galactic_max:.1f}]. "
                f"Dwarf-scale discrepancy ({galactic_range[1]}×) is "
                f"{'reachable' if dwarf_reachable else 'NOT reachable'} with this β_eff."
            ),
        },
        "degeneracy": (
            f"α and κ_earth enter only through β_eff = α/κ_earth = {beta_eff:.1f}. "
            f"Gravity alone cannot separate α from κ_earth; a proxy measurement "
            f"of κ (or a clock λ_P·κ bound) is needed to break the degeneracy."
        ),
    }


# ── Worked lab-fitting example ──────────────────────────────────────────────


def fit_lab_example(
    clock_precision: float = 1e-18,   # best optical-lattice clocks.
    eotvos_eta: float = 1e-13,        # Eöt-Wash (conservative); MICROSCOPE ~1e-15.
    alpha: float = 20.0,
    kappa_earth: float = 1.0,
    kappa_eq: float = 0.5,
) -> dict:
    """Fit representative existing lab data onto DET parameters.

    Inputs are observed SI precision/bounds (NOT smuggled physics): the
    clock comparison precision and the equivalence-principle bound.
    """
    # Clock: a null result at `clock_precision` bounds λ_P·κ < σ.
    lambda_p_kappa_bound = clock_precision  # λ_P·κ < σ (product only).

    impl = coupling_implications(
        alpha=alpha, kappa_earth=kappa_earth, kappa_eq=kappa_eq,
        eotvos_eta=eotvos_eta,
    )

    return {
        "inputs": {
            "clock_precision": clock_precision,
            "eotvos_eta": eotvos_eta,
            "alpha": alpha,
            "kappa_earth": kappa_earth,
        },
        "inferred": {
            "lambda_p_kappa_upper_bound": lambda_p_kappa_bound,
            "delta_kappa_lab_max": impl["lab"]["delta_kappa_lab_max"],
        },
        "interpretation": (
            f"Null clock result at {clock_precision:.0e} bounds the PRODUCT "
            f"λ_P·κ < {lambda_p_kappa_bound:.0e} (λ_P is unconstrained until κ "
            f"is independently measured). Eötvös at η={eotvos_eta:.0e} bounds "
            f"Δκ_lab < {impl['lab']['delta_kappa_lab_max']:.2e} for α={alpha}. "
            f"Together these are the model-independent statements; both need a "
            f"structural-proxy κ measurement to become constraints on the "
            f"individual couplings."
        ),
    }
