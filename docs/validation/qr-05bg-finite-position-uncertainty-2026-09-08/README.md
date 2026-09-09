# QR-05BG: finite sampling-position uncertainty

8 September 2026 (Pacific/Honolulu). This protocol and its finite menus
precede implementation and fixed evaluation. Exact synthetic population
identification only; no ontology premise, apparatus data or RET integration.

## Supplied spacetime, uncertain sampling position

Supply Q = [0,1]² with null coordinates u = t+x, v = t−x, c = 1,
signature (+,−), dμ = du dv/2, V = μ(Q), F = V²f and σ = V⁴.
Keep the fixed kernel R_Q = (1−u)(1−v)/2 and target

\[
T(F)=\sigma^{-1}\int_Q F R_Q\,d\mu.
\]

The field family is f = Σc_a φ_a + θb, with
φ = ((1−u)(1−v),u(1−v),(1−u)v,uv) and b = u(1−u)v(1−v).
The admitted coefficient class is max|c_a|+|θ|/16 ≤ 1. This sufficient
bound guarantees |f| ≤ 1 everywhere; it is not a necessary condition for
physical validity. No continuum quantum field or gravity source is inferred.

Four stations have known coordinates (00,10,01,11). The fifth, labeled cc,
has one position fixed throughout a run, but only a finite allowed menu is
supplied to the observer. “cc” names a role, not a known center coordinate.
Q, the axes, kernel and profile basis are fixed: uncertain sampling location
is not uncertain spacetime geometry. There is no prior over positions and
no mixture, posterior weighting or random per-shot movement.

At each role a fresh independent qubit has ρ = (I+mZ)/2,
Z = diag(1,−1), with ideal projectors Π_x = (I+xZ)/2, x ∈ {−1,+1}.
The supplied five m values are exact population means, not estimates from
five shots. They define a complete product-qubit law. Keep every
unnormalized branch and probability-zero outcome. Spatial localization is
not an additional quantum degree of freedom in this model; equal role-
labeled internal states are not equality of localized QFT systems.

## Prospective finite menus

The [input](protocol.json) declares these positions:
center (1/2,1/2), equality_u (1/3,5/8), equality_v (5/8,1/3),
shift_low (1/3,1/2), shift_high (2/3,1/2), near_corner (3/4,3/4).
All are strictly interior. Five public menus are fixed: all six,
center_only, equality_pair, shifted_pair and center_near. Each is an
explicit ordered subset, not a probability distribution.

Seven exact population vectors in (00,10,01,11,cc) order are fixed:

| Case | Population means |
|---|---|
| zero | (0,0,0,0,0) |
| plus | (1,1,1,1,1) |
| minus | (−1,−1,−1,−1,−1) |
| quarter_interior | (0,0,0,0,1/4) |
| unit_interior | (0,0,0,0,1) |
| constant_corners_zero_interior | (1,1,1,1,0) |
| asymmetric | (1/2,−1/3,2/3,−1/2,1/3) |

Case names identify public synthetic inputs; none supplies an origin
position. Position IDs label hypotheses or disclosed alternatives, not a
hidden truth field in the measurement data. No position-specific
preparation/calibration tag is used to distinguish identical laws.

## Exact hypothesis inversion and finite target sets

Compile the five coefficient integrals q independently of responses. For
each position z, A_z has top rows (I₄,0) and last row (φ(z),b(z)). Since
b(z)>0, it has a two-sided inverse D_z. For any supplied five means m,

\[
c=m_{\rm corners},\qquad
\theta_z=\frac{m_{cc}-\phi(z)\cdot c}{b(z)},\qquad
T_z=q_{\rm corner}\cdot c+q_b\theta_z.
\]

Re-evaluate the resulting polynomial at that candidate's coordinates to
recover m and independently integrate its target. Do not demonstrate
candidate-law equality merely by feeding the original means back into
every simulator. Retain the full inverse identities, response residuals,
all candidate coefficient vectors, targets and admission bounds.

Each candidate is a joint hypothesis about a position and a profile.
Admit it iff max|c_a|+|θ_z|/16 ≤ 1, including the boundary. A candidate
outside this sufficient class still reproduces valid sampled qubit states;
retain its local branch law as a diagnostic, not a globally certified field.
An empty feasible set means failure of this menu/class combination, not
physical impossibility of the observations.

For each case/menu retain every admitted (position,coefficients,target)
entry in menu order, including positions with identical target values.
Separately form the sorted distinct target values. Zero, one or multiple
values give status infeasible, identified or ambiguous. Target identification
does not imply position identification. In this particular full-corner
model, c is already fixed and q_b is nonzero, so a unique target also fixes
θ and hence the coefficient vector. Report null for an
empty target range, otherwise its minimum, maximum and width. This interval
hull encloses the exact finite set; it need not consist of attainable values.
For multiple distinct targets, retain the midpoint of the first two sorted
values as a fixed gap probe: it lies in the hull but outside the exact set.
That probe is not a posterior mean, interpolation or proposed estimate.

This exhaustive inversion is exact for the declared finite position menu
and sufficient coefficient class: any consistent admitted model must have
the inverted coefficients at one of those positions; every retained entry
constructs such a model. It is not a finite-sample confidence region, a
claim about all globally physical profiles or continuous localization.
Menu restriction must equal filtering the all-position feasible entries;
the possible target set can only shrink.

For each candidate also disclose that exact position as a hypothetical
additional input. Report its target if admitted, or infeasible/null if
outside the declared class. Do not assume the disclosure is a verified
actual position; no physical calibration is performed. Additional shots at
the same undisclosed position cannot separate hypotheses with identical
complete laws, even though finite-shot sampling error is a different issue.

## Prespecified witnesses and admission boundary

Compare center against near_corner for quarter_interior and for zero.
Both members of each witness must be admitted. Keep coefficient and target
differences, complete-law total variation, branch-state disagreement count,
and the difference of full outcome-averaged state diagonals. All differences
are second candidate minus first. The former asks for a genuine target
ambiguity; the latter separates target identification from position ambiguity.
Full corner access already includes 11, so this is not BF's missing-site
obstruction. No targets are averaged across position hypotheses.

The separate constant_corners_zero_interior center candidate is f=1−16b.
Since 0≤b≤1/16, its global range is [0,1], attained at the center and at a
corner. Its sufficient admission bound nevertheless exceeds one. Retain
this exact range certificate and its domain rejection: conservative
admission is not a complete physical-validity test. No such global
certificate is automatically extended to the other rejected candidates.

Keep 32 branches for each of seven public laws and each of 42 candidate
laws, including rejected candidates' local-only laws: 1,568 rows total.
The 35 menu reports add no measurements. All likelihoods remain exactly
classical Bernoulli-equivalent. There is no new public acquisition API,
quantum advantage, field-recovery algorithm outside this domain, or RET
likelihood adapter in this gate.

## Independent routes and native report contract

The primary uses sparse matrix instruments, exact monomial integration and
rational elimination. The reference uses beta integrals, a direct block
inverse and Bernoulli/bit-index formulas without reading/importing primary
helpers. Tests add a verified degree-five tensor-Boole integral oracle,
cofactor inversion and direct scalar branch calculations. Integration
nodes are synthetic oracle inputs, not extra stations. No prior executor
or stored mathematical answer is used as an integration oracle.

Both engines expose analyze(protocol) with no fixed computation at import.
The complete native wire is below. F denotes Fraction; counts/outcomes are
native integers and identifiers/statuses are strings. Collections are
lists/dicts, never tuples; no floats or boolean numeric values. List order
is protocol order unless distinct-target sorting is explicitly specified.
Computational bits are lexicographic, first role most significant, bit 0
means Z+1; outcome order is the product of (−1,+1).

```text
geometry: {volume:F, sigma:F, coefficient_integrals:[5F]}
positions: [{id, position:[2F], basis:[5F], evaluation_matrix:[5x5F],
  coefficient_decoder:[5x5F], left_inverse:[5x5F], right_inverse:[5x5F],
  full_weights:[5F], full_residual:[5F]}]
cases: [{id, population_means:[5F], law:law,
  candidates:[{position_id, coefficients:[5F], admission_bound:F,
    admission_status, reconstructed_means:[5F], reconstruction_residual:[5F],
    target:F, law:law, disclosure:{status, target:F-or-null}}],
  menus:[{id, position_ids:[names], feasible:[{position_id, coefficients:[5F], target:F}],
    distinct_targets:[F], target_range:null-or-{minimum:F,maximum:F,width:F},
    gap_probe:F-or-null, status}]}]
witnesses: [{id, case_id, position_ids:[2names], admission_bounds:[2F],
  coefficients_difference:[5F], means_difference:[5F], target_difference:F,
  law_total_variation:F, branch_state_disagreements:int,
  averaged_state_difference:[32F], disclosed_targets:[2F]}]
domain_control: {case_id, position_id, coefficients:[5F], admission_bound:F,
  admission_status, bubble_range:[2F], profile_range:[2F],
  minimum_position:[2F], maximum_position:[2F]}
law: {rows:[{outcomes:[5ints], probability:F, state_diagonal:[32F]}],
  averaged_state:[32F]}
```

left_inverse is D_z A_z, right_inverse is A_z D_z. full_residual is
(qD_z)A_z−q; reconstruction_residual is candidate means minus public means.
admission_status is admitted or outside_sufficient_class. Menu status is
infeasible, identified or ambiguous. Disclosure status is identified or
infeasible and its target is null on refusal. bubble_range/profile_range
are ordered [minimum,maximum]; the domain control uses minimum_position
(1/2,1/2) and maximum_position (0,0). The witness state count includes
all 32 outcome rows, not only supported ones.

## Source-bound execution and acceptance

Freeze the README, protocol, engines, driver and tests before any fixed
engine/test evaluation, with five BF predecessor documents/artifacts.
Keep first-capture failures and disclose any post-first correction. Use
create-only publication, strict bounded JSON (4,000,000 bytes), exact
native route agreement, input nonmutation, fresh verified source bytes,
and final source/freeze/capture checks normally and under optimized Python.
Static lint and syntax-only checks are allowed before freezing.

Compare all six positions' selected geometry against BF and compare the
four center laws/coefficient vectors for zero, plus, minus and asymmetric
(BF's asymmetric_bubble) against retained data. Count those 128 distinct
full-law rows once. Do not execute historical engines or recertify BF's
reduced access, moved-profile branches, collisions or score controls.

Acceptance requires complete independent reports, exhaustive finite
inverse/set/disclosure certificates, the two admitted witnesses, the
valid-but-excluded control, all full branch states and strict evidence
tests. No RET/core changes, dependencies, large jobs, timing benchmarks,
apparatus actions, clock work or gravity dynamics. Small runs must not
overlap a timing-sensitive RET rehearsal.

After publication, from this directory:

```sh
python3 -I -B study.py --replay results.json
python3 -I -O -B study.py --replay results.json
python3 -I -B test_qr05bg.py
python3 -I -O -B test_qr05bg.py
```

Original create-only steps are `study.py --freeze source-freeze.json`, then
`study.py --capture results.json`. Read [RESULTS.md](RESULTS.md) after
execution. Hashes establish local byte integrity, not physical
authentication or protection against a hostile host.
