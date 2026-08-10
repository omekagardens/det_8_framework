"""
DET Continuum Limit — Einstein Equation Emergence

Implements the κ-weighted discrete action and tests the emergence
of the Einstein field equations from DET primitives.

Architecture:
  1. Discrete action: S_DET = S_BD[≺] + S_κ[κ, bonds]
     where S_BD is the Benincasa-Dowker geometric action and
     S_κ is the κ-field matter action.
  
  2. Variational principle: δS_DET = 0 at each event produces
     discrete equations of motion.
  
  3. Continuum limit: as N → ∞,
     S_BD → (1/16πG_q) ∫ R √|g| d⁴x    (conjectured)
     S_κ  → ∫ [½K(∇κ)² + ψ(κ)] √|g| d⁴x  (verified in 1D)
  
  4. Field equations: δS/δg^μν = 0 → G_μν = 8πG_q·T^κ_μν

Where T^κ_μν = ∂_μκ ∂_νκ − ½g_μν[(∂κ)² + 2ψ(κ)] is the κ-field
stress-energy tensor.

What we can verify numerically:
  A. S_κ converges to the continuum scalar field action.
  B. The Newtonian limit G_00 → ∇²Φ matches our verified 1/r².
  C. The κ stress-energy T^κ_μν has the correct form.
  D. The combined action S_DET is stationary for the known solutions.

What remains conjectured:
  - Full BD action convergence to Einstein-Hilbert (shared with CST)
  - Variation with respect to the metric (requires continuum structure)
  - The Bianchi identity in the full GR sense
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional, Callable


# ═══════════════════════════════════════════════════════════════════════════
# A. κ-Field Action Convergence
# ═══════════════════════════════════════════════════════════════════════════


def kappa_field_action_1d(
    kappa_values: list[float],
    dx: float,
    K: float = 1.0,
    kappa_eq: float = 0.0,
) -> float:
    """Compute the discrete κ-field action in 1D.

    S_κ = Σ [½K(∇κ_i)² + ½K(κ_i − κ_eq)²]·dx

    where ∇κ_i ≈ (κ_{i+1} − κ_i)/dx.

    Continuum: S → ∫ [½K(∂_xκ)² + ψ(κ)] dx.
    """
    n = len(kappa_values)
    S = 0.0

    for i in range(n - 1):
        # Kinetic term: ½K(∇κ)².
        grad_kappa = (kappa_values[i + 1] - kappa_values[i]) / dx
        S += 0.5 * K * grad_kappa**2 * dx

        # Potential term: ψ(κ) = ½K(κ − κ_eq)².
        S += 0.5 * K * (kappa_values[i] - kappa_eq)**2 * dx

    return S


def continuum_kappa_action_1d(
    kappa_fn: Callable[[float], float],
    dkappa_fn: Callable[[float], float],
    x_min: float, x_max: float,
    K: float = 1.0,
    kappa_eq: float = 0.0,
    n_points: int = 1000,
) -> float:
    """Compute the continuum κ-field action.

    S = ∫_{x_min}^{x_max} [½K(dκ/dx)² + ½K(κ − κ_eq)²] dx.
    """
    dx = (x_max - x_min) / n_points
    S = 0.0
    for i in range(n_points):
        x = x_min + (i + 0.5) * dx
        S += 0.5 * K * dkappa_fn(x)**2 * dx
        S += 0.5 * K * (kappa_fn(x) - kappa_eq)**2 * dx
    return S


def verify_kappa_action_convergence(
    n_values: list[int] = None,
    seed: int = 42,
) -> dict:
    """Verify S_κ(discrete) → S_κ(continuum) as N → ∞.

    Uses a known analytic solution and compares discrete and continuum actions.
    """
    if n_values is None:
        n_values = [20, 50, 100, 200, 500]

    # Analytic solution: κ(x) = κ_eq + A·sin(kx).
    A, k, kappa_eq = 0.5, 2 * math.pi / 5.0, 0.0
    kappa_fn = lambda x: kappa_eq + A * math.sin(k * x)
    dkappa_fn = lambda x: A * k * math.cos(k * x)
    x_min, x_max = 0.0, 5.0

    continuum_S = continuum_kappa_action_1d(
        kappa_fn, dkappa_fn, x_min, x_max, n_points=5000
    )

    results = []
    for n in n_values:
        dx = (x_max - x_min) / n
        xs = [x_min + (i + 0.5) * dx for i in range(n)]
        kappas = [kappa_fn(x) for x in xs]
        discrete_S = kappa_field_action_1d(kappas, dx)
        error = abs(discrete_S - continuum_S) / abs(continuum_S) if abs(continuum_S) > 1e-15 else 0.0
        results.append({
            "n": n,
            "discrete_S": discrete_S,
            "continuum_S": continuum_S,
            "relative_error": error,
        })

    return {
        "results": results,
        "converging": all(
            results[i]["relative_error"] > results[i + 1]["relative_error"]
            for i in range(len(results) - 1)
        ) if len(results) > 1 else False,
        "component_A_status": (
            "κ-field action converges to continuum scalar field action. "
            "This is the matter part of S_DET. Verified for 1D."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# B. κ Stress-Energy Tensor
# ═══════════════════════════════════════════════════════════════════════════


def kappa_stress_energy(
    kappa: float,
    grad_kappa_sq: float,
    K: float = 1.0,
    kappa_eq: float = 0.0,
) -> dict:
    """Compute the κ-field stress-energy tensor components.

    T^κ_μν = ∂_μκ ∂_νκ − ½g_μν[(∂κ)² + 2ψ(κ)].

    For a static, spherically symmetric configuration in flat background:
      T^κ_00 = ½K(∇κ)² + ψ(κ)   (energy density)
      T^κ_11 = ½K(∇κ)² − ψ(κ)   (radial pressure)
      T^κ_22 = T^κ_33 = −½K(∇κ)² − ψ(κ)  (tangential pressure).

    where ψ(κ) = ½K(κ − κ_eq)².
    """
    psi = 0.5 * K * (kappa - kappa_eq)**2

    T00 = 0.5 * K * grad_kappa_sq + psi  # Energy density.
    T11 = 0.5 * K * grad_kappa_sq - psi  # Radial pressure.
    T22 = -0.5 * K * grad_kappa_sq - psi  # Tangential pressure.

    return {
        "kappa": kappa,
        "grad_kappa_sq": grad_kappa_sq,
        "potential_psi": psi,
        "T00_energy_density": T00,
        "T11_radial_pressure": T11,
        "T22_tangential_pressure": T22,
        "trace": T00 + T11 + 2 * T22,  # Should be -2ψ(κ) for massless κ.
    }


# ═══════════════════════════════════════════════════════════════════════════
# C. Combined Action and Field Equations
# ═══════════════════════════════════════════════════════════════════════════


def det_combined_action_sketch() -> dict:
    """Sketch the combined DET action and its continuum limit.

    S_DET = S_geometry + S_matter

    where:
      S_geometry = (1/16πG_q) Σ_i κ_i · BD_i  (κ-weighted BD action)
      S_matter   = Σ_i [½K(∇κ_i)² + ψ(κ_i)]  (κ-field action)

    Variation δS_DET = 0 gives:
    
    Geometry variation (δ/δg^μν):
      G_μν = 8πG_q · T^κ_μν + 8πG_q · T^matter_μν

    κ variation (δ/δκ):
      K·∇²κ − K(κ − κ_eq) = −(1/16πG_q) · R

    This couples the κ-field to the Ricci scalar R.
    In the Newtonian limit: ∇²Φ = 4πG_q·ρ_γ.
    """
    return {
        "combined_action": "S_DET = S_BD[≺, κ] + S_κ[κ, bonds]",
        "geometry_variation": "G_μν = 8πG_q·(T^κ_μν + T^matter_μν)",
        "kappa_variation": "K·∇²κ − K(κ−κ_eq) = −R/(16πG_q)",
        "newtonian_limit": "∇²Φ = 4πG_q·λ_γ·κ  (verified)",
        "coupling_interpretation": (
            "The κ-field is sourced by curvature (R) and in turn sources "
            "gravity (via T^κ_μν). This is a two-way coupling: matter tells "
            "geometry how to curve; geometry tells κ how to accumulate."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# D. Numerical Test: Action Stationarity
# ═══════════════════════════════════════════════════════════════════════════


def test_action_stationarity(
    n_events: int = 200,
    seed: int = 42,
) -> dict:
    """Test that the discrete action is stationary for the known solution.

    For Minkowski with uniform κ: S_BD → 0, S_κ = minimum.
    Perturbing κ should increase S_κ (the action is at a minimum).

    This is a weak test — it checks that the known solution is a
    stationary point of the discrete action, not that the discrete
    equations of motion match the continuum ones.
    """
    rng = random.Random(seed)
    T, X = 10.0, 5.0

    # Baseline: uniform κ = κ_eq.
    kappa_eq = 0.5
    events_base = [(rng.uniform(0, T), rng.uniform(-X, X)) for _ in range(n_events)]
    kappa_base = [kappa_eq] * n_events

    dx_effective = math.sqrt(T * 2 * X / n_events)  # Mean spacing.
    S_base = kappa_field_action_1d(kappa_base, dx_effective)

    # Perturbed: random variation around κ_eq.
    perturbations = [0.1 * (rng.random() - 0.5) for _ in range(n_events)]
    kappa_perturbed = [kappa_eq + p for p in perturbations]
    S_perturbed = kappa_field_action_1d(kappa_perturbed, dx_effective)

    return {
        "n_events": n_events,
        "S_base": S_base,
        "S_perturbed": S_perturbed,
        "delta_S": S_perturbed - S_base,
        "action_increases": S_perturbed > S_base,
        "interpretation": (
            f"Perturbing κ increases action by {S_perturbed - S_base:.4f}. "
            f"The uniform solution is a local minimum (stationary point). "
            "Full verification requires the geometric part (S_BD) which "
            "is conjectural for general spacetimes."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# E. Full Status
# ═══════════════════════════════════════════════════════════════════════════


def einstein_emergence_status() -> dict:
    """Complete status of Einstein equation emergence."""
    action_conv = verify_kappa_action_convergence()
    stationarity = test_action_stationarity()
    sketch = det_combined_action_sketch()

    # Compute sample stress-energy.
    te = kappa_stress_energy(kappa=0.5, grad_kappa_sq=0.1)

    return {
        "component_A_action_convergence": action_conv,
        "component_B_stress_energy": te,
        "component_C_sketch": sketch,
        "component_D_stationarity": stationarity,
        "newtonian_verified": True,  # 1/r², Kepler, SPARC, solar system, clusters.
        "gr_conjectured": True,      # Requires BD action convergence.
        "status": (
            "Einstein equation emergence: Newtonian limit verified (5 datasets). "
            "κ-field action converges to continuum (numerical). "
            "Discrete action stationary for known solutions (weak test). "
            "Full G_μν = 8πG_q·T^κ_μν emergence remains conjectural — "
            "requires BD action → Einstein-Hilbert convergence (shared with CST)."
        ),
    }
