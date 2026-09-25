# RI-100 — direct mode-weighted selected-output trace

25 September 2026 UTC. Root accepts this fixed saved-input result after both
actual application modes and the separately authored arithmetic audit passed,
with independent review of all three executions. The complete [result](RESULT.json),
[audit report](AUDIT_REPORT.json), [auditor](audit_saved_result.py) and
[source contract](AUDIT_CONTRACT.md) are published unchanged.

Direct weighting reduces the four conditional trace-interval widths by about
3.73e56–3.84e57 relative to RI-96. This removes enormous conservatism from the
earlier band bounds for this scalar quantity. It establishes precise numerical
bounds within the fixed covariance model. Whether that model accurately
represents the detector noise remains unestablished.

## Result and scientific meaning

The [RI-97 design](../gwosc_mode_weighted_trace_v1/DESIGN.md) and
[RI-98 qualified implementation](../gwosc_mode_weighted_trace_check_v1/IMPLEMENTATION.md)
stay fixed. The sole upstream numerical input is the complete accepted
[RI-96 result](../gwosc_frequency_resolved_proxy_result_v1/RESULT.json).
There is no new transform, acquisition, PSD estimate, bin selection, precision
choice or covariance model. The same eight selected output rows and four
H1/L1 left/right scenarios apply.

For the fixed long-minus-short processing operator B and hypothetical input
covariance K_s, the scalar is
`t_s = E ||d - E d||^2 = tr(B K_s B^T)`, with `d=B x`.
It sums centered discrepancy variance over eight selected coordinates. It is
not an observed residual score, an average, a result for all 2769 outputs, or
uncentered energy without a mean premise. Nominal units are input strain
squared under the inherited publisher interpretation; calibration limits remain.

The actual exact final intervals are `[C-E,C+E]`, where
`E=E_tau+E_alpha`. Every raw/final lower endpoint is positive, every one of the
20 ratio fields is defined, and the prior scalar intersection leaves the raw
interval unchanged. No negative endpoint or undefined ratio was replaced.

The table displays magnitudes to nine significant digits. These are not
outward-rounded decimal endpoints: rounding C discards far more digits than
the tiny enclosure width. The saved rational C and E specify the interval;
printed C and width must not be treated as a newly certified decimal interval.

| Scenario | Center C, nominal strain squared | Final width 2E | RI-96 width / final width |
|---|---:|---:|---:|
| H1:left | 4.93063411e-41 | 1.95084939e-95 | 4.36207640e56 |
| H1:right | 5.33187959e-41 | 2.26064422e-95 | 3.73039057e56 |
| L1:left | 1.61625235e-40 | 2.94611833e-95 | 3.84169274e57 |
| L1:right | 1.61879600e-40 | 3.14655541e-95 | 3.33579886e57 |

| Scenario | Transform-only E_tau | Coefficient-added E_alpha |
|---|---:|---:|
| H1:left | 3.00664864e-111 | 9.75424696e-96 |
| H1:right | 3.15388067e-111 | 1.13032211e-95 |
| L1:left | 4.43104899e-111 | 1.47305916e-95 |
| L1:right | 4.73126205e-111 | 1.57327771e-95 |

Coefficient enclosure dominates the remaining deterministic error by roughly
3.24e15–3.58e15. That term includes coefficient/transform cross terms; the
split is not between independent statistical uncertainties. Direct mode
weighting removes coarse spectral-band slack while preserving the same PSD
bins and true DC-annihilation premise. Nyquist has its real-only singleton
weight. No source DC/Parseval evidence is overwritten.

This result answers the numerical-width question: the fixed proxy scalar can
now be bounded very tightly. It does not quantify empirical PSD uncertainty,
nonstationarity, calibration error or covariance-model error, and it cannot
rank those unquantified physical uncertainties against each other. Large
width-reduction factors do not describe improved detector accuracy or
statistical significance.

## Independent arithmetic and actual execution

Normal and optimized workers each saved and reloaded the full result, then
passed the complete separately authored product-form validator. Their complete
8,844,567-byte results are identical. All eleven declared application gates pass.

The independent auditor imports neither the producer nor its validator. For
Q256 endpoints l,u it accumulates integer numerators `(l+u)^2` and
`(u-l)(2|l+u|+u-l)` before dividing by `(2Q)^2`; the separate alpha term
retains all cross terms. This differs from both the producer's Fraction
expansion and the validator's successive square differences. Complete source
and contract reviews preceded execution.

The actual auditor reconstructs all 8192 modes and 24576 scalar entries,
visits all 65544 retained rectangles and 131064 active real components,
checks all 32772 PSD bins/eigenvalues, 56 extrema and 20 ratio states, and
reconstructs the whole ten-section canonical result. All four complete
reconstructed scenario bodies and section identities agree with the actual
result. RI-96 transform/row validity and the covariance premise are inherited;
this audit does not claim another FFT or physical-noise validation.

| Execution | Child seconds | Peak sampled sole-child KiB | Raw observations | Genuine outer completion |
|---|---:|---:|---:|---|
| Normal application | 24.73833041600301 | 231792 | 700 | d392a2, exit 0 |
| Optimized application | 24.783851250002044 | 235728 | 705 | c55bf3, exit 0 |
| Independent arithmetic audit | 10.442295417000423 | 288160 | 295 | 9632f9, exit 0 |

All 1700 raw observations reconcile independently. The unchanged envelope is
180 child seconds, 524288 KiB sampled sole-child RSS, 0.025-second target
polling, 0.1-second maximum/final gaps and 0.05-second ps timeout. This is
sampled RSS, not a hard OS/process-group cap. The audit maximum gap is
0.03924904199811863 seconds and its final gap is 0.03508320899709361 seconds.
The raw records do not separately encode ps-call duration; the reviewed
timeout implementation and genuine custody support that guard.

The qualified recovered CPython 3.11.6 runtime, literal interpreter links,
all 3925 runtime files and full source/input closures match before and after.
The audit binds 105 source/helper observations and the original completed
producer evidence. A separate reviewer independently reconstructs the final
4143-file stat/hash custody map. The audit's exclusive report and separate
stdout are byte-identical. All three successful stderr streams are empty.

The adapter preserves the qualified monitor and cleanup. Its new input and
report bindings received root and two complete independent source reviews;
root then issued a status-only immutable freeze and separate normal-only
authorization. No audit retry, threshold relaxation or broad execution occurred.
The unchanged source contract describes preparation at its historical date;
this review records later genuine execution and acceptance. Historical
`arithmetic_accepted=false` in the pre-audit custody bridge is preserved.

## Exact files and retained evidence

| Published file | Bytes | SHA-256 |
|---|---:|---|
| RESULT.json | 8844567 | 37dc6865be52e6888bcf325022a18cef65e5b3dd8bf1ba2a9f287e1c12d929dc |
| AUDIT_REPORT.json | 79442 | a6d0ea5592a9716f053322904effc6aa64945ac1e3d6e9d9e4dd7d31e438f03d |
| audit_saved_result.py | 55394 | 843f52ab0c26e28152987b228e7ca4d88fe668a0d95e6d14b947037a914f32e3 |
| AUDIT_CONTRACT.md | 17182 | ee29ef111aae2e6c9c28bbf24e2895e4c5d6d504e500268c5798419f9e4cd372 |

The upstream RI-96 result is 41,673,703 bytes, SHA256
`5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580`.
Original machine-specific evidence remains under
`/Volumes/AI_DATA/development/det-review-evidence/`:

- `ri100-execution/application-preparation-uhq7i_49/`: immutable source/input
  closure, freeze, original normal/optimized outputs and complete receipts.
- `ri100-root-execution-o0ys80jh/`: genuine producer admissions/completions,
  completed custody bridge and independent scientific-source acceptance.
- `ri100-independent-saved-audit-tujq6qh2/`: original auditor, historical
  preparation contract and retained source-review corrections.
- `ri100-saved-audit-execution-8dv7l7vg/`: original adapter, descriptor,
  reviewed predecessor deltas, source-only template, issued freeze and outputs.
- `ri100-independent-completed-audit-sxs6kzm1/INDEPENDENT_COMPLETED_AUDIT_REVIEW.json`:
  6964 bytes, `44e7a50627b428c53e2333033246c31eb6ea254b420b1599de8b709008d165b4`.
- `ri102-ri100-root-review-hnltxouk/RI100_ROOT_FINAL_ADJUDICATION.json`:
  7451 bytes, `499fddd1a5315fb8c14c39ae8d161ab11e12f53f8f640d814b1ed81e2f780d21`.
- `ri100-saved-scalar-interpretation-stlxp3yb/FORMAT_RECORD.json`:
  75782 bytes, `d79346e5e7f5b4ae3710d5de020cfe66a11e363aa47e1498f58ced8e0fb340c4`.
  Exact source fields and decimal formatting are retained; root separately
  checked the displayed saved rationals without replaying scientific targets.

The auditor author wrote neither the RI-98 primary, product validator nor
qualifier; related design and earlier-auditor authorships are disclosed in the
contract. The completed-execution reviewer authored the primary/qualifier but
neither this auditor nor its adapter. That review independently checks custody
and output binding, rather than claiming a further arithmetic implementation.

Published source bytes equal those executed at their original external path.
The historical descriptor binds that path and genuine custody. Replaying a
published copy requires a newly reviewed concrete path/closure and fresh
admission with unchanged gates; a copied receipt supplies no authorization.

## Next measurement step and remaining premises

RI-104 designs an observed off-event context-discrepancy benchmark using the
existing thirteen windows per detector and original raw inputs. It must fix
the segment-to-operator index map, eight selected coordinates and side
centering, then specify a descriptive comparison with these four proxy traces.
Overlapping windows, prior access and an unknown population mean must remain
explicit. Source review, qualification and separate actual admission precede
execution. This is a direct observed-data question, with no new enclosure
refinement needed merely to improve this scalar's deterministic width.

Finite four-second circulant wraparound, population covariance, PSD error,
stationarity, detector dependence and mean/template adequacy remain unproved.
Public V2/C02 provenance, blank literal Yunits, the clear L1 NO_CW_HW_INJ flag
and unresolved calibration meaning below 10 Hz are retained. The accessed
32-second inputs remain development/calibration evidence. No protected
validation, calibrated significance, whitening, SNR, p-value, native forward
map or geometry/gravity measurement follows. RET alone remains paused.
