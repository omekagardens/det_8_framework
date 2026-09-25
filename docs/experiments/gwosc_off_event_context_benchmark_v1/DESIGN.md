# RI-104 — observed context discrepancy on the fixed off-event windows

25 September 2026 UTC. **External source-only proof and prospective design.**
No new strain values, coefficient intervals or application-result values were
decoded to prepare this note. No scientific code, filter, transform or numerical
fixture was run. The already accepted RI-100 saved audit and source/metadata
documents were read. This note awaits independent and root review; it supplies
neither execution authorization nor an observed result.

The practical question is: **on the same thirteen surrounding windows already
used for each detector's descriptive spectra, how large is the prescribed
long-context-minus-short processing discrepancy at the eight fixed coordinates,
and how much changes after centering these finite observations by side?** The
four accepted RI-100 proxy trace intervals provide a fixed conditional scale
alongside those measurements. They are not empirical acceptance bands.

This is the next bounded ME-02 application in the
[measurement plan](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md).
It uses existing public data and the accepted finite conventional filter. It
does not propose another trace-enclosure refinement, a new covariance fit,
reselected windows, a signal-template comparison or a native forward law.

## 1. Exact inputs, inherited map and the minimum missing custody step

Use only the same RI-37 GW150914 V2 H1/L1 pair, with 131072 finite binary64
samples per detector and clock `GPS 1126259446 + j/4096`. The two already
recovered files are under
`/Volumes/AI_DATA/development/det-review-evidence/ri37-input-recovery-20260924T221315Z-9ac44e02/inputs/`.

| Detector / filename | Bytes | SHA-256 |
|---|---:|---|
| H1 / `H-H1_LOSC_4_V2-1126259446-32.hdf5` | 1040592 | `6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6` |
| L1 / `L-L1_LOSC_4_V2-1126259446-32.hdf5` | 1007420 | `56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189` |

The publisher MD5s remain `50441a42c13fc1f14e5c4ea5527f1515` and
`361ae6a040a9fef7897b1e0124d5b0a1`. These are expected historical identities,
not a claim that this design reread either file. Future custody must freshly
bind both complete byte snapshots before either HDF5 parse, retain them, and
use those same snapshots for the unchanged RI-37 inspector and strain reads.
Require the full inspector result to equal its pinned accepted report, not
merely selected dimensions or flags. The recovery handoff is a retained new
acquisition of identical old bytes, not a recreated historical receipt.

Retain literal blank `Yunits`, the nominal V2/C02 release interpretation, all
quality and injection flags, and the known L1 warning: **L1 `NO_CW_HW_INJ` is
clear throughout; samples are retained, and neither injection absence nor
negligible effect is claimed.** DATA is set throughout; DQ masks are 127,
H1 injection masks are 31 and L1 masks are 23. Missing or altered flags refuse;
the known L1 clear bit is not a failure or a new veto. No additional calibration
correction or physical calibration bound is supplied.

The RI-83 result retains each segment's raw binary64 SHA-256, but its exported
sample arrays are the rounded demeaned and windowed arrays. They are **not**
the raw segment bytes. Recovering raw samples by adding a saved mean is invalid:
binary64 subtraction can round differently at each coordinate. The exact
identity `A 1 = 0` removes a common exact constant, not an arbitrary vector of
subtraction errors. Therefore this application must extract raw samples from
the retained identical HDF5 snapshots and reconcile every complete M-segment
hash with the accepted RI-83 raw hash. There is no new download or substitution
fallback if those operands or their custody are unavailable.

Freeze the following integers without reference to new observed values:

```text
fs = 4096; M = 16384; stride = 8192
N = 2769; L = 4096; T = N + 2 L = 10961
I = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
scenario order = (H1:left, H1:right, L1:left, L1:right)
left starts  = (0, 8192, 16384, 24576, 32768, 40960, 49152)
right starts = (69632, 77824, 86016, 94208, 102400, 110592)
```

For each detector X, side and listed start s, use half-open slices:

```text
u_s = X[s : s+16384]                   # original RI-83 M-vector
w_s = X[s : s+10961]                   # first T coordinates of u_s
x_s = X[s+4096 : s+6865]               # N-coordinate short center
z_s = (X[s:s+4096], X[s+6865:s+10961]) # left L, then right L
output sample i has index s+4096+i and exact GPS 1126259446+(s+4096+i)/4096.
```

This is precisely the `S=[I_T,0]`, `B=A S=[A,0]` map used in RI-92/97/100.
It is not a recentering of T inside M. The last `M-T=5423` coordinates of each
M-vector have zero action in B, although they remain part of the retained raw
segment identity and of the already fixed PSD construction. The left last M
segment ends at 65536, and the right last ends at 126976. All T and short slices
lie inside their M segment and side. No segment crosses `[65536,69632)`; the
right tail `[126976,131072)` remains unused. Thus the existing map **does permit
the proposed comparison** without padding, alignment or reselecting a crop.

For every M, T and short slice retain start/end and exact rational clock
offsets. Flag rows are the integers `floor(start/fs)` through
`ceil(end/fs)-1`; a partly covered one-second row is included. In particular,
T is not an integer number of seconds. Reconcile the M-segment flags and raw
hash with RI-83; derive the T/short annotations from the same full RI-37 masks.
The M windows overlap by 8192 samples; neighboring T windows overlap by
2769 samples. Distinct short centers do not establish independent outputs,
since the long inputs share samples. The detectors and sides remain separate.

## 2. The exact conventional operator and retained coefficient premise

Use the same exact finite rational filter F_m from RI-55/60: admitted binary64
coefficients interpreted as exact rationals, all 17 stage orders, finite odd
extensions, initial states, reversals and unpadding unchanged. This mathematical
operator differs from a rounded production recurrence. Let C select the
central N coordinates of a T-vector and J select I. Keep

```text
P = J F_N C,       Q = J C F_T,       A = Q-P.
p_s = P w_s,      q_s = Q w_s,       d_s = q_s-p_s = A w_s = B u_s.
```

All eight p, q and d components are in nominal strain units. Neither a longer
window nor q is ground truth. RI-104 does not reproduce a new full rounded
filter output, run an FFT, claim a bound on all 2769 outputs, or replace A by
an infinite-record transfer function. This deliberately small conventional
application reports the finite boundary sensitivity at the already selected
coordinates; it is not a measured error relative to the physical waveform.

Use the accepted **complete** original RI-73 interval capture, not the Gram G,
scalar radius maxima, midpoint Fourier rectangles, or a row hash as a numeric
operand. The normal and optimized original captures are separately retained:

```text
/Volumes/AI_DATA/development/det-review-evidence/ri73-execution/
  prep-20260924T213357Z-4493c189/actual-normal/INTERVALS.json
  prep-20260924T213357Z-4493c189/actual-optimized/INTERVALS.json
```

Each is 51891508 bytes, SHA-256
`fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba`.
Future execution uses a new retained identical snapshot of the normal capture,
with the completed RI-73 capture/reconciliation and later accepted usage chain
bound as premises. The optimized capture is a historical equality reference,
not a second set of coefficient measurements. Do not silently reconstruct
missing coefficients or treat the old reconstruction as newly run.

The closed compact schema is `ri73-reconstructed-intervals-v1`, dimensions
N/L/T, exact row order I, and eight records with keys `long,row,short`.
Each short list has N ordered reduced hex-rational endpoint pairs, each long
list T. There are 109840 inherited intervals in total. For row i and coordinate
j, denote the long interval `[q^-_ij,q^+_ij]` and the embedded short interval
`[p^-_ij,p^+_ij]` (zero outside the center). Form

```text
[a^-_ij,a^+_ij] = [q^-_ij-p^+_ij, q^+_ij-p^-_ij]
m_ij = (a^-_ij+a^+_ij)/2;  r_ij = (a^+_ij-a^-_ij)/2 >= 0.
```

This preserves the coordinate order left, center, right. Accepted exact A
annihilates constants; its interval row sum must contain zero, but its midpoint
row sum need not be zero. Do not project or renormalize the midpoint row.

Reuse the already reviewed RI-93 streaming grammar/custody approach, adapted
only to return the short/long intervals needed here. Bind the complete capture
before parsing; decode at most one row at a time; check exact compact canonical
row bytes, all keys/types/lengths/order/endpoints, fixed header/footer, EOF and
the unique ninth-item exhaustion sentinel. Preserve its 8 MiB per-row and
64 MiB complete-snapshot limits. Hash the bytes actually consumed, compare
descriptor/device/inode/size/timestamps before and after, and recheck the full
identity. A separate validator must independently decode the retained capture;
it must not trust the producer's iterator or successful gate booleans.

## 3. Interval outputs and exact finite side centering

Every raw binary64 sample is interpreted as its exact dyadic rational. Preserve
its original bits, including signed zero, in the raw binary artifacts; the
rational numerical value of either signed zero is zero. No binary64 mean
subtraction, Hann window, detrending, taper, normalization or PSD calculation
is applied to these operator inputs. The earlier periodic-Hann PSDs remain
unchanged model inputs; their preprocessing is not an instruction to taper A.

For any exact vector v in this application, define

```text
c_i(v) = sum_j m_ij v_j
e_i(v) = sum_j r_ij |v_j|
D_i(v) = [c_i(v)-e_i(v), c_i(v)+e_i(v)].                 (1)
```

Since the one true coefficient obeys `|A_ij-m_ij| <= r_ij`, the triangle
inequality proves `(A v)_i in D_i(v)`. This does not posit independent interval
errors or claim that all endpoint choices are jointly attainable. For raw
w_s additionally retain short and long signed-endpoint interval dot products
`P_i(w_s)`, `Q_i(w_s)`. Require the direct D_i(w_s) and interval difference
`Q_i(w_s)-P_i(w_s)` to have nonempty intersection. Preserve both routes and
do not replace the direct result by an adaptively selected narrower interval.

For each separate side with n=7 or n=6, define the **exact coordinatewise** mean
input and centered input vectors

```text
bar_w = (1/n) sum_s w_s
v_s = w_s-bar_w
bar_d = A bar_w = (1/n) sum_s d_s
h_s = A v_s = d_s-bar_d;        sum_s h_s = 0.           (2)
```

This aligns coordinates relative to each fixed window start, with no fitted
lag. It subtracts the finite side's coordinatewise mean vector; it does not
estimate and remove one scalar temporal mean within each segment. It uses all
windows with their unequal fixed counts and gives no added population-mean
premise. Compute c/e from (1) for bar_w and each v_s. Centers satisfy the exact
linear identities `c(bar_w)=mean c(w_s)` and `c(v_s)=c(w_s)-c(bar_w)`; verify
them. Independently sum the interval output means and require intersection
with the directly computed D(bar_w). Require zero in the sum of centered
intervals. These are consistency checks, not equality claims for interval
endpoints and not replacements for direct input centering.

Retain the previously fixed RI-62 numerical usefulness gate for each direct
A-dot enclosure, now applied to raw, mean and centered inputs:

```text
width(D_i(v)) <= (1/10^12) max_j |v_j|;  if v=0, D_i(v)=[0,0].   (3)
```

The same threshold is frozen before observations; no absolute strain floor,
data-based relaxation, row removal or precision increase is allowed. Applying
it to the new finite vectors is a new check, not a claimed earlier success.
This is a deterministic enclosure-width gate, not a small-discrepancy or
physical-noise criterion. Failure is a retained inconclusive application
outcome and must not start an automatic enclosure-improvement loop.

For `[l,u]`, define its exact nonnegative square enclosure

```text
sq([l,u]) = [0,max(l*l,u*u)] if l <= 0 <= u,
            [min(l*l,u*u),max(l*l,u*u)] otherwise.
```

Use this fixed map, summation and division by n to retain, per component i,

```text
U_i = (1/n) sum_s d_si^2                 # uncentered observed second moment
M_i = bar_d_i^2                         # squared finite side mean
V_i = (1/n) sum_s (d_si-bar_d_i)^2        # centered observed second moment
U = sum_i U_i; Mbar = sum_i M_i; V = sum_i V_i.           (4)
```

The input of sq for V_i is the **direct** D_i(v_s), not the much looser
difference of separately uncertain output intervals. Retain every component
contribution and all eight terms in each total. Divisor n is fixed: this is a
finite descriptive average, not an unbiased sample covariance estimate.

For exact point values, expansion of (2) proves
`U_i=V_i+M_i` and `U=V+Mbar`. All three interval constructions enclose those
same exact quantities; require nonempty intersection of U_i with V_i+M_i,
and of U with V+Mbar. Do not require equal interval endpoints or tighten the
reported primary intervals by intersection. Since the outputs share uncertain
coefficients, treating their intervals as independent probabilities is invalid.

## 4. What the four proxy comparisons mean

RI-100 supplies four accepted intervals for

```text
t_s = tr(B K_s B^T) = E ||B u-E(B u)||^2,
K_s = U_F* diag(lambda_s) U_F,
```

where U_F is the fixed unitary M-point Fourier matrix and lambda_s is derived
from the corresponding already accepted empirical PSD using the unchanged
DC/Nyquist/interior normalization. This design does not recompute any lambda,
transform, coefficient, fit, proxy enclosure or RI-100 ratio. Bind the complete
RI-100 result and final root arithmetic acceptance, and retain each scenario's
original final interval exactly, including any negative lower endpoint. Match
IDs, ordered rows, M/T/crop, nominal units, PSD source-record identities and
the inherited model/limitations; reject a same-shaped but different scenario.

The finite U, Mbar and V from (4) are displayed alongside **that side's** t
only. All four side rows are compulsory; there is no detector pooling, side
selection, ratio ranking, plot-driven tuning or empirical magnitude pass/fail.
No division by eight is introduced: each total and t is a sum of the same
eight squared output coordinates. A reviewer can assess whether the observed
boundary sensitivity is practically visible on these data, while the report
retains the distinct interpretation of every column.

Here is the precise centering/dependence limitation. For hypothetical random
vectors d_1,...,d_n with finite second moments, set mu_s=E d_s, bar_mu=mean mu_s,
and bar_d=mean d_s. Expanding the finite identity in (4) gives

```text
E V = (1/n) sum_s tr Cov(d_s) - tr Cov(bar_d)
      + (1/n) sum_s ||mu_s-bar_mu||^2.                    (5)
Cov(bar_d) = (1/n^2) sum_(s,t) Cov(d_s,d_t).
```

Under a common mean and common marginal covariance Omega this becomes
`E V=tr(Omega)-tr Cov(bar_d)`. Even if those assumptions held, overlap prevents
substituting Omega/n for the sample-mean covariance. Without common means
there is an additional mean-dispersion term. RI-100 supplies neither the joint
cross-window covariance nor the population means. Thus V is **not** justified
as an unbiased estimate of t; n/(n-1) is not an authorized repair. U also
contains unknown mean energy. No chi-square law, SNR, significance, coverage
probability or detector-noise validation follows from a numerical resemblance
between these columns.

Furthermore, the PSDs were calculated from these same already inspected M
segments. This comparison is development evidence with shared data, not a
held-out validation. The four finite circulant covariances are postulated
proxies, not known physical detector covariances. Periodic M-wraparound, the
T-principal crop, Welch estimation error, window dependence, possible signals
or injection effects, stationarity and physical calibration remain explicit
unproved premises. The word off-event still labels the inherited exclusion;
it does not mean signal-free. Unknown calibration behavior below 10 Hz is not
resolved by keeping or by comparing those modes. No native geometry/gravity
prediction or RET work is involved.

## 5. Complete retained result and independent verification contract

The future implementation must first publish a closed concrete schema and
source-only handoff implementing the following fixed field contract. All
rational numeric values use the same canonical reduced hex numerator/positive
denominator strings as the held exact consumers; interval endpoints are two
such values with `lo<=hi`. Integers, booleans and floats are not interchangeable.
Reject duplicate keys, nonfinite values, extra/missing keys and noncanonical
encodings. Numeric controls do not use Python assertions. The canonical
scientific JSON is ASCII, sorted keys, indent 2, finite-only, with one terminal
newline; normal and optimized execution must produce identical whole bytes.

Top-level sections are exactly `schema`, `phase`, `status`, `method`,
`provenance`, `inputs`, `operator`, `scenarios`, `checks`, `limitations`.
Use schema `ri104-observed-context-benchmark-v1` and distinguish the phases
`fabricated_qualification` and `fixed_observed_application`. `status` may claim
success only after every declared gate passes. Fabricated inputs/provenance
must be explicitly labeled and cannot pass the actual custody path.

* `method` fixes every integer/index/order above, the first-T crop, no raw
  input preprocessing, direct interval rule, n-divisor coordinatewise side
  centering, fixed square rule, exact threshold (3), nominal units, and the
  no-magnitude-test comparison rule. It is compared as a complete literal.
* `provenance` binds the complete reviewed source closure, genuine runtime,
  actual source/input custody decision and qualification acceptance, predecessor
  report/capture/full-input identities and external execution receipt locator.
  Deterministic scientific content excludes mode-specific execution timestamps
  and paths; outer custody binds them. No future acceptance fields are invented.
* `inputs` contains both detector file pins, full RI-37 metadata/flag identities,
  original raw-array identity and the 26 M-segment identities. Preserve two
  complete little-endian float64 arrays of length 131072 as exclusive artifacts
  (`H1-raw.f64le`, `L1-raw.f64le`, 1048576 bytes each), with shape/dtype/byteorder
  and SHA-256; these are an exact lossless export of the retained HDF5 samples.
  Full values need not be duplicated as giant JSON float lists. All raw/T/short
  slices are reproducible from these retained arrays and explicit indices.
* `operator` identifies the accepted full capture, row order and coefficient
  counts, A interval construction and accepted constant-annihilation premise.
  Preserve per-row exact coefficient midpoint/radius sum identities and the
  full capture bytes in the external closure. Do not copy only a scalar bound.
* `scenarios` is the fixed four-record list. Each record retains detector,
  side, n, all starts, full slice/clock/flag records and all eight p/q/d output
  enclosures for every window. Each d additionally retains c,e,width, exact
  input max-absolute scale and gate result. It also retains all eight direct
  side-mean enclosures, every centered d enclosure with its c/e/scale/width,
  all eight U_i/M_i/V_i square-sum records and their U/Mbar/V totals. Each
  record binds its RI-100 scenario and exact final trace interval, units and
  inherited model label. The complete coordinatewise bar_w is retained in
  four canonical rational-array artifacts (`H1-left-mean.json`,
  `H1-right-mean.json`, `L1-left-mean.json`, `L1-right-mean.json`), each length T.
  Centered vectors are exactly derived from the retained raw arrays and these
  means; do not retain a rounded substitute or replace means by hashes alone.
* `checks` retains complete fixed gate IDs and actual measured values/reasons:
  input/metadata/custody, full slice/hash reconciliation, coefficient grammar
  and endpoint order, every signed dot and width, mean/centering linearity,
  all square/energy intersections, scenario correspondence, artifact membership
  and independent full saved-result validation. No boolean-only summary is
  accepted as arithmetic evidence. There are exactly 26 windows, 208 raw A
  enclosures, 416 short/long enclosures, 32 mean A enclosures, 208 centered A
  enclosures, 4 scenarios and 6 application data artifacts. Result/stdout and
  external receipts are separately accounted output files, not data artifacts.
* `limitations` retains every interpretation boundary in sections 1–4 as fixed
  explicit statements. Success means reproducible finite computation only.

The six artifacts are complete and exclusively written, fsynced and inventoried;
the caller rejects a missing, extra, symlinked or changed file and reopens every
byte identity. Preserve both full HDF5 snapshots and the full interval capture
as input closure copies, distinct from the six output artifacts. Means contain
actual exact fractions, not only summaries. A full independent saved arithmetic
consumer must reconstruct outputs from those retained raw binary arrays and
an independently parsed accepted capture, recompute all means, centered inputs,
signed endpoint sums and square sums, reconcile raw hashes/metadata, and compare
all nested output fields and six artifacts. It may use endpoint-sign sums as
an independent arithmetic route to the producer's midpoint/radius formula.
It must not call producer arithmetic or accept supplied c/e/gate flags as an
oracle. The accepted interval validity remains an inherited premise; a second
dot-product implementation does not re-prove the adjoint reconstruction.

## 6. Bounded qualification before the actual input branch

Source review first establishes that the concrete implementation obeys this
design and that no observed input can be opened from its fixture entrypoint.
Then freeze a finite fabricated domain and real resources before executing
normal/optimized qualification. No observation selects tolerances or fixtures.
The following obligations are fixed; their exact named gate inventory and
artifact identities are made concrete with the implementation, before launch.

1. **Full index domain.** With labeled integer/rational dummy records of length
   131072 and sentinel labels in the excluded interval and unused right tail,
   independently enumerate all 13 starts/detector, M/T/short slices, GPS offsets,
   flag-row coverage and the eight output indices. Verify endpoint and overlap
   counts and all 26 raw-segment hashes. No target filter/FFT is needed. A
   deliberately altered first-T versus centered-T crop must refuse.
2. **Exact tiny outputs and centering.** Use
   `A0=((1,-1,0),(0,1,-1))`, three inputs
   `(1,0,-1),(0,1,-1),(1,1,0)` and separately the two inputs
   `(-1,2,0),(2,0,1)`. A separately authored endpoint evaluator computes every
   output, mean, centered output, square and energy, with zero radii. Compare
   every field, the n-divisor identity, and `U=V+Mbar`. Repeat with all inputs
   zero, a common exact constant vector, and signed amplitude scales -1 and 2;
   intervals change sign correctly and all energies scale by 1 and 4.
3. **Interval-box enclosure.** Give all six entries of A0 radius 1/16 and
   enumerate exactly all 64 coefficient endpoint matrices. For the same five
   inputs and each separate side, independently evaluate their exact outputs,
   finite means and energies and require containment in the frozen box formulas.
   Box corners need not annihilate constants; never apply the A1=0 premise to
   them. Include a non-corner center matrix, and compare the direct endpoint
   interval to (1). Negative samples and zero samples are compulsory. Include
   intervals wholly positive/negative, crossing zero and zero-width for sq.
4. **Same uncertain coefficients.** Retain a tiny case where separately
   subtracting output intervals is wider than evaluating a centered input,
   although both contain the exact centered response. A concrete scalar case
   is `a in [1,2]`, inputs 1 and 3: direct centered intervals [-2,-1],[1,2]
   and V in [1,4], while independent-output subtraction is wider. This guards
   the dependency-aware input-centering rule without assuming independence.
5. **Closed full-result fixture.** Construct a fully labeled fabricated pair,
   fabricated accepted-row source and four fixed scenarios under a non-observed
   phase. Validate complete production dimensions, six exact artifacts and
   canonical roundtrip; no synthetic pin impersonates a genuine historical
   input. The actual custody path must refuse fabricated status/pins. An exact
   full-dimension zero input gives zero outputs, means and energies.
6. **Intended-reason refusals.** Pin stable exception codes and require each
   expected first reason, including altered whole input or raw-segment hash,
   missing/changed flags (especially falsely set L1 CW bit), shape/nonfinite
   data, alternate start/crop/row order, missing/duplicate/extra coefficient
   row, bad/crossed/noncanonical interval, wrong signed endpoint multiplication,
   scalar temporal centering, n-1 divisor, wrong square lower endpoint,
   swapped scenario/trace, missing mean artifact, changed artifact bytes,
   duplicate JSON keys/types, false success, and relaxed width threshold.
   Explicitly fail a width example `[−1,1]` on input 1 under (3), and accept
   exact zero input. Every refusal uses the actual guard used by the full path;
   a fixture declaration alone is not evidence of a caught failure.

Items 3 and 4 are deliberately wide **containment/dependency algebra controls**,
not successful full-path application cases: their synthetic boxes cannot pass
the unchanged width gate (3). They exercise the same enclosure and square
primitives, while the actual width guard remains active on every full-result
fixture and the explicit refusal cases. Their containment success never
overrides a width refusal or qualifies those boxes as actual inputs.

Testing dot products of fabricated rows does not establish actual-row custody.
The later caller review must separately cover the actual input branch, both
bytes-before-parse ordering, inspector/source capture and full external closure.
The existing RI-62 floating/Decimal whole-array controls are not relabeled as
run here, and are not newly required for an implementation that performs only
exact rational interval contractions without a rounded filtering branch.

## 7. Execution prerequisites and stop conditions

After independent design acceptance, the next deliverable is one small
reviewable source packet: exact dot/centering/energy consumer, separately
authored full validator, finite qualifier and implementation note. Reuse the
accepted interval-reader and custody patterns with explicit source deltas;
do not import or execute an entire transform consumer as a side effect. This
design does not reserve repository files or start a new generic harness.

Before actual observed execution, the coordinator must have accepted the full
source packet, real fabricated qualification in normal and optimized modes,
and the concrete actual caller/source/input closure. Bind the already qualified
CPython 3.11.6 / NumPy 2.1.3 / SciPy 1.14.1 / h5py 3.12.1 / HDF5 1.12.2 runtime,
named interpreter symlink chain and target bytes, complete runtime/build
fingerprint and dependencies. Reuse the actual qualified supervisor with a
narrow reviewed adapter. Freeze serial normal then optimized commands,
single numerical worker environment, exclusive outputs and all sources before
any observed parse. Root alone issues the appropriate actual admissions.

Keep 180 seconds of numerical child time and 524288 KiB **sampled child RSS**,
poll target 0.025 s, maximum admitted sampling gap 0.1 s and ps timeout 0.05 s,
including the final sample-to-reap gap. These are a monitored execution budget,
not an OS-enforced memory cap or a guarantee that exact dot products will finish.
Retain raw attempts, failures, actual OS exit, stdout/stderr, partial artifacts
and before/after source/runtime/input identities. Stream interval rows and JSON;
release row objects rather than keeping eight Fraction matrices simultaneously.
Reuse exact common-denominator integer sums where algebraically identical and
reviewed; do not round to float for speed. Keep the inherited 262144-bit limit
on admitted rational inputs and reduced completed-operation numerator and
denominator values; do not falsely claim this bounds internal temporary
cross-products of a Fraction implementation. Any resource/width/custody failure
remains a failure with no automatic retry, gate relaxation or operand change.

The independent completed review must verify genuine two-mode custody and full
result/six-artifact byte equality, followed by the independent saved arithmetic
comparison. A correct internal validator alone does not establish observation
custody or substitute for that review. Preserve historical failures, source-only
templates and every predecessor; only a later explicit accepted record can
assert actual RI-104 success. Authorized work can continue through these gates
without asking the user to reapprove the same measurement programme.

The remaining prerequisites are concrete, rather than a demand for a new
physical covariance law: fresh identical raw/capture snapshot custody, complete
source/caller review and meaningful fabricated qualification, actual bounded
execution and independent saved arithmetic/custody acceptance. Physical
covariance adequacy, joint cross-window law, calibration bounds, protected
validation and a native forward map remain separate blockers for stronger
claims; they do not block this descriptive conventional measurement.

## 8. Source references and limits of this author's review

`PREDECESSOR_PINS.json` alongside this draft records exact current source,
design, metadata and accepted-audit identities read or hashed during authoring.
It is a source-reference manifest, not a complete executable freeze. Principal
numerical bodies must be bound before future use, including the complete
RI-83 result (38952074 bytes,
`e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f`)
and complete RI-100 result (8844567 bytes,
`37dc6865be52e6888bcf325022a18cef65e5b3dd8bf1ba2a9f287e1c12d929dc`).
The accepted RI-100 normal result locator is
`/Volumes/AI_DATA/development/det-review-evidence/ri100-execution/application-preparation-uhq7i_49/controls/normal/RESULT.json`;
its independent audit is
`/Volumes/AI_DATA/development/det-review-evidence/ri100-saved-audit-execution-8dv7l7vg/controls/normal/REPORT.json`
(79442 bytes, `a6d0ea5592a9716f053322904effc6aa64945ac1e3d6e9d9e4dd7d31e438f03d`).
The root final RI-100 adjudication is
`/Volumes/AI_DATA/development/det-review-evidence/ri102-ri100-root-review-hnltxouk/RI100_ROOT_FINAL_ADJUDICATION.json`
(7451 bytes, `499fddd1a5315fb8c14c39ae8d161ab11e12f53f8f640d814b1ed81e2f780d21`).
Later published copies may be used only at these exact scientific byte pins,
with their actual publication record added; a prospective path is not evidence
of publication. All transitive accepted premise and runtime records must be
enumerated and freshly reconciled in the later concrete closure.

The author previously wrote measurement callers and the RI-98 product-form
validator, and reviewed several predecessors. This note is a new design by
that author, not an independent review of their own code. Independent proof
review and root adjudication remain required. Authoring performed no observed
HDF5 read, coefficient reconstruction/decoding, filtering, FFT, source import,
numerical qualification, application execution, new data acquisition or
repository/Git change. No existing protected validation or RET work was opened.
