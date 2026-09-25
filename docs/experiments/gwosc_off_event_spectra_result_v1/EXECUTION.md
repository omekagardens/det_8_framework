# RI-83 — prospective observed spectral execution

25 September 2026 UTC. **Source-only proposal.** RI-80's repaired fabricated
qualification is independently accepted by the coordinator. This caller and
contract have not been executed or admitted for observed processing. No observed
`RESULT.json` exists from this packet. The coordinator owns a new external
freeze, execution, independent adjudication and publication. This is continued
authorized work, with source and execution review boundaries rather than a new
user-permission request.

The operation is the fixed [RI-78 descriptive statistic](../gwosc_off_event_spectra_v1/DESIGN.md)
on the exact recovered RI-37 public H1/L1 V2 pair. It calls the accepted
[RI-80 implementation](../gwosc_off_event_spectra_implementation_v1/IMPLEMENTATION.md)
without editing its primary, inspector, validator, method, tolerance, segment
selection or interpretation. Source inspection and metadata reads are the only
work performed in this initial packet; no numerical module, window, fabricated
fixture, HDF5 parser or observed array has been executed/read for it.

## 1. Accepted prerequisites

`run_observed.py` fixes the exact primary/validator/qualifier, design, inspector,
RI-37 report, RI-60 runtime source/report and accepted qualification identities.
The accepted full fabricated report is 63,464,716 bytes, SHA-256
`f247c20f9e112b48cc037d6256b47b5056ec354d58c0cf2817aad0363fc0fa0d`.
Its production window contains 16,384 little-endian binary64 values: 131,072
bytes, SHA-256
`525f6eb5be56990ea0a936ca11c8860797ee83df453e972cd734d5e065a170e8`.
These are accepted fabricated evidence and a fixed window, not observed spectra.
The caller hashes the full qualification file without retaining its large parsed
object. Its fixed window pin comes from that separately adjudicated report;
the caller cannot substitute a report merely claiming to have passed.

The recovery handoff is
`/Volumes/AI_DATA/development/det-review-evidence/ri37-input-recovery-20260924T221315Z-9ac44e02/INPUT_RECOVERY_HANDOFF.json`,
16,293 bytes, SHA-256
`be0b518ca43e423d7e2a737b85eec0cad119a1b4cbd19ed4f056f662277d2dc0`.
Only the following already recovered files are admitted under that directory's
`inputs/`; this packet includes no acquisition or alternate revision.

| Detector | Filename | Bytes | SHA-256 | Publisher MD5 |
|---|---|---:|---|---|
| H1 | `H-H1_LOSC_4_V2-1126259446-32.hdf5` | 1040592 | `6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6` | `50441a42c13fc1f14e5c4ea5527f1515` |
| L1 | `L-L1_LOSC_4_V2-1126259446-32.hdf5` | 1007420 | `56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189` | `361ae6a040a9fef7897b1e0124d5b0a1` |

Their public source URLs remain `https://gwosc.org/GW150914data/` plus those
exact filenames. URL provenance is already retained in the recovery handoff;
no network access is necessary here. Raw input pins are not replaced by newly
calculated pins or a renamed product.

## 2. Complete captured-source and runtime closure

A new unique durable directory below
`/Volumes/AI_DATA/development/det-review-evidence/ri83-execution/` is selected
only after this source review. No exact future execution path is claimed yet.
Its `experiments/` subtree contains these **sixteen** files with the relative
names in `SOURCE_NAMES`. Each manifest row carries `relative`, `original`,
`copy`, and `{bytes,sha256}` pin. The thirteen fixed pins are explicit in the
caller; the three noncircular descriptive/caller pins are frozen by the root.

| Files | Purpose |
|---|---|
| `gwosc_off_event_spectra_implementation_v1/{spectra.py,validate_result.py,qualify.py,IMPLEMENTATION.md,QUALIFICATION.json}` | Complete accepted RI-80 implementation, evidence and qualification source |
| `gwosc_off_event_spectra_v1/DESIGN.md` | Fixed RI-78 method and scope |
| `gwosc_context_operator_v2/{check.py,QUALIFICATION_REPORT.json}` | Exact admitted full runtime probe/report |
| `gwosc_input_qualification_v1/{inspect_inputs.py,INPUT_REPORT.json,requirements.txt,QUALIFICATION.md}` | Unchanged RI-37 inspection closure and full expected metadata |
| `accepted/INPUT_RECOVERY_HANDOFF.json` | Exact recovered-generation receipt |
| `accepted/production_window.f64le` | Qualified, pre-observed window bytes |
| `gwosc_off_event_spectra_result_v1/{run_observed.py,EXECUTION.md}` | This reviewed caller and contract |

The recovery handoff and window are copied from their separately pinned durable
locations. The window must be the already qualified binary snapshot, or an
explicitly reviewed byte-exact extraction of the accepted fabricated report;
no observed data or new numerical window construction is needed to prepare it.
The caller's `prepare_windows()` call occurs only during the subsequently
admitted worker and before input snapshotting, and must reproduce that exact
qualified pin. The same immutable cached production window supplies
`build_result`; its pin is checked again after calculation.

The external control, worker and supervisor form an additional explicitly
pinned helper closure. They are **not yet authored/frozen by this source-only
packet**. Their review must cover source capture before import and the exact
manifest/descriptor/resource contract below. The existing RI-80 `control.py`
provides the intended metadata-only API: `verify_sources`, `verify_runtime`,
`verified_body`, `parse_json`, `file_pin`, and `write_exclusive`. Reuse its
accepted bytes where compatible; any helper changes require their own new
source review and pins. Neither an ambient Python import nor a helper selected
only by filename is admission.

The unchanged named interpreter is
`/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python`.
Freeze its complete symlink chain, resolved executable bytes and exact runtime
inventory, including package binaries/metadata, extension modules and Python
support files. The existing RI-80 inventory has 3,925 files; its JSON is
1,216,343 bytes, SHA-256
`8b0329a83a1208b21dfb4771d2dd078aae6cb54a1741b7f20b4a4695c06e245c`.
Every file and membership list must still match. No installation, rebuild,
package update or new runtime qualification is implied.

The complete RI-60 fingerprint, including platform/build, NumPy configuration
and HDF5 1.12.2, must match before and after execution. Version strings alone
are insufficient. Its recorded CPython 3.11.6 / NumPy 2.1.3 / SciPy 1.14.1 /
h5py 3.12.1 configuration is not generalized to another environment. Preserve
all three RI-80 attempt directories and their original helper/source/runtime,
resource, failure and success receipts.

## 3. Worker interface, manifest and order

There is intentionally no runnable observed CLI in `run_observed.py`.
A separately reviewed external worker executes its pinned bytes as a captured
module and calls:

```python
execute(manifest, mode, control, runtime_probe, scientific_stream)
```

`mode` is `normal` or `optimized`. `control` and `runtime_probe` are the
worker's already source-admitted modules, with captured bytes bound to the
same root freeze. They are not injection points for arbitrary callbacks.
`scientific_stream` is the worker's binary stdout. The parent opens its exact
exclusive external `RESULT.json` destination, redirects stdout to it and
retains the descriptor through child termination. The caller checks the empty
regular file, offset zero, one hard link, device/inode and canonical path
before writing, and rechecks descriptor/path identity afterward.

The root's new canonical `PROSPECTIVE_FREEZE.json` has
`schema="ri83-observed-execution-freeze-v1"` and
`status="prospective_not_authorized"`. It declares the absolute root, sixteen
sources, complete helpers, interpreter binding, runtime inventory, expected
runtime, exact input declarations, qualification/window and acceptance-review
provenance, environment, limits, both mode commands and all exclusive paths.
After independent source/contract review and required fabricated controls, the
root preserves that file and writes a separately pinned
`AUTHORIZED_FREEZE.json` changing only status to
`authorized_observed_execution`. An authorization string supplied by an
unreviewed caller has no evidentiary force: the external launcher must itself
bind the complete root-reviewed authorization bytes before importing/launching.

For each mode the parent directory is `<root>/controls/<mode>/`. The manifest's
`runs[mode]` fields include `stdout=.../RESULT.json`,
`input_snapshots=.../inputs`, `artifacts=.../arrays`, and
`custody=.../CUSTODY.json`. The last three must be absent before the caller;
stdout must be the parent's newly exclusively opened empty file. Separate
`stderr`, attempt, runtime/worker and supervisor receipt paths are also frozen
and exclusive. All mode destinations are disjoint. Source/data/output symlinks
and alternate resolved paths refuse; the declared named interpreter symlink
is admitted only through its exact frozen chain and target bytes.

The worker/supervisor enforce this complete order:

1. Bind the authorization bytes and exact child argv/environment; refuse an
   existing attempt/output. Verify all original/copy/helper source pins and
   runtime inventory before scientific imports. Capture the RI-60 probe and
   caller source from admitted bytes. Caller repeats source/runtime admission,
   checks its own copied path and requires the full pinned RI-60 fingerprint.
2. Hash/admit the full accepted qualification, recovery handoff, actual window
   bytes and input report. Capture primary, validator and inspector bodies
   before executing any of these three local modules. Load those exact bodies,
   not imports resolved through an ambient sibling search path.
3. Materialize/check the already qualified production window. Snapshot both
   complete raw files as immutable bytes, checking fixed size, SHA-256 and MD5,
   canonical paths, descriptor identity and before/after file metadata. Record device/inode/size/mtime for both original and retained files and require those bindings again after calculation. Retain
   both complete snapshots in new exclusive read-only files. **Both bindings
   finish before either HDF5 parser sees either input.**
4. Call unchanged `build_result(payloads, inspector, expected_report,
   QUALIFICATION_PIN, WINDOW_PIN, artifact_dir)`. It rechecks both identities,
   uses those same immutable bodies for unchanged `_inspect` calls, compares
   the full published RI-37 metadata report, then reads the strain from those
   same bodies. It preserves every quality flag, L1's clear `NO_CW_HW_INJ`,
   empty literal `Yunits`, fixed selection and all finite/numerical gates.
5. Apply the complete unchanged `validate_result`. Independently enumerate and
   reopen every expected binary artifact as described below; a validator pass
   alone is not observation custody. Recheck source/runtime/input bytes and
   the production-window pin. Stream every canonical scientific JSON value
   with sorted keys, indent 2, finite JSON and one final newline; compare the
   expected streamed identity, emitted identity and reopened result file.
6. Reopen the complete binary inventory again after serialization and write
   separate caller custody. Root worker/supervisor then independently recheck
   source/runtime/input/artifact/output identities **after caller return and
   process termination**, bind the caller receipt to authorization and return
   status, and retain all resource samples and any failures.
7. Run optimized only if the normal attempt succeeded on the same authorized
   freeze and all its outputs still match. Require complete scientific
   `RESULT.json` byte equality and equal binary artifact names/shapes/pins
   after removing the deliberately different mode paths. An independent
   reviewer audits the observed all-bin evidence and provenance before the
   coordinator accepts and publishes an exact result copy.

Caller success is named `caller_gates_passed_pending_independent_review`.
It neither substitutes for the parent monitor nor publishes a result. The
captured caller returns the custody/result identities and artifact count to
the external worker. Exceptions, partial files or missing receipts mean failure;
the supervisor keeps the evidence, terminates if required and starts no
optimized successor. No clean-up or automatic retry is authorized by a failure.

## 4. Complete retained arrays and output distinction

The accepted builder has 122 direct binary artifacts: one production window,
one frequency grid, four arrays per each of 26 segments (demeaned, windowed,
primary PSD and conventional reference PSD), and four arrays per each of four
sides (mean PSD, ASD, reference PSD, reference ASD). It also saves all 113 array
records recursively exported anywhere in the complete scientific result,
including every comparison/window/square-root residual and every per-bin
threshold. The resulting expected inventory is exactly **235 regular files**.
No reported value or file is omitted to reduce memory or output volume.

The caller derives this full mapping independently from the validated result,
its exact segment starts, array shapes and identities. It checks every row's
closed keys, unique name, canonical path, `<f8` dtype, shape, byte count and
SHA-256, hashes every retained body, and requires exact directory membership.
It checks both direct names and the complete recursive `result-...` names.
Missing, duplicated, stale-hashed, extra or symlinked arrays refuse. This establishes
that retained snapshots represent the validated result; it does not independently
prove the observed calculation's numerical correctness.

Raw segment values are retained through the two complete immutable HDF5
snapshots and exact index ranges, as RI-78 specifies. The accepted builder
retains de-meaned/windowed intermediates and the array closure above; this
contract does not introduce unexported FFT-component artifacts or modify the
accepted builder. The complete scientific JSON retains all 8,193 frequency
bins, every segment and both distinct sides for both detectors. Canonical
streaming avoids a second full JSON string; it does not replace the all-bin
output by hashes or summaries. There is no new scientific output-size gate.

The separate `CUSTODY.json` contains both original/snapshot input records,
qualification/window pins, all 235 artifact rows, result identity, source and
runtime before/after records and literal limitations. Parent receipts add
manifest/command/helper identities, complete acquisition and acceptance
provenance, descriptor/output custody, resource samples, mode comparison and
failures. Host paths, clocks, mode and memory measurements do not enter the
scientific JSON. The unchanged result validator's existing canonical-input
contract remains; this caller does not redefine it.

## 5. Fixed launch and resource contract

The new external worker, after its own admission, invokes this captured callable.
The future serial child commands are equivalent to:

```text
<admitted-python> -I -B <root>/worker.py <root>/AUTHORIZED_FREEZE.json normal
<admitted-python> -I -B -O <root>/worker.py <root>/AUTHORIZED_FREEZE.json optimized
```

Exact absolute argv arrays, parent launch commands and helper pins are frozen
before launch; these templates are not execution evidence. Both children have
exactly this environment, with `<root>` expanded to the new durable directory:

```text
PATH=/usr/bin:/bin
LC_ALL=C
TZ=UTC
TMPDIR=<root>/tmp
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
VECLIB_MAXIMUM_THREADS=1
NUMEXPR_NUM_THREADS=1
__CF_USER_TEXT_ENCODING=0x1F5:0x0:0x0
```

The last value preserves the explicitly tested macOS startup binding; the
worker requires full environment equality, not an ignored-key exception.
One numerical worker at a time receives the unchanged 180-second wall deadline
and 524,288 KiB (512 MiB) sampled-RSS threshold. The existing monitoring policy
uses 0.025-second target polling, 0.1-second maximum accepted sample gap and
0.05-second `/bin/ps` timeout. Record every monitor attempt and valid sample,
elapsed time, maximum, exit code and termination/failure reason. Unavailable
monitoring or a missed deadline fails closed. A sampled bound can miss a shorter
transient peak and is not an OS hard memory cap. No tolerance or budget is
increased after observing the data or resource outcome.

## 6. Prospective fabricated caller checks and remaining gates

Before any actual input opening, review the caller and external helper source,
then freeze one bounded fabricated integration harness under the same admitted
runtime, environment and resource limits. It must accept no observed input path
and must not monkeypatch input pins to make an observed entry appear accepted.
Normal and optimized controls retain their exact fixture/source/output pins.
The new integration coverage is:

- On one already qualified fixed quarter-rate fabricated record for both
  detectors, use the unchanged `fabricated_result_fixture` and full validator.
  Independently materialize its direct segment arrays and every recursive
  result-array record into a temporary exclusive directory. Exercise the
  caller's `expected_artifacts` and `verify_artifacts` positive closure, exact
  122/113 counts, all names/shapes/body hashes, and named missing/extra,
  duplicate, wrong-shape, wrong-hash and symlink refusals. Retain the deliberate
  fabrication label; this is not actual `build_result` or HDF5 admission.
- Exercise `stream_result` on that full validated fabricated object against
  the unchanged validator's canonical contract, with every array intact.
  Validate the full canonical output and compare independent byte identity;
  use a parent-opened exclusive empty regular descriptor. Check wrong
  descriptor/path, altered bytes, pre-existing output and alias refusals.
- Use stdlib-only manifests and isolated scratch paths to test exact source
  closure names, changed/missing pins, prospective status, environment,
  runtime/command binding, stale paths and output admission. A refusal must
  occur before the harness's observed-read/parser sentinel could be called.
  Review snapshot ordering and descriptor checks separately; the positive
  fixed-input SHA gate cannot honestly be demonstrated using fabricated bytes.

These controls validate the new custody/encoding glue and do not repeat the
already completed 14 analytic, 10 direct-DFT or remaining RI-80 scientific
qualification campaign. They are **designed but not run** in this handoff.
The root must review and freeze their concrete source and receipts; no invented
pass count or report is supplied here. No normal/optimized actual result,
HDF5 replay, 235-file artifact inventory, measured resource outcome or observed
independent audit is yet established. A source correction requires review and
a new pin before the relevant subsequent freeze.

## 7. Scientific scope after an eventual pass

A pass would produce an auditable conventional four-second Welch description
of the already accessed public V2 records under the RI-78 fixed seven/six
segment and exclusion choices. This is the explicitly declared adaptation,
not an exact reproduction of the historical tutorial or a discovery analysis.
The term off-event identifies the fixed excluded interval; it does not prove
that either side is signal-free, stationary, Gaussian or statistically
independent. The L1 continuous-wave injection flag remains clear and its
physical effect remains unresolved.

The units are the publisher's nominal released V2/C02 strain convention; the
literal HDF5 `Yunits` is empty. No extra calibration correction, uncertainty
band, inferred detector-noise covariance, unit-white substitution, whitening,
chi-square/significance, fitted parameters or DET/native gravity prediction
is supplied. Qualified calibration/timing/mean-response/noise-estimation
premises and a native forward map remain distinct future requirements.
RET remains paused. Completing this bounded reproduction does not complete
the broader native geometry, gravity and measurement programme.
