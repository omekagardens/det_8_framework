"""
nested_regime_source_experiment.py

Stage 8 Comprehensive Mathematical & Computational Verification Suite:
  Pillar 1: Frozen Multi-Horizon & Multi-Observable Scale-Pattern Holdout Test
            (N in {512, 1024, 2048} + N = 4096 Log-Quadratic check; 5 interval
            structural observables across fixed-cardinality and horizon-growing
            windows; exact Future-Cone 1D Markov Chain Proposition).
  Pillar 2: Dynamical Nested-Regime Projection & Live Residual-to-Structure
            Coupling on X = (C, Z):
            - Theorem 2.1: Anchor Projection Pi_A diamond compatibility, omitted
              micro-interval non-Markovianity R_branch(m) = Z_{m+1} - 1, and exact
              Markov sufficiency of shadow-volume summary Z_geom.
            - Theorem 2.2 (2A): Arbitrary-horizon active off-diagonal residual law
              via exact subset-weight root martingale M_root (verified at N_act = 8
              and N_act = 12 across all 3,644 diamonds up to |C| = 4).
            - Theorem 2.3 (2B): All-horizon two-mode Log-Quadratic CPTP instrument
              with RECORD_PROCESS_CONTRACT evolve_residual source excitation and
              exact algebraic non-mixture separation against all static CSG mixtures.
  Pillar 3: Paired 3-Arm Source-Perturbation to Clock-Tick & Nested-Interval
            Focusing Bridge (matched committed prefix C_{n_0} at n_0 = 128 evolved
            to N = 512 and N = 1024 across M = 40 paired runs, tracking downstream
            clock ticks, matched-m interval reorganization, coarse-grained anchor
            comparability, and two-way Bayesian residual recoil / decoherence).
"""

import os
import sys
import math
import json
import time
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from poset_generator import generate_naturally_ordered_posets


# =============================================================================
# SECTION 1: MYRHEIM-MEYER, FIVE INTERVAL OBSERVABLES & VECTORIZED SAMPLERS
# =============================================================================

def myrheim_meyer_f(d):
    """
    Exact Myrheim-Meyer unordered-pair comparability expectation in a d-dimensional
    Minkowski Alexandrov causal diamond (d >= 1):
        f(d) = Gamma(d + 1) * Gamma(d / 2) / (2 * Gamma(3 * d / 2)).
    Satisfies f(1) = 1, f(2) = 1/2, f(3) = 8/35, f(4) = 1/10.
    """
    if d <= 1.0:
        return 1.0
    log_f = (
        math.lgamma(d + 1.0)
        + math.lgamma(0.5 * d)
        - math.log(2.0)
        - math.lgamma(1.5 * d)
    )
    return math.exp(log_f)


def invert_myrheim_meyer(r2, d_max=16.0):
    """Monotone inverse d_MM = f^{-1}(r2) on [f(d_max), 1] via 64-step bisection."""
    if r2 >= 1.0:
        return 1.0
    f_min = myrheim_meyer_f(d_max)
    if r2 <= f_min:
        return float(d_max)
    lo, hi = 1.0, float(d_max)
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        if myrheim_meyer_f(mid) > r2:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def compute_interval_five_observables(sub_C):
    """
    Computes the five structural observables on an open interval subposet I(u, v)
    represented by strictly lower-triangular {0,1} matrix sub_C of size m x m (m >= 2):
      1. r2:          Comparability fraction C_1(I) / binom(m, 2)
      2. ell_link:    Hasse link fraction N_0(I) / max(1, C_1(I))
      3. h_over_m:    Longest-chain proper-time density h(I) / m, where
                      h(I) = max{ L >= 1 : exists z_1 < ... < z_L in I }
      4. rho2:        Multi-step 3-chain ratio C_3(I) / max(1, C_2(I))
      5. wmin_over_m: Minimal-layer entry width fraction |Min(I)| / m
    Also returns d_mm = f^{-1}(r2) if r2 > 0 else d_max.
    """
    m = int(sub_C.shape[0])
    if m < 2:
        return {
            "m": m,
            "r2": 0.0,
            "d_mm": 16.0,
            "ell_link": 0.0,
            "h_over_m": 1.0 if m == 1 else 0.0,
            "rho2": 0.0,
            "wmin_over_m": 1.0 if m == 1 else 0.0,
        }

    row_sums = np.sum(sub_C, axis=1, dtype=np.int64)
    c1 = int(np.sum(row_sums))
    total_pairs = m * (m - 1) // 2
    r2 = float(c1) / float(total_pairs)
    d_mm = invert_myrheim_meyer(r2) if r2 > 0.0 else 16.0
    wmin_over_m = float(np.sum(row_sums == 0)) / float(m)

    if c1 == 0:
        return {
            "m": m,
            "r2": 0.0,
            "d_mm": 16.0,
            "ell_link": 0.0,
            "h_over_m": 1.0 / float(m),
            "rho2": 0.0,
            "wmin_over_m": 1.0,
        }

    # Exact integer C2 via int16/int32 matmul (avoids BLAS GCD thread overhead on small m <= 1024)
    if m <= 1024:
        sub_i = sub_C.astype(np.int16)
        C2 = (sub_i @ sub_i).astype(np.int64)
    else:
        sub_f = sub_C.astype(np.float32)
        C2 = np.rint(sub_f @ sub_f).astype(np.int64)
    n0 = int(np.sum((sub_C == 1) & (C2 == 0)))
    ell_link = float(n0) / float(max(1, c1))

    c2_sum = int(np.sum(C2))
    # Exact identity: 1^T (C2 @ sub_C) 1 == (1^T C2) @ (sub_C 1)
    c3_sum = int(np.dot(np.sum(C2, axis=0, dtype=np.int64), row_sums))
    rho2 = float(c3_sum) / float(max(1, c2_sum))

    # Longest directed chain vertex count h(I) in topological order
    dp = np.ones(m, dtype=np.int32)
    for i in range(1, m):
        if row_sums[i] > 0:
            preds = sub_C[i, :i] == 1
            dp[i] = 1 + int(np.max(dp[:i][preds]))
    h_over_m = float(np.max(dp)) / float(m)

    return {
        "m": m,
        "r2": r2,
        "d_mm": d_mm,
        "ell_link": ell_link,
        "h_over_m": h_over_m,
        "rho2": rho2,
        "wmin_over_m": wmin_over_m,
    }


def sample_minkowski_fast(dim, N, rng, geometry="diamond", slab_width=3.0):
    """
    Vectorized Poisson sprinkling of size N in d-dimensional Minkowski spacetime:
      - geometry='diamond': Alexandrov diamond between (0, 0, ...) and (1, 0, ...)
      - geometry='slab' (dim=2): Wide cylinder/slab [0, 1] x [0, slab_width]
    Returns strictly lower-triangular uint8 incidence matrix C of shape (N, N).
    """
    if geometry == "slab":
        if dim != 2:
            raise ValueError("Slab geometry benchmark is defined for dim=2")
        t = rng.uniform(0.0, 1.0, N)
        x = rng.uniform(0.0, slab_width, N)
        pts = np.column_stack([t, x])
    elif geometry == "diamond":
        chunks = []
        collected = 0
        mult = 4 if dim == 2 else (6 if dim == 3 else 10)
        while collected < N:
            batch = max(128, (N - collected) * mult)
            t = rng.uniform(0.0, 1.0, batch)
            sp = rng.uniform(-0.5, 0.5, (batch, dim - 1))
            r = np.linalg.norm(sp, axis=1) if dim > 2 else np.abs(sp[:, 0])
            valid = (r < t) & (r < (1.0 - t))
            if np.any(valid):
                chunk = np.column_stack([t[valid], sp[valid]])
                chunks.append(chunk)
                collected += chunk.shape[0]
        pts = np.vstack(chunks)[:N]
    else:
        raise ValueError(f"Unsupported geometry: {geometry}")

    pts = pts[np.argsort(pts[:, 0])]
    dt = pts[:, None, 0] - pts[None, :, 0]
    dx2 = np.sum((pts[:, None, 1:] - pts[None, :, 1:]) ** 2, axis=2)
    C = ((dt > 0.0) & ((dt * dt - dx2) > 0.0)).astype(np.uint8)
    # Enforce strict lower triangularity in case of identical timestamps
    C = np.tril(C, k=-1)
    return C


def _precompute_csg_tables(max_N, coupling_type, params):
    """Precomputes log-gamma and log-coupling tables for fast Rideout-Sorkin CSG sampling."""
    lgam = np.array([math.lgamma(m + 1) for m in range(max_N + 1)], dtype=np.float64)
    c_param = float(params.get("c", 0.20))

    if coupling_type == "log_quadratic":
        q_param = float(params.get("q", 0.20))
        k_cap = min(max_N, 64)
        ks = np.arange(k_cap + 1, dtype=np.int64)
        log_c = math.log(c_param)
        log_q = math.log(q_param)
        k_term = ks * log_c + 0.5 * ks * (ks - 1) * log_q - lgam[: k_cap + 1]
    elif coupling_type == "finite_cutoff":
        k_cap = min(max_N, int(params.get("k_max", 2)))
        ks = np.arange(k_cap + 1, dtype=np.int64)
        log_c = math.log(c_param)
        k_term = ks * log_c - lgam[: k_cap + 1]
    else:
        raise ValueError(f"Unsupported CSG table coupling_type: {coupling_type}")

    cdf_list = [None]
    for n in range(1, max_N + 1):
        klim = min(n, k_cap)
        lw = lgam[n] - lgam[n - ks[: klim + 1]] + k_term[: klim + 1]
        lw -= np.max(lw)
        w = np.exp(lw)
        w /= np.sum(w)
        cdf = np.cumsum(w)
        cdf[-1] = 1.0
        cdf_list.append(cdf)

    return lgam, ks, k_term, k_cap, cdf_list


def _uniform_k_subset(rng, n, K):
    """Samples an exact uniform K-element subset of {0, ..., n - 1} without replacement."""
    if K <= 12 and K * 4 < n:
        while True:
            cand = rng.integers(0, n, size=K)
            if len(set(cand.tolist())) == K:
                return cand
    return rng.choice(n, size=K, replace=False)


def sample_csg_fast(N, coupling_type, params, rng):
    """
    Vectorized exact Rideout-Sorkin sequential sampler for:
      - 'log_quadratic': t_k = c^k q^{binom(k, 2)}
      - 'finite_cutoff': t_k = c^k for 0 <= k <= k_max
      - 'percolation':   fixed-p Bernoulli transitive percolation
      - 'random_dag_sparse': sparse random DAG closure with p_N = min(1, c_deg / N)
    Returns (C, k_seeds_mean_last_quarter, link_deg_mean_last_quarter).
    """
    C = np.zeros((N, N), dtype=np.uint8)
    ks_tail = []
    ld_tail = []
    tail_start = max(1, N - (N // 4))

    if coupling_type in ("percolation", "random_dag_sparse"):
        if coupling_type == "percolation":
            p_edge = float(params["p"])
        else:
            p_edge = min(1.0, float(params["c_deg"]) / float(N))

        for n in range(1, N):
            B = np.nonzero(rng.random(n) < p_edge)[0]
            K = int(B.shape[0])
            if K == 1:
                b0 = int(B[0])
                C[n, :b0] = C[b0, :b0]
                C[n, b0] = 1
                max_cnt = 1
            elif K > 1:
                sub_rows = C[B, :n]
                row = np.bitwise_or.reduce(sub_rows, axis=0)
                row[B] = 1
                C[n, :n] = row
                if n >= tail_start:
                    sub_B = C[np.ix_(B, B)]
                    max_cnt = int(np.sum(np.sum(sub_B, axis=0) == 0))
                else:
                    max_cnt = 0
            else:
                max_cnt = 0

            if n >= tail_start:
                ks_tail.append(K)
                ld_tail.append(max_cnt)

        return (
            C,
            float(np.mean(ks_tail)) if ks_tail else 0.0,
            float(np.mean(ld_tail)) if ld_tail else 0.0,
        )

    lgam, ks, k_term, k_cap, cdf_list = _precompute_csg_tables(N, coupling_type, params)
    u_ks = rng.random(N)

    for n in range(1, N):
        K = int(np.searchsorted(cdf_list[n], u_ks[n], side="right"))
        if K > min(n, k_cap):
            K = min(n, k_cap)

        if K == 1:
            b0 = int(rng.integers(0, n))
            C[n, :b0] = C[b0, :b0]
            C[n, b0] = 1
            max_cnt = 1
        elif K > 1:
            B = _uniform_k_subset(rng, n, K)
            sub_rows = C[B, :n]
            row = np.bitwise_or.reduce(sub_rows, axis=0)
            row[B] = 1
            C[n, :n] = row
            if n >= tail_start:
                sub_B = C[np.ix_(B, B)]
                max_cnt = int(np.sum(np.sum(sub_B, axis=0) == 0))
            else:
                max_cnt = 0
        else:
            max_cnt = 0

        if n >= tail_start:
            ks_tail.append(K)
            ld_tail.append(max_cnt)

    return (
        C,
        float(np.mean(ks_tail)) if ks_tail else 0.0,
        float(np.mean(ld_tail)) if ld_tail else 0.0,
    )


# =============================================================================
# SECTION 1B: EXACT FUTURE-CONE 1D MARKOV CHAIN PROPOSITION & PILLAR 1 SUITE
# =============================================================================

def compute_log_partition_sequence(max_n, coupling_type, params):
    """
    Computes log(Z_n) for 0 <= n <= max_n where Z_n = sum_{k=0}^n binom(n, k) t_k
    (with Z_0 = 1, log Z_0 = 0.0).
    Also returns exact expected parent-seed counts E[K_n] for 1 <= n <= max_n.
    """
    if coupling_type == "percolation":
        p = float(params["p"])
        # t_k = (p / (1 - p))^k => Z_n = (1 - p)^{-n}
        log_z = np.array([-n * math.log(1.0 - p) for n in range(max_n + 1)], dtype=np.float64)
        mean_k = np.array([n * p for n in range(max_n + 1)], dtype=np.float64)
        return log_z, mean_k

    lgam, ks, k_term, k_cap, _ = _precompute_csg_tables(max_n, coupling_type, params)
    log_z = np.zeros(max_n + 1, dtype=np.float64)
    mean_k = np.zeros(max_n + 1, dtype=np.float64)

    for n in range(1, max_n + 1):
        klim = min(n, k_cap)
        lw = lgam[n] - lgam[n - ks[: klim + 1]] + k_term[: klim + 1]
        m_lw = float(np.max(lw))
        w_unnorm = np.exp(lw - m_lw)
        s_unnorm = float(np.sum(w_unnorm))
        log_z[n] = m_lw + math.log(s_unnorm)
        probs = w_unnorm / s_unnorm
        mean_k[n] = float(np.dot(ks[: klim + 1], probs))

    return log_z, mean_k


def exact_future_cone_markov_distribution(N, n0, log_z):
    """
    Exact 1D Markov chain distribution of F_N(u) = |J^+_{P_N}[u]| for vertex u born at
    stage n0 (0 <= n0 < N), initialized at F_{n0 + 1}(u) = 1:
        P(F_{n+1} = f | F_n = f)     = exp(log_z[n - f] - log_z[n]) = Z_{n - f} / Z_n,
        P(F_{n+1} = f + 1 | F_n = f) = 1 - Z_{n - f} / Z_n.
    Returns probability vector dist of length (N - n0 + 1) indexed by f in {0..N-n0}.
    """
    max_f = N - n0
    dist = np.zeros(max_f + 1, dtype=np.float64)
    dist[1] = 1.0
    for n in range(n0 + 1, N):
        f_hi = n - n0
        fs = np.arange(1, f_hi + 1, dtype=np.int64)
        p_stay = np.exp(log_z[n - fs] - log_z[n])
        p_grow = 1.0 - p_stay
        nxt = np.zeros_like(dist)
        nxt[fs] += dist[fs] * p_stay
        nxt[fs + 1] += dist[fs] * p_grow
        dist = nxt
    return dist


def exact_ensemble_expected_r2_via_future_cone(N, log_z):
    """
    Computes exact E[R_2(P_N)] for any subset-weight CSG law purely from the 1D
    Future-Cone Markov Chain without sampling any poset:
        E[C_1(P_N)] = sum_{n0 = 0}^{N - 1} (E[F_N(x_{n0})] - 1).
    Vectorized across all birth stages n0 simultaneously in O(N^2) operations!
    """
    if N < 2:
        return 0.0
    # Note: linearity of expectation gives E[F_{n+1}(u) | F_n(u)] directly, or we evolve
    # the summed occupancy histogram H[f] = sum_{n0=0}^{n-1} P(F_n(x_{n0}) == f) in O(N) memory!
    H = np.zeros(N + 1, dtype=np.float64)
    H[1] = 1.0  # vertex x_0 at stage n = 1 has F_1(x_0) = 1
    for n in range(1, N):
        fs = np.arange(1, n + 1, dtype=np.int64)
        p_stay = np.exp(log_z[n - fs] - log_z[n])
        cur = H[fs].copy()
        H[fs] = cur * p_stay
        H[fs + 1] += cur * (1.0 - p_stay)
        H[1] += 1.0  # newborn vertex x_n enters with F_{n+1}(x_n) = 1
    all_fs = np.arange(N + 1, dtype=np.float64)
    expected_c1 = float(np.dot(all_fs, H)) - float(N)
    return expected_c1 / (N * (N - 1) / 2.0)


def verify_future_cone_markov_proposition(N_mc=96, num_mc=400, seed=20260811):
    """
    Verifies Proposition 1.1 numerically by comparing the exact 1D Future-Cone Markov
    chain distribution and exact E[R_2(P_N)] against Monte Carlo CSG simulations, and
    evaluates exact E[K_N] octave increments across N in {512, 1024, 2048, 4096}.
    """
    rng = np.random.default_rng(seed)
    params_q20 = {"c": 0.20, "q": 0.20}
    params_q10 = {"c": 0.20, "q": 0.10}

    log_z_q20, mean_k_q20 = compute_log_partition_sequence(4096, "log_quadratic", params_q20)
    log_z_q10, mean_k_q10 = compute_log_partition_sequence(4096, "log_quadratic", params_q10)

    exact_r2_mc = exact_ensemble_expected_r2_via_future_cone(N_mc, log_z_q20)
    probe_n0s = [n0 for n0 in (0, 8, 24, 48, 64) if n0 < N_mc]
    exact_f_means = {}
    for n0 in probe_n0s:
        dist = exact_future_cone_markov_distribution(N_mc, n0, log_z_q20)
        exact_f_means[str(n0)] = float(np.dot(np.arange(len(dist), dtype=np.float64), dist))

    mc_r2s = []
    mc_f_samples = {str(n0): [] for n0 in probe_n0s}
    for _ in range(num_mc):
        C, _, _ = sample_csg_fast(N_mc, "log_quadratic", params_q20, rng)
        mc_r2s.append(float(np.sum(C)) / (N_mc * (N_mc - 1) / 2.0))
        fut_inclusive = 1 + np.sum(C, axis=0)
        for n0 in probe_n0s:
            mc_f_samples[str(n0)].append(int(fut_inclusive[n0]))

    mc_r2_mean = float(np.mean(mc_r2s))
    mc_r2_sem = float(np.std(mc_r2s, ddof=1)) / math.sqrt(num_mc)
    mc_f_means = {k: float(np.mean(v)) for k, v in mc_f_samples.items()}

    # Exact E[R_2(P_N)] and E[K_N] across ALL horizons including 2048 and 4096!
    exact_horizon_table = {}
    for N_val in (512, 1024, 2048, 4096):
        ex_r2_20 = exact_ensemble_expected_r2_via_future_cone(N_val, log_z_q20)
        ex_r2_10 = exact_ensemble_expected_r2_via_future_cone(N_val, log_z_q10)
        exact_horizon_table[str(N_val)] = {
            "q020_mean_K_N": round(float(mean_k_q20[N_val]), 6),
            "q010_mean_K_N": round(float(mean_k_q10[N_val]), 6),
            "q020_exact_expected_r2": round(ex_r2_20, 6),
            "q010_exact_expected_r2": round(ex_r2_10, 6),
        }

    octave_dk_q20 = [
        float(mean_k_q20[1024] - mean_k_q20[512]),
        float(mean_k_q20[2048] - mean_k_q20[1024]),
        float(mean_k_q20[4096] - mean_k_q20[2048]),
    ]
    asymp_dk_q20 = math.log(2.0) / math.log(1.0 / 0.20)
    asymp_dk_q10 = math.log(2.0) / math.log(1.0 / 0.10)

    return {
        "N_mc": N_mc,
        "num_mc": num_mc,
        "exact_r2": exact_r2_mc,
        "mc_r2_mean": mc_r2_mean,
        "mc_r2_sem": mc_r2_sem,
        "abs_r2_error": abs(exact_r2_mc - mc_r2_mean),
        "exact_f_means": exact_f_means,
        "mc_f_means": mc_f_means,
        "asymptotic_octave_delta_mu_q020": asymp_dk_q20,
        "asymptotic_octave_delta_mu_q010": asymp_dk_q10,
        "realized_octave_delta_K_q020": octave_dk_q20,
        "exact_horizon_table": exact_horizon_table,
    }


PILLAR1_MODELS = [
    {
        "model_id": "log_quad_c02_q020",
        "label": "Log-Quadratic CSG (c=0.20, q=0.20)",
        "family": "frozen_candidate",
        "sampler": "csg",
        "coupling_type": "log_quadratic",
        "params": {"c": 0.20, "q": 0.20},
    },
    {
        "model_id": "log_quad_c02_q010",
        "label": "Log-Quadratic CSG (c=0.20, q=0.10)",
        "family": "frozen_companion",
        "sampler": "csg",
        "coupling_type": "log_quadratic",
        "params": {"c": 0.20, "q": 0.10},
    },
    {
        "model_id": "minkowski_4d",
        "label": "4D Minkowski Diamond",
        "family": "geometric_control",
        "sampler": "minkowski",
        "dim": 4,
        "geometry": "diamond",
    },
    {
        "model_id": "minkowski_2d",
        "label": "2D Minkowski Diamond",
        "family": "geometric_control",
        "sampler": "minkowski",
        "dim": 2,
        "geometry": "diamond",
    },
    {
        "model_id": "minkowski_2d_slab",
        "label": "2D Minkowski Slab [0,1]x[0,3]",
        "family": "geometric_control",
        "sampler": "minkowski",
        "dim": 2,
        "geometry": "slab",
        "slab_width": 3.0,
    },
    {
        "model_id": "cutoff_kmax2",
        "label": "Finite-Cutoff CSG (c=1.0, k_max=2)",
        "family": "non_geometric_control",
        "sampler": "csg",
        "coupling_type": "finite_cutoff",
        "params": {"c": 1.0, "k_max": 2},
    },
    {
        "model_id": "percolation_p008",
        "label": "Bernoulli Percolation (p=0.08)",
        "family": "non_geometric_control",
        "sampler": "csg",
        "coupling_type": "percolation",
        "params": {"p": 0.08},
    },
    {
        "model_id": "random_dag_sparse",
        "label": "Sparse Random DAG Closure (c_deg=2.0)",
        "family": "non_geometric_control",
        "sampler": "csg",
        "coupling_type": "random_dag_sparse",
        "params": {"c_deg": 2.0},
    },
]

FIXED_M_WINDOWS = [
    ("6_11", 6, 11),
    ("12_24", 12, 24),
    ("25_48", 25, 48),
    ("49_96", 49, 96),
]

GROWING_ALPHAS = (0.35, 0.50, 0.65)
OBS_KEYS = ("r2", "d_mm", "ell_link", "h_over_m", "rho2", "wmin_over_m")


def _evaluate_windows_on_poset(C, C2, windows_dict, delta_bulk, max_intervals, rng):
    """
    Evaluates all five interval structural observables across multiple [m_lo, m_hi]
    windows on a single realized poset C with precomputed C2 = C @ C.
    """
    past_sizes = np.sum(C, axis=1)
    future_sizes = np.sum(C, axis=0)
    j_bar = float(np.mean(past_sizes))
    bulk_thresh = delta_bulk * j_bar

    min_m_all = min(lo for lo, _ in windows_dict.values())
    max_m_all = max(hi for _, hi in windows_dict.values())
    bv, bu = np.nonzero(
        (C == 1)
        & (C2 >= min_m_all)
        & (C2 <= max_m_all)
        & (future_sizes[:, None] >= bulk_thresh)
        & (past_sizes[None, :] >= bulk_thresh)
    )
    bm = C2[bv, bu]

    out = {}
    for w_key, (m_lo, m_hi) in windows_dict.items():
        w_idx = np.nonzero((bm >= m_lo) & (bm <= m_hi))[0]
        j_cnt = int(w_idx.shape[0])
        if j_cnt == 0:
            out[w_key] = {"j_count": 0, "valid": False}
            continue
        if j_cnt > max_intervals:
            sel = w_idx[rng.choice(j_cnt, size=max_intervals, replace=False)]
        else:
            sel = w_idx

        per_int = {k: [] for k in OBS_KEYS}
        m_vals = []
        for idx_pair in sel:
            v = int(bv[idx_pair])
            u = int(bu[idx_pair])
            zs = (u + 1) + np.nonzero(C[v, u + 1 : v] & C[u + 1 : v, u])[0]
            if zs.shape[0] >= 2:
                obs = compute_interval_five_observables(C[np.ix_(zs, zs)])
                m_vals.append(obs["m"])
                for k in OBS_KEYS:
                    per_int[k].append(obs[k])

        if not m_vals:
            out[w_key] = {"j_count": j_cnt, "valid": False}
            continue

        summary = {
            "j_count": j_cnt,
            "valid": True,
            "m_mean": float(np.mean(m_vals)),
            "r2_var_within": float(np.var(per_int["r2"], ddof=1)) if len(per_int["r2"]) > 1 else 0.0,
        }
        for k in OBS_KEYS:
            summary[k] = float(np.mean(per_int[k]))
        if summary["r2"] > 0.0:
            summary["d_mm"] = invert_myrheim_meyer(summary["r2"])
        out[w_key] = summary

    return out


def _aggregate_window_runs(run_list, m_lo, m_hi):
    """Aggregates run-level window summaries across M independent histories."""
    j_counts = [r["j_count"] for r in run_list]
    valid_runs = [r for r in run_list if r.get("valid", False)]
    n_valid = len(valid_runs)
    agg = {
        "m_window": [int(m_lo), int(m_hi)],
        "valid_runs": n_valid,
        "total_runs": len(run_list),
        "mean_j_count": float(np.mean(j_counts)) if j_counts else 0.0,
        "mean_m_realized": float(np.mean([r["m_mean"] for r in valid_runs])) if n_valid > 0 else None,
        "r2_var_within_mean": float(np.mean([r["r2_var_within"] for r in valid_runs])) if n_valid > 0 else None,
    }
    for k in OBS_KEYS:
        if n_valid > 0:
            vals = [r[k] for r in valid_runs]
            agg[f"{k}_mean"] = float(np.mean(vals))
            agg[f"{k}_std"] = float(np.std(vals, ddof=1)) if n_valid > 1 else 0.0
        else:
            agg[f"{k}_mean"] = None
            agg[f"{k}_std"] = None
    return agg


def run_pillar1_frozen_holdout_suite(
    horizons=(512, 1024, 2048),
    runs_by_horizon=None,
    n4096_runs=10,
    max_intervals_per_window=50,
    delta_bulk=0.05,
    base_seed=20260801,
):
    """
    Executes Pillar 1: Frozen Multi-Horizon & Multi-Observable Scale-Pattern Holdout Test.
    """
    if runs_by_horizon is None:
        runs_by_horizon = {512: 16, 1024: 16, 2048: 12}

    t0 = time.time()
    horizons_out = {}
    trim_sensitivity = {"N": 1024, "m_window": [12, 24], "deltas": [0.02, 0.05, 0.10], "models": {}}

    for N in horizons:
        n_key = str(N)
        horizons_out[n_key] = {}
        num_runs = int(runs_by_horizon.get(N, 12))

        fixed_w = {wk: (lo, hi) for wk, lo, hi in FIXED_M_WINDOWS}
        grow_w = {
            f"alpha_{a:.2f}": (
                max(4, int(math.ceil(0.5 * (N ** a)))),
                max(6, int(math.floor(1.5 * (N ** a)))),
            )
            for a in GROWING_ALPHAS
        }
        all_windows = {}
        for wk, bounds in fixed_w.items():
            all_windows[f"fixed_{wk}"] = bounds
        for ak, bounds in grow_w.items():
            all_windows[ak] = bounds

        for m_idx, cfg in enumerate(PILLAR1_MODELS):
            mid = cfg["model_id"]
            glob_r2s = []
            glob_dmms = []
            k_seeds = []
            link_degs = []
            win_runs = {wk: [] for wk in all_windows}
            trim_runs = {f"{d:.2f}": [] for d in (0.02, 0.05, 0.10)} if (
                N == 1024 and mid in ("log_quad_c02_q020", "minkowski_4d")
            ) else None

            for r in range(num_runs):
                run_seed = base_seed + 100000 * N + 1000 * m_idx + r
                rng = np.random.default_rng(run_seed)

                if cfg["sampler"] == "minkowski":
                    C = sample_minkowski_fast(
                        cfg["dim"],
                        N,
                        rng,
                        geometry=cfg.get("geometry", "diamond"),
                        slab_width=cfg.get("slab_width", 3.0),
                    )
                    ks_m, ld_m = None, None
                else:
                    C, ks_m, ld_m = sample_csg_fast(N, cfg["coupling_type"], cfg["params"], rng)

                r2_g = float(np.sum(C)) / (N * (N - 1) / 2.0)
                glob_r2s.append(r2_g)
                glob_dmms.append(invert_myrheim_meyer(r2_g) if r2_g > 0.0 else 16.0)
                if ks_m is not None:
                    k_seeds.append(ks_m)
                    link_degs.append(ld_m)

                C_f = C.astype(np.float32)
                C2 = np.rint(C_f @ C_f).astype(np.int32)

                eval_res = _evaluate_windows_on_poset(
                    C, C2, all_windows, delta_bulk, max_intervals_per_window, rng
                )
                for wk, wres in eval_res.items():
                    win_runs[wk].append(wres)

                if trim_runs is not None:
                    for d_trim in (0.02, 0.05, 0.10):
                        tres = _evaluate_windows_on_poset(
                            C, C2, {"12_24": (12, 24)}, d_trim, max_intervals_per_window, rng
                        )
                        trim_runs[f"{d_trim:.2f}"].append(tres["12_24"])

            fixed_agg = {
                wk: _aggregate_window_runs(win_runs[f"fixed_{wk}"], lo, hi)
                for wk, lo, hi in FIXED_M_WINDOWS
            }
            grow_agg = {
                f"{a:.2f}": _aggregate_window_runs(
                    win_runs[f"alpha_{a:.2f}"],
                    grow_w[f"alpha_{a:.2f}"][0],
                    grow_w[f"alpha_{a:.2f}"][1],
                )
                for a in GROWING_ALPHAS
            }

            horizons_out[n_key][mid] = {
                "label": cfg["label"],
                "family": cfg["family"],
                "num_runs": num_runs,
                "global_r2_mean": float(np.mean(glob_r2s)),
                "global_r2_std": float(np.std(glob_r2s, ddof=1)) if num_runs > 1 else 0.0,
                "global_var_between": float(np.var(glob_r2s, ddof=1)) if num_runs > 1 else 0.0,
                "global_d_mm_mean": float(np.mean(glob_dmms)),
                "global_d_mm_std": float(np.std(glob_dmms, ddof=1)) if num_runs > 1 else 0.0,
                "k_seed_tail_mean": float(np.mean(k_seeds)) if k_seeds else None,
                "link_deg_tail_mean": float(np.mean(link_degs)) if link_degs else None,
                "fixed_m_windows": fixed_agg,
                "growing_alpha_windows": grow_agg,
            }

            if trim_runs is not None:
                trim_sensitivity["models"][mid] = {
                    dk: _aggregate_window_runs(tlist, 12, 24)
                    for dk, tlist in trim_runs.items()
                }

    # Extended N = 4096 holdout check on frozen log_quad_c02_q020
    n4096_summary = None
    if n4096_runs > 0:
        N_big = 4096
        fixed_w_big = {wk: (lo, hi) for wk, lo, hi in FIXED_M_WINDOWS}
        grow_w_big = {
            f"alpha_{a:.2f}": (
                max(4, int(math.ceil(0.5 * (N_big ** a)))),
                max(6, int(math.floor(1.5 * (N_big ** a)))),
            )
            for a in GROWING_ALPHAS
        }
        all_w_big = {}
        for wk, bounds in fixed_w_big.items():
            all_w_big[f"fixed_{wk}"] = bounds
        for ak, bounds in grow_w_big.items():
            all_w_big[ak] = bounds

        glob_r2s_big, glob_dmms_big, ks_big, ld_big = [], [], [], []
        win_runs_big = {wk: [] for wk in all_w_big}
        for r in range(n4096_runs):
            rng = np.random.default_rng(base_seed + 100000 * N_big + r)
            C, ks_m, ld_m = sample_csg_fast(
                N_big, "log_quadratic", {"c": 0.20, "q": 0.20}, rng
            )
            r2_g = float(np.sum(C)) / (N_big * (N_big - 1) / 2.0)
            glob_r2s_big.append(r2_g)
            glob_dmms_big.append(invert_myrheim_meyer(r2_g))
            ks_big.append(ks_m)
            ld_big.append(ld_m)

            C_f = C.astype(np.float32)
            C2 = np.rint(C_f @ C_f).astype(np.int32)
            eval_res = _evaluate_windows_on_poset(
                C, C2, all_w_big, delta_bulk, max_intervals_per_window, rng
            )
            for wk, wres in eval_res.items():
                win_runs_big[wk].append(wres)

        n4096_summary = {
            "N": N_big,
            "model_id": "log_quad_c02_q020",
            "num_runs": n4096_runs,
            "global_r2_mean": float(np.mean(glob_r2s_big)),
            "global_r2_std": float(np.std(glob_r2s_big, ddof=1)) if n4096_runs > 1 else 0.0,
            "global_var_between": float(np.var(glob_r2s_big, ddof=1)) if n4096_runs > 1 else 0.0,
            "global_d_mm_mean": float(np.mean(glob_dmms_big)),
            "k_seed_tail_mean": float(np.mean(ks_big)),
            "link_deg_tail_mean": float(np.mean(ld_big)),
            "fixed_m_windows": {
                wk: _aggregate_window_runs(win_runs_big[f"fixed_{wk}"], lo, hi)
                for wk, lo, hi in FIXED_M_WINDOWS
            },
            "growing_alpha_windows": {
                f"{a:.2f}": _aggregate_window_runs(
                    win_runs_big[f"alpha_{a:.2f}"],
                    grow_w_big[f"alpha_{a:.2f}"][0],
                    grow_w_big[f"alpha_{a:.2f}"][1],
                )
                for a in GROWING_ALPHAS
            },
        }

    markov_prop = verify_future_cone_markov_proposition()

    # Pre-declared decision evaluation on frozen log_quad_c02_q020 vs minkowski_4d
    decision_eval = {}
    if all(str(h) in horizons_out for h in (512, 1024, 2048)):
        lq_512_w6 = horizons_out["512"]["log_quad_c02_q020"]["fixed_m_windows"]["6_11"]
        lq_2048_w6 = horizons_out["2048"]["log_quad_c02_q020"]["fixed_m_windows"]["6_11"]
        lq_512_w = horizons_out["512"]["log_quad_c02_q020"]["fixed_m_windows"]["12_24"]
        lq_2048_w = horizons_out["2048"]["log_quad_c02_q020"]["fixed_m_windows"]["12_24"]
        m4_512_w = horizons_out["512"]["minkowski_4d"]["fixed_m_windows"]["12_24"]
        m4_2048_w = horizons_out["2048"]["minkowski_4d"]["fixed_m_windows"]["12_24"]

        lq_m6_11_r2_drift_per_oct = 0.5 * (lq_2048_w6["r2_mean"] - lq_512_w6["r2_mean"])
        lq_r2_drift_per_oct = 0.5 * (lq_2048_w["r2_mean"] - lq_512_w["r2_mean"])
        lq_rho2_drift_per_oct = 0.5 * (lq_2048_w["rho2_mean"] - lq_512_w["rho2_mean"])
        m4_r2_drift_per_oct = 0.5 * (m4_2048_w["r2_mean"] - m4_512_w["r2_mean"])
        lq_m_span_2048 = (
            horizons_out["2048"]["log_quad_c02_q020"]["fixed_m_windows"]["6_11"]["r2_mean"]
            - horizons_out["2048"]["log_quad_c02_q020"]["fixed_m_windows"]["49_96"]["r2_mean"]
        )
        stationarity_tol = 0.012  # pre-declared max |drift/octave| for strict fixed-m R_2 stationarity
        passes_m_crossover = bool(lq_m_span_2048 > 0.40)
        passes_fixed_m_stationarity = bool(
            max(abs(lq_m6_11_r2_drift_per_oct), abs(lq_r2_drift_per_oct)) <= stationarity_tol
        )
        passes_4d_width = bool(lq_2048_w["wmin_over_m_mean"] >= 0.40)

        decision_eval = {
            "candidate_id": "log_quad_c02_q020",
            "predeclared_fixed_m_octave_drift_tol": stationarity_tol,
            "lq_m6_11_r2_drift_per_octave_512_to_2048": lq_m6_11_r2_drift_per_oct,
            "lq_m12_24_r2_drift_per_octave_512_to_2048": lq_r2_drift_per_oct,
            "lq_m12_24_rho2_drift_per_octave_512_to_2048": lq_rho2_drift_per_oct,
            "mink4d_m12_24_r2_drift_per_octave_512_to_2048": m4_r2_drift_per_oct,
            "lq_m_crossover_span_6_11_to_49_96_at_2048": lq_m_span_2048,
            "lq_wmin_over_m_at_2048_m12_24": lq_2048_w["wmin_over_m_mean"],
            "mink4d_wmin_over_m_at_2048_m12_24": m4_2048_w["wmin_over_m_mean"],
            "passes_m_scale_crossover": passes_m_crossover,
            "passes_strict_fixed_m_stationarity": passes_fixed_m_stationarity,
            "passes_4d_transverse_entry_width": passes_4d_width,
            "disposition": (
                "RETIRE_STATIC_SCALAR_STANDALONE_GEOMETRY_RETAIN_AS_BASELINE_KERNEL"
                if not (passes_fixed_m_stationarity and passes_4d_width)
                else "PASS_STATIONARY_HOLDOUT"
            ),
        }

    return {
        "parameters": {
            "horizons": list(horizons),
            "runs_by_horizon": {str(k): int(v) for k, v in runs_by_horizon.items()},
            "n4096_runs": n4096_runs,
            "max_intervals_per_window": max_intervals_per_window,
            "delta_bulk": delta_bulk,
            "base_seed": base_seed,
            "elapsed_seconds": time.time() - t0,
        },
        "horizons": horizons_out,
        "boundary_trim_sensitivity_N1024_m12_24": trim_sensitivity,
        "large_horizon_N4096_check": n4096_summary,
        "future_cone_markov_proposition": markov_prop,
        "decision_evaluation": decision_eval,
    }


# =============================================================================
# SECTION 2: PILLAR 2 — COARSE PROJECTION & ACTIVE RESIDUAL-TO-STRUCTURE LAWS
# =============================================================================

def _get_ideals_adj(adj):
    """Enumerates all downward-closed ideals of a small poset with upper-triangular adj[u,v]=(u<v)."""
    n = adj.shape[0]
    ideals = []
    for mask in range(1 << n):
        ok = True
        for v in range(n):
            if (mask >> v) & 1:
                for u in range(n):
                    if adj[u, v] and not ((mask >> u) & 1):
                        ok = False
                        break
            if not ok:
                break
        if ok:
            ideals.append(frozenset(i for i in range(n) if (mask >> i) & 1))
    return ideals


def _max_elements_adj(adj, S):
    return [u for u in S if not any((v in S and v != u and adj[u, v]) for v in S)]


def _extend_poset_adj(adj, S):
    n = adj.shape[0]
    child = np.zeros((n + 1, n + 1), dtype=bool)
    child[:n, :n] = adj
    for u in S:
        child[u, n] = True
    return child


def _csg_ideal_prob_exact(adj, S, t_seq):
    """Exact Rideout-Sorkin transition probability q(P_n, S) for small posets."""
    n = adj.shape[0]
    d = len(_max_elements_adj(adj, S))
    p = len(S) - d
    num = sum(math.comb(p, j) * t_seq[d + j] for j in range(p + 1))
    den = sum(math.comb(n, k) * t_seq[k] for k in range(n + 1))
    return num / den


def _canonical_marked_signature(adj, marks):
    """Canonical isomorphism invariant of a small marked poset (V, <, r)."""
    import itertools
    n = adj.shape[0]
    if n == 0:
        return (0, (), ())
    best = None
    for perm in itertools.permutations(range(n)):
        edge_tuple = tuple(
            int(adj[perm[i], perm[j]]) for i in range(n) for j in range(n)
        )
        mark_tuple = tuple(int(marks[perm[i]]) for i in range(n))
        cand = (n, mark_tuple, edge_tuple)
        if best is None or cand < best:
            best = cand
    return best


def verify_coarse_projection_theorems():
    """
    Verifies Theorem 2.1:
      (a) Intrinsic anchor projection Pi_A commutes across 100% of 3,644 incomparable
          diamonds (1 <= |C| <= 4), whereas stage-parity selection fails diamond commutation.
      (b) Omitted micro-interval chain C^{(m)} = {u < z_1 < ... < z_m < v} (anchors {u, v})
          projects to the identical coarse 2-chain {u < v} for all m >= 0, yet the exact
          branching-to-disconnected probability ratio P(S cap V_A = {u}) / P(S = empty)
          equals Z_{m+1} - 1 (which equals (1 + m) c for k_max = 1, and G(1 + m, 1) for the
          maximal micro-ideal S = {u, z_1, ..., z_m}).
      (c) Retaining the micro-interval shadow-volume vector Z_geom(C) = (nu_C(I))_{I in I(C_tilde)}
          restores exact coarse transition sufficiency across 100% of marked posets up to N = 4.
    """
    posets_by_n = {n: [] for n in range(1, 5)}
    for n_val, C_low in generate_naturally_ordered_posets(4):
        posets_by_n[n_val].append(C_low.T > 0.5)

    # (a) Exhaustive diamond commutation check for intrinsic-past anchor rule vs stage-parity rule
    # Intrinsic rule: x in V_A iff |S| >= 1 (has nonempty past, intrinsic to S)
    # Stage-parity rule: x in V_A iff birth stage n is odd (extrinsic!)
    total_diamonds = 0
    intrinsic_proj_violations = 0
    stage_parity_proj_violations = 0

    for n in (1, 2, 3, 4):
        for adj in posets_by_n[n]:
            ideals = _get_ideals_adj(adj)
            anc_base = [1 if int(np.sum(adj[:, i])) >= 1 else 0 for i in range(n)]
            # Canonical transport between (C + x_S) + y_T and (C + y_T) + x_S swaps n <-> n + 1
            perm_swap = list(range(n)) + [n + 1, n]
            for S in ideals:
                adj_x = _extend_poset_adj(adj, S)
                for T in ideals:
                    adj_y = _extend_poset_adj(adj, T)
                    total_diamonds += 1

                    # Path 1: x_S at stage n, then y_T at stage n + 1
                    adj_xy = _extend_poset_adj(adj_x, T)
                    anc_xy_intr = anc_base + [1 if len(S) >= 1 else 0, 1 if len(T) >= 1 else 0]

                    # Path 2: y_T at stage n, then x_S at stage n + 1, transported via perm_swap
                    adj_yx = _extend_poset_adj(adj_y, S)
                    anc_yx_intr = anc_base + [1 if len(T) >= 1 else 0, 1 if len(S) >= 1 else 0]
                    adj_yx_tr = adj_yx[np.ix_(perm_swap, perm_swap)]
                    anc_yx_tr = [anc_yx_intr[p] for p in perm_swap]

                    idx1 = [i for i, flg in enumerate(anc_xy_intr) if flg == 1]
                    idx2 = [i for i, flg in enumerate(anc_yx_tr) if flg == 1]
                    if idx1 != idx2 or not np.array_equal(
                        adj_xy[np.ix_(idx1, idx1)], adj_yx_tr[np.ix_(idx2, idx2)]
                    ):
                        intrinsic_proj_violations += 1

                    # Extrinsic stage-parity rule: stage n odd -> 1, even -> 0
                    anc_xy_par = anc_base + [n % 2, (n + 1) % 2]
                    anc_yx_par_tr = [
                        (anc_base + [n % 2, (n + 1) % 2])[p] for p in perm_swap
                    ]
                    p_idx1 = [i for i, flg in enumerate(anc_xy_par) if flg == 1]
                    p_idx2 = [i for i, flg in enumerate(anc_yx_par_tr) if flg == 1]
                    if p_idx1 != p_idx2 or not np.array_equal(
                        adj_xy[np.ix_(p_idx1, p_idx1)], adj_yx_tr[np.ix_(p_idx2, p_idx2)]
                    ):
                        stage_parity_proj_violations += 1

    # (b) Omitted micro-interval chain C^{(m)} = {u < z_1 < ... < z_m < v} for m = 0..4
    c_val = 0.20
    q_val = 0.20
    t_kmax1 = [1.0, c_val] + [0.0] * 12
    t_logq = [(c_val ** k) * (q_val ** (k * (k - 1) // 2)) for k in range(14)]

    omitted_chain_table = []
    max_formula_err = 0.0
    for m_omit in range(0, 5):
        n_tot = m_omit + 2  # vertices 0=u, 1..m=z_i, m+1=v; anchors = {0, m+1}
        adj_chain = np.zeros((n_tot, n_tot), dtype=bool)
        for i in range(n_tot):
            for j in range(i + 1, n_tot):
                adj_chain[i, j] = True
        ideals_ch = _get_ideals_adj(adj_chain)
        anchors = frozenset([0, n_tot - 1])

        # Verify projected poset is always the 2-chain {0 < 1}
        proj_adj = adj_chain[np.ix_([0, n_tot - 1], [0, n_tot - 1])]
        assert proj_adj.shape == (2, 2) and proj_adj[0, 1] and not proj_adj[1, 0]

        # Enumerate exact coarse transition probabilities under k_max=1 and Log-Quadratic
        p_empty_k1 = sum(_csg_ideal_prob_exact(adj_chain, S, t_kmax1) for S in ideals_ch if len(S & anchors) == 0)
        p_branch_k1 = sum(_csg_ideal_prob_exact(adj_chain, S, t_kmax1) for S in ideals_ch if (S & anchors) == frozenset([0]))
        ratio_k1 = p_branch_k1 / p_empty_k1
        analytic_k1 = (1 + m_omit) * c_val

        p_empty_lq = sum(_csg_ideal_prob_exact(adj_chain, S, t_logq) for S in ideals_ch if len(S & anchors) == 0)
        p_branch_lq = sum(_csg_ideal_prob_exact(adj_chain, S, t_logq) for S in ideals_ch if (S & anchors) == frozenset([0]))
        ratio_lq = p_branch_lq / p_empty_lq
        z_m_plus_1_lq = sum(math.comb(m_omit + 1, k) * t_logq[k] for k in range(m_omit + 2))
        analytic_lq = z_m_plus_1_lq - 1.0

        # Maximal micro-ideal S_max = {0, 1, ..., m} weight ratio G(1 + m, 1)
        s_max = frozenset(range(m_omit + 1))
        g_max_lq = _csg_ideal_prob_exact(adj_chain, s_max, t_logq) / p_empty_lq
        analytic_g_max = sum(math.comb(m_omit, j) * t_logq[1 + j] for j in range(m_omit + 1))

        max_formula_err = max(
            max_formula_err,
            abs(ratio_k1 - analytic_k1),
            abs(ratio_lq - analytic_lq),
            abs(g_max_lq - analytic_g_max),
        )
        omitted_chain_table.append({
            "m_omitted": m_omit,
            "kmax1_branch_over_empty": ratio_k1,
            "kmax1_analytic_linear": analytic_k1,
            "logq_branch_over_empty": ratio_lq,
            "logq_analytic_Zm1_minus_1": analytic_lq,
            "logq_max_ideal_G_1_plus_m": g_max_lq,
        })

    # (c) Exhaustive Markov sufficiency audit of (C_tilde, Z_geom) across all marked posets N <= 4
    # Group all (adj, anchor_mask) for 1 <= N <= 4 by fixed labeled anchor order + Z_geom
    buckets_with_zgeom = {}
    buckets_coarse_only = {}
    for n in (1, 2, 3, 4):
        for adj in posets_by_n[n]:
            ideals = _get_ideals_adj(adj)
            q_map = {S: _csg_ideal_prob_exact(adj, S, t_logq) for S in ideals}
            for anc_mask in range(1 << n):
                anc_list = [i for i in range(n) if (anc_mask >> i) & 1]
                k_anc = len(anc_list)
                anc_pos = {v_orig: idx for idx, v_orig in enumerate(anc_list)}
                coarse_adj = tuple(
                    int(adj[anc_list[a], anc_list[b]]) for a in range(k_anc) for b in range(k_anc)
                )
                # Shadow pi_A^-(y) in {0..k_anc-1} for each micro-vertex y in {0..n-1}
                shadows = []
                for y in range(n):
                    sh = frozenset(
                        anc_pos[a] for a in anc_list if (a == y or adj[a, y])
                    )
                    shadows.append(sh)
                coarse_ideals = _get_ideals_adj(
                    np.array(coarse_adj, dtype=bool).reshape((k_anc, k_anc))
                ) if k_anc > 0 else [frozenset()]
                nu_vec = tuple(sum(1 for sh in shadows if sh == ci) for ci in coarse_ideals)

                # Induced exact coarse transition distribution over coarse_ideals
                coarse_dist = []
                for ci in coarse_ideals:
                    prob_ci = sum(
                        q_map[S]
                        for S in ideals
                        if frozenset(anc_pos[a] for a in S if a in anc_pos) == ci
                    )
                    coarse_dist.append(prob_ci)
                coarse_dist = tuple(coarse_dist)

                key_full = (k_anc, coarse_adj, nu_vec)
                buckets_with_zgeom.setdefault(key_full, []).append(coarse_dist)

                key_coarse = (k_anc, coarse_adj)
                buckets_coarse_only.setdefault(key_coarse, []).append(coarse_dist)

    max_zgeom_sufficiency_discrepancy = 0.0
    nontrivial_zgeom_collisions = 0
    for key_full, dists in buckets_with_zgeom.items():
        if len(dists) > 1:
            nontrivial_zgeom_collisions += 1
            ref = np.array(dists[0])
            for d_other in dists[1:]:
                max_zgeom_sufficiency_discrepancy = max(
                    max_zgeom_sufficiency_discrepancy, float(np.max(np.abs(ref - np.array(d_other))))
                )

    max_coarse_only_non_markov_gap = 0.0
    for key_coarse, dists in buckets_coarse_only.items():
        if len(dists) > 1:
            ref = np.array(dists[0])
            for d_other in dists[1:]:
                max_coarse_only_non_markov_gap = max(
                    max_coarse_only_non_markov_gap, float(np.max(np.abs(ref - np.array(d_other))))
                )

    return {
        "total_diamonds_n_le_4": total_diamonds,
        "intrinsic_projection_diamond_violations": intrinsic_proj_violations,
        "stage_parity_projection_diamond_violations": stage_parity_proj_violations,
        "omitted_chain_non_markov_table": omitted_chain_table,
        "omitted_chain_max_formula_err": max_formula_err,
        "zgeom_equivalence_classes_checked": len(buckets_with_zgeom),
        "zgeom_multi_member_classes": nontrivial_zgeom_collisions,
        "max_zgeom_sufficiency_discrepancy": max_zgeom_sufficiency_discrepancy,
        "max_coarse_only_non_markov_gap": max_coarse_only_non_markov_gap,
    }


class ActiveRootMartingaleLaw:
    """
    Theorem 2A: Arbitrary-horizon active off-diagonal residual-to-structure law on X = (C, Z)
    driven by the exact birth-order-independent subset-weight root martingale:
        M_root(P_n) = |Min(P_n)| - sum_{j=0}^{n-1} (1 / Z_j).
    """

    def __init__(self, t_seq, t_ret=0.75, N_act=12, theta=None):
        self.t_seq = list(t_seq)
        self.t_ret = float(t_ret)
        self.N_act = int(N_act)
        max_bound = 0.5 * (1.0 - self.t_ret) * (self.t_ret ** (self.N_act - 1))
        if theta is None:
            self.theta = 0.5 * max_bound  # middle of admissible positive interval
        else:
            self.theta = float(theta)
        if not (0.0 < self.theta < max_bound):
            raise ValueError(f"theta={self.theta} must lie in (0, {max_bound}) for positivity")

        self.Z = [
            sum(math.comb(n, k) * self.t_seq[k] for k in range(n + 1))
            for n in range(self.N_act + 2)
        ]

    @staticmethod
    def M_matrix(t_ret, r_val):
        return 0.5 * np.array(
            [
                [1.0 + r_val + t_ret, 1.0 - r_val - t_ret],
                [1.0 + r_val - t_ret, 1.0 - r_val + t_ret],
            ],
            dtype=np.float64,
        )

    def m_root(self, adj):
        n = adj.shape[0]
        min_cnt = int(np.sum(np.sum(adj, axis=0) == 0)) if n > 0 else 0
        comp = sum(1.0 / self.Z[j] for j in range(n))
        return float(min_cnt) - comp

    def r_coeff(self, n, is_empty_ideal):
        if n >= self.N_act:
            raise ValueError(f"Parent size n={n} exceeds declared horizon N_act={self.N_act}")
        ind = 1.0 if is_empty_ideal else 0.0
        return self.theta * (self.t_ret ** (-n)) * (ind - (1.0 / self.Z[n]))

    def branch_matrix(self, adj, S):
        n = adj.shape[0]
        q_val = _csg_ideal_prob_exact(adj, S, self.t_seq)
        r_val = self.r_coeff(n, len(S) == 0)
        return q_val * self.M_matrix(self.t_ret, r_val)


def verify_active_root_martingale_law():
    """
    Exhaustively audits Theorem 2A at N_act = 8 and N_act = 12 using Log-Quadratic CSG
    q_LQ(0.20, 0.20) across all 3,644 diamonds (1 <= |C| <= 4, endpoints up to 6), plus
    multi-step trajectory telescoping and sampled diamonds up to n = 10 < N_act = 12.
    """
    t_logq = [(0.20 ** k) * (0.20 ** (k * (k - 1) // 2)) for k in range(16)]
    posets_by_n = {n: [] for n in range(1, 6)}
    for n_val, C_low in generate_naturally_ordered_posets(5):
        posets_by_n[n_val].append(C_low.T > 0.5)

    u_vec = np.array([0.5, 0.5], dtype=np.float64)
    v_vec = np.array([0.5, -0.5], dtype=np.float64)
    W = np.column_stack([u_vec, v_vec])
    W_inv = np.linalg.inv(W)
    ones = np.ones(2, dtype=np.float64)

    out_by_horizon = {}
    for N_act in (8, 12):
        law = ActiveRootMartingaleLaw(t_logq, t_ret=0.75, N_act=N_act)

        min_entry = float("inf")
        max_row_norm_err = 0.0
        max_uniform_anchor_err = 0.0
        max_martingale_err = 0.0
        diamond_violations = 0
        max_diamond_mat_err = 0.0
        total_diamonds = 0

        # Check empty parent n = 0
        adj0 = np.zeros((0, 0), dtype=bool)
        A0 = law.branch_matrix(adj0, frozenset())
        min_entry = min(min_entry, float(np.min(A0)))
        max_row_norm_err = max(max_row_norm_err, float(np.max(np.abs(ones @ A0 - ones))))
        max_uniform_anchor_err = max(max_uniform_anchor_err, float(np.max(np.abs(A0 @ u_vec - u_vec))))

        for n in (1, 2, 3, 4, 5):
            for adj in posets_by_n[n]:
                ideals = _get_ideals_adj(adj)
                row_sum = np.zeros((2, 2), dtype=np.float64)
                mart_lhs = 0.0
                for S in ideals:
                    A_S = law.branch_matrix(adj, S)
                    min_entry = min(min_entry, float(np.min(A_S)))
                    row_sum += A_S
                    q_S = _csg_ideal_prob_exact(adj, S, t_logq)
                    max_uniform_anchor_err = max(
                        max_uniform_anchor_err, float(np.max(np.abs(A_S @ u_vec - q_S * u_vec)))
                    )
                    mart_lhs += q_S * law.m_root(_extend_poset_adj(adj, S))
                max_row_norm_err = max(max_row_norm_err, float(np.max(np.abs(ones @ row_sum - ones))))
                max_martingale_err = max(max_martingale_err, abs(mart_lhs - law.m_root(adj)))

        # Exhaustive 3,644 diamonds on 1 <= |C| <= 4
        for n in (1, 2, 3, 4):
            for adj in posets_by_n[n]:
                ideals = _get_ideals_adj(adj)
                for S in ideals:
                    adj_x = _extend_poset_adj(adj, S)
                    A_CS = law.branch_matrix(adj, S)
                    for T in ideals:
                        adj_y = _extend_poset_adj(adj, T)
                        A_CT = law.branch_matrix(adj, T)
                        A_Cx_T = law.branch_matrix(adj_x, T)
                        A_Cy_S = law.branch_matrix(adj_y, S)

                        total_diamonds += 1
                        diff = float(np.max(np.abs((A_Cx_T @ A_CS) - (A_Cy_S @ A_CT))))
                        max_diamond_mat_err = max(max_diamond_mat_err, diff)
                        if diff > 1e-14:
                            diamond_violations += 1

        # Multi-step telescoping & higher-n diamond checks up to N_act (e.g., n = N_act - 2)
        rng = np.random.default_rng(20260820 + N_act)
        max_telescope_err = 0.0
        high_n_diamond_violations = 0
        for _ in range(25):
            adj_cur = np.zeros((0, 0), dtype=bool)
            M_prod = np.eye(2, dtype=np.float64)
            m0_val = law.m_root(adj_cur)
            for step_n in range(N_act):
                # Pick random parent subset B in {0..step_n-1} to form an actual ideal
                k_draw = int(rng.integers(0, min(3, step_n) + 1))
                chosen = rng.choice(step_n, size=k_draw, replace=False) if k_draw > 0 else []
                S_set = set()
                for b in chosen:
                    S_set.add(int(b))
                    for u in range(step_n):
                        if adj_cur[u, int(b)]:
                            S_set.add(u)
                S = frozenset(S_set)
                r_step = law.r_coeff(step_n, len(S) == 0)
                M_prod = law.M_matrix(law.t_ret, r_step) @ M_prod

                # At step_n == N_act - 2, check an explicit diamond on this large poset!
                if step_n == N_act - 2:
                    T_set = frozenset()  # incomparable empty ideal vs S
                    r_CS = law.r_coeff(step_n, len(S) == 0)
                    r_CT = law.r_coeff(step_n, True)
                    r_CxT = law.r_coeff(step_n + 1, True)
                    r_CyS = law.r_coeff(step_n + 1, len(S) == 0)
                    # Check exact M-product equality across diamond at n = N_act - 2
                    m_diff = float(np.max(np.abs(
                        (law.M_matrix(law.t_ret, r_CxT) @ law.M_matrix(law.t_ret, r_CS))
                        - (law.M_matrix(law.t_ret, r_CyS) @ law.M_matrix(law.t_ret, r_CT))
                    )))
                    if m_diff > 1e-14:
                        high_n_diamond_violations += 1

                adj_cur = _extend_poset_adj(adj_cur, S)

            # Verify exact W^{-1} M_prod W == [[1, theta * (M_root(E) - M_root(empty))], [0, t^{N_act}]]
            conj = W_inv @ M_prod @ W
            target = np.array(
                [
                    [1.0, law.theta * (law.m_root(adj_cur) - m0_val)],
                    [0.0, law.t_ret ** N_act],
                ],
                dtype=np.float64,
            )
            max_telescope_err = max(max_telescope_err, float(np.max(np.abs(conj - target))))

        # Exact active update contrast at step n = 1 (singleton P_1 = {0}, chain event S = {0})
        adj1 = np.zeros((1, 1), dtype=bool)
        S_chain = frozenset([0])
        delta0 = np.array([1.0, 0.0], dtype=np.float64)
        delta1 = np.array([0.0, 1.0], dtype=np.float64)
        K_empty = A0  # since q(empty, empty) = 1 and r_empty = 0, T_empty = A0 = M_t(0)
        A1_chain = law.branch_matrix(adj1, S_chain)

        p_d0 = float(ones @ (A1_chain @ delta0))
        p_d1 = float(ones @ (A1_chain @ delta1))
        p_Kd0 = float(ones @ (A1_chain @ (K_empty @ delta0)))
        delta_current = p_d0 - p_d1
        delta_update = p_Kd0 - p_d0
        expected_ratio = -0.5 * (1.0 - law.t_ret)

        # Static-seed diagonal control (T = I => K_diag = I => K_diag delta0 == delta0 => update == 0)
        delta_update_static_seed_ctrl = float(ones @ (A1_chain @ delta0) - p_d0)
        # Forward-only uncoupled control (r = 0 => A_ctrl = q M_t(0) => p_ctrl(rho) = q for all rho)
        q1_chain = _csg_ideal_prob_exact(adj1, S_chain, t_logq)
        A1_fwd = q1_chain * law.M_matrix(law.t_ret, 0.0)
        delta_update_forward_ctrl = float(ones @ (A1_fwd @ (K_empty @ delta0)) - ones @ (A1_fwd @ delta0))

        out_by_horizon[str(N_act)] = {
            "N_act": N_act,
            "t_ret": law.t_ret,
            "theta": law.theta,
            "min_branch_matrix_entry": min_entry,
            "max_row_normalization_err": max_row_norm_err,
            "max_uniform_anchor_err": max_uniform_anchor_err,
            "max_martingale_err": max_martingale_err,
            "total_diamonds_n_le_4": total_diamonds,
            "diamond_violations_n_le_4": diamond_violations,
            "max_diamond_matrix_err": max_diamond_mat_err,
            "high_n_sampled_diamond_violations": high_n_diamond_violations,
            "max_trajectory_telescope_err": max_telescope_err,
            "step1_chain_delta_current": delta_current,
            "step1_chain_delta_update": delta_update,
            "update_over_current_ratio": delta_update / delta_current,
            "analytic_ratio_minus_half_one_minus_t": expected_ratio,
            "static_seed_control_delta_update": delta_update_static_seed_ctrl,
            "forward_only_control_delta_update": delta_update_forward_ctrl,
        }

    return out_by_horizon


def verify_two_mode_source_instrument_and_non_mixture():
    """
    Verifies Theorem 2B:
      1. Exact CPTP trace preservation sum_S K_{C,S}^dagger K_{C,S} = I_2 and exact 2x2
         complex operator diamond commutation K_{C+x_S, T} K_{C, S} = K_{C+y_T, S} K_{C, T}
         across all 3,644 diamonds (1 <= |C| <= 4).
      2. Intervention non-factorization at identical committed prefix C_{n_0}: U_id vs U_X
         produce distinct conditional empty-birth probabilities 1/Z_{n_0}^{(0)} != 1/Z_{n_0}^{(1)}.
      3. Single-intervened joint (prefix, terminal) distribution violates EVERY time-homogeneous
         static CSG mixture int P_t d mu(t) over all t in [0, infty)^infty via the exact
         isomorphism-invariant cross-event identity:
             P_mu(E_post(n_0)) / P_mu(E_pre(n_0)) == 2 / (n_0 - 1),
         whereas the intervened law gives (2 / (n_0 - 1)) * (c_1 / c_0) = 5 / (n_0 - 1).
    """
    c0, q0 = 0.20, 0.20
    c1, q1 = 0.50, 0.35
    omega0, omega1 = 0.25, 0.85
    t0_seq = [(c0 ** k) * (q0 ** (k * (k - 1) // 2)) for k in range(12)]
    t1_seq = [(c1 ** k) * (q1 ** (k * (k - 1) // 2)) for k in range(12)]

    posets_by_n = {n: [] for n in range(1, 5)}
    for n_val, C_low in generate_naturally_ordered_posets(4):
        posets_by_n[n_val].append(C_low.T > 0.5)

    def kraus_op(adj, S):
        p0 = _csg_ideal_prob_exact(adj, S, t0_seq)
        p1 = _csg_ideal_prob_exact(adj, S, t1_seq)
        dphi = 1.0 + float(len(S))
        k00 = math.sqrt(p0) * complex(math.cos(-omega0 * dphi), math.sin(-omega0 * dphi))
        k11 = math.sqrt(p1) * complex(math.cos(-omega1 * dphi), math.sin(-omega1 * dphi))
        return np.array([[k00, 0.0j], [0.0j, k11]], dtype=np.complex128)

    max_cptp_err = 0.0
    max_op_diamond_err = 0.0
    op_diamond_violations = 0
    total_diamonds = 0

    for n in (1, 2, 3, 4):
        for adj in posets_by_n[n]:
            ideals = _get_ideals_adj(adj)
            k_sum = np.zeros((2, 2), dtype=np.complex128)
            k_cache = {}
            for S in ideals:
                K_S = kraus_op(adj, S)
                k_cache[S] = K_S
                k_sum += K_S.conj().T @ K_S
            max_cptp_err = max(max_cptp_err, float(np.max(np.abs(k_sum - np.eye(2)))))

            for S in ideals:
                adj_x = _extend_poset_adj(adj, S)
                for T in ideals:
                    adj_y = _extend_poset_adj(adj, T)
                    total_diamonds += 1
                    K_Cx_T = kraus_op(adj_x, T)
                    K_Cy_S = kraus_op(adj_y, S)
                    diff = float(np.max(np.abs((K_Cx_T @ k_cache[S]) - (K_Cy_S @ k_cache[T]))))
                    max_op_diamond_err = max(max_op_diamond_err, diff)
                    if diff > 1e-14:
                        op_diamond_violations += 1

    # Exact algebraic non-mixture audit at n0 in {2, 3, 4} by full trajectory enumeration!
    non_mixture_checks = []
    for n0 in (2, 3, 4):
        # Enumerate ALL growth trajectories from P_1 = {0} up to P_{n0 + 1} (size n0 + 1)
        # under intervened law (q^{(0)} for n < n0, U_X flip to q^{(1)} at n = n0)
        # and verify against arbitrary 3-component test mixture of static CSG laws!
        trajectories = [(np.zeros((1, 1), dtype=bool), 1.0, [1.0, 1.0, 1.0], None)]
        mix_t_seqs = [
            [(0.15 ** k) * (0.10 ** (k * (k - 1) // 2)) for k in range(10)],
            [(0.35 ** k) * (0.25 ** (k * (k - 1) // 2)) for k in range(10)],
            [(0.70 ** k) / math.factorial(k) for k in range(10)],
        ]
        mix_weights = [0.45, 0.35, 0.20]

        for step_n in range(1, n0 + 1):
            nxt_trajs = []
            for adj_p, w_int, w_mix_list, c_n0_edges in trajectories:
                rec_n0 = int(np.sum(adj_p)) if step_n == n0 else c_n0_edges
                for S in _get_ideals_adj(adj_p):
                    adj_c = _extend_poset_adj(adj_p, S)
                    q_step_int = _csg_ideal_prob_exact(
                        adj_p, S, t0_seq if step_n < n0 else t1_seq
                    )
                    nxt_mix = [
                        wm * _csg_ideal_prob_exact(adj_p, S, mts)
                        for wm, mts in zip(w_mix_list, mix_t_seqs)
                    ]
                    nxt_trajs.append((adj_c, w_int * q_step_int, nxt_mix, rec_n0))
            trajectories = nxt_trajs

        # Event E_pre(n0): C_1(C_{n0}) == 1 and C_1(C_{n0+1}) == 1 (isomorphism class C_2 + A_{n0-1})
        # Event E_post(n0): C_1(C_{n0}) == 0 and C_1(C_{n0+1}) == 1 (isomorphism class C_2 + A_{n0-1})
        # Note: a poset with C_1 == 1 has ONLY ONE unlabeled isomorphism class: K_2 disjoint union isolated vertices!
        p_int_pre = 0.0
        p_int_post = 0.0
        p_mix_pre = 0.0
        p_mix_post = 0.0
        total_int_mass = 0.0

        for adj_end, w_int, w_mix_list, e_n0 in trajectories:
            total_int_mass += w_int
            e_end = int(np.sum(adj_end))
            w_mix = sum(mw * wm for mw, wm in zip(mix_weights, w_mix_list))
            if e_n0 == 1 and e_end == 1:
                p_int_pre += w_int
                p_mix_pre += w_mix
            elif e_n0 == 0 and e_end == 1:
                p_int_post += w_int
                p_mix_post += w_mix

        universal_static_ratio = 2.0 / float(n0 - 1)
        realized_mix_ratio = p_mix_post / p_mix_pre
        intervened_ratio = p_int_post / p_int_pre
        analytic_intervened_ratio = universal_static_ratio * (c1 / c0)

        non_mixture_checks.append({
            "n0": n0,
            "N_terminal": n0 + 1,
            "total_intervened_probability_mass": total_int_mass,
            "universal_static_mixture_ratio": universal_static_ratio,
            "arbitrary_3component_mixture_ratio": realized_mix_ratio,
            "intervened_UX_ratio": intervened_ratio,
            "analytic_intervened_ratio": analytic_intervened_ratio,
            "non_mixture_discrepancy": intervened_ratio - universal_static_ratio,
        })

    # Same-prefix conditional jump at n0 = 128
    log_z0, _ = compute_log_partition_sequence(128, "log_quadratic", {"c": c0, "q": q0})
    log_z1, _ = compute_log_partition_sequence(128, "log_quadratic", {"c": c1, "q": q1})
    p_empty_id_128 = math.exp(-float(log_z0[128]))
    p_empty_ux_128 = math.exp(-float(log_z1[128]))

    return {
        "total_diamonds_n_le_4": total_diamonds,
        "max_cptp_trace_err": max_cptp_err,
        "operator_diamond_violations": op_diamond_violations,
        "max_operator_diamond_err": max_op_diamond_err,
        "same_prefix_n128_p_empty_id": p_empty_id_128,
        "same_prefix_n128_p_empty_UX": p_empty_ux_128,
        "non_mixture_exact_enumeration_checks": non_mixture_checks,
    }


# =============================================================================
# SECTION 3: PILLAR 3 — PAIRED 3-ARM SOURCE-PERTURBATION & RECOIL EXPERIMENT
# =============================================================================

def _exact_log_ideal_prob(n, s_size, d_max_in_s, log_z_n, log_c, log_q, lgam):
    """
    Computes exact log q(C_n, S) for Log-Quadratic CSG from (n, |S|, |Max(S)|):
        q(C_n, S) = Z_n^{-1} sum_{j=0}^{p} binom(p, j) c^{d+j} q^{binom(d+j, 2)},
    where d = |Max(S)| and p = |S| - d.
    """
    d = int(d_max_in_s)
    p = int(s_size) - d
    j_hi = min(p, 64)
    js = np.arange(j_hi + 1, dtype=np.int64)
    ks = d + js
    lw = (
        lgam[p]
        - lgam[js]
        - lgam[p - js]
        + ks * log_c
        + 0.5 * ks * (ks - 1) * log_q
    )
    m_lw = float(np.max(lw))
    return m_lw + math.log(float(np.sum(np.exp(lw - m_lw)))) - float(log_z_n)


def _compute_pillar3_arm_readouts(C, marks, u_src, u_far, rho_N, rng_eval):
    """
    Computes operational downstream clock-tick, causal-focusing, matched-m interval,
    coarse-anchor comparability, and residual recoil readouts on a realized poset C_N.
    """
    N = int(C.shape[0])

    # 1. Downstream inclusive future cone & longest directed chain from u_src (and u_far)
    def source_cone_and_clock(u_anchor, compute_intervals=True):
        fut_nodes = [u_anchor] + list(np.nonzero(C[:, u_anchor] == 1)[0])
        f_vol = len(fut_nodes)
        if f_vol <= 1:
            return {
                "cone_volume": 1,
                "l_max_ticks": 0,
                "mean_downstream_h": 0.0,
                "downstream_r2_ge4": None,
                "matched_m12_24_r2": None,
                "matched_m12_24_h_over_m": None,
                "matched_m12_24_ell_link": None,
                "matched_m12_24_count": 0,
            }

        # Longest chain length in edges starting at u_anchor inside J^+[u_anchor]
        sub_cone = C[np.ix_(fut_nodes, fut_nodes)]
        dp = np.zeros(f_vol, dtype=np.int32)
        for i in range(1, f_vol):
            preds = sub_cone[i, :i] == 1
            if np.any(preds):
                dp[i] = 1 + int(np.max(dp[:i][preds]))
        l_max = int(np.max(dp))

        if not compute_intervals:
            return {
                "cone_volume": f_vol,
                "l_max_ticks": l_max,
                "mean_downstream_h": 0.0,
                "downstream_r2_ge4": None,
                "matched_m12_24_r2": None,
                "matched_m12_24_h_over_m": None,
                "matched_m12_24_ell_link": None,
                "matched_m12_24_count": 0,
            }

        h_vals_all = []
        r2_ge4 = []
        m12_24_r2 = []
        m12_24_hm = []
        m12_24_ll = []

        # Sample up to 40 downstream receipts v > u_anchor if large, else evaluate all
        v_indices = np.arange(1, f_vol)
        if v_indices.shape[0] > 40:
            eval_v = np.sort(rng_eval.choice(v_indices, size=40, replace=False))
        else:
            eval_v = v_indices

        for idx_v in eval_v:
            int_idx = np.nonzero(sub_cone[idx_v, 1:idx_v] == 1)[0] + 1
            m_int = int(int_idx.shape[0])
            if m_int == 0:
                h_vals_all.append(0)
            elif m_int == 1:
                h_vals_all.append(1)
            else:
                obs = compute_interval_five_observables(sub_cone[np.ix_(int_idx, int_idx)])
                h_int = int(round(obs["h_over_m"] * m_int))
                h_vals_all.append(h_int)
                if m_int >= 4:
                    r2_ge4.append(obs["r2"])
                if 12 <= m_int <= 24:
                    m12_24_r2.append(obs["r2"])
                    m12_24_hm.append(obs["h_over_m"])
                    m12_24_ll.append(obs["ell_link"])

        return {
            "cone_volume": f_vol,
            "l_max_ticks": l_max,
            "mean_downstream_h": float(np.mean(h_vals_all)) if h_vals_all else 0.0,
            "downstream_r2_ge4": float(np.mean(r2_ge4)) if r2_ge4 else None,
            "matched_m12_24_r2": float(np.mean(m12_24_r2)) if m12_24_r2 else None,
            "matched_m12_24_h_over_m": float(np.mean(m12_24_hm)) if m12_24_hm else None,
            "matched_m12_24_ell_link": float(np.mean(m12_24_ll)) if m12_24_ll else None,
            "matched_m12_24_count": len(m12_24_r2),
        }

    src_data = source_cone_and_clock(u_src, compute_intervals=True)
    far_data = source_cone_and_clock(u_far, compute_intervals=False) if u_far is not None else None

    # Also evaluate post-n0 matched-cardinality bulk intervals m in [12, 24] across the post-n0 slab
    C_f = C.astype(np.float32)
    C2 = np.rint(C_f @ C_f).astype(np.int32)
    bv12, bu12 = np.nonzero((C == 1) & (C2 >= 12) & (C2 <= 24))
    post_m12_r2, post_m12_hm, post_m12_ll = [], [], []
    if bv12.shape[0] > 0:
        if bv12.shape[0] > 40:
            sel = rng_eval.choice(bv12.shape[0], size=40, replace=False)
            ev_v, ev_u = bv12[sel], bu12[sel]
        else:
            ev_v, ev_u = bv12, bu12
        for v, u in zip(ev_v, ev_u):
            vi, ui = int(v), int(u)
            zs = (ui + 1) + np.nonzero(C[vi, ui + 1 : vi] & C[ui + 1 : vi, ui])[0]
            obs = compute_interval_five_observables(C[np.ix_(zs, zs)])
            post_m12_r2.append(obs["r2"])
            post_m12_hm.append(obs["h_over_m"])
            post_m12_ll.append(obs["ell_link"])

    # Coarse-grained anchor poset Pi_A(C_N) comparability
    anc_idx = np.nonzero(marks[:N] == 1)[0]
    n_anc = int(anc_idx.shape[0])
    if n_anc >= 2:
        sub_anc = C[np.ix_(anc_idx, anc_idx)]
        coarse_r2 = float(np.sum(sub_anc)) / (n_anc * (n_anc - 1) / 2.0)
    else:
        coarse_r2 = 0.0

    global_r2 = float(np.sum(C)) / (N * (N - 1) / 2.0)

    return {
        "global_r2": global_r2,
        "coarse_anchor_count": n_anc,
        "coarse_anchor_r2": coarse_r2,
        "src_cone_volume": src_data["cone_volume"],
        "src_l_max_ticks": src_data["l_max_ticks"],
        "src_mean_downstream_h": src_data["mean_downstream_h"],
        "src_downstream_r2_ge4": src_data["downstream_r2_ge4"],
        "far_cone_volume": far_data["cone_volume"] if far_data else None,
        "far_l_max_ticks": far_data["l_max_ticks"] if far_data else None,
        "matched_m12_24_r2": float(np.mean(post_m12_r2)) if post_m12_r2 else None,
        "matched_m12_24_h_over_m": float(np.mean(post_m12_hm)) if post_m12_hm else None,
        "matched_m12_24_ell_link": float(np.mean(post_m12_ll)) if post_m12_ll else None,
        "residual_p1_excited": float(np.real(rho_N[1, 1])),
        "residual_coherence_abs": float(np.abs(rho_N[0, 1])),
        "residual_coherence_complex": [float(np.real(rho_N[0, 1])), float(np.imag(rho_N[0, 1]))],
    }


def _paired_diff_stats(vals_y, vals_x):
    """Computes paired difference statistics (mean, std, sem, t_stat) on matched runs."""
    diffs = np.array([y - x for y, x in zip(vals_y, vals_x) if (y is not None and x is not None)], dtype=np.float64)
    m_cnt = int(diffs.shape[0])
    if m_cnt == 0:
        return {"n_pairs": 0, "mean": None, "std": None, "sem": None, "t_stat": None}
    mean_d = float(np.mean(diffs))
    if m_cnt < 2:
        return {"n_pairs": m_cnt, "mean": mean_d, "std": 0.0, "sem": 0.0, "t_stat": 0.0}
    std_d = float(np.std(diffs, ddof=1))
    sem_d = std_d / math.sqrt(m_cnt)
    t_stat = (mean_d / sem_d) if sem_d > 1e-15 else (None if abs(mean_d) > 0 else 0.0)
    return {
        "n_pairs": m_cnt,
        "mean": mean_d,
        "std": std_d,
        "sem": sem_d,
        "t_stat": t_stat,
    }


def run_pillar3_paired_source_experiment(
    n0=128,
    horizons=(512, 1024),
    num_runs=40,
    p_anc=0.125,
    omega0=0.25,
    omega1=0.85,
    seed=20260803,
):
    """
    Executes Pillar 3: Paired 3-Arm Source-Perturbation to Clock-Tick & Nested-Interval
    Focusing Bridge from IDENTICAL committed prefixes C_{n0} (n0 = 128) evolved to
    N = 512 and N = 1024 across M = 40 paired runs:
      - Arm A: Unperturbed Reference Baseline (Z_{n0} = |0><0|, coupled law)
      - Arm B_p10 / Arm B_p05: Uncoupled Forward-Only Control (evolve_residual excites
        |1><1| or coherent |+><+|, with q_ctrl^{(1)} = q^{(0)})
      - Arm C_p10: Nested Active Source-Coupled Evolution (evolve_residual full flip U_X:
        |0><0| -> |1><1| under q^{(0)} = q_LQ(0.20,0.20), q^{(1)} = q_LQ(0.50,0.35))
      - Arm C_p05: Nested Active Coherent Superposition (evolve_residual U_H:
        |0><0| -> |+><+|, testing both downstream structural response AND Bayesian
        residual recoil / single-history decoherence!).
    """
    t_start = time.time()
    max_N = max(horizons)
    c0, q0 = 0.20, 0.20
    c1, q1 = 0.50, 0.35

    lgam0, ks0, k_term0, k_cap0, cdf0 = _precompute_csg_tables(max_N, "log_quadratic", {"c": c0, "q": q0})
    _, ks1, k_term1, k_cap1, cdf1 = _precompute_csg_tables(max_N, "log_quadratic", {"c": c1, "q": q1})
    log_z0, _ = compute_log_partition_sequence(max_N, "log_quadratic", {"c": c0, "q": q0})
    log_z1, _ = compute_log_partition_sequence(max_N, "log_quadratic", {"c": c1, "q": q1})
    log_c0, log_q0 = math.log(c0), math.log(q0)
    log_c1, log_q1 = math.log(c1), math.log(q1)

    arm_names = ("arm_A_baseline", "arm_B_uncoupled_p05", "arm_B_uncoupled_p10", "arm_C_coupled_p10", "arm_C_coherent_p05")
    per_horizon_runs = {str(H): {an: [] for an in arm_names} for H in horizons}

    def evolve_suffix(C_prefix, marks_full, rho_init, coupled, crn_streams):
        """
        Evolves (C_{n0}, rho_init) from n = n0 to max_N using exact marginal-preserving
        Strassen common random numbers (u_mode_arr, u_k_arr, u_prio_mat):
          - Arm A and Arm B share bit-for-bit identical realizations C_N;
          - Each arm's marginal transition kernel is 100% exact Rideout-Sorkin CSG.
        """
        u_mode_arr, u_k_arr, u_prio_mat = crn_streams
        C_work = np.zeros((max_N, max_N), dtype=np.uint8)
        C_work[:n0, :n0] = C_prefix
        rho = np.array(rho_init, dtype=np.complex128)
        snapshots = {}

        for n in range(n0, max_N):
            step_i = n - n0
            p1_cur = float(np.real(rho[1, 1]))
            use_mode_1 = bool(coupled and (u_mode_arr[step_i] < p1_cur))

            cdf_cur = cdf1[n] if use_mode_1 else cdf0[n]
            klim = min(n, k_cap1 if use_mode_1 else k_cap0)
            K = int(np.searchsorted(cdf_cur, u_k_arr[step_i], side="right"))
            if K > klim:
                K = klim

            if K == 1:
                b0 = int(np.argmin(u_prio_mat[step_i, :n]))
                C_work[n, :b0] = C_work[b0, :b0]
                C_work[n, b0] = 1
                max_cnt = 1
            elif K == 2:
                prow = u_prio_mat[step_i, :n]
                b0 = int(np.argmin(prow))
                saved = float(prow[b0])
                prow[b0] = 2.0
                b1 = int(np.argmin(prow))
                prow[b0] = saved
                row = C_work[b0, :n] | C_work[b1, :n]
                row[b0] = 1
                row[b1] = 1
                C_work[n, :n] = row
                if b0 < b1:
                    max_cnt = 1 if C_work[b1, b0] == 1 else 2
                else:
                    max_cnt = 1 if C_work[b0, b1] == 1 else 2
            elif K > 2:
                B = np.argpartition(u_prio_mat[step_i, :n], K - 1)[:K]
                sub_rows = C_work[B, :n]
                row = np.bitwise_or.reduce(sub_rows, axis=0)
                row[B] = 1
                C_work[n, :n] = row
                sub_B = C_work[np.ix_(B, B)]
                max_cnt = int(np.sum(np.sum(sub_B, axis=0) == 0))
            else:
                max_cnt = 0

            s_size = int(np.sum(C_work[n, :n]))
            dphi = 1.0 + float(s_size)
            phase_diff = -(omega0 - omega1) * dphi
            ph = complex(math.cos(phase_diff), math.sin(phase_diff))

            if not coupled:
                # L0 == L1 => diagonal populations invariant, off-diagonal accumulates phase
                rho = np.array(
                    [
                        [rho[0, 0], rho[0, 1] * ph],
                        [rho[1, 0] * ph.conjugate(), rho[1, 1]],
                    ],
                    dtype=np.complex128,
                )
            else:
                # Exact selective Kraus Bayesian update in log-space to prevent underflow
                ll0 = _exact_log_ideal_prob(n, s_size, max_cnt, log_z0[n], log_c0, log_q0, lgam0)
                ll1 = _exact_log_ideal_prob(n, s_size, max_cnt, log_z1[n], log_c1, log_q1, lgam0)
                m_ll = max(ll0, ll1)
                r0_s = math.exp(ll0 - m_ll)
                r1_s = math.exp(ll1 - m_ll)
                p00_new = float(np.real(rho[0, 0])) * r0_s
                p11_new = float(np.real(rho[1, 1])) * r1_s
                denom = p00_new + p11_new
                p01_new = rho[0, 1] * math.sqrt(r0_s * r1_s) * ph / denom
                rho = np.array(
                    [
                        [p00_new / denom, p01_new],
                        [p01_new.conjugate(), p11_new / denom],
                    ],
                    dtype=np.complex128,
                )

            N_cur = n + 1
            if N_cur in horizons:
                snapshots[N_cur] = (C_work[:N_cur, :N_cur].copy(), rho.copy())

        return snapshots

    rho_0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)
    rho_1 = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=np.complex128)
    rho_plus = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=np.complex128)

    prefix_r2s = []
    for run_idx in range(num_runs):
        rng_pre = np.random.default_rng(seed + 1000 * run_idx)
        C_pre, _, _ = sample_csg_fast(n0, "log_quadratic", {"c": c0, "q": q0}, rng_pre)
        marks = (rng_pre.random(max_N) < p_anc).astype(np.int8)
        prefix_r2s.append(float(np.sum(C_pre)) / (n0 * (n0 - 1) / 2.0))

        # Select maximal source anchor u_src in Max(C_{n0}) (deepest strict past, ties by index)
        max_cands = np.nonzero(np.sum(C_pre, axis=0) == 0)[0]
        past_counts = np.sum(C_pre[max_cands, :], axis=1)
        best_order = np.lexsort((max_cands, past_counts))
        u_src = int(max_cands[best_order[-1]])
        # Ensure u_src is marked as a coarse anchor as part of source preparation
        marks[u_src] = 1

        u_far = None
        if max_cands.shape[0] > 1:
            others = [int(x) for x in max_cands if int(x) != u_src]
            src_past = C_pre[u_src, :]
            overlaps = [int(np.sum(C_pre[x, :] & src_past)) for x in others]
            u_far = others[int(np.argmin(overlaps))]

        # Pre-draw Strassen common-random-numbers streams once for all 5 arms of this run
        rng_crn = np.random.default_rng(seed + 1000000 + run_idx)
        n_steps = max_N - n0
        crn_streams = (
            rng_crn.random(n_steps),
            rng_crn.random(n_steps),
            rng_crn.random((n_steps, max_N), dtype=np.float32),
        )

        snaps_A = evolve_suffix(C_pre, marks, rho_0, True, crn_streams)
        snaps_B05 = evolve_suffix(C_pre, marks, rho_plus, False, crn_streams)
        snaps_B10 = evolve_suffix(C_pre, marks, rho_1, False, crn_streams)
        snaps_C10 = evolve_suffix(C_pre, marks, rho_1, True, crn_streams)
        snaps_C05 = evolve_suffix(C_pre, marks, rho_plus, True, crn_streams)

        for H in horizons:
            h_key = str(H)
            C_A, rho_A = snaps_A[H]
            C_B05, rho_B05 = snaps_B05[H]
            C_B10, rho_B10 = snaps_B10[H]
            assert np.array_equal(C_B05, C_A) and np.array_equal(C_B10, C_A)

            rng_ev_A = np.random.default_rng(seed + 9000000 + 100 * H + run_idx)
            read_A = _compute_pillar3_arm_readouts(C_A, marks, u_src, u_far, rho_A, rng_ev_A)
            per_horizon_runs[h_key]["arm_A_baseline"].append(read_A)

            # Reuse bit-for-bit identical structural readouts on C_B05 == C_B10 == C_A
            for an_b, rho_b in (("arm_B_uncoupled_p05", rho_B05), ("arm_B_uncoupled_p10", rho_B10)):
                rb = dict(read_A)
                rb["residual_p1_excited"] = float(np.real(rho_b[1, 1]))
                rb["residual_coherence_abs"] = float(np.abs(rho_b[0, 1]))
                rb["residual_coherence_complex"] = [float(np.real(rho_b[0, 1])), float(np.imag(rho_b[0, 1]))]
                per_horizon_runs[h_key][an_b].append(rb)

            for an_c, sn_dict in (("arm_C_coupled_p10", snaps_C10), ("arm_C_coherent_p05", snaps_C05)):
                C_H, rho_H = sn_dict[H]
                rng_ev = np.random.default_rng(seed + 9000000 + 100 * H + run_idx)
                per_horizon_runs[h_key][an_c].append(
                    _compute_pillar3_arm_readouts(C_H, marks, u_src, u_far, rho_H, rng_ev)
                )

    # Summarize arms & paired contrasts at each horizon
    readout_metrics = (
        "src_l_max_ticks",
        "src_mean_downstream_h",
        "src_cone_volume",
        "src_downstream_r2_ge4",
        "far_l_max_ticks",
        "far_cone_volume",
        "matched_m12_24_r2",
        "matched_m12_24_h_over_m",
        "matched_m12_24_ell_link",
        "coarse_anchor_r2",
        "global_r2",
        "residual_p1_excited",
        "residual_coherence_abs",
    )

    horizons_summary = {}
    for H in horizons:
        h_key = str(H)
        arms_agg = {}
        for an in arm_names:
            rlist = per_horizon_runs[h_key][an]
            a_stat = {}
            for mk in readout_metrics:
                vals = [r[mk] for r in rlist if r[mk] is not None]
                a_stat[f"{mk}_mean"] = float(np.mean(vals)) if vals else None
                a_stat[f"{mk}_std"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
                if mk == "residual_p1_excited":
                    a_stat["residual_p1_var_between"] = float(np.var(vals, ddof=1)) if len(vals) > 1 else 0.0
            # Ensemble-averaged coherence |E[<0|Z_N|1>]|
            coh_c = [complex(r["residual_coherence_complex"][0], r["residual_coherence_complex"][1]) for r in rlist]
            a_stat["ensemble_mean_coherence_abs"] = float(abs(np.mean(coh_c)))
            arms_agg[an] = a_stat

        # Paired contrasts
        contrast_specs = [
            ("B_p05_minus_A", "arm_B_uncoupled_p05", "arm_A_baseline"),
            ("B_p10_minus_A", "arm_B_uncoupled_p10", "arm_A_baseline"),
            ("C_p10_minus_A", "arm_C_coupled_p10", "arm_A_baseline"),
            ("C_p10_minus_B_p10", "arm_C_coupled_p10", "arm_B_uncoupled_p10"),
            ("C_p05_minus_A", "arm_C_coherent_p05", "arm_A_baseline"),
            ("C_p05_minus_B_p05", "arm_C_coherent_p05", "arm_B_uncoupled_p05"),
        ]
        contrasts_agg = {}
        for cname, ay, ax in contrast_specs:
            ry = per_horizon_runs[h_key][ay]
            rx = per_horizon_runs[h_key][ax]
            contrasts_agg[cname] = {
                mk: _paired_diff_stats([r[mk] for r in ry], [r[mk] for r in rx])
                for mk in (
                    "src_l_max_ticks",
                    "src_mean_downstream_h",
                    "src_cone_volume",
                    "matched_m12_24_r2",
                    "matched_m12_24_h_over_m",
                    "coarse_anchor_r2",
                    "global_r2",
                    "residual_coherence_abs",
                )
            }

        horizons_summary[h_key] = {
            "arms": arms_agg,
            "paired_contrasts": contrasts_agg,
        }

    return {
        "parameters": {
            "n0": n0,
            "horizons": list(horizons),
            "num_runs": num_runs,
            "p_anc": p_anc,
            "q0_params": {"c": c0, "q": q0},
            "q1_params": {"c": c1, "q": q1},
            "omega0": omega0,
            "omega1": omega1,
            "seed": seed,
            "prefix_r2_mean": float(np.mean(prefix_r2s)),
            "prefix_r2_std": float(np.std(prefix_r2s, ddof=1)),
            "elapsed_seconds": time.time() - t_start,
        },
        "horizons": horizons_summary,
    }


def export_results_to_json(results, output_path):
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, allow_nan=False)
    print(f"Results successfully exported to: {output_path}")


if __name__ == "__main__":
    all_res = {
        "pillar1_holdout": run_pillar1_frozen_holdout_suite(),
        "pillar2_coarse_projection": verify_coarse_projection_theorems(),
        "pillar2_active_root_martingale": verify_active_root_martingale_law(),
        "pillar2_two_mode_non_mixture": verify_two_mode_source_instrument_and_non_mixture(),
        "pillar3_source_response": run_pillar3_paired_source_experiment(),
    }
    export_results_to_json(
        all_res, os.path.join(SCRIPT_DIR, "nested_regime_experiment_results.json")
    )
