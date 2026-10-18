# RI-40 — O1 calibration inputs for the selected GW150914 pair

24 September 2026 UTC. This packet qualifies public calibration inputs for
the exact V2/C02 strain pair inspected in [RI-37](../gwosc_input_qualification_v1/QUALIFICATION.md).
It supplies **pinned, detector-specific nearest-time uncertainty summaries**
and their two bracketing records. It does not supply a guaranteed waveform
error envelope, timing calibration, or a native DET observable.

The new [inspector](inspect_calibration.py) and [deterministic report](CALIBRATION_REPORT.json)
operate on the public archive and its documentation. No strain sample is read
or transformed in this packet. The original strain files, accepted contracts,
native proofs, protected evidence and RET pause remain unchanged. This advances
the public-data lane of the [programme](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md)
while QR independently works on RI-39.

## 1. Acquisition and identity

The source is [LIGO-T2100313-v3](https://dcc.ligo.org/T2100313/public).
The three bodies below were acquired by HTTPS into external temporary storage.
Each returned HTTP 200 at its requested URL. No archive or publisher program
is stored in the repository, and the publisher program was read, never executed.

| Body | Exact source | Bytes | Retrieval completed, UTC |
|---|---|---:|---|
| O1 archive | [LIGO_O1_cal_uncertainty.tgz](https://dcc.ligo.org/public/0177/T2100313/003/LIGO_O1_cal_uncertainty.tgz) | 12841275 | 2026-09-24T02:51:42.011055+00:00 |
| Documentation | [README](https://dcc.ligo.org/public/0177/T2100313/003/README) | 7585 | 2026-09-24T02:51:40.700541+00:00 |
| Example reader | [makeSamplePlot.py](https://dcc.ligo.org/public/0177/T2100313/003/makeSamplePlot.py) | 6147 | 2026-09-24T02:51:40.701675+00:00 |

Local SHA-256 identities, in the same order:

- Archive: `426c3e46242566351272d8b8a14044c1e97e8bd292ca2df74b0fee261bbc4d5c`.
- README: `fb4650601da797badc8bf9e068f798788842667a5bc27ae035ae5ffd0d311d7e`.
- Example: `548783b3010288c94430d54d4ac393a412f6c6afa8dbb3c3da8b41489fa80c7a`.

The web reader could not decode the archive or Python MIME types; ordinary
HTTPS acquisition succeeded. These are local identity pins tied to the stated
public source, not publisher-supplied checksums or independent instrument
authentication. No checksum manifest was supplied on the inspected DCC page.
Reproduction must refuse different bytes rather than silently refresh the pins.

The archive has **3784 entries**: three directories and 3781 regular files.
There are 2022 H1 and 1757 L1 `FinalResults` members, plus two detector-specific
O1 statistical summaries. No `MinMax` member occurs. The complete archive is
identity-checked; the four members below receive numeric table inspection.
The other 3777 regular files are inventoried, not numerically validated.

## 2. Time selection and its exact scope

The fixed strain interval is `[1126259446,1126259478)` GPS seconds. Choose its
midpoint `1126259462` as this qualification's reference; this is a declared
selection rule, not a fitted arrival time. The publisher's
[example reader](https://dcc.ligo.org/public/0177/T2100313/003/makeSamplePlot.py)
selects the available detector-specific estimation time with smallest absolute
distance to the requested time. It provides no maximum allowed gap or
deterministic drift guarantee.

| Detector | Previous estimate | Next estimate | Selected nearest | Selected minus midpoint |
|---|---:|---:|---:|---:|
| H1 | 1126256791 | 1126260391 | 1126260391 | +929 s |
| L1 | 1126257729 | 1126261329 | 1126257729 | -1733 s |

The same member is uniquely nearest throughout the 32-second interval. The
H1 switch between its bracketing estimates is at `1126258591`, before the
window; the L1 switch is at `1126259529`, after it. The inspector checks the
full detector inventory, including adjacent estimates outside these brackets.
This stable selection is an exact fact about timestamps, not evidence that
the underlying calibration is constant over the interval.

Both bracket members are retained for reproducibility and future sensitivity
design. They are not interpolated, combined into an envelope, or substituted
for one another. The earliest/latest H1 inventory estimates are `1125973168`
and `1137251384`; L1's are `1126073056` and `1137249662`. The inspected window
is within each inventory's range; this alone does not certify every time
between those endpoints.

The exact member names all have the pattern
`DETECTOR/Jun-28-2017_O1_SITE_GPSTime_GPS_C02_RelativeResponseUncertainty_FinalResults.txt`,
with `SITE=LHO` for H1 and `SITE=LLO` for L1. Each is 10605 bytes:

| Detector / GPS | Role | Member SHA-256 |
|---|---|---|
| H1 / 1126256791 | Previous bracket | `daaaf31118ec76dafa69973e9db4e75fe9dff210859b0bcec5129e026e7d0832` |
| H1 / 1126260391 | Selected; next bracket | `10e24d7b9d95c8eba55599a909cd052b1108fe924241ee9b2c52f5e1f1bec820` |
| L1 / 1126257729 | Selected; previous bracket | `53ea55a36ca4a593d9bc7c3890c428c8544878b6ea88bc1b9bd958fcd628aa0a` |
| L1 / 1126261329 | Next bracket | `430f4818af5f27183b92d50f368eb414b376d27f6d45a01f9fddce485fbd3733` |

The [release README](https://dcc.ligo.org/public/0177/T2100313/003/README)
associates O1 uncertainty products with final C02 strain. Embedded GPS values
are estimation times; the leading date is file creation. This agrees with
RI-37's externally documented V2/C02 mapping. There is no literal C02 field
inside the previously inspected HDF5 pair, and no event-time estimate exactly
coincident with this midpoint is invented here.

## 3. Actual numeric tables and conventions

Each of the four selected members has 100 seven-column rows. All entries are
finite decimals, frequencies strictly increase, magnitude entries are positive,
and each median lies between its corresponding lower and upper entries.
The common native grid runs from 5 to 5000 Hz.

| Column, zero-based | Interpretation |
|---|---|
| 0 | Frequency, Hz |
| 1, 2 | Median response-ratio magnitude and phase |
| 3, 4 | Lower 1-sigma magnitude and phase summaries |
| 5, 6 | Upper 1-sigma magnitude and phase summaries |

The [README](https://dcc.ligo.org/public/0177/T2100313/003/README) defines the
ratio as `eta=R_true/R_model`; magnitudes are dimensionless and phases are
radians. Its limits exclude calibration interpretation below 10 Hz and above
5000 Hz. In each inspected table, 10 rows are below 10 Hz, 77 satisfy
`10 <= f < 2048`, and 13 are at or above 2048 Hz. The 77-row subset runs from
10.046165 to 2018.5086 Hz. The extra 2048 Hz cutoff is the Nyquist boundary
of this particular 4096 Hz strain product, not a defect in the archive.
These partitions retain all input rows and choose no waveform analysis band.

[Sun et al., equation 9](https://arxiv.org/html/2005.02531#S2.SS5) gives the
orientation explicitly: multiplying the modeled response by eta produces
the true response. A later data/template nuisance convention must respect
that orientation; inversion or phase-sign reversal cannot be assumed.
The [publisher's display example](https://dcc.ligo.org/public/0177/T2100313/003/makeSamplePlot.py)
converts magnitude to percent excursion with `100*(value-1)` and phase to
degrees with `180/pi*value`. This packet keeps native units and applies no
correction to strain.

## 4. What the summaries do and do not qualify

[Cahillane et al., sections III.2–III.3 and Appendix A](https://arxiv.org/html/1708.03023)
describe the O1/O2 inference, including response draws assembled from uncertain
model components and central 68% contours; Appendix A explicitly revisits
GW150914/C02. The frequency-dependent Gaussian-process component includes
correlations. Seven per-frequency summaries do not specify a joint response
distribution across frequency, time or detectors.

The later methodological description identifies pointwise median and 16th/84th
percentile summaries, with systematic offsets retained inside the uncertainty
bands. Those are statistical summaries, not deterministic bounds, nor a joint
simultaneous confidence region. Its O3 interpolation practice is not an adopted
O1 prescription here. [Sun et al., sections 5.1 and 5.3](https://arxiv.org/html/2005.02531#S5)

The qualification supports selecting and inspecting the stated nearest-time
summaries for a conventional public-data demonstration. It does not justify:

- treating every table value as an independent Gaussian random variable;
- adding a boundary as though it were a standard deviation, then adding the
  systematic offset again;
- enclosing the true response between the two bracketing-time curves;
- extrapolating outside the valid/native frequency range or certifying an
  interpolation error without an additional model;
- turning a general frequency-dependent phase into one clock or arrival-time
  error bound;
- multiplying the V2 strain by another calibration correction merely because
  an uncertainty file exists.

These limitations concern particular precision inferences. They do not prevent
a clearly labeled nominal-strain display using the already calibrated V2
samples, provided its processing is frozen and its claims remain appropriate.
No fitted waveform, detection statistic, confidence band or time lag is
computed in this qualification.

## 5. Reproduction and next action

`inspect_calibration.py` verifies byte count and SHA-256 for all three inputs
before reading the archive's same in-memory snapshot. It reads regular members
without extraction to the filesystem, inventories epochs and parses the four
tables using exact decimal values. It emits deterministic JSON to stdout and
refuses mismatched inputs through explicit checks that remain active under
`-O`. It performs no network request or project import. This is a fixed-release
inspection tool, not a general archive security boundary.

An external temporary reproduction, from the project root, is:

```sh
ri40_bundle="$PWD/docs/experiments/gwosc_calibration_qualification_v1"
ri40_work="$(mktemp -d)"
for ri40_name in README makeSamplePlot.py LIGO_O1_cal_uncertainty.tgz; do
  curl --fail --location --proto '=https' --proto-redir '=https' \
    "https://dcc.ligo.org/public/0177/T2100313/003/$ri40_name" \
    -o "$ri40_work/$ri40_name"
done
python3 -I -S -B "$ri40_bundle/inspect_calibration.py" \
  --input-dir "$ri40_work" > "$ri40_work/report.json"
cmp "$ri40_work/report.json" "$ri40_bundle/CALIBRATION_REPORT.json"
```

Repeat with `-O`. No dependency installation is required. Actual interpreter,
replay, refusal and independent-review evidence is recorded in the
[progress record](../../coordination/REVIEW_PROGRESS.md); the report carries
input identities and inspection results, not regenerated acquisition times.

The next bounded measurement packet should freeze a **nominal V2 strain-display
recipe** before transforming these samples: exact sample indices and display
window, baseline removal, filter/window/edge treatment, frequency band,
reference comparison, and retained quality/injection annotations. Its purpose
is conventional reproduction, not a new detection or precise intersite timing
estimate. RI-37's L1 `NO_CW_HW_INJ` bit remains clear for the full interval;
a nominal display may retain and label those samples, but must not assert
injection absence or infer that the injection has no effect. Any claim needing
that absence or a quantified effect requires additional evidence. Longer noise
context, if needed, must be separately qualified.

Statistical calibration propagation requires an explicit temporal and joint
nuisance model before the associated confidence claim. A DET comparison also
requires a native forward map to the same observable. Those open obligations
do not block the bounded nominal reproduction step. Preserve the existing
clock contract, protected-validation/freeze prerequisites and published pins.

This work uses public LIGO/Virgo calibration products. Retain the DCC version,
member identities and calibration-method references when reusing this packet;
the observations and calibration estimates were not produced by DET.
