# QR-05AB results: frozen rules under replacement-mechanism stress

7 September 2026. Exact finite, classical forecast-stress comparison.
Completed: independent engines, runner, normal/optimized tests, exact
read-only replays and raw-history audit pass.

## Outcome

Every originally selected AA rule remains coarse-safe under both prespecified
replacement tilts in the six fixed experiments. This covers 192 certificates
and 388 old-rule evaluations, including all original ties. In 64 certificates
every old rule remains strictly beneficial; the remaining 128 have zero
worst-case excess for the old rules.

Safety does not imply preservation of the original quantitative guarantee.
Ten certificates lose their original negative upper bound: five in each
mixture case, under the forward tilt only. Each has a unique old minimizing
rule, and each remains strictly better than coarse in case-average risk
throughout its declared finite noise set. There is no alternative old tie
that rescues the broken bound. No harmful old rule was observed in these
two mechanisms; this is not a guarantee for arbitrary replacement laws.

The left and right cases preserve all old bounds under both tilts. Each
mixture case preserves 11 of 16 under forward and all 16 under reverse.
Across the 192 certificates, 182 preserve every old bound and ten do not.
These are an inventory of exact mathematical cases, not empirical success
rates. Risks are never pooled across experiments.

## What changed, and what stayed fixed

The actual replacement distribution changes from uniform to two opposite
canonical-label rank tilts. Within each whole-model N fiber, with m distinct
labels and zero-based rank r:

- forward probability is 2(r+1)/(m(m+1));
- reverse probability is 2(m-r)/(m(m+1)).

Both laws have full support. Their pointwise average is uniform. All
93 distinct labels in 72 whole-model fibers are included, even when a label
has zero clean prior. Multiplicities and history-specific support do not
choose the ranks. Label order is a mathematical stress convention, not a
calibrated sensor model.

Forecasts, original history weights, target, noise levels {0,1/2,3/4,1},
retained weights {0,1/2,1}, and every nominal AA minimizing set stay fixed.
Each mechanism applies globally across histories; no stressed optimization,
forecast refit, retrospective tie selection or per-history adversary occurs.
All three candidates and every worst-world witness remain in the artifact,
including unselected rules.

The actual joint law is rebuilt before conditional normalization:

`J_t,mu(z,q) = (1-t) J_0(z,q) + t mu(z|N(z)) J_N(z)(q)`,

where `J_N(q) = sum_{b with prefix N} J_0(b,q)` is an UNNORMALIZED
N/future subjoint. Dividing it by P(N) here would incorrectly change the
original N-fiber probability mass. Tests explicitly cover unequal fiber
masses and a clean-zero but replacement-positive label.

## Broken quantitative bounds

The same five (assumed level s, upper bound u, retained weight a) combinations
occur in both mixture experiments. These are old choices, not newly selected
stressed optima.

| s | u | Old a | Forward outcome |
| ---: | ---: | ---: | --- |
| 0 | 1/2 | 1/2 | Still strictly beneficial; original bound broken |
| 1/2 | 1/2 | 1 | Still strictly beneficial; original bound broken |
| 1/2 | 3/4 | 1/2 | Still strictly beneficial; original bound broken |
| 3/4 | 1/2 | 1 | Still strictly beneficial; original bound broken |
| 3/4 | 3/4 | 1 | Still strictly beneficial; original bound broken |

For example, in mixture_balanced at s=0, u=1/2, a=1/2:

| Quantity | Exact worst-case excess over coarse |
| --- | ---: |
| Original AA bound | -859/764411904 |
| Forward tilt | -1811/2293235712 |
| Forward minus original bound | +383/1146617856 |

A positive bound deviation is adverse even though the stressed excess
itself is negative. The stored unsafe-world list is empty, while the
bound-breaking-world list contains actual level 1/2. Equivalent complete
witnesses are retained for all ten failures.

Opposite tilts have the nominal JOINT law as their midpoint. Frozen-policy
risk is linear in that law, so opposite risks average to nominal risk.
This is not an unweighted average of conditional posteriors.

Here clean excess is nonpositive, full replacement leaves the true
N-conditioned future law, and full-replacement excess is a nonnegative
tilt-weighted squared forecast distance times a squared. Actual-risk
affinity therefore makes the upper noise endpoint a worst world for every
candidate. In this particular family, opposite worst risks also average
to their nominal value. Thus each adverse old-bound deviation has an equal
favorable reverse deviation. This is a checked structural control, not
independent empirical evidence. In general, a maximum need not commute
with averaging; the endpoint property is essential.

All/any flags are reported separately. They happen to agree in these fixed
outcomes because all old rules survive safety, and each broken old bound
has a singleton old set. Synthetic tests exercise unequal all/any outcomes,
including different surviving tied rules under different mechanisms.

## Verification and provenance

The complete protocol preceded the first AB fixed-case outcome. Two
standalone engines carry separately implemented nominal AA lineages and
stress classifiers. The independent runner constructs complete tilted laws,
scores them quadratically and checks them by literal outcome-coordinate loss.
The JSON-only auditor independently pushes each clean source atom through
the stochastic channel and replays the inherited raw-history chain.
No executor, runner or test is imported by the auditor.

The standalone API accepts exact risk tables, not observation laws or
histories. It does not authenticate their origin or impose the producer's
affinity, midpoint or endpoint assumptions on arbitrary input tables.
Its generic tests include nonaffine risks, interior maxima and both signed
shift endpoints +/-4. Input/retained fractions are bounded at 4,096 bits;
unretained arithmetic may exceed that bound and cancel exactly.

All native schemas and planned work limits precede nominal or stress
arithmetic. Expanded-node/depth/ASCII-byte guards handle benign shared
subtrees without accepting cycles or explosive expansion. Outputs are
detached. The wrapper has its own native admission boundary; this does not
claim replaying every historical AA public byte/node admission limit.

Declared work is 840 terms per case: 216 nominal decision terms, 96 stress
excess terms, 240 candidate/world visits, 192 signed shifts and 96 candidate
classifications. Across six cases this is 5,040 terms, not an elapsed-time
or total validation-cost claim. There are 576 candidate certificates,
12 public analyze calls and 16 rejected malformed public calls.

The first complete comparison passed in 17.67093654099881s. All four
protocol/engine/runner identities and 32 prior artifacts stayed unchanged.
Its canonical suite is 1,799,505 bytes, SHA256
`ca56aada0a0acc5fac508a7b638a10ccec41121bce296925ebd29f8e38c46ba2`;
the complete analysis list is 468,518 bytes, SHA256
`490b73fdaa854597ee20e7a12fa11fba983b2417311d23b2e94c178e06bf9d77`.

| Final verification | Result | Elapsed seconds |
| --- | --- | ---: |
| Isolated normal tests | 272 passed | 47.47 |
| Isolated optimized tests | 272 passed | 47.67 |
| Exclusive final capture | Created; matches preflight suite | 18.080229458999383 |
| Fresh normal read-only replay | Exact suite match | 19.410666625000886 |
| Fresh optimized read-only replay | Exact suite match | 19.37849279099828 |
| JSON-only raw-history audit | 38,952,932 checks passed | 46.543764541998826 |

The final artifact is 1,805,554 bytes, SHA256
`7cbe2668d5b022f73207502bab214078b911e25d25a3826918b916e967643009`.
Its bytes, all seven frozen sources and all 32 prior artifacts remain
unchanged through both replays and the full audit. Final runs use isolated
Python and fresh external bytecode caches. The optimized pytest run emits
its expected assertion warning; production guards and the dedicated
normal/-O subprocess checks use explicit exceptions, not assertions.
No fixed-case comparison, preflight or final verification required a
numerical or scientific-rule correction. No pre-outcome mathematical
correction was needed; formatting and test-hook naming were finalized before
the first fixed comparison. RESULTS.md and the roadmap are outside the
frozen source ledger. Timings describe these checks, not application performance.

The independent test file first passed 237 tests in 46.30s; the lifecycle
file passed 35 in 0.13s. Tests include 193 malformed fixtures (112 inherited
nominal and 81 wrapper/stress), 486 explicit rejections in each normal/-O
guard subprocess, 60 pre-serialization graph rejections, 15 nonvacuous
complete-output corruptions and six source/law/weight corruptions. Full
projection checks are separate from cached-input output-corruption checks.
Historical artifact and rank-law origin authentication stay at the pinned
fixture/raw-audit boundary, not arbitrary supplied-helper metadata.

The first create-only external preflight passed 38,952,932 raw-audit checks
in 48.14518833300099s. Its unchanged 1,805,555 bytes remain outside the
checkout, SHA256
`211f88cfea7f9ebd60e116db3b12a6331cc902a5cd5dcb961fb327a719679cf8`.
It was not overwritten or substituted for the final artifact. The seven
sources and all 32 prior artifacts were unchanged, then pinned for final
tests/capture/replays/audit. No fixed-case or preflight correction was needed.

The raw chain reconstructs 4,447 states, 168,388 induced-subset relations,
9,201,100 subset-Mobius subtractions, 8,894 K3 rows, 32,768 vertex-lifetime
assignments, 482 histories and 2,064 nominal noisy cells. It checks all 96
unsupported current-posterior/future-law equality controls and the complete
native canonical X/Y/Z/AA suites before closing the complete AB suite.

New AB work includes 21,168 source-atom/target channel visits, 4,128 actual
cells with 18,544 positive future-law atoms, and 49,536 frozen-forecast plus
4,128 coarse-comparator rescorings. It adds 1,681,488 literal loss coordinates
and 241,072 scalar disagreement summands: the complete chain totals
3,996,626 and 659,198 respectively, not all possible replica pairs.
There are 9,656 affine-joint, 9,272 opposite-joint, 576 affine-risk,
288 opposite-risk and 194 opposite-old-bound checks. AB extrema use 4,320
exhaustive maximum comparisons and no stressed argmin. These audit counts
differ from the cores' declared 5,040 work terms.

Identity checks cover seven sources each for AB/AA/Z/Y/X, six for W and
32 prior artifacts: 73 targets before and after. Source contents are identity
bytes only. The inherited polynomial digest
`8e1aa78672835867ad2177cd43b8314562186ee2271444a4a14d6f7cd1ddb5db`
is pinned producer identity, not a fresh polynomial derivation. Historical
API/runtime fields are metadata, not replayed APIs or reproduced performance.
No broader operator/minimality certificate or prior source alias is replayed.

## Application value and boundaries

This adds an explicit assumption-stress certificate to the decision layer.
A consumer can distinguish a rule that has become harmful from one that
still helps but no longer earns its advertised improvement guarantee.
The latter occurs here. Failure under a changed mechanism does not refute
AA's original conditional result; it identifies a premise that matters.

Two label-order tilts are neither a complete uncertainty class nor evidence
about the frequency of real sensor errors. These are original-weight
case-average risks, not guarantees for every history or individual report.
Generic harmful controls verify rejection/classification logic; they are
not hidden claims that the fixed producer had harmful old choices.

No calibration data, deployed sensor, RET integration, Lean proof, quantum
experiment, new physical law, ontology, metric reconstruction or gravity
correspondence is supplied. No observation is dismissed as noise or a setup
artifact.

## Proposed next gate: QR-05AC, whole-fiber replacement envelope

Keep the same forecasts, target, histories, finite noise bounds and complete
AA old-rule sets. Before any new outcome, specify a closed probability
simplex of replacement laws on each existing whole-model N alphabet.
A single law for each N must be shared across histories and noise levels.

For each frozen candidate, aggregate the original-weight loss coefficients
across histories BEFORE maximizing over replacement labels within N.
Then calculate the exact worst-case envelope over the declared replacement
class, retaining all maximizing labels and a complete globally consistent
mechanism witness. Do not substitute a stronger adversary that chooses
separately for each history, or reoptimize forecasts/weights after outcomes.

A boundary point-mass maximizer belongs to the closed simplex, not the
strictly positive interior. State explicitly when it supplies an attained
maximum versus the supremum approached by full-support laws. Candidate-wise
worst mechanisms may differ; their separate certificates must not be
misrepresented as one common jointly worst mechanism.
Boundary laws can omit labels, so AB's full-support law-coincidence
equivalences must not be carried over unchanged.

At zero noise bound every mechanism maximizes the unchanged clean objective;
do not incorrectly restrict its witness set to full-noise maximizing labels.
Unused fibers also keep every label. A zero worst-case supremum is not a
uniform strict benefit margin, even if every interior law happens to have
negative excess. Within each assumed model, the frozen mixture's squared
weight scaling suggests a common maximizing mechanism across weights; verify
that control without presuming a common maximizer across assumed models.

This would test whether AB's coarse-safety survival extends beyond two
chosen tilts, while preserving original-bound failures. No AC outcomes have
been calculated; its complete protocol and API still need to be recorded.
