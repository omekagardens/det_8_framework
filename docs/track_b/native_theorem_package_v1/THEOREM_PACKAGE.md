# A conditional theorem package for record-marked order growth

18 October 2026. Editorial public edition of a conditional mathematical consolidation.

## Abstract

A strictly positive, record-local, scalar-passive growth model admits an explicit record-blind harmonic extension through one additional birth layer at sufficiently small amplitude. For the fixed admitted law, a specified amplitude of \(1/4\) fails on three precisely defined supports of 30, 33 and 38 child classes. The complete signed kernel on those supports survives: it has one dimension, or two if a particular pair of canonical coefficients agrees. That actual equality remains unresolved.

These statements concern a conditional mathematical model, not a derivation of quantum dynamics or spacetime from DET. The arbitrary complex positive-semidefinite payload is retained, but growth probabilities do not depend on it. The distinction between a positive small-amplitude extension, a signed solution, and a rejected fixed-amplitude endpoint is essential.

This document provides the definitions, complete reduced systems, recovery formulas, assumptions and proof arguments in one place. Finite coefficient lemmas inherited from the admitted instance are stated explicitly. Their admission is not replaced by a new calculation or a new axiom of DET. The original numerical certificate is not reconstructed here. Compact provenance identifiers appear in §12; no chronological reading of the archive is required to understand the statements or their dependencies.

The [20 October law-family supplement](LAW_FAMILY_SUPPLEMENT.md) proves a fixed-seed obstruction and an explicit moving-seed classification for a declared parent-five family. Its [singular-law kernel and width theorem](SINGULAR_LAW_WIDTH.md) proves rank ten and kernel dimension one throughout that eleven-column family. At any \(\chi=0\) law all harmonic directions are target-width-blind; the admitted \(\theta\) bound excludes the formal compatible alternative. Whether such a law occurs remains conditional on \(\Xi=\theta+360\mu_1-359\mu_0>1\); \(\Xi=1\) is excluded. This separate eleven-column result does not select the later canonical-coefficient branch or transfer the fixed-law 30/33/38 conclusions. See the [publication note](PUBLICATION_NOTE.md) for review and evidence boundaries.

Conditional on \(\Xi>1\), the [positive-contrast limit theorem](POSITIVE_CONTRAST_LIMIT.md) proves a local uniform quadratic upper bound on the absolute target-width contrast of all strictly positive harmonic perturbations in that eleven-class family, with arbitrary normalization and amplitude. The comparison is to the baseline at the same parameter; no continuity or uniform positive lower bound of \(\rho_\lambda\) is required. The bound does not select occurrence, prove sharpness or imply convergence of raw widths or entire laws.

The [exceptional-law width witness](SINGULAR_OBSERVABLE_WITNESS.md) distinguishes the already admitted parent \(P_4=C_4\oplus A_2\) from that \(P_1\) target. Conditional on \(\Xi>1\), the surviving kernel has exact positive interval \(-\lambda_*\theta/(2\kappa^2)<\eta<1/\kappa\); complete-row width at \(P_4\) detects it iff \(\eta\ne0\). The proof retains all eight ideals and sixteen marked outcomes. It assumes complete child-order access and the known parent embedding, supplies no physical detector or sampling implementation, and leaves the actual occurrence comparison and later 30/33/38 questions unchanged.

The [regular observable family](REGULAR_OBSERVABLE_FAMILY.md) gives a kernel section with \(v_{11}=1\), no division by \(\chi\), and a fixed amplitude whose multipliers stay at least \(1/4\) on a neighborhood of the conditional exception. Its complete \(P_4\) contrast is positive in both root sectors and obeys \(\delta_{4,i}/\rho_\lambda>1/4\) there. This is a normalized lower bound; a uniform absolute effect would need a separately admitted positive lower bound on \(\rho_\lambda\). Actual occurrence, scale continuity, numerical neighborhood size and benchmark success are not supplied, and the \(P_1\) quadratic upper bound remains intact.

The [baseline-scale theorem](BASELINE_SCALE_THEOREM.md) separately fixes the full-layer half-scale continuation on the changed prefix. It proves continuity and a symbolic positive lower bound for \(\rho^H_\lambda\), upgrading the regular family's normalized \(P_4\) contrast to a uniform absolute lower bound on its neighborhood, conditional on \(\Xi>1\). The maximum covers every marked six-parent and every proper ideal; the scale rule is an optional law choice. An explicit positive compatible continuation shows why arbitrary scale choices need not share the bound. No numerical effect size, occurrence selection or physical detector is supplied.

The [complete-row observation comparison](P4_OBSERVATION_SUFFICIENCY.md), conditional on \(\Xi>1\), shows that \(P_4\) width attains the full row's total variation at the exception and to its left, but strictly loses it to the right on the admitted neighborhood. The normalized loss has a positive first-order right-hand term; the absolute loss has that order for the selected half-scale law. Width is nevertheless not a statistically sufficient summary anywhere in that neighborhood. Complete child-order access and the parent embedding remain assumed.

## 1. Mathematical object and admitted model

A state consists of a finite order \(P\), immutable binary marks \(r:P\to\{0,1\}\), and an arbitrary complex positive-semidefinite payload \(\mathfrak D\) on a fixed carrier. An ideal \(S\subseteq P\) is a downward-closed subset, including the empty and full ideals. A birth appends one maximal vertex with strict past exactly \(S\); write the resulting order \(P+S\). The newborn mark \(b\) is independently fair. The branch map is

\[
 \mathcal B^{P,r}_{S,b}(\mathfrak D)
       =\frac{q(P,r,S)}2\,\mathfrak D .
 \tag{1}
\]

The admitted model requires:

- Every ideal is eligible, \(q(P,r,S)>0\), and the complete ideal sum is one.
- A proper-slot probability may read the whole unmarked order \(P\), but only the marks in \(S\). A full slot may read all old marks.
- Relabeling transports order, ideal and marks together; probabilities are equivariant.
- Two incomparable births commute as complete unnormalized marked maps. Both newborn bits, equal-precursor pairs and all inherited marks are included.
- There is one committed birth at a step. This bookkeeping step is not a physical clock and is not a claim that every present relational activity creates a record.

For two ideals \(S,T\) of a base \(C\), with the new vertices excluded from the second precursors, the diamond identity is

\[
 q(C,r,S)q(C+S,r+b,T)
   =q(C,r,T)q(C+T,r+c,S).
 \tag{2}
\]

Both sides multiply the same transported terminal payload by \(1/4\). Equation (2) is not merely agreement of normalized probabilities or diagonal payloads.

For a proper ideal in a nonempty parent, let \(M=\operatorname{Max}(P)\setminus S\). Its fixed maximal-deletion potential is

\[
 u(P,r,S)=
 \prod_{\varnothing\ne A\subseteq M}
 q(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}} .
 \tag{3}
\]

These are evaluations of smaller mathematical inputs, not erasure of committed history. Full smaller-parent slots retain their full induced marks.

The admitted ratio-component theorem says that (3) satisfies all inherited ratio equations and that every positive solution at the next layer has the form
\(q(P,r,S)=\alpha_{\mathcal C(P,S,r|S)}u(P,r,S)\) on proper slots. The component key keeps the whole unmarked parent and selected marks. All labeled ideal occurrences contribute separately to row sums. Full slots are normalization complements.

### The fixed instance, not a uniquely selected law

The smaller seed is prescribed:

\[
 a_{\rm seed}=2/3,\quad c_{\rm seed}=1/5,\quad d_{\rm seed}=1/4,
 \quad f_{\rm seed}(0)=1/6,\quad f_{\rm seed}(1)=1/3,
\]
\[
 g_{\rm seed}=1/10,\quad k_{\rm seed}=11/20,\quad
 h_{\rm seed}(0)=19/30,\quad h_{\rm seed}(1)=7/15,\quad e=1/44 .
\]

The singleton, two-chain and two-antichain ideal rows are
\((a_{\rm seed},1-a_{\rm seed})\),
\((c_{\rm seed},f_{\rm seed}(i),h_{\rm seed}(i))\), and
\((d_{\rm seed},g_{\rm seed},g_{\rm seed},k_{\rm seed})\).
The parent-three proper rows are:

| Parent | Proper ideal probabilities |
| --- | --- |
| Three-antichain | Empty \(e\); each singleton \(eg_{\rm seed}/d_{\rm seed}\); each pair \(ek_{\rm seed}/d_{\rm seed}\) |
| Edge \(u<v\), isolate \(w\) | Empty and \(w\): \(e\); \(u\): \(ef_{\rm seed}(r_u)/c_{\rm seed}\); \(uv\): \(eh_{\rm seed}(r_u)/c_{\rm seed}\); \(uw\): \(ek_{\rm seed}/g_{\rm seed}\) |
| Fork | Empty and root: \(e\); each root-plus-leaf ideal \(eh_{\rm seed}(i)/f_{\rm seed}(i)\) |
| Join | Empty, each root singleton and root pair: \(e\) |
| Three-chain | Empty, root and initial pair: \(e\) |

Every full slot is the complete complement. At parent four, the instance uses the prescribed component witness described in *Normalization versus height growth*, not a newly optimized vector. At parent five it uses the primary-then-sequential-lexicographic expected-defect minimizer of §9, restored by

\[
 \widetilde\alpha=(35/36)\alpha^{\min}+\theta\mathbf1,\qquad
 \theta=c_5/36,\qquad c_5=\frac1{2(1+M_5)}.
 \tag{4}
\]

The exact prescribed parent-four witness and parent-five finite certificate are admitted inputs, not all reproduced numerical tables. Their identities and status are in §12. All coefficient facts used below are printed in §§4–8. Accordingly the mathematical statements are conditional on those facts; this package does not claim to reconstruct all 109 or 798 coordinates from the few displayed rows.

The baseline \(B\) preserves that prefix and uses the common half-scale continuation at parent sizes \(n\ge6\):

\[
 a_n=\frac1{2(1+M_n)},\qquad
 M_n=\max_{P,r}\sum_{S\subsetneq P}u(P,r,S),\qquad
 q_B(P,r,S)=a_nu(P,r,S)\quad(S\subsetneq P).
 \tag{5}
\]

The maximum is over the whole marked layer. Write \(\rho=a_6,\ s=a_7\). No selected-support maximum or fitted numerical scale replaces them.

## 2. The finite harmonic question

Let \(C_k,A_k\) denote a chain and an antichain; \(\oplus,\sqcup\) denote ordinal sum and disjoint union. Put \(I=C_3\), and \(T_j=I\oplus Q_j\), with this fixed order:

| \(j\) | Four-event cap \(Q_j\) |
| ---: | --- |
| 1 | \(A_4\) |
| 2 | \(C_2\sqcup A_2\) |
| 3 | \((A_2\oplus A_1)\sqcup A_1\) |
| 4 | \((A_1\oplus A_2)\sqcup A_1\) |
| 5 | \(C_2\sqcup C_2\) |
| 6 | The order with \(0<2,\ 0<3,\ 1<3\) |
| 7 | \(C_3\sqcup A_1\) |
| 8 | \(A_2\oplus A_2\) |
| 9 | \(A_1\oplus A_3\) |
| 10 | \(A_1\oplus(C_2\sqcup A_1)\) |
| 11 | \(C_2\oplus A_2\) |

These exhaust four-event caps with at least two maxima. The five possible six-parent classes are

\[
 \mathcal P_i=I\oplus R_i,\qquad
 (R_1,\ldots,R_5)=(A_3,C_2\sqcup A_1,A_2\oplus A_1,
                         A_1\oplus A_2,C_3).
\]

Use the admitted nonzero harmonic direction \(z\), normalized by
\(z_1=1,\ |z_j|\le1\), every \(z_j\ne0\). Define
\(Z(T_j)=z_j\), zero on every other seven-order class. It obeys, on every complete marked six-parent row,

\[
 \sum_{S\text{ ideal of }C}q_B(C,r,S)Z(C+S)=0.
 \tag{6}
\]

This finite direction is an admitted result, not selected anew here. The full supported equations, with actual held quantities
\(a=q(I,I), b=q(C_4,I), c=q(C_4,C_4)\),
\(d=q(C_5,I), e'=q(C_5,C_4), f=q(C_5,C_5)\),
\(g=q(I\oplus A_2,I), h=q(I\oplus A_2,I+\text{one cap})\),
and \(j=q(I\oplus A_2,I\oplus A_2)\), are

\[
\begin{array}{ll}
 \mathcal P_1:&(ag^3/b^3)z_1+3(h^2/c)z_2+3jz_3=0,\\
 \mathcal P_2:&(dg/b)z_2+(e'h/c)z_4+hz_5+jz_6+fz_7=0,\\
 \mathcal P_3:&gz_3+2hz_6+jz_8=0,\\
 \mathcal P_4:&(d^2/b)z_4+((e')^2/c)z_9+2fz_{10}=0,\\
 \mathcal P_5:&dz_7+e'z_{10}+fz_{11}=0.
\end{array}                                                    \tag{7}
\]

Each equation retains its induced records. The factors three and two count distinct forward ideals, not backward deletion multiplicities.

Set \(h_n=1\) for \(n\le6\), and \(h_7=1+\epsilon Z\), \(0<\epsilon\le1/4\). This defines an admissible perturbed prefix through seven births. Seek one record-blind value \(x_H=h_8(H)\) for every eight-order class. Each value is shared by all parent aliases, marks and newborn outcomes. Define

\[
 A_{(P,r),H}=\sum_{S:[P+S]=H}q_B(P,r,S),\qquad A\mathbf1=\mathbf1.
\]

Then extension through eight births in this relative class is equivalent to

\[
 Ax=\mathbf1+\epsilon Z,\quad x_H>0\ \text{for all }H,
 \qquad x=\mathbf1+\epsilon y:
 \quad Ay=Z,\quad 1+\epsilon y_H>0 .
 \tag{8}
\]

The candidate law is \(q_Q=q_Bx_{[P+S]}/h_7(P)\). Normalization gives (8); locality follows from the unmarked multiplier. Diamond factors telescope to the same \(h_8/h_6\). This proves necessity and sufficiency within the declared relative class, not existence at every amplitude.

For any homogeneous correction \(\delta y\), all private full slopes can be eliminated without dropping their positivity conditions: if \(F(P)\) appends a unique greatest vertex, its only incoming parent is \(P\). With full coefficient \(b_r>0\) and proper row \(a'_r\),

\[
 (b_0a'_r-b_ra'_0)\delta y_{\rm proper}=0,\qquad
 \delta y_{F(P)}=-a'_0\delta y_{\rm proper}/b_0 .
 \tag{9}
\]

All remaining marked contrasts, not just one pair, are required.

## 3. Positive one-layer theorem at small amplitude

**Theorem 1.** Let the admissible baseline and connected supported seven-orders above satisfy (6). Put \(E(P)=P\sqcup A_1\),
\(J_j=E(T_j)\), and \(e_P=q_B(P,r,\varnothing)>0\), independent of records. Then

\[
 y^*_{J_j}=z_j/e_{T_j},\qquad y^*_H=0\text{ otherwise}
 \tag{10}
\]

solves the complete system \(Ay=Z\). It gives a strictly positive extension through eight births for

\[
 0<\epsilon\le1/4,\qquad
 \epsilon<\epsilon_{\rm lift}:=
     \min_{z_j<0}\frac{e_{T_j}}{-z_j}.
 \tag{11}
\]

The minimum is finite and positive; equality is not admitted.

**Proof.** A child \(J_j\) has one isolated vertex and a connected seven-vertex core. Every incoming parent is either \(T_j\) or one of \(D_i=E(\mathcal P_i)\), and there are no others. The supported forward occurrences from \(D_i\) have counts \(7,5,4,4,3\), respectively, inherited from (7). The \(T_j\) row contributes exactly its empty term \(e_{T_j}y^*_{J_j}=z_j\).

For an individual birth \(C+S=T_j\), the complete empty-birth diamond gives

\[
 q_B(C,r,S)e_{T_j}=e_Cq_B(E(C),r+\text{isolate mark},S).
\]

Thus the \(D_i\) row of (10) is \(e_{\mathcal P_i}^{-1}\) times (6), hence zero for every mark. Outside these sixteen parents no supported column is incoming. Both bits and the full payload retain their common \(1/4\) factors before cancellation. This proves all rows, without a global enumeration.

Every unlisted multiplier is one. For listed children positivity is exactly
\(e_{T_j}+\epsilon z_j>0\), giving (11). At least one \(z_j\) is negative because the positive-coefficient first equation of (7) has \(z_1=1\). ∎

This is a genuine positive one-layer theorem, not merely a local witness. It does not provide a uniform amplitude at all future sizes, or an all-size record-blind harmonic continuation. Connected-core uniqueness is used in the closure proof and cannot simply be reused after arbitrary isolated vertices have accumulated.

## 4. Coordinates and the complete natural thirty-class system

### Coordinate dictionary and its limit

The three proper connected child classes are

\[
 H_0=I\oplus A_5,\quad
 H_2=I\oplus(C_2\sqcup A_3),\quad
 H_3=I\oplus((A_2\oplus A_1)\sqcup A_2).
\]

The natural support is exactly

\[
 \mathcal S_{30}=\{H_0,H_2,H_3,J_1,\ldots,J_{11},
                  F(T_1),\ldots,F(T_{11}),F(D_1),\ldots,F(D_5)\}.
 \tag{12}
\]

All thirty classes are distinct. The \(H\)'s are connected with several maxima, the \(J\)'s have component sizes \(7+1\), and the \(F\)'s have a unique greatest vertex whose deletion identifies its parent.

| Object | Exact convention |
| --- | --- |
| Relative multiplier | \(x_H=1+\epsilon y_H\) |
| Proper-child correction | \(\eta_s=\delta y_{H_s}\), \(s=0,2,3\) |
| Isolated-child coordinate | \(W_j=e_{T_j}\delta y_{J_j}\), not \(\delta y_{J_j}\) |
| Connected private slope | \(v_j=\delta y_{F(T_j)}\) |
| Disconnected private slope | \(d_i=\delta y_{F(D_i)}\) |
| Historical local \(X_0,Y_0,Y_1,Y_2\) | \(X_0=J_1;\ (Y_0,Y_1,Y_2)=(H_0,H_2,H_3)\) |
| Component amplitude variation | With \(m_j=1+\epsilon z_j\): \(\delta\alpha(H_0)=s\epsilon\eta_0/m_1^5\), \(\delta\alpha(H_2)=s\epsilon\eta_2/(m_1m_2^3)\), \(\delta\alpha(H_3)=s\epsilon\eta_3/(m_1m_3^2)\) |

The last row follows by counting every maximal deletion in
\(\alpha(H)=s x_H/\prod_{v\in\operatorname{Max}(H)}h_7(H-v)\).
If one varies \(x\) rather than \(y\), its factor \(\epsilon\) is absent.

**Unresolved historical dictionary.** A bounded lookup of three admitted historical text bodies confirms a genuine partial role statement: \(u_0,u_2,u_3\) are described as the proper-child variations themselves. The same passage prints the isolated-child formula \(\delta y_{J_j}=W_j/e_j\), in its historical notation. The variables are therefore not wholly unnamed auxiliaries, but the isolated-child formula cannot be extended to the proper children by analogy.

The remaining premise is an original definition identifying the child for each \(u_s\), its varied quantity and scale/sign or mixing relative to \(\eta_s\) at the same law and amplitude, the complete original support and zero-column convention, and the corresponding all-record \(\Gamma/\beta\) elimination and recovery. Neither that complete dictionary nor an exact title/path identified as supplying it was located in those three bodies. This finite source finding asserts neither global absence nor mathematical impossibility, and current source-identity checks do not reconstruct historical custody.

Matching suffixes, support counts or sparse row shapes does not establish that map. If a valid source supplied \(\eta_s=k_su_s\), the historical proper columns would be \(p_{js}k_s\), not \(p_{js}\); a general linear dictionary would require its full matrix. No such missing map is inserted here. The classification below is for (12) with the explicit natural conventions above. Historical formulas are preserved separately, not silently identified with it.

### Held rows and bounds

Use \(i=0,1\) for the initial root bit and \(\Delta=\text{root }1-\text{root }0\). Let \(\mathcal J=(\varnothing,\text{root},\text{initial pair},I)\). The required fixed-law data are

\[
 A=(1/44,1/44,1/44,41/44),\quad a=41/44,\quad
 B_\varnothing=B_{\rm root}=1/352,
\]
\[
 B_{\rm pair}(0)=1/352,\ B_{\rm pair}(1)=27/5500,\quad
 b_0=8077/8800,\ b_1=40303/44000,
\]
\[
 c_0=81/1100,\ c_1=3231/44000,\quad
 G_S=\theta B_S^2/A_S,\quad
 D_S=\theta B_S+\mu_i1_{S=\rm root},
\]
\[
 h_i=\theta c_i,\quad
 j_i=1-\theta Q_{2,i}-2\theta c_i,\quad
 \ell_i=1-\theta-\mu_i,\quad
 Q_{k,i}=\sum_{S\in\mathcal J}B_S^k/A_S^{k-1}.
 \tag{13}
\]

These complete held rows are root-only by admitted all-mark proofs, not by sampling. They do not make every disconnected lower row root-only. The bounds are

\[
 0<\theta<10^{-10},\quad 0<\rho<1/7,\quad0<s<1/6,\quad
 0\le\mu_i<1/26,\quad B_S/A_S<1 .
 \tag{14}
\]

All actual seven-parent full probabilities exceed \(1/2\).
Write \(f_j(r)=q_B(T_j,r,T_j)\) and \(g_i(r)=q_B(D_i,r,D_i)\).

The five proper coefficients needed for the first three rows are

\[
\begin{array}{lll}
 p_{10}=s\rho^4\theta^6b^4/a^3,&
 p_{12}=4s\rho^3\theta^3c,&p_{13}=6s\rho^2j,\\
 p_{22}=s\rho^3\theta^4b^3/a^2,&
 p_{33}=s\rho^2\theta^3b^3/a^2.&
\end{array}                                                    \tag{15}
\]

The first three complete rows are

\[
 W_1+p_{10}\eta_0+p_{12}\eta_2+p_{13}\eta_3+f_1v_1=0,
\quad W_2+p_{22}\eta_2+f_2v_2=0,
\quad W_3+p_{33}\eta_3+f_3v_3=0.
 \tag{16}
\]

There are respectively 19, 15 and 13 individual ideals. \(H_2\) occurs four times from \(T_1\) and once from \(T_2\); \(H_3\) six times from \(T_1\) and once from \(T_3\). Unlisted terms have zero correction, not zero baseline probability.

For \(j=4,\ldots,11\), the row is \(W_j+f_jv_j=0\). The five disconnected rows are

\[
 \rho l_i/e_{\mathcal P_i}+g_id_i=0,
\]
\[
\begin{array}{l}
 l_1=(\theta^3b^3/a^2)W_1+3\theta^2cW_2+3jW_3,\\
 l_2=(\theta^2b^2/a)W_2+\theta^2cW_4+\theta cW_5+jW_6+\ell W_7,\\
 l_3=(\theta b^2/a)W_3+2\theta cW_6+jW_8,\\
 l_4=\theta^2bW_4+\theta^2cW_9+2\ell W_{10},\\
 l_5=\theta bW_7+\theta cW_{10}+\ell W_{11}.
\end{array}                                                    \tag{17}
\]

Equations (16)–(17), the eight remaining connected rows, all 128 markings per parent, and the exhaustive incoming closure are the full system. Full-slope recovery is
\(d_i=-\rho l_i(0)/(e_{\mathcal P_i}g_i(0))\), with every contrast
\(g_i(0)l_i(r)-g_i(r)l_i(0)=0\) retained.

## 5. Complete signed kernel and both unresolved branches

The following coefficient lemmas belong to the fixed admitted law. They are not asserted for every law satisfying §1.

| Fixed-law lemma | Consequence / role |
| --- | --- |
| \(\Delta f_1,\Delta f_3>0\); complete relevant old profiles root-only | Valid natural front elimination on every mark |
| \(f_j\) nonconstant for \(j=4,5,6,7\) | \(W_j=v_j=0\) |
| \(h_b=\theta^2[g_2(0)b_1^2/a-g_2(1)b_0^2/a]<0\) | \(D_2\) forces \(W_2=0\) on the natural support |
| \(C_{\rm nat}=p_{22}(0)f_2(1)-p_{22}(1)f_2(0)>p_{22}(0)(1/400-1/546)>0\) | \(\eta_2=v_2=0\), including \(\Delta f_2=0\) |
| \(f_8=f_{11}=f_*=1-s(2-2\rho+\rho^2)>2/3\) | Constant-profile recoveries |
| \(A_*<0,\ Q_8>0\), as defined below | Complete front line |
| \(t_{11}\ne0\); \(\Delta f_{10}=0\) iff \(\mu_1=\mu_0\); \(\Delta f_9=0\Rightarrow a_9<0\) | Exhaustive rear elimination |
| Equal \(\mu\) gives \(\Delta f_9=\Delta f_{10}=0,\ a_{10}>0\) | Independent rear line only in that branch |

These admitted lemmas are sufficient to verify the classification without dividing by \(\Delta f_2\), \(\Delta\mu\), or an unproved nonzero numerator.

Define natural, not historical, coefficients:

\[
 \beta_{10}=-\Delta p_{10}/\Delta f_1,\quad
 \beta_{13}=-\Delta p_{13}/\Delta f_1,\quad
 \gamma_{10}=p_{10}(0)+f_1(0)\beta_{10}>0,\quad
 \gamma_{13}=p_{13}(0)+f_1(0)\beta_{13},
\]
\[
 \beta_3=-\Delta p_{33}/\Delta f_3>0,\qquad
 \gamma_3=p_{33}(0)+f_3(0)\beta_3>0,
\]
\[
 A_*=(\theta^3/a^2)[g_1(0)b_1^3-g_1(1)b_0^3]<0,\quad
 J_*=3[g_1(0)j_1-g_1(1)j_0],
\]
\[
 P_*=(\theta/a)[g_3(0)b_1^2-g_3(1)b_0^2],\qquad
 Q_8=g_3(0)j_1-g_3(1)j_0>0.
\]

Set

\[
 q_1=J_*\gamma_3/A_*,\quad q_3=-\gamma_3,\quad
 q_8=P_*\gamma_3/Q_8,\quad
 \alpha_0=-(q_1+\gamma_{13})/\gamma_{10},\quad
 \chi_1=\beta_{10}\alpha_0+\beta_{13}.
\]

For every real \(t\), the front is

\[
 \eta_3=t,\ \eta_0=\alpha_0t,\quad
 (W_1,W_3,W_8)=(q_1,q_3,q_8)t,\quad
 (v_1,v_3,v_8)=(\chi_1,\beta_3,-q_8/f_*)t.
 \tag{18}
\]

Always \(\eta_2=W_2=v_2=W_4=\cdots=W_7=v_4=\cdots=v_7=0\).

For the rear define

\[
 a_9=\theta^2[g_4(0)c_1-g_4(1)c_0],\quad
 a_{10}=2[g_4(0)\ell_1-g_4(1)\ell_0],
\]
\[
 t_{10}=\theta[g_5(0)c_1-g_5(1)c_0],\quad
 t_{11}=g_5(0)\ell_1-g_5(1)\ell_0\ne0.
\]

If \(\mu_1\ne\mu_0\), all rear \(W_9,W_{10},W_{11},v_9,v_{10},v_{11},d_4,d_5\) are zero. If \(\mu_1=\mu_0\), put
\(a_r=-a_9/a_{10}>0,\ b_r=-(t_{10}/t_{11})a_r\). For an independent real \(w\),

\[
 (W_9,W_{10},W_{11})=(1,a_r,b_r)w,\qquad
 (v_9,v_{10},v_{11})=(-1/f_9(0),-a_r/f_{10}(0),-b_r/f_*)w.
 \tag{19}
\]

No division by \(t_{10}\), or nonzero assumption on \(b_r\), is made. The private recoveries are

\[
 d_1=-\frac{\rho[(\theta^3b_0^3/a^2)q_1+3j_0q_3]t}
                  {e_{\mathcal P_1}g_1(0)},\quad d_2=0,\quad
 d_3=-\frac{\rho[(\theta b_0^2/a)q_3+j_0q_8]t}
                  {e_{\mathcal P_3}g_3(0)},
\]
\[
 d_4=-\frac{\rho[\theta^2c_0+2\ell_0a_r]w}{e_{\mathcal P_4}g_4(0)},
 \qquad
 d_5=-\frac{\rho[\theta c_0a_r+\ell_0b_r]w}{e_{\mathcal P_5}g_5(0)}
 \quad\text{only in the equal-}\mu\text{ branch}.
 \tag{20}
\]

Actual isolated slopes are \(W_j/e_{T_j}\).

**Theorem 2.** Equations (18)–(20) are exactly the signed homogeneous kernel on \(\mathcal S_{30}\). Its dimension is one for unequal \(\mu\), two for equal \(\mu\).

**Proof.** Nonconstant connected profiles eliminate \(4,\ldots,7\). The \(D_2\) contrast then gives \(W_2=0\), and \(C_{\rm nat}>0\) eliminates \(\eta_2,v_2\) without a zero-pivot exclusion. The first and third rows yield the natural \(\beta,\gamma\) formulas. The \(D_1,D_3\) contrasts are precisely
\(A_*W_1+J_*W_3=0\) and \(P_*W_3+Q_8W_8=0\), giving (18).

For unequal \(\mu\), nonconstant \(f_{10}\) gives \(W_{10}=0\). Either \(f_9\) is nonconstant, or its flat case has \(a_9<0\); in both cases \(W_9=0\). Then \(t_{11}\ne0\) gives \(W_{11}=0\). For equal \(\mu\), the two constraints are \(a_9W_9+a_{10}W_{10}=0\) and \(t_{10}W_{10}+t_{11}W_{11}=0\), giving (19).

Reference recoveries give (20). Substitution verifies every connected row and every root contrast; the admitted complete-profile reductions extend this to every old mark. Outside the sixteen parent classes no supported column is incoming. Finally \(\eta_3=t\) and \(W_9=w\) show independence and the stated dimensions. ∎

## 6. Fixed-amplitude obstruction, not an all-amplitude obstruction

The affine reference (10) lies in \(\mathcal S_{30}\). Every supported affine solution differs from it by Theorem 2 and therefore has \(W_2=0\).

From the two root-sector \(\mathcal P_1\) harmonic equations in (7),

\[
 \theta^3b_i^3/a^2+3\theta^2c_i z_2+3j_i z_3=0.
\]

Let \(N=b_0^3j_1-b_1^3j_0\) and \(D=c_0j_1-c_1j_0\). The held values give
\(b_0>b_1>0,\ c_0>c_1>0,\ j_1>j_0>1/2\), hence \(N,D>0\). Elimination yields

\[
 z_2=-\frac{\theta N}{3a^2D}<-\theta/3000.
 \tag{21}
\]

For the bound, \(b_0-b_1>1/1000\) and \(b_i>9/10\) imply
\(b_0^3-b_1^3>1/500\), so \(N>1/1000\); also \(3a^2D<3\).
The unique empty-slot occurrence in \(T_2\) has

\[
 e_{T_2}=s\rho^3\theta^4/22528<\theta^4 .
 \tag{22}
\]

Thus at the prescribed \(\epsilon=1/4\),

\[
 e_{T_2}+z_2/4<\theta^4-\theta/12000<-\theta/24000<0.
 \tag{23}
\]

**Theorem 3.** No affine solution supported on \(\mathcal S_{30}\) is strictly positive at amplitude \(1/4\), in either \(\mu\) branch. The shared \(J_2\) multiplier is negative for every member of that affine family.

This is not a contradiction of Theorem 1. Its positive interval requires
\(\epsilon<e_{T_2}/(-z_2)\), among other inequalities. Fixing \(1/4\) is a different quantifier. Reducing \(\epsilon\) changes the deformation; it is not a repair of the prescribed endpoint.

All other conditions remain \(1+\epsilon(y_H^*+\delta y_H)>0\), for every child, including the recovered full slopes. No artificial bound \(x_H\le1\) is imposed. Normalized transition bounds follow from the complete positive row sum.

## 7. The precise 33- and 38-class exclusions

To avoid collisions with the small canonical carriers in §9, use subscript \(+\) for enlarged-support orders. Put \(H=I\oplus A_2\) and

\[
 K_+=\mathcal P_2\sqcup C_2^{\rm chain},\quad
 E_H=H\sqcup C_2^{\rm chain},\quad
 E_C=C_5^{\rm chain}\sqcup C_2^{\rm chain}.
\]

Here \(\mathcal P_2=I\oplus(C_2^{\rm chain}\sqcup A_1)\) is the six-parent from §2; the superscript distinguishes ordinary chains from indexed parent classes. Equivalently,
\(K_+=[I\oplus(C_2^{\rm chain}\sqcup A_1)]\sqcup C_2^{\rm chain}\).
Define

\[
 \mathcal S_{33}=\mathcal S_{30}\cup\{K_+,F(E_H),F(E_C)\},
\]
\[
 A_H=H\sqcup A_2,\quad A_C=C_5^{\rm chain}\sqcup A_2,\quad
 B_+=C_4^{\rm chain}\sqcup C_2^{\rm chain}\sqcup A_1,
\]
\[
 \mathcal S_{38}=\mathcal S_{33}\cup
 \{L_H=E_H\sqcup A_1,L_C=E_C\sqcup A_1,F(A_H),F(A_C),F(B_+)\}.
 \tag{24}
\]

The incoming closure is complete:

| Added child | Incoming parents and forward multiplicities |
| --- | --- |
| \(K_+\) | \(D_2\): isolate singleton once; \(E_H\): either twin-cap extension, twice; \(E_C\): \(I\), once |
| \(F(E_H),F(E_C)\) | Its named parent only, full once |
| \(L_H\) | \(E_H\): empty once; \(A_H\): either isolate singleton, twice; \(B_+\): \(I\), once |
| \(L_C\) | \(E_C\): empty once; \(A_C\): either isolate singleton, twice; \(B_+\): whole four-chain, once |
| \(F(A_H),F(A_C),F(B_+)\) | Its named parent only, full once |

Maximal deletion proves exhaustiveness. It does not replace the displayed forward multiplicities. The complete systems have respectively eighteen and twenty-one seven-parent classes, each with all 128 marks.

For \(\mathcal S_{38}\), let the eight added slopes be
\(k,d_H,d_C,W_H/e_{E_H},W_C/e_{E_C},d_{AH},d_{AC},d_B\).
Retain the old equations, except that \(D_2\) gains \(\psi_Dk\). The additional rows are

\[
\begin{array}{l}
 W_H+\psi_Hk+f_Hd_H=0,\qquad W_C+\psi_Ck+f_Cd_C=0,\\
 8\Lambda W_H+g_{AH}d_{AH}=0,\qquad
 \Lambda W_C+g_{AC}d_{AC}=0,\\
 (\rho/e_X)[(\theta^2/8)bW_H+\theta cW_C]+g_Bd_B=0.
\end{array}                                                    \tag{25}
\]

Here every full coefficient is the actual complete complement; \(X=C_4^{\rm chain}\sqcup C_2^{\rm chain}\), and

\[
 \psi_D=s\rho^2\theta^2k_\varnothing^+>0,\quad
 \psi_H=2s\rho^2\theta^2c,\quad
 \psi_C=\lambda b,\quad \lambda=s\rho^2\theta^3/8>0,\quad
 \Lambda=2k_\varnothing^+/y_\varnothing>0.
\]

The lower \(k_\varnothing^+,y_\varnothing\) are the actual isolate-singleton and empty probabilities in the four- and five-parent disconnected carriers, not independent adjustable coefficients. The 33-class equations set \(W_H,W_C,d_{AH},d_{AC},d_B=0\).

### Three additional slopes: no mobility

The complete \(E_C\) proper-potential sum \(B_C\) obeys
\(|B_C(r)-(2-2\rho+\rho^2)|<200\rho\theta\).
Since \(f_C=1-sB_C>1/2\), \(b_0-b_1>1/1000\), and \(\theta<10^{-10}\),

\[
 f_C(0)\psi_C(1)-f_C(1)\psi_C(0)<-\lambda/4000<0 .
 \tag{26}
\]

The two \(E_C\) rows on the 33-class support therefore force \(k=d_C=0\); the \(E_H\) row gives \(d_H=0\). Only then does the old \(D_2\) equation return. Thus its kernel is exactly Theorem 2 with three zeros, and Theorem 3 applies.

### Eight additional slopes: both residual sectors vanish

The 38-class system cannot initially use the preceding two-column elimination: it has added constant columns. Two further fixed-law facts resolve it.

First, the original four marked prefix roles in the order
\(K_4=(r<a<b)\sqcup\{u\}\) satisfy

\[
 q(K_4,\{r,a,u\};i,j)=(65/88)(361/1000)=4693/17600
 \quad\text{for all }i,j.
 \tag{27}
\]

They are four distinct components with equal prescribed values. The complete marked diamond joins them to original component roots
\((70,11,i+2j)\); the potential is \(65/88\), not one.

For \(V=(r<a<b)\sqcup\{u,z\}\), its eight one-isolate occurrences sum to
\(Q_V=2\theta[C+(\lambda_2-1)t_{ij}]\), with \(C,\lambda_2\) record-constant. Equation (27) gives \(\Delta Q_V=0\). The full \(A_H\) complement has
\(\Delta g_{AH}=s\rho(T_H-K_A\Delta Q_V)<0\),
where \(K_A>0\) and the admitted complete expansion gives
\(T_H<-\theta/7\).
Thus the \(A_H\) rows in (25) force \(d_{AH}=W_H=0\).
The actual \(E_H\) determinant
\(f_H(0)c_1-f_H(1)c_0<0\) then forces \(k=d_H=0\), and the old \(D_2\) contrast forces \(W_2=0\).

Second, the residual \(C\) rows are
\(W_C+f_Cd_C=0,\ \Lambda W_C+g_{AC}d_{AC}=0,\
(\rho\theta/e_X)cW_C+g_Bd_B=0\).
A nonzero \(W_C\) would require \(f_C\) constant on its whole marked domain. It is not.

For completeness the decisive bound follows from the complete seventeen-proper-slot expansion. Let \(U=I\sqcup(u<v)\),
\(U_{0S}=q(U,S)\), \(Q_U=\sum_{S\in\mathcal J}q(U,S+u)\),
\(r_S=B_S/A_S\), \(R_U=c+\sum U_{0S}r_S\),
\(\omega=5/352\), and \(K_\mu=44\rho U_{0,\rm root}-\omega\).
Writing
\(H_B=\sum\alpha_SB_S+c\),
\(\alpha=(5/352,5/352,203153/8800,1/8)\),
and \(T=138697/387200\), the expansion is

\[
 B_C=2-2\rho+\rho^2+\rho\theta[
 (2-\rho-\theta)H_B+(\rho\theta-1)R_U+(1-\rho)T
 +K_\mu\mu_i+(\rho-1)Q_U].
 \tag{28}
\]

The canonical-support carrier argument makes all four \(U_{0S}\) restoration-only and record-constant, with \(\sum U_{0S}<1/72\). The separate one-isolate restoration argument gives \(0<Q_U<1/72\), without making its full profile root-only. The held bounds give
\(\Delta H_B>1/25,\ |\Delta R_U|<1/500,\ |K_\mu|<1/8,\
|\Delta\mu|<1/26\). Therefore, for every root flip with all other marks fixed,

\[
 \frac{\Delta B_C}{\rho\theta}>
       1/25-1/500-1/208-1/72>1/100,\qquad
 \Delta f_C<-s\rho\theta/100<0.
 \tag{29}
\]

To see why restoration-only is justified rather than assumed, append a vertex above each stem ideal \(S\) to obtain \(C_S\). Its largest induced Ferrers suborder has at least three vertices. A nonempty Ferrers order cannot span two disconnected components. Hence changing
\(C_S\sqcup A_1\) to \(C_S\sqcup C_2^{\rm chain}\) raises arbitrary-vertex deletion defect by one. The admitted canonical everywhere-neutral support theorem sets that carrier's boundary component to zero. The complete lower diamonds transport its strict coefficient \(\theta\) to \(q(U,S)=\theta u(U,S)\). This is not a zero strict probability.

Equation (29) forces \(d_C=W_C=0\), then \(d_{AC}=d_B=0\). All eight new slopes vanish. Every new marked row is now identically zero, and all old rows have exactly the recoveries (18)–(20).

**Theorem 4.** On the fixed law, both \(\mathcal S_{33}\) and \(\mathcal S_{38}\) have precisely the embedded natural kernel of Theorem 2. Their fixed-amplitude \(1/4\) positive affine families are empty. Neither statement classifies arbitrary larger supports or record-dependent relative weights.

This final classification supersedes the earlier *unresolved signed mobility* wording for the 38-class candidate. The earlier independent positivity rejection remains valid. Its history is preserved, not rewritten.

## 8. Exact status of the \(\mu\) comparison

The actual canonical selector uniquely specifies the finite law. “Both branches remain” means that this bounded proof has not determined which branch its actual coefficients occupy; it does not mean that the coefficients may be chosen freely.

Let \(C=r<a<b<c\), \(H^\sharp=(r<a<b<c,r<y)\), and
\(Q=(r<a<b,r<y)\). The canonical component \(\sigma_i\) has exactly two carriers: \(C_5^{\rm chain}\) at selected \(r\), and \(H^\sharp\) at selected \(C\). Their potentials are \(x=1/352\) and \(c_i\), respectively. Complete canonical capacities and primary optimality give

\[
 \sigma_i=(1-R_i)/c_i,\qquad
 \mu_i=(35/12672)\sigma_i,\qquad 0\le R_i\le1.
 \tag{30}
\]

The proof is not “negative cost implies allocation”: its complete objective coefficient is \(-c_i\Pi_{H^\sharp,i}<0\). If \(\sigma_i\) lay strictly below its smallest full carrier cap, increasing that one global coordinate would remain feasible and lower the primary objective. All coupled competitors remain inside \(R_i\).

Because \(c_1=(359/360)c_0\),

\[
 \mu_1-\mu_0=\frac{35}{12672}
        \frac{1-360R_1+359R_0}{359c_0}.
 \tag{31}
\]

Thus equality is exactly \(360R_1-359R_0=1\). No sign of its difference from one has been established.

The complete additional carrier identities narrow, but do not decide, the residuals. Put \(V=(r<a,r<y)\),
\(P^\sharp=(r<a<b,r<y,a<z,y<z)\),
\(K^\sharp=(r<a<b,r<y<t)\), and

\[
 p_i=q_Q(ry)>0,\quad g_{ij}=q_Q(ray;i,j)>0,\quad
 v_i=q_V(V)>0,\quad h_*=q_Q(rab)=41/352,\quad
 \bar g_i=\max_j g_{ij}.
\]

These are lower-law probabilities, distinct from §5's natural elimination coefficients. The canonical roles and their complete carriers are:

| Coefficient | Terminal / compulsory marks | Carrier occurrences per whole row |
| --- | --- | --- |
| \(\sigma_i\) | Hook \((5,1)\); root \(i\) | \(C_5^{\rm chain}\): one; \(H^\sharp\): one |
| \(\beta_i\) | Hook \((4,1,1)\); root \(i\) | \(H^\sharp\): one; \(K^\sharp\): two |
| \(\gamma_{ij}\) | Shape \((4,2)\); ordered marks \(i,j\) | \(H^\sharp\): one; \(P^\sharp\): one |
| \(\xi_i\) | Shape \((3,2,1)\); root \(i\) | \(P^\sharp\): one; \(K^\sharp\): one |

Exhaustive terminal-maximal deletions identify these carriers. Complete diamonds remove optional selected marks; compulsory marks remain. In the last row there are five quotient local nodes per root, not six: two from \(P^\sharp\), three from the arm-symmetric \(K^\sharp\). This does not double a forward ideal occurrence.

After the fixed canonical zero-support reduction, all marked carrier constraints are

\[
\begin{array}{ll}
 H^\sharp:&c_i\sigma_i+p_i\beta_i+g_{ij}\gamma_{ij}\le1,\\
 P^\sharp:&h_*\gamma_{ij}+(p_i/v_i)g_{im}\xi_i\le1,\\
 K^\sharp:&2h_*\beta_i+(g_{ij}g_{im}/v_i)\xi_i\le1.
\end{array}                                                    \tag{32}
\]

The chain carrier also imposes \(x\sigma_i\le1\), with \(x=1/352\). This constraint is redundant: the hook carrier gives \(\sigma_i\le1/c_i\), and the displayed values satisfy \(c_i>x\), hence \(x\sigma_i<1\). Thus omitting that inequality from (32) does not drop a binding carrier constraint.

Every \(j,m\) combination is retained. The competing \(P^\sharp\) potential uses two omitted maxima:
\(q_Q(ry)q_{(2,2)}(ry)/q_V(ry)=(p_i/v_i)g_{im}\).
Replacing it by a single deletion factor would be wrong.

Define actual loads \(G_i=\max_jg_{ij}\gamma_{ij}\),
\(Y_i=(p_i\bar g_i/v_i)\xi_i\),
\(Z_i=(\bar g_i^2/v_i)\xi_i\). Then

\[
 \bar g_iY_i=p_iZ_i,\quad
 R_i=p_i\beta_i+G_i,\quad
 \beta_i=\min\{1/p_i,(1-Z_i)/(2h_*)\},
\]
\[
 c_i\sigma_i+G_i=[1-p_i(1-Z_i)/(2h_*)]_+,\qquad
 \gamma_{ij}=\min\{G_i/g_{ij},(1-Y_i)/h_*\}.
 \tag{33}
\]

The beta and gamma equalities follow from complete-carrier saturation and global feasible-descent arguments. For example increasing \(\beta_i\) and decreasing \(\sigma_i\) at fixed \(H^\sharp\) load would strictly improve the \(K^\sharp\) objective if both singleton mass and \(K^\sharp\) slack were positive. Decreasing both gamma coordinates and increasing beta likewise cancels the entire \(H^\sharp\) contribution and strictly improves \(K^\sharp\). These are primary-descent contradictions, not lexicographic selections.

The full \(P^\sharp\) birth is the neutral rectangle \((3,3)\); it contributes zero, not negative, gamma or xi objective cost. The xi objective is the negative actual history-weighted \(K^\sharp\) sum, not \(-\bar g_i^2\) times uniform row counts.

Equations (32)–(33) do not license independent choices of \(G,Y,Z\) or determine the original ordered selector. No xi saturation or lexicographic allocation is added here. The residual comparison (31), and the original ordered-root binding of the two sigma entries, remain named gaps. Their resolution is not needed for Theorems 1, 3 or 4.

## 9. All-size existence, prescribed optimization and finite verification

These are different claims.

**Conditional extension existence.** Given the model's admissible finite prefix and the ratio-potential theorem, choosing sufficiently small positive component scales at each subsequent finite layer and taking full complements yields compatible positive extensions. The common choice (5) is one prescription. Consistent finite-history probabilities define an infinite classical history measure. This does not prove a desired asymptotic geometry or a record-blind relative continuation of a particular harmonic seed.

**Prescribed expected-defect recursion.** For a finite order \(P\), let
\(\delta(P)\) be the minimum number of arbitrary vertices removed to leave an induced Ferrers cell order, whose order is coordinatewise on a partition diagram. This is a diagnostic, not physical record deletion. Let \(d_j(S)\in\{0,1\}\) be its birth increment and let \(\pi_j\) be the actual prefix-history mass of a complete marked parent class, summing all natural histories with their \(q/2\) factors.

At a free layer form
\(A_{jc}=\sum_{S:\mathcal C=c}u_j(S)\),
\(K_n=\{\alpha\ge0:A\alpha\le\mathbf1\}\), and

\[
 \Phi_n(\alpha)=\sum_j\pi_j\left[
 d_j(P_j)+\sum_{S\subsetneq P_j}(d_j(S)-d_j(P_j))
                       u_j(S)\alpha_{\mathcal C(j,S)}\right].
 \tag{34}
\]

Minimize \(\Phi_n\) over \(K_n\), then minimize coordinates successively in the fixed canonical component order. This produces a unique prescribed boundary vector even if the primary optimum is nonunique. Mix it with \(c_n\mathbf1\) using \(\eta_n=1/(n+1)^2\). The strict all-size recursion exists by finite compactness and induction; it is a mathematical choice, not a DET selection principle.

If \(m_n=\min\Phi_n\) and \(r_n\) is the resulting expected increment, then
\(m_n\le r_n\le m_n+\eta_n\). Consequently expected, \(L^1\), and in-probability normalized sublinear defect are equivalent to
\(N^{-1}\sum_{n<N}m_n\to0\). That Cesaro estimate has not been proved. Almost-sure sublinearity requires a separate pathwise argument.

**Finite admitted verification.** The first free layer has admitted exact primary optimum \(m_5=6650803/108900000\), with distinct primary optima and an exact sequential canonical certificate. Its active canonical components are everywhere defect-neutral. This is a finite, instance-specific result, not an all-size support theorem. The actual strict mixture restores every proper branch and has full complements greater than \(1/72\).

This package neither executes nor reauthenticates that historical certificate. Current byte checks establish current source identity, not its mathematics or repaired historical execution custody.

## 10. Dependencies and claim scope

| Claim | Required input / scope | Not established |
| --- | --- | --- |
| Ratio-component characterization; positive continuation | Declared scalar-passive model and admitted deletion-potential theorem | Unique DET law |
| Theorem 1 | Positive baseline, connected support, complete harmonic identity (6) | Fixed \(1/4\) success; uniform all-size amplitude |
| Natural 30 kernel | Exact support, whole marked system, fixed-law coefficient lemmas | Historical \(u\)-dictionary; actual \(\mu\) branch |
| 30-class rejection | \(W_2=0\), (13)–(14), fixed \(z_1=1,\epsilon=1/4\) | All-support or all-amplitude impossibility |
| 33-class rejection and kernel | New incoming closure, determinant (26), old kernel | General support-independent obstruction |
| 38-class rejection and kernel | Complete (25), prescribed four-role equality (27), canonical restoration, (29) | Arbitrary alternative seed or selector |
| Canonical carrier/coupling identities | Complete carriers, exact objective, actual finite canonical zero support | Numerical allocation or cross-sector equality |
| Expected-defect recursion | Additional objective, ordering and mixing prescriptions | Cesaro decay, manifoldlike limit, optimal future policy |
| Arbitrary PSD maps retained | Scalar maps (1), complete terminal matching | Informative quantum dynamics or a reconstruction of QM |

The “prescribed witness”, “canonical optimum”, “strict restored law”, “baseline continuation”, and “harmonic deformation” are five distinct objects. A theorem about one must not be relabeled as a theorem about another.

## 11. Result boundaries and open questions

The established fixed-law results here are Theorems 1–4 and the explicit conditional identities above. Law dependence is addressed in [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md), the [family supplement](LAW_FAMILY_SUPPLEMENT.md) and the separate [singular-law kernel and width theorem](SINGULAR_LAW_WIDTH.md). That eleven-column family has rank ten and kernel dimension one even at an exceptional law; its occurrence comparison for \(\Xi\) remains unselected. The historical-definition lookup adds no theorem and does not complete the coordinate dictionary or reproduce the full parent-four and parent-five certificate tables.

The analysis does not investigate uniform coverage, noncollapse, enlarged supports, joint geometry, causal-operator extensions, or measure/divergence extensions. No additional coefficients or optimized laws are calculated. Determining the actual \(\mu\) branch would be necessary for a claim selecting the kernel's actual dimension; it is not necessary for the complete branch-conditional classification or the fixed-amplitude endpoint rejection.

The kinematic question remains whether a map from record/order/growth primitives to manifoldlike Lorentzian structure can be established. This package does not supply that map. A metric, Minkowski coordinates, Hilbert-space dynamics, physical amplitudes, Johnston kernel or borrowed growth parameter cannot be inserted and then claimed as a derivation of the same input.

This work does not validate the metric-as-record interpretation, rehabilitate the previously retired gravity proposal, establish production readiness, or supply the outstanding validation evidence. It establishes no empirical discriminator, mass/gravity derivation or physical clock. Separate software, empirical and book projects are outside its scope; their prior status is not changed by these results.

## 12. Compact provenance and evidence limits

The supporting proof titles and their mathematical roles are listed below. They identify inherited evidence, not additional axioms. Their exact current source identities are recorded separately.

| Proof title or topic | Role |
| --- | --- |
| *Normalization versus height growth* | Prescribed seed/parent-four witness; ratio-component and strict-capacity statements |
| *History-weighted expected-defect candidate* | Explicit all-size recursion and its unproved asymptotic condition |
| *Canonical completion* | Admitted finite parent-five solution, restoration and canonical support |
| *Four-vertex cap design* | Eleven-class support, exhaustive five-parent closure, full harmonic equations |
| *Harmonic extension* and *Signed extension* | Shared-child system and positive small-amplitude lift |
| Child-coordinate binding, natural block and natural compatibility proofs | Natural coordinate binding, coefficients and complete natural kernel; historical dictionary gap |
| Unchanged-coordinate obstruction and the three-class and thirty-eight-class support analyses | Fixed-amplitude 30/33/38 obstructions and exact enlarged systems |
| Marked-prefix binding and residual-sector rejection with complete recovery | Four-role prefix binding; final eight-added-slopes-zero classification |
| Singleton saturation, beta/gamma carrier capacities and neutral-staircase coupling | Canonical saturation, complete beta/gamma/xi carriers and coupled residuals |

The exact admitted parent-four certificate identity is SHA-256
3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969.
The admitted parent-five certificate identity is
f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b;
its strict-probability manifest identity is
7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378.
These identify the fixed inputs. Hashes alone are not proofs and are not new certificate reads or replays.

Scientific reasoning in this consolidation is manual. Inherited finite coefficient lemmas remain visibly inherited; the historical coordinate dictionary and actual branch are not filled by assumption. The preserved evidence record retains the entire predecessor and its designated recovery material, including missing original execution records, truncated displays, failed source-verification and receipt-matching attempts, and earlier provisional corrections. Present integrity checks do not erase or repair those historical limitations.

## Complete P4 child shape as a sufficient observation

The [child-shape manuscript](P4_CHILD_SHAPE_OBSERVATION.md) gives a conditional
fixed-pair sufficiency theorem for the complete unlabelled, unmarked child
order. The seven shapes preserve full-row TV; their coarsest sufficient
partition has four blocks locally off the exception and three at it. The
result removes the supplied parent embedding and newborn identity, retains
exact complete-order access, and supplies no physical observation channel.
Its equal- and unequal-mixture conclusions use the distinct benchmarks in §5.

## P4 model-label separation with nuisance parameters

The [nuisance-identifiability manuscript](P4_NUISANCE_IDENTIFIABILITY.md)
proves conditional separation of the baseline and fixed-amplitude perturbed
full child-shape laws when the baseline parameter and admitted common scale
may vary. The original prefix, parent and full old marking remain fixed.
Its invariant two-shape ratio requires no scale regularity or half-scale
selection. Individual parameter recovery, uniform finite-sample stability
and a physical observation channel are not supplied.

## P4 separation with different hidden marking mixtures

The [marking-mixture manuscript](P4_MARKING_MIXTURES.md) gives conditional
model-label separation even when the hypotheses use different old-marking
distributions and different nuisance parameters. Its two ratio intervals are
disjoint throughout the whole inherited perturbation neighborhood. The
fixed-instance all-mark held identities, fixed prefix and parent, and one
common scale per hypothesis remain essential. No parameter recovery, uniform
finite-sample guarantee or physical observation channel is supplied.

## A seed-calibrated P4 prefix-family separator

The [prefix-family manuscript](P4_PREFIX_FAMILY_SEPARATOR.md) binds the complete
held rows to their named C4/C5 slots and obtains the common separator
coefficient 648/25 for an explicitly constrained class of actual valid
prefixes. Each perturbable member must justify its own regular construction,
neighborhood and fixed amplitude. The class may be a singleton; no second
member or result for all canonical prefixes is established. The coefficient
is not a numerical probability effect, stability bound or physical detector.

## A prospective P4 diagnostic-event test

The [diagnostic-event manuscript](P4_DIAGNOSTIC_EVENT_TEST.md) gives a closed
capped rule under additional iid repetition and exact shape classification.
It distinguishes conditional diagnostic-label errors from raw-draw
availability and reports ABSTAIN when the event target is not reached.
A fixed latent-law model is treated separately. The illustrative rational
threshold and counts are prospective mathematical choices; no numerical
native availability, test implementation or physical observation is supplied.

## P4 separation under an explicit observation model

The [observation-channel manuscript](P4_OBSERVATION_CHANNEL.md) gives a
conditional channel-transfer theorem, a rare-event obstruction for fixed
positive OTHER leakage, and a sufficient restricted contamination condition.
It keeps the distinction between conservative envelopes and actual native
laws, conditional label errors and collection availability, and fixed-law
and run-latent observation models. Positive clean-channel orientation alone
does not certify the original thresholds. No calibrated physical channel or
operational validation is supplied.

## A conditional fixed raw-budget testing limit

The [fixed-budget testing theorem](P4_FIXED_BUDGET_TESTING_LIMIT.md) bounds
finite-observation total variation along an actually admitted positive-scale
pair approaching the rare-event boundary. No fixed finite raw cap uniformly
gives low false-positive probability and high power, even with an identity
or known invertible channel and arbitrary common randomized decision rules.
Low conditional error with abstention requires vanishing decision coverage
when the tolerance sum is below one. Exact-law distinction, conditional
occurrence and the separation from physical validation remain explicit.

## Separate synthetic application design

The [synthetic diagnostic benchmark plan](../../applications/synthetic_channel_benchmark_v1/BENCHMARK_PLAN.md)
is a separate application project using invented probabilities, not another
native-law result. Its manual design rejects C256's raw-observation cost
superiority over the standard sequential reference and specifies only minimal
operating-point conformance. Core/stress separation, fresh independent held-out
controls, simultaneous inference, costs and failure reporting are fixed.
No implementation, sampling, interval evaluation or benchmark has executed or
is authorized by the plan; no practical-value or physical-validation claim is
supplied. See its [publication scope](../../applications/synthetic_channel_benchmark_v1/PUBLICATION_NOTE.md).

## Half-scale event availability for a fixed eligible prefix

[Half-scale event availability](HALF_SCALE_EVENT_AVAILABILITY.md) gives a
conditional positive symbolic availability floor for one actual eligible
fixed prefix on its own fixed compact positive-lambda neighborhood under
an optional whole-domain half-scale law. With the stated exact iid access
premises, it gives a finite symbolic prospective raw cap with explicit
error, abstention, coverage and power guarantees. It supplies no numerical
cap, actual eligible occurrence or physical readout. This restricted
positive result leaves the arbitrary-scale fixed-budget limitation and
the original 40,000 / 400,000 / 38,825 diagnostic design unchanged.

## Intrinsic height under the all-layer half-scale baseline

[The height-growth theorem](HALF_SCALE_HEIGHT_GROWTH.md) proves almost-sure
linear intrinsic longest-chain height and cardinality exponent one for the
selected baseline, conditional on the admitted prefix, ratio-potential
construction and infinite classical history measure. Its optional
whole-layer half-scale prescription applies at every parent size from six
onward. Conditional-history bounds require no iid births and establish a
liminf height fraction of at least one half, without an exact limiting
speed. The classical kernel is separately defined even for zero PSD
payload. No coefficient-branch decision, physical dimension or validation,
or transfer to the separate optimizer or infinite harmonic perturbation
follows.

## Intrinsic target screen from native height

[The intrinsic target screen](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) gives
conditional finite-time deletion-distance bounds and an almost-sure liminf
deletion fraction of at least one half for fixed intrinsic target classes
with a common sublinear height envelope under the selected all-layer
half-scale baseline. Its dense bounded-aspect Ferrers example requires
both occupancy and aspect controls; balanced thin hooks disprove the
aspect-only premise. Unrestricted Ferrers defect and the separate optimizer
remain unresolved. The target and native law are optional choices; the
result supplies no physical readout, dimension or geometry bridge.

## Height drift as a necessary law-selection test

[The height-drift criterion](HEIGHT_DRIFT_LAW_SELECTION.md) identifies the
complete probability of a height-spanning precursor, including proper
ideals, and proves that its actual-history Cesaro average tracks normalized
height almost surely and in mean square for each admitted all-size law.
It distinguishes the almost-sure requirement from expectation, mean-absolute
and in-probability conclusions. The separate full-capacity, history-weighted
height objective and strict restoration give conditional admissibility;
they prove neither sublinear height nor target geometry. The finite proper-
ideal example is not an alternative all-size counterlaw, and the existing
Ferrers objective and its unresolved questions remain unchanged.

## Neutral-support feasibility at two finite boundaries

[Neutral-support feasibility](NEUTRAL_SUPPORT_FEASIBILITY.md) gives a
shared neutral-component row-saturation criterion and explicit zero
boundary minima at parent sizes two and three, separately for every admitted
strictly positive lower prefix of the required length. Complete marked
diamonds and component aliases are retained. Strictly positive next layers
have positive objectives with infimum zero, approached by restoration;
they do not attain the boundary minimum. The two zero witnesses cannot be
concatenated as positive lower prefixes. Larger sizes, recursive drift
decay, sublinear height and geometry remain unresolved; existing Ferrers
objectives and physical-readout limitations remain unchanged.

## An optional all-size law with sublinear intrinsic height

[The factorial-subset law](FACTORIAL_SUBSET_HEIGHT_LAW.md) constructs an
explicit admitted marked-order family from empty with
\(\limsup H_N/\sqrt N\le2\mathrm e\) almost surely. Per-subset factorial
weights induce the stated cardinality law; inclusions within a subset are
not independent. Induced-ideal maxima, all newborn bits and the entire PSD
carrier are covered by the complete diamond proof. The full height drift
includes proper raising ideals and need not decay uniformly over all rows.
This optional law resolves an all-size existence question; it neither
preserves an arbitrary fixed prefix nor derives a selector from DET.
Sublinear intrinsic height alone supplies no target approximation, geometry
or physical readout. Earlier finite-prefix and half-scale results keep
their original scopes.

## Ordering fraction of the fixed factorial-subset law

[The ordering-fraction theorem](ORDERING_FRACTION_OF_FACTORIAL_LAW.md)
proves that the fixed optional factorial-subset law's incomparable-pair
fraction tends to zero almost surely, while its sublinear-height bound
remains valid. Pair-density convergence does not imply eventual total order
or a chain containing almost all vertices. For a separately declared fixed
target class whose sufficiently large members have a fixed positive
incomparable-pair density, induced retained size is \(o(N)\) and the vertex-
deletion fraction tends to one almost surely. The extra density premise
is not established for the earlier Ferrers target. This is an intrinsic
conditional diagnostic, not a redesigned law or physical-geometry exclusion.

## Dense Ferrers incomparability and the fixed-law screen

[The dense Ferrers screen](DENSE_FERRERS_INCOMPARABILITY_SCREEN.md) proves
the density premise left conditional by the ordering-fraction theorem for
the existing target with fixed occupancy \(0<\nu\le1\) and aspect bound
\(1\le A<\infty\). Every target member of size at least
\(m_0=\lceil16A/\nu^2\rceil\) has incomparable-pair density at least
\(\epsilon=\nu^4/128\). For the fixed factorial-subset law, induced
retained fraction tends to zero and deletion fraction tends to one almost
surely. These are sufficient conditions and conservative constants; no necessity
or optimality claim is made. Balanced thin hooks are not density
counterexamples. The result does not extend to unrestricted Ferrers,
other laws, the separate optimizer or physical geometry.

## A factorial-power family with the same target obstruction

[The factorial-power family](FACTORIAL_POWER_LAW_FAMILY.md) constructs
an admitted optional from-empty law for each fixed integer \(q\ge1\).
Under each law, \(\limsup H_N/N^{1/(q+1)}\le\mathrm e(q+1)\) almost
surely, the incomparable fraction tends to zero, and induced deletion
fraction to each fixed dense occupancy/aspect Ferrers target tends to one.
At the two-vertex antichain, the invariant full-to-empty branch ratio
\(2^{-q}\) shows that changing the exponent changes the law, not just
its coordinates. These are changing
height upper bounds; distinct exact height-growth exponents are not proved.
There is no assertion uniform over growing exponents or all admitted laws,
and no unrestricted Ferrers, optimizer or physical-geometry conclusion.

## Quadratic subset penalty and nonvanishing incomparability

The [quadratic subset-penalty law screen](QUADRATIC_SUBSET_PENALTY_LAW_SCREEN.md)
constructs an explicit strictly positive optional law in the declared
scalar/passive marked-order model. Under the same from-empty probability
measure, eventually
\(H_N\le\lceil16e[\log_2(N+1)]^2\rceil\) almost surely and
\(\liminf_{N\to\infty}I(P_N)/\binom N2\ge1/4096\) almost surely.
The height conclusion is an upper bound; the incomparability conclusion is
a positive full-sequence lower limit, not a limiting density.

The law differs from every fixed-integer factorial-power law: at a
three-vertex antichain, the full-subset/empty-subset ratio is \(1/8\),
whereas the factorial-power ratio is \(6^{-q}\) for integer \(q\ge1\).
This establishes law dependence within the declared model. It does not
prove a target approximation, induced Ferrers embedding, arbitrary-prefix
preservation, physical interpretation or a universally forced DET law.

## Ferrers height and induced retention

The [Ferrers height and retention obstruction](FERRERS_HEIGHT_RETENTION_OBSTRUCTION.md)
concerns finite orders isomorphic to filled coordinatewise partition cell
diagrams, with empty included. If height \(H\) is maximum chain cardinality,
every such order \(Q\) obeys \(|Q|\le H(Q)(H(Q)+1)/2\), with staircase
equality cases. For any parent \(P\), its largest induced retained order
in this cell class has size
\(R_{\mathcal F}(P)\le\min\{|P|,H(P)(H(P)+1)/2\}\).
This ceiling is sharp in parent size and height; it need not be attained
for every parent. Induced restriction means restriction of the completed
order, not recomputed reachability after deleting generating-DAG vertices.

Applying the accepted height inputs gives
\(R_{\mathcal F}(P_N)=O(\log^4(N+1))\) for the quadratic law and
\(R_{\mathcal F}(P_N)=O(N^{2/(q+1)})\) for each separately fixed integer
factorial-power law \(q\ge2\), almost surely under each law's own measure.
For both cases, the deletion fraction to the unrestricted filled cell
class tends to one almost surely. At \(q=1\), this height-only argument
is inconclusive for unrestricted retention; the previous fixed dense-target
result remains valid. The target is unchanged. No conclusion for all
dimension-two orders, other meanings of Ferrers order or physical geometry
is supplied.

## Joint height and density obstruction to Ferrers retention

The [joint Ferrers obstruction](FERRERS_JOINT_HEIGHT_DENSITY_OBSTRUCTION.md)
proves a pathwise criterion for the unrestricted class of filled coordinatewise
partition cell orders, including empty. For \(N\)-vertex parents, maximum
chain cardinality \(H_N=O(\sqrt N)\), together with incomparable-pair count
\(I(P_N)=o(N^2)\), implies that the maximum induced retained fraction tends
to zero and the deletion fraction tends to one. Restriction is of the
completed order. When both premises hold almost surely under the same
measure, the conclusions do too.

The joint argument supplies the \(q=1\) case using the additional density
premise; height alone remains inconclusive there. Together with the prior
height-only cases, the deletion fraction tends to one almost surely for
each separately fixed integer factorial-power law \(q\ge1\), under that
law's own measure. No convergence rate follows from an unspecified
little-o premise. There is no growing-exponent or all-law conclusion,
target redesign, extension to all dimension-two orders or physical claim.

## Bernoulli-subset law and unrestricted Ferrers retention

The [Bernoulli-subset counterexample](BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md)
gives a completely admitted optional law in the declared scalar/passive
marked-order model for each fixed \(p\in(0,1)\). On the same from-empty
measure, \(\liminf H_N/N\ge p\),
\(\liminf R_{\mathcal F}(P_N)/N\ge p\) and
\(\limsup D_{\mathcal F}(P_N)/N\le1-p\), almost surely, for the unrestricted
filled coordinatewise Ferrers cell class. Also
\(\mathbb E_p I(P_N)\le N(1-p)/p^2\) and the incomparable-pair density
tends to zero almost surely on that measure.

The constructed greedy chain has \(L_N/N\to p\) almost surely; this is
not an exact longest-chain or optimal-retention limit. The retained chain
does not establish two-dimensional geometry. Each previously fixed dense
occupancy/aspect target still has deletion fraction tending to one almost surely.
The result demonstrates actual optional-law dependence within the declared
model, with no all-DET, physical or novelty claim and no uniform or adaptive
parameter assertion.
