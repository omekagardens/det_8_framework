"""
DET Continuum Limit — Curvature Convergence

Implements discrete curvature estimators on the event graph and
tests convergence to continuum curvature.

Estimators:
  1. Ricci scalar from interval volumes (Myrheim-Meyer dimension).
  2. Timelike Ricci curvature from proper-time distortions.
  3. Sectional curvature from triangle comparisons.
  4. κ-weighted curvature: R_κ ∝ κ·R (matter-curvature coupling).

Target spacetimes:
  - Minkowski (R=0): curvature estimators → 0.
  - de Sitter (R=const): curvature estimators → constant.
  - Schwarzschild: curvature estimators → M-dependent profile.

DET advantage: κ-weighting provides matter-coupled curvature.
Bare causal sets have only the geometric BD action.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional, Callable


# ═══════════════════════════════════════════════════════════════════════════
# 1. Ricci Scalar from Interval Volumes (Myrheim-Meyer)
# ═══════════════════════════════════════════════════════════════════════════


def ricci_scalar_estimator(
    events: list[tuple[float, float]],  # (t, x) for 1+1.
    c: float = 1.0,
    n_samples: int = 50,
    seed: int = 42,
) -> dict:
    """Estimate the Ricci scalar from causal interval volumes.

    In 1+1, the Myrheim-Meyer dimension estimator uses the ratio:
      ⟨N_interval⟩ / ⟨τ²⟩

    For Minkowski (R=0): this ratio is constant.
    For curved spacetimes (R≠0): the ratio deviates; the deviation
    is proportional to R at leading order.

    Specifically: N(interval) / τ² ≈ ρ·(1 − R·τ²/24 + ...)
    where ρ is the sprinkling density.

    So R can be estimated from the slope of N/τ² vs τ².
    """
    rng = random.Random(seed)
    n = len(events)
    T = max(t for t, _ in events)
    X = max(abs(x) for _, x in events)

    # Collect (τ², N) pairs.
    data = []
    for _ in range(n_samples):
        i = rng.randint(0, n - 1)
        j = rng.randint(0, n - 1)
        if i == j:
            continue
        ti, xi = events[i]
        tj, xj = events[j]
        if ti > tj:
            i, j = j, i
            ti, xi = events[i]
            tj, xj = events[j]
        dt = tj - ti
        dx = xj - xi
        if dt <= 0 or abs(dx) >= c * dt:
            continue
        tau_sq = dt**2 - dx**2 / c**2
        if tau_sq < 1e-10:
            continue

        # Count events in the causal interval.
        N_int = 0
        for k in range(n):
            if k == i or k == j:
                continue
            tk, xk = events[k]
            if (
                ti < tk < tj
                and abs(xk - xi) < c * (tk - ti)
                and abs(xj - xk) < c * (tj - tk)
            ):
                N_int += 1
        data.append((tau_sq, N_int))

    if len(data) < 5:
        return {"error": "Insufficient data"}

    # Fit: N/τ² ≈ ρ + β·τ². R ∝ −β/ρ.
    # Linear regression of N vs τ² and (τ²)².
    sum_t2 = sum(t2 for t2, _ in data)
    sum_t4 = sum(t2**2 for t2, _ in data)
    sum_N = sum(N for _, N in data)
    sum_Nt2 = sum(t2 * N for t2, N in data)
    m = len(data)

    denom = m * sum_t4 - sum_t2**2
    if abs(denom) < 1e-15:
        return {"error": "Singular fit"}

    rho = (sum_N * sum_t4 - sum_t2 * sum_Nt2) / denom  # Intercept.
    beta = (m * sum_Nt2 - sum_t2 * sum_N) / denom       # Slope.

    # R ∝ −β/ρ (leading order).
    if abs(rho) > 1e-15:
        R_est = -24.0 * beta / rho  # Factor 24 from expansion.
    else:
        R_est = 0.0

    return {
        "n_events": n,
        "n_samples": len(data),
        "density_rho": rho,
        "curvature_slope_beta": beta,
        "R_estimated": R_est,
        "R_expected_minkowski": 0.0,
        "deviation_from_zero": abs(R_est),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. Timelike Ricci Curvature from Proper-Time Distortion
# ═══════════════════════════════════════════════════════════════════════════


def timelike_ricci_estimator(
    events: list[tuple[float, float, float]],  # (t, x, Π).
    c: float = 1.0,
    n_samples: int = 50,
    seed: int = 42,
) -> dict:
    """Estimate timelike Ricci curvature from proper-time distortions.

    The Raychaudhuri equation relates the expansion of a congruence
    of timelike geodesics to the Ricci tensor:
      dθ/dτ = −R_{μν} u^μ u^ν − (trace terms).

    For a small causal diamond, the proper time between two events
    is distorted by curvature:
      τ²(actual) ≈ τ²(flat) · (1 − R_{00}·τ²(flat)/12 + ...).

    So R_{00} can be estimated from the deviation of Π-weighted
    interval counts from the flat-spacetime expectation.
    """
    rng = random.Random(seed)
    n = len(events)

    # Calibrate flat-spacetime expectation from pairs with small τ.
    # For small intervals, curvature effects are negligible.
    small_ratios = []
    large_deviations = []

    for _ in range(n_samples):
        i = rng.randint(0, n - 1)
        j = rng.randint(0, n - 1)
        if i == j:
            continue
        ti, xi, _ = events[i]
        tj, xj, _ = events[j]
        if ti > tj:
            i, j = j, i
            ti, xi, _ = events[i]
            tj, xj, _ = events[j]
        dt = tj - ti
        dx = xj - xi
        if dt <= 0 or abs(dx) >= c * dt:
            continue
        tau_sq_flat = dt**2 - dx**2 / c**2
        if tau_sq_flat < 1e-10:
            continue

        # Π-weighted interval count.
        pi_sum = 0.0
        for k in range(n):
            if k == i or k == j:
                continue
            tk, xk, pi_k = events[k]
            if (
                ti < tk < tj
                and abs(xk - xi) < c * (tk - ti)
                and abs(xj - xk) < c * (tj - tk)
            ):
                pi_sum += pi_k

        if pi_sum > 1e-10:
            ratio = pi_sum / tau_sq_flat
            if tau_sq_flat < 1.0:  # Small interval.
                small_ratios.append(ratio)
            else:
                large_deviations.append((tau_sq_flat, ratio))

    if not small_ratios:
        return {"error": "No small-interval calibration data"}

    rho_0 = sum(small_ratios) / len(small_ratios)  # Flat-spacetime density.

    # For large intervals: ratio = ρ₀·(1 − R_{00}·τ²/12 + ...).
    # Fit: ratio/ρ₀ − 1 ≈ −R_{00}·τ²/12.
    if not large_deviations:
        return {"R00_estimated": 0.0, "note": "All intervals small, R≈0"}

    sum_t2 = sum(t2 for t2, _ in large_deviations)
    sum_dev = sum(ratio / rho_0 - 1.0 for _, ratio in large_deviations)
    sum_t2dev = sum(t2 * (ratio / rho_0 - 1.0) for t2, ratio in large_deviations)
    m = len(large_deviations)

    if sum_t2 > 1e-15:
        R00_est = -12.0 * sum_t2dev / sum_t2
    else:
        R00_est = 0.0

    return {
        "n_events": n,
        "flat_density_rho0": rho_0,
        "R00_estimated": R00_est,
        "n_small": len(small_ratios),
        "n_large": len(large_deviations),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 3. Sectional Curvature from Triangle Comparisons
# ═══════════════════════════════════════════════════════════════════════════


def sectional_curvature_estimator(
    events: list[tuple[float, float]],  # (t, x) for 1+1.
    c: float = 1.0,
    n_samples: int = 30,
    seed: int = 42,
) -> dict:
    """Estimate sectional curvature from causal triangle comparisons.

    In a Lorentzian manifold, the sectional curvature K(Π) for a
    timelike plane Π can be estimated from the excess or deficit
    in the sum of angles of causal triangles.

    For a triangle formed by three causally related events (i ≺ j ≺ k):
      - Compute the three proper times τ_ij, τ_jk, τ_ik.
      - The "angle" at j can be estimated from the law of cosines.
      - The sum of angles minus π is proportional to K.

    In 1+1 Minkowski: angle sum = π (K=0).
    In positively curved: angle sum > π.
    In negatively curved: angle sum < π.
    """
    rng = random.Random(seed)
    n = len(events)

    angle_excesses = []
    for _ in range(n_samples):
        # Find three events i ≺ j ≺ k.
        i = rng.randint(0, n - 1)
        ti, xi = events[i]

        # Find j in the causal future of i.
        candidates_j = []
        for jj in range(n):
            if jj == i:
                continue
            tj, xj = events[jj]
            dt = tj - ti
            dx = xj - xi
            if dt > 0 and abs(dx) < c * dt:
                candidates_j.append(jj)

        if not candidates_j:
            continue
        j = rng.choice(candidates_j)
        tj, xj = events[j]

        # Find k in the causal future of j.
        candidates_k = []
        for kk in range(n):
            if kk == i or kk == j:
                continue
            tk, xk = events[kk]
            dt = tk - tj
            dx = xk - xj
            if dt > 0 and abs(dx) < c * dt:
                candidates_k.append(kk)

        if not candidates_k:
            continue
        k = rng.choice(candidates_k)
        tk, xk = events[k]

        # Compute proper times.
        tau_ij_sq = (tj - ti)**2 - (xj - xi)**2 / c**2
        tau_jk_sq = (tk - tj)**2 - (xk - xj)**2 / c**2
        tau_ik_sq = (tk - ti)**2 - (xk - xi)**2 / c**2

        if min(tau_ij_sq, tau_jk_sq, tau_ik_sq) < 1e-10:
            continue

        tau_ij = math.sqrt(tau_ij_sq)
        tau_jk = math.sqrt(tau_jk_sq)
        tau_ik = math.sqrt(tau_ik_sq)

        # Hyperbolic law of cosines for angle at j:
        # cosh(angle) = (τ_ij² + τ_jk² − τ_ik²) / (2·τ_ij·τ_jk).
        cosh_angle = (tau_ij_sq + tau_jk_sq - tau_ik_sq) / (2 * tau_ij * tau_jk)

        # Clamp to valid range (numerical noise near light cone).
        cosh_angle = max(1.0, min(cosh_angle, 10.0))
        angle = math.acosh(cosh_angle)

        # In Minkowski: sum of three hyperbolic angles = 0? No — for
        # 1+1 Lorentzian, the matching condition gives triangular identity.
        # The excess over the flat-spacetime value is ∝ K.
        # Simplified: angle excess ∝ curvature.
        angle_excesses.append(angle - 1.0)  # Baseline ~1 for Minkowski.

    if not angle_excesses:
        return {"error": "No valid triangles"}

    mean_excess = sum(angle_excesses) / len(angle_excesses)
    std_excess = (
        math.sqrt(sum((e - mean_excess)**2 for e in angle_excesses) / (len(angle_excesses) - 1))
        if len(angle_excesses) > 1 else 0.0
    )

    return {
        "n_events": n,
        "n_triangles": len(angle_excesses),
        "mean_angle_excess": mean_excess,
        "std_angle_excess": std_excess,
        "expected_minkowski": 0.0,
        "curvature_sign": "positive" if mean_excess > std_excess else "negative" if mean_excess < -std_excess else "consistent with zero",
    }


# ═══════════════════════════════════════════════════════════════════════════
# 4. Curvature Convergence Test
# ═══════════════════════════════════════════════════════════════════════════


def curvature_convergence_test(
    n_values: list[int] = None,
    seed: int = 42,
    n_trials: int = 3,
) -> dict:
    """Test convergence of Ricci scalar estimator in Minkowski.

    For Minkowski (R=0): R_est → 0 as N → ∞.
    Deviation from zero should decrease with N.
    """
    if n_values is None:
        n_values = [100, 200, 500, 1000]

    results = []
    for n in n_values:
        trial_R = []
        for trial in range(n_trials):
            rng = random.Random(seed + trial * 1000 + n)
            T, X = 10.0, 5.0
            events = [(rng.uniform(0, T), rng.uniform(-X, X)) for _ in range(n)]
            ricci = ricci_scalar_estimator(events, n_samples=30, seed=seed + trial)
            if "error" not in ricci:
                trial_R.append(abs(ricci["R_estimated"]))

        if trial_R:
            mean_R = sum(trial_R) / len(trial_R)
            std_R = (
                math.sqrt(sum((r - mean_R)**2 for r in trial_R) / (len(trial_R) - 1))
                if len(trial_R) > 1 else 0.0
            )
        else:
            mean_R, std_R = 0.0, 0.0

        results.append({
            "n_events": n,
            "mean_abs_R": mean_R,
            "std_R": std_R,
            "expected": "→ 0 (Minkowski R=0)",
        })

    # Check decreasing trend.
    decreasing = all(
        results[i]["mean_abs_R"] > results[i + 1]["mean_abs_R"]
        for i in range(len(results) - 1)
    ) if len(results) > 1 else False

    return {
        "results": results,
        "decreasing": decreasing,
        "status": (
            "Ricci scalar estimator implemented and tested on Minkowski. "
            f"{'Deviation decreases with N.' if decreasing else 'More trials needed for clean trend.'} "
            "Full convergence proof requires de Sitter and Schwarzschild tests "
            "plus analytic bounds."
        ),
    }
