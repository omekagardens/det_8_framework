# Relational-Identity Completion: Coarse-Cell Minors, Complex Qubit Cone Selection, and Active Pair-Kernel Causal Growth

31 October 2026. **CONDITIONAL_UPSTREAM_BRIDGE_THEOREMS; OBSTRUCTIONS_AND_CLASSICAL_COMPARATORS_EXPLICIT.**

Prospective protocol frozen prior to proof assembly and verification in [`PROTOCOL.md`](PROTOCOL.md) (`2631552`). This study extends [`t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md`](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md) (`9b38efe`) on branch `qr-pair-kernel-bridge` without modifying any previously frozen file, accepted source, core module, or other branch (`main`, `ret`, `qr-05-bridge`). All results are conditional mathematical theorems, obstructions, and classical comparators (`TH-DET` / `MATH` at declared scope) under [`GOVERNANCE.md`](../../../GOVERNANCE.md).

---

## 1. Executive Summary and How `main`'s Relational Identity Bridges the Gaps

The companion note [`BRIDGE_THEOREM.md`](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md) proved that silent quarter-phase interchange selects ordinary tensor composition \(D\otimes E\) out of the complete real-incidence-natural family \(D\odot_\alpha E\), that two-copy coincidence grouping forces record orthogonality \(D(A_r,A_s)=0\), and that one silent Hadamard lift \(D_{+X}=S_H(D_{+Z})\) replaces [RI-21](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md)'s unrecordable trace-three seed. It simultaneously isolated three remaining gaps:

- **Gap B2 (Sub-cell addressing):** RI-21 and Theorem 3A of [`BRIDGE_THEOREM.md`](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md) evaluated principal minors on permutation events \(\widetilde E_I^{\mathrm{nat}}\) addressing internal sub-cell atoms \(\{2\},\{3\}\subset A_1\).
- **Gap A2 + Gap C (Rank-1 mass trap and complex residual cone selection):** [`OPERATION_DOMAIN.md`](../t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md) proved that linear instruments positive on the *unrestricted* total-entry-mass cone \(K_n\) have rank-1 sum \(\Gamma_n=\mathbf 1_n\mathbf 1_n^\dagger\) and admit noncompact scalings \(M_\lambda=P_++\lambda P_-\), while [`why_complex.py`](../../../det8/models/why_complex.py) exhibited mixed-rank \(D_t=(I_{2m}+itJ_0)/2\) (\(0<t<1\)) with \((G^{-1}\Omega)^2=-t^2 I_{2m}\ne -I_{2m}\).
- **Gap D (Active pair-kernel causal growth across diamonds):** [`native_active_residual_v1.md`](../../track_b/native_active_residual_v1.md) coupled active residuals to causal growth only on classical \(\mathbb R_+^2\), while [`homogeneous_native_compensation.md`](../../track_b/homogeneous_native_compensation.md) and [`finite_homogeneous_compensation.md`](../../track_b/finite_homogeneous_compensation.md) proved that context-independent branch maps \(\mathcal B_{S,b}=q(P,r,S)\mathcal C_b\) satisfy incomparable diamonds iff \([\mathcal C_b,\mathcal C_c]=0\).

On `main`, relational identity ([`ONTOLOGY.md`](../../../ONTOLOGY.md), [`QR_MAP_RECORD_SUFFICIENCY.md`](../../track_b/QR_MAP_RECORD_SUFFICIENCY.md), [`THEOREM_PACKAGE.md`](../../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md), [`fact_genesis_resurrection_bridge.md`](../../track_b/fact_genesis_resurrection_bridge.md)) provides three structural principles that directly target these gaps:

1. **Future-test equivalence \(\sim_{\mathscr T}\) (`PID-C`):** Sub-cell labels inside a coarse record cell \(C_a\) are internal encoding coordinates, not individually commitable facts; physical states live on the operational quotient \(\mathcal C/{\sim_{\mathscr T}}\), while couplers need only respect \(\sim_{\mathscr T}\) and preserve coarse-cell decoherence ([RI-08d](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md)).
2. **Order-unit lifting, identity-atomicity, and generator observability:** Quotienting RI-08b's control-viable cone \(\mathcal C_4\) ([`CONTROL_SELECTED_QUBIT.md`](../t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md)) by \(\sim_{\mathscr T}\) turns rank-1 \(\Gamma_4\) into full-rank \(\operatorname{Tr}\) on \(\mathrm{PSD}_2(\mathbb C)\), while the selection principles explored in [`RESEARCH.md`](../t8-q-principle-selection-research-2026-09-13/RESEARCH.md) separate \(\mathrm{PSD}_2(\mathbb C)\) from both classical \(\mathrm{Diag}_+(\Omega_d)\) and real rebit \(\mathrm{PSD}_2(\mathbb R)\) without invoking local tomography.
3. **Context-addressed branch maps \(\mathcal B^{P,r}_{S,b}\):** Relational identity addresses each birth by its actual causal prefix \((P,r,S)\) up to relabeling covariance, bypassing [`finite_homogeneous_compensation.md`](../../track_b/finite_homogeneous_compensation.md)'s context-independent commutation trap.

| Bridge component | Load-bearing operational premises | Proved mathematical conclusion | Exact obstruction / classical comparator |
|---|---|---|---|
| **Theorem 1A–1B** (§2): Coarse-cell dyadic minor witness | Pre-PSD \(D\in\operatorname{Herm}_n(\mathbb C)\) (\(\operatorname{Tr} D=1\)); Walsh section \(J_n(D)\) on \(\Omega_{nL}\); \(\le 2\) diagonal ancillas \(D_{+Z}\); \(\sim_{\mathscr T}\)-lifted dyadic Sylvester-Hadamard coupler \(\mathcal U_I\); coarse-cell nonnegativity | \(J_n(D)\in M_{nL}(\mathbb Z[1/2,i])\) is coarse-cell decoherent with \(M(J_n(D))=\operatorname{Tr} D\) and \(J_n(D)\succeq 0\iff D\succeq 0\); \(\mathcal U_I\) uses **zero sub-cell addressing**, preserves \(M=1\) and full coarse decoherence, and yields \(\mu(C_*)=\frac{|I|!}{2^k}\det(D_I)\) | **Theorem 1B:** On raw unencoded \(D^{\otimes m}\otimes D_{\mathrm{anc}}\) with one ancilla \(D_{\mathrm{anc}}\in\mathcal C_4\), any controlled unitary with \(V_{\mathbf x}\mathbf 1_4=\mathbf 1_4\) obeys \(|\mathbf 1_4^\dagger y|\le\sqrt 2\|y\|_2\) on \(\ker D_{\mathrm{anc}}\), forcing \(v_+=v_-\) and zero \(\det\) sensitivity |
| **Theorem 2A–2D** (§3): Quotient escape & complex cone selection | Control-viable cone \(\mathcal C_4\); quotient \(\sim_{\mathscr T}\); reference-complete identity-atomicity; Barnum–Müller–Ududec generator observability; minimal-rank purity | \(\mathcal C_4/{\sim_{\mathscr T}}\cong\mathrm{PSD}_2(\mathbb C)\) lifts \(\Gamma_4\) to full-rank \(\operatorname{Tr}\) and forces \(\lambda=1\) in \(M_\lambda\); identity-atomicity excludes \(\mathrm{Diag}_+(\Omega_d)\) (\(d\ge 2\)); generator observability excludes \(\mathrm{Sym}_2(\mathbb R)\) (\(\ker D_{J_0}^*=\mathbb R\operatorname{Tr}\)); \(\operatorname{rank}_{\mathbb C}(D)=m\iff (G^{-1}\Omega)^2=-I_{2m}\) | Raw \(K_2\) without \(S_H\)-reachability admits \(M_\lambda\) (\(\lambda\ne 1\)); dropping purity allows mixed-rank \(D_t\) (\(|t|<1\), \(\operatorname{rank}_{\mathbb C}=2m>m\)) from [`why_complex.py`](../../../det8/models/why_complex.py) |
| **Theorem 3A–3B** (§4): Four-birth active pair-kernel diamond law | Part A marked \(q_C(S)\) ([`finite_incidence_register.md`](../../observables/finite_incidence_register.md)); context-addressed CP family \(\mathcal B^{P,r}_{S,b}\) on \(\mathcal C_4\subset M_4(\mathbb C)\) | Strictly PD \(16\times 16\) Choi matrices; exact \(M\) and \(\operatorname{Tr}\) row normalization; relabeling covariance; timelike noncommutativity \([\mathcal B_2,\mathcal B_1]\ne 0\); all **580** labeled (\(|C|\le 2\)) \(16\times 16\) superoperator diamonds commute; \(\operatorname{Re}\)-identical \(D_{\pm Y}\) shift 4-birth antichain probability by \(\Delta_Z=263/1{,}115{,}136\) | Explicit \(d=4\) classical cyclic-simplex model \((\Delta_4,C_4)\) on mixed states matches the attenuated single-wing four-step \(S_P^k\) table, showing why Target R2 or bipartite CHSH is needed for full classical exclusion |

---

## 2. Target R1 — Coarse-Cell Dyadic-Rational Principal-Minor Witness via \(\sim_{\mathscr T}\) Quotienting

### 2.1 Walsh-untwisted \(n\)-cell section over \(\mathbb Z[1/2,i]\)

For any \(n\ge 2\), let \(p=\lceil\log_2 n\rceil\), \(L=2^p\), and \(H_L=H_0^{\otimes p}\in\{\pm 1\}^{L\times L}\), where \(H_0=\bigl(\begin{smallmatrix}1&1\\1&-1\end{smallmatrix}\bigr)\) satisfies \(H_0^2=2I_2\) and hence \(H_L^2=L I_L\). Partition the \(nL\)-element carrier \(\Omega_{nL}=\{0,\dots,nL-1\}\) into \(n\) coarse record cells
\[
C_a=\{aL,\,aL+1,\dots,(a+1)L-1\}\qquad(a=0,\dots,n-1).
\tag{1}
\]
Let \(w_a=(H_L)_{a,\bullet}^T\in\{\pm 1\}^L\) denote row \(a\) of \(H_L\), set \(\Omega_a=\operatorname{diag}(w_a)\) (\(\Omega_a^2=I_L\)), and define \(V_{n,L}=\bigoplus_{a=0}^{n-1}\Omega_a\) (\(V_{n,L}^2=I_{nL}\)). Given any pre-PSD Hermitian candidate \(D\in\operatorname{Herm}_n(\mathbb C)\), pad \(D\) by zeros to \(D_{\mathrm{pad}}=\operatorname{diag}(D,0_{L-n})\in\operatorname{Herm}_L(\mathbb C)\), set \(\widetilde D=\frac{1}{L^2}H_L D_{\mathrm{pad}}H_L\), and define the **Walsh-untwisted \(n\)-cell section**
\[
\boxed{J_n(D):=\bigoplus_{a=0}^{n-1}\Omega_a\widetilde D\Omega_a = \frac{1}{L^2}\,V_{n,L}\bigl(I_n\otimes(H_L D_{\mathrm{pad}}H_L)\bigr)V_{n,L}\in\operatorname{Herm}_{nL}(\mathbb C).}
\tag{2}
\]

### 2.2 Coarse-cell determinant witness with zero sub-cell addressing

**Theorem 1A (Dyadic Walsh section and coarse-cell principal-minor witness).** *Let \(n\ge 2\) and \(D\in\operatorname{Herm}_n(\mathbb C)\) with \(\operatorname{Tr} D=1\).*

1. **Exact coarse decoherence, dyadic rationality, and PSD equivalence:** *If \(D\in M_n(\mathbb Z[1/2,i])\) (respectively \(M_n(\mathbb Q(i))\)), then \(J_n(D)\in M_{nL}(\mathbb Z[1/2,i])\) (respectively \(M_{nL}(\mathbb Q(i))\)) without roots of unity for any \(n\). Furthermore, \(J_n(D)(C_a,C_b)=0\) for all \(a\ne b\), \(\mu_{J_n(D)}(C_a)=D_{aa}\), \(M(J_n(D))=\operatorname{Tr} D=1\), and \(J_n(D)\succeq 0\iff D\succeq 0\). At \(n=2\) (\(L=2\)), \(J_2(D)=S_H(\operatorname{diag}(\frac12 D,\frac12 ZDZ))\in\mathcal C_4\) for every \(D\succeq 0\).*
2. **Single-coarse-cell principal-minor readout:** *For every nonempty \(I=\{i_0<\dots<i_{m-1}\}\subseteq\{0,\dots,n-1\}\) (\(m=|I|\)), let \(k\ge 0\) be the smallest **even** integer with \(2^k\ge m!\), and take \(r\in\{0,1,2\}\) diagonal classical ancillas \(D_{+Z}=J_2(\operatorname{diag}(1,0))\) satisfying \((2^r-1)n^m\ge 2^k-m!\) (\(r=0\) for \(m=1\); \(r=1\) suffices for \(m\in\{2,3\}\); \(r\le 2\) suffices for all \(n\ge m\ge 1\)). There exists an explicit \(\sim_{\mathscr T}\)-lifted coupler \(\mathcal U_I\) with exact dyadic-rational entries in \(\mathbb Z[1/2]\) such that on*
   \[
   K_I := \mathcal U_I\bigl(J_n(D)^{\otimes m}\otimes D_{+Z}^{\otimes r}\bigr)\mathcal U_I^\dagger,
   \tag{3}
   \]
   *\(K_I\) is Hermitian, preserves total-entry mass \(M(K_I)=1\), is **100% block-diagonal (exactly decoherent)** across all \(n^m 2^r\) coarse product cells \(C_{\mathbf a,\mathbf b}=C_{a_1}\times\dots\times C_{a_m}\times A_{b_1}\times\dots\times A_{b_r}\), uses **zero sub-cell addressing**, and assigns to the single target coarse product cell \(C_*=C_{i_0}\times\dots\times C_{i_{m-1}}\times A_0^{\times r}\) the weight*
   \[
   \boxed{\mu_{K_I}(C_*) = \frac{|I|!}{2^k}\,\det(D_I).}
   \tag{4}
   \]
   *Consequently, nonnegativity of coarse product-cell weights across the \(2^n-1\) nonempty subsets \(I\) holds if and only if \(D\succeq 0\).*

**Proof.**
*(1)* Since \(1/L^2=2^{-2p}\in\mathbb Z[1/2]\) and \(H_L,\Omega_a\) have entries in \(\{\pm 1\}\), \(J_n(D)\) preserves \(\mathbb Z[1/2,i]\) and \(\mathbb Q(i)\) for every \(n\). Block-diagonality of (2) gives \(J_n(D)(C_a,C_b)=0\) for \(a\ne b\). Because \(\mathbf 1_L^T\Omega_a=w_a^T=e_a^T H_L\) and \(H_L^2=L I_L\),
\[
\mu_{J_n(D)}(C_a) = \mathbf 1_L^T\Omega_a\widetilde D\Omega_a\mathbf 1_L
= \frac{1}{L^2}(e_a^T H_L^2)D_{\mathrm{pad}}(H_L^2 e_a)
= e_a^T D_{\mathrm{pad}}e_a = D_{aa},
\]
so \(M(J_n(D))=\sum_{a=0}^{n-1}D_{aa}=\operatorname{Tr} D=1\). Each block \(\Omega_a\widetilde D\Omega_a\) is unitarily congruent to \(\widetilde D=\frac1L\bigl(\frac1{\sqrt L}H_L\bigr)D_{\mathrm{pad}}\bigl(\frac1{\sqrt L}H_L\bigr)\), whose nonzero spectrum is \(\frac1L\operatorname{spec}(D)\); hence \(J_n(D)\succeq 0\iff D\succeq 0\). For \(n=2\), \(\Omega_0=I_2\) and \(\Omega_1=Z\), recovering RI-08b's \(S_H\)-encoded block structure.

*(2)* If \(m=1\), \(k=r=0\), \(\mathcal U_{\{i_0\}}=I_{nL}\), and \(\mu_{J_n(D)}(C_{i_0})=D_{i_0 i_0}=\det(D_{\{i_0\}})\). For \(m\ge 2\), minimality of even \(k\) implies \(2^{k-2}<m!\), so \(2^k-m!<3\,m!\le 3n^m=(2^2-1)n^m\); thus \(r\le 2\) always supplies at least \(2^k-m!\) ancilla-zero tuples in \(\{0,\dots,n-1\}^m\times(\{0,1\}^r\setminus\{\mathbf 0\})\).

Let \(\Pi\) be the permutation regrouping tensor factors into \((\text{coarse cell indices})\otimes(\text{internal Walsh fiber})\), and set \(T_{m,r}=\Pi(V_{n,L}^{\otimes m}\otimes V_{2,2}^{\otimes r})\). By (2),
\[
T_{m,r}\bigl(J_n(D)^{\otimes m}\otimes D_{+Z}^{\otimes r}\bigr)T_{m,r}^\dagger
= I_{n^m 2^r}\otimes\bigl(\widetilde D^{\otimes m}\otimes\widetilde E_{00}^{\otimes r}\bigr),
\tag{5}
\]
where \(E_{00}=\operatorname{diag}(1,0)\) and \(\widetilde E_{00}=\frac14 H_2 E_{00}H_2\). Inside the unpadded index set \(\{0,\dots,n-1\}^m\times\{0,1\}^r\subseteq\{0,\dots,L-1\}^m\times\{0,1\}^r\), partition the \(m!\) permutation tuples \(\{(i_{\pi(0)},\dots,i_{\pi(m-1)},\mathbf 0):\pi\in S_m\}\) into \(m!/2\) even and \(m!/2\) odd tuples, adjoin \(\frac12(2^k-m!)\) distinct ancilla-zero tuples \((\mathbf a,\mathbf b\ne\mathbf 0)\) to each half to form a \(2^k\)-element active set, and align them with the \(2^{k-1}\) \((+1)\)-columns and \(2^{k-1}\) \((-1)\)-columns of row \(1\) of \(H_0^{\otimes k}\). Placing row \(1\) of \(H_0^{\otimes k}\) at output index \(*=(i_0,\dots,i_{m-1},\mathbf 0)\) and scaling by \(2^{-k/2}=2^{-(k/2)}\in\mathbb Z[1/2]\) (exact dyadic rational because \(k\) is even) yields an orthogonal matrix \(U_I\in\mathbb Z[1/2]^{(L^m 2^r)\times(L^m 2^r)}\) acting as the identity on all remaining (including all padded) coordinates.

Conjugate \(U_I\) into the Walsh fiber via \(\widetilde U_I=(H_L^{-1})^{\otimes m}\otimes(H_2^{-1})^{\otimes r}\cdot U_I\cdot(H_L^{\otimes m}\otimes H_2^{\otimes r})\in\mathbb Z[1/2]^{(L^m 2^r)\times(L^m 2^r)}\) (using \(H_L^{-1}=2^{-p}H_L\)) and lift across coarse cells by
\[
\mathcal U_I := T_{m,r}^\dagger\bigl(I_{n^m 2^r}\otimes\widetilde U_I\bigr)T_{m,r}.
\tag{6}
\]
By (5)–(6), \(T_{m,r}K_I T_{m,r}^\dagger = I_{n^m 2^r}\otimes\widetilde S_I\), where
\[
\widetilde S_I = \frac{1}{L^{2m}4^r}(H_L^{\otimes m}\otimes H_2^{\otimes r})\,S_I\,(H_L^{\otimes m}\otimes H_2^{\otimes r}),\qquad
S_I := U_I\bigl(D_{\mathrm{pad}}^{\otimes m}\otimes E_{00}^{\otimes r}\bigr)U_I^T.
\tag{7}
\]
Because \(T_{m,r}\) acts only within each coarse product cell \(C_{\mathbf a,\mathbf b}\) by internal signs \(\Omega_{a_1}\otimes\dots\otimes Z^{b_r}\), \(K_I\) is **strictly block-diagonal** across all \(n^m 2^r\) coarse product cells, proving \(K_I(C_{\mathbf a,\mathbf b},C_{\mathbf a',\mathbf b'})=0\) for \((\mathbf a,\mathbf b)\ne(\mathbf a',\mathbf b')\). Evaluating the cell indicator on \(C_{\mathbf a,\mathbf b}\) contracts \(\mathbf 1^{\otimes(m+r)}(\Omega_{a_1}\otimes\dots\otimes Z^{b_r})=e_{\mathbf a,\mathbf b}^T(H_L^{\otimes m}\otimes H_2^{\otimes r})\) against (7) to yield \(\mu_{K_I}(C_{\mathbf a,\mathbf b})=(S_I)_{(\mathbf a,\mathbf b),(\mathbf a,\mathbf b)}\). Since \(U_I\) fixes every padded coordinate outside \(\{0,\dots,n-1\}^m\times\{0,1\}^r\), all padded diagonal entries of \(S_I\) vanish, so
\[
M(K_I)=\sum_{\mathbf a\in\{0,\dots,n-1\}^m}\sum_{\mathbf b\in\{0,1\}^r}(S_I)_{(\mathbf a,\mathbf b),(\mathbf a,\mathbf b)}
=\operatorname{Tr}(S_I)=\operatorname{Tr}(D_{\mathrm{pad}}^{\otimes m}\otimes E_{00}^{\otimes r})=(\operatorname{Tr} D)^m=1.
\]
Finally, on \(D_{\mathrm{pad}}^{\otimes m}\otimes E_{00}^{\otimes r}\), every ancilla-zero tuple \((\mathbf a,\mathbf b\ne\mathbf 0)\) has zero row and column, so row \(*\) of \(U_I\) picks up exclusively the signed permutation sum:
\[
\mu_{K_I}(C_*)=(S_I)_{*,*}
=\frac{1}{2^k}\sum_{\pi,\sigma\in S_m}\operatorname{sgn}(\pi)\operatorname{sgn}(\sigma)\prod_{t=0}^{m-1}D_{i_{\pi(t)},i_{\sigma(t)}}
=\frac{m!}{2^k}\det(D_I).
\]
By Sylvester's Hermitian PSD criterion (every principal minor \(\det(D_I)\ge 0\), cf. [RI-21 §3](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md#3-main-theorem-bounded-copy-strong-positivity-selection)), \(\mu_{K_I}(C_*)\ge 0\) for all \(\varnothing\ne I\subseteq\{0,\dots,n-1\}\) holds iff \(D\succeq 0\). (For \(n=2,m=2\), applying \(H_0\) on both \(\{01,10\}\) and \(\{00,11\}\) gives an integer \(U_0\) with \(U_0 U_0^T=2I_4\), achieving \(\mu(C_{01})=\det(D)\) with \(r=0\) ancillas.) ∎

### 2.3 Exact obstruction on raw unencoded composites with one mass-preserving ancilla

Why must \(D\) be embedded via the \(\sim_{\mathscr T}\) section \(J_n(D)\) (or why cannot a single four-label ancilla \(D_{\mathrm{anc}}\in\mathcal C_4\) isolate \(\det(D_I)\) from raw unencoded \(D^{\otimes m}\otimes D_{\mathrm{anc}}\) under branchwise mass-preserving unitaries)?

**Lemma 1B.1 (Kernel overlap bound on \(\mathcal C_4\)).** *For every normalized \(D_{\mathrm{anc}}=D(A,c)\in\mathcal C_4\) (\(2\operatorname{Tr} A=1\), \(A\succeq |c|I_2\)) and every \(y\in\ker(D_{\mathrm{anc}})\),*
\[
|\mathbf 1_4^\dagger y|^2 \le 2\,\|y\|_2^2.
\tag{8}
\]

**Proof.** If \(A\succ |c|I_2\), \(D(A,c)\succ 0\), so \(y=0\). Notice that \(\frac1{\sqrt 2}\mathbf 1_2\) and \(\frac1{\sqrt 2}Z\mathbf 1_2\) form an orthonormal basis of \(\mathbb C^2\), so for every \(u\in\mathbb C^2\),
\[
|\mathbf 1_2^\dagger u|^2 + |\mathbf 1_2^\dagger Z u|^2 = 2\|u\|_2^2, \qquad
\|\mathbf 1_2 - e^{i\phi}Z\mathbf 1_2\|_2^2 = \|\mathbf 1_2\|_2^2 + \|Z\mathbf 1_2\|_2^2 = 4.
\tag{9}
\]
If \(c=0\) and \(\det A=0\), then \(A=\frac12|\psi\rangle\langle\psi|\) (\(\|\psi\|_2=1\)) and \(\ker D(A,0)=\{(\alpha\psi_\perp,\beta Z\psi_\perp)^T:\alpha,\beta\in\mathbb C\}\) for unit \(\psi_\perp\perp\psi\); Cauchy–Schwarz and (9) give \(|\mathbf 1_4^\dagger y|^2\le(|\alpha|^2+|\beta|^2)(|\mathbf 1_2^\dagger\psi_\perp|^2+|\mathbf 1_2^\dagger Z\psi_\perp|^2)=2\|y\|_2^2\). If \(|c|>0\) and \(\lambda_{\min}(A)=|c|\) (\(c=|c|e^{i\phi}\)), every \(y\in\ker D(A,c)\) has the form \(y=(u,-e^{-i\phi}Zu)^T\) with \(\|y\|_2^2=2\|u\|_2^2\), and Cauchy–Schwarz with (9) gives \(|\mathbf 1_4^\dagger y|^2=|(\mathbf 1_2-e^{i\phi}Z\mathbf 1_2)^\dagger u|^2\le 4\|u\|_2^2=2\|y\|_2^2\). ∎

**Theorem 1B (Single-ancilla raw mass-preserving obstruction).** *Let \(D\in\operatorname{Herm}_2(\mathbb C)\) be unencoded (\(M_2(D)=\mathbf 1_2^\dagger D\mathbf 1_2\)), let \(D_{\mathrm{anc}}\in\mathcal C_4\) (\(M_4(D_{\mathrm{anc}})=1\)), and let \(\mathcal V=\sum_{\mathbf x\in\{0,1\}^2}|\mathbf x\rangle\langle\mathbf x|\otimes V_{\mathbf x}\) be any controlled unitary whose branches preserve raw ancilla mass, \(V_{\mathbf x}\mathbf 1_4=\mathbf 1_4\). For either coarse ancilla cell \(A_r\) (\(r\in\{0,1\}\)) read out on the permutation sector \(E_r=\{(0,1),(1,0)\}\times A_r\), \(\mu_{\mathcal V(D^{\otimes 2}\otimes D_{\mathrm{anc}})\mathcal V^\dagger}(E_r)\) cannot equal \(\kappa\det(D)\) for any nonzero constant \(\kappa\ne 0\).*

**Proof.** Let \(\beta_r\in\{0,1\}^4\) be the indicator of \(A_r\) (\(\|\beta_r\|_2=\sqrt 2\), \(\mathbf 1_4^\dagger\beta_r=2\)), and set \(v_+=V_{(0,1)}^\dagger\beta_r\), \(v_-=V_{(1,0)}^\dagger\beta_r\). Unitarity and \(V_{\mathbf x}\mathbf 1_4=\mathbf 1_4\) imply \(\|v_+\|_2=\|v_-\|_2=\sqrt 2\) and \(\mathbf 1_4^\dagger(v_++v_-)=4\). On the normalized singular matrix \(D_{\mathrm{flat}}=\frac14\mathbf 1_2\mathbf 1_2^T\) (\(M_2(D_{\mathrm{flat}})=1\), \(\det D_{\mathrm{flat}}=0\)),
\[
\mu_{\mathcal V(D_{\mathrm{flat}}^{\otimes 2}\otimes D_{\mathrm{anc}})\mathcal V^\dagger}(E_r)
= \frac1{16}(v_++v_-)^\dagger D_{\mathrm{anc}}(v_++v_-).
\]
Proportionality to \(\det(D)\) forces this weight to vanish, hence \(v_++v_-\in\ker(D_{\mathrm{anc}})\). Applying Lemma 1B.1 to \(y=v_++v_-\) yields \(16=|\mathbf 1_4^\dagger(v_++v_-)|^2\le 2\|v_++v_-\|_2^2\), so \(\|v_++v_-\|_2\ge 2\sqrt 2=\|v_+\|_2+\|v_-\|_2\). Strict convexity of \(\|\cdot\|_2\) forces \(v_+=v_-\) (with \(v_+\in\ker D_{\mathrm{anc}}\)), making the weight on *every* \(D\in\operatorname{Herm}_2(\mathbb C)\) equal to \(v_+^\dagger D_{\mathrm{anc}}v_+\,(D_{00}D_{11}+D_{01}D_{10})=0\), so \(\kappa=0\). ∎

---

## 3. Target R2 — \(\sim_{\mathscr T}\)-Quotient Escape and Selection of Complex Qubit Residual Geometry

### 3.1 Escaping the rank-1 total-entry-mass trap and excluding \(M_\lambda\)

In [`OPERATION_DOMAIN.md`](../t8-q-operation-domain-2026-09-13/OPERATION_DOMAIN.md), total-entry mass on the unrestricted PSD cone \(K_n=\mathrm{PSD}_n(\mathbb C)\) is \(M_n(D)=\operatorname{Tr}(\Gamma_n D)\) with \(\Gamma_n=\mathbf 1_n\mathbf 1_n^\dagger\) of **rank 1**. On \(K_2\), \(\ker(\Gamma_2)=\operatorname{span}\{|-\rangle\}\) allows the noncompact scaling family \(M_\lambda=P_++\lambda P_-\) (\(\lambda>0\), \(P_\pm=|\pm\rangle\langle\pm|\)) to satisfy \(M_\lambda^\dagger\Gamma_2 M_\lambda=\Gamma_2\) for all \(\lambda\ne 1\).

Now pass to RI-08b's control-viable cone on \(\Omega_4\) ([`CONTROL_SELECTED_QUBIT.md`](../t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md)):
\[
\mathcal C_4 = \left\{D(A,c)=\begin{pmatrix}A&cZ\\\bar c Z&ZAZ\end{pmatrix} : A\in\mathrm{PSD}_2(\mathbb C),\ A\succeq |c|I_2\right\},
\tag{10}
\]
equipped with the silent control group \(\mathcal G_1=\langle S_H,S_P,S_Z\rangle\) and two-cell coarse readout \(\{A_0=\{0,1\},A_1=\{2,3\}\}\). Define future-test equivalence \(D_1\sim_{\mathscr T} D_2\) iff \(\mu_{S(D_1)}(A_r)=\mu_{S(D_2)}(A_r)\) for all \(S\in\mathcal G_1\) and \(r\in\{0,1\}\) ([`QR_MAP_RECORD_SUFFICIENCY.md`](../../track_b/QR_MAP_RECORD_SUFFICIENCY.md)).

**Theorem 2A (\(\sim_{\mathscr T}\)-quotient order-unit lift and exclusion of \(M_\lambda\)).**
1. *For \(D(A_1,c_1),D(A_2,c_2)\in\mathcal C_4\), \(D(A_1,c_1)\sim_{\mathscr T} D(A_2,c_2)\iff A_1=A_2\). The quotient map \(\pi(D(A,c))=\rho:=2A\) is a cone isomorphism \(\mathcal C_4/{\sim_{\mathscr T}}\xrightarrow{\sim}\mathrm{PSD}_2(\mathbb C)\) under which raw total-entry mass \(M_4(D)=\operatorname{Tr}(\Gamma_4 D)\) descends to the **full-rank** trace order unit*
   \[
   M_4(D(A,c)) = 2\operatorname{Tr}(A) = \operatorname{Tr}(I_2\,\rho),\qquad \operatorname{rank}(I_2)=2.
   \tag{11}
   \]
2. *Lifting \(M_\lambda=P_++\lambda P_-\) (\(\lambda>0\)) to \(\mathcal C_4\) via \(\widetilde M_\lambda=\operatorname{diag}(M_\lambda,Z M_\lambda Z)\) yields on the \(\{I,S_H\}\)-reachable preparations \(D_{+X},D_{+Z},D_{-X}=S_H(D_{-Z})\):*
   \[
   M_4(\widetilde M_\lambda D_{+X}\widetilde M_\lambda^\dagger)=1,\quad
   M_4(\widetilde M_\lambda D_{+Z}\widetilde M_\lambda^\dagger)=\frac{1+\lambda^2}2,\quad
   M_4(\widetilde M_\lambda D_{-X}\widetilde M_\lambda^\dagger)=\lambda^2,
   \tag{12}
   \]
   *forcing \(\lambda=1\) as soon as mass preservation holds across \(\{I,S_H\}\)-reachable states.*

**Proof.**
*(1)* For every unitary \(U\in U(2)\) and \(W_U=\operatorname{diag}(U,ZUZ)\), the upper-right block of \(W_U D(A,c)W_U^\dagger\) is \(U(cZ)(ZU^\dagger Z)=c\,UU^\dagger Z=cZ\), so \(W_U D(A,c)W_U^\dagger=D(UAU^\dagger,c)\). Since \(\mathbf 1_2^\dagger Z\mathbf 1_2=1-1=0\), the cross blocks \(cZ\) and \(\bar c Z\) contribute zero to \(M_4\) and are never coupled into the diagonal blocks by \(\mathcal G_1\). On cell \(A_0\), \(\mu_{D(UAU^\dagger,c)}(A_0)=\mathbf 1_2^\dagger(UAU^\dagger)\mathbf 1_2=2\langle +|UAU^\dagger|+\rangle\): choosing \(U\in\{I_2,H,HP^\dagger\}\) reads out \(\operatorname{Tr} A+\operatorname{Re}(2A_{01})\), \(\operatorname{Tr} A+(A_{00}-A_{11})\), and \(\operatorname{Tr} A+\operatorname{Im}(2A_{01})\), while \(\mu(A_0)+\mu(A_1)=\mathbf 1_2^\dagger(A+ZAZ)\mathbf 1_2=2\operatorname{Tr} A\). Thus \(\{S_U\in\mathcal G_1\}\) uniquely determines \(A\) and is completely blind to \(c\), giving \(D(A_1,c_1)\sim_{\mathscr T}D(A_2,c_2)\iff A_1=A_2\) and (11).

*(2)* Every \(D\in\{D_{+Z},D_{-Z},D_{+X},D_{-X}\}\) has \(c=0\), so \(\widetilde M_\lambda D(A,0)\widetilde M_\lambda^\dagger=D(M_\lambda A M_\lambda^\dagger,0)\in\mathcal C_4\). By (11), its mass is \(2\operatorname{Tr}((P_++\lambda^2 P_-)A)\). Substituting \(A=\frac12 P_+\), \(\frac12|0\rangle\langle 0|\), and \(\frac12 P_-\) gives \(1\), \(\frac{1+\lambda^2}2\), and \(\lambda^2\), which equal \(1\) iff \(\lambda^2=1\), i.e., \(\lambda=1\) for \(\lambda>0\). ∎

### 3.2 Identity-atomicity excludes classical cones \(\mathrm{Diag}_+(\Omega_d)\)

Compare three normalized two-outcome quotient cones: any classical diagonal cone \(\mathrm{Diag}_+(\Omega_d)\cong\mathbb R_+^d\) (\(d\ge 2\)), the real rebit quotient cone \(\mathrm{PSD}_2(\mathbb R)\subset\mathrm{Sym}_2(\mathbb R)\), and the complex qubit quotient cone \(\mathrm{PSD}_2(\mathbb C)\subset\operatorname{Herm}_2(\mathbb C)\). Call the identity transformation **reference-completely atomic** if whenever admissible (completely positive) sub-operations \(\{T_x\}\) satisfy \(\sum_x T_x=\mathrm{id}\), each branch satisfies \(T_x=p_x\,\mathrm{id}\) for some scalar \(p_x\ge 0\) ([`RESEARCH.md` §3](../t8-q-principle-selection-research-2026-09-13/RESEARCH.md)).

**Theorem 2B (Identity-atomicity separates \(\mathrm{PSD}_2(\mathbb R),\mathrm{PSD}_2(\mathbb C)\) from \(\mathrm{Diag}_+(\Omega_d)\)).**
1. *For every \(d\ge 2\), \(\mathrm{Diag}_+(\Omega_d)\) violates identity-atomicity.*
2. *Both \(\mathrm{PSD}_2(\mathbb R)\) and \(\mathrm{PSD}_2(\mathbb C)\) satisfy reference-complete identity-atomicity.*

**Proof.**
*(1)* On \(\mathrm{Diag}_+(\Omega_d)\) (\(d\ge 2\)), let \(E_k=\operatorname{diag}(e_k)\) and \(T_k(D)=E_k D E_k\) (\(k=0,\dots,d-1\)). Each \(T_k\) is completely positive on diagonal composites and \(\sum_{k=0}^{d-1}T_k=\mathrm{id}_{\mathrm{Diag}_d}\), yet \(T_0(E_0)=E_0\ne 0\) while \(T_0(E_1)=0\), so \(T_0\notin\mathbb R_+\mathrm{id}\).

*(2)* Let \(\mathbb F\in\{\mathbb R,\mathbb C\}\) and let \(\Psi=\frac12(|00\rangle+|11\rangle)(\langle 00|+\langle 11|)\in\mathrm{PSD}_4(\mathbb F)\). Notice \(\Psi\in\mathrm{PSD}_4(\mathbb R)\subset\mathrm{PSD}_4(\mathbb C)\) is rank-1 (an extreme ray of \(\mathrm{PSD}_4(\mathbb F)\)), and the Choi map \(\mathcal J(T)=(T\otimes\mathrm{id}_2)(\Psi)\) is injective on \(\mathcal L(M_2(\mathbb F))\) because \(\mathcal J(T)_{(i,a),(j,b)}=\frac12\langle i|T(|a\rangle\langle b|)|j\rangle\). If completely positive maps \(\{T_x\}\) on \(\mathrm{PSD}_2(\mathbb F)\) satisfy \(\sum_x T_x=\mathrm{id}\), then \((T_x\otimes\mathrm{id}_2)(\Psi)\in\mathrm{PSD}_4(\mathbb F)\) and \(\sum_x(T_x\otimes\mathrm{id}_2)(\Psi)=\Psi\). Since \(\operatorname{rank}(\Psi)=1\), every PSD summand below \(\Psi\) is a nonnegative multiple of \(\Psi\): \(\mathcal J(T_x)=p_x\Psi=\mathcal J(p_x\mathrm{id})\) with \(p_x\ge 0\). Injectivity of \(\mathcal J\) forces \(T_x=p_x\,\mathrm{id}\). ∎

### 3.3 Generator observability excludes the real rebit without local tomography

To distinguish \(\mathrm{PSD}_2(\mathbb C)\) from \(\mathrm{PSD}_2(\mathbb R)\) *without* assuming bipartite local tomography, recall Barnum–Müller–Ududec **generator observability** ([`RESEARCH.md` §4](../t8-q-principle-selection-research-2026-09-13/RESEARCH.md)): there exists an injective linear correspondence \(\phi:\mathfrak g\to\mathcal O_{\mathrm{lin}}\) from continuous reversible dynamical generators \(D\in\mathfrak g\) to linear observables on the normalized state space such that each \(\phi(D)\) is **conserved by its own flow** (\(\phi(D)\circ D=0\)) and is **non-constant** across normalized states whenever \(D\ne 0\).

**Theorem 2C (Direct rebit obstruction and complex qubit realization).**
1. **Rebit failure:** *On \(\mathrm{Sym}_2(\mathbb R)=\operatorname{span}_{\mathbb R}\{I_2,X,Z\}\) (\(\dim_{\mathbb R}=3\)), the continuous \(SO(2)\) rotation generator \(D_{J_0}(\rho)=[J_0,\rho]\) (\(J_0=\bigl(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\bigr)\)) has image \(\operatorname{im}(D_{J_0})=\operatorname{span}_{\mathbb R}\{X,Z\}\). Every linear functional \(\ell\in\mathrm{Sym}_2(\mathbb R)^*\) conserved by \(D_{J_0}\) (\(\ell\circ D_{J_0}=0\)) belongs to \(\mathbb R\operatorname{Tr}\) and is therefore **constant** (\(\equiv c\)) on all normalized rebit states \(\{\rho\in\mathrm{PSD}_2(\mathbb R):\operatorname{Tr}\rho=1\}\).*
2. **Complex qubit satisfaction:** *On \(\operatorname{Herm}_2(\mathbb C)=\operatorname{span}_{\mathbb R}\{I_2,X,Y,Z\}\) (\(\dim_{\mathbb R}=4\)), the \(\mathfrak{su}(2)\) generators \(D_{-iH}(\rho)=[-iH,\rho]\) (\(H\in\operatorname{Herm}_2^0(\mathbb C)\), \(\operatorname{Tr} H=0\)) admit the injective map \(\phi(D_{-iH})(\rho)=\operatorname{Tr}(H\rho)\), which satisfies \(\phi(D_{-iH})(D_{-iH}(\rho))=0\) for all \(\rho\), is non-constant on normalized states for every \(H\ne 0\), and is not simultaneously conserved by noncommuting generators.*

**Proof.**
*(1)* Direct commutation on \(\{I_2,X,Z\}\) gives \([J_0,I_2]=0\), \([J_0,Z]=2X\), and \([J_0,X]=-2Z\) (since \(iY=-J_0\notin\mathrm{Sym}_2(\mathbb R)\) is absent from the rebit state space!). Hence \(\operatorname{rank}_{\mathbb R}(D_{J_0})=2\) and \(\operatorname{im}(D_{J_0})=\operatorname{span}_{\mathbb R}\{X,Z\}\). If \(\ell(\rho)=\operatorname{Tr}(L\rho)\) (\(L=c_0 I_2+c_x X+c_z Z\in\mathrm{Sym}_2(\mathbb R)\)) satisfies \(\ell(D_{J_0}(\rho))=0\) for all \(\rho\in\mathrm{Sym}_2(\mathbb R)\), evaluating on \(\rho=Z\) and \(\rho=X\) gives \(4c_x=0\) and \(-4c_z=0\), so \(L=c_0 I_2\) and \(\ell=c_0\operatorname{Tr}\).

*(2)* On \(\operatorname{Herm}_2(\mathbb C)\), \(D_{-iH}=0\iff [-iH,\rho]=0\ \forall\rho\iff H\in\mathbb R I_2\iff H=0\) (since \(\operatorname{Tr} H=0\)). If \(\operatorname{Tr}(H\rho)=0\) for all \(\rho\), taking \(\rho=H\) gives \(\operatorname{Tr}(H^2)=0\implies H=0\), proving \(\phi\) injective; choosing \(\rho=\frac12(I_2\pm H/\|H\|)\) gives distinct values on normalized states. Self-conservation follows from cyclic trace invariance \(\operatorname{Tr}(H[-iH,\rho])=-i\operatorname{Tr}([H,H]\rho)=0\), while for \(H'\in\operatorname{Herm}_2^0(\mathbb C)\) with \([H,H']\ne 0\), choosing \(\rho=i[H,H']\in\operatorname{Herm}_2^0(\mathbb C)\) yields \(\operatorname{Tr}(H[-iH',\rho])=\operatorname{Tr}(-i[H,H']\rho)=-\operatorname{Tr}(\rho^2)\ne 0\). ∎

### 3.4 Minimal-rank purity selects compatible complex structures \(J^2=-I_{2m}\)

In [`why_complex.py`](../../../det8/models/why_complex.py), decomposing a positive Hermitian kernel on an even real space \(\mathbb R^{2m}\) as \(D=G+i\Omega\) (\(G\in\operatorname{Sym}_{2m}(\mathbb R)\), \(G\succ 0\), \(\Omega\in\operatorname{Skew}_{2m}(\mathbb R)\)) left open why \(J:=G^{-1}\Omega\) must obey \(J^2=-I_{2m}\), because the damped family \(D_t=\frac12(I_{2m}+itJ_0)\) (\(0\le |t|\le 1\)) is PSD for every \(|t|\le 1\) yet has \(J^2=-t^2 I_{2m}\ne -I_{2m}\) whenever \(|t|<1\).

**Theorem 2D (Minimal-rank characterization of \(J^2=-I_{2m}\)).** *Let \(D=G+i\Omega\in\operatorname{Herm}_{2m}(\mathbb C)\) with \(G\in\operatorname{Sym}_{2m}(\mathbb R)\), \(G\succ 0\), and \(\Omega\in\operatorname{Skew}_{2m}(\mathbb R)\), and define \(J=G^{-1}\Omega\in M_{2m}(\mathbb R)\). Then:*
1. *\(D\succeq 0\iff G+\Omega G^{-1}\Omega\succeq 0\) (equivalently, \(I_{2m}+J^2\) is \(G\)-positive semidefinite);*
2. *Every \(D\succeq 0\) with \(G\succ 0\) satisfies \(\operatorname{rank}_{\mathbb C}(D)\ge m\);*
3. *Equality \(\operatorname{rank}_{\mathbb C}(D)=m\) holds **if and only if** \(J^2=-I_{2m}\) (so \((G,\Omega,J)\) is a compatible Kähler triple).*

**Proof.** Under realification \(\Phi(G+i\Omega)=\bigl(\begin{smallmatrix}G&-\Omega\\\Omega&G\end{smallmatrix}\bigr)\in\operatorname{Sym}_{4m}(\mathbb R)\), every \(z=x+iy\in\mathbb C^{2m}\) obeys \(z^\dagger Dz=(x^T\;y^T)\Phi(D)\binom xy\), and \(z\in\ker_{\mathbb C}D\iff\binom xy,\binom{-y}x\in\ker_{\mathbb R}\Phi(D)\), so \(D\succeq 0\iff\Phi(D)\succeq 0\) and \(\operatorname{rank}_{\mathbb R}\Phi(D)=2\operatorname{rank}_{\mathbb C}(D)\). Since \(G\succ 0\) and \(\Omega^T=-\Omega\), block Gaussian elimination gives the exact congruence
\[
\begin{pmatrix}I_{2m}&0\\-\Omega G^{-1}&I_{2m}\end{pmatrix}
\begin{pmatrix}G&-\Omega\\\Omega&G\end{pmatrix}
\begin{pmatrix}I_{2m}&-G^{-1}\Omega\\0&I_{2m}\end{pmatrix}
= \begin{pmatrix}G&0\\0&G+\Omega G^{-1}\Omega\end{pmatrix}.
\tag{13}
\]
By Sylvester's law of inertia on (13), \(\Phi(D)\succeq 0\iff S:=G+\Omega G^{-1}\Omega\succeq 0\), proving (1), and
\[
2\operatorname{rank}_{\mathbb C}(D) = \operatorname{rank}_{\mathbb R}\Phi(D)
= \operatorname{rank}_{\mathbb R}(G) + \operatorname{rank}_{\mathbb R}(S)
= 2m + \operatorname{rank}_{\mathbb R}(S)\ge 2m,
\tag{14}
\]
proving (2). Moreover, \(\operatorname{rank}_{\mathbb C}(D)=m\iff\operatorname{rank}_{\mathbb R}(S)=0\iff G+\Omega G^{-1}\Omega=0\iff G(I_{2m}+(G^{-1}\Omega)^2)=0\iff J^2=-I_{2m}\) since \(G\succ 0\), proving (3). In [`why_complex.py`](../../../det8/models/why_complex.py)'s family \(D_t=\frac12(I_{2m}+itJ_0)\), \(S=\frac{1-t^2}2 I_{2m}\) has rank \(2m\) for \(|t|<1\) (\(\operatorname{rank}_{\mathbb C}(D_t)=2m\), interior mixed state) and rank \(0\) iff \(t=\pm 1\) (\(\operatorname{rank}_{\mathbb C}(D_{\pm 1})=m\), \(J^2=-I_{2m}\)). ∎

---

## 4. Target R3 — Active Pair-Kernel-to-Growth Causal Diamond Law Through Four Births

### 4.1 Explicit completely positive context-addressed branch family \(\mathcal B^{P,r}_{S,b}\)

Let \(q_C(S)=q(P,r,S)\) be the unchanged Part A four-birth marked structural reference law of [`finite_incidence_register.md`](../../observables/finite_incidence_register.md) (with constants \(q_A=\frac23\), \(q_C=\frac15\), \(q_D=\frac14\), \(q_F(0)=\frac16\), \(q_F(1)=\frac13\), \(q_G=\frac1{10}\), \(q_K=\frac{11}{20}\), \(q_H(0)=\frac{19}{30}\), \(q_H(1)=\frac7{15}\), \(q_E=\frac1{44}\)). Define the unmarked-antichain harmonic potential \(H(P)=a_{|P|}\chi_{\mathrm{antichain}}(P)\) with
\[
(a_0,a_1,a_2,a_3,a_4)=\left(\frac1{264},\;\frac1{264},\;\frac1{176},\;\frac1{44},\;1\right),
\qquad \sum_{S\in\mathcal I(P)}q_C(S)\,H(P+S)=H(P)\quad(0\le |P|\le 3),
\tag{15}
\]
as in [`native_active_residual_v1.md`](../../track_b/native_active_residual_v1.md). Fix coherent survival fraction \(t=\frac12\), coupling amplitude \(\theta=\frac1{32}\), initial phase axis \(\mathbf w_0=(0,1,0)^T\) (the **purely imaginary \(Y\)-quadrature**), and Bloch quarter-rotation \(O_P=\bigl(\begin{smallmatrix}0&-1&0\\1&0&0\\0&0&1\end{smallmatrix}\bigr)\) satisfying \(P(\mathbf w\cdot\vec\sigma)P^\dagger=(O_P\mathbf w)\cdot\vec\sigma\) and \(P^\dagger(\mathbf w\cdot\vec\sigma)P=(O_P^{-1}\mathbf w)\cdot\vec\sigma\).

For any marked parent \(C=(P,r)\) of size \(n=|P|\in\{0,1,2,3\}\), ideal \(S\in\mathcal I(P)\), and newborn mark \(b\in\{0,1\}\), define the context-addressed Bloch coupling vector, strictly positive-definite \(4\times 4\) effect \(G_{\mathbf r_C(S)}\), and branch map \(\mathcal B^{P,r}_{S,b}:M_4(\mathbb C)\to M_4(\mathbb C)\) by
\[
\mathbf r_C(S) := \theta\,2^n\,[H(P+S)-H(P)]\,O_P^n\mathbf w_0\in\mathbb Q^3,
\tag{16}
\]
\[
F_{\mathbf r} := (1-t)I_2 + \mathbf r\cdot\vec\sigma,\qquad
G_{\mathbf r} := \operatorname{diag}(F_{\mathbf r},\;Z F_{\mathbf r} Z),
\tag{17}
\]
\[
\boxed{\mathcal B^{P,r}_{S,b}(D) := \frac{q_C(S)}{2}\left(t\,W_P D W_P^\dagger + \operatorname{Tr}\!\bigl(G_{\mathbf r_C(S)}D\bigr)\,\frac14 I_4\right).}
\tag{18}
\]

### 4.2 Complete positivity, normalization, sequential noncommutativity, and exact \(16\times 16\) diamonds

**Theorem 3A (Admitted four-birth active pair-kernel diamond law).** *Across all reachable marked prefixes \(0\le |P|\le 3\), ideals \(S\in\mathcal I(P)\), and bits \(b\in\{0,1\}\), the family (16)–(18) satisfies:*

1. **Strict complete positivity and \(\mathcal C_4\)-invariance:** *\(\|\mathbf r_C(S)\|_2\le\frac{43}{176}<\frac12=1-t\), so \(G_{\mathbf r_C(S)}\succ 0\), \(\mathcal B^{P,r}_{S,b}(\mathcal C_4)\subseteq\mathcal C_4\), and whenever \(q_C(S)>0\) its \(16\times 16\) Choi matrix*
   \[
   \operatorname{Choi}\!\bigl(\mathcal B^{P,r}_{S,b}\bigr)
   = \frac{q_C(S)}{2}\left(t\,|\operatorname{vec}(W_P)\rangle\langle\operatorname{vec}(W_P)| + G_{\mathbf r_C(S)}^T\otimes\frac14 I_4\right)
   \tag{19}
   \]
   *is **strictly positive-definite** on \(\mathbb C^{16}\).*
2. **Complete-row normalization and relabeling covariance:** *For every parent \(C=(P,r)\), \(\sum_{S\in\mathcal I(P)}\sum_{b\in\{0,1\}}\operatorname{Tr}(\mathcal B^{P,r}_{S,b}(D))=\operatorname{Tr}(D)\) on all \(D\in M_4(\mathbb C)\) and \(\sum_{S,b}M_4(\mathcal B^{P,r}_{S,b}(D))=M_4(D)\) on \(\mathcal C_4\), and \(\mathcal B^{\pi(P),\pi(r)}_{\pi(S),b}=\mathcal B^{P,r}_{S,b}\) for every poset isomorphism \(\pi\).*
3. **Timelike sequential noncommutativity:** *Along the two-step chain \(\varnothing\xrightarrow{S_1=\varnothing}C_1\xrightarrow{S_2=\{0\}}C_2\), the sequential branch superoperators do **not** commute:*
   \[
   \bigl[\mathcal B^{C_1,r_1}_{\{0\},b_2},\;\mathcal B^{\varnothing}_{\varnothing,b_1}\bigr]\ne 0,
   \tag{20}
   \]
   *escaping the commutativity constraint of [`finite_homogeneous_compensation.md`](../../track_b/finite_homogeneous_compensation.md).*
4. **Exact \(16\times 16\) spacelike causal diamonds:** *For every labeled marked base \(C=(P,r)\) of size \(|P|\le 2\) (all \(15\) labeled marked posets on \(\le 2\) vertices, including non-canonical \(1\prec 0\) labelings, yielding \(4+32+544=580\) marked diamonds), every pair of ideals \(S,T\in\mathcal I(P)\), and every \((b,c)\in\{0,1\}^2\),*
   \[
   \boxed{\mathcal B^{C+x_S,r+b}_{T,c}\circ\mathcal B^{C,r}_{S,b}
   = \mathcal B^{C+y_T,r+c}_{S,b}\circ\mathcal B^{C,r}_{T,c}}
   \tag{21}
   \]
   *holds identically as \(16\times 16\) linear superoperators on **all** of \(M_4(\mathbb C)\).*

**Proof.**
*(1)* For \(0\le n\le 3\), \(2^n|H(P+S)-H(P)|\le 8(1-\frac1{44})=\frac{344}{44}=\frac{86}{11}\), so \(\|\mathbf r_C(S)\|_2\le\frac1{32}\cdot\frac{86}{11}=\frac{43}{176}<\frac12\). Thus \(\operatorname{spec}(F_{\mathbf r})=\{\frac12\pm\|\mathbf r\|_2\}\subset[\frac{45}{176},\frac{131}{176}]\), giving \(F_{\mathbf r}\succ 0\) and \(G_{\mathbf r}\succ 0\). Consequently \(G_{\mathbf r}^T\otimes\frac14 I_4\succ 0\) while \(t|\operatorname{vec}(W_P)\rangle\langle\operatorname{vec}(W_P)|\succeq 0\), proving \(\operatorname{Choi}(\mathcal B^{P,r}_{S,b})\succ 0\) whenever \(q_C(S)>0\) (with rank-17 Kraus operators \(K_0=\sqrt{q_C(S)t/2}\,W_P\) and \(K_{v,u}=\sqrt{q_C(S)/8}\,|v\rangle\langle\phi_u|\) for any decomposition \(G_{\mathbf r}=\sum_{u=0}^3|\phi_u\rangle\langle\phi_u|\)). On \(D(A,c)\in\mathcal C_4\), \(W_P D(A,c)W_P^\dagger=D(PAP^\dagger,c)\in\mathcal C_4\) and \(\frac14 I_4=D(\frac14 I_2,0)\in\mathcal C_4\) with \(\operatorname{Tr}(G_{\mathbf r}D)\ge 0\), so \(\mathcal C_4\) is preserved.

*(2)* By (15)–(16), \(\sum_{S\in\mathcal I(P)}q_C(S)\mathbf r_C(S)=0\). Summing (18) over \(b\in\{0,1\}\) and \(S\in\mathcal I(P)\) cancels \(\mathbf r_C(S)\), leaving \(\mathcal U(D):=t\,W_P D W_P^\dagger+(1-t)\operatorname{Tr}(D)\frac14 I_4\), which satisfies \(\operatorname{Tr}(\mathcal U(D))=\operatorname{Tr}(D)\) on \(M_4(\mathbb C)\) and \(M_4(\mathcal U(D))=M_4(D)\) on \(\mathcal C_4\) (since \(M_4(D)=\operatorname{Tr}(D)\) on \(\mathcal C_4\) by Theorem 2A(1)). Relabeling covariance holds because \(q_C(S)\), \(n=|P|\), and \(\chi_{\mathrm{antichain}}\) are isomorphism invariants.

*(3)–(4)* For any \(\mathbf w\in\mathbb R^3\), define the traceless functional \(\ell_{\mathbf w}(D):=\operatorname{Tr}\bigl(\operatorname{diag}(\mathbf w\cdot\vec\sigma,\,Z(\mathbf w\cdot\vec\sigma)Z)\,D\bigr)\) on \(M_4(\mathbb C)\). Direct trace evaluation yields two exact identities on **all** \(D\in M_4(\mathbb C)\):
\[
\ell_{\mathbf w}\!\left(\frac14 I_4\right)=0,\qquad
\ell_{\mathbf w}\bigl(\mathcal U(D)\bigr) = t\,\ell_{O_P^{-1}\mathbf w}(D),
\tag{22}
\]
together with \(\mathcal U(\frac14 I_4)=\frac14 I_4\). Rewrite (18) as \(\mathcal B^{C,r}_{S,b}(D)=\frac{q_C(S)}2\bigl(\mathcal U(D)+\ell_{\mathbf r_C(S)}(D)\frac14 I_4\bigr)\). For the timelike chain step in (20), \(\mathbf r_{\varnothing}(\varnothing)=0\) (since \(a_1=a_0=\frac1{264}\)) while \(\mathbf r_{C_1}(\{0\})=-\frac1{32}\cdot 2\cdot\frac1{264}O_P\mathbf w_0=\frac1{4224}(1,0,0)^T\ne 0\): on \(D_{+X}\) (\(\ell_{(1,0,0)}(D_{+X})=1\)), \(\mathcal U(D_{+X})=tD_{+Y}+(1-t)\frac14 I_4\) has \(\ell_{(1,0,0)}(\mathcal U(D_{+X}))=0\), whereas applying \(\mathcal B^{C_1,r_1}_{\{0\},b_2}\) first injects \(\frac1{4224}\cdot\frac14 I_4\) before \(\mathcal U\) acts, yielding nonzero commutator (20).

Now compose any two incomparable steps at base \(C=(P,r)\) (\(|P|=n\le 2\)) on arbitrary \(D\in M_4(\mathbb C)\). By (22), the quadratic cross-term \(\ell_{\mathbf r_{C+x_S}(T)}(\frac14 I_4)\) vanishes identically and \(t\,O_P^{-1}O_P^{n+1}\mathbf w_0=\frac12 O_P^n\mathbf w_0\), so the linear functional coefficients telescope:
\[
\ell_{\mathbf r_{C+x_S}(T)}\bigl(\mathcal U(D)\bigr) + \ell_{\mathbf r_C(S)}(D)
= \theta\,2^n\bigl([H(P+S+T)-H(P+S)] + [H(P+S)-H(P)]\bigr)\,\ell_{O_P^n\mathbf w_0}(D)
= \theta\,2^n\,[H(P+S+T)-H(P)]\,\ell_{O_P^n\mathbf w_0}(D).
\]
Hence
\[
\bigl(\mathcal B^{C+x_S,r+b}_{T,c}\circ\mathcal B^{C,r}_{S,b}\bigr)(D)
= \frac{q_C(S)\,q_{C+x_S,r+b}(T)}{4}\left(\mathcal U^2(D) + \theta\,2^n\,[H(P+S+T)-H(P)]\,\ell_{O_P^n\mathbf w_0}(D)\,\frac14 I_4\right).
\tag{23}
\]
By Part A's scalar diamond law, \(q_C(S)q_{C+x_S,r+b}(T)=q_C(T)q_{C+y_T,r+c}(S)\), and up to canonical birth-order isomorphism \(P+S+T\cong P+T+S\), so \(H(P+S+T)=H(P+T+S)\). Thus (23) is symmetric under \((S,b)\leftrightarrow(T,c)\) for every \(D\in M_4(\mathbb C)\), proving (21). ∎

### 4.3 Purely imaginary initial phase shifts four-birth causal order and the \((\Delta_4,C_4)\) classical comparator

Compare the two initial states \(D_{+Y}=S_P(S_H(D_{+Z}))\) and \(D_{-Y}=S_Z(D_{+Y})\) in \(\mathcal C_4\):
\[
D_{\pm Y} = \frac14\begin{pmatrix}
1&\mp i&0&0\\
\pm i&1&0&0\\
0&0&1&\pm i\\
0&0&\mp i&1
\end{pmatrix},\qquad
\operatorname{Re}(D_{+Y})=\operatorname{Re}(D_{-Y})=\frac14 I_4.
\tag{24}
\]
Because scalar event weights depend only on \(\operatorname{Re}(D)\), \(D_{+Y}\) and \(D_{-Y}\) have **identical initial weights \(\mu(A)=|A|/4\) on all \(2^4=16\) Boolean subsets \(A\subseteq\Omega_4\)**. Let \(Z(P_4)=\chi_{\mathrm{antichain}}(P_4)\in\{0,1\}\) be the terminal four-birth unmarked-antichain indicator across all \(640\) complete four-birth marked histories \(\gamma\).

**Theorem 3B (Purely imaginary phase drives four-birth causal structure).**
1. *For every normalized \(D\in\mathcal C_4\) (\(M_4(D)=1\)), summing \(\mathcal B_\gamma(D)\) over all \(640\) four-birth marked histories yields the exact closed-form endpoint law*
   \[
   P(Z=1\mid D) = a_0 + \theta\,a_0(1-a_0)\,\ell_{\mathbf w_0}(D),\qquad
   P(Z=0\mid D) = 1 - P(Z=1\mid D).
   \tag{25}
   \]
2. *In particular, \(D_{+Y}\) and \(D_{-Y}\) (\(\ell_{\mathbf w_0}(D_{\pm Y})=\pm 1\)) induce strictly distinct four-birth causal-order distributions despite \(\operatorname{Re}(D_{+Y})=\operatorname{Re}(D_{-Y})=\frac14 I_4\):*
   \[
   P(Z=1\mid D_{+Y})=\frac{8711}{2{,}230{,}272},\quad
   P(Z=1\mid D_{-Y})=\frac{8185}{2{,}230{,}272},\quad
   \boxed{\Delta_Z := P(Z=1\mid D_{+Y})-P(Z=1\mid D_{-Y})=\frac{263}{1{,}115{,}136},}
   \tag{26}
   \]
   *whereas \(D_{\pm X}\) and \(D_{\pm Z}\) have \(\ell_{\mathbf w_0}=0\) and zero contrast (\(P(Z=1\mid D_{\pm X})=P(Z=1\mid D_{\pm Z})=\frac1{264}\)). Applying \(k\in\{0,1,2,3\}\) pre-trial silent quarter-phase pulses \(S_P^k\) rotates the contrast cyclic-quadrature-wise: \((0,+\Delta_Z,0,-\Delta_Z)\) on \(D_{\pm X}\) and \((+\Delta_Z,0,-\Delta_Z,0)\) on \(D_{\pm Y}\).*
3. **Classical mixed-state comparator boundary:** *On the four-state classical simplex \(\Delta_4\subset\mathbb R_+^4\) with cyclic shift \(C_4(p_0,p_1,p_2,p_3)=(p_3,p_0,p_1,p_2)\), the valid effect \(e_{Z=1}=(a_0,\,a_0+2v,\,a_0,\,a_0-2v)^T\in(0,1)^4\) (\(v=\theta a_0(1-a_0)=\frac{263}{2{,}230{,}272}\)) and mixed states \(c_{+X}=(\frac12,\frac14,0,\frac14)^T\), \(c_{-X}=(0,\frac14,\frac12,\frac14)^T\), \(c_{\pm Y}=C_4 c_{\pm X}\) reproduce the exact four-step table (26). Thus single-wing attenuated causal-order readout proves genuine complex-phase-to-growth coupling inside \(\mathcal C_4\), while full exclusion of arbitrary-\(d\) classical mixed comparators still relies on Target R2's cone-selection principles (or Theorem 3B–3C of [`BRIDGE_THEOREM.md`](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md)).*

**Proof.**
*(1)–(2)* Iterating the telescoping identity (23) four times from \(C=\varnothing\) (\(n=0\)) along any complete four-birth marked history \(\gamma\) ending at \(P_4\) gives
\[
\mathcal B_\gamma(D) = P_{\mathrm{ref}}(\gamma)\left(\mathcal U^4(D) + \theta\,[H(P_4)-H(\varnothing)]\,\ell_{\mathbf w_0}(D)\,\frac14 I_4\right),
\tag{27}
\]
where \(P_{\mathrm{ref}}(\gamma)\) is the Part A scalar probability of \(\gamma\). Taking \(M_4\) on normalized \(D\in\mathcal C_4\) uses \(M_4(\mathcal U^4(D))=1\) and \(M_4(\frac14 I_4)=1\). Because \(H(P)\) is a \(q\)-martingale (15), \(\sum_\gamma P_{\mathrm{ref}}(\gamma)H(P_4)=H(\varnothing)=a_0=\frac1{264}\); since \(H(P_4)=a_4\chi_{\mathrm{antichain}}(P_4)=\chi_{\mathrm{antichain}}(P_4)\), \(\sum_{Z(P_4)=1}P_{\mathrm{ref}}(\gamma)=a_0\). Summing (27) over \(Z(P_4)=1\) gives \(a_0+\theta a_0(1-a_0)\ell_{\mathbf w_0}(D)\), proving (25). Substituting \(a_0=\frac1{264}\), \(\theta=\frac1{32}\), and \(\ell_{\mathbf w_0}(D_{\pm Y})=\pm 1\) gives \(\frac1{264}\pm\frac{263}{2{,}230{,}272}=\frac{8448\pm 263}{2{,}230{,}272}\), i.e., (26). Since \(\ell_{\mathbf w_0}(S_P^k(D))=\ell_{O_P^{-k}\mathbf w_0}(D)\) and \(O_P^{-1}(0,1,0)^T=(1,0,0)^T\), pre-trial \(S_P^k\) cycles \(\ell_{\mathbf w_0}\) through \((0,+1,0,-1)\) on \(D_{\pm X}\) and \((+1,0,-1,0)\) on \(D_{\pm Y}\).

*(3)* Since \(2v=\frac{263}{1{,}115{,}136}<\frac1{264}=a_0\), every coordinate of \(e_{Z=1}\) lies strictly in \((0,1)\), each \(c_{\pm X},c_{\pm Y}\in\Delta_4\) is a mixed probability vector supported on three vertices, \(C_4\) is a stochastic permutation matrix, and direct dot products yield \(e_{Z=1}\cdot c_{\pm Y}=a_0\pm v\) and \(e_{Z=1}\cdot c_{\pm X}=a_0\), matching (26) across all \(k\in\{0,1,2,3\}\). ∎

---

## 5. Integrated Conditional Chain and Remaining Open Obligations

Combining [`BRIDGE_THEOREM.md`](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md) with Theorems 1A, 2A–2D, and 3A–3B yields an end-to-end conditional architecture in which relational identity \(\sim_{\mathscr T}\) connects silent activity, coarse-cell strong positivity, complex qubit state-space selection, Hilbert/Born readout, and active four-birth causal growth:

\[
\begin{aligned}
&\text{Silent } S_P \text{ interchange} \implies D\odot E = D\otimes E,\quad \text{2-copy record grouping} \implies D(A_r,A_s)=0\quad\text{([BRIDGE\_THEOREM.md](../t8-q-pair-kernel-bridge-2026-10-31/BRIDGE_THEOREM.md))} \\
&\quad+\;\text{Walsh section } J_n(D) + \sim_{\mathscr T}\text{-lifted dyadic coupler } \mathcal U_I \implies \mu(C_*)=\tfrac{|I|!}{2^k}\det(D_I)\ge 0 \iff D\succeq 0\quad\text{(Theorem 1A, zero sub-cell addressing)} \\
&\quad+\;\mathcal C_4/{\sim_{\mathscr T}} + \text{identity-atomicity} + \text{generator observability} + \text{minimal-rank purity} \implies \mathrm{PSD}_2(\mathbb C)\ \&\ J^2=-I_{2m}\quad\text{(Theorems 2A–2D)} \\
&\quad+\;\text{Context-addressed CP branch family } \mathcal B^{P,r}_{S,b} \implies \text{580 exact } 16\times 16 \text{ diamonds}\ \&\ \operatorname{Im}(D_{\pm Y})\to\Delta_Z=\tfrac{263}{1{,}115{,}136}\quad\text{(Theorems 3A–3B)}.
\end{aligned}
\]

**What still remains open from bare DET causal posets \((V,\prec,r)\) alone:**
1. **Grade-2 pair calculus from primitive uncommitted history dynamics:** Deriving why uncommitted alternatives carry a grade-2 biadditive pair functional rather than grade-1 classical weights or grade-\(\ge 3\) Sorkin interference ([`grade2_justification.py`](../../../det8/models/grade2_justification.py)).
2. **Native operational emergence of couplers and continuous generators:** Deriving physical availability of the \(\sim_{\mathscr T}\)-lifted couplers \(\mathcal U_I\) and continuous reversible flows \(\mathfrak g\) from DET micro-dynamics rather than declaring them as operational premises.
3. **Unattenuated multi-wing causal-diamond Bell separation and physical scales:** Extending Theorem 3A–3B from single-wing attenuated visibility (\(\Delta_Z=263/1{,}115{,}136\), which admits the \((\Delta_4,C_4)\) mixed comparator) to a two-wing spacelike-separated causal-growth CHSH witness exceeding \(2\), and addressing Track A/B physical scale/geometry questions. Option B (gravity) and Status M (open becoming) remain unchanged ([`GOVERNANCE.md`](../../../GOVERNANCE.md)).

---

## 6. Exact Verification Record

[`check.py`](check.py) is a self-contained Python standard-library test suite (`fractions.Fraction`, `itertools`, `unittest`, and an exact immutable Gaussian-rational type `G`) with zero floating-point operations or third-party dependencies. Its seven test methods verify:

1. `test_01_walsh_section_and_dyadic_coarse_cell_minors`: Full \(16\times 16\) raw two-copy verification of \(J_2(D)\) (PSD and non-PSD) and \(12\)-label verification of \(J_3(D)\) across all \(7\) principal minors (\(m=1,2,3\), including a \(3\times 3\) matrix with positive \(1\times 1\) and \(2\times 2\) minors and \(\det<0\)) using exact dyadic-rational unitaries \(\mathcal U_I\) with a single ancilla \(D_{+Z}\), confirming coarse decoherence, \(M=1\), and \(\mu(C_*)=\frac{|I|!}{2^k}\det(D_I)\).
2. `test_02_single_ancilla_raw_mass_preserving_obstruction`: Verification across pure \(c=0\) boundary states, \(|c|=1/4\) mixed boundary states, and full-rank interior states of \(\mathcal C_4\) that every mass-preserving ancilla permutation pair \(v_+\ne v_-\) produces strictly positive permanent contamination \((v_++v_-)^\dagger D_{\mathrm{anc}}(v_++v_-)>0\) on \(\det=0\) inputs.
3. `test_03_quotient_escape_and_noncompact_scaling_exclusion`: Verification of \(\operatorname{rank}(\Gamma_4)=1\) versus \(\sim_{\mathscr T}\)-indistinguishability of \(D(A,0)\) and \(D(A,c)\) across all \(24\) octahedral Clifford images in \(\langle S_H,S_P,S_Z\rangle\), and failure of \(M_4\) preservation for lifted \(\widetilde M_\lambda\) (\(\lambda\in\{1/2,2,3/2\}\)) on \(D_{+Z}\) and \(D_{-X}=S_H(D_{-Z})\).
4. `test_04_identity_atomicity_and_generator_observability`: Coordinate-instrument refutation of identity-atomicity on \(\mathrm{Diag}_+(\Omega_d)\) (\(d=2,3,4\)), rank-1 Bell-Choi injectivity (rank \(16\)) on \(M_2\), rank-\(2\) commutator image \(\operatorname{im}(D_{J_0})=\operatorname{span}\{X,Z\}\) on \(\mathrm{Sym}_2(\mathbb R)\) forcing \(\ker(D_{J_0}^*)=\mathbb R\operatorname{Tr}\), and rank-\(3\) self-conserved injective \(\mathfrak{su}(2)\) observables on \(\operatorname{Herm}_2(\mathbb C)\).
5. `test_05_minimal_rank_characterizes_compatible_complex_structure`: Verification of Schur-complement PSD equivalence, \(\operatorname{rank}_{\mathbb C}(D)\ge m\), and \(\operatorname{rank}_{\mathbb C}(D)=m\iff (G^{-1}\Omega)^2=-I_{2m}\) on [`why_complex.py`](../../../det8/models/why_complex.py)'s \(D_t\) family (\(m=1,2\)) and on an anisotropic metric \(G=\operatorname{diag}(1,4,9,1)\).
6. `test_06_active_pair_kernel_cp_normalization_and_superoperator_diamonds`: Strict positive-definiteness of \(G_{\mathbf r}\) and all \(16\times 16\) Choi matrices, \(\mathcal C_4\) cone invariance, harmonic martingale cancellation, complete-row \(\operatorname{Tr}\) and \(M_4\) normalization, poset-relabeling covariance, timelike sequential noncommutativity \([\mathcal B_2,\mathcal B_1]\ne 0\), and exact \(16\times 16\) superoperator equality across all \(580\) labeled marked causal diamonds (\(|C|\le 2\)).
7. `test_07_purely_imaginary_phase_drives_four_birth_causal_order`: Equality of \(\operatorname{Re}(D_{+Y})=\operatorname{Re}(D_{-Y})=\frac14 I_4\) and all \(16\) initial Boolean subset weights \(\mu(A)=|A|/4\), complete summation of all \(640\) four-birth marked histories yielding \(P(Z=1\mid D_{+Y})=8711/2{,}230{,}272\), \(P(Z=1\mid D_{-Y})=8185/2{,}230{,}272\), and \(\Delta_Z=263/1{,}115{,}136\), four-step \(S_P^k\) quadrature rotation, and exact agreement of the \(d=4\) mixed-state classical cyclic-simplex comparator \((\Delta_4,C_4)\).

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/validation/t8-q-relational-identity-completion-2026-10-31/check.py -v
PYTHONDONTWRITEBYTECODE=1 python3 -B -O docs/validation/t8-q-relational-identity-completion-2026-10-31/check.py -v
```

Checked source SHA-256 (`check.py`):
`a591981cd1fb64c144a6358860b7e705bd035693c7b5183a82621dc5320d9f96`.
