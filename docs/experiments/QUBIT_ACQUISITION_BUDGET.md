# Qubit acquisition budget: when separated predictions are certified

14 September 2026 UTC. RI-28 is a conditional proof and acquisition-design
companion to the accepted [RI-25 experiment](qubit_record_v1/EXPERIMENT.md).
Its purpose is to turn the default run's overlapping phase-pair W bands into
an explicit planning question. It changes no accepted source, default plan,
record, estimator, confidence allocation or prior result. The tables below
are illustrative future designs, not a selected or executed experiment.

The main result is a sufficient fixed-sample condition for the two **random
frozen prediction bands** to be disjoint. It counts training uncertainty both
in the fitted center and in the interval around that center. It also exposes
a systematic-error/loss floor. Failure of this conservative certificate does
not prove that observed separation or a different design is impossible.

## 1. Reference laws and the scope of the premise

Keep all three RI-25 recipes, fresh X/Y/Z training preparations and separately
acquired W=(0,3/5,4/5) outcomes. With equal N attempts in each stratum there
are nine training and three held strata: **12N total attempted acquisitions**.
Retain every attempt, including erased outcomes. The retained sequential
controls are separate and are not part of this 12N tomography count.

For the two phase recipes, write p+ and p− for their reference-state W-plus
probabilities. Supply a lower bound

\[
p_+-p_-\ge\Delta>0.
\]

For the nominal reference states r±=(0,±3/5,0), these probabilities are
17/25 and 8/25, giving Δ=9/25=0.36. This is a **reference-state premise**,
not measured ground truth or an outcome of tomography. A per-trial drift
bound relative to an unknown reference state does not establish this gap.
If separately justified reference-state bounds give trace distances at most
δ+ and δ− from the two nominal states, the effect inequality gives the valid
lower gap Δ=9/25−δ+−δ−, provided it is positive. Those reference errors are
different from the per-trial drift budgets already in RI-25. Uncertain
reference guarantees require their own failure-probability accounting.

All statements retain RI-25's binary-read-then-erasure law, independently
sampled underlying binary results within each fixed stratum, comparable
preparations, stated measurement frame and justified average per-trial
calibration/drift bounds. Erasure may depend on the outcome. Independence
between distinct strata is unnecessary for the union bound.

## 2. From training records to separated frozen bands

For recipe a∈{+,−} and training axis k, define

\[
\ell_{a,k}=n_{0,a,k}/N,\qquad
\eta_{a,k}=\epsilon_{T,a,k}+c_{T,a,k}+d_{T,a,k}+\ell_{a,k}/2,
\]

\[
h_a=\tfrac35\eta_{a,Y}+\tfrac45\eta_{a,Z},\qquad
\widehat p_a=\frac{1+(3/5)m_{a,Y}+(4/5)m_{a,Z}}2,
\qquad g_a=c_{W,a}+d_{W,a}+\epsilon_{W,a}.
\]

On the simultaneous training concentration event E_T, RI-25 gives
|r_k−m_k|≤2η_k and hence

\[
|\widehat p_a-p_a|\le h_a.
\]

The reference state then supplies a witness that the compatibility set is
nonempty. The empirical full midpoint may still be nonphysical; this
argument needs no reported physical point estimate or repaired estimator.
The implemented frozen completed-frequency band B_a is the ideal interval
expanded by future calibration/drift and held sampling, with intersection
with [0,1] after each step. For this feasible case its endpoints are

\[
B_a=[\max(0,\widehat p_a-h_a-g_a),\;
     \min(1,\widehat p_a+h_a+g_a)].
\]

**Separation proposition.** On E_T,

\[
\inf B_+-\sup B_-
\ge\Delta-2(h_++h_-)-(g_++g_-).
\tag{1}
\]

Consequently Δ>2(h++h−)+(g++g−) is sufficient for strict, ordered separation.
Proof: the lower positive-recipe endpoint before clipping is at least
p+−2h+−g+, and the upper negative-recipe endpoint is at most p−+2h−+g−.
Subtract. Clipping can only raise the first lower endpoint and lower the
second upper endpoint. Equality allows touching closed intervals and does
not certify separation. For an actual completed fit, compare its actual
endpoints directly; failure of this uniform design bound need not prevent
a particular observed fit from separating.

For planning, replace each realized training loss fraction by a declared
upper ceiling L_{T,a,k}. The resulting H_a≥h_a gives the sufficient condition

\[
\Delta>2(H_++H_-)+(g_++g_-)
\quad\text{whenever every required loss ceiling is met.}
\tag{2}
\]

The extra training term cannot be omitted. A physical counterexample has
reference Bloch vectors r±=(0,±1/2,0), empirical midpoints
m±=(0,±5/14,∓1/7), ηY=ηZ=1/14, h±=1/10 and g±=1/50.
Both reference and empirical vectors lie in the Bloch ball, and the
coordinate bounds hold. Reference W probabilities are 0.65 and 0.35;
fitted centers are 0.55 and 0.45. The bands are [0.43,0.67] and [0.33,0.57],
which overlap despite Δ=0.30>2(h+g)=0.24. Treating nominal probabilities as
fixed fitted centers would give an invalid guarantee.

## 3. Distinct aims for held observations

Let f_a be the underlying completed W-plus frequency, and let
C_a=[n+/N,(n++n0)/N] be the **observable completion interval**. Its width is
the held loss fraction ℓW,a; f_a∈C_a pathwise. On the held concentration
event E_W, |f_a−p_a|≤g_a. Every endpoint of C_a is within ℓW,a of f_a.
Thus held loss affects what the observer can resolve even though it does
not widen the frozen B_a in RI-25's algorithm.

On E_T∩E_W and declared loss ceilings, the following are sufficient:

| Desired conclusion | Strict sufficient condition |
|---|---|
| Frozen bands B+ and B− are disjoint | Δ>2(H++H−)+g++g−. |
| Observed completion intervals C+ and C− are disjoint | Δ>g++g−+LW,++LW,−. |
| C+ excludes the negative-recipe frozen band | Δ>2H−+g++g−+LW,+. |
| C− excludes the positive-recipe frozen band | Δ>2H++g++g−+LW,−. |

For example, inf C+≥p+−g+−LW,+ and sup B−≤p−+2H−+g−,
which proves the third row; the other rows follow by the same endpoint
subtraction. These conclusions do not identify an unknown recipe, supply
a classifier or establish model truth. In the accepted scoring contract,
a recipe's own completion interval overlapping its frozen band means
compatibility, not validation. All-erased held data give C=[0,1] and remain
uninformative even if the two frozen bands are disjoint.

With common H and g, the three distinct sufficient thresholds are 4H+2g
for band separation, 2g+2LW for completion separation and 2H+2g+LW for
excluding the other band in both directions. Pick and freeze the intended
question; these are not interchangeable success criteria.

## 4. Explicit equal-count designs and the systematic floor

To preserve the existing schedule, keep αtrain=αscore=1/100. Assign
αtrain/9 to every training stratum and αscore/3 to each held stratum before
acquisition. For common positive εT=εW=e, Hoeffding's two-sided bounded-variable
inequality and a union bound require

\[
2\exp(-2Ne^2)\le1/900
\]

for training; this also meets the less stringent held requirement 1/300.
The independent, possibly nonidentically distributed bounded-read result
comes from [Hoeffding's original paper](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).
RI-25's unchanged `tail_certificate` instead certifies it by a finite
positive exponential sum S64(x)≤exp(x), with S64(x)/900≥2.

An explicit sufficient count without a floating-log decision is

\[
N=\left\lceil\frac{15}{4e^2}\right\rceil.
\tag{3}
\]

Indeed x=2Ne²≥15/2, and exact rational summation gives
S32(15/2)>1800. Positive terms and monotonicity imply
S64(x)≥S32(15/2)>1800. The integer part of this S32 value is 1808.
This proves a convenient conservative count, not an optimal sample size.

For equal training loss ceilings LT and the original supplied budgets
cT=dT=cW=dW=1/100,

\[
H=\frac75(e+\tfrac1{50}+L_T/2),\quad g=e+\tfrac1{50},\qquad
4H+2g=\frac{38}{5}e+\frac{19}{125}+\frac{14}{5}L_T.
\tag{4}
\]

At nominal Δ=9/25, a positive-e certificate requires LT<13/175≈0.074286.
At LT=0, require e<13/475; at LT=1/20, require e<17/1900.
At LT=0.08, even e→0 leaves 0.376>0.36; at LT=0.10 it leaves 0.432.
No N certifies this particular uniform criterion at those original
systematic budgets. This is a limitation of the conservative bound, not
an impossibility theorem for phase discrimination. Merely increasing N
while keeping the declared e=0.1 unchanged does not reduce that term.

The following common-budget examples all meet (2)–(3) for Δ=0.36.
They impose training loss ceilings; a held-resolution objective additionally
needs the separate LW conditions in section 3.

| LT | Each of cT,dT,cW,dW | e | N per stratum | 12N attempts | 4H+2g | Δ−(4H+2g) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.01 | 1/40 | 6,000 | 72,000 | 0.342 | 0.018 |
| 0.01 | 0.01 | 1/50 | 9,375 | 112,500 | 0.332 | 0.028 |
| 0.05 | 0.01 | 1/125 | 58,594 | 703,128 | 0.3528 | 0.0072 |
| 0.10 | 0.001 | 1/125 | 58,594 | 703,128 | 0.356 | 0.004 |

The last row assumes independently justified calibration/drift bounds ten
times smaller; more data do not supply that improvement automatically.
Reference-state uncertainty δ++δ− consumes the displayed gap slack. For
example, δ+=δ−=0.01 invalidates the first row's nominal-gap certificate,
while the second retains 0.008 of slack. Those δ values themselves would
need evidence. Actual acquisition duration, reference stability, reset and
calibration overhead are absent from 12N; a longer run can invalidate a
previously justified drift window. No hardware runtime, price or power to
achieve these loss caps is estimated.

## 5. Probability, refusal and preregistration

Under the declared sampling premises P(E_T^c)≤0.01 and
P((E_T∩E_W)^c)≤0.02. The first proposition uses E_T alone; E_W is needed
for claims involving actual completed W frequencies or intervals. If A is
the event that the frozen loss ceilings are met, (2) establishes

\[
\Pr(A\ \text{and frozen-band separation fails})\le0.01.
\]

It does **not** automatically establish a 99% conditional guarantee given A.
Without an erasure-frequency model or another justified guarantee of A,
there is no lower bound on the chance of an informative run. If a separate
argument bounds P(A^c)≤β, then P(A∩E_T)≥1−β−0.01; this still depends on
the supplied reference gap and systematic assumptions. Estimated rather
than deterministic calibration/reference guarantees need additional failure
allocations. RI-25's code does not estimate or allocate those extra risks.

Freeze N, settings, recipes, error budgets, caps, intended comparison and
failure handling before acquiring outcomes. Reaching a cap violation makes
this planned separation certificate inconclusive while retaining every
scheduled attempt and the ordinary compatibility analysis where valid.
Do not replace lost shots, exclude unfavorable runs, normalize by detected
shots, change the target W, or keep collecting until intervals separate.
Any sequential/stopping design requires its own valid statistical contract.

RI-25's `ExperimentPlan` can express new N/e/current-budget values, but its
fingerprint does **not** include loss ceilings, the reference-gap premise,
these separation rules or added calibration-failure allocations. A future
acquisition must bind those choices in a separately hashed preregistration
artifact alongside the new plan and unchanged source identities. This note
is a planning analysis, not that experiment-specific preregistration.
Changing the number of recipes, strata or settings needs a different
schedule and allocation; dropping the mixed control invalidates the 12N
accounting quoted here.

A suitable measured source is still required by the
[data-readiness contract](../coordination/QUBIT_DATA_AND_FOLLOWUP.md).
Conventional tomography receives the same records, missing-data treatment,
budgets and comparison rule. These certificates give no DET sample-efficiency
or accuracy advantage. The original RI-25 simulation, its overlapping default
bands and all accepted file identities remain unchanged.

## 6. Review and arithmetic evidence

Independent mathematical and experimental-design reviews checked the center
factor, systematic floor, fixed-sample allocation, loss/refusal semantics,
reference-gap premise and separate preregistration requirement. A standalone
coordinator Fraction-only audit passed 617 assertions over the four exact
count/budget rows, positive-series certificate, physical inward-center
counterexample and endpoint bounds at an independent rational corner grid.
It imports no experiment source and runs no simulator, predecessor suite,
calibration bank or acquisition. The grid corroborates the displayed proofs;
it is not a substitute for them. No registered witness total changes.
