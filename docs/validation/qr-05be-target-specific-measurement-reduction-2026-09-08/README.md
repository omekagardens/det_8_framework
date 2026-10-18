# QR-05BE: target-specific measurement reduction

8 September 2026 (Pacific/Honolulu). The protocol precedes implementation
and fixed engine evaluation. Exact finite synthetic verification only:
no ontology commitment, apparatus data, RET integration or new physical law.

## Supplied model and target

Use Q = [0,1]² in flat null coordinates u = t+x, v = t−x, c = 1,
signature (+,−), dμ = du dv/2, V = μ(Q), F = V²f and σ = V⁴.
With R_Q = (1−u)(1−v)/2, the target is

\[
T(F)=\sigma^{-1}\int_Q F R_Q\,d\mu.
\]

Geometry, coordinate positions, local Z axes and this future-volume kernel
are supplied, not inferred from quantum outcomes or software record counts.
The kernel is not a quantum instrument or a polarization–gravity coupling.

Let φ = ((1−u)(1−v),u(1−v),(1−u)v,uv), b = u(1−u)v(1−v), and
f = Σc_a φ_a + θb. The admitted class obeys max|c_a|+|θ|/16 ≤ 1,
which guarantees |f| ≤ 1 globally by the partition of unity and b ≤ 1/16.
This sufficient bound is not a necessary physical-validity condition.
The distinct global-validity controls in [BD](../qr-05bd-interior-measurement-repair-2026-09-08/RESULTS.md)
remain retained there; this study does not rerun those controls.

A local fresh qubit has ρ = (I₂+fZ)/2, Z = diag(1,−1). Ideal Z projectors
Πₓ = (I₂+xZ)/2 have x ∈ {−1,+1}. Use independent copies, including
repeated shots at a nominal station, and retain ΠₓρΠₓ without branch
normalization. These response/preparation maps are not a continuum QFT
state. Nominal repeated coordinates do not mean fresh measurements at an
identical spacetime event. Actual localization, calibration, drift and loss
would require a different apparatus protocol.

## Two new acquisition contracts

The existing five sites are (00,10,01,11,cc), with cc = (1/2,1/2).
Compile the evaluation matrix A of (φ,b), a two-sided inverse D and
integral row q from geometry before processing any profile response.
Recompute v = qD; do not import old target outputs as an integration oracle.
BD's zero 11 coefficient motivates the new question, not a change to its
original complete-record contract.

| Plan | Event slots in tensor-factor order | Weight rule | Cost |
|---|---|---|---:|
| corner4 | 00#1,10#1,01#1,11#1 | Original corner weights | 4 |
| repair5 | 00#1,10#1,01#1,11#1,cc#1 | Full repaired weights | 5 |
| corner5 | 00#1,00#2,10#1,01#1,11#1 | Original weights; average 00 | 5 |
| target4 | 00#1,10#1,01#1,cc#1 | Retain the four declared target weights | 4 |
| repeatcc5 | 00#1,10#1,01#1,cc#1,cc#2 | Same retained weights; average cc | 5 |

All listed slots remain mandatory for their own plan. repair5 must still
refuse a missing 11 record, even with a zero weight. repeatcc5 has two
distinct fresh cc records, not duplicate registrations or an unreset qubit.
Center replication is fixed before evaluation because of its largest
absolute geometric weight. This is not proof of variance-optimal allocation:
the unknown profile also controls each Bernoulli variance.

The frozen input retains BD's ten admitted fixtures and adds the two
profiles ±(φ₁₁−4b)/2, labeled collision_minus and collision_plus. Every
profile receives all five plans and all 16/32 outcomes, including zero
branches. No plan or fixture is selected after seeing its score.

## Exact reduction and the information it loses

Delete A's 11 observation row to form S A. Retain its rank, and the
omitted-data direction d = D e₁₁. Verify S A d = 0 and qd = 0 alongside
AD = DA = I₅ and vA = q. Target identification can survive a missing
coefficient direction; full coefficient identification need not survive.
These finite linear-map identities are separate from finite-shot accuracy.

For each retained four-outcome vector y, collect both repair5 outcomes
whose (00,10,01,cc) entries equal y. Keep both old outcome indices and
estimates. Each full estimate must equal the target4 estimate, even if its
branch probability is zero. Sum the two unnormalized five-factor branch
states, then partial-trace the original factor index 3 (11). Compare this
16-dimensional reduced state and its trace with direct target4 execution.
Keep the 32-dimensional summed state in the report too; it is not equal
to, or reconstructed from, the smaller output.

As a wrong-subsystem control, trace the final factor cc instead and retain
the resulting diagonal in its own (00,10,01,11) order. Comparing it as if
it were the desired (00,10,01,cc) result is the error being tested, not an
assertion that the two physical subsystem labels are interchangeable.

The collision pair must have different full coefficients and omitted-site
states, yet equal retained laws and targets. Retain full- and retained-law
total variations and the two full outcome-averaged state diagonals. Do not
turn this into full-state recovery or a minimal measurement-count theorem.

## Error, cost and off-model boundary

For every plan retain mean, bias relative to the full true T(F), variance
and MSE = variance+bias². Report target4 minus corner4 at equal four-shot
cost and repeatcc5 minus both five-shot baselines. Preserve every sign.
Separately compare target4 with repair5 under exact marginalization.

For the fixed fresh-copy replication, verify the direct variance reduction
against v_cc²(1−f(cc)²)/2. Compare the direct MSE reduction too; the two
target estimators have the same mean and hence the same bias. A nonnegative
reduction from repeating an independent observation is not automatically
superiority to the corner plan or a quantum advantage. These diagonal
product-state likelihoods are exactly classical Bernoulli-equivalent.

Retain h = b[(u−1/2)²+(v−1/2)²], amplitude one, bounded by 1/32.
It vanishes at every original site while its integral target is positive.
Run repair5, target4 and repeatcc5 on it, retain their complete branch
reports and the reduction certificate, and compare with the zero profile.
Neither omission nor replication adds access to this blind spatial mode.
This obstruction is a model/access limitation, not presumed sensor noise.

## Independent methods and native report contract

The primary statically adapts its own sparse tensor and monomial helpers,
uses rational elimination for inverses/rank, and explicitly traces sparse
branch matrices. The reference independently uses Bernoulli products,
beta integrals, direct coefficient recovery and bit-index summation for
partial traces. No old executor or cross-engine helper is imported.
Tests use a distinct tensor-Boole oracle, verifying degree-zero through
degree-five moments before integrating the declared polynomials. Its
synthetic nodes are not observer measurements.

Both engines return this complete native schema. F below means an exact
Fraction; indices/counts/outcomes are native integers and names are strings.
No floats, boolean-as-number values, tuples or private output tables occur
in the mathematical report. Lists retain protocol order.

```text
geometry: {volume:F, sigma:F, corner_weights:[4F], bubble_target:F,
  bubble_at_center:F, center_basis:[4F], evaluation_matrix:[5x5F],
  coefficient_decoder:[5x5F], repair_weights:[5F], weight_sum:F}
operators: {corner4:[16 operator rows], five_factor:[32 operator rows]}
  operator row: {outcomes:[n ints], kraus_diagonal:[2^n F]}
schedule_counts: {corner4:int, five_factor:int}
plans: [{id, slots:[[station,shot]], cost:int, event_weights:[n F]}]
reduction: {retained_indices:[4 ints], omitted_index:int,
  retained_evaluation_matrix:[4x5F], retained_rank:int,
  omission_direction:[5F], retained_null_image:[4F], target_null_image:F,
  target_weights:[4F]}
profiles: [{id, corners:[4F], theta:F, admission_bound:F,
  sample_means:[5F], recovered_coefficients:[5F], target:F, corner_target:F,
  plans:{each plan id: plan report}, marginalization: marginal report,
  reallocation:{direct_variance_reduction:F, predicted_variance_reduction:F,
    direct_mse_reduction:F},
  mse_differences:{target4_minus_corner4:F, repeatcc5_minus_corner5:F,
    repeatcc5_minus_repair5:F}}]
plan report: {rows:[{outcomes:[n ints], probability:F,
  state_diagonal:[2^n F], estimate:F}], mean:F, bias:F, variance:F, mse:F}
marginal report: {rows:[{outcomes:[4 ints], full_indices:[2 ints],
  full_estimates:[2F], probability:F, summed_full_state:[32F],
  reduced_state:[16F], wrong_trace_state:[16F], estimate:F}],
  pathwise_checks:int, wrong_trace_disagreements:int,
  moment_differences:{mean:F, variance:F, mse:F}}
collision: {profiles:[2 names], coefficients_difference:[5F],
  full_means_difference:[5F], target_difference:F,
  omitted_states:[[2F],[2F]], full_averaged_states:[[32F],[32F]],
  full_law_total_variation:F, retained_law_total_variation:F}
off_model: {id, sample_means:[5F], global_bound:F, target:F,
  plans:{repair5:plan report, target4:plan report, repeatcc5:plan report},
  marginalization:marginal report}
```

Collision differences are second profile minus first. Computational basis
bits are lexicographic with bit 0 meaning Z = +1 and the first slot most
significant; outcomes use lexicographic products of (−1,+1). TV is half
the sum of absolute differences of complete outcome probabilities.
Each marginal certificate counts 32 full-branch pathwise checks and counts
wrong-trace disagreements over its 16 retained-outcome rows. Its moment
differences are target4 minus repair5.

## Public observer and source-bound evidence

The observer receives only a complete plan's records, compiled station
weights and the public plan ID. It averages declared fresh station shots,
then applies the weights. All 15 record fields in the protocol are exact;
unknown plans, missing/duplicate/wrong slots, private fields, invalid native
types, mismatched contexts or unavailable/unattempted records are refused.
Registered binary outcomes are not physical loss or postselected data.
Check forward/reverse record order for every main and off-model branch.

Hold the README, protocol, engines, driver and tests before the first
source freeze. Bind those six files and five preceding BD documents/
artifacts by exact bytes. Compare the selected overlapping BD geometry,
operators, original plans, first ten profile branches and repair5 off-model
law directly with retained data; do not execute historical engines or
claim a new replay of unrelated covariance/global-validity controls.

Use create-only source freeze/capture, native-type exact engine comparison,
unmutated inputs, fresh verified source-byte execution, strict bounded JSON
(4,000,000 bytes per file), full replay and final source/freeze/artifact
byte checks under normal and optimized Python. Preserve any failed first
capture and document any post-first correction. No fixed engine or test
evaluation precedes freezing; syntax and static lint checks are allowed.
No RET/core changes, dependencies, runtime benchmark, apparatus action,
clock experiment or gravity dynamics belongs to this gate. Small runs must
not overlap a timing-sensitive RET rehearsal.

Acceptance requires full independent reports, all linear/reduction/state
identities, the intended collision/off-model controls, complete signed
cost comparisons and strict record/evidence tests. Read [RESULTS.md](RESULTS.md)
after execution. This is a target-specific result on supplied geometry,
not unknown-geometry inference or a calibrated application certificate.

## Reproduction

From this directory after publication:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05be.py
python3 -I -O -B test_qr05be.py
```

Original creation uses `study.py --freeze source-freeze.json` followed by
`study.py --capture results.json`; neither may overwrite a retained file.
Hashes provide local integrity, not physical authentication or protection
against a hostile host.
