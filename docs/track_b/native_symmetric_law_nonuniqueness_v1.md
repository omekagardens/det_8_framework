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
