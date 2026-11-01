# Upstream Pair-Kernel Bridge: Silent-Activity Interchange, Composite Record Grouping, and Classical Residual Separation

31 October 2026. **CONDITIONAL_UPSTREAM_BRIDGE_THEOREMS; COUNTERMODELS_AND_PREMISE_BOUNDARIES_EXPLICIT.**

**Integration audit notice (31 October 2026, Pacific/Honolulu):** the
[current claim and verification ledger](../qr-bridge-integration-2026-10-31/ADOPTION.md)
records the review disposition and subsequent conditional links. In particular,
real-incidence naturality here means all real rectangular maps; the later
coarse-cell result uses a specified encoded section and added controls.
The checker source below has not been independently executed in this
integration. Its listed commands and matching hash are not execution receipts.
The original protocol and checker remain unchanged; the pre-audit note is
preserved at Git revision `50be57d85aab1bf0396143694b4f9c32632010de`.

Prospective protocol frozen prior to analysis in [`PROTOCOL.md`](PROTOCOL.md) (`bab724b`). This study leaves all existing accepted documents, executors, registries, and branches untouched. No global DET axiom, physical apparatus availability, complex-field derivation, native causal growth law \(q(P,r,S)\), geometry, or empirical claim is asserted.

---

## 1. Executive Summary and Premise-to-Conclusion Map

The [strict finite reconstruction](../t8-q-strict-derivation-2026-09-12/DERIVATION.md) already proves that an admitted complex, Hermitian, biadditive, normalized, strongly positive pair-kernel \(D\) canonically defines a finite Hilbert space \(\mathcal H_D\), norm-squared event weights \(\mu(A)=\|A\|_D^2\), and Born-form record probabilities \(K(r)=\|P_r\psi\|_D^2\) on any declared exactly decoherent partition. Upstream composition studies ([RI-20](../../coordination/QR_COMPOSITION_PREMISE_PLAN.md), [RI-21](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md), [RI-22](../../coordination/QR_COMPOSITION_INDEPENDENCE_PLAN.md)) showed that scalar statistical independence alone neither fixes the event-pair tensor product \(D\otimes E\), nor forces single-copy additive records to be orthogonal, nor supplies the signed seed required for finite-copy strong positivity.

Using the semantic separation between silent residual activity (`evolve_residual`), commitment (`commit_record`), and passive record grouping (`access_records`) in [`RECORD_PROCESS_CONTRACT.md`](../../track_b/RECORD_PROCESS_CONTRACT.md), this note proves three connected bridge theorems together with exact deletion countermodels:

| Bridge component | Load-bearing operational premises | Proved mathematical conclusion | Exact obstruction when a premise is omitted |
|---|---|---|---|
| **Theorem 1** (§2): Composition classification & \(\otimes\) selection | Pre-PSD Hermitian biadditive calculus; unit \([1]\); real-incidence naturality; independent local interchange (or local product-cell positivity) for silent quarter-phase \(S_P\) on \(S_H(D_{+Z})\) | Classifies *all* real-incidence-natural Hermitian bilinear products as the associative family \(D\odot_\alpha E = R\otimes S + \alpha(J\otimes K) + i(J\otimes S + R\otimes K)\) (\(\alpha\in\mathbb R\)), and uniquely selects \(\alpha=-1\) (\(D\otimes E\)) | Deleting \(S_P\) while keeping all real controls \(\langle S_H,S_Z\rangle\) leaves every \(\alpha\in[-1,1]\)—including RI-22's \(\star\) (\(\alpha=0\))—valid and weakly positive on all PSD inputs |
| **Theorem 2** (§3): Composite committed-record grouping | Single-copy additive \(k\)-cell partition \(\mathcal P\); two-copy product composition \(\odot_\alpha\) with \(\alpha\ne 0\); additivity under Boolean coincidence grouping of committed outcomes | Coincidence grouping discrepancy equals \(2\alpha\,t_{rs}^2\), forcing \(J(A_r,A_s)=0\) and hence exact complex decoherence \(D(A_r,A_s)=0\) (\(\langle A_r|A_s\rangle_D=0\) once \(D\succeq 0\)) | Single copy allows \(D_{\mathrm{imag}}(1/4)\succ 0\) with \(D(\{0\},\{1\})=i/4\ne 0\); RI-22's \(\alpha=0\) passes all \(m\)-copy groupings with \(t_{rs}\ne 0\); internal zero-sum \(cZ\) still requires RI-08d's coupler |
| **Theorem 3A** (§4.1): Classical-to-seed principal-minor lift | Ordinary tensor law (\(\alpha=-1\) from Theorem 1); classical diagonal \(D_{+Z}=\operatorname{diag}(1/2,0,1/2,0)\); one silent \(S_H\); nonnegativity of \(2^n-1\) Boolean catalogue weights on \(D^{\otimes n}\otimes S_H(D_{+Z})\) | \(D_{+X}=S_H(D_{+Z})\) has \(M=1\), \(\operatorname{Tr}=1\), and exact two-cell decoherence, and yields \(\mu(\widetilde E_I^{\mathrm{nat}})=\frac{|I|!}4\det(D_I)\), characterizing \(D\succeq 0\) without RI-21's trace-three unrecordable seed | Without \(S_H\) (diagonal classical ancillas only), non-PSD \(D_3=(J_3-I_3)/6\) and \(D_i\) pass ([RI-20 §6](../../coordination/QR_COMPOSITION_PREMISE_PLAN.md#6-exact-countermodels-and-what-each-one-refutes)) |
| **Theorem 3B–3C** (§§4.2–4.3): Separation from classical active residuals \(\mathbb R_+^d\) | Reversible silent controls on extreme preparations (\(\forall d\ge 1\)), or bipartite local silent controls after one RI-08d shared coupler (\(\forall d_A,d_B\ge 1\), mixed states & noisy effects allowed) | Classical reversible maps on \(\Delta_d\) are permutations giving \(\{0,1\}\) sharp weights on extreme states; bipartite classical cones obey \(|S_{\mathrm{CHSH}}|\le 2\), whereas exact rational local silent controls on \(N'\) give \(S_{\mathrm{CHSH}}=14/5>2\) | Dropping extreme-state purity on a single system admits an explicit 6-state permutation witness on \(\Delta_6\) achieving \((1,1/2,0)\) |

---

## 2. Silent-Activity Interchange Selects the Full Event-Pair Tensor Law

### 2.1 Complete classification of real-incidence-natural Hermitian products

For each finite carrier \(\Omega_n=\{0,\dots,n-1\}\) (\(n\ge 1\)), write \(D=R+iJ\in\operatorname{Herm}_n(\mathbb C)\) with \(R\in\operatorname{Sym}_n(\mathbb R)\), \(J\in\operatorname{Skew}_n(\mathbb R)\), scalar weight \(\mu_D(A)=\chi_A^T R\chi_A\), and total-entry mass \(M(D)=\mathbf 1_n^\dagger D\mathbf 1_n=\mathbf 1_n^T R\mathbf 1_n\). Following [RI-22 §3](../../coordination/QR_COMPOSITION_INDEPENDENCE_PLAN.md#3-complex-marginals-scalar-independence-and-real-map-naturality), let \(\Gamma_U(D)=UDU^T\) for any real rectangular matrix \(U\in\mathbb R^{n'\times n}\).

**Theorem 1A (One-parameter classification).** *Let \(\{\odot_{n,k}:\operatorname{Herm}_n(\mathbb C)\times\operatorname{Herm}_k(\mathbb C)\to\operatorname{Herm}_{nk}(\mathbb C)\}_{n,k\ge 1}\) be a family of real-bilinear maps satisfying:*
1. **Unit:** *\([1]\odot E = E\) and \(D\odot[1] = D\) under canonical carrier identification;*
2. **Real-incidence naturality:** *\(\Gamma_U(D)\odot\Gamma_V(E)=\Gamma_{U\otimes V}(D\odot E)\) for all real rectangular matrices \(U\in\mathbb R^{n'\times n}\), \(V\in\mathbb R^{k'\times k}\).*

*Then there exists a unique real constant \(\alpha\in\mathbb R\) such that for every \(n,k\ge 1\) and every \(D=R+iJ\in\operatorname{Herm}_n(\mathbb C)\), \(E=S+iK\in\operatorname{Herm}_k(\mathbb C)\),*
\[
\boxed{D\odot_\alpha E = R\otimes S + \alpha\,(J\otimes K) + i\,(J\otimes S + R\otimes K).}
\tag{1}
\]
*Conversely, for every \(\alpha\in\mathbb R\), \(\odot_\alpha\) satisfies unit, real-incidence naturality, swap covariance, universal associativity, mass-scaled complex whole-carrier marginals (reducing to the original factors on normalized inputs), and rectangular scalar independence \(\mu_{D\odot_\alpha E}(A\times C)=\mu_D(A)\mu_E(C)\).*

**Proof.** By real bilinearity it suffices to evaluate \(\odot\) on \((R,0)\times(S,0)\), \((iJ,0)\times(S,0)\), \((R,0)\times(iK)\), and \((iJ,0)\times(iK)\).

1. *Symmetric–symmetric sector:* By the unit axiom, \([1]\odot[1]=[1]\). For any column vectors \(u\in\mathbb R^{n\times 1}\) and \(v\in\mathbb R^{k\times 1}\), \(\Gamma_u([1])=uu^T\) and \(\Gamma_v([1])=vv^T\). Real-incidence naturality gives
   \[
   (uu^T)\odot(vv^T) = (u\otimes v)([1]\odot[1])(u\otimes v)^T = (uu^T)\otimes(vv^T).
   \]
   Because rank-one matrices \(\{uu^T:u\in\mathbb R^n\}\) span \(\operatorname{Sym}_n(\mathbb R)\) (via \((e_a+e_b)(e_a+e_b)^T - e_ae_a^T - e_be_b^T = e_ae_b^T+e_be_a^T\)), real bilinearity forces \(R\odot S = R\otimes S\) for all \(R,S\).

2. *Mixed real/imaginary sectors:* Let \(\Omega_2=\bigl(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\bigr)\in\operatorname{Skew}_2(\mathbb R)\). Right-unit gives \((i\Omega_2)\odot[1]=i\Omega_2\). For any \(U=[u\;w]\in\mathbb R^{n\times 2}\) and \(v\in\mathbb R^{k\times 1}\), note \(\Gamma_U(\Omega_2)=uw^T-wu^T\). Naturality gives
   \[
   \bigl(i(uw^T-wu^T)\bigr)\odot(vv^T) = (U\otimes v)(i\Omega_2)(U\otimes v)^T = i(uw^T-wu^T)\otimes(vv^T).
   \]
   Since elementary bivectors \(uw^T-wu^T\) span \(\operatorname{Skew}_n(\mathbb R)\), bilinearity forces \((iJ)\odot S = i(J\otimes S)\), and symmetrically \(R\odot(iK)=i(R\otimes K)\).

3. *Skew–skew sector:* By the same bivector spanning property, \((iJ)\odot(iK)\) for all \(n,k\) is uniquely determined via \(\Gamma_U\otimes\Gamma_V\) (\(U\in\mathbb R^{n\times 2}\), \(V\in\mathbb R^{k\times 2}\)) by the single \(4\times 4\) Hermitian matrix
   \[
   X_0 := (i\Omega_2)\odot(i\Omega_2)\in\operatorname{Herm}_4(\mathbb C).
   \]
   Every \(A\in\mathbb R^{2\times 2}\) obeys \(A\Omega_2 A^T = (\det A)\,\Omega_2\). Naturality and real bilinearity therefore require
   \[
   (A\otimes B)X_0(A\otimes B)^T = (\det A)(\det B)\,X_0 \qquad\text{for all }A,B\in\mathbb R^{2\times 2}.
   \tag{2}
   \]
   Choose diagonal \(A=\operatorname{diag}(\lambda,1)\), \(B=\operatorname{diag}(\mu,1)\). On the product basis \((00,01,10,11)\), \((A\otimes B)X_0(A\otimes B)^T\) multiplies entry \((p,q)\) by \(w_pw_q\) where \(w=(\lambda\mu,\lambda,\mu,1)\), while the right-hand side of (2) multiplies every entry by \(\lambda\mu\). Matching polynomials in \((\lambda,\mu)\) forces \((X_0)_{p,q}=0\) except on \(\{(00,11),(11,00),(01,10),(10,01)\}\). Next apply the unimodular shear \(A=\bigl(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\bigr)\), \(B=I_2\) (\(\det A=\det B=1\)): entry \((00,01)\) of \((A\otimes I_2)X_0(A^T\otimes I_2)=X_0\) reads \((X_0)_{00,11}+(X_0)_{10,01}=0\), so \((X_0)_{10,01}=-(X_0)_{00,11}\), and Hermiticity gives \((X_0)_{01,10}=-(X_0)_{11,00}\). Finally, applying simultaneous swap \(A=B=\bigl(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\bigr)\) (\((\det A)(\det B)=(-1)(-1)=+1\)) exchanges \(00\leftrightarrow 11\), forcing \((X_0)_{00,11}=(X_0)_{11,00}=\overline{(X_0)_{00,11}}\). Thus \((X_0)_{00,11}=\alpha\in\mathbb R\) is real, and \(X_0=\alpha(\Omega_2\otimes\Omega_2)\). Transporting by \(U\otimes V\) yields \((iJ)\odot(iK)=\alpha(J\otimes K)\), proving (1).

4. *Converse and algebraic properties:* Direct expansion for \(F=T+iL\) gives both \((D\odot_\alpha E)\odot_\alpha F\) and \(D\odot_\alpha(E\odot_\alpha F)\) equal to
   \[
   R\otimes S\otimes T + \alpha(J\otimes K\otimes T + J\otimes S\otimes L + R\otimes K\otimes L)
   + i\bigl(J\otimes S\otimes T + R\otimes K\otimes T + R\otimes S\otimes L + \alpha\,J\otimes K\otimes L\bigr),
   \]
   reflecting the commutative associative real algebra \(\mathbb R[\tau]/(\tau^2-\alpha)\) (\(\alpha=-1\): complex numbers \(\mathbb C\); \(\alpha=0\): dual numbers, recovering [RI-22](../../coordination/QR_COMPOSITION_INDEPENDENCE_PLAN.md); \(\alpha=+1\): split-complex numbers). Whole-carrier contraction of the second factor gives \(M(E)D\), and contraction of the first gives \(M(D)E\); these are \(D\) and \(E\), respectively, when both factors are normalized. These mass-scaled identities hold because \(\mathbf 1^T K\mathbf 1=0\) kills \(\alpha(J\otimes K)\) as well as \(i(R\otimes K)\); rectangular scalar independence holds because \(\chi_A^T J\chi_A=\chi_C^T K\chi_C=0\). ∎

### 2.2 Weak-positivity interval and selection of \(\alpha=-1\) by silent-control interchange

Before invoking silent controls, determine which \(\alpha\in\mathbb R\) preserve weak Boolean positivity on individually PSD quantum kernels:

**Lemma 1B (Exact PSD weak-positivity interval).** *Every composite \(D\odot_\alpha E\) of individually PSD Hermitian matrices \(D,E\succeq 0\) has nonnegative Boolean event weights \(\mu_{D\odot_\alpha E}(E_{\mathrm{joint}})\ge 0\) if and only if \(-1\le\alpha\le 1\). Within this interval, \(Q\odot_\alpha Q\succeq 0\) for the normalized rank-one PSD projector \(Q=\frac12\bigl(\begin{smallmatrix}1&i\\-i&1\end{smallmatrix}\bigr)\) holds if and only if \(\alpha=-1\).*

**Proof.** Since \(\overline E=S-iK\) is PSD whenever \(E\succeq 0\), both \(D\otimes E\succeq 0\) and \(D\otimes\overline E\succeq 0\) have PSD real parts \(R\otimes S-J\otimes K\) and \(R\otimes S+J\otimes K\). For \(\alpha\in[-1,1]\),
\[
\operatorname{Re}(D\odot_\alpha E)
= \frac{1-\alpha}2\operatorname{Re}(D\otimes E) + \frac{1+\alpha}2\operatorname{Re}(D\otimes\overline E)\succeq 0,
\tag{3}
\]
so \(\chi^T\operatorname{Re}(D\odot_\alpha E)\chi\ge 0\) for every real vector \(\chi\), including all Boolean indicators. Conversely, on \(Q=\frac12 I_2+\frac i2\Omega_2\) (\(M(Q)=1\), \(Q\succeq 0\)), the events \(E_{\mathrm{eq}}=\{(0,0),(1,1)\}\) and \(E_{\mathrm{diff}}=\{(0,1),(1,0)\}\) satisfy
\[
\mu_{Q\odot_\alpha Q}(E_{\mathrm{eq}})=\frac{1+\alpha}2,\qquad
\mu_{Q\odot_\alpha Q}(E_{\mathrm{diff}})=\frac{1-\alpha}2,
\]
which go negative for \(\alpha<-1\) and \(\alpha>1\), respectively. Direct multiplication shows that \(Q\odot_\alpha Q\) has orthogonal eigenvectors \((1,-i,-i,-1)^T\), \((1,i,i,-1)^T\), \((1,0,0,1)^T\), \((0,1,-1,0)^T\) with eigenvalues
\[
\operatorname{spec}(Q\odot_\alpha Q)
=\left\{\frac{3-\alpha}4,\;-\frac{1+\alpha}4,\;\frac{1+\alpha}4,\;\frac{1+\alpha}4\right\},
\]
forcing \(-\frac{1+\alpha}4\ge 0\) and \(\frac{1+\alpha}4\ge 0\), hence \(\alpha=-1\) if PSD is required. ∎

Notice that requiring \(Q\odot_\alpha Q\succeq 0\) outright would assume composite strong positivity. Instead, use the silent residual operations of [`RECORD_PROCESS_CONTRACT.md`](../../track_b/RECORD_PROCESS_CONTRACT.md) on the four-label two-cell carrier \(\Omega_4=\{0,1,2,3\}\), \(\mathcal P_4=\{A_0=\{0,1\},A_1=\{2,3\}\}\), with the mass- and recordability-preserving lifted generators of [RI-08b](../t8-q-control-selected-qubit-2026-09-13/CONTROL_SELECTED_QUBIT.md):
\[
W_U=\operatorname{diag}(U,ZUZ),\quad S_U(D)=W_U D W_U^\dagger,\quad
H=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad
P=\operatorname{diag}(1,i),\quad Z=\operatorname{diag}(1,-1).
\tag{4}
\]
Begin from the **classical diagonal** balanced preparation \(D_{+Z}=\operatorname{diag}(1/2,0,1/2,0)\) (\(M(D_{+Z})=1\), zero off-diagonal entries). One silent \(S_H\) step produces the **purely real** state
\[
D_{+X}=S_H(D_{+Z})=\frac14\begin{pmatrix}
1&1&0&0\\1&1&0&0\\0&0&1&-1\\0&0&-1&1
\end{pmatrix},\qquad
D_{+Y}=S_P(D_{+X})=\frac14\begin{pmatrix}
1&-i&0&0\\i&1&0&0\\0&0&1&i\\0&0&-i&1
\end{pmatrix},
\tag{5}
\]
with cell weights \((1,0)\) for \(D_{+X}\), \((1/2,1/2)\) for \(D_{+Y}\), and \((0,1)\) for \(D_{-X}=S_P(D_{+Y})=S_P^2(D_{+X})\).

In the growth theorem package ([`THEOREM_PACKAGE.md` §1](../../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model)), incomparable births satisfy the diamond law \(q(C,S)q(C+S,T)=q(C,T)q(C+T,S)\). Its silent-activity counterpart for independent systems is **bifunctorial interchange**: applying independent local silent controls before or after independent composition yields the same composite state,
\[
(W_1\otimes W_2)(D\odot_\alpha E)(W_1\otimes W_2)^\dagger
= (W_1 D W_1^\dagger)\odot_\alpha(W_2 E W_2^\dagger).
\tag{6}
\]

**Theorem 1C (Selection of \(D\otimes E\) from silent-control interchange or local product-cell positivity).** *Within the classified family \(\odot_\alpha\) (\(\alpha\in\mathbb R\)):*
1. *Evaluating (6) on the purely real state pair \((D_{+X},D_{+X})\) with \(W_1=W_2=W_P\) uniquely forces \(\alpha=-1\), i.e., \(D\odot_\alpha E = D\otimes E\).*
2. *Even without imposing (6) directly on raw off-diagonal entries, applying the local product silent control \(S_P\otimes S_P\) to \(D_{+Y}\odot_\alpha D_{+Y}\) leaves \(\mathcal P_4\times\mathcal P_4\) exactly decoherent with total mass \(1\) and product-cell weights*
   \[
   \bigl(q_{00}(\alpha),\,q_{01}(\alpha),\,q_{10}(\alpha),\,q_{11}(\alpha)\bigr)
   =\left(-\frac{1+\alpha}4,\;\frac{1+\alpha}4,\;\frac{1+\alpha}4,\;\frac{3-\alpha}4\right).
   \tag{7}
   \]
   *Requiring either agreement with the single-system marginal \((0,1)^{\otimes 2}=(0,0,0,1)\) or mere nonnegativity \(q_{ab}(\alpha)\ge 0\) uniquely forces \(\alpha=-1\). In particular, RI-22's \(\star\)-product (\(\alpha=0\)) produces the negative product-cell weight \(q_{00}(0)=-1/4\).*
3. **Deletion countermodel (necessity of phase-bearing silent control):** *If \(S_P\) is omitted while retaining the entire silent control group \(\langle S_H,S_Z\rangle\) (16 signed orthogonal matrices, 8 distinct congruence actions \(S_U\)) and all real incidence maps, then (6) holds identically for every \(\alpha\in\mathbb R\), leaving the entire non-tensor interval \(\alpha\in[-1,1]\) unexcluded on all PSD inputs.*

**Proof.** Because \(D_{+X}\) is purely real (\(J_{+X}=0\)), \(D_{+X}\odot_\alpha D_{+X}=D_{+X}\otimes D_{+X}\) is independent of \(\alpha\). Entry \(((0,0),(1,1))\) of \((W_P\otimes W_P)(D_{+X}\otimes D_{+X})(W_P\otimes W_P)^\dagger\) equals \(\frac1{16}\overline{i^2}=-\frac1{16}\). By contrast, \(D_{+Y}=R_{+Y}+iJ_{+Y}\) has diagonal \(R_{+Y}=\frac14 I_4\) and \((J_{+Y})_{0,1}=-\frac14\), so entry \(((0,0),(1,1))\) of \(D_{+Y}\odot_\alpha D_{+Y}\) comes solely from \(\alpha(J_{+Y}\otimes J_{+Y})_{(0,0),(1,1)}=\frac\alpha{16}\). Equating the two gives \(\alpha=-1\).

For (7), let \(e_0=(1,1,0,0)^T\), \(e_1=(0,0,1,1)^T\), \(u_0=W_P^\dagger e_0=(1,-i,0,0)^T\), and \(u_1=W_P^\dagger e_1=(0,0,1,-i)^T\) (since \(W_P=\operatorname{diag}(1,i,1,i)\)). Direct contraction on \(D_{+Y}\) gives \(u_0^\dagger R_{+Y}u_0=u_1^\dagger R_{+Y}u_1=\frac12\), \(u_0^\dagger(iJ_{+Y})u_0=-\frac12\) (\(u_0^\dagger J_{+Y}u_0=\frac i2\)), and \(u_1^\dagger(iJ_{+Y})u_1=+\frac12\) (\(u_1^\dagger J_{+Y}u_1=-\frac i2\)). Expanding \((u_a\otimes u_b)^\dagger(D_{+Y}\odot_\alpha D_{+Y})(u_a\otimes u_b)\) yields (7), while cross-cell contractions vanish because \(u_0^\dagger R_{+Y}u_1=u_0^\dagger J_{+Y}u_1=0\). Nonnegativity of \(q_{00}(\alpha)=-\frac{1+\alpha}4\) and \(q_{01}(\alpha)=\frac{1+\alpha}4\) forces \(\alpha=-1\).

Finally, every generator \(W_H,W_Z\) is real (\(W^\dagger=W^T\)), so (6) reduces to Theorem 1A's real-incidence naturality \(\Gamma_{W_1\otimes W_2}(D\odot_\alpha E)=\Gamma_{W_1}(D)\odot_\alpha\Gamma_{W_2}(E)\), which holds for all \(\alpha\in\mathbb R\); Lemma 1B keeps all Boolean weights nonnegative on \(\alpha\in[-1,1]\). ∎

---

## 3. Composite Committed-Record Grouping Forces Exact Decoherence

Once records are committed (`commit_record`), passive projections and Boolean groupings of exclusive committed outcomes (`access_records`) must add as classical probabilities. On a single copy, additivity of \(\mathcal P=\{A_0,\dots,A_{k-1}\}\) across all outcome subsets \(S\subseteq\{0,\dots,k-1\}\) is equivalent to
\[
\mu_D(A_r\sqcup A_s)-\mu_D(A_r)-\mu_D(A_s)=2\operatorname{Re} D(A_r,A_s)=2R(A_r,A_s)=0\qquad(r\ne s),
\tag{8}
\]
which leaves \(D(A_r,A_s)=iJ(A_r,A_s)=it_{rs}\) (\(t_{rs}\in\mathbb R\)) unrestricted. Even strict positive definiteness \(D\succ 0\) does not remove \(it_{rs}\): on \(\Omega_2=\{0,1\}\) with \(A_0=\{0\}\), \(A_1=\{1\}\),
\[
D_{\mathrm{imag}}(t)=\begin{pmatrix}1/2&it\\-it&1/2\end{pmatrix},\qquad t=\frac14,
\tag{9}
\]
has \(M=1\), eigenvalues \(\frac34,\frac14>0\), and \(\mu(\{0\})+\mu(\{1\})=\frac12+\frac12=1=\mu(\{0,1\})\), yet \(D(\{0\},\{1\})=\frac i4\ne 0\), so \(|\{0\}\rangle\) and \(|\{1\}\rangle\) are non-orthogonal in \(\mathcal H_D\).

**Theorem 2 (Composite record-grouping criterion across \(\odot_\alpha\)).** *Let \(\mathcal P=\{A_0,\dots,A_{k-1}\}\) (\(k\ge 2\)) satisfy single-copy additivity (8) on \(D=R+iJ\in\operatorname{Herm}_n(\mathbb C)\), with \(p_r=\mu_D(A_r)\) and \(t_{rs}=J(A_r,A_s)\in\mathbb R\). For each pair \(r\ne s\), define the two-copy committed-outcome coincidence and anti-coincidence groupings*
\[
C_{rs}^{\mathrm{same}}=(A_r\times A_r)\sqcup(A_s\times A_s),\qquad
C_{rs}^{\mathrm{diff}}=(A_r\times A_s)\sqcup(A_s\times A_r).
\]
*Then under \(D\odot_\alpha D\):*
\[
\mu_{D\odot_\alpha D}(C_{rs}^{\mathrm{same}})-\bigl(\mu_{D\odot_\alpha D}(A_r\times A_r)+\mu_{D\odot_\alpha D}(A_s\times A_s)\bigr)=2\alpha\,t_{rs}^2,
\tag{10}
\]
\[
\mu_{D\odot_\alpha D}(C_{rs}^{\mathrm{diff}})-\bigl(\mu_{D\odot_\alpha D}(A_r\times A_s)+\mu_{D\odot_\alpha D}(A_s\times A_r)\bigr)=-2\alpha\,t_{rs}^2.
\tag{11}
\]
*Consequently:*
1. **Nonzero \(\alpha\) (in particular \(\alpha=-1\), \(D\otimes D\), selected by Theorem 1):** *Two-copy committed product outcomes satisfy Boolean grouping additivity if and only if \(t_{rs}=0\) for all \(r\ne s\), i.e.,*
   \[
   \boxed{D(A_r,A_s)=0\quad\text{for all }r\ne s\qquad(\text{exact decoherence}).}
   \]
   *When \(D\succeq 0\), this is exact orthogonality \(\langle A_r|A_s\rangle_D=0\) in \(\mathcal H_D\), and \(\mathcal P^{\times m}\) is then decoherent on \(D^{\otimes m}\) for every \(m\ge 1\).*
2. **Zero \(\alpha\) (RI-22's \(\star\)-product):** *The discrepancy \(2\alpha\,t_{rs}^2\) vanishes identically; \(D_{\mathrm{imag}}(1/4)^{\star m}\) satisfies all \(2^{k^m}\) Boolean product-record groupings for every \(m\ge 1\) despite \(D(\{0\},\{1\})=i/4\ne 0\). Thus Theorem 1 is strictly load-bearing for deriving record orthogonality from composite record stability.*
3. **Boundary with [RI-08d](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md):** *Equation (10) constrains only cell-summed cross-relations \(D(A_r,A_s)=\chi_{A_r}^\dagger D\chi_{A_s}\). An internal zero-sum cross-cell block such as \(D(I_2/4,c)\) with off-diagonal block \(cZ\) (\(c\ne 0\)) already satisfies \(\chi_{A_0}^\dagger D\chi_{A_1}=0\) and therefore passes all uncoupled multi-copy record groupings on \(D^{\otimes m}\); excluding \(c\ne 0\) still requires a shared coupler as in RI-08d.*

**Proof.** Because \(R(A_r,A_s)=0\) for \(r\ne s\), expanding (1) on \((A_r\times A_r,\,A_s\times A_s)\) kills \(R\otimes R\), \(J\otimes R\), and \(R\otimes J\), leaving \((D\odot_\alpha D)(A_r\times A_r,A_s\times A_s)=\alpha J(A_r,A_s)^2=\alpha t_{rs}^2\). Biadditivity gives \(\mu(C_{rs}^{\mathrm{same}})=p_r^2+p_s^2+2\alpha t_{rs}^2\), proving (10); \(J(A_s,A_r)=-t_{rs}\) gives \((D\odot_\alpha D)(A_r\times A_s,A_s\times A_r)=-\alpha t_{rs}^2\), proving (11). For \(\alpha\ne 0\), (10) vanishes for all \(r\ne s\) iff every real \(t_{rs}=0\), which together with \(R(A_r,A_s)=0\) means \(D(A_r,A_s)=0\); conversely \(D(A_r,A_s)=0\) implies \((D^{\otimes m})(A_{r_1}\times\cdots\times A_{r_m},A_{s_1}\times\cdots\times A_{s_m})=\prod_\ell D(A_{r_\ell},A_{s_\ell})=0\) whenever the tuples differ. For \(\alpha=0\), [RI-22 eq. (12)](../../coordination/QR_COMPOSITION_INDEPENDENCE_PLAN.md#5-ri-21-under-the-changed-product-law) gives \(\operatorname{Re}(D^{\star m})=R^{\otimes m}\), whose cross-entries vanish whenever \(R(A_r,A_s)=0\). The \(cZ\) remark follows because \((1,1)Z(1,1)^T=0\). ∎

---

## 4. Classical-to-Seed Lift and Operational Separation from Classical Active Residuals

### 4.1 Generating a recordable principal-minor seed from a classical diagonal state

In [RI-21](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md), strong positivity \(D\succeq 0\) is characterized via \(D^{\otimes n}\otimes B\) using the supplied three-label rank-one matrix \(B=bb^\dagger\), \(b=(1,-1,1)^T\), which has \(\operatorname{Tr} B=3\) and no nontrivial two-cell decoherent partition. Using Theorem 1 (\(\odot=\otimes\)), the state \(D_{+X}=S_H(D_{+Z})\) already constructed in (5) from the classical diagonal state \(D_{+Z}=\operatorname{diag}(1/2,0,1/2,0)\) supplies the exact principal-minor signs inside a trace-one, two-cell recordable kernel:

**Theorem 3A (Classical-diagonal-plus-\(S_H\) principal-minor witness).** *Let \(D\in\operatorname{Herm}_n(\mathbb C)\) satisfy \(M(D)=1\) and weak Boolean positivity \(\mu_D(A)\ge 0\) (\(A\subseteq\Omega_n\)). Let \(D_{+X}=S_H(D_{+Z})\) on \(\Omega_4=\{0,1,2,3\}\), so \(M(D_{+X})=\operatorname{Tr}(D_{+X})=1\) and \(D_{+X}(A_0,A_1)=0\). For each nonempty \(I=\{i_1<\dots<i_m\}\subseteq\Omega_n\), define the ordinary Boolean events*
\[
E_I^{\mathrm{nat}}=\bigl\{(h_\sigma,a_\sigma^{\mathrm{nat}}):\sigma\in S_m\bigr\}\subseteq\Omega_n^m\times\Omega_4,\qquad
\widetilde E_I^{\mathrm{nat}}=\bigl\{(h_\sigma,z,a_\sigma^{\mathrm{nat}}):\sigma\in S_m,\ z\in\Omega_n^{n-m}\bigr\}\subseteq\Omega_n^n\times\Omega_4,
\]
*where \(h_\sigma=(i_{\sigma(1)},\dots,i_{\sigma(m)})\) and \(a_\sigma^{\mathrm{nat}}=2\) for \(\sigma\) even, \(3\) for \(\sigma\) odd. Then*
\[
\mu_{D^{\otimes m}\otimes D_{+X}}(E_I^{\mathrm{nat}})
=\mu_{D^{\otimes n}\otimes D_{+X}}(\widetilde E_I^{\mathrm{nat}})
=\frac{m!}4\,\det(D_I),
\tag{12}
\]
*and therefore*
\[
\boxed{D\succeq 0\ \Longleftrightarrow\ \mu_{D^{\otimes n}\otimes S_H(D_{+Z})}(\widetilde E_I^{\mathrm{nat}})\ge 0\quad\text{for all nonempty }I\subseteq\Omega_n.}
\tag{13}
\]

**Proof.** On cell \(A_1=\{2,3\}\), (5) has submatrix \(\frac14\bigl(\begin{smallmatrix}1&-1\\-1&1\end{smallmatrix}\bigr)\), so \((D_{+X})_{a_\sigma^{\mathrm{nat}},a_\tau^{\mathrm{nat}}}=\frac14\operatorname{sgn}(\sigma)\operatorname{sgn}(\tau)\). Expanding the quadratic form and substituting \(\pi=\tau\circ\sigma^{-1}\) as in [RI-21 §3](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md#3-explicit-boolean-event-and-determinant-identity) sums \(m!\) copies of \(\frac14\det(D_I)\), while the unused \(n-m\) factors contribute \(M(D)^{n-m}=1\), giving (12). Equivalence (13) then follows from Sylvester/principal-minor characterization of Hermitian PSD matrices ([RI-21 §4](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md#4-complete-principal-minor-criterion-and-finite-catalogue-equivalence)) and PSD closure under Kronecker products. ∎

Note the exact scope of (13): \(D_{+Z}\) is diagonal nonnegative and \(S_H\) is one reversible silent control, removing RI-21's ad-hoc trace-three seed. However, \(E_I^{\mathrm{nat}}\) selects individual atoms \(\{2,3\}\) inside \(A_1\) paired with permutation histories, so \(\mu(\widetilde E_I^{\mathrm{nat}})\ge 0\) remains a **composite weak-positivity requirement on the Boolean event algebra**, not a single sharp post-commitment readout.

### 4.2 Single-system classical cones: extreme-state obstruction vs mixed-state counterexample

Recent Track B models show that classical active residuals on \(\Delta_2\subset\mathbb R_+^2\) can alter subsequent growth probabilities ([`native_active_residual_v1.md`](../../track_b/native_active_residual_v1.md)) and that classical counters reproduce the prepared pair-incidence joint law ([`finite_pair_incidence_register.md`](../../observables/finite_pair_incidence_register.md)). To identify precisely where quantum residual geometry becomes necessary, consider any finite-dimensional classical simplex \(\Delta_d=\{\rho\in\mathbb R_+^d:\mathbf 1_d^T\rho=1\}\) (\(d\ge 1\)).

**Theorem 3B (Reversible automorphisms of \(\Delta_d\) and purity sensitivity).**
1. *Every silent residual map \(S\in\mathrm{Stoch}_d\) (`evolve_residual`) possessing an admissible silent inverse \(S^{-1}\in\mathrm{Stoch}_d\) is a permutation matrix \(P_\pi\) (\(\pi\in S_d\)). Consequently, on any extreme (pure) preparation \(e_j\in\Delta_d\) and any sharp binary partition \(A_0\sqcup A_1=\{0,\dots,d-1\}\), every finite word \(W\) of reversible silent operations yields deterministic readout weights \(q_0(We_j)\in\{0,1\}\)—unlike \(D_{+X},D_{+Y}\in\mathcal C_0\), which are extreme rays of \(\mathcal C_0\cong\mathrm{PSD}_2\) mapped reversibly by \(S_H,S_P\) through cell weights \((1,1/2,1)\) and \((1,1/2,0)\).*
2. **Mixed-state classical counterexample (\(d=6\)):** *If the extreme-state requirement is dropped and hidden classical dimension is allowed, the mixed preparation \(\rho=\frac12(e_0+e_1)\in\Delta_6\), sharp cell \(A_0=\{0,1,2\}\), and reversible permutation \(\pi=(0\mapsto 2\mapsto 3\mapsto 1\mapsto 4\mapsto 5\mapsto 0)\in S_6\) satisfy*
   \[
   \bigl(q_0(\rho),\,q_0(P_\pi\rho),\,q_0(P_\pi^2\rho)\bigr)=\left(1,\,\frac12,\,0\right).
   \]
   *Thus single-system sequential transition probabilities without an extreme-state or carrier-dimension premise do not suffice to exclude enlarged classical residual cones.*

**Proof.** Let \(S\ge 0\), \(S^{-1}\ge 0\) satisfy \(S^{-1}S=I_d\) and \(\mathbf 1_d^T S=\mathbf 1_d^T\). Each column \(j\) of \(S\) is nonzero. If column \(j\) had two positive entries \(S_{a,j}>0\) and \(S_{b,j}>0\) (\(a\ne b\)), then for every \(m\ne j\), \(0=(S^{-1}S)_{m,j}\ge (S^{-1})_{m,a}S_{a,j}+(S^{-1})_{m,b}S_{b,j}\ge 0\) would force \((S^{-1})_{m,a}=(S^{-1})_{m,b}=0\), confining both columns \(a\) and \(b\) of \(S^{-1}\) to row \(j\) and contradicting \(\operatorname{rank}(S^{-1})=d\). Hence each column of \(S\) has one positive entry, equal to \(1\) by column-sum normalization, so \(S=P_\pi\). On \(e_j\), \(P_\pi e_j=e_{\pi(j)}\) has indicator weight \(\mathbf 1_{\pi(j)\in A_0}\in\{0,1\}\). In the \(d=6\) witness, \(\operatorname{supp}(\rho)=\{0,1\}\subseteq A_0\) (\(q_0=1\)), \(\pi(\{0,1\})=\{2,4\}\) has \(2\in A_0,4\notin A_0\) (\(q_0=1/2\)), and \(\pi^2(\{0,1\})=\{3,5\}\subseteq A_0^c\) (\(q_0=0\)). ∎

### 4.3 Dimension-free bipartite separation via exact rational silent controls

To eliminate the mixed-state loophole of Theorem 3B(2) across **all** finite classical dimensions \(d_A,d_B\ge 1\), **all** shared classical mixtures, **all** (even irreversible) column-stochastic local silent maps, and **all** noisy local effects, use the 16-label composite interface of [RI-08d](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md):

**Theorem 3C (Exact-rational 16-label CHSH separation against all classical residual cones).**
1. *For any finite dimensions \(d_A,d_B\ge 1\), any shared classical active-residual state \(\rho_{AB}=\sum_\lambda p_\lambda\,\rho_A^{(\lambda)}\otimes\rho_B^{(\lambda)}\) (\(p_\lambda\ge 0\), \(\sum_\lambda p_\lambda=1\), \(\rho_A^{(\lambda)}\in\Delta_{d_A}\), \(\rho_B^{(\lambda)}\in\Delta_{d_B}\)), any local column-stochastic silent evolutions \(\mathcal E_{A,x}\in\mathrm{Stoch}_{d_A}\), \(\mathcal E_{B,y}\in\mathrm{Stoch}_{d_B}\) (\(x,y\in\{0,1\}\)), and any bounded local binary readout effects \(e_{A,0}\in[0,1]^{d_A}\), \(e_{B,0}\in[0,1]^{d_B}\) (\(e_{\bullet,1}=\mathbf 1-e_{\bullet,0}\)), the correlators \(E(x,y)=p_{00}(x,y)+p_{11}(x,y)-p_{01}(x,y)-p_{10}(x,y)\) satisfy*
   \[
   \bigl|E(0,0)+E(0,1)+E(1,0)-E(1,1)\bigr|\le 2.
   \tag{14}
   \]
   *This bound covers [`native_active_residual_v1.md`](../../track_b/native_active_residual_v1.md), [`finite_homogeneous_compensation.md`](../../track_b/finite_homogeneous_compensation.md), and [`finite_pair_incidence_register.md`](../../observables/finite_pair_incidence_register.md) at any finite register size.*
2. *On \(\Omega_4\times\Omega_4\), prepare \(D_{+X}=S_H(D_{+Z})\) and the polarized reference \(R_{t=1}=D_{+Z}\), and apply RI-08d's single shared coupler \(\mathcal U=T^\dagger(I_{\mathrm{cells}}\otimes U)T\) (\(U=\frac1{\sqrt2}(I_2\otimes H_0)\mathrm{CNOT}\)) to obtain \(N'=\mathcal U(D_{+X}\otimes R_{t=1})\mathcal U^\dagger\). Define the four **exact rational** local silent controls \(S_{A,x}\otimes S_{B,y}\) via \(W_{A_x}\otimes W_{B_y}\) with integer generators and rational congruence divisors:*
   \[
   A_0=I_2\ (\div 1),\quad
   A_1=\begin{pmatrix}1&1\\1&-1\end{pmatrix}\ (\div 2),\qquad
   B_0=\begin{pmatrix}2&-1\\1&2\end{pmatrix}\ (\div 5),\quad
   B_1=\begin{pmatrix}1&-2\\2&1\end{pmatrix}\ (\div 5).
   \tag{15}
   \]
   *For every \((x,y)\in\{0,1\}^2\), the evolved 16-label kernel \(N'_{xy}\) is Hermitian, PSD, total-entry normalized (\(M_{16}(N'_{xy})=1\)), and **exactly four-cell decoherent** on RI-08d's unchanged partition \(\{C_{00},C_{01},C_{10},C_{11}\}\), with exact rational correlators*
   \[
   E(0,0)=\frac45,\quad E(0,1)=\frac45,\quad E(1,0)=\frac35,\quad E(1,1)=-\frac35,\qquad
   \boxed{S_{\mathrm{CHSH}}=\frac{14}5>2.}
   \tag{16}
   \]

**Proof.** In (1), \(E(x,y)=\sum_\lambda p_\lambda\,a_x^{(\lambda)}b_y^{(\lambda)}\) where \(a_x^{(\lambda)}=(2e_{A,0}-\mathbf 1_{d_A})^T\mathcal E_{A,x}\rho_A^{(\lambda)}\in[-1,1]\) and \(b_y^{(\lambda)}\in[-1,1]\). For reals in \([-1,1]\), \(a_0(b_0+b_1)+a_1(b_0-b_1)\le |b_0+b_1|+|b_0-b_1|=2\max(|b_0|,|b_1|)\le 2\), and convex averaging preserves (14).

In (2), \(A_x A_x^T = d_{A,x} I_2\) (\(d_{A,0}=1,d_{A,1}=2\)) and \(B_y B_y^T = 5 I_2\), so each \(\widetilde A_x=A_x/\sqrt{d_{A,x}}\) and \(\widetilde B_y=B_y/\sqrt5\) is orthogonal, while congruence \((W_{A_x}\otimes W_{B_y})N'(W_{A_x}\otimes W_{B_y})^\dagger/(d_{A,x}\cdot 5)\) uses only rational arithmetic without square roots. Because \(D_{+X}\) has \(c=0\), [RI-08d §6](../t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md#6-countercontrols-and-the-limited-larger-closure) proves that \(N'\) and all its shared/product unitary images remain PSD, normalized (\(M_{16}=1\)), and exactly four-cell decoherent, with quotient state \(\rho_{\mathrm{joint}}=(I_2\otimes H)|\Phi^+\rangle\langle\Phi^+|(I_2\otimes H)\) satisfying \(\langle Z\otimes X\rangle=\langle X\otimes Z\rangle=1\) and \(\langle X\otimes X\rangle=\langle Z\otimes Z\rangle=0\). Conjugating the native \(X\)-readout by \(\widetilde A_x\) yields \(X\) (\(x=0\)) and \(Z\) (\(x=1\)); conjugating \(X\) by \(\widetilde B_0,\widetilde B_1\) yields \(\frac45 Z+\frac35 X\) and \(\frac45 Z-\frac35 X\) (the \((3,4,5)\) Pythagorean rotations). Evaluating on \(\rho_{\mathrm{joint}}\) gives \((\frac45,\frac45,\frac35,-\frac35)\) and sum \(\frac{14}5\). ∎

---

## 5. Connected Upstream-to-Born Chain and Remaining Unproved DET Premises

Combining Theorems 1, 2, and 3A with [`DERIVATION.md` §2](../t8-q-strict-derivation-2026-09-12/DERIVATION.md#2-canonical-finite-representation--an-actual-derivation) reduces four previously separate assumptions—ordinary tensor composition, record orthogonality, RI-21's trace-three seed, and Hilbert/Born representation—to one connected conditional sequence:

\[
\begin{aligned}
&\text{Pre-PSD Hermitian biadditive } D + \text{Unit} + \text{Real-incidence naturality} + \text{Silent } S_P \text{ interchange} \\
&\quad\Longrightarrow\quad D\odot E = D\otimes E \quad\text{(Theorem 1)} \\
&\quad\Longrightarrow\quad
\begin{cases}
\text{Composite record coincidence grouping} \implies D(A_r,A_s)=0 & \text{(Theorem 2)} \\
\text{Classical diagonal } D_{+Z} + \text{silent } S_H + \text{catalogue positivity} \implies D\succeq 0 & \text{(Theorem 3A)}
\end{cases} \\
&\quad\Longrightarrow\quad \mathcal H_D = F_\Omega/\ker D,\quad \langle A_r|A_s\rangle_D=0,\quad K(r)=\|P_r\psi\|_D^2 \quad\text{([DERIVATION.md §2](../t8-q-strict-derivation-2026-09-12/DERIVATION.md#2-canonical-finite-representation--an-actual-derivation))}.
\end{aligned}
\]

**What remains unproved from bare DET causal order and records \((V,\prec,r)\) alone:**
1. **Grade-two complex pair calculus:** Why uncommitted alternatives prior to record commitment are represented by a complex Hermitian biadditive functional \(D=R+iJ\) rather than a classical measure or higher-grade functional, and why nature selects \(\mathbb C\).
2. **Operational availability and composite event positivity:** Physical availability of the reversible silent controls \(S_H,S_P\), independent multi-copy preparation without a copy cutoff, and weak positivity on the nonrectangular permutation events \(\widetilde E_I^{\mathrm{nat}}\) (which select sub-cell atoms \(\{2,3\}\subset A_1\) rather than a single sharp coarse-grained partition).
3. **Coupling to native causal growth:** In [`THEOREM_PACKAGE.md`](../../track_b/native_theorem_package_v1/THEOREM_PACKAGE.md) the payload \(\mathfrak D\) is scalar-passive, while in [`native_active_residual_v1.md`](../../track_b/native_active_residual_v1.md) the active residual is classical \(\mathbb R_+^2\). Constructing an admitted causal-order birth law \(q(P,r,S;\mathfrak D)\) whose residual-to-growth feedback exhibits Theorem 3B/3C's nonclassical silent-control signatures remains an open Track B research problem.

Option B (gravity), Status M (open becoming), and all governance, calibration, custody, and execution gates ([`GOVERNANCE.md`](../../../GOVERNANCE.md)) remain unchanged.

---

## 6. Exact Verification Record

[`check.py`](check.py) is a self-contained Python standard-library test suite (`fractions.Fraction`, `itertools`, `unittest`, and an exact immutable Gaussian-rational class `G`) with zero floating-point operations or external imports. Its eight named tests verify:

1. Exact rational Gaussian elimination on the 256-dimensional space of real-bilinear maps \(\operatorname{Herm}_2(\mathbb C)\times\operatorname{Herm}_2(\mathbb C)\to\operatorname{Herm}_4(\mathbb C)\) (proving rank \(255\) and nullity \(1\) spanned by \(J\otimes K\)), plus \(8\times 8\) associativity, swap covariance, unit, and complex marginals across \(\alpha\);
2. Convex decomposition (3), Boolean weights, and the exact spectrum of \(Q\odot_\alpha Q\) across \(\alpha\);
3. Silent-control interchange on \(D_{+X}=S_H(D_{+Z})\) and local product-cell weights (7), including \(q_{00}(0)=-1/4\) for RI-22's \(\star\)-product;
4. Closure of the real silent-control group \(\langle S_H,S_Z\rangle\) (16 signed matrices, 8 distinct congruence actions \(S_U\)) and exact preservation of \(\odot_\alpha\) across all 64 action pairs when \(S_P\) is deleted;
5. Exact coincidence/anti-coincidence discrepancies (10)–(11) on \(D_{\mathrm{imag}}(1/4)\succ 0\), all \(2^4\) two-copy and \(2^8\) three-copy groupings under \(\alpha=0\), and the \(cZ\) boundary with RI-08d;
6. Direct and padded principal-minor identities (12) using \(D_{+X}=S_H(D_{+Z})\) across all seven benchmark candidates from [RI-21 §5](../../coordination/QR_FINITE_COPY_WITNESS_PLAN.md#5-exact-examples-and-supplementary-arithmetic), checked against independent Gaussian-elimination determinants;
7. Permutation-automorphism determinism on \(\Delta_d\) (\(d=2,3,4\)), the explicit \(d=6\) mixed-state permutation countermodel achieving \((1,1/2,0)\), and exact rational confirmation of [`native_active_residual_v1.md`](../../track_b/native_active_residual_v1.md)'s stochastic matrices and \(\Delta_{\mathrm{update}}=1/25344\);
8. Exhaustive classical extreme-strategy bound \(|S_{\mathrm{CHSH}}|\le 2\) and exact rational 16-label pair-kernel evaluation on \(N'\) giving \(E=(4/5,4/5,3/5,-3/5)\) and \(S_{\mathrm{CHSH}}=14/5\).

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/validation/t8-q-pair-kernel-bridge-2026-10-31/check.py -v
PYTHONDONTWRITEBYTECODE=1 python3 -B -O docs/validation/t8-q-pair-kernel-bridge-2026-10-31/check.py -v
```

Checked source SHA-256 (`check.py`):
`7cce895f6ff26d52dcf0d069f4b6b5e020f1485d2fa04c4d198555fcf32e0f4a`.
