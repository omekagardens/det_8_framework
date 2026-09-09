# QR-05BI results: interval-valued interior response

9 September 2026 (Pacific/Honolulu). The bounded gate passes.
The two exact implementations agree on **126 position/interval reports
and 105 menus**. Their inner and outer hypothesis sets, and separately
their target sets, coincide in **101 menus**. Four remain bounded rather
than exact. All zero-width controls recover the selected BH results.

Every feasible menu with a nonzero response width is target-ambiguous
in this fixed run. This is compatible with knowing its target set
exactly: an exactly determined interval is not a uniquely determined
number. The remaining certificate gap concerns additional possible
profiles, not a failure to establish those menus' existing ambiguity.

See the [frozen model and checking contract](README.md),
[input](protocol.json) and [complete capture](results.json).
These are supplied population intervals, not statistically calibrated
confidence intervals or observed apparatus errors. Geometry remains
supplied, and no ontology or changed physical law is assumed.

## What changed, and what stayed fixed

Keep the square, measure, profile family and target:
f=c·φ+θb, b=u(1−u)v(1−v),
q=(1/9,1/18,1/18,1/36,1/144).
Exact corner means fix c. The fifth role has one fixed, unknown position
in a supplied finite menu. Only its population mean varies, over
J=[max(−1,m_cc−r),min(1,m_cc+r)], for r=0,1/64,1/8.
There is no position prior, mixing or per-shot movement.

At each possible position z, invert m=r_z+s_zθ with s_z=b(z)>0.
This gives a closed data interval D_z(J). Global-validity constraints
depend on c, not on the candidate position: each Bernstein coefficient
and actual point value is A+Bθ. Solve their scalar inequalities
exactly, then intersect with D_z(J) and project T=t0+θ/144.

The capture retains **35 affine patches**, **315 coefficient pairs**,
**630 zero scalar reconstruction residuals**, and **63 affine witness
pairs**. The four half-square leaves give sufficient global bounds;
the nine actual-point witnesses give necessary bounds. The root net
is diagnostic, not an extra veto. Zero slopes, signed slopes, inclusive
endpoints, empty constraints and all-real constraints are kept distinct.

The old sufficient interval remains visible. Six of the seven cases
have matching global inner and outer bounds; asymmetric does not:

| Case(s) | Old sufficient θ | Refined sufficient θ | Necessary θ |
|---|---|---|---|
| zero, quarter_interior, unit_interior | [−16,16] | [−16,16] | [−16,16] |
| plus, constant_corners_zero_interior | {0} | [−32,0] | [−32,0] |
| minus | {0} | [0,32] | [0,32] |
| asymmetric | [−16/3,16/3] | [−13,31/3] | [−52/3,44/3] |

In each case θ=0 belongs to both sufficient routes, and their union
is connected. Data intersection and target projection preserve the
verified inclusions old⊆inner⊆valid⊆outer. Matching bounds determine
the globally valid set within this profile family, not outside it.
Generic helper tests also cover disconnected and unbounded unions.

## Complete sets versus unique targets

Each budget has 42 position reports and 35 menus:

| Budget / radius | Feasible / infeasible menus | Identified / ambiguous / infeasible targets | Exact / bounded menu sets | Exact position sets |
|---|---|---|---|---:|
| point / 0 | 33 / 2 | 26 / 7 / 2 | 35 / 0 | 42 |
| narrow / 1/64 | 33 / 2 | 0 / 33 / 2 | 33 / 2 | 41 |
| wide / 1/8 | 34 / 1 | 0 / 34 / 1 | 33 / 2 | 41 |

The menu exact/bounded counts apply separately to hypothesis sets
and target sets; they happen to agree here. None of these fixed menus
has unresolved existence or target status. This does not mean that
every profile inside its outer bound is valid. In particular, certified
ambiguity needs only two distinct inner targets, not a complete solution
of the admissible set. Generic tests retain unresolved existence,
unresolved target status, and target exactness without hypothesis exactness.

For zero, the all-position target changes from {0} to
[−1/324,1/324] under the narrow budget and [−2/81,2/81] under wide.
Both nonpoint sets are exact and ambiguous. Under the narrow budget,
the center-only set is [−1/576,1/576]. Restricting position information
therefore helps this example, but cannot remove the supplied response
width. No strictly improved precision is promised for every restriction.

For plus, the old route retains only T=1/4. The refined exact target
sets are [20/81,1/4] and [73/324,1/4] for narrow and wide. Treating
the old conservative admission as the full model would hide valid
alternatives. The constant-corner/zero-interior old route is empty
under all three budgets, while the refined route certifies existence.

For unit_interior, equality_pair remains infeasible at all three widths.
shifted_pair is infeasible at point and narrow but becomes feasible
and ambiguous under wide. This is expected under a wider set of allowed
population means, not a new measurement or a changed polynomial family.

## Gaps are not filled by a hull

For quarter_interior with all positions, the point target set has
four elements. Under the narrow interval it becomes exactly

```text
[5/192,17/480] ∪ [5/108,17/324].
```

Its genuine open gap is (17/480,5/108), containing the retained
midpoint 353/8640. The hull [5/192,17/324] includes that excluded
value and is not the answer. Under wide the components coalesce into
the exact interval [1/72,2/27]. Coalescence does not indicate increased
precision: the widened data set contains the earlier alternatives.

The constant-corner wide all-position set is also disconnected:
[1/36,25/324] ∪ [1/10,11/72]. Across point/narrow/wide, respectively
7/7/4 menus have an inner-union gap, and 7/8/6 have an outer-union gap.
An inner gap means only absence of a certificate there. An outer gap
excludes that target within the declared family, data and menu. The
two coincide only where the bounds justify that conclusion.

Every union is sorted, merges overlap or touching endpoints, and retains
its actual open gaps. Empty unions have null hulls, not a fabricated
zero result. Point⊆narrow⊆wide and exact menu filtering pass through
all retained routes. These are non-strict set inclusions.

## The one localized remaining validity question

Only asymmetric/near_corner has nonmatching data-intersected bounds,
and only under the two nonzero widths:

| Budget | Data θ interval | Inner θ | Outer θ | Additional outer target component |
|---|---|---|---|---|
| narrow | [388/27,412/27] | empty | [388/27,44/3] | [311/1944,35/216] |
| wide | [304/27,496/27] | empty | [304/27,44/3] | [269/1944,35/216] |

BH's point alternative remains refuted, exactly as before. Widening
the response admits smaller θ values that the existing physical grid
does not all exclude, but the existing subdivision certifies none of
these near-corner intervals. Neither “valid” nor “invalid throughout”
follows for those remaining outer portions from this budget.

Consequently all and center_near have bounded hypothesis and target
sets under narrow and wide: precisely four menu reports. Their other
positions already have certified positive-width target intervals, so
existence and ambiguity are settled. A better global-validity bound
could decide additional alternatives; it cannot restore target uniqueness
with these same already-certified alternatives and response data.

For example, asymmetric/wide/all has inner target
[29/540,221/1728] and outer target
[29/540,221/1728] ∪ [269/1944,35/216]. The first interval is certified;
the second is unresolved. The gap between them is outside even the
outer set. No claim is made that either bound is an attained extremum
of the full globally valid family where they disagree.

## The response interval specifies one coupled law family

Each case retains all **32 affine branch probabilities** and all
**32 diagonal entries per unnormalized branch state**, plus the averaged
state: 224 affine branches, 7,168 branch-diagonal pairs and 224
averaged-state pairs across seven cases. Every pair uses the same
interior mean m. Zero-probability branches remain present.

All 42 budget-endpoint checks pass: probabilities and state entries
are nonnegative, probability sums and averaged traces are one, and
branch-trace residuals are zero. Since the entries are affine, the
endpoint checks establish these properties throughout each interval.
The signed slope matrices themselves need not be positive.

The test oracle additionally checks complete laws at several scalar
means. Explicit controls show why a midpoint law loses alternatives
and why independently maximizing probability entries can violate
normalization. This is a coupled one-parameter family, not an entrywise
uncertainty box or a posterior distribution over models.

These diagonal five-qubit laws are Bernoulli-equivalent. Their equality
at fixed role means is not equality of spatial fields, evidence of
quantum advantage, or a derivation of geometry from quantum records.

## Verification and source history

The first source freeze and first capture succeeded. Primary sparse
quantum/monomial/Bernstein conversion and independent beta/Bernoulli/
interpolation/de Casteljau reports agree with native types preserved.
A third oracle uses Boole integration, Gram moments and cofactors,
scalar endpoint laws, a breakpoint-arrangement constraint solver, and
connected-component interval unions.

All **43 tests passed** in isolated CPython 3.14.0 normally and optimized
(23.245 s and 24.093 s). Zero Python assert statements occur in the
tests; the checks remain active under optimization. Both complete driver
replays passed and retained all eleven frozen source identities and
unchanged freeze/capture bytes.

Exactly one isolated CPython 3.11.6 reference-only audit made one analyze
call (0.3433 s) and matched the full mathematical report: **298,512
canonical bytes**, SHA256
`18fa882b5a6b65de1a53c9f21d26d03c39511950d116a4a43b56423546476fb8`.
It verified the protocol/input, all eleven source files and the
freeze/capture bytes before and after. Only the verified current
reference executed; primary, driver, tests and historical executors did
not run in that audit. This is not a Python 3.11 full-suite claim.
Recorded timings are not benchmarks.

The selected zero-width restriction matches six-position geometry,
seven cases, 42 point coefficient/target/classification hypotheses,
1,890 root/leaf coefficient values, 378 actual witness values and
35 point menus. Complete evaluated laws match seven public laws and
42 candidate laws, together contributing 1,568 branch rows. This is
not a replay of all BH fields, its earlier BG restriction, historical
test suites or prior audit/publication process. No old executor ran.

Evidence tests reject raw type substitutions, missing and late report
fields, convexification of genuine gaps, null/empty/all-real confusion,
input mutation, wrong source/cache state, malformed/oversized JSON,
duplicate keys, nonfinite/float values and changed publication bytes.
Both protocol hashes and parses use their respective same byte snapshots.
Capture is create-only; replay is read-only. Fault injections stay in
memory or temporary fixtures, not in retained evidence.

Prefreeze work included formatting, pairwise-iteration/dictionary-items
lint cleanup and adjustment of a test helper's default argument. **No post-first
source, protocol, mathematical or test correction was required.** All
three response budgets and the certificate/witness grids were fixed
before evaluation. No failed first capture is hidden.

| Artifact | Bytes | SHA256 |
|---|---:|---|
| source-freeze.json | 2,320 | `dafe9c9e0c04d0d49214735ac8048e097fac2402d45b75377396ecc186f448cd` |
| results.json | 1,703,421 | `79b4dc506585ab1117c39b6bee86c10c7fe0dec469cf4633a47affcf1bc1dd29` |

Use the [model sheet's commands](README.md#source-bound-execution-and-acceptance)
to replay or test; do not overwrite the capture. Publication starts from
pushed BH commit `4ac7848a27d184dd857606ba04afeb7d8b2e0877`.
Separate core, RET, applications and other dirty work are outside scope.
The local pre-run check found no timing-sensitive RET rehearsal.

## Next proposed gate: QR-05BJ, fixed-budget interval refinement

Keep BI's exact corners, response budgets, finite position menus, profile
family and coupled laws. Prospectively freeze one additional refinement:
16 quarter-square Bernstein leaves and the corresponding 5×5 physical
witness grid. Retain BI's half-square/nine-witness bounds as the baseline.
Compute all new affine constraints independently and prove nested bounds:
the certified inner set cannot shrink and the necessary outer set cannot
grow at unchanged data. Carry those inclusions through each position and
menu target union without replacing unions by hulls.

The question is whether this fixed extra budget resolves or narrows
the two asymmetric near-corner intervals and the four bounded menus.
Do not choose further subdivisions after seeing their answers or promise
complete closure; an unresolved remainder is an acceptable recorded result.
Actual witness violations, not failed coefficient bounds, must justify
exclusion. Added grid points are mathematical checks, not acquired data.

BJ is conceptual only and has not been run. Exact general extrema with
potential algebraic endpoints are a separate, larger contract. Finite-shot
coverage, noisy corners, continuous unknown positions, RET integration,
apparatus calibration, inferred metrics and gravity dynamics remain outside
this next gate. The useful advance here is controlled inversion and honest
admissible-set uncertainty within a supplied geometric model.
