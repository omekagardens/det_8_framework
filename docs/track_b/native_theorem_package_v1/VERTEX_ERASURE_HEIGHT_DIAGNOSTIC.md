# Vertex-erasure transfer of the finite-height diagnostic

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: a declared bounded vertex-erasure channel, not physical acquisition,
arbitrary noisy orders, or application performance.

## 1. The transferred test

Before observation fix \(p_0\in(0,1)\), the true integer size \(N\ge2\),
and a nonnegative integer budget \(d\). Put

\[
 n=N-1,\quad k=\lceil p_0n/2\rceil,\quad
 0\le d\le\lfloor p_0n/4\rfloor,\quad \ell=k-d.
 \tag{1}
\]

Keep the accepted law classes: each separately fixed Bernoulli-subset law
with \(p\in[p_0,1)\), and each separately fixed factorial-power subset law
with integer \(q\ge1\), each started from empty under its own measure.
There is no prior, joint coupling, adaptive parameter selection, or
data-dependent stopping size.

The channel erases at most \(d\) vertices from the generated completed
order \(P_N\) and supplies exactly the completed induced order \(Q\)
on every survivor, together with its observed cardinality \(m\) and the
known true \(N\). All surviving comparisons must be faithful.
Define \(h=H(Q)\), where height counts chain vertices. Decide

\[
 \boxed{\delta(Q;N,p_0,d)=
 \begin{cases}
 \mathrm B,&h\ge\ell+1=k-d+1,\\
 \mathrm F,&h<\ell+1.
 \end{cases}}
 \tag{2}
\]

For every allowed channel \(K\), the joint law/channel errors obey

\[
 \boxed{\Pr_{p,K}(\delta=\mathrm F)
 \le \min\{1,1/(np_0^2)\}
 \quad\text{for every fixed }p\in[p_0,1),}
 \tag{3}
\]

\[
 \boxed{\Pr_{q,K}(\delta=\mathrm B)
 \le \min\left\{1,\frac{N(2\sqrt n)^\ell}{\ell!}\right\}
 \le \min\left\{1,N\left(\frac{2\mathrm e\sqrt n}{\ell}\right)^\ell\right\}
 \quad\text{for every fixed integer }q\ge1.}
 \tag{4}
\]

These are class-conditional frequentist bounds, uniform over the allowed
channels and separately fixed laws. They are not posterior probabilities.
The proof does not assume erasure independence or treat the survivors as
a fresh \(m\)-vertex draw from either original law.

## 2. Channel and probability conventions

For a finite generated history \(\omega\), write \(P_N(\omega)\) on
vertex set \(V\). A channel is a measurable probability kernel
\(K(\omega,A)\) on erased subsets \(A\subseteq V\), supported on
\(|A|\le d\). The output is an arbitrary relabeling of
\(Q=P_N[V\setminus A]\), with \(m=N-|A|\).
A deterministic, data-dependent adversarial deletion is a point-mass
kernel; random deletions are also allowed. The choice can depend on the
whole realized finite history. All relevant finite sets have their
discrete sigma-fields; any additional channel randomization is included
in the joint probability model.

The joint probability is obtained by integrating the channel conditional
on the generated history. Its history marginal remains the stated
Bernoulli or factorial law. No independence between \(A\) and \(\omega\)
is imposed. Equivalently, the proof works for any joint distribution
with that history marginal and the prescribed deletion/output support.
An adversary is allowed to select an admissible kernel, not to change
the generative marginal or condition the reported experiment on a
favorable selected subset of histories.

The output must include every survivor and every true comparison among
survivors. It contains no inserted vertices, altered comparisons,
unknown comparisons, or incorrect true size. The restriction is of the
**completed order**, not deletion from a generating DAG followed by
recomputed reachability. For example, if an old comparison was witnessed
by a path through an erased vertex, that comparison remains in the
completed restriction.

A sufficient input representation is an \(m\)-by-\(m\) Boolean matrix
\(M_{uv}=1\) exactly when survivor \(u\prec v\), plus \(m,N\).
Matrix indices are arbitrary names, not birth labels. The rule needs no
latent edges, deleted-vertex identities, marks, payload, or supplied
parent embedding. Height and the decision are isomorphism invariant.

The bounds (3)–(4) refer to the unconditional joint law at fixed \(N\).
They are not asserted conditional on the realized \(m\), an erasure
pattern, or a decision: data-dependent erasures can make such conditioning
selective. No observations are discarded and no abstention is used in (2).

## 3. Deterministic height inequality and finite endpoints

For any finite order \(P\) of size \(N\), any erased set \(A\) of actual
size \(a\), and \(Q=P[V\setminus A]\), choose a longest chain in \(P\).
At most \(a\) members are removed. Its remaining members are still a
chain because all their original comparisons are retained. Conversely,
every chain in \(Q\) is a chain in \(P\). Hence

\[
 \boxed{\max\{0,H(P)-a\}\le H(Q)\le\min\{H(P),N-a\}.}
 \tag{5}
\]

In particular, if \(a\le d\),

\[
                    H(P)-d\le H(Q)\le H(P).
 \tag{6}
\]

The lower endpoint in (5) is clipped at zero rather than asserting a
negative height. If \(a=0\), \(Q=P\) and the height is unchanged.
If \(a=N\), \(Q\) is empty and its height is zero.
For empty \(P\), all heights and \(a\) are zero. A singleton has height
one if retained and zero if erased. A chain shows that deleting \(a\)
vertices can lower height by exactly \(a\); deleting unrelated vertices
can leave a longest chain unchanged. No equality for every parent or
erasure pattern is asserted.

These statements are deterministic and hold simultaneously for every
erasure set. They require neither an erasure distribution nor knowledge
of how the set was chosen.

For the test's restricted design (1), \(n\ge1\) gives \(1\le k\le n\).
Moreover,

\[
 \ell=k-d\ge p_0n/2-p_0n/4=p_0n/4>0,
 \qquad 1\le\ell\le k\le n.
 \tag{7}
\]

The first inequality uses \(d\le\lfloor p_0n/4\rfloor\le p_0n/4\);
integrality then gives \(\ell\ge1\). Because \(d<N-1\), \(m\ge N-d\ge2\).
Also

\[
                        2\le\ell+1\le N-d\le m.
 \tag{8}
\]

Thus the test threshold is nondegenerate and never exceeds the minimum
possible observed size. The general empty-output endpoints above are
not silently included in this restricted test.

## 4. Error transfer by pointwise event inclusions

Write \(H=H(P_N)\). From (6), the Bernoulli error event satisfies

\[
 \{h<k-d+1\}\subseteq\{H<k+1\}.
 \tag{9}
\]

Indeed \(H-d\le h<k-d+1\) implies \(H<k+1\). The factorial error event
satisfies

\[
                 \{h\ge\ell+1\}\subseteq\{H\ge\ell+1\}
 \tag{10}
\]

because \(h\le H\). Each inclusion holds for every generated history
and every allowed deletion. Integrating its indicator against any
allowed kernel \(K\) bounds the joint error by the corresponding
original-law probability on the right. This is why adversarial,
data-dependent and random erasures require no independence assumption.

### Bernoulli side

The accepted finite adaptive-tip argument supplies, on each Bernoulli
law's own measure,

\[
             H\ge 1+B_n,\qquad B_n\sim\operatorname{Binomial}(n,p).
\]

This witness uses latent selections only in the proof; it is not
required by the observation rule. If \(H<k+1\), then the integer \(B_n\)
obeys

\[
                  B_n\le k-1<p_0n/2.
\]

The strict ceiling identity \(\lceil x\rceil-1<x\) remains valid even
when \(x\) is an integer. Therefore, for \(p\ge p_0\),

\[
 np-B_n>np-p_0n/2\ge np_0/2.
\]

Using \(\operatorname{Var}(B_n)=np(1-p)\le n/4\), Chebyshev gives

\[
 \Pr_p(H<k+1)
 \le\Pr_p(|B_n-np|>np_0/2)
 \le\frac{n/4}{(np_0/2)^2}=\frac1{np_0^2}.
 \tag{11}
\]

Combine (9) with (11) and clip at one to obtain (3).
Lowering the threshold by the full budget prevents a new Bernoulli
error outside the original error event; it does not assert that the
actual error probability is equal to that of the unerased test.

### Factorial side

For each separately fixed integer \(q\ge1\), the accepted per-subset
law has weights \((j!)^{-q}\), independent subset coordinates at distinct
births, and marginal selection probability

\[
               \rho_{r,q}\le r^{-q/(q+1)}\le r^{-1/2}
               \quad(r\ge1).
\]

Its order is the transitive closure of a forward birth-label DAG.
A completed chain with at least \(t+1\) vertices yields a directed
path with at least \(t\) edges: concatenate witness paths between
successive chain vertices. Their increasing-label intervals have
disjoint interiors. Truncate to exactly \(t\) edges if necessary.

For a specified increasing \(t\)-edge path, the required selections
have distinct birth heads and probability equal to the product of
their marginals. There is only one required inclusion in each birth
subset. No independence within a subset or between different paths is
used. Set \(A_{N,q}=\sum_{r=1}^n\rho_{r,q}\).
For each ordered set of \(t\) distinct heads, there are at most \(N\)
possible starting vertices. Expanding \(A_{N,q}^t\) counts each
distinct-head product \(t!\) times, with other terms nonnegative.
A path count and Markov's inequality therefore give, for integer
\(1\le t\le n\),

\[
 \Pr_q(H\ge t+1)\le
 \min\{1,N A_{N,q}^t/t!\},\qquad
 A_{N,q}\le\sum_{r=1}^n r^{-1/2}\le2\sqrt n.
 \tag{12}
\]

The last bound follows by integrating \(x^{-1/2}\) on each interval
\([r-1,r]\). The exact factorial bound
\(t!\ge(t/\mathrm e)^t\) follows from
\(\log(t!)\ge\int_1^t\log x\,dx\ge t\log t-t\), including \(t=1\).
Apply (12) with \(t=\ell\), valid by (7), and combine with (10).
This proves (4), not just an appeal to a threshold formula at a
different integer.

All probability bounds are for the original \(N\)-vertex law.
The surviving \(Q\) can be an adversarially selected induced order;
replacing \(N\) by \(m\) in these generative bounds is unjustified.

## 5. Sufficient size, rounding and limiting scope

For desired predeclared errors
\(\varepsilon_{\mathrm B},\varepsilon_{\mathrm F}\in(0,1)\), a
conservative sufficient design is integer \(n=N-1\) satisfying

\[
 \boxed{
 n\ge\left\lceil\max\left\{
 1,\ \frac{4d}{p_0},\
 \frac1{\varepsilon_{\mathrm B}p_0^2},\
 \left(\frac{16\mathrm e}{p_0}\right)^2,\
 \left(\frac8{p_0\log2}\right)^2,\
 \frac8{p_0\log2}\log\frac1{\varepsilon_{\mathrm F}}
 \right\}\right\rceil.}
 \tag{13}
\]

Here \(\log\) is natural. The \(4d/p_0\) entry ensures
\(d\le\lfloor p_0n/4\rfloor\), because \(d\) is an integer. It may be
omitted if that budget condition is imposed separately. All design
quantities are chosen before the observation; (13) is not an adaptive
size or threshold search.

The Bernoulli claim follows immediately from (3). By (7),

\[
 \frac{2\mathrm e\sqrt n}{\ell}
 \le\frac{8\mathrm e}{p_0\sqrt n}\le\frac12
 \quad\text{if } n\ge(16\mathrm e/p_0)^2.
\]

Then the factorial error is at most

\[
                    N2^{-\ell}\le(n+1)2^{-p_0n/4}.
 \tag{14}
\]

For \(n\ge1\), \(\log(n+1)\le\sqrt n\): the function
\(f(x)=\sqrt x-\log(x+1)\) has \(f(1)>0\) and
\(f'(x)=(\sqrt x-1)^2/[2\sqrt x(x+1)]\ge0\) for \(x\ge1\).
If \(n\ge[8/(p_0\log2)]^2\), this yields
\(\log(n+1)\le(p_0\log2)n/8\). Thus (14) is bounded by

\[
 \exp[-(p_0\log2)n/8]\le\varepsilon_{\mathrm F}
\]

using the final entry of (13). Ceilings and equalities at thresholds
are compatible with the claimed nonstrict error inequalities.

For fixed \(p_0>0\), these bounds tend to zero as \(N\) increases,
uniformly in the separately allowed budgets \(d\le\lfloor p_0n/4\rfloor\),
channels, and fixed candidate laws in the finite-bound sense. This
does not construct one adaptive-parameter growth law, assert simultaneous
correct decisions over many inspected sizes, or require a joint coupling
of all channels and laws.

At \(d=0\), no vertex is erased, \(\ell=k\), and the rule and both
finite bounds are exactly those of the accepted unerased theorem.
Condition (13) remains a conservative sufficient condition in this
case; the sharper unerased sufficient-size constants may instead be
used. There is no claim that the new conservative size constants are
minimal or equal to the old ones.

At \(N=2\), \(n=1\) forces \(d=0\), \(k=\ell=1\).
The rule is valid although the clipped upper bounds may be one.
Whenever a raw bound exceeds one, only its minimum with one is used.
Failure to meet (13), a trivial upper bound, or a budget outside (1)
does not establish failure of the test or impossibility for other
statistics/channels. No numerical probability, tail, size optimization
or performance evaluation is performed.

## 6. Sufficient input and computation costs

On the promised valid observed matrix, compute height by scanning for
indegrees, using Kahn's topological ordering, and propagating longest-chain
values along the strict relation. Initialize every vertex value to one;
when a predecessor \(u\) is processed, update each successor \(v\) by
\(\max\{h(v),h(u)+1\}\). All predecessors are processed before a value is
final. Every relation path is a chain and every chain can be traversed
via its successive relation entries, proving correctness even when
transitive comparisons are present.

With \(m\ge2\) in the test domain, sufficient costs are:

- \(m^2\) observed relation bits, plus encodings of true \(N\), observed
  \(m\), and the predeclared design parameters.
- \(O(m^2)\) relation inspections and integer operations for height;
  heights, indegrees and indices use \(O(\log m)\) bits.
- \(O(m^2\log m)\) bookkeeping bit work under indexed matrix access,
  and \(m^2+O(m\log m)\) bits for matrix plus workspace.
- Separate \(O(\log N)\)-bit threshold/budget/cardinality bookkeeping.
  If \(p_0=a/b\) is supplied with numerator and denominator of at most
  \(L\) bits, exact preparation of
  \(k=\lceil a(N-1)/(2b)\rceil\) and \(\ell=k-d\) has a sufficient
  grade-school bound \(O((L+\log N)^2)\) bit operations. Include
  \(O(L+\log N)\) bits for those design inputs/workspace.

For arbitrary real \(p_0\), the mathematical threshold is well-defined,
but computation assumes an exactly predeclared integer threshold or a
finite exact encoding such as that rational design. No unit-cost
exact-real oracle is assumed. Matrix access and integer bookkeeping
costs do not claim arbitrary sequential-tape or unbounded-name costs.

The matrix algorithm depends on observed \(m\); the design and probability
bounds depend on true \(N\). One may check \(N-d\le m\le N\) and the
matrix dimensions without knowing erased identities. Optional matrix
validity checks use \(O(m^3)\) relation inspections for transitivity,
with diagonal/asymmetry checks taking \(O(m^2)\).
These checks cannot establish that the reported matrix is the true
completed restriction: a wrong but valid order can pass them.

No generating-DAG reconstruction or Ferrers optimizer is required.
The costs are sufficient, not optimal, measured throughput, or an
application advantage. No algorithm was run here. Obtaining a reliable
true \(N\), establishing a valid erasure budget, acquiring every retained
comparison, and verifying physical fidelity remain unsupplied measurement
requirements, not costs paid by the matrix calculation.

## 7. Interpretation and remaining blockers

The result relaxes the exact-input premise only by a known-budget
vertex-erasure channel with faithful completed survivor relations.
It supplies no physical acquisition or preparation mechanism.

Unknown true size, unknown erasure budget, omitted comparisons, altered
retained relations, inserted or misidentified vertices, or a differently
selected generative marginal are outside the theorem. Observing \(m\)
alone does not reconstruct true \(N\) or license substituting \(m\)
into the original-law formulas. Closing a partial report does not
certify that it is the completed survivor order. No error transfer for
these other channels, and no general impossibility result for alternative
tests, has been supplied.

Bounds (3)–(4) concern errors conditional on the true candidate family,
not probabilities of truth conditional on a label or on the observed
matrix. They do not classify every law satisfying the broad admission
principles, supply a prior, or validate either optional law physically.
The test requires predeclared \(p_0>0\); it gives no parameter-free
uniform guarantee by allowing \(p_0\) to be chosen after inspection.

The quantum payload remains part of the original conditional model but
is passive and unused by the rule. No ontology, full-QM derivation,
metric, geometry emergence, mass/gravity law, clock or metric-as-record
promotion follows. No geometry target is redesigned. Records are not
declared to exhaust all present relational activity.

A future application would still need a fixed benchmark, relevant
baselines, preparation/readout and computation costs, specified failure
rates, held-out evaluation and an explicit practical objective. These
requirements and the physical preparation/readout blocker remain open.
No application performance, superiority or production readiness is claimed.

## 8. Sources, review and stop boundary

The permitted sources have these roles: FINITE_HEIGHT_LAW_SEPARATION.md
supplies the exactly accepted finite test and general path-tail premise;
BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md supplies its finite adaptive-tip
binomial witness; FACTORIAL_POWER_LAW_FAMILY.md supplies the selection
marginals and distinct-birth independence; INTRINSIC_GEOMETRY_TARGET_SCREEN.md
supplies the completed-order deletion convention and height inequality
context; THEOREM_PACKAGE.md and LAW_DEPENDENCE.md preserve the declared
model, optional-law and physical-scope distinctions. The error-transfer
inclusions and constants are proved above, not imported as accepted facts.

The source author inspected the actual schemas of the two supplied
provenance records and matched the source identities and adjudication
identity. The exact finite-height predecessor was accepted separately;
its historical pending header does not contradict that later acceptance.
This is acceptance of a source, not acceptance of the present theorem.
The public snapshot attribution was supplied metadata, without fresh
Git or network verification.

The public reader references below preserve the six scientific roles
above. They do not supply private provenance records or original atomic
custody.

| Scientific source role | Public reader reference |
| --- | --- |
| Finite diagnostic and general path-tail premise | [FINITE_HEIGHT_LAW_SEPARATION.md](FINITE_HEIGHT_LAW_SEPARATION.md) |
| Finite adaptive-tip binomial witness | [BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md](BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md) |
| Selection marginals and distinct-birth independence | [FACTORIAL_POWER_LAW_FAMILY.md](FACTORIAL_POWER_LAW_FAMILY.md) |
| Completed-order deletion convention and height context | [INTRINSIC_GEOMETRY_TARGET_SCREEN.md](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) |
| Declared marked-order and passive-payload model | [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) |
| Optional-law and physical-scope distinctions | [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) |

The following consumption and verification account describes the source
author's work; it does not claim a new display of every reused body during
publication preparation.

Only the six literal manuscripts and the two permitted literal JSON
records were read. No originals, linked archives, extra adjudication
members, programs or protected paths were followed. All eight current
native captures are complete. Three manuscript bodies exactly match
previously consumed complete stored bodies; package and law bodies
match consumed prefixes and their appended additions were displayed.
The changed public Bernoulli body was fully displayed in two bounded
contiguous slices after its exact-text comparison differed. Both JSON
bodies were fully consumed. No new truncated aggregate display occurred.

Exact text comparisons and native byte/hash checks are distinct
administrative observations, not atomic historical-custody certificates.
Earlier aggregate display failures and recovery, source-check/receipt
failures and custody limitations remain preserved. No omitted timestamp
is inferred. Full source captures, newly consumed text, reused consumed
text, metadata-only own-receipt readbacks, and worker-reported observations
are distinguished in the retained private source and verification records.

A bounded independent supplied-context manual review is recorded
separately; it is not a source audit, proof-assistant certificate or
native adjudication. All mathematical reasoning is manual.
There is no scientific/numerical executor, probability/tail/interval
evaluation, simulation, optimizer, dataset/network acquisition,
benchmark, experiment, protected validation or historical reconstruction.
Text assembly, exact readback comparisons, JSON parsing, native hash/byte
checks and final inventory are administrative only.

Manual source construction, the supplied-context worker review,
independent native review, editorial review and publication are distinct.
Acceptance and publication are recorded separately. This derivative
preparation does not adjudicate the theorem or recast a worker's
reported observations as direct source-identity verification.

The source manuscript and three private administrative records form the
author's frozen packet. Private record names, paths, identifiers,
fingerprints and tool receipts are withheld here; the exact transformation
and correspondence map are retained separately. This public derivative
does not provide machine proof, executable custody or reconstructed
historical custody. No physical readout or application execution follows.
Existing thresholds, frozen protocols and RET remain unchanged. See the
[publication note](PUBLICATION_NOTE.md) and
[redacted-publication policy](../../coordination/REDACTED_PUBLICATION.md).
