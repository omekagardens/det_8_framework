# QR-05AR results: fine-response measurement sufficiency

8 September 2026. Completed bounded investigative gate: coarse-measurement
sufficiency fails for some fine questions; the explicit fine-measurement repair
passes. Protocol: [README.md](README.md). Evidence: [results.json](results.json).
Base: pushed AQ commit `8e1bac5f1e0e6d7c01f9d08708e56db8c0ad8ed8`.

## Main finding

The same 32 coarse moments that determine all 49 coarse responses do NOT
determine all 64 fine responses on AQ's unchanged nonnegative source simplex.
This is actual information loss, not merely failure of an inherited decoder:
two admissible normalized mixtures give exactly the same coarse measurements
but different fine truths. No decoder of those measurements can resolve that
ambiguity throughout the declared simplex.

Both grid and warp retain the same 108 original fine-tile Bernstein generators,
7 coarse cells, 8 fine cells, 8 coarse tiles and 12 original fine tiles.
No source amplitude, support, local coordinate or ordering was changed.

| Per family | Grid | Warp |
|---|---:|---:|
| Measured coarse moments | 32 | 32 |
| rank A, including known normalization | 32 | 33 |
| rank of fine-target matrix Q | 24 | 24 |
| rank [A;Q] | 37 | 38 |
| Recoverable fine-response rows | 51 of 64 | 51 of 64 |
| Recoverable identically-zero / nonzero rows | 33 / 18 | 33 / 18 |
| Unrecoverable fine-response rows | 13 | 13 |
| Repair tiles / added overlay tiles | 12 / 0 | 12 / 0 |
| Fine/repair moment values | 48 | 48 |
| Nonzero repair residual entries | 0 of 6,912 | 0 of 6,912 |

A=[1^T;O_coarse]. The normalization row is known, not an extra measured value.
Target rank24 being below the measurement count32 does not imply recovery:
the relevant row spaces differ. The joint-rank increment is five in both
families; the thirteen failed questions are not thirteen independent lost
directions. Row counts are not success probabilities, and 33 recovered rows
are identically zero.

The same thirteen ordered fine pairs fail in both geometries:
(1,2), (1,3), (2,2), (2,3), (2,4), (2,7), (2,9), (2,10),
(3,3), (3,4), (3,7), (3,9), (3,10).
All fixed response scales are positive. Generic empty-region cases retain
zero raw targets, recovered zero rows and null normalized differences.

## Exact recovery-or-collision certificate

Write F=sum_g lambda_g phi_g, lambda>=0, sum(lambda)=1.
Measurements and true responses are O*lambda and Q*lambda.
A target row is recoverable precisely when it belongs to rowspace(A).
For every recoverable row, retain its unique coefficient vector in the
lexicographically first independent ORIGINAL row basis of A. Retain all
other rows explicitly as failed, not as zero decoder rows.

If w is in ker(A) and Q*w is nonzero, its positive and negative parts have
equal mass. Normalizing each gives two genuine simplex mixtures.
Their coarse observations coincide; their fine responses differ.
This excludes even nonlinear decoding of those same data on the full
declared simplex. It does not exclude recovery on a smaller source family.

The primary Gauss-Jordan route, independent forward-elimination/back-substitution
route and separate rational Gram-Schmidt oracle agree on all ranks,
row bases, pivot/free columns, recovery decisions, complete decoder identities
and the canonical first-free-column/first-detecting-row rule.
No witness was chosen to maximize the observed difference.

Let e_g mean a unit weight on zero-based generator g. The retained witnesses are:

| Quantity | Grid | Warp |
|---|---|---|
| Canonical null direction | 3e0-4e1+e9 | 9e0-9e1-e9+e10 |
| Positive mass | 4 | 10 |
| lambda_plus | (3/4)e0+(1/4)e9 | (9/10)e0+(1/10)e10 |
| lambda_minus | e1 | (9/10)e1+(1/10)e9 |
| First free column / separating row index | 9 / 1 | 10 / 1 |
| First separating pair | (1,2) | (1,2) |
| True plus response at (1,2) | 1/73728 | 1/3538944 |
| True minus response at (1,2) | 1/82944 | 1/5308416 |
| True plus-minus difference | 1/663552 | 1/10616832 |
| Difference divided by V^2*h_1*h_2 | 1/288 | 1/160 |

Every weight, all 32 coarse observations and all 64 true responses for BOTH
mixtures are retained and checked. Truth difference is Q*w/mass, not Q*w.
Each first witness distinguishes only (1,2) and (1,3), not all thirteen
failed rows. The raw differences at those two pairs are equal and opposite;
their normalized differences are grid +1/288,-1/288 and warp +1/160,-1/480.
These declared dimensional normalizations are not percentages of true response
or maximum-error bounds.

Here original source tiles0 and1 belong to fine source cell1 and coarse
observation tile0. Fine destination cells2 and3 share coarse parent2.
The witness redistributes their responses without changing the parent sum.
Thus even destination resolution can expose lost information; a failure need
not arise from uncertainty about the fine source-cell label.

## Repair: explicit new access, unchanged source model

The repair takes four incoming-field moments, in global (1,u,v,uv) order,
on each deterministic fine-endpoint overlay tile. In these fixed geometries,
the twelve original fine tiles already accommodate all fine destination
breakpoints: the overlay adds zero pieces. Generic controls do require
additional pieces, including splits caused by inactive knots.

All integrations continue to use the original source supports and original
Bernstein coordinates. The generic overlay test explicitly distinguishes this
from restarting source polynomials on smaller pieces.

Each outgoing tail R_D is bilinear on an admitted repair tile, so its geometric
coefficients give an exact response map. Both implementations integrate true Q
independently of this map, then check the complete identity
G_repair*O_repair=Q_fine. For the two collision mixtures, the newly acquired
moments differ and the map reconstructs each complete true response exactly.
The branch-and-ownership argument also applies to any integrable incoming F
on the admitted supplied geometry; that structural statement is distinct
from the finite-simplex sufficiency certificate.

Fine measurements are NEW values of the unknown field. Supplied geometry
specifies where and how to measure; it cannot supply these values from coarse
data. Coarse moments are parent sums of the fine/repair moments. Therefore
48 versus32 describes two measurement banks, not80 independent values, and
does not prove that16 new local measurements or all48 fine values are minimal.

All sixteen geometric moments per tile, three observation levels, two target
levels, direct repair-to-coarse sums and double-parent response sums agree.
These are additive integrals, not a product/composition rule. The dictionary
sums to the V^2-constant field almost everywhere; its integral is V^3.
That unweighted sum is not a normalized mixture.

AQ's selected geometry, original source coefficients, coarse measurements,
coarse targets and geometric map are exactly preserved. No older executor,
AQ canonical residual calculation or unselected historical mathematics was
replayed. AO's narrower-span success and AQ's coarse structural identity
remain intact.

## Retained representation and verification

Across both families: 216 sources, 1,944 source coefficients,
27,648 observation entries across the three banks, 24,408 target entries,
9,408 raw geometric-map coefficients including repair intercepts, and
3,315 recoverable-row decoder entries. The complete repair retains
13,824 predictions and 13,824 zero residuals.
The two coarse collision certificates contain 1,162 rational occurrences;
their repair witnesses contain 1,120. Zeros and repetitions count.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Geometry-only inherited input | 1,955 | 1,965 |
| Derived geometry | 18,110 | 20,203 |
| Original source dictionary | 11,305 | 12,837 |
| Three measurement label/matrix projections | 90,588 | 93,408 |
| Two target label/matrix projections | 79,665 | 81,461 |
| Sufficiency certificate | 14,580 | 14,956 |
| Complete repair certificate | 107,867 | 108,914 |
| Complete native family | 337,930 | 348,120 |

Suite size: 688,321 bytes. These scopes overlap, include verification material,
and are not additive unique storage or a compact online packet.

All 65 tests pass normally and optimized: 53.17 s / 53.11 s in the recorded
concurrent runs. Before freeze, 56 generic tests passed in both modes
(12.95 s / 12.97 s); all 9 fixed tests were deselected. Coverage includes:

- Complete independent beta/tail-integral and Gram-Schmidt family/suite oracles.
- Analytic normalized collisions, partial and normalization-only recovery,
  duplicate/dependent columns, tiny exact pivots and first-free witness ordering.
- Full affine transport of source coefficients, all moments/observations,
  outgoing coefficients, target sums and repair maps; canonical recertification
  and separate transport of dense recovered maps.
- Same-level recovery without full-field identification, empty regions,
  original-coordinate overlay integration, shared-input detachment and
  file-blind affine application.
- Accepted certificate bounds 256 by 576 and application bounds 64 by 1024;
  late shape rejection and a 406-piece overlay rejected before moment arithmetic.
- 214 explicit guard rejections in each isolated subprocess mode:
  104 per engine plus three early-admission checks per engine.
- 295 rejected non-noop corruptions: 131 generic family/null changes,
  144 fixed family changes, 8 suite changes and 12 selected-producer changes.
  One unselected prior decoder residual mutation is deliberately admitted by
  the projection/selected-bridge helpers; the whole real prior artifact is pinned.
- Create-only capture, canonical native wires, identity changes, symlink refusal,
  isolated execution, external caches, bounded serialization and read-only replay.

The optimized pytest run emits its usual assertion warning for non-test
modules. Engine admission uses explicit exceptions, with separate isolated
normal/-O guard execution. Capture/working byte caps are serialized-document
limits, not process-memory bounds or exhaustive hostile-input hardening.

## Freeze and evidence lifecycle

Five sources were frozen at 2026-09-08 21:02:21 UTC, before any fixed AR
projection, overlay, integration, rank or collision calculation.
All 112 authenticated targets were bracketed: 5 AR sources, 48 prior captures
and 59 ancestor sources.

1. First external primary/reference comparison: 2.9575 s.
2. Exactly ONE independent normal reference-only read-only audit: 2.0725 s.
3. Full normal/-O tests; all 112 identities and first-capture bytes rechecked.
4. External create-only comparison preflight: 2.9746 s.
5. Exclusive final comparison capture: 2.9727 s.
6. Fresh primary-normal / reference--O final read-only replays: 1.3204 s / 2.0144 s.

The independent audit and full tests ran concurrently after the first
comparison; both finished before preflight. All non-runtime fields of first,
preflight and final captures agree exactly. All 112 identities and each
capture's bytes remained unchanged across verification.

Prefreeze review strengthened the primary's late rational-pair SHAPE admission
before rectangle arithmetic. Test authoring corrections fixed an append
parenthesis, outgoing-record paths, helper argument order and the unselected
AQ decoder path; corresponding-column and affine checks were strengthened.
No mathematical model or fixed result was changed. There were NO post-first
source, protocol, fixture or mathematical corrections.
The staged whitespace check reports one cosmetic terminal blank line in the
frozen README; its authenticated bytes are retained unchanged.

Final capture: 704,842 bytes, SHA256
`c9ed0e299c057eb6503238a3bc5ce18352abe81bc111615464afaa6ed264e4f8`.
Complete suite: 688,321 bytes, SHA256
`9f899fb55dcd93cb794161484c874b5b8043537928820fba57369b1910bd810e`.

## Next bounded question and application value

The immediate value is a verifiable interface boundary: coarse data suffice
for declared coarse questions, but not every finer question. A source-side
system with fine access can compute exact fine responses; a coarse-only
receiver cannot infer the missing information without new input.

Proposed QR-05AS will construct query-specific supplemental linear readouts.
The retained rank increment is five in both cases. A prospective exact
quotient construction can select target rows independent modulo A, retain
their explicit repair-moment filters, and certify full decoding from coarse
data plus those readouts. This is a transmission/storage interface question,
not a surprise source of free measurements.

Any minimality claim must be limited to fixed noiseless scalar linear
readouts on the full declared source simplex. A signed/global filter may
require many local moments to acquire. Selecting the smallest subset of
individual moment measurements, apparatus cost, noise/precision, adaptive
readouts, physical source preparation, unknown geometry and gravity remain
separate questions. No AS filter selection or decoder construction has run.
