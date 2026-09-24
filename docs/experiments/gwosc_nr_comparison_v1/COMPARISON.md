# RI-53 — illustrative H1 comparison with a supplied NR reference

24 September 2026 UTC. **Independently accepted numerical comparison and
illustrative display.** The prospective contract below was frozen before actual
processing. The final section records source review, actual isolated replays,
independent export reconciliation and visual inspection. The coordinator owns
acceptance and publication; the wider native programme remains open.

The accepted [RI-50 contract](../gwosc_nr_reference_v1/QUALIFICATION.md) fixes
this comparison. The supplied scalar SXS:BBH:0305 waveform has publisher-adjusted
amplitude and phase informed by GW150914 observations. It is neither a withheld
prediction nor a new parameter fit. Its time coordinates are printed seconds
relative to its supplied peak convention. The [RI-47 H1 observations](../gwosc_nominal_result_v1/DISPLAY.md)
remain exactly as published; both original detector exports and their complete
quality/injection annotations remain preserved.

## Qualification and numerical processing boundary

[qualify.py](qualify.py) must first qualify the actual reference length, 2769,
using the published [RI-44 production filter and independently authored Decimal reference](../gwosc_nominal_processing_v1/PROCESSING.md).
The frozen synthetic fixtures are zeros, ones and unit impulses at indices
0, 1384 and 2768. Compare every output sample, including boundaries, against
the unrounded 80-digit Decimal recurrence. The prospective criterion is
`max error <= 1e-9 * max(1,maxabs(input))`; additionally require exact zero
output for the zero input. Failure stops admission without a changed threshold.

After that qualification, [process.py](process.py) may bind the complete public
reference bytes and accepted source/report/coefficient identities, convert each
retained decimal strain token once to binary64, and apply the 17 admitted stages
in their original order. Its additional whole-array actual-reference audit must
meet `max error <= 1e-9 * maxabs(input)` against the unrounded Decimal result.
The actual input must be nonzero. This scale-relative comparison prevents the
tiny physical strain values from passing a unit-scale tolerance trivially; it
does not rescale the produced waveform or establish physical uncertainty.

The Decimal reference was authored without reading the production implementation.
Subsequent reviewers have inspected both sources; independent authorship is not
a claim that every later reviewer remained unaware of the production code.

The numerical runtime is the admitted CPython 3.11.6 / NumPy 2.1.3 / SciPy
1.14.1 / h5py 3.12.1 environment. The admitted coefficient manifest SHA-256 is
`700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0`.
Filtering acts on the nominal 4096 Hz index clock, with separate odd padding
and forward/backward passes at each stage. It introduces no mean removal,
taper, extra correction, normalization, sign inversion or fitted parameter.

All 2769 reference samples must be filtered and retained in `REFERENCE.json`
before display selection. The export preserves every source time/strain token,
exact represented rational value, index and original line number, as well as
each input/output binary64 hexadecimal value and complete array identities.
It also retains an exact copy of the accepted H1 entry and observation grid.
The numerical processing report must bind the resulting reference export's
complete byte count and SHA-256 for subsequent reviewed rendering.

These are numerical finite-array checks. Odd extension is an algorithmic
boundary condition, not supplied physical continuation. The shorter reference
and the 32-second observation have different input contexts; passing these
checks does not measure endpoint contamination or calibrated agreement.

## Export-only rendering and fixed placement

[render.py](render.py) consumes only the accepted `CROP.json` and the new
`REFERENCE.json`. It loads no HDF5 input or original reference text and imports
no processing/filtering module. Before JSON parsing it checks both retained byte
snapshots: the observation is pinned to 395470 bytes and SHA-256
`a580481b9f6ea8dbb90242f12023817709ee7ac208d504110966f01f353592e7`;
the caller supplies the new reference identity from the independently reviewed
processing receipt. A caller-supplied digest establishes matching bytes, not
publisher provenance or proof that filtering was correct.

The renderer additionally validates both schemas, coefficient/source pins,
all 4096 sample indices per observed detector, finite canonical binary64 values,
little-endian array digests and the complete quality/injection annotation hashes.
It requires the embedded H1 entry and grid to equal the original export exactly.
For every reference row it checks lexical-to-rational time and strain values,
the indexed decimal-to-binary64 input, the finite filtered output, both array
identities and the exact declared placement. Extra provenance fields may be
retained but cannot override these core values.

Every H1 value is plotted unchanged at `j/4096`, `0 <= j < 4096`, seconds after
GPS `1126259462`. Every reference coordinate is formed first as

```text
Fraction(retained printed time) + 53/125
```

The renderer selects points with exact `0 <= placed_time < 1`, then converts
only those coordinates to binary64 for plotting. Selection uses no rounded GPS
comparison, interpolation or reconstructed uniform grid. It does not fit a
shift, invert a sign or change any numerical strain value. Ordinary polyline
connections between successive retained samples create no new exported sample
or resampled time series.

The fixed `53/125 = 0.424` second offset combines the historical tutorial's
`1126259462.422` event anchor and its extra 2 ms NR placement. That tutorial used
V1 data; V2 corrected a roughly 1 ms downsampling offset without specifying an
exact replacement NR alignment here. The chart therefore visibly labels the
placement as historical and illustrative, with precise V2 alignment unresolved.
The tutorial's L1 inversion and 28-sample shift are not part of this H1-only
comparison.

The supplied reference's placed support is approximately `[-0.196404109,
0.479377141]` seconds. Only its original points inside the one-second view are
shown. A dotted line and visible text mark its final supported sample; the rest
of the view has no supplied reference continuation. The plot also labels the
reference as data-informed and retains the H1 no-CW-flag annotation.

Both series use one common amplitude axis, spanning five percent beyond the
largest absolute value among all 4096 H1 points and all visible reference points.
The all-zero synthetic case uses `[-1,1]`. Nonfinite or unrepresentable limits
are refused. No values are numerically scaled before plotting; scientific tick
notation is axis formatting only. Path simplification is disabled, and every
selected point is supplied without amplitude clipping.

## Prospective reproduction and review

The renderer checks a separate CPython 3.11.6 / Matplotlib 3.11.1 / NumPy 2.4.6 /
Pillow 12.3.0 / FreeType 2.14.3 runtime. These are rendering dependencies, not a
replacement for the qualified filtering environment. Root selects the existing
environments; this packet installs or modifies neither environment.

After source review, successful numerical qualification, processing replay and
independent export reconciliation, use the reference identity from the reviewed
processing receipt:

```sh
/absolute/path/to/qualified-env/bin/python -I -B \
  docs/experiments/gwosc_nr_comparison_v1/qualify.py \
  > /absolute/path/to/qualification-normal.json
/absolute/path/to/qualified-env/bin/python -I -B \
  docs/experiments/gwosc_nr_comparison_v1/process.py \
  --qualification-report /absolute/path/to/qualification-normal.json \
  --expected-qualification-bytes 15544 \
  --expected-qualification-sha256 dab0822ae97639e16674bea6b059d4d67fae48dc725ce9c24576db0408339efe \
  --input /absolute/path/to/GW150914_4_NR_waveform.txt \
  --output-dir /absolute/path/to/new-normal-processing \
  > /absolute/path/to/process-normal.json
```

The qualification identity above is the coordinator-reported candidate receipt.
It must be reconciled with the frozen source and independently accepted before
actual processing. The processor's new output directory must be outside Git
checkouts; its parent must exist. It writes only `REFERENCE.json` and
`PROCESSING_REPORT.json`. The latter's `exported_reference_file` supplies the
byte count and SHA-256 used below; the stdout identity summary also exposes them
as `outputs['REFERENCE.json']`. Review those processing outputs independently;
do not obtain authority merely by hashing an arbitrary export.

```sh
/absolute/path/to/render-env/bin/python -I -B \
  docs/experiments/gwosc_nr_comparison_v1/render.py \
  --crop /absolute/path/to/accepted/CROP.json \
  --reference /absolute/path/to/REFERENCE.json \
  --expected-reference-bytes REFERENCE_BYTE_COUNT \
  --expected-reference-sha256 REFERENCE_SHA256 \
  --output /absolute/path/to/new-normal.png \
  > /absolute/path/to/render-normal.json
```

Repeat each operation with `-O` and different new report/output paths, retaining
failed attempts as well as successful ones. PNG destinations must be
outside Git checkouts, with existing parent directories. Exclusive creation
refuses overwrites. Invalid exports are refused before PNG creation; successful
stdout records both input identities, renderer and PNG identities, runtime,
selected reference indices and exact support, H1 identity and shared limits.
Record actual commands/modes externally, compare full PNG and JSON bytes across
modes, then visually inspect the figure. The shell owns stdout redirection and
does not itself prevent overwriting a redirected record.

The Agg PNG uses fixed dimensions, layout, font and text metadata without an
embedded timestamp or path. Matplotlib defaults are reset within a temporary
configuration scope; its font cache lives outside the checkout. A font-cache
progress message on stderr may accompany success. Byte reproducibility must be
checked in the recorded runtime; no cross-platform rasterization identity is
promised.

Synthetic renderer checks may use explicitly mocked identity constants in an
external test harness, with no change to production pins or accepted data.
They should cover exact boundary selection, signed zeros, shared limits, changed
annotation/grid/sample/identity refusals and output overwrite protection.
Such mocks are not acquisition, processing qualification or an observed result.
Actual source/output acceptance and visual evidence belong to the coordinator.

The chart supplies no residual score, whitening, matched-filter statistic,
significance, confidence region, calibrated agreement, new arrival estimate or
DET-versus-GR inference. It uses the public [GW150914 release](https://doi.org/10.7935/K5MW2F23),
the event page's SXS attribution and [GWOSC acknowledgement](https://gwosc.org/data/).
Native forward-law obligations and the RET pause remain unchanged.


## Accepted actual execution and evidence

The complete qualifier and processor passed root and independent source review.
The complete renderer also passed root and independent source review. The final
renderer delta moved the legend outside the data area; no numerical contract,
threshold, accepted dependency or supplied sample changed. All execution used
external copies with the complete pinned published dependency closure.

In the admitted numerical environment, normal and optimized `-I -B` qualifier
runs both exited zero with empty stderr. All five full-length fixtures passed;
zero input gave exact zero in both implementations. The largest synthetic
maximum absolute error was approximately `3.6860685767e-14` (last impulse),
below `1e-9`. Both qualification outputs are identical, 15544 bytes, SHA-256
`dab0822ae97639e16674bea6b059d4d67fae48dc725ce9c24576db0408339efe`.
The author's separate synthetic/mock consumer suite passed 42 checks per mode,
with identical 4573-byte output SHA-256
`fe7c3ae70922f5345a314134d62169df1087b66255b417a6c5038810f203e981`.
Those mock checks are not actual public-data evidence.

Both actual processor runs exited zero with empty stderr and produced identical
complete exports. Their 359-byte stdout SHA-256 is
`d9ad1e9d8270adbe16cc1004438162d0a18d7c7d2450dc8d3d4ed6b8474122bd`.
All 2769 actual output samples were compared against the 80-digit recurrence,
using exact rational differences and threshold comparison. The maximum error
was approximately `7.4148812451e-35`, at index 2001, below the unchanged
input-peak-relative threshold `1.2263698655e-30`. There is no unit floor in
this actual gate. Exact error, peak, threshold, reference worst-sample value
and array digests are retained in [PROCESSING_REPORT.json](PROCESSING_REPORT.json).
The human-readable Decimal summaries do not decide the gate.

A separate audit without production imports or refiltering reconciled all
2769 full export rows and 5538 raw decimal values against the retained public
body and accepted RI-50 report, every binary64 input conversion, both complete
22152-byte array hashes, every exact placed time, all source/runtime and
qualification bindings, and the complete unchanged H1/grid. It also checked
the reported worst sample and exact threshold. The full Decimal vector is not
exported: this independent audit does **not** recompute the global maximum.
The root actual executions supply the complete-array comparison. Independent
export-audit JSON is 2995 bytes, SHA-256
`549e6e8b459de1d395e6b0a876c7e986bb854d43b7b7a7331dba91450f9e670b`.

Both actual rendering runs exited zero in the separate declared rendering
runtime. Stderr contained only the expected font-cache progress message.
Their identical 11854-byte receipt has SHA-256
`2e8bbdf1c45e6fe049b96598d474f62603ba89ceea56cb78cc0cb633a8449215`;
PNG bytes are identical across modes. Root visually inspected the actual
1200-by-700 image: the two series, scientific strain axis, outside legend,
historical placement/provenance labels and finite-support endpoint are readable
and unclipped. All 4096 H1 values remain unchanged. Exactly 1964 reference
samples (indices 805 through 2768) are visible. Their exact first and last
coordinates are `645470625000093/5000000000000000000` and
`2396885705000000093/5000000000000000000`; the full shifted support begins at
`-982020544999999907/5000000000000000000`. Shared limits are
`[-0x1.844a9d52ce747p-70, 0x1.844a9d52ce747p-70]`.

The renderer author's separate synthetic suite passed six positive checks and
27 refusal controls per mode. Its identical 11854-byte JSON SHA-256 is
`3269365008dc98f0b2faeed44d6aa743dd2f10b4bcf20c8410969cdd54489893`;
synthetic PNG SHA-256 is
`c82aa8b248187bed8c32353c51305f06aa03f815884fd1bd01224aebfdfb4bd2`.
These use explicitly mocked identity constants outside the checkout and are
separate from the actual outputs above.

Accepted source and artifact identities:

| File | Bytes | SHA-256 |
|---|---:|---|
| [qualify.py](qualify.py) | 13916 | `e0d63265d812a02a2524c1f8f9a712465a45afec165859567859b4a5d5802823` |
| [process.py](process.py) | 14909 | `374ff49a09c37aca4337631a275cef11a36e124e4bf56e2cdcb6c0d7988e34d4` |
| [render.py](render.py) | 17944 | `9f4f5ac4f72ed9ab9e638453781f5fb3e27b7d2663036fca4a862d0c3c9301fc` |
| [QUALIFICATION_REPORT.json](QUALIFICATION_REPORT.json) | 15544 | `dab0822ae97639e16674bea6b059d4d67fae48dc725ce9c24576db0408339efe` |
| [REFERENCE.json](REFERENCE.json) | 1633767 | `24c291c9f4f160fe3cb7ca75926ccbed2ba1fe1559f8badc130f3d14dc3e407d` |
| [PROCESSING_REPORT.json](PROCESSING_REPORT.json) | 28405 | `6e3e2f85c2d05274e9919921b56be8a53bef41f01a81b1039e490925c4a3bb4f` |
| [COMPARISON.png](COMPARISON.png) | 135519 | `c650b63950ceb415a57bd2d97b81fe2a956b1993bec5ceeeebbd60731bc93ade` |

All prior accepted artifacts remain fixed. The new reference input array SHA-256
is `e34926cba71051771bdea7a75f26ac207dc45c59a16c9142edacc0b154efc52f`;
filtered array SHA-256 is
`7cdadbf91b4ce88b66830a1c33d766b555728cdecb952c430175691c5ca845a6`.
Full commands, stdout/stderr and acquisition bodies remain in external audit
storage; the public inputs and recorded environments are needed for replay.

Remaining premises are physical boundary continuation, exact V1-to-V2 alignment,
a calibrated statistical comparison, and a native observable forward law.
This accepted display supplies none of them. No residual score or detection
claim is inferred from the visual resemblance.
