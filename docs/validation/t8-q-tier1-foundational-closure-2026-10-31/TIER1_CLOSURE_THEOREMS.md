# Conditional Tier I Bridges: Bell-CHSH Causal Growth, Degree and Dimension Selection, Degenerate Lüders Update, and Walsh-Section Probability Acquisition

31 October 2026. **CONDITIONAL_TIER1_FOUNDATIONAL_THEOREMS; OBSTRUCTIONS_AND_CLASSICAL_COMPARATORS_EXPLICIT.**

**Audit correction, 31 October 2026 (HST):** This revision repairs the all-dimension spectral argument in Theorem 4A, supplies the full-map diamond premise of Theorem 1A, and narrows the dimension, projector-lift, quotient and arithmetic claims. The original note is preserved at commit `50be57d85aab1bf0396143694b4f9c32632010de`; the prospective protocol and checker remain byte-identical. [`AUDIT_AMENDMENT.md`](AUDIT_AMENDMENT.md) records the deviations and verification limits. These revisions await distinct review and coordinator disposition. Here “spacelike” means order-incomparable births only, with no Lorentzian geometry implied. The Walsh constructions act on the specified sections; no extension of the single-system quotient to every representative under arbitrary joint tests is claimed.

The prospective protocol was committed in [`PROTOCOL.md`](PROTOCOL.md) (`b673dc5`) before the original theorem-note commit; committed order alone does not independently establish when reasoning or execution occurred. This study extends [`t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md`](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md) (`9b38efe`) and [`t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md`](../t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md) (`2e68a48`) on branch `qr-pair-kernel-bridge` without modifying any previously frozen file, accepted source, core module, or other branch (`main`, `ret`, `qr-05-bridge`). All results are conditional mathematical theorems, obstructions, and comparators (`TH-DET` / `MATH` at declared scope) under [`GOVERNANCE.md`](../../../GOVERNANCE.md).

---

## 1. Executive Summary and Tier I Premise-to-Conclusion Map

The upstream bridges [`BRIDGE_THEOREM.md`](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md) and [`RELATIONAL_IDENTITY_BRIDGE.md`](../t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md) conditionally connected silent quarter-phase interchange (\(D\odot E=D\otimes E\)), two-copy coincidence grouping (\(D(A_r,A_s)=0\)), coarse-cell dyadic principal-minor positivity on the Walsh section \(J_n(D)\), complex qubit cone selection (\(\mathcal C_4/{\sim_{\mathscr T}}\cong\mathrm{PSD}_2(\mathbb C)\), \(J^2=-I_{2m}\)), and single-wing four-birth active causal growth (\(\Delta_Z=263/1{,}115{,}136\)). Across [`OPERATIONAL_PREMISE_LEDGER.md`](../../coordination/OPERATIONAL_PREMISE_LEDGER.md), [`PROOF_SYNTHESIS_AND_PREMISE_SELECTION.md`](../../research/PROOF_SYNTHESIS_AND_PREMISE_SELECTION.md), [`SCALAR_VALUE_ERROR_CONTRACT.md`](../../coordination/SCALAR_VALUE_ERROR_CONTRACT.md) (RI-23), [`grade2_justification.py`](../../../det8/models/grade2_justification.py), [`REPEATABLE_INSTRUMENT.md`](../t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md) (RI-08c), and [`CUT_CLOSED_COMPLETION.md`](../t8-q-cut-closed-completion-2026-09-13/CUT_CLOSED_COMPLETION.md) (RI-08g), this package selected the following four mathematical questions; the cited scope is not an inventory of every accepted programme result:

1. **Gap G1 (Two-wing spacelike causal-diamond Bell-CHSH growth law):** Single-wing attenuated causal-order visibility admitted a \(d=4\) mixed classical comparator \((\Delta_4,C_4)\), whereas [`BRIDGE_THEOREM.md` Theorem 3C](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md) achieved \(S_{\mathrm{CHSH}}=14/5>2\) only as a static algebraic readout on [RI-08d](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md)'s 16-label kernel \(N'\) without embedding into an admitted causal-order birth law satisfying [`THEOREM_PACKAGE.md` §1](../../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model).
2. **Gap G2 (Operational exclusion of grade-\(\ge 3\) Sorkin interference):** [`grade2_justification.py`](../../../det8/models/grade2_justification.py) proved that normalization and Boolean positivity admit grade-3 measures (\(I_3\ne 0\)), leaving `grade <= 2` pairwise biadditivity as an unjustified premise upstream of [`DERIVATION.md`](../t8-q-strict-derivation-2026-09-12/DERIVATION.md).
3. **Gap G3 (Degenerate `rank >= 2` selective post-commitment update):** [RI-08c](../t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md) relied on rank-1 exposed rays to derive post-measurement state resets, leaving open which non-circular principle selects the coherence-preserving **Lüders projection** \(\rho\mapsto P_R\rho P_R\) over measure-and-prepare or dephasing resets on degenerate `rank >= 2` coarse record cells (`n >= 3`).
4. **Gap G4 (Minor-sign catalogue copy bound and single-copy acquisition on a new domain):** Coarse-cell minor positivity required up to \(m=n\) copies, while [RI-23 §6](../../coordination/SCALAR_VALUE_ERROR_CONTRACT.md) proved that on raw \(K_n\), rank-1 total-entry mass \(\Gamma_n=\mathbf 1_n\mathbf 1_n^\dagger\) blocks any informationally complete single-copy catalogue of bounded probability effects \(0\le\operatorname{Tr}(DT)\le M_n(D)\).

| Tier I gap & theorem | Load-bearing operational premises | Proved mathematical conclusion | Exact obstruction / classical comparator |
|---|---|---|---|
| **G1 — Theorem 1A–1C** (§2): Spacelike causal-diamond Bell-CHSH birth law | Dyadic transitive-percolation \(q_{1/2}(P,S)>0\); two-origin spacelike setting seed \(P_0=\{r_A,r_B\}\); precursor-mark-local Walsh projectors \(\widehat Q_{A,x,a}\otimes I_4\), \(I_4\otimes\widehat Q_{B,y,b}\) on \(N'=(J_2\otimes J_2)(\sigma_{\mathrm{joint}})\) | Strictly positive \(q_{1/2}\), strict precursor-mark locality, four-cell block-diagonality, \(M_{16}=\operatorname{Tr}\) row normalization, exact \(256\times 256\) superoperator diamonds across **all** ideal pairs \((S,T)\), wingwise repeatability & no-signaling, and \(S_{\mathrm{CHSH}}=14/5>2\) on \(P_4^\parallel\) | **Theorem 1A:** Unanchored precursor-isomorphism locality together with full unnormalized branch-map diamonds forces all four instruments to commute (\(|S_{\mathrm{CHSH}}|\le 2\) on *any* cone). **Theorem 1C:** Bipartite/residual-no-signaling classical simplices obey \(|S_{\mathrm{CHSH}}|\le 2\), whereas omitting subsystem locality admits an explicit 10-state commuting simplex PR-box (\(S_{\mathrm{CHSH}}=4\)) |
| **G2 — Theorem 2A–2C** (§3): Operational exclusion of grade-\(\ge 3\) Sorkin interference | *Route B:* Degree-\(k\) homogeneous slit-amplitude scaling + signed-phase positivity + one \((3,4,5)\) rotation conserving two-cell mass. *Route C:* Sorkin-hierarchy dimension \(d(n)=\sum_{r=1}^m c_r\binom n r\) + composite multiplicativity \(d(n_1n_2)=d(n_1)d(n_2)\) + \(d(2)\le 4\) | Route B forces even \(k=2r\) and \((9/25)^r+(16/25)^r=1\iff k=2\implies I_m\equiv 0\) (\(\forall m\ge 3\)). Route C forces \(d(n)=n^{r_0}\) with Stirling \(c_r=r!\,S(r_0,r)\), selecting only \(d(n)=n\) or \(d(n)=n^2\) and the corresponding coefficients; no cone or interference rule follows from dimension alone | **Theorem 2A:** 4-atom witness (\(I_2=0\) pairwise, \(I_3=1/4\)) and 3-atom masked witness \(\mu_{\mathrm{mask}}\) (singleton-complete + Pairwise Decoherence Sufficiency everywhere, yet \(I_3=1/8\ne 0\)). Degree-4 \(F_4(a)=((a_0+a_1+a_2)/3)^4\) gives \(I_3=4/9\) without rotated partition conservation |
| **G3 — Theorem 3A–3C** (§4): Degenerate `rank >= 2` Lüders projection | 1-positivity \(\Phi(\mathrm{PSD}_n)\subseteq\mathrm{PSD}_n\) (**zero** Kraus/CP assumption); effect calibration \(\operatorname{Tr}(\Phi(\rho))=\operatorname{Tr}(P\rho)\); repeat-face non-disturbance \(\Phi(\sigma)=\sigma\) on \(F_P\) (on the qutrit repeat face, equivalently finer-cell non-disturbance across the declared three subspace controls) | Uniquely derives the exact **Lüders rule** \(\Phi(\rho)=P\rho P\) for *every* rank \(1\le d\le n\) (eliminating cross-subspace terms via rank-1 quadratic discriminant \(at^2+bt\ge 0\implies b=0\)), for coordinate/coarse-cell \(P=P_R\), lifted on \(J_n(\rho)\) by one dyadic-rational projector \(\widehat P\in M_{nL}(\mathbb Z[1/2])\) | **Theorem 3A & 3C:** On \(J_3(\mathrm{PSD}_3)\) (\(P_{01}=\operatorname{diag}(1,1,0)\), \(\dim_{\mathbb R}F_{01}=4\)), calibration + repeatability admit \(\mathcal T_{01}^{\mathrm{mix}}\) and \(\mathcal T_{01}^{\mathrm{deph}}\) (even preserving fine \(\{C_0,C_1\}\) weights without silent controls); literal cut \(\Pi_{C_{01}}\) leaves \(\operatorname{span}(J_3)\) with dark zero-mass payload |
| **G4 — Theorem 4A–4B** (§5): Minor-catalogue copy obstruction and Walsh-section acquisition | Walsh section cone \(J_n(\mathrm{PSD}_n(\mathbb C))\) (\(M_{nL}=\operatorname{Tr}\)); \(1+2\binom n2\) exact Gaussian-rational \(\sim_{\mathscr T}\)-lifted Pythagorean silent unitaries \(\mathcal W^{R,\mathrm{Pyth}}_{ij},\mathcal W^{I,\mathrm{Pyth}}_{ij}\in U(nL,\mathbb Q(i))\) | **Theorem 4A:** Skew-Hermitian tournament family \(D^{(n)}_{\mathrm{imag}}(t_n)=\frac1n I_n+it_n T_n\) (\(\forall n\ge 2\)) has \(\operatorname{Tr}=M_n=1\), uniform single-copy weights, and **all \(2^n-2\) proper submatrices (\(|I|\le n-1\)) strictly PD** while \(\det<0\). **Theorem 4B:** Supplies single-copy coarse-cell probabilities in \([0,1]\) on the Walsh section, an exact linear inverse and deterministic bounds (rational when the supplied data and bounds are rational); [RI-23 §6](../../coordination/SCALAR_VALUE_ERROR_CONTRACT.md) remains valid on its raw domain | Raw \(K_n\) collapses bounded effects \(0\le T\le\mathbf 1_n\mathbf 1_n^\dagger\) to rank 1; uncoupled \(D_+^{\otimes m}\) stays nonnegative for all \(m\ge 1\); single-copy *signs* alone remain polyhedral-blind on RI-23's \(D_*\) |

---

## 2. Target G1 — Unattenuated Bipartite Spacelike Causal-Diamond Bell-CHSH Growth Law

### 2.1 Unanchored precursor-locality monogamy obstruction

In [`THEOREM_PACKAGE.md` §1](../../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model), an admitted growth model assigns to every finite order \(P\), binary mark map \(r:P\to\{0,1\}\), downward-closed ideal \(S\in\mathcal I(P)\), and newborn mark \(b\in\{0,1\}\) a strictly positive ideal probability \(q(P,r,S)>0\) (\(\sum_{S\in\mathcal I(P)}q(P,r,S)=1\)) obeying the incomparable-birth scalar diamond identity \(q(P,r,S)q(P+u_S,r+a,T)=q(P,r,T)q(P+v_T,r+b,S)\). Before introducing localized origin roots, we prove why a *strictly unanchored* active-residual branch law depending solely on the unlabeled marked isomorphism class \([P|_S,r|_S]\) can never violate Bell-CHSH on *any* operational cone:

**Theorem 1A (Unanchored precursor-locality forces universal instrument commutativity and \(|S_{\mathrm{CHSH}}|\le 2\)).** *Let \((V,K,M)\) be any finite-dimensional pointed ordered vector space with nonnegative linear mass functional \(M:K\to\mathbb R_{\ge 0}\). Suppose an active-residual growth law has the strictly unanchored precursor-local form*
\[
\mathcal B^{P,r}_{S,b}(\mathfrak D) = q(P,r,S)\,\mathcal M\bigl([P|_S,r|_S],\,b\bigr)(\mathfrak D)\qquad(\mathfrak D\in V),
\tag{1}
\]
*where \(q(P,r,S)>0\) satisfies scalar diamonds, the complete unnormalized branch maps obey incomparable-birth diamonds on all of \(V\) for every base, ideal pair and newborn-mark pair, and each \(\mathcal M([Q,r_Q],b):V\to V\) is cone-positive (\(\mathcal M(K)\subseteq K\)), depends only on the unlabeled marked poset isomorphism class \([Q,r_Q]\), and is mass-complete (\(\sum_{b\in\{0,1\}}M(\mathcal M([Q,r_Q],b)(\mathfrak D))=M(\mathfrak D)\) on \(V\)). Then:*

1. **Universal mutual commutativity:** *For every pair of finite marked posets \((Q_1,r_1),(Q_2,r_2)\) and every \((a,b)\in\{0,1\}^2\),*
   \[
   \bigl[\mathcal M([Q_1,r_1],a),\;\mathcal M([Q_2,r_2],b)\bigr] = 0\qquad\text{on all of }V.
   \tag{2}
   \]
2. **Universal CHSH bound across all cones:** *For any normalized initial state \(\mathfrak D_0\in K\) (\(M(\mathfrak D_0)=1\)) and any four precursor classes \(\{[Q_{A,0}],[Q_{A,1}],[Q_{B,0}],[Q_{B,1}]\}\) representing binary settings \(x,y\in\{0,1\}\), the joint outcome probabilities \(P(a,b\mid x,y)=M\bigl(\mathcal M([Q_{A,x}],a)\mathcal M([Q_{B,y}],b)(\mathfrak D_0)\bigr)\) are exact marginals of a single 16-outcome nonnegative joint probability distribution \(p(a_0,a_1,b_0,b_1)\ge 0\) (\(\sum p=1\)) and therefore satisfy*
   \[
   \bigl|E(0,0)+E(0,1)+E(1,0)-E(1,1)\bigr|\le 2.
   \tag{3}
   \]

**Proof.**
*(1)* Form the disjoint union \((P,r)=(Q_1,r_1)\sqcup(Q_2,r_2)\) with ideals \(S=Q_1\in\mathcal I(P)\) and \(T=Q_2\in\mathcal I(P)\). Appending \(u_S\) above \(S\) leaves \((P+u_S)|_T=Q_2\) with mark \(r_2\), and appending \(v_T\) above \(T\) leaves \((P+v_T)|_S=Q_1\) with mark \(r_1\). Superoperator diamond commutation \(\mathcal B^{P+u_S,r+a}_{T,b}\circ\mathcal B^{P,r}_{S,a}=\mathcal B^{P+v_T,r+b}_{S,a}\circ\mathcal B^{P,r}_{T,b}\) reads
\[
q(P,r,S)\,q(P+u_S,r+a,T)\,\mathcal M([Q_2,r_2],b)\circ\mathcal M([Q_1,r_1],a)
= q(P,r,T)\,q(P+v_T,r+b,S)\,\mathcal M([Q_1,r_1],a)\circ\mathcal M([Q_2,r_2],b).
\]
The full-map identity is an independent hypothesis, not a consequence of scalar diamonds. Dividing by the strictly positive equal scalar diamond factors proves (2).

*(2)* Write \(\mathcal M_{W,s,c}:=\mathcal M([Q_{W,s}],c)\) (\(W\in\{A,B\}\), \(s,c\in\{0,1\}\)). By (2), all four instrument families mutually commute—including same-wing pairs \([\mathcal M_{A,0,a_0},\mathcal M_{A,1,a_1}]=0\) and \([\mathcal M_{B,0,b_0},\mathcal M_{B,1,b_1}]=0\). Define
\[
p(a_0,a_1,b_0,b_1) := M\Bigl(\mathcal M_{A,0,a_0}\mathcal M_{A,1,a_1}\mathcal M_{B,0,b_0}\mathcal M_{B,1,b_1}(\mathfrak D_0)\Bigr)\ge 0.
\tag{4}
\]
For any setting pair \((x,y)\in\{0,1\}^2\), use (2) to commute \(\mathcal M_{A,1-x,a_{1-x}}\) and \(\mathcal M_{B,1-y,b_{1-y}}\) to the front adjacent to \(M\). Applying mass-completeness \(M\circ(\mathcal M_{W,s,0}+\mathcal M_{W,s,1})=M\) twice eliminates \(a_{1-x}\) and \(b_{1-y}\), yielding \(\sum_{a_{1-x},b_{1-y}}p(a_0,a_1,b_0,b_1)=M(\mathcal M_{A,x,a_x}\mathcal M_{B,y,b_y}(\mathfrak D_0))=P(a_x,b_y\mid x,y)\) and \(\sum_{a_0,a_1,b_0,b_1}p=M(\mathfrak D_0)=1\). For every \((a_0,a_1,b_0,b_1)\in\{0,1\}^4\), \(\alpha_s=(-1)^{a_s}\in\{\pm 1\}\) and \(\beta_t=(-1)^{b_t}\in\{\pm 1\}\) obey \(|\alpha_0(\beta_0+\beta_1)+\alpha_1(\beta_0-\beta_1)|=2\), so convex averaging over (4) yields (3). ∎

Theorem 1A explains structurally why [RI-08d](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md) explicitly retained distinct named origin tags (`Independence(origins=("local","reference"))`): localized origin roots allow Wing A and Wing B to act on disjoint factors while preventing two incompatible Wing-A settings from firing simultaneously as spacelike siblings on the same factor.

### 2.2 Anchored 16-label spacelike causal-diamond Bell-CHSH birth law

For any finite poset \(P\) and downward-closed ideal \(S\in\mathcal I(P)\), let \(\max(S)=\{u\in S:\neg\exists v\in S,\ u\prec v\}\) and define the exact dyadic transitive-percolation scalar law at edge parameter \(p=1/2\):
\[
q_{1/2}(P,S) := 2^{|S|-|\max(S)|-|P|} > 0.
\tag{5}
\]
Every subset \(X\subseteq P\) generates a unique downward closure \(\downarrow X=S\), and \(\downarrow X=S\iff \max(S)\subseteq X\subseteq S\), which holds for \(2^{|S|-|\max(S)|}\) subsets \(X\subseteq P\). Hence \(\sum_{S\in\mathcal I(P)}q_{1/2}(P,S)=2^{-|P|}\cdot 2^{|P|}=1\) for every finite poset \(P\). Moreover, if \(S,T\in\mathcal I(P)\) and \(u_S\) is appended with strict past \(S\), then \(u_S\notin T\), so \(T\) retains the exact same \(|T|\) and \(|\max(T)|\) inside \(P+u_S\) while \(|P+u_S|=|P|+1\), giving the all-horizon scalar diamond identity
\[
q_{1/2}(P,S)\,q_{1/2}(P+u_S,T) = 2^{|S|+|T|-|\max(S)|-|\max(T)|-2|P|-1} = q_{1/2}(P,T)\,q_{1/2}(P+v_T,S).
\tag{6}
\]

Recall from Theorem 1A of [`RELATIONAL_IDENTITY_BRIDGE.md`](../t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md) the two-cell Walsh section \(J_2(D)=\frac14 V_{2,2}(I_2\otimes H_2 D H_2)V_{2,2}\) (\(V_{2,2}=\operatorname{diag}(I_2,Z)\), \(H_2=\bigl(\begin{smallmatrix}1&1\\1&-1\end{smallmatrix}\bigr)\)) and define for any \(K\in M_2(\mathbb C)\) its \(\sim_{\mathscr T}\)-lifted \(4\times 4\) operator
\[
\widehat K := V_{2,2}\Bigl(I_2\otimes\bigl(\tfrac12 H_2 K H_2\bigr)\Bigr)V_{2,2},
\qquad \widehat K\,J_2(D)\,\widehat K^\dagger = J_2(K D K^\dagger).
\tag{7}
\]
Define the eight **exact rational** rank-1 qubit projectors \(Q_{A,x,a},Q_{B,y,b}\in M_2(\mathbb Q)\) (\(x,y,a,b\in\{0,1\}\)):
\[
Q_{A,0,0}=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix},\quad
Q_{A,0,1}=\frac12\begin{pmatrix}1&-1\\-1&1\end{pmatrix},\quad
Q_{A,1,0}=\begin{pmatrix}1&0\\0&0\end{pmatrix},\quad
Q_{A,1,1}=\begin{pmatrix}0&0\\0&1\end{pmatrix},
\tag{8}
\]
\[
Q_{B,0,0}=\frac1{10}\begin{pmatrix}9&3\\3&1\end{pmatrix},\quad
Q_{B,0,1}=\frac1{10}\begin{pmatrix}1&-3\\-3&9\end{pmatrix},\quad
Q_{B,1,0}=\frac1{10}\begin{pmatrix}9&-3\\-3&1\end{pmatrix},\quad
Q_{B,1,1}=\frac1{10}\begin{pmatrix}1&3\\3&9\end{pmatrix},
\tag{9}
\]
and let \(\widehat Q_{A,x,a},\widehat Q_{B,y,b}\in M_4(\mathbb Q)\) be their dyadic Walsh lifts via (7). Start from the two-origin spacelike setting seed \(P_0=\{r_A,r_B\}\) (\(r_A\parallel r_B\)) carrying immutable binary setting marks \(x=r(r_A)\in\{0,1\}\), \(y=r(r_B)\in\{0,1\}\) and the **setting-independent** coupled 16-label pair kernel \(N_0=N'=\mathcal U(D_{+X}\otimes R_{t=1})\mathcal U^\dagger\) of [RI-08d](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md). For every finite marked order \((P,r)\) extending \(P_0\), every downward-closed ideal \(S\in\mathcal I(P)\), and every newborn mark \(c\in\{0,1\}\), define the active-residual branch map \(\mathcal B^{P,r}_{S,c}:M_{16}(\mathbb C)\to M_{16}(\mathbb C)\) by
\[
\boxed{
\mathcal B^{P,r}_{S,c}(N) :=
\begin{cases}
q_{1/2}(P,S)\,\bigl(\widehat Q_{A,r(r_A),c}\otimes I_4\bigr)\,N\,\bigl(\widehat Q_{A,r(r_A),c}\otimes I_4\bigr), & r_A\in S,\ r_B\notin S, \\[4pt]
q_{1/2}(P,S)\,\bigl(I_4\otimes\widehat Q_{B,r(r_B),c}\bigr)\,N\,\bigl(I_4\otimes\widehat Q_{B,r(r_B),c}\bigr), & r_B\in S,\ r_A\notin S, \\[4pt]
\dfrac12\,q_{1/2}(P,S)\,N, & S\cap\{r_A,r_B\}\in\{\varnothing,\{r_A,r_B\}\}.
\end{cases}
}
\tag{10}
\]

**Theorem 1B (Admitted 16-label spacelike causal-diamond Bell-CHSH growth law).**
1. **Exact Walsh-section identity for RI-08d's \(N'\):** *\(N'=(J_2\otimes J_2)(\sigma_{\mathrm{joint}})\) where \(\sigma_{\mathrm{joint}}=|\psi_{\mathrm{joint}}\rangle\langle\psi_{\mathrm{joint}}|\) and \(|\psi_{\mathrm{joint}}\rangle=\frac12(|00\rangle+|01\rangle+|10\rangle-|11\rangle)=(I_2\otimes H)|\Phi^+\rangle\). In particular, \(N'\in M_{16}(\mathbb Q)\) is PSD, normalized (\(M_{16}(N')=\operatorname{Tr}(\sigma_{\mathrm{joint}})=1\)), and strictly block-diagonal across RI-08d's four joint cells \(\{C_{00},C_{01},C_{10},C_{11}\}\).*
2. **Projective CP structure, precursor-mark locality, and complete-row normalization:** *Each \(\widehat Q_{A,x,a},\widehat Q_{B,y,b}\in M_4(\mathbb Q)\) is a rank-2 real orthogonal projector (\(\widehat Q^2=\widehat Q=\widehat Q^T\), \(\widehat Q_{\bullet,0}+\widehat Q_{\bullet,1}=I_4\)) with \([\widehat Q_{A,0,0},\widehat Q_{A,1,0}]\ne 0\) and \([\widehat Q_{B,0,0},\widehat Q_{B,1,0}]\ne 0\). Every branch map (10) reads **only** marks inside \(S\) ([`THEOREM_PACKAGE.md` §1](../../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model)), preserves \((J_2\otimes J_2)(\mathrm{PSD}_4(\mathbb C))\) and strict four-cell block-diagonality, and satisfies \(\sum_{S\in\mathcal I(P)}\sum_{c\in\{0,1\}}M_{16}(\mathcal B^{P,r}_{S,c}(N))=M_{16}(N)\) on \((J_2\otimes J_2)(\operatorname{Herm}_4(\mathbb C))\) (and \(\sum_{S,c}\operatorname{Tr}(\mathcal B^{P,r}_{S,c}(N))=\operatorname{Tr}(N)\) on all \(M_{16}(\mathbb C)\)).*
3. **All-horizon \(256\times 256\) superoperator causal diamonds:** *For every marked order \((P,r)\) extending \(P_0\), every pair of ideals \(S,T\in\mathcal I(P)\) (including equal \(S=T\) and nested \(S\subset T\)), and every \((c_1,c_2)\in\{0,1\}^2\),*
   \[
   \boxed{\mathcal B^{P+u_S,r+c_1}_{T,c_2}\circ\mathcal B^{P,r}_{S,c_1}
   = \mathcal B^{P+v_T,r+c_2}_{S,c_1}\circ\mathcal B^{P,r}_{T,c_2}}
   \tag{11}
   \]
   *holds identically as \(256\times 256\) linear superoperators on **all** of \(M_{16}(\mathbb C)\).*
4. **Wingwise repeatability, no-signaling, and \(S_{\mathrm{CHSH}}=14/5>2\):** *Along each wing, consecutive births repeat the committed outcome with certainty (\(\widehat Q_{W,s,c_2}\widehat Q_{W,s,c_1}=\delta_{c_1,c_2}\widehat Q_{W,s,c_1}\)). Across the two incomparable birth histories forming the spacelike diamond order \(P_4^\parallel=\{r_A\prec v_A,\;r_B\prec v_B\}\), the structural order probability is \(P(P_4^\parallel\mid x,y)=\frac1{16}\) (independent of \(x,y\)), the conditional committed-mark distribution \(P(a,b\mid P_4^\parallel,x,y)\) satisfies exact no-signaling \(P(a\mid P_4^\parallel,x,y)=P(b\mid P_4^\parallel,x,y)=\frac12\), and its correlators are*
   \[
   E(0,0)=\frac45,\quad E(0,1)=\frac45,\quad E(1,0)=\frac35,\quad E(1,1)=-\frac35,\qquad
   \boxed{S_{\mathrm{CHSH}}=\frac{14}5>2.}
   \tag{12}
   \]

**Proof.**
*(1)* In Walsh coordinates, \(D_{+X}=J_2(|0\rangle\langle 0|)\) has internal block \(\frac14 H_2|0\rangle\langle 0|H_2=\frac12|+\rangle\langle +|\) and \(R_{t=1}=D_{+Z}=J_2(|+\rangle\langle +|)\) has internal block \(\frac14 H_2|+\rangle\langle +|H_2=\frac12|0\rangle\langle 0|\). Applying RI-08d's coupler \(U=(I_2\otimes H)\mathrm{CNOT}\) sends \(|+,0\rangle\mapsto (I_2\otimes H)|\Phi^+\rangle=|\psi_{\mathrm{joint}}\rangle\), so each joint internal block becomes \(\frac14\sigma_{\mathrm{joint}}\). The normalized operator \(H\otimes H\), with \(H=H_2/\sqrt2\), fixes \(|\psi_{\mathrm{joint}}\rangle\) because \((H\otimes H)(I_2\otimes H)|\Phi^+\rangle=(H\otimes I_2)|\Phi^+\rangle=(I_2\otimes H)|\Phi^+\rangle\). Consequently the corresponding block in \((J_2\otimes J_2)(\sigma_{\mathrm{joint}})\) is \(\frac1{16}(H_2\otimes H_2)\sigma_{\mathrm{joint}}(H_2\otimes H_2)=\frac14\sigma_{\mathrm{joint}}\). (In contrast, \(H_2^{-1}\otimes H_2^{-1}=\frac12(H\otimes H)\) scales the vector by \(1/2\).) Restoring \(V_{2,2}\otimes V_{2,2}\) on both sides therefore yields \(N'=(J_2\otimes J_2)(\sigma_{\mathrm{joint}})\) with the stated normalization.

*(2)* Since \(H_2^2=2I_2\) and \(V_{2,2}^2=I_4\), (7) is a similarity-orthogonal algebra homomorphism \(M_2(\mathbb Q)\to M_4(\mathbb Q)\) sending rank-1 orthogonal projectors summing to \(I_2\) to rank-2 orthogonal projectors summing to \(I_4\), and preserving noncommutativity since \(J_2\) and (7) are injective. By bilinearity of \(J_2\otimes J_2\), \((\widehat K_A\otimes\widehat K_B)(J_2\otimes J_2)(\rho)(\widehat K_A\otimes\widehat K_B)^\dagger=(J_2\otimes J_2)((K_A\otimes K_B)\rho(K_A\otimes K_B)^\dagger)\), which preserves \((J_2\otimes J_2)(\mathrm{PSD}_4(\mathbb C))\) and strict four-cell block-diagonality. Summing over \(c\in\{0,1\}\) uses \(Q_{\bullet,0}^2+Q_{\bullet,1}^2=I_2\) and \(\operatorname{Tr}((Q_0\otimes I_2)\rho(Q_0\otimes I_2)+(Q_1\otimes I_2)\rho(Q_1\otimes I_2))=\operatorname{Tr}(\rho)\), while summing over \(S\in\mathcal I(P)\) multiplies by \(\sum_S q_{1/2}(P,S)=1\).

*(3)* Appending \(u_S\) above \(S\) neither adds nor removes \(r_A\) or \(r_B\) from \(T\subseteq P\), nor alters the immutable root marks \(r(r_A)=x\), \(r(r_B)=y\). For fixed \((x,y)\), the Kraus operators appearing in (10) belong to \(\{I_{16},\;\widehat Q_{A,x,0}\otimes I_4,\;\widehat Q_{A,x,1}\otimes I_4,\;I_4\otimes\widehat Q_{B,y,0},\;I_4\otimes\widehat Q_{B,y,1}\}\), every two of which commute as \(16\times 16\) matrices (same-wing projectors share the fixed axis \(x\) or \(y\) and satisfy \(\widehat Q_{W,s,c_1}\widehat Q_{W,s,c_2}=\delta_{c_1,c_2}\widehat Q_{W,s,c_1}\), while opposite-wing projectors act on disjoint tensor factors). Combining Kraus commutativity with the scalar diamond identity (6) proves (11) on all of \(M_{16}(\mathbb C)\).

*(4)* The order \(P_4^\parallel\) arises from \(P_0\) exclusively via \((S=\{r_A\},\text{ then }T=\{r_B\})\) or \((T=\{r_B\},\text{ then }S=\{r_A\})\). By (5)–(6), each order contributes \(q_{1/2}(P_0,\{r_A\})q_{1/2}(P_0+v_A,\{r_B\})=\frac14\cdot\frac18=\frac1{32}\), summing to \(\frac1{16}\) times \(M_{16}((\widehat Q_{A,x,a}\otimes\widehat Q_{B,y,b})N'(\widehat Q_{A,x,a}\otimes\widehat Q_{B,y,b}))=\operatorname{Tr}((Q_{A,x,a}\otimes Q_{B,y,b})\sigma_{\mathrm{joint}})\). Note \(Q_{A,0,0}-Q_{A,0,1}=X\), \(Q_{A,1,0}-Q_{A,1,1}=Z\), \(Q_{B,0,0}-Q_{B,0,1}=\frac45 Z+\frac35 X\), and \(Q_{B,1,0}-Q_{B,1,1}=\frac45 Z-\frac35 X\). Since \(\sigma_{\mathrm{joint}}\) has \(\langle X\otimes I_2\rangle=\langle I_2\otimes Z\rangle=\langle I_2\otimes X\rangle=\langle Z\otimes I_2\rangle=0\), \(\langle X\otimes Z\rangle=\langle Z\otimes X\rangle=1\), and \(\langle X\otimes X\rangle=\langle Z\otimes Z\rangle=0\), all marginals equal \(\frac12\) and the four correlators equal \((\frac45,\frac45,\frac35,-\frac35)\), giving \(S_{\mathrm{CHSH}}=\frac{14}5\). ∎

### 2.3 Classical-simplex CHSH dichotomy and the 10-state commuting PR-box obstruction

Why is **bipartite subsystem tensor locality** (Wing A acting via \(\mathcal M_A\otimes\mathrm{id}_B\) and Wing B via \(\mathrm{id}_A\otimes\mathcal M_B\), as in (10)) strictly required alongside spacelike superoperator commutation \([\mathcal B_A,\mathcal B_B]=0\)? Theorem 1C resolves this completely on classical simplices \(\mathbb R_+^d\):

**Theorem 1C (Classical-simplex CHSH bound vs unfactorized commuting PR-box countermodel).**
1. **Classical bound under bipartite locality or residual-level no-signaling:** *On every bipartite classical cone \(\mathbb R_+^{d_A}\otimes\mathbb R_+^{d_B}\) (\(d_A,d_B\ge 1\)) with local nonnegative mass-complete instruments \(M^{(A)}_{x,a}\otimes I_{d_B}\) and \(I_{d_A}\otimes M^{(B)}_{y,b}\) (\(\mathbf 1^T(M_{\bullet,0}+M_{\bullet,1})=\mathbf 1^T\))—and even on an **unfactorized** single simplex \(\mathbb R_+^d\) whenever commuting nonnegative instruments \([M^{(A)}_{x,a},M^{(B)}_{y,b}]=0\) satisfy **residual-level no-signaling** \((M^{(B)}_{0,0}+M^{(B)}_{0,1})p_0=(M^{(B)}_{1,0}+M^{(B)}_{1,1})p_0=:\tilde p\) at the initial state \(p_0\in\Delta_d\)—the joint outcome probabilities satisfy \(|S_{\mathrm{CHSH}}|\le 2\).*
2. **Explicit 10-state commuting classical-simplex PR-box when subsystem locality is omitted:** *On the unfactorized 10-state simplex \(\Delta_{10}\subset\mathbb R_+^{10}\) with basis \(\{e_{\mathrm{init}}\}\cup\{e_{\alpha_{x,a}}\}_{x,a\in\{0,1\}}\cup\{e_{\beta_{y,b}}\}_{y,b\in\{0,1\}}\cup\{e_{\mathrm{sink}}\}\), define \(10\times 10\) entrywise-nonnegative matrices \(A_{x,a},B_{y,b}\in\mathbb Q_{\ge 0}^{10\times 10}\) by*
   \[
   \begin{aligned}
   A_{x,a}(e_{\mathrm{init}})&=\tfrac12 e_{\alpha_{x,a}}, &
   A_{x,a}(e_{\alpha_{x',a'}})&=\tfrac12 e_{\alpha_{x',a'}}, &
   A_{x,a}(e_{\beta_{y,b}})&=2P_{\mathrm{PR}}(a,b\mid x,y)\,e_{\mathrm{sink}}, &
   A_{x,a}(e_{\mathrm{sink}})&=\tfrac12 e_{\mathrm{sink}}, \\
   B_{y,b}(e_{\mathrm{init}})&=\tfrac12 e_{\beta_{y,b}}, &
   B_{y,b}(e_{\beta_{y',b'}})&=\tfrac12 e_{\beta_{y',b'}}, &
   B_{y,b}(e_{\alpha_{x,a}})&=2P_{\mathrm{PR}}(a,b\mid x,y)\,e_{\mathrm{sink}}, &
   B_{y,b}(e_{\mathrm{sink}})&=\tfrac12 e_{\mathrm{sink}},
   \end{aligned}
   \tag{13}
   \]
   *where \(P_{\mathrm{PR}}(a,b\mid x,y)=\frac12\mathbf 1_{a\oplus b=xy}\). Then \(\mathbf 1_{10}^T(A_{x,0}+A_{x,1})=\mathbf 1_{10}^T(B_{y,0}+B_{y,1})=\mathbf 1_{10}^T\), **all \(16\) pairs satisfy exact \(10\times 10\) matrix commutativity \([A_{x,a},B_{y,b}]=0\)**, outcome marginals satisfy no-signaling \(P(a\mid x,y)=P(b\mid x,y)=\frac12\), yet on \(p_0=e_{\mathrm{init}}\) the model realizes the Popescu–Rohrlich box with **\(S_{\mathrm{CHSH}}=4\)**.*

**Proof.**
*(1)* The bipartite case \(\mathbb R_+^{d_A}\otimes\mathbb R_+^{d_B}\) follows directly from convex decomposition \(p_0=\sum_\lambda p_\lambda u_\lambda\otimes w_\lambda\) as in [`BRIDGE_THEOREM.md` Theorem 3C(1)](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md). On unfactorized \(\mathbb R_+^d\) with \((M^{(B)}_{0,0}+M^{(B)}_{0,1})p_0=(M^{(B)}_{1,0}+M^{(B)}_{1,1})p_0=\tilde p\in\Delta_d\), define for each coordinate \(k\in\{1,\dots,d\}\) with \(\tilde p_k>0\) the local conditional probabilities \(\alpha_{x,a}(k):=(\mathbf 1_d^T M^{(A)}_{x,a})_k\in[0,1]\) (\(\alpha_{x,0}(k)+\alpha_{x,1}(k)=1\)) and \(\beta_{y,b}(k):=(M^{(B)}_{y,b}p_0)_k/\tilde p_k\in[0,1]\) (\(\beta_{y,0}(k)+\beta_{y,1}(k)=1\) because \(\tilde p\) is independent of \(y\)). Then
\[
p(a_0,a_1,b_0,b_1) := \sum_{k:\tilde p_k>0}\tilde p_k\,\alpha_{0,a_0}(k)\alpha_{1,a_1}(k)\beta_{0,b_0}(k)\beta_{1,b_1}(k)\ge 0
\tag{14}
\]
marginalizes for every \((x,y)\in\{0,1\}^2\) to \(\sum_{k:\tilde p_k>0}\tilde p_k\alpha_{x,a}(k)\beta_{y,b}(k)=\mathbf 1_d^T M^{(A)}_{x,a}M^{(B)}_{y,b}p_0=P(a,b\mid x,y)\), forcing \(|S_{\mathrm{CHSH}}|\le 2\).

*(2)* In (13), nonnegativity and column-sum normalization hold by inspection (\(\sum_{a=0}^1 2P_{\mathrm{PR}}(a,b\mid x,y)=2(\frac12+0)=1\)). Check \(A_{x,a}B_{y,b}=B_{y,b}A_{x,a}\) on all 10 basis vectors: on \(e_{\mathrm{init}}\), both yield \(P_{\mathrm{PR}}(a,b\mid x,y)e_{\mathrm{sink}}\); on \(e_{\alpha_{x',a'}}\), both yield \(P_{\mathrm{PR}}(a',b\mid x',y)e_{\mathrm{sink}}\); on \(e_{\beta_{y',b'}}\), both yield \(P_{\mathrm{PR}}(a,b'\mid x,y')e_{\mathrm{sink}}\); on \(e_{\mathrm{sink}}\), both yield \(\frac14 e_{\mathrm{sink}}\). Thus \([A_{x,a},B_{y,b}]=0\) identically on \(\mathbb R^{10}\), and \(\mathbf 1_{10}^T A_{x,a}B_{y,b}e_{\mathrm{init}}=P_{\mathrm{PR}}(a,b\mid x,y)\), giving \(E(0,0)=E(0,1)=E(1,0)=+1\), \(E(1,1)=-1\), and \(S_{\mathrm{CHSH}}=4\). Notice how (13) evades (14): \((B_{y,0}+B_{y,1})e_{\mathrm{init}}=\frac12(e_{\beta_{y,0}}+e_{\beta_{y,1}})\) depends on \(y\), writing Bob's setting into a nonlocal classical memory slot read by Alice. ∎

---

## 3. Target G2 — Non-Circular Operational Exclusion of Grade-\(\ge 3\) Sorkin Interference

### 3.1 Baseline countermodels: even Pairwise Decoherence Sufficiency does not force \(I_3=0\)

Every set function \(\mu:2^{\Omega_n}\to\mathbb R\) (\(\mu(\varnothing)=0\)) has a unique Möbius expansion \(\mu(A)=\sum_{\varnothing\ne S\subseteq A}w_S\), under which Sorkin's \(k\)-th order interference on disjoint singletons is \(I_k(\{i_1\},\dots,\{i_k\})=w_{\{i_1,\dots,i_k\}}\), and \(\mu\) has grade \(\le 2\) (\(I_m(A_1,\dots,A_m)=0\) for all \(m\ge 3\) and all pairwise disjoint \(A_1,\dots,A_m\subseteq\Omega_n\)) iff \(w_S=0\) for all \(|S|\ge 3\).

**Theorem 2A (Exact grade-3 countermodels refuting naive positivity and pairwise decoherence sufficiency).**
1. **Zero-pairwise-interference countermodel ([`grade2_justification.py`](../../../det8/models/grade2_justification.py)):** *On \(\Omega_4=\{0,1,2,3\}\), \(\mu_1\) with \(w_{\{i\}}=\frac{3}{16}\) (\(i=0,1,2,3\)), \(w_{\{0,1,2\}}=\frac14\), and all other \(w_S=0\) satisfies \(\mu_1(\Omega_4)=1\), \(\mu_1(A)\ge 0\) for all \(A\subseteq\Omega_4\), and \(I_2(\{i\},\{j\})=0\) on **every** singleton pair, yet \(I_3(\{0\},\{1\},\{2\})=\frac14\ne 0\) and \(\sum_{i=0}^3\mu_1(\{i\})=\frac34\ne 1\).*
2. **Masked countermodel surviving singleton completeness and Pairwise Decoherence Sufficiency:** *Say \(\mu\) satisfies **Pairwise Decoherence Sufficiency** if every pairwise-disjoint collection \(\{A_1,\dots,A_k\}\) obeying \(I_2(A_r,A_s)=0\) (\(\forall r\ne s\)) sums classically, \(\mu(\bigsqcup_{r=1}^k A_r)=\sum_{r=1}^k\mu(A_r)\). On \(\Omega_3=\{0,1,2\}\), define \(\mu_{\mathrm{mask}}\) by*
   \[
   w_{\{0\}}=w_{\{1\}}=w_{\{2\}}=\frac13,\quad
   w_{\{0,1\}}=+\frac18,\quad w_{\{0,2\}}=w_{\{1,2\}}=-\frac18,\quad
   w_{\{0,1,2\}}=+\frac18.
   \tag{15}
   \]
   *Then \(\mu_{\mathrm{mask}}(\Omega_3)=1\), \(\mu_{\mathrm{mask}}(A)>0\) for every nonempty \(A\subseteq\Omega_3\), \(\sum_{i=0}^2\mu_{\mathrm{mask}}(\{i\})=1\), and \(\mu_{\mathrm{mask}}\) satisfies Pairwise Decoherence Sufficiency across **every** disjoint family \(\{A_1,\dots,A_k\}\) of nonempty subsets of \(\Omega_3\), yet \(I_3(\{0\},\{1\},\{2\})=\frac18\ne 0\).*

**Proof.** Part (1) is immediate from \(w_{\{i,j\}}=0\). In (15), singletons have weight \(\frac13\) (summing to \(1\)); pairs have weights \(\mu_{\mathrm{mask}}(\{0,1\})=\frac23+\frac18=\frac{19}{24}>0\) and \(\mu_{\mathrm{mask}}(\{0,2\})=\mu_{\mathrm{mask}}(\{1,2\})=\frac23-\frac18=\frac{13}{24}>0\); and \(\mu_{\mathrm{mask}}(\Omega_3)=1+\frac18-\frac18-\frac18+\frac18=1\). Every disjoint singleton pair has \(I_2\in\{\pm\frac18\}\ne 0\), while the three coarse disjoint pairs satisfy \(I_2(\{0,1\},\{2\})=w_{\{0,2\}}+w_{\{1,2\}}+w_{\{0,1,2\}}=-\frac18\ne 0\) and \(I_2(\{0,2\},\{1\})=I_2(\{1,2\},\{0\})=+\frac18\ne 0\). Thus no nontrivial disjoint collection on \(\Omega_3\) is pairwise non-interfering, so Pairwise Decoherence Sufficiency holds without exception while \(I_3(\{0\},\{1\},\{2\})=w_{\{0,1,2\}}=\frac18\ne 0\). ∎

### 3.2 Route I: Homogeneous slit-amplitude scaling, signed-phase positivity, and one Pythagorean rotation

**Theorem 2B (Selection of degree \(k=2\) and \(I_{\ge 3}\equiv 0\) from amplitude scaling and rotated partition conservation).** *Let \(\mathcal F_n\) (\(n\ge 2\)) be a non-zero family of polynomial throughput functionals \(F:\mathbb R^n\to\mathbb R\) mapping diagonal slit-amplitude multipliers \(a=(a_0,\dots,a_{n-1})^T\in\mathbb R^n\) to total throughput weight \(F(a)\), recovering Boolean event weights on \(0\)-\(1\) slit masks via \(\mu_F(A):=F(\chi_A)\). Suppose:*
1. **Degree-\(k\) scale homogeneity:** *There is an integer \(k\ge 1\) such that \(F(\lambda a)=\lambda^k F(a)\) for all \(F\in\mathcal F_n\), \(\lambda\in\mathbb R\), and \(a\in\mathbb R^n\);*
2. **Signed-amplitude positivity:** *\(F(a)\ge 0\) for all \(F\in\mathcal F_n\) and \(a\in\mathbb R^n\) (in particular under phase-flip sign reversal \(a\mapsto -a\));*
3. **Single Pythagorean silent rotation & two-cell partition conservation:** *\(\mathcal F_n\) contains the localized unit cell-\(0\) functional \(F_{e_0}(a)=a_0^k\) and is closed under at least one nontrivial two-cell orthogonal rotation \(O_\theta=\bigl(\begin{smallmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{smallmatrix}\bigr)\oplus I_{n-2}\) (\(\cos\theta\sin\theta\ne 0\), e.g., the exact rational \((3,4,5)\) rotation \(\cos\theta=\frac35,\sin\theta=\frac45\)) acting by \((O_\theta\cdot F)(a):=F(O_\theta^T a)\), such that the rotated state \(F_\theta=O_\theta\cdot F_{e_0}\) conserves unit probability across \(\{0\}\sqcup\{1\}\): \(\mu_{F_\theta}(\{0\})+\mu_{F_\theta}(\{1\})=1\).*

*Then:*
- *(i)* \(k=2\) *uniquely;*
- *(ii)* *Every \(F\in\mathcal F_n\) is a homogeneous quadratic form \(F(a)=a^T R a\) (\(R\in\operatorname{Sym}_n(\mathbb R)\)) whose induced Boolean set function \(\mu_F(A)=\sum_{i\in A}R_{ii}+2\sum_{\{i,j\}\subseteq A,\,i<j}R_{ij}\) has **exact Sorkin grade \(\le 2\)** (\(I_m(A_1,\dots,A_m)=0\) for all \(m\ge 3\) and all pairwise disjoint \(A_1,\dots,A_m\subseteq\Omega_n\));*
- *(iii)* **Quartic countermodel when (3) is omitted:** *The degree-4 functional \(F_4(a)=\bigl(\frac{a_0+a_1+a_2}{3}\bigr)^4\) on \(\mathbb R^3\) satisfies (1), (2), and \(F_4(\mathbf 1_3)=1\), fails (3) (\((\frac9{25})^2+(\frac{16}{25})^2=\frac{337}{625}\ne 1\)), and induces \(I_3(\{0\},\{1\},\{2\})=\frac49\ne 0\).*

**Proof.** Pick \(F\in\mathcal F_n\) and \(a_*\in\mathbb R^n\) with \(F(a_*)>0\) (guaranteed by \(F_{e_0}(e_0)=1>0\)). By (1)–(2), \(0\le F(-a_*)=(-1)^k F(a_*)\), forcing \(k=2r\) (\(r\in\mathbb Z_{\ge 1}\)) to be even. Evaluating \(F_\theta(a)=F_{e_0}(O_\theta^T a)=(a_0\cos\theta+a_1\sin\theta)^{2r}\) at \(\chi_{\{0\}}=e_0\) and \(\chi_{\{1\}}=e_1\) gives
\[
\mu_{F_\theta}(\{0\})+\mu_{F_\theta}(\{1\}) = p^r + (1-p)^r = 1,\qquad p:=\cos^2\theta\in(0,1)\quad\left(p=\tfrac{9}{25}\text{ for }(3,4,5)\right).
\tag{16}
\]
Because \(0<p<1\), every \(r\ge 2\) satisfies \(p^r<p\) and \((1-p)^r<1-p\), so \(p^r+(1-p)^r<p+(1-p)=1\). Hence (16) holds iff \(r=1\), i.e., \(k=2\), proving *(i)*. Every homogeneous degree-2 polynomial on \(\mathbb R^n\) has the form \(F(a)=\sum_{i,j=0}^{n-1}R_{ij}a_i a_j\) with \(R_{ij}=R_{ji}\). On Boolean vectors \(\chi_A\in\{0,1\}^n\), \(\chi_A(i)^2=\chi_A(i)\) yields \(\mu_F(A)=\sum_{i\in A}R_{ii}+\sum_{\{i,j\}\subseteq A,\,i<j}2R_{ij}\), whose Möbius coefficients vanish identically for all \(|S|\ge 3\), proving *(ii)*. In *(iii)*, \(F_4(\chi_A)=(|A|/3)^4\) gives \(1-3(\frac{16}{81})+3(\frac1{81})=\frac{36}{81}=\frac49\). ∎

### 3.3 Route II: Sorkin-hierarchy composite dimension multiplicativity

Independently of slit-amplitude scaling, composite dimension multiplicativity constrains the polynomial dimension and its binomial coefficients. It does not determine a positive cone, effects, composition law, or a classical/complex quantum theory:

**Theorem 2C (Polynomial dimension and Stirling-coefficient selection under composite multiplicativity).** *Suppose an \(m\)-grade Sorkin operational state theory (\(m\ge 1\)) assigns to each \(n\)-cell carrier \(\Omega_n\) (\(n\ge 1\)) an unnormalized real linear state space \(V_n\) of dimension*
\[
d(n) := \dim_{\mathbb R}(V_n) = \sum_{r=1}^{m} c_r \binom{n}{r},\qquad c_1=1,\quad c_r\in\mathbb Z_{\ge 0}\ \ (2\le r\le m),
\tag{17}
\]
*satisfying composite dimension multiplicativity \(d(n_1 n_2)=d(n_1)d(n_2)\) for all \(n_1,n_2\ge 1\). Then:*
1. *There exists an integer \(r_0\in\{1,\dots,m\}\) such that \(d(n)=n^{r_0}\) for all \(n\ge 1\), with unique coefficients \(c_r=r!\,S(r_0,r)\) for \(1\le r\le r_0\) and \(c_r=0\) for \(r>r_0\), where \(S(r_0,r)\) are the Stirling numbers of the second kind.*
2. *No purely real Möbius measure hierarchy (\(c_1=c_2=\dots=c_m=1\), \(d_{\text{Möbius},m}(n)=\sum_{r=1}^m\binom n r\)) satisfies composite multiplicativity for any \(m\ge 2\).*
3. *Under the additional supplied bound \(d(2)\le 4\) (motivated by the restricted single-system quotient in [`RELATIONAL_IDENTITY_BRIDGE.md` §3](../t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md), whose transfer to this hierarchy must be assumed), \(2^{r_0}=d(2)\le 4\) forces \(r_0\in\{1,2\}\), leaving exclusively:*
   - *\(r_0=1\): \(c_1=1\), \(c_{\ge 2}=0\), \(d(n)=n\) (**dimension and coefficient pattern only**, with no cone identified); or*
   - *\(r_0=2\): \(c_1=1\), \(c_2=2\), \(c_{\ge 3}=0\), \(d(n)=n+2\binom n 2=n^2\) (**dimension and coefficient pattern only**, matching the dimension of \(\operatorname{Herm}_n(\mathbb C)\) but not establishing its positive cone, effects, or operational equivalence).*

**Proof.**
*(1)* By (17), \(d(x)\in\mathbb Q[x]\) is a nonzero polynomial of degree \(r_0\in\{1,\dots,m\}\) with \(d(1)=c_1=1\). Write \(d(x)=a_{r_0}x^{r_0}+a_s x^s+\dots\) where \(a_{r_0}\ne 0\) and \(s<r_0\) is the next highest degree with \(a_s\ne 0\) (if one exists). Because \(d(2n)=d(2)d(n)\) holds for every integer \(n\ge 1\), \(d(2x)=d(2)d(x)\) holds identically in \(\mathbb Q[x]\): matching \(x^{r_0}\) gives \(d(2)=2^{r_0}\), and matching \(x^s\) gives \(2^s a_s=2^{r_0}a_s\), impossible for \(s<r_0\) and \(a_s\ne 0\). Hence \(d(x)=a_{r_0}x^{r_0}\), and \(d(1)=1\) forces \(a_{r_0}=1\), so \(d(n)=n^{r_0}\). Expanding \(n^{r_0}=\sum_{r=1}^{r_0}r!\,S(r_0,r)\binom n r\) in the linearly independent polynomial basis \(\{\binom x r\}_{r\ge 1}\) uniquely identifies \(c_r=r!\,S(r_0,r)\) (\(r\le r_0\)) and \(c_r=0\) (\(r>r_0\)).

*(2)* For \(r_0\ge 2\), \(c_2=2!\,S(r_0,2)=2(2^{r_0-1}-1)\ge 2\ne 1\), so \(c_r\equiv 1\) fails already at \(n_1=n_2=2\) (\(3^2=9\ne d_{\text{Möbius},m}(4)\in\{10,14,15\}\)).

*(3)* \(2^{r_0}=d(2)\le 4\) forces \(r_0\in\{1,2\}\); \(r_0=1\) gives \(c_1=1,c_{\ge 2}=0\), and \(r_0=2\) gives \(c_1=1!\,S(2,1)=1\), \(c_2=2!\,S(2,2)=2\), \(c_{\ge 3}=0\). ∎

---

## 4. Target G3 — Selective Post-Commitment Lüders Update on Degenerate (`rank >= 2`) Subspaces

### 4.1 Degenerate repeat faces and coherence-destroying countermodels on the 12-label qutrit Walsh section

In [RI-08c](../t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md), rank-1 Pauli effects had one-dimensional exposed repeat faces \(F_e=\mathbb R_{\ge 0}h\), so cone positivity, effect calibration, and repeatability uniquely forced \(B(x)=e(x)h\). On carriers with \(n\ge 3\) coarse cells, grouping two or more cells produces a **degenerate (`rank >= 2`) subspace** where exposed-ray uniqueness fails:

**Theorem 3A (Non-uniqueness of repeatable instruments and literal-cut dark payload on degenerate qutrit cells).** *Let \(\mathcal C_{12,0}:=J_3(\mathrm{PSD}_3(\mathbb C))\subset\operatorname{Herm}_{12}(\mathbb C)\) be the 12-label qutrit Walsh section (\(L=4\), coarse cells \(C_0=\{0..3\},C_1=\{4..7\},C_2=\{8..11\}\), total-entry mass \(M_{12}(J_3(\rho))=\operatorname{Tr}(\rho)\)), and consider the coarse binary grouping \(\{C_{01}:=C_0\sqcup C_1,\;C_2\}\) with effect \(e_{01}(J_3(\rho))=\mu_{J_3(\rho)}(C_0)+\mu_{J_3(\rho)}(C_1)=\operatorname{Tr}(P_{01}\rho)\), \(P_{01}=\operatorname{diag}(1,1,0)\).*

1. **Four-dimensional repeat face:** *The repeat face \(F_{01}=\{x\in\mathcal C_{12,0}:e_{01}(x)=M_{12}(x)\}=J_3(P_{01}\mathrm{PSD}_3(\mathbb C)P_{01})\cong\mathrm{PSD}_2(\mathbb C)\) has real span dimension \(4>1\).*
2. **Coherence-destroying repeatable resets:** *Both the maximally-mixed reset \(\mathcal T_{01}^{\mathrm{mix}}(J_3(\rho)):=\operatorname{Tr}(P_{01}\rho)\,J_3(\frac12 P_{01})\) and the fine-cell dephasing map \(\mathcal T_{01}^{\mathrm{deph}}(J_3(\rho)):=J_3(P_0\rho P_0+P_1\rho P_1)\) (\(P_a=|a\rangle\langle a|\)) are completely positive, map \(\mathcal C_{12,0}\to\mathcal C_{12,0}\), and satisfy exact effect calibration \(M_{12}(\mathcal T(x))=e_{01}(x)\) and perfect repeatability \(e_{01}(\mathcal T(x))=M_{12}(\mathcal T(x))\), yet erase superposition coherence on \(\rho_{+01}=\frac12(|0\rangle+|1\rangle)(\langle 0|+\langle 1|)\) (giving post-Pythagorean-rotation cell-\(C_0\) probability \(\frac12\), versus \(\frac{49}{50}\) for Lüders projection).*
3. **Literal 12-label cut failure:** *The literal coarse-cell cut \(\mathsf C_{01}(X)=\Pi_{C_{01}}X\Pi_{C_{01}}\) (\(\Pi_{C_{01}}=\operatorname{diag}(I_8,0_4)\)) leaves \(\operatorname{span}_{\mathbb R}(\mathcal C_{12,0})\) and maps \(J_3(|2\rangle\langle 2|)\) (\(e_{01}=0\)) to a **nonzero** PSD matrix with zero total-entry mass \(M_{12}=0\).*

**Proof.** *(1)* \(e_{01}(J_3(\rho))=M_{12}(J_3(\rho))\iff\rho_{22}=0\iff\rho=P_{01}\rho P_{01}\) for \(\rho\succeq 0\), spanning \(\operatorname{Herm}_2(\mathbb C)\oplus 0\) (\(\dim_{\mathbb R}=4\)) via the injective map \(J_3\). *(2)* Direct trace evaluation gives \(M_{12}(\mathcal T_{01}^{\mathrm{mix}}(J_3(\rho)))=\rho_{00}+\rho_{11}=e_{01}(J_3(\rho))\) and similarly for \(\mathcal T_{01}^{\mathrm{deph}}\). Under the lifted Pythagorean subspace unitary \(\mathcal W^R_{01}\) (\(\frac15\bigl(\begin{smallmatrix}3&4\\-4&3\end{smallmatrix}\bigr)\oplus[1]\)), \(J_3(\rho_{+01})\) yields cell-\(C_0\) weight \(\frac1{25}(3\cdot\frac1{\sqrt 2}+4\cdot\frac1{\sqrt 2})^2=\frac{49}{50}\), whereas \(\frac12 P_{01}\) yields \(\frac{9+16}{50}=\frac12\). *(3)* Every \(J_3(\rho)\) has three non-zero \(4\times 4\) blocks congruent to the *same* \(\widetilde\rho=\frac1{16}H_4\operatorname{diag}(\rho,0)H_4\); zeroing cell \(C_2\) while retaining \(\widetilde{|2\rangle\langle 2|}\ne 0\) inside \(C_0\) and \(C_1\) leaves \(\operatorname{span}(J_3)\) while \(\mathbf 1_4^T\Omega_a\widetilde{|2\rangle\langle 2|}\Omega_a\mathbf 1_4=\delta_{a,2}=0\) for \(a\in\{0,1\}\), giving \(M_{12}=0\). ∎

### 4.2 Pure 1-positivity derivation of the exact Lüders rule for arbitrary rank \(1\le d\le n\)

Continuing [RI-08c](../t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md)'s non-smuggling principle (*"No Kraus or Lüders update is inserted as a premise"*), we now prove that **1-positivity alone** (cone positivity \(\Phi(\mathrm{PSD}_n)\subseteq\mathrm{PSD}_n\), without assuming complete positivity or Kraus operators), combined with effect calibration and non-disturbance on states *already* certain on the outcome face \(F_P\), uniquely forces the exact **Lüders selective update** \(\Phi(\rho)=P\rho P\) across the entire Hermitian space—including all off-diagonal coherences between \(\operatorname{ran}(P)\) and \(\operatorname{ran}(I_n-P)\):

**Theorem 3B (Lüders uniqueness for arbitrary projectors and dyadic Walsh lift for coordinate projectors).** *Let \(n\ge 2\), let \(P=P^\dagger=P^2\in\operatorname{Herm}_n(\mathbb C)\) be any orthogonal projector of rank \(d\in\{1,\dots,n\}\) (\(P_\perp:=I_n-P\)), and let \(\Phi:\operatorname{Herm}_n(\mathbb C)\to\operatorname{Herm}_n(\mathbb C)\) be any real-linear map satisfying:*
1. **1-Positivity (cone positivity):** *\(\rho\in\mathrm{PSD}_n(\mathbb C)\implies\Phi(\rho)\in\mathrm{PSD}_n(\mathbb C)\);*
2. **Effect calibration:** *\(\operatorname{Tr}(\Phi(\rho))=\operatorname{Tr}(P\rho)\) for all \(\rho\in\mathrm{PSD}_n(\mathbb C)\);*
3. **Repeat-face non-disturbance:** *\(\Phi(\sigma)=\sigma\) whenever \(\sigma\in\mathrm{PSD}_n(\mathbb C)\) satisfies \(\operatorname{Tr}(P\sigma)=\operatorname{Tr}(\sigma)\).*

*Then:*
1. **Exact Lüders uniqueness:** *\(\Phi(\rho)=P\rho P\) for **every** \(\rho\in\operatorname{Herm}_n(\mathbb C)\) (and perfect repeatability \(\operatorname{Tr}(P\Phi(\rho))=\operatorname{Tr}(\Phi(\rho))\) follows automatically).*
2. **Operational equivalence via compatible subspace tests:** *On \(\mathcal C_{12,0}=J_3(\mathrm{PSD}_3(\mathbb C))\) with \(P=P_{01}=\operatorname{diag}(1,1,0)\), Condition (3) for \(\mathcal T_{01}(J_3(\rho))=J_3(\Phi(\rho))\) holds if and only if committing \(C_{01}\) on states already satisfying \(e_{01}(x)=M_{12}(x)\) preserves repeatability \(e_{01}(\mathcal T_{01}(x))=M_{12}(x)\) and leaves finer-cell weights \(\mu(\{C_0,C_1\})\) invariant after the three finite subspace silent controls \(\{\mathcal I,\;\mathcal W^{R,\mathrm{Pyth}}_{01},\;\mathcal W^{I,\mathrm{Pyth}}_{01}\}\).*
3. **Exact dyadic-rational Walsh-section lift:** *For any coarse cell subset \(R\subseteq\{0,\dots,n-1\}\) (\(P_R=\sum_{a\in R}|a\rangle\langle a|\), \(P_{R,\mathrm{pad}}=\operatorname{diag}(P_R,0_{L-n})\)), the single matrix*
   \[
   \widehat P_R := V_{n,L}\Bigl(I_n\otimes\bigl(\tfrac1L H_L P_{R,\mathrm{pad}}H_L\bigr)\Bigr)V_{n,L}\in M_{nL}\bigl(\mathbb Z[1/2]\bigr)
   \tag{18}
   \]
   *is a real symmetric orthogonal projector (\(\widehat P_R^2=\widehat P_R=\widehat P_R^T\), \(\operatorname{rank}(\widehat P_R)=n|R|\)) satisfying \(\widehat P_R J_n(\rho)\widehat P_R=J_n(P_R\rho P_R)\) identically on all \(\rho\in\operatorname{Herm}_n(\mathbb C)\).*

**Proof.**
*(1)* Let \(|\chi\rangle\in\operatorname{ran}(P_\perp)\), so \(P|\chi\rangle=0\). Since \(|\chi\rangle\langle\chi|\succeq 0\), Condition (1) gives \(\Phi(|\chi\rangle\langle\chi|)\succeq 0\) and Condition (2) gives \(\operatorname{Tr}(\Phi(|\chi\rangle\langle\chi|))=\operatorname{Tr}(P|\chi\rangle\langle\chi|)=0\); a trace-zero PSD matrix vanishes, so \(\Phi(|\chi\rangle\langle\chi|)=0\). Because rank-1 projectors in \(\operatorname{ran}(P_\perp)\) span \(P_\perp\operatorname{Herm}_n(\mathbb C)P_\perp\) over \(\mathbb R\), real linearity yields \(\Phi(P_\perp\rho P_\perp)=0\) for all \(\rho\in\operatorname{Herm}_n(\mathbb C)\). Likewise, every \(\sigma\in P\,\mathrm{PSD}_n(\mathbb C)\,P\) satisfies \(\operatorname{Tr}(P\sigma)=\operatorname{Tr}(\sigma)\), so Condition (3) and real-linear spanning of \(P\,\mathrm{PSD}_n(\mathbb C)\,P\) in \(P\operatorname{Herm}_n(\mathbb C)P\) give \(\Phi(P\rho P)=P\rho P\) for all \(\rho\).

Now fix arbitrary vectors \(|\psi\rangle\in\operatorname{ran}(P)\) and \(|\chi\rangle\in\operatorname{ran}(P_\perp)\). For every scalar \(t\in\mathbb R\), the rank-1 matrix
\[
\rho(t) := \bigl(t|\psi\rangle+|\chi\rangle\bigr)\bigl(t\langle\psi|+\langle\chi|\bigr)
= t^2|\psi\rangle\langle\psi| + t\bigl(|\psi\rangle\langle\chi|+|\chi\rangle\langle\psi|\bigr) + |\chi\rangle\langle\chi|
\tag{19}
\]
lies in \(\mathrm{PSD}_n(\mathbb C)\). Applying \(\Phi\) and substituting \(\Phi(|\psi\rangle\langle\psi|)=|\psi\rangle\langle\psi|\) and \(\Phi(|\chi\rangle\langle\chi|)=0\) gives
\[
\Phi(\rho(t)) = t^2|\psi\rangle\langle\psi| + t\,X \succeq 0 \qquad\text{for all }t\in\mathbb R,\qquad
X := \Phi\bigl(|\psi\rangle\langle\chi|+|\chi\rangle\langle\psi|\bigr)\in\operatorname{Herm}_n(\mathbb C).
\tag{20}
\]
For every vector \(|w\rangle\in\mathbb C^n\), (20) requires the real quadratic polynomial \(|\langle w|\psi\rangle|^2 t^2 + \langle w|X|w\rangle t\ge 0\) for all \(t\in\mathbb R\). A quadratic \(at^2+bt\ge 0\) (\(\forall t\in\mathbb R\)) with zero constant term has discriminant \(b^2-4a\cdot 0=b^2\le 0\), forcing \(b=\langle w|X|w\rangle=0\) for every \(|w\rangle\in\mathbb C^n\). Since \(X\) is Hermitian, \(X=0\). Replacing \(|\chi\rangle\) by \(i|\chi\rangle\in\operatorname{ran}(P_\perp)\) identically yields \(\Phi(-i|\psi\rangle\langle\chi|+i|\chi\rangle\langle\psi|)=0\). Spanning \(P\operatorname{Herm}_n(\mathbb C)P_\perp+P_\perp\operatorname{Herm}_n(\mathbb C)P\) over \(\mathbb R\) gives \(\Phi(P\rho P_\perp+P_\perp\rho P)=0\), so
\[
\Phi(\rho) = \Phi(P\rho P) + \Phi(P\rho P_\perp+P_\perp\rho P) + \Phi(P_\perp\rho P_\perp) = P\rho P + 0 + 0 = P\rho P.
\]

*(2)–(3)* On \(F_{01}=J_3(P_{01}\mathrm{PSD}_3(\mathbb C)P_{01})\), repeatability forces \(\Phi(\sigma)\in P_{01}\mathrm{PSD}_3(\mathbb C)P_{01}\), where the four coarse-cell functionals \((\sigma_{00},\sigma_{11},(9\sigma_{00}+16\sigma_{11}+24\operatorname{Re}\sigma_{01})/25,(9\sigma_{00}+16\sigma_{11}+24\operatorname{Im}\sigma_{01})/25)\) are linearly independent (rank \(4\)), fixing \(\Phi(\sigma)=\sigma\). Equation (18) has entries in \(\mathbb Z[1/2]\) because \(1/L=2^{-p}\in\mathbb Z[1/2]\), satisfies \(\widehat P_R^2=\widehat P_R=\widehat P_R^T\) via \(H_L^2=LI_L\) and \(V_{n,L}^2=I_{nL}\), and conjugates \(J_n(\rho)\) directly to \(J_n(P_R\rho P_R)\). ∎

**Theorem 3C (Necessity of subspace silent controls).** *If the three-control condition in Theorem 3B(2) is weakened on \(F_{01}\) to preserving only the unrotated finer coarse-cell weights \(\mu(C_0)\) and \(\mu(C_1)\) (omitting subspace silent controls), then \(\mathcal T_{01}^{\mathrm{deph}}(J_3(\rho))=J_3(P_0\rho P_0+P_1\rho P_1)\) satisfies cone positivity, calibration, repeatability, and finer-cell weight preservation across all \(\rho\in\mathrm{PSD}_3(\mathbb C)\) while failing Lüders uniqueness.*

**Proof.** On every \(\rho\), \((P_0\rho P_0+P_1\rho P_1)_{aa}=\rho_{aa}\) for \(a\in\{0,1\}\) while \((P_0\rho P_0+P_1\rho P_1)_{01}=0\ne\rho_{01}\). ∎

---

## 5. Target G4 — Minor-Catalogue Copy Bound and Single-Copy Acquisition on the Walsh Section

### 5.1 Sharp copy bound for the principal-minor sign catalogue across all \(n\ge 2\)

**Theorem 4A (Declared minor-sign catalogue and universal \((n-1)\)-copy minor-truncation obstruction).**
1. **Uncoupled / unseeded all-copy blind spot (\(\forall m\ge 1\)):** *Without \(\sim_{\mathscr T}\)-lifted couplers or silent controls, coarse product-cell weights on \(J_n(D)^{\otimes m}\) equal \(D_{a_1a_1}\cdots D_{a_ma_m}\) (blind to all off-diagonal entries), while on unencoded \(D_+=\frac16(J_3-I_3)\) (\(M_3(D_+)=1\), \(2\times 2\) principal minors \(-\frac1{36}<0\), \(D_+\not\succeq 0\)) every tensor power \(D_+^{\otimes m}\) is entrywise nonnegative and satisfies \(\mu_{D_+^{\otimes m}}(E)\ge 0\) on all \(2^{3^m}\) Boolean events for every \(m\ge 1\).*
2. **Universal \((n-1)\)-copy minor-truncation obstruction (\(\forall n\ge 2\)):** *Let \(T_n\in\operatorname{Skew}_n(\mathbb R)\) be the skew-symmetric tournament matrix \((T_n)_{ab}=\operatorname{sgn}(b-a)\) (\(a\ne b\)), \((T_n)_{aa}=0\), for which \(\Lambda_m:=\lambda_{\max}(iT_m)=\cot(\frac{\pi}{2m})\) is strictly increasing in \(m\ge 1\) (\(\Lambda_1=0<\Lambda_2=1<\Lambda_3=\sqrt 3<\Lambda_4=\sqrt 2+1<\cdots\)). For **every** \(n\ge 2\) and any rational \(t_n\in\mathbb Q\) satisfying*
   \[
   t_2>\frac12\quad(n=2),\qquad
   \frac{1}{n\Lambda_n}<t_n<\frac{1}{n\Lambda_{n-1}}\quad(n\ge3)
   \qquad\left(\text{e.g. } t_2=\tfrac35,\ t_3=\tfrac14,\ t_4=\tfrac18,\ t_5=\tfrac1{13}\right).
   \tag{21}
   \]
   *the Gaussian-rational Hermitian kernel \(D^{(n)}_{\mathrm{imag}}(t_n):=\frac1n I_n+it_n T_n\in\operatorname{Herm}_n(\mathbb Q(i))\) satisfies:*
   - *(a)* \(\operatorname{Tr}(D^{(n)}_{\mathrm{imag}})=1\), \(M_n(D^{(n)}_{\mathrm{imag}})=1\), *and uniform single-copy Boolean weights \(\mu(A)=|A|/n\ge 0\) for all \(A\subseteq\Omega_n\);*
   - *(b)* ***every** nonempty proper principal submatrix \((D^{(n)}_{\mathrm{imag}})_I\) of size \(1\le |I|\le n-1\) (all \(2^n-2\) proper subsets \(I\)) is **strictly positive definite**, so every coarse-cell minor readout \(\mu_{K_I}(C_*)=\frac{|I|!}{2^k}\det((D^{(n)}_{\mathrm{imag}})_I)>0\) using \(m\le n-1\) copies in Theorem 1A of [`RELATIONAL_IDENTITY_BRIDGE.md`](../t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md) is strictly positive;*
   - *(c)* *yet \(D^{(n)}_{\mathrm{imag}}(t_n)\) has **strictly negative top determinant** \(\det(D^{(n)}_{\mathrm{imag}}(t_n))<0\) (\(-\frac{11}{100},-\frac{11}{432},-\frac{7}{4096},-\frac{10564}{89253125}\) for \(n=2,3,4,5\)) and is non-PSD.*
3. **Single-copy fixed-menu polyhedral sign blindness:** *For any finite single-copy menu of bounded PSD effects \(\{E_1,\dots,E_N\}\subset\mathrm{PSD}_n(\mathbb C)\) (\(0\preceq E_r\preceq I_n\), \(n\ge 2\)), the sign constraints \(\operatorname{Tr}(DE_r)\ge 0\) define a polyhedron in the trace-one affine space \(\operatorname{Herm}_n^1(\mathbb C)\) strictly containing the non-polyhedral set \(\mathrm{PSD}_n^1(\mathbb C)\); in particular, [RI-23](../../coordination/SCALAR_VALUE_ERROR_CONTRACT.md)'s non-PSD matrix \(D_*\) produces strictly positive single-copy probabilities in \([\frac1{10},\frac45]\subset(0,1)\) across all \(n^2=9\) tomographic settings below.*

**Proof.**
*(1)* Entrywise nonnegativity is preserved under Kronecker powers.

*(2)* Because \(\operatorname{Re}(D^{(n)}_{\mathrm{imag}})=\frac1n I_n\) and \(\mathbf 1_A^T T_n\mathbf 1_A=0\) for every real indicator \(\mathbf 1_A\), *(a)* holds. If \(I=\{i_0<\dots<i_{m-1}\}\), then \((T_n)_I=T_m\) in the inherited order.

For \(m\ge1\) and \(0\le r<m\), put \(\theta_r=(2r+1)\pi/m\), \(z_r=e^{-i\theta_r}\), and \(v_{r,j}=z_r^j\) for \(0\le j<m\). Here \(z_r^m=-1\) and \(z_r\ne1\). Direct finite geometric summation gives
\[
(T_m v_r)_j
=\sum_{b=j+1}^{m-1}z_r^b-\sum_{b=0}^{j-1}z_r^b
=\frac{z_r^{j+1}-z_r^m-1+z_r^j}{1-z_r}
=\frac{1+z_r}{1-z_r}z_r^j,
\]
and therefore
\[
(iT_m)v_r=\lambda_r(m)v_r,\qquad
\lambda_r(m)=i\frac{1+z_r}{1-z_r}
=\cot\!\left(\frac{(2r+1)\pi}{2m}\right).
\]
These \(m\) eigenvalues are distinct, since cotangent is strictly decreasing on \((0,\pi)\), so they give the full spectrum. Its extrema are \(\lambda_0(m)=\Lambda_m\) and \(\lambda_{m-1}(m)=-\Lambda_m\). The number \(\Lambda_m=\cot(\pi/(2m))\) is strictly increasing, with \(\Lambda_1=0\). For \(n\ge3\), (21) specifies a nonempty open interval, hence admits rational \(t_n\). Every proper submatrix of size \(m<n\) then has minimum eigenvalue
\[
\frac1n-t_n\Lambda_m\ \ge\ \frac1n-t_n\Lambda_{n-1}\ >0,
\]
proving *(b)*. The full matrix has the negative eigenvalue \(\frac1n-t_n\Lambda_n<0\), coming from \(v_{n-1}\), not \(v_0\).

There is exactly one nonpositive eigenvalue. Indeed, fix any coordinate principal subspace of dimension \(n-1\); the preceding paragraph shows that the quadratic form is strictly positive on it. If the full matrix had two nonpositive eigenvalues, the span of their eigenvectors would be a two-dimensional subspace on which the quadratic form is nonpositive. This subspace would intersect the coordinate principal subspace nontrivially, a contradiction. Thus the one negative eigenvalue already found is the only nonpositive eigenvalue, and all other eigenvalues are strictly positive. Their product is strictly negative, proving *(c)* for \(n\ge3\). This is the usual principal-subspace interlacing argument, and does not require the false bound on absolute values of all non-leading eigenvalues in the original revision.

For \(n=2\), handle the case directly: \(D=\bigl(\begin{smallmatrix}1/2&it_2\\-it_2&1/2\end{smallmatrix}\bigr)\) has eigenvalues \(1/2\pm t_2\). Any rational \(t_2>1/2\) gives one negative and one positive eigenvalue, while each proper principal submatrix is \([1/2]\). No division by \(\Lambda_1=0\) is used. These conclusions establish the copy bound for the specified principal-minor sign catalogue; they do not exclude every possible measurement strategy with fewer copies.

*(3)* The normalized qubit slice \(\{\frac12(I_2+yY+zZ)\oplus 0_{n-2}:y^2+z^2\le 1\}\subset\mathrm{PSD}_n^1(\mathbb C)\) is a Euclidean disk in \(\mathbb R^2\); finitely many linear inequalities \(\operatorname{Tr}(DE_r)\ge 0\) cut out a polygon containing the disk, which strictly contains rational exterior points whenever bounded (or an unbounded ray otherwise). ∎

### 5.2 Single-copy probability acquisition on the Walsh section; the raw RI-23 obstruction remains

In [RI-23 §6](../../coordination/SCALAR_VALUE_ERROR_CONTRACT.md), any PSD test \(T\) obeying \(0\le\operatorname{Tr}(DT)\le M_n(D)=\operatorname{Tr}(D\mathbf 1_n\mathbf 1_n^\dagger)\) across the raw PSD domain \(K_n\) had to vanish on \(\ker(\mathbf 1_n^\dagger)\), forcing \(T=a\mathbf 1_n\mathbf 1_n^\dagger\) (rank \(\le 1\)), while RI-23's unscaled off-diagonal probes \(T_{e_i+e_j}\) had operator norm \(2>1\). On the separately supplied Walsh section \(J_n(D)\), with its trace mass and admitted controls, a probability catalogue is available using single-copy (`m = 1`), zero-ancilla, square-root-free Gaussian-rational unitary silent controls:

**Theorem 4B (Single-copy Gaussian-rational probability catalogue, exact inverse, and deterministic certificates on \(J_n(D)\)).** *Fix any \(n\ge 2\) (\(L=2^{\lceil\log_2 n\rceil}\)). For each pair \(0\le i<j<n\), define \(U^R_{ij},U^I_{ij}\in U(L,\mathbb Q(i))\) acting as the identity on all coordinates outside \(\{i,j\}\) (including all padded coordinates \(\ge n\)) and on \(\{i,j\}\) by the exact Pythagorean Gaussian-rational unitaries*
\[
U^R_{ij}\big|_{\{i,j\}} = \frac15\begin{pmatrix}3&4\\-4&3\end{pmatrix},\qquad
U^I_{ij}\big|_{\{i,j\}} = \frac15\begin{pmatrix}3&4i\\4i&3\end{pmatrix},
\tag{22}
\]
*and lift them to \(\Omega_{nL}\) via \(\mathcal W^{R,\mathrm{Pyth}}_{ij}:=V_{n,L}(I_n\otimes\frac1L H_L U^R_{ij}H_L)V_{n,L}\in U(nL,\mathbb Q)\) and \(\mathcal W^{I,\mathrm{Pyth}}_{ij}:=V_{n,L}(I_n\otimes\frac1L H_L U^I_{ij}H_L)V_{n,L}\in U(nL,\mathbb Q(i))\). Then:*

1. **Exact coarse-cell probability realization in \([0,1]\):** *Every \(\mathcal W\in\{\mathcal I,\mathcal W^{R,\mathrm{Pyth}}_{ij},\mathcal W^{I,\mathrm{Pyth}}_{ij}\}\) is an exact Gaussian-rational unitary (\(\mathcal W\mathcal W^\dagger=I_{nL}\), zero square roots) mapping \(J_n(D)\mapsto J_n(UDU^\dagger)\), preserving \(M_{nL}=\operatorname{Tr} D\) and exact \(n\)-cell coarse decoherence. Reading coarse cell \(C_i\) yields \(n^2\) genuine bounded outcome probabilities \(p_v(D)=\operatorname{Tr}(DE_v)\in[0,1]\) (\(0\preceq E_v\preceq I_n\)) across all normalized \(D\in\mathrm{PSD}_n^1(\mathbb C)\):*
   \[
   p_i(D)=\mu_{J_n(D)}(C_i)=D_{ii},\quad
   p^R_{ij}(D)=\frac{9D_{ii}+16D_{jj}+24\operatorname{Re} D_{ij}}{25},\quad
   p^I_{ij}(D)=\frac{9D_{ii}+16D_{jj}+24\operatorname{Im} D_{ij}}{25}.
   \tag{23}
   \]
2. **Exact Hermitian inverse and trace-mass feasibility check:** *Given noisy real estimates \((y_i,y^R_{ij},y^I_{ij})\) with nonnegative absolute bounds \((\eta_i,\eta^R_{ij},\eta^I_{ij})\), the unique Hermitian linear inverse \(\widehat D\) is*
   \[
   \widehat D_{ii}=y_i,\qquad
   \widehat D_{ij}=\frac{25y^R_{ij}-9y_i-16y_j}{24}+i\,\frac{25y^I_{ij}-9y_i-16y_j}{24}\quad(i<j),\qquad
   \widehat D_{ji}=\overline{\widehat D_{ij}},
   \tag{24}
   \]
   *with exact Walsh mass \(M_{nL}(J_n(\widehat D))=\operatorname{Tr}(\widehat D)=\sum_{i=0}^{n-1}y_i\). Nonempty normalized compatibility requires \(|\sum_{i=0}^{n-1}y_i-1|\le\sum_{i=0}^{n-1}\eta_i\).*
3. **Deterministic Frobenius radius and exact rational special case:** *For the real data and bounds in (2), set*
   \[
   \alpha_{ij}=\frac{25\eta^R_{ij}+9\eta_i+16\eta_j}{24},\qquad
   \beta_{ij}=\frac{25\eta^I_{ij}+9\eta_i+16\eta_j}{24},\qquad
   r_{\mathrm{Pyth}}^2 := \sum_{i=0}^{n-1}\eta_i^2 + 2\sum_{0\le i<j<n}\bigl(\alpha_{ij}^2+\beta_{ij}^2\bigr)\in\mathbb R_{\ge 0}.
   \tag{25}
   \]
   *If all supplied estimates and absolute error bounds are rational, then \(\widehat D\in\operatorname{Herm}_n(\mathbb Q(i))\) and \(r_{\mathrm{Pyth}}^2\in\mathbb Q_{\ge 0}\), so the following certificates can be checked in exact rational arithmetic. For arbitrary real inputs the same implications hold analytically, without an exact rational computation claim. Every compatible kernel \(D\) satisfies \(\|D-\widehat D\|_{\mathrm{op}}\le\|D-\widehat D\|_F\le\sqrt{r_{\mathrm{Pyth}}^2}\). Once nonemptiness of the compatibility polytope is verified:*
   - **Universal PSD certificate (rational, \(\sqrt{\cdot}\)-free):** *If \(\bar r\in\mathbb Q_{\ge 0}\) satisfies \(\bar r^2\ge r_{\mathrm{Pyth}}^2\) and \(\widehat D-\bar r I_n\succeq 0\), then every compatible \(D\) satisfies \(D\succeq 0\).*
   - **Universal non-PSD certificate (rational, \(\sqrt{\cdot}\)-free):** *If \(v\in\mathbb Q(i)^n\setminus\{0\}\) satisfies \(v^\dagger\widehat D v<0\) and \((v^\dagger\widehat D v)^2 > r_{\mathrm{Pyth}}^2\|v\|_2^4\), then every compatible \(D\) satisfies \(D\not\succeq 0\).*

**Proof.**
*(1)* Direct multiplication gives \(U^R_{ij}(U^R_{ij})^\dagger=I_L\) and \(U^I_{ij}(U^I_{ij})^\dagger=I_L\) since \(\frac{9+16}{25}=1\) and \(\pm 12i\mp 12i=0\). Because \(H_L^{-1}=\frac1L H_L\) and \(V_{n,L}^2=I_{nL}\), \(\mathcal W\mathcal W^\dagger=I_{nL}\) and \(\mathcal W J_n(D)\mathcal W^\dagger=J_n(U_0 D U_0^\dagger)\) where \(U_0\) is the \(n\times n\) unpadded block of \(U\) (since \(U\) fixes all padded coordinates \(\ge n\)). By Theorem 1A(1) of [`RELATIONAL_IDENTITY_BRIDGE.md`](../t8-q-relational-identity-completion-2026-10-31/RELATIONAL_IDENTITY_BRIDGE.md), \(\mu_{J_n(U_0 D U_0^\dagger)}(C_i)=(U_0 D U_0^\dagger)_{ii}=u^\dagger D u=\operatorname{Tr}(D\,uu^\dagger)\) where \(u=U_0^\dagger e_i\) is the unit vector \(\frac15(3e_i+4e_j)\) for \(U^R_{ij}\) and \(\frac15(3e_i-4ie_j)\) for \(U^I_{ij}\). Since \(\|u\|_2=1\), \(E_v=uu^\dagger\) is a rank-1 orthogonal projector satisfying \(0\preceq E_v\preceq I_n\), so \(p_v(D)\in[0,\operatorname{Tr} D]=[0,1]\) on all \(D\in\mathrm{PSD}_n^1(\mathbb C)\), and expanding \(u^\dagger D u\) gives (23).

*(2)–(3)* Solving (23) linearly for \(D_{ii},\operatorname{Re} D_{ij},\operatorname{Im} D_{ij}\) yields (24). By the triangle inequality on (24), \(|D_{ii}-\widehat D_{ii}|\le\eta_i\), \(|\operatorname{Re}(D_{ij}-\widehat D_{ij})|\le\alpha_{ij}\), and \(|\operatorname{Im}(D_{ij}-\widehat D_{ij})|\le\beta_{ij}\); summing over all \(n\) diagonal and \(2\binom n2\) off-diagonal entries proves \(\|D-\widehat D\|_F^2\le r_{\mathrm{Pyth}}^2\). If \(\bar r^2\ge r_{\mathrm{Pyth}}^2\) and \(\widehat D-\bar r I_n\succeq 0\), then \(D=\widehat D+(D-\widehat D)\succeq\bar r I_n-\|D-\widehat D\|_{\mathrm{op}}I_n\succeq(\bar r-\sqrt{r_{\mathrm{Pyth}}^2})I_n\succeq 0\). If \(v^\dagger\widehat D v<0\) and \((v^\dagger\widehat D v)^2>r_{\mathrm{Pyth}}^2\|v\|_2^4\), then \(v^\dagger D v\le v^\dagger\widehat D v+\sqrt{r_{\mathrm{Pyth}}^2}\|v\|_2^2<0\), so \(D\not\succeq 0\). ∎

---

## 6. Conditional Connections and Remaining Boundaries

The three packages provide separate conditional connections. They do not establish that all foundational questions are closed, and their premises must be transferred individually:

1. **Degree and coefficient selection (Theorems 2A–2C):** The amplitude-family theorem yields quadratic throughput and Sorkin grade at most two under its stated localized preparation, homogeneous scaling, signed positivity and rotated partition-conservation premises. The independent polynomial theorem yields only \(d(n)=n\) or \(n^2\) and their binomial coefficients when multiplicativity and the supplied \(d(2)\le4\) bound hold. Neither dimensions alone nor the coefficient count identifies a positive cone, effects or composition.
2. **Composition, restricted quotient and section readouts:** The first package selects ordinary tensor composition from its real-incidence-natural family using quarter-phase interchange, and two-copy coincidence grouping forces complex cross-cell orthogonality. The second package's single-system test quotient, identity-atomicity, generator-observability and minimal-rank hypotheses have their declared scope. Its \(J_n\) section and admitted joint couplers supply coarse-cell principal-minor readouts. These are not a proved extension of equivalence to all representatives under arbitrary joint tests.
3. **Copies and probability values (Theorems 4A–4B):** The tournament family proves that truncating the specified principal-minor sign catalogue at \(n-1\) copies fails in dimension \(n\). It does not exclude arbitrary bounded-copy strategies. The Pythagorean controls supply a single-copy probability catalogue and inverse on the trace-normalized Walsh section. RI-23's raw total-entry-mass obstruction remains valid on its original domain. Real error bounds give analytic enclosures; exact rational computation additionally requires rational supplied data and bounds.
4. **Selective update (Theorems 3A–3C):** For arbitrary orthogonal \(P\), 1-positivity, effect calibration and non-disturbance on the entire repeat face imply \(\Phi(\rho)=P\rho P\). Ordinary repeatability alone does not. The explicit dyadic-real Walsh lift is proved for coordinate/coarse-cell projectors \(P_R\), not arbitrary projectors.
5. **Order-growth construction (Theorems 1A–1C):** The anchored tensor-local candidate realizes \(S_{\mathrm{CHSH}}=14/5\) over \(q_{1/2}>0\), with full branch-map diamonds. Its comparator distinction requires the declared setting independence and locality assumptions. The unanchored obstruction additionally assumes full unnormalized branch-map diamonds; scalar diamonds alone do not suffice. “Spacelike” denotes order incomparability, not a derived spacetime metric.

Physical availability of the controls, couplers, origin handles and readouts is unsupplied. The constructions do not select a unique growth law, reconstruct global quantum theory, derive native energy/mass/gravity or a continuum limit, or establish empirical calibration. They neither complete the separate sustaining-regime/mass objective nor establish personal continuity. Ontological claims remain distinct from these conditional calculations.

---

## 7. Checker Source, Finite Coverage and Reproduction Status

[`check.py`](check.py) is a self-contained Python standard-library test suite (`fractions.Fraction`, `itertools`, `unittest`, and an exact immutable Gaussian-rational type `G`) with zero floating-point literals, types, or external imports, and all lines \(\le 100\) characters. Its eight test methods encode the following finite checks. The audit correction author has read the source but has not executed either the normal or optimized command below; no independent reproduction is asserted by this revision. The finite examples supplement the written proofs and do not formally verify their universal quantifiers:

1. `test_01_unanchored_monogamy_and_spacelike_chsh_diamond_growth`: Exact identity \(N'=(J_2\otimes J_2)(\sigma_{\mathrm{joint}})\), unanchored disjoint-union diamond failure \([\widehat Q_{A,0,0},\widehat Q_{A,1,0}]\ne 0\) versus the 16-outcome joint distribution (\(|S_{\mathrm{CHSH}}|\le 2\)) for mutually commuting instruments, dyadic \(q_{1/2}\) normalization and scalar diamonds, strict four-cell block-diagonality, \(M_{16}\) and \(\operatorname{Tr}\) row normalization, \(832\) marked branch comparisons across \(P_0\) and \(P_3\) (eight comparisons explicitly materialize the full \(256\times256\) matrices; the remainder compare scalar factors and Kraus products), wingwise repeatability, no-signaling, and \(S_{\mathrm{CHSH}}=14/5>2\) on \(P_4^\parallel\).
2. `test_02_classical_simplex_chsh_bound_and_pr_box_countermodel`: Hadamard-product 16-outcome joint distribution (\(|S_{\mathrm{CHSH}}|\le 2\)) on unfactorized \(\mathbb R_+^6\) under residual-level no-signaling, versus the exact-rational \(10\times 10\) commuting classical-simplex countermodel on \(\mathbb R_+^{10}\) (\([A_{x,a},B_{y,b}]=0\) on all 16 pairs, outcome no-signaling, \(S_{\mathrm{CHSH}}=4\)).
3. `test_03_grade3_countermodels_and_pairwise_decoherence_insufficiency`: Exact rational verification of the 4-atom witness (\(I_2=0\) pairwise, \(I_3=1/4\)) and exhaustive disjoint-family verification of the 3-atom masked witness \(\mu_{\mathrm{mask}}\) (singleton-complete, Pairwise Decoherence Sufficiency everywhere, \(I_3=1/8\ne 0\)).
4. `test_04_amplitude_scaling_and_stirling_dimension_select_grade2`: Odd-degree sign failure, rational \((3,4,5)\) rotation selection \((9/25)^r+(16/25)^r=1\iff r=1\), \(I_3=I_4=0\) across all disjoint subset triples/quadruples for one selected four-dimensional quadratic form, degree-4 countermodel \(F_4\) (\(I_3=4/9\)), Stirling identity \(n^{r_0}=\sum_{r=1}^{r_0}r!\,S(r_0,r)\binom n r\), refutation of real Möbius hierarchies, and \(c_2\in\{0,2\}\) selection.
5. `test_05_degenerate_subspace_countermodels_on_qutrit_walsh_section`: Rank-9 embedding of \(J_3(\operatorname{Herm}_3(\mathbb C))\), rank-4 repeat face \(F_{01}\), calibration and repeatability of \(\mathcal T_{01}^{\mathrm{mix}}\) and \(\mathcal T_{01}^{\mathrm{deph}}\) (plus fine-cell preservation by \(\mathcal T_{01}^{\mathrm{deph}}\)), coherence contrast \(\frac{49}{50}\) vs \(\frac12\) under \(\mathcal W^R_{01}\), and zero-mass nonzero dark payload of literal 12-label cut \(\Pi_{C_{01}}\) on \(J_3(|2\rangle\langle 2|)\).
6. `test_06_pure_one_positivity_uniqueness_of_degenerate_luders_rule`: Exact dyadic-rational \(12\times 12\) projectors \(\widehat P_{01}\) (rank 6) and \(\widehat P_2\) (rank 3) reproducing \(J_3(P_R\rho P_R)\), rank-4 subspace finer-cell tomography on \(F_{01}\), and a basis of 32 surviving perturbation directions in an 81-dimensional linear space; each basis direction is given a positivity counterexample. Arbitrary combinations require the written quadratic argument, not this finite basis check. The encoded counterexamples violate \(\Phi(\rho(t))\succeq 0\) at an explicit rational \(t\in\mathbb Q\).
7. `test_07_bounded_copy_minor_truncation_and_sign_blindness`: Entrywise nonnegativity for powers one through three of non-PSD \(D_+=(J_3-I_3)/6\), strict positive definiteness of all \(2^n-2\) proper principal submatrices (\(|I|\le n-1\)) alongside \(\det<0\) for \(D^{(n)}_{\mathrm{imag}}(t_n)\) at \(n=2,3,4,5\) (\(-11/100,-11/432,-7/4096,-10564/89253125\)), and explicit 32-dimensional fiber verification of positive \(m=2\) coarse-cell minor readout \(7/288>0\) on \(J_3(D^{(3)}_{\mathrm{imag}}(1/4))\).
8. `test_08_single_copy_walsh_probability_catalogue_and_ri23_certificates`: Raw-domain rank-1 obstruction on \(K_3\) and \(\|T_{e_0+e_1}\|_{\mathrm{op}}=2>1\); exact unitarity, coarse decoherence, \(M_{nL}=1\) preservation, \(0\preceq E_v\preceq I_n\), and exact linear reconstruction \(\widehat D=D\) across \(n=2,3,4\) (including RI-23's \(D_*\) with all 9 probabilities in \((0,1)\)); and square-root-free rational verification of all four RI-23 interval decision regimes on \(J_2(D_t)\).

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/validation/t8-q-tier1-foundational-closure-2026-10-31/check.py -v
PYTHONDONTWRITEBYTECODE=1 python3 -B -O docs/validation/t8-q-tier1-foundational-closure-2026-10-31/check.py -v
```

Preserved checker source SHA-256 (`check.py`; identity only, not an execution receipt):
`3b0b99420527fd7d26b4e5d9e7f780be1728d6a45176517c7366eea7e9d901c7`.
