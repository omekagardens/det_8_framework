# Prospective Research Protocol PW5-A: Intrinsic Sorkin–Johnston Stress and Order Backreaction

**Document ID**: `PW5A_PROTOCOL.md`  
**Author**: `teamwork_worker_m1`  
**Date**: 2026-11-14T01:25:00Z  
**Target Deliverable**: `/Volumes/AI_DATA/development/det_8_framework_gemini/docs/observables/intrinsic_sorkin_johnston_stress_and_order_backreaction.md`  
**Workspace**: `/Volumes/AI_DATA/development/det_8_framework_gemini/.agents/teamwork/teamwork_worker_m1/`  
**Protocol Status**: Frozen Prospective Specification  

---

## 1. Objectives & Scientific Scope

### 1.1 Purpose and Physical Vision
This prospective protocol establishes the formal mathematical specification, derivation plan, verification procedure, and governance compliance rules for authoring **Stage 4 Observable PW5-A: Intrinsic Sorkin–Johnston Stress and Order Backreaction** (`docs/observables/intrinsic_sorkin_johnston_stress_and_order_backreaction.md`).

In Stage 2 and Stage 3 investigations (`PW2-A`, `PW2-B`, `PW3-A`, `PW3-B`), quantum-order feedback and gravitational backreaction were established under two distinct formulations:
1. Multi-birth quantum-order feedback and record-compensated conservation (`PW2-A`, `PW2-B`), where quantum probe coherence steered causal growth across downward-closed precursor ideals, and lost quantum expectation was absorbed into a diamond-confluent geometric potential $V_{\rm geom}(P)$.
2. Branch-dressed cavity stress-energy and retarded curvature readouts (`PW3-A`, `PW3-B`), where history branches were coupled to an external continuous spatial cavity container $\Omega = [-L/2, L/2]^3$ with smooth eigenmodes and an exterior confining Beltrami stress collar $W_{\rm collar}$.

While mathematically rigorous, the external cavity container $[0, L]^3$, continuous spatial coordinates $(t, \mathbf{x})$, continuous wave operators $\Box$, and flat Minkowski background $\mathbb{R}^{1,3}$ represented an unphysical scaffolding that is not native to discrete causal sets.

**The primary objective of PW5-A is to close the gravitational backreaction loop natively within Stage 3's background-free world:**
- Eliminate the external continuous cavity box $[0, L]^3$, boundary collars, and continuous embedding coordinates entirely from the backreaction and conservation loop.
- Formulate native discrete stress-energy observables $\mathcal{T}_{\rm link}(v, u)$ and $\mathcal{T}(u)$ directly on the covering relations (links) of a finite causal poset $P = (V, \prec)$ using the intrinsic Sorkin–Johnston bosonic field algebra ($G_R(P), i\Delta(P), W_{\rm SJ}(P)$) established in `PW4-A`.
- Construct Fock states and coherent state excitations $\lvert \alpha\rangle$, proving that normal-ordered coherent link stress is strictly non-negative, real, and quadratic in mode displacement amplitudes.
- Couple intrinsic field excitations via a Kolmogorov-projective, diamond-commuting Completely Positive Trace-Preserving (CPTP) instrument $\mathcal{B}_{S, b}^{P, r}$ directly into sequential causal-order growth probabilities $q(P, r, S)$.
- Evaluate the discrete Benincasa–Dowker scalar curvature response ($S_{\rm BD}^{(2)}, S_{\rm BD}^{(4)}$), demonstrating an operational backreaction bridge where positive field excitation enhances lateral diamond-forming precursor branches (inducing interval-volume focusing, $S_{\rm BD}^{(4)} < 0$), while field suppression favors chain-like dispersion ($S_{\rm BD}^{(4)} > 0$).
- Establish an exact conditional-mean joint field-plus-geometry conservation ledger $\mathcal{C}(P, \rho_{\rm field}) = V_{\rm geom}(P) + \operatorname{Tr}[H_{\rm field}(P)\rho_{\rm field}]$ defined purely on finite partially ordered sets, proving that measurement-induced field dissipation is absorbed conservatively into native causal geometry without energy loss.

---

## 2. Governance, Isolation, and Quarantine Constraints

### 2.1 Strict Sibling Isolation
Observable PW5-A is subject to strict sibling isolation:
- `PW5A_PROTOCOL.md` and the deliverable `docs/observables/intrinsic_sorkin_johnston_stress_and_order_backreaction.md` MUST contain ZERO mentions, cross-links, or cross-citations to sibling Stage 4 observables, protocols, or track deliverables.
- Permitted references are strictly restricted to committed prior stage observables (`PW2-A`, `PW2-B`, `PW3-A`, `PW3-B`, `PW4-A`, `PW4-B`), master governance plans (`docs/coordination/FOUNDATIONAL_RESEARCH_SCOPE.md`, `docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md`), and tracking documents.
- Compliance will be verified by running automated string inspection confirming zero mentions or cross-citations of sibling deliverables or alternate Stage 4 tracks.

### 2.2 Strict Software Pause Affirmation
In accordance with foundational research governance (`FOUNDATIONAL_RESEARCH_SCOPE.md`):
- ZERO execution of Python, Node, `bc`, `awk`, calculator tools, or automated test runners is permitted.
- All matrix inverses, resolvents, spectral projections, commutators, rational arithmetic fractions, Kraus decompositions, Choi eigenvalues, and conservation ledgers must be derived and verified 100% by hand from first principles.
- Tool usage is strictly restricted to POSIX file operations (`cat`, `cp`, `diff`, `mv`, `printf`), cryptographic hashing (`shasum -a 256`), and version control (`git`).

### 2.3 Status-M Quarantine Affirmation
The following four ontological documents are strictly quarantined under Status-M:
1. `ONTOLOGY.md`
2. `GOVERNANCE.md`
3. `PHYSICS.md`
4. `FALSIFICATION_LEDGER.md`

These files must remain completely untouched. Every deliverable produced under this protocol must include an explicit quarantine declaration in its Line 3 Decision block and in its Scope/Non-claims section.

### 2.4 KaTeX Syntax and Formatting Rules
- Inline math expressions must strictly use `$ ... $`.
- Display math blocks must strictly use `$$ ... $$`.
- Delimiters `\( ... \)` and `\[ ... \]` are strictly prohibited.
- Inside GitHub Flavored Markdown (GFM) tables, math pipe characters must be escaped as `\lvert ... \rvert`, `\lVert ... \rVert`, `\mid`, or `\parallel` to prevent corruption of table column boundaries.

---

## 3. Mathematical Blueprint by Deliverable Section

The deliverable `docs/observables/intrinsic_sorkin_johnston_stress_and_order_backreaction.md` will be organized into nine comprehensive sections as detailed below.

### Section 0: Frontmatter & Decision Block
- Title: *Stage 4 Observable PW5-A: Intrinsic Sorkin–Johnston Stress and Order Backreaction*
- Line 3 Decision Block:
  ```markdown
  **Decision.** Coupling excitations of the intrinsic Sorkin–Johnston bosonic field algebra ($G_R(P), i\Delta(P), W_{\rm SJ}(P)$) directly into sequential causal-order growth $q(P, r, S)$ and discrete Benincasa–Dowker curvature ($S_{\rm BD}^{(2)}, S_{\rm BD}^{(4)}$) establishes an exact, Kolmogorov-projective, diamond-commuting gravitational backreaction instrument and joint conditional-mean conservation ledger completely free of any external continuum cavity box $[0, L]^3$, boundary stress collar, or background metric; Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime dimension, Born's rule, physical constants, or General Relativity.
  ```

### Section 1: Finite Poset Causal Algebra & Background-Free Sorkin–Johnston State
- **Poset Incidence Matrix**: For finite poset $P = (V, \prec)$ with $N = \lvert V\rvert \ge 1$ elements, topologically sorted such that $v \prec u \implies v < u$, define $C_P \in \{0, 1\}^{N \times N}$ by $(C_P)_{uv} = 1$ if $v \prec u$ and $0$ otherwise.
  * Strict lower triangularity: $(C_P)_{uv} = 0$ for $u \le v$.
  * Strict $k$-chain counting: $(C_P^k)_{uv}$ counts chains $v = x_0 \prec x_1 \prec \dots \prec x_k = u$.
  * Exact nilpotency: $C_P^{h(P)+1} = 0 \implies C_P^N = 0$.
- **Resolvent Retarded Green Operator**: For propagation parameter $\mu > 0$:
  $$
  G_R(P) := (I - \mu C_P)^{-1} - I = \sum_{k=1}^{N-1} \mu^k C_P^k.
  $$
  Advanced Green operator $G_A(P) := G_R(P)^T = \sum_{k=1}^{N-1} \mu^k (C_P^T)^k$.
- **Discrete Pauli–Jordan Commutator**:
  $$
  i\Delta(P) := G_R(P) - G_A(P) \in \mathbb{R}^{N \times N}, \qquad (i\Delta(P))^T = -i\Delta(P).
  $$
  Hermitian skew operator $M := \Delta(P) = -i(G_R(P) - G_A(P)) \in \mathbb{C}^{N \times N}$, with $M^\dagger = M$.
  * Discrete Microcausality Theorem: $(i\Delta(P))_{uv} = 0$ for all incomparable pairs $u \parallel v$ and for coincident points $u = v$.
- **Sorkin–Johnston Two-Point State**:
  $$
  W_{\rm SJ}(P) := \frac{1}{2}\left( \lvert M\rvert + M \right) = \sum_{\lambda_j > 0} \lambda_j v_j v_j^\dagger \succeq 0,
  $$
  where $\lvert M\rvert = \sqrt{M^2}$, $\lambda_j > 0$ are the positive eigenvalues of $M$ with normalized complex eigenvectors $v_j$, and $W_{\rm SJ} v_0 = 0$ for all $v_0 \in \ker(M) = \ker(G_R - G_A)$.
- **Order-Convex Restriction Invariance**: For any order-convex subposet $Q \subseteq P$, $(G_R(P))\vert_Q = G_R(Q)$, $(G_A(P))\vert_Q = G_A(Q)$, and $(i\Delta(P))\vert_Q = i\Delta(Q)$.

### Section 2: Local & Link Discrete Stress-Energy Observables
- **Elimination of Continuous Derivatives**: Replace $\partial_\mu \phi$ with differences along the covering relations (links) of $P$:
  $$
  \operatorname{Link}(P) := \{ (v, u) \in V \times V : v \prec u \text{ and } I(v, u) = \varnothing \} = \operatorname{supp}(A_1).
  $$
- **Discrete Link Difference Operator**: For $e = (v, u) \in \operatorname{Link}(P)$:
  $$
  D_{(v, u)}\phi := \phi(u) - \phi(v).
  $$
- **Normal-Ordered Link Stress Observable**:
  $$
  \mathcal{T}_{\rm link}(v, u) := \frac{1}{2} : \left( \phi(u) - \phi(v) \right)^2 :_{W_{\rm SJ}} = \frac{1}{2}\left( \phi(u) - \phi(v) \right)^2 - \frac{1}{2}\langle \left( \phi(u) - \phi(v) \right)^2 \rangle_{\rm SJ} \mathbf{1},
  $$
  with Sorkin–Johnston vacuum expectation:
  $$
  \langle \left( \phi(u) - \phi(v) \right)^2 \rangle_{\rm SJ} = (W_{\rm SJ})_{uu} + (W_{\rm SJ})_{vv} - (W_{\rm SJ})_{uv} - (W_{\rm SJ})_{vu}.
  $$
- **Local Site Energy Density Observable**:
  $$
  \mathcal{T}(u) := \frac{1}{2} \sum_{v: (v, u) \in \operatorname{Link}(P)} \mathcal{T}_{\rm link}(v, u) + \frac{1}{2} \sum_{w: (u, w) \in \operatorname{Link}(P)} \mathcal{T}_{\rm link}(u, w).
  $$
- **Total Discrete Field Hamiltonian**:
  $$
  H_{\rm field}(P) := \sum_{u \in V} \mathcal{T}(u) = \sum_{(v, u) \in \operatorname{Link}(P)} \mathcal{T}_{\rm link}(v, u).
  $$
  Relation to discrete graph Laplacian $L_P$: $\frac{1}{2}\sum_{(v, u) \in \operatorname{Link}(P)} (\phi(u) - \phi(v))^2 = \frac{1}{2}\phi^T L_P \phi$.

### Section 3: Sorkin–Johnston Mode Algebra & Field Excitations
- **Mode Annihilation and Creation Operators**: For each strictly positive eigenvalue $\lambda_j > 0$ of $M$:
  $$
  \hat{a}_j := \frac{1}{\sqrt{\lambda_j}} v_j^\dagger \phi, \qquad \hat{a}_j^\dagger := \frac{1}{\sqrt{\lambda_j}} \phi^T v_j,
  $$
  satisfying $[\hat{a}_j, \hat{a}_k^\dagger] = \delta_{jk}\mathbf{1}$ and $[\hat{a}_j, \hat{a}_k] = 0$.
- **Sorkin–Johnston Vacuum State**: $\hat{a}_j \lvert 0\rangle_{\rm SJ} = 0$ for all $j$ with $\lambda_j > 0$.
- **Fock Excitations**: $\lvert n_j\rangle = \frac{(\hat{a}_j^\dagger)^n}{\sqrt{n!}}\lvert 0\rangle_{\rm SJ}$ with mode number operator $\hat{N}_j = \hat{a}_j^\dagger \hat{a}_j$.
- **Coherent Excitations**: $\lvert \alpha\rangle = \exp(\sum_j (\alpha_j \hat{a}_j^\dagger - \alpha_j^* \hat{a}_j))\lvert 0\rangle_{\rm SJ}$.
  * Expectation of local field: $\langle \alpha\rvert \phi(u) \lvert \alpha\rangle = \sum_j \sqrt{\lambda_j} ((v_j)_u \alpha_j + (v_j^*)_u \alpha_j^*) \in \mathbb{R}$.
  * Expectation of normal-ordered link stress:
    $$
    \langle \alpha\rvert \mathcal{T}_{\rm link}(v, u) \lvert \alpha\rangle = \frac{1}{2}\left[ \sum_j \sqrt{\lambda_j}\left( (v_j)_u - (v_j)_v \right)\alpha_j + \text{c.c.} \right]^2 \ge 0.
    $$
    Strict non-negativity and quadratic scaling in displacement amplitudes.

### Section 4: Kolmogorov-Projective Diamond-Commuting Instrument & Growth Coupling
- **All-Horizon Sequential Growth**: For parent size $n = \lvert P\rvert \ge 4$ and proper ideal $S \subsetneq P$:
  $$
  u(P, r, S) := \prod_{\varnothing \ne A \subseteq M} q\left( P \setminus A, \, r\vert_{P \setminus A}, \, S \right)^{(-1)^{\lvert A\rvert + 1}} > 0,
  $$
  where $M = \operatorname{Max}(P) \setminus S$. Admitted scale schedule $a_n \in (0, 1/M_n)$ ensures $q(P, r, P) = 1 - a_n \sum_{S \subsetneq P} u(P, r, S) > 0$.
- **Field Observable Coupling**: Let $\mathcal{O}_{\rm field}$ be a bounded self-adjoint observable in the field algebra. Steered transition probabilities:
  $$
  p(S \mid \rho_{\rm field}) = q(P, r, S) \left( 1 + r_P(S) \operatorname{Tr}\left[ \mathcal{O}_{\rm field} \rho_{\rm field} \right] \right),
  $$
  with zero-mean drift $\sum_{S \in \mathcal{I}(P)} q(P, r, S) r_P(S) = 0$.
- **CPTP Instrument Superoperator**:
  $$
  \mathcal{B}_{S, b}^{P, r}(\rho_{\rm field}) := \frac{1}{2} q(P, r, S) \left\{ \lambda_{\lvert P\rvert} U \rho_{\rm field} U^\dagger + \frac{1}{2} \operatorname{Tr}\left[ \left( (1 - \lambda_{\lvert P\rvert})\mathbf{1} + r_P(S) \mathcal{O}_{\rm field} \right) \rho_{\rm field} \right] \mathbf{1}_{\rm local} \right\}.
  $$
- **Choi Spectrum & Complete Positivity**: Complete positivity holds if and only if $\lvert r_P(S)\rvert \le 1 - \lambda_{\lvert P\rvert}$.
- **Diamond Commutation & Kolmogorov Projectivity**: On every pair of incomparable births $(S, b)$ and $(T, c)$ on base $(C, r)$:
  $$
  \left( \mathcal{B}_{T, c}^{C+x_S, r+b_x} \circ \mathcal{B}_{S, b}^{C, r} \right) \otimes \operatorname{id}_{\rm ref} = \left( \mathcal{B}_{S, b}^{C+y_T, r+c_y} \circ \mathcal{B}_{T, c}^{C, r} \right) \otimes \operatorname{id}_{\rm ref}.
  $$

### Section 5: Discrete Benincasa–Dowker Curvature Response and Backreaction Focusing
- **Combinatorial Curvature Actions**:
  $$
  S_{\rm BD}^{(2)}(P) := N - 2N_0 + 4N_1 - 2N_2,
  $$
  $$
  S_{\rm BD}^{(4)}(P) := N - N_0 + 9N_1 - 16N_2 + 8N_3,
  $$
  where $N_k = \mathbf{1}^T A_{k+1} \mathbf{1}$ counts comparable pairs with $k$ intermediate elements.
- **Benchmark Values**:
  * Lateral diamond focusing: $S_{\rm BD}^{(4)}(E_{\text{diamond}}) = -16$.
  * Linear chain dispersion: $S_{\rm BD}^{(4)}(C_4) = +3$.
  * Disconnected antichain: $S_{\rm BD}^{(4)}(A_4) = +4$.
- **Curvature Linear Response**:
  $$
  \mathbb{E}_{\rho_{\rm field}}\left[ S_{\rm BD}^{(4)} \right] = \bar{S}_0^{(4)} + \kappa_{\rm steer}^{(4)} \langle \mathcal{O}_{\rm field} \rangle.
  $$
  Derivation showing how causal drift $r_{C_2}(\{a\}) = +1/88 > 0$ enhances diamond-forming ideals ($S_{\rm BD}^{(4)} = -16$) while suppressing unlinked antichains ($r_{C_2}(\varnothing) = -1/22 < 0$), establishing interval focusing from field energy.

### Section 6: Exact Joint Field-Plus-Geometry Conservation Ledger (Zero Box)
- **Joint Conserved Quantity**:
  $$
  \mathcal{C}(P, \rho_{\rm field}) := V_{\rm geom}(P) + \operatorname{Tr}\left[ H_{\rm field}(P) \rho_{\rm field} \right].
  $$
- **Master Linear System across Horizon Steps**:
  $$
  \text{(I)} \quad \sum_{S \in \mathcal{I}(P)} q(P, r, S) \overline{V}(P+S, r) = V(P, r),
  $$
  $$
  \text{(II)} \quad \sum_{S \in \mathcal{I}(P)} q(P, r, S) r_P(S) \overline{V}(P+S, r) = \frac{\varepsilon}{2}(1 - \lambda_{\lvert P\rvert}).
  $$
- **Single-Parent Rank Criterion & Canonical Solution**:
  $$
  \overline{V}_{\min}(P+S, r) = V(P, r) + \frac{\varepsilon(1 - \lambda_{\lvert P\rvert})}{2 \operatorname{Var}_{q}(r_P)} r_P(S).
  $$
- **Multi-Birth Globally Active Potential $H_{\rm full}$**: Defined on the 16 classes of $\mathcal{U}_4$ with coupling $\theta = 1/16$, ensuring $\operatorname{Var}_q(r_P) > 0$ on all reachable parents without reachability obstructions.
- **Purely Geometric Potential $V_{\rm geom}$**: Evaluated on all 25 posets of sizes $0 \le \lvert P\rvert \le 4$, proving mark-independence, diamond confluence, and exact absorption of measurement dissipation:
  $$
  \Delta E_{\rm field}^{\rm lost} = \frac{\varepsilon}{2}(1 - \lambda_{\lvert P\rvert})\langle \mathcal{O}_{\rm field} \rangle \iff \Delta \mathbb{E}[V_{\rm geom}] = \frac{\varepsilon}{2}(1 - \lambda_{\lvert P\rvert})\langle \mathcal{O}_{\rm field} \rangle.
  $$

### Section 7: Hand-Calculated Canonical Benchmarks

#### Benchmark Table 1: Field Incidence, Resolvent, and Sorkin–Johnston Spectrum ($\mu = 1$)

| Poset $P$ | Vertices $N$ | Height $h(P)$ | Nilpotency Index | Incomparable Pairs | $(i\Delta)_{uv}$ on $u \parallel v$ | Spectrum of $M$ ($\mu=1$) | $\dim\ker(M)$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Singleton $P_1$ | 1 | 0 | 1 ($C^1 = 0$) | 0 | Vacuous | None | 1 |
| Two-Chain $C_2$ | 2 | 1 | 2 ($C^2 = 0$) | 0 | Vacuous | $\pm 1$ | 0 |
| Two-Antichain $A_2$ | 2 | 0 | 1 ($C^1 = 0$) | 1 ($0 \parallel 1$) | $(i\Delta)_{01} = 0$ | None | 2 |
| Three-Chain $C_3$ | 3 | 2 | 3 ($C^3 = 0$) | 0 | Vacuous | $\pm\sqrt{6}$ | 1 |
| Fork $V$ | 3 | 1 | 2 ($C^2 = 0$) | 1 ($1 \parallel 2$) | $(i\Delta)_{12} = 0$ | $\pm\sqrt{2}$ | 1 |
| Diamond $E_{\text{diamond}}$ | 4 | 2 | 3 ($C^3 = 0$) | 1 ($1 \parallel 2$) | $(i\Delta)_{12} = 0$ | $\pm\sqrt{13}$ | 2 |
| Four-Chain $C_4$ | 4 | 3 | 4 ($C^4 = 0$) | 0 | Vacuous | $\pm\sqrt{20}$ | 2 |
| Four-Antichain $A_4$ | 4 | 0 | 1 ($C^1 = 0$) | 6 | 0 on all pairs | None | 4 |

#### Benchmark Table 2: Layer Cardinalities and Benincasa–Dowker Curvature Actions

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

### Section 8: Scope, Non-Implications, and Status-M Quarantine
- Reiteration of strict boundaries: no claim to derive continuum manifolds, Einstein equations, physical constants ($c, \hbar, G$), or Born's rule.
- Explicit Status-M quarantine clause naming `ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, and `FALSIFICATION_LEDGER.md`.

### Section 9: Reserved Scientific Review Placeholder
Standardized provenance footer reservation.

---

## 4. Hand-Verification Procedure & Computational Protocols

Under the Strict Software Pause, all computations must follow this deterministic, hand-executable protocol:

1. **Incidence & Resolvents**:
   - Write out $C_P$ in upper-lower triangular form according to a chosen topological sorting.
   - Compute matrix powers $C_P^2, C_P^3, \dots, C_P^{N-1}$ by row-column vector dot products.
   - Sum the terminating polynomial $G_R = \mu C_P + \mu^2 C_P^2 + \dots$ with $\mu = 1$.
   - Transpose to obtain $G_A = G_R^T$ and take difference $i\Delta = G_R - G_A$. Confirm $(i\Delta)_{uv} = 0$ for all $u \parallel v$.
2. **Spectral Analysis of $M = -i(G_R - G_A)$**:
   - Compute characteristic polynomial $\det(M - \lambda I) = 0$ using cofactor expansion.
   - Identify non-zero eigenvalue pairs $\pm \lambda_j$.
   - Solve linear systems $(M - \lambda_j I)v_j = 0$ by Gaussian elimination for normalized eigenvectors $v_j$.
   - Form outer products $v_j v_j^\dagger$ and assemble $W_{\rm SJ} = \sum_{\lambda_j > 0} \lambda_j v_j v_j^\dagger$. Verify $W_{\rm SJ} \succeq 0$.
3. **Discrete Stress Observables**:
   - Identify covering links $\operatorname{Link}(P)$ by checking which pairs $v \prec u$ have no intermediate vertices ($n(u, v) = 0$).
   - Compute vacuum link fluctuation $(W_{\rm SJ})_{uu} + (W_{\rm SJ})_{vv} - (W_{\rm SJ})_{uv} - (W_{\rm SJ})_{vu}$.
   - For coherent state $\lvert \alpha\rangle$, evaluate difference $\sum_j \sqrt{\lambda_j}((v_j)_u - (v_j)_v)\alpha_j + \text{c.c.}$ and verify non-negativity of $\mathcal{T}_{\rm link}$.
4. **Curvature Actions**:
   - Count $N_0 = \lvert \operatorname{Link}(P)\rvert$, $N_1 = \lvert \{(v, u) : n(u, v) = 1\}\rvert$, $N_2 = \lvert \{(v, u) : n(u, v) = 2\}\rvert$, $N_3 = \lvert \{(v, u) : n(u, v) = 3\}\rvert$.
   - Evaluate $S_{\rm BD}^{(2)} = N - 2N_0 + 4N_1 - 2N_2$ and $S_{\rm BD}^{(4)} = N - N_0 + 9N_1 - 16N_2 + 8N_3$.
5. **Conservation Ledger**:
   - Verify master linear equations (I) and (II) by exact rational arithmetic.
   - Confirm $\Delta E_{\rm field}^{\rm lost} = \Delta \mathbb{E}[V_{\rm geom}]$ to 0 residue.

---

## 5. Verification and Pre-Flight Audit Checklist

Before deliverable release, verify:
- [ ] Line 3 Decision block contains exact Status-M quarantine clause.
- [ ] Section 8 contains explicit non-claims and quarantine statement.
- [ ] Zero mentions, links, or cross-citations to sibling Stage 4 deliverables or alternate tracks (automated string search yields 0 matches).
- [ ] All math uses `$ ... $` and `$$ ... $$` delimiters only; zero `\(` or `\[`.
- [ ] In all GFM tables, pipe characters inside math spans are escaped as `\lvert ... \rvert`, `\lVert ... \rVert`, `\mid`, or `\parallel`.
- [ ] All calculations derived 100% by hand; zero python, node, bc, or awk execution.
- [ ] Status-M files untouched (`git diff ONTOLOGY.md GOVERNANCE.md PHYSICS.md FALSIFICATION_LEDGER.md` is empty).
- [ ] SHA-256 hash computed and frozen via `shasum -a 256 PW5A_PROTOCOL.md`.

---

## 6. Reserved Scientific Review Placeholder

```markdown
## Scientific review

Prospective protocol SHA-256 <64-hex-protocol-hash>; accepted author report SHA-256 <64-hex-author-report-hash>; independent scientific review SHA-256 <64-hex-review-report-hash>.
```
