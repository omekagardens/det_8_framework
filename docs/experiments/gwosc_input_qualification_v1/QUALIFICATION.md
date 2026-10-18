# RI-37 — inspected GW150914 V2 inputs

24 September 2026 UTC. This packet acquires and inspects the exact two public
files selected in the accepted [RI-33 contract](../observer_channel_v1/CONTRACT.md).
It advances ME-02 of the [native geometry/gravity/measurement programme](../../coordination/NATIVE_GEOMETRY_GRAVITY_MEASUREMENT_PLAN.md).
The admitted result is **verified fixed-file identity and declared schema/grid,
with inspected finite-sample and quality/injection status**. Calibration-dependent
inference and a conventional transient reproduction remain separate work.

No waveform plot, filtering, shifting, noise estimation, fit, inferred arrival
lag or detection statistic was produced. No native law is compared with these
observations. The acquired bodies stayed in external temporary storage; the
repository contains only this guide, the fixed-file inspector, its metadata
report and its two pinned Python dependencies.

## 1. Exact inputs and acquisition evidence

The [official event release](https://gwosc.org/events/GW150914/), DOI
[10.7935/K5MW2F23](https://doi.org/10.7935/K5MW2F23), links this corrected V2
4096 Hz pair. The strain product version is distinct from catalogue revisions.
The publisher maps V2 to C02 calibration; that interpretation is external
release metadata, not a literal calibration field inside these two files.

| Detector / filename | Bytes | Publisher MD5, locally matched |
|---|---:|---|
| H1 / `H-H1_LOSC_4_V2-1126259446-32.hdf5` | 1040592 | `50441a42c13fc1f14e5c4ea5527f1515` |
| L1 / `L-L1_LOSC_4_V2-1126259446-32.hdf5` | 1007420 | `361ae6a040a9fef7897b1e0124d5b0a1` |

Local SHA-256 identities:

- H1: `6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6`.
- L1: `56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189`.

Exact sources are the [H1 product](https://gwosc.org/GW150914data/H-H1_LOSC_4_V2-1126259446-32.hdf5)
and [L1 product](https://gwosc.org/GW150914data/L-L1_LOSC_4_V2-1126259446-32.hdf5).
Both returned HTTPS 200 at those same response URLs. Retrieval completed at
`2026-09-24T02:15:14.733084+00:00` and
`2026-09-24T02:15:15.434045+00:00`, respectively. The official
[checksum manifest](https://gwosc.org/GW150914data/md5.txt) was independently
retrieved first at `2026-09-24T02:15:14.004969+00:00`: 3352 bytes, SHA-256
`1411e50b88c58f791edfc1d170cfe1ce459433deca57a474b6c7b55471a6f8f0`.
Its selected entries agree with RI-33's pins and the actual bodies. The web
reader could not retrieve that manifest, but the ordinary HTTPS acquisition
succeeded; no missing source was replaced by an assumed value.

MD5 supplies the publisher's transfer comparison; local SHA-256 binds the
particular acquired bytes. Neither establishes instrument calibration or an
independent chain of custody. These are public reference/development inputs,
not protected or blind evaluation data. Prior access to the release pages and
published event interpretation was already known. This packet additionally
read the sample arrays to count finite/nonfinite entries and inspect flags;
it did not examine their amplitudes, extrema or a waveform display.

## 2. Actual file structure and declared time grid

Both files identify the expected detector and observatory, type
`StrainTimeSeries`, GPS start `1126259446`, duration `32`, and UTC-start string
`2015-09-14T09:50:29`. Each `strain/Strain` dataset contains **131072 float64
samples**. Its declared grid is `GPSstart + i/4096`, with integer indices
`0 <= i < 131072`, covering `[1126259446,1126259478)`. The last sample is
`1126259478 - 1/4096`; the exclusive end is not another acquired sample.

The file has no separate timestamp array. The grid is reconstructed from
`Xstart`, `Xspacing`, `Npoints`, shape and the independent metadata start/duration.
This consistency check does not independently calibrate hardware timing.
Strain `Xunits` is `second`, `Ylabel` is `Strain`, and **`Yunits` is an empty
string**. Dimensionless calibrated strain is the release's interpretation;
this report preserves the literal empty unit attribute rather than inventing
an explicit unit string or raw acquisition-channel name.

Both 1 Hz mask arrays contain 32 uint32 values and have matching GPS starts,
spacing, point counts and second units. Their seven DQ names and five injection
names/descriptions are read in the selected file's bit order. The report keeps
raw masks and all set/clear intervals, including the publisher's literal text.

## 3. Actual quality, missingness and injection findings

| Finding | H1 | L1 |
|---|---:|---:|
| Finite strain samples | 131072 | 131072 |
| NaN / infinite samples | 0 / 0 | 0 / 0 |
| DQ mask for every second | 127 | 127 |
| Injection mask for every second | 31 | 23 |
| `NO_CW_HW_INJ` set | 32 seconds | 0 seconds |
| `NO_CW_HW_INJ` clear | 0 seconds | 32 seconds |

Every published DQ bit is set throughout both files: DATA, the three CBC
categories and the three burst categories. The DATA mask agrees with all
4096 finite samples in every corresponding second. There are no DATA-excluded
intervals or unexplained missing samples in this pair.

Injection bits have the opposite practical reading to a presence flag:
**one means no injection of that named class**. H1 has all five bits set.
L1 has its continuous-wave bit clear over the full
`[1126259446,1126259478)` interval; the other four no-injection bits are set.
The correct finding is therefore that the released L1 flags do not assert
absence of continuous-wave hardware injections. The pair is not wholly
injection-free. This is a flag-based finding, not an independently measured
injection amplitude, frequency or effect on a proposed statistic.

Passing DQ flags does not establish absence of noise. A cleared injection bit
is not a missing strain sample and does not silently discard the detector.
This packet selects no analysis-specific veto policy. A later policy requiring
all hardware-injection classes absent would exclude the entire L1 interval;
any narrower treatment needs the statistic's stated scientific justification.
Flag semantics follow the [release technical notes](https://gwosc.org/techdetails/).

## 4. Calibration and analysis readiness

The [technical notes](https://gwosc.org/techdetails/) explain that V2 corrected
the old approximately 1 ms downsampling offset, uses C02, and that content
below 10 Hz is uncalibrated. They also distinguish independently downsampled
32-second and 4096-second products. No earlier V1 file or longer companion
was substituted here; overlapping products must not be assumed byte-identical.

The [public uncertainty archive](https://dcc.ligo.org/T2100313/public) and its
[README](https://dcc.ligo.org/public/0177/T2100313/003/README) remain the next
calibration inputs to qualify. O1 has detector-specific `FinalResults` files
with frequency-dependent magnitude/phase estimates and ±1-sigma boundaries;
phase is in radians and the embedded GPS value identifies the estimation
epoch. A leading creation date is not the observation time. O1 does not supply
the `MinMax` products described for other releases. These bands are not
simultaneous deterministic error bounds.

No uncertainty archive body, event-specific member, interpolation rule or
cross-frequency/detector correlation model was acquired or accepted here.
That gap blocks quantitative calibration-dependent amplitude/phase/timing
claims; it does not erase the verified input bytes or flag findings.
The HDF5 pair alone does not establish a calibrated timing-error budget.

Next: select the applicable H1/L1 C02 uncertainty records, justify their GPS
applicability and frequency/correlation treatment, and freeze a conventional
reproduction recipe before waveform processing. That recipe must specify
comparison intervals, filters/edge treatment, sample indexing, the CW-injection
policy and an independent reference. Any longer noise-estimation context must
be separately identified and qualified. A measured reproduction would still
not test DET without a native forward map to the same observable.

## 5. Reproducible fixed-file inspection

[inspect_inputs.py](inspect_inputs.py) reads only the two explicitly supplied
local files. It checks byte count, publisher MD5 and the local SHA-256 pin
before parsing the same byte snapshot in read-only mode. It validates the
selected schema/grid and reports every mask bit and its intervals. It performs
no network access, waveform transformation or repository write. Refusals use
explicit runtime checks and remain enabled under `-O`. This is a fixed-release
replay tool, not a general HDF5 ingestion API or a hostile-file security boundary.

[INPUT_REPORT.json](INPUT_REPORT.json) contains deterministic inspection output;
retrieval times above are acquisition evidence, not fields regenerated by replay.
[requirements.txt](requirements.txt) pins h5py 3.12.1 and NumPy 2.1.3. Root's
external isolated environment uses Python 3.11.6 and HDF5 1.12.2. No repository
virtual environment or dependency file was modified. Runtime versions belong
to execution evidence, not instrument provenance.

From the repository root, an external temporary replay can use:

```sh
ri37_bundle="$PWD/docs/experiments/gwosc_input_qualification_v1"
ri37_work="$(mktemp -d)"
python3.11 -m venv "$ri37_work/env"
"$ri37_work/env/bin/python" -m pip install --only-binary=:all: -r "$ri37_bundle/requirements.txt"
curl --fail --location --proto '=https' --proto-redir '=https' \
  'https://gwosc.org/GW150914data/H-H1_LOSC_4_V2-1126259446-32.hdf5' \
  -o "$ri37_work/H-H1_LOSC_4_V2-1126259446-32.hdf5"
curl --fail --location --proto '=https' --proto-redir '=https' \
  'https://gwosc.org/GW150914data/L-L1_LOSC_4_V2-1126259446-32.hdf5' \
  -o "$ri37_work/L-L1_LOSC_4_V2-1126259446-32.hdf5"
"$ri37_work/env/bin/python" -I -B "$ri37_bundle/inspect_inputs.py" \
  --input-dir "$ri37_work" > "$ri37_work/report.json"
cmp "$ri37_work/report.json" "$ri37_bundle/INPUT_REPORT.json"
```

Repeat the inspector with `-O` to check optimized execution. Missing, swapped,
truncated or modified inputs must refuse; do not update pins merely to make a
substituted file pass. Full acceptance, exact source hashes and actual replay/
negative-check results are recorded in the [coordination progress](../../coordination/REVIEW_PROGRESS.md).
The original contract and all native proofs remain unchanged by this packet.

## 6. Attribution

This packet uses public data provided through GWOSC by the LIGO and Virgo
collaborations. The release is distributed under CC BY 4.0; retain the dataset
DOI, product identifiers and [GWOSC acknowledgment guidance](https://gwosc.org/data/)
when reusing it. These observations were not produced by DET.
