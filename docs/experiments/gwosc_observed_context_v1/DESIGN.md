# RI-62 — finite observed-context comparison

24 September 2026 UTC. **Prospective design; coordinator adjudication accepted.**
No new observed sample body was read, filtering performed, driver implemented,
or comparison result produced in this packet. This freezes a later application
of the accepted [RI-60 finite operator](../gwosc_context_operator_v2/IMPLEMENTATION.md)
to the already qualified public H1/L1 observations. It preserves the
[RI-55 exact-operator definition](../gwosc_context_sensitivity_v1/DESIGN.md),
every accepted numerical source, the separate native proof lane and RET pause.

The question is concrete: how do the same central observed samples change
under the prescribed filter when their input is the short segment, a specified
longer segment containing recorded surroundings, or the previously processed
32-second record? The three results have different finite boundary conditions.
The longest record is not physical ground truth, and increasing context is not
assumed to improve results monotonically. No criterion requires the observed
context effect to be small.

## 1. Fixed inputs and admission

Use only the [RI-37 V2 pair](../gwosc_input_qualification_v1/QUALIFICATION.md),
at its original 4096 Hz index clock. Preserve both complete byte snapshots:

| Detector / filename | Bytes | Publisher MD5 | Local SHA-256 |
|---|---:|---|---|
| H1 / `H-H1_LOSC_4_V2-1126259446-32.hdf5` | 1040592 | `50441a42c13fc1f14e5c4ea5527f1515` | `6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6` |
| L1 / `L-L1_LOSC_4_V2-1126259446-32.hdf5` | 1007420 | `361ae6a040a9fef7897b1e0124d5b0a1` | `56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189` |

Each record has 131072 finite binary64 samples at
`1126259446 + k/4096`, `0 <= k < 131072`. Dimensionless nominal strain is the
release interpretation; retain the literal empty HDF5 `Yunits` attribute.
Before any HDF5 parsing, verify both complete snapshots against all identities
above, then inspect and extract from those same retained bytes. Reuse the
accepted inspector and reconcile its complete result with the pinned report.
No substituted release, longer product or independently downsampled overlap
is admitted. [GWOSC release details](https://gwosc.org/techdetails/) explain
the V2/C02 mapping and distinguish the separately downsampled products.

Keep every RI-37 quality, injection, missingness and DATA-exclusion annotation.
Both records have DATA throughout and no missing samples. H1's `NO_CW_HW_INJ`
flag is set throughout; L1's is clear throughout. Retain the L1 samples with
the unchanged visible/report warning: "L1 NO_CW_HW_INJ flag is clear throughout
input interval; samples retained. Injection absence and negligible effect are
not claimed." A clear injection flag is not missing data. No additional veto,
injection-effect correction or inference is introduced.

Before opening any observed input, including the published crop, bind the
current successful RI-60 qualification receipt and the complete reused source
and numerical dependency closure. Recompute all sixteen qualified adjoint rows
(eight each at lengths N and T), and reconcile their complete certificate
identities and summaries with that receipt. The failed v1 receipt cannot admit
this calculation. The new driver must not broaden the existing RI-60 processor,
which deliberately accepts only the RI-53 NR export.

The principal frozen dependencies are below. Relative paths resolve from this
directory. Verify byte identities before parsing/importing/executing the retained
snapshots, and preserve all additional dependencies checked by the published
RI-60 qualifier and RI-47 consumer.

| Dependency | Bytes | SHA-256 |
|---|---:|---|
| [RI-42 recipe](../gwosc_nominal_display_v1/RECIPE.md) | 14014 | `872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a` |
| [RI-44 coefficients](../gwosc_nominal_processing_v1/COEFFICIENTS.json) | 7698 | `700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0` |
| [RI-44 production](../gwosc_nominal_processing_v1/filtering.py) | 8805 | `9a93c1f218fecfa6fdf7ee0e30e054ad0973dfb1f04ae339dfbb0e7a6f8ae1be` |
| [RI-44 independent Decimal reference](../gwosc_nominal_processing_v1/reference.py) | 7253 | `c8cffaac8bf0c1647a120ecb00ba1505ef69b60f80cda653d60b2a2f7e9da305` |
| [RI-44 synthetic receipt](../gwosc_nominal_processing_v1/SYNTHETIC_REPORT.json) | 107468 | `2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3` |
| [RI-37 inspector](../gwosc_input_qualification_v1/inspect_inputs.py) | 14817 | `bdafb9c694fc9f33071072f1a2fc027bdb85e9262245ad3f9e29f860935d142a` |
| [RI-37 metadata report](../gwosc_input_qualification_v1/INPUT_REPORT.json) | 31096 | `a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80` |
| [RI-60 engine](../gwosc_context_operator_v2/operator.py) | 30531 | `ef8169986977c533f549f2ca59b5f72224464db616d8303c451d6a29f22df6af` |
| [RI-60 qualifier](../gwosc_context_operator_v2/check.py) | 38088 | `a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02` |
| [Reused exact oracle](../gwosc_context_operator_v1/oracle.py) | 9484 | `37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651` |
| [RI-60 qualification receipt](../gwosc_context_operator_v2/QUALIFICATION_REPORT.json) | 9413345 | `1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f` |
| [RI-47 rounded crop](../gwosc_nominal_result_v1/CROP.json) | 395470 | `a580481b9f6ea8dbb90242f12023817709ee7ac208d504110966f01f353592e7` |
| [RI-47 processing receipt](../gwosc_nominal_result_v1/PROCESSING_REPORT.json) | 159384 | `98bf0c53d5b988d3bb2aaa5f60c0fbcd87512501dd1137175b25589cc4856820` |

The accepted RI-60 actual NR report is historical prerequisite evidence,
8556874 bytes, SHA-256
`cb8347703040747f684538470dbf077a4b9beca072fdd4cdf3093c8a99b7b186`.
Its NR samples and measured amplitudes are not inputs to this comparison or
to its selection rules. Its successful actual-input result does not certify
the yet-uncomputed observed-context outputs.

Use the existing admitted CPython 3.11.6 / NumPy 2.1.3 / SciPy 1.14.1 /
h5py 3.12.1 runtime, including the full build/platform/library configuration
matched by RI-60. Preserve float64 production, the independently authored
80-digit Decimal recurrence and the 256-bit certified engine. Every one of the
17 filter stages, coefficient bit patterns, section order, separate odd padding,
DC initialization, reversal and unpadding stays fixed. The
[SciPy method specification](https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.signal.sosfiltfilt.html)
does not replace the admitted explicit per-stage settings.

## 2. Windows and three comparisons

For each detector separately let X be the unchanged raw record. Set
`N=2769`, `L=4096`, `T=N+2L=10961`, with half-open integer slices:

```text
x = X[65536:68305]                         # N central samples
w = X[61440:72401]                         # T recorded samples
z = concat(X[61440:65536], X[68305:72401])  # left L, then right L
```

Thus `w=(z[:L],x,z[L:])` exactly, including signed zeros. The extended window
starts at GPS 1126259461. Central index j has exact clock
`1126259462+j/4096`, for `0 <= j < N`; its exclusive end is
`1126259462+2769/4096`. Use integer indexing and rational offsets, never a
floating comparison of large GPS timestamps. The length matches RI-60's
qualified operator for reuse; it makes no correspondence claim between these
observations and the NR reference's printed-time grid.

Apply the unchanged production filter independently to x and w, obtaining
binary64 arrays p_short of length N and p_long of length T. Do not filter an
already filtered crop. Set p_context=p_long[L:L+N]. For p_record take the first
2769 values of the corresponding detector in RI-47's unchanged 4096-sample
crop. These are the same source indices [65536:68305), from the previously
filtered complete 32-second record. Verify the entire crop, both detector
array identities, grid, input provenance and annotation identities before this
subset operation; retain the original complete export unchanged.

Retain all N points of each of the three arrays with their original coordinates.
No alignment, fitted lag, sign inversion, mean subtraction, taper, interpolation,
normalization, extra calibration correction or changed stage is allowed.
Define two nominal differences over the whole center:

```text
D_context[j] = exact_fraction(p_context[j]) - exact_fraction(p_short[j])
D_record[j]  = exact_fraction(p_record[j])  - exact_fraction(p_context[j])
```

Compute these differences and their maxima as exact differences of the retained
finite binary64 values; do not hide a further subtraction rounding. Report
every difference, the maximum absolute difference and every maximizing index.
These are descriptive finite-array quantities, not residual scores, calibrated
errors, noise estimates or detection statistics. There is no magnitude pass/fail
gate. The record comparison is entirely a comparison with a published rounded
baseline; this packet does not certify exact F_131072 or refilter that record.

## 3. Exact selected-row question

F_m means the exact rational finite operator of RI-55, using the admitted
binary64 coefficients interpreted exactly. It is different from both rounded
production and rounded Decimal evaluation. Let E insert the center into zeros,
U insert the two context blocks around a zero center, and C retain [L:L+N).
Then w=Ex+Uz and, at the unchanged pilot indices

```text
I = (0, 1, 27, 805, 1384, 2741, 2767, 2768),
```

write s_i=F_N^T e_i, v_i=F_T^T C^T e_i,
a_i=E^T v_i-s_i and b_i=U^T v_i. The exact outputs and difference are

```text
y_short,i = s_i^T x
y_context,i = v_i^T w
Delta_i = y_context,i - y_short,i = a_i^T x + b_i^T z.
```

All input values in these expressions are their exact dyadic rational values.
The context z is a known part of the same released record. No M, assumed
continuation, peak multiplier or adversarial box is introduced. The identity
describes this finite w only, not an unknown physical continuation outside it.

Use the recomputed qualified coefficient intervals to enclose each output and
Delta. Interval dot products must multiply by the exact signed input values,
choose the correct endpoint order and sum exactly (or with separately proved
outward rounding included). Obtain Delta directly from the a/b rows. Also form
the difference of the independently retained short/long output intervals as a
consistency check: both enclose the same exact quantity, so their intersection
must be nonempty. Do not claim equal endpoints; the two constructions retain
different interval dependencies. Preserve the direct a/b interval for the
fixed width gate rather than selecting the narrower result after inspection.

Let A_x=max|x_j| and A_w=max|w_j|, evaluated exactly. For every detector and
every i in I require

```text
width(direct Delta interval) <= 1e-12 * A_w.
```

There is no unit floor. A zero extended input requires exact [0,0]. An overly
wide valid interval fails qualification for this pilot; do not raise precision,
change rows or loosen the gate in response to its result.

## 4. Numerical checks and actual-specific rigorous bounds

First compare every production output to the unrounded retained Decimal-80
output for the same input and admitted coefficients. Independently apply both
implementations to x and to w; do not compare only the center of w. Require

```text
max_j |p_short[j] - Decimal_short[j]| <= 1e-9 * A_x
max_k |p_long[k]  - Decimal_long[k]|  <= 1e-9 * A_w.
```

Form residuals, peaks and threshold comparisons as exact Fractions of the
retained finite binary64/Decimal values. Zero inputs must produce exact zero
in both implementations. These complete-vector checks are numerical diagnostics;
Decimal agreement by itself is not a rigorous error bound against exact F_m.

Separately, let J_short,i and J_context,i be the certified exact-output
intervals from section 3. For a point p and interval [l,u], define
`distance_bound(p,[l,u])=max(abs(p-l),abs(p-u))`. Since the true exact value
lies in that interval, passing the following proves an actual-specific bound:

```text
distance_bound(exact_fraction(p_short[i]), J_short,i) <= 1e-9 * A_x
distance_bound(exact_fraction(p_context[i]), J_context,i) <= 1e-9 * A_w
distance_bound(D_context[i], direct Delta interval) <= 1e-9 * (A_x + A_w).
```

Compute all endpoint distances and comparisons exactly. Merely intersecting
a tolerance interval, comparing interval midpoints, or observing Decimal
agreement is insufficient. The difference tolerance is the sum of the two
fixed output tolerances, not a relative tolerance divided by a possibly tiny
context effect. Keep each production value unchanged; it need not lie inside
the much narrower exact-operator interval. These proofs concern these inputs
and eight coordinates only. They establish no uniform production-roundoff
bound over an extension box, other data or the whole 2769-row profile.

## 5. Later implementation, controls and evidence

After independent design acceptance, reserve a separate fixed-input driver
and report/guide paths. Freeze their source and closure before any new observed
access. Reuse the published engine and filter; do not edit their accepted
sources or replace the independent oracle. A successful current receipt and
the sixteen reconciled certificates admit coefficient use, not unreviewed new
indexing, interval reductions or export logic. Those require their own review
and synthetic controls. No new runtime installation is part of this design.

The later checks must include the following, in ordinary and optimized modes:

- Synthetic indexed arrays `X[k]=k/2^20` and its negative, each of length
  131072, proving every original/central/extended/crop index, both context-block
  orders and the exact identity w=Ex+Uz. Repeat with signed zeros at indices
  61440, 65536 and 68305. Preserve signed
  zeros in exported source and production arrays; rational arithmetic may
  correctly identify both signs with zero.
- Independent exact small-system forward/basis checks using all eight published
  oracle configurations at central lengths 4,7 and side lengths 1,2. Test every
  row with `x[j]=(j-2)/8`, `z[k]=(-1)^k*(k+1)/16`, then repeat with zero center,
  zero context and both zero. Check the signed interval reductions and
  known-context decomposition with exact point rows and with coordinate radii
  `((j mod 3)+1)/1024`. These broad synthetic intervals test containment, not
  actual-width admission. Check endpoint-distance gates separately: the point
  `1+2^-40` and exact interval [1,1] pass a 1e-9 limit although the point lies
  outside the interval; `1+2^-20` fails it. Unequal radii and input signs must
  not be collapsed into an unjustified common or signed-canceling bound.
- Controls rejecting an interval that misses a known exact toy value, reversed
  endpoints, an overwide valid interval, a missed numerical threshold, and a
  midpoint/overlap-only claim incorrectly presented as the endpoint bound.
- Explicit pre-observation refusals for changed/missing dependencies, changed
  coefficients/order/padding, failed or stale receipts, incompatible runtime,
  unreconciled certificates and exhausted arithmetic/resource bounds.
- Missing, swapped, truncated and same-size-corrupted original files; any
  mismatch must reject before HDF5 parsing. Reject wrong grids, nonfinite or
  DATA-inconsistent samples, altered flags/annotations, one-sample index shifts,
  modified RI-47 sample identities and an already existing output destination.

Use a new exclusive output leaf outside Git checkouts. Write no accepted output
until every check passes, retain stderr/nonzero failures without a success
record, and refuse overwrite. Record actual commands and execution modes
externally. Compare complete report/export bytes across normal and optimized
runs; their scientific content must be deterministic and exclude changing
paths, timestamps and elapsed times. Resource or qualification failure is a
reported result, not permission to refresh a pin or silently change the design.

The export must bind both raw-file identities, complete original annotations,
the unchanged RI-47 export, dependency/receipt/driver identities and runtime.
Retain exact source indices and clocks; canonical finite input/output hex
arrays with C-order little-endian binary64 hashes; exact rational nominal
differences; all full-vector residuals/peaks/gates; and all sixteen selected-row
results (eight per detector) with coefficient/certificate identities, direct Delta and
short/long intervals, widths and endpoint-distance checks. Summary maxima may
not replace the complete values or imply unexamined-row certificates.

An independent export audit must reconcile every slice and retained value
against the admitted snapshots and existing crop, every exported rational
reduction and gate, both modes and all provenance. Identities alone cannot
recompute a dot product whose coefficient arrays were not exported. In that
case state explicitly that those dots rely on the reviewed source and reproduced
engine executions; claim independent dot-product verification only if the
coefficient intervals and input values were actually replayed by a separately
implemented reducer. Distinguish export reconciliation from an independent
filter computation. Any later figure requires a separately
reviewed export-only renderer and source reservation: all points, original time
coordinates, unchanged amplitudes, readable detector/context labels and the L1
warning. No figure or renderer is assigned by this note.

## 6. Availability and interpretation

A metadata-only inventory at design handoff found the two expected filenames
in the coordinator's external RI-37 `det-ri37-gwosc-zdmry2a0/inputs` directory,
with the byte counts listed above. No sample body was opened or hashed for this
inventory. There is no current file-availability blocker, but this temporary
location is not durable custody and file existence is not identity verification.
Later execution must repeat full admission; missing or altered bytes stop it.
No new acquisition or replacement dataset is authorized here.

The [RI-40 calibration qualification](../gwosc_calibration_qualification_v1/QUALIFICATION.md)
supplies nearby pointwise statistical summaries, not a joint temporal/frequency
law or deterministic envelope. This packet applies no further correction and
makes no calibrated amplitude, phase, arrival-time or confidence claim. The
[RI-53 comparison](../gwosc_nr_comparison_v1/COMPARISON.md) remains illustrative:
observed surroundings here cannot be substituted as the NR signal's missing
physical continuation, and its historical V1-to-V2 placement is not resolved.

The result sought is source-bound finite processing sensitivity for nominal
public observations. It is neither a new detection nor a withheld prediction,
fit, native detector forward map, DET-versus-GR test or gravity proof. Public
source attribution and the [GW150914 release DOI](https://doi.org/10.7935/K5MW2F23)
remain attached. RI-63's native assignment proceeds separately; RET remains
paused. This note's tests and outputs are prospective, not reported passes.
