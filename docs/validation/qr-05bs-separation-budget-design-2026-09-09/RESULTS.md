# QR-05BS decision record

9 September 2026 (Pacific/Honolulu). **Analytical/design checkpoint complete.**
The [standalone contract](README.md) now separates sampling uncertainty,
rounding resolution and genuine model nonidentifiability. It supplies
exact geometric distance certificates and a conservative sufficient
sample-budget theorem. No new numerical study, confidence-table capture,
large-quota count law, test suite, simulation or acquisition was run.

## What the calculus now tells us

In the supplied two-geometry model, varying the continuous density parameter
traces an exact line segment in the two-probability plane. The target
question is therefore not simply whether two chosen fixtures differ: it is
whether the true probability pair is separated from the ENTIRE segment
with the other geometric target.

The segments' only supporting-line intersection is
(17/80,21/64), realized by flat δ=1 and conformal δ=0. This pair also
has identical whole-point density and different relative-volume targets.
It cannot be separated by collecting more of the same records. Scale
copies are likewise indistinguishable in normalized law.

For a common density premise [0,b], the exact whole-class separation is

```text
D([0,b]) = 3(1−b)/[16(4+b)]   when 0≤b<1,
D([0,b]) = 0                 when 1≤b≤2.
```

| External density premise | Uniform separation between targets | Consequence |
|---|---:|---|
| uniform [0,0] | 3/64 | A sufficient whole-class budget can be certified |
| half [0,1/2] | 1/48 | A sufficient whole-class budget can be certified |
| one [0,1] | 0 | Admits the indistinguishable pair |
| two [0,2] | 0 | Admits the same pair; separated individual points still exist |

The positive-margin pair is attained by flat δ=b and conformal δ=0.
Both coordinates are ordered across the two families for b<1, giving
a global lower proof, not just an endpoint guess. Narrowing B is an
external scientific assumption that requires justification; it must not
be chosen after seeing favorable records.

An exact clipped balancing formula gives the nearest point on each
opposite segment, with a competing-density witness and a matching lower
bound. Under the widest premise, the two interior fixtures have directed
margins 5/16816 and 5/16416. These are both smaller than their selected
second-probability gap 5/7296: a closer competing density exists.
The corresponding nearest densities are 270/973 and 16516/11261.
These values are symbolic derivations, not an executed distance table.

## A sufficient budget, with its conditions attached

For fixed n, four tail allocations 1/80 and grid step h, the unrounded
binomial endpoints lie within empirical frequency ±sqrt(ln(80)/(2n)).
Outward rounding contributes less than h at each endpoint. Hence EVERY
constructed confidence box has maximum side width at most

```text
2 sqrt(ln(80)/(2n)) + 2h.
```

The standard concentration bound was checked against Hoeffding's original
Theorem 1, inequality (2.3); the standalone sheet includes a short
Bernoulli derivation and primary-source links. This bound concerns fresh
independent attempts, not independence between the two questions.
No tail table or large-quota count enumeration is needed for the argument.

If that deterministic width is strictly less than a certified distance d
to the opposite family, the simultaneous population-coverage event forces
a CORRECT singleton target. The width comparison consumes no additional
failure budget. It must use full width: a box with half-width below d
can still contain both the truth and a competing point. Equality does
not exclude a closed contact.

Using ln(80)<5 gives a purely rational sufficient check:

```text
d>2h and n(d−2h)²≥10.
```

The strict logarithmic inequality follows from the finite positive
exponential-series sum 1097/12>80. Equality in the rational check is safe;
it still implies strict geometric exclusion. Failure of this check
means “not certified by this bound,” not “identification impossible.”

One concrete fixed design is n=65,536 with the unchanged grid m=256.
Its rational certificate is 100 under uniform and 100/9 under half, both
above 10. Under either independently justified narrow premise and the
stated acquisition/model assumptions, the rule therefore has

```text
P(correct singleton) ≥ 19/20.
```

This is a conservative sufficient quota, NOT a minimum, a practical
instrument-cost estimate, a verified acquisition plan or a directive
to run 65,536 samples. Broader classes have zero uniform margin, although
a separately justified restricted truth region may admit a positive
pointwise-distance lower bound. Its competing family must not be silently
narrowed to match that planning region.

## What changes about singleton-selected reliability

BR remains valid and unchanged: with only four records, its rare singleton
answers are always wrong under the conformal fixtures despite nominal
unconditional coverage. BS does not retrofit a guarantee onto that baseline.

The NEW strict width/separation premise establishes something stronger
than ordinary target coverage: the same high-probability event guarantees
a correct singleton. If a and w are the probabilities of correct and wrong
singletons, a≥1−α and a+w≤1 imply

```text
P(wrong | singleton) = 1−a/(a+w) ≤ 1−a ≤ α.
```

Thus under the sufficient design conditions the conditional singleton
error is also at most 5%. A weaker argument using only separate coverage
and P(singleton)≥1−α would give α/(1−α); it must not obscure
why the stronger conclusion is valid here.

This does not assign a posterior probability to an observed geometric
world, justify false density bounds, or authorize repeated batches until
a singleton appears. One hidden world, a fixed quota/grid/budget and the
acquisition premises remain essential.

## Review and provenance

BS began from pushed BR commit
`710f62f0f8b8336bc5bcf0b8f2bf341a59de6128`. Read-only SHA-256 checks match
the predecessor [capture](../qr-05br-finite-record-confidence-2026-09-09/results.json)
`9bf4751ee7a044a7ec5a0d413d71bf0c83713f94cbcce07ef3503962dee24e6c`
and [freeze](../qr-05br-finite-record-confidence-2026-09-09/source-freeze.json)
`3b42328f56433c9dca32c9b83c38a6d61f19f0cb2bc41ed788eda7ba7c0e95bd`.
This authenticates retained bytes; it is not an old-study replay.

Independent analytical checks cover the segment identities, clipped and
interior contacts, whole-class margins, confidence/default/tie bounds,
strict rational budgets and strengthened conditional guarantee.
The review distinguished the correct-singleton event from merely high
total singleton frequency; the final contract retains that distinction.

The original concentration paper was consulted as literature, including
visual inspection of printed pages 14–15. No PDF, dependency, apparatus
dataset or temporary rendering is part of this publication. The PDF-reading
workflow was read-only. No new numerical source freeze or capture exists;
no mathematical engine, helper, test, oracle, prior replay or larger-quota
experiment ran. These are analytical arguments with review, not formal
Lean verification or measured physical evidence.

Publication is limited to this record, the standalone contract and the
Track-B roadmap. Three independent analytical reviews and the final
scientific-prose review found no outstanding issue after clarifying the
separate singleton-rate premise. Documentation-only QA resolves all 89
local-link occurrences across the three Markdown files and checks
heading/fence structure, math delimiters, whitespace and conflict markers.
Both BR artifacts and all eleven frozen source identities remain unchanged;
these checks are not mathematical executions or a new physical validation.
The 231 pre-existing dirty status entries, including
separate core/RET/application work and the temporary model file, remain
outside the change.

## Next gate: QR-05BT

Proceed next to **bounded separation and budget verification**, as specified
in the standalone contract. Keep the existing six fixtures/four bounds:
24 pointwise distance certificates, four whole-class margins and one fixed
n=65,536,m=256 planning pair, evaluated through rational certificate
inequalities rather than a huge count law. Retain all 28 pointwise/class
planning outcomes with premise and sufficient-condition flags, both scale
comparisons, authenticated stored BR interval widths and six fixed derived
box controls.

Use independent exact minimizer and breakpoint routes, actual forward
contacts and lower witnesses, closed/half-width controls and complete
native-report comparison. Freeze all numerical schemas and resource bounds
before that gate's first evaluation. No outcome-dependent grid/quota scan,
old engine rerun, physical collection or hidden-world observer input.
BT is not implemented or executed by BS.

Acquisition calibration, more general density and metric families, scale,
dynamics, RET adapters and applications remain separate. This closes one
design checkpoint, not QR-05, an ontology or a gravity theory. Book work
remains archival; clocks, later gravity couplings and Lean installation
stay deferred. See the
[research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
