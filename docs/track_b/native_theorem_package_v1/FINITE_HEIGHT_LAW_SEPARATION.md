# Finite intrinsic-height separation of two optional law families

Status: manual theorem manuscript; independent review and publication are recorded separately.
Date: 2026-10-21.
Scope: one predeclared finite completed-order observation, fixed Bernoulli
and factorial-power law families, explicit class-conditional errors and
sufficient computational costs. No physical readout or application claim.

## 1. Finite diagnostic theorem

Before observing an order, fix a real lower bound \(p_0\in(0,1)\) and
an integer \(N\ge2\). Define

\[
 n=N-1,\qquad k=\left\lceil\frac{p_0n}{2}\right\rceil.
 \tag{1}
\]

The two candidate classes are:

- \(\mathrm B(p_0)\): each separately fixed Bernoulli-subset law with
  \(p_0\le p<1\), started from empty.
- \(\mathrm F\): each separately fixed factorial-power subset law with
  integer exponent \(q\ge1\), started from empty.

The input is **exactly one fully and faithfully supplied, completed,
unmarked finite order \(P_N\) of known size \(N\)**. Section 2 specifies
a sufficient finite representation. Let \(H(P_N)\) be the maximum
cardinality of a chain. Use the deterministic rule

\[
 \boxed{
 \delta_{N,p_0}(P_N)=
 \begin{cases}
 \mathrm B,&H(P_N)\ge k+1,\\
 \mathrm F,&H(P_N)<k+1.
 \end{cases}}
 \tag{2}
\]

For every fixed \(p\in[p_0,1)\), under that Bernoulli law,

\[
 \boxed{
 \Pr_p(\delta_{N,p_0}=\mathrm F)
 \le b_{\mathrm B}(N,p_0):=
 \min\left\{1,\frac1{np_0^2}\right\}.}
 \tag{3}
\]

For every fixed integer \(q\ge1\), under that factorial-power law,

\[
 \boxed{
 \Pr_q(\delta_{N,p_0}=\mathrm B)
 \le b_{\mathrm F}(N,p_0):=
 \min\left\{1,\frac{N(2\sqrt n)^k}{k!}\right\}
 \le
 \min\left\{1,N\left(\frac{2\mathrm e\sqrt n}{k}\right)^k\right\}.}
 \tag{4}
\]

The two displayed upper bounds tend to zero as \(N\to\infty\) for
each fixed predeclared \(p_0>0\). Section 6 gives an explicit symbolic
sufficient size for any predeclared errors
\(\varepsilon_{\mathrm B},\varepsilon_{\mathrm F}\in(0,1)\).

These are finite, frequentist, class-conditional error bounds, uniform
in the stated parameter ranges in the sense of separate inequalities
under each law. They do not assume a coupling of the candidate laws,
a prior on their classes, or a parameter chosen after seeing the order.
They do not give posterior probabilities that an observed classification
is true. The rule is not a classifier for every admitted growth law.

## 2. Observation contract and predeclaration

A sufficient representation is an \(N\)-by-\(N\) Boolean matrix \(M\)
with an arbitrary indexing of the observed vertices:

\[
                  M_{uv}=1\quad\Longleftrightarrow\quad u\prec v.
 \tag{5}
\]

This is the **complete strict order relation**, including transitive
comparisons, not just selected generating edges. It is assumed to be
irreflexive and transitive, hence acyclic and asymmetric. The indexing
is an arbitrary naming convention and need not be a natural birth
ordering. The known cardinality \(N\), matrix dimensions and entries
are supplied consistently. No external vertex-name encoding is needed
beyond this indexing.

Thus the decision requires no birth labels, hidden generating subsets,
marks, PSD entries, metric coordinates or parent embedding. The use of
latent birth coordinates in the proofs below is a probability-space
construction, not extra data required by (2). An isomorphism carries
chains to chains, so \(H\), the threshold decision, and both error events
are invariant under vertex relabeling.

The observation channel here is the exact projection of the candidate's
finite history to its completed unmarked order. This is a declared
mathematical input, not a construction of a physical preparation/readout
map. A single \(N\)-vertex order is not \(N\) independently prepared
experiments; its vertices and relations can be dependent.

The following are fixed before the observed matrix is inspected:

1. The lower bound \(p_0\), the size \(N\), and the two candidate classes.
2. The threshold \(k\) in (1) and the rule (2).
3. Any requested error tolerances and sufficient-size design using section 6.

There is no data-dependent choice of \(p_0\), threshold optimization,
parameter fitting, optional stopping in \(N\), or history-dependent
\(p\) or \(q\). The theorem is not a guarantee for those other procedures.

For arbitrary mathematical real \(p_0\), (1) defines an exact integer
but does not itself supply a finite encoding or algorithm for that real.
The computational claim assumes that \(k\) has been predeclared exactly,
or, as a sufficient finite design, that \(p_0=a/b\) is supplied as positive
integers \(0<a<b\). Then

\[
                 k=\left\lceil\frac{a(N-1)}{2b}\right\rceil
 \tag{6}
\]

is obtained by exact integer arithmetic before receiving the order.
No unit-cost exact-real oracle is assumed. The size conditions in
section 6 are mathematical sufficient conditions, not numerical
probability evaluations performed here.

## 3. Accepted law inputs and the finite premises actually used

The accepted Bernoulli law has independent elementary selections
\(E_{ij}\sim\operatorname{Bernoulli}(p)\) for every \(i<j\).
At birth \(j\), the strict past is the downward closure of the selected
old vertices. The newborn bit is independently fair, and the arbitrary
fixed-carrier complex PSD payload is scalar-passive. Its individual
ideal probability, for parent size \(m\), ideal size \(s\), and induced
maximum count \(a\), is \(p^a(1-p)^{m-s}\).

The accepted adaptive-tip proof starts a chain at vertex 1, and appends
each new vertex exactly when it selects the current tip. Conditional
on the entire past, that increment has probability \(p\); iteration
proves iid Bernoulli increments. In particular, at **each finite size**,

\[
 H(P_N)\ge L_N=1+B_n,\qquad
 B_n\sim\operatorname{Binomial}(n,p),\quad n=N-1.
 \tag{7}
\]

This is a pathwise witness on that law's own from-empty measure, not
a stochastic comparison obtained by coupling it to another law.
The finite binomial statement, rather than merely the almost-sure
limiting chain fraction, is the premise needed here.

The factorial-power family draws independent subset coordinates at
different births, with

\[
 \Pr_q(U_m=U)=
 \frac1{(|U|!)^q Z_{m,q}},\qquad
 Z_{m,q}=\sum_{j=0}^m\frac{\binom mj}{(j!)^q},
 \quad U\subseteq[m],\quad q\in\{1,2,\ldots\}.
 \tag{8}
\]

The strict past is again the downward closure, with independent fair
bits and the same declared scalar-passive payload convention.
For any specified old vertex the accepted finite marginal bound is

\[
 \rho_{m,q}:=\Pr_q(i\in U_m)
       \le m^{-q/(q+1)}\quad(m\ge1).
 \tag{9}
\]

Inclusions **within one subset** need not be independent. Distinct
birth coordinates are independent, which is all that the path proof
in section 5 requires. No branch-probability or tail evaluation,
simulation, or scientific executor is used here.

Both classes are optional admitted laws. Their positivity, mark
locality, complete marked diamonds and full PSD maps, including zero
payload, are supplied accepted premises. These observation-error
calculations do not rederive full QM, select a law from DET primitives,
or identify record count with physical time.

## 4. Bernoulli-class error and exact integer handling

Because \(0<p_0<1\) and \(n\ge1\),

\[
                        1\le k\le n.
 \tag{10}
\]

Indeed \(p_0n/2>0\) and is less than \(n\), whose integrality gives
\(\lceil p_0n/2\rceil\le n\). The threshold \(k+1\) is therefore between
2 and \(N\); no division by \(k=0\) will occur.

Under a fixed \(p\ge p_0\), the erroneous decision \(\mathrm F\) means
\(H<k+1\). By (7), it implies

\[
 B_n<k
 \quad\Longrightarrow\quad
 B_n\le k-1<\frac{p_0n}{2}.
 \tag{11}
\]

The last inequality holds for every real \(p_0n/2\), including when
that quantity is an integer: \(\lceil x\rceil-1<x\).
This strict step avoids any rounding loss.

Since \(\mathbb E_p B_n=np\),

\[
 np-B_n>np-\frac{p_0n}{2}
          \ge\frac{np_0}{2}.
 \tag{12}
\]

The binomial variance obeys
\(\operatorname{Var}_p(B_n)=np(1-p)\le n/4\), since
\(p(1-p)=1/4-(p-1/2)^2\).
Chebyshev's inequality, applied to the strict deviation event in (12),
gives

\[
 \begin{aligned}
 \Pr_p(H<k+1)
 &\le \Pr_p\left(|B_n-np|>\frac{np_0}{2}\right)\\
 &\le\frac{n/4}{(np_0/2)^2}
 =\frac1{np_0^2}.
 \end{aligned}
 \tag{13}
\]

Clipping this bound at one proves (3).
There is no assertion that the bound is sharp, that the chain witness
is longest, or that the increments of the entire order are iid.

The bound has no unknown \(p\) on its right side and holds separately
for every fixed \(p\in[p_0,1)\). This is the required class-uniform
inequality without a cross-law coupling. At \(N=2\), \(n=k=1\);
the formula remains valid, although its clipped bound may be trivial.
Sizes zero and one are outside the declared test, not cases in which
one divides by \(n=0\) or applies a nonexistent threshold.

## 5. Factorial-class error from distinct-head paths

### Completed chains and generating paths

For analysis only, place a directed edge \(i\to j\) when \(i\in U_{j-1}\).
The order generated by (8) is the transitive closure of this
increasing-label DAG. This follows inductively from the downward-closure
past rule.

Every directed path is a chain in the completed order. Conversely,
if \(v_0\prec v_1\prec\cdots\prec v_k\) is a chain, choose a directed
path between each successive pair. All internal labels for a path
from \(v_{a-1}\) to \(v_a\) lie strictly between those labels. The
successive intervals have disjoint interiors. The paths therefore
concatenate without repeated internal vertices into one directed path
containing the whole chain. It has at least \(k\) edges. Truncating its
initial segment yields a path of exactly \(k\) edges.

Thus \(H\ge k+1\) implies that at least one \(k\)-edge directed path
exists. This argument does not require observing any generating edges
or recovering their realization from \(M\).

### Probability and union count

For a specified increasing path
\(v_0<v_1<\cdots<v_k\), its required selections have the distinct heads
\(v_1,\ldots,v_k\). They depend on distinct, independent birth subset
coordinates in (8). Its probability is therefore

\[
                  \prod_{a=1}^k\rho_{v_a-1,q}.
 \tag{14}
\]

Only one selection is required in each coordinate. No multiplication
of different same-subset inclusion probabilities has occurred.

Let \(X_k\) count \(k\)-edge increasing paths, and set

\[
                         A_{N,q}=\sum_{m=1}^n\rho_{m,q}.
\]

For each increasing tuple of \(k\) distinct heads there are at most
\(N\) choices of starting vertex. Counting only valid starts would
improve the bound; using \(N\) is a safe overcount. Hence

\[
 \mathbb E_q X_k
 \le N\sum_{1\le m_1<\cdots<m_k\le n}
               \prod_{a=1}^k\rho_{m_a,q}
 \le\frac{N A_{N,q}^k}{k!}.
 \tag{15}
\]

For the last inequality, each product of \(k\) distinct indices occurs
\(k!\) times in the expansion of \(A_{N,q}^k\); the repeated-index
terms are nonnegative. Markov's inequality for \(X_k\) now gives

\[
                 \Pr_q(H\ge k+1)
                 \le\min\{1,N A_{N,q}^k/k!\}.
 \tag{16}
\]

Different paths may be dependent; no independence of their existence
events was used in (15)–(16).

### A common finite bound for every integer q >= 1

For \(q\ge1\), \(q/(q+1)\ge1/2\). Since each \(m\ge1\), (9) yields

\[
 \begin{aligned}
 A_{N,q}
 &\le\sum_{m=1}^n m^{-1/2}
 \le\int_0^n x^{-1/2}\,dx
 =2\sqrt n.
 \end{aligned}
 \tag{17}
\]

The integral comparison holds on each interval \([m-1,m]\) because
\(x^{-1/2}\ge m^{-1/2}\), with the integrable endpoint at zero.
Equations (16)–(17) prove the first bound in (4).

For every integer \(k\ge1\), monotonicity of \(\log x\) gives

\[
 \log(k!)\ge\int_1^k\log x\,dx
        =k\log k-k+1\ge k\log k-k,
 \qquad k!\ge(k/\mathrm e)^k.
 \tag{18}
\]

This also holds at \(k=1\). Substitution gives the second bound in (4).
Both bounds are clipped at one; a raw expression greater than one
is not a probability prediction greater than one, nor evidence that
the rule has small error. All small admissible \(N\) and all ceiling
values in (1) are covered.

No assertion about distinct exact asymptotic height exponents is needed.
The common finite inequality (17) alone makes (4) independent of the
unknown fixed integer \(q\).

## 6. Vanishing bounds and a sufficient symbolic error budget

For fixed \(p_0>0\), (3) tends to zero.
Because \(k\ge p_0n/2\),

\[
       \frac{2\mathrm e\sqrt n}{k}
       \le\frac{4\mathrm e}{p_0\sqrt n}.
 \tag{19}
\]

In particular, if

\[
                         n\ge(8\mathrm e/p_0)^2,
 \tag{20}
\]

the ratio is at most \(1/2\). The factorial-class error is then at most

\[
               N2^{-k}\le(n+1)2^{-p_0n/2}.
 \tag{21}
\]

The exponential dominates the linear factor, so this tends to zero.
The following entirely symbolic sufficient-size condition makes the
statement quantitative without evaluating any probability.

Predeclare \(\varepsilon_{\mathrm B},\varepsilon_{\mathrm F}\in(0,1)\).
It suffices to choose \(N=n+1\) with integer

\[
 \boxed{
 n\ge\left\lceil\max\left\{
 1,\;
 \frac1{\varepsilon_{\mathrm B}p_0^2},\;
 \left(\frac{8\mathrm e}{p_0}\right)^2,\;
 \left(\frac4{p_0\log2}\right)^2,\;
 \frac4{p_0\log2}\log\frac1{\varepsilon_{\mathrm F}}
 \right\}\right\rceil.}
 \tag{22}
\]

Here \(\log\) is the natural logarithm. This is conservative, not
optimized, and is a sufficient rather than necessary sample-order size.

The first error bound follows immediately from the second entry in (22).
For the second, the elementary inequality

\[
                           \log(n+1)\le\sqrt n
                           \quad(n\ge1)
 \tag{23}
\]

can be checked by setting \(f(x)=\sqrt x-\log(x+1)\).
At \(x=1\), \(f(1)=1-\log2>0\), and for \(x\ge1\),

\[
 f'(x)=\frac{(\sqrt x-1)^2}{2\sqrt x(x+1)}\ge0.
\]

The fourth entry of (22) consequently gives

\[
                  \log(n+1)\le\frac{p_0\log2}{4}n.
 \tag{24}
\]

Using (20), (21), (24) and the final entry in (22),

\[
 \Pr_q(\delta_{N,p_0}=\mathrm B)
 \le(n+1)\exp[-(p_0\log2)n/2]
 \le\exp[-(p_0\log2)n/4]
 \le\varepsilon_{\mathrm F}.
 \tag{25}
\]

Thus (22) guarantees errors at most
\(\varepsilon_{\mathrm B}\) and \(\varepsilon_{\mathrm F}\), respectively,
for all the fixed laws in the declared classes. Equality at a sufficient
threshold causes no problem: the claimed error inequalities are
nonstrict. Ceilings enforce integer size without changing their direction.

For a separately predeclared smaller \(N\), (3)–(4) still apply, but
they may not certify the desired tolerances. Failure of (22), or
triviality of these upper bounds, is **not** failure of the decision
rule itself and is not an impossibility theorem for other tests.

The theorem concerns a chosen deterministic \(N\). Interpreting these
bounds as simultaneous error control for inspecting many sizes and
stopping when the result looks convincing would require a different
argument. No such procedure is proposed here.

## 7. A sufficient algorithm and its separate costs

Height does not require solving the Ferrers induced-retention optimizer.
On the promised valid matrix (5), a sufficient exact procedure is:

1. Scan the matrix to compute the indegree of every vertex in its
   strict-relation DAG.
2. Use Kahn's topological algorithm: queue indegree-zero vertices;
   when removing a vertex, scan its outgoing row, decrement its
   successors' remaining indegrees, and queue newly zero entries.
3. Along that topological ordering, use
   \(h(v)=1+\max\{h(u):M_{uv}=1\}\), with maximum over empty set zero.
   Return \(H=\max_v h(v)\), then compare with \(k+1\).

The dynamic program can be implemented by updating each successor
when its predecessor is removed, so sorting and updates share an
outgoing-row scan. All predecessors have been processed before a
vertex is finalized. A path in the strict-relation DAG is a chain;
each chain is a path using its successive comparisons. Induction in
the topological order therefore proves that \(h(v)\) is the longest
chain ending at \(v\), even with transitive/redundant edges present.

This proves correctness using only the completed relation.
It does not compute a transitive reduction, reconstruct the original
generating DAG, or infer a birth ordering. A topological ordering is
a computational convenience; any such ordering yields the same \(H\).

The sufficient costs for this declared representation are:

| Cost category | Sufficient requirement/bound |
| --- | --- |
| Observation supplied | One exact complete \(N\)-vertex order and its known \(N\); all \(N^2\) Boolean matrix entries available |
| Input storage | \(N^2\) relation bits, plus an encoding of \(N\); arbitrary matrix indexing is sufficient |
| Height computation on promised valid input | \(O(N^2)\) relation-entry inspections and integer additions, comparisons, and indegree updates |
| Integer sizes | Heights, counts and indices use \(O(\log N)\) bits |
| Bookkeeping bit upper bound | \(O(N^2\log N)\), under indexed matrix-bit access and ordinary binary bookkeeping |
| Auxiliary working storage | \(O(N)\) words, or \(O(N\log N)\) bits; input plus workspace \(N^2+O(N\log N)\) bits |
| Exact threshold preparation | If \(p_0=a/b\) and each integer uses at most \(L\) bits, sufficient grade-school arithmetic costs \(O((L+\log N)^2)\) bit operations, separately from height processing |

For the word-operation count, use words large enough to hold a vertex
index, indegree or height. For the bit upper bound, charge
\(O(\log N)\) for such elementary integer operations and indexing,
with the stated indexed matrix access convention. This is not a claim
about arbitrary sequential-tape access or unbounded external vertex-name
strings. The threshold's rational arithmetic is not counted as a
unit-cost operation on an arbitrary real.

If validity of the finite relation is not promised, a sufficient
separate check scans the diagonal and opposite pairs for irreflexivity
and asymmetry and checks all triples for
\(M_{uv}=M_{vw}=1\Rightarrow M_{uw}=1\).
This uses \(O(N^3)\) relation inspections, without increasing the
asymptotic matrix storage. A malformed matrix is outside the theorem's
observation domain; rejecting it is input validation, not a third
in-family statistical conclusion. Topological sorting alone would detect
cycles but would not certify transitive completeness.

Neither matrix validity nor exact computation can certify that a
physically obtained matrix is faithful to an inaccessible underlying
order. The cost of preparing a system, obtaining each relation,
determining \(N\), establishing readout fidelity, or controlling noise
is **not supplied**. \(N^2\) is the sufficient data representation,
not an asserted number of physical measurements or their cost.

These are justified sufficient algorithms and resource bounds, not
optimality, implementation, measured throughput, empirical speedup,
or an application advantage. No algorithm was executed in this packet.

## 8. Interpretation, absent inputs, and failure boundaries

If the true process belongs to \(\mathrm B(p_0)\), (3) bounds how
often (2) returns \(\mathrm F\) at the chosen size. If it belongs to
\(\mathrm F\), (4) bounds how often the rule returns \(\mathrm B\).
Neither quantity is
\(\Pr(\text{true class}\mid\text{observed decision or order})\).
No class prior or distribution on \(p\) or \(q\) is specified.

The fixed lower bound \(p_0>0\) is load-bearing for the common threshold
and common finite-size assurance. Without it, the Bernoulli class
contains parameters arbitrarily close to zero, and the present
size/error guarantee cannot be made parameter-free by inserting an
unknown \(p\) after observing the order. For any chosen positive \(p_0\),
parameters below it lie outside the declared class. This states a
limit of the present theorem and bounds, not an impossibility theorem
for all possible statistics, observation budgets, or tests.

The assumptions are equally important on the observation side:

- A partial order report with missing or unknown comparisons is not
  necessarily the completed relation in (5). Computing its height or
  closing its reported edges does not establish the true height.
- Spurious comparisons, missing vertices, identification errors and
  noisy orientation can change height. The present error bounds
  include none of these mechanisms; a specified observation channel
  and a new error-transfer argument would be required.
- If faithful readout or known cardinality \(N\) is unavailable, this
  theorem does not furnish them. It supplies no calibrated physical
  experiment or currently executable native preparation/readout map.
- Processes outside the two declared optional families have no
  classification guarantee, even if they satisfy the broad marked
  admission principles. A confident-looking label is not evidence
  that those two families exhaust the model space.

The accepted asymptotic difference is therefore accompanied by a
predeclared finite mathematical prediction on an explicit input.
It has not thereby become a physical discriminator.

Nothing here redesigns the Ferrers target or computes its retention.
Height alone is used to distinguish the specified laws, not to infer
a metric, dimension, dense two-dimensional approximation, or geometry
emergence. The primitive-input and physical-correspondence gaps are
unchanged. Scalar passive payloads do not become informative quantum
dynamics through this test. No gravity/mass law, clock, metric-as-record
promotion or physical-law validation follows.

An application claim would still require a fixed benchmark, relevant
baselines, preparation/readout and computation costs, failure rates,
held-out evaluation and an explicit practical objective. None is
supplied, executed or authorized by this manual theorem. It is not
evidence of production readiness or superiority.

## 9. Mathematical dependencies and source correspondence

The new yield is the finite two-family decision rule, its exact
rounding-aware Bernoulli bound, common factorial bound, symbolic
sufficient-size theorem and sufficient input/computation analysis.
The accepted finite law premises are not replaced by asymptotic
intuition or by a new numerical calculation.

The six literal source manuscripts have these roles:

- BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md supplies the accepted
  from-empty product law and finite adaptive-tip iid chain witness (7).
- FACTORIAL_POWER_LAW_FAMILY.md supplies the law (8), finite marginal
  bound (9), independent-birth distinction and finite distinct-head
  path mechanism. Section 5 spells out the conversion and count.
- DENSE_FERRERS_INCOMPARABILITY_SCREEN.md preserves the distinction
  between a fixed dense target and unrestricted retention; no density
  premise is needed for the new height classifier.
- INTRINSIC_GEOMETRY_TARGET_SCREEN.md preserves the intrinsic completed
  order/target/physical-readout distinctions; its half-scale law is not
  silently added to the candidate classes.
- THEOREM_PACKAGE.md supplies the declared marked-order/passive-payload
  setting and separation from the independent optimizer.
- LAW_DEPENDENCE.md distinguishes actual optional laws, coordinate
  changes and unsupported principle-forced or physical conclusions.

The source author inspected the two literal provenance-record schemas
and joined the six source identities to the supplied adjudication record.
The Bernoulli source's later acceptance refers to that predecessor only;
its historical pending header does not determine this manuscript's
acceptance. This source-identity observation is distinct from independent
review of the present theorem.

The other five public source snapshots were attributed by supplied
metadata to an earlier published state. That attribution was not
independently checked with Git or network access. No original path,
archive link, additional adjudication member, source program or protected
input was followed.

The public reader equivalents below preserve the six scientific roles
listed above. These links identify readable public dependencies, not
public copies of private provenance records or original atomic custody.

| Scientific source role | Public reader reference |
| --- | --- |
| Bernoulli-subset law and finite adaptive-tip witness | [BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md](BERNOULLI_SUBSET_LAW_FERRERS_COUNTEREXAMPLE.md) |
| Factorial-power law and finite marginal/path premises | [FACTORIAL_POWER_LAW_FAMILY.md](FACTORIAL_POWER_LAW_FAMILY.md) |
| Fixed dense target versus unrestricted retention | [DENSE_FERRERS_INCOMPARABILITY_SCREEN.md](DENSE_FERRERS_INCOMPARABILITY_SCREEN.md) |
| Intrinsic order, target and physical-readout distinctions | [INTRINSIC_GEOMETRY_TARGET_SCREEN.md](INTRINSIC_GEOMETRY_TARGET_SCREEN.md) |
| Declared marked-order and passive-payload setting | [THEOREM_PACKAGE.md](THEOREM_PACKAGE.md) |
| Optional laws versus coordinates and physical claims | [LAW_DEPENDENCE.md](LAW_DEPENDENCE.md) |

All eight current source captures are complete. Four current manuscript
bodies exactly match previously consumed complete native strings.
The two remaining bodies have exact previously consumed prefixes;
their complete appended additions were displayed and consumed.
These are exact stored-text comparisons plus separate native byte/hash
checks, not assertions that every unchanged body was fully redisplayed
this sitting. Both literal JSON bodies were fully displayed and consumed.

There was no new truncated source display. The earlier two aggregate
THEOREM_PACKAGE.md display failures and complete bounded-slice recovery,
as well as older source-contained execution, receipt, source-check and
custody limitations, are preserved. Current joins do not erase or
reconstruct them. No omitted observation timestamp is supplied by
inference.

## 10. Verification categories and stop

Two independent manual workers reviewed supplied mathematical context.
One checked the finite error bounds, strict integer case and sufficient
size constants; the other checked observation/encoding assumptions,
algorithm correctness, costs and interpretation. Neither accessed
source files or independently audited their identity. Their scopes
are separate, and their worker-reported guard observations are distinct
from direct root observations. Both reviews passed without a required
mathematical correction.

All new mathematical reasoning is manual symbolic proof. There is no
probability/tail/interval evaluation, coefficient reduction, scientific
executor, simulation, dataset or network acquisition, optimization,
benchmark, experiment or protected validation. Text assembly, exact
readback comparisons, JSON parsing, native hashes, byte counts and
directory inventory are administrative, not scientific computation.
Manual cross-checks are not proof-assistant verification or native
adjudication. Separate source read/hash observations are not atomic
historical-custody certificates.

The source manuscript and three private administrative records form the
source author's frozen packet.
The mathematical manuscript's full readback is distinguished from
metadata-only summaries of own JSON receipt readbacks.

Manual mathematical construction is separate from independent native and
editorial review. Acceptance and publication records are maintained
separately; this derivative preparation does not adjudicate the theorem.
The source-author supplied-context worker reviews above are not replaced
by, or represented as, a fresh source-identity audit.

Private record names, paths, identifiers, fingerprints and tool receipts
are withheld from this public derivative. The exact transformation and
private correspondence map are retained separately. This metadata
redaction supplies no public executable custody, machine proof or
reconstruction of historical custody. It supplies neither physical
readout nor application execution; existing thresholds, frozen protocols
and RET remain unchanged. See the [publication note](PUBLICATION_NOTE.md)
and [redacted-publication policy](../../coordination/REDACTED_PUBLICATION.md).
