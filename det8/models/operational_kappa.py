"""
DET v8.0 — Operational κ and the Precision-Materials Program (L0/L1/L2)

Reframes Track A as a precision-measurement program for detecting and
controlling history-dependent structural effects in materials used by clocks,
oscillators, and quantum devices. This keeps DET consistent with Option B
(κ couples only to participation, not gravity) while giving it a realistic
experimental home.

Three layers, each valuable on its own:

  L0 — κ as an engineering descriptor of structural history.
       Useful even if DET is false.
  L1 — κ as an INDEPENDENT residual beyond standard materials variables.
       The empirical Track A milestone (the scientific discriminator).
  L2 — κ coupling to proper time / clock rate via λ_P.
       The risky DET-specific prediction.

Operational κ (κ_op) is a METROLOGICAL quantity, not a purely theoretical
variable:

  z = f_std(x_std) + s·κ_op + ε

  z     : vector of measured material responses (multiple probes).
  x_std : standard material variables.
  f_std : the best standard-physics model.
  s     : the calibrated κ-sensitivity (per probe).
  ε     : residual noise.

  κ̂_op = Σ w_i s_i (z_i − f_std_i) / Σ w_i s_i²     (weighted least squares)
  u(κ_op) = 1 / sqrt(Σ w_i s_i²)                     (reported per sample)

Two guardrails for credibility:

  1. Standard-variable completeness audit — every standard variable capable of
     producing > 0.05× the expected DET signal at target sensitivity must be
     measured, bounded, or actively stabilized.
  2. Anti-circularity — κ must NOT be inferred from the clock anomaly it is
     used to test. Allowed: mechanical/calorimetric/microscopic/transport,
     a separate reference sample, a non-clock oscillator. Forbidden: the clock
     anomaly itself, post hoc adjustment, calibration after seeing the shift.
"""

from __future__ import annotations

import math
from typing import Optional


# ── The three layers ────────────────────────────────────────────────────────


def kappa_layers() -> list[dict]:
    """The L0/L1/L2 layer structure of the precision-materials program."""
    return [
        {
            "layer": "L0",
            "claim": "κ as an engineering descriptor of structural history",
            "status": "useful even if DET is false",
        },
        {
            "layer": "L1",
            "claim": "κ as an independent residual beyond standard materials variables",
            "status": "empirical Track A milestone (the scientific discriminator)",
        },
        {
            "layer": "L2",
            "claim": "κ coupling to proper time / clock rate via λ_P",
            "status": "the risky DET prediction",
        },
    ]


# ── Operational κ (metrological estimate) ───────────────────────────────────


def operational_kappa(
    z: list[float],
    f_std: list[float],
    s: list[float],
    noise: Optional[list[float]] = None,
) -> dict:
    """The metrological κ_op estimate via weighted least squares.

    Model:  z_i = f_std_i + s_i·κ_op + ε_i,  Var(ε_i) = noise_i².

    κ̂_op = Σ w_i s_i r_i / Σ w_i s_i²,   r_i = z_i − f_std_i,  w_i = 1/noise_i².
    u(κ_op) = 1 / sqrt(Σ w_i s_i²).

    Returns κ_op and its uncertainty — the L1 quantity (the residual beyond
    standard physics), ready for the L2 clock test.
    """
    n = len(z)
    if not (len(f_std) == n and len(s) == n):
        raise ValueError("z, f_std, s must have equal length")
    if n == 0:
        raise ValueError("empty inputs")
    if noise is None:
        noise = [1.0] * n
    if len(noise) != n:
        raise ValueError("noise must match length")

    r = [zi - fi for zi, fi in zip(z, f_std)]
    w = [1.0 / (ni**2) if ni > 0 else float("inf") for ni in noise]

    numerator = sum(wi * si * ri for wi, si, ri in zip(w, s, r))
    denominator = sum(wi * si * si for wi, si in zip(w, s))

    if denominator <= 1e-15:
        kappa = None
        u_kappa = float("inf")
    else:
        kappa = numerator / denominator
        u_kappa = math.sqrt(1.0 / denominator)

    return {
        "kappa_op": kappa,
        "uncertainty": u_kappa,
        "n_probes": n,
        "residuals": r,
        "sensitivity_snr": (
            sum(si * si / (ni**2) for si, ni in zip(s, noise)) if noise else 0.0
        ),
        "interpretation": (
            f"κ_op = {kappa if kappa is None else round(kappa, 4)} ± "
            f"{u_kappa if u_kappa == float('inf') else round(u_kappa, 4)} — the "
            f"multi-probe residual beyond the standard-physics model."
        ),
    }


# ── Standard-variable completeness audit ────────────────────────────────────


def standard_variable_audit() -> dict:
    """The completeness checklist for the κ-residual claim.

    Rule: any parameter capable of producing > 0.05× the expected DET signal
    at the target sensitivity must be measured, bounded, or actively
    stabilized (strengthened from the earlier 0.1× rule).
    """
    return {
        "rule": (
            "Any standard parameter capable of producing > 0.05× the expected "
            "DET signal at the target sensitivity must be measured, bounded, or "
            "actively stabilized."
        ),
        "categories": {
            "thermal": ["temperature", "thermal history", "annealing schedule", "gradients"],
            "structural": ["density", "lattice parameter", "crystallinity", "grain size"],
            "defects": ["vacancy density", "interstitial density", "dislocation density", "Frenkel pairs"],
            "mechanical": ["residual stress", "elastic moduli", "hardness", "strain"],
            "electrical": ["resistivity", "charge state", "dielectric loss"],
            "optical": ["absorption", "color centers", "scattering"],
            "chemical": ["impurity content", "oxidation state", "hydrogen content"],
            "surface": ["adsorbates", "oxide layers", "surface roughness"],
            "environmental": ["magnetic field", "electric field", "pressure", "vibration", "radiation dose"],
        },
        "n_categories": 9,
    }


# ── Anti-circularity guard ──────────────────────────────────────────────────

_ALLOWED_KAPPA_SOURCES = {
    "mechanical",
    "calorimetric",
    "microscopic",
    "transport",
    "reference_sample",
    "non_clock_oscillator",
}

_FORBIDDEN_KAPPA_SOURCES = {
    "clock_anomaly_itself",
    "post_hoc_adjustment",
    "calibration_after_shift",
}


def circularity_guard(kappa_source: str) -> dict:
    """Classify a κ-measurement source as allowed or circular.

    The κ value used in the clock prediction must NOT be inferred from the
    same clock frequency shift being tested.
    """
    if kappa_source in _ALLOWED_KAPPA_SOURCES:
        return {
            "source": kappa_source,
            "allowed": True,
            "detail": "Independent of the clock anomaly — admissible.",
        }
    if kappa_source in _FORBIDDEN_KAPPA_SOURCES:
        return {
            "source": kappa_source,
            "allowed": False,
            "detail": "Circular — the κ value is inferred from (or adjusted to) the clock shift it is meant to test.",
        }
    return {
        "source": kappa_source,
        "allowed": False,
        "detail": "Unrecognized source — must be independently justified.",
    }


# ── Consolidated precision-materials program summary ───────────────────────


def precision_materials_program() -> dict:
    """The full strategic framing: layers + operational κ + guardrails."""
    return {
        "reframing": (
            "Track A is a precision-measurement program for detecting and "
            "controlling history-dependent structural effects in materials used "
            "by clocks, oscillators, and quantum devices."
        ),
        "layers": kappa_layers(),
        "operational_kappa": (
            "κ_op is a metrological quantity: z = f_std(x_std) + s·κ_op + ε, "
            "κ̂_op = Σ w_i s_i (z_i − f_std_i)/Σ w_i s_i², with u(κ_op) per sample."
        ),
        "completeness_audit": standard_variable_audit(),
        "circularity_rule": (
            "κ must not be inferred from the clock anomaly it is used to test "
            "(mechanical/calorimetric/microscopic/transport, a reference sample, "
            "or a non-clock oscillator only)."
        ),
        "l0_value": (
            "Even if L1 and L2 fail, L0 (κ as an engineering descriptor of "
            "structural history) has applied value on its own."
        ),
    }
