# QR-05AC results: whole-fiber replacement envelope

7 September 2026. Exact finite, classical forecast-robustness calculation.
Completed: independent engines, runner, normal/optimized tests, exact
read-only replays and raw-history audit pass.

## Outcome

Every originally selected AA rule remains coarse-safe over the ENTIRE
declared replacement class: arbitrary probability distributions within
the existing N-fibers, shared across histories and noise levels.
This extends beyond the two particular AB tilts. It covers 96 certificates
and 194 old-rule evaluations, including every original tie.
Each certificate retains its declared finite noise set t<=u; the bound u
is not inferred from data, and noise outside that set is not certified here.

Thirty-two certificates retain a strictly negative worst-case excess,
giving a uniform case-average improvement margin over coarse fallback.
The remaining 64 have zero worst-case excess for every old rule.
Ten certificates nevertheless lose their original negative quantitative
guarantee: the same five assumed-level/bound pairs in each mixture case
that failed under AB's forward tilt. Those rules remain strictly beneficial
even under the larger class, but the guaranteed improvement can be much smaller.
The other 86 certificates preserve every old bound.
Because the enlarged class contains nominal uniform replacement, preservation
here means equality to the original bound, not a stronger guarantee.

This is an exact robustness statement for a declared mathematical family,
not evidence that a real sensor follows it. The class preserves N and the
underlying future law, fixes the original history distribution and uses one
N-conditioned replacement law across histories. It excludes history-dependent,
future-dependent and clean-label-dependent errors within N, disturbance,
missing/reclassified N, and changed history/target distributions.

## Complete old-set classification

Each row represents 16 assumed-model/upper-bound certificates.

| Experiment | Every old rule safe | Uniform strict benefit | Every old bound preserved | Unique witness mechanisms |
| --- | ---: | ---: | ---: | ---: |
| left_balanced | 16 | 0 | 16 | 1 |
| left_biased | 16 | 0 | 16 | 1 |
| right_balanced | 16 | 8 | 16 | 1 |
| right_biased | 16 | 8 | 16 | 1 |
| mixture_balanced | 16 | 8 | 11 | 2 |
| mixture_biased | 16 | 8 | 11 | 2 |

These counts are scenario inventory, not empirical success rates. Risks are
not pooled across the six experiments. All/any classifications are separate
in the evidence; they coincide here because safety holds for every old tie
and each broken original bound has a singleton old set.

The five failures in EACH mixture case are:

| Assumed level s | Noise upper bound u | Old retained weight a |
| ---: | ---: | ---: |
| 0 | 1/2 | 1/2 |
| 1/2 | 1/2 | 1 |
| 1/2 | 3/4 | 1/2 |
| 3/4 | 1/2 | 1 |
| 3/4 | 3/4 | 1 |

For mixture_balanced, s=0, u=1/2, a=1/2:

| Guarantee or stress | Exact worst-case excess over coarse |
| --- | ---: |
| Original nominal AA bound | -859/764411904 |
| AB forward tilt | -1811/2293235712 |
| AC complete replacement-class envelope | -5/63700992 |
| AC minus original bound | +799/764411904 |

The complete-class bound is still negative, but its improvement magnitude
is only 60/859 of the original guarantee. A positive bound deviation does
not mean actual harm. Every unsafe-world list for an old rule is empty;
each of these ten failures has a bound-breaking witness at its upper world.
The artifact retains all three candidates, including unselected rules,
rather than discarding adverse scores or choosing a surviving old tie.

## Why a continuum of mechanisms has an exact finite certificate

For each frozen forecast and each N-fiber label z, aggregate the full-noise
excess-loss coefficient over the ORIGINAL weighted histories:

`B_N(z) = sum_H w_H sum_q J_H,N(q) [loss(q,h_H(z))-loss(q,g_H,N)]`.

Here J_H,N is an unnormalized N/future subjoint, with mass P_H(N), not a
conditional distribution of mass one. A squared-distance calculation and
independent literal outcome-coordinate losses give the same coefficients.
Each is nonnegative. Zero-mass histories contribute zero without deleting
whole-model labels.

A fixed mechanism gives excess
`E(t,mu)=(1-t)c+t sum_N sum_z mu_N(z) B_N(z)`.
Linearity on a product of closed probability simplices gives the exact
per-world envelope
`U_t=(1-t)c+t sum_N max_z B_N(z)`.
The implementation then retains ALL maximizing finite noise worlds.

The label maximum occurs only AFTER history aggregation. A law-based hand
control uses history weights 1/4 and 3/4 and gives aggregate coefficients
3/8 and 7/8. One shared mechanism therefore has full-noise maximum 7/8.
The incorrect stronger adversary that maximizes each history separately
gives 9/8; incorrectly equalizing history weights gives 5/8.
Both mistakes are explicitly distinguished from the implemented calculation.

All 93 distinct whole-model labels in 72 fibers remain represented, including
clean-zero and unused labels. The producer's nonpositive clean excess and
nonnegative full-replacement coefficients make the upper noise endpoint a
worst world. The generic API does not assume that property: it also accepts
positive clean excess, for which zero noise can dominate.

At zero noise, or whenever zero is already a worst world, every mechanism
attains the envelope through the clean world. Otherwise each fiber's complete
maximizing-label set defines the global maximizing face. The certificate
retains the whole face and a lexicographically first pointmass witness,
not just a chosen maximizing score.

The witness is applied unchanged across all histories and actual levels.
Its OWN worst-world list is recomputed: it need not realize every envelope
maximizer when the clean world dominates. The eight distinct case-specific
mechanisms are deduplicated only for storing their full actual laws; all
288 candidate-certificate links remain explicit. All four actual noise
channels and every positive conditional future atom are retained for each.

## Closed maxima, full-support suprema and strict benefit

A pointmass witness lies on the CLOSED class boundary. It need not have
full support, even when a different full-support maximizing law exists.
The same envelope is the supremum over strictly positive replacement laws.

A full-support maximizer exists exactly when clean is a worst world or
every fiber's coefficients are constant across all of its labels.
Otherwise full-support laws approach the envelope without attaining it.
All ten weakened original guarantees have this nonattainment property,
but their supremum is already strictly negative, so they retain a uniform
negative margin. Their original-bound failures are not merely artifacts
of allowing zero support: AB already supplies positive-law failures.

No fixed candidate has a zero unattained supremum in these six experiments.
Synthetic controls explicitly exercise that different case, where every
full-support mechanism is strictly beneficial but there is no uniform
negative margin. It must not be confused with the results observed here.
Unused fibers, zero retained weight and zero noise keep every appropriate
label tie. Boundary laws are not assigned AB's full-support coincidence
equivalences when labels disappear.

## Verification and provenance

The complete protocol was recorded before any AC fixed coefficient,
maximizing law or envelope calculation. Two independent stdlib engines
carry their own nominal AA lineage and independently compute complete
profiles, faces, witnesses and old-set classifications. No new forecasting
weight is selected. The runner independently aggregates squared distances,
then checks literal risks. The JSON-only auditor aggregates literal
outcome losses from authenticated raw subjoint atoms and directly pushes
each clean source atom through each global witness channel.

Uniform coefficient averages reproduce every nominal AA risk, and both
AB tilt risk tensors are reproduced separately. The complete class encloses
all those risks and worst-case certificates. These are producer checks,
not generic API origin claims. The generic API can accept unrelated
well-formed nominal nomination tables; it does not falsely require
nominal enclosure without the uniform-family premise.

The generic exact input includes all coefficients, with 4,096-bit reduced
rational components. Newly retained sums, world values, witness values
and signed shifts are bounded separately; unretained intermediates may
exceed the bit limit and cancel. Outer native budgets reject malformed
graphs/expansion before whole serialization. All ten live resource caps
are checked before nominal or coefficient work. Output ownership and
complete witness/face/attainment corruption controls are tested.

Per case, the planned work is 10,548 terms:
216 nominal decision terms, 1,116 profile coefficient visits,
864 profile fiber reductions, 48 distinct world envelopes,
120 candidate/world visits, 4,464 face-label visits,
3,456 witness coefficient terms, 120 witness-world evaluations,
96 signed shifts and 48 candidate classifications.
Across six cases: 63,288 declared terms, not total validation cost or
application performance. There are 12 public analyze calls and
16 rejected malformed public inputs.

The first complete comparison passed in 15.862147499999992s, with four
protocol/engine/runner identities and all 33 prior artifacts unchanged.
The canonical suite is 1,777,451 bytes, SHA256
`316846022fb4898ec57f14c9b22f940071ad0a5db69959383c16b79d27ba625c`.
The complete analysis list is 863,144 bytes, SHA256
`4c2b9d95371020e601a90f5e146cb0d93ddc797e8990aefcc6f6c281ce10dbc8`.

| Final verification | Result | Elapsed seconds |
| --- | --- | ---: |
| Isolated normal tests | 300 passed | 48.79 |
| Isolated optimized tests | 300 passed | 48.90 |
| Exclusive final capture | Created; matches preflight suite | 17.055276541999774 |
| Fresh normal read-only replay | Exact suite match | 17.59990800000014 |
| Fresh optimized read-only replay | Exact suite match | 17.58563949999734 |
| JSON-only raw-history audit | 41,096,511 checks passed | 54.36003804199936 |

The final artifact is 1,783,649 bytes, SHA256
`3fc5a502c214ba408e5f539133156b0ad81a2ef243545645dc980e7936932c18`.
Its bytes, all seven frozen sources and all 33 prior artifacts remain
unchanged through both replays and the full audit. Final runs use isolated
Python and fresh external bytecode caches. Optimized pytest emits its
expected assertion warning; production guards and the dedicated normal/-O
subprocess checks use explicit exceptions, not assertions. Timings describe
these verification runs, not application performance.

The lifecycle file initially passed 35 tests in 0.15s.
The independent main test file passed 265 tests in 48.29s. It includes
213 malformed inputs (112 inherited nominal and 101 AC-specific),
542 explicit rejection checks per normal/-O guard subprocess, 60 early
graph/serialization rejections, 15 nonvacuous complete-output corruptions
and six producer baseline/risk/forecast/weight/law/mapping corruptions.
Output-corruption tests isolate the full-wire checker using an independently
verified projection; complete coefficient and witness-law reconstruction is
tested separately. Historical origin authentication remains at the pinned
fixture/raw-audit boundary, not arbitrary supplied-helper metadata.
Pre-outcome verification was strengthened to check input identity immediately
after EACH core call, preventing a later route from masking mutation.
Formatting and test-hook naming were finalized before fixed outcomes.
No fixed comparison, preflight or final verification required a numerical
or scientific-rule correction.
RESULTS.md and the roadmap are outside the seven-file frozen source ledger.
The final default Git whitespace check flags only an extra trailing blank
line in the frozen README. Its audited bytes are deliberately preserved;
the check passes with only blank-at-EOF checking excluded. Ruff passes.

The first create-only external preflight passed its full 41,096,511-check
raw audit in 53.33202416600034s. Its unchanged 1,783,651 bytes remain
outside the checkout, SHA256
`c0178981691d277d27cc773efb0f9e948b4dcbbe3d568962eb9b9339fcabbb9f`.
It was neither overwritten nor substituted for the final artifact. All
seven source identities and 33 prior artifacts were then frozen for final
tests, capture, replays and audit. The four implementation/protocol files
still matched their first fixed-comparison identities.

The auditor reconstructs the inherited 4,447 raw states, 168,388 subset
relations, 9,201,100 subset-Mobius subtractions, 8,894 K3 rows, 32,768
vertex-lifetime assignments, 482 histories and 2,064 nominal noisy cells.
It checks all 96 unsupported current/future-law equalities and reconstructs
the complete native canonical X/Y/Z/AA/AB suites before closing AC.

New AC work includes 6,288 active history/label/rule coefficient contributions
and 28,968 subjoint-outcome terms, while keeping 34,222 zero-mass
fiber/history pairs as zero contributions. It checks 864 nominal/AB risk
equations. The eight global witnesses produce 2,704 actual cells and
11,380 positive future-law atoms through 11,160 source-atom visits.
All 32,448 frozen forecasts and 2,704 coarse comparators are literally
rescored, with 11,904 affine-joint equations, 384 literal-risk equations
and all 288 certificate-to-witness links checked.

The AC-specific literal-loss counter is 1,355,070 outcome-coordinate
evaluations, separate from the inherited chain's 3,996,626 literal-loss
coordinates and 659,198 scalar disagreement summands. Coefficient maxima
use 12,456 exhaustive pairwise comparisons; envelope extrema, coefficient
witness extrema and literal witness extrema use 2,160 each. These audit
counts are not the cores' declared 63,288 work terms or all replica pairs.

Identity checks cover seven sources each for AC/AB/AA/Z/Y/X, six for W
and 33 prior artifacts: 81 targets before/after. No executor, runner or
test is imported by the auditor; source contents are identity bytes only.
The inherited polynomial digest
`8e1aa78672835867ad2177cd43b8314562186ee2271444a4a14d6f7cd1ddb5db`
is pinned producer identity, not a new polynomial derivation. Prior public
APIs, source aliases and broader operator/minimality certificates are not
replayed. Historical runtime/API counters are metadata, not reproduced
performance measurements.

## Application value and limits

The practical output is a conditional robustness envelope and a reproducible
mechanism witness. It identifies how much forecast advantage remains under
an explicitly enlarged observation-error class, and separates a lost margin
from actual loss relative to fallback. This is stronger than testing two
chosen stress directions, while keeping the premises visible.

This gate does not choose a new optimal retention weight, learn calibration
from data, integrate RET, establish per-history safety, or provide deployment
performance. No Lean proof, new quantum experiment, physical law, ontology,
metric reconstruction or gravity correspondence is supplied. No observable
is dismissed as noise or a setup artifact.

## Proposed next gate: QR-05AD, continuous robust retention

Now that the replacement class has an exact envelope, keep the same
forecast segment h_a=(1-a)g+a f_s and permit a in the closed interval [0,1].
Choose one weight for the whole experiment given an assumed model and a
declared bound, not a different weight for each history or unknown actual
world. Include the original three-weight menu's class-aware optimum as a
comparator inside this gate, preserving AA/AC old selections and failures.

Before new outcomes, independently derive from the original weighted vectors
D0=E_clean||f_s-g||^2, C0=E_clean< p0-g,f_s-g > and the full-retention
replacement envelope S1. The already checked clean forecast-segment relation
implies C0>=D0>=0 and nonpositive clean excess throughout [0,1]. Squared
weight scaling then gives the prospective producer objective

`Q_u(a)=[(1-u)D0+u S1] a^2 - 2(1-u)C0 a`.

Certify the exact interval optimizer, complete optimized forecast laws,
mechanism witnesses and nonnegative improvement over the finite menu.
This is optimality only within the fixed g/f_s segment and declared class,
not among all possible forecasts. Derive coefficients from laws, not a fit
to selected realized outcomes.

For positive quadratic coefficient the clipped stationary point is unique.
If that coefficient is zero, only a zero linear term makes the ENTIRE
interval optimal; a generic linear objective otherwise selects an endpoint.
Represent continuum ties explicitly, not by choosing a favorable single
weight. Agreement of risks on evaluated support does not imply that all
forecast maps coincide elsewhere.

The upper-noise-endpoint reduction relies on the producer premises and must
not be imposed on arbitrary generic coefficients without validating them.
Record retained-rational/resource limits, complete tie semantics and the
full protocol before computing any new weight or risk. No AD outcomes have
been calculated. Calibration, RET integration and physical interfaces remain
separate gates.
