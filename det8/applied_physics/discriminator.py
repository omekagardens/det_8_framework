"""Descriptive single, stretched and compressed exponential fit families.

A fitted stretch exponent labels a curve within a supplied search bank. It
neither identifies a material mechanism nor distinguishes DET from ordinary
relaxation models. Finite-grid fitting is not an ordinary BIC certificate.
"""

from __future__ import annotations

import math

from det8.applied_physics import adversarial as adv
from det8.models.validation import require_nonnegative_finite, require_positive_finite


def fit_kww(
    t, y,
    tau_grid=(1.0, 2.0, 5.0, 10.0, 20.0, 30.0, 50.0, 70.0, 100.0, 150.0, 200.0, 300.0, 500.0),
    beta_grid=(0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0),
) -> dict:
    """Minimize RSS for A exp(-(t/tau)^beta), with a fitted linear amplitude.

    The offset-free continuous family has three nominal mean parameters, or
    two when beta is fixed independently. A finite search does not establish
    those parameters' identifiability or regular asymptotic BIC assumptions.
    A zero represented shape norm refuses the entire bank. Tiny individual
    tail squares may round away in a representable total norm; this bounded
    guard does not certify floating-point accuracy or subnormal conditioning.
    """
    t, y = adv.paired_series(t, y)
    if any(ti < 0 for ti in t):
        raise ValueError("relaxation times must be nonnegative")
    taus = tuple(require_positive_finite(value, "tau") for value in tau_grid)
    betas = tuple(require_positive_finite(value, "beta") for value in beta_grid)
    if not taus or not betas:
        raise ValueError("tau and beta grids must be nonempty")
    best = None
    for tau in taus:
        for beta in betas:
            xs = [adv.kww_relaxation(ti, tau, beta) for ti in t]
            # hypot accumulates the aggregate norm without first squaring
            # each tiny tail term. RSS retains its stricter residual guard.
            shape_norm = math.hypot(*xs)
            sxx = require_nonnegative_finite(shape_norm * shape_norm, "relaxation shape norm")
            if sxx == 0:
                raise ValueError("relaxation shape norm underflows float representation")
            amplitude = sum(x * value for x, value in zip(xs, y)) / sxx
            rss = adv.rss_between([amplitude * x for x in xs], y)
            if best is None or rss < best["rss"]:
                best = {"A": amplitude, "tau": tau, "beta": beta, "rss": rss}
    if best is None:
        raise ValueError("relaxation bank has no representable fit")
    nominal = 3 if len(set(betas)) > 1 else 2
    degenerate = best["A"] == 0 or len(set(t)) < nominal
    if degenerate:
        best["grid_minimizer"] = {"tau": best["tau"], "beta": best["beta"]}
        best["tau"] = best["beta"] = None
    best.update({"classification": classify_relaxation(best["beta"]),
                 "fit_family": "offset_free_stretched_exponential" if len(set(betas)) > 1
                 else "offset_free_fixed_exponent_exponential",
                 "nominal_continuous_mean_parameters": nominal,
                 "identifiable_mean_parameters": None, "degenerate": degenerate,
                 "bic_available": False,
                 "bic_reason": "finite tau/beta bank; regular continuous likelihood fit not established",
                 "physical_mechanism_identified": False})
    return best


def classify_relaxation(beta, tol=0.05) -> str:
    """A descriptive exponent category; no statistical uncertainty or mechanism claim."""
    tol = require_nonnegative_finite(tol, "tol")
    if beta is None:
        return "unclassified"
    beta = require_positive_finite(beta, "beta")
    if abs(beta - 1) <= tol:
        return "single_exponential"
    return "stretched_exponential" if beta < 1 else "compressed_exponential"
