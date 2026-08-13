"""
DET v8.0 — Applied Physics: Standard-Physics Adversary

The industry-standard baselines that DET must beat, and the BIC comparison
machinery. Rule (per the applied-physics program): DET claims a "win" ONLY if
the κ-model yields a LOWER Bayesian Information Criterion than the standard
model on the same data.
"""

from __future__ import annotations

import math


K_B_EV = 8.617333262e-5  # Boltzmann constant, eV/K.


# ── Model-selection machinery ───────────────────────────────────────────────


def bic(n_params: int, n_data: int, rss: float) -> float:
    """Bayesian Information Criterion.

    BIC = n·ln(RSS/n) + k·ln(n). Lower is better. Penalizes extra parameters.
    A perfect fit (RSS = 0) is −inf — the best possible.
    """
    if n_data <= 0:
        return float("inf")
    if rss <= 0.0:
        return float("-inf")
    return n_data * math.log(rss / n_data) + n_params * math.log(n_data)


def compare_bic(
    det_n_params: int,
    det_rss: float,
    std_n_params: int,
    std_rss: float,
    n_data: int,
) -> dict:
    """Compare DET κ-model vs standard model by BIC.

    det_wins is True iff BIC_det < BIC_std.
    """
    b_det = bic(det_n_params, n_data, det_rss)
    b_std = bic(std_n_params, n_data, std_rss)
    return {
        "bic_det": b_det,
        "bic_std": b_std,
        "det_wins": b_det < b_std,
        "delta_bic": b_det - b_std,
        "verdict": "DET wins" if b_det < b_std else "standard model wins (or tie)",
    }


# ── Standard baselines ──────────────────────────────────────────────────────


def ieee_clock_aging(t: float, a: float, b: float, c: float) -> float:
    """IEEE-style clock aging: y(t) = a·ln(1+t) + b·t + c (fractional frequency)."""
    return a * math.log1p(t) + b * t + c


def kww_relaxation(t: float, tau: float, beta: float) -> float:
    """Kohlrausch–Williams–Watts stretched exponential: exp(−(t/τ)^β).

    The standard empirical model for glass/metallurgical structural relaxation.
    β < 1 (a distribution of activation energies); β = 1 is single-exponential.
    """
    if tau <= 0.0:
        return 0.0
    return math.exp(-((t / tau) ** beta))


def arrhenius_rate(T_K: float, tau0_s: float, E_a_eV: float) -> float:
    """Arrhenius recovery rate: (1/τ0)·exp(−E_a/k_B T). Temperature-only."""
    if T_K <= 0.0:
        return 0.0
    return (1.0 / tau0_s) * math.exp(-E_a_eV / (K_B_EV * T_K))


def ddd_degradation(cumulative_flux: float, k: float) -> float:
    """Displacement Damage Dose: monotonic degradation ∝ cumulative flux."""
    return k * cumulative_flux


def least_squares_fit_linear(xs, ys):
    """Ordinary least squares for y = m·x + b. Returns (m, b, rss)."""
    n = len(xs)
    if n == 0:
        return 0.0, 0.0, float("inf")
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-15:
        return 0.0, 0.0, float("inf")
    m = (n * sxy - sx * sy) / denom
    b = (sxx * sy - sx * sxy) / denom
    rss = sum((y - (m * x + b)) ** 2 for x, y in zip(xs, ys))
    return m, b, rss


def rss_between(predicted, observed) -> float:
    """Residual sum of squares between two equal-length series."""
    return sum((p - o) ** 2 for p, o in zip(predicted, observed))
