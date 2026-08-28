"""DET — dynamical κ (κ in time-evolution, not the single-time measure).

The D_κ push bounded the *static* κ-coupling — a grade-3 record term in the
single-time decoherence functional — via three-slit interference.  But κ also
couples, independently, to the *time-evolution* (the generator / "law map" L).
This module formalizes that dynamical coupling and shows the three-slit null
does not reach it.

Key theorem (MATH): any unitary Born-rule evolution produces a grade-2
single-time measure, P = |Σₛ Aₛ|², so its third-order interference I₃ = 0 at
every fixed time — regardless of κ in the generator.  Dynamical κ shifts the
*amplitudes* Aₛ (their phases and decay), never their grade-2 structure, so a
three-slit experiment is blind to it.

Dynamical κ signatures (where it is *not* blind):
  - clock (FL-1):   κ_dyn shifts the frequency → Δν = κ_dyn·v.
  - recovery (F9):  κ_dyn shifts the relaxation rate → τ_rec(κ_dyn).

The three channels — static interference (κ_static), clock, and recovery — are
therefore three *independent* couplings of the same structural-history κ.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass


# ── The grade-2 theorem: dynamical κ is three-slit-blind ────────────────────


def path_amplitudes(
    kappa_dyn: float,
    *,
    magnitudes=(1.0, 1.0, 1.0),
    base_phases=(0.0, 0.0, 0.0),
    phase_couplings=(1.0, 1.0, 1.0),
) -> tuple:
    """Three path amplitudes Aₛ = aₛ·exp(i(φₛ + κ_dyn·cₛ)).

    Dynamical κ enters the *phase* of each path (its generator), not the
    magnitude.  This is where a clock sees κ.
    """

    return tuple(
        m * cmath.exp(1j * (p + kappa_dyn * c))
        for m, p, c in zip(magnitudes, base_phases, phase_couplings)
    )


def born_rule_probability(amplitudes: tuple, subset) -> float:
    """P(subset) = |Σ_{s∈subset} Aₛ|² — a grade-2 (Born) single-time measure."""

    total = sum(amplitudes[i] for i in subset)
    return abs(total) ** 2


def third_order_interference(amplitudes: tuple) -> float:
    """I₃ = P_ABC − P_AB − P_AC − P_BC + P_A + P_B + P_C."""

    p = lambda *idx: born_rule_probability(amplitudes, idx)
    return p(0, 1, 2) - p(0, 1) - p(0, 2) - p(1, 2) + p(0) + p(1) + p(2)


def grade2_theorem(kappa_dyn_values=(0.0, 0.1, 0.5, 1.0, 10.0)) -> dict:
    """Show I₃ = 0 for every κ_dyn: dynamical κ is invisible to three-slit."""

    residuals = []
    for kappa in kappa_dyn_values:
        amplitudes = path_amplitudes(kappa)
        residuals.append(abs(third_order_interference(amplitudes)))
    maximum = max(residuals)
    return {
        "theorem": "P = |Σₛ Aₛ|² is grade-2 for any generator, so I₃ = 0 for every κ_dyn",
        "kappa_dyn_values": kappa_dyn_values,
        "max_I3_residual": maximum,
        "holds": maximum < 1e-12,
    }


# ── Dynamical signatures ────────────────────────────────────────────────────


def clock_frequency_shift(kappa_dyn: float, coupling: float) -> float:
    """Δν = κ_dyn · v — first-order frequency shift (MATH, linear)."""

    return kappa_dyn * coupling


def clock_frequency_shift_det(kappa: float, lambda_P: float) -> float:
    """Δν/ν = λ_P·κ / (1 + λ_P·κ) — the DET clock ansatz (FL-1, TH-DET)."""

    if lambda_P < 0.0:
        raise ValueError("lambda_P must be non-negative")
    return lambda_P * kappa / (1.0 + lambda_P * kappa)


def recovery_timescale(kappa_dyn: float, tau_0: float, gamma: float) -> float:
    """τ_rec = τ_0 / (1 + κ_dyn·γ) — κ_dyn speeds up record relaxation (F9)."""

    if tau_0 <= 0.0 or gamma < 0.0:
        raise ValueError("tau_0 must be positive and gamma non-negative")
    return tau_0 / (1.0 + kappa_dyn * gamma)


# ── Unification of the three channels ───────────────────────────────────────


def unify_channels(
    *,
    kappa_dyn=1.0,
    clock_coupling=1e6,        # Hz per κ
    lambda_P=1e-8,             # DET clock saturation scale
    tau_0=1e4,                 # s
    recovery_gamma=0.5,
) -> dict:
    """Show κ_static, the clock, and recovery are independent κ channels.

    Returns the three signatures and the honest conclusion: the three-slit
    bound on κ_static (≲ 10⁻⁵) does not constrain κ_dyn, which the clock and
    recovery channels must probe separately.
    """

    theorem = grade2_theorem()
    return {
        "grade2_theorem": theorem,
        "static_channel": (
            "κ_static (grade-3 record term) — bounded by three-slit to ≲ 10⁻⁵; "
            "independent of the dynamical couplings below."
        ),
        "clock_channel": {
            "frequency_shift_linear": clock_frequency_shift(
                kappa_dyn, clock_coupling
            ),
            "fractional_shift_det": clock_frequency_shift_det(
                kappa_dyn, lambda_P
            ),
            "probe": "FL-1 common-mode clock universality",
        },
        "recovery_channel": {
            "tau_rec": recovery_timescale(kappa_dyn, tau_0, recovery_gamma),
            "probe": "F9 τ_rec-vs-annealing discriminator",
        },
        "unification": (
            "Static interference, the clock, and recovery are three independent "
            "couplings of the same structural-history κ. The three-slit null "
            "closes the static channel; the clock (FL-1) and recovery (F9) "
            "channels remain open and are probed by their own experiments."
        ),
        "provenance": {
            "P = |Σₛ Aₛ|² is grade-2": "MATH — Born rule / Sorkin grade-2",
            "I₃ = 0 for any generator": "MATH — grade-2 structure",
            "Δν = κ_dyn·v (linear)": "MATH — first-order perturbation",
            "Δν/ν = λ_P·κ/(1+λ_P·κ)": "TH-DET — the DET clock ansatz (FL-1)",
            "τ_rec = τ_0/(1+κ_dyn·γ)": "TH-DET — the DET recovery ansatz (F9)",
            "channels are independent": "TH-DET — κ couples to each channel separately",
        },
    }
