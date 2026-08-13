"""
DET v8.0 — Applied Physics: the κ-Residual Discriminator

The DET signature vs the standard-defect signature in a relaxation trace.

Standard defect / glass relaxation (KWW): a DISTRIBUTION of activation
energies → stretched exponential  exp(−(t/τ)^β)  with β < 1.

DET κ-recovery: ONE structural-history variable, single relaxation time →
single exponential  exp(−t/τ)  with β = 1 (Debye).

The discriminator: fit the recovery trace to y = A·exp(−(t/τ)^β) and read β.
  β ≈ 1  → single-exponential (DET-like: one κ, one τ_rec).
  β < 1  → stretched (defect-like: a spectrum of defect activation energies).

This is the applied, L1-level discriminator: it tests whether the residual
relaxation is a single κ variable or a defect spectrum — WITHOUT invoking λ_P.
"""

from __future__ import annotations

import math


def fit_kww(
    t,
    y,
    tau_grid=(1.0, 2.0, 5.0, 10.0, 20.0, 30.0, 50.0, 70.0, 100.0, 150.0, 200.0, 300.0, 500.0),
    beta_grid=(0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
) -> dict:
    """Fit y(t) = A·exp(−(t/τ)^β) by grid search over (τ, β); linear amplitude A.

    Returns the best (A, τ, β), the RSS, and the classification.
    """
    if len(t) != len(y) or len(t) == 0:
        raise ValueError("t and y must be equal-length, non-empty")

    best = {"A": 0.0, "tau": None, "beta": None, "rss": float("inf")}
    for tau in tau_grid:
        for beta in beta_grid:
            xs = [math.exp(-((ti / tau) ** beta)) for ti in t]
            sxy = sum(xi * yi for xi, yi in zip(xs, y))
            sxx = sum(xi * xi for xi in xs)
            A = sxy / sxx if sxx > 0 else 0.0
            rss = sum((yi - A * xi) ** 2 for yi, xi in zip(y, xs))
            if rss < best["rss"]:
                best = {"A": A, "tau": tau, "beta": beta, "rss": rss}

    best["classification"] = classify_relaxation(best["beta"])
    return best


def classify_relaxation(beta: float, tol: float = 0.05) -> str:
    """β ≈ 1 → single-exponential (DET-like); β < 1 → stretched (defect-like)."""
    if beta is None:
        return "unclassified"
    if beta >= 1.0 - tol:
        return "single_exponential_det_like"
    return "stretched_defect_like"
