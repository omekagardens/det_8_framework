# Whole-history mark symmetry and the failure of row averaging

RI1492 consolidates the independently reviewed QR-LD007 finite theorem and counterexample. Mixing the original fair marked-history law with its global mark-flipped transport produces a consistent candidate on this four-birth prefix. Averaging the completed transition rows at each step fails a required commutation identity. The distinction is explicit, including every proper-slot locality check.

Part A prints the original model and the structural prefix; Part B defines and checks the candidate mixture. Only parent sizes zero through three and at most four births are used. The [native theorem package](native_theorem_package_v1/THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model) supplies the admitted structural identities. The [mark-bias note](native_mark_law_geometry_v1.md) examines a different operation: changing newborn bias while keeping the structural rule fixed.

The valid whole-history mixture preserves unmarked event probabilities but changes marked ones. It supplies neither a unique native-law selection principle nor a calibrated physical observation channel. Its mixture components are a mathematical representation, not proposed physical agents or hidden sectors. No performance or execution claim follows.

## A. Original model and the fixed four-birth structural prefix

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

Every full slot is the complete complement.

## B. Whole-history symmetrization and the row-average counterexample

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
