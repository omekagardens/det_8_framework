# QR-05BK: analytic upper-admission boundary

9 September 2026 (Pacific/Honolulu). Prospective acceptance contract:
initially recorded before implementation, with interface clarifications
during static review; finalized before polynomial expansion, root isolation
or fixed-input evaluation. One bounded exact-mathematics gate on the unchanged
supplied model; no new observation, physical law or ontology premise.

## Model and scope

On Q=[0,1]² let u=t+x, v=t−x, c=1, signature (+,−), dμ=du dv/2,
V=1/2, F=V²f, σ=V⁴=1/16 and R=(1−u)(1−v)/2. Then
T=σ⁻¹∫F R dμ=∫f(1−u)(1−v)du dv.
Set φ=((1−u)(1−v),u(1−v),(1−u)v,uv),
b=u(1−u)v(1−v) and f=c·φ+θb. The coefficient integrals are
(1/9,1/18,1/18,1/36,1/144). Global admission is |f|≤1 on Q.

The complete unchanged BJ protocol is embedded as model. Independently
recompute its whole mathematical report locally, including all seven
cases, six position alternatives, three supplied population-mean intervals,
five menus, quantum affine laws, old restrictions and quarter-square
certificates. Preserve it as bj_model. Retained answers only authenticate
that restriction after recomputation; never import a historical engine.

Only the asymmetric corners (1/2,−1/3,2/3,−1/2) need a new analytic
certificate. Their bilinear part is
r=1/2−5u/6+v/6−uv/3, and T=13/216+θ/144.
The interior mean remains 1/3, with point/narrow/wide radii 0,1/64,1/8.
All data, positions and menu labels stay fixed. No sharp negative-θ
threshold is attempted; inherited negative pieces must be sufficient for
the actual supplied data before their exact resolution can be asserted.

## Why the positive boundary is global and closed

For θ≥0, f≥r≥−1/2, so only f≤1 matters. On the open square define
h=(1−r)/b. Since b>0 there, θ is valid precisely when θ≤inf h;
on the boundary b=0 and the corner convex combination r is already valid.
The four reciprocal-product terms are

```text
h = (1/2)/(uv) + (4/3)/((1−u)v)
  + (1/3)/(u(1−v)) + (3/2)/((1−u)(1−v)).
```

For g(x,y)=1/(xy), g_xx=2/(x³y), g_xy=1/(x²y²),
g_yy=2/(xy³), with positive determinant 3/(x⁴y⁴).
Affine reflections preserve positive-definiteness. Positive weighted sums
therefore make h strictly jointly convex. Also 1−r≥1/3 and b tends to
zero at every boundary approach, so h diverges there. It has exactly one
interior global minimizer. Minimization over u produces an attained
strictly convex one-variable function H: applying strict joint convexity
to the two minimizing pairs proves this statement, not a generic claim
that all infima preserve strict convexity.

Its minimum β is admitted including equality. At the same interior contact
point, every θ>β makes f>1 because b>0. This proves necessity, sufficiency,
sharpness and closedness of [0,β], not merely stationarity or a grid bound.

## One-variable construction and independent elimination

All polynomials have ascending exact rational coefficients. Let

```text
A=3−v, C=5+2v, D=v(1−v), δ=2v−1,
S=A(A+C), k=CD−2Sδ,
u_min=√A/(√A+√(A+C)),
H=(11+2√S)/(6D),
H'=(11δ√S−k)/(6√S D²).
```

For 0<v≤1/2, the derivative is strictly negative. Above 1/2, retain
only roots satisfying k>0; together with S>0 and the squared equation
this restores the unsquared positive-radical condition.

Primary quantum.py constructs Q=k²−121δ²S and exactly divides by C.
Independent reference.py derives stationarity equations
U=C u²+2Au−A and V=p+qu, with p=A'D−AD', q=C'D−CD', then constructs
E=Cp²−2Apq−Aq². The raw identity is Q=C E:
2p+q=11δ and k=−11p−Aq provide a symbolic check.
Primitive leading-positive integer normalization and squarefree reduction
must retain their content/factor relationship. Do not call the resulting
defining polynomial irreducible or minimal. Require this fixed eliminant
to be squarefree (if not, fail the fixed gate instead of changing its
meaning); report raw E, its normalization scalar and defining P.

Isolate every real P root in (0,1), not just the desired root.
Primary uses exact Sturm counts. Reference uses Bernstein/Descartes
variation with exact rational subdivision. The common output is the first
dyadic cell at depth at least 24 with exactly one root and nonroot endpoints;
a rational midpoint root is instead a singleton. Test the midpoint before
terminal-cell emission, including at depth 24; subdivisions used only for
an internal count must not otherwise change the canonical output.
Prune zero-root cells;
traverse left before right. Both algorithms must certify the same canonical
cells, even if the reference needs finer internal subdivisions to certify
an ancestor count. Endpoint roots are handled explicitly, not counted as
interior roots. Report root cells in increasing order. Bounds: maximum
polynomial degree 12, recursion depth 64, visited nodes 4096 per isolation.
Reject zero and repeated-root polynomials; constants return no roots.
Stop/fail closed if an isolation, count or strict sign cannot be certified
within these prespecified bounds; do not raise them after seeing results.
The fixed output cells must also separate the v=1/2 and k sign tests.
Label each cell admissible, rejected_nonpositive_delta or
rejected_wrong_radical_sign. Require exactly one admissible root α.
Do not divide away v=1/2 without explicitly checking it.

Use the common rational polynomial images

```text
u(α) = 11δA/(11δA+k),
β(α) = (121δ+2k)/(66δD).
```

The reference may derive u=−p/q and β=(A+Cu)/(6u(1−u)D)
internally but must independently verify the common images.
Record exact interval-Horner enclosures for k, u, β and image denominators;
require the admitted contact coordinates in (0,1), β>0 and positive
denominators. Clear denominators in f−1, ∂uf and ∂vf at these images:
all three polynomial remainders modulo P must be zero. This checks contact,
but the preceding convexity/divergence/sign argument is what proves globality.
β is exactly the rational image of the isolated α, not either endpoint
or midpoint of its rational enclosure. No floating optimizer, fitted
threshold, decimal equality or unproved root deletion is allowed.

## Algebraic endpoints and unchanged-data propagation

An endpoint is a Fraction or
{kind: "beta_affine", offset: Fraction, scale: Fraction}, meaning offset+scale β.
Scale zero normalizes to a Fraction. The exact boundary is (0,1);
the target boundary is (13/216,1/144) in this representation.

This is a bounded fixed-case algebraic comparator, not a general SDK.
Equal normalized coefficients compare equal. Otherwise enclose the affine
difference using the certified rational β enclosure; a strictly positive
or negative interval proves the order. If it includes zero, raise an
unresolved-order error. Never guess, widen evidence claims, or treat touching
enclosures as equality. No extra isolation budget is granted by comparison.

For each asymmetric data interval D_z(J), first intersect the BJ inner
and outer θ sets with (−∞,0]. They must coincide; preserve that negative
piece exactly. Intersect D_z(J) with [0,β] for its exact nonnegative
piece, merge them, and project through 13/216+θ/144.
If the negative equality fails, this fixed complete-resolution contract
fails; it must not silently discard the uncertain part.
Verify BJ inner⊆new exact⊆BJ outer for hypotheses and targets.
Every already exact BJ set must remain identical. Check point⊆narrow⊆wide.

Menu hypotheses preserve position labels. Form sorted closed target
components, merging overlap and touching, and retain the hull and every
open gap. Keep gaps as endpoint pairs (no new midpoint-oracle API).
For each menu distinguish set exactness, existence and target identification:
empty is infeasible; one singleton component is identified; otherwise
nonempty is ambiguous. Exactness does not mean an identified target.
Preserve settled BJ existence and target classifications. The other six
cases' exact sets remain available unchanged in bj_model.

## Common report and helper contract

The native report has exactly bj_model, certificate and resolution.

certificate fields:

- raw_eliminant: dense Fraction polynomial E;
- normalization_scalar: Fraction with E=scalar*P;
- defining_polynomial: primitive leading-positive dense Fraction P;
- roots: ordered records {interval: [lo,hi], classification: string};
- alpha_interval: selected [lo,hi];
- k_interval: selected interval-Horner range;
- u_image and beta_image: {numerator: dense polynomial, denominator: dense polynomial};
- u_interval, beta_interval: exact rational interval-Horner image ranges;
- denominator_intervals: {u: [lo,hi], beta: [lo,hi]};
- contact_remainders: {value: [0], du: [0], dv: [0]};
- convexity: {corner_gaps: [1/2,4/3,1/3,3/2], hessian_determinant_numerator: 3,
  minimum_corner_gap: 1/3};
- status: "exact_positive_boundary".

Use the displayed unreduced common image numerator/denominator expressions,
trimmed dense coefficient lists; do not normalize each route differently.
The Hessian determinant numerator and summary counts are native integers;
polynomial, image, interval, corner-gap and minimum-gap quantities are Fractions.
Only remaining_global_negative_gap is the declared native boolean.

resolution fields: case_id ("asymmetric"), positive_theta ([[0,beta]]),
budgets and summary. Each budget: id, response_interval, positions, menus.
Each position: position_id, data_theta (unchanged BJ interval),
negative_theta (preserved rational union), theta (exact union),
targets (exact projected union), status ("exact").
Each menu: id, position_ids, hypotheses (nonempty position entries with
position_id, theta, targets), target_set ({intervals,hull,gaps}),
existence_status ("feasible" or "infeasible"), target_status
("identified", "ambiguous" or "infeasible"), status ("exact").
Empty hull is null; gaps are [left upper,right lower].
summary fields: resolved_positions (18), resolved_menus (15),
collection_exact_positions, collection_exact_menus, remaining_global_negative_gap
(true). Counts of complete-collection exactness are computed, not substituted
for invariant checks or made acceptance targets.
Count positions by exact hypothesis sets (inner_theta equals outer_theta);
count menus only when both hypothesis and target sets are exact. Add the
new resolved records to the unchanged other six cases, without double counting.

Common independently implemented test interfaces:
_isolate_unit_roots(poly, depth, max_depth, max_nodes);
_beta_affine(offset, scale);
_endpoint_compare(left, right, beta_interval);
_merge_endpoint_intervals(intervals, beta_interval).
Inputs use Fractions, ascending polynomials; helpers reject malformed types,
nonfinite/unordered intervals and excess budgets. Isolation degree cap is 12.
Return root intervals only; comparator returns −1,0,+1 or raises ValueError.
Mutating inputs, Python assert-only validation, floating arithmetic and
cross-engine imports are forbidden. Engines may carry their own prior
implementation locally and expose analyze(protocol), without fixed computation
at import. No requirement to match algorithm-specific internal proof trees.

## Evidence lifecycle and bounded execution

Authoritative base e608e472b9fd6251e294a988010ee4c1bc04f183 on ret.
Keep unrelated dirty RET/core/application files and temp_qr.md untouched.
Timing-sensitive RET rehearsal takes priority: inspect narrowly before runs
and pause this work if it is active. Do not install dependencies or run
broad repository tests. Standard-library Python only.

Six sources (this README, protocol.json, quantum.py, reference.py, study.py,
test_qr05bk.py) and five pinned BJ inputs (README, RESULTS, protocol,
source-freeze, results) form the source freeze. The driver authenticates the
whole embedded BJ protocol and whole recomputed BJ mathematics, not its
historical execution lifecycle. Bounded same-snapshot JSON reading rejects
duplicates, floats, special values, symlinks and oversized artifacts.
Maximum artifact/source size remains 4,000,000 bytes.
Exclusive creation and source checks before/after execution/publication
preserve prior evidence; complete native-type route comparison precedes
encoding. No fixed-input computation until all six sources have been
written, statically reviewed and frozen.

Retain the first capture or first failure. Any post-first-run correction
requires a separate numbered source freeze/capture and explicit original
failure record; do not overwrite or erase the chronology.
After a successful capture, run the dedicated unit suite in normal and
optimized Python, full driver replay in both modes, and exactly one bounded
reference-only alternate Python 3.11.6 analyze audit against the canonical
whole mathematical report. Hash all source/evidence files before and after.
Static formatting before the first run is allowed and recorded.

Tests must cover independent polynomial/contact identities, complete root
census and rejected roots, simple known polynomial roots and exact dyadic
midpoints, cap failures, malformed inputs, squared-root sign guards,
β-affine exact endpoint retention and unresolved-order failure, interval
union/gap correctness, preserved negative pieces, full nesting and inherited
answers, closed contact admission and θ>β witness reasoning, fresh source
execution, corrupted protocols/evidence/freeze and source/publication races.
Do not change fixtures or tolerances to obtain an expected result.

This gate has no metric inference, Einstein dynamics, ontology proof,
quantum advantage, empirical calibration, confidence-level, general-purpose
optimization or sharp negative-boundary claim. Its application is an exact
admission and partial-identification certificate in this supplied model.
