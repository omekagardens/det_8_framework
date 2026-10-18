# QR-05BI: interval-valued interior response

9 September 2026 (Pacific/Honolulu). This prospective protocol fixes
all budgets before implementation and numerical evaluation. Supplied
population intervals are not calibrated confidence intervals. No ontology,
RET integration, apparatus data or changed physical law is involved.

## Supplied model and the one uncertain response

Supply Q=[0,1]², u=t+x, v=t−x, c=1, signature (+,−),
dμ=du dv/2, V=1/2, F=V²f, σ=V⁴=1/16, R_Q=(1−u)(1−v)/2.
The normalized target is T=σ⁻¹∫F R_Qdμ=∫f(1−u)(1−v)du dv.
Use f=c·φ+θb, with
φ=((1−u)(1−v),u(1−v),(1−u)v,uv), b=u(1−u)v(1−v).
On (c00,c10,c01,c11,θ), q=(1/9,1/18,1/18,1/36,1/144).
Global response validity means |f|≤1 throughout this supplied square.

Exact corner means fix c. The fifth role cc has a position fixed during
a run, unknown within one finite menu. Its role label is not a position
tag. Retain six possibilities: center (1/2,1/2), equality_u (1/3,5/8),
equality_v (5/8,1/3), shift_low (1/3,1/2), shift_high (2/3,1/2),
near_corner (3/4,3/4). Menus all, center_only, equality_pair,
shifted_pair and center_near are inherited exactly from BH.
There is no prior, position mixture or per-shot movement.

The [input](protocol.json) embeds the unchanged BH protocol. Its
seven centers in (00,10,01,11,cc) order are:

| Case | Exact corners and interior interval center |
|---|---|
| zero | (0,0,0,0,0) |
| plus | (1,1,1,1,1) |
| minus | (−1,−1,−1,−1,−1) |
| quarter_interior | (0,0,0,0,1/4) |
| unit_interior | (0,0,0,0,1) |
| constant_corners_zero_interior | (1,1,1,1,0) |
| asymmetric | (1/2,−1/3,2/3,−1/2,1/3) |

For every case use point, narrow and wide budgets with radii
0, 1/64 and 1/8. The response interval is
J=[max(−1,m_cc−r),min(1,m_cc+r)], with closed endpoints.
Only the interior response varies; exact corners are a premise.
Intervals describe sets of possible population means, not noisy
realizations, finite-shot estimates or probabilities over alternatives.

## Scalar global-validity constraints

Recompute two-sided inverse geometry as in BH. At position z,
r_z=φ(z)·c and s_z=b(z)>0 give m=r_z+s_zθ, hence
D_z(J)=[(J_lo−r_z)/s_z,(J_hi−r_z)/s_z].
The target is t0+q_bθ, t0=q_corner·c, q_b=1/144.
Reconstruct both endpoint responses directly from their polynomials.

Use the unchanged degree-(2,2) Bernstein root and four half-square
leaves ll,lh,hl,hh. Each coefficient is A+Bθ. Retain both coefficients,
and both components of the exact degree-(2,2) reconstruction residual
on the local {0,1/2,1}² unisolvent grid. Their vanishing establishes
the identity for every θ, not just selected point profiles.
The nine physical witness values on {0,1/2,1}² are likewise affine.
These mathematical grids add no acquired data.

For each affine quantity solve −1≤A+Bθ≤1. With B=0 the constraint
is all real if |A|≤1, otherwise empty. Negative slopes reverse endpoint
order. Boundaries are inclusive. Retain every individual constraint
preimage; do not discard zero slopes or confuse infinity with emptiness.

The old sufficient interval is O=[−g,g], g=16(1−max|c|).
The Bernstein interval B is the conjunction of all 36 leaf-coefficient
constraints; root constraints are diagnostic, not an extra veto.
The witness interval W is the conjunction of actual point constraints.
The global sufficient set is O∪B; W is necessary, not sufficient.
For these valid corners θ=0 belongs to O and B, so their union is
connected before data intersection. Verify rather than assume that
simplification; generic union helpers must also handle disjoint sets.

Intersect O, B, O∪B and W separately with each D_z(J), keeping
old, Bernstein, inner and outer routes visible. Project each through
t0+q_bθ. A single position can have both certified and unresolved
θ portions: do not give an interval hypothesis one BH-style validity label.
Only the zero-width budget has point_classification, using
certified if inner nonempty, refuted if outer empty, unresolved otherwise.

## Exact unions and logical status

Hypotheses are (position,θ). Per menu retain nonempty position-specific
old, inner and outer θ/target sets in the declared position order.
Their merged target unions are separate objects. Sort components by
lower endpoint and merge overlapping or touching closed intervals.
Retain each genuine open gap (left_upper,right_lower) and its midpoint
outside the union. A hull encloses the union but need not equal it.
Empty unions have null hulls, no gaps and no fabricated zero answer.

Old⊆inner⊆valid⊆outer holds as hypothesis sets; the same inclusions
hold for target projections. Existence is infeasible only if outer is
empty, feasible if inner is nonempty, unresolved otherwise. Target status
is infeasible if outer is empty; identified if inner is nonempty and
outer is exactly one singleton; ambiguous if inner already contains
two different values (including a positive-width component); unresolved
otherwise. Hypothesis exactness and target-union exactness are separate.
No existence assumption is added when inner is empty.

Point⊆narrow⊆wide must survive inversion, route intersections and
target projection. Restricting a position menu must equal filtering
position records. Both inner and outer can stay unchanged on narrowing;
no strictly improved precision is promised. Global validity need not
be completely decided for response intervals even if BH's points were.

## One coupled quantum-record law family per case

At each role use a fresh independent diagonal qubit ρ=(I+mZ)/2,
Z=diag(1,−1), and ideal projectors Π_x=(I+xZ)/2, x∈{−1,+1}.
The four corner states are fixed. The full five-role input, every
unnormalized branch state and every probability are affine in the SAME
interior mean m. Retain intercept/slope pairs for all 32 branches and
every entry of their 32-dimensional diagonal states, plus the averaged
state. Keep zero-probability branches. Slope matrices need not be positive.

For each budget evaluate every probability/state entry at both endpoints
and verify nonnegativity, normalization and branch-trace agreement;
affinity proves these properties throughout the interval. Retain endpoint
summary checks. The full coefficients retain the shared-parameter
dependence that an entrywise interval box or midpoint law would lose.
An affine representation does not assign prior weights to hypotheses.
Role-labeled internal state equality is not equality of spatial fields;
these likelihoods remain classical Bernoulli-equivalent.

## Independent routes and native report contract

The primary uses its owned sparse quantum/monomial helpers, affine
power-to-Bernstein conversion and sequential scalar clipping.
The reference uses independent beta/Bernoulli, interpolation/de Casteljau
and lower/upper threshold extrema. Tests use Boole/Gram-moment/cofactor
reconstruction and an independent breakpoint-arrangement scalar solver,
with scalar endpoint quantum laws. No old executor or the other engine's
helpers are imported; retained BH answers are not computation oracles.

Both analyze(protocol) functions do no fixed computation at import.
F means Fraction; affine pair A=[intercept:F,slope:F].
I=[lower:F-or-null,upper:F-or-null] is a nonempty closed interval;
null interval means empty, while [null,null] means all real.
Only individual/global constraint intervals may have infinite endpoints.
Data-intersected and target intervals must be finite. U=[I] is a sorted,
merged finite union; [] is empty. No tuple, float or boolean report values.
Labels are strings, outcomes are native integers, empty fields typed null.

```text
report: {geometry:BG_geometry, positions:[BG_position], cases:[case]}
case: {id, corners:[4F], center_mean:F, target_offset:F, target_slope:F,
  constraints:constraints, law_family:law_family, budgets:[budget]}
constraints: {old_theta:I-or-null, patches:[patch], witnesses:[witness],
  bernstein_theta:I-or-null, witness_theta:I-or-null,
  inner_theta:U, outer_theta:U}
patch: {id,bounds:[[2F],[2F]],coefficients:[3x3A],
  reconstruction_residual:[3x3A],allowed:[3x3 I-or-null],theta_interval:I-or-null}
witness: {position:[2F],value:A,allowed:I-or-null}
law_family: {rows:[{outcomes:[5ints],probability:A,state_diagonal:[32A]}],
  averaged_state:[32A]}
budget: {id,response_interval:[2F],endpoint_checks:[2check],
  positions:[position_report],menus:[menu]}
check: {mean:F,probability_sum:F,averaged_trace:F,
  minimum_probability:F,minimum_state_entry:F,maximum_trace_residual:F}
position_report: {position_id,response_intercept:F,response_slope:F,
  data_theta:[2F],data_target:[2F],reconstruction_residual:[2x5F],
  old_theta:U,bernstein_theta:U,inner_theta:U,outer_theta:U,
  old_targets:U,bernstein_targets:U,inner_targets:U,outer_targets:U,
  point_classification:string-or-null}
menu: {id,position_ids:[strings],old:[entry],inner:[entry],outer:[entry],
  target_sets:{old:set_summary,inner:set_summary,outer:set_summary},
  existence_status,target_status,hypothesis_set_status,target_set_status}
entry: {position_id,theta:U,targets:U}
set_summary: {intervals:U,hull:I-or-null,gaps:[I],gap_probes:[F]}
```

Patch rows index u, columns v, both Bernstein degree 0,1,2.
Residual pairs are original polynomial minus Bernstein representation.
Patches are root,ll,lh,hl,hh; witness/local grids are u-major.
The inherited geometry/position fields are defined in the pinned BG/BH
contract: q, V, σ, basis/evaluation matrix, decoder, both inverse products,
full target weights and row residual. All are recomputed here.
Budget/position/menu order is protocol order; outcomes are lexicographic
(−1,+1), computational bits 0=Z+1 with first role most significant.
Exactness statuses are exact or bounded. Gap intervals denote open
gaps despite the shared two-endpoint storage notation.

## Source-bound execution and acceptance

Freeze README, protocol, engines, driver and tests plus five BH
README/RESULTS/protocol/freeze/capture identities before any fixed
engine/test evaluation. Static lint and syntax-only checks may precede
freeze. Preserve first-capture failure history and disclose post-first
corrections. Use strict bounded JSON (4,000,000 bytes), native-type exact
independent agreement, input nonmutation, same-byte protocol hashing/
parsing, fresh verified source execution, create-only capture/read-only
replay, and final source/freeze/capture byte brackets.

The zero-width historical restriction checks selected BH geometry,
42 coefficient/target/classification hypotheses, all point root/leaf
coefficients and witness values, 35 point menu layers/statuses, and
complete affine-law evaluations against seven public and 42 candidate
laws (1,568 branch rows). It does not embed or recertify the entire BH
report, old lifecycle or earlier BG restriction; no historical engine runs.

Acceptance requires full independent reports, exact affine/global/data
constraints, coupled complete laws, endpoint checks, union gaps and
monotonicity, semantic and evidence tests, zero-width historical agreement,
normal/optimized tests and replays. After first capture use exactly one
reference-only audit in another available Python runtime. No RET/core
edits, dependencies, large jobs, apparatus actions, clocks or gravity.
Small runs must not overlap a timing-sensitive RET rehearsal.

After publication, from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bi.py
python3 -I -O -B test_qr05bi.py
```

Original create-only steps: study.py --freeze source-freeze.json, then
study.py --capture results.json. Read [RESULTS.md](RESULTS.md) afterward.
Hashes establish local integrity, not physical authentication or protection
against a hostile host.
