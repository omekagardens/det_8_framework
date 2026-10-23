# Finite law dependence after two-survivor thinning

Historical author status: manual finite counterexample candidate; independent review and root adjudication pending.
Subsequent independent manual review and coordinator adjudication accepted the exact finite witness below. Publication preparation and editorial acceptance are separate gates.
Public edition: 22 October 2026.
Execution remains HOLD. This is a finite three-vertex law-dependence witness, not an admitted all-size growth family, physical acquisition model or execution permission.

## Public question and source crosswalk

Can a positive correlated three-vertex edge law retain the independent model's Bernoulli edge marginals and complete two-survivor report distribution while changing the full intrinsic order law? The scientific sections below answer this finite question. Horizon-three natural-label covariance does not establish all-size native admission.

The source's historical label RI1377 denotes [the finite thinning likelihood](THINNED_ORDER_LIKELIHOOD.md), including the declared channel and three-vertex probabilities. RI1380 denotes [parameter identifiability within the admitted family](PARAMETER_IDENTIFIABILITY.md), which remains valid. The full-order law and intrinsic likelihood are in [the Bernoulli-order theorem](BERNOULLI_ORDER_LIKELIHOOD.md); the accepted alternate-seed comparison is [auxiliary-seed identifiability](AUXILIARY_SEED_IDENTIFIABILITY.md). Faithful completed restriction is also used in [the vertex-erasure diagnostic](VERTEX_ERASURE_HEIGHT_DIAGNOSTIC.md). The [package index](THEOREM_PACKAGE.md) and [law-dependence note](LAW_DEPENDENCE.md) retain the native model's wider admission boundaries.

Scientific sections 1–7 are reproduced literally. Their historical labels have the public meanings above and require no private chronology or filesystem evidence.

## 1. Question and result

Keep known true \(N=3\), deterministic \(m=2\), and the accepted channel:
select one of the three actual survivor pairs uniformly and independently
of the completed birth-labeled order, restrict that completed order
faithfully, then forget birth labels. The report has only two possible
intrinsic order classes, a chain \(C_2\) or antichain \(A_2\).
Comparisons mediated by an erased vertex remain in the completed restriction.

The answer is yes. The finite correlated family below has:

- Exactly Bernoulli(\(p\)) marginal distribution for each forward edge.
- Positive probability for each of the eight elementary edge configurations.
- Genuine positive correlation between every pair of distinct edge variables.
- Exactly the same reported two-survivor distribution as the independent-edge
  construction at the same \(p\), even before averaging over which pair survives.
- A different intrinsic full three-vertex completed-order distribution.

Thus identifying a parameter within the admitted family does not validate
that family from this observation. The counterexample changes the native
completed-order law; it is not the already accepted alternate-seed
representation of one unchanged native law.

## 2. Explicit open parameter domain and all elementary probabilities

Let
\[
 X=E_{12},\qquad Y=E_{13},\qquad Z=E_{23},\qquad q=1-p.
\]
These are forward-edge indicators on birth labels \(1,2,3\).
Fix parameters in the open nonempty domain
\[
                \boxed{0<p<1,\qquad 0<\delta<pq^2.}                  \tag{1}
\]
Equivalently one may put \(\delta=\varepsilon pq^2\), with independently
chosen \(p,\varepsilon\in(0,1)\). No numerical parameter choice is required.

Define the joint mass \(\nu_{p,\delta}\) on \((X,Y,Z)\) by this complete table:

| \(XYZ\) | Independent mass \(\nu_{p,0}\) | Correlated mass \(\nu_{p,\delta}\) |
| --- | --- | --- |
| 000 | \(q^3\) | \(q^3+2\delta\) |
| 100 | \(pq^2\) | \(pq^2-\delta\) |
| 010 | \(pq^2\) | \(pq^2-\delta\) |
| 001 | \(pq^2\) | \(pq^2-\delta\) |
| 110 | \(p^2q\) | \(p^2q\) |
| 101 | \(p^2q\) | \(p^2q\) |
| 011 | \(p^2q\) | \(p^2q\) |
| 111 | \(p^3\) | \(p^3+\delta\) |

All eight masses are strictly positive on (1). The single-edge atoms
are positive by its upper bound; the others are sums or products of
strictly positive quantities. Their sum is
\[
q^3+3pq^2+3p^2q+p^3+(2-3+1)\delta=(p+q)^3=1.                          \tag{2}
\]
This verifies nonnegativity, normalization and full elementary support,
not merely selected moments. In particular no atom can exceed one.

The reference \(\delta=0\) is the admitted independent construction;
it is a boundary reference for the positive-\(\delta\) domain, not
claimed to belong to that domain. Each choice in (1) is a fully specified
finite correlated probability law.

## 3. All one-edge marginals and genuine correlations

For any coordinate, symmetry of the table gives
\[
\Pr_{\nu}(X=1)
=(pq^2-\delta)+2p^2q+(p^3+\delta)
=p(q+p)^2=p.                                                         \tag{3}
\]
The same calculation holds for \(Y\) and \(Z\), so all three are
Bernoulli(\(p\)); their zero probabilities are \(q\).
No assumption of independence was used in this marginal calculation.

For each pair of distinct coordinates, for example \(X,Y\), the only
atoms with both equal to one are 110 and 111. Hence
\[
\Pr_\nu(X=Y=1)=p^2q+p^3+\delta=p^2+\delta,\qquad
\operatorname{Cov}_\nu(X,Y)=\delta>0.                                 \tag{4}
\]
The same equation holds for \(X,Z\) and \(Y,Z\). These joint probabilities
differ from the product \(p^2\), proving genuine dependence, not merely
a renamed independent array. The probability table itself guarantees
that these moments obey the required probability inequalities.

Although the table is symmetric in the three edge coordinates, that
alone is not an all-size native covariance or growth-admissibility proof.
The precise finite completed-order status is checked in section 6.

## 4. Identical retained pair marginals and complete two-survivor law

Let \(P\) be the transitive closure of the realized forward-edge DAG.
Its comparisons are exactly
\[
 1\prec_P2\ \Longleftrightarrow\ X=1,\qquad
 2\prec_P3\ \Longleftrightarrow\ Z=1,\qquad
 1\prec_P3\ \Longleftrightarrow\ Y=1\ \text{or}\ (X=Z=1).
\]
For the last comparison use disjoint events:
\[
 \Pr_\nu(1\prec_P3)
 =\Pr_\nu(Y=1)+\Pr_\nu(Y=0,X=Z=1)
 =p+\nu(101)=p+p^2q.                                                 \tag{5}
\]
The 101 atom was intentionally left unchanged. Adding joint path
probabilities without the \(Y=0\) condition would double-count 111.

The conditional report probabilities for each fixed survivor pair are
therefore:

| Survivor set | Chain probability | Antichain probability |
| --- | --- | --- |
| \(\{1,2\}\) | \(p\) | \(q\) |
| \(\{2,3\}\) | \(p\) | \(q\) |
| \(\{1,3\}\) | \(p+p^2q\) | \(q(1-p^2)\) |

They agree entry by entry with the independent construction. Selection is
independent of the completed order, so conditioning on the selected pair
does not reweight these probabilities. Uniformly averaging the three rows,
\[
\boxed{
 \Pr_\nu(Q=C_2)=p+\frac{p^2q}{3},\qquad
 \Pr_\nu(Q=A_2)=q\left(1-\frac{p^2}{3}\right).
}                                                                     \tag{6}
\]
Both are positive, sum to one, and contain no \(\delta\). These are exactly
the accepted RI1377 probabilities at the same known \(N=3,m=2,p\).
Because these are the only two output classes, equality of (6) proves
equality of the entire declared observed distribution, not just its mean.

Birth-label-conditioned rows are proof calculations, not added observer
inputs. The actual report still forgets labels. No assertion about multiple
overlapping pair reports from one shared three-vertex realization is made:
such an enlarged observation could reveal joint information absent here.

## 5. The intrinsic full three-vertex law actually changes

The closure map from elementary configurations gives these five classes:

| Full intrinsic order | Elementary configurations | Independent mass | Correlated mass |
| --- | --- | --- | --- |
| Antichain \(A_3\) | 000 | \(q^3\) | \(q^3+2\delta\) |
| One comparison plus isolate | 100,010,001 | \(3pq^2\) | \(3pq^2-3\delta\) |
| Fork (one minimum) | 110 | \(p^2q\) | \(p^2q\) |
| Join (one maximum) | 011 | \(p^2q\) | \(p^2q\) |
| Chain \(C_3\) | 101,111 | \(p^2\) | \(p^2+\delta\) |

These events partition all eight atoms. In the chain row, 101 already
generates the endpoint comparison transitively; 111 adds a redundant edge.
Thus its mass is \(p^2q+p^3+\delta=p^2+\delta\).
All five class masses are positive and sum to one by (2).
At least the antichain, single-comparison and chain masses differ from
the independent law for every allowed \(\delta\).

A direct survivor-count check agrees with (6). A one-comparison order
has one comparable survivor pair, a fork/join two, and a chain three.
Consequently
\[
\begin{aligned}
 \Pr_\nu(Q=C_2)
 &=\frac{(3pq^2-3\delta)+4p^2q+3(p^2+\delta)}3\\
 &=pq^2+\frac43p^2q+p^2
  =p+\frac13p^2q.
\end{aligned}
\]
The lost single-comparison contribution and gained chain contribution
cancel. This is a manual cross-check of the same witness, not a new
height-erasure result or calibration.

The changed full intrinsic distribution makes this a genuine finite
completed-order law change. It does not claim zero-error discrimination
from one full report: all five classes have positive mass under both laws.

## 6. Finite covariance and admission boundary

The construction is a finite \(N=3\) candidate family on forward-edge
arrays, and its completed-order law is naturally label-covariant at this
horizon in the following explicit, limited sense: two naturally
birth-labeled completed orders on \([3]\) that are isomorphic receive
equal probability.

To check this, the antichain and chain each have one natural labeled
representative. The fork and join likewise each have one. The
one-comparison-plus-isolate class has three natural labeled representatives,
with comparisons 12, 13 or 23; each is the closure of its corresponding
single-edge atom, of the common mass \(pq^2-\delta\).
These exhaust the possibilities and prove the stated finite covariance.
Equivalently the natural-label counts are \(1,3,1,1,1\), with the
three-copy class sharing its mass equally.

This finite statement is not invariance under arbitrary permutations
that turn forward birth labels into backward edges. It is also not a
proof of all-size natural-label covariance or an admitted sequential
growth family. No law beyond the three-vertex experiment, projective
extension, every-parent transition prescription, full marked diamond
identities, complete native instrument conditions, or proper-precursor
restriction has been supplied or verified. Existing native eligibility,
mark/payload and positivity requirements have not been weakened.

An initial empty/singleton prefix and a Bernoulli edge at size two are
consistent with the table's \(X\) marginal; finite conditional
factorization exists because all atoms are positive. This observation
does not discharge those missing all-size admission obligations.
The comparison remains a finite candidate with explicitly verified
horizon-three natural-label covariance, not an admitted growth alternative.

## 7. What the witness closes, and what it leaves unchanged

Four notions must be kept separate:

1. A coordinate change transports the same observable probability law
   along a relabeling; it cannot create the changed intrinsic masses above.
2. Hidden representation equality, as in the accepted auxiliary-seed
   theorem, preserves the complete native law at each \(p\).
3. The present finite candidate changes that complete three-vertex order
   law, despite keeping every individual edge marginal Bernoulli(\(p\)).
4. Observational alias is equality only after the specified two-survivor
   observation channel. Equation (6) proves that alias here.

RI1380 remains correct: within its stipulated independent-edge native
family, \(p\) is distribution-identifiable for each known \(N\) and
\(2\le m\le N\). At \(N=3,m=2\), this candidate family even retains the
same strictly increasing function \(p+p^2(1-p)/3\), while \(\delta\)
is invisible. Thus within-family parameter identification does not
establish family validity or independent elementary edge structure from
that impoverished observation.

The stronger assertion that two different fully admitted all-size growth
families alias is not proved. If native-law admission is required of a
competing model, that remains an explicit unclosed requirement. The
finite witness answers the present question without concealing this gap.

Known true size, uniform independent subset selection and faithful
completed comparisons remain load-bearing. This is not an unknown-size,
biased-selection or noisy-comparison extension. The existing
auxiliary-seed nonidentifiability and physical acquisition gap are
unchanged. No physical preparation/readout, quantum derivation, geometry,
mass/gravity, clock, RET, application gain, estimator or calibration follows.

## Publication and verification note

The author constructed this finite probability witness manually. Independent manual review and coordinator adjudication subsequently accepted its declared three-vertex scope. The historical candidate status above records the author stage; it is distinct from the later adjudication. This public edition preserves scientific sections 1–7 literally, including the complete atom table, survivor-pair table, intrinsic-order table and finite covariance/admission limitations. Private administrative section 8 is withheld.

Public correspondence checks compare exact scientific text, mathematical spans, tables, relative dependencies and present byte identities. They are not machine proof, empirical confirmation or reconstruction of historical custody. Reused scientific-body consumption, partial metadata exposure, worker-reported controls, historical display failures and recoveries remain distinguished in private evidence. Private paths, command receipts, fingerprints and raw source-capture maps are withheld.

The witness changes the full three-vertex law while preserving the single faithful uniform two-survivor distribution. It does not supply an admitted all-size alternative, a joint multi-pair report, exact discrimination from one order, estimator calibration or physical readout. Within-family parameter identifiability remains unchanged. The assigned latent-mixture extension and native-admission continuation is pending independent admission and excluded.
