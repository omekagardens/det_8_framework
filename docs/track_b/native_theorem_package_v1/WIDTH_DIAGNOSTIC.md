# D4-A: one-birth width diagnostic in simulated finite growth

18 October 2026. Design and manual probability bound only. No sampling,
coefficient acquisition, numerical run or physical observation.

Public design edition: 20 October 2026. The interrupted draft and its
original provenance are retained privately. The [publication note](PUBLICATION_NOTE.md)
records review scope and evidence limits.

**Scope.** This benchmark tests one declared simulated growth comparison.
It connects the accepted one-birth width gain to an explicit observation
channel and a finite-sample decision. It is not an empirical DET channel,
a physical prediction, or validation of the ontology. Its current operational
disposition is ABSTAIN / NOT RUN: no numerical lower effect bound or executable
exact sampling interface is supplied by this design.

## 1. One comparison, fixed before observation

Use the [original admitted baseline B](THEOREM_PACKAGE.md#1-mathematical-object-and-admitted-model)
at lambda=1, with its common positive
parent-six scale rho. Use the admitted original normalized harmonic vector z,
with z1=1, every z_j nonzero and |z_j|<=1. Fix epsilon=1/4.

Every trial starts afresh at the same six-element poset

    P*=C3 ordinal-sum A3,

with all six record bits zero. Its width is three.
Do not sample a trajectory and retain only visits to this parent.

The baseline arm draws one birth using the COMPLETE baseline row:
an ideal S of P*, followed by its fair newborn bit.
The perturbed arm uses the complete row

    q_Q(P*,0,S)=q_B(P*,0,S)*h7([P*+S]),
    h7(T_j)=1+z_j/4 on the eleven admitted classes,
    h7=1 on other seven-order classes.

Both arms retain every ideal, full births and both fair newborn bits.
The admitted harmonicity and h7>=3/4 establish normalization and positivity.
No conditioning on supported children, proper births, width gain or record
outcome is allowed. There is no parameter search over lambda, epsilon,
the initial parent or the harmonic direction.

The accepted full-row identity gives

    Delta=E_Q[width]-E_B[width]
         =rho*U0/4>0, U0=a*g0^3/b0^3>0.                (D1)

The original held coefficients and rho remain those of B.
Their numerical values are not acquired here. The lambda-dependent seed
theorem motivates a broader mathematical family, but this benchmark chooses
only its original lambda=1 member.

## 2. The observation channel

Each draw emits the complete unmarked seven-element order after one birth.
The declared channel computes its exact maximum antichain size W and reports

    Y=W-3.

Appending one maximal vertex cannot destroy an old antichain and can increase
width by at most one. Therefore W is exactly 3 or 4 and Y is Bernoulli.
The record bit and scalar-passive payload are not observed by this channel;
discarding them does not discard any birth outcome.

An exact specialized decoder is available: P* has a unique three-element
antichain, its three caps. A four-antichain after the birth exists exactly
when the newborn is incomparable with all three caps. Thus three declared
order comparisons suffice. This is an observation of the emitted poset,
not an estimator using the desired expected gain.

The channel assumes access to the complete simulated order and the known
initial-parent embedding. No missing edges, record thinning, noisy detector,
unknown coarse-graining or real-world measurement interpretation is included.
Changing that channel requires a separate analysis.

## 3. Held-out draws and statistic

After the candidate laws, channel, lower bound and sample size are frozen,
reserve n independent draws from each arm. These 2n draws are independent of
all calibration, debugging or law-selection data and of one another.
Use distinct predeclared independent streams; common-random-number coupling
is not part of this protocol.

Let Y_Qi,Y_Bi be the outputs. The sole statistic is

    Dhat=(sum_i Y_Qi-sum_i Y_Bi)/n
        =mean observed width_Q-mean observed width_B.   (D2)

The sample size is fixed before any held-out result is viewed.
Analyze once after both complete batches. No optional stopping, favorable
seed selection, retries until success, dropped outcomes, or extra comparisons
are covered by the guarantee. Preserve the complete draw accounting and the
sampling/channel versions for an independent consumer.

## 4. Effect-size premise and finite-sample guarantee

Declare a certified numerical lower bound d with

    0<d<=Delta,

independently of the held-out data. Freeze false-positive and false-negative
budgets alpha=beta=1/20. Define

    n=ceiling(4*log(20)/d^2).                             (D3)

Here log denotes the natural logarithm.

More draws may be chosen in advance, but not after seeing the result.
The competing statistical regions are

    H0: Delta<=0
    H1: Delta>=d.

Certification of d concerns the declared-law alternative, not estimated
held-out outcomes. H0 is the no-gain comparator for the statistical rule,
not another prediction of the declared laws. The error bounds below apply
to independent Bernoulli data in these respective regions; faithful sampling
of the declared laws with the certified bound places the run in H1.

No guarantee distinguishes effects in the gap 0<Delta<d.

Here is a manual bound, requiring only independence and Y in {0,1}.
For a Bernoulli Y, put psi(s)=log E exp(s*(Y-EY)).
Its exponentially tilted variance is psi''(s)=p_s*(1-p_s)<=1/4,
and psi(0)=psi'(0)=0. Integrating gives psi(s)<=s^2/8.
Applying this to the 2n signed summands of Dhat yields

    E exp(s*(Dhat-Delta)) <= exp(s^2/(4n)).

Markov's inequality, minimized at s=2*n*t, gives both tails

    P(Dhat-Delta>=t)<=exp(-n*t^2)
    P(Delta-Dhat>=t)<=exp(-n*t^2), t>0.                 (D4)

Consequently the threshold d/2 has

    sup_(Delta<=0) P(Dhat>=d/2) <= exp(-n*d^2/4)<=1/20
    sup_(Delta>=d) P(Dhat<d/2)  <= exp(-n*d^2/4)<=1/20. (D5)

These are finite-sample guarantees, not normal approximations or asymptotic
standard-error claims. They are conditional on the sampling and observation
premises. A biased sampler, dependent draws or wrong channel is not covered
by these probabilities.

## 5. Closed PASS / FAIL / ABSTAIN rule

Before acquiring held-out draws, verify the following preconditions:

- The two complete normalized laws are the frozen laws in section 1.
- An exact sampling interface for those laws and independent resets exists.
- The exact width channel is used, without filtering or missing draws.
- A numerical d>0 certified to satisfy d<=Delta is supplied independently.
- n is frozen according to (D3), fits the declared budget, and no held-out
  outcomes were used in selecting any preceding item.

If any item is unavailable or violated, report ABSTAIN with the actual reason.
Do not substitute an estimated d from the same held-out samples.
An interrupted/incomplete batch, sampler failure, channel failure or violated
independence assumption also produces ABSTAIN, not a mathematical failure.

If every item holds and both full batches complete:

    PASS iff Dhat>=d/2.
    FAIL iff Dhat<d/2.

There is exactly one terminal outcome. PASS means the predeclared simulation
contrast passed this test. FAIL means it did not; it is not a proof that
Delta<=0, nor a refutation of DET or the mathematical theorem.
Under the valid H1 premise, FAIL still has probability at most 5%.
A defect in the implementation or effect-bound premise is a different issue
from that sampling error.

The test can discriminate an implementation showing no gain from one
delivering at least d under its assumptions. It does not independently
establish that a simulator realizes its declared law.

## 6. What symbolic positivity does and does not supply

Equation (D1) proves the exact effect is positive. For that actual effect,
some finite sample size could meet specified error budgets.
It does not provide a numerical d, and thus does not instantiate (D3).
The formula is also highly sensitive to a small d through its inverse square.

Knowing only Delta>0 cannot certify a chosen numerical n with the stated
power from (D4): effects may be smaller than the resolution justified by
that sample size. An upper bound on a factor is not the needed lower bound.
Likewise a lower bound on h7 positivity does not bound the width effect
rho*U0/4 from below.

This is the precise missing effect-size premise, not an obligation to launch
another coefficient investigation. The symbolic design and guarantee are
complete without it. No numerical n, simulated result or empirical power is
claimed. The present uninstantiated benchmark remains ABSTAIN / NOT RUN.

## 7. Computational and oracle cost

Conditional on an available exact sampler, the benchmark requires exactly
2n one-birth samples, each selecting among the eleven individual ideals
of P* and drawing a fair newborn bit. It requires at most 6n cap-comparability
checks for the specialized width channel and O(n) counting operations.
The statistic uses O(1) counters, requiring O(log n) bits of working memory;
retaining all auditable draw records requires O(n) records of storage.

Building and validating the exact law oracle is a separate input cost.
The baseline target row has eleven positive probabilities; the perturbation
uses its corresponding shared h7 multipliers. Producing those probabilities
may depend on the original global normalization prescription. This design
does not price that work as a cheap local lookup or assume that the unknown
normalization has already been evaluated.

Write C_build for that independently established preparation cost and
C_draw for the cost per exact draw. The run cost is
C_build+2n*C_draw+O(n) channel/counting work, plus audit storage.
If the oracle is approximate, its distributional error needs a separately
proved allowance before these guarantees can be used. No such allowance,
sampler implementation or numerical runtime is supplied here.

## 8. Interpretation boundary and completion

This is one application/simulation diagnostic with an explicit observation
channel, complete outcome accounting, independent held-out data, bounded
error probabilities, oracle-cost accounting and a closed decision rule.
Its symbolically positive effect is not an observed result.

It does not assert sustained width growth, an h8 lift, transfer of the
30/33/38 exclusions, a physical record-to-geometry channel, informative quantum
measurement, or empirical DET/gravity validation. It neither depends on nor
alters any separately prepared observed-data replay.

The design uses the [accepted law-family supplement](LAW_FAMILY_SUPPLEMENT.md)
and its original-law member. No numerical coefficients, solver or sampling run
were used. The bounded symbolic design is complete; missing operational inputs
cause abstention. A numerical effect bound and sampler are separate deliverables,
not evidence already supplied by this design.
