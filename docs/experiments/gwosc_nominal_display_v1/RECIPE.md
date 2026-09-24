# RI-42 — frozen design for a nominal GW150914 V2 strain display

24 September 2026 UTC. **Design only; implementation and numerical validation
have not been performed.** This recipe fixes the proposed conventional display
before observed waveform processing. RI-44 is to implement and independently
qualify its numerical operations on synthetic inputs, then pin the qualified
coefficients before applying them to the already qualified public strain pair.
No successful test or produced waveform is claimed by this note.

## 1. Inputs, observable and scope

Use exactly the 32-second, 4096 Hz V2 files from
[RI-37](../gwosc_input_qualification_v1/QUALIFICATION.md):

| Detector / file | Bytes | SHA-256 |
|---|---:|---|
| H1 / `H-H1_LOSC_4_V2-1126259446-32.hdf5` | 1040592 | `6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6` |
| L1 / `L-L1_LOSC_4_V2-1126259446-32.hdf5` | 1007420 | `56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189` |

Before HDF5 parsing, verify both complete byte snapshots against these sizes,
SHA-256 values and RI-37's publisher MD5 values. Parse those same snapshots and
revalidate the declared schema, sample grid, finite samples and quality flags.
Do not substitute another release, a longer product or overlapping samples.

Each input has `N=131072` samples at
`t_i=1126259446+i/4096`, `0 <= i < N`. Use integer indices and exact rational
offsets to define intervals, not a floating-point comparison of large GPS
timestamps. The nominal observable is the released dimensionless calibrated
strain, subject to its subsequent filter response; the literal HDF5 `Yunits`
attribute remains empty. No uncertainty band is attached.

[RI-40](../gwosc_calibration_qualification_v1/QUALIFICATION.md) qualifies the
nearest C02 uncertainty tables at H1 GPS `1126260391` and L1 GPS `1126257729`,
with midpoint offsets `+929` and `-1733` seconds. Their pointwise statistical
summaries supply no deterministic time-dependent envelope or joint error law.
This recipe applies no extra calibration correction or uncertainty draw.

Retain all RI-37 DQ/injection annotations. In particular, L1's `NO_CW_HW_INJ`
bit is clear throughout the input interval. Retain and label those samples for
this nominal display; claim neither injection absence nor a negligible effect.
Any inference requiring either claim remains outside this packet.

## 2. Fixed filtering and display choices

The source is the nominal time-domain branch of the historical
[official GWOSC tutorial](https://gwosc.org/s/events/GW150914/GW150914_tutorial.html#Time-domain-filtering---Bandpassing+notching),
also available as [publisher Python source](https://gwosc.org/s/events/GW150914/GW150914_tutorial.py).
Its code uses 43–260 Hz, despite nearby prose saying 40–300 Hz. Its notch helper
does not use its `order=4` argument, and its apparent 100 Hz renormalization is
not applied. The tutorial is unmaintained and refers to V1. This is an explicit
SOS adaptation on qualified V2 data, not a reproduction of its shifted/inverted
plot or the discovery paper's Figure 1.

Freeze CPython **3.11.6**, NumPy **2.1.3**, SciPy **1.14.1**, and h5py **3.12.1**.
Use NumPy CPU `float64` arrays and SciPy's digital designs, with `fs=4096`.
No optional array backend is admitted. The ordinary interpreter and `-O` must
retain all checks; use explicit runtime failures, not removable assertions.

There are 17 ordered stages. Stage 0 is
`butter(4, [43,260], btype="bandpass", analog=False, output="sos", fs=4096)`.
The prototype order is four: the one-pass bandpass has order eight/four SOS
sections. Forward–backward filtering squares its magnitude response.
[SciPy Butterworth specification](https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.signal.butter.html).

Stages 1–16 are the following `(center, pass half-width, stop half-width)`
triples, in Hz and in this order:

```text
(14,1,0.1), (34.70,1,0.1), (35.30,1,0.1), (35.90,1,0.1),
(36.70,1,0.1), (37.30,1,0.1), (40.95,1,0.1), (60,1,0.1),
(120,1,0.1), (179.99,1,0.1), (304.99,1,0.1), (331.49,1,0.1),
(510.02,1,0.1), (1009.99,1,0.1), (510,200,20), (331.5,10,1)
```

For each triple `(f,d,s)`, design
`iirdesign([f-d,f+d], [f-s,f+s], gpass=1, gstop=6, analog=False,
ftype="ellip", output="sos", fs=4096)`. Decimal literals are converted once to
binary64, and interval-edge arithmetic uses binary64. The pinned design
routine determines the minimum notch order; record the actual section counts.
Retain its gain without additional normalization.
[SciPy IIR design specification](https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.signal.iirdesign.html).

For every stage, apply `sosfiltfilt` to the complete current detector array,
with `axis=-1`, `padtype="odd"` and explicit integer padding

```text
m = 3 * (2 * number_of_sections + 1
         - min(number_of_exact_zero_b2, number_of_exact_zero_a2))
```

Coefficient columns are `[b0,b1,b2,a0,a1,a2]`. Require `m < N-1` and `a0=1`
in every section. Pad independently at each stage, use the same SOS order for
both passes, remove that stage's padding, then advance to the next stage.
Do not concatenate the 17 stages into one forward–backward call or filter
individual biquads forward–backward separately; their boundary operations
would differ. [SciPy SOS forward–backward specification](https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.signal.sosfiltfilt.html).

Process H1 and L1 separately with the same coefficients. Baseline removal is
**none**: no mean subtraction or trend fitting. Apply no taper, whitening, PSD
estimate, decimation, clipping, fitted amplitude scale, sign change or time
shift. There is no taper before or after filtering.

Only retain the display crop `output[65536:69632]`: 4096 samples at GPS
`[1126259462,1126259463)`. Its local axis is `j/4096`, `0 <= j < 4096`, labeled
seconds after GPS `1126259462`. Show two detector panels on the same nominal
strain scale with the stated processing and CW annotation. No detector-specific
normalization or alignment is allowed. Axis limits may encompass the full
displayed values but must not clip points or rescale one detector independently.
All other filtered samples are outside the admitted display crop. Filtering is
offline and noncausal; this is not a detector-trigger or arrival-time estimator.

## 3. Synthetic qualification before observed transformation

The tests and tolerances below are prospective requirements, not results.
Run them before reading observed strain amplitudes. Failed requirements stop
admission. Diagnose and record a failure; do not loosen tolerances, change
filters or adjust the crop to obtain a desired observed waveform. A design
revision requires an explicitly identified replacement recipe and renewed
synthetic qualification before observed processing.

First require finite coefficients and poles strictly inside the unit circle.
Record all stage orders, padding lengths and DC gains. Design a separate ZPK
representation using the same pinned design specifications. Evaluate its
transfer function directly as `k*product(z-zero)/product(z-pole)`, with
`z=exp(2*pi*i*f/4096)`. Independently evaluate the SOS polynomials in `z^-1`.
Do not use a SciPy frequency-response helper for either evaluation.

The fixed frequency set is the sorted union of `j/16` Hz for integer
`0 <= j <= 32768`, `{43,260}`, and each notch's center and four pass/stop edges.
Use the same binary64 frequency value for both evaluations. Require maximum
absolute complex-response difference **<= 1e-8 for each stage**, and maximum
absolute difference **<= 1e-8** for the final real gain
`G(f)=product(abs(H_stage(f))**2)`. These checks independently evaluate the
representation and cascade arithmetic; the ZPK and SOS designs still share
SciPy's design implementation and are not an independent filter-design proof.
Use the directly evaluated ZPK value of `G(f)` for the tone reference below.

### Independent recurrence reference

Use an independently authored scalar direct-form-I reference, not a wrapper
around SciPy filtering or its initialization helpers. Set Decimal precision
to **80 significant decimal digits**, rounding `ROUND_HALF_EVEN`. Convert each
frozen binary64 coefficient and synthetic input sample to its exact Decimal
value before performing reference arithmetic. For each section use

```text
y[n] = (b0*x[n] + b1*x[n-1] + b2*x[n-2]
        - a1*y[n-1] - a2*y[n-2]) / a0
DCgain = (b0+b1+b2)/(a0+a1+a2)
```

Require each DC denominator nonzero. For an input array `v` of length `L`,
construct the odd extension explicitly: left entries are `2*v[0]-v[k]` for
`k=m,m-1,...,1`; right entries are `2*v[L-1]-v[k]` for
`k=L-2,L-3,...,L-m-1`. Keep the original array between them.

For the forward cascade, the first section has constant prehistory
`x[-1]=x[-2]=extended[0]` and `y[-1]=y[-2]=DCgain*extended[0]`.
For section `j`, its input prehistory is exactly
`c_j=extended[0]*product(DCgain_k for k<j)` and its output prehistory is
`DCgain_j*c_j`. Do not initialize every section with the original input value.
Pass the complete forward output through the same ordered cascade in
reverse time, initializing its first input prehistory from the last forward
output and propagating DC gains in the same way. Reverse the result back and
remove `m` entries from each side. Repeat this operation for each of the 17
stages, including its own extension and initialization.

Use five fixed synthetic arrays of length `L=2048`, with `t_j=j/4096`:

- all zeros;
- all ones;
- the ramp `2*j/(L-1)-1`;
- a unit impulse at index `1024`, zero elsewhere;
- `(sin(2*pi*40*t_j)+cos(2*pi*60*t_j)+sin(2*pi*100*t_j)
  +cos(2*pi*300*t_j))/4`.

Construct each once as binary64 and supply exactly those sample values to
both implementations; use NumPy's `sin`, `cos` and binary64 `pi` in the stated
formulas, with binary64 arithmetic throughout fixture generation. Save their
byte identities. Across **every output
sample**, require the maximum absolute difference between SciPy's result
and the Decimal result **<= 1e-9 * max(1,max(abs(input)))**. Evaluate the
comparison against the Decimal result without first rounding it to binary64.
This tests arithmetic and finite-array boundary handling, including transients.

### Production-length tone and context checks

Use unit tones at frequencies
`{0,10,43,60,100,120,179.99,260,331.5,510,1009.99,1500}` Hz,
each with phases `0` and `pi/3`. Generate 128 seconds as
`sin(2*pi*f*t_j+phase)`, with `t_j=j/4096-64` and
`0 <= j < 524288`, using the same NumPy binary64 generation convention.
The central 32-second input is the exact array slice
`[196608:327680]`, not a separately regenerated sinusoid. These are entirely
synthetic longer inputs; acquire no longer strain context.

For each fixture, filter both lengths using the frozen stagewise procedure.
The comparison crops are `[65536:69632]` in the 32-second result and
`[262144:266240]` in the 128-second result; both correspond to `[0,1)` in
the synthetic time coordinate. Require the infinity norm of their difference
**<= 1e-3**. Also require the 32-second crop to differ from
`G(f)*input_crop` by infinity norm **<= 1e-3**. These are absolute tolerances
in units of the unit-amplitude input, including frequencies with near-zero
output; use no relative division by the filtered amplitude, fitted phase,
shift or amplitude. The zero-phase zero-frequency fixture is deliberately
zero; the other phase supplies a nonzero constant-input check.

These tests bound discrepancies on the declared fixtures. They do not prove
a uniform bound for arbitrary signals or certify the physical continuation
of the observed strain outside the acquired interval. A central crop is an
edge-treatment choice, not a claim that IIR transients are identically absent.

## 4. Numerical identity, admission and deliverable

Before observed transformation, publish the synthetic qualification record:
actual commands and interpreter/platform identity; package and HDF5 versions;
OS, machine architecture, byte order and NumPy numerical-library configuration;
test-input identities; every measured maximum residual, its tolerance and
pass/fail result; and explicit normal/`-O` agreement. Do not substitute a
single aggregate PASS for the measured residuals or hide failed attempts.

For each ordered stage, record its SOS shape, padding length, every coefficient
as its exact binary64 hexadecimal string, and SHA-256 of its C-order,
little-endian binary64 matrix bytes, with columns `[b0,b1,b2,a0,a1,a2]`.
Preserve section order and signed zeros. Pin an ordered coefficient manifest;
its SHA-256 is computed from ASCII JSON with sorted object keys,
`ensure_ascii=True`, separators `(',',':')`, and no trailing newline.
Include stage index, specification, shape, coefficient hex strings, matrix
digest and padding length. Use these qualified coefficient values for the
subsequent display; refuse changed identities rather than silently accepting
a new numerical design or runtime. Any platform dependence is execution
provenance, not instrument provenance.

RI-44's synthetic implementation and independent review must establish this
admission record before observed filtering. This recipe alone does not authorize
claiming that the proposed tolerances are met. After admission, the bounded
deliverable is the fixed nominal V2 display and reproducible indexed numeric
crop, with input, coefficient, source and runtime identities and the retained
quality/injection annotations. No extra waveform template is needed.

There is no PSD whitening, noise significance, confidence interval, precise
intersite delay, newly established detection or DET-versus-GR comparison.
Those require separate models and evidence. The work uses public LIGO/Virgo
data, with the [GW150914 release DOI](https://doi.org/10.7935/K5MW2F23) and
[GWOSC acknowledgement](https://gwosc.org/data/). The accepted calibration and
clock contracts, native-proof obligations, protected evidence and RET pause
remain unchanged.
