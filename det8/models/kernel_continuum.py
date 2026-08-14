"""
DET v8.1 — Local Kernel Continuum Theorem (T5)

A local, conservative (normalized), exchange-symmetric graph kernel with weak
incremental updating forces the graph-Laplacian generator:

    Q = I + ε M,   M_ij = σ_ij (i≠j),   M_ii = −Σ_j σ_ij,

so the discrete update is

    p_i^{(n+1)} − p_i^{(n)} = ε Σ_j σ_ij (p_j − p_i).

In the continuum limit every coefficient arises from a MOMENT of the discrete
jump distribution:

    drift     v = Σ_j (x_j − x_i) σ_ij            (first moment)
    diffusion D = (1/2) Σ_j (x_j − x_i)² σ_ij      (half second moment)

giving the drift–diffusion equation ∂_t p = −v ∂_x p + D ∂²_x p, and the
spectral gap λ₂ of the Laplacian controls exponential relaxation to uniformity.

DERIVATION CERTIFICATE (honest provenance):

  Q = I + εM (weak update)              AX-DET — the incremental-update ansatz.
  normalization ⇒ zero row sums         TH-DET — Σ_j Q_ij = 1 ⇒ Σ_j M_ij = 0.
  exchange symmetry ⇒ symmetric M       TH-DET — detailed balance ⇒ M_ij = M_ji.
  ⇒ M = graph Laplacian                 TH-DET — locality + the two above.
  moments → drift/diffusion coefficients MATH  — Taylor expansion of the master
                                                  equation (Kramers–Moyal), credited.
  ∂_t p = −v ∂_x p + D ∂²_x p           MATH  — the continuum limit (credited).

  NOT derived here: the reversible wave-like (Schrödinger) limit — that requires
  the pair-kernel 𝔇 and the complex structure (T2/T6), still open.

Anti-smuggling: no standard-physics constants; the heat equation is NOT inserted
as a starting point — it is the *limit* of the kernel update.
"""

from __future__ import annotations

import math


# ── Generator from a local, symmetric, conservative kernel ─────────────────


def graph_laplacian_generator(Q: list[list[float]], eps: float) -> dict:
    """Extract M = (Q − I)/ε and verify it is a graph Laplacian.

    Returns M and the three structural checks (row-stochastic ⇒ zero row sums;
    exchange symmetry ⇒ symmetric; locality ⇒ nonnegative off-diagonal).
    """
    n = len(Q)
    M = [[(Q[i][j] - (1.0 if i == j else 0.0)) / eps for j in range(n)]
         for i in range(n)]

    zero_row_sums = all(abs(sum(M[i])) < 1e-9 for i in range(n))
    symmetric = all(abs(M[i][j] - M[j][i]) < 1e-9 for i in range(n) for j in range(n))
    nonneg_offdiag = all(M[i][j] >= -1e-12 for i in range(n) for j in range(n) if i != j)
    neg_diag = all(M[i][i] <= 1e-12 for i in range(n))

    return {
        "M": M,
        "zero_row_sums": zero_row_sums,
        "symmetric": symmetric,
        "nonneg_offdiag": nonneg_offdiag,
        "neg_diag": neg_diag,
        "is_laplacian": zero_row_sums and symmetric and nonneg_offdiag and neg_diag,
    }


def make_nearest_neighbor_kernel(n: int, w: float, eps: float,
                                 drift: float = 0.0) -> list[list[float]]:
    """A weak-update kernel Q = I + εM on a 1D chain (open boundary).

    M is the nearest-neighbor generator with symmetric weight w plus an
    asymmetric advection term `drift`: M[i][i+1] = w + drift, M[i][i−1] = w − drift.
    For drift = 0 the generator is the symmetric path-graph Laplacian; for
    drift > 0 it is drift–diffusion (Laplacian + antisymmetric advection).
    """
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        row_sum = 0.0
        if i > 0:
            M[i][i - 1] = w - drift
            row_sum += M[i][i - 1]
        if i < n - 1:
            M[i][i + 1] = w + drift
            row_sum += M[i][i + 1]
        M[i][i] = -row_sum
    Q = [[(M[i][j] * eps + (1.0 if i == j else 0.0)) for j in range(n)]
         for i in range(n)]
    return Q


# ── Continuum coefficients from kernel moments ─────────────────────────────


def continuum_coefficients(M: list[list[float]], positions: list[float]) -> dict:
    """drift v and diffusion D from the first and second moments of the
    OUTGOING jump distribution, evaluated at a BULK (interior) reference site.

    The generator entry M[i][j] is the incoming rate j → i, so the outgoing
    jump from i to j is M[j][i] (transpose). The boundary sites carry an
    O(1/n) finite-size correction that the continuum limit ignores.
    """
    n = len(M)
    i = n // 2  # interior reference site.
    v = sum((positions[j] - positions[i]) * M[j][i] for j in range(n) if j != i)
    d = 0.5 * sum((positions[j] - positions[i]) ** 2 * M[j][i]
                  for j in range(n) if j != i)
    return {"drift": v, "diffusion": d, "reference_site": i}


# ── Spectral gap ───────────────────────────────────────────────────────────


def _jacobi_eigh(A: list[list[float]], tol: float = 1e-12, max_iter: int = 500) -> list[float]:
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(max_iter):
        p, q, mx = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > mx:
                    mx, p, q = abs(a[i][j]), i, j
        if mx < tol:
            break
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        theta = 0.5 * math.atan2(2.0 * apq, aqq - app)
        c, s = math.cos(theta), math.sin(theta)
        for k in range(n):
            if k == p or k == q:
                continue
            akp, akq = a[k][p], a[k][q]
            a[k][p] = a[p][k] = c * akp - s * akq
            a[k][q] = a[q][k] = s * akp + c * akq
        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0
    return sorted((a[i][i] for i in range(n)), reverse=True)


def spectral_gap(M: list[list[float]]) -> float:
    """Magnitude of the smallest nonzero eigenvalue of the Laplacian (−M).

    Controls the exponential relaxation rate to the uniform (stationary)
    distribution.
    """
    n = len(M)
    L = [[-M[i][j] for j in range(n)] for i in range(n)]  # positive-semidefinite Laplacian.
    evals = _jacobi_eigh(L)          # descending (λ_max, …, λ_min).
    evals_asc = sorted(evals)        # ascending.
    # smallest nonzero eigenvalue (skip near-zero).
    for e in evals_asc:
        if abs(e) > 1e-10:
            return e
    return 0.0


# ── Discrete diffusion ──────────────────────────────────────────────────────


def diffuse(p0: list[float], M: list[list[float]], eps: float, n_steps: int) -> list[float]:
    """Iterate p^{(n+1)} = p^{(n)} + ε M p^{(n)}."""
    n = len(p0)
    p = p0[:]
    for _ in range(n_steps):
        Mp = [sum(M[i][j] * p[j] for j in range(n)) for i in range(n)]
        p = [p[i] + eps * Mp[i] for i in range(n)]
    return p


def _moments(p: list[float], positions: list[float]) -> dict:
    """mean and variance of a distribution over positions."""
    total = sum(p)
    mean = sum(positions[i] * p[i] for i in range(len(p))) / total
    var = sum((positions[i] - mean) ** 2 * p[i] for i in range(len(p))) / total
    return {"mean": mean, "variance": var}


def measure_relaxation_rate(M: list[list[float]], eps: float,
                            n_steps: int = 300) -> float:
    """Numerical spectral gap λ₂: the late-time decay rate of the deviation
    from the uniform stationary distribution.

    ‖δ_n‖² decays as e^{−2λ₂ ε n}, dominated by the slowest (second) eigenmode,
    so λ₂ = −slope/(2ε) from a late-time least-squares fit of log‖δ‖².
    """
    n = len(M)
    uniform = [1.0 / n] * n
    p = [0.0] * n
    p[0] = 1.0  # maximally far from uniform.
    norms = []
    for _ in range(n_steps):
        Mp = [sum(M[i][j] * p[j] for j in range(n)) for i in range(n)]
        p = [p[i] + eps * Mp[i] for i in range(n)]
        norms.append(sum((p[i] - uniform[i]) ** 2 for i in range(n)))

    start = int(0.6 * n_steps)
    xs = list(range(start, n_steps))
    ys = [math.log(max(norms[s], 1e-300)) for s in xs]
    N = len(xs)
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    den = N * sxx - sx * sx
    slope = (N * sxy - sx * sy) / den if abs(den) > 1e-15 else 0.0
    return -slope / (2.0 * eps)


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "T5 — Local Kernel Continuum Theorem",
        "deliverables": {
            "Q = I + εM weak-update ansatz": "AX-DET — incremental-update assumption",
            "normalization ⇒ zero row sums": "TH-DET",
            "exchange symmetry ⇒ symmetric M": "TH-DET",
            "⇒ M = graph Laplacian": "TH-DET — locality + the two above",
            "moments → drift/diffusion coefficients": "MATH — Kramers–Moyal / master-equation Taylor expansion (credited)",
            "∂_t p = −v ∂_x p + D ∂²_x p": "MATH — continuum limit (credited)",
        },
        "not_derived_here": [
            "the reversible wave-like (Schrödinger) limit — needs the pair-kernel 𝔇 + complex structure (T2/T6)",
        ],
        "status": "MATH/TH-DET implemented; the heat equation is a derived limit, not an input.",
    }


# ── End-to-end T5 ───────────────────────────────────────────────────────────


def run_t5(n: int = 61, w: float = 1.0, eps: float = 0.05,
           drift: float = 0.0, n_steps: int = 200, seed: int = 42) -> dict:
    """1D chain: verify (i) the generator is the Laplacian, (ii) the discrete
    update matches the drift–diffusion continuum solution (mean/variance),
    (iii) the spectral gap controls the relaxation rate."""
    positions = [float(i - n // 2) for i in range(n)]  # Δx = 1.

    Q = make_nearest_neighbor_kernel(n, w, eps, drift)
    gen = graph_laplacian_generator(Q, eps)
    M = gen["M"]

    coef = continuum_coefficients(M, positions)

    # Delta initial condition at the center; iterate.
    p0 = [0.0] * n
    p0[n // 2] = 1.0
    p_end = diffuse(p0, M, eps, n_steps)

    # Continuum prediction: mean = v·t, variance = 2D·t, t = n_steps·eps.
    t = n_steps * eps
    pred_mean = coef["drift"] * t
    pred_var = 2.0 * coef["diffusion"] * t
    emp = _moments(p_end, positions)

    # Spectral gap: on a small chain (n_small), where λ₂ is large enough to
    # measure, cross-check the late-time relaxation rate against the analytic
    # path-graph value.
    n_small = 21
    Qs = make_nearest_neighbor_kernel(n_small, w, eps, 0.0)
    Ms = graph_laplacian_generator(Qs, eps)["M"]
    gap_analytic = 2.0 * w * (1.0 - math.cos(math.pi / n_small))
    gap_measured = measure_relaxation_rate(Ms, eps, n_steps=4000)

    return {
        "n": n, "eps": eps, "n_steps": n_steps, "w": w, "drift": drift,
        "is_laplacian": gen["is_laplacian"],
        "continuum_coefficients": coef,
        "empirical_mean": emp["mean"],
        "predicted_mean": pred_mean,
        "empirical_variance": emp["variance"],
        "predicted_variance": pred_var,
        "spectral_gap_analytic": gap_analytic,
        "spectral_gap_measured": gap_measured,
        "certificate": derivation_certificate(),
        "interpretation": (
            f"Generator is Laplacian: {gen['is_laplacian']}. "
            f"Drift v={coef['drift']:.4f}, diffusion D={coef['diffusion']:.4f}. "
            f"Empirical mean={emp['mean']:.3f} (pred {pred_mean:.3f}); "
            f"empirical variance={emp['variance']:.3f} (pred {pred_var:.3f}). "
            f"Spectral gap λ₂: analytic={gap_analytic:.5f}, measured={gap_measured:.5f}."
        ),
    }
