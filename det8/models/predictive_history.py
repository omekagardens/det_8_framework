"""
DET v8.1 — Predictive History Sufficiency (T1) and Matched-State Transport

Implements the T1 deliverables from docs/record_kernel_physics.md:

  1. Fisher–Rao operational metric  κ(h_a, h_b | S)  (§2.2)
  2. History-distinction test  H0: K_a = K_b  (§7.1)
  3. Latent-rank test  rank 0 / 1 / r>1 / nontransportable  (§2.1)
  4. Held-out transport test — κ inferred from probes A,B predicts probe C (§7.1)

κ is redefined here as a DERIVED predictive-history coordinate: the distance
between history-conditioned future kernels, NOT an assumed fraction of locked
degrees of freedom. No standard-physics constants are imported; the machinery
operates on raw outcome counts and the commit kernel K.

Anti-smuggling: this module uses only DET primitives (commit kernel K,
possibility set Ω, causal record R⁻, present state S). Classification of every
deliverable below is TH-DET (theorem implemented) or CORR (metric imported and
attributed — the Fisher/Bhattacharyya angle is standard information geometry).
"""

from __future__ import annotations

import math
import random


# ── 1. Fisher–Rao history distance (§2.2) ───────────────────────────────────


def fisher_rao_distance(K_a: list[float], K_b: list[float]) -> float:
    """Normalized Fisher–Rao / Bhattacharyya angle between two kernels.

    κ = (2/π) · arccos( Σ_x √(K_a(x)·K_b(x)) ),   in [0, 1].

    κ = 0  ⇒ identical future kernels (history carries no predictive weight).
    κ = 1  ⇒ disjoint future supports (maximal retained distinction).

    This is CORR: the Bhattacharyya angle is standard information geometry,
    monotone under stochastic coarse-graining.
    """
    n = len(K_a)
    if n != len(K_b) or n == 0:
        raise ValueError("kernels must be non-empty and over the same Ω")
    bc = sum(math.sqrt(K_a[i] * K_b[i]) for i in range(n))
    bc = max(0.0, min(1.0, bc))  # numerical guard
    return (2.0 / math.pi) * math.acos(bc)


# ── 2. History-distinction test  H0: K_a = K_b  (§7.1) ─────────────────────


def _g_statistic(obs: list[float], exp: list[float]) -> float:
    """Log-likelihood-ratio (G) statistic for a multinomial against expected."""
    g = 0.0
    for o, e in zip(obs, exp):
        if o > 0.0:
            g += o * math.log(o / e)
    return 2.0 * g


def test_history_distinction(
    K_a: list[float],
    K_b: list[float],
    n_a: int,
    n_b: int,
    n_bins: int | None = None,
) -> dict:
    """Does history change the future kernel?  H0: K_a = K_b.

    G-test against the pooled kernel. Returns whether H0 is rejected at the
    default 5% level (chi-square critical value via the Wilson–Hilferty
    approximation is avoided — the G value is compared to a documented
    threshold, and the honest verdict is reported as "distinct" only for large G).
    """
    n = len(K_a)
    n_total = n_a + n_b
    pooled = [(n_a * K_a[i] + n_b * K_b[i]) / n_total for i in range(n)]

    obs = [n_a * K_a[i] for i in range(n)]
    exp = [n_a * pooled[i] for i in range(n)]
    g = _g_statistic(obs, exp)

    # Degrees of freedom = (#outcomes − 1). χ²_{0.95}(df) for the tested df.
    df = (n_bins or n) - 1
    crit = {1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070}.get(
        df, 1.0 + 2.0 * math.sqrt(df / 2.0) * 1.96
    )
    distinct = g > crit
    return {
        "G": g,
        "df": df,
        "critical_value_0.05": crit,
        "distinct": distinct,
        "interpretation": (
            f"G = {g:.1f} vs χ²₀.₀₅({df}) = {crit:.1f} → histories "
            f"{'ARE' if distinct else 'are NOT'} predictively distinct "
            f"(κ > 0 {'supported' if distinct else 'unsupported'})."
        ),
    }


# ── 3. Latent-rank test (§2.1) ──────────────────────────────────────────────


def _jacobi_eigh(A: list[list[float]], tol: float = 1e-12, max_iter: int = 200) -> list[float]:
    """Eigenvalues of a small symmetric matrix via Jacobi rotations."""
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


def _singular_values(M: list[list[float]]) -> list[float]:
    """Singular values of a P×H matrix via the Gram matrix M·Mᵀ."""
    P = len(M)
    H = len(M[0]) if M else 0
    gram = [[0.0] * P for _ in range(P)]
    for i in range(P):
        for j in range(P):
            gram[i][j] = sum(M[i][k] * M[j][k] for k in range(H))
    evals = _jacobi_eigh(gram)
    return [math.sqrt(max(0.0, e)) for e in evals]


def latent_rank_test(
    residual_matrix: list[list[float]],
    rank_tol: float = 0.05,
) -> dict:
    """Determine the rank of the history-conditioned residual across probes.

    Rows = probes, columns = histories. The residual is (observed kernel −
    history-independent baseline). Classification (§2.1):

      rank 0  — present variables are state-complete; κ unnecessary.
      rank 1  — a scalar κ is supported (the milestone).
      rank r  — structural history is a vector/tensor (r components).
      nontransportable — each probe has its own nuisance history variable.

    This is TH-DET (rank test on the kernel residual).
    """
    P = len(residual_matrix)
    if P == 0:
        raise ValueError("empty residual matrix")
    sig = _singular_values(residual_matrix)
    total = math.sqrt(sum(s * s for s in sig))
    if total < 1e-14:
        return {"rank": 0, "verdict": "rank_0",
                "singular_values": sig,
                "interpretation": "Residual ≈ 0: present state is complete; κ unnecessary."}
    sig_norm = [s / total for s in sig]
    # Count effective components above the tolerance (relative to σ_1).
    r = sum(1 for s in sig_norm if s > rank_tol)
    if r <= 1:
        verdict, text = "rank_1", (
            "Residual is effectively rank-1: a single scalar κ (the history "
            "coordinate) explains every probe. Scalar κ is supported."
        )
    elif r < min(P, len(residual_matrix[0])):
        verdict, text = f"rank_{r}", (
            f"Residual is rank-{r}: structural history is a vector/tensor of "
            f"{r} components, not a scalar."
        )
    else:
        verdict, text = "nontransportable", (
            "Residual is full rank: each probe has its own nuisance history "
            "variable; no universal κ."
        )
    return {"rank": r, "verdict": verdict, "singular_values": sig_norm,
            "interpretation": text}


# ── 4. Held-out transport (§7.1) ────────────────────────────────────────────


def held_out_transport(
    train_residuals: list[list[float]],
    heldout_residual: list[float],
    tol: float = 0.10,
) -> dict:
    """Infer the scalar history from training probes, predict a held-out probe.

    The training probes each give a residual vector over histories; their shared
    rank-1 direction is the inferred κ mode. If that mode predicts the held-out
    probe's residual to within `tol` (relative), the history coordinate
    TRANSPORTS — the decisive test for a common history coordinate.
    """
    P = len(train_residuals)
    H = len(train_residuals[0]) if P else 0
    if P == 0 or H == 0:
        raise ValueError("empty training residuals")

    # Best rank-1 mode via the leading right singular vector (power iteration).
    # Work with the P×H matrix R; find the dominant left singular vector u,
    # then the shared history direction v ∝ Rᵀ u.
    u = [1.0 / math.sqrt(P)] * P
    for _ in range(200):
        v = [sum(train_residuals[i][j] * u[i] for i in range(P)) for j in range(H)]
        nv = math.sqrt(sum(x * x for x in v)) or 1.0
        v = [x / nv for x in v]
        u_new = [sum(train_residuals[i][j] * v[j] for j in range(H)) for i in range(P)]
        nu = math.sqrt(sum(x * x for x in u_new)) or 1.0
        u_new = [x / nu for x in u_new]
        if max(abs(u_new[i] - u[i]) for i in range(P)) < 1e-12:
            u = u_new
            break
        u = u_new

    # Project the held-out residual onto the shared history direction v.
    # The scalar history h_v ∈ {±} is inferred per-column; predict held-out as
    # a scalar multiple of v.
    proj_num = sum(heldout_residual[j] * v[j] for j in range(H))
    proj_den = sum(v[j] * v[j] for j in range(H))
    scalar = proj_num / proj_den if proj_den > 1e-15 else 0.0
    predicted = [scalar * v[j] for j in range(H)]
    # Relative prediction error (fraction of held-out residual norm).
    true_norm = math.sqrt(sum(heldout_residual[j] ** 2 for j in range(H))) or 1e-15
    err_norm = math.sqrt(
        sum((heldout_residual[j] - predicted[j]) ** 2 for j in range(H))
    )
    rel_err = err_norm / true_norm
    transports = rel_err < tol

    return {
        "rel_error": rel_err,
        "tol": tol,
        "transports": transports,
        "inferred_scalar": scalar,
        "interpretation": (
            f"Held-out probe predicted with relative error {rel_err:.2f} "
            f"(tol {tol}). The κ coordinate {'TRANSPORTS' if transports else 'does NOT transport'} "
            f"— {'a common history coordinate is supported.' if transports else 'each probe has its own history; no universal κ.'}"
        ),
    }


# ── 5. Synthetic matched-state dataset generator ───────────────────────────


def generate_history_dataset(
    n_histories: int = 4,
    n_outcomes: int = 3,
    n_probes: int = 3,
    n_samples: int = 2000,
    history_strength: float = 0.2,
    seed: int = 42,
    transportable: bool = True,
) -> dict:
    """Generate a matched-state, different-history dataset.

    Each history h ∈ {0, …, H−1} shifts the future kernel by a shared scalar
    direction; the present state S is identical across histories (matched).
    `n_probes` observations are independent projections of the same Ω. When
    `transportable` is True, every probe's history-conditioned residual is a
    linear function of the SAME scalar history (⇒ rank-1). When False, each
    probe gets its own independent random history-dependence (⇒ full rank).

    Returns {histories, kernels_by_history, probe_residuals, kappa}.
    """
    rng = random.Random(seed)

    if n_histories < 3:
        raise ValueError("need ≥ 3 histories so the rank test is non-trivial")

    # A hidden scalar history strength per history (the thing κ must recover).
    h_values = [(i / (n_histories - 1) - 0.5) * 2.0 * history_strength
                for i in range(n_histories)]

    # Base kernel + a shared history direction in outcome space.
    base = [1.0 / n_outcomes] * n_outcomes
    direction = [math.sin(2.0 * math.pi * (x + 0.25) / n_outcomes)
                 for x in range(n_outcomes)]

    def _kernel(h):
        w = [base[x] + h * direction[x] for x in range(n_outcomes)]
        w = [max(1e-4, wi) for wi in w]
        tot = sum(w)
        return [wi / tot for wi in w]

    kernels = {i: _kernel(h_values[i]) for i in range(n_histories)}

    # Each probe p is a distinct stochastic projection Ω → [0,1] (a Bernoulli
    # observable). Its residual is (P(y=1 | h) − probe mean over h).
    probe_residuals = []
    for p in range(n_probes):
        if transportable:
            # Linear in the shared scalar h → rank-1 across probes.
            proj = [rng.random() for _ in range(n_outcomes)]
            resp = [sum(kernels[h][x] * proj[x] for x in range(n_outcomes))
                    for h in range(n_histories)]
        else:
            # Probe-specific independent history dependence → full rank.
            resp = [rng.gauss(0.0, 1.0) for _ in range(n_histories)]
        mean_p = sum(resp) / len(resp)
        probe_residuals.append([r - mean_p for r in resp])

    # Ground-truth κ between history 0 and the last history.
    kappa = fisher_rao_distance(kernels[0], kernels[n_histories - 1])

    return {
        "n_histories": n_histories,
        "n_outcomes": n_outcomes,
        "n_probes": n_probes,
        "n_samples": n_samples,
        "transportable": transportable,
        "kernels": kernels,
        "baseline": base,
        "probe_residuals": probe_residuals,
        "kappa": kappa,
    }


# ── 6. End-to-end T1 ────────────────────────────────────────────────────────


def run_t1(
    transportable: bool = True,
    seed: int = 42,
) -> dict:
    """Run the full T1 pipeline on a synthetic matched-state dataset.

    Steps: (1) generate the dataset; (2) history-distinction test (H0: K_a=K_b);
    (3) latent-rank test; (4) held-out transport test (infer κ from the first
    two probes, predict the third).
    """
    d = generate_history_dataset(
        n_histories=4, n_outcomes=3, n_probes=3, n_samples=2000,
        transportable=transportable, seed=seed,
    )
    K0 = d["kernels"][0]
    K1 = d["kernels"][1]
    dist = test_history_distinction(K0, K1, n_a=d["n_samples"], n_b=d["n_samples"])
    rank = latent_rank_test(d["probe_residuals"])
    transport = held_out_transport(
        d["probe_residuals"][:2], d["probe_residuals"][2]
    )

    return {
        "kappa_ground_truth": d["kappa"],
        "history_distinction": dist,
        "latent_rank": rank,
        "held_out_transport": transport,
        "interpretation": (
            f"κ(fisher–rao) = {d['kappa']:.3f}. History distinct: {dist['distinct']}. "
            f"Latent rank: {rank['verdict']}. Transport: {transport['transports']}. "
            f"Scalar κ supported: {dist['distinct'] and rank['verdict'] == 'rank_1' and transport['transports']}."
        ),
    }
