# RI-25 — ordinary qubits, retained records and withheld predictions

14 September 2026 UTC. **Conditional mathematical model and isolated synthetic
experiment; physical validation and strict DET derivation are not claimed.**
This implements the [approved interface](../../../REVIEW_IMPLEMENTATION_PLAN.md)
without changing any accepted predecessor source or registering another suite.
Review and publication status are recorded in the
[QR handoff](../../coordination/QR_HANDOFF.md).

## 1. Object and adopted premises

The working chain is a physical-model snapshot → conditional outcome law →
actual attempted acquisition → retained classical record → observer's declared
training/withheld access. A state is not an already observed outcome; a record
is not the full state. “Missing” does not mean no interaction occurred.

We explicitly adopt a complex two-dimensional Hilbert space, trace-one states
ρ=(I+r·σ)/2 with ||r||₂≤1, Born probabilities, available projective X/Y/Z and
W=(0,3/5,4/5), and the selective/nonselective Lüders instruments below. These
are physical-model premises, not conclusions from DET primitives. The frame
and calibration labels identify a supplied contract; they do not establish
that an apparatus realizes it. All executable arithmetic uses integers and
exact rational numbers, not floating-point tolerance as proof.

For a unit axis n and outcome a∈{−1,+1},

\[
Q_{n,a}=(I+a n\cdot\sigma)/2,\qquad
p(a\mid\rho,n)=(1+a n\cdot r)/2.
\]

On a positive-probability selected branch, r↦a n. If an actual record has
probability zero in the supplied model, no selected update is defined: keep
the record and report model mismatch. The nonselective, deliberately
unconditioned instrument gives r↦(n·r)n. This known ensemble channel is **not**
used as a substitute for an erased serial outcome.

Nominal recipes, generator truth and inferred estimates have separate roles.
The default simulator truth is:

| Nominal recipe | Simulator r | X+ | Y+ | Z+ | Withheld W+ |
|---|---|---:|---:|---:|---:|
| phase_plus | (0,3/5,0) | 1/2 | 4/5 | 1/2 | 17/25 |
| phase_minus | (0,−3/5,0) | 1/2 | 1/5 | 1/2 | 8/25 |
| mixed | (1/3,−2/5,1/4) | 2/3 | 3/10 | 5/8 | 12/25 |

These vectors are generator inputs, not knowledge granted to inference by a
recipe name. The first two states demonstrate equal X/Z laws and different Y
and W laws exactly. W is fixed before acquisition and is never a fitting axis.

## 2. Explicit DET representation, without a normalization substitution

Let Zp=diag(1,−1), reserving it here for the Pauli matrix rather than the live
relational-configuration symbol Z. The accepted C0 section has
D(A,0)=diag(A,Zp A Zp). Define

\[
J_2(\rho)=D(\rho^T/2,0)=\frac14
\begin{pmatrix}
1+r_z&r_x+i r_y&0&0\\
r_x-i r_y&1-r_z&0&0\\
0&0&1+r_z&-r_x-i r_y\\
0&0&-r_x+i r_y&1-r_z
\end{pmatrix}.
\]

Then J2(ρ) is PSD, its trace and total-entry mass M(D)=1†D1 are one, and
Φ(D)=2Aᵀ gives ΦJ2(ρ)=ρ. The executable inverse checks the **entire** four-label
matrix against this image, including cross-block zeros and the lower block;
it does not discard out-of-image payload. The transpose is load-bearing:
ρ01=(rx−i ry)/2 but A01=(rx+i ry)/4. The RI-23 imaginary scalar on the original
two-label ρ is qI=1−ry=2p(Y−), not 2p(Y+).

The original trace-one ρ has total-entry mass **1+rx**, generally not one.
Thus ρ is not silently inserted into the unchanged
[RI-23](../../coordination/SCALAR_VALUE_ERROR_CONTRACT.md) mass-one domain.
The bounded observation here is the restricted effect
f(n,a)(D)=tr(Q(n,a)Φ(D)) on the J2 image. This does not evade RI-23's obstruction
to separating bounded effects on the whole raw PSD/mass domain; it explicitly
changes the operational domain.

For two states, transpose and unitary conjugation preserve singular values;
the two half-scaled diagonal blocks therefore give

\[
\|J_2(\rho)-J_2(\sigma)\|_1=\|\rho-\sigma\|_1
=\|r-s\|_2,\qquad T(\rho,\sigma)=\|r-s\|_2/2.
\]

Hence the trace-distance certificates below also hold in this C0 embedding.
No physical encoder or preparation of a four-cell native source is supplied.
Generic XYZ measurements do not implement L_t, its filters/couplers, or the
16-dimensional theorem in
[FINITE_RECORD_OBSERVABILITY](../../research/FINITE_RECORD_OBSERVABILITY.md).

## 3. Frozen acquisition and observer access

The plan fixes three recipe labels, 512 attempts per stratum, X/Y/Z training,
W held out, session/frame/calibration/provenance identities, and all error
budgets before any records. Training has K=9 strata, held scoring has three.
Every shot uses a fresh successful preparation comparable to its recipe's
unknown reference state. Independent underlying Bernoulli reads are assumed
within each fixed-size stratum; identical distributions are not required.
No independence between different strata is needed for the union bound.
Adaptive stopping, unexplained preparation failures and unknown acquisition
laws are not covered by this contract.

[inference.py](inference.py) imports neither the simulator nor its state module.
Its fit interface accepts only the frozen plan and training record tuple;
it refuses W records, extra/duplicate IDs, absent scheduled attempts, foreign
contexts and unsupported failures. It does not read truth vectors, seeds,
latent erased outcomes, nominal preparation formulas or held-out results.

[worked_example.py](worked_example.py) writes plan and training records, fits
and writes both full-XYZ and partial-XZ predictions, **then** generates W
records. Scoring consumes the same immutable fit output; it never refits or
uses W to change a budget. Its before/after prediction digest must agree.
Truth is audited separately after scoring. Tests change truth and withheld
data while holding the training observations fixed, and check this boundary.

Frozen Python objects and metadata strings are a trusted program/audit
contract, not authenticated provenance, a security sandbox or protection from
someone constructing a forged object. External prediction JSON is an export,
not an accepted deserialization/fit-certification API. The fit/score hashes
canonicalize records in ID order: they identify an order-invariant tomography
input, **not acquisition-order identity**. Raw JSONL keeps generation order;
the ordered commands, precursors and nominal per-setting trial indices remain.
There are no physical timestamps or clock claims. Both the protocol and a
future adapter must retain order rather than deriving it from a sorted hash.

## 4. Missingness, error budgets and deterministic guarantees

### Binary-read-then-erasure forward law

For a stratum let N=n+ + n− + n0, including every attempted shot. There is an
underlying binary result for each attempt, followed by erasure. Erasure may
depend on the result or vary between attempts; its selection need not be
independent. The completed, possibly inaccessible plus frequency f satisfies

\[
f\in[n_+/N,(n_++n_0)/N],\qquad
\widehat p=(n_++n_0/2)/N,\quad
|f-\widehat p|\le n_0/(2N).
\]

This is a pathwise counting statement, not a missing-at-random assumption.
The default simulator erases plus results with probability 1/20 and minus
results with probability 1/10. No detected-only denominator or inferred
replacement outcome is used. N=0 is refused. All-erased strata remain in the
record set and count as unobserved for point estimation. A failed acquisition
without this binary law or an unsuccessful/unknown preparation is retained
as a raw record but makes this inference refuse, not silently discard it.

### Sampling, calibration and preparation drift are different premises

Write p_j=tr(E_j ρ_j) for the underlying plus probability and p0=tr(Q ρref).
Supply deterministic calibration and drift bounds, separately for each
stratum, satisfying

\[
c\ge N^{-1}\sum_j\|E_j-Q\|_{op},\qquad
d\ge N^{-1}\sum_j T(\rho_j,\rho_{ref}).
\]

A separately justified bound on average absolute probability error can
replace the calibration norm condition. **The norm of the average effect
error is insufficient** when states and errors can covary. The displayed
conditions imply |N⁻¹Σp_j−p0|≤c+d by the trace/operator inequalities. If c,d
come from uncertain calibration instead of a deterministic premise, their
failure probabilities need extra allocation; the present code does not
estimate them from either training or W observations.

For fixed independent [0,1] reads,
Pr(|f−N⁻¹Σp_j|>ε)≤2exp(−2Nε²), using
[Hoeffding's bounded-variable inequality](https://www.tandfonline.com/doi/abs/10.1080/01621459.1963.10500830).
Freeze αtrain and K, then ε≥sqrt(log(2K/αtrain)/(2N)) suffices for simultaneous
training bounds. K is not recomputed from surviving groups. Here αtrain=1/100,
K=9 and ε=1/10 for N=512; the same allocation remains conservative when Y is
withheld from the partial-XZ fit. Each held stratum has αscore/3 with
αscore=1/100 and εW=1/10. Global allocations are positive and sum below one.

The program certifies this without a floating logarithm: set x=2Nε² and
S64=Σ(j=0..64)x^j/j!. Since S64≤exp(x), the exact rational comparison
S64·αstratum≥2 proves the required tail bound. A failed truncation certificate
means “not certified by this test,” not that a probability theorem is false.
The certificate is numerical accounting for an adopted sampling premise,
not evidence that real attempts were independent.

On the joint training event, the pathwise count bound and triangle inequality
give, for k=X,Y,Z,

\[
\eta_k=\epsilon_k+c_k+d_k+\frac{n_{0,k}}{2N_k},\quad
m_k=2\widehat p_k-1=\frac{n_{+,k}-n_{-,k}}{N_k},\quad
|r_k-m_k|\le 2\eta_k.
\]

The implementation uses equal supplied budgets ε=1/10 and c=d=1/100 for all
training strata, while keeping each stratum's actual erasure term separate.
Actual simulator calibration error and preparation drift are zero: the
nonzero supplied allowances are conservative, not measured uncertainties.

### Physical state, compatibility set and refused point estimate

Intersect each interval [mk−2ηk,mk+2ηk] with [−1,1]. An unmeasured coordinate
has interval [−1,1], reference midpoint zero and η=1/2; that zero is bookkeeping,
not an inferred coordinate. Let B be the resulting box and C=B∩{||r||₂≤1}.

**Feasibility theorem.** Let z select the point in each coordinate interval
nearest zero. C is nonempty iff ||z||₂≤1. Indeed each coordinate independently
minimizes its squared magnitude at z; every point in B has norm at least ||z||.
When feasible z itself is a physical witness. A witness is not a fit.

The reported point is m only if all three settings have at least one detected
result and ||m||₂≤1. Otherwise inference retains C and its prediction interval;
it does not project, clip or rescale m into an invented estimate. If C is empty,
the bounds/model are incompatible and no prediction is scored. Example:
X=[9/10,9/10], Y=[0,1], Z=[0,0] has a physical witness (9/10,0,0), but its box
center (9/10,1/2,0) has norm squared 53/50. Radial projection of that center
would even violate the exact X constraint. X,Y≥4/5 is infeasible because the
minimum norm squared is 32/25. These are exact regression counterexamples.

For a physical full midpoint, on the joint event,
T(ρref,ρm)²≤min(1,Σηk²). For arbitrary compatible states r,s,
T(ρr,ρs)²≤min(1,Σ(width_k)²/4). These are conservative bounds, not optimized
ball/box diameters. For unobserved Y, the code supplies two compatible opposite-Y
witnesses whenever there is rational interior room; they are alternatives,
not a default phase. For example exact X=3/5,Z=0 admits Y=±4/5 and W+
probabilities 37/50 and 13/50. X/Z records alone cannot select between them.

### Withheld W prediction and score

For any r∈C, pW=(1+(3/5)ry+(4/5)rz)/2 lies in the conservative interval

\[
I_{ideal}=[\widehat p_W-h,\widehat p_W+h]\cap[0,1],\quad
\widehat p_W=(1+(3/5)m_y+(4/5)m_z)/2,\quad
h=(3/5)\eta_y+(4/5)\eta_z.
\]

The reference center is not a point prediction unless a physical full point
was reported. Future W has its own cW=dW=1/100; expanding Iideal by cW+dW
bounds its average probability under those premises. Expanding again by the
**held sampling** εW=1/10 gives the frozen completed-frequency band. Sampling
error is not folded into an alleged physical state or apparatus probability.
All clipping is interval intersection with [0,1], not estimator repair.

Scoring forms the held completion interval [n+/N,(n++n0)/N]. Disjointness from
the frozen band is a model-or-budget mismatch. Overlap means compatibility,
not validation; all-erased W records are explicitly uninformative. The
training-plus-held sampling event has failure probability at most 2/100 under
the stated deterministic calibration/drift and sampling premises. This is
not a posterior probability of the model or an independence certificate.

Any observed result assigned zero probability by the **point model** is
reported by its retained record ID, even when a wider uncertainty band can
remain compatible. For an available point p, the Brier score is reported as
a full-N interval: observed loss plus each erased result's possible loss
between min(p²,(1−p)²) and max(p²,(1−p)²), divided by N. No score normalizes
by detected shots alone.

## 5. Conventional baseline and serial information loss

The conventional comparator is ordinary single-qubit linear inversion of the
same erasure-midpoint counts, with the same records, uncertainty budgets and
physical-point refusal. A separate arithmetic path computes (n+−n−)/N for
each axis. Its loss convention is squared displacement from those empirical
midpoints; it is not a maximum-likelihood or constrained-projection method.
The resulting estimates and Brier intervals agree by construction. No DET
accuracy, sample-efficiency or novel-tomography advantage is presumed.
The distinction between linear inversion and positivity-enforcing likelihood
methods is standard; see [James et al., On the Measurement of Qubits](https://arxiv.org/abs/quant-ph/0103121).
The helper's local status/duplicate guards do not certify a complete schedule;
full schedule/context validation occurs through fit.

The actual serial control Y→Y→Z→Y uses one preparation and conditional Lüders
updates. The first same-axis repetition is certain conditional on the first
record. After Z, subsequent Y is uniform and no longer accesses the initial
phase. **The earlier Y record remains** and still carries initial phase
information; the complete Y→Y→Z→Y histories need not have the same laws for
the opposite-phase states. In contrast Z→Y has identical laws for those two
states, and the known nonselective Z channel maps both to I/2. Exact tests
check the latter controls separately. Later serial outcomes never enter the
fresh-preparation tomography of the initial state.

A separate serial run erases the first result and stops after that actual
attempt, returning no residual model and no fabricated continuation. Another
explicitly labeled fault fixture reverses a repeated outcome, preserves both
records and reports zero-probability mismatch. It is not represented as a
valid Born-generated acquisition or experimental observation.

## 6. Record format and reproducible implementation

[trial_record.schema.json](trial_record.schema.json) specifies the structural
JSON format. [records.py](records.py) additionally enforces exact integer
types, unique JSON keys, ordered command/precursor chains, prefix length,
non-self-linked identities and serial context/preparation-status consistency.
Every row has record/trial/preparation/recipe/session IDs, split, step, record
precursor, all actual commands through this acquisition, setting, frame,
calibration, provenance, acquisition model, preparation status, detection
status, whether measurement occurred, outcome and reason. Unknown extra fields
are refused. A serial command uses its preceding command ID; a serial record
uses its preceding record ID. Both first precursors name the preparation
anchor. Sequence IDs are nominal labels independent of RNG seeds.

`detected` requires an actual ±1; `missing` requires an occurred binary read
with erased outcome; `failed` retains its reason and no fabricated outcome.
Records with failed/unknown preparation can be stored but not inferred under
this successful-preparation contract. No serial continuation follows an
unresolved record. The schema is structural; the Python validation supplies
cross-field/history semantics. JSON Schema numeric equality may accept `1.0`
where the strict Python contract intentionally demands an integer token.

The isolated files are [qubit.py](qubit.py), [simulator.py](simulator.py),
[inference.py](inference.py), the record module/schema, the worked runner,
[focused test runner](run_checks.py), and four focused test files. They use only
the Python standard library and import no accepted DET sources, core/RET
package, predecessor executor or research registry. Python 3.11+ is sufficient;
any existing compatible `python3` may replace `.venv/bin/python` below. No
virtual environment or additional dependency installation is required.
From the repository root:

```sh
.venv/bin/python -I -S -B docs/experiments/qubit_record_v1/run_checks.py
.venv/bin/python -I -S -B -O docs/experiments/qubit_record_v1/run_checks.py
.venv/bin/python -I -S -B docs/experiments/qubit_record_v1/worked_example.py
.venv/bin/python -I -S -B -O docs/experiments/qubit_record_v1/worked_example.py
```

Each worked command creates a new external temporary directory and prints its
location. `--output /absolute/new-or-empty-directory` and `--seed INTEGER` are
optional. Existing data is not overwritten; output inside the checkout is
refused. Generated trial datasets stay outside the repository. The output
contains plan, raw training/held/serial JSONL, frozen predictions, score,
partial-XZ prediction, separate truth audit and summary. No download, hardware,
cloud job, credential, paid service, provider message or automatic successor
is invoked. The runner adds only this known bundle directory to the isolated
startup path; contract guards do not depend on Python assertions.

## 7. Actual default simulation and interpretation

With Python **3.11.6** and seed 20260914, the executed run retained **4,608 training attempts
(372 erased)** and **1,536 held attempts (119 erased)**. Full-XYZ midpoints
were physical; the XZ-only fits reported no point and retained distinct
opposite-Y alternatives. The frozen full-fit predictions were:

| Recipe | Fitted W+ point | Ideal W+ interval | Frozen held-frequency band | Held completion interval |
|---|---:|---|---|---|
| phase_plus | 109/160 | [14749/32000,28851/32000] | [10909/32000,1] | [323/512,357/512] |
| phase_minus | 473/1280 | [2187/16000,4819/8000] | [267/16000,5779/8000] | [165/512,203/512] |
| mixed | 2623/5120 | [141/500,47527/64000] | [81/500,55207/64000] | [119/256,285/512] |

All held completion intervals overlap their frozen bands. The phase-pair
bands also overlap each other: this run **does not establish finite-count
confidence that their W populations differ**. The exact Born-law separation
is a property of the adopted model; the observed point differences are
simulation output. This small run verifies accounting and control behavior,
not a quantum-law discovery or an empirical test of DET ontology.

The plan SHA256 is
`9397a3c39105d88027c92873a1ff1661c09931b508c8af719c63586fd9233900`;
the full training-only prediction SHA256 is
`49b2217760a9fac5a508ced52d8c86399107f3fedb91d859c08705d725202820`.
These describe reproducible content, not signatures or experimental custody.
Main's normal and optimized focused runs both passed **61 tests** (0.642 s and
0.650 s). Separate normal/optimized worked CLI runs produced byte-identical
contents across all 12 exported files. Full sources, mathematical statements
and dataflow received independent review; final identities and review status
accompany the source-quiet handoff. These checks do not increase predecessor
research-registry witness totals.

## 8. Completed obligation and remaining boundary

The result is an explicit conditional qubit/C0 correspondence, a proved
record-erasure/uncertainty contract, counterexamples to phase invention and
midpoint repair, and an executable withheld-prediction experiment. The live
state/record/observer distinctions are kept; this does not derive a law for
all unrecorded relational activity or prove that record growth exhausts time.

Actual calibrated data with the prescribed preparation/frame and independently
measured W is a separate dependency documented by the coordinator in
[QUBIT_DATA_AND_FOLLOWUP](../../coordination/QUBIT_DATA_AND_FOLLOWUP.md).
Calculated W from an XYZ reconstruction is not measured held-out W. No current
dataset or calibration label is silently promoted to that acquisition law.
The RET voltage comparator and observer-in-supplied-geometry directions remain
separately queued. This assignment stops at reviewed handoff: no new lettered
QR gate, coverage/noncollapse sequel, full-QM reconstruction, native F/L,
metric emergence, physical mass, Einstein dynamics or gravity claim follows.
The primitive-input test, Option B and metric-as-record Status M are unchanged.
