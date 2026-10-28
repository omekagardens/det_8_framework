# One further positive scalar growth layer

For every finite integer \(n\ge1\) and field \(K\in\{\mathbb R,\mathbb Q\}\) (real or rational scalars), every prefix in the family below admits one further strictly positive scalar layer in the same field. The construction preserves all prefix rows. This conditional lemma has an independent blind proof and coordinator acceptance.

## Declared family

A parent \((A,r)\) is any finite strict partial order with immutable binary marks \(r:A\to\{0,1\}\). A birth adjoins a maximal vertex whose entire strict past is an actual ideal \(S\) of \(A\). The prefix supplies \(q(A,r,S)\in K\) for every marked parent of size at most \(n-1\) and every actual ideal, including empty and full. Require:

- Every slot is strictly positive; the complete actual-ideal row sums to one, including its full-slot complement. The empty-parent slot is one.
- Scalars depend only on the marked parent and actual ideal, not its natural-history encoding, payload or next newborn bit. Newborn bits are independent and fair, so each marked branch has weight \(q/2\).
- Every marked order isomorphism transports scalars equivariantly, including automorphisms.
- All incomparable-birth scalar diamonds hold on bases of sizes \(0,\ldots,n-2\). For every such \((C,r)\), ideals \(S,T\), and newborn bits \(b,c\),
\[
q(C,r,S)q(C+x_S,r+b,T)
=q(C,r,T)q(C+y_T,r+c,S).
\]
Here \(r+b\) extends the inherited marking by the bit at \(x\); actual old identities are matched. The common fair-bit factor is \(1/4\). This condition is vacuous when \(n=1\).

All finite order types, markings and ideal occurrences are included. No additional locality or coupling axiom is assumed. Write this family as \(\mathcal F_n(K)\).

## Construction and lemma

For a marked order with \(k\le n\) vertices, choose a natural birth order and set
\[
W_k(A,r)=\prod_{j=1}^{k}q(A_{j-1},r_{j-1},S_j),
\qquad W_0(\varnothing)=1,
\]
where \(S_j\) is the newborn's full strict past. This is an individual structural history product. Its marked-history probability is \(2^{-k}W_k\); it is neither an endpoint mass nor a product containing automorphism or history-count factors.

Let \(\mathcal P_n\) contain every strict partial order on fixed labels \(\{1,\ldots,n\}\), with every binary marking. Define
\[
m_n=\min_{(A,r)\in\mathcal P_n}W_n(A,r),
\qquad B_n=2^n-1.
\]
Choose any rational \(\theta\) with \(0<\theta<1\), common to the new layer, and put \(\varepsilon=\theta m_n/B_n\). If \(N(A)\) counts the actual proper ideals of an \(n\)-vertex parent, define
\[
Q(A,r,S)=\frac{\varepsilon}{W_n(A,r)}\quad(S\subsetneq A),
\qquad
Q(A,r,A)=1-N(A)\frac{\varepsilon}{W_n(A,r)}.
\]
Each proper ideal occurrence retains its own slot; both newborn bits receive \(Q/2\).

**Lemma.** These formulas are well defined, and the unchanged prefix together with \(Q\) belongs to \(\mathcal F_{n+1}(K)\). In particular,
\[
\varepsilon\le Q(A,r,S)\le\theta/B_n\quad(S\subsetneq A),
\qquad Q(A,r,A)\ge1-\theta>0.
\]
Thus every new slot has lower bound \(\min\{\varepsilon,1-\theta\}\), depending on the prefix, horizon and choice of \(\theta\).

## Proof

Repeatedly removing a minimal vertex gives a natural order of every finite parent. Each newborn's strict past is an available ideal, so full support makes every such marked history positive.

Any two natural orders connect by adjacent swaps of incomparable vertices: move the next vertex of the desired order left across the remaining list. A crossed predecessor would contradict the desired order; a crossed successor would contradict the current order. For histories of length at most \(n\), each swap has base size at most \(n-2\). Its assumed marked diamond preserves the two scalar factors. The resulting marked parent is identical, so parent-only dependence preserves the subsequent suffix; equivariance transports names. Consequently \(W_k\) is independent of the natural order and marked-equivariant. Normalization and positivity give \(0<W_k\le1\). In particular, for \(|C|=n-1\),
\[
W_n(C+x_S,r+b)=W_{n-1}(C,r)q(C,r,S).
\]

The set \(\mathcal P_n\) is finite and nonempty, so its positive minimum is attained and lies in \(K\). Equivariance extends the bound to arbitrary vertex names. There are between one and \(B_n\) actual proper ideals. Hence the displayed bounds follow from \(m_n\le W_n\le1\); summing all proper slots and their full complement gives exactly one. The full slot is strictly positive. Transport preserves \(W_n\) and bijects proper ideals, preserving \(N\) and the complete row. The new scalars are independent of the next bit and history encoding.

For any new diamond on \(|C|=n-1\), the ideal \(T\) remains an ideal of \(C+x_S\) and excludes \(x\), hence is proper even when \(T=C\). Therefore
\[
q(C,r,S)Q(C+x_S,r+b,T)
=\frac{\varepsilon}{W_{n-1}(C,r)}
=q(C,r,T)Q(C+y_T,r+c,S).
\]
All divisions have positive denominators. This covers every marking, both newborn bits, and empty, full-in-base, equal, overlapping or disjoint precursors. A full new slot cannot be an incomparable second step, but remains present in normalized rows and suffixes.

Adjacent swaps through birth \(n+1\) use only old or new diamonds. After each pair, the same marked parent and parent-only dependence preserve every transported suffix, including full slots. With fresh names fixed by birth position, summing all actual ideals and both bits preserves total finite-history mass one at each depth. Different vertex names are coordinate encodings, not extra stochastic outcomes; distinct natural histories retain their multiplicities when summed.

For \(n=1\), \(W_0=W_1=m_1=B_1=1\): the singleton empty/full slots are \(\theta,1-\theta\) for either root mark. Both orders of the empty-base diamond have scalar product \(\theta\), completing this edge case.

Finite products, an attained minimum, rational \(\theta\), and nonzero division preserve rationality when \(K=\mathbb Q\). For \(K=\mathbb R\), the exact finite minimum is a mathematical definition, not an assumed effective comparison oracle. This completes the scalar lemma.

## Meaning and limits

The choice of \(\theta\) is optional extension data; labels and natural orders are coordinate conventions. No canonical, optimal or physically preferred choice is selected. The premises used above are sufficient; their use is not a necessity theorem for weakened families.

The result concerns one additional scalar layer over this declared family, not all DET laws. It supplies no infinite compatible object or measure, payload or quantum-channel extension, quantum reconstruction or limit, arbitrary-horizon modulo-five readout extension, output marginal, computational advantage or physical law selection. It includes no executed enumeration, algorithmic cost claim or operational permission.

Earlier interruption/recovery and premises-save qualifications remain historical qualifications; this accepted proof does not repair them. Scientific, independent-review, protected-validation, custody, calibration, resource, execution and publication gates remain in force.
