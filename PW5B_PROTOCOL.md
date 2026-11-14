# Prospective Research Protocol PW5-B: Manifold-Compatible Growth Scaling and Dimension Stabilization

**Document ID**: `PW5B_PROTOCOL.md`  
**Author**: `teamwork_worker_m1`  
**Date**: 2026-11-14T01:28:00Z  
**Target Deliverable**: `/Volumes/AI_DATA/development/det_8_framework_gemini/docs/observables/manifold_compatible_growth_scaling_and_dimension_stabilization.md`  
**Workspace**: `/Volumes/AI_DATA/development/det_8_framework_gemini/.agents/teamwork/teamwork_worker_m1/`  
**Protocol Status**: Frozen Prospective Specification  

---

## 1. Objectives & Scientific Scope

### 1.1 Purpose and Physical Vision
This prospective protocol establishes the formal mathematical specification, derivation plan, verification procedure, and governance compliance rules for authoring **Stage 4 Observable PW5-B: Manifold-Compatible Growth Scaling and Dimension Stabilization** (`docs/observables/manifold_compatible_growth_scaling_and_dimension_stabilization.md`).

The foundational research mandate established in `docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md` (`NG-02`, `NG-03`) and `ORIGINAL_REQUEST.md` (R2) requires advancing beyond Stage 1's Asymptotic Width Dichotomy by analyzing size-dependent and sparse-link sequential growth schedules, proving exact analytical obstructions against naive growth laws, and constructing discrete generally covariant regimes that stabilize the intrinsic Myrheim–Meyer dimension to four spacetime dimensions ($d \approx 4.0$) without collapsing into non-manifold geometries.

In prior investigations:
1. Stage 1 (`PW2-A`, `PW2-B`) constructed the all-horizon sequential growth kernel $q(P, r, S) = a_n u(P, r, S)$ for $n = \lvert P\rvert \ge 4$ via the maximal-deletion potential and established an asymptotic width dichotomy: summable scale schedules ($\sum a_n M_n < \infty$) freeze almost surely into 1D ordinal chains, while fixed-parameter Bernoulli transitive percolation ($0 < p_- < p_+ < 1$) has almost surely diverging width.
2. Stage 3 (`PW4-B`) formulated coordinate-free geometric observables on finite posets: the intrinsic Myrheim–Meyer comparable-pair fraction $R_2(P) = \mathbf{1}^T C_P \mathbf{1} / \binom{N}{2}$, continuous Alexandrov comparison curve $f(d) = \frac{\Gamma(d+1)\Gamma(d/2)}{2\Gamma(3d/2)}$, continuous dimension estimator $d(R_2) = f^{-1}(R_2)$, $k$-chain abundance estimators $C_k(P) = \mathbf{1}^T C_P^k \mathbf{1}$, and discrete Benincasa–Dowker scalar curvature actions $S_{\rm BD}^{(2)}, S_{\rm BD}^{(4)}$.

**The primary objective of PW5-B is to resolve the fundamental problem of manifold-compatible causal set growth:**
- Mathematically prove four exact analytical obstructions that explain why standard growth models fail to generate manifold-like causal sets:
  1. **1D Chain Freezing**: Summable maximal-deletion schedules ($\sum a_n M_n < \infty$) freeze almost surely into an ordinal chain tail $P_{N_*} \oplus C_{N-N_*}$, causing width to remain bounded and the dimension estimator to collapse to $d(R_2) \to 1.0$.
  2. **Fixed-$p$ Transitive Percolation 1D Collapse**: In fixed-parameter transitive percolation ($p \in (0, 1)$), non-local transitive shortcuts dominate as $N \to \infty$, forcing the comparable-pair fraction $R_2(P_N) \xrightarrow{p} 1$ and collapsing the dimension estimator to $d(R_2) \xrightarrow{p} 1.0$ despite infinite width.
  3. **3-Layer Kleitman–Rothschild (KR) Collapse**: Unconstrained or uniform random poset ensembles are combinatorially dominated by 3-layer posets with height $h \le 3$, zero chains of length $k \ge 3$ ($\rho_2 = 0$), and an unphysical frozen comparable-pair fraction $R_2 \approx 3/8$.
  4. **Covariance Obstruction for Naive Size-Dependent Percolation ($p_n \to 0$)**: Attempting to prevent 1D collapse by allowing edge probabilities to decay with poset size ($p_n \to 0$) violates the scalar diamond commutation identity whenever $p_{n+1} \ne p_n$, proving that naive stage-dependent percolation destroys discrete general covariance.
- Formulate three constructive, discrete generally covariant regimes that overcome all four obstructions:
  1. **Non-Summable Maximal-Deletion Schedules ($\sum a_n M_n = \infty$)**: Proving that arbitrary scale sequences $0 < a_n < 1/M_n$ satisfy scalar diamond commutation identically, while non-summability guarantees that proper precursor ideals are chosen infinitely often almost surely, preventing 1D chain freezing. In addition, the row sum maximum $M_n = \Sigma_u(A_n)$ on antichains provides an intrinsic self-throttling mechanism that suppresses wide antichains and KR collapse.
  2. **Covariant Decaying-Coupling Classical Sequential Growth (CSG)**: Constructing an intrinsically covariant sparse-link kernel via the Rideout–Sorkin CSG family with decaying coupling constants $t_k$, bounding the expected link degree to $O(1)$ and breaking long-range transitivity without violating covariance.
  3. **Quantum-Steered Dimension Bounds and Closed-Loop Stabilization**: Coupling the sequential growth kernel via a coherent qubit instrument on carrier $\mathcal{H}_{\rm hor} = \mathbb{C}^2$ between a dense focusing kernel $q^{(+)}$ and a sparse branching kernel $q^{(-)}$, proving linear steering of the comparable-pair fraction $\mathbb{E}_\rho[R_2] = \bar{R}_2 + \frac{1}{2}\Delta R_2 \langle X\rangle$, establishing exact dimension stabilization at $d = 4.0$ ($R_2 = 1/10$) via critical coherence tuning $\langle X\rangle_*$, and demonstrating closed-loop feedback stabilization against both chain freezing and KR collapse via discrete curvature response.

---

## 2. Governance, Isolation, and Quarantine Constraints

### 2.1 Strict Sibling Isolation
Observable PW5-B is subject to strict sibling isolation:
- `PW5B_PROTOCOL.md` and the deliverable `docs/observables/manifold_compatible_growth_scaling_and_dimension_stabilization.md` MUST contain ZERO mentions, cross-links, or cross-citations to sibling Stage 4 observables, protocols, or track deliverables.
- Permitted references are strictly restricted to committed prior stage observables (`PW2-A`, `PW2-B`, `PW3-A`, `PW3-B`, `PW4-A`, `PW4-B`), master governance plans (`docs/coordination/FOUNDATIONAL_RESEARCH_SCOPE.md`, `docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md`), and tracking documents.
- Compliance will be verified by running automated string inspection confirming zero mentions or cross-citations of sibling deliverables or alternate Stage 4 tracks.

### 2.2 Strict Software Pause Affirmation
In accordance with foundational research governance (`FOUNDATIONAL_RESEARCH_SCOPE.md`):
- ZERO execution of Python, Node, `bc`, `awk`, calculator tools, or automated test runners is permitted.
- All combinatorial bounds, gamma function evaluations, rational arithmetic reductions, Borel–Cantelli probabilities, Markov inequalities, and asymptotic scaling limits must be derived and verified 100% by hand from first principles.
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

The deliverable `docs/observables/manifold_compatible_growth_scaling_and_dimension_stabilization.md` will be organized into seven comprehensive sections as detailed below.

### Section 0: Frontmatter & Decision Block
- Title: *Stage 4 Observable PW5-B: Manifold-Compatible Growth Scaling, Asymptotic Poset Geometry, and Intrinsic Dimension Stabilization*
- Line 3 Decision Block:
  ```markdown
  **Decision.** Formulating size-dependent, sparse-link, and quantum-steered sequential growth schedules beyond Stage 1's Dichotomy establishes an exact mathematical separation between non-covariant or degenerate growth regimes and discrete generally covariant, manifold-compatible regimes that stabilize the intrinsic Myrheim–Meyer dimension $d(R_2) \approx 4.0$ ($R_2 \approx 1/10$), avoid both 1D chain freezing and 3-layer Kleitman–Rothschild collapse, and preserve Kolmogorov cylinder-set projectivity across all finite and infinite horizons without external continuous spacetime embeddings; Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime geometry, Born's rule, physical constants, or General Relativity.
  ```

### Section 1: Asymptotic Poset Geometry and the Challenge of Manifoldlikeness (`NG-02` / `NG-03`)
- **Poset Incidence Representation**: For finite poset $P = (V, \prec)$ with cardinality $\lvert V\rvert = N \ge 2$, topologically sorted such that $v \prec u \implies v < u$, the incidence matrix $C_P \in \{0, 1\}^{N \times N}$ satisfies $(C_P)_{uv} = 1 \iff v \prec u$.
- **Chain Abundances & Height**:
  $$
  C_k(P) := \mathbf{1}^T C_P^k \mathbf{1} = \sum_{u=0}^{N-1} \sum_{v=0}^{N-1} (C_P^k)_{uv}, \qquad h(P) := \max\{k \ge 1 : C_k(P) > 0\}.
  $$
  Nilpotency index: $C_P^{h(P)+1} = 0 \implies C_P^N = 0$. Successive chain ratios: $\rho_k(P) = C_{k+1}(P) / C_k(P)$.
- **Intrinsic Myrheim–Meyer Comparable-Pair Fraction**:
  $$
  R_2(P) := \frac{C_1(P)}{\binom{N}{2}} = \frac{2\,\mathbf{1}^T C_P \mathbf{1}}{N(N-1)} \in [0, 1].
  $$
- **Continuum Alexandrov Comparison Function**:
  $$
  f(d) := \frac{\Gamma(d+1)\,\Gamma(d/2)}{2\,\Gamma(3d/2)}.
  $$
  Hand-derived exact rational values:
  * $f(1) = 1$
  * $f(2) = 1/2 = 0.500000$
  * $f(3) = 8/35 \approx 0.228571$
  * $f(4) = 1/10 = 0.100000$
  * $f(5) = 128/3003 \approx 0.042624$
  * $f(6) = 1/56 \approx 0.017857$
  Strict monotone decrease $f'(d) < 0$ on $[1, \infty)$ and unique continuous dimension estimator $d(R_2) = f^{-1}(R_2(P))$.
- **Discrete Benincasa–Dowker Curvature Actions**:
  $$
  S_{\rm BD}^{(2)}(P) := N - 2N_0 + 4N_1 - 2N_2,
  $$
  $$
  S_{\rm BD}^{(4)}(P) := N - N_0 + 9N_1 - 16N_2 + 8N_3,
  $$
  where $N_k$ counts comparable pairs with $k$ intervening elements ($n(u, v) = k$).

### Section 2: Exact Analytical Obstructions: Why Standard Growth Laws Fail
- **Obstruction 1: 1D Chain Freezing for Summable Maximal-Deletion Schedules ($\sum a_n M_n < \infty$)**:
  * Theorem: Under $\sum_{n=4}^\infty a_n M_n < \infty$, the first Borel–Cantelli lemma implies that the event $\{S_n \subsetneq P_n\}$ occurs only finitely often almost surely.
  * Almost-sure existence of stopping size $N_* < \infty$ such that $S_n = P_n$ for all $n \ge N_*$.
  * Freezing into ordinal chain tail: $P_N = P_{N_*} \oplus C_{N - N_*}$.
  * Bounded width: $\sup_{N \ge 1} \operatorname{width}(P_N) = \operatorname{width}(P_{N_*}) < \infty$ almost surely.
  * Dimension collapse: $R_2(P_N) = 1 - O(1/N^2) \to 1 \implies d(R_2(P_N)) \to 1.0$.
- **Obstruction 2: Fixed-$p$ Bernoulli Transitive Percolation 1D Dimension Collapse**:
  * Theorem: In Bernoulli transitive percolation with fixed edge probability $p \in (0, 1)$, for any $u < v$ with $v - u \ge 2$:
    $$
    \Pr(u \not\prec v) \le (1 - p^2)^{v - u - 1}.
    $$
  * Expected comparable-pair fraction:
    $$
    \mathbb{E}[R_2(P_N)] \ge 1 - \frac{2}{p^2 (N - 1)} \xrightarrow{N \to \infty} 1.
    $$
  * Dimension collapse in probability: $R_2(P_N) \xrightarrow{p} 1 \implies d(R_2(P_N)) \xrightarrow{p} 1.0$.
  * Coexistence of infinite width with 1D dimension collapse due to non-local transitive shortcuts.
- **Obstruction 3: 3-Layer Kleitman–Rothschild (KR) Collapse**:
  * Theorem: Uniform random posets on $N$ elements are combinatorially dominated (fraction $1 - O(1/N)$) by 3-layer posets $V = L_1 \sqcup L_2 \sqcup L_3$ with $\lvert L_1\rvert \approx N/4, \lvert L_2\rvert \approx N/2, \lvert L_3\rvert \approx N/4$.
  * Pathology: Height freezes at $h(P) \le 3$, timelike chain abundances vanish for $k \ge 3$ ($C_k = 0 \implies \rho_2 = 0$), and comparable fraction freezes at an unphysical constant $R_2 \approx 3/8 = 0.375$.
- **Obstruction 4: Covariance Obstruction for Naive Size-Dependent Percolation ($p_n \to 0$)**:
  * Theorem: For transition kernel $q_n(C, S) = p_n^{\lvert \operatorname{Max}(S)\rvert}(1 - p_n)^{n - \lvert S\rvert}$, the scalar diamond commutation identity:
    $$
    q_n(C, S)\,q_{n+1}(C + x_S, T) = q_n(C, T)\,q_{n+1}(C + y_T, S)
    $$
    holds on all ideals $S, T \in \mathcal{I}(C)$ if and only if $p_{n+1} = p_n$.
  * Proof: Ratio on base $A_n$ with $S = \varnothing$ and $T = \{v\}$ yields $\frac{p_{n+1}(1 - p_n)}{p_n(1 - p_{n+1})} = 1 \iff p_{n+1} = p_n$.
  * Analytical no-go: Naive stage-dependent edge decay breaks discrete general covariance.

### Section 3: Constructive Regimes: Manifold-Compatible Sequential Growth
- **Constructive Regime 1: Non-Summable Maximal-Deletion Schedules ($\sum a_n M_n = \infty$)**:
  * Discrete General Covariance Theorem: For *any* sequence $0 < a_n < 1/M_n$, scalar diamond commutation holds identically across all base posets $C$ of size $n - 1$:
    $$
    q(C, r, S)\,q(C + x_S, r + b_x, T) = q(C, r, T)\,q(C + y_T, r + c_y, S),
    $$
    because $\lvert C + x_S\rvert = \lvert C + y_T\rvert = n$, so scale factor $a_n$ cancels identically.
  * Evasion of Chain Freezing: Non-summability $\sum_{n=4}^\infty a_n M_n = \infty$ ensures proper precursor ideals are chosen infinitely often almost surely: $\mathbb{P}_\infty(\limsup_{n \to \infty} \{S_n \subsetneq P_n\}) = 1$.
  * Antichain Self-Throttling: The row sum maximum $M_n = \Sigma_u(A_n)$ peaks on wide antichains, dynamically reducing the capping probability $q(P, r, P)$ and suppressing KR collapse.
- **Constructive Regime 2: Covariant Decaying-Coupling CSG Schedules**:
  * Rideout–Sorkin Classical Sequential Growth (CSG) parameterized by coupling sequence $(t_k)_{k \ge 0}$.
  * Decaying couplings ($t_k = t^k / k!$ or $t_k = c\,k^{-\beta}$ with $\beta > 1$) exponentially or polynomially penalize large precursor degrees, bounding expected link degree $\mathbb{E}[\lvert\operatorname{Max}(S_n)\rvert] = O(1)$ while preserving exact covariance.
  * Breaking long-range transitivity without violating Kolmogorov prefix consistency.

### Section 4: Quantum-Steered Dimension Bounds and Closed-Loop Stabilization
- **Coherent Two-Way Growth Instrument**:
  * Carrier Hilbert space $\mathcal{H}_{\rm hor} = \mathbb{C}^2$.
  * Base kernels: dense/focusing kernel $q^{(+)}$ (higher $R_2$) and sparse/branching kernel $q^{(-)}$ (lower $R_2$).
  * Coherent Kraus operators preserving Kolmogorov cylinder-set projectivity and diamond commutation.
  * Steered structural transition law:
    $$
    \mathbb{P}_\rho(S \mid P, r) = \bar{q}(P, r, S) + \frac{1}{2}\Delta q(P, r, S)\,\langle X\rangle,
    $$
    where $\langle X\rangle = \operatorname{Tr}[X\rho] \in [-1, 1]$.
- **Quantum-Steered Dimension Bounds Theorem**:
  * Linear comparable-pair steering: $\mathbb{E}_\rho[R_2(P_N)] = \bar{R}_2(N) + \frac{1}{2}\Delta R_2(N)\,\langle X\rangle$.
  * Extremal state bounds: $R_2^{(-)}(N) \le \mathbb{E}_\rho[R_2(P_N)] \le R_2^{(+)}(N)$.
  * Inverse intrinsic dimension bounds:
    $$
    d^{(+)}(N) := f^{-1}(R_2^{(+)}(N)) \le d_{\rm eff}(\rho, N) \le f^{-1}(R_2^{(-)}(N)) =: d^{(-)}(N).
    $$
  * Exact Dimension Stabilization at $d = 4.0$: For base kernels satisfying $R_2^{(-)}(N) \le 1/10 \le R_2^{(+)}(N)$, there exists a unique target coherence:
    $$
    \langle X\rangle_* = \frac{1/10 - \bar{R}_2(N)}{\frac{1}{2}\Delta R_2(N)} = \frac{2/10 - (R_2^{(+)} + R_2^{(-)})}{R_2^{(+)} - R_2^{(-)}} \in [-1, 1]
    $$
    achieving $\mathbb{E}_{\rho_*}[R_2(P_N)] = 1/10 \implies d(R_2) = 4.0$ identically.
- **Closed-Loop Dynamical Feedback**:
  * Suppression of chain freezing: Long chains increase 1-intervals $N_1$, driving $S_{\rm BD}^{(4)} > 0$ (dispersion); back-action rotates Bloch vector toward $\langle X\rangle < 0$, enhancing sparse kernel $q^{(-)}$ and suppressing chain continuation.
  * Suppression of KR collapse: Wide antichains increase lateral links without intermediate elements, driving $S_{\rm BD}^{(4)} < 0$ (focusing); back-action rotates Bloch vector toward $\langle X\rangle > 0$, enhancing chain continuation.

### Section 5: Canonical Benchmarks and Asymptotic Scaling Verification
Comprehensive evaluation table covering canonical posets across sizes $N = 1, 2, 3, 4$ and asymptotic prototypes:
1. Singleton $P_1$ ($N=1$)
2. Two-chain $C_2$ ($N=2$)
3. Two-antichain $A_2$ ($N=2$)
4. Three-chain $C_3$ ($N=3$)
5. Fork $V$ ($N=3$)
6. Diamond $E_{\text{diamond}}$ ($N=4$)
7. Four-chain $C_4$ ($N=4$)
8. Four-antichain $A_4$ ($N=4$)
9. Crown $E_{\text{crown}}$ ($N=6$, 3 minimal, 3 maximal)
10. KR 3-layer prototype $P_{\rm KR}$ ($N=8$)

For each poset, evaluate:
- Vertex count $N$, height $h(P)$, comparable pairs $C_1$, 2-chains $C_2$, 3-chains $C_3$.
- Comparable-pair fraction $R_2(P)$ and continuous dimension estimate $d(R_2) = f^{-1}(R_2)$.
- Layer abundances $N_0, N_1, N_2, N_3$.
- Discrete Benincasa–Dowker scalar curvature actions $S_{\rm BD}^{(2)}(P)$ and $S_{\rm BD}^{(4)}(P)$.

### Section 6: Scope, Non-Claims, and Status-M Quarantine
- Reiteration of strict boundaries: no claim to derive continuous Riemannian/Lorentzian manifolds, Einstein field equations, physical constants ($c, \hbar, G$), or Born's rule.
- Explicit Status-M quarantine clause naming `ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, and `FALSIFICATION_LEDGER.md`.

### Section 7: Reserved Scientific Review Placeholder
Standardized provenance footer reservation.

---

## 4. Hand-Verification Procedure & Computational Protocols

Under the Strict Software Pause, all proofs and evaluations must follow this deterministic, hand-executable protocol:

1. **Analytical Proof of Obstructions**:
   - Verify the Borel–Cantelli summability condition for $a_n M_n$ using partial sums of rational series.
   - For transitive percolation, re-verify the conditional independence of intermediate paths $E_w$ on vertices $w \in \{u+1, \dots, v-1\}$, confirming $\Pr(u \not\prec v) \le (1 - p^2)^{v-u-1}$ and the geometric sum bound $\mathbb{E}[I(P_N)] \le N/p^2$.
   - For KR posets, compute bipartite edge densities $\lvert L_1\rvert\lvert L_3\rvert + \frac{1}{2}\lvert L_1\rvert\lvert L_2\rvert + \frac{1}{2}\lvert L_2\rvert\lvert L_3\rvert = \frac{3}{16}N^2$, giving $R_2 \approx 3/8 = 0.375$ and verifying $C_k = 0$ for $k \ge 3$.
   - For size-dependent percolation, re-evaluate ratio $\Pi_1(\varnothing, \{v\}) / \Pi_2(\{v\}, \varnothing) = \frac{p_{n+1}(1-p_n)}{p_n(1-p_{n+1})}$, confirming it equals $1$ if and only if $p_{n+1} = p_n$.
2. **Dimension Comparison Curve $f(d)$**:
   - Re-derive the exact rational reductions of $f(d) = \frac{\Gamma(d+1)\Gamma(d/2)}{2\Gamma(3d/2)}$ by hand:
     * $f(1) = \frac{1 \cdot \sqrt{\pi}}{2 \cdot (\frac{1}{2}\sqrt{\pi})} = 1$.
     * $f(2) = \frac{2 \cdot 1}{2 \cdot 2} = \frac{1}{2}$.
     * $f(3) = \frac{6 \cdot (\frac{1}{2}\sqrt{\pi})}{2 \cdot (\frac{105}{16}\sqrt{\pi})} = \frac{3}{\frac{105}{8}} = \frac{24}{105} = \frac{8}{35}$.
     * $f(4) = \frac{24 \cdot 1}{2 \cdot 120} = \frac{24}{240} = \frac{1}{10}$.
     * $f(5) = \frac{120 \cdot (\frac{3}{4}\sqrt{\pi})}{2 \cdot (\frac{135135}{128}\sqrt{\pi})} = \frac{90}{\frac{135135}{64}} = \frac{5760}{135135} = \frac{128}{3003}$.
     * $f(6) = \frac{720 \cdot 2}{2 \cdot 40320} = \frac{720}{40320} = \frac{1}{56}$.
3. **Canonical Benchmark Invariants**:
   - Write out explicit incidence matrices $C_P$ and compute powers $C_P^2, C_P^3$.
   - Count $C_1 = \mathbf{1}^T C_P \mathbf{1}$ and evaluate $R_2(P) = 2C_1 / (N(N-1))$.
   - Count layer intervals $N_0, N_1, N_2, N_3$ and compute $S_{\rm BD}^{(2)}$ and $S_{\rm BD}^{(4)}$.
   - Confirm all arithmetic by independent rational fraction reduction.

---

## 5. Canonical Benchmark Reference Table

#### Benchmark Table 1: Invariant Geometry, Dimension Estimates, and Curvature Actions

| Poset $P$ | Vertices $N$ | Height $h(P)$ | $C_1(P)$ | $C_2(P)$ | $C_3(P)$ | $R_2(P)$ | $d(R_2)$ | $S_{\rm BD}^{(2)}(P)$ | $S_{\rm BD}^{(4)}(P)$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Singleton $P_1$ | 1 | 0 | 0 | 0 | 0 | Undefined | Undefined | $1$ | $1$ |
| Two-Chain $C_2$ | 2 | 1 | 1 | 0 | 0 | $1$ | $1.000$ | $0$ | $1$ |
| Two-Antichain $A_2$ | 2 | 0 | 0 | 0 | 0 | $0$ | $\infty$ | $2$ | $2$ |
| Three-Chain $C_3$ | 3 | 2 | 3 | 1 | 0 | $1$ | $1.000$ | $3$ | $10$ |
| Fork $V$ | 3 | 1 | 2 | 0 | 0 | $\frac{2}{3}$ | $\approx 1.54$ | $-1$ | $1$ |
| Diamond $E_{\text{diamond}}$ | 4 | 2 | 5 | 2 | 0 | $\frac{5}{6}$ | $\approx 1.25$ | $-6$ | $-16$ |
| Four-Chain $C_4$ | 4 | 3 | 6 | 3 | 1 | $1$ | $1.000$ | $4$ | $3$ |
| Four-Antichain $A_4$ | 4 | 0 | 0 | 0 | 0 | $0$ | $\infty$ | $4$ | $4$ |
| Crown $E_{\text{crown}}$ | 6 | 1 | 6 | 0 | 0 | $\frac{2}{5}$ | $\approx 2.29$ | $-6$ | $6$ |
| 3-Layer KR $P_{\rm KR}$ | 8 | 2 | 11 | 4 | 0 | $\frac{11}{28}$ | $\approx 2.32$ | $-4$ | $-12$ |

*Note: In GFM tables, all math expressions inside cells strictly avoid bare pipe symbols.*

---

## 6. Verification and Pre-Flight Audit Checklist

Before deliverable release, verify:
- [ ] Line 3 Decision block contains exact Status-M quarantine clause.
- [ ] Section 6 contains explicit non-claims and quarantine statement.
- [ ] Zero mentions, links, or cross-citations to sibling Stage 4 deliverables or alternate tracks (automated string search yields 0 matches).
- [ ] All math uses `$ ... $` and `$$ ... $$` delimiters only; zero `\(` or `\[`.
- [ ] In all GFM tables, pipe characters inside math spans are escaped as `\lvert ... \rvert`, `\lVert ... \rVert`, `\mid`, or `\parallel`.
- [ ] All calculations derived 100% by hand; zero python, node, bc, or awk execution.
- [ ] Status-M files untouched (`git diff ONTOLOGY.md GOVERNANCE.md PHYSICS.md FALSIFICATION_LEDGER.md` is empty).
- [ ] SHA-256 hash computed and frozen via `shasum -a 256 PW5B_PROTOCOL.md`.

---

## 7. Reserved Scientific Review Placeholder

```markdown
## Scientific review

Prospective protocol SHA-256 <64-hex-protocol-hash>; accepted author report SHA-256 <64-hex-author-report-hash>; independent scientific review SHA-256 <64-hex-review-report-hash>.
```
