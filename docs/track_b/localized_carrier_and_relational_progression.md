# DET v8.0 Track B — Stages 9–11: Localized Present-State Carrier Propagation, Persistent All-Horizon Local Coupling, and Coordinate-Free Relational Progression on $X = (C, \{\mathcal{Z}_v\})$

**Document ID**: `localized_carrier_and_relational_progression.md`  
**Stages**: Stages 9, 10, and 11 (Track B Localized Carrier Foundations, Persistent Intra-Cone Coupling Engine, and Coordinate-Free Relational Comparison Benchmark)  
**Date**: 2026-11-16  
**Verification Suite**:
- `docs/track_b/verification/stage9_localized_carrier_experiment.py` (Gate 9 benchmark; deterministic audit output in `docs/track_b/verification/stage9_carrier_experiment_results.json`)
- `docs/track_b/verification/stage10_persistent_coupling_experiment.py` (Gate 10 benchmark; deterministic audit output in `docs/track_b/verification/stage10_coupling_experiment_results.json`)
- `docs/track_b/verification/stage11_relational_comparison_experiment.py` (Gate 11 benchmark; deterministic audit output in `docs/track_b/verification/stage11_comparison_experiment_results.json`)
- Master Runner & Regression Suite: `docs/track_b/verification/run_stage9_11_verification.py` (`79/79` unit tests PASS: `test_stage9_verification.py` `25/25`, `test_stage10_verification.py` `29/29`, `test_stage11_verification.py` `25/25`; composite artifact `docs/track_b/verification/stage9_11_experiment_results.json`)  
**Epistemic Scope**: Conditional mathematical theorems, exhaustive finite-poset diamond commutation and post-excitation taxonomy audits, exact analytical-to-sampler Markov kernel alignment across arbitrary horizons, synchronized Common Random Number (CRN) paired trajectory simulations, and coordinate-free relational attenuation and clock-exchange benchmarks on $X = (C, \{\mathcal{Z}_v\}_{v \in V(C)})$. Does not claim a derivation of continuum General Relativity, inverse-square metric falloff, physical spacetime dimension, or Status-M metaphysical propositions. Status M remains strictly quarantined.

---

## 1. Executive Summary, Epistemic Architecture, and Decision Block

### 1.1 Context and Technical Problem Statement
Track B Stage 8 (`docs/track_b/nested_regime_dynamics_and_source_response.md`) established two foundational results on $X = (C, \mathcal{Z})$: first, retiring standalone static scalar Log-Quadratic Classical Sequential Growth (CSG) as a stationary fixed-size geometry due to monotonic logarithmic drift; second, demonstrating that active coupling between committed causal structure $C$ and live residual state $\mathcal{Z}$ generates statistically decisive downstream shifts in chain length, cone volume, and coarse interval comparability. However, Stage 8 retained three explicit limitations identified in external review:
1. **Global Residual Carrier and Extrinsic Triggering:** Stage 8 represented $\mathcal{Z}$ as a single shared residual register or switched modes at a global birth index $n_0$, producing a spatially homogeneous regime shift rather than a localized source influencing its causal surroundings relative to a distant comparison region.
2. **Horizon-Shrinking Finite Cutoff ($\theta = O(t^{N_{\rm act}})$):** Stage 8's exact diamond-commuting root-martingale construction $\mathcal{M}_{\rm root}$ required a finite active horizon $N_{\rm act}$, causing allowed coupling amplitude to shrink exponentially as $N_{\rm act}$ increased.
3. **Need for Coordinate-Free Relational Comparison:** Because the discrete growth model does not yet possess a derived continuum metric or justified spatial distance $r$, imposing an inverse-square law by hand is methodologically invalid. Source-versus-surroundings tests must instead be formulated purely through poset-intrinsic order invariants.

To address these three requirements without overclaiming continuum geometry, this package executes a gated three-stage progression (Stages 9–11):
- **Stage 9 (Gate 9):** Replaces the monolithic carrier with a localized vertex-frontier state bundle $X = (C, \{\mathcal{Z}_v\}_{v \in V(C)})$, $\mathcal{Z}_v \in \mathcal{D}(\mathbb{C}^2)$, propagating strictly along incoming Hasse covering links $\operatorname{Max}(S) \to x_S$, paired with an event-anchored source excitation operator $\mathcal{U}_{\rm src}^{(u_*)}$ and cone-internal ideal probability redistribution. Beyond verifying baseline Growth–Growth (`73,786` pairs) and Source–Birth interleaving (`86,628` pairs) commutation, Stage 9 establishes the complete **post-excitation Growth–Growth diamond taxonomy** (`14,276` quadruples on $N \le 4$), proving that **Cone-Closure Redistribution** on $S_{\rm cone}(C; u_*) = J^-_C[J^+_C[u_*]]$ eliminates $100\%$ of mixed cone–spacelike post-excitation violations (`0 / 6,388` vs. `6,388 / 6,388` under naive stage-renormalized $Z_{\rm cone}$) while isolating the inner cone–cone overlap frontier (`1,988 / 3,944`).
- **Stage 10 (Gate 10):** Eliminates the terminal cutoff $N_{\rm act}$ via an exact **Intra-Cone Focused Seed Markov Kernel** coupled to the unmodified Stage 9 propagation channel $\Phi_{\rm prop}$. Both the closed-form ideal transition engine (`PersistentLocalTransitionEngine`) and the rejection-free $O(k_{\rm cap})$ Vandermonde conditional sampler (`simulate_persistent_trajectory`) implement the **exact same Markov transition law**, collapsing with zero Total Variation Distance ($\operatorname{TVD} = 0.0$) to unconditional Rideout–Sorkin CSG $(c_0, q_0)$ when uncoupled, while sustaining monotonically increasing near-source structural contrast $\Delta\rho_{\rm link} \in [0.7813, 1.1045] \ge \delta_* = 0.20$ and zero global posts ($\rho_{\rm post} \equiv 0.0$) across $N \in \{256, 512, 1024, 2048\}$.
- **Stage 11 (Gate 11):** Evaluates a coordinate-free three-tier comparison protocol contrasting $J^+[u_{\rm src}]$ against a mature spacelike comparison anchor $u_{\rm far} \notin J^+[u_{\rm src}] \cup J^-[u_{\rm src}]$: Tier 1 verifies exact zero spacelike perturbation ($\Delta L_{\max} = 0$, $\Delta\rho_{\rm link} = 0.0$, $p_1 = 0.0$); Tier 2 verifies monotone carrier decay across covering-link depth $d_{\rm link} \in \{1, \dots, 8\}$ and non-tautological monotone growth of Hasse covering in-degree shift $\Delta k_{\rm Hasse}$ across Alexandrov causal overlap $\eta_{\rm ov}$; and Tier 3 executes a bidirectional two-worldline clock-exchange protocol on peripheral low-overlap chains ($\eta_{\rm ov} \le 0.30$), achieving non-zero relays on both $X \to Y$ and $Y \to X$, exact abstention conservation $N_{\rm relay} + N_{\rm abst} = N_{\rm sent}$, and measured clock-ratio contrast $\Delta\mathcal{R} \in [+1.2763, +2.4757]$.

### 1.2 Gated Milestone Progression and Authoritative Decision Block

> **Authoritative Decision Block.**  
> 1. **Gate 9 — PASSED (Localized Carrier Propagation, Source–Birth Interleaving, and Post-Excitation Taxonomy):** Across all $407$ non-isomorphic posets up to $N \le 5$, covering-link propagation $\Phi_{\rm prop}$ achieves **zero carrier-bundle violations** on both baseline diamonds ($0 / 73{,}786$, max diff $0.0$) and post-excitation diamonds ($0 / 14{,}276$ on $N \le 4$, max diff $0.0$). Baseline CSG Growth–Growth diamonds ($0 / 73{,}786$, max diff $1.39 \times 10^{-17}$) and event-anchored Source–Birth interleaving diamonds ($0 / 73{,}786$ Formulation A newborn pairs; $0 / 12{,}842$ Formulation B existing-vertex pairs) commute with zero violations. Cone-internal redistribution satisfies exact row normalization (max error $2.22 \times 10^{-16}$), strict spacelike non-disturbance ($\Delta q(T) \equiv 0.0$ for all $T \not\ni u_*$), and cone-entry conservation (max error $1.11 \times 10^{-16}$). On post-excitation Growth–Growth diamonds, Cone-Closure Redistribution reduces mixed cone–spacelike violations from $6{,}388 / 6{,}388$ to **$0 / 6{,}388$** (max diff $2.78 \times 10^{-17}$), leaving only inner cone–cone overlap pairs ($1{,}988 / 3{,}944$) where local frontier rules without global marked-core potentials do not commute.
> 2. **Gate 10 — PASSED (Persistent $O(1)$ All-Horizon Intra-Cone Coupling Without Cutoff $N_{\rm act}$):** Coupling $(c_0, q_0) = (0.20, 0.20)$ and intra-cone focused mode $(c_1, q_1) = (0.90, 0.60)$ at gain $\kappa = 2.00$ ($\gamma = 0.0$) under unmodified Stage 9 $\Phi_{\rm prop}$ guarantees strict branch positivity ($q(C, X, I) \ge \frac{1}{1+\kappa} q_0(C, I) > 0$; audited $\min q = 4.01 \times 10^{-2}$), exact row normalization (error $0.0$), Kolmogorov cylinder projectivity ($\mathbb{P}_{N+1}\vert_{\mathcal{F}_N} = \mathbb{P}_N$, deviation $0.0$), and $\rho_{\rm post}(N) \equiv 0.0$ across $N \in \{256, 512, 1024, 2048\}$. Near-source covering-link contrast grows monotonically across horizons ($\Delta\rho_{\rm link}: +0.7813 \to +0.9817 \to +1.0797 \to +1.1045$), exceeding $\delta_* = 0.20$ by nearly $4\times$ at every tested scale, while $\kappa = 0$ and vacuum fault injections yield exact $\operatorname{TVD} = 0.0$ and bitwise identical trajectories.
> 3. **Gate 11 — PASSED (Coordinate-Free Spacelike Non-Disturbance, Non-Tautological Attenuation, and Bidirectional Clock Exchange):** Under synchronized CRN streams: (i) Tier 1 confirms $\max\lvert\Delta L_{\max}(u_{\rm far})\rvert = 0$, $\max\lvert\Delta\rho_{\rm link}(u_{\rm far})\rvert = 0.0$, and $\max p_1(u_{\rm far}) = 0.0$ at $N \in \{256, 512\}$ alongside near-source dilation $\Delta L_{\max} \in [+10.70, +14.80]$; (ii) Tier 2 ($N = 512, M = 15, \gamma = 0.12$) confirms bitwise zero shift on the uncoupled control (`Control Arm B - Baseline Arm A == 0.0`), strict monotone decay of $p_1$ across $d_{\rm link} = 1 \dots 8$ ($0.6542 \to 0.0492$), and non-tautological monotone growth of Hasse covering in-degree shift $\Delta k_{\rm Hasse}$ across $\eta_{\rm ov}$ bins ($0.0000 \to +0.1439 \to +0.5656 \to +0.8736$, near-core minus distant-periphery contrast $+0.7065$); (iii) Tier 3 confirms bidirectional causal relays ($X \to Y: 1.0 \to 4.0$; $Y \to X: 2.1 \to 9.4$), exact conservation $N_{\rm relay} + N_{\rm abst} = N_{\rm sent}$, and $\Delta\mathcal{R} = +1.2763, +1.8466, +2.4757$ across $N \in \{256, 512, 1024\}$.

### 1.3 Epistemic Status Matrix

| Result / Component | Formal Statement | Epistemic Status | Verification Evidence |
|:---|:---|:---:|:---|
| **Proposition 9.1** (CPTP Covering-Link Localization) | $X = (C, \{\mathcal{Z}_v\}_{v \in V(C)})$ with $\Phi_{\rm prop}$ reading solely $\operatorname{Max}(S)$ is CPTP and Markov-sufficient on newborn frontiers. | `[PROVED PROPOSITION]` | Analytic proof (§2.2) + unit tests & audit across $407$ posets ($N \le 5$). |
| **Theorem 9.2** (Carrier, Baseline GG & Source–Birth Commutation) | Carrier propagation commutes universally; baseline CSG Growth–Growth and event-anchored Source–Birth interleaving diamonds commute identically. | `[PROVED THEOREM]` | Analytic proof (§2.4) + exhaustive audit ($73{,}786$ GG + $86{,}628$ SB pairs; $0$ violations, max diff $1.39 \times 10^{-17}$). |
| **Theorem 9.3** (Cone-Internal Redistribution & Non-Disturbance) | Partitioning $\mathcal{I}(C) = \mathcal{I}_{\not\ni u_*} \sqcup \mathcal{I}_{\ni u_*}$ preserves $\sum_I q = 1$, $\Delta q(T) \equiv 0$ ($T \not\ni u_*$), and $\sum_{S \ni u_*} q(S) = P_{\rm enter}(C; u_*)$. | `[PROVED THEOREM]` | Analytic proof (§2.5) + $186$ anchor checks (max row err $2.22 \times 10^{-16}$, spacelike err $0.0$). |
| **Theorem 9.4** (Post-Excitation Taxonomy & Cone-Closure Repair) | Routing slack within $S_{\rm cone}(C; u_*) = J^-_C[J^+_C[u_*]]$ eliminates $100\%$ of mixed cone–spacelike post-excitation violations ($0/6{,}388$ vs. $6{,}388/6{,}388$), isolating inner cone–cone overlaps ($1{,}988/3{,}944$). | `[PROVED THEOREM]` | Analytic proof (§2.6) + exhaustive $14{,}276$-quadruple audit (`stage9_localized_carrier_experiment.py`). |
| **Theorem 10.1** (Exact Analytical–Sampler Intra-Cone Kernel) | Closed-form ideal probabilities and rejection-free Vandermonde/intra-cone seed sampling define the identical all-horizon Markov law without $N_{\rm act}$, with $q > 0$, $\sum q = 1$, $\mathbb{P}_{N+1}\vert_{\mathcal{F}_N} = \mathbb{P}_N$. | `[PROVED THEOREM]` | Analytic proof (§3.2–3.5) + $40{,}000$-draw equivalence test (`max err < 0.01`) & prefix invariance up to $N = 2048$. |
| **Proposition 10.2 & Theorem 10.3** (Persistent Contrast & Decoupling Collapse) | Empirical $\rho_{\rm post}(N) \equiv 0.0$ and $\Delta\rho_{\rm link}(N) \in [0.7813, 1.1045] \ge 0.20$ across $N \in \{256, \dots, 2048\}$; $\kappa = 0$ and $\rho_{\rm vac}$ collapse to $q_0$ with $\operatorname{TVD} = 0.0$. | `[VERIFIED BENCHMARK / PROVED COLLAPSE]` | Analytic decoupling proof (§3.7) + $M = 15$ multi-horizon sweep (`stage10_coupling_experiment_results.json`). |
| **Proposition 11.1** (CRN Spacelike Non-Disturbance) | Partitioned $(\text{rng}_{\rm ext}, \text{rng}_{\rm cone})$ streams preserve bitwise identity of $J^-[u_{\rm far}]$ for all $u_{\rm far} \notin J^+[u_{\rm src}] \cup J^-[u_{\rm src}]$. | `[PROVED PROPOSITION]` | Analytic proof (§4.2) + $100\%$ zero-shift audit at $N = 256, 512$. |
| **Proposition 11.2** (Link-Depth Bound & Overlap In-Degree Shift) | $p_1(v) \le (1 - \gamma)^{d_{\rm link}(u_{\rm src}, v)}$ holds unconditionally; empirically $\Delta k_{\rm Hasse}$ vanishes at $\eta_{\rm ov} = 0$ and increases monotonically across $\eta_{\rm ov}$ bins. | `[PROVED BOUND / VERIFIED SCALING]` | Analytic induction (§4.3) + $N = 512, M = 15$ benchmark (`stage11_comparison_experiment_results.json`). |
| **Theorem 11.3** (Two-Worldline Clock Exchange & Transitivity Scope) | Tick exchange satisfies $N_{\rm relay} + N_{\rm abst} = N_{\rm sent}$ identically; peripheral chains ($\eta_{\rm ov} \le 0.30$) support two-way relays with $\Delta\mathcal{R} \ge +1.2763$, whereas strictly exterior chains forbid $X \to Y_{\rm ext}$ by order transitivity. | `[PROVED CONSERVATION / VERIFIED BENCHMARK]` | Analytic proof (§4.4) + multi-horizon audit ($N = 256, 512, 1024$). |
| **Status-M Quarantine** | Zero edits to `det8/`, `scripts/`, `run_tests.py`, `main`, or Status-M/protocol files; strictly mathematical and order-theoretic identifiers throughout. | `[SYSTEM INVARIANT]` | Confirmed by `git diff` (`0` lines outside `docs/track_b/`). |

---

## 2. Stage 9: Localized Present-State Carrier & Order-Consistent Source Introduction

### 2.1 From Monolithic $X = (C, \mathcal{Z})$ to the Vertex-Frontier Bundle $X = (C, \{\mathcal{Z}_v\})$
Under `docs/track_b/RECORD_PROCESS_CONTRACT.md`, a relational process state has the form $X = (C, \mathcal{Z})$. To eliminate Stage 8's spatially undifferentiated register without storing non-present global birth counters, we decentralize $\mathcal{Z}$ into a **localized vertex-frontier carrier bundle**:
$$
X = \left(C, \{\mathcal{Z}_v\}_{v \in V(C)}\right), \qquad \mathcal{Z}_v \in \mathcal{D}(\mathbb{C}^2) := \{\rho \in \mathcal{B}(\mathbb{C}^2) : \rho = \rho^\dagger, \;\rho \succeq 0, \;\operatorname{Tr}(\rho) = 1\}.
$$
Each committed event $v \in V(C)$ carries an immutable density operator $\mathcal{Z}_v$ recorded at its commitment. When a newborn event $x_S$ is adjoined above a downward-closed precursor ideal $S \in \mathcal{I}(C)$, its incoming Hasse covering links originate exclusively from the maximal frontier of $S$:
$$
\operatorname{Max}_C(S) := \{u \in S : \nexists v \in S \text{ with } u \prec v\}.
$$
Accordingly, the newborn carrier $\mathcal{Z}_{x_S}$ is synthesized strictly from $\{\mathcal{Z}_m\}_{m \in \operatorname{Max}_C(S)}$.

### 2.2 Covering-Link CPTP Propagation Channel $\Phi_{\rm prop}$
Let $\{\lvert 0\rangle, \lvert 1\rangle\}$ denote the computational basis of $\mathbb{C}^2$, with vacuum ground state $\rho_{\rm vac} = \lvert 0\rangle\langle 0\rvert = \operatorname{diag}(1, 0)$ and excited state $\rho_{\rm exc} = \lvert 1\rangle\langle 1\rvert = \operatorname{diag}(0, 1)$. For $M = \operatorname{Max}_C(S)$:
1. If $M = \varnothing$ ($S = \varnothing$, minimal root birth), $\Phi_{\rm prop}(\varnothing) := \rho_{\rm vac}$.
2. If $\lvert M\rvert \ge 1$, form the permutation-symmetric frontier mean $\bar{\mathcal{Z}}_M := \frac{1}{\lvert M\rvert}\sum_{m \in M} \mathcal{Z}_m$, apply coherent link phase rotation $U_{\rm link} = \operatorname{diag}(e^{-i\omega_0}, e^{-i\omega_1})$, and apply vacuum damping $\gamma \in [0, 1]$:
   $$
   \Phi_{\rm prop}\left(\{\mathcal{Z}_m\}_{m \in M}\right) := (1 - \gamma)\, U_{\rm link} \bar{\mathcal{Z}}_M U_{\rm link}^\dagger + \gamma\, \rho_{\rm vac}.
   $$

**Proposition 9.1 (`[PROVED PROPOSITION]` CPTP Frontier Propagation and Markov Sufficiency).**  
*For every finite frontier $M \subseteq V(C)$ and $\gamma \in [0, 1]$, $\Phi_{\rm prop}: \mathcal{D}(\mathbb{C}^2)^{\lvert M\rvert} \to \mathcal{D}(\mathbb{C}^2)$ is completely positive, trace-preserving, symmetric under permutations of $M$, and conditionally independent of all non-maximal ancestors $S \setminus \operatorname{Max}_C(S)$.*

*Proof.* Uniform convex averaging $\bar{\mathcal{Z}}_M = \frac{1}{\lvert M\rvert}\sum_{m \in M} \mathcal{Z}_m$ is a permutation-invariant convex combination of marginal projections, hence CPTP. Unitary conjugation $\rho \mapsto U_{\rm link}\rho U_{\rm link}^\dagger$ and convex mixing $(1 - \gamma)(\cdot) + \gamma\rho_{\rm vac}$ with a fixed density matrix $\rho_{\rm vac} \in \mathcal{D}(\mathbb{C}^2)$ are CPTP for all $\gamma \in [0, 1]$; their composition is CPTP. Because $\Phi_{\rm prop}$ reads only $\{\mathcal{Z}_m : m \in \operatorname{Max}_C(S)\}$, altering $\mathcal{Z}_u$ for $u \in S \setminus \operatorname{Max}_C(S)$ leaves $\mathcal{Z}_{x_S}$ identically unchanged. $\blacksquare$

### 2.3 Event-Anchored Source Introduction Operator $\mathcal{U}_{\rm src}^{(u_*)}$
Rather than triggering at an extrinsic birth counter $n_0$ (which excites different physical events under different linear extensions of incomparable elements), source introduction is anchored directly to a designated committed event $u_* \in V(C)$:
$$
\mathcal{U}_{\rm src}^{(u^*)}\left(C, \{\mathcal{Z}_v\}_{v \in V(C)}\right) := \left(C, \{\mathcal{Z}'_v\}_{v \in V(C)}\right), \qquad
\mathcal{Z}'_v = \begin{cases}
U_{\rm src} \mathcal{Z}_{u_*} U_{\rm src}^\dagger, & v = u_*, \\
\mathcal{Z}_v, & v \ne u_*,
\end{cases}
$$
with $U_{\rm src} = \sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, mapping $\rho_{\rm vac} \mapsto \rho_{\rm exc}$ at $u_*$ while leaving $C$ and all $\mathcal{Z}_v$ ($v \ne u_*$) bitwise unchanged.

### 2.4 Baseline Growth–Growth and Source–Birth Interleaving Commutation

**Theorem 9.2 (`[PROVED THEOREM]` Universal Carrier Commutation, Baseline Growth–Growth, and Source–Birth Interleaving).**  
*Let $C$ be any finite causal set with arbitrary vertex carriers $\{\mathcal{Z}_v\}_{v \in V(C)}$, and let $q_0(C, \cdot)$ denote any Rideout–Sorkin Classical Sequential Growth transition kernel.*
1. **Universal Carrier-Bundle Diamond Commutation:** *For any ideals $S, T \in \mathcal{I}(C)$, adjoining $x_S$ at index $n$ then $y_T$ at index $n+1$ (Path 1) versus adjoining $y_T$ at index $n$ then $x_S$ at index $n+1$ (Path 2) produces canonically isomorphic carrier-decorated states under the transposition $\sigma = (n \leftrightarrow n+1)$: $\sigma(X^{(21)}) \equiv X^{(12)}$, regardless of whether an excited source $u_* \in V(C)$ is already present.*
2. **Baseline Growth–Growth Probability Commutation:** *Under $q_0$, $q_0(C, S)\, q_0(C + x_S, T) = q_0(C, T)\, q_0(C + y_T, S)$ for all $S, T \in \mathcal{I}(C)$.*
3. **Source–Birth Interleaving Commutation (under any kernel satisfying $q(P, X, T) = q_0(P, T)$ for $T \not\ni u_*$):**
   - *Formulation A (Newborn Source Pair): Committing $u_* = x_S$, applying $\mathcal{U}_{\rm src}^{(u_*)}$, and committing $y_T$ ($T \in \mathcal{I}(C)$, hence $u_* \notin T$) yields the identical state and path probability as committing $y_T$ unexcited, then committing $u_* = x_S$, and applying $\mathcal{U}_{\rm src}^{(u_*)}$.*
   - *Formulation B (Existing Source Pair): For any existing $u_* \in V(C)$ and any $T \in \mathcal{I}_{\not\ni u_*}(C)$, applying $\mathcal{U}_{\rm src}^{(u_*)}$ before versus after committing $y_T$ yields identical transition probabilities $q_{\rm exc}(C, T) = q_0(C, T)$ and identical resulting carrier bundles.*

*Proof.*  
**1.** Since $T \subseteq V(C)$ does not contain the newborn vertex $x_S$ ($x_S \notin V(C)$), the induced order on $T$ in $C + x_S$ equals that in $C$, so $\operatorname{Max}_{C + x_S}(T) = \operatorname{Max}_C(T)$. Because existing carriers in $V(C)$ are immutable under `add_vertex`, $\mathcal{Z}_{y_T}^{(12)} = \Phi_{\rm prop}(\{\mathcal{Z}_m : m \in \operatorname{Max}_C(T)\}) = \mathcal{Z}_{y_T}^{(21)}$, and symmetrically $\mathcal{Z}_{x_S}^{(21)} = \mathcal{Z}_{x_S}^{(12)}$. Note that this holds for *any* parent carrier assignment $\{\mathcal{Z}_v\}_{v \in V(C)}$, including post-excitation states.  
**2.** In Rideout–Sorkin CSG, $q_0(C, S) = \operatorname{Num}(C, S)/Z_n$ where $\operatorname{Num}(C, S)$ depends only on $\lvert S\rvert$ and $\lvert\operatorname{Max}_C(S)\rvert$. Since $\operatorname{Max}_{C + x_S}(T) = \operatorname{Max}_C(T)$ and $\operatorname{Max}_{C + y_T}(S) = \operatorname{Max}_C(S)$, both paths have numerator product $\operatorname{Num}(C, S)\operatorname{Num}(C, T)$ and denominator product $Z_n Z_{n+1}$.  
**3.** In Formulation A, $u_* = x_S \notin T$ implies $q(C + x_S, \mathcal{U}_{\rm src}^{(x_S)}(X_{x_S}), T) = q_0(C + x_S, T)$, reducing Path 1's joint probability to $q_0(C, S)\, q_0(C + x_S, T) = q_0(C, T)\, q_0(C + y_T, S)$, which equals Path 2's joint probability. Because $u_* \notin \operatorname{Max}_{C + x_S}(T)$, $\mathcal{Z}_{y_T}$ is unaffected by $\mathcal{U}_{\rm src}^{(x_S)}$. Formulation B follows similarly from $u_* \notin T \implies u_* \notin \operatorname{Max}_C(T)$ and $q_{\rm exc}(C, T) = q_0(C, T)$. $\blacksquare$

#### Table 2.1: Exhaustive Baseline Growth–Growth and Source–Birth Diamond Audit ($N \le 5$)
Values match `docs/track_b/verification/stage9_carrier_experiment_results.json` across all $407$ non-isomorphic posets up to $N = 5$:

| Horizon $N$ | Non-Isomorphic Posets | Baseline GG Diamonds | GG Violations | Max GG Prob Diff | SB Form. A Diamonds | SB Form. A Violations | SB Form. B Diamonds | SB Form. B Violations | Max Carrier Matrix Diff |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $1$ | $1$ | $4$ | $0$ | $1.39 \times 10^{-17}$ | $4$ | $0$ | $1$ | $0$ | $0.0$ |
| $2$ | $2$ | $25$ | $0$ | $3.47 \times 10^{-18}$ | $25$ | $0$ | $7$ | $0$ | $0.0$ |
| $3$ | $7$ | $238$ | $0$ | $1.73 \times 10^{-18}$ | $238$ | $0$ | $60$ | $0$ | $0.0$ |
| $4$ | $40$ | $3{,}377$ | $0$ | $6.94 \times 10^{-18}$ | $3{,}377$ | $0$ | $714$ | $0$ | $0.0$ |
| $5$ | $357$ | $70{,}142$ | $0$ | $6.94 \times 10^{-18}$ | $70{,}142$ | $0$ | $12{,}060$ | $0$ | $0.0$ |
| **Total** | **$407$** | **$73{,}786$** | **$0$** | **$1.39 \times 10^{-17}$** | **$73{,}786$** | **$0$** | **$12{,}842$** | **$0$** | **$0.0$** |

### 2.5 Cone-Internal Probability Redistribution and Spacelike Non-Disturbance

**Theorem 9.3 (`[PROVED THEOREM]` Cone-Internal Ideal Partition and Spacelike Non-Disturbance).**  
*For any finite causal set $C$ and source event $u_* \in V(C)$, partition $\mathcal{I}(C) = \mathcal{I}_{\not\ni u_*}(C) \sqcup \mathcal{I}_{\ni u_*}(C)$ and define $P_{\rm enter}(C; u_*) := \sum_{S \in \mathcal{I}_{\ni u_*}(C)} q_0(C, S)$. Any transition kernel that sets $q(C, X, T) = q_0(C, T)$ for all $T \in \mathcal{I}_{\not\ni u_*}(C)$ and redistributes mass among $S \in \mathcal{I}_{\ni u_*}(C)$ with total mass $P_{\rm enter}(C; u_*)$ satisfies:*
1. **Exact Row Normalization:** $\sum_{I \in \mathcal{I}(C)} q(C, X, I) = 1$.
2. **Strict Spacelike Non-Disturbance:** $\Delta q(T) := q(C, X, T) - q_0(C, T) \equiv 0$ for all $T \in \mathcal{I}_{\not\ni u_*}(C)$.
3. **Cone-Entry Conservation:** $\sum_{S \in \mathcal{I}_{\ni u_*}(C)} q(C, X, S) = P_{\rm enter}(C; u_*)$.

*Proof.* Summing over $\mathcal{I}_{\not\ni u_*}(C)$ gives $1 - P_{\rm enter}(C; u_*)$ and summing over $\mathcal{I}_{\ni u_*}(C)$ gives $P_{\rm enter}(C; u_*)$, totaling $1$. Claims 2 and 3 hold by definition of the partition. $\blacksquare$

#### Table 2.2: Cone-Internal Redistribution Invariant Audit ($N \le 4$, $186$ Anchor Configurations)

| Invariant Checked | Mathematical Condition | Tolerance | Audited Maximum Error | Status |
|:---|:---|:---:|:---:|:---:|
| **Row Normalization** | $\lvert\sum_{I \in \mathcal{I}(C)} q(C, X, I) - 1\rvert$ | $\le 10^{-14}$ | $2.22 \times 10^{-16}$ | **PASS** |
| **Spacelike Non-Disturbance** | $\max_{T \not\ni u_*} \lvert q(C, X, T) - q_0(C, T)\rvert$ | $\equiv 0.0$ | $0.00 \times 10^{00}$ | **PASS** |
| **Cone-Entry Conservation** | $\lvert\sum_{S \ni u_*} q(C, X, S) - P_{\rm enter}(C; u_*)\rvert$ | $\le 10^{-14}$ | $1.11 \times 10^{-16}$ | **PASS** |

### 2.6 Post-Excitation Growth–Growth Diamond Taxonomy and Cone-Closure Repair
Theorem 9.2 Part 2 audited Growth–Growth probability commutation for the *unperturbed* CSG baseline $q_0$ (`u_star = None`). Rigorous claim hygiene requires separately auditing **post-excitation Growth–Growth diamonds**, where $u_* \in V(C)$ is *already excited* before incomparable births $x_S, y_T$ occur!

Suppose $q(C, X, T) = q_0(C, T)$ holds for all $T \not\ni u_*$. For a **mixed cone–spacelike diamond** ($S \in \mathcal{I}_{\ni u_*}(C)$, $T \in \mathcal{I}_{\not\ni u_*}(C)$), since $u_* \notin T$ and $x_S \notin T$, we have $q(C, X, T) = q_0(C, T)$ and $q(C + x_S, X', T) = q_0(C + x_S, T)$. Dividing the diamond condition $q(C, X, S)\, q(C + x_S, X', T) = q(C, X, T)\, q(C + y_T, X'', S)$ by the CSG identity $q_0(C, S)\, q_0(C + x_S, T) = q_0(C, T)\, q_0(C + y_T, S)$ yields the exact necessary and sufficient condition for mixed post-excitation commutation:
$$
\frac{q(C, X, S)}{q_0(C, S)} = \frac{q(C + y_T, X'', S)}{q_0(C + y_T, S)} \qquad \forall\, S \in \mathcal{I}_{\ni u_*}(C),\; \forall\, T \in \mathcal{I}_{\not\ni u_*}(C).
$$
Under naive stage-renormalized cone weighting $q(C, X, S) = P_{\rm enter}(C; u_*)\frac{w(S)}{Z_{\rm cone}(C)}$ (`ConeRedistributionTransitionEngine`), once $\lvert J^+_C[u_*]\rvert \ge 2$, adjoining $y_T$ adds cross-join ideals $S \cup \{y_T\}$ to $\mathcal{I}_{\ni u_*}(C + y_T)$, altering $P_{\rm enter} / Z_{\rm cone}$ and violating mixed cone–spacelike diamonds (`6,388 / 6,388` pairs on $N \le 4$).

We repair 100% of mixed cone–spacelike diamonds via **Cone-Closure Redistribution** (`ConeClosureRedistributionEngine`): define the cone-past closure ideal
$$
S_{\rm cone}(C; u_*) := J^-_C\bigl[J^+_C[u_*]\bigr] \in \mathcal{I}_{\ni u_*}(C).
$$
For every proper sub-ideal $S \subsetneq S_{\rm cone}(C; u_*)$ with $u_* \in S$, attenuate $q_{\rm cc}(C, X, S) := (1 - \lambda_{\rm att}(S))\, q_0(C, S)$ where $\lambda_{\rm att}(S) = \eta_{\rm gain}\max_{m \in \operatorname{Max}_C(S)} p_1(m) \in [0, 1)$, route the exact slack $\sum_{S \subsetneq S_{\rm cone}, u_* \in S} \lambda_{\rm att}(S)\, q_0(C, S)$ into $S_{\rm cone}(C; u_*)$, and leave all other ideals—both $T \not\ni u_*$ and cross-join ideals $S' \not\subseteq S_{\rm cone}(C; u_*)$—equal to $q_0(C, \cdot)$.

**Theorem 9.4 (`[PROVED THEOREM]` Exact Mixed-Diamond Commutation of Cone-Closure Redistribution and Inner-Cone Scope).**  
*Under Cone-Closure Redistribution $q_{\rm cc}$:*
1. *Exact row normalization ($\sum_I q_{\rm cc} = 1$), branch positivity ($q_{\rm cc} > 0$ for $\eta_{\rm gain} \in [0, 1)$), strict spacelike non-disturbance, and cone-entry conservation hold on every finite poset $C$.*
2. *Every post-excitation Spacelike–Spacelike diamond ($S, T \not\ni u_*$) and every post-excitation Mixed Cone–Spacelike diamond ($S \ni u_*, T \not\ni u_*$) commutes **identically**.*
3. *Universal commutation across Inner Cone–Cone diamonds ($S_1, S_2 \ni u_*$) additionally requires that $q(C, X, I)/q_0(C, I) = \widehat{L}(\operatorname{Core}(C + x_I; u_*))/\widehat{L}(\operatorname{Core}(C; u_*))$ factor through a positive potential on the marked cone-past core $\operatorname{Core}(C; u_*) = S_{\rm cone}(C; u_*)$; local frontier rules without global core potentials exhibit inner-cone overlap non-commutativity analogous to `CR-1` Proposition 6.3.*

*Proof.*  
**1.** The slack subtracted from $\{S \subsetneq S_{\rm cone} : u_* \in S\}$ is added directly to $S_{\rm cone} \in \mathcal{I}_{\ni u_*}(C)$, preserving $\sum_{S \ni u_*} q_{\rm cc}(C, X, S) = P_{\rm enter}(C; u_*)$ and $\sum_I q_{\rm cc} = 1$.  
**2.** Let $T \in \mathcal{I}_{\not\ni u_*}(C)$ and adjoin $y_T$. Since $u_* \notin T$, $y_T \notin J^+_{C + y_T}[u_*]$, so $J^+_{C + y_T}[u_*] = J^+_C[u_*]$; since $y_T$ is maximal in $C + y_T$, $y_T$ lies below no element of $J^+_C[u_*]$, whence $S_{\rm cone}(C + y_T; u_*) = S_{\rm cone}(C; u_*)$. Moreover, for every $S' \subseteq S_{\rm cone}(C; u_*) \subseteq V(C)$, $y_T \notin S'$ implies $\operatorname{Max}_{C + y_T}(S') = \operatorname{Max}_C(S')$, invariant frontier carriers, and $\operatorname{Num}(C + y_T, S') = \operatorname{Num}(C, S')$. In the ratio
$$
\frac{q_{\rm cc}(C, X, S_{\rm cone})}{q_0(C, S_{\rm cone})} = 1 + \sum_{S' \subsetneq S_{\rm cone},\, u_* \in S'} \lambda_{\rm att}(S')\, \frac{\operatorname{Num}(C, S')}{\operatorname{Num}(C, S_{\rm cone})},
$$
the stage partition sum $Z_n$ cancels identically! Thus $q_{\rm cc}(C + y_T, X'', S)/q_0(C + y_T, S) = q_{\rm cc}(C, X, S)/q_0(C, S)$ for all $S \in \mathcal{I}_{\ni u_*}(C)$ (including $S \subsetneq S_{\rm cone}$, $S = S_{\rm cone}$, and $S \not\subseteq S_{\rm cone}$ where both sides equal $1$), proving exact mixed commutation.  
**3.** Universal diamond commutation across all $(S, T)$ holds iff $q(C, I) = \mathcal{W}(C + x_I)/\mathcal{W}(C)$ for a marked-poset invariant $\mathcal{W}$; setting $L = \mathcal{W}/\mathcal{W}_0$, spacelike non-disturbance $L(C + y_T) = L(C)$ ($T \not\ni u_*$) holds iff $L$ is invariant under peeling maximal vertices outside $S_{\rm cone}(C; u_*)$, i.e., $L(C; u_*) = \widehat{L}(S_{\rm cone}(C; u_*))$. When both $S_1, S_2 \ni u_*$, adjoining $x_{S_1}$ expands $S_{\rm cone}(C + x_{S_1}; u_*) = S_{\rm cone}(C; u_*) \cup S_1 \cup \{x_{S_1}\}$, so local frontier rules not derived from $\widehat{L}$ need not commute on $(S_1, S_2)$. $\blacksquare$

#### Table 2.3: Exhaustive Post-Excitation Growth–Growth Diamond Taxonomy ($N \le 4$, $14{,}276$ Quadruples)
Values match `post_excitation_diamond_taxonomy` in `docs/track_b/verification/stage9_carrier_experiment_results.json`:

| Post-Excitation Diamond Category | Audited Quadruples $(C, u_*, S, T)$ | Carrier Bundle $\Phi_{\rm prop}$ Violations | Stage-Normalized $Z_{\rm cone}$ Violations | Cone-Closure $q_{\rm cc}$ Violations | Max $q_{\rm cc}$ Prob Diff |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Spacelike–Spacelike** ($S, T \not\ni u_*$) | $3{,}944$ | **$0$** | $0$ | **$0$** | $6.94 \times 10^{-18}$ |
| **Mixed Cone–Spacelike** ($S \ni u_*, T \not\ni u_*$) | $6{,}388$ | **$0$** | $6{,}388$ | **$0$** | $2.78 \times 10^{-17}$ |
| **Inner Cone–Cone** ($S_1, S_2 \ni u_*$) | $3{,}944$ | **$0$** | $2{,}746$ | $1{,}988$ *(overlap frontier)* | — |
| **Total ($N \le 4$)** | **$14{,}276$** | **$0$** (max diff $0.0$) | $9{,}134$ | $1{,}988$ ($0 / 10{,}332$ non-inner) | — |

---

## 3. Stage 10: Persistent $O(1)$ All-Horizon Local Coupling

### 3.1 Eliminating the $N_{\rm act}$ Cutoff with Exact Analytical–Sampler Alignment
Stage 10 constructs an all-horizon sequential growth law without any terminal cutoff $N_{\rm act}$, ensuring two strict methodological requirements:
1. **Unmodified Stage 9 Carrier Propagation:** Newborn vertices inside $J^+[u_{\rm src}]$ synthesize their carrier via the exact Stage 9 CPTP channel $\Phi_{\rm prop}$ averaging over **all** incoming Hasse covering parents $\operatorname{Max}(S)$ (with zero hidden `in_cone` filtering).
2. **Exact Analytical–Sampler Equivalence:** Rather than pairing an exponential ideal-sum formula on small posets with a heuristic approximation at $N = 2048$, both `PersistentLocalTransitionEngine.compute_probabilities` and `simulate_persistent_trajectory` implement the **exact same Intra-Cone Focused Seed Markov Kernel**.

### 3.2 Definition of the Intra-Cone Focused Seed Markov Kernel
Let $\mathbf{t}_0, \mathbf{t}_1$ denote Log-Quadratic subset coupling sequences:
$$
t_{0, k} = c_0^k q_0^{\binom{k}{2}} \;\text{ with }\; (c_0, q_0) = (0.20, 0.20), \qquad
t_{1, k} = c_1^k q_1^{\binom{k}{2}} \;\text{ with }\; (c_1, q_1) = (0.90, 0.60),
$$
truncated at $k_{\rm cap} = 32$ (where $q_1^{\binom{32}{2}} = 0.60^{496} < 10^{-110}$, well below IEEE-754 double underflow). Let $Z_m(\mathbf{t}_0) = \sum_{k=0}^{\min(m, k_{\rm cap})} \binom{m}{k} t_{0, k}$.

For a causal set $C$ of size $n = \lvert V(C)\rvert$ with source $u_* \in V(C)$, future cone $F = J^+_C[u_*]$ ($\lvert F\rvert = F_n \ge 1$), and exterior $E = V(C) \setminus F$ ($\lvert E\rvert = n_{\rm ext} = n - F_n$):
1. **Baseline Cone-Entrance Split:** Since $F$ is upward-closed, a seed subset $B \subseteq V(C)$ generates an ideal $S = J^-_C[B] \ni u_*$ if and only if $B \cap F \ne \varnothing$. Under baseline CSG $\mathbf{t}_0$, this occurs with exact probability
   $$
   P_{\rm enter}(C; u_*) = 1 - \frac{Z_{n - F_n}(\mathbf{t}_0)}{Z_n(\mathbf{t}_0)}.
   $$
   With probability $1 - P_{\rm enter}(C; u_*)$, draw $B \subseteq E$ from baseline CSG $\mathbf{t}_0$ on $E$, inducing $q(C, X, T) \equiv q_0(C, T)$ for every $T \in \mathcal{I}_{\not\ni u_*}(C)$.
2. **Local Cone Probe and Intra-Cone Focused Activation:** Conditioned on entering $F$ (probability $P_{\rm enter}(C; u_*)$), sample a local cone event $v_{\rm probe} \sim \operatorname{Unif}(F)$ and read its local excitation $p_1(v_{\rm probe}) = \operatorname{Re}\langle 1\rvert\mathcal{Z}_{v_{\rm probe}}\lvert 1\rangle \in [0, 1]$, defining rational saturation coupling:
   $$
   \lambda(v) := \frac{\kappa\, p_1(v)}{1 + \kappa\, p_1(v)} \in \left[0, \frac{\kappa}{1 + \kappa}\right], \qquad \bar{\lambda}(F, X) := \frac{1}{F_n}\sum_{v \in F} \lambda(v),
   $$
   calibrated at $\kappa = 2.00$ ($\lambda(v) \in [0, 2/3]$) and $\gamma = 0.0$ for Stage 10.
   - **Baseline Conditional Branch (probability $1 - \lambda(v_{\rm probe})$):** Draw $B \sim \mathbb{P}_{\mathbf{t}_0}(B \mid B \cap F \ne \varnothing)$ via exact two-step Vandermonde sampling: first draw total seed size $k \in \{1, \dots, \min(n, k_{\rm cap})\}$ with weight $\bigl[\binom{n}{k} - \binom{n - F_n}{k}\bigr] t_{0, k}$, then draw $r = \lvert B \cap F\rvert \in \{\max(1, k - n_{\rm ext}), \dots, \min(k, F_n)\}$ with hypergeometric weight $\binom{F_n}{r}\binom{n_{\rm ext}}{k - r}$, and sample $r$ seeds in $F$ plus $k - r$ seeds in $E$. By Vandermonde's identity $\sum_{r \ge 1}\binom{F_n}{r}\binom{n_{\rm ext}}{k - r} = \binom{n}{k} - \binom{n_{\rm ext}}{k}$, this induces the **exact** conditional CSG law $q_0(C, S)/P_{\rm enter}(C; u_*)$ on every $S \in \mathcal{I}_{\ni u_*}(C)$!
   - **Intra-Cone Focused Branch (probability $\lambda(v_{\rm probe})$):** Draw a focused intra-cone seed set $B \subseteq F$ containing $v_{\rm probe}$ by choosing $j = \lvert B \setminus \{v_{\rm probe}\}\rvert \in \{0, \dots, \min(F_n - 1, k_{\rm cap} - 1)\}$ with weight $\binom{F_n - 1}{j} t_{1, j+1} / Z_{F_n}^{(1)}(1)$, where $Z_{F_n}^{(1)}(1) = \sum_{j=0}^{\min(F_n-1, k_{\rm cap}-1)} \binom{F_n - 1}{j} t_{1, j+1}$. Because $B \subseteq F$, focused births draw parents strictly inside $J^+_C[u_*]$, preventing exterior vacuum dilution of $\Phi_{\rm prop}$ without modifying Stage 9's covering-link rule.

### 3.3 Closed-Form Ideal Probabilities, Positivity, and Projectivity

**Theorem 10.1 (`[PROVED THEOREM]` Exact Ideal Kernel, All-Horizon Positivity, Normalization, and Kolmogorov Projectivity).**  
*For every finite causal set $C$ ($n = \lvert V(C)\rvert \ge 0$), carrier bundle $X$, and $\kappa \ge 0$, the generative process of §3.2 induces the closed-form ideal transition kernel:*
$$
q(C, X, I) = \begin{cases}
q_0(C, I), & I \in \mathcal{I}_{\not\ni u_*}(C), \\
\bigl(1 - \bar{\lambda}(F, X)\bigr)\, q_0(C, I) + \dfrac{P_{\rm enter}(C; u_*)}{F_n} \displaystyle\sum_{v \in I \cap F} \lambda(v)\, q_1^{(v)}(C, I), & I \in \mathcal{I}_{\ni u_*}(C),
\end{cases}
$$
*where $q_1^{(v)}(C, S) = 0$ if $\operatorname{Max}_C(S) \not\subseteq F$, and when $\operatorname{Max}_C(S) \subseteq F$ (with $d = \lvert\operatorname{Max}_C(S)\rvert$ and $p_F = \lvert S \cap F\rvert - d$):*
$$
q_1^{(v)}(C, S) = \begin{cases}
\dfrac{1}{Z_{F_n}^{(1)}(1)}\displaystyle\sum_{j=0}^{p_F} \binom{p_F}{j} t_{1, d + j}, & v \in \operatorname{Max}_C(S), \\
\dfrac{1}{Z_{F_n}^{(1)}(1)}\displaystyle\sum_{j=0}^{p_F - 1} \binom{p_F - 1}{j} t_{1, d + 1 + j}, & v \in (S \cap F) \setminus \operatorname{Max}_C(S).
\end{cases}
$$
*Consequently, for all $n \ge 0$ without any terminal horizon cutoff $N_{\rm act}$:*
1. **Strict Branch Positivity:** $q(C, X, I) \ge \frac{1}{1 + \kappa}\, q_0(C, I) > 0$ for every ideal $I \in \mathcal{I}(C)$.
2. **Exact Row Normalization:** $\sum_{I \in \mathcal{I}(C)} q(C, X, I) = 1$.
3. **Kolmogorov Cylinder Projectivity:** The sequential path measures $\{\mathbb{P}_N\}_{N \ge 1}$ on labeled causal-set histories satisfy $\mathbb{P}_{N+1}\vert_{\mathcal{F}_N} = \mathbb{P}_N$ for all $N \ge 1$.

*Proof.* For $v \in B \subseteq F$, $J^-_C[B] = S$ holds iff $\operatorname{Max}_C(S) \subseteq B \subseteq S \cap F$ and $v \in S \cap F$; counting subsets $B \setminus \{v\}$ by cardinality yields the two cases of $q_1^{(v)}(C, S)$, and summing over all ideals $S \in \mathcal{I}_{\ni u_*}(C)$ partitions $\{B \subseteq F : v \in B\}$, giving $\sum_{S \ni u_*} q_1^{(v)}(C, S) = 1$ for every $v \in F$. Hence $\sum_{S \ni u_*} q(C, X, S) = (1 - \bar{\lambda}) P_{\rm enter} + \frac{P_{\rm enter}}{F_n}\sum_{v \in F}\lambda(v) = P_{\rm enter}$, proving Claim 2. Since $\lambda(v) \le \frac{\kappa}{1 + \kappa}$, $1 - \bar{\lambda}(F, X) \ge \frac{1}{1 + \kappa} > 0$ and $q_1^{(v)} \ge 0$, proving Claim 1. Because every one-step Markov transition row sums to $1$ with no dependence on a future stopping horizon $N$, marginalizing step $N + 1$ yields $\mathbb{P}_{N+1}\vert_{\mathcal{F}_N} = \mathbb{P}_N$ identically (Claim 3). $\blacksquare$

*(Empirical Equivalence Check: In `test_stage10_verification.py`, $40{,}000$ draws of the forward sampler on a $5$-vertex poset with mixed cone/exterior ancestry match `PersistentLocalTransitionEngine.compute_probabilities` across all ideals within statistical sampling noise $< 0.01$.)*

### 3.4 Vanishing Global Post Density and Persistent Contrast Across $N \in \{256, 512, 1024, 2048\}$
Across $M = 15$ paired trajectories per horizon (`stage10_coupling_experiment_results.json`), the global post count is identically zero at every horizon:
$$
\rho_{\rm post}(N) = \frac{\langle N_{\rm post}\rangle}{N} \equiv 0.000000 \qquad \forall\, N \in \{256, 512, 1024, 2048\}.
$$
Within $J^+[u_{\rm src}]$, we measure three structural observables between coupled ($\kappa = 2.00$) and unperturbed ($\kappa = 0$ / baseline CSG) runs:
1. **Covering Link Density:** $\rho_{\rm link} := \frac{\text{Hasse links in } J^+[u_{\rm src}]}{\lvert J^+[u_{\rm src}]\rvert - 1}$ (primary Gate 10 observable $\mathcal{O}_{\rm near}$).
2. **Cone Comparability Fraction:** $r_2 := \frac{C_1(J^+[u_{\rm src}])}{\binom{\lvert J^+[u_{\rm src}]\rvert}{2}}$.
3. **Cone Chain Height:** $h_{\max} := \text{longest directed chain in } J^+[u_{\rm src}]$.

#### Table 3.1: Persistent Downstream Near-Source Contrast Across Macroscopic Horizons ($N = 256 \to 2048$, $M = 15$)
Values match `docs/track_b/verification/stage10_coupling_experiment_results.json`:

| Horizon $N$ | Coupled $\rho_{\rm link}$ | Unperturbed $\rho_{\rm link}$ | Contrast $\Delta\rho_{\rm link}$ | Exceeds $\delta_* = 0.20$? | Coupled $r_2$ | Unperturbed $r_2$ | Contrast $\Delta r_2$ | Coupled $h_{\max}$ | Unperturbed $h_{\max}$ | Contrast $\Delta h_{\max}$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $256$ | $2.0608$ | $1.2795$ | **$+0.7813$** | **YES** | $0.3964$ | $0.1124$ | $+0.2840$ | $20.07$ | $12.33$ | $+7.73$ |
| $512$ | $2.5342$ | $1.5525$ | **$+0.9817$** | **YES** | $0.3342$ | $0.0719$ | $+0.2623$ | $29.07$ | $15.67$ | $+13.40$ |
| $1024$ | $2.9919$ | $1.9122$ | **$+1.0797$** | **YES** | $0.3144$ | $0.0634$ | $+0.2509$ | $38.07$ | $20.33$ | $+17.73$ |
| $2048$ | $3.4363$ | $2.3318$ | **$+1.1045$** | **YES** | $0.3182$ | $0.0690$ | $+0.2492$ | $48.60$ | $26.20$ | $+22.40$ |

Across all tested horizons up to $N = 2048$, $\min_N \Delta\rho_{\rm link}(N) = +0.7813 \ge \delta_* = 0.20$, with $\Delta\rho_{\rm link}$ increasing monotonically ($+0.7813 \to +0.9817 \to +1.0797 \to +1.1045$) and $\Delta h_{\max}$ growing from $+7.73$ to $+22.40$ ticks without parameter retuning.

### 3.5 Exact Decoupling Collapse Under Fault Injection
**Theorem 10.3 (`[PROVED COLLAPSE]` Exact Decoupling Equivalence).**  
*Whenever $\kappa = 0$ or all cone carriers lie in the vacuum state $\rho_{\rm vac}$ ($p_1(v) \equiv 0$), $\lambda(v) \equiv 0$ and $\bar{\lambda}(F, X) \equiv 0$, so $q(C, X, I) \equiv q_0(C, I)$ identically ($\operatorname{TVD}(q, q_0) = 0.0$) and the forward sampler executes the exact same pseudorandom draws as the unperturbed baseline.*

Audited in `stage10_coupling_experiment_results.json`: both $\kappa = 0$ and vacuum-carrier fault injections produce $\Delta\rho_{\rm link} = 0.0$, bitwise identical `pasts` arrays, and $\operatorname{TVD}(q_{\kappa=0}, q_0) = \operatorname{TVD}(q_{\rm vac}, q_0) = 0.0$.

---

## 4. Stage 11: Source vs. Distant Comparison Protocol & Relational Attenuation

### 4.1 Coordinate-Free Poset-Intrinsic Observables
Without assuming a continuum metric or $1/r^2$ falloff, Stage 11 defines three purely order-theoretic relational quantities relative to $u_{\rm src}$:
1. **Distant Spacelike Comparison Anchor ($u_{\rm far}$):** The vertex in $V(C) \setminus (J^+[u_{\rm src}] \cup J^-[u_{\rm src}])$ maximizing past causal volume $\lvert J^-[v]\rvert$ and chain height $L_{\max}(v)$.
2. **Covering Link Depth ($d_{\rm link}$):** Shortest directed path distance from $u_{\rm src}$ to $v \in J^+[u_{\rm src}]$ in the Hasse covering reduction (`hasse_cone`).
3. **Alexandrov Causal Overlap Fraction ($\eta_{\rm ov}$):**
   $$
   \eta_{\rm ov}(v) := \frac{\lvert J^-[v] \cap J^+[u_{\rm src}]\rvert}{\lvert J^-[v]\rvert} = \frac{\lvert[u_{\rm src}, v]\rvert}{\lvert J^-[v]\rvert} \in [0, 1].
   $$

### 4.2 Tier 1: Exact Spacelike Non-Disturbance Under Synchronized CRN Streams

**Proposition 11.1 (`[PROVED PROPOSITION]` CRN Bitwise Past Invariance Outside $J^+[u_{\rm src}]$).**  
*Because `simulate_persistent_trajectory` draws all pre-source births, cone-entrance Bernoulli trials ($P_{\rm enter}$), and exterior parent sets ($B \subseteq V \setminus F$) exclusively from $\text{rng}_{\rm ext}$, while drawing cone-interior parent choices exclusively from $\text{rng}_{\rm cone}$, coupled ($\kappa = 2.00$) and unperturbed ($\kappa = 0$) runs sharing the same seed induce bitwise identical sub-posets $J^-[u_{\rm far}]$ and pure vacuum carriers $\mathcal{Z}_{u_{\rm far}} = \rho_{\rm vac}$ for every $u_{\rm far} \notin J^+[u_{\rm src}]$.*

*Proof.* By upward closure of $J^+[u_{\rm src}]$, $u_{\rm far} \notin J^+[u_{\rm src}] \implies J^-[u_{\rm far}] \cap J^+[u_{\rm src}] = \varnothing$. By induction on birth step $n$, the indicator sequence $\{\mathbf{1}_{v \in J^+[u_{\rm src}]}\}_{v < n}$ (hence $F_n$, $n_{\rm ext}$, and $P_{\rm enter}(n, F_n)$) and every exterior parent set drawn from $\text{rng}_{\rm ext}$ are identical in both runs, never desynchronizing $\text{rng}_{\rm ext}$. Hence $J^-[u_{\rm far}]$ is bitwise identical across runs, yielding $\Delta L_{\max}(u_{\rm far}) \equiv 0$, $\Delta\rho_{\rm link}(u_{\rm far}) \equiv 0.0$, and $p_1(u_{\rm far}) \equiv 0.0$. $\blacksquare$

#### Table 4.1: Tier 1 Spacelike Non-Disturbance Audit ($M = 10$ Paired Runs per Horizon)
Values match `docs/track_b/verification/stage11_comparison_experiment_results.json`:

| Horizon $N$ | Samples | Distant $\max \lvert\Delta L_{\max}\rvert$ | Distant $\max \lvert\Delta\rho_{\rm link}\rvert$ | Distant $\max p_1$ | Near-Source Mean $\Delta L_{\max}$ | Near-Source Mean $\Delta\rho_{\rm link}$ | Spacelike Non-Disturbance? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $256$ | $10$ | **$0$** | **$0.0000$** | **$0.0000$** | $+10.70$ | $+0.5926$ | **VERIFIED** |
| $512$ | $10$ | **$0$** | **$0.0000$** | **$0.0000$** | $+14.80$ | $+0.8365$ | **VERIFIED** |

### 4.3 Tier 2: Monotone Link-Depth Decay and Non-Tautological Causal-Overlap Response

**Proposition 11.2 (`[PROVED BOUND / VERIFIED SCALING]` Covering-Link Damping Bound and Non-Tautological Overlap Shift).**  
1. **Analytic Link-Depth Upper Bound:** *Under $\Phi_{\rm prop}$ with damping $\gamma \in (0, 1)$, every vertex $v \in J^+[u_{\rm src}]$ at shortest Hasse covering distance $d = d_{\rm link}(u_{\rm src}, v) \ge 1$ satisfies*
   $$
   p_1(v) \le (1 - \gamma)^{d_{\rm link}(u_{\rm src}, v)}.
   $$
2. **Non-Tautological Overlap Structural Response:** *Let $k_{\rm Hasse}(v) := \lvert\operatorname{Max}_C(J^-[v] \setminus \{v\})\rvert$ denote the immediate Hasse covering in-degree of $v$, and define the paired structural shift $\Delta k_{\rm Hasse}(\mathcal{B}) := \langle k_{\rm Hasse}\rangle_{\rm coupled, \mathcal{B}} - \langle k_{\rm Hasse}\rangle_{\rm uncoupled, \mathcal{B}}$ in overlap bin $\mathcal{B}$. Unlike the fraction of transitive predecessors in $J^+[u_{\rm src}]$ (which algebraically duplicates $\eta_{\rm ov}$), $k_{\rm Hasse}$ decreases across higher $\eta_{\rm ov}$ bins in uncoupled CSG ($2.4320 \to 1.9234$), whereas active coupling drives $\Delta k_{\rm Hasse}$ strictly monotonically upward across $\eta_{\rm ov}$ while vanishing identically at $\eta_{\rm ov} = 0$.*

*Proof of Part 1.* At $u_{\rm src}$, $p_1(u_{\rm src}) = 1 = (1 - \gamma)^0$. Suppose the bound holds for all vertices born before $v$, and let $d = d_{\rm link}(u_{\rm src}, v) \ge 1$ with $M = \operatorname{Max}_C(J^-[v] \setminus \{v\})$. Every covering parent $m \in M \cap J^+[u_{\rm src}]$ has a Hasse covering edge $m \prec_* v$ in $J^+[u_{\rm src}]$, so by the shortest-path triangle inequality $d_{\rm link}(u_{\rm src}, m) \ge d - 1$, giving $p_1(m) \le (1 - \gamma)^{d - 1}$; every exterior covering parent $m \in M \setminus J^+[u_{\rm src}]$ has $p_1(m) = 0 \le (1 - \gamma)^{d - 1}$. Since $U_{\rm link}$ is diagonal in $\{\lvert 0\rangle, \lvert 1\rangle\}$ and $\langle 1\rvert\rho_{\rm vac}\lvert 1\rangle = 0$, $p_1(v) = (1 - \gamma)\frac{1}{\lvert M\rvert}\sum_{m \in M} p_1(m) \le (1 - \gamma)(1 - \gamma)^{d - 1} = (1 - \gamma)^d$. $\blacksquare$

#### Table 4.2: Tier 2 Link-Depth Attenuation and Non-Tautological Overlap Shift ($N = 512, M = 15, \kappa = 2.00, \gamma = 0.12$)
Values match `docs/track_b/verification/stage11_comparison_experiment_results.json`:

| Link Depth $d_{\rm link}$ | Mean Excitation $p_1$ | Monotone Decay? | Overlap Bin $\eta_{\rm ov}$ | Coupled $\langle k_{\rm Hasse}\rangle$ | Uncoupled $\langle k_{\rm Hasse}\rangle$ | Shift $\Delta k_{\rm Hasse}$ | Monotone Growth? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $1$ | $0.6542$ | — | $[0.00, 0.01)$ | $1.9592$ | $1.9592$ | **$0.0000$** | — |
| $2$ | $0.3949$ | **DECREASING** | $[0.01, 0.30)$ | $2.5759$ | $2.4320$ | **$+0.1439$** | **INCREASING** |
| $3$ | $0.2663$ | **DECREASING** | $[0.30, 0.60)$ | $2.7741$ | $2.2086$ | **$+0.5656$** | **INCREASING** |
| $4$ | $0.1972$ | **DECREASING** | $[0.60, 1.01)$ | $2.7970$ | $1.9234$ | **$+0.8736$** | **INCREASING** |
| $5$ | $0.1556$ | **DECREASING** | — | — | — | — | — |
| $6$ | $0.1155$ | **DECREASING** | — | — | — | — | — |
| $7$ | $0.0791$ | **DECREASING** | — | — | — | — | — |
| $8$ | $0.0492$ | **DECREASING** | — | — | — | — | — |

**Disambiguated Control and Regional Attenuation Comparisons:**
- **Uncoupled Control Check (`Control Arm B` vs. `Baseline Arm A`):** Comparing `Control Arm B` (source excited at $u_{\rm src}$ with coupling gain $\kappa = 0$) against `Baseline Arm A` (unexcited baseline) yields $\text{Control Arm B} - \text{Baseline Arm A} \equiv 0.000000$, with `pasts` and adjacency matrices $C$ bitwise identical.
- **Depth-Conditioned Coupling Attenuation:** Mean local coupling activation decays from $\langle\lambda_{\rm coup}\rangle_{d_{\rm link} \in \{1, 2\}} = 0.4373$ to $\langle\lambda_{\rm coup}\rangle_{d_{\rm link} \ge 5} = 0.1862$ (net depth contrast $+0.2511 > 0$). *(Note: by definition of a covering link $u_{\rm src} \prec_* v$, any $d_{\rm link} = 1$ vertex satisfies $J^-[v] \cap J^+[u_{\rm src}] = \{u_{\rm src}, v\}$ and thus has at most $1$ in-cone covering parent, whereas structural multi-parent focusing manifests across higher causal overlap $\eta_{\rm ov}$.)*
- **Near-Core vs. Distant-Periphery Structural Contrast:** Comparing the **Near-Core Overlap Region** ($\eta_{\rm ov} \ge 0.50$: $\Delta k_{\rm Hasse} = +0.6289$) against the **Distant Low-Overlap Periphery** ($\eta_{\rm ov} < 0.20$: $\Delta k_{\rm Hasse} = -0.0776$) yields a net regional structural contrast of **$+0.7065 > 0$**.

### 4.4 Tier 3: Operational Two-Worldline Clock-Exchange Protocol
Tier 3 constructs two maximal directed timelike chains via dynamic programming:
1. **Worldline $X$ (Near-Source Core):** Maximal chain in $J^+[u_{\rm src}]$ starting at $u_{\rm src}$.
2. **Worldline $Y$ (Distant Low-Overlap Periphery):** Maximal chain starting at $u_{\rm far} \notin J^+[u_{\rm src}] \cup J^-[u_{\rm src}]$ within the low-overlap peripheral domain $\{v \in J^+[u_{\rm far}] : \eta_{\rm ov}(v) \le 0.30\}$.

> [!IMPORTANT]
> **Methodological Avoidance of the Exterior Transitivity Tautology:** If a comparison chain $Y_{\rm ext}$ is restricted strictly to $V(C) \setminus J^+[u_{\rm src}]$, then **by transitivity of $\prec$** no tick $x_i \in J^+[u_{\rm src}]$ can ever precede any $y_j \in Y_{\rm ext}$ ($u_{\rm src} \preceq x_i \prec y_j \implies y_j \in J^+[u_{\rm src}]$), forcing $N_{\rm relay}(X \to Y_{\rm ext}) \equiv 0$ as a trivial set-theoretic identity rather than a dynamical "horizon" effect! Defining Worldline $Y$ on the low-overlap periphery ($\eta_{\rm ov} \le 0.30$) allows late peripheral events to receive sparse causal links from $X$, testing genuine **bidirectional** signal exchange ($X \to Y$ and $Y \to X$) alongside the strictly exterior reference chain $Y_{\rm ext}$.

**Theorem 11.3 (`[PROVED CONSERVATION / VERIFIED BENCHMARK]` Exact Relay/Abstention Conservation and Clock-Ratio Shift).**  
*For each emitted tick $x_i \in X$, record a relay at $y_{\rm arr}(x_i) = \min\{j : x_i \prec y_j\}$ if non-empty and an abstention otherwise (and symmetrically for $Y \to X$). Then:*
1. **Exact Channel Conservation:** $N_{\rm relay}(X \to Y) + N_{\rm abst}(X \to Y) \equiv \lvert X\rvert$ and $N_{\rm relay}(Y \to X) + N_{\rm abst}(Y \to X) \equiv \lvert Y\rvert$ on every causal set.
2. **Measured Clock-Ratio Contrast:** Across $N \in \{256, 512, 1024\}$ ($M = 10$), both $X \to Y$ and $Y \to X$ exhibit positive relay counts, $\mathcal{R}_{\rm coupled} = \lvert X\rvert/\lvert Y\rvert \ne 1.0$, and $\Delta\mathcal{R} := \mathcal{R}_{\rm coupled} - \mathcal{R}_{\rm uncoupled}$ grows monotonically from $+1.2763$ to $+2.4757$.

*Proof of Part 1.* Every emitted index in $\{0, \dots, \lvert X\rvert - 1\}$ maps to either a unique minimum index in $Y$ (incrementing $N_{\rm relay}$ by $1$) or the empty arrival set (incrementing $N_{\rm abst}$ by $1$). $\blacksquare$

#### Table 4.3: Tier 3 Bidirectional Two-Worldline Clock-Exchange Benchmark ($N \in \{256, 512, 1024\}$, $M = 10$)
Values match `docs/track_b/verification/stage11_comparison_experiment_results.json`:

| Horizon $N$ | Mean $\lvert X\rvert$ | Mean $\lvert Y\rvert$ | Coupled $\mathcal{R}_{\rm coupled}$ | Uncoupled $\mathcal{R}_{\rm uncoupled}$ | Contrast $\Delta\mathcal{R}$ | Exterior Ref. $\Delta\mathcal{R}_{\rm ext}$ | $X \to Y$ Relays / Abst. | $Y \to X$ Relays / Abst. | $Y \to X$ Fail Rate |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $256$ | $16.3$ | $7.5$ | **$2.7392$** | $1.4629$ | **$+1.2763$** | $+1.2333$ | $1.0 \; / \; 15.3$ | $2.1 \; / \; 5.4$ | $69.5\%$ |
| $512$ | $24.6$ | $9.3$ | **$3.4777$** | $1.6311$ | **$+1.8466$** | $+1.6343$ | $1.9 \; / \; 22.7$ | $7.1 \; / \; 2.2$ | $26.9\%$ |
| $1024$ | $34.2$ | $10.4$ | **$4.5358$** | $2.0601$ | **$+2.4757$** | $+2.0970$ | $4.0 \; / \; 30.2$ | $9.4 \; / \; 1.0$ | $8.8\%$ |

*(Note: Even in uncoupled baseline CSG, $\mathcal{R}_{\rm uncoupled} > 1$ because $u_{\rm src} = 4$ is an early birth whereas $u_{\rm far}$ is born later outside $J^+[u_{\rm src}]$; the paired differential shift $\Delta\mathcal{R} = \mathcal{R}_{\rm coupled} - \mathcal{R}_{\rm uncoupled} \in [+1.2763, +2.4757]$ isolates the genuine dynamical elongation induced by localized carrier coupling.)*

---

## 5. Verification Ledger, Open Theoretical Boundaries, and Status-M Hygiene

### 5.1 Master Verification Ledger Across Gates 9, 10, and 11

| Gate Criterion | Mathematical / Empirical Requirement | Verification Script | Observed Result | Status |
|:---|:---|:---|:---:|:---:|
| **Gate 9.1** | Carrier bundle & baseline Growth–Growth diamonds commute ($N \le 5$). | `stage9_localized_carrier_experiment.py` | **$0 / 73{,}786$ violations** (max prob diff $1.39 \times 10^{-17}$, carrier diff $0.0$) | **PASS** |
| **Gate 9.2** | Event-anchored Source–Birth interleaving diamonds commute ($N \le 5$). | `stage9_localized_carrier_experiment.py` | **$0 / 86{,}628$ violations** (Form A: $73{,}786$; Form B: $12{,}842$) | **PASS** |
| **Gate 9.3** | Cone redistribution preserves $\sum q = 1$, $\Delta q(T) \equiv 0$, and mixed post-excitation repair. | `stage9_localized_carrier_experiment.py` | Row err $2.22 \times 10^{-16}$; spacelike err $0.0$; Cone-Closure mixed **$0 / 6{,}388$** | **PASS** |
| **Gate 10.1** | Exact analytical–sampler alignment, $q > 0$, $\sum q = 1$, no cutoff $N_{\rm act}$. | `stage10_persistent_coupling_experiment.py` | $\min q = 4.01 \times 10^{-2} > 0$, row err **$0.0$**, MC vs. exact $< 0.01$ | **PASS** |
| **Gate 10.2** | Kolmogorov cylinder projectivity $\mathbb{P}_{N+1}\vert_{\mathcal{F}_N} = \mathbb{P}_N$ & $\rho_{\rm post} \to 0$. | `stage10_persistent_coupling_experiment.py` | Prefix dev **$0.0$**, $\rho_{\rm post} \equiv \mathbf{0.000000}$ ($N = 256 \dots 2048$) | **PASS** |
| **Gate 10.3** | Persistent contrast $\min_N \lvert\Delta\mathcal{O}_{\rm near}(N)\rvert \ge \delta_* = 0.20$ & fault collapse. | `stage10_persistent_coupling_experiment.py` | $\min \Delta\rho_{\rm link} = \mathbf{+0.7813} \ge 0.20$ ($+0.7813 \to +1.1045$), fault $\operatorname{TVD} = 0.0$ | **PASS** |
| **Gate 11.1** | Tier 1 exact zero spacelike shift at $u_{\rm far} \notin J^+[u_{\rm src}] \cup J^-[u_{\rm src}]$. | `stage11_relational_comparison_experiment.py` | $\Delta L_{\max} = \mathbf{0}$, $\Delta\rho_{\rm link} = \mathbf{0.0000}$, $p_1 = \mathbf{0.0000}$ ($N = 256, 512$) | **PASS** |
| **Gate 11.2** | Tier 2 monotone $d_{\rm link}$ decay, non-tautological $\eta_{\rm ov}$ growth, control $= 0.0$. | `stage11_relational_comparison_experiment.py` | Decay: **TRUE**, $\Delta k_{\rm Hasse}$ growth: **TRUE** ($0.0 \to +0.8736$), control: **$0.0$** | **PASS** |
| **Gate 11.3** | Tier 3 bidirectional two-worldline clock exchange ($\mathcal{R} \ne 1$, $N_{\rm relay} + N_{\rm abst} = N_{\rm sent}$). | `stage11_relational_comparison_experiment.py` | $\Delta\mathcal{R}: +1.2763 \to +2.4757$, bidirectional relays verified | **PASS** |

### 5.2 Open Mathematical Boundaries (No Overclaiming)
1. **Inner Cone–Cone Post-Excitation Commutation:** While Cone-Closure Redistribution (`Theorem 9.4`) achieves exact commutation across $100\%$ of Spacelike–Spacelike and Mixed Cone–Spacelike post-excitation diamonds, two births occurring *both* inside $J^+[u_*]$ ($S_1, S_2 \ni u_*$) still exhibit order dependence ($1{,}988 / 3{,}944$ on $N \le 4$) unless transition weights derive from a global marked-core potential $\widehat{L}(S_{\rm cone}(C; u_*))$. Constructing a tractable polynomial-time all-horizon marked-core potential $\widehat{L}$ remains an explicit open problem.
2. **Discrete Relational Contrast vs. Continuum Metric Gravity:** The covering-link attenuation ($d_{\rm link}$), Alexandrov overlap shift ($\Delta k_{\rm Hasse}$), and worldline tick-ratio shift ($\Delta\mathcal{R}$) demonstrate localized, persistent, coordinate-free source-to-surroundings response in a sequential poset process. They do **not** yet establish 4D Lorentzian manifold emergence (`CR-1a–d`), Newtonian $1/r^2$ falloff, or Einstein's field equations.

### 5.3 Status-M Boundary Hygiene and Quarantine Discipline
In accordance with `ONTOLOGY.md`, `GOVERNANCE.md`, and `docs/track_b/RECORD_PROCESS_CONTRACT.md`:
1. **Zero Core or Protocol Modifications:** Zero edits have been made to `det8/`, `scripts/`, `run_tests.py`, `main`, `qr-pair-kernel-bridge`, `ONTOLOGY.md`, `GOVERNANCE.md`, `PHYSICS.md`, `FALSIFICATION_LEDGER.md`, `PW6A_PROTOCOL.md`, or `PW6B_PROTOCOL.md`. All deliverables reside strictly inside `docs/track_b/` and `docs/track_b/verification/`.
2. **Strict Mathematical Identifier Hygiene:** All mathematical symbols, equations, and code identifiers are strictly mathematical, physical, or order-theoretic, preserving the Status-M quarantine boundary.
3. **KaTeX Formatting Compliance:** All inline math uses `$ ... $`, display math uses `$$ ... $$`, and vertical bars inside Markdown tables use `\lvert ... \rvert`.
