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
from det8.models.f9_execution import f9_densified_silica_reference


def product_bounds() -> dict:
    """The three channel bounds, stated explicitly as products."""

    static = push_standard_qm_general(n=4, triple_weights={frozenset((0, 1, 2)): 1.0})
    clock = push_clock_channel()
    recovery = f9_densified_silica_reference()

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
            "result": "literature reference only — NOT executed",
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
        "status": (
            "ASSUMPTION, not a derivation: 'naturally O(1)' is a fine-tuning "
            "choice. λ_P is elsewhere stated free and underived (PHYSICS §2.1); "
            "assuming it is O(1) does not fix it."
        ),
    }


def cross_channel_ratio(bounds: dict | None = None) -> dict:
    """Angle B: dividing the two product bounds — flagged INVALID as stated."""

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
        "validity": (
            "INVALID as a DET constraint: it divides product bounds whose κ are "
            "NOT the same quantity — the κ of a photon three-slit interferometer "
            "and the κ of a ¹⁷¹Yb⁺ clock are 'independent couplings of the same "
            "structural-history κ' (dkappa_dynamics), so (λ_P·κ)/(κ·w₃) does not "
            "cancel to λ_P/w₃. The ratio is illustrative only."
        ),
        "interpretation": (
            "read only as a scale comparison, not a derived constraint: the clock "
            "product bound is ~10⁻¹³× tighter than the static product bound."
        ),
    }


def f9_breaks_or_confirms(bounds: dict | None = None) -> dict:
    """Angle C: the recovery channel is a literature reference, not an execution."""

    if bounds is None:
        bounds = product_bounds()
    recovery = bounds["recovery"]
    return {
        "result": recovery["bound"],
        "outcome": recovery["result"],
        "conclusion": (
            "E_a = 2.64 eV ≠ 0 (literature, densified silica) ⇒ recovery is "
            "Arrhenius ⇒ κ = defect density. This is a literature reference, not "
            "an execution: no (T, τ) data is ingested, and the null is predicted "
            "by standard theory. F9 remains unexecuted against real data."
        ),
    }


def degeneracy_resolution() -> dict:
    """The full account: what is NOT resolved, and what would finish it."""

    bounds = product_bounds()
    return {
        "problem": (
            "every channel bounds a product κ·(coupling), never κ alone"
        ),
        "bounds": bounds,
        "naturalness": naturalness_resolution(bounds),
        "cross_channel_ratio": cross_channel_ratio(bounds),
        "f9_literature_reference": f9_breaks_or_confirms(bounds),
        "resolved": (
            "Nothing is resolved to a κ-alone bound. What IS established: the "
            "three product bounds (static, clock, and the recovery literature "
            "reference), and the honest statement of what would finish the job."
        ),
        "not_resolved": (
            "the bounds remain on products; naturalness is an assumption, and the "
            "cross-channel ratio is invalid as a constraint. A full κ-alone bound "
            "still requires either a DET-internal derivation of λ_P (from "
            "Π = …(1+λ_P·κ)⁻¹) or a channel that measures κ directly rather than "
            "κ·coupling."
        ),
        "what_would_finish_it": [
            "derive λ_P from the participation aperture Π (the κ→proper-time coupling)",
            "a direct κ measurement independent of any coupling (e.g. a κ-preparation/measurement protocol from the F9 ladder)",
        ],
    }
