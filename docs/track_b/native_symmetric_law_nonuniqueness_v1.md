# Symmetric law nonuniqueness: a finite family and conditional all-size continuation

This note consolidates accepted conditional results in one document. Part A supplies the admitted model and extension premise, retaining the theorem package's historical fixed instance and baseline B as context. Part B constructs the symmetric finite prefix. Part C varies its last finite layer. Part D begins an optional continuation at parent size four from each new family member, using that member's own smaller rows and whole-layer maxima. No historical parent-four/five witness, optimizer or baseline B coefficients are imported into that continuation.

The all-size conclusion relies on both the admitted maximal-deletion potential identity and the explicit extension-sufficiency premise; necessity-only parameterization would not suffice. The conclusions concern finite order events and classical growth-history cylinders, including unmarked history projections. They do not identify an unlabelled infinite endpoint or establish physical law selection, asymptotic geometry, efficient computation or execution permission.

Historical section and equation references in Part A refer to the [native theorem package](native_theorem_package_v1/THEOREM_PACKAGE.md). The finite qualifications in Parts B and C retain their original horizons; Part D states the additional premises used for continuation. All displayed scientific text below is retained from the accepted sources, with heading changes and declared source-reference substitutions.

## A. Admitted model and conditional extension premise

### 1. Mathematical object and admitted model

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

#### The fixed instance, not a uniquely selected law

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

### 9. All-size existence, prescribed optimization and finite verification

These are different claims.

**Conditional extension existence.** Given the model's admissible finite prefix and the ratio-potential theorem, choosing sufficiently small positive component scales at each subsequent finite layer and taking full complements yields compatible positive extensions. The common choice (5) is one prescription. Consistent finite-history probabilities define an infinite classical history measure. This does not prove a desired asymptotic geometry or a record-blind relative continuation of a particular harmonic seed.

## B. Accepted symmetric finite prefix

### 1. Whole histories and parent sufficiency

Let \(q_0\) be the printed structural prefix and
\(q_1(P,r,S)=q_0(P,1-r,S)\). Both retain fair newborn marks and scalar-passive payload. Declare
\[
 L_*(\gamma)=\tfrac12[L_0(\gamma)+L_1(\gamma)].
\]
The component is fixed for the entire history in this mathematical decomposition. No physical hidden sector, memory register or Boundary agency is proposed.

For a marked parent \((P,r)\) of size \(n\), write \(w_s(P,r)\) for the product of structural factors along any natural history producing it under component \(s\). This is well-defined: any two natural labelings are related by adjacent exchanges of incomparable births, each complete marked diamond preserves the product, and equivariance transports the marked endpoint. Thus
\[
 L_s(\gamma)=2^{-n}w_s(P,r).
\]
This argument applies through size four using only the admitted prefix. If the marked parent is treated as an isomorphism class, its number of distinct natural encodings multiplies both component weights equally. That multiplicity cancels in the ratio; it is neither omitted from endpoint probabilities nor counted twice.

The posterior component weight after any such history is therefore
\[
 \omega(P,r)=\frac{w_0(P,r)}{w_0(P,r)+w_1(P,r)}.
\]
It depends only on the original marked parent. The induced kernel is
\[
 q_*(P,r,S)=\omega q_0(P,r,S)+(1-\omega)q_1(P,r,S),
 \qquad \mathcal B^*_{S,b}(X)=\tfrac12 q_*(P,r,S)X.
\]
The next bit remains independently fair. In general \(\omega\ne1/2\); multiplying fresh arithmetic row averages is a different history law.

Set \(M(P,r)=(w_0+w_1)/2\), with \(M(\varnothing)=1\). For a birth with mark \(b\),
\[
 q_*(P,r,S)=\frac{M(P+S,r+b)}{M(P,r)}.
\]
This is the same parent formula, not an endpoint oracle. Its product telescopes to \(M\), so the resulting history weight is exactly \(L_*\).

### 2. Normalization, diamonds and the locality check

Positive component weights give positivity and complete ideal support. Each row sums to one; its complete passive payload map is identity. Relabeling equivariance follows from that of the component potentials and kernels.

For two incomparable births from \(C\) to a common transported marked terminal parent \(D\), both complete two-step branch products are
\[
 \frac14\frac{M(D)}{M(C)}\,\operatorname{id}.
\]
Hence the full unnormalized marked diamonds hold for every old marking, both newborn bits and equal precursors, not merely scalar endpoint totals.

That argument alone does not prove restricted proper-slot mark locality. Here it can be checked exhaustively at every allowed parent size. Use
\[
 a=2/3,\ c=1/5,\ d=1/4,\ g=1/10,\ k=11/20,\ e=1/44,
\]
\[
 f_0=1/6,\ f_1=1/3,\qquad h_0=19/30,\ h_1=7/15.
\]
At sizes zero, one and two the component structural path weights coincide: respectively \(1,1\), and \(a\) or \(1-a\). Thus \(\omega=1/2\). The singleton and two-antichain rows stay unchanged; the two-chain row becomes
\[
 (c,\bar f,\bar h)=(1/5,1/4,11/20).
\]
These rows are mark-independent.

All five size-three shapes have the following per-encoding structural weights. Here \(i\) is the fork root or chain minimum mark.

| Parent | \(w_0,w_1\) | Posterior \(\omega\) |
| --- | --- | --- |
| Antichain | \(1/6,1/6\) | \(1/2\) |
| Edge plus isolate | \(1/15,1/15\) | \(1/2\) |
| Fork | \(f_i/3,f_{1-i}/3\) | \(1/3\) if \(i=0\); \(2/3\) if \(i=1\) |
| Join | \(11/30,11/30\) | \(1/2\) |
| Chain | \(h_i/3,h_{1-i}/3\) | \(19/33\) if \(i=0\); \(14/33\) if \(i=1\) |

The edge has three distinct natural encodings, each with weight \(1/15\) in both components. Leaf, upper-chain and isolate marks do not change the displayed weights. This accounts for every role-mark assignment, including all inherited marking choices.

Substitution gives every induced proper slot and its full complement:

| Parent | Proper-slot values under \(q_*\) | Full slot |
| --- | --- | --- |
| Antichain | Empty \(e\); each singleton \(1/110\); each pair \(1/20\) | \(4/5\) |
| Edge \(u<v\), isolate \(w\) | Empty and \(\{w\}\): \(e\); \(\{u\}:5/176\); \(\{u,v\}:11/176\); \(\{u,w\}:11/88\) | \(65/88\) |
| Fork | Empty and root: \(e\); each root-plus-leaf: \(1/20\) | \(47/55\) |
| Join | Empty, each root singleton and root pair: \(e\) | \(10/11\) |
| Chain | Empty, root and initial pair: \(e\) | \(41/44\) |

For the fork's potentially delicate proper slot,
\[
 \omega e\frac{h_i}{f_i}+(1-\omega)e\frac{h_{1-i}}{f_{1-i}}
 =e\frac{h_0+h_1}{f_0+f_1}
 =\frac1{20}.
\]
For its empty/root slots the two components both equal \(e\), so even the posterior's root dependence cancels. On the chain all proper entries equal \(e\) in both components; its nonuniform posterior also cancels. On the edge, equal posterior weights average the root-dependent \(f_i,h_i\), and all other entries were already mark-independent. Antichain and join rows are identical between components.

Every displayed induced slot is consequently independent of every mark, which is stronger than the required locality. The complete complements are positive. This exhausts parents zero through three; no closure claim about later layers or arbitrary mixtures is made.

### 3. Naive row averaging: an exact failure

Define \(q_{\rm avg}=(q_0+q_1)/2\). It is positive, normalized, equivariant and mark-independent on these rows, but those facts do not imply diamonds.

Take the two-chain \(u<v\), both marked zero, and two new zero-marked incomparable births with precursors
\(S=\{u\}\), \(T=\{u,v\}\). Neither precursor includes the other newborn. Appending \(S\) first gives a fork; appending \(T\) first gives a three-chain. Both routes are on the complete support and give the same transported marked terminal order.

At the base,
\[
 q_{\rm avg}(S)=\bar f=1/4,\qquad
 q_{\rm avg}(T)=\bar h=11/20.
\]
The fork's \(T\) slot is
\[
 \frac e2\left(\frac{h_0}{f_0}+\frac{h_1}{f_1}\right)
 =\frac e2(19/5+7/5)=13e/5;
\]
the three-chain's \(S\) slot is \(e\). Including both fair newborn factors, the complete maps are
\[
 \frac14\frac14\frac{13e}{5}\operatorname{id}
 =\frac{13}{3520}\operatorname{id},
 \qquad
 \frac14\frac{11}{20}e\operatorname{id}
 =\frac{11}{3520}\operatorname{id}.
\]
Their difference is \((1/1760)\operatorname{id}\), so \(q_{\rm avg}\) is rejected. It agrees with \(q_*\) through parent size two; therefore diamonds ending by three births hold, and this failure first appears at four births.

Averaging seeds before reconstructing the printed structural relations is different. With \(\bar f=1/4,\bar h=11/20\), the fork relation gives
\(e\bar h/\bar f=11e/5=1/20\), not \(13e/5\). Through these printed rows, that reconstructed prefix agrees with \(q_*\); both diamond routes then give \(11/3520\). This does not authorize reconstruction at a later layer.

### 4. Symmetry, height and the remaining selection premise

Let \(F\) flip every mark in a complete history. Whole-law transport gives
\(L_1(\gamma)=L_0(F\gamma)\), hence
\[
 L_*(F\gamma)=L_*(\gamma).
\]
For any unmarked order event, \(F\) is a probability-sum bijection leaving the event unchanged. Its probabilities under \(L_0,L_1,L_*\) are therefore equal. This uses no assumed independence between marks and geometry. In particular, the four height tails remain
\[
 1,\quad263/264,\quad1997/2640,\quad41/240.
\]
These are the original fair results, not the fixed-\(q\) biased-mark family of QR-LD006.

The equal-mixture convention enforces global mark-name symmetry within this chosen two-component construction. It changes marked-history probabilities: for example, a specified marked three-fork with root zero has structural weights \(1/18\) and \(1/9\) in the two components, averaged to \(1/12\). Thus the components differ. Within their weighted segment, flip invariance forces equal weights; this is not uniqueness among all admissible structural laws.

The finite boundary is explicit: whole-process symmetrization is feasible on this prefix; arithmetic averaging of its completed rows is not. Symmetry remains an additional proposed mathematical principle. The next unresolved selection question is whether an independently justified DET premise favors this convention over the original marked law. Physical preparation, record interpretation and calibrated readout remain separate missing premises. No metric, gravity, detector, GWOSC, performance or Boundary claim follows. The original fair results and CE advantage closure remain intact.

## C. Finite symmetric-law nonuniqueness

### 1. Definition and exact support interval

Use the admitted model in Part A and the accepted \(q_*\) rows in Part B. A state has finite order \(P\), immutable binary marks \(r\), and scalar-passive payload \(\mathfrak D\). An ideal \(S\) is the strict past of one appended maximal vertex. Each newborn bit is independently fair; the complete branch map is
\[
 \mathcal B^{P,r}_{S,b}(X)=q_\lambda(P,r,S)X/2.
\]
All parent-zero-through-two rows remain those of \(q_*\). For \(|P|=3\), define
\[
 q_\lambda(P,r,S)=\lambda q_*(P,r,S)\quad(S\subsetneq P),
 \qquad q_\lambda(P,r,P)=1-\lambda
       \sum_{S\subsetneq P}q_*(P,r,S).
\]
This defines distinct candidate laws; it does not silently replace the accepted law. No parent-four transition is defined.

For completeness, every proper occurrence and complement is retained below. Equal entries in a row still count as separate ideals.

| Three-vertex parent | Proper entries before scaling | Proper sum | Full slot after scaling | Upper bound |
|---|---|---|---|---|
| Antichain | Empty \(1/44\); three singletons \(1/110\); three pairs \(1/20\) | \(1/5\) | \(1-\lambda/5\) | \(5\) |
| Edge \(u<v\), isolate \(w\) | Empty and \(\{w\}\): \(1/44\); \(\{u\}\): \(5/176\); \(\{u,v\}\): \(11/176\); \(\{u,w\}\): \(11/88\) | \(23/88\) | \(1-23\lambda/88\) | \(88/23\) |
| Fork | Empty and root: \(1/44\); two root-plus-leaf ideals \(1/20\) | \(8/55\) | \(1-8\lambda/55\) | \(55/8\) |
| Join | Empty, two root singletons and root pair: \(1/44\) each | \(1/11\) | \(1-\lambda/11\) | \(11\) |
| Chain | Empty, root and initial pair: \(1/44\) each | \(3/44\) | \(1-3\lambda/44\) | \(44/3\) |

For example, the edge sum is
\((8+5+11+22)/176=23/88\); the fork sum is
\(1/22+1/10=8/55\). The antichain sum is
\(1/44+3/110+3/20=1/5\).

Every proper slot is positive precisely when \(\lambda>0\). All five full slots are positive precisely when \(\lambda\) is smaller than every listed upper bound. The smallest is \(88/23\), proving the exact interval. At zero the proper support disappears; at \(88/23\) the edge's full slot vanishes. Neither endpoint is admitted. Beyond the upper endpoint that full entry is negative. The earlier unchanged rows are positive.

### 2. All finite marked diamonds

Take any complete incomparable-birth diamond with base \(C\), ideals \(S,T\subseteq C\), inherited marking \(r\), and newborn bits \(b,c\). The second precursor excludes the other newborn, as required by the admitted model.

If the terminal size is at most three, both parent rows have size at most two. Neither changes, so the accepted complete \(q_*\) diamond holds unchanged.

If the terminal size is four, \(|C|=2\). The first factors use unchanged parent-two rows. In either intermediate parent, the second precursor is a proper ideal: \(T\) excludes the vertex appended with precursor \(S\), and conversely. Hence
\[
 q_\lambda(C,r,S)q_\lambda(C+S,r+b,T)
 =\lambda q_*(C,r,S)q_*(C+S,r+b,T),
\]
\[
 q_\lambda(C,r,T)q_\lambda(C+T,r+c,S)
 =\lambda q_*(C,r,T)q_*(C+T,r+c,S).
\]
The accepted \(q_*\) identity makes these equal. Both complete payload maps also carry the identical fair factor \(1/4\), with the same transported terminal order, marks and payload.

This argument quantifies over every allowed pair, not selected examples. It includes \(S=T\), even \(S=T=C\): each second precursor is still proper because it omits the first newborn. It includes empty precursors, all inherited marks, and all four newborn-bit choices. Mark independence precludes an omitted mark case; equivariant transport identifies the two terminal encodings.

A parent-three full slot cannot be the second transition of such an incomparable diamond, because it contains the other newborn. Its modified value therefore imposes no missing top-layer diamond equation at this horizon. This is a finite boundary observation, not permission to disregard later constraints. No fifth-birth extension or later locality closure is inferred.

### 3. Remaining obligations and symmetry

Every \(q_*\) prefix row is mark-independent. Multiplication by a common constant and taking full complements preserve this property, which is stronger than proper-slot mark locality. The probabilities may still read the unmarked parent as the admitted model permits.

Ideal inclusion, properness and the table's order roles are invariant under relabeling. A common \(\lambda\) therefore preserves equivariance, including transport of individual ideal occurrences. Positivity and normalization were proved above. For every payload \(X\),
\[
 \sum_{S,b}\mathcal B^{P,r}_{S,b}(X)
   =\sum_S q_\lambda(P,r,S)X=X.
\]
The complete unnormalized branch maps are scalar positive multiples of identity; the result holds for arbitrary admitted payloads and retained references, without diagonal or postselection restrictions.

For any natural four-birth history, its probability is its structural product times \(2^{-4}\). Flipping all marks leaves every structural factor and the fair-bit weight unchanged. The whole history law is consequently globally mark-symmetric. No independent hidden component or physical interpretation is added.

### 4. An intrinsic unmarked difference

Choose the exact interior parameters \(\lambda=1\) and \(\lambda=2\). A four-vertex total order can arise only by taking the full ideal at every nonempty parent. Its three-birth prefix probability is
\[
 (1/3)(11/20)=11/60.
\]
The factors are the singleton full slot and the two-chain full slot; both are unchanged. The final full slot is \(1-3\lambda/44\), so
\[
 \Pr_\lambda(H_4=4)
 =\frac{11}{60}\left(1-\frac{3\lambda}{44}\right)
 =\frac{11}{60}-\frac{\lambda}{80}.
\]
Thus
\[
 \Pr_1(H_4=4)=41/240,\qquad
 \Pr_2(H_4=4)=19/120,\qquad
 \Pr_1-\Pr_2=1/80.
\]
The complementary probabilities are respectively \(199/240\) and \(101/120\). No complementary outcome is discarded or renormalized.

There is exactly one natural order encoding of a chain: its birth labels must follow its total order. Each of its sixteen mark assignments has fair weight \(1/16\) times the structural product; summing all sixteen restores the displayed unmarked probability. No \(4!\), extra automorphism divisor, or conditioning on a chain prefix belongs in this unconditional endpoint probability. Other shapes retain their own encoding multiplicities in the normalized full law.

The event is intrinsic to the unmarked endpoint. Renaming mark symbols leaves it unchanged; relabeling natural encodings is a probability-sum bijection. Neither can eliminate this difference between laws.

QR-LD007 proved equal weighting unique only inside the segment joining the original law and its mark-flipped transport. Every law in that segment has the same unmarked probabilities. The \(\lambda=2\) law lies outside it, as the chain event shows. There is no contradiction: segment uniqueness is weaker than uniqueness among admissible mark-symmetric laws.

### 5. Scope and unresolved selection

This is a construction-family nonuniqueness result conditional on the accepted finite prefix. It neither classifies all admissible laws nor identifies a DET principle selecting \(\lambda\). The scalar-passive payload supplies no new quantum dynamics. Physical preparation, record/readout correspondence, metric reconstruction and law selection remain unresolved.

Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause and speculative Boundary separation remain unchanged. No physical, gravity, GWOSC, detector, agency or performance evidence is claimed.

## D. Conditional all-size continuation

### 1. Premise and recursive definition

Part C gives the accepted positive, normalized, equivariant, mark-independent prefix \(q_\lambda\) on parents of sizes zero through three, with complete marked diamonds through four births. Part B supplies its underlying \(q_*\) rows.

The load-bearing premise is Part A: the maximal-deletion potential satisfies all inherited ratio equations; next-layer proper probabilities are parameterized by component scales; sufficiently small positive scales with full normalization complements give compatible extensions, including the common prescription below. The necessity phrase “every positive solution has the form” alone would not prove sufficiency. We use the stated potential property and the explicit conditional-extension paragraph together. Their underlying theorem is admitted, not re-proved here.

Fix \(\lambda\) once. Suppose all rows below size \(n\), \(n\ge4\), are already defined. For a proper ideal \(S\) of an \(n\)-vertex parent \(P\), set
\[
 K(P,S)=\operatorname{Max}(P)\setminus S,\qquad
 u_\lambda(P,r,S)=
 \prod_{\varnothing\ne A\subseteq K(P,S)}
 q_\lambda(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}}.
\]
Define
\[
 U_n(P,r)=\sum_{S\subsetneq P}u_\lambda(P,r,S),\qquad
 M_n(\lambda)=\max_{|P|=n,\ r}U_n(P,r),
 \qquad a_n(\lambda)=\frac1{2(1+M_n(\lambda))},
\]
\[
 q_\lambda(P,r,S)=a_n(\lambda)u_\lambda(P,r,S)\ (S\subsetneq P),
 \qquad q_\lambda(P,r,P)=1-a_n(\lambda)U_n(P,r).
\]
The sum includes every proper ideal occurrence. The maximum covers the entire admitted marked layer, represented on a fixed \(n\)-element label set; it is not a selected-support maximum. All smaller rows and maxima are those of this same \(\lambda\)-law.

### 2. Well-definedness and positivity

A proper ideal of a finite nonempty order omits a maximal element: extend any omitted element upward to a maximal one; if that maximum were in the ideal, downward closure would include the omitted element. Thus \(K(P,S)\ne\varnothing\).

Deleting a nonempty subset of omitted maximal elements leaves a smaller order containing \(S\) as an ideal. Every factor is therefore an already defined, strictly positive finite number. Reciprocal factors are well-defined, and the finite product is positive and finite. A smaller-parent occurrence of \(S\) can be full; its actual normalization complement, with its full induced marking, must be used. It is not replaced by a proper-slot formula or discarded.

There are finitely many orders on a fixed finite label set, finitely many binary markings, and finitely many ideals in each. Hence every \(U_n\) and the whole-layer maximum \(M_n\) are finite and positive. This is a finiteness proof, not layer enumeration or an efficiency bound.

Consequently \(a_n>0\), every proper probability is positive, and
\[
 0<a_nU_n(P,r)\le\frac{M_n}{2(1+M_n)}<\frac12.
\]
Every full complement is strictly greater than \(1/2\) and less than one. The complete row sums to one. No limit in \(n\), uniform lower bound on individual proper entries, or uniform-in-\(\lambda\) estimate is needed.

### 3. Inductive compatibility, locality and transport

Assign the same \(a_n\) to every component at layer \(n\). This is permitted by the admitted construction: the potential already solves the inherited homogeneous ratio equations, and multiplying both unknown sides by one common scale preserves them. Distinct components need not be assigned distinct values. The complete normalization bound above supplies the required positive complements.

More explicitly, consider any new diamond with base \(C\) of size \(n-1\), ideals \(S,T\subseteq C\), inherited marking \(r\), and newborn bits \(b,c\). Each second precursor excludes the other newborn, so is proper in its intermediate \(n\)-vertex parent. The admitted potential identity is
\[
 q_\lambda(C,r,S)u_\lambda(C+S,r+b,T)
 =
 q_\lambda(C,r,T)u_\lambda(C+T,r+c,S).
\]
Multiplication by \(a_n\) proves the required structural diamond. Multiplication by the fair-bit factor \(1/4\) proves equality of the complete unnormalized payload maps after terminal transport.

The premise covers all inherited markings, all four newborn-bit choices and equal precursors, including \(S=T=C\); both second precursors still omit the other newborn. Empty and full base ideals are included. Older diamonds are unchanged. New full slots cannot be second precursors of these incomparable diamonds, but they enter later smaller-parent evaluations; no later constraint is waived.

For locality, use the stronger inductive fact that every smaller row is mark-independent, including its full slot. Every factor in \(u_\lambda\) is then mark-independent, so \(u_\lambda\), \(U_n\), the common scale and both proper and full new entries are mark-independent. This implies the required restricted proper-slot mark locality. No convex-mixture locality argument is used.

A relabeling maps maximal elements, deletion subsets and ideal occurrences bijectively, carrying the induced marks with them. Equivariance of all smaller rows therefore implies equivariance of \(u_\lambda\) and \(U_n\). The whole-layer maximum and common scale are unchanged by that transport. Thus the complete new row is equivariant.

These arguments, with the accepted prefix as base case, complete the induction for every finite \(n\). The all-size conclusion relies on the admitted compatibility theorem; it is not inferred merely from finite admission.

### 4. History probabilities, payload and symmetry

For a legal marked natural history \(\gamma_m\) of \(m\) births, define
\[
 p_\lambda(\gamma_m)
   =2^{-m}\prod_{j=0}^{m-1}q_\lambda(P_j,r_j,S_j).
\]
At each parent there are finitely many ideal/bit choices, all allowed choices have positive probability, and their complete sum is one. Therefore summing over all one-step extensions returns \(p_\lambda(\gamma_m)\). Iterating gives consistent normalized finite-history distributions.

The usual probability extension on a finitely branching discrete history tree yields an infinite classical history measure with these cylinder probabilities. No transition at an infinite parent is required: each individual step has a finite parent. This measure is on growth histories; no measure on an unlabelled infinite-order quotient or asymptotic geometry is asserted.

The payload branch remains \(\mathcal B_{S,b}(X)=q_\lambda(P,r,S)X/2\). Summing over all ideals and both bits gives \(X\), and the diamonds hold as linear maps on arbitrary admitted payloads, also with retained references. If \(X=0\), every branch payload is zero, while the declared classical kernel still defines the history probabilities. No division by a zero trace is used, and no new quantum dynamics is derived.

At every finite horizon the structural product is independent of all marks, and every mark string has its fair factor \(2^{-m}\). Global mark flipping preserves each corresponding cylinder weight. It follows that the infinite measure is invariant under global mark flipping on its cylinder-generated sigma-algebra. This proves symmetry for this recursively constructed law, not a claim about arbitrary mixtures.

### 5. The finite witness survives

Let \(E\) be the cylinder event that the first four births form a total order, with all marks forgotten. Its finite prefix is exactly the accepted QR-LD010 prefix. Every later continuation sums to one, so
\[
 \Pr_\lambda(E)=\frac{11}{60}-\frac{\lambda}{80}
\]
under the infinite history measure as well. The single natural order encoding of the four-chain and all sixteen fair mark assignments remain included. Complementary histories retain their mass.

For the two interior parameters,
\[
 \Pr_1(E)=41/240,\qquad \Pr_2(E)=19/120,\qquad
 \Pr_1(E)-\Pr_2(E)=1/80.
\]
Their complements remain \(199/240\) and \(101/120\). Thus the two all-size laws, and their unmarked history projections, differ. This is not removable by mark renaming or transport of finite natural encodings. It does not imply mutual singularity or distinguishability from an unlabelled infinite endpoint alone.

The finite nonuniqueness is consequently not forced to disappear when extension is required: this admitted construction supplies all-size witnesses. Selecting \(\lambda\), the continuation prescription, or a physical law still requires additional justification. No universal classification, asymptotic speed, dimension, metric, gravity, native forward map, efficient computation, detector or empirical selection follows.

Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause and speculative Boundary separation remain.

## E. Backward determination of compatible kernels

Part E adds the accepted conditional backward-determination theorem. Within the admitted model, a complete later conditional transition layer uniquely determines every earlier layer among compatible laws. Applied to the two laws in Part D, it rules out an identical complete later layer or an exactly common complete kernel tail after finite burn-in.

The backward implication uses positivity, normalization, complete marked diamonds and the shared transported dictionary. Existence of the particular all-size pair still relies on Part D’s admitted potential identity and extension sufficiency. The finite horizons in Parts B and C retain their stated scope. This result supplies no observational access, robustness bound, physical memory or retrocausation, and no existence claim for arbitrary proposed later tables.

### 1. Model and meaning of the supplied layer

Part A fixes finite orders \(C\), immutable binary marks \(r\), every ideal as an eligible precursor, strictly positive probabilities, normalized complete ideal rows, fair newborn bits, relabeling equivariance, and complete unnormalized marked diamonds. A birth adds one maximal vertex with the chosen ideal as its strict past. The payload branch is \(q(C,r,S)X/2\).

Let \(Q\) be the known size-\(n+1\) layer of an admitted law. It gives \(q(P,r_P,U)\) for **every** marked parent \(P\) of that size and every individual ideal \(U\), in a common transported dictionary. It is not a distribution of which parents occur, an orbit-aggregated transition count, or an average over markings. Each ideal occurrence remains separate in normalization.

The backward theorem needs the model's positivity, normalization, complete diamonds and transport. It does not require mark independence, global mark symmetry, or the deletion-potential extension theorem. That latter premise is needed for the existence of the particular all-size pair to which we apply it.

### 2. Domain and complete diamond

Fix any marked size-\(n\) parent \((C,r)\), ideals \(S,T\subseteq C\), and bits \(b,c\). Introduce fresh vertices \(x,y\). Write \(C_S^x\) for \(C\) with \(x\) appended above exactly \(S\), marked \(b\); write \(C_T^y\) analogously with \(y\), marked \(c\).

After adding \(x\), the old ideal \(T\) remains an ideal when \(x\) is excluded. A new maximal vertex cannot become a predecessor of an old element. The same holds for \(S\) after adding \(y\). Both second precursors are proper because they omit the first newborn. Both routes therefore exist on the complete support.

Their common terminal order retains \(C\), gives \(x\) past \(S\) and \(y\) past \(T\), and leaves \(x,y\) incomparable. Old marks remain fixed; marks \(b,c\) stay attached to \(x,y\). If natural birth labels are used, the route comparison transports those labels while preserving these vertices' order roles and marks. Equivariance lets either intermediate parent be queried in the supplied representative dictionary.

The complete maps on the two routes have scalar coefficients
\[
 \frac14q(C,r,S)Q(C_S^x,r_x,T),\qquad
 \frac14q(C,r,T)Q(C_T^y,r_y,S).
\]
The matching fair-bit factors cancel. The admitted diamond consequently gives
\[
 \boxed{\frac{q(C,r,S)}{q(C,r,T)}
 =\frac{Q(C_T^y,r_y,S)}{Q(C_S^x,r_x,T)}}. \tag{1}
\]
All divisions are legal: both earlier probabilities and every queried later entry are strictly positive.

This holds for all old markings and all four newborn-bit choices. It includes empty and full base ideals. Even when \(S=C\) or \(T=C\), the second precursor is proper in the enlarged parent. When \(S=T\), including \(S=T=C\), the ratio equals one; the equal-precursor diamond supplies that equality even for different newborn bits. Nothing identifies distinct marked parents without the required transport.

### 3. Explicit row recovery

Choose the reference \(T=\varnothing\) and any fixed bits \(b,c\), for example both zero. For every ideal \(S\) of \(C\), form from the known layer
\[
 R_{C,r}(S)=
 \frac{Q(C_\varnothing^y,r_y,S)}
      {Q(C_S^x,r_x,\varnothing)},\qquad
 Z_{C,r}=\sum_{I\in\operatorname{Id}(C)}R_{C,r}(I).
\]
These are finite positive numbers. Equation (1) implies
\(R_{C,r}(S)=q(C,r,S)/q(C,r,\varnothing)\), so
\(R_{C,r}(\varnothing)=1\), independently of the chosen bits. Complete row normalization gives
\[
 1=q(C,r,\varnothing)Z_{C,r},\qquad
 \boxed{q(C,r,S)=\frac{R_{C,r}(S)}{Z_{C,r}}}. \tag{2}
\]
Thus the whole earlier row, including its full slot, is determined. The sum counts all actual ideals, including equal-valued or symmetry-related occurrences. For \(n=0\), the only ideal is empty/full; (2) returns its required probability one.

Positivity prevents missing reference transitions and zero denominators. Normalization fixes the otherwise undetermined row scale. The shared state/support dictionary and equivariance make the later queries comparable; matching fair-mark factors give precisely (1). The proof uses the declared classical scalar identity, not division by a payload trace. A zero payload does not erase the separately specified classical kernel.

Equation (2) proves uniqueness **among admitted compatible predecessors**. It does not assert that an arbitrary positive later table has an admitted predecessor. For a table without the stipulated compatibility, ratios from different bit choices or reference ideals need not agree. Here existence is part of the admitted-law premise.

### 4. Iteration and the accepted pair

If two admitted laws agree on the whole size-\(N\) transition layer, their \(R\) and \(Z\) values for every size-\(N-1\) marked parent agree. Equation (2) gives equality of that earlier layer. Repeating recovers equality through size zero. This is a backward implication; identical earlier layers do not imply identical later ones.

Part C establishes the finite \(\lambda\)-family. Part D establishes its accepted conditional all-size continuations. The \(\lambda=1,2\) laws share parent layers zero, one and two. At a three-chain parent, for any inherited marking, their empty-ideal probabilities are already
\[
 q_1(C_3,r,\varnothing)=1/44,\qquad
 q_2(C_3,r,\varnothing)=1/22.
\]
They therefore differ at layer three.

If any complete layer \(N\ge3\) were identical, either it would be this already different layer or backward determination would force layer three to be identical. Both are contradictions. Hence, for every such \(N\), some parent/ideal entry differs. This need not be the same order shape or slot at every size.

An exactly common tail after a finite parent-size cutoff would contain an identical layer with \(N\ge3\), which is impossible. Shared layers zero through two are consistent with the theorem: those earlier layers have multiple admissible forward continuations. The all-size application retains Part D's admitted ratio-potential and extension-sufficiency assumptions; it does not re-prove them.

### 5. Limits of the conclusion

The input is a complete conditional transition rule on all marked parents. Restricted records, sampled paths, averaged kernels and a few cylinder probabilities do not supply that input. No marginal parent probability is substituted for a conditional entry anywhere in the proof. The previously accepted four-birth cylinder difference \(1/80\) remains a separate history-law result.

The conclusion is exact nonidentity at each complete later layer. It supplies no quantitative lower separation bound, asymptotic nonconvergence, uniform statistical identifiability, or finite-sample guarantee. It does not say all coarse observations differ, or all agree. It establishes no property of unlabelled infinite endpoints, mutual singularity, physical memory or retrocausation. Backward mathematical determination is a constraint between compatible rules, not a process acting on earlier events.

Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause and speculative Boundary separation remain.

## F. Exact backward reconstruction: local continuity without uniform stability

Part F records the accepted conditional stability limits of the backward reconstruction in Part E. Here “inverse” means recovery of the unique compatible earlier rule, not selection of a unique forward continuation. The reconstruction F is generally many-to-one: several later tables can have the same earlier compatible rule. The new family below keeps the finite prefixes fixed while varying their continuations; Part D’s previously fixed pair remains unchanged. Construction and all-size existence continue to require both Part A’s admitted potential identity and explicit extension sufficiency.

Complete positive parent-four tables can be arbitrarily close in maximum entry difference while their uniquely determined parent-three kernels retain a fixed nonzero gap. Thus the accepted exact inverse has no uniform modulus of continuity over the admitted positive-law class. It remains locally continuous at each fixed strictly positive compatible table.

The counterexample uses a **new family of continuations** of the fixed \(\lambda=1,2\) finite prefixes. It does not alter the previously fixed Part D pair or describe that pair's large-size behavior.

### 1. Dictionary, metric and new family

For each parent size \(n\), use the shared dictionary of orders on a fixed \(n\)-element label set, all binary markings and every individual ideal. Equivariance handles other representative labels. Define
\[
 d_n(K,L)=\max_{\substack{|P|=n,\ r\\S\in\operatorname{Id}(P)}}
       |K(P,r,S)-L(P,r,S)|.
\]
These are structural probabilities, before the common fair newborn-bit factor. The finite maximum includes full slots, all markings, and all ideal occurrences.

Let \(p_1,p_2\) be exactly the accepted \(\lambda=1,2\) rows on parent sizes zero through three. They stay fixed throughout. At a three-chain parent,
\[
 |p_1(C_3,r,\varnothing)-p_2(C_3,r,\varnothing)|
 =|1/44-1/22|=1/44,
\]
so \(d_3(p_1,p_2)\ge1/44\).

For each size-four parent and proper ideal, compute from that prefix alone
\[
 u_i(P,r,S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P)\setminus S}
 p_i(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}},
 \quad
 U_i(P,r)=\sum_{S\subsetneq P}u_i(P,r,S).
\]
Use each actual smaller full slot whenever deletion makes \(S\) full. All factors have size at most three and are prescribed, positive and finite.

Set
\[
 M=\max_{i\in\{1,2\},\,|P|=4,\,r}U_i(P,r),\qquad
 a(t)=\frac{t}{2(1+M)},\quad 0<t<1.
\]
The maximum covers both laws and the entire marked layer. A proper ideal omits a maximal element, so each deletion product is defined. Finite orders, markings and ideal sets give \(0<M<\infty\), without enumeration.

The new parent-four tables are
\[
 Q_i^t(P,r,S)=a(t)u_i(P,r,S)\quad(S\subsetneq P),\qquad
 Q_i^t(P,r,P)=1-a(t)U_i(P,r).
 \tag{1}
\]
Their common scale depends on neither the parent nor its marks. The potentials and \(M\) are fixed as \(t\) varies.

### 2. Admission and all-size continuation

Every proper entry is positive. Every full entry satisfies
\[
 1-a(t)U_i(P,r)\ge1-\frac{tM}{2(1+M)}
 >1-\frac t2>\frac12,
\]
and each complete row sums to one.

Admission uses both the admitted potential identity and the explicit extension-sufficiency premise in Part A. The necessity-only component parameterization would not suffice. For each law separately, the potential solves every inherited marked ratio equation; giving all components the common positive scale \(a(t)\) multiplies both sides of each new diamond by the same factor. The scale is no larger than that law's own admitted half-scale prescription, and the full complements are positive.

This includes all old markings, both newborn bits, equal precursors and empty/full base ideals. Both second precursors omit the other newborn and are proper. Fair factors \(1/4\) and terminal transport are retained. Earlier diamonds are unchanged. The fixed prefixes are mark-independent, so the potentials and new complements are mark-independent, establishing locality directly. Equivariance follows from deletion and ideal transport. Complete scalar payload sums remain identity.

For each fixed \(i,t\), the resulting prefix can be continued from parent size five using its **own** smaller-row potentials and whole-layer maxima, with scale \(1/[2(1+M_n^{i,t})]\) and full complements. The accepted conditional induction applies at every subsequent finite size; normalized finite histories give an infinite classical history measure. This uses no historical \(B\), parent-four/five witness or optimizer coefficient. No joint limit in size and \(t\) is asserted.

### 3. Uniform closeness of complete later rows

For every matched proper entry, positivity gives
\[
 |u_1-u_2|\le\max(u_1,u_2)\le M,
 \qquad |Q_1^t-Q_2^t|\le a(t)M.
\]
For the full entry, both proper sums lie in \((0,M]\), hence
\[
 |Q_1^t(P,r,P)-Q_2^t(P,r,P)|
   =a(t)|U_1-U_2|\le a(t)M.
\]
Consequently the **entire** layer obeys
\[
 d_4(Q_1^t,Q_2^t)\le\frac{tM}{2(1+M)}<\frac t2
 \longrightarrow0. \tag{2}
\]

There is also a complete-row total-variation bound. At a fixed marked parent, write \(\Delta u_S=u_1(P,r,S)-u_2(P,r,S)\). Including its full slot,
\[
 \operatorname{TV}(Q_1^t,Q_2^t)
 =\frac{a(t)}2\left(\sum_{S\subsetneq P}|\Delta u_S|
                         +|U_1-U_2|\right)
 \le a(t)\max(U_1,U_2)\le a(t)M.
\]
The inequality uses \(\sum|\Delta u_S|\le U_1+U_2\). It holds uniformly over all parents and markings. For the joint ideal/bit distribution \(Q_i^t(S)/2\), summing both fair bits gives the same total variation. No ideal or bit outcome is omitted.

### 4. Failure of a uniform inverse modulus

Let \(F\) be the accepted reconstruction map from a compatible complete parent-four table to its parent-three layer. Exact backward determination gives
\[
 F(Q_i^t)=p_i|_{|P|=3},
 \qquad d_3(F(Q_1^t),F(Q_2^t))\ge1/44
 \quad\text{for every }t>0.
\]
If a uniform inverse modulus \(\omega(\delta)\to0\) as \(\delta\downarrow0\) existed over this family, the output distance would be at most
\(\omega(d_4(Q_1^t,Q_2^t))\), contradicting (2) and the fixed gap. Failure on this admitted subfamily rules out such a guarantee over the larger admitted class as well.

Exact backward determination is preserved: no \(t>0\) pair of complete tables can be equal, because that would force equal earlier rows. Both tables approach the same boundary table \(H\), whose full entry is one and every proper entry zero at each parent. That table loses strictly positive full support. It is not an admitted \(t=0\) counterlaw; the inverse's relevant proper-entry ratios become \(0/0\) there.

This is a parameterized family approaching a boundary at the fixed parent size four. It proves neither large-size nonconvergence nor any asymptotic statement about the original fixed Part D pair.

### 5. Local continuity and history-law distinction

At a fixed strictly positive compatible later table \(Q^0\), the finite Part E formula is
\[
 R_{C,r}(S)=
 \frac{Q(C+\varnothing,r+0,S)}{Q(C+S,r+0,\varnothing)},
 \qquad
 F(Q)(C,r,S)=\frac{R_{C,r}(S)}{\sum_I R_{C,r}(I)},
\]
with the prescribed transport and both newborn bits chosen zero. There are finitely many queried denominators. Their minimum at \(Q^0\) is some \(m>0\); within entry distance \(m/2\), they stay at least \(m/2\). Ratios and finite sums are continuous, and the normalizing sums stay positive near \(Q^0\). Thus every reconstructed entry, and the finite maximum-entry output metric, varies continuously on the compatible domain near \(Q^0\).

This establishes local continuity without a uniform denominator bound over all positive tables. It does not establish predecessor existence for arbitrary perturbed tables, or recovery from measurements.

For every \(t>0\), the first-four-birth chain cylinder still has probabilities \(41/240\) and \(19/120\), with contrast \(1/80\). Its generating transitions are the unchanged parent-zero-through-three rows; later normalized continuations preserve that marginal and all complement mass. Near-equality of later conditional tables therefore does not imply near-equality of complete history laws. No sampled-data identifiability, physical indistinguishability, runtime/energy advantage, readout, native forward map, retrocausation, law selection or geometry result follows.

Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause and speculative Boundary separation remain.

## G. A relative-error certificate for one backward reconstruction

**Dependencies and review.** This part uses the admitted marked model in Part A, the complete-table backward reconstruction in Part E and the instability family in Part F. The proof and its stated premises received distinct mathematical review and coordinator acceptance. Compatibility and strictly positive support are input assumptions; the result supplies no measured probability floor or observation channel.

**Accepted conditional one-step theorem.** The certificate holds. If the maximum queried log-relative error is \(\epsilon\), every reconstructed structural row satisfies
\[
 \max_S|\log(p'_S/p_S)|\le4\epsilon,\qquad
 \operatorname{TV}(p,p')\le\tanh(\epsilon).
\]
A supplied common floor \(m>0\) on both tables' queried entries and maximum absolute entry error \(\eta\) give \(\epsilon\le\eta/m\). These are bounds between compatible mathematical tables, not measured error bars or a readout procedure.

### 1. Exact input and reconstruction

Fix a finite parent size \(n\), the full transported order/mark/individual-ideal dictionary, and fixed newborn bits, chosen zero for both routes. Let \(Q,Q'\) be strictly positive complete later tables, each having an admitted compatible predecessor. No compatibility or predecessor existence is inferred merely from proximity.

For a marked earlier parent \((C,r)\), define the actually queried structural entries
\[
 N_S=Q(C+\varnothing,r+0,S),\qquad
 D_S=Q(C+S,r+0,\varnothing),\qquad
 R_S=N_S/D_S,\quad p_S=R_S/\sum_I R_I.
\]
Use the same definitions with primes. All ideals \(S,I\) of \(C\), including the full ideal, remain separate occurrences. The earlier full ideal is proper in the enlarged later parent because it excludes the other newborn. The accepted diamond and label transport justify these queries and give
\(R_\varnothing=R'_\varnothing=1\). Their sums normalize complete earlier rows.

Let \(\mathcal J\) be the finite union of numerator and denominator coordinates actually queried across all marked earlier parents. It is a subset of the complete later dictionary, not an average or a replacement support. With natural logarithms, set
\[
 \epsilon=\max_{j\in\mathcal J}|\log(Q'_j/Q_j)|.
\]
Strict positivity and finiteness make this well-defined. Repeated queries do not change this maximum; repeated ideal occurrences still count in each normalization sum.

### 2. Log-error propagation

For one earlier row,
\[
 \delta_S=\log(R'_S/R_S)
 =\log(N'_S/N_S)-\log(D'_S/D_S)\in[-2\epsilon,2\epsilon],
 \qquad \delta_\varnothing=0.
\]
Writing \(p\) for the unprimed normalized row,
\[
 p'_S=\frac{p_Se^{\delta_S}}{\mu},
 \qquad \mu=\sum_I p_Ie^{\delta_I}.
\]
Let \(a=\min_S\delta_S\), \(b=\max_S\delta_S\), and \(h=b-a\). Since
\(e^a\le\mu\le e^b\),
\[
 \log(p'_S/p_S)=\delta_S-\log\mu,\qquad
 |\log(p'_S/p_S)|\le h\le4\epsilon. \tag{1}
\]
In particular \(e^{-4\epsilon}p_S\le p'_S\le e^{4\epsilon}p_S\). Every earlier slot, including the full slot, is covered.

### 3. Finite positive-weight tilt lemma

For any finite positive probability vector \(p\) and real tilts \(\delta_S\), normalize \(p'_S=p_Se^{\delta_S}/\mu\) as above. Then
\[
 \operatorname{TV}(p,p')\le\tanh\!\left(\frac{\operatorname{osc}(\delta)}4\right).
 \tag{2}
\]

**Proof.** If all tilts are equal, normalization cancels their common factor and \(p'=p\). Otherwise put \(\ell=e^a<u=e^b\) and \(w_S=e^{\delta_S}\), so \(\mu=\mathbb E_p w\in[\ell,u]\). Total variation is
\[
 \operatorname{TV}(p,p')=\frac{\mathbb E_p|w-\mu|}{2\mu}.
\]
The convex function \(w\mapsto|w-\mu|\) lies below its endpoint chord on \([\ell,u]\). Averaging that chord gives
\[
 \mathbb E_p|w-\mu|
 \le\frac{2(\mu-\ell)(u-\mu)}{u-\ell}.
\]
Therefore
\[
 \operatorname{TV}(p,p')
 \le\frac{(\mu-\ell)(u-\mu)}{\mu(u-\ell)}
 =\frac{u+\ell-\mu-u\ell/\mu}{u-\ell}
 \le\frac{u+\ell-2\sqrt{u\ell}}{u-\ell}
 =\frac{\sqrt u-\sqrt\ell}{\sqrt u+\sqrt\ell}
 =\tanh((b-a)/4).
\]
The middle inequality is \(\mu+u\ell/\mu\ge2\sqrt{u\ell}\). This proves the lemma without enumeration.

Applying it to reconstruction yields, uniformly over all earlier rows,
\[
 \boxed{\operatorname{TV}(p,p')\le\tanh(h/4)\le\tanh(\epsilon)}. \tag{3}
\]
Each individual absolute probability difference is also at most this total variation. This is a valid bound; no attainment or sharpness within the native compatible-law family is established.

If all reconstruction tilts are equal, their common value must be zero because \(\delta_\varnothing=0\); the rows agree exactly. In particular \(\epsilon=0\) gives zero log error and zero total variation. Equality of reconstructed rows need not imply \(\epsilon=0\): common factors can cancel in the queried ratios.

The scalar convention uses the probability of each ideal. In the joint ideal/newborn-bit convention, the probabilities are \(p_S/2\) and \(p'_S/2\) for each bit. Their likelihood ratios are unchanged, and summing both half-differences leaves total variation unchanged. Full-slot and fair-bit mass are retained throughout; no payload-trace division is involved.

### 4. Translation from a supplied common floor

Assume **both** \(Q_j\ge m\) and \(Q'_j\ge m\) for every \(j\in\mathcal J\), and complete structural-entry difference at most \(\eta\ge0\). The floor covers all queried numerators and denominators, not just denominator coordinates.

For two such entries \(x,y\), applying \(\log(1+z)\le z\) to the larger divided by the smaller gives
\[
 |\log(y/x)|\le\frac{|y-x|}{\min(x,y)}\le\frac{\eta}{m}.
\]
Thus
\[
 \boxed{\epsilon\le\eta/m,\qquad
 \max_S|\log(p'_S/p_S)|\le4\eta/m,\qquad
 \operatorname{TV}(p,p')\le\tanh(\eta/m)}. \tag{4}
\]
No assumption \(\eta<m\) is needed when the positive floor is independently supplied for both tables. The bound is informative according to the size of \(\eta/m\).

Such a floor must be feasible with normalization: if a row contains \(k\) distinct queried entries, \(km\le1\), strictly so when other positive outcomes remain. These inequalities do not make an arbitrary floor or perturbed table admissible. Both tables' compatibility remains an input premise.

For joint fair-bit entries, the corresponding structural floor/error \(m,\eta\) become \(m/2,\eta/2\); log-relative errors and their ratio \(\eta/m\) are unchanged. A fixed finite positive pair has some mathematical minimum, but qualitative positivity supplies neither a uniform numerical floor over the class nor a calibrated measured floor.

### 5. Reconciliation and scope

In Part F's new small-scale family, all coordinates queried by the backward formula are proper later slots. They have the form \(Q_i^t(j)=a(t)u_i(j)\). Hence
\[
 \log\!\frac{Q_2^t(j)}{Q_1^t(j)}
 =\log\!\frac{u_2(j)}{u_1(j)}
\]
is independent of \(t>0\). Shrinking absolute differences therefore need not shrink the queried relative errors. The usable common entry floor tends to zero with \(a(t)\).

The earlier chain-empty gap \(1/44\) implies that row's total variation is at least \(1/44\), consistent with (3): its global queried error must satisfy \(\tanh(\epsilon)\ge1/44\). The bound does not predict vanishing earlier error in that family. Its separate four-birth cylinder contrast \(1/80\) also remains unchanged.

The reconstruction \(F\) is generally many-to-one: for fixed branch \(i\), distinct positive \(t\) give different later tables but the same earlier kernel. Unique compatible backward determination is not injectivity of \(F\) or a unique forward continuation.

This part proves one finite-step certificate only. It does not revise the fixed Part D pair, iterate bounds without limit, establish a measured floor, calibrate readout, or infer physical observability, indistinguishability, efficient statistics, native-family sharpness, geometry or size asymptotics. No law is selected.

Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause and speculative Boundary separation remain.

### 6. Premises and certificate scope

- **Input:** two strictly positive compatible complete later tables on the same finite transported order/mark/individual-ideal dictionary. The accepted empty-reference formula uses fixed newborn bits; no arbitrary-perturbation predecessor existence is inferred.
- **Error definition:** natural-log relative error \(\epsilon\) over the union of actually queried numerator and denominator entries across every earlier row. Full dictionary and query set are distinguished; all actual ideal occurrences remain in normalization.
- **Derived bounds:** ratio tilts lie in \([-2\epsilon,2\epsilon]\), with empty tilt zero. Normalized row log-likelihood errors are at most the tilt oscillation \(h\le4\epsilon\). The proved finite tilt lemma gives TV at most \(\tanh(h/4)\le\tanh(\epsilon)\).
- **Controls:** equal tilts leave normalized weights unchanged; the empty reference then forces the common tilt to zero. Epsilon zero gives identical rows. The converse is not claimed.
- **Full mass:** every earlier full slot is included. Joint independently fair newborn-bit splitting preserves log-likelihood ratios and total variation.
- **Supplied floor:** both tables' queried numerator AND denominator entries must be at least \(m>0\). Complete absolute error at most \(\eta\) implies \(\epsilon\le\eta/m\), hence log error at most \(4\eta/m\) and TV at most \(\tanh(\eta/m)\). Feasibility with row normalization and compatibility remains required.
- **Not a measured floor:** finite positivity alone is neither a uniform class-wide lower bound nor an acquisition, calibration or error-bar procedure.
- **Part F reconciliation:** shared small-scale factors cancel in queried relative ratios while the usable floor collapses. Fixed earlier gap and persistent cylinder contrast are consistent. F is generally many-to-one, not an injective or uniquely forward-selecting map.
- **Limits:** one finite step, no unbounded iteration, native-family sharpness, revision of the fixed Part D pair, size asymptotics, sampled identifiability or physical readout.

## H. Complete finite marked endpoint-law sufficiency

**Dependencies and review.** This part retains the admitted marked model of Part A. For proper slots, the family restriction to the whole unmarked parent and marks on the selected ideal remains in force, although this reconstruction proof does not require it. The conditional finite theorem and its finite controls received distinct mathematical review and coordinator acceptance. The complete admitted marked endpoint distribution is the exact mathematical input; this result does not provide that distribution through observation.

**Accepted conditional finite theorem.** In the admitted scalar marked growth model, the complete law of the marked order isomorphism class after a fixed finite \(N\) births determines the entire natural-encoding history law through \(N\). It therefore determines every actual ideal/bit transition with parent size below \(N\). Endpoint and history total-variation distances are equal. A single realized endpoint, or its unmarked projection, does not supply this input.

### 1. Object and premises

Start at exactly the empty order. Every ideal, including empty and full, has strictly positive normalized probability \(q(P,r,S)\). Birth adds a maximal vertex with strict past \(S\), and an independently fair immutable bit \(b\). The joint branch probability is \(q(P,r,S)/2\). Retain equivariance and every complete marked incomparable-birth diamond, with final marks transported on their vertices. The scalar-passive payload does not supply extra classical information; no payload trace is divided out.

Let \(\mathcal H_N\) be all legal natural histories of \(N\) births, with birth labels \(1,\ldots,N\). A naturally labeled final order and its marks uniquely specify such a history: restrict to the first \(k\) labels at each step, and read each newborn's predecessor ideal and bit. Conversely each history gives that encoding. This is a bijection, without quotienting individual ideal choices.

Let \(\mathcal A_N\) be the marked order isomorphism classes, with mark symbols preserved. For \(A=[C,r]\), write \(\Gamma_A\subset\mathcal H_N\) for its distinct natural encodings. These finite fibers partition \(\mathcal H_N\). Full support makes every encoding positive: each finite order admits a linear extension, and its successive predecessor sets are legal ideals. This also makes every earlier marked parent reachable.

### 2. Equal weights and the correct multiplicity

Any two abstract linear extensions of \(C\) are connected by adjacent swaps of incomparable vertices. To see this inductively, move the first vertex of a target extension to the front of another extension. It is minimal among the remaining vertices; every vertex it passes is incomparable with it. Remove that first vertex and repeat.

Consider one adjacent swap. Both precursor ideals lie in the common earlier prefix, and neither newborn is in the other's precursor. The complete marked diamond equates the two structural products, including equal precursors and both newborn bits. The two fair factors are \(1/4\). After the pair, the marked state is identical under transport; equivariance preserves every subsequent factor. The entire history probabilities are therefore equal. Repeating swaps proves equality throughout \(\Gamma_A\).

Let \(e(C)\) count abstract linear extensions of the fixed concrete vertex set, and \(G=\operatorname{Aut}(C,r)\) be its mark-preserving order automorphism group. An automorphism acts on an extension's vertex list. This action is free: fixing the whole list fixes every vertex. Two lists produce the same labeled order/mark encoding exactly when their matching-positions bijection is a member of \(G\). Hence
\[
 m(A):=|\Gamma_A|=\frac{e(C)}{|G|}.
\]
No \(N!\) occurs. Abstract extensions are not already distinct encodings.

**Counting control.** A two-element antichain has \(e(C)=2\). With equal marks, \(|G|=2\), so \(m=1\): exchanging indistinguishable vertices produces the same encoding. With different marks, \(|G|=1\), so \(m=2\): the two encodings have bit strings \(01\) and \(10\). Mark flipping is not a mark-preserving automorphism. Thus a common per-encoding probability contributes once or twice respectively, never twice followed by another orbit multiplier.

### 3. The common conditional rule and prefix recovery

For an admitted law \(q\), let \(\mu_q(h)\) be its natural-history probability and \(\pi_q(A)\) its complete marked endpoint probability. Equal weights give
\[
 \mu_q(h)=\frac{\pi_q(A)}{m(A)}\quad(h\in\Gamma_A),\qquad
 K_N(h\mid A)=\frac{\mathbf1_{\{h\in\Gamma_A\}}}{m(A)}.
 \tag{1}
\]
The conditional rule \(K_N\) is independent of the growth law. It contains only the specified encoding dictionary and multiplicities. Each history probability already includes all \(N\) fair-bit factors; (1) introduces no further \(2^{-N}\).

For a specified natural prefix \(g\) of \(n\le N\) births, define
\[
 c_A(g)=|\{h\in\Gamma_A:h|_n=g\}|,\qquad
 p_q(g)=\sum_{A\in\mathcal A_N}\pi_q(A)\frac{c_A(g)}{m(A)}.
 \tag{2}
\]
These finite sums recover every prefix cylinder, with all future extensions retained. For \(n<N\), append the actual ideal \(S\) and bit \(b\) to \(g\), giving \(g(S,b)\). Positivity permits
\[
 \Pr_q(S,b\mid g)=\frac{p_q(g(S,b))}{p_q(g)}
 =\frac{q(P_g,r_g,S)}2.
 \tag{3}
\]
Thus the complete earlier transition row is recovered. Distinct symmetry-related ideals remain distinct numerator cylinders, even when their next endpoints are isomorphic. Equivariance transports the result to any representative parent. The supplied endpoint law must come from an admitted law; arbitrary positive endpoint masses need not reconstruct admissible fair-mark/local kernels.

For \(N=0\), the sole history is empty and there are no earlier transitions. For \(N=1\), the construction recovers the forced empty-parent row and its two fair outcomes. Generally, (3) covers only \(n<N\); it does not determine a unique future continuation. For example, in accepted Part F, fixed branch \(i\) and different positive \(t\) retain exactly the same history and endpoint laws through four births while giving different parent-four tables \(Q_i^t\). The special empty-parent row remains forced independently of such examples.

### 4. Exact total-variation equality and the finite witness

Take two admitted laws with the same conventions and finite \(N\). Because the fibers are disjoint and (1) is common,
\[
 \begin{aligned}
 \operatorname{TV}(\mu_1,\mu_2)
 &=\frac12\sum_A\sum_{h\in\Gamma_A}
       \left|\frac{\pi_1(A)-\pi_2(A)}{m(A)}\right|\\
 &=\frac12\sum_A|\pi_1(A)-\pi_2(A)|
 =\operatorname{TV}(\pi_1,\pi_2).
 \end{aligned} \tag{4}
\]
This is equality for complete laws, not a guarantee for selected statistics.

The accepted \(\lambda=1,2\) all-size pair in Parts C–D has first-four-birth chain-cylinder probabilities \(41/240\) and \(19/120\), differing by \(1/80\). At every finite \(N\ge4\), later normalized continuation preserves that cylinder. Consequently
\[
 \boxed{\operatorname{TV}(\pi_1^{(N)},\pi_2^{(N)})\ge1/80.}
 \tag{5}
\]
The application retains the pair's admitted potential identity and extension-sufficiency premises. The general finite theorem (1)–(4) does not need that extension theorem.

For \(N>4\), the first-four cylinder is not assumed to be an indicator of the final isomorphism class. Its conditional probability is the bounded function
\(f_N(A)=|\{h\in\Gamma_A:h|_4\text{ is a chain}\}|/m(A)\).
The difference of its expectations is \(1/80\), also proving (5). No assertion about an infinite unlabeled endpoint or a limiting geometry follows.

### 5. Failure control and observation boundary

Part B supplies the original finite law \(q_0\) and its global mark-flipped transport \(q_1(P,r,S)=q_0(P,1-r,S)\). Flipping every bit bijects their histories and leaves every unmarked endpoint unchanged. Their complete unmarked endpoint laws therefore agree at the admitted finite horizons.

Nevertheless their marked laws differ already at three births. For a three-fork whose root and both leaves are zero, there is one natural encoding: two abstract leaf orders divided by two mark-preserving automorphisms. Its structural weights are \(1/18\) and \(1/9\); including the three fair bits gives endpoint probabilities \(1/144\) and \(1/72\). Thus the unmarked law cannot replace the marked law in (1). A selected height statistic also cannot do so, since even the full unmarked laws agree in this example.

This theorem is conditional finite classical reconstruction. A complete probability law is not one realized endpoint or an empirical frequency table. No physical label access, tomography, calibration, repeated-trial protocol, intervention, efficient counting, computational advantage, law selection or new quantum dynamics is established. The prior backward-table theorems and their continuity qualifications are unchanged.

Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause and Boundary separation persist.

### 6. Premises, scope and failure controls

- **Model:** exact empty initial state; finite order with immutable binary marks; one maximal birth with any actual ideal as strict past; strict positivity and complete normalization; independently fair newborn mark; parent-state kernel; equivariance; every complete unnormalized marked diamond with inherited and final marks transported.
- **History dictionary:** birth labels \(1,\ldots,N\) and every individual ideal/bit choice. Each natural final encoding uniquely specifies its full prefix history. Abstract linear extensions, distinct encodings and marked isomorphism classes are different sets.
- **Multiplicity theorem:** adjacent incomparable swaps connect linear extensions and preserve complete probability. The mark-preserving automorphism group acts freely on extension lists, with encoding fibers its orbits. Thus \(m([C,r])=e(C)/|\operatorname{Aut}(C,r)|\). Equal-mark two-antichain gives one encoding; different marks give two. No factorial or duplicate orbit factor.
- **Input:** the entire admitted probability law on marked endpoint isomorphism classes at one finite \(N\), with mark names retained. This is neither a realized endpoint nor samples nor an unmarked projection.
- **Derived result:** conditional on a marked endpoint, each distinct natural encoding has probability \(1/m\), independent of the admitted law. Finite sums recover all prefix cylinders. Positive conditioning recovers actual ideal/bit probabilities on all parents of size less than \(N\); scalar ideal probabilities are twice these fair-bit probabilities.
- **Compatibility:** no claim that arbitrary endpoint masses give a legal kernel. Strict support makes every legal prefix and parent reachable. Empty and singleton horizons are handled.
- **Future limitation:** no unique continuation is implied. Accepted Part F supplies different parent-four continuations with identical laws through four births when branch \(i\) is fixed and \(t\) varies.
- **Distance result:** complete history and marked endpoint total variations are exactly equal. For the accepted all-size pair, the first-four-birth chain contrast \(1/80\) gives an endpoint-law TV lower bound for every fixed finite \(N\ge4\). At later \(N\), the cylinder induces a conditional function on endpoints, not necessarily an endpoint indicator.
- **Extra existence premise only for witnesses:** the pair's all-size existence retains the admitted maximal-deletion identity and extension sufficiency. The basic finite sufficiency/TV theorem uses diamonds, positivity, normalization, transport and the stated model, without that extension premise.
- **Failure control:** the accepted finite \(q_0\)/global-mark-flipped \(q_1\) pair has identical unmarked endpoint laws but different marked three-fork probabilities \(1/144\) and \(1/72\) for all-zero marks. Selected height data is likewise insufficient in that example.
- **Limits:** no infinite unlabeled endpoint result, size limit, physical observation or label access, efficient counting, computational or energy advantage, calibration, repeated trials, intervention, law selection or new quantum dynamics. Payload remains scalar-passive.

## I. An exact finite endpoint-law admission criterion

**Dependencies and review.** This part asks when exact finite endpoint masses generate a law in the admitted model of Part A, using the encoding lift proved in Part H. The theorem, its finite locality countermodel and its admitted positive control received distinct mathematical review and coordinator acceptance. Selected-mark locality permits the whole unmarked parent and marks on the chosen proper ideal; it is not a spatial or relativistic locality condition. A prescribed prefix is an additional explicit constraint, and no historical seed is silently substituted.

**Accepted conditional finite theorem and countermodels.** For a strictly positive normalized mass on every marked endpoint class at a fixed finite horizon, its uniform encoding lift automatically supplies positive normalized parent-state transitions, equivariance and complete marked diamonds. Admission to the declared model is equivalent to the fair-bit and proper-slot locality equations below, plus separate equalities for any prescribed prefix. Locality is not automatic: a three-birth control satisfies the other requirements and violates it.

### 1. Input and prefix potentials

Fix \(N<\infty\), exact empty start, and the complete dictionary of natural histories, actual ideal occurrences and immutable binary marks. Let \(\mathcal A_N\) be marked order isomorphism classes, preserving mark symbols. Assume
\(\pi(A)>0\) for every \(A\), and \(\sum_A\pi(A)=1\).

Accepted Part H gives the encoding count
\(m(A)=e(C)/|\operatorname{Aut}(C,r)|\) for \(A=[C,r]\). Define on every natural history \(h\) of length \(N\)
\[
 \mu(h)=\frac{\pi([h])}{m([h])}.
\]
Each naturally labeled final order/mark encoding determines its entire history. Distinct abstract extensions related by a mark-preserving automorphism are one encoding, not additional probability occurrences. Thus \(\mu\) is positive and normalized, with endpoint law exactly \(\pi\).

For a natural prefix \(g\), put
\[
 Z(g)=\sum_{h:\,h|_{|g|}=g}\mu(h)
     =\sum_{A\in\mathcal A_N}\frac{c_A(g)}{m(A)}\pi(A).
 \tag{1}
\]
Here \(c_A(g)\) counts the distinct natural encodings of endpoint \(A\) that extend \(g\). Every prefix has a completion, so \(Z(g)>0\); \(Z(\varnothing)=1\). These are finite linear forms in \(\pi\) with fixed nonnegative rational coefficients. No scientific enumeration is required for this existence statement.

### 2. What follows automatically

If prefixes \(g,g'\) encode the same marked parent, their order/mark isomorphism is a permutation of the first \(n\) labels. Extend that permutation by the identity on future labels. It bijects their completions: internal old relations become the target natural encoding, all future labels exceed the old ones, and future relations and marks are transported. Each matched completion has the same marked endpoint class and hence the same \(\mu\). Therefore \(Z(g)=Z(g')\); write \(Z(P,r)\).

For each actual ideal \(S\) and bit \(b\), write
\[
 Z_{S,b}(P,r)=Z(P+S,r+b),\quad
 B_S(P,r)=Z_{S,0}(P,r)+Z_{S,1}(P,r),\quad
 t_{S,b}(P,r)=\frac{Z_{S,b}(P,r)}{Z(P,r)}.
 \tag{2}
\]
Here the child carries the actual newborn and its mark. Prefix partition gives
\(\sum_{S,b}Z_{S,b}=Z(P,r)\), counting every ideal/bit event separately, including isomorphic children and full slots. Hence \(t>0\), its complete sum is one, and it depends only on the marked parent and actual event. Transport proves equivariance.

For incomparable births ending by \(N\), both routes telescope:
\[
 t_{S,b}(C,r)t_{T,c}(C+S,r+b)
 =\frac{Z(D,r_D)}{Z(C,r)}
 =t_{T,c}(C,r)t_{S,b}(C+T,r+c).
 \tag{3}
\]
The transported terminal marked order \(D\) is the same. This includes equal precursors, empty/full base ideals and every newborn-bit pair. Thus complete marked diamonds already hold for the joint transitions. Scalar branch maps \(t_{S,b}\operatorname{id}\) preserve the arbitrary passive payload upon complete summation.

Neither fair bits nor proper-slot mark locality was assumed in this argument.

### 3. Finite necessary-and-sufficient equations

For every parent of size \(n<N\), impose:

**F — fair bits, linear in \(\pi\):**
\[
 Z_{S,0}(P,r)=Z_{S,1}(P,r)\quad\text{for every actual ideal }S.
 \tag{F}
\]
Then the structural probability is \(q(P,r,S)=B_S(P,r)/Z(P,r)\), and \(t_{S,b}=q(P,r,S)/2\). Fairness holds conditional on the complete prefix and chosen ideal, as required.

**L — selected-mark locality, bilinear in \(\pi\):** for the same unmarked \(P\), every proper ideal \(S\subsetneq P\), and all \(r,r'\) with \(r|_S=r'|_S\),
\[
 B_S(P,r)Z(P,r')=B_S(P,r')Z(P,r).
 \tag{L}
\]
All denominators are positive, so this is exactly equality of the two structural probabilities. Full slots are exempt from L, but remain in F, normalization and every applicable diamond. Under F, either single-bit child mass can replace \(B_S\) on both sides, canceling a factor two.

**P — optional prescribed prefix, separate linear equations:** for each declared structural entry \(q^*(P,r,S)\) with parent size below \(N\), require
\[
 B_S(P,r)=q^*(P,r,S)Z(P,r).
 \tag{P}
\]
These are extra conditions for that declared seed, not part of the unrestricted finite class. Entries outside the horizon are not determined by this criterion. No historical seed or baseline is silently chosen or dropped.

**Theorem.** The uniform lift of \(\pi\) arises from the declared finite model through \(N\), respecting a prescribed prefix when present, if and only if F, L and the applicable P hold.

**Necessity.** Any admitted law with endpoint mass \(\pi\) has the same uniform lift by Part H. Its prefix probabilities therefore equal (1), and positive conditioning fixes (2). Its fair bits, locality and prescribed entries give F, L and P.

**Sufficiency.** Define \(q=B/Z\). Positivity, complete ideal normalization and equivariance follow from §2. F supplies the independently fair bit factor; L gives precisely the required proper-slot locality. Equation (3), with the two fair factors retained, proves the complete unnormalized marked diamonds on arbitrary payloads. P enforces exactly the specified prefix. Products of the joint transitions telescope to
\[
 \prod_{j=0}^{N-1}t_{S_j,b_j}(P_j,r_j)
 =\frac{Z(h)}{Z(\varnothing)}
 =\frac{\pi([h])}{m([h])}.
\]
Summing all \(m(A)\) distinct encodings recovers the exact supplied \(\pi(A)\). This proves existence and uniqueness of the finite kernel through parent \(N-1\), not merely normalization of a candidate table.

For \(N=0\) the conditions are vacuous and the only mass is the empty endpoint. At \(N=1\), F requires the two singleton-mark masses to be equal. Strict positivity and normalization are input conditions; F/P are linear and L is a finite family of degree-at-most-two equalities. No convexity, linear-feasibility or efficient-solving claim is inferred.

### 4. Failure and positive controls

**Biased marks.** At \(N=1\), give the zero-marked singleton mass \(1/3\) and the one-marked singleton \(2/3\). Both encoding counts are one. The lift is positive and normalized, but its child masses violate F. Arbitrary positive endpoint masses are therefore not admitted.

**Locality is independently needed in the general finite class.** At \(N=3\), construct an auxiliary structural kernel with fair newborn bits. Its empty-parent entry is one; both singleton entries are \(1/2\). Put \(c(0)=1/8,\ c(1)=1/4\). The two-element rows are:

| Parent | Empty | Other proper ideals | Full |
|---|---|---|---|
| Chain \(x<y\) | \(c(r_x)\) | \(\{x\}:1/4\) | \(3/4-c(r_x)\) |
| Antichain \(x\parallel y\) | \(1/4\) | \(\{x\}:c(r_x),\ \{y\}:c(r_y)\) | \(3/4-c(r_x)-c(r_y)\) |

Every entry is positive; chain full slots are at least \(1/2\), antichain full slots at least \(1/4\). Rows normalize and are equivariant. No prescribed historical prefix is asserted for this control.

All diamonds through three births can be checked symbolically. At the empty base the singleton-empty factors are equal. At a singleton base marked \(i\), both empty precursors give structural product \(1/8\); both full precursors give \(1/8\); mixed precursors give \(c(i)/2\) on either route. These formulas hold for all newborn bits; the common fair factor is \(1/4\). Thus every required marked diamond holds.

Define its endpoint masses by
\[
 \pi_{\rm aux}(A)=m(A)\,2^{-3}\prod_{j=0}^{2}
 q_{\rm aux}(P_j,r_j,S_j),
\]
using any encoding of \(A\). The diamonds make this independent of the encoding; complete row normalization gives total mass one and full support gives positivity. Its uniform lift is its history law, so F passes.

But on a two-chain the proper empty-ideal probability is \(1/8\) or \(1/4\) according to the root mark. The markings agree on the empty selected ideal. L fails. This proves locality is not a consequence of the other finite requirements. The construction is a rejected model candidate, not an admitted law or an all-size extension.

**Positive control.** Take the complete endpoint law at \(N=3\) of accepted \(q_*\) in Part B. Part H reconstructs its actual kernel; independently fair bits and its mark-independent rows satisfy F and L. If that same prefix is explicitly prescribed, P also holds. This does not assert agreement with a different prescribed seed.

### 5. Scope

This is an exact finite mathematical admission criterion. It supplies no all-size continuation, efficient algorithm, experimental admission, sampled-data confidence, calibration, physical label access, law selection or new quantum dynamics. The locality countermodel has only the stated three-birth horizon. No unbounded independence search was undertaken.

Part A fixes the admitted model; Part H supplies the accepted finite endpoint-law sufficiency theorem. The older witness in Parts C–D uses \(\lambda=1\) and \(\lambda=2\), not \(\lambda=1/2\); no witness is altered here. Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause and Boundary/physical/execution gates remain.

### 6. Premises, admission tests and scope

- **Input:** one fixed finite horizon N, exact empty start and the complete finite dictionary of natural histories, marked endpoint classes and actual ideal/bit events. Every endpoint class has strictly positive mass pi, with complete sum one.
- **Encoding convention:** immutable binary marks, mark-preserving isomorphisms, and distinct natural encodings counted by e(C)/|Aut(C,r)|. No factorial, orbit collapse or duplicate fair-bit factor.
- **Lift and automatic results:** mu(h)=pi([h])/m([h]); finite completion sums define positive prefix masses Z. A permutation of old labels, fixing future labels, bijects completions of isomorphic marked prefixes. Thus Z depends only on the marked parent. Child/parent ratios are positive normalized parent-state transitions, equivariant and satisfy complete marked diamonds by telescoping.
- **F:** each actual ideal's two bit-extension masses are equal. These linear equations supply q/2 joint transitions and conditional independently fair newborn bits.
- **L:** for a proper ideal S and markings agreeing on S, cross-multiply B_S/Z ratios, where B_S is the sum of the two child masses. These bilinear equations impose exactly selected-mark locality. Full slots are exempt from L only, not from support, normalization, fairness or applicable diamonds.
- **P:** any explicitly prescribed prefix adds separate linear equations B_S=q*Z for its declared entries below N. No particular historical seed is silently incorporated or discarded; entries beyond the horizon need separate information.
- **Iff proof:** admitted kernels must induce the uniform Part H lift, so their conditional probabilities force F/L/P. Conversely these equations supply every finite-model obligation, and telescoping yields exactly pi/m on histories and pi on endpoints. The kernel is unique through parent N-1 within this finite scope.
- **Constraint types:** input positivity/normalization; linear F/P; degree-at-most-two locality equations. No convexity, linear feasibility, efficient solver or sampled-data admission is claimed.
- **Negative control:** N=1 singleton-mark masses 1/3 and 2/3 are positive normalized but violate F.
- **Locality independence:** a three-birth auxiliary fair-bit kernel has singleton row (1/2,1/2); chain row (c(root),1/4,3/4-c(root)); antichain row (1/4,c(first),c(second),3/4-c(first)-c(second)), with c(0)=1/8,c(1)=1/4. It is positive, normalized, equivariant and satisfies all finite marked diamonds; its induced endpoint law passes F but its chain-empty entry violates L. This rejected candidate is not claimed to match a prescribed historical prefix or extend beyond three births.
- **Positive control:** accepted q* at N=3 gives a complete endpoint law satisfying F/L; P holds when that same prefix is declared.
- **Gates:** distinct scientific review and coordinator disposition; protected validation/custody, ABSTAIN, Status M, zero qualification, RET-only pause, speculative Boundary separation, physical and execution gates unchanged. No all-size, observation, efficiency, empirical admission, law-selection or new quantum-dynamics result.

## J. Whole-law mixing does not generally preserve locality

**Dependencies and review.** This part uses the admitted finite model and printed laws in Parts A–B, the common encoding lift in Part H and the finite admission criterion in Part I. Its exact mixture-locality criterion, altered component and four-birth nonconvexity witness received distinct mathematical review and coordinator acceptance. Mixing entire laws is distinguished from fresh row averaging. The counterexample retains precisely the complete parent-zero and parent-one prefix shared by its components; it does not impose the entire historical parent-three seed.

**Accepted conditional finite counterexample and exact slot criterion.** At four births, two laws satisfying the declared finite model can have a whole-law midpoint whose uniquely reconstructed kernel violates selected-mark locality. The half-scale component passes all required finite checks. This establishes nonconvexity of the admitted finite endpoint/history-law set at this horizon, while retaining the accepted equal-scale symmetrization as a positive control.

### 1. Fixed whole-law mixture

Use the empty start, complete positive actual-ideal support, immutable independently fair marks, equivariance, complete marked diamonds and passive scalar payload of the admitted model. Proper-slot locality allows the whole unmarked parent and only the marks on the selected ideal. It is not a claim about spatial or relativistic locality.

Let two admitted finite laws \(A,B\) have complete endpoint masses \(\pi_A,\pi_B\) at the same \(N\), history laws \(\mu_A,\mu_B\), and per-natural-prefix masses \(Z_A(P,r),Z_B(P,r)>0\). For a fixed \(0\le a\le1\), define
\[
 \pi_a=a\pi_A+(1-a)\pi_B,\qquad
 \mu_a=a\mu_A+(1-a)\mu_B.
\]
Part H's common encoding conditional \(K_N\) gives
\(\pi_aK_N=\mu_a\). Prefix summation therefore gives
\(Z_a=aZ_A+(1-a)Z_B\). Each component's child mass is
\(Z_j(P,r)q_j(P,r,S)/2\), so positive conditioning yields
\[
 q_a(P,r,S)=\omega_a(P,r)q_A(P,r,S)
       +(1-\omega_a(P,r))q_B(P,r,S),\qquad
 \omega_a=\frac{aZ_A}{aZ_A+(1-a)Z_B}. \tag{1}
\]
The newborn bit is still independently fair.

This is fixed mixing of entire laws. The effective weight after a prefix is generally not \(a\); multiplying freshly averaged rows defines a different law. The word posterior here denotes the ratio in (1), without an assumed physical hidden component or calibrated inference procedure.

Positive support, normalization and equivariance persist. By accepted Part I, the prefix-potential construction gives every complete marked diamond through \(N\): both joint routes equal \(Z_a(D)/Z_a(C)\). Thus the possible obstruction is locality, not the already known diamond failure of fresh row averaging. If both components have the same separately prescribed entries, (1) preserves those entries too.

### 2. Exact locality criterion on one slot

Fix an unmarked parent \(P\), a proper actual ideal \(S\), and markings \(r,r'\) agreeing on \(S\). Component locality gives common values
\[
 v_A=q_A(P,r,S)=q_A(P,r',S),\quad
 v_B=q_B(P,r,S)=q_B(P,r',S).
\]
Equation (1) gives the exact difference
\[
 q_a(P,r,S)-q_a(P,r',S)
 =(v_A-v_B)\,[\omega_a(P,r)-\omega_a(P,r')]. \tag{2}
\]
For \(0<a<1\), equality of the two posterior weights is equivalent to
\[
 Z_A(P,r)Z_B(P,r')=Z_A(P,r')Z_B(P,r). \tag{3}
\]
Thus locality on this slot holds precisely when (2) vanishes for every such marking pair. On each fixed selected-mark fiber, either the component slot values coincide, or their prefix likelihood ratio must be constant over the unselected marks.

Equivalently, let \(B_a(P,r,S)=Z_a(P,r)q_a(P,r,S)\), the sum of the two bit-child masses. The Part I locality residual is
\[
 \begin{aligned}
 &B_a(P,r,S)Z_a(P,r')-B_a(P,r',S)Z_a(P,r)\\
 &\quad=a(1-a)(v_A-v_B)
 [Z_A(P,r)Z_B(P,r')-Z_A(P,r')Z_B(P,r)].
 \end{aligned} \tag{4}
\]
This factorization proves the criterion; it does not infer nonconvexity merely from quadratic equations. At \(a=0,1\), admission is inherited. Full ideals are exempt from this locality test, while retaining their mass and other obligations.

### 3. Admission of the second component

Let \(q_0\) be the printed finite prefix in Parts A–B, and
\(q_1(P,r,S)=q_0(P,1-r,S)\). Both are accepted through four births. For parents of size below three, retain \(q_1\) exactly. At size three define
\[
 \widetilde q_1(P,r,S)=\tfrac12q_1(P,r,S)\quad(S\subsetneq P),
 \qquad
 \widetilde q_1(P,r,P)=1-\tfrac12\sum_{S\subsetneq P}q_1(P,r,S).
 \tag{5}
\]
This reduces the common proper-slot scale \(e=1/44\) to \(e/2\), with every full slot recomputed, not rescaled.

**Support and normalization.** Every proper occurrence remains positive. Writing the original full probability as \(q_1(P,r,P)>0\), the new full probability is
\(\tfrac12+\tfrac12q_1(P,r,P)>1/2\). Every complete row sums to one. All actual ideal occurrences remain in the sum.

**Locality, transport and payload.** The same constant multiplies every proper slot, preserving its selected-mark dependence and equivariance. Full complements may read all old marks as the model permits. Newborn bits remain fair; complete branch maps \(\widetilde q_1(P,r,S)\operatorname{id}/2\) sum to identity on every admitted payload.

**All diamonds within \(N=4\).** Diamonds ending by three births use only unchanged rows. A diamond ending at four births has a size-two base. Each second precursor omits the other newborn and is therefore proper in its intermediate size-three parent. Both routes' original structural products acquire exactly one factor \(1/2\); the first factors are unchanged. Original marked diamond equality persists, including empty/full base ideals, equal precursors, every inherited marking and all four newborn-bit choices. The two fair factors remain \(1/4\), with identical terminal transport. A size-three full slot cannot be a second precursor of these incomparable diamonds. No diamond beyond this horizon is asserted.

Thus \(\widetilde q_1\) satisfies every stated finite-model obligation through four births. This is a new finite component; it does not preserve the original prescribed parent-three prefix.

### 4. Exact four-birth failure of closure

Take components \(A=q_0\), \(B=\widetilde q_1\), with \(a=1/2\). Consider a three-fork, root mark \(i\), and fixed zero marks on both leaves. The printed values are
\[
 f_0=1/6,\qquad f_1=1/3,\qquad e=1/44.
\]
Its per-encoding structural prefix weights are
\[
 w_A(i)=f_i/3,\qquad w_B(i)=f_{1-i}/3.
\]
The half-scale alteration affects parent-three transitions only, so it cannot change these three-birth prefix weights. Actual prefix masses are \(Z_j=2^{-3}w_j\). Their common fair factor cancels in (1); no automorphism multiplier is added. If endpoint-class prefix masses were used instead, their common encoding multiplicity would also cancel.

Consequently
\[
 \omega_{1/2}(0)=1/3,\qquad \omega_{1/2}(1)=2/3.
\]
For the proper empty ideal, the component probabilities are \(e\) and \(e/2\), independently of all marks. Therefore
\[
 q_{1/2}(P,r,\varnothing)=\frac e2(1+\omega_{1/2}(i)),
\]
\[
 q_{1/2}(i=0,\varnothing)=\frac{2e}{3}=\frac1{66},\qquad
 q_{1/2}(i=1,\varnothing)=\frac{5e}{6}=\frac5{264}. \tag{6}
\]
Their difference is \(e/6=1/264\). These are structural probabilities; each bit branch retains its factor \(1/2\). The two markings agree on the empty selected ideal, yet the probabilities differ. Selected-mark locality fails.

Both component endpoint distributions at \(N=4\) are positive and admitted by the preceding checks. Their midpoint has the unique uniform lift and unique positive prefix-conditioned kernel. Hence no alternative admitted kernel can realize that same midpoint while repairing (6): Part H uniqueness and Part I's necessity of locality exclude it. This proves nonconvexity of the admitted complete endpoint-law set at \(N=4\), and of the corresponding history-law set.

The largest shared complete prescribed prefix of these components is parent sizes zero and one: the empty row and singleton row \((2/3,1/3)\). At parent two, the chain's root-slot values \(f_i\) and \(f_{1-i}\) already differ. Thus the counterexample also holds with that actually shared prefix fixed, but makes no claim for the full historical seed fixed through parent three or every special subfamily.

### 5. Positive control and scope

With the original equal-scale pair \(q_0,q_1\), Part B proves that their equal whole-law mixture \(q_*\) satisfies locality on every row through parent three. In the fork-empty slot specifically, both component values are \(e\), so (2) vanishes despite the same root-dependent posterior weights. Part B's complete mark-independent rows and positive full complements supply the full positive control. This special cancellation is consistent with the new failure when one component has scale \(e/2\).

The accepted fresh-row-average diamond failure is unchanged and is not counted as this result. Finite reconstruction uniqueness concerns which kernel a supplied law determines; it does not say the admitted-law class is closed under uncertainty expressed by whole-law mixtures.

All results remain within the declared finite model and \(N=4\) counterexample. No physical latent sector, hidden memory, Bayesian calibration, law-selection principle, infinite extension, efficient method, empirical conclusion or new quantum dynamics follows. Parts A–B supply the model, printed pair and positive control; Parts H–I supply the accepted reconstruction and admission results. Protected validation/custody, distinct review, ABSTAIN, Status M, zero qualification, RET-only pause and Boundary/physical/execution gates remain.

### 6. Mixture locality, component admission and scope

- **Model:** fixed finite horizon, empty start, complete positive actual-ideal support, immutable fair bits, parent-state kernels, equivariance, complete transported marked diamonds and scalar-passive payload. Proper-slot locality concerns selected old marks, not spatial or relativistic locality.
- **Whole-law convention:** one fixed weight a mixes complete endpoint/history laws. Part H's common encoding lift gives the same mixture of history and prefix masses. Fresh row averaging is a different construction.
- **Exact kernel:** q_a=omega q_A+(1-omega)q_B with omega=a Z_A/[a Z_A+(1-a)Z_B]. Newborn bits remain fair. Positivity, normalization, parent sufficiency, equivariance and finite diamonds follow through the Part I prefix-potential construction.
- **Locality criterion:** for fixed P, proper S and two markings agreeing on S, the mixed-slot difference is (v_A-v_B)(omega(r)-omega(rprime)). For interior a, posterior equality is exactly Z_A(r)Z_B(rprime)=Z_A(rprime)Z_B(r). The bilinear locality residual factors by a(1-a)(v_A-v_B) times that cross-product difference. Full slots are exempt only from locality.
- **Prescribed prefix:** any structural entries shared by both components are retained. The displayed counterexample shares complete parent layers zero and one only, not the original full parent-three seed.
- **New component:** retain the accepted mark-flipped q1 below parent size three; halve every actual proper slot at parent three and replace each full slot by its complete complement. Proper entries stay positive and new full entries equal (1+old full)/2 >1/2. Scaling preserves proper mark locality and equivariance; fair-bit splitting and passive payload maps remain.
- **Finite diamond proof:** terminal sizes at most three are unchanged. At terminal size four, both second precursors are proper and each route acquires one factor 1/2. This covers all inherited/newborn marks, equal precursors and empty/full base ideals. No beyond-four-birth claim.
- **Negative control:** mix q0 and the verified altered q1 at equal whole-law weights. Three-fork structural prefix weights f_i/3 and f_(1-i)/3 are unchanged by the later alteration; f0=1/6,f1=1/3. Posterior weights are 1/3 and 2/3. Empty-slot values e and e/2 give mixed probabilities 1/66 and 5/264, gap 1/264, although the selected empty ideal has identical mark restriction.
- **Closure conclusion:** both N4 endpoint laws are admitted; their midpoint fails locality. Unique finite reconstruction prevents an alternative local kernel for that same midpoint. This is an explicit nonconvexity witness for the general finite law class, also with its actual shared parent-zero/one prefix fixed; not an inference from quadratic notation or a claim about every special subfamily.
- **Positive control:** accepted equal-scale q0/q1 symmetrization remains admitted through N4. Equal fork-empty component values make posterior variation cancel, and Part B's complete row calculation verifies all proper slots.
- **Multiplicity:** natural-history probabilities already include fair factors. The common factor 2^-3 cancels in the displayed posterior; isomorphism-class multiplicity would multiply both component weights equally. No new factorial, support restriction or duplicate orbit weight.
- **Limits:** No latent physical sector, hidden memory, Bayesian calibration, law selection, all-size extension, efficiency, empirical result or new quantum dynamics.
- **Gates:** distinct review and coordinator disposition; protected validation/custody, ABSTAIN, Status M, zero qualification, RET-only pause, speculative Boundary separation and physical/execution gates unchanged.

## K. Self-orbit symmetrization is closed through four births

**Dependencies and review.** This part uses the model and controls in Parts A–B and the exact whole-law mixture criterion in Part J. The theorem received distinct mathematical review and coordinator acceptance for every admitted law through four births with the stated empty and singleton rows. Its lower-layer formulas are necessary consequences of admission, not a sufficient free-parameter classification. Parent-three rows remain arbitrary within that admitted class, and the result proves selected-mark locality rather than universal mark independence.

**Accepted conditional finite theorem.** Every admitted law through \(N=4\), with empty start and the prescribed singleton row \((2/3,1/3)\), has an admitted equal whole-law average with its own global mark flip. The proof covers the entire declared class, including arbitrary admitted parent-three rows. It does not fix the historical later seed or infer closure at larger horizons.

### 1. Statement and mixture reduction

Retain strictly positive complete ideal support, immutable independently fair binary marks, equivariance, complete transported marked diamonds, selected-mark locality on proper ideals, and scalar-passive payload. Let \(F\) flip every mark in a complete history and \(L^F=F_*L\). Its structural kernel is
\[
 q^F(P,r,S)=q(P,1-r,S).
\]
Global flipping preserves every model obligation: it transports all old/newborn marking cases, preserves fair bits, and preserves agreement of marks on a selected ideal. It also preserves the fixed empty and singleton rows.

For the equal whole-law mixture \(\bar L=(L+L^F)/2\), accepted Part J gives
\[
 \bar q(P,r,S)=\omega(P,r)q(P,r,S)
 +(1-\omega(P,r))q(P,1-r,S),\qquad
 \omega(P,r)=\frac{Z(P,r)}{Z(P,r)+Z(P,1-r)}, \tag{1}
\]
where \(Z\) is the probability of one specified natural prefix encoding. These are positive finite masses, including the fair-mark factors.

The common endpoint encoding lift and prefix summation show that (1) realizes exactly \(\bar L\). Positivity, normalization, independently fair newborn bits, parent sufficiency, equivariance and every marked diamond through four births follow from the accepted mixture/prefix-potential result. Both components retain the prescribed parent-zero/one rows. Only proper-slot locality requires further proof.

For markings \(r,r'\) agreeing on a proper ideal \(S\), component locality makes \(v=q(P,r,S)=q(P,r',S)\) and \(v^F=q(P,1-r,S)=q(P,1-r',S)\). The accepted slot criterion is
\[
 \bar q(P,r,S)-\bar q(P,r',S)
 =(v-v^F)\,[\omega(P,r)-\omega(P,r')]. \tag{2}
\]

### 2. Necessary lower-layer form for every admitted law

Write \(a=2/3\) for the singleton empty probability, with full probability \(1-a=1/3\). At a two-chain \(x<y\), proper-slot locality forces
\[
 q(\varnothing)=c,\qquad q(\{x\})=f_i,\qquad
 q(\{x,y\})=h_i:=1-c-f_i,\qquad i=r_x. \tag{3}
\]
The empty ideal reads no marks. The root ideal reads only its root mark. Complete normalization therefore forces even the full entry to be independent of the upper mark.

At a two-antichain \(x\parallel y\), locality and equivariance initially give empty probability \(d\) and singleton probabilities \(g(r_x),g(r_y)\), using the same function \(g\) for both transported actual ideals.

Take the complete diamond from a singleton \(x\), marked \(i\), with precursors \(\varnothing\) and \(\{x\}\). Empty-first gives an antichain then its old-root singleton; full-first gives a chain then its empty ideal. Canceling the common fair factor \(1/4\) gives
\[
 a\,g(i)=(1-a)c,\qquad g(i)=c/2\quad(i=0,1). \tag{4}
\]
This holds for both newborn bits without restriction. Hence every two-antichain row is
\[
 (d,c/2,c/2,k),\qquad k=1-d-c. \tag{5}
\]
All displayed entries \(c,d,f_0,f_1,h_0,h_1,k\) are positive because they belong to the original admitted law.

Equations (3)–(5) are **necessary forms derived from the model**, not a chosen parameter family. No historical values for \(c,d,f_i\), or any parent-three coefficient \(e\), are imposed. Nor is every positive parameter tuple asserted to extend: the starting law is already admitted through four births.

### 3. Complete three-birth prefix-weight analysis

Let \(w(P,r)\) be the structural product along one natural history producing \(P,r\). Complete marked diamonds and equivariance make it independent of the chosen natural encoding; the actual per-encoding mass is \(Z(P,r)=2^{-|P|}w(P,r)\). Normalized later transitions cannot change this prefix mass.

For parent sizes zero, one and two, the structural weights are respectively \(1\), \(1\), and \(a\) for an antichain or \(1-a\) for a chain. All are mark-independent, so \(\omega=1/2\) there.

Every three-element order is one of the following five shapes:

| Parent | Structural weight for any marking | Possible mark dependence |
|---|---|---|
| Antichain | \(ad=2d/3\) | None |
| Edge plus isolate | \((1-a)c=c/3\) | None |
| Fork | \((1-a)f_i=f_i/3\) | Root mark \(i\) only |
| Join | \(ak=2k/3\) | None |
| Chain | \((1-a)h_i=h_i/3\) | Minimum mark \(i\) only |

These weights follow directly from a legal construction of each shape: start with the appropriate two-chain or two-antichain and use its empty, root or full ideal. For the edge-plus-isolate alternative construction, \(ag(i)=(1-a)c\) is exactly (4). Every inherited marking and every role is covered.

For completeness, the shape list is exhaustive by the number of comparable unordered pairs: zero gives an antichain, one an edge plus isolate, two a fork or join, and three a chain. With two pairs, a directed two-edge chain would force a third pair by transitivity. This is a finite structural argument, not a numerical search.

All weights are per distinct encoding. No factorial, automorphism multiplier or extra bit factor is introduced. For the flip comparison the common factor \(2^{-3}\) cancels. Thus \(\omega=1/2\) on the three mark-independent shapes, while
\[
 \omega_{\rm fork}(P,r)=\frac{f_i}{f_i+f_{1-i}},\qquad
 \omega_{\rm chain}(P,r)=\frac{h_i}{h_i+h_{1-i}}. \tag{6}
\]
Strict positivity makes every denominator legal. Leaf marks and upper-chain marks do not enter (6).

### 4. Locality on every required slot

Only parents of sizes zero through three generate transitions within \(N=4\).

For every proper empty ideal, at any such parent, the original locality condition makes \(q(P,r,\varnothing)\) independent of all marks. Consequently \(v=v^F\), and (2) vanishes even if the posterior depends on marks. This uses no common empty probability across different unmarked shapes.

For every proper ideal at parent size at most two, and at a three-antichain, edge-plus-isolate or join, the posterior is the constant \(1/2\). Equation (2) again vanishes for every pair of markings agreeing on the selected ideal.

The only remaining parents are the three-fork and three-chain, with a nonempty proper ideal. Every such ideal contains the fork root or chain minimum, respectively. Markings agreeing on that ideal therefore have the same \(i\) in (6). Their posterior weights coincide, so (2) vanishes regardless of the admitted parent-three slot values or dependence on other selected marks.

This exhausts all proper ideals and all markings. Full ideals remain exempt only from locality; their positive mass, complete normalization, fair bits and applicable diamonds were retained in §1. Thus the reconstructed mixture satisfies every declared finite-model obligation, proving the theorem. Since \(F^2\) is identity, \(F_*\bar L=\bar L\), so the resulting finite law is globally mark-name symmetric.

The proof leaves the parent-three rows arbitrary within the admitted class. General selected-mark locality is proved; additional mark independence of every symmetrized row is not asserted.

### 5. Controls and limits

The printed Part B example is recovered by taking its admitted values \(c=1/5,d=1/4,f_0=1/6,f_1=1/3\), giving \(g=c/2=1/10\), \(k=11/20\), and its stated fork/chain posterior weights. Part B's complete positive local mixture remains the accepted special control.

Part J's negative pair uses an independently halved parent-three scale in its second component. That component is not the first law's own mark flip. In particular, it gives different fork-empty component values \(e\) and \(e/2\); a genuine self-flip must give equal values on every proper empty slot. The arbitrary-pair nonconvexity result remains valid and does not contradict this self-orbit theorem.

This result covers exactly the declared \(N=4\) class with the actual parent-zero/one prefix. No full historical parent-three seed, separately rescaled second component, larger horizon, or sufficiency of a free parameter family has been inserted. The proof's small-parent weight structure does not establish an all-size symmetrization prescription or a law-selection principle.

No physical latent sector, calibrated readout, efficient procedure, empirical validation or DET physical derivation is supplied. Parts A–B provide the model and accepted controls; Part J supplies the accepted mixture-locality criterion. Preserve independent review, protected validation/custody, ABSTAIN, Status M, zero qualification, RET-only pause and Boundary/physical/execution gates.

### 6. Self-orbit theorem premises and scope

- **Claim:** for every admitted law through N=4 with exact empty start and singleton row (2/3,1/3), the equal whole-law average with its own global immutable-mark flip is admitted through N=4 and is globally mark-name symmetric.
- **Model retained:** complete positive actual-ideal support; independently fair newborn bits; parent-state kernel; equivariance; complete transported marked diamonds; proper-slot selected-mark locality; arbitrary scalar-passive payload.
- **Same-law requirement:** q^F(P,r,S)=q(P,1-r,S). Fix the law first, then flip every mark. No independent rescaling of the second component and no fresh arithmetic row averaging.
- **Mixture reduction:** accepted Part J gives posterior-weighted qbar with omega=Z(r)/(Z(r)+Z(1-r)); automatic positivity, normalization, fairness, equivariance and finite diamonds. The remaining locality residual is (v-v^F)(omega(r)-omega(rprime)).
- **Universal necessary lower-layer form:** locality gives chain row (c,f_i,1-c-f_i). Antichain proper singleton entries initially g(i); the singleton empty/full diamond forces (2/3)g(i)=(1/3)c, so g=c/2 and the full antichain row is (d,c/2,c/2,1-d-c). This is derived for every admitted law, not restricted to printed numerical seed values.
- **No new admission classification:** the parameters are inherited from an already admitted law. No assertion that every positive tuple extends, and no historical parent-three coefficient is fixed.
- **Prefix weights:** at sizes <=2, structural weights are mark-independent. At size3 the exhaustive five shapes have weights 2d/3, c/3, f_i/3, 2k/3, h_i/3 for antichain, edge-plus-isolate, fork, join and chain. Only fork root or chain minimum marks can affect these weights.
- **Completeness:** the five three-vertex shapes follow from 0/1/2/3 comparable pairs and transitivity; all role markings and actual ideal occurrences are retained. Each table entry is per distinct natural encoding, not an orbit total; fair factors are counted once.
- **Locality proof:** empty proper slots have equal component values under self-flip. Other slots at mark-independent-prefix shapes have constant posterior. Every nonempty ideal of a fork/chain contains the sole root/minimum whose mark controls its posterior. Thus no required slot can acquire unselected-mark dependence.
- **Parent-three freedom:** arbitrary admitted rows at parent three are retained in the universal argument. Full slots are exempt only from locality, not from other obligations. General locality, not universal mark independence of the resulting rows, is proved.
- **Controls:** accepted printed Part B is a special positive case. Part J's half-scale arbitrary pair is not a same-law flip and remains a separate valid nonconvexity counterexample.
- **Limits:** No larger horizon, all-size theorem, physical latent sector, law selection, calibrated readout, efficiency or DET physical validation.
- **Gates:** distinct review and coordinator disposition; protected validation/custody, ABSTAIN, Status M, zero qualification, RET-only pause, speculative Boundary separation and physical/execution gates unchanged.

## L. Five births obstruct equal self-orbit symmetrization

**Dependencies and review.** This counterexample received distinct mathematical review and coordinator acceptance. Its finite admission uses the accepted maximal-deletion identity and extension-sufficiency premise of Parts A and D; a necessity-only parameterization would not suffice. The construction retains the printed seed only through parent size two, modifies parent-three rows and defines the complete parent-four layer before taking the law’s own global mark flip. The first-failure-at-five-births conclusion also depends on Part K’s closure theorem for the stated four-birth class.

**Accepted result: conditional explicit counterexample.** In the admitted model, equal whole-law averaging with a law's own global mark flip need not preserve selected-mark locality at N=5. The construction below specifies every row through parent size four. It uses the accepted maximal-deletion compatibility theorem, not an unverified coefficient vector. Together with accepted Part K, five births is the first failure horizon in the stated class with the empty row and singleton row (2/3,1/3) fixed.

### 1. Exact finite component

All marks are immutable and independently fair at birth. For each actual ideal S of marked parent (P,r), the complete branch is q(P,r,S) times the identity payload map, divided by two. A proper slot may read the whole unmarked parent and marks only in S.

Retain the accepted printed rows through parent size two:

- Empty parent: its sole ideal has probability 1.
- Singleton: empty/full probabilities 2/3,1/3.
- Two-chain, minimum mark i: empty/root/full probabilities c,f_i,h_i.
- Two-antichain: empty/two actual singleton/full probabilities d,g,g,k.

Here
\[
c=1/5,\quad d=1/4,\quad g=1/10,\quad k=11/20,
\quad f_0=1/6,\ f_1=1/3,\quad h_0=19/30,\ h_1=7/15.
\]
Every lower entry lies in [1/10,1].

For a proper ideal define the accepted potential, using the already specified smaller rows of this very component:
\[
u(P,r,S)=\prod_{\varnothing\ne A\subseteq K}
q(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}},
\qquad K=\operatorname{Max}(P)\setminus S.
\]
Smaller full occurrences use their actual full complements.

Put
\[
\alpha=1/30000,\qquad \epsilon=1/300000000,\qquad
\beta=\epsilon^7/32.
\]
At every size-three parent define
\[
q(P,r,S)=\alpha\,t(P,r,S)u(P,r,S)\quad(S\subsetneq P),
\]
where t=1 except when P is the three-chain x<y<z and S={x,y}; there t=1+r_y. Thus the exceptional multiplier is 1 or 2 and depends only on selected marks. Define every full entry by the complete normalization complement.

At every size-four parent define
\[
q(P,r,S)=\beta u(P,r,S)\quad(S\subsetneq P),\qquad
q(P,r,P)=1-\sum_{S\subsetneq P}q(P,r,S).
\]
This is a complete finite definition, over all orders, markings and actual ideals. No table search or coefficient optimization is required. The constants are conservative existence witnesses, with no optimality claim.

### 2. Complete admission

**Support and full mass.** A proper ideal omits some maximal vertex, so K is nonempty. All factors are positive. At size three, at most four positive-exponent and three negative-exponent factors occur. The lower bound 1/10 therefore gives
\[
10^{-4}\le u\le10^3.
\]
There are at most seven proper actual ideals. Consequently every size-three proper entry is at least epsilon, and their complete sum is at most
\[
7(2\alpha10^3)=7/15.
\]
Every size-three full entry is at least 8/15. Thus all rows through size three have entries in [epsilon,1].

At size four, at most seven negative-exponent factors occur, so u<=epsilon^{-7}. At most fifteen proper ideals give total proper mass at most 15/32. Every full complement is at least 17/32. All proper entries are positive, every actual ideal is included, and every complete row sums to one.

**Locality and equivariance.** Every smaller factor reads only marks in S: if S is proper this follows from lower locality; if S is full in a deletion parent, that parent is exactly S. The exceptional multiplier reads y in S and uses intrinsic chain positions. Hence proper locality holds at size three and then size four. Deletion subsets, chain positions and actual ideals transport under relabeling, so all rows are equivariant. Full complements retain the model's permitted full-mark dependence.

**Diamonds through four births.** First consider the size-three proper rows alpha*u without the exceptional multiplier, with full complements. The accepted potential identity and common scaling prove every new diamond from a size-two base. Their full complements are positive by the same bound.

Now apply t only to the initial-pair slot of a three-chain. If this slot occurs as a second precursor in a diamond, the intermediate parent is x<y<z and the first newborn must be its unique maximum z. The base is exactly x<y; both precursors must be the full base {x,y}. Thus the other route also uses the initial-pair slot of a three-chain with the same inherited mark r_y. Both routes acquire exactly the same multiplier 1+r_y, for every inherited marking and both newborn bits. No other diamond has a changed second slot. Changed size-three full entries cannot be second precursors of these incomparable births. Earlier diamonds are unchanged.

This covers equal precursors, empty/full base ideals and every old/newborn marking; it is not a claim based only on normalized endpoint probabilities.

**Diamonds through five births.** The modified prefix is now admitted through four births. The accepted potential theorem applies to this prefix. In every new diamond from a size-three base its identity is
\[
q(C,r,S)u(C+S,r+b,T)
=q(C,r,T)u(C+T,r+c,S).
\]
Multiplying both sides by the common beta proves the size-four transition diamonds. Both second precursors are proper, including equal/full base precursors. The support and complement bounds above meet the extension hypotheses.

Fair splitting gives the same factor 1/4 on both routes, with identical transported identity maps on arbitrary positive-semidefinite complex payloads. Complete one-step maps sum to identity. No payload restriction or normalized-state substitution occurs.

Thus q is an admitted N=5 law, conditional only on the explicitly accepted potential theorem.

### 3. Exact failure for this law and its own flip

Fix this q completely, and only then set q^F(P,r,S)=q(P,1-r,S). Flipping transports all admission conditions, including fair bits and the unchanged zero/one-parent prefix.

Take P to be the four-chain x<y<z<w and select the proper ideal S={x}. Write i=r_x, j=r_y. For the three-chain prefix, deletion of its unique maximum gives
\[
q_3(\varnothing)=\alpha c,\quad q_3(\{x\})=\alpha f_i,\quad
q_3(\{x,y\})=\alpha(1+j)h_i,
\]
so its full probability is
\[
H_{ij}=1-\alpha(c+f_i+(1+j)h_i)
      =1-\alpha-\alpha jh_i.
\]
The four-chain's per-encoding structural prefix weight is
\[
w(i,j)=h_iH_{ij}/3.
\]
Its actual marked mass is 2^{-4}w(i,j). This total order has a unique natural order encoding; no factorial or duplicate orbit weight appears.

Let A=1-alpha and B_i=A-alpha*h_i. Choose markings
r=(0,0,0,0) and r'=(0,1,0,0).
They agree on S. Their equal-mixture posterior weights are
\[
\omega_{00}=\frac{h_0A}{h_0A+h_1B_1},\qquad
\omega_{01}=\frac{h_0B_0}{h_0B_0+h_1A}.
\]
All quantities are positive. Their exact difference is
\[
\omega_{00}-\omega_{01}
=\frac{h_0h_1(A^2-B_0B_1)}
{(h_0A+h_1B_1)(h_0B_0+h_1A)}>0,
\]
because
\[
A^2-B_0B_1
=\alpha A(h_0+h_1)-\alpha^2h_0h_1>0.
\]
For example, A>1/2, h_0+h_1=11/10, h_0h_1<1 and alpha<1/2 give a strictly positive bracket.

Deleting the four-chain maximum in the root slot gives
\[
q(P,r,S)=q(P,r',S)=\beta\alpha f_0,\quad
q^F(P,r,S)=q^F(P,r',S)=\beta\alpha f_1.
\]
The uniquely reconstructed kernel of the equal whole-law mixture is
\[
\bar q(P,r,S)=\beta\alpha\left(\frac13-\frac{\omega_{00}}6\right),
\qquad
\bar q(P,r',S)=\beta\alpha\left(\frac13-\frac{\omega_{01}}6\right).
\]
Their difference is exactly
\[
-\frac{\beta\alpha}{6}
\frac{h_0h_1(A^2-B_0B_1)}
{(h_0A+h_1B_1)(h_0B_0+h_1A)}<0.
\]
Thus this proper slot reads the unselected mark r_y after averaging. Selected-mark locality fails. Both component values and both posterior weights are exact, with explicitly defined positive rational constants.

The accepted whole-law reconstruction result preserves the other mixture conditions and makes this kernel unique. An alternative admitted kernel cannot realize the same complete mixture while repairing the failed slot.

### 4. Boundary and evidence

Part K applies to this component's four-birth restriction despite its changed parent-three rows; all self-orbit averages through N=4 remain admitted in the declared class. The failure occurs at the next transition. Part J's earlier arbitrary-pair nonconvexity remains distinct: here the second component is exactly the first law's own flip, with no independent rescaling.

This is a finite conditional counterexample, not an all-size result, scientific execution, law-selection principle or physical prediction. It rejects universal self-orbit closure at N=5, not the existence of particular symmetric laws.

Part A supplies the admitted potential/extension premise; Parts A, B, D, H, I and J supply the seed, construction conventions and mixture criterion; Part K establishes accepted N4 closure. The potential identity and extension-sufficiency premise remain explicit dependencies.

### 5. Premises and proof obligations

#### Admitted premises

1. The finite marked-order model in Part A: every actual ideal has positive mass; complete rows normalize; newborn bits are independently fair; proper slots read only selected marks; full slots may read all old marks; equivariance and complete transported marked diamonds are required; payloads are arbitrary complex positive-semidefinite objects acted on by scalar identity branches.
2. The printed empty/singleton/two-parent seed is accepted. Only its rows through parent size two are retained. Historical parent-three or parent-four coefficients are NOT imposed.
3. The maximal-deletion potential theorem is accepted, including its sufficiency statement: for an admitted smaller prefix its potential satisfies every inherited marked ratio identity, and a sufficiently small common positive scale with positive full complements supplies compatible next-layer rows. Merely knowing that solutions must have a component form would not suffice. This theorem is not re-proved here.
4. Accepted Parts H/I/J give the common lift, prefix-conditioned mixture kernel, automatic preservation of all finite mixture conditions except locality, and reconstruction uniqueness. The exact locality difference is (v-vF)(omega(r)-omega(rprime)).
5. Accepted Part K is the full N4-class closure result with fixed parent0/1 prefix.

#### New construction, not an assumed coefficient witness

- Define alpha=1/30000, epsilon=1/300000000 and beta=epsilon^7/32 exactly.
- Compute the mathematical size-three potential from the retained seed. On every proper slot multiply by alpha. Additionally multiply just the three-chain initial-pair slot by 1+r_y, where y is its second vertex. Every full entry is the complete complement.
- Compute the mathematical size-four potential from these modified smaller rows, including actual smaller full complements. Multiply every proper slot by beta and use the full complement.
- These formulas specify all allowed finite rows. No numerical potential evaluation, enumeration, optimization or unlisted coordinate is assumed.

#### Admission discharged manually

- Lower entries belong to [1/10,1]. At size three at most four numerator and three denominator factors imply 10^-4 <= u <= 10^3. At most seven proper occurrences and multiplier <=2 imply total <=7/15; full >=8/15. Every proper entry >=epsilon.
- All smaller entries then belong to [epsilon,1]. At size four at most seven denominator factors imply u<=epsilon^-7. At most fifteen proper occurrences give total <=15/32; full >=17/32.
- A proper ideal omits a maximal vertex. All deletion factors are defined and positive. Full factors read only selected marks because their remaining parent equals that ideal.
- Intrinsic chain positions and deletion sets are equivariant. The exceptional multiplier reads only a selected old mark.
- The common-alpha size-three reference obeys the admitted potential identity. A changed initial-pair second slot forces the base to be a two-chain with both precursors equal to the full base. The two routes get the same inherited multiplier. All other diamonds are unchanged. Recomputed size-three full entries cannot be second precursors at this horizon.
- The modified prefix therefore qualifies for the accepted size-four potential identity. Common beta preserves every new diamond, with all old/new marks and empty/full/equal precursor cases.
- Independent fair bits and the common factor 1/4 yield complete unnormalized identity-map diamonds on all payloads, and normalized complete rows sum to the identity map.

#### Failure discharged manually

For the four-chain x<y<z<w, selected ideal {x}, the component prefix weight is h_i(1-alpha-alpha*j*h_i)/3. The q/qF posterior therefore changes between marks0000 and0100, although the selected mark is fixed. Both component root slots equal beta*alpha*f_i; the flipped value uses f_(1-i). Since f0 != f1 and the posterior difference is strictly positive, the exact mixed root-slot difference is strictly negative as displayed in Section 3 above.

All factors are per natural encoding, with the common fair factor2^-4. The chain has unique natural order encoding. The global flip changes all four bits, but the formulas depend only on the first two. The second law has no independent alteration.

#### Scope and stopping

The conditional N5 counterexample and the accepted universal N4 result together establish the first failure horizon in this declared class. No classification of later horizons, all-size symmetrization, optimal constants, efficient algorithm, native physical selector, calibrated observation, geometry or DET physical validation follows.

Scientific/custody/independent-review/ABSTAIN/Status M/zero-qualification/RET-only/Boundary/execution gates remain.

## M. Four endpoint masses expose locality failure

**Dependencies and review.** This endpoint witness received distinct mathematical review and coordinator acceptance. It translates the fixed finite counterexample in Part L using the common-lift and mixture results of Parts H/I/J. The counterexample's conditional extension premise remains separate from the encoding conversion. Exact compatible probability laws and immutable role marks are supplied mathematical inputs, without a physical readout or empirical-frequency claim.

**Accepted result.** Four normalized marked endpoint-class probabilities at horizons four and five give an exact signed witness for the accepted Part L midpoint. The witness is strictly negative, whereas selected-mark locality requires zero. After forgetting all marks, that midpoint has exactly the same entire finite unmarked-history law as its admitted component through five births. Thus even complete unmarked data cannot distinguish these two laws.

### 1. Endpoint events and the information retained

Write pi_n(C) for the unconditional probability of a marked order isomorphism class C after n births. Each pi_n is normalized on its entire endpoint space; the horizons belong to the same consistent finite law. Isomorphisms preserve the binary mark names and transport marks on vertices.

For j=0,1 define P_j to be the four-chain
\[
x<y<z<w,\qquad (r_x,r_y,r_z,r_w)=(0,j,0,0).
\]
Define Q_j by adding v with strict past exactly {x}, mark r_v=0, and no other new comparisons. Its covering relations are
\[
x<y<z<w,\qquad x<v.
\]
The selected ideal in P_j is S={x}; both parent markings agree on S. The declared fifth-birth bit is zero.

All names here denote intrinsic order roles, not observed birth labels. In Q_j, x is the unique minimum. Of the two maximal vertices, v has one strict predecessor and w has three. The remaining y,z are fixed by the long chain. Consequently the short leaf v and its deletion to the four-chain are identifiable from the endpoint order itself. The marked events Q_0,Q_1 differ at y, not at an interchangeable leaf. No extra distinguished embedding is supplied.

The four required masses are
\[
p_j=\pi_4(P_j),\qquad c_j=\pi_5(Q_j)\quad(j=0,1).
\]
They retain exact order type and all specified role marks. They are not probabilities conditioned on selecting one of these four events.

### 2. Multiplicity and the endpoint-to-slot identity

A four-chain has exactly one abstract linear extension and trivial automorphism group, so P_j has one distinct natural encoding.

For Q_j the root must come first. The remaining y,z,w must keep their chain order; v can occupy any one of four positions:
\[
(x,v,y,z,w),\quad (x,y,v,z,w),\quad
(x,y,z,v,w),\quad (x,y,z,w,v).
\]
These exhaust the extensions, since v is incomparable with each of y,z,w. The intrinsic-role argument above proves the unmarked automorphism group is trivial. Therefore its mark-preserving subgroup is also trivial for both j. The accepted encoding formula e(Q)/|Aut(Q,r)| gives exactly four distinct encodings, even for Q_0 with all marks zero. There is no factorial or additional orbit factor.

Complete marked diamonds equate these four history probabilities: adjacent exchanges of v with an incomparable chain vertex transport each bit with its vertex, including the j=1 case. Equivariance transports the remaining suffix. This equal-weight argument does not use selected-mark locality.

For an admitted law, the unique P_j history followed by (S,bit0) is precisely the last listed Q_j encoding. Its probability is p_j*q(P_j,S)/2. Hence
\[
c_j=4\left(p_j\frac{q(P_j,S)}2\right)
=2p_jq(P_j,S),\qquad q(P_j,S)=\frac{c_j}{2p_j}. \tag{1}
\]
The endpoint masses already include all fair-bit factors. Division by four recovers one encoding; multiplication by two recovers a structural ideal probability from a declared bit branch. Neither factor is inserted twice.

The same identity holds for the Part L whole-law midpoint: each component is constant on every encoding fiber, and their fixed convex mixture remains constant there. Its positive prefix-conditioned kernel retains fair bits and diamonds even though locality fails. Thus (1) does not assume the property being tested.

Selected-mark locality requires the two recovered root-slot probabilities to coincide. Since p_0,p_1>0, its exact necessary endpoint equality is
\[
\boxed{W:=c_0p_1-c_1p_0=0.} \tag{2}
\]
This is a test of one locality constraint, not a complete admission criterion for arbitrary endpoint tables. Consistency, support, fair bits and the common-lift assumptions remain explicit.

### 3. Exact value for the accepted midpoint

Use precisely the Part L component q, then its own global flip q^F, and their equal whole-law mixture. No row or event is changed. The accepted constants are
\[
\alpha=1/30000,\quad \epsilon=1/300000000,\quad
\beta=\epsilon^7/32,\quad
f_0=1/6,\ f_1=1/3,\quad h_0=19/30,\ h_1=7/15.
\]
Put A=1-alpha and B_i=A-alpha*h_i. The accepted component's four-chain structural weight is
\[
w(i,j)=h_i(1-\alpha-\alpha jh_i)/3.
\]
Its per-encoding marked probability is 2^{-4}w. The component root-slot values are beta*alpha*f_0 at both P_j, and beta*alpha*f_1 for its flip.

For the midpoint, the four unconditional endpoint masses are therefore
\[
p_0=\frac{h_0A+h_1B_1}{96},\qquad
p_1=\frac{h_0B_0+h_1A}{96},
\]
\[
c_0=\frac{\beta\alpha}{48}
(f_0h_0A+f_1h_1B_1),\qquad
c_1=\frac{\beta\alpha}{48}
(f_0h_0B_0+f_1h_1A). \tag{3}
\]
The parent denominator 96 is 3*16*2: the structural 1/3, four fair bits and the equal mixture. For a child, append its fair bit and root-slot factor to each parent component, average the components, then sum its four equal encodings. This gives denominator 48 in (3), with all complementary endpoint classes left in the normalized law.

Cross-multiplication now gives
\[
\begin{aligned}
W
&=\frac{\beta\alpha(f_0-f_1)h_0h_1}{4608}
 (A^2-B_0B_1)\\
&=-\frac{\beta\alpha h_0h_1}{27648}
 (A^2-B_0B_1)<0.
\end{aligned}\tag{4}
\]
Indeed
\[
A^2-B_0B_1
=\alpha[A(h_0+h_1)-\alpha h_0h_1]>0.
\]
Here A>1/2, h_0+h_1=11/10, h_0h_1<1 and alpha<1/2, making the bracket strictly positive. Every other displayed factor is strictly positive. This is an exact rational signed witness, without numerical estimation.

Equivalently, W=2p_0p_1[qbar(P_0,S)-qbar(P_1,S)], matching the accepted negative slot difference. Each original admitted component separately satisfies (2); the midpoint violates it. The counterexample's admission retains Part L's explicitly conditional maximal-deletion extension premise. The encoding conversion itself uses only the finite common-lift conditions.

### 4. Mathematical channel, not a physical instrument

A sufficient deterministic endpoint channel at horizon four reports P_0, P_1 or “other.” At horizon five it reports Q_0, Q_1 or “other.” Their exact output laws supply the four masses in (2). This is a transparent finite sufficient witness; no global minimality is claimed.

These channels read endpoint order and immutable role marks. They require neither access to a particular realized birth history nor a history-label oracle: the multiplicity proof supplies the conversion algebraically. The two horizon laws must be compatible marginals of the same process. A lone endpoint, finite sample, unknown mark readout or arbitrary pair of probability tables is not this input. No physical instrument, repeated-trial protocol, calibration, detection threshold or sample-size assertion is supplied.

### 5. Exact boundary after forgetting marks

Let mu be the complete natural-history law of the accepted q through five births, F flip every immutable mark, and U erase every mark while retaining the entire underlying natural order-growth history. Then
\[
\mu^F=F_*\mu,\qquad U\circ F=U.
\]
Consequently, for the midpoint mubar=(mu+mu^F)/2,
\[
U_*\bar\mu
=\tfrac12(U_*\mu+(U\circ F)_*\mu)
=U_*\mu. \tag{5}
\]
Equivalently, for every unmarked-history event E,
\[
\bar\mu(U^{-1}E)=\mu(U^{-1}E)=\mu^F(U^{-1}E).
\]
This proof sums the complete mark fibers; it assumes no independence between later order growth and old marks.

The equality retains more information than an unmarked endpoint: it retains every unmarked prefix and actual ideal choice in the natural history. All coarser unmarked endpoint events, unmarked multi-time events and unmarked history statistics through five births therefore agree exactly. Prefix marginals give the same conclusion at every smaller horizon.

In particular, the full unmarked law is shared by the midpoint kernel that violates selected-mark locality and an already admitted local component. No rule using only that unmarked law can distinguish these two cases. The marked witness is therefore not an unmarked prediction. This does not assert that forgetting marks produces a parent-only Markov kernel, and says nothing beyond the defined five-birth horizon.

### 6. Dependencies and scope

Part L specifies the accepted component and its conditional maximal-deletion extension premise. Part H supplies the encoding/common-lift theorem, and Parts I/J supply the finite mixture conditions. The extension premise remains a dependency of component admission; the endpoint conversion uses the finite common-lift conditions separately.

The exact information-sufficiency question is closed at this conditional scope.

### 7. Premises and endpoint witness obligations

#### Inputs and admitted facts

1. The model retains empty start, full positive actual-ideal support, normalized parent-state kernels, immutable fair newborn bits, relabeling equivariance, complete transported marked diamonds and scalar-passive payload. Proper selected-mark locality is the condition being tested.
2. Part H gives natural histories as birth-labeled encodings, equality of all encoding weights within a marked endpoint class, and multiplicity e(C)/|Aut(C,r)|. Mark names are preserved by isomorphisms. Its equality proof requires diamonds and transport, not selected-mark locality.
3. Part L gives exactly the accepted finite component. The accepted counterexample remains conditional on the maximal-deletion compatibility/extension theorem. That underlying theorem is not re-proved or enlarged here.
4. Parts I/J give the positive prefix-conditioned whole-law mixture, fairness, retained diamonds and exact locality residual. Applying the common lift to a mixture is justified also directly: both component probabilities are constant on each same encoding fiber, so their fixed midpoint is constant there.
5. Adjacent endpoint laws at horizons4/5 must belong to one consistent finite process. Four arbitrary normalized numbers would not by themselves establish those model assumptions.

#### New endpoint event definitions

- P_j is the four-chain x<y<z<w with marks(0,j,0,0), for j=0,1.
- Q_j has that chain plus v with strictpast{ x } and bit0, with no other new comparisons.
- p_j=pi4(P_j), c_j=pi5(Q_j) are unconditional masses in fully normalized marked endpoint-class distributions. No selected-support renormalization is used.
- Vertex names are intrinsic roles. In Q, x is unique minimum, v is the maximal vertex with one predecessor, w is the maximal vertex with three, and y/z are the intermediate long-chain roles. Thus the indicated parent embedding is recoverable from the endpoint shape, without an added distinguished label.
- In both parents the selected ideal{x} has mark0. The changed parent mark is at y outside the selected ideal. Q_1 retains that same role change while the declared new bit remains0.

#### Counting and conversion proved manually

- P_j has e=1, trivial automorphisms and one natural encoding.
- Q_j has exactly four linear extensions: rootfirst, the ordered triple y,z,w, and v inserted in any of four positions. Its intrinsic roles force every order automorphism to be identity, so its marked automorphism group is identity for both j. Thus e/|Aut|=4, including all-zero Q_0.
- Adjacent swaps of v with incomparable y/z/w transport their marks. Complete marked diamonds and equivariance equate all four history weights, including j=1. Convex mixing preserves that equality.
- The encoding with v last has probability p_j*q(P_j,{x})/2. Endpoint mass is four times that probability. Hence c_j=2p_j*q(P_j,{x}) and q=c_j/(2p_j). All existing fair factors are already inside endpoint masses; the single factor2 only removes the specified newborn-bit split.
- Locality requires W=c0*p1-c1*p0=0. This is one necessary locality equation, not a full admission characterization.

#### Exact evaluation

Retain alpha=1/30000, epsilon=1/300000000, beta=epsilon^7/32, f0=1/6,f1=1/3,h0=19/30,h1=7/15. Set A=1-alpha and B_i=A-alpha*h_i.

For the accepted midpoint:
p0=(h0*A+h1*B1)/96; p1=(h0*B0+h1*A)/96;
c0=beta*alpha*(f0*h0*A+f1*h1*B1)/48;
c1=beta*alpha*(f0*h0*B0+f1*h1*A)/48.

The parent factor96=3*16*2 counts structuralprefix1/3, fourfairbits and midpoint1/2. The child factor48 follows from oneextra fairbit and four distinct terminal encodings. Cross multiplication gives
W=-beta*alpha*h0*h1*(A^2-B0*B1)/27648.
A^2-B0*B1=alpha*[A*(11/10)-alpha*h0*h1]>0 by the explicit bounds. Thus W<0 exactly.

#### Information sufficiency and limitation

The two deterministic mathematical channels each report one of the two specified classes or other. Exact compatible output laws suffice. No global minimality, history oracle, physical mark access, calibration, sampling protocol or statistical accuracy is asserted.

For the entire finite history law, global markflip F preserves the underlying unmarked history U: U composed with F equals U. Therefore the midpoint, q and qF have exactly equal U-pushforwards. This covers every unmarked endpoint/event and every unmarked multi-time/history statistic through five births, including all smaller prefix horizons. It does not assume mark/order independence or a Markov kernel after erasure.

The admitted component and the locality-violating midpoint share this complete unmarked law. Their difference cannot be certified from that projection alone. No all-size or physical-observation claim follows.

## N. Relative marks and an absolute root reference

**Dependencies and review.** This finite channel criterion and witness recovery received distinct mathematical review and coordinator acceptance. Parts L/M fix the component, its own flip, their midpoint and the endpoint witness. The pushforward and relative-bit arguments are finite channel algebra; application to the admitted component retains its conditional extension premise. Reconstruction under separately stipulated midpoint symmetry is distinct from identifying the actual generating law.

**Accepted result.** Any globally flip-invariant deterministic channel gives identical output laws for the fixed component and its midpoint with its own flip, even when it retains complete relative marks and order history. Non-invariance is necessary for discrimination but not sufficient: the fair first bit is a concrete counterexample. On the two intrinsic shapes underlying the four Part M events, relative marks plus the existing absolute root bit recover those events and their four probabilities exactly.

This is a finite mathematical information result through five births, with no new law, horizon or physical instrument.

### 1. Exact channel criterion

Let mu be the accepted component's complete finite natural-history law, F flip every immutable binary mark, and
\[
\mu^F=F_*\mu,\qquad \bar\mu=(\mu+\mu^F)/2.
\]
For a declared deterministic channel C define
\[
\nu=C_*\mu,\qquad \nu^F=C_*\mu^F=(C\circ F)_*\mu.
\]
The midpoint output law is
\[
C_*\bar\mu=(\nu+\nu^F)/2.
\]
Consequently the exact output distributions distinguish mu from its midpoint if and only if
\[
\boxed{C_*\mu\ne C_*F_*\mu.} \tag{1}
\]
Equivalently, some output event B satisfies
\(\mu(C^{-1}B)\ne\mu(F^{-1}C^{-1}B)\).
On the finite image of C,
\[
\operatorname{TV}(C_*\mu,C_*\bar\mu)
=\tfrac12\operatorname{TV}(\nu,\nu^F).
\]
This follows by subtracting the two output probability vectors and taking their absolute sums. “Distinguish” here means unequal exact laws; no sampling or single-observation success claim is included.

If C composed with F equals C pointwise, then nu^F=nu, so the component, flip and midpoint have identical outputs. Pointwise non-invariance is therefore necessary for a distinguishing channel, but it does not ensure the distributional inequality (1).

### 2. Complete relative marks remain invariant

For vertices u,v, define the relative bit
\[
d_{uv}=r_u\mathbin{\oplus}r_v.
\]
Global flipping changes neither d_uv nor any order relation or precursor choice. Thus a channel retaining the entire unmarked natural history and every pairwise relative bit satisfies C composed F=C. The same holds for an endpoint channel retaining its unmarked order and the complete pairwise-bit relation up to transported isomorphism.

This includes much more than erasing all marks. Nevertheless (1) proves exact equality of these relative-information output laws for mu and its midpoint. Any further deterministic coarsening is also unable to distinguish them.

On a fixed nonempty vertex set, complete pairwise relative bits determine a binary marking up to a common flip: choose a vertex x; each r_v equals r_x XOR d_xv. This is a proof of the two possible orientations, not permission to choose an arbitrary observable root on general orders. At the endpoint-class level, automorphisms can sometimes identify the two orientations. No general two-element-orbit or one-bit requirement is asserted for arbitrary orders.

### 3. Non-invariant negative control

Take C_first(h) to be the first newborn bit in the complete natural history. It is also the bit of the singleton endpoint at horizon one. It is not claimed to be recoverable as a distinguished first vertex of every later endpoint.

Pointwise,
\[
C_{\rm first}(Fh)=1-C_{\rm first}(h)\ne C_{\rm first}(h).
\]
Yet the forced empty-parent row has probability one and the first mark is independently fair. Summing every subsequent normalized continuation preserves its marginal:
\[
\Pr_\mu(C_{\rm first}=0)=\Pr_\mu(C_{\rm first}=1)=1/2.
\]
The flip and midpoint have exactly this same marginal. Hence this non-invariant channel fails (1). Future order growth may correlate with this bit; no independence from later geometry or conditional fairness after shape selection is used.

### 4. An equivariant reference construction on the witness shapes

Part M uses P_j, the four-chain x<y<z<w with marks (0,j,0,0), and Q_j, that chain plus v above x alone, marked zero, for j=0,1. Marks and names refer to intrinsic roles.

On the four-chain the unique minimum is x. On Q, x is again the unique minimum; its maximal short leaf v has one strict predecessor while its maximal long-chain endpoint w has three. The intervening y,z are then fixed. Both shapes have trivial unmarked and marked automorphism groups. In particular x is a canonical role, and no leaf exchange or auxiliary embedding is hidden in the definition.

For every marking on either of these two shapes, define
\[
a=r_x,\qquad \delta_v=r_v\oplus r_x,\qquad
C_{\rm ref}([P,r])=([P],\delta,a).
\]
Here delta is an assignment to the transported intrinsic roles, with delta_x=0. The corresponding relative channel drops a. At horizon four use this construction on the chain shape; at horizon five use it on the Q shape. On other shapes report their unmarked shape with a “reference not specified” tag. No root is selected there.

An order isomorphism takes the unique root to the unique root and transports delta with its vertices; a is unchanged by relabeling. Thus the construction is well-defined on endpoint isomorphism classes. It is equivariant before quotienting and involves no birth-label oracle.

On the specified shapes the inverse is exact:
\[
r_v=a\oplus\delta_v.
\]
The data therefore recover every original marked class on those shapes. Under global mark flip, delta stays fixed and a changes to 1-a. “Absolute” here means relative to the declared mathematical names 0 and 1; the existing root bit is read, not a new birth or physical reference added.

For P_j the required output has chain shape, a=0 and role vector delta=(0,j,0,0). For Q_j it has Q shape, a=0 and delta=(0,j,0,0,0), in roles (x,y,z,w,v). Their output probabilities are precisely
\[
p_j=\pi_4(P_j),\qquad c_j=\pi_5(Q_j).
\]
All other events keep their mass; there is no postselection or extra multiplicity. The accepted natural-encoding counts remain one for P and four for Q. Hence the original Part M equality and midpoint failure are recovered unchanged:
\[
W=c_0p_1-c_1p_0,\qquad
W_{\rm admitted}=0,\quad W_{\rm midpoint}<0.
\]
This recovers that specific witness; it is not a full admission test or a globally minimal locality readout.

For a known two-element flip orbit on these shapes, delta identifies the orbit and a separates its two members. Any exact deterministic recovery of orientation on that orbit needs at least two distinguishable tag values; the binary root tag suffices. This is only an outcome-capacity statement for that known orbit, not a Shannon-entropy lower bound, global test minimality or universal physical-reference claim.

### 5. Discrimination and witness recovery are different

The referenced channels actually distinguish this particular component from its midpoint. For example, with the accepted constants
\[
\alpha=1/30000,\quad A=1-\alpha,\quad
h_0=19/30,\quad h_1=7/15,\quad B_1=A-\alpha h_1,
\]
the recovered P_0 event has
\[
\mu_4(P_0)=h_0A/48,\qquad
\bar\mu_4(P_0)=(h_0A+h_1B_1)/96.
\]
Their difference is
\[
\frac{(h_0-h_1)A+\alpha h_1^2}{96}>0.
\]
Thus a referenced horizon-four event already separates these exact laws. The Part M locality witness is a different task: it combines the four specified masses at compatible horizons four and five. No minimal discrimination horizon is claimed. The first-bit control does not contradict this result: the referenced output retains correlations with shape and relative marks that a lone unconditional bit discards.

There is a further qualification. The known midpoint is flip invariant because F is an involution. Let R_j and T_j be relative-channel probabilities of the two-element orbits {P_j,FP_j} and {Q_j,FQ_j}. Their members are distinct because their unique root has opposite named marks. If midpoint symmetry is stipulated, then
\[
\bar\mu_4(P_j)=R_j/2,\quad
\bar\mu_5(Q_j)=T_j/2,\quad
W_{\bar\mu}=(T_0R_1-T_1R_0)/4.
\]
So relative data plus that additional known-law symmetry can reconstruct the midpoint witness without measuring an orientation tag.

But the admitted component produces exactly the same invariant relative data, and need not split either orbit equally. Applying the halving rule to it would infer the midpoint's masses rather than its actual masses. Thus this model-dependent reconstruction does not discriminate the generating law or certify its actual locality from invariant readout alone. The absolute-reference construction instead recovers the named masses directly, without assuming equal orientation weights.

### 6. Missing physical premises and scope

To turn these mathematical channels into a physical readout would require an explicit association between immutable model bits and physical records; access to the stated order relations and intrinsic roles; a stable, calibrated meaning for absolute 0/1 and relative comparisons; and a justified way to obtain compatible endpoint probabilities with controlled readout and sampling errors. None is supplied here. A reference that co-flips and reports only differences remains invariant and does not evade the proposition.

The accepted Part L component retains its maximal-deletion extension premise; Part M's endpoint conversion retains its finite consistency, support, fair-bit and transported-diamond premises. No growth law, support, payload action or horizon changes. No detector, physical reference, clock, native forward map or empirical validation is derived.

Parts L/M give the accepted component and endpoint witness, within the finite common-lift and mixture framework of Parts H/I/J. The generic channel statements and the component's conditional admission retain their distinct premises.

### 7. Premises and readout-information obligations

#### Fixed inputs

- One fixed accepted finite component mu through five births, its own immutable global binary-mark flip F, and midpoint(mu+F_*mu)/2. No independent second component or new law.
- The model has fair newborn bits and normalized complete continuations. The first-bit control uses these facts, without assuming independence from later order.
- Part M gives the accepted four-mass locality witness.
- Parts L/M retain the conditional finite construction and endpoint witness, within the finite common-lift framework of Part H. The maximal-deletion extension theorem remains an admitted premise for the component, not re-proved here.
- The channel statements are elementary finite pushforward statements. No physical mark/reference/calibration or sampling channel is assumed.

#### General proposition and negative control

For deterministic C, put nu=C_*mu and nuF=(C composed F)_*mu. The midpoint outputs(nu+nuF)/2. Therefore unequal component/midpoint output laws occur exactly when nu differs from nuF. Their total-variation distance is one-half TV(nu,nuF). This concerns exact laws, not guaranteed single-trial discrimination.

If C composed F=C, equality follows pointwise. Complete relative bits r_u XOR r_v, together with any unmarked endpoint/order/history information, satisfy this condition. Complete relative bits on a fixed nonempty vertex set leave one common binary orientation; endpoint automorphisms may identify orientations on general shapes.

The first newborn bit is pointwise non-invariant, but both its values have probability1/2 under mu, its flip and midpoint. The empty-parent row is forced and later normalized branches sum to1. This is a full-history channel or the singleton endpoint channel, not a claim of an identifiable first vertex in every later endpoint. No conditional fairness after selecting geometry is asserted.

#### Intrinsic reference construction

Only the two unmarked shapes underlying the four Part M events are used:
P is chain x<y<z<w; Q is P plus v with strictpast{x}. Both have unique minimum x. In Q, the two maxima have respectively1 and3 strict predecessors, fixing v,w; y,z follow from the long chain. Thus both shapes have trivial order and marked automorphisms.

For all markings on those shapes retain(unmarkedshape,delta,a), where a=r_x and delta_v=r_v XOR r_x. Outside them retain only unmarkedshape with an unspecified-reference tag. No arbitrary root choice is made on other orders.

Transport takes root to root and relative assignments with vertices, establishing equivariance and well-definedness on endpoint classes. The inverse r_v=a XOR delta_v recovers every named mark. Under F, delta is unchanged and a flips.

The P_j output is(a0,delta(0,j,0,0)); the Q_j output is(a0,delta(0,j,0,0,0)) in intrinsic roles. Their unconditional probabilities give exactly p_j,c_j. No added branch, factorial, orbit splitting, postselection or altered support occurs. Accepted encoding multiplicities1/4 and W=c0*p1-c1*p0 remain unchanged.

For a known two-element flip orbit in these rigid rooted shapes, delta identifies the orbit and a binary tag distinguishes its two members. Two tag outcomes are necessary only for exact orientation recovery on that orbit. No global locality-test minimality, entropy lower bound or universal physical-reference claim follows.

#### Two distinct information tasks

The referenced channel distinguishes this particular component from midpoint already via P0:
mu4(P0)-midpoint4(P0)
=[(h0-h1)A+alpha*h1^2]/96>0,
with alpha=1/30000,A=1-alpha,h0=19/30,h1=7/15. Its shape/relative-bit correlations are retained; the fair-bit-only control discards them. No earliest discrimination horizon is claimed.

Recovering the Part M locality witness uses four masses at compatible horizons4/5. Direct reference data recover those actual named masses for either law.

If the candidate is independently stipulated to be the flip-invariant midpoint, invariant relative orbit probabilities R_j,T_j can instead be halved to recover its p_j,c_j and W=(T0*R1-T1*R0)/4. Each orbit has two distinct classes because its unique root changes named mark. This symmetry-based inference is conditional on knowing the law's orientation balance. The admitted component has the same relative data but need not split its orbits equally; the rule would reconstruct the midpoint, not its actual masses. Thus relative data alone do not discriminate component/midpoint or certify the actual generating law's locality.

#### Missing physical premises and limits

Physical realization would need: a mapping of model bits to distinguishable physical records; access to order and intrinsic roles; a stable calibrated absolute alphabet and relative comparisons; and compatible probability estimation with controlled errors. No such implementation, reference stability or data protocol is established. A co-flipped reference that only yields differences remains invariant.

All results concern finite mathematical channels through five births. No physical instrument, native forward map, detector, clock, empirical validation, efficiency or new growth law.

## O. A finite noisy-reference calibration contract

**Dependencies and review.** This finite binary-reference channel contract received distinct mathematical review and coordinator acceptance. Parts L/M fix the admitted component and its witness; Part N fixes the root-reference output. The channel algebra is conventional, while application to the component retains the conditional extension premise. Exact discrimination, generic named-mass inversion and reconstruction under a separately stipulated symmetric midpoint remain distinct tasks.

**Accepted result.** A binary symmetric error preserves each orientation-orbit total and multiplies its imbalance by 1-2*eta. Known rates other than 1/2 permit exact inversion; the inverse becomes ill-conditioned near 1/2. Discrimination between the fixed component and its midpoint survives every nonsingular rate, but unknown nonsingular rates do not generally determine the underlying named probabilities. This is conventional finite-channel algebra, not a physical calibration or novelty claim.

### 1. Complete hypothetical readout

Keep the accepted component mu, its own global flip F, midpoint mubar=(mu+F_*mu)/2, and horizons four/five unchanged. Use Part N's reference output on the chain P and root-short-leaf shape Q: unmarked shape, intrinsic root-relative role bits delta, and absolute root bit a. Other shapes retain their unmarked shape and the unspecified-reference tag.

Report shape and delta exactly. Replace a by
\[
\widetilde a=a\oplus E,\qquad \Pr(E=1\mid\hbox{endpoint})=\eta,\quad0\le\eta\le1.
\]
The same eta applies to both bit values, every selected shape/relative pattern, both horizons, and either candidate law. This specifies a hypothetical endpoint-independent flip error; fresh independent errors may be used for separate readouts, but no multi-readout or sampling result is claimed. Unspecified-reference outputs pass unchanged.

This is postprocessing of an endpoint, not a change to growth, marks, branch kernels or payloads. All endpoint masses remain unconditional and normalized; no shape selection is renormalized. The intrinsic roles and trivial automorphisms are those already accepted in Part N.

### 2. Orbit algebra and known-rate inversion

For one known two-member orientation orbit, let x_0,x_1 be its unconditional true masses and y_0,y_1 its reported masses. These are subprobabilities within the complete output law:
\[
\binom{y_0}{y_1}
=K_\eta\binom{x_0}{x_1},\qquad
K_\eta=\begin{pmatrix}1-\eta&\eta\\\eta&1-\eta\end{pmatrix}.
\]
Write k=1-2*eta, m=x_0+x_1 and d=x_0-x_1. Then
\[
y_0+y_1=m,\qquad z:=y_0-y_1=kd.
\]
For known k nonzero,
\[
\binom{x_0}{x_1}
=\frac1k\begin{pmatrix}1-\eta&-\eta\\-\eta&1-\eta\end{pmatrix}
\binom{y_0}{y_1},
\qquad x_{0,1}=\frac{m\pm z/k}{2}. \tag{1}
\]
At eta=1/2 both outputs equal m/2, so arbitrary orientation splits cannot be recovered. The orbit total remains exact.

Rates above 1/2 are not discarded: k is negative, and (1) remains valid. At eta=1 the channel is a deterministic swap. Relabeling the reported bit converts eta to 1-eta only with the corresponding label convention; relabeling alone does not establish the rate or the true absolute orientation.

For known eta, the inverse's induced L1 and infinity norms are 1/|k|: each absolute row/column sum is [(1-eta)+eta]/|k|. Hence, for either norm,
\[
\|\widehat x-x\|\le\frac{\|\widehat y-y\|}{|k|}. \tag{2}
\]
The bound is sharp on antisymmetric errors (t,-t). This is deterministic error amplification, with no sample-size assertion. Negative reconstructed entries indicate incompatible data/rate or estimation error; they must not be silently clipped or reweighted.

With the same exact y and two nonsingular candidate rates,
\[
|x_0(\eta)-x_0(\eta')|
=\frac{|z|\,|\eta-\eta'|}{|k(\eta)k(\eta')|}. \tag{3}
\]
This separates uncertainty about the rate from probability-estimation error.

### 3. Recovering the witness from paired reported outcomes

For each of the four Part M relative patterns P_0,P_1,Q_0,Q_1, retain both reported root outcomes. The corresponding true root-zero masses are p_0,p_1,c_0,c_1. Known nonsingular eta permits (1) on all four pairs, followed by
\[
W=c_0p_1-c_1p_0.
\]
No natural-encoding multiplicity changes: the accepted counts remain one for P and four for Q. Raw noisy root-zero masses generally must not be substituted for these true masses.

If every reported coordinate has absolute error at most e_y, each recovered target mass has error at most e=e_y/|k|. Expanding the two products, using true masses in [0,1], gives the conservative bound
\[
|\widehat W-W|\le4e+2e^2.
\]
This is an algebraic bound, not a physical detection guarantee.

A stipulated flip-invariant midpoint is a special case: each true pair is already (m/2,m/2), unchanged at every eta, including 1/2. Thus its theoretical witness can be reconstructed from orbit totals under that symmetry premise. This does not identify the actual generating law or justify balanced orientation weights for an unknown source.

### 4. Exact distinguishability scaling and its scope

At a fixed horizon n=4 or 5, let rho_n be the noiseless reference-output law of mu. Its midpoint reference law rhobar_n has the same orbit totals, with each orientation pair replaced by (m/2,m/2). Unspecified-reference outputs coincide because they are flip invariant.

On each pair, rho_n-rhobar_n=(d/2,-d/2); K_eta multiplies this difference by k. Summing absolute differences over all pairs, with zero outside contribution, proves
\[
\operatorname{TV}(K_\eta\rho_n,K_\eta\bar\rho_n)
=|1-2\eta|\,\operatorname{TV}(\rho_n,\bar\rho_n). \tag{4}
\]
This exact scaling concerns these reference-output laws with equal orbit totals and one common eta. It is not a formula for arbitrary laws with different orbit totals or for the full hidden-history TV.

The accepted P_0 mass gap makes the horizon-four noiseless TV strictly positive. Hence component-versus-midpoint discrimination as unequal exact output laws survives every eta other than 1/2, and disappears at 1/2. The midpoint output is independent of eta. No finite-sample success or physical detection rate follows.

### 5. Known, unknown and interval-constrained eta

**Known eta.** For eta not equal to 1/2, both discrimination and exact inversion are available under the model; conditioning is given above. At eta=1/2 these two candidate output laws coincide and generic orientation recovery fails. The separately stipulated symmetric-midpoint calculation remains possible from totals.

**Completely unknown eta in [0,1].** Exact orbit totals are still identifiable. Nonzero observed imbalance rejects the midpoint within the two fixed hypotheses, because it always has zero imbalance. Thus an unknown rate does not destroy every possible discrimination. But balanced output is ambiguous: the component with eta=1/2 and the midpoint with that same rate produce identical complete reference-output laws.

Named probabilities are not generally identified by y alone. For example,
\[
y=(3/5,2/5)
\]
is produced both by x=(3/5,2/5), eta=0, and by x=(7/10,3/10), eta=1/4. These are probability-channel controls on one normalized orbit, not claims of admitted local growth laws. They can be scaled to an unconditional orbit mass, with balanced complementary pairs retained, without postselecting an actual endpoint law.

Moreover (x,eta) and (flipped x,1-eta) have the same reported law. For the accepted component and its flip, this is a genuine orientation ambiguity between two admitted components, not a new growth law.

If the component itself is stipulated, its known nonzero orbit contrast d_mu allows k=z/d_mu, and thus eta=(1-z/d_mu)/2. Other pairs must agree with that same k. This is model-conditional parameter inference, not independent physical calibration. Likewise identifying one of two fully stipulated candidate laws can supply its already known probabilities; that is different from inverting arbitrary actual masses without calibration.

**A declared closed interval I=[l,u] excluding 1/2.** Put
\[
\kappa=\min_{\eta\in I}|1-2\eta|>0.
\]
The side of 1/2 is known. Orbit totals, whether an orbit is balanced, and the sign of its true imbalance are identifiable from exact data, with the known sign reversal if I lies above 1/2. For the fixed hypotheses, (4) gives a strictly positive lower separation kappa*TV(rho_4,rhobar_4), so exact discrimination is retained without knowing the numerical rate.

Nevertheless the interval alone does not generally give exact masses: I=[0,1/4] already contains both controls above. The feasible recovery set is
\[
x_{a,o}(\eta)=\frac{m_o+(-1)^a z_o/(1-2\eta)}2,
\quad\eta\in I,
\]
using one common eta across all orbits and both horizons, retaining only rates giving nonnegative probabilities. Extra data constraints may narrow this set; point identification is not guaranteed. This is channel feasibility, not proof of growth-model admission. Bounds (2) and (3) are uniformly controlled by 1/kappa and 1/kappa^2. If an interval merely approaches 1/2 without including it, invertibility is pointwise but no positive uniform kappa follows.

For the four target orbits, the corresponding witness values are exactly
\[
W(\eta)=\tfrac14[
(m_{Q0}+z_{Q0}/k)(m_{P1}+z_{P1}/k)
-(m_{Q1}+z_{Q1}/k)(m_{P0}+z_{P0}/k)].
\]
One must retain that feasible set of values; excluding 1/2 alone is not an exact W inversion. A sign conclusion from the set requires that every feasible value have that sign. Balanced pairs are an exception with exact split m/2 at every nonsingular rate.

### 6. Physical suppliers and closure

The missing suppliers remain explicit: a model-bit/physical-record map; order, intrinsic-role and relative-bit readout; calibration of the absolute-reference error rate and its declared independence/common-rate stability across shapes and horizons; and compatible probability estimation with controlled errors. None is delivered by this algebra or by relabeling a noisy output.

The application retains the accepted component's conditional extension premise and Parts M/N's endpoint-information assumptions. No law, support, horizon or protected gate changes. Parts L/M fix the component and witness, and Part N fixes the reference construction.

This closes the stated toy-channel question.

### 7. Noisy-reference premises and obligations

#### Fixed object and declared channel

The accepted component mu, its own global mark flip, equal midpoint, chain4/root-short-leaf5 shapes, all support and horizons remain unchanged. Part N supplies the accepted reference construction. The component's conditional potential-extension premise remains inherited; it is not re-proved.

The accepted reference output contains exact unmarked shape and root-relative bits, and an absolute root bit on the two rigid shapes. Other shapes retain their unmarked shape and unspecified-reference tag. The hypothetical channel changes only the readout bit, with P(flip|endpoint)=eta in[0,1], the same eta for both orientations, all selected relative patterns, shapes, horizons and hypotheses. This is a conventional binary symmetric postprocessing channel, not a changed growth kernel. Fresh independent readout errors can realize these marginals; no repeated-readout statistical claim is made.

#### Exact algebra

On each two-member orientation orbit, x=(x0,x1) are unconditional true masses, y=K_eta*x, K_eta=[[1-eta,eta],[eta,1-eta]]. Let k=1-2eta, m=x0+x1, d=x0-x1. Then y0+y1=m and z=y0-y1=k*d.

For known k nonzero, x0=(m+z/k)/2, x1=(m-z/k)/2. The inverse matrix is [[1-eta,-eta],[-eta,1-eta]]/k. At half error the channel has rank one, retaining m but discarding orientation. Eta>1/2 is included; eta1 is a swap. Relabeling is a convention change, not calibration.

Inverse induced L1/infinity norms equal1/|k| by absolute row/column sums; antisymmetric perturbations attain it. The same-y rate sensitivity is |z|*|eta-eta'|/|k*k'| per recovered coordinate. Negative inverse entries must not be silently clipped.

For the general paired inversion, retain both reported orientations for each of the four target relative patterns to recover actual p0,p1,c0,c1. This is a sufficient input specification, not a minimality claim; eta=0 or other supplied information can simplify it. Accepted encoding multiplicities1/4 do not change. Known-rate coordinate errors<=e imply W error<=4e+2e^2 by product expansion and true masses<=1. No sampling interpretation is assumed.

#### Discrimination scope

Each reference orbit has equal total under component and midpoint; midpoint orientations are balanced. Their difference on that pair is(d/2,-d/2). The channel multiplies it by k; all unspecified-tag differences vanish. Therefore TV of these noisy reference-output laws is |k| times their noiseless reference-output TV at each horizon. This is not asserted for arbitrary probability laws with unequal orbit totals or for full underlying-history TV.

The accepted P0 difference makes horizon4 reference TV positive. Fixed component/midpoint output laws differ exactly when eta!=1/2. Unknown numerical eta does not prevent distinguishing nonzero observed imbalance from the midpoint's zero imbalance, but allowing half error creates an exact overlap.

#### Calibration cases and classified controls

Known eta!=1/2 gives exact inversion, with unstable amplification near half; eta1/2 gives no generic orientation inverse. A separately stipulated symmetric midpoint is balanced before noise and its masses remain recoverable from totals for every rate; this does not identify the actual generator.

Unknown eta: pair totals remain exact; imbalance only identifies the product k*d. y=(3/5,2/5) arises from x=(3/5,2/5),eta0 and x=(7/10,3/10),eta1/4. These are channel-level probability controls, NOT asserted admitted local growth laws. They can be embedded with common scaled orbit mass and balanced complementary pairs. The actual admitted component/flip pair also has ambiguity (x,eta) versus(flipped x,1-eta).

Stipulating the component permits conditional eta inference from any known nonzero d_mu and exact observed z, with consistency across pairs. Stipulating the midpoint permits balanced splitting. Neither is independent physical calibration or law-independent inversion.

For closed I excludinghalf, kappa=min_I|1-2eta|>0. Totals, balance/nonbalance and sign corrected for the known side ofhalf are identifiable; exact hypothesis separation is bounded below by kappa times positive horizon4 noiselessTV. Exact masses generally are not identified: I=[0,1/4] contains both abstract controls.

Use the single common eta across all pairs/horizons and retain the feasible family x_a,o(eta)=(m_o+(-1)^a*z_o/k)/2 with nonnegative entries. This is only output-channel feasibility, not growth admission. It may narrow with further exact data; no generic point-identification claim. Uniform inverse bounds are1/kappa and rate-sensitivity coefficient1/kappa^2. An open interval approachinghalf has no such uniform separation despite pointwise invertibility.

W values follow by substituting those four candidate root-zero masses into c0*p1-c1*p0. Sign claims require the whole feasible set to have that sign; excludinghalf alone is not exact witness inversion. Balanced pairs are exact m/2 exceptions for nonsingular rates.

#### Missing suppliers and limits

Physical use still lacks bit-to-record mapping; order/role/relative-bit access; calibrated reference error and independence/stability assumptions; compatible probability estimation/error control. Exact algebra supplies none of these.

## P. Finite maximal-deletion identity and sufficient extension

**Dependency and scope.** This proof starts from an admitted smaller prefix in the declared positive scalar-passive binary-marked-order model. It supplies the finite identity and sufficient common-scale extension used in Part L at parent sizes three and four, conditional on each incoming prefix being admitted. Part L's seed, exceptional-slot, complement, mixture, reconstruction and four-birth premises retain their separate status. Earlier Parts A–O remain unchanged.

Status: mathematics accepted following timely distinct independent review and coordinator adjudication. Author procedure: **NONCOMPLIANT**; substantive drafting exceeded its cutoff by **65 seconds**. Mathematical reuse does not retroactively extend or waive that budget. Manual symbolic reasoning only. This proves the finite identity and the common-scale sufficiency needed by Part L; it does not prove the full ratio-component classification.

### 1. Premises and source boundary

Fix a nonnegative parent size n. Rows on every marked parent of size less than n are given in the scalar-passive model stated here: all actual ideals have positive probability, complete rows normalize, proper slots read only selected marks, full slots may read all inherited marks, probabilities are equivariant, and every available complete transported marked diamond holds. Newborn bits are independently fair and branch maps are q/2 times the identity on arbitrary complex positive-semidefinite payloads. “Available” means both transition rows lie in the given prefix.

This note supplies a standalone finite argument, without claiming historical novelty or that the theorem was previously unproved. Part L explicitly needs sufficiency, not merely a necessary parameterization.

### 2. Derive the smaller endpoint weights

For a concrete marked order Q with at most n vertices, define w(Q,r) by multiplying structural probabilities q along any linear extension of Q, starting with w(empty)=1. Do not include the fair-bit factors in w. Each birth uses its actual strict past, an eligible ideal; all rows used have parent size less than n.

This definition is independent of the chosen linear extension. Two linear extensions are connected by adjacent swaps of incomparable vertices: take the first vertex of the target extension, move it left past the vertices preceding it in the other extension, and repeat on the remaining induced order. Those crossed vertices are incomparable with it, since the target first vertex is minimal. The same argument applies inductively after the common prefix.

For one such adjacent swap, the existing base C has size at most n-2. The two strict pasts S,T are ideals of C; the vertices swapped are not in each other's past. The assumed lower-prefix diamond gives

q(C,r,S)q(C+S,r+b,T) = q(C,r,T)q(C+T,r+c,S).

The inherited marks and the two arbitrary newborn bits travel with their vertices. Complete scalar-map equality yields this equality after cancelling the common factor 1/4. After the pair, both orders and markings are identical under the natural transport, so equivariance gives identical suffix factors. Thus the whole products agree.

Consequently w is positive, well-defined and equivariant. In particular, whenever R has fewer than n vertices and Q=R+x has strict past S for x,

\[
q(R,r,S)=\frac{w(Q,r+b)}{w(R,r)}
\tag{1}
\]

for either bit b. Choose a linear extension placing maximal x last to obtain (1). This is a derived finite path-independence statement, not an added history-independence premise. The probability of one marked natural encoding is \(2^{-|Q|}w(Q,r)\); no endpoint multiplicity, automorphism factor or factorial is introduced.

### 3. A symmetric deletion product

Let P have size n≥1 and let S be a proper ideal. Put M=Max(P)\S. This set is nonempty: an omitted vertex has a maximal successor, which must also be omitted because S is downward closed. Removing any nonempty subset A of M leaves S as an ideal in a smaller parent, so every factor in

\[
u(P,r,S)=
\prod_{\varnothing\ne A\subseteq M}
q(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}}
\tag{2}
\]

exists and is positive. Smaller full slots are used exactly as given.

Append y with past S and an arbitrary bit and call the resulting marked order D. Its maximal set is precisely M∪{y}. A previous maximum in S lies below y, and an omitted previous maximum remains maximal. Thus D has at least two maxima.

Define an auxiliary symmetric product only from already defined endpoint weights:

\[
H(D)=
\prod_{\varnothing\ne B\subseteq\operatorname{Max}(D)}
w(D\setminus B)^{(-1)^{|B|+1}}.
\tag{3}
\]

All markings in this formula are induced restrictions. Every argument has at most n vertices; the empty endpoint has weight one. No weight, transition or law at the new terminal size n+1 has been assumed.

For each nonempty A⊆M, equation (1) gives

\[
q(P\setminus A,S)
=\frac{w(D\setminus A)}
       {w(D\setminus(A\cup\{y\}))}.
\tag{4}
\]

The birth of y is legal after these deletions and retains precisely past S. Substitute (4) into (2). Multiplying by w(P)=w(D\{y}) proves

\[
w(P)u(P,S)=H(D).
\tag{5}
\]

Here is the complete exponent accounting, including arbitrarily many omitted maxima. The nonempty subsets B of M∪{y} partition into {y}, nonempty A⊆M, and A∪{y} with nonempty A⊆M. The first contributes exponent +1 from w(P). The second contributes \((-1)^{|A|+1}\) from the numerator. The third contributes its negative, \((-1)^{|A|}=(-1)^{|B|+1}\), from the denominator. These are exactly all factors of (3), once each. There is no additional cycle or gluing assumption.

### 4. The required identity

Let C have size n-1, with arbitrary inherited marks, and let S,T be any two ideals of C. Append incomparable x,y with pasts S,T and arbitrary bits b,c. Write P_x=C+x, P_y=C+y and let D be their common marked terminal order.

Each second precursor is proper because it excludes the other newborn. The terminal D has at least two maxima. Equations (1) and (5), using the same concrete marked D, give

\[
\begin{aligned}
q(C,r,S)u(P_x,r+b,T)
&=\frac{w(P_x)}{w(C)}\frac{H(D)}{w(P_x)}\\
&=\frac{H(D)}{w(C)}\\
&=q(C,r,T)u(P_y,r+c,S).
\end{aligned}
\tag{6}
\]

All w values and their path independence used only rows below n and diamonds with base size at most n-2. Equation (6) therefore does not assume the new diamond it proves.

Nothing in the subset partition or this argument requires distinct, nonempty or proper base precursors. It includes S=T, either empty precursor, either full-base precursor, and S=T=C. In the latter case the two newborns remain incomparable above the base. Full smaller-parent factors and all their induced marks remain in (4). Both arbitrary newborn bits and every inherited marking were retained throughout.

### 5. Sufficient common-scale extension

The potential u is finite and positive. Each factor reads only marks in S: lower proper-slot locality gives this when S is proper in P\A; if S is full there, the remaining parent equals S. Hence u has proper-slot selected-mark locality. Equivariance follows from transporting maxima, deletion subsets, ideals and marks together.

There are finitely many orders on a fixed n-element label set, finitely many binary markings and finitely many actual ideals. Define the whole-layer quantities

\[
U(P,r)=\sum_{S\subsetneq P,\ S\ \mathrm{ideal}}u(P,r,S),
\qquad K_n=\max_{P,r}U(P,r).
\]

For n≥1, \(0<K_n<\infty\). Every actual ideal occurrence enters the sum; this is not a sum over symmetry classes. Choose any \(0<a_n<1/K_n\), and set

\[
q_n(P,r,S)=a_nu(P,r,S)\quad(S\subsetneq P),\qquad
q_n(P,r,P)=1-a_nU(P,r).
\tag{7}
\]

For example \(a_n=1/[2(1+K_n)]\) makes every full complement greater than 1/2. All entries are positive, complete rows normalize, and locality and equivariance hold. Full complements may depend on every old mark, as permitted. No row-independence assumption is needed.

Every new incomparable-birth diamond has base size n-1. Both second precursors exclude the first newborn, so neither is the full intermediate parent. Thus each side of (6) receives exactly the same factor a_n. New full complements do not enter these diamonds; later extension steps will use them as actual smaller-parent inputs. Earlier diamonds are unchanged.

The two fair branches contribute the common factor 1/4 and the same transported identity map on every allowed complex payload. Complete one-step maps sum to identity because each structural row sums to one and the two newborn probabilities sum to one. This establishes the required complete unnormalized marked-map diamonds.

### 6. Boundary layers and the N5 dependency

At n=0 the empty parent has only its full ideal, with q=1. There are no proper slots and no extension diamond; no nonempty-maximal-set assertion is made.

At n=1, the only proper singleton ideal is empty and its potential is q(empty,empty)=1. The only base is empty, with S=T=empty. Both routes have structural product a_1 for every pair of bits. Any common \(0<a_1<1\) is allowed. In particular a_1=2/3 retains the prescribed singleton row (2/3,1/3); the illustrative half-scale choice is not mandatory.

Part L first uses a common-alpha potential at parent size three, then changes only the three-chain initial-pair slot by 1+r_y and separately checks its diamonds. It next applies a common-beta potential at parent size four. The proof here supplies the identity and sufficient-extension premise at both uses, provided each incoming prefix satisfies the stated model. Part L's separately established seed, exceptional-slot check, and explicit positive-complement bounds remain necessary. Its conservative alpha and beta need only satisfy those bounds, not equal the illustrative half-scale.

No earlier acceptance is rewritten. Following distinct review and coordinator acceptance, this proof replaces the opaque identity/sufficiency dependency with a self-contained derivation in the declared model. It does not re-review the entire N5 counterexample or discharge its other reconstruction and N4 premises.

### 7. Exact scope

The yield is a finite theorem: every admitted smaller prefix has the stated maximal-deletion identity and a positive common-scale extension by (7). No additional local consistency axiom was required.

Not established: necessity or classification of all component solutions; unique DET law selection; a uniform scale or quantitative all-size bound; asymptotic geometry; informative quantum evolution; physical calibration or empirical correspondence. The scalar-passive model itself remains an admitted model, not a derivation of quantum mechanics.

Protected validation, independent review, ABSTAIN, Status M, zero qualification, RET-only pause and Boundary separation remain unchanged.

### 8. Premises and proof audit

Status: mathematics accepted with the author-procedure qualification stated above. The self-contained proof is given in Sections 1–7.

#### Assumed, not newly derived

- The complete finite marked-order model and smaller-prefix admission stated in Section 1: all actual ideals eligible with positive normalized rows; immutable binary marks; proper-slot selected-mark locality; permitted full-mark dependence of full slots; equivariance; complete transported diamonds for all available lower rows; independent fair newborn bits; scalar identity branches on arbitrary complex positive-semidefinite payloads.
- Each finite order can be built by any linear extension using its strict-past ideals. This follows directly from the declared birth rule and complete support.
- For the N5 application, the accepted lower seed and Part L's separate exceptional-slot and complement arguments remain premises. Its mixture/reconstruction and N4 results are not re-proved.
- Model admission does not establish physical DET necessity, an empirical instrument, or informative quantum dynamics.

#### Discharged manually, without scientific code

1. Adjacent incomparable swaps connect linear extensions by moving the target first minimal element left, then induction.
2. Each swap uses a lower diamond based on at most n-2 vertices, with all endpoint marks carried on their vertices; suffix factors agree by equivariance. Structural endpoint weights w through size n are therefore derived and positive.
3. A smaller transition is the ratio of its derived endpoint weights; per-encoding fair factors are separate.
4. A proper ideal omits a maximum. Deletion subsets outside it preserve its ideal status; smaller full slots keep their actual marks.
5. Adding a vertex with that past makes terminal maxima exactly the omitted maxima plus the newborn.
6. The complete partition of nonempty maximal-deletion subsets, with explicit numerator/denominator signs, yields w(P)u(P,S)=H(D).
7. The same symmetric H(D) on both routes gives the required new diamond for arbitrary inherited/newborn marks, empty/full/equal precursor cases and multiple omitted maxima.
8. Positivity, locality and equivariance of u follow factorwise. The maximum is finite over the entire finite marked layer and complete actual-ideal sums.
9. A sufficiently small common scale gives positive full complements. Those full slots cannot be second precursors of the new incomparable-birth diamonds. Fair factors and transported scalar identity maps yield complete map equality.
10. Empty and singleton layers are handled separately; the singleton seed 2/3 is compatible without requiring the illustrative half-scale.

#### Not assumed

No ratio-potential theorem, next-layer history independence, strengthened Markov axiom, row independence, unmarked law, new local/gluing condition, coefficient witness, numerical enumeration, mesh, metric, physical clock, geometry, additional quantum axiom or optimized scale is used as a hidden premise.

The ordinary structural weights w and auxiliary H are definitions from already supplied lower rows. H is not a stipulated new endpoint law. Its factors never require an endpoint weight beyond size n.

#### Reviewed scope and limits

Distinct independent review examined the layer indexing, concrete marked terminal transport, exponent partition, all boundary cases, and the scope of the N5 application. This is sufficiency only; it is not a classification of arbitrary component-dependent scales. No source hash authenticates a theorem by itself.

No historical novelty or exhaustive absence-of-proof claim is made. Part N remains outside the scientific scope of this proof.

## Q. An admitted continuation with an eventual chain tail

**Acceptance and scope.** This is an existence result above a complete admitted finite kernel prefix, using Part P's finite sufficiency theorem; no classification of all component solutions is assumed. The available records support timely completion of this continuation proof; its independent reviewer did not inspect the author's raw final verification receipt. That timing limitation is separate from the inherited Part P author's recorded 65-second noncompliance, which remains preserved below.

Status: mathematics accepted following distinct independent review and coordinator disposition. Manual proof only.

**Accepted result.** Every complete admitted finite marked prefix in the declared scalar-passive model admits a positive common-scale continuation in which only finitely many subsequent births use proper ideals, almost surely. Thereafter each newborn is above every previous vertex. Height/cardinality tends to one, width becomes a finite random constant, and comparable-pair density tends to one. The current model therefore does not exclude this particular asymptotic order structure.

### 1. Model, accepted dependency and horizon

A state is a finite order P with immutable binary marks r and an arbitrary complex positive-semidefinite payload. Every actual ideal S is eligible. Structural probabilities q(P,r,S) are positive and normalize over all ideal occurrences. Proper slots read only marks in S; full slots may read all old marks. Equivariance and complete transported marked diamonds hold. A newborn bit is independently fair, and its branch map is q/2 times the identity.

Fix an integer h≥0. Preserve all supplied admitted rows on parents of size less than h, equivalently the complete history law through h births. This means a complete finite prefix of the kernel, not just one observed path. If h=0, first supply the forced empty-parent row q(empty,empty)=1. Set m=max(h,1). We choose only rows at parent sizes n≥m. Any already prescribed singleton row is preserved when h≥2.

The mathematical dependency is Part P's accepted finite maximal-deletion identity and common-scale sufficiency theorem. It establishes that, from any admitted smaller prefix, the maximal-deletion potential is positive, equivariant and selected-mark local, satisfies every inherited marked ratio identity, and admits any common layer scale with positive full complements. Its author's recorded 65-second procedural breach remains NONCOMPLIANT; the later timely review and coordinator disposition permit mathematical reuse without waiving that breach.

Parts A and D retain their historical conditional wording. We neither rewrite those records nor assume their full classification premise. Only accepted finite identity and common-scale sufficiency are needed here.

### 2. Declare the continuation

Suppose all rows below n are fixed, with n≥m. For every proper ideal S of every n-vertex marked parent define

\[
M(P,S)=\operatorname{Max}(P)\setminus S,\qquad
u_n(P,r,S)=
\prod_{\varnothing\ne A\subseteq M(P,S)}
q(P\setminus A,r|_{P\setminus A},S)^{(-1)^{|A|+1}}.
\]

All factors use this same recursively constructed law, including its actual smaller full complements. Put

\[
U_n(P,r)=\sum_{\substack{S\subsetneq P\\S\text{ ideal}}}u_n(P,r,S),
\qquad K_n=\max_{|P|=n,\ r}U_n(P,r).
\]

The sum counts all actual ideals separately. The maximum covers the entire marked layer represented on a fixed n-element label set, including parents unlikely under the chosen prefix. Part P gives \(0<K_n<\infty\). This is mathematical finiteness, not an enumeration or complexity claim.

Choose explicitly

\[
\varepsilon_n=2^{-(n+2)},\qquad
a_n=\frac{\varepsilon_n}{1+K_n},
\]
\[
q(P,r,S)=a_nu_n(P,r,S)\quad(S\subsetneq P),\qquad
q(P,r,P)=1-a_nU_n(P,r).
\tag{1}
\]

Because n≥1, \(0<\varepsilon_n<1\), and

\[
0<a_nU_n(P,r)\le
\varepsilon_n\frac{K_n}{1+K_n}<\varepsilon_n<1.
\tag{2}
\]

Thus every proper slot is positive and every full complement exceeds \(1-\varepsilon_n\). Complete rows normalize. The single constant a_n across the whole layer preserves the accepted potential identity. Full complements cannot be second precursors of new incomparable-birth diamonds, since such a precursor excludes the first newborn. All old/newborn markings, empty/full/equal base precursors and the common fair factor 1/4 remain included. Locality, equivariance and complete scalar-map admission follow from Part P.

Induction defines an admitted row at every finite parent size. No bound on the growth of K_n, uniform positive coefficient floor, mark independence of the structural law, extra gluing axiom or physical clock is assumed. The chosen epsilon sequence is an explicit mathematical selection, not a derived DET preference.

### 3. The infinite classical history law exists

Give vertices their birth labels. At each finite stage there are finitely many legal actual ideal/bit choices. For a legal marked history of k births define its cylinder weight by

\[
p(\gamma_k)=2^{-k}\prod_{j=0}^{k-1}q(P_j,r_j,S_j).
\tag{3}
\]

Each weight is positive. Summing the weights of all one-step extensions gives the parent-cylinder weight, since the structural row sums to one and both fair bits are retained. Induction gives normalized finite-history distributions and consistency under every truncation.

The standard probability extension theorem on this finitely branching discrete history tree therefore supplies a unique measure on the sigma-algebra generated by these cylinders. Its hypotheses here are precisely the finite normalized distributions and verified truncation consistency. Each transition still has a finite parent; no kernel at an infinite parent is requested. This is a classical probability construction, not an added physical axiom or a measure on an unlabelled infinite-order quotient.

Let \(\mathcal F_n\) contain the entire history through n births. Under this measure the conditional next-branch probabilities are exactly q(P_n,r_n,S)/2, by the cylinder ratios. Different births need not be independent. In particular, old marks may influence later structural choices. The payload remains scalar-passive at every finite horizon; no infinite-dimensional payload construction or division by a payload trace is used.

### 4. Finitely many proper births, without independence

For n≥m let E_n denote the event that the birth from parent size n chooses a proper ideal. Summing over all proper ideals and both bits, equation (2) gives the uniform conditional bound

\[
\Pr(E_n\mid\mathcal F_n)
=a_nU_n(P_n,r_n)<\varepsilon_n.
\tag{4}
\]

For any fixed N≥m, the tower property gives
\(\Pr(E_n\mid\mathcal F_N)\le\varepsilon_n\) for every n≥N. Apply the conditional union bound first to finitely many events, then pass to their increasing union:

\[
\Pr\!\left(\bigcup_{n\ge N}E_n\mid\mathcal F_N\right)
\le\sum_{n=N}^{\infty}2^{-(n+2)}
=2^{-(N+1)}.
\tag{5}
\]

Taking expectations gives the same unconditional bound. The events \(\bigcup_{n\ge N}E_n\) decrease as N increases, and their intersection is the event of infinitely many proper births. Continuity of probability from above and (5) give probability zero for that intersection. No independence or independent-event version of Borel–Cantelli is needed.

Define the random tail-start cardinality T by T=m if no E_n occurs for n≥m; otherwise

\[
T=1+\max\{n\ge m:E_n\text{ occurs}\},
\]

with T=infinity on the null event of infinitely many occurrences. Then T is finite almost surely. For every deterministic N≥m,

\[
\{T>N\}=\bigcup_{n\ge N}E_n,\qquad
\Pr(T>N\mid\mathcal F_N)\le2^{-(N+1)}.
\tag{6}
\]

This is a bound on the last exception, not a deterministic cutoff. T is generally not a stopping time: knowing that an exception was the last requires future information. We use T only in pathwise statements and invoke no stopping-time theorem.

Indeed every finite state of size N≥m has a positive proper-ideal sum. Thus \(\Pr(E_N\mid\mathcal F_N)>0\), and \(\Pr(T>N)>0\) for each such N. No finite observation certifies that exceptions are finished. Positive support of every finite legal history is compatible with probability zero for infinitely many exceptions.

### 5. Exact intrinsic order statistics

For a finite order P with n vertices define:

- H(P): maximum number of vertices in a chain, with H(empty)=0.
- W(P): maximum number of vertices in an antichain, with W(empty)=0.
- I(P): number of unordered pairs of distinct incomparable vertices.
- For n≥2, \(D(P)=1-I(P)/\binom n2\): the fraction of unordered distinct-vertex pairs that are comparable. No density is assigned at n=0 or 1.

A full-ideal newborn lies above every old vertex. It increases height by exactly one: a longest old chain can be extended, and removing the newborn from any chain leaves an old chain. For a nonempty parent it leaves width unchanged, since an antichain containing the newborn has only that vertex. It creates no incomparable pair and changes no relation among old vertices.

On every path with finite T, we have T≥m≥1, and all births from parent sizes n≥T are full. Therefore, for all n≥T,

\[
H(P_n)=H(P_T)+n-T,\qquad
W(P_n)=W(P_T),\qquad I(P_n)=I(P_T).
\tag{7}
\]

The tail is a chain above the entire finite prefix P_T. Existing incomparable pairs inside P_T persist; the final order need not be a total order, and its eventual width need not equal one.

Equation (7) gives, almost surely,

\[
\frac{H(P_n)}n
=1-\frac{T-H(P_T)}n\longrightarrow1,
\qquad W(P_n)\text{ is eventually the finite constant }W(P_T),
\]
\[
D(P_n)
=1-\frac{I(P_T)}{\binom n2}\longrightarrow1
\quad(n\ge\max(T,2)).
\tag{8}
\]

The constants in these exact formulas are path-dependent finite quantities. For each fixed N≥m, equation (5) also says that with probability at least \(1-2^{-(N+1)}\), every subsequent birth is full and the corresponding formulas hold from P_N onward. The empty-prefix case is already covered by the forced first birth and m≥1.

### 6. What this establishes, and what it does not

The result answers an existence question for every admitted finite prefix. The declared model allows a continuation with an almost-sure full-ideal chain tail. Accordingly its existing admission conditions alone do not exclude that behavior or force another asymptotic order structure.

Preserving a finite prefix does not assert that every continuation has these statistics. No analysis of all other scales, the earlier half-scale prescription, or a general asymptotic classification is supplied. The chosen summable schedule is not uniquely selected, optimized or justified physically.

Height, width and comparability density are intrinsic order statistics. Their limits establish no physical dimension, Lorentzian manifold, metric, gravity, empirical correspondence or informative quantum dynamics. Birth index is bookkeeping, not a physical clock. No novelty claim is made.

Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause, execution/publication gates and Boundary separation remain.

### 7. Premises and manual obligations

Status: mathematics accepted following distinct independent review and coordinator disposition.

#### Inputs actually used

1. Section 1 states the scalar-passive marked-order model. The complete admitted finite kernel prefix is assumed, including every actual ideal, normalized positive support, selected-mark proper locality, equivariance, transported marked diamonds and independent fair newborn bits.
2. Part P's finite identity and common-scale sufficient-extension theorem is mathematically accepted after distinct review. Necessity/classification is not required. The former author's 65-second cutoff breach remains NONCOMPLIANT.
3. Parts A, B.4 and D establish historical definitions, finite-selection scope and the prior cylinder-law construction; their historical conditional status is preserved.
4. Ordinary classical probability extension for consistent finite discrete cylinder laws, the conditional tower property, the union bound and continuity of probability are standard mathematical tools. They are not new physical or DET selection axioms. No external reference or hidden source was opened.

#### Explicit new choices

- Horizon h means all rows with parent size less than h are fixed. The empty row is forced if absent; new choices begin at m=max(h,1).
- Every later layer uses its actual maximal-deletion potential from this same recursively defined law.
- K_n is the whole marked-layer maximum of the sum over all actual proper ideal occurrences.
- Epsilon_n=2^(-(n+2)) and a_n=epsilon_n/(1+K_n) are declared choices, not derived preferred constants.
- Birth labels are auxiliary coordinates for the classical history space. Order statistics do not depend on renaming them.

#### Manual proof obligations discharged

- Part P makes each potential defined, positive, equivariant and selected-mark local; K_n is positive and finite at each n≥1.
- Proper probability sum is epsilon_n U_n/(1+K_n), bounded strictly below epsilon_n. Positive normalized full complements and all marked-map diamonds follow. No infinite coefficient limit or quantitative K_n rate is needed.
- Complete fair-bit cylinder weights are positive, normalized and consistent under truncation. These verify the hypotheses for a countable infinite history measure.
- Conditional proper-birth bounds hold given the complete past, without independence of different births or independence between old marks and later geometry.
- Tower, finite union bounds and monotone passage give the exact tail estimate sum_(n≥N)epsilon_n=2^(-(N+1)). Continuity from above gives finitely many proper births almost surely.
- T is defined after the last proper birth, with a no-exception case. It is not treated as a stopping time. No deterministic last exception follows; positive proper mass at every finite state excludes finite certainty.
- A full birth adds one to height, preserves nonempty-parent width and preserves the number of incomparable pairs. Since T≥1, exact post-T formulas prove all three asserted statistics.
- Empty/singleton parents and undefined pair densities below size2 are treated explicitly. Old incomparable pairs are never erased, so eventual width need not be1.

#### Remains outside the result

No assertion covers every admissible continuation, classifies all asymptotics, or evaluates the earlier half-scale law. There is no uniform coefficient floor, computational guarantee, empirical evidence, preferred law, physical dimension, metric, spacetime or gravity claim. Fair scalar payload branches are preserved without deriving quantum dynamics.

Distinct independent review examined the horizon convention, whole-layer maximum, complete ideal/bit counting, probability extension hypotheses, conditional tail estimate and its indexing, the non-stopping-time treatment, and the exact pathwise height/width/pair formulas.

All preserved custody, protected-validation, ABSTAIN, Status M, zero-qualification, RET-only pause, execution/publication and Boundary gates remain.

## R. Finite observations of the chain-tail continuation family

**Acceptance and scope.** This accepted result uses Part Q's admitted continuation above a complete finite kernel prefix and Part P's finite sufficiency. It concerns one common finite or stopped observation in the unrestricted scalar-passive family. Recorded timely completion distinguishes the author-reported final verification from supported chat completion; the raw final author receipt was not independently reopened. That evidence limitation is separate from the inherited Part P author's 65-second NONCOMPLIANCE, which remains unwaived.

Status: mathematics accepted following distinct independent review and coordinator disposition. Manual proof and admitted counterexample only.

**Result.** For each admitted infinite law L and deterministic horizon h, the accepted Part Q construction gives an admitted chain-tail law L_h with exactly the same complete first-h-birth distribution. For one fixed nonanticipating stopped observation, its output laws satisfy
\[
d_{\rm TV}(\operatorname{Law}_L(Y),\operatorname{Law}_{L_h}(Y))
\le \Pr_L(\tau>h).
\]
If tau is finite almost surely under L, this bound tends to zero as h increases. Finiteness under each L_h is unnecessary and does not follow in general.

### 1. Family, construction and exact finite-prefix equality

Work in the full scalar-passive marked-law family specified in Parts P and Q, not its particular fixed coefficients or half-scale continuation. Every actual ideal has positive probability; complete rows normalize; proper slots satisfy selected-mark locality; equivariance, complete transported marked diamonds, fair newborn bits and scalar identity payload maps are retained.

Let L be any admitted infinite law with the declared consistent finite kernels. For each integer h≥0, preserve its rows on every marked parent of size less than h. Apply accepted Part Q to that complete finite prefix. If h=0, the empty row is forced; the continuation begins at m=max(h,1). At every later finite layer it uses its own potential u_n, whole-layer proper-sum maximum K_n, and
\[
a_n=\frac{2^{-(n+2)}}{1+K_n},\quad
q_{L_h}(P,r,S)=a_nu_n(P,r,S)\ (S\subsetneq P),
\]
with the complete full complement. Denote this law by L_h. Part Q establishes its existence, admission and almost-sure eventual full-ideal chain tail. The accepted finite maximal-deletion identity and common-scale sufficiency behind it are in Part P.

On the common space Omega of legal marked natural histories, let F_n be the raw sigma-algebra generated by the complete first n births. For every legal marked history gamma_h,
\[
\Pr_L(\gamma_h)
=2^{-h}\prod_{n=0}^{h-1}q_L(P_n,r_n,S_n)
=\Pr_{L_h}(\gamma_h).
\tag{1}
\]
Every actual ideal occurrence and every newborn mark is included. At fixed h there are finitely many such histories, so (1) proves equality of the restrictions of both measures to F_h. The empty product covers h=0.

Consequently every common measurable bounded statistic of the complete first h births has exactly the same distribution under L and L_h, and the same bounded expectations. This is equality of finite-history laws, not a fit to a realized path. A fixed further measurable coarsening of these histories also has equal distributions.

### 2. Common observation contract

The following conditions specify the stopped-observation assertion.

- Use the same raw history filtration under both laws, without adding different law-dependent completed null sets.
- Optionally supply an auxiliary randomizer R, with one declared law nu, independent of the growth history under both hypotheses. A common random tape may be revealed at time zero. Set G_n=F_n joined with sigma(R); without randomization, R is constant.
- Fix one common map tau: Omega times the randomizer space to the nonnegative integers or infinity. It is a stopping time for G_n: {tau≤n} belongs to G_n. The rule cannot read the hypothesis identity or future growth.
- Fix one common measurable output space with a distinguished cemetery symbol Delta. On {tau=n<infinity}, output Y is determined measurably by the first n births and R. Equivalently, {tau=n,Y in B} belongs to G_n for every measurable B. Set Y=Delta on {tau=infinity}.

The output may include tau and the entire stopped transcript, or a common measurable summary of it. The cemetery symbol makes the output law a probability measure even if stopping fails; it is mathematical bookkeeping, not a finite-time detector of nontermination. We do not discard or condition away this mass.

These rules observe the histories without changing the growth law through interventions. No extra physical readout, clock or hypothesis-dependent information is supplied. Since the same independent randomizer is used, (1) also gives equality on G_h.

### 3. Direct subprobability proof of the TV bound

Write P=L times nu and Q=L_h times nu when randomization is present. For measurable output set B, define
\[
\mu_h(B)=P(Y\in B,\tau\le h).
\]
The event is the finite union of {tau=n,Y in B}, n≤h, hence belongs to G_h. Equality on G_h gives
\[
\mu_h(B)=Q(Y\in B,\tau\le h),\qquad
P(\tau>h)=Q(\tau>h)=:p_h.
\tag{2}
\]

Both complete output laws therefore have the same subprobability part mu_h of mass 1-p_h. Their remaining positive parts rho_P and rho_Q each have mass p_h, including any cemetery contribution. With the convention
\[
d_{\rm TV}(\alpha,\beta)=\sup_B|\alpha(B)-\beta(B)|,
\]
we have
\[
|\operatorname{Law}_P(Y)(B)-\operatorname{Law}_Q(Y)(B)|
=|\rho_P(B)-\rho_Q(B)|\le p_h.
\tag{3}
\]
Taking the supremum proves the claimed bound, with no factor two and no coupling regularity assumption. Neither independence of births nor finiteness of tau under Q is used.

If P(tau<infinity)=1, continuity of probability gives p_h decreasing to zero. Thus the output laws of the sequence L_h approach the output law of L in total variation for this fixed observation rule. Here p_h is the stopping-rule tail under L; it is not Part Q's numerical bound on its own last proper birth.

### 4. Termination need not transfer: an admitted example

This bounded example addresses only the possible extra assertion that tau must also be finite under L_h.

For an n-vertex parent P, let k(S) be the number of maximal elements of the induced ideal S, with k(empty)=0. Define a mark-independent kernel
\[
q_*(P,S)=2^{-(n-|S|+k(S))}.
\tag{4}
\]
Every entry is positive. To check normalization, independently select each old vertex with probability 1/2 and take the downward closure of the selected subset. Its closure equals S exactly when all maxima of S are selected and every vertex outside S is unselected; other vertices in S are free. This has probability (4). The closure events partition all subsets, so the sum over every actual ideal is one. This is a mathematical row construction, not an executed simulation.

Locality and equivariance hold because the kernel ignores marks and uses intrinsic order quantities. In a diamond based on C, with a newborn x excluded from second precursor T, the induced order on T is unchanged and
\[
q_*(C+x,T)=\tfrac12q_*(C,T).
\]
Hence both structural diamond products equal \(q_*(C,S)q_*(C,T)/2\), including empty/full/equal precursors. Independent fair bits and scalar identity maps give every marked-map diamond. Normalized finite cylinder laws supply an admitted infinite law L_*.

For every nonempty parent,
\[
q_*(P,P)=2^{-k(P)}\le\tfrac12.
\]
Let tau be the birth number of the first proper-ideal choice from a parent of size at least one, or infinity if none occurs. This is a raw-history stopping time. Under L_*, the conditional chance of avoiding such a choice for k successive steps is at most 2^{-k}, by successive conditioning. Therefore tau is finite almost surely.

Now take its Part Q continuation L_{*,1}, preserving the first birth. The accepted bound gives
\[
\Pr_{L_{*,1}}(\text{some proper birth from parent size }n\ge1)
\le\sum_{n\ge1}2^{-(n+2)}=\tfrac14.
\]
Thus \(\Pr_{L_{*,1}}(\tau=\infty)\ge3/4\). Choosing Y=0 upon termination and Delta otherwise gives a two-symbol counterexample to transferred termination. There is no contradiction with (3): here \(\Pr_{L_*}(\tau>1)=1\). This example belongs to the unrestricted admitted family; it does not replace a separately prescribed seed or continuation.

For general L_h the proof only ensures
\(\Pr_{L_h}(\tau=\infty)\le p_h\).
A positive p_h cannot establish almost-sure termination. No further termination classification is asserted.

### 5. Quantified limit on uniform separation

Let C be the family of admitted laws with an almost-sure eventual full-ideal chain tail; it contains every L_h above. Fix L and one common observation pair (tau,Y) satisfying Section 2, with tau finite almost surely under L. Then
\[
\forall\delta>0\ \exists h<\infty\ \exists Q=L_h\in C:
\quad d_{\rm TV}(\operatorname{Law}_L(Y),
                       \operatorname{Law}_Q(Y))
\le\Pr_L(\tau>h)<\delta.
\tag{5}
\]
In particular the infimum of this output-law distance over C is zero. For any common test taking values in [0,1], the difference of its expectations is at most that TV distance. Therefore this fixed observation cannot have a positive separation gap from L uniformly over the unrestricted chain-tail family.

The horizon and continuation in (5) may depend on L, the fixed rule and delta, and must be fixed before seeing the data. The construction preserves all possible histories through h, not merely the observed one. No rate uniform over L or over stopping rules follows. If tau≤h surely by design, (3) gives exact stopped-output equality at that horizon.

The quantifier order matters: a different L_h is available for each h. This is not one chain-tail law agreeing with L at every finite horizon. If one measure agreed on every finite-history cylinder, uniqueness on the cylinder-generated sigma-algebra would make it equal to L, including its measurable tail-event probabilities. No such single-measure assertion is made here.

### 6. Boundaries

Exact finite-prefix matching and the stopped-output bound do not imply equality of infinite-tail events between L and L_h. The TV limit controls bounded tests, not unbounded stopped-output expectations, mean observation costs or waiting times without further hypotheses.

This is a mathematical statement about a specified common observation of the unrestricted scalar-passive family. It gives no actual-measurement indistinguishability, universal untestability of DET, metric, clock, physical readout, gravity or quantum-dynamics result. Restricting to a physically selected or fixed parametric law, adding a justified observable channel, or intervening on growth is a different problem.

The Part P author's timing breach remains NONCOMPLIANT despite its separately accepted mathematics. Part Q acceptance and current evidence retain their exact scopes. Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause, execution/publication gates and Boundary separation remain.

### R premises and manual obligations

Status: accepted premises and manual obligations for the finite-observation theorem and admitted counterexample above.

#### Accepted inputs and assumptions

- The full scalar-passive marked-law family specified in Parts P and Q: complete actual-ideal support, positive normalized rows, proper selected-mark locality, equivariance, complete transported marked diamonds, independent fair newborn bits, scalar identity payload maps.
- L is any admitted infinite law in that family with its consistent finite kernels. Its complete rows below each deterministic h, not a realized path, supply the preserved prefix.
- Part Q's construction has been distinctly reviewed and accepted. It supplies an admitted L_h with an almost-sure eventual full-ideal chain tail, preserving all rows belowh.
- Part P supplies the accepted finite sufficiency theorem. Historical conditional records and the65-second NONCOMPLIANT author overrun are not rewritten or waived.
- Standard finite-cylinder probability extension, restriction/pushforward of measures, continuity of probability, conditional expectations and total variation are mathematical tools, not added physical assumptions.

#### Observation conditions, explicitly required

Use the same raw full-history filtration. A common optional randomizer has a fixed distribution independent of either growth history; reveal its tape at timezero if desired. The stopping rule is a common stopping time for the resulting filtration. For every finite n, the event {tau=n,Y in B} must be measurable from that prefix and randomizer. Output equals a distinguished cemetery symbol on nontermination.

No law-dependent completion, hypothesis identity leak, future-dependent output at a claimed finite stop, conditioning on termination, growth intervention or extra physical channel is admitted. Almost-sure finiteness is assumed under L only.

#### Proof obligations discharged manually

1. Equal rows belowh give equal probabilities for every complete firsth-birth history, including all ideal occurrences and all fair marks; finite disjoint unions give equality on F_h.
2. Appending the same independent randomizer preserves equality on G_h.
3. For each output set B, {tau<=h,Y in B} is G_h-measurable. The two output laws therefore share the same subprobability measure of mass1-p_h, with p_h=P_L(tau>h)=P_Lh(tau>h).
4. Both residual positive measures have massp_h; their difference on any event is at mostp_h. This proves TV<=p_h under the supremum-over-events convention, without a factor2.
5. Almost-sure finiteness underL gives p_h->0. Finiteness underL_h is not needed, and its nontermination mass is bounded byp_h rather than forced tozero.
6. The bounded counterexample has q_*(P,S)=2^{-(|P|-|S|+|Max(S)|)}. Subset-closure partition proves row normalization; positivity, mark-blind locality and equivariance are immediate. A second precursor excluding a newborn gains precisely a factor1/2, proving every complete diamond. Fair scalar branches and normalized cylinders give an admitted infinite law.
7. Under that law, full-birth probability at a nonempty parent is at most1/2, so waiting for the first proper birth after parent-size1 terminates almost surely. Its Part Q horizon1 continuation has probability at least3/4 of no such birth, giving nontermination. A two-symbol output suffices.
8. Quantifiers are fixedL/fixedrule, then everydelta, then a deterministich and continuation chosen beforedata. The family infimum of outputTV iszero; this is not one continuation matching all horizons or a guarantee uniform over all rules.

#### Limits and review

No classification of laws or termination rules is attempted. The counterexample refutes transferred termination, not the proposed TV bound. Exact prefix equality is preserved; infinite-tail equality, unbounded-cost control, physical indistinguishability and universal untestability are excluded.

Distinct independent review examined the common raw filtration, stopped-output measurability, residual-mass bound, counterexample admission and indexing, and the quantifier order. Current byte identities and readbacks are evidence of source identity, not a substitute for mathematical verification.

All original protected-validation, custody, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary and execution/publication gates remain.

## S. Unbounded width and finite-prefix agreement

**Acceptance and scope.** This theorem uses the unrestricted model in Part A, the accepted continuation in Part Q and the observation result in Part R. Its author-reported final verification and supported chat completion are distinct from the separately attributed review completion; the raw external final sessions were not independently reopened. The available records support timely completion of this theorem and its review. Those evidence limits do not waive the inherited Part P author's recorded 65-second NONCOMPLIANCE.

Status: mathematics accepted following distinct independent review and coordinator disposition. Manual proof only.

**Result.** Under the admitted law
\[
q_*(P,S)=2^{-(|P|-|S|+|\operatorname{Max}(S)|)},
\]
the number of maximal vertices has conditional transition \(1+\operatorname{Binomial}(M_n,1/2)\), its limsup is infinite almost surely, and order width tends to infinity almost surely. Nevertheless, for every fixed finite horizon h, an admitted chain-tail continuation has exactly the same complete first-h-birth law and eventually constant finite width. The full infinite-history measures are separated by their width asymptotics, while the accepted fixed stopped-output approximation remains valid along different h.

### 1. Model and exact accepted dependencies

Let P_n be the order after n births and let F_n contain the complete marked natural history through n. Define
\[
M_n=|\operatorname{Max}(P_n)|,\qquad
W_n=\max\{|A|:A\text{ is an antichain of }P_n\}.
\]
Set M_0=W_0=0. Here maxima of an ideal mean maxima of its induced order. All cardinalities and indices are combinatorial; n is not a physical clock.

The scalar-passive model retains every actual ideal occurrence, positive normalized rows, proper selected-mark locality, equivariance, complete transported marked diamonds, independent fair newborn marks, and scalar identity payload maps. We use its unrestricted family, not the particular fixed coefficients printed in Part A.

Part R supplies the accepted admission of q_*, its subset-closure representation and its finite/stopped-observation theorem. Part Q supplies the accepted finite-prefix-preserving chain-tail construction. These are distinct accepted dependencies. Neither the maximal-count transition nor its unbounded excursions is assumed from those results.

### 2. Fresh conditional subset representation

Given any complete current history, select each vertex of P_n independently with probability 1/2 and let S be the downward closure of the selected subset. A given actual ideal S is obtained precisely when every maximum of S is selected and every vertex outside S is unselected; its other vertices may be selected or not. Thus its conditional probability is exactly q_*(P_n,S).

These disjoint closure events partition all subsets. Consequently this is an exact representation of the already admitted row, including empty and full ideals, rather than a restriction of support or a new growth law. Attach the independently fair newborn bit as before. The representation can be used afresh at each transition conditional on the current history. The auxiliary subset itself is not an added observable or a physical process.

An old maximal vertex belongs to the closure S if and only if it was selected: no strictly larger old vertex can generate it by downward closure. A selected old maximum lies below the newborn and ceases to be maximal. An unselected old maximum lies outside S and remains maximal. An old nonmaximum cannot become maximal, because its old successor remains in the order. The newborn is maximal.

Therefore, on this exact representation,
\[
M_{n+1}
=1+\sum_{v\in\operatorname{Max}(P_n)}
             {\bf1}\{v\text{ was unselected}\}.
\]
The summands are conditionally independent Bernoulli(1/2) variables given F_n. Equivalently,
\[
\Pr_*(M_{n+1}=j\mid F_n)
=\binom{M_n}{j-1}2^{-M_n},
\quad 1\le j\le M_n+1,
\tag{1}
\]
and the probability is zero otherwise. This derives the conditional transition; it does not assume independent successive M_n or independent blocks.

At n=0 the sum is empty, so M_1=1 deterministically. At n=1, M_2 is one or two with probability 1/2 each. All already committed marks remain in F_n, and both possible next newborn marks are retained; q_* ignores their values. The formula is consequently valid for every legal marked history, not merely an unmarked average.

### 3. A uniform finite-block hitting bound

Fix an integer threshold k≥1 and any deterministic starting index N≥0. Suppose the current count is r=M_N<k. At a step having m current maxima, the event that none of those maxima is selected has conditional probability 2^{-m}. It raises the count from m to m+1, whatever happens to the other old vertices.

Require this event successively until the count reaches k. Starting from r, this requires k-r steps and has conditional probability
\[
\prod_{m=r}^{k-1}2^{-m}
=2^{-\sum_{m=r}^{k-1}m}
\ \ge\ \delta_k:=2^{-k(k-1)/2}>0.
\tag{2}
\]
The product follows by successive conditioning: along the specified events the counts are r,r+1,...,k, and each next conditional probability is fixed. No independence between those events is assumed. Since 0≤r<k, the exponent is at most 0+1+...+(k-1), and k-r≤k. Thus every history below k has probability at least delta_k of reaching k within the next k births. If the count already reaches or exceeds k, hitting has occurred at once.

Define the waiting index
\[
\sigma_{N,k}=\inf\{j\ge0:M_{N+j}\ge k\},
\]
with infinity if the set is empty. For every integer b≥1,
\[
\Pr_*(\sigma_{N,k}>bk\mid F_N)
\le(1-\delta_k)^b.
\tag{3}
\]
To verify the iteration, let A_b={sigma_{N,k}>bk}. This event is measurable at N+bk, and on A_b the count is still below k. The one-block bound applied to that complete history gives
\[
\Pr_*(A_{b+1}\mid F_{N+bk})
\le(1-\delta_k){\bf1}_{A_b}.
\]
The conditional tower property and induction give (3), starting from the first-block bound. Blocks can be dependent. For k=1, delta_1=1 and hitting occurs by the next birth even from the empty parent; (3) for b≥1 is then zero without any ambiguous zeroth power.

Letting b tend to infinity proves that sigma_{N,k} is finite almost surely for every fixed pair N,k. There are countably many such pairs. On their common probability-one event, for every N and k there is an n≥N with M_n≥k. Hence
\[
\limsup_{n\to\infty}M_n=\infty
\quad\text{almost surely}.
\tag{4}
\]
This proves arbitrarily large excursions at arbitrarily late indices. It does not assert that M_n itself tends to infinity, give a stationary distribution, or establish an asymptotic rate.

### 4. Width tends to infinity

The maximal vertices form an antichain, so M_n≤W_n. Births preserve the entire induced order on old vertices. In particular, an old antichain remains an antichain even when some of its vertices cease to be maximal. Thus
\[
W_{n+1}\ge W_n.
\]
On the probability-one event of (4), W_n is unbounded. A nondecreasing sequence of nonnegative integers that is unbounded tends to infinity. Therefore
\[
\Pr_*(W_n\longrightarrow\infty)=1.
\tag{5}
\]
The proof uses neither a width enumeration nor a claim about the frequency of maximum-count excursions. The empty and singleton cases are already handled by W_0=0 and W_1=1.

### 5. Same finite laws, different infinite width

Let L_* denote the infinite marked-history law of q_*. For every deterministic h≥0, apply accepted Part Q to its complete kernel prefix on all marked parents of size less than h. Call the resulting chain-tail law Q_h. Its later rows use the declared summable common-scale prescription, while every earlier row remains q_*.

By Part Q, under Q_h there is an almost-sure finite random cardinality T>=max(h,1) after which every birth uses the full ideal. Such a newborn is above all previous vertices of the nonempty parent, and
\[
W_n=W_T<\infty\qquad(n\ge T)
\quad Q_h\text{-almost surely}.
\tag{6}
\]
By Part R, for every complete first-h-birth history gamma_h, including all ideal choices and marks,
\[
\Pr_{L_*}(\gamma_h)
=2^{-h}\prod_{n<h}q_*(P_n,S_n)
=\Pr_{Q_h}(\gamma_h).
\tag{7}
\]
Thus for every finite h there exist two admitted infinite laws with identical complete laws through h and opposite almost-sure width conclusions. This is not one Q agreeing with L_* at every horizon.

For precise infinite-history separation, define
\[
A=\{W_n\to\infty\}
=\bigcap_{k\ge1}\ \bigcup_{N\ge0}
  \bigcap_{n\ge N}\{W_n\ge k\}.
\]
This is a measurable asymptotic event in the cylinder-generated history sigma-algebra. Equations (5)–(6) give
\[
L_*(A)=1,\qquad Q_h(A)=0
\quad\text{for every fixed }h.
\tag{8}
\]
Accordingly the two full-history measures are mutually singular, and their full-history total variation, defined as the supremum over measurable events, equals one. No independence-tail zero-one theorem is used. The separation event requires the infinite history; positive support of every finite legal history does not imply equivalence of infinite measures.

### 6. Fixed stopped outputs still obey the accepted bound

Fix one common nonanticipating observation (tau,Y), with the same raw full-history filtration, optional common independent randomizer, and a cemetery output on nontermination, exactly as specified in Part R. Suppose tau is finite almost surely under L_*. Then the accepted result gives
\[
d_{\rm TV}\bigl(\operatorname{Law}_{L_*}(Y),
               \operatorname{Law}_{Q_h}(Y)\bigr)
\le\Pr_{L_*}(\tau>h)\longrightarrow0.
\tag{9}
\]
Finiteness under Q_h is not needed. The output, rule and reference L_* are fixed first; h and its different Q_h can then be chosen before data to make this output distance arbitrarily small. There is no uniform rate over rules, and no single Q_h is claimed to match every finite horizon.

There is no conflict between (8) and (9). They concern different information: the complete infinite-history event A versus one output measurable at its finite stopping time under L_*. Infinite-width behavior is not converted into a finite-time certificate by this proof. No equality of infinite tails or bound on unbounded observation costs follows from (9).

### 7. Scope

This is a formal dependence-on-law result inside the declared mathematical family: its admission conditions allow both almost-sure unbounded width and, above any finite prefix of that same law, eventual finite width. It selects neither continuation as preferred.

No stationary law, rate, height/density classification, physical dimension, metric, gravity, readout, efficient algorithm, empirical DET validation or universal untestability claim is supplied. The inherited Part P timing breach remains NONCOMPLIANT and unwaived; accepted dependencies retain their exact scopes.

Protected validation/custody, distinct review, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary separation and all execution/publication/resource gates remain. Mathematical acceptance supplies no execution or publication permission for other results.

### 8. Premises and proof obligations

Status: these premises accompany the accepted theorem at its stated scope.

#### Accepted inputs

- Part A states the unrestricted scalar-passive binary-marked-order model: all actual ideals, positive normalized complete rows, selected-mark proper locality, equivariance, complete transported marked diamonds, independently fair newborn marks and scalar identity payload maps.
- Part R supplies the accepted q_* admission, subset-closure representation and finite/stopped-observation theorem.
- Part Q supplies the accepted complete-finite-prefix chain-tail construction and eventual finite width. Its underlying finite sufficiency in Part P retains its existing status; no stronger classification is imported.
- Historical authorization and current coordination/resource boundaries remain separate from mathematical acceptance. Resource guards are checked independently before authorized work.
- Standard conditional probability, finite iteration, continuity and countable intersections are mathematical tools, not physical selection axioms.

#### Derived results

1. The fresh conditional half-selected subset has the exact q_* distribution after taking downward closure. Each actual ideal is retained. It is an auxiliary representation of the admitted row, not a new law or observation.
2. An old maximum belongs to the precursor precisely if selected. Selected maxima cease being maximal; unselected maxima survive. An old nonmaximum cannot become maximal, and the newborn is maximal.
3. Therefore, conditional on the entire marked history, M_(n+1)=1+Binomial(M_n,1/2) in distribution. Empty-parent M_0=0 gives M_1=1; the singleton gives M_2=1 or 2 equally.
4. From any r<k, sequentially declining to select current maxima reaches k after k-r steps. Its conditional probability is 2^(-sum_(m=r)^(k-1)m), at least delta_k=2^(-k(k-1)/2).
5. For every deterministic N>=0, k>=1 and b>=1, conditional failure to hit k within bk steps is at most (1-delta_k)^b. The proof conditions on complete histories at block boundaries; it assumes no block independence.
6. Taking b to infinity and intersecting the probability-one conclusions over countably many N,k gives limsup M_n=infinity almost surely. This is not a claim that M_n converges to infinity.
7. Maximal vertices form an antichain; old induced relations persist. Thus W_n>=M_n and W_n is nondecreasing, proving W_n tends to infinity almost surely.
8. For each fixed h, accepted Q_h preserves every marked finite history through h and has eventual finite width. The measurable infinite-history event of width diverging has probabilities 1 and 0, proving full-history mutual singularity.
9. Under the exact common stopping/output contract of Part R, every fixed rule finite almost surely under L_* still has output TV bounded by P_L*(tau>h), tending to zero along different Q_h. Full-history separation is not a finite-time certificate.

#### Explicit boundaries

The complete prefix includes all rows below h, not one realized path. The construction of Q_h depends on the chosen horizon, not observed data. No single chain-tail law matches L_* at every horizon.

The half-selection variables are used only to derive the exact already admitted transition. Marks, actual ideal occurrences and scalar payload branches remain unchanged. There is no empirical or physical interpretation of those auxiliary variables or of birth index.

No stationary distribution, asymptotic rate, height/density classification, preferred law, geometry/metric/gravity, efficient algorithm, physical readout or universal untestability is inferred.

#### Review and evidence

Distinct review checked the closure-to-maxima implication, conditional-binomial transition, precise stopped successful run in the hitting bound, dependent-block iteration, countable quantifiers, monotone-width implication, and distinction between full-history and fixed stopped-output laws.

The proof package retained twelve source/control files and fourteen source/prose bodies. Distinct review and coordinator checks verified exact current identities and five actual dependency-acceptance joins. Original/nested locators and raw external final sessions were not reopened. Hashes and readbacks establish identity, not mathematical verification or repaired historical custody. The initial exclusive output directory was absent; this observation and its subsequent creation remain in the evidence record. Recorded display clipping and its recovery are retained separately from the mathematical conclusions.

The inherited Part P author's 65-second NONCOMPLIANT overrun remains unwaived; the current theorem's recorded completion was timely. All protected-validation/custody, independent-review, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary and execution/publication gates remain. Any later result requires its own review and coordinator disposition.

## T. Constant-parameter transitive percolation in the marked contract

**Acceptance and scope.** This part records the independently reviewed and coordinator-accepted constant-parameter embedding. It extends Part S’s width result over a declared subfamily; Parts Q and R retain their finite-observation limits. The scalar formula has a conventional antecedent. No preferred law or physical measurement is selected.

Status: mathematics accepted following distinct independent review and coordinator disposition. Manual proof only.

**Result.** Half-selection is not forced by the scalar-passive marked admission conditions. Every fixed \(0<p<1\) gives the admitted kernel
\[
q_p(P,r,S)=p^{|\operatorname{Max}(S)|}(1-p)^{|P|-|S|}.
\tag{1}
\]
Its maximal-count transition is \(1+\operatorname{Binomial}(M_n,1-p)\), and its width tends to infinity almost surely. Different p give different two-birth laws.

The scalar formula and ancestor-closure construction already appear in the conventional transitive-percolation literature identified below. This part is a checked embedding and proof under the Part A marked contract, not a new model or a novelty claim.

### 1. Conventional antecedent and exact scope of the source

The recorded primary-source observation identifies D. P. Rideout and R. D. Sorkin, *A Classical Sequential Growth Dynamics for Causal Sets*, Physical Review D 61, 024002 (2000), [arXiv:gr-qc/9904062v3](https://arxiv.org/html/gr-qc/9904062v3), revised 26 June 2004, §4.2, “Another look at transitive percolation,” equation (6).

The supplied observation reports the scalar transition
\[
\alpha_n=p^m(1-p)^{n-\varpi},
\]
where m is the number of maximal precursor elements and varpi its cardinality, with independent ancestor selection followed by inclusion of their pasts. The correspondence is exact:

| Reported primary notation | Present notation |
| --- | --- |
| n | cardinality of parent P |
| varpi | cardinality of actual precursor ideal S |
| m | number of maxima of the induced order S |
| p | constant probability of selecting each old vertex |
| alpha_n | structural transition q_p(P,r,S) |

The literature attribution here follows a pinned, paraphrased primary-source observation, not a fresh direct reading by the proof author or independent reviewer. Its version, section and equation are retained exactly. That observation records a garbled PDF extraction and a readable versioned arXiv HTML observation. It supports the identified antecedent, not an exhaustive priority survey.

The paper's covariance, Bell-causality and normalization conditions are not assumed identical to the present marked-diamond contract. Admission below is checked directly. Neither the marks nor scalar payload embedding is licensed merely by citing the older paper, and no claim of their historical novelty is made.

### 2. Definition and complete normalization

Fix p once for the entire law, with 0<p<1. Work in the unrestricted model in Part A, not its separately prescribed seed or half-scale continuation. A state is a finite order P, immutable binary marks r, and an arbitrary complex positive-semidefinite payload X on the declared carrier. Every actual ideal S is eligible. Write n=|P|, s=|S| and m(S)=|Max(S)|, with m(empty)=0. Define q_p by (1), independent of r.

Given any current history, select each old vertex independently with probability p and take the downward closure of the selected subset. The closure equals S precisely when every maximum of S is selected and every vertex outside S is unselected. Other vertices of S are unrestricted. The corresponding probability is
\[
p^{m(S)}(1-p)^{n-s}.
\]
The unrestricted choices contribute total factor one. Closure events for all actual ideals partition all subsets; hence
\[
\sum_{S\text{ ideal of }P}q_p(P,r,S)=1.
\tag{2}
\]
This sums ideal occurrences, not isomorphism classes or selected representatives.

Because both p and 1-p are positive, every entry is strictly positive. The empty ideal has mass \((1-p)^n\), and the full ideal has mass \(p^{|\operatorname{Max}(P)|}\). The empty parent has only its full/empty ideal and mass one. No normalization complement is omitted.

A relabeling preserves n, s and m(S), proving equivariance. Ignoring marks satisfies proper-slot selected-mark locality and the permitted full-slot dependence. The subset representation is an exact mathematical representation of these rows; it is not a new physical mechanism or an executed procedure.

The endpoints are excluded by strict support. On a singleton, the empty/full row is (1-p,p): p=0 makes the full ideal impossible, and p=1 makes the empty ideal impossible. The forced empty-parent row remains one in the subset construction, without needing an ambiguous endpoint 0^0 convention. Endpoint processes therefore do not satisfy the declared full-support model.

### 3. Every complete marked diamond and payload map

Let C be any finite base and S,T any two ideals, including empty, full-base and equal choices. Append incomparable newborns x and y with pasts S and T, respectively. Each second precursor is an old ideal and excludes the other newborn. Its induced order, cardinality and number of maxima are unchanged, while the intermediate parent has one additional vertex. Therefore
\[
q_p(C+x,r+b,T)=(1-p)q_p(C,r,T),
\]
and similarly with x,S and y,T interchanged. It follows that
\[
q_p(C,r,S)q_p(C+x,r+b,T)
=(1-p)q_p(C,r,S)q_p(C,r,T)
=q_p(C,r,T)q_p(C+y,r+c,S).
\tag{3}
\]
This holds for every inherited marking and both arbitrary newborn bits b,c. It includes S=T=C and the empty base; these second precursors are still proper in their intermediate parents. Full ideals remain present in every normalized row and can occur as first precursors.

The newborn mark remains independently fair, whatever the structural parameter p. Define
\[
\mathcal B^{P,r}_{S,b}(X)=\frac{q_p(P,r,S)}2X.
\]
Both complete two-step routes in (3) multiply the same transported payload by the same scalar times 1/4. Thus their unnormalized maps agree on every admitted complex positive-semidefinite X, not just on normalized or diagonal states. Summing all ideal/bit branches gives X by (2). No trace division or informative quantum dynamics is introduced.

Normalized positive finite history weights
\[
2^{-N}\prod_{n=0}^{N-1}q_p(P_n,r_n,S_n)
\]
are consistent under truncation. The usual probability extension on the finitely branching history tree supplies an infinite classical law L_p. Each individual transition still has a finite parent. This verifies the model directly, without importing a differently named axiom from the primary paper.

### 4. Maximal count and width for each fixed interior p

Let F_n contain the complete marked history through n births, \(M_n=|\operatorname{Max}(P_n)|\), and W_n be its maximum antichain size. Set M_0=W_0=0.

In the conditional subset representation, an old maximum is in the precursor exactly when selected. Selected maxima cease being maximal; unselected maxima survive. Old nonmaxima retain an old successor, and the newborn is maximal. Consequently
\[
M_{n+1}\mid F_n\ \sim\ 1+\operatorname{Binomial}(M_n,1-p),
\tag{4}
\]
or explicitly
\[
\Pr_p(M_{n+1}=j\mid F_n)
=\binom{M_n}{j-1}(1-p)^{j-1}p^{M_n-j+1},
\quad 1\le j\le M_n+1.
\]
The empty parent gives M_1=1. The singleton gives M_2=1 with probability p and M_2=2 with probability 1-p. All committed marks stay in F_n; the next bit remains a separate fair branch.

For fixed k≥1, if the current count is r<k, require no current maximum to be selected until first reaching k. Successive conditioning gives probability
\[
(1-p)^{\sum_{m=r}^{k-1}m}
\ge \delta_{k,p}:=(1-p)^{k(k-1)/2}>0
\tag{5}
\]
of this successful run. It lasts k-r≤k births. This bound is uniform over every complete current history below k for the fixed p and k.

For deterministic N≥0, let
\(\sigma_{N,k}=\inf\{j\ge0:M_{N+j}\ge k\}\).
Condition at successive k-step block boundaries. On the event of no previous hit the count is still below k, so the next block fails with conditional probability at most \(1-\delta_{k,p}\). The tower property gives, for every integer b≥1,
\[
\Pr_p(\sigma_{N,k}>bk\mid F_N)
\le(1-\delta_{k,p})^b.
\tag{6}
\]
No independent-block assumption is made. If the count already exceeds the threshold, failure is empty. For k=1, delta is one and hitting occurs by the next birth, including from the empty parent.

Letting b increase and intersecting the probability-one conclusions over countably many N,k proves
\[
\limsup_n M_n=\infty \quad L_p\text{-almost surely}.
\]
Old induced relations persist, so W_n is nondecreasing; maximal vertices form an antichain, so W_n≥M_n. Therefore
\[
W_n\longrightarrow\infty \quad L_p\text{-almost surely}.
\tag{7}
\]
This extends the accepted Part S argument to every fixed interior p under its own law. The bound depends on p; for k≥2 it tends to zero as p approaches one. No bound uniform over the whole open parameter interval, stationary distribution, asymptotic rate or assertion \(M_n\to\infty\) is supplied.

### 5. Different parameters are different finite laws

Let E be the intrinsic event that the first two vertices form a chain, with both marks forgotten. The first birth is forced. From its singleton parent the full ideal has probability p and creates a chain; the empty ideal has probability 1-p and creates a two-antichain. Summing all four fair mark assignments gives
\[
\Pr_{L_p}(E)=p,\qquad
\Pr_{L_p}(E^c)=1-p.
\tag{8}
\]
Hence p≠p' implies different distributions already at two births. Vertex relabeling, order-coordinate changes preserving the order, and mark renaming preserve comparability, so they cannot remove this difference. Reparameterizing the name of p does not identify two distinct probability measures.

This is a distinction in the declared formal record channel, not a supplied physical measurement. A single realization need not identify p with certainty; both outcomes have positive probability for every interior parameter.

At p=1/2, (1) is exactly the accepted q_* kernel. The other admitted values refute the assertion that the marked admission conditions force half-selection. They do not determine a preferred p. The fair newborn-bit probability remains 1/2 throughout and is a different part of the model.

The constant-p laws are only a subfamily of the unrestricted admitted family. For example, accepted Part S also supplies chain-tail continuations with eventually finite width; (7) excludes those from the interior constant-p family. We give no general parameterization of all admitted laws, nor an admission result for a state-dependent or varying p. Separately imposed seed coefficients are additional constraints and need not match (1).

### 6. Scope

The scalar kernel and ancestor-closure construction have the transitive-percolation antecedent identified in §1 of this part. The present yield is the explicit verification under the marked contract, the fixed-p width argument and the finite-law distinction, with no model-novelty or broader historical-priority claim.

No preferred law, physical clock/dimension/metric/gravity/readout, height/density classification, empirical DET validation, quantum reconstruction, efficient algorithm or universal untestability follows. Part S is accepted at its exact scope; the inherited Part P author’s recorded 65-second timing breach remains NONCOMPLIANT and unwaived.

Protected validation/custody, independent review, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary separation and all resource/execution/publication gates remain. Acceptance of this mathematical result supplies no execution or successor permission.

### 7. Premises and proof obligations

Status: the following premises and proof obligations accompany the independently reviewed and accepted result.

#### Model and accepted dependencies

- Part A gives the unrestricted scalar-passive binary-marked-order contract, with every actual ideal, strict positive normalized support, proper selected-mark locality, equivariance, complete transported marked diamonds, fair newborn bits and scalar identity payload maps.
- Part S supplies the accepted half-selection argument. It is a checked predecessor, not an assumption that all p work.
- Part R supplies the accepted finite-observation proof and premises. No stronger family classification or physical observation premise is imported.
- Existing authorization, resource and coordination boundaries remain in force; mathematical acceptance does not remove them.
- A constant p with0<p<1 is an explicit mathematical choice for the entire law. Structural p does not replace the independently fair newborn mark probability.

#### Literature evidence and limits

The literature attribution in §1 of this part follows a pinned paraphrase of a primary-source observation: Rideout and Sorkin, A Classical Sequential Growth Dynamics for Causal Sets, Phys.Rev.D61,024002(2000), arXiv:gr-qc/9904062v3 revised26June2004, section4.2 equation(6). It reports alpha_n=p^m(1-p)^(n-varpi) and independent ancestor selection followed by adding pasts.

The mapping is n=|P|, varpi=|S|, m=|Max(S)|, with the same selection p. This scalar formula and construction are prior transitive percolation. The proof author and independent reviewer read the supplied primary-source observation, not the primary page or PDF. The note's garbled-PDF/readable-HTML history remains attributed. No URL expansion, broader survey, novelty claim or claim of identical axiom systems is made.

#### Manual obligations discharged

1. The subset-closure event for an actual ideal S requires all its maxima selected, all outside vertices unselected, and leaves interior choices free. Its probability is q_p; disjoint closure events exhaust all subsets and normalize the complete ideal row.
2. Interior p makes every factor positive. Empty/full ideals and empty parent are retained. At p=0 or1 the singleton row loses strict support, so endpoints are excluded without relying on0^0.
3. Intrinsic counts give equivariance. Mark independence implies the required proper locality.
4. In any incomparable-birth diamond, the old second precursor retains size and maxima while parent size rises byone. Thus its q_p factor gains1-p; both routes have the same structural product. This includes all markings and empty/full/equal base ideals.
5. Fair newborn bits give the same1/4 factor on both complete two-step scalar maps. Complete one-step maps sum to identity on every admitted complex positive-semidefinite payload. Consistent normalized finite cylinders supply L_p.
6. Unselected old maxima survive, selected maxima cease being maximal, old nonmaxima retain successors and the newborn is maximal. Hence conditional count is1+Binomial(M_n,1-p), including empty/singleton cases.
7. For each fixed p,k the successful run from r<k has probability(1-p)^(sum fromr tok-1ofm), at least delta_(k,p)=(1-p)^(k(k-1)/2). Conditional block iteration gives failure at most(1-delta_(k,p))^b, with no block independence.
8. Countable deterministic N,k hitting conclusions imply limsupM_n=infinity. Nondecreasing width and W_n>=M_n give W_n→infinity under each fixed interior-p law. No uniform-in-p or stationary/rate result follows.
9. The intrinsic two-birth chain event has probabilityp after summing all fair marks. Different p therefore give distinct formal laws, not order/mark-coordinate renamings.
10. Half-selection is one member, not forced by admission. The larger family also contains the accepted eventually finite-width continuations, which are outside this interior constant-p subfamily.

#### Boundaries and review

No claim asserts that arbitrary varying/state-dependent p is admitted, that any p satisfies a separately fixed seed, or that the constant-p family classifies all laws. No preferred parameter, actual readout, physical dimension/clock/metric/gravity, quantum reconstruction, height/density classification, efficiency or empirical validation is supplied.

The checked obligations include the exact literature-note attribution, complete normalization, factor1-p diamonds, fair-mark/scalar-map embedding, survival parameter1-p, fixed-p uniformity of the block bound, and two-birth distinction. The proof and review retain their declared source-access and evidence limits.

The original author and review records retain their recovered packaging, display and readback failures. All inherited failures and the Part P author’s recorded 65-second NONCOMPLIANCE remain unwaived. All original custody, protected-validation, independent-review, ABSTAIN, Status M, zero-qualification, RET-only pause, Boundary separation and execution gates remain.

## U. Endpoint likelihood and birth-order information

**Acceptance and scope.** This part records the independently reviewed and accepted fixed-horizon endpoint-likelihood result for Part T’s constant-parameter family. Part A supplies the model, and Part R retains the finite-prefix identifiability limit. Statistical sufficiency does not recover the realized history or supply a physical observation channel.

Status: mathematics accepted following distinct independent review and coordinator disposition. Manual proof and finite examples only.

**Result.** At a declared fixed horizon N, forgetting birth labels loses no statistical information about p within the accepted constant-p family. Either the marked or unmarked terminal order up to isomorphism is sufficient. The intrinsic pair (number of covers, number of incomparable pairs) is already sufficient. This does not recover the realized history, supply a physical channel, or identify a law in the unrestricted admitted family.

### 1. Exact history and observation spaces

Fix one p in (0,1) for the entire law. Use the unrestricted scalar-passive marked contract of Part A and the accepted constant-p law of Part T, not the separately prescribed seed.

A canonical history h of N births is the sequence
\[
h=((S_1,b_1),\ldots,(S_N,b_N)).
\]
At birth j, the old carrier is [j-1], S_j is an actual ideal of its current order, and b_j is the independently fair immutable bit on the new vertex j. Its strict past is exactly S_j. Thus birth labels remain in the history; no ideal occurrences are quotient-identified. The empty history covers N=0.

The terminal marked order on [N] is naturally labeled: x<y implies x's label is smaller. It determines the whole history, since each prefix is its induced restriction and S_j is the strict past of j. Conversely every such marked order determines one legal history. Labels here are birth indices, not extra random names.

We consider two deterministic endpoint maps: T_m(h)=[C,r], retaining bits under mark-preserving order isomorphism, and T_u(h)=[C], forgetting bits as well as birth labels. Binary symbols are fixed, not identified by a global bit flip. N is fixed before observation and is a birth count, not physical time. No stopped or data-selected horizon is being analyzed.

### 2. Intrinsic likelihood factorization

Define L(C) as the number of cover relations x<y with no z satisfying x<z<y. Define I(C) as the number of unordered incomparable vertex pairs.

At birth j, Max(S_j) consists precisely of j's lower covers. Later births cannot insert an intermediate vertex below an existing j: every new vertex is maximal when born and relations between old vertices persist. Conversely any terminal vertex between x and j was already present at birth j. Therefore
\[
\sum_{j=1}^N|\operatorname{Max}(S_j)|=L(C).
\tag{1}
\]
Every older vertex outside S_j is incomparable with j, since j cannot precede an older vertex. Each terminal incomparable pair is counted once, when its later member is born. Hence
\[
\sum_{j=1}^N(j-1-|S_j|)=I(C).
\tag{2}
\]

The accepted row formula and fair bits now give the exact canonical-history mass
\[
\Pr_p(h)=2^{-N}\prod_{j=1}^N
p^{|\operatorname{Max}(S_j)|}(1-p)^{j-1-|S_j|}
=2^{-N}p^{L(C)}(1-p)^{I(C)}.
\tag{3}
\]
This is a product of complete unnormalized branch weights, not an inference from normalized terminal agreement. For any fixed incoming payload X, the composed scalar map is the same scalar in (3) times X. No informative quantum evolution is added. In particular, transitive comparable pairs that are not covers contribute neither exponent.

### 3. Multiplicities and automorphisms

Choose a representative C on an abstract N-element set V. Let e(C) count its natural labelings, namely order-preserving bijections lambda:V→[N], equivalently linear extensions. Let a(C)=|Aut(C)| and a_m(C,r)=|Aut(C,r)|. Empty-set conventions are e=a=a_m=1.

Each lambda produces a naturally labeled order by transporting C, and also its marks when retained. Two labelings lambda,mu produce exactly the same marked order on [N] iff mu inverse composed with lambda is an automorphism of (C,r). This proves that the fibers are precisely the automorphism orbits. The action on labelings is free: an automorphism fixing a bijective labeling fixes every vertex. Every orbit therefore has a_m elements. Consequently the number of compatible canonical marked histories is
\[
K_m(C,r)=e(C)/a_m(C,r).
\tag{4}
\]
There is no further division by N! or by mark permutations.

For an unmarked endpoint, the identical argument gives e(C)/a(C) naturally labeled structural orders. Each permits exactly 2^N bit vectors, all distinct canonical marked histories. Thus
\[
K_u(C)=2^Ne(C)/a(C).
\tag{5}
\]
All counts are independent of p. Multiplying (3) by the actual number of histories yields
\[
\Pr_p(T_m=[C,r])
=\frac{e(C)}{2^Na_m(C,r)}p^{L(C)}(1-p)^{I(C)},
\tag{6}
\]
\[
\Pr_p(T_u=[C])
=\frac{e(C)}{a(C)}p^{L(C)}(1-p)^{I(C)}.
\tag{7}
\]

As a consistency check for forgetting marks, Aut(C) acts on the 2^N markings. A marking orbit has size a/a_m, so summing a/a_m over marking orbits gives 2^N. Summing (6) over those orbits therefore gives (7).

An ordered list of named vertices in a chosen representative has e(C) possibilities, but it is not the canonical sample space: each canonical history appears a_m times when an endpoint identification is also specified. A uniform auxiliary choice among those identifications would give a uniform list among e(C) possibilities conditional on the marked endpoint. Without that declared lift, listing all extensions as distinct observed histories overcounts symmetries.

### 4. Conditional histories and precise sufficiency

All compatible histories have the same strictly positive mass (3). For t=T_m(h) or T_u(h), respectively,
\[
\Pr_p(h\mid T=t)=1/K_t
\quad\text{on the fiber }T^{-1}(t).
\tag{8}
\]
This conditional law is independent of p. Thus either endpoint is sufficient for p in this finite statistical family. More explicitly, an endpoint can be randomized into a compatible canonical history uniformly using a kernel independent of p; composing with its endpoint distribution reproduces the full history law. This concerns statistical information, not recovery of the actual forgotten history.

Likewise U(h)=(L(C),I(C)) is sufficient: all canonical histories in a U-fiber have the same mass, and their number is independent of p. No minimality or computational-cost result is needed.

For two parameters p,p', the history likelihood ratio, and the endpoint ratio for the observed endpoint, both equal
\[
(p/p')^{L(C)}
\big((1-p)/(1-p')\big)^{I(C)}.
\tag{9}
\]
The conditional proof (8), not this ratio alone, establishes the stated sufficiency.

Other history encodings need not be uniform. If E is a deterministic coarsening of canonical histories, then conditional on endpoint t its probability is
\[
\Pr_p(E=e\mid T=t)
=\frac{|E^{-1}(e)\cap T^{-1}(t)|}{K_t}.
\tag{10}
\]
For example, forgetting names at every prefix can merge unequal numbers of histories. This changes multiplicities but not their independence from p.

### 5. Complete small checks and negative controls

These are manual finite examples, not executed enumeration.

For N=0, the only endpoint and history have mass one; L=I=0. For N=1, the unmarked singleton has mass one and each marked singleton has mass 1/2. Both horizons carry no information about p.

For N=2:

| Endpoint | e | a | L | I | Unmarked mass |
| --- | ---: | ---: | ---: | ---: | --- |
| Chain | 1 | 1 | 1 | 0 | p |
| Antichain | 2 | 2 | 0 | 1 | 1-p |

Each of the four marked chain endpoints has mass p/4. On the antichain, the 00 and 11 endpoints have a_m=2 and mass (1-p)/4 each. The mixed-bit endpoint has a_m=1, K_m=2 and mass (1-p)/2. Its two canonical histories have birth-bit sequences 01 and 10 and conditional mass 1/2 each. These seven marked endpoint probabilities sum to one.

At N=3, the five unmarked types exhaust the possibilities:

| C | e | a | L | I | Endpoint mass |
| --- | ---: | ---: | ---: | ---: | --- |
| Antichain | 6 | 6 | 0 | 3 | (1-p)^3 |
| One edge and an isolate | 3 | 1 | 1 | 2 | 3p(1-p)^2 |
| One root below two leaves | 2 | 2 | 2 | 1 | p^2(1-p) |
| Two roots below one top | 2 | 2 | 2 | 1 | p^2(1-p) |
| Chain | 1 | 1 | 2 | 0 | p^2 |

With r=1-p, the sum is r^3+3pr^2+2p^2r+p^2=1, since p^2=p^2r+p^3. The chain has three comparable pairs but only two covers, confirming the cover exponent.

For the edge-plus-isolate endpoint, its three structural canonical histories have edges (1,2), (1,3), or (2,3). Exactly one has a two-chain prefix and two have a two-antichain prefix. Thus the two possible sequences of unmarked prefix isomorphism classes have conditional probabilities 1/3 and 2/3, not 1/2 each. All fair marks can be summed without changing this ratio.

Dropping e/a from the N=3 endpoint probabilities would count the edge-plus-isolate only once. The resulting total is 1-2p(1-p)^2, not one. Renormalizing these wrong weights changes the family. A p-independent multiplicity cancels from the likelihood ratio for a fixed observed endpoint; that cancellation does not license omitting it from sampling probabilities.

A genuinely information-losing coarsening is L alone. At N=3, L=2 groups the chain, fork and join, and
\[
\Pr_p(C\text{ is a chain}\mid L=2)
=\frac{1}{1+2(1-p)}=\frac1{3-2p}.
\tag{11}
\]
This depends on p, so L alone is not sufficient. The pair (L,I) avoids this loss.

### 6. Scope and limits

The result concerns a declared finite endpoint channel within one fixed parametric family. No sensor, physical time, geometry, quantum reconstruction, algorithmic advantage or novelty claim is supplied. Every finite canonical history and endpoint has positive probability for every interior p; one sample cannot identify p with certainty.

The larger admitted family remains underdetermined. Part R supplies accepted different chain-tail continuations matching any chosen deterministic finite prefix, hence matching these endpoint observations at that horizon. Sufficiency for p within this subfamily does not identify a unique unrestricted law or its infinite tail.

Part T supplies the independently reviewed and accepted family formula at its stated scope. Historical custody limits, display/parser failures and the Part P author's recorded 65-second NONCOMPLIANCE remain unwaived. Protected validation, independent review, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary and execution/publication gates remain. Acceptance of this mathematics does not grant scientific or operational execution authority.

### 7. Premises and manual obligations

Status: premises accepted with the preceding result following distinct independent review and coordinator disposition.

#### Accepted premises

1. Part A supplies the unrestricted scalar-passive order model with immutable binary marks, all actual ideals, complete normalized positive rows, selected-mark locality, equivariance, complete marked diamonds, independently fair newborn bits and scalar payload maps. Its separately prescribed numerical seed is not imposed on the comparison family.
2. Part T supplies the independently reviewed and accepted constant-parameter family at its exact stated scope. For each one fixed p in (0,1), q_p(P,r,S)=p^|Max(S)|(1-p)^(|P|-|S|) is admitted. The fair mark probability remains1/2.
3. Part R supplies the independently reviewed and accepted finite-prefix continuation theorem, used here only at deterministic horizons to delimit identifiability in the larger family. Its historical source copies establish exact content identity, without asserting original-path identity through intermediate copies.
4. Existing authorization, resource and coordination boundaries remain in force. Mathematical acceptance does not grant execution authority or waive a later resource ambiguity.
5. The result retains its declared source and evidence limits. No new source access or reconstruction of historical custody is claimed by this presentation.

#### Explicit statistical choices

N is a deterministic declared nonnegative integer, fixed before data. A canonical history contains every actual ideal S_j on old birth labels[ j-1 ] and every fair bit b_j. It is equivalent to one naturally birth-labeled marked terminal order on[N]. No auxiliary ancestor-selection subset, named-vertex identification or physical observation is included in this sample space.

The marked endpoint forgets birth labels up to mark-preserving order isomorphism; the unmarked endpoint additionally forgets all bits. Bit names0 and1 remain distinct for marked isomorphism. The incoming scalar-passive payload is fixed, not a parameter-dependent side channel. A birth index is not physical time or a claim that every present activity commits a record.

Standard finite probability, fiber counting and free finite-group actions are mathematical tools. No external physical premise is added.

#### Manual proof obligations discharged

- Every precursor maximum is exactly a lower cover of the new vertex. Later maximal births cannot insert vertices into old intervals. Summing precursor maxima gives terminal cover countL.
- Every older vertex outside the precursor is incomparable with the new vertex. Each unordered incomparable pair is counted at its later birth. Summing outside counts gives terminalI.
- Complete marked-history mass is2^-N p^L(1-p)^I, including the empty history. The corresponding composed unnormalized scalar payload map has that coefficient.
- Labelings of a fixed representative give the same natural labeled marked endpoint exactly along Aut(C,r) orbits. The action is free, so the marked canonical-history count is e(C)/a_m. The unmarked structural count is e(C)/a, with2^N independent mark vectors per structural history.
- Endpoint multiplicities are independent ofp. Mark-orbit counting gives sum a/a_m=2^N, checking agreement of the marked and unmarked formulas.
- Conditional on either endpoint, canonical histories are uniform over the compatible fiber independently ofp. The count pair(L,I) also has this property, establishing finite statistical sufficiency within the fixed-p family.
- Other history encodings push forward this uniform conditional law with their own fiber multiplicities. Uniformity does not transfer automatically to lists of named extensions or sequences of unmarked prefix classes.
- N=0,1,2 are checked completely, including the symmetric mixed-bit two-antichain. All five unmarked N=3 endpoint types give a normalized table.
- Edge-plus-isolate has three canonical structural histories but only two unmarked prefix-class sequences with multiplicities1 and2. Dropping its factor3 breaks normalization.
- L alone loses parameter information: at N=3, conditional chain probability givenL=2 is1/(3-2p). Correct endpoint multiplicities cancel from likelihood ratios for a fixed outcome but remain necessary for the probability law.

#### Limits, provenance and review

No assertion concerns a stopped/random horizon, empirical channel, preferredp, unrestricted-law classification, physical clock/geometry/gravity, quantum derivation, efficient counting or algorithmic advantage. Sufficiency permits a p-independent conditional reconstruction in distribution, not recovery of the actual hidden history. Full finite support prevents certainty aboutp from one endpoint. Part R's matching continuations prevent promotion to unrestricted-law or tail identifiability.

The original proof and distinct review records retain their recovered display, parser and readback failures, input-identity checks and completion-evidence limits. Inherited failures and the Part P author's 65-second substantive breach remain unwaived. Hash/readback checks establish artifact identity, not mathematical correctness or reconstructed historical custody.

All protected-validation/custody, independent-review, ABSTAIN, StatusM, zeroqualification, RET-only pause, Boundary and execution/publication gates remain. Acceptance of the stated mathematics does not remove these requirements.

## V. Bounded stopping, weighted endpoints and censoring

**Acceptance and scope.** This part records the independently reviewed and accepted bounded-stopping endpoint result for Part T’s constant-parameter family. Part A supplies the model, Part U supplies the fixed-horizon likelihood and symmetry counts, and Part R retains the finite-prefix identifiability limit. Correct stopping weights preserve endpoint information; erasing a censored endpoint can destroy it. No missing physical observation is supplied by the theorem.

Status: mathematics accepted following distinct independent review and coordinator disposition. Manual finite proof and examples only.

**Result.** For a known parameter-independent stopping design capped at a finite birth horizon H, a retained marked or unmarked stopped endpoint remains sufficient for p in the accepted constant-p family. Compatible histories generally have unequal, design-dependent weights. Replacing censored endpoints by a common symbol can destroy sufficiency, even when the censor probability itself is independent of p.

### 1. Experiment and full stopped record

Fix H≥0 and one unknown p in (0,1). The growth law is the accepted constant-p scalar-passive family, with independently fair immutable bits and canonical histories h_t of actual precursor ideals and newborn marks on birth labels1,...,t. For terminal order C(h_t), the accepted result of Part U gives
\[
f_p(h_t)=2^{-t}p^{L(C(h_t))}(1-p)^{I(C(h_t))},
\tag{1}
\]
where L counts covers and I counts unordered incomparable pairs.

Declare a finite seed space E and a known distribution nu on E, independent of p and the entire growth history. A seed eta can encode all finite random decisions. Declare known functions
\[
d_t(h_t,\eta)\in\{0,1\},\qquad 0\le t\le H,
\]
which request stopping using only the current prefix and seed. History-dependent decisions are permitted. The rule neither intervenes on growth nor reads its unknown parameter or future. Fixed design constants are allowed even if chosen using a named reference value p_0; they remain unchanged when the true p varies.

If any request occurs, T is its first index and J=1. If none occurs through H, force T=H and set J=0, the censor indicator. A request at H has J=1, distinct from censoring at H. The complete stopped record compared here is
\[
X=(\eta,T,J,h_T).
\]
It contains no growth after T. The full H-birth history used below is only a finite normalization device, not extra observed evidence.

For either marked or unmarked order isomorphism, the retained-endpoint channel is
\[
Y=(T,J,[C(h_T)]).
\tag{2}
\]
Marked isomorphisms preserve bits; unmarked ones forget them. H and the design are known protocol data. The passive incoming payload is fixed, not a parameter-dependent side channel. Birth counts are not physical time.

### 2. Stop compatibility and normalization

For a candidate h_t, let h_k denote its prefix. Define
\[
A_{t,1}(h_t,\eta)
=\left[\prod_{k=0}^{t-1}(1-d_k(h_k,\eta))\right]d_t(h_t,\eta),
\tag{3}
\]
\[
A_{t,0}(h_t,\eta)
=\mathbf1_{\{t=H\}}\prod_{k=0}^{H}(1-d_k(h_k,\eta)).
\tag{4}
\]
Equation(4) is defined as zero for t<H, without evaluating unavailable prefixes. Empty products equal one. These indicators include every no-earlier-stop condition; they do not assume independent decisions.

For each complete h_H and seed,
\[
\sum_{t=0}^{H}A_{t,1}(h_t,\eta)+A_{H,0}(h_H,\eta)=1.
\tag{5}
\]
This partitions outcomes by the first request or the cap. Normalized finite growth rows and sum nu=1 make the H-history/seed experiment normalized. Summing its future continuations from any compatible stopped prefix contributes one. Therefore
\[
\Pr_p(X=(\eta,t,j,h))
=\nu(\eta)A_{t,j}(h,\eta)\,
2^{-t}p^{L(C(h))}(1-p)^{I(C(h))}.
\tag{6}
\]
Summing(6) over all finite stopped records gives one by(5). No conditioning on successful stopping, discarding censor mass, or separate normalization at each length is performed.

### 3. Weighted multiplicity and conditional reconstruction

Set
\[
w_{t,j}(h)=\sum_{\eta\in E}\nu(\eta)A_{t,j}(h,\eta).
\]
For endpoint class c of size t, let H_t(c) be all compatible canonical marked histories before applying the stopping rule. For an unmarked c this includes every bit vector. Define the weighted multiplicity
\[
W_{t,j}(c)=\sum_{h\in H_t(c)}w_{t,j}(h).
\tag{7}
\]
It depends on the declared design, not on p, and need not be an integer. Summing(6) gives
\[
\Pr_p(Y=(t,j,c))
=2^{-t}W_{t,j}(c)\,p^{L(c)}(1-p)^{I(c)}.
\tag{8}
\]
The probabilities over all lengths, indicators and endpoint classes sum to one. A zero W makes an output impossible for every p; it is not conditioned upon.

For positive W, the exact conditional law is
\[
\Pr_p(X=(\eta,t,j,h)\mid Y=(t,j,c))
=\frac{\nu(\eta)A_{t,j}(h,\eta)}{W_{t,j}(c)}
\quad(h\in H_t(c)).
\tag{9}
\]
Its history marginal is w(h)/W, generally not uniform. Both are independent of p. Thus Y is sufficient relative to the full stopped record X: the kernel(9), composed with its endpoint law, reconstructs the full stopped-record distribution. It does not recover the actual hidden history or any unobserved future.

Changing the encoding requires summing these weights over the corresponding fibers, not assigning equal probabilities to different descriptions.

The old automorphism factors can be used only inside a weighted sum. For a marked representative (C,r), natural labelings lambda produce histories h_lambda, and
\[
W_{t,j}([C,r])
=\frac1{|\operatorname{Aut}(C,r)|}
\sum_{\lambda}w_{t,j}(h_\lambda).
\tag{10}
\]
The accepted free action shows each canonical history appears exactly |Aut(C,r)| times; repeated descriptions have the same weight. For an unmarked representative,
\[
W_{t,j}([C])
=\frac1{|\operatorname{Aut}(C)|}
\sum_{\lambda}\sum_{b\in\{0,1\}^t}w_{t,j}(h_{\lambda,b}).
\tag{11}
\]
Here b is the birth-index bit vector. Each canonical marked history is repeated exactly |Aut(C)| times. No extra factorial is inserted, and mark-dependent rules do not license replacing the inner sum by 2^t times a selected representative. The fixed-horizon counts return when all relevant w equal one.

T is recoverable from endpoint size. Retaining J makes the protocol explicit, but J is not mathematically essential when the complete endpoint is retained: summing W over j leaves the same p-dependent factor in(8) and a p-independent conditional kernel. This does not justify omitting endpoints on censored branches. Known design data are kept fixed throughout.

### 4. Complete weighted example

Take H=3, a fair independent seed eta in{0,1}, and request stopping only at t=2 when the two-vertex prefix is a chain and eta=1. All other d_t are zero. Every surviving run is censored at3.

After summing fair marks, all outcomes are:

| T,J,unmarked endpoint | Probability |
| --- | --- |
| 2,1,chain | p/2 |
| 3,0,antichain | (1-p)^3 |
| 3,0,one edge and an isolate | (5/2)p(1-p)^2 |
| 3,0,fork | p^2(1-p)/2 |
| 3,0,join | p^2(1-p) |
| 3,0,chain | p^2/2 |

To see the noninteger structural factor, the three naturally labeled edge-plus-isolate histories have their edge at(1,2),(1,3),or(2,3). Their survival weights are1/2,1,1: only the first has a chain prefix at2. Thus their conditional probabilities given that censored endpoint are1/5,2/5,2/5. The canonical marked-history W is 2^3(1/2+1+1)=20, giving coefficient20/8=5/2. The five compatible structural-history/seed pairs each have conditional mass1/5; fair marks remain independent in this particular design.

The other rows follow from the complete five-type N=3 table in Part U: the fork and chain have chain prefixes and lose half their mass, while the antichain and join have antichain prefixes. Relative to that normalized table, the removed mass is
\[
\tfrac12[p(1-p)^2+p^2(1-p)+p^2]=p/2,
\]
exactly the early-stop row. Thus the displayed different-length probabilities sum to one. Applying the old unweighted e/Aut count to the censored endpoint would be wrong.

At H=0, (3)–(5) split the unique empty history into request/censor outcomes with total mass one. At H=1, all underlying prefix masses are p-independent, so every such fixed design remains p-independent. These cases require no positive-length convention.

### 5. Censor-only negative control

Compare two output channels of the same full stopped experiment X. Take H=2 and an independent fair seed. Request stopping at1 iff eta=1; make no other request. Then eta=0 runs are censored at2.

The endpoint-retaining unmarked channel has the complete law
\[
\Pr(Y=(1,1,\text{singleton}))=\tfrac12,\quad
\Pr(Y=(2,0,\text{chain}))=\tfrac p2,\quad
\Pr(Y=(2,0,\text{antichain}))=\tfrac{1-p}{2}.
\tag{12}
\]
In full marked records, the two early singleton bits each have mass1/4; the four censored chain bit vectors each have massp/8, and the four censored antichain bit vectors each have mass(1-p)/8. Their total is one. Marked symmetric endpoints aggregate those vectors as in Part U.

Now report Z=Y for J=1, but Z=Delta for every J=0, discarding its endpoint. Then
\[
\Pr_p(Z=(1,1,\text{singleton}))=\tfrac12,\qquad
\Pr_p(Z=\Delta)=\tfrac12.
\tag{13}
\]
This law is identical for every p, while
\[
\Pr_p(C(h_T)\text{ is a chain}\mid Z=\Delta)=p.
\tag{14}
\]
Consequently Z is not sufficient for X: its conditional missing record depends on p. Indeed a fixed reconstruction kernel applied to the p-independent law(13) could not reproduce the p-dependent law(12). Reporting the known censor count2 and indicator alongside Delta does not repair the loss.

This compares a record-retaining censor protocol with its explicit erasure channel. If an actual protocol never acquires the censored endpoint, its observation is Z; missing evidence must not be silently treated as Y. No physical sensor implementation is asserted.

### 6. Limits

The conclusion requires a known finite design whose rule and seed distribution are independent of the unknown true p. Decisions can depend on observed history, whose distribution depends on p; this does not make the rule itself parameter-dependent. If the rule or seed distribution changes with the unknown p, factors nu and A may no longer cancel in(9), and this theorem provides no guarantee.

All results are confined to finite H and the specified constant-p family. Every feasible stopped record has positive probability for all interior p, so one record supplies no certainty about p. Part R's accepted finite-prefix matching still supplies other admitted laws with exactly the same bounded experiment under the same independent seed. No unique unrestricted law or infinite-tail identification follows.

There is no unbounded-stopping, nontermination, optional-stopping asymptotic, confidence-sequence, physical-time/geometry/quantum, efficient-algorithm or novelty claim. The examples are manual, not executed enumeration. Inherited custody/failure limits and the Part P author's recorded 65-second NONCOMPLIANCE remain unwaived. Protected validation, independent review, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary and execution/publication gates remain. Acceptance of this mathematics grants no scientific or operational execution authority.

### 7. Premises and proof obligations

Status: premises accepted with the preceding result following distinct independent review and coordinator disposition.

#### Accepted source boundary

- Part A supplies the unrestricted scalar-passive marked order contract. The constant-p comparison family does not impose that source's separately fixed seed or continuation.
- Part U supplies the independently reviewed and accepted fixed-horizon endpoint result at its exact stated scope. The underlying report, premises and review retain their exact-content and original-locator joins to the actual acceptance.
- Part U supplies f_p(h_t)=2^-t p^L(C)(1-p)^I(C), covers and unordered incomparable-pair statistics, and the free automorphism action on natural labelings. Its fixed-horizon sufficiency alone does not prove the present stopped result.
- Part R supplies the independently reviewed and accepted finite-prefix matching result. Its historical source copies establish exact content identity through intermediate copies, without asserting original-path identity. Only its exact finite-prefix matching scope is used here.
- Existing resource and coordination boundaries remain in force. A historical resource authorization does not excuse a later ambiguity, and mathematical acceptance does not grant execution authority.
- The result retains its declared source-access limits. No new source access, nested acquisition or reconstruction of historical sessions is claimed by this presentation.

#### Explicit observation assumptions

H is a predeclared deterministic finite nonnegative birth count. One unknown interior p governs all growth rows. Canonical histories retain each actual precursor ideal on birth labels and each independently fair immutable bit. The scalar incoming payload is fixed.

The known auxiliary seed has a finite space E and one known probability law nu, independent of p and growth. All random decisions can be encoded in that seed. For each0≤t≤H, a known deterministic decision d_t(h_t,eta) reads only the current canonical prefix and seed. It may depend on history and fixed design constants, but not the unknown true p or future. Stopping does not intervene on the growth kernels.

T is the first request time within0,...,H, orH if there is none. J=1 denotes a request, including atH; J=0 denotes forced censoring atH. Full compared record X=(eta,T,J,h_T) excludes all growth afterT. A complete H-history is used only to prove finite normalization.

Retained endpoint Y=(T,J,[C(h_T)]) may preserve marks or forget them. Isomorphisms never change retained bit values. Endpoint size already determinesT. J can be summed out without losing the factorization if the endpoint itself remains available. H and the known design are protocol information, not unknown nuisance parameters.

#### Manual obligations discharged

1. A_(t,1) is the product of no-earlier-stop indicators times the request at t. A_(H,0) is the product of no request throughH; A_(t,0)=0 for t<H. No unavailable future prefix is evaluated.
2. For each full finite history/seed, first-request events and cap partition the sample space. Summing normalized future continuations gives exact stopped-record mass nu(eta)A2^-t p^L(1-p)^I. Mass across all lengths and both indicators remains one.
3. The marginalized design weight is w(h)=sum_eta nu(eta)A(h,eta). Endpoint W sums w over all canonical marked histories, including all bit vectors for unmarked endpoints.
4. Endpoint probability is2^-t W p^L(1-p)^I. W is independent ofp but need not be integral. W=0 excludes that output for everyp; no conditional probability is asserted there.
5. Conditional full records have weight nu A/W and conditional histories have weight w/W, independently ofp. This gives reconstruction in distribution for the stopped record only, not actual-history recovery or future reconstruction.
6. Natural labelings repeat each canonical marked history exactly |Aut(C,r)| times, or each unmarked structural history |Aut(C)| times. Weighted label sums divide by those proved multiplicities; bit vectors remain explicitly summed when the rule can read marks.
7. Further history encodings require sums of weights over their fibers. Neither randomization nor selective stopping preserves uniformity automatically.
8. The complete H=3 example stops half the two-chain prefixes. Its six unmarked outcome rows normalize, and the censored edge/isolate histories have weights1/2,1,1, giving conditional probabilities1/5,2/5,2/5 and marked-history W=20.
9. H=0 empty-product conventions partition the empty history; H=1 contributes no p-dependent underlying growth evidence.
10. The H=2 fair early-stop/censor experiment has endpoint masses1/2,p/2,(1-p)/2. Erasing the censored endpoint yields the p-independent two-outcome law1/2,1/2, while the missing conditional chain probability isp. This refutes sufficiency of censor-only output for that same full experiment.

#### Limits and preserved evidence

No result extends to unbounded stopping, optional-stopping asymptotics, nontermination, confidence sequences, physical sensor/clock design, quantum or gravity claims, efficient counting, benchmarks or novelty. Finite-horizon normalization is a direct partition argument. Known policy dependence is distinct from dependence on the unknown true parameter.

Sufficiency holds inside the stated fixed-p family and channel. Part R's matching continuations preserve the whole bounded experiment with the same independent seed, so unrestricted-law and tail identification remain unsupported. A censor-only channel is not supplied a missing endpoint by assumption.

The original theorem record retains its twelve complete source/control captures and exact native input checks, with no current author tool/read failure reported. The distinct review retains its two recovered control/metadata display truncations and actual checks. Historical display/parser/custody limits and the Part P author's recorded 65-second NONCOMPLIANCE remain unwaived. Readback and hashes establish artifact identity, not mathematical truth or reconstructed historical custody.

All protected-validation/custody, independent-review, ABSTAIN, StatusM, zeroqualification, RET-only pause, Boundary and execution/publication gates remain. Acceptance of the stated mathematics does not remove these requirements.

## W. Intrinsic comparable-pair density

**Acceptance and scope.** This part records the independently reviewed and accepted intrinsic order-density theorem for each fixed interior parameter in Part T's family. Part A supplies the unrestricted marked contract, Part T supplies the accepted kernel and unbounded-width result, and Part U supplies the intrinsic pair-count convention. The density limit is a result about that family; it neither selects the family nor supplies a calibrated physical dimension. Part V's stopped observation theorem is a closed predecessor, not a premise of this geometry proof.

Status: mathematics accepted following distinct independent review and coordinator disposition. Manual mathematics only.

**Result.** Under every one fixed interior-p law in the admitted family,
\[
R_N:=1-\frac{I_N}{\binom N2}\longrightarrow1
\quad\text{almost surely}.
\]
Here I_N counts unordered incomparable pairs in the N-vertex order. An explicit bound is
\[
\mathbb E_p[1-R_N]\le
\min\left\{1,\frac{2(1-p)}{Np^2}\right\},\qquad N\ge2.
\tag{1}
\]
This common limiting statistic does not distinguish fixed parameters. It coexists with unbounded width and supplies no manifold dimension.

### 1. Family and intrinsic quantity

Fix p in (0,1) once for the entire infinite law. The admitted kernel is
\[
q_p(P,r,S)=p^{|\operatorname{Max}(S)|}(1-p)^{|P|-|S|},
\tag{2}
\]
on every actual ideal S, with independently fair immutable bits and scalar payload branches q_p/2. This is the unrestricted comparison family accepted in Part T, not the separately fixed seed or continuation in Part A.

For the order P_N after N births, I_N is the number of unordered pairs with neither vertex preceding the other. R_N is their complementary fraction among all distinct unordered pairs. Both depend only on the unmarked order up to isomorphism. Set I_0=I_1=0; the ratio is defined only for N≥2. Birth labels below organize a proof, not metric coordinates or physical time.

Part U supplies the intrinsic statistic convention. Part V closes the stopped-result predecessor; its observation theorem is not a premise for this geometry calculation.

### 2. Exact coupling before using independent edges

On a mathematical probability space take mutually independent Bernoulli(p) variables E_ij for all positive integers i<j, and independent fair bits b_j. Draw an oriented edge i→j when E_ij=1. On[ N ], take the transitive closure of these forward edges as P_N and attach b_1,...,b_N.

Forward labels make the graph acyclic. A path between old vertices cannot use a later-born vertex, so old induced orders remain fixed as N grows. At birth j the selected old vertices are
\[
A_j=\{i<j:E_{ij}=1\},
\]
and j's strict past is exactly the downward closure of A_j in P_(j-1).

Conditional on the entire old canonical marked history, all incoming E_ij remain independent Bernoulli(p): that history is a function only of old edges and old bits, disjoint from these new variables. For any old ideal S, its closure is exactly S iff every maximum of S is selected and every old vertex outside S is unselected. All other choices in S are free. Thus the conditional probability is precisely(2).

These closure events partition all subsets of the old carrier, so every actual ideal is included and the complete row sums to one. Interior p gives strict positivity. Empty and full ideals have probabilities(1-p)^|P| and p^|Max(P)|; the empty-parent row is one. The next bit is independently fair. Therefore every complete marked branch has the accepted coefficient q_p/2 and the same scalar action on the fixed payload.

Induction gives equality with the admitted law for every finite canonical marked history, not just terminal summaries. The countable edge/bit construction consequently pushes forward to the same infinite history law on its cylinder-generated sigma-algebra. Its almost-sure conclusions about the sequence P_N therefore apply to that law.

Auxiliary edges are not newly committed observations or a physical mechanism. This verifies an exact representation of the already chosen law; it does not choose p or derive this family uniquely from DET.

### 3. Birth-gap connection bound

Write a=1-p^2 and q=1-p. Fix i<j and gap g=j-i. The direct edge i→j suffices for comparability. Each k with i<k<j also gives a sufficient two-edge path i→k→j when E_ik=E_kj=1.

For distinct intermediate k, these events use disjoint pairs of edge variables, so they are mutually independent with probability p^2. They are also independent of the direct edge. Sharing endpoint vertices does not mean sharing edge variables.

Incomparability implies failure of the direct edge and of every such two-edge path. Hence
\[
\Pr_p(i\mathrel{\|}j)
\le q\,a^{g-1}.
\tag{3}
\]
Longer paths can only reduce the incomparability probability. We do not assume independence between different pairs' incomparability events.

For g=1 the bound is exactly q. For g=2, the direct and single two-edge paths exhaust all possible paths, so the bound q(1-p^2) is also exact. At larger gaps(3) is an upper bound, not an exact reachability formula.

### 4. Explicit finite-N bounds

There are N-g pairs with gap g. Linearity of expectation, without pair independence, gives
\[
\mathbb E_p I_N
\le q\sum_{g=1}^{N-1}(N-g)a^{g-1}
\le \frac{q(N-1)}{p^2}.
\tag{4}
\]
The last inequality uses N-g≤N-1 and the convergent geometric sum1/(1-a)=1/p^2. Dividing by N(N-1)/2 proves(1). For every epsilon>0, Markov's inequality also gives
\[
\Pr_p(1-R_N>\epsilon)
\le\min\left\{1,\frac{2(1-p)}{\epsilon Np^2}\right\}.
\tag{5}
\]

These are explicit, nonoptimal bounds with their parameter dependence visible. They imply convergence in mean and in probability for every fixed p. They do not by themselves prove almost-sure convergence.

Manual small checks: at N=2, I_2 is one exactly when the direct edge is absent, so E I_2=q and E R_2=p. At N=3, two pairs have gap1 and one has gap2, giving the exact value
\[
\mathbb E I_3=2q+q(1-p^2)=q(3-p^2).
\]
This agrees with the finite gap sum in(4) before its geometric relaxation. Fair marks sum to one and affect neither count. No examples were generated by enumeration code.

### 5. Almost-sure passage, with interpolation

Let D_N=1-R_N≥0. For each fixed epsilon>0, (5) on the square subsequence N=m^2, m≥2, gives
\[
\sum_{m=2}^{\infty}
\Pr_p(D_{m^2}>\epsilon)
\le\frac{2q}{\epsilon p^2}
\sum_{m=2}^{\infty}m^{-2}<\infty.
\tag{6}
\]
The first Borel–Cantelli implication follows directly from the union bound on tail events: their tail sum tends to zero, so only finitely many exceedances occur almost surely. No independence is required. Intersecting these probability-one statements for epsilon=1/k, k=1,2,..., yields D_(m^2)→0 almost surely.

Old incomparable pairs persist, so I_N is nondecreasing. The normalized fraction D_N need not be monotone; we do not use that assertion. For m^2≤N≤(m+1)^2,
\[
0\le D_N
\le\frac{I_{(m+1)^2}}{\binom{m^2}{2}}
=D_{(m+1)^2}
\frac{\binom{(m+1)^2}{2}}{\binom{m^2}{2}}.
\tag{7}
\]
For m≥2 the denominator is positive, and the binomial ratio tends to one. Thus the square-subsequence conclusion controls every sufficiently large N. This proves D_N→0, and hence R_N→1, almost surely for each fixed p under its own law.

### 6. Why unbounded width is consistent

Let W_N be the largest antichain size. Part T gives W_N→infinity almost surely for every fixed interior p. Every pair inside an antichain is incomparable, so
\[
\binom{W_N}{2}\le I_N.
\tag{8}
\]
Together with I_N/N^2→0, this implies W_N/N→0 almost surely: indeed
\[
(W_N/N)^2\le 2I_N/N^2+1/N.
\]
Intersecting with the accepted width event gives both
\[
W_N\to\infty,\qquad W_N/N\to0
\]
on a probability-one set.

There is no contradiction. Antichains become arbitrarily large while occupying a vanishing fraction of vertices, and incomparable pairs occupy a vanishing fraction of all pairs. The order need not eventually be a chain; in this family its diverging width rules that out. Existing incomparable pairs are not erased. No optimal width rate or full shape classification is asserted.

### 7. What the limit cannot identify

All fixed p in(0,1) produce the same limiting value1. Observing only that limit therefore cannot separate them. This does not identify their probability laws: already R_2 is Bernoulli(p). Finite-N distributions and bounds retain parameter dependence, and this packet analyzes no estimator based on fluctuations or rates.

The conclusion is not uniform over the entire open parameter interval. For a concrete distinction, let each N≥2 be sampled under its own constant parameter p_N=N^-3. In that N-vertex coupling,
\[
\Pr_{p_N}(\text{any edge})
\le\binom N2p_N=\frac{N-1}{2N^2}\longrightarrow0.
\tag{9}
\]
With no edge the order is an antichain and R_N=0. Thus these different finite experiments have R_N→0 in probability, rather than1. This is a triangular sequence of already admitted constant-parameter laws, not one law with a time-varying transition parameter and not a new admission claim.

The theorem also does not cover every law allowed by the broader marked contract. It supplies no unique law selection, physical readout, continuum limit, manifold embedding or1D/4D spacetime inference. An intrinsic order-density limit is not a calibrated dimension map, metric, gravity result or quantum reconstruction.

The family's conventional transitive-percolation antecedent remains as recorded in Part T. No fresh primary-source read, bibliographic assertion, DET-specific mechanism or novelty claim is made.

All inherited failures/custody limits and the Part P author's recorded 65-second NONCOMPLIANCE remain unwaived. Protected validation, independent review, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary and execution/publication gates remain. Acceptance of this mathematics grants no scientific or operational execution authority; any successor requires its own review and coordinator disposition.

### 8. Premises and proof obligations

Status: mathematics accepted following distinct independent review and coordinator disposition.

#### Supplied premises and exact joins

- Part A supplies the unrestricted scalar-passive marked order model. Its separately prescribed seed is not imposed on the constant-p comparison family.
- Part T supplies the independently reviewed and accepted family result. The original source report, premises and review join its actual acceptance by exact byte size and SHA256. Their provenance locators name intermediate copies, so original-path identity is not claimed.
- That accepted scope gives q_p(P,r,S)=p^|Max(S)|(1-p)^(|P|-|S|) for every actual ideal, independent fair marks and scalar branch maps, for each fixed interior p. It also gives W_N→infinity almost surely and the finite two-birth distinction.
- Part U supplies the accepted endpoint result. Its source report joins the actual acceptance by original locator, size and hash. It is used for intrinsic cover/incomparable statistics, not as a proof of an asymptotic density theorem.
- Part V's actual acceptance was read and pinned in the original proof only to record predecessor closure. Its author/reviewer files were not reopened there, and its observation theorem is not a geometry premise.
- The original authorizations and assignment preserve scope and usage boundaries. Both original control hashes/sizes matched their dispatch pins.
- The original proof used only its ten literal inputs and two controls; no nested file, URL or historical session was followed.

#### Explicit mathematical choices

One p in(0,1) is fixed for an entire infinite growth law. R_N is defined only for deterministic N≥2 as1-I_N/binom(N,2), with I_N the unordered incomparable-pair count. I_0=I_1=0 without defining a zero-denominator ratio.

The proof constructs independent Bernoulli(p) variables on oriented birth-label pairs i<j, together with independent fair bits, and takes their transitive closure. This is an auxiliary mathematical coupling, not a new physical input, observable, implemented generator or uniquely derived DET law.

Standard countable product probability, finite conditioning, linearity of expectation, geometric sums, Markov's inequality and the summable-event implication are mathematical tools, not additional physical assumptions.

#### Manual obligations discharged

1. Forward-edge transitive closure preserves old induced orders and makes each new vertex maximal. Its strict past is the downward closure of its selected incoming neighbors.
2. New incoming edges are independent of every old edge/bit and therefore of the old canonical marked history. Closure equals S iff all Max(S) are selected and every outside vertex is unselected; interior choices are free.
3. This proves the exact admitted q_p conditional row at every finite prefix, complete normalization, strict support, empty/full ideals and the empty parent. The next bit stays independently fair and the complete scalar branch coefficient is q_p/2.
4. Induction identifies every finite canonical marked-history probability. The countable coupled process therefore induces the same infinite law, allowing transfer of measurable almost-sure conclusions.
5. For gap g, the direct edge and each two-edge path through a distinct intermediate vertex depend on disjoint edge variables. Their absence probability is(1-p)(1-p^2)^(g-1). Incomparability is contained in this absence event; longer paths need not be excluded independently.
6. Summing over N-g pairs at each gap gives E I_N≤(1-p)sum_g(N-g)(1-p^2)^(g-1)≤(1-p)(N-1)/p^2. No independence of incomparable-pair indicators is used.
7. Dividing by binom(N,2) gives E(1-R_N)≤min(1,2(1-p)/(Np^2)). Markov gives the corresponding epsilon-tail bound. Exact N=2 and N=3 checks agree with the unrelaxed gap sum.
8. On N=m^2 the tail bound is summable. The first Borel–Cantelli implication, then countably many epsilon=1/k, gives almost-sure convergence on squares without independence.
9. I_N is nondecreasing because old incomparabilities persist. Interpolation using I_N≤I_(m+1)^2 and binomial denominators fills every index between successive squares. The normalized density is not assumed monotone.
10. The largest antichain contributes binom(W_N,2) incomparable pairs. Hence W_N/N→0 almost surely, consistently with accepted W_N→infinity.
11. Common limiting density1 does not distinguish fixed p values, although the two-birth law does. The explicit triangular p_N=N^-3 comparison has vanishing probability of any edge and thus R_N→0 in probability. It is not an admitted variable-p-in-time process.

#### Limits and evidence

No optimal rate, estimator/efficiency, arbitrary-law classification, continuum geometry, physical readout/time/dimension, metric, gravity or quantum result is inferred. In particular no1D/4D physical interpretation follows from the common order-density limit. The already recorded conventional antecedent remains; no new bibliography or novelty claim is made.

The original proof record retains twelve complete source/control captures with exact native pins and capture-byte comparisons. Its assigned output directory was initially absent and was created explicitly; that observation and resolution are retained. No source-read failure occurred. The distinct review's recovered combined display overflow and metadata truncation remain recorded. Author-reported final verification at 14:01:47 UTC and supported chat completion at 14:02:19 UTC on 26 October 2026 remain distinct; the review's reported final completion was 14:11:59 UTC after its recorded full freeze readback and integrity check. These were within their respective hard deadlines. Original external final native sessions were not independently reopened. Historical display/parser/timing/custody limits and the Part P author's recorded 65-second NONCOMPLIANCE remain unwaived. Hashes/readbacks establish artifact identity, not mathematical correctness or repaired historical custody.

Subsequent results require their own distinct review, coordinator disposition and scoped publication. All protected-validation/custody, independent-review, ABSTAIN, StatusM, zeroqualification, RET-only pause, Boundary and execution gates remain.

---

## X. A fixed admitted law with vanishing order density

**Acceptance and scope.** This part records an independently reviewed and coordinator-accepted fixed positive subset-weight law under Part A's unrestricted marked contract. Part T supplies the contrasting fixed-parameter family, and Part W proves density one almost surely for each member of that family. The present law instead has comparable-pair density tending to zero in mean and probability. It is not the separately prescribed seed, and almost-sure density zero is not asserted. Thus the admitted conditions alone do not force the Part W asymptotic behavior.

Status: mathematics accepted following distinct independent review and coordinator disposition. Manual mathematics only.

**Result.** The fixed weights, unchanged throughout the law, define a strictly positive normalized all-ideal scalar-passive marked law. Its comparable-pair fraction R_N satisfies
\[
\mathbb E R_N\longrightarrow0,\qquad R_N\longrightarrow0
\quad\text{in probability}.
\]
Thus the unrestricted admission conditions do not force the almost-sure density-one behavior accepted for each fixed-p family member. Almost-sure density zero is not proved here.

### 1. Fixed law and exact transition formula

Fix once and for all
\[
t_0=1,\qquad t_k=2^{-2^k}\quad(k\ge1),\qquad
Z_n=\sum_{k=0}^n\binom nk t_k.
\tag{1}
\]
For an n-vertex parent choose each actual subset A with probability t_|A|/Z_n, take its downward closure as the new vertex's strict past, and attach an independently fair immutable bit.

For an actual ideal S, write s=|S| and m=|Max(S)|. The closure equals S exactly for subsets
\[
\operatorname{Max}(S)\subseteq A\subseteq S.
\]
There are binom(s-m,k-m) such subsets of cardinality k. Therefore
\[
G(s,m)=\sum_{k=m}^{s}\binom{s-m}{k-m}t_k,\qquad
q(P,r,S)=\frac{G(s,m)}{Z_n}.
\tag{2}
\]
This proves the proposed formula, rather than assuming its admission.

Every t_k is positive, Z_n is finite and at least1, and every ideal has at least its maximal-generator subset. Thus every q is strictly positive. Closure events partition all actual subsets, so the complete ideal row sums to one. Empty and full ideals are included. The empty-parent row is G(0,0)/Z_0=1, and the empty ideal at any parent has probability1/Z_n.

The formula ignores all marks, satisfying proper selected-mark locality and permitted full-slot dependence. Relabeling preserves n,s,m, proving equivariance. No ideal occurrences are merged into isomorphism classes in a row.

### 2. Complete marked diamonds and all-size law

Let C have n vertices and let S,T be any ideals of C, including empty, full-base and equal choices. In either incomparable-birth route the second old precursor excludes the other newborn. Its induced order, cardinality and maximal count are unchanged. Both structural products equal
\[
q(C,r,S)q(C+S,r+b,T)
=\frac{G(|S|,|Max(S)|)\,G(|T|,|Max(T)|)}
       {Z_nZ_{n+1}}
=q(C,r,T)q(C+T,r+c,S).
\tag{3}
\]
This holds for every inherited marking and both arbitrary newborn bits b,c. Full-base precursors remain eligible, including when they become proper in the intermediate parent.

With branch map B_(S,b)(X)=q(P,r,S)X/2, each complete two-step route multiplies the same transported arbitrary complex positive-semidefinite payload by(3)/4. This verifies unnormalized marked maps, not merely normalized probabilities. Summing every one-step ideal/bit branch gives X.

For an exact all-size construction, sample subsets A_j of[ j-1 ] independently across births with the prescribed cardinality-weight probabilities, and sample independent fair bits. The distributions depend only on j-1, not the previously formed order. Draw i→j iff i belongs to A_j and take transitive closure. Induction shows the new strict past is exactly the required downward closure. Conditional on every old canonical marked history, the next subset still has its specified distribution. Hence this construction realizes all rows(2), every marked finite-history law and its consistent infinite extension.

Edges entering the same vertex are generally dependent. Independence is asserted only between the sampled subsets at distinct births. These auxiliary subsets are proof devices, not new committed observations or a physical mechanism.

Manual row checks are:
- Z_0=1.
- Z_1=5/4, giving singleton empty/full row(4/5,1/5).
- Z_2=25/16, giving two-antichain row(16,4,4,1)/25 and two-chain row(16,4,5)/25.

All sums equal one and retain full slots. The singleton row differs from the model's separately prescribed seed(2/3,1/3). This example concerns the unrestricted admitted contract; no seed-match or preferred-law claim is made.

### 3. Explicit selected-cardinality bound

For n≥1 let K_n be the selected-subset cardinality, with
\[
w_{n,k}=\binom nk t_k,\quad
\Pr(K_n=k)=w_{n,k}/Z_n,\quad \mu_n=\mathbb E K_n.
\]
For 1≤k<n,
\[
\frac{w_{n,k+1}}{w_{n,k}}
=\frac{n-k}{k+1}\,2^{-2^k}.
\tag{4}
\]
The k=0 ratio is not replaced by this formula because t_0 is separately defined.

Define
\[
c_n=\max\{1,\lceil\log_2\log_2(2n)\rceil\},
\qquad B_n=c_n+2.
\tag{5}
\]
If k≥c_n, then 2^k≥log_2(2n), so(4) is at most1/2. When c_n≤n, it follows that w_(n,c_n+r)≤2^-r w_(n,c_n) whenever the index is allowed. Consequently
\[
\mu_n
\le c_n+\sum_{r\ge1}r\,\Pr(K_n=c_n+r)
\le c_n+\sum_{r\ge1}r2^{-r}
=B_n.
\tag{6}
\]
If c_n>n, the simpler bound mu_n≤n<c_n suffices. Thus(6) holds for every n≥1. B_n is nondecreasing and
\[
B_n\le3+\log_2\log_2(2n)=O(\log\log n).
\tag{7}
\]
These are analysis bounds; neither the threshold nor n changes the fixed t_k.

Conditional on K_n=k the subset is uniform among all k-subsets, since each has the same weight. Equivalently, exchangeability and sum of inclusion indicators=K_n give, for every old vertex,
\[
\Pr(i\in A_{n+1})=\mu_n/n.
\tag{8}
\]
This is a single-edge marginal, not within-birth edge independence.

### 4. Reachability among later vertices

Fix delta in(0,1), then consider deterministic N≥2. Set
\[
\beta_N=\frac{B_N}{\delta N}.
\]
For i≥ceil(delta N) and j>i, consider a forward path
\[
i=v_0<v_1<\cdots<v_\ell=j.
\]
It requires one inclusion in each distinct target-birth subset A_(v_r). Independence across those births, together with(8), gives the exact path probability
\[
\prod_{r=1}^{\ell}
\frac{\mu_{v_r-1}}{v_r-1}
\le\beta_N^\ell,
\tag{9}
\]
because v_r-1≥i≥delta N and mu_(v_r-1)≤B_N. No two required inclusions in this one path belong to the same birth.

There are binom(j-i-1,ell-1) such paths of length ell. Comparability is equivalent to at least one forward path; reverse paths cannot occur. A union bound, requiring no independence between different paths, yields
\[
\Pr(i\prec j)
\le\sum_{\ell=1}^{j-i}
\binom{j-i-1}{\ell-1}\beta_N^\ell
=\beta_N(1+\beta_N)^{j-i-1}
\le\rho_N(\delta):=\frac{B_N}{\delta N}e^{B_N/\delta}.
\tag{10}
\]
The bound is valid even when its right side exceeds one. For each fixed delta, (7) gives
\[
e^{B_N/\delta}
\le e^{3/\delta}
[\log_2(2N)]^{1/(\delta\ln2)}.
\]
A fixed power of log N times log log N divided by N tends to zero. Therefore rho_N(delta)→0 for every fixed delta>0.

### 5. Density zero in mean and probability

Let C_N count unordered comparable pairs and
\[
R_N=C_N/\binom N2,\qquad N\ge2.
\]
This is intrinsic to the unmarked order. Birth labels are used only to split the proof.

Pairs whose earlier vertex i<ceil(delta N) number at most (ceil(delta N)-1)N≤delta N^2; bound their comparability probabilities by one. Every remaining pair obeys(10). Hence
\[
0\le\mathbb E R_N
\le\min\left\{1,\frac{2\delta N}{N-1}+\rho_N(\delta)\right\}.
\tag{11}
\]
First let N tend to infinity with delta fixed. Then limsup E R_N≤2delta. Since this holds for every delta in(0,1), letting delta decrease to zero proves E R_N→0.

For every epsilon>0, Markov's inequality gives
\[
\Pr(R_N>\epsilon)
\le\min\left\{1,
\frac{2\delta N/(N-1)+\rho_N(\delta)}{\epsilon}\right\},
\tag{12}
\]
and E R_N→0 proves R_N→0 in probability. The order of limits is fixed delta, then N→infinity, then delta→0; no silently changing law or weight sequence is used.

### 6. Exact conclusion and limits

This is one fixed all-size law, not Part W's triangular comparison using different p_N for different N. Admission was proved before its independent-birth representation was used.

Part W gives R_N→1 almost surely for every fixed interior-p law. The present admitted example instead has E R_N→0 and R_N→0 in probability. If every admitted law had R_N→1 almost surely, bounded convergence applied to this law's0≤R_N≤1 would force E R_N→1, a contradiction. Thus density one depends on the selected law and is not forced by the unrestricted admission conditions.

This argument does not prove R_N→0 almost surely. It also supplies no optimized rate, full asymptotic shape, width classification for this new law, physical dimension/readout/time, metric, gravity, quantum reconstruction, computational advantage or novelty claim. The conventional attribution in Part T retains its stated scope; no additional identification is asserted.

The original authorizations and accepted-source dispositions retain their limits. The proof author's clipped authorization display was recovered in full, and the initially absent output directory was created; both observations remain recorded. Historical custody/failure limits and the Part P author's recorded 65-second NONCOMPLIANCE remain unwaived. Protected validation, independent review, ABSTAIN, Status M, zero qualification, RET-only pause, Boundary and execution/publication gates remain. This mathematics has received distinct independent review and coordinator acceptance; it grants no execution or successor authority.

### 7. Premises and manual obligations

Status: mathematics accepted following distinct independent review and coordinator disposition.

#### Sources and fixed law

Part A supplies the unrestricted scalar-passive marked order contract. The original proof's supplied Part T family report and premises joined their actual acceptance record by exact bytes and hashes through intermediate locators; no original-path identity was asserted. Its supplied Part W density report, premises and review joined their actual acceptance record by original locator, size and hash. That theorem concerns fixed interior-p laws only. The original author checked both authorization sources and both control pins without opening nested originals or URLs. These are attributed source checks, not a claim that this public edition reopened historical sessions.

This fixed law is accepted on its direct admission and density proofs, not by inheriting another family’s acceptance: t_0=1 and t_k=2^(-2^k) for k≥1, fixed once for the entire law. Each actual n-parent subset has probability t_|A|/Z_n, with Z_n=sum_k binom(n,k)t_k. Its downward closure is the strict past. Independently fair immutable bits and scalar payload actions are retained.

The separately prescribed model seed is not imposed. The law's singleton row(4/5,1/5) differs from that seed. No parameter is fitted or changed with N.

#### Admission obligations discharged before use

1. Closure equals an ideal S iff Max(S) is contained in A and A is contained in S. Counting actual subsets by cardinality gives G(s,m)=sum_(k=m)^s binom(s-m,k-m)t_k and q=G/Z_n.
2. All weights are positive and the normalizer is finite. Every ideal has a maximal-generator subset, and closure events partition all subsets. This gives strict support and complete normalization, including empty/full slots and the empty parent.
3. Ignoring marks satisfies proper selected-mark locality. Cardinalities and maximal counts are invariant under transported relabeling.
4. In every incomparable-birth diamond, each second old precursor retains its G numerator. Both routes give G(S)G(T)/(Z_n Z_(n+1)), including empty/full/equal choices, all inherited markings and both newborn bits.
5. The fair bits multiply both transported complete unnormalized maps by1/4. One-step maps sum to the identity on any admitted complex positive-semidefinite payload.
6. Independent subsets on deterministic carriers[j-1], with independent fair bits, realize these exact conditional rows at every canonical finite history. Transitive closure agrees with the sequential ideal construction, and consistent cylinders define one infinite law.
7. Empty, singleton, two-chain and two-antichain rows are checked manually. No enumeration code is used.

#### Sparse-density proof obligations

For K_n=|A_(n+1)|, w_(n,k)=binom(n,k)t_k and mu_n=E K_n:

- For k≥1, w_(n,k+1)/w_(n,k)=(n-k)/(k+1) times2^(-2^k). The k=0 ratio is treated separately, never silently reused.
- With c_n=max(1,ceil(log2 log2(2n))) and B_n=c_n+2, the upper tail above c_n has successive weight ratio at most1/2. Its first excess moment is at most sum_(r≥1)r2^-r=2. If c_n>n the trivial bound suffices. Hence mu_n≤B_n for all n≥1, with monotone B_n≤3+log2 log2(2n).
- Exchangeability, or uniformity conditional on cardinality, gives the exact marginal probability mu_n/n for selecting any particular old vertex.
- Within-birth inclusions are not assumed independent. A particular forward path requires one inclusion at each of distinct target births, so its probability factors across independent subsets.
- For fixed delta in(0,1), i≥ceil(delta N) and later j, all path-edge probabilities are at most beta_N=B_N/(delta N). Counting paths and using only a union bound gives reachability at most beta_N(1+beta_N)^(j-i-1)≤rho_N(delta)=B_N exp(B_N/delta)/(delta N).
- For fixed delta, the explicit logarithmic bound makes rho_N(delta) tend to zero: its numerator is at most a fixed power of log N times O(log log N).
- Pairs with an earlier label below ceil(delta N) number at most delta N^2. The rest satisfy the path bound. Thus E R_N≤min(1,2delta N/(N-1)+rho_N(delta)).
- Take N→infinity for fixed delta, then delta→0, obtaining E R_N→0. Markov yields R_N→0 in probability.

#### Scope and evidence

R_N is the intrinsic unordered comparable-pair fraction at deterministic N≥2. Auxiliary subset edges and birth labels are proof devices, not added committed observables or a physical clock. The chosen weights define one law; proof thresholds depend on n but do not alter the law.

Density zero in probability is not promoted to almost-sure density zero. The admitted example contradicts universal almost-sure density one because bounded convergence would otherwise force its expectation to tend to one. No optimal rate, shape/width classification, physical dimension, readout, metric, gravity, quantum result, runtime advantage or novelty is inferred.

The original proof author freshly captured and fully read all twelve allowed source/control bodies. A combined display clipped one authorization and omitted the other; both retained complete bodies were displayed before proof drafting. The recorded exact native pins and capture-byte checks passed. Initial output-directory absence and its explicit creation remain recorded. Historical display/parser/custody limits and the Part P author's recorded 65-second NONCOMPLIANCE remain unwaived.

Coordinator owns distinct review, disposition, publication and successors. All protected-validation/custody, independent-review, ABSTAIN, StatusM, zeroqualification, RET-only pause, Boundary and execution gates remain.
