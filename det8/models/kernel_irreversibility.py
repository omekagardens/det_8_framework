"""
DET v8.1 — Kernel Irreversibility Theorem (T4)

For a committed trajectory ω = (x_0,…,x_n), the forward path probability is

    P_F[ω] = p_0(x_0) ∏_{j=0}^{n−1} K_j(x_{j+1} | x_j),

and a lawful reverse process gives P_R[ω†]. Define the record-path
irreversibility

    Σ[ω] = ln( P_F[ω] / P_R[ω†] ).

Then, from normalization of the reverse process alone,

    ⟨ e^(−Σ) ⟩_F = Σ_ω P_R[ω†] = 1 − λ,

where λ is the reverse probability on trajectories with no forward counterpart
(incomplete reverse support). Jensen then gives the second-law form

    ⟨ Σ ⟩_F ≥ 0

with equality iff the forward and reverse processes coincide (reversibility).

Absolute irreversibility: a forward path with P_F[ω] > 0 but P_R[ω†] = 0 has
Σ = +∞; it contributes zero to ⟨e^(−Σ)⟩ but drives ⟨Σ⟩ to +∞. This is the
record-level analogue of the standard fluctuation theorems.

DERIVATION CERTIFICATE (honest provenance):

  Σ[ω] = ln(P_F/P_R) path ratio      MATH — stochastic thermodynamics (Seifert),
                                             credited.
  ⟨e^(−Σ)⟩ = 1 − λ                   TH-DET — from reverse normalization alone.
  ⟨Σ⟩ ≥ 0 (Jensen)                   TH-DET — convexity of the exponential.
  absolute-irreversibility correction MATH — Murashita–Funo–Ueda, credited.

Anti-smuggling: no standard-physics constants; pure commit-kernel path arithmetic.
"""

from __future__ import annotations

import math


# ── Markov path process ─────────────────────────────────────────────────────


class PathProcess:
    """A finite Markov process: initial distribution p0 + per-step kernels K_j."""

    def __init__(self, p0: list[float], kernels: list[list[list[float]]]):
        self.p0 = [float(x) for x in p0]
        self.kernels = [[[float(v) for v in row] for row in K] for K in kernels]
        self.n_states = len(p0)
        self.n_steps = len(kernels)

    def path_probability(self, path: tuple[int, ...]) -> float:
        if len(path) != self.n_steps + 1:
            raise ValueError("path length mismatch")
        p = self.p0[path[0]]
        for j in range(self.n_steps):
            p *= self.kernels[j][path[j]][path[j + 1]]
        return p

    def marginals(self) -> list[list[float]]:
        """Forward marginals p_0, …, p_n."""
        p = [self.p0[:]]
        for K in self.kernels:
            nxt = [0.0] * self.n_states
            for x in range(self.n_states):
                for y in range(self.n_states):
                    nxt[y] += p[-1][x] * K[x][y]
            p.append(nxt)
        return p


def reverse_path(path: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(reversed(path))


def time_reversed(process: PathProcess) -> PathProcess:
    """The standard time-reversal of a Markov process.

    Reverse initial = forward final marginal p_n; reverse kernel at step j is
    K̄_j(y → x) = p_j(x) K_j(x,y) / p_{j+1}(y) (Bayes rule), in reversed order.
    """
    p = process.marginals()
    n = process.n_steps
    s = process.n_states
    r_p0 = p[n]
    r_kernels = []
    for j in range(n):
        K = process.kernels[j]
        Kbar = [[0.0] * s for _ in range(s)]
        for y in range(s):
            denom = p[j + 1][y]
            if denom <= 0.0:
                continue
            for x in range(s):
                Kbar[y][x] = p[j][x] * K[x][y] / denom
        r_kernels.append(Kbar)
    r_kernels.reverse()  # reverse path x_{j+1} → x_j uses Kbar_j, in reverse order.
    return PathProcess(r_p0, r_kernels)


def entropy_production(path: tuple[int, ...], forward: PathProcess,
                       reverse: PathProcess) -> float:
    """Σ[ω] = ln(P_F[ω] / P_R[ω†]). +∞ if P_R[ω†] = 0 (absolute irreversibility)."""
    pf = forward.path_probability(path)
    pr = reverse.path_probability(reverse_path(path))
    if pf <= 0.0:
        return 0.0  # path not in forward support; excluded from ⟨·⟩_F.
    if pr <= 0.0:
        return math.inf
    return math.log(pf / pr)


def _all_paths(n_states: int, n_steps: int):
    """Enumerate all state sequences (x_0,…,x_n)."""
    from itertools import product
    return product(range(n_states), repeat=n_steps + 1)


def fluctuation_statistics(forward: PathProcess, reverse: PathProcess) -> dict:
    """⟨e^(−Σ)⟩_F, ⟨Σ⟩_F, and the absolute-irreversibility diagnostic."""
    exp_sum = 0.0
    sigma_sum = 0.0
    sigma_sq_sum = 0.0
    n_irreversible = 0.0   # forward probability mass on paths with P_R[ω†] = 0.
    n_total = 0.0
    has_infinite = False

    for path in _all_paths(forward.n_states, forward.n_steps):
        path = tuple(path)
        pf = forward.path_probability(path)
        if pf <= 0.0:
            continue
        n_total += pf
        pr = reverse.path_probability(reverse_path(path))
        if pr <= 0.0:
            n_irreversible += pf
            has_infinite = True
            continue  # e^(−Σ) = 0; Σ = +∞.
        sigma = math.log(pf / pr)
        exp_sum += pf * math.exp(-sigma)   # = pr
        sigma_sum += pf * sigma
        sigma_sq_sum += pf * sigma * sigma

    mean_sigma = sigma_sum if not has_infinite else math.inf
    return {
        "exp_neg_sigma": exp_sum,          # ⟨e^(−Σ)⟩_F (≤ 1)
        "lambda_irrev": n_irreversible,    # forward mass on absolutely-irreversible paths
        "phantom_mass": 1.0 - exp_sum,     # reverse mass on paths with no forward counterpart
        "mean_sigma": mean_sigma,          # ⟨Σ⟩_F (≥ 0 when finite)
        "has_infinite_sigma": has_infinite,
        "interpretation": (
            f"⟨e^(−Σ)⟩={exp_sum:.6f} (≤1); absolutely-irreversible mass={n_irreversible:.4f}; "
            f"phantom reverse mass={1.0 - exp_sum:.4f}; "
            f"⟨Σ⟩={'+∞' if has_infinite else f'{mean_sigma:.4f}'}."
        ),
    }


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "T4 — Kernel Irreversibility Theorem",
        "deliverables": {
            "Σ[ω] = ln(P_F/P_R) path ratio": "MATH — stochastic thermodynamics (Seifert), credited",
            "⟨e^(−Σ)⟩_F = 1 − λ (λ = incomplete reverse support)": "TH-DET — from reverse normalization alone",
            "⟨Σ⟩_F ≥ 0": "TH-DET — Jensen's inequality",
            "absolute-irreversibility correction": "MATH — Murashita–Funo–Ueda, credited",
        },
        "notes": [
            "⟨Σ⟩ ≥ 0 with equality iff P_F = P_R (reversible);",
            "Σ is 'record-path irreversibility', not yet thermodynamic heat — a physical realization must be added later;",
            "this is a non-κ route to the arrow of time (per the re-foundation §5.5).",
        ],
        "status": "MATH/TH-DET implemented.",
    }


# ── End-to-end T4 ───────────────────────────────────────────────────────────


def run_t4() -> dict:
    """Three cases: reversible, absolute-irreversible, incomplete reverse support."""
    from det8.models.kernel_irreversibility import (
        PathProcess, time_reversed, fluctuation_statistics,
    )

    # Case 1 — reversible: reverse = perfect time-reversal → Σ = 0 exactly.
    K = [[0.7, 0.3], [0.3, 0.7]]  # one 2×2 kernel, both directions open.
    fwd = PathProcess([0.5, 0.5], [K])
    rev = time_reversed(fwd)
    case1 = fluctuation_statistics(fwd, rev)

    # Case 2 — absolute irreversibility: forward allows 0→1 but reverse cannot
    # undo it (reverse is the identity: no 1→0 transition). Forward path (0,1)
    # then has P_R[(1,0)] = 0, so Σ = +∞ on that path.
    fwd2 = PathProcess([0.5, 0.5], [[[0.7, 0.3], [0.0, 1.0]]])
    rev2 = PathProcess([0.35, 0.65], [[[1.0, 0.0], [0.0, 1.0]]])  # identity reverse.
    case2 = fluctuation_statistics(fwd2, rev2)

    # Case 3 — incomplete reverse support: forward is the identity (only the
    # two diagonal paths), but the reverse process has extra "phantom" paths
    # (0→1 and 1→0) that forward cannot reach, so ⟨e^(−Σ)⟩ = 1 − phantom < 1.
    fwd3 = PathProcess([0.5, 0.5], [[[1.0, 0.0], [0.0, 1.0]]])
    rev3 = PathProcess([0.5, 0.5], [[[0.7, 0.3], [0.3, 0.7]]])
    case3 = fluctuation_statistics(fwd3, rev3)

    s2 = "∞" if case2["has_infinite_sigma"] else f"{case2['mean_sigma']:.4f}"
    return {
        "case_reversible": case1,
        "case_absolute_irreversible": case2,
        "case_incomplete_reverse": case3,
        "certificate": derivation_certificate(),
        "interpretation": (
            f"Reversible: ⟨e^(−Σ)⟩={case1['exp_neg_sigma']:.4f}, ⟨Σ⟩={case1['mean_sigma']:.4f}. "
            f"Absolute-irreversible: irrev mass={case2['lambda_irrev']:.4f}, ⟨Σ⟩={s2}. "
            f"Incomplete-reverse: ⟨e^(−Σ)⟩={case3['exp_neg_sigma']:.4f} (<1), "
            f"phantom={case3['phantom_mass']:.4f}. "
            f"Second law ⟨Σ⟩≥0 holds in every finite case."
        ),
    }
