# QR-05BR results: finite-record confidence verification

9 September 2026 (Pacific/Honolulu). **Bounded gate complete.** Two independent
implementations and a third mathematical oracle agree on the fixed four-record
confidence construction. All 26 tests pass normally and optimized; both full
replays and the single alternate-runtime reference audit match. The first
capture passed without any post-first source correction.

The main finding is a limitation as well as a verified bridge: this rule
usually returns both geometric targets. Every singleton it returns is the
flat target. Consequently its singleton answers are **always wrong under
each of the three conformal fixtures**, even though its unconditional
model-relative target coverage exceeds 95%. This is not a coverage theorem
failure, nor a reason to discard those outcomes.

## From records to a target set

The [prospective specification](README.md) and [fixed protocol](protocol.json)
retain the supplied marked-causal queries, two geometries, continuous
sampling-density parameter δ∈[0,2] and scale copies. Relative-volume targets
are 1/4 (flat) and 17/80 (conformal). Each of four fresh iid points supplies
two nested membership bits; dependence within a point is retained. Marks,
independence, no loss, the geometric family and an independently justified
density bound remain assumptions, not acquired evidence.

With total failure budget α=1/20, four one-sided allocations 1/80 and grid
j/256, inclusive binomial-tail inversion gives these closed intervals:

| Count k | Lower endpoint | Upper endpoint |
|---|---:|---:|
| 0 | 0 | 171/256 |
| 1 | 0 | 109/128 |
| 2 | 3/64 | 61/64 |
| 3 | 19/128 | 1 |
| 4 | 85/256 | 1 |

All 2,570 retained tail values agree exactly. Nondefault endpoints retain
their actual tail value and the next inward grid point's strictly larger
than budget value. The k=0 lower and k=4 upper defaults are explicit.
Separate ε=1/16 helper controls retain both exact equality endpoints at 1/2;
they do not change the main budget. The main dyadic table has no equality
with 1/80. Tests detect inward certificate substitution without claiming
that any such substitution must fail a measured coverage census.

The two count intervals form one simultaneous population box. For each
geometry, four affine mass inequalities intersect the SAME δ within the
external bound. The output preserves the entire empty/closed nuisance
interval, actual scale-dependent coefficients and coupled endpoint laws.
A product of the two coordinate ranges is not declared attainable.

The continuous-parameter coverage argument is the
[BQ theorem](../qr-05bq-finite-record-uncertainty-design-2026-09-09/README.md):
four marginal tail-failure bounds and a union bound, followed by true-world
membership in the shared-δ inverse. The finite grid/fixture verification
does not replace that proof or formally verify every physical premise.

## Complete outcomes and why singleton selection is unsafe

All 15 valid count states are retained under each of four density bounds.
The case pattern is identical for these bounds:

| Count event | Target set | Count states per bound |
|---|---|---:|
| k₂≤3 | {17/80,1/4} | 10 |
| k₂=4 and k₁<4 | {1/4} | 4 |
| k₁=k₂=4 | ∅ | 1 |

Thus the 60 cases contain **40 ambiguous, 16 target-identified and four
infeasible answers**. These are case counts, not probability-weighted
success rates. Of 240 labeled geometry hypotheses, 192 are feasible:
48 singleton δ intervals under the uniform bound, and 144 nonpoint
intervals under the other bounds. The remaining 48 are empty. Every feasible
geometry keeps its scale copy, so target identification is not scale or
full-geometry identification.

On the singleton event the flat nuisance interval is [0,0] under uniform,
[0,1/2] under half and [0,44/49] under either one or two. The conformal
maximum q₂=21/64 is below the selected lower endpoint 85/256, so these
rare records exclude every conformal density value. All00 retains every
allowed δ and both targets; all11 is a possible record whose inverse is
empty. Neither is a hardware diagnosis.

The event pattern makes its exact probabilities transparent:

```text
P(ambiguous) = 1 − q₂⁴,
P(singleton) = q₂⁴ − q₁⁴ > 0,
P(empty)     = q₁⁴ > 0.
```

Under a flat fixture every singleton target is correct; under a conformal
fixture every singleton target is wrong. For the latter,
P(target miss)=P(empty)+P(wrong singleton)=q₂⁴, while
P(wrong | singleton)=1. That conditional error does not contradict the
unconditional target-miss bound≤α. This behavior occurs in the actual
prespecified interval rule, not merely BQ's different illustrative rule.

The following percentages summarize the stored exact rational probabilities.
Each fixture has the same target-status probabilities under all four bounds;
the capture retains every separate premise label and probability.

| Fixture | Ambiguous | Singleton | Empty | Target miss | Wrong given singleton |
|---|---:|---:|---:|---:|---:|
| flat δ=0 | 98.022461% | 1.586914% | 0.390625% | 0.390625% | 0% |
| flat δ=1 | 98.840803% | 0.955288% | 0.203909% | 0.203909% | 0% |
| flat δ=16/11 | 99.046326% | 0.793674% | 0.160000% | 0.160000% | 0% |
| conformal δ=0 | 98.840803% | 0.955288% | 0.203909% | 1.159197% | 100% |
| conformal δ=1 | 99.385013% | 0.519804% | 0.095183% | 0.614987% | 100% |
| conformal δ=45/158 | 99.054664% | 0.785336% | 0.160000% | 0.945336% | 100% |

All six complete count laws normalize, give the correct binomial marginals
and retain positive covariance 4q₁(1−q₂). The deliberately wrong independent-
question law assigns the impossible10 symbol positive probability
q₁(1−q₂). Count weights are multinomial, not independent-binomial products.

There are 16 in-premise and eight out-of-premise fixture/bound summaries.
Every fixture's simultaneous population noncoverage is below 1/20; the
largest among these six is 194481/16777216, about 1.159197%. All 16 in-premise
rows obey event-level target-miss containment and target≤population≤α.
The eight excluded-density rows also happen to have target noncoverage
below α in this census. That does not validate their false premise or
extend the target theorem to false bounds. Empty outcomes remain in every
denominator. No singleton-only success score is substituted for coverage.

## Obstructions retained

Flat δ=1 and conformal δ=0 have identical normalized whole-point density,
not just equal first-query probability. They share q=(17/80,21/64) and
the entire count law, while their targets differ by 3/80. Both-target
probability is 16582735/16777216, about 98.840803%, under every supplied
bound in this census. The common-box bound≥1−α applies to the paired
worlds only for bounds one and two, which admit both true density values.
The same numerical result under the narrower bounds does not admit the
excluded flat parameter or establish a two-world theorem there.

The interior fixtures share q₁=1/5 but their second probabilities differ
by 5/7296. Their count laws are indeed different, yet this very coarse
four-record procedure offers no reliable singleton-selected separation.
A gap between two fixtures is not the separation of either fixture from
the ENTIRE competing continuous model family.

Both scale-pair comparisons preserve all nuisance sets and normalized
curve laws in all 60 cases while actual masses and volumes scale by four.
More records from the same normalized law cannot identify absolute scale
or remove the exact whole-point geometry/density compensation. Positivity
over the continuous density domain also preserves all 15 count states,
81 possible four-attempt words and 175 impossible words analytically;
no exponential word bank was enumerated.

## Interface and verification record

The new `study.infer_records` routine accepts exactly four paired records
with ordered native integer attempt IDs, native integer bits and fixed
confidence-protocol metadata. All rows are validated before counting or
arithmetic. A later malformed row cannot be hidden by an earlier10.
A well-shaped impossible10 yields a structured refusal with no counts,
bounds or answer; a valid all11 packet is accepted with an empty target
set. Neither should be presented as a confidently diagnosed instrument fault.

The public routine computes directly from fixed formulas without reading
files, fixture tables, engines or prior results. All 60 canonical valid
packets agree with the report; one fixed bit-order reassociation preserves
counts. Strict type/schema/association/private-field and detached-output
tests pass. Two prescribed private inverse probes verify safe unreachable-
pole rejection and exact closed singleton contacts. This is bounded
verification, not authentication of iid acquisition or all possible inputs.

BR began from pushed BQ commit
`0062a36c57530e48d84932bc2f58cfd9127ae92d`. The final specification and
sources were reviewed before the first numerical evaluation. Independent
static mathematical, cross-implementation, API and lifecycle reviews
found no outstanding issue; existing Ruff and normal/optimized syntax
checks passed. The create-only freeze was produced at approximately
**23:02:59 UTC on 9 September 2026**, before the first mathematical capture.
Eleven identities bind six BR source/specification/test files, BQ and BP
README/RESULTS, and the authenticated BM utility driver.

Only fresh authenticated BM codec/comparison, bounded-I/O, exclusive-write
and deadline helpers are reused with isolated globals. BR owns its
analysis, public API and publication wrappers. No historical mathematical
executor, estimator, publication wrapper or old test suite ran; no previous
numerical capture is a BR dependency.

| Check | Observed outcome |
|---|---|
| Python 3.14.0 first capture | Full primary/reference native agreement; 0.303146 s |
| Normal suite | 26 passed; 0.892 s |
| Optimized suite | 26 passed; 0.898 s |
| Normal complete replay | Exact match; 0.346809 s |
| Optimized complete replay | Exact match; 0.347689 s |
| Python 3.11.6 reference-only audit | Exactly one analysis; full native/canonical match; 0.160137 s |

Each suite caches one full analysis. Synthetic routes, temporary files and
mocks test identity/type/protocol mutations, fresh separate inputs,
immutability, owned schemas/defaults, canonical JSON, exclusive publication,
failed-evidence retention and final source/freeze/capture readbacks.
The earlier enclosing deadline is forwarded and restored; suite expiry
raises KeyboardInterrupt. Work stayed within 30 s analysis/120 s suite caps.
There was no numerical retry, post-first source change, adaptive fixture,
grid/cap increase or timing-sensitive RET overlap observed at preflight.

- [Source freeze](source-freeze.json): 1,526 bytes; SHA-256
  `3b42328f56433c9dca32c9b83c38a6d61f19f0cb2bc41ed788eda7ba7c0e95bd`.
- [Complete capture](results.json): 542,655 bytes; SHA-256
  `9bf4751ee7a044a7ec5a0d413d71bf0c83713f94cbcce07ef3503962dee24e6c`.
- Canonical mathematical report: 541,118 bytes; SHA-256
  `42398fc87802c557a55a3c63958d78dd6f661776343d77d692c0b940d9716a15`.

Publication is confined to nine BR artifacts and the owned roadmap.
Independent stored-evidence and final scientific-prose reviews found no
outstanding issue. Documentation QA resolves all 90 local-link occurrences
across the three scoped Markdown files and checks heading/fence structure,
math delimiters, whitespace and conflict markers. All eleven frozen source
identities and both retained artifacts remain unchanged. These checks do
not add mathematical runs or physical validation.
The 231 pre-existing dirty status entries, including separate core/RET/
application work and the temporary model file, remain outside this change.
No dependencies, physical devices, external data, quantum-state or chart
enumeration were added. Reproduction commands are in the specification.

## Next bounded question

Propose **QR-05BS: separation and acquisition-budget contract**, initially
analytical/design only. Separate three limits: finite-sample uncertainty,
outward-grid resolution and exact model nonidentifiability. Define relevant
separation from the entire opposite-target continuous curve under a declared
density bound, not just from one selected competing fixture. Retain the
zero-separation compensation and scale obstructions explicitly.

Derive sufficient fixed-quota/rounding conditions for useful target-set
precision on appropriately separated model regions, with a declared
failure probability. Distinguish a sufficient conservative budget from a
minimal sample requirement, unconditional coverage from singleton-selected
reliability, and pointwise separation from a uniform family-wide guarantee.
A finer grid is computation, not an added observation. Do not tune BR's
frozen baseline or silently turn fixed-quota inference into optional stopping.

BS should then prespecify any bounded executable successor, its work caps
and complete reporting obligations before new numerical evaluation.
BS is not started here. No acquisition, larger-quota sweep or precision
optimization was run. Apparatus calibration, general densities/metrics,
RET integration, dynamics and formal Lean verification remain separate.
This closes BR, not QR-05 or a gravity theory. Book work stays archival;
clocks and later gravity couplings remain deferred. See the
[research roadmap](../../track_b/QUANTUM_RECORD_GRAVITY_BRIDGE_PLAN.md).
