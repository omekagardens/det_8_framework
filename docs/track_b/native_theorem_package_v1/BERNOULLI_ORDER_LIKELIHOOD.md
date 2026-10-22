# Intrinsic finite-order likelihood for the Bernoulli-subset law

Historical author status: manual theorem candidate; independent native adjudication pending.
Subsequent independent manual review and coordinator adjudication accepted the exact finite scope stated below.
Public edition: 22 October 2026.
Scope: fixed deterministic known size, exact completed unmarked order,
and the admitted from-empty Bernoulli-subset family only.

## 1. The finite likelihood theorem

Fix a known deterministic integer \(N\ge2\). At each birth \(j\), each
old vertex \(i<j\) is selected with probability \(p\), independently for
all pairs \(i<j\), where one separately fixed \(p\in(0,1)\) governs the
whole history. The newborn's strict past is the downward closure of the
selected subset. Equivalently, let \(E_{ij}\) be these independent Bernoulli
variables and take the transitive closure of the forward DAG with edges
\(i\to j\) when \(E_{ij}=1\). Induction on births gives this equivalence:
every old predecessor of a selected vertex reaches the newborn, and every
path to the newborn ends with a selected vertex.

Observe the complete faithful unmarked order only up to isomorphism.
There are no erased vertices, omitted or incorrect comparisons, stopping
rules, supplied prefixes, or observation-selection effects. The independent
fair marks are forgotten. The declared arbitrary fixed-carrier complex
PSD payload is scalar-passive and does not change this classical law.
The elementary-edge independence is an explicit premise of this optional
law, not a consequence derived here from DET's general principles.

For an \(N\)-vertex finite order \(P\), define these intrinsic quantities:

- \(c(P)\): the number of cover relations \(x\prec y\), meaning there is
  no \(z\) with \(x\prec z\prec y\). Each cover is counted once.
- \(i(P)\): the number of unordered incomparable pairs.
- \(e(P)\): the number of linear extensions, counted as increasing
  bijections from a fixed representative vertex set to \([N]\).
- \(a(P)=|\operatorname{Aut}(P)|\): the number of order automorphisms.

Write \(A(P)=e(P)/a(P)\). Then the exact isomorphism-class probability is
\[
\boxed{\Pr_p([P_N]=[P])=A(P)\,p^{c(P)}(1-p)^{i(P)}.} \tag{1}
\]
The ratio \(A(P)\) is a positive integer: it counts distinct naturally
labeled orders on the actual birth-label set \([N]\) in the class \([P]\).
It is neither the number of linear extensions alone nor \(N!/a(P)\).
There is no additional factor \(1/N!\).

At this fixed \(N\), \((c(P),i(P))\) is a minimal sufficient statistic
for \(p\). Formula (1) includes \(A(P)\) for the exact probability;
that factor cancels in likelihood comparisons between parameter values.
The family of observed-order distributions is identifiable in \(p\).
For an observed order the likelihood maximizer over the admitted open
interval is
\[
\widehat p=\frac{c(P)}{c(P)+i(P)}
\quad\text{if }c(P)>0,\ i(P)>0. \tag{2}
\]
If either count is zero, there is no maximizer in \((0,1)\); section 5
gives the exact supremum and boundary behavior.

## 2. Summing generating edge subsets

First fix one naturally labeled order \(Q\) on \([N]\): every comparison
\(u\prec_Q v\) has \(u<v\) in the birth-label ordering. Put
\(B=\binom N2\), \(c=c(Q)\), \(i=i(Q)\), and \(u=B-c-i\).
Here \(u\) counts comparable noncover pairs, and is nonnegative.

A forward edge subset has transitive closure exactly \(Q\) if and only if:

1. Every cover edge of \(Q\) is present.
2. No edge joining an incomparable pair of \(Q\) is present.
3. Each comparable noncover edge is freely either present or absent.

Necessity of the second condition follows because an edge is a comparison
in its own closure. A cover must be an edge: otherwise a path witnessing
that comparison has an intermediate vertex strictly between its endpoints,
contradicting the cover property.

For sufficiency, all edges in an allowed subset are comparisons in \(Q\),
so transitivity keeps their closure inside \(Q\). Conversely, every
comparison in a finite order is a chain of covers. One proof is induction
on the number of vertices in the interval: a noncover comparison splits
at an intermediate vertex into strictly smaller intervals. The present
cover edges therefore generate all comparisons of \(Q\).

Thus the edge-subset events above are an exact, disjoint description of
the closure preimage. Their probabilities sum to
\[
p^c(1-p)^i
 \sum_{S\subseteq U}p^{|S|}(1-p)^{u-|S|}
=p^c(1-p)^i\,[p+(1-p)]^u
=p^c(1-p)^i, \tag{3}
\]
where \(U\) is the set of \(u\) comparable noncover pairs.
This is a sum over edge subsets, not a sum over potentially overlapping
path witnesses. Redundant comparable edges have been marginalized, not
assumed absent.

The law's newborn bits contribute total factor
\(\sum_{r\in\{0,1\}^N}2^{-N}=1\).
There is no division by a payload trace; even zero PSD payload leaves the
separately defined classical order law meaningful.

## 3. Forgetting natural labels: the automorphism quotient

Choose a representative \(P\) with a fixed \(N\)-element vertex set \(V\).
Every increasing bijection \(\ell:V\to[N]\) transports \(P\) to a naturally
labeled order \(Q_\ell\). Conversely, every naturally labeled representative
of \([P]\) is obtained this way.

For increasing bijections \(\ell,m\),
\[
Q_\ell=Q_m
\quad\Longleftrightarrow\quad
m^{-1}\circ\ell\in\operatorname{Aut}(P). \tag{4}
\]
Indeed equality of the transported relations says exactly that this
bijection preserves and reflects the order. Precomposition by an
automorphism acts freely on the increasing bijections: if
\(\ell\circ\alpha=\ell\), injectivity gives \(\alpha=\mathrm{id}\).
Each fiber consequently has exactly \(a(P)\) elements. Since there are
\(e(P)\) increasing bijections, the number of distinct \(Q_\ell\) is
\(e(P)/a(P)\).

The events that the actual birth-labeled closure equals these distinct
\(Q_\ell\) are disjoint. Each has probability (3), with the same \(c,i\).
Adding them proves (1). The labels \([N]\) already have their generative
birth meaning; no uniform relabeling experiment has been added.
Counting all \(N!/a(P)\) labeled copies would also count copies incompatible
with increasing birth labels, and counting \(e(P)\) would overcount
automorphism-equivalent presentations.

All finite orders admit a linear extension (remove a minimal vertex and
induct), and every cover/forbidden-edge event has positive probability
for \(0<p<1\). Thus every \(N\)-vertex isomorphism class has positive mass.
The classes partition the finite edge experiment, so (1) is already
normalized over them; no further partition function is needed.

As symbolic checks: an antichain has \(e=N!\), \(a=N!\), hence \(A=1\);
a chain has \(e=a=1\). A three-vertex fork has \(e=a=2\), also \(A=1\).
A three-vertex order with one comparison and one isolate has \(e=3\),
\(a=1\), hence \(A=3\). These distinguish the counting conventions.
They are manual finite counts, not an enumeration or numerical executor.

## 4. Sufficiency and identification

Let \(\mathcal P_N\) be the finite set of order isomorphism classes and
\(T([P])=(c(P),i(P))\). For any attained \(t=(c,i)\), set
\[
W_t=\sum_{\substack{[Q]\in\mathcal P_N\\T([Q])=t}} A(Q)>0.
\]
Equation (1) gives
\[
\Pr_p(T=t)=W_t p^c(1-p)^i,\qquad
\Pr_p([P]\mid T=t)=\frac{A(P)}{W_t}
\quad(T([P])=t). \tag{5}
\]
The conditional distribution is independent of \(p\), proving sufficiency
directly on this finite sample space. The likelihood of the summary
and of the full order differ only by a positive \(p\)-independent factor,
so they have the same likelihood ratios and maximizers.

For minimality, the ratio of the masses of \([P]\) and \([Q]\) is
\[
\frac{A(P)}{A(Q)}
 p^{c(P)-c(Q)}(1-p)^{i(P)-i(Q)}. \tag{6}
\]
It is constant for all \(p\in(0,1)\) exactly when both count differences
are zero. To see necessity, logarithmic differentiation of its positive
\(p\)-dependent part gives
\[
\frac{\Delta c}{p}-\frac{\Delta i}{1-p}=0
\quad\Longrightarrow\quad
\Delta c-(\Delta c+\Delta i)p=0
\quad\text{for every }p\in(0,1),
\]
so \(\Delta c=\Delta i=0\). Sufficiency is immediate.
If any other statistic \(S\) is sufficient and \(S([P])=S([Q])\), the
ratio of their conditional probabilities within that fiber is independent
of \(p\). All masses are positive, so (6) must be constant. It follows
that \(T([P])=T([Q])\); \(T\) is therefore a function of \(S\).
This is minimal sufficiency without an unproved statistical criterion.

Parameter identifiability is simpler. The observable antichain class has
\[
\Pr_p([P_N]=[A_N])=(1-p)^{\binom N2}, \tag{7}
\]
strictly decreasing on \((0,1)\) because \(N\ge2\).
Equal observed-order distributions must have equal probabilities in (7),
hence equal parameters. The statistic \(T\) also preserves identifiability,
since its value \((0,\binom N2)\) occurs only for the antichain.
This is a statement about entire probability distributions, not the
ability to read an unknown real parameter exactly from one realized order.

No premise of repeated observations is used. If sizes zero or one were
instead considered, only one unmarked order is possible and its mass is
one for every \(p\); that separate trivial experiment is not identifiable.
This explains the stated domain \(N\ge2\).

## 5. Exact maximization and its limitations

For an observed class, write \(c=c(P)\), \(i=i(P)\). Its log likelihood is
\[
\log A(P)+c\log p+i\log(1-p),\qquad 0<p<1. \tag{8}
\]
For \(N\ge2\), \(c+i>0\). If the order has any comparison, its cover-chain
decomposition supplies a cover, so \(c=0\) occurs exactly for the
antichain, with \(i=\binom N2>0\). If \(i=0\), the order is a chain,
with \(c=N-1>0\).

When \(c,i>0\), differentiation gives
\[
\frac{d}{dp}\log L(p)=\frac c p-\frac i{1-p},\qquad
\frac{d^2}{dp^2}\log L(p)=-\frac c{p^2}-\frac i{(1-p)^2}<0.
\]
There is a unique stationary point (2), strictly between zero and one,
and the likelihood tends to zero at both ends. It is the unique global
maximizer; the maximal value is
\[
A(P)\left(\frac c{c+i}\right)^c
     \left(\frac i{c+i}\right)^i. \tag{9}
\]

For the antichain, \(L(p)=(1-p)^{\binom N2}\) is strictly decreasing;
its supremum is 1 as \(p\downarrow0\), not attained in the admitted family.
For the chain, \(L(p)=p^{N-1}\) is strictly increasing;
its supremum is 1 as \(p\uparrow1\), again not attained.
Treating zero or one as a reported boundary estimate would extend the
optimization domain, not provide an MLE in the admitted open interval.
At \(N=2\), these are the only two observable classes, so no observation
has an interior MLE.

The algebraic appearance of (8) does **not** make the random order
statistics \(c,i\) independent Bernoulli successes and failures with
trial count \(c+i\). They are functions of the dependent transitive
closure, and their sum can depend on the observed order. For instance,
at \(N=3\) a chain has \(c+i=2\), while an antichain has \(c+i=3\).
The independent variables used in the proof are the latent \(E_{ij}\);
the observed order does not reveal all their outcomes. Equations (3)
and (5), rather than a claimed binomial sampling law for these summaries,
justify the likelihood.

Minimal sufficiency, distribution-level identifiability, and an exact
likelihood optimizer are three distinct finite statements. None proves
unbiasedness, consistency as \(N\) grows, error rates, confidence coverage,
posterior probability, or calibration from a single observed order.
Indeed every class has positive probability under every admitted \(p\);
one finite observation cannot uniquely rule out all other parameters or
provide zero-error discrimination between two distinct parameters.
No consistency or inference-calibration project is opened.

## 6. Model, computational and source boundaries

Computing likelihood ratios or the interior maximizer needs only the
two intrinsic counts. Evaluating the absolute mass in (1) additionally
needs the exact combinatorial coefficient \(e/a\). This existence formula
is not a claim of an efficient general counting algorithm; no enumeration,
optimizer, simulation, likelihood evaluation or scientific executor was
run. The proofs use only finite edge-subset partitioning, automorphism
fiber counting, conditional probabilities and elementary differentiation.

The exact observation contract remains load-bearing. No result transfers
here to erasure, partial or unfaithful comparisons, random or selected
size, another seed law, a different parameter history, or GWOSC strain.
The accepted unknown-size erasure theorem is not extended or reinterpreted.
Neither the optional Bernoulli law nor its independent-edge premise is
uniquely selected by the declared model principles. No physical readout,
clock, action/work-store, quantum reconstruction, geometry, mass/gravity
or application-value claim follows. Marks and passive payload remain
part of the underlying model; this statistic is only an order observation.

The four supplied literal manuscripts have distinct roles:

- BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md supplies the elementary
  independent-edge law, closure construction and individual-ideal law.
- LAW_DEPENDENCE.md and THEOREM_PACKAGE.md distinguish optional laws,
  declared scalar-passive premises and other fixed-instance results.
- UNKNOWN_SIZE_HEIGHT_DIAGNOSTIC.md supplies the accepted predecessor and
  its observation/error boundaries, not a premise for formula (1).

The authorized source bodies do not already establish this whole
finite unlabelled likelihood/sufficiency/identification result. The
package's P4 shape/width likelihood references concern a different
fixed-carrier/marking problem. No linked document was followed and no
claim of literature novelty or repository-wide absence is made.

## Publication and evidence boundary

Independent manual review checked the closure fibers, natural-label multiplicity, minimal sufficiency, identifiability and boundary optimization. Administrative current-source and readback checks support correspondence, not the mathematics or historical custody. Private raw receipts, source identity maps and machine metadata are withheld under the publication policy. Historical source-body reuse, metadata-only readbacks, display truncations and their recoveries retain their narrower status; this derivative does not reconstruct a custody package. No scientific executor ran for this theorem. The author's historical pending header above is preserved as provenance, with subsequent acceptance stated separately.

The [consolidated theorem package](THEOREM_PACKAGE.md), [law-dependence audit](LAW_DEPENDENCE.md), [Bernoulli law construction](BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md), and [unknown-size height diagnostic](UNKNOWN_SIZE_HEIGHT_DIAGNOSTIC.md) retain their distinct assumptions. The new auxiliary-seed identifiability question and separate measurement, relational-state, energy and computing packages are excluded from this publication. RET remains paused.
