# QR-05BJ: fixed-budget interval refinement

9 September 2026 (Pacific/Honolulu). Prospective model and acceptance
contract, fixed before implementation or numerical evaluation.
One additional mathematical checking budget refines BI's remaining
validity bounds. It adds no acquired measurements or physical laws.

## Unchanged supplied model

Supply Q=[0,1]², u=t+x, v=t−x, c=1, signature (+,−),
dμ=du dv/2, V=1/2, F=V²f, σ=V⁴=1/16,
R_Q=(1−u)(1−v)/2. The target is
T=σ⁻¹∫F R_Qdμ=∫f(1−u)(1−v)du dv.
Let φ=((1−u)(1−v),u(1−v),(1−u)v,uv),
b=u(1−u)v(1−v), f=c·φ+θb.
The five coefficient weights are q=(1/9,1/18,1/18,1/36,1/144).
Global validity means |f|≤1 throughout the supplied square.

Exact corner means fix c. The interior role cc has one fixed, unknown
position within a supplied menu, not a random position or actual
coordinate tag. The positions remain center (1/2,1/2), equality_u
(1/3,5/8), equality_v (5/8,1/3), shift_low (1/3,1/2), shift_high
(2/3,1/2), near_corner (3/4,3/4). Retain all, center_only,
equality_pair, shifted_pair and center_near menus in their BI order.

In (00,10,01,11,cc) order, centers remain:

| Case | Supplied means |
|---|---|
| zero | (0,0,0,0,0) |
| plus | (1,1,1,1,1) |
| minus | (−1,−1,−1,−1,−1) |
| quarter_interior | (0,0,0,0,1/4) |
| unit_interior | (0,0,0,0,1) |
| constant_corners_zero_interior | (1,1,1,1,0) |
| asymmetric | (1/2,−1/3,2/3,−1/2,1/3) |

For each case, point/narrow/wide radii are 0,1/64,1/8 and
J=[max(−1,m_cc−r),min(1,m_cc+r)]. These are supplied sets of population
means, not confidence intervals, finite-shot estimates or fault models.
Only the interior mean varies. At position z, r_z=φ(z)·c and s_z=b(z)>0
give D_z(J)=[(J_lo−r_z)/s_z,(J_hi−r_z)/s_z].
T=t0+θ/144, where t0=q_corner·c.

The [input](protocol.json) embeds BI's complete unchanged protocol.
Recompute its entire mathematical report, retaining it as bi_model.
That includes inverse geometry, all affine law families, endpoint checks,
old/half-square/physical-witness constraints, position sets and menus.
Do not execute a historical module or use retained answers as an oracle.

## One fixed additional certificate and witness budget

Keep the degree-(2,2) basis. Subdivide each of BI's four half-square
leaves into four quarter-square leaves: 16 in total. IDs qij have
u-index i and v-index j, each 0..3, ordered u-major. Bounds are
[i/4,(i+1)/4]×[j/4,(j+1)/4]. Parent IDs ll,lh,hl,hh follow the
two half-indices. The explicit descriptors in the protocol must agree
with these bounds and parentage; verify complete coverage.

Retain every new affine Bernstein coefficient A+Bθ, every individual
allowed θ constraint, and the intersection for each leaf. Retain both
components of its reconstruction residual on local {0,1/2,1}².
Zero residuals establish the polynomial identity for all θ within
the declared degree bound. Parent coefficients are not themselves
actual field extrema. Failure of a coefficient certificate is never
an actual violation or a new reason to reject a certified parent.

Let B1 be BI's half-square sufficient θ interval, B2 the conjunction
of all 144 new leaf-coefficient inequalities |A+Bθ|≤1. Keep the old
sufficient interval O=[−g,g], g=16(1−max|c|).
Let W1 be BI's nine-witness interval and W2 the conjunction of actual
point constraints on {0,1/4,1/2,3/4,1}², ordered u-major.
Retain all 25 affine witness values and allowed intervals, including
the old nine rows. A mathematical witness node is not a sampling site.

Solve linear constraints with closed endpoints. When B=0, the allowed
set is all real if |A|≤1 and empty otherwise; a negative slope reverses
endpoints. Infinite endpoints, an empty interval and a singleton are
distinct. New inner I2=O∪B2 and outer W2 must satisfy

```text
B1 ⊆ B2
I1 ⊆ I2 ⊆ H_valid ⊆ W2 ⊆ W1, where I1=O∪B1.
```

These global sets are θ sets for fixed c. θ=0 belongs to both
sufficient routes for the supplied valid corners, so their union is
connected; verify rather than silently assume that simplification.
Check each inherited witness pair exactly at its matching new node.
No strict improvement, fixed number of resolutions, or general
completeness theorem is an acceptance condition.

## Data intersections, target unions and logical invariants

Intersect O, B2, I2 and W2 separately with each unchanged D_z(J),
then project through t0+θ/144. Retain endpoint-response reconstruction,
the old route, Bernstein route and new inner/outer sets as in BI.
Hypotheses are (position,θ), not merely positions. A position interval
may contain certified, excluded and unresolved portions.
Only the point budget receives certified/refuted/unresolved classification.

For every position and menu verify BI inner⊆new inner⊆new outer⊆BI
outer, separately for hypothesis sets and target projections. When a
baseline set is already exact it must stay identical. Previously
certified ambiguity cannot disappear at unchanged data. Preserve
point⊆narrow⊆wide nesting, and exact filtering by position menus.

Menu target unions are sorted closed components, merging overlap and
touching endpoints, not arbitrary convex hulls. Keep hulls, every open
gap and a midpoint outside the corresponding union. Empty sets have
null hulls and no fabricated zero answer. An inner gap only lacks a
certificate; an outer gap rules out a target in this declared model.
Component counts and numbers of gaps need not be monotone under nesting.

Do not represent new-minus-old differences as closed intervals: exact
set differences can be half-open. This gate retains old and new sets
and verifies inclusions rather than adding a difference-set schema.

Existence is infeasible if outer is empty, feasible if inner is nonempty,
otherwise unresolved. Target status is infeasible if outer is empty;
identified if inner is nonempty and outer is one singleton; ambiguous
if inner contains two distinct values; otherwise unresolved. Exactness
of hypothesis sets and of merged target sets are separate fields.
An exact target interval is not a uniquely identified number.

## Coupled quantum-record laws are unchanged

Each role uses a fresh independent ρ=(I+mZ)/2, Z=diag(1,−1), and
Π_x=(I+xZ)/2 for x=−1,+1. With fixed corners, all 32 probabilities,
every entry of the 32-dimensional unnormalized branch diagonals and
the averaged state are affine in the same interior mean m.
bi_model retains all intercept/slope pairs and both endpoint checks
for each budget, including zero-probability branches. It is recomputed
independently, not read from the historical capture.

New checking nodes do not add qubits, registrations, branch rows or
experimental information. Do not duplicate law families in refinement,
choose a midpoint law, independently vary entry bounds, or assign a
posterior over alternatives. Endpoint positivity extends across each
interval by affinity; slope matrices need not be positive. These
diagonal laws remain Bernoulli-equivalent. Internal role-state equality
is not spatial-field equality or a quantum advantage claim.

## Independent implementations and exact report contract

The primary statically carries only its own BI implementation and uses
affine monomial substitution/power-to-Bernstein conversion for the new
leaves. The reference statically carries only its own BI implementation
and applies a second exact de Casteljau subdivision to its half-square
nets. Tests independently use Boole/Gram-moment/cofactor reconstruction,
breakpoint-arrangement constraints and scalar endpoint law families.
No engine imports another engine or historical executor; no fixed
computation is performed at module import.

F means Fraction; A=[intercept:F,slope:F]. I=[lower:F-or-null,
upper:F-or-null] is nonempty closed; a null interval is empty,
[null,null] is all real. U=[I] is a sorted merged finite union;
[] is empty. Only global/individual constraints may be infinite.
All data-intersected and target intervals are finite. No native
boolean, float or tuple report values. Outcome labels are native ints.

```text
report: {bi_model:BI_report, refinement:[refinement_case]}
refinement_case: {id, constraints:constraints, budgets:[budget]}
constraints: {old_theta:I-or-null, patches:[patch], witnesses:[witness],
  bernstein_theta:I-or-null, witness_theta:I-or-null,
  inner_theta:U, outer_theta:U}
patch: {id,bounds:[[2F],[2F]],coefficients:[3x3A],
  reconstruction_residual:[3x3A],allowed:[3x3 I-or-null],theta_interval:I-or-null}
witness: {position:[2F],value:A,allowed:I-or-null}
budget: {id,response_interval:[2F],positions:[BI_position_report],menus:[BI_menu]}
```

BI_report, BI_position_report, BI_menu and their nested fields are
exactly those in the [pinned BI contract](../qr-05bi-interval-valued-response-2026-09-09/README.md#independent-routes-and-native-report-contract).
The refinement budget intentionally has no endpoint_checks field;
unchanged complete law families and checks occur only in bi_model.
Refinement patches contain exactly the 16 qij leaves; parent IDs are
authenticated input metadata, not additional patch output fields.
Local coefficient rows index u, columns v, degrees 0..2; residuals
are original polynomial minus representation. Cases, budgets, positions
and menus retain protocol order. All rational payloads are exact.

## Source-bound acceptance and reproducibility

Freeze six current files (README, protocol, quantum, reference, study,
tests) and five BI files (README, RESULTS, protocol, source-freeze,
results) before fixed engine or test evaluation. Static lint/syntax
checks may precede freeze. Keep all first-capture failures and disclose
any post-first source or numerical correction. The JSON cap remains
4,000,000 bytes; no outcome-driven cap or budget expansion.

Require whole-report native-type exact independent agreement, complete
third-oracle checks, input immutability, authenticated same-byte protocol
hashing/parsing, fresh source-verified engine execution, strict bounded
JSON, create-only capture and read-only replay, and final source/freeze/
capture byte brackets. Compare the entire newly recomputed bi_model
with stored BI mathematics, but do not rerun its separate BH restriction,
test suite or audit/publication lifecycle. Only current engines execute.

Acceptance includes all affine identities/constraints, old-witness
agreement, nested global/position/menu sets, complete unchanged coupled
laws, exact-set persistence, logical/gap/empty-set semantics, and evidence
mutation tests. Run normal and optimized tests and complete replays.
After first capture run exactly one reference-only audit in another
available Python runtime. Finite results remain finite; no calibration,
apparatus, RET/core/dependency changes, clocks or gravity work is included.
Small runs must not overlap a timing-sensitive RET rehearsal.

After publication, from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bj.py
python3 -I -O -B test_qr05bj.py
```

Original create-only steps are study.py --freeze source-freeze.json,
then study.py --capture results.json. Read [RESULTS.md](RESULTS.md)
afterward. Hashes establish local integrity, not protection from a
hostile host or physical authentication.
