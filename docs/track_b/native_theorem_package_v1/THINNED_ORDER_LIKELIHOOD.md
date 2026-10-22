# Exact finite likelihood after faithful uniform vertex thinning

Historical author status: manual theorem candidate; independent review and coordinator adjudication pending.
Subsequent independent manual review and coordinator adjudication accepted the exact conditional finite scope below. The historical status is retained as an author-stage record.
Public edition: 22 October 2026.
Scope: a declared finite observation channel for the accepted from-empty
Bernoulli native order law. No physical acquisition map is supplied.

Public dependencies: [full-order likelihood](BERNOULLI_ORDER_LIKELIHOOD.md), [auxiliary-seed nonidentifiability](AUXILIARY_SEED_IDENTIFIABILITY.md), and [vertex-erasure height diagnostic](VERTEX_ERASURE_HEIGHT_DIAGNOSTIC.md). These links identify existing public expositions, not replayable private custody.


## 1. Observation contract and answer

Fix a known deterministic integer \(N\ge2\), a deterministic integer
\(0\le m\le N\), and one \(p\in(0,1)\) for the entire from-empty history.
Generate the completed birth-labeled order \(P_N\) under the accepted law:
independent \(E_{ij}\sim\operatorname{Bernoulli}(p)\), \(i<j\le N\), give
a forward DAG whose transitive closure is \(P_N\).
This is a representation of the accepted native law, not a uniquely
identified auxiliary mechanism or a derivation of this optional law from
general DET principles.

Choose \(T\) uniformly among the \(\binom Nm\) subsets of the actual birth
labels \([N]\), independently of the realized completed birth-labeled order.
Equivalently the conditional distribution of \(T\) given that order is
uniform. Report only
\[
                         [Q]=[P_N[T]], \quad N,\quad m.                 \tag{1}
\]
The restriction retains every true completed comparison among survivors.
In particular a comparison remains when its generating path passed through
an erased vertex. This is not deletion from a generating DAG followed by
recomputed reachability. Birth labels, erased identities, marks and payload
are not observed. The original marks and scalar-passive complex PSD payload
are not removed from the underlying model; they are marginalized here.
There is no stopping, order-dependent selection, conditional acceptance of
reports, missing comparison, or unknown true size.

The full-order likelihood survives as an exact finite **pushforward**, not
as its original formula with \(N\) replaced by \(m\). Already at \(N=3,m=2\),
\[
\Pr_p(Q\text{ is a chain})=p+\frac{p^2(1-p)}3\ne p.                     \tag{2}
\]
Nevertheless this two-outcome family remains identifiable in \(p\).
The derivation and its exact scope follow.

## 2. Counts and exact pushforward theorem

Let \(\mathcal P_k\) be the finite set of isomorphism classes of \(k\)-vertex
orders. On a representative \(P\) of a class in \(\mathcal P_N\), put
\[
c(P)=\#\{\text{covers}\},\qquad i(P)=\#\{\text{unordered incomparable pairs}\},
\quad a(P)=|\operatorname{Aut}(P)|,\quad A(P)=e(P)/a(P),
\]
where \(e(P)\) counts increasing bijections from its representative vertex
set to \([N]\). The accepted exact full-order theorem supplies
\[
                    \Pr_p([P_N]=[P])=A(P)p^{c(P)}(1-p)^{i(P)}.         \tag{3}
\]
Here \(A(P)\) counts distinct naturally birth-labeled copies, not arbitrary
labeled copies. No factor \(1/N!\) is present.

For a representative \(Q\) of an \(m\)-vertex class define the survivor count
\[
s_m(P,Q)=\#\{S\subseteq V(P): |S|=m,\ [P[S]]=[Q]\}.                    \tag{4}
\]
Every actual subset is counted once, including distinct subsets in the same
automorphism orbit. The count is unchanged by an isomorphism of \(P\) or
\(Q\). The exact likelihood of the reported order is
\[
\boxed{
L_{N,m}(p;[Q])=
 \frac1{\binom Nm}\sum_{[P]\in\mathcal P_N}
 \frac{e(P)}{a(P)}\,s_m(P,Q)\,p^{c(P)}(1-p)^{i(P)} .
}                                                                        \tag{5}
\]

Proof. Conditional on any particular naturally labeled realization \(R\)
of the full order, uniform independent thinning makes the conditional
probability of \([Q]\) equal to \(s_m(R,Q)/\binom Nm\).
This count is the same for all labeled copies in a fixed full-order class.
Consequently it also holds conditional on that full-order class. The law
of total probability and (3) give (5).

Equivalently, sum first over all distinct naturally labeled \(R\) on
\([N]\), each with weight \(p^{c(R)}(1-p)^{i(R)}\), and then over its
\(\binom Nm\) equally weighted survivor subsets. Grouping these \(R\)'s by
isomorphism contributes precisely \(e(P)/a(P)\). The survivor count is
a second, different multiplicity. This derives rather than assumes their
product in (5).

For each \(P\), survivor subsets partition by the class of their completed
restriction, so
\[
                   \sum_{[Q]\in\mathcal P_m}s_m(P,Q)=\binom Nm.
\]
Summing (5) over all output classes therefore gives one by normalization
of the accepted full-order law. At \(m=N\), \(s_N(P,Q)\) is the indicator
of \([P]=[Q]\), and (5) is exactly (3). For \(m=0\) or \(m=1\) the only
output order has probability one. These are channel endpoint checks, not
a general identifiability theorem for intermediate sizes.

### Three different counting operations

1. \(e(P)/a(P)\) counts distinct compatible birth-labeled full orders.
   Neither \(e(P)\) alone nor \(N!/a(P)\) replaces it.
2. \(s_m(P,Q)\) counts survivor subsets, not automorphism orbits of subsets
   and not labelings of \(Q\). Each such subset has channel weight
   \(1/\binom Nm\), even when another subset is isomorphic to it.
3. If counting induced embeddings instead, let \(\operatorname{Emb}_{\rm ind}(Q,P)\)
   be the injections preserving and reflecting the strict order.
   Each valid image subset supports exactly \(a(Q)\) such isomorphisms.
   Thus
   \[
               s_m(P,Q)=|\operatorname{Emb}_{\rm ind}(Q,P)|/a(Q).       \tag{6}
   \]
   There is no further division by \(a(P)\) for subset sampling and no
   extra \(e(Q)/a(Q)\) factor multiplying (5).

Equation (6) is only an alternative expression for (4), not an additional
observation operation. For example all \(m\)-subsets of an \(N\)-antichain
are in a single automorphism orbit but their count is \(\binom Nm\).
Replacing this count by one would incorrectly reduce its conditional
output probability below one when \(0<m<N\).

## 3. One fully manual example: \(N=3,\ m=2\)

Write \(q=1-p\). There are five three-vertex order classes:
the antichain, a single comparable pair plus an isolate, a fork, a join,
and the chain. This list follows by counting comparable pairs: zero,
one, two (only the fork or join without forced third comparison), or
three. A two-step ordered path forces the third comparison and belongs
to the chain.

The following are manual finite counts, with no enumeration program or
numerical probability evaluation.

| Full order \(P\) | \(e(P)\) | \(a(P)\) | \(c(P)\) | \(i(P)\) | Full mass | \(s_2(P,C_2)\) | \(s_2(P,A_2)\) |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Antichain \(A_3\) | 6 | 6 | 0 | 3 | \(q^3\) | 0 | 3 |
| One comparison plus isolate | 3 | 1 | 1 | 2 | \(3pq^2\) | 1 | 2 |
| Fork (one minimum, two maxima) | 2 | 2 | 2 | 1 | \(p^2q\) | 2 | 1 |
| Join (two minima, one maximum) | 2 | 2 | 2 | 1 | \(p^2q\) | 2 | 1 |
| Chain \(C_3\) | 1 | 1 | 2 | 0 | \(p^2\) | 3 | 0 |

For a single pair plus isolate there are three placements of the isolate
in a linear extension and no nontrivial automorphism. For a fork or join
the two interchangeable incomparable vertices account for both the two
linear extensions and the two automorphisms. Every two-subset is either
a comparable pair or an incomparable pair; thus the last columns count
exactly those pairs. Their row sums are three, not one.

The full masses normalize:
\[
q^3+3pq^2+2p^2q+p^2
=q^3+3pq^2+3p^2q+p^3=(p+q)^3=1.
\]
Applying (5), with \(\binom32=3\), gives
\[
\begin{aligned}
L_{3,2}(p;C_2)
 &=\frac{3pq^2+4p^2q+3p^2}{3}\\
 &=pq^2+\frac43p^2q+p^2
  =p+\frac13p^2q,\\
L_{3,2}(p;A_2)
 &=\frac{3q^3+6pq^2+2p^2q}{3}\\
 &=q^3+2pq^2+\frac23p^2q
  =q\left(1-\frac{p^2}{3}\right).
\end{aligned}                                                           \tag{7}
\]
Both are positive for \(0<p<1\), and their sum is one.

A direct check of the same example uses the three possible survivor
subsets of birth labels. For \(\{1,2\}\) and \(\{2,3\}\) the comparison
probability is \(p\). For \(\{1,3\}\), the comparison occurs if \(E_{13}=1\),
or if \(E_{13}=0\) and \(E_{12}=E_{23}=1\). These are disjoint cases, of
total probability \(p+qp^2\). Averaging the three equal channel weights
again gives \(p+p^2q/3\). The event with absent direct edge and present
two-step path is precisely the additional contribution retained after
deleting vertex 2. No overlapping path witnesses have been added.

### Failure of naive size substitution

A fresh from-empty two-vertex draw has chain probability \(p\) and
antichain probability \(q\). Equation (7) differs by \(p^2q/3>0\) on the
chain for every admitted \(p\). Thus the unchanged raw likelihood at
\(N=m=2\) is not the likelihood of this thinned observation.

The two-outcome distribution can of course be written as a fresh two-
vertex distribution at a different effective parameter
\(p_{\rm eff}=p+p^2(1-p)/3\). This is not validity of substituting only the
size while retaining the original \(p\), nor is it a claim about any
larger-size thinning consistency or parameter transformation.

### Small-case distribution identifiability

Define \(f(p)=p+p^2(1-p)/3\). Manual differentiation gives
\[
 f'(p)=1+\frac{2p-3p^2}{3}
      =\frac23+\frac{(1-p)(1+3p)}3>0,\qquad 0<p<1.                       \tag{8}
\]
Hence \(f\) is strictly increasing. Equal distributions of the two
possible reports force equal chain probabilities, then equal \(p\)'s.
This proves distribution identifiability in this \(N=3,m=2\) family only.

It does not permit recovering an unknown real \(p\) exactly from one
realized pair: both outcomes have positive probability at every admitted
parameter. No estimator, confidence interval, consistency, posterior,
repeated-sampling design or arbitrary-\(m\) identifiability result is
asserted. The full-order sufficient-statistic and optimizer statements
are not automatically transferred through (5).

## 4. Dependencies, nonidentification and limits

The permitted BERNOULLI_ORDER_LIKELIHOOD.md supplies (3) and the exact
meaning of natural-label counting. Its original no-erasure hypothesis is
not ignored: it is applied only to the latent full order before the
explicit observation-channel sum.

VERTEX_ERASURE_HEIGHT_DIAGNOSTIC.md already distinguishes completed-order
restriction from deleting generating edges and proves height-error
transfer under a different bounded-erasure contract. That existing result
is a dependency/context boundary, not a new result here. Neither its
error bounds nor its size/budget conditions are needed to prove (5).
The present uniform fixed-size channel does not extend its calibration,
adversarial-erasure or unknown-size claims.

AUXILIARY_SEED_IDENTIFIABILITY.md, whose exact subject is accepted by the
supplied adjudication, proves equality of the original and maximal-seed
representations' full native history laws and coarse payload maps.
Applying the same declared order-dependent observation kernel to equal
native distributions gives equal observed distributions. Alternatively,
use its pathwise order coupling and the same independent uniform \(T\).
Thus the auxiliary seed nonidentifiability persists after thinning.
The current \(p\)-identifiability in the small case does not identify
independent hidden seeds. No new native generative law is produced.

The channel is a stipulated mathematical observation mechanism, not an
implemented or physically justified readout. Obtaining known true \(N\),
uniform independent survivor selection and every true retained comparison
remains an unsupplied acquisition obligation. The sum in (5) is finite but
no efficient general computation or reduced counting algorithm is claimed.
There is no general/adversarial erasure calibration, new physical premise,
QM derivation, geometry/mass/gravity result, RET work or application gain.

### Editorial clarification outside the accepted scientific text

In section 4, “order-dependent observation kernel” means that restriction of a supplied input order depends on that order. It does not permit order-dependent subset selection: the survivor subset remains uniform and independent of the completed birth-labeled order, exactly as section 1 requires. Scientific sections 1–4 are reproduced literally; the original 4-to-6 numbering gap is cosmetic and retained.



## 6. Evidence and halt

The source author read two authorized coordinator JSON records and three literal supplied manuscript copies, without following embedded references. The author records full consumption of all five current captures, three matching manuscript byte/hash pairs, and an exact join from the auxiliary source to its accepted subject. The JSON identities were observed rather than supplied as expected pins by that same manifest. An explicit source-adjudication timestamp was retained rather than inferred. Historical source custody and review qualifications remain source reports. Current byte joins neither reconstruct that history nor prove mathematics.

The proof and finite counts are manual. Author preparation used only inert text, JSON, readback, hash, size and inventory operations, with no descendants, scientific or numerical runner, source import, fixture, data/hardware/network access, protected validation, RET work, repository mutation or publication. The original closing statement that independent review and adjudication had not yet occurred was true at author freeze; subsequent separate manual review and coordinator adjudication accepted the exact conditional scope.

The independent reviewer disclosed predecessor exposure and did not claim a blinded review. The reviewer freshly consumed the permitted current manuscript bodies in bounded portions. An aggregate display was truncated and the complete manuscript/ledger and needed metadata schemas were recovered; oversized embedded receipt arrays were parsed and selectively joined rather than claimed as fully reread prose. Thirty-seven administrative checks joined the declared current subject, freeze members, source pins, acceptance and captured records. Source-author consumption, supplied acceptance premises, metadata-only readbacks, worker-reported controls and historical custody retain those narrower statuses.

The author and reviewer each recorded temporary control-identity ambiguity and stopped dependent work. Fresh supported observations reconciled the expected current identity before resumption; this was not a reset, a threshold-stop exception or a capacity waiver. Raw machine/control identifiers and receipts remain private. The bounded author preparation and independent review ended at their respective freezes; no execution or successor was authorized by those freezes.

This public edition preserves all scientific sections literally and adds only the separately marked selection clarification, public dependency links and metadata-obscured provenance. Exact private originals, correspondence, review/adjudication pins, command receipts, administrative scripts and machine/filesystem identifiers are withheld locally. Public payload hashes identify the published derivatives only. This is not an independently replayable custody archive, a new proof, an efficient implementation or physical observation admission. Subsequent assigned questions remain pending and excluded.
