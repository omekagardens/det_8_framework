# RI-60 — per-coordinate finite-context error bounds

24 September 2026 UTC. **All 196 qualification gates and all eight actual reference-input rows
independently accepted in both modes. No physical envelope is inferred.**
This is a separate attempt under the unchanged [RI-55 design](../gwosc_context_sensitivity_v1/DESIGN.md).
The [failed RI-57 attempt](../gwosc_context_operator_v1/IMPLEMENTATION.md),
its source and exact failed receipt remain fixed and reproducible.

## Why the method changes

RI-57 passed 187 of 196 qualification gates in both modes. Every selected gain
interval failed its width limit; the dependent structural report could not
complete. Its exact toys, complete production/reference comparisons, adjoint
diagnostics and refusal controls passed. The initial method propagated one
uniform error radius through each vector. Startup and endpoint errors therefore
became error allowances at every position in later stages. This was rigorous
but too conservative to pass the fixed usefulness gates.

A frozen row-zero diagnostic yielded uniform radius about 1.26e-10, and its
gain interval was about 1.05 million times wider than allowed. RI-60 preserves
the location of each error. This is a prospective arithmetic revision after
a recorded failure. It changes no coefficients, point precision, selected rows,
context lengths, reference tolerance, width threshold or scientific input.

The target remains the exact rational finite operator F_m, including each
stage's own odd extension, initialized ordered forward/reversed passes and
unpadding. Production binary64 and Decimal80 reference filtering remain rounded
evaluations, not exactly linear maps. The same independent exact small-system
DFI oracle is reused by its published v1 path and hash; it was not reauthored.

## Fixed pilot and interpretation

N=2769, L=4096 and T=N+2L=10961. The eight selected central rows are
0, 1, 27, 805, 1384, 2741, 2767 and 2768. With central injection E, context
injection U and central crop C, use

`a_i = E^T F_T^T C^T e_i - F_N^T e_i`,

`b_i = U^T F_T^T C^T e_i`,

`d_i = a_i^T x`, and `g_i = sum_j |b_ij|`.

For any explicitly supplied finite M>=0, the exact rowwise supremum is
`sup_{||z||inf<=M}|d_i+b_i z| = |d_i|+M*g_i`.
Enclosing that supremum does not turn its upper endpoint into an attained
numerical extremum. Attaining contexts may differ between rows. No physical
M is chosen. Without M, only conditional ingredients and exact-zero,
proved-nonzero or unresolved classifications may be reported.

The selected finite window is not infinite continuation; the eight rows are
not a full profile. Exact rational operator bounds do not supply a uniform
roundoff guarantee for production filtering over arbitrary extended inputs.
A native detector forward map and calibrated physical uncertainty remain
separate obligations.

## Per-coordinate residual proof

For one SOS section let
`H=[[-a1,1],[-a2,0]]`, `c=(1,0)`,
`J=(b1-a1*b0,b2-a2*b0)`,
`g=(b0+b1+b2)/(1+a1+a2)`, and `h=(g-b0,b2-a2*g)`.
The point adjoint is unchanged: it runs backward from zero terminal state,
outputs `b0*v_k+J^T*lambda_(k+1)`, then sets
`lambda_k=c^T*v_k+H^T*lambda_(k+1)`.
Only the first state coordinate is rounded; the second is an exact copy.
All point operations still round to 256 significant binary digits nearest/even.
Local output, first-state-coordinate and startup residuals are computed exactly.

For complex poles set `D=a2-a1^2/4>0`,
`P=[[a2,-a1/2],[-a1/2,1]]`, and `Q=P^-1`.
The exact identities are `H^T P H=a2 P` and `H Q H^T=a2 Q`.
Thus the adjoint state error contracts in Q norm by sqrt(a2). This is a
transpose bound, not backward propagation through H inverse.

For error vector e, duality gives
`|J^T e|<=sqrt(J^T P J)*||e||_Q`,
`|h^T e|<=sqrt(h^T P h)*||e||_Q`, and `||e1||_Q=sqrt(1/D)`.
Form J, h, DC products and quadratic forms exactly before bounding them.
Compute outward upper constants rho, jnorm, hnorm and f for these four roots,
with a proved `rho<1`. Let r_k be the incoming error radius at coordinate k,
s_next bound the next-state Q norm, and eX/eL the exact local residual magnitudes.
The update is

`output_radius_k = up(|b0|*r_k + jnorm*s_next + eX)`,

`s_k = up(rho*s_next + f*(r_k+eL))`.

The output uses s_next **before** the state bound is updated. The terminal
state bound is exactly zero. Each displayed nonnegative expression may be
computed exactly as a Fraction and then rounded upward once at 256 bits.
Every input is already an upper bound, so this cannot understate the result.
There is no statistical independence assumption on coordinate errors.

For a2=0, use stable component bounds u,v instead of the singular quadratic
form. Before the update, the output error is bounded by
`up(|b0|*r_k+|J0|*u+|J1|*v+eX)`; the next state bound is
`(up(|a1|*u+r_k+eL),u)`. Exact Jury conditions give `|a1|<1`.
The complex-pole path never uses an unstable entrywise-absolute H recurrence.
Unsupported denominator classes still refuse certification.

## Startup, padding and full composition

Each section's initial state depends directly on the ORIGINAL pass input's
first value, multiplied by h and the preceding exact DC-gain product. The
adjoint startup contribution is therefore a bypass to that original coordinate,
not an input to the earlier sections. Its error is bounded by
`up(hnorm*s_0+eP)` in the complex case, or
`up(|h0|*u_0+|h1|*v_0+eP)` in the scalar case.

Multiply by the absolute preceding DC product, accumulate upward with each
exact point-add residual, and add the total only at pass-input coordinate zero.
Do not divide by a preceding gain, which may vanish. Other coordinates retain
their own radii. The final point addition at coordinate zero has its own residual.

Reverse radius vectors alongside centers. The transpose of unpadding inserts
zero centers AND zero radii. The odd-extension transpose propagates each radius
through the absolute value of its own coefficient, retaining all endpoint and
reflected-index multiplicities; it cannot cancel uncertainty with a signed sum.
Include local point-rounding residuals afterward. Reverse stage order as in RI-55.
Induction through these operations encloses every exact adjoint coordinate.
The API's scalar `radius` is only the maximum reported coordinate radius;
the returned intervals use the individual radii.

Both H and H^T retain the same signed-power contraction admission search,
K=2^j for j=0,...,20, at 256-bit outward precision. Point arithmetic and exact
small DFII forward/transpose helpers retain their earlier definitions. The
finite coefficient, length, stage, padding, exponent, integer, serialization
and state-update caps remain explicit in `arithmetic_contract()`.
Resource failure or an unresolved bound yields no qualified certificate.
A positive radius must never silently underflow to zero.

Proof traces identify radius vectors by deterministic hashes and retain exact
maximum/endpoint summaries and state bounds. Their compactness does not replace
the analytic proof or the independent toy checks. Source review and reproduction
are required; no formal proof-assistant verification is claimed.

## Freeze, qualification and actual-input gate

The v2 qualifier pins the reused v1 oracle, frozen failed predecessor receipt,
current engine and all published numerical dependencies before parsing or
executing those snapshots. The previous failure cannot qualify the new method.
Current schema and source identities distinguish the attempts.

After independent method/source review, root must freeze the complete closure
before any revised admitted-coefficient execution. Both modes must pass the
same 196 gates: 32 exact toy cases, 14 complete forward-vector comparisons,
126 adjoint diagnostics, eight selected-row enclosure cases, the structural
constant check and 15 refusal categories. Every original numerical tolerance
and width rule remains. A mathematically valid but overwide enclosure fails.

The processor requires a caller-pinned successful CURRENT receipt, recomputes
all eight row certificates, and verifies their identities before actual input
access. Only then may it consume the unchanged RI-53 `input_hex` export.
Original printed-time metadata remains distinct from the nominal 4096 Hz index
clock. There is no interpolation, retiming, new acquisition or double filtering.
The actual context width limit remains `1e-12*max(abs(x))`, with no unit floor.
M is optional and must be a labeled canonical nonnegative rational under the
fixed integer bound. Outputs remain external, exclusive and complete: any
failed gate prevents an accepted partial sensitivity result.

## Evidence and remaining work

Root and independent complete-source reviews accept the recurrence, engine,
qualifier, driver and prospective guide. The earlier reviewed method-guide snapshot, before the pre-execution source
evidence was added, had SHA-256 `8d1f936971aa3284447ac9be95518d1feedb1545a7d12b600a703583f1bc8b2b`.
No admitted-coefficient calculation or actual-input computation preceded them.

| Frozen source | Bytes | SHA-256 |
|---|---:|---|
| `operator.py` | 30531 | `ef8169986977c533f549f2ca59b5f72224464db616d8303c451d6a29f22df6af` |
| `check.py` | 38088 | `a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02` |
| `process.py` | 17795 | `0c5ba1e0ac0091688ae1dc9b6dade04627a31614fa0a1891504cee8ab7862361` |

The engine author's normal/optimized tiny checks each passed 360 certified rows
and 2936 coordinate containments across 48 models, 192 forward cases, 40 dense
seeds, 360 unchanged-v1-center checks, 288 pass-error corners and 2384 odd-fold
corners, plus arithmetic/hash/refusal controls. Their 981-byte report SHA-256 is
`a87272dc05874b1861a033cdbe1292c2ea28e05b2ea31e5ef192b1440c5c21c6`.
A separate engine reviewer reconstructed exact DFI matrices: both modes passed
512 certified vectors/3904 coordinate containments, 512 radius-vector hashes,
864 nonuniform pass-error corners/4032 coordinates, 2512 odd-fold corners/12224
coordinates and eight refusals. Their identical 470-byte report SHA-256 is
`f29839e33e7bf13bef9af768cd5f2cbf498aeaee34f64f51e44fae99bbc913f4`.

The qualifier/driver author passed 104 helper/mock controls in each mode. An
independent reviewer passed 53 controls per mode with identical 2201-byte output,
SHA-256 `155e55df3700ada6c06d9e6b7eca9e41fe05cd323952b97b74dce6c4e24734c2`.
These include failed-predecessor status/source/inventory checks, rejection of that
old receipt as current qualification, current source binding and compatibility
with unequal coordinate radii. All runs exited zero with empty stderr. Complete
source comparison verified that all 196 numerical gates and thresholds remain
unchanged. These small tests do not establish full-length qualification.

The source closure was prospectively frozen before full qualification in both
modes; the successful result now admits separately gated actual-input processing.
Every failed run must remain visible; any source revision requires its own review
and freeze. The first attempt is preserved in verified commit
`995ed0390d1bd6a05a6a90c9aef021f09e9823d4`.

RET remains paused. Neither successful numerical qualification nor a finite
conditional bound would establish a native gravity prediction or calibrated
agreement with a detector observation.

## Full qualification result and reproduction

Root froze the twelve-file reviewed closure at 2026-09-24 07:30:59 UTC,
manifest SHA-256 `1b0fccef2046b53c1341b18c0fc7c1bc072d2eddf406bde271df24304818cef3`.
The guide actually frozen in both execution closures was 11240 bytes, SHA-256
`84a294c7b1cdf32bc76621c6c525e5827a78d4f0aacdf0f09e12e0cddd382585`.
Later guide edits add status, results and reproduction instructions; the method
and all executed Python sources remain fixed.
Normal and optimized executions took approximately 600 seconds each and
returned zero with empty stderr. Both emitted the same
[QUALIFICATION_REPORT.json](QUALIFICATION_REPORT.json): 9413345 bytes,
SHA-256 `1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f`.
All 196 gates passed, with no additional engine failure. All 126 retained
point-center diagnostics are byte-for-byte equal as JSON values to v1's
passing diagnostics; only their rigorous error enclosure method changed.

All eight gain-width and 56 synthetic-context-width checks pass. The largest
width/allowed-limit ratios are approximately 2.657e-45 and 1.372e-45,
respectively. Each selected continuation row has a rigorous nonzero coefficient
witness. All 24 structural row-sum/context-plus-extension intervals contain
zero, consistent with the exact constant-annihilation proof. These very narrow
arithmetic intervals certify the finite rational operator; they do not bound
physical model error, calibration uncertainty or rounded production error over
arbitrary extensions.

An independent standalone report audit imported no project code and evaluated
no filter coefficients. It passed 55786 checks per mode, with identical
1096-byte audit output SHA-256
`267ca7a3f9e0af3f8112e1bb456f0d3ca88005cd5450f3d4daa63c380c69bc30`.
It reconciled exact gate arithmetic, complete coverage, all width limits,
nonzero witnesses, structural intervals and source/predecessor identities.
This report reconciliation complements the separately reviewed proof and
small exact oracle checks; it is not another full coefficient computation.

Use the already qualified runtime documented in the
[RI-44 processing bundle](../gwosc_nominal_processing_v1/PROCESSING.md):
CPython 3.11.6, NumPy 2.1.3, SciPy 1.14.1, h5py 3.12.1 and the additional
platform/build fields in the receipt. The scripts check the complete runtime
identity. From the project root, choose an external directory and distinct
fresh output files. Enable shell noclobber so a replay cannot overwrite an
earlier successful or failed receipt:

```sh
set -C
python -I -B docs/experiments/gwosc_context_operator_v2/check.py > /absolute/external/qualification-normal.json
python -I -B -O docs/experiments/gwosc_context_operator_v2/check.py > /absolute/external/qualification-optimized.json
cmp /absolute/external/qualification-normal.json /absolute/external/qualification-optimized.json
```

Both qualifier commands must exit zero, their complete outputs must agree, and
the receipt must match the identity above before invoking the processor.
Preserve any failed output and its exit status; do not overwrite it for a retry. Its output leaf must not already exist
and must be outside Git checkouts. No envelope is supplied in this pilot:

```sh
python -I -B docs/experiments/gwosc_context_operator_v2/process.py \
  --qualification-report /absolute/external/qualification-normal.json \
  --expected-qualification-bytes 9413345 \
  --expected-qualification-sha256 1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f \
  --input docs/experiments/gwosc_nr_comparison_v1/REFERENCE.json \
  --output-dir /absolute/external/new-ri60-output
```

The processor first recomputes all sixteen qualified adjoint rows and reconciles
their complete summaries before reading the actual central export. The unchanged
RI-53 input export and its five published provenance dependencies were added to
a nineteen-file external closure only after root and independent qualification
adjudication. That closure froze at 2026-09-24 07:43:37 UTC, manifest SHA-256
`ade9e68d5d8ca9b1a75b5110f9642ae16a75eccebbbf327053cb2017dfce31d7`.
The successful actual results and their independent audit follow. All executed
Python sources remain identical to their reviewed pre-qualification snapshots;
guide changes record status, reproduction commands and evidence only.

## Actual reference-input result

Both actual executions exited zero with empty stderr after approximately
423 seconds per mode. They recomputed all sixteen coefficient certificates,
matched the qualified summaries, then consumed the unchanged RI-53 input.
Their identical [SENSITIVITY_REPORT.json](SENSITIVITY_REPORT.json) is 8556874 bytes,
SHA-256 `cb8347703040747f684538470dbf077a4b9beca072fdd4cdf3093c8a99b7b186`.
Both complete 205-byte stdout summaries have SHA-256
`21c833ee56cfc708742a0e03de20fb20ff30b195f3c54bcfddaa4196ae8e487a`.
All eight actual scale-relative context-width gates passed, with no failures
or partially accepted rows. No envelope argument or conditional-bound field
was supplied.

Root independently reconstructed all 2769 canonical input_hex values and their
22152-byte little-endian binary64 array, SHA-256
`e34926cba71051771bdea7a75f26ac207dc45c59a16c9142edacc0b154efc52f`.
Its peak is approximately 1.22636986555e-21; the exact rational is in the report.
The largest context-interval width divided by this peak is approximately
3.097e-58, well inside the unchanged 1e-12 limit. This is arithmetic enclosure
width, not the size of a continuation effect or a physical error bar.

The following numbers are rounded display approximations. Exact rational
endpoints, coefficient/proof identities and nonzero witnesses are in the report.
Here d_i is the exact-operator difference between the central crop of the
**zero-extended** finite long input and the short-input result. It is not a
claim that the unobserved physical continuation is zero.

| Central row | Continuation gain g_i, approximately | d_i / input peak, approximately |
|---:|---:|---:|
| 0 | 1.95270298638 | -0.0524854514627 |
| 1 | 1.85479653254 | -0.0673018817758 |
| 27 | 1.20465693942 | 0.00201961039115 |
| 805 | 0.703491781527 | 0.00653527180703 |
| 1384 | 0.627917258561 | 0.00336742006384 |
| 2741 | 1.23703560114 | -0.00388396188502 |
| 2767 | 1.89007281899 | 0.000829379050289 |
| 2768 | 1.98766786399 | 0.00618368311044 |

Every b_i is proved nonzero. Consequently each exact selected-row difference
is unbounded over completely unrestricted real context values. For a declared
finite box amplitude M the sharp rowwise quantity remains |d_i|+M*g_i;
this packet chooses no M and reports no physical continuation bound. The
zero-extension offset reaches about 6.73 percent of this input peak among the
eight rows, but that is one finite artificial-context comparison, not an
observational discrepancy or an uncertainty estimate.

A standalone independent audit passed 64278 checks per mode, producing
identical 31882-byte audit reports, SHA-256
`b13f0bd79682cc9a4895db8229577dd4c106faf8323e45d114ddcba166b3881c`.
It reconciled all input hex/time records, exact peak and interval-width rules,
all eight qualified row identities, nonzero witnesses, current source/runtime
pins, unchanged predecessor and absence of an implicit M. Its independently
reconstructed original-time metadata is 529613 bytes, SHA-256
`fdc6b3443453a648738ec894ff7c11be6db4cb7f007f2344f89294280c63becb`.
All nineteen frozen files remained unchanged. This independent output audit
does not recompute the unexported coefficient arrays or dot products: those
come from the two reviewed and reproduced engine executions. The distinction
between analytic proof, exact small oracle controls, full numerical qualification,
actual execution and exported-data reconciliation is retained.

The next public-data question is the same finite-context comparison using
actually recorded H1/L1 surrounding samples, with their original custody and
warnings. It is a separate design and driver, since this processor deliberately
accepts only the fixed RI-53 reference export. Native detector predictions,
calibrated confidence statements, infinite continuation and geometry/gravity
remain outside this successful numerical packet.
