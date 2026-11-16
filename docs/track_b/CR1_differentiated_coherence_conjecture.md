# Cross-Regime Differentiated Coherence (`CR-1`): Research Conjecture, Nested-Interval Diagnostics, and Unbounded CSG Tests

**Document Status:** Research Conjecture & Analytical/Empirical Investigation (`[RESEARCH CONJECTURE]` — Track B; **not** a proven law-selection principle and **not** a Status-M ontological commitment).  
**Dependencies:** [boundary_concepts.md](boundary_concepts.md) (Track B conceptual framing), [intrinsic_subset_restriction.md](intrinsic_subset_restriction.md) (`QR-LD036`), [intrinsic_law_selection_limits.md](intrinsic_law_selection_limits.md) (`QR-LD037`), [finite_prefix_nonidentification.md](finite_prefix_nonidentification.md) (`QR-LD032`), [PW6A_PROTOCOL.md](../../PW6A_PROTOCOL.md) (`PW6-A` covariance and fixed-cutoff bounds), and [manifold_compatible_growth_scaling_and_dimension_stabilization.md](../observables/manifold_compatible_growth_scaling_and_dimension_stabilization.md) (`PW5-B`).

---

## 1. Conceptual Motivation, Quarantine Boundary, and Scope

### 1.1 Conceptual Motivation and Strict Anti-Smuggling Quarantine
The Track B exploratory notes in [boundary_concepts.md](boundary_concepts.md) motivate asking whether lawful causal development across nested scales preserves both **relational coherence** (preventing fragmentation into causally disconnected dust) and **meaningful differentiation** (preventing collapse into a total order or global-post saturation). Separately, [intrinsic_law_selection_limits.md](intrinsic_law_selection_limits.md) (`QR-LD037`) proves that intrinsic marginal consistency under linear-extension deletion ($\mu_N K_N = \mu_{N-1}$) admits infinitely many distinct parameter values and finite non-diamond perturbations, leaving growth-law narrowing open.

To test whether a requirement of cross-regime differentiated coherence does genuine mathematical work rather than supplying post-hoc narrative vocabulary, we enforce a strict **anti-smuggling quarantine**:
1. **Conjecture Status (`[RESEARCH CONJECTURE]`):** Cross-Regime Differentiated Coherence (`CR-1`) is formulated and investigated strictly as a falsifiable **research conjecture**, not an established DET axiom or proven selection principle.
2. **Purely Poset-Theoretic Formalism:** Sections 2–8 contain zero theological or metaphysical variables. Every definition, theorem, counterexample, and numerical observable is stated purely in terms of finite posets, order ideals, transition probabilities, and causal intervals.
3. **No Built-In Four-Dimensionality:** Neither $d = 4$ nor the 4D Myrheim–Meyer target $f(4) = 1/10$ is inserted into `CR-1`. Whether any candidate growth family concentrates near a specific effective dimension is an empirical/analytical output to be measured, not assumed.
4. **Separation of Relational Coherence (`CR-1`) from Scale Self-Similarity (`SS-1`):** An open causal interval $I(u, v)$ inside a history $P_N$ and a birth-prefix $P_m$ of the same cardinality are **not** automatically samples from the same distribution. Section 3 explicitly separates internal interval concentration (`CR-1d`) from the stronger optional hypothesis of interval-to-global comparability matching (`SS-1`: $R_{\rm int}^* = R_{\rm global}^*$), proving analytically on continuum Lorentzian sprinklings that `CR-1` does not imply `SS-1`.

### 1.2 Summary of Claim Hygiene Labels
Throughout this document, every mathematical statement carries one of four explicit status tags:
- `[PROVED THEOREM]` / `[PROVED PROPOSITION]`: Self-contained proof valid under stated hypotheses.
- `[COUNTEREXAMPLE / OBSTRUCTION]`: Explicit finite or asymptotic construction falsifying a specific stronger claim.
- `[UNPROVED CANDIDATE]`: Complete mathematical specification of a candidate mechanism whose consistency or asymptotic behavior remains unproved, accompanied by explicit proof obligations.
- `[RESEARCH CONJECTURE]` / `[NUMERICAL EVIDENCE]`: Open research hypothesis or finite-horizon simulation result ($N \le 1024$), explicitly bounded against asymptotic overclaiming.

---

## 2. Mathematical Preliminaries: Poset Observables and Subset-Weight CSG

### 2.1 Finite Causal Sets, Intervals, and Intrinsic Observables
Let $P = (V, \prec)$ be a finite strict partial order (causal set) of cardinality $N = \lvert V\rvert \ge 2$, naturally labeled in birth order $V = \{0, 1, \dots, N-1\}$ so that $u \prec v \implies u < v$. Let $C \in \{0, 1\}^{N \times N}$ denote the strictly lower-triangular causal incidence matrix with $C_{vu} = 1 \iff u \prec v$.

For each vertex $x \in V$, define its strict causal past, inclusive causal past, strict causal future, and inclusive causal future:
$$
J^-(x) := \{u \in V : u \prec x\}, \quad J^-[x] := J^-(x) \cup \{x\}, \quad J^+(x) := \{v \in V : x \prec v\}, \quad J^+[x] := J^+(x) \cup \{x\}.
$$
A subset $S \subseteq V$ is a **downward-closed order ideal** ($S \in \mathcal{I}(P)$) if $x \in S$ and $u \prec x$ imply $u \in S$. Its maximal antichain is $\operatorname{Max}(S) := \{u \in S : \neg\exists\, v \in S \text{ with } u \prec v\}$. When a newborn vertex $x_n$ adjoins to $P_n$ with strict causal past $S \in \mathcal{I}(P_n)$, we write $P_n + x_S$ for the resulting $(n+1)$-element poset; the covering links into $x_n$ are precisely the elements of $\operatorname{Max}(S)$.

We track five intrinsic, relabeling-invariant poset observables:
1. **Global Comparability Fraction ($R_2$):** Let $C_1(P) := \lvert\{(u, v) \in V^2 : u \prec v\}\rvert = \sum_{v > u} C_{vu}$. For $N \ge 2$:
   $$
   R_2(P) := \frac{C_1(P)}{\binom{N}{2}} \in [0, 1].
   $$
   For a Poisson sprinkling into a continuum $d$-dimensional Minkowski Alexandrov causal diamond ($d \ge 1$), the Myrheim–Meyer continuum expectation for unordered-pair comparability is:
   $$
   f(d) = \frac{\Gamma(d + 1)\,\Gamma(d/2)}{2\,\Gamma(3d/2)}, \qquad f(1) = 1, \quad f(2) = \frac{1}{2}, \quad f(3) = \frac{8}{35} \approx 0.2286, \quad f(4) = \frac{1}{10}.
   $$
   (The denominator contains $2\,\Gamma(3d/2)$ rather than $4\,\Gamma(3d/2)$ because $R_2(P) = C_1(P)/\binom{N}{2}$ measures unordered-pair comparability $\mathbb{P}(p_1 \sim p_2) = 2\,\mathbb{P}(p_1 \prec p_2)$.) Because $f : [1, \infty) \to (0, 1]$ is continuous and strictly decreasing, $d_{\rm MM}(P) := f^{-1}(R_2(P))$ is a monotone readout of $R_2(P)$ on $(0, 1]$. However, matching $R_2(P) \approx f(d)$ is only a coarse necessary condition for $d$-dimensional geometry, not a sufficient one.
2. **Global Post Density ($\rho_{\rm post}$):** A vertex $x \in V$ is a **global post** if every $y \in V \setminus \{x\}$ satisfies $y \prec x$ or $x \prec y$, equivalently $\lvert J^-(x)\rvert + \lvert J^+(x)\rvert = N - 1$ (so $V$ splits as $J^-(x) \oplus \{x\} \oplus J^+(x)$ with zero causal paths bypassing $x$). The post density is:
   $$
   \rho_{\rm post}(P) := \frac{1}{N}\,\bigl\lvert\bigl\{x \in V : \lvert J^-(x)\rvert + \lvert J^+(x)\rvert = N - 1\bigr\}\bigr\rvert \in [0, 1].
   $$
3. **Multi-Step Chain Ratio ($\rho_2$):** Let $C_2(P) := \sum_{v > u} (C^2)_{vu}$ count $2$-step chains $u \prec z \prec v$, and let $C_3(P) := \sum_{v > u} (C^3)_{vu}$ count $3$-step chains $u \prec z_1 \prec z_2 \prec v$. Define:
   $$
   \rho_2(P) := \begin{cases} C_3(P) / C_2(P), & C_2(P) > 0, \\ 0, & C_2(P) = 0. \end{cases}
   $$
   Any poset of height at most $3$ (such as a 3-layer Kleitman–Rothschild poset) has $C_3(P) = 0$ and therefore $\rho_2(P) = 0$ identically.
4. **Open Causal (Alexandrov) Intervals and Layer Counts:** For any comparable pair $u \prec v$, the open causal interval is:
   $$
   I(u, v) := \{z \in V : u \prec z \prec v\}, \qquad m(u, v) := \lvert I(u, v)\rvert = (C^2)_{vu}.
   $$
   The layer count $N_k(P) := \lvert\{(u, v) : u \prec v,\; \lvert I(u, v)\rvert = k\}\rvert$ counts comparable pairs separated by $k$ intermediate vertices ($N_0(P)$ is the Hasse link count).
5. **Sub-Interval Comparability ($R_2(I(u, v))$):** Whenever $m = \lvert I(u, v)\rvert \ge 2$, viewing $(I(u, v), \prec|_{I(u, v)})$ as an induced subposet gives:
   $$
   R_2\bigl(I(u, v)\bigr) := \frac{C_1\bigl(I(u, v)\bigr)}{\binom{m}{2}} \in [0, 1].
   $$

### 2.2 Exact Rideout–Sorkin / `QR-LD036` Subset-Weight Dynamics and Cone Overlap
In scalar subset-weight Classical Sequential Growth (Rideout & Sorkin 1999; [intrinsic_subset_restriction.md](intrinsic_subset_restriction.md) `QR-LD036` Eq. (1); [PW6A_PROTOCOL.md](../../PW6A_PROTOCOL.md) Lemma 6.2), a non-negative coupling sequence $(t_k)_{k \ge 0}$ with $t_0 = 1$ assigns to each order ideal $S \in \mathcal{I}(P_n)$ of an $n$-element parent poset $P_n$ ($\lvert P_n\rvert = n$) the transition probability:
$$
Z_n := \sum_{k=0}^n \binom{n}{k} t_k, \qquad G(s, m) := \sum_{k=m}^s \binom{s - m}{k - m} t_k, \qquad q(P_n, S) := \frac{G\bigl(\lvert S\rvert, \lvert\operatorname{Max}(S)\rvert\bigr)}{Z_n}.
$$
By `PW6A` Lemma 6.2, a subset $B \subseteq P_n$ has inclusive downward closure $J^-[B] := \bigcup_{b \in B} J^-[b]$ equal to $S$ if and only if $\operatorname{Max}(S) \subseteq B \subseteq S$. Summing $t_{\lvert B\rvert}$ over the $2^{\lvert S\rvert - \lvert\operatorname{Max}(S)\rvert}$ subsets $B$ sandwiched between $\operatorname{Max}(S)$ and $S$ yields $G(\lvert S\rvert, \lvert\operatorname{Max}(S)\rvert)$, proving both $\sum_{S \in \mathcal{I}(P_n)} q(P_n, S) = 1$ and the **two-step subset representation**:
1. Draw seed cardinality $K_n \in \{0, 1, \dots, n\}$ from the poset-independent distribution $\pi_n(k) := \binom{n}{k} t_k / Z_n$;
2. Draw a uniform $K_n$-element subset $B_n \subseteq P_n$ and set the newborn's strict causal past to $S_n = J^-[B_n]$.

Crucially, the **selected seed count** $K_n = \lvert B_n\rvert$ and the **realized Hasse link in-degree** $m_n = \lvert\operatorname{Max}(S_n)\rvert$ satisfy $m_n \le K_n$, with strict inequality whenever two selected seed vertices are causally comparable ($b_1 \prec b_2 \implies J^-[b_1] \subsetneq J^-[b_2]$). Thus parent-count scaling $\mathbb{E}_{\pi_n}[K_n]$ **alone** does not determine resulting poset geometry: overlapping causal cones $J^-[b]$ control both link compression $K_n - \lvert\operatorname{Max}(S_n)\rvert$ and transitive comparability $R_2(P_N)$.

---

## 3. Conjecture `CR-1` vs. Self-Similarity Hypothesis `SS-1` (`[RESEARCH CONJECTURE]`)

We now state **Cross-Regime Differentiated Coherence (`CR-1`)** with explicit rules for bulk interval selection, interval-to-history size scaling, single-history convergence, and within- vs. between-history variation, and separate it cleanly from scale self-similarity (`SS-1`).

### 3.1 Modular Statement of Conjecture `CR-1` (`[RESEARCH CONJECTURE]`)
Let $(\Omega_\infty, \mathcal{F}, (\mathcal{F}_n)_{n \ge 1}, \mathbb{P})$ be the path space of sequential causal histories $\omega = (P_1(\omega), P_2(\omega), \dots)$ generated by a Markov transition kernel $q(P_n, \cdot)$ on order ideals (possibly coupled to local finite registers as in `PW6A` §5.3). We say the growth law satisfies **Cross-Regime Differentiated Coherence (`CR-1`)** if all four of the following conditions hold:

1. **`CR-1a` (Order-Covariant & Diamond-Consistent Growth):**  
   Transition probabilities are invariant under poset isomorphisms, depend on proper ideals $S \subsetneq P_n$ only through intrinsic causal-past data on $S$ up to stage normalization, and satisfy **exact spacelike diamond commutation**: for every finite poset $C$ and every pair of ideals $S, T \in \mathcal{I}(C)$, adjoining incomparable newborn elements $x$ (above $S$) and $y$ (above $T$) in either birth order yields identical two-step transition probability:
   $$
   q(C, S)\, q(C + x_S, T) = q(C, T)\, q(C + y_T, S).
   $$

2. **`CR-1b` (Single-History Global Differentiation, Coherence, and Depth):**  
   There exists a **deterministic interior constant** $R_{\rm global}^* \in (0, 1)$ (depending only on the law, not on the realization $\omega$) such that along individual histories:
   $$
   R_2\bigl(P_N(\omega)\bigr) \xrightarrow[N \to \infty]{\mathbb{P}} R_{\rm global}^* \in (0, 1), \qquad \lim_{N \to \infty} \operatorname{Var}_{\rm between}\bigl(R_2(P_N)\bigr) = 0,
   $$
   where $\operatorname{Var}_{\rm between}(R_2(P_N)) := \mathbb{E}\bigl[(R_2(P_N) - \mathbb{E}[R_2(P_N)])^2\bigr]$ (estimated across $M$ independent histories $\omega^{(1)}, \dots, \omega^{(M)}$ by $\widehat{\operatorname{Var}}_{\rm between}(R_2) = \frac{1}{M - 1}\sum_{r=1}^M (R_2(P_N(\omega^{(r)})) - \langle R_2\rangle)^2$). In addition, global posts vanish and multi-step causal chains persist in single histories:
   $$
   \rho_{\rm post}\bigl(P_N(\omega)\bigr) \xrightarrow[N \to \infty]{\mathbb{P}} 0, \qquad \lim_{N \to \infty} \mathbb{P}\bigl(\rho_2(P_N(\omega)) > \rho_{\min}\bigr) = 1 \quad \text{for some } \rho_{\min} > 0.
   $$

3. **`CR-1c` (Explicit Bulk Causal-Interval Selection & Mesoscopic Scaling Rule):**  
   Fix a mesoscopic size exponent $\alpha \in (0, 1)$, window constants $0 < c_- < c_+ < \infty$, and a boundary-trimming fraction $\delta_{\rm bulk} \in [0, 1/4)$. Let $\overline{J}_N(\omega) := \frac{1}{N}\sum_{x \in P_N(\omega)} \lvert J^-(x)\rvert$ denote the mean strict-past size in $P_N(\omega)$. Define the **admissible mesoscopic interval family** at horizon $N$:
   $$
   \mathcal{J}_N(\omega; \alpha, c_-, c_+, \delta_{\rm bulk}) := \Bigl\{(u, v) \in P_N(\omega)^2 : u \prec v,\; \lvert J^-(u)\rvert \ge \delta_{\rm bulk}\overline{J}_N(\omega),\; \lvert J^+(v)\rvert \ge \delta_{\rm bulk}\overline{J}_N(\omega),\; c_- N^\alpha \le \lvert I(u, v)\rvert \le c_+ N^\alpha\Bigr\}.
   $$
   (In finite-$N$ benchmarks we take the canonical mesoscopic exponent $\alpha = 1/2$ with $m = \lvert I(u, v)\rvert \in \bigl[\max(4, \lfloor\frac{1}{2}\sqrt{N}\rfloor), \max(12, \lfloor\frac{5}{2}\sqrt{N}\rfloor)\bigr]$; at very small horizons $N \in \{16, 32\}$ where $N^{1/2} \le 5.7$, we include all nontrivial intervals $m \ge 4$.) `CR-1c` requires that the bulk interval sample size diverges in single histories: $\lvert\mathcal{J}_N(\omega)\rvert \xrightarrow{\mathbb{P}} \infty$ as $N \to \infty$.

4. **`CR-1d` (Within-History and Between-History Nested-Interval Concentration):**  
   For any history $\omega$ with $\lvert\mathcal{J}_N(\omega)\rvert \ge 2$, define the **single-history mean interval comparability** and **within-history interval variance**:
   $$
   \overline{R}_{\rm int}\bigl(P_N(\omega)\bigr) := \frac{1}{\lvert\mathcal{J}_N(\omega)\rvert}\sum_{(u, v) \in \mathcal{J}_N(\omega)} R_2\bigl(I(u, v)\bigr),
   $$
   $$
   \operatorname{Var}_{\rm within}\bigl(R_2(I); \omega\bigr) := \frac{1}{\lvert\mathcal{J}_N(\omega)\rvert - 1}\sum_{(u, v) \in \mathcal{J}_N(\omega)} \Bigl(R_2\bigl(I(u, v)\bigr) - \overline{R}_{\rm int}\bigl(P_N(\omega)\bigr)\Bigr)^2,
   $$
   and define the **between-history interval variance** $\operatorname{Var}_{\rm between}(\overline{R}_{\rm int}(P_N)) := \mathbb{E}\bigl[(\overline{R}_{\rm int}(P_N) - \mathbb{E}[\overline{R}_{\rm int}(P_N)])^2\bigr]$. `CR-1d` requires the existence of a **deterministic interior constant** $R_{\rm int}^* \in (0, 1)$ (independent of $\omega$) such that:
   $$
   \overline{R}_{\rm int}\bigl(P_N(\omega)\bigr) \xrightarrow[N \to \infty]{\mathbb{P}} R_{\rm int}^* \in (0, 1), \qquad \operatorname{Var}_{\rm within}\bigl(R_2(I); \omega\bigr) \xrightarrow[N \to \infty]{\mathbb{P}} 0, \qquad \lim_{N \to \infty} \operatorname{Var}_{\rm between}\bigl(\overline{R}_{\rm int}(P_N)\bigr) = 0.
   $$

### 3.2 Separation from Optional Self-Similarity Hypothesis `SS-1` (`[PROVED PROPOSITION]`)
Notice that `CR-1b` and `CR-1d` require $R_{\rm global}^* \in (0, 1)$ and $R_{\rm int}^* \in (0, 1)$ individually, **without** assuming $R_{\rm int}^* = R_{\rm global}^*$. Requiring internal causal intervals $I(u, v)$ to match the global comparability of the ambient history (or of a birth-prefix $P_m$ of size $m = \lvert I(u, v)\rvert$) is a strictly stronger **additional geometric/distributional self-similarity hypothesis**:

- **Optional Hypothesis `SS-1` (`[OPTIONAL SELF-SIMILARITY HYPOTHESIS]`):** Under the conditions of `CR-1`, the mesoscopic internal interval limit equals the global history limit:
  $$
  R_{\rm int}^* = R_{\rm global}^*.
  $$
  (A still stronger distributional version `SS-1+` would require the law of the unlabeled subposet $I(u, v)$ conditioned on $\lvert I(u, v)\rvert = m$ to converge in total variation to the law of $P_m$; even continuum Lorentzian slabs violate `SS-1`, while continuum diamonds satisfy `SS-1`.)

**Proposition 3.1 (`[PROVED PROPOSITION]` Non-Vacuity of Observable Conditions `CR-1b–d` and Exact Separation from `SS-1` in Continuum Minkowski Sprinklings).**  
*(Scope Clarification: Static Poisson Point Processes vs. Sequential Markovian Growth Laws): Static Poisson point processes on continuum Lorentzian domains establish the non-vacuity of the geometric observable and concentration conditions `CR-1b`, `CR-1c`, and `CR-1d` (and demonstrate the exact mathematical separation of `CR-1` from `SS-1`). However, a continuum sprinkling is an ensemble of random partial orders, not a sequential Markovian growth law on order ideals (it does not define discrete Markov transition probabilities $q(P_n, S)$ satisfying `CR-1a`). Whether there exists a discrete, sequential, diamond-commuting Markovian growth law satisfying all four conditions `CR-1a–d` remains an open research conjecture.*

*Let $P_N$ be generated by uniform i.i.d. (binomial) sprinkling of $N$ points into a causally convex or slab compact Lorentzian domain $\Omega \subset \mathbb{R}^{1, d-1}$ ($d \ge 2$), ordered by continuum Minkowski causality ($t_2 - t_1 > \lVert \mathbf{x}_2 - \mathbf{x}_1\rVert_2$). In every such domain (with $\delta_{\rm bulk} \in [0, \delta_0(\Omega))$, including all $\delta_{\rm bulk} \in [0, 1/4)$ for $D_d$ and $\Omega_L$): (i) global posts vanish in probability: $\rho_{\rm post}(P_N) \xrightarrow{\mathbb{P}} 0$ (with $\mathbb{E}[N_{\rm post}] = O(N^{1-d}) \to 0$ in Alexandrov diamonds); (ii) multi-step chains persist: $\rho_2(P_N) = \Theta_{\mathbb{P}}(N) \xrightarrow{\mathbb{P}} \infty$, so $\lim_{N\to\infty} \mathbb{P}(\rho_2(P_N) > \rho_{\min}) = 1$ for every $\rho_{\min} > 0$; and (iii) for every $\alpha \in (0, 1)$, admissible mesoscopic bulk intervals diverge in probability ($\lvert\mathcal{J}_N\rvert \xrightarrow{\mathbb{P}} \infty$), with exact near-lightlike-enhanced asymptotic order:*
$$
\lvert\mathcal{J}_N\rvert = \Theta_{\mathbb{P}}\!\left(N^{1 + \alpha}\ln N\right) \quad \text{in } d = 2 \text{ (on both } D_2 \text{ and } \Omega_L,\; L \ge 1\text{)}, \qquad \lvert\mathcal{J}_N\rvert = \Theta_{\mathbb{P}}\!\left(N^{2 - \frac{2(1 - \alpha)}{d}}\right) \quad \text{in } d \ge 3 \text{ (on } D_d\text{)},
$$
*both strictly exceeding the naive smooth-volume order $N^{1 + \alpha}$ (since $2 - \frac{2(1 - \alpha)}{d} - (1 + \alpha) = (1 - \alpha)(1 - \frac{2}{d}) > 0$ for $d \ge 3$) and matching the classical Brightwell–Gregory link asymptotics $\Theta(N\ln N)$ ($d = 2$) and $\Theta(N^{2 - 2/d})$ ($d \ge 3$) as $\alpha \to 0^+$. Furthermore:*
1. *($d$-Dimensional Alexandrov Diamond Satisfies `CR-1b–d` and `SS-1`): If $\Omega = D_d := \{(t, \mathbf{x}) \in \mathbb{R}^{1, d-1} : \lVert \mathbf{x}\rVert_2 < \min(t, 1 - t)\}$ ($d \ge 2$), then $R_2(P_N) \xrightarrow{\mathbb{P}} f(d) \in (0, 1/2]$, $\operatorname{Var}_{\rm between}(R_2(P_N)) = O(N^{-1}) \to 0$, and for every $\alpha \in (0, 1)$, mesoscopic intervals satisfy $\overline{R}_{\rm int}(P_N) \xrightarrow{\mathbb{P}} f(d)$, $\operatorname{Var}_{\rm within}(R_2(I); \omega) \xrightarrow{\mathbb{P}} 0$, and $\operatorname{Var}_{\rm between}(\overline{R}_{\rm int}(P_N)) \to 0$. Thus $R_{\rm int}^* = R_{\rm global}^* = f(d)$, satisfying **both** `CR-1b–d` and `SS-1`.*
2. *(2D Wide-Slab Cylinder Satisfies `CR-1b–d` While Violating `SS-1`): Let $\Omega_L := [0, 1] \times [0, L] \subset \mathbb{R}^{1, 1}$ with spatial width $L \ge 1$. Then the global comparability converges in probability to the exact rational function:*
   $$
   R_{\rm global}^*(\Omega_L) = \frac{4L - 1}{6 L^2} \in \left(0, \frac{1}{2}\right], \qquad R_{\rm global}^*(\Omega_3) = \frac{11}{54} \approx 0.203704,
   $$
   *with $\operatorname{Var}_{\rm between}(R_2(P_N)) = O(N^{-1}) \to 0$, whereas for every $\alpha \in (0, 1)$ and $\delta_{\rm bulk} \in [0, 1/4)$, mesoscopic bulk intervals $I(u, v)$ satisfy:*
   $$
   R_{\rm int}^*(\Omega_L) = f(2) = \frac{1}{2} = 0.500000 \ne \frac{11}{54} = R_{\rm global}^*(\Omega_3) \quad (L > 1),
   $$
   *with $\operatorname{Var}_{\rm within}(R_2(I); \omega) \xrightarrow{\mathbb{P}} 0$ and $\operatorname{Var}_{\rm between}(\overline{R}_{\rm int}(P_N)) \to 0$. Hence $\Omega_3$ satisfies `CR-1b–d` while strictly falsifying `SS-1`.*

*Proof.*  
First, for vanishing post density $\rho_{\rm post} \xrightarrow{\mathbb{P}} 0$: for any point $z \in \Omega$ with $d \ge 2$, its spacelike complement $S(z) = \Omega \setminus (J^-[z] \cup J^+[z])$ has strictly positive Lebesgue volume $V_{\rm space}(z) > 0$ for almost all $z \in \Omega$. Conditioned on $Z_1 = z$, the remaining $N - 1$ points fall outside $S(z)$ with probability $(1 - V_{\rm space}(z)/V)^{N - 1}$. Dominated convergence gives $\mathbb{E}[\rho_{\rm post}(P_N)] = \mathbb{P}(Z_1 \text{ is a post}) = \int_\Omega (1 - V_{\rm space}(z)/V)^{N - 1}\frac{d^d z}{V} \to 0$ as $N \to \infty$, whence $\rho_{\rm post}(P_N) \xrightarrow{\mathbb{P}} 0$ by Markov's inequality (in $D_d$, integrating near the boundary tips yields $\mathbb{E}[N_{\rm post}] = O(N^{1-d}) \to 0$).  
Second, for chain ratio persistence: since $\Omega$ has non-empty interior, there exist open subsets of timelike triples $z_1 \prec z_2 \prec z_3$ and quadruples $z_1 \prec z_2 \prec z_3 \prec z_4$, so $p_{\rm chain2} := \mathbb{P}(Z_1 \prec Z_2 \prec Z_3) > 0$ and $p_{\rm chain3} := \mathbb{P}(Z_1 \prec Z_2 \prec Z_3 \prec Z_4) > 0$. By Hoeffding's U-statistic convergence, $C_2(P_N) / N^3 \xrightarrow{\mathbb{P}} p_{\rm chain2}$ and $C_3(P_N) / N^4 \xrightarrow{\mathbb{P}} p_{\rm chain3}$, so $\rho_2(P_N) = C_3(P_N)/C_2(P_N) = \Theta_{\mathbb{P}}(N) \xrightarrow{\mathbb{P}} \infty$, proving $\mathbb{P}(\rho_2(P_N) > \rho_{\min}) \to 1$ for every $\rho_{\min} > 0$.  
Third, for exact near-lightlike mesoscopic interval asymptotics under i.i.d. binomial sprinkling: let $V := \operatorname{Vol}(\Omega)$ and $\mu_{\rm comp} := \mathbb{P}(Z_1 \sim Z_2) \in (0, 1)$. For $\delta_{\rm bulk} \in [0, \delta_0(\Omega))$ (including all $\delta_{\rm bulk} \in [0, 1/4)$ on $D_d$ and $\Omega_L$, since $2^{-d} \ge \frac{1}{2}f(d) > \frac{1}{4}\cdot\frac{1}{2}f(d)$ near $(1/2, \mathbf{0}) \in D_d$ and $\frac{(1/3)^2}{L} = \frac{1}{9L} > \frac{1}{4}\cdot\frac{4L - 1}{12 L^2}$ on $(3/8, 1/2) \times (3/8, L - 3/8)$ with $T_0 = 1/24$ in $\Omega_L$), there exist $T_0 = \Theta(1) > 0$, slack $\eta > 0$, and a positive-measure interior bulk core $\Omega_{\rm core} \subset \Omega$ such that for every $u \in \Omega_{\rm core}$, its forward truncated cone $C(u; T_0) := \{u + (\Delta t, \Delta\mathbf{x}) : 0 < r = \lVert\Delta\mathbf{x}\rVert_2 < \Delta t < T_0\}$ lies inside $\Omega$ with $\mathcal{A}(u, v) \subset \Omega$ unclipped and $\operatorname{Vol}(J^-(u) \cap \Omega)/V,\; \operatorname{Vol}(J^+(v) \cap \Omega)/V \ge (\delta_{\rm bulk} + \eta)\frac{1}{2}\mu_{\rm comp}$ for all $v \in C(u; T_0)$. An unclipped $d$-dimensional Minkowski diamond of proper time $\tau = \sqrt{\Delta t^2 - r^2} > 0$ has volume $\operatorname{Vol}(\mathcal{A}(u, v)) = c_d \tau^d$ with $c_d = \frac{\omega_{d-1}}{2^{d-1} d}$ ($\omega_{d-1} := \pi^{(d-1)/2}/\Gamma(\frac{d+1}{2})$). Writing $t := \Delta t$ and changing variables from $(t, r)$ to $(t, w)$ with $w := t^2 - r^2 \in [\tau_-^2, \tau_+^2]$ ($\tau_\pm := (v_\pm / c_d)^{1/d}$, $v_\pm \propto N^{\alpha - 1}$ with $v_-/v_+ = \Theta(1)$, using $d^{d-1}(\Delta\mathbf{x}) = (d - 1)\omega_{d-1} r^{d-2}\,dr = \frac{(d - 1)\omega_{d-1}}{2}(t^2 - w)^{\frac{d - 3}{2}}\,dw$) yields the exact forward shell volume:
$$
M_d(\tau_-, \tau_+; T_0) := \operatorname{Vol}\bigl(\{v \in C(u; T_0) : v_- \le \operatorname{Vol}(\mathcal{A}(u, v)) \le v_+\}\bigr) = \frac{(d - 1)\omega_{d-1}}{2} \int_{\tau_-^2}^{\tau_+^2} \left(\int_{\sqrt{w}}^{T_0} (t^2 - w)^{\frac{d - 3}{2}}\,dt\right) dw.
$$
- For $d = 2$ ($\omega_1 = 2$, $c_2 = 1/2$, $\tau_\pm^2 = 2 v_\pm$), near-lightlike pairs hugging $r \approx t$ out to height $T_0$ yield $\int_{\sqrt{w}}^{T_0} (t^2 - w)^{-1/2}\,dt = \operatorname{arccosh}(T_0/\sqrt{w}) = \frac{1}{2}\ln(1/w) + \ln(2 T_0) + O(w)$, so integrating over $w \in [2 v_-, 2 v_+]$ gives $M_2(\tau_-, \tau_+; T_0) = (v_+ - v_-)\ln(1/v_+) + O(v_+) = \Theta(N^{\alpha - 1}\ln N)$. Moreover, on $D_2$ in null coordinates $(\xi, \eta) = (t + x, t - x) \in (0, 1)^2$ (where uniform measure on $D_2$ pushes forward to $\operatorname{Unif}((0, 1)^2)$ and $\operatorname{Vol}(\mathcal{A}(Z_1, Z_2))/V = \lvert\xi_2 - \xi_1\rvert\,\lvert\eta_2 - \eta_1\rvert$ on $(\xi_2 - \xi_1)(\eta_2 - \eta_1) > 0$), integrating $2(1 - a)(1 - b)$ over $0 < a, b < 1$ with $a b \le v$ gives the exact closed-form unordered comparable pair-volume CDF:
  $$
  F_{D_2}(v) := \mathbb{P}\bigl(Z_1 \sim Z_2,\; \operatorname{Vol}(\mathcal{A}(Z_1, Z_2))/V \le v\bigr) = (2v + v^2)\ln(1/v) - 2v + \frac{5}{2}v^2 \qquad (0 < v \le 1),
  $$
  satisfying $F_{D_2}(1) = \frac{1}{2} = f(2)$ and $F_{D_2}(v_+ / V) - F_{D_2}(v_- / V) = \Theta(N^{\alpha - 1}\ln N)$.
- For $d \ge 3$, $\frac{d - 3}{2} \ge 0$ gives $\int_{\sqrt{w}}^{T_0} (t^2 - w)^{\frac{d - 3}{2}}\,dt = \frac{T_0^{d - 2}}{d - 2} + o(1)$ as $w \to 0^+$, so near-lightlike pairs along the $(d - 2)$-dimensional null sphere yield $M_d(\tau_-, \tau_+; T_0) = \Theta(v_+^{2/d} - v_-^{2/d}) = \Theta\bigl(N^{-\frac{2(1 - \alpha)}{d}}\bigr)$.
- For matching global upper bounds and variance control, let $p_N(2) := N^{\alpha - 1}\ln N$ and $p_N(d) := N^{-\frac{2(1 - \alpha)}{d}}$ ($d \ge 3$). On $D_d$, causal convexity ensures $\mathcal{A}(u, v) \subset D_d$ and $\Delta t < 1$ for every $u \prec v$, bounding the forward shell volume uniformly over all $u \in D_d$ by $M_d(0, \tau_+; 1) = O(p_N(d))$. On $\Omega_L = [0, 1] \times [0, L]$ ($L \ge 1$), any comparable pair $u = (t_1, x_1) \prec v = (t_2, x_2)$ has null increments $\Delta\xi := (t_2 - t_1) + (x_2 - x_1) > 0$, $\Delta\eta := (t_2 - t_1) - (x_2 - x_1) > 0$, full diamond area $A_{\rm full} = \frac{1}{2}\Delta\xi\,\Delta\eta$, left corner $x_L = x_1 - \frac{1}{2}\Delta\eta = x_2 - \frac{1}{2}\Delta\xi$, and right corner $x_R = x_1 + \frac{1}{2}\Delta\xi = x_2 + \frac{1}{2}\Delta\eta$; since $x_R - x_L = t_2 - t_1 \le 1 \le L$, at most one lateral wall $x = 0$ or $x = L$ clips $\mathcal{A}(u, v)$, and whenever $x_L < 0$ (with $x_1, x_2 \ge 0$), the clipped right triangle $\mathcal{A}(u, v) \cap \{x < 0\}$ has area $A_{\rm clip} = (-x_L)^2 \le \frac{1}{4}\min(\Delta\xi, \Delta\eta)^2 \le \frac{1}{2}A_{\rm full}$ (symmetrically $(x_R - L)^2 \le \frac{1}{2}A_{\rm full}$ when $x_R > L$), so $\frac{1}{2}A_{\rm full} \le \operatorname{Area}(\mathcal{A}(u, v) \cap \Omega_L) \le A_{\rm full}$ globally on $\Omega_L$, bounding the forward shell area uniformly over $u \in \Omega_L$ by $M_2(0, \sqrt{4 v_+}; 1) = O(p_N(2))$. Now fix $\varepsilon \in \bigl(0, \min(\frac{\eta}{2}, \frac{c_+ - c_-}{2(c_+ + c_-)})\bigr)$. Conditioned on $(Z_i, Z_j) = (u, v)$ with $u \prec v$, $\lvert I(Z_i, Z_j)\rvert \sim \operatorname{Binomial}\bigl(N - 2, \operatorname{Vol}(\mathcal{A}(u, v) \cap \Omega)/V\bigr)$. Defining tightened inner and relaxed outer continuum pair indicators $h_N^{\rm inner}(u, v) \le h_N^{\rm outer}(u, v)$ that depend **only** on $(u, v)$ via $(N - 2)\operatorname{Vol}(\mathcal{A}(u, v) \cap \Omega)/V \in \bigl[\frac{c_-}{1 \mp \varepsilon}N^\alpha, \frac{c_+}{1 \pm \varepsilon}N^\alpha\bigr]$ and $\operatorname{Vol}(J^\pm \cap \Omega)/V \ge (\delta_{\rm bulk} \pm \varepsilon)\frac{1}{2}\mu_{\rm comp}$ (omitting the lower bulk shift when $\delta_{\rm bulk} = 0$), multiplicative binomial Chernoff bounds (using binomial monotonicity in $p$ for arbitrarily small volumes) union-bounded over all $N(N - 1)$ ordered pairs and $N$ vertices—together with Hoeffding concentration of $\overline{J}_N / (N - 1) = \frac{1}{2}R_2(P_N)$—sandwich $\lvert\mathcal{J}_N\rvert$ with probability $1 - O(N^2 e^{-\gamma N^\alpha}) = 1 - o(1)$ ($\gamma > 0$, using $N^\alpha \gg \ln N$ for $\alpha \in (0, 1)$) between genuine symmetric 2-point U-statistics $U_N^{\rm inner} \le \lvert\mathcal{J}_N\rvert \le U_N^{\rm outer}$, where $U_N^{\bullet} := \sum_{1 \le i < j \le N} \bar{h}_N^{\bullet}(Z_i, Z_j)$ and $\bar{h}_N^{\bullet}(z_1, z_2) := h_N^{\bullet}(z_1, z_2) + h_N^{\bullet}(z_2, z_1) \in \{0, 1\}$. On $D_d$ ($d \ge 2$) and $\Omega_L$ ($L \ge 1$, $d = 2$), $\mathbb{E}[\bar{h}_N^{\bullet}(Z_1, Z_2)] = \Theta(p_N(d))$ and $\sup_{z_1 \in \Omega}\mathbb{E}[\bar{h}_N^{\bullet}(z_1, Z_2)] = O(p_N(d))$, so $\mathbb{E}[U_N^{\bullet}] = \Theta(N^2 p_N(d))$. Because disjoint pairs $(Z_1, Z_2)$ and $(Z_3, Z_4)$ are independent in $U_N^{\bullet}$, single-shared-endpoint covariances satisfy $\operatorname{Cov}(\bar{h}_N^{\bullet}(Z_1, Z_2), \bar{h}_N^{\bullet}(Z_1, Z_3)) = \operatorname{Var}(\mathbb{E}[\bar{h}_N^{\bullet}(Z_1, Z_2)\mid Z_1]) = O(p_N(d)^2)$, giving
  $$
  \frac{\operatorname{Var}(U_N^{\bullet})}{\mathbb{E}[U_N^{\bullet}]^2} = O\!\left(\frac{1}{N^2 p_N(d)} + \frac{1}{N}\right) = O(N^{-1}) \xrightarrow[N \to \infty]{} 0
  $$
  (since $N^2 p_N(d) \gg N$ for all $d \ge 2$ and $\alpha \in (0, 1)$), which establishes both the exact $\Theta_{\mathbb{P}}(N^2 p_N(d))$ rates on $D_d$ and $\Omega_L$ and $\lvert\mathcal{J}_N\rvert \xrightarrow{\mathbb{P}} \infty$ on every domain $\Omega$.

Finally, for items (1) and (2): by U-statistic concentration for bounded symmetric degree-$2$ kernels ($h(z_1, z_2) = \mathbf{1}\{z_1 \sim z_2\} \in \{0, 1\}$), Hoeffding's variance decomposition gives $\mathbb{E}[R_2(P_N)] = \mathbb{P}(Z_1 \sim Z_2)$ and $\operatorname{Var}(R_2(P_N)) \le \frac{2}{N} = O(N^{-1})$ on any domain $\Omega$. For internal intervals, conditional on $Z_i = u \prec Z_j = v$ and $\lvert I(Z_i, Z_j)\rvert = m \ge 2$, the $m$ interior points in $I(Z_i, Z_j)$ are i.i.d. uniform on $\mathcal{A}(u, v) \cap \Omega$ with conditional expectation $\mu(u, v) := \mathbb{P}_{W_1, W_2 \sim \operatorname{Unif}(\mathcal{A}(u, v) \cap \Omega)}(W_1 \sim W_2)$. Changing one of those $m$ interior points alters at most $m - 1$ pair comparabilities, shifting $R_2(I) = \binom{m}{2}^{-1} C_1(I)$ by at most $\frac{m - 1}{\binom{m}{2}} = \frac{2}{m}$. McDiarmid's bounded-differences inequality ($\sum_{a=1}^m (2/m)^2 = 4/m$) gives $\mathbb{P}(\lvert R_2(I) - \mu(u, v)\rvert > \epsilon \mid Z_i = u, Z_j = v, m) \le 2 e^{-\epsilon^2 m / 2}$, so union-bounding over all $\binom{N}{2}$ unordered pairs yields
$$
\max_{\{i, j\} : \lvert I(Z_i, Z_j)\rvert \ge c_- N^\alpha} \bigl\lvert R_2\bigl(I(Z_i, Z_j)\bigr) - \mu(Z_i, Z_j)\bigr\rvert \xrightarrow[N \to \infty]{\mathbb{P}} 0
$$
uniformly (including for arbitrarily boosted near-lightlike intervals), since $\binom{N}{2} e^{-\frac{1}{2}c_- \epsilon^2 N^\alpha} \to 0$ for every $\epsilon > 0$ and $\alpha \in (0, 1)$.
1. In $D_d$, $\mathbb{P}(Z_1 \sim Z_2) = f(d)$ (Myrheim 1978; Meyer 1988). For any two comparable points $u \prec v$ in $D_d$—including arbitrarily boosted near-lightlike pairs—causal convexity gives $\mathcal{A}(u, v) \subset D_d$, and an affine Poincaré transformation plus uniform dilation (constant Jacobian determinant) maps $\mathcal{A}(u, v)$ onto $D_d$ while preserving normalized Lebesgue measure, so $\mu(u, v) \equiv f(d)$. Uniform McDiarmid concentration together with $\lvert\mathcal{J}_N\rvert \xrightarrow{\mathbb{P}} \infty$ immediately gives $\overline{R}_{\rm int}(P_N) \xrightarrow{\mathbb{P}} f(d)$, $\operatorname{Var}_{\rm within}(R_2(I); \omega) \xrightarrow{\mathbb{P}} 0$, and (by bounded convergence since $0 \le \overline{R}_{\rm int} \le 1$) $\operatorname{Var}_{\rm between}(\overline{R}_{\rm int}(P_N)) \to 0$.
2. On $\Omega_L = [0, 1] \times [0, L]$ ($L \ge 1$), let $(T_1, X_1), (T_2, X_2)$ be independent uniform points. Then $U := \lvert T_2 - T_1\rvert \in (0, 1)$ has density $g_U(u) = 2(1 - u)$ on $(0, 1)$, and independent $X_1, X_2 \sim \operatorname{Unif}(0, L)$ satisfy $\mathbb{P}(\lvert X_2 - X_1\rvert < u) = \frac{2u}{L} - \frac{u^2}{L^2}$ for all $u \in (0, 1] \subseteq (0, L]$. Integrating over $u \in (0, 1)$ gives:
$$
R_{\rm global}^*(\Omega_L) = \int_0^1 2(1 - u)\left(\frac{2u}{L} - \frac{u^2}{L^2}\right) du = \frac{4}{L}\int_0^1 (u - u^2)\,du - \frac{2}{L^2}\int_0^1 (u^2 - u^3)\,du = \frac{4}{6L} - \frac{2}{12 L^2} = \frac{4L - 1}{6 L^2}.
$$
At $L = 3$, $R_{\rm global}^*(\Omega_3) = \frac{11}{54} \approx 0.203704$ (at $L = 1$, $R_{\rm global}^*(\Omega_1) = 1/2$, while for every $L > 1$ wide spatial separation suppresses global comparability strictly below $1/2$). On the high-probability Chernoff outer event for $\mathcal{J}_N(\omega)$ ($m \in [c_- N^\alpha, c_+ N^\alpha]$), every pair $(u, v) \in \mathcal{J}_N(\omega)$ satisfies $\frac{1}{2}\Delta\xi\,\Delta\eta = A_{\rm full}(u, v) \le 2\operatorname{Area}(\mathcal{A}(u, v) \cap \Omega_L) = O(N^{-(1 - \alpha)})$ uniformly. Using $A_{\rm clip} \le \frac{1}{4}\min(\Delta\xi, \Delta\eta)^2$ and $A_{\rm full} = \frac{1}{2}\max(\Delta\xi, \Delta\eta)\min(\Delta\xi, \Delta\eta)$: (i) for near-lightlike pairs with $\max(\Delta\xi, \Delta\eta) \ge N^{-(1 - \alpha)/4}$, $\min(\Delta\xi, \Delta\eta) = O(N^{-3(1 - \alpha)/4})$, so relative wall clipping satisfies $\frac{A_{\rm clip}}{A_{\rm full}} \le \frac{\min(\Delta\xi, \Delta\eta)}{2\max(\Delta\xi, \Delta\eta)} = O(N^{-(1 - \alpha)/2}) \to 0$, whence $\lvert\mu(u, v) - \frac{1}{2}\rvert \le 4(A_{\rm clip}/A_{\rm full}) = O(N^{-(1 - \alpha)/2}) \to 0$ uniformly; (ii) for small-diameter pairs with $\max(\Delta\xi, \Delta\eta) < N^{-(1 - \alpha)/4}$, $\mathcal{A}(u, v) \subset \Omega_L$ is completely unclipped ($\mu(u, v) = f(2) = 1/2$) outside the vanishing spatial boundary strips $x_1 \in [0, \frac{1}{2}N^{-(1 - \alpha)/4}) \cup (L - \frac{1}{2}N^{-(1 - \alpha)/4}, L]$, which contain at most $O_{\mathbb{P}}(N^{1 + \alpha - (1 - \alpha)/4}\ln N) = o_{\mathbb{P}}(\lvert\mathcal{J}_N\rvert)$ pairs. Combining $\mu(u, v) \to 1/2$ outside this $o_{\mathbb{P}}(\lvert\mathcal{J}_N\rvert)$ boundary subset with uniform McDiarmid concentration $\max_{(u, v) \in \mathcal{J}_N}\lvert R_2(I(u, v)) - \mu(u, v)\rvert \xrightarrow{\mathbb{P}} 0$ and $0 \le R_2(I) \le 1$ yields $\overline{R}_{\rm int}(P_N) \xrightarrow{\mathbb{P}} 1/2 \ne \frac{11}{54}$, $\operatorname{Var}_{\rm within}(R_2(I); \omega) \xrightarrow{\mathbb{P}} 0$, and $\operatorname{Var}_{\rm between}(\overline{R}_{\rm int}(P_N)) \to 0$. $\blacksquare$

---

## 4. Intrinsic Subset-Restriction Kernel $K_N$ vs. Physical Nested Regimes

Before testing growth laws against `CR-1`, we clarify the exact mathematical status of the linear-extension deletion kernel $K_N$ established in [intrinsic_subset_restriction.md](intrinsic_subset_restriction.md) (`QR-LD036`).

### 4.1 Self-Contained Proof of Marginal Readout Consistency ($\mu_N K_N = \mu_{N-1}$)
Let $L(P)$ denote the number of linear extensions of an unmarked $N$-vertex poset $P$ ($L(\varnothing) := 1$). Partitioning linear extensions by their final element $v \in \operatorname{Max}(P)$ gives the fundamental identity $L(P) = \sum_{v \in \operatorname{Max}(P)} L(P \setminus v)$. Define the stochastic transition kernel $K_N([P], [Q])$ from unmarked $N$-vertex isomorphism types $[P]$ to $(N-1)$-vertex isomorphism types $[Q]$ by:
$$
K_N([P], [Q]) := \frac{1}{L(P)} \sum_{v \in \operatorname{Max}(P)} L(P \setminus v)\,\mathbf{1}\{P \setminus v \cong Q\}.
$$

**Theorem 4.1 (`[PROVED THEOREM]` Exact Marginal Consistency of Subset-Weight CSG; `QR-LD036` Eqs. (2)–(6)).**  
*Let $(t_k)_{k \ge 0}$ be any strictly positive subset-weight sequence ($t_0 = 1, t_k > 0$), and let $\mu_N$ denote the endpoint distribution over unmarked $N$-element poset isomorphism classes generated by $q(P_n, S) = G(\lvert S\rvert, \lvert\operatorname{Max}(S)\rvert)/Z_n$. Then at every finite horizon $N \ge 1$:*
$$
\mu_N K_N = \mu_{N-1}.
$$

*Proof.*  
Fix any naturally labeled $N$-element poset $P$ on $\{0, \dots, N-1\}$. For each vertex $v \in P$, its strict causal past at the moment of its birth in *any* linear extension of $P$ is $S_v = J^-(v)$, with cardinality $s_v = \lvert J^-(v)\rvert$ and maximal antichain size $m_v = \lvert\operatorname{Max}(J^-(v))\rvert$; incomparable vertices born before $v$ change only the stage denominator $Z_n$. Because each stage size $n = 0, 1, \dots, N-1$ occurs once along any $N$-step birth history, every canonical natural encoding of $[P]$ has identical history probability:
$$
W_N(P) = \frac{\prod_{v \in P} G(s_v, m_v)}{\prod_{n=0}^{N-1} Z_n}.
$$
The automorphism group $\operatorname{Aut}(P)$ acts freely on the $L(P)$ linear extensions of $P$, partitioning them into $L(P)/\lvert\operatorname{Aut}(P)\rvert$ distinct canonical encodings, so $\mu_N([P]) = \frac{L(P)}{\lvert\operatorname{Aut}(P)\rvert} W_N(P)$. Conditioned on $[P]$, choosing a linear extension uniformly at random and deleting its last vertex $v \in \operatorname{Max}(P)$ selects $v$ with probability $L(P \setminus v)/L(P)$—which is precisely $K_N([P], \cdot)$—and induces the uniform distribution over canonical encodings of the $(N-1)$-step prefix, whose marginal over $[P] \sim \mu_N$ equals $\mu_{N-1}$ because $\sum_{S \in \mathcal{I}(P_{N-1})} q(P_{N-1}, S) = 1$. $\blacksquare$

**Explicit $N = 3 \to 2$ Control (`QR-LD036` §5):** Writing $a = t_1 > 0$, $b = t_2 > 0$, and $H = (1 + a)(1 + 2a + b) = Z_1 Z_2$, the five unmarked $3$-vertex posets illustrate why $K_3$ differs from uniform maximal deletion:

| $3$-Vertex Poset $P$ | $\mu_3([P])$ | $L(P)$ | Chain $[C_2]$ Prob. Under $K_3$ | Chain $[C_2]$ Prob. Under Uniform Maximal Deletion |
|---|---|---|---|---|
| Antichain $A_3$ | $1/H$ | $6$ | $0$ | $0$ |
| Edge $u \prec v$ + isolate $w$ | $3a/H$ | $3$ | $1/3$ ($w$ has weight $1/3$, $v$ has $2/3$) | $1/2$ (uniform over $\{v, w\}$) |
| Fork ($u \prec v_1, v_2$) | $a^2/H$ | $2$ | $1$ | $1$ |
| Join ($u_1, u_2 \prec v$) | $b/H$ | $2$ | $0$ | $0$ |
| Chain $C_3$ | $a(a + b)/H$ | $1$ | $1$ | $1$ |

*(Note: `QR-LD036` §5 compares $K_3$ against uniform deletion over **all $3$ vertices** of $P$, which yields discrepancy $(2b - a^2)/(3H)$; uniform deletion over **maximal** vertices already fails on the edge-plus-isolate poset $E$, giving chain mass $\frac{3a/2 + a^2 + a(a+b)}{H} = \frac{a}{1+a} + \frac{a}{2H} \ne \frac{a}{1+a} = \mu_2([C_2])$!)*

### 4.2 Why $K_N$ Is Strictly a Mathematical Readout, Not a Physical Map Between Nested Regimes
As emphasized in [intrinsic_subset_restriction.md](intrinsic_subset_restriction.md) §6, $K_N$ must **not** be conflated with a physical restriction map onto internal nested causal regimes:
1. **Boundary Prefix Projection vs. Internal Two-Sided Conditioning:** $K_N$ deletes a *maximal* boundary element $v \in \operatorname{Max}(P_N)$ weighted by global linear-extension counts $L(P_N \setminus v)/L(P_N)$, recovering the $(N-1)$-birth marginal $\mu_{N-1}$. By contrast, an internal causal interval $I(u, v) = J^+(u) \cap J^-(v)$ conditions simultaneously on a **past cap $u$** and a **future cap $v$**.
2. **Global Non-Locality of $L(P)$:** Computing $L(P \setminus v)/L(P)$ is `#P`-complete in general and depends on spacelike structure arbitrarily far from $v$; no local growth step has operational access to $K_N$.
3. **Failure to Enforce `CR-1`:** Every positive sequence $(t_k)_{k \ge 0}$ satisfies $\mu_N K_N = \mu_{N-1}$ identically—including fixed-$p$ percolation ($R_2 \to 1$), finite-cutoff CSG ($R_2 \to 0$), and the non-diamond `QR-LD037` perturbation ($\mu_n K_n = \mu_{n-1}$ for $1 \le n \le 4$). Thus `CR-1d` must be defined directly on internal Alexandrov intervals $I(u, v)$ as in §3.1, not via $K_N$.

---

## 5. Exact Scope of Analytical Exclusions Under `CR-1`

We now prove what `CR-1` rigorously excludes, stating the exact mathematical scope of every exclusion without overclaiming.

### 5.1 Non-Diamond Finite Perturbations (`QR-LD037`) Fail `CR-1a`
**Proposition 5.1 (`[COUNTEREXAMPLE / OBSTRUCTION]` Exclusion of `QR-LD037` by `CR-1a`).**  
*The 4-birth mark-independent order-covariant perturbation in [intrinsic_law_selection_limits.md](intrinsic_law_selection_limits.md) (`QR-LD037` §2–4) satisfies $\mu_n K_n = \mu_{n-1}$ for $1 \le n \le 4$ and reproduces the exact baseline endpoint measure $\mu_4$, yet violates `CR-1a` on the $2$-element antichain $C = A_2 = \{0, 1\}$ with ideals $S = \{0\}$ and $T = \varnothing$:*
$$
\Pi_1 = q(A_2, \{0\})\, q(E, \varnothing) = \frac{1}{4}\cdot\frac{3}{32} = \frac{3}{128} \ne \frac{5}{128} = \frac{1}{4}\cdot\frac{5}{32} = q(A_2, \varnothing)\, q(A_3, \{0\}) = \Pi_2.
$$

*Proof.* Under `QR-LD037` §2, $q(A_2, \{0\}) = q_*(A_2, \{0\}) = 2^{-(2 - 1 + 1)} = 1/4$ and $q(A_2, \varnothing) = 2^{-(2 - 0 + 0)} = 1/4$. Adjoining $x$ above $\{0\}$ produces the edge-plus-isolate poset $E$, where `QR-LD037` sets $q(E, \varnothing) = 3/32$; adjoining $y$ above $\varnothing$ produces the $3$-antichain $A_3$, where `QR-LD037` sets $q(A_3, \{0\}) = 5/32$. Both two-step paths construct the identical unmarked $4$-element poset $X$ (one edge and two isolates), yet $\Pi_1 = 3/128 \ne 5/128 = \Pi_2$ (verified numerically in `verify_exact_diamond_and_readout_properties()`). $\blacksquare$

### 5.2 Fixed-$p$ Percolation CSG ($t_k = (\frac{p}{1-p})^k$) Fails `CR-1b` via 2-Hop Saturation
**Theorem 5.2 (`[PROVED THEOREM]` Exact Equivalence with Transitive Percolation and $R_2(P_N) \to 1$ Saturation).**  
*Fix $p \in (0, 1)$ and consider the subset-weight CSG law with $t_k = \bigl(\frac{p}{1 - p}\bigr)^k$ ($k \ge 0$).*
1. *(Equivalence with Transitive Bernoulli($p$) Percolation): At every birth step $n \ge 1$, $Z_n = (1 - p)^{-n}$, $\pi_n(k) = \binom{n}{k} p^k (1 - p)^{n - k}$, and the seed set $B_n \subseteq \{0, \dots, n-1\}$ consists of independent $\operatorname{Bernoulli}(p)$ directed edges $u \to n$, followed by transitive closure $S_n = J^-[B_n]$.*
2. *(Non-Asymptotic 2-Hop Saturation Bound): For every $N \ge 2$ and every $0 \le u < v < N$:*
   $$
   \mathbb{P}(u \not\prec v) \le (1 - p)\,(1 - p^2)^{v - u - 1},
   $$
   *whence:*
   $$
   1 - \mathbb{E}[R_2(P_N)] \le \frac{2(1 - p)}{p^2 N} \xrightarrow[N \to \infty]{} 0, \qquad R_2(P_N) \xrightarrow[N \to \infty]{\mathbb{P}} 1.
   $$
   *Consequently, fixed-$p$ percolation CSG violates `CR-1b` ($R_{\rm global}^* = 1 \notin (0, 1)$) for every $p \in (0, 1)$.*

*Proof.*  
1. By the binomial theorem, $Z_n = \sum_{k=0}^n \binom{n}{k} \bigl(\frac{p}{1-p}\bigr)^k = \bigl(1 + \frac{p}{1-p}\bigr)^n = (1 - p)^{-n}$. Therefore, for every subset $B \subseteq \{0, \dots, n-1\}$ of size $k = \lvert B\rvert$, its selection probability in the Rideout–Sorkin subset representation (§2.2) is $\frac{\pi_n(k)}{\binom{n}{k}} = \frac{t_k}{Z_n} = p^k (1 - p)^{n - k}$. Thus the indicators $\{\mathbf{1}\{u \in B_n\} : 0 \le u < n, 1 \le n < N\}$ are i.i.d. $\operatorname{Bernoulli}(p)$ random variables, and $u \prec v$ holds in $P_N$ iff there is a directed path $u = v_0 \to v_1 \to \dots \to v_\ell = v$ of open $\operatorname{Bernoulli}(p)$ edges.
2. Fix $0 \le u < v < N$. If $u \not\prec v$, then the direct edge $u \to v$ must be closed (probability $1 - p$), and for each intermediate vertex $w \in \{u + 1, \dots, v - 1\}$ at least one of the two edges $u \to w$ or $w \to v$ must be closed (probability $1 - p^2$ for each $w$). Because the edge pairs $\{(u, v)\} \cup \{\{(u, w), (w, v)\} : u < w < v\}$ are pairwise disjoint, mutual independence of the $\operatorname{Bernoulli}(p)$ edges gives:
$$
\mathbb{P}(u \not\prec v) \le \mathbb{P}\bigl(u \not\to v \text{ and } \forall\, w \in (u, v),\; \neg(u \to w \wedge w \to v)\bigr) = (1 - p)\,(1 - p^2)^{v - u - 1}.
$$
Summing over $0 \le u < v < N$ with $d = v - u \ge 1$ yields:
$$
\sum_{0 \le u < v < N} \mathbb{P}(u \not\prec v) \le (1 - p)\sum_{u=0}^{N-2} \sum_{d=1}^{N - 1 - u} (1 - p^2)^{d - 1} \le \frac{(1 - p)(N - 1)}{p^2}.
$$
Dividing by $\binom{N}{2} = \frac{N(N - 1)}{2}$ gives $1 - \mathbb{E}[R_2(P_N)] \le \frac{2(1 - p)}{p^2 N} \to 0$. Since $0 \le 1 - R_2(P_N) \le 1$, Markov's inequality implies $\mathbb{P}(1 - R_2(P_N) > \epsilon) \le \frac{2(1 - p)}{\epsilon p^2 N} \to 0$ for every $\epsilon > 0$, so $R_2(P_N) \xrightarrow{\mathbb{P}} 1$. $\blacksquare$

*Remark 5.2.1 (Scope Correction on Parent Counts, Global Posts, and Kleitman–Rothschild Posets):*  
Two distinct conflations must be avoided here:
1. **What $\mathbb{E}_{\pi_n}[K_n] = p n$ Does and Does Not Prove:** Computing $\mathbb{E}_{\pi_n}[K_n] = p n$ alone neither proves global-post regeneration nor proves Kleitman–Rothschild behavior. In fact, transitive Bernoulli($p$) percolation *does* regenerate infinitely many global posts almost surely ($\rho_{\rm post}(P_N) \to c(p) > 0$; Alon, Bollobás, Brightwell & Janson 1994), which is a *separate, deeper* theorem not needed here because $R_2(P_N) \to 1$ already excludes the family under `CR-1b`.
2. **Transitive Percolation vs. Kleitman–Rothschild 3-Layer Posets:** Fixed-$p$ sequential percolation does **not** converge to a 3-layer Kleitman–Rothschild poset (since $R_2(P_N) \to 1$, whereas a uniform 3-layer Kleitman–Rothschild poset has $R_2(P_N) \to 3/8 = 0.375$ and $h(P_N) \le 3$). Rather, if one separately tests the uniform/3-layer Kleitman–Rothschild random poset ensemble (where vertices are partitioned into layers $L_1 \sqcup L_2 \sqcup L_3$ of sizes $\approx N/4, N/2, N/4$ with $L_1 \prec L_3$ and $\operatorname{Bernoulli}(1/2)$ edges on $L_1 \times L_2$ and $L_2 \times L_3$), that non-sequential control has interior comparability $\mathbb{E}[R_2] \to 3/8 \in (0, 1)$ and vanishing between-history variance, yet is excluded by `CR-1b` because it contains **zero 3-step chains** ($\rho_2(P_N) \equiv 0$, verified in §7.2).

### 5.3 Heterogeneous Static Mixtures vs. Single-History Concentration
By Rideout–Sorkin / de Finetti representation (`PW6A` §4.1), any relabeling-covariant, diamond-commuting static mixture $\mathbb{P}_\mu = \int \mathbb{P}_t\,d\mu(t)$ over pure CSG parameter sequences $t$ satisfies `CR-1a`. One might therefore tune a mixture average $\mathbb{E}_{\mathbb{P}_\mu}[R_2(P_N)] = r_* \in (0, 1)$ (e.g., $r_* = 1/10$). Single-history testing in `CR-1b` rules out heterogeneous mixtures whose components concentrate at distinct values:

**Proposition 5.3 (`[PROVED PROPOSITION]` Exclusion of Heterogeneous / Bimodal Static Mixtures, and Exact Scope).**  
*Let $\mathbb{P}_\mu = \int \mathbb{P}_\theta\,d\mu(\theta)$ be a static mixture such that under each pure component $\mathbb{P}_\theta$, $R_2(P_N) \xrightarrow{\mathbb{P}_\theta} r(\theta) \in [0, 1]$ as $N \to \infty$. Then by bounded convergence:*
$$
\lim_{N \to \infty} \operatorname{Var}_{\rm between}\bigl(R_2(P_N)\bigr) = \int \bigl(r(\theta) - \bar{r}\bigr)^2\,d\mu(\theta) = \operatorname{Var}_\mu\bigl(r(\Theta)\bigr), \qquad \bar{r} := \int r(\theta)\,d\mu(\theta).
$$
*Consequently:*
1. *Every heterogeneous mixture with $\operatorname{Var}_\mu(r(\Theta)) > 0$ violates `CR-1b` ($\lim_{N\to\infty}\operatorname{Var}_{\rm between}(R_2(P_N)) > 0$). In particular, an $\alpha$-chain / $(1-\alpha)$-antichain mixture with $\alpha = 1/10$ achieves exact ensemble mean $\mathbb{E}[R_2(P_N)] \equiv 1/10 = f(4)$ for all $N \ge 2$, yet every individual history satisfies $R_2(P_N(\omega)) \in \{0, 1\}$ and $\operatorname{Var}_{\rm between}(R_2(P_N)) = \alpha(1 - \alpha) = 0.09 \not\to 0$; likewise, the two-point quantum-steered mixture of `PW6A` Theorem 4.2 ($r(\theta_\pm) = r_\pm$, $r_+ \ne r_-$) has $\lim_{N\to\infty}\operatorname{Var}_{\rm between} = p_+(1 - p_+)(r_+ - r_-)^2 > 0$.*
2. *(Exact Scope): Proposition 5.3 excludes **only** mixtures for which $r(\Theta)$ is non-degenerate under $\mu$. It does **not** exclude degenerate (pure) CSG laws $\mu = \delta_t$ or mixtures supported entirely on a level set $\{\theta : r(\theta) = r_*\}$, which must be tested individually on their asymptotic $r(\theta)$ and sub-interval behavior.*

*Proof.* Since $0 \le R_2(P_N) \le 1$ for all $N \ge 2$, under each $\mathbb{P}_\theta$ convergence $R_2(P_N) \xrightarrow{\mathbb{P}_\theta} r(\theta)$ implies $\mathbb{E}_{\mathbb{P}_\theta}[R_2(P_N)] \to r(\theta)$ and $\mathbb{E}_{\mathbb{P}_\theta}[R_2(P_N)^2] \to r(\theta)^2$. Applying the dominated convergence theorem over $\theta \sim \mu$ gives $\lim_{N\to\infty}\mathbb{E}_{\mathbb{P}_\mu}[R_2(P_N)] = \bar{r}$ and $\lim_{N\to\infty}\mathbb{E}_{\mathbb{P}_\mu}[R_2(P_N)^2] = \int r(\theta)^2\,d\mu(\theta)$, yielding $\lim_{N\to\infty}\operatorname{Var}_{\rm between}(R_2(P_N)) = \operatorname{Var}_\mu(r(\Theta))$. $\blacksquare$

### 5.4 Finite-Cutoff CSG ($k_{\rm max} = 1$ and $k_{\rm max} \ge 2$) and the Universal Sub-Logarithmic Parent-Count No-Go

For finite-cutoff subset-weight CSG ($t_k = 0$ for all $k > k_{\rm max}$), `PW6A` Theorem 7.3B' establishes distinct decay rates for the special case $k_{\rm max} = 1$ and for $k_{\rm max} \ge 2$. In addition, at $k_{\rm max} = 1$ we prove an exact finite-$N$ identity for internal intervals, and in Theorem 5.5 we extend comparability collapse to **all** unbounded subset-weight laws with sub-logarithmic expected parent count $\mathbb{E}_{\pi_n}[K_n] = o(\ln n)$.

**Theorem 5.4 (`[PROVED THEOREM]` Finite-Cutoff CSG Collapse at $k_{\rm max} = 1$ vs. $k_{\rm max} \ge 2$, and Exact $k_{\rm max} = 1$ Spine Identity).**  
*Let $(t_k)_{k \ge 0}$ ($t_0 = 1, t_k \ge 0$) satisfy $t_k = 0$ for all $k > k_{\rm max}$, where $k_{\rm max} \ge 1$ is fixed.*
1. *(Special Case $k_{\rm max} = 1$ — Logarithmic-Over-Linear Decay & Exact Tree-Interval Identity): When $k_{\rm max} = 1$, for every $N \ge 2$:*
   $$
   \mathbb{E}[R_2(P_N)] \le \frac{2 H_{N-1}}{N} \le \frac{2(1 + \ln N)}{N} = O\!\left(\frac{\ln N}{N}\right) \xrightarrow[N \to \infty]{} 0,
   $$
   *where $H_{N-1} = \sum_{r=1}^{N-1} \frac{1}{r}$ (see [PW6A_PROTOCOL.md](../../PW6A_PROTOCOL.md) Theorem 7.3B'(1)). Moreover, **deterministically for every finite $N$, every realization $\omega$, and every comparable pair $u \prec v$ with $m = \lvert I(u, v)\rvert \ge 2$**:*
   $$
   R_2\bigl(I(u, v)\bigr) \equiv 1.
   $$
   *Hence $k_{\rm max} = 1$ simultaneously fails `CR-1b` ($R_{\rm global}^* = 0$) and `CR-1d` ($R_{\rm int}^* = 1$).*
2. *(General Finite Cutoff $k_{\rm max} \ge 2$ — Power-Law Decay): For every fixed integer $k_{\rm max} \ge 2$ and every $N \ge 2$ ([PW6A_PROTOCOL.md](../../PW6A_PROTOCOL.md) Theorem 7.3B'(2)):*
   $$
   \mathbb{E}[R_2(P_N)] \le \frac{2}{N} + \frac{2\,k_{\rm max}^{2 + 1/k_{\rm max}}}{(k_{\rm max} - 1)(2 k_{\rm max} - 1)}\,\frac{N^{1 - 1/k_{\rm max}}}{N - 1} = O\!\left(N^{-1/k_{\rm max}}\right) \xrightarrow[N \to \infty]{} 0,
   $$
   *so $R_2(P_N) \xrightarrow{\mathbb{P}} 0$, violating `CR-1b`.*

*Proof.* The global comparability bounds in (1) and (2) are proved in full in [PW6A_PROTOCOL.md](../../PW6A_PROTOCOL.md) Theorem 7.3B' (lines 687–733) via the exact forward parent-chain union bound $\mathbb{P}(i \prec j) \le \frac{k_{\rm max}}{j}\prod_{m=i+1}^{j-1}(1 + \frac{k_{\rm max}}{m})$: at $k_{\rm max} = 1$, the product telescopes to $\frac{1}{j}\cdot\frac{j}{i+1} = \frac{1}{i+1}$ (whose sum over $i$ produces $H_{N-1}$ rather than a power law), whereas for $k_{\rm max} \ge 2$, $\prod_{m=i+1}^{j-1}(1 + \frac{k_{\rm max}}{m}) \le (j/i)^{k_{\rm max}}$ yields the integral tail $O(N^{-1/k_{\rm max}})$.  
To prove the exact interval identity $R_2(I(u, v)) \equiv 1$ at $k_{\rm max} = 1$, observe by induction on birth index $n \ge 0$ that every vertex $n$ has strict causal past $J^-(n)$ totally ordered (a finite chain): at $n = 0$, $J^-(0) = \varnothing$ is vacuously a chain; at step $n \ge 1$, $k_{\rm max} = 1$ forces $\lvert B_n\rvert \in \{0, 1\}$, so either $B_n = \varnothing$ ($J^-(n) = \varnothing$) or $B_n = \{b\}$ for a single vertex $b < n$, giving $J^-(n) = J^-(b) \cup \{b\}$, which is a total chain because $J^-(b)$ is a total chain and every $w \in J^-(b)$ satisfies $w \prec b$. Since $I(u, v) = \{z \in J^-(v) : u \prec z\} \subseteq J^-(v)$, every two distinct elements $z_1, z_2 \in I(u, v)$ belong to the total chain $J^-(v)$ and are therefore comparable, giving $C_1(I(u, v)) = \binom{m}{2}$ and $R_2(I(u, v)) = 1$. $\blacksquare$

We now prove a general analytical threshold extending Theorem 5.4 and [finite_prefix_nonidentification.md](finite_prefix_nonidentification.md) (`QR-LD032`) to **unbounded** coupling sequences:

**Theorem 5.5 (`[PROVED THEOREM]` Universal Sub-Logarithmic Parent-Count No-Go for Static Subset-Weight CSG).**  
*Let $(t_k)_{k \ge 0}$ ($t_0 = 1, t_k \ge 0$) be **any** static subset-weight CSG coupling sequence—bounded or unbounded—and let $\mu_n := \mathbb{E}_{\pi_n}[K_n] = \frac{1}{Z_n}\sum_{k=0}^n k\binom{n}{k} t_k$ denote the expected seed cardinality at birth step $n \ge 1$. If:*
$$
\lim_{n \to \infty} \frac{\mu_n}{\ln n} = 0 \qquad \bigl(\text{i.e., } \mu_n = o(\ln n)\bigr),
$$
*then $\lim_{N \to \infty} \mathbb{E}[R_2(P_N)] = 0$ and $R_2(P_N) \xrightarrow{\mathbb{P}} 0$. Consequently, $\limsup_{n \to \infty} \frac{\mathbb{E}_{\pi_n}[K_n]}{\ln n} > 0$ is a **necessary condition** for any static subset-weight CSG law to satisfy `CR-1b`.*

*Proof.*  
Fix an arbitrary $\epsilon \in (0, 1)$ and set $\delta := \epsilon / 4 \in (0, 1/4)$. For every integer $N > 4/\delta$, put $k_0(N) := \lceil \delta N\rceil \ge \delta N \ge 4$. Partition the $\binom{N}{2}$ vertex pairs $0 \le i < j < N$ into:
- **Early-origin pairs ($0 \le i < k_0(N)$):** There are $\sum_{i=0}^{k_0(N)-1}(N - 1 - i) \le k_0(N)(N - 1)$ such pairs, contributing to $\mathbb{E}[R_2(P_N)]$ at most:
  $$
  \frac{k_0(N)(N - 1)}{N(N - 1)/2} = \frac{2\lceil\delta N\rceil}{N} \le 2\delta + \frac{2}{N} = \frac{\epsilon}{2} + \frac{2}{N}.
  $$
- **Bulk pairs ($k_0(N) \le i < j < N$):** By §2.2 (`PW6A` Lemma 6.2(2)), the random subsets $(B_1, \dots, B_{N-1})$ are mutually independent across birth steps, and for each $m \in \{1, \dots, N-1\}$ and $u \in \{0, \dots, m-1\}$, symmetric $K_m$-subset sampling gives $\mathbb{P}(u \in B_m) = \frac{\mu_m}{m}$. By strong induction on $j - i \ge 1$ (`PW6A` Theorem 7.3B'), $i \prec j$ holds iff there exists a strictly increasing chain $i = v_0 < v_1 < \dots < v_\ell = j$ ($\ell \ge 1$) with $v_{r-1} \in B_{v_r}$ for every $r = 1, \dots, \ell$. Setting $M_N(\delta) := \max_{k_0(N) < m < N} \mu_m$, union-bounding over all intermediate sets $I = \{v_1, \dots, v_{\ell-1}\} \subseteq \{i + 1, \dots, j - 1\}$ yields:
  $$
  \mathbb{P}(i \prec j) \le \sum_{I \subseteq \{i+1, \dots, j-1\}} \frac{\mu_j}{j} \prod_{m \in I} \frac{\mu_m}{m} = \frac{\mu_j}{j} \prod_{m = i + 1}^{j - 1} \left(1 + \frac{\mu_m}{m}\right) \le \frac{M_N(\delta)}{\delta N} \exp\!\left(M_N(\delta) \sum_{m = k_0(N) + 1}^{N - 1} \frac{1}{m}\right).
  $$
  Because $x \mapsto 1/x$ is strictly decreasing on $(0, \infty)$ and $k_0(N) \ge \delta N$, the harmonic slice is bounded uniformly in $N$:
  $$
  \sum_{m = k_0(N) + 1}^{N - 1} \frac{1}{m} \le \int_{k_0(N)}^{N - 1} \frac{dx}{x} \le \int_{\delta N}^N \frac{dx}{x} = \ln\!\left(\frac{1}{\delta}\right).
  $$
  Now use $\lim_{m \to \infty} \frac{\mu_m}{\ln m} = 0$: since every $m \in (k_0(N), N)$ satisfies $m > \delta N \to \infty$ as $N \to \infty$ and $\ln m < \ln N$, we have $\lim_{N \to \infty} \frac{M_N(\delta)}{\ln N} = 0$. Because $\delta = \epsilon/4 > 0$ is fixed, $\ln(1/\delta) < \infty$ is fixed, so there exists $N_1(\epsilon) > 4/\delta$ such that for all $N \ge N_1(\epsilon)$, $M_N(\delta)\ln(1/\delta) \le \frac{1}{2}\ln N$, i.e., $\exp\bigl(M_N(\delta)\ln(1/\delta)\bigr) \le N^{1/2}$. Hence for all $N \ge N_1(\epsilon)$ and all $k_0(N) \le i < j < N$:
  $$
  \mathbb{P}(i \prec j) \le \frac{M_N(\delta)}{\delta N}\,N^{1/2} = \frac{M_N(\delta)}{\delta \sqrt{N}}.
  $$
Combining both regions gives, for all $N \ge N_1(\epsilon)$:
$$
\mathbb{E}[R_2(P_N)] \le \frac{\epsilon}{2} + \frac{2}{N} + \frac{M_N(\delta)}{\delta\sqrt{N}} \xrightarrow[N \to \infty]{} \frac{\epsilon}{2} < \epsilon.
$$
Since $\epsilon > 0$ was arbitrary, $\lim_{N \to \infty} \mathbb{E}[R_2(P_N)] = 0$, and Markov's inequality yields $R_2(P_N) \xrightarrow{\mathbb{P}} 0$. $\blacksquare$

*Corollary 5.5.1:* Every stretched-exponentially super-quadratic law $t_k = \exp(-\gamma k^\eta)$ with $\gamma > 0$ and $\eta > 2$ has $\mu_n = \Theta\bigl((\ln n)^{1/(\eta - 1)}\bigr) = o(\ln n)$, and every doubly-exponential law $t_k = 2^{-2^k}$ (`QR-LD032`) has $\mu_n = \Theta(\ln\ln n) = o(\ln n)$; by Theorem 5.5, all such laws collapse to $R_2(P_N) \xrightarrow{\mathbb{P}} 0$ and fail `CR-1b`.

---

## 6. Local-Cone Compensation Strictly as an Unproved Candidate (`[UNPROVED CANDIDATE]`)

In [PW6A_PROTOCOL.md](../../PW6A_PROTOCOL.md) Theorems 5.3, 5.4, and 8.1, two complementary obstacles appeared when attempting to steer single histories via local causal-past observables:
1. **Stage-Normalized Partition Obstruction (`PW6A` Theorem 5.3):** If one tilts ideal weights by a local function $w(S) > 0$ and normalizes across all ideals $S \in \mathcal{I}(P_n)$ via $q_{\rm norm}(P_n, S) = w(S)/Z(P_n)$ ($Z(P_n) := \sum_{U \in \mathcal{I}(P_n)} w(U)$), the denominator $Z(P_n)$ breaks diamond commutation generically. Specifically, already for constant weight $w \equiv 1$ on the $2$-antichain $C = A_2 = \{a, b\}$ with ideals $S = \{a\}$ and $T = \varnothing$:
   - Adjoining $x$ above $S = \{a\}$ gives the edge-plus-isolate poset $A_2 + x_{\{a\}}$ with $\lvert\mathcal{I}(A_2 + x_{\{a\}})\rvert = 6$ ideals ($\varnothing, \{a\}, \{b\}, \{a, b\}, \{a, x\}, \{a, b, x\}$);
   - Adjoining $y$ above $T = \varnothing$ gives the $3$-antichain $A_2 + y_\varnothing = A_3$ with $\lvert\mathcal{I}(A_3)\rvert = 2^3 = 8$ ideals;
   so $q_{\rm norm}(A_2, \{a\})\,q_{\rm norm}(A_2 + x_{\{a\}}, \varnothing) = \frac{1}{4}\cdot\frac{1}{6} = \frac{1}{24} \ne \frac{1}{32} = \frac{1}{4}\cdot\frac{1}{8} = q_{\rm norm}(A_2, \varnothing)\,q_{\rm norm}(A_2 + y_\varnothing, \{a\})$.
2. **Global-Post Slack Dilemma (`PW6A` Theorem 5.4 vs. Theorem 8.1):** Setting $q(P_n, S) = a_n u(S)$ for $S \subsetneq P_n$ and routing all residual probability $1 - a_n \sum_{S \subsetneq P_n} u(S)$ into the full ideal $S = P_n$ restores exact diamond commutation on proper branches, provided $u(S)$ depends **strictly on the intrinsic poset $S$** and **not** on ambient stage size $n = \lvert P_n\rvert$. *(Indeed, inserting $1/n$ inside an exponential damping factor $u_{\rm buggy}(P_n, S) = \exp\bigl(-\lambda \sum_{u \in \operatorname{Max}(S)} \lvert J^-[u]\rvert / n\bigr)$ immediately violates diamond commutation on $A_2$ with $S = \{a\}, T = \varnothing$, giving $a_2 a_3 e^{-\lambda/2} \ne a_2 a_3 e^{-\lambda/3}$, failing on $2{,}066/3{,}644$ diamonds for $N \le 4$!)* Yet routing normalization slack into $S = P_n$ creates global posts whenever the full-ideal branch fires (`PW6A` Theorem 8.1).

### 6.1 Explicit Complete Specification of a Downward Local-Cone-Routed Candidate (`[UNPROVED CANDIDATE]`)
A natural exploratory proposal is to route damping slack **downward within each local cone $S$** to proper sub-ideals $R \subsetneq S$, rather than upward into the global post $S = P_n$. To evaluate this honestly as a candidate rather than assuming it works, we write down an **explicit, complete, positive, row-normalized growth rule** and test its diamond consistency directly.

**Definition 6.1 (`[UNPROVED CANDIDATE]` Downward Local-Cone-Routed Growth Rule).**  
Let $q_{\rm base}(P_n, S) = G(\lvert S\rvert, \lvert\operatorname{Max}(S)\rvert)/Z_n$ be an admitted subset-weight CSG kernel (which satisfies $\sum_{S \in \mathcal{I}(P_n)} q_{\rm base}(P_n, S) = 1$ and exact diamond commutation). Let $\eta : \mathcal{I}_{\rm fin} \to (0, 1]$ be an isomorphism-invariant retention factor on finite ideals with $\eta(\varnothing) = 1$ (for example, $\eta(S) = \exp\bigl(-\lambda \sum_{u \in \operatorname{Max}(S)} \lvert J^-[u]\rvert\bigr)$ for $S \ne \varnothing$, $\lambda > 0$), and for every nonempty ideal $S \ne \varnothing$ let $M_S(R) \ge 0$ ($R \subsetneq S$, $R \in \mathcal{I}(S)$) be an intrinsic probability distribution over the proper sub-ideals of $S$:
$$
\sum_{R \in \mathcal{I}(S) : R \subsetneq S} M_S(R) = 1 \qquad (\forall\, S \ne \varnothing).
$$
Define the **downward local-cone-routed transition kernel** $q_{\rm loc}(P_n, \cdot)$ on $\mathcal{I}(P_n)$ by:
$$
q_{\rm loc}(P_n, R) := \eta(R)\,q_{\rm base}(P_n, R) + \sum_{\substack{S \in \mathcal{I}(P_n) \\ R \subsetneq S}} \bigl(1 - \eta(S)\bigr)\,M_S(R)\,q_{\rm base}(P_n, S) \qquad \bigl(R \in \mathcal{I}(P_n)\bigr).
$$

**Lemma 6.2 (`[PROVED PROPOSITION]` Exact Positivity, Row Normalization, and Global-Post Suppression of $q_{\rm loc}$).**  
*For every finite poset $P_n$ ($\lvert P_n\rvert = n \ge 1$):*
1. $q_{\rm loc}(P_n, R) \ge 0$ *for every $R \in \mathcal{I}(P_n)$ (and strictly positive if $q_{\rm base} > 0, \eta > 0$);*
2. $\sum_{R \in \mathcal{I}(P_n)} q_{\rm loc}(P_n, R) = 1$ *identically, without dividing by any stage-dependent partition function;*
3. *For the full ideal $R = P_n$, no larger ideal $S \supsetneq P_n$ exists in $\mathcal{I}(P_n)$, so $q_{\rm loc}(P_n, P_n) = \eta(P_n)\,q_{\rm base}(P_n, P_n) \le q_{\rm base}(P_n, P_n)$: local routing strictly **suppresses** global posts rather than creating them.*

*Proof.* (1) and (3) are immediate from $0 < \eta(S) \le 1$, $M_S(R) \ge 0$, and maximality of $P_n$ in $\mathcal{I}(P_n)$. For (2), interchanging the order of summation and using $\eta(\varnothing) = 1$ gives:
$$
\sum_{R \in \mathcal{I}(P_n)} q_{\rm loc}(P_n, R) = \sum_{S \in \mathcal{I}(P_n)} \eta(S)\,q_{\rm base}(P_n, S) + \sum_{\substack{S \in \mathcal{I}(P_n) \\ S \ne \varnothing}} \bigl(1 - \eta(S)\bigr)\,q_{\rm base}(P_n, S) \underbrace{\sum_{R \in \mathcal{I}(S) : R \subsetneq S} M_S(R)}_{=\,1} = \sum_{S \in \mathcal{I}(P_n)} q_{\rm base}(P_n, S) = 1. \quad \blacksquare
$$

### 6.2 The Cone-Overlap Order-Dependence Obstruction (`[COUNTEREXAMPLE / OBSTRUCTION]`)
Despite satisfying exact row normalization and suppressing global posts, **generic choices of $(\eta, M_S)$ in Definition 6.1 STILL VIOLATE DIAMOND COMMUTATION (`CR-1a`)**!

**Proposition 6.3 (`[COUNTEREXAMPLE / OBSTRUCTION]` Asymmetric Upper-Cone Overlap Breaks Diamond Commutation in Naive Local Routing).**  
*In Definition 6.1, take uniform sub-ideal routing $M_S(R) = \frac{1}{\lvert\mathcal{I}(S)\rvert - 1}$ ($R \subsetneq S$) and $\eta(S) = \exp\bigl(-\lambda \sum_{u \in \operatorname{Max}(S)} \lvert J^-[u]\rvert\bigr)$ ($\lambda = 0.5$) over any positive subset-weight base $q_{\rm base}$. Although $\max_{P_n}\bigl\lvert\sum_R q_{\rm loc}(P_n, R) - 1\bigr\rvert \le 2.22 \times 10^{-16}$, $q_{\rm loc}$ violates diamond commutation $q_{\rm loc}(C, R_1)\,q_{\rm loc}(C + x_{R_1}, R_2) = q_{\rm loc}(C, R_2)\,q_{\rm loc}(C + y_{R_2}, R_1)$ on **$3{,}036$ out of $3{,}644$ diamonds** across $1 \le \lvert C\rvert \le 4$ (starting already at $\lvert C\rvert = 1$, $C = \{0\}$, $R_1 = \{0\}$, $R_2 = \varnothing$).*

*Structural Mechanism.* Along Route 1 ($C \xrightarrow{R_1} C + x_{R_1} \xrightarrow{R_2} \dots$), $q_{\rm loc}(C + x_{R_1}, R_2)$ receives downward-routed slack from ideals of the form $S' = U \cup \{x\} \in \mathcal{I}(C + x_{R_1})$ whenever $R_1 \cup R_2 \subseteq U \in \mathcal{I}(C)$—that is, from upper cones $U$ where the past cones of $x$ and the target ideal $R_2$ **overlap inside $U$**. Along Route 2 ($C \xrightarrow{R_2} C + y_{R_2} \xrightarrow{R_1} \dots$), $q_{\rm loc}(C + y_{R_2}, R_1)$ receives slack from $S'' = U \cup \{y\} \in \mathcal{I}(C + y_{R_2})$. Because $U \cup \{x\}$ (where $x$ covers $\operatorname{Max}(R_1)$) and $U \cup \{y\}$ (where $y$ covers $\operatorname{Max}(R_2)$) are non-isomorphic whenever $R_1 \ne R_2$, the cross-routed weights fail to commute unless $(\eta, M_S)$ satisfies non-trivial algebraic Möbius/incidence identities across all upper extensions!

### 6.3 Mandatory Consistency Proof Obligations for Any Local-Cone Compensation Candidate
Accordingly, local-cone compensation is strictly an **unproved candidate research direction**, not an established fix for `PW6A`. Any proposed local-cone feedback rule $q_{\rm cand}(P_n, \tilde{r}_n, S)$ must discharge all five of the following proof obligations before being admitted as a covariant DET growth law:
1. **Strict Branch Positivity:** $q_{\rm cand}(P_n, \tilde{r}_n, S) \ge 0$ on all ideals $S \in \mathcal{I}(P_n)$ at all horizons $n \ge 1$.
2. **Exact Row Normalization Without Post Saturation:** $\sum_{S \in \mathcal{I}(P_n)} q_{\rm cand}(P_n, \tilde{r}_n, S) = 1$ with $\rho_{\rm post}(P_N) \xrightarrow{\mathbb{P}} 0$.
3. **Exact Spacelike Diamond Commutation Under Cone Overlaps (`CR-1a`):** Proof of $q_{\rm cand}(C, R_1)\,q_{\rm cand}(C + x_{R_1}, R_2) = q_{\rm cand}(C, R_2)\,q_{\rm cand}(C + y_{R_2}, R_1)$ (or operator-valued CPTP commutation on marked payloads) across **all** overlapping upper cones $U \supseteq R_1 \cup R_2$.
4. **Kolmogorov Cylinder Projectivity:** Existence of a consistent projective measure $\mathbb{P}_\infty$ on $\Omega_\infty$ independent of arbitrary birth ordering of spacelike-separated events.
5. **Single-History `CR-1b–d` Concentration:** Analytical or large-$N$ proof that both global $R_2(P_N)$ and mesoscopic internal interval $\overline{R}_{\rm int}(P_N)$ concentrate at interior values with vanishing within- and between-history variances.

---

## 7. Candidate Unbounded CSG Families and First-Pass Multi-Horizon Experiments

Theorem 5.5 establishes that $\limsup_{n\to\infty} \mu_n/\ln n > 0$ is a universal necessary condition for any static subset-weight CSG law to satisfy `CR-1b` (since $\mu_n = o(\ln n) \implies R_2(P_N) \xrightarrow{\mathbb{P}} 0$), while Theorem 5.2 proves that within the independent-edge percolation subfamily ($t_k = (\frac{p}{1-p})^k$), linear seed scaling $\mu_n = p n$ drives upper comparability saturation $R_2(P_N) \xrightarrow{\mathbb{P}} 1$. Together, Theorem 5.5's necessary condition $\limsup_{n\to\infty} \mu_n/\ln n > 0$ and Theorem 5.2's percolation saturation motivate focusing on unbounded coupling sequences whose expected seed counts scale sub-linearly but at or above the logarithmic threshold $\Theta(\ln n)$ (without asserting an unproven general upper bound for all non-percolation static sequences). In `PW6A` §7.3, factorial/geometric-factorial couplings $t_k = c^k / k!$ ($\mu_n = \Theta(\sqrt{c n})$) exhibited steady upward comparability drift ($R_2(2000) \approx 0.88\text{–}0.93$). We therefore examine two faster-decaying unbounded candidate families—**Gevrey** and **Log-Quadratic**—deriving their exact parent-count scalings and testing them empirically across $N \in \{16, 32\}$ ($M = 50$ runs/model) and $N \in \{16, 32, 64, 128, 256, 512, 1024\}$ ($M = 25$ runs/model) in the quarantined verification suite ([verification/cr1_discriminating_experiment.py](verification/cr1_discriminating_experiment.py), orchestrated by [verification/run_cr1_verification.py](verification/run_cr1_verification.py)).

### 7.1 Exact Parent-Count Scaling of Gevrey and Log-Quadratic CSG (`[PROVED PROPOSITION]`)

**Proposition 7.1 (`[PROVED PROPOSITION]` Exact Seed-Count Scaling $\mathbb{E}_{\pi_n}[K_n]$ for Gevrey and Log-Quadratic Couplings).**  
*Let $w_n(k) := \binom{n}{k} t_k$ ($0 \le k \le n$) and $\pi_n(k) = w_n(k)/Z_n$, where $Z_n = \sum_{k=0}^n \binom{n}{k} t_k$.*
1. *(Super-Factorial / Gevrey CSG: $t_k = \frac{c^k}{(k!)^\beta}$ with $c > 0, \beta > 0$): Consecutive weights satisfy the exact ratio:*
   $$
   \frac{w_n(k + 1)}{w_n(k)} = \frac{c\,(n - k)}{(k + 1)^{\beta + 1}} \qquad (0 \le k \le n - 1),
   $$
   *which is strictly decreasing in $k$, giving unique mode and expectation scaling:*
   $$
   \mathbb{E}_{\pi_n}[K_n] = \Theta\!\left((c n)^{\frac{1}{\beta + 1}}\right) \gg \ln n \qquad (n \to \infty).
   $$
2. *(Log-Quadratic CSG: $t_k = c^k q^{\binom{k}{2}}$ with $c > 0, q \in (0, 1)$): Here $Z_n = \sum_{k=0}^n \binom{n}{k} c^k q^{\binom{k}{2}}$ uses the ordinary subset binomial $\binom{n}{k}$, and consecutive weights satisfy the exact ratio:*
   $$
   \frac{w_n(k + 1)}{w_n(k)} = \frac{n - k}{k + 1}\,c\,q^k \qquad (0 \le k \le n - 1),
   $$
   *which crosses $1$ at $k_*(n) = \frac{\ln(c n) - \ln\ln(c n) + O(1)}{\ln(1/q)}$ and yields critical logarithmic seed scaling:*
   $$
   \mathbb{E}_{\pi_n}[K_n] = \frac{\ln(c n)}{\ln(1/q)} - O(\ln\ln n) = \Theta(\ln n) \qquad (n \to \infty).
   $$

*Proof.*  
1. Direct division gives $\frac{w_n(k+1)}{w_n(k)} = \frac{n - k}{k + 1}\cdot\frac{c}{(k + 1)^\beta} = \frac{c(n - k)}{(k + 1)^{\beta + 1}}$, which strictly decreases with $k$. Set $a_n := (c n)^{\frac{1}{\beta + 1}}$. For large $n$ and $k + 1 \le \frac{1}{2} a_n$ (so $n - k > n/2$), $\frac{w_n(k+1)}{w_n(k)} > \frac{c n / 2}{2^{-(\beta+1)} c n} = 2^\beta > 1$, so the total weight on $k \le \frac{1}{4} a_n$ is exponentially smaller than $w_n(\lfloor \frac{1}{2} a_n\rfloor)$. Conversely, for $k + 1 \ge 2 a_n$, $\frac{w_n(k+1)}{w_n(k)} < \frac{c n}{2^{\beta + 1} c n} = 2^{-(\beta + 1)} \le \frac{1}{2}$, so geometric tail domination gives $\mathbb{E}_{\pi_n}[K_n] = \Theta(a_n) = \Theta\bigl((c n)^{\frac{1}{\beta + 1}}\bigr)$.
2. Similarly, $\frac{w_n(k+1)}{w_n(k)} = \frac{n - k}{k + 1} c q^k$ strictly decreases with $k$. Put $\Lambda_n := \frac{\ln(c n)}{\ln(1/q)}$. For $k \le k_- := \bigl\lfloor\Lambda_n - \frac{2\ln\Lambda_n}{\ln(1/q)}\bigr\rfloor$ and large $n$, $c q^k \ge \frac{\Lambda_n^2}{n}$, so $\frac{w_n(k+1)}{w_n(k)} \ge \frac{n - \Lambda_n}{\Lambda_n + 1}\cdot\frac{\Lambda_n^2}{n} > 2$ for large $n$; hence $\pi_n(k < k_- - r) \le 2^{-r}$. For $k \ge k_+ := \lceil\Lambda_n\rceil + 1$, $c q^k \le \frac{q}{n}$, so $\frac{w_n(k+1)}{w_n(k)} < \frac{q}{k + 1} < q < 1$, giving geometric tail decay $\pi_n(k > k_+ + r) \le q^r$. Sandwiching between $k_-$ and $k_+$ proves $\mathbb{E}_{\pi_n}[K_n] = \frac{\ln(c n)}{\ln(1/q)} - O(\ln\ln n)$. $\blacksquare$

*(Exact Finite-Diamond Verification):* Exhaustive enumeration over all naturally labeled posets of size $1 \le n \le 4$ (`poset_generator.py`, $3{,}644$ diamonds) confirms $0/3{,}644$ diamond violations for both Gevrey and Log-Quadratic CSG (`CR-1a` holds identically).

### 7.2 First-Pass Benchmark Across Positive Controls, Negative Controls, and Candidates ($N = 16, 32$)
Following our experimental sequence, we first verify non-vacuity of `CR-1b–d` on positive continuum controls (`minkowski_2d`, `minkowski_4d`, and `minkowski_2d_slab`), then verify rejection of negative controls (`bimodal_mix_10_90`, `kr_3layer`, `cutoff_kmax1`, `percolation`, `random_dag`), and finally evaluate Gevrey and Log-Quadratic CSG ($M = 50$ independent histories per model at $N \in \{16, 32\}$; full output in [verification/cr1_experiment_results.json](verification/cr1_experiment_results.json)):

#### Quantitative Results at Horizon $N = 32$ ($M = 50$ Independent Histories per Model)

| Model Configuration | Family | $\langle R_2 \rangle$ | $\widehat{\operatorname{Var}}_{\rm betw}(R_2)$ | $\langle \rho_2 \rangle$ | $\langle R_2(I) \rangle$ ($m \ge 4$) | $\langle\operatorname{Var}_{\rm within}(R_2(I))\rangle$ | `CR-1d` Int? | `SS-1` Match? |
|---|---|---|---|---|---|---|:---:|:---:|
| 2D Minkowski Diamond ($f(2)=0.50$) | `geometric_control` | $0.4973 \pm 0.0607$ | $0.003679$ | $1.685$ | $0.4932$ | $0.026720$ | YES | YES |
| 2D Minkowski Slab $[0,1]\times[0,3]$ | `geometric_control` | $0.2015 \pm 0.0244$ | $0.000596$ | $0.384$ | $0.4630$ | $0.026492$ | YES | NO |
| 4D Minkowski Diamond ($f(4)=0.10$) | `geometric_control` | $0.0956 \pm 0.0303$ | $0.000917$ | $0.031$ | $0.0659$ | $0.004611$ | YES | YES |
| Bimodal 10/90 Chain–Antichain Mix | `non_geometric_control` | $0.0400 \pm 0.1979$ | $0.039184$ | $0.290$ | $1.0000$ | $0.000000$ | NO | NO |
| 3-Layer Kleitman–Rothschild Poset | `non_geometric_control` | $0.3887 \pm 0.0179$ | $0.000322$ | $0.000$ | $0.0000$ | $0.000000$ | NO | NO |
| Finite-Cutoff CSG ($k_{\rm max}=1$) | `non_geometric_control` | $0.1371 \pm 0.0319$ | $0.001020$ | $0.557$ | $1.0000$ | $0.000000$ | NO | NO |
| Bernoulli Percolation ($p=0.08$) | `non_geometric_control` | $0.1661 \pm 0.0575$ | $0.003302$ | $0.521$ | $0.6403$ | $0.026704$ | YES | NO |
| Bernoulli Percolation ($p=0.15$) | `non_geometric_control` | $0.4094 \pm 0.0767$ | $0.005890$ | $1.271$ | $0.6231$ | $0.035163$ | YES | YES |
| Sparse Random DAG ($c_{\rm deg}=2.0$) | `non_geometric_control` | $0.1141 \pm 0.0407$ | $0.001659$ | $0.359$ | $0.6459$ | $0.011444$ | YES | NO |
| Dense Random DAG ($p=0.05$) | `non_geometric_control` | $0.0813 \pm 0.0300$ | $0.000902$ | $0.262$ | $0.7484$ | $0.032732$ | NO | NO |
| Gevrey CSG ($c=0.20, \beta=1.5$) | `candidate_gevrey` | $0.1607 \pm 0.0405$ | $0.001644$ | $0.540$ | $0.6948$ | $0.032322$ | NO | NO |
| Gevrey CSG ($c=0.20, \beta=2.0$) | `candidate_gevrey` | $0.1410 \pm 0.0379$ | $0.001439$ | $0.533$ | $0.7874$ | $0.022705$ | NO | NO |
| Log-Quadratic CSG ($c=0.20, q=0.10$) | `candidate_log_quadratic` | $0.1037 \pm 0.0274$ | $0.000752$ | $0.424$ | $0.9014$ | $0.008483$ | NO | NO |
| Log-Quadratic CSG ($c=0.20, q=0.20$) | `candidate_log_quadratic` | $0.1219 \pm 0.0322$ | $0.001036$ | $0.467$ | $0.8068$ | $0.023219$ | NO | NO |

### 7.3 Extended Multi-Horizon Scaling & Cone-Overlap Analysis ($N = 16 \dots 1024$) (`[NUMERICAL EVIDENCE]`)
Small-horizon windows ($N \le 32$) can mask slow power-law or logarithmic drift (just as $N \le 140$ masked $k_{\rm max} = 3$ decay in `PW6A`). We therefore track single-history scaling, parent-seed size $\langle K_n\rangle$ vs. realized link in-degree $\langle \lvert\operatorname{Max}(S_n)\rvert\rangle$, between-history variance, and mesoscopic bulk intervals $m \in \bigl[\max(4, \lfloor\frac{1}{2}\sqrt{N}\rfloor), \max(12, \lfloor\frac{5}{2}\sqrt{N}\rfloor)\bigr]$ ($v \ge N/4$) across $N \in \{16, 32, 64, 128, 256, 512, 1024\}$ ($M = 25$ independent runs/model):

| Model Configuration | $R_2(32)$ | $R_2(128)$ | $R_2(512)$ | $R_2(1024)$ | $\widehat{\operatorname{Var}}_{\rm betw}(1024)$ | $\langle K_n \rangle_{1024}$ | $\langle \lvert\operatorname{Max}(S_n)\rvert \rangle_{1024}$ | Mesoscopic $\langle R_2(I) \rangle$ ($32 / 128 / 512 / 1024$) |
|---|---|---|---|---|---|---|---|---|
| Gevrey ($0.20, \beta=1.5$) | $0.1554$ | $0.2102$ | $0.3447$ | $0.4226$ | $0.000097$ | $7.62$ | $4.20$ | $0.688 / 0.620 / 0.408 / 0.325$ |
| Gevrey ($0.20, \beta=2.0$) | $0.1340$ | $0.1466$ | $0.2146$ | $0.2691$ | $0.000105$ | $5.30$ | $3.82$ | $0.738 / 0.691 / 0.419 / 0.342$ |
| Gevrey ($0.20, \beta=3.0$) | $0.1093$ | $0.0866$ | $0.0945$ | $0.1087$ | $0.000055$ | $3.26$ | $2.94$ | $0.811 / 0.767 / 0.487 / 0.380$ |
| Log-Quad ($0.20, q=0.10$) | $0.1043$ | $0.0720$ | $0.0590$ | $0.0563$ | $0.000025$ | $2.30$ | $2.22$ | $0.963 / 0.807 / 0.534 / 0.436$ |
| Log-Quad ($0.20, q=0.20$) | $0.1140$ | $0.1011$ | $0.1047$ | $0.1086$ | $0.000064$ | $2.95$ | $2.69$ | $0.799 / 0.720 / 0.488 / 0.396$ |
| Log-Quad ($1.00, q=0.50$) | $0.5191$ | $0.4914$ | $0.4894$ | $0.4873$ | $0.000170$ | $7.33$ | $3.90$ | $0.671 / 0.578 / 0.419 / 0.333$ |
| Cutoff ($c=1.0, k_{\rm max}=1$) | $0.1390$ | $0.0524$ | $0.0182$ | $0.0105$ | $0.000001$ | $1.00$ | $1.00$ | $1.000 / 1.000 / 1.000 / \text{n/a}$ |
| Cutoff ($c=1.0, k_{\rm max}=2$) | $0.3725$ | $0.2118$ | $0.1133$ | $0.0819$ | $0.000038$ | $2.00$ | $1.91$ | $0.733 / 0.668 / 0.512 / 0.443$ |
| Percolation ($p=0.08$) | $0.1758$ | $0.5400$ | $0.8651$ | $0.9299$ | $0.000004$ | $71.44$ | $3.26$ | $0.636 / 0.527 / 0.434 / 0.443$ |
| 4D Minkowski Diamond | $0.0925$ | $0.0943$ | $0.0995$ | — | $0.000110^*$ | — | — | $0.050 / 0.106 / 0.096 / \text{—}$ |
| 2D Minkowski Slab $[0,1]\times[0,3]$ | $0.2106$ | $0.2030$ | $0.2027$ | — | $0.000030^*$ | — | — | $0.565 / 0.499 / 0.509 / \text{—}$ |

*(Asterisk $*$ denotes $N = 512$ value for continuum Poisson controls; global post density satisfies $\rho_{\rm post} = 0.0000$ across all Gevrey and Log-Quadratic $(0.20, q)$ runs at $N = 256$.)*

Four substantive findings emerge from the multi-horizon data:
1. **Positive Controls Confirm Proposition 3.1 Quantitatively:** In 4D Minkowski diamonds, both global and mesoscopic interval comparability concentrate around $f(4) = 0.1000$ ($0.0995$ and $0.0957$ at $N = 512$, satisfying `CR-1b–d` + `SS-1`). In the 2D Minkowski wide slab $[0, 1] \times [0, 3]$, global comparability converges sharply to $\frac{11}{54} = 0.2037$ ($0.2027 \pm 0.0055$ at $N = 512$, $\widehat{\operatorname{Var}}_{\rm betw} = 3.0 \times 10^{-5}$), while mesoscopic internal intervals converge to $f(2) = 0.5000$ ($0.5087$ at $N = 512$, $\langle\operatorname{Var}_{\rm within}\rangle = 0.0071$, satisfying `CR-1b–d` while violating `SS-1`).
2. **Gevrey CSG Turns Upward Beyond $N \approx 64\text{–}128$:** Although Gevrey ($\beta = 2.0$) decreases slightly from $N = 16$ ($0.144$) to $N = 32$ ($0.134$), its polynomial seed growth $\mathbb{E}_{\pi_n}[K_n] = \Theta(n^{1/(\beta+1)})$ drives monotonic upward drift at larger horizons ($0.147$ at $N = 128 \to 0.215$ at $N = 512 \to 0.269$ at $N = 1024$; even $\beta = 3.0$ dips to $0.087$ at $N = 128$ before turning upward to $0.109$ at $N = 1024$). Thus small-$N$ stability of Gevrey must **not** be claimed as asymptotic stabilization.
3. **Log-Quadratic CSG Holds a Critical Logarithmic Global Window With Strong Cone Compression:** Because $\mathbb{E}_{\pi_n}[K_n] = \Theta(\ln n)$ sits directly on the critical boundary of Theorem 5.5, Log-Quadratic $(c, q) = (0.20, 0.20)$ maintains single-history global comparability inside $[0.101, 0.114]$ across $N = 32 \dots 1024$ with $\widehat{\operatorname{Var}}_{\rm betw}(R_2) = 6.39 \times 10^{-5}$ at $N = 1024$ and $\rho_{\rm post} = 0$, while $(c, q) = (1.00, 0.50)$ ($t_k = 2^{-\binom{k}{2}}$) maintains $R_2(P_N) \in [0.487, 0.491]$ across $N = 128 \dots 1024$ as causal-cone overlaps compress seed size $\langle K_n\rangle = 7.33$ down to realized link in-degree $\langle\lvert\operatorname{Max}(S_n)\rvert\rangle = 3.90$.
4. **Mesoscopic Sub-Interval Spine Excess vs. Homogeneous 4D Diamonds:** Even at $(c, q) = (0.20, 0.20)$ where global $R_2(P_{1024}) = 0.1086$ matches $f(4) = 0.1000$, nested intervals are substantially denser along sequential causal spines than in homogeneous 4D Minkowski space: $\langle R_2(I)\rangle = 0.807$ ($N = 32, m \ge 4$), relaxing on larger mesoscopic intervals $m \in [16, 80]$ at $N = 1024$ to $0.3957$ ($\langle\operatorname{Var}_{\rm within}\rangle = 0.0110$)—still **$4.1\times$ higher** than 4D Minkowski mesoscopic intervals ($0.0957$, $d_{\rm MM}^{\rm int} \approx 2.3$ vs. $4.0$). Across the multi-exponent mesoscopic scan $\alpha \in \{0.25, 0.35, 0.45, 0.50, 0.65\}$ in §7.4, internal interval comparability exhibits coherent scale-dependent relaxation ($R_{\rm int}: 0.9406 \to 0.2647$ at $N = 1024$), violating homogeneous 4D `SS-1` at finite horizons ($R_{\rm int}(\alpha) \approx 0.100$), while tracking a tight function $\Phi(m)$ of absolute interval cardinality $m = \lvert I(u, v)\rvert$.

### 7.4 Scale-Dependent Nested-Regime Profile $R_{\rm int}(\alpha)$ of Log-Quadratic CSG (`[NUMERICAL EVIDENCE]`)

To test whether internal causal geometry stabilizes homogeneously, fragments noisily, or follows a coherent scale-dependent law, we evaluate $\overline{R}_{\rm int}(P_N; \alpha)$ across five mesoscopic interval scaling exponents $\alpha \in \{0.25, 0.35, 0.45, 0.50, 0.65\}$ at horizons $N = 512$ and $N = 1024$ ($M = 20$ independent realizations per model, seed `20261116`; `run_multi_alpha_profile_experiment()` in [verification/cr1_discriminating_experiment.py](verification/cr1_discriminating_experiment.py)), using the exact `CR-1c` bulk family:
$$
\mathcal{J}_N(\omega; \alpha) := \left\{(u, v) \in P_N(\omega)^2 : u \prec v,\; \lvert J^-(u)\rvert \ge \delta_{\rm bulk}\overline{J}_N,\; \lvert J^+(v)\rvert \ge \delta_{\rm bulk}\overline{J}_N,\; c_- N^\alpha \le \lvert I(u, v)\rvert \le c_+ N^\alpha\right\},
$$
with boundary-trimming fraction $\delta_{\rm bulk} = 0.05$ and window constants $c_- = 0.5, c_+ = 1.5$. *(Note on finite-$N$ bulk ceiling: in $D_4$ with $\delta_{\rm bulk} = 0.05$, bulk-trimmed endpoints satisfy $t_u, 1 - t_v \gtrsim (\frac{1}{2}\delta_{\rm bulk} f(4))^{1/4} \approx 0.224$, capping bulk diamond volume at $(1 - 2\cdot 0.224)^4 N \approx 0.094 N \approx 96$ points at $N = 1024$; exponents $\alpha \in [0.25, 0.65]$ keep $c_- N^\alpha \le 46$ well inside the populated bulk regime.)* In continuum $d$-dimensional Minkowski diamonds, Alexandrov intervals are Lorentz-congruent diamonds at all scales, yielding scale-invariant internal comparability $R_{\rm int}^*(\alpha) \equiv f(d)$ for all $\alpha \in (0, 1)$ (`SS-1`):

#### Scale-Dependent Internal Comparability Profile $R_{\rm int}(\alpha)$ at Horizon $N = 1024$ ($M = 20$ Runs)
| Model Configuration | Global $R_2$ | $\alpha = 0.25$ ($m \in [3, 8]$) | $\alpha = 0.35$ ($m \in [6, 16]$) | $\alpha = 0.45$ ($m \in [12, 33]$) | $\alpha = 0.50$ ($m \in [16, 48]$) | $\alpha = 0.65$ ($m \in [46, 135]$) | Homogeneous `SS-1`? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **4D Minkowski Diamond** ($f(4)=0.100$) | $0.0995 \pm 0.0059$ | $0.0960 \pm 0.0220$ | $0.0992 \pm 0.0114$ | $0.1000 \pm 0.0115$ | $0.0989 \pm 0.0098$ | $0.1040 \pm 0.0236$ | **YES** |
| Effective $d_{\rm MM}$ (4D Diamond) | $4.01 \pm 0.07$ | $4.08 \pm 0.27$ | $4.02 \pm 0.14$ | $4.01 \pm 0.14$ | $4.02 \pm 0.12$ | $3.98 \pm 0.25$ | **4D Flat** |
| **Log-Quad CSG** ($(c, q) = (0.20, 0.20)$) | $0.1095 \pm 0.0099$ | $0.9406 \pm 0.0159$ | $0.7511 \pm 0.0346$ | $0.5064 \pm 0.0430$ | $0.4264 \pm 0.0324$ | $0.2647 \pm 0.0228$ | **NO** |
| Effective $d_{\rm MM}$ (Log-Quad CSG) | $3.90 \pm 0.10$ | $1.10 \pm 0.03$ | $1.44 \pm 0.07$ | $1.99 \pm 0.11$ | $2.21 \pm 0.10$ | $2.82 \pm 0.11$ | **Scale-Dependent** |

#### Scale-Dependent Internal Comparability Profile $R_{\rm int}(\alpha)$ at Horizon $N = 512$ ($M = 20$ Runs)
| Model Configuration | Global $R_2$ | $\alpha = 0.25$ ($m \in [3, 7]$) | $\alpha = 0.35$ ($m \in [5, 13]$) | $\alpha = 0.45$ ($m \in [9, 24]$) | $\alpha = 0.50$ ($m \in [12, 33]$) | $\alpha = 0.65$ ($m \in [29, 86]$) | Homogeneous `SS-1`? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **4D Minkowski Diamond** ($f(4)=0.100$) | $0.1001 \pm 0.0088$ | $0.0946 \pm 0.0335$ | $0.0856 \pm 0.0299$ | $0.0915 \pm 0.0268$ | $0.0964 \pm 0.0383$ | $0.0985 \pm 0.0417$ | **YES** |
| Effective $d_{\rm MM}$ (4D Diamond) | $4.00 \pm 0.10$ | $4.13 \pm 0.40$ | $4.16 \pm 0.32$ | $4.16 \pm 0.38$ | $4.13 \pm 0.47$ | $4.10 \pm 0.48$ | **4D Flat** |
| **Log-Quad CSG** ($(c, q) = (0.20, 0.20)$) | $0.1079 \pm 0.0097$ | $0.9316 \pm 0.0254$ | $0.8042 \pm 0.0524$ | $0.5955 \pm 0.0626$ | $0.5025 \pm 0.0491$ | $0.3016 \pm 0.0381$ | **NO** |
| Effective $d_{\rm MM}$ (Log-Quad CSG) | $3.91 \pm 0.11$ | $1.11 \pm 0.04$ | $1.34 \pm 0.10$ | $1.77 \pm 0.15$ | $2.00 \pm 0.13$ | $2.66 \pm 0.16$ | **Scale-Dependent** |

Three structural conclusions follow from this multi-scale profile:
1. **Violation of Homogeneous 4D Scale Self-Similarity (`SS-1`) at Finite Horizons:** While 4D Minkowski diamond point processes remain flat across all tested exponents ($R_{\rm int}(\alpha) \in [0.096, 0.104]$ at $N = 1024$, $d_{\rm MM} \in [3.98, 4.08]$), Log-Quadratic CSG ($(c, q) = (0.20, 0.20)$) departs strongly from homogeneous `SS-1`. At ultraviolet interval scales ($\alpha = 0.25, m \in [3, 8]$), internal comparability reaches $0.9406 \pm 0.0159$ ($d_{\rm MM} = 1.10 \pm 0.03$, **$9.8\times$ denser** than 4D diamonds), relaxing across intermediate scales ($\alpha = 0.50, m \in [16, 48]$: $0.4264 \pm 0.0324$, $d_{\rm MM} = 2.21 \pm 0.10$) down to $0.2647 \pm 0.0228$ ($d_{\rm MM} = 2.82 \pm 0.11$) at $\alpha = 0.65$ ($m \in [46, 135]$).
2. **Sequential Causal Spine Mechanism:** Because the expected parent seed count grows only logarithmically ($\mathbb{E}_{\pi_n}[K_n] \approx \frac{\ln(c n)}{\ln(1/q)} \approx 2.5\text{–}3.0$), small intervals $I(u, v)$ are dominated by narrow ancestral spines ($d_{\rm MM} \approx 1.1$), whereas larger bulk intervals ($m \gtrsim 50$) sample multiple transversely branching chains, progressively lowering internal comparability and shrinking within-history interval variance ($\langle\operatorname{Var}_{\rm within}\rangle: 0.0453$ at $\alpha = 0.35 \to 0.0114$ at $\alpha = 0.50 \to 0.0012$ at $\alpha = 0.65$).
3. **Coherent Cardinality Collapse $\Phi(m)$ vs. Homogeneous 4D Rejection:** Crucially, mismatching a homogeneous 4D diamond benchmark does **not** automatically rule out a **coherent scale-dependent nested regime**. Comparing $N = 512 = 2^9$ at $\alpha = 0.50$ and $N = 1024 = 2^{10}$ at $\alpha = 0.45$—which select the **identical** absolute interval-cardinality window $m \in [12, 33]$ ($512^{0.50} = 1024^{0.45} = 2^{4.5} \approx 22.6$)—yields virtually indistinguishable internal comparability: $0.5025 \pm 0.0491$ ($d_{\rm MM} = 2.00 \pm 0.13$) at $N = 512$ vs. $0.5064 \pm 0.0430$ ($d_{\rm MM} = 1.99 \pm 0.11$) at $N = 1024$, with low between-history variance ($\widehat{\operatorname{Var}}_{\rm betw} = 0.0018\text{–}0.0024$; and $\widehat{\operatorname{Var}}_{\rm betw} = 0.00052$ at $N = 1024, \alpha = 0.65$). Thus, rather than fluctuating erratically between histories, internal comparability in Log-Quadratic CSG concentrates along a deterministic-looking crossover curve $\Phi(m)$ of **absolute interval cardinality $m = \lvert I(u, v)\rvert$** (dimensional reduction $d_{\rm MM} \to 1$ at small $m$, flowing toward higher $d_{\rm MM}$ as $m$ grows). Whether $\lim_{m \to \infty} \Phi(m)$ converges as $N^\alpha \to \infty$ to a scale-separated interior limit $R_{\rm int}^* \in (R_{\rm global}^*, 1)$ (satisfying `CR-1a–d` without `SS-1`), relaxes asymptotically to $R_{\rm global}^*$ at ultra-large $m \gg 10^2$, or continues drifting slowly remains an open analytical question.

---

## 8. Strictly Narrowed Conclusions and Open Mathematical Problems

To maintain rigorous claim hygiene, we bound every conclusion strictly to its proved or tested scope:

1. **What Is Proved Analytically (`[PROVED]`):**
   - The observable and nested-interval conditions `CR-1b–d` are **non-vacuous** on continuum Minkowski diamond sprinklings and are **strictly weaker than `SS-1`** ($R_{\rm int}^* = R_{\rm global}^*$), as proved on the 2D wide-slab cylinder $[0, 1] \times [0, 3]$ ($R_{\rm global}^* = \frac{11}{54} \ne \frac{1}{2} = R_{\rm int}^*$; Proposition 3.1).
   - The `QR-LD036` linear-extension deletion kernel $K_N$ satisfies $\mu_N K_N = \mu_{N-1}$ for all positive subset-weight laws (Theorem 4.1) and is strictly a mathematical prefix-projection readout, not a physical nested-regime map (§4.2).
   - Within the static subset-weight CSG family, `CR-1` rigorously rules out: (i) non-diamond finite perturbations (`QR-LD037`, Proposition 5.1); (ii) fixed-$p$ percolation $t_k = (\frac{p}{1-p})^k$ via $R_2(P_N) \xrightarrow{\mathbb{P}} 1$ (Theorem 5.2); (iii) finite-cutoff laws for both $k_{\rm max} = 1$ ($O(\frac{\ln N}{N}) \to 0$ and $R_2(I) \equiv 1$) and fixed $k_{\rm max} \ge 2$ ($O(N^{-1/k_{\rm max}}) \to 0$) (Theorem 5.4); and (iv) **all** sub-logarithmic parent-count subset-weight laws with $\mathbb{E}_{\pi_n}[K_n] = o(\ln n)$, making $\limsup_{n\to\infty}\mathbb{E}_{\pi_n}[K_n]/\ln n > 0$ a universal necessary condition within that family (Theorem 5.5). Single-history concentration (`CR-1b`) also rules out heterogeneous static mixtures with $\operatorname{Var}_\mu(r(\Theta)) > 0$ (Proposition 5.3), without ruling out degenerate or level-set mixtures.

2. **What Is NOT Proved (Explicit Non-Claims & Open Frontiers):**
   - **Joint Sequential Existence (`CR-1a–d`) Remains Open:** Because continuum Poisson/binomial sprinklings are static point-process ensembles rather than discrete order-ideal transition kernels (`CR-1a`), Proposition 3.1 proves non-vacuity of `CR-1b–d` only; constructing or proving the existence of a complete discrete sequential Markovian growth law satisfying all four conditions `CR-1a–d` simultaneously remains an open problem.
   - **No Universal Static Subset-Weight No-Go Is Claimed:** Testing Gevrey and Log-Quadratic CSG up to $N = 1024$ does **not** prove that every static subset-weight CSG law fails `CR-1` (or even `CR-1` + `SS-1`). In particular, determining analytically whether Log-Quadratic CSG $t_k = c^k q^{\binom{k}{2}}$ ($0 < q < 1$) possesses a rigorous interior limit $\lim_{N\to\infty} R_2(P_N) = R_{\rm global}^*(c, q) \in (0, 1)$ and $\lim_{N\to\infty} \overline{R}_{\rm int}(P_N) = R_{\rm int}^*(c, q) \in (0, 1)$—and whether $R_{\rm int}^*(c, q) > R_{\rm global}^*(c, q)$ persists asymptotically—remains an open mathematical problem.
   - **No Uniqueness of Nested Feedback Is Claimed:** Even if a future theorem proved that *every* static scalar subset-weight CSG law fails `CR-1` + `SS-1`, that result would exclude **only that defined scalar subset-weight family under those conditions**. It would **not** imply that nested or local-cone feedback is the unique remaining route: non-subset-weight static covariant kernels, higher-rank algebraic/quantum payload laws (`PW5-A` / `PW6-B`), or non-sequential covariant measures remain logically distinct alternatives.
   - **Local-Cone Compensation Remains an Unproved Candidate:** As demonstrated by Proposition 6.3 ($3{,}036/3{,}644$ cone-overlap diamond violations under uniform downward sub-ideal routing), routing normalization slack through local cones does not automatically preserve order independence; any viable local-cone growth rule must satisfy all five consistency proof obligations of §6.3.
