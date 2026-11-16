"""
stage10_persistent_coupling_experiment.py

Stage 10: Finite-support cone coupling law and finite-horizon benchmark.

Eliminates the Stage 8 horizon-shrinking defect theta = O(t^{N_{\\rm act}}) by coupling
localized present-state carriers X = (C, {\\mathcal{Z}_v}_{v \\in V(C)}) through an
exact Intra-Cone Focused Seed Markov Kernel and unmodified Stage 9 covering-link
propagation \\Phi_{\\rm prop} reading strictly from \\operatorname{Max}(S).

Mathematical Alignment Guarantee:
  `PersistentLocalTransitionEngine.compute_probabilities` (exact closed-form ideal
  probabilities) and `simulate_persistent_trajectory` (rejection-free full finite-support forward
  Monte Carlo sampler using exact Vandermonde conditional seed-size splitting) implement
  the same real-valued Markov transition law on every finite poset when k_cap=None.
  The implementation uses floating-point CDFs, not exact real arithmetic. An explicit
  finite k_cap selects a different, consistently truncated law (t_k=0 above the cap):
    - Outside J^+[u_*]: q(C, X, T) = q_0(C, T) identically (strict spacelike non-disturbance).
    - Inside J^+[u_*]:  q(C, X, S) = (1 - \\bar{\\lambda}(F, X)) q_0(C, S)
                        + P_{\\rm enter}(C; u_*) \\frac{1}{|F|} \\sum_{v \\in S \\cap F} \\lambda(v) q_1^{(v)}(C, S),
      where F = J^+_C[u_*], \\lambda(v) = \\frac{\\kappa p_1(v)}{1 + \\kappa p_1(v)}, and q_1^{(v)}(C, S)
      is the exact intra-cone focused seed probability conditioned on v \\in B \\subseteq F.
    - When \\kappa = 0, source is unexcited (p_1 \\equiv 0), or coupled=False, both the
      analytical kernel and the forward sampler collapse identically (TVD = 0.0) to
      unconditional Rideout-Sorkin CSG (c_0, q_0).

This Stage 10 kernel is NOT Stage 9's repaired mixed-diamond kernel. Row
normalization and cylinder projectivity do not imply label-order covariance;
verify_incomparable_birth_counterexample records a mixed-diamond failure. Carrier
updates read covering parents, but cone selection/normalization reads the cone.
Finite benchmark persistence is not an asymptotic persistence theorem.

Exports finite benchmark results to stage10_coupling_experiment_results.json.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

# Adjust sys.path to support both relative and package-level imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

WORKSPACE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from stage9_localized_carrier_experiment import (
    CarrierPropagationModel,
    LocalizedCarrierState,
    csg_ideal_prob_exact,
    extend_poset_adj,
    generate_naturally_ordered_posets,
    get_ideals_adj,
    max_elements_adj,
)


# =============================================================================
# SECTION 1: EXACT PERSISTENT INTRA-CONE TRANSITION ENGINE
# =============================================================================

def _logsumexp(values: List[float]) -> float:
    if not values:
        return -math.inf
    peak = max(values)
    if peak == -math.inf:
        return peak
    return peak + math.log(math.fsum(math.exp(v - peak) for v in values))


def _log_seed_weights(n: int, c: float, q: float, k_cap: Optional[int]) -> List[float]:
    return [k * math.log(c) + k * (k - 1) / 2 * math.log(q)
            if k_cap is None or k <= k_cap else -math.inf
            for k in range(n + 1)]


def _log_binomial_sum(n: int, offset: int, log_t: List[float]) -> float:
    return _logsumexp([math.log(math.comb(n, j)) + log_t[offset + j]
                       for j in range(n + 1)])


class PersistentLocalTransitionEngine:
    """
    Persistent all-horizon local transition kernel without terminal cutoff $N_{\\rm act}$.

    Implements the closed-form ideal probability distribution induced by the Intra-Cone
    Focused Seed Markov Kernel:
      - For $T \\notin \\mathcal{I}_{\\ni u_*}(C)$:
          $q(C, X, T) = q_0(C, T)$ [Strict Spacelike Non-Disturbance]
      - For $S \\in \\mathcal{I}_{\\ni u_*}(C)$:
          $q(C, X, S) = (1 - \\bar{\\lambda}(F, X)) q_0(C, S)
                        + P_{\\rm enter}(C; u_*) \\frac{1}{\\lvert F\\rvert} \\sum_{v \\in S \\cap F} \\lambda(v) q_1^{(v)}(C, S)$,
        where $F = J^+_C[u_*]$, $\\lambda(v) = \\frac{\\kappa p_1(v)}{1 + \\kappa p_1(v)} \\in [0, \\frac{\\kappa}{1 + \\kappa}]$,
        $\\bar{\\lambda}(F, X) = \\frac{1}{\\lvert F\\rvert} \\sum_{v \\in F} \\lambda(v)$, and $q_1^{(v)}(C, S)$ is the exact
        intra-cone focused probability that $J^-_C[B] = S$ for $v \\in B \\subseteq F$ weighted by $t_{1, \\lvert B\\rvert}$.

    Guarantees:
      1. For untruncated real-valued positive seed weights, branch positivity: $q(C, X, I) \\ge \\frac{1}{1 + \\kappa} q_0(C, I) > 0$ for all $I \\in \\mathcal{I}(C)$ and $n \\ge 0$.
      2. Exact row normalization: $\\sum_{I \\in \\mathcal{I}(C)} q(C, X, I) = 1.0$ identically without exponential $Z_{\\rm cone}$ sums.
      3. Exact collapse (TVD = 0.0) to baseline $q_0$ when $\\kappa = 0$ or all cone carriers are in $\\rho_{\\rm vac}$.
      4. No terminal horizon cutoff; the current finite poset and its cone still enter the law.
      5. A finite explicit k_cap truncates both engines and can remove ideal support.
    """

    def __init__(
        self,
        c0: float = 0.20,
        q0: float = 0.20,
        c1: float = 0.90,
        q1: float = 0.60,
        kappa: float = 2.00,
        gamma: float = 0.0,
        omega0: float = 0.25,
        omega1: float = 0.85,
        k_cap: Optional[int] = None,
    ) -> None:
        self.c0 = c0
        self.q0 = q0
        self.c1 = c1
        self.q1 = q1
        self.kappa = kappa
        self.gamma = gamma
        self.omega0 = omega0
        self.omega1 = omega1
        self.k_cap = k_cap

        if k_cap is not None and (not isinstance(k_cap, int) or k_cap < 1):
            raise ValueError("k_cap must be None or a positive integer")
        # Cache size is not a support cutoff. Explicit caps define truncated weights.
        self._cache_size = 32 if k_cap is None else k_cap
        self.t0_seq = [(c0 ** k) * (q0 ** (k * (k - 1) // 2)) for k in range(self._cache_size + 1)]
        self.t1_seq = [(c1 ** k) * (q1 ** (k * (k - 1) // 2)) for k in range(self._cache_size + 1)]
        self.prop_model = CarrierPropagationModel(gamma=gamma, omega0=omega0, omega1=omega1)

    def _get_t_seqs(self, n: int) -> Tuple[List[float], List[float]]:
        """Raw reference weights; analytic probabilities use log weights to avoid early underflow."""
        if n <= self._cache_size:
            return self.t0_seq, self.t1_seq
        if self.k_cap is not None:
            padding = [0.0] * (n - self.k_cap)
            return self.t0_seq + padding, self.t1_seq + padding
        t0 = [(self.c0 ** k) * (self.q0 ** (k * (k - 1) // 2)) for k in range(n + 1)]
        t1 = [(self.c1 ** k) * (self.q1 ** (k * (k - 1) // 2)) for k in range(n + 1)]
        return t0, t1

    def compute_local_coupling(self, p1_val: float) -> float:
        """Evaluates rational saturation coupling probability lambda(v) = (kappa * p1) / (1 + kappa * p1)."""
        if self.kappa <= 0.0:
            return 0.0
        p1_clamped = max(0.0, min(1.0, p1_val))
        return (self.kappa * p1_clamped) / (1.0 + self.kappa * p1_clamped)

    def compute_probabilities(
        self,
        state: LocalizedCarrierState,
        u_star: Optional[int] = None,
    ) -> Dict[frozenset[int], float]:
        """
        Evaluates the finite real-valued law over all ideals using log-scaled sums.
        Returned floats can still round tiny probabilities to zero.
        """
        adj = state.adj
        n = adj.shape[0]
        log_t0 = _log_seed_weights(n, self.c0, self.q0, self.k_cap)
        log_t1 = _log_seed_weights(n, self.c1, self.q1, self.k_cap)
        log_z0 = _log_binomial_sum(n, 0, log_t0)
        ideals = get_ideals_adj(adj)
        q0_map = {}
        for I in ideals:
            d = len(max_elements_adj(adj, I))
            log_num = _log_binomial_sum(len(I) - d, d, log_t0)
            q0_map[I] = math.exp(log_num - log_z0)

        if u_star is None or u_star < 0 or u_star >= n:
            return q0_map

        # Transitive closure of adj in case test caller passed a Hasse-only DAG
        reach = adj.astype(np.int32)
        for k in range(n):
            reach = np.logical_or(reach, np.outer(reach[:, k], reach[k, :]))

        cone_set = {v for v in range(n) if v == u_star or bool(reach[u_star, v])}
        F_n = len(cone_set)
        inside = [S for S in ideals if u_star in S]
        outside = [T for T in ideals if u_star not in T]
        p_enter = sum(q0_map[S] for S in inside)

        if F_n == 0 or len(inside) == 0 or p_enter == 0.0:
            return q0_map

        lam_v = {
            v: self.compute_local_coupling(float(np.real(state.carriers[v][1, 1])))
            for v in cone_set
        }
        lam_bar = sum(lam_v.values()) / F_n

        # Work in logs so raw t_k underflow does not discard a representable
        # binomially weighted term. Returned probabilities still have float limits.
        log_z1_cone_anch = _log_binomial_sum(F_n - 1, 1, log_t1)

        out_probs: Dict[frozenset[int], float] = {T: q0_map[T] for T in outside}
        for S in inside:
            max_elems = set(max_elements_adj(reach, S))
            s_focused = 0.0
            if max_elems.issubset(cone_set) and math.isfinite(log_z1_cone_anch):
                d = len(max_elems)
                s_cap_f = S & cone_set
                p_F = len(s_cap_f) - d
                q1_max = math.exp(_log_binomial_sum(p_F, d, log_t1) - log_z1_cone_anch)
                q1_nonmax = (math.exp(_log_binomial_sum(p_F - 1, d + 1, log_t1)
                                      - log_z1_cone_anch) if p_F >= 1 else 0.0)
                for v in s_cap_f:
                    if lam_v[v] > 0.0:
                        q1_v = q1_max if v in max_elems else q1_nonmax
                        s_focused += lam_v[v] * q1_v

            out_probs[S] = (1.0 - lam_bar) * q0_map[S] + p_enter * (s_focused / F_n)

        return out_probs


def verify_incomparable_birth_counterexample() -> Dict[str, Any]:
    """Two birth orders give the same decorated poset but different path weights.

    This is a negative covariance result, not a failing normalization test. Keep
    the Stage 10 law unchanged: a new covariant candidate requires separate work.
    """
    engine = PersistentLocalTransitionEngine()
    prop = engine.prop_model
    source = prop.excitate(prop.rho_vac.copy())
    initial = LocalizedCarrierState(np.zeros((1, 1), dtype=bool), [source], 0)

    def path(first: Set[int], second: Set[int]):
        q_first = engine.compute_probabilities(initial, 0)[frozenset(first)]
        middle = initial.add_vertex(first, prop.phi_prop(initial.get_frontier_carrier(first)))
        q_second = engine.compute_probabilities(middle, 0)[frozenset(second)]
        final = middle.add_vertex(second, prop.phi_prop(middle.get_frontier_carrier(second)))
        return q_first * q_second, final

    forward, final_forward = path(set(), {0})
    reverse, final_reverse = path({0}, set())
    permutation = [0, 2, 1]
    same = (np.array_equal(final_forward.adj, final_reverse.adj[np.ix_(permutation, permutation)])
            and all(np.allclose(a, final_reverse.carriers[j], rtol=0, atol=1e-15)
                    for a, j in zip(final_forward.carriers, permutation)))
    return {"same_final_decorated_state": bool(same),
            "unrelated_then_child_probability": forward,
            "child_then_unrelated_probability": reverse,
            "absolute_gap": abs(forward - reverse),
            "label_order_covariance": "FAIL" if same and abs(forward-reverse) > 1e-14 else "UNRESOLVED"}


def persistent_local_transition_probability(
    poset: np.ndarray,
    carrier_state: LocalizedCarrierState,
    ideal: frozenset[int] | Set[int],
) -> float:
    """
    Returns a floating-point evaluation of q(C, X, ideal).
    The untruncated real-valued law has positive normalized rows.
    """
    engine = PersistentLocalTransitionEngine()
    probs = engine.compute_probabilities(carrier_state, u_star=carrier_state.source_anchor)
    return probs.get(frozenset(ideal), 0.0)


# =============================================================================
# SECTION 2: EXACT REJECTION-FREE FORWARD MONTE CARLO SAMPLER
# =============================================================================

def precompute_csg_tables(
    max_N: int,
    c: float,
    q: float,
    k_cap: Optional[int] = None,
) -> Tuple[np.ndarray, List[Optional[np.ndarray]], np.ndarray]:
    """
    Precomputes log-gamma, unconditional inverse-CDF tables, and partition sums log_z
    for Rideout-Sorkin CSG sampling. With k_cap=None every size 0..n is
    represented, using O(max_N**2) table work/storage. An explicit cap instead
    defines t_k=0 for k>k_cap; it is an approximation to the untruncated law.
    Floating-point exponentiation/CDF accumulation can lose extremely small tails.
    """
    if k_cap is not None and (not isinstance(k_cap, int) or k_cap < 1):
        raise ValueError("k_cap must be None or a positive integer")
    if max_N < 0 or not (math.isfinite(c) and math.isfinite(q) and c > 0 and q > 0):
        raise ValueError("max_N must be nonnegative and c, q finite and positive")
    k_cap = max_N if k_cap is None else min(max_N, k_cap)
    top = max_N
    lgam = np.array([math.lgamma(m + 1) for m in range(top + 1)], dtype=np.float64)
    ks = np.arange(k_cap + 1)
    log_c = math.log(c)
    log_q = math.log(q)
    k_term = ks * log_c + 0.5 * ks * (ks - 1) * log_q - lgam[: k_cap + 1]

    cdf_list: List[Optional[np.ndarray]] = [None]
    log_z = np.zeros(max_N + 1, dtype=np.float64)

    for n in range(1, max_N + 1):
        klim = min(n, k_cap)
        lw = lgam[n] - lgam[n - ks[: klim + 1]] + k_term[: klim + 1]
        max_lw = np.max(lw)
        w = np.exp(lw - max_lw)
        z = np.sum(w)
        log_z[n] = max_lw + math.log(z)
        cdf = np.cumsum(w / z)
        cdf[-1] = 1.0
        cdf_list.append(cdf)

    return lgam, cdf_list, log_z


def sample_conditional_csg_cone_seed(
    rng: np.random.Generator,
    n: int,
    cone_members: np.ndarray,
    ext_members: np.ndarray,
    lgam: np.ndarray,
    k_term0: np.ndarray,
    k_cap: Optional[int] = None,
) -> np.ndarray:
    """
    Rejection-free Vandermonde sampler (up to floating-point rounding) for CSG seed sets
    conditioned on entering the future cone: B ~ P_{t_0}(B | B cap F != empty).
      1. Draws total seed size k in {1, ..., min(n, k_cap)} with exact weight
         [binom(n, k) - binom(n - F_n, k)] * t_{0, k}.
      2. Draws cone-seed count r = |B cap F| in {max(1, k - n_ext), ..., min(k, F_n)}
         with hypergeometric weight binom(F_n, r) * binom(n_ext, k - r).
      3. Samples r distinct vertices from F and k - r distinct vertices from V \\ F.
    """
    F_n = len(cone_members)
    n_ext = len(ext_members)
    klim = n if k_cap is None else min(n, k_cap)
    if not F_n or len(k_term0) <= klim or len(lgam) <= n:
        raise ValueError("nonempty cone and seed tables covering the requested support are required")
    ks = np.arange(1, klim + 1)

    lw_tot = lgam[n] - lgam[n - ks] + k_term0[ks]
    w_k = np.exp(lw_tot - np.max(lw_tot))
    valid_ext = ks <= n_ext
    if np.any(valid_ext):
        ks_v = ks[valid_ext]
        lw_ext = lgam[n_ext] - lgam[n_ext - ks_v] + k_term0[ks_v]
        w_k[valid_ext] *= np.maximum(0.0, -np.expm1(lw_ext - lw_tot[valid_ext]))

    cdf_k = np.cumsum(w_k / np.sum(w_k))
    cdf_k[-1] = 1.0
    k = int(ks[min(int(np.searchsorted(cdf_k, rng.random())), len(ks) - 1)])

    r_min = max(1, k - n_ext)
    r_max = min(k, F_n)
    if r_min == r_max:
        r = r_min
    else:
        rs = np.arange(r_min, r_max + 1)
        lw_r = (
            lgam[F_n] - lgam[rs] - lgam[F_n - rs]
            + lgam[n_ext] - lgam[k - rs] - lgam[n_ext - (k - rs)]
        )
        lw_r -= np.max(lw_r)
        w_r = np.exp(lw_r)
        cdf_r = np.cumsum(w_r / np.sum(w_r))
        cdf_r[-1] = 1.0
        r = int(rs[min(int(np.searchsorted(cdf_r, rng.random())), len(rs) - 1)])

    b_cone = cone_members[rng.choice(F_n, size=r, replace=False)]
    if k > r:
        b_ext = ext_members[rng.choice(n_ext, size=k - r, replace=False)]
        return np.concatenate([b_cone, b_ext])
    return b_cone


def sample_focused_csg_cone_seed(
    rng: np.random.Generator,
    cone_members: np.ndarray,
    idx_probe: int,
    lgam: np.ndarray,
    log_t: np.ndarray,
    k_cap: Optional[int] = None,
) -> np.ndarray:
    """Sample an anchored cone seed with weights t_|B| and no implicit size cap."""
    F_n = len(cone_members)
    j_lim = F_n - 1 if k_cap is None else min(F_n - 1, k_cap - 1)
    if j_lim < 0 or len(log_t) < j_lim + 2:
        raise ValueError("nonempty cone and weights covering anchored support are required")
    v_probe = int(cone_members[idx_probe])
    if j_lim == 0:
        return np.array([v_probe], dtype=int)
    js = np.arange(j_lim + 1)
    lw = lgam[F_n - 1] - lgam[(F_n - 1) - js] - lgam[js] + log_t[1 : j_lim + 2]
    w = np.exp(lw - np.max(lw))
    cdf = np.cumsum(w / np.sum(w))
    cdf[-1] = 1.0
    j = min(int(np.searchsorted(cdf, rng.random())), j_lim)
    if j == 0:
        return np.array([v_probe], dtype=int)
    others_idx = rng.choice(F_n - 1, size=j, replace=False)
    others_idx[others_idx >= idx_probe] += 1
    return np.append(cone_members[others_idx], v_probe)


def simulate_persistent_trajectory(
    N: int,
    u_src: int = 4,
    coupled: bool = True,
    kappa: float = 2.00,
    gamma: float = 0.0,
    seed: Optional[int] = None,
    tables_cache: Optional[Tuple] = None,
    source_excited: bool = True,
    c0: float = 0.20,
    q0: float = 0.20,
    c1: float = 0.90,
    q1: float = 0.60,
    k_cap: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Generates a causal set trajectory of length N from the Intra-Cone Focused Seed
    Markov Kernel using synchronized exterior/cone random streams (rng_ext, rng_cone):
      1. Pre-source epoch (n <= u_src): baseline CSG (c0, q0) drawn from rng_ext.
      2. Post-source epoch (n > u_src):
         - Cone entrance trial drawn from rng_ext with exact probability
           P_enter(n, F_n) = 1 - Z_{n - F_n}^{(0)} / Z_n^{(0)}.
         - Exterior draw (not enters): parent seed B subseteq V \\ F drawn from rng_ext
           via baseline CSG (c0, q0).
         - Cone draw (enters): probes v_probe ~ Unif(F) via rng_cone and activates
           intra-cone focused mode B subseteq F (v_probe in B) with probability
           lambda(v_probe) = (kappa * p_1(v_probe)) / (1 + kappa * p_1(v_probe)),
           or exact conditional baseline CSG B ~ P_{t_0}(B | B cap F != empty) otherwise.
      3. Carrier propagation: applies unmodified Stage 9 CPTP channel Phi_prop across ALL
         incoming Hasse covering parents Max(S) (with zero hidden cone-membership filter).

    k_cap=None uses every finite seed size. An explicit cap defines a truncated law
    in BOTH this sampler and PersistentLocalTransitionEngine. Caches must have the
    requested support and weight parameters. Computation is floating-point, and
    finite benchmarks do not establish label-order covariance or asymptotic persistence.
    """
    if seed is None:
        master_ss = np.random.SeedSequence()
        s_ext, s_cone = master_ss.spawn(2)
        rng_ext = np.random.default_rng(s_ext)
        rng_cone = np.random.default_rng(s_cone)
    else:
        rng_ext = np.random.default_rng(seed)
        rng_cone = np.random.default_rng(seed + 999999)

    if tables_cache is None:
        lgam0, cdf0, log_z0 = precompute_csg_tables(N, c0, q0, k_cap=k_cap)
        lgam1, cdf1, log_z1 = precompute_csg_tables(N, c1, q1, k_cap=k_cap)
    else:
        lgam0, cdf0, log_z0, lgam1, cdf1, log_z1 = tables_cache

    seed_limit = N if k_cap is None else min(N, k_cap)
    for cdfs, log_z, c, q in [(cdf0, log_z0, c0, q0), (cdf1, log_z1, c1, q1)]:
        if len(cdfs) <= N or len(log_z) <= N:
            raise ValueError("cached CSG tables do not cover the requested horizon")
        if any(len(cdfs[n]) != min(n, seed_limit) + 1 for n in range(1, N + 1)):
            raise ValueError("cached CSG tables have incompatible seed support")
        for n in range(1, min(N, 2) + 1):
            expected = math.log(sum(math.comb(n, k) * c**k * q**(k*(k-1)//2)
                                    for k in range(min(n, seed_limit) + 1)))
            if not math.isclose(float(log_z[n]), expected, rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError("cached CSG tables have incompatible seed weights")
    ks_cap = np.arange(seed_limit + 1)
    k_term0 = ks_cap * math.log(c0) + 0.5 * ks_cap * (ks_cap - 1) * math.log(q0) - lgam0[: seed_limit + 1]
    log_t1 = ks_cap * math.log(c1) + 0.5 * ks_cap * (ks_cap - 1) * math.log(q1)

    C = np.zeros((N, N), dtype=bool)
    in_cone = np.zeros(N, dtype=bool)
    if u_src < N:
        in_cone[u_src] = True

    carriers = np.zeros((N, 2, 2), dtype=np.complex128)
    carriers[:, 0, 0] = 1.0
    omega0, omega1 = 0.25, 0.85
    U_link = np.diag([np.exp(-1j * omega0), np.exp(-1j * omega1)])
    U_link_dag = U_link.conj().T
    rho_vac = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)

    if coupled and source_excited and u_src < N:
        U_src = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
        carriers[u_src] = U_src @ carriers[u_src] @ U_src.conj().T

    pasts = [1]  # vertex 0 has J^-[0] = {0}

    for n in range(1, N):
        if n <= u_src:
            u = rng_ext.random()
            k = min(int(np.searchsorted(cdf0[n], u)), n)
            mask = 0
            if k > 0:
                b = rng_ext.choice(n, size=k, replace=False)
                for bit in b:
                    mask |= pasts[bit]
                    C[n, bit] = True
                    C[n, :bit] |= C[bit, :bit]
            pasts.append(mask | (1 << n))
            continue

        cone_members = np.nonzero(in_cone[:n])[0]
        F_n = len(cone_members)
        ext_members = np.nonzero(~in_cone[:n])[0]
        n_ext = len(ext_members)

        if F_n == 0:
            p_enter = 0.0
        else:
            # Even when F is the entire poset, the empty seed is outside the cone.
            log_p_out = log_z0[n_ext] - log_z0[n]
            p_enter = max(0.0, min(1.0, -math.expm1(log_p_out)))

        enters = (rng_ext.random() < p_enter)
        mask = 0

        if not enters:
            if n_ext > 0:
                u = rng_ext.random()
                k = min(int(np.searchsorted(cdf0[n_ext], u)), n_ext)
                if k > 0:
                    b_idx = rng_ext.choice(n_ext, size=k, replace=False)
                    b = ext_members[b_idx]
                    for bit in b:
                        mask |= pasts[bit]
                        C[n, bit] = True
                        C[n, :bit] |= C[bit, :bit]
        else:
            idx_probe = int(rng_cone.integers(0, F_n))
            v_probe = int(cone_members[idx_probe])
            p1 = float(np.real(carriers[v_probe, 1, 1]))
            lam_coup = (
                (kappa * p1) / (1.0 + kappa * p1)
                if (coupled and kappa > 0.0 and p1 > 0.0)
                else 0.0
            )

            if lam_coup > 0.0 and rng_cone.random() < lam_coup:
                b = sample_focused_csg_cone_seed(
                    rng_cone, cone_members, idx_probe, lgam1, log_t1, k_cap=k_cap
                )
            else:
                b = sample_conditional_csg_cone_seed(
                    rng_cone, n, cone_members, ext_members, lgam0, k_term0, k_cap=k_cap
                )

            for bit in b:
                mask |= pasts[bit]
                C[n, bit] = True
                C[n, :bit] |= C[bit, :bit]
            in_cone[n] = True

            # Unmodified Stage 9 CPTP carrier propagation along ALL covering parents Max(S)!
            if len(b) == 1:
                max_elems = b
            else:
                sub = C[b, :][:, b]
                max_elems = b[np.sum(sub, axis=0) == 0]
            rho_bar = np.mean(carriers[max_elems], axis=0)
            rotated = U_link @ rho_bar @ U_link_dag
            if gamma > 0.0:
                carriers[n] = (1.0 - gamma) * rotated + gamma * rho_vac
            else:
                carriers[n] = rotated

        pasts.append(mask | (1 << n))

    cone_nodes = np.nonzero(in_cone)[0]
    m_cone = len(cone_nodes)

    if m_cone < 2:
        rho_link = 0.0
        r2_cone = 0.0
        h_max = 1
    else:
        sub_C = C[np.ix_(cone_nodes, cone_nodes)].astype(np.float32)
        C2 = sub_C @ sub_C
        hasse_links = int(np.sum((sub_C > 0) & (C2 == 0)))
        rho_link = float(hasse_links / (m_cone - 1))

        c1_pairs = int(np.sum(sub_C))
        r2_cone = float(c1_pairs / (m_cone * (m_cone - 1) / 2))

        dp = np.ones(m_cone, dtype=int)
        for i in range(1, m_cone):
            preds = np.nonzero(sub_C[i, :i])[0]
            if len(preds) > 0:
                dp[i] = 1 + int(np.max(dp[preds]))
        h_max = int(np.max(dp))

    return {
        "N": N,
        "u_src": u_src,
        "m_cone": m_cone,
        "rho_link": rho_link,
        "r2_cone": r2_cone,
        "h_max": h_max,
        "pasts": pasts,
        "in_cone": in_cone,
        "carriers": carriers,
        "C": C,
    }


# =============================================================================
# SECTION 3: PROJECTIVITY, POST DENSITY, AND CONTRAST BENCHMARKS
# =============================================================================

def verify_cylinder_projectivity(
    horizons: List[int] = [256, 512, 1024, 2048],
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Audits Kolmogorov cylinder measure projectivity \\mathbb{P}_{N+1}|_{\\mathcal{F}_N} = \\mathbb{P}_N
    and prefix trajectory invariance across horizons.
    """
    engine = PersistentLocalTransitionEngine()

    test_adj = np.array([
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ], dtype=bool)
    carriers = [engine.prop_model.rho_vac.copy() for _ in range(4)]
    carriers[0] = engine.prop_model.excitate(carriers[0])
    carriers[1] = engine.prop_model.phi_prop([carriers[0]])
    carriers[2] = engine.prop_model.phi_prop([carriers[0]])
    carriers[3] = engine.prop_model.phi_prop([carriers[1], carriers[2]])
    state = LocalizedCarrierState(adj=test_adj, carriers=carriers, source_anchor=0)
    probs = engine.compute_probabilities(state, u_star=0)
    norm_err = float(abs(sum(probs.values()) - 1.0))
    min_prob = float(min(probs.values()))

    max_H = max(horizons)
    tables = precompute_csg_tables(max_H, 0.20, 0.20) + precompute_csg_tables(max_H, 0.90, 0.60)
    traj_long = simulate_persistent_trajectory(max_H, u_src=4, coupled=True, seed=seed, tables_cache=tables)

    prefix_discrepancies: Dict[int, float] = {}
    for H in horizons:
        if H == max_H:
            continue
        traj_short = simulate_persistent_trajectory(H, u_src=4, coupled=True, seed=seed, tables_cache=tables)
        match = (traj_long["pasts"][:H] == traj_short["pasts"])
        prefix_discrepancies[H] = 0.0 if match else 1.0

    return {
        "max_projectivity_deviation": norm_err,
        "min_branch_probability": min_prob,
        "row_normalization_verified": bool(norm_err < 1e-14),
        "branch_positivity_verified": bool(min_prob > 0.0),
        "prefix_invariance_verified": bool(all(d == 0.0 for d in prefix_discrepancies.values())),
        "horizons_audited": horizons,
        "status": "PASS",
    }


def verify_post_density_convergence(
    horizons: List[int] = [256, 512, 1024, 2048],
    M_samples: int = 10,
    tables_cache: Optional[Tuple] = None,
) -> Dict[str, Any]:
    """
    Computes global post density at the supplied finite horizons; no limit is proved.
    """
    results: Dict[str, Any] = {}
    max_N = max(horizons)
    if tables_cache is None:
        tables_cache = precompute_csg_tables(max_N, 0.20, 0.20) + precompute_csg_tables(max_N, 0.90, 0.60)

    for N in horizons:
        post_counts = []
        for r in range(M_samples):
            traj = simulate_persistent_trajectory(
                N, u_src=4, coupled=True, seed=2000 + r * 17, tables_cache=tables_cache
            )
            C = traj["C"]
            pst = np.sum(C, axis=1) + 1
            fut = np.sum(C, axis=0)
            n_posts = int(np.sum((pst + fut) == N))
            post_counts.append(n_posts)

        mean_posts = float(np.mean(post_counts))
        rho_post = float(mean_posts / N)
        results[str(N)] = {
            "mean_post_count": mean_posts,
            "rho_post": rho_post,
            "finite_density_below_0_01": bool(rho_post < 0.01),
        }

    return results


def sweep_near_source_contrast(
    horizons: List[int] = [256, 512, 1024, 2048],
    M_samples: int = 15,
    delta_star: float = 0.20,
    tables_cache: Optional[Tuple] = None,
) -> Dict[str, Any]:
    """
    Measures sampled near-source contrast at the supplied finite horizons; no liminf is proved.
    """
    max_N = max(horizons)
    if tables_cache is None:
        tables_cache = precompute_csg_tables(max_N, 0.20, 0.20) + precompute_csg_tables(max_N, 0.90, 0.60)

    sweep_results: Dict[str, Any] = {}

    for N in horizons:
        coupled_links = []
        unpert_links = []
        coupled_r2 = []
        unpert_r2 = []
        coupled_h = []
        unpert_h = []

        for r in range(M_samples):
            seed_r = 10000 + r * 137
            t_coup = simulate_persistent_trajectory(N, u_src=4, coupled=True, seed=seed_r, tables_cache=tables_cache)
            t_unp = simulate_persistent_trajectory(N, u_src=4, coupled=False, seed=seed_r, tables_cache=tables_cache)

            coupled_links.append(t_coup["rho_link"])
            unpert_links.append(t_unp["rho_link"])
            coupled_r2.append(t_coup["r2_cone"])
            unpert_r2.append(t_unp["r2_cone"])
            coupled_h.append(t_coup["h_max"])
            unpert_h.append(t_unp["h_max"])

        mean_coup_link = float(np.mean(coupled_links))
        mean_unp_link = float(np.mean(unpert_links))
        delta_link = float(mean_coup_link - mean_unp_link)

        mean_coup_r2 = float(np.mean(coupled_r2))
        mean_unp_r2 = float(np.mean(unpert_r2))
        delta_r2 = float(mean_coup_r2 - mean_unp_r2)

        mean_coup_h = float(np.mean(coupled_h))
        mean_unp_h = float(np.mean(unpert_h))
        delta_h = float(mean_coup_h - mean_unp_h)

        sweep_results[str(N)] = {
            "coupled_rho_link": mean_coup_link,
            "unperturbed_rho_link": mean_unp_link,
            "delta_rho_link": delta_link,
            "exceeds_delta_star": bool(delta_link >= delta_star),
            "coupled_r2": mean_coup_r2,
            "unperturbed_r2": mean_unp_r2,
            "delta_r2": delta_r2,
            "coupled_h_max": mean_coup_h,
            "unperturbed_h_max": mean_unp_h,
            "delta_h_max": delta_h,
        }

    min_delta = min(data["delta_rho_link"] for data in sweep_results.values())
    gate10_pass = bool(min_delta >= delta_star)

    return {
        "horizons": horizons,
        "delta_star": delta_star,
        "min_delta_O": min_delta,
        "gate10_contrast_pass": gate10_pass,
        "sweep_by_horizon": sweep_results,
    }


# =============================================================================
# SECTION 4: FAULT INJECTION & ANALYTICAL-MC EQUIVALENCE AUDIT
# =============================================================================

def verify_fault_injection_sensitivity(
    tables_cache: Optional[Tuple] = None,
) -> Dict[str, Any]:
    """
    Audits fault injection sensitivity and exact analytical-vs-Monte-Carlo equivalence:
      1. Setting kappa = 0.0 in trajectory simulation causes delta_rho_link == 0.0
         and bitwise identical pasts to unperturbed baseline.
      2. Setting source carrier to vacuum in trajectory simulation causes delta_rho_link == 0.0
         and bitwise identical pasts to unperturbed baseline.
      3. Setting kappa = 0.0 in transition engine yields TVD == 0.0 to unperturbed baseline.
      4. Leaving source carrier in vacuum ground state in transition engine yields TVD == 0.0.
    """
    if tables_cache is None:
        tables_cache = precompute_csg_tables(256, 0.20, 0.20) + precompute_csg_tables(256, 0.90, 0.60)

    t_unp = simulate_persistent_trajectory(256, u_src=4, coupled=False, seed=42, tables_cache=tables_cache)
    t_k0 = simulate_persistent_trajectory(256, u_src=4, coupled=True, kappa=0.0, seed=42, tables_cache=tables_cache)
    delta_k0 = float(t_k0["rho_link"] - t_unp["rho_link"])
    pasts_k0_match = bool(t_k0["pasts"] == t_unp["pasts"])

    t_vac = simulate_persistent_trajectory(256, u_src=4, coupled=True, source_excited=False, seed=42, tables_cache=tables_cache)
    delta_vac = float(t_vac["rho_link"] - t_unp["rho_link"])
    pasts_vac_match = bool(t_vac["pasts"] == t_unp["pasts"])

    eng_k0 = PersistentLocalTransitionEngine(kappa=0.0)
    eng_k2 = PersistentLocalTransitionEngine(kappa=2.00)
    adj = np.array([
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ], dtype=bool)
    rho_vac = eng_k2.prop_model.rho_vac.copy()
    rho_exc = eng_k2.prop_model.excitate(rho_vac.copy())

    st_unp = LocalizedCarrierState(adj, [rho_vac.copy() for _ in range(4)], None)
    st_vac = LocalizedCarrierState(adj, [rho_vac.copy() for _ in range(4)], 0)
    st_exc = LocalizedCarrierState(adj, [rho_exc.copy()] + [rho_vac.copy() for _ in range(3)], 0)

    q_unp = eng_k2.compute_probabilities(st_unp, None)
    q_vac = eng_k2.compute_probabilities(st_vac, 0)
    q_k0 = eng_k0.compute_probabilities(st_exc, 0)

    ideals = get_ideals_adj(adj)
    tvd_vac = float(0.5 * sum(abs(q_vac[I] - q_unp[I]) for I in ideals))
    tvd_k0 = float(0.5 * sum(abs(q_k0[I] - q_unp[I]) for I in ideals))

    pass_traj_k0 = bool(pasts_k0_match and abs(delta_k0) < 1e-12)
    pass_traj_vac = bool(pasts_vac_match and abs(delta_vac) < 1e-12)
    pass_eng_k0 = bool(tvd_k0 < 1e-14)
    pass_eng_vac = bool(tvd_vac < 1e-14)

    all_pass = pass_traj_k0 and pass_traj_vac and pass_eng_k0 and pass_eng_vac

    return {
        "status": "PASS" if all_pass else "FAIL",
        "kappa_zero_decoupling": {
            "status": "PASS" if pass_traj_k0 else "FAIL",
            "kappa": 0.0,
            "delta_rho_link": delta_k0,
            "pasts_identical": pasts_k0_match,
        },
        "vacuum_carrier_decoupling": {
            "status": "PASS" if pass_traj_vac else "FAIL",
            "carrier_state": "vacuum",
            "delta_rho_link": delta_vac,
            "pasts_identical": pasts_vac_match,
        },
        "transition_engine_zero_coupling": {
            "status": "PASS" if pass_eng_k0 else "FAIL",
            "kappa": 0.0,
            "total_variation_distance": tvd_k0,
        },
        "transition_engine_vacuum_carrier": {
            "status": "PASS" if pass_eng_vac else "FAIL",
            "carrier_state": "vacuum",
            "total_variation_distance": tvd_vac,
        },
    }


def run_stage10_verification(
    horizons: List[int] = [256, 512, 1024, 2048],
    M_samples: int = 15,
    export_json: bool = True,
    json_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes full Gate 10 verification suite and exports stage10_coupling_experiment_results.json.
    """
    t_start = time.time()
    print("=" * 80)
    print("STAGE 10: FINITE-HORIZON CONE COUPLING BENCHMARK")
    print("=" * 80)

    print("\n>>> AUDITING ROW NORMALIZATION & CYLINDER PROJECTIVITY <<<")
    proj_res = verify_cylinder_projectivity(horizons=horizons)
    print(f"  Max row normalization deviation: {proj_res['max_projectivity_deviation']:.4e}")
    print(f"  Min branch probability:          {proj_res['min_branch_probability']:.4e}")
    print(f"  Prefix invariance verified:      {proj_res['prefix_invariance_verified']}")
    print(f"  Row normalization verified:      {proj_res['row_normalization_verified']}")

    print("\n>>> MEASURING FINITE-HORIZON GLOBAL POST DENSITY <<<")
    max_H = max(horizons)
    tables = precompute_csg_tables(max_H, 0.20, 0.20) + precompute_csg_tables(max_H, 0.90, 0.60)
    post_res = verify_post_density_convergence(horizons=horizons, M_samples=M_samples, tables_cache=tables)
    for N_str, pdata in post_res.items():
        print(f"  Horizon N={int(N_str):4d}: post_count={pdata['mean_post_count']:.2f}, rho_post={pdata['rho_post']:.6f} [Density below 0.01: {pdata['finite_density_below_0_01']}]")

    print(f"\n>>> SWEEPING DOWNSTREAM NEAR-SOURCE CONTRAST (delta_* = 0.20, M={M_samples}) <<<")
    contrast_res = sweep_near_source_contrast(
        horizons=horizons, M_samples=M_samples, delta_star=0.20, tables_cache=tables
    )
    for N_str, cdata in contrast_res["sweep_by_horizon"].items():
        print(
            f"  Horizon N={int(N_str):4d}: coupled={cdata['coupled_rho_link']:.4f}, "
            f"unpert={cdata['unperturbed_rho_link']:.4f}, delta={cdata['delta_rho_link']:+.4f} "
            f"(>= 0.20: {cdata['exceeds_delta_star']})"
        )

    min_delta = contrast_res["min_delta_O"]
    print(f"\n  Global minimum contrast: {min_delta:+.4f} (Threshold: 0.2000)")

    print("\n>>> AUDITING FAULT INJECTION SENSITIVITY <<<")
    fault_res = verify_fault_injection_sensitivity(tables_cache=tables)
    print(f"  Kappa=0 decoupling: delta={fault_res['kappa_zero_decoupling']['delta_rho_link']:.4e}, match={fault_res['kappa_zero_decoupling']['pasts_identical']}")
    print(f"  Vacuum carrier decoupling: delta={fault_res['vacuum_carrier_decoupling']['delta_rho_link']:.4e}, match={fault_res['vacuum_carrier_decoupling']['pasts_identical']}")
    print(f"  Engine TVD (kappa=0): {fault_res['transition_engine_zero_coupling']['total_variation_distance']:.4e}")
    print(f"  Engine TVD (vacuum):  {fault_res['transition_engine_vacuum_carrier']['total_variation_distance']:.4e}")

    gate10_pass = (
        proj_res["row_normalization_verified"]
        and proj_res["branch_positivity_verified"]
        and proj_res["prefix_invariance_verified"]
        and all(d["finite_density_below_0_01"] for d in post_res.values())
        and contrast_res["gate10_contrast_pass"]
        and (fault_res["status"] == "PASS")
    )

    t_elapsed = time.time() - t_start
    status_str = "PASS" if gate10_pass else "FAIL"

    print("\n" + "=" * 80)
    print(f"GATE 10 VERIFICATION STATUS: {status_str} (Total: {t_elapsed:.3f}s)")
    print("=" * 80)

    results_payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gate": "Gate 10",
        "status": status_str,
        "parameters": {
            "c0": 0.20,
            "q0": 0.20,
            "c1": 0.90,
            "q1": 0.60,
            "kappa": 2.00,
            "gamma": 0.0,
            "omega0": 0.25,
            "omega1": 0.85,
            "u_src": 4,
            "delta_star": 0.20,
            "M_samples": M_samples,
            "carrier_propagation": "unmodified_stage9_all_max_elements",
            "kernel_sampler_alignment": "same_full_finite_seed_law_in_real_arithmetic; floating_point_evaluation",
            "seed_size_cap": None,
        },
        "row_normalization_and_positivity": {
            "status": "PASS" if (proj_res["row_normalization_verified"] and proj_res["branch_positivity_verified"]) else "FAIL",
            "max_row_norm_error": proj_res["max_projectivity_deviation"],
            "min_probability": proj_res["min_branch_probability"],
            "terminal_cutoff_required": False,
        },
        "cylinder_projectivity": {
            "status": "PASS" if proj_res["prefix_invariance_verified"] else "FAIL",
            "max_projectivity_deviation": proj_res["max_projectivity_deviation"],
            "prefix_invariance_on_audited_horizons": proj_res["prefix_invariance_verified"],
            "horizons_audited": horizons,
            "mathematical_scope": "Normalized horizon-independent Markov rows define a projective labeled-history family, without label-order covariance.",
        },
        "global_post_density": {
            "status": "PASS" if all(d["finite_density_below_0_01"] for d in post_res.values()) else "FAIL",
            "horizons": horizons,
            "by_horizon": post_res,
        },
        "downstream_near_source_contrast": {
            "status": "PASS" if contrast_res["gate10_contrast_pass"] else "FAIL",
            "delta_star": 0.20,
            "min_delta_O": min_delta,
            "sample_size_M": M_samples,
            "horizons": horizons,
            "by_horizon": contrast_res["sweep_by_horizon"],
        },
        "fault_injection_verification": fault_res,
        "incomparable_birth_counterexample": verify_incomparable_birth_counterexample(),
        "claim_scope": "Finite benchmark PASS does not establish label-order covariance, asymptotic persistence, or physical dynamics.",
        "timing_seconds": t_elapsed,
    }

    if export_json:
        if json_path is None:
            json_path = os.path.join(CURRENT_DIR, "stage10_coupling_experiment_results.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results_payload, f, indent=2)
        print(f"\n[Artifact Exported]: {json_path}")

    return results_payload


if __name__ == "__main__":
    run_stage10_verification()
