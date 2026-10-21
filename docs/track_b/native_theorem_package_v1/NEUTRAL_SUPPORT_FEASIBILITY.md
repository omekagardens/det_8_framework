# Neutral-support feasibility for the height-design boundary

21 October 2026. Manual exact finite-layer mathematics.
Independent review is recorded separately from this source manuscript. No numerical optimization,
scientific program, probability evaluation, simulation or experiment.

## 1. Decision

**A zero boundary minimum is feasible at parent sizes two and three,
for every admitted strictly positive lower prefix of the corresponding
length.** Shared components and complete marked-row constraints do not
force a positive closed-polytope minimum at either size.

The witnesses below are fully normalized boundary rows, compatible with
every diamond contained in their respective finite prefixes. Each puts
probability one on a height-neutral ideal in every marked row.
Explicit component coefficients and complete diamond matrices verify
the claim. These are not strictly positive laws: many branches, including
every full birth, have probability zero.

For a fixed positive lower prefix at either of these sizes:

- The closed capacity polytope has minimum expected height increment zero.
- Every strictly positive next layer has positive expected height increment.
- Strict restoration of the displayed witness makes that increment
  arbitrarily small, so the strict feasible set has infimum zero,
  not an attained zero minimum.

These are separate one-layer statements. The zero size-two boundary
cannot be used as the strictly positive lower prefix of the size-three
argument. No all-size zero-boundary theorem, Cesaro decay, almost-sure
sublinear growth, target approximation or geometry result is claimed.

At general size, the exact remaining condition is a simultaneous
nonnegative row-saturation equation on globally height-neutral
components. A structural terminal-order test identifies those components.
It does not automatically solve their shared row equations.

## 2. Model and actual-history support

Use the admitted scalar-passive record-marked growth model from
[THEOREM_PACKAGE](THEOREM_PACKAGE.md) and the accepted [HEIGHT_DRIFT_LAW_SELECTION](HEIGHT_DRIFT_LAW_SELECTION.md) theorem.
A birth chooses an ideal \(S\) of a finite marked order \((P,r)\),
adds a maximal vertex with strict past \(S\), and assigns a fair bit.
The complete branch map is
\[
             \mathcal B^{P,r}_{S,b}(\mathfrak D)
                      =q(P,r,S)\mathfrak D/2,\qquad b=0,1.
\]
Old relations and marks are unchanged. A positive lower prefix has
\(q(P,r,S)>0\) for every ideal of every parent in its domain.
Proper probabilities may read the whole unmarked parent but only
the marks in \(S\); full probabilities are complete complements.
Marked equivariance and all incomparable-birth diamonds are required:
\[
 q(C,r,S)q(C+S,r+b,T)
 =q(C,r,T)q(C+T,r+c,S).                                    \tag{1}
\]
The second precursor excludes the other newborn. Equal precursors,
all old marks, both newborn bits and the complete payload are included.
Each two-step map carries the common factor \(1/4\).

Fix a free parent size \(n\) and an admitted strictly positive lower
prefix through parent size \(n-1\), starting from the empty order.
Let \(j=(P_j,r_j)\) range over a complete finite set of marked parent
classes of size \(n\). Its history weight \(\pi_j\) is the sum of
the actual \(q/2\)-weighted natural histories reaching that class.

**Full-support lemma.** Every \(\pi_j>0\).

To prove it, take any marked finite order and a linear extension of it.
Insert its vertices in that order. At each insertion the already
inserted strict past is an eligible ideal, and assign the specified
bit. Every factor in this finite \(q/2\) product is strictly positive,
including the first fair bit. Thus at least one history reaching the
specified marked class has positive mass. Summing all histories
preserves positivity. The complete history distribution is normalized,
so \(\sum_j\pi_j=1\).

This establishes support, not equal weights. Marked-isomorphism
multiplicities and the number of natural histories can differ;
no uniform-over-shapes or uniform-over-markings replacement is made.
Conditioning on one realized parent would be a different objective.
The result here uses the actual complete lower-prefix distribution.

Height \(h\) counts vertices, with \(h(\varnothing)=0\). The accepted
exact increment is
\[
 e_j(S)=h(P_j+S)-h(P_j)=\mathbf1_{\{h(S)=h(P_j)\}}.
\]
Both newborn bits sum to \(q_j(S)e_j(S)\), so the complete row drift is
\[
                 p_j=q_j(P_j)+
                    \sum_{\substack{S\subsetneq P_j\\e_j(S)=1}}q_j(S).
                                                               \tag{2}
\]
In particular a full birth always raises height. Payload passivity and
the separately specified classical kernel do not reconstruct quantum
dynamics; no trace normalization of a zero payload is used.

## 3. Exact zero-support and row-saturation criterion

For \(n\ge1\), use the admitted positive finite proper-slot potential
\[
 u_j(S)=
 \prod_{\varnothing\ne A\subseteq\operatorname{Max}(P_j)\setminus S}
 q(P_j\setminus A,r_j|_{P_j\setminus A},S)^{(-1)^{|A|+1}}.    \tag{3}
\]
The component key \(c(j,S)\) retains the whole unmarked parent and
selected marks and all inherited ratio identifications. It is not
merely an ideal size or a child shape.
Each individual ideal occurrence contributes separately to
\[
 A_{jc}=\sum_{\substack{S\subsetneq P_j\\c(j,S)=c}}u_j(S),
 \qquad K_n=\{\alpha\ge0:A\alpha\le\mathbf1\}.                \tag{4}
\]
Proper probabilities are \(u_j(S)\alpha_{c(j,S)}\); full probability
is \(1-(A\alpha)_j\). The closed set allows zero branches, as a
boundary optimization domain, not as the strictly positive law family.
The expected objective is
\[
               \Psi_n^H(\alpha)=\sum_j\pi_jp_j(\alpha).
\]

Let \(\mathcal C_0\) be the components for which **every** proper-slot
occurrence in every marked row is height-neutral:
\[
 c\in\mathcal C_0
 \quad\Longleftrightarrow\quad
 e_j(S)=0\ \text{whenever }c(j,S)=c.                         \tag{5}
\]
Because all \(\pi_j>0\), \(u_j(S)>0\), and every term of (2) is
nonnegative, \(\Psi_n^H(\alpha)=0\) holds exactly when every full
probability is zero and every height-raising proper probability is zero.
A single raising occurrence forces its shared coefficient to vanish.
Consequently
\[
 \boxed{\quad
 \min_{\alpha\in K_n}\Psi_n^H(\alpha)=0
 \quad\Longleftrightarrow\quad
 \exists\,\alpha_{\mathcal C_0}\ge0:
        A_{\mathcal C_0}\alpha_{\mathcal C_0}=\mathbf1.
 \quad}                                                     \tag{6}
\]
Set all other coefficients to zero for the reverse implication.
Then complete row sums are one and all supported proper slots are neutral.

No row can be discarded as negligible. Although actual positive
weights affect a positive optimum, their numerical values do not
affect this exact zero-feasibility test. Local neutrality of one
occurrence is not enough; shared components impose (5).

For precision, \(K_n\) is compact: it contains zero, is closed, has
finitely many components, and each occurring component has some
\(A_{jc}>0\), which bounds \(\alpha_c\le1/A_{jc}\).
Thus the minimum is attained. If (6) is infeasible, that fixed
prefix's minimum is strictly positive, not merely unattained zero.
This gives no uniform bound over different sizes or lower prefixes.

At \(n=0\) there are no proper components. The sole empty/full
precursor makes the first birth with probability one, so the drift
and its minimum are one. Criterion (6) is used only for \(n\ge1\).

## 4. Structural test for a globally neutral component

For a proper birth, let \(Q=P+S\). Its newborn is maximal and \(Q\)
has at least two maximal vertices. Conversely each maximal \(v\)
of such a \(Q\) defines an incoming proper slot
\[
                 (Q-v,\ \operatorname{Past}_Q(v)).
\]
All those incoming presentations have the same unmarked terminal order.

Fix a complete marking of \(Q\) and two distinct maxima \(v,w\).
Removing both gives a base of size \(n-1\). The two routes that add
\(v,w\) in either order form a complete diamond. The first factors
belong to the strictly positive lower prefix; the second factors
are the two incoming size-\(n\) proper slots. Therefore (1) relates
them by a strictly positive ratio. This holds for every pair of maxima
and every marking. It propagates a forced zero from any incoming
presentation to every other incoming presentation for that marking.

Relabeling and precursor-record identifications cannot change the
unmarked terminal shape. Components may still split according to
records; the following reasoning applies to each such component.
Given any slot's selected marks, extend them to a complete terminal
marking and apply the preceding diamond. No old or newborn bit is
discarded in doing so.

An incoming birth at \(v\) is neutral exactly when
\(h(Q-v)=h(Q)\). Let a height endpoint mean a maximal vertex at
which some longest chain of \(Q\) ends. Every longest chain ends
at such a vertex. Then
\[
 \boxed{\quad
 h(Q-v)=h(Q)\ \text{for every maximal }v
 \quad\Longleftrightarrow\quad
 Q\text{ has at least two distinct height endpoints}.
 \quad}                                                     \tag{7}
\]
If there are two, deleting one maximum leaves a longest chain ending
at the other; deleting any other maximum also leaves one.
If there is only one height endpoint \(v\), every longest chain
contains \(v\), and deleting it reduces height by one.

It follows that all components belonging to a terminal shape with
two height endpoints are globally neutral. If the terminal has a
unique height endpoint, its raising incoming slot forces every
incoming component to zero in a zero-drift solution, including
locally neutral occurrences.

Every nonempty parent has at least one globally neutral possible
terminal: choose a maximal endpoint \(v\) of a longest chain and
add a new vertex with the same strict past as \(v\).
The old and new endpoints both attain the unchanged height.
This is a support-coverage fact only. Different rows may share
components with different positive potentials, and (6) still requires
a single vector saturating all their capacities. Nonempty neutral
support in each row does not by itself prove feasibility.

## 5. General positive lower prefixes through size two

The finite witnesses below do not assume the source's optional numerical
seed. Their lower-prefix parameters are forced into the following form
by the declared locality, normalization, equivariance and diamonds.

At a singleton, let the empty probability be \(a\). Proper locality
makes it independent of the singleton bit, and strict positivity gives
\(0<a<1\). Full probability is \(1-a\).

At parent size two, write the complete rows as follows. For a chain
\(x<y\), \(i=r_x\); for an antichain, both singleton occurrences are
listed separately:
\[
\begin{array}{c|c|c}
\text{parent}&\text{precursor}&q\\ \hline
C_2&\varnothing&c\\
C_2&\{x\}&f_i\\
C_2&\{x,y\}&h_i=1-c-f_i\\ \hline
A_2&\varnothing&d\\
A_2&\{x\}&g\\
A_2&\{y\}&g\\
A_2&\{x,y\}&k=1-d-2g
\end{array}                                                  \tag{8}
\]
The mixed singleton-base diamond gives
\[
                       a g=(1-a)c,\qquad
                       g=\frac{(1-a)c}{a}.                  \tag{9}
\]
Initially the antichain singleton probability could depend on its
selected bit. Equation (9), valid for every singleton mark, forces
that dependence away. Full complements then give the displayed \(h_i,k\).
The inequalities are
\[
 c,d,f_0,f_1,h_0,h_1,g,k>0.                                 \tag{10}
\]

This describes **every** admitted positive prefix through parent two.
Conversely, any parameters satisfying \(0<a<1\), (9) and (10)
give such a prefix: locality and normalization are explicit;
the singleton-base equal-empty and equal-full diamonds are
identities, the mixed diamond is exactly (9), and the empty-base
diamond holds because \(a\) is independent of the old bit.
All newborn bits and relabelings are respected.
Thus this is a complete declared positive prefix family, not a
claim that DET uniquely selects these parameters.

The size-two design below holds only the smaller singleton prefix fixed.
The size-three design holds a complete positive prefix (8) fixed.
The source's optional seed is an instance of this family; no historical
coefficient certificate is evaluated or needed.

## 6. Exact size-two boundary witness

Keep any positive singleton prefix \(0<a<1\).
For every marking prescribe the following **complete** boundary rows:
\[
 \begin{array}{c|c|c}
 \text{parent}&\text{sole probability-one ideal}&
                    \text{all other ideals, including full}\\ \hline
 A_2&\varnothing&0\\
 C_2=\{x<y\}&\{x\}&0
 \end{array}                                                \tag{11}
\]
The selected heights are respectively \(0<1\) and \(1<2\).
Thus each row is normalized and has zero complete height increment.

To verify every new diamond, the only base shape is a singleton.
Order its ideals as \((\varnothing,\mathrm{full})\) and define
\[
 R_{S,T}=q(C,r,S)\,
             q^{\partial}(C+S,r+b,T),
\]
where \(q^\partial\) is (11).
For any base mark and newborn bits, the route-product matrix is
\[
                   R=\begin{pmatrix}a&0\\0&1-a\end{pmatrix}.
                                                               \tag{12}
\]
It is symmetric, exactly the two-route requirement in (1), with
the newborn marks exchanged between the two routes. Equal precursor
pairs are included. Earlier diamonds are unchanged.

In convention (3), the nonzero proper-slot potentials and component
coefficients are
\[
 \begin{array}{c|c|c|c}
 \text{slot}&u&\alpha&\text{terminal}\\ \hline
 (A_2,\varnothing)&a^2&a^{-2}&A_3\\
 (C_2,\{x\}),\ r_x=i&1-a&(1-a)^{-1}&
                              \text{one root, two leaves}
 \end{array}                                                \tag{13}
\]
The fork's selected root mark remains part of the component
presentation; the same displayed coefficient works in both sectors.
Set every other component coefficient to zero.
In particular the chain-empty and antichain-singleton occurrences
linked by the mixed diamond are both zero.

Deleting any maximal vertex from either displayed terminal yields
the same listed parent/precursor type. Thus the selected presentation
set is closed under all incoming aliases. Distinct terminal shapes
cannot be joined by a ratio edge; no unlisted slot is secretly forced
positive by this prescription. Formula (13) gives exactly (11)
and saturates every row of (4).

Since the objective is nonnegative and every row drift is zero,
\[
          \boxed{m_2^H=0\quad\text{for every admitted
                  positive lower prefix through parent one}.} \tag{14}
\]
No numerical history weights or optimization are required.

## 7. Exact size-three boundary witness

Now keep **any** strictly positive lower prefix (8)–(10) through
parent two. Let \(E=C_2\sqcup A_1\), let \(F\) be the fork with
one root and two leaves, and let \(J\) be the join with two roots
and one top. The five unmarked three-parent types are exhausted by
\(A_3,E,F,J,C_3\).

For every old marking use the following complete boundary rows:
\[
 \begin{array}{c|c|c|c}
 P&\text{sole probability-one ideal }S&h(P)&h(S)\\ \hline
 A_3&\varnothing&1&0\\
 E&\text{its isolated vertex}&2&1\\
 F&\text{its root}&2&1\\
 J&\text{its two-root ideal}&2&1\\
 C_3&\text{its initial two vertices}&3&2
 \end{array}                                                \tag{15}
\]
Every unlisted proper ideal and every full ideal has probability zero.
The selected subset is unambiguously specified by the unmarked order,
so these rows respect marked equivariance and precursor-record locality.
They ignore marks, but the lower potentials and component coefficients
need not.

All rows sum to one and each has zero drift. This alone would not
establish shared-component feasibility; the following checks do.

### Complete last-diamond matrices

Every new diamond has base size two, hence base \(C_2\) or \(A_2\).
For \(C_2=\{x<y\}\), let \(i=r_x\) and order its ideals as
\((\varnothing,\{x\},\{x,y\})\).
The full route-product matrix is
\[
 R_{C_2}=
 \begin{pmatrix}
 0&0&0\\
 0&f_i&0\\
 0&0&h_i
 \end{pmatrix}.                                             \tag{16}
\]
An empty first birth gives \(E\) with the newborn as its isolate;
the second precursor excludes that newborn, so the first row is zero.
A root first birth gives \(F\), whose selected next precursor is
the old root. A full first birth gives \(C_3\), whose selected next
precursor is the old entire base. These facts account for every entry.

For \(A_2=\{x,y\}\), order the four ideals as
\((\varnothing,\{x\},\{y\},\{x,y\})\).
The complete matrix is
\[
 R_{A_2}=
 \begin{pmatrix}
 d&0&0&0\\
 0&0&g&0\\
 0&g&0&0\\
 0&0&0&k
 \end{pmatrix}.                                             \tag{17}
\]
An empty first birth gives \(A_3\), selecting empty again.
A birth above \(x\) gives \(E\) whose isolate is the old \(y\),
and conversely. A full first birth gives \(J\), selecting the
old pair of roots. Crucially, the off-diagonal entries agree because
(9) forced both singleton probabilities to be the same \(g\),
even for unequal root marks.

Matrices (16)–(17) cover all ordered ideal pairs, including equal
precursors. They are symmetric for every inherited marking and both
newborn bits. Each route multiplies the same transported arbitrary
payload by its displayed entry divided by four. Thus these are
complete unnormalized marked-map checks, not merely normalized
probability comparisons. All earlier diamonds are unchanged.

### Explicit shared-component and potential witness

The complete list of nonzero component types is:
\[
 \begin{array}{c|c|c|c}
 \text{parent / selected ideal}&u&\alpha=1/u&\text{terminal}\\ \hline
 A_3/\varnothing&d^3/a^3&a^3/d^3&A_4\\
 E/\text{isolate}&g&1/g&C_2\sqcup C_2\\
 F/\text{root of mark }i&f_i^2/(1-a)&(1-a)/f_i^2&
                              \text{one root, three leaves}\\
 J/\text{root pair}&k&1/k&A_2\oplus A_2\\
 C_3/\text{initial pair, bottom mark }i&h_i&1/h_i&C_2\oplus A_2
 \end{array}                                                \tag{18}
\]
Here \(\oplus\) denotes ordinal sum; in \(A_2\oplus A_2\) every
lower vertex precedes every upper vertex.
All denominators are strictly positive by the lower-prefix hypotheses.

These potentials follow directly from (3):

- For \(A_3,\varnothing\), the three single-maximal deletions give
  \(d^3\), the three double deletions give \(a^{-3}\), and the
  triple deletion gives the empty-parent factor one.
- For \(E\)'s isolate, the only maximal vertex outside the precursor
  is the edge's top. Deleting it gives an \(A_2\) singleton slot \(g\).
- For the fork root, the two single-leaf deletions each give \(f_i\);
  deleting both leaves gives the singleton full factor \(1-a\)
  in the denominator.
- For the join's root pair, deleting its sole top gives \(k\).
- For the chain's initial pair, deleting its top gives \(h_i\).

For each terminal in (18), deleting **any** maximal vertex returns
the corresponding listed parent/precursor type. Thus no additional
parent shape or unlisted ideal enters that terminal's component.
The terminal types are mutually distinct.

Record identifications also agree. The star's root mark and the
chain-prefix bottom mark are in their selected precursors, so the
displayed dependence is allowed. Other selected marks remain
in the component key even when the coefficient happens not to
depend on them. The two-edge terminal aliases have identical
potential \(g\), as proved in (9); no unequal-mark alias has been
silently averaged. Leaf and newborn marks do not alter any entry.
Assign the displayed value to each corresponding record component,
and zero to every unlisted component.

This is one shared component vector, not a set of independently
optimized rows. Its products give exactly (15), so
\(A_{\mathcal C_0}\alpha_{\mathcal C_0}=\mathbf1\).
It follows that
\[
          \boxed{m_3^H=0\quad\text{for every admitted
                  positive lower prefix through parent two}.} \tag{19}
\]

## 8. Boundary zero versus a positive restored law

Equations (14) and (19) are universal within their declared
positive lower-prefix classes; they are not limited to the optional
numerical seed in the source. They do not describe two consecutive
zero layers of one admitted positive law.

In particular, feeding the size-two zero boundary into the size-three
potential formulas would violate positivity and introduce vanishing
denominators. The size-three proof starts instead from a genuinely
positive parent-two prefix. This may be the source prefix, another
member of (8)–(10), or a strictly restored earlier construction,
provided all the lower-prefix hypotheses hold. No old later layer
may be retained unchanged after changing a lower law.

For a fixed lower prefix at either tested size, let \(\alpha^\partial\)
be the displayed zero-drift vector. Retain the accepted restoration
construction, in the same potential convention:
\[
 T_j=\sum_{S\subsetneq P_j}u_j(S),\quad
 B_n=\max_jT_j,\quad a_n=\frac1{2(1+B_n)},\quad
 \alpha^\circ=a_n\mathbf1,
\]
\[
       \widetilde\alpha=(1-\eta)\alpha^\partial+\eta\alpha^\circ,
                    \qquad0<\eta<1.                       \tag{20}
\]
All marked rows and individual ideal multiplicities enter \(B_n\).
The accepted bounds give positive proper probabilities and a full
complement at least \(\eta(1/2+a_n)>0\).
Affinity gives the exact finite-layer identity
\[
 \Psi_n^H(\widetilde\alpha)
       =\eta\Psi_n^H(\alpha^\circ),\qquad
 0<\eta(1/2+a_n)\le\Psi_n^H(\widetilde\alpha)\le\eta.         \tag{21}
\]
No numerical value is evaluated.

Thus strict feasible layers have infimum zero at \(n=2,3\), approached
by \(\eta\downarrow0\) with that lower prefix held fixed.
They cannot attain zero: each full probability is strictly positive,
every \(\pi_j>0\), and (2) makes their objective positive.
This is a family of compatible next-layer prefixes, not an infinite
zero-growth process. The already accepted restoration/Cesaro and
actual-history distinctions are unchanged.

A paired positive potential gauge rescales columns of (4) and
inversely rescales \(\alpha\); actual probabilities, drift and zero
feasibility are unchanged. Reselecting a common-coordinate reference
in a different gauge can change the law. A genuine prefix change
requires later potentials, history weights and rows rebuilt from
that changed positive prefix.

## 9. Decision table and exact unresolved condition

| Question | Bounded answer | Limit |
| --- | --- | --- |
| Which rows matter for exact zero? | Every complete marked row has positive actual history mass | Weights are not uniform; conditioning on one realized row is different |
| When can the boundary objective be zero? | Precisely (6), with all raising components removed and every row saturated | Compactness makes infeasibility a strictly positive fixed-prefix minimum |
| Which terminal components can survive? | Exactly those whose terminal has at least two longest-chain endpoints | Having an available neutral component in each row does not solve shared capacities |
| Size-two boundary | Explicit universal zero witness (11)–(14) | Requires a positive singleton lower prefix |
| Size-three boundary | Explicit universal zero witness (15)–(19) | Requires a positive lower prefix through parent two |
| Strict positive next layers at these sizes | Every objective is positive; infimum is zero by (20)–(21) | No zero minimum is attained inside the strict family |
| All larger sizes | Not settled | Need a simultaneous witness for (6), or an incompatibility proof, for the actual inherited positive prefix |
| Recursive sublinear height or target growth | Not settled | Finite zero minima do not prove minima Cesaro decay, actual-history drift decay or target approximation |

This closes the requested nontrivial finite-layer feasibility question.
The general all-size question is left as the explicit shared equation
(6) with structurally characterized columns, not as an assertion that
rowwise choices suffice. No further layer, coefficient audit or
automatic reduction chain is started.

The new height-law design remains separate from the existing
expected-Ferrers-defect objective. Neither that objective, its historical
canonical coefficients nor its unresolved claims is altered.
The accepted height/drift theorem remains necessary for the declared
sublinear-height targets; feasibility at two finite boundaries is not
a successful asymptotic law or a derivation of geometry.

Cardinality is not physical time. No physical clock, metric, manifold
dimension, Lorentzian embedding, mass/gravity/QM, empirical observation
or application-performance claim follows. The completed prospective
GWOSC replay and rejected C256 raw-cost advantage remain separate.
RET remains paused; other historical custody and validation
prerequisites are preserved.

## 10. Provenance, receipts and stop boundary

The public exposition dependencies and their scientific roles are:

| Source | Provenance and use |
| --- | --- |
| [HEIGHT_DRIFT_LAW_SELECTION.md](HEIGHT_DRIFT_LAW_SELECTION.md) | Accepted height-drift manuscript; complete height objective, convergence distinctions and restoration bounds |
| [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) | Accepted public exposition; model, ratio potential and separate Ferrers objective |
| [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) | Accepted public exposition; prefix-change and paired-gauge boundaries |
| [HALF_SCALE_HEIGHT_GROWTH.md](HALF_SCALE_HEIGHT_GROWTH.md) | Accepted public exposition; selected half-scale law, not a universal law |
| [INTRINSIC_GEOMETRY_TARGET_SCREEN.md](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Accepted public exposition; fixed-target necessary conditions, not a converse geometry theorem |

The original source record distinguishes the accepted native height-drift
manuscript from four public exposition snapshots. The first link here is
its public derivative; it does not claim that the private native manuscript
was already published with those other snapshots. Historical pending-header
metadata does not determine separately recorded review status. The source
record's public provenance attribution was not independently verified by
network or Git operations.

Private snapshot pins and adjudication records are withheld. Paths and
commands printed inside those records are metadata, not authority to open
linked originals, archives, coefficient certificates, protected custody or
validation inputs. Public links identify premises, not executable custody.

For the source-author's original capture and consumption process, the
retained account is:

Fresh full native source captures and actual native hash/size outputs
are retained. The height-drift and half-scale-height bodies exactly
matched previously fully consumed bodies. Package and law snapshots
matched previously consumed complete prefixes plus their displayed new
target-screen paragraphs. The current public target-screen manuscript
was separately displayed and read in full. No display truncation
occurred in these source-author reads; earlier historical display,
execution and custody limitations remain preserved rather than erased.

The source-receipt and result-receipt readback entries are metadata-only
summaries of reported command completion, parsing and exact-body-match
outcomes, distinct from the retained full native captures. Supplied-context
worker conclusions and their usage observations remain worker-reported
records, not direct coordinator tool observations or fresh source audits.

The original evidence limitation is retained exactly:

Separate read/hash observations are not atomic identity certificates;
current matches do not reconstruct original custody or repair prior
source-check, execution, receipt-matching or validation failures.
Manual worker checks are not independent source-custody adjudication.

For the source-author's construction, the retained statement is:

All mathematics here is manual exact symbolic reasoning.
No numerical optimizer, probability/tail/interval evaluation, coefficient
program, simulation, benchmark, scientific source execution, data
acquisition, dependency installation or experiment was performed.
The rational expressions and matrices are displayed proofs, not tool
evaluations of scientific quantities.

Those statements concern source-author activity. Later independent review
and its separate checks are recorded separately. This derivative does not
claim a machine proof or scientific acceptance by its preparer.

The size-two and size-three zero boundary witnesses remain separate tests,
each universal over its declared admitted strictly positive lower-prefix
class. They are not consecutive zero layers of a positive law. At each
tested size and fixed positive lower prefix, every strictly positive next
layer has positive objective, with infimum zero approached by restoration;
the zero minimum is attained only in the closed boundary domain. Neutral
support in each row does not by itself solve simultaneous shared capacities.
Larger sizes, recursive drift decay, sublinear height, target approximation
and geometry remain unresolved. Existing Ferrers objectives and separate
project findings retain their stated scope.

Private identifiers, exact paths, hashes, timestamps, receipt filenames
and tool/account metadata are withheld; the original evidence and exact
correspondence remain local. No scientific executor, optimizer, sampler,
dataset, experiment or physical readout is supplied or authorized. Frozen
protocols and protected validation remain unchanged. RET remains paused.

See [the publication note](PUBLICATION_NOTE.md) and
[the public publication policy](../../coordination/REDACTED_PUBLICATION.md)
for the public/private boundary.
