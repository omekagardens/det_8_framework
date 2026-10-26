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
