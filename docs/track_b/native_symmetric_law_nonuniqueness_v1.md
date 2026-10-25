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
