# QR-05BV — bounded acquisition-distortion verification

Prospective executable contract. The authoritative checkout is `ret`; this
gate implements the [BU design](../qr-05bu-acquisition-distortion-design-2026-09-09/README.md)
and its [accepted result](../qr-05bu-acquisition-distortion-design-2026-09-09/RESULTS.md).
No physical law, ontological commitment, apparatus calibration, new data
collection, or continuum reconstruction is asserted by this finite toy check.

## Mathematical scope

Use the supplied two-dimensional metric `ds²=s(1+ηuv)du dv`, signature
`(+,-)`, volume density `s(1+ηuv)/2`, and sampling density `1+δuv`.
The fixed rectangles are Q=(0,1)², I1=(0,1/2)², and
I2=(0,3/4)×(0,1/2). For a rectangle anchored at zero with area z,

`M_z(δ)=(s/2)[z+(η+δ)z²/4+ηδz³/9]`.

The normalized probabilities are `q_i=M_Ii/M_Q`; the geometric target is
`τ=(16+η)/(16(4+η))`. The four geometry labels use η=0,1 and s=1,4.
The nuisance classes are δ∈[0,b], b=0,1/2,1,2. All arithmetic is rational.
The class-separation and zero-error planning baseline is the authenticated
[BT capture](../qr-05bt-separation-budget-verification-2026-09-09/results.json),
described in its [contract](../qr-05bt-separation-budget-verification-2026-09-09/README.md)
and [results](../qr-05bt-separation-budget-verification-2026-09-09/RESULTS.md).

The admitted actual iid nested-bit law is
`π(r)=(1-r2,r2-r1,0,r1)` in bit order 00,01,10,11, with
`r∈S={0≤r1≤r2≤1}`. A deterministic, externally justified bound
`||r-q_true||∞≤e` is an assumption, not an output of this verification.
The actual-law classes allow separate admissible distortions under each
hypothesis, not a single known common acquisition channel.

Let D be the ideal class distance and p0,p1 its contact points. Their
distorted distance is exactly `max(D-2e,0)`: the reverse triangle inequality
is a global lower bound; for D>0 the interpolated contacts
`r0=(1-λ)p0+λp1`, `r1=λp0+(1-λ)p1`,
`λ=min(e/D,1/2)`, attain it inside convex S. For D=0 use λ=0.
The signed remainder D-2e is retained separately from this clipped distance.
No new above-contact numerical fixture is added in this gate.

For an original probability box C=[L1,U1]×[L2,U2], check C∩S first.
If empty, its nuisance inverse is empty even when an enlarged rectangle
intersects S. Otherwise set `Le_i=max(0,Li-e)` and `Ue_i=min(1,Ui+e)`.
The exact latent inverse is the set of shared δ∈[0,b] satisfying all four
affine mass inequalities for `Le_i≤q_i(δ)≤Ue_i`.
At each retained endpoint define
`Ai=max(Li,qi-e)`, `Bi=min(Ui,qi+e)` and
`r=(A1,max(A2,A1))`. This is an explicit original-box nested witness, not
merely an assertion of coordinatewise overlap. Both endpoints are retained
even for a singleton. Empty inverses retain their four constraints but no
endpoint witnesses, except the pre-enlargement empty-S guard, which returns
all three inverse lists empty.

The conditional pre-data guarantee requires `W(C)+2e<D` for every possible
count box. With n=65536, grid denominator m=256, α=1/20 and four tails
1/80, the fixed sufficient test is
`slack=D-2e-2/m>0` and `n*slack²≥10`, using the BU/BT proof `ln(80)<5`.
The positive sign is checked before interpreting a squared score.
The statement is conditional on the admitted iid law and valid distortion
bound: correct singleton probability ≥19/20 and conditional wrong-singleton
probability ≤1/20. A failed sufficient test need not mean impossibility.
Statistical calibration would require a separate β failure allocation and
selection conditions; neither is silently absorbed into α here.

## Frozen census and independent routes

[protocol.json](protocol.json) fixes four geometries, four classes, eight
class/error cases and corresponding plans, ten singleton population boxes,
forty enlarged and forty unexpanded geometry hypotheses, two scale pairs,
one nonnested negative control, and four complete BT class/plan comparisons.
The three error fractions are 0,1/4,1/2 of D for the narrow classes;
the two broad classes use e=0. No count enumeration, synthetic acquisition,
new large-quota binomial tail, adaptive search, or fixture expansion occurs.

[primary.py](primary.py) integrates monomials and clips the four affine
mass inequalities directly in δ. [reference.py](reference.py) uses tensor
Simpson quadrature at δ=0,1, clips the shared probability-segment parameter,
and maps it independently back to δ. Both derive global class lower
certificates from all four segment-pair corners and explicit attaining
contacts. [test_qr05bv.py](test_qr05bv.py) uses a third rectangle-moment
route and direct root/closed-cell admission for an independent full-report
oracle. Engines do not import each other, earlier engines, or test oracles.

The only additional private boundary exercise is
`C=[[3/4,1],[0,1/4]], e=1, b=0`: C∩S is empty and must stay excluded
before enlargement. It is not an additional population fixture or an
admissible distorted world. Other malformed-input tests are schema checks,
not new scientific cases. Both engines export private
`_inverse(geometry, box, error, upper)` returning exactly
`{delta_set,constraints,endpoints}`; box is a list of two rational intervals.

## Exact native report wire

All native containers are plain dict/list; mathematical numbers, including
zeros, are `Fraction`. Metadata counts, eta and scale are exact ints (not
bools); flags are exact bools. No floats, tuples, None, subclass substitutions,
cycles, or reserved encoding keys are admitted. Protocol order fixes row
order throughout; endpoint and constraint order is defined below.
Native rational trees are compared before canonical encoding.

Top-level keys are exactly `schema,planning,geometries,classes,cases,plans,
boxes,negative,scale_pairs,baseline`, schema `qr05bv-report-v1`.

* `planning`: `quota,grid_denominator,alpha,tail_allocations,threshold,
  log_upper,basis`; threshold=10, log_upper=5, basis=`ln80_lt_5`.
* Each geometry: `id,eta,scale,volumes,mass_coefficients,
  derivative_numerators,target,line,positive_normalizer,decreasing`.
  Volumes and coefficient pairs [A,B] use Q,I1,I2 order and actual s;
  derivatives use I1,I2 order. The normalized line [a,b,c] means
  aq1+bq2=c (flat [-20,16,1], conformal [-9520,7296,371]).
  The flags certify the whole δ∈[0,2] range, not a finite sample.
* Each class is the complete BT native wire: `bound,upper,segments,kind,
  deltas,parameters,points,residual,distance,closed_form,lower`.
  Two segments in flat/conformal order have `start,end,vector`.
  Kind is `ordered` or `collision`; contacts use δ=(b,0) for b<1,
  otherwise (1,0). Each point/vector has two coordinates. Lower has
  `normal,coefficients,corner_values,norm,value`, with affine coefficients
  [c,mt,ms] and corners (0,0),(0,1),(1,0),(1,1). Use normal (0,1)
  for b<1 and (0,0) otherwise. No division by a zero-length segment.
* Each case: `id,bound,upper,fraction,error,ideal_distance,signed_remaining,
  distance,ideal_deltas,ideal_contacts,actual_contacts,displacements,
  distortion_norms,laws,nested,interpolation,kind,lower`.
  Two-world arrays are flat/conformal. Displacements are actual minus
  ideal; norms are infinity norms. Kind is `separated`, `new_collision`,
  or `inherited_collision`. Lower has `normal,norm,ideal_corner_values,
  penalty,signed_value,value`: penalty=2e||normal||1, signed value is the
  minimum ideal corner minus penalty, value=max(0,signed value).
* Each plan: `id,ideal_distance,error,signed_remaining,distance,step,slack,
  score,grid_positive,threshold_holds,sufficient,status,guarantees`.
  step=1/m; slack uses the signed remainder; score=n*slack².
  Sufficient is the conjunction of the two flags. Status is `certified`
  or `not_certified`. Guarantees is empty or a singleton list containing
  `correct_singleton_at_least` and `conditional_wrong_singleton_at_most`.
* Each box: `id,bound,upper,fraction,error,point,intervals,nested_box,
  expanded,hypotheses,targets,status,unexpanded`. Original intervals are
  the singleton point. Point is the selected ideal flat/conformal contact
  or their midpoint. Targets are sorted unique geometric targets from
  nonempty hypotheses; status is `empty`, `singleton`, or `ambiguous`.
  `unexpanded` has exactly `hypotheses,targets,status` using the original
  C and e=0, not a different C. Each hypothesis has `id,eta,scale,target,
  delta_set,constraints,endpoints`. A nuisance set is [] or [lo,hi].
  Constraints [c,m] mean c+mδ≥0, ordered I1 lower, I1 upper, I2 lower,
  I2 upper, with coefficients (Ai-Le_i*Aq,Bi-Le_i*Bq) then
  (Ue_i*Aq-Ai,Ue_i*Bq-Bi). Every endpoint has exactly
  `delta,q,constraint_values,A,B,r,law,offset,norm,nested,inside_box,
  within_error`. The four values are the original mass-constraint values;
  A,B and r are the original-box witness above, offset=r-q. Flags are
  evaluated, not hardcoded. Empty sets have no witnesses.
* `negative`: `eta,delta,error,lambda,ideal_q,ideal_law,actual_law,
  actual_marginals,marginals_equal,within_error,population_in_S,
  nonnegative,normalized,nested_support,forbidden_mass,refusal_lower,
  alpha,refusal_exceeds_alpha,status`. The one flat δ=0 law moves mass
  λ=1/16 by [-λ,+λ,+λ,-λ]. Its marginals are unchanged at e=0 but
  P(10)=λ>α. The first-attempt refusal lower bound is λ; do not evaluate
  the large-quota power. Status is `outside_nested_law`. This shows why
  matching marginal error alone cannot validate the nested iid premise.
* Each scale pair: `worlds,volume_factor,actual_scaling,classes_equal,
  cases_equal,inverses_equal,constraints_scaled,targets_equal`.
  Worlds are [unitID,x4ID] and volume_factor=4. Recompute class/case
  normalized rows with both scaled geometries. Compare all enlarged and
  unexpanded inverses at identical B,e,C after removing id,eta,scale,
  target and raw constraints/endpoint constraint_values. Raw constraints
  and endpoint constraint_values instead scale by four; mass/volume by
  four, derivative numerators by sixteen. No arbitrary r is equated
  between independent acquisitions merely because its bound is equal.
* `baseline`: `schema,zero_ids,classes_equal,plans_equal,plans`, schema
  `qr05bv-bt-comparison-v1`. Zero IDs are uniform/zero, half/zero,
  one/zero, two/zero. Plans are freshly derived complete legacy BT class
  rows: `id,kind,source,distance,in_premise,slack,score,grid_positive,
  threshold_holds,sufficient,eligible,status,guarantees` with id
  `class/BOUND`, kind=`class`, source=BOUND, in_premise=True and
  eligible=sufficient. The complete newly derived class and legacy plan
  trees must equal the authenticated BT rows, or analysis raises.

## Input and evidence boundary

Each engine's `analyze(protocol,baseline)` independently validates the
entire protocol against its literal fixed schema and values, and the
entire native baseline shape/types/metadata before constructing new
Fractions or performing mathematics. Baseline is exactly
`{schema:'qr05bv-bt-baseline-v1',classes:[four complete BT classes],
plans:[four complete BT class plans]}` in bound order. All mathematical
fields must be plain Fractions and every flag a bool. Baseline values
are checked against fresh derivations after calculation; shape validation
is not a claim of pre-calculation mathematical truth checking.

[study.py](study.py) authenticates the entire stored BT capture by its
literal SHA-256 before parsing it, extracts only those complete class and
class-plan rows, and never imports or runs the BT engine. The only prior
executable source is the literal-hash-pinned
[BM evidence utility](../qr-05bm-relative-volume-verification-2026-09-09/study.py),
used only for bounded reads, strict JSON, canonical encoding/decoding,
typed equality, identities, deadline, and exclusive write helpers. No
earlier mathematical, freeze, capture or replay wrapper is called.

The source freeze has twelve identities: this README, protocol, both
engines, driver, tests; BU README/RESULTS; BT README/RESULTS/capture;
and BM study. Maximum source size is 262144 bytes; the BT capture uses
the separate 16777216-byte artifact cap. Strict protocol-byte identity
and complete baseline-byte identity are checked before parsing. Freeze
does not decode baseline Fractions or call mathematical engines.
Fresh engine namespaces and independent deep-copied inputs are used;
input mutations and full native report disagreements abort before encoding.
Source/freeze identities are rechecked after work and before exclusive
artifact creation; replay compares the complete canonical capture.

All six new sources must be held and statically reviewed before the first
source freeze and first mathematical run. Once run, do not retune or
overwrite evidence. Any failed run is preserved and requires a separately
named prospective revision. Use 30-second per-analysis and 120-second
whole-suite interrupting deadlines. Run one first capture, all 28 tests
in both normal and optimized modes, one replay in each mode, and exactly one
reference-only Python 3.11 alternate-runtime audit. No dependency install.
Static formatting/compilation precedes the freeze. Results and roadmap
are publication documents outside the prospective six-source freeze.

## Decision boundary

Pass requires complete independent rational equality, full mathematical
oracle equality, the fixed census, endpoint/negative-control certificates,
zero-error BT agreement, scale audits, and evidence-boundary tests.
Passing this gate establishes only the conditional, bound-aware toy
calculus and implementation agreement. It does not measure an actual e,
establish iid or zero forbidden support for an apparatus, identify absolute
scale, reconstruct gravity, or resolve the broad-class collision.
The next gate must be chosen from the resulting remaining premise gaps,
with a prospective contract before new calculations or acquisition.
