# RI-64 — fixed observed-context consumer

**Independently accepted after source, qualification, actual-result and final
documentation reviews. Both execution modes and the independent actual-result
audits passed.** The new 75-gate consumer qualification passed and was
adjudicated before observed access. Both actual driver runs reported all fixed
gates passed and produced identical complete exports. Sections 9–10 record the
execution and accepted independent-audit evidence, with their exact limits.

The accepted [RI-62 design](DESIGN.md), the three source files, every numerical
threshold and the resource budgets were frozen prospectively. The execution
snapshot of this guide was **32323 bytes**, SHA-256
`bb5fdf6656a9fa212bf56d2807303a4847c1ad49ed5cbe1e422e12550aba8bf3`.
It is retained separately from this later documentation revision. The final
documentation's eventual hash must be recorded with publication after the audit;
it is not the method-snapshot identity. This revision adds outcome, custody and
reproduction evidence without retroactively changing the executed method.

The comparison uses the same central nominal H1/L1 samples under three finite
boundary conditions: filter the short segment; filter a specified longer segment
containing its recorded surroundings; and retain the corresponding values of the
published filtered 32-second record. Increasing context is not assumed to improve
the answer, and the 32-second rounded result is not physical ground truth. There
is no magnitude gate on either observed difference.

## 1. Source and dependency custody

The new files have disjoint responsibilities. `context.py` owns the source and
metadata admission, immutable-snapshot custody, private state-bound admission
checks, interval arithmetic and fixed numerical evaluation. `check.py` executes
the 75 synthetic consumer gates. `process.py` requires a caller-pinned successful
new receipt, orchestrates the fixed actual calculation and writes the two complete
exports exclusively. The shared module pins no child; the qualifier pins the
shared module, and the driver pins the qualifier. No published numerical,
inspector, oracle, receipt, design or prior output is modified.

| New source | Bytes | SHA-256 |
|---|---:|---|
| `context.py` | 32566 | `fb0ec155f16292a07a5884e686e1dca167d5e37d7efc87e26ea1c41eb35f717b` |
| `check.py` | 34640 | `f76bab65b4f3a4d8cde5efe292d2bfe3a5d8792048feace55308884757f38241` |
| `process.py` | 10478 | `4a7ad4e1a800a03eb7fcb4ddafec3c6951d46af8032a20f2f45d6893ca633fcc` |

The following 15 source, design and metadata artifacts join those three files
in the pre-observation closure. Paths in the table are relative to
`docs/experiments/`. Preserve this layout in the isolated execution copy.

| Dependency | Bytes | SHA-256 |
|---|---:|---|
| `gwosc_observed_context_v1/DESIGN.md` | 19255 | `636401b05620f227115362e1ecbf175a4a90a9dd34a021e0813f14e73ed58be2` |
| `gwosc_context_operator_v2/check.py` | 38088 | `a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02` |
| `gwosc_context_operator_v2/QUALIFICATION_REPORT.json` | 9413345 | `1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f` |
| `gwosc_nominal_result_v1/process.py` | 18823 | `f026667837cfb6e2040e228f8cd9dd73e983fb5bc0610cb106e8dce521d685fd` |
| `gwosc_context_operator_v1/QUALIFICATION_REPORT.json` | 161816 | `7dfbc8cac7e631a9c3663bca2b288b134d6cea03f1d0ca14c8334746761a808a` |
| `gwosc_nominal_processing_v1/filtering.py` | 8805 | `9a93c1f218fecfa6fdf7ee0e30e054ad0973dfb1f04ae339dfbb0e7a6f8ae1be` |
| `gwosc_nominal_processing_v1/reference.py` | 7253 | `c8cffaac8bf0c1647a120ecb00ba1505ef69b60f80cda653d60b2a2f7e9da305` |
| `gwosc_nominal_processing_v1/COEFFICIENTS.json` | 7698 | `700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0` |
| `gwosc_nominal_processing_v1/SYNTHETIC_REPORT.json` | 107468 | `2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3` |
| `gwosc_nominal_display_v1/RECIPE.md` | 14014 | `872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a` |
| `gwosc_context_sensitivity_v1/DESIGN.md` | 21702 | `e672cea6c5f06c5927b54b0021636793c14b01e8efe57aa8e719fd464a527e45` |
| `gwosc_input_qualification_v1/inspect_inputs.py` | 14817 | `bdafb9c694fc9f33071072f1a2fc027bdb85e9262245ad3f9e29f860935d142a` |
| `gwosc_input_qualification_v1/INPUT_REPORT.json` | 31096 | `a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80` |
| `gwosc_context_operator_v2/operator.py` | 30531 | `ef8169986977c533f549f2ca59b5f72224464db616d8303c451d6a29f22df6af` |
| `gwosc_context_operator_v1/oracle.py` | 9484 | `37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651` |

The old failed RI-57 receipt remains a failed prerequisite record: 187 passes
and nine failures out of 196. It cannot qualify this consumer or substitute for
the successful RI-60 receipt. The latter's 196 gates are validated as previously
completed evidence, **not reported as newly executed gates** by RI-64. The exact
small-system oracle is reused from its published v1 path; no new oracle authorship
is claimed.

Admission binds retained source/metadata bytes before parsing or execution. The
shared module rechecks the inherited closure and numerical state at the access
and evaluation boundaries. These checks protect the fixed-source reproduction
workflow; they are not a sandbox against arbitrary malicious Python mutation.
No caller-provided replacement coefficients, filter settings or stages exist.

## 2. Runtime and bounded execution

Use the existing qualified interpreter:

```text
/var/folders/47/s7fm88bn5ql2tw7j103kbyzr0000gn/T/det-ri44-processing-apas30qu/env/bin/python
```

This is an existing temporary location, not a durable installation promise.
Do not install or substitute a runtime if it disappears. The required versions
are CPython 3.11.6, NumPy 2.1.3, SciPy 1.14.1 and h5py 3.12.1, with HDF5 1.12.2.
The source also compares the complete previously recorded configuration:
CPython build `3.11.6 (main, Nov  2 2023, 04:39:43) [Clang 14.0.3
(clang-1403.0.22.14.1)]`, Darwin 25.5.0, arm64, little endian, the full Darwin
kernel string and NumPy compiler/BLAS/LAPACK/SIMD configuration. Version-number
agreement alone does not qualify another machine. The pinned RI-44 and RI-60
receipts remain authoritative for the complete fields.

Run modes serially, with one worker and no environment installation. The
qualifier uses dense exact matrices only for the tiny fixed oracle systems. The
actual path recomputes the sixteen selected adjoint certificates and uses the
fixed interval/256-bit engine limits; it does not construct a dense 10961-square
matrix or certify the whole 131072-sample operator. Precision, row selection,
padding and thresholds cannot be changed after inspecting an outcome.

The coordinator froze external wall-time and resident-memory budgets at 1800
seconds and 2 GiB sampled resident memory **per process** before either phase.
These are operational watchdog limits, not a hard allocator cap or proof of
whole-machine memory usage. All four completed processes stayed within them;
the measured times and sampled RSS values are recorded in section 9. Use a supervisor that
records the command, return code, timeout/resource reason, stdout and stderr in
new external files; a limit failure stops adjudication. Normal/optimized jobs
must not run concurrently. Do not discard a failure and silently retry with
larger limits or revised source.

The command examples below use an external `run_once.py` supervisor accepting
`LABEL COMMAND...`. One suitable minimal Darwin supervisor is provided here so
that the command sequence is executable without a shell-specific timeout utility.
Save it **outside the repository**, review/freeze it with the execution record,
and set `RI64_RUN_DIR` to the new external receipt directory. Its RSS sample is
for the launched process, whose reviewed consumer code creates no worker
processes; it is not a measurement of the machine's total memory. It writes no
scientific output and never handles an input body.

```python
# External run_once.py; receipt metadata does not enter scientific JSON.
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

root = Path(os.environ['RI64_RUN_DIR'])
label, command = sys.argv[1], sys.argv[2:]
if not root.is_dir() or not command or not label.replace('-', '').isalnum():
    raise SystemExit('invalid external run directory, label or command')
paths = {name: root / (label + '.' + name) for name in ('stdout', 'stderr', 'run.json')}
if any(path.exists() or path.is_symlink() for path in paths.values()):
    raise SystemExit('refuse to replace an existing run record')
wall_limit, rss_limit_kib = 1800, 2 * 1024 * 1024
start, peak_rss_kib, stop_reason = time.monotonic(), 0, None
with paths['stdout'].open('xb') as out, paths['stderr'].open('xb') as err:
    child = subprocess.Popen(command, stdout=out, stderr=err, start_new_session=True)
    try:
        while child.poll() is None:
            if time.monotonic() - start > wall_limit:
                stop_reason = 'wall_time_limit'
                break
            sample = subprocess.run(['/bin/ps', '-o', 'rss=', '-p', str(child.pid)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    timeout=5, check=False)
            if child.poll() is not None:
                break
            text = sample.stdout.strip()
            if sample.returncode or not text.isdigit():
                stop_reason = 'rss_monitor_unavailable'
                break
            peak_rss_kib = max(peak_rss_kib, int(text))
            if peak_rss_kib > rss_limit_kib:
                stop_reason = 'resident_memory_limit'
                break
            time.sleep(0.25)
    except BaseException as error:
        stop_reason = 'supervisor_' + type(error).__name__
    finally:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL)
        code = child.wait()
def file_identity(path):
    # Incremental hashing avoids bringing large result streams into supervisor memory.
    digest, size = hashlib.sha256(), 0
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
            size += len(chunk)
    return {'bytes': size, 'sha256': digest.hexdigest()}
record = {'command': command, 'exit_code': code, 'stop_reason': stop_reason,
          'wall_limit_seconds': wall_limit, 'rss_limit_kib': rss_limit_kib,
          'elapsed_seconds': time.monotonic() - start, 'peak_sampled_rss_kib': peak_rss_kib,
          'stdout': file_identity(paths['stdout']), 'stderr': file_identity(paths['stderr'])}
with paths['run.json'].open('x') as stream:
    json.dump(record, stream, sort_keys=True, indent=2)
    stream.write('\n')
raise SystemExit(0 if code == 0 and stop_reason is None else 1)
```

A launch/supervisor failure is also a failure, even if it precedes creation of a
complete run receipt. Keep any files that already exist. External elapsed times,
paths and sampled memory belong in run records, not deterministic scientific
reports. The driver removes only its own newly created output files if a write
fails; preserve any incomplete external remnants for inspection, never treat
them as an accepted two-file export.

## 3. The new 75-gate inventory

The fixed top-level count is **6 index + 32 toy + 4 control + 33 refusal = 75**.
Each gate retains its detailed subcase counts. A failed category produces a failed
qualification; a failed or incomplete receipt cannot admit actual processing.

The six index cases are `positive_plain`, `negative_plain`,
`positive_zeros_a`, `negative_zeros_a`, `positive_zeros_b` and
`negative_zeros_b`. Each uses all 131072 synthetic source values `±k/2^20`.
Zero variants explicitly assign both sign patterns at source indices 61440,
65536 and 68305. They check every retained x/w/z coordinate, source index,
central rational clock, array hex value/hash and signed-zero injection identity.
Each also fabricates a nonconstant identity-transform 4096-sample crop and proves
both detector baselines select precisely its first 2769 values, corresponding to
the original central indices. A one-sample shifted prefix has a consistent new
array identity but must fail the exact original-index comparison. This controls
subset custody; it is not a filtering result for a synthetic indexed record.

Across the six cases there are 131532 retained x/w/z coordinate checks,
16614 central clock checks, **33228 crop-prefix coordinate checks** and six
targeted off-by-one refusals. These are repeated synthetic checks, not counts
of independent observed measurements.

The 32 toy categories use the eight published configurations, in order:
`identity`, `first_order`, `biquad`, `two_sections`, `two_stages`, `fir`,
`zero_dc`, `zero_dc_then_biquad`; each has central length 4 or 7 and side length
1 or 2. The oracle constructs all 448 required basis columns. Every central row
is exercised using the fixed signed x/z values and their zero-center,
zero-context and both-zero variants. There are 704 exact-point row checks and
704 broad-interval row checks. Broad radii are `((coordinate mod 3)+1)/1024`:
they test exact signed reductions and containment, not the actual width gate.
Point-row controls also exercise selected-row endpoint gates and exact-zero
behavior. No admitted physical coefficient is filtered by these tiny systems.

The four standalone controls are `endpoint_outside_pass`,
`endpoint_outside_fail`, `nominal_all_ties` and `nominal_signed_reduction`.
They include the prescribed points `1+2^-40` and `1+2^-20` against [1,1],
and exact binary64-difference reductions retaining every maximum tie.

The 33 refusal categories are the following exact names:

```text
source_changed, source_missing, coefficients, stage_order, padding,
current_receipt_missing, current_receipt_failed, current_receipt_stale,
ri60_receipt_failed, ri60_receipt_stale, runtime_mismatch,
unreconciled_rows, resource_exhaustion,
input_missing, input_swapped, input_truncated, input_corrupt_same_size,
grid_mismatch, nonfinite_samples, data_inconsistency, altered_flags,
altered_annotations, index_shift, crop_values_changed, crop_identity_changed,
output_exists, interval_misses_exact, interval_reversed, interval_overwide,
numerical_threshold, midpoint_only, overlap_only, both_inputs_bound_before_parse
```

Current-receipt mutations start from a complete positively validated synthetic
receipt, then change only the claimed status or source identity. That fixture
is never emitted as executed qualification. The numerical-threshold control
uses a mocked four-value identity computation at input peak `2^-20`: exact
agreement passes, then residual `2^-40` fails the actual-scale limit even though
it would pass a unit-floor tolerance. It also checks signed-zero output and
refusal of a nonzero output for zero input. The both-inputs control invokes the
actual custody entry point with only its row prerequisite mocked: failure of
the second synthetic snapshot must occur before any inspector parser call.
No observed raw or crop body is accessed by qualification.

## 4. Qualification commands and adjudication

First freeze the reviewed source/dependency closure in a new external copy
retaining `docs/experiments/...` paths. Do not include raw HDF5 or the two observed
RI-47 exports in the qualification copy. The pre-observation sources/metadata
listed above suffice. The later actual copy can add those artifacts only after
qualification is accepted; its 18-file pre-observation closure must stay identical.
The execution guide's frozen identity is recorded separately from its later
status/evidence revisions.

These variables are examples of required caller choices, not existing result
locations. Replace the absolute-path placeholders before running. The input path
is not assigned until the later actual phase. `set -C` prevents shell-redirection
overwrite; every supervisor label and output leaf must also be new.

```sh
set -eu
set -C
export RI64_PY='/var/folders/47/s7fm88bn5ql2tw7j103kbyzr0000gn/T/det-ri44-processing-apas30qu/env/bin/python'
export RI64_ROOT='/absolute/new/external/qualification-copy'
export RI64_RUN_DIR='/absolute/new/external/run-records'
export RI64_SUPERVISOR='/absolute/new/external/run_once.py'
RI64_PROGRAM="$RI64_ROOT/docs/experiments/gwosc_observed_context_v1"
test -x "$RI64_PY"
test -d "$RI64_RUN_DIR"
```

Verify the top-level source and accepted design bytes before executing them.
The reviewed admission then binds the complete inherited closure before use.
Keep the output of this check in the external freeze record if desired.

```sh
"$RI64_PY" -I -S -B - "$RI64_PROGRAM" <<'PY'
import hashlib
from pathlib import Path
import sys
base = Path(sys.argv[1])
pins = {
 'context.py': (32566, 'fb0ec155f16292a07a5884e686e1dca167d5e37d7efc87e26ea1c41eb35f717b'),
 'check.py': (34640, 'f76bab65b4f3a4d8cde5efe292d2bfe3a5d8792048feace55308884757f38241'),
 'process.py': (10478, '4a7ad4e1a800a03eb7fcb4ddafec3c6951d46af8032a20f2f45d6893ca633fcc'),
 'DESIGN.md': (19255, '636401b05620f227115362e1ecbf175a4a90a9dd34a021e0813f14e73ed58be2')}
for name, expected in pins.items():
    path = base / name
    if not path.is_file() or path.is_symlink():
        raise SystemExit('source must be a regular retained file: ' + name)
    body = path.read_bytes()
    if (len(body), hashlib.sha256(body).hexdigest()) != expected:
        raise SystemExit('source pin mismatch: ' + name)
print('Three source files and accepted design match the prospective pins.')
PY

if "$RI64_PY" -I -S -B "$RI64_SUPERVISOR" qualification-normal \
    "$RI64_PY" -I -B "$RI64_PROGRAM/check.py"
then RI64_QN=0
else RI64_QN=$?
fi
if "$RI64_PY" -I -S -B "$RI64_SUPERVISOR" qualification-optimized \
    "$RI64_PY" -I -B -O "$RI64_PROGRAM/check.py"
then RI64_QO=0
else RI64_QO=$?
fi
test "$RI64_QN" -eq 0
test "$RI64_QO" -eq 0
test ! -s "$RI64_RUN_DIR/qualification-normal.stderr"
test ! -s "$RI64_RUN_DIR/qualification-optimized.stderr"
cmp "$RI64_RUN_DIR/qualification-normal.stdout" "$RI64_RUN_DIR/qualification-optimized.stdout"
```

A zero exit code or byte equality alone is insufficient. Independently review
both complete receipts: schema `ri64-consumer-qualification-v1`, status
`all_consumer_gates_passed`, exact 75/75/0 counts, ordered inventory, detailed
index/toy subcounts, source/design/dependency identities, unchanged runtime and
the separately identified successful RI-60 receipt. Confirm no admitted-coefficient row or observed
body was computed/read by the new synthetic suite. Engine resource-refusal
controls and source/coefficient validation are separate from such execution. Archive failures under their original
identities; never replace an unsuccessful attempt with a success-looking summary.

The completed new receipt was adjudicated before the actual phase. Neither the
old RI-60 receipt nor an author/mock report substitutes for this **33132-byte**
normal/optimized-identical receipt:

```sh
export RI64_RECEIPT_BYTES='33132'
export RI64_RECEIPT_SHA256='56aa06c442384bd6249875443930202e09e874b4318aa995a8b7bb6dec1dab1b'
```

Both actual modes used this same caller-pinned normal receipt. The driver rebinds
its bytes, loads the pinned qualifier and independently validates its complete
admission fields before computing certificates or accessing observed input.
The literal path examples elsewhere in the commands are caller-selected fresh
reproduction locations, not missing scientific pins; never rerun into the retained
completed output directories listed in section 9.

For the completed coordinator execution, qualification used the isolated
18-file copy. The actual driver used the byte-frozen project source tree, where
the two published observed exports already existed. The launchers checked the
same eighteen source/metadata identities before and after each run; the actual
and qualification freezes bind the same source closure. The driver alone opened
and parsed the observed exports after certificate reconciliation. Only after a
successful driver return did the outer launcher rehash the observed predecessors
and raw files for its unchanged-input check. No observed artifact was copied into
the qualification tree. Outputs and execution records remain external. A later isolated reproduction may restore the published
observed artifacts after qualification, preserving the same pins and layout.

## 5. Actual input custody and commands — after qualification only

Include the following unchanged published exports in the actual closure.
They are observed bodies and are intentionally absent from the qualification copy.
The consumer binds both before parsing either JSON body, after all sixteen row
certificates have reconciled.

| Artifact relative to `docs/experiments/` | Bytes | SHA-256 |
|---|---:|---|
| `gwosc_nominal_result_v1/CROP.json` | 395470 | `a580481b9f6ea8dbb90242f12023817709ee7ac208d504110966f01f353592e7` |
| `gwosc_nominal_result_v1/PROCESSING_REPORT.json` | 159384 | `98bf0c53d5b988d3bb2aaa5f60c0fbcd87512501dd1137175b25589cc4856820` |

Use only the existing qualified original 4096 Hz V2/C02 pair. No new acquisition,
substituted version, longer record or downsampled overlap is part of this packet.

| Filename | Bytes | Publisher MD5 | Local SHA-256 |
|---|---:|---|---|
| `H-H1_LOSC_4_V2-1126259446-32.hdf5` | 1040592 | `50441a42c13fc1f14e5c4ea5527f1515` | `6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6` |
| `L-L1_LOSC_4_V2-1126259446-32.hdf5` | 1007420 | `361ae6a040a9fef7897b1e0124d5b0a1` | `56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189` |

The driver accepts only a directory containing these named records. It first
validates the current new receipt and RI-60 receipt and recomputes all eight short
and eight long coefficient certificates. Complete summaries and interval identities
must reconcile with RI-60. Its private row token binds the retained rows and
numerical state. Then both complete raw snapshots must pass size, MD5 and SHA-256
checks before either is parsed. The same bytes supply inspection and arrays.
The complete two-detector RI-47 crop and provenance are validated before selecting
its prefixes; private observed-state binding rejects ordinarily substituted or
mutated raw arrays, baselines or annotations before evaluation.

Check the frozen project source/dependency closure against the qualification
freeze before these commands. Reuse the source-pin command above with its program
path set to the frozen project root below. Replace the external input/output path
placeholders; both output leaves must not exist and must remain outside Git
checkouts. An optional later isolated reproduction must explicitly substitute
its own identically pinned source root.

```sh
export RI64_ACTUAL_ROOT='/Volumes/AI_DATA/development/det_8_framework-ret'
export RI64_INPUTS='/absolute/external/existing-qualified-original-pair'
export RI64_OUTPUT_PARENT='/absolute/new/external/result-parent'
RI64_ACTUAL_PROGRAM="$RI64_ACTUAL_ROOT/docs/experiments/gwosc_observed_context_v1"
test -d "$RI64_OUTPUT_PARENT"
test ! -e "$RI64_OUTPUT_PARENT/normal"
test ! -e "$RI64_OUTPUT_PARENT/optimized"

"$RI64_PY" -I -S -B "$RI64_SUPERVISOR" actual-normal \
  "$RI64_PY" -I -B "$RI64_ACTUAL_PROGRAM/process.py" \
  --qualification-report "$RI64_RUN_DIR/qualification-normal.stdout" \
  --expected-qualification-bytes "$RI64_RECEIPT_BYTES" \
  --expected-qualification-sha256 "$RI64_RECEIPT_SHA256" \
  --input-dir "$RI64_INPUTS" --output-dir "$RI64_OUTPUT_PARENT/normal"

"$RI64_PY" -I -S -B "$RI64_SUPERVISOR" actual-optimized \
  "$RI64_PY" -I -B -O "$RI64_ACTUAL_PROGRAM/process.py" \
  --qualification-report "$RI64_RUN_DIR/qualification-normal.stdout" \
  --expected-qualification-bytes "$RI64_RECEIPT_BYTES" \
  --expected-qualification-sha256 "$RI64_RECEIPT_SHA256" \
  --input-dir "$RI64_INPUTS" --output-dir "$RI64_OUTPUT_PARENT/optimized"

test ! -s "$RI64_RUN_DIR/actual-normal.stderr"
test ! -s "$RI64_RUN_DIR/actual-optimized.stderr"
cmp "$RI64_RUN_DIR/actual-normal.stdout" "$RI64_RUN_DIR/actual-optimized.stdout"
cmp "$RI64_OUTPUT_PARENT/normal/OBSERVED_CONTEXT.json" "$RI64_OUTPUT_PARENT/optimized/OBSERVED_CONTEXT.json"
cmp "$RI64_OUTPUT_PARENT/normal/PROCESSING_REPORT.json" "$RI64_OUTPUT_PARENT/optimized/PROCESSING_REPORT.json"
```

Each driver mode reuses the same caller-pinned **normal** new receipt; the two new
qualification receipts already had to match. A failed command stops the sequence.
Preserve all stdout/stderr/run records, failure JSON and any partial filesystem
artifacts without claiming success. Do not publish either accepted file if any
actual gate or the independent audit fails. Successful complete scientific outputs
are deterministic; external supervision records intentionally contain run metadata.

## 6. Fixed calculation and output meaning

For each detector, preserve binary64 values and signed zeros. The exact source
clock is `1126259446+k/4096`, never a floating GPS comparison. Use:

```text
N=2769, L=4096, T=10961
x = X[65536:68305]
w = X[61440:72401]
z = concat(X[61440:65536], X[68305:72401])
p_short = published_filter(x)
p_context = published_filter(w)[4096:6865]
p_record = unchanged_RI47_crop[:2769]
```

The central grid is `1126259462+j/4096` for `0 <= j < 2769`; its exclusive end
is `1126259462+2769/4096`. The nominal differences are exact Fractions of retained
binary64 values: `p_context-p_short` and `p_record-p_context`. Export every value,
maximum absolute difference and every maximizing index, with no magnitude test.

For each complete short/long vector, the unchanged float64 production and
independent Decimal-80 recurrence must agree within `A_x/10^9` or `A_w/10^9`,
respectively, using exact Fraction residuals and comparisons. A zero input needs
exact zero in both. No unit floor is used. This remains a complete-vector numerical
diagnostic, not an exact-operator certificate for all output coordinates.

At `I=(0,1,27,805,1384,2741,2767,2768)`, retain certified short and long output
intervals and direct `a_i*x+b_i*z` difference intervals. Signed products and sums
are exact Fractions. The direct interval must intersect the separately formed
long-minus-short interval, but the gate continues to use the direct interval;
there is no after-the-fact choice of the narrower construction. Its width must be
at most `A_w/10^12`; a zero w requires [0,0]. The three farthest-endpoint distance
bounds use limits `A_x/10^9`, `A_w/10^9` and `(A_x+A_w)/10^9`. A rounded production
point may lie outside its narrow exact-output interval and still pass the stated
distance bound. Midpoint agreement or tolerance overlap is insufficient.

No envelope M is accepted or inferred: z is the recorded context from the same
released data. No extra filter, fit, alignment, normalization, calibration,
interpolation, sign inversion, mean subtraction, taper, injection correction or
additional veto is performed. This does not compute exact F_131072 or refilter
the full record. The prior result is a rounded baseline at matching source indices.

On complete success the only two output files are:

- `OBSERVED_CONTEXT.json`, schema `ri64-observed-context-v1`: both complete
  detector records, source and receipt identities, runtime, original annotations,
  all input/output hex arrays and array identities, index grids, all Decimal
  diagnostics and rational reductions, maxima/ties and sixteen selected-row results.
- `PROCESSING_REPORT.json`, schema `ri64-observed-context-processing-v1`, status
  `all_observed_context_gates_passed`: the new receipt, complete provenance,
  detector-result identities and the exact byte identity of the first file.

The driver writes neither accepted file before both complete detector evaluations
pass. It refuses an existing output leaf, uses exclusive writes and has no
append/update/overwrite mode. Failures use a distinct stdout failure record with
`accepted_outputs=false`, stderr and nonzero exit status. Parser failures outside
normal processing can precede a structured failure record; they still do not
constitute success.

## 7. Independent export-audit contract

The following checklist was fixed before execution. A successful driver run alone
was insufficient; section 10 records the accepted independent reconciliation
and distinguishes direct recomputation from reliance on the pinned earlier
inspection. This checklist does not mean the later auditor implemented a new
complete HDF5 schema/flags parser. The required checks were:

1. Check complete byte identities, zero return codes, empty stderr and equality
   of both qualification reports, actual stdout and both scientific files. Verify
   exact source/design/dependency/runtime pins, new receipt status/coverage,
   separately bound RI-60 success and immutable RI-57 failure. Reconcile the
   processing report's exported-file hash and canonical complete-detector hashes.
2. Independently verify both raw files before parsing, then all 262144 finite
   original samples and the complete prior two-detector 8192-value crop. Validate
   the original grids, full inspection/annotation/provenance, array hashes and the
   published processing receipt before taking the baseline prefixes. Preserve the
   empty literal HDF5 Yunits and the release interpretation of nominal strain.
3. Reconcile every retained x/w/z value with its original index, both ordered
   context blocks and signed-zero injection; reconcile every p_record value with
   the unchanged crop. There are 43844 exported input values and 38536 exported
   output values, counting deliberately repeated windows/subarrays. Recompute
   canonical finite hex forms and little-endian binary64 hashes, and verify
   p_context is precisely the central 2769 values of the retained long output.
   This is export reconciliation, not an independent refiltering of observations.
4. Recompute all 11076 exact nominal differences and every maximum/tie index.
   For the 27460 retained Decimal outputs and residuals, parse each finite Decimal
   exactly, recompute binary64-minus-Decimal discrepancies, input peaks, limits,
   all maximizers and zero rules as Fractions. No extra rounding or unit floor may
   enter this audit. Do not turn these diagnostics into exact full-vector bounds.
5. Validate all sixteen selected-row identities, direct/short/long intervals,
   decomposition intersections, exact widths and the 48 endpoint-distance gates.
   Recompute endpoint distances from unchanged exported production points. Check
   all peaks/limits against the exported exact dyadic inputs and preserve the
   direct interval used by the width gate. Check no M, statistical score, fit or
   unexamined-row certificate has appeared.
6. Distinguish arithmetic reconciliation from independent dot-product verification.
   The scientific export retains coefficient-enclosure identities and interval
   results, not the complete coefficient vectors. Those identities alone do not
   let an auditor recompute `s*x`, `v*w` or `a*x+b*z`. Unless the exact coefficient
   intervals were also retained/reconstructed and reduced by an independently
   implemented reducer, the dot enclosures rely on source review plus the two
   reproduced engine/consumer executions. State that limitation explicitly.

The complete bound reports and accepted independent audit support the rounded
summary in section 9. The reported differences, numerical diagnostics and selected
bounds are finite-processing quantities, not detection or calibrated error
estimates. Section 10 states which quantities were independently recomputed and
retains the coefficient-vector limitation.

## 8. Interpretation and retained warnings

Keep the full original quality, injection, missingness and DATA-exclusion
annotations. H1's NO_CW flag is set throughout; L1's is clear throughout. L1's
samples remain included with this unchanged warning:

> L1 NO_CW_HW_INJ flag is clear throughout input interval; samples retained.
> Injection absence and negligible effect are not claimed.

An injection flag is not missing data. Dimensionless nominal strain is the release
interpretation, not an inference from the empty Yunits attribute. The nearby
[RI-40 calibration summaries](../gwosc_calibration_qualification_v1/QUALIFICATION.md)
are statistical summaries, not a deterministic joint envelope, and this consumer
applies no calibration correction. The independently qualified NR illustration
remains separate: observed surroundings cannot fill its missing physical
continuation, and no V1-to-V2 alignment premise is resolved here.

There is no new detection, residual statistic, noise or confidence estimate,
calibrated arrival/amplitude/phase claim, withheld prediction, DET-versus-GR test,
native detector forward map or gravity proof. The native research lane stays
separate and RET remains paused. A later figure requires a separately assigned,
reviewed export-only renderer; no renderer is part of these three files.

The original public-data attribution remains attached through the
[GW150914 release DOI](https://doi.org/10.7935/K5MW2F23) and
[GWOSC technical release details](https://gwosc.org/techdetails/).


## 9. Completed execution evidence

The coordinator froze the qualification closure on **2026-09-24 at
08:48:15.624269 UTC**. Both new consumer runs completed with schema
`ri64-consumer-qualification-v1`, status `all_consumer_gates_passed` and exactly
**75 passes, zero failures**. Their complete receipts are byte-identical. The
coordinator's qualification audit confirmed the fixed inventory, all subcounts,
runtime/source pins and absence of observed access. The separately recorded
independent qualification audit was accepted before the actual freeze at
**08:50:22.370210 UTC**. The old RI-60 196-gate receipt was bound and validated,
not re-executed as 196 new RI-64 gates.

The frozen operational budgets stayed at 1800 seconds and 2097152 KiB sampled
RSS for every process. Runs were serial. All four returned code zero, had empty
stderr and no watchdog stop reason. The elapsed times below are rounded display
values from the external receipts; RSS is the maximum sampled process resident
set, not a hard peak or a whole-system measurement.

| Run | Elapsed seconds | Maximum sampled RSS, KiB |
|---|---:|---:|
| Qualification, normal | 4.180 | 166608 |
| Qualification, optimized | 4.967 | 184480 |
| Actual driver, normal | 463.330 | 339248 |
| Actual driver, optimized | 466.083 | 347792 |

Each actual mode recomputed and reconciled all sixteen coefficient certificates
before its observed access, then reported `all_observed_context_gates_passed`.
Both detector records passed; all sixteen selected-row results and their 48
endpoint gates passed. The two actual stdout receipts match (361 bytes,
SHA-256 `1d26f2dd046db19c46d0a791ec75a278276b9cdf8f5bf140ef6e6fad6735e179`).
The two complete scientific files also match across modes:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| New `QUALIFICATION_REPORT.json` content | 33132 | `56aa06c442384bd6249875443930202e09e874b4318aa995a8b7bb6dec1dab1b` |
| `OBSERVED_CONTEXT.json` | 13189579 | `d9d094b7851ed97b732a142d3130c12d8420bdb6420921a211e3031c8a9bbfc4` |
| `PROCESSING_REPORT.json` | 42247 | `8edfe1bd235a22ad308d1e086dacd9bbe7ac02cfbfc09240878ff5e05ab05869` |

The new qualification receipt was retained during execution as
`runs/qualification-normal.stdout` and its identical optimized counterpart;
the table specifies content identity independently of its eventual publication
filename. Scientific artifacts have no execution paths, elapsed times or changing
timestamps in their deterministic contents.

The following descriptive maxima are read from the complete exported exact
binary64-difference reductions, with display rounded to seven significant digits.
They are nominal dimensionless-strain differences under fixed finite filters,
not calibrated waveform errors or evidence about gravity. Each listed maximizing
index is unique in its retained array; the export carries all indices in general.

| Detector | Maximum absolute context-minus-short difference | Central / original source index | Maximum absolute record-minus-context difference | Central / original source index |
|---|---:|---|---:|---|
| H1 | 1.300145e-20 | 2762 / 68298 | 4.604740e-23 | 469 / 66005 |
| L1 | 1.711427e-20 | 2762 / 68298 | 5.517297e-23 | 469 / 66005 |

The exact maxima, before display rounding, are respectively:

- H1 context-minus-short:
  `1106041100950380831/85070591730234615865843651857942052864`.
- L1 context-minus-short:
  `363980328484469743/21267647932558653966460912964485513216`.
- H1 record-minus-context:
  `1958639687963745/42535295865117307932921825928971026432`.
- L1 record-minus-context:
  `2346798630243793/42535295865117307932921825928971026432`.

The two source locations have exact clocks `1126259462+1381/2048` and
`1126259462+469/4096`. In this prescribed comparison, the context-minus-short
maximum is larger than the record-minus-context maximum for both detectors.
Its maximizing point is near the short segment's right edge. That is a concrete
finite-boundary effect in these retained results; it does not establish that more
context always improves an estimate or that the full-record baseline is correct.
There is no pass/fail limit on these descriptive difference magnitudes.

For compact numerical reporting, the next table gives **upward-rounded upper
bounds** computed from the exported exact ratios. The two full-vector columns
are maximum production-versus-Decimal residual divided by that input's peak;
their fixed limit is `1e-9`. The direct-width column is the largest of the eight
selected direct interval widths divided by A_w; its limit is `1e-12`. The last
column is the largest of the 24 selected endpoint-distance bounds divided by
its own fixed tolerance; its limit is one. These different columns must not be
read as interchangeable error measures.

| Detector | Short Decimal residual / A_x | Extended Decimal residual / A_w | Selected direct width / A_w | Selected endpoint bound / its tolerance |
|---|---:|---:|---:|---:|
| H1 | 3.348737e-15 | 4.881727e-15 | 1.147079e-57 | 1.453307e-6 |
| L1 | 5.006590e-15 | 5.278820e-15 | 2.487565e-57 | 3.531815e-6 |

The very narrow rational enclosure widths concern the exact finite operator;
they do not establish that the rounded production outputs have errors of those
widths. The retained endpoint bounds are the separate actual-specific statement
about production at the eight selected coordinates. Neither statement is a
calibration uncertainty interval or a proof for unexamined coordinates. Both
actual input peaks are nonzero, and the unchanged L1 CW warning remains attached.

The original external execution bundle is
`/var/folders/47/s7fm88bn5ql2tw7j103kbyzr0000gn/T/det-ri64-observed-czgvxzy2`.
Its retained paths are `candidate/` for the qualification copy, `runs/` for all
four command/return/resource/stdout/stderr records, and `results/{normal,optimized}/`
for actual exports. The actual command used the unchanged project
`docs/experiments/gwosc_observed_context_v1/process.py`, the caller pin shown in
section 4, and the existing original-pair input directory
`/var/folders/47/s7fm88bn5ql2tw7j103kbyzr0000gn/T/det-ri37-gwosc-zdmry2a0/inputs`.
These temporary execution paths document this run; they are not durable custody
or fresh destinations for replay.

The reviewed external launchers were `run_qualification.py` (2559 bytes,
SHA-256 `3c534da454034a200b0302eb41631d09852999e4c24c7fc64cda47bb90d2b8d1`)
and `run_actual.py` (3705 bytes,
SHA-256 `c7f3bbcc29045f27cee6cee6331118a1f57d49d1cbbe37d1e67d6ddc59f60717`).
The supervisor was 2881 bytes,
SHA-256 `7398c77948f2ed37a5fdfc09bdf0151febacfed56899a427575b900dea5856cb`.
They checked the source closure, prospective guide, both launchers and supervisor
before and after each mode. The supervisor alone owned the resource watchdog and
child cleanup; there was no outer timeout that could orphan its scientific child.
Replay summaries were created exclusively. The actual launcher rehashed original
raw inputs and observed predecessors only after a clean successful driver return.

Additional retained evidence identities are:

| External record | Bytes | SHA-256 |
|---|---:|---|
| `qualification_freeze.json` | 4432 | `745ceaeeb1c53b00364af871b47f10a53479e8d1fd57c9fbbacdfff5ec0c4867` |
| `actual_freeze.json` | 5755 | `ff167e29c5c4c812b5ea015500ba3b8d944050fad025f68cdba4a044f3021048` |
| `qualification_replays.json` | 306 | `e433f05582a093c3360b5f26887ad3e8ec61bfe27ea9b72013979da68bd0a208` |
| `actual_replays.json` | 792 | `e2496970d31f05f61ac23f8068a241ba7e91d1763fe64e9f49b2d1f2bd0586d5` |
| `root_qualification_audit.json` | 456 | `1a167e262260ecbca16ccdde9824ddf73bb7dc9bb91bd29b5c14b05c6af0ee96` |

The qualification replay summary's original `independent_adjudication_pending`
field records its status when created. It was followed by the accepted root and
independent qualification audits and the actual freeze. Do not rewrite that
historical record. The actual replay summary likewise retains its original pending field; it was
subsequently followed by the accepted independent actual audit in section 10. The actual freeze separately records the accepted
independent qualification audit identity (3628 bytes,
SHA-256 `a45bc198c5d617b10efee11b45b19fd1cd78aa3288f829c7e21f1f4db59744d1`).

## 10. Accepted independent actual export audit

An independently authored preserved-output audit passed in normal and optimized
modes, with zero exit codes, empty stderr and identical **14516-byte** reports:
SHA-256 `9ff31647206675389a8ab70e5212e0cda73cb40a06f2b4f7f0074b3df2e0a1df`.
Their external paths are
`/tmp/det-ri64-report-audit/actual-normal-audit.json` and
`/tmp/det-ri64-report-audit/actual-optimized-audit.json`.
The reported tool wall times were 0.976896333 and 1.062890291 seconds. These are
audit timings, not filter-execution timings.

The audit source was 25217 bytes, SHA-256
`4b093aab9ff0f00c605548c13c28063f52ae5cd278e2d55d12caa672a7d45726`.
The 806-byte execution receipt `actual-audit-execution.json` has SHA-256
`5c1e7b113fb2bd30b7567dc170fbd18c22378cab7a3ae3874a3b055adab77409`.
The separate 8504-byte `actual-effect-summary.json` has SHA-256
`63b3b870461aef77dbbeca17d0140f16f8ac44c0c39abaad88a41235e1b59533`;
it is a display summary of independently audited exact values, not additional
scientific gates. Both records are in the same external audit directory.

The audit independently bound both complete original raw snapshots before HDF5
parsing and matched all **43844 exported x/w/z coordinates** to their original
values and indices. It checked the complete unchanged RI-47 crop and all
**5538 retained baseline-prefix coordinates**, with the same nominal grid and
original detector annotations. It re-read the full finite strain arrays and
checked their binary64 identities. For complete schema, grid, attributes and
flag-dataset evidence, however, it reused the pinned RI-37 inspection tied to the
verified whole-file bytes and checked the exported annotations against that
record; it did not independently re-read every HDF5 attribute or flag dataset.
It reconciled **27460 retained Decimal/residual pairs**, **11076 exact nominal
differences**, all maxima and ties, **sixteen selected width gates** and **48
endpoint-distance gates**. Source, runtime, qualification and published dependency
identities matched; both full output modes and the processing-report/export
binding agreed. The unchanged L1 CW warning was preserved.

The independent audit rechecked exact arithmetic on retained Decimal and
binary64 outputs; it did **not** rerun the production filter or Decimal
recurrences. It also did not reconstruct the unexported coefficient vectors or
independently recompute their dot products. Consequently, the certified dot
intervals continue to rely on the reviewed method, qualified engine and two
reproduced source-bound executions; their widths, intersections and endpoint
gates were independently reconciled. Actual access order likewise relies on
the reviewed source and controlled custody tests, rather than being inferred
solely from output metadata. No independent refiltering, all-coordinate exact
production bound, uncertainty model or native-geometry conclusion is claimed.

The coordinator and a separate reviewer accepted this final documentation
against the frozen execution and independent audit evidence. Publication records
its final identity separately from the original execution-guide identity. All
prospective source pins, thresholds and resource limits remain unchanged.
