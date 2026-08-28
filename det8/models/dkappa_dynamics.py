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


# ── Part 1: push the clock channel (FL-1) to a concrete λ_P·κ bound ─────────


EXPERIMENTAL_CLOCK_BOUNDS = {
    "lange_2021": {
        "reference": "Lange et al., Phys. Rev. Lett. 126, 011102 (2021)",
        "system": "171Yb+ E2 vs E3 clock comparison (LPI)",
        "fractional_uncertainty": 1.0e-18,
        "note": "α variation 1.0(1.1)×10⁻¹⁸/yr",
    },
    "filzinger_2026": {
        "reference": "Filzinger et al. (2026), multi-ion Sr+ vs Yb+",
        "system": "88Sr+ / 171Yb+ frequency ratio",
        "fractional_uncertainty": 2.9e-18,
    },
    "pizzocaro_2026": {
        "reference": "Pizzocaro et al. (2026), Yb+ E3 at NPL vs PTB",
        "system": "international optical-fiber clock comparison",
        "fractional_uncertainty": 7.7e-18,
    },
}


def clock_kappa_bound(epsilon_clock: float) -> float:
    """λ_P·κ < ε/(1−ε) ≈ ε, from FL-1 Δν/ν = λ_P·κ/(1+λ_P·κ) < ε_clock."""

    if not 0.0 < epsilon_clock < 1.0:
        raise ValueError("epsilon must lie in (0,1)")
    return epsilon_clock / (1.0 - epsilon_clock)


def push_clock_channel() -> dict:
    """Invert the atomic-clock universality null through the FL-1 ansatz.

    Clock comparisons bound the fractional frequency difference ε_clock, so
    Δν/ν = λ_P·κ/(1+λ_P·κ) < ε_clock, i.e. λ_P·κ ≲ ε_clock ≈ 10⁻¹⁸.  This is
    the tightest κ-bound of the three channels, but it bounds the *product*
    λ_P·κ and only the *differential* (non-common-mode) coupling.
    """

    bounds = {}
    for key, exp in EXPERIMENTAL_CLOCK_BOUNDS.items():
        eps = exp["fractional_uncertainty"]
        bounds[key] = {
            "experiment": exp["reference"],
            "system": exp["system"],
            "epsilon_clock": eps,
            "lambda_P_kappa_bound": clock_kappa_bound(eps),
        }
    best = min(bounds, key=lambda k: bounds[k]["lambda_P_kappa_bound"])
    return {
        "theorem": "FL-1: Δν/ν = λ_P·κ/(1+λ_P·κ); clock null ⟹ λ_P·κ ≲ ε_clock",
        "experimental_bounds": bounds,
        "best_bound": {
            "experiment": bounds[best]["experiment"],
            "lambda_P_kappa_bound": bounds[best]["lambda_P_kappa_bound"],
        },
        "provenance": {
            "Δν/ν = λ_P·κ/(1+λ_P·κ)": "TH-DET — the DET clock ansatz (FL-1)",
            "inversion λ_P·κ < ε/(1−ε)": "MATH — algebra",
            "clock-comparison precision": "EXPERIMENT — Lange 2021, Filzinger 2026, Pizzocaro 2026",
        },
        "honest_caveat": (
            "Bounds the product λ_P·κ, not κ alone (λ_P is the unconstrained "
            "Planck-scale coupling). It constrains only the differential "
            "(species/transition-dependent) part of the κ clock coupling: a "
            "purely common-mode shift rescales proper time and is invisible to "
            "clock-ratio tests."
        ),
    }


# ── Part 2: two-time decoherent histories ───────────────────────────────────


def hamiltonian_2level(nu: float, kappa: float, coupling: float) -> list:
    """H_κ = (ν/2)σ_z + (κ·g/2)σ_x — the κ-dependent 2-level generator."""

    return [
        [complex(nu / 2.0, 0.0), complex(kappa * coupling / 2.0, 0.0)],
        [complex(kappa * coupling / 2.0, 0.0), complex(-nu / 2.0, 0.0)],
    ]


def evolution_operator_2level(
    nu: float, kappa: float, coupling: float, t: float
) -> list:
    """U_κ(t) = exp(−i H_κ t) via the Pauli closed form (no external linalg)."""

    g = kappa * coupling
    omega = math.sqrt(nu * nu + g * g)
    nz = nu / omega
    nx = g / omega
    c = math.cos(omega * t / 2.0)
    s = math.sin(omega * t / 2.0)
    return [
        [complex(c, -s * nz), complex(0.0, -s * nx)],
        [complex(0.0, -s * nx), complex(c, s * nz)],
    ]


def transition_probability(nu, kappa, coupling, t, a, b) -> float:
    """|⟨b|U_κ(t)|a⟩|² — the κ-dependent transition amplitude (the signature)."""

    U = evolution_operator_2level(nu, kappa, coupling, t)
    return abs(U[b][a]) ** 2


def two_time_decoherence_functional(nu, kappa, coupling, tau) -> dict:
    """𝔇((a,b),(a',b')) = A(a,b)·A(a',b')* for a pure initial |+⟩.

    Histories are 'start in |+⟩, pass through level a at t₁, end in level b at
    t₂'.  The diagonal is the two-time probability P(a,b) = |A(a,b)|².
    """

    U = evolution_operator_2level(nu, kappa, coupling, tau)
    root2 = math.sqrt(2.0)
    amplitudes = {(a, b): U[b][a] / root2 for a in (0, 1) for b in (0, 1)}

    functional = {}
    for a in (0, 1):
        for b in (0, 1):
            for ap in (0, 1):
                for bp in (0, 1):
                    functional[((a, b), (ap, bp))] = (
                        amplitudes[(a, b)] * amplitudes[(ap, bp)].conjugate()
                    )
    return functional


def single_time_born_rule(nu, kappa, coupling, tau, b) -> float:
    """P(b at t₂) = |⟨b|U_κ(τ)|+⟩|² — grade-2 (Born) regardless of κ."""

    U = evolution_operator_2level(nu, kappa, coupling, tau)
    root2 = math.sqrt(2.0)
    amplitude = (U[b][0] + U[b][1]) / root2
    return abs(amplitude) ** 2


def _is_unitary(U) -> bool:
    n = len(U)
    for i in range(n):
        for j in range(n):
            total = sum(U[i][k] * U[j][k].conjugate() for k in range(n))
            expected = 1.0 if i == j else 0.0
            if abs(total - expected) > 1e-12:
                return False
    return True


def demonstrate_two_time(nu: float = 1.0, coupling: float = 0.5, tau: float = 1.0) -> dict:
    """Show κ_dyn drives transitions while the single-time Born rule stays grade-2."""

    flip_zero = transition_probability(nu, 0.0, coupling, tau, 0, 1)
    flip_one = transition_probability(nu, 1.0, coupling, tau, 0, 1)
    p1_zero = single_time_born_rule(nu, 0.0, coupling, tau, 1)
    p0_one = single_time_born_rule(nu, 1.0, coupling, tau, 0)
    return {
        "theorem": (
            "single-time P(b) = |⟨b|U_κ|+⟩|² is a single modulus-squared (grade-2) "
            "for any κ; κ enters the transition amplitudes, not the grade."
        ),
        "transition_flip_at_kappa_zero": flip_zero,
        "transition_flip_at_kappa_one": flip_one,
        "dynamical_signature": flip_one > flip_zero,
        "single_time_normalized_kappa_zero": abs(
            p1_zero + single_time_born_rule(nu, 0.0, coupling, tau, 0) - 1.0
        )
        < 1e-12,
        "single_time_normalized_kappa_one": abs(
            p0_one + single_time_born_rule(nu, 1.0, coupling, tau, 1) - 1.0
        )
        < 1e-12,
        "unitarity_holds": _is_unitary(
            evolution_operator_2level(nu, 1.0, coupling, tau)
        ),
    }


