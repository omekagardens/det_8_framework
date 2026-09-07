# QR-05AA results: finite uncertainty-bound decisions

7 September 2026. Exact finite, classical forecast-decision comparison.
Completed: independent engines, runner, normal/optimized tests, exact
read-only replays and raw-history audit pass.

## Outcome

Both implementations and the independent runner agree on the complete
decision certificates for six separate experiments, four assumed models,
four declared upper bounds and three fixed retained weights.

There are 96 decisions. In 32, the minimum worst-case excess risk is strictly
negative: a certified rule improves case-average risk over coarse-only in
every actual world inside that declared finite uncertainty set. This does
not guarantee improvement in every history or report. The remaining 64 have value
zero. Coarse-only is always available, so a nonpositive optimum is guaranteed
by menu construction; it is not evidence that detailed forecasting is
universally robust.

Each candidate rule applies across every history and report in an experiment;
the certificate retains every minimizing rule. Bounds are supplied assumptions. Neither the unknown actual noise nor a
future outcome chooses the rule, and no six-case risk average is formed.

## Complete minimizing-weight pattern

Each cell below lists ALL minimizing retained weights. Columns are declared
upper bounds u; rows are the assumed replacement level s. A retained weight
of 0 is coarse-only, 1 is the completed Y forecast, and 1/2 is Z's half blend.
Full retention keeps the already assumed-noise-conditioned forecast; it
does not mean assuming a clean sensor or inferring its calibration.

For both right cases:

| Assumed s \\ Bound u | 0 | 1/2 | 3/4 | 1 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1/2 | {0,1/2} | 0 |
| 1/2 | 1 | 1 | 1/2 | 0 |
| 3/4 | 1 | 1 | 1 | 0 |
| 1 | {0,1/2,1} | {0,1/2,1} | {0,1/2,1} | {0,1/2,1} |

Both mixture cases have the same pattern EXCEPT s=0,u=3/4: only 0 minimizes.
The half blend is still harmful relative to coarse there, as Z already showed.
Both left cases have all three weights tied in every decision.

Across the 96 decisions, 24 uniquely select full retention, 8 uniquely select
the half blend and 14 uniquely select coarse-only. There are 2 two-way ties
and 48 three-way ties. These are scenario inventory counts, not probabilities,
empirical success rates or a policy recommendation.

## Selected exact certificates

Worst-case excess means forecast risk minus coarse risk under the same actual
world, maximized over all supplied worlds t<=u. Negative is beneficial.

| Case; s,u | Coarse worst excess | Half-blend worst excess | Full-retention worst excess |
| --- | ---: | ---: | ---: |
| right_balanced; 0,1/2 | 0 | -49/23887872 | 0 |
| mixture_balanced; 0,1/2 | 0 | -859/764411904 | 377/191102976 |
| right_balanced; 0,3/4 | 0 | 0 | 49/11943936 |
| mixture_balanced; 0,3/4 | 0 | 377/509607936 | 263/42467328 |

These are small absolute differences in hypothetical exact experiments,
not measured application gains or percentages of total prediction error.

The right-case tie at s=0,u=3/4 does not mean coarse and half-blend laws
coincide. The half blend has strictly lower risk at some lower actual levels
but matches coarse risk at the upper endpoint. Both minimize worst-case
excess, so both are retained. No retrospective tie-breaking rule is invented.

When u=1 and s<1, the four informative cases uniquely select coarse-only.
At s=1, or in either left case, the three complete rules coincide and tie.
These were prospective consequences of full replacement and the fixed
forecast family, not newly discovered empirical robustness.

## Mathematical certificate and authenticated premises

For original-weight experiment risks R(t,s,a) and coarse risk G(t),

    E(t,s,a) = R(t,s,a)-G(t),
    M(s,u,a) = max_{t in S_u} E(t,s,a),
    V(s,u) = min_{a in {0,1/2,1}} M(s,u,a).

The core retains all 48 candidate/world risks per case, all signed differences,
all 16 decisions, all 48 candidate maxima, every maximizing world and every
minimizing weight. Comparison with coarse happens BEFORE maximization.
Risk is averaged using original history/report probabilities BEFORE taking
the maximum over actual worlds. There is no per-history adversary or
actual-world-dependent choice.

The W actual joint report/future law is affine in replacement. Its expected
risk for a fixed rule is therefore affine, even though conditional future
laws need not be. The runner checks complete joint laws, original likelihood
weights, true N-conditioned coarse forecasts, actual-index-independent mixed
laws and literal outcome-coordinate Brier scores.

It also checks the clean-positive forecast segment, clean nonpositive excess,
constant coarse risk and full-replacement quadratic penalty. In this W
family, excess is nondecreasing in actual replacement, so the upper endpoint
is among the maximizing worlds. All maximizing ties remain visible; endpoint
membership is not a uniqueness assertion.

For arbitrary supplied tables the generic API does NOT assume affinity,
monotonicity, constant coarse risk or realizability by the Z forecast family.
It verifies a finite decision problem, not origin or calibration. Generic
tests retain negative maxima, interior worst worlds, varying coarse risks,
and complete ties; they catch clipping benefits to zero, reversing min/max
and subtracting independently maximized coarse risk.

## Evidence and bounded work

| Object | Per case | Six-case inventory |
| --- | ---: | ---: |
| Actual worlds / assumed models / fixed rules | 4 / 4 / 3 | Cases remain separate |
| Complete risk-minus-coarse entries | 48 | 288 |
| Bound/model decisions | 16 | 96 |
| Candidate-world visits over nested sets | 120 | 720 |
| Candidate-selection visits | 48 | 288 |
| Total declared decision-work terms | 216 | 1,296 |

These counters describe risk subtraction and decision visits, not every
comparison, input validation, copying operation or CPU instruction. Both
live work caps are planned before any subtraction or decision scan. Strict
native JSON, exact reduced fractions, retained-bit caps, pre-serialization
DAG/depth/byte checks and detached outputs remain part of the contract.

Z's complete laws and nested Y/X evidence remain immutable in the pinned
31,075,315-byte Z artifact; the smaller AA artifact references that evidence
and retains the complete risk-table decision interface. It does not silently
replace full-law evidence with an unauthenticated scalar table.

## Verification and immutable evidence

Seven source/protocol files were frozen after the successful external
preflight. All final verification runs passed on their first attempt.

| Final check | Result | Time |
| --- | --- | ---: |
| Normal Python tests | 190 passed | 29.95s |
| Optimized Python tests | 190 passed; expected assertion warning | 29.88s |
| Exclusive final capture | Created once | 7.224s |
| Normal exact read-only replay | Passed | 7.608s |
| Optimized exact read-only replay | Passed | 7.524s |
| Independent raw-history JSON-only audit | 36,786,183 checks passed | 40.199s |
| Ruff lint / format checks | Passed / unchanged | — |

Times are rounded local measurements, not reproducible performance claims.
Optimized pytest emits its expected warning about ordinary Python assertions;
the dedicated guard subprocesses use explicit exceptions/checks.

| Canonical object | Bytes | SHA256 |
| --- | ---: | --- |
| Final results.json | 112,206 | `bf5661984f9df4cb111fbe97061035967de9f7516a26154abefc7d1d3a49c424` |
| Numerical suite | 106,305 | `af0171687da938c4e16d42d3a05453c9965099ede68af5462310d4fdc20c4be2` |
| Complete analysis list | 87,445 | `03f50bdd9e10009a8179f813af0dab61b157948168bb7d85a320a151b43a6241` |

The exact suite and complete analysis list match the first comparison and
external preflight. Canonical identity uses compact sorted ASCII JSON with
one trailing newline. The outer envelope additionally includes runtime
metadata, which is not part of the exact numerical suite.

The 190 tests include 112 malformed native/schema fixtures, 12 nonvacuous
complete AA-output corruptions, six producer risk/law/weight corruptions,
and 35 isolated capture-lifecycle controls. Each normal/optimized guard
subprocess performs 297 explicit rejections, including 45 before whole-tree
serialization (15 graph placements across both cores and the runner).
Those subprocess checks do not rely on Python assertions.

The core checks cover signed benefits, interior worst worlds, all exact ties,
same-world subtraction before maximization, global rather than actual-world
selection, nested values without assuming nested minimizer sets, all six
live caps, honest work counts, detached ownership, exact ASCII sizes and
scalar/empty/cached-subtree depth boundaries. A valid-input example produces
a genuinely 4097-bit retained difference and is rejected; separate controls
accept large intermediates that cancel into allowed retained values.

The direct producer-helper corruption tests concern projected risks, original
weights and complete laws. Whole Z identity is checked separately by pinned
fixtures and the raw auditor; an internal helper is not presented as a generic
authenticator of arbitrary supplied historical metadata.

The JSON-only auditor reconstructs 4,447 raw states, 168,388 induced-subset
relations, 9,201,100 subset-Mobius subtractions, 8,894 K3 raw-member rows and
32,768 vertex-lifetime assignments. It authenticates 482 histories, 2,064
noisy cells and all 96 unsupported posterior/future-law equality controls.
It rebuilds the entire X/Y/Z report chain before projecting and deciding AA.

Across that chain and AA rescoring it checks 2,315,138 literal
actual-outcome/forecast-coordinate loss terms and 418,126 scalar disagreement
summands, not every possible replica pair. The AA projection rescores 24,768
forecasts and adds 776,042 literal loss coordinates. New producer controls
include 4,828 affine-joint coordinates, 300 affine-risk equations and 1,968
clean-positive forecast-segment laws. Complete full-replacement law
coincidence, not merely a scalar tie, is checked.

AA's independent extrema audit uses exhaustive pairwise dominance: 2,160
maximum comparisons and 864 minimum comparisons. These audit counts differ
from the cores' explicitly declared 1,296 decision-work visits. Full native
and canonical X/Y/Z/AA suites, all candidate/world risks, ties, counts and
producer-control fields agree.

No executor, runner or test is imported by the auditor. Source content is
used only as identity bytes. The inherited polynomial digest
`8e1aa78672835867ad2177cd43b8314562186ee2271444a4a14d6f7cd1ddb5db`
is pinned producer identity, not a fresh polynomial derivation. Prior public
APIs, source aliases and broader operator/minimality certificates are not
replayed. Historical API/runtime fields are validated metadata, not
reproduced performance measurements.

Before any AA fixed outcome, code review strengthened early string-size
rejection in the primary and early traversal-depth/cached-depth/width
rejection in the reference. One manual reference shared-subtree harness
initially counted an extra wrapper incorrectly; the fixture was corrected
to its actual depth. Test review also separated input-native cap acceptance
from the larger output cap, and scoped internal producer corruptions to
their promised risk/law/weight checks. No mathematical rule, bound, weight,
schema, acceptance criterion or retained outcome was changed.

The first complete comparison passed in 7.313218999999663s with four
protocol/implementation files and all 31 prior artifacts unchanged.
The first independent test file run passed 155 tests in 29.63s; the
capture-lifecycle file passed 35 tests in 0.13s.

The create-only external preflight passed its full 36,786,183-check audit
in 39.61294604199975s before final freeze. Its 112,208 bytes remain unchanged
outside the checkout, SHA256
`3f4c60a8cefb4560e1372285d2bc259235847736f610cdd30203892efaf50732`.
It was not overwritten or substituted for the final artifact. No fixed-case
comparison, preflight audit or final verification required a numerical fix.

Seven AA source/protocol files and 31 prior artifacts remain unchanged
through final tests, capture, replays and audit. The auditor additionally
authenticates seven sources each for Z/Y/X and six for W: 65 source/prior
identity targets in total. Final artifact bytes remain unchanged after
exclusive creation. Final runs use isolated Python and fresh external
bytecode caches. RESULTS.md and the roadmap are outside the frozen ledger.

## Application value and boundaries

This is a small, auditable decision layer: given a declared uncertainty set
and an authenticated table of expected risks, it identifies every best
fixed choice in the menu and shows the conditional cost of conservatism.
Its useful output is a certificate with premises, not a universal safe
policy. Nothing guarantees performance if the actual world falls outside
the supplied set or the observation model is wrong.

No calibration dataset, deployed sensor, RET integration, Lean proof,
new physical law, ontology, metric reconstruction or gravity correspondence
is supplied. No observation is dismissed as noise or a setup artifact.

## Proposed next gate: QR-05AB, replacement-mechanism stress

Before enlarging the weight menu, test an unresolved assumption: the uniform
replacement law. Keep Z's forecasts, coarse laws, original histories, target
and AA's complete minimizing-weight sets fixed. Prespecify two full-support
asymmetric replacement laws within each whole-model N alphabet, including
currently zero-prior labels, using a canonical-order tilt and its reverse
as mathematical stress controls defined independently of outcomes.

Recompute the actual report/future laws and evaluate every originally
certified rule, including every old tie, under the same finite declared
bounds. Report the two tilted mechanisms separately and distinguish whether
every old minimizing rule remains safe from whether merely some do.
Retain all three rule scores and harmful outcomes. Do not
reoptimize, select a surviving tie after seeing results, or assign a different
replacement mechanism separately to each history or report.

These label-order tilts would not be sensor models or a complete uncertainty
class. The question is whether the existing conditional certificates survive
specified mechanism changes, not whether DET or a physical law is validated.
Record the complete AB protocol and channel formulas before any new outcome
calculation. No AB outcomes have been computed.
