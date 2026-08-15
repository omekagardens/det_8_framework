"""
DET v8.1 — Physical Realization of FL-4 / FL-5 (relational creation → materials)

The abstract relational-creation model (relational_creation.py) has two
falsification levers that need a PHYSICAL instantiation before they can be
tested. This module supplies the mapping from the relational symbols to
measurable materials-science observables, and states the discriminators.

THE MAPPING (the heart of the realization):

    σ_ij  active bond      ↔  current bond / interfacial cohesion
                              (measurable: elastic modulus, hardness,
                               ultrasonic attenuation, resistivity)
    A_ij  latent capacity  ↔  RECOVERABLE bond capacity — the cohesion
                              achievable after an ideal recovery protocol
                              (measurable: re-bondable site density from
                               microscopy/calorimetry). THIS is the quantity
                               DET claims is larger than standard theory allows.
    κ_i   damage gap       ↔  (A_ij − σ_ij)/A_ij — the fraction of recoverable
                              capacity currently inactive (the structural proxy's κ).

THE DISCRIMINATORS:

  FL-4 (extent) — the new one. Standard materials science treats damage as
      LARGELY PERMANENT: after damage, the recoverable capacity A drops with σ,
      so recovery SATURATES (σ → σ₁ < σ₀, never back to σ₀). DET's latent-
      capacity reading says A is PRESERVED (damage lowers σ but not A), so
      recovery is FULL (σ → σ₀, κ → 0). The discriminator: after a standard
      damage + ideal recovery cycle, does cohesion return to the PRE-DAMAGE
      value (latent capacity, DET) or saturate below it (permanent damage)?
      This is the EXTENT complement to F9's RATE discriminator (τ_rec
      T-independent vs Arrhenius), which already lives in kappa_discriminator.py.

  FL-5 (conservation) — externalization relocates damage, does not annihilate
      it. Total damage D = Σ(A−σ) is conserved across a boundary. Honest note:
      for ordinary defect density this is close to a conservation tautology
      (defects travel with the material). The DET-specific claim is only that
      the STRUCTURAL HISTORY κ is conserved too, which is testable only once
      the structural proxy is calibrated — so FL-5 is downstream of FL-4/F9.

DERIVATION CERTIFICATE (honest provenance):

  σ/A ↔ materials observables       TH-DET — mapping (terminology, not new physics).
  FL-4 extent discriminator          TH-DET — a genuine new test (full vs partial).
  FL-5 conservation                  TH-DET — mostly standard, downstream of F9.
  F9 rate discriminator              (existing) kappa_discriminator.py — MATH/simulated.

  NOT claimed: that latent capacity is ALREADY observed. That is exactly the
  FL-4 experiment. This module specifies the test; it does not report a result.
"""

from __future__ import annotations

import math

from det8.models.kappa_discriminator import (
    annealing_timescale, kappa_recovery_timescale, K_B_EV,
)


# ── The mapping ─────────────────────────────────────────────────────────────


def observable_map() -> dict:
    """σ/A/L/M → measurable materials observables (SI units)."""
    return {
        "sigma_ij": {
            "meaning": "current bond / interfacial cohesion",
            "observable": "elastic modulus E [Pa], hardness H [Pa], ultrasonic attenuation α [Np/m], resistivity ρ [Ω·m]",
            "note": "all are monotone in bond integrity; a composite proxy reduces noise",
        },
        "A_ij": {
            "meaning": "recoverable bond capacity (latent capacity)",
            "observable": "re-bondable site density n_r [m⁻³] (microscopy) + cohesive energy after ideal recovery (calorimetry/mechanical test)",
            "note": "THE DET-specific quantity: claimed LARGER than standard damage theory allows",
        },
        "kappa_i": {
            "meaning": "damage gap (A−σ)/A",
            "observable": "the structural proxy's κ (structural_proxy.py)",
            "note": "0 = fully recovered, 1 = fully latent damage",
        },
        "L_i_M_iG": {
            "meaning": "lineage + regime membership",
            "observable": "material provenance + which functional sub-system a region belongs to (bookkeeping, not a new field)",
            "note": "immutable by construction; not directly measured",
        },
    }


# ── FL-4 extent discriminator (full vs partial recovery) ────────────────────


def fl4_extent_discriminator(
    sigma0: float = 1.0,      # pre-damage cohesion (normalized)
    sigma_damaged: float = 0.3,  # cohesion after damage
    recovery_fraction_standard: float = 0.5,  # standard: only partial recovery
) -> dict:
    """FL-4 EXTENT: does recovery return cohesion to σ₀ (latent) or saturate?

    Standard damage model: damage reduces the recoverable capacity A along
    with σ, so the achievable recovery is A = σ₁ = σ₀·recovery_fraction < σ₀.
    DET latent model: A is preserved (A = σ₀), so recovery is full (σ → σ₀).

    The discriminator is the recovered cohesion after an ideal recovery cycle.
    """
    # Standard (permanent-damage) model: capacity drops with damage.
    A_standard = sigma0 * recovery_fraction_standard
    sigma_recovered_standard = A_standard          # saturation at partial cohesion

    # DET (latent-capacity) model: capacity is preserved.
    A_det = sigma0
    sigma_recovered_det = A_det                     # full recovery to pre-damage

    return {
        "sigma0": sigma0,
        "sigma_damaged": sigma_damaged,
        "recovered_cohesion_standard": sigma_recovered_standard,
        "recovered_cohesion_det": sigma_recovered_det,
        "permanent_damage_fraction_standard": 1.0 - recovery_fraction_standard,
        "permanent_damage_fraction_det": 0.0,
        "distinguishes": abs(sigma_recovered_det - sigma_recovered_standard) > 1e-9,
        "falsifier": (
            "If, after an ideal recovery protocol, cohesion SATURATES below the "
            "pre-damage value (permanent damage fraction > 0), the latent-"
            "capacity reading is false — damage IS permanent, and FL-4 is "
            "falsified. Full recovery to the pre-damage cohesion is the "
            "latent-capacity signature."
        ),
    }


# ── Combined FL-4 (extent) + F9 (rate) experiment ───────────────────────────


def combined_f9_fl4(
    T_low_K: float = 300.0,
    T_high_K: float = 900.0,
    E_a_eV: float = 1.0,
    tau0_s: float = 1e-13,
    tau_rec_s: float = 1e4,
) -> dict:
    """The single experiment that tests BOTH the rate (F9) and extent (FL-4).

    Run damage + recovery at T_low and T_high. Measure:
      - RATE: recovery timescale τ vs temperature (F9: T-independent = κ
        distinct, Arrhenius = defect density).
      - EXTENT: recovered cohesion (FL-4: full = latent capacity, partial =
        permanent damage).
    """
    tau_anneal_low = annealing_timescale(T_low_K, E_a_eV, tau0_s)
    tau_anneal_high = annealing_timescale(T_high_K, E_a_eV, tau0_s)
    tau_rec = kappa_recovery_timescale(tau_rec_s)

    return {
        "rate_discriminator": {
            "tau_anneal_low_s": tau_anneal_low,
            "tau_anneal_high_s": tau_anneal_high,
            "tau_rec_s": tau_rec,
            "annealing_sweep_factor": tau_anneal_low / tau_anneal_high,
            "f9_question": (
                "Does the measured recovery time track the Arrhenius law across "
                "T (defect density) or stay T-independent (κ distinct)?"
            ),
        },
        "extent_discriminator": {
            "fl4_question": (
                "Does cohesion return to the pre-damage value (latent capacity) "
                "or saturate below it (permanent damage)?"
            ),
        },
        "combined_verdict": (
            "F9 tests the RATE of recovery (τ_rec vs τ_anneal); FL-4 tests the "
            "EXTENT (full vs partial). Both are needed: a T-independent τ_rec "
            "with PARTIAL recovery would still leave κ = defect-density-plus-"
            "permanent-damage, not the full latent-capacity story."
        ),
    }


# ── FL-5 conservation discriminator ─────────────────────────────────────────


def fl5_conservation_discriminator() -> dict:
    """FL-5: externalization relocates damage; it does not annihilate it.

    Honest note: for ordinary defect density, conservation under mechanical
    transfer is close to a tautology (defects travel with the material). The
    DET-specific claim is only that the STRUCTURAL HISTORY κ is also conserved,
    which is testable only AFTER the structural proxy is calibrated (FL-4/F9).
    So FL-5 is downstream of FL-4/F9, not an independent near-term test.
    """
    return {
        "claim": "total damage D = Σ(A−σ) is conserved across a regime boundary",
        "standard_part": (
            "ordinary defect density is conserved under transfer — not novel"
        ),
        "det_specific_part": (
            "the STRUCTURAL HISTORY κ (not just defect density) is conserved "
            "— testable via the structural proxy on the discarded material"
        ),
        "downstream_of": "FL-4 (extent) and F9 (rate) — needs a calibrated κ",
        "falsifier": (
            "total κ of a closed system decreases at a boundary with no "
            "compensating transfer to the discarded material (once κ is measurable)"
        ),
    }


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "physical realization of FL-4 / FL-5",
        "deliverables": {
            "σ/A ↔ materials observables": "TH-DET — mapping (terminology, not new physics)",
            "FL-4 extent discriminator (full vs partial)": "TH-DET — a genuine new test",
            "FL-5 conservation": "TH-DET — mostly standard, downstream of FL-4/F9",
            "F9 rate discriminator": "MATH — kappa_discriminator.py (existing)",
        },
        "falsification_levers": {
            "FL-4": "cohesion saturates below pre-damage value after ideal recovery ⟹ falsified",
            "FL-5": "total κ decreases at a boundary with no compensating transfer ⟹ falsified",
        },
        "not_claimed": [
            "that latent capacity is ALREADY observed — FL-4 is the test, not a result",
            "any new material property — σ/A map onto standard observables; only the RECOVERY EXTENT is the novel claim",
        ],
        "status": (
            "FL-4 reduces to a concrete, novel experiment (full-vs-partial "
            "recovery of cohesion), complementing the existing F9 rate test. "
            "FL-5 is downstream (needs a calibrated κ). Registered in "
            "FALSIFICATION_LEDGER.md."
        ),
    }


# ── End-to-end ──────────────────────────────────────────────────────────────


def run_realization() -> dict:
    return {
        "observable_map": observable_map(),
        "fl4_extent": fl4_extent_discriminator(),
        "combined_f9_fl4": combined_f9_fl4(),
        "fl5": fl5_conservation_discriminator(),
        "certificate": derivation_certificate(),
        "interpretation": (
            "σ (bond strength) and A (recoverable capacity) map onto standard "
            "materials observables. FL-4 is the novel EXTENT test — does cohesion "
            "return to pre-damage (latent capacity) or saturate (permanent "
            "damage)? — complementing F9's RATE test. FL-5 (conservation) is "
            "downstream of a calibrated κ."
        ),
    }
