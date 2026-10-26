# Intrinsic consistency and law selection

QR-LD037 — independently reviewed and coordinator-accepted at the scope below. This is conditional mathematics, including a finite process that deliberately fails the admitted diamond condition. It is not a physical prediction or an alternative admitted DET law.

Dependencies: the [intrinsic restriction theorem](intrinsic_subset_restriction.md) supplies the stated positive subset-weight family and its kernel; [finite-prefix nonidentification](finite_prefix_nonidentification.md) retains the limit on extrapolating from finite records. The accepted body is reproduced below without mathematical edits. Its closing stop language records the author handoff; subsequent questions are tracked separately. Raw local source identities, review receipts and custody records remain private under the metadata-obscured publication policy.

**Result.** The accepted intrinsic restriction property holds for many distinct admitted all-size laws. Moreover, through four births, endpoint consistency under that kernel alone does not force equal canonical history weights or subset-weight form. The counterexample below is a positive, mark-independent, order-covariant finite process; it violates the DET diamond condition and is not an admitted DET extension.

## 1. What the accepted construction establishes

Let L(P) count linear extensions on distinct vertices. The fixed observation kernel K chooses a maximal actual vertex v with probability \(L(P\setminus v)/L(P)\), restricts the transitive marked order, then takes its marked isomorphism class. All actual deletion occurrences are counted before equal outputs are merged.

Accepted QR-LD036 proves, for its declared positive subset-weight scalar laws,
\[
\mu_NK_N=\mu_{N-1}
\tag{1}
\]
at every supported finite horizon. Its proof derives equal canonical history weights from the G/Z rows, handles natural encodings and marked automorphisms, and retains arbitrary common complex PSD payload coefficients.

Take the two accepted all-size instances
\[
q_p(P,S)=p^{|\operatorname{Max}(S)|}(1-p)^{|P|-|S|},
\qquad p=1/3,\quad p=2/3.
\]
Their subset weights are respectively \(t_k=(1/2)^k\) and \(t_k=2^k\). Both satisfy (1) at every finite N using the same K. Yet their direct two-birth chain probabilities are \(1/3\) and \(2/3\).

The complete marked two-vertex law has four distinct chains \(C_{00},C_{01},C_{10},C_{11}\), each of probability \(p/4\); antichains \(A_{00},A_{11}\), each \((1-p)/4\); and the mixed antichain, \((1-p)/2\). Thus the finite predictions, including scalar output coefficients, differ. They are indistinguishable only by whether they pass the consistency requirement, not by their output distributions. Every interior p supplies another accepted example; the property does not uniquely select a parameter or law.

## 2. One finite converse test: precise construction

Use the admitted half-selection kernel
\[
q_*(P,S)=2^{-(|P|-|S|+|\operatorname{Max}(S)|)}
\tag{2}
\]
through the first three births. To produce birth four, change only the following three-vertex parent rows. All old and newborn marks remain independent fair bits. Every branch remains \(X\mapsto q(P,S)X/2\).

Denote the antichain by A; the edge-plus-isolate parent by E, with \(u<v\) and isolate w; and the join by J, with roots u,w below z.

| Parent | Actual ideal(s) | New probability per ideal |
| --- | --- | ---: |
| A | empty; full | \(1/8\) each |
| A | each of three singletons | \(5/32\) |
| A | each of three pairs | \(3/32\) |
| E | empty | \(3/32\) |
| E | \(\{u\};\{w\}\) | \(1/8\) each |
| E | \(\{u,v\}\); full | \(1/4\) each |
| E | \(\{u,w\}\) | \(5/32\) |
| J | empty | \(7/32\) |
| J | each root singleton | \(5/64\) |
| J | root pair | \(1/8\) |
| J | full | \(1/2\) |

These list every ideal of the modified parents. Their row sums are, respectively,
\[
(4+15+9+4)/32=1,\quad
(3+4+4+8+5+8)/32=1,\quad
(14+5+5+8+32)/64=1.
\]
All entries are strictly positive. Fork and chain parent rows remain (2). Explicitly, the fork has empty/root probabilities \(1/8\), each root-plus-leaf ideal \(1/4\), and full probability \(1/4\); the chain row is \((1/8,1/8,1/4,1/2)\). Both sum to one. Earlier rows are the normalized accepted baseline, including the forced empty-parent row.

The rules depend only on order roles, treating interchangeable vertices equally. They are therefore order-covariant and mark-independent, with full ideal support. The horizon is exactly four births; no transition from a four-vertex parent is defined.

## 3. Exact cancellation of endpoint changes

The unchanged three-birth unmarked masses are
\[
\mu_3(A)=1/8,\quad \mu_3(E)=3/8,\quad
\mu_3(\mathrm{fork})=1/8,\quad
\mu_3(J)=1/8,\quad \mu_3(\mathrm{chain})=1/4.
\]
Only three four-vertex shapes receive changed incoming mass:

- X: one edge and two isolates.
- Y: a two-root join and one isolate.
- Z: four vertices u,w,z,v with relations \(u<z,\ w<z,\ u<v\), and no other strict relations.

Put \(\varepsilon=3/256\). Relative to the baseline, the changes in joint parent-to-endpoint probabilities are:

| Parent | X | Y | Z |
| --- | ---: | ---: | ---: |
| A | \(+\varepsilon\) | \(-\varepsilon\) | 0 |
| E | \(-\varepsilon\) | 0 | \(+\varepsilon\) |
| J | 0 | \(+\varepsilon\) | \(-\varepsilon\) |

For A, each singleton increases by \(1/32\), and each pair decreases by \(1/32\); multiplying their three actual occurrences by \(1/8\) gives the first row. For E, empty decreases and the two-minimum ideal increases by \(1/32\); multiplying by \(3/8\) gives the second. For J, empty increases by \(3/32\) and its two singleton probabilities each decrease by \(3/64\); multiplying by \(1/8\) gives the third.

The indicated ideals produce precisely X, Y or Z. Every other transition is unchanged. Each column sums to zero, so the entire unmarked four-birth endpoint law equals the baseline law.

This equality includes all marks, not only these three coarse events. Conditional on any unmarked endpoint P, every assignment of its four independent fair bits to distinct vertices is uniform, whatever its birth encoding. A marked orbit \([P,r]\) consequently has mass
\[
\mu_4([P])\,
\frac{|\operatorname{Aut}(P)|}
     {16\,|\operatorname{Aut}(P,r)|}.
\tag{3}
\]
The orbit-size factor retains all actual assignments; no uniform weighting of marked orbits is substituted. Since each unmarked mass is unchanged, every marked endpoint mass is unchanged. Its coarse-grained scalar map on common X is unchanged as well.

Thus all marked endpoint laws through four births equal the baseline, and
\[
\mu_nK_n=\mu_{n-1}\qquad(1\le n\le4)
\tag{4}
\]
follows from the baseline's accepted property.

## 4. What consistency fails to recover

Two distinct canonical four-birth encodings end in the same all-zero marked X:

1. Create \(1<2\), then isolated vertices 3 and 4. The unmarked prefix probability is \(1/8\); its last empty-E transition is \(3/32\).
2. Create an antichain on 1,2,3, then vertex 4 with past \(\{1\}\). Its prefix probability is \(1/8\); its last singleton-A transition is \(5/32\).

Their complete marked history weights are
\[
\frac18\frac3{32}\frac1{16}=\frac3{4096},
\qquad
\frac18\frac5{32}\frac1{16}=\frac5{4096}.
\]
They are different natural label encodings, not interchangeable extension representatives of one encoding. Equal endpoint probabilities have not forced equal history weights.

The conditional predecessor also differs. X receives masses \(15/256\) from A and \(9/256\) from E, so its actual previous unmarked endpoint is A with probability \(5/8\). But \(L(X)=12\), and deleting its edge's upper vertex leaves the antichain with six extensions; K therefore outputs A with probability \(1/2\). Equation (4) is a marginal statement, not equality of this conditional history law.

No single subset-weight row form G/Z can produce the modified rows: at parent size three its empty-ideal probability must be the same \(t_0/Z_3\) for every parent. Here the A, E and J empty probabilities are \(4/32,3/32,7/32\).

The example also explicitly violates the admitted diamond condition. From a two-antichain, append incomparable newborns with pasts \(\{u\}\) and empty. The structural route products are
\[
(1/4)(3/32)=3/128,\qquad
(1/4)(5/32)=5/128.
\]
Fair newborn bits multiply both by \(1/4\), so complete scalar maps still differ. This is a counterexample to the converse from endpoint consistency alone, not a counterexample satisfying the full DET contract. No all-size admissible continuation is asserted.

## 5. Reader-facing separation

**Sufficient construction:** the accepted subset-weight rows yield equal canonical history weights and hence intrinsic marginal consistency.

**Necessary principle:** consistency is a consequence within that family, but neither a unique selector there nor a sufficient finite characterization of its rows or history symmetry. This packet does not establish necessity across every DET-admitted law or settle an all-size converse.

**Observation choice:** K is a specified mathematical stochastic restriction. Choosing it does not identify the realized chronology or establish a physical detector. Uniform vertex deletion is a different kernel; its earlier obstructions remain.

The one finite counterexample closes the converse at the stated horizon. No higher-order audit, physical variable, experiment, efficient implementation, novel-law claim or successor is opened.
