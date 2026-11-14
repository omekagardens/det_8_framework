# Research Protocol PW6-B: Step-by-Step Sorkin–Johnston Bogoliubov Lift, Exact Skew-Bordering Transition Laws, Finite Diamond Obstructions, and Relativistic Balance

**Document ID**: `PW6B_PROTOCOL.md`  
**Stage**: Stage 5B / PW6-B  
**Date**: 2026-11-14T19:45:00Z  
**Target Repository Location**: `PW6B_PROTOCOL.md`  
**Protocol Status**: Authoritative Mathematical Specification & Deliverable (Stage 5B / PW6-B)  

**Decision.** Resolving the step-by-step operator dynamics of the background-free Sorkin–Johnston bosonic quantum field across causal set sequential growth establishes an exact skew-bordered resolvent expansion $\Delta(P+S) = \begin{pmatrix} \Delta(P) & -v_S \\ v_S^T & 0 \end{pmatrix}$ with $v_S = \mu(I + G_A(P))\mathbf{1}_S$, an exact binary mode transition law $K(P+S) \in \{K(P), K(P)+1\}$ governed by kernel orthogonality $v_S \perp \ker(\Delta(P))$ together with the odd-$N$ 1D-kernel Pfaffian transition identity $\operatorname{Pf}(\Delta(P+S)) = -w^T v_S$, an exact marginal-preserving Gaussian state-extension dichotomy proving that $W(P+S)|_{P \times P} = W_{\rm SJ}(P)$ is achievable if and only if $K(P+S) = K(P)$ (via unique real cross-correlation $\eta_S = -\frac{1}{2}\lvert M(P)\rvert z$ for $\Delta(P)z = v_S$) while $W_\kappa(P) = W_{\rm SJ}(P) + \frac{\kappa}{2}\Pi_{\ker(\Delta(P))}$ satisfies $\operatorname{range}(W_\kappa(P)) = \mathcal{H}_+(P) \oplus \ker(\Delta(P))$ ($\operatorname{rank} = N - K(P)$, $\ker = \mathcal{H}_-(P)$), an exact necessary-and-sufficient coordinate mode-subspace misalignment criterion $\sum_{k,j}\lvert\beta_{kj}\rvert^2 > 0 \iff \Delta(P)v_S \ne 0$, a genuine composable all-horizon causal-marginal-preserving Schur-symplectic state transition law $\mathcal{T}_\kappa : \mathcal{C}_+(P) \to \mathcal{C}_+(P+S)$ (combining mode-preserving congruence $B W B^T$, mode-creating canonical quadratures $[\hat{X}_{\rm new}, \hat{P}_{\rm new}] = i\mathbf{1}$, and the Universal Range Lemma so $[W(P_{n+1})]_{P_n \times P_n} = W(P_n)$ across all horizons without vacuum reset, commuting identically on $281/441$ diamonds while exhibiting real symmetric path-ordering discrepancy on $160/441$ diamonds starting at $P = C_2 \sqcup A_1$), and a finite diamond obstruction on local covering-link energy flux at $N = 5$ on $P = C_2 \sqcup A_1$ ($\lvert\Delta H_{\rm diamond}\rvert = 0.338427$) and $N = 6$ (207 discrepancies) proving the cohomological impossibility of mark-independent scalar potential compensation, whereas including interior fluctuation shifts yields the exact bulk-boundary additive bookkeeping decomposition $\Delta H_{\rm field} = \Phi_{\rm flux} + \Delta H_{\rm int}$ restoring diamond confluence in alignment with guideline `GD-01`; Status-M ontological documents (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined, and no claim is made to derive continuum Einstein field equations, physical Planck units, or non-gravitational gauge forces.

---

## 1. Executive Summary & Epistemic Taxonomy

Stage 5B (PW6-B) resolves the foundational operator dynamics of the intrinsic Sorkin–Johnston (SJ) quantum field across sequential causal set growth $P \to P+S$, directly addressing Open Proposal 6.1 (§6.5) of `docs/observables/intrinsic_sorkin_johnston_stress_and_order_backreaction.md` and the relativistic balance requirement `GD-01` of `docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md`.

In prior stages (`PW2-B`, `PW5-A`), quantum-order backreaction was analyzed under two idealized domains:
1. A finite-horizon ($N \le 4$) two-level probe sector, where quantum measurement damping was absorbed by an artificial scalar potential $V_{\rm geom}(P)$ defined on the 25 unlabeled posets of $\mathcal{U}_4$.
2. Intrinsic Sorkin–Johnston link stress observables on static finite posets, establishing non-negative coherent link stress and discrete curvature backreaction.

Open Proposal 6.1 framed the transition to variable-dimension multi-mode quantum fields across causal set growth as an open problem, requiring:
- The exact operator bordering and spectral transition law for the Pauli–Jordan matrix $\Delta(P) \to \Delta(P+S)$;
- A canonical Gaussian Completely Positive Trace-Preserving (CPTP) state-update map $W(P) \mapsto W(P+S)$ intertwining discrete Bogoliubov mixing;
- A test of whether local energy-flux balance across newly created covering links holds across elementary growth diamonds, or whether an obstruction prevents global scalar compensation.

This protocol provides the definitive mathematical solutions to all core questions, establishing eight rigorously proved theorems, three finite diamond counterexamples/obstructions, and one open asymptotic conjecture.

### Epistemic Taxonomy Table
Every mathematical claim in this deliverable is strictly classified below:

| Identifier | Mathematical Proposition / Assertion | Epistemic Status | Primary Support / Proof Reference |
|:---|:---|:---:|:---|
| **Theorem 1** | Exact Block Bordering of Retarded Resolvent $G_R$ and Pauli–Jordan Commutator $\Delta(P+S)$ | **[PROVED THEOREM]** | Section 2.3, Matrix Neumann series induction |
| **Theorem 2** | Skew-Rank Parity and Binary Mode-Count Transition Dichotomy: $K(P+S) \in \{K(P), K(P)+1\}$ | **[PROVED THEOREM]** | Section 3.1, Frobenius-Schur skew rank theorem |
| **Theorem 3** | Mode Preservation Criterion via Kernel Orthogonality: $K(P+S) = K(P) \iff v_S \perp \ker(\Delta(P))$ | **[PROVED THEOREM]** | Section 3.2, Congruence dilation and kernel extension |
| **Theorem 4** | Exact Pfaffian Kernel Adjugate Formula for Odd Posets: $\operatorname{Pf}(\Delta(P+S)) = -w^T v_S$ | **[PROVED THEOREM]** | Section 3.3, Cayley multilinear Pfaffian expansion |
| **Theorem 5** | Marginal-Preserving Gaussian Extension Dichotomy & Null-Space Activated Range $\mathcal{H}_+ \oplus \ker\Delta$ | **[PROVED THEOREM]** | Section 4.1–4.2, Schur complement & spectral decomposition |
| **Theorem 6** | Exact Criterion for Coordinate Mode-Subspace Misalignment: $\sum \lvert\beta_{kj}\rvert^2 > 0 \iff \Delta(P)v_S \ne 0$ | **[PROVED THEOREM]** | Section 4.3, Positive spectral subspace misalignment |
| **Theorem 6A** | Mode-Preserving Symplectic Congruence $B W(P) B^T$ & Non-Resetting Excitation Propagation | **[PROVED THEOREM]** | Section 4.5, Symplectic congruence across 2,241 births |
| **Theorem 6B** | Mode-Creating Canonical Quadratures $[\hat{X}_{\rm new}, \hat{P}_{\rm new}] = i\mathbf{1}$ & Heisenberg–Schur Equivalence | **[PROVED THEOREM]** | Section 4.5, Robertson–Schrödinger bound across 2,989 births |
| **Theorem 6C** | Universal Range Lemma & Composable All-Horizon Schur-Symplectic Evolution $\mathcal{T}_\kappa : \mathcal{C}_+(P) \to \mathcal{C}_+(P+S)$ | **[PROVED THEOREM]** | Section 4.5, Full-row-rank KKT Schur extension across all horizons |
| **Obstruction 3** | Real Symmetric Two-Step Diamond Ordering Discrepancy Under $\mathcal{T}_\kappa$ ($160/441$ diamonds, starting at $C_2 \sqcup A_1$) | **[COUNTEREXAMPLE/OBSTRUCTION]** | Section 4.5, Exact CCR/marginal preservation vs. zero-mode ordering |
| **Obstruction 1** | Finite Diamond Obstruction on Local Covering-Link Flux at $N=5$ on $C_2 \sqcup A_1$ and $N=6$ | **[COUNTEREXAMPLE/OBSTRUCTION]** | Section 5.3, Exact circulation curl $\lvert\Delta H\rvert = 0.338427$ |
| **Obstruction 2** | Cohomological Impossibility of Mark-Independent Global Scalar Potential Compensation | **[COUNTEREXAMPLE/OBSTRUCTION]** | Section 5.4, Discrete Poincaré lemma on growth DAG |
| **Theorem 7** | Bulk-Boundary Additive Bookkeeping Decomposition & Diamond Confluence | **[PROVED THEOREM]** | Section 6.2, Link-partition telescoping identity |
| **Conjecture 1** | Asymptotic Convergence of Relativistic Field Stress in the Poisson Continuum Limit | **[OPEN CONJECTURE]** | Section 6.4, Unproved continuum limit scaling |

---

## 2. Background-Free Causal Propagator Algebra & Exact Skew Bordering Across Births

### 2.1 Poset Incidence, Resolvents, and Discrete Microcausality
Let $P = (V, \prec)$ be a finite strict partially ordered set of cardinality $\lvert V\rvert = N \ge 1$. Throughout this protocol, the elements of $V$ are topologically indexed $\{0, 1, \dots, N-1\}$ such that $v \prec u \implies v < u$.

**Definition 2.1 (Causal Incidence Matrix).**  
The causal incidence matrix $C_P \in \{0, 1\}^{N \times N}$ is defined by:
$$
(C_P)_{uv} := \begin{cases} 1 & \text{if } v \prec u, \\ 0 & \text{otherwise.} \end{cases}
$$
Because the labeling is topological, $C_P$ is strictly lower triangular with zeros on the diagonal. Transitivity implies that $(C_P^k)_{uv}$ counts the exact number of directed chains of length $k$ strictly bounded by $v$ and $u$. Since $P$ is finite, $C_P$ is strictly nilpotent with nilpotency index $h(P) + 1 \le N$:
$$
C_P^N = 0, \qquad \det(I - \mu C_P) = 1 \quad (\forall \mu \in \mathbb{C}).
$$

**Definition 2.2 (Retarded and Advanced Green Resolvents).**  
For propagation parameter $\mu > 0$ (canonically set to $\mu = 1$), the background-free retarded Green resolvent $G_R(P) \in \mathbb{R}^{N \times N}$ and advanced Green resolvent $G_A(P) \in \mathbb{R}^{N \times N}$ are:
$$
G_R(P) := (I - \mu C_P)^{-1} - I = \sum_{k=1}^{N-1} \mu^k C_P^k, \qquad G_A(P) := G_R(P)^T = (I - \mu C_P^T)^{-1} - I = \sum_{k=1}^{N-1} \mu^k (C_P^T)^k.
$$
$G_R(P)$ is strictly lower triangular, and $G_A(P)$ is strictly upper triangular.

**Definition 2.3 (Pauli–Jordan Commutator & Hermitian Generator).**  
The discrete Pauli–Jordan commutator operator $\Delta(P) \in \mathbb{R}^{N \times N}$ and Hermitian generator $M(P) \in \mathbb{C}^{N \times N}$ are:
$$
\Delta(P) := G_R(P) - G_A(P) = G_R(P) - G_R(P)^T, \qquad M(P) := i \Delta(P).
$$
$\Delta(P)$ is real skew-symmetric ($\Delta(P)^T = -\Delta(P)$), and $M(P)$ is Hermitian ($M(P)^\dagger = M(P)$) with purely imaginary entries.

**Proposition 2.1 (Exact Discrete Microcausality).**  
*For every pair of events $u, v \in V$:*
1. *If $v \prec u$, then $\Delta(P)_{uv} = (G_R(P))_{uv} > 0$ and $\Delta(P)_{vu} = -(G_R(P))_{uv} < 0$;*
2. *If $u \parallel v$ (spacelike incomparable), then $(G_R(P))_{uv} = (G_R(P))_{vu} = 0$, so $\Delta(P)_{uv} = 0$ identically;*
3. *If $u = v$, then $\Delta(P)_{uu} = 0$.*

*Proof.* Follows immediately from Definition 2.2 and Definition 2.3 because $(C_P^k)_{uv} > 0$ if and only if there exists a chain from $v$ to $u$. Incomparable elements admit no chains between them. $\blacksquare$

### 2.2 Sorkin–Johnston Two-Point State & Mode Counting
Because $M(P)$ is Hermitian and skew-symmetric, its non-zero eigenvalues occur in symmetric pairs $\pm \lambda_j$ ($\lambda_j > 0$) with orthonormal complex eigenvectors $v_j, v_j^*$:
$$
M(P) v_j = \lambda_j v_j, \qquad M(P) v_j^* = -\lambda_j v_j^*.
$$
The number of positive eigenvalues is the mode count $K(P) \in \mathbb{N}_0$, satisfying:
$$
\operatorname{rank}(\Delta(P)) = \operatorname{rank}(M(P)) = 2K(P), \qquad \dim\ker(\Delta(P)) = N - 2K(P).
$$

**Definition 2.4 (Sorkin–Johnston Vacuum Covariance).**  
The positive-spectral projection defines the Sorkin–Johnston two-point covariance matrix:
$$
W_{\rm SJ}(P) := \frac{1}{2}\left( \lvert M(P)\rvert + M(P) \right) = \sum_{j=1}^{K(P)} \lambda_j v_j v_j^\dagger \in \mathbb{C}^{N \times N}.
$$
The Sorkin–Johnston covariance satisfies:
1. $W_{\rm SJ}(P) \succeq 0$ (positive semidefinite);
2. $W_{\rm SJ}(P) - W_{\rm SJ}(P)^T = M(P) = i \Delta(P)$;
3. $W_{\rm SJ}(P) v_0 = 0$ for all $v_0 \in \ker(\Delta(P))$.

### 2.3 Exact Block Bordering Across Causal Set Births
Let $S \in \mathcal{I}(P)$ be a downward-closed precursor ideal of $P$, meaning that $u \in S$ and $v \prec u$ implies $v \in S$. The adjoining of a newborn event $x$ with causal past $\{u \in P : u \prec x\} = S$ produces the child poset $P' = P+S$ of cardinality $\lvert P+S\rvert = N+1$. Under topological sorting, $x$ is maximal and is assigned index $N$.

**Theorem 1 (Exact Block Bordering of Retarded Resolvent and Pauli–Jordan Operator) [PROVED THEOREM].**  
*Let $P$ be a poset of cardinality $N$ and $S \in \mathcal{I}(P)$ a downward-closed ideal with indicator vector $\mathbf{1}_S \in \{0, 1\}^N$ where $(\mathbf{1}_S)_u = 1 \iff u \in S$. Then:*
1. *The child incidence matrix is strictly lower triangular:*
   $$
   C_{P+S} = \begin{pmatrix} C_P & 0 \\ \mathbf{1}_S^T & 0 \end{pmatrix}.
   $$
2. *The child retarded Green resolvent expands as an exact lower block triangular matrix:*
   $$
   G_R(P+S) = \begin{pmatrix} G_R(P) & 0 \\ v_S^T & 0 \end{pmatrix},
   $$
   *where the bordering vector $v_S \in \mathbb{R}^N$ is given explicitly by:*
   $$
   v_S = \mu (I - \mu C_P^T)^{-1} \mathbf{1}_S = \mu (I + G_A(P)) \mathbf{1}_S.
   $$
3. *The child Pauli–Jordan operator borders as:*
   $$
   \Delta(P+S) = \begin{pmatrix} \Delta(P) & -v_S \\ v_S^T & 0 \end{pmatrix} \in \mathbb{R}^{(N+1)\times(N+1)},
   $$
   *and the Hermitian generator borders as:*
   $$
   M(P+S) = \begin{pmatrix} M(P) & -i v_S \\ i v_S^T & 0 \end{pmatrix} \in \mathbb{C}^{(N+1)\times(N+1)}.
   $$

*Proof.*  
For the incidence powers, we proceed by induction on $k \ge 1$. For $k=1$, $C_{P+S} = \begin{pmatrix} C_P & 0 \\ \mathbf{1}_S^T & 0 \end{pmatrix}$. Assume for $k \ge 1$ that $C_{P+S}^k = \begin{pmatrix} C_P^k & 0 \\ \mathbf{1}_S^T C_P^{k-1} & 0 \end{pmatrix}$. Then:
$$
C_{P+S}^{k+1} = C_{P+S}^k C_{P+S} = \begin{pmatrix} C_P^k & 0 \\ \mathbf{1}_S^T C_P^{k-1} & 0 \end{pmatrix} \begin{pmatrix} C_P & 0 \\ \mathbf{1}_S^T & 0 \end{pmatrix} = \begin{pmatrix} C_P^{k+1} & 0 \\ \mathbf{1}_S^T C_P^k & 0 \end{pmatrix}.
$$
By mathematical induction, this holds for all $k \ge 1$. Evaluating the resolvent Neumann series:
$$
G_R(P+S) = \sum_{k=1}^N \mu^k C_{P+S}^k = \begin{pmatrix} \sum_{k=1}^{N-1} \mu^k C_P^k & 0 \\ \mu \mathbf{1}_S^T \sum_{k=0}^{N-1} \mu^k C_P^k & 0 \end{pmatrix} = \begin{pmatrix} G_R(P) & 0 \\ \mu \mathbf{1}_S^T (I - \mu C_P)^{-1} & 0 \end{pmatrix}.
$$
Taking the transpose of the bottom-left block yields the column vector $v_S$:
$$
v_S = \left( \mu \mathbf{1}_S^T (I - \mu C_P)^{-1} \right)^T = \mu \left( (I - \mu C_P)^{-1} \right)^T \mathbf{1}_S = \mu (I - \mu C_P^T)^{-1} \mathbf{1}_S = \mu (I + G_A(P)) \mathbf{1}_S.
$$
The advanced Green operator is $G_A(P+S) = G_R(P+S)^T = \begin{pmatrix} G_A(P) & v_S \\ 0 & 0 \end{pmatrix}$. Subtracting yields:
$$
\Delta(P+S) = G_R(P+S) - G_A(P+S) = \begin{pmatrix} G_R(P) - G_A(P) & -v_S \\ v_S^T & 0 \end{pmatrix} = \begin{pmatrix} \Delta(P) & -v_S \\ v_S^T & 0 \end{pmatrix}.
$$
Multiplying by $i$ gives $M(P+S)$. $\blacksquare$

---

## 3. Exact Spectral and Pfaffian Transition Laws

### 3.1 Skew-Rank Parity and Binary Mode-Count Transition
Because $\Delta(P+S)$ is a bordered real skew-symmetric matrix, its algebraic and spectral invariants are constrained by skew-symmetric matrix theory.

**Theorem 2 (Skew-Rank Parity and Binary Mode Transition) [PROVED THEOREM].**  
*Let $P$ be a poset of cardinality $N$ with mode count $K(P) = \frac{1}{2}\operatorname{rank}(\Delta(P))$, and let $S \in \mathcal{I}(P)$ be any precursor ideal. Then:*
1. *The rank of $\Delta(P+S)$ must be an even integer: $\operatorname{rank}(\Delta(P+S)) \in 2\mathbb{N}_0$;*
2. *The rank can shift by at most 2: $\operatorname{rank}(\Delta(P+S)) - \operatorname{rank}(\Delta(P)) \in \{0, 2\}$;*
3. *The mode count undergoes a strict binary transition:*
   $$
   K(P+S) \in \{K(P), \, K(P) + 1\}.
   $$

*Proof.*  
Let $A \in \mathbb{R}^{m \times m}$ be any real skew-symmetric matrix ($A^T = -A$). Its non-zero eigenvalues are purely imaginary and appear in complex conjugate pairs $\pm i \lambda_k$ ($\lambda_k > 0$). Therefore, the algebraic multiplicity of non-zero eigenvalues is even, which implies $\operatorname{rank}(A) = 2K \in 2\mathbb{N}_0$.  
Now let $\tilde{A} = \Delta(P+S)$ be obtained from $A = \Delta(P)$ by adding one row and one column. By the standard rank inequality for bordered matrices, $\operatorname{rank}(\tilde{A}) \le \operatorname{rank}(A) + 2$. Since $A$ is a submatrix of $\tilde{A}$, $\operatorname{rank}(\tilde{A}) \ge \operatorname{rank}(A)$.  
Because both $\operatorname{rank}(\tilde{A})$ and $\operatorname{rank}(A)$ are even integers, the difference $\operatorname{rank}(\tilde{A}) - \operatorname{rank}(A)$ must be an even non-negative integer bounded above by 2. Hence:
$$
\operatorname{rank}(\tilde{A}) - \operatorname{rank}(A) \in \{0, 2\}.
$$
Dividing by 2 yields $K(P+S) - K(P) \in \{0, 1\}$. $\blacksquare$

### 3.2 Kernel Orthogonality and Mode Preservation Criterion
We now determine the exact algebraic criterion that distinguishes mode preservation from mode creation.

**Theorem 3 (Mode Transition Law via Kernel Orthogonality) [PROVED THEOREM].**  
*Let $P$ be a finite poset and $S \in \mathcal{I}(P)$ a precursor ideal with bordering vector $v_S = \mu(I + G_A(P))\mathbf{1}_S$.*
1. **Mode-Preserving Transition ($K(P+S) = K(P)$):**  
   $$
   K(P+S) = K(P) \iff v_S \in \operatorname{range}(\Delta(P)) \iff v_S \perp \ker(\Delta(P)).
   $$
   *In this case:*
   - $\operatorname{rank}(\Delta(P+S)) = \operatorname{rank}(\Delta(P))$;
   - $\dim\ker(\Delta(P+S)) = \dim\ker(\Delta(P)) + 1$;
   - *There exists a vector $z \in \mathbb{R}^N$ satisfying $\Delta(P) z = v_S$. The block unitriangular matrix $T = \begin{pmatrix} I_N & 0 \\ z^T & 1 \end{pmatrix}$ effects the exact congruence:*
     $$
     T \Delta(P+S) T^T = \begin{pmatrix} \Delta(P) & 0 \\ 0 & 0 \end{pmatrix} = \Delta(P) \oplus (0);
     $$
   - *The new null vector of $\Delta(P+S)$ is explicitly given by:*
     $$
     w_{\rm new} = \begin{pmatrix} z \\ 1 \end{pmatrix} \in \ker(\Delta(P+S)).
     $$
2. **Mode-Creating Transition ($K(P+S) = K(P) + 1$):**  
   $$
   K(P+S) = K(P) + 1 \iff v_S \notin \operatorname{range}(\Delta(P)) \iff \exists w \in \ker(\Delta(P)) \text{ s.t. } w^T v_S \ne 0.
   $$
   *In this case:*
   - $\operatorname{rank}(\Delta(P+S)) = \operatorname{rank}(\Delta(P)) + 2$;
   - $\dim\ker(\Delta(P+S)) = \dim\ker(\Delta(P)) - 1$;
   - *The birth adjoins a new conjugate pair of non-zero eigenvalues $\pm \lambda_{\rm new}$ ($\lambda_{\rm new} > 0$).*

*Proof.*  
Because $\Delta(P)$ is skew-symmetric, $\Delta(P)^T = -\Delta(P)$. By the fundamental theorem of linear algebra, the orthogonal complement of the image of $\Delta(P)$ is $\ker(\Delta(P)^T) = \ker(-\Delta(P)) = \ker(\Delta(P))$. Therefore, $\operatorname{range}(\Delta(P)) = (\ker(\Delta(P)))^\perp$, which establishes that $v_S \in \operatorname{range}(\Delta(P)) \iff v_S \perp \ker(\Delta(P))$.

Suppose $v_S \in \operatorname{range}(\Delta(P))$. Then there exists $z \in \mathbb{R}^N$ such that $\Delta(P) z = v_S$. Consider the invertible block unitriangular matrix $T = \begin{pmatrix} I_N & 0 \\ z^T & 1 \end{pmatrix}$. Applying the skew-congruence transformation:
$$
T \Delta(P+S) T^T = \begin{pmatrix} I_N & 0 \\ z^T & 1 \end{pmatrix} \begin{pmatrix} \Delta(P) & -v_S \\ v_S^T & 0 \end{pmatrix} \begin{pmatrix} I_N & z \\ 0 & 1 \end{pmatrix}.
$$
Performing the block matrix multiplication:
$$
\begin{pmatrix} I_N & 0 \\ z^T & 1 \end{pmatrix} \begin{pmatrix} \Delta(P) & -v_S \\ v_S^T & 0 \end{pmatrix} = \begin{pmatrix} \Delta(P) & -v_S \\ z^T \Delta(P) + v_S^T & -z^T v_S \end{pmatrix}.
$$
Multiplying on the right by $T^T = \begin{pmatrix} I_N & z \\ 0 & 1 \end{pmatrix}$:
$$
T \Delta(P+S) T^T = \begin{pmatrix} \Delta(P) & \Delta(P)z - v_S \\ z^T \Delta(P) + v_S^T & z^T \Delta(P) z + v_S^T z - z^T v_S \end{pmatrix}.
$$
Evaluating each block:
1. Top-right block: $\Delta(P)z - v_S = v_S - v_S = 0$.
2. Bottom-left block: Using skew-symmetry $\Delta(P)^T = -\Delta(P)$, we have $z^T \Delta(P) = (\Delta(P)^T z)^T = -(\Delta(P)z)^T = -v_S^T$. Thus $z^T \Delta(P) + v_S^T = -v_S^T + v_S^T = 0$.
3. Bottom-right block: Since $\Delta(P)$ is skew-symmetric, $z^T \Delta(P) z = 0$. Furthermore, $v_S^T z = z^T v_S$ is a real scalar, so $0 + v_S^T z - z^T v_S = 0$.

Therefore, the congruence strictly isolates the newborn degree of freedom as a decoupled zero mode:
$$
T \Delta(P+S) T^T = \begin{pmatrix} \Delta(P) & 0 \\ 0 & 0 \end{pmatrix} = \Delta(P) \oplus (0).
$$
Because congruence preserves rank, $\operatorname{rank}(\Delta(P+S)) = \operatorname{rank}(\Delta(P))$, establishing $K(P+S) = K(P)$. The nullity increases by:
$$
\dim\ker(\Delta(P+S)) = (N+1) - 2K(P) = \dim\ker(\Delta(P)) + 1.
$$
The new null vector is obtained directly by mapping $e_{N+1}$ under $T^T$:
$$
w_{\rm new} = T^T e_{N+1} = \begin{pmatrix} I_N & z \\ 0 & 1 \end{pmatrix} \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} z \\ 1 \end{pmatrix}.
$$
Indeed, direct multiplication verifies:
$$
\Delta(P+S) \begin{pmatrix} z \\ 1 \end{pmatrix} = \begin{pmatrix} \Delta(P) & -v_S \\ v_S^T & 0 \end{pmatrix} \begin{pmatrix} z \\ 1 \end{pmatrix} = \begin{pmatrix} \Delta(P)z - v_S \\ v_S^T z \end{pmatrix} = \begin{pmatrix} v_S - v_S \\ z^T \Delta(P)^T z \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix},
$$
since $v_S^T z = (\Delta(P)z)^T z = z^T \Delta(P)^T z = -z^T \Delta(P) z = 0$. Thus $w_{\rm new} \in \ker(\Delta(P+S))$ identically.

Conversely, suppose $v_S \notin \operatorname{range}(\Delta(P))$. Then $v_S$ cannot be eliminated by any congruence transformation, so the column space of $\Delta(P+S)$ contains $\operatorname{range}(\Delta(P))$ and an independent direction. By Theorem 2, the rank must increase by an even integer $\le 2$, forcing $\operatorname{rank}(\Delta(P+S)) = \operatorname{rank}(\Delta(P)) + 2$, which gives $K(P+S) = K(P) + 1$. $\blacksquare$

### 3.3 Pfaffian Kernel Formula for Odd Dimension
When $N$ is odd, $\dim\ker(\Delta(P)) \ge 1$ by skew-rank parity. The child poset has cardinality $N+1$, which is even. Therefore, $\Delta(P+S)$ is an even-dimensional skew-symmetric matrix possessing a polynomial Pfaffian $\operatorname{Pf}(\Delta(P+S))$ such that:
$$
\det(\Delta(P+S)) = \left( \operatorname{Pf}(\Delta(P+S)) \right)^2.
$$

**Theorem 4 (Exact Pfaffian Adjugate Transition Formula) [PROVED THEOREM].**  
*Let $N$ be odd, and suppose $\dim\ker(\Delta(P)) = 1$. Let $w \in \mathbb{R}^N$ span $\ker(\Delta(P))$, normalized componentwise by the principal sub-Pfaffians:*
$$
w_j := (-1)^j \operatorname{Pf}(\Delta(P)_{\hat{j}}) \quad (j = 0, 1, \dots, N-1),
$$
*where $\Delta(P)_{\hat{j}}$ is the $(N-1)\times(N-1)$ principal skew-symmetric submatrix obtained by deleting row and column $j$ of $\Delta(P)$ (with $\operatorname{Pf}(\varnothing) := 1$ at $N = 1$). Then:*
1. *The Pfaffian of the bordered child matrix evaluates to:*
   $$
   \operatorname{Pf}(\Delta(P+S)) = -w^T v_S = -\sum_{j=0}^{N-1} (-1)^j (v_S)_j \operatorname{Pf}(\Delta(P)_{\hat{j}});
   $$
2. *The child matrix $\Delta(P+S)$ is strictly non-singular ($\dim\ker(\Delta(P+S)) = 0$, $K(P+S) = \frac{N+1}{2}$) if and only if:*
   $$
   w^T v_S \ne 0.
   $$

*Proof.*  
By Cayley's Pfaffian expansion along the last column $N$ of the $(N+1)\times(N+1)$ skew-symmetric matrix $\Delta(P+S)$ (ordered with $j < N$):
$$
\operatorname{Pf}(\Delta(P+S)) = \sum_{j=0}^{N-1} (-1)^{N-1-j} \Delta(P+S)_{j, N} \operatorname{Pf}(\Delta(P+S)_{\widehat{j, N}}).
$$
From Theorem 1, the $(j, N)$-entry in the last column is $\Delta(P+S)_{j, N} = -(v_S)_j$, while deleting rows and columns $j$ and $N$ yields the $(N-1)\times(N-1)$ principal submatrix $\Delta(P)_{\hat{j}}$ of the parent poset $P$:
$$
\operatorname{Pf}(\Delta(P+S)) = -\sum_{j=0}^{N-1} (-1)^{N-1-j} (v_S)_j \operatorname{Pf}(\Delta(P)_{\hat{j}}).
$$
Since $N$ is odd, $N-1$ is an even integer, so $(-1)^{N-1-j} = (-1)^{-j} = (-1)^j$. Substituting the definition $w_j = (-1)^j \operatorname{Pf}(\Delta(P)_{\hat{j}})$ yields:
$$
\operatorname{Pf}(\Delta(P+S)) = -\sum_{j=0}^{N-1} (v_S)_j w_j = -w^T v_S.
$$
By standard multilinear algebra for skew-symmetric matrices, the vector $w$ defined by the signed $(N-1)$-principal sub-Pfaffians spans the 1-dimensional null space $\ker(\Delta(P))$ when $\operatorname{rank}(\Delta(P)) = N-1$.  
Consequently, $\det(\Delta(P+S)) = (\operatorname{Pf}(\Delta(P+S)))^2 = (-w^T v_S)^2 = (w^T v_S)^2$. Therefore, $\Delta(P+S)$ is non-singular ($\det \ne 0$) if and only if $w^T v_S \ne 0$. By Theorem 3, $w^T v_S \ne 0 \iff v_S \notin \operatorname{range}(\Delta(P)) \iff K(P+S) = K(P) + 1 = \frac{N-1}{2} + 1 = \frac{N+1}{2}$. $\blacksquare$

### 3.4 Benchmark Transitions Table across Canonical Posets
The analytical invariants and transition laws derived in Theorems 1–4 are summarized in Table 1 across canonical posets:

| Transition $P \to P+S$ | $N \to N+1$ | $\Delta(P)$ Rank & $K(P)$ | Ideal $S$ & Vector $v_S$ | Kernel Generator $w$ | Inner Product $w^T v_S$ | Child Mode $K(P+S)$ | $\operatorname{Pf}(\Delta(P+S))$ | Transition Class |
|:---|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| $P_1 \to C_2$ | $1 \to 2$ | Rank 0, $K=0$ | $S=\{0\}$, $v_S = (1)$ | $w = (1)$ | $+1$ | $K=1$ | $-1$ | Mode Created |
| $C_2 \to C_3$ | $2 \to 3$ | Rank 2, $K=1$ | $S=\{0, 1\}$, $v_S = (2, 1)^T$ | $\ker = \{0\}$ | Vacuous | $K=1$ | Undefined (odd) | Mode Preserved |
| $C_3 \to C_4$ | $3 \to 4$ | Rank 2, $K=1$ | $S=\{0, 1, 2\}$, $v_S = (4, 2, 1)^T$ | $w = (-1, 2, -1)^T$ | $-4 + 4 - 1 = -1$ | $K=2$ | $+1$ | Mode Created |
| $C_3 \to \text{Upper Fork } Q$ | $3 \to 4$ | Rank 2, $K=1$ | $S=\{0\}$, $v_S = (1, 0, 0)^T$ | $w = (-1, 2, -1)^T$ | $-1 + 0 + 0 = -1$ | $K=2$ | $+1$ | Mode Created |
| Fork $V \to E_{\text{diamond}}$ | $3 \to 4$ | Rank 2, $K=1$ | $S=\{0, 1, 2\}$, $v_S = (3, 1, 1)^T$ | $w = (0, 1, -1)^T$ | $0 + 1 - 1 = 0$ | $K=1$ | $0$ | Mode Preserved |
| $A_3 \to C_2 \sqcup A_2$ | $3 \to 4$ | Rank 0, $K=0$ | $S=\{0\}$, $v_S = (1, 0, 0)^T$ | $\ker = \mathbb{R}^3$ ($\dim=3$) | $e_0^T v_S = 1 \ne 0$ | $K=1$ | $0$ ($\dim\ker=2$) | Mode Created |

*Remark on $V \to E_{\text{diamond}}$*: Table 1 highlights the critical transition Fork $V \to E_{\text{diamond}}$. In this birth, the newborn event caps both arms of the fork. Although $v_S = (3, 1, 1)^T \ne 0$, its inner product with the kernel generator $w = (0, 1, -1)^T$ is exactly $0(3) + 1(1) - 1(1) = 0$. Thus $v_S \in \operatorname{range}(\Delta(V))$, and the mode count remains strictly frozen at $K(E_{\text{diamond}}) = K(V) = 1$. The null space dimension increments from 1 to 2, and the diamond Pauli–Jordan matrix remains singular ($\operatorname{Pf} = 0$).

---

## 4. Canonical Gaussian CPTP State-Update Map & Discrete Bogoliubov Lift

### 4.1 Gaussian Covariance Extension and Choi Positive Semidefiniteness
Let $\mathcal{F}_{\rm SJ}(P)$ denote the bosonic Fock space over the one-particle Hilbert space associated with the positive-frequency subspace of $\Delta(P)$. A centered Gaussian quantum state is completely characterized by its two-point covariance matrix:
$$
W(P) = \gamma(P) + \frac{i}{2} \Delta(P) \in \mathbb{C}^{N \times N},
$$
where $\gamma(P) \in \mathbb{R}^{N \times N}$ is symmetric, $\Delta(P) \in \mathbb{R}^{N \times N}$ is skew-symmetric, and $W(P) \succeq 0$ expresses the generalized Robertson–Schrödinger uncertainty relation.

Across a causal birth $P \to P+S$, the child state on $\mathbb{C}^{(N+1)\times(N+1)}$ has the block form:
$$
W(P+S) = \begin{pmatrix} W(P) & c_S \\ c_S^\dagger & \sigma_x^2 \end{pmatrix},
$$
where $c_S \in \mathbb{C}^N$ is the cross-correlation vector between the parent field and the newborn site $x$, and $\sigma_x^2 = \langle \phi(x)^2 \rangle \in \mathbb{R}$ is the newborn local variance.

**Theorem 5 (Marginal-Preserving Gaussian Extension Dichotomy & Mode-Isometric Fock CPTP Lift) [PROVED THEOREM].**  
*Let $W(P) = \gamma(P) + \frac{i}{2}\Delta(P) \succeq 0$ be any parent Gaussian covariance matrix on $P$, and consider a bordered covariance matrix $W(P+S) = \begin{pmatrix} W(P) & c_S \\ c_S^\dagger & \sigma_x^2 \end{pmatrix}$ with $c_S = \eta_S - \frac{i}{2}v_S$ ($\eta_S \in \mathbb{R}^N$, $v_S = \mu(I + G_A(P))\mathbf{1}_S$).*
1. *(General Schur-Complement Characterization.)* *$W(P+S)$ defines a valid quantum Gaussian state extending $W(P)$ ($W(P+S) \succeq 0$ and $W(P+S) - W(P+S)^T = i\Delta(P+S)$) if and only if $c_S \in \operatorname{range}(W(P))$ and $\sigma_x^2 \ge c_S^\dagger W(P)^+ c_S$, where $W(P)^+$ denotes the Moore–Penrose pseudoinverse.*
2. *(Exact Sorkin–Johnston Marginal-Preserving Dichotomy.)* *Specialize to the pure Sorkin–Johnston vacuum covariance $W_{\rm SJ}(P) = \frac{1}{2}\lvert M(P)\rvert + \frac{i}{2}\Delta(P)$. A marginal-preserving Gaussian extension $W(P+S)|_{P \times P} = W_{\rm SJ}(P)$ exists **if and only if** the birth is mode-preserving ($K(P+S) = K(P) \iff v_S \in \operatorname{range}(\Delta(P))$):*
   - *When $K(P+S) = K(P)$, let $z \in \mathbb{R}^N$ solve $\Delta(P) z = v_S$ (e.g., $z = \Delta(P)^+ v_S$). Because $\mathcal{H}_+(P) \cap \mathbb{R}^N = \{0\}$, there is a **unique** vector $c_S \in \operatorname{range}(W_{\rm SJ}(P)) = \mathcal{H}_+(P)$ with $\operatorname{Im}(c_S) = -\frac{1}{2}v_S$, given by the non-zero real cross-correlation $\eta_S = -\frac{1}{2}\lvert M(P)\rvert z \in \mathbb{R}^N$ ($c_S = -W_{\rm SJ}(P)z$), with minimal newborn variance $\sigma_{x,\min}^2 = z^T W_{\rm SJ}(P) z = \frac{1}{2} z^T \lvert M(P)\rvert z \ge 0$ and explicit congruence factorization:*
     $$
     W_{\rm ext}(P+S) := \begin{pmatrix} I_N \\ -z^T \end{pmatrix} W_{\rm SJ}(P) \begin{pmatrix} I_N & -z \end{pmatrix} = \begin{pmatrix} W_{\rm SJ}(P) & -W_{\rm SJ}(P)z \\ -z^T W_{\rm SJ}(P) & \frac{1}{2} z^T \lvert M(P)\rvert z \end{pmatrix} \succeq 0.
     $$
   - *When $K(P+S) = K(P) + 1$, there exists $w \in \ker(\Delta(P)) \subset \mathbb{R}^N$ with $w^T v_S \ne 0$. Because $W_{\rm SJ}(P)w = 0$ while $\operatorname{Im}(w^T c_S) = -\frac{1}{2}w^T v_S \ne 0$ for **every** $\eta_S \in \mathbb{R}^N$, no choice of $(\eta_S, \sigma_x^2)$ can satisfy $W(P+S) \succeq 0$ without modifying the parent marginal (a zero-variance parent zero mode $w^T\hat{\phi}$ violates the Robertson–Schrödinger uncertainty bound once $[\hat{\phi}(x), w^T\hat{\phi}] = i w^T v_S \ne 0$).*
3. *(Universal Mode-Isometric Fock-Space Gaussian CPTP Lift & Null-Space Activated Schur Extension.)* *Across **all** births ($K(P+S) \in \{K(P), K(P)+1\}$), $K(P) \le K(P+S)$ holds identically (Theorem 2). Consequently, every isometric one-particle embedding $V : \mathcal{H}_+(P) \hookrightarrow \mathcal{H}_+(P+S)$ ($V^\dagger V = I_{K(P)}$) induces an exact second-quantized Gaussian CPTP channel $\mathcal{E}_V : \mathcal{S}(\mathcal{F}_{\rm SJ}(P)) \to \mathcal{S}(\mathcal{F}_{\rm SJ}(P+S))$, $\mathcal{E}_V(\rho) = \Gamma(V)\rho\Gamma(V)^\dagger$, mapping the parent SJ vacuum $\lvert 0_P\rangle\langle 0_P\rvert$ directly to the child SJ vacuum $\lvert 0_{P+S}\rangle\langle 0_{P+S}\rvert$ ($W_{\rm SJ}(P) \mapsto W_{\rm SJ}(P+S)$). Equivalently, in coordinate space, activating the parent null space via $W_\kappa(P) := W_{\rm SJ}(P) + \frac{\kappa}{2}\Pi_{\ker(\Delta(P))}$ ($\kappa > 0$) strictly preserves the CCR commutator ($W_\kappa(P) - W_\kappa(P)^T = i\Delta(P)$) while satisfying $\operatorname{range}(W_\kappa(P)) = \mathcal{H}_+(P) \oplus \ker(\Delta(P))$, $\ker W_\kappa(P) = \mathcal{H}_-(P)$, and $\operatorname{rank}(W_\kappa(P)) = N - K(P)$. For every birth (mode-preserving or mode-creating), decomposing $v_S = \Delta(P)z_\parallel + v_0$ with $z_\parallel = \Delta(P)^+ v_S$ and $v_0 = \Pi_{\ker(\Delta(P))} v_S$ yields $c_S = -W_{\rm SJ}(P)z_\parallel - \frac{i}{2}v_0 \in \mathcal{H}_+(P) \oplus \ker(\Delta(P)) = \operatorname{range}(W_\kappa(P))$, admitting a valid quantum Schur extension $W_{\kappa,\operatorname{ext}}(P+S) \succeq 0$ across every birth with minimal newborn variance $\sigma_{x,\min}^2(\kappa) = \frac{1}{2}z_\parallel^T \lvert M(P)\rvert z_\parallel + \frac{1}{2\kappa}\lVert v_0 \rVert_2^2$.*

*Proof.*  
1. By the commutation identity of quantum covariances (Definition 2.4), $W(P+S) - W(P+S)^T = i \Delta(P+S)$. From Theorem 1, the top-right block of $\Delta(P+S)$ is $-v_S$, so $c_S - c_S^* = 2i \operatorname{Im}(c_S) = -i v_S \iff \operatorname{Im}(c_S) = -\frac{1}{2}v_S$. By the Albert–Schur complement theorem for Hermitian block matrices:
$$
\begin{pmatrix} W(P) & c_S \\ c_S^\dagger & \sigma_x^2 \end{pmatrix} \succeq 0 \iff W(P) \succeq 0, \quad (I - W(P)W(P)^+)c_S = 0, \quad \sigma_x^2 - c_S^\dagger W(P)^+ c_S \ge 0,
$$
establishing Part 1.
2. Suppose $W(P+S) \succeq 0$ extends $W_{\rm SJ}(P)$. Then $c_S \in \operatorname{range}(W_{\rm SJ}(P))$. For every real null vector $w \in \ker(\Delta(P)) \subset \mathbb{R}^N$, $W_{\rm SJ}(P)w = 0$ and Hermiticity of $W_{\rm SJ}(P)$ give $w^T c_S = w^\dagger c_S = 0$. Taking the imaginary part yields $0 = \operatorname{Im}(w^T c_S) = -\frac{1}{2} w^T v_S$, so $v_S \perp \ker(\Delta(P))$ and hence $K(P+S) = K(P)$ by Theorem 3.  
Conversely, if $K(P+S) = K(P)$, choose $z \in \mathbb{R}^N$ such that $\Delta(P)z = v_S$. Because $-\Delta(P)^2$ is real symmetric positive semidefinite, its principal square root $\lvert M(P)\rvert = \sqrt{-\Delta(P)^2}$ is real symmetric, so $\eta_S := -\frac{1}{2}\lvert M(P)\rvert z \in \mathbb{R}^N$ is real and $c_S = \eta_S - \frac{i}{2}v_S = -\frac{1}{2}\lvert M(P)\rvert z - \frac{i}{2}\Delta(P)z = -W_{\rm SJ}(P)z \in \operatorname{range}(W_{\rm SJ}(P))$. Uniqueness of $\eta_S$ follows because if $c_S, c_S' \in \mathcal{H}_+(P)$ satisfy $\operatorname{Im}(c_S) = \operatorname{Im}(c_S')$, then $c_S - c_S' \in \mathcal{H}_+(P) \cap \mathbb{R}^N$; since $\mathcal{H}_+(P)^* = \mathcal{H}_-(P)$ and $\mathcal{H}_+(P) \cap \mathcal{H}_-(P) = \{0\}$, $\mathcal{H}_+(P) \cap \mathbb{R}^N = \{0\}$, whence $c_S = c_S'$ (note in particular that naive $\eta_S = 0$ fails whenever $v_S \ne 0$, since $-\frac{i}{2}v_S$ is purely imaginary and cannot lie in $\mathcal{H}_+(P)$). Since $B W_{\rm SJ}(P) B^\dagger \succeq 0$ for $B = \begin{pmatrix} I_N \\ -z^T \end{pmatrix}$ and $z^T \Delta(P)z = 0$, $W_{\rm ext}(P+S) \succeq 0$ satisfies both positivity and $W_{\rm ext}(P+S) - W_{\rm ext}(P+S)^T = i\Delta(P+S)$, annihilating the new zero mode $w_{\rm new} = \begin{pmatrix} z \\ 1 \end{pmatrix}$ of Theorem 3.
3. Since $K(P) \le K(P+S)$, $\dim\mathcal{H}_+(P) \le \dim\mathcal{H}_+(P+S)$ holds across all births. On symmetric Fock spaces $\mathcal{F}_{\rm SJ}(P) = \bigoplus_{m=0}^\infty \mathcal{H}_+(P)^{\odot m}$, second quantization $\Gamma(V)$ of any Hilbert-space isometry $V : \mathcal{H}_+(P) \hookrightarrow \mathcal{H}_+(P+S)$ satisfies $\Gamma(V)^\dagger \Gamma(V) = I_{\mathcal{F}_{\rm SJ}(P)}$ and $\Gamma(V)\lvert 0_P\rangle = \lvert 0_{P+S}\rangle$ (acting as a single-Kraus isometric CPTP channel that tensors in the vacuum $\lvert 0_{\rm new}\rangle$ on $\mathcal{H}_+(P+S) \ominus V\mathcal{H}_+(P)$ when $K(P+S) = K(P)+1$).  
Next, consider the null-space activated covariance in coordinate space:
$$
W_\kappa(P) := W_{\rm SJ}(P) + \frac{\kappa}{2}\Pi_{\ker(\Delta(P))}, \qquad \kappa > 0.
$$
Since $\Delta(P)$ is real skew-symmetric, $\ker(\Delta(P)) \subset \mathbb{R}^N$ is real, so its orthogonal projection matrix $\Pi_{\ker(\Delta(P))}$ is real symmetric ($\Pi_{\ker(\Delta(P))}^T = \Pi_{\ker(\Delta(P))}$). Thus:
$$
W_\kappa(P) - W_\kappa(P)^T = \left(W_{\rm SJ}(P) - W_{\rm SJ}(P)^T\right) + \frac{\kappa}{2}\left(\Pi_{\ker(\Delta(P))} - \Pi_{\ker(\Delta(P))}^T\right) = i\Delta(P),
$$
preserving the canonical commutation relations exactly.  
From the spectral decomposition of $M(P) = i\Delta(P)$, carrier space $\mathbb{C}^N$ decomposes orthogonally into eigenspaces:
$$
\mathbb{C}^N = \mathcal{H}_+(P) \oplus \mathcal{H}_-(P) \oplus \ker(\Delta(P)),
$$
where $W_{\rm SJ}(P) = \sum_{j=1}^{K(P)} \lambda_j v_j v_j^\dagger$. On $\mathcal{H}_+(P)$, $W_\kappa(P)v_j = \lambda_j v_j$ ($\lambda_j > 0$); on $\ker(\Delta(P))$, $W_\kappa(P)u = \frac{\kappa}{2}u$ ($\frac{\kappa}{2} > 0$); on $\mathcal{H}_-(P)$, $W_{\rm SJ}(P)v_j^* = 0$ and $\Pi_{\ker(\Delta(P))}v_j^* = 0$, so $W_\kappa(P)v_j^* = 0$. Consequently:
$$
\operatorname{range}(W_\kappa(P)) = \mathcal{H}_+(P) \oplus \ker(\Delta(P)), \qquad \ker(W_\kappa(P)) = \mathcal{H}_-(P),
$$
$$
\operatorname{rank}(W_\kappa(P)) = \dim \mathcal{H}_+(P) + \dim \ker(\Delta(P)) = K(P) + (N - 2K(P)) = N - K(P).
$$
Whenever $K(P) > 0$, $\operatorname{rank}(W_\kappa(P)) = N - K(P) < N$, so $\operatorname{range}(W_\kappa(P))$ is a strict subspace of $\mathbb{C}^N$, with kernel exactly equal to the negative-frequency subspace $\mathcal{H}_-(P)$.  
To establish the universal Schur extension across every birth, decompose the bordering vector $v_S \in \mathbb{R}^N$ orthogonally as $v_S = v_\parallel + v_0$, where $v_0 = \Pi_{\ker(\Delta(P))} v_S \in \ker(\Delta(P))$ and $v_\parallel = (I - \Pi_{\ker(\Delta(P))}) v_S \in \operatorname{range}(\Delta(P))$. Setting $z_\parallel = \Delta(P)^+ v_S$, we have $\Delta(P)z_\parallel = v_\parallel$. Choosing $\eta_S = -\frac{1}{2}\lvert M(P)\rvert z_\parallel \in \mathbb{R}^N$, the cross-coupling vector is:
$$
c_S = \eta_S - \frac{i}{2}v_S = -\frac{1}{2}\lvert M(P)\rvert z_\parallel - \frac{i}{2}\Delta(P)z_\parallel - \frac{i}{2}v_0 = -W_{\rm SJ}(P)z_\parallel - \frac{i}{2}v_0.
$$
Since $-W_{\rm SJ}(P)z_\parallel \in \mathcal{H}_+(P)$ and $-\frac{i}{2}v_0 \in \ker(\Delta(P))$, we have $c_S \in \mathcal{H}_+(P) \oplus \ker(\Delta(P)) = \operatorname{range}(W_\kappa(P))$ identically for all births. In particular, for every negative-frequency eigenvector $v_j^* \in \mathcal{H}_-(P)$:
$$
(v_j^*)^\dagger c_S = -(v_j^*)^\dagger W_{\rm SJ}(P)z_\parallel - \frac{i}{2}(v_j^*)^\dagger v_0 = 0 - 0 = 0.
$$
The Moore–Penrose pseudoinverse is $W_\kappa(P)^+ = \sum_{j=1}^{K(P)} \frac{1}{\lambda_j} v_j v_j^\dagger + \frac{2}{\kappa}\Pi_{\ker(\Delta(P))}$. Since $\mathcal{H}_+(P)$ and $\ker(\Delta(P))$ are mutually orthogonal, the quadratic form decouples:
$$
c_S^\dagger W_\kappa(P)^+ c_S = z_\parallel^T W_{\rm SJ}(P)^\dagger W_{\rm SJ}(P)^+ W_{\rm SJ}(P) z_\parallel + \left(-\frac{i}{2}v_0\right)^\dagger \left(\frac{2}{\kappa}\Pi_{\ker(\Delta(P))}\right) \left(-\frac{i}{2}v_0\right) = \frac{1}{2}z_\parallel^T \lvert M(P)\rvert z_\parallel + \frac{1}{2\kappa}\lVert v_0\rVert_2^2.
$$
By Albert's theorem, setting $\sigma_x^2 \ge \sigma_{x,\min}^2(\kappa) = \frac{1}{2}z_\parallel^T \lvert M(P)\rvert z_\parallel + \frac{1}{2\kappa}\lVert v_0\rVert_2^2$ guarantees $W_{\kappa,\operatorname{ext}}(P+S) \succeq 0$ and $W_{\kappa,\operatorname{ext}}(P+S) - W_{\kappa,\operatorname{ext}}(P+S)^T = i\Delta(P+S)$ across every birth. $\blacksquare$

### 4.2 Physical Interpretation of the Extension Dichotomy: Mode Misalignment vs. Vacuum Reset
Theorem 5(2)–(3) uncovers a profound distinction between **vacuum-resetting Fock embeddings** and **physical quantum state propagation**:
1. **The Vacuum Reset $\Gamma(V)$**: The second-quantized map $\Gamma(V) : \mathcal{S}(\mathcal{F}_{\rm SJ}(P)) \to \mathcal{S}(\mathcal{F}_{\rm SJ}(P+S))$ constructed in Theorem 5(3) satisfies $\Gamma(V)\lvert 0_P\rangle = \lvert 0_{P+S}\rangle$. It maps the parent vacuum directly to the child vacuum. Crucially, a map that maps vacuum to vacuum operates by discarding prior excitations: it resets the quantum state to the new ground state. While mathematically valid as an isometric Fock embedding, it does not constitute dynamical physical state propagation for general excited states $\rho$.
2. **The Coordinate Marginal Dichotomy**: When parent modes are tracked in coordinate space, Theorem 5(2) proves that on all **2,989 / 5,230** mode-creating births ($57.2\%$ of extensions up to $N = 6$), exact marginal preservation $W(P+S)|_{P \times P} = W_{\rm SJ}(P)$ is strictly forbidden by the Robertson–Schrödinger uncertainty relation: newly adjoined sites couple to parent zero modes $w \in \ker(\Delta(P))$, requiring non-zero variance $\sigma_x^2$ and symplectic activation. Updating to the intrinsic child Sorkin–Johnston vacuum $W_{\rm SJ}(P+S)$ induces bulk interior polarization backreaction ($\Delta H_{\rm int} \ne 0$ in Section 6) across pre-existing links.

### 4.3 Exact Criterion for Discrete Bogoliubov Mixing and Mode-Subspace Misalignment
Let $\{v_j\}_{j=1}^{K(P)}$ be the positive-frequency orthonormal eigenvectors of $M(P)$, spanning the one-particle subspace $\mathcal{H}_+(P) \subset \mathbb{C}^N$. The parent annihilation operators are $\hat{a}_j(P) = \frac{1}{\sqrt{\lambda_j}} v_j^\dagger \hat{\phi}$.  
Upon adjoining $x$ to precursor ideal $S$, the child Hermitian operator $M(P+S)$ possesses positive-frequency eigenvectors $\{v_k'\}_{k=1}^{K(P+S)}$ spanning $\mathcal{H}_+(P+S) \subset \mathbb{C}^{N+1}$. Embedding parent modes into coordinate space $\mathbb{C}^{N+1}$ via $\tilde{v}_j := \begin{pmatrix} v_j \\ 0 \end{pmatrix}$, the child annihilation operators couple to the parent dynamical sector via the discrete Bogoliubov coefficients:
$$
\alpha_{kj} = \sqrt{\frac{\lambda_j}{\lambda_k'}} (v_k')^\dagger \begin{pmatrix} v_j \\ 0 \end{pmatrix}, \qquad \beta_{kj} = \sqrt{\frac{\lambda_j}{\lambda_k'}} (v_k')^\dagger \begin{pmatrix} v_j^* \\ 0 \end{pmatrix}.
$$
These coefficients quantify the geometric mode-subspace misalignment between the coordinate-embedded parent positive-frequency modes $\tilde{v}_j$ and the child spectral subspaces $\mathcal{H}_\pm(P+S) \subset \mathbb{C}^{N+1}$.

**Theorem 6 (Exact Necessary and Sufficient Criterion for Discrete Bogoliubov Mixing and Mode-Subspace Misalignment) [PROVED THEOREM].**  
*Let $P$ be any finite poset and $S \in \mathcal{I}(P)$ any downward-closed precursor ideal with bordering vector $v_S = \mu(I + G_A(P))\mathbf{1}_S \in \mathbb{R}^N$. Then:*
1. *Whenever $S \ne \varnothing$, $v_S \in \mathbb{R}^N \setminus \{0\}$ has strictly non-negative entries and cannot belong to $\mathcal{H}_+(P)$.*
2. *Geometric mode-subspace misalignment between the child positive-frequency modes and the coordinate-embedded parent negative-frequency modes ($\beta_{kj} \ne 0$) occurs **if and only if** $v_S$ has a non-zero projection onto the parent dynamical subspace $(\ker\Delta(P))^\perp$:*
   $$
   \sum_{k=1}^{K(P+S)} \sum_{j=1}^{K(P)} \lvert \beta_{kj}\rvert^2 > 0 \iff \Delta(P) v_S \ne 0 \quad \bigl(\text{i.e., } v_S \notin \ker(\Delta(P))\bigr).
   $$
3. *Whenever $\Delta(P)v_S \ne 0$, evaluating the child mode occupation in the coordinate-embedded parent vacuum state yields strictly positive spontaneous particle creation $\langle \hat{N}_k \rangle = \sum_{j=1}^{K(P)} \lvert \beta_{kj}\rvert^2 > 0$; conversely, when $\Delta(P)v_S = 0$ (which occurs for $S = \varnothing$, when $K(P) = 0$ as in $P_1 \to C_2$ or $A_n \to C_2 \sqcup A_{n-1}$, or when $S$ lies entirely inside an isolated edgeless component of $P$), every embedded parent mode $\tilde{v}_j$ remains an exact unmixed eigenvector of $M(P+S)$ with $\beta_{kj} = 0$.*

*Proof.*  
1. Since $I + G_A(P) = (I - \mu C_P^T)^{-1}$ is unipotent upper triangular with non-negative entries and unit diagonal, $S \ne \varnothing \implies \mathbf{1}_S \ne 0 \implies v_S \ne 0$. Because $M(P)^* = -M(P)$, $\mathcal{H}_+(P)^* = \mathcal{H}_-(P)$ and $\mathcal{H}_+(P) \cap \mathcal{H}_-(P) = \{0\}$, so $\mathcal{H}_+(P) \cap \mathbb{R}^N = \{0\}$ and no non-zero real vector $v_S$ lies in $\mathcal{H}_+(P)$.
2. **($\Delta(P)v_S = 0 \implies \beta \equiv 0$):** Suppose $\Delta(P)v_S = 0$, so $v_S \in \ker(\Delta(P)) = (\mathcal{H}_+(P) \oplus \mathcal{H}_-(P))^\perp$. Then for every parent eigenvector $\psi \in \mathcal{H}_\pm(P)$ ($M(P)\psi = \pm\lambda\psi$, $\lambda > 0$), we have $v_S^T \psi = v_S^\dagger \psi = 0$, and hence
$$
M(P+S)\begin{pmatrix} \psi \\ 0 \end{pmatrix} = \begin{pmatrix} M(P)\psi \\ i v_S^T \psi \end{pmatrix} = \pm\lambda \begin{pmatrix} \psi \\ 0 \end{pmatrix}.
$$
Thus every embedded parent mode $\tilde{v}_j$ (eigenvalue $+\lambda_j > 0$) and $\tilde{v}_j^*$ (eigenvalue $-\lambda_j < 0$) is an exact eigenvector of the Hermitian matrix $M(P+S)$. Because eigenvectors of $M(P+S)$ with positive eigenvalues $\lambda_k' > 0$ are strictly orthogonal to eigenvectors with negative eigenvalues $-\lambda_j < 0$, $(v_k')^\dagger \tilde{v}_j^* = 0$ and $\beta_{kj} = 0$ for all $k, j$.  
**($\beta \equiv 0 \implies \Delta(P)v_S = 0$):** Conversely, suppose $\beta_{kj} = 0$ for all $k \in \{1, \dots, K(P+S)\}$ and $j \in \{1, \dots, K(P)\}$. Then $(v_k')^\dagger \tilde{v}_j^* = 0$, and taking complex conjugates gives $((v_k')^*)^\dagger \tilde{v}_j = 0$ for all $k, j$, meaning $\tilde{v}_j \perp \mathcal{H}_-(P+S)$. From the orthogonal decomposition $\mathbb{C}^{N+1} = \mathcal{H}_+(P+S) \oplus \mathcal{H}_-(P+S) \oplus \ker M(P+S)$, it follows that $\tilde{v}_j \in \mathcal{H}_+(P+S) \oplus \ker M(P+S)$ for every $j = 1, \dots, K(P)$. On $\mathcal{H}_+(P+S) \oplus \ker M(P+S)$, the operator modulus $\lvert M(P+S)\rvert = \sqrt{-\Delta(P+S)^2}$ coincides identically with $M(P+S)$, so:
$$
\lvert M(P+S)\rvert \tilde{v}_j = M(P+S)\tilde{v}_j = \begin{pmatrix} \lambda_j v_j \\ i v_S^T v_j \end{pmatrix}.
$$
Because $\lvert M(P+S)\rvert$ and $v_S$ are both **real**, taking the complex conjugate yields:
$$
\lvert M(P+S)\rvert \tilde{v}_j^* = \begin{pmatrix} \lambda_j v_j^* \\ -i v_S^T v_j^* \end{pmatrix}.
$$
Using Hermiticity of $\lvert M(P+S)\rvert$ and the identity $\lvert M(P+S)\rvert^2 = M(P+S)^2 = \begin{pmatrix} M(P)^2 + v_S v_S^T & -i M(P)v_S \\ i v_S^T M(P) & v_S^T v_S \end{pmatrix}$, together with $(v_j^*)^\dagger v_j = 0$, we compute the inner product $(\lvert M(P+S)\rvert \tilde{v}_j^*)^\dagger (\lvert M(P+S)\rvert \tilde{v}_j) = (\tilde{v}_j^*)^\dagger M(P+S)^2 \tilde{v}_j$ in two ways:
$$
\bigl(\lvert M(P+S)\rvert \tilde{v}_j^*\bigr)^\dagger \bigl(\lvert M(P+S)\rvert \tilde{v}_j\bigr) = \lambda_j^2 (v_j^*)^\dagger v_j + (i v_S^T v_j)(i v_S^T v_j) = -(v_S^T v_j)^2,
$$
$$
(\tilde{v}_j^*)^\dagger M(P+S)^2 \tilde{v}_j = (v_j^*)^\dagger M(P)^2 v_j + (v_j^*)^\dagger v_S v_S^T v_j = \lambda_j^2 (v_j^*)^\dagger v_j + (v_S^T v_j)^2 = +(v_S^T v_j)^2.
$$
Equating the two expressions gives $-(v_S^T v_j)^2 = +(v_S^T v_j)^2 \implies v_S^T v_j = 0$ (and hence $v_S^T v_j^* = (v_S^T v_j)^* = 0$) for every $j = 1, \dots, K(P)$. Therefore $v_S \perp (\mathcal{H}_+(P) \oplus \mathcal{H}_-(P))$, which means $v_S \in \ker(\Delta(P))$, i.e., $\Delta(P)v_S = 0$.
3. Using $\hat{a}_j(P)\lvert 0_P\rangle = 0$ and $[\hat{a}_j(P), \hat{a}_{j'}^\dagger(P)] = \delta_{jj'}$ on the parent dynamical modes yields $\sum_{j, j'} \beta_{kj}^* \beta_{kj'} \langle 0_P \mid \hat{a}_j(P)\hat{a}_{j'}^\dagger(P)\mid 0_P\rangle = \sum_j \lvert\beta_{kj}\rvert^2$, and summing over $k = 1, \dots, K(P+S)$ completes the proof. $\blacksquare$

### 4.4 Why Coordinate Mode Overlaps Alone Are Not a Unitary Particle-Creation Law
A crucial algebraic distinction separates the rectangular coordinate-overlap matrices $\alpha, \beta \in \mathbb{C}^{K(P+S) \times K(P)}$ of Section 4.3 from a closed canonical Bogoliubov transformation. Using the orthogonal resolution of the identity on $\mathbb{C}^{N+1}$:
$$
I_{N+1} = \sum_{j=1}^{K(P)} \left( \tilde{v}_j \tilde{v}_j^\dagger + \tilde{v}_j^* (\tilde{v}_j^*)^\dagger \right) + \left( \Pi_{\ker(\Delta(P))} \oplus 0 \right) + e_{N+1} e_{N+1}^T,
$$
and the eigenvalue equation $M(P+S)v_k' = \lambda_k' v_k'$, one finds that $(\alpha\alpha^\dagger - \beta\beta^\dagger)_{kk'}$ does **not** in general equal $\delta_{kk'}$: the remaining commutator weight of the child annihilation operators $[\hat{a}_k(P+S), \hat{a}_{k'}^\dagger(P+S)] = \delta_{kk'}$ resides precisely in the parent zero-mode subspace $\ker(\Delta(P))$ and the newborn field coordinate $\hat{\phi}(x)$! Consequently, one must distinguish three operations across $P \to P+S$:
1. **The Vacuum Reset Channel $\Gamma(V)$ (Theorem 5(3))**: Second quantization of an isometry $V : \mathcal{H}_+(P) \hookrightarrow \mathcal{H}_+(P+S)$ maps $\lvert 0_P\rangle \mapsto \lvert 0_{P+S}\rangle$ ($W(P) \mapsto W_{\rm SJ}(P+S)$), resetting the field to the child Sorkin–Johnston ground state and erasing prior excitations $\Delta W(P)$.
2. **Coordinate Mode-Subspace Misalignment $(\alpha_{kj}, \beta_{kj})$ (Theorem 6)**: Measures the geometric tilt between coordinate-embedded parent dynamical modes $\tilde{v}_j$ and child modes $v_k'$, without supplying the canonical zero-mode/newborn completion.
3. **Composable CCR-Preserving Gaussian State Propagation (Section 4.5)**: Explicitly incorporates parent zero modes and the newborn field operator $\hat{\phi}(x)$ so that $W(P) \mapsto W(P+S)$ preserves $W \succeq 0$, exact CCR $W - W^T = i\Delta$, and causal past marginals $[W(P+S)]_{P\times P} = W(P)$ across all horizons without vacuum reset.

### 4.5 Canonical CCR-Preserving Gaussian State Transitions Across All Horizons

We now construct the explicit linear and symplectic state-evolution laws resolving both mode-preserving ($K(P+S) = K(P)$) and mode-creating ($K(P+S) = K(P)+1$) births across arbitrary multi-step causal set trajectories.

**Theorem 6A (Mode-Preserving Symplectic Congruence & Excitation Propagation) [PROVED THEOREM].**  
*Let $W(P) = \gamma(P) + \frac{i}{2}\Delta(P) \succeq 0$ be any parent Gaussian covariance matrix on $P$. Across any mode-preserving birth ($K(P+S) = K(P) \iff v_S \in \operatorname{range}(\Delta(P))$), set $z := \Delta(P)^+ v_S \in \operatorname{range}(\Delta(P))$ and $B := \begin{pmatrix} I_N \\ -z^T \end{pmatrix} \in \mathbb{R}^{(N+1)\times N}$. Then $W_{\rm cong}(P+S) := B W(P) B^T \in \mathbb{C}^{(N+1)\times(N+1)}$ satisfies:*
1. *Unconditional Positivity & Exact CCR: $W_{\rm cong}(P+S) \succeq 0$ and $W_{\rm cong}(P+S) - W_{\rm cong}(P+S)^T = i\Delta(P+S)$.*
2. *Exact Past-Marginal Preservation & Zero-Mode Annihilation: $[W_{\rm cong}(P+S)]_{P \times P} = W(P)$ and $W_{\rm cong}(P+S) w_{\rm new} = 0$ for $w_{\rm new} = \begin{pmatrix} z \\ 1 \end{pmatrix} \in \ker(\Delta(P+S))$.*
3. *Non-Resetting Excitation Propagation: For any excited parent state $W(P) = W_{\rm base}(P) + \Delta W(P)$ with real symmetric $\Delta W(P) \succeq 0$, the propagated excitation $\Delta W(P+S) := B \Delta W(P) B^T \succeq 0$ is real symmetric and satisfies $\operatorname{Tr}(\Delta W(P+S)) = \operatorname{Tr}(\Delta W(P)) + z^T \Delta W(P) z \ge \operatorname{Tr}(\Delta W(P))$.*

*Proof.*  
Since $B$ is real, $B^\dagger = B^T$, so $\xi^\dagger (B W(P) B^T)\xi = (B^T \xi)^\dagger W(P) (B^T \xi) \ge 0$ for all $\xi \in \mathbb{C}^{N+1}$. Using $\Delta(P)z = v_S$ and skew-symmetry $z^T \Delta(P)z = 0$:
$$
W_{\rm cong}(P+S) - W_{\rm cong}(P+S)^T = i B\Delta(P)B^T = i\begin{pmatrix} \Delta(P) & -\Delta(P)z \\ z^T \Delta(P) & z^T \Delta(P) z \end{pmatrix} = i\begin{pmatrix} \Delta(P) & -v_S \\ v_S^T & 0 \end{pmatrix} = i\Delta(P+S).
$$
The top-left $N\times N$ block is $W(P)$, $B^T w_{\rm new} = z - z = 0 \implies W_{\rm cong}(P+S)w_{\rm new} = 0$, and $\operatorname{Tr}(B\Delta W(P)B^T) = \operatorname{Tr}(\Delta W(P)(I_N + zz^T)) = \operatorname{Tr}(\Delta W(P)) + z^T\Delta W(P)z \ge \operatorname{Tr}(\Delta W(P))$. $\blacksquare$

**Theorem 6B (Mode-Creating Canonical Quadratures & Heisenberg–Schur Identity) [PROVED THEOREM].**  
*Across any mode-creating birth ($K(P+S) = K(P) + 1 \iff v_0 := \Pi_{\ker(\Delta(P))} v_S \ne 0$), let $z_\parallel := \Delta(P)^+ v_S \in \operatorname{range}(\Delta(P))$ so that $v_S = \Delta(P)z_\parallel + v_0$. Let $\hat{\Phi}_P = (\hat{\phi}(0), \dots, \hat{\phi}(N-1))^T$ and $\hat{\phi}(x)$ satisfy $[\hat{\Phi}_P, \hat{\Phi}_P^T] = i\Delta(P)$ and $[\hat{\Phi}_P, \hat{\phi}(x)] = -i v_S$. Define the Hermitian linear field quadratures:*
$$
\hat{X}_{\rm new} := \frac{v_0^T \hat{\Phi}_P}{\lVert v_0\rVert_2}, \qquad \hat{P}_{\rm new} := -\frac{\hat{\phi}(x) + z_\parallel^T \hat{\Phi}_P}{\lVert v_0\rVert_2}.
$$
*Then:*
1. *Exact Canonical Conjugate Pair: $[\hat{X}_{\rm new}, \hat{P}_{\rm new}] = i\mathbf{1}$.*
2. *Symplectic Decoupling: $[\hat{X}_{\rm new}, u^T \hat{\Phi}_P] = [\hat{P}_{\rm new}, u^T \hat{\Phi}_P] = 0$ for all $u \in \operatorname{range}(\Delta(P))$, and $[\hat{X}_{\rm new}, w^T \hat{\Phi}_P] = [\hat{P}_{\rm new}, w^T \hat{\Phi}_P] = 0$ for all $w \in \ker(\Delta(P)) \cap v_0^\perp$ (with $\ker(\Delta(P+S)) = (\ker(\Delta(P)) \cap v_0^\perp) \oplus \{0\}$).*
3. *Complete Schur-Family Parametrization & Heisenberg Bound: Under $W_\kappa(P) = W_{\rm SJ}(P) + \frac{\kappa}{2}\Pi_{\ker(\Delta(P))}$ ($\kappa > 0$), a vector $c_S = \eta_S - \frac{i}{2}v_S$ ($\eta_S \in \mathbb{R}^N$) lies in $\operatorname{range}(W_\kappa(P)) = \mathcal{H}_+(P) \oplus \ker(\Delta(P))$ **if and only if** $\eta_S = -\frac{1}{2}\lvert M(P)\rvert z_\parallel + \eta_0$ for some $\eta_0 \in \ker(\Delta(P))$, in which case:*
   $$
   c_S^\dagger W_\kappa(P)^+ c_S = \frac{1}{2}z_\parallel^T \lvert M(P)\rvert z_\parallel + \frac{1}{2\kappa}\lVert v_0\rVert_2^2 + \frac{2}{\kappa}\lVert \eta_0\rVert_2^2 \ge \sigma_{x,\min}^2(\kappa),
   $$
   *attaining its unique minimum at $\eta_0 = 0$ and matching the Heisenberg minimum-uncertainty bound $\langle \hat{X}_{\rm new}^2\rangle \langle \hat{P}_{\rm new}^2\rangle \ge \frac{1}{4}$ at $\langle \hat{X}_{\rm new}^2\rangle = \frac{\kappa}{2}$ (and extending additively to $W(P) = W_\kappa(P) + \Delta W(P)$ via $W_{\kappa,\operatorname{ext}}(P+S) + B_\parallel \Delta W(P) B_\parallel^T \succeq 0$ with $B_\parallel = \begin{pmatrix} I_N \\ -z_\parallel^T \end{pmatrix}$).*

*Proof.*  
1. Since $v_0 \in \ker(\Delta(P))$ and $v_0 \perp \Delta(P)z_\parallel$, $[v_0^T \hat{\Phi}_P, \hat{\phi}(x)] = -i v_0^T v_S = -i\lVert v_0\rVert_2^2$ and $[v_0^T \hat{\Phi}_P, z_\parallel^T \hat{\Phi}_P] = i v_0^T \Delta(P)z_\parallel = 0$, giving $[\hat{X}_{\rm new}, \hat{P}_{\rm new}] = -\lVert v_0\rVert_2^{-2}(-i\lVert v_0\rVert_2^2) = i\mathbf{1}$.
2. For $u \in \operatorname{range}(\Delta(P))$, $v_0^T \Delta(P)u = 0$ and $v_S^T u + z_\parallel^T \Delta(P)u = (v_S - \Delta(P)z_\parallel)^T u = v_0^T u = 0$, so both commutators vanish. For $w \in \ker(\Delta(P)) \cap v_0^\perp$, $\Delta(P)w = 0$ and $v_S^T w = v_0^T w = 0$, so both commutators again vanish. Moreover, $\Delta(P+S)\begin{pmatrix} u \\ \alpha \end{pmatrix} = 0 \iff \Delta(P)u = \alpha v_S \text{ and } v_S^T u = 0$; since $v_S \notin \operatorname{range}(\Delta(P))$, $\alpha = 0$ and $u \in \ker(\Delta(P)) \cap v_0^\perp$.
3. By Theorem 5(3), $\ker(W_\kappa(P)) = \mathcal{H}_-(P)$. Writing $\eta_S = \eta_\parallel + \eta_0$ with $\eta_\parallel \in \operatorname{range}(\Delta(P))$ and $\eta_0 \in \ker(\Delta(P))$, $(v_j^*)^\dagger c_S = 0$ for all $j = 1, \dots, K(P)$ holds if and only if $\eta_\parallel - \frac{i}{2}\Delta(P)z_\parallel \in \mathcal{H}_+(P)$, which uniquely fixes $\eta_\parallel = -\frac{1}{2}\lvert M(P)\rvert z_\parallel$ while leaving $\eta_0 \in \ker(\Delta(P))$ free with $c_S = -W_{\rm SJ}(P)z_\parallel + (\eta_0 - \frac{i}{2}v_0)$. Evaluating $c_S^\dagger W_\kappa(P)^+ c_S$ on the orthogonal subspaces $\mathcal{H}_+(P)$ and $\ker(\Delta(P))$ (where $(\eta_0 - \frac{i}{2}v_0)^\dagger(\eta_0 - \frac{i}{2}v_0) = \lVert \eta_0\rVert_2^2 + \frac{1}{4}\lVert v_0\rVert_2^2$ since $\eta_0, v_0 \in \mathbb{R}^N$) yields the exact formula and unique minimizer $\eta_0 = 0$. Under $W_\kappa(P)$, $z_\parallel^T \hat{\Phi}_P$ and $\hat{P}_{\rm new}$ have vanishing symmetrized cross-covariance at $\eta_0 = 0$, $\langle \hat{X}_{\rm new}^2\rangle = \frac{\kappa}{2}$, and $\langle \hat{P}_{\rm new}^2\rangle \ge (4\langle \hat{X}_{\rm new}^2\rangle)^{-1} = \frac{1}{2\kappa}$ gives $\langle \hat{\phi}(x)^2\rangle = \langle (z_\parallel^T \hat{\Phi}_P)^2\rangle + \lVert v_0\rVert_2^2 \langle \hat{P}_{\rm new}^2\rangle \ge \sigma_{x,\min}^2(\kappa)$. $\blacksquare$

To compose births across **arbitrary horizons** $P_1 \to P_2 \to \dots \to P_N$ without ever resetting intermediate states to $W_\kappa(P_n)$, observe that any mode-preserving congruence $W_{\rm cong}(P+S) = B W(P) B^T$ leaves the newborn zero mode $w_{\rm new} = \begin{pmatrix} z \\ 1 \end{pmatrix}$ at zero variance, which would block a subsequent mode-creating birth coupling to $w_{\rm new}$, while a mode-creating Schur extension produces a child state $W(P+S) \ne W_\kappa(P+S)$ with general null space. Both requirements are unified by the **Universal Range Lemma**:

**Theorem 6C (Universal Range Lemma & Composable All-Horizon Schur-Symplectic Evolution $\mathcal{T}_\kappa$) [PROVED THEOREM].**  
*For any finite poset $P$ of cardinality $N$, define the admissible Gaussian state cone:*
$$
\mathcal{C}_+(P) := \left\{ W = \gamma + \frac{i}{2}\Delta(P) \in \mathbb{C}^{N \times N} : \gamma \in \mathbb{R}^{N \times N} \text{ symmetric}, \; W \succeq 0, \; w^T \gamma w > 0 \;\; \forall w \in \ker(\Delta(P)) \setminus \{0\} \right\}.
$$
*Then for every $W \in \mathcal{C}_+(P)$, every downward-closed precursor ideal $S \in \mathcal{I}(P)$ ($v_S = \mu(I + G_A(P))\mathbf{1}_S$), and every zero-mode activation scale $\kappa > 0$:*
1. *(Universal Purely-Imaginary Kernel Exclusion & Full-Row-Rank Range Lemma.)* *$\ker W$ contains no non-zero purely imaginary vector ($\ker W \cap i\mathbb{R}^N = \{0\}$). Consequently, for any $\mathbb{C}$-basis $\{u_1, \dots, u_r\}$ of $\ker W$ ($u_m = a_m + i b_m$ with $a_m, b_m \in \mathbb{R}^N$), the $2r$ real vectors $\{a_1, \dots, a_r, b_1, \dots, b_r\} \subset \mathbb{R}^N$ are $\mathbb{R}$-linearly independent ($r = \dim_\mathbb{C}\ker W \le K(P) \le N/2$), the feasible affine space $\mathcal{A}(W, v_S) := \{\eta \in \mathbb{R}^N : \eta - \frac{i}{2}v_S \in \operatorname{range}(W)\}$ is **non-empty** for every $v_S \in \mathbb{R}^N$, and the quadratic objective $\eta \mapsto (\eta - \frac{i}{2}v_S)^\dagger W^+ (\eta - \frac{i}{2}v_S)$ is strictly convex on $\mathcal{A}(W, v_S)$ with a **unique** minimizer $\eta_S^*(W, v_S) \in \mathcal{A}(W, v_S)$.*
2. *(All-Horizon Composable State Update $\mathcal{T}_\kappa : \mathcal{C}_+(P) \to \mathcal{C}_+(P+S)$.)* *Setting $c_S^* := \eta_S^*(W, v_S) - \frac{i}{2}v_S \in \operatorname{range}(W)$ and defining:*
   $$
   \mathcal{T}_\kappa(W; S) := \begin{pmatrix} W & c_S^* \\ (c_S^*)^\dagger & \sigma_x^2(W, S; \kappa) \end{pmatrix}, \quad \sigma_x^2(W, S; \kappa) := (c_S^*)^\dagger W^+ c_S^* + \begin{cases} \frac{\kappa}{2}\left(1 + \lVert z\rVert_2^2\right) & \text{if } K(P+S) = K(P) \;\;(z = \Delta(P)^+ v_S), \\ 0 & \text{if } K(P+S) = K(P) + 1, \end{cases}
   $$
   *maps $\mathcal{C}_+(P)$ into $\mathcal{C}_+(P+S)$ across **every** birth and **every** horizon $N \ge 1$, satisfying:*
   - *Positivity & Strict Zero-Mode Support: $\mathcal{T}_\kappa(W; S) \in \mathcal{C}_+(P+S)$ (so $\mathcal{T}_\kappa$ composes across arbitrarily long growth histories $P_1 \to P_2 \to \dots \to P_N$ initialized at $W_\kappa(P_1) = \frac{\kappa}{2}I_1 \in \mathcal{C}_+(P_1)$);*
   - *Exact CCR Preservation: $\mathcal{T}_\kappa(W; S) - \mathcal{T}_\kappa(W; S)^T = i\Delta(P+S)$;*
   - *Exact Causal Past-Restriction Invariance: $[\mathcal{T}_\kappa(W; S)]_{P \times P} = W$ at every birth step (hence $[W(P_N)]_{P_m \times P_m} = W(P_m)$ for all $1 \le m \le N$, strictly preserving all past two-point correlations and prior excitations without vacuum reset).*

*Proof.*  
1. Suppose $u = i b \in \ker W$ with $b \in \mathbb{R}^N$. Then $0 = W(ib) = i\gamma b - \frac{1}{2}\Delta(P)b$; separating real and imaginary parts gives $\Delta(P)b = 0$ (so $b \in \ker(\Delta(P))$) and $\gamma b = 0$ (so $b^T \gamma b = 0$), forcing $b = 0$ because $W \in \mathcal{C}_+(P)$. Now suppose $\sum_{m=1}^r (\alpha_m a_m + \beta_m b_m) = 0$ for real scalars $\alpha_m, \beta_m \in \mathbb{R}$. Since $\ker W$ is a complex subspace, $u := \sum_{m=1}^r (\alpha_m - i\beta_m)u_m \in \ker W$ has real part $\operatorname{Re}(u) = \sum_{m=1}^r (\alpha_m a_m + \beta_m b_m) = 0$, so $u \in \ker W \cap i\mathbb{R}^N = \{0\}$. By $\mathbb{C}$-linear independence of $\{u_1, \dots, u_r\}$, $\alpha_m - i\beta_m = 0 \implies \alpha_m = \beta_m = 0$ for all $m$. Thus the $2r \times N$ real matrix $R = \begin{pmatrix} a_1 & \dots & a_r & b_1 & \dots & b_r \end{pmatrix}^T$ has full row rank $2r$. Since $u_m^\dagger(\eta - \frac{i}{2}v_S) = (a_m^T \eta - \frac{1}{2}b_m^T v_S) - i(b_m^T \eta + \frac{1}{2}a_m^T v_S) = 0$ ($m = 1, \dots, r$) is a $2r \times N$ real linear system with surjective coefficient matrix $R$, $\mathcal{A}(W, v_S)$ is non-empty for every $v_S \in \mathbb{R}^N$. Moreover, for any two distinct points $\eta_1, \eta_2 \in \mathcal{A}(W, v_S)$, $\delta := \eta_1 - \eta_2 \in (\operatorname{range}(W) \cap \mathbb{R}^N) \setminus \{0\}$, and since $W^+$ is strictly positive definite on $\operatorname{range}(W)$, $\delta^\dagger W^+ \delta > 0$, proving strict convexity and uniqueness of $\eta_S^*(W, v_S)$.
2. By Theorem 5(1), $c_S^* \in \operatorname{range}(W)$ and $\sigma_x^2(W, S; \kappa) \ge (c_S^*)^\dagger W^+ c_S^*$ immediately yield $\tilde{W} := \mathcal{T}_\kappa(W; S) \succeq 0$, $\tilde{W} - \tilde{W}^T = i\Delta(P+S)$, and $[\tilde{W}]_{P \times P} = W$. To verify strict zero-mode support on $\ker(\Delta(P+S))$, let $\tilde{w} = \begin{pmatrix} u \\ \alpha \end{pmatrix} \in \ker(\Delta(P+S)) \setminus \{0\}$ ($u \in \mathbb{R}^N, \alpha \in \mathbb{R}$), so $\Delta(P)u = \alpha v_S$ and $v_S^T u = 0$:
   - If $K(P+S) = K(P) + 1$, then $v_S \notin \operatorname{range}(\Delta(P))$ forces $\alpha = 0$ and $u \in \ker(\Delta(P)) \setminus \{0\}$, whence $\tilde{w}^T \operatorname{Re}(\tilde{W}) \tilde{w} = u^T \gamma u > 0$.
   - If $K(P+S) = K(P)$, write $\tilde{W} = \tilde{W}_0 + \frac{\kappa}{2}(1 + \lVert z\rVert_2^2)e_{N+1}e_{N+1}^T$ with $\tilde{W}_0 \succeq 0$. If $\alpha \ne 0$, then $\tilde{w}^T \operatorname{Re}(\tilde{W}) \tilde{w} \ge \frac{\kappa}{2}(1 + \lVert z\rVert_2^2)\alpha^2 > 0$; if $\alpha = 0$, then $u \in \ker(\Delta(P)) \setminus \{0\}$ and $\tilde{w}^T \operatorname{Re}(\tilde{W}) \tilde{w} = u^T \gamma u > 0$.  
   Hence $\mathcal{T}_\kappa(W; S) \in \mathcal{C}_+(P+S)$ in all cases. $\blacksquare$

**Obstruction 3 (Two-Step Diamond Symmetric Ordering Discrepancy vs. Exact CCR & Marginal Confluence) [COUNTEREXAMPLE/OBSTRUCTION].**  
*Consider any incomparable two-step growth diamond $P \to (P_1 = P+x_S \text{ vs. } P_2 = P+y_T) \to Q = P + x_S + y_T$ ($S \not\subseteq T, T \not\subseteq S$) initialized at $W_0 = W_\kappa(P)$ ($\kappa = 1$), comparing $W_{12} = \mathcal{T}_\kappa(\mathcal{T}_\kappa(W_0; S); T)$ against the coordinate-permuted state $\tilde{W}_{21} = P_{\rm swap}\,\mathcal{T}_\kappa(\mathcal{T}_\kappa(W_0; T); S)\,P_{\rm swap}^T$:*
1. *Across all **441 / 441** incomparable diamonds ($N \le 4$), both path states satisfy $W_{12} \succeq 0$ and $\tilde{W}_{21} \succeq 0$, preserve exact causal marginals ($[W_{12}]_{P \times P} = [\tilde{W}_{21}]_{P \times P} = W_0$, eliminating spacelike marginal disturbance on $P$), and have **identically equal imaginary parts**:*
   $$
   \operatorname{Im}(W_{12} - \tilde{W}_{21}) = \frac{1}{2}\bigl(\Delta(Q) - \Delta(Q)\bigr) \equiv 0.
   $$
2. *Across **281 / 441** diamonds ($63.7\%$, including $1/1$ at $N = 2$ and $15/20$ at $N = 3$), the full two-point Gaussian state commutes identically ($W_{12} = \tilde{W}_{21}$).*
3. *Starting at parent size $N = 3$ on **5 / 20** diamonds—first occurring on the disjoint union poset $P = C_2 \sqcup A_1$ ($0 \prec 1$, $2$ isolated) with $S = \{0, 1\}$ (mode-preserving) and $T = \{0, 2\}$ (mode-creating), where $\max\lvert\operatorname{Re}(W_{12} - \tilde{W}_{21})\rvert = 1.000000$—and on **155 / 420** diamonds at $N = 4$ (**160 / 441** total, $36.3\%$, $\max = 5.833333$), the real symmetric Hadamard block exhibits path-ordering dependence $\operatorname{Re}(W_{12} - \tilde{W}_{21}) \ne 0$ whenever intermediate zero-mode creation/consumption alters the active Schur subspace seen by the spacelike partner birth.*

---

## 5. Local Covering-Link Stress & The Finite Diamond Obstruction

### 5.1 Discrete Link Stress and Boundary Energy Flux
In background-free causal set theory, continuous spacetime derivatives $\partial_\mu \phi$ are replaced natively by finite differences along covering relations (links).

**Definition 5.1 (Covering Relations / Links).**  
A causal relation $v \prec u$ is a covering link, denoted $(v, u) \in \operatorname{Link}(P)$, if the open causal interval between them is strictly empty:
$$
I(v, u) := \{ w \in P : v \prec w \prec u \} = \varnothing.
$$
The link set $\operatorname{Link}(P)$ coincides with the support of the non-transitive layer-1 incidence matrix $A_1(P) = C_P - (C_P^2 > 0)$.

**Proposition 5.1 (Link Invariance and Creation under Sequential Growth).**  
*Let $P$ be a poset and $S \in \mathcal{I}(P)$ a downward-closed ideal. When newborn vertex $x$ adjoins to $S$:*
1. *All pre-existing links of $P$ are strictly preserved: $\operatorname{Link}(P) \subseteq \operatorname{Link}(P+S)$;*
2. *The newly created links are precisely the incoming links from the maximal elements of $S$:*
   $$
   \Delta \operatorname{Link}(P \to P+S) := \operatorname{Link}(P+S) \setminus \operatorname{Link}(P) = \{ (v, x) : v \in \operatorname{Max}(S) \}.
   $$

*Proof.*  
Since $x$ is maximal in $P+S$, no existing pair $(v, u) \in \operatorname{Link}(P)$ can have $x \in I(v, u)$. Hence no links are destroyed, proving $\operatorname{Link}(P) \subseteq \operatorname{Link}(P+S)$.  
Now consider an incoming relation $v \prec x$, which means $v \in S$. The relation $(v, x)$ is a covering link if and only if there is no $w \in P+S$ such that $v \prec w \prec x$. Since $w \prec x \iff w \in S$, this is equivalent to saying there is no $w \in S$ with $v \prec w$. By definition, this means $v \in \operatorname{Max}(S)$. $\blacksquare$

**Definition 5.2 (Covering-Link Quantum Stress and Fluctuation Variance).**  
For any link $(v, u) \in \operatorname{Link}(P)$:
1. The **normal-ordered quantum link stress observable** with respect to the Sorkin–Johnston vacuum covariance $W_{\rm SJ}$ is:
   $$
   \mathcal{T}_{\rm link}(v, u) := \frac{1}{2}:(\phi(u) - \phi(v))^2:_{W_{\rm SJ}} = \frac{1}{2}\left( (\phi(u) - \phi(v))^2 - \langle 0_{\rm SJ}\mid (\phi(u) - \phi(v))^2 \mid 0_{\rm SJ}\rangle \right).
   $$
   By definition of normal ordering, its Sorkin–Johnston vacuum expectation value vanishes identically:
   $$
   \langle 0_{\rm SJ}\mid \mathcal{T}_{\rm link}(v, u)\mid 0_{\rm SJ}\rangle \equiv 0.
   $$
2. The **unrenormalized two-point link fluctuation variance** is:
   $$
   \mathcal{E}_{\rm fluc}(v, u; P) := \langle 0_{\rm SJ}\mid (\phi(u) - \phi(v))^2 \mid 0_{\rm SJ}\rangle = (W_{\rm SJ}(P))_{uu} + (W_{\rm SJ}(P))_{vv} - 2\operatorname{Re}(W_{\rm SJ}(P))_{uv} \ge 0.
   $$
   The local boundary energy flux carried across newly created links upon birth $P \to P+S$ is the sum of unrenormalized fluctuation variances:
   $$
   \Phi_{\rm flux}(P \to P+S) := \sum_{v \in \operatorname{Max}(S)} \mathcal{E}_{\rm fluc}(v, x; P+S).
   $$
   *Remark on the Factor of $1/2$*: The kinetic link stress observable $\mathcal{T}_{\rm link}$ incorporates the standard kinetic prefactor of $1/2$. In contrast, $\mathcal{E}_{\rm fluc}(v, u; P)$ is defined directly as the raw two-point difference variance (e.g., $\mathcal{E}_{\rm fluc}(0, 1; C_2) = 1.000000$ on $C_2$, where $W_{00} = W_{11} = 0.5$ and $\operatorname{Re}(W_{01}) = 0$). The total discrete field Hamiltonian $H_{\rm field}(P) = \sum_{e \in \operatorname{Link}(P)} \mathcal{E}_{\rm fluc}(e; P)$ sums these unrenormalized link fluctuation variances directly, maintaining consistency with all subsequent numerical calculations and verification tests.

### 5.2 Growth Diamonds and Cumulative Link Flux
In classical sequential growth, discrete general covariance is expressed by commutation across elementary growth diamonds. Let $C$ be a base poset of cardinality $n-1$, and let $S, T \in \mathcal{I}(C)$ be two downward-closed precursor ideals. The confluence of adjoining $x_S$ and $y_T$ forms a diamond with two alternative paths to the confluent poset $Q = C + x_S + y_T$:
- **Path 1**: $C \xrightarrow{\text{adjoin } x_S} P_1 = C+x_S \xrightarrow{\text{adjoin } y_T} Q$.
- **Path 2**: $C \xrightarrow{\text{adjoin } y_T} P_2 = C+y_T \xrightarrow{\text{adjoin } x_S} Q$.

When the births are incomparable in $Q$ ($x \parallel y$), the ideals satisfy $S \not\subseteq T$ and $T \not\subseteq S$. The cumulative boundary fluxes along the two paths are:
$$
\Phi^{(1)} = \sum_{v \in \operatorname{Max}(S)} \mathcal{E}_{\rm fluc}(v, x; P_1) + \sum_{w \in \operatorname{Max}(T)} \mathcal{E}_{\rm fluc}(w, y; Q),
$$
$$
\Phi^{(2)} = \sum_{w \in \operatorname{Max}(T)} \mathcal{E}_{\rm fluc}(w, y; P_2) + \sum_{v \in \operatorname{Max}(S)} \mathcal{E}_{\rm fluc}(v, x; Q).
$$
The loop circulation (curl) around the growth diamond is:
$$
\oint_{\rm diamond} \Phi_{\rm flux} := \Phi^{(1)} - \Phi^{(2)}.
$$

### 5.3 The Finite Diamond Obstruction at $N=5$ and $N=6$
We now prove the breakdown of step-by-step covering-link flux balance across causal set growth diamonds.

**Obstruction 1 (Finite Diamond Obstruction to Local Link Flux) [COUNTEREXAMPLE/OBSTRUCTION].**  
*Step-by-step local covering-link energy flux $\Phi_{\rm flux}$ is NOT a closed 1-form on the causal set growth graph. Specifically:*
1. *For all child posets of cardinality $N \le 4$ (parents $N \le 2$), incomparable-ideal diamond swaps satisfy exact link flux balance: $\oint_{\rm diamond} \Phi_{\rm flux} = 0$;*
2. *Exact balance strictly breaks down at child size $N = 5$ (parent $N = 3$). Across the 20 incomparable growth diamonds at $N = 5$, exactly 3 exhibit non-zero circulation, all originating on the disjoint union base poset:*
   $$
   P = C_2 \sqcup A_1 \quad (\text{relations: } 0 \prec 1, \quad 2 \text{ isolated}),
   $$
   *with precursor ideals $S = \{0, 1\}$ ($\operatorname{Max}(S) = \{1\}$) and $T = \{0, 2\}$ ($\operatorname{Max}(T) = \{0, 2\}$). The loop circulation discrepancy is:*
   $$
   \lvert\Delta H_{\rm diamond}\rvert = \lvert\Phi^{(1)} - \Phi^{(2)}\rvert = \lvert 3.468721 - 3.130294\rvert = 0.338427 \ne 0;
   $$
3. *At child size $N = 6$ (parent $N = 4$), the obstruction expands dramatically: across the 420 incomparable growth diamonds, exactly 207 exhibit non-zero circulation, with maximum discrepancy:*
   $$
   \max \lvert\Delta H_{\rm diamond}\rvert = 0.936226.
   $$

*Proof by Exact Analytic and Numerical Evaluation.*  
Consider the base poset $P = C_2 \sqcup A_1$ with vertices $\{0, 1, 2\}$ and causal incidence matrix:
$$
C_P = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}.
$$
The ideals are $S = \{0, 1\}$ (causal chain) and $T = \{0, 2\}$ (disjoint elements). Note $S \not\subseteq T$ and $T \not\subseteq S$.  
- **Path 1**: Adjoin $x$ to $S = \{0, 1\}$ at index 3, then adjoin $y$ to $T = \{0, 2\}$ at index 4.
  - Step 1 ($P \to P_1$): $P_1$ has relations $0 \prec 1 \prec x$, with element $2$ isolated ($P_1 \cong C_3 \sqcup A_1$). $\operatorname{Max}(S) = \{1\}$, so the only new link is $(1, x)$. Computing $W_{\rm SJ}(P_1)$ from the spectral decomposition of $M(P_1) = i\Delta(P_1)$ gives:
    $$
    \mathcal{E}_{\rm fluc}(1, x; P_1) = \frac{\sqrt{6}}{4} \approx 0.612372.
    $$
  - Step 2 ($P_1 \to Q$): $Q$ adjoins $y$ with past $T = \{0, 2\}$. The maximal elements of $T$ in $Q$ are $\operatorname{Max}(T) = \{0, 2\}$, creating new covering links $(0, y)$ and $(2, y)$. Computing $W_{\rm SJ}(Q)$ from $M(Q)$ yields:
    $$
    \mathcal{E}_{\rm fluc}(0, y; Q) \approx 1.771039, \qquad \mathcal{E}_{\rm fluc}(2, y; Q) \approx 1.085310,
    $$
    summing to Step 2 boundary flux $\Phi^{(1, 2)} = 1.771039 + 1.085310 = 2.856349$.
  - Cumulative Path 1 flux: $\Phi^{(1)} = 0.612372 + 2.856349 = 3.468721$.
- **Path 2**: Adjoin $y$ to $T = \{0, 2\}$ at index 3, then adjoin $x$ to $S = \{0, 1\}$ at index 4.
  - Step 1 ($P \to P_2$): $P_2$ adjoins $y$ to $T = \{0, 2\}$. $\operatorname{Max}(T) = \{0, 2\}$, creating new covering links $(0, y)$ and $(2, y)$. Computing $W_{\rm SJ}(P_2)$ yields:
    $$
    \mathcal{E}_{\rm fluc}(0, y; P_2) \approx 1.341641, \qquad \mathcal{E}_{\rm fluc}(2, y; P_2) \approx 1.118034,
    $$
    summing to Step 1 boundary flux $\Phi^{(2, 1)} = 1.341641 + 1.118034 = 2.459675$.
  - Step 2 ($P_2 \to Q$): $Q$ adjoins $x$ with past $S = \{0, 1\}$. $\operatorname{Max}(S) = \{1\}$, creating new covering link $(1, x)$. Computing its fluctuation in $W_{\rm SJ}(Q)$ yields:
    $$
    \mathcal{E}_{\rm fluc}(1, x; Q) \approx 0.670619.
    $$
  - Cumulative Path 2 flux: $\Phi^{(2)} = 2.459675 + 0.670619 = 3.130294$.
- Subtracting the two cumulative fluxes:
$$
\oint_{\rm diamond} \Phi_{\rm flux} = \Phi^{(1)} - \Phi^{(2)} = 3.468721 - 3.130294 = 0.338427 \ne 0.
$$
The 3 discrepancies at $N=5$ and 207 discrepancies at $N=6$ are confirmed by mechanical execution of Check 11 of the master suite. $\blacksquare$

*Analytic Counterexample on Canonical Two-Chain ($C_2$)*:  
Even on nested ideals ($S \subset T$), local link flux exhibits non-zero circulation. Let $C = C_2 = (0 \prec 1)$ with $S = \{0\}$ and $T = \{0, 1\}$.
- Path 1 ($C_2 \to \text{Fork } V \to Q$): $\Phi^{(1)} = \frac{3\sqrt{2}}{4} + \frac{5}{6} \approx 1.893994$.
- Path 2 ($C_2 \to C_3 \to Q$): $\Phi^{(2)} = \frac{\sqrt{6}}{4} + \frac{3}{2} \approx 2.112372$.
- Circulation:
  $$
  \oint_{\rm diamond} \Phi_{\rm flux} = \Phi^{(1)} - \Phi^{(2)} = \frac{3\sqrt{2} - \sqrt{6}}{4} - \frac{2}{3} \approx -0.218379 \ne 0.
  $$

### 5.4 Cohomological Impossibility of Global Scalar Compensation
In Stage 2 (`PW2-B`), lost quantum expectation was absorbed by an artificial scalar potential $V_{\rm geom}(P)$ defined on unlabeled posets. We now prove that this mechanism fails identically for multi-mode covering-link stress.

**Obstruction 2 (Poincaré Cohomological No-Go for Global Scalar Potential) [COUNTEREXAMPLE/OBSTRUCTION].**  
*There exists NO mark-independent scalar potential $V : \bigsqcup_{n} \mathcal{U}_n \to \mathbb{R}$ defined on unlabeled posets that can compensate step-by-step covering-link energy flux across causal set sequential growth.*

*Proof.*  
Let $G_{\rm growth} = (\mathcal{V}_{\rm growth}, \mathcal{E}_{\rm growth})$ denote the directed acyclic graph of causal set sequential growth, whose vertices are isomorphism classes of posets $\mathcal{U}$ and whose directed edges correspond to elementary births $P \to P+S$. An assignment of step-by-step energy increments across births defines a discrete 1-cochain $\Phi \in C^1(G_{\rm growth})$.  
A 1-cochain $\Phi$ can be compensated by a 0-cochain scalar potential $V \in C^0(G_{\rm growth})$ such that:
$$
\Phi(P \to P+S) = V(P+S) - V(P) \quad (\forall P \to P+S),
$$
if and only if $\Phi$ is an exact 1-cochain: $\Phi = \delta V$.  
By the discrete Poincaré lemma on graphs (cellular 1-cohomology $H^1$), a 1-cochain is exact if and only if its circulation around every fundamental 2-cell (elementary growth diamond) vanishes identically:
$$
\delta \Phi = 0 \iff \oint_{\rm diamond} \Phi = 0 \quad (\forall \text{ diamonds}).
$$
For any putative mark-independent scalar function $V(P)$, the sum of potential differences along the two paths of an elementary diamond $C \to (P_1 \text{ vs. } P_2) \to Q$ evaluates to:
$$
\Delta V_{\rm Path 1} = (V(P_1) - V(C)) + (V(Q) - V(P_1)) = V(Q) - V(C),
$$
$$
\Delta V_{\rm Path 2} = (V(P_2) - V(C)) + (V(Q) - V(P_2)) = V(Q) - V(C).
$$
Therefore:
$$
\oint_{\rm diamond} \delta V = \Delta V_{\rm Path 1} - \Delta V_{\rm Path 2} \equiv 0 \quad \text{identically!}
$$
Because the scalar potential difference telescopes identically to zero around every closed diamond loop, the net circulation of the combined flux-plus-potential increment is:
$$
\oint_{\rm diamond} (\Phi_{\rm flux} - \delta V) = \oint_{\rm diamond} \Phi_{\rm flux} - \oint_{\rm diamond} \delta V = \oint_{\rm diamond} \Phi_{\rm flux} - 0 = \oint_{\rm diamond} \Phi_{\rm flux}.
$$
By Obstruction 1, $\oint_{\rm diamond} \Phi_{\rm flux} = 0.338427 \ne 0$ on $P = C_2 \sqcup A_1$. Consequently, no choice of scalar function $V(P)$ can ever vanish this circulation. Global scalar compensation is cohomologically impossible. $\blacksquare$

---

## 6. Resolution via Relativistic Divergence Balance (GD-01)

### 6.1 The Relativistic Motivation: Absence of Global Scalar Energy in Curved Spacetime
The failure of local covering-link flux $\Phi_{\rm flux}$ to form an exact 1-form is not a pathological breakdown of discrete general covariance. Rather, it reflects the foundational principle of general relativity codified in guideline `GD-01` of `docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md`:
> *"Relativistic source interpretation concerns energy, momentum, stresses and their coupling. State local balance and boundary flux assumptions. **Do not require a globally conserved scalar energy on every curved spacetime without the additional structure that defines it.** Conventional GR dynamics and Noether-charge methods provide conditional comparison tools, not native derivations."*

In general relativity, a globally conserved scalar energy exists if and only if the spacetime possesses a global timelike Killing vector field $\xi^\mu$ ($\nabla_{(\mu}\xi_{\nu)} = 0$). On a generic, dynamically fluctuating curved spacetime, no such Killing symmetry exists. The motivating continuum conservation law is the local covariant divergence of stress-energy:
$$
\nabla_\mu T^{\mu\nu} = 0.
$$
Integrating $\nabla_\mu T^{\mu\nu} = 0$ over a spacetime volume $\Omega$ with boundary $\partial \Omega$ via Gauss's divergence theorem yields:
$$
\int_\Omega \nabla_\mu T^{\mu 0} \, dV = \oint_{\partial \Omega} T^{i 0} \, d\Sigma_i + \int_\Omega \Gamma^\mu_{\mu \alpha} T^{\alpha 0} \, dV = 0.
$$
Continuum energy balance in curved spacetime decomposes into boundary flux plus bulk gravitational stress backreaction. On a discrete causal set, we establish the exact algebraic counterpart: an exact bulk-boundary additive bookkeeping decomposition across covering links that restores diamond confluence.

### 6.2 Interior Vacuum Polarization Backreaction and Total Hamiltonian
On a finite causal set, adjoining a newborn vertex $x$ does not merely inject stress into newly created boundary links; it non-locally alters the Sorkin–Johnston vacuum covariance $W_{\rm SJ}$ across the entire interior bulk of the pre-existing poset!

**Definition 6.1 (Interior Bulk Polarization Backreaction).**  
The **interior vacuum polarization backreaction** across a birth $P \to P+S$ is the net shift in quantum fluctuation energy across all pre-existing links of $P$:
$$
\Delta H_{\rm int}(P \to P+S) := \sum_{e \in \operatorname{Link}(P)} \left( \mathcal{E}_{\rm fluc}(e; P+S) - \mathcal{E}_{\rm fluc}(e; P) \right).
$$

**Definition 6.2 (Total Field Hamiltonian).**  
The **total discrete field Hamiltonian** of the Sorkin–Johnston field on poset $P$ is the total vacuum link fluctuation energy:
$$
H_{\rm field}(P) := \sum_{e \in \operatorname{Link}(P)} \mathcal{E}_{\rm fluc}(e; P).
$$

**Theorem 7 (Bulk-Boundary Additive Bookkeeping Decomposition & Diamond Confluence) [PROVED THEOREM].**  
*For every elementary birth $P \to P+S$, the total discrete field Hamiltonian increment satisfies the exact additive bookkeeping decomposition:*
$$
\Delta H_{\rm field}(P \to P+S) = \Phi_{\rm flux}(P \to P+S) + \Delta H_{\rm int}(P \to P+S) = H_{\rm field}(P+S) - H_{\rm field}(P),
$$
*arising directly from the partition of covering links $\operatorname{Link}(P+S) = \operatorname{Link}(P) \sqcup \Delta \operatorname{Link}(P \to P+S)$. Consequently, around every elementary growth diamond:*
1. *The total field Hamiltonian change telescopes to zero identically: $\oint_{\rm diamond} \Delta H_{\rm field} = 0$;*
2. *The boundary flux circulation is algebraically balanced by the interior polarization curl:*
   $$
   \oint_{\rm diamond} \Phi_{\rm flux} + \oint_{\rm diamond} \Delta H_{\rm int} = 0 \iff \Delta \Phi_{\rm flux} = -\Delta(\Delta H_{\rm int}).
   $$

*Proof.*  
By Proposition 5.1, the link set decomposes into disjoint subsets:
$$
\operatorname{Link}(P+S) = \operatorname{Link}(P) \sqcup \Delta \operatorname{Link}(P \to P+S).
$$
Evaluating the total field Hamiltonian on $P+S$:
$$
H_{\rm field}(P+S) = \sum_{e \in \operatorname{Link}(P+S)} \mathcal{E}_{\rm fluc}(e; P+S) = \sum_{e \in \Delta \operatorname{Link}} \mathcal{E}_{\rm fluc}(e; P+S) + \sum_{e \in \operatorname{Link}(P)} \mathcal{E}_{\rm fluc}(e; P+S).
$$
By Definition 5.2, the first sum is precisely $\Phi_{\rm flux}(P \to P+S)$. Adding and subtracting $\sum_{e \in \operatorname{Link}(P)} \mathcal{E}_{\rm fluc}(e; P) = H_{\rm field}(P)$:
$$
H_{\rm field}(P+S) = \Phi_{\rm flux}(P \to P+S) + H_{\rm field}(P) + \sum_{e \in \operatorname{Link}(P)} \left( \mathcal{E}_{\rm fluc}(e; P+S) - \mathcal{E}_{\rm fluc}(e; P) \right).
$$
By Definition 6.1, the last term is $\Delta H_{\rm int}(P \to P+S)$. Therefore:
$$
\Delta H_{\rm field}(P \to P+S) = H_{\rm field}(P+S) - H_{\rm field}(P) = \Phi_{\rm flux}(P \to P+S) + \Delta H_{\rm int}(P \to P+S).
$$
Because $H_{\rm field}(P)$ is a well-defined function on posets, its variation along any closed loop in the growth graph telescopes to zero:
$$
\oint_{\rm diamond} \Delta H_{\rm field} = (H(Q) - H(P_1) + H(P_1) - H(C)) - (H(Q) - H(P_2) + H(P_2) - H(C)) = (H(Q) - H(C)) - (H(Q) - H(C)) = 0.
$$
Substituting $\Delta H_{\rm field} = \Phi_{\rm flux} + \Delta H_{\rm int}$ yields $\oint_{\rm diamond} \Phi_{\rm flux} + \oint_{\rm diamond} \Delta H_{\rm int} = 0$. $\blacksquare$

*Epistemic Status and Distinction from Continuum Conservation*:  
Theorem 7 is an **exact additive bookkeeping decomposition** on the directed acyclic graph of causal set growth. It establishes that because the discrete field Hamiltonian $H_{\rm field}(P)$ is defined directly as a state function summing unrenormalized link fluctuations over covering links, its variation around any closed growth diamond telescopes algebraically to zero ($\oint_{\rm diamond} \Delta H_{\rm field} \equiv 0$). This guarantees diamond confluence in alignment with guideline `GD-01`. However, this discrete bookkeeping identity does NOT constitute a derived dynamical general relativistic conservation law $\nabla_\mu T^{\mu\nu} = 0$; genuine dynamical conservation in the Poisson sprinkling continuum limit remains an open problem (formally classified as Conjecture 1 in Section 6.4).

### 6.3 Exact Diamond Confluence and Discrete Stress Divergence
We illustrate the exact cancellation on the canonical diamond $C_2 \to (V \text{ vs. } C_3) \to Q$:
- On Base $C_2 = (0 \prec 1)$, there is a single link $e_0 = (0, 1)$ with initial fluctuation $\mathcal{E}_{\rm fluc}(0, 1; C_2) = 1.000000$, giving base field Hamiltonian $H(C_2) = 1.000000$.
- In fork $V$ (relations $0 \prec 1, 0 \prec 2$), covering links are $(0, 1)$ and $(0, 2)$, each with fluctuation $\frac{3\sqrt{2}}{4} \approx 1.060660$. The field Hamiltonian is $H(V) = 2 \times \frac{3\sqrt{2}}{4} = \frac{3\sqrt{2}}{2} \approx 2.121320$.
- In chain $C_3$ (relations $0 \prec 1 \prec 2$), covering links are $(0, 1)$ and $(1, 2)$, each with fluctuation $\frac{\sqrt{6}}{4} \approx 0.612372$. The field Hamiltonian is $H(C_3) = 2 \times \frac{\sqrt{6}}{4} = \frac{\sqrt{6}}{2} \approx 1.224745$.
- In confluent child $Q$ (relations $0 \prec 1, 0 \prec 2, 1 \prec 3, 0 \prec 3$), the covering links are $(0, 1), (0, 2)$, and $(1, 3)$. Evaluating their fluctuations in $W_{\rm SJ}(Q)$ gives:
  $$
  \mathcal{E}_{\rm fluc}(0, 1; Q) = 1.000000, \quad \mathcal{E}_{\rm fluc}(0, 2; Q) = \frac{3}{2} = 1.500000, \quad \mathcal{E}_{\rm fluc}(1, 3; Q) = \frac{5}{6} \approx 0.833333.
  $$
  The confluent field Hamiltonian is $H(Q) = 1 + \frac{3}{2} + \frac{5}{6} = \frac{10}{3} \approx 3.333333$.
- **Path 1** ($C_2 \to V \to Q$):
  - Step 1 ($C_2 \to V$): Link $(0, 1)$ shifts from $1.000000$ to $\frac{3\sqrt{2}}{4} \approx 1.060660$.  
    Interior backreaction: $\Delta H_{\rm int}^{(1, 1)} = \frac{3\sqrt{2}}{4} - 1 \approx +0.060660$.  
    Boundary flux (new link $(0, 2)$): $\Phi^{(1, 1)} = \frac{3\sqrt{2}}{4} \approx 1.060660$.  
    Step 1 total increment: $\Delta H_1 = \Phi^{(1, 1)} + \Delta H_{\rm int}^{(1, 1)} = \frac{3\sqrt{2}}{2} - 1 \approx 1.121320 = H(V) - H(C_2)$.
  - Step 2 ($V \to Q$): Existing links $(0, 1)$ and $(0, 2)$ shift from $\frac{3\sqrt{2}}{4}$ to $1.000000$ and $\frac{3}{2} = 1.500000$.  
    Interior backreaction: $\Delta H_{\rm int}^{(1, 2)} = \left(1 - \frac{3\sqrt{2}}{4}\right) + \left(\frac{3}{2} - \frac{3\sqrt{2}}{4}\right) = \frac{5}{2} - \frac{3\sqrt{2}}{2} \approx 0.378680$.  
    Boundary flux (new link $(1, 3)$): $\Phi^{(1, 2)} = \frac{5}{6} \approx 0.833333$.  
    Step 2 total increment: $\Delta H_2 = \Phi^{(1, 2)} + \Delta H_{\rm int}^{(1, 2)} = \frac{10}{3} - \frac{3\sqrt{2}}{2} \approx 1.212013 = H(Q) - H(V)$.
  - Total Path 1 Hamiltonian change: $\Delta H_{\rm field}^{(1)} = \Delta H_1 + \Delta H_2 = \frac{10}{3} - 1 = \frac{7}{3} \approx 2.333333$.
- **Path 2** ($C_2 \to C_3 \to Q$):
  - Step 1 ($C_2 \to C_3$): Link $(0, 1)$ shifts from $1.000000$ to $\frac{\sqrt{6}}{4} \approx 0.612372$.  
    Interior backreaction: $\Delta H_{\rm int}^{(2, 1)} = \frac{\sqrt{6}}{4} - 1 \approx -0.387628$.  
    Boundary flux (new link $(1, 2)$): $\Phi^{(2, 1)} = \frac{\sqrt{6}}{4} \approx 0.612372$.  
    Step 1 total increment: $\Delta H_1 = \Phi^{(2, 1)} + \Delta H_{\rm int}^{(2, 1)} = \frac{\sqrt{6}}{2} - 1 \approx 0.224745 = H(C_3) - H(C_2)$.
  - Step 2 ($C_3 \to Q$): Existing links $(0, 1)$ and $(1, 2)$ shift from $\frac{\sqrt{6}}{4}$ to $1.000000$ and $\frac{5}{6} \approx 0.833333$.  
    Interior backreaction: $\Delta H_{\rm int}^{(2, 2)} = \left(1 - \frac{\sqrt{6}}{4}\right) + \left(\frac{5}{6} - \frac{\sqrt{6}}{4}\right) = \frac{11}{6} - \frac{\sqrt{6}}{2} \approx 0.608588$.  
    Boundary flux (new link $(0, 3)$): $\Phi^{(2, 2)} = \frac{3}{2} = 1.500000$.  
    Step 2 total increment: $\Delta H_2 = \Phi^{(2, 2)} + \Delta H_{\rm int}^{(2, 2)} = \frac{10}{3} - \frac{\sqrt{6}}{2} \approx 2.108588 = H(Q) - H(C_3)$.
  - Total Path 2 Hamiltonian change: $\Delta H_{\rm field}^{(2)} = \Delta H_1 + \Delta H_2 = \frac{10}{3} - 1 = \frac{7}{3} \approx 2.333333$.
- Subtracting the total changes gives $\oint_{\rm diamond} \Delta H_{\rm field} = \frac{7}{3} - \frac{7}{3} = 0.000000$ identically!  
The curl of boundary flux $\Delta \Phi = \Phi^{(1)} - \Phi^{(2)} = \left(\frac{3\sqrt{2}}{4} + \frac{5}{6}\right) - \left(\frac{\sqrt{6}}{4} + \frac{3}{2}\right) = \frac{3\sqrt{2} - \sqrt{6}}{4} - \frac{2}{3} \approx -0.218379$ is cancelled to twelve decimal places by the interior backreaction curl $\Delta(\Delta H_{\rm int}) = \left(\Delta H_{\rm int}^{(1, 1)} + \Delta H_{\rm int}^{(1, 2)}\right) - \left(\Delta H_{\rm int}^{(2, 1)} + \Delta H_{\rm int}^{(2, 2)}\right) = \left(\frac{3}{2} - \frac{3\sqrt{2}}{4}\right) - \left(\frac{5}{6} - \frac{\sqrt{6}}{4}\right) = \frac{2}{3} - \frac{3\sqrt{2} - \sqrt{6}}{4} \approx +0.218379$.

### 6.4 Open Continuum Conjecture
While discrete divergence balance is an exact algebraic theorem on all finite posets, connecting this discrete law to the Einstein field equations remains an open problem.

**Conjecture 1 (Continuum Stress-Energy Conservation Limit) [OPEN CONJECTURE].**  
*Let $\mathcal{M}$ be a 4-dimensional globally hyperbolic Lorentzian spacetime, and let $P_N \sim \operatorname{Poisson}(\mathcal{M}, \rho)$ be a sequence of Poisson-sprinkled causal sets with density $\rho \to \infty$. Then the discrete link stress divergence $\Delta \Phi_{\rm flux} + \Delta(\Delta H_{\rm int})$ converges weakly in expectation to the continuum stress-energy conservation identity:*
$$
\lim_{\rho \to \infty} \mathbb{E}\left[ \rho^2 \left( \Phi_{\rm flux} + \Delta H_{\rm int} \right) \right] = \int_\Omega \nabla_\mu T^{\mu 0} \, d^4x = 0.
$$
*Status*: Open Conjecture. No claim is made in this protocol that the continuum limit has been proved.

---

## 7. Mechanical Poset Verification Across All 5,231 Posets ($N \le 6$)

### 7.1 Verification Architecture and Poset Census
The theorems and finite obstructions in this protocol have been subjected to exhaustive automated mechanical verification via the external scratch suite (`teamwork_master_verification/run_master_n_le_6_suite.py`, `check11_stage5b_pfaffian_cptp_flux_balance.py`).

The master suite evaluates all $5{,}231$ naturally ordered posets for $N \le 6$:
- $N = 1$: 1 poset
- $N = 2$: 2 posets
- $N = 3$: 7 posets
- $N = 4$: 40 posets
- $N = 5$: 357 posets
- $N = 6$: 4,824 posets
- **Total Posets Verified**: **5,231 posets**.

### 7.2 Check 11 Automated Results (5,230 Extensions & 1,619 Diamonds)
Check 11 of the master suite implements the automated verification of Stage 5B across two comprehensive test tiers:

#### Tier 1: Skew-Bordering, Pfaffian Sign, Gaussian Dichotomy & Bogoliubov Equivalence ($N \le 5 \to N+1 \le 6$)
Evaluated across all **5,230 child birth extensions** generated by adjoining a downward-closed ideal $S \in \mathcal{I}(P)$ to every poset $P$ with $N \le 5$:
- **Mode-Preserved Extensions ($K(P+S) = K(P)$)**:
  - Observed in exactly **2,241 extensions** ($42.8\%$).
  - In all 2,241 instances, $v_S \in \operatorname{range}(\Delta(P)) \iff v_S \perp \ker(\Delta(P))$ held with residual $< 10^{-10}$, and the unique minimal-noise marginal-preserving congruence extension $W_{\rm ext}(P+S)$ with $\eta_S = -\frac{1}{2}\lvert M(P)\rvert z$ satisfied $W_{\rm ext}(P+S) \succeq 0$ and CCR $W_{\rm ext} - W_{\rm ext}^T = i\Delta(P+S)$ across **2,241 / 2,241** births.
- **Mode-Created Extensions ($K(P+S) = K(P) + 1$)**:
  - Observed in exactly **2,989 extensions** ($57.2\%$).
  - In all 2,989 instances, $v_S \notin \operatorname{range}(\Delta(P)) \iff \exists w \in \ker(\Delta(P))$ with $w^T v_S \ne 0$, strictly obstructing marginal preservation and activating the mode-isometric Fock CPTP lift.
- **Universal Null-Space Activated Schur Extension ($W_\kappa(P)$ with $\kappa = 1.0$)**:
  - Evaluated across all **5,230 / 5,230** extensions (both mode-preserving and mode-creating).
  - In all 5,230 instances, decomposing $v_S = \Delta(P)z_\parallel + v_0$ yielded $c_S \in \operatorname{range}(W_\kappa(P))$ with $(v_j^*)^\dagger c_S = 0$ for all negative-frequency modes $\mathcal{H}_-(P)$, and the extended covariance $W_{\kappa, \operatorname{ext}}(P+S)$ with minimal newborn variance $\sigma_{x,\min}^2(\kappa) = \frac{1}{2}z_\parallel^T \lvert M(P)\rvert z_\parallel + \frac{1}{2\kappa}\lVert v_0\rVert_2^2$ satisfied complete positivity $W_{\kappa, \operatorname{ext}} \succeq 0$ and exact CCR $W_{\kappa, \operatorname{ext}} - W_{\kappa, \operatorname{ext}}^T = i\Delta(P+S)$ across **5,230 / 5,230** births.
- **Null-Space Activated Spectral & Rank Theorem ($\operatorname{rank}(W_\kappa(P)) = N - K(P)$)**:
  - Evaluated across all **5,231 / 5,231** posets ($N \le 6$).
  - For every poset, $W_\kappa(P) - W_\kappa(P)^T = i\Delta(P)$ held with residual $< 10^{-10}$, the positive rank was exactly $N - K(P)$, the zero eigenspace had dimension exactly $K(P)$, and the kernel coincided identically with the negative-frequency subspace $\ker(W_\kappa(P)) = \mathcal{H}_-(P)$, proving $\operatorname{range}(W_\kappa(P)) = \mathcal{H}_+(P) \oplus \ker(\Delta(P))$ with zero violations.
- **Exact Odd-to-Even 1D-Kernel Pfaffian Formula ($\operatorname{Pf}(\Delta(P+S)) = -w^T v_S$)**:
  - Verified with zero sign or magnitude error across all **3,486 / 3,486** odd-to-even 1D-kernel birth extensions ($N \in \{1, 3, 5\}$, $\dim\ker(\Delta(P)) = 1$).
- **Exact Discrete Bogoliubov Mixing Equivalence ($\sum_{k,j}\lvert\beta_{kj}\rvert^2 > 0 \iff \Delta(P)v_S \ne 0$)**:
  - Verified across all **5,230 / 5,230** extensions (4,468 births with active particle creation $\Delta(P)v_S \ne 0$; 762 decoupled births with $\beta \equiv 0$, consisting of 407 empty births $S = \varnothing$ and 355 non-empty births with $v_S \in \ker(\Delta(P))$).
- **Adherence Rate**: **5,230 / 5,230 (100.0% PASS, 0 failures, 0 warnings)**.

#### Tier 2: Covering-Link Flux Balance & Finite Diamond Obstruction ($N \le 4 \to N+2 \le 6$)
Evaluated across all **1,619 growth diamonds**, of which **441 are incomparable-ideal diamonds** ($S \not\subseteq T, T \not\subseteq S$):
- **Child Posets $N \le 4$ (Parents $N \le 2$)**:
  - Total incomparable diamonds: 1 ($A_2$ with $S=\{0\}, T=\{1\}$).
  - Observed discrepancy: $\lvert\Delta H_{\rm diamond}\rvert = 0.000000$ (exact balance).
- **Child Posets $N = 5$ (Parents $N = 3$)**:
  - Total incomparable diamonds: 20.
  - Discrepancies observed: exactly **3 discrepancies** ($15.0\%$).
  - All 3 discrepancies occur on the base poset $P = C_2 \sqcup A_1$ with ideals $S=\{0, 1\}$ and $T=\{0, 2\}$.
  - Exact numerical value: $\lvert\Delta H_{\rm diamond}\rvert = 0.338427$.
- **Child Posets $N = 6$ (Parents $N = 4$)**:
  - Total incomparable diamonds: 420.
  - Discrepancies observed: exactly **207 discrepancies** ($49.3\%$).
  - Maximum discrepancy: $\max \lvert\Delta H_{\rm diamond}\rvert = 0.936226$.
- **Total Field Hamiltonian Confluence**:
  - For all 1,619 diamonds, the bulk-plus-boundary balance $\oint_{\rm diamond} (\Phi_{\rm flux} + \Delta H_{\rm int}) = 0$ held identically with numerical residual $< 10^{-12}$.
- **Composable All-Horizon State Transition Census (`frontier_b_gaussian_state_transition.py`)**:
  - Across all **2,241** mode-preserving births ($K(P+S) = K(P)$), symplectic congruence $B W(P) B^T$ preserved positivity, CCR, parent marginals, zero-mode annihilation, and non-decaying excitation propagation ($\operatorname{Tr}(\Delta W(P+S)) \ge \operatorname{Tr}(\Delta W(P))$).
  - Across all **2,989** mode-creating births ($K(P+S) = K(P)+1$), canonical quadratures $(\hat{X}_{\rm new}, \hat{P}_{\rm new})$ satisfied $[\hat{X}_{\rm new}, \hat{P}_{\rm new}] = i\mathbf{1}$, decoupled from parent symplectic/zero modes, and matched the Albert–Schur minimal variance $\sigma_{x,\min}^2(\kappa)$.
  - Across all **441** incomparable diamonds ($N \le 4$) under genuine two-step composable $\mathcal{T}_\kappa$ evolution, **441 / 441** preserved positivity, step-by-step causal marginals ($[W_{12}]_{P_1 \times P_1} = W_1$, $[W_{12}]_{P \times P} = W_0$), and exact CCR ($\operatorname{Im}(W_{12} - \tilde{W}_{21}) = 0$), with **281 / 441** ($63.7\%$) commuting identically ($W_{12} = \tilde{W}_{21}$) and **160 / 441** ($36.3\%$) exhibiting real symmetric ordering discrepancy starting at $P = C_2 \sqcup A_1$, alongside **200 / 200** multi-horizon 7-step trajectories ($N = 1 \to 8$) preserving all nested causal marginals $[W_8]_{P_m \times P_m} = W_m$.
- **Adherence Rate**: **1,619 / 1,619 (100.0% PASS, 0 failures, 0 warnings)**.

### 7.3 Master Suite Execution Summary
Executing the complete suite confirms 100% mechanical verification across all 11 checks:
```
================================================================================
MASTER VERIFICATION SUITE EXECUTION SUMMARY:
================================================================================
  Check 1: Resolvent Nilpotency & Invertibility (5,231 posets)    : [PASSED] ( 0.15 s)
  Check 2: Sorkin-Johnston Field Algebra & CCR (Canonical)        : [PASSED] ( 0.08 s)
  Check 3: Exact C_4 Spectrum & Pfaffian Non-Singularity          : [PASSED] ( 0.05 s)
  Check 4: Exact 4x4 Choi Spectrum & Complete Positivity          : [PASSED] ( 0.12 s)
  Check 5: Precursor Ideals & Chain Counts C_1 != C_2             : [PASSED] ( 0.32 s)
  Check 6: Unique-Top Identity Sigma_u(Q + A_1) == 1              : [PASSED] ( 0.28 s)
  Check 7: Conditional Borel-Cantelli Dynamics (0.00% freezing)   : [PASSED] ( 0.45 s)
  Check 8: Single-History Bifurcation vs Ensemble Steering        : [PASSED] ( 0.41 s)
  Check 9: Follow-Up Review Audit (Choi, n=5, Screen 3, Birth 4)  : [PASSED] ( 0.38 s)
  Check 10: Stage 5A Precursor Covariance & Diamond Commutation   : [PASSED] ( 1.25 s)
  Check 11: Stage 5B Skew Bordering & Finite Diamond Obstruction  : [PASSED] ( 3.22 s)
--------------------------------------------------------------------------------
Total Checks Executed : 11
Checks Passed         : 11 / 11 (100.0%)
Checks Failed         : 0
Warnings Recorded     : 0
Total Execution Time  : 6.71 seconds
>>> 100% PASS: ALL 11 MASTER VERIFICATION CHECKS PASSED (0 FAILURES, 0 WARNINGS) <<<
================================================================================
```

---

## 8. Status-M Quarantine & Boundary Declarations

In strict adherence to project governance:
1. **Quarantine Affirmation**: The four Status-M core files (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) have remained 100% untouched throughout this work (0 diff lines).
2. **Software Pause Compliance**: Zero Python or executable software files were added to or modified within the git repository (`det8/`, `scripts/`, `run_tests.py`, etc.). All mechanical verification scripts live strictly in the external scratch directory.
3. **Branch Protection**: Work has been performed exclusively on branch `swarm/field-stress-gravity-bridge` at commit `a6e51abd22199d31bbf1bdc7a70154f9c232f580`. Protected branches `main` and `qr-pair-kernel-bridge` remain untouched.
4. **Non-Claims**: This protocol claims only the mathematical derivations, algebraic transition laws, finite diamond obstructions, and discrete divergence balances explicitly proved herein on finite partially ordered sets. It makes NO claim to:
   - Derive the continuum Einstein field equations $G_{\mu\nu} = 8\pi G T_{\mu\nu}$;
   - Derive the 4-dimensional continuum metric or smooth manifold topology;
   - Derive Born's rule or quantum measurement theory;
   - Calibrate the physical values of $\hbar$, $c$, or Newton's constant $G$.

---

## 9. References

1. `docs/observables/intrinsic_sorkin_johnston_stress_and_order_backreaction.md` (§2, §3, §4, §6.5, Open Proposal 6.1, §7)
2. `docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md` (`GD-01`, `GD-02`)
3. `docs/observables/intrinsic_causal_propagator_and_pauli_jordan_algebra.md` (`PW4-A`)
4. `docs/observables/record_compensated_quantum_order_conservation.md` (`PW2-B`)
5. `docs/observables/all_horizon_two_way_feedback_and_growth.md` (`PW2-A`)
6. `docs/observables/manifold_compatible_growth_scaling_and_dimension_stabilization.md` (`PW5-B`, `NG-02`)
7. External Master Poset Scratch Verification Suite (`teamwork_master_verification/run_master_n_le_6_suite.py`, `check11_stage5b_pfaffian_cptp_flux_balance.py`, `frontier_b_gaussian_state_transition.py`, Checks 1–11)
