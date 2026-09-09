# QR-05BF: known-placement portability of reduced access

8 September 2026 (Pacific/Honolulu). This protocol and its fixture menu
precede implementation and fixed evaluation. Exact finite synthetic
mathematics only; no ontology premise, RET integration or apparatus data.

## Question and supplied model

Can a moved, but exactly known, interior measurement position preserve
the target-specific four-site access found in BE? Separate failure of old
weights from insufficiency of the remaining measurements.

Supply Q = [0,1]², null coordinates u = t+x, v = t−x, c = 1,
signature (+,−), dμ = du dv/2, V = μ(Q), F = V²f and σ = V⁴.
The fixed kernel is R_Q = (1−u)(1−v)/2 and

\[
T(F)=\sigma^{-1}\int_Q F R_Q\,d\mu.
\]

Let φ = ((1−u)(1−v),u(1−v),(1−u)v,uv),
b = u(1−u)v(1−v), and f = Σc_a φ_a + θb. The sufficient admitted domain
max|c_a|+|θ|/16 ≤ 1 guarantees |f| ≤ 1 everywhere. This conservative
domain contains a neighborhood of zero; it is not the necessary domain of
valid quantum preparations. Geometry, the kernel and local Z axes are
supplied, not inferred from records. No quantum field or gravity source
is defined by this response model.

At each site prepare a fresh independent qubit ρ = (I+fZ)/2,
Z = diag(1,−1), and measure Π_x = (I+xZ)/2, x ∈ {−1,+1}.
Keep the unnormalized branch state Π_xρΠ_x including zero branches.
The four fixed corners have labels (00,10,01,11). Label cc denotes the
interior station's role, not a promise it remains the geometric center.
Its supplied position z is part of the geometry context; changing z is a
different declared experiment, not an unreported calibration adjustment.

## Fixed menu and exact access certificate

The [input](protocol.json) fixes six positions before evaluation:
center (1/2,1/2), equality_u (1/3,5/8), equality_v (5/8,1/3),
shift_low (1/3,1/2), shift_high (2/3,1/2), near_corner (3/4,3/4).
The equality cases are chosen as analytical controls, not discovered by
searching numerical results. Require 0 < u_z,v_z < 1; boundary positions
are outside this invertible five-site construction.

Compile the geometric integral row q = (T(V²φ_00), …, T(V²φ_11), T(V²b))
and the five-site evaluation matrix A_z independently of profile responses.
Its top four rows are (I₄,0), and its last row is (φ(z),b(z)).
Retain both inverse identities for D_z = A_z⁻¹ and v = qD_z.
Let S select rows (00,10,01,cc) and d = D_z e_11, where e_11 means the
fourth observation coordinate, not the interior station.

The block form gives

\[
d=(0,0,0,1,-\phi_{11}(z)/b(z))^\mathsf T,\quad
SA_zd=0,\quad \operatorname{rank}(SA_z)=4.
\]

Hence a linear target decoder exists exactly when qd = 0. Necessity for
any decoder on the admitted class also follows from the collision pair
below, not merely from a failed candidate weight choice. The population
identification statement does not make a finite-shot estimator exact.

Retain three distinct rows:

1. Frozen BE weights w_old = (1/12,1/36,1/36,1/9). Compute the complete
   stale residual w_old SA_z − q.
2. Recompiled candidate w = (v_00,v_10,v_01,v_cc). Its residual is
   w SA_z − q = −v_11 e_11ᵀ in coefficient order, and v_11 = qd.
   Always retain this candidate's diagnostic estimates, but certify it as
   a target decoder only when the entire residual vanishes.
3. Restored full-access weights v, satisfying vA_z = q and coefficient
   recovery D_z A_z = I₅. All five observations remain required for that
   contract even at positions where a weight happens to vanish.

Independently derive the equality locus from fresh integrals:

\[
qd=q_{11}-q_b/[(1-u_z)(1-v_z)],\qquad
(1-u_z)(1-v_z)=q_b/q_{11}.
\]

Retain the locus residual and its threshold as exact values. A moved
station can preserve target access while requiring new weights. Conversely,
recompiling a four-site candidate need not restore target identifiability.

## Prespecified profiles, collisions and complete branches

Every position receives the same four base profiles: zero, plus, minus,
and BE's asymmetric_bubble. Also construct two profiles with coefficient
vectors a_- = −δd and a_+ = +δd, where

\[
\delta=\frac{1}{2(1+|d_\theta|/16)}.
\]

Because d's corner part is e_11, each pair member has sufficient admission
bound exactly 1/2. This fixed scaling rule is not fitted to outcomes.
Both retained response vectors vanish. Their complete four-site laws and
unnormalized branch states agree; full five-site laws and omitted-site
states differ. Record the signed target difference T(a_+)−T(a_-) = 2δqd
even when zero, and full/retained total variations. Thus each position has
a profile collision, and only positions with qd ≠ 0 have a target ambiguity.
No number of fresh repeated measurements at those same retained sites can
distinguish this pair under the stipulated response law.

Keep all 16 reduced and 32 full outcomes for each of six profiles at each
of six positions: 1,728 complete branch rows. Each reduced row retains
both the stale and candidate estimate; the full row uses v. For each row
system retain mean, bias = mean−true target, variance and MSE.
Candidate scores remain diagnostic when identification fails. Do not select
a decoder from these scores or claim allocation optimality.

For each retained outcome, sum its two full branches over the 11 outcome,
retain the full 32-dimensional sum, and partial-trace original factor 3
to a 16-dimensional state. The result and its trace must match direct
four-site execution at every placement. Separately keep the two full-minus-
candidate estimate differences, including probability-zero rows. State/law
marginalization is not automatically target-estimator preservation.

This is a diagonal product-state model with exactly classical Bernoulli
likelihoods; no quantum advantage is claimed. All coefficients, means and
targets in this study are synthetic, not hidden inputs to an operational
observer. This gate adds a mathematical access certificate, not a new
public record decoder, calibration procedure or acquisition API. BE's
original record contracts remain unchanged.

The broader continuous-profile obstruction retained in BE remains a
limitation of that study. Its center-blind polynomial is not assumed
invisible after moving cc; BF does not repeat or extend its off-model
claim. Nor does model-specific full access establish unrestricted recovery.

## Independent methods and report schema

The primary uses independently adapted sparse matrix instruments, exact
monomial integration and rational elimination. The reference uses beta
integrals, the block inverse and direct Bernoulli/bit-index formulas,
without importing primary or historical numerical helpers. Tests add a
tensor-Boole integral oracle whose degree-zero through degree-five moments
are first checked. Synthetic integration nodes are not extra measurements.

Both engines expose analyze(protocol) without fixed computation at import,
returning the complete native schema below. F means Fraction, int is a
native integer, and all collections are lists/dicts (no tuples, floats,
boolean numeric values or hidden tables). List order is protocol order.
Statuses are strings. Row residuals are estimator minus true target;
collision differences are plus minus minus. Basis bits are lexicographic,
first slot most significant, bit 0 = Z+1. Outcomes use products of (−1,+1).

```text
geometry: {volume:F, sigma:F, coefficient_integrals:[5F],
  stale_weights:[4F], equality_threshold:F,
  retained_indices:[4ints], omitted_index:int}
placements: [{id, position:[2F], basis:[5F], evaluation_matrix:[5x5F],
  coefficient_decoder:[5x5F], left_inverse:[5x5F], right_inverse:[5x5F],
  full_weights:[5F], full_residual:[5F],
  retained_evaluation_matrix:[4x5F], retained_rank:int,
  omission_direction:[5F], retained_null_image:[4F], target_null_image:F,
  locus_residual:F, stale_residual:[5F], candidate_weights:[4F],
  candidate_residual:[5F], recovery_status, collision_scale:F,
  profiles:[{id, coefficients:[5F], admission_bound:F,
    sample_means:[5F], recovered_coefficients:[5F], target:F,
    reduced:{rows:[{outcomes:[4ints], probability:F, state_diagonal:[16F],
      stale_estimate:F, candidate_estimate:F}], stale:score, candidate:score},
    full:{rows:[{outcomes:[5ints], probability:F, state_diagonal:[32F],
      estimate:F}], mean:F, bias:F, variance:F, mse:F},
    marginalization:{rows:[{outcomes:[4ints], full_indices:[2ints],
      probability:F, summed_full_state:[32F], reduced_state:[16F],
      full_minus_candidate:[2F]}], pathwise_nonzero_count:int}}],
  collision:{profiles:[2names], coefficients_difference:[5F],
    full_means_difference:[5F], target_difference:F, predicted_target_difference:F,
    omitted_states:[[2F],[2F]], full_averaged_states:[[32F],[32F]],
    full_law_total_variation:F, retained_law_total_variation:F}}]
score: {mean:F, bias:F, variance:F, mse:F}
```

recovery_status is "identified" iff qd and the candidate residual are zero,
otherwise "not_identified". A nonzero stale residual does not set this
status. Full-minus-candidate differences are counted over all 32 full
branches for each profile, not only positive-probability rows. There is
no assumption that raw five-factor and four-factor states are equal.
left_inverse means D_z A_z, right_inverse means A_z D_z, and
locus_residual means (1−u_z)(1−v_z) minus equality_threshold.

## Source-bound execution and acceptance

Freeze this README, protocol, both engines, driver and tests before the
first fixed evaluation, together with five BE documents/artifacts. Keep
first-capture failures and disclose any post-first corrections. Use
create-only publication, strict bounded JSON (4,000,000 bytes), exact
native-type route agreement, input nonmutation, fresh verified source
loading, and final source/freeze/capture identity checks under normal and
optimized Python. Static syntax/lint checks are allowed before freezing;
fixed engine/test evaluations are not.

Compare selected BE center geometry and full repair5/target4 branch
reports for the four base profiles directly with retained data. Do not
execute old engines, recertify other BE controls, or treat the newly scaled
collision pair as BE's original fixtures. This narrow historical check
does not repeat BE's observer, shot-allocation or off-model studies.

Acceptance requires complete independent reports, both inverse identities,
rank/null/row certificates, all admitted collision witnesses, complete
branch states and marginalization, signed diagnostic scores and strict
source/capture/replay tests. No RET/core changes, dependencies, large jobs,
benchmarks, apparatus actions, clock experiments or gravity dynamics.
Small runs must not overlap a timing-sensitive RET rehearsal.

After publication, from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bf.py
python3 -I -O -B test_qr05bf.py
```

Original create-only steps are `study.py --freeze source-freeze.json`, then
`study.py --capture results.json`. See [RESULTS.md](RESULTS.md) after execution.
Hashes establish local byte integrity, not physical authentication or safety
against a hostile host.
