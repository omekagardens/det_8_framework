"""
DET v8.0 — Applied Physics: κ-Proxy Ingest + κ-Dynamics Solver

Maps external dataset variables to DET inputs:

  T(t)        → τ_rec(T)        temperature modulates recovery (Arrhenius)
  Φ(t)        → κ̇_damage         radiation flux drives damage
  Δf/f / ΔL/L → κ(t)             the observable proxy (via R(κ) = R0(1−κ)^α)

and integrates the κ-dynamics:

  dκ/dt = −(κ − κ_eq)/τ_rec(t) + κ̇_damage(t)
"""

from __future__ import annotations

import math


K_B_EV = 8.617333262e-5  # Boltzmann constant, eV/K.


def temperature_to_tau_rec(T_t, tau0_s: float, E_a_eV: float):
    """T(t) [K] → τ_rec(t) [s] = τ0·exp(E_a/k_B T)."""
    return [tau0_s * math.exp(E_a_eV / (K_B_EV * T)) if T > 0 else float("inf")
            for T in T_t]


def flux_to_damage(flux_t, damage_rate: float):
    """Φ(t) [arb. flux] → κ̇_damage(t) [1/s] = damage_rate·Φ."""
    return [damage_rate * f for f in flux_t]


def observable_to_kappa(drift, R0: float = 1.0, alpha: float = 1.0):
    """Δf/f or ΔL/L → κ(t) via the calibrated proxy R(κ) = R0(1−κ)^α.

    κ = 1 − (R/R0)^(1/α), with R the observed (post-standard-subtraction) drift.
    """
    if R0 <= 0.0 or alpha <= 0.0:
        raise ValueError("R0 and alpha must be > 0")
    result = []
    for d in drift:
        ratio = max(0.0, d) / R0
        kappa = 1.0 - ratio ** (1.0 / alpha)
        result.append(max(0.0, min(1.0, kappa)))
    return result


def solve_kappa(
    kappa0: float,
    kappa_eq: float,
    tau_rec_t,
    damage_t,
    dt: float,
) -> list[float]:
    """Integrate dκ/dt = −(κ−κ_eq)/τ_rec(t) + κ̇_damage(t) (forward Euler).

    Handles time-varying τ_rec (temperature) and damage (radiation), which is
    the applied DET model: recovery competes with environmental damage.
    """
    n = len(tau_rec_t)
    if n != len(damage_t):
        raise ValueError("tau_rec_t and damage_t must have equal length")
    kappa = max(0.0, min(1.0, kappa0))
    out = [kappa]
    for i in range(1, n):
        tau = tau_rec_t[i]
        recovery = -(kappa - kappa_eq) / tau if tau > 0 and tau != float("inf") else 0.0
        dk = recovery + damage_t[i]
        kappa += dk * dt
        kappa = max(0.0, min(1.0, kappa))
        out.append(kappa)
    return out


def free_energy(kappa: float, kappa_eq: float, K: float) -> float:
    """DET structural free energy ψ = ½K(κ−κ_eq)²."""
    return 0.5 * K * (kappa - kappa_eq) ** 2
