# RI-96 — saved public-data frequency-resolved covariance bounds

25 September 2026 UTC. Root accepts this fixed saved-input calculation:
both application modes passed full saved validation and produced identical
bytes; a separately written arithmetic auditor and independent reviews of
all three executions also passed. The [exact result](RESULT.json) and
[audit report](AUDIT_REPORT.json) are published unchanged.

The fourteen fixed frequency bands reduce the width of the four proxy trace
intervals by approximately 203–4455 times relative to RI-90's global envelope.
The resulting intervals remain very broad. This is a useful reduction in
mathematical conservatism under the same postulated finite covariance model;
it is not evidence that the model represents detector noise accurately.

## Result and interpretation

The [accepted design](../gwosc_frequency_resolved_proxy_v1/DESIGN.md) and
[qualified implementation](../gwosc_frequency_resolved_proxy_implementation_v1/IMPLEMENTATION.md)
are unchanged. The inputs are RI-73's saved compact operator intervals and
RI-90's accepted Gram/PSD result. There is no new strain acquisition, FFT
recipe selection, bin exclusion, PSD floor or adaptive precision choice.
The same eight selected operator rows and four H1/L1 left/right spectra apply.

For each band, exact midpoint/error matrices C/H bound the real output Gram
contribution. The scenario's spectral extrema weight C/H before taking the
maximum absolute row-sum error margin. The resulting matrix endpoints apply
in Loewner order. The report also retains the old global endpoints. Diagonal
and trace intervals may be intersected as scalar bounds; entrywise matrix
intersection is not a valid Loewner operation and is not performed.

The trace measures the sum of the eight selected output variances under the
postulated proxy. It is neither an observed residual score nor a calibrated
physical observable. Approximate decimal summaries of the exact rational
trace bounds are:

| Scenario | Trace lower | Trace upper | Upper/lower ratio | Reduction in interval width |
|---|---:|---:|---:|---:|
| H1:left | 3.933191e-44 | 8.509793e-39 | 216358.50 | 4454.6225 |
| H1:right | 5.404406e-44 | 8.433140e-39 | 156041.94 | 4051.9202 |
| L1:left | 1.881600e-43 | 1.131810e-37 | 601514.84 | 202.6633 |
| L1:right | 2.916711e-43 | 1.049631e-37 | 359867.83 | 421.7197 |

The reduction is `(global_upper-global_lower)/(band_upper-band_lower)`,
not a ratio of standard deviations, an accuracy measure or a significance
improvement. In every scenario the trace intersection equals the band trace
interval exactly. All 32 diagonal intersections and four trace intersections
have positive lower bounds. The diagonal upper/lower ratios span approximately
14803.76 to 22384399.96. Numerical success therefore does not establish a
practically precise covariance estimate or a covariance adequacy test.

All 8193 PSD bins per scenario remain authenticated and converted to exact
dyadic values, with eigenvalues fs*PSD at endpoints and fs*PSD/2 internally.
The true operator's DC action is excluded only under the accepted A1=0
premise. The midpoint transform's real DC term remains in its Parseval check;
DC and Nyquist imaginary endpoints and errors are exactly zero. The fourteen
non-DC bands retain their fixed boundaries, including singleton Nyquist.
Below-10-Hz values remain present without acquiring a calibrated interpretation.

## What was independently checked

The actual application workers called the fixed consumer, serialized its whole
result, released the producer object, reloaded the saved bytes and ran the
complete recursive validator. Normal and optimized modes each validated eight
rows, 65544 one-sided rectangles, fourteen bands and four scenarios.

The separately authored [auditor](audit_saved_result.py) imports neither the
producer nor its validator. It independently reads the delimiter-framed compact
snapshot, reconstructs all 109840 source intervals and 87688 initial coordinates,
row midpoint/radius/quantization information and uncertainty contributions,
and checks all 65544 saved rectangles structurally. Its direct
product-of-magnitudes error bound is a separate arithmetic route. It reconstructs
all 896 band C and 896 band H entries, the DC-inclusive midpoint Parseval check,
32772 PSD values/eigenvalues, every spectral extremum and tie, scenario-weighted
matrices/margins, 1024 band/global endpoint entries, and all 36 scalar
intersections and conditional ratios. Every declared rebuilt field agrees exactly.

The recursive Fourier root isolation, twiddle construction, butterflies and
validity of the saved transform enclosures remain an explicit inherited premise:
the qualified independent validator actually replayed them in both application
modes. This saved-result auditor does not claim a third independent FFT.
RI-73 interval validity, the accepted Gram/rho certificate, constant annihilation
and the RI-92 Loewner theorem likewise retain their stated predecessor premises.
The [audit contract](AUDIT_CONTRACT.md) is the unchanged source-preparation
contract; this result note records the subsequent actual execution and acceptance.

## Actual execution and custody

The admitted recovered CPython 3.11.6 runtime, all 3925 runtime files, literal
interpreter links, scientific input identities and complete source closures
were checked before and after. Both application modes used the same frozen
inputs and unchanged qualification. The actual audit used a separately
reviewed adaptation of the genuinely completed RI-90 audit supervisor.

| Execution | Child seconds | Peak sampled KiB | Raw observations | Genuine outer completion |
|---|---:|---:|---:|---|
| Normal application | 68.26647300000332 | 304816 | 2144 | ab3417, exit 0 |
| Optimized application | 68.67150933299854 | 310432 | 2152 | 40d2fe, exit 0 |
| Independent arithmetic audit | 12.065320083005645 | 328608 | 340 | fe6238, exit 0 |

All 4636 raw observations reconcile independently. The fixed envelope is
180 active-child seconds, 524288 KiB sampled sole-child RSS, 0.025-second target
polling, 0.1-second maximum/final gaps and a 0.05-second ps timeout. This is not
an OS allocation cap or a process-group aggregate. The audit's maximum gap is
0.03907016599987401 seconds and final gap 0.03509320800367277 seconds. All three
successful stderr streams are empty; genuine outer exits, worker exits,
source/runtime stability and output identities agree.

Before audit execution an independent source reviewer found an inherited
premise label naming RI-96 instead of RI-90. The single literal was corrected,
the old packet preserved and final pins reviewed before authorization. This
was a source-preparation repair, not a failed scientific run or relaxed gate.
The auditor also checked the entire 4085-file final custody map; independent
completed-execution review reconstructed its exact byte identity separately.

## Exact files and reproducibility evidence

| Published file | Bytes | SHA-256 |
|---|---:|---|
| RESULT.json | 41673703 | 5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580 |
| AUDIT_REPORT.json | 108637 | 943a9d88eddb66ea6f7cba6070d7b937a182b24491a9877c11a5b5fbdd1702d6 |
| audit_saved_result.py | 49063 | 77bae781685fe0c42bbc1e7ff112399ae2aeecdd213db05a5373d4afb4d8c224 |
| AUDIT_CONTRACT.md | 11765 | 997606b1acb0ebd6fc3e4c2b7ecd8cb068d6b3a2d337b54f03c10654d3222132 |

The compact snapshot is 51891508 bytes at
`fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba`;
[RI-90's result](../gwosc_colored_covariance_proxy_result_v1/RESULT.json) is
6994965 bytes at
`c3a90d4d4516cce5309e47ec0b276455a515dcd3a67c749fa6c2500a2d9af3bf`.
Machine-specific evidence is retained under
`/Volumes/AI_DATA/development/det-review-evidence/`:

- `ri96-execution/application-preparation-wvp1hizx/`: exact application closure,
  inputs, freezes, both results, runtime receipts and raw samples.
- `ri96-application-checkpoint-3cg5f8gf/`: root admissions, genuine application
  completions, full-byte equality, source review, descriptor and custody bridge.
- `ri96-saved-audit-execution/preparation-ex2gupks/`: preserved earlier source
  packet, final reviewed caller adaptation, authorization and actual audit.
- `ri96-independent-completed-audit-review-fo3q2x5f/INDEPENDENT_COMPLETED_AUDIT_REVIEW.json`:
  11453 bytes, `21dfdf8472fe8ed9c79ccb600f0608d7183f30cb619b54143fe06850e63bf9be`.
  The reviewer authored the producer, not the auditor/runner; this is an
  independent execution-custody review, not another arithmetic implementation.
- `ri96-result-checkpoint-m4z2kzhh/RI96_ROOT_RESULT_ADJUDICATION.json`:
  6551 bytes, `c7842d05fa0d34dddf60d5b3963abb0dbbcae6090ebfcc28af7ca525f61cc836`.
  The root decision binds source reviews, actual modes, independent audit,
  its own reviewed execution and remaining premises.

The exact auditor takes a concrete authenticated descriptor, byte count and
SHA-256 as described in its contract. Published source bytes are identical
to those executed at their original external path. The historical descriptor
binds that original path, runtime and actual custody; moving a source file or
copying a success receipt is not a new execution authorization. A replay needs
its own concrete path/closure review and fresh admission with unchanged gates.

## Remaining scientific work

The four-second circulant proxy, long-lag wraparound and empirical PSD values
remain model choices. Population covariance, PSD estimation uncertainty,
stationarity, detector dependence and mean/template adequacy remain unproved.
Nominal public V2/C02 provenance, blank literal Yunits, prior public access and
the clear L1 NO_CW_HW_INJ flag remain recorded. These already used 32-second
inputs are development/calibration material, not independent held-out evidence.
No covariance inverse, whitening, SNR, p-value, calibrated significance, native
observation map or geometry/gravity test follows. RET remains paused.

The next bounded measurement question is whether direct mode-weighted bounds
on the selected-output trace can separate coarse-band conservatism from
transform-enclosure slack. It can be designed using the already retained
rectangles and PSDs without new data or a new transform; any implementation,
qualification and actual application require their own review. RI-96 stays
fixed. The independent native-law amplitude decision proceeds in parallel.
