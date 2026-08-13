"""
DET v8.0 — Falsification Ladder & Data Guardrail (Option B)

DET is a participation/measurement theory with ONE falsifiable prediction:
the κ-Π clock anomaly (Δν/ν = λ_P·κ / (1 + λ_P·κ)). This module defines:

1. The FALSIFICATION LADDER — the ordered, DET-native experiments that test
   (and can falsify) the claim, with explicit decision rules.
2. The DATA GUARDRAIL — every external dataset was built under a DIFFERENT
   theory (GR, ΛCDM, materials science), so only its theory-independent
   OBSERVED quantity is admissible; its theory-dependent interpretation is
   quarantined.
3. The DECISION LOGIC — given lab results, classify the outcome as
   falsified / bounded / consistent / confirmed.

Gravity-emergence note: gravity is NOT a current DET claim, but the door is
left open. "Does κ source or modify gravity?" is an OPEN research frontier,
not a rejected hypothesis; the retired gravity modules are archived so the
question can be revisited if a DET-native mechanism ever emerges.

Operational layer: SI conversion is via det_units (clock Δν/ν ↔ λ_P, proxy
R/R₀ ↔ κ). The fractional quantities used here are dimensionless and
anchor-free.
"""

from __future__ import annotations

import math


# ── Falsification ladder ────────────────────────────────────────────────────


def falsification_ladder() -> list[dict]:
    """The ordered, DET-native experiments that test the clock-anomaly claim.

    Each step names the question, the measurement, and the explicit
    falsification / confirmation conditions.
    """
    return [
        {
            "step": 1,
            "name": "κ-vs-defect-density discriminator (F9)",
            "question": "Is κ anything beyond ordinary material history?",
            "measurement": "recovery timescale τ_rec across temperature T",
            "falsifies_if": (
                "τ_rec tracks the Arrhenius annealing law τ_anneal = τ_0·exp(E_a/k_B T) "
                "⇒ κ = defect density ⇒ DET is a relabeling"
            ),
            "confirms_if": (
                "τ_rec is T-independent (distinct from thermal annealing) "
                "⇒ κ is a distinct field"
            ),
            "module": "kappa_discriminator.py",
        },
        {
            "step": 2,
            "name": "Structural-proxy calibration",
            "question": "Can κ be measured independently of the clock?",
            "measurement": (
                "residual after regressing probe response against all known "
                "material variables (density, defect density, stress, …)"
            ),
            "falsifies_if": (
                "residual = 0 after the known-physics regression ⇒ κ = ordinary "
                "materials science ⇒ no independent κ"
            ),
            "confirms_if": "nonzero residual, cross-validated, reproducible",
            "module": "structural_proxy.py",
        },
        {
            "step": 3,
            "name": "Clock comparison",
            "question": "Does κ change the clock rate?",
            "measurement": (
                "fractional frequency difference Δν/ν between two κ-prepared "
                "clocks (κ_A = 0 reference, κ_B = κ)"
            ),
            "falsifies_if": (
                "null at precision σ ⇒ λ_P·κ < σ (λ_P bounded from above; "
                "the prediction is null at that precision)"
            ),
            "confirms_if": "Δν/ν = λ_P·κ/(1+λ_P·κ) at ≥5σ with the correct sign",
            "module": "clock_experiment.py",
        },
    ]


# ── Data guardrail ──────────────────────────────────────────────────────────


DATA_PROVENANCE = {
    "atomic_clock_comparison": {
        "origin_theory": "GR + quantum metrology",
        "observed_quantity": "fractional frequency ratio Δν/ν (theory-independent)",
        "derived_quantity": "gravitational redshift / relativistic corrections (GR-dependent)",
        "safe_use": "constrain λ_P·κ via Δν/ν = λ_P·κ/(1+λ_P·κ)",
    },
    "material_response": {
        "origin_theory": "materials science (elasticity, defect theory)",
        "observed_quantity": "probe response R (hardness, resistivity, …) (theory-independent)",
        "derived_quantity": "dislocation density / residual stress (materials-science-dependent)",
        "safe_use": "structural-proxy input: κ = 1 − (R/R₀)^(1/p)",
    },
    "sparc_rotation_curves": {
        "origin_theory": "ΛCDM (dark-matter halos)",
        "observed_quantity": "velocity field v(r) (theory-independent)",
        "derived_quantity": "dark-matter halo profile (ΛCDM-dependent)",
        "safe_use": "N/A under Option B (gravity program retired) — archived",
    },
    "eotvos_eta": {
        "origin_theory": "GR / equivalence principle",
        "observed_quantity": "Eötvös ratio η (theory-independent)",
        "derived_quantity": "bound on a fifth force (model-dependent)",
        "safe_use": "N/A under Option B (no fifth force in DET) — informational",
    },
}


def data_guardrail(dataset_key: str) -> dict:
    """Return the provenance + safe-use label for an external dataset.

    The guardrail is: only the OBSERVED quantity is admissible; the DERIVED
    quantity (valid only under the originating theory) is quarantined.
    """
    if dataset_key not in DATA_PROVENANCE:
        raise KeyError(f"unknown dataset: {dataset_key}")
    entry = dict(DATA_PROVENANCE[dataset_key])
    entry["dataset"] = dataset_key
    entry["rule"] = (
        "Use ONLY the observed_quantity. The derived_quantity is valid only "
        "under the origin_theory, not under DET."
    )
    return entry


# ── Decision logic ──────────────────────────────────────────────────────────


def classify_clock_result(
    measured_shift: float,
    sigma: float = 1e-18,
    required_sigma: float = 5.0,
) -> dict:
    """Classify a clock-comparison result (the sole prediction).

    measured_shift = Δν/ν (dimensionless, SI-observed ratio).
    sigma = measurement precision (fractional).
    """
    if sigma <= 0.0:
        raise ValueError("sigma must be > 0")
    significance = abs(measured_shift) / sigma

    if significance < 1.0:
        verdict = "null"
        detail = (
            f"|Δν/ν| = {measured_shift:.2e} < σ = {sigma:.0e} ⇒ λ_P·κ < σ. "
            f"The prediction is not confirmed at this precision; λ_P is bounded."
        )
    elif significance >= required_sigma and measured_shift > 0.0:
        verdict = "consistent"
        detail = (
            f"Δν/ν = {measured_shift:.2e} at {significance:.1f}σ with the correct "
            f"sign ⇒ consistent with Δν/ν = λ_P·κ/(1+λ_P·κ)."
        )
    else:
        verdict = "anomalous"
        detail = (
            f"|Δν/ν| = {measured_shift:.2e} at {significance:.1f}σ but wrong sign "
            f"or below {required_sigma:.0f}σ ⇒ not the predicted signal."
        )

    return {
        "measured_shift": measured_shift,
        "sigma": sigma,
        "significance": significance,
        "verdict": verdict,
        "detail": detail,
    }


def classify_discriminator_result(
    recovery_ratio: float,
    arrhenius_expected: float,
    tolerance: float = 0.1,
) -> dict:
    """Classify the F9 discriminator result.

    recovery_ratio = measured τ_rec(T_high)/τ_rec(T_low).
    arrhenius_expected = the ratio predicted by thermal annealing.
    κ is distinct iff recovery_ratio ≈ 1 (T-independent); it is defect density
    iff recovery_ratio ≈ arrhenius_expected (tracks the Arrhenius law).
    """
    tracks_arrhenius = abs(recovery_ratio - arrhenius_expected) <= tolerance * abs(arrhenius_expected)
    t_independent = abs(recovery_ratio - 1.0) <= tolerance

    if tracks_arrhenius and not t_independent:
        verdict = "falsified"
        detail = (
            f"recovery ratio {recovery_ratio:.2e} tracks the Arrhenius law "
            f"({arrhenius_expected:.2e}) ⇒ κ = defect density ⇒ DET is a relabeling."
        )
    elif t_independent and not tracks_arrhenius:
        verdict = "distinct"
        detail = (
            f"recovery ratio ≈ 1 (T-independent) ⇒ κ is distinct from thermal "
            f"annealing ⇒ proceed to proxy calibration."
        )
    else:
        verdict = "inconclusive"
        detail = "recovery ratio is ambiguous between the two hypotheses."

    return {
        "recovery_ratio": recovery_ratio,
        "arrhenius_expected": arrhenius_expected,
        "verdict": verdict,
        "detail": detail,
    }


# ── Gravity-emergence note ──────────────────────────────────────────────────


def gravity_emergence_note() -> dict:
    """Record that gravity is not a current claim but the door is open."""
    return {
        "status": "OPEN research frontier (not a rejected hypothesis)",
        "current_position": (
            "Option B (Round 6): κ couples only to participation; gravity is "
            "standard GR and dark matter is standard."
        ),
        "revisit_condition": (
            "A DET-native mechanism that sources or modifies gravity may be "
            "revisited IF and only if it is DERIVED from DET primitives and "
            "survives the same falsification discipline (equivalence principle, "
            "Eötvös, rotation curves) — not imported from a non-DET theory."
        ),
        "archived_modules": (
            "gravity_v2.py, sparc_analysis.py, cluster_dynamics.py, "
            "post_newtonian.py, kappa_derivation.py, det_gravity.py, "
            "gravity_experiment.py — retained for audit, not active claims."
        ),
    }


# ── Claim register (Option B) ───────────────────────────────────────────────


def claim_register() -> dict:
    """The active DET claims under Option B, with status labels."""
    return {
        "clock_anomaly": {
            "claim": "Δν/ν = λ_P·κ/(1+λ_P·κ) — two κ-prepared clocks tick at different rates.",
            "status": "PR (pre-registered, falsifiable)",
            "falsifies": "null at precision σ ⇒ λ_P·κ < σ",
        },
        "structural_proxy": {
            "claim": "κ can be measured independently via a calibrated probe response R(κ) = R₀(1−κ)^p.",
            "status": "P (proposed; gated on F9 discriminator)",
            "falsifies": "zero residual after known-physics regression",
        },
        "kappa_distinct_field": {
            "claim": "κ is a distinct field, not ordinary defect density.",
            "status": "P (proposed; gated on temporal signature)",
            "falsifies": "τ_rec tracks thermal annealing",
        },
        "gravity_emergence": {
            "claim": "κ does NOT source or modify gravity (current).",
            "status": "OPEN frontier (not claimed)",
            "falsifies": "N/A — no gravity claim is made",
        },
    }
