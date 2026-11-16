# DET v8.0 Track B — Stage 8: Nested-Regime Dynamics, Multi-Horizon Scale-Pattern Holdout, and Active Source-Perturbation Response on $X = (C, \mathcal{Z})$

**Document ID**: `nested_regime_dynamics_and_source_response.md`  
**Stage**: Stage 8 (Track B Mathematical & Computational Verification Package)  
**Date**: 2026-11-16  
**Verification Suite**: `docs/track_b/verification/run_nested_regime_verification.py` (18 unit/property tests, 4 acceptance gates; deterministic output in `docs/track_b/verification/nested_regime_experiment_results.json`)  
**Epistemic Scope**: Conditional mathematical theorems, exact finite-poset diamond audits, pre-declared multi-horizon holdout tests, and paired three-arm source-response simulations under the declared state $X = (C, \mathcal{Z})$. Status M remains strictly quarantined.

---

## 1. Executive Summary, Scope, and Pre-Declared Decision Block

### 1.1 Research Objective
Stage 7 (`CR-1`) showed that critical Log-Quadratic Classical Sequential Growth ($t_k = c^k q^{\binom{k}{2}}$ with $c = 0.20, q = 0.20$) maintains single-history global comparability near $R_2(P_N) \approx 0.10$ up to $N = 1024$ while exhibiting strong interval-cardinality crossover across $m = \lvert I(u, v)\rvert$. However, three decisive questions remained open before connecting nested causal regimes to the mass/gravity correspondence programme (`NEXT_STEPS.md`, `docs/coordination/NATIVE_MASS_MAPPING.md`):

1. **Pillar 1 (Frozen Multi-Horizon & Multi-Observable Scale-Pattern Holdout):** When parameters $(c, q) = (0.20, 0.20)$ (and companion $(0.20, 0.10)$) are **frozen without retuning** and tested up to $N = 2048$ (plus $N = 4096$) across **five** distinct interval observables—not $R_2(I)$ alone—does uncoupled static scalar Log-Quadratic CSG define a genuinely $N$-stationary 4D geometry at fixed interval cardinality $m$, or does its parent-seed scale $\mu_N \propto \ln N$ induce systematic logarithmic drift?
2. **Pillar 2 (Nested-Regime Projection & Live Residual-to-Structure Coupling on $X = (C, \mathcal{Z})$):** Following the semantic process contract (`docs/track_b/RECORD_PROCESS_CONTRACT.md`) with state $X = (C, \mathcal{Z})$ and operations `evolve_residual`, `commit_record`, and `access_records`, how does coarse-graining $\Pi_{\mathcal{A}}(C, \mathcal{Z}) = (\widetilde{C}, \widetilde{\mathcal{Z}})$ transform causal dynamics, can active off-diagonal residual-to-structure coupling (`docs/track_b/native_active_residual_v1.md`, `NM004`) be extended rigorously beyond $N = 4$ births across all subset-weight CSG kernels, and how does present-state `evolve_residual` intervention separate live $X = (C, \mathcal{Z})$ laws from every passive static-seed de Finetti mixture?
3. **Pillar 3 (Paired Source-Perturbation to Clock-Tick & Interval Focusing Bridge):** Starting from **100% identical committed prefixes** $C_{n_0}$ ($n_0 = 128$) evolved to $N = 512$ and $N = 1024$, does an explicit `evolve_residual` source excitation produce zero structural shift under an uncoupled forward-only control (`Arm B - Arm A == 0`) while generating a statistically decisive shift in downstream chain-tick count, causal cone volume, matched-cardinality interval geometry, coarse-grained anchor connectivity, and two-way Bayesian residual recoil (`Order -> Residual`) under nested active coupling (`Arm C`)?

### 1.2 Authoritative Decision Block

> **Decision.**  
> 1. **Honest Retirement of Uncoupled Static Scalar Log-Quadratic CSG as a Standalone Stationary Geometry Law (Pillar 1):** Under the frozen holdout test across $N \in \{512, 1024, 2048\}$ and $N = 4096$, `log_quad_c02_q020` confirms strong within-horizon $m$-scale crossover ($R_2(I)$ drops monotonically from $0.8243$ at $m \in [6, 11]$ to $0.2284$ at $m \in [49, 96]$ for $N = 2048$, span $0.5959$), **but fails strict fixed-$m$ $N$-stationarity and fails 4D transverse hypersurface width**. By the **Exact Future-Cone 1D Markov Chain Proposition** (Proposition 2.1), every subset-weight CSG law drives inclusive future-cone size $F_n(u) = \lvert J^+_{P_n}[u]\rvert$ via $\mathbb{P}(F_{n+1} = F_n + 1 \mid P_n) = 1 - Z_{n - F_n}/Z_n$, so logarithmic growth of the active parent-seed count ($\Delta \mu_{\rm octave} = \frac{\ln 2}{\ln(1/q)} = 0.4307$ per doubling at $q = 0.20$; exact $\mathbb{E}[K_N]: 2.6708 \to 3.0327 \to 3.4003 \to 3.7734$) forces monotonic upward drift in exact expected global comparability ($\mathbb{E}[R_2(P_N)]: 0.1052 \to 0.1091 \to 0.1138 \to 0.1185$ for $N = 512 \to 4096$) and fixed-window $m \in [6, 11]$ comparability ($0.7656 \to 0.8105 \to 0.8243$, $+0.0293$/octave, exceeding the pre-declared $\pm 0.012$/octave stationarity gate), while minimal-layer entry width remains narrow ($w_{\min}(I)/m = 0.1387$ at $N = 2048, m \in [12, 24]$ vs $0.6717$ in 4D Minkowski diamonds). Static scalar Log-Quadratic CSG is therefore **retired as a standalone stationary all-horizon geometry law** and retained strictly as a controlled baseline transition kernel $q_{\rm LQ}$ for coupled $X = (C, \mathcal{Z})$ dynamics.  
> 2. **Proved Coarse-Graining Memory & Arbitrary-Horizon Active Residual Coupling Theorems (Pillar 2):** Under intrinsic anchor projection $\Pi_{\mathcal{A}}(C, \mathcal{Z}) = (\widetilde{C}, \widetilde{\mathcal{Z}})$, intrinsic-past anchor selection commutes across $100\%$ of incomparable-birth diamonds ($0 / 3,644$ violations vs $3,644 / 3,644$ for extrinsic stage-parity selection), while projected order $\widetilde{C}_n$ alone is provably non-Markovian with exact omitted-chain branching ratio $\mathcal{R}_{\rm branch}(m) = Z_{m+1} - 1$ (Theorem 3.1); retaining the micro-interval shadow-volume vector $\widetilde{\mathcal{Z}}_{\rm geom}(C) = (\nu_C(I))_{I \in \mathcal{I}(\widetilde{C})}$ restores exact Markov sufficiency (maximum discrepancy $1.11 \times 10^{-16}$ across all $126$ equivalence classes up to $N = 4$). Using the exact birth-order-independent root martingale $\mathcal{M}_{\rm root}(P_n) = \lvert\operatorname{Min}(P_n)\rvert - \sum_{j=0}^{n-1} Z_j^{-1}$, Theorem 3.2 constructs a row-normalized, off-diagonal $2 \times 2$ active residual-to-structure law valid for **any** subset-weight CSG kernel (strictly entrywise positive on every supported ideal $q(P_n, S) > 0$, i.e., all $S \in \mathcal{I}(P_n)$ whenever $t_k > 0$ for all $k \ge 1$) and **any** finite horizon $N_{\rm act} \ge 2$ (verified at $N_{\rm act} = 8$ and $N_{\rm act} = 12$ with $0 / 3,644$ full-matrix diamond violations and exact nonzero update contrast $\Delta_{\rm update} = -\frac{1 - t}{2}\Delta_{\rm current} \ne 0$ on every supported ideal). Theorem 3.3 constructs an all-horizon CPTP two-mode Log-Quadratic instrument paired with `evolve_residual` source excitation and proves via an exact isomorphism-invariant cross-event identity ($\mathbb{P}_\mu(\mathcal{E}_{\rm post}(n_0)) / \mathbb{P}_\mu(\mathcal{E}_{\rm pre}(n_0)) \equiv \frac{2}{n_0 - 1}$) that even a single intervened joint distribution is impossible for **every** time-homogeneous static CSG mixture $\int \mathbb{P}_{\mathbf{t}}\,d\mu(\mathbf{t})$.  
> 3. **Verified Paired Source-to-Clock & Two-Way Recoil Bridge (Pillar 3):** Across $M = 40$ matched prefixes $C_{n_0}$ ($n_0 = 128$) evolved to $N = 512$ and $N = 1024$, uncoupled `evolve_residual` excitation (`Arm B`) yields **exact zero** structural shift relative to baseline (`Arm A`) on every observable ($0.0000 \pm 0.0000$), whereas nested active coupling (`Arm C`, $p_{\rm exc} = 1.0$) produces $> 14\sigma$ to $57\sigma$ shifts at $N = 1024$ in downstream clock ticks $L_{\max}(u_{\rm src})$ ($+6.675 \pm 0.470$, $t = 14.20$), future cone volume $\lvert J^+[u_{\rm src}]\rvert$ ($+344.20 \pm 18.13$, $t = 18.98$), coarse anchor comparability $\widetilde{R}_2(\Pi_{\mathcal{A}}(C_N))$ ($+0.1667 \pm 0.0029$, $t = 57.07$), and matched-cardinality $m \in [12, 24]$ diamond widening ($\Delta R_2(I) = -0.0325 \pm 0.0060$, $t = -5.41$), while coherent superposition ($p_{\rm exc} = 0.5$) demonstrates simultaneous structural shifts ($t = 5.27\text{--}5.88$ at $N = 1024$) and two-way Bayesian residual recoil ($\operatorname{Var}(\langle 1\rvert\mathcal{Z}_N\lvert 1\rangle) = 0.2558$ vs $0.0000$ in Arm B; single-history coherence collapse $0.5000 \to 1.08 \times 10^{-190}$). No physical clock calibration, inertial mass derivation, continuum General Relativity, or theological conclusion is claimed.

### 1.3 Epistemic Status Matrix

| Result / Component | Formal Statement | Status | Verification Evidence |
|:---|:---|:---:|:---|
| **Proposition 2.1** (Future-Cone 1D Markov Chain) | Under any subset-weight CSG law $(t_k)_{k \ge 0}$, $F_n(u) = \lvert J^+_{P_n}[u]\rvert$ evolves via $\mathbb{P}(F_{n+1} = F_n + 1 \mid P_n) = 1 - Z_{n - F_n}/Z_n$ independently of transverse topology, driving $\Delta\mu_{\rm octave} = \frac{\ln 2}{\ln(1/q)}$ drift in Log-Quadratic CSG. | `[PROVED PROPOSITION]` | Analytic proof + exact trajectory enumeration at $N = 5$ ($\text{err} < 10^{-14}$) + $N = 96$ MC check ($\lvert\Delta R_2\rvert = 0.00070 < 0.8\,\text{SEM}$). |
| **Pillar 1 Holdout Disposition** | Frozen `log_quad_c02_q020` passes $m$-scale crossover ($\Delta R_2 = 0.5959$ at $N = 2048$) but fails fixed-$m$ stationarity ($+0.0293$/octave at $m \in [6, 11]$) and 4D entry width ($w_{\min}/m = 0.1387$ vs $0.6717$); retired as standalone stationary geometry. | `[EMPIRICAL HOLDOUT DISPOSITION]` | Held-out runs across $N \in \{512, 1024, 2048\}$ ($8$ models) + $N = 4096$ check + $\delta_{\rm bulk} \in \{0.02, 0.05, 0.10\}$ sensitivity. |
| **Theorem 3.1** (Coarse Projection & Shadow Sufficiency) | Intrinsic $\Pi_{\mathcal{A}}$ commutes on all diamonds; projected order $\widetilde{C}_n$ alone is non-Markovian with omitted-chain ratio $\mathcal{R}_{\rm branch}(m) = Z_{m+1} - 1$; retaining $\widetilde{\mathcal{Z}}_{\rm geom} = (\nu_C(I))_{I \in \mathcal{I}(\widetilde{C})}$ restores exact Markov sufficiency. | `[PROVED THEOREM]` | Analytic proof + $3,644 / 3,644$ diamond audit + exhaustive $N \le 4$ audit ($126$ classes, max discrepancy $1.11 \times 10^{-16}$ vs $0.2923$ coarse-only gap). |
| **Theorem 3.2** (Arbitrary-Horizon Active Root-Martingale Law) | $\mathcal{M}_{\rm root}(P_n) = \lvert\operatorname{Min}(P_n)\rvert - \sum_{j=0}^{n-1} Z_j^{-1}$ yields a row-normalized, diamond-commuting off-diagonal $2 \times 2$ active law (strictly positive with $\Delta_{\rm update} = -\frac{1 - t}{2}\Delta_{\rm current} \ne 0$ on every supported ideal $q(P_n, S) > 0$) for any CSG kernel and any $N_{\rm act} \ge 2$. | `[PROVED THEOREM]` | Analytic proof + exhaustive $3,644$-diamond audit at $N_{\rm act} = 8$ and $N_{\rm act} = 12$ ($0$ violations, telescoping err $\le 4.44 \times 10^{-16}$). |
| **Theorem 3.3** (All-Horizon CPTP Source Law & Non-Mixture) | Two-mode instrument $K_{C_n, S}$ is CPTP and diamond-commuting for all $n \ge 0$; pairing with `evolve_residual` at $C_{n_0}$ violates every static CSG mixture $\int \mathbb{P}_{\mathbf{t}}\,d\mu(\mathbf{t})$ by factor $c_1/c_0 = 2.5$ on isomorphism-invariant events $(\mathcal{E}_{\rm pre}(n_0), \mathcal{E}_{\rm post}(n_0))$. | `[PROVED THEOREM]` / `[COUNTEREXAMPLE/OBSTRUCTION]` | Analytic proof + $3,644$-diamond operator audit ($\text{err} \le 2.23 \times 10^{-16}$) + exact full-trajectory enumeration at $n_0 \in \{2, 3, 4\}$. |
| **Pillar 3 Paired Source-Response Bridge** | Matched $C_{128} \to C_{512}, C_{1024}$ ($M = 40$): `Arm B - Arm A == 0` identically; `Arm C - Arm A` yields $+6.675$ clock ticks ($t = 14.20$), $+344.2$ cone volume ($t = 18.98$), $+0.1667$ coarse $\widetilde{R}_2$ ($t = 57.07$), and Bayesian recoil $\operatorname{Var}(p_1) = 0.2558$. | `[VERIFIED COMPUTATIONAL BRIDGE]` | Strassen common-random-numbers paired experiment ($M = 40$ runs, exact marginal preservation). |
| **Spatial $1/r$ Localization & Calibrated Gravity** | Horizon-wide mode $(q^{(0)}, q^{(1)})$ excites $u_{\rm src}$ and $u_{\rm far}$ symmetrically ($15.05$ vs $14.90$ ticks at $N = 1024$); spatially localized $1/r$ focusing via vertex-local registers $\mathcal{R}(v)$ and physical clock calibration remain open. | `[OPEN PROBLEM]` | Explicit $u_{\rm src}$ vs $u_{\rm far}$ control readout in Pillar 3 (§4.3 & §5). |

---

## 2. Pillar 1: Frozen Multi-Horizon & Multi-Observable Scale-Pattern Holdout Test

### 2.1 Pre-Declared Freeze, Controls, and Five Interval Observables
To prevent post-hoc parameter tuning, Stage 8 freezes the Stage 7 Log-Quadratic candidate `log_quad_c02_q020` ($t_k = c^k q^{\binom{k}{2}}$ with $c = 0.20, q = 0.20$, $t_0 = 1$) and its sparser companion `log_quad_c02_q010` ($c = 0.20, q = 0.10$) prior to generating any held-out seeds (`base_seed = 20260801`, disjoint from all Stage 7 seeds). We evaluate eight models across $N \in \{512, 1024, 2048\}$ ($M = 8, 8, 6$ independent histories per model, plus a large-horizon $N = 4096$, $M = 4$ check on `log_quad_c02_q020`):
- **Frozen Candidates:** `log_quad_c02_q020` ($c = 0.20, q = 0.20$) and `log_quad_c02_q010` ($c = 0.20, q = 0.10$).
- **Geometric Controls:** `minkowski_4d` (4D Alexandrov causal diamond, theoretical $f(4) = 0.1000$), `minkowski_2d` (2D Alexandrov diamond, $f(2) = 0.5000$), and `minkowski_2d_slab` (wide 2D cylinder $[0, 1] \times [0, 3]$, global $\mathbb{E}[R_2] = 11/54 \approx 0.2037$ vs internal interval $\mathbb{E}[R_2(I)] = 0.5000$).
- **Non-Geometric Controls:** `cutoff_kmax2` ($c = 1.0, k_{\max} = 2$), `percolation_p008` ($p = 0.08$), and `random_dag_sparse` ($p_N = \min(1, 2.0/N)$).

Because matching unordered-pair comparability $R_2$ alone cannot certify manifold-like causal geometry, we evaluate **five distinct structural observables** inside bulk open order intervals $I(u, v) := \{z \in P_N : u \prec z \prec v\}$ of cardinality $m = \lvert I(u, v)\rvert \ge 4$ (with bulk boundary trim $\lvert J^-(u)\rvert \ge \delta_{\rm bulk}\overline{J}_N$ and $\lvert J^+(v)\rvert \ge \delta_{\rm bulk}\overline{J}_N$, default $\delta_{\rm bulk} = 0.05$, sampling up to $20$ intervals per window per run):
1. **Comparability fraction & Myrheim–Meyer dimension:** $R_2(I) := C_1(I)/\binom{m}{2}$ and $d_{\rm MM}(I) := f^{-1}(R_2(I))$, where $f(d) = \frac{\Gamma(d+1)\Gamma(d/2)}{2\,\Gamma(3d/2)}$.
2. **Hasse link fraction:** $\ell_{\rm link}(I) := N_0(I) / \max(1, C_1(I))$, measuring the proportion of comparable pairs inside $I$ that are direct covering links ($u' \prec v'$ with no $w \in I$ satisfying $u' \prec w \prec v'$).
3. **Longest-chain proper-time density:** $h(I) / m$, where $h(I) := \max\{L \ge 1 : \exists z_1 \prec z_2 \prec \dots \prec z_L \text{ in } I\} \in \{1, \dots, m\}$ is the vertex cardinality of a maximum directed chain inside $I$ ($h(I)/m = 1$ on a total chain and $1/m$ on an antichain).
4. **Multi-step 3-chain ratio:** $\rho_2(I) := C_3(I) / \max(1, C_2(I))$, where $C_k(I) = \mathbf{1}^T C_I^k \mathbf{1}$ counts directed $k$-step chains inside $I$.
5. **Minimal-layer entry width fraction:** $w_{\min}(I) / m := \lvert\operatorname{Min}(I)\rvert / m$, measuring the initial spatial cross-section entering $I$ above $u$ (distinguishing wide 3D spatial hypersurfaces in 4D Minkowski diamonds from narrow quasi-1D spines).

We separate **fixed-cardinality windows** $m \in \{[6, 11], [12, 24], [25, 48], [49, 96]\}$ from **horizon-growing windows** $m \in [\lceil 0.5 N^\alpha\rceil, \lfloor 1.5 N^\alpha\rfloor]$ for $\alpha \in \{0.35, 0.50, 0.65\}$, and pre-declare that standalone fixed-$m$ stationarity requires $\lvert\text{drift/octave}\rvert \le 0.012$ in fixed-$m$ comparability across $N = 512 \to 2048$ alongside 4D-compatible entry width $w_{\min}(I)/m \ge 0.40$ at $m \in [12, 24]$.

### 2.2 Exact Future-Cone 1D Markov Chain Proposition (`[PROVED PROPOSITION]`)

**Proposition 2.1 (`[PROVED PROPOSITION]` Autonomous 1D Markov Evolution of Inclusive Future Cones in Subset-Weight CSG).**  
*Let $(P_n)_{n \ge 1}$ be generated by any Classical Sequential Growth law with nonnegative subset couplings $(t_k)_{k \ge 0}$ ($t_0 = 1$) and stage partition functions $Z_n := \sum_{k=0}^n \binom{n}{k} t_k > 0$ ($Z_0 := 1$). Fix any vertex $u$ born at stage $n_0 \ge 0$ (so $u \in P_{n_0+1}$ with inclusive future cone $J^+_{P_{n_0+1}}[u] := \{w \in P_{n_0+1} : u \preceq w\} = \{u\}$ and cardinality $F_{n_0+1}(u) := \lvert J^+_{P_{n_0+1}}[u]\rvert = 1$). Then relative to the full poset filtration $\mathcal{F}_n = \sigma(P_1, \dots, P_n)$, the integer sequence $(F_n(u))_{n \ge n_0+1}$ is an **exact time-inhomogeneous 1D Markov chain** whose transition probabilities are completely independent of the transverse poset topology of $P_n$:*
$$
\mathbb{P}\!\left(F_{n+1}(u) = F_n(u) \,\middle|\, \mathcal{F}_n\right) = \frac{Z_{n - F_n(u)}}{Z_n}, \qquad \mathbb{P}\!\left(F_{n+1}(u) = F_n(u) + 1 \,\middle|\, \mathcal{F}_n\right) = 1 - \frac{Z_{n - F_n(u)}}{Z_n}.
$$
*Consequently, the exact ensemble-expected comparable-pair fraction at any horizon $N \ge 2$ is determined purely by the 1D chain:*
$$
\mathbb{E}\bigl[R_2(P_N)\bigr] = \frac{1}{\binom{N}{2}} \sum_{n_0 = 0}^{N - 1} \bigl(\mathbb{E}[F_N(x_{n_0})] - 1\bigr).
$$

*Proof.* By the Rideout–Sorkin subset–ideal representation (`PW6A_PROTOCOL.md` Lemma 6.2), conditional on $P_n$ ($\lvert P_n\rvert = n$), drawing the precursor ideal $S_n \in \mathcal{I}(P_n)$ with CSG probability $q(P_n, S)$ is identically distributed to drawing a random parent subset $B_n \subseteq P_n$ with probability $\mathbb{P}(B_n = B \mid P_n) = t_{\lvert B\rvert} / Z_n$ and taking its downward closure $S_n = J^-_{P_n}[B_n] := \{w \in P_n : \exists b \in B_n,\; w \preceq b\}$. Adjoining newborn $x_n$ above $S_n$ leaves all causal relations within $P_n$ unchanged and places $x_n \in J^+_{P_{n+1}}[u]$ if and only if $u \in S_n$. By transitivity of $\preceq$:
$$
u \in J^-_{P_n}[B_n] \iff \exists b \in B_n \text{ such that } u \preceq b \iff B_n \cap J^+_{P_n}[u] \ne \varnothing.
$$
Thus $F_{n+1}(u) = F_n(u)$ if $B_n \subseteq P_n \setminus J^+_{P_n}[u]$ and $F_{n+1}(u) = F_n(u) + 1$ otherwise. Because $\lvert P_n \setminus J^+_{P_n}[u]\rvert = n - F_n(u)$, summing $t_{\lvert B\rvert}/Z_n$ over all subsets $B \subseteq P_n \setminus J^+_{P_n}[u]$ yields
$$
\mathbb{P}\!\left(F_{n+1}(u) = F_n(u) \,\middle|\, P_n\right) = \frac{1}{Z_n} \sum_{k=0}^{n - F_n(u)} \binom{n - F_n(u)}{k} t_k = \frac{Z_{n - F_n(u)}}{Z_n},
$$
which depends on $P_n$ solely through the scalar integer $F_n(u)$. Since CSG growth is Markovian on $(P_n)$, conditioning on $\mathcal{F}_n$ equals conditioning on $P_n$. Finally, $C_1(P_N) = \sum_{n_0=0}^{N-1} (\lvert J^+_{P_N}[x_{n_0}]\rvert - 1)$, and taking expectations yields the exact $R_2(P_N)$ identity. $\blacksquare$

**Logarithmic Drift Mechanism in Log-Quadratic CSG.** For $t_k = c^k q^{\binom{k}{2}}$ ($c > 0, q \in (0, 1)$), consecutive terms $w_n(k) = \binom{n}{k} c^k q^{\binom{k}{2}}$ in $Z_n$ satisfy $\frac{w_n(k+1)}{w_n(k)} = \frac{n - k}{k + 1} c q^k$. Equating this ratio to $1$ locates the active parent-seed mode at
$$
\mu_n = \frac{\ln(c n)}{\ln(1/q)} - \frac{\ln \mu_n}{\ln(1/q)} + O\!\left(\frac{1}{\mu_n}\right) = \frac{\ln(c n)}{\ln(1/q)} - O(\ln\ln n).
$$
Doubling the horizon $N \mapsto 2N$ shifts the asymptotic mode upward by $\Delta \mu_{\rm octave} = \frac{\ln 2}{\ln(1/q)} = 0.430677$ for $q = 0.20$ (and $0.301030$ for $q = 0.10$). Because $\frac{Z_{n - F}}{Z_n} = \mathbb{E}_{K_n}[(n - F)_{K_n}/(n)_{K_n}] \approx (1 - F/n)^{\mathbb{E}[K_n]}$, this steady $+0.36$ to $+0.43$ per-octave increase in active parent seeds accelerates cone capture and increases multi-parent transitive overlap inside fixed-$m$ bulk intervals born at stage $n = \Theta(N)$.

#### Table 2.1: Exact 1D Future-Cone Markov Chain Predictions vs. Monte Carlo Verification
At $N = 96$ ($400$ Monte Carlo histories of `log_quad_c02_q020`), Proposition 2.1 predicts $\mathbb{E}[R_2(P_{96})] = 0.105233$ vs. Monte Carlo $0.105930 \pm 0.000888$ ($\lvert\text{error}\rvert = 0.000698 < 0.79\,\text{SEM}$), with exact vs. MC mean future-cone sizes $\mathbb{E}[F_{96}(x_{n_0})]$ matching across birth epochs ($n_0 = 0$: $33.77$ vs $35.44$; $n_0 = 8$: $16.91$ vs $16.97$; $n_0 = 24$: $7.10$ vs $6.80$; $n_0 = 48$: $3.01$ vs $3.08$; $n_0 = 64$: $1.95$ vs $1.94$). Across macroscopic octaves $N \in \{512, 1024, 2048, 4096\}$, the exact 1D Markov chain yields:

| Horizon $N$ | $\mathbb{E}[K_N]$ ($q = 0.20$) | Octave $\Delta\mathbb{E}[K_N]$ ($q = 0.20$) | Exact $\mathbb{E}[R_2(P_N)]$ ($q = 0.20$) | $\mathbb{E}[K_N]$ ($q = 0.10$) | Exact $\mathbb{E}[R_2(P_N)]$ ($q = 0.10$) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| $512$ | $2.670821$ | — | $0.105154$ | $2.102079$ | $0.059098$ |
| $1024$ | $3.032706$ | $+0.361885$ | $0.109139$ | $2.359670$ | $0.056923$ |
| $2048$ | $3.400343$ | $+0.367638$ | $0.113776$ | $2.625502$ | $0.056342$ |
| $4096$ | $3.773424$ | $+0.373081$ | $0.118498$ | $2.890767$ | $0.056775$ |

### 2.3 Multi-Horizon & Multi-Observable Holdout Results ($N = 512, 1024, 2048, 4096$)

#### Table 2.2: Global Scaling and Fixed-Window $m \in [12, 24]$ Five-Observable Comparison Across All Eight Models
Values match `nested_regime_experiment_results.json` (`pillar1_holdout.horizons` and `large_horizon_N4096_check`). For `random_dag_sparse` ($c_{\rm deg} = 2.0$), intervals of size $m \ge 12$ never form (`n/a`) because transitive closure collapses to sparse tree-like fragments ($R_2 \to 0$).

| Horizon $N$ | Model ID | Global $\langle R_2 \rangle \pm \text{SD}$ | $\operatorname{Var}_{\rm betw}(R_2)$ | Global $d_{\rm MM}$ | $m \in [12, 24]$ $\langle R_2(I)\rangle \pm \text{SD}$ | $\langle \ell_{\rm link}(I)\rangle$ | $\langle h(I)/m\rangle$ | $\langle \rho_2(I)\rangle$ | $\langle w_{\min}(I)/m\rangle$ |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $512$ | `log_quad_c02_q020` | $0.1132 \pm 0.0059$ | $0.000035$ | $3.85$ | $0.4907 \pm 0.0417$ | $0.2959$ | $0.5185$ | $1.1212$ | $0.1336$ |
| $512$ | `log_quad_c02_q010` | $0.0582 \pm 0.0074$ | $0.000055$ | $4.65$ | $0.4920 \pm 0.0443$ | $0.3007$ | $0.5454$ | $1.0818$ | $0.1549$ |
| $512$ | `minkowski_4d` | $0.0985 \pm 0.0077$ | $0.000059$ | $4.02$ | $0.0741 \pm 0.0269$ | $0.9654$ | $0.1546$ | $0.0004$ | $0.7164$ |
| $512$ | `minkowski_2d` | $0.4911 \pm 0.0129$ | $0.000165$ | $2.02$ | $0.4981 \pm 0.0221$ | $0.4210$ | $0.3534$ | $0.7854$ | $0.2025$ |
| $512$ | `minkowski_2d_slab` | $0.2026 \pm 0.0038$ | $0.000015$ | $3.15$ | $0.5000 \pm 0.0213$ | $0.4262$ | $0.3568$ | $0.7815$ | $0.2050$ |
| $512$ | `cutoff_kmax2` | $0.1108 \pm 0.0107$ | $0.000114$ | $3.88$ | $0.5384 \pm 0.0618$ | $0.2747$ | $0.5326$ | $1.2774$ | $0.1283$ |
| $512$ | `percolation_p008` | $0.8605 \pm 0.0050$ | $0.000025$ | $1.24$ | $0.4653 \pm 0.0321$ | $0.3297$ | $0.4240$ | $1.0393$ | $0.1478$ |
| $512$ | `random_dag_sparse` | $0.0077 \pm 0.0005$ | $0.000000$ | $6.96$ | n/a | n/a | n/a | n/a | n/a |
| $1024$ | `log_quad_c02_q020` | $0.1072 \pm 0.0049$ | $0.000024$ | $3.92$ | $0.5496 \pm 0.0617$ | $0.2722$ | $0.5661$ | $1.2423$ | $0.1250$ |
| $1024$ | `log_quad_c02_q010` | $0.0583 \pm 0.0055$ | $0.000031$ | $4.64$ | $0.5188 \pm 0.0401$ | $0.2852$ | $0.5451$ | $1.1787$ | $0.1296$ |
| $1024$ | `minkowski_4d` | $0.1023 \pm 0.0053$ | $0.000028$ | $3.97$ | $0.0901 \pm 0.0121$ | $0.9444$ | $0.1525$ | $0.0005$ | $0.6760$ |
| $1024$ | `minkowski_2d` | $0.4914 \pm 0.0042$ | $0.000018$ | $2.02$ | $0.4943 \pm 0.0174$ | $0.4180$ | $0.3555$ | $0.8071$ | $0.2074$ |
| $1024$ | `minkowski_2d_slab` | $0.2020 \pm 0.0025$ | $0.000006$ | $3.15$ | $0.4962 \pm 0.0229$ | $0.4332$ | $0.3514$ | $0.7302$ | $0.2087$ |
| $1024$ | `cutoff_kmax2` | $0.0807 \pm 0.0056$ | $0.000032$ | $4.26$ | $0.5351 \pm 0.0449$ | $0.2684$ | $0.5294$ | $1.2780$ | $0.1271$ |
| $1024$ | `percolation_p008` | $0.9290 \pm 0.0019$ | $0.000004$ | $1.12$ | $0.4640 \pm 0.0188$ | $0.3302$ | $0.4171$ | $1.0186$ | $0.1480$ |
| $1024$ | `random_dag_sparse` | $0.0043 \pm 0.0003$ | $0.000000$ | $7.61$ | n/a | n/a | n/a | n/a | n/a |
| $2048$ | `log_quad_c02_q020` | $0.1148 \pm 0.0040$ | $0.000016$ | $3.84$ | $0.4966 \pm 0.0257$ | $0.2894$ | $0.5353$ | $1.1657$ | $0.1387$ |
| $2048$ | `log_quad_c02_q010` | $0.0555 \pm 0.0020$ | $0.000004$ | $4.69$ | $0.5612 \pm 0.0431$ | $0.2607$ | $0.5904$ | $1.3270$ | $0.1194$ |
| $2048$ | `minkowski_4d` | $0.1022 \pm 0.0065$ | $0.000042$ | $3.98$ | $0.0967 \pm 0.0023$ | $0.9232$ | $0.1583$ | $0.0076$ | $0.6717$ |
| $2048$ | `minkowski_2d` | $0.5019 \pm 0.0066$ | $0.000043$ | $1.99$ | $0.5014 \pm 0.0198$ | $0.4114$ | $0.3549$ | $0.8617$ | $0.2010$ |
| $2048$ | `minkowski_2d_slab` | $0.2025 \pm 0.0018$ | $0.000003$ | $3.15$ | $0.5155 \pm 0.0141$ | $0.4268$ | $0.3479$ | $0.7766$ | $0.2087$ |
| $2048$ | `cutoff_kmax2` | $0.0584 \pm 0.0033$ | $0.000011$ | $4.63$ | $0.5197 \pm 0.0399$ | $0.2655$ | $0.5241$ | $1.2953$ | $0.1254$ |
| $2048$ | `percolation_p008` | $0.9640 \pm 0.0008$ | $0.000001$ | $1.06$ | $0.4496 \pm 0.0172$ | $0.3393$ | $0.4086$ | $0.9744$ | $0.1544$ |
| $2048$ | `random_dag_sparse` | $0.0021 \pm 0.0001$ | $0.000000$ | $8.39$ | n/a | n/a | n/a | n/a | n/a |
| $4096$ | `log_quad_c02_q020` | $0.1186 \pm 0.0039$ | $0.000015$ | $3.80$ | $0.5033 \pm 0.0357$ | $0.2733$ | $0.5236$ | $1.2407$ | $0.1303$ |

#### Table 2.3: Fixed-Cardinality Window Profiles Across $m \in \{[6, 11], [12, 24], [25, 48], [49, 96]\}$
Comparing `log_quad_c02_q020` and `log_quad_c02_q010` against `minkowski_4d` across fixed-$m$ windows exposes two sharp structural contrasts: (i) in `minkowski_4d`, comparability remains flat near $f(4) = 0.10$ across every $m$-window ($0.1082, 0.0967, 0.1048, 0.1024$ at $N = 2048$) with link-dominated interiors ($\ell_{\rm link} \in [0.7543, 0.9232]$) and wide spatial entry cross-sections ($w_{\min}/m = 0.6717$ at $m \in [12, 24]$); (ii) in `log_quad_c02_q020`, small intervals $m \in [6, 11]$ are strongly spine-like and drift monotonically upward with $N$ ($0.7656 \to 0.8105 \to 0.8243$ from $N = 512$ to $2048$, and $0.8179$ at $N = 4096$), while `log_quad_c02_q010` exhibits monotonic fixed-$m \in [12, 24]$ drift ($0.4920 \to 0.5188 \to 0.5612$) as $\mathbb{E}[K_N]$ grows.

| Model | Horizon $N$ | Window $m$ | $\langle R_2(I)\rangle \pm \text{SD}$ | $d_{\rm MM}(I)$ | $\langle \ell_{\rm link}(I)\rangle$ | $\langle h(I)/m\rangle$ | $\langle \rho_2(I)\rangle$ | $\langle w_{\min}(I)/m\rangle$ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `log_quad_c02_q020` | $512$ | $[6, 11]$ | $0.7656 \pm 0.0342$ | $1.41$ | $0.3756$ | $0.7937$ | $0.7299$ | $0.1890$ |
| `log_quad_c02_q020` | $512$ | $[12, 24]$ | $0.4907 \pm 0.0417$ | $2.03$ | $0.2959$ | $0.5185$ | $1.1212$ | $0.1336$ |
| `log_quad_c02_q020` | $512$ | $[25, 48]$ | $0.3458 \pm 0.0255$ | $2.48$ | $0.2357$ | $0.3334$ | $1.5046$ | $0.0978$ |
| `log_quad_c02_q020` | $512$ | $[49, 96]$ | $0.2815 \pm 0.0449$ | $2.75$ | $0.1859$ | $0.2268$ | $1.9467$ | $0.0633$ |
| `log_quad_c02_q020` | $1024$ | $[6, 11]$ | $0.8105 \pm 0.0365$ | $1.33$ | $0.3539$ | $0.8327$ | $0.7748$ | $0.1802$ |
| `log_quad_c02_q020` | $1024$ | $[12, 24]$ | $0.5496 \pm 0.0617$ | $1.88$ | $0.2722$ | $0.5661$ | $1.2423$ | $0.1250$ |
| `log_quad_c02_q020` | $1024$ | $[25, 48]$ | $0.3631 \pm 0.0312$ | $2.42$ | $0.2127$ | $0.3649$ | $1.7657$ | $0.0920$ |
| `log_quad_c02_q020` | $1024$ | $[49, 96]$ | $0.2659 \pm 0.0102$ | $2.81$ | $0.1670$ | $0.2276$ | $2.2179$ | $0.0553$ |
| `log_quad_c02_q020` | $2048$ | $[6, 11]$ | $0.8243 \pm 0.0357$ | $1.30$ | $0.3421$ | $0.8568$ | $0.8415$ | $0.1746$ |
| `log_quad_c02_q020` | $2048$ | $[12, 24]$ | $0.4966 \pm 0.0257$ | $2.01$ | $0.2894$ | $0.5353$ | $1.1657$ | $0.1387$ |
| `log_quad_c02_q020` | $2048$ | $[25, 48]$ | $0.3223 \pm 0.0199$ | $2.57$ | $0.2213$ | $0.3212$ | $1.6197$ | $0.0902$ |
| `log_quad_c02_q020` | $2048$ | $[49, 96]$ | $0.2284 \pm 0.0275$ | $3.01$ | $0.1846$ | $0.2072$ | $1.9526$ | $0.0668$ |
| `log_quad_c02_q020` | $4096$ | $[6, 11]$ | $0.8179 \pm 0.0543$ | $1.31$ | $0.3395$ | $0.8414$ | $0.8278$ | $0.1727$ |
| `log_quad_c02_q020` | $4096$ | $[12, 24]$ | $0.5033 \pm 0.0357$ | $1.99$ | $0.2733$ | $0.5236$ | $1.2407$ | $0.1303$ |
| `log_quad_c02_q020` | $4096$ | $[25, 48]$ | $0.3314 \pm 0.0343$ | $2.54$ | $0.2222$ | $0.3334$ | $1.6163$ | $0.0927$ |
| `log_quad_c02_q020` | $4096$ | $[49, 96]$ | $0.2297 \pm 0.0255$ | $3.00$ | $0.1765$ | $0.2108$ | $2.1008$ | $0.0544$ |
| `log_quad_c02_q010` | $2048$ | $[6, 11]$ | $0.8538 \pm 0.0627$ | $1.25$ | $0.3374$ | $0.8760$ | $0.8472$ | $0.1697$ |
| `log_quad_c02_q010` | $2048$ | $[12, 24]$ | $0.5612 \pm 0.0431$ | $1.85$ | $0.2607$ | $0.5904$ | $1.3270$ | $0.1194$ |
| `log_quad_c02_q010` | $2048$ | $[25, 48]$ | $0.3639 \pm 0.0204$ | $2.42$ | $0.2123$ | $0.3645$ | $1.7171$ | $0.0809$ |
| `log_quad_c02_q010` | $2048$ | $[49, 96]$ | $0.2488 \pm 0.0004$ | $2.89$ | $0.1713$ | $0.2484$ | $2.2054$ | $0.0532$ |
| `minkowski_4d` | $2048$ | $[6, 11]$ | $0.1082 \pm 0.0140$ | $3.91$ | $0.8032$ | $0.2370$ | $0.0010$ | $0.7640$ |
| `minkowski_4d` | $2048$ | $[12, 24]$ | $0.0967 \pm 0.0023$ | $4.04$ | $0.9232$ | $0.1583$ | $0.0076$ | $0.6717$ |
| `minkowski_4d` | $2048$ | $[25, 48]$ | $0.1048 \pm 0.0062$ | $3.95$ | $0.8449$ | $0.1005$ | $0.0355$ | $0.5434$ |
| `minkowski_4d` | $2048$ | $[49, 96]$ | $0.1024 \pm 0.0057$ | $3.97$ | $0.7543$ | $0.0668$ | $0.1232$ | $0.4378$ |

*Note on $N = 2048$ `minkowski_4d` SDs*: exact run-level SDs in `nested_regime_experiment_results.json` at $N = 2048$ are $0.013961$ ($[6, 11]$), $0.002288$ ($[12, 24]$), $0.006156$ ($[25, 48]$), and $0.005689$ ($[49, 96]$).

#### Table 2.4: Horizon-Growing Window Profiles ($m \in [\lceil 0.5 N^\alpha\rceil, \lfloor 1.5 N^\alpha\rfloor]$, $\alpha \in \{0.35, 0.50, 0.65\}$)
When the interval window grows with the horizon as $m \propto N^\alpha$, `log_quad_c02_q020` shifts systematically toward lower $R_2(I)$ (higher effective $d_{\rm MM}$) as $N$ increases because larger $m$ dominates the slower logarithmic parent-seed drift ($d_{\rm MM}$ at $\alpha = 0.65$ progresses $2.58 \to 2.79 \to 3.21 \to 3.50$ across $N = 512 \to 4096$), whereas `minkowski_4d` remains scale-invariant near $d_{\rm MM} \approx 4.0$ across all $(\alpha, N)$.

| Model | Horizon $N$ | $\alpha = 0.35$ $\langle R_2(I)\rangle$ ($d_{\rm MM}$) | $\alpha = 0.50$ $\langle R_2(I)\rangle$ ($d_{\rm MM}$) | $\alpha = 0.65$ $\langle R_2(I)\rangle$ ($d_{\rm MM}$) | $\alpha = 0.65$ $\langle w_{\min}(I)/m\rangle$ |
|:---|:---:|:---:|:---:|:---:|:---:|
| `log_quad_c02_q020` | $512$ | $0.8099 \pm 0.0465$ ($1.33$) | $0.4813 \pm 0.0306$ ($2.05$) | $0.3199 \pm 0.0269$ ($2.58$) | $0.0833$ |
| `log_quad_c02_q020` | $1024$ | $0.7730 \pm 0.0442$ ($1.40$) | $0.4454 \pm 0.0433$ ($2.16$) | $0.2717 \pm 0.0093$ ($2.79$) | $0.0651$ |
| `log_quad_c02_q020` | $2048$ | $0.6151 \pm 0.0536$ ($1.72$) | $0.3330 \pm 0.0294$ ($2.53$) | $0.1932 \pm 0.0185$ ($3.21$) | $0.0531$ |
| `log_quad_c02_q020` | $4096$ | $0.5719 \pm 0.0627$ ($1.82$) | $0.2843 \pm 0.0223$ ($2.73$) | $0.1520 \pm 0.0177$ ($3.50$) | $0.0315$ |
| `minkowski_4d` | $512$ | $0.0899 \pm 0.0335$ ($4.19$) | $0.0715 \pm 0.0204$ ($4.43$) | $0.0759 \pm 0.0000$ ($4.33$) | $0.6333$ |
| `minkowski_4d` | $1024$ | $0.0889 \pm 0.0232$ ($4.17$) | $0.0878 \pm 0.0182$ ($4.17$) | $0.0947 \pm 0.0230$ ($4.10$) | $0.4663$ |
| `minkowski_4d` | $2048$ | $0.0908 \pm 0.0105$ ($4.12$) | $0.0999 \pm 0.0124$ ($4.01$) | $0.1053 \pm 0.0073$ ($3.94$) | $0.3714$ |

#### Table 2.5: Boundary-Trim Sensitivity Audit ($\delta_{\rm bulk} \in \{0.02, 0.05, 0.10\}$ at $N = 1024, m \in [12, 24]$)
Varying $\delta_{\rm bulk}$ over a $5\times$ range confirms that the five-observable separation between `log_quad_c02_q020` and `minkowski_4d` is an intrinsic bulk property rather than a boundary-trimming artifact:

| Model | $\delta_{\rm bulk}$ | Mean Bulk Candidates $\langle \lvert J_N\rvert \rangle$ | $\langle R_2(I)\rangle \pm \text{SD}$ | $\langle \ell_{\rm link}(I)\rangle$ | $\langle h(I)/m\rangle$ | $\langle \rho_2(I)\rangle$ | $\langle w_{\min}(I)/m\rangle$ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `log_quad_c02_q020` | $0.02$ | $1363.9$ | $0.5341 \pm 0.0386$ | $0.2704$ | $0.5593$ | $1.2765$ | $0.1317$ |
| `log_quad_c02_q020` | $0.05$ | $684.4$ | $0.5211 \pm 0.0329$ | $0.2782$ | $0.5543$ | $1.2381$ | $0.1275$ |
| `log_quad_c02_q020` | $0.10$ | $101.6$ | $0.5490 \pm 0.0803$ | $0.2783$ | $0.5752$ | $1.2331$ | $0.1291$ |
| `minkowski_4d` | $0.02$ | $698.0$ | $0.1006 \pm 0.0127$ | $0.8950$ | $0.1553$ | $0.0122$ | $0.6586$ |
| `minkowski_4d` | $0.05$ | $276.0$ | $0.0881 \pm 0.0088$ | $0.9000$ | $0.1489$ | $0.0017$ | $0.6769$ |
| `minkowski_4d` | $0.10$ | $53.1$ | $0.0908 \pm 0.0266$ | $0.9055$ | $0.1607$ | $0.0050$ | $0.6686$ |

### 2.4 Enforcement of Pre-Declared Holdout Decision Rule
Applying the pre-declared decision criteria (`decision_evaluation` in `nested_regime_experiment_results.json`):
- **Within-horizon $m$-scale crossover (`PASS`):** At $N = 2048$, `log_quad_c02_q020` achieves $\langle R_2(I)\rangle_{6\text{--}11} - \langle R_2(I)\rangle_{49\text{--}96} = 0.5959 > 0.40$.
- **Strict fixed-$m$ $N$-stationarity (`FAIL`):** At $m \in [6, 11]$, `log_quad_c02_q020` drifts upward at $+0.0293$ per octave across $N = 512 \to 2048$ (exceeding $\pm 0.012$/octave), while exact global $\mathbb{E}[R_2(P_N)]$ drifts monotonically $0.1052 \to 0.1091 \to 0.1138 \to 0.1185$ to $N = 4096$ by Proposition 2.1.
- **4D transverse hypersurface width (`FAIL`):** At $N = 2048, m \in [12, 24]$, `log_quad_c02_q020` yields $\langle w_{\min}(I)/m\rangle = 0.1387 < 0.40$ (vs. $0.6717$ in `minkowski_4d`), confirming narrow multi-parent spine structure at mesoscopic scales.
- **Formal Disposition:** `RETIRE_STATIC_SCALAR_STANDALONE_GEOMETRY_RETAIN_AS_BASELINE_KERNEL`. Uncoupled static scalar Log-Quadratic CSG is retired as a standalone stationary all-horizon geometry law and retained strictly as a well-controlled, diamond-covariant baseline kernel $q_{\rm LQ}$ for coupled $X = (C, \mathcal{Z})$ dynamics in Pillars 2 and 3.

---

## 3. Pillar 2: Dynamical Nested-Regime Projection & Live Residual-to-Structure Coupling on $X = (C, \mathcal{Z})$

### 3.1 Coarse-Graining & Omitted Micro-Interval Memory Theorem (`[PROVED THEOREM]`)
In `docs/track_b/RECORD_PROCESS_CONTRACT.md`, a process state is $X = (C, \mathcal{Z})$ where $C = (V, \prec, r)$ is an immutable committed snapshot with mark map $r: V \to \mathcal{A}_{\rm mark}$ and $\mathcal{Z}$ is the live residual state. For an isomorphism-covariant anchor subset $V_{\mathcal{A}} \subseteq V$, define the **intrinsic anchor projection** (corresponding to `access_records` on $V_{\mathcal{A}}$ together with coarse residual summary $\widetilde{\mathcal{Z}}$):
$$
\Pi_{\mathcal{A}}(C, \mathcal{Z}) := (\widetilde{C}, \widetilde{\mathcal{Z}}), \qquad \widetilde{C} := \bigl(V_{\mathcal{A}},\, \prec\rvert_{V_{\mathcal{A}}},\, r\rvert_{V_{\mathcal{A}}}\bigr).
$$

**Theorem 3.1 (`[PROVED THEOREM]` Diamond Compatibility, Omitted-Chain Non-Markovianity, and Shadow-Volume Sufficiency).**  
*Let $(C_n)_{n \ge 0}$ evolve by sequential maximal births under any subset-weight CSG kernel $(t_k)_{k \ge 0}$ with $t_0 = 1$ and $t_1 = c > 0$.*
1. *(Diamond Compatibility): If newborn anchor membership $\mathbf{1}_{\{x \in V_{\mathcal{A}}\}} = \chi_{\mathcal{A}}(S, r\rvert_S, r(x))$ depends strictly on the intrinsic strict causal past $(S, r\rvert_S)$ and newborn mark $r(x)$, then $\Pi_{\mathcal{A}}$ commutes up to canonical vertex transport across every incomparable-birth diamond: $\Pi_{\mathcal{A}}((C + x_{S, b}) + y_{T, c}) \cong \Pi_{\mathcal{A}}((C + y_{T, c}) + x_{S, b})$.*
2. *(Omitted Micro-Interval Non-Markovianity): The projected coarse order $\widetilde{C}_n = \Pi_{\mathcal{A}}(C_n)$ alone is **non-Markovian**. Specifically, for $m \ge 0$, let $C^{(m)} = \{u \prec z_1 \prec \dots \prec z_m \prec v\}$ have anchors $V_{\mathcal{A}} = \{u, v\}$ and $m$ omitted micro-events $z_1, \dots, z_m \notin V_{\mathcal{A}}$. Every $C^{(m)}$ projects to the identical coarse 2-chain $\Pi_{\mathcal{A}}(C^{(m)}) = \{u \prec v\}$, yet for a newborn anchor $w$ the exact ratio of coarse branching from $u$ incomparably to $v$ ($S \cap V_{\mathcal{A}} = \{u\}$) versus disconnected birth ($S \cap V_{\mathcal{A}} = \varnothing$) is*
   $$
   \mathcal{R}_{\rm branch}(m) := \frac{\mathbb{P}(S \cap V_{\mathcal{A}} = \{u\} \mid C^{(m)})}{\mathbb{P}(S \cap V_{\mathcal{A}} = \varnothing \mid C^{(m)})} = \sum_{r=0}^{m} G(1 + r, 1) = Z_{m+1} - 1 = (1 + m)c + \sum_{k=2}^{m+1} \binom{m+1}{k} t_k,
   $$
   *which equals $(1 + m)c$ when $t_{\ge 2} = 0$ ($k_{\max} = 1$) and is strictly increasing in $m$ for every CSG law with $c > 0$ (while the maximal micro-ideal $S_{\max} = \{u, z_1, \dots, z_m\}$ alone carries weight ratio $G(1 + m, 1) = \sum_{j=0}^m \binom{m}{j} t_{1+j}$).*
3. *(Exact Markov Closure via Shadow-Volume Residual $\widetilde{\mathcal{Z}}_{\rm geom}$): For each $y \in V$, let $\pi_{\mathcal{A}}^-(y) := J^-_C[y] \cap V_{\mathcal{A}} \in \mathcal{I}(\widetilde{C})$ be its anchor past-shadow, and define the shadow-volume multiplicity vector $\widetilde{\mathcal{Z}}_{\rm geom}(C) := (\nu_C(I))_{I \in \mathcal{I}(\widetilde{C})}$ where $\nu_C(I) := \lvert\{y \in V : \pi_{\mathcal{A}}^-(y) = I\}\rvert$. Under independent (or coarse-shadow-dependent) newborn anchor marking, $(\widetilde{C}_n, \widetilde{\mathcal{Z}}_{\rm geom}(C_n))$ is an **exact autonomous Markov process** whose coarse ideal law satisfies $\mathbb{P}(S_n \cap V_{\mathcal{A}} \subseteq \widetilde{U} \mid C_n) = Z_{N_{\le}(\widetilde{U})} / Z_n$ with $N_{\le}(\widetilde{U}) = \sum_{I \subseteq \widetilde{U}} \nu_{C_n}(I)$ and $n = \sum_I \nu_{C_n}(I)$.*

*Proof.*  
**(1)** Across an incomparable diamond $(S, T)$ over $C$, $x \notin T$ and $y \notin S$ ($x \parallel y$). Hence the induced subposet $(S, \prec\rvert_S, r\rvert_S)$ inside $C + y_{T, c}$ is identical to that inside $C$, and $(T, \prec\rvert_T, r\rvert_T)$ inside $C + x_{S, b}$ is identical to that inside $C$. Thus $\chi_{\mathcal{A}}$ assigns identical anchor flags to $x$ and $y$ on both paths, and restricting the canonically isomorphic marked endpoints $(C + x_{S, b}) + y_{T, c} \cong (C + y_{T, c}) + x_{S, b}$ to $V_{\mathcal{A}}$ preserves isomorphism identically.  
**(2)** In the $(m+2)$-chain $C^{(m)} = \{u \prec z_1 \prec \dots \prec z_m \prec v\}$ with $V_{\mathcal{A}} = \{u, v\}$, $u$ is the unique minimal element and $v$ is the unique maximal element. For a Rideout–Sorkin parent subset $B \subseteq V(C^{(m)})$, $S = J^-[B]$ satisfies $S \cap \{u, v\} = \varnothing \iff u \notin S \iff B = \varnothing$, which has probability $1 / Z_{m+2}$. Similarly, $S \cap \{u, v\} = \{u\} \iff u \in S \text{ and } v \notin S \iff \varnothing \ne B \subseteq \{u, z_1, \dots, z_m\}$, which sums over the $(m+1)$-element set $\{u, z_1, \dots, z_m\}$ to $\frac{1}{Z_{m+2}}\sum_{k=1}^{m+1}\binom{m+1}{k} t_k = \frac{Z_{m+1} - 1}{Z_{m+2}}$. Taking the ratio gives $\mathcal{R}_{\rm branch}(m) = Z_{m+1} - 1 = \sum_{r=0}^m G(1 + r, 1)$, strictly increasing in $m$ since $t_1 = c > 0$ and $t_k \ge 0$.  
**(3)** Because intersection distributes over union, for every parent subset $B \subseteq V$,
$$
J^-_C[B] \cap V_{\mathcal{A}} = \left(\bigcup_{b \in B} J^-_C[b]\right) \cap V_{\mathcal{A}} = \bigcup_{b \in B} \pi_{\mathcal{A}}^-(b).
$$
Therefore $\bigcup_{b \in B_n} \pi_{\mathcal{A}}^-(b) \subseteq \widetilde{U}$ holds if and only if every $b \in B_n$ lies in $\{y \in V : \pi_{\mathcal{A}}^-(y) \subseteq \widetilde{U}\}$, a set of cardinality $N_{\le}(\widetilde{U}) = \sum_{I \subseteq \widetilde{U}} \nu_C(I)$, which occurs with exact probability $Z_{N_{\le}(\widetilde{U})} / Z_n$. By Möbius inversion on the finite lattice $\mathcal{I}(\widetilde{C})$, the exact distribution of $\widetilde{S}_n := S_n \cap V_{\mathcal{A}}$ is uniquely determined by $(\widetilde{C}, \widetilde{\mathcal{Z}}_{\rm geom}(C))$. Moreover, adjoining maximal $x_n$ never alters $\pi_{\mathcal{A}}^-(y)$ for existing $y \in V$: if $x_n \notin V_{\mathcal{A}}$ (an omitted micro-birth, acting as a silent coarse residual update `evolve_residual`), $\widetilde{C}$ is unchanged and $\nu(\widetilde{S}_n) \mapsto \nu(\widetilde{S}_n) + 1$; if $x_n \in V_{\mathcal{A}}$ (`commit_record` on the coarse regime), $\widetilde{C} \mapsto \widetilde{C} + x_n$ above $\widetilde{S}_n$ with $\nu(\widetilde{S}_n \cup \{x_n\}) = 1$. Hence $(\widetilde{C}_n, \widetilde{\mathcal{Z}}_{\rm geom}(C_n))$ is closed and Markovian. $\blacksquare$

#### Table 3.1: Numerical Verification of Theorem 3.1 (`pillar2_coarse_projection`)
Exhaustive audit across all $3,644$ diamonds ($1 \le \lvert C\rvert \le 4$) confirms $0$ diamond violations for intrinsic past-nonempty anchor projection vs. $3,644$ violations for extrinsic stage-parity projection. Across all marked posets up to $N = 4$ ($126$ $(\widetilde{C}, \widetilde{\mathcal{Z}}_{\rm geom})$ classes, $56$ multi-member classes), maximum coarse transition discrepancy within identical $(\widetilde{C}, \widetilde{\mathcal{Z}}_{\rm geom})$ is $1.11 \times 10^{-16}$, whereas matching $\widetilde{C}$ alone produces a non-Markovian probability gap of $0.2923$. Exact omitted-chain ratios ($c = 0.20, q = 0.20$, formula error $2.22 \times 10^{-16}$):

| Omitted Micro-Events $m$ | $k_{\max} = 1$ $\mathcal{R}_{\rm branch}(m)$ | $k_{\max} = 1$ Analytic $(1 + m)c$ | Log-Quad $\mathcal{R}_{\rm branch}(m)$ | Log-Quad Analytic $Z_{m+1} - 1$ | Maximal Micro-Ideal $G(1 + m, 1)$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| $0$ | $0.200000$ | $0.200000$ | $0.200000$ | $0.200000$ | $0.200000$ |
| $1$ | $0.400000$ | $0.400000$ | $0.408000$ | $0.408000$ | $0.208000$ |
| $2$ | $0.600000$ | $0.600000$ | $0.624064$ | $0.624064$ | $0.216064$ |
| $3$ | $0.800000$ | $0.800000$ | $0.848256$ | $0.848256$ | $0.224192$ |
| $4$ | $1.000000$ | $1.000000$ | $1.080641$ | $1.080641$ | $0.232384$ |

### 3.2 Theorem 2A: Arbitrary-Horizon Active Off-Diagonal Residual Law via Root Martingale $\mathcal{M}_{\rm root}$ (`[PROVED THEOREM]`)
The reviewed `NM004` construction (`docs/track_b/native_active_residual_v1.md`) proved an active $2 \times 2$ residual-to-structure law through $N = 4$ births using an antichain indicator potential that vanishes on non-antichain parents. We now prove a general arbitrary-horizon construction valid for **every** subset-weight CSG kernel and **every** finite horizon $N_{\rm act} \ge 2$, active on **all** parent posets (antichain and non-antichain alike).

**Theorem 3.2 (`[PROVED THEOREM]` Arbitrary-Horizon Active Residual-to-Structure Law via $\mathcal{M}_{\rm root}$).**  
*Let $q(P_n, S)$ be any subset-weight CSG kernel with couplings $(t_k)_{k \ge 0}$ ($t_0 = 1, t_1 = c > 0$) and partition sequence $Z_n = \sum_{k=0}^n \binom{n}{k} t_k$ ($Z_0 = 1$). Let $M_0(P_n) := \lvert\operatorname{Min}(P_n)\rvert$ ($M_0(\varnothing) := 0$).*
1. *(Exact Poset Root Martingale): For every $n \ge 0$ and every poset $P_n$ of size $n$, $\sum_{S \in \mathcal{I}(P_n)} q(P_n, S) M_0(P_n + x_S) = M_0(P_n) + \frac{1}{Z_n}$. Hence $\mathcal{M}_{\rm root}(P_n) := M_0(P_n) - \sum_{j=0}^{n-1} \frac{1}{Z_j}$ is an exact birth-order-independent poset martingale for all $n \ge 0$.*
2. *(Positivity, Row Normalization, and Full $2 \times 2$ Matrix Diamond Commutation): Fix any declared horizon $N_{\rm act} \ge 2$, retention parameter $t \in (0, 1)$, and coupling $\theta \in \bigl(0,\, \frac{1 - t}{2} t^{N_{\rm act} - 1}\bigr)$. For $0 \le n < N_{\rm act}$ and $S \in \mathcal{I}(P_n)$, define*
   $$
   r_{P_n}(S) := \theta t^{-n}\!\left(\mathbf{1}_{\{S = \varnothing\}} - \frac{1}{Z_n}\right), \qquad A_{P_n, S} := q(P_n, S)\, M_t(r_{P_n}(S)), \qquad M_t(r) := \frac{1}{2}\begin{bmatrix} 1 + r + t & 1 - r - t \\ 1 + r - t & 1 - r + t \end{bmatrix}.
   $$
   *Then at every $0 \le n < N_{\rm act}$: (i) $M_t(r_{P_n}(S)) > 0$ and the column-stochastic factor $T_{P_n, S} := M_t(r_{P_n}(S))\operatorname{diag}(1 + r_{P_n}(S), 1 - r_{P_n}(S))^{-1} > 0$ are strictly entrywise positive for all $S \in \mathcal{I}(P_n)$, so $A_{P_n, S} = q(P_n, S) T_{P_n, S}\operatorname{diag}(1 + r_{P_n}(S), 1 - r_{P_n}(S))$ is strictly entrywise positive ($A_{P_n, S} > 0$) on every **supported** ideal $q(P_n, S) > 0$ (which includes $S = \varnothing$ and all principal ideals $J^-[u]$ whenever $c > 0$, and equals all of $\mathcal{I}(P_n)$ whenever $t_k > 0$ for all $k \ge 1$); (ii) $\sum_{S \in \mathcal{I}(P_n)} A_{P_n, S} = M_t(0)$ and $\sum_{S \in \mathcal{I}(P_n)} \mathbf{1}^T A_{P_n, S} = \mathbf{1}^T$; (iii) the uniform state $u = (\frac{1}{2}, \frac{1}{2})^T$ satisfies $A_{P_n, S} u = q(P_n, S) u$; and (iv) in the basis $W = [u\;\; v]$ with $v = (\frac{1}{2}, -\frac{1}{2})^T$, any $m$-birth trajectory $C = P_{n_0} \to \dots \to P_{n_0 + m} = E$ ($n_0 + m \le N_{\rm act}$) telescopes identically as*
   $$
   W^{-1} M_t(r_{m-1})\cdots M_t(r_0) W = \begin{bmatrix} 1 & \theta t^{-n_0}\bigl[\mathcal{M}_{\rm root}(E) - \mathcal{M}_{\rm root}(C)\bigr] \\ 0 & t^m \end{bmatrix},
   $$
   *establishing exact $2 \times 2$ matrix diamond commutation $A_{C + x_S, T} A_{C, S} = A_{C + y_T, S} A_{C, T}$ across $100\%$ of incomparable-birth diamonds.*
3. *(Nonzero Active Update Contrast): At $n = 0$ ($P_0 = \varnothing$), $Z_0 = 1 \implies r_\varnothing(\varnothing) = 0$, so $K := T_{\varnothing, \varnothing} = M_t(0)$ actively mixes $\delta_0 = (1, 0)^T$ to $K\delta_0 = (\frac{1+t}{2}, \frac{1-t}{2})^T$. At every step $1 \le n < N_{\rm act}$ and every supported ideal $S \in \mathcal{I}(P_n)$ with $q(P_n, S) > 0$, $p_{P_n, S}(\rho) := \mathbf{1}^T A_{P_n, S} \rho$ satisfies*
   $$
   \Delta_{\rm update} := p_{P_n, S}(K\delta_0) - p_{P_n, S}(\delta_0) = -\frac{1 - t}{2}\,\Delta_{\rm current} \ne 0, \qquad \Delta_{\rm current} := p_{P_n, S}(\delta_0) - p_{P_n, S}(\delta_1),
   $$
   *whereas every diagonal static-seed control ($T = I$) and every uncoupled forward-only control ($r \equiv 0$) yields $\Delta_{\rm update} \equiv 0$.*

*Proof.*  
**(1)** Adjoining a maximal vertex $x_S$ never adds predecessors to existing vertices $y \in P_n$, while $x_S$ itself is minimal in $P_n + x_S$ iff $S = \varnothing$. Thus $M_0(P_n + x_S) = M_0(P_n) + \mathbf{1}_{\{S = \varnothing\}}$. Since $q(P_n, \varnothing) = t_0 / Z_n = 1 / Z_n$ for every poset $P_n$ of size $n$, taking the $q(P_n, \cdot)$-expectation adds $1/Z_n$, proving $\sum_S q(P_n, S)\mathcal{M}_{\rm root}(P_n + x_S) = \mathcal{M}_{\rm root}(P_n)$ and $\mathcal{M}_{\rm root}(P_n + x_S) - \mathcal{M}_{\rm root}(P_n) = \mathbf{1}_{\{S = \varnothing\}} - \frac{1}{Z_n}$.  
**(2)** Since $\frac{1}{Z_n} \in (0, 1]$, $\lvert \mathbf{1}_{\{S = \varnothing\}} - \frac{1}{Z_n}\rvert < 1$ for $n \ge 1$ and $= 0$ at $n = 0$. For $0 \le n \le N_{\rm act} - 1$, $\lvert r_{P_n}(S)\rvert \le \theta t^{-(N_{\rm act}-1)} < \frac{1 - t}{2}$, so every entry of $M_t(r)$ exceeds $\min\bigl(\frac{1 + 3t}{4}, \frac{1 - t}{4}\bigr) > 0$ and its column sums $1 \pm r$ are strictly positive (making $A_{P_n, S} > 0$ whenever $q(P_n, S) > 0$, and for all $S \in \mathcal{I}(P_n)$ when $t_k > 0$ for all $k \ge 1$ since $G(\lvert S\rvert, \lvert\operatorname{Max}(S)\rvert) \ge t_{\lvert S\rvert} > 0$). Because $\sum_S q(P_n, S) r_{P_n}(S) = 0$ and $M_t(r)$ is affine in $r$, $\sum_S A_{P_n, S} = M_t(0)$ and $\mathbf{1}^T M_t(0) = \mathbf{1}^T$. Direct multiplication gives $M_t(r) u = u$ and $M_t(r) v = r u + t v$, so $W^{-1} M_t(r) W = \begin{bmatrix} 1 & r \\ 0 & t \end{bmatrix}$. Multiplying chronologically yields upper-right entry $\sum_{j=0}^{m-1} t^j r_j = \sum_{j=0}^{m-1} t^j \theta t^{-(n_0+j)}[\mathcal{M}_{\rm root}(P_{n_0+j+1}) - \mathcal{M}_{\rm root}(P_{n_0+j})] = \theta t^{-n_0}[\mathcal{M}_{\rm root}(E) - \mathcal{M}_{\rm root}(C)]$. Since $\mathcal{M}_{\rm root}(E)$ depends only on the unlabeled endpoint $E = C + x_S + y_T$ and scalar $q$ satisfies diamond commutation, $A_{C + x_S, T} A_{C, S} = A_{C + y_T, S} A_{C, T}$ holds identically as full $2 \times 2$ matrices.  
**(3)** At $P_0 = \varnothing$, $Z_0 = 1 \implies r_\varnothing(\varnothing) = 0$, giving $K = M_t(0)$ and $(K\delta_0)_0 - (K\delta_0)_1 = t$. For $1 \le n < N_{\rm act}$, $Z_n \ge 1 + n c > 1 \implies r_{P_n}(S) \ne 0$ for every $S \in \mathcal{I}(P_n)$, so $d_{P_n}(S) := q(P_n, S) r_{P_n}(S) \ne 0$ for every supported ideal $S \in \mathcal{I}(P_n)$ ($q(P_n, S) > 0$). Since $p_{P_n, S}(\rho) = q(P_n, S) + d_{P_n}(S)(\rho_0 - \rho_1)$, we have $\Delta_{\rm current} = 2 d_{P_n}(S) \ne 0$ and $\Delta_{\rm update} = d_{P_n}(S)(t - 1) = -\frac{1 - t}{2}\Delta_{\rm current} \ne 0$ on every supported ideal. $\blacksquare$

#### Table 3.2: Exhaustive Verification of Theorem 3.2 at $N_{\rm act} = 8$ and $N_{\rm act} = 12$ (`pillar2_active_root_martingale`)
Audited on `log_quad_c02_q020` with $t = 0.75$ and $\theta = \frac{1 - t}{4} t^{N_{\rm act} - 1}$ across all posets up to $N = 5$ and all $3,644$ diamonds ($1 \le \lvert C\rvert \le 4$, endpoints up to size $6$), plus $25$ full-horizon multi-step trajectories and high-$n$ diamonds up to $N_{\rm act}$:

| Metric / Invariant | $N_{\rm act} = 8$ | $N_{\rm act} = 12$ |
|:---|:---:|:---:|
| Retention $t$ / Coupling $\theta$ | $0.75$ / $0.00834274$ | $0.75$ / $0.00263970$ |
| Minimum branch matrix entry ($0 \le n \le 5$) | $1.836 \times 10^{-12} > 0$ | $1.927 \times 10^{-12} > 0$ |
| Max row-normalization error $\lVert \sum_S \mathbf{1}^T A_{P, S} - \mathbf{1}^T\rVert_\infty$ | $1.33 \times 10^{-15}$ | $5.55 \times 10^{-16}$ |
| Max uniform-anchor error $\lVert A_{P, S} u - q(P, S) u\rVert_\infty$ | $5.55 \times 10^{-17}$ | $1.39 \times 10^{-17}$ |
| Max root-martingale error $\lvert \sum_S q \mathcal{M}_{\rm root}(P + x_S) - \mathcal{M}_{\rm root}(P)\rvert$ | $1.78 \times 10^{-15}$ | $1.78 \times 10^{-15}$ |
| Exhaustive $2 \times 2$ matrix diamond violations ($1 \le \lvert C\rvert \le 4$) | $0 / 3,644$ (max err $1.39 \times 10^{-17}$) | $0 / 3,644$ (max err $1.39 \times 10^{-17}$) |
| Sampled high-$n$ diamond violations ($n = N_{\rm act} - 2$) | $0 / 25$ | $0 / 25$ |
| Max trajectory telescoping error ($m = N_{\rm act}$) | $3.33 \times 10^{-16}$ | $4.44 \times 10^{-16}$ |
| Step-1 chain contrast $\Delta_{\rm current}$ / $\Delta_{\rm update}$ | $-3.089905 \times 10^{-3}$ / $+3.862381 \times 10^{-4}$ | $-9.776652 \times 10^{-4}$ / $+1.222081 \times 10^{-4}$ |
| Ratio $\Delta_{\rm update} / \Delta_{\rm current}$ (analytic $-\frac{1 - t}{2} = -0.125$) | $-0.125000000000$ | $-0.125000000000$ |
| Static-seed ($T = I$) & Forward-only ($r = 0$) control $\Delta_{\rm update}$ | $0.0$ / $0.0$ | $0.0$ / $0.0$ |

### 3.3 Theorem 2B: All-Horizon Present-State Source Perturbation Law & Non-Mixture Separation (`[PROVED THEOREM]`)
To couple present-state residual interventions to causal growth across **unbounded** horizons $0 \le n < \infty$ without exponential $\theta$-attenuation, let $\mathcal{Z}_n \in \mathcal{D}(\mathbb{C}^2)$ and define the two-mode Log-Quadratic Kraus instrument with ground mode $q^{(0)} = q_{\rm LQ}(c_0, q_0) = q_{\rm LQ}(0.20, 0.20)$, excited source mode $q^{(1)} = q_{\rm LQ}(c_1, q_1) = q_{\rm LQ}(0.50, 0.35)$, and intrinsic size-plus-edge potential $\Phi(C) := \lvert C\rvert + C_1(C)$ ($\Delta \Phi(C_n, S) := \Phi(C_n + x_S) - \Phi(C_n) = 1 + \lvert S\rvert$):
$$
K_{C_n, S} := \sqrt{q^{(0)}(C_n, S)}\,e^{-i\omega_0(1 + \lvert S\rvert)}\lvert 0\rangle\langle 0\rvert + \sqrt{q^{(1)}(C_n, S)}\,e^{-i\omega_1(1 + \lvert S\rvert)}\lvert 1\rangle\langle 1\rvert, \qquad \mathcal{J}_{C_n, S}(\mathcal{Z}) := K_{C_n, S}\mathcal{Z}K_{C_n, S}^\dagger.
$$
At a committed prefix $C_{n_0}$, the `RECORD_PROCESS_CONTRACT` operation `evolve_residual` applies a unitary source excitation $\mathcal{U}_{\vartheta}(\mathcal{Z}) = U_\vartheta \mathcal{Z} U_\vartheta^\dagger$ ($U_\vartheta\lvert 0\rangle = \cos(\vartheta/2)\lvert 0\rangle + \sin(\vartheta/2)\lvert 1\rangle$) while leaving $C_{n_0}$ **identically unchanged**.

**Theorem 3.3 (`[PROVED THEOREM]` All-Horizon CPTP Covariance & Universal Static-Mixture Obstruction).**  
1. *(All-Horizon CPTP Projectivity & Operator Diamonds): For every $n \ge 0$ and every finite poset $C_n$, $\sum_{S \in \mathcal{I}(C_n)} K_{C_n, S}^\dagger K_{C_n, S} = I_2$ (exact trace preservation and Kolmogorov projectivity across all $N \ge 1$ to $\infty$), and across every incomparable-birth diamond $(S, T)$ within any growth epoch, $K_{C + x_S, T} K_{C, S} = K_{C + y_T, S} K_{C, T}$ identically.*
2. *(Untouched-Run Caveat vs. Same-Prefix Intervention Separation): An untouched run from $n = 0$ without `evolve_residual` reduces on order marginals to the static two-point mixture $\langle 0\rvert\mathcal{Z}_0\lvert 0\rangle \mathbb{P}^{(0)} + \langle 1\rvert\mathcal{Z}_0\lvert 1\rangle \mathbb{P}^{(1)}$ (`PW6A` Theorem 4.2). By contrast, starting from $\mathcal{Z}_0 = \lvert 0\rangle\langle 0\rvert$, applying $\mathcal{U}_{\rm id}$ ($\vartheta = 0$) vs. $\mathcal{U}_X$ ($\vartheta = \pi$) at the **same** committed snapshot $C_{n_0}$ ($n_0 \ge 1$) produces distinct conditional future laws ($\mathbb{P}(S_{n_0} = \varnothing \mid C_{n_0}, \mathcal{U}_{\rm id}) = 1/Z_{n_0}^{(0)} \ne 1/Z_{n_0}^{(1)} = \mathbb{P}(S_{n_0} = \varnothing \mid C_{n_0}, \mathcal{U}_X)$), impossible for any passive latent-seed model conditioned on $C_{n_0}$ alone.*
3. *(Single-Intervened Joint Law Violates Every Time-Homogeneous Static CSG Mixture): Fix any $n_0 \ge 2$ and consider the two **unlabeled isomorphism-invariant** events on the `(prefix, terminal)` pair $([C_{n_0}], [C_{n_0+1}])$:*
   $$
   \mathcal{E}_{\rm pre}(n_0) := \bigl\{ [C_{n_0}] = K_2 \sqcup A_{n_0 - 2},\; [C_{n_0 + 1}] = K_2 \sqcup A_{n_0 - 1} \bigr\}, \qquad \mathcal{E}_{\rm post}(n_0) := \bigl\{ [C_{n_0}] = A_{n_0},\; [C_{n_0 + 1}] = K_2 \sqcup A_{n_0 - 1} \bigr\},
   $$
   *where $K_2 \sqcup A_k$ is the unique unlabeled $(k+2)$-poset with $C_1 = 1$. For **every** probability measure $\mu$ on $[0, \infty)^\infty$ mixing time-homogeneous subset-weight CSG laws $\mathbb{P}_\mu = \int_{[0, \infty)^\infty} \mathbb{P}_{\mathbf{t}}\,d\mu(\mathbf{t})$ (whenever $\mathbb{P}_\mu(\mathcal{E}_{\rm pre}(n_0)) > 0$):*
   $$
   \frac{\mathbb{P}_\mu\bigl(\mathcal{E}_{\rm post}(n_0)\bigr)}{\mathbb{P}_\mu\bigl(\mathcal{E}_{\rm pre}(n_0)\bigr)} = \frac{2}{n_0 - 1},
   $$
   *whereas the single intervened law ($q^{(0)}$ for $n < n_0$, $\mathcal{U}_X$ at $n_0$, $q^{(1)}$ for $n \ge n_0$) yields*
   $$
   \frac{\mathbb{P}_{\rm int}\bigl(\mathcal{E}_{\rm post}(n_0)\bigr)}{\mathbb{P}_{\rm int}\bigl(\mathcal{E}_{\rm pre}(n_0)\bigr)} = \frac{2}{n_0 - 1}\,\frac{c_1}{c_0} \ne \frac{2}{n_0 - 1} \qquad (c_1 \ne c_0).
   $$

*Proof.*  
**(1)–(2)** Since $\sum_{S \in \mathcal{I}(C_n)} q^{(\ell)}(C_n, S) = 1$ ($\ell \in \{0, 1\}$), $\sum_S K_{C_n, S}^\dagger K_{C_n, S} = I_2$. Across any diamond $(S, T)$ over $C$, $\Delta\Phi(C, S) + \Delta\Phi(C + x_S, T) = 2 + \lvert S\rvert + \lvert T\rvert$ is symmetric in $(S, T)$, and each $q^{(\ell)}$ satisfies scalar diamond commutation, so $K_{C+x_S, T} K_{C, S} = K_{C+y_T, S} K_{C, T}$. At $C_{n_0}$, $c_0 = 0.20 < 0.50 = c_1$ and $q_0 = 0.20 < 0.35 = q_1$ imply $Z_{n_0}^{(0)} < Z_{n_0}^{(1)}$ for every $n_0 \ge 1$ (at $n_0 = 128$: $1/Z_{128}^{(0)} = 0.008728$ vs. $1/Z_{128}^{(1)} = 0.000246$).  
**(3)** Under any CSG law $\mathbb{P}_{\mathbf{t}}$ ($\mathbf{t} = (t_1, t_2, \dots) \in [0, \infty)^\infty$), $[C_{n_0}] = K_2 \sqcup A_{n_0 - 2}$ occurs iff exactly one step $m \in \{1, \dots, n_0 - 1\}$ draws a singleton subset $\lvert B_m\rvert = 1$ ($m$ choices) and all other steps draw $B_j = \varnothing$, summing to $\sum_{m=1}^{n_0-1} m = \binom{n_0}{2}$ trajectories each of probability $t_1 / \prod_{j=1}^{n_0-1} Z_j(\mathbf{t})$. Appending $B_{n_0} = \varnothing$ (probability $1/Z_{n_0}(\mathbf{t})$) gives $\mathbb{P}_{\mathbf{t}}(\mathcal{E}_{\rm pre}(n_0)) = \binom{n_0}{2} t_1 / \prod_{j=1}^{n_0} Z_j(\mathbf{t})$—completely independent of $t_2, t_3, \dots$ except through the shared denominator! Similarly, $\mathcal{E}_{\rm post}(n_0)$ requires $B_1 = \dots = B_{n_0-1} = \varnothing$ followed by $\lvert B_{n_0}\rvert = 1$ ($n_0$ choices), giving $\mathbb{P}_{\mathbf{t}}(\mathcal{E}_{\rm post}(n_0)) = n_0 t_1 / \prod_{j=1}^{n_0} Z_j(\mathbf{t}) = \frac{2}{n_0 - 1}\mathbb{P}_{\mathbf{t}}(\mathcal{E}_{\rm pre}(n_0))$ pointwise for **every** $\mathbf{t} \in [0, \infty)^\infty$. Integrating over any measure $\mu$ preserves $\mathbb{P}_\mu(\mathcal{E}_{\rm post}(n_0)) - \frac{2}{n_0 - 1}\mathbb{P}_\mu(\mathcal{E}_{\rm pre}(n_0)) = 0$. Under $\mathcal{U}_X$ at $n_0$, pre-$n_0$ singleton births carry factor $c_0$ while post-$n_0$ singleton births carry factor $c_1$, multiplying the ratio by $c_1/c_0 = 0.50/0.20 = 2.5$. $\blacksquare$

#### Table 3.3: Exact Trajectory-Enumeration Verification of Theorem 3.3 (`pillar2_two_mode_non_mixture`)
Across all $3,644$ diamonds ($1 \le \lvert C\rvert \le 4$, $\omega_0 = 0.25, \omega_1 = 0.85$), maximum CPTP trace error is $2.23 \times 10^{-16}$ and complex operator diamond violations equal $0 / 3,644$ (max error $1.24 \times 10^{-16}$). Full trajectory enumeration confirms the universal static-mixture obstruction:

| Intervention Epoch $n_0$ (Terminal $N = n_0 + 1$) | Total Intervened Mass | Universal Static-Mixture Ratio $\frac{2}{n_0 - 1}$ | Arbitrary 3-Component CSG Mixture Check | Intervened $\mathcal{U}_X$ Ratio | Analytic Intervened $\frac{5}{n_0 - 1}$ | Non-Mixture Discrepancy |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $n_0 = 2$ ($N = 3$) | $1.000000$ | $2.0000$ | $2.0000$ | $5.0000$ | $5.0000$ | $+3.0000$ |
| $n_0 = 3$ ($N = 4$) | $1.000000$ | $1.0000$ | $1.0000$ | $2.5000$ | $2.5000$ | $+1.5000$ |
| $n_0 = 4$ ($N = 5$) | $1.000000$ | $0.6667$ | $0.6667$ | $1.6667$ | $1.6667$ | $+1.0000$ |

---

## 4. Pillar 3: Paired Source-Perturbation to Clock-Tick & Nested-Interval Focusing Bridge

### 4.1 Three-Arm Paired Experimental Design ($n_0 = 128 \to N \in \{512, 1024\}$, $M = 40$)
To test a concrete native source-to-readout bridge in strict compliance with `docs/coordination/NATIVE_MASS_MAPPING.md` (requiring matched preparations, explicit forward-only controls, pre-declared readouts, and retained source recoil accounting), we generate $M = 40$ baseline committed prefixes $C_{n_0}$ at $n_0 = 128$ (`seed = 20260803`) under ground mode $q^{(0)} = q_{\rm LQ}(0.20, 0.20)$ with $\mathcal{Z}_{n_0} = \mathcal{Z}_{\rm ref} = \lvert 0\rangle\langle 0\rvert$ (mean prefix comparability $0.1041 \pm 0.0218$) and independent anchor marks $r(x) \sim \operatorname{Bernoulli}(p_{\rm anc})$ with $p_{\rm anc} = 0.125$. On each $C_{n_0}$, we designate the deepest-past maximal vertex $u_{\rm src} \in \operatorname{Max}(C_{n_0})$ ($r(u_{\rm src}) = 1$) as the source anchor and the minimal-past-overlap vertex $u_{\rm far} \in \operatorname{Max}(C_{n_0}) \setminus \{u_{\rm src}\}$ as a spacelike-separated frontier reference.

Holding $C_{n_0}$ **100% identical** and coupling suffix draws via marginal-preserving Strassen common random numbers (`evolve_suffix` in `nested_regime_source_experiment.py`), we evolve five configurations across the three protocol arms to $N = 512$ and $N = 1024$:
- **Arm A (`arm_A_baseline`):** Unperturbed $\mathcal{Z}_{n_0} = \lvert 0\rangle\langle 0\rvert$ evolved under coupled $(q^{(0)}, q^{(1)})$.
- **Arm B (`arm_B_uncoupled_p05` & `arm_B_uncoupled_p10`):** Apply `evolve_residual` to prepare coherent $\lvert +\rangle\langle +\rvert$ ($p_{\rm exc} = 0.5$) or pure excited $\lvert 1\rangle\langle 1\rvert$ ($p_{\rm exc} = 1.0$) under the **uncoupled control** $q_{\rm ctrl}^{(1)} = q^{(0)}$ (retaining differential phase frequencies $\omega_0 = 0.25, \omega_1 = 0.85$ without structural back-coupling).
- **Arm C (`arm_C_coupled_p10` & `arm_C_coherent_p05`):** Apply the identical `evolve_residual` excitations ($\lvert 1\rangle\langle 1\rvert$ and coherent $\lvert +\rangle\langle +\rvert$) under the **nested active coupled instrument** ($q^{(0)} = q_{\rm LQ}(0.20, 0.20)$, $q^{(1)} = q_{\rm LQ}(0.50, 0.35)$, $\omega_0 = 0.25, \omega_1 = 0.85$), updating $\mathcal{Z}_n$ at every birth via the exact selective Bayesian Kraus map $\mathcal{Z}_{n+1} = \mathcal{J}_{C_n, S_n}(\mathcal{Z}_n) / \operatorname{Tr}\mathcal{J}_{C_n, S_n}(\mathcal{Z}_n)$.

### 4.2 Downstream Clock-Tick, Interval Focusing, Coarse Connectivity, and Recoil Results

#### Table 4.1: Complete Arm Readouts at Horizons $N = 512$ and $N = 1024$ ($M = 40$ Matched Histories)
Here $L_{\max}(u_{\rm src})$ is the maximum directed chain length (in causal links) from $u_{\rm src}$ into $C_N$, $\langle h(I_{\rm src})\rangle$ is the mean interior longest-chain tick count across downstream receipts $v \succ u_{\rm src}$, $\lvert J^+[u_{\rm src}]\rvert$ is inclusive future-cone volume, $R_2^{\rm match}$ and $(h/m)^{\rm match}$ evaluate fixed-cardinality $m \in [12, 24]$ intervals, $\widetilde{R}_2(\Pi_{\mathcal{A}})$ is coarse-grained anchor comparability, and $p_1 = \langle 1\rvert\mathcal{Z}_N\lvert 1\rangle$, $\lvert\rho_{01}\rvert = \lvert\langle 0\rvert\mathcal{Z}_N\lvert 1\rangle\rvert$ track residual recoil and single-history quantum coherence.

| Horizon $N$ | Arm | $L_{\max}(u_{\rm src}) \pm \text{SD}$ | $\langle h(I_{\rm src})\rangle \pm \text{SD}$ | $\lvert J^+[u_{\rm src}]\rvert \pm \text{SD}$ | $m \in [12, 24]$ $R_2^{\rm match}$ | $m \in [12, 24]$ $(h/m)^{\rm match}$ | Coarse $\widetilde{R}_2(\Pi_{\mathcal{A}}) \pm \text{SD}$ | $\langle p_1\rangle$ ($\operatorname{Var}_{\rm betw}(p_1)$) | Single-Hist $\langle \lvert\rho_{01}\rvert\rangle$ |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $512$ | `arm_A_baseline` | $4.175 \pm 1.986$ | $1.3591 \pm 0.7708$ | $19.425 \pm 14.261$ | $0.4935$ | $0.5097$ | $0.0978 \pm 0.0278$ | $0.0000$ ($0.0000$) | $0.0000$ |
| $512$ | `arm_B_uncoupled_p05` | $4.175 \pm 1.986$ | $1.3591 \pm 0.7708$ | $19.425 \pm 14.261$ | $0.4935$ | $0.5097$ | $0.0978 \pm 0.0278$ | $0.5000$ ($0.0000$) | $0.5000$ |
| $512$ | `arm_B_uncoupled_p10` | $4.175 \pm 1.986$ | $1.3591 \pm 0.7708$ | $19.425 \pm 14.261$ | $0.4935$ | $0.5097$ | $0.0978 \pm 0.0278$ | $1.0000$ ($0.0000$) | $0.0000$ |
| $512$ | `arm_C_coupled_p10` | $7.825 \pm 2.500$ | $3.0518 \pm 1.1953$ | $80.475 \pm 48.315$ | $0.4622$ | $0.4775$ | $0.2242 \pm 0.0374$ | $1.0000$ ($0.0000$) | $0.0000$ |
| $512$ | `arm_C_coherent_p05` | $6.000 \pm 2.736$ | $2.1965 \pm 1.1923$ | $46.450 \pm 43.734$ | $0.4782$ | $0.4937$ | $0.1573 \pm 0.0616$ | $0.4750$ ($0.2558$) | $1.00 \times 10^{-72}$ |
| $1024$ | `arm_A_baseline` | $8.375 \pm 2.984$ | $3.1584 \pm 1.2547$ | $115.050 \pm 77.184$ | $0.5022$ | $0.5207$ | $0.1058 \pm 0.0220$ | $0.0000$ ($0.0000$) | $0.0000$ |
| $1024$ | `arm_B_uncoupled_p05` | $8.375 \pm 2.984$ | $3.1584 \pm 1.2547$ | $115.050 \pm 77.184$ | $0.5022$ | $0.5207$ | $0.1058 \pm 0.0220$ | $0.5000$ ($0.0000$) | $0.5000$ |
| $1024$ | `arm_B_uncoupled_p10` | $8.375 \pm 2.984$ | $3.1584 \pm 1.2547$ | $115.050 \pm 77.184$ | $0.5022$ | $0.5207$ | $0.1058 \pm 0.0220$ | $1.0000$ ($0.0000$) | $0.0000$ |
| $1024$ | `arm_C_coupled_p10` | $15.050 \pm 3.021$ | $6.3356 \pm 1.4319$ | $459.250 \pm 139.243$ | $0.4697$ | $0.4882$ | $0.2725 \pm 0.0275$ | $1.0000$ ($0.0000$) | $0.0000$ |
| $1024$ | `arm_C_coherent_p05` | $11.700 \pm 4.274$ | $4.7564 \pm 2.0155$ | $272.925 \pm 203.162$ | $0.4890$ | $0.5076$ | $0.1859 \pm 0.0833$ | $0.4750$ ($0.2558$) | $1.08 \times 10^{-190}$ |

#### Table 4.2: Paired Within-Prefix Differences & $t$-Statistics ($M = 40$ Pairs)
Because `Arm B` shares identical structural random streams with `Arm A`, `B_p10_minus_A` and `B_p05_minus_A` equal $0.0000 \pm 0.0000$ identically across all structural readouts, so `C_p10_minus_B_p10` equals `C_p10_minus_A` identically (`pillar3_source_response.horizons.*.paired_contrasts`):

| Horizon $N$ | Paired Contrast | $\Delta L_{\max}(u_{\rm src})$ ($t$-stat) | $\Delta \langle h(I_{\rm src})\rangle$ ($t$-stat) | $\Delta \lvert J^+[u_{\rm src}]\rvert$ ($t$-stat) | $\Delta R_2^{\rm match}$ ($m \in [12, 24]$) ($t$-stat) | $\Delta \widetilde{R}_2(\Pi_{\mathcal{A}})$ ($t$-stat) | $\Delta R_2^{\rm glob}$ ($t$-stat) |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| $512$ | `B_p10 - A` | $0.000 \pm 0.000$ ($0.00$) | $0.0000 \pm 0.0000$ ($0.00$) | $0.000 \pm 0.000$ ($0.00$) | $0.0000 \pm 0.0000$ ($0.00$) | $0.0000 \pm 0.0000$ ($0.00$) | $0.0000 \pm 0.0000$ ($0.00$) |
| $512$ | `C_p10 - A` | $+3.650 \pm 0.383$ ($+9.52$) | $+1.6927 \pm 0.1794$ ($+9.44$) | $+61.050 \pm 6.691$ ($+9.12$) | $-0.0313 \pm 0.0063$ ($-4.97$) | $+0.1264 \pm 0.0030$ ($+42.44$) | $+0.1296 \pm 0.0016$ ($+80.96$) |
| $512$ | `C_p05 - A` | $+1.825 \pm 0.387$ ($+4.71$) | $+0.8374 \pm 0.1755$ ($+4.77$) | $+27.025 \pm 6.062$ ($+4.46$) | $-0.0153 \pm 0.0057$ ($-2.68$) | $+0.0595 \pm 0.0101$ ($+5.90$) | $+0.0612 \pm 0.0102$ ($+5.97$) |
| $1024$ | `B_p10 - A` | $0.000 \pm 0.000$ ($0.00$) | $0.0000 \pm 0.0000$ ($0.00$) | $0.000 \pm 0.000$ ($0.00$) | $0.0000 \pm 0.0000$ ($0.00$) | $0.0000 \pm 0.0000$ ($0.00$) | $0.0000 \pm 0.0000$ ($0.00$) |
| $1024$ | `C_p10 - A` | $+6.675 \pm 0.470$ ($+14.20$) | $+3.1772 \pm 0.2024$ ($+15.69$) | $+344.200 \pm 18.132$ ($+18.98$) | $-0.0325 \pm 0.0060$ ($-5.41$) | $+0.1667 \pm 0.0029$ ($+57.07$) | $+0.1650 \pm 0.0014$ ($+119.07$) |
| $1024$ | `C_p05 - A` | $+3.325 \pm 0.631$ ($+5.27$) | $+1.5980 \pm 0.2940$ ($+5.43$) | $+157.875 \pm 29.226$ ($+5.40$) | $-0.0131 \pm 0.0057$ ($-2.32$) | $+0.0801 \pm 0.0136$ ($+5.88$) | $+0.0782 \pm 0.0131$ ($+5.96$) |

*Note*: Paired values above report $\text{mean} \pm \text{SEM}$ ($n_{\rm pairs} = 40$). At $N = 1024$, matched-cardinality proper-time density $(h/m)^{\rm match}$ shifts by $-0.0325 \pm 0.0052$ ($t = -6.24$) while Hasse link fraction $\ell_{\rm link}^{\rm match}$ rises from $0.2768 \pm 0.0137$ (`Arm A`) to $0.2975 \pm 0.0137$ (`Arm C_p10`).

### 4.3 Physical & Combinatorial Interpretation of the Three Key Signatures
1. **Separation of Macroscopic Cone/Tick Expansion from Fixed-$m$ Diamond Widening:** Source excitation into $q^{(1)} = q_{\rm LQ}(0.50, 0.35)$ nearly doubles downstream proper-time ticks $L_{\max}(u_{\rm src})$ ($8.375 \to 15.050$ at $N = 1024$, $t = 14.20$) and quadruples future-cone volume ($115.05 \to 459.25$, $t = 18.98$). Crucially, evaluating **matched-cardinality** intervals $m \in [12, 24]$ demonstrates that this is *not* mere 1D chain inflation: inside fixed-size intervals, $R_2^{\rm match}$ *decreases* by $-0.0325$ ($t = -5.41$), $(h/m)^{\rm match}$ decreases by $-0.0325$ ($t = -6.24$), and link fraction $\ell_{\rm link}^{\rm match}$ increases ($0.2768 \to 0.2975$), reflecting wider multi-parent causal diamonds (analogous to negative-curvature diamond focusing in `PW6A_PROTOCOL.md` §3.2).
2. **Two-Way Interaction (`Residual -> Order` and `Order -> Residual` Recoil):** Under coherent initial excitation $\mathcal{Z}_{n_0} = \lvert +\rangle\langle +\rvert$ ($p_{\rm exc} = 0.5$), uncoupled `Arm B` exhibits pure history-dependent phase rotation: ensemble-averaged coherence $\lvert\mathbb{E}[\rho_{01}]\rvert$ decays from $0.5000$ to $0.0580$ ($N = 512$) and $0.1495$ ($N = 1024$), **yet on every individual history** $\lvert\langle 0\rvert\mathcal{Z}_N\lvert 1\rangle\rvert = 0.5000$ and $\langle 1\rvert\mathcal{Z}_N\lvert 1\rangle = 0.5000$ ($\operatorname{Var}_{\rm betw}(p_1) = 0.0000$). Under coupled `Arm C`, committed structural births perform selective Bayesian recoil on $\mathcal{Z}_n$, driving single-history posterior population onto $\{0, 1\}$ ($19/40 = 0.4750$ excited realizations, $\operatorname{Var}_{\rm betw}(p_1) = 0.2558$) and collapsing single-history coherence to $1.00 \times 10^{-72}$ ($N = 512$) and $1.08 \times 10^{-190}$ ($N = 1024$).
3. **Honest Spatial-Localization Control ($u_{\rm src}$ vs. $u_{\rm far}$):** Because the Theorem 3.3 instrument $(q^{(0)}, q^{(1)})$ couples to a single horizon-wide residual carrier $\mathcal{Z} \in \mathcal{D}(\mathbb{C}^2)$, the spacelike-separated frontier reference $u_{\rm far}$ responds symmetrically alongside $u_{\rm src}$: at $N = 1024$, $L_{\max}(u_{\rm far})$ shifts from $7.825 \pm 3.358$ (`Arm A`) to $14.900 \pm 3.862$ (`Arm C_p10`) and $\lvert J^+[u_{\rm far}]\rvert$ shifts from $106.30 \pm 87.14$ to $443.50 \pm 195.31$. This confirms zero spurious vertex-index bias while establishing that $(q^{(0)}, q^{(1)})$ models a **spatially homogeneous (zero-wavenumber) source mode** rather than a spatially $1/r$-localized gravitational potential.

---

## 5. Explicit Limitations, Negative Controls, and Open Mathematical Obligations

1. **Spatial Localization Obligation (`Open`):** Achieving distance-decaying focusing ($\Delta L_{\max}(u_{\rm src}) \gg \Delta L_{\max}(u_{\rm far})$ as causal/graph distance between $u_{\rm src}$ and $u_{\rm far}$ grows) requires replacing the monolithic two-state carrier $\mathcal{Z} \in \mathcal{D}(\mathbb{C}^2)$ with vertex-local past-record registers $\mathcal{R}(v)$ propagating strictly along covering links $\operatorname{Max}(S)$ (`PW6A_PROTOCOL.md` Theorem 5.4), while avoiding the stage-normalized partition-function obstruction (`PW6A` Theorem 5.3).
2. **Finite-Horizon Attenuation in Fixed-Matrix Active Laws (`Theorem 3.2` vs. `Theorem 3.3`):** In Theorem 3.2, maintaining entrywise positivity of $M_t(r_{P_n}(S))$ with fixed retention $t \in (0, 1)$ requires $\theta < \frac{1 - t}{2} t^{N_{\rm act} - 1}$, so per-step coupling amplitude scales as $O(t^{N_{\rm act} - n})$ at early steps when $N_{\rm act}$ is large. Theorem 3.3 overcomes finite-$N_{\rm act}$ capping ($0 \le n < \infty$) via diagonal CPTP Kraus operators interleaved with `evolve_residual`, at the cost that between explicit `evolve_residual` operations its conditional dynamics bifurcates across modes ($p_{\rm exc} \in \{0, 1\}$ recoil). Constructing an all-horizon ($N_{\rm act} = \infty$), diamond-commuting, continuously self-stabilizing 4D feedback law with wide transverse entry layers ($w_{\min}(I)/m \approx 0.67$) remains open.
3. **No Physical Clock Calibration, Mass Identification, or General Relativity Claim:** Discrete chain-tick count $L_{\max}(u_{\rm src})$, interval proper-time density $h(I)/m$, and coarse comparability $\widetilde{R}_2(\Pi_{\mathcal{A}}(C_N))$ are conditional order-theoretic observables on finite posets. Per `docs/track_b/RECORD_PROCESS_CONTRACT.md` (§5) and `docs/coordination/NATIVE_MASS_MAPPING.md`, birth index is bookkeeping rather than elapsed physical duration, `evolve_residual` excitation is not calibrated physical rest energy or inertial mass, and interval focusing does not derive a Lorentzian metric, geodesic deviation, or Einstein's field equations.

---

## 6. Cross-Scale Relational Coherence (`CR-2`) as a Quarantined Generative Constraint

### 6.1 Mathematical Formulation of `CR-2` and Law-Class Elimination
Synthesizing Pillars 1–3 yields a sharp mathematical constraint—**Cross-Scale Relational Coherence (`CR-2`)**—requiring any candidate dynamical law on $X = (C, \mathcal{Z})$ to satisfy three simultaneous mathematical conditions:
1. **Diamond Order-Invariance:** Unnormalized multi-step branch maps on $(C, \mathcal{Z})$ commute identically across every incomparable-birth diamond within each commitment epoch, and coarse projection $\Pi_{\mathcal{A}}$ uses strictly past-intrinsic/mark-covariant anchor selection.
2. **Cross-Regime Memory Compatibility:** Coarse-grained evolution on $\Pi_{\mathcal{A}}(X) = (\widetilde{C}, \widetilde{\mathcal{Z}})$ accounts explicitly for omitted micro-interval ideal volumes $\widetilde{\mathcal{Z}}_{\rm geom}$ rather than assuming naive Markovianity on $\widetilde{C}$ alone.
3. **Active Present-State Responsiveness with Two-Way Recoil:** Present-state residual transformations (`evolve_residual` at fixed committed history $C_{n_0}$) produce non-degenerate downstream structural shifts ($\Delta_{\rm update} \ne 0$, `Arm C - Arm A != 0`) accompanied by lawful `Order -> Residual` conditioning, rather than reducing to a static initial-seed mixture or forward-only spectator carrier.

#### Table 6.1: Summary of Candidate Law Classes Eliminated by `CR-1` and `CR-2`

| Candidate Law Class | Eliminated By | Exact Mathematical / Empirical Obstruction |
|:---|:---|:---|
| Finite-cutoff CSG ($k_{\max} < \infty$) & sparse DAG closures | `CR-1` + Pillar 1 | $R_2(P_N) = O(N^{-1/k_{\max}}) \to 0$ (`cutoff_kmax2`: $0.1108 \to 0.0807 \to 0.0584$); tree intervals have $R_2(I) \equiv 1$. |
| Fixed-$p$ percolation ($t_k = (\frac{p}{1-p})^k$) | `CR-1` Thm. 5.2 + Pillar 1 | Exact transitive saturation $R_2(P_N) \xrightarrow{\mathbb{P}} 1$ (`percolation_p008`: $0.8605 \to 0.9290 \to 0.9640$). |
| Gevrey CSG ($t_k = c^k/(k!)^\beta$, $\beta > 0$) | `CR-1` Prop. 7.1 & §7.3 | Polynomial active-seed growth $\mathbb{E}[K_n] = \Theta((cn)^{1/(\beta+1)}) \gg \ln n$ with monotonic finite-horizon upward $R_2$ drift through $N = 1024$. |
| Passive static CSG mixtures $\int \mathbb{P}_{\mathbf{t}}\,d\mu(\mathbf{t})$ | `CR-1` Prop. 5.3 + Thm. 3.3 | Heterogeneous $\mu$ ($\operatorname{Var}_\mu(r(\Theta)) > 0$) fails single-history concentration (`PW6A` Thm. 4.2), while **every** passive time-homogeneous $\mu$ obeys $\mathbb{P}_\mu(\mathcal{E}_{\rm post})/\mathbb{P}_\mu(\mathcal{E}_{\rm pre}) \equiv \frac{2}{n_0 - 1}$, unable to represent present-state `evolve_residual` interventions. |
| Uncoupled static scalar Log-Quadratic CSG as standalone geometry | Pillar 1 (Prop. 2.1) | Active seed drift $\Delta\mu_{\rm octave} = \frac{\ln 2}{\ln(1/q)}$ forces monotonic $\mathbb{E}[R_2]$ and fixed-$m$ drift ($+0.0293$/octave at $m \in [6, 11]$) and narrow entry width ($w_{\min}/m = 0.1387$ vs. $0.6717$). |
| Coarse-order-only Markov laws on $\widetilde{C}_n = \Pi_{\mathcal{A}}(C_n)$ | Theorem 3.1(2) | Omitted micro-chains $C^{(m)}$ share identical $\widetilde{C} = \{u \prec v\}$ while branching ratio $\mathcal{R}_{\rm branch}(m) = Z_{m+1} - 1$ grows strictly with $m$ ($0.2923$ coarse-only gap at $N \le 4$). |
| Extrinsic stage-indexed projections & stage-normalized damping | Theorem 3.1(1) + `CR-1a` | Violates diamond commutation ($3,644 / 3,644$ violations for stage-parity anchor selection). |
| Forward-only uncoupled residual laws ($q_{\rm ctrl}^{(1)} = q^{(0)}$) | Theorem 3.2(3) + Pillar 3 | Zero structural response ($\Delta_{\rm update} = 0$; `Arm B - Arm A == 0.0000` across all $M = 40$ runs) and zero single-history recoil ($\operatorname{Var}(p_1) = 0$). |

### 6.2 Status-M Quarantine and Strict Claim Hygiene
In accordance with `ONTOLOGY.md`, `GOVERNANCE.md`, and `docs/track_b/boundary_concepts.md`:
- **Zero Theological Variables in Equations:** All definitions, theorems, transition kernels, and observables in this document are purely mathematical objects defined on finite posets and finite-dimensional linear/CPTP operators. No theological, agential, or Status-M symbols enter any formula.
- **Role of Heuristic Motivation vs. Admitted Proof:** While DET's presentist Track B philosophy motivates investigating live present-state activity ($X = (C, \mathcal{Z})$) alongside immutable committed records rather than block-static mixtures, philosophical or aesthetic coherence (`CR-2`) serves strictly as a **heuristic search filter** for formulating falsifiable mathematical conjectures. Every retained result stands or falls solely on explicit proofs, pre-declared holdout gates, and controlled numerical experiments—as demonstrated by Pillar 1's retirement of standalone static Log-Quadratic CSG.
- **No Divine-Authorship or Physical-Completion Claim:** Narrowing the class of admissible mathematical growth laws via `CR-1` and `CR-2` does **not** establish divine authorship, teleology, ontological agency, quantum mechanics, physical clock calibration, or General Relativity.

---

## 7. Reproducibility & Verification Manifest

All theorems, exhaustive finite-poset audits, multi-horizon holdout tables, and paired three-arm experiments are reproduced deterministically by executing:

```bash
python3 docs/track_b/verification/run_nested_regime_verification.py
```

- **Verification Artifacts:**
  - `docs/track_b/verification/nested_regime_source_experiment.py` — Vectorized CSG/Minkowski samplers, 5-observable bulk interval engine, exact 1D Future-Cone Markov solver, coarse-projection & active residual law audits, and Strassen-coupled 3-arm source-response simulator.
  - `docs/track_b/verification/test_nested_regime_source_experiment.py` — 18 unit & mathematical property tests covering antichain/chain/bipartite exact observables, Myrheim–Meyer inversion, full $N = 5$ trajectory enumeration vs. 1D Markov chain, 4D width separation, coarse projection diamonds, omitted-chain formulas, $\widetilde{\mathcal{Z}}_{\rm geom}$ Markov sufficiency, $N_{\rm act} \in \{8, 12\}$ active root-martingale laws, CPTP non-mixture separation, and paired recoil controls.
  - `docs/track_b/verification/run_nested_regime_verification.py` — Master verification harness executing all 18 unit tests and asserting Gates 1–4 (`total_wall_seconds = 45.989`, Pillar 1 `23.66s`, Pillar 3 `19.26s`; exit code `0`).
  - `docs/track_b/verification/nested_regime_experiment_results.json` — Complete RFC-8259-compliant deterministic numerical output matching every figure in Tables 2.1–4.2 and inline text.
