# Calibration, acquisition and Bell-data audit

12 September 2026. Review target: `qr-05-bridge` commit
`ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8`.
This report distinguishes errors in an implication or interface from evidence
against the underlying physical theory or experiment.

## Scope and useful structure

BW/BX were read as design contracts; BY/BZ were assessed as downstream
acceptance proposals. CA/CB/CC/CE sources and tests received selective review.
The CA, CB, CC and CE suites passed respectively 11, 9, 10 and 7 tests in an
isolated archive, with Python bytecode writes disabled. This is 37 tests,
not independent validation of every physical or statistical premise.

Retain the reference-versus-transfer distinction, explicit validity and
acceptance events, and BX's separation of metrology, events, marks, sampling,
loss/selection and optional order/timebase. CB/CD correctly recognize that a
Bell correlation dataset and a calibrated geometric-volume measurement are
different targets. A category mismatch is not a refutation of either model.
These are useful interfaces, not evidence that their premises are satisfied.

## A1. BW misstates the independence requirement

BW says epistemic independence enables the union bound and that reusing
records prevents separate failure budgets from composing. This is too strong.
For any events E, G_a and G_d under the actual procedure, valid marginal
bounds imply

`P(E ∩ G_a ∩ G_d) ≥ 1 − (α + β_a + β_d)`,

with no independence assumption. Shared data may invalidate a particular
pre-selection marginal bound; that bound then needs repair. Shared data do
not invalidate the union inequality itself.

For three equally probable atoms, E={0,1}, G={1,2}, the intersection has
probability 1/3. The union lower bound is exactly 1/3, while multiplying
success probabilities gives the unjustified 4/9. The local exact regression
retains this counterexample.

Repair: require valid bounds for the actual sampling/adaptation procedure,
not a blanket prohibition on same-data calibration. Independence can be a
useful design choice without being a premise of this inequality.
[Branch BW §3](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05bw-reference-calibration-design-2026-09-10/README.md#L87)

## A2. BW mixes populations and estimates, and overstates distortion

The reference symbol is first used as a population point, then as a
finite-sample estimate with a separate population limit. The production
symbol is similarly reused in transfer decomposition. That makes it unclear
whether the calibration allowance bounds population distortion, sampling
error, or both.

Keep four objects distinct: ideal q, production population r, reference
population v, and finite-data estimates z. For q,r,v in the nested probability
triangle, the valid deterministic implication is

`||r−q||∞ ≤ min(1, a+d)`

on `||v−q||∞≤a` and `||r−v||∞≤d`. Probability distances here cannot be
arbitrarily large: the domain has diameter 1. Missing reference validity means
there is no justified *small* allowance, not an unbounded actual distance.
An upper bound a is not a lower bound on actual reference error; perfect
reference/record agreement can coexist with any error permitted by the
remaining premises, including zero.

Also, jointly valid coordinate intervals can be intersected with the known
probability triangle without losing coverage of the true point. The
triangle's nonrectangular support is not a reason to forbid confidence
rectangles.
[Branch BW definitions and composition](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05bw-reference-calibration-design-2026-09-10/README.md#L102)

The corrected design is recorded in [CALCULUS.md](CALCULUS.md), including
selection-conditional bounds, envelope failure budgets and the need to carry
all BV admissibility premises. No numerical calibration allocation or actual
reference is supplied.

## A3. CA's integrity seal omits an analysis-changing field

CA's sealed dataset keys omit `case`, although `pipeline` uses
`dataset["case"]` to select the nuisance candidates B, distortion allowance e
and metric/dynamics case. A caller can alter these analysis inputs without
changing the sealed core. The seal is also optional.

Thus the code does not provide end-to-end integrity for the analysis it
reports. A seal can be useful for accidental-change detection, but it must
cover the complete interpretation-bearing packet and be mandatory for an
authenticated route. This is a source-level defect, not a claim of malicious
tampering.
[CA sealed keys and reducer](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05ca-synthetic-pipeline-rehearsal-2026-09-10/primary.py#L21),
[CA pipeline](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05ca-synthetic-pipeline-rehearsal-2026-09-10/primary.py#L165)

## A4. CA is simplified plumbing, not the hardened BV inference

The reducer discards lost attempts and works with the resulting usable
count. Its inverse compares a point frequency against a finite supplied list
of nuisance candidates. That is not BV's simultaneous confidence-box
construction and continuous coupled nuisance inverse. A loss-rate threshold
alone does not establish that retained records have the intended sampling
law.

The metric/dynamics statuses largely echo supplied flags such as
`causal_consistent`, `normalized`, `preferred_clock` and `limit_stable`.
A Boolean input is not a measured metric, proof of a continuum limit, or
derived dynamics. Normalization and absence of a named preferred clock do
not establish the Einstein equations or general covariance.

Repair: label CA a synthetic interface illustration. Before any executable
apparatus adapter, bind all analysis fields, define acquisition and loss
semantics, reject coercive/malformed inputs, and use the actual verified
statistical inverse with its premises. Keep premise judgments separate from
computationally checked quantities.
[CA inverse and status flags](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05ca-synthetic-pipeline-rehearsal-2026-09-10/primary.py#L103)

## A5. CE visibility is not a general CHSH violation test

CE computes each correlation curve's half-range A=(max E−min E)/2 and calls
A²>1/2 a CHSH witness. That implication needs an additional validated
correlation model, appropriate relative phases/settings and measurement
assumptions. It is not a general consequence of a curve's visibility.

A deterministic local model with A_0=A_1=1, B_0=1, B_1=−1 has correlation
matrix

`E = [[1,−1],[1,−1]]`.

Each row has half-range 1 and passes the branch threshold, but every CHSH
sign combination has absolute value at most 2. The new local regression
checks all eight sign combinations exactly.

Repair: either explicitly condition the visibility interpretation on its
sinusoidal model, or calculate the four-correlator statistic for a declared
setting quadruple and give its actual sampling, selection and detection
assumptions. Preserve the curve and Fisher–Rao summaries as descriptive
calculations. Do not call these summaries a standalone Bell test or a
distinctive DET prediction.
[CE calculation](https://github.com/omekagardens/det_8_framework/blob/ac1f80ffb51ac1f6be0d6d740eaf82a1e411c5a8/docs/validation/qr-05ce-bell-correspondence-2026-09-10/primary.py#L48),
[original CHSH paper](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.23.880)

This audit does **not** conclude that the source experiment failed to violate
a Bell inequality. It identifies an insufficient inference in this branch's
analysis. Nor does the inspected dataset justify a claim that no suitable
geometric dataset exists anywhere.

## Adoption decision

Adopt the corrected conditional calibration contract and target-specific
data-routing discipline. Do not import CA as a production adapter or CE's
unqualified witness label. RET integration, calibrated acquisition and
physical reference evidence remain separately gated. BY/BZ can guide a
future protocol, but their existence does not close metric or dynamics work.
