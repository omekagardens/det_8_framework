# QR-05BG results: finite sampling-position uncertainty

8 September 2026 (Pacific/Honolulu). The bounded investigative gate passes.
Full five-site population information need not identify the target when
the fifth sampling position is unknown within the declared finite menu.
Two admitted position/profile hypotheses have identical complete record
laws and internal qubit outputs, but target difference **7/324**.
Conversely, several menus identify the target without identifying position.
These are exact supplied-model results, not evidence for a new physical law.

The [standalone model and prospective protocol](README.md) and
[frozen input](protocol.json) define the calculation. The complete
[capture](results.json) retains all candidates, including local-only
diagnostics outside the sufficient admission class.

## Inversion and the exact finite set

The supplied square has V = 1/2 and σ = 1/16. The normalized target row is
q = (1/9,1/18,1/18,1/36,1/144) on coefficients (c00,c10,c01,c11,θ).
The four corner means fix c. At each strictly interior candidate position z,
the fifth mean fixes

\[
\theta_z=\frac{m_{cc}-\phi(z)\cdot c}{b(z)},\qquad
T_z=q_{\rm corner}\cdot c+\theta_z/144.
\]

All six evaluation matrices have verified two-sided inverses. The compiled
target rows have zero residual; reconstructing every candidate polynomial
at its candidate coordinates reproduces all five supplied means exactly.
The engines then compute each candidate's quantum law from those
reconstructed responses, rather than copying the public law as a proof.

Exhaustive inversion followed by max|c|+|θ|/16 ≤ 1 is an exact
position/coefficient/target set for this finite menu and sufficient class.
Of 42 candidates, **28 are admitted**, including 13 on the boundary;
14 are outside the sufficient class. All 42 have valid local sampled
qubit states, which does not by itself certify a globally valid profile.

The largest menu gives:

| Public case | Feasible positions | Exact distinct target set | Status |
|---|---:|---|---|
| zero | 6 | {0} | identified |
| plus | 6 | {1/4} | identified |
| minus | 6 | {−1/4} | identified |
| quarter_interior | 6 | {1/36,1/32,1/30,4/81} | ambiguous |
| unit_interior | 1 | {1/9} | identified |
| constant_corners_zero_interior | 0 | ∅ | infeasible within this class |
| asymmetric | 3 | {19/270,61/864,19/216} | ambiguous |

Across seven cases and five menus there are **25 identified, 3 ambiguous
and 7 infeasible** reports. These are counts of prespecified analytical
controls, not population frequencies or experimental probabilities.
Every feasible position entry is retained in menu order even when
different positions give the same coefficient vector and target.
Only the separate target projection removes duplicates.

## Missing position information can matter even with full access

For quarter_interior, all four corner means are zero and m_cc = 1/4.
The six position hypotheses give:

| Candidate position | θ | Admission bound | Target |
|---|---:|---:|---:|
| center (1/2,1/2) | 4 | 1/4 | 1/36 |
| equality_u (1/3,5/8) | 24/5 | 3/10 | 1/30 |
| equality_v (5/8,1/3) | 24/5 | 3/10 | 1/30 |
| shift_low (1/3,1/2) | 9/2 | 9/32 | 1/32 |
| shift_high (2/3,1/2) | 9/2 | 9/32 | 1/32 |
| near_corner (3/4,3/4) | 64/9 | 4/9 | 4/81 |

In particular, f = 4b sampled at the center and f = (64/9)b sampled
at near_corner have the same full population vector. Their complete
five-site record-law total variation is zero. All 32 unnormalized
branch-state comparisons agree, as do the full outcome-averaged states.
Their coefficient difference is (0,0,0,0,28/9), and their target difference
is 4/81−1/36 = **7/324**, second hypothesis minus first.
Both have certified admission bounds below one.

Restoring 11 is not a remedy here: 11 is already observed. BF repaired
missing-site access given an exactly known position; BG demonstrates
the distinct missing-position obstruction. Fresh repetitions with the
same undisclosed fixed sampling position have the same complete laws
under the two hypotheses and cannot distinguish them in this model.

This equality concerns role-labeled internal product-qubit states.
It is not equality of spatially localized quantum fields or position
degrees of freedom. No position-dependent preparation tag or hidden
actual-position field is supplied in the measurement input.

## Target identification, position identification and disclosure

Restricting a menu is exactly filtering its feasible hypothesis entries;
the target set can only shrink. For quarter_interior, equality_pair
identifies 1/30 and shifted_pair identifies 1/32, each with two remaining
positions. center_only identifies 1/36. center_near retains the two
targets 1/36 and 4/81. These are alternative supplied information sets,
not an algorithm that learns which menu is true.

The zero control has the same zero profile and target at all six
positions. Its center/near_corner witness has zero target difference,
zero law total variation and no branch or averaged-state differences.
It is genuine position ambiguity with no target penalty.

In this full-corner family, a unique target also determines θ, since
c is fixed and q_b = 1/144 is nonzero. Thus target identification fixes
the coefficient vector here, although it need not fix position.
This differs from BF's reduced four-site access.

Hypothetically disclosing each candidate position yields 28 identified
targets and 14 class refusals with null targets. It does not change
the public quantum law. Disclosure is additional mathematical input,
not measured or authenticated position calibration.

For unit_interior, only center is admitted. The equality_pair and
shifted_pair menus are empty; all, center_only and center_near identify
1/9. For asymmetric, the admitted positions are center, equality_u and
shift_low. Its all-position target hull has width 19/1080, but its exact
target set has only the three values shown above.

The quarter_interior all-position hull [1/36,4/81] has width 7/324.
Its fixed gap probe 17/576, between the first two sorted targets,
lies in the hull but is unattainable in the finite model. The corresponding
center_near probe is 25/648, and the asymmetric all-menu probe is
203/2880. None is an estimate, posterior mean or interpolated target.
Empty menus retain null ranges, not a fabricated zero-width answer.

## Class infeasibility is not physical inconsistency

Every constant_corners_zero_interior candidate lies outside the
sufficient class, so all five menus are class-infeasible. Nevertheless,
its center candidate is f = 1−16b. Since 0 ≤ b ≤ 1/16, this profile
has global range **[0,1]**, with minimum at (1/2,1/2) and maximum at
(0,0). Its admission bound is 2 and its diagnostic target is 5/36.

This gives an explicit globally valid profile rejected by the current
sufficient rule. The capture preserves both facts; it does not silently
expand the admitted set or turn the rule into a necessary condition.
The other excluded candidates retain local laws and targets only;
this one global range certificate is not transferred to them.
Nor does local-law agreement establish unrestricted field recovery.

## Verification and retained history

The first source freeze and first capture succeeded. The primary
matrix/monomial route and independent Bernoulli/beta route agree on the
complete native report: six positions, seven public laws and 42 candidate
laws, with **1,568 branch rows** (812 positive and 756 zero probability).
All 49 laws include 32-dimensional unnormalized branch-state diagonals
and full averaged states. Probability-zero rows remain present.

All **39 tests passed** in isolated Python 3.14.0 normally and optimized
(8.432 s and 8.445 s respectively). Tests include a third complete
native-report oracle using verified degree-five tensor-Boole integration,
cofactor inversion and direct scalar branch calculations. Its synthetic
integration nodes are mathematical checks, not additional measurements.
Both full driver replays pass with the same eleven frozen identities and
unchanged capture. The tests use explicit checks, not Python assert
statements that disappear under optimization.

Exactly one separate reference-only audit in isolated Python 3.11.6
also matches the complete mathematical subreport: **348,899 canonical
bytes**, SHA256
`fc937b3b5a242208bf538878ccd3c6aa4e31daf7691f6a252c756a0a0f37a4f9`.
It made one reference call (0.38000 s) with a fresh external cache.
The input, all eleven source identities, freeze and capture were unchanged
before and after. No primary engine, driver, test suite or historical
executor ran in this audit. This is not full-suite Python 3.11
compatibility evidence; the recorded times are not benchmarks.

The driver retains strict bounded JSON, exact native types, same-byte
protocol hashing/parsing, independent nonmutating route inputs, fresh
verified source execution, create-only publication and final byte
brackets. Tests exercise invalid types and extra fields, late-branch
changes, mutated inputs, stale identities, cache bypass, symlinks,
publication/replay changes and failure-without-replacement. Fault
injections use temporary or in-memory fixtures, not retained artifacts.
There is no new public observer or acquisition API.

Selected BF evidence matches all six positions' geometry and the four
center cases zero, plus, minus and asymmetric (BF's asymmetric_bubble):
coefficients, admission, responses, targets and 128 distinct complete
full-law branch rows, counted once. Both current public and candidate
laws are checked. BF's reduced access, moved-profile branches, score
controls and separate collisions are not rerun or recertified; historical
executors are not imported. The comparison does not invent averaged-state
fields absent from the selected older reports.

Before any fixed evaluation, static review corrected one conceptual
sentence: BG's full corner means and nonzero bubble target coefficient
mean that unique target does imply unique coefficients in this family.
The protocol now states this correctly; both engines and a dedicated
test check it. Position ambiguity can still remain. This prefreeze
correction did not change the finite menu or numerical inputs.
Newly adapted sources were also formatted and statically checked.
**No post-first source, protocol, mathematical or test correction was
required.** No failed first capture is hidden.

| Artifact | Bytes | SHA256 |
|---|---:|---|
| source-freeze.json | 2,337 | `1b0db4a54362ac689bb52a14af78d3191db20b922b39469eba05d1054a2a979c` |
| results.json | 1,971,938 | `1f4aab687899437ffd56ff7e9565256714062a7bdb85c0b45e641bc50c9f9a56` |

Use the normal/optimized test and read-only replay commands in the
[model sheet](README.md#source-bound-execution-and-acceptance). Do not
overwrite the retained capture. Publication starts from pushed BF commit
`219d59750e87a8af625c1870b53fdec8a7ef7fd0`. Separate RET/core, application
and other working-tree changes remain outside this gate. No RET timing
rehearsal was seen in the local pre-run process checks.

## Next proposed gate: QR-05BH, certified global-admission refinement

Keep BG's supplied geometry, population inputs, inverses and candidate
polynomials. Preserve its recorded sufficient-class answers. Prospectively
freeze an exact rational degree-(2,2) tensor-Bernstein conversion and a
bounded rectangular subdivision. Verify conversion against the original
polynomial. If every leaf's coefficients lie in [−1,1], the Bernstein
convex-hull property certifies global validity.

A Bernstein coefficient outside [−1,1] is a failed sufficient certificate,
not proof of an invalid field. Separately freeze rational witness points:
an actual polynomial value with |f| > 1 disproves global validity.
Retain three outcomes: certified (including the old sufficient class),
explicitly refuted, or unresolved. Require certificates and actual
violations never to coexist.

Per menu, certified candidates give an inner set and all not-disproved
candidates give an outer set for globally valid position/profile
hypotheses. Their target projections bracket the finite physical target
set. An empty inner set alone is not infeasibility; unresolved positions
need not prevent inner and outer target sets from coinciding.
The valid-but-excluded 1−16b and a locally valid but globally overshooting
control should test these distinctions under a frozen checking budget.

This proposal has had conceptual review only; **BH has not been run**.
It improves the admission certificate, not the quantum data or position
calibration, and need not decide every candidate. No continuous-position
reconstruction, finite-shot confidence, RET adapter, empirical readiness,
metric inference, gravity dynamics or quantum advantage follows.
