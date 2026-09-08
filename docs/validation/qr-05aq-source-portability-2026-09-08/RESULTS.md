# QR-05AQ results: frozen-decoder source-span portability

8 September 2026. Completed bounded investigative gate; canonical portability
fails, while the geometric control passes. Protocol: [README.md](README.md).
Evidence: [results.json](results.json). Base: pushed AP commit
`5b4d767a1942640c38b8205b9a30d50208becdb0`.

## Main finding

The SAME four weighted moments per coarse tile remain sufficient for every
declared coarse response on the new sources. The SAME canonical compact
decoder does not remain correct. This is a clean source-model dependence
result for a frozen decoder, NOT a proof that the measurements are insufficient.

Keep AO's supplied whole-probe l1/l2 geometry, AP's embedded original
observations/targets, and both inherited policies. Each grid/warp case retains
7 coarse cells, 8 fine cells, 8 coarse tiles, 12 fine tiles, 32 measurements
and all 49 ordered coarse responses. Replace the old 64-column source model
with 108 V-squared-scaled nonnegative fine-tile Bernstein biquadratics:
9 per positive fine tile. No decoder was fitted, selected, clipped or projected.

V is the probe volume. The explicit coefficient/antiderivative engine,
independent interpolation/knot-split Simpson engine and separate beta-integral
test oracle agree on the
complete new measurements, independently integrated true responses and
residual certificates. True responses were not obtained by treating G*O_new
as an oracle.

| Per family | Grid | Warp |
|---|---:|---:|
| New generators | 108 | 108 |
| Geometric nonzero residual entries | 0 | 0 |
| Canonical nonzero residual entries | 305 | 330 |
| Negative / positive canonical residuals | 168 / 137 | 187 / 143 |
| Canonical failed response rows | 10 of 49 | 10 of 49 |
| Generators with any canonical failure | 96 of 108 | 99 of 108 |
| Sharp maximum absolute normalized mismatch | 11/36 | 49/100 |

A "failed generator" has at least one nonzero response error. It does not
mean every response fails for that generator. There are 39 identically
zero-error canonical response rows in each case. Both families fail the same
ten rows:
(1,1), (1,2), (1,3), (1,4), (1,6), (3,3), (4,4), (6,6), (8,8), (8,9).
All 49 response scales are positive in each fixed case; generic empty regions
retain explicit normalized nulls without hiding raw failures.

## Structural reason and what was actually tested

For supplied clipped destination D, the outgoing function is

```text
R_D(u,v) = clamp(d_u1-u,0,d_u1-d_u0)
         * clamp(d_v1-v,0,d_v1-d_v0) / 2.
```

On each admitted coarse tile t it is bilinear, with independently derived
coefficients b_Dt in the basis (1,u,v,uv). Consequently,

```text
y_CD(F) = sum over t owned by C:
          b_Dt dot integral_t F(u,v)*(1,u,v,uv) dmu,
dmu = du*dv/2.
```

This establishes the geometric response identity for any integrable incoming
F on the declared supplied geometry. The argument uses the actual branches
and tile ownership, not an extrapolation from a finite matrix identity.
The entire newly derived G equals the inherited geometric matrix. Both
complete old response identities were also rechecked.

The canonical map instead has error a+(L_canonical-G)x. Being exact on the
old observations need not make this expression vanish on new observations.
All inherited fixed intercepts happen to be zero, but neither implementation
discarded them; generic nonzero-intercept tests pass.

For fine tile f, the new source is V^2*B_i(xi_f)*B_j(eta_f) in its interior
and zero elsewhere, including boundaries. Quadrature uses its one-sided
polynomial extension at support endpoints. The local Bernstein factors are
nonnegative and sum to one. Their global monomial coefficients can be signed.

All 16 geometric moments on every coarse/fine tile were independently
reconstructed and their parent sums checked. Nine generators on a tile sum
to the constant V^2 on that tile almost everywhere; each integrates to
V^2*h_f/9. The complete unweighted dictionary sum integrates to V^3.
This is not a normalized mixture and does not inherit the old chain-model
V^4/576 identity.

## Signed extrema and actual nonnegative counterexamples

Errors are prediction minus truth. Normalize row (C,D) by V^2*h_C*h_D.
This is a declared dimensional scale, NOT a percentage of the true response.

For unknown normalized nonnegative weights lambda,

```text
e(lambda) = sum_g lambda_g * e_g,  lambda_g >= 0, sum_g lambda_g = 1.
```

Thus every retained row minimum, maximum and maximum absolute error is sharp
on this dictionary simplex. The capture keeps ALL attaining generator indices,
not just one chosen tie. The bounds are not AP's measurement-error gains,
empirical noise risks or bounds over arbitrary integrable fields.

The only globally maximum-absolute-error response row is (8,9) in each family:

| Signed normalized extremum at (8,9) | Grid | Warp | All attaining generator indices |
|---|---:|---:|---|
| Minimum (attains maximum absolute error) | -11/36 | -49/100 | 56, 59, 62 |
| Maximum | 65/216 | 15533/32400 | 83 |

Indices are zero-based. Generators 56,59,62 are fine tile6 with j=2 and
i=0,1,2. No negative mixture weights are needed to attain these errors.
Every geometric row has zero extrema and all 108 generators attain each one.

The prescribed first-generator/first-row rule selects generator0, fine tile0,
i=j=0, detected first at response (1,1). It is not selected for maximum error.

| First-witness quantity at (1,1) | Grid | Warp |
|---|---:|---:|
| Support | [0,1/3] x [0,1/4] | [0,1/9] x [0,1/16] |
| True response | 7/110592 | 5/5308416 |
| Canonical prediction | 1/165888 | 1/11943936 |
| Raw error | -19/331776 | -41/47775744 |
| Normalized error | -19/576 | -41/2304 |

Both complete witnesses also give positive canonical predictions for (8,8)
and (8,9), where the true response to this localized source is zero.
At (8,9) these predictions are 1/6912 (grid) and 7/30720 (warp).
This exposes reliance on old source-model correlations; it is not a physical
nonlocality result.

Each retained witness includes all 108 weights, 32 observations and complete
49-component truth, prediction, signed-error and normalized-error vectors.
Weights are the actual unit-simplex vertex, not a signed null difference.
All vectors, support and normalization were checked.

## Retained representation and validation

Across both families the capture retains 216 new sources, 1,944 source
coefficients, 6,912 observation entries and 10,584 independently integrated
target entries. Both maps together retain 6,468 raw coefficients including
intercepts, 21,168 predictions, 21,168 signed residuals and 21,168 normalized
residuals. There are 588 rational row-extremum values, 57,546 repeated
attainer-index occurrences, and two complete witnesses with 672 rational
entries. These counts include retained zeros and repetitions; they are not
counts of independent information.

| Canonical serialized scope, newline included | Grid bytes | Warp bytes |
|---|---:|---:|
| Inherited input projection | 53,392 | 56,457 |
| Derived geometry | 9,219 | 10,447 |
| Source dictionary | 11,305 | 12,837 |
| Measurement labels and matrix | 23,004 | 23,944 |
| Target labels and matrix | 34,717 | 35,600 |
| Both decoder certificates | 317,785 | 322,372 |
| Complete native family | 452,177 | 464,620 |

The complete suite is 918,833 bytes. These scopes overlap and must not be
added as unique storage or described as a compact online packet.

All 66 tests pass in normal and optimized Python (37.71 s / 37.57 s in the
recorded concurrent runs). Before freeze, 57 generic tests passed in both
modes, with all nine fixed tests deselected. Tests include:

- Complete independent family and suite oracles; all nine unit anchors;
  signed residuals, complete ties and first-generator witnesses.
- Nonzero intercepts, raw empty-response failures, inactive-axis knot
  acceptance versus active-knot rejection, and boundary quadrature.
- Same-map positive affine transport of geometry, moments, source
  coefficients, measurements, targets, residuals, extrema and witnesses.
- Complete accepted 72- and 576-generator cases; restricted file-blind apply,
  detached outputs, shared valid containers and intermediate cancellation.
- Late shape rejection before rectangle arithmetic; 176 explicit guard
  rejections per mode: two engines times (65 malformed families,
  22 malformed applications and one retained overflow).
- 155 rejected non-noop corruptions: 49 generic, 86 fixed-family,
  8 suite and 12 selected-producer changes.
- Create-only capture, read-only replay, canonical/native types, source and
  artifact changes, symlink refusal, external caches and serialization caps.

One additional unselected AP gain mutation is deliberately admitted by the
input-projection helper: that helper does not replay unselected mathematics.
Whole historical artifacts remain pinned, so this does not authorize changing
the actual prior artifact.

The optimized pytest run emits its usual warning about assertions in
non-test modules. Engine admission uses explicit exceptions, and dedicated
isolated normal/-O subprocess tests explicitly check the guard inventory.

## Freeze and evidence lifecycle

Five sources were frozen at 2026-09-08 20:15:28 UTC, before any fixed AQ
projection/integration/residual calculation. There are 106 distinct
authenticated targets: 5 AQ sources, 47 prior captures and 54 ancestor sources.
AP and the selected AO artifact are explicitly pinned in the protocol.
No historical executor was run.

The evidence lifecycle completed as follows. The independent audit and full
tests ran concurrently after the first comparison; both completed before
the preflight:

1. First primary/reference comparison, externally captured: suite 3.6495 s.
2. Exactly ONE independent normal reference-only read-only audit: 3.0399 s.
3. Full normal/-O tests and a post-test identity/first-capture bracket.
4. External create-only comparison preflight: 3.6826 s.
5. Exclusive final comparison capture: 3.6583 s.
6. Fresh read-only primary-normal / reference--O replays: 1.1780 / 2.9598 s.

All non-runtime fields of first, preflight and final captures agree exactly.
All 106 identities and final bytes remained unchanged across verification.
Timing is verification work, not an application benchmark. The final recorded
RSS high-water mark is 263,962,624 bytes. The 128 MiB capture and 192 MiB
serialized working-document limits are not process-memory limits or
exhaustive hostile-input guarantees.

Two prospective orchestration clarifications occurred before freeze:
the inherited-history tuple is converted to native lists for exact comparison,
and the protocol explicitly distinguishes input identity admission before
builds from its recheck afterward. Selected old moments are checked only
after new calculations. Ordinary formatting and a test-closure binding were
completed before freeze. No post-first source, protocol, fixture or
mathematical correction was needed.

Final [results.json](results.json): 934,498 bytes; SHA256
`c9c0bb0b20cd3646217e6ad97eaf2f41ca40406fc94d8fac975b67267eec6a08`.
Canonical suite: 918,833 bytes; SHA256
`25cfd4843a5c4940a4dc5beceb16b6b41e0fa61b1e1ed019b32326ed829d51bc`.

Sources, ancestry, complete mathematical data and runtime metadata are in the
capture. README remains prospective; this report and the bridge roadmap are
outside its frozen source ledger.

## Application meaning and next boundary

For a supplied-geometry response service, the geometric map offers a
source-span-independent coarse-response contract with the SAME measurement
interface. AQ distinguishes that structural justification from exactness
certified only on a source dictionary. AP separately described measurement-error
amplification; AQ does not combine the two into an empirical performance claim.

This provides a useful rule for the broader calculus: a prediction-sufficient
representation is relative to its measurement access, source assumptions and
question family. A compact decoder should not silently carry its original
source-model relations into an enlarged domain.

Next proposed gate QR-05AR changes the question resolution, not the source
family: test the current coarse moments against fine-region responses on the
same AQ dictionary. Retain either an exact recovery certificate or TWO
normalized nonnegative mixtures with identical coarse observations and
different fine responses. Include normalization in the observation matrix.
Test fine-tile moments as explicitly new measurements and a structural repair;
geometry alone does not supply the unknown field's missing fine moments.
Do not presume failure, minimality or a free coarse-to-fine reconstruction.

No old convex-hull inclusion, full-field recovery extension, physical source
preparation, calibrated sensor noise, unknown-geometry reconstruction, quantum
channel, gravity derivation, RET integration, Lean verification or production
API hardening is established. Prior quantum and geometric obstructions remain
intact. RET/core/governance work and the temporary model sheet were not changed.
