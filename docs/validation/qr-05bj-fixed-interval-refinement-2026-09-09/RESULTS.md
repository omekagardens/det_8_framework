# QR-05BJ results: fixed-budget interval refinement

9 September 2026 (Pacific/Honolulu). The bounded gate passes.
The additional fixed refinement makes **103 of 105 menu sets exact**,
up from 101 in BI. It completely excludes the narrow asymmetric
near-corner alternative and certifies part of the wide alternative.
Two wide-menu sets remain bounded rather than exact.

All previous exact sets survive unchanged. Target identification,
ambiguity and existence statuses also remain unchanged: more complete
knowledge of admissible alternatives does not restore uniqueness where
distinct valid targets were already certified. No response data,
sampling positions, quantum laws or supplied geometry changed.

See the [prospective model and checking rules](README.md),
[input](protocol.json) and [complete capture](results.json).
The entire freshly recomputed BI mathematical report is retained under
bi_model; the additional checking results are under refinement.

## The fixed refinement and its guarantee

The profile remains f=c·φ+θb, b=u(1−u)v(1−v), with exact corners
and target T=t0+θ/144. Response radii remain 0,1/64,1/8 at the same
six possible positions and five menus. Their uncertainty is supplied
population uncertainty, not calibrated confidence or acquired noise.

The new budget subdivides each of four half-square leaves into four
quarter-square leaves, with unchanged degree-(2,2) Bernstein basis.
It retains **112 new case-specific patches**, **1,008 affine coefficient
pairs**, **2,016 zero scalar reconstruction residuals**, and **175
affine actual-point witness pairs** across seven cases. Each case has
16 leaves and a fixed 5×5 witness grid. All nine old witness rows are
present and identical in that grid.

Independent Gram-moment reconstruction also verifies the parent-to-child
coefficient maps. Each map has nonnegative entries and row sums one.
Tensor application to both intercept and slope gives every new affine
net exactly. Thus a successful parent coefficient bound remains sufficient
for every child, for the whole θ interval, not just selected profiles.
Actual witness inequalities give necessary bounds; a failed coefficient
bound is not used as an actual violation.

The retained inclusions are

```text
B_half ⊆ B_quarter
I_BI ⊆ I_BJ ⊆ H_valid ⊆ O_BJ ⊆ O_BI.
```

Here I is the union of the old sufficient route and the relevant
Bernstein route; O is the actual-witness outer set. The same inclusions
hold after data intersection, per position and per menu target union.
They are non-strict: greater computational effort need not change a bound.

Six of the seven cases already had exact global θ bounds and stay
unchanged. Only the asymmetric case has a changed global enclosure:

| Layer | BI half-square / 3×3 | BJ quarter-square / 5×5 |
|---|---|---|
| Old sufficient θ | [−16/3,16/3] | [−16/3,16/3] |
| Bernstein and combined inner θ | [−13,31/3] | [−61/4,151/12] |
| Necessary outer θ | [−52/3,44/3] | [−52/3,128/9] |

These are global parameter bounds for this fixed corner vector, not
general optimizers or necessarily sharp validity endpoints. The two
data-intersected near-corner intervals below are the only changed position
reports. The negative-θ global gap also remains; it does not create an
additional changed position report in this supplied data menu.

## A new actual witness settles the narrow alternative

For asymmetric/near_corner, the narrow data interval is
θ∈[388/27,412/27]. The new mathematical witness at (u,v)=(1/4,1/2)
has the retained affine value

```text
f(1/4,1/2) = 1/3 + (3/64)θ,
allowed θ = [−256/9,128/9].
```

At the smallest data-compatible θ=388/27, this is **145/144>1**.
The slope is positive, so the entire narrow interval violates the
declared global response bound. This is an actual polynomial-value
argument, not an inference from a failed sufficient certificate.

The previous narrow inner set was empty and the outer set was
[388/27,44/3]. Both are now empty. Consequently asymmetric/narrow/all
and center_near become exact menu sets. They remain feasible and
ambiguous because their other positions already have certified
positive-width target intervals.

For narrow/all, the exact target set is now

```text
[59/864,1003/13824] ∪ [149/1728,155/1728] ∪ [463/4320,1579/13824].
```

For narrow/center_near it is [149/1728,155/1728]. BI's extra outer
component [311/1944,35/216] is excluded. All point-budget position and menu records,
including BH's already-refuted exact near-corner alternative, remain
unchanged. The witness node adds no acquired measurement.

## The wide alternative contains certified and unresolved portions

The wide near-corner data interval is [304/27,496/27]. Its refined bounds are:

| Object | Certified inner | Necessary outer |
|---|---|---|
| θ | [304/27,151/12] | [304/27,128/9] |
| Target | [269/1944,85/576] | [269/1944,103/648] |

Previously its inner set was empty. There is now a continuous certified
portion, as well as the unresolved remainder (151/12,128/9]. The upper
data portion above 128/9 is excluded by the actual witness. One label
for this entire position interval would lose these distinctions.

As an explanatory instance derived from the retained affine certificates,
θ=12 gives m_cc=15/64 and T=31/216. It lies inside the wide interval
and outside BI's sufficient set. Its quarter-leaf coefficient enclosure
is [−1/2,185/192], so the whole supplied square is certified valid.
At the certificate endpoint θ=151/12 the enclosure is [−1/2,1].
That endpoint is a boundary of this certificate, not a claim that the
true global-validity boundary is attained there. These instances are
readouts of the fixed affine certificates, not additional acceptance
fixtures or a changed checking budget.

For asymmetric/wide/all, retain the separate target unions:

```text
inner = [29/540,221/1728] ∪ [269/1944,85/576]
outer = [29/540,221/1728] ∪ [269/1944,103/648].
```

The genuine gap (221/1728,269/1944), with midpoint 4141/31104, is
outside even the outer set. The new certified component increases
the inner union's component count from one to two. Nested sets do not
imply monotone component or gap counts. Hulls still do not replace unions.

wide/center_near has the same second components but first component
[2/27,11/108]. These are the only two menus with nonmatching bounds.
Both remain demonstrably ambiguous. Resolving the residual validity
question could determine more of their target sets, not remove their
already-certified alternative target values.

## Full census and unchanged observations

Each budget has 42 position reports and 35 menus:

| Budget | Exact / bounded menu sets | Exact position sets | Identified / ambiguous / infeasible targets |
|---|---|---:|---|
| point | 35 / 0 | 42 | 26 / 7 / 2 |
| narrow | 35 / 0 | 42 | 0 / 33 / 2 |
| wide | 33 / 2 | 41 | 0 / 34 / 1 |

Exactness counts apply separately to hypothesis and target sets; they
happen to agree in this run. In total 125 of 126 position sets are
exact. Existence counts remain 33/2, 33/2 and 34/1 feasible/infeasible;
none of these fixed menus has unresolved existence or target status.
Generic semantic tests still exercise those legitimate outcomes.

All 101 previously exact menus and 124 previously exact position sets
remain identical. The only changes are the two near-corner position
reports and their four containing menus. Nonempty inner/outer position
counts are 36/36, 36/36 and 39/39. Across point/narrow/wide, 7/7/6
menus have an inner gap and 7/7/6 an outer gap. An inner gap only lacks
a certificate; exclusion requires an outer gap or stronger evidence.

All **224 affine branches**, **7,168 branch-diagonal pairs**, **224
averaged-state pairs** and **42 endpoint checks** remain present once
in bi_model. The same interior mean couples their entries. New checking
nodes add no qubits, branch rows or observed information. Complete
families are neither midpoint laws nor independently variable probability
boxes. They remain diagonal, Bernoulli-equivalent quantum-record laws.

This gate improves mathematical knowledge under the stipulated model;
it does not supply a metric, quantum advantage, apparatus calibration,
RET application evidence, an ontology proof or gravitational dynamics.

## Verification and source history

The first freeze and first capture succeeded. Primary direct affine-power
conversion and independent second de Casteljau subdivision agree on the
entire native report. A third route uses Boole integration, Gram moments
and cofactor reconstruction for every quarter net, breakpoint arrangements
for constraints, and independent scalar endpoint law families.

All **52 tests passed** in isolated CPython 3.14.0 normally and optimized
(48.504 s and 47.883 s). The test source has zero Python assert statements;
checks remain active under optimization. Both full driver replays passed.
The entire recomputed BI mathematics matches stored BI mathematics,
including all geometry, 21 budgets, 126 position reports, 105 menus,
35 affine patches, 315 coefficient pairs, 63 witness pairs, 224 affine
branches and 42 endpoint checks. BI's separate BH restriction, historical
tests and audit/publication process were not rerun. No old executor ran.

Exactly one isolated CPython 3.11.6 reference-only audit made one analyze
call (0.6253 s), matching the entire baseline-plus-refinement mathematical
report: **540,208 canonical bytes**, SHA256
`9aff263629dd08e9c16fdde58e1b4448ef2338463bf92ae382c5251d854198fd`.
It verified all eleven sources, input and freeze/capture bytes before
and after. Only the current reference executed; primary, driver, tests
and historical executors did not run in that audit. This is not a
Python 3.11 full-suite compatibility claim; timings are not benchmarks.

Tests cover affine parent relations, preserved exactness and ambiguity,
signed/zero slopes, empty/all-real intervals, genuine gaps, and membership
witnesses without encoding half-open differences as closed sets. Evidence
tests reject complete/late field mutations, native-type substitutions,
omitted patches or witnesses, wrong leaf parentage/bounds/order, duplicated
law/check payloads, source/cache/input mutation, malformed or oversized
JSON, changed artifacts and overwriting existing outputs. Protocol hashes
and parsing use their respective same byte snapshots. Fault injection
uses temporary fixtures or memory, not modified retained evidence.

Only static formatting cleanup preceded freeze. **No post-first source,
protocol, mathematical or test correction was needed.** Both carried BI
implementation bodies are unchanged apart from analyzer names and module
descriptions. The one added budget was fixed before evaluation; no extra
refinement was chosen to close the remaining cases. The 4,000,000-byte
artifact cap was unchanged. No failed first capture is hidden.

| Artifact | Bytes | SHA256 |
|---|---:|---|
| source-freeze.json | 2,313 | `f8a4f5935abf7b99212878e794fe17f0caccbce82d4585edf574b2b067e19fcc` |
| results.json | 3,080,661 | `04c2092edca46a329e73798a6701985b83a9870b3916c7ff59f65d3396ec969f` |

Use the [model sheet's commands](README.md#source-bound-acceptance-and-reproducibility)
for read-only replay and tests; do not replace the capture. Publication
starts from pushed BI commit `20545605a41540134ff2596710244d525c25e2f6`.
Separate dirty core, RET and application work remains outside scope.
The local pre-run check found no timing-sensitive RET rehearsal.

## Next proposed gate: QR-05BK, analytic upper-admission boundary

Keep all response data, geometry, finite positions and law families fixed.
Address the remaining positive-θ global-validity boundary for the single
asymmetric corner vector, instead of selecting another finer grid.
For θ≥0, f≥c·φ≥−1 because b≥0 and the bilinear basis is a partition
of unity. Only the upper condition f≤1 remains to be settled.

Prospectively derive and verify an analytic reduction for the sharp upper
θ threshold, bracketed by BJ's sufficient 151/12 and necessary 128/9.
The stationary-contact equations f=1, ∂u f=0, ∂v f=0 are a possible
route, but finding a stationary point alone does not certify the global
threshold. Account for all admissible interior candidates, boundary
behavior and any extraneous roots from elimination. A nonrational answer
must have an exact algebraic certificate with a rational isolating interval,
not a forced rational fit or an uncertified floating optimizer output.

Preserve closed-boundary admission and compare any resulting threshold
with the retained BJ bounds and wide-menu target sets. Freeze the exact
elimination/isolation method, resource bound and failure semantics before
evaluation; an unresolved certificate attempt must remain visible.
Do not add arbitrary adaptive grid rounds or new acquired observations.

BK is conceptual only and has not run. General corner families, negative-θ
sharp bounds, continuous-position uncertainty, finite-shot calibration,
noisy corners, RET integration, inferred metrics and gravity dynamics are
separate later contracts. This next step concerns completeness of one
scalar admission boundary within an already supplied geometric model.
