# RI-78 — fixed off-event descriptive spectra of the GW150914 V2 pair

24 September 2026 UTC. **Prospective design independently accepted for
implementation and fabricated qualification.**
No observed spectrum, new strain-amplitude read, implementation or numerical
qualification is claimed by this packet. Its next milestone is a reviewed
implementation qualified on fabricated inputs, followed by a separately frozen
application to the already selected public files. This is an actionable step in
[ME-02](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md), with no
new user permission needed for authorized continuation through those gates.

## 1. Observable, inputs and access history

Compute four descriptive power spectral densities (PSDs), one per detector and
side, and their amplitude spectral densities (ASDs). Use the released nominal
strain directly, without the RI-47 display filters, calibration correction,
alignment, subtraction, whitening, frequency selection or fitting. The output
units are nominal strain squared/Hz and nominal strain/sqrt(Hz). The literal
HDF5 strain `Yunits` attribute remains empty; dimensionless calibrated strain
is the release interpretation already qualified in
[RI-37](../gwosc_input_qualification_v1/QUALIFICATION.md).

| Detector / exact public source | Bytes | SHA-256 |
|---|---:|---|
| H1 / [H-H1_LOSC_4_V2-1126259446-32.hdf5](https://gwosc.org/GW150914data/H-H1_LOSC_4_V2-1126259446-32.hdf5) | 1040592 | `6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6` |
| L1 / [L-L1_LOSC_4_V2-1126259446-32.hdf5](https://gwosc.org/GW150914data/L-L1_LOSC_4_V2-1126259446-32.hdf5) | 1007420 | `56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189` |

Publisher MD5 values remain `50441a42c13fc1f14e5c4ea5527f1515` (H1) and
`361ae6a040a9fef7897b1e0124d5b0a1` (L1). No alternate revision or longer record
is admitted. Each `/strain/Strain` dataset has 131072 float64 samples on the
declared grid `GPS 1126259446 + i/4096`, `0 <= i < 131072`.

Durable input custody was recovered by new acquisitions of identical bytes,
not by restoration of historical execution receipts. The current external root
is `/Volumes/AI_DATA/development/det-review-evidence/ri37-input-recovery-20260924T221315Z-9ac44e02`;
the two files are in `inputs/`. Its `INPUT_RECOVERY_HANDOFF.json` has SHA-256
`be0b518ca43e423d7e2a737b85eec0cad119a1b4cbd19ed4f056f662277d2dc0`.
The unchanged RI-37 inspector in normal and optimized modes reproduced the
published `INPUT_REPORT.json` identity
`a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80`.
Future execution must recheck these identities; this path is a locator, not
permission to accept whatever bytes later occupy it.

These are familiar public development inputs. Prior metadata inspection,
nominal waveform display and context comparisons are known; the side selection
below is not blind or protected validation. Its one-second exclusion is inherited
from the [previously declared display crop](../gwosc_nominal_display_v1/RECIPE.md).
“Off-event” names that exclusion only. It does not assert signal-free samples,
noise stationarity or a measured absence of injections.

Retain both detectors with their full RI-37 flags. Every DQ mask is 127; H1's
injection mask is 31 and L1's is 23. In particular, **L1 `NO_CW_HW_INJ` is clear
throughout all 32 seconds**: the flags do not establish absence of continuous-wave
hardware injections. This known clear bit is retained and labeled, not treated
as missing data or changed to a pass. No injection frequency or effect is
inferred. Missing flags or disagreement with the qualified bytes must refuse.

## 2. Frozen indices and finite statistic

Use integer sample indices; convert times only by the exact rational rule above.
Set `fs=4096 Hz`, segment length `M=16384` (4 seconds), stride `H=8192`
(2 seconds), and `delta_f=fs/M=1/4 Hz`. Exclude `[65536,69632)` in each detector.
The sides and complete segment starts are:

| Side | Half-open interval | Complete starts | Count |
|---|---|---|---:|
| left | `[0,65536)` | `0,8192,16384,24576,32768,40960,49152` | 7 |
| right | `[69632,131072)` | `69632,77824,86016,94208,102400,110592` | 6 |

For a side `[a,b)`, starts are `a+rH`, with
`0 <= r <= floor((b-a-M)/H)`. Thus the counts are
`1+floor(49152/8192)=7` and `1+floor(45056/8192)=6`.
Every segment is `[start,start+M)`. The left last segment ends at 65536; the
right last ends at 126976. The right tail `[126976,131072)` contains 4096 unused
samples. Do not pad it, change stride to use it, concatenate sides, or let a
segment cross the excluded interval. No observed value changes these choices.
There are 13 segments per detector and 26 periodograms in total.

For a segment `x_j`, `0 <= j < M`, define

```text
mu = (1/M) sum_j x_j
d_j = x_j - mu
w_j = (1 - cos(2*pi*j/M))/2                 (periodic Hann)
v_j = w_j*d_j
W2 = sum_j w_j^2
Z_k = sum_j v_j exp(-2*pi*i*j*k/M)          (unscaled forward DFT)
c_0 = c_(M/2) = 1; c_k = 2 for 0 < k < M/2
P_s[k] = c_k*|Z_k|^2/(fs*W2)
P_side[k] = (1/K) sum_s P_s[k]
ASD_side[k] = sqrt(P_side[k]).
```

All 8193 bins are retained: `k=0,...,8192`, `f_k=k/4 Hz`, including DC and
2048 Hz Nyquist. Demean before applying the window. Do not detrend a whole
side, remove a fitted slope, average ASDs, use a median, discard bins or pool
detectors/sides. Overlapping segments are not asserted independent. Unequal
7/6 counts are retained, without reweighting them into a combined statistic.

The primary implementation must use real CPU binary64 arrays, explicit ordered
segment extraction, `mean(..., dtype=float64)`, the stored binary64 window,
`numpy.fft.rfft(..., n=M, norm="backward")`, and the above density formula.
Construct the window once with SciPy 1.14.1 `windows.hann(M, sym=False)`;
retain its full binary64 array and identity. Compute the execution denominator
from that array, using binary64 summation; do not replace it by its analytic
ideal. The side average is the arithmetic binary64 mean of ascending-start
periodograms. No extension or zero padding occurs.

The [SciPy 1.14.1 Welch specification](https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.signal.welch.html)
supports explicit windows, density scaling and arithmetic averaging. Its
[version-pinned implementation](https://raw.githubusercontent.com/scipy/scipy/v1.14.1/scipy/signal/_spectral_py.py)
confirms complete-window extraction, detrending before multiplication, window
energy normalization and doubling only interior bins for even length. The
[Hann specification](https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.signal.windows.hann.html)
distinguishes `sym=False` periodic windows from the symmetric default; the
periodic definition here uses denominator M. The
[NumPy 2.1 rFFT specification](https://numpy.org/doc/2.1/reference/generated/numpy.fft.rfft.html)
fixes the transform convention and unique even-length Nyquist endpoint.

## 3. Independent identities and qualification fixtures

Finite Fourier orthogonality gives `sum(w)=M/2` and `sum(w^2)=3M/8` for this
ideal periodic Hann. Parseval and the endpoint weights give the exact identity

```text
delta_f * sum_k P_s[k] = sum_j (w_j*(x_j-mu))^2 / W2 = Q_s.
delta_f * sum_k P_side[k] = (1/K) sum_s Q_s = Q_side.
```

This is window-weighted demeaned power, not ordinary unwindowed sample variance.
The finite Fourier identity is mathematical; numerical satisfaction of a
tolerance is a separate check, not a proof of a floating-point enclosure.

Before any observed calculation, qualify the exact production-size M with
the following fixed fixtures, using amplitudes `A=1` and `A=2^-70`. No random
search, observed scaling or tolerance tuning is needed.

| Input | Exact ideal one-sided nonzero PSD values | Integral Q |
|---|---|---|
| zero, constant `+A`, constant `-A` | all zero after demeaning | 0 |
| repeating `[A,0,-A,0]` cosine, `k0=M/4` | bins `k0-1,k0,k0+1`: `(A^2*M/fs)*(1/12,1/3,1/12)` | `A^2/2` |
| repeating `[0,A,0,-A]` sine, `k0=M/4` | the same three values | `A^2/2` |
| alternating `+A,-A` (Nyquist cosine) | bins `M/2-1,M/2`: `(A^2*M/fs)*(1/3,2/3)` | `A^2` |
| `A*cos(2*pi*j/M)` (lowest nonconstant cosine) | bins `0,1,2`: `(A^2*M/fs)*(1/6,1/3,1/12)` | `7*A^2/12` |

For interior tones, multiplication by Hann spreads the amplitude to the tone
and its two neighbors, yielding those three powers. At Nyquist, the unique
endpoint has weight one. For the lowest cosine, windowing creates a constant
term `-A/4`. **Demeaning before Hann does not force the final DC bin to zero.**
These endpoint fixtures catch DC/Nyquist doubling and reversed detrending order.
Only the dyadic constant/zero fixtures demand bitwise numerical zeros; ideal
zero bins of a nonconstant tone use the tolerance below for window/trigonometric
rounding. Generate the quarter-rate and Nyquist patterns exactly rather than
using large trigonometric arguments. Use small arguments for the lowest cosine.

Also use a separately authored direct DFT on lengths `m=8` and `m=16`, each
with `fs=4096`, its own periodic Hann and `delta_f=fs/m`. For each m use zeros,
constant one, a unit impulse at index 1, the dyadic sequence
`x_j=((j mod 5)-2)/4`, and the exact quarter-rate cosine pattern. Compute its
real/imaginary sums using scalar sine/cosine and `math.fsum`; do not call an FFT,
Welch, or the primary periodogram helper in that reference. Compare every bin
and the time-domain identity. This small direct DFT is an independent algorithm,
not exact-real arithmetic. The analytic fixtures supply independent ideal
normalizations; the production-size checks retain the actual transform length.

An aggregation fixture with two periodograms `P` and `4P` must yield `2.5P`
and `sqrt(2.5P)`. It distinguishes the specified ASD from `1.5*sqrt(P)`.
Check amplitude-squared PSD scaling and absolute-amplitude ASD scaling across
the two fixed amplitudes. Index fixtures must establish the two start lists,
counts, excluded interval and unused tail independently of the production
iterator. Refusal fixtures cover a wrong input pin, absent/changed flags,
nonfinite values, malformed dimensions, empty or short windows and wrong bins.

## 4. Frozen numerical consistency budget and conventional cross-check

Set `eps=2^-52`, `tau=4096*eps=2^-40` before observed execution. This chosen
binary64 reproducibility budget allows accumulated transform/window/reduction
rounding at the fixed length. It is **not a certified worst-case error bound,
confidence interval, calibration allowance or model-error tolerance**.

Independently accumulate `W2_ref=math.fsum(w_j*w_j)` and
`Q_s=math.fsum(v_j*v_j)/W2_ref` from the retained binary64 window and demeaned
segment, without obtaining Q from any spectrum. Recompute the segment mean
with `math.fsum(x_j)/M` and check the primary mean within
`tau*max_j(abs(x_j))`; zero input requires exactly zero. Check both window
sum identities against their ideal values with relative budget tau, and check
the window against its explicitly evaluated periodic formula within `16*eps`
in dimensionless absolute value. Record discrepancies, not only pass booleans.

For each segment or side set `Q=Q_s` or
`math.fsum(Q_s)/K` respectively and `S=Q/delta_f`. Check every bin against each
applicable independent/reference PSD with `abs(P[k]-P_ref[k]) <= tau*S`.
Check Parseval with `abs(delta_f*math.fsum(P)-Q) <= tau*Q`. For analytic tone
fixtures use the independently derived ideal Q in the tolerance scale when
comparing to their exact ideal spectra; additionally run numerical Parseval.
Use the same rule at m=8/16 with that fixture's delta_f. No peak-bin-only check,
relative division by nearly zero bins, `max(1,power)`, or fixed strain-unit floor
is permitted. All bins, including theoretically zero bins, remain in the test.

If Q is zero, require every windowed value and every PSD/ASD value to be exactly
zero. If a nonzero windowed vector produces Q=0, refuse as underflow. For Q>0,
require Q, S and both tolerance scales to be finite and strictly positive;
unexpected numerical underflow/overflow or nonfinite intermediates refuse.
Ill-conditioned nearly constant inputs may fail this budget. Preserve that
failure rather than enlarging the scale, dropping bins or clipping outputs.

Require PSD and ASD arrays finite and nonnegative. Independently check each
ASD against `math.sqrt(P_side[k])`: exact zero if P is zero; otherwise absolute
error at most `8*eps*sqrt(P)`. For the conventional cross-reference ASD use
`abs(ASD-ASD_ref) <= sqrt(tau*S)+8*eps*sqrt(S)`, following
`abs(sqrt(p)-sqrt(q)) <= sqrt(abs(p-q))` and allowing square-root rounding.
The direct pointwise sqrt gate remains required; the looser near-zero
cross-reference gate cannot replace it.

Run SciPy 1.14.1 `signal.welch` on each **entire fixed side slice**, with every
parameter explicit: `fs=4096`, `window=stored_window`, `nperseg=nfft=16384`,
`noverlap=8192`, `detrend="constant"`, `return_onesided=True`, `scaling="density"`,
`axis=-1`, `average="mean"`. This independently checks the complete-window
selection and dropped tail through the public API. Also compare each segment
against the same explicit call with `noverlap=0`. Frequencies must equal k/4
exactly and every PSD bin must satisfy the applicable budget. NumPy/SciPy FFT
agreement is a conventional API cross-check, not a claim of independent FFT
engines; their implementations share PocketFFT lineage
([NumPy implementation](https://raw.githubusercontent.com/numpy/numpy/v2.1.3/numpy/fft/_pocketfft.py),
[SciPy backend](https://raw.githubusercontent.com/scipy/scipy/v1.14.1/scipy/fft/_basic_backend.py)).
The analytic identities, small direct DFT and source review provide additional
independent checks.

## 5. Retained result contract

Future output consists of a deterministic UTF-8 JSON result, separate execution
receipts, and a complete external artifact manifest. JSON uses sorted keys,
indent 2, one final newline, no duplicate keys, NaN or Infinity. All scientific
binary64 scalars/arrays are finite Python `float.hex()` strings, preserving
signed zero. Integer indices, counts and byte lengths are JSON integers.
Array records have `dtype="<f8"`, `shape`, row-major `values_hex`, and SHA-256
of the corresponding C-order little-endian binary64 bytes. Binary array
snapshots are retained too; hashes do not substitute for the arrays.

The closed scientific top-level fields are `schema`, `method`, `inputs`,
`frequency_hz`, `window`, `detectors`, `checks`, and `limitations`, with
`schema="ri78-off-event-spectra-v1"`. The future implementation must freeze the
complete nested validator before observed execution; its required field content
is fixed here:

- `method`: this design identity, fs/M/stride/nfft, exact exclusion/side intervals,
  ordered starts, bin/endpoint weights, detrending/window/FFT/scaling/averaging
  conventions and eps/tau/sqrt budgets; no selectable algorithm or band.
- `inputs`: H1 then L1 records with exact filename, URL, bytes, MD5, SHA-256,
  dataset path/dtype/shape, GPS/grid and literal unit metadata. Embed the full
  admitted RI-37 detector metadata/flag records, retaining raw 32-element masks,
  names, descriptions and every set/clear interval. Bind the inspector report
  and the new recovery handoff by identity; distinguish acquisition generations.
- `frequency_hz`: all 8193 values k/4 in ascending k; `window`: all 16384 values,
  its byte identity, actual sum and W2, independent sums and ideal-check errors.
- `detectors`: exactly H1 then L1, each with sides `left` then `right`. Each side
  retains its interval, count, starts, used/unused intervals and 7 or 6 segment
  records. Each segment has start/end indices, rational GPS offsets with
  denominator 4096, the four intersecting 1 Hz flag-row indices and their raw
  masks, scalar mean, raw/de-meaned/windowed array byte hashes, Q, and **all
  8193 PSD bins**. Preserve each raw segment's provenance through the retained
  complete HDF5 and indices; retain demeaned/windowed binary arrays externally.
  Each side also has all-bin mean PSD, all-bin ASD, Q_side, and units. No detector
  stack, side average, selected peaks or fitted summaries are added.
- `checks`: named expected/actual dimensions, indices and exact identity gates;
  per-segment/side Parseval residuals and thresholds; complete conventional
  reference PSD arrays with identity and all-bin comparison residuals/limits;
  mean/window/sqrt checks; and the separately identified fabricated qualification
  report pin. Qualification results cannot be labeled observed findings.
- `limitations`: literal prior-access/public-development status, nominal
  calibration, L1 injection caveat, short overlapping unequal-count records,
  descriptive-only scope, and the outstanding requirements in section 7.

Keep a separate custody manifest binding every output and source with path,
bytes and SHA-256. It records source/helper/package/runtime/window pins, frozen
launch arguments/environment, input snapshots, canonical schemas, qualification
reports and normal/-O comparisons. Mode, wall time, host paths, resource usage,
stdout/stderr identities and failures belong in receipts, outside scientific
JSON, so deterministic result bytes can be compared exactly across modes.
No plot, rounded table or selected frequency range can replace complete arrays.

## 6. Implementation, execution and failure boundary

Implementation follows review of this design. First freeze primary, direct-DFT,
qualification and result-validator source with their imported helper closure;
retain a source review and fabricated normal/-O evidence. Use the recovered
qualified CPython 3.11.6, NumPy 2.1.3, SciPy 1.14.1, h5py 3.12.1 and HDF5 1.12.2
runtime, with the full platform/build/library fingerprint matched to
[RI-60's report](../gwosc_context_operator_v2/QUALIFICATION_REPORT.json)
(SHA-256 `1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f`).
The current executable is
`/Volumes/AI_DATA/development/det-review-evidence/ri73-recovery/recovery-20260924T212511Z-2403d37c/env/bin/python`.
Version strings alone do not replace that fingerprint. Freeze the actual
binary64 window and source/runtime closure before observed access.

After independent qualification and coordinator adjudication, freeze exact
read-only input snapshots, method/source/report identities, exclusive durable
output paths, commands, environment and limits. Then apply normal and `-O`
modes serially with `-I -B`; explicit runtime errors must survive optimization.
Set numerical worker counts to one in the recorded launch environment. Budget
each complete process at 180 seconds wall time and a 512 MiB sampled resident
memory threshold. A supervisor polls at intervals no greater than 0.1 seconds,
terminates on deadline or sampled RSS above the threshold, and records elapsed
time, samples and their maximum. This sampled monitor is not an OS-enforced
hard memory cap and may miss a shorter transient peak; report that limitation.
Retain raw receipts on failure; do not silently retry with larger budgets or tune
the method. This is a small 26-segment calculation, not a new escalating
qualification campaign.

Before HDF5 parsing, snapshot/check complete input sizes and hashes. Parse
those same snapshots, replay the unchanged RI-37 metadata/flags/finite-data
admission, and require its published report identity. Explicitly enforce every
segment and bin count, finite input/intermediate/output and schema/flag gate.
Refuse missing dependencies, changed source/runtime/data identities, unexpected
source/data/output symlinks or changed resolved path targets, output overwrite,
empty windows and any failed tolerance. The admitted named venv interpreter
may itself be a symlink: freeze its named path, resolved target chain and target
bytes together with the full runtime fingerprint, and refuse changes to that
binding. Do not prohibit or silently re-resolve that already declared symlink.
Never silently shorten segments, mask a detector, replace a missing flag or
alter an accepted threshold. Record L1's expected clear bit as retained context.

Reopen source/input identities after each run. Normal and optimized scientific
results must be byte-identical under the frozen environment; receipts remain
separate. An independent reviewer checks the complete all-bin evidence and
identities before the coordinator publishes the result. A successful run earns
only the bounded claim defined here. A failed run remains useful evidence and
must identify its precise gate; its failure cannot authorize an inference or a
method revision. Proposed repairs are reviewed before any new observed run.

## 7. What this advances and what remains open

This produces an auditable conventional spectral description on the exact
public V2 data already used by the project. The historical
[official GWOSC tutorial](https://gwosc.org/s/events/GW150914/GW150914_tutorial.html)
uses a different full-record, one-second FFT PSD route on its old V1 inputs.
Our four-second, two-side V2 calculation is an explicitly declared adaptation,
not an exact reproduction of that tutorial, its whitening, or the discovery
paper. A future exact-baseline claim must name and freeze its own matched
version, data, parameters and observable; this packet invents no agreement target.

Short, overlapping periodograms describe the selected records. They do not
establish a population detector-noise PSD, Gaussianity, stationarity, effective
degrees of freedom, detector independence, sampling uncertainty, a signal-free
interval or the negligible effect of L1's injection flag. Those are premises or
empirical questions for a later explicitly scoped noise design. This estimated
PSD must not replace known covariance in the
[RI-67 theorem](../gwosc_context_noise_v1/DESIGN.md), or be identified with
[RI-71/73 unit-white covariance](../gwosc_noise_operator_covariance_v1/DESIGN.md).
No whitening, SNR, chi-square, likelihood, residual significance or detection
claim follows. No ratio/fit of the side spectra is a hidden additional statistic.

[RI-40's nearest-time C02 summaries](../gwosc_calibration_qualification_v1/QUALIFICATION.md)
remain pointwise uncertainty summaries, not a joint frequency/time response
law or deterministic calibration envelope. Their known time offsets and
limitations, including no calibration interpretation below 10 Hz, remain.
Retaining DC through Nyquist is a finite numerical specification; it supplies
no additional calibrated physical meaning at unsupported frequencies. No
extra response correction, calibration draw or timing offset is inferred.

A calibrated transient comparison still needs a specified mean/template,
detector response and timing convention, analysis selection, and a justified
noise/estimation-uncertainty treatment. The scalar NR illustration does not
supply that closure. A DET gravity/geometry comparison additionally needs its
native quantitative forward observable and premises. Conventional public-data
progress does not settle that separate proof question or resume RET.

## 8. Design adjudication

The coordinator and an independent measurement reviewer read the complete
design, reconciled the fixed indices and existing input/flag/runtime premises,
and checked the analytic normalization, endpoint fixtures and frozen numerical
budgets. The independent reviewer separately derived the fixture identities and
checked the cited version-specific primary sources. Two execution-wording
findings were resolved before acceptance: preserve the admitted interpreter
symlink binding and describe sampled RSS honestly. Neither changed the statistic,
tolerances or input population.

The reviewed author version was 23044 bytes, SHA-256
`b725ac0aa015459bfe53354b9d676abd21e1a70b5b14248b8849fac821db50cb`.
Independent evidence is retained as `FINAL_DESIGN_REVIEW.json`, 8520 bytes,
SHA-256 `5647e676ae7611ec8c96b2f80117377423f2a1a59fe0d58df9de760cfab462c8`,
under `/Volumes/AI_DATA/development/det-review-evidence/ri78-independent-method-20260924T223957Z-58083398/`.
Root added only this adjudication and the opening acceptance status afterward.
No numerical fixture or observed spectrum has yet been executed in this packet.
RI-80 implements and qualifies this fixed design before the separate actual-data
freeze; acceptance here is not acceptance of an unseen implementation or result.
