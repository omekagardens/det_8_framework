"""
DET Parameter Constraints from Published Data

Uses published experimental results to set upper bounds on
DET free parameters (λ_P, λ_γ, G_q) and identify anomaly
candidates consistent with DET predictions.

Sources:
  - Atomic clock comparisons: NIST/Boulder, Tokyo, PTB
  - Eötvös experiments: MICROSCOPE, Eöt-Wash
  - Lunar laser ranging: Nordtvedt parameter
  - Orbit anomalies: flyby, Pioneer, perihelion precession
  - Material science: processing-history effects on material properties
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# 1. λ_P Constraints from Atomic Clock Comparisons
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class ClockComparison:
    """A published atomic clock frequency comparison."""

    name: str
    clock_type_a: str
    clock_type_b: str
    fractional_uncertainty: float      # Total measurement uncertainty Δy/y
    observed_offset: Optional[float]    # Measured fractional offset (None if zero within uncertainty)
    year: int
    reference: str


# Published clock comparisons (real data).
PUBLISHED_CLOCK_COMPARISONS = [
    ClockComparison(
        name="NIST Yb vs Sr (2021)",
        clock_type_a="¹⁷¹Yb optical lattice",
        clock_type_b="⁸⁷Sr optical lattice",
        fractional_uncertainty=2.0e-18,
        observed_offset=None,  # Consistent with zero within uncertainty.
        year=2021,
        reference="Boulder Atomic Clock Network, Nature 2021",
    ),
    ClockComparison(
        name="NIST Al+ vs Yb (2020)",
        clock_type_a="²⁷Al+ quantum logic",
        clock_type_b="¹⁷¹Yb optical lattice",
        fractional_uncertainty=8.0e-18,
        observed_offset=None,
        year=2020,
        reference="NIST Al+/Yb comparison, PRL 2020",
    ),
    ClockComparison(
        name="Tokyo Sr vs Sr (2020)",
        clock_type_a="⁸⁷Sr optical lattice (cryogenic)",
        clock_type_b="⁸⁷Sr optical lattice (room temp)",
        fractional_uncertainty=5.0e-18,
        observed_offset=None,
        year=2020,
        reference="Tokyo Sr clock comparison, Nature Photonics 2020",
    ),
    ClockComparison(
        name="PTB Yb+ vs Sr (2022)",
        clock_type_a="¹⁷¹Yb+ single ion",
        clock_type_b="⁸⁷Sr optical lattice",
        fractional_uncertainty=4.0e-18,
        observed_offset=None,
        year=2022,
        reference="PTB Yb+/Sr comparison, PRL 2022",
    ),
]


def constrain_lambda_p_from_clocks(
    max_kappa_difference: float = 0.5,
) -> dict:
    """Compute upper bounds on λ_P from published clock comparisons.

    If two clocks with κ difference Δκ show no unexplained frequency
    offset at precision σ, then:

      λ_P < σ / Δκ   (for κ_A ≈ 0, Δκ = κ_B)

    This gives an upper bound on λ_P. More constraining for larger Δκ.

    Args:
        max_kappa_difference: Maximum plausible κ difference between clocks.
                              0.5 means one clock is pristine (κ=0) and the
                              other is heavily damaged (κ=0.5).

    Returns:
        Upper bounds on λ_P from each comparison.
    """
    bounds = []
    best_bound = float("inf")
    best_experiment = ""

    for comp in PUBLISHED_CLOCK_COMPARISONS:
        # Upper bound: λ_P < σ / Δκ.
        # The fractional frequency offset from DET is y = λ_P·Δκ / (1+λ_P·κ_A).
        # For κ_A=0: y = λ_P·κ_B → λ_P = y/κ_B.
        # If y < σ (no detection), then λ_P < σ/κ_B.
        bound = comp.fractional_uncertainty / max_kappa_difference

        bounds.append({
            "experiment": comp.name,
            "uncertainty": comp.fractional_uncertainty,
            "lambda_p_upper_bound": bound,
            "interpretation": f"λ_P < {bound:.1e} (if Δκ={max_kappa_difference} between clocks)",
        })

        if bound < best_bound:
            best_bound = bound
            best_experiment = comp.name

    return {
        "method": "Atomic clock comparison — null result at precision σ",
        "assumption": f"Maximum κ difference between clocks: Δκ = {max_kappa_difference}",
        "formula": "λ_P < σ / Δκ  (for κ_A=0, signal y = λ_P·κ_B < σ → λ_P < σ/κ_B)",
        "best_bound": best_bound,
        "best_experiment": best_experiment,
        "all_bounds": bounds,
        "implication": (
            f"The best current constraint is λ_P < {best_bound:.1e} "
            f"from {best_experiment}, assuming Δκ={max_kappa_difference}. "
            "If the actual κ difference between clocks is smaller, "
            "the bound weakens proportionally."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. Eötvös Parameter Constraints on λ_γ
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class EotvosExperiment:
    """A published equivalence principle test."""

    name: str
    material_a: str
    material_b: str
    eta_upper_bound: float  # Eötvös parameter η = 2|a_A - a_B|/|a_A + a_B|
    year: int
    reference: str


PUBLISHED_EOTVOS = [
    EotvosExperiment(
        name="MICROSCOPE (2022)",
        material_a="Titanium",
        material_b="Platinum",
        eta_upper_bound=1.5e-15,
        year=2022,
        reference="MICROSCOPE final results, PRL 2022",
    ),
    EotvosExperiment(
        name="Eöt-Wash (2008)",
        material_a="Beryllium",
        material_b="Titanium",
        eta_upper_bound=1.8e-13,
        year=2008,
        reference="Eöt-Wash Be/Ti, PRL 2008",
    ),
    EotvosExperiment(
        name="Lunar Laser Ranging",
        material_a="Earth (silicate/iron)",
        material_b="Moon (silicate)",
        eta_upper_bound=1.0e-13,  # Nordtvedt parameter constraint.
        year=2020,
        reference="Lunar laser ranging, Classical and Quantum Gravity 2020",
    ),
]


def constrain_lambda_gamma_from_eotvos() -> dict:
    """Constrain λ_γ from equivalence principle tests.

    If two materials have different κ values (different structural
    histories per unit mass), then in DET gravity:

      a_DET = G_q · λ_γ² · κ² / r²
      (gravitational acceleration per unit test mass with κ_test).

    The Eötvös parameter for two materials A, B:
      η = 2|a_A - a_B| / |a_A + a_B|.

    If the DET gravitational charge depends on κ, and κ differs
    between materials A and B, then:

      η_DET ≈ |κ_A² - κ_B²| / (κ_A² + κ_B²).

    The experimental bound η < η_max constrains:

      |κ_A² - κ_B²| / (κ_A² + κ_B²) < η_max.

    This constrains the κ difference between materials, which
    translates to a constraint on λ_γ if we can relate κ to
    known material properties.
    """
    # If κ ∝ (something like atomic number, density, or known material property),
    # we can estimate Δκ between materials.

    # For a rough estimate: assume κ scales with some material property.
    # Titanium (Z=22), Platinum (Z=78): very different atomic structure.
    # If κ ∝ Z (atomic number), then κ_Ti/κ_Pt ≈ 22/78 ≈ 0.28.

    materials = {
        "Titanium": {"Z": 22, "density_gcm3": 4.5},
        "Platinum": {"Z": 78, "density_gcm3": 21.5},
        "Beryllium": {"Z": 4, "density_gcm3": 1.85},
        "Earth": {"Z_avg": 14, "density_gcm3": 5.5},
        "Moon": {"Z_avg": 10, "density_gcm3": 3.3},
    }

    results = []
    for exp in PUBLISHED_EOTVOS:
        # Estimate κ ratio from atomic number (one possible model).
        za = materials.get(exp.material_a, {}).get("Z", 20)
        zb = materials.get(exp.material_b, {}).get("Z", 20)

        # Model: κ ∝ Z (atomic number) as a proxy for structural complexity.
        # This is speculative — the actual κ(Z) relation is unknown.
        kappa_ratio = za / zb if zb > 0 else 1.0

        # Eötvös parameter from DET with κ ∝ Z:
        eta_det_predicted = abs(za**2 - zb**2) / (za**2 + zb**2)

        results.append({
            "experiment": exp.name,
            "materials": f"{exp.material_a} vs {exp.material_b}",
            "eta_experimental_bound": exp.eta_upper_bound,
            "eta_det_predicted (κ∝Z)": eta_det_predicted,
            "constrains_det": eta_det_predicted > exp.eta_upper_bound,
            "implication": (
                f"If κ ∝ Z, DET predicts η ≈ {eta_det_predicted:.2e}, "
                f"which is {'EXCLUDED by' if eta_det_predicted > exp.eta_upper_bound else 'consistent with'} "
                f"the experimental bound η < {exp.eta_upper_bound:.1e}."
            ),
        })

    return {
        "model": "κ ∝ Z (atomic number — speculative proxy for structural complexity)",
        "warning": (
            "The κ(Z) relationship is UNKNOWN. These bounds assume κ ∝ Z. "
            "If κ is independent of Z (or proportional to a different material "
            "property), the constraints change. This analysis demonstrates the "
            "METHOD, not a definitive bound."
        ),
        "results": results,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 3. Orbital/Gravity Anomaly Analysis
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class GravityAnomaly:
    """A known gravitational anomaly that could be a κ-gravity signature."""

    name: str
    observed_effect: str
    magnitude: float  # Fractional deviation from Newton/GR.
    standard_explanation: str
    det_explanation_candidate: str


KNOWN_ANOMALIES = [
    GravityAnomaly(
        name="Pioneer anomaly",
        observed_effect="Unexplained sunward acceleration ~8.7×10⁻¹⁰ m/s²",
        magnitude=8.7e-10 / 9.8,  # Fractional relative to g.
        standard_explanation="Thermal recoil force (resolved, 2012)",
        det_explanation_candidate=(
            "Could be κ-gravity if spacecraft κ changed during mission. "
            "But anomaly was fully explained by thermal effects — no residual."
        ),
    ),
    GravityAnomaly(
        name="Flyby anomaly",
        observed_effect="Velocity change ~few mm/s during Earth flybys",
        magnitude=1e-6,  # Fractional velocity change.
        standard_explanation="Unresolved; possibly unmodeled Earth gravity harmonics",
        det_explanation_candidate=(
            "If spacecraft κ differs from Earth κ, the gravitational interaction "
            "could produce anomalous acceleration during close approach. "
            "Requires modeling κ-dependent gravity during flyby."
        ),
    ),
    GravityAnomaly(
        name="Galaxy rotation curves",
        observed_effect="Flat rotation curves requiring dark matter or MOND",
        magnitude=1.0,  # Factor of ~2-5 discrepancy.
        standard_explanation="Dark matter halos (ΛCDM)",
        det_explanation_candidate=(
            "If κ varies with galactic radius (structural history accumulates "
            "differently in dense vs sparse regions), the effective gravitational "
            "coupling λ_γ·κ could produce MOND-like effects without dark matter. "
            "Requires modeling κ(r) from galactic formation history."
        ),
    ),
    GravityAnomaly(
        name="Mercury perihelion precession",
        observed_effect="43 arcsec/century excess over Newtonian",
        magnitude=43.0 * math.pi / (180 * 3600 * 100),  # Fractional relative to orbit.
        standard_explanation="GR prediction matches exactly (Einstein, 1915)",
        det_explanation_candidate=(
            "DET must reproduce the GR prediction. The Newtonian limit of DET "
            "gravity matches GR in the weak-field, low-velocity regime. The "
            "perihelion precession would be a test of the post-Newtonian DET "
            "corrections, not yet computed."
        ),
    ),
]


def analyze_gravity_anomalies() -> dict:
    """Analyze known gravitational anomalies for DET signatures.

    For each anomaly, assess whether DET provides a natural
    explanation and what parameters would be required.
    """
    return {
        "anomalies": [
            {
                "name": a.name,
                "standard_status": a.standard_explanation,
                "det_potential": a.det_explanation_candidate,
                "testable": "flyby" in a.name.lower(),
            }
            for a in KNOWN_ANOMALIES
        ],
        "most_promising": (
            "Galaxy rotation curves: if κ(r) varies with radius due to "
            "differential structural history accumulation, DET could produce "
            "MOND-like effects from the κ-field. This is speculative but "
            "testable by modeling κ(r) from galactic formation history and "
            "comparing to observed rotation curves."
        ),
        "requires_newtonian_match": (
            "GR-precision phenomena (Mercury, binary pulsars, gravitational "
            "waves) require DET to match GR in the post-Newtonian regime. "
            "This is not yet computed and is a research frontier."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 4. Material Science κ-Calibration
# ═══════════════════════════════════════════════════════════════════════════


def material_science_kappa_calibration() -> dict:
    """Use published material science data to estimate κ for common materials.

    κ represents structural history density. In materials science:
      - Annealed (fully recovered) materials: κ ≈ 0.
      - Cold-worked (heavily deformed) materials: κ ≈ 0.3–0.5.
      - Irradiated (neutron-damaged) materials: κ ≈ 0.5–0.9.

    Known effects that could be κ-proxies:
      - Dislocation density ρ_d: increases with cold work.
      - Residual stress: increases with inhomogeneous deformation.
      - Grain boundary area: increases with grain refinement.
      - Point defect concentration: increases with irradiation.

    If κ correlates with any of these, the structural proxy can be
    calibrated against known material state variables.
    """
    return {
        "candidate_kappa_proxies": [
            {
                "variable": "Dislocation density ρ_d",
                "range": "10⁶ cm⁻² (annealed) to 10¹² cm⁻² (heavily deformed)",
                "kappa_correlation": "Higher ρ_d → more structural history → higher κ",
                "testable": "Measure ρ_d via TEM/XRD, correlate with proxy response",
            },
            {
                "variable": "Residual stress σ_res",
                "range": "0 (annealed) to ~yield strength (cold-worked)",
                "kappa_correlation": "Higher σ_res → more stored elastic energy → higher κ",
                "testable": "Measure σ_res via XRD/hole-drilling, correlate with proxy",
            },
            {
                "variable": "Hardness / yield strength",
                "range": "Annealed → work-hardened (2-5× increase)",
                "kappa_correlation": "Higher hardness → more structural constraints → higher κ",
                "testable": "Standard hardness tests vs proxy response",
            },
            {
                "variable": "Electrical resistivity",
                "range": "Increases with defect density (Matthiessen's rule)",
                "kappa_correlation": "Higher resistivity → more scattering centers → higher κ",
                "testable": "Four-point probe resistivity vs proxy response",
            },
        ],
        "calibration_strategy": (
            "1. Prepare samples with known processing history (annealed, cold-worked, irradiated). "
            "2. Measure all candidate standard variables (ρ_d, σ_res, hardness, resistivity). "
            "3. Measure structural proxy response R. "
            "4. Fit R = R_standard(standard_vars) + R_residual. "
            "5. If R_residual correlates with processing history beyond standard variables, "
            "   it is a κ candidate."
        ),
        "published_data_potential": (
            "Extensive literature exists on dislocation density, residual stress, "
            "and mechanical properties vs processing history for common alloys "
            "(steel, aluminum, copper, titanium). This data can be re-analyzed "
            "to search for κ-residuals beyond standard material models."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 5. Combined Constraint Summary
# ═══════════════════════════════════════════════════════════════════════════


def combined_parameter_constraints() -> dict:
    """Combine all experimental constraints on DET parameters."""

    clock = constrain_lambda_p_from_clocks(max_kappa_difference=0.5)
    eotvos = constrain_lambda_gamma_from_eotvos()

    return {
        "lambda_P": {
            "best_upper_bound": clock["best_bound"],
            "source": clock["best_experiment"],
            "method": clock["method"],
            "assumptions": clock["assumption"],
            "if_kappa_difference_is_0_01": (
                f"λ_P < {clock['best_bound'] * 50:.1e} (bound weakens ∝ 1/Δκ)"
            ),
        },
        "lambda_gamma": {
            "constraint_type": "Eötvös parameter — constrains Δκ between materials",
            "best_bound": "Model-dependent (κ(Z) unknown)",
            "if_kappa_equals_Z": eotvos["results"],
            "note": "λ_γ not directly constrained without κ calibration",
        },
        "G_q": {
            "constraint_type": "Degenerate with λ_γ — broken only by independent κ measurement",
            "calibration": "G_q·λ_γ²·κ² = G·M² for laboratory masses",
        },
        "next_steps": [
            "Calibrate κ against known material state variables (dislocation density, etc.)",
            "Re-analyze published clock data with explicit κ estimates",
            "Model galaxy rotation curves with κ(r) from formation history",
            "Compute DET post-Newtonian corrections for solar system tests",
        ],
    }
