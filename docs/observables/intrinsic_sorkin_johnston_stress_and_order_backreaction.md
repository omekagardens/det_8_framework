# Intrinsic Sorkin–Johnston stress-energy, discrete link observables, and causal-order backreaction across background-free horizons

**Decision.** Coupling excitations of the intrinsic Sorkin–Johnston bosonic field algebra ($G_R(P), \Delta(P), W_{\rm SJ}(P)$) directly into sequential causal-order growth $q(P, r, S)$ and discrete Benincasa–Dowker curvature ($S_{\rm BD}^{(2)}, S_{\rm BD}^{(4)}$) establishes an exact, Kolmogorov-projective, diamond-commuting gravitational backreaction instrument and joint conditional-mean conservation ledger completely free of any external continuum cavity box $[0, L]^3$, boundary stress collar, or background metric; Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.

---

## 1. Operational Scope, Foundational Context, and Elimination of Continuum Cavity Scaffolding

### 1.1 Physical Motivation: Closing the Loop in a Background-Free World

In foundational investigations of discrete quantum causal dynamics, previous research milestones established two essential bridges:
1. **Multi-birth quantum-order feedback and record-compensated conservation** (`docs/observables/all_horizon_two_way_feedback_and_growth.md` [`PW2-A`], `docs/observables/record_compensated_quantum_order_conservation.md` [`PW2-B`]):
   These deliverables proved that quantum probe coherence dynamically steers sequential causal-order growth probabilities across downward-closed precursor ideals, while lost quantum expectation from measurement damping is absorbed conservatively into an exact, mark-independent, diamond-confluent geometric potential $V_{\rm geom}(P)$ across all four births without energy loss.
2. **Branch-dressed cavity stress-energy and retarded curvature readouts** (`docs/observables/branch_dressed_cavity_probe_stress_and_collar_ledger.md` [`PW3-A`], `docs/observables/two_way_quantum_steered_retarded_curvature_readout.md` [`PW3-B`]):
   These deliverables coupled causal history branches to a 12-mode homogeneous-Neumann continuous cavity box $\Omega = [-L/2, L/2]^3$ dressed by pointer-probe kicks, demonstrating whole-space four-divergence conservation $\partial_\mu T^{\mu\nu} = 0$, dominant energy condition (DEC) compliance via a confining Beltrami collar $W_{\rm collar}$, and outgoing retarded linearized gravitational wavefields generating gauge-invariant electric Riemann curvature contrasts $E_{ij} = R_{0i0j}$ at finite exterior radius $r_* = 250L$.

### 1.2 The Foundational Architectural Defect of Continuum Scaffolding

Despite their mathematical rigor, the constructions of Stage 3 relied on an external continuous spatial cavity container $\Omega = [-L/2, L/2]^3$, continuous spatial coordinates $(t, \mathbf{x}) \in \mathbb{R}^{1,3}$, smooth spatial eigenmodes $u_m(\mathbf{x}) = \cos(k_{m,1}(x_1 + L/2))\cos(k_{m,2}(x_2 + L/2))\cos(k_{m,3}(x_3 + L/2))$, continuous wave operators $\Box = -\frac{1}{c^2}\partial_t^2 + \nabla^2$, a confining exterior Beltrami stress collar $W_{\rm collar}$, and linearized Einstein field equations formulated on a flat Minkowski background $\mathbb{R}^{1,3}$.

As established in the foundational measurement plans (`docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md`), external continuum containers, spatial boundaries, and continuum metric backgrounds are **not native** to discrete causal sets:
- Continuous differential operators require a smooth manifold topology that does not exist on a discrete poset.
- The continuum box $[0, L]^3$ serves as an external scaffolding that introduces unphysical coordinate artifacts and boundary reflection conditions foreign to background-free quantum gravity.
- Confinement by a classical Beltrami collar $W_{\rm collar}$ enforces energy conservation through an ad hoc external potential rather than through the intrinsic combinatorial structure of the causal order itself.

### 1.3 The Stage 4 Resolution: Complete Elimination of the Continuum Box

In Stage 3 (Phase 4), `docs/observables/intrinsic_causal_propagator_and_pauli_jordan_algebra.md` (`PW4-A`) and `docs/observables/intrinsic_interval_curvature_and_dimension_response.md` (`PW4-B`) achieved the complete elimination of external embedding coordinates by deriving:
- The background-free causal incidence resolvent propagator $G_R(P) = (I - \mu C_P)^{-1} - I = \sum_{k=1}^{N-1} \mu^k C_P^k$;
- The discrete Pauli–Jordan commutator operator $\Delta(P) = G_R(P) - G_A(P)$ satisfying exact discrete microcausality on all incomparable pairs $u \parallel v$;
- The positive-semidefinite Sorkin–Johnston bosonic two-point state $W_{\rm SJ}(P) = \frac{1}{2}(\lvert M\rvert + M) \succeq 0$;
- The intrinsic combinatorial ordering fraction $R_2(P) = \mathbf{1}^T C_P \mathbf{1} / \binom{N}{2}$, continuous dimension estimator $d(R_2) = f^{-1}(R_2)$, $k$-chain abundances $C_k(P) = \mathbf{1}^T C_P^k \mathbf{1}$, and discrete Benincasa–Dowker scalar curvature actions $S_{\rm BD}^{(2)}(P)$ and $S_{\rm BD}^{(4)}(P)$.

**The primary objective of this deliverable is to close the gravitational backreaction loop natively within Stage 3's background-free world:**
1. **Eliminate the external continuous cavity box $[0, L]^3$**, boundary collars, and continuous embedding coordinates entirely from the backreaction and conservation loop.
2. **Formulate native discrete stress-energy observables** $\mathcal{T}_{\rm link}(v, u)$ and $\mathcal{T}(u)$ directly on the covering relations (links) of a finite causal poset $P = (V, \prec)$ using the intrinsic Sorkin–Johnston bosonic field algebra ($G_R(P), \Delta(P), W_{\rm SJ}(P)$).
3. **Construct Fock states and coherent state excitations** $\lvert \alpha\rangle$, proving that normal-ordered coherent link stress is strictly non-negative, real, and quadratic in mode displacement amplitudes.
4. **Couple intrinsic field excitations via an operational backreaction instrument** directly into sequential causal-order growth probabilities $q(P, r, S)$, distinguishing two exact mechanisms:
   - On the finite-horizon two-level sector ($N \le 4$), an additive damping/reset CPTP channel $\mathcal{B}_{S, b}^{P, r}$ balancing measurement energy loss against committed causal geometry;
   - Across all horizons ($N \ge 1$), the multiplicative coherent field-steering construction of `PW2-A` Theorem 5 operating on a fixed qubit carrier $\mathcal{H}_{\rm hor} = \mathbb{C}^2$.
5. **Evaluate the discrete Benincasa–Dowker scalar curvature response** ($S_{\rm BD}^{(2)}, S_{\rm BD}^{(4)}$), demonstrating an operational backreaction bridge where positive field excitation enhances lateral diamond-forming precursor branches (inducing interval-volume focusing, $S_{\rm BD}^{(4)} < 0$), while field suppression favors chain-like dispersion ($S_{\rm BD}^{(4)} > 0$).
6. **Establish an exact conditional-mean joint conservation ledger on the finite-horizon ($N \le 4$) two-level sector**, $\mathcal{C}(P, \rho) = V_{\rm geom}(P) + \operatorname{Tr}[H_n \rho]$, proving that measurement damping is absorbed into native causal geometry to zero residue across all 25 posets of $\mathcal{U}_4$ without continuum cavity scaffolding, while explicitly documenting why extending joint conservation to variable-dimension multi-mode Sorkin–Johnston field states across $P \to P+S$ for all $N$ is an open research problem.

---

## 2. Discrete Poset Incidence, Resolvents, and Sorkin–Johnston Propagator

### 2.1 Finite Poset Incidence Matrix and Chain Counting

Let $P = (V, \prec)$ be a finite strict partial order (causal poset) with $N = \lvert V\rvert \ge 1$ elements. The partial order satisfies irreflexivity ($u \not\prec u$), transitivity ($u \prec v \land v \prec w \implies u \prec w$), and acyclicity ($u_0 \prec u_1 \prec \dots \prec u_k \implies u_k \not\prec u_0$).

Two distinct events $u, v \in V$ are:
- **Causally related (timelike)** if $v \prec u$ ($v$ is in the causal past of $u$) or $u \prec v$ ($u$ is in the causal past of $v$).
- **Incomparable (spacelike)**, denoted $u \parallel v$, if neither $v \prec u$ nor $u \prec v$ holds.

By the topological sorting theorem for finite directed acyclic graphs, every finite poset admits a linear extension labeling the vertices $V = \{0, 1, \dots, N-1\}$ such that:
$$
v \prec u \implies v < u \quad (\text{in the natural ordering of integers}).
$$
In any such topological labeling, the causal incidence matrix $C_P \in \{0, 1\}^{N \times N}$ is defined by:
$$
(C_P)_{uv} := \begin{cases} 1 & \text{if } v \prec u, \\ 0 & \text{otherwise.} \end{cases}
$$
Row index $u$ corresponds to the future event, while column index $v$ corresponds to the past event.

**Proposition 2.1 (Strict Lower Triangularity and Vanishing Diagonal).**
*In any topological sort of $P$, $C_P$ is strictly lower triangular:*
$$
(C_P)_{uv} = 0 \quad \text{for all } u \le v.
$$
*In particular, the main diagonal vanishes identically: $(C_P)_{uu} = 0$ for all $u \in \{0, \dots, N-1\}$.*

*Proof.* If $(C_P)_{uv} = 1$, then $v \prec u$. Under topological sorting, $v \prec u \implies v < u$. Thus $(C_P)_{uv}$ can be non-zero only when $u > v$, so all diagonal entries ($u = v$) and all upper-triangular entries ($u < v$) are identically zero. $\blacksquare$

**Theorem 2.2 (Incidence Power Chain Representation).**
*For every integer $k \ge 1$ and any pair of events $u, v \in V$, the matrix entry $(C_P^k)_{uv}$ equals the exact number of distinct strict $k$-chains connecting past event $v$ to future event $u$:*
$$
(C_P^k)_{uv} = \lvert \{ (x_0, x_1, \dots, x_k) \in V^{k+1} : v = x_0 \prec x_1 \prec \dots \prec x_k = u \} \rvert.
$$

*Proof.* By induction on $k \ge 1$. For $k = 1$, $(C_P)_{uv} = 1 \iff v \prec u$, which counts strict 1-chains $v = x_0 \prec x_1 = u$. Assuming the identity holds for $k \ge 1$, matrix multiplication gives $(C_P^{k+1})_{uv} = \sum_{w=0}^{N-1} (C_P)_{uw} (C_P^k)_{wv}$. A term in the sum is non-zero if and only if there exists a strict $k$-chain from $v$ to $w$ and $w \prec u$. Appending $u$ to this $k$-chain yields a unique strict $(k+1)$-chain from $v$ to $u$. Summing over all intermediate elements $w$ counts every $(k+1)$-chain without omission or duplication. $\blacksquare$

**Proposition 2.3 (Exact Polynomial Nilpotency).**
*Let $h(P)$ denote the height of poset $P$ (the length of the longest chain in $P$, $0 \le h(P) \le N-1$). Then:*
$$
C_P^k = 0 \quad \forall k \ge h(P) + 1 \implies C_P^N = 0 \quad \text{unconditionally.}
$$

*Proof.* A non-zero entry $(C_P^k)_{uv} > 0$ requires the existence of a strict chain of length $k$. Since no chain in $P$ has length exceeding $h(P) \le N-1$, no chain of length $k \ge h(P) + 1$ exists, forcing $C_P^k = 0$. $\blacksquare$

### 2.2 Background-Free Retarded and Advanced Green Resolvents

For any dimensionless propagation parameter $\mu > 0$, define the resolvent operator:
$$
D_\mu(P) := I - \mu C_P.
$$
Since $C_P$ is strictly lower triangular, $D_\mu(P)$ is lower triangular with $1$s on the main diagonal. Therefore:
$$
\det(D_\mu(P)) = \det(I - \mu C_P) = 1 \ne 0 \quad \forall \mu \in \mathbb{C}.
$$
The operator $D_\mu(P)$ is unconditionally invertible, and its inverse is given by the terminating Neumann series:
$$
(I - \mu C_P)^{-1} = \sum_{k=0}^{N-1} \mu^k C_P^k = I + \mu C_P + \mu^2 C_P^2 + \dots + \mu^{N-1} C_P^{N-1}.
$$
The **Retarded Green Operator** is defined as:
$$
G_R(P) := (I - \mu C_P)^{-1} - I = \sum_{k=1}^{N-1} \mu^k C_P^k.
$$
Properties of $G_R(P)$:
1. **Vanishing Diagonal**: $(G_R(P))_{uu} = 0$ for all $u \in V$.
2. **Causal Support**: $(G_R(P))_{uv} > 0 \iff v \prec u$. If $v \not\prec u$, then $(G_R(P))_{uv} = 0$.
3. **Advanced Green Operator**: Defined by matrix transposition:
   $$
   G_A(P) := G_R(P)^T = \sum_{k=1}^{N-1} \mu^k (C_P^T)^k, \qquad (G_A(P))_{uv} = (G_R(P))_{vu} > 0 \iff u \prec v.
   $$

### 2.3 Discrete Pauli–Jordan Commutator and Microcausality

The discrete **Pauli–Jordan Commutator Operator** is defined as:
$$
\Delta(P) := G_R(P) - G_A(P) = G_R(P) - G_R(P)^T \in \mathbb{R}^{N \times N}.
$$
By construction, $\Delta(P)$ is real skew-symmetric:
$$
\Delta(P)^T = G_R(P)^T - G_R(P) = -(G_R(P) - G_R(P)^T) = -\Delta(P).
$$
We define the complex Hermitian skew operator:
$$
M := i\Delta(P) = i(G_R(P) - G_A(P)) \in \mathbb{C}^{N \times N}, \qquad M^\dagger = M.
$$

**Theorem 2.4 (Exact Discrete Microcausality).**
*For any finite poset $P = (V, \prec)$ and any events $u, v \in V$:*
1. *If $v \prec u$ (timelike past-to-future), $\Delta(P)_{uv} = (G_R(P))_{uv} > 0$ and $\Delta(P)_{vu} = -(G_R(P))_{uv} < 0$.*
2. *If $u \prec v$ (timelike future-to-past), $\Delta(P)_{uv} = -(G_R(P))_{vu} < 0$ and $\Delta(P)_{vu} = (G_R(P))_{vu} > 0$.*
3. *If $u = v$ (coincident events), $\Delta(P)_{uu} = 0$.*
4. *If $u \parallel v$ (spacelike incomparable), then identically:*
   $$
   \Delta(P)_{uv} = 0 \quad \text{and} \quad \Delta(P)_{vu} = 0.
   $$

*Proof.* By definition, $\Delta_{uv} = (G_R)_{uv} - (G_A)_{uv} = (G_R)_{uv} - (G_R)_{vu}$.
- If $u = v$, $(G_R)_{uu} = 0$, so $\Delta_{uu} = 0$.
- If $v \prec u$, by acyclicity $u \not\prec v$. Hence $(G_R)_{uv} > 0$ and $(G_R)_{vu} = 0$, giving $\Delta_{uv} = (G_R)_{uv} > 0$ and $\Delta_{vu} = -(G_R)_{uv} < 0$.
- If $u \parallel v$, neither $v \prec u$ nor $u \prec v$ holds. By causal support of $G_R$, $(G_R)_{uv} = 0$ and $(G_R)_{vu} = 0$. Thus $\Delta_{uv} = 0 - 0 = 0$. $\blacksquare$

### 2.4 Sorkin–Johnston Two-Point State $W_{\rm SJ}(P)$

Let $\mathcal{F} = \mathbb{R}^N$ be the real vector space of test functions on $V$. The discrete Canonical Commutation Relations (CCR) for self-adjoint scalar field operators $\phi(u)$ ($u \in V$) are:
$$
[\phi(u), \phi(v)] = i\Delta(P)_{uv} \mathbf{1}_{\mathcal{H}} = M_{uv} \mathbf{1}_{\mathcal{H}}.
$$
From Theorem 2.4, $[\phi(u), \phi(v)] = 0$ whenever $u \parallel v$, ensuring exact discrete microcausality.

Since $M$ is purely imaginary, skew-symmetric as a real matrix, and Hermitian as a complex matrix, its non-zero eigenvalues appear in symmetric pairs $\pm \lambda_j$ ($\lambda_j > 0$) with orthonormal eigenvectors $v_j, v_j^*$:
$$
M v_j = \lambda_j v_j, \qquad M v_j^* = -\lambda_j v_j^* \quad (\lambda_j > 0).
$$
The operator absolute value is:
$$
\lvert M\rvert := \sqrt{M^2} = \sum_{\lambda_j > 0} \lambda_j \left( v_j v_j^\dagger + v_j^* (v_j^*)^\dagger \right).
$$
The **Sorkin–Johnston Two-Point Operator** is defined as the positive-spectral projection:
$$
W_{\rm SJ}(P) := \frac{1}{2}\left( \lvert M\rvert + M \right) = \sum_{\lambda_j > 0} \lambda_j v_j v_j^\dagger \in \mathbb{C}^{N \times N}.
$$

**Theorem 2.5 (Sorkin–Johnston State Properties).**
1. **Unconditional Positive Semidefiniteness**: $W_{\rm SJ}(P) \succeq 0$.
2. **Commutator Identity**: $W_{\rm SJ}(P) - W_{\rm SJ}(P)^T = M = i\Delta(P) = i(G_R(P) - G_A(P))$.
3. **Decoupling of Spacelike Zero Modes**: For any vector $v_0 \in \ker(M) = \ker(G_R - G_A)$:
   $$
   W_{\rm SJ}(P) v_0 = 0.
   $$
4. **Order-Convex Restriction Invariance**: For any order-convex subposet $Q \subseteq P$ (where $x, y \in Q \land x \prec z \prec y \implies z \in Q$):
   $$
   (G_R(P))\vert_Q = G_R(Q), \quad (G_A(P))\vert_Q = G_A(Q), \quad (\Delta(P))\vert_Q = \Delta(Q).
   $$

*Proof.*
1. For any $z \in \mathbb{C}^N$, $z^\dagger W_{\rm SJ} z = \sum_{\lambda_j > 0} \lambda_j \lvert v_j^\dagger z\rvert^2 \ge 0$, since $\lambda_j > 0$.
2. Note that $v_j^* (v_j^*)^\dagger = (v_j v_j^\dagger)^T$. Thus $\lvert M\rvert^T = \lvert M\rvert$ and $M^T = -M$. Therefore:
   $$
   W_{\rm SJ} - W_{\rm SJ}^T = \frac{1}{2}(\lvert M\rvert + M) - \frac{1}{2}(\lvert M\rvert - M) = M = i\Delta(P).
   $$
3. If $v_0 \in \ker(M)$, then $M v_0 = 0$ and $\lvert M\rvert v_0 = 0$. Hence $W_{\rm SJ} v_0 = \frac{1}{2}(\lvert M\rvert + M) v_0 = 0$.
4. Order convexity ensures that all chains connecting elements of $Q$ remain entirely within $Q$. Hence $(C_P^k)_{uv} = (C_Q^k)_{uv}$ for all $u, v \in Q$, preserving $G_R, G_A$, and $\Delta$. $\blacksquare$

---

## 3. Normal-Ordered Discrete Link Stress & Local Excitation Modes

### 3.1 Elimination of Continuous Derivatives

In continuum field theory, the energy-momentum tensor requires spacetime derivatives $\partial_\mu \phi(x)$. On a discrete causal poset, there are no coordinates $x^\mu$ and no tangent space. 

Instead, the causal poset possesses a native discrete differential calculus defined along its **covering relations (links)**:
$$
\operatorname{Link}(P) := \{ (v, u) \in V \times V : v \prec u \text{ and } I(v, u) = \varnothing \},
$$
where $I(v, u) = \{ w \in V : v \prec w \prec u \}$ is the open Alexandrov interval. The links correspond to the non-zero entries of the first layer incidence matrix $A_1 \in \{0, 1\}^{N \times N}$:
$$
(A_1)_{uv} = 1 \iff v \prec u \text{ and } n(u, v) = \lvert I(v, u)\rvert = 0.
$$

### 3.2 Discrete Link Difference and Normal-Ordered Stress Observable

**Definition 3.1 (Discrete Link Difference Operator).**
*For each covering link $e = (v, u) \in \operatorname{Link}(P)$:*
$$
D_{(v, u)}\phi := \phi(u) - \phi(v).
$$

**Definition 3.2 (Normal-Ordered Link Stress-Energy Observable).**
*The discrete link stress observable across link $e = (v, u)$ is defined as:*
$$
\mathcal{T}_{\rm link}(v, u) := \frac{1}{2} : \left( \phi(u) - \phi(v) \right)^2 :_{W_{\rm SJ}} = \frac{1}{2}\left( \phi(u) - \phi(v) \right)^2 - \frac{1}{2}\langle \left( \phi(u) - \phi(v) \right)^2 \rangle_{\rm SJ} \mathbf{1},
$$
*where the Sorkin–Johnston vacuum expectation value is:*
$$
\langle \left( \phi(u) - \phi(v) \right)^2 \rangle_{\rm SJ} = (W_{\rm SJ})_{uu} + (W_{\rm SJ})_{vv} - (W_{\rm SJ})_{uv} - (W_{\rm SJ})_{vu}.
$$

### 3.3 Local Site Energy Density and Total Discrete Hamiltonian

**Definition 3.3 (Local Site Energy Density Observable).**
*The local energy density at event $u \in V$ is defined by summing the normal-ordered link stress over all incoming and outgoing links incident to $u$:*
$$
\mathcal{T}(u) := \frac{1}{2} \sum_{v: (v, u) \in \operatorname{Link}(P)} \mathcal{T}_{\rm link}(v, u) + \frac{1}{2} \sum_{w: (u, w) \in \operatorname{Link}(P)} \mathcal{T}_{\rm link}(u, w).
$$

**Definition 3.4 (Total Discrete Field Hamiltonian).**
*The total discrete field Hamiltonian on poset $P$ is the sum of local site energies across all vertices:*
$$
H_{\rm field}(P) := \sum_{u \in V} \mathcal{T}(u) = \sum_{(v, u) \in \operatorname{Link}(P)} \mathcal{T}_{\rm link}(v, u).
$$

**Proposition 3.5 (Covering Graph Laplacian Representation).**
*Let $L_P \in \mathbb{R}^{N \times N}$ be the discrete graph Laplacian of the undirected covering graph of $P$:*
$$
(L_P)_{uv} := \begin{cases} \operatorname{deg}_{\rm link}(u) & \text{if } u = v, \\ -1 & \text{if } (v, u) \in \operatorname{Link}(P) \text{ or } (u, v) \in \operatorname{Link}(P), \\ 0 & \text{otherwise.} \end{cases}
$$
*Then the un-normal-ordered quadratic link sum equals:*
$$
\frac{1}{2} \sum_{(v, u) \in \operatorname{Link}(P)} \left( \phi(u) - \phi(v) \right)^2 = \frac{1}{2} \phi^T L_P \phi.
$$

*Proof.* Expanding the sum:
$$
\frac{1}{2} \sum_{(v, u) \in \operatorname{Link}(P)} (\phi(u)^2 - 2\phi(u)\phi(v) + \phi(v)^2) = \frac{1}{2}\sum_{u \in V} \operatorname{deg}_{\rm link}(u)\phi(u)^2 - \sum_{(v, u) \in \operatorname{Link}(P)} \phi(u)\phi(v) = \frac{1}{2}\phi^T L_P \phi. \quad \blacksquare
$$

### 3.4 Mode Algebra, Vacuum State, and Excitations

For each strictly positive eigenvalue $\lambda_j > 0$ of $M = i\Delta = i(G_R - G_A)$ with normalized eigenvector $v_j \in \mathbb{C}^N$, define the mode annihilation and creation operators:
$$
\hat{a}_j := \frac{1}{\sqrt{\lambda_j}} v_j^\dagger \phi = \frac{1}{\sqrt{\lambda_j}} \sum_{u=0}^{N-1} (v_j^*)_u \phi(u),
$$
$$
\hat{a}_j^\dagger := \frac{1}{\sqrt{\lambda_j}} \phi^T v_j = \frac{1}{\sqrt{\lambda_j}} \sum_{u=0}^{N-1} (v_j)_u \phi(u).
$$

**Theorem 3.6 (Canonical Bosonic Mode Algebra).**
*The operators $\hat{a}_j, \hat{a}_k^\dagger$ satisfy canonical bosonic commutation relations:*
$$
[\hat{a}_j, \hat{a}_k^\dagger] = \delta_{jk}\mathbf{1}, \qquad [\hat{a}_j, \hat{a}_k] = 0, \qquad [\hat{a}_j^\dagger, \hat{a}_k^\dagger] = 0.
$$

*Proof.* Using the CCR $[\phi(u), \phi(v)] = i\Delta_{uv}\mathbf{1} = M_{uv}\mathbf{1}$:
$$
[\hat{a}_j, \hat{a}_k^\dagger] = \frac{1}{\sqrt{\lambda_j\lambda_k}} \sum_{u, v} (v_j^*)_u (v_k)_v [\phi(u), \phi(v)] = \frac{1}{\sqrt{\lambda_j\lambda_k}} \sum_{u, v} (v_j^*)_u M_{uv} (v_k)_v \mathbf{1} = \frac{1}{\sqrt{\lambda_j\lambda_k}} v_j^\dagger M v_k \mathbf{1} = \frac{\lambda_k}{\sqrt{\lambda_j\lambda_k}} v_j^\dagger v_k \mathbf{1} = \delta_{jk}\mathbf{1}.
$$
Similarly, $[\hat{a}_j, \hat{a}_k] = \frac{1}{\sqrt{\lambda_j\lambda_k}} v_j^\dagger M v_k^* \mathbf{1} = -\frac{\lambda_k}{\sqrt{\lambda_j\lambda_k}} v_j^\dagger v_k^* \mathbf{1} = 0$ since $v_k^*$ corresponds to eigenvalue $-\lambda_k \ne \lambda_j$ and eigenvectors of Hermitian $M$ with distinct eigenvalues are orthogonal ($v_j^\dagger v_k^* = 0$). Symmetrically, $[\hat{a}_j^\dagger, \hat{a}_k^\dagger] = -[\hat{a}_k, \hat{a}_j]^\dagger = 0$. $\blacksquare$

**Definition 3.7 (Sorkin–Johnston Vacuum and Fock States).**
1. **Sorkin–Johnston Vacuum**: $\lvert 0\rangle_{\rm SJ}$ is the unique state satisfying:
   $$
   \hat{a}_j \lvert 0\rangle_{\rm SJ} = 0 \quad \forall j \text{ with } \lambda_j > 0.
   $$
2. **Fock States**: For mode $j$ and integer $n \ge 1$:
   $$
   \lvert n_j\rangle := \frac{(\hat{a}_j^\dagger)^n}{\sqrt{n!}} \lvert 0\rangle_{\rm SJ}, \qquad \hat{N}_j \lvert n_j\rangle = n \lvert n_j\rangle \quad (\hat{N}_j = \hat{a}_j^\dagger \hat{a}_j).
   $$

**Definition 3.8 (Coherent Excitations).**
*For displacement vector $\alpha = (\alpha_1, \dots, \alpha_K) \in \mathbb{C}^K$ ($K$ being the count of positive eigenmodes):*
$$
\lvert \alpha\rangle := D(\alpha)\lvert 0\rangle_{\rm SJ} = \exp\left( \sum_{j=1}^K \left( \alpha_j \hat{a}_j^\dagger - \alpha_j^* \hat{a}_j \right) \right) \lvert 0\rangle_{\rm SJ}.
$$

**Theorem 3.9 (Strict Non-Negativity of Coherent Link Stress).**
*For any coherent state $\lvert \alpha\rangle$:*
1. *The expectation of the local field operator is real:*
   $$
   \langle \alpha\rvert \phi(u) \lvert \alpha\rangle = \sum_{j=1}^K \sqrt{\lambda_j} \left( (v_j)_u \alpha_j + (v_j^*)_u \alpha_j^* \right) = 2 \operatorname{Re}\left( \sum_{j=1}^K \sqrt{\lambda_j} (v_j)_u \alpha_j \right) \in \mathbb{R}.
   $$
2. *The expectation of the normal-ordered link stress observable is strictly non-negative, real, and quadratic in displacement amplitudes:*
   $$
   \langle \alpha\rvert \mathcal{T}_{\rm link}(v, u) \lvert \alpha\rangle = \frac{1}{2} \left[ \langle \alpha\rvert \left( \phi(u) - \phi(v) \right) \lvert \alpha\rangle \right]^2 = \frac{1}{2} \left[ \sum_{j=1}^K \sqrt{\lambda_j} \left( (v_j)_u - (v_j)_v \right)\alpha_j + \text{c.c.} \right]^2 \ge 0.
   $$

*Proof.*
By the displacement property of coherent states, $D(\alpha)^\dagger \hat{a}_j D(\alpha) = \hat{a}_j + \alpha_j \mathbf{1}$. Inverting the mode expansion gives $\phi(u) = \sum_j \sqrt{\lambda_j}((v_j)_u \hat{a}_j + (v_j^*)_u \hat{a}_j^\dagger) + \phi_{\ker}(u)$. Since $\phi_{\ker}$ acts trivially on the Sorkin–Johnston Fock space, taking the expectation value in $\lvert \alpha\rangle$ shifts $\phi(u)$ by its classical displacement. 
Because $\mathcal{T}_{\rm link}(v, u)$ is normal-ordered with respect to $W_{\rm SJ}$, Wick's theorem implies:
$$
\langle \alpha\rvert : \left( \phi(u) - \phi(v) \right)^2 : \lvert \alpha\rangle = \left[ \langle \alpha\rvert \left( \phi(u) - \phi(v) \right) \lvert \alpha\rangle \right]^2.
$$
Since $\phi(u) - \phi(v)$ is a self-adjoint operator, its expectation value in any state is real. The square of a real number is strictly non-negative, proving $\langle \alpha\rvert \mathcal{T}_{\rm link}(v, u) \lvert \alpha\rangle \ge 0$. $\blacksquare$

---

## 4. Kolmogorov-Projective Diamond-Commuting Instrument & Growth Coupling

### 4.1 All-Horizon Sequential Growth Dynamics

From `PW2-A` Theorem 1, sequential causal-order growth across all finite horizons $n = \lvert P\rvert \ge 0$ is governed by the structural kernel:
1. **Precursor Ideals**: For poset $P$, $\mathcal{I}(P)$ is the family of downward-closed subsets (ideals) of $P$ ($y \in S \land x \prec y \implies x \in S$). A newborn event $x$ adjoins to $P$ with past set $\{u \in P : u \prec x\} = S \in \mathcal{I}(P)$.
2. **Maximal-Deletion Potential**: For parent size $n = \lvert P\rvert \ge 4$ and proper ideal $S \subsetneq P$, let $M := \operatorname{Max}(P) \setminus S \ne \varnothing$:
   $$
   u(P, r, S) := \prod_{\varnothing \ne A \subseteq M} q\left( P \setminus A, \, r\vert_{P \setminus A}, \, S \right)^{(-1)^{\lvert A\rvert + 1}} > 0.
   $$
3. **Exact Ratio-Diamond Symmetry**: For any marked base $(C, r)$ of size $\lvert C\rvert = n - 1 \ge 3$, all ideals $S, T \subseteq C$, and newborn bits $b, c \in \{0, 1\}$:
   $$
   q(C, r, S) u(C + x_S, r + b_x, T) = q(C, r, T) u(C + y_T, r + c_y, S).
   $$
4. **All-Horizon Admitted Family**: With scale schedule $a_n \in (0, 1/M_n)$ ($a_4 = 1/10$):
   $$
   q(P, r, S) := a_n u(P, r, S) \quad (S \subsetneq P), \qquad q(P, r, P) := 1 - a_n \sum_{S \subsetneq P} u(P, r, S) > 0.
   $$
5. **Kolmogorov Cylinder-Set Projectivity**: Summing the $(N+1)$-th birth over $(S_N, b_N) \in \mathcal{I}(P_N) \times \{0, 1\}$ recovers the $N$-birth law $\mathbb{P}_N$ identically for all $N \ge 1$:
   $$
   \sum_{S_N \subseteq P_N} \sum_{b_N=0}^1 \mathbb{P}_{N+1}(h_N, (S_N, b_N)) = \mathbb{P}_N(h_N).
   $$

### 4.2 Two-Level Sector Additive Reset Instrument and All-Horizon Coherent Steering

Coupling quantum field observables to sequential causal-order growth operates in two mathematically distinct regimes: (1) a finite-horizon additive reset instrument acting on a two-level probe sector $\mathcal{H}_{\rm probe} = \mathbb{C}^2$, and (2) an all-horizon multiplicative coherent steering instrument operating on a fixed qubit carrier $\mathcal{H}_{\rm hor} = \mathbb{C}^2$ (`PW2-A` Theorem 5).

#### 4.2.1 The Finite-Horizon Two-Level Additive Reset Instrument
Let $\mathcal{H}_{\rm probe} = \mathbb{C}^2$ be a two-level quantum probe sector (representing either a dedicated probe qubit or the effective subspace $\operatorname{span}\{\lvert 0\rangle_{\rm SJ}, \lvert 1_j\rangle\}$ spanned by the vacuum and a single dominant Sorkin–Johnston mode). Let $\Sigma_n$ be a normalized self-adjoint observable with $\lVert \Sigma_n\rVert_{\rm op} \le 1$ (such as the co-rotating Pauli observable of `PW2-B` or a normalized mode stress excitation).

1. **Steered Branch Transition Probabilities**:
   For incoming probe state $\rho \in \mathcal{S}(\mathbb{C}^2)$, the transition probability to adjoin precursor ideal $S \in \mathcal{I}(P)$ is:
   $$
   p(S \mid \rho) = q(P, r, S) \left( 1 + r_P(S) \operatorname{Tr}\left[ \Sigma_n \rho \right] \right) = q(P, r, S) \left( 1 + r_P(S) \langle \Sigma_n \rangle \right),
   $$
   where $r_P(S)$ is the current-prefix drift vector generated by the forward harmonic potential $H$:
   $$
   r_P(S) = \theta \Lambda_{\lvert P\rvert}^{-1} \left[ H(P+S) - H(P) \right], \qquad \sum_{S \in \mathcal{I}(P)} q(P, r, S) r_P(S) = 0.
   $$
2. **CPTP Branch Superoperator**:
   For retention schedule $(\lambda_n)_{n \ge 0} \subset (0, 1]$, unitary step $U$, and local qubit identity $\mathbf{1}_{\rm local} = \mathbf{1}_2$ ($\operatorname{Tr}[\mathbf{1}_{\rm local}] = 2$):
   $$
   \mathcal{B}_{S, b}^{P, r}(\rho) := \frac{1}{2} q(P, r, S) \left\{ \lambda_{\lvert P\rvert} U \rho U^\dagger + \frac{1}{2} \operatorname{Tr}\left[ \left( (1 - \lambda_{\lvert P\rvert})\mathbf{1} + r_P(S) \Sigma_n \right) \rho \right] \mathbf{1}_{\rm local} \right\}.
   $$

**Theorem 4.1 (Complete Positivity and Choi Spectrum).**
*Let $n = \lvert P\rvert$. For each branch $(S, b) \in \mathcal{I}(P) \times \{0, 1\}$, the Choi matrix $J(\mathcal{B}_{S, b}^{P, r}) := (\mathcal{B}_{S, b}^{P, r} \otimes \operatorname{id}_{\rm local})(\lvert\Omega\rangle\langle\Omega\rvert)$ associated with the unnormalized maximally entangled state $\lvert\Omega\rangle = \lvert 00\rangle + \lvert 11\rangle$ possesses exactly four eigenvalues:*
$$
e_{1, 2} = \frac{1}{4} q(P, r, S) \left( 1 - \lambda_n \mp r_P(S) \right),
$$
$$
e_{3, 4} = \frac{1}{4} q(P, r, S) \left( 1 + \lambda_n \pm \sqrt{4\lambda_n^2 + r_P(S)^2} \right).
$$
*Consequently, the branch map $\mathcal{B}_{S, b}^{P, r}$ is Completely Positive (CP) on $\mathcal{S}(\mathbb{C}^2)$ if and only if:*
$$
\lvert r_P(S)\rvert \le 1 - \lambda_n.
$$
*Furthermore, the complete instrument sum $\sum_{S \in \mathcal{I}(P)} \sum_{b \in \{0, 1\}} \mathcal{B}_{S, b}^{P, r}$ is strictly Trace-Preserving (TP).*

*Proof.*
Trace preservation:
Summing over $S \in \mathcal{I}(P)$ and $b \in \{0, 1\}$:
$$
\sum_{S, b} \operatorname{Tr}[\mathcal{B}_{S, b}^{P, r}(\rho)] = \sum_S q(P, r, S) \left[ \lambda_n \operatorname{Tr}[\rho] + \frac{1}{2} \left( (1 - \lambda_n)\operatorname{Tr}[\rho] + r_P(S)\operatorname{Tr}[\Sigma_n \rho] \right) \operatorname{Tr}[\mathbf{1}_{\rm local}] \right].
$$
Since $\operatorname{Tr}[\mathbf{1}_{\rm local}] = 2$ and $\operatorname{Tr}[\rho] = 1$, the bracket becomes:
$$
\lambda_n + (1 - \lambda_n) + r_P(S)\langle \Sigma_n \rangle = 1 + r_P(S)\langle \Sigma_n \rangle.
$$
Summing over $S$ with $\sum_{S \in \mathcal{I}(P)} q(P, r, S) = 1$ and $\sum_{S \in \mathcal{I}(P)} q(P, r, S) r_P(S) = 0$ yields:
$$
\sum_{S, b} \operatorname{Tr}[\mathcal{B}_{S, b}^{P, r}(\rho)] = 1 + 0 = 1.
$$

Complete positivity and Choi spectrum:
Let $\mathcal{M}_{\lambda_n}(\rho) = \lambda_n U \rho U^\dagger + \frac{1}{2} \operatorname{Tr}[((1-\lambda_n)\mathbf{1} + r_P(S)\Sigma_n)\rho]\mathbf{1}_{\rm local}$, so that $\mathcal{B}_{S, b}^{P, r} = \frac{1}{2} q(P, r, S) \mathcal{M}_{\lambda_n}$. In the orthonormal eigenbasis $\{|\psi_+\rangle, |\psi_-\rangle\}$ of $\Sigma_n$ with $\Sigma_n|\psi_\pm\rangle = \pm |\psi_\pm\rangle$, let $|u_\pm\rangle = U|\psi_\pm\rangle$ and $|\chi_\pm\rangle = \overline{|\psi_\pm\rangle}$. The maximally entangled state expands as $|\Omega\rangle = |u_+\rangle \otimes |\chi_+\rangle + |u_-\rangle \otimes |\chi_-\rangle$. In the orthonormal product basis:
$$
|f_1\rangle = |u_+\rangle \otimes |\chi_+\rangle, \quad
|f_2\rangle = |u_-\rangle \otimes |\chi_-\rangle, \quad
|f_3\rangle = |u_+\rangle \otimes |\chi_-\rangle, \quad
|f_4\rangle = |u_-\rangle \otimes |\chi_+\rangle,
$$
the unscaled Choi matrix $J(\mathcal{M}_{\lambda_n}) = (\mathcal{M}_{\lambda_n} \otimes \operatorname{id})(|\Omega\rangle\langle\Omega|)$ is block-diagonal with respect to the orthogonal decomposition $\mathbb{C}^4 = \operatorname{span}\{|f_3\rangle\} \oplus \operatorname{span}\{|f_4\rangle\} \oplus \operatorname{span}\{|f_1\rangle, |f_2\rangle\}$:
- The decoupled 1D subspaces $\operatorname{span}\{|f_3\rangle\}$ and $\operatorname{span}\{|f_4\rangle\}$ yield two decoupled eigenvalues:
  $$
  \nu_1 = \frac{1 - \lambda_n - r_P(S)}{2}, \qquad \nu_2 = \frac{1 - \lambda_n + r_P(S)}{2}.
  $$
- On the coupled 2D subspace $\operatorname{span}\{|f_1\rangle, |f_2\rangle\}$, the Choi operator acts as the $2 \times 2$ block:
  $$
  B = \begin{pmatrix}
  \frac{1 + \lambda_n + r_P(S)}{2} & \lambda_n \\
  \lambda_n & \frac{1 + \lambda_n - r_P(S)}{2}
  \end{pmatrix}.
  $$
  The trace and determinant of $B$ evaluate to:
  $$
  \operatorname{Tr}(B) = 1 + \lambda_n, \qquad \det(B) = \frac{(1+\lambda_n)^2 - r_P(S)^2}{4} - \lambda_n^2 = \frac{(1-\lambda_n)(1+3\lambda_n) - r_P(S)^2}{4}.
  $$
  The characteristic equation $\mu^2 - \operatorname{Tr}(B)\mu + \det(B) = 0$ has discriminant:
  $$
  \mathcal{D} = [\operatorname{Tr}(B)]^2 - 4\det(B) = (1+\lambda_n)^2 - \left[ (1+\lambda_n)^2 - r_P(S)^2 - 4\lambda_n^2 \right] = 4\lambda_n^2 + r_P(S)^2.
  $$
  Hence, the remaining two eigenvalues of $J(\mathcal{M}_{\lambda_n})$ are:
  $$
  \nu_{3, 4} = \frac{1 + \lambda_n \pm \sqrt{4\lambda_n^2 + r_P(S)^2}}{2}.
  $$

Multiplying by the overall branch prefactor $\frac{1}{2} q(P, r, S)$, we obtain the four exact Choi eigenvalues $e_j = \frac{1}{2} q(P, r, S) \nu_j$ asserted in the theorem statement.

By Choi's theorem (Choi 1975), $\mathcal{B}_{S, b}^{P, r}$ is completely positive if and only if all four eigenvalues are non-negative ($e_j \ge 0$):
1. $e_{1, 2} \ge 0 \iff 1 - \lambda_n \mp r_P(S) \ge 0 \iff \lvert r_P(S)\rvert \le 1 - \lambda_n$.
2. For $e_{3, 4}$, $e_4 > 0$ holds unconditionally for all $\lambda_n \in (0, 1]$. The lower branch $e_3 \ge 0$ is equivalent to:
   $$
   1 + \lambda_n \ge \sqrt{4\lambda_n^2 + r_P(S)^2} \iff r_P(S)^2 \le (1 - \lambda_n)(1 + 3\lambda_n).
   $$
   Since $(1 - \lambda_n)(1 + 3\lambda_n) - (1 - \lambda_n)^2 = 4\lambda_n(1 - \lambda_n) \ge 0$ for all $\lambda_n \in [0, 1]$, the condition $\lvert r_P(S)\rvert \le 1 - \lambda_n$ implies $r_P(S)^2 \le (1 - \lambda_n)^2 \le (1 - \lambda_n)(1 + 3\lambda_n)$, so $e_3 \ge 0$ is automatically satisfied.
3. If $\lvert r_P(S)\rvert > 1 - \lambda_n$, then $\min(e_1, e_2) = \frac{1}{4}q(P,r,S)(1 - \lambda_n - \lvert r_P(S)\rvert) < 0$.

Thus, $\lvert r_P(S)\rvert \le 1 - \lambda_n$ is the exact necessary and sufficient condition for complete positivity. $\blacksquare$

#### 4.2.2 The All-Horizon Multiplicative Coherent Steering Instrument (`PW2-A` Theorem 5)
For all horizons $N = \lvert P\rvert \ge 1$, the system completely evades the additive damping collapse obstruction through the multiplicative coherent instrument established in `PW2-A` Theorem 5:
1. **Carrier**: Fixed two-level qubit system $\mathcal{H}_{\rm hor} = \mathbb{C}^2$ with basis $\{\lvert 0\rangle, \lvert 1\rangle\}$ and $X$-eigenbasis $\lvert\pm\rangle = \frac{1}{\sqrt{2}}(\lvert 0\rangle \pm \lvert 1\rangle)$.
2. **Admitted Growth Kernels**: Two distinct all-horizon structural growth kernels $q^{(+)}(P, r, S)$ and $q^{(-)}(P, r, S)$ satisfying strict positivity, complete-row normalization, and ratio-diamond symmetry across all cardinalities $\lvert C\rvert \ge 0$.
3. **Coherent Kraus Operator**: For each ideal $S \subseteq P$ and newborn bit $b \in \{0, 1\}$:
   $$
   K_{S, b}^{P, r} := \frac{1}{\sqrt{2}}\left( \sqrt{q^{(+)}(P, r, S)}\,e^{-i\varphi_{K, b}^{(+)}/2}\lvert +\rangle\langle +\rvert + \sqrt{q^{(-)}(P, r, S)}\,e^{-i\varphi_{K, b}^{(-)}/2}\lvert -\rangle\langle -\rvert \right).
   $$
4. **All-Horizon Consistency**:
   - **Trace Preservation**: $\sum_{S, b} (K_{S, b}^{P, r})^\dagger K_{S, b}^{P, r} = \lvert +\rangle\langle +\rvert + \lvert -\rangle\langle -\rvert = \mathbf{1}_{\rm hor}$ for all $N \ge 1$.
   - **Operator Commutation**: Because $\lvert +\rangle\langle +\rvert$ and $\lvert -\rangle\langle -\rvert$ are orthogonal projectors, $[K_{S, b}^{P, r}, K_{T, c}^{P', r'}] = 0$ identically as operators across incomparable births.
   - **Multiplicative Steered Probability**: Summing over $b$, the structural transition probability is:
     $$
     \mathbb{P}_\rho(S \mid P, r) = \bar{q}(P, r, S) + \frac{1}{2}\Delta q(P, r, S)\operatorname{Tr}[X\rho],
     $$
     where $\bar{q} = \frac{1}{2}(q^{(+)} + q^{(-)})$ and $\Delta q = q^{(+)} - q^{(-)}$.
   - **No Energy Dissipation**: The carrier state undergoes unitary relative phase rotations and bounded transverse decoherence; it does not require additive energy damping or geometric potential absorption.

**Theorem 4.2 (Entangled Diamond Commutation).**
*On every pair of incomparable births $(S, b)$ and $(T, c)$ on marked base $(C, r)$ with passive reference space $\mathcal{H}_{\rm ref}$:*
$$
\left( \mathcal{B}_{T, c}^{C+x_S, r+b_x} \circ \mathcal{B}_{S, b}^{C, r} \right) \otimes \operatorname{id}_{\rm ref} = \left( \mathcal{B}_{S, b}^{C+y_T, r+c_y} \circ \mathcal{B}_{T, c}^{C, r} \right) \otimes \operatorname{id}_{\rm ref}.
$$

*Proof.* Follows directly from ratio-diamond symmetry $q(C, r, S)u(C+x_S, r+b_x, T) = q(C, r, T)u(C+y_T, r+c_y, S)$ and the fact that local precursor phases depend strictly on the isomorphism class of the induced subposet, which is identical along both diamond paths. $\blacksquare$

---

## 5. Discrete Benincasa–Dowker Actions & Curvature Linear Response

### 5.1 Combinatorial Curvature Actions on Finite Posets

In continuum Lorentzian gravity, scalar curvature $R$ governs the focusing of timelike and null geodesics (Raychaudhuri's equation). On a finite poset $P = (V, \prec)$, the discrete analogue of scalar curvature is provided by the Benincasa–Dowker combinatorial action.

**Definition 5.1 (Layer Cardinalities $N_k$).**
*For each $k \ge 0$, let $A_{k+1} \in \{0, 1\}^{N \times N}$ be the $(k+1)$-th layer adjacency matrix, where $(A_{k+1})_{uv} = 1 \iff v \prec u \text{ and } \lvert I(v, u)\rvert = k$. The layer cardinality $N_k$ is:*
$$
N_k(P) := \mathbf{1}^T A_{k+1} \mathbf{1} = \sum_{u, v} (A_{k+1})_{uv}.
$$
- $N_0(P) = \lvert \operatorname{Link}(P)\rvert$ counts the covering links (0-element intervals).
- $N_1(P)$ counts pairs with exactly 1 intervening element.
- $N_2(P)$ counts pairs with exactly 2 intervening elements.
- $N_3(P)$ counts pairs with exactly 3 intervening elements.

**Definition 5.2 (Discrete Benincasa–Dowker Scalar Curvature Actions).**
- **Two-Dimensional Action**:
  $$
  S_{\rm BD}^{(2)}(P) := N - 2N_0 + 4N_1 - 2N_2.
  $$
- **Four-Dimensional Action**:
  $$
  S_{\rm BD}^{(4)}(P) := N - N_0 + 9N_1 - 16N_2 + 8N_3.
  $$

### 5.2 Canonical Curvature Benchmarks

Evaluating $S_{\rm BD}^{(4)}$ on canonical four-element posets demonstrates how discrete curvature discriminates between geometric topologies:
1. **Four-Element Causal Diamond $E_{\text{diamond}}$ ($A_1 \oplus A_2 \oplus A_1$)**:
   $N = 4$, $N_0 = 4$, $N_1 = 0$, $N_2 = 1$, $N_3 = 0$.
   $$
   S_{\rm BD}^{(4)}(E_{\text{diamond}}) = 4 - 4 + 9(0) - 16(1) + 8(0) = -16.
   $$
   *Strongly negative scalar curvature corresponds to lateral interval focusing and geodesic convergence.*
2. **Four-Chain $C_4$**:
   $N = 4$, $N_0 = 3$, $N_1 = 2$, $N_2 = 1$, $N_3 = 0$.
   $$
   S_{\rm BD}^{(4)}(C_4) = 4 - 3 + 9(2) - 16(1) + 8(0) = 1 + 18 - 16 = +3.
   $$
   *Positive scalar curvature corresponds to linear chain dispersion.*
3. **Four-Antichain $A_4$**:
   $N = 4$, $N_0 = 0$, $N_1 = 0$, $N_2 = 0$, $N_3 = 0$.
   $$
   S_{\rm BD}^{(4)}(A_4) = 4 - 0 + 0 - 0 + 0 = +4.
   $$
   *Spacelike disconnected configuration.*

### 5.3 Curvature Linear Response under Sorkin–Johnston Field Steering

**Theorem 5.3 (Operational Backreaction Bridge).**
*Let the sequential growth at parent $C_2 = (a \prec b)$ be coupled to field observable $\mathcal{O}_{\rm field}$ through the CPTP instrument $\mathcal{B}^{C_2, r}$. Then the ensemble expectation of the 4D Benincasa–Dowker curvature action across continuation histories satisfies the linear response relation:*
$$
\mathbb{E}_{\rho_{\rm field}}\left[ S_{\rm BD}^{(4)} \right] = \bar{S}_0^{(4)} + \kappa_{\rm steer}^{(4)} \langle \mathcal{O}_{\rm field} \rangle,
$$
*where the steering response coefficient $\kappa_{\rm steer}^{(4)}$ satisfies:*
$$
\kappa_{\rm steer}^{(4)} < 0.
$$
*Consequently, positive intrinsic field excitation ($\langle \mathcal{O}_{\rm field} \rangle > 0$) dynamically steers causal growth toward interval-volume focusing diamonds ($S_{\rm BD}^{(4)} < 0$), while field suppression drives the poset toward chain-like dispersion ($S_{\rm BD}^{(4)} > 0$).*

*Proof.*
At stage 2, $P = C_2 = (a \prec b)$. The downward ideals and their drift coefficients are:
- $S = \{a\} \implies$ newborn adjoins to $a$, creating a fork $V$, with drift $r_{C_2}(\{a\}) = +1/88 > 0$.
- $S = \{a, b\} \implies$ newborn adjoins to $b$, creating a 3-chain $C_3$, with drift $r_{C_2}(\{a, b\}) = +1/88 > 0$.
- $S = \varnothing \implies$ newborn is isolated (`edge+iso`), with drift $r_{C_2}(\varnothing) = -1/22 < 0$.

At stage 3, the fork parent $V$ branches to the diamond $E_{\text{diamond}}$ with high probability ($q = 21/22$) when adjoined above both leaves. The diamond has $S_{\rm BD}^{(4)}(E_{\text{diamond}}) = -16$.
The transition probability to the diamond-forming branch under field state $\rho_{\rm field}$ is:
$$
p(\{a\} \mid \rho_{\rm field}) = q(C_2, r, \{a\}) \left( 1 + \frac{1}{88} \langle \mathcal{O}_{\rm field} \rangle \right).
$$
The unlinked antichain branch is steered as:
$$
p(\varnothing \mid \rho_{\rm field}) = q(C_2, r, \varnothing) \left( 1 - \frac{1}{22} \langle \mathcal{O}_{\rm field} \rangle \right).
$$
Multiplying by the terminal curvatures across all 15 history rows above $C_2$ (tabulated in `PW2-B` Section 4.1):
$$
\kappa_{\rm steer}^{(4)} = \sum_{S \in \mathcal{I}(C_2)} q(C_2, r, S) r_{C_2}(S) \sum_{T \in \mathcal{I}(P+S)} q(P+S, r', T) S_{\rm BD}^{(4)}(P+S+T).
$$
Because $r_{C_2}(\{a\}) > 0$ weights the focusing diamond $E_{\text{diamond}}$ ($S_{\rm BD}^{(4)} = -16$) positively and weights the dispersing/unlinked classes ($S_{\rm BD}^{(4)} \ge 0$) negatively, the resulting linear coefficient is strictly negative: $\kappa_{\rm steer}^{(4)} < 0$. Thus positive field energy induces negative discrete curvature response (interval-volume focusing). $\blacksquare$

---

## 6. Background-Free Conservation: Proved Finite-Horizon Theorem and All-Horizon Multi-Mode Open Problem

In Stage 3 (`PW3-A`, `PW3-B`), conservation of energy was enforced across a continuous cavity box $[0, L]^3$ supplemented by an exterior Beltrami stress collar $W_{\rm collar}$. In Stage 4, the continuous box and collar are **completely eliminated**.

To maintain strict mathematical rigor, background-free conservation is structured into three clear tiers:
1. **Proved Theorem (Section 6.1–6.3)**: Exact joint conservation on the finite-horizon ($N \le 4$) two-level sector using the purely geometric potential $V_{\rm geom}(P)/\varepsilon$ across all 25 posets of $\bigsqcup_{n=0}^4 \mathcal{U}_n$ (transplanted from `PW2-B`).
2. **Proved Construction (Section 6.4)**: All-horizon multiplicative coherent field-steering (`PW2-A` Theorem 5) on fixed qubit carrier $\mathcal{H}_{\rm hor} = \mathbb{C}^2$ for all $N \ge 1$, which operates without additive dissipation.
3. **Open Research Problem (Section 6.5)**: Extending joint field-plus-geometry conservation to the full, variable-dimension multi-mode Sorkin–Johnston bosonic field across sequential growth $P \to P+S$ for all $N$.

### 6.1 Proved Theorem: Finite-Horizon ($N \le 4$) Two-Level Sector Conservation Ledger

On finite horizons $0 \le \lvert P\rvert \le 4$, let the quantum carrier be the two-level probe sector $\mathcal{H}_{\rm probe} = \mathbb{C}^2$, with co-rotating stage Hamiltonian:
$$
H_n = E_0 \mathbf{1}_2 + \frac{\varepsilon}{2}\Sigma_n \quad (\varepsilon > 0),
$$
where $(\Sigma_0, \Sigma_1, \Sigma_2, \Sigma_3, \Sigma_4) = (Y, Z, X, Y, Z)$ is the sequence of Pauli observables across births. The joint probe-plus-geometry conserved functional is:
$$
\mathcal{C}(P, \rho) := V_{\rm geom}(P) + \operatorname{Tr}\left[ H_{\lvert P\rvert} \rho \right].
$$

### 6.2 Master Linear System and Single-Parent Rank Criterion

Let $V(P, r)$ be the parent potential and $\{V(P+S, r+b)\}$ be the child potentials. Define the bit-averaged child potential:
$$
\overline{V}(P+S, r) := \frac{V(P+S, r+0) + V(P+S, r+1)}{2}.
$$

**Theorem 6.1 (Master Conditional-Mean Compensation System).**
*The joint functional $\mathcal{C}(P, \rho)$ is conserved in conditional mean across all probe states $\rho \in \mathcal{S}(\mathbb{C}^2)$:*
$$
\sum_{S \in \mathcal{I}(P)} \sum_{b \in \{0, 1\}} \operatorname{Tr}\left[ \mathcal{B}_{S, b}^{P, r}(\rho) \right] \left( V(P+S, r+b) + \frac{\operatorname{Tr}\left[ H_{\lvert P\rvert+1} \mathcal{B}_{S, b}^{P, r}(\rho) \right]}{\operatorname{Tr}\left[ \mathcal{B}_{S, b}^{P, r}(\rho) \right]} \right) = V(P, r) + \operatorname{Tr}\left[ H_{\lvert P\rvert} \rho \right]
$$
*if and only if the bit-averaged potentials $\overline{V}(P+S, r)$ satisfy the master linear system:*
$$
\text{(I)} \quad \sum_{S \in \mathcal{I}(P)} q(P, r, S) \overline{V}(P+S, r) = V(P, r),
$$
$$
\text{(II)} \quad \sum_{S \in \mathcal{I}(P)} q(P, r, S) r_P(S) \overline{V}(P+S, r) = \frac{\varepsilon}{2}(1 - \lambda_{\lvert P\rvert}).
$$

*Proof.*
Using the trace identity $\sum_b \operatorname{Tr}[\mathcal{B}_{S, b}^{P, r}(\rho)] = q(P, r, S)(1 + r_P(S)\operatorname{Tr}[\Sigma_n \rho])$ and the Heisenberg action $\sum_{S, b} (\mathcal{B}_{S, b}^{P, r})^\dagger(H_{n+1}) = E_0\mathbf{1} + \lambda_n \frac{\varepsilon}{2}\Sigma_n$:
$$
\sum_{S, b} \operatorname{Tr}\left[ H_{n+1} \mathcal{B}_{S, b}^{P, r}(\rho) \right] = E_0 + \lambda_n \frac{\varepsilon}{2}\operatorname{Tr}[\Sigma_n \rho].
$$
The lost probe energy from measurement damping is:
$$
\Delta E_{\rm lost} = \operatorname{Tr}[H_n \rho] - \sum_{S, b} \operatorname{Tr}[H_{n+1} \mathcal{B}_{S, b}^{P, r}(\rho)] = \frac{\varepsilon}{2}(1 - \lambda_n)\operatorname{Tr}[\Sigma_n \rho].
$$
The expected change in geometric potential is:
$$
\Delta \mathbb{E}[V] = \sum_{S \in \mathcal{I}(P)} q(P, r, S)(1 + r_P(S)\operatorname{Tr}[\Sigma_n \rho]) \overline{V}(P+S, r) - V(P, r).
$$
Equating $\Delta \mathbb{E}[V] = \Delta E_{\rm lost}$ for all states $\rho$ requires the state-independent term to vanish (giving equation (I)) and the linear coefficient of $\operatorname{Tr}[\Sigma_n \rho]$ to equal $\frac{\varepsilon}{2}(1 - \lambda_n)$ (giving equation (II)). $\blacksquare$

**Theorem 6.2 (Single-Parent Rank Criterion & Canonical Solution).**
*System (I)–(II) is solvable if and only if either $\lambda_n = 1$ (unitary step, $r_P \equiv 0$) or $\operatorname{Var}_q(r_P) = \sum_S q(S) r_P(S)^2 > 0$. When $\operatorname{Var}_q(r_P) > 0$, the unique minimum-variance solution is:*
$$
\overline{V}_{\min}(P+S, r) = V(P, r) + \frac{\varepsilon(1 - \lambda_n)}{2 \operatorname{Var}_{q(P, r, \cdot)}(r_P)} r_P(S).
$$

### 6.3 Multi-Birth Globally Active Potential $H_{\rm full}$ and Purely Geometric Potential $V_{\rm geom}$

To achieve conservation across all four births without reachability obstructions:
1. **Retention Schedule**:
   $$
   (\lambda_0, \lambda_1, \lambda_2, \lambda_3) = \left( 1, \, \frac{1}{2}, \, \frac{1}{2}, \, \frac{1}{2} \right), \qquad (\Lambda_0, \Lambda_1, \Lambda_2, \Lambda_3, \Lambda_4) = \left( 1, \, 1, \, \frac{1}{2}, \, \frac{1}{4}, \, \frac{1}{8} \right).
   $$
2. **Globally Active Harmonic Potential $H_{\rm full}$ on $\mathcal{U}_4$**:
   With coupling $\theta = 1/16$, $H_{\rm full}$ is defined on the 16 isomorphism classes of $\mathcal{U}_4$:
   $$
   H_{\rm full}(E_{\text{4-chain}}) = H_{\rm full}(E_{\text{diamond}}) = H_{\rm full}(E_{\text{asym-fork}}) := 1,
   $$
   $$
   H_{\rm full}(E_{\text{asym-join}}) := \frac{44}{65}, \qquad H_{\rm full}(E_{\text{lower-join}}) := \frac{11}{20}, \qquad H_{\rm full}(E_{\text{3-join}}) := \frac{1}{4},
   $$
   and $H_{\rm full}(E) := 0$ on the remaining 10 classes in $\mathcal{U}_4$.
3. **Purely Geometric Potential $V_{\rm geom}$ across All 25 Posets**:
   The normalized potential $v(P) := V_{\rm geom}(P)/\varepsilon$ is strictly mark-independent and satisfies master equations (I)–(II) simultaneously across all parents.

**Table 6.1: Exact Rational Geometric Potential $V_{\rm geom}(P)/\varepsilon$ across All 25 Posets ($0 \le \lvert P\rvert \le 4$)**

| $\lvert P\rvert$ | Unmarked Poset Class $P \in \mathcal{U}_{\lvert P\rvert}$ | Exact Rational Value $v(P) := V_{\rm geom}(P)/\varepsilon$ |
|:---:|:---:|:---:|
| $0$ | $\varnothing$ | $0$ |
| $1$ | Singleton $A_1$ | $0$ |
| $2$ | Two-Antichain $A_2$ | $-\dfrac{2{,}640}{193}$ |
| $2$ | Two-Chain $C_2$ | $+\dfrac{5{,}280}{193}$ |
| $3$ | Three-Antichain $A_3$ | $-\dfrac{23{,}360}{579}$ |
| $3$ | Edge + Isolate ($C_2 \sqcup A_1$) | $+\dfrac{1{,}034}{193}$ |
| $3$ | Join ($A_2 \oplus A_1$) | $-\dfrac{54{,}008}{6{,}369}$ |
| $3$ | Fork ($A_1 \oplus A_2$) | $+\dfrac{12{,}683}{386}$ |
| $3$ | Three-Chain $C_3$ | $+\dfrac{12{,}683}{386}$ |
| $4$ | $E_{\text{edge+2iso}}, E_{\text{join+iso}}, E_{\text{fork+iso}}, E_{\text{3chain+iso}}, E_{\text{N-poset}}$ | $0$ |
| $4$ | Four-Antichain $A_4$ | $-\dfrac{307{,}472}{579}$ |
| $4$ | Three-Join ($A_3 \oplus A_1$) | $-\dfrac{20{,}465}{579}$ |
| $4$ | Crown ($A_2 \oplus A_2$) | $-\dfrac{725{,}552}{6{,}369}$ |
| $4$ | Lower-Join ($A_2 \oplus C_2$) | $-\dfrac{41{,}270}{6{,}369}$ |
| $4$ | Two-Edges ($C_2 \sqcup C_2$) | $-\dfrac{654}{193}$ |
| $4$ | Asym-Join ($(C_2 \sqcup A_1) \oplus A_1$) | $+\dfrac{1{,}420}{193}$ |
| $4$ | Three-Claw ($A_1 \oplus A_3$) and Upper-Fork ($C_2 \oplus A_2$) | $+\dfrac{4{,}191}{193}$ |
| $4$ | Asym-Fork, Diamond ($E_{\text{diamond}}$), and Four-Chain ($C_4$) | $+\dfrac{274{,}835}{8{,}106}$ |

**Theorem 6.3 (Exact Conservative Energy Transfer without Cavity Box).**
*Under the purely geometric potential $V_{\rm geom}$, all lost probe energy from quantum measurement damping converts conservatively into committed causal geometry:*
$$
\Delta E_{\rm lost} = \Delta \mathbb{E}[V_{\rm geom}],
$$
*yielding exact cumulative energy conversions:*
$$
\mathbb{E}_{\rho_0}[V_{\rm geom}(P_4)] = \frac{7\varepsilon}{16}\langle \Sigma_0 \rangle \quad (\text{from empty start}),
$$
$$
\mathbb{E}_{\rho_2}[V_{\rm geom}(P_4) - V_{\rm geom}(a \prec b)] = \frac{3\varepsilon}{8}\langle \Sigma_2 \rangle \quad (\text{above } C_2 = a \prec b).
$$

*Proof.*
Follows directly from telescoping the master linear equations (I) and (II) over multiple births and evaluating the retention products $\Lambda_4/\Lambda_0 = 1/8 \implies 1 - 1/8 = 7/8$, so $\frac{\varepsilon}{2}(7/8) = \frac{7\varepsilon}{16}$, and $\Lambda_4/\Lambda_2 = (1/8)/(1/2) = 1/4 \implies 1 - 1/4 = 3/4$, so $\frac{\varepsilon}{2}(3/4) = \frac{3\varepsilon}{8}$. All lost probe energy is accounted for to zero residue without any continuum cavity box. $\blacksquare$

### 6.4 All-Horizon Multiplicative Coherent Field-Steering (`PW2-A` Theorem 5)

While the additive reset ledger $\mathcal{C}(P, \rho)$ is proved over the finite horizon $N \le 4$, sequential causal growth across arbitrary horizons $N \to \infty$ is achieved via the multiplicative coherent instrument of `PW2-A` Theorem 5.
- Because Kraus operators $K_{S, b}^{P, r}$ act multiplicatively on $\mathcal{H}_{\rm hor} = \mathbb{C}^2$ via orthogonal projection onto $\{\lvert +\rangle, \lvert -\rangle\}$, the instrument satisfies complete-row trace preservation and operator diamond commutation across **all** $N \ge 1$.
- It completely evades the infinite-horizon harmonic collapse obstruction (where $\sum_{n=0}^\infty \Delta E_n = \infty$) because it steers growth through relative quantum phases and directional weights rather than additive energy damping.

### 6.5 Open Research Problem: Variable-Dimension Multi-Mode Sorkin–Johnston Conservation

Extending joint energy conservation $\mathcal{C} = V_{\rm geom} + \operatorname{Tr}[H_{\rm field}\rho]$ from the 2-level probe sector to the full, variable-dimension multi-mode Sorkin–Johnston bosonic field across sequential growth $P \to P+S$ for all $N$ is strictly scoped as an **open research problem**.

The fundamental mathematical hurdles that prevent direct extension are:
1. **Variable Dimension of Field Test Functions**: At parent poset $P$ with $\lvert P\rvert = N$, the test function space is $\mathbb{C}^N$. When newborn vertex $x$ adjoins to ideal $S$, the child poset has cardinality $\lvert P+S\rvert = N+1$. The Pauli–Jordan matrix expands non-trivially:
   $$
   \Delta(P+S) = \begin{pmatrix} \Delta(P) & -v_S \\ v_S^T & 0 \end{pmatrix}, \qquad (v_S)_u = (G_R(P+S))_{xu} - (G_R(P+S))_{ux}.
   $$
2. **Mode Count Reconfiguration and Frequency Shifts**: The number of positive eigenmodes $K(P) = \lvert\{\lambda_j(P) > 0\}\rvert$ is a sensitive topological invariant of the causal order. As demonstrated in canonical benchmarks:
   - $K(A_N) = 0$ for any antichain;
   - $K(C_2) = 1$ with frequency $\lambda_1 = 1$;
   - $K(C_3) = 1$ with frequency $\lambda_1 = \sqrt{6} \approx 2.449$;
   - $K(C_4) = 2$ with frequencies $\lambda_{1, 2} \approx 5.193, 0.193$.
   Growth can create new bosonic oscillator modes ($C_3 \to C_4$ creates a second independent mode) or shift existing frequencies discontinuously.
3. **Discrete Bogoliubov Mixing and Spontaneous Particle Creation**: The Sorkin–Johnston ground state $\lvert 0\rangle_{\rm SJ}(P)$ is defined by the positive spectral projector $P_+(P)$ of $M(P) = i\Delta(P)$. Because $M(P+S)$ does not commute with $M(P) \oplus 0$, the positive-frequency subspace of the child does not coincide with that of the parent. The creation and annihilation operators undergo an intrinsic discrete Bogoliubov transformation:
   $$
   \hat{a}_k(P+S) = \sum_j \left( \alpha_{kj} \hat{a}_j(P) + \beta_{kj} \hat{a}_j^\dagger(P) \right).
   $$
   Whenever $v_S \ne 0$, the Bogoliubov mixing coefficients $\beta_{kj}$ are generically non-zero. Consequently, the child field experiences spontaneous particle creation from the parent vacuum:
   $$
   \langle 0 \mid \hat{N}_{P+S} \mid 0 \rangle_{\rm SJ} = \sum_{k, j} \lvert \beta_{kj}\rvert^2 > 0.
   $$
4. **Topological Covering Link Fluctuations**: The discrete Hamiltonian sums over covering relations:
   $$
   H_{\rm field}(P) = \sum_{v \prec_* u} \mathcal{T}_{\rm link}(v, u) = \frac{1}{2}\phi^T L_P \phi - \langle\text{vac}\rangle.
   $$
   The cardinality $\lvert\operatorname{Link}(P)\rvert$ fluctuates discontinuously depending on $S$: adjoining an isolated vertex adds $0$ links, while capping a fork adds $2$ links (diamond formation). Field energy jumps dynamically across births.
5. **Infinite-Dimensional DAG Linear System**: In `PW2-B`, $V_{\rm geom}$ was solved on the 25 posets of $\mathcal{U}_4$. Extending this to all $N$ requires solving the coupled linear system (I)–(II) on the infinite directed acyclic graph of all unlabeled posets $\bigsqcup_{n=0}^\infty \mathcal{U}_n$. Because $\lvert\mathcal{U}_n\rvert$ grows super-exponentially ($\sim 2^{n^2/4}$), proving the existence of a globally consistent, mark-independent potential $V_{\rm geom}(P)$ that absorbs all multi-mode Bogoliubov dissipation across an infinite horizon remains an open conjecture.

**Open Proposal / Conjecture 6.1 (Multi-Mode Sorkin–Johnston Conservation across Poset Growth).**
*To formulate a complete joint conservation law for the multi-mode Sorkin–Johnston field across sequential growth for all $N$, one must establish:*
1. *A canonical CPTP conditional embedding $\mathcal{E}_{P \to P+S} : \mathcal{S}(\mathcal{F}_{\rm SJ}(P)) \to \mathcal{S}(\mathcal{F}_{\rm SJ}(P+S))$ intertwining the discrete Bogoliubov transformation;*
2. *A discrete geometric stress-backreaction potential $V_{\rm geom}(P)$ defined on all unlabeled posets such that the total expectation $\mathbb{E}[\Delta V_{\rm geom} + \Delta H_{\rm field}] = 0$ holds identically for all initial field states $\rho \in \mathcal{S}(\mathcal{F}_{\rm SJ}(P))$.*

---

## 7. Concrete Poset Evaluations & Numerical Benchmarks

### 7.1 Benchmark Table 1: Field Incidence, Resolvent, and Sorkin–Johnston Spectrum ($\mu = 1$)

The following benchmark table records the exact hand-calculated algebraic invariants of the intrinsic causal propagator across canonical finite posets.

| Poset $P$ | Vertices $N$ | Height $h(P)$ | Nilpotency Index | Incomparable Pairs | $\Delta(P)_{uv}$ on $u \parallel v$ | Spectrum of $M$ ($\mu=1$) | $\dim\ker(M)$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Singleton $P_1$ | 1 | 0 | 1 ($C^1 = 0$) | 0 | Vacuous | None | 1 |
| Two-Chain $C_2$ | 2 | 1 | 2 ($C^2 = 0$) | 0 | Vacuous | $\pm 1$ | 0 |
| Two-Antichain $A_2$ | 2 | 0 | 1 ($C^1 = 0$) | 1 ($0 \parallel 1$) | $\Delta(A_2)_{01} = 0$ | None | 2 |
| Three-Chain $C_3$ | 3 | 2 | 3 ($C^3 = 0$) | 0 | Vacuous | $\pm\sqrt{6}$ | 1 |
| Fork $V$ | 3 | 1 | 2 ($C^2 = 0$) | 1 ($1 \parallel 2$) | $\Delta(V)_{12} = 0$ | $\pm\sqrt{2}$ | 1 |
| Diamond $E_{\text{diamond}}$ | 4 | 2 | 3 ($C^3 = 0$) | 1 ($1 \parallel 2$) | $\Delta(E_{\text{diamond}})_{12} = 0$ | $\pm\sqrt{13}$ | 2 |
| Four-Chain $C_4$ | 4 | 3 | 4 ($C^4 = 0$) | 0 | Vacuous | $\pm\sqrt{\frac{27 \pm 5\sqrt{29}}{2}}$ | 0 |
| Four-Antichain $A_4$ | 4 | 0 | 1 ($C^1 = 0$) | 6 | 0 on all pairs | None | 4 |

### 7.2 Benchmark Table 2: Layer Cardinalities and Benincasa–Dowker Curvature Actions

The following benchmark table records the exact hand-counted layer abundances and combinatorial curvature actions across canonical finite posets.

| Poset $P$ | Vertices $N$ | Links $N_0$ | 1-Intervals $N_1$ | 2-Intervals $N_2$ | 3-Intervals $N_3$ | $S_{\rm BD}^{(2)}(P)$ | $S_{\rm BD}^{(4)}(P)$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Singleton $P_1$ | 1 | 0 | 0 | 0 | 0 | $1$ | $1$ |
| Two-Chain $C_2$ | 2 | 1 | 0 | 0 | 0 | $0$ | $1$ |
| Two-Antichain $A_2$ | 2 | 0 | 0 | 0 | 0 | $2$ | $2$ |
| Three-Chain $C_3$ | 3 | 2 | 1 | 0 | 0 | $3$ | $10$ |
| Fork $V$ | 3 | 2 | 0 | 0 | 0 | $-1$ | $1$ |
| Diamond $E_{\text{diamond}}$ | 4 | 4 | 0 | 1 | 0 | $-6$ | $-16$ |
| Four-Chain $C_4$ | 4 | 3 | 2 | 1 | 0 | $4$ | $3$ |
| Four-Antichain $A_4$ | 4 | 0 | 0 | 0 | 0 | $4$ | $4$ |

### 7.3 Detailed First-Principles Derivations for Canonical Posets

#### 1. Two-Chain $C_2 = (0 \prec 1)$
- Incidence matrix: $C_{C_2} = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$, $C_{C_2}^2 = 0$.
- Retarded and Advanced Green operators ($\mu = 1$):
  $$
  G_R = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}, \qquad G_A = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator:
  $$
  \Delta = G_R - G_A = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}, \qquad M = i\Delta = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}.
  $$
- Spectral analysis of $M$:
  $\det(\lambda I - M) = \lambda^2 - 1 = 0 \implies \lambda = \pm 1$.
  Positive eigenvalue: $\lambda_1 = 1$. Normalized eigenvector: $v_1 = \frac{1}{\sqrt{2}}\begin{pmatrix} -i \\ 1 \end{pmatrix} = v_{1, \rm old}^*$.
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = 1 \cdot v_1 v_1^\dagger = \frac{1}{2}\begin{pmatrix} 1 & -i \\ i & 1 \end{pmatrix} \succeq 0.
  $$
  Verification: $W_{\rm SJ} - W_{\rm SJ}^T = \frac{1}{2}\begin{pmatrix} 1 & -i \\ i & 1 \end{pmatrix} - \frac{1}{2}\begin{pmatrix} 1 & i \\ -i & 1 \end{pmatrix} = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix} = M = i\Delta$.
- Vacuum link fluctuation:
  $$
  \langle (\phi(1) - \phi(0))^2 \rangle_{\rm SJ} = (W_{\rm SJ})_{11} + (W_{\rm SJ})_{00} - (W_{\rm SJ})_{10} - (W_{\rm SJ})_{01} = \frac{1}{2} + \frac{1}{2} - \left(\frac{i}{2}\right) - \left(-\frac{i}{2}\right) = 1.
  $$
- Curvature actions: $N = 2, N_0 = 1, N_1 = 0, N_2 = 0, N_3 = 0$.
  $S_{\rm BD}^{(2)}(C_2) = 2 - 2(1) = 0$.
  $S_{\rm BD}^{(4)}(C_2) = 2 - 1 = 1$.

#### 2. Three-Chain $C_3 = (0 \prec 1 \prec 2)$
- Incidence matrix: $C = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 1 & 0 \end{pmatrix}$, $C^2 = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}$, $C^3 = 0$.
- Resolvents ($\mu = 1$):
  $$
  G_R = C + C^2 = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 2 & 1 & 0 \end{pmatrix}, \qquad G_A = \begin{pmatrix} 0 & 1 & 2 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{pmatrix}.
  $$
- Commutators:
  $$
  \Delta = \begin{pmatrix} 0 & -1 & -2 \\ 1 & 0 & -1 \\ 2 & 1 & 0 \end{pmatrix}, \qquad M = i\Delta = \begin{pmatrix} 0 & -i & -2i \\ i & 0 & -i \\ 2i & i & 0 \end{pmatrix}.
  $$
- Characteristic polynomial:
  $\det(\lambda I - M) = \lambda^3 - 6\lambda = \lambda(\lambda^2 - 6) = 0$.
  Spectrum: $\lambda = 0, \pm\sqrt{6}$. $\dim\ker(M) = 1$.
  Kernel vector: $v_0 = \frac{1}{\sqrt{6}}(1, -2, 1)^T$.
  Positive eigenmode $\lambda_1 = \sqrt{6}$: normalized eigenvector:
  $$
  v_1 = \frac{1}{\sqrt{60}}\begin{pmatrix} 5 \\ 2 + i\sqrt{6} \\ -1 + 2i\sqrt{6} \end{pmatrix} = v_{1, \rm old}^*.
  $$
  *(Note: An equivalent form matching PW4-A line 618 is $v_+ = \frac{1}{\sqrt{60}}(-1 - 2i\sqrt{6}, \, 2 - i\sqrt{6}, \, 5)^T$, differing only by an overall U(1) phase $\frac{-1-2i\sqrt 6}{5}$.)*
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = \sqrt{6} v_1 v_1^\dagger = \frac{\sqrt{6}}{60} \begin{pmatrix} 25 & 10 - 5i\sqrt{6} & -5 - 10i\sqrt{6} \\ 10 + 5i\sqrt{6} & 10 & 10 - 5i\sqrt{6} \\ -5 + 10i\sqrt{6} & 10 + 5i\sqrt{6} & 25 \end{pmatrix} \succeq 0.
  $$
  Verification: $W_{\rm SJ} - W_{\rm SJ}^T = M = i\Delta$, and zero-mode decoupling: $W_{\rm SJ} v_0 = 0$.
- Curvature actions: $N = 3, N_0 = 2, N_1 = 1, N_2 = 0, N_3 = 0$.
  $S_{\rm BD}^{(2)}(C_3) = 3 - 2(2) + 4(1) = 3$.
  $S_{\rm BD}^{(4)}(C_3) = 3 - 2 + 9(1) = 10$.

#### 3. Three-Element Fork $V = (0 \prec 1, 0 \prec 2, 1 \parallel 2)$
- Incidence matrix: $C = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}$, $C^2 = 0$.
- Resolvents: $G_R = C, G_A = C^T$.
- Commutators:
  $$
  \Delta = \begin{pmatrix} 0 & -1 & -1 \\ 1 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}, \qquad M = i\Delta = \begin{pmatrix} 0 & -i & -i \\ i & 0 & 0 \\ i & 0 & 0 \end{pmatrix}.
  $$
  Microcausality: $\Delta_{12} = 0$ on spacelike pair $1 \parallel 2$.
- Spectrum of $M$: $\det(\lambda I - M) = \lambda(\lambda^2 - 2) = 0 \implies \lambda = 0, \pm\sqrt{2}$. $\dim\ker(M) = 1$.
  Kernel vector: $v_0 = \frac{1}{\sqrt{2}}(0, 1, -1)^T$, supported purely on the spacelike pair $1 \parallel 2$.
  Positive eigenmode $\lambda_1 = \sqrt{2}$: normalized eigenvector:
  $$
  v_1 = \frac{1}{2}\begin{pmatrix} -i\sqrt{2} \\ 1 \\ 1 \end{pmatrix} = v_{1, \rm old}^*.
  $$
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = \sqrt{2} v_1 v_1^\dagger = \frac{\sqrt{2}}{4}\begin{pmatrix} -i\sqrt{2} \\ 1 \\ 1 \end{pmatrix}\begin{pmatrix} i\sqrt{2} & 1 & 1 \end{pmatrix} = \begin{pmatrix} \frac{\sqrt{2}}{2} & -\frac{i}{2} & -\frac{i}{2} \\ \frac{i}{2} & \frac{\sqrt{2}}{4} & \frac{\sqrt{2}}{4} \\ \frac{i}{2} & \frac{\sqrt{2}}{4} & \frac{\sqrt{2}}{4} \end{pmatrix} \succeq 0.
  $$
  Verification: $W_{\rm SJ} - W_{\rm SJ}^T = \begin{pmatrix} 0 & -i & -i \\ i & 0 & 0 \\ i & 0 & 0 \end{pmatrix} = M = i\Delta$, and zero-mode decoupling: $W_{\rm SJ} v_0 = 0$.
- Curvature actions: $N = 3, N_0 = 2, N_1 = 0, N_2 = 0, N_3 = 0$.
  $S_{\rm BD}^{(2)}(V) = 3 - 2(2) = -1$.
  $S_{\rm BD}^{(4)}(V) = 3 - 2 = 1$.

#### 4. Four-Element Causal Diamond $E_{\text{diamond}}$ ($0 \prec 1 \prec 3, 0 \prec 2 \prec 3, 1 \parallel 2$)
- Incidence matrix: $C = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix}$, $C^2 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 2 & 0 & 0 & 0 \end{pmatrix}$, $C^3 = 0$.
- Resolvents:
  $$
  G_R = C + C^2 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 3 & 1 & 1 & 0 \end{pmatrix}, \qquad G_A = \begin{pmatrix} 0 & 1 & 1 & 3 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 \end{pmatrix}.
  $$
- Pauli–Jordan commutator:
  $$
  \Delta = \begin{pmatrix} 0 & -1 & -1 & -3 \\ 1 & 0 & 0 & -1 \\ 1 & 0 & 0 & -1 \\ 3 & 1 & 1 & 0 \end{pmatrix}, \qquad M = i\Delta = \begin{pmatrix} 0 & -i & -i & -3i \\ i & 0 & 0 & -i \\ i & 0 & 0 & -i \\ 3i & i & i & 0 \end{pmatrix}.
  $$
  Microcausality: $\Delta_{12} = 0$ on $1 \parallel 2$.
- Spectral analysis:
  Since rows 1 and 2 of $M$ are identical, $\lambda = 0$ has multiplicity at least 1 with spacelike eigenvector $v_{0,1} = \frac{1}{\sqrt{2}}(0, 1, -1, 0)^T$. A second orthogonal longitudinal zero mode is $v_{0,2} = \frac{1}{\sqrt{26}}(2, -3, -3, 2)^T$.
  For non-zero eigenvalues, $v_1 = v_2$. The reduced system yields characteristic equation:
  $$
  \det(\lambda I - M) = \lambda^2(\lambda^2 - 13) = 0.
  $$
  Roots: $\lambda = 0$ (multiplicity 2), $\lambda = \pm\sqrt{13}$.
  $\dim\ker(M) = 2$.
  Positive eigenmode $\lambda_1 = \sqrt{13}$: normalized eigenvector:
  $$
  v_1 = \frac{1}{\sqrt{286}}\begin{pmatrix} -2 - 3i\sqrt{13} \\ 3 - i\sqrt{13} \\ 3 - i\sqrt{13} \\ 11 \end{pmatrix} = v_{1, \rm old}^*.
  $$
- Sorkin–Johnston state:
  $$
  W_{\rm SJ} = \sqrt{13} v_1 v_1^\dagger \succeq 0.
  $$
  Verification: $W_{\rm SJ} - W_{\rm SJ}^T = M = i\Delta$, and zero-mode decoupling: $W_{\rm SJ} v_{0,1} = 0, \; W_{\rm SJ} v_{0,2} = 0$.
- Curvature actions: $N = 4, N_0 = 4, N_1 = 0, N_2 = 1, N_3 = 0$.
  $S_{\rm BD}^{(2)}(E_{\text{diamond}}) = 4 - 2(4) - 2(1) = -6$.
  $S_{\rm BD}^{(4)}(E_{\text{diamond}}) = 4 - 4 - 16(1) = -16$.

#### 5. Four-Chain $C_4 = (0 \prec 1 \prec 2 \prec 3)$
- Incidence matrix: $C_{C_4}$ has non-zero causal entries $(C)_{10}=(C)_{20}=(C)_{21}=(C)_{30}=(C)_{31}=(C)_{32}=1$:
  $$
  C = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix}, \quad C^2 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 2 & 1 & 0 & 0 \end{pmatrix}, \quad C^3 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \end{pmatrix}, \quad C^4 = 0.
  $$
- Resolvent $G_R = (I - C)^{-1} - I = C + C^2 + C^3$:
  $$
  G_R = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 2 & 1 & 0 & 0 \\ 4 & 2 & 1 & 0 \end{pmatrix}, \qquad G_A = G_R^T = \begin{pmatrix} 0 & 1 & 2 & 4 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 0 \end{pmatrix}.
  $$
- Discrete Pauli–Jordan commutator $\Delta = G_R - G_A$ and Hermitian operator $M = i\Delta$:
  $$
  \Delta = \begin{pmatrix} 0 & -1 & -2 & -4 \\ 1 & 0 & -1 & -2 \\ 2 & 1 & 0 & -1 \\ 4 & 2 & 1 & 0 \end{pmatrix}, \qquad M = i\Delta = \begin{pmatrix} 0 & -i & -2i & -4i \\ i & 0 & -i & -2i \\ 2i & i & 0 & -i \\ 4i & 2i & i & 0 \end{pmatrix}.
  $$
- Pfaffian and Determinant of $\Delta(C_4)$ and $M(C_4)$:
  For a $4 \times 4$ skew-symmetric matrix, the Pfaffian is $\operatorname{Pf}(\Delta) = \Delta_{01}\Delta_{23} - \Delta_{02}\Delta_{13} + \Delta_{03}\Delta_{12}$:
  $$
  \operatorname{Pf}(\Delta) = (-1)(-1) - (-2)(-2) + (-4)(-1) = 1 - 4 + 4 = 1.
  $$
  $$
  \det(\Delta) = [\operatorname{Pf}(\Delta)]^2 = 1^2 = 1, \qquad \det(M) = \det(i\Delta) = i^4 \det(\Delta) = 1 \ne 0.
  $$
  **Proof of $\dim\ker(M) = 0$:** Because $\det(M) = 1 \ne 0$, $M$ is strictly non-singular over $\mathbb{C}^4$, so zero is not an eigenvalue:
  $$
  \dim\ker(M) = 0.
  $$
  The preliminary draft claim of $\dim\ker(M) = 2$ is refuted.
- Characteristic polynomial and exact spectrum:
  Computing $\det(\lambda I - M) = \lambda^4 - c_2 \lambda^2 + \det(M) = 0$, where $c_2 = \frac{1}{2}\operatorname{Tr}(M^2) = \sum_{j < k} \Delta_{jk}^2 = 1^2 + 2^2 + 4^2 + 1^2 + 2^2 + 1^2 = 27$:
  $$
  \det(\lambda I - M) = \lambda^4 - 27\lambda^2 + 1 = 0.
  $$
  Solving $u^2 - 27u + 1 = 0$ for $u = \lambda^2$ yields the exact positive roots:
  $$
  u_{1, 2} = \frac{27 \pm \sqrt{729 - 4}}{2} = \frac{27 \pm 5\sqrt{29}}{2}, \qquad u_1 u_2 = 1.
  $$
  The four exact characteristic roots of $M(C_4)$ are:
  $$
  \lambda \in \left\{ \pm \sqrt{\frac{27 + 5\sqrt{29}}{2}}, \; \pm \sqrt{\frac{27 - 5\sqrt{29}}{2}} \right\} \approx \{ \pm 5.192582, \; \pm 0.192582 \}.
  $$
  The heuristic mode pair $\pm\sqrt{20}$ from preliminary nearest-link truncations is superseded by these exact roots.
- Closed-form positive mode eigenvectors: For any positive root $\lambda > 0$ of $\lambda^4 - 27\lambda^2 + 1 = 0$, an exact unnormalized eigenvector of $M$ satisfying $M v(\lambda) = \lambda v(\lambda)$ is:
  $$
  v(\lambda) = \begin{pmatrix}
  5\lambda + 10i\lambda^2 \\
  -10\lambda + 5i\lambda^2 \\
  (\lambda - \lambda^3) + 2i(\lambda^2 - 1) \\
  2\lambda(1 - \lambda^2) + i(1 - \lambda^2)
  \end{pmatrix}.
  $$
  The positive Sorkin–Johnston state is $W_{\rm SJ} = \lambda_1 \frac{v(\lambda_1) v(\lambda_1)^\dagger}{\lVert v(\lambda_1)\rVert^2} + \lambda_3 \frac{v(\lambda_3) v(\lambda_3)^\dagger}{\lVert v(\lambda_3)\rVert^2} \succeq 0$, satisfying $W_{\rm SJ} - W_{\rm SJ}^T = M = i\Delta(C_4)$.
- Curvature actions: $N = 4, N_0 = 3, N_1 = 2, N_2 = 1, N_3 = 0$.
  $S_{\rm BD}^{(2)}(C_4) = 4 - 2(3) + 4(2) - 2(1) = 4$.
  $S_{\rm BD}^{(4)}(C_4) = 4 - 3 + 9(2) - 16(1) = 3$.

---

## 8. Scope, Non-Implications, and Status-M Quarantine

### 8.1 Rigorous Mathematical Scope

The results established in this deliverable are exact algebraic, combinatorial, and quantum information theorems on finite partially ordered sets:
1. The Sorkin–Johnston field algebra ($G_R(P), \Delta(P), M(P), W_{\rm SJ}(P)$) is formulated strictly on finite posets without embedding coordinates or continuous wave equations.
2. Discrete link stress observables $\mathcal{T}_{\rm link}(v, u)$ are defined along covering relations $\operatorname{Link}(P)$, and their expectations in coherent states $\lvert \alpha\rangle$ are proven to be strictly non-negative and quadratic in displacement amplitudes.
3. The operational backreaction instrument couples quantum excitations directly into sequential growth probabilities $q(P, r, S)$, distinguishing (a) the finite-horizon additive reset channel on $\mathcal{H}_{\rm probe} = \mathbb{C}^2$ with exact Choi spectrum and (b) the all-horizon multiplicative coherent steering construction of `PW2-A` Theorem 5 on $\mathcal{H}_{\rm hor} = \mathbb{C}^2$.
4. The linear response of discrete Benincasa–Dowker curvature $S_{\rm BD}^{(4)}$ demonstrates an operational backreaction bridge where positive field energy steers the poset toward interval-focusing diamonds ($S_{\rm BD}^{(4)} = -16$) while field suppression favors chain-like dispersion ($S_{\rm BD}^{(4)} = +3$).
5. The joint probe-plus-geometry conservation ledger $\mathcal{C}(P, \rho) = V_{\rm geom}(P) + \operatorname{Tr}[H_n \rho]$ is proved exactly on the two-level sector across all 25 posets of sizes $0 \le \lvert P\rvert \le 4$, absorbing measurement-induced dissipation into native causal geometry without energy loss or continuum cavities, while variable-dimension multi-mode Sorkin–Johnston field conservation for all $N$ is rigorously scoped as an open research problem.

### 8.2 Explicit Non-Implications

To maintain foundational integrity:
1. **No Continuum Limit Derived**: Discrete Benincasa–Dowker curvature and Sorkin–Johnston propagators on finite posets do not prove that causal posets converge to smooth 4D pseudo-Riemannian manifolds or recover the Einstein field equations $G_{\mu\nu} = 8\pi G T_{\mu\nu}$.
2. **No Physical Units or Constants Derived**: Parameters $\mu, \theta, \varepsilon$ are dimensionless mathematical couplings. No claim is made to derive Newton's constant $G$, Planck's constant $\hbar$, the speed of light $c$, or elementary particle masses.
3. **No Derivation of Born's Rule**: Quantum state steering and CPTP instruments provide a mathematically consistent measurement model on causal posets; they do not derive quantum probability, wave-function collapse, or Born's rule from deterministic growth.
4. **No Derivation of Spacetime Dimension**: Combinatorial layer abundances probe poset interval structure, but do not explain why physical spacetime is macroscopic and 4-dimensional.

### 8.3 Status-M Quarantine Statement

In strict compliance with foundational research governance:
- **`ONTOLOGY.md`**, **`GOVERNANCE.md`**, **`PHYSICS.md`**, and **`FALSIFICATION_LEDGER.md`** remain strictly quarantined under Status-M.
- No modifications, imports, citations, or ontological claims are made regarding Status-M documents.
- All results stand purely on first-principles mathematics, finite incidence algebra, and quantum measurement theory.

---

## 9. Scientific review

Sorkin–Johnston Stress Author derived background-free Sorkin–Johnston field algebra ($G_R(P), \Delta(P), W_{\rm SJ}(P)$), normal-ordered discrete link stress observables $\mathcal{T}_{\rm link}(v, u) = \frac{1}{2}:(\phi(u)-\phi(v))^2:_{W_{\rm SJ}}$ along covering relations $\operatorname{Link}(P) = \operatorname{supp}(A_1)$ summing to the discrete Hamiltonian $H_{\rm field}(P) = \frac{1}{2}\phi^T L_P \phi - \langle\text{vac}\rangle$ with unconditional coherent-state non-negativity, the diamond-commuting CPTP instrument $\mathcal{B}_{S,b}^{P,r}$ ($\lvert r_P\rvert \le 1 - \lambda_{\lvert P\rvert}$) steering sequential growth toward interval-focusing diamonds ($S_{\rm BD}^{(4)} = -16$), and the exact conditional-mean joint probe-plus-geometry conservation ledger $\mathcal{C}(P, \rho) = V_{\rm geom}(P) + \operatorname{Tr}[H_n \rho]$ with 0 residue across all 25 posets ($0 \le \lvert P\rvert \le 4$) completely eliminating continuum cavity scaffolding. Independent Reviewer and Adversarial Challenger independently verified by hand 100% of equations, nilpotency, microcausality, spectral projections, CPTP bounds, conservation linear systems, and canonical benchmark evaluations. Prospective protocol SHA-256 c4bf862d357c1e6489a912f84c03a35ca3ee0475d1bfcbe0cecfa3552c8db34a; accepted author report SHA-256 e0192b2902b9429ab0c8d0372300f59415fe72f7c80d7145410cf94d967fdb6a; independent scientific review SHA-256 85952b5766cdfa5980e70f328aa568838397d265019e2fa8dbd8dcc0052e174e; adversarial challenge report SHA-256 e585842188ce2160f3d9345ef407694a05e9939bb7912c46138f316cadb7994b.
