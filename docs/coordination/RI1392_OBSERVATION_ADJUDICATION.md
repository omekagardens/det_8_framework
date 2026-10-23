# RI1392 — Observation channels and five-lane adjudication

The coordinator accepts the conditional RI1391 observation-channel proposition after a distinct manual mathematical review. Independent fresh preparations permit a finite binary discriminator for two specified optional laws; one latent history retains a positive error floor, even with its entire history available. The proofs and operational assumptions are stated below. This is neither physical validation nor execution permission.

## Admitted law and observation-channel theorem

In the optional common-latent growth family, draw a latent parameter
\(\Theta\in[0,1]\). Conditional on \(\Theta=t\), all forward edges on the
birth-indexed vertices are independent Bernoulli(t); take transitive closure
and forget birth labels. An observer receives intrinsic, unmarked finite
orders, not the generating edge array. The indices below declare known
cardinality, not physical time. Native fair record bits and the passive
fixed-carrier PSD payload are not additional measured channels here.

Use the accepted pair
\[
 h(t)=70t^4-140t^3+90t^2-20t+1,\qquad \epsilon=1/642,\qquad
 d\mu_\sigma(t)=(1+\sigma\epsilon h(t))\,dt,\quad \sigma\in\{+1,-1\}.
 \tag{1}
\]
The input identities are
\[
 |h|\le321,\quad \int_0^1t^j h(t)\,dt=0\ (0\le j\le3),\quad
 \int_0^1t^4 h(t)\,dt=1/630.
 \tag{2}
\]
Thus the two densities are between 1/2 and 3/2, are normalized, and have
overlapping full support. These are exact accepted polynomial identities,
not numerical estimates made here. Their construction and admission are
optional mathematical choices, not laws selected uniquely by DET.

Let \(C_n\) be the total order with n vertices. Conditional on t, obtaining
\(C_n\) requires precisely the n-1 consecutive edges: a forward path between
consecutive vertices has no intermediate vertex. Once these edges occur,
all other pairs are ordered regardless of the other edges. Hence
\[
 \Pr(C_n\mid t)=t^{n-1},\qquad
 a_\sigma:=\Pr_{\mu_\sigma}(C_5)=1/5+\sigma d,\quad
 d=\epsilon/630,\quad \Delta=a_+-a_-=2d=\epsilon/315.
 \tag{3}
\]
Size five is a specified distinguishing readout, not a claim of minimality.

## 2. Proposition: the preparation channel changes the inference

For the two fixed hypotheses in (1):

**A. Independent preparations.** If each of k trials independently redraws
its latent variable from the same unknown \(\mu_\sigma\), independently grows
a fresh order from empty to exactly five vertices, and faithfully reports
whether the completed unmarked order is \(C_5\), there is a test whose two
conditional error probabilities are each at most
\[
 \exp(-2kd^2)=\exp(-k\Delta^2/2).
 \tag{4}
\]
In particular, for a predeclared \(\alpha\in(0,1)\),
\[
 k\ \ge\ \left\lceil\frac{\log(1/\alpha)}{2d^2}\right\rceil
 \tag{5}
\]
suffices for each error to be at most alpha.

**B. One entire history.** If there is only one latent draw and all
observations are obtained through a common hypothesis-independent channel
from that latent variable, then even observation of the entire infinite
growth history cannot make both errors tend to zero. For every possibly
randomized binary test,
\[
 \Pr_-(\text{choose }+)+\Pr_+(\text{choose }-)
 \ \ge\ 1-\epsilon\int_0^1|h(t)|\,dt\ \ge\ 1/2.
 \tag{6}
\]
Consequently the larger conditional error and the equal-prior average
error are each at least 1/4. These conservative bounds do not assert that
the output laws are identical or that the optimal error equals 1/4.

## 3. Proof and specification of channel A

Fix k before acquiring observations. For trial i, independently sample
\(\Theta_i\sim\mu_\sigma\), then independently generate all its conditional
forward edges on five vertices. Fresh trial randomness is independent
between trials; the hypothesis sigma is fixed across the experiment.
Report \(B_i=1\) exactly when the resulting completed unmarked order is a
chain, otherwise report zero. The observer may receive the whole
unmarked five-vertex order and compute this bit, or receive a faithful
binary oracle for the same predicate. Both descriptions require known
true size five. There is no thinning, missing-vertex, unknown-size or
comparison-error channel in this proposition.

Integrating out the independently redrawn parameters gives independent
Bernoulli variables \(B_i\) with common mean \(a_\sigma\) in (3). Choose plus
when \(\overline B\ge1/5\), and minus otherwise.

For completeness, the concentration estimate is derived here. For
\(B\sim\mathrm{Bernoulli}(a)\), put
\[
 \psi(s)=\log\mathbb E e^{s(B-a)}.
\]
Then \(\psi(0)=\psi'(0)=0\) and
\[
 \psi''(s)=r_s(1-r_s)\le1/4,\qquad
 r_s=\frac{ae^s}{1-a+ae^s}.
\]
Taylor's integral formula yields \(\psi(s)\le s^2/8\) for all real s.
Independence therefore gives
\[
 \mathbb E e^{s\sum_i(B_i-a)}\le e^{ks^2/8}.
\]
For the upper tail, exponential Markov with \(s=4d\) yields
\[
 \Pr(\overline B-a\ge d)\le e^{-4kd^2+2kd^2}=e^{-2kd^2}.
\]
Using \(s=-4d\) gives the same bound for
\(\Pr(\overline B-a\le-d)\). Under minus, an error is the upper-tail
event; under plus, an error is a subset of the lower-tail event. This
proves (4); rearranging it proves (5), including the declared tie rule.

No numerical sample-size evaluation, simulation, efficiency claim or
estimator benchmark is needed for this existence bound. In particular,
multiple prefixes of one history are not the independent trials in this
proof. Its independent redraw premise is load-bearing.

## 4. Proof and specification of channel B

Draw \(\Theta\sim\mu_\sigma\) only once. Conditional on t, generate one
countable independent forward-edge array and its growing order history.
A strong declared readout supplies the unmarked isomorphism class of
the completed prefix at every known cardinality \(n=1,2,\ldots\).
Its output space is the countable product of finite order-class spaces,
with the sigma-field generated by cylinder events. Every finite prefix
is a measurable function of finitely many edges, so this defines a
measurable probability kernel \(K(t,\cdot)\). Any further common
hypothesis-blind randomization or readout can be included in K.
Indeed the argument below even allows the stronger oracle revealing t
itself; no claim that t is recoverable from the unmarked history is needed.

Crucially, the conditional channel K is the same under both hypotheses:
the hypotheses differ only in their mixing distribution. The observer
does not receive sigma, the exact distribution law, numerical
hypothesis-dependent native transition weights, or any other
law-encoded oracle. Such information would be a different channel.

Write the output laws as
\[
 P_\sigma(A)=\int_0^1 K(t,A)(1+\sigma\epsilon h(t))\,dt.
 \tag{7}
\]
For a randomized test let \(f(y)\in[0,1]\) be its probability of choosing
plus at output y, and let \(g(t)=\int f(y)K(t,dy)\). Then \(0\le g\le1\).
Because \(\int h=0\), the positive and negative parts of h have equal
integral, so
\[
 \left|\int_0^1g(t)h(t)\,dt\right|
 \le \tfrac12\int_0^1|h(t)|\,dt.
\]
It follows directly, without an ergodic assumption, that
\[
 |\mathbb E_+f-\mathbb E_-f|
 \le \epsilon\int_0^1|h(t)|\,dt
 =\operatorname{TV}(\mu_+,\mu_-)\le1/2.
 \tag{8}
\]
Here \(\operatorname{TV}(P,Q)=\sup_A|P(A)-Q(A)|\); the displayed equality
is its density formula. Taking indicator tests also proves the
data-processing inequality
\(\operatorname{TV}(P_+,P_-)\le\operatorname{TV}(\mu_+,\mu_-)\).

The sum of the two errors is
\[
 \mathbb E_- f+\mathbb E_+(1-f)
 =1-(\mathbb E_+f-\mathbb E_-f),
\]
which proves (6). Equivalently the latent overlap is
\(\int\min(1+\epsilon h,1-\epsilon h)=1-\epsilon\int|h|\ge1/2\);
a common channel cannot remove it. Positive densities also imply
mutual absolute continuity of the two output laws, but the quantitative
bound, not absolute continuity alone, supplies the uniform error floor.

Every finite-prefix test is a test on the full history that ignores the
remaining output. Thus (6) holds uniformly for every prefix size and
every sequence of such tests, including common adaptive stopping and
postprocessing rules. It precludes asymptotically vanishing errors for
this fixed pair. Infinite conditional edge draws at one t are not
independent redraws of t. Even perfect inference of that single t would
not identify which overlapping mixing distribution produced it.
There can still be nonzero discriminating information: the size-five
chain event already has the positive difference in (3).

## 5. Three different information regimes

Exact law access means knowing ensemble probabilities
\(\Pr_\mu(C_n)=\int t^{n-1}d\mu(t)\) at every known size. The accepted
RI1389 result says these moments uniquely specify the mixing measure
on [0,1]. It is a statement about exact laws, not the content of one
sample path.

Channel A supplies independent preparations and proves only the finite
binary discrimination result above for the fixed pair. It does not
reconstruct arbitrary mixing measures or promote a physical experiment.

Channel B supplies arbitrarily much conditional history for just one
latent draw. Its failure of consistent discrimination does not contradict
exact-law identifiability: the two regimes provide different information.

## Conditional scope and provenance

The mathematical model admits positive normalized ideal rows, whole unmarked-parent access with precursor-restricted marks, transported equivariance, fair immutable newborn bits and complete unnormalized marked diamonds on an arbitrary fixed-carrier positive-semidefinite payload. These are declared optional-model premises. No theorem here selects a unique DET law or establishes physical geometry, gravity, mass, clock, energy, a native forward map or an application advantage. Known cardinality is not physical time.

Channel A requires genuine from-empty preparations, independent latent redraws and conditional randomness, a fixed hypothesis, known true size five and a faithful completed-order or chain-bit readout. Native admission supplies no reset, preparation, fidelity or physical-readout certificate. Thinning, missing vertices, unknown size and erroneous comparisons are excluded. Channel B requires one latent draw and a common measurable hypothesis-blind channel. Its error bounds concern measurable binary decisions, including finite-prefix or common adaptive postprocessing that yields such a decision. Error conditioned on abstention, or a procedure that never terminates, needs separate coverage/termination accounting. The lower bound is conservative; it does not say the two output laws are identical or that the optimal error is exactly one quarter.

The accepted polynomial pair was previously present in a coordinator-captured RI1389 draft. That original author's missing SOURCE_PINS, RESULT and FREEZE artifacts remain missing. RI1391 is a complete later author package with its own current source and output inventory, followed by a distinct reviewer and this coordinator disposition. Neither current identity nor this publication repairs the historical gap. Review exposure is disclosed; review was distinct, not blinded. Exact hashes establish present identity, not mathematics or historical custody. The current ten-package audit passed 161 administrative checks. In particular, the E review completed after the prior coordinator snapshot; its later completion is not retroactively inserted into that snapshot.

## Current dispositions and bounded successors

The following are coordinator decisions on actual frozen predecessors. Every named successor is an assignment awaiting its own distinct review and coordinator disposition. No successor result is accepted by this checkpoint.

| Lane | Accepted result or required repair | Actual blocker and next bounded deliverable |
| --- | --- | --- |
| Native geometry / QR | RI1391's conditional two-channel proposition above is accepted. Exact ensemble-law access, independent preparations and one history remain distinct regimes. | RI1393 is assigned a common noisy binary-readout calibration proposition: known response, shared unknown response and separate competing nuisance choices must be distinguished. It must test robust separation versus aliasing; a nonzero slope alone does not settle an unknown offset. Physical preparation/readout remains absent. |
| Relational State | E-C006's conditional common restoration signature and complete source-ledger requirements are accepted. The model's full-cycle comparison remains underdetermined. | E-C007 is assigned a within-attempt baseline/candidate representation audit. It must identify an actual finite operation/information distinction or the exact missing algorithm definitions, without weakening the baseline's 32-sample history and persistent prior/covariance across retry. A physical/common reset module and competence certificate remain absent. |
| Energy | NE-C006 repairs the row-to-record argument using one explicit common iid process pair; its forced-binary and abstention distinctions are accepted. | NE-C007 is assigned a conditional finite-catalogue preparation/readout error-budget proposition at the accepted within-K scope. Independent non-target calibration and physical preparation, terminal readout, structural command, shared-response/support, validity/selection and finite-data premises remain open. |
| Computing Efficiency | CE-S003 needs exact resource/count corrections and fatal-resource-stop propagation. No runtime correctness or verification result is accepted. | CE-S004 is assigned an inert repair and manual exception-path traces. A concrete reviewed enforcing runner, exact runtime/source identity and all execution gates remain required. Benchmark/M1 execution is not admitted. |
| Measurement / public data | The five captured declarations and reported linker identity are accepted only as prospective documentary evidence. | A separate author is assigned one inert conditional native-C R1 own-task resident-size component and interface/effects contract. Actual ownership/lifetime, build inputs and binary identity, active image/cache correspondence and same-invocation B1 binding remain HOLD. No build, launch, probe, contrast or new acquisition is granted. |

### Relational State: why full-cycle costs remain unresolved

The common service must give both arms the same versioned transition and sensing/actuator permissions, feedback family, fallback and termination rule. It may respond to their different realized states, but cannot choose privileged rules by arm identity. Every opened failure or abort, retry preparation and terminal restoration remains chargeable; terminal reset failure removes success credit. Source electricity is distinct from delivered heat, and each source branch is counted once. A nonduplicated work-equivalent debit for unfulfilled restoration cannot silently be set to zero or duplicate already paid restoration.

The within-attempt model does not specify chamber/reset dynamics, source coefficients, latent regeneration or finite-time reachability. Completions that agree during every stated attempt can still differ in whether reset succeeds and what it costs. The accepted result is this missing-premise finding and a candidate common-module interface, not a runnable physical service, measured gain or universal thermodynamic impossibility. Quality, reliability, held-out evaluation, competence, full source-to-reset accounting and the accepted retry policy remain required.

### Energy: the corrected record-law conclusion

At the declared countermodel response rho=4 with zero increment errors, the two nominal command phases are 4pi and 6pi. Both cosines are one, giving the same normalized row (13,7,10,10,10,10,10,10)/80. A fixed schedule, a common iid sampler of this row and deterministic or common candidate-independent labels/timestamps give one identical complete record law under the two hypotheses. Equal rows alone would not imply equality of every possible temporally dependent record law.

For this explicit common law, a possibly randomized forced binary rule chooses the first candidate with a common probability t, so the two opposite errors sum to t+(1-t)=1. With abstention probability a, the wrong-label probabilities instead sum to 1-a. Always abstaining supplies no identification. One admissible indistinguishable pair defeats a uniform guarantee over the unqualified class. Since rho=4 is outside the hypothetical K=[1,3], this does not contradict the accepted conditional within-K separation result. Excluding that witness alone does not supply the missing physical/calibration premises, and target outcomes cannot calibrate their own interpretation. No clock, action scale or work store is supplied.

### Computing Efficiency: the exact required correction

The C15 negative input is 33,347 bytes, while the retained stdout protocol limit remains 33,346. There are 22 named cases, including eight C20 malformed-wire subchecks; 40 _eq/_rejects calls occur only on the complete no-exception path. The previous figure 29 is a case/subcase counting convention, not an assertion count. A case's first failure can prevent its later checks, so a failure report cannot claim every call executed.

The harness's broad Exception handler can consume MemoryError or TimeoutError and continue to later cases. Designated fatal resource stops must propagate, while ordinary bounded diagnostic failures may retain their proposed finite FAIL-row behavior. A concrete enforcing runner is still absent. CPU, wall-time, resident-memory and output caps may not be weakened or replaced by periodic resident polling. All these findings come from inert-source review and manual traces; no source parse, import, compile, harness run or benchmark was performed for this adjudication.

### Measurement: conditional source design without a runtime grant

The documentary acquisition stopped before hashing a reported 290,664,032-byte compiler because the read cap was 268,435,456 bytes. That acquisition boundary is exhausted and is not enlarged. Header accessor/type and selected-address/object-UUID declarations do not establish borrowed-right lifetime, active-cache correspondence or runtime applicability. The reported linker hash remains a prospective static identity, not source-to-build or invocation equivalence.

The new R1-only inert component must explicitly assume a valid initialized own-task accessor/right with borrowed lifetime, reset the native TASK_BASIC_INFO count for each call, require success with the exact native returned count, and use checked resident-size conversion/serialization. Missing or invalid status/count/units are errors, never a successful zero. No other-task right, deallocation, hard-coded ABI size or guessed API is admitted. Existing frozen declaration captures may support the text; no new live SDK/binary acquisition is needed or authorized. The source design is not an integrated qualification helper or B1 implementation. Build, launch and contrast remain gated on actual ownership, exact build/source identity and same-invocation binding.

The accepted prospective GWOSC replay remains complete and is not repeated. Measurement follow-up remains separate from full production qualification and from a physical native prediction. Historical acquisition exceptions and identity failures are preserved. RET remains paused. Five parallel lanes share the current capacity guard, protected-validation rules, separate author/reviewer roles and scoped publication requirements; no result in one lane validates another lane's assumptions or the physical theory.
