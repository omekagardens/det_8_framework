# Prospective Research Protocol PW6-A: Single-History Geometry Without Breaking Covariance

**Document ID**: `PW6A_PROTOCOL.md`  
**Stage**: Stage 5A / PW6-A  
**Date**: 2026-11-14T19:35:00Z  
**Target Deliverable**: Authoritative Specification & Proof Protocol for Stage 5A / PW6-A  
**Protocol Status**: Authoritative Prospective Specification & Proof Protocol  

---

## 1. Objectives, Foundational Scope & Decision Block

### 1.1 Purpose and Physical Vision
This prospective protocol establishes the authoritative mathematical specification, analytical derivations, proof structures, covariance obstructions, and verification procedures for **Stage 5A / PW6-A: Single-History Geometry Without Breaking Covariance**.

The foundational research mandate established in `docs/coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md` (`NG-02`) and `docs/observables/manifold_compatible_growth_scaling_and_dimension_stabilization.md` addresses the fundamental problem of **single-history dimension stabilization**:
1. In Stage 4 investigations (`NG-02`), static quantum steering over an ensemble of causal set histories was shown to steer the ensemble-averaged comparable-pair fraction $\mathbb{E}_\rho[R_2(P_N)]$ linearly via probe coherence $\langle X\rangle$, tuning the ensemble average to the 4D Alexandrov value $\mathbb{E}_{\rho_*}[R_2] = 1/10 = f(4)$. However, **Proposition 5.5** proved that under static steering, individual histories almost surely never stabilize at $d = 4.0$: the probability measure bifurcates into a disjoint bimodal mixture of dense ($R_2^{(+)}$) and sparse ($R_2^{(-)}$) branches with zero concentration at the mean.
2. To achieve true physical dimension stabilization for a single realized universe, dynamical feedback is required. Yet, Markovian ad-hoc closed-loop feedback rules conditioned on global stage-slice observables (such as $R_2(P_{n+1})$ or $S_{\rm BD}^{(4)}(P_{n+1})$) break **Discrete General Covariance** (path independence / diamond commutation across incomparable births)—in sharp contrast to covariant de Finetti mixtures $\mathbb{P}_\mu = \int \mathbb{P}_t\,d\mu(t)$—while sequential monolithic carrier conditioning generates path-dependent gauge non-commutation without constituting operational channel-level spacelike signaling ($\mathcal{E}_x = \sum_S \mathcal{J}_{x_S}$).
3. This protocol resolves this foundational tension by:
   - Formulating exact **Covariance No-Go Theorems on Global, Monolithic-Carrier, and Stage-Normalized Precursor Feedback** (establishing why stage-normalized precursor weights $w(S, \mathcal{R}|_S)/Z(P, \mathcal{R})$—including register-modulated CSG couplings—break diamond commutation whenever $Z(C+x_S) \ne Z(C+y_T)$), and constructing the **local past-record register** $\mathcal{R}(v)$ whose causal synthesis commutes identically across spacelike births and couples covariantly to order growth via maximal-deletion full-ideal compensation (`PW2-A`, Theorem 1).
   - Providing rigorous analytic proofs of **uniformly bounded link in-degree** ($\sup_n \sup_{P_n} \mathbb{E}[\lvert\operatorname{Max}(S_n)\rvert \mid P_n] \le k_{\rm max} < \infty$ in finite-cutoff Classical Sequential Growth, alongside exact two-sided $\sqrt{n}$ antichain extremal bounds in factorial CSG $t_k = c/k!$) and **almost surely vanishing global-post density** ($\rho_{\rm post}(P_N) \xrightarrow{\text{a.s.}} 0$ in both families, with $N_{\rm post}(\infty) < \infty$ a.s. in finite-cutoff CSG).
   - Proving from first principles via the Rideout–Sorkin subset-ideal bijection that individual histories of both covariant CSG families almost surely satisfy **Screen 1** ($\operatorname{width}(P_N) \to \infty$), **Screen 2** ($h(P_N) \to \infty$ and $\rho_2(P_N) > 0$ eventually), and **covering-link sparsity with linear connectivity** ($N_0(P_N)/\binom{N}{2} \to 0$ and $N_0(P_N) \ge N - O(1)$ a.s.), while rigorously demarcating infinite-volume transitive comparability concentration ($R_2(P_N) \in (\epsilon, 1-\epsilon)$, Screen 3) and closed-loop 4D dimension stabilization (`Conjecture 5.5`) as explicit `[OPEN CONJECTURE]` problems.

### 1.2 Decision Block

**Decision.** Conditioning Markovian ad-hoc feedback on global stage-slice observables (in sharp contrast to covariant de Finetti mixtures $\mathbb{P}_\mu = \int \mathbb{P}_t\,d\mu(t)$), branch-selective monolithic carrier updates (which induce diamond path non-commutation without constituting operational channel-level spacelike signaling under $\mathcal{E}_x = \sum_S \mathcal{J}_{x_S}$), or naive stage-normalized precursor weights $w(S, \mathcal{R}|_S)/Z(P, \mathcal{R})$ provably violates Discrete General Covariance across incomparable growth diamonds, whereas localized past-record registers $\mathcal{R}(v)$ synthesized strictly from causal predecessors $\operatorname{Max}(S)$ preserve exact path independence, eliminate spacelike signaling, and couple covariantly to sequential growth via maximal-deletion full-ideal compensation; in Classical Sequential Growth, finite-cutoff couplings ($t_k = 0$ for $k > k_{\rm max}$, $k_{\rm max} \ge 2$) provably achieve uniformly bounded link in-degree ($\lvert\operatorname{Max}(S_n)\rvert \le k_{\rm max}$), finite total global posts ($N_{\rm post}(\infty) < \infty \implies \rho_{\rm post} \xrightarrow{\text{a.s.}} 0$), width divergence ($\operatorname{width}(P_N) \to \infty$ a.s., Screen 1), height divergence with 3-chain depth ($h(P_N) \to \infty, \rho_2(P_N) > 0$ eventually a.s., Screen 2), and vanishing covering-link density with linear connectivity ($N_0/\binom{N}{2} \to 0$, $N_0 \ge N - O(1)$ a.s.), but are provably obstructed from Screen 3 by the exact non-asymptotic fixed-cutoff parent-path union bound ($\mathbb{E}[R_2(P_N)] \le \frac{2}{N} + \frac{2 k_{\rm max}^{2+1/k_{\rm max}}}{(k_{\rm max}-1)(2k_{\rm max}-1)}\frac{N^{1-1/k_{\rm max}}}{N-1} = O(N^{-1/k_{\rm max}}) \to 0$ for $k_{\rm max} \ge 2$, and $\le \frac{2(1+\ln N)}{N} = O(\ln N / N) \to 0$ for $k_{\rm max} = 1$), formally eliminating fixed-cutoff CSG from Conjecture 7.3B; meanwhile, factorial CSG ($t_k = c/k!$) exhibits exact $c$-cancellation ($q = \tilde{q}/\alpha_n$ independent of $c > 0$) while geometric-factorial CSG ($t_k = c^k/k!$) exhibits empirical upward drift of $R_2$ toward transitive saturation ($R_2(2000) = 0.8842$ at $c = 1$, $0.9253$ at $c = 2$), and full-ideal-compensated feedback obeys the exact capping comparability bound $\mathbb{E}[R_2(P_N)] \ge \frac{2}{N(N-1)}\sum_{n=1}^{N-1} n\,\mathbb{E}[1 - a_n\Sigma_u(P_n, \tilde{r}_n)]$ (Theorem 8.1), leaving asymptotic interior transitive comparability ($R_2(P_N) \in (\epsilon, 1-\epsilon)$, Screen 3) for unbounded coupling families and single-history 4D closed-loop attraction as explicitly formulated open conjectures; Status-M ontological documents (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) remain strictly quarantined under Status-M, and no claim is made to derive continuum general relativity, smooth manifold topology, Born's rule, or physical coupling constants.

### 1.3 Governance, Isolation, and Quarantine Constraints
- **Strict Sibling Isolation**: This protocol is authored under strict sibling isolation. It contains ZERO mentions, cross-links, or citations to sibling Stage 5 observables, protocols, or parallel track deliverables.
- **Strict Software Pause**: In accordance with foundational research governance, ZERO modifications have been or will be made to software code inside the repository (`det8/`, `scripts/`, `run_tests.py`, etc.). All mathematical identities, combinatorial bounds, differences, and limits are derived analytically from first principles. Numerical cross-checks are restricted to external scratch verification tools outside the git repository.
- **Status-M Quarantine**: Ontological files (`ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`) are strictly quarantined and remain 100% untouched (0 diff lines).
- **Formatting Standards**: Strict KaTeX syntax is maintained throughout: inline math uses `$ ... $`, display math uses `$$ ... $$` (zero LaTeX paren/bracket math delimiters), and GitHub Flavored Markdown (GFM) tables escape pipe characters as `\lvert ... \rvert`, `\parallel`, or `\mid`.

---

## 2. Mathematical Taxonomy & Epistemic Matrix

To maintain absolute epistemic integrity, every claim in this protocol is rigorously classified into one of three explicit categories:
1. `[PROVED THEOREM]`: A mathematically complete statement with an analytic proof derived from first principles.
2. `[COUNTEREXAMPLE/OBSTRUCTION]`: A rigorous no-go result or explicit counterexample establishing the impossibility of a naive formulation.
3. `[OPEN CONJECTURE]`: A precise mathematical proposition whose full infinite-volume asymptotic closure remains open, supported by finite-size derivations and numerical scratch verification.

### Epistemic Status Matrix

| Claim / Theorem | Formal Mathematical Statement | Epistemic Status | Primary Obstacle / Proof Strategy |
|:---|:---|:---:|:---|
| **Proposition 5.5** | Static unmeasured steering yields bimodal measure $\mathbb{P}_{\infty, \rho} = p_+ \mathbb{P}_\infty^{(+)} + p_- \mathbb{P}_\infty^{(-)}$ with $\lim_{N \to \infty} \mathbb{P}_{\infty, \rho}(\lvert R_2 - \mathbb{E}[R_2]\rvert > \epsilon) = 1$. | `[PROVED THEOREM]` | Proved via Kraus diagonal decomposition and disjoint asymptotic support of extremal kernels. |
| **Theorem 5.1** (Markovian Global Feedback Obstruction) | Markovian growth conditioned on global slice $R_2(P_{n+1})$ breaks diamond commutation $\Pi_1 \ne \Pi_2$ because $R_2(C+x_S) - R_2(C+y_T) = \frac{\lvert S\rvert - \lvert T\rvert}{\binom{n+1}{2}} \ne 0$, distinct from covariant de Finetti mixtures $\mathbb{P}_\mu = \int \mathbb{P}_t\,d\mu(t)$. | `[COUNTEREXAMPLE/OBSTRUCTION]` | Explicit combinatorial computation of comparable-pair discrepancy across diamond paths. |
| **Theorem 5.2** (Monolithic Carrier Non-Commutation & Path Dependence) | Sequential measurement updates on a monolithic carrier $\rho$ across spacelike births $x \parallel y$ generate path-dependent states $\rho_{n+1}^{(1)} \ne \rho_{n+1}^{(2)}$ and diamond non-commutation; does not constitute operational channel-level signaling ($\mathcal{E}_x = \sum_S \mathcal{J}_{x_S}$). | `[COUNTEREXAMPLE/OBSTRUCTION]` | Proved via non-commutativity of sequential Kraus updates conditioned on spacelike-separated data. |
| **Theorem 5.3 & Cor. 5.3.1** (Partition Function Obstruction) | Stage-normalized precursor feedback $w(S, \mathcal{R}\rvert_S)/Z(P, \mathcal{R})$ (including register-modulated CSG $t_k(\mathcal{R})$) breaks covariance whenever $Z(C+x_S) \ne Z(C+y_T)$ ($6 \ne 8$ for uniform weights on $A_2$; $6 \ne 5$ for register-modulated $t_1$). | `[COUNTEREXAMPLE/OBSTRUCTION]` | Direct counterexamples on $A_2$ evaluating ideal lattice sums and diamond ratios. |
| **Theorem 5.4** (Local Register Covariance & Compensation) | Register $\mathcal{R}(v)$ synthesized strictly via $\operatorname{Max}(S)$ commutes across spacelike births, eliminates signaling, and couples covariantly to order growth via maximal-deletion full-ideal compensation (`PW2-A` Theorem 1). | `[PROVED THEOREM]` | Proved via causal independence $x_S \notin T, y_T \notin S$ and recursive proper-slot maximal-deletion induction. |
| **Theorem 6.1** (CSG Link In-Degree Bounds) | In finite-cutoff CSG ($t_k = 0$ for $k > k_{\rm max}$), $\lvert\operatorname{Max}(S_n)\rvert \le k_{\rm max} < \infty$ identically; in any CSG, $\mathbb{E}[d_n \mid P_n] \le \mathbb{E}[d_n \mid A_n]$, with exact non-asymptotic bounds $\sqrt{n+1}-1 < \mathbb{E}[d_n \mid A_n] < \sqrt{n}$ for $t_k = c/k!$ and antichain extinction $\le K e^{-\frac{4}{3}n^{3/2}}$. | `[PROVED THEOREM]` | Proved via Rideout–Sorkin subset bijection $B \mapsto J^-(B)$ and Laguerre real-root Poisson-binomial variance inequality. |
| **Theorem 6.2** (Vanishing Global-Post Density) | Global-post density vanishes almost surely ($\rho_{\rm post}(P_N) \xrightarrow{\text{a.s.}} 0$) in both finite-cutoff CSG ($\mathbb{P}(S_n = P_n \mid P_n) \le k_{\rm max}/n$, $N_{\rm post}(\infty) < \infty$ a.s. for $k_{\rm max} \ge 2$) and factorial CSG ($\mathbb{P}(S_n = P_n \mid P_n) < 1/\sqrt{n}$ universally). | `[PROVED THEOREM]` | Proved via exact falling-factorial identity, Cesàro $k^4$-subsequence Borel–Cantelli interpolation, and $\lvert\operatorname{Max}(P_n)\rvert \to \infty$. |
| **Theorem 7.1** (Screen 1: Width Divergence) | Both finite-cutoff CSG ($k_{\rm max} \ge 1$) and factorial CSG ($t_k = c/k!$) satisfy $\operatorname{width}(P_N) \xrightarrow{N \to \infty} \infty$ $\mathbb{P}_\infty$-a.s. | `[PROVED THEOREM]` | Proved via exact autonomous hypergeometric Markov transition for $M_n = \lvert\operatorname{Max}(P_n)\rvert$. |
| **Theorem 7.2** (Screen 2: Height & 3-Chains) | Both finite-cutoff CSG ($k_{\rm max} \ge 1$) and factorial CSG ($t_k = c/k!$) satisfy $h(P_N) \to \infty$ and $\rho_2(P_N) > 0$ eventually $\mathbb{P}_\infty$-a.s. | `[PROVED THEOREM]` | Proved via exact maximal-chain extension bound $\mathbb{P}(\Delta h_n \ge 1 \mid \mathcal{F}_{n-1}) \ge \mathbb{E}_{\pi_n}[K_n]/n$ and Lévy's conditional Borel–Cantelli lemma. |
| **Theorem 7.3A** (Link Sparsity & Linear Connectivity) | In finite-cutoff ($k_{\rm max} \ge 2$) and factorial CSG, covering-link density vanishes ($\mathbb{E}[N_0(P_N)]/\binom{N}{2} \to 0$) while $N_0(P_N) \ge N - O(1)$ $\mathbb{P}_\infty$-a.s. (finitely many empty births). | `[PROVED THEOREM]` | Proved via Theorem 6.1 degree bounds and First Borel–Cantelli summability of $\sum t_0/\alpha_n < \infty$. |
| **Theorem 7.3B'** (Fixed-Cutoff Parent-Path Bound & Comparability Collapse) | In any fixed-cutoff CSG ($k_{\rm max} < \infty$), expected comparability decays via exact finite-$N$ union bounds: $\mathbb{E}[R_2(P_N)] \le \frac{2(1+\ln N)}{N} \to 0$ ($k_{\rm max} = 1$) and $\mathbb{E}[R_2(P_N)] \le \frac{2}{N} + \frac{2 k_{\rm max}^{2+1/k_{\rm max}}}{(k_{\rm max}-1)(2k_{\rm max}-1)}\frac{N^{1-1/k_{\rm max}}}{N-1} = O(N^{-1/k_{\rm max}}) \to 0$ ($k_{\rm max} \ge 2$), eliminating fixed-cutoff CSG from Screen 3. | `[PROVED THEOREM]` / `[COUNTEREXAMPLE/OBSTRUCTION]` | Exact discrete parent-path union bound over independent subset draws $B_m$ (Lemma 6.2(2)). |
| **Conjecture 7.3B** (Screen 3: Interior Transitive Comparability in Unbounded CSG) | Decaying-coupling CSG with unbounded coupling support concentrates transitive comparability inside $\epsilon < R_2(P_N) < 1 - \epsilon$ without global posts (`NG-02` Conjecture 5.3). | `[OPEN CONJECTURE]` | Fixed-cutoff CSG ruled out by Theorem 7.3B'; $t_k = c^k/k!$ drifts upward ($R_2(2000) = 0.8842$ at $c=1$, $0.9253$ at $c=2$). |
| **Theorem 8.1** (Full-Ideal Capping Lower Bound & Normalization-Covariance Dilemma) | Maximal-deletion compensation satisfies $\mathbb{E}[R_2(P_N)] \ge \frac{2}{N(N-1)}\sum_{n=1}^{N-1} n\,\mathbb{E}[1 - a_n\Sigma_u(P_n, \tilde{r}_n)]$, requiring $\mathbb{E}[a_n\Sigma_u] \ge 9/10$ on average to reach $R_2 = 1/10$, while stage-normalized $q_{\rm tilt}$ breaks covariance on $279/441$ ($63.3\%$) incomparable diamonds ($N \le 4$). | `[PROVED THEOREM]` / `[COUNTEREXAMPLE/OBSTRUCTION]` | Exact identity $C_1(P_N) = \sum_{n=1}^{N-1}\lvert S_n\rvert \ge \sum_{n=1}^{N-1} n\,\mathbf{1}_{\{S_n = P_n\}}$ and exhaustive $N \le 4$ diamond census. |
| **Conjecture 8.1** (Closed-Loop Curvature Attractor) | Local register feedback drives Lyapunov drift $\mathbb{E}[\Delta V \mid \mathcal{F}_n] \le -c V/n$ toward $\mathcal{M}_4^* = \{P : R_2 = 1/10, S_{\rm BD}^{(4)} = 0\}$ (`NG-02` Conjecture 5.5). | `[OPEN CONJECTURE]` | Pointwise negative drift verified across 100% of out-of-band posets ($N \le 6$); infinite-volume martingale concentration remains open. |

---

## 3. Mathematical Foundations: Poset Invariants and Sequential Growth

### 3.1 Poset Incidence Algebra, Chain Counts & Myrheim–Meyer Dimension
Let $P = (V, \prec)$ be a finite, partially ordered set (poset) of cardinality $\lvert V\rvert = N \ge 2$. We assume a natural topological labelling $V = \{0, 1, \dots, N-1\}$ such that $u \prec v \implies u < v$.

The causal order structure is fully encoded by the strict incidence matrix $C_P \in \{0, 1\}^{N \times N}$:
$$
(C_P)_{uv} = \begin{cases} 1 & \text{if } v \prec u, \\ 0 & \text{otherwise}. \end{cases}
$$
Under the topological sort, $C_P$ is strictly lower-triangular, ensuring that $(C_P)_{uv} = 0$ for all $u \le v$.

- **Chain Abundances**: For any integer $k \ge 1$, the total number of strict $k$-chains $v_0 \prec v_1 \prec \dots \prec v_k$ in $P$ is given by the matrix power sum:
  $$
  C_k(P) := \mathbf{1}^T C_P^k \mathbf{1} = \sum_{u=0}^{N-1} \sum_{v=0}^{N-1} (C_P^k)_{uv}.
  $$
- **Poset Height**: The height $h(P)$ is the length of the longest chain:
  $$
  h(P) := \max\{ k \ge 1 : C_k(P) > 0 \}.
  $$
  Strict nilpotency guarantees that $C_P^{h(P)+1} \equiv 0$ and $C_P^N \equiv 0$.
- **Successive Chain Ratios**:
  $$
  \rho_k(P) := \frac{C_{k+1}(P)}{C_k(P)} \quad (k \ge 1).
  $$
- **Intrinsic Myrheim–Meyer Comparable-Pair Fraction**:
  $$
  R_2(P) := \frac{C_1(P)}{\binom{N}{2}} = \frac{2\,\mathbf{1}^T C_P \mathbf{1}}{N(N-1)} \in [0, 1].
  $$
- **Continuum Alexandrov Comparison Function**: In flat $d$-dimensional Minkowski spacetime $\mathbb{M}^d$, the expected comparable-pair fraction of a Poisson sprinkling into an Alexandrov causal diamond is:
  $$
  f(d) := \frac{\Gamma(d+1)\,\Gamma(d/2)}{2\,\Gamma(3d/2)}.
  $$
  Evaluating $f(d)$ for low integer spacetime dimensions yields the exact rational sequence:
  $$
  f(1) = 1, \quad f(2) = \frac{1}{2}, \quad f(3) = \frac{8}{35} \approx 0.228571, \quad f(4) = \frac{1}{10} = 0.100000, \quad f(5) = \frac{128}{3003} \approx 0.042624.
  $$
  Because $f(d)$ is strictly monotonically decreasing ($f'(d) < 0$) on $[1, \infty)$, there exists a unique continuous inverse $f^{-1}: (0, 1] \to [1, \infty)$, providing the intrinsic dimension estimator:
  $$
  d(R_2(P)) := f^{-1}(R_2(P)).
  $$

### 3.2 Discrete Benincasa–Dowker Curvature Actions
For a finite causal set $P$, the discrete Benincasa–Dowker scalar curvature actions evaluate local interval layer abundances:
- Let $N_k(P)$ denote the number of pairs $(u, v)$ such that $u \prec v$ and the order interval $\langle u, v\rangle := \{z \in P : u \prec z \prec v\}$ has cardinality exactly $\lvert\langle u, v\rangle\rvert = k$.
- Note that $N_0(P)$ is the number of direct covering relations (links), while $C_1(P) = \sum_{k=0}^{N-2} N_k(P)$.
- The 2D Benincasa–Dowker action is:
  $$
  S_{\rm BD}^{(2)}(P) := N - 2 N_0(P) + 4 N_1(P) - 2 N_2(P).
  $$
- The 4D Benincasa–Dowker action is:
  $$
  S_{\rm BD}^{(4)}(P) := N - N_0(P) + 9 N_1(P) - 16 N_2(P) + 8 N_3(P).
  $$
  The curvature action discriminates sharply between geometric phases:
  - Linear chains ($C_N$): Intermediate elements accumulate in $N_1, N_2$, giving positive curvature $S_{\rm BD}^{(4)}(C_4) = +3 > 0$ (geodesic dispersion).
  - Causal diamonds ($E_{\rm diamond}$): Direct covering links dominate with empty interiors, giving negative curvature $S_{\rm BD}^{(4)}(E_{\rm diamond}) = -16 < 0$ (interval focusing).

### 3.3 Downward-Closed Ideals, Covering Links, and Growth Paths
In sequential growth, a causal set is formed by adjoining elements $x_0, x_1, x_2, \dots$ one at a time.
- At stage $n$, given the current parent poset $P_n$ of cardinality $n$, a newborn element $x_n$ chooses a subset $S_n \subseteq P_n$ to be its causal past.
- Transitivity of the causal order requires that $S_n$ be a **downward-closed ideal** ($S_n \in \mathcal{I}(P_n)$):
  $$
  u \in S_n \text{ and } v \prec u \implies v \in S_n.
  $$
- The causal past of the newborn vertex $x_n$ in the child poset $P_{n+1} = P_n \cup \{x_n\}$ is:
  $$
  J^-(x_n) := \{ u \in P_{n+1} : u \preceq x_n \} = S_n \cup \{x_n\}.
  $$
- The set of immediate causal predecessors (covering relations or links) entering $x_n$ is the maximal antichain of $S_n$:
  $$
  \operatorname{Max}(S_n) := \{ m \in S_n : \nexists z \in S_n \text{ s.t. } m \prec z \}.
  $$
  The link in-degree of the newborn vertex is $\operatorname{deg}_{\rm in}(x_n) = \lvert\operatorname{Max}(S_n)\rvert$.

### 3.4 Discrete General Covariance & The Scalar Diamond Commutation Identity
Discrete General Covariance is the causal set counterpart of diffeomorphism invariance: the physical probability of obtaining a given unlabeled causal set must not depend on the arbitrary labeling or birth order in which its elements were adjoined.

Consider a base poset $C$ of cardinality $n-1$, and let $S, T \in \mathcal{I}(C)$ be two downward-closed ideals.
Two newborn elements $x$ (with past $S$) and $y$ (with past $T$) can be adjoined in either order:
- **Path 1**: $x_S$ is born at step $n$ with past $S \subseteq C$, yielding intermediate poset $C + x_S$. Then $y_T$ is born at step $n+1$ with past $T \subseteq C$, yielding $(C + x_S) + y_T$.
- **Path 2**: $y_T$ is born at step $n$ with past $T \subseteq C$, yielding intermediate poset $C + y_T$. Then $x_S$ is born at step $n+1$ with past $S \subseteq C$, yielding $(C + y_T) + x_S$.

Because $x \notin C \implies x \notin T$ and $y \notin C \implies y \notin S$, the elements $x$ and $y$ are mutually incomparable ($x \parallel y$). The two growth paths terminate at the identical child poset:
$$
(C + x_S) + y_T \cong (C + y_T) + x_S =: C + x_S + y_T.
$$
**Discrete General Covariance** requires that the path transition probabilities commute identically:
$$
\Pi_1(S, T) = \Pi_2(T, S) \iff q_n(C, S)\,q_{n+1}(C + x_S, T) = q_n(C, T)\,q_{n+1}(C + y_T, S).
$$
This fundamental equality is the **scalar diamond commutation identity**.

---

## 4. Analysis and Proof of Proposition 5.5: Single-History Bifurcation

### 4.1 Quantum Carrier Setup & Kraus Channel Representation
Let $(\Omega_\infty, \mathcal{F}_\infty)$ denote the measurable space of infinite causal set histories $\omega = (P_1, P_2, \dots)$.
Consider a two-level horizon quantum carrier $\mathcal{H}_{\rm hor} = \mathbb{C}^2$ initialized in a static, unmeasured density operator $\rho \in \mathcal{D}(\mathcal{H}_{\rm hor})$ with coherence parameter:
$$
\langle X\rangle = \operatorname{Tr}[X\rho] \in [-1, 1], \qquad \text{where } X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}.
$$
Let $\{ \lvert +\rangle, \lvert -\rangle \}$ be the eigenbasis of $X$, so that $\rho$ has diagonal elements:
$$
p_+ = \langle +|\rho|+\rangle = \frac{1 + \langle X\rangle}{2}, \qquad p_- = \langle -|\rho|-\rangle = \frac{1 - \langle X\rangle}{2}.
$$
Let $q^{(+)}(P, S)$ and $q^{(-)}(P, S)$ be two distinct classical sequential growth kernels satisfying strict positivity and diamond commutation.
As established in `PW2-A` (Theorem 5), the coherent Kraus operators for the growth step are:
$$
K_{S, b}^{P, r} = \frac{1}{\sqrt{2}}\left( \sqrt{q^{(+)}(P, r, S)}\,e^{-i\varphi_{K, b}^{(+)}/2}\lvert +\rangle\langle +\rvert + \sqrt{q^{(-)}(P, r, S)}\,e^{-i\varphi_{K, b}^{(-)}/2}\lvert -\rangle\langle -\rvert \right).
$$
Because the Kraus operators $K_{S, b}^{P, r}$ are strictly diagonal in the $\{ \lvert +\rangle, \lvert -\rangle \}$ basis for every parent poset $P$, precursor ideal $S$, and newborn mark $b$, the carrier state $\rho$ undergoes zero off-diagonal basis rotation across sequential births.
Consequently, the cylinder measure on infinite histories decomposes as an exact convex mixture:
$$
\mathbb{P}_{\infty, \rho} = p_+ \mathbb{P}_\infty^{(+)} + p_- \mathbb{P}_\infty^{(-)} = \frac{1 + \langle X\rangle}{2}\mathbb{P}_\infty^{(+)} + \frac{1 - \langle X\rangle}{2}\mathbb{P}_\infty^{(-)}.
$$

### 4.2 Proof of Bimodal Asymptotic Distribution Along Single Histories

**Theorem 4.1 (`[PROVED THEOREM]` Single-History Extremal Branch Bifurcation).**  
*Let the extremal kernels $q^{(+)}$ (dense/focusing) and $q^{(-)}$ (sparse/branching) possess distinct, well-defined almost sure asymptotic comparable-pair fractions:*
$$
R_2(P_N) \xrightarrow{N \to \infty} R_2^{(+)} \quad \mathbb{P}_\infty^{(+)}\text{-a.s.}, \qquad R_2(P_N) \xrightarrow{N \to \infty} R_2^{(-)} \quad \mathbb{P}_\infty^{(-)}\text{-a.s.},
$$
*with $0 \le R_2^{(-)} < R_2^{(+)} \le 1$. Then along almost every realized single history $\omega = (P_1, P_2, \dots) \in \Omega_\infty$, the observable $R_2(P_N(\omega))$ converges to the discrete two-point set $\{R_2^{(+)}, R_2^{(-)}\}$, sampling the extremal branches with fixed probabilities:*
$$
\mathbb{P}_{\infty, \rho}\left(\lim_{N \to \infty} R_2(P_N) = R_2^{(+)}\right) = \frac{1 + \langle X\rangle}{2}, \qquad \mathbb{P}_{\infty, \rho}\left(\lim_{N \to \infty} R_2(P_N) = R_2^{(-)}\right) = \frac{1 - \langle X\rangle}{2}.
$$

*Proof.*  
Define the tail events in $\mathcal{F}_\infty$:
$$
E_+ := \left\{ \omega \in \Omega_\infty : \lim_{N \to \infty} R_2(P_N(\omega)) = R_2^{(+)} \right\}, \qquad E_- := \left\{ \omega \in \Omega_\infty : \lim_{N \to \infty} R_2(P_N(\omega)) = R_2^{(-)} \right\}.
$$
Because $R_2^{(-)} < R_2^{(+)}$, the limit values are distinct, so the sets $E_+$ and $E_-$ are disjoint: $E_+ \cap E_- = \varnothing$.
By hypothesis, under the extremal measure $\mathbb{P}_\infty^{(+)}$, the history converges almost surely to $R_2^{(+)}$, which means $\mathbb{P}_\infty^{(+)}(E_+) = 1$ and $\mathbb{P}_\infty^{(+)}(E_-) = 0$.
Symmetrically, under the extremal measure $\mathbb{P}_\infty^{(-)}$, the history converges almost surely to $R_2^{(-)}$, which means $\mathbb{P}_\infty^{(-)}(E_-) = 1$ and $\mathbb{P}_\infty^{(-)}(E_+) = 0$.
Evaluating the mixture probability measure $\mathbb{P}_{\infty, \rho} = p_+ \mathbb{P}_\infty^{(+)} + p_- \mathbb{P}_\infty^{(-)}$ on these events:
$$
\mathbb{P}_{\infty, \rho}(E_+) = p_+ \mathbb{P}_\infty^{(+)}(E_+) + p_- \mathbb{P}_\infty^{(-)}(E_+) = p_+ \cdot 1 + p_- \cdot 0 = p_+ = \frac{1 + \langle X\rangle}{2}.
$$
Similarly:
$$
\mathbb{P}_{\infty, \rho}(E_-) = p_+ \mathbb{P}_\infty^{(+)}(E_-) + p_- \mathbb{P}_\infty^{(-)}(E_-) = p_+ \cdot 0 + p_- \cdot 1 = p_- = \frac{1 - \langle X\rangle}{2}.
$$
Furthermore, $\mathbb{P}_{\infty, \rho}(E_+ \cup E_-) = p_+ + p_- = 1$. Thus, along almost every individual history $\omega$, $R_2(P_N(\omega))$ converges to either $R_2^{(+)}$ or $R_2^{(-)}$. $\blacksquare$

### 4.3 Proof of Absence of Concentration at the Ensemble Mean

**Theorem 4.2 (`[PROVED THEOREM]` Absence of Concentration at Ensemble Mean).**  
*For any mixed coherence $\langle X\rangle \in (-1, 1)$, the single-history observable $R_2(P_N)$ almost surely fails to concentrate at the ensemble expectation value $\mathbb{E}_\rho[R_2(P_N)]$. Specifically, for any tolerance:*
$$
0 < \epsilon < \frac{1}{2}\min\left\{ \mathbb{E}_\rho[R_2] - R_2^{(-)}, \, R_2^{(+)} - \mathbb{E}_\rho[R_2] \right\},
$$
*the probability that a single history enters the $\epsilon$-neighborhood of the ensemble mean vanishes asymptotically:*
$$
\lim_{N \to \infty} \mathbb{P}_{\infty, \rho}\left( \left\lvert R_2(P_N) - \mathbb{E}_\rho[R_2(P_N)] \right\rvert \le \epsilon \right) = 0 \iff \lim_{N \to \infty} \mathbb{P}_{\infty, \rho}\left( \left\lvert R_2(P_N) - \mathbb{E}_\rho[R_2(P_N)] \right\rvert > \epsilon \right) = 1.
$$

*Proof.*  
The ensemble expectation value under the mixture measure is:
$$
\mathbb{E}_\rho[R_2(P_N)] = p_+ \mathbb{E}^{(+)}[R_2(P_N)] + p_- \mathbb{E}^{(-)}[R_2(P_N)].
$$
Taking the asymptotic limit as $N \to \infty$:
$$
\lim_{N \to \infty} \mathbb{E}_\rho[R_2(P_N)] = p_+ R_2^{(+)} + p_- R_2^{(-)} =: R_2^{(\rho)}.
$$
Because $\langle X\rangle \in (-1, 1)$, both weights are strictly positive: $p_+ > 0$ and $p_- > 0$. Since $R_2^{(-)} < R_2^{(+)}$, the convex combination lies strictly in the interior:
$$
R_2^{(-)} < R_2^{(\rho)} < R_2^{(+)}.
$$
Define the distances from the ensemble limit to the extremal points:
$$
\delta_- := R_2^{(\rho)} - R_2^{(-)} = p_+ (R_2^{(+)} - R_2^{(-)}) > 0, \qquad \delta_+ := R_2^{(+)} - R_2^{(\rho)} = p_- (R_2^{(+)} - R_2^{(-)}) > 0.
$$
Let $\epsilon_0 := \min\{\delta_-, \delta_+\} = \min\{p_+, p_-\}(R_2^{(+)} - R_2^{(-)}) > 0$.
For any chosen tolerance $\epsilon \in (0, \epsilon_0)$, the closed interval $I_\epsilon := [R_2^{(\rho)} - \epsilon, R_2^{(\rho)} + \epsilon]$ is at a strictly positive distance from both $R_2^{(+)}$ and $R_2^{(-)}$:
$$
\operatorname{dist}(I_\epsilon, R_2^{(+)}) \ge \delta_+ - \epsilon > 0, \qquad \operatorname{dist}(I_\epsilon, R_2^{(-)}) \ge \delta_- - \epsilon > 0.
$$
Therefore, neither $R_2^{(+)}$ nor $R_2^{(-)}$ is contained in $I_\epsilon$.
On the event $E_+$, $\lim_{N \to \infty} R_2(P_N) = R_2^{(+)} \notin I_\epsilon$, so there exists $N_0(\omega)$ such that $R_2(P_N(\omega)) \notin I_\epsilon$ for all $N \ge N_0(\omega)$. Hence $\mathbf{1}_{\{R_2(P_N) \in I_\epsilon\}} \to 0$ pointwise on $E_+$.
Similarly, on $E_-$, $\lim_{N \to \infty} R_2(P_N) = R_2^{(-)} \notin I_\epsilon$, so $\mathbf{1}_{\{R_2(P_N) \in I_\epsilon\}} \to 0$ pointwise on $E_-$.
Since $\mathbb{P}_{\infty, \rho}(E_+ \cup E_-) = 1$, by the Dominated Convergence Theorem:
$$
\lim_{N \to \infty} \mathbb{P}_{\infty, \rho}\left( R_2(P_N) \in I_\epsilon \right) = \int_{E_+ \cup E_-} \lim_{N \to \infty} \mathbf{1}_{\{R_2(P_N) \in I_\epsilon\}} \, d\mathbb{P}_{\infty, \rho} = 0.
$$
Taking the complement yields $\lim_{N \to \infty} \mathbb{P}_{\infty, \rho}(\lvert R_2(P_N) - R_2^{(\rho)}\rvert > \epsilon) = 1$. $\blacksquare$

### 4.4 Exact Variance and Bimodality Coefficient Derivations

The failure of concentration is quantitatively characterized by the non-vanishing asymptotic variance and bimodality coefficient:
1. **Asymptotic Variance**:
   $$
   \operatorname{Var}_\rho[R_2(P_N)] = \mathbb{E}_\rho\left[ (R_2(P_N) - \mathbb{E}_\rho[R_2(P_N)])^2 \right].
   $$
   Expanding under the mixture measure:
   $$
   \lim_{N \to \infty} \operatorname{Var}_\rho[R_2(P_N)] = p_+ (R_2^{(+)} - R_2^{(\rho)})^2 + p_- (R_2^{(-)} - R_2^{(\rho)})^2.
   $$
   Substituting $R_2^{(+)} - R_2^{(\rho)} = p_- (R_2^{(+)} - R_2^{(-)})$ and $R_2^{(-)} - R_2^{(\rho)} = -p_+ (R_2^{(+)} - R_2^{(-)})$:
   $$
   \lim_{N \to \infty} \operatorname{Var}_\rho[R_2(P_N)] = p_+ p_-^2 (\Delta R_2)^2 + p_- p_+^2 (\Delta R_2)^2 = p_+ p_- (\Delta R_2)^2 = \frac{1 - \langle X\rangle^2}{4}(R_2^{(+)} - R_2^{(-)})^2.
   $$
   For any mixed state $\langle X\rangle \in (-1, 1)$, this asymptotic variance is strictly positive:
   $$
   \lim_{N \to \infty} \operatorname{Var}_\rho[R_2(P_N)] > 0.
   $$
2. **Sarle's Bimodality Coefficient**:
   For any random variable $Y$ with skewness $\gamma_1 = m_3 / \sigma^3$ and kurtosis $\beta_2 = m_4 / \sigma^4$, Sarle's bimodality coefficient is:
   $$
   b := \frac{\gamma_1^2 + 1}{\beta_2} = \frac{m_3^2 + \sigma^6}{m_4 \sigma^2}.
   $$
   For any discrete two-point distribution with values $R_2^{(\pm)}$ and probabilities $p_\pm \in (0, 1)$ ($p_+ + p_- = 1$), the central moments satisfy:
   $$
   \sigma^2 = p_+ p_- (\Delta R_2)^2, \quad \gamma_1^2 + 1 = \frac{1 - 3p_+ p_-}{p_+ p_-}, \quad \beta_2 = \frac{1 - 3p_+ p_-}{p_+ p_-}.
   $$
   Because Pearson's inequality $\beta_2 \ge \gamma_1^2 + 1$ is saturated as an exact identity $\beta_2 \equiv \gamma_1^2 + 1$ for any discrete two-point measure, Sarle's bimodality coefficient satisfies:
   $$
   b := \frac{\gamma_1^2 + 1}{\beta_2} \equiv 1.0000 \quad \text{identically for the idealized two-point distribution.}
   $$
   In any physical realization or numerical simulation with small finite intra-branch Gaussian variance $\sigma_N \approx 0.005 > 0$ due to finite-size fluctuations (as evaluated in Check 8 of the master suite), Sarle's coefficient evaluates to:
   $$
   b \approx 0.9810 > \frac{5}{9} \approx 0.5556.
   $$
   Because the uniform distribution has $b_{\rm unif} = 5/9 \approx 0.5556$, any value $b > 5/9$ indicates extreme bimodality; here $b \approx 0.9810 \gg 0.5556$ rigorously confirms the bimodal bifurcation into the two extremal branches.

### 4.5 Physical Consequence: Failure of Static Quantum Steering for a Single Universe
Theorem 5.4 of `NG-02` proved that by setting the probe coherence to the critical target value:
$$
\langle X\rangle_* := \frac{2/10 - (R_2^{(+)} + R_2^{(-)})}{R_2^{(+)} - R_2^{(-)}} \in (-1, 1),
$$
the ensemble-averaged comparable-pair fraction is steered precisely to:
$$
\lim_{N \to \infty} \mathbb{E}_{\rho_*}[R_2(P_N)] = \frac{1}{10} = f(4) \implies d_{\rm eff}(\rho_*, \infty) = 4.0.
$$
However, Proposition 5.5 and Theorems 4.1–4.2 demonstrate that:
**An individual causal set history almost surely NEVER stabilizes at $d(R_2) = 4.0$.**
Instead, the physical universe realizes:
- An overly dense, collapsed spacetime with dimension $d^{(+)} = f^{-1}(R_2^{(+)})$ with probability $\frac{1+\langle X\rangle_*}{2}$; OR
- An overly sparse, fragmented spacetime with dimension $d^{(-)} = f^{-1}(R_2^{(-)})$ with probability $\frac{1-\langle X\rangle_*}{2}$.

Therefore, **static quantum steering cannot produce a four-dimensional spacetime on a single history**. Single-history stabilization requires active, adaptive, closed-loop feedback across births.

---

## 5. The Covariance No-Go Theorems & Local Past-Record Register Architecture

### 5.1 Theorem 5.1: The Markovian Global Stage-Slice Feedback Obstruction

**Theorem 5.1 (`[COUNTEREXAMPLE/OBSTRUCTION]` Markovian Global Feedback Covariance Obstruction).**  
*Let $(P_n)_{n \ge 1}$ be a sequential growth process. Any ad-hoc Markovian growth transition rule in which the transition probability at step $n+1$ conditions on global stage-slice observables of the intermediate parent poset $P_{n+1}$ (such as $R_2(P_{n+1})$ or $S_{\rm BD}^{(4)}(P_{n+1})$) violates Discrete General Covariance.*

*Proof.*  
Let $C$ be a base poset of cardinality $n-1$, and let $S, T \in \mathcal{I}(C)$ be two downward-closed ideals of $C$ with unequal cardinalities: $\lvert S\rvert \ne \lvert T\rvert$.
Consider the two growth paths connecting $C$ to $C + x_S + y_T$:
- Path 1 creates intermediate poset $P^{(1)} = C + x_S$ at step $n$, then adjoins $y_T$ at step $n+1$.
- Path 2 creates intermediate poset $P^{(2)} = C + y_T$ at step $n$, then adjoins $x_S$ at step $n+1$.

Let us evaluate the total number of comparable pairs in the intermediate posets:
In Path 1, $x_S$ is added above exactly the elements of $S \subseteq C$:
$$
C_1(C + x_S) = C_1(C) + \lvert S\rvert.
$$
In Path 2, $y_T$ is added above exactly the elements of $T \subseteq C$:
$$
C_1(C + y_T) = C_1(C) + \lvert T\rvert.
$$
Dividing by the total number of pairs $\binom{n}{2}$ in an $n$-element poset:
$$
R_2(C + x_S) - R_2(C + y_T) = \frac{\lvert S\rvert - \lvert T\rvert}{\binom{n}{2}} \ne 0.
$$
Because $\lvert S\rvert \ne \lvert T\rvert$, the global observable $R_2$ takes different values in the two intermediate posets:
$$
R_2(C + x_S) \ne R_2(C + y_T).
$$
Now, suppose the transition probability at step $n+1$ is conditioned on the global $R_2$ of the parent poset via some function $g$:
$$
q_{n+1}(P, U) = F(P, U; R_2(P)).
$$
Then the probability of adjoining $y_T$ along Path 1 is $F(C + x_S, T; R_2(C + x_S))$, while the probability of adjoining $x_S$ along Path 2 is $F(C + y_T, S; R_2(C + y_T))$.
The diamond path probability ratio is:
$$
\frac{\Pi_1(S, T)}{\Pi_2(T, S)} = \frac{q_n(C, S)\,F(C + x_S, T; R_2(C + x_S))}{q_n(C, T)\,F(C + y_T, S; R_2(C + y_T))}.
$$
Unless $F(P, U; R_2(P))$ is independent of $R_2(P)$, this ratio varies with $\lvert S\rvert - \lvert T\rvert$ and is generically not equal to 1.
An identical discrepancy arises for the 4D Benincasa–Dowker curvature action:
$$
S_{\rm BD}^{(4)}(C + x_S) \ne S_{\rm BD}^{(4)}(C + y_T).
$$
Therefore, global stage-slice feedback breaks scalar diamond commutation $\Pi_1 = \Pi_2$, violating Discrete General Covariance. $\blacksquare$

*Remark 5.1 (Separation from Covariant de Finetti Mixtures).*  
Theorem 5.1 must not be confused with covariant de Finetti mixture processes. In causal set theory (Rideout & Sorkin 1999), a sequential growth process can be expressed as a mixture over pure CSG coupling vectors: $\mathbb{P}_\mu = \int \mathbb{P}_t\,d\mu(t)$. Conditioned on an observed finite history $P_n$, the effective transition probability $q_\mu(P_n, S) = \int q_t(P_n, S)\,d\mu(t \mid P_n)$ depends on the global history $P_n$ through the Bayesian posterior $d\mu(t \mid P_n) \propto \mathbb{P}_t(P_n)\,d\mu(t)$. Nevertheless, $\mathbb{P}_\mu$ satisfies exact diamond commutation $\Pi_1(S, T) = \int \Pi_{1, t}(S, T)\,d\mu(t) = \int \Pi_{2, t}(T, S)\,d\mu(t) = \Pi_2(T, S)$ because every constituent CSG measure $\mathbb{P}_t$ is discrete generally covariant. The covariance obstruction in Theorem 5.1 arises specifically when transition probabilities are modified by ad-hoc Markovian functions of slice observables $R_2(P_n)$ that do not originate from a legitimate de Finetti mixture measure.

### 5.2 Theorem 5.2: Monolithic Quantum Carrier Non-Commutation & Path Dependence

**Theorem 5.2 (`[COUNTEREXAMPLE/OBSTRUCTION]` Monolithic Carrier Path Dependence & Gauge Obstruction).**  
*Let sequential growth be steered by a single, monolithic quantum carrier state $\rho \in \mathcal{D}(\mathcal{H})$. If the carrier is updated dynamically after each birth step based on branch-selected measurement outcomes: $\rho_{n+1} = \mathcal{J}_{x_n, S}(\rho_n)/\operatorname{Tr}[\mathcal{J}_{x_n, S}(\rho_n)]$, then the physical path probabilities violate Discrete General Covariance ($\Pi_1(S, T) \ne \Pi_2(T, S)$), and the quantum state assigned to identical posets becomes path-dependent ($\rho_{n+1}^{(1)} \ne \rho_{n+1}^{(2)}$). However, such path-order non-commutation and post-selection correlation do not constitute operational channel-level spacelike signaling unless the non-selective CPTP map $\mathcal{E}_x = \sum_S \mathcal{J}_{x_S}$ alters the unconditioned marginal distribution at spacelike separated $y$.*

*Proof.*  
Consider the base poset $C$ and two incomparable ideals $S, T \in \mathcal{I}(C)$. The newborn vertices $x_S$ and $y_T$ are spacelike separated ($x \parallel y$).
- In Path 1, $x_S$ is adjoined first, updating the carrier state from $\rho_n$ to $\rho_{n+1}^{(1)} = \mathcal{J}_{x_S}(\rho_n)/\operatorname{Tr}[\mathcal{J}_{x_S}(\rho_n)]$. Then $y_T$ is adjoined, sampling from carrier state $\rho_{n+1}^{(1)}$ with transition probability $\operatorname{Tr}[M_T \rho_{n+1}^{(1)}]$.
- In Path 2, $y_T$ is adjoined first, updating the carrier state from $\rho_n$ to $\rho_{n+1}^{(2)} = \mathcal{J}_{y_T}(\rho_n)/\operatorname{Tr}[\mathcal{J}_{y_T}(\rho_n)]$. Then $x_S$ is adjoined, sampling from carrier state $\rho_{n+1}^{(2)}$ with transition probability $\operatorname{Tr}[M_S \rho_{n+1}^{(2)}]$.

The path probabilities are:
$$
\Pi_1(S, T) = \operatorname{Tr}[\mathcal{J}_{x_S}(\rho_n)] \cdot \frac{\operatorname{Tr}[M_T \mathcal{J}_{x_S}(\rho_n)]}{\operatorname{Tr}[\mathcal{J}_{x_S}(\rho_n)]} = \operatorname{Tr}[M_T \mathcal{J}_{x_S}(\rho_n)],
$$
$$
\Pi_2(T, S) = \operatorname{Tr}[\mathcal{J}_{y_T}(\rho_n)] \cdot \frac{\operatorname{Tr}[M_S \mathcal{J}_{y_T}(\rho_n)]}{\operatorname{Tr}[\mathcal{J}_{y_T}(\rho_n)]} = \operatorname{Tr}[M_S \mathcal{J}_{y_T}(\rho_n)].
$$
For $\Pi_1 = \Pi_2$ to hold for all choices of measurement operators and ideals, the quantum operations must satisfy:
$$
\operatorname{Tr}[M_T \mathcal{J}_{x_S}(\rho_n)] = \operatorname{Tr}[M_S \mathcal{J}_{y_T}(\rho_n)].
$$
When operations fail to commute, $\Pi_1(S, T) \ne \Pi_2(T, S)$ and $\rho_{n+1}^{(1)} \ne \rho_{n+1}^{(2)}$.

Crucially, we must distinguish between gauge path-dependence and operational spacelike signaling:
1. *Diamond Path Gauge-Dependence:* $\Pi_1(S, T) \ne \Pi_2(T, S)$ means that the labelling sequence in the causal set cannot be freely relabelled without altering the history weights. The sequential growth process is not discrete generally covariant.
2. *Operational Microcausality & No-Signaling:* Operational signaling requires that an action at $x$ transmit information to spacelike-separated $y$ in the absence of post-selection. The non-selective quantum channel implemented at birth $x$ is:
$$
\mathcal{E}_x(\rho) = \sum_{S \in \mathcal{I}(C)} \mathcal{J}_{x_S}(\rho).
$$
Under standard quantum mechanics, if the dual Heisenberg-picture channel satisfies $\mathcal{E}_x^\dagger(M_y) = M_y$ for all spacelike observables $M_y$ (for instance, when the Kraus operators of $\mathcal{E}_x$ commute with $M_y$ and satisfy $\sum_S K_{x_S}^\dagger K_{x_S} = I$), the unconditioned marginal statistics at $y$ are independent of whether birth $x$ occurred: $\operatorname{Tr}[M_y \mathcal{E}_x(\rho)] = \operatorname{Tr}[\mathcal{E}_x^\dagger(M_y)\rho] = \operatorname{Tr}[M_y \rho]$. Post-selecting on a specific outcome $S$ at $x$ establishes conditional branch correlations, but does not constitute operational signaling because an observer at $y$ cannot determine which branch $S$ was realized without subluminal classical communication. Therefore, monolithic carrier steering represents a gauge covariance defect and path dependence rather than an operational violation of relativistic causality. $\blacksquare$

### 5.3 Theorem 5.3: The Stage-Normalized Precursor Feedback Partition-Function Obstruction

**Theorem 5.3 (`[COUNTEREXAMPLE/OBSTRUCTION]` Precursor Feedback Partition-Function Obstruction).**  
*Let the unnormalized transition weight $\tilde{q}(P, S) = w(S)$ depend strictly on intrinsic invariants of the precursor ideal $(S, \prec|_S)$, and let physical probabilities be normalized by the stage partition function:*
$$
q(P, S) = \frac{w(S)}{Z(P)}, \qquad Z(P) := \sum_{S' \in \mathcal{I}(P)} w(S').
$$
*Then $q(P, S)$ satisfies the scalar diamond commutation identity $\Pi_1 = \Pi_2$ if and only if the partition function $Z(P)$ depends solely on the cardinality $N = \lvert P\rvert$. For generic precursor weights $w(S)$ (including uniform ideal picking $w(S) \equiv 1$), $Z(C + x_S) \ne Z(C + y_T)$ whenever $\lvert S\rvert \ne \lvert T\rvert$, breaking Discrete General Covariance.*

*Proof.*  
Let $C$ be a base poset of cardinality $n-1$, and let $S, T \in \mathcal{I}(C)$.
Along Path 1 ($x_S$ then $y_T$):
$$
\Pi_1(S, T) = q_n(C, S)\,q_{n+1}(C + x_S, T) = \frac{w(S)}{Z(C)} \cdot \frac{w(T)}{Z(C + x_S)}.
$$
Along Path 2 ($y_T$ then $x_S$):
$$
\Pi_2(T, S) = q_n(C, T)\,q_{n+1}(C + y_T, S) = \frac{w(T)}{Z(C)} \cdot \frac{w(S)}{Z(C + y_T)}.
$$
Equating $\Pi_1(S, T) = \Pi_2(T, S)$:
$$
\frac{w(S)\,w(T)}{Z(C)\,Z(C + x_S)} = \frac{w(T)\,w(S)}{Z(C)\,Z(C + y_T)} \iff Z(C + x_S) = Z(C + y_T).
$$
Thus, diamond commutation holds if and only if $Z(C + x_S) = Z(C + y_T)$ for all pairs of ideals $S, T \in \mathcal{I}(C)$.

Now consider the ideal lattice of the child poset.
Any ideal of $C + x_S$ either does not contain $x_S$ (in which case it is an ideal of $C$), or contains $x_S$ (in which case it must contain $J^-(x_S) \setminus \{x_S\} = S$). Therefore:
$$
\mathcal{I}(C + x_S) = \mathcal{I}(C) \cup \{ U \cup \{x_S\} : S \subseteq U \in \mathcal{I}(C) \}.
$$
Summing the weights over this union:
$$
Z(C + x_S) = \sum_{U \in \mathcal{I}(C)} w(U) + \sum_{S \subseteq U \in \mathcal{I}(C)} w(U \cup \{x_S\}) = Z(C) + \sum_{S \subseteq U \in \mathcal{I}(C)} w(U \cup \{x_S\}).
$$
The second sum runs strictly over the ideals of $C$ that contain $S$ as a sub-ideal.
If $\lvert S\rvert \ne \lvert T\rvert$, the number of ideals containing $S$ is in general strictly different from the number of ideals containing $T$.

#### Concrete Analytic Counterexample: 2-Antichain Base Poset $A_2$
Let $C = A_2 = \{a, b\}$ be a two-element antichain ($a \parallel b$), so $n-1 = 2$.
The downward-closed ideals of $A_2$ are:
$$
\mathcal{I}(A_2) = \{ \varnothing, \{a\}, \{b\}, \{a, b\} \}, \qquad \lvert\mathcal{I}(A_2)\rvert = 4.
$$
Consider the uniform precursor weight $w(S) \equiv 1$ (naive uniform ideal picking).
- Choose $S = \{a\}$ and $T = \varnothing$.
- In $C + x_S$, element $x$ is adjoined above $a$ ($a \prec x$, while $b \parallel x$).
  The ideals containing $S = \{a\}$ are $\{a\}$ and $\{a, b\}$.
  Hence the new ideals containing $x$ are $\{a, x\}$ and $\{a, b, x\}$.
  The total number of ideals of $C + x_S$ is:
  $$
  Z(C + x_S) = \lvert\mathcal{I}(C + x_S)\rvert = 4 + 2 = 6.
  $$
- In $C + y_T$, element $y$ is adjoined above $T = \varnothing$ ($y$ is disconnected, $y \parallel a, y \parallel b$).
  The ideals containing $T = \varnothing$ are all 4 ideals of $C$: $\varnothing, \{a\}, \{b\}, \{a, b\}$.
  Hence the new ideals containing $y$ are $\{y\}, \{a, y\}, \{b, y\}, \{a, b, y\}$.
  The total number of ideals of $C + y_T$ is:
  $$
  Z(C + y_T) = \lvert\mathcal{I}(C + y_T)\rvert = 4 + 4 = 8.
  $$

Comparing the partition sums:
$$
Z(C + x_S) = 6 \ne 8 = Z(C + y_T).
$$
The diamond path probability ratio evaluates to:
$$
\frac{\Pi_1(S, T)}{\Pi_2(T, S)} = \frac{Z(C + y_T)}{Z(C + x_S)} = \frac{8}{6} = \frac{4}{3} \ne 1.
$$
Path 1 has probability $\Pi_1 = \frac{1}{4} \cdot \frac{1}{6} = \frac{1}{24}$, while Path 2 has probability $\Pi_2 = \frac{1}{4} \cdot \frac{1}{8} = \frac{1}{32}$.
The ratio $\frac{1/24}{1/32} = \frac{32}{24} = \frac{4}{3} \ne 1$.
This explicit counterexample rigorously proves that naive stage normalization $w(S)/Z(P)$ destroys Discrete General Covariance. $\blacksquare$

**Corollary 5.3.1 (`[COUNTEREXAMPLE/OBSTRUCTION]` Obstruction to Stage-Normalized Register-Modulated CSG Couplings).**  
*Replacing universal Rideout–Sorkin constants $(t_k)_{k \ge 0}$ by register-modulated couplings $t_k(S, \mathcal{R}|_S)$ and normalizing by the stage partition sum $Z(P, \mathcal{R}) = \sum_{S' \in \mathcal{I}(P)} \tilde{q}(P, \mathcal{R}, S')$ also violates $Z(C+x_S, \mathcal{R}') = Z(C+y_T, \mathcal{R}'')$ and breaks Discrete General Covariance.*

*Proof.*  
On the marked 2-antichain $C = A_2 = \{a, b\}$ with $\mathcal{R}(a) = 0$ and $\mathcal{R}(b) = 1$, set $t_0 = 1$, $t_1(\mathcal{R}(m)) = 1 + \mathcal{R}(m)$ (so $t_1(0) = 1$ and $t_1(1) = 2$), and $t_k = 0$ for $k \ge 2$, with deterministic register propagation $\mathcal{R}(x) = 0$ for $S = \varnothing$ and $\mathcal{R}(x) = \max_{m \in \operatorname{Max}(S)} \mathcal{R}(m)$ for $S \ne \varnothing$. On $A_2$, the ideals $\varnothing, \{a\}, \{b\}, \{a, b\}$ have weights $1, 1, 2, 0$, so $Z(A_2, \mathcal{R}) = 4$. Comparing $S = \{b\}$ ($\mathcal{R}(x) = 1$) against $T = \varnothing$ ($\mathcal{R}(y) = 0$):
- In $A_2 + x_{\{b\}}$, the only new non-zero-weight ideal containing $x$ is $\{b, x\}$ ($\operatorname{Max} = \{x\}, d = 1$), contributing $t_1(\mathcal{R}(x)) = t_1(1) = 2$, so $Z(A_2 + x_{\{b\}}, \mathcal{R}') = 4 + 2 = 6$.
- In $A_2 + y_\varnothing$, the only new non-zero-weight ideal containing $y$ is $\{y\}$ ($\operatorname{Max} = \{y\}, d = 1$), contributing $t_1(\mathcal{R}(y)) = t_1(0) = 1$, so $Z(A_2 + y_\varnothing, \mathcal{R}'') = 4 + 1 = 5$.

Thus $Z(A_2 + x_{\{b\}}, \mathcal{R}') = 6 \ne 5 = Z(A_2 + y_\varnothing, \mathcal{R}'')$ and $\Pi_1(\{b\}, \varnothing)/\Pi_2(\varnothing, \{b\}) = 5/6 \ne 1$ (whereas constant $t_1 \equiv 1$ satisfies $Z = 4 = 4$). The Rideout–Sorkin identity $Z(P_n) = \alpha_n$ holds only for universal constants $(t_k)_{k \ge 0}$. $\blacksquare$

### 5.4 Theorem 5.4: Construction & Covariance Proof of the Local Past-Record Register $\mathcal{R}(v)$

**Theorem 5.4 (`[PROVED THEOREM]` Local Past-Record Register Covariance & Compensated Growth Coupling).**  
*Let each vertex $v \in V$ carry a localized past-record register $\mathcal{R}(v) \in \mathcal{X}$ (finite or measurable state space). When a newborn vertex $x$ is adjoined with precursor ideal $S$, its register $\mathcal{R}(x)$ is synthesized exclusively by a deterministic or Markovian aggregation map $\mathcal{A}$ acting on the causal past $(S, \prec|_S, \mathcal{R}|_S)$ (in particular, along incoming covering links):*
$$
\mathcal{R}(x) = \mathcal{A}\left( \{ \mathcal{R}(m) : m \in \operatorname{Max}(S) \} \right).
$$
*Then:*
1. *Causal Localization: For any two spacelike-separated births $x_S \parallel y_T$ extending base poset $C$, the registers $\mathcal{R}(x)$ and $\mathcal{R}(y)$ evaluate identically regardless of whether $x$ or $y$ is adjoined first:*
   $$
   \mathcal{R}(x)_{C + y_T} \equiv \mathcal{R}(x)_C, \qquad \mathcal{R}(y)_{C + x_S} \equiv \mathcal{R}(y)_C.
   $$
2. *Acausal Signaling Elimination: Under any unmodulated covariant structural kernel (or compensated kernel in Part 3), the marginal register-and-birth distribution at $y_T$ is statistically independent of the spacelike birth $x_S$, eliminating all acausal spacelike signaling.*
3. *Exact Covariant Register-to-Order Coupling via Maximal-Deletion Full-Ideal Compensation: Let $\tilde{r}_v := (r_v, \mathcal{R}(v)) \in \tilde{\mathcal{X}}$ be the combined append-only local vertex record on a finite discrete alphabet $\tilde{\mathcal{X}}$, initialized by any strictly positive seed prefix $q(P, \tilde{r}, S) > 0$ ($\lvert P\rvert \le n_0$) satisfying complete-row normalization, proper-slot locality ($q(P, \tilde{r}, S)$ depends on $\tilde{r}$ solely through $\tilde{r}|_S$ for $S \subsetneq P$), relabeling equivariance, and scalar diamond commutation on bases $\lvert C\rvert \le n_0 - 1$. Defining recursively for $\lvert P\rvert = n \ge n_0 + 1$ ($M := \operatorname{Max}(P)\setminus S$):*
   $$
   u(P, \tilde{r}, S) := \prod_{\varnothing \ne A \subseteq M} q\left(P\setminus A, \, \tilde{r}|_{P\setminus A}, \, S\right)^{(-1)^{\lvert A\rvert + 1}} \quad (S \subsetneq P),
   $$
   $$
   q(P, \tilde{r}, S) := a_n\,u(P, \tilde{r}, S) \quad (S \subsetneq P), \qquad q(P, \tilde{r}, P) := 1 - a_n \sum_{S \subsetneq P} u(P, \tilde{r}, S),
   $$
   *for any scale sequence $0 < a_n < 1/M_n$ ($M_n := \max_{\lvert P\rvert = n, \tilde{r}} \sum_{S \subsetneq P} u(P, \tilde{r}, S)$), yields an exact complete-row normalized ($\sum_{S \subseteq P} q(P, \tilde{r}, S) = 1$), proper-slot register-local, Kolmogorov-projective sequential growth process satisfying exact diamond commutation across all incomparable births:*
   $$
   q(C, \tilde{r}, S)\,q(C + x_S, \tilde{r} + \tilde{r}_x, T) = q(C, \tilde{r}, T)\,q(C + y_T, \tilde{r} + \tilde{r}_y, S) \quad \forall S, T \subseteq C.
   $$

*Proof.*  
1. Let $C$ be the base poset with assigned registers $\{\mathcal{R}(u) : u \in C\}$. When $x_S$ is adjoined along Path 1, $S \subseteq C$ and $\operatorname{Max}_C(S) \subseteq C$, giving $\mathcal{R}(x) = \mathcal{A}(\{\mathcal{R}(m) : m \in \operatorname{Max}_C(S)\})$. When $y_T$ ($T \subseteq C$) is adjoined at step $n+1$, $x \notin C \implies x \notin T$, so $(T, \prec|_{C + x_S}) \equiv (T, \prec|_C)$, $\operatorname{Max}_{C + x_S}(T) = \operatorname{Max}_C(T)$, and the existing registers on $T$ are untouched. Hence $\mathcal{R}(y)_{C + x_S} = \mathcal{A}(\{\mathcal{R}(m) : m \in \operatorname{Max}_C(T)\}) = \mathcal{R}(y)_C$, and symmetrically $\mathcal{R}(x)_{C + y_T} = \mathcal{R}(x)_C$.
2. Because $\mathcal{R}(y)_{C + x_S}$ depends solely on $\mathcal{R}|_T$ inside $C$, no register state at $y$ depends on $x_S$, eliminating acausal signaling across $x \parallel y$.
3. Unlike naive stage normalization $1/Z(P, \mathcal{R})$ (obstructed by Theorem 5.3 and Corollary 5.3.1), maximal-deletion compensation absorbs proper-ideal weight variations into the single full-ideal slot $S = P$. Notice that in Theorem 1 of `docs/observables/all_horizon_two_way_feedback_and_growth.md` (`PW2-A`), the inductive proof of proper-slot mark locality and exact ratio-diamond symmetry $q(C, \tilde{r}, S) u(C + x_S, \tilde{r} + \tilde{r}_x, T) = q(C, \tilde{r}, T) u(C + y_T, \tilde{r} + \tilde{r}_y, S)$ uses only that $\tilde{r}$ is an append-only vertex assignment whose newborn value $\tilde{r}_x$ does not alter $\tilde{r}|_C$, together with finiteness of $\tilde{\mathcal{X}}^n$ for $M_n < \infty$. Because $x_S \notin T \implies T \subsetneq C + x_S$ and $y_T \notin S \implies S \subsetneq C + y_T$ are both proper ideals of $n$-element parents, multiplying the ratio-diamond identity by $a_n$ yields $\Pi_1(S, T) = q(C, \tilde{r}, S) \cdot a_n u(C + x_S, \tilde{r} + \tilde{r}_x, T) = q(C, \tilde{r}, T) \cdot a_n u(C + y_T, \tilde{r} + \tilde{r}_y, S) = \Pi_2(T, S)$ identically. $\blacksquare$

---

## 6. Decaying-Coupling Classical Sequential Growth ($t_k = c/k!$)

### 6.1 Parameterization and Finite-Difference Representation of CSG Weights
In Classical Sequential Growth (Rideout & Sorkin 1999), the dynamic is parameterized by a sequence of non-negative constants $t_0, t_1, t_2, \dots$ with $t_0 > 0$.
The binomial transform constants $\alpha_m$ are defined by:
$$
\alpha_m := \sum_{k=0}^m \binom{m}{k} t_k \quad (m \ge 0).
$$
For a parent poset $P_n$ and precursor ideal $S \in \mathcal{I}(P_n)$, let:
$$
d := \lvert \operatorname{Max}(S) \rvert, \qquad p := \lvert S \setminus \operatorname{Max}(S) \rvert = \lvert S\rvert - d.
$$
The unnormalized Rideout–Sorkin transition weight is given by the inclusion-exclusion sum:
$$
\tilde{q}(P_n, S) = \sum_{k=0}^d (-1)^{d-k} \binom{d}{k} \alpha_{p + k}.
$$
Recognizing this sum as the $d$-th forward difference $\Delta^d \alpha_p$ of the sequence $\alpha$, we establish the fundamental representation:

**Lemma 6.1 (Forward Difference Identity for CSG Weights).**  
*For any coupling sequence $(t_k)_{k \ge 0}$ and any ideal $S$ with $d = \lvert\operatorname{Max}(S)\rvert$ and $p = \lvert S\setminus\operatorname{Max}(S)\rvert$, the unnormalized weight satisfies:*
$$
\tilde{q}(P_n, S) = \sum_{j=0}^p \binom{p}{j} t_{j+d}.
$$

*Proof.*  
Recall that the forward difference operator $\Delta$ acts on a sequence $a$ by $(\Delta a)_m = a_{m+1} - a_m$.
Applying $\Delta$ to the definition $\alpha_m = \sum_{k=0}^m \binom{m}{k} t_k$:
$$
(\Delta \alpha)_m = \sum_{k=0}^{m+1} \binom{m+1}{k} t_k - \sum_{k=0}^m \binom{m}{k} t_k = \sum_{k=1}^{m+1} \left[ \binom{m+1}{k} - \binom{m}{k} \right] t_k = \sum_{k=1}^{m+1} \binom{m}{k-1} t_k = \sum_{j=0}^m \binom{m}{j} t_{j+1}.
$$
By mathematical induction on $d$, applying the difference operator $d$ times yields:
$$
(\Delta^d \alpha)_p = \sum_{j=0}^p \binom{p}{j} t_{j+d}.
$$
Since $\Delta^d \alpha_p = \sum_{k=0}^d (-1)^{d-k} \binom{d}{k} \alpha_{p+k} = \tilde{q}(P_n, S)$, the identity is proved. $\blacksquare$

#### Partition Function Evaluation & Subset-Ideal Bijection
Summing the unnormalized weights over all downward-closed ideals $S \in \mathcal{I}(P_n)$ yields the celebrated Rideout–Sorkin partition identity via an exact subset-ideal bijection that underpins all degree, post, width, and height bounds below:

**Lemma 6.2 (Rideout–Sorkin Subset-Ideal Bijection & Hypergeometric Maximal Representation).**  
*For any finite poset $P_n$ of cardinality $n$:*
1. *Every subset $B \subseteq P_n$ generates a unique downward-closed ideal $S = J^-(B) := \{u \in P_n : \exists b \in B \text{ with } u \preceq b\}$, and $J^-(B) = S$ holds if and only if $\operatorname{Max}(S) \subseteq B \subseteq S$. Consequently, $B \mapsto (S = J^-(B), \, J = B \setminus \operatorname{Max}(S))$ is an exact bijection between the power set $2^{P_n}$ and pairs $(S \in \mathcal{I}(P_n), \, J \subseteq S \setminus \operatorname{Max}(S))$.*
2. *For any non-negative coupling sequence $(t_k)_{k \ge 0}$ ($t_0 > 0$), sampling $S_n \in \mathcal{I}(P_n)$ with probability $q(P_n, S) = \tilde{q}(P_n, S)/\alpha_n$ ($\alpha_n := \sum_{k=0}^n \binom{n}{k}t_k$) is identically distributed to sampling a random subset $B_n \subseteq P_n$ with poset-independent symmetric distribution $\mathbb{P}(B_n = B \mid P_n) = \frac{t_{\lvert B\rvert}}{\alpha_n}$ (equivalently: drawing $K_n = \lvert B_n\rvert \sim \pi_n(k) := \frac{1}{\alpha_n}\binom{n}{k}t_k$, then drawing $B_n$ uniformly among $K_n$-subsets of $P_n$) and setting $S_n = J^-(B_n)$.*
3. *Because no element of $P_n$ lies strictly above any $m \in \operatorname{Max}(P_n)$, we have $m \in J^-(B_n) \iff m \in B_n$ for every $m \in \operatorname{Max}(P_n)$, so $S_n \cap \operatorname{Max}(P_n) = B_n \cap \operatorname{Max}(P_n)$ identically.*

*Proof.*  
1. Every maximal element of $J^-(B)$ belongs to $B$, so $\operatorname{Max}(J^-(B)) \subseteq B \subseteq J^-(B)$. Conversely, if $\operatorname{Max}(S) \subseteq B \subseteq S$, downward closure of $S$ gives $J^-(B) \subseteq S$, while every $u \in S$ lies below some $m \in \operatorname{Max}(S) \subseteq B$, giving $S \subseteq J^-(B)$.
2. Grouping $B \subseteq P_n$ by $S = J^-(B)$ and $j = \lvert B \setminus \operatorname{Max}(S)\rvert \in \{0, \dots, p\}$ ($p = \lvert S\rvert - d$, $d = \lvert\operatorname{Max}(S)\rvert$) yields $\sum_{B : J^-(B) = S} t_{\lvert B\rvert} = \sum_{j=0}^p \binom{p}{j}t_{j+d} = \tilde{q}(P_n, S)$ by Lemma 6.1, and summing over all $S \in \mathcal{I}(P_n)$ yields $Z(P_n) = \sum_{B \subseteq P_n} t_{\lvert B\rvert} = \sum_{k=0}^n \binom{n}{k}t_k = \alpha_n$.
3. If $m \in \operatorname{Max}(P_n)$ satisfies $m \in J^-(B_n)$, then $m \preceq b$ for some $b \in B_n$; maximality of $m$ in $P_n$ forces $b = m \in B_n$. The converse $m \in B_n \implies m \in J^-(B_n)$ is immediate. $\blacksquare$

For the **factorial decaying coupling schedule** $t_k := c/k!$ ($k \ge 0, c > 0$), the partition function evaluates to the Laguerre polynomial $\alpha_n = c\sum_{k=0}^n \binom{n}{k}\frac{1}{k!} = c\,L_n(-1)$, with Perron–Szegő asymptotics $\alpha_n \sim \frac{c}{2\sqrt{\pi}}n^{-1/4}e^{2\sqrt{n}}$ as $n \to \infty$.  
*Crucial Invariance Note on $c$-Cancellation:* In normalized transition probabilities $q(P_n, S) = \tilde{q}(P_n, S)/\alpha_n$, the constant $c > 0$ cancels identically:
$$
q(P_n, S) = \frac{c \sum_{j=0}^p \binom{p}{j} \frac{1}{(j+d)!}}{c \sum_{k=0}^n \binom{n}{k} \frac{1}{k!}} = \frac{\sum_{j=0}^p \binom{p}{j} \frac{1}{(j+d)!}}{\sum_{k=0}^n \binom{n}{k} \frac{1}{k!}}.
$$
Thus, all values $c > 0$ yield the identical stochastic process, in contrast to geometric-factorial couplings $t_k = c^k/k!$ where $c$ enters with variable powers $c^{j+d}$ and serves as a genuine tunable coupling constant.

### 6.2 Theorem 6.1: Exact Bounds on Expected Link In-Degree

**Theorem 6.1 (`[PROVED THEOREM]` Link In-Degree Bounds & Antichain Extremality in CSG Families).**  
1. *Universal Antichain Extremality (All CSG Sequences):* *For **every** non-negative CSG sequence $(t_k)_{k \ge 0}$ ($t_0 > 0$) and **every** poset $P_n$ on $n \ge 1$ vertices, the conditional expected link in-degree is maximized over $\mathcal{P}_n$ by the $n$-antichain $A_n$:*
   $$
   \mathbb{E}\left[ \lvert \operatorname{Max}(S_n) \rvert \;\middle|\; P_n \right] \le \mathbb{E}_{\pi_n}[K_n] = \mathbb{E}\left[ \lvert \operatorname{Max}(S_n) \rvert \;\middle|\; A_n \right].
   $$
2. *Finite-Cutoff Classical Sequential Growth ($k_{\rm max} \ge 1$):* *If $t_k > 0$ for $0 \le k \le k_{\rm max}$ and $t_k = 0$ for $k > k_{\rm max}$, then $\lvert\operatorname{Max}(S_n)\rvert \le k_{\rm max}$ holds deterministically on every poset and every birth:*
   $$
   \sup_{n \ge 1} \sup_{P_n \in \mathcal{P}_n} \mathbb{E}\left[ \lvert \operatorname{Max}(S_n) \rvert \;\middle|\; P_n \right] \le k_{\rm max} < \infty.
   $$
   *In particular, for $k_{\rm max} = 2$ ($t_2 > 0$), $\alpha_n = t_0 + n t_1 + \binom{n}{2}t_2$ and $\mathbb{E}[\lvert\operatorname{Max}(S_n)\rvert \mid P_n] = 2 - R_2(P_n) + O(n^{-1}) \in [0, 2]$.*
3. *Factorial Decaying CSG ($t_k = c/k!$):*
   - *Exact Non-Asymptotic Two-Sided Antichain Bound:* *For **every** integer $n \ge 1$:*
     $$
     \sqrt{n + 1} - 1 < \mathbb{E}\left[ \lvert \operatorname{Max}(S_n) \rvert \;\middle|\; A_n \right] = \mathbb{E}_{\pi_n}[K_n] < \sqrt{n + \frac{1}{4}} - \frac{1}{2} < \sqrt{n},
     $$
     *establishing both the universal sublinear bound $\mathbb{E}[\lvert\operatorname{Max}(S_n)\rvert \mid P_n] < \sqrt{n}$ on every poset $P_n$ and the unbounded static supremum $\sup_{P_n} \mathbb{E}[d_n \mid P_n] \sim \sqrt{n} \to \infty$ (`[COUNTEREXAMPLE/OBSTRUCTION]` to unconditioned static boundedness).*
   - *Super-Exponential Extinction of Persistent Antichains:* *Under $\mathbb{P}_{\rm CSG}$, $\mathbb{P}_{\rm CSG}(P_n = A_n) = \prod_{k=1}^{n-1}(c/\alpha_k) \le K \exp(-\frac{4}{3}n^{3/2}) \to 0$, so $\mathbb{P}_{\rm CSG}(\limsup_{n \to \infty}\{P_n = A_n\}) = 0$. (Whether realized histories of $t_k = c/k!$ also satisfy uniform $O(1)$ expectation $\sup_n \mathbb{E}_{\mathbb{P}_{\rm CSG}}[d_n] < \infty$ remains open under `NG-02` Conjecture 5.3(1).)*

*Proof.*  
1. By Lemma 6.2, $S_n = J^-(B_n)$ where $\operatorname{Max}(J^-(B_n)) \subseteq B_n$, so $\lvert\operatorname{Max}(J^-(B_n))\rvert \le \lvert B_n\rvert = K_n$ pointwise for every subset $B_n \subseteq P_n$ (with equality for all $B_n$ if and only if $P_n = A_n$). Taking expectations yields $\mathbb{E}[\lvert\operatorname{Max}(S_n)\rvert \mid P_n] \le \mathbb{E}_{\pi_n}[K_n] = \mathbb{E}[\lvert\operatorname{Max}(S_n)\rvert \mid A_n]$.
2. Under $t_k = 0$ for $k > k_{\rm max}$, $\mathbb{P}(K_n > k_{\rm max}) = 0$, so $\lvert\operatorname{Max}(S_n)\rvert \le K_n \le k_{\rm max}$ identically. At $k_{\rm max} = 2$, $d_n = 2$ occurs precisely when $B_n$ is one of the $\binom{n}{2} - C_1(P_n)$ incomparable pairs (each of weight $t_2$), while $d_n = 1$ occurs on $B_n = \{u\}$ (weight $t_1$) or comparable pairs $\{v \prec u\}$ (weight $t_2$, totaling $C_1(P_n)t_2$), giving $\mathbb{E}[d_n \mid P_n] = \frac{n t_1 + (2\binom{n}{2} - C_1(P_n))t_2}{t_0 + n t_1 + \binom{n}{2}t_2} = 2 - R_2(P_n) + O(n^{-1})$.
3. For $t_k = c/k!$, set $\mu_n := \mathbb{E}_{\pi_n}[K_n]$. Using $k^2 \binom{n}{k}\frac{1}{k!} = n\binom{n-1}{k-1}\frac{1}{(k-1)!}$ ($k \ge 1$) and Pascal's identity $\binom{n}{k} = \binom{n-1}{k} + \binom{n-1}{k-1}$ gives two exact moment identities for every $n \ge 1$:
$$
\mathbb{E}_{\pi_n}[K_n^2] = n\,\frac{\alpha_{n-1}}{\alpha_n}, \qquad \alpha_n = \alpha_{n-1} + \frac{\mu_n}{n}\,\alpha_n \iff \frac{\alpha_{n-1}}{\alpha_n} = 1 - \frac{\mu_n}{n} \implies \mathbb{E}_{\pi_n}[K_n^2] = n - \mu_n.
$$
Since $\operatorname{Var}_{\pi_n}(K_n) = \mathbb{E}_{\pi_n}[K_n^2] - \mu_n^2 > 0$, we immediately obtain $\mu_n^2 < n - \mu_n \iff (\mu_n + \frac{1}{2})^2 < n + \frac{1}{4} \iff \mu_n < \sqrt{n + \frac{1}{4}} - \frac{1}{2} < \sqrt{n}$. Conversely, because all $n$ zeros $r_1, \dots, r_n > 0$ of the Laguerre polynomial $L_n(z)$ are real and strictly positive, the probability generating function $\sum_{k=0}^n \pi_n(k) z^k = \frac{L_n(-z)}{L_n(-1)} = \prod_{i=1}^n \frac{r_i + z}{r_i + 1}$ factors into $n$ independent Bernoulli variables $\xi_i \sim \operatorname{Bernoulli}(\frac{1}{1+r_i})$, so $\operatorname{Var}_{\pi_n}(K_n) = \sum_{i=1}^n \frac{r_i}{(1+r_i)^2} < \sum_{i=1}^n \frac{1}{1+r_i} = \mu_n$. Substituting $n - \mu_n = \mu_n^2 + \operatorname{Var}_{\pi_n}(K_n) < \mu_n^2 + \mu_n$ gives $(\mu_n + 1)^2 > n + 1 \iff \mu_n > \sqrt{n + 1} - 1$. Numerical values confirm tightness: $\mu_{10} = 2.5117 \in (2.3166, 3.1623)$, $\mu_{100} = 9.2835 \in (9.0499, 10.0000)$, $\mu_{1000} = 30.8836 \in (30.6386, 31.6228)$. Finally, $P_n = A_n$ requires $S_k = \varnothing$ for $1 \le k < n$, with $\prod_{k=1}^{n-1}(c/\alpha_k) \le K \exp(-2\sum_{k=1}^{n-1}\sqrt{k}) \le K \exp(-\frac{4}{3}n^{3/2})$, whose summability gives $\mathbb{P}_{\rm CSG}(\limsup_n \{P_n = A_n\}) = 0$ by the First Borel–Cantelli Lemma. $\blacksquare$

### 6.3 Theorem 6.2: Exact Proof of Vanishing Global-Post Density

**Theorem 6.2 (`[PROVED THEOREM]` Vanishing Global-Post Density in Finite-Cutoff & Factorial CSG).**  
*In both Finite-Cutoff CSG ($k_{\rm max} \ge 1$, $t_{k_{\rm max}} > 0$) and Factorial CSG ($t_k = c/k!$), the asymptotic global-post density vanishes almost surely:*
$$
\rho_{\rm post}(P_N) := \frac{N_{\rm post}(P_N)}{N} = \frac{1}{N}\sum_{n=1}^{N-1} \mathbf{1}_{\{S_n = P_n\}} \xrightarrow{N \to \infty} 0 \quad \mathbb{P}_\infty\text{-a.s.}
$$
*Specifically, for any parent poset $P_n$ with $M_n := \lvert\operatorname{Max}(P_n)\rvert \ge 1$ maximal elements:*
1. *Universal Falling-Factorial Identity (All CSG Sequences):*
   $$
   \mathbb{P}(S_n = P_n \mid P_n) = \frac{\mathbb{E}_{\pi_n}[(K_n)_{M_n}]}{(n)_{M_n}} \le \frac{\mathbb{E}_{\pi_n}[K_n]}{n}.
   $$
2. *Finite-Cutoff CSG ($k_{\rm max} \ge 1$):* *$\mathbb{P}(S_n = P_n \mid P_n) = 0$ identically whenever $M_n > k_{\rm max}$, and $\mathbb{P}(S_n = P_n \mid P_n) \le k_{\rm max}/n$ everywhere ($\mathbb{E}[\rho_{\rm post}(P_N)] \le k_{\rm max}\frac{1 + \ln N}{N} \to 0$). Moreover, since $M_n \to \infty$ $\mathbb{P}_\infty$-a.s. (Theorem 7.1 Remark), only finitely many global posts ever occur along almost every realized history: $N_{\rm post}(\infty) < \infty$ $\mathbb{P}_\infty$-a.s.*
3. *Factorial CSG ($t_k = c/k!$):* *By Theorem 6.1(3), $\mathbb{P}(S_n = P_n \mid P_n) \le \frac{\mathbb{E}_{\pi_n}[K_n]}{n} < \frac{1}{\sqrt{n}}$ holds **non-asymptotically for every poset $P_n$ and every $n \ge 1$** (with $O(n^{-M_n/2})$ scaling at fixed $M_n$), yielding $\mathbb{E}[\rho_{\rm post}(P_N)] < \frac{2}{\sqrt{N}} \to 0$, $\rho_{\rm post}(P_N) \xrightarrow{\text{a.s.}} 0$, and pure-chain extinction $\mathbb{P}_{\rm CSG}(P_n = C_n) \le (\frac{3}{5})^{n-2} \to 0$ ($n \ge 2$).*

*Proof.*  
1. By Lemma 6.2(3), $S_n = J^-(B_n) = P_n$ if and only if $\operatorname{Max}(P_n) \subseteq B_n$. Conditioned on $K_n = k$, the probability that a uniformly chosen $k$-subset of $P_n$ contains the $M_n$ elements of $\operatorname{Max}(P_n)$ is $\binom{n - M_n}{k - M_n}/\binom{n}{k} = \frac{(k)_{M_n}}{(n)_{M_n}}$ (zero if $k < M_n$). Averaging over $K_n \sim \pi_n$ proves $\mathbb{P}(S_n = P_n \mid P_n) = \mathbb{E}_{\pi_n}[(K_n)_{M_n}]/(n)_{M_n}$. Since $M_n \ge 1$, for every $k \ge M_n$ we have $\frac{(k)_{M_n}}{(n)_{M_n}} = \frac{k}{n}\prod_{j=1}^{M_n-1}\frac{k-j}{n-j} \le \frac{k}{n}$ (as $k \le n \implies \frac{k-j}{n-j} \le 1$), whence $\mathbb{P}(S_n = P_n \mid P_n) \le \mathbb{E}_{\pi_n}[K_n]/n$.
2. In Finite-Cutoff CSG, $K_n \le k_{\rm max}$ identically, so $(K_n)_{M_n} \equiv 0$ whenever $M_n > k_{\rm max}$, and $\mathbb{E}_{\pi_n}[K_n]/n \le k_{\rm max}/n$. By Remark 7.1 below, in Finite-Cutoff CSG $M_n \to \infty$ $\mathbb{P}_\infty$-a.s., so there exists an a.s. finite random stage $\tau(\omega) < \infty$ such that $M_n(\omega) > k_{\rm max}$ for all $n \ge \tau(\omega)$, forcing $\mathbf{1}_{\{S_n = P_n\}} = 0$ for all $n \ge \tau(\omega)$ and $N_{\rm post}(\infty) < \infty$ $\mathbb{P}_\infty$-a.s.
3. In Factorial CSG, Theorem 6.1(3) gives $\mathbb{E}_{\pi_n}[K_n] < \sqrt{n}$, so $\mathbb{P}(S_n = P_n \mid \mathcal{F}_{n-1}) < n^{-1/2}$ everywhere on $\Omega_\infty$ for all $n \ge 1$. Taking expectations gives $\mathbb{E}[\rho_{\rm post}(P_N)] < \frac{1}{N}\sum_{n=1}^{N-1} n^{-1/2} < \frac{1}{N}\int_0^N x^{-1/2}\,dx = \frac{2}{\sqrt{N}}$. For any $\delta > 0$, Markov's inequality along $N_m = m^4$ yields $\sum_{m=1}^\infty \mathbb{P}_\infty(\rho_{\rm post}(P_{m^4}) > \delta) < \sum_{m=1}^\infty \frac{2}{\delta m^2} = \frac{\pi^2}{3\delta} < \infty$, so $\rho_{\rm post}(P_{m^4}) \to 0$ $\mathbb{P}_\infty$-a.s. by First Borel–Cantelli. For arbitrary $N$ with $m^4 \le N < (m+1)^4$, monotonicity $N_{\rm post}(P_N) \le N_{\rm post}(P_{(m+1)^4})$ gives:
$$
0 \le \rho_{\rm post}(P_N) = \frac{N_{\rm post}(P_N)}{N} \le \frac{(m+1)^4}{m^4}\,\rho_{\rm post}(P_{(m+1)^4}) \xrightarrow{m \to \infty} 1 \cdot 0 = 0 \quad \mathbb{P}_\infty\text{-a.s.}
$$
Finally, on $C_k$ ($k \ge 2$), $\mathbb{P}(S_2 = C_2 \mid C_2) = \frac{3/2}{7/2} = \frac{3}{7} < \frac{3}{5}$ and for $k \ge 3$, $\mathbb{P}(S_k = C_k \mid C_k) < 1/\sqrt{3} < 3/5$, so $\mathbb{P}_{\rm CSG}(P_n = C_n) \le (3/5)^{n-2} \to 0$. $\blacksquare$

---

## 7. `NG-02` Screens 1–3 on Individual Histories of Explicit Covariant CSG Families

### 7.1 Screen 1: Width Divergence ($\operatorname{width}(P_N) \to \infty$)

**Theorem 7.1 (`[PROVED THEOREM]` Screen 1: Almost Sure Width Divergence via Autonomous Maximal-Count Dynamics).**  
*Let $(t_k)_{k \ge 0}$ ($t_0 > 0$) be **any** Classical Sequential Growth coupling sequence satisfying $\lim_{n \to \infty} \frac{\mathbb{E}_{\pi_n}[K_n]}{n} = 0$—including every Finite-Cutoff CSG family ($k_{\rm max} \ge 1$) and Factorial CSG ($t_k = c/k!$). Then the antichain width of individual causal set histories diverges almost surely:*
$$
\lim_{N \to \infty} \mathbb{P}_\infty\left( \operatorname{width}(P_N) \le K \right) = 0 \quad \forall K < \infty \iff \operatorname{width}(P_N) \xrightarrow{N \to \infty} \infty \quad \mathbb{P}_\infty\text{-a.s.}
$$

*Proof.*  
Let $M_n := \lvert\operatorname{Max}(P_n)\rvert$ denote the number of maximal elements of $P_n$. Because $\operatorname{Max}(P_n)$ is an antichain of $P_n$ and adding new vertices never destroys existing antichains, $\operatorname{width}(P_N)$ is monotonically non-decreasing in $N$ and satisfies:
$$
\operatorname{width}(P_N) \ge \max_{1 \le n \le N} M_n.
$$
At step $n \to n+1$, the newborn element $x_n$ is maximal in $P_{n+1}$, while an existing maximal element $m \in \operatorname{Max}(P_n)$ ceases to be maximal in $P_{n+1}$ if and only if $m \in S_n$. By Lemma 6.2(3), $S_n \cap \operatorname{Max}(P_n) = B_n \cap \operatorname{Max}(P_n)$, so:
$$
M_{n+1} = M_n + 1 - H_n, \qquad H_n := \lvert B_n \cap \operatorname{Max}(P_n)\rvert.
$$
Conditioned on $\mathcal{F}_{n-1}$, $B_n$ is drawn symmetrically from $P_n$ with size $K_n \sim \pi_n$, so $H_n$ has conditional expectation:
$$
\mathbb{E}[H_n \mid \mathcal{F}_{n-1}] = M_n\,\frac{\mathbb{E}_{\pi_n}[K_n]}{n}.
$$
Fix any integer $K \ge 1$. Because $\lim_{n \to \infty} \mathbb{E}_{\pi_n}[K_n]/n = 0$ (specifically $\le k_{\rm max}/n$ in Finite-Cutoff CSG and $< 1/\sqrt{n}$ in Factorial CSG), there exists an integer $n_0(K)$ such that $\frac{\mathbb{E}_{\pi_n}[K_n]}{n} \le \frac{1}{4K}$ for all $n \ge n_0(K)$.  
Whenever $n \ge n_0(K)$ and $M_n \le 2K$, Markov's inequality gives:
$$
\mathbb{P}(H_n \ge 1 \mid \mathcal{F}_{n-1}) \le \mathbb{E}[H_n \mid \mathcal{F}_{n-1}] \le 2K \cdot \frac{1}{4K} = \frac{1}{2} \implies \mathbb{P}(M_{n+1} = M_n + 1 \mid \mathcal{F}_{n-1}) = \mathbb{P}(H_n = 0 \mid \mathcal{F}_{n-1}) \ge \frac{1}{2}.
$$
Partition stages $n \ge n_0(K)$ into disjoint blocks of length $K$: $I_r := \{n_0(K) + rK, \dots, n_0(K) + (r+1)K - 1\}$ ($r = 0, 1, 2, \dots$). On the event $\{M_{n_0(K) + rK} \le K\}$, if $H_n = 0$ occurs at all $K$ steps of block $I_r$, then $M_n$ increments by $+1$ at each step of $I_r$ (staying $\le 2K$ throughout $I_r$) and reaches $M_{n_0(K) + (r+1)K} = M_{n_0(K) + rK} + K \ge 1 + K > K$. Chaining the $K$ conditional bounds yields:
$$
\mathbb{P}\left( \max_{n \in I_r \cup \{n_0 + (r+1)K\}} M_n > K \;\middle|\; \mathcal{F}_{n_0 + rK - 1} \right) \ge 2^{-K} > 0 \quad \text{everywhere on } \Omega_\infty.
$$
Consequently, for $R$ blocks ($N \ge n_0(K) + RK$), $\mathbb{P}_\infty(\operatorname{width}(P_N) \le K) \le \mathbb{P}_\infty(\max_{1 \le n \le N} M_n \le K) \le (1 - 2^{-K})^R \xrightarrow{R \to \infty} 0$. Monotonicity of $\operatorname{width}(P_N)$ implies $\lim_{N \to \infty}\operatorname{width}(P_N) = \infty$ $\mathbb{P}_\infty$-a.s. $\blacksquare$

*Remark 7.1 (Strong $M_n \to \infty$ in Finite-Cutoff CSG):* In Finite-Cutoff CSG ($k_{\rm max} \ge 1$), $\mathbb{P}(H_n \ge 2 \mid \mathcal{F}_{n-1}) = \mathbb{P}(\lvert B_n \cap \operatorname{Max}(P_n)\rvert \ge 2 \mid \mathcal{F}_{n-1}) \le \binom{M_n}{2}\frac{k_{\rm max}(k_{\rm max}-1)}{n(n-1)}$. Thus on $\{M_n \le 2K\}$, downward steps $M_{n+1} \le M_n - 1$ ($H_n \ge 2$) have summable conditional probabilities $O(K^2/n^2)$ and occur only finitely many times a.s. by First Borel–Cantelli, while upward steps $M_{n+1} = M_n + 1$ have probability $1 - O(K/n) \to 1$, proving $\lim_{n \to \infty} M_n = \infty$ $\mathbb{P}_\infty$-a.s. (closing Theorem 6.2(2)).

### 7.2 Screen 2: Height Divergence ($h(P_N) \to \infty$) and Timelike Depth ($\rho_2(P_N) > 0$)

**Theorem 7.2 (`[PROVED THEOREM]` Screen 2: Height Divergence & Timelike Depth).**  
*Let $(t_k)_{k \ge 0}$ ($t_0 > 0$) be any CSG sequence satisfying $\sum_{n=1}^\infty \frac{\mathbb{E}_{\pi_n}[K_n]}{n} = \infty$—including every non-trivial Finite-Cutoff CSG family ($k_{\rm max} \ge 1, t_{k_{\rm max}} > 0$, where $\frac{\mathbb{E}_{\pi_n}[K_n]}{n} = \frac{k_{\rm max}}{n} + O(n^{-2})$) and Factorial CSG ($t_k = c/k!$, where $\frac{\mathbb{E}_{\pi_n}[K_n]}{n} > \frac{\sqrt{n+1}-1}{n} \sim n^{-1/2}$). Then individual causal set histories satisfy:*
$$
\lim_{N \to \infty} h(P_N) = \infty \quad \mathbb{P}_\infty\text{-a.s.}, \qquad \lim_{N \to \infty} \mathbb{P}_\infty\left( h(P_N) \le 3 \right) = 0, \qquad \lim_{N \to \infty} \mathbb{P}_\infty\left( \rho_2(P_N) = 0 \right) = 0.
$$

*Proof.*  
At each stage $n \ge 1$, select deterministically (e.g., smallest label) a vertex $m_n^* \in P_n$ at the top of a longest chain of $P_n$ (length $h(P_n)$). Necessarily $m_n^* \in \operatorname{Max}(P_n)$ (if $m_n^* \prec z$, extending the chain by $z$ would yield length $h(P_n) + 1$).  
Whenever $m_n^* \in S_n$, adjoining $x_n$ above $S_n$ puts $m_n^* \prec x_n$ and creates a chain of length $h(P_n) + 1$, so $h(P_{n+1}) \ge h(P_n) + 1$. By Lemma 6.2(3) and symmetric $K_n$-subset sampling:
$$
\mathbb{P}_\infty\left( h(P_{n+1}) \ge h(P_n) + 1 \;\middle|\; \mathcal{F}_{n-1} \right) \ge \mathbb{P}_\infty\left( m_n^* \in B_n \;\middle|\; \mathcal{F}_{n-1} \right) = \frac{\mathbb{E}_{\pi_n}[K_n]}{n}.
$$
Summing over $n \ge 1$ gives $\sum_{n=1}^\infty \mathbb{P}_\infty(h(P_{n+1}) \ge h(P_n) + 1 \mid \mathcal{F}_{n-1}) \ge \sum_{n=1}^\infty \frac{\mathbb{E}_{\pi_n}[K_n]}{n} = \infty$ everywhere on $\Omega_\infty$. By Lévy's Conditional Borel–Cantelli Lemma (Williams 1991, §12.15), $h(P_{n+1}) \ge h(P_n) + 1$ occurs infinitely often $\mathbb{P}_\infty$-a.s., and monotonicity of $h(P_N)$ proves $\lim_{N \to \infty} h(P_N) = \infty$ $\mathbb{P}_\infty$-a.s.  
Once $h(P_N) \ge 3$ (a 4-vertex chain $v_0 \prec v_1 \prec v_2 \prec v_3$), $C_3(P_N) \ge 1$ and $C_2(P_N) \ge 4$, so $\rho_2(P_N) = C_3(P_N)/C_2(P_N) > 0$. Since $\tau_3 := \inf\{N : h(P_N) \ge 3\} < \infty$ $\mathbb{P}_\infty$-a.s., $\rho_2(P_N) > 0$ for all $N \ge \tau_3$ a.s. $\blacksquare$

### 7.3 Screen 3: Covering-Link Sparsity vs. Open Asymptotic Transitive Comparability

We distinguish strictly between **covering-link sparsity with linear connectivity** (proved analytically below) and **asymptotic interior concentration of transitive comparability $R_2(P_N) \in (\epsilon, 1 - \epsilon)$** (which requires controlling transitive past overlaps without posts and remains an open conjecture).

**Theorem 7.3A (`[PROVED THEOREM]` Covering-Link Sparsity & Almost Sure Linear Connectivity).**  
*In both Finite-Cutoff CSG ($k_{\rm max} \ge 2, t_{k_{\rm max}} > 0$) and Factorial CSG ($t_k = c/k!$):*
1. *Vanishing Covering-Link Density:* *The Hasse link count $N_0(P_N) = \sum_{n=1}^{N-1} \lvert\operatorname{Max}(S_n)\rvert$ satisfies $N_0(P_N)/\binom{N}{2} \le \frac{2 k_{\rm max}}{N} \to 0$ deterministically in Finite-Cutoff CSG, and $\mathbb{E}[N_0(P_N)]/\binom{N}{2} < \frac{4}{3\sqrt{N}} \to 0$ in Factorial CSG.*
2. *Finitely Many Empty Births & Linear Connectivity:* *Empty precursor selections $\{S_n = \varnothing\}$ occur **only finitely many times $\mathbb{P}_\infty$-almost surely**, so there exists an a.s. finite constant $B(\omega) < \infty$ such that for all $N \ge 2$:*
   $$
   C_1(P_N) \ge N_0(P_N) \ge N - 1 - B(\omega) \quad \mathbb{P}_\infty\text{-a.s.},
   $$
   *strictly ruling out disconnected antichain dust and bounding the number of Hasse connected components by $1 + B(\omega) < \infty$ $\mathbb{P}_\infty$-a.s.*

*Proof.*  
1. By §3.3 (maximal-element covering relations), each birth $x_n$ creates exactly $\lvert\operatorname{Max}(S_n)\rvert$ covering links and destroys none (since $x_n$ is maximal in $P_{n+1}$), so $N_0(P_N) = \sum_{n=1}^{N-1} \lvert\operatorname{Max}(S_n)\rvert$. Theorem 6.1(2) gives $N_0(P_N) \le k_{\rm max}(N-1)$ in Finite-Cutoff CSG, while Theorem 6.1(3) gives $\mathbb{E}[N_0(P_N)] < \sum_{n=1}^{N-1} \sqrt{n} < \frac{2}{3}N^{3/2}$ in Factorial CSG; dividing by $\binom{N}{2} = N(N-1)/2$ yields both limits.
2. For $S_n = \varnothing$, $\mathbb{P}(S_n = \varnothing \mid \mathcal{F}_{n-1}) = t_0/\alpha_n$. In Finite-Cutoff CSG with $k_{\rm max} \ge 2$ ($t_2 > 0$ or $t_{k_{\rm max}} > 0$), $\alpha_n \ge \binom{n}{k_{\rm max}} t_{k_{\rm max}} = \Omega(n^2)$; in Factorial CSG, $\alpha_n \ge c(1 + n + \frac{n(n-1)}{4}) = \Omega(n^2)$. In both cases $\sum_{n=1}^\infty (t_0/\alpha_n) < \infty$, so by the First Borel–Cantelli Lemma $B(\omega) := \sum_{n=1}^\infty \mathbf{1}_{\{S_n = \varnothing\}} < \infty$ $\mathbb{P}_\infty$-a.s. Every step with $S_n \ne \varnothing$ contributes $\lvert\operatorname{Max}(S_n)\rvert \ge 1$ link, proving $C_1(P_N) \ge N_0(P_N) \ge N - 1 - B(\omega)$. $\blacksquare$

**Theorem 7.3B' (`[PROVED THEOREM]` / `[COUNTEREXAMPLE/OBSTRUCTION]` Non-Asymptotic Fixed-Cutoff Parent-Path Union Bound & Comparability Collapse).**  
*Let $(t_k)_{k \ge 0}$ ($t_0 > 0$) be **any** Classical Sequential Growth coupling sequence with finite cutoff $k_{\rm max} \ge 1$ ($t_k = 0$ for all $k > k_{\rm max}$). Label the vertices in birth order $V_N = \{0, 1, \dots, N-1\}$. Then for every $0 \le i < j < N$, the pairwise comparability probability satisfies the exact discrete parent-path union bound:*
$$
\mathbb{P}(i \prec j) \le \frac{k_{\rm max}}{j} \prod_{m = i + 1}^{j - 1} \left( 1 + \frac{k_{\rm max}}{m} \right).
$$
*Consequently, for every finite size $N \ge 2$:*
1. *For $k_{\rm max} = 1$ (random recursive forest CSG), $\mathbb{P}(i \prec j) \le \frac{1}{i + 1}$ for all $0 \le i < j < N$ (with equality in the pure tree limit $t_0 \to 0^+$), yielding the exact harmonic bound:*
   $$
   \mathbb{E}[R_2(P_N)] \le \frac{2 H_{N-1}}{N} \le \frac{2(1 + \ln N)}{N} = O\left(\frac{\ln N}{N}\right) \xrightarrow{N \to \infty} 0.
   $$
2. *For any fixed integer $k_{\rm max} \ge 2$, $\mathbb{P}(i \prec j) \le \min\!\left(1, \, \frac{k_{\rm max}\,j^{k_{\rm max}-1}}{i^{k_{\rm max}}}\right)$ for all $1 \le i < j < N$, yielding the exact non-asymptotic power-law decay bound:*
   $$
   \mathbb{E}[R_2(P_N)] \le \frac{2}{N} + \frac{2\,k_{\rm max}^{2 + 1/k_{\rm max}}}{(k_{\rm max} - 1)(2 k_{\rm max} - 1)}\,\frac{N^{1 - 1/k_{\rm max}}}{N - 1} = O\left(N^{-1/k_{\rm max}}\right) \xrightarrow{N \to \infty} 0.
   $$
3. *Consequence for Screen 3: For every $\epsilon > 0$ and every fixed $k_{\rm max} < \infty$, Markov's inequality implies $\lim_{N \to \infty} \mathbb{P}_\infty(R_2(P_N) > \epsilon) = 0$. No fixed-cutoff CSG model can maintain an asymptotic interior comparability band $\epsilon < R_2(P_N) < 1 - \epsilon$, formally eliminating fixed-cutoff CSG from Conjecture 7.3B.*

*Proof.*  
By Lemma 6.2(2), at each birth step $m \in \{1, \dots, N-1\}$ the precursor ideal is $S_m = J^-(B_m)$, where $B_m \subseteq \{0, \dots, m-1\}$ has conditional law $\mathbb{P}(B_m = B \mid \mathcal{F}_{m-1}) = t_{\lvert B\rvert}/\alpha_m$. Because this conditional distribution depends solely on $m$ and $\lvert B\rvert$ and is completely independent of $\mathcal{F}_{m-1}$, the random subsets $(B_1, B_2, \dots, B_{N-1})$ are **mutually independent** across birth steps. Moreover, since $t_k = 0$ for $k > k_{\rm max}$ forces $K_m = \lvert B_m\rvert \le \min(m, k_{\rm max})$ deterministically, symmetric subset sampling gives for every $u \in \{0, \dots, m-1\}$:
$$
\mathbb{P}(u \in B_m) = \frac{\mathbb{E}_{\pi_m}[K_m]}{m} \le \frac{k_{\rm max}}{m}.
$$
Next, we claim that $i \prec j$ ($0 \le i < j < N$) holds in $P_N$ if and only if there exists a strictly increasing sequence $i = v_0 < v_1 < \dots < v_\ell = j$ ($\ell \ge 1$) such that $v_{r-1} \in B_{v_r}$ for each $r = 1, \dots, \ell$. The reverse implication is immediate because $v_{r-1} \in B_{v_r} \subseteq S_{v_r} \implies v_{r-1} \prec v_r$ and $\prec$ is transitive. Conversely, by strong induction on $j - i \ge 1$, if $i \prec j$, then $i \in S_j = J^-(B_j)$ inside $P_j$, so $i \preceq b$ for some $b \in B_j \subseteq \{0, \dots, j-1\}$; either $b = i$ ($\ell = 1, v_1 = j$) or $i \prec b < j$, in which case appending $v_\ell = j$ to the inductive chain from $i$ to $b$ completes the path.

Indexing each strictly increasing path $i = v_0 < v_1 < \dots < v_\ell = j$ bijectively by its intermediate vertex set $I = \{v_1, \dots, v_{\ell-1}\} \subseteq \{i+1, \dots, j-1\}$, the union bound and mutual independence of $(B_m)_{m=1}^{N-1}$ yield:
$$
\mathbb{P}(i \prec j) \le \sum_{\ell=1}^{j-i} \sum_{i = v_0 < v_1 < \dots < v_\ell = j} \prod_{r=1}^\ell \mathbb{P}(v_{r-1} \in B_{v_r}) \le \sum_{I \subseteq \{i+1, \dots, j-1\}} \frac{k_{\rm max}}{j} \prod_{m \in I} \frac{k_{\rm max}}{m} = \frac{k_{\rm max}}{j} \prod_{m = i + 1}^{j - 1} \left( 1 + \frac{k_{\rm max}}{m} \right).
$$
1. For $k_{\rm max} = 1$, the product telescopes identically for every $0 \le i < j$:
$$
\mathbb{P}(i \prec j) \le \frac{1}{j} \prod_{m = i + 1}^{j - 1} \frac{m + 1}{m} = \frac{1}{j} \cdot \frac{j}{i + 1} = \frac{1}{i + 1}.
$$
Summing over $0 \le i < j < N$ gives $\mathbb{E}[C_1(P_N)] \le \sum_{i=0}^{N-2} \frac{N - 1 - i}{i + 1} \le (N - 1)\sum_{r=1}^{N-1} \frac{1}{r} = (N - 1)H_{N-1}$, and dividing by $\binom{N}{2} = \frac{N(N-1)}{2}$ yields $\mathbb{E}[R_2(P_N)] \le \frac{2 H_{N-1}}{N} \le \frac{2(1 + \ln N)}{N} \to 0$.
2. For $k_{\rm max} \ge 2$ and any $1 \le i < j < N$, applying $1 + x \le e^x$ ($x \ge 0$) and $\sum_{m = i+1}^{j-1} \frac{1}{m} \le \int_i^j \frac{dx}{x} = \ln(j/i)$ gives:
$$
\prod_{m = i + 1}^{j - 1} \left( 1 + \frac{k_{\rm max}}{m} \right) \le \exp\left( k_{\rm max} \sum_{m = i + 1}^{j - 1} \frac{1}{m} \right) \le \left( \frac{j}{i} \right)^{k_{\rm max}} \implies \mathbb{P}(i \prec j) \le \min\left( 1, \; \frac{k_{\rm max}\,j^{k_{\rm max}-1}}{i^{k_{\rm max}}} \right).
$$
For each fixed $j \in \{1, \dots, N-1\}$, set $x_*(j) := k_{\rm max}^{1/k_{\rm max}} j^{1 - 1/k_{\rm max}}$. Splitting $1 \le i \le j-1$ into $1 \le i \le \lfloor x_*(j)\rfloor$ (using $\mathbb{P}(i \prec j) \le 1$) and $i \ge \lfloor x_*(j)\rfloor + 1 > x_*(j)$ (where $t^{-k_{\rm max}}$ is strictly decreasing, so $\sum_{i = \lfloor x_*(j)\rfloor + 1}^{j-1} i^{-k_{\rm max}} \le \int_{x_*(j)}^\infty t^{-k_{\rm max}}\,dt = \frac{x_*(j)^{1 - k_{\rm max}}}{k_{\rm max} - 1}$):
$$
\sum_{i=1}^{j-1} \mathbb{P}(i \prec j) \le x_*(j) + \frac{k_{\rm max}\,j^{k_{\rm max}-1}}{k_{\rm max} - 1}\,x_*(j)^{1 - k_{\rm max}} = \left( 1 + \frac{1}{k_{\rm max} - 1} \right) k_{\rm max}^{1/k_{\rm max}} j^{1 - 1/k_{\rm max}} = \frac{k_{\rm max}^{1 + 1/k_{\rm max}}}{k_{\rm max} - 1}\,j^{1 - 1/k_{\rm max}}.
$$
Since $y \mapsto y^{1 - 1/k_{\rm max}}$ is strictly increasing on $[0, N]$, $\sum_{j=1}^{N-1} j^{1 - 1/k_{\rm max}} \le \int_0^N y^{1 - 1/k_{\rm max}}\,dy = \frac{k_{\rm max}}{2 k_{\rm max} - 1}\,N^{2 - 1/k_{\rm max}}$. Including the $N - 1$ pairs with $i = 0$ ($\mathbb{P}(0 \prec j) \le 1$) gives:
$$
\mathbb{E}[C_1(P_N)] = \sum_{j=1}^{N-1} \mathbb{P}(0 \prec j) + \sum_{j=1}^{N-1} \sum_{i=1}^{j-1} \mathbb{P}(i \prec j) \le (N - 1) + \frac{k_{\rm max}^{2 + 1/k_{\rm max}}}{(k_{\rm max} - 1)(2 k_{\rm max} - 1)}\,N^{2 - 1/k_{\rm max}}.
$$
Dividing by $\binom{N}{2} = \frac{N(N-1)}{2}$ yields $\mathbb{E}[R_2(P_N)] \le \frac{2}{N} + \frac{2 k_{\rm max}^{2 + 1/k_{\rm max}}}{(k_{\rm max} - 1)(2 k_{\rm max} - 1)}\frac{N^{1 - 1/k_{\rm max}}}{N - 1} \to 0$.
3. Because $R_2(P_N) \ge 0$, Markov's inequality gives $\mathbb{P}_\infty(R_2(P_N) > \epsilon) \le \mathbb{E}[R_2(P_N)]/\epsilon \to 0$ for every $\epsilon > 0$. $\blacksquare$

**Conjecture 7.3B (`[OPEN CONJECTURE]` Screen 3: Interior Transitive Comparability in Unbounded CSG Families; `NG-02` Conjecture 5.3(2)).**  
*Determine whether there exists any Classical Sequential Growth coupling sequence $(t_k)_{k \ge 0}$ with unbounded support ($\sup\{k : t_k > 0\} = \infty$) and $\epsilon \in (0, 1/2)$ such that:*
$$
\lim_{N \to \infty} \mathbb{P}_\infty\left( \epsilon < R_2(P_N) < 1 - \epsilon \right) = 1.
$$

*Analytical Status & Large-$N$ Empirical Scaling ($N \le 2000$):*  
- **Fixed-Cutoff Elimination ($k_{\rm max} < \infty$):** Rigorously ruled out by Theorem 7.3B'. Large-$N$ stochastic trajectories up to $N = 2000$ (`frontier_a_r2_stabilization_simulation.py`) confirm both the power-law collapse and the tightness of the $N^{-1/k_{\rm max}}$ exponent whenever $t_{k_{\rm max}} > 0$:
  - $k_{\rm max} = 1$: $R_2(2000) = 0.0061 \pm 0.0004$, with $R_2(N)\frac{N}{\ln N} \in [1.36, 1.59]$;
  - $k_{\rm max} = 2$: $R_2(2000) = 0.0586 \pm 0.0014$, with $R_2(N)N^{1/2} \in [2.34, 2.62]$;
  - $k_{\rm max} = 3$: $R_2(2000) = 0.1521 \pm 0.0051$, with $R_2(N)N^{1/3} \in [1.80, 1.92]$ (exposing the $N \le 140$ window as a finite-size crossover).
- **Factorial & Geometric-Factorial Upward Drift ($t_k = c/k!$ vs. $t_k = c^k/k!$):** While $c > 0$ cancels identically in $t_k = c/k!$ (§6.1), the geometric-factorial family $t_k = c^k/k!$ ($c > 0$) has generating function $\frac{L_n(-cz)}{L_n(-c)}$ with growing subset mean $\mathbb{E}_{\pi_n}[K_n] \sim \sqrt{c n} \to \infty$. Conditioned on $(\mathcal{F}_{n-1}, K_n)$, any element $u \in P_n$ with future cone $J^+[u] := \{w \in P_n : u \preceq w\}$ fails to enter $S_n = J^-(B_n)$ if and only if $B_n \cap J^+[u] = \varnothing$, satisfying the exact hypergeometric bound:
  $$
  \mathbb{P}\left( u \notin S_n \;\middle|\; \mathcal{F}_{n-1}, K_n \right) = \frac{\binom{n - \lvert J^+[u]\rvert}{K_n}}{\binom{n}{K_n}} \le \left( 1 - \frac{\lvert J^+[u]\rvert}{n} \right)^{K_n} \le \exp\left( -\frac{K_n\,\lvert J^+[u]\rvert}{n} \right).
  $$
  Once early vertices acquire future cones $\lvert J^+[u]\rvert \gg \sqrt{n/c}$, $S_n$ captures a growing fraction of $P_n$ even while global-post density vanishes ($\rho_{\rm post}(2000) < 0.0014$). Empirical trajectories up to $N = 2000$ exhibit monotonic upward drift toward transitive saturation:
  - $c = 1.0$ ($t_k = 1/k!$): $R_2(50) = 0.6479 \to R_2(500) = 0.8145 \to R_2(1000) = 0.8539 \to R_2(2000) = 0.8842 \pm 0.0021$;
  - $c = 2.0$ ($t_k = 2^k/k!$): $R_2(50) = 0.7831 \to R_2(500) = 0.8767 \to R_2(1000) = 0.9033 \to R_2(2000) = 0.9253 \pm 0.0008$.
  Whether $\lim_{N \to \infty} R_2(P_N) = 1$ holds $\mathbb{P}_\infty$-almost surely for every $c > 0$ in $t_k = c^k/k!$, or whether a slower-growing unbounded coupling profile (e.g., super-factorial decay with $\mathbb{E}_{\pi_n}[K_n]$ growing logarithmically) can avoid both $R_2 \to 0$ and $R_2 \to 1$, remains an explicit `[OPEN CONJECTURE]`.

---

## 8. Formalization of Open Conjecture 5.5: Closed-Loop Curvature Feedback Attractor

### 8.1 Coupled Stochastic Process Formulation (Covariant Compensated vs. Stage-Tilted Prototypes)
Having established that static quantum steering fails on single histories (Proposition 5.5), that global feedback breaks covariance (Theorem 5.1), and that naive stage normalization breaks covariance even for local precursor weights (Theorem 5.3 & Corollary 5.3.1), we distinguish two properly normalized local-past feedback formulations on $(\Omega, \mathcal{F}, (\mathcal{F}_n)_{n \ge 1}, \mathbb{P})$:
1. **Local Curvature-Register Synthesis**: When newborn vertex $x_n$ adjoins with precursor ideal $S_n \subseteq P_n$, its local causal-past signal $\langle X\rangle(S_n) \in (-1, 1)$ and discretized register $\mathcal{R}(x_n) \in \mathcal{X}$ are evaluated strictly from $(S_n, \prec|_{S_n})$:
   $$
   \langle X\rangle(S_n) := -\tanh\left( \gamma \left( R_2(S_n) - \frac{1}{10} \right) + \kappa\,\frac{S_{\rm BD}^{(4)}(S_n)}{\max(1, \lvert S_n\rvert)} \right) \in (-1, 1), \quad \gamma, \kappa > 0,
   $$
   with $R_2(S_n) := 0$ for $\lvert S_n\rvert \le 1$.
2. **Exact Covariant Compensated Rule vs. Stage-Normalized Local-Tilt Prototype**:
   - *Exact Covariant Maximal-Deletion Rule (Theorem 5.4(3))*: Discretizing $\mathcal{R}(v) \in \mathcal{X}$ and steering a seed prefix between $q^{(+)}$ and $q^{(-)}$, maximal-deletion extension $q(P_n, \tilde{r}_n, S) = a_n u(P_n, \tilde{r}_n, S)$ ($S \subsetneq P_n$) with full-ideal slack $q(P_n, \tilde{r}_n, P_n) = 1 - a_n \sum_{S \subsetneq P_n} u(P_n, \tilde{r}_n, S)$ preserves **exact** complete-row normalization ($\sum_S q = 1$) and **exact** diamond commutation ($\Pi_1 = \Pi_2$).
   - *Stage-Normalized Precursor-Tilt Prototype (Normalized Non-Post Benchmark)*: Note that the unnormalized expression $\tilde{q}_{\rm tilt}(P_n, S) := \bar{q}(P_n, S) + \frac{1}{2}\Delta q(P_n, S)\,\langle X\rangle(S) > 0$ does **not** sum to $1$ over $S \in \mathcal{I}(P_n)$ when $\langle X\rangle(S)$ varies with $S$; complete-row normalization requires dividing by $Z_{\rm tilt}(P_n) := 1 + \frac{1}{2}\sum_{S' \in \mathcal{I}(P_n)} \Delta q(P_n, S')\,\langle X\rangle(S') > 0$:
     $$
     q_{\rm tilt}(P_n, S) := \frac{\bar{q}(P_n, S) + \frac{1}{2}\Delta q(P_n, S)\,\langle X\rangle(S)}{Z_{\rm tilt}(P_n)}.
     $$
     While $q_{\rm tilt}$ depends only on $S$ in its numerator, Theorem 5.3 shows that $Z_{\rm tilt}(P_n)$ introduces residual partition-ratio non-commutation across finite diamonds unless absorbed by full-ideal compensation.
3. **Discrete Curvature Response Sign**:
   - *Chain Dispersion ($R_2(S_n) > 1/10, S_{\rm BD}^{(4)} > 0$)*: Local past is elongated into chains; feedback sets $\langle X\rangle(S_n) < 0$, enhancing the sparse kernel $q^{(-)}$ and suppressing chain continuation.
   - *Interval Focusing ($R_2(S_n) < 1/10, S_{\rm BD}^{(4)} < 0$)*: Local past is overly wide and flat; feedback sets $\langle X\rangle(S_n) > 0$, enhancing timelike capping and chain formation.

### 8.2 Geometric Lyapunov Function & Martingale Increment
To analyze stability around the four-dimensional manifold geometry, define the target hypersurface:
$$
\mathcal{M}_4^* := \left\{ P \in \mathcal{P} : R_2(P) = \frac{1}{10}, \; S_{\rm BD}^{(4)}(P) = 0 \right\}.
$$
Define the geometric Lyapunov function:
$$
V(P_n) := \left( R_2(P_n) - \frac{1}{10} \right)^2 + \alpha \left( \frac{S_{\rm BD}^{(4)}(P_n)}{n} \right)^2 \quad (\alpha > 0).
$$
Let us compute the conditional increment $\Delta V_n := V(P_{n+1}) - V(P_n)$ given $\mathcal{F}_n$.
The recurrence relation for the comparable-pair fraction is:
$$
R_2(P_{n+1}) = \frac{C_1(P_n) + \lvert S_n\rvert}{\binom{n+1}{2}} = R_2(P_n)\frac{n-1}{n+1} + \frac{2\lvert S_n\rvert}{n(n+1)}.
$$
Subtracting $R_2(P_n)$:
$$
R_2(P_{n+1}) - R_2(P_n) = \frac{2}{n+1}\left( \frac{\lvert S_n\rvert}{n} - R_2(P_n) \right).
$$
Subtracting the target value $1/10$:
$$
R_2(P_{n+1}) - \frac{1}{10} = \left( R_2(P_n) - \frac{1}{10} \right) \left( 1 - \frac{2}{n+1} \right) + \frac{2}{n+1}\left( \frac{\lvert S_n\rvert}{n} - \frac{1}{10} \right).
$$
Squaring both sides:
$$
\left( R_2(P_{n+1}) - \frac{1}{10} \right)^2 = \left( R_2(P_n) - \frac{1}{10} \right)^2 \left( 1 - \frac{4}{n+1} + O\left(\frac{1}{n^2}\right) \right) + \frac{4}{n+1}\left( R_2(P_n) - \frac{1}{10} \right)\left( \frac{\lvert S_n\rvert}{n} - \frac{1}{10} \right) + O\left(\frac{1}{n^2}\right).
$$
Taking the conditional expectation $\mathbb{E}[\cdot \mid \mathcal{F}_n]$:
$$
\mathbb{E}\left[ \left( R_2(P_{n+1}) - \frac{1}{10} \right)^2 - \left( R_2(P_n) - \frac{1}{10} \right)^2 \;\middle|\; \mathcal{F}_n \right] = -\frac{4}{n+1}\left( R_2(P_n) - \frac{1}{10} \right) \left( R_2(P_n) - \frac{\mathbb{E}[\lvert S_n\rvert \mid \mathcal{F}_n]}{n} \right) + O\left(\frac{1}{n^2}\right).
$$

### 8.3 Negative Drift Supermartingale Property Outside Attractor Band

**Conjecture 8.1 (`[OPEN CONJECTURE]` Closed-Loop Curvature Feedback Dimension Attractor).**  
*Let $(P_n, \mathcal{R}_n)_{n \ge 1}$ be the closed-loop coupled stochastic process with feedback gains $\gamma, \kappa > 0$. Then:*
1. *Lyapunov Negative Drift: There exists a target neighborhood $U_\delta = \{ P \in \mathcal{P} : \lvert R_2(P) - 1/10\rvert \le \delta \}$ and a drift constant $c > 0$ such that for all $P_n \notin U_\delta$:*
   $$
   \mathbb{E}\left[ V(P_{n+1}) - V(P_n) \;\middle|\; \mathcal{F}_n \right] \le -c\,\frac{V(P_n)}{n}.
   $$
2. *Single-History 4D Dimension Convergence: Along almost every realized causal set history $\omega \in \Omega_\infty$:*
   $$
   \lim_{N \to \infty} R_2(P_N(\omega)) = \frac{1}{10} \quad \mathbb{P}\text{-a.s.} \implies \lim_{N \to \infty} d(R_2(P_N(\omega))) = 4.0 \quad \mathbb{P}\text{-a.s.}
   $$

#### Mathematical Analysis of the Drift Condition
When $R_2(P_n) > 1/10 + \delta$ (overly dense/chain phase):
- Typical precursor ideals have $R_2(S_n) > 1/10$, driving local coherence $\langle X\rangle(S_n) < 0$.
- The sparse kernel $q^{(-)}$ dominates, suppressing ancestor selection: $\mathbb{E}[\lvert S_n\rvert \mid \mathcal{F}_n]/n \ll R_2(P_n)$.
- The product $(R_2(P_n) - 1/10)(R_2(P_n) - \mathbb{E}[\lvert S_n\rvert]/n) > \delta^2 > 0$.
- The drift increment is strictly negative: $\mathbb{E}[\Delta V_n \mid \mathcal{F}_n] \le -\frac{4c_1}{n} V(P_n)$.

When $R_2(P_n) < 1/10 - \delta$ (overly sparse/antichain phase):
- Typical precursor ideals have $R_2(S_n) < 1/10$, driving local coherence $\langle X\rangle(S_n) > 0$.
- The dense kernel $q^{(+)}$ dominates, enhancing ancestor selection: $\mathbb{E}[\lvert S_n\rvert \mid \mathcal{F}_n]/n \gg R_2(P_n)$.
- The difference $R_2(P_n) - \mathbb{E}[\lvert S_n\rvert]/n < -\delta$, so multiplying by $(R_2(P_n) - 1/10) < -\delta$ yields a positive product $> \delta^2 > 0$.
- The negative sign in front guarantees $\mathbb{E}[\Delta V_n \mid \mathcal{F}_n] \le -\frac{4c_2}{n} V(P_n)$.

#### Epistemic Obstacles to Full Martingale Closure
Why is Conjecture 8.1 classified as `[OPEN CONJECTURE]` rather than `[PROVED THEOREM]`?
1. **Normalization-vs-Covariance Tension Without Full-Ideal Posts**: Under exact maximal-deletion compensation (Theorem 5.4(3)), proper-ideal weight variations are absorbed into the full-ideal post probability $q(P_n, \tilde{r}_n, P_n) = 1 - a_n \Sigma_u$, which requires $a_n \Sigma_u(P_n, \tilde{r}_n) \to 1$ along typical trajectories to suppress global posts (quantified rigorously by Theorem 8.1 below); conversely, stage-normalized non-post rules $q_{\rm tilt}(P_n, S)$ suffer $Z_{\rm tilt}(P_n)$ partition-ratio non-commutation across finite diamonds (Theorem 5.3).
2. **Local-to-Global Poset Martingale Coupling**: While the drift inequality holds conditionally when local precursor statistics $\mathbb{E}[\lvert S_n\rvert]$ mirror the global poset state $R_2(P_n)$, proving that local causal pasts $S_n$ remain faithful estimators of the global poset in an expanding universe without trapping in localized limit cycles requires a full martingale concentration theorem on partially ordered graphs.
3. **Infinite-Horizon Stochastic Stability**: Proving that the stochastic process does not exhibit rare large deviations that escape the attractor basin $U_\delta$ requires establishing a global Foster–Lyapunov criterion for Markov chains on causal sets, which remains an active open problem in causal set quantum gravity.

### 8.4 Theorem 8.1: Full-Ideal Capping Comparability Bound & The Normalization–Covariance Dilemma

**Theorem 8.1 (`[PROVED THEOREM]` / `[COUNTEREXAMPLE/OBSTRUCTION]` Full-Ideal Capping Comparability Lower Bound & Stage-Normalized Diamond Census).**  
*Let $(P_n, \tilde{r}_n)_{n \ge 1}$ evolve under any maximal-deletion full-ideal-compensated kernel (Theorem 5.4(3)), where proper ideals satisfy $q(P_n, \tilde{r}_n, S) = a_n u(P_n, \tilde{r}_n, S)$ ($S \subsetneq P_n$) and the full ideal satisfies $q(P_n, \tilde{r}_n, P_n) = 1 - a_n \Sigma_u(P_n, \tilde{r}_n)$ with $\Sigma_u(P_n, \tilde{r}_n) := \sum_{S \subsetneq P_n} u(P_n, \tilde{r}_n, S)$ and $0 < a_n \le 1/M_n$ ($M_n := \max_{\lvert P\rvert = n, \tilde{r}} \Sigma_u(P, \tilde{r})$). Then:*
1. *Exact Capping Comparability Lower Bound: For every finite horizon $N \ge 2$:*
   $$
   \mathbb{E}[R_2(P_N)] \ge \frac{2}{N(N-1)} \sum_{n=1}^{N-1} n\,\mathbb{E}\bigl[1 - a_n \Sigma_u(P_n, \tilde{r}_n)\bigr] \ge \frac{2}{N(N-1)} \sum_{n=1}^{N-1} n\left( 1 - \frac{\mathbb{E}[\Sigma_u(P_n, \tilde{r}_n)]}{M_n} \right).
   $$
2. *Slack Ratio Constraint for 4D Stabilization: If $\limsup_{n \to \infty} \mathbb{E}[a_n \Sigma_u(P_n, \tilde{r}_n)] \le 1 - \delta$ for some $\delta \in (0, 1]$, then $\liminf_{N \to \infty} \mathbb{E}[R_2(P_N)] \ge \delta$. In particular:*
   - *Avoiding asymptotic overshoot above $f(4) = 1/10$ requires $\limsup_{n \to \infty} \mathbb{E}[a_n \Sigma_u(P_n, \tilde{r}_n)] \ge \frac{9}{10}$;*
   - *Whenever $\lim_{n \to \infty} \frac{\mathbb{E}[\Sigma_u(P_n, \tilde{r}_n)]}{M_n} = 0$ (uniform maximal-sum domination over realized histories), $\lim_{N \to \infty} \mathbb{E}[R_2(P_N)] = 1$ and $R_2(P_N) \xrightarrow{\mathbb{P}} 1$ by capping saturation.*
3. *Stage-Normalized Local-Tilt Covariance Breakdown: Conversely, eliminating full-ideal slack via the stage-normalized non-post rule $q_{\rm tilt}(P_n, S) = \tilde{q}_{\rm tilt}(P_n, S)/Z_{\rm tilt}(P_n)$ (§8.1) violates $\Pi_1(S, T) = \Pi_2(T, S)$ across **279 / 441** ($63.3\%$) incomparable growth diamonds on base posets $N \le 4$.*

*Proof.*  
1. At each birth step $n \in \{1, \dots, N-1\}$, adjoining $x_n$ above $S_n \subseteq P_n$ adds exactly $\lvert S_n\rvert$ comparable pairs, so $C_1(P_N) = \sum_{n=1}^{N-1} \lvert S_n\rvert$. Because $\lvert S_n\rvert = n$ on the full-ideal capping event $\{S_n = P_n\}$ and $\lvert S_n\rvert \ge 0$ on $\{S_n \subsetneq P_n\}$, we have the pointwise inequality $C_1(P_N) \ge \sum_{n=1}^{N-1} n\,\mathbf{1}_{\{S_n = P_n\}}$. Note that this bound uses only the $n$ predecessors of $x_n$ at the moment $x_n$ is born and makes no assumptions on vertices born after $x_n$ (which could select $S_m = \varnothing$). Taking conditional expectations $\mathbb{P}(S_n = P_n \mid \mathcal{F}_{n-1}) = 1 - a_n \Sigma_u(P_n, \tilde{r}_n)$, dividing by $\binom{N}{2} = \frac{N(N-1)}{2}$, and applying $a_n \le 1/M_n$ yields both inequalities in Part 1.
2. If $\limsup_{n \to \infty} \mathbb{E}[a_n \Sigma_u(P_n, \tilde{r}_n)] \le 1 - \delta$, then $\liminf_{n \to \infty} \mathbb{E}[1 - a_n \Sigma_u(P_n, \tilde{r}_n)] \ge \delta$, so the triangular Cesàro average with weights $\frac{2n}{N(N-1)}$ ($\sum_{n=1}^{N-1} \frac{2n}{N(N-1)} = 1$) satisfies $\liminf_{N \to \infty} \mathbb{E}[R_2(P_N)] \ge \delta$. Setting $\delta > 9/10$ forces $\liminf_{N \to \infty}\mathbb{E}[R_2(P_N)] > 9/10 > 1/10$, and if $\mathbb{E}[\Sigma_u(P_n, \tilde{r}_n)]/M_n \to 0$, then $1 \ge \mathbb{E}[R_2(P_N)] \to 1$, which implies $\mathbb{E}[1 - R_2(P_N)] \to 0$ and $R_2(P_N) \xrightarrow{\mathbb{P}} 1$ by Markov's inequality on $1 - R_2(P_N) \ge 0$.
3. Exhaustive evaluation of $q_{\rm tilt}$ ($\gamma = 5.0, \kappa = 0.5$) across all 441 incomparable ideal pairs $(S, T)$ ($S \not\subseteq T, T \not\subseteq S$) on the 50 naturally ordered base posets $N \le 4$ (`frontier_a_r2_stabilization_simulation.py`) yields $Z_{\rm tilt}(C + x_S) \ne Z_{\rm tilt}(C + y_T)$ and $\lvert \Pi_1(S, T) - \Pi_2(T, S)\rvert > 10^{-12}$ on 279 / 441 diamonds ($63.265\%$). $\blacksquare$

---

## 9. Poset Verification Cross-Checks & Master Verification Suite Audit

### 9.1 Hand Verification of Benchmark Small Posets ($N \le 6$)

To guarantee absolute algebraic precision, the combinatorial invariants and curvature actions for all canonical posets up to $N = 6$ are derived by hand:

| Poset $P$ | $N$ | Hasse Links ($N_0$) | $C_1(P)$ | $R_2(P)$ | $d(R_2)$ | $S_{\rm BD}^{(2)}(P)$ | $S_{\rm BD}^{(4)}(P)$ | Verification Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Singleton $P_1$ | 1 | 0 | 0 | Undefined | Undefined | $+1$ | $+1$ | Hand-verified; $\binom{1}{2} = 0$ |
| Antichain $A_2$ | 2 | 0 | 0 | $0.0000$ | $\infty$ | $+2$ | $+2$ | Hand-verified; completely disconnected |
| Two-chain $C_2$ | 2 | 1 | 1 | $1.0000$ | $1.0000$ | $0$ | $+1$ | Hand-verified; $(N_0, N_1) = (1, 0)$ |
| Three-antichain $A_3$ | 3 | 0 | 0 | $0.0000$ | $\infty$ | $+3$ | $+3$ | Hand-verified |
| Three-fork $V_3$ | 3 | 2 | 2 | $2/3 \approx 0.6667$ | $\approx 1.54$ | $-1$ | $+1$ | Hand-verified; $(N_0, N_1) = (2, 0)$ |
| Three-chain $C_3$ | 3 | 2 | 3 | $1.0000$ | $1.0000$ | $+3$ | $+10$ | Hand-verified; $(N_0, N_1) = (2, 1)$ |
| Four-diamond $E_{\rm diamond}$ | 4 | 4 | 5 | $5/6 \approx 0.8333$ | $\approx 1.25$ | $-6$ | $-16$ | Hand-verified; $(N_0, N_1, N_2) = (4, 0, 1)$ |
| Four-chain $C_4$ | 4 | 3 | 6 | $1.0000$ | $1.0000$ | $+4$ | $+3$ | Hand-verified; $(N_0, N_1, N_2) = (3, 2, 1)$ |
| Five-antichain $A_5$ | 5 | 0 | 0 | $0.0000$ | $\infty$ | $+5$ | $+5$ | Hand-verified; $\Sigma_u(A_5) = 0.8774$ at $a_4 = 3/10$ |
| Five-chain $C_5$ | 5 | 4 | 10 | $1.0000$ | $1.0000$ | $+5$ | $+4$ | Hand-verified; $(N_0, N_1, N_2, N_3) = (4, 3, 2, 1)$ |
| Crown Poset $E_{\rm crown}$ | 6 | 6 | 6 | $6/15 = 0.4000$ | $\approx 2.30$ | $-6$ | $0$ | Hand-verified; $(N_0, N_1, N_2, N_3) = (6, 0, 0, 0)$ |
| Toy KR Poset $P_{\rm KR}$ | 8 | 8 | 11 | $11/28 \approx 0.3929$ | $\approx 2.33$ | $-2$ | $+2$ | Hand-verified; $(N_0, N_1, N_2, N_3) = (8, 2, 1, 0)$ |

### 9.2 External Scratch Suite Audit & Master Execution Summary
All theoretical claims and algebraic structures have been independently audited and confirmed using the external master verification suite (`teamwork_master_verification/run_master_n_le_6_suite.py`, `check10_stage5a_covariance_lyapunov_indegree.py`).

The master suite evaluated all 5,231 naturally ordered posets up to $N = 6$:
- $N = 1$: 1 poset
- $N = 2$: 2 posets
- $N = 3$: 7 posets
- $N = 4$: 40 posets
- $N = 5$: 357 posets
- $N = 6$: 4,824 posets
- **Total evaluated posets**: 5,231 posets across 11 master checks (including Check 10 for Stage 5A covariance obstructions, compensated local-register commutation, Lyapunov drift, and CSG degree/post bounds).

### 9.3 Numerical Confirmation of Check 8: Single-History Bifurcation and Conjecture Criteria
Check 8 of the master verification suite directly corroborates the theorems established in Sections 4, 6, and 8:
1. **Target Coherence Tuning**: Target coherence $\langle X\rangle_* = -1/7 \approx -0.142857$ tunes the ensemble mean exactly to $\mathbb{E}_{\rho_*}[R_2] = 0.100000 = f(4)$.
2. **Absence of Concentration at the Mean**:
   - At target coherence $\langle X\rangle_* = -1/7$, individual histories exhibit positive variance $\operatorname{Var}[R_2] \approx 0.00483 > 0$.
   - Sarle's bimodality coefficient evaluates to $b = 0.9810 \gg 0.555$, proving extreme bimodal separation into extremal branches $R_2^{(+)} \approx 0.180$ and $R_2^{(-)} \approx 0.040$.
   - Percentage of realized histories concentrating within $\pm 0.02$ of the ensemble mean $0.100$ is **0.0%**.
3. **CSG Decaying Couplings Degree Suppression**:
   - Factorial decaying couplings suppress link in-degree $d = 6$ by a factor of $6! = 720$, confirming Theorem 6.1.
4. **Curvature Feedback Sign Response**:
   - $S_{\rm BD}^{(4)}(C_4) = +3 > 0$ (confirming dispersion response).
   - $S_{\rm BD}^{(4)}(E_{\rm diamond}) = -16 < 0$ and $S_{\rm BD}^{(4)}(\text{KR Antichain}) \ll 0$ (confirming focusing response).
   - Negative Lyapunov drift $\mathbb{E}[\Delta V \mid \mathcal{F}_n] < 0$ verified across all sample test points outside the target band.

---

## 10. Governance Compliance, Quarantine & Non-Claims Declarations

### 10.1 Status-M Quarantine Attestation
The author hereby formally certifies that the four foundational Status-M ontological documents:
1. `ONTOLOGY.md`
2. `GOVERNANCE.md`
3. `PHYSICS.md`
4. `FALSIFICATION_LEDGER.md`

remain strictly quarantined and completely untouched (0 diff lines).

### 10.2 Strict Software Pause Attestation
In strict adherence to foundational research governance, ZERO modifications have been made to any software, test, or script files inside the repository (`det8/`, `scripts/`, `run_tests.py`, etc.). All mathematical proofs and derivations contained in this protocol were derived analytically from first principles.

### 10.3 Sibling Isolation Declaration
In accordance with Stage 5 isolation protocols, this document contains zero mentions, citations, or references to sibling Stage 5 research deliverables or parallel tracks, ensuring complete independence of the research tracks.

### 10.4 Non-Claims Boundary Attestation
This protocol adheres to the strict epistemic boundary of the research program:
- No claim is made to derive the continuous Einstein Field Equations, general relativity, or smooth Lorentzian manifolds from causal sets.
- No claim is made to derive quantum mechanics, Born's rule, or the origin of complex amplitudes.
- No claim is made that the 4D Alexandrov constant $f(4) = 1/10$ represents the unique true dimension of the physical universe, but rather that it serves as an exact combinatorial target for discrete dimension stabilization.
- All statements are formal mathematical theorems, structural obstructions, or explicitly labeled open conjectures within discrete causal set theory.
