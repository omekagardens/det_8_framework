# QR-05BH: certified global-admission refinement

8 September 2026 (Pacific/Honolulu). This finite protocol precedes
implementation and fixed evaluation. Refine global-validity certificates
without changing the means, positions, profile family or quantum experiment.
No ontology premise, apparatus data, RET integration or new law is involved.

## Fixed mathematical and quantum model

Supply Q=[0,1]², u=t+x, v=t−x, c=1, signature (+,−),
dμ=du dv/2, V=1/2, F=V²f, σ=V⁴=1/16 and R_Q=(1−u)(1−v)/2.
The target is T=σ⁻¹∫F R_Q dμ=∫f(1−u)(1−v)du dv, with family

\[
f=c_{00}(1-u)(1-v)+c_{10}u(1-v)+c_{01}(1-u)v+c_{11}uv
  +\theta u(1-u)v(1-v).
\]

The target row on (c00,c10,c01,c11,θ) is
q=(1/9,1/18,1/18,1/36,1/144). Global validity in this stipulated
response model means |f|≤1 throughout Q. The older sufficient condition
max|c|+|θ|/16≤1 remains recorded; it is not necessary.

Four roles have known corner positions (00,10,01,11). The fifth, cc,
has one fixed but unknown position in a finite supplied menu; its role
name does not disclose a coordinate. Six possibilities are fixed:
center (1/2,1/2), equality_u (1/3,5/8), equality_v (5/8,1/3),
shift_low (1/3,1/2), shift_high (2/3,1/2), near_corner (3/4,3/4).
The five menus are all, center_only, equality_pair, shifted_pair,
center_near, explicitly listed in the [input](protocol.json).
There is no position prior, mixture or per-shot random movement.

Seven exact five-role population vectors are retained:

| Case | Means in (00,10,01,11,cc) order |
|---|---|
| zero | (0,0,0,0,0) |
| plus | (1,1,1,1,1) |
| minus | (−1,−1,−1,−1,−1) |
| quarter_interior | (0,0,0,0,1/4) |
| unit_interior | (0,0,0,0,1) |
| constant_corners_zero_interior | (1,1,1,1,0) |
| asymmetric | (1/2,−1/3,2/3,−1/2,1/3) |

For each candidate z, A_z has top rows (I₄,0) and bottom (φ(z),b(z)).
Its inverse yields c=m_corners and θ_z=(m_cc−φ(z)·c)/b(z), since
b(z)>0. Independently reconstruct responses and integrate the target.
These 42 polynomials are unchanged candidates, not new experiments.

Each role supplies a fresh independent diagonal qubit ρ=(I+mZ)/2,
Z=diag(1,−1), with ideal projectors Π_x=(I+xZ)/2, x∈{−1,+1}.
Exact population means are not finite-shot estimates. Recompute seven
public and 42 candidate complete laws, all 1,568 branches including zero
outcomes, and unnormalized/averaged 32-dimensional state diagonals.
Every candidate is locally state-valid at sampled sites, even if globally
refuted. Internal role-state equality is not equality of spatial quantum
fields. These likelihoods remain classical Bernoulli-equivalent.

## Fixed exact certificates and counterexamples

Use degree-(2,2) tensor Bernstein polynomials
B_i(s)=binom(2,i)s^i(1−s)^(2−i), i=0,1,2. On [a,b]×[c,d],

\[
f(a+(b-a)s,c+(d-c)t)=\sum_{i,j=0}^2 C_{ij}B_i(s)B_j(t).
\]

Rows of C index u/s, columns index v/t. Nonnegativity and partition
of unity on each closed rectangle imply min C≤f≤max C. These
enclosures need not be attained extrema. All family members have
degree at most two in each variable. Equality on nine local nodes
{0,1/2,1}² proves equality of the two degree-(2,2) polynomials,
not just approximate sampling agreement.

The budget is fixed: full-square root net and four covering half-square
leaves ll, lh, hl, hh (u interval first, v second). No adaptive subdivision,
tolerance, optimized partition or post-result budget selection. Retain
all 45 coefficients per candidate and 45 reconstruction residuals.
Root coefficient bounds must enclose every leaf coefficient; root success
implies leaf success. A failed root bound cannot veto successful refinement.

Separately evaluate the original polynomial at the nine physical witness
points {0,1/2,1}² in u-major order. Retain every value and every index
with strict |f|>1. Equality at ±1 is valid. An out-of-range Bernstein
coefficient is a failed certificate, not an actual violation.
Reconstruction nodes and physical witness points have different logical
roles; neither adds observer measurements.

For each candidate:

- certified: old sufficient admission, or every coefficient in every
  covering leaf lies in [−1,1];
- refuted: an actual fixed witness value has |f|>1;
- unresolved: neither condition has been established.

Certificate/refutation conflict raises. Retain certificate routes in order
old_bound, subdivision_bernstein, including both when both apply. Root
certification is diagnostic only. The budget need not decide all candidates;
no positive unresolved count is required. Tests exercise unresolved semantics
without tuning fixed inputs.

The existing 1−16b center profile is a valid-but-excluded improvement
control. The unit_interior near_corner candidate is the sampled-valid
overshoot control. Existing BG collisions retain their laws/targets.
Any changed admitted set comes from the certificate, not extra quantum data.

## Inner and outer hypothesis/target sets

For each menu retain old BG admitted entries, inner certified entries,
and outer entries not explicitly refuted, as position/coefficient/target
triples in menu order. Keep distinct positions even when coefficients
or targets repeat. Exhaustive inversion gives

\[
H_{\rm old}\subseteq H_{\rm inner}\subseteq H_{\rm valid}
\subseteq H_{\rm outer}.
\]

H_valid refers only to the fixed family and finite position menu.
Separately project sorted distinct targets. Inner/outer target images
bracket the true finite target set. Hypothesis-set exactness and
target-set exactness are separate: duplicate targets can conceal
unresolved hypotheses. Do not assume this occurs in the fixtures.

Existence is infeasible only if outer is empty, feasible if inner is
nonempty, and unresolved otherwise. Target status is infeasible if
outer is empty, identified if inner is nonempty and outer has one
distinct target, ambiguous if inner has at least two distinct targets,
and unresolved otherwise. A singleton outer with empty inner does not
certify existence or identification. Proven ambiguity need not mean
the complete target set is known; empty inner alone is not infeasibility.

Empty target hulls are null; otherwise retain minimum/maximum/width.
Hulls do not replace finite sets or carry probability weights.
Menu restriction must equal filtering the all-menu sets at every layer.
No extra existence premise, finite-shot confidence, calibrated position
metadata or unrestricted family is assumed.

## Independent routes and native report contract

The primary statically adapts its BG matrix/monomial engine, then uses
affine monomial substitution and power-to-Bernstein conversion per patch.
The reference statically adapts its independent Bernoulli/beta engine,
recovers the root net by interpolation, and uses half-way de Casteljau
subdivision for leaves. Neither imports the other or a prior executor.
Tests add a third route: verified tensor-Boole moments, a Bernstein
Gram matrix and cofactor inversion recover each patch net without
either engine's conversion helpers.

Both analyze(protocol) functions return the native report below.
F means Fraction; labels are strings, counts/indices native integers.
No floats, boolean numeric values or tuple containers. The bg_model is
the complete freshly recomputed BG mathematical report specified in its
byte-pinned README, not a loaded answer or historical module execution.
Its fields/types/values stay unchanged. The input model embeds the exact
BG protocol. No fixed computation is done at import.

```text
report: {bg_model:BG_report, refinement:[case]}
case: {id, candidates:[candidate], menus:[menu]}
candidate: {position_id, coefficients:[5F], target:F,
  old_admission_status, root:patch, leaves:[4patch],
  subdivision_range_bound:[2F], subdivision_status,
  witnesses:[{position:[2F],value:F,status}], violating_indices:[ints],
  certificate_routes:[strings], classification}
patch: {id, bounds:[[2F],[2F]], coefficients:[3x3F],
  reconstruction_residual:[3x3F], range_bound:[2F], bound_status}
menu: {id, position_ids:[strings], old:[entry], inner:[entry], outer:[entry],
  old_targets:[F], inner_targets:[F], outer_targets:[F],
  inner_range:null-or-range, outer_range:null-or-range,
  existence_status, target_status, hypothesis_set_status, target_set_status}
entry: {position_id, coefficients:[5F], target:F}
range: {minimum:F, maximum:F, width:F}
```

Reconstruction residual is original f minus represented polynomial
at local nodes, u rows/v columns. Bounds use minimum then maximum.
bound_status/subdivision_status are within or outside; witness status
is within or violation. old_admission_status is admitted or
outside_sufficient_class. classification is certified/refuted/unresolved.
Exactness status is exact or bounded. Ordering is as prescribed above,
or inherited from BG; only distinct target projections are sorted.

## Source-bound execution and acceptance

Freeze README, protocol, engines, driver and tests plus five BG
predecessor documents/artifacts before any fixed engine/test evaluation.
Allow static lint and syntax-only checks first. Retain first-capture
failure history and disclose post-first corrections. Strict bounded JSON
(4,000,000 bytes), native-type exact route agreement, nonmutating inputs,
same-byte protocol hashing/parsing, fresh verified source execution,
create-only capture and read-only replay remain required. Before/after
source, freeze and capture identities must remain unchanged.

The historical check compares the entire recomputed bg_model with BG's
retained mathematical report: six positions, seven cases, 42 candidates,
35 menus, 1,568 branches, both witnesses and domain control. It does
not execute historical engines or rerun BG's BF restriction, evidence
tests, Python audit or publication process. Pin all five BG README,
RESULTS, protocol, freeze and capture identities before comparison.

Acceptance requires complete independent reports, all patch identities,
witness grids, preserved BG calculations, monotone sets and correct
three-way/empty-set semantics. Test normally and optimized, then replay
both modes. After first capture use exactly one separate reference-only
audit in another available Python runtime. No RET/core changes,
dependencies, large jobs, apparatus actions, clocks or gravity dynamics.
Small runs must not overlap a timing-sensitive RET rehearsal.

After publication, from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bh.py
python3 -I -O -B test_qr05bh.py
```

Original create-only steps: study.py --freeze source-freeze.json,
then study.py --capture results.json. Read [RESULTS.md](RESULTS.md)
after execution. Hashes check local bytes, not physical authentication
or protection against a hostile host.
