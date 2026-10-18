# QR-05AD: continuous robust retention

7 September 2026. Exact finite-model research, not an apparatus or gravity
validation. The prospective [protocol](README.md) precedes every AD fixed
coefficient, weight and outcome. Base: pushed AC commit
`7712aa398b0c04eabdbcfa3d97c1ddf884f6e1d0`.

## Result

Continuous retention improves the class-aware finite-menu minimum in 12 of
96 decisions; the other 84 are unchanged. There are 36 strictly negative
worst-case excess values, compared with 32 for the original three-weight
menu reoptimized under the SAME replacement class. Sixty continuous minima
are zero. Availability of weight zero makes nonpositive minima automatic;
the strict improvements and complete optimizer sets carry the useful result.

Both independent engines and the runner's independent oracle agree on the
complete outputs. The separate JSON-only auditor also reconstructs the
complete suite independently. Final publication verification is recorded
below; no physical observation has been added by this gate.

| Frozen experiment | Menu strict benefit | Continuous strict benefit | Strict menu improvements | Point / interval optima |
| --- | ---: | ---: | ---: | ---: |
| left_balanced | 0 | 0 | 0 | 0 / 16 |
| left_biased | 0 | 0 | 0 | 0 / 16 |
| right_balanced | 8 | 9 | 1 | 12 / 4 |
| right_biased | 8 | 9 | 1 | 12 / 4 |
| mixture_balanced | 8 | 9 | 5 | 12 / 4 |
| mixture_biased | 8 | 9 | 5 | 12 / 4 |
| Total | 32 | 36 | 12 | 48 / 48 |

Counts are experiment/assumed-model/bound certificates, not independent
physical trials. Risks are original-weight case averages, not pooled across
experiments and not guarantees for each individual history.

## What was certified

Keep the six experiments, 482 histories, H2/K3/Q3, original weights, target,
four assumed/actual levels and AC's closed product of replacement simplices.
One N-conditioned replacement law is shared across histories and actual
levels. Keep the frozen coarse forecast g and detailed forecast f_s.
Only the retention parameter changes: h_a = g + a(f_s-g), with one a in
[0,1] for the whole experiment at a declared assumed model s and bound u.

The root producer computes, from original weighted clean laws,

    D0 = E ||f_s-g||^2
    C0 = E <p0-g, f_s-g>
    S1 = authenticated AC full-retention replacement envelope.

The raw auditor independently expands literal outcome-coordinate losses
against unnormalized joint masses. Neither route fits coefficients to
selected weights or outcome samples. The complete clean-segment premise
gives C0 >= D0 >= 0. Full-replacement coefficients scale exactly as a^2.
A full-retention maximizing mechanism is a common witness along the entire
segment. Therefore the exact worst-case objective at the declared bound is

    Q_u(a) = A_u a^2 - 2 B_u a,
    A_u = (1-u) D0 + u S1,
    B_u = (1-u) C0.

Every original menu value is recovered exactly from the unchanged AC
candidate certificate. For A_u > 0 the unique optimum is clip(B_u/A_u,0,1).
The generic API also handles signed linear objectives when A_u=0:
positive B_u selects 1, negative B_u selects 0, and ONLY A_u=B_u=0 gives
the whole interval. A unique endpoint with zero derivative is not an
interval optimum.

Every point certificate carries the exact gradient, curvature, KKT sign and
global polynomial identity

    Q(a)-Q(a*) = A(a-a*)^2 + Q'(a*)(a-a*).

Every interval certificate retains the entire [0,1] optimizer set and a
zero-polynomial proof, with no preferred anchor. Critical candidates are
the endpoints and any isolated interior stationary point; they are a
sufficient finite minimization set, not the stationary continuum of a
flat polynomial. All finite-menu ties are retained as well.

## Weights, gains and limitations

Of 48 point optima, 16 are interior, 12 are weight zero and 20 are weight
one. Four interior weights already equal the menu's half-retention choice;
the remaining 12 account for the strict menu improvements. The 48 interval
optima are represented parametrically, not replaced by an arbitrary point.

In the right_balanced case, clean assumed model s=0 and bound u=3/4 give

    a* = 1/4,
    continuous worst excess = -49/95551488,
    finite-menu worst excess = 0 (weights 0 and 1/2 tied).

Thus a useful intermediate weight survives where the available menu cannot
guarantee strict benefit. This is a worst-case-value improvement, not
pointwise dominance over every menu choice in every actual world.

The mixture_balanced case at s=0 and u=1/2 gives

    D0 = C0 = 103/15925248, S1 = 299/15925248,
    a* = 103/402,
    continuous worst excess = -10609/12803899392,
    finite-menu worst excess = -5/63700992,
    menu discretization gap = 2401/3200974848.

The guaranteed improvement magnitude is 10609/1005 times the menu's, but
the absolute Brier-excess gain is only about 7.50e-7. It is still only
42436/57553 of the original AA guarantee magnitude 859/764411904 in this
example. Do not confuse improvement over the enlarged-class menu with
restoration of the old nominal guarantee or empirical significance.

All original AC certificates are preserved byte-for-byte as mathematical
wires, including all candidates, AA ties and ten failed original negative
bounds. Thirty-four unselected candidate certificates still have positive
worst-case excess: seven in each right-hand case and ten in each mixture.
These harmful rules are not relabeled or removed. This gate
does not make their old guarantees true by changing the selected policy.

For arbitrary admitted generic quadratics, the best three-weight menu's
gap is at most A/16 <= 1/8; quarter and three-quarter hand cases attain
the sharp bound. These are prespecified generic bounds, not the observed
scale of this model's gains. The generic Q range is [-4,6], while actual
producer Brier-excess values remain in [-2,2].

## Complete forecast and witness evidence

The suite retains 52 unique forecast families and eight case-specific
global replacement mechanisms. Families are deduplicated by assumed model
and complete optimizer set, in first-occurrence certificate order; no
claim of minimum representation across assumed models is made. Every
family keeps original history weights, all nominal full-support reports,
and complete coarse/detailed endpoint laws. Point families additionally
carry their exact mixed law. Interval families deliberately have null
point forecasts: their two endpoints define the entire parametric family.
There are 4,632 retained family/report cells, including 1,016 deliberately
parametric interval cells. The witness laws retain 2,704 actual cells and
11,380 positive future-law atoms, with unchanged original history weights.

All 96 decisions retain complete positive-weight maximizing faces, separate
all-label faces at zero weight or zero bound, and a common full-retention
extreme witness. A canonical common witness need not be AC's lex-first
whole-simplex witness at a clean bound. Both remain valid; neither is a
history-dependent error rule.

The independent auditor authenticates all 96 assumed-model/actual-world
polynomials (192 coefficients) from literal losses under the common witnesses. It
literally rescores all 40 unique point families at all four actual levels.
For the 48 interval decisions, 120 included lower/upper world-polynomial
checks establish that each lower world is nonpositive throughout [0,1]
and the upper polynomial is identically zero. A flat upper objective does
not by itself imply that every lower-world polynomial is zero.

The generic optimizer receives only 16 supplied (A,B) pairs, fixed labels
and schema fields. It does not authenticate laws, derive the quadratic
reduction, consume raw histories, establish physical realizability or
perform calibration. Those producer/auditor obligations remain separate.

## Verification and provenance

| Final verification | Result | Elapsed seconds |
| --- | --- | ---: |
| Isolated normal tests | 198 passed | 58.00 |
| Isolated optimized tests | 198 passed | 58.24 |
| Exclusive final capture | Created; matches first/preflight suite | 26.641243666002993 |
| Fresh normal read-only replay | Exact suite match | 37.76714458399874 |
| Fresh optimized read-only replay | Exact suite match | 37.93377533400053 |
| JSON-only raw-history audit | 43,849,782 checks passed | 77.4624156250029 |

The final artifact is 5,003,206 bytes, SHA256
`099c9df18db91545fdd3a08a383e2e4ed96bf5734f6b80a9e492c3bc954c611a`.
All seven frozen sources, all 34 prior artifacts and final evidence bytes
remain unchanged through both replays and the full audit. The audit checks
89 distinct source/prior identity targets before/after, plus the capture
itself. Verification uses isolated Python and fresh external cache
directories; paired final tests and final read-only runs were scheduled
concurrently. These are verification timings, not application-performance
claims. Optimized pytest emits its expected assertion warning; production
guards and dedicated normal/-O subprocess checks use explicit exceptions.
Ruff and the default scoped Git whitespace check pass.

The first fixed comparison passed in 23.891770875001384s with the four
protocol/implementation source identities and all 34 prior artifacts
unchanged before/after. The complete suite is 4,996,857 bytes, SHA256
`158591e7b353dd8e03e8512504088f42662f4f87f92b15a51fc9bbc8dad64ade`.
An independent fixed auditor-helper comparison subsequently passed 804,591
checks in 7.026867s and matched the entire suite; its 110,189-byte analysis
list has SHA256
`00e1247743e3b02ebdaaada01848224e384284e8a70a808abf8b0f46f38712ff`.
These helper checks are not substitutes for the final full raw audit.

The exclusive external preflight is 5,003,208 bytes, SHA256
`336a9fc10db27bba2ae76ab62901bf325e527a182cab6245843057706b8015dc`,
retained outside the checkout at
`/tmp/det8-qr05ad-preflight-NA097MYg/preflight.json`. Its full JSON-only
raw-history audit passed 43,849,782 checks in 58.54269458300041s, with
all 89 source/prior identity targets and capture bytes unchanged. The
preflight is not overwritten or substituted for the final artifact.

The initial main test suite passed 163 tests in 56.49s, and the separate
lifecycle suite passed 35 tests in 0.15s. The main suite includes 114
malformed inputs and 311 explicit rejection checks per normal/optimized
guard subprocess, including 39 pre-serialization graph rejections. Fifteen
optimizer-output corruptions, 13 complete evidence/law/map corruptions
and six producer corruptions are explicitly nonvacuous. Direct current-
gate mutation helpers bypass only separately verified AC parent checking;
they do not claim to authenticate arbitrary supplied historical metadata.
The synthetic flat-upper/nonzero-lower-world case is an algebraic-builder
test, not a claim that this is a realizable frozen producer.

The raw chain reconstructs 4,447 states, 168,388 subset relations,
9,201,100 subset-Mobius subtractions, 8,894 K3 rows, 32,768 lifetime
assignments, 482 histories and 2,064 nominal noisy cells. New AD work
includes 8,120 clean source-atom polynomial expansions, 33,152 witness
source-atom polynomial expansions, 258,752 literal polynomial coordinates
and 763,936 literal point-loss coordinates. It checks 1,968 clean forecast
segments, all 288 AC menu values, 11,904 affine witness-joint equations,
all 192 world coefficients and the complete native canonical suite.

No first fixed comparison, preflight, final test, replay or raw audit
required a numerical or scientific-rule correction. The four original
protocol/implementation identities remain exactly those recorded at the
first fixed comparison. Test authoring and formatting were completed
before external preflight; all seven sources were then frozen for final
verification. Read-only independent reviews found no actionable
optimizer, producer, auditor, provenance or scientific-claim discrepancy.

Seven source files are frozen for publication: README.md, retention.py,
reference_qr05ad.py, study.py, test_qr05ad.py, test_capture.py and audit_json.py.
RESULTS.md and the roadmap are outside that source ledger. Prior source
identities and all 34 artifacts remain in the audit chain; inherited
polynomial identities are not described as fresh derivations, and prior
runtime/API or broader operator/minimality certificates are not replayed.

## Next proposed gate: QR-05AE, history-level safety diagnostic

Keep AD's globally selected policy and complete interval families frozen.
Inspect signed history-level excess under its retained common mechanisms
at each included actual level. For point policies, separate harmed-history
likelihood mass and positive harm contribution from offsetting negative
benefit, and verify that the original-weight sum recovers the case value.
Carry interval families parametrically with explicit quantifiers, never
selecting a convenient representative.

This proposed diagnostic is limited to the retained common witnesses; it
would not prove conditional safety under every replacement mechanism.
If a later gate computes individual-history mechanism envelopes, each
history's maximizing mechanism is a separate globally admissible witness,
not one simultaneous history-dependent adversary. Never sum such maxima
and relabel them the existing case minimax. No AE outcomes are calculated
here; its exact protocol and resource limits must precede execution.

The gate remains an exact finite forecasting construction. No RET
deployment, measured-noise calibration, Lean proof, new quantum law,
ontological conclusion, metric or gravitational dynamics follows from it.
