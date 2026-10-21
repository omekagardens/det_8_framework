# A prospective synthetic three-category diagnostic benchmark

21 October 2026. **DESIGN ONLY.**
No implementation, dataset generation, sampler, calibration or benchmark
has been executed. This document grants no execution permission.

## 1. Disposition: a minimal conformance benchmark, not an advantage claim

This fixes one finite-alphabet benchmark with one candidate, three
references, explicit operating targets, cost accounting and a fresh
independently controlled held-out design.

A substantive design check has already rejected the candidate's
**raw-observation cost superiority** over the standard sequential
reference below. On the core class, the candidate consumes at least
256 raw observations, whereas the reference has expected consumption
at most \(640/3<256\), while also meeting the stated risk/coverage
operating targets. Section 5 proves this without running a benchmark.

Accordingly this packet takes the permitted fallback: a **minimal
implementation-conformance/adequacy specification**. Its primary endpoint
can certify a bounded synthetic operating point if a future implementation
passes; it cannot certify competitive practical value. The missing premise
is a distinct justified diagnostic, or a genuinely different predeclared
utility objective with a defensible advantage hypothesis. Neither is
invented here. There is no second candidate, weakened reference or
replacement success target chosen to rescue the rejected raw-cost claim.

The synthetic probabilities below are invented mathematical inputs.
They are not evaluated DET probabilities, evidence that a native law
attains these vectors, or evidence of any conditional \(\Xi>1\) occurrence.
[The fixed-budget testing theorem](../../track_b/native_theorem_package_v1/P4_FIXED_BUDGET_TESTING_LIMIT.md) motivates separating an availability-restricted operating class
from rare-event stress; it does not make either synthetic class native.

## 2. Fully declared synthetic family and information access

True and reported alphabets are \(\{0,4,O\}\).
For a label \(H\in\{B,Q\}\), define
\[
 q_B=1/4,\qquad q_Q=3/4,\qquad
 p_{H,\nu}=\bigl(\nu(1-q_H),\nu q_H,1-\nu\bigr).
\]
These are complete normalized three-category probability vectors.
All raw draws are iid for one fixed \(H,\nu,M\) per run; conditional on
true draws, channel outputs are independent with the fixed row-stochastic
matrix \(M\). This is an explicitly specified synthetic generator model.

The three channels, rows true and columns reported in order \(0,4,O\), are
\[
 M_I=\begin{pmatrix}1&0&0\\0&1&0\\0&0&1\end{pmatrix},\quad
 M_C=\begin{pmatrix}7/8&1/8&0\\1/8&7/8&0\\0&0&1\end{pmatrix},
\]
\[
 M_D=\begin{pmatrix}
 7/16&1/16&1/2\\
 1/16&7/16&1/2\\
 1/256&1/256&127/128
 \end{pmatrix}.                                          \tag{1}
\]
Thus I is exact reporting, C confuses diagnostic labels, and D combines
misses, confusion and symmetric false diagnostics from OTHER.
All entries and row sums are exact. No channel parameter is estimated
or calibrated in this benchmark.

| Regime | True availability values | Labels | Channels | Number of strata |
| --- | --- | --- | --- | ---: |
| Core operating grid | \(1/4,1/2\) | B,Q | I,C,D | 12 |
| Rare-event stress grid | \(1/256,1/4096\) | B,Q | I,C,D | 12 |

A stratum is one exact triple \((H,\nu,M)\). The core floor
\(\nu\ge1/4\) is justified **by design**, not by native theory or measurement.
The selected core points lie in \([1/4,1/2]\); mathematical bounds below
hold on that interval, but a finite-grid evaluation would not empirically
validate an entire continuous family.
Stress results are always separate, with no inherited core guarantee.

Every method receives only the reported stream, channel identifier,
public family definition, fixed cap and its frozen constants.
None receives the true label, true-category stream, exact generating
availability, core/stress identifier, seed or a run identifier encoding
those facts. The evaluator holds those fields. Each method resets state
between runs; no cross-run inference from presentation order is allowed.
Runs are presented through opaque identifiers in an independently shuffled
order. Channels and the public label probabilities are equally known
to candidate and statistical reference.

There is **no oracle baseline**. The sequential reference knows the same
core availability range and label/channel information as the candidate,
not a run's exact generating pair. A future oracle cannot be added to
this frozen comparison without a separately labeled revision.

## 3. Exactly one candidate and three references

All methods have the same maximum raw budget
\[
                              N=4096.
\]
Reported OTHER counts toward the cap. Outputs are B, Q, or A=ABSTAIN.
Failure flags are recorded separately as described in §8.

### Candidate C256: fixed diagnostic count

Use \(m=256\) and integer threshold \(k=128\), fixed now.

Read raw observations until the earlier of the 256th reported
diagnostic (\(Y\in\{0,4\}\)) and raw observation 4096.
Among the first 256 diagnostics let \(S\) count reported 4.

- If the target count is reached, output Q for \(S\ge128\), otherwise B.
- If it is not reached by the cap, output A.
- If the 256th diagnostic arrives exactly at the cap, classify it.
- No cap extension, label replacement, peeking-based threshold change
  or conditional exclusion of unfavorable outcomes is allowed.

This is a separate proposed signal-processing diagnostic. It is not a
new native law, a DET-derived optimal algorithm, or a retuning of [the diagnostic-event theorem](../../track_b/native_theorem_package_v1/P4_DIAGNOSTIC_EVENT_TEST.md)'s
\(m=40000,N=400000,k=38825\) design.

### Reference S: capped robust sequential likelihood ratio

The core observed conditional-label endpoints are
\[
 (U_I,V_I)=(1/4,3/4),\quad
 (U_C,V_C)=(5/16,11/16),\quad
 (U_D,V_D)=(43/134,91/134).                                \tag{2}
\]
In every case \(V=1-U\).
For the supplied channel, maintain diagnostic score
\(J=\#4-\#0\), initially zero, and define the exact integer
\[
 h_M=\min\{j\ge1:(V_M/U_M)^j\ge1000\}.                    \tag{3}
\]
This unique threshold is part of the specification, not fitted to data.
It may be computed once with exact rational comparisons during a future
authorized implementation; no such computation is executed here.
For I, \(h_I=7\) since \(3^6<1000<3^7\).

After each diagnostic, output Q immediately if \(J\ge h_M\), or B if
\(J\le-h_M\). OTHER leaves \(J\) unchanged but consumes a raw draw.
If neither boundary is reached by 4096, output A.
A boundary reached on the final draw takes precedence over abstention.

This is the standard sequential likelihood-ratio construction for the
two conservative Bernoulli endpoints, with thresholds 1000 and 1/1000,
capped by the same raw budget. The diagnostic likelihood ratio is
\[
 L=(V/U)^{\#4}((1-V)/(1-U))^{\#0}=(V/U)^J.
\]
The reference uses integer score comparisons, not needless per-draw
floating-point logarithms. Its setup cost is accounted separately.
Neither reference nor candidate is given a nuisance-parameter oracle.

### Reference A: always abstain

Output A without reading the stream. Raw consumption is zero.
This is the explicit control showing why tiny wrong-label counts
without coverage cannot establish success.

### Reference R: balanced random label

Use one exogenous fair random bit, independent of source/channel draws
and labels, to output B or Q with equal probability, without reading
the stream. Raw consumption is zero. Its prevalence assumption is the
benchmark's balanced label weighting, not knowledge of a hidden label.
Expected per-label error is \(1/2\) and coverage one.

All four methods are evaluated on paired source realizations, but their
outputs are not independent replicates. No extra data, optimization or
training budget is assigned to a method under another name.

## 4. Why the core target is mathematically plausible

These are prospective hand calculations on invented inputs, not observed
performance or native probability evaluation.

For I and C the observed diagnostic availability is \(\nu\); their
conditional endpoints are immediate from (1).
For D,
\[
 \widehat\nu=\nu/2+(1-\nu)/128,\qquad
 \widehat q_H
 =\frac{(\nu/2)(1/8+3q_H/4)+(1-\nu)/(256)}
        {\widehat\nu}.
\]
At the core floor \(\nu=1/4\),
\(\widehat\nu=67/512\), and genuine detections have weight \(64/67\)
among reported diagnostics. Symmetric leakage pulls labels toward
\(1/2\); its maximum core pull is at this smallest \(\nu\).
Therefore, throughout the core,
\[
 \widehat\nu\ge67/512,\qquad
 \widehat q_B\le43/134,\qquad
 \widehat q_Q\ge91/134.                                   \tag{4}
\]
The midpoint margins are at least \(12/67\).

Under fixed iid reported categories, conditioning on the indicator
pattern of diagnostic arrivals leaves the selected diagnostic labels
iid Bernoulli at \(\widehat q_H\). Thus, conditional on collecting 256,
the candidate's selected count is binomial, as in [the diagnostic-event theorem](../../track_b/native_theorem_package_v1/P4_DIAGNOSTIC_EVENT_TEST.md)/[the observation-channel theorem](../../track_b/native_theorem_package_v1/P4_OBSERVATION_CHANNEL.md).
The one-sided bounded-variable exponential bound gives
\[
 e_{\rm conditional}
 \le \exp[-2(256)(12/67)^2]
 =e^{-73728/4489}<e^{-12}<1/4096.                          \tag{5}
\]
Here \(73728>12(4489)\), and \(e>2\) implies \(e^{12}>4096\).
If fewer than 256 diagnostics occur in 4096 draws, their count is at
most 255. Since the minimum expected count is
\(4096(67/512)=536\), the same inequality gives
\[
 P(A_C)\le
 \exp[-2(4096)((536-255)/4096)^2]
 =e^{-157922/4096}<e^{-12}<1/4096.                         \tag{6}
\]
Hence the mathematical candidate has stringent core error, coverage
and power bounds under the declared model. These do not guarantee that
a future implementation or finite evaluation will pass its acceptance
rules.

Expected uncapped collection cost is \(m/\widehat\nu\), from the
geometric waiting-time sum. Capping can only reduce it, so
\[
 256\le E[T_C]\le\frac{256(512)}{67}
       =\frac{131072}{67}<2048=N/2.                       \tag{7}
\]
The lower bound is deterministic: 256 diagnostics require at least
256 raw draws, and an unsuccessful run consumes 4096.

The core conditions are deliberately restricted. For D at fixed
positive leakage, the reported conditional labels tend to \(1/2\) as
true \(\nu\to0\); reported diagnostics can still occur.
Stress uses the **unchanged** core-frozen rules, not new endpoints
selected to rescue performance. All stress errors and abstentions
must be reported; no core claim is extrapolated to stress.

## 5. The raw-cost advantage claim is rejected before execution

The reference's wrong-label guarantee is standard but can be checked
directly here. Under a baseline conditional probability \(q\le U\),
the mean one-diagnostic likelihood multiplier is
\[
 q\,V/U+(1-q)(1-V)/(1-U)\le1.
\]
It equals one at \(q=U\) and increases with \(q\).
Adding OTHER steps of multiplier one preserves this inequality.
Thus the nonnegative likelihood product has conditional mean no greater
than its previous value. Finite summation/conditioning for the first
upper crossing capped at N gives expected stopped product at most one;
on a crossing it is at least 1000. The probability of an erroneous Q
crossing is therefore at most \(1/1000\). The reciprocal argument under
\(q\ge V\) bounds an erroneous B crossing by the same number.
Stopping at the other boundary can only remove such errors.
This proof uses bounded stopping, not an unbounded stopping assumption.

The reference also meets the proposed quality targets, so its lower
cost is not obtained merely by tolerating chance performance.
All odds \(V/U\) exceed 2, and \(2^{10}>1000\), so \(h_M\le10\).
If no reference boundary has been reached after the first 256
diagnostics, then under Q their 4 count is at most 132.
Under B the same statement holds for the count of 0.
Using (4),
\[
 91/134-132/256=701/4288>5/32.
\]
The probability of such a no-hit event is less than
\(e^{-2(256)(5/32)^2}=e^{-25/2}<1/4096\).
Adding the failure to collect 256 by the cap from (6) gives
\[
 P(A_S)<1/2048,\quad
 P_Q(Q_S)>1-1/1000-1/2048,\quad
 e_{S,\rm conditional}<\frac{1/1000}{1-1/2048}<.01.        \tag{8}
\]
In particular its population coverage exceeds .99 and power exceeds .98.

For its cost, orient the raw score toward the true label. Each raw
increment is in \(\{-1,0,1\}\). Its mean under I,C,D is respectively
\[
             \nu/2,\qquad 3\nu/8,\qquad 3\nu/16,
\]
so the mean \(\mu\) is at least \(3/64\) on the core.
Let \(\tau\le N\) be the reference's stopping time.
Because \(\{\tau\ge n\}\) depends only on previous observations,
independence and finite summation give
\[
 E[J_\tau^{\rm oriented}]
 =\sum_{n=1}^N E[\mathbf1_{\{\tau\ge n\}}\Delta J_n^{\rm oriented}]
 =\mu E[\tau].
\]
Its stopped score is at most \(h_M\), including a cap without crossing;
unit increments do not overshoot the integer boundary. Consequently
\[
 \boxed{\quad E[T_S]\le\frac{h_M}{\mu}\le\frac{640}{3}
                <256\le E[T_C].\quad}                    \tag{9}
\]
This rejects raw-cost superiority in every core cell, not just a pooled
comparison. A fortiori a proposed 20% raw-cost gain is impossible.
No observation or simulated sample was used to select this conclusion.

The benchmark may measure implementation overhead and confirm logical
behavior, but a favorable noisy cost estimate cannot override (9).
Such a discrepancy requires checking assumptions, implementation and
sampling uncertainty, not promoting an advantage claim.
No alternative utility objective is selected after seeing this rejection.

## 6. Development, freeze and fresh held-out control

All probabilities, channels, counts, thresholds, strata, targets and
inference formulas in this document are fixed analytically **now**.
There is no outcome-based parameter search.

If implementation is separately authorized, development material is
limited to **200 independent complete runs per stratum**:
24 strata, 4800 runs. Labels and parameters may be visible in development.
That material may be used to verify category mapping, boundary/tie
behavior, cap accounting, exact score thresholds, metric formulas,
failure handling and instrumentation. It may not fit m, k, N, channel
rates, reference boundaries or acceptance criteria.

Any proposed scientific redesign requires a new independently reviewed
specification before any held-out generation/access. It is not an
amendment to this frozen result, and no redesign is authorized here.

Before held-out generation, an independent evaluator must record and
freeze the candidate/reference source and build hashes, generator and
metric implementation/version, random-stream separation scheme,
runtime environment, timing harness and an information-access audit.
Development may continue fixing implementation bugs only before that
code freeze; every attempted version and development cost must be retained.

The evaluator then creates **fresh, separately controlled** held-out
randomness and realizations. No existing protected holdout is read,
repurposed, copied or reused. Developers must not receive held-out seeds,
true categories, labels, availability values, partial metric summaries
or per-case feedback before final evaluation closes.
The evaluator retains generator keys and immutable run/stratum manifests;
source/channel draws, presentation ordering and random-reference bits
use separate streams.

The mathematical sampling model uses independent draws. A future
pseudorandom realization must disclose and freeze its algorithm/version,
seed management and exact rational-category mapping; a seed hash is not
a proof of iid physical randomness. No generator has been implemented
or chosen from sample outcomes here.

The fixed held-out size is
\[
                    R=2500\text{ independent runs per stratum}.
\]
There are 60000 independent evaluation units across all 24 strata.
Each unit is one entire iid vector of at most 4096 reported categories,
with a fixed true stratum. Raw observations, repeated timings, paired
method outputs and internal diagnostic hits are **not** extra independent
evaluation units.

The evaluator may generate a full length-4096 vector once and expose
each method only the prefix it requests, using the same vector for all
methods. A method receives no later observations after it stops.
Paired replay improves comparison control without creating independent
replicates. No method state persists across runs.

No early stopping for apparent statistical success, sample-size expansion,
failed-run deletion, seed search, favorable-stratum selection or
post-result threshold adjustment is allowed. An interrupted evaluation
is incomplete, not a pass. A bug or leakage discovered after code freeze
invalidates the affected evaluation; preserve every result and request
separate authorization for any corrected fresh evaluation.

## 7. Primary endpoint and simultaneous error accounting

### Primary endpoint: operating-point conformance, not competitive value

A future C256 implementation passes the **single conjunctive primary
endpoint** only if all of the following hold in **every core stratum**
using the simultaneous bounds below:

| Requirement | Acceptance condition |
| --- | --- |
| Unconditional wrong label | Upper bound \(\le .01\), under each true label |
| Coverage \(P(\text{B or Q})\) | Lower bound \(\ge .99\), under each true label |
| Conditional-on-decision error | Upper bound \(\le .01\), with defined/positive coverage support |
| Alternative power \(P_Q(Q)\) | Lower bound \(\ge .98\) |
| Type-II failure including A | Upper bound \(\le .02\), equivalently the power condition |
| Mean consumed raw draws | Upper bound \(\le .60N\), under each true label |
| Numerical/protocol failures | None for the candidate in core evaluation |

Every core cell must pass; pooled accuracy cannot compensate for a
failure. Frequent abstention fails coverage and power, while near-chance
classification fails error targets. Always-abstain and random references
make those two pathologies explicit.

A pass is called **synthetic operating-point conformance only**.
It is not practical-value success: the candidate's raw-cost superiority
has already been rejected by (9). The standard reference is assessed
against the same quality targets, with its own reported coverage/cost.
Stress cells have no primary pass target; they document failure behavior
under unchanged rules and cannot be pooled into or selected out of the core.

### Probability intervals: 288 predeclared quantities

For each of four methods and each of 24 strata, estimate the three output
probabilities \(p_B,p_Q,p_A\). This is \(4\cdot24\cdot3=288\) quantities.
Allocate family error .025 to their two-sided exact binomial-tail
intervals: each one-sided tail has probability
\[
                         \gamma_p=1/23040.
\]
For a count \(k\) out of \(R=2500\), use the interval \([L(k),U(k)]\):

- \(L(0)=0\); otherwise L solves
  \(P_{\operatorname{Bin}(R,L)}(K\ge k)=\gamma_p\).
- \(U(R)=1\); otherwise U solves
  \(P_{\operatorname{Bin}(R,U)}(K\le k)=\gamma_p\).

These are monotone binomial-tail inversions, not normal approximations.
For any fixed true probability, the chance of exceeding either endpoint
is at most its tail allocation: the corresponding rejected count set
is an upper or lower binomial tail of probability at most \(\gamma_p\).
A union bound gives simultaneous coverage at least .975 for all 288.
Independence between methods, categories or intervals is unnecessary.

Derive the requested metrics from the same simultaneous intervals:

\[
 \begin{array}{ll}
 \text{coverage:}&[1-U_A,\ 1-L_A],\\
 \text{power under Q:}&[L_Q,\ U_Q],\\
 \text{type-II failure including A under Q:}&[1-U_Q,\ 1-L_Q],\\
 \text{conditional wrong-label upper bound:}&
       \min\{1,U_{\rm wrong}/(1-U_A)\}\quad\text{if }1-U_A>0.
 \end{array}                                             \tag{10}
\]
Do not estimate conditional error by treating its random denominator
as another fixed sample size without justification.
If there are zero observed decisions, the empirical conditional error
is **undefined**, not zero. If coverage has no positive lower bound,
report the uninformative conditional interval and do not certify it.

### Cost intervals: 120 predeclared quantities

Normalize consumed raw count as \(Z=T/N\in[0,1]\).
Report 96 mean-cost intervals (four methods times 24 strata), and 24
paired mean contrasts
\[
                    W=(T_C-T_S)/N\in[-1,1].
\]
The contrasts describe cost differences; they are not live superiority
tests for a claim already rejected analytically.

Allocate the other family error .025 to these 120 two-sided intervals.
Each tail is \(1/9600\). For R independent run values in an interval of
width \(w\), use radius
\[
                   r_w=w\sqrt{\log(9600)/(2R)}.           \tag{11}
\]
Use \(w=1\) for mean normalized cost and \(w=2\) for paired contrasts,
clipping to their possible ranges as appropriate.
The paired differences are independent across runs; the two methods
within a run need not be independent.

For completeness, the bounded-variable exponential inequality behind
(5), (6), (8), and (11) is self-contained. For \(X\in[a,b]\), its
centered log moment-generating function has second derivative equal to
a tilted variance, at most \((b-a)^2/4\): subtract the interval midpoint
and bound the second moment. Its value and first derivative vanish at
zero, so integration gives log-mgf at most \(t^2(b-a)^2/8\).
Independence, exponential Markov and optimization give
\(P(\bar X-EX\ge r)\le e^{-2Rr^2/(b-a)^2}\), and the lower tail likewise.
This proves (11) without relying on a numerical experiment.

Together the probability and cost allocations have family failure
probability at most .05 by a union bound. The conjunctive primary
endpoint adds no extra unbudgeted testing. All probability/mean-cost
inferences stay within this fixed family; any exploratory metric is
clearly descriptive with no new headline success claim.

No intervals have been evaluated. A future implementation must use
monotone root bracketing and verified binomial-tail evaluation with
outward-rounded endpoints of absolute bracket width at most \(10^{-10}\).
If this cannot be certified, use an uninformative interval and a
numerical-failure flag; do not substitute an anti-conservative shortcut.
Metric code and its numerical policy must be frozen before evaluation.

The selected R is a fixed design size, not a native power calculation.
It permits informative bounds for favorable counts, but does not
guarantee a pass or justify post-result expansion.

## 8. Mandatory reporting, costs and failure rules

Publish no result from this design without a complete per-method,
per-stratum table containing:

- Exact synthetic \(H,\nu,M\), and core/stress status.
- B/Q/A counts, unconditional wrong-label frequency and interval,
  type-II failure including A, power, coverage and their intervals.
- Conditional error where empirically defined, its conservative bound,
  and explicit undefined/uninformative cases.
- Numerical/protocol failure counts and reasons. For probability
  accounting a failed method invocation is A, **and** remains separately
  flagged; no failed run disappears. Candidate core failure disqualifies
  primary conformance even if its other averages pass.
- Consumed raw count, reported diagnostic count, stopping reason and
  raw mean interval; paired candidate-reference cost contrasts.
- Complete development, generation, evaluation and replay costs,
  including unsuccessful attempts and invalidated runs.

The held-out generation cap is
\[
                    60000(4096)=245760000
\]
reported raw category positions.
Development adds \(4800(4096)=19660800\), for a combined
265420800 reported positions if every full vector is generated.
A two-stage true-category/channel generator has at most twice as many
categorical draw slots, 530841600 across development and held-out;
deterministic rows may require no random draw, but all actual generator
work must be counted. These are prospective workload ceilings, not
performed sampling or physical acquisition costs.

Generating full vectors once for pairing still costs the generator
those positions even when a method consumes a short prefix.
Method-consumed prefixes are a separate **logical** acquisition metric.
Do not claim actual generation savings by multiplying only those
prefix lengths; do not multiply shared raw vectors by four and call
them independent data.

Instrumentation must report a cost vector, not an unexplained unit score:
raw fetches, category tests, integer counter updates, comparisons,
probability/log operations, allocations and one-time setup.
Both stream methods have linear worst-case raw processing and bounded
counter state; exact constants and build choices must be measured.
Reference S must use its integer score implementation rather than
artificially expensive per-draw logs.
Do not equate software operation counts with physical measurement costs.

For any later authorized timing study, freeze language/compiler/runtime,
hardware/OS, thread settings and process configuration before held-out
generation. Use identical stream adapters and isolated method instances.
Measure both full pipeline time (including data generation/dispatch)
and method-only time on already generated vectors; report them separately.

The timing subset is fixed now: the first 100 evaluator-assigned units
from each stratum, 2400 vectors, not the fastest or easiest outcomes.
After five public-development warm-up batches, run 30 timing replays
per method with independently randomized method order and fixed code.
Report all 30 durations, median, interquartile range and range.
Replays create no new independent accuracy units and no new raw source
realizations, but their actual reads/operations/time count as work.
These timing summaries are descriptive, not added statistical
superiority claims. Developers remain unable to inspect held-out
realizations during timing.

Measure peak process memory and method-state allocations using a
documented OS/runtime instrument; report fixture/generator storage
separately from detector state. Preserve timing harness overhead and
empty-method control measurements. A slower or more memory-intensive
result cannot be discarded as inconvenient.

Physical preparation, measurement access and calibration costs are
**unknown**, not zero. Known synthetic matrices require no empirical
calibration here; that says nothing about the cost of obtaining a
real channel. No conversion from synthetic throughput to physical
deployment cost is justified.

Stop/failure rules are fixed:

1. No run starts without separate implementation/evaluation authorization,
   reviewed frozen code and independent holdout control.
2. A source/label leak, duplicated/reused holdout, generator/specification
   mismatch, protocol alteration or missing accounting invalidates
   conformance. Preserve evidence; no quiet repair/re-run.
3. Any candidate numerical failure or any core acceptance failure means
   no primary pass. Incomplete evaluation is incomplete, not success.
4. A reference defect makes the comparison invalid; do not weaken or
   replace it after results. Its analytic definition stays fixed.
5. No early efficacy stopping, optional sample-size extension,
   re-seeding to improve results or selective reporting.
6. Exceeding the declared workload or a later authorized execution
   resource cap stops the run as incomplete; it does not authorize
   additional resources or a changed protocol.

## 9. Meaning, boundaries and stop

A successful conformance evaluation would establish only that a particular
frozen implementation met declared synthetic risk/coverage/cost targets
on this grid, with the stated uncertainty and generator assumptions.
It would not establish competitive raw-cost value, which is already
rejected for C256 against S, nor general superiority in unspecified tasks.

There is currently no independently established DET-specific implementation
advantage or physical readout in this packet. A genuinely practical-value
candidate remains a missing premise, not an outcome to be manufactured by
weak baselines, hidden abstention or a changed metric.

Neither the designed parameters, mathematical adequacy checks nor any
future benchmark success would establish native physical predictions,
actual conditional \(\Xi>1\) occurrence, empirical DET/ontology validation,
historical-custody recovery, production qualification, or physical
calibration/preparation feasibility. Observing full native order or other
physical records remains a separately justified correspondence problem.

All existing numerical designs and WIDTH_DIAGNOSTIC /
APPROXIMATE_WIDTH_DIAGNOSTIC remain frozen and untouched. No existing
protected holdout is repurposed. RET remains paused.
This is one separate proposed benchmark, not execution permission,
a new coefficient gate, or an inverse-estimation programme.

## Public premises and evidence scope

The [fixed-budget testing theorem](../../track_b/native_theorem_package_v1/P4_FIXED_BUDGET_TESTING_LIMIT.md)
motivates the distinction between an availability-restricted operating class
and rare-event stress. The
[observation-channel theorem](../../track_b/native_theorem_package_v1/P4_OBSERVATION_CHANNEL.md)
states the declared category-channel premises and rare-event leakage limits.
The [diagnostic-event theorem](../../track_b/native_theorem_package_v1/P4_DIAGNOSTIC_EVENT_TEST.md)
supplies the conditional-label selection argument and the separate earlier
design. These dependencies do not turn invented benchmark probabilities into
native laws or establish a conditional native occurrence.

For construction of the source manuscript, the following finding and manual
proof statement are retained:

Two supplied-context manual challenges checked family/channel arithmetic,
statistical accounting and reference fairness. Both identified the
raw-cost dominance obstruction before any design was written or data
generated. The tentative superiority endpoint was rejected; the frozen
paired contrast is descriptive \(T_C-T_S\), not a 20% advantage test.
This is a preserved design finding, not a failed executed experiment.

All new statistical proofs and illustrative arithmetic are manual.

These statements describe source-author construction and its supplied-context
challenges, not later independent review or its separate checks. No machine
proof, independent source audit or completed benchmark is asserted by public
preparation. Private review/check records retain their own scope.

This is one separate synthetic application design with one candidate and
three fixed references. Raw-observation cost superiority is analytically
rejected; any later pass could establish only the specified synthetic
operating-point conformance. The fixed core/stress split, inference family,
cost accounting, fresh independent held-out controls and failure rules remain
unchanged. No implementation, generation, sampling, interval evaluation,
calibration or execution is authorized by this document. Existing native
numerical designs and frozen protocols are unchanged, and RET remains paused.

Private source labels, exact source/check correspondence, source fingerprints,
review/freeze records, raw administrative receipts and reader/checker scripts
are intentionally withheld. Public links state mathematical dependencies;
they do not provide private custody or original certificate reproduction.
This edition is a design manuscript, not an executable installation or an
independently replayable custody package. See the
[application publication note](PUBLICATION_NOTE.md) and
[public evidence policy](../../coordination/REDACTED_PUBLICATION.md).
