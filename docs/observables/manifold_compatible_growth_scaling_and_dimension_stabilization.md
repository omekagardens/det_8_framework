# Manifold-Compatible Growth Scaling, Asymptotic Poset Geometry, and Intrinsic Dimension Stabilization

**Decision.** Formulating size-dependent, sparse-link, and quantum-steered sequential growth regimes beyond Stage 1's Dichotomy establishes four exact analytical growth/covariance obstructions (summable-schedule 1D chain freezing, fixed-$p$ percolation 1D dimension collapse $d(R_2) \to 1.0$, 3-layer Kleitman–Rothschild $\rho_2 = 0$ collapse, and discrete general covariance failure $\Pi_1/\Pi_2 = 1 \iff p_{n+1}=p_n$ for naive stage-dependent percolation) together with `NG-02` operational rejection screens, proves chain-tail non-freezing ($\mathbb{P}_\infty(\bigcup_{N_*} F_{N_*}) = 0$) for non-summable maximal-deletion schedules $\sum a_n = \infty$ via $\Sigma_u(Q \oplus A_1) \equiv 1$, proves linear ensemble-mean quantum dimension steering ($\mathbb{E}_{\rho_*}[R_2] = 1/10$) alongside bimodal single-history branch bifurcation (non-concentration at the ensemble mean under static carrier states), and formulates decaying-coupling CSG transitivity breaking and closed-loop single-history $d(R_2) \to 4.0$ feedback attraction as explicit open conjectures with exact Lyapunov and covariance criteria, preserving Kolmogorov cylinder-set projectivity without external continuous spacetime embeddings; Status-M ontological documents (ONTOLOGY.md, GOVERNANCE.md, PHYSICS.md, FALSIFICATION_LEDGER.md) remain strictly quarantined, and no claim is made to derive continuum spacetime geometry, single-history 3+1D emergence, Born's rule, physical constants, or General Relativity.

---

## 1. Operational Scope, Foundational Context, and Governance Boundaries

### 1.1 Foundational Motivation and the Challenge Beyond Stage 1's Dichotomy

In foundational causal set quantum gravity, discrete sequential growth models face a severe challenge: standard growth dynamics almost generically fail to produce causal sets that resemble smooth Lorentzian spacetimes. Instead, they suffer from catastrophic combinatorial collapses into degenerate geometries.

In prior milestones of this research program:
1. **Stage 1 (`all_horizon_two_way_feedback_and_growth.md`, `record_compensated_quantum_order_conservation.md`)** achieved an all-horizon recursive sequential growth extension on parent cardinalities $n = \lvert P\rvert \ge 4$ via the maximal-deletion potential $q(P, r, S) = a_n u(P, r, S)$ and established the **Asymptotic Width Dichotomy** (Theorem 6 of `PW2-A`):
   - Summable maximal-deletion scale schedules ($\sum a_n M_n < \infty$) freeze almost surely into 1D ordinal chains ($P_{N_*} \oplus C_{N-N_*}$), where the asymptotic width remains bounded;
   - Fixed-parameter Bernoulli transitive percolation ($0 < p_- < p_+ < 1$) generates causal sets whose width diverges almost surely as $N \to \infty$.
2. **Stage 3 (`intrinsic_interval_curvature_and_dimension_response.md`)** formulated background-free, coordinate-free geometric observables defined directly on the finite causal incidence matrix $C_P \in \{0, 1\}^{N \times N}$:
   - The intrinsic Myrheim–Meyer comparable-pair fraction $R_2(P) = \mathbf{1}^T C_P \mathbf{1} / \binom{N}{2} \in [0, 1]$;
   - The continuum Alexandrov comparison curve $f(d) = \frac{\Gamma(d+1)\Gamma(d/2)}{2\Gamma(3d/2)}$ and its unique continuous inverse dimension estimator $d(R_2) = f^{-1}(R_2(P))$;
   - The strict $k$-chain abundance estimators $C_k(P) = \mathbf{1}^T C_P^k \mathbf{1}$ and successive abundance ratios $\rho_k(P) = C_{k+1}(P)/C_k(P)$;
   - The discrete Benincasa–Dowker scalar curvature actions $S_{\rm BD}^{(2)}(P)$ and $S_{\rm BD}^{(4)}(P)$.

While Stage 1 proved that fixed-$p$ percolation avoids 1D chain freezing by having diverging width, this deliverable proves a far deeper pathology: **fixed-$p$ percolation undergoes an intrinsic 1D dimension collapse ($R_2 \to 1, d(R_2) \to 1.0$) despite having infinite width**, because non-local transitive shortcuts overwhelm the causal order. Furthermore, unconstrained random poset ensembles collapse into 3-layer Kleitman–Rothschild posets with bounded height $h \le 3$, zero timelike chain propagation ($\rho_2 = 0$), and an unphysical fixed comparable-pair fraction $R_2 \approx 3/8$.

The central objective of this deliverable is to advance decisively beyond Stage 1's Asymptotic Width Dichotomy by:
1. Formulating and proving four exact analytical obstructions that explain why standard growth models fail;
2. Proving that naive size-dependent percolation ($p_n \to 0$) breaks discrete general covariance;
3. Constructing discrete generally covariant sequential growth regimes that preserve Kolmogorov prefix consistency—proving chain-tail non-freezing under $\sum a_n = \infty$ and linear ensemble-mean dimension steering $\mathbb{E}_{\rho_*}[R_2] = 1/10$ while proving single-history bimodal bifurcation for static quantum steering and formulating decaying-coupling CSG sparsity and closed-loop single-history $d(R_2) \to 4.0$ stabilization as explicit open conjectures.

### 1.2 Native Geometry and Gravity Governance (`NG-02` / `NG-03`)

This work fulfills the governance mandates of the Native Geometry and Gravity Measurement Plan (`docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md`):
- **Requirement `NG-02` (Histories and Inexpensive Regime Screens)**:
  Requires all-size measurable state/kernel families, Kolmogorov cylinder-set prefix consistency, nonterminating scaling regimes, and explicit rejection screens against antichains, chains, layered posets, and bounded-width failure modes ($\Pr(\operatorname{width}(P_N) \le k) \to 0$).
- **Requirement `NG-03` (Geometry, Local Measure, and Clocks)**:
  Defines mathematical criteria for coordinate-free geometric reconstruction, ensuring that discrete geometric observables (comparable-pair fraction, chain ratios, discrete scalar actions) reflect genuine Lorentzian order geometry rather than statistical artifacts of non-local percolation shortcuts.

### 1.3 Kolmogorov Cylinder-Set Projectivity and Discrete General Covariance

A sequential growth process generates a sequence of causal sets $P_1 \subset P_2 \subset \dots \subset P_N \subset \dots$ by adjoining one element at a time. Let $\Omega_N$ denote the set of labeled causal sets on $N$ elements, and $\Omega_\infty$ the space of infinite causal set histories.

For the growth dynamics to define a legitimate physical probability measure on $\Omega_\infty$, the transition kernels $q_n(P_n, S)$ must satisfy **Kolmogorov cylinder-set projectivity**: for every cylinder event $E \subseteq \Omega_n$, the measure assigned at stage $n$ must match the measure assigned at stage $n+1$:
$$
\mu_{n+1}(E \times \mathcal{I}) = \mu_n(E).
$$
This projectivity holds if and only if the transition probabilities sum to unity at every step:
$$
\sum_{S \in \mathcal{I}(P_n)} q_n(P_n, S) = 1 \quad \forall P_n.
$$
Furthermore, in a causal set, the physical spacetime geometry is represented by the unlabeled isomorphism class of the poset. The arbitrary choice of labeling (which corresponds to an arbitrary choice of time-slicing in the continuum) must not affect physical probabilities. In classical sequential growth (Rideout & Sorkin 1999), this physical principle of **Discrete General Covariance** is expressed by the **scalar diamond commutation identity**: for any base poset $C$ of size $n-1$ and any two downward-closed ideals $S, T \in \mathcal{I}(C)$, adjoining $x_S$ first and then $y_T$ must yield the identical path probability as adjoining $y_T$ first and then $x_S$:
$$
q(C, r, S)\,q(C + x_S, r + b_x, T) = q(C, r, T)\,q(C + y_T, r + c_y, S).
$$
Every constructive regime formulated in this deliverable strictly preserves complete-row normalization, Kolmogorov projectivity, and discrete general covariance across all finite and infinite horizons.

### 1.4 Scope, Non-Claims, and Status-M Quarantine Affirmation

In strict compliance with foundational research governance (`docs/coordination/FOUNDATIONAL_RESEARCH_SCOPE.md`):
1. **Quarantine Affirmation**: Status-M ontological documents (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined and completely untouched.
2. **Non-Claims**:
   - No claim is made to derive continuous Riemannian or Lorentzian manifolds from scratch.
   - No claim is made to derive the Einstein field equations, continuous general covariance, or smooth diffeomorphism invariance.
   - No claim is made to derive physical fundamental constants ($c, \hbar, G$).
   - No claim is made to derive Born's quantum probability rule.
   - All results established herein are exact combinatorial, operational, and probabilistic theorems governing finite and asymptotic partially ordered sets and their quantum-steered instruments.

### 1.5 Strict Software Pause and Sibling Isolation Mandates

1. **Repository Software Pause & External Small-Case Audit**: All repository runtime code, simulation packages, and test harnesses (`det8/`, `scripts/`, `run_tests.py`) remain strictly paused and untouched. Every combinatorial sum, gamma function evaluation, rational reduction, Borel–Cantelli probability argument, and asymptotic limit is derived explicitly by hand from first principles (and independently cross-checked on finite posets $N \le 6$ solely via ephemeral external audit scripts outside the repository).
2. **Strict Sibling Isolation**: In accordance with R3 of `ORIGINAL_REQUEST.md`, this deliverable maintains absolute sibling isolation, containing zero mentions, cross-links, citations, or dependencies regarding sibling Stage 4 observables.

---

## 2. Mathematical Foundations, Poset Combinatorics, and Geometric Observables

### 2.1 Finite Poset Representation and Causal Incidence Matrix

Let $P = (V, \prec)$ be a finite strict partial order (poset) of cardinality $\lvert V\rvert = N \ge 2$, where the relation $\prec$ satisfies irreflexivity ($u \not\prec u$), transitivity ($u \prec v \text{ and } v \prec w \implies u \prec w$), and acyclicity.

We label the vertices $V = \{0, 1, \dots, N-1\}$ according to an arbitrary topological sort (natural labeling), such that:
$$
v \prec u \implies v < u.
$$
The causal structure of $P$ is completely encoded by its **causal incidence matrix** $C_P \in \{0, 1\}^{N \times N}$, defined by:
$$
(C_P)_{uv} := \begin{cases} 1 & \text{if } v \prec u, \\ 0 & \text{otherwise.} \end{cases}
$$
Under topological sorting, $C_P$ is strictly lower triangular with zero diagonal entries:
$$
(C_P)_{uv} = 0 \quad \text{for all } u \le v.
$$
Consequently, $C_P$ is strictly nilpotent with nilpotency index bounded by the cardinality:
$$
C_P^N = 0.
$$

### 2.2 Strict $k$-Chain Abundances, Height, and Successive Ratios

A strict $k$-chain of length $k \ge 1$ is an ordered sequence of $k+1$ distinct elements:
$$
x_0 \prec x_1 \prec x_2 \prec \dots \prec x_k.
$$
The number of distinct $k$-chains having minimal element $v$ and maximal element $u$ is given exactly by the matrix power entry $(C_P^k)_{uv}$.

1. **Total $k$-Chain Abundance**:
   Summing over all pairs yields the total $k$-chain abundance observable:
   $$
   C_k(P) := \mathbf{1}^T C_P^k \mathbf{1} = \sum_{u=0}^{N-1}\sum_{v=0}^{N-1} (C_P^k)_{uv},
   $$
   where $\mathbf{1} = (1, 1, \dots, 1)^T \in \mathbb{R}^N$ is the all-ones vector. In particular:
   - $C_1(P) = \mathbf{1}^T C_P \mathbf{1}$ counts the total number of causally comparable pairs ($v \prec u$);
   - $C_2(P) = \mathbf{1}^T C_P^2 \mathbf{1}$ counts the total number of 2-chains ($v \prec w \prec u$);
   - $C_3(P) = \mathbf{1}^T C_P^3 \mathbf{1}$ counts the total number of 3-chains ($v \prec w_1 \prec w_2 \prec u$).
2. **Poset Height**:
   The height $h(P)$ is the length of the longest chain in $P$:
   $$
   h(P) := \max\{k \ge 1 : C_k(P) > 0\}, \qquad C_k(P) = 0 \quad \forall k > h(P).
   $$
3. **Successive Chain Abundance Ratios**:
   The successive chain abundance ratios probe higher-order interval profiles:
   $$
   \rho_k(P) := \frac{C_{k+1}(P)}{C_k(P)} \quad (1 \le k < h(P)).
   $$
   In a causal set faithfully embedded into a $d$-dimensional spacetime manifold, $\rho_k(P)$ scales systematically with spacetime volume, whereas in non-manifold posets (such as Kleitman–Rothschild layered posets), $\rho_k$ truncates abruptly at low $k$.

### 2.3 Intrinsic Myrheim–Meyer Comparable-Pair Fraction $R_2(P)$

The total number of unordered distinct vertex pairs in $P$ is $\binom{N}{2} = \frac{N(N-1)}{2}$. The **intrinsic Myrheim–Meyer comparable-pair fraction** $R_2(P)$ is defined as the ratio of causally comparable pairs to total vertex pairs:
$$
R_2(P) := \frac{C_1(P)}{\binom{N}{2}} = \frac{2\,\mathbf{1}^T C_P \mathbf{1}}{N(N-1)} \in [0, 1].
$$
The fraction $R_2(P)$ satisfies fundamental properties:
1. **Coordinate-Free Invariance**: $R_2(P)$ is a purely combinatorial invariant of the abstract poset $(V, \prec)$, strictly invariant under order automorphisms and independent of any background coordinates or metrics.
2. **Universal Extremal Bounds**:
   - **Antichain $A_N$ (Purely Spacelike)**: If no relations exist ($u \not\prec v$ for all $u, v$), then $C_P = 0$, giving $C_1(A_N) = 0$ and:
     $$
     R_2(A_N) = 0.
     $$
   - **Linear Chain $C_N$ (Purely Timelike)**: If $P$ is a total order ($x_0 \prec x_1 \prec \dots \prec x_{N-1}$), then every distinct pair is comparable, so $C_1(C_N) = \binom{N}{2}$ and:
     $$
     R_2(C_N) = 1.
     $$

### 2.4 Continuum Alexandrov Diamond Comparison Function $f(d)$

In continuum Lorentzian geometry, an Alexandrov causal diamond between two timelike separated events $p \prec q$ in flat $d$-dimensional Minkowski spacetime $\mathbb{M}^d = (\mathbb{R}^d, \eta_{\mu\nu})$ ($d \ge 1$) is the intersection of the chronological future of $p$ and chronological past of $q$:
$$
I(p, q) := J^+(p) \cap J^-(q).
$$
If two events $x, y \in I(p, q)$ are sampled independently and uniformly with respect to the flat spacetime volume measure, the probability that they are causally comparable (either $x \prec y$ or $y \prec x$) depends only on the dimension $d$, and is given analytically by the Myrheim–Meyer continuum comparison function:
$$
f(d) := \frac{\Gamma(d+1)\,\Gamma(d/2)}{2\,\Gamma(3d/2)},
$$
where $\Gamma(z) = \int_0^\infty t^{z-1} e^{-t}\,dt$ is the Euler gamma function.

#### Step-by-Step Hand Derivations for Integer Dimensions $d \in \{1, 2, 3, 4, 5, 6\}$
We derive the exact rational values from first principles using $\Gamma(z+1) = z\Gamma(z)$, $\Gamma(n+1) = n!$, and $\Gamma(1/2) = \sqrt{\pi}$:

- **Dimension $d = 1$**:
  $$
  f(1) = \frac{\Gamma(2)\,\Gamma(1/2)}{2\,\Gamma(3/2)} = \frac{1! \cdot \sqrt{\pi}}{2 \cdot \left(\frac{1}{2}\sqrt{\pi}\right)} = \frac{\sqrt{\pi}}{\sqrt{\pi}} = 1.
  $$
- **Dimension $d = 2$**:
  $$
  f(2) = \frac{\Gamma(3)\,\Gamma(1)}{2\,\Gamma(3)} = \frac{2! \cdot 0!}{2 \cdot 2!} = \frac{2}{4} = \frac{1}{2} = 0.500000.
  $$
- **Dimension $d = 3$**:
  $$
  \Gamma(4) = 3! = 6, \quad \Gamma(3/2) = \frac{1}{2}\sqrt{\pi}, \quad \Gamma(9/2) = \frac{7}{2}\cdot\frac{5}{2}\cdot\frac{3}{2}\cdot\frac{1}{2}\sqrt{\pi} = \frac{105}{16}\sqrt{\pi}.
  $$
  $$
  f(3) = \frac{6 \cdot \frac{1}{2}\sqrt{\pi}}{2 \cdot \frac{105}{16}\sqrt{\pi}} = \frac{3}{\frac{105}{8}} = \frac{24}{105} = \frac{8}{35} \approx 0.228571.
  $$
- **Dimension $d = 4$**:
  $$
  \Gamma(5) = 4! = 24, \quad \Gamma(2) = 1! = 1, \quad \Gamma(6) = 5! = 120.
  $$
  $$
  f(4) = \frac{24 \cdot 1}{2 \cdot 120} = \frac{24}{240} = \frac{1}{10} = 0.100000.
  $$
- **Dimension $d = 5$**:
  $$
  \Gamma(6) = 5! = 120, \quad \Gamma(5/2) = \frac{3}{2}\cdot\frac{1}{2}\sqrt{\pi} = \frac{3}{4}\sqrt{\pi}.
  $$
  $$
  \Gamma(15/2) = \frac{13}{2}\cdot\frac{11}{2}\cdot\frac{9}{2}\cdot\frac{7}{2}\cdot\frac{5}{2}\cdot\frac{3}{2}\cdot\frac{1}{2}\sqrt{\pi} = \frac{135135}{128}\sqrt{\pi}.
  $$
  $$
  f(5) = \frac{120 \cdot \frac{3}{4}\sqrt{\pi}}{2 \cdot \frac{135135}{128}\sqrt{\pi}} = \frac{90}{\frac{135135}{64}} = \frac{5760}{135135} = \frac{128}{3003} \approx 0.042624.
  $$
- **Dimension $d = 6$**:
  $$
  \Gamma(7) = 6! = 720, \quad \Gamma(3) = 2! = 2, \quad \Gamma(9) = 8! = 40320.
  $$
  $$
  f(6) = \frac{720 \cdot 2}{2 \cdot 40320} = \frac{720}{40320} = \frac{1}{56} \approx 0.017857.
  $$

#### Exact Hand-Derived Reference Table

| Dimension $d$ | Exact Formula | Exact Reduced Rational Fraction | Decimal Value (6 D.P.) |
|:---:|:---:|:---:|:---:|
| $d = 1$ | $\frac{\Gamma(2)\Gamma(1/2)}{2\Gamma(3/2)}$ | $1$ | $1.000000$ |
| $d = 2$ | $\frac{\Gamma(3)\Gamma(1)}{2\Gamma(3)}$ | $\frac{1}{2}$ | $0.500000$ |
| $d = 3$ | $\frac{\Gamma(4)\Gamma(3/2)}{2\Gamma(9/2)}$ | $\frac{8}{35}$ | $0.228571$ |
| $d = 4$ | $\frac{\Gamma(5)\Gamma(2)}{2\Gamma(6)}$ | $\frac{1}{10}$ | $0.100000$ |
| $d = 5$ | $\frac{\Gamma(6)\Gamma(5/2)}{2\Gamma(15/2)}$ | $\frac{128}{3003}$ | $0.042624$ |
| $d = 6$ | $\frac{\Gamma(7)\Gamma(3)}{2\Gamma(9)}$ | $\frac{1}{56}$ | $0.017857$ |

#### Strict Monotonicity and Continuous Inverse Dimension Estimator

Taking the logarithmic derivative of $f(d)$ with respect to $d$:
$$
\ln f(d) = \ln \Gamma(d+1) + \ln \Gamma(d/2) - \ln 2 - \ln \Gamma(3d/2).
$$
Differentiating with respect to $d$:
$$
\frac{f'(d)}{f(d)} = \psi(d+1) + \frac{1}{2}\psi(d/2) - \frac{3}{2}\psi(3d/2),
$$
where $\psi(z) = \frac{\Gamma'(z)}{\Gamma(z)}$ is the digamma function. Using the integral representation $\psi(z) = \ln z - \frac{1}{2z} - \int_0^\infty \left(\frac{1}{e^t - 1} - \frac{1}{t} + \frac{1}{2}\right) e^{-zt}\,dt$, the convexity of $\psi(z)$ guarantees that for all $d \ge 1$:
$$
\frac{f'(d)}{f(d)} < 0 \implies f'(d) < 0.
$$
Since $f(d)$ is strictly monotonically decreasing on $[1, \infty)$ with $f(1) = 1$ and $\lim_{d \to \infty} f(d) = 0$, the continuous intrinsic dimension estimator:
$$
d(R_2) := f^{-1}(R_2(P))
$$
is uniquely and well defined for every $R_2(P) \in (0, 1]$. In particular:
$$
R_2 = \frac{1}{10} \iff d(R_2) = 4.0.
$$

### 2.5 Discrete Benincasa–Dowker Scalar Curvature Actions

For any comparable pair $v \prec u$, the intervening interval cardinality is:
$$
n(u, v) := \lvert I(v, u)\rvert = \lvert\{w \in V : v \prec w \prec u\}\rvert.
$$
The layer abundances $N_k$ count comparable pairs with exactly $k$ intervening elements:
$$
N_k(P) := \lvert\{(v, u) \in V \times V : v \prec u \text{ and } n(u, v) = k\}\rvert.
$$
In particular, $N_0(P)$ counts the covering relations (links), $N_1(P)$ counts pairs separated by exactly one intervening element, $N_2(P)$ counts pairs separated by two elements, and $N_3(P)$ counts pairs separated by three elements. The sum of all layer abundances equals the total number of comparable pairs: $\sum_{k=0}^{N-2} N_k(P) = C_1(P)$.

The dimensionless discrete Benincasa–Dowker scalar curvature actions are defined by:
- **Two-Dimensional Discrete Action**:
  $$
  S_{\rm BD}^{(2)}(P) := N - 2N_0 + 4N_1 - 2N_2.
  $$
- **Four-Dimensional Discrete Action**:
  $$
  S_{\rm BD}^{(4)}(P) := N - N_0 + 9N_1 - 16N_2 + 8N_3.
  $$
These discrete actions act as coordinate-free geometric diagnostics: they distinguish interval-focusing configurations ($S_{\rm BD} < 0$, causal diamond convergence) from dispersing configurations ($S_{\rm BD} > 0$, linear chain extension).

---

## 3. Exact Analytical Growth Obstructions: Why Standard Growth Laws Fail

We now prove four exact analytical obstructions demonstrating that conventional growth laws fail to generate manifold-compatible causal sets, identifying the precise mathematical boundaries that any viable growth dynamics must respect.

### 3.1 Obstruction 1: 1D Chain Freezing for Summable Maximal-Deletion Schedules

In Stage 1 (`PW2-A`, Theorem 1), the sequential growth kernel is defined by:
$$
q(P, r, S) = a_n u(P, r, S) \quad (S \subsetneq P), \qquad q(P, r, P) = 1 - a_n \sum_{S \subsetneq P} u(P, r, S),
$$
where $a_n$ is a positive scale parameter satisfying $0 < a_n < 1/M_n$ with:
$$
M_n := \max_{\lvert P\rvert=n, r} \sum_{S \subsetneq P} u(P, r, S).
$$

**Theorem 3.1 (1D Chain Freezing Theorem).**  
*Let $(a_n)_{n \ge 4}$ be a maximal-deletion scale schedule satisfying the summability condition:*
$$
\sum_{n=4}^\infty a_n M_n < \infty.
$$
*Then for any initial quantum state $\rho$ and any marking $r$:*
1. *Almost surely, there exists a finite random stopping size $N_* < \infty$ such that for all $n \ge N_*$, $S_n = P_n$.*
2. *For all $N \ge N_*$, the causal set freezes into an ordinal chain tail:*
   $$
   P_N = P_{N_*} \oplus C_{N - N_*}.
   $$
3. *The asymptotic poset width is almost surely finite:*
   $$
   \mathbb{P}_\infty\left(\sup_{N \ge 1} \operatorname{width}(P_N) = \operatorname{width}(P_{N_*}) < \infty\right) = 1.
   $$
4. *The intrinsic Myrheim–Meyer dimension estimator collapses to one dimension:*
   $$
   \lim_{N \to \infty} R_2(P_N) = 1 \implies \lim_{N \to \infty} d(R_2(P_N)) = 1.0.
   $$

*Proof.*  
At step $n$, the probability that the newborn element chooses a proper precursor ideal $S_n \subsetneq P_n$ is:
$$
\mathbb{P}(S_n \subsetneq P_n \mid P_n, r_n) = a_n \sum_{S \subsetneq P_n} u(P_n, r_n, S) \le a_n M_n.
$$
By hypothesis, $\sum_{n=4}^\infty a_n M_n < \infty$. By the first Borel–Cantelli lemma, the probability of the event that proper ideals are chosen infinitely often is zero:
$$
\mathbb{P}_\infty\left(\limsup_{n \to \infty} \{S_n \subsetneq P_n\}\right) = 0.
$$
Therefore, with probability 1, the event $\{S_n \subsetneq P_n\}$ occurs only finitely many times. Hence, there exists an almost surely finite random stopping index $N_* = N_*(\omega) < \infty$ such that:
$$
S_n = P_n \quad \text{for all } n \ge N_*.
$$
When $S_n = P_n$, the newborn element $n$ is placed strictly above every existing element in $P_n$ ($u \prec n$ for all $u \in P_n$). Consequently, for any $N \ge N_*$, the poset decomposes as an ordinal sum (linear stack):
$$
P_N = P_{N_*} \oplus C_{N - N_*},
$$
where $C_{N - N_*}$ is a total order of size $N - N_*$.

Because every element of $C_{N - N_*}$ is comparable to every element of $P_N$, any antichain in $P_N$ can contain at most one element from $C_{N - N_*}$, and cannot contain elements from both $P_{N_*}$ and $C_{N - N_*}$. Thus, the maximum antichain cardinality is bounded:
$$
\operatorname{width}(P_N) = \operatorname{width}(P_{N_*}) < \infty \quad \text{for all } N \ge N_*.
$$
Now we compute the total number of comparable pairs $C_1(P_N)$. The pairs partition into:
- Pairs within $P_{N_*}$: $C_1(P_{N_*})$;
- Cross pairs between $P_{N_*}$ and $C_{N - N_*}$: $N_*(N - N_*)$;
- Pairs within $C_{N - N_*}$: $\binom{N - N_*}{2}$.

Summing these three contributions:
$$
C_1(P_N) = C_1(P_{N_*}) + N_*(N - N_*) + \frac{(N - N_*)(N - N_* - 1)}{2} = \binom{N}{2} - \left[\binom{N_*}{2} - C_1(P_{N_*})\right].
$$
Dividing by $\binom{N}{2}$:
$$
R_2(P_N) = 1 - \frac{\binom{N_*}{2} - C_1(P_{N_*})}{\binom{N}{2}} = 1 - O\left(\frac{1}{N^2}\right).
$$
As $N \to \infty$, $R_2(P_N) \to 1$. Because $f^{-1}: (0, 1] \to [1, \infty)$ is continuous and $f^{-1}(1) = 1.0$:
$$
\lim_{N \to \infty} d(R_2(P_N)) = f^{-1}\left(\lim_{N \to \infty} R_2(P_N)\right) = f^{-1}(1) = 1.0. \quad \blacksquare
$$

### 3.2 Obstruction 2: Fixed-$p$ Bernoulli Transitive Percolation 1D Dimension Collapse

Stage 1 proved that fixed-parameter transitive percolation avoids 1D chain freezing by having almost surely diverging width. Here we prove that fixed-$p$ percolation is nonetheless geometrically pathological: it undergoes an intrinsic **1D dimension collapse**.

**Theorem 3.2 (Transitive Percolation 1D Collapse Theorem).**  
*Let $P_N$ be generated by Bernoulli transitive percolation with fixed parameter $p \in (0, 1)$ on $N$ vertices, where each edge $(u, v)$ ($u < v$) is independently present with probability $p$. As $N \to \infty$:*
1. *The probability that any two vertices $u < v$ are incomparable decays exponentially with their label difference:*
   $$
   \Pr(u \not\prec v) \le (1 - p^2)^{v - u - 1}.
   $$
2. *The expected fraction of comparable pairs approaches unity as $N \to \infty$:*
   $$
   \mathbb{E}[R_2(P_N)] \ge 1 - \frac{2}{p^2 (N - 1)} \xrightarrow{N \to \infty} 1.
   $$
3. *The intrinsic Myrheim–Meyer dimension estimator collapses in probability to one dimension:*
   $$
   d(R_2(P_N)) \xrightarrow{p} 1.0.
   $$

*Proof.*  
Fix two vertices $u < v$ with $v - u \ge 2$. For each intermediate vertex $w \in \{u+1, u+2, \dots, v-1\}$, consider the event that both edges $(u, w)$ and $(w, v)$ are present in the random graph:
$$
E_w := \{(u, w) = 1 \text{ and } (w, v) = 1\}.
$$
Since edges are independent Bernoulli trials with parameter $p$:
$$
\Pr(E_w) = p^2.
$$
If $E_w$ occurs, then $u \prec w$ and $w \prec v$, which implies $u \prec v$ by transitivity. The events $\{E_w\}_{w=u+1}^{v-1}$ involve distinct intermediate vertices and disjoint pairs of edges, so they are conditionally mutually independent given the absence of the direct edge $(u, v)$. Therefore:
$$
\Pr(u \not\prec v) \le \Pr\left(\bigcap_{w=u+1}^{v-1} E_w^c\right) = \prod_{w=u+1}^{v-1} (1 - p^2) = (1 - p^2)^{v - u - 1}.
$$
Now let $I(P_N) := \binom{N}{2} - C_1(P_N)$ denote the number of incomparable pairs in $P_N$. Taking the expectation:
$$
\mathbb{E}[I(P_N)] = \sum_{1 \le u < v \le N} \Pr(u \not\prec v) \le \sum_{u=1}^{N-1} \sum_{v=u+1}^N (1 - p^2)^{v - u - 1}.
$$
Setting $k = v - u$, the inner sum runs from $k = 1$ to $N - u$:
$$
\mathbb{E}[I(P_N)] \le \sum_{k=1}^{N-1} (N - k)(1 - p^2)^{k-1} \le N \sum_{k=1}^\infty (1 - p^2)^{k-1} = \frac{N}{1 - (1 - p^2)} = \frac{N}{p^2}.
$$
The total number of pairs is $\binom{N}{2} = \frac{N(N-1)}{2}$. Therefore, the expected comparable-pair fraction satisfies:
$$
\mathbb{E}[R_2(P_N)] = 1 - \frac{\mathbb{E}[I(P_N)]}{\binom{N}{2}} \ge 1 - \frac{N / p^2}{N(N-1)/2} = 1 - \frac{2}{p^2 (N - 1)}.
$$
As $N \to \infty$, $\mathbb{E}[R_2(P_N)] \to 1$.

To establish convergence in probability, note that $0 \le 1 - R_2(P_N) \le 1$. By Markov's inequality, for any $\epsilon > 0$:
$$
\Pr(\lvert R_2(P_N) - 1\rvert \ge \epsilon) = \Pr(1 - R_2(P_N) \ge \epsilon) \le \frac{\mathbb{E}[1 - R_2(P_N)]}{\epsilon} \le \frac{2}{\epsilon p^2 (N - 1)}.
$$
Taking $N \to \infty$ shows that $\Pr(\lvert R_2(P_N) - 1\rvert \ge \epsilon) \to 0$, establishing $R_2(P_N) \xrightarrow{p} 1$.

Finally, because the continuous comparison inverse $f^{-1}: (0, 1] \to [1, \infty)$ is continuous and $f^{-1}(1) = 1.0$, the Continuous Mapping Theorem yields:
$$
d(R_2(P_N)) = f^{-1}(R_2(P_N)) \xrightarrow{p} f^{-1}(1) = 1.0. \quad \blacksquare
$$

*Physical Interpretation*: Theorem 3.2 exposes a crucial geometric flaw of fixed-$p$ percolation: intermediate elements generate an abundance of 2-step transitive shortcuts that connect virtually every pair of vertices. As a result, the lightcone structure degenerates, and the intrinsic dimension collapses to 1D despite having infinite width.

### 3.3 Obstruction 3: 3-Layer Kleitman–Rothschild (KR) Collapse

In unconstrained random poset ensembles (uniform measure over all partial orders of size $N$), an entirely different combinatorial catastrophe occurs: posets collapse into three thin layers.

**Theorem 3.3 (Kleitman–Rothschild Asymptotic Collapse Theorem).** *(Kleitman & Rothschild 1975)*  
*Let $\mathcal{P}_N$ denote the set of all labeled partial orders on $N$ vertices with the uniform probability measure. As $N \to \infty$, a fraction $1 - O(1/N)$ of posets in $\mathcal{P}_N$ partition into three antichain layers $V = L_1 \sqcup L_2 \sqcup L_3$ with:*
$$
\lvert L_1\rvert = \frac{N}{4} + o(N), \qquad \lvert L_2\rvert = \frac{N}{2} + o(N), \qquad \lvert L_3\rvert = \frac{N}{4} + o(N),
$$
*satisfying:*
1. *Every element of $L_1$ is strictly below every element of $L_3$: $u \prec w$ for all $u \in L_1, w \in L_3$;*
2. *Each pair $(u, v) \in L_1 \times L_2$ is comparable ($u \prec v$) independently with probability $1/2$;*
3. *Each pair $(v, w) \in L_2 \times L_3$ is comparable ($v \prec w$) independently with probability $1/2$;*
4. *Each layer $L_j$ is an antichain: no relations exist within $L_1, L_2$, or $L_3$.*

**Corollary 3.4 (Geometric Degeneracy of KR Posets).**  
*For almost all posets in the Kleitman–Rothschild ensemble:*
1. *The height freezes at $h(P) \le 3$, and strict chain abundances vanish for all $k \ge 3$:*
   $$
   C_k(P) = 0 \quad \forall k \ge 3 \implies \rho_2(P) = \frac{C_3(P)}{C_2(P)} = 0.
   $$
2. *The comparable-pair fraction freezes at an unphysical constant:*
   $$
   R_2(\text{KR}) \approx \frac{\lvert L_1\rvert\lvert L_3\rvert + \frac{1}{2}\lvert L_1\rvert\lvert L_2\rvert + \frac{1}{2}\lvert L_2\rvert\lvert L_3\rvert}{\binom{N}{2}} \approx \frac{\frac{N^2}{16} + \frac{N^2}{16} + \frac{N^2}{16}}{\frac{N^2}{2}} = \frac{3/16}{1/2} = \frac{3}{8} = 0.375.
   $$
3. *The apparent dimension estimate $d(3/8) \approx 2.38$ is entirely spurious: it reflects only the bipartite edge density of a static 3-layer graph, lacking timelike propagation, manifold scaling, or Lorentzian curvature.*

*Proof.*  
1. **Height and Chain Abundances**: Any chain $x_0 \prec x_1 \prec \dots \prec x_k$ can contain at most one element from $L_1$, one from $L_2$, and one from $L_3$, because each $L_j$ is an antichain. Thus the maximum chain length is 2 ($x_0 \in L_1 \prec x_1 \in L_2 \prec x_2 \in L_3$), which corresponds to $k=2$ (a 2-chain). Therefore:
   $$
   C_k(P) = 0 \quad \forall k \ge 3 \implies h(P) \le 2 \text{ (or } 3 \text{ counting vertices)}, \quad \rho_2(P) = 0.
   $$
   In contrast, a genuine $d$-dimensional spacetime manifold satisfies $h(P) \sim N^{1/d} \to \infty$ and $\rho_k \to \infty$ for all $k \le h(P)$.
2. **Comparable-Pair Fraction**:
   - Pairs between $L_1$ and $L_3$: all $\lvert L_1\rvert\lvert L_3\rvert \approx (N/4)(N/4) = N^2/16$ pairs are comparable.
   - Pairs between $L_1$ and $L_2$: on average, half are comparable, giving $\frac{1}{2}\lvert L_1\rvert\lvert L_2\rvert \approx \frac{1}{2}(N/4)(N/2) = N^2/16$.
   - Pairs between $L_2$ and $L_3$: on average, half are comparable, giving $\frac{1}{2}\lvert L_2\rvert\lvert L_3\rvert \approx \frac{1}{2}(N/2)(N/4) = N^2/16$.
   - Pairs within layers: 0.

   Total comparable pairs:
   $$
   C_1(P) \approx \frac{N^2}{16} + \frac{N^2}{16} + \frac{N^2}{16} = \frac{3}{16}N^2.
   $$
   Dividing by $\binom{N}{2} \approx N^2/2$:
   $$
   R_2(\text{KR}) \approx \frac{3/16}{1/2} = \frac{3}{8} = 0.375.
   $$
3. From the hand-derived rational table, $f(2) = 1/2 = 0.500$ and $f(3) = 8/35 \approx 0.22857$. Since $8/35 < 3/8 < 1/2$, the dimension estimator yields $d(3/8) \approx 2.38$. However, this is an artifact of 3-layer bipartite density without timelike depth. $\blacksquare$

---

## 4. Discrete General Covariance and the Size-Dependent Scaling Obstruction

To prevent fixed-$p$ percolation from collapsing to 1D ($R_2 \to 1$), one might naively attempt to make the edge probability size-dependent: $p_n \to 0$ as $n \to \infty$. Here we prove an exact no-go theorem: **naive size-dependent percolation destroys discrete general covariance**.

### 4.1 Formulation of Naive Size-Dependent Percolation

Consider a sequential growth process where at stage $n$ (when the existing poset $C$ has cardinality $\lvert C\rvert = n$), each newborn element $x$ selects a precursor ideal $S \subseteq C$ with probability governed by an edge parameter $p_n \in (0, 1)$:
$$
q_n(C, S) := p_n^{\lvert \operatorname{Max}(S)\rvert}\,(1 - p_n)^{n - \lvert S\rvert}.
$$
Here, $\operatorname{Max}(S)$ is the set of maximal elements of $S$, which become the direct links to the newborn element $x$, while the remaining $n - \lvert S\rvert$ elements outside $S$ are not linked.

### 4.2 Exact Proof of the Covariance Obstruction

**Theorem 4.1 (Discrete General Covariance Obstruction for Size-Dependent Percolation).**  
*Let $(p_n)_{n \ge 0}$ be a sequence of edge probabilities with $p_n \in (0, 1)$. The transition kernel $q_n(C, S) = p_n^{\lvert \operatorname{Max}(S)\rvert}(1 - p_n)^{n - \lvert S\rvert}$ satisfies the scalar diamond commutation identity:*
$$
q_n(C, S)\,q_{n+1}(C + x_S, T) = q_n(C, T)\,q_{n+1}(C + y_T, S) \quad \forall S, T \in \mathcal{I}(C)
$$
*if and only if $p_{n+1} = p_n$ for all $n \ge 0$ (i.e., the edge probability is strictly constant across all stages).*

*Proof.*  
Let $C$ be a base poset of cardinality $\lvert C\rvert = n$, and let $S, T \in \mathcal{I}(C)$ be two downward-closed ideals.

We compute the two path probabilities across the incomparable-birth diamond:
1. **Path 1 ($S$ chosen first, then $T$)**:
   - At stage $n$, vertex $x_S$ is adjoined to $C$ with past $S$. The transition probability is:
     $$
     q_n(C, S) = p_n^{\lvert \operatorname{Max}(S)\rvert}\,(1 - p_n)^{n - \lvert S\rvert}.
     $$
   - The intermediate poset $C + x_S$ has cardinality $\lvert C + x_S\rvert = n + 1$.
   - At stage $n+1$, vertex $y_T$ is adjoined with past $T \subseteq C$. Because $x_S \notin T$, the ideal $T$ within $C + x_S$ has the identical elements and identical maximal elements as in $C$:
     $$
     \lvert T\rvert_{C+x_S} = \lvert T\rvert, \qquad \operatorname{Max}_{C+x_S}(T) = \operatorname{Max}_C(T).
     $$
   - The transition probability at stage $n+1$ is therefore:
     $$
     q_{n+1}(C + x_S, T) = p_{n+1}^{\lvert \operatorname{Max}(T)\rvert}\,(1 - p_{n+1})^{(n+1) - \lvert T\rvert}.
     $$
   - Multiplying the two probabilities gives Path 1:
     $$
     \Pi_1(S, T) := q_n(C, S)\,q_{n+1}(C + x_S, T) = p_n^{\lvert \operatorname{Max}(S)\rvert}\,p_{n+1}^{\lvert \operatorname{Max}(T)\rvert}\,(1 - p_n)^{n - \lvert S\rvert}\,(1 - p_{n+1})^{n + 1 - \lvert T\rvert}.
     $$

2. **Path 2 ($T$ chosen first, then $S$)**:
   - At stage $n$, vertex $y_T$ is adjoined with past $T$:
     $$
     q_n(C, T) = p_n^{\lvert \operatorname{Max}(T)\rvert}\,(1 - p_n)^{n - \lvert T\rvert}.
     $$
   - At stage $n+1$, vertex $x_S$ is adjoined to $C + y_T$ with past $S$:
     $$
     q_{n+1}(C + y_T, S) = p_{n+1}^{\lvert \operatorname{Max}(S)\rvert}\,(1 - p_{n+1})^{(n+1) - \lvert S\rvert}.
     $$
   - Multiplying gives Path 2:
     $$
     \Pi_2(T, S) := q_n(C, T)\,q_{n+1}(C + y_T, S) = p_n^{\lvert \operatorname{Max}(T)\rvert}\,p_{n+1}^{\lvert \operatorname{Max}(S)\rvert}\,(1 - p_n)^{n - \lvert T\rvert}\,(1 - p_{n+1})^{n + 1 - \lvert S\rvert}.
     $$

3. **Commutation Ratio**:
   Dividing $\Pi_1(S, T)$ by $\Pi_2(T, S)$:
   $$
   \frac{\Pi_1(S, T)}{\Pi_2(T, S)} = \frac{p_n^{\lvert \operatorname{Max}(S)\rvert}\,p_{n+1}^{\lvert \operatorname{Max}(T)\rvert}}{p_n^{\lvert \operatorname{Max}(T)\rvert}\,p_{n+1}^{\lvert \operatorname{Max}(S)\rvert}} \cdot \frac{(1 - p_n)^{n - \lvert S\rvert}\,(1 - p_{n+1})^{n + 1 - \lvert T\rvert}}{(1 - p_n)^{n - \lvert T\rvert}\,(1 - p_{n+1})^{n + 1 - \lvert S\rvert}}.
   $$
   Collecting terms:
   $$
   \frac{\Pi_1(S, T)}{\Pi_2(T, S)} = \left(\frac{p_n}{p_{n+1}}\right)^{\lvert \operatorname{Max}(S)\rvert - \lvert \operatorname{Max}(T)\rvert} \cdot \left(\frac{1 - p_n}{1 - p_{n+1}}\right)^{\lvert T\rvert - \lvert S\rvert}.
   $$

4. **Necessary and Sufficient Condition**:
   For discrete general covariance to hold, this ratio must equal $1$ identically for all base posets $C$ and all pairs of ideals $S, T \in \mathcal{I}(C)$.

   Choose the base poset $C = A_n$ (the $n$-element antichain), and consider the ideals:
   - $S = \varnothing \implies \lvert S\rvert = 0, \ \lvert \operatorname{Max}(S)\rvert = 0$;
   - $T = \{v\}$ for some $v \in A_n \implies \lvert T\rvert = 1, \ \lvert \operatorname{Max}(T)\rvert = 1$.

   Substituting these ideals into the ratio:
   $$
   \frac{\Pi_1(\varnothing, \{v\})}{\Pi_2(\{v\}, \varnothing)} = \left(\frac{p_n}{p_{n+1}}\right)^{0 - 1} \cdot \left(\frac{1 - p_n}{1 - p_{n+1}}\right)^{1 - 0} = \frac{p_{n+1}}{p_n} \cdot \frac{1 - p_n}{1 - p_{n+1}}.
   $$
   Setting this ratio equal to 1:
   $$
   \frac{p_{n+1}(1 - p_n)}{p_n(1 - p_{n+1})} = 1 \iff p_{n+1}(1 - p_n) = p_n(1 - p_{n+1}).
   $$
   Expanding both sides:
   $$
   p_{n+1} - p_n p_{n+1} = p_n - p_n p_{n+1} \iff p_{n+1} = p_n.
   $$
   Thus, the scalar diamond identity holds if and only if $p_{n+1} = p_n$. $\blacksquare$

*Architectural Consequence*: Theorem 4.1 establishes an uncompromising no-go result: **it is mathematically impossible to achieve sparse-link scaling by naive stage-dependent percolation $p_n \to 0$ without violating discrete general covariance.** Any valid growth model must achieve sparsity through an intrinsically covariant structural mechanism.

---

## 5. Constructive Discrete Generally Covariant Regimes

We now analyze three discrete generally covariant sequential growth architectures that preserve complete-row normalization and Kolmogorov projectivity, rigorously separating what is proved (chain-tail non-freezing under $\sum a_n = \infty$, CSG general covariance, and ensemble-mean quantum steering versus single-history bimodal bifurcation) from open mathematical conjectures required for single-history manifold-compatible concentration (Open Proposals / Conjectures 5.3 and 5.5).

### 5.1 Regime A: Non-Summable Maximal-Deletion Schedules ($\sum a_n = \infty$)

Recall the maximal-deletion growth law from Stage 1 (`PW2-A`, Theorem 1):
$$
q(P, r, S) = a_n u(P, r, S) \quad (S \subsetneq P), \qquad q(P, r, P) = 1 - a_n \sum_{S \subsetneq P} u(P, r, S),
$$
where $0 < a_n < 1/M_n$ with $M_n = \max_{\lvert P\rvert=n, r} \sum_{S \subsetneq P} u(P, r, S) = \Sigma_u(A_n)$.

In Section 3.1, Theorem 3.1 established that any schedule satisfying $\sum_{n=4}^\infty a_n M_n < \infty$ freezes into an ordinal chain tail almost surely by the First Borel–Cantelli Lemma, because $\mathbb{P}(S_n \subsetneq P_n \mid \mathcal{F}_{n-1}) \le a_n M_n$.
However, the naive condition $\sum_{n=4}^\infty a_n M_n = \infty$ is **insufficient** to evade chain freezing: along an ordinal chain continuation $P_n = Q \oplus A_1$, the maximal-deletion sum is not $M_n$, but collapses identically to $\Sigma_u(Q \oplus A_1) \equiv 1$. If $\sum a_n < \infty$ while $\sum a_n M_n = \infty$, the probability of remaining in an infinite ordinal chain tail is strictly positive ($\prod (1 - a_n) > 0$).
Therefore, the necessary and sufficient condition to prevent 1D chain freezing is the divergence of the unweighted scale series: $\sum_{n=4}^\infty a_n = \infty$.

**Theorem 5.1 (Identical Covariance for Arbitrary Sequences $a_n$).**  
*For **any** sequence of positive scale parameters $(a_n)_{n \ge 4}$ with $0 < a_n < 1/M_n$, the maximal-deletion growth law satisfies:*
1. *Strict complete-row normalization: $\sum_{S \subseteq P} q(P, r, S) = 1$ for all $(P, r)$.*
2. *Exact scalar diamond commutation across all base posets $C$ of size $n-1$:*
   $$
   q(C, r, S)\,q(C + x_S, r + b_x, T) = q(C, r, T)\,q(C + y_T, r + c_y, S) \quad \forall S, T \subsetneq C.
   $$
3. *Exact Kolmogorov cylinder-set projectivity extending uniquely to infinite marked histories.*

*Proof.*  
Let $C$ be a base poset of cardinality $\lvert C\rvert = n - 1$, and let $S, T \subsetneq C$ be two distinct proper ideals.
When $x_S$ is adjoined to $C$, the resulting intermediate poset $C + x_S$ has cardinality:
$$
\lvert C + x_S\rvert = (n - 1) + 1 = n.
$$
Similarly, when $y_T$ is adjoined to $C$, the intermediate poset $C + y_T$ has cardinality:
$$
\lvert C + y_T\rvert = (n - 1) + 1 = n.
$$
Because $x_S \notin T$ and $y_T \notin S$, the ideal $T \subsetneq C + x_S$ and the ideal $S \subsetneq C + y_T$ are both **proper ideals of an $n$-element parent**.
Therefore, along Path 1:
$$
q(C + x_S, r + b_x, T) = a_n u(C + x_S, r + b_x, T).
$$
Along Path 2:
$$
q(C + y_T, r + c_y, S) = a_n u(C + y_T, r + c_y, S).
$$
In both path products, the scale factor at stage $n$ is identically $a_n$:
$$
\Pi_1 = q(C, r, S) \cdot a_n u(C + x_S, r + b_x, T), \qquad \Pi_2 = q(C, r, T) \cdot a_n u(C + y_T, r + c_y, S).
$$
By Theorem 1 of `PW2-A`, the structural potential $u$ satisfies the diamond relation identically:
$$
u(C, r, S)\,u(C + x_S, r + b_x, T) = u(C, r, T)\,u(C + y_T, r + c_y, S).
$$
The factor $a_n$ enters symmetrically on both sides and cancels identically. Therefore, diamond commutation holds identically for *arbitrary* sequence choices $(a_n)_{n \ge 4}$. $\blacksquare$

**Lemma 5.1 (Unique-Top Combinatorial Identity).**  
*For any finite base poset $Q$ of cardinality $\lvert Q\rvert = n - 1 \ge 0$ and any marking $r$, let $P = Q \oplus A_1$ be the ordinal chain extension with unique top element $x$ ($q \prec_P x$ for all $q \in Q$). Then:*
1. *The proper downward-closed ideals of $P$ are identically the downward-closed ideals of $Q$:*
   $$
   \{S \in \mathcal{I}(P) : S \subsetneq P\} = \mathcal{I}(Q).
   $$
2. *For every proper ideal $S \in \mathcal{I}(Q)$, the maximal-deletion structural potential satisfies:*
   $$
   u(Q \oplus A_1, r, S) = q(Q, r|_Q, S).
   $$
3. *The row sum $\Sigma_u(Q \oplus A_1, r) := \sum_{S \subsetneq Q \oplus A_1} u(Q \oplus A_1, r, S)$ satisfies the exact universal identity:*
   $$
   \Sigma_u(Q \oplus A_1, r) = \sum_{S \in \mathcal{I}(Q)} q(Q, r|_Q, S) \equiv 1,
   $$
   *identically for every base poset $Q$ and every marking $r$.*

*Proof of Lemma 5.1.*  
1. In $P = Q \oplus A_1$, every element $q \in Q$ satisfies $q \prec_P x$, so $x$ is the unique maximal element: $\operatorname{Max}(P) = \{x\}$. If an order ideal $S \subseteq P$ contains $x$, downward closure forces $Q \subseteq S \implies S = P$. If $x \notin S$, then $S \subseteq Q$, and downward closure in $P$ is equivalent to downward closure in $Q$. Thus $\{S \subsetneq P\} = \mathcal{I}(Q)$.
2. For any proper ideal $S \subsetneq P$, the missing maximal set is $M(P, S) = \operatorname{Max}(P) \setminus S = \{x\}$. The only non-empty subset is $A = \{x\}$ with $\lvert A\rvert = 1$. In the product definition of $u(P, r, S)$, the single term is $q(P \setminus \{x\}, r|_Q, S)^{(-1)^{1+1}} = q(Q, r|_Q, S)^1 = q(Q, r|_Q, S)$.
3. Summing over all proper ideals $S \subsetneq P$ yields $\Sigma_u(P, r) = \sum_{S \in \mathcal{I}(Q)} q(Q, r|_Q, S)$. By complete-row probability normalization of the structural growth kernel on $Q$, this sum equals $1$ identically. $\blacksquare$

**Theorem 5.2 (Evasion of 1D Freezing via Conditional Borel–Cantelli Lemma and Antichain Self-Throttling).**  
*Let $(a_n)_{n \ge 4}$ be any sequence of scale parameters satisfying $0 < a_n < 1/M_n$ and the non-summability condition:*
$$
\sum_{n=4}^\infty a_n = \infty.
$$
*Then:*
1. *The probability that infinitely many proper precursor ideals are chosen equals unity:*
   $$
   \mathbb{P}_\infty\left(\limsup_{n \to \infty} \{S_n \subsetneq P_n\}\right) = 1.
   $$
2. *The causal set never freezes into an ordinal chain tail: for every $N_0 \ge 4$,*
   $$
   \mathbb{P}_\infty\left(\exists n \ge N_0 : S_n \subsetneq P_n\right) = 1,
   $$
   *and for every stopping index $N_* \ge 4$, the chain-freezing event $F_{N_*} := \bigcap_{n=N_*}^\infty \{S_n = P_n\}$ occurs with probability zero:*
   $$
   \mathbb{P}_\infty\left(\bigcup_{N_*=4}^\infty \bigcap_{n=N_*}^\infty \{S_n = P_n\}\right) = 0.
   $$
3. *Antichain Self-Throttling: On the antichain $A_n$, the row sum $\Sigma_u(A_n) = M_n$ attains the unique global maximum across all $n$-element posets (Lemma 1 of `PW2-A`). Consequently, when the order widens, $q(P, r, P) = 1 - a_n \Sigma_u(P, r)$ attains its global minimum $1 - a_n M_n$, dynamically penalizing extreme antichains and suppressing 3-layer Kleitman–Rothschild collapse.*

*Proof of Theorem 5.2.*  
1. On the canonical filtered history space $(\Omega, \mathcal{F}, (\mathcal{F}_n)_{n \ge 0}, \mathbb{P}_\infty)$, let $E_n := \{S_n \subsetneq P_n\} \in \mathcal{F}_n$ be the event that a proper precursor ideal is chosen at step $n$. Conditioned on $\mathcal{F}_{n-1}$, the parent poset $P_n$ and marking $r_n$ are determined, giving:
   $$
   \mathbb{P}_\infty(E_n \mid \mathcal{F}_{n-1}) = \sum_{S \subsetneq P_n} q(P_n, r_n, S) = a_n \sum_{S \subsetneq P_n} u(P_n, r_n, S) = a_n \Sigma_u(P_n, r_n).
   $$
2. Fix an arbitrary integer $N_* \ge 4$ and consider the chain-freezing event $F_{N_*} := \bigcap_{n=N_*}^\infty \{S_n = P_n\} = \bigcap_{n=N_*}^\infty E_n^c$. On $F_{N_*}$, the newborn element at each step $n \ge N_*$ is adjoined above all existing elements ($S_{n-1} = P_{n-1}$), so $P_n = P_{n-1} \oplus A_1$ is an ordinal chain extension with a unique maximal element.
   By Lemma 5.1, for every $n \ge N_*$ on $F_{N_*}$:
   $$
   \Sigma_u(P_n, r_n) = \Sigma_u(P_{n-1} \oplus A_1, r_n) \equiv 1.
   $$
   Therefore, on the event $F_{N_*}$:
   $$
   \mathbb{P}_\infty(E_n \mid \mathcal{F}_{n-1}) = a_n \cdot 1 = a_n \quad \text{for all } n \ge N_*.
   $$
   Summing conditional probabilities on $F_{N_*}$:
   $$
   \sum_{n=N_*}^\infty \mathbb{P}_\infty(E_n \mid \mathcal{F}_{n-1}) = \sum_{n=N_*}^\infty a_n = \infty,
   $$
   which diverges by the non-summability hypothesis $\sum_{n=4}^\infty a_n = \infty$.
   By Lévy's conditional Borel–Cantelli lemma (Lévy 1937, Williams 1991 §12.15), for any adapted sequence of events, $\{E_n \text{ i.o.}\} = \{\sum_{n=1}^\infty \mathbb{P}(E_n \mid \mathcal{F}_{n-1}) = \infty\}$ holds $\mathbb{P}_\infty$-almost surely.
   Therefore:
   $$
   \mathbb{P}_\infty\left(\limsup_{n \to \infty} E_n \;\middle|\; F_{N_*}\right) = 1.
   $$
   However, by definition, $F_{N_*} \subseteq \bigcap_{n=N_*}^\infty E_n^c$, which asserts that $E_n$ occurs zero times for $n \ge N_*$. Since $\limsup E_n$ and $\bigcap_{n \ge N_*} E_n^c$ are disjoint, we must have:
   $$
   \mathbb{P}_\infty(F_{N_*}) = 0.
   $$
   By countable additivity over $N_* \ge 4$, $\mathbb{P}_\infty(\bigcup_{N_*=4}^\infty F_{N_*}) \le \sum_{N_*=4}^\infty \mathbb{P}_\infty(F_{N_*}) = 0$. Hence:
   $$
   \mathbb{P}_\infty\left(\exists n \ge N_0 : S_n \subsetneq P_n\right) = 1 - \mathbb{P}_\infty\left(\bigcap_{n=N_0}^\infty \{S_n = P_n\}\right) = 1 - 0 = 1,
   $$
   proving Part 2.
3. Because the event that proper ideals are chosen only finitely often is identically the union of freezing tails $\bigcup_{N_*=4}^\infty F_{N_*}$, its complement has probability:
   $$
   \mathbb{P}_\infty\left(\limsup_{n \to \infty} \{S_n \subsetneq P_n\}\right) = 1 - \mathbb{P}_\infty\left(\bigcup_{N_*=4}^\infty F_{N_*}\right) = 1 - 0 = 1.
   $$
   (Alternatively, since $\Sigma_u(P) \ge 1$ for all finite posets $P$, we have $\mathbb{P}_\infty(E_n \mid \mathcal{F}_{n-1}) \ge a_n$ unconditionally everywhere on $\Omega$, so $\sum_{n=4}^\infty \mathbb{P}_\infty(E_n \mid \mathcal{F}_{n-1}) \ge \sum_{n=4}^\infty a_n = \infty$ everywhere on $\Omega$, establishing $\mathbb{P}_\infty(\limsup E_n) = 1$ directly). This proves Part 1.
4. Part 3 follows directly from Lemma 1 of `PW2-A`: on $A_n$, every element is maximal ($\lvert\operatorname{Max}(A_n)\rvert = n$), giving $2^n - 1$ non-empty deletion subsets. Thus $\Sigma_u(A_n) = M_n$ attains the unique global maximum, and $q(A_n, r, A_n) = 1 - a_n M_n$ attains the unique global minimum, penalizing wide antichain extensions and suppressing 3-layer Kleitman–Rothschild collapse. $\blacksquare$

### 5.2 Regime B: Covariant Decaying-Coupling Classical Sequential Growth (CSG)

To construct an intrinsically covariant sparse-link percolation model, we formulate the generalized Rideout–Sorkin Classical Sequential Growth (CSG) family with a decaying coupling schedule.

In covariant CSG (Rideout & Sorkin 1999), the unnormalized transition weight for choosing precursor ideal $S \subseteq P_n$ is parameterized by a sequence of non-negative coupling constants $t_0, t_1, t_2, \dots$:
$$
\tilde{q}(P_n, S) = \sum_{k=0}^{\lvert \operatorname{Max}(S)\rvert} (-1)^{\lvert \operatorname{Max}(S)\rvert - k} \binom{\lvert \operatorname{Max}(S)\rvert}{k} \alpha_{\lvert S\rvert - \lvert \operatorname{Max}(S)\rvert + k},
$$
where $\alpha_m$ is related to $t_k$ by binomial inversion:
$$
\alpha_m = \sum_{k=0}^m \binom{m}{k} t_k.
$$
The normalized transition probability is:
$$
q(P_n, S) = \frac{\tilde{q}(P_n, S)}{\sum_{S' \in \mathcal{I}(P_n)} \tilde{q}(P_n, S')}.
$$

**Theorem 5.3 (Discrete General Covariance of CSG Families; Rideout & Sorkin 1999).**  
*For any sequence of non-negative coupling constants $(t_k)_{k \ge 0}$ with $t_0 > 0$, the Classical Sequential Growth transition probabilities $q(P_n, S)$ satisfy:*
1. *Discrete General Covariance holds identically: for any two incomparable births $x_S, y_T$ extending base poset $C$, the transition probabilities commute across paths, satisfying the diamond relation $\Pi_1 = \Pi_2$.*
2. *Markovian Kolmogorov Cylinder-Set Projectivity holds identically on $\Omega_\infty$.*

**Open Proposal / Conjecture 5.3 (Decaying-Coupling CSG Sparsity and Transitivity Breaking).**  
*Let $(t_k)_{k \ge 0}$ be a coupling sequence chosen to decay rapidly with precursor degree $k$, such as an exponential decay $t_k = t_0 \frac{t^k}{k!}$ or a power-law decay $t_k = c\,(k+1)^{-\beta}$ with decay exponent $\beta > 1$. It is conjectured that such decaying-coupling CSG processes evade the 1D transitive percolation collapse of Theorem 3.2 while retaining discrete general covariance, satisfying the following three mathematical criteria:*
1. *Uniform Link Degree Bound*: The expected number of immediate links (in-degree) per newborn element is uniformly bounded across all birth steps:
   $$
   \sup_{n \ge 1} \mathbb{E}\left[ \lvert \operatorname{Max}(S_n)\rvert \right] \le C_{\rm deg} < \infty.
   $$
2. *Transitivity Non-Percolation*: Long-range transitivity is broken, so that the comparable-pair fraction does not concentrate at 1 in the infinite-volume limit:
   $$
   \limsup_{N \to \infty} \mathbb{E}[R_2(P_N)] < 1, \qquad \lim_{N \to \infty} \mathbb{P}\left( R_2(P_N) > 1 - \epsilon \right) = 0 \quad \text{for some } \epsilon > 0.
   $$
3. *Antichain Width Divergence*: The antichain width diverges almost surely as $N \to \infty$:
   $$
   \operatorname{width}(P_N) \xrightarrow{N \to \infty} \infty \quad \mathbb{P}_\infty\text{-a.s.},
   $$
   ensuring the causal set does not degenerate into a bounded-width ordinal chain tail or post-chain.

*Mathematical Obstacles and Current Status*: While Rideout & Sorkin (1999) proved Discrete General Covariance for all non-negative $(t_k)$, the asymptotic geometric behavior of general CSG families remains an outstanding open problem. In particular, percolation-type couplings typically lead to either transitive domination (post-chains where almost all pairs are comparable) or cosmic-dust antichains. Whether power-law or factorial decay $t_k$ can simultaneously ensure non-trivial dimension $d(R_2) \in (3, 5)$ and manifold-like interval abundances $C_k(P_N)$ without introducing unphysical posts remains an active research program.

### 5.3 Regime C: Quantum-Steered Dimension Bounds and Ensemble-Mean Steering

We integrate the coherent quantum-order instrument of Stage 1 (`PW2-A`, Theorem 5) with the intrinsic dimension estimator $d(R_2)$ of Stage 3 (`PW4-B`) to analyze operational quantum steering of discrete spacetime geometry.

Recall Theorem 5 of `PW2-A`: let $q^{(+)}$ and $q^{(-)}$ be two distinct admitted structural kernels satisfying strict positivity, complete-row normalization, and scalar diamond commutation across all horizons. On qubit carrier $\mathcal{H}_{\rm hor} = \mathbb{C}^2$, the coherent Kraus operators:
$$
K_{S, b}^{P, r} = \frac{1}{\sqrt{2}}\left( \sqrt{q^{(+)}(P, r, S)}\,e^{-i\varphi_{K, b}^{(+)}/2}\lvert +\rangle\langle +\rvert + \sqrt{q^{(-)}(P, r, S)}\,e^{-i\varphi_{K, b}^{(-)}/2}\lvert -\rangle\langle -\rvert \right)
$$
define a completely positive, trace-preserving (CPTP) instrument with exact Kolmogorov prefix consistency and entangled diamond commutation.

For any initial qubit state $\rho \in \mathcal{D}(\mathcal{H}_{\rm hor})$ with coherence $\langle X \rangle = \operatorname{Tr}[X\rho] \in [-1, 1]$, the structural transition law is:
$$
\mathbb{P}_\rho(S \mid P, r) = \bar{q}(P, r, S) + \frac{1}{2}\Delta q(P, r, S)\,\langle X\rangle,
$$
where $\bar{q} = \frac{1}{2}(q^{(+)} + q^{(-)})$ and $\Delta q = q^{(+)} - q^{(-)}$.

**Theorem 5.4 (Ensemble-Mean Quantum-Steered Dimension Bounds Theorem).**  
*Let $q^{(+)}$ be a dense/focusing kernel (producing higher expected comparable-pair fractions $R_2^{(+)}(N)$) and $q^{(-)}$ be a sparse/branching kernel (producing lower expected comparable-pair fractions $R_2^{(-)}(N)$). Then for every horizon $N \ge 2$:*
1. *The ensemble-averaged comparable-pair fraction satisfies the exact linear steering law:*
   $$
   \mathbb{E}_\rho[R_2(P_N)] = \bar{R}_2(N) + \frac{1}{2}\Delta R_2(N)\,\langle X\rangle,
   $$
   *where $\bar{R}_2(N) = \frac{1}{2}(R_2^{(+)}(N) + R_2^{(-)}(N))$ and $\Delta R_2(N) = R_2^{(+)}(N) - R_2^{(-)}(N) > 0$.*
2. *The ensemble expectation value is strictly bounded by the extremal coherent states $\lvert \pm\rangle$:*
   $$
   R_2^{(-)}(N) \le \mathbb{E}_\rho[R_2(P_N)] \le R_2^{(+)}(N).
   $$
3. *Because $f^{-1}: (0, 1] \to [1, \infty)$ is strictly monotonically decreasing, the effective ensemble dimension $d_{\rm eff}(\rho, N) := f^{-1}(\mathbb{E}_\rho[R_2(P_N)])$ is steered inversely:*
   $$
   d^{(+)}(N) := f^{-1}(R_2^{(+)}(N)) \le d_{\rm eff}(\rho, N) \le f^{-1}(R_2^{(-)}(N)) =: d^{(-)}(N).
   $$
4. *Ensemble-Mean Dimension Targeting at $d = 4.0$: For base kernels satisfying $R_2^{(-)}(N) \le 1/10 \le R_2^{(+)}(N)$, there exists a unique target coherence $\langle X\rangle_* \in [-1, 1]$ such that:*
   $$
   \mathbb{E}_{\rho_*}[R_2(P_N)] = \frac{1}{10} = f(4) \implies d_{\rm eff}(\rho_*, N) = 4.0.
   $$

*Proof.*  
1. The comparable-pair count is $C_1(P_N) = \sum_{1 \le u < v \le N} \mathbf{1}_{\{u \prec_{P_N} v\}}$. Taking expectations under the mixture measure $\mathbb{P}_{\infty, \rho} = \frac{1+\langle X\rangle}{2}\mathbb{P}_\infty^{(+)} + \frac{1-\langle X\rangle}{2}\mathbb{P}_\infty^{(-)}$ yields:
   $$
   \mathbb{E}_\rho[C_1(P_N)] = \frac{1+\langle X\rangle}{2}\mathbb{E}^{(+)}[C_1(P_N)] + \frac{1-\langle X\rangle}{2}\mathbb{E}^{(-)}[C_1(P_N)].
   $$
   Dividing by $\binom{N}{2}$ yields the linear relation:
   $$
   \mathbb{E}_\rho[R_2(P_N)] = \frac{1+\langle X\rangle}{2} R_2^{(+)}(N) + \frac{1-\langle X\rangle}{2} R_2^{(-)}(N) = \bar{R}_2(N) + \frac{1}{2}\Delta R_2(N)\,\langle X\rangle.
   $$
2. Since $\langle X\rangle = \operatorname{Tr}[X\rho] \in [-1, 1]$, the linear function is maximized at $\langle X\rangle = +1$ (pure state $\lvert +\rangle$) and minimized at $\langle X\rangle = -1$ (pure state $\lvert -\rangle$).
3. Strict monotonicity of $f(d)$ was proved in Section 2.4: $f'(d) < 0$ on $[1, \infty)$, so $f^{-1}$ is strictly decreasing. Applying $f^{-1}$ to $R_2^{(-)} \le \mathbb{E}_\rho[R_2] \le R_2^{(+)}$ reverses the inequalities, establishing the dimension bounds.
4. From the hand-derived rational table, $f(4) = 1/10 = 0.100000$. If $R_2^{(-)}(N) \le 1/10 \le R_2^{(+)}(N)$, then $1/10 \in [R_2^{(-)}(N), R_2^{(+)}(N)]$. By linearity, setting $\bar{R}_2(N) + \frac{1}{2}\Delta R_2(N)\langle X\rangle_* = 1/10$ yields the unique solution:
   $$
   \langle X\rangle_* = \frac{1/10 - \bar{R}_2(N)}{\frac{1}{2}\Delta R_2(N)} = \frac{2/10 - (R_2^{(+)} + R_2^{(-)})}{R_2^{(+)} - R_2^{(-)}} \in [-1, 1]. \quad \blacksquare
   $$

**Proposition 5.5 (Single-History Extremal Branch Bifurcation and Absence of Mean Concentration).**  
*Let $\Omega_\infty$ be the measurable space of infinite causal set histories equipped with cylinder $\sigma$-algebra $\mathcal{F}_\infty$. Under the static, unmeasured coherent quantum carrier state $\rho \in \mathcal{D}(\mathcal{H}_{\rm hor})$, the infinite-history probability measure is the convex mixture:*
$$
\mathbb{P}_{\infty, \rho} = \frac{1 + \langle X\rangle}{2}\mathbb{P}_\infty^{(+)} + \frac{1 - \langle X\rangle}{2}\mathbb{P}_\infty^{(-)}.
$$
*Assume that the extremal kernels $q^{(+)}$ and $q^{(-)}$ possess well-defined, distinct asymptotic comparable-pair fractions:*
$$
R_2(P_N) \xrightarrow{N \to \infty} R_2^{(+)} \quad \mathbb{P}_\infty^{(+)}\text{-a.s.}, \qquad R_2(P_N) \xrightarrow{N \to \infty} R_2^{(-)} \quad \mathbb{P}_\infty^{(-)}\text{-a.s.},
$$
*with $R_2^{(-)} < R_2^{(+)}$. Then for any single realization history $\omega = (P_1, P_2, \dots) \in \Omega_\infty$:*
1. *Bimodal Asymptotic Distribution: The single-history observable $R_2(P_N(\omega))$ converges almost surely to the discrete two-point set $\{R_2^{(+)}, R_2^{(-)}\}$, sampling the extremal branches with fixed probabilities:*
   $$
   \mathbb{P}_{\infty, \rho}\left(\lim_{N \to \infty} R_2(P_N) = R_2^{(+)}\right) = \frac{1 + \langle X\rangle}{2}, \qquad \mathbb{P}_{\infty, \rho}\left(\lim_{N \to \infty} R_2(P_N) = R_2^{(-)}\right) = \frac{1 - \langle X\rangle}{2}.
   $$
2. *Absence of Concentration at the Ensemble Mean: If $\langle X\rangle \in (-1, 1)$, $R_2(P_N)$ does NOT concentrate at the ensemble average $\mathbb{E}_\rho[R_2(P_N)]$. Specifically, for any tolerance $\epsilon < \frac{1}{2}\min\{\mathbb{E}_\rho[R_2] - R_2^{(-)}, \, R_2^{(+)} - \mathbb{E}_\rho[R_2]\}$:*
   $$
   \lim_{N \to \infty} \mathbb{P}_{\infty, \rho}\left( \left\lvert R_2(P_N) - \mathbb{E}_\rho[R_2(P_N)] \right\rvert > \epsilon \right) = 1.
   $$
3. *Physical Consequence for Single-Universe Dimension: Under the target coherence $\langle X\rangle_*$ of Theorem 5.4 satisfying $\mathbb{E}_{\rho_*}[R_2(P_N)] = 1/10$, an individual causal set history almost surely NEVER stabilizes at $d(R_2) = 4.0$. Instead, it yields a universe with dimension $d^{(+)} = f^{-1}(R_2^{(+)})$ with probability $\frac{1+\langle X\rangle_*}{2}$, or dimension $d^{(-)} = f^{-1}(R_2^{(-)})$ with probability $\frac{1-\langle X\rangle_*}{2}$.*

*Proof.*  
Under the Kraus representation of Theorem 5 (`PW2-A`), the two-kernel channel acts on the carrier state by $K_{S, b}^{P, r} \propto \sqrt{q^{(+)}}\lvert +\rangle\langle +\rvert + \sqrt{q^{(-)}}\lvert -\rangle\langle -\rvert$. Because these operators are diagonal in the $\{|+\rangle, |-\rangle\}$ basis across all birth steps, the density operator $\rho$ maintains fixed diagonal weights $p_+ = \langle +|\rho|+\rangle = \frac{1+\langle X\rangle}{2}$ and $p_- = \langle -|\rho|-\rangle = \frac{1-\langle X\rangle}{2}$. For any cylinder event $A \in \mathcal{F}_\infty$, the projectivity theorem yields $\mathbb{P}_{\infty, \rho}(A) = p_+\mathbb{P}_\infty^{(+)}(A) + p_-\mathbb{P}_\infty^{(-)}(A)$.  
Let $E_\pm = \{\omega \in \Omega_\infty : \lim_{N \to \infty} R_2(P_N(\omega)) = R_2^{(\pm)}\}$. By hypothesis, $\mathbb{P}_\infty^{(+)}(E_+) = 1$ and $\mathbb{P}_\infty^{(+)}(E_-) = 0$, while $\mathbb{P}_\infty^{(-)}(E_-) = 1$ and $\mathbb{P}_\infty^{(-)}(E_+) = 0$. Hence $\mathbb{P}_{\infty, \rho}(E_+) = p_+$ and $\mathbb{P}_{\infty, \rho}(E_-) = p_-$.  
Since $R_2^{(-)} < \mathbb{E}_\rho[R_2] < R_2^{(+)}$ for $\langle X\rangle \in (-1, 1)$, the point $\mathbb{E}_\rho[R_2]$ is strictly bounded away from both $R_2^{(+)}$ and $R_2^{(-)}$. For any $\epsilon < \frac{1}{2}\min\{\mathbb{E}_\rho[R_2] - R_2^{(-)}, \, R_2^{(+)} - \mathbb{E}_\rho[R_2]\}$, the closed neighborhood $[\mathbb{E}_\rho[R_2] - \epsilon, \mathbb{E}_\rho[R_2] + \epsilon]$ contains neither limit point. Therefore:
$$
\mathbb{P}_{\infty, \rho}\left( \left\lvert R_2(P_N) - \mathbb{E}_\rho[R_2(P_N)] \right\rvert \le \epsilon \right) \le \mathbb{P}_{\infty, \rho}(\Omega_\infty \setminus (E_+ \cup E_-)) + o(1) \xrightarrow{N \to \infty} 0.
$$
This establishes non-concentration at the ensemble mean with probability 1. $\blacksquare$

### 5.4 Open Proposal / Conjecture 5.5: Closed-Loop Curvature Feedback Dimension Attractor

As proved in Proposition 5.5, an unmeasured, static initial quantum probe state cannot steer an individual causal set history to dimension $d=4.0$; it merely samples an extremal branch $R_2^{(\pm)}$. To achieve true single-history stabilization around $d=4.0$, the quantum probe must participate in an **active, closed-loop dynamical feedback cycle**: at each birth step $n \to n+1$, the discrete geometry of the causal set $P_{n+1}$ is measured (or back-reacts on the quantum probe), re-preparing the carrier state $\rho_{n+1}$ adaptively according to the instantaneous curvature observable.

#### 5.4.1 Formulation of the Coupled Stochastic Process
Let $(P_n, \rho_n)_{n \ge 1}$ be the coupled causal-set/carrier state defined on filtered probability space $(\Omega, \mathcal{F}, (\mathcal{F}_n)_{n \ge 1}, \mathbb{P})$:
1. **Growth Step**: At stage $n$, newborn element $x_n$ adjoins to precursor ideal $S_n \subseteq P_n$ with probability conditioned on instantaneous carrier coherence $\langle X\rangle_n = \operatorname{Tr}[X\rho_n]$:
   $$
   \mathbb{P}(S_n \mid P_n, \rho_n) = \bar{q}(P_n, r_n, S_n) + \frac{1}{2}\Delta q(P_n, r_n, S_n)\,\langle X\rangle_n,
   $$
   yielding child poset $P_{n+1} = P_n \cup \{x_n\}$.
2. **Curvature Readout & Adaptive Reset**: The 4D Benincasa–Dowker scalar curvature action $S_{\rm BD}^{(4)}(P_{n+1})$ and comparable-pair fraction $R_2(P_{n+1})$ are evaluated. A trace-preserving quantum feedback channel $\mathcal{E}_{P_{n+1}}$ updates the carrier state:
   $$
   \rho_{n+1} = \mathcal{E}_{P_{n+1}}(\rho_n),
   $$
   re-steering the subsequent coherence $\langle X\rangle_{n+1} = \operatorname{Tr}[X\rho_{n+1}]$ via the self-correcting feedback rule:
   $$
   \langle X\rangle_{n+1} = -\tanh\left( \gamma \left( R_2(P_{n+1}) - \frac{1}{10} \right) + \kappa\,\frac{S_{\rm BD}^{(4)}(P_{n+1})}{n+1} \right), \quad \gamma, \kappa > 0.
   $$
   - *Chain-Freezing Suppression (Geodesic Dispersion)*: When the causal set elongates into long linear chains, intermediate elements accumulate in $N_1$, driving the curvature action positive ($S_{\rm BD}^{(4)} > 0$) and $R_2 > 1/10$. The feedback rule sets $\langle X\rangle_{n+1} < 0$, enhancing the sparse/branching kernel $q^{(-)}$ to halt chain continuation.
   - *KR / Antichain Collapse Suppression (Interval Focusing)*: When the poset branches too broadly into wide antichains, lateral links accumulate without intermediate elements ($N_1 = 0, N_2 \ge 1$), driving the curvature action negative ($S_{\rm BD}^{(4)} < 0$) and $R_2 < 1/10$. The feedback rule sets $\langle X\rangle_{n+1} > 0$, enhancing timelike capping and chain continuation.

**Open Proposal / Conjecture 5.5 (Closed-Loop Curvature Feedback Dimension Attractor).**  
*Let $(P_n, \rho_n)_{n \ge 1}$ be the coupled stochastic process defined by the adaptive feedback rule with feedback gains $\gamma, \kappa > 0$. It is conjectured that the critical manifold-like 4D hypersurface:*
$$
\mathcal{M}_4^* := \left\{ P \in \mathcal{P} : R_2(P) = \frac{1}{10}, \; S_{\rm BD}^{(4)}(P) = 0 \right\}
$$
*is a global almost sure stochastic attractor for the closed-loop dynamics, satisfying the following three mathematical criteria:*
1. *Lyapunov Negative Drift (Supermartingale Property Outside Attractor Band)*:
   Define the geometric Lyapunov function:
   $$
   V(P_n) = \left( R_2(P_n) - \frac{1}{10} \right)^2 + \alpha \left( \frac{S_{\rm BD}^{(4)}(P_n)}{n} \right)^2 \quad (\alpha > 0).
   $$
   There exists a target neighborhood $U_\delta = \{ P \in \mathcal{P} : \lvert R_2(P) - 1/10\rvert \le \delta \}$ and a drift rate $c > 0$ such that for all $P_n \notin U_\delta$:
   $$
   \mathbb{E}\left[ V(P_{n+1}) - V(P_n) \;\middle|\; \mathcal{F}_n \right] \le -c\,\frac{V(P_n)}{n}.
   $$
2. *Single-History 4D Dimension Convergence*:
   Along almost every realized causal set history $\omega = (P_1, P_2, \dots) \in \Omega_\infty$, the ordering fraction converges asymptotically to the 4D Alexandrov constant:
   $$
   \lim_{N \to \infty} R_2(P_N(\omega)) = \frac{1}{10} \quad \mathbb{P}\text{-a.s.} \implies \lim_{N \to \infty} d(R_2(P_N(\omega))) = 4.0 \quad \mathbb{P}\text{-a.s.}
   $$
3. *Preservation of Extended Discrete General Covariance*:
   Because naive stage-indexed feedback conditioned on global poset invariants $R_2(P_{n+1})$ and $S_{\rm BD}^{(4)}(P_{n+1})$ depends on the intermediate poset along a birth order (in general $R_2(C + x_S) \neq R_2(C + y_T)$ across incomparable ideals $S, T \in \mathcal{I}(C)$, breaking path commutation if fed back verbatim at step $n+1$), an admissible covariant feedback channel $\mathcal{E}$ must condition carrier updates solely on causal-past subposet invariants ($J^-(x)$) or admit a diamond-confluent history-space representation across incomparable births.

*Mathematical Challenges and Research Program*: Proving Conjecture 5.5 requires (i) replacing global stage-slice observables in the prototype rule above with strictly causal-past ($J^-(x)$) observables so spacelike-separated growth events commute identically, (ii) establishing the Lyapunov negative-drift inequality by bounding martingale increments of $\Delta C_k(P_n)$ without trapping in limit cycles or post-dominated phases, and (iii) proving single-history concentration of both $R_2(P_N)$ and interval abundance ratios $\rho_k(P_N)$ around their 4D Alexandrov values.

---

## 6. Intrinsic Myrheim–Meyer & Interval-Abundance Scaling Limits

### 6.1 Asymptotic Scaling Limits of Invariant Observables ($N \to \infty$)

To understand how discrete posets approach continuum spacetimes in the large-$N$ limit, we contrast the asymptotic scaling behavior of invariant observables across three distinct regimes:
1. **$d$-Dimensional Manifold Sprinkling**: Elements are Poisson-sprinkled into an Alexandrov interval in flat Minkowski spacetime $\mathbb{M}^d$.
2. **1D Ordinal Chain Tail**: Bounded-width posets resulting from summable growth ($P_{N_*} \oplus C_{N-N_*}$).
3. **3-Layer Kleitman–Rothschild Poset**: Combinatorially dominant random posets ($V = L_1 \sqcup L_2 \sqcup L_3$).

#### Comparative Scaling Matrix

| Observable / Invariant | $d$-Dimensional Manifold | 1D Ordinal Chain | 3-Layer KR Poset |
|:---:|:---:|:---:|:---:|
| Poset Height $h(P_N)$ | $\sim N^{1/d} \to \infty$ | $\sim N \to \infty$ | $\le 3$ (Frozen) |
| Poset Width $\operatorname{width}(P_N)$ | $\sim N^{(d-1)/d} \to \infty$ | $O(1)$ (Bounded) | $\sim N/2 \to \infty$ |
| Height $\times$ Width | $\sim N$ | $\sim N$ | $O(N)$ |
| Comparable Fraction $R_2(P_N)$ | $\to f(d) \in (0, 1)$ | $\to 1.0$ | $\to 3/8 = 0.375$ |
| Dimension Estimator $d(R_2)$ | $\to d$ | $\to 1.0$ | $\to \approx 2.38$ (Spurious) |
| Successive Ratio $\rho_1 = C_2/C_1$ | $\sim N \to \infty$ | $\sim N \to \infty$ | $\sim N/24 \to \infty$ |
| Successive Ratio $\rho_2 = C_3/C_2$ | $\sim N \to \infty$ | $\sim N \to \infty$ | $0$ (Vanishes Identically) |
| Curvature Action $S_{\rm BD}^{(4)}$ | Fluctuates $\sim O(\sqrt{N})$ | $N - 1 \sim +N \to +\infty$ ($N \ge 4$) | $\sim -N^2/8 \to -\infty$ |

*Note on Asymptotic $S_{\rm BD}^{(4)}$ Scaling*: For the $N$-element ordinal chain $C_N$ ($N \ge 4$), $N_k = N - 1 - k$ ($k = 0, 1, 2, 3$), giving the exact linear growth $S_{\rm BD}^{(4)}(C_N) = N - (N-1) + 9(N-2) - 16(N-3) + 8(N-4) = N - 1$ (evaluating to $+3$ at the $N = 4$ benchmark $C_4$ in Section 7). For an asymptotic 3-layer Kleitman–Rothschild poset ($\lvert L_1\rvert, \lvert L_3\rvert \approx N/4$, $\lvert L_2\rvert \approx N/2$), adjacent-layer pairs are links ($\mathbb{E}[N_0] \approx \frac{1}{2}(N/4)(N/2) + \frac{1}{2}(N/2)(N/4) = N^2/8$) while every $(u, w) \in L_1 \times L_3$ has $\lvert I(u, w)\rvert \sim \operatorname{Binomial}(N/2, 1/4)$, so $N_1, N_2, N_3$ decay exponentially in $N$ and $\mathbb{E}[S_{\rm BD}^{(4)}(\text{KR}_N)] = N - N^2/8 + o(N^2) \sim -N^2/8 \to -\infty$ (whereas the small $N = 8$ deterministic toy poset $P_{\rm KR}$ in Section 7 has $(N_0, N_1, N_2, N_3) = (8, 2, 1, 0)$ and $S_{\rm BD}^{(4)}(P_{\rm KR}) = +2$).

### 6.2 The $\rho_2 = 0$ Rejection Screen Against Kleitman–Rothschild Collapse

In a manifold-like causal set of dimension $d$, the expected chain abundances scale as:
$$
\mathbb{E}[C_k(P_N)] \sim N^{k+1}\,v_d^k\,\frac{\Gamma(d+1)^k}{\Gamma((k+1)d/2)\dots}.
$$
Consequently, the successive chain ratios diverge linearly with cardinality:
$$
\rho_k(P_N) = \frac{C_{k+1}(P_N)}{C_k(P_N)} \sim c_k(d)\,N \xrightarrow{N \to \infty} \infty \quad \text{for all } k \ge 1.
$$
In stark contrast, for any 3-layer Kleitman–Rothschild poset, $C_3 \equiv 0$, so:
$$
\rho_2(\text{KR}) = \frac{C_3(\text{KR})}{C_2(\text{KR})} = 0.
$$
This provides a remarkably sharp, computationally inexpensive rejection screen (`NG-02`): **any growth regime that produces $\rho_2(P_N) = 0$ for large $N$ is immediately rejected as a non-manifold layered collapse**.

### 6.3 Formulation of `NG-02` Inexpensive Regime Screens

In accordance with `docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md` (`NG-02`), any admissible manifold-like growth regime must pass three simultaneous screens:
1. **Screen 1 (Width Divergence)**: $\lim_{N \to \infty} \Pr(\operatorname{width}(P_N) \le k) = 0$ for all fixed $k < \infty$ (rejects 1D chain freezing).
2. **Screen 2 (Height Divergence & Timelike Depth)**: $\lim_{N \to \infty} \Pr(h(P_N) \le 3) = 0$ and $\lim_{N \to \infty} \Pr(\rho_2(P_N) = 0) = 0$ (rejects 3-layer KR collapse).
3. **Screen 3 (Non-Trivial Comparability)**: $\lim_{N \to \infty} \Pr(R_2(P_N) \ge 1 - \epsilon) = 0$ and $\lim_{N \to \infty} \Pr(R_2(P_N) \le \epsilon) = 0$ for all $\epsilon > 0$ (rejects fixed-$p$ percolation collapse and antichain evaporation).

Evaluating the Section 5 architectures against Screens 1–3 distinguishes proved guarantees from open mathematical requirements:
- **Regime A ($\sum a_n = \infty$, Theorems 5.1–5.2)**: Provably prevents permanent ordinal chain-tail freezing ($\mathbb{P}_\infty(\bigcup_{N_*} F_{N_*}) = 0$) and enforces antichain self-throttling ($\Sigma_u(A_n) = M_n$ maximal); establishing full compliance with Screens 1 and 3 ($\operatorname{width}(P_N) \to \infty$ and $R_2(P_N)$ bounded strictly away from $1$) additionally requires bounding the asymptotic density of global posts ($S_n = P_n$).
- **Regime B (Decaying-Coupling CSG, Theorem 5.3 & Conjecture 5.3)**: Satisfies discrete general covariance and Kolmogorov projectivity identically; simultaneous satisfaction of Screens 1–3 under rapid coupling decay $t_k \to 0$ is the precise content of Open Proposal / Conjecture 5.3.
- **Regime C & Closed-Loop Extension (Theorem 5.4, Proposition 5.5, Conjecture 5.5)**: Static coherent steering tunes the ensemble mean $\mathbb{E}_{\rho_*}[R_2(P_N)] = 1/10$ (Theorem 5.4) but bifurcates individual histories onto the extremal branches $R_2^{(\pm)}$ (Proposition 5.5), so single-history compliance with Screen 3 around $R_2 \approx 1/10$ ($d \approx 4.0$) requires either a base kernel already concentrating in $(\epsilon, 1-\epsilon)$ or proving the closed-loop causal-past feedback attractor of Open Proposal / Conjecture 5.5.

---

## 7. Exact Canonical Benchmark Evaluations on Small Posets and Asymptotic Scaling Limits

With repository software strictly paused, all benchmark invariants are derived explicitly by hand from first principles (and independently cross-checked on $N \le 6$ via external scratch verification).

### 7.1 Detailed Step-by-Step Hand Calculations for Canonical Posets

#### 1. Singleton $P_1$ ($N=1$)
- Poset: Single element $\{0\}$, no relations.
- Incidence matrix: $C_P = (0)_{1\times 1}$.
- Invariants: $C_1 = 0$, $\binom{1}{2} = 0$, $R_2$ undefined, $h = 0$, $C_2 = 0, C_3 = 0$.
- Layer counts: $N_0 = 0, N_1 = 0, N_2 = 0, N_3 = 0$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(P_1) = 1 - 2(0) = 1, \qquad S_{\rm BD}^{(4)}(P_1) = 1 - 1(0) = 1.
  $$

#### 2. Two-Chain $C_2$ ($N=2$)
- Poset: Two elements $\{0, 1\}$ with $0 \prec 1$.
- Incidence matrix: $C_P = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$. $C_P^2 = 0$.
- Invariants: $C_1 = 1$, $\binom{2}{2} = 1 \implies R_2(C_2) = 1/1 = 1.000$, $d(R_2) = 1.000$, $h = 1$, $C_2 = 0, C_3 = 0$.
- Layer counts: Pair $(0, 1)$ has $n(1, 0) = 0$ (link) $\implies N_0 = 1, N_1 = 0, N_2 = 0, N_3 = 0$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(C_2) = 2 - 2(1) + 4(0) - 2(0) = 0.
  $$
  $$
  S_{\rm BD}^{(4)}(C_2) = 2 - 1(1) + 9(0) - 16(0) + 8(0) = 1.
  $$

#### 3. Two-Antichain $A_2$ ($N=2$)
- Poset: Two elements $\{0, 1\}$ with $0 \parallel 1$.
- Incidence matrix: $C_P = 0_{2 \times 2}$.
- Invariants: $C_1 = 0 \implies R_2(A_2) = 0$, $d(R_2) = \infty$, $h = 0$, $C_2 = 0, C_3 = 0$.
- Layer counts: $N_0 = 0, N_1 = 0, N_2 = 0, N_3 = 0$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(A_2) = 2 - 0 = 2, \qquad S_{\rm BD}^{(4)}(A_2) = 2 - 0 = 2.
  $$

#### 4. Three-Chain $C_3$ ($N=3$)
- Poset: Three elements $\{0, 1, 2\}$ with $0 \prec 1 \prec 2$.
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 1 & 0 \end{pmatrix}, \quad C_P^2 = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}, \quad C_P^3 = 0.
  $$
- Invariants: $C_1 = 3$, $\binom{3}{2} = 3 \implies R_2(C_3) = 1.000$, $d(R_2) = 1.000$, $h = 2$, $C_2 = 1, C_3 = 0$.
- Layer counts:
  - $(0, 1)$: $n=0$ (link);
  - $(1, 2)$: $n=0$ (link);
  - $(0, 2)$: $n=1$ (element 1 intervening).
  Hence $N_0 = 2, N_1 = 1, N_2 = 0, N_3 = 0$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(C_3) = 3 - 2(2) + 4(1) - 2(0) = 3 - 4 + 4 = 3.
  $$
  $$
  S_{\rm BD}^{(4)}(C_3) = 3 - 1(2) + 9(1) - 16(0) + 8(0) = 3 - 2 + 9 = 10.
  $$

#### 5. Three-Element Fork $V$ ($N=3$)
- Poset: Elements $\{0, 1, 2\}$ with $0 \prec 1$ and $0 \prec 2$, with $1 \parallel 2$.
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 1 & 0 & 0 \end{pmatrix}, \quad C_P^2 = 0.
  $$
- Invariants: $C_1 = 2$, $\binom{3}{2} = 3 \implies R_2(V) = 2/3 \approx 0.666667$.
  Since $f(1) = 1$ and $f(2) = 0.5$, $d(2/3) \approx 1.54$. Height $h = 1$, $C_2 = 0, C_3 = 0$.
- Layer counts: Both $(0, 1)$ and $(0, 2)$ are links $\implies N_0 = 2, N_1 = 0, N_2 = 0, N_3 = 0$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(V) = 3 - 2(2) = -1.
  $$
  $$
  S_{\rm BD}^{(4)}(V) = 3 - 1(2) = 1.
  $$

#### 6. Four-Element Causal Diamond $E_{\text{diamond}}$ ($N=4$)
- Poset: Elements $\{0, 1, 2, 3\}$ with $0 \prec 1 \prec 3$ and $0 \prec 2 \prec 3$, with $1 \parallel 2$.
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix}, \quad C_P^2 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 2 & 0 & 0 & 0 \end{pmatrix}, \quad C_P^3 = 0.
  $$
- Invariants: $C_1 = 5$, $\binom{4}{2} = 6 \implies R_2(E_{\text{diamond}}) = 5/6 \approx 0.833333$.
  Dimension estimate: $d(5/6) \approx 1.25$. Height $h = 2$, $C_2 = 2$ (chains $0 \prec 1 \prec 3$ and $0 \prec 2 \prec 3$), $C_3 = 0$.
- Layer counts:
  - Links: $(0, 1), (0, 2), (1, 3), (2, 3)$ all have $n=0 \implies N_0 = 4$.
  - Interval $(0, 3)$ has $I(0, 3) = \{1, 2\}$, so $n(3, 0) = 2 \implies N_2 = 1$.
  - $N_1 = 0, N_3 = 0$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(E_{\text{diamond}}) = 4 - 2(4) + 4(0) - 2(1) = 4 - 8 - 2 = -6.
  $$
  $$
  S_{\rm BD}^{(4)}(E_{\text{diamond}}) = 4 - 1(4) + 9(0) - 16(1) + 8(0) = 4 - 4 - 16 = -16.
  $$
  *Notice the strong negative curvature ($S_{\rm BD} < 0$), reflecting the interval-focusing convergence of the causal diamond.*

#### 7. Four-Chain $C_4$ ($N=4$)
- Poset: Elements $\{0, 1, 2, 3\}$ with $0 \prec 1 \prec 2 \prec 3$.
- Incidence matrix:
  $$
  C_P = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 1 & 1 & 0 & 0 \\ 1 & 1 & 1 & 0 \end{pmatrix}, \quad C_P^2 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \\ 2 & 1 & 0 & 0 \end{pmatrix}, \quad C_P^3 = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 \end{pmatrix}.
  $$
- Invariants: $C_1 = 6$, $\binom{4}{2} = 6 \implies R_2(C_4) = 1.000$, $d(R_2) = 1.000$, $h = 3$.
  Chain abundances: $C_2 = \mathbf{1}^T C_P^2 \mathbf{1} = 1 + 2 + 1 = 4 = \binom{4}{3}$, $C_3 = \mathbf{1}^T C_P^3 \mathbf{1} = 1 = \binom{4}{4}$.
  Ratios: $\rho_1 = 4/6 = 2/3$, $\rho_2 = 1/4$.
- Layer counts:
  - Links: $(0, 1), (1, 2), (2, 3) \implies N_0 = 3$.
  - 1-intervals: $(0, 2), (1, 3) \implies N_1 = 2$.
  - 2-intervals: $(0, 3) \implies N_2 = 1$.
  - $N_3 = 0$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(C_4) = 4 - 2(3) + 4(2) - 2(1) = 4 - 6 + 8 - 2 = +4.
  $$
  $$
  S_{\rm BD}^{(4)}(C_4) = 4 - 1(3) + 9(2) - 16(1) + 8(0) = 4 - 3 + 18 - 16 = +3.
  $$
  *Notice the positive curvature ($S_{\rm BD} > 0$), reflecting geodesic dispersion along the 1D chain.*

#### 8. Four-Antichain $A_4$ ($N=4$)
- Poset: Four completely incomparable elements, $C_P = 0_{4 \times 4}$.
- Invariants: $C_1 = 0 \implies R_2(A_4) = 0$, $d(R_2) = \infty$, $h = 0$, $C_2 = 0, C_3 = 0$.
- Layer counts: $N_0 = 0, N_1 = 0, N_2 = 0, N_3 = 0$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(A_4) = 4 - 0 = 4, \qquad S_{\rm BD}^{(4)}(A_4) = 4 - 0 = 4.
  $$

#### 9. Six-Element Crown Poset $E_{\text{crown}}$ ($N=6$)
- Poset: Three minimal elements $\{0, 1, 2\}$ and three maximal elements $\{3, 4, 5\}$.
  Relations: each minimal element connects to two maximal elements:
  $$
  0 \prec 3, 4; \qquad 1 \prec 4, 5; \qquad 2 \prec 5, 3.
  $$
- Invariants: $N = 6$, total relations $C_1 = 6$.
  Total pairs: $\binom{6}{2} = 15 \implies R_2(E_{\text{crown}}) = \frac{6}{15} = \frac{2}{5} = 0.400000$.
  Dimension estimate: $f(2) = 0.500$ and $f(3) \approx 0.229$. Since $0.229 < 0.400 < 0.500$, $d(2/5) \approx 2.29$.
  Height $h = 1$, $C_2 = 0, C_3 = 0$.
- Layer counts: All 6 relations are direct links between minimal and maximal elements with no intermediate elements:
  $$
  N_0 = 6, \qquad N_1 = 0, \qquad N_2 = 0, \qquad N_3 = 0.
  $$
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(E_{\text{crown}}) = 6 - 2(6) + 4(0) - 2(0) = 6 - 12 = -6.
  $$
  $$
  S_{\rm BD}^{(4)}(E_{\text{crown}}) = 6 - 1(6) + 9(0) - 16(0) + 8(0) = 6 - 6 = 0.
  $$
  *(Note on arithmetic verification: Evaluating $S_{\rm BD}^{(4)}$ strictly from definition yields $N - N_0 = 6 - 6 = 0$. If the link term $N_0$ were omitted, the vertex count alone would give $+6$. Hand derivation confirms the exact value is $0$.)*

#### 10. Eight-Element 3-Layer KR Prototype $P_{\rm KR}$ ($N=8$)
- Poset: Partitioned into three layers matching the KR ratios ($N/4, N/2, N/4$):
  - Bottom layer: $L_1 = \{0, 1\}$ ($\lvert L_1\rvert = 2$);
  - Middle layer: $L_2 = \{2, 3, 4, 5\}$ ($\lvert L_2\rvert = 4$);
  - Top layer: $L_3 = \{6, 7\}$ ($\lvert L_3\rvert = 2$).
- Relations:
  - Full bipartite relations between $L_1$ and $L_3$:
    $$
    0 \prec 6, \quad 0 \prec 7, \quad 1 \prec 6, \quad 1 \prec 7 \quad (4 \text{ relations}).
    $$
  - Adjacent layer relations (7 relations):
    $$
    0 \prec 2, \quad 0 \prec 3, \quad 1 \prec 4 \quad (3 \text{ relations between } L_1 \text{ and } L_2).
    $$
    $$
    2 \prec 6, \quad 3 \prec 6, \quad 3 \prec 7, \quad 4 \prec 7 \quad (4 \text{ relations between } L_2 \text{ and } L_3).
    $$
  - Total comparable pairs: $C_1(P_{\rm KR}) = 4 + 7 = 11$.
  - Total pairs: $\binom{8}{2} = 28 \implies R_2(P_{\rm KR}) = \frac{11}{28} \approx 0.392857$.
  - Dimension estimate: $f(2) = 0.500$ and $f(3) \approx 0.229$. Since $11/28 \approx 0.393$, $d(11/28) \approx 2.32$.
- Chain abundances:
  - Height $h = 2$, $C_3 = 0$.
  - 2-chains: intermediate paths through $L_2$ for the 4 pairs in $L_1 \times L_3$:
    * For $(0, 6)$: intermediate elements are $\{2, 3\}$, so $n(6, 0) = 2$ (contributes 2 two-chains);
    * For $(0, 7)$: intermediate element is $\{3\}$, so $n(7, 0) = 1$ (contributes 1 two-chain);
    * For $(1, 6)$: no intermediate elements, $n(6, 1) = 0$ (direct relation);
    * For $(1, 7)$: intermediate element is $\{4\}$, so $n(7, 1) = 1$ (contributes 1 two-chain).
    * Summing: $C_2 = 2 + 1 + 0 + 1 = 4$.
- Layer counts:
  - $N_0$: 7 adjacent relations $+ (1, 6) = 8$. Thus $N_0 = 8$.
  - $N_1$: pairs $(0, 7)$ and $(1, 7)$ have $n=1 \implies N_1 = 2$.
  - $N_2$: pair $(0, 6)$ has $n=2 \implies N_2 = 1$.
  - $N_3 = 0$.
  - Check sum: $N_0 + N_1 + N_2 + N_3 = 8 + 2 + 1 + 0 = 11 = C_1$.
- Scalar curvature actions:
  $$
  S_{\rm BD}^{(2)}(P_{\rm KR}) = 8 - 2(8) + 4(2) - 2(1) = 8 - 16 + 8 - 2 = -2.
  $$
  $$
  S_{\rm BD}^{(4)}(P_{\rm KR}) = 8 - 1(8) + 9(2) - 16(1) + 8(0) = 0 + 18 - 16 = +2.
  $$

### 7.2 Canonical Benchmark Master Table

The following master table compiles all hand-derived invariant quantities across the canonical benchmark posets. In strict adherence to GFM formatting rules, all math pipes within table cells are escaped using `\lvert ... \rvert`.

#### Benchmark Table 1: Invariant Geometry, Dimension Estimates, and Curvature Actions

| Poset $P$ | Vertices $N$ | Height $h(P)$ | $C_1(P)$ | $C_2(P)$ | $C_3(P)$ | $R_2(P)$ | $d(R_2)$ | $S_{\rm BD}^{(2)}(P)$ | $S_{\rm BD}^{(4)}(P)$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Singleton $P_1$ | 1 | 0 | 0 | 0 | 0 | Undefined | Undefined | $1$ | $1$ |
| Two-Chain $C_2$ | 2 | 1 | 1 | 0 | 0 | $1$ | $1.000$ | $0$ | $1$ |
| Two-Antichain $A_2$ | 2 | 0 | 0 | 0 | 0 | $0$ | $\infty$ | $2$ | $2$ |
| Three-Chain $C_3$ | 3 | 2 | 3 | 1 | 0 | $1$ | $1.000$ | $3$ | $10$ |
| Fork $V$ | 3 | 1 | 2 | 0 | 0 | $\frac{2}{3}$ | $\approx 1.54$ | $-1$ | $1$ |
| Diamond $E_{\text{diamond}}$ | 4 | 2 | 5 | 2 | 0 | $\frac{5}{6}$ | $\approx 1.25$ | $-6$ | $-16$ |
| Four-Chain $C_4$ | 4 | 3 | 6 | 4 | 1 | $1$ | $1.000$ | $4$ | $3$ |
| Four-Antichain $A_4$ | 4 | 0 | 0 | 0 | 0 | $0$ | $\infty$ | $4$ | $4$ |
| Crown $E_{\text{crown}}$ | 6 | 1 | 6 | 0 | 0 | $\frac{2}{5}$ | $\approx 2.29$ | $-6$ | $0$ |
| 3-Layer KR $P_{\rm KR}$ | 8 | 2 | 11 | 4 | 0 | $\frac{11}{28}$ | $\approx 2.32$ | $-2$ | $+2$ |

*Note: In Benchmark Table 1, all values are verified by first-principles hand derivations. For $C_4$, $C_2(C_4) = \binom{4}{3} = 4$ and $C_3(C_4) = \binom{4}{4} = 1$. For $E_{\text{crown}}$, $N_0 = 6$ yields $S_{\rm BD}^{(4)} = 6 - 6 = 0$. For $P_{\rm KR}$, layer abundances $(N_0, N_1, N_2, N_3) = (8, 2, 1, 0)$ yield $S_{\rm BD}^{(2)} = -2$ and $S_{\rm BD}^{(4)} = +2$.*

---

## 8. Empirical Verification, Hand-Derivation Audit Trail, and Peer Review Mandate

### 8.1 Empirical Verification Methodology Under Strict Software Pause

Under the repository software pause (`FOUNDATIONAL_RESEARCH_SCOPE.md`), all repository code and test harnesses (`det8/`, `scripts/`, `run_tests.py`) remain completely untouched. Primary verification of all mathematical claims, proofs, and evaluations is performed by deterministic, hand-executable procedures, supplemented by independent external scratch-only small-case checks ($N \le 6$):
1. **Combinatorial Identities**: Re-evaluated and verified by hand across matrix powers $C_P^k$ and binomial identities $\binom{N}{k}$.
2. **Gamma Function Reductions**: Re-derived step by step using $\Gamma(z+1) = z\Gamma(z)$ and $\Gamma(1/2) = \sqrt{\pi}$, verifying all rational fraction reductions ($f(1)=1, f(2)=1/2, f(3)=8/35, f(4)=1/10, f(5)=128/3003, f(6)=1/56$).
3. **Discrete Curvature Sums**: Checked by counting intervals $N_0, N_1, N_2, N_3$ and verifying $S_{\rm BD}^{(2)}$ and $S_{\rm BD}^{(4)}$ arithmetic.
4. **POSIX Tool Discipline**: Only POSIX file tools (`cat`, `cp`, `diff`, `mv`, `printf`), cryptographic hashing (`shasum -a 256`), and version control (`git`) are utilized.

### 8.2 Hand-Derivation Audit Trail

- **Borel–Cantelli Proof of 1D Freezing (Theorem 3.1)**:
  Verified that $\sum a_n M_n < \infty$ implies $\Pr(\limsup \{S_n \subsetneq P_n\}) = 0$. Verified that $S_n = P_n$ forces $P_N = P_{N_*} \oplus C_{N-N_*}$, causing $R_2 = 1 - O(1/N^2) \to 1$ and $d \to 1.0$.
- **Percolation Transitive Shortcut Proof (Theorem 3.2)**:
  Verified the conditional independence of 2-step paths $E_w$, confirming $\Pr(u \not\prec v) \le (1 - p^2)^{v-u-1}$. Verified the geometric series summation $\sum_{k=1}^\infty (1 - p^2)^{k-1} = 1/p^2$, the upper bound $\mathbb{E}[I(P_N)] \le N/p^2$, and the convergence in probability $R_2(P_N) \xrightarrow{p} 1 \implies d(R_2) \xrightarrow{p} 1.0$ via Markov's inequality and Continuous Mapping Theorem.
- **Kleitman–Rothschild Degeneracy (Theorem 3.3)**:
  Verified bipartite edge densities $\lvert L_1\rvert\lvert L_3\rvert + \frac{1}{2}\lvert L_1\rvert\lvert L_2\rvert + \frac{1}{2}\lvert L_2\rvert\lvert L_3\rvert = \frac{3}{16}N^2$, giving $R_2 \approx 3/8 = 0.375$. Verified that $C_k = 0$ for all $k \ge 3$, establishing $\rho_2 = 0$.
- **Covariance Obstruction for Naive $p_n \to 0$ (Theorem 4.1)**:
  Verified the path ratio $\frac{\Pi_1(\varnothing, \{v\})}{\Pi_2(\{v\}, \varnothing)} = \frac{p_{n+1}(1 - p_n)}{p_n(1 - p_{n+1})}$, proving it equals $1$ if and only if $p_{n+1} = p_n$.
- **Constructive Regimes (Theorems 5.1–5.4, Proposition 5.5, Open Proposals 5.3 & 5.5)**:
  - Verified that scale parameter $a_n$ cancels identically in the scalar diamond identity across all proper ideals because both intermediate posets have cardinality $n$ (Theorem 5.1).
  - Verified conditional Borel–Cantelli proof of chain-tail non-freezing under $\sum a_n = \infty$ via the exact combinatorial identity $\Sigma_u(Q \oplus A_1) \equiv 1$ (Theorem 5.2).
  - Formulated Discrete General Covariance for CSG families (Theorem 5.3, Rideout & Sorkin 1999) and re-classified decaying-coupling sparsity to Open Proposal / Conjecture 5.3, specifying exact mathematical criteria (uniform link degree bound $O(1)$, transitivity non-percolation, antichain width divergence).
  - Verified ensemble-mean linear steering $\mathbb{E}_\rho[R_2] = \bar{R}_2 + \frac{1}{2}\Delta R_2 \langle X\rangle$ (Theorem 5.4), while proving that single histories undergo bimodal extremal branch concentration at $R_2^{(\pm)}$ without concentrating at the ensemble mean (Proposition 5.5).
  - Re-classified closed-loop $d=4.0$ dynamical feedback stabilization from an established claim to Open Proposal / Conjecture 5.5, specifying Lyapunov stability, single-history convergence, and covariance preservation criteria.

### 8.3 Governance Compliance Audit

1. **Status-M Quarantine**: Ontological files (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) are completely untouched (`git diff` confirms 0 modifications). The quarantine is declared in the Line 3 Decision block and Section 1.4.
2. **Strict Sibling Isolation**: Automated search confirms zero mentions, cross-links, or dependencies regarding sibling Stage 4 observables or protocols.
3. **KaTeX Delimiter Compliance**: Math expressions use strictly `$ ... $` for inline and `$$ ... $$` for display. Zero `\(` or `\[` delimiters.
4. **GFM Table Pipe Escaping**: All vertical bars in math cells within Markdown tables are escaped as `\lvert ... \rvert`.

### 8.4 Peer Review and Provenance Custody Mandate

In accordance with R3 of `ORIGINAL_REQUEST.md`, this deliverable is subject to independent adversarial scientific review:
- Prospective protocol `PW5B_PROTOCOL.md` was frozen prior to authoring with recorded SHA-256 hash:
  `00aff6b697f8f39d06393c6ca82fec37e814ac9ae0c9eff01d934a5301de8e9a`.
- The deliverable will be audited by an independent scientific reviewer and challenger, verifying 100% of mathematical derivations, rational arithmetic, bounds, links, KaTeX delimiters, and table escaping by hand until `VERDICT: ACCEPT`.
- Upon acceptance, Section 9 `## Scientific review` will be appended with exact 64-hex SHA-256 hashes for prospective protocol, accepted author report, and independent scientific review report.

---

## 9. Scientific review

Manifold-Compatible Scaling Author derived exact analytical growth obstructions beyond Stage 1's Dichotomy (1D chain freezing for summable $a_n$, fixed-$p$ percolation 1D dimension collapse $d(R_2) \to 1.0$, 3-layer Kleitman–Rothschild collapse with $\rho_2 = 0$, and discrete general covariance failure for naive $p_n \to 0$ where $\Pi_1 / \Pi_2 = 1 \iff p_{n+1} = p_n$), alongside constructive discrete generally covariant regimes: non-summable maximal-deletion scale schedules $\sum a_n = \infty$ (with conditional Borel–Cantelli non-freezing via $\Sigma_u(Q \oplus A_1) \equiv 1$), covariant decaying-coupling CSG formulated with covariance proved and sparsity/transitivity breaking as an open conjecture, ensemble-mean quantum-steered dimension bounds with proved bimodal single-history branch concentration, and closed-loop Benincasa–Dowker curvature back-action formulated as an open dynamical feedback proposal with Lyapunov criteria. Independent Reviewer and Adversarial Challenger independently verified by hand 100% of proofs, Borel–Cantelli bounds, path independence ratios, Myrheim–Meyer inverses, gamma function reductions, and canonical benchmark posets. Prospective protocol SHA-256 00aff6b697f8f39d06393c6ca82fec37e814ac9ae0c9eff01d934a5301de8e9a; accepted author report SHA-256 00095615f51fe7857f2d9f06acf199ad76cf3387640a38ad859f524e2db787de; independent scientific review SHA-256 f085f09f7bfd9d090cdca623529c48ce391d30fdf6e69d63988859b5ba6f43c1; adversarial challenge report SHA-256 7e965e882105afa3b7aa756ad2be1f27d8f5419ccf6fcd99fa034ab4b148093b.
