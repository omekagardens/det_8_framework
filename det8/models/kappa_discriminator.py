"""
DET v8.0 — κ vs. Defect-Density Discriminator (F9)

The gating experiment for Track A: is κ anything more than ordinary
defect density?

Standard defect density ρ_d relaxes by thermal annealing with an Arrhenius
timescale that is a STRONG function of temperature:

    τ_anneal(T) = τ_0 · exp(E_a / k_B T)

DET κ relaxes by the recovery law (det8_core / kappa_diffusion):

    dκ/dt = −(κ − κ_eq)/τ_rec

with a recovery timescale τ_rec that is, by hypothesis, a DET-native
structural quantity — NOT the thermal annealing time.

The discriminator: if κ-recovery tracks τ_anneal(T) across temperature,
then κ = defect density (relabeling; the clock anomaly is just the known
defect-induced shift). If κ-recovery follows τ_rec independently of T,
then κ is distinct from ordinary materials history — the first evidence
for a novel field.

This module simulates both hypotheses and computes the discriminating
statistic: the temperature dependence of the measured recovery time.

Status: P (proposed) — this simulates the protocol that must be run on
real samples (see red-team review §6, items 1–3).
"""

from __future__ import annotations

import math


K_B_EV = 8.617333262e-5  # Boltzmann constant, eV/K.


# ── Recovery timescales ─────────────────────────────────────────────────────


def annealing_timescale(
    T_K: float,
    E_a_eV: float,
    tau0_s: float,
) -> float:
    """τ_anneal(T) = τ_0·exp(E_a/(k_B·T)). Strong Arrhenius T-dependence.

    Higher T → shorter τ (faster annealing).
    """
    if T_K <= 0.0:
        raise ValueError("temperature must be > 0 K")
    return tau0_s * math.exp(E_a_eV / (K_B_EV * T_K))


def kappa_recovery_timescale(tau_rec_s: float) -> float:
    """κ recovery timescale τ_rec — by hypothesis T-independent."""
    return tau_rec_s


# ── Trajectories ────────────────────────────────────────────────────────────


def defect_density(
    t: float,
    rho0: float,
    T_K: float,
    E_a_eV: float,
    tau0_s: float,
) -> float:
    """ρ_d(t) = ρ_0·exp(−t/τ_anneal(T)) — thermal annealing."""
    tau = annealing_timescale(T_K, E_a_eV, tau0_s)
    return rho0 * math.exp(-t / tau)


def kappa_trajectory(
    t: float,
    kappa0: float,
    kappa_eq: float,
    tau_rec_s: float,
) -> float:
    """κ(t) = κ_eq + (κ_0 − κ_eq)·exp(−t/τ_rec) — DET recovery."""
    return kappa_eq + (kappa0 - kappa_eq) * math.exp(-t / tau_rec_s)


def clock_shift(
    kappa: float,
    lambda_p: float,
) -> float:
    """Δν/ν = λ_P·κ/(1 + λ_P·κ) — the DET clock signal (F10 convention)."""
    return lambda_p * kappa / (1.0 + lambda_p * kappa)


# ── The discriminator ───────────────────────────────────────────────────────


def discriminator_signature(
    T_low_K: float = 300.0,
    T_high_K: float = 900.0,
    E_a_eV: float = 1.0,
    tau0_s: float = 1e-13,
    tau_rec_s: float = 1e4,
) -> dict:
    """The temperature dependence that separates κ from defect density.

    Defect model: recovery time changes by τ_anneal(T_low)/τ_anneal(T_high)
                  ≈ exp(E_a/k_B·(1/T_low − 1/T_high))  (≫ 1 over a sweep).
    κ model:       recovery time is T-independent (ratio = 1).

    If a measured recovery time is constant across the sweep, κ ≠ defect
    density; if it tracks the Arrhenius law, κ = defect density.
    """
    tau_a_low = annealing_timescale(T_low_K, E_a_eV, tau0_s)
    tau_a_high = annealing_timescale(T_high_K, E_a_eV, tau0_s)
    tau_k_low = kappa_recovery_timescale(tau_rec_s)
    tau_k_high = kappa_recovery_timescale(tau_rec_s)

    defect_ratio = tau_a_high / tau_a_low          # < 1 (faster at high T).
    kappa_ratio = tau_k_high / tau_k_low           # = 1 (T-independent).
    sweep_factor = tau_a_low / tau_a_high if tau_a_high > 0 else float("inf")

    distinguishable = (
        abs(kappa_ratio - 1.0) < 1e-12
        and abs(sweep_factor - 1.0) > 1e-3
    )

    return {
        "T_low_K": T_low_K,
        "T_high_K": T_high_K,
        "tau_anneal_low_s": tau_a_low,
        "tau_anneal_high_s": tau_a_high,
        "tau_rec_s": tau_rec_s,
        "defect_T_ratio": defect_ratio,
        "kappa_T_ratio": kappa_ratio,
        "annealing_sweep_factor": sweep_factor,
        "distinguishable": distinguishable,
        "verdict": (
            f"Thermal annealing changes the recovery time by ×{sweep_factor:.1e} "
            f"over {T_low_K:.0f}→{T_high_K:.0f} K (Arrhenius); κ-recovery is "
            f"T-independent (×{kappa_ratio:.3f}). A measured recovery time that "
            f"does NOT track the Arrhenius law is the discriminator: κ ≠ defect "
            f"density. If it DOES track it, κ = defect density (no novelty)."
        ),
    }


# ── Simulated clock-signal decay under each hypothesis ─────────────────────


def simulate_signal_decay(
    t_values: list[float],
    kappa0: float = 0.5,
    kappa_eq: float = 0.0,
    tau_rec_s: float = 1e4,
    rho0: float = 0.5,
    T_K: float = 600.0,
    E_a_eV: float = 1.0,
    tau0_s: float = 1e-13,
    lambda_p: float = 1.0,
) -> dict:
    """Clock-shift decay under the κ model vs a defect-driven model.

    The κ-driven shift decays with τ_rec; the defect-driven shift decays
    with τ_anneal(T). The two decay constants differ, which is the temporal
    signature separating the hypotheses.
    """
    kappa_series = [kappa_trajectory(t, kappa0, kappa_eq, tau_rec_s) for t in t_values]
    shift_kappa = [clock_shift(k, lambda_p) for k in kappa_series]

    tau_anneal = annealing_timescale(T_K, E_a_eV, tau0_s)
    defect_series = [defect_density(t, rho0, T_K, E_a_eV, tau0_s) for t in t_values]
    shift_defect = [lambda_p * d / (1.0 + lambda_p * d) for d in defect_series]

    return {
        "t_values": t_values,
        "kappa_series": kappa_series,
        "defect_series": defect_series,
        "shift_kappa": shift_kappa,
        "shift_defect": shift_defect,
        "tau_rec_s": tau_rec_s,
        "tau_anneal_s": tau_anneal,
        "interpretation": (
            f"κ-driven clock shift decays with τ_rec = {tau_rec_s:.1e} s; "
            f"defect-driven shift decays with τ_anneal = {tau_anneal:.1e} s at "
            f"{T_K:.0f} K. The decay constants differ by ×{tau_rec_s/tau_anneal:.1e} "
            f"— the temporal signature that separates the two hypotheses."
        ),
    }
