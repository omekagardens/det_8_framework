# Joint height/density obstruction to Ferrers retention

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: unrestricted finite coordinatewise Ferrers cell orders, induced
restriction of completed orders, and the supplied accepted fixed-law results.
No new law, target or stochastic constant optimization.

## 1. Joint criterion and the closed boundary

For a finite poset \(P\), let \(H(P)\) be maximum chain cardinality and
\(I(P)\) the number of unordered pairs of distinct incomparable vertices.
Let \(\mathcal F\) be the unrestricted class of finite coordinatewise
Ferrers cell orders, including empty. Define

\[
 R_{\mathcal F}(P)=
 \max\{|W|:W\subseteq V(P),\ P[W]\in\mathcal F\},\qquad
 D_{\mathcal F}(P)=|P|-R_{\mathcal F}(P).
 \tag{1}
\]

Then, for any sequence of \(N\)-vertex posets,

\[
 \boxed{
 H_N=O(\sqrt N)\quad\text{and}\quad I(P_N)=o(N^2)
 \quad\Longrightarrow\quad
 \frac{R_{\mathcal F}(P_N)}N\to0,\qquad
 \frac{D_{\mathcal F}(P_N)}N\to1.
 }
 \tag{2}
\]

This is a deterministic, pathwise implication. Consequently it applies
almost surely when its two premises hold almost surely under the same
probability measure.

The criterion requires only \(O(\sqrt N)\), not \(o(\sqrt N)\), once
the incomparable-count premise is added. It closes the previously
unsettled height-only boundary for the fixed factorial-power law \(q=1\).
Together with the already accepted height-only result for every fixed
integer \(q\ge2\), unrestricted Ferrers deletion fraction is therefore
one almost surely for **every separately fixed integer \(q\ge1\)** in
that family.

The two-premise result does not contradict the earlier conclusion that
height alone is inconclusive at \(q=1\). Nor is it a universal theorem
about all admitted laws or a physical geometry result.

## 2. Exact target, restrictions and accepted finite input

A nonempty Ferrers cell diagram is specified by a partition
\(\lambda_1=w\ge\cdots\ge\lambda_r\ge1\), with cells

\[
 Q_\lambda=\{(i,j):1\le i\le r,\ 1\le j\le\lambda_i\},
\]

ordered coordinatewise:

\[
 (i,j)\preceq(i',j')
 \quad\Longleftrightarrow\quad i\le i'\ \text{and}\ j\le j'.
 \tag{3}
\]

Membership in \(\mathcal F\) means isomorphism to some such diagram,
or empty. No occupancy/aspect condition or unique representation is
assumed for \(\mathcal F\). It is this filled partition cell-order class,
not every use of “Ferrers,” arbitrary subsets of the plane, or all
dimension-two posets.

The first column and first row of a diagram are chains, so for each
qualifying representation, with \(k=|Q|\),

\[
 r,w\le H(Q),\qquad k\le rw.
 \tag{4}
\]

These inequalities also follow from the accepted exact formula
\(H(Q_\lambda)=\max_i(i+\lambda_i-1)\), but the elementary row/column
argument is sufficient here.

The restriction \(P[W]\) in (1) retains the relations of the completed
parent order. Thus

\[
 H(P[W])\le H(P),\qquad I(P[W])\le I(P).
 \tag{5}
\]

Every chain remains a chain and every retained incomparable pair was
already incomparable in \(P\). Deleting generating-DAG vertices and then
recomputing reachability is a different operation, not the target distance.

For fixed real parameters \(0<\nu\le1,\ 1\le A<\infty\), the existing
dense target \(\mathcal T_{\nu,A}\) consists of empty and Ferrers orders
having a representation satisfying

\[
 k\ge\nu rw,\qquad A^{-1}\le r/w\le A.
 \tag{6}
\]

The accepted DENSE_FERRERS_INCOMPARABILITY_SCREEN.md supplies the
deterministic finite theorem

\[
 I(Q)\ge\frac{\nu^4}{128}\binom{|Q|}{2}
 \quad\text{if }Q\in\mathcal T_{\nu,A}
 \text{ and }|Q|\ge m_0(\nu,A):=
 \left\lceil\frac{16A}{\nu^2}\right\rceil.
 \tag{7}
\]

It applies to every qualifying representation, not just rectangles.
Here \(\nu\) means diagram occupancy, not event availability.
The proof below uses exactly (7), with parameters fixed before varying
size or selecting a subsequence. It does not change the target definition
or assume a stochastic uniformity theorem over targets.

Empty has \(H=I=R_{\mathcal F}=D_{\mathcal F}=0\). At empty define normalized
retained and deletion fractions to be zero. A singleton has
\(H=R_{\mathcal F}=1,\ I=D_{\mathcal F}=0\). For nonempty parents the
normalized retained/deletion fractions sum to one, and for sizes at least
two the incomparable fraction is \(I(P)/\binom{|P|}{2}\); set the latter
to zero at sizes zero and one.

## 3. Fixed-parameter reduction of a macroscopic retained diagram

Fix constants

\[
 C>0,\qquad 0<\varepsilon\le\min\{1,C^2\}.
 \tag{8}
\]

They are independent of \(N\), the parent order and the retained set.
Set

\[
 \boxed{\nu=\frac{\varepsilon}{C^2},\qquad
 A=\frac{C^2}{\varepsilon}.}
 \tag{9}
\]

These are valid fixed target parameters: \(0<\nu\le1,\ A\ge1\),
and \(A^{-1}=\nu\).

Suppose \(P\) has \(N\ge1\) vertices and

\[
 H(P)\le C\sqrt N,\qquad R_{\mathcal F}(P)\ge\varepsilon N.
 \tag{10}
\]

Choose a maximizing retained set, which exists because \(P\) is finite,
and let \(Q=P[W]\), \(k=|W|\ge\varepsilon N\).
It is nonempty. Take **any** qualifying partition representation of \(Q\)
with \(r\) rows and width \(w\). By (4)–(5),

\[
 r,w\le C\sqrt N,\qquad rw\le C^2N.
 \tag{11}
\]

Since \(k\le rw\), the upper bound on each dimension also gives a lower
bound on the other:

\[
 r\ge\frac{k}{w}\ge\frac{\varepsilon\sqrt N}{C},\qquad
 w\ge\frac{k}{r}\ge\frac{\varepsilon\sqrt N}{C}.
 \tag{12}
\]

Therefore

\[
 \frac{k}{rw}\ge\frac{\varepsilon}{C^2}=\nu,\qquad
 \frac{\varepsilon}{C^2}\le\frac rw
 \le\frac{C^2}{\varepsilon}=A.
 \tag{13}
\]

Thus \(Q\in\mathcal T_{\nu,A}\) for the same fixed parameters in (9).
All its qualifying representations obey these bounds. No representation
needs to remain the same across parent sizes, retained sets or subsequences.

The logical point is not that all unrestricted Ferrers diagrams have
uniform positive occupancy and bounded aspect. It is that a retained
diagram occupying at least a **fixed fraction** of a parent whose height
has a **fixed square-root bound** must have them. These two parent-relative
premises provide the constants.

### Infeasible and small parameter cases

If \(\varepsilon>1\), the retained-size premise is impossible since
\(R_{\mathcal F}(P)\le N\). If \(\varepsilon>C^2\), it is also impossible
under the height premise: (11) and \(k\le rw\) imply
\(k\le C^2N<\varepsilon N\). No invalid parameter \(\nu>1\) is then fed
into (7).

For \(N\ge1\), \(H(P)\ge1\), so \(C=0\) makes the height premise impossible.
Nonpositive \(\varepsilon\) is not a macroscopic retained-fraction test
and is outside (8). \(N=0\) is handled by the empty conventions, without
division by \(N\) or \(\sqrt N\).

For any small positive \(N\), the reduction (11)–(13) is still valid
whenever (10) is feasible, but the large-size density bound (7) cannot be
used until its explicit size threshold is reached.

## 4. Explicit finite conditional inequality and contrapositive

With the fixed constants (8)–(9), define

\[
 \boxed{
 m_0=\left\lceil\frac{16C^6}{\varepsilon^3}\right\rceil,\qquad
 N_0=\left\lceil\frac{m_0}{\varepsilon}\right\rceil,\qquad
 \delta=\frac{\varepsilon^6}{512C^8}>0.
 }
 \tag{14}
\]

The first expression is exactly
\(\lceil16A/\nu^2\rceil\), not a new target threshold.
Because \(C^2/\varepsilon\ge1\), \(m_0\ge16\).
For every integer \(N\ge N_0\), \(\varepsilon N\ge m_0\).

Under (10), \(k\ge K_N:=\lceil\varepsilon N\rceil\ge m_0\ge2\).
Equations (5), (7) and (13) imply

\[
 \boxed{
 I(P)\ge
 \frac{\varepsilon^4}{128C^8}
 \binom{\lceil\varepsilon N\rceil}{2}
 \ge\frac{\varepsilon^6}{512C^8}N^2
 =\delta N^2.
 }
 \tag{15}
\]

For the last inequality, if an integer \(K\ge2\) then
\(\binom K2=K(K-1)/2\ge K^2/4\), and \(K_N\ge\varepsilon N\).
Every ceiling and threshold is explicit. The pair count is a deterministic
count of unordered distinct pairs, not an expected value.

Equivalently, for the same fixed constants and every \(N\ge N_0\),

\[
 \left.
 \begin{gathered}
 H(P)\le C\sqrt N,\\
 I(P)<
 \dfrac{\varepsilon^4}{128C^8}
       \binom{\lceil\varepsilon N\rceil}{2}
 \end{gathered}
 \right\}
 \quad\Longrightarrow\quad
 \boxed{R_{\mathcal F}(P)\le\lceil\varepsilon N\rceil-1
 <\varepsilon N.}
 \tag{16}
\]

The simpler sufficient condition \(I(P)<\delta N^2\) also gives (16).
Strictness matters: equality in either lower bound does not give this
contrapositive. Since \(R_{\mathcal F}\) is an integer, ruling out
\(R_{\mathcal F}\ge\varepsilon N\) is exactly the ceiling-minus-one
conclusion. It also yields the finite deletion lower bound
\(D_{\mathcal F}(P)\ge N-\lceil\varepsilon N\rceil+1\).

For \(N<N_0\), no positive pair-density assertion is claimed by (15);
trivial cardinality bounds and the already accepted height-retention
bound remain available. The constants are conservative sufficient
constants, not sharp or optimized. In particular no numerical threshold
or tail evaluation is performed.

## 5. Pathwise joint theorem

Let \((P_N)\) be any sequence of finite posets with \(|P_N|=N\).
Assume \(H_N=O(\sqrt N)\) and \(I(P_N)=o(N^2)\).
The first hypothesis means there are fixed finite \(C_0>0\) and an
initial size after which \(H_N\le C_0\sqrt N\).
Enlarge the constant to \(C=\max\{1,C_0\}\); then every fixed
\(0<\varepsilon\le1\) satisfies (8).

For a chosen \(\varepsilon\), fix \(\nu,A,m_0,N_0,\delta\) by
(9) and (14). Since \(I(P_N)/N^2\to0\) and \(\delta>0\) is fixed,
eventually \(I(P_N)<\delta N^2\). At all sufficiently large sizes the
height bound and \(N\ge N_0\) also hold. Equation (16) gives
\(R_{\mathcal F}(P_N)/N<\varepsilon\) eventually.
Taking, for example, the countable sequence \(\varepsilon=1/j\),
\(j\ge1\), proves (2).

Equivalently, a nonzero retained-fraction limsup would supply some fixed
\(\varepsilon>0\) and an unbounded subsequence with
\(R_{\mathcal F}(P_N)\ge\varepsilon N\).
The same constants \(C,\nu,A,m_0,N_0,\delta\) would apply throughout that
subsequence. Equation (15) would force
\(I(P_N)/N^2\ge\delta\) there, contradicting the second hypothesis.

Neither version replaces \(\varepsilon\), \(C\), \(\nu\) or \(A\) by
size-dependent values. The representation may vary, but the target
parameters do not. The parents need not form a consistent growth process:
only the completed-order restriction statements at each size are used.
There is no pair-event, path or sampling independence assumption.

### Almost-sure form without an uncountable intersection

Suppose under one probability measure the events
\(H_N=O(\sqrt N)\) and \(I(P_N)=o(N^2)\) each have probability one.
Their intersection has probability one. On each outcome in that
intersection, choose its finite eventual height constant and apply the
deterministic theorem just proved.

Even if that constant is outcome-dependent, it is fixed along that
outcome's sequence before taking the asymptotic limit. The finite theorem
is a universal deterministic inequality for admissible constants, not a
family of stochastic assertions requiring an uncountable probability-one
intersection. No simultaneous stochastic target theorem is assumed.

The conclusion is almost-sure \(R_{\mathcal F}/N\to0\) and
\(D_{\mathcal F}/N\to1\), not an asserted polynomial rate of convergence.
Without a rate in the incomparable-count premise, no new power-law
retention rate is supplied by this proof.

## 6. Application to the fixed \(q=1\) law

The accepted factorial-power family uses, for each separately fixed
integer \(q\ge1\), per-subset weight \((k!)^{-q}\), independent birth
subsets, downward-closure past, independent fair immutable marks and
the declared passive PSD payload, under its own from-empty measure.

At \(q=1\), the supplied accepted statements are

\[
 \limsup_N\frac{H_N}{\sqrt N}\le2\mathrm e
 \quad\text{almost surely},\qquad
 \frac{I(P_N)}{\binom N2}\to0
 \quad\text{almost surely}.
 \tag{17}
\]

These hold under the same fixed-\(q=1\) measure.
Use the fixed deterministic slack constant

\[
 C=2\mathrm e+1.
 \tag{18}
\]

The height event in (17) implies \(H_N\le C\sqrt N\) eventually.
This does not assert eventual \(H_N\le2\mathrm e\sqrt N\) at the exact
limsup constant.

For \(N\ge2\),

\[
 \frac{I(P_N)}{N^2}
 =\frac{I(P_N)}{\binom N2}\frac{N-1}{2N}\to0
\]

on the incomparable-fraction event. Intersecting these two probability-one
events and applying section 5 proves

\[
 \boxed{
 \frac{R_{\mathcal F}(P_N)}N\to0,\qquad
 \frac{D_{\mathcal F}(P_N)}N\to1
 \quad\text{almost surely for fixed }q=1.
 }
 \tag{19}
\]

For each fixed retained-fraction test \(0<\varepsilon\le1\), the finite
bound can be made explicit by substituting (18) into (14)–(16).
All target parameters and thresholds are then deterministic and fixed
for that test. No numerical evaluation or improved stochastic constant
is needed.

This supplies the previously missing **joint-premise** unrestricted
Ferrers obstruction. It does not claim a matching height lower bound,
an actual height exponent, a rate for (19), or a successful approximation.

## 7. What is now established for the family

The accepted height-retention predecessor already proves, for each
fixed integer \(q\ge2\),

\[
 R_{\mathcal F}(P_N)=O(N^{2/(q+1)}),\qquad
 R_{\mathcal F}(P_N)/N\to0,\qquad
 D_{\mathcal F}(P_N)/N\to1
 \quad\text{almost surely}.
 \tag{20}
\]

Its premise is the accepted upper height exponent
\(1/(q+1)<1/2\), together with the deterministic Ferrers capacity
\(|Q|\le H(Q)(H(Q)+1)/2\). That height-only proof remains unchanged.

Combining (19) with (20) closes unrestricted Ferrers deletion for every
separately fixed integer \(q\ge1\) in the accepted family:

\[
 \boxed{
 \text{For each fixed integer }q\ge1,\qquad
 D_{\mathcal F}(P_N)/N\to1
 \quad\text{almost surely under that law}.}
 \tag{21}
\]

There is no simultaneous-law probability claim without a declared
coupling, no uniform result for growing or history-dependent \(q\), and
no universality over all admitted kernels. The laws themselves and their
admissibility are not changed.

For the original fixed occupancy/aspect target
\(\mathcal T_{\nu,A}\subseteq\mathcal F\),

\[
 R_{\nu,A}(P)\le R_{\mathcal F}(P),\qquad
 D_{\nu,A}(P)\ge D_{\mathcal F}(P).
 \tag{22}
\]

Thus (21) also implies its deletion fraction tends to one, consistently
with the already accepted restricted-target result. The new proof is
not the invalid reverse inference from failure of one restricted target
to failure of its unrestricted superclass. Its added argument is the
fixed-parameter reduction (11)–(13): any macroscopic retained unrestricted
diagram, under a fixed square-root height bound, would necessarily
belong to one of the fixed dense classes used in the contradiction.

The values \(\nu=\varepsilon/C^2\) and \(A=C^2/\varepsilon\) are proof
parameters forced by a hypothetical macroscopic retained fraction.
They do not replace or redesign any previously fixed target parameters.

## 8. Why the height-only boundary and other scopes remain correct

The predecessor's sharp height-only ceiling is

\[
 R_{\mathcal F}(P)\le
 \min\{|P|,H(P)(H(P)+1)/2\}.
 \tag{23}
\]

At \(q=1\), substituting the accepted \(O(\sqrt N)\) height bound into
(23) gives only an order-\(N\) ceiling, and with the cardinality cap its
limsup bound is trivial. That calculation is still inconclusive by itself.
The new conclusion uses the additional \(I(P_N)=o(N^2)\) premise through
(7) and (15); it does not reinterpret (23) as a stronger result.

Accordingly \(O(\sqrt N)\), rather than little-\(o\), is sufficient
**with** the incomparable-count premise. Neither premise is discarded,
nor is sublinear height alone declared sufficient for approximation.
The unrestricted class still contains long chains with zero incomparable
pairs, so it still has no universal positive pair-density floor without
the macroscopic-retention and height restrictions used here.

The accepted quadratic-penalty law's unrestricted obstruction remains the
separate height-only result already recorded in the predecessor. Its
positive incomparable-fraction liminf does not satisfy the vanishing
density premise of (2), so that premise is not transferred to it.
Nothing here changes the established law dependence of incomparable
behavior.

The theorem concerns a mathematical target class of filled coordinatewise
cell orders. It does not classify all manifoldlike or Lorentzian orders,
all dimension-two orders, other meanings of Ferrers, or successful
physical geometry. No metric, manifold, gravity/mass law, physical
prediction, physical discriminator or application benchmark follows.
The accepted processes retain their fair marks and passive quantum
payloads; this order-projection diagnostic neither derives full QM nor
identifies committed records with all live relational activity.

## 9. Dependencies, evidence and stop boundary

The new work is the fixed-parameter reduction, finite conditional
inequality and contrapositive, pathwise/almost-sure joint theorem, and
the exact fixed-law consequences. The accepted dense-target theorem
(7), factorial-law stochastic premises (17), and prior height-only
results are used at their stated scopes rather than re-proved or
numerically evaluated.

The six literal sources have these roles:

- FERRERS_HEIGHT_RETENTION_OBSTRUCTION.md supplies the exactly accepted
  height-capacity theorem, completed-order retention convention, prior
  \(q\ge2\) result and correctly limited height-only \(q=1\) boundary.
- FACTORIAL_POWER_LAW_FAMILY.md supplies both accepted stochastic premises
  for the same fixed-\(q\) measures and their fixed-integer quantifiers.
- DENSE_FERRERS_INCOMPARABILITY_SCREEN.md supplies the finite density
  floor and explicit size threshold in (7).
- INTRINSIC_GEOMETRY_TARGET_SCREEN.md supplies the existing coordinatewise
  cell target, fixed occupancy/aspect conventions and induced objective.
- THEOREM_PACKAGE.md supplies the declared marked-order/passive-payload
  setting and scope of the accepted constructions.
- LAW_DEPENDENCE.md supplies the distinction between optional laws and
  unsupported universal or physical conclusions.

The source manuscript was constructed from only those six permitted literal
copies and two literal provenance records. These public links provide reader
equivalents for the six scientific roles; they do not reconstruct original
native custody or replace the retained private source evidence.

| Public reader reference | Scientific source role |
| --- | --- |
| [Ferrers height and retention obstruction](FERRERS_HEIGHT_RETENTION_OBSTRUCTION.md) | Accepted height-capacity theorem, completed-order retention convention, prior higher-integer-exponent result and correctly limited height-only boundary. |
| [Factorial-power law family](FACTORIAL_POWER_LAW_FAMILY.md) | Both accepted stochastic premises under the same fixed-exponent measures and their fixed-integer quantifiers. |
| [Dense Ferrers incomparability screen](DENSE_FERRERS_INCOMPARABILITY_SCREEN.md) | Finite density floor and explicit size threshold. |
| [Intrinsic geometry target screen](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) | Existing coordinatewise cell target, fixed occupancy/aspect conventions and induced objective. |
| [Theorem package](THEOREM_PACKAGE.md) | Declared marked-order/passive-payload setting and scope of the accepted constructions. |
| [Law dependence](LAW_DEPENDENCE.md) | Optional law choices and limits on universal or physical conclusions. |

At source construction, the height-retention manuscript was an accepted
native predecessor and the other five scientific inputs were public snapshots.
The predecessor retained its historical pending header; a later exact
subject-joined adjudication recorded acceptance of that input, not this
manuscript. Supplied metadata attributed the five public snapshots to a
historical publication state, without fresh Git or network verification.

The following paragraphs preserve the source manuscript’s account of its
source consumption and manual work. Its current complete captures,
historical display recovery, custody failures and readback categories are
distinct from this derivative’s administrative checks and later review.

All six native source captures are complete. Four fresh bodies exactly
match already consumed complete bodies; package/law additions after
exact prefix joins were displayed and consumed. Both literal JSON
records were fully displayed and consumed. There was no new truncated
source display in this sitting. The predecessor retains its earlier
combined-display truncation and complete recovery, as well as older
administrative parse/custody limitations. Current joins do not erase,
reconstruct or recertify those historical events.

Two manual workers checked supplied context without source/file access:
one checked the finite reduction, constants, integer thresholds and
contrapositives; the other checked the pathwise/almost-sure argument and
fixed-law scope, using the separately checked finite lemma.
Their full worker-reported supported usage observations are separate
from root-direct captures. Mathematical reports are summaries, not
verbatim transcripts, source audits or native acceptance.

All new reasoning is manual symbolic proof. There is no mathematical
executor, numerical probability/tail/interval evaluation, sampling,
simulation, optimizer, benchmark, experiment, dataset/network acquisition,
protected validation, law scan or target redesign. Bounded inert text
assembly, exact readback/string comparisons and native hashes/byte
counts are administrative checks, not scientific execution.

Full native source/manuscript captures are distinguished from metadata-only
summaries of own-receipt readbacks. Separate observations are not atomic
original-custody proofs. Manual cross-checks are not proof-assistant
verification. Actual custody controls/failures, physical/application
separation and the RET-only pause remain unchanged.

The native manuscript and its three companion source-provenance, result
and freeze records remain private. Exact original pins, declared metadata
substitutions, source-tail correspondence and check receipts are retained
locally. Private identifiers, filesystem locations, fingerprints and tool
transcripts are withheld. No linked original source or archive, additional
manifest member, program, repository history or protected input was followed
in preparing this public derivative.

Manual mathematical construction is separate from independent native and
editorial review. This derivative is text preparation, not scientific
acceptance, machine proof or public executable custody. Native acceptance,
editorial acceptance, publication and subsequent assignments are recorded
separately by the coordinator; no later result is claimed here. Target and
protocol boundaries and the RET-only pause remain unchanged. See the
[publication note](PUBLICATION_NOTE.md) and
[redacted-publication policy](../../coordination/REDACTED_PUBLICATION.md).
