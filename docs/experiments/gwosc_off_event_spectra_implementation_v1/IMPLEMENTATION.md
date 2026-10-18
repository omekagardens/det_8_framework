# RI-80 — qualified implementation of the RI-78 descriptive spectra

25 September 2026 UTC. **Fabricated numerical qualification independently
accepted.** Both frozen normal/optimized runs passed and produced byte-identical
[QUALIFICATION.json](QUALIFICATION.json). The final section records actual
execution, two retained failures, allocation repair and independent audits.
No observed spectrum was computed in this packet. The following original
source/interface contract remains applicable; its source-handoff status and
prospective counts are superseded by the acceptance record below.

The [accepted RI-78 design](../gwosc_off_event_spectra_v1/DESIGN.md) remains
unchanged: 24390 bytes, SHA-256
`3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce`.
The statistic, fixed 7/6 starts, periodic Hann, density normalization, complete
8193-bin outputs, `tau=2^-40`, endpoint fixtures and scientific limits are the
design's choices. No new adjustable method, data source or acceptance budget is
introduced here. This is a public conventional-measurement implementation;
RI-73 unit-white covariance and the native-law/RET boundaries do not change.

## Source responsibilities and interfaces

[spectra.py](spectra.py) implements fixed numerical operations and the complete
scientific-result assembler. Importing it opens no data file and computes no
window, synthetic signal or spectrum. It imports NumPy, SciPy signal and h5py;
the root launcher must admit that package/runtime closure before import.

| Interface | Contract |
|---|---|
| `prepare_windows()` | Materialize immutable little-endian binary64 window bytes for lengths 8, 16 and 16384; return their byte counts/SHA-256. Segment calls reuse read-only views. Freeze the production window pin during fabricated qualification, before observed parsing. |
| `segment_spectrum(x)` | Finite real NumPy float64 vector of length 16384 in production; lengths 8/16 are only the design's direct-DFT fixtures. Return window/mean/demeaned/windowed/FFT components, PSD, Q, frequency, explicit single-segment Welch reference and numerical check records. |
| `aggregate_periodograms(psds)` | Finite nonnegative 2-D float64 periodograms with 5, 9 or 8193 bins; return `(arithmetic_mean_psd, sqrt_mean_psd)`. Small bins support only those same fixtures. |
| `fixed_indices()` | Return fresh exact left/right interval/start/count/used/unused records; observed values cannot select indices. |
| `side_spectra(samples, side)` | Finite float64 shape `(131072,)`, side `left` or `right`; return the 7/6 segment outputs, means/ASDs/Q, whole-side explicit Welch reference and complete comparisons. |
| `check_psd(candidate, reference, q, delta_f)` | Enforce nonnegative finite arrays, matching fixed bins/spacing, the design's input-power scale and all-bin budget; return every absolute residual and its threshold. |
| `admit_metadata(actual, expected)` | Pure, type-sensitive, complete recursive comparison of already admitted metadata expectations; explicitly refuse identity or flag differences. It cannot authenticate its own `expected` argument. The actual builder first pins the complete published report. |
| `fabricated_result_fixture(arrays, expected_report)` | No HDF5 or filesystem access. Assemble a complete schema fixture from fabricated H1/L1 arrays and the pinned public metadata report. Return an explicit `fabricated_schema_fixture_not_observed` wrapper with a conspicuously fabricated qualification-report pin. Preserve that wrapper in qualification evidence; never publish its inner object as an observed result. |
| `build_result(payloads, inspector, expected_report, qualification_pin, window_pin, artifact_dir)` | Future observed worker only. Admit both fixed byte snapshots before either HDF5 parse, check the pre-observed window pin, run the unchanged admitted RI-37 inspector on those bytes, compare its full report, calculate fixed spectra, and retain every exported array plus demeaned/windowed snapshots in an exclusive external directory. Return `(scientific_result, artifact_inventory)`. Caller must separately validate, retain and publish that result. |

`SpectraError(ValueError).code` names the failure domain: `DIMENSION`, `DTYPE`,
`LENGTH`, `BINS`, `NONFINITE`, `NEGATIVE_PSD`, `ZERO_POWER`, `UNDERFLOW`,
`TOLERANCE`, `INPUT_PIN`, `FLAGS`, `METADATA`, `SCHEMA`, `IDENTITY`, or `PATH`.
All admission and numerical gates use explicit exceptions, not assertions.
An arithmetic exception refuses the run; an error classification never turns a
failed gate into a pass.

[validate_result.py](validate_result.py) is a separately implemented stdlib-only
consumer. `validate_result(result)` checks the exact closed nested scientific
schema, canonical floathex values, every array byte identity, fixed method,
indices/flags, frequency/window, every reported comparison/threshold, mean PSD,
pointwise ASD and Parseval consistency. `load_result(payload)` additionally
requires canonical finite UTF-8 JSON, no duplicate keys, and a 64 MiB result
size cap. Its `ValidationError(ValueError).code` distinguishes `SCHEMA`,
`IDENTITY`, `BINS`, `METADATA`, `NONFINITE`, `NEGATIVE_PSD`, `ZERO_POWER`,
`UNDERFLOW` and `TOLERANCE`. It imports neither the primary nor an FFT library.

The validator does not establish observation provenance by inspecting a hash
string. It authenticates embedded RI-37 metadata by reassembling the complete
published report and checking its exact canonical byte identity. Source/data
custody, accepted qualification, stored intermediate identities and their
association with the observed execution require the caller's separate manifest
and review. A deliberately fabricated schema fixture is useful for mutation
checks and never satisfies that observation custody.

[qualify.py](qualify.py) is independently authored in the measurement-review
lane. It contains the analytic endpoint/normalization fixtures, scalar direct
DFT, tiny-amplitude scaling, aggregation, whole-side index/unused-tail tests and
positive/mutated complete-result checks. It must not import a primary FFT or
normalization helper into the scalar direct-DFT oracle. Exact fixture coverage,
source identity and any eventual observed pass/failure counts come from its
reviewed source and actual report, not predictions in this note.

The source currently declares 14 production-size analytic cases, 10 small direct
DFT cases, 7 amplitude-scaling comparisons, 2 whole-side cases, 1 aggregation
case, 18 producer refusals, 19 validator/parser refusals, 2 positive complete
schema/serialization checks and an equal fabricated-metadata control. These were
prospective coverage counts at source handoff; every listed case subsequently
passed in both admitted modes, as recorded below. The complete schema fixture
is also reconciled to the independently checked segment/side values and byte
identities; it cannot pass solely because producer and validator agree internally.

## Scientific encoding and retained artifacts

The eight scientific top-level fields are `schema`, `method`, `inputs`,
`frequency_hz`, `window`, `detectors`, `checks`, and `limitations`. The executable
validator is the exact nested field contract. Scientific floating values use
canonical finite `float.hex()` strings. Each complete array record contains
exactly `dtype="<f8"`, one-dimensional `shape`, ordered `values_hex`, and the
SHA-256 of C-order little-endian binary64 bytes. Integer fields retain integer
types. Historical metadata is embedded unchanged, including its literal
numeric attributes, raw mask arrays and publisher descriptions; its original
JSON numeric spelling is part of the pinned RI-37 report, not a newly processed
scientific floating result.

The actual builder retains every full all-bin segment PSD, side mean PSD/ASD,
conventional reference and residual/threshold array in both JSON and external
binary form. A recursive traversal backs every exported array record with
identical bytes, including window/frequency and numeric check arrays. It also
retains complete demeaned/windowed segment bytes and their hashes. Raw segments
are identified through the retained complete HDF5 inputs, global indices and
raw segment hashes; they are not separately duplicated as raw waveform JSON.
The artifact inventory gives each emitted binary's logical name, actual path,
byte count, SHA-256, dtype and shape. Files are created exclusively, never
overwritten; failure leaves already written evidence in place.

The caller validates the returned scientific object before writing canonical
`RESULT.json` with `spectra.canonical`, and verifies all retained artifact
identities against the inventory. A separate custody manifest binds the result,
inventory, accepted qualification, source/runtime/window closure, input
snapshots and source/data rechecks. Absolute paths, execution mode, clocks,
resource samples and stderr belong in separate receipts. Normal/-O scientific
result bytes must agree exactly under the admitted environment.

## Complete closure and prospective execution

The local scientific source closure is `spectra.py`, `validate_result.py` and
`qualify.py`; include this note and RI-78's design in the frozen method bundle.
No sibling is imported by an ambient `sys.path` search: the independently
reviewed qualification launcher snapshots and executes the pinned source bytes.
The additional fixed predecessor closure is:

| Purpose | Fixed repository source/report |
|---|---|
| Complete runtime fingerprint | `gwosc_context_operator_v2/check.py` (38088 bytes, SHA-256 `a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02`) and `QUALIFICATION_REPORT.json` (9413345 bytes, SHA-256 `1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f`). Only the already published runtime function is called. |
| Exact metadata expectation | `gwosc_input_qualification_v1/INPUT_REPORT.json` (31096 bytes, SHA-256 `a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80`); no observed input opens in fabricated qualification. |
| Future actual input admission | Unchanged `gwosc_input_qualification_v1/inspect_inputs.py` (14817 bytes, SHA-256 `bdafb9c694fc9f33071072f1a2fc027bdb85e9262245ad3f9e29f860935d142a`), its qualified metadata and the exact input/recovery pins in RI-78. Both byte snapshots are bound before parsing; no download path exists in this implementation. |

The admitted packages remain CPython 3.11.6, NumPy 2.1.3, SciPy 1.14.1,
h5py 3.12.1 and HDF5 1.12.2, with the complete existing RI-60 platform/build/
configuration fingerprint. The currently recovered executable is
`/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python`.
The launcher must bind its named symlink, resolved chain and target bytes,
not reject the already admitted interpreter symlink or accept a changed target.
No package installation, runtime migration or qualification relaxation belongs
to this source packet.

After source review, the coordinator creates a new durable external execution
directory, copies and checks the complete relative layout, freezes exact paths
and commands, and launches **serial** children equivalent to:

```text
<admitted-python> -I -B <frozen-experiments>/gwosc_off_event_spectra_implementation_v1/qualify.py
<admitted-python> -I -B -O <frozen-experiments>/gwosc_off_event_spectra_implementation_v1/qualify.py
```

These are prospective child commands, not evidence of launch or a substitute
for the root's pre-import custody/resource gate. Freeze numerical worker counts
to one (`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`,
`VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS`) in the recorded environment.
The supervisor enforces the existing 180-second wall deadline and 512 MiB
sampled-RSS threshold, polling no slower than 0.1 seconds. It records samples,
maximum, exit/status, output hashes and any timeout/termination. Sampling can
miss a shorter peak and is not an OS hard memory cap. Retain failed evidence;
do not enlarge budgets, tune tolerances or retry silently.

The initial fabricated run reads source and the two pinned predecessor JSON
reports only. It accepts no observed input path and creates no observed spectral
result for H1/L1; its complete schema object is explicitly fabricated. Reopen
the complete source closure after each mode, compare full
deterministic qualification outputs and have the coordinator independently
adjudicate actual checks. Only then may a later observed execution freeze bind
the accepted qualification report, production-window pin, exact pair, admitted
inspector, read-only snapshots and exclusive output destinations. This module
contains no CLI that can self-authorize that observed step.

## Historical remaining work at source handoff

Numerical behavior, runtime/resource use, fabricated gate counts and normal/-O
equivalence remain untested. The positive complete-result fixture and targeted
mutations must pass under the same frozen budget, with independent analytic
and direct-DFT evidence. A source correction after the freeze requires a new
recorded source identity and appropriate requalification; no report is edited
to manufacture success. No observed spectra or noise/covariance claims follow
from source completion. The subsequent observed step remains separately gated
within the user's already authorized programme.

## Actual qualification and independent acceptance — 25 September 2026 UTC

The unchanged RI-78 numerical method and 180-second/512 MiB sampled-RSS
limits passed after two separately preserved failed attempts. The final
numerical sources are:

| File | Bytes | SHA-256 |
|---|---:|---|
| spectra.py | 25668 | `591321eafeae2faa231bae2409fb6d95227d67976a3ff0f801a37686bc745093` |
| validate_result.py | 18529 | `00514faa329cb4bc05d83de74db49d3b603fe8512f9435844f9af48c0c032a63` |
| qualify.py | 38194 | `1ef4df335fbd1fb50878e1961d41a2697e51351e703f1f743ada08ea1c8b8682` |
| QUALIFICATION.json | 63464716 | `f247c20f9e112b48cc037d6256b47b5056ec354d58c0cf2817aad0363fc0fa0d` |

The report is the exact normal stdout and also the exact optimized stdout;
it was copied without editing or removing any array. All 14 production analytic
cases, 10 scalar-DFT cases, 7 amplitude-scaling comparisons, 2 whole-side cases,
1 aggregation case, 18 producer refusals, 19 validator/parser refusals, 2 positive
complete-schema cases and the equal-metadata control passed in each mode.
Repeating under optimization does not double distinct case counts.
The admitted production window is 131072 bytes, SHA-256
`525f6eb5be56990ea0a936ca11c8860797ee83df453e972cd734d5e065a170e8`.

| Actual mode | Seconds | Peak sampled RSS (KiB) | Samples | Largest sample gap (s) |
|---|---:|---:|---:|---:|
| normal | 6.308242499999324 | 440992 | 197 | 0.03460891599934257 |
| optimized | 6.899942459000158 | 461168 | 214 | 0.04090720800013514 |

Both exited zero, had empty stderr and no supervisor stop; full runtime
fingerprints matched RI-60. Sources, helpers and all 3925 runtime files passed
pre/post identity checks. Root additionally reconciled every raw monitor attempt
with its recorded sample. These are sampled-RSS results, not a hard memory cap.

The first attempt failed before numerical import because macOS inserted
`__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0`. A separate stdlib-only startup probe
identified the sole environmental difference. A newly frozen explicit
environment retained strict equality. That second attempt failed at 533152 KiB
sampled RSS after 6.581045958 seconds; no completed qualification report or
measured phase attribution was available. Neither failed attempt launched its
optimized successor. Both failures and their original frozen sources remain
in durable external evidence.

The reviewed allocation repair changed only `qualify.py`: preserve complete
binary64 arrays until streaming the identical canonical floathex JSON; mutate
and restore exact fixture slots rather than cloning complete schema objects;
release unused schema aliases before the unchanged complete parser checks.
It did not change scientific sources, fixtures, residuals, thresholds, domains,
refusal reasons, runtime or resource limits. The old qualifier (35210 bytes,
SHA-256 `a10b24b8dfaba91bf4936512941b9e32e12affeb707a80af0821b50d33882741`)
and complete delta remain retained. Root and a separate reviewer examined the
full final source and repair before a new prospective freeze and actual runs.

Root's saved-report audit reconstructed all 345 arrays (1836244 values), all
75 PSD comparisons and 369 bound records, 39 Parseval calculations and the 37
recorded refusal reasons. A separate stdlib-only audit also reconstructed the
37 fabricated segment inputs and checked every analytic endpoint oracle,
small scalar DFT, scaling case, fixed-side sentinel and aggregation discriminator;
it checked 450755 PSD comparison bins and 155667 ASD bins. Neither audit reran
the numerical producer or opened observed strain.

Audit limits remain explicit: primary energy/Q scalar operands are not all
separately retained, so their recorded discrepancies have source/receipt support
rather than independent recomputation of every original operand. The complete
fabricated RESULT fixture is represented by its identity and actual validation
records, not retained as an observed object or independently rerun by the audit.
Its identity is 38642203 bytes, SHA-256
`b077ee26bde1a6eb742d2677cb267a54029ad419f72592d9f1dff1d1561d3ddf`.
The report retains its `fabricated_schema_fixture_not_observed` wrapper.

Durable successful execution directory:
`/Volumes/AI_DATA/development/det-review-evidence/ri80-execution/prep-allocation-20260924T235309Z-ac71099c/`.
It retains the original note, complete copied source/runtime closure, concrete
command arrays and environment, exclusive logs and receipts. This acceptance
appendix changes only documentation, after execution. Key evidence identities:

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| PROSPECTIVE_FREEZE.json | 22192 | `7a9a0747c03cfeab918c74348f6519748ea48787a0c3ab4297827bbeb9c4316b` |
| AUTHORIZED_FREEZE.json | 22201 | `d882e6d34d335c6f2711da543ce07f534adf2f4b537444853166b57ebe4c356d` |
| ROOT_PREEXECUTION_REVIEW.json | 7644 | `a7e58de477a4cc893a629bca3bc530bdf383e93755923dec3642273f0cfc68bf` |
| controls/normal/receipt.json | 64835 | `fbab3b58c583a7a00252934e5d71fe60c2228dfacf729c8090582cdfbabcf0b4` |
| controls/optimized/receipt.json | 69067 | `95400e182d229f8dbe08c8a7e5e0a2b198cf347f903a177c893f0deb8e2d7d4b` |
| ROOT_SAVED_REPORT_RECONCILIATION.json | 2131 | `d596c8b8bfc347384f9f04b39443e44125a94c0ea25da0bc7368dd2b2e98f676` |

Independent completed audit:
`/Volumes/AI_DATA/development/det-review-evidence/ri80-independent-math-review/completed-20260925/INDEPENDENT_COMPLETED_EVIDENCE_REVIEW.json`,
6715 bytes, SHA-256
`f1c5ec676454ec0d4dcd5e76a9fdaa7d2c6671b9951dba38edc6b1893710c49a`.
The publication checkpoint's `EVIDENCE_MANIFEST.json` under
`/Volumes/AI_DATA/development/det-review-evidence/ri80-ri82-publication-20260925T000640Z-63dd51ee/`
also pins both earlier failed receipts, the repair and independent delta review.
External receipts are local custody evidence; the repository report and sources
are the portable scientific qualification artifacts, not a claim that all raw
external files are included in git.

RI-83 now implements the separate actual-input caller/contract. Its source
must be independently reviewed and its complete data/source/runtime/window/
qualification closure freshly frozen before any observed processing. Retain
the unchanged RI-37 inspector, exact recovered H1/L1 bytes, blank Yunits and
L1 clear CW no-injection bit. Descriptive nominal spectra cannot replace
calibration, a joint covariance model, significance or a native forward map.
