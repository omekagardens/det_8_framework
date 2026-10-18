# RI-83 — accepted descriptive spectra of the public GW150914 V2 pair

25 September 2026 UTC. **Accepted for scoped descriptive publication.**
[RESULT.json](RESULT.json) is the unchanged canonical scientific stdout: **38,952,074 bytes**, SHA-256
`e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f`.
It retains four detector/side PSDs and ASDs, all 26 segment periodograms,
conventional reference spectra, the complete frequency/window arrays and metadata.
This is the finite statistic defined by [RI-78](../gwosc_off_event_spectra_v1/DESIGN.md),
implemented and qualified in [RI-80](../gwosc_off_event_spectra_implementation_v1/IMPLEMENTATION.md)
and applied through the unchanged [RI-83 caller contract](EXECUTION.md).

## Fixed output and input scope

The released nominal H1 and L1 V2 strains use fs=4096 Hz, M=16384 samples,
8192-sample stride, demeaning before a periodic Hann window and arithmetic
mean periodograms. ASD is the square root of mean PSD. All 8193 bins k/4 Hz
from DC through 2048 Hz remain; detectors and sides are separate.
Each detector has seven left segments in [0,65536) and six right segments in
[69632,131072). The excluded interval is [65536,69632); the 4096-sample right
tail [126976,131072) remains unused. No selection was revised after execution.
The retained PSD integral is window-weighted demeaned power, not ordinary
unwindowed sample variance. Overlapping periodograms are not independent draws.

The original and retained snapshots match the already qualified public files:

| File | Bytes | SHA-256 |
|---|---:|---|
| H-H1_LOSC_4_V2-1126259446-32.hdf5 | 1040592 | `6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6` |
| L-L1_LOSC_4_V2-1126259446-32.hdf5 | 1007420 | `56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189` |

The blank literal `Yunits` attribute is retained; nominal strain units follow
the publisher interpretation. All 32 DQ/injection-mask rows remain. In L1,
`NO_CW_HW_INJ` is clear throughout; injection absence or negligible effect is
not established. “Off-event” describes only the fixed exclusion. These are
previously accessed public development data, with no blind-validation claim.

## Actual checks and execution

RI-80's numerical qualification used analytic identities, independent small
DFTs, scaling, whole-side Welch, aggregation and 37 intended refusals in both
interpreter modes. Its unchanged report is 63,464,716 bytes, SHA-256
`f247c20f9e112b48cc037d6256b47b5056ec354d58c0cf2817aad0363fc0fa0d`.
RI-83 fabricated integration then passed 33 intended refusals and ten positive
controls in both modes before the separately authorized observed execution.

| Actual observed mode | Worker wall seconds | Peak sampled RSS, KiB | Monitor samples |
|---|---:|---:|---:|
| normal | 4.126044042 | 259264 | 129 |
| optimized | 4.692322083 | 275696 | 147 |

Both genuine observed executions exited zero with empty stderr and identical
scientific bytes. Each retains 235 binary artifacts, complete input snapshots,
source/runtime custody and actual resource receipts. The 16-file dependency
closure, five observed helper files, qualified production window and recovered
CPython 3.11.6 / NumPy 2.1.3 / SciPy 1.14.1 / h5py 3.12.1 / HDF5 1.12.2
runtime were frozen and rechecked, including full runtime bytes and fingerprint.
The observed source, method, data, precision, thresholds and limits matched
the authorized freeze; prior qualification failures remain separately retained.

The separate saved-evidence consumer first passed 25 intended refusals and two
full positive controls in each mode. Its unchanged 40,246-byte source has SHA-256
`be6bae43b4d216de040ee5ee31c87ebade22e292a0cd1cff598ecc50ddda41ab`.
One authorized normal invocation then audited **both** real observed modes:
113 array records / 942191 values, 30 PSD comparisons / 245790 bins,
26 segments and four sides per mode. It reconstructed retained binary64 values,
all-bin residuals, window products, time/spectral Parseval, side means, ASDs,
metadata and custody under the declared budgets. It completed in 4.953141875 s
at 303536 KiB sampled RSS, with 153 monitor samples, zero exit and empty stderr.
The exact 3830-byte audit report and streamed stdout agree.

Independent final review rehashed 43 audit source bindings, 37 observed source
bindings, 3925 runtime files and all 480 saved outputs, including 470 binary
artifacts; it reconciled all 429 raw monitor samples and direct result-byte equality.
It reviewed actual custody and reports without rerunning the numerical consumer.
The accepted observed and saved-audit executions stayed within 180 s / 524288 KiB
sampled RSS and the fixed monitor gap limits. Sampled RSS may miss shorter peaks; it is not an OS hard memory cap.

## Durable acceptance evidence

All paths below are under `/Volumes/AI_DATA/development/det-review-evidence/`.
`E = ri83-execution/prep-20260925T001602Z-86696e9b/`;
`S = ri83-saved-audit-execution/prep-20260925T021546Z-c072584c/`;
`C = ri83-audit-controls-execution/prep-20260925T015457Z-7090db1b/`.
Each receipt binds its exact commands, outputs and full upstream dependencies.

| Relative evidence path | Bytes | SHA-256 |
|---|---:|---|
| E/FABRICATED_ADJUDICATION.json | 1812 | `34f837d8c52dc7dc71643ed68c09bb01d13af260f51ef426a3c10ffe1a997f8b` |
| E/observed/AUTHORIZED_FREEZE.json | 33360 | `da72f20717ec09f1ba1de843b82a2fa8da1f0d22f4a768ce00c29af9899db8bd` |
| C/ROOT_AUDIT_CONTROLS_ADJUDICATION.json | 8450 | `082f05186b01456bf846449dad31fa16a3ffb4950a6fbbebe202f312c3add74e` |
| S/AUTHORIZED_FREEZE.json | 22897 | `1c93b88b449393ea041b60d92a395efaecb718e84224fa303a4f17f1ccef685f` |
| S/controls/normal/AUDIT.json | 3830 | `de92f52c6bc5a9f34365085dec3ce1c346b3b9c93f7d8ee4a211c4ec02cdcc4a` |
| S/ROOT_RESULT_ADJUDICATION.json | 6680 | `d47d0f1185cf25360290def0d70eb56bbe0dc3eac3aeff7deadfc691048eed29` |
| ri83-single-saved-audit-independent-completed-el4hub66/INDEPENDENT_COMPLETED_REVIEW.json | 6904 | `d82909b8adf7e4a2153d4b34e1fe7a7e9c85b5f9ddd3f93865760b5ef721f771` |

## Interpretation and next boundary

The numerical consistency budget tau=2^-40 is not a certified error enclosure
or a statistical/calibration allowance. Conventional NumPy/SciPy comparisons
share FFT lineage. The independent saved audit executes no FFT or raw-HDF5
parser: it does not independently establish raw segment hashes, raw means,
raw-to-demeaned subtraction or correct Fourier coefficients. Those operations
retain the evidence of source qualification, actual caller checks and custody.
The audit verifies consistency of the saved operands under that limited scope.

The result supplies no population noise PSD, stationarity/Gaussianity test,
known covariance, calibration envelope, whitening, significance, detector
independence, protected validation or native gravity/geometry confirmation.
RI-40's pointwise calibration summaries and their frequency/time limitations
remain separate. No interpretation below 10 Hz is newly calibrated here.
This is an explicit V2, four-second, two-side adaptation, not an exact claim
about the older V1 tutorial, its whitening or the discovery analysis.
A next design may map each spectrum into a separately postulated finite
covariance proxy and propagate conditional bounds through RI-71/73's fixed
operator. It must preserve the distinction between empirical description,
chosen model covariance and calibrated physical covariance. RET remains paused.
