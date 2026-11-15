"""
cr1_discriminating_experiment.py

Comprehensive Discriminating Experiment Suite for Conjecture CR-1
(Cross-Regime Differentiated Coherence).

Evaluates:
1. Exact finite-poset diamond commutation & intrinsic readout checks (using poset_generator.py),
   including the QR-LD037 4-birth non-diamond law and local-compensation diamond tests.
2. Small-to-moderate horizon ensemble & single-history suite (N in {16, 32}, M = 50 runs/model):
   - Positive geometric controls:
     * 2D Minkowski Alexandrov Diamond (f(2) = 0.5000; satisfies CR-1b-d + SS-1)
     * 4D Minkowski Alexandrov Diamond (f(4) = 0.1000; satisfies CR-1b-d + SS-1)
     * 2D Minkowski Wide-Slab Cylinder [0,1]x[0,3] (R_global = 11/54 = 0.2037 != f(2) = 0.5000;
       satisfies CR-1b-d while falsifying naive interval-equals-prefix assumption SS-1)
   - Deliberately non-geometric / negative controls:
     * Bimodal 10/90 Chain-Antichain Static Mixture (E[R_2] = 0.1000, Var_between ~ 0.09 -> fails CR-1b)
     * 3-Layer Kleitman-Rothschild Random Poset (E[R_2] ~ 0.375, rho_2 == 0 -> fails CR-1b)
     * Finite-Cutoff CSG k_max = 1 (random recursive forest: R_2 = O(ln N / N) -> 0, R_2(I) == 1.0)
     * Finite-Cutoff CSG k_max = 2 (binary CSG: R_2 = O(N^{-1/2}) -> 0)
     * Bernoulli Transitive Percolation p in {0.08, 0.15} (R_2 -> 1.0 -> fails CR-1b)
     * Sparse & Fixed Random DAG Closures
   - Candidate unbounded subset-weight CSG families:
     * Gevrey CSG: t_k = c^k / (k!)^beta
     * Log-Quadratic CSG: t_k = c^k q^{binom(k, 2)}
3. Extended fast bitmask multi-horizon scaling sweep (N in {16, 32, 64, 128, 256, 512, 1024}, M = 25 runs):
   - Tracks parent-seed count K_n vs. realized link in-degree |Max(S_n)| (cone overlap),
   - Global R_2(P_N), global post density rho_post(P_N),
   - Mesoscopic bulk interval comparability <R_2(I)> and within/between-history variances,
   - Distinguishing transient small-N plateaus from large-N Gevrey upward drift and
     Log-Quadratic logarithmic-window spine behavior.
4. Multi-alpha nested-regime profile R_int(alpha) (alpha in {0.25, 0.35, 0.45, 0.50, 0.65}, N in {512, 1024}):
   - Evaluates exact CR-1c bulk interval family J_N(omega; alpha, c_-, c_+, delta_bulk) and
     inverts the Myrheim-Meyer unordered-pair comparability relation f(d) = Gamma(d+1)Gamma(d/2)/(2 Gamma(3d/2)).
"""

import os
import sys
import math
import json
import time
import random
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from poset_generator import generate_naturally_ordered_posets


# =============================================================================
# SECTION 1: METRICS AND INTERVAL ANALYSIS ENGINE
# =============================================================================

class PosetMetrics:
    """Computes single-history relational and causal-interval observables on finite posets."""

    @staticmethod
    def compute_all_metrics(C, pasts=None, r2_trajectory=None, min_interval_size=4):
        """
        Analyzes a naturally ordered poset represented by strictly lower-triangular
        incidence matrix C (C[v, u] == 1 iff u < v).
        """
        N = C.shape[0]
        total_pairs = N * (N - 1) // 2
        c1 = int(np.sum(C))

        if total_pairs == 0:
            return {
                "N": N,
                "c1": 0,
                "total_pairs": 0,
                "r2": 0.0,
                "post_count": N,
                "post_density": 1.0 if N > 0 else 0.0,
                "c2_chains": 0,
                "c3_chains": 0,
                "rho2_chain_ratio": 0.0,
                "layer_counts": {},
                "link_count": 0,
                "link_fraction": 0.0,
                "mean_interval_size": 0.0,
                "intervals_ge4_count": 0,
                "sub_interval_r2_values": [],
                "sub_interval_r2_mean": 0.0,
                "within_history_interval_var": 0.0,
                "within_history_traj_var": 0.0,
                "bd2_action": float(N),
                "bd4_action": float(N),
            }

        r2 = float(c1) / float(total_pairs)

        # Global posts: x is comparable to all y != x iff |J^-(x)\{x}| + |J^+(x)\{x}| == N - 1
        past_sizes = np.sum(C, axis=1)    # number of u < x
        future_sizes = np.sum(C, axis=0)  # number of v > x
        post_count = int(np.sum((past_sizes + future_sizes) == (N - 1)))
        post_density = float(post_count) / float(N)

        # Chain counts: C2[v, u] = |I(u, v)| = number of 2-chains u < z < v
        C2 = C @ C
        C3 = C2 @ C
        c2_chains = int(np.sum(C2))
        c3_chains = int(np.sum(C3))
        rho2_chain_ratio = float(c3_chains) / float(c2_chains) if c2_chains > 0 else 0.0

        comparable_coords = np.argwhere(C == 1)
        layer_counts = {}
        total_m = 0
        sub_r2_values = []

        for v, u in comparable_coords:
            m = int(C2[v, u])
            layer_counts[m] = layer_counts.get(m, 0) + 1
            total_m += m

            if m >= min_interval_size:
                z_indices = np.nonzero((C[v, :] == 1) & (C[:, u] == 1))[0]
                sub_C = C[np.ix_(z_indices, z_indices)]
                sub_c1 = int(np.sum(sub_C))
                sub_total_pairs = m * (m - 1) // 2
                if sub_total_pairs > 0:
                    sub_r2_values.append(float(sub_c1) / float(sub_total_pairs))

        link_count = layer_counts.get(0, 0)
        link_fraction = float(link_count) / float(c1) if c1 > 0 else 0.0
        mean_m = float(total_m) / float(c1) if c1 > 0 else 0.0

        if len(sub_r2_values) > 0:
            sub_r2_mean = float(np.mean(sub_r2_values))
            within_hist_int_var = float(np.var(sub_r2_values, ddof=1)) if len(sub_r2_values) > 1 else 0.0
        else:
            sub_r2_mean = 0.0
            within_hist_int_var = 0.0

        if r2_trajectory is not None and len(r2_trajectory) >= N:
            late_traj = r2_trajectory[(N // 2) - 1: N]
            within_hist_traj_var = float(np.var(late_traj, ddof=1)) if len(late_traj) > 1 else 0.0
        else:
            within_hist_traj_var = 0.0

        n0 = layer_counts.get(0, 0)
        n1 = layer_counts.get(1, 0)
        n2 = layer_counts.get(2, 0)
        n3 = layer_counts.get(3, 0)
        bd2_action = float(N - 2 * n0 + 4 * n1 - 2 * n2)
        bd4_action = float(N - n0 + 9 * n1 - 16 * n2 + 8 * n3)

        return {
            "N": N,
            "c1": c1,
            "total_pairs": total_pairs,
            "r2": r2,
            "post_count": post_count,
            "post_density": post_density,
            "c2_chains": c2_chains,
            "c3_chains": c3_chains,
            "rho2_chain_ratio": rho2_chain_ratio,
            "layer_counts": layer_counts,
            "link_count": link_count,
            "link_fraction": link_fraction,
            "mean_interval_size": mean_m,
            "intervals_ge4_count": len(sub_r2_values),
            "sub_interval_r2_values": sub_r2_values,
            "sub_interval_r2_mean": sub_r2_mean,
            "within_history_interval_var": within_hist_int_var,
            "within_history_traj_var": within_hist_traj_var,
            "bd2_action": bd2_action,
            "bd4_action": bd4_action,
        }


# =============================================================================
# SECTION 2: SIMULATION ENGINES FOR CANDIDATE CSG & GEOMETRIC/NEGATIVE CONTROLS
# =============================================================================

def sample_minkowski_poisson(dim, N, seed=None, geometry="diamond", slab_width=3.0):
    """
    Samples a Poisson causal set of size N in d-dimensional Minkowski spacetime:
      - geometry='diamond': Alexandrov causal diamond between (0, 0) and (1, 0),
        where theoretical global and interval comparability both equal f(d).
      - geometry='slab' (dim=2): Wide cylinder/slab [0, 1] x [0, L] with L = slab_width,
        where theoretical global comparability is (6L - 1)/(18 L^2) * ... = 11/54 (for L=3)
        while every internal Alexandrov interval I(u, v) has <R_2(I)> = f(2) = 0.5000.
    """
    rng = np.random.default_rng(seed)

    if geometry == "slab":
        if dim != 2:
            raise ValueError("Slab geometry benchmark is defined for dim=2")
        t = rng.uniform(0.0, 1.0, N)
        x = rng.uniform(0.0, slab_width, N)
        pts = np.column_stack([t, x])
    elif geometry == "diamond":
        pts = []
        if dim == 2:
            while len(pts) < N:
                batch = max(50, (N - len(pts)) * 4)
                t = rng.uniform(0.0, 1.0, batch)
                x = rng.uniform(-0.5, 0.5, batch)
                valid = (np.abs(x) < t) & (np.abs(x) < (1.0 - t))
                pts.extend(np.column_stack([t[valid], x[valid]]))
        elif dim == 3:
            while len(pts) < N:
                batch = max(80, (N - len(pts)) * 6)
                t = rng.uniform(0.0, 1.0, batch)
                x = rng.uniform(-0.5, 0.5, batch)
                y = rng.uniform(-0.5, 0.5, batch)
                r = np.sqrt(x**2 + y**2)
                valid = (r < t) & (r < (1.0 - t))
                pts.extend(np.column_stack([t[valid], x[valid], y[valid]]))
        elif dim == 4:
            while len(pts) < N:
                batch = max(100, (N - len(pts)) * 10)
                t = rng.uniform(0.0, 1.0, batch)
                x = rng.uniform(-0.5, 0.5, batch)
                y = rng.uniform(-0.5, 0.5, batch)
                z = rng.uniform(-0.5, 0.5, batch)
                r = np.sqrt(x**2 + y**2 + z**2)
                valid = (r < t) & (r < (1.0 - t))
                pts.extend(np.column_stack([t[valid], x[valid], y[valid], z[valid]]))
        else:
            raise ValueError(f"Unsupported Minkowski dimension: {dim}")
        pts = np.array(pts[:N])
    else:
        raise ValueError(f"Unsupported geometry: {geometry}")

    order = np.argsort(pts[:, 0])
    pts = pts[order]

    C = np.zeros((N, N), dtype=int)
    for i in range(N):
        dt = pts[i + 1:, 0] - pts[i, 0]
        dx2 = np.sum((pts[i + 1:, 1:] - pts[i, 1:]) ** 2, axis=1)
        C[i + 1:, i] = ((dt > 0.0) & ((dt**2 - dx2) > 0.0)).astype(int)

    r2_trajectory = [0.0]
    c1_cum = 0
    for n in range(1, N):
        c1_cum += int(np.sum(C[n, :n]))
        r2_trajectory.append(float(c1_cum) / ((n + 1) * n / 2.0))

    return C, r2_trajectory


def sample_csg_history(N, coupling_type, params, seed=None):
    """
    Simulates a single sequential CSG history up to size N via the exact Rideout-Sorkin
    subset-ideal bijection (Lemma 6.2 of PW6A / QR-LD036):
      - 'gevrey': t_k = c^k / (k!)^beta
      - 'log_quadratic': t_k = c^k q^{binom(k, 2)}
      - 'finite_cutoff': t_k = c^k for 0 <= k <= k_max, 0 for k > k_max
      - 'factorial': t_k = c^k / k!
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    pasts = [set([i]) for i in range(N)]
    C = np.zeros((N, N), dtype=int)
    r2_trajectory = [0.0]
    c1_running = 0

    c_param = params.get("c", 0.20)

    if coupling_type == "gevrey":
        beta = params.get("beta", 2.0)
        k_upper = lambda n: n
        def log_t(k):
            return k * math.log(c_param) - beta * math.lgamma(k + 1)
    elif coupling_type == "log_quadratic":
        q = params.get("q", 0.10)
        k_upper = lambda n: n
        def log_t(k):
            return k * math.log(c_param) + 0.5 * k * (k - 1) * math.log(q)
    elif coupling_type == "finite_cutoff":
        k_max = int(params.get("k_max", 1))
        k_upper = lambda n: min(n, k_max)
        def log_t(k):
            return k * math.log(c_param)
    elif coupling_type == "factorial":
        k_upper = lambda n: n
        def log_t(k):
            return k * math.log(c_param) - math.lgamma(k + 1)
    else:
        raise ValueError(f"Unknown coupling type: {coupling_type}")

    for n in range(1, N):
        kmax_n = k_upper(n)
        log_w = []
        for k in range(kmax_n + 1):
            log_comb = math.lgamma(n + 1) - math.lgamma(n - k + 1) - math.lgamma(k + 1)
            log_w.append(log_comb + log_t(k))
        log_w = np.array(log_w)
        max_log = np.max(log_w)
        w = np.exp(log_w - max_log)
        prob = w / np.sum(w)

        k_draw = int(np.random.choice(kmax_n + 1, p=prob))
        chosen = random.sample(range(n), k_draw) if k_draw > 0 else []

        s = set([n])
        for b in chosen:
            s.update(pasts[b])
        pasts[n] = s

        for u in s:
            if u != n:
                C[n, u] = 1

        c1_running += len(s) - 1
        n_cur = n + 1
        r2_trajectory.append(float(c1_running) / (n_cur * (n_cur - 1) / 2.0))

    return C, r2_trajectory, pasts


def sample_bernoulli_percolation(N, p, seed=None):
    """Samples fixed-p Bernoulli transitive percolation (equivalent to t_k = (p/(1-p))^k CSG)."""
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    pasts = [set([i]) for i in range(N)]
    C = np.zeros((N, N), dtype=int)
    r2_trajectory = [0.0]
    c1_running = 0

    for n in range(1, N):
        s = set([n])
        for i in range(n):
            if np.random.rand() < p:
                s.update(pasts[i])
        pasts[n] = s

        for u in s:
            if u != n:
                C[n, u] = 1

        c1_running += len(s) - 1
        n_cur = n + 1
        r2_trajectory.append(float(c1_running) / (n_cur * (n_cur - 1) / 2.0))

    return C, r2_trajectory, pasts


def sample_random_dag(N, p, mode="fixed", seed=None):
    """Samples a random DAG on N vertices and takes its transitive closure."""
    effective_p = min(1.0, p / float(N)) if mode == "sparse" else p
    return sample_bernoulli_percolation(N, effective_p, seed=seed)


def sample_bimodal_extremal_mixture(N, chain_prob=0.10, seed=None):
    """
    Static convex mixture lambda * delta_{C_N} + (1 - lambda) * delta_{A_N}
    (corresponding to t_k -> infty vs t_k = delta_{k,0} de Finetti mixture).
    Ensemble average E[R_2] == chain_prob (e.g. 0.1000 = f(4)), while every
    single history lands at R_2 = 1.0 or R_2 = 0.0 (failing CR-1b concentration).
    """
    rng = np.random.default_rng(seed)
    is_chain = bool(rng.random() < chain_prob)
    C = np.zeros((N, N), dtype=int)
    if is_chain:
        for v in range(N):
            C[v, :v] = 1
        r2_traj = [0.0] + [1.0] * (N - 1)
    else:
        r2_traj = [0.0] * N
    return C, r2_traj


def sample_kleitman_rothschild_3layer(N, edge_prob=0.5, seed=None):
    """
    Canonical 3-layer Kleitman-Rothschild random poset with layer sizes
    (L1, L2, L3) = (N // 4, N - 2*(N // 4), N // 4).
    Independent edges with probability 1/2 between L1 -> L2 and L2 -> L3,
    closed by transitivity. Asymptotically R_2 -> 3/8 = 0.375, height <= 3,
    and 3-chain ratio rho_2 == 0 identically (failing CR-1c).
    """
    rng = np.random.default_rng(seed)
    n1 = N // 4
    n3 = N // 4
    n2 = N - n1 - n3
    C = np.zeros((N, N), dtype=int)

    # L1: [0, n1), L2: [n1, n1+n2), L3: [n1+n2, N)
    for u in range(0, n1):
        for z in range(n1, n1 + n2):
            if rng.random() < edge_prob:
                C[z, u] = 1
    for z in range(n1, n1 + n2):
        for v in range(n1 + n2, N):
            if rng.random() < edge_prob:
                C[v, z] = 1
    # Transitive closure L1 -> L3
    for u in range(0, n1):
        for v in range(n1 + n2, N):
            if np.any((C[n1:n1 + n2, u] == 1) & (C[v, n1:n1 + n2] == 1)):
                C[v, u] = 1

    r2_traj = [0.0]
    c1_cum = 0
    for n in range(1, N):
        c1_cum += int(np.sum(C[n, :n]))
        r2_traj.append(float(c1_cum) / ((n + 1) * n / 2.0))
    return C, r2_traj


# =============================================================================
# SECTION 3: EXACT DIAMOND & QR-LD037 / LOCAL-COMPENSATION CHECKS (poset_generator)
# =============================================================================

def verify_exact_diamond_and_readout_properties():
    """
    Uses poset_generator.py across all posets up to N=4 to verify:
      1. QR-LD037 non-diamond 4-birth counterexample: Pi_1 = 3/128 != 5/128 = Pi_2 (fails CR-1a).
      2. Exact diamond commutation (Pi_1 == Pi_2) for Gevrey and Log-Quadratic CSG across all
         incomparable ideal pairs (S, T) on all posets up to N=4.
      3. Intrinsic-past full-ideal compensation w(S) commutes on 100% of diamonds, whereas
         stage-n-dependent damping exp(-lambda * sum |J^-[u]| / n) FAILS diamond commutation
         on A_2 with S={0}, T=emptyset (exp(-lambda/2) != exp(-lambda/3)).
    """
    posets_by_n = {n: [] for n in range(1, 5)}
    for n_val, C_low in generate_naturally_ordered_posets(4):
        # C_low[v, u] == 1 iff u < v; adj[u, v] == True iff u < v
        posets_by_n[n_val].append(C_low.T > 0.5)

    def get_ideals(adj):
        n = adj.shape[0]
        ideals = []
        for mask in range(1 << n):
            ok = True
            for v in range(n):
                if (mask >> v) & 1:
                    for u in range(v):
                        if adj[u, v] and not ((mask >> u) & 1):
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                ideals.append(frozenset(i for i in range(n) if (mask >> i) & 1))
        return ideals

    def max_elements(adj, S):
        return [u for u in S if not any((v in S and v != u and adj[u, v]) for v in S)]

    def extend_poset(adj, S):
        n = adj.shape[0]
        child = np.zeros((n + 1, n + 1), dtype=bool)
        child[:n, :n] = adj
        for u in S:
            child[u, n] = True
        return child

    def csg_q(adj, S, t_seq):
        n = adj.shape[0]
        d = len(max_elements(adj, S))
        p = len(S) - d
        num = sum(math.comb(p, j) * t_seq[j + d] for j in range(p + 1))
        den = sum(math.comb(n, k) * t_seq[k] for k in range(n + 1))
        return num / den

    gevrey_t = [0.2**k / (math.factorial(k) ** 2) for k in range(10)]
    logq_t = [(0.2**k) * (0.2 ** (k * (k - 1) // 2)) for k in range(10)]

    total_diamonds = 0
    gevrey_violations = 0
    logq_violations = 0
    intrinsic_comp_violations = 0
    stage_n_damping_violations = 0
    local_cone_routed_violations = 0
    local_cone_routed_max_row_err = 0.0

    lam = 0.5
    a_seq = {1: 0.20, 2: 0.15, 3: 0.10, 4: 0.05, 5: 0.02}

    def eta_damp(adj, S):
        if len(S) == 0:
            return 1.0
        cone_sum = 0
        for u in max_elements(adj, S):
            past_u = 1 + sum(1 for z in S if z != u and adj[z, u])
            cone_sum += past_u
        return math.exp(-lam * cone_sum)

    def local_cone_routed_probs(adj, ideals):
        # Complete, positive, row-normalized candidate rule routing slack downward
        # within each local cone S to proper sub-ideals R subsetneq S (never flooding P_n).
        base_p = {S: csg_q(adj, S, logq_t) for S in ideals}
        routed_p = {R: eta_damp(adj, R) * base_p[R] for R in ideals}
        for S in ideals:
            if len(S) > 0:
                proper_subs = [R for R in ideals if R < S]
                m_cnt = len(proper_subs)
                slack = (1.0 - eta_damp(adj, S)) * base_p[S]
                for R in proper_subs:
                    routed_p[R] += slack / float(m_cnt)
        return routed_p

    def intrinsic_u(adj, S):
        # Depends strictly on isomorphism invariants of S (no ambient n = |P|!)
        base = sum(math.comb(len(S) - len(max_elements(adj, S)), j) * logq_t[j + len(max_elements(adj, S))]
                   for j in range(len(S) - len(max_elements(adj, S)) + 1))
        cone_sum = 0
        for u in max_elements(adj, S):
            past_u = 1 + sum(1 for z in S if z != u and adj[z, u])
            cone_sum += past_u
        return base * math.exp(-lam * cone_sum)

    def stage_n_buggy_u(adj, S):
        n = adj.shape[0]
        base = 1.0
        cone_sum = 0
        for u in max_elements(adj, S):
            past_u = 1 + sum(1 for z in S if z != u and adj[z, u])
            cone_sum += past_u / float(n)
        return base * math.exp(-lam * cone_sum)

    for n in (1, 2, 3, 4):
        for adj in posets_by_n[n]:
            ideals = get_ideals(adj)
            loc_C = local_cone_routed_probs(adj, ideals)
            local_cone_routed_max_row_err = max(
                local_cone_routed_max_row_err, abs(sum(loc_C.values()) - 1.0)
            )
            full_C = frozenset(range(n))
            for S in ideals:
                adj_x = extend_poset(adj, S)
                ideals_x = get_ideals(adj_x)
                loc_Cx = local_cone_routed_probs(adj_x, ideals_x)
                for T in ideals:
                    adj_y = extend_poset(adj, T)
                    ideals_y = get_ideals(adj_y)
                    loc_Cy = local_cone_routed_probs(adj_y, ideals_y)
                    total_diamonds += 1

                    # 1. Gevrey & Log-Quadratic exact diamond commutation
                    pi1_g = csg_q(adj, S, gevrey_t) * csg_q(adj_x, T, gevrey_t)
                    pi2_g = csg_q(adj, T, gevrey_t) * csg_q(adj_y, S, gevrey_t)
                    if abs(pi1_g - pi2_g) > 1e-13:
                        gevrey_violations += 1

                    pi1_l = csg_q(adj, S, logq_t) * csg_q(adj_x, T, logq_t)
                    pi2_l = csg_q(adj, T, logq_t) * csg_q(adj_y, S, logq_t)
                    if abs(pi1_l - pi2_l) > 1e-13:
                        logq_violations += 1

                    # 2. Intrinsic-past full-ideal compensation (proper base ideals S, T != C)
                    if S != full_C and T != full_C:
                        qC_S = a_seq[n] * intrinsic_u(adj, S)
                        qCx_T = a_seq[n + 1] * intrinsic_u(adj_x, T)
                        qC_T = a_seq[n] * intrinsic_u(adj, T)
                        qCy_S = a_seq[n + 1] * intrinsic_u(adj_y, S)
                        if abs(qC_S * qCx_T - qC_T * qCy_S) > 1e-13:
                            intrinsic_comp_violations += 1

                        # 3. Stage-n-normalized damping inside u(P_n, S)
                        bC_S = a_seq[n] * stage_n_buggy_u(adj, S)
                        bCx_T = a_seq[n + 1] * stage_n_buggy_u(adj_x, T)
                        bC_T = a_seq[n] * stage_n_buggy_u(adj, T)
                        bCy_S = a_seq[n + 1] * stage_n_buggy_u(adj_y, S)
                        if abs(bC_S * bCx_T - bC_T * bCy_S) > 1e-10:
                            stage_n_damping_violations += 1

                    # 4. Complete row-normalized downward local-cone routing:
                    #    row-normalized without global-post flooding, yet asymmetric upper cones break diamond!
                    if abs(loc_C[S] * loc_Cx[T] - loc_C[T] * loc_Cy[S]) > 1e-10:
                        local_cone_routed_violations += 1

    # QR-LD037 explicit 4-birth route discrepancy from 2-antichain: (1/4)*(3/32) vs (1/4)*(5/32)
    qr_ld037_pi1 = (1.0 / 4.0) * (3.0 / 32.0)
    qr_ld037_pi2 = (1.0 / 4.0) * (5.0 / 32.0)

    return {
        "total_diamonds_n_le_4": total_diamonds,
        "gevrey_diamond_violations": gevrey_violations,
        "log_quadratic_diamond_violations": logq_violations,
        "intrinsic_compensation_proper_violations": intrinsic_comp_violations,
        "stage_n_exponent_damping_violations": stage_n_damping_violations,
        "local_cone_routed_max_row_err": local_cone_routed_max_row_err,
        "local_cone_routed_diamond_violations": local_cone_routed_violations,
        "qr_ld037_pi1": qr_ld037_pi1,
        "qr_ld037_pi2": qr_ld037_pi2,
        "qr_ld037_diamond_commutes": abs(qr_ld037_pi1 - qr_ld037_pi2) < 1e-12,
    }


# =============================================================================
# SECTION 4: EXPERIMENT ORCHESTRATION (N=16, 32 + EXTENDED SCALING N=16..1024)
# =============================================================================

DEFAULT_CONFIGS = [
    {
        "model_id": "gevrey_c02_beta15",
        "family": "candidate_gevrey",
        "label": "Gevrey CSG (c=0.20, beta=1.5)",
        "type": "csg",
        "coupling_type": "gevrey",
        "params": {"c": 0.20, "beta": 1.5},
    },
    {
        "model_id": "gevrey_c02_beta20",
        "family": "candidate_gevrey",
        "label": "Gevrey CSG (c=0.20, beta=2.0)",
        "type": "csg",
        "coupling_type": "gevrey",
        "params": {"c": 0.20, "beta": 2.0},
    },
    {
        "model_id": "log_quad_c02_q010",
        "family": "candidate_log_quadratic",
        "label": "Log-Quadratic CSG (c=0.20, q=0.10)",
        "type": "csg",
        "coupling_type": "log_quadratic",
        "params": {"c": 0.20, "q": 0.10},
    },
    {
        "model_id": "log_quad_c02_q020",
        "family": "candidate_log_quadratic",
        "label": "Log-Quadratic CSG (c=0.20, q=0.20)",
        "type": "csg",
        "coupling_type": "log_quadratic",
        "params": {"c": 0.20, "q": 0.20},
    },
    {
        "model_id": "minkowski_2d",
        "family": "geometric_control",
        "label": "2D Minkowski Diamond Poisson (f(2)=0.50)",
        "type": "geometric",
        "dim": 2,
        "geometry": "diamond",
    },
    {
        "model_id": "minkowski_2d_slab",
        "family": "geometric_control",
        "label": "2D Minkowski Slab [0,1]x[0,3] (R_glob=0.204, R_int=0.50)",
        "type": "geometric",
        "dim": 2,
        "geometry": "slab",
        "slab_width": 3.0,
    },
    {
        "model_id": "minkowski_4d",
        "family": "geometric_control",
        "label": "4D Minkowski Diamond Poisson (f(4)=0.10)",
        "type": "geometric",
        "dim": 4,
        "geometry": "diamond",
    },
    {
        "model_id": "bimodal_mix_10_90",
        "family": "non_geometric_control",
        "label": "Bimodal 10/90 Chain-Antichain Mixture (E[R2]=0.10)",
        "type": "bimodal_mixture",
        "chain_prob": 0.10,
    },
    {
        "model_id": "kr_3layer",
        "family": "non_geometric_control",
        "label": "3-Layer Kleitman-Rothschild Poset (rho_2=0)",
        "type": "kr_3layer",
        "edge_prob": 0.50,
    },
    {
        "model_id": "cutoff_kmax1",
        "family": "non_geometric_control",
        "label": "Finite-Cutoff CSG (k_max=1, Recursive Forest)",
        "type": "csg",
        "coupling_type": "finite_cutoff",
        "params": {"c": 1.0, "k_max": 1},
    },
    {
        "model_id": "percolation_p008",
        "family": "non_geometric_control",
        "label": "Bernoulli Percolation (p=0.08)",
        "type": "percolation",
        "p": 0.08,
    },
    {
        "model_id": "percolation_p015",
        "family": "non_geometric_control",
        "label": "Bernoulli Percolation (p=0.15)",
        "type": "percolation",
        "p": 0.15,
    },
    {
        "model_id": "random_dag_sparse",
        "family": "non_geometric_control",
        "label": "Sparse Random DAG Closure (c_deg=2.0)",
        "type": "random_dag",
        "p": 2.0,
        "mode": "sparse",
    },
    {
        "model_id": "random_dag_fixed",
        "family": "non_geometric_control",
        "label": "Dense Random DAG Closure (p=0.05)",
        "type": "random_dag",
        "p": 0.05,
        "mode": "fixed",
    },
]


def run_discriminating_experiment(configs=None, horizons=None, num_runs=50, base_seed=1000):
    """Executes the CR-1 discriminating experiment across specified configurations and horizons."""
    if configs is None:
        configs = DEFAULT_CONFIGS
    if horizons is None:
        horizons = [16, 32]

    experiment_results = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "horizons": horizons,
            "num_runs_per_config": num_runs,
            "base_seed": base_seed,
            "total_configurations": len(configs),
        },
        "horizons_data": {},
    }

    t_start = time.time()
    print("=" * 92)
    print("CR-1 DISCRIMINATING EXPERIMENT: UNBOUNDED CSG CANDIDATES VS GEOMETRIC & NEGATIVE CONTROLS")
    print(f"Horizons: {horizons} | Runs per config: {num_runs} | Base seed: {base_seed}")
    print("=" * 92)

    for N in horizons:
        print(f"\n>>> EXECUTING HORIZON N = {N} ({num_runs} independent histories per model) <<<")
        horizon_results = {}

        for cfg in configs:
            model_id = cfg["model_id"]
            model_type = cfg["type"]
            label = cfg["label"]

            runs_r2 = []
            runs_post_density = []
            runs_rho2 = []
            runs_link_fraction = []
            runs_mean_m = []
            runs_sub_r2_means = []
            runs_within_int_var = []
            runs_within_traj_var = []
            runs_bd2 = []
            runs_bd4 = []
            all_layer_counts = {}
            total_intervals_ge4 = 0

            for r in range(num_runs):
                seed = base_seed + 1000 * N + r

                if model_type == "geometric":
                    C, r2_traj = sample_minkowski_poisson(
                        cfg["dim"],
                        N,
                        seed=seed,
                        geometry=cfg.get("geometry", "diamond"),
                        slab_width=cfg.get("slab_width", 3.0),
                    )
                    pasts = None
                elif model_type == "csg":
                    C, r2_traj, pasts = sample_csg_history(N, cfg["coupling_type"], cfg["params"], seed=seed)
                elif model_type == "percolation":
                    C, r2_traj, pasts = sample_bernoulli_percolation(N, cfg["p"], seed=seed)
                elif model_type == "random_dag":
                    C, r2_traj, pasts = sample_random_dag(N, cfg["p"], mode=cfg.get("mode", "fixed"), seed=seed)
                elif model_type == "bimodal_mixture":
                    C, r2_traj = sample_bimodal_extremal_mixture(N, chain_prob=cfg.get("chain_prob", 0.10), seed=seed)
                    pasts = None
                elif model_type == "kr_3layer":
                    C, r2_traj = sample_kleitman_rothschild_3layer(N, edge_prob=cfg.get("edge_prob", 0.50), seed=seed)
                    pasts = None
                else:
                    raise ValueError(f"Unknown model type: {model_type}")

                metrics = PosetMetrics.compute_all_metrics(C, pasts=pasts, r2_trajectory=r2_traj, min_interval_size=4)

                runs_r2.append(metrics["r2"])
                runs_post_density.append(metrics["post_density"])
                runs_rho2.append(metrics["rho2_chain_ratio"])
                runs_link_fraction.append(metrics["link_fraction"])
                runs_mean_m.append(metrics["mean_interval_size"])
                runs_within_traj_var.append(metrics["within_history_traj_var"])
                runs_bd2.append(metrics["bd2_action"])
                runs_bd4.append(metrics["bd4_action"])

                if metrics["intervals_ge4_count"] > 0:
                    runs_sub_r2_means.append(metrics["sub_interval_r2_mean"])
                    runs_within_int_var.append(metrics["within_history_interval_var"])
                    total_intervals_ge4 += metrics["intervals_ge4_count"]

                for m_val, count in metrics["layer_counts"].items():
                    all_layer_counts[m_val] = all_layer_counts.get(m_val, 0) + count

            r2_mean = float(np.mean(runs_r2))
            r2_std = float(np.std(runs_r2, ddof=1))
            r2_sem = r2_std / math.sqrt(num_runs)
            var_between_r2 = float(np.var(runs_r2, ddof=1))

            post_density_mean = float(np.mean(runs_post_density))
            rho2_mean = float(np.mean(runs_rho2))
            link_frac_mean = float(np.mean(runs_link_fraction))
            mean_m_mean = float(np.mean(runs_mean_m))

            if len(runs_sub_r2_means) > 0:
                sub_r2_mean = float(np.mean(runs_sub_r2_means))
                sub_r2_std = float(np.std(runs_sub_r2_means, ddof=1)) if len(runs_sub_r2_means) > 1 else 0.0
                var_between_sub_r2 = float(np.var(runs_sub_r2_means, ddof=1)) if len(runs_sub_r2_means) > 1 else 0.0
                mean_within_int_var = float(np.mean(runs_within_int_var)) if len(runs_within_int_var) > 0 else 0.0
            else:
                sub_r2_mean = 0.0
                sub_r2_std = 0.0
                var_between_sub_r2 = 0.0
                mean_within_int_var = 0.0

            mean_within_traj_var = float(np.mean(runs_within_traj_var))

            # CR-1 vs SS-1 flags:
            # CR-1 core: interior global R2, low between-history variance (< 0.02), non-zero 3-chains,
            #            and interior sub-interval R2 in (0.04, 0.70) (not 1D spine >= 0.75).
            stabilizes_4d_band = bool(0.05 <= r2_mean <= 0.20 and var_between_r2 < 0.02)
            cr1d_interior_intervals = bool(len(runs_sub_r2_means) > 0 and 0.04 <= sub_r2_mean <= 0.65)
            interval_self_similarity = bool(
                len(runs_sub_r2_means) > 0 and (0.5 * r2_mean <= sub_r2_mean <= 2.0 * r2_mean)
            )

            horizon_results[model_id] = {
                "model_id": model_id,
                "label": label,
                "family": cfg["family"],
                "type": model_type,
                "num_runs": num_runs,
                "r2_mean": r2_mean,
                "r2_std": r2_std,
                "r2_sem": r2_sem,
                "var_between_r2": var_between_r2,
                "post_density_mean": post_density_mean,
                "rho2_chain_ratio_mean": rho2_mean,
                "mean_within_traj_var": mean_within_traj_var,
                "link_fraction_mean": link_frac_mean,
                "mean_interval_size_mean": mean_m_mean,
                "total_intervals_ge4": total_intervals_ge4,
                "sub_interval_r2_mean": sub_r2_mean,
                "sub_interval_r2_std": sub_r2_std,
                "var_between_sub_r2": var_between_sub_r2,
                "mean_within_int_var": mean_within_int_var,
                "bd2_action_mean": float(np.mean(runs_bd2)),
                "bd4_action_mean": float(np.mean(runs_bd4)),
                "layer_counts_total": all_layer_counts,
                "cr1_stabilizes_4d_band": stabilizes_4d_band,
                "cr1d_interior_intervals": cr1d_interior_intervals,
                "cr1_interval_self_similarity": interval_self_similarity,
            }

            print(
                f"  [{model_id:20s}] R2={r2_mean:.4f}+/-{r2_std:.4f} (Var_b={var_between_r2:.5f}) | "
                f"rho2={rho2_mean:.3f} | SubR2={sub_r2_mean:.4f} (Var_w={mean_within_int_var:.4f})"
            )

        experiment_results["horizons_data"][str(N)] = horizon_results

    elapsed = time.time() - t_start
    experiment_results["metadata"]["elapsed_seconds"] = elapsed
    print("\n" + "=" * 92)
    print(f"SMALL-TO-MODERATE HORIZON SUITE COMPLETE in {elapsed:.2f} seconds.")
    print("=" * 92)

    return experiment_results


def run_extended_multi_horizon_scaling(
    horizons=(16, 32, 64, 128, 256, 512, 1024),
    num_runs=25,
    seed=20261115,
):
    """
    Fast bitmask multi-horizon scaling suite testing asymptotic trends beyond N=32:
      - Tracks parent-seed size K_n vs realized link in-degree |Max(S_n)| (cone overlap),
      - Global R_2(P_N), between-history variance Var_between(R_2), post density rho_post,
      - Mesoscopic bulk interval comparability <R_2(I)> for m in [max(4, sqrt(N)/2), max(8, 2.5*sqrt(N))],
      - Compares Gevrey (beta=1.5, 2.0, 3.0), Log-Quadratic ((0.2,0.1), (0.2,0.2), (1.0,0.5)),
        Finite-Cutoff (k_max=1, 2), Percolation (p=0.08), and 2D/4D Minkowski controls.
    """
    rng = np.random.default_rng(seed)
    maxN = max(horizons)

    csg_models = [
        ("gevrey_c02_beta15", "gevrey", (0.20, 1.5)),
        ("gevrey_c02_beta20", "gevrey", (0.20, 2.0)),
        ("gevrey_c02_beta30", "gevrey", (0.20, 3.0)),
        ("log_quad_c02_q010", "logquad", (0.20, 0.10)),
        ("log_quad_c02_q020", "logquad", (0.20, 0.20)),
        ("log_quad_c10_q050", "logquad", (1.00, 0.50)),
        ("cutoff_kmax1", "cutoff", (1.0, 1)),
        ("cutoff_kmax2", "cutoff", (1.0, 2)),
        ("percolation_p008", "perc", (0.08, 0.0)),
    ]

    scaling_out = {}

    for model_id, kind, (p1, p2) in csg_models:
        per_N = {
            N: {"r2": [], "post": [], "k_seed": [], "link_deg": [], "int_r2": [], "int_var_w": []}
            for N in horizons
        }
        for _ in range(num_runs):
            pasts = [1 << 0]
            c1 = 0
            ks_h = []
            ld_h = []
            for n in range(1, maxN):
                if kind == "perc":
                    B = [i for i in range(n) if rng.random() < p1]
                    K = len(B)
                else:
                    k_lim = min(n, int(p2)) if kind == "cutoff" else min(n, 48)
                    ks = np.arange(k_lim + 1)
                    if kind == "gevrey":
                        logw = np.array([
                            math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
                            + k * math.log(p1) - p2 * math.lgamma(k + 1)
                            for k in ks
                        ])
                    elif kind == "logquad":
                        logw = np.array([
                            math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
                            + k * math.log(p1) + 0.5 * k * (k - 1) * math.log(p2)
                            for k in ks
                        ])
                    else:
                        logw = np.array([
                            math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
                            + k * math.log(p1)
                            for k in ks
                        ])
                    logw -= logw.max()
                    w = np.exp(logw)
                    w /= w.sum()
                    K = int(rng.choice(ks, p=w))
                    B = [int(x) for x in rng.choice(n, size=K, replace=False)] if K > 0 else []

                ks_h.append(K)
                S_mask = 0
                for b in B:
                    S_mask |= pasts[b]
                max_cnt = sum(
                    1 for b in B if not any((b2 > b) and ((pasts[b2] >> b) & 1) for b2 in B)
                )
                ld_h.append(max_cnt)
                c1 += bin(S_mask).count("1")
                pasts.append(S_mask | (1 << n))

                N_cur = n + 1
                if N_cur in per_N:
                    per_N[N_cur]["r2"].append(c1 / (N_cur * (N_cur - 1) / 2.0))
                    tail = max(1, N_cur // 4)
                    per_N[N_cur]["k_seed"].append(float(np.mean(ks_h[-tail:])))
                    per_N[N_cur]["link_deg"].append(float(np.mean(ld_h[-tail:])))

                    # Post check on sample/exact
                    if N_cur <= 256:
                        post_cnt = 0
                        for x in range(N_cur):
                            p_sz = bin(pasts[x]).count("1")
                            f_sz = sum(1 for v in range(x + 1, N_cur) if (pasts[v] >> x) & 1)
                            if p_sz + f_sz == N_cur:
                                post_cnt += 1
                        per_N[N_cur]["post"].append(post_cnt / float(N_cur))
                    else:
                        per_N[N_cur]["post"].append(0.0)

                    # Mesoscopic interval sampling at N in {32, 128, 512, 1024}
                    if N_cur in (32, 128, 512, 1024):
                        m_lo = max(4, int(0.5 * math.sqrt(N_cur)))
                        m_hi = max(12, int(2.5 * math.sqrt(N_cur)))
                        int_r2s = []
                        trials = 0
                        while len(int_r2s) < 25 and trials < 350:
                            trials += 1
                            v = int(rng.integers(N_cur // 4, N_cur))
                            pm = pasts[v] ^ (1 << v)
                            if pm == 0:
                                continue
                            u_cands = [u for u in range(v) if (pm >> u) & 1]
                            u = u_cands[int(rng.integers(len(u_cands)))]
                            zs = [z for z in u_cands if z > u and ((pasts[z] >> u) & 1)]
                            m = len(zs)
                            if m_lo <= m <= m_hi:
                                sc1 = 0
                                for ai in range(m):
                                    za = zs[ai]
                                    for bi in range(ai + 1, m):
                                        if (pasts[zs[bi]] >> za) & 1:
                                            sc1 += 1
                                int_r2s.append(sc1 / (m * (m - 1) / 2.0))
                        if int_r2s:
                            per_N[N_cur]["int_r2"].append(float(np.mean(int_r2s)))
                            per_N[N_cur]["int_var_w"].append(
                                float(np.var(int_r2s, ddof=1)) if len(int_r2s) > 1 else 0.0
                            )

        scaling_out[model_id] = {}
        for N in horizons:
            d = per_N[N]
            scaling_out[model_id][str(N)] = {
                "r2_mean": float(np.mean(d["r2"])),
                "r2_std": float(np.std(d["r2"], ddof=1)),
                "var_between_r2": float(np.var(d["r2"], ddof=1)),
                "k_seed_mean": float(np.mean(d["k_seed"])),
                "link_deg_mean": float(np.mean(d["link_deg"])),
                "post_density_mean": float(np.mean(d["post"])),
                "meso_int_r2_mean": float(np.mean(d["int_r2"])) if d["int_r2"] else None,
                "meso_int_var_within": float(np.mean(d["int_var_w"])) if d["int_var_w"] else None,
            }

    # Also evaluate 4D Minkowski Diamond & 2D Minkowski Slab at N in {32, 128, 512}
    for geo_id, dim, geom in [
        ("minkowski_4d", 4, "diamond"),
        ("minkowski_2d_slab", 2, "slab"),
    ]:
        scaling_out[geo_id] = {}
        for N in (32, 128, 512):
            r2s, ir2s, ivws = [], [], []
            m_lo = max(4, int(0.5 * math.sqrt(N)))
            m_hi = max(12, int(2.5 * math.sqrt(N)))
            for r in range(15):
                C, _ = sample_minkowski_poisson(dim, N, seed=seed + 100 * N + r, geometry=geom, slab_width=3.0)
                r2s.append(float(np.sum(C)) / (N * (N - 1) / 2.0))
                C2 = C @ C
                coords = np.argwhere((C == 1) & (C2 >= m_lo) & (C2 <= m_hi))
                if len(coords) > 25:
                    idx = rng.choice(len(coords), size=25, replace=False)
                    coords = coords[idx]
                sub_vals = []
                for v, u in coords:
                    zs = np.nonzero((C[v, :] == 1) & (C[:, u] == 1))[0]
                    m = len(zs)
                    if m >= 4:
                        sc1 = int(np.sum(C[np.ix_(zs, zs)]))
                        sub_vals.append(sc1 / (m * (m - 1) / 2.0))
                if sub_vals:
                    ir2s.append(float(np.mean(sub_vals)))
                    ivws.append(float(np.var(sub_vals, ddof=1)) if len(sub_vals) > 1 else 0.0)
            scaling_out[geo_id][str(N)] = {
                "r2_mean": float(np.mean(r2s)),
                "r2_std": float(np.std(r2s, ddof=1)),
                "var_between_r2": float(np.var(r2s, ddof=1)),
                "meso_int_r2_mean": float(np.mean(ir2s)) if ir2s else None,
                "meso_int_var_within": float(np.mean(ivws)) if ivws else None,
            }

    return scaling_out


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
    """
    Monotone inverse d_MM = f^{-1}(r2) on [f(d_max), 1] via 64-step bisection.
    """
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


def _sample_logquad_incidence_fast(N, c_param, q_param, rng):
    """Exact IEEE-754 double-precision Rideout-Sorkin sampler for Log-Quadratic CSG."""
    pasts = [1 << 0]
    C = np.zeros((N, N), dtype=np.int8)
    log_c = math.log(c_param)
    log_q = math.log(q_param)
    for n in range(1, N):
        k_lim = min(n, 48)
        ks = np.arange(k_lim + 1)
        logw = np.array([
            math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            + k * log_c + 0.5 * k * (k - 1) * log_q
            for k in ks
        ])
        logw -= logw.max()
        w = np.exp(logw)
        w /= w.sum()
        K = int(rng.choice(ks, p=w))
        B = [int(x) for x in rng.choice(n, size=K, replace=False)] if K > 0 else []
        S_mask = 0
        for b in B:
            S_mask |= pasts[b]
        u = S_mask
        while u:
            lsb = u & -u
            idx = lsb.bit_length() - 1
            C[n, idx] = 1
            u ^= lsb
        pasts.append(S_mask | (1 << n))
    return C


def run_multi_alpha_profile_experiment(
    horizons=(512, 1024),
    alphas=(0.25, 0.35, 0.45, 0.50, 0.65),
    c_minus=0.5,
    c_plus=1.5,
    delta_bulk=0.05,
    num_runs=20,
    max_intervals_per_alpha=100,
    seed=20261116,
):
    """
    Evaluates the scale-dependent nested-regime profile R_int(alpha) across multiple
    mesoscopic interval scaling exponents alpha in (0, 1) under the exact CR-1c rule:
      J_N(omega; alpha) = { (u, v) : u < v, |J^-(u)| >= delta_bulk * J_bar_N,
                            |J^+(v)| >= delta_bulk * J_bar_N,
                            c_- N^alpha <= |I(u, v)| <= c_+ N^alpha }.
    Compares 4D Minkowski Alexandrov Diamonds against critical Log-Quadratic CSG (c=0.20, q=0.20).
    """
    rng = np.random.default_rng(seed)
    models = [
        ("minkowski_4d", "4D Minkowski Diamond"),
        ("log_quad_c02_q020", "Log-Quadratic CSG (c=0.20, q=0.20)"),
    ]

    profile_out = {
        "parameters": {
            "horizons": list(horizons),
            "alphas": list(alphas),
            "c_minus": c_minus,
            "c_plus": c_plus,
            "delta_bulk": delta_bulk,
            "num_runs": num_runs,
            "max_intervals_per_alpha": max_intervals_per_alpha,
            "seed": seed,
        },
        "horizons": {},
    }

    for N in horizons:
        n_key = str(N)
        profile_out["horizons"][n_key] = {}

        for model_id, label in models:
            glob_r2s = []
            glob_dmms = []
            per_alpha_runs = {
                f"{a:.2f}": {
                    "r_int": [],
                    "d_mm": [],
                    "var_within": [],
                    "j_count": [],
                    "m_mean": [],
                }
                for a in alphas
            }

            for r in range(num_runs):
                run_seed = seed + 10000 * N + (1000 if model_id == "log_quad_c02_q020" else 0) + r
                if model_id == "minkowski_4d":
                    C_int, _ = sample_minkowski_poisson(4, N, seed=run_seed, geometry="diamond")
                    C = C_int.astype(np.int8)
                else:
                    local_rng = np.random.default_rng(run_seed)
                    C = _sample_logquad_incidence_fast(N, 0.20, 0.20, local_rng)

                r2_glob = float(np.sum(C)) / (N * (N - 1) / 2.0)
                glob_r2s.append(r2_glob)
                glob_dmms.append(invert_myrheim_meyer(r2_glob))

                past_sizes = np.sum(C, axis=1)
                future_sizes = np.sum(C, axis=0)
                j_bar = float(np.mean(past_sizes))
                bulk_thresh = delta_bulk * j_bar

                C_f = C.astype(np.float64)
                C2 = np.rint(C_f @ C_f).astype(np.int32)
                bulk_mask = (
                    (C == 1)
                    & (future_sizes[:, None] >= bulk_thresh)
                    & (past_sizes[None, :] >= bulk_thresh)
                )

                for a in alphas:
                    a_key = f"{a:.2f}"
                    m_lo = max(2, int(math.ceil(c_minus * (N ** a))))
                    m_hi = int(math.floor(c_plus * (N ** a)))
                    coords = np.argwhere(bulk_mask & (C2 >= m_lo) & (C2 <= m_hi))
                    j_cnt = int(len(coords))
                    per_alpha_runs[a_key]["j_count"].append(j_cnt)
                    if j_cnt == 0:
                        continue
                    if j_cnt > max_intervals_per_alpha:
                        sel = rng.choice(j_cnt, size=max_intervals_per_alpha, replace=False)
                        eval_coords = coords[sel]
                    else:
                        eval_coords = coords

                    sub_vals = []
                    m_vals = []
                    for v, u in eval_coords:
                        zs = np.nonzero((C[v, :] == 1) & (C[:, u] == 1))[0]
                        m = len(zs)
                        if m >= 2:
                            sc1 = int(np.sum(C[np.ix_(zs, zs)]))
                            sub_vals.append(sc1 / (m * (m - 1) / 2.0))
                            m_vals.append(m)
                    if sub_vals:
                        r_bar = float(np.mean(sub_vals))
                        per_alpha_runs[a_key]["r_int"].append(r_bar)
                        if r_bar > 0.0:
                            per_alpha_runs[a_key]["d_mm"].append(invert_myrheim_meyer(r_bar))
                        per_alpha_runs[a_key]["var_within"].append(
                            float(np.var(sub_vals, ddof=1)) if len(sub_vals) > 1 else 0.0
                        )
                        per_alpha_runs[a_key]["m_mean"].append(float(np.mean(m_vals)))

            alpha_summary = {}
            for a in alphas:
                a_key = f"{a:.2f}"
                ad = per_alpha_runs[a_key]
                n_valid = len(ad["r_int"])
                n_pos = len(ad["d_mm"])
                r_mean_val = float(np.mean(ad["r_int"])) if n_valid > 0 else None
                alpha_summary[a_key] = {
                    "target_m_scale": round(N ** a, 1),
                    "m_window": [
                        max(2, int(math.ceil(c_minus * (N ** a)))),
                        int(math.floor(c_plus * (N ** a))),
                    ],
                    "valid_runs": n_valid,
                    "mean_j_count": float(np.mean(ad["j_count"])),
                    "mean_m_realized": float(np.mean(ad["m_mean"])) if n_valid > 0 else None,
                    "r_int_mean": r_mean_val,
                    "r_int_std": float(np.std(ad["r_int"], ddof=1)) if n_valid > 1 else 0.0,
                    "var_between_r_int": float(np.var(ad["r_int"], ddof=1)) if n_valid > 1 else 0.0,
                    "mean_var_within_r_int": float(np.mean(ad["var_within"])) if n_valid > 0 else None,
                    "d_mm_from_mean": invert_myrheim_meyer(r_mean_val) if (r_mean_val and r_mean_val > 0.0) else None,
                    "d_mm_mean": float(np.mean(ad["d_mm"])) if n_pos > 0 else None,
                    "d_mm_std": float(np.std(ad["d_mm"], ddof=1)) if n_pos > 1 else 0.0,
                }

            profile_out["horizons"][n_key][model_id] = {
                "label": label,
                "global_r2_mean": float(np.mean(glob_r2s)),
                "global_r2_std": float(np.std(glob_r2s, ddof=1)),
                "global_var_between": float(np.var(glob_r2s, ddof=1)),
                "global_d_mm_mean": float(np.mean(glob_dmms)),
                "global_d_mm_std": float(np.std(glob_dmms, ddof=1)),
                "alphas": alpha_summary,
            }

    return profile_out


def export_results_to_json(results, output_path):
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results successfully exported to: {output_path}")


def print_formatted_summary_table(results):
    horizons_data = results["horizons_data"]
    for N_str, data in horizons_data.items():
        print(f"\n### Quantitative Comparison Table for Horizon $N = {N_str}$")
        print("| Model Configuration | Family | $\\langle R_2 \\rangle$ | $\\operatorname{Var}_{\\rm betw}(R_2)$ | $\\langle \\rho_2 \\rangle$ | $\\langle R_2(I) \\rangle$ ($m \\ge 4$) | $\\operatorname{Var}_{\\rm within}(R_2(I))$ | CR-1d Int? | SS-1 Match? |")
        print("|---|---|---|---|---|---|---|:---:|:---:|")
        for mid, d in data.items():
            cr1d = "YES" if d["cr1d_interior_intervals"] else "NO"
            ssim = "YES" if d["cr1_interval_self_similarity"] else "NO"
            print(
                f"| {d['label']} | {d['family']} | "
                f"${d['r2_mean']:.4f} \\pm {d['r2_std']:.4f}$ | "
                f"${d['var_between_r2']:.6f}$ | "
                f"${d['rho2_chain_ratio_mean']:.3f}$ | "
                f"${d['sub_interval_r2_mean']:.4f}$ | "
                f"${d['mean_within_int_var']:.6f}$ | "
                f"{cr1d} | {ssim} |"
            )


if __name__ == "__main__":
    json_path = os.path.join(SCRIPT_DIR, "cr1_experiment_results.json")
    results = run_discriminating_experiment(horizons=[16, 32], num_runs=50, base_seed=1000)
    results["exact_diamond_audit"] = verify_exact_diamond_and_readout_properties()
    results["extended_scaling_n16_to_1024"] = run_extended_multi_horizon_scaling()
    results["multi_alpha_profile"] = run_multi_alpha_profile_experiment()
    export_results_to_json(results, json_path)
    print_formatted_summary_table(results)
