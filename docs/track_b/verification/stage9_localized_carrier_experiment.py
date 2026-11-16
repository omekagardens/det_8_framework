"""
stage9_localized_carrier_experiment.py

Stage 9: Localized Present-State Carrier and Order-Consistent Source Introduction.

Replaces the global residual carrier with a localized present-state vertex/frontier
carrier X = (C, {\mathcal{Z}_v}_{v \in V(C)}) propagating strictly along causal
covering links Max(S) -> x_S. Introduces event-anchored source excitation
\mathcal{U}_{\rm src}^{(u_*)} acting locally on vertex u_*, and cone-internal ideal
probability redistribution reconciling exact row normalization (\sum q = 1) with
strict spacelike non-disturbance (\Delta\mathbb{P}(T | \mathcal{U}_{\rm src}^{(u_*)}) = 0
for all T \not\ni u_*).

Exhaustively audits:
  1. Growth-Growth diamonds up to N <= 5 (73,786 pairs, 0 violations).
  2. Source-Birth interleaving diamonds up to N <= 5:
     - Formulation A: newborn pairs (73,786 pairs, 0 violations).
     - Formulation B: existing-vertex pairs (12,842 pairs, 0 violations).
  3. Cone-internal redistribution invariants (row normalization, no-signalling, entry conservation).

Exports benchmark results to stage9_carrier_experiment_results.json asserting Gate 9 criteria.
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

try:
    from poset_generator import generate_naturally_ordered_posets
except ImportError:
    try:
        from docs.track_b.verification.poset_generator import generate_naturally_ordered_posets
    except ImportError:
        def generate_naturally_ordered_posets(max_N: int = 5):
            for N in range(1, max_N + 1):
                num_edges = N * (N - 1) // 2
                indices = [(i, j) for i in range(N) for j in range(i)]
                for mask in range(1 << num_edges):
                    C = np.zeros((N, N), dtype=float)
                    for idx, (r, c) in enumerate(indices):
                        if (mask >> idx) & 1:
                            C[r, c] = 1.0
                    C2 = C @ C
                    if np.all((C2 == 0) | (C == 1)):
                        yield N, C


# =============================================================================
# SECTION 1: POSET & COMBINATORIAL UTILITIES
# =============================================================================

def get_ideals_adj(adj: np.ndarray) -> List[frozenset[int]]:
    """
    Enumerates all downward-closed ideals of a finite poset with upper-triangular
    boolean adjacency matrix adj[u, v] == True iff u < v.
    """
    n = adj.shape[0]
    ideals: List[frozenset[int]] = []
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


def max_elements_adj(adj: np.ndarray, S: frozenset[int] | Set[int]) -> List[int]:
    """
    Finds maximal elements Max(S) := {u in S : not exists v in S with u < v}.
    In the Hasse diagram, covering links incoming to newborn vertex x_S originate
    precisely from Max(S).
    """
    return [u for u in S if not any((v in S and v != u and adj[u, v]) for v in S)]


def extend_poset_adj(adj: np.ndarray, precursor_ideal: frozenset[int] | Set[int]) -> np.ndarray:
    """
    Extends poset of size n by adjoining newborn vertex at index n above precursor ideal.
    Preserves upper-triangular form: adj_new[u, n] = True for all u in precursor_ideal.
    """
    n = adj.shape[0]
    child = np.zeros((n + 1, n + 1), dtype=bool)
    child[:n, :n] = adj
    for u in precursor_ideal:
        child[u, n] = True
    return child


def csg_ideal_prob_exact(adj: np.ndarray, S: frozenset[int] | Set[int], t_seq: List[float]) -> float:
    """
    Calculates exact Rideout-Sorkin transition probability q(C, S) = Num(C, S) / Z_n.
    Numerator: Num(C, S) = sum_{j=0}^p binom(p, j) * t_{d + j}, where d = |Max(S)|, p = |S| - d.
    Denominator: Z_n = sum_{k=0}^n binom(n, k) * t_k.
    """
    n = adj.shape[0]
    max_elems = max_elements_adj(adj, S)
    d = len(max_elems)
    p = len(S) - d
    num = sum(math.comb(p, j) * t_seq[d + j] for j in range(p + 1))
    den = sum(math.comb(n, k) * t_seq[k] for k in range(n + 1))
    return float(num / den)


# =============================================================================
# SECTION 2: LOCALIZED CARRIER STATE & PROPAGATION ENGINE
# =============================================================================

class LocalizedCarrierState:
    """
    Localized state bundle X = (C, {\mathcal{Z}_v}_{v \in V(C)}).

    Represents a finite poset C equipped with immutable per-vertex carriers
    \mathcal{Z}_v \in \mathcal{D}(\mathbb{C}^2).
    """

    def __init__(
        self,
        adj: np.ndarray,
        carriers: List[np.ndarray],
        source_anchor: Optional[int] = None,
    ) -> None:
        self.adj = np.array(adj, dtype=bool)
        self.n = self.adj.shape[0]
        self.carriers = [np.array(c, dtype=np.complex128) for c in carriers]
        self.source_anchor = source_anchor

    def copy(self) -> LocalizedCarrierState:
        return LocalizedCarrierState(
            adj=self.adj.copy(),
            carriers=[c.copy() for c in self.carriers],
            source_anchor=self.source_anchor,
        )

    def get_frontier_carrier(self, ideal: frozenset[int] | Set[int]) -> List[np.ndarray]:
        """Returns the carriers of the maximal elements Max(ideal)."""
        max_elems = max_elements_adj(self.adj, ideal)
        return [self.carriers[m] for m in max_elems]

    def add_vertex(
        self,
        precursor_ideal: frozenset[int] | Set[int],
        new_carrier: np.ndarray,
    ) -> LocalizedCarrierState:
        """
        Adjoins newborn vertex at index n with precursor ideal S and new carrier.
        Preserves immutability of parent vertices (append-only).
        """
        new_adj = extend_poset_adj(self.adj, precursor_ideal)
        new_carriers = [c.copy() for c in self.carriers] + [np.array(new_carrier, dtype=np.complex128)]
        return LocalizedCarrierState(
            adj=new_adj,
            carriers=new_carriers,
            source_anchor=self.source_anchor,
        )

    def apply_source(
        self,
        vertex_u: int,
        excitation_matrix: np.ndarray,
    ) -> LocalizedCarrierState:
        """
        Applies local excitation \mathcal{U}_{\rm src} to vertex u_*:
          \mathcal{Z}_{u_*} \mapsto U \mathcal{Z}_{u_*} U^\dagger.
        All other vertices v != u_* remain bitwise identical.
        """
        if not (0 <= vertex_u < self.n):
            raise IndexError(f"Vertex index {vertex_u} out of range [0, {self.n})")
        new_carriers = [c.copy() for c in self.carriers]
        u_mat = np.array(excitation_matrix, dtype=np.complex128)
        new_carriers[vertex_u] = u_mat @ new_carriers[vertex_u] @ u_mat.conj().T
        return LocalizedCarrierState(
            adj=self.adj.copy(),
            carriers=new_carriers,
            source_anchor=vertex_u,
        )


class CarrierPropagationModel:
    """
    CPTP local carrier propagation channel \Phi_{\rm prop} along causal covering links.

    \Phi_{\rm prop}(\{\mathcal{Z}_m : m \in \operatorname{Max}(S)\}) =
      \begin{cases}
        \rho_{\rm vac}, & \operatorname{Max}(S) = \varnothing \\
        (1 - \gamma) U_{\rm link} \bar{\mathcal{Z}}_M U_{\rm link}^\dagger + \gamma \rho_{\rm vac}, & \operatorname{Max}(S) \ne \varnothing
      \end{cases}
    where \bar{\mathcal{Z}}_M = \frac{1}{|M|} \sum_{m \in M} \mathcal{Z}_m.
    """

    def __init__(
        self,
        gamma: float = 0.10,
        omega0: float = 0.25,
        omega1: float = 0.85,
    ) -> None:
        self.gamma = gamma
        self.omega0 = omega0
        self.omega1 = omega1

        # Ground vacuum state |0><0|
        self.rho_vac = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)
        # Excited source state |1><1|
        self.rho_exc = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=np.complex128)

        # Coherent link phase rotation U_link = diag(e^{-i \omega_0}, e^{-i \omega_1})
        self.U_link = np.array(
            [[np.exp(-1j * omega0), 0.0], [0.0, np.exp(-1j * omega1)]],
            dtype=np.complex128,
        )
        # Pauli-X source excitation operator (bit-flip |0> <-> |1|)
        self.U_src = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)

    def phi_prop(self, parent_carriers: List[np.ndarray]) -> np.ndarray:
        """Propagates frontier carriers across incoming covering links."""
        if len(parent_carriers) == 0:
            return self.rho_vac.copy()
        rho_bar = np.mean(parent_carriers, axis=0)
        rotated = self.U_link @ rho_bar @ self.U_link.conj().T
        return (1.0 - self.gamma) * rotated + self.gamma * self.rho_vac

    def excitate(self, carrier: np.ndarray) -> np.ndarray:
        """Excites carrier state via local unitary channel."""
        return self.U_src @ carrier @ self.U_src.conj().T


# =============================================================================
# SECTION 3: CONE-INTERNAL REDISTRIBUTION ENGINE & TRANSITION KERNEL
# =============================================================================

class ConeRedistributionTransitionEngine:
    """
    Transition kernel implementing cone-internal ideal probability redistribution.

    Partitions ideals \mathcal{I}(C) = \mathcal{I}_{\not\ni u_*} \sqcup \mathcal{I}_{\ni u_*}:
      - For T \not\ni u_*: q(C, X, T) = q_0(C, T) [Strict Spacelike Non-Disturbance]
      - For S \ni u_*:    q(C, X, S) = P_{\rm enter}(C; u_*) * \frac{w(S)}{Z_{\rm cone}}

    Guarantees:
      1. Exact row normalization: \sum_{I \in \mathcal{I}(C)} q(C, X, I) = 1.
      2. Strict spacelike non-disturbance: \Delta\mathbb{P}(T | \mathcal{U}_{\rm src}^{(u_*)}) = 0 for all T \not\ni u_*.
      3. Entry probability preservation: \sum_{S \ni u_*} q(C, X, S) = P_{\rm enter}(C; u_*).
    """

    def __init__(
        self,
        c0: float = 0.20,
        q0: float = 0.20,
        c1: float = 0.50,
        q1: float = 0.35,
        kappa: float = 0.50,
    ) -> None:
        self.c0 = c0
        self.q0 = q0
        self.c1 = c1
        self.q1 = q1
        self.kappa = kappa

        self.t0_seq = [(c0 ** k) * (q0 ** (k * (k - 1) // 2)) for k in range(16)]
        self.t1_seq = [(c1 ** k) * (q1 ** (k * (k - 1) // 2)) for k in range(16)]

    def compute_probabilities(
        self,
        state: LocalizedCarrierState,
        u_star: Optional[int] = None,
    ) -> Dict[frozenset[int], float]:
        """
        Computes the complete transition probability distribution over all ideals of state.adj.
        If u_star is None or not specified, returns the unperturbed baseline CSG distribution q_0.
        If u_star is specified, redistributes probability strictly within the future cone of u_star.
        """
        ideals = get_ideals_adj(state.adj)
        q0_map = {S: csg_ideal_prob_exact(state.adj, S, self.t0_seq) for S in ideals}

        if u_star is None or u_star < 0 or u_star >= state.n:
            return q0_map

        inside = [S for S in ideals if u_star in S]
        outside = [S for S in ideals if u_star not in S]
        p_enter = sum(q0_map[S] for S in inside)

        # Spacelike / exterior ideals maintain exact baseline probabilities
        out_probs: Dict[frozenset[int], float] = {T: q0_map[T] for T in outside}

        # Causal future ideals receive cone-internal redistribution
        if len(inside) == 0:
            return out_probs

        w_inside: Dict[frozenset[int], float] = {}
        for S in inside:
            q1_s = csg_ideal_prob_exact(state.adj, S, self.t1_seq)
            max_elems = max_elements_adj(state.adj, S)
            max_p1 = max(
                (float(np.real(state.carriers[m][1, 1])) for m in max_elems),
                default=0.0,
            )
            w_inside[S] = q1_s * (1.0 + self.kappa * max_p1)

        z_cone = sum(w_inside.values())
        if z_cone > 0.0:
            for S in inside:
                out_probs[S] = p_enter * (w_inside[S] / z_cone)
        else:
            for S in inside:
                out_probs[S] = q0_map[S]

        return out_probs


class ConeClosureRedistributionEngine:
    """
    Cone-closure redistribution engine restoring exact post-excitation commutation on ALL
    Mixed (Cone-Spacelike) and Spacelike-Spacelike Growth-Growth diamonds.

    For an excited source anchor u_* in V(C), let F = J^+_C[u_*] and define the cone-past
    closure ideal S_cone(C; u_*) := J^-_C[F] in I_{ni u_*}(C).
      - Every proper sub-ideal S subsetneq S_cone with u_* in S is attenuated by a local
        frontier factor (1 - lam(S)), where lam(S) = eta_gain * max_{m in Max(S)} p_1(m) in [0, 1).
      - The exact probability slack sum_{S subsetneq S_cone, u_* in S} lam(S) q_0(C, S)
        is routed into S_cone(C; u_*).
      - All exterior ideals T notni u_* AND cross-join ideals S' not subseteq S_cone retain q_0(C, .).

    Because S_cone(C + y_T; u_*) == S_cone(C; u_*) and Num(C + y_T, S) == Num(C, S) for every
    T notni u_* and S subseteq S_cone, the relative likelihood ratio q(C, X, S) / q_0(C, S) is
    strictly invariant under adjoining any spacelike birth y_T, eliminating 100% of mixed
    cone-spacelike post-excitation diamond violations (0 / 6,388 on N <= 4).
    """

    def __init__(
        self,
        c0: float = 0.20,
        q0: float = 0.20,
        eta_gain: float = 0.50,
    ) -> None:
        self.c0 = c0
        self.q0 = q0
        self.eta_gain = eta_gain
        self.t0_seq = [(c0 ** k) * (q0 ** (k * (k - 1) // 2)) for k in range(16)]

    def compute_probabilities(
        self,
        state: LocalizedCarrierState,
        u_star: Optional[int] = None,
    ) -> Dict[frozenset[int], float]:
        adj = state.adj
        n = adj.shape[0]
        ideals = get_ideals_adj(adj)
        q0_map = {S: csg_ideal_prob_exact(adj, S, self.t0_seq) for S in ideals}

        if u_star is None or u_star < 0 or u_star >= n:
            return q0_map

        j_plus = {v for v in range(n) if v == u_star or adj[u_star, v]}
        s_cone = frozenset(
            u for u in range(n) if u in j_plus or any(adj[u, w] for w in j_plus)
        )

        out_probs = dict(q0_map)
        slack = 0.0
        for S in ideals:
            if u_star in S and S != s_cone and S.issubset(s_cone):
                max_elems = max_elements_adj(adj, S)
                max_p1 = max(
                    (float(np.real(state.carriers[m][1, 1])) for m in max_elems),
                    default=0.0,
                )
                lam = self.eta_gain * max(0.0, min(1.0, max_p1))
                delta = lam * q0_map[S]
                out_probs[S] = q0_map[S] - delta
                slack += delta

        out_probs[s_cone] = out_probs[s_cone] + slack
        return out_probs


# Module-level wrapper functions matching PROJECT.md interface contracts:
def compute_newborn_carrier(
    poset: np.ndarray,
    ideal: frozenset[int] | Set[int],
    parent_carriers: List[np.ndarray],
    prop_model: Optional[CarrierPropagationModel] = None,
) -> np.ndarray:
    """Interface wrapper: synthesizes newborn carrier strictly reading Max(ideal)."""
    model = prop_model or CarrierPropagationModel()
    return model.phi_prop(parent_carriers)


def apply_event_source(
    carrier_state: LocalizedCarrierState,
    vertex_u: int,
    params: Optional[Dict[str, Any]] = None,
) -> LocalizedCarrierState:
    """Interface wrapper: excites local carrier at designated event vertex_u."""
    model = CarrierPropagationModel()
    u_mat = params.get("excitation_matrix", model.U_src) if params else model.U_src
    return carrier_state.apply_source(vertex_u, u_mat)


def compute_ideal_probabilities(
    poset: np.ndarray,
    carrier_state: LocalizedCarrierState,
    u_star: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[frozenset[int], float]:
    """Interface wrapper: computes transition probabilities under cone-internal redistribution."""
    engine = ConeRedistributionTransitionEngine()
    return engine.compute_probabilities(carrier_state, u_star=u_star)


# =============================================================================
# SECTION 4: EXHAUSTIVE DIAMOND AUDIT ENGINES (GATE 9 CRITERIA)
# =============================================================================

def audit_growth_growth_diamonds(
    max_N: int = 5,
    tolerance: float = 1e-14,
) -> Dict[str, Any]:
    """
    Exhaustively audits all Growth-Growth diamond pairs up to max_N (73,786 diamonds for N <= 5).

    Verifies:
      1. Canonical state and carrier isomorphism: \sigma(X^{(21)}) \equiv X^{(12)} under \sigma = (n <-> n+1).
      2. Probability commutation: \Pi_1(S, T) \equiv \Pi_2(T, S) via matrix symmetry \Pi_1 == \Pi_1^T.
    """
    posets = list(generate_naturally_ordered_posets(max_N))
    prop_model = CarrierPropagationModel()
    t_seq = [(0.20 ** k) * (0.20 ** (k * (k - 1) // 2)) for k in range(16)]

    total_diamonds = 0
    violations = 0
    max_prob_discrepancy = 0.0
    max_carrier_discrepancy = 0.0

    breakdown_by_N: Dict[int, Dict[str, Any]] = {
        n: {
            "posets": 0,
            "diamonds": 0,
            "violations": 0,
            "max_discrepancy": 0.0,
            "max_carrier_discrepancy": 0.0,
        }
        for n in range(1, max_N + 1)
    }

    for N, C in posets:
        adj = C.T > 0.5
        n = adj.shape[0]
        ideals = get_ideals_adj(adj)
        K = len(ideals)
        n_diamonds = K * K

        breakdown_by_N[n]["posets"] += 1
        breakdown_by_N[n]["diamonds"] += n_diamonds
        total_diamonds += n_diamonds

        # Base probabilities vector q in R^K
        q_vec = np.array([csg_ideal_prob_exact(adj, S, t_seq) for S in ideals], dtype=np.float64)

        # Transition matrix M[i, j] = q(C + x_{S_i}, T_j)
        M = np.zeros((K, K), dtype=np.float64)
        for i, S in enumerate(ideals):
            adj_x = extend_poset_adj(adj, S)
            for j, T in enumerate(ideals):
                M[i, j] = csg_ideal_prob_exact(adj_x, T, t_seq)

        # Path 1 matrix Pi1[i, j] = q_vec[i] * M[i, j]
        Pi1 = q_vec[:, None] * M

        # Discrepancy matrix Delta = |Pi1 - Pi1^T|
        Delta = np.abs(Pi1 - Pi1.T)
        cur_max_prob = float(np.max(Delta))
        if cur_max_prob > max_prob_discrepancy:
            max_prob_discrepancy = cur_max_prob
        if cur_max_prob > breakdown_by_N[n]["max_discrepancy"]:
            breakdown_by_N[n]["max_discrepancy"] = cur_max_prob

        n_viol = int(np.sum(Delta > tolerance))
        violations += n_viol
        breakdown_by_N[n]["violations"] += n_viol

        # Verify Genuine Carrier State Isomorphism across extended posets C + x_S and C + y_T
        base_carriers = [prop_model.rho_vac.copy() for _ in range(n)]
        for v in range(n):
            preds = [u for u in range(v) if adj[u, v]]
            max_preds = max_elements_adj(adj, set(preds))
            base_carriers[v] = prop_model.phi_prop([base_carriers[m] for m in max_preds])

        # Step 1: Precompute first newborn carrier c_first for each ideal S_i
        c_first = np.array([
            prop_model.phi_prop([base_carriers[m] for m in max_elements_adj(adj, S)])
            for S in ideals
        ], dtype=np.complex128)

        # Step 2: Construct extended posets C + x_{S_i} and extended carrier bundles
        extended_adjs = [extend_poset_adj(adj, S) for S in ideals]
        extended_carriers = [base_carriers + [c_first[i]] for i in range(K)]

        # Step 3: Compute second newborn carrier c_second[i, j] = Phi(Max_{C+x_{S_i}}(T_j))
        c_second_mat = np.zeros((K, K, 2, 2), dtype=np.complex128)
        for i in range(K):
            adj_x = extended_adjs[i]
            carriers_x = extended_carriers[i]
            for j, T in enumerate(ideals):
                max_T_in_x = max_elements_adj(adj_x, T)
                c_second_mat[i, j] = prop_model.phi_prop([carriers_x[m] for m in max_T_in_x])

        # Step 4: Vectorized comparison of Path 1 vs Path 2
        # Path 1 (S_i then T_j): newborn x_S has c_first[i], newborn y_T has c_second[i, j]
        # Path 2 (T_j then S_i): newborn y_T has c_first[j], newborn x_S has c_second[j, i]
        # Commutation requires: c_second[i, j] == c_first[j] and c_second[j, i] == c_first[i]
        diff_y = np.max(np.abs(c_second_mat - c_first[None, :, :, :]), axis=(2, 3))
        diff = np.maximum(diff_y, diff_y.T)

        cur_max_carrier = float(np.max(diff))
        if cur_max_carrier > max_carrier_discrepancy:
            max_carrier_discrepancy = cur_max_carrier
        if cur_max_carrier > breakdown_by_N[n]["max_carrier_discrepancy"]:
            breakdown_by_N[n]["max_carrier_discrepancy"] = cur_max_carrier

        n_viol_carrier = int(np.sum(diff > tolerance))
        violations += n_viol_carrier
        breakdown_by_N[n]["violations"] += n_viol_carrier

    return {
        "max_N": max_N,
        "total_posets": len(posets),
        "total_diamonds_audited": total_diamonds,
        "violations": violations,
        "max_discrepancy": max_prob_discrepancy,
        "max_carrier_discrepancy": max_carrier_discrepancy,
        "breakdown_by_N": breakdown_by_N,
        "gate9_passed": (violations == 0 and max_prob_discrepancy <= tolerance and max_carrier_discrepancy <= tolerance),
    }


def audit_source_birth_interleaving_diamonds(
    max_N: int = 5,
    tolerance: float = 1e-14,
) -> Dict[str, Any]:
    """
    Exhaustively audits Source-Birth interleaving diamonds up to max_N:
      - Formulation A: All 73,786 newborn pairs (x_S designated as source anchor u_*, y_T parallel u_*).
      - Formulation B: All 12,842 existing-vertex pairs (u_* in V(C), T with u_* not in T).

    Verifies path probability commutation and strict spacelike non-disturbance.
    """
    posets = list(generate_naturally_ordered_posets(max_N))
    prop_model = CarrierPropagationModel()
    redist_engine = ConeRedistributionTransitionEngine()

    total_form_A = 0
    violations_form_A = 0
    max_diff_form_A = 0.0

    total_form_B = 0
    violations_form_B = 0
    max_diff_form_B = 0.0

    breakdown_by_N: Dict[int, Dict[str, Any]] = {
        n: {
            "posets": 0,
            "form_A_diamonds": 0,
            "form_A_violations": 0,
            "form_A_max_diff": 0.0,
            "form_B_diamonds": 0,
            "form_B_violations": 0,
            "form_B_max_diff": 0.0,
        }
        for n in range(1, max_N + 1)
    }

    for N, C in posets:
        adj = C.T > 0.5
        n = adj.shape[0]
        ideals = get_ideals_adj(adj)
        K = len(ideals)

        breakdown_by_N[n]["posets"] += 1

        # Initialize base carrier state
        base_carriers = [prop_model.rho_vac.copy() for _ in range(n)]
        for v in range(n):
            preds = [u for u in range(v) if adj[u, v]]
            max_preds = max_elements_adj(adj, set(preds))
            base_carriers[v] = prop_model.phi_prop([base_carriers[m] for m in max_preds])

        base_state = LocalizedCarrierState(adj, base_carriers)
        q_base = redist_engine.compute_probabilities(base_state)

        # ---------------------------------------------------------------------
        # Formulation B: Existing vertex u_* in V(C), spacelike birth y_T (u_* not in T)
        # ---------------------------------------------------------------------
        for u in range(n):
            exc_state = base_state.apply_source(u, prop_model.U_src)
            q_exc = redist_engine.compute_probabilities(exc_state, u_star=u)

            for T in ideals:
                if u not in T:
                    total_form_B += 1
                    breakdown_by_N[n]["form_B_diamonds"] += 1

                    # Path 1: Excitation applied first, then y_T committed -> q_exc[T]
                    # Path 2: y_T committed first from unexcited base, then u_* excited -> q_base[T]
                    # No-signalling equivalence implies q_exc[T] == q_base[T]
                    diff = abs(q_exc[T] - q_base[T])
                    if diff > max_diff_form_B:
                        max_diff_form_B = diff
                    if diff > breakdown_by_N[n]["form_B_max_diff"]:
                        breakdown_by_N[n]["form_B_max_diff"] = diff
                    if diff > tolerance:
                        violations_form_B += 1
                        breakdown_by_N[n]["form_B_violations"] += 1

        # ---------------------------------------------------------------------
        # Formulation A: Newborn pairs (x_S designated as u_*, y_T with u_* not in T)
        # Explicit Forward Execution of Path 1 vs Path 2:
        # Path 1: commit u_* over S -> excite u_* -> commit y_T over T
        # Path 2: commit y_T over T (UNEXCITED) -> commit u_* over S -> excite u_*
        # ---------------------------------------------------------------------
        q_vec = np.array([q_base[S] for S in ideals], dtype=np.float64)
        M_path1 = np.zeros((K, K), dtype=np.float64)
        M_unexc = np.zeros((K, K), dtype=np.float64)

        for i, S in enumerate(ideals):
            child_carrier = prop_model.phi_prop(base_state.get_frontier_carrier(S))
            child_state = base_state.add_vertex(S, child_carrier)

            # Path 2 transition kernel from unexcited child: q(C + y_{T_i}, S_j)
            q_unexc_child = redist_engine.compute_probabilities(child_state, u_star=None)
            for j, T in enumerate(ideals):
                M_unexc[i, j] = q_unexc_child[T]

            # Path 1 transition kernel from excited child (u_* = n): q(C + x_{S_i}, X_exc, T_j)
            exc_child = child_state.apply_source(n, prop_model.U_src)
            q_exc_child = redist_engine.compute_probabilities(exc_child, u_star=n)
            for j, T in enumerate(ideals):
                M_path1[i, j] = q_exc_child[T]

        # Path 1: commit S_i -> excite u_* -> commit T_j
        Pi1_A = q_vec[:, None] * M_path1
        # Path 2: commit T_j (unexcited) -> commit S_i -> excite u_*
        # (q_vec[:, None] * M_unexc)[j, i] = q_vec[j] * q(C + y_{T_j}, S_i)
        Pi2_A = (q_vec[:, None] * M_unexc).T

        Delta_A = np.abs(Pi1_A - Pi2_A)
        cur_max_A = float(np.max(Delta_A))
        if cur_max_A > max_diff_form_A:
            max_diff_form_A = cur_max_A
        if cur_max_A > breakdown_by_N[n]["form_A_max_diff"]:
            breakdown_by_N[n]["form_A_max_diff"] = cur_max_A

        n_viol_A = int(np.sum(Delta_A > tolerance))
        violations_form_A += n_viol_A
        breakdown_by_N[n]["form_A_violations"] += n_viol_A
        breakdown_by_N[n]["form_A_diamonds"] += K * K
        total_form_A += K * K

    return {
        "max_N": max_N,
        "formulation_A_newborn_diamonds": total_form_A,
        "formulation_A_violations": violations_form_A,
        "formulation_A_max_diff": max_diff_form_A,
        "formulation_B_existing_diamonds": total_form_B,
        "formulation_B_violations": violations_form_B,
        "formulation_B_max_diff": max_diff_form_B,
        "breakdown_by_N": breakdown_by_N,
        "gate9_passed": (
            violations_form_A == 0
            and violations_form_B == 0
            and max_diff_form_A <= tolerance
            and max_diff_form_B <= tolerance
        ),
    }


def audit_cone_internal_redistribution(
    max_N: int = 4,
    tolerance: float = 1e-14,
) -> Dict[str, Any]:
    """
    Audits cone-internal probability redistribution across all posets up to max_N:
      1. Exact row normalization: |sum_{I} q(C, X, I) - 1.0| < tolerance.
      2. Strict spacelike non-disturbance: |q(C, X, T) - q_0(C, T)| == 0 for all T not containing u_*.
      3. Entry probability preservation: |sum_{S in inside} q(C, X, S) - P_enter| < tolerance.
    """
    posets = list(generate_naturally_ordered_posets(max_N))
    prop_model = CarrierPropagationModel()
    redist_engine = ConeRedistributionTransitionEngine()

    max_row_norm_err = 0.0
    max_spacelike_err = 0.0
    max_p_enter_err = 0.0
    total_checks = 0

    for N, C in posets:
        adj = C.T > 0.5
        n = adj.shape[0]
        ideals = get_ideals_adj(adj)

        base_carriers = [prop_model.rho_vac.copy() for _ in range(n)]
        for v in range(n):
            preds = [u for u in range(v) if adj[u, v]]
            max_preds = max_elements_adj(adj, set(preds))
            base_carriers[v] = prop_model.phi_prop([base_carriers[m] for m in max_preds])

        base_state = LocalizedCarrierState(adj, base_carriers)
        q_base = redist_engine.compute_probabilities(base_state)

        for u in range(n):
            total_checks += 1
            exc_state = base_state.apply_source(u, prop_model.U_src)
            q_exc = redist_engine.compute_probabilities(exc_state, u_star=u)

            # 1. Exact row normalization
            norm_sum = sum(q_exc.values())
            norm_err = abs(norm_sum - 1.0)
            if norm_err > max_row_norm_err:
                max_row_norm_err = norm_err

            # 2. Strict spacelike non-disturbance
            for T in ideals:
                if u not in T:
                    sp_err = abs(q_exc[T] - q_base[T])
                    if sp_err > max_spacelike_err:
                        max_spacelike_err = sp_err

            # 3. Entry probability preservation
            p_enter_base = sum(q_base[S] for S in ideals if u in S)
            p_enter_exc = sum(q_exc[S] for S in ideals if u in S)
            pe_err = abs(p_enter_exc - p_enter_base)
            if pe_err > max_p_enter_err:
                max_p_enter_err = pe_err

    passed = (
        max_row_norm_err <= tolerance
        and max_spacelike_err <= tolerance
        and max_p_enter_err <= tolerance
    )

    return {
        "max_N": max_N,
        "total_anchor_checks": total_checks,
        "max_row_norm_error": max_row_norm_err,
        "max_spacelike_nondisturbance_error": max_spacelike_err,
        "max_entry_probability_error": max_p_enter_err,
        "gate9_passed": passed,
    }


def audit_post_excitation_diamond_taxonomy(
    max_N: int = 4,
    tolerance: float = 1e-13,
) -> Dict[str, Any]:
    """
    Exhaustively audits post-excitation Growth-Growth diamonds (where u_* in V(C) is ALREADY
    excited prior to both births x_S and y_T) across all (C, u_*, S, T) quadruples up to max_N:
      1. Carrier bundle isomorphism: verifies sigma(X^{(21)}) == X^{(12)} across 100% of all
         post-excitation diamonds (0 / 14,276 violations for N <= 4).
      2. Stage-normalized Z_cone redistribution vs. Cone-Closure redistribution on S_cone = J^-_C[J^+_C[u_*]]:
         - Spacelike-Spacelike (S, T notni u_*): 0 / 3,944 violations under both rules.
         - Mixed Cone-Spacelike (S ni u_*, T notni u_*): stage-normalized Z_cone incurs 6,388 / 6,388
           violations due to cross-join ideals S cup {y_T} altering Z_cone(C + y_T), whereas
           ConeClosureRedistributionEngine eliminates 100% of mixed violations (0 / 6,388).
         - Inner Cone-Cone (S_1, S_2 ni u_*): documents the exact local frontier overlap boundary
           (1,988 / 3,944 under ConeClosureRedistributionEngine; 2,746 / 3,944 under Z_cone),
           paralleling CR-1 Proposition 6.3.
    """
    posets = list(generate_naturally_ordered_posets(max_N))
    prop_model = CarrierPropagationModel()
    zcone_engine = ConeRedistributionTransitionEngine()
    closure_engine = ConeClosureRedistributionEngine()

    carrier_total = 0
    carrier_violations = 0
    max_post_carrier_diff = 0.0

    counts = {"spacelike_spacelike": 0, "mixed_cone_spacelike": 0, "inner_cone_cone": 0}
    zcone_viol = {"spacelike_spacelike": 0, "mixed_cone_spacelike": 0, "inner_cone_cone": 0}
    closure_viol = {"spacelike_spacelike": 0, "mixed_cone_spacelike": 0, "inner_cone_cone": 0}
    max_closure_mixed_diff = 0.0
    max_closure_row_err = 0.0

    for N, C in posets:
        adj = C.T > 0.5
        n = adj.shape[0]
        ideals = get_ideals_adj(adj)

        for u in range(n):
            carriers = [prop_model.rho_vac.copy() for _ in range(n)]
            for v in range(n):
                preds = [w for w in range(v) if adj[w, v]]
                max_p = max_elements_adj(adj, set(preds))
                carriers[v] = prop_model.phi_prop([carriers[m] for m in max_p])
                if v == u:
                    carriers[v] = prop_model.excitate(carriers[v])

            st = LocalizedCarrierState(adj, carriers, source_anchor=u)
            q_z_base = zcone_engine.compute_probabilities(st, u_star=u)
            q_c_base = closure_engine.compute_probabilities(st, u_star=u)
            row_err = abs(sum(q_c_base.values()) - 1.0)
            if row_err > max_closure_row_err:
                max_closure_row_err = row_err

            child_states: Dict[frozenset[int], LocalizedCarrierState] = {}
            child_first_c: Dict[frozenset[int], np.ndarray] = {}
            q_z_child: Dict[frozenset[int], Dict[frozenset[int], float]] = {}
            q_c_child: Dict[frozenset[int], Dict[frozenset[int], float]] = {}

            for S in ideals:
                c_new = prop_model.phi_prop(st.get_frontier_carrier(S))
                st_S = st.add_vertex(S, c_new)
                child_first_c[S] = c_new
                child_states[S] = st_S
                q_z_child[S] = zcone_engine.compute_probabilities(st_S, u_star=u)
                q_c_child[S] = closure_engine.compute_probabilities(st_S, u_star=u)

            for S in ideals:
                st_S = child_states[S]
                for T in ideals:
                    st_T = child_states[T]
                    cT_after_S = prop_model.phi_prop(st_S.get_frontier_carrier(T))
                    cS_after_T = prop_model.phi_prop(st_T.get_frontier_carrier(S))
                    cdiff = max(
                        float(np.max(np.abs(cT_after_S - child_first_c[T]))),
                        float(np.max(np.abs(cS_after_T - child_first_c[S]))),
                    )
                    carrier_total += 1
                    if cdiff > max_post_carrier_diff:
                        max_post_carrier_diff = cdiff
                    if cdiff > tolerance:
                        carrier_violations += 1

                    z_diff = abs(q_z_base[S] * q_z_child[S][T] - q_z_base[T] * q_z_child[T][S])
                    c_diff = abs(q_c_base[S] * q_c_child[S][T] - q_c_base[T] * q_c_child[T][S])

                    s_in = (u in S)
                    t_in = (u in T)
                    if not s_in and not t_in:
                        cat = "spacelike_spacelike"
                    elif s_in != t_in:
                        cat = "mixed_cone_spacelike"
                        if c_diff > max_closure_mixed_diff:
                            max_closure_mixed_diff = c_diff
                    else:
                        cat = "inner_cone_cone"

                    counts[cat] += 1
                    if z_diff > tolerance:
                        zcone_viol[cat] += 1
                    if c_diff > tolerance:
                        closure_viol[cat] += 1

    taxonomy_passed = (
        carrier_violations == 0
        and closure_viol["spacelike_spacelike"] == 0
        and closure_viol["mixed_cone_spacelike"] == 0
        and max_closure_row_err <= tolerance
    )

    return {
        "max_N": max_N,
        "total_post_excitation_quadruples": carrier_total,
        "carrier_bundle_violations": carrier_violations,
        "max_carrier_bundle_diff": max_post_carrier_diff,
        "category_counts": counts,
        "stage_normalized_zcone_violations": zcone_viol,
        "cone_closure_redistribution_violations": closure_viol,
        "max_cone_closure_mixed_diff": max_closure_mixed_diff,
        "max_cone_closure_row_norm_error": max_closure_row_err,
        "passed": taxonomy_passed,
    }


# =============================================================================
# SECTION 5: MASTER VERIFICATION RUNNER & RFC-8259 JSON EXPORT
# =============================================================================

def run_stage9_verification(
    output_json_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes the full Stage 9 verification suite:
      1. Baseline CSG Growth-Growth & Carrier Bundle diamonds audit (N <= 5, 73,786 pairs).
      2. Source-Birth interleaving diamonds audit (N <= 5, Form A: 73,786; Form B: 12,842).
      3. Cone-internal redistribution invariants audit (N <= 4, 186 anchor configs).
      4. Post-excitation Growth-Growth diamond taxonomy audit (N <= 4, 14,276 quadruples).
      5. Asserts Gate 9 criteria and exports RFC-8259 benchmark JSON.
    """
    start_time = time.time()
    print("=" * 80)
    print("STAGE 9: LOCALIZED PRESENT-STATE CARRIER & ORDER-CONSISTENT SOURCE AUDIT")
    print("=" * 80)

    # 1. Growth-Growth Diamond Audit (Baseline CSG + Carrier Bundle)
    print("\n>>> AUDITING BASELINE GROWTH-GROWTH & CARRIER DIAMONDS (N <= 5) <<<")
    t0 = time.time()
    gg_results = audit_growth_growth_diamonds(max_N=5)
    t_gg = time.time() - t0
    print(
        f"  Total diamonds audited: {gg_results['total_diamonds_audited']:,} across {gg_results['total_posets']} posets"
    )
    print(
        f"  Commutation violations: {gg_results['violations']} | Max prob discrepancy: {gg_results['max_discrepancy']:.4e}"
    )
    print(
        f"  Max carrier discrepancy: {gg_results['max_carrier_discrepancy']:.4e} | Elapsed: {t_gg:.3f}s"
    )

    # 2. Source-Birth Interleaving Diamond Audit
    print("\n>>> AUDITING SOURCE-BIRTH INTERLEAVING DIAMONDS (N <= 5) <<<")
    t0 = time.time()
    sb_results = audit_source_birth_interleaving_diamonds(max_N=5)
    t_sb = time.time() - t0
    print(
        f"  Formulation A (newborn): {sb_results['formulation_A_newborn_diamonds']:,} pairs | Violations: {sb_results['formulation_A_violations']} | Max diff: {sb_results['formulation_A_max_diff']:.4e}"
    )
    print(
        f"  Formulation B (existing): {sb_results['formulation_B_existing_diamonds']:,} pairs | Violations: {sb_results['formulation_B_violations']} | Max diff: {sb_results['formulation_B_max_diff']:.4e}"
    )
    print(f"  Elapsed: {t_sb:.3f}s")

    # 3. Cone-Internal Redistribution Audit
    print("\n>>> AUDITING CONE-INTERNAL REDISTRIBUTION INVARIANTS (N <= 4) <<<")
    t0 = time.time()
    redist_results = audit_cone_internal_redistribution(max_N=4)
    t_redist = time.time() - t0
    print(f"  Total anchor configurations audited: {redist_results['total_anchor_checks']}")
    print(f"  Max row normalization error:         {redist_results['max_row_norm_error']:.4e}")
    print(f"  Max spacelike non-disturbance error: {redist_results['max_spacelike_nondisturbance_error']:.4e}")
    print(f"  Max entry probability error:         {redist_results['max_entry_probability_error']:.4e}")
    print(f"  Elapsed: {t_redist:.3f}s")

    # 4. Post-Excitation Diamond Taxonomy Audit
    print("\n>>> AUDITING POST-EXCITATION GROWTH-GROWTH DIAMOND TAXONOMY (N <= 4) <<<")
    t0 = time.time()
    post_exc_results = audit_post_excitation_diamond_taxonomy(max_N=4)
    t_pe = time.time() - t0
    print(
        f"  Post-excitation carrier bundle violations: {post_exc_results['carrier_bundle_violations']} / {post_exc_results['total_post_excitation_quadruples']:,}"
    )
    print(
        f"  Cone-Closure Mixed (Cone-Spacelike) viols: {post_exc_results['cone_closure_redistribution_violations']['mixed_cone_spacelike']} / {post_exc_results['category_counts']['mixed_cone_spacelike']:,} "
        f"(vs Z_cone: {post_exc_results['stage_normalized_zcone_violations']['mixed_cone_spacelike']:,})"
    )
    print(
        f"  Inner Cone-Cone overlap frontier:          {post_exc_results['cone_closure_redistribution_violations']['inner_cone_cone']} / {post_exc_results['category_counts']['inner_cone_cone']:,} | Elapsed: {t_pe:.3f}s"
    )

    elapsed_total = time.time() - start_time

    # Gate 9 Criteria Assertions
    gate9_passed = (
        gg_results["gate9_passed"]
        and sb_results["gate9_passed"]
        and redist_results["gate9_passed"]
        and post_exc_results["passed"]
        and elapsed_total < 30.0
    )

    print("\n" + "=" * 80)
    print(f"GATE 9 VERIFICATION STATUS: {'PASS' if gate9_passed else 'FAIL'} (Total: {elapsed_total:.3f}s)")
    print("=" * 80)

    # Convert breakdown keys to strings for valid JSON export
    gg_breakdown_str = {str(k): v for k, v in gg_results["breakdown_by_N"].items()}
    sb_breakdown_str = {str(k): v for k, v in sb_results["breakdown_by_N"].items()}

    results_data: Dict[str, Any] = {
        "metadata": {
            "stage": "Stage 9: Localized Present-State Carrier and Order-Consistent Source Introduction",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_wall_seconds": elapsed_total,
            "gate9_passed": gate9_passed,
            "audit_methodology": {
                "carrier_isomorphism": "genuine_extended_poset_evaluation",
                "baseline_growth_growth_kernel": "unperturbed_rideout_sorkin_csg",
                "source_birth_interleaving": "explicit_path2_construction",
                "probability_redistribution": "cone_internal_partition_audit",
                "post_excitation_taxonomy": "cone_closure_vs_stage_zcone_exhaustive_audit",
            },
        },
        "gate9_summary": {
            "status": "PASS" if gate9_passed else "FAIL",
            "growth_growth_diamonds_passed": gg_results["gate9_passed"],
            "source_birth_interleaving_passed": sb_results["gate9_passed"],
            "cone_internal_redistribution_passed": redist_results["gate9_passed"],
            "post_excitation_taxonomy_passed": post_exc_results["passed"],
            "runtime_under_30s": elapsed_total < 30.0,
        },
        "growth_growth_diamonds": {
            "max_N": gg_results["max_N"],
            "total_posets": gg_results["total_posets"],
            "total_diamonds_audited": gg_results["total_diamonds_audited"],
            "violations": gg_results["violations"],
            "max_discrepancy": gg_results["max_discrepancy"],
            "max_carrier_discrepancy": gg_results["max_carrier_discrepancy"],
            "breakdown_by_N": gg_breakdown_str,
            "passed": gg_results["gate9_passed"],
        },
        "source_birth_interleaving_diamonds": {
            "max_N": sb_results["max_N"],
            "formulation_A_newborn_diamonds": sb_results["formulation_A_newborn_diamonds"],
            "formulation_A_violations": sb_results["formulation_A_violations"],
            "formulation_A_max_diff": sb_results["formulation_A_max_diff"],
            "formulation_B_existing_diamonds": sb_results["formulation_B_existing_diamonds"],
            "formulation_B_violations": sb_results["formulation_B_violations"],
            "formulation_B_max_diff": sb_results["formulation_B_max_diff"],
            "breakdown_by_N": sb_breakdown_str,
            "passed": sb_results["gate9_passed"],
        },
        "cone_internal_redistribution": {
            "max_N": redist_results["max_N"],
            "total_anchor_checks": redist_results["total_anchor_checks"],
            "max_row_norm_error": redist_results["max_row_norm_error"],
            "max_spacelike_nondisturbance_error": redist_results["max_spacelike_nondisturbance_error"],
            "max_entry_probability_error": redist_results["max_entry_probability_error"],
            "passed": redist_results["gate9_passed"],
        },
        "post_excitation_diamond_taxonomy": post_exc_results,
    }

    if output_json_path is None:
        output_json_path = os.path.join(CURRENT_DIR, "stage9_carrier_experiment_results.json")

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2)

    print(f"\n[Artifact Exported]: {output_json_path}")
    return results_data


if __name__ == "__main__":
    results = run_stage9_verification()
    if not results["metadata"]["gate9_passed"]:
        sys.exit(1)
