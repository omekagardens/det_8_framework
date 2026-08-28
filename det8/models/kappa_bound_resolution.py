"""DET — resolving the κ product-bound degeneracy.

Every κ channel bounds a *product* (κ·w₃, λ_P·κ, κ·γ), never κ alone:

  - static:   κ_static·w₃  ≲ 1.5×10⁻⁵   (three-slit, Kauten 2017)
  - clock:    λ_P·κ        ≲ 1.0×10⁻¹⁸  (atomic-clock universality, Lange 2021)
  - recovery: E_a = 2.64 eV ≠ 0         (densified silica, real data — null)

This module formalizes the three honest ways the degeneracy is *partially*
resolved, and states what would fully resolve it.

  A. Naturalness — w₃, λ_P are dimensionless couplings naturally O(1), so the
     tightest bound on κ is the clock channel: κ ≲ 10⁻¹⁸.
  B. Cross-channel ratio — dividing the two product bounds forces
     λ_P / w₃ ≲ 10⁻¹³, i.e. the Planck coupling is at most 10⁻¹³ times the
     static record weight (consistent with a genuinely small λ_P).
  C. Second independent channel — F9's real result (E_a = 2.64 eV) is a third
     null (κ = defect density), consistent with κ ≈ 0 but NOT an independent κ
     measurement, so it does not break the degeneracy by itself.

The full resolution requires either a DET-internal derivation of λ_P (from the
participation aperture Π = …(1+λ_P·κ)⁻¹) or a channel that measures κ directly
rather than κ·coupling.
"""

from __future__ import annotations

from det8.models.dkappa_decoherence import push_standard_qm_general
from det8.models.dkappa_dynamics import push_clock_channel
from det8.models.f9_execution import f9_densified_silica


def product_bounds() -> dict:
    """The three channel bounds, stated explicitly as products."""

    static = push_standard_qm_general(n=4, triple_weights={frozenset((0, 1, 2)): 1.0})
    clock = push_clock_channel()
    recovery = f9_densified_silica()

    return {
        "static": {
            "product": "κ_static · w₃",
            "bound": static["best_bound"]["kappa_DET_bound"],
            "experiment": static["best_bound"]["experiment"],
        },
        "clock": {
            "product": "λ_P · κ",
            "bound": clock["best_bound"]["lambda_P_kappa_bound"],
            "experiment": clock["best_bound"]["experiment"],
        },
        "recovery": {
            "product": "E_a (κ = defect density test)",
            "bound": recovery["activation_energy_eV"],
            "result": recovery["outcome"],
        },
    }


def naturalness_resolution(bounds: dict | None = None) -> dict:
    """Angle A: with O(1) couplings, the clock channel gives κ ≲ 10⁻¹⁸."""

    if bounds is None:
        bounds = product_bounds()
    clock_bound = bounds["clock"]["bound"]
    return {
        "argument": (
            "w₃ and λ_P are dimensionless couplings, naturally O(1) absent "
            "fine-tuning. The tightest product bound is the clock channel, so "
            "κ ≲ λ_P·κ ≲ 10⁻¹⁸."
        ),
        "kappa_bound": clock_bound,
        "couplings_assumed_O1": ["w₃", "λ_P"],
    }


def cross_channel_ratio(bounds: dict | None = None) -> dict:
    """Angle B: dividing the two product bounds constrains λ_P / w₃."""

    if bounds is None:
        bounds = product_bounds()
    static_bound = bounds["static"]["bound"]
    clock_bound = bounds["clock"]["bound"]
    ratio = clock_bound / static_bound
    return {
        "argument": (
            "(λ_P·κ) / (κ·w₃) = λ_P / w₃ ≲ (10⁻¹⁸) / (10⁻⁵) = 10⁻¹³."
        ),
        "lambda_P_over_w3_bound": ratio,
        "interpretation": (
            "the Planck coupling λ_P is at most 10⁻¹³ times the static record "
            "weight w₃ — so if w₃ = O(1), then λ_P ≲ 10⁻¹³, consistent with a "
            "genuinely small (Planck-scale) λ_P."
        ),
    }


def f9_breaks_or_confirms(bounds: dict | None = None) -> dict:
    """Angle C: F9's real result is a null, not an independent κ measurement."""

    if bounds is None:
        bounds = product_bounds()
    recovery = bounds["recovery"]
    return {
        "result": recovery["bound"],
        "outcome": recovery["result"],
        "conclusion": (
            "E_a = 2.64 eV ≠ 0 ⇒ recovery is Arrhenius ⇒ κ = defect density. "
            "This is a third null (consistent with κ ≈ 0), but it tests whether "
            "recovery is κ-driven or defect-driven — it does NOT measure κ "
            "independently, so it does not break the degeneracy by itself."
        ),
    }


def degeneracy_resolution() -> dict:
    """The full account: what is resolved, what is not, and what would finish it."""

    bounds = product_bounds()
    return {
        "problem": (
            "every channel bounds a product κ·(coupling), never κ alone"
        ),
        "bounds": bounds,
        "naturalness": naturalness_resolution(bounds),
        "cross_channel_ratio": cross_channel_ratio(bounds),
        "f9_real_result": f9_breaks_or_confirms(bounds),
        "resolved": (
            "κ ≲ 10⁻¹⁸ (clock, naturalness) and λ_P/w₃ ≲ 10⁻¹³ (cross-channel) "
            "are now honest, concrete statements; F9 adds a third null on real data."
        ),
        "not_resolved": (
            "the bounds remain on products; a full κ-alone bound still requires "
            "either a DET-internal derivation of λ_P (from Π = …(1+λ_P·κ)⁻¹) or "
            "a channel that measures κ directly rather than κ·coupling."
        ),
        "what_would_finish_it": [
            "derive λ_P from the participation aperture Π (the κ→proper-time coupling)",
            "a direct κ measurement independent of any coupling (e.g. a κ-preparation/measurement protocol from the F9 ladder)",
        ],
    }
